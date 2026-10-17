"""V15 fase 1.2 · Auditoría de datos, grupo FINANCIACIÓN Y MACRO (capa C4, descriptivo, sin efectos estimados).

Fuentes (todas de data/base/hechos.parquet con NOT coalesce(muestra_sellada_v6,false); data/raw solo para
reproducibilidad nacional y metadatos de manifiestos): hipotecas INE (HPT 76317), crédito y tipos BdE/BCE, EPA, ETCL,
CNT, CRE, Seguridad Social (municipal), SEPE, BLS, compraventas ETDP y visados MIVAU.
Cruces territoriales por código INE (data/base/territorios.parquet). Determinista (SEED=20261010), sin red, solo lectura.
Salida: output/v15/auditoria/financiacion_macro/ (CSV resumen y resultado.json). Sin datos crudos.
Uso: python3 src/v15/auditoria/financiacion_macro.py
"""
from __future__ import annotations

import glob
import json
import re
import warnings
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parents[3]
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v15" / "auditoria" / "financiacion_macro"
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
UMBRAL_Z = 5.0
MIN_OBS = {"T": 12, "M": 12, "A": 8}
LAG = {"T": 4, "M": 12, "A": 1}

# ---------------------------------------------------------------- utilidades


def pidx(p: str) -> int:
    p = str(p)
    if "T" in p:
        return int(p[:4]) * 4 + int(p[5]) - 1
    if "-" in p:
        return int(p[:4]) * 12 + int(p[5:7]) - 1
    if "M" in p:
        return int(p[:4]) * 12 + int(p[5:7]) - 1
    return int(p)


def lab(i: int, f: str) -> str:
    i = int(i)
    return {"T": f"{i // 4}T{i % 4 + 1}", "M": f"{i // 12}-{i % 12 + 1:02d}", "A": str(i)}[f]


def qlab(i: int) -> str:
    return lab(i, "T")


def qi(s: str) -> int:
    return pidx(s)


def limpia(o):
    if isinstance(o, dict):
        return {str(k): limpia(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpia(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else round(float(o), 4)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


# ---------------------------------------------------------------- carga


def variables_grupo() -> list[str]:
    inv = pd.read_csv(RAIZ / "docs" / "v15" / "inventario_variables.csv")
    inv = inv[inv.concepto.isin(["financiacion", "empleo", "renta", "otro"])]
    nombres = {v for v in inv.variable if not re.match(r"^(aeat_|adrh_)", v)}
    nombres |= {"compraventas", "visados"}
    return sorted(nombres)


def cargar() -> pd.DataFrame:
    lista = ",".join(f"'{v}'" for v in variables_grupo())
    con = duckdb.connect()
    df = con.sql(f"""select territorio_codigo c, nivel, periodo, frecuencia f, variable v, coalesce(desagregacion,'') d, valor,
        unidad u, edicion, fecha_dato, metodo_dato from '{HECHOS}'
        where not coalesce(muestra_sellada_v6,false) and variable in ({lista})""").df()
    df["p"] = [pidx(x) for x in df.periodo]
    return df


DF = cargar()
SER = {k: g for k, g in DF.groupby(["v", "nivel", "d", "f"])}  # la frecuencia forma parte de la clave (provincial A y T conviven)


def K(var: str, nivel: str, desag: str = ""):
    """Clave de SER para (variable, nivel, desagregación); prefiere la frecuencia T, luego M y A."""
    for f in ("T", "M", "A"):
        if (var, nivel, desag, f) in SER:
            return (var, nivel, desag, f)
    return None
TERR = pd.read_parquet(RAIZ / "data" / "base" / "territorios.parquet")
PROV2CCAA = dict(TERR.loc[TERR.nivel == "provincia", ["territorio_codigo", "cod_ccaa"]].itertuples(index=False))


def serie(var: str, nivel: str = "nacional", cod: str = "00", desag: str = "") -> pd.Series:
    k = K(var, nivel, desag)
    if k is None:
        return pd.Series(dtype=float)
    g = SER[k]
    g = g[g.c == cod]
    return pd.Series(g.valor.values, index=g.p.values).sort_index()


def panel(var: str, nivel: str, desag: str = "") -> pd.DataFrame:
    g = SER[K(var, nivel, desag)]
    return g.pivot_table(index="c", columns="p", values="valor", aggfunc="first").sort_index(axis=1)


def m2q(s: pd.Series, how: str = "sum") -> pd.Series:
    """Serie mensual (índice y*12+m-1) a trimestral (y*4+q-1), exigiendo los 3 meses."""
    q = (s.index // 12) * 4 + (s.index % 12) // 3
    g = s.groupby(q)
    r = g.sum() if how == "sum" else g.mean()
    return r[g.size() == 3]


def grid(s: pd.Series) -> pd.Series:
    return s.reindex(range(int(s.index.min()), int(s.index.max()) + 1)) if len(s) else s


def yoy_log(s: pd.Series, lag: int = 4) -> pd.Series:
    s = grid(s.dropna().astype(float))
    return np.log(s / s.shift(lag)) * 100


def runs(flag: pd.Series, minlen: int) -> list[tuple[int, int]]:
    out, ini, prev = [], None, None
    for t, f in flag.items():
        if f and ini is not None and t - prev == 1:
            prev = t
        elif f:
            if ini is not None and prev - ini + 1 >= minlen:
                out.append((ini, prev))
            ini, prev = t, t
        else:
            if ini is not None and prev - ini + 1 >= minlen:
                out.append((ini, prev))
            ini = None
    if ini is not None and prev - ini + 1 >= minlen:
        out.append((ini, prev))
    return out


def zrob1(x: pd.Series, minobs: int = 12):
    x = x.dropna()
    if len(x) < minobs:
        return None
    med = float(np.median(x))
    mad = float(np.median(np.abs(x - med)))
    if mad == 0:
        return None
    return (x - med) / (1.4826 * mad)


# ---------------------------------------------------------------- 1. atípicos


def es_tipo_dif(var: str, u: str) -> bool:
    return bool(re.search(r"%|puntos|porcentuales|pp", str(u))) or var.startswith(
        ("bls_", "dif_hip", "tipo_", "euribor", "inflacion", "tasa_paro", "bce_hip_tipo", "bce_cuota", "monitor_tipo"))


def zmat(X: np.ndarray, minobs: int):
    n = np.sum(~np.isnan(X), axis=1)
    med = np.nanmedian(X, axis=1)
    mad = np.nanmedian(np.abs(X - med[:, None]), axis=1)
    sd = np.nanstd(X, axis=1)
    cls = np.where(n < minobs, "corta", np.where(mad == 0, "mad_nula", np.where(1.4826 * mad < 0.1 * sd, "mad_casi_nula", "normal")))
    Z = (X - med[:, None]) / (1.4826 * np.where(mad == 0, np.nan, mad)[:, None])
    return Z, cls, med


def tasa_mat(X: np.ndarray, lag: int, dif: bool) -> np.ndarray:
    R = np.full_like(X, np.nan)
    A, B = X[:, lag:], X[:, :-lag]
    if dif:
        R[:, lag:] = A - B
    else:
        R[:, lag:] = np.where((A > 0) & (B > 0), np.log(np.where(B > 0, A, 1) / np.where(B > 0, B, 1)) * 100, np.nan)
    return R


def tarea1_atipicos():
    filas, tops, unid, dup_keys, transv = [], [], [], 0, []
    for (v, niv, d, f), g in SER.items():
        u = str(g.u.iloc[0])
        dup_keys += int(g.duplicated(["c", "p"]).sum())
        pv = g.pivot_table(index="c", columns="p", values="valor", aggfunc="first")
        pv = pv.reindex(columns=np.arange(pv.columns.min(), pv.columns.max() + 1))
        X = pv.values.astype(float)
        mo = MIN_OBS[f]
        dif = es_tipo_dif(v, u)
        Zn, cn, _ = zmat(X, mo)
        Rt = tasa_mat(X, LAG[f], dif)
        Zr, cr, _ = zmat(Rt, mo)
        norm_n, norm_r = cn == "normal", cr == "normal"
        big_n = (np.abs(Zn) > UMBRAL_Z) & norm_n[:, None]
        big_r = (np.abs(Zr) > UMBRAL_Z) & norm_r[:, None]
        cas = cr == "mad_casi_nula"
        nul = cr == "mad_nula"
        casi_atip = int(((np.abs(Zr) > UMBRAL_Z) & cas[:, None]).sum())
        desv_mad0 = 0
        if nul.any():
            med = np.nanmedian(Rt[nul], axis=1)
            desv_mad0 = int((np.abs(Rt[nul] - med[:, None]) > 0).sum())
        obs_r = int(np.sum(~np.isnan(Rt[norm_r])))
        filas.append({"variable": v, "nivel": niv, "desag": d, "frec": f, "tasa_tipo": "dif" if dif else "log_x100", "unidad": u,
                      "n_series": len(pv), "series_corta": int((cr == "corta").sum()),
                      "series_mad_nula": int(nul.sum()), "series_mad_casi_nula": int(cas.sum()), "series_z_valido_tasa": int(norm_r.sum()),
                      "obs_tasa_validas": obs_r, "atip_tasa": int(big_r.sum()),
                      "pct_atip_tasa": round(100 * big_r.sum() / obs_r, 3) if obs_r else np.nan,
                      "series_con_atip_tasa": int((big_r.sum(axis=1) > 0).sum()),
                      "atip_tasa_en_mad_casi_nula": casi_atip, "desv_distintas_de_mediana_en_mad_nula": desv_mad0,
                      "series_mad_nula_nivel": int((cn == "mad_nula").sum()), "series_mad_casi_nula_nivel": int((cn == "mad_casi_nula").sum()),
                      "atip_nivel": int(big_n.sum()), "series_con_atip_nivel": int((big_n.sum(axis=1) > 0).sum()),
                      "obs_nivel_validas": int(np.sum(~np.isnan(X[norm_n])))})
        for i, j in np.argwhere(big_r):
            tops.append({"variable": v, "nivel": niv, "desag": d, "cod_ine": pv.index[i], "periodo": lab(pv.columns[j], f),
                         "z_robusto_tasa": float(Zr[i, j]), "tasa": float(Rt[i, j]), "nivel_valor": float(X[i, j])})
        if len(pv) >= 10:
            med_t = pd.Series(np.nanmedian(Rt, axis=0), index=pv.columns)
            n_t = pd.Series(np.sum(~np.isnan(Rt), axis=0), index=pv.columns)
            zt = zrob1(med_t[n_t >= max(5, int(0.5 * len(pv)))], mo)
            if zt is not None:
                for t, zz in zt[zt.abs() > UMBRAL_Z].items():
                    transv.append({"variable": v, "nivel": niv, "desag": d, "periodo": lab(t, f), "z_robusto_mediana_transversal": float(zz),
                                   "mediana_tasa": float(med_t.loc[t]), "n_series": int(n_t.loc[t])})
        pos = X[~np.isnan(X)]
        if len(pos):
            prev, nxt = X[:, :-1], X[:, 1:]
            with np.errstate(all="ignore"):
                salto = np.where((prev > 0) & (nxt > 0), np.abs(np.log10(nxt / prev)) >= 1, False)
            unid.append({"variable": v, "nivel": niv, "desag": d, "unidad": u, "min": float(pos.min()), "mediana": float(np.median(pos)),
                         "max": float(pos.max()), "n_negativos": int((pos < 0).sum()), "n_ceros": int((pos == 0).sum()),
                         "saltos_orden_magnitud_entre_periodos_adyacentes": int(salto.sum())})
    F = pd.DataFrame(filas)
    T = pd.DataFrame(tops)
    T["absz"] = T.z_robusto_tasa.abs()
    T = T.sort_values(["absz", "variable", "cod_ine", "periodo"], ascending=[False, True, True, True], kind="mergesort")
    top_glob = T.head(40).drop(columns="absz")
    top_grp = T.groupby(["variable", "nivel", "desag"], sort=True).head(3).drop(columns="absz")
    return F, top_glob, top_grp, pd.DataFrame(unid), dup_keys, pd.DataFrame(transv)


def importe_medio() -> dict:
    out = {}
    for niv in ("ccaa", "provincia"):
        a, b = panel("hip_importe", niv), panel("hip_n", niv)
        cols = sorted(set(a.columns) & set(b.columns))
        idx = sorted(set(a.index) & set(b.index))
        r = (a.loc[idx, cols] / b.loc[idx, cols]).replace([np.inf, -np.inf], np.nan).values
        out[niv] = {"unidad": "miles de euros por hipoteca", "min": float(np.nanmin(r)), "p5": float(np.nanpercentile(r, 5)),
                    "mediana": float(np.nanmedian(r)), "p95": float(np.nanpercentile(r, 95)), "max": float(np.nanmax(r)),
                    "n_fuera_20_1000": int(((r < 20) | (r > 1000)).sum())}
    return out


def duplicadas_nacionales() -> list[dict]:
    ks = [(v, d) for (v, niv, d, f), g in SER.items() if niv == "nacional" and f == "T"]
    S = {k: serie(k[0], desag=k[1]) for k in ks}
    res = []
    for i, a in enumerate(ks):
        for b in ks[i + 1:]:
            j = pd.concat([S[a], S[b]], axis=1, join="inner").dropna()
            if len(j) >= 20 and float((j.iloc[:, 0] - j.iloc[:, 1]).abs().max()) < 1e-9:
                res.append({"A": a[0], "B": b[0], "n_comunes": len(j), "identicas": True})
    return res


# ---------------------------------------------------------------- 2. coherencia


def divergencia_pp(a: pd.Series, b: pd.Series, umbral: float = 0.5, minlen: int = 4) -> list[dict]:
    j = pd.concat([a, b], axis=1, join="inner").dropna()
    if len(j) == 0:
        return []
    d = j.iloc[:, 0] - j.iloc[:, 1]
    return [{"inicio": qlab(i0), "fin": qlab(i1), "trimestres": i1 - i0 + 1, "dif_media": round(float(d.loc[i0:i1].mean()), 3)}
            for i0, i1 in runs(d.abs() > umbral, minlen)]


def signo_opuesto(a: pd.Series, b: pd.Series, lag: int = 4, minpp: float = 0.25, minlen: int = 4) -> list[dict]:
    da, db = grid(a).diff(lag), grid(b).diff(lag)
    j = pd.concat([da, db], axis=1, join="inner").dropna()
    if len(j) == 0:
        return []
    f = (np.sign(j.iloc[:, 0]) != np.sign(j.iloc[:, 1])) & (j.iloc[:, 0].abs() > minpp) & (j.iloc[:, 1].abs() > minpp)
    return [{"inicio": qlab(i0), "fin": qlab(i1), "trimestres": i1 - i0 + 1} for i0, i1 in runs(f, minlen)]


def par_tipos(nom: str, a: pd.Series, b: pd.Series) -> dict:
    j = pd.concat([a, b], axis=1, join="inner").dropna()
    j.columns = ["A", "B"]
    d = j.A - j.B
    ga, gb = grid(j.A), grid(j.B)
    c4 = pd.concat([ga.diff(4), gb.diff(4)], axis=1).dropna().corr().iloc[0, 1]
    c1 = pd.concat([ga.diff(1), gb.diff(1)], axis=1).dropna().corr().iloc[0, 1]
    sub = {}
    for n, (x, y) in {"2003-2007": (2003, 2007), "2008-2014": (2008, 2014), "2015-2021": (2015, 2021), "2022-2026": (2022, 2026)}.items():
        m = [t for t in d.index if x <= t // 4 <= y]
        sub[n] = round(float(d.loc[m].mean()), 3) if m else None
    return {"par": nom, "n_trim": len(j), "primero": qlab(j.index.min()), "ultimo": qlab(j.index.max()),
            "dif_media_pp_AmenosB": float(d.mean()), "dif_abs_media_pp": float(d.abs().mean()), "dif_abs_max_pp": float(d.abs().max()),
            "trim_dif_abs_max": qlab(d.abs().idxmax()), "corr_niveles": float(j.A.corr(j.B)), "corr_cambio_4t": float(c4), "corr_cambio_1t": float(c1),
            "dif_media_por_periodo": sub, "rachas_dif_abs_gt_0.5pp_4t": divergencia_pp(a, b),
            "rachas_cambio_4t_signo_opuesto": signo_opuesto(a, b)}


def tarea2_tipos():
    bde, bce, tae = serie("tipo_hip_bde"), serie("tipo_hip_bce"), serie("tipo_hip_nuevas_tae")
    mir = m2q(serie("bce_hip_tipo_nuevas", "pais", "ES", "fijacion=AM"), "mean")
    pares = [par_tipos("tipo_hip_bde (BdE referencia) vs tipo_hip_bce (BCE MIR nuevas)", bde, bce),
             par_tipos("tipo_hip_bde vs tipo_hip_nuevas_tae (BdE nuevas TAE)", bde, tae),
             par_tipos("tipo_hip_bce vs tipo_hip_nuevas_tae", bce, tae),
             par_tipos("tipo_hip_bce vs media trimestral de bce_hip_tipo_nuevas ES AM (hechos mensual)", bce, mir),
             par_tipos("tipo_bce vs tipo_mro", serie("tipo_bce"), serie("tipo_mro")),
             par_tipos("euribor vs euribor_1y", serie("euribor"), serie("euribor_1y"))]
    ident = {}
    eu = serie("euribor_1y")
    ident["dif_hip_euribor_bce = tipo_hip_bce - euribor_1y (resid. max pp)"] = float((serie("dif_hip_euribor_bce") - (serie("tipo_hip_bce") - eu)).abs().dropna().max())
    ident["dif_hip_euribor_bde = tipo_hip_bde - euribor (resid. max pp)"] = float((serie("dif_hip_euribor_bde") - (serie("tipo_hip_bde") - serie("euribor"))).abs().dropna().max())
    infl = serie("inflacion_ipc_yoy")
    ident["tipo_hip_real_bce = tipo_hip_bce - inflacion_ipc_yoy (resid. max pp)"] = float((serie("tipo_hip_real_bce") - (serie("tipo_hip_bce") - infl)).abs().dropna().max())
    ident["tipo_hip_real_bde = tipo_hip_bde - inflacion_ipc_yoy (resid. max pp)"] = float((serie("tipo_hip_real_bde") - (serie("tipo_hip_bde") - infl)).abs().dropna().max())
    e3 = serie("euribor")
    ident["euribor_ultimo_trimestre_y_valor (trimestre incompleto en la descarga)"] = [qlab(e3.index[-1]), float(e3.iloc[-1])]
    return pares, ident


def comp_series(a: pd.Series, b: pd.Series, nom: str) -> dict:
    j = pd.concat([a, b], axis=1, join="inner").dropna()
    j.columns = ["A", "B"]
    ra = j.A / j.B
    jy = pd.concat([yoy_log(j.A), yoy_log(j.B)], axis=1).dropna()
    jy.columns = ["A", "B"]
    d = jy.A - jy.B
    f = (np.sign(jy.A) != np.sign(jy.B)) & (jy.A.abs() > 1) & (jy.B.abs() > 1)
    return {"par": nom, "n_trim": len(j), "primero": qlab(j.index.min()), "ultimo": qlab(j.index.max()), "ratio_A_B_mediana": float(ra.median()),
            "ratio_A_B_p10": float(ra.quantile(.1)), "ratio_A_B_p90": float(ra.quantile(.9)), "corr_yoy": float(jy.A.corr(jy.B)),
            "dif_media_yoy_pp": float(d.mean()), "dif_abs_media_yoy_pp": float(d.abs().mean()),
            "rachas_yoy_signo_opuesto_4t": [{"inicio": qlab(i0), "fin": qlab(i1), "trimestres": i1 - i0 + 1} for i0, i1 in runs(f, 4)],
            "rachas_dif_yoy_gt10pp_4t": [{"inicio": qlab(i0), "fin": qlab(i1), "trimestres": i1 - i0 + 1, "dif_media_pp": round(float(d.loc[i0:i1].mean()), 2)}
                                       for i0, i1 in runs(d.abs() > 10, 4)]}


def tarea2_hipotecas() -> dict:
    out = {}
    cn, ci = panel("hip_n", "ccaa"), panel("hip_importe", "ccaa")
    nac_n = cn.sum(min_count=17).dropna()
    nac_i = ci.sum(min_count=17).dropna() / 1000.0
    cred = serie("credito_nuevo")
    vol = m2q(serie("bce_hip_volumen_nuevas", "pais", "ES"), "sum")
    out["comparacion"] = [comp_series(nac_i, cred, "INE hip_importe (suma 17 CCAA, M€) vs BCE credito_nuevo"),
                          comp_series(nac_i, vol, "INE hip_importe (suma 17 CCAA, M€) vs BCE MIR volumen nuevas ES (suma trimestral)"),
                          comp_series(nac_n, cred, "INE hip_n (suma 17 CCAA) vs BCE credito_nuevo (M€)"),
                          comp_series(cred, vol, "BCE credito_nuevo vs BCE MIR volumen nuevas ES")]
    mq = m2q(serie("monitor_hipotecas_viviendas"), "sum")
    c = comp_series(nac_n, mq, "INE hip_n (suma 17 CCAA, tabla 76317) vs monitor_hipotecas_viviendas (HPT34618, suma 3 meses)")
    j = pd.concat([nac_n, mq], axis=1, join="inner").dropna()
    c["ratio_por_trimestre"] = {qlab(t): round(float(r), 4) for t, r in (j.iloc[:, 0] / j.iloc[:, 1]).items()}
    out["monitor_vs_76317"] = c
    out["importe_medio_hipoteca"] = importe_medio()
    return out


def tarea2_ss_epa():
    ss = SER[K("ss_afiliados_cota_inferior", "municipio")].copy()
    ss["prov"] = ss.c.str[:2]
    ss["mes"] = ss.p % 12 + 1
    ss = ss[ss.mes % 3 == 0]
    ss["q"] = (ss.p // 12) * 4 + ss.mes // 3 - 1
    sp = ss.groupby(["prov", "q"]).valor.sum().unstack("q")
    ep = panel("ocupados_epa", "provincia")
    provs = sorted(set(sp.index) & set(ep.index))
    cols = sorted(set(sp.columns) & set(ep.columns))
    rat = sp.loc[provs, cols] / (1000.0 * ep.loc[provs, cols])
    filas = []
    for p in provs:
        a, b = sp.loc[p].dropna(), ep.loc[p].dropna() * 1000
        jy = pd.concat([yoy_log(a), yoy_log(b)], axis=1).dropna()
        filas.append({"cod_ine": p, "n_trim": int(rat.loc[p].notna().sum()), "ratio_ss_epa_mediana": float(rat.loc[p].median()),
                      "ratio_ss_epa_2019T4": float(rat.loc[p].get(qi("2019T4"), np.nan)), "ratio_ss_epa_2025T4": float(rat.loc[p].get(qi("2025T4"), np.nan)),
                      "n_yoy": len(jy), "corr_yoy": float(jy.iloc[:, 0].corr(jy.iloc[:, 1])) if len(jy) >= 8 else np.nan})
    P = pd.DataFrame(filas)
    por_año = {}
    for y in range(2012, 2027):
        cs = [q for q in rat.columns if q // 4 == y and q % 4 == 3]
        if cs:
            por_año[y] = {"ratio_mediana_provincias": float(rat[cs[0]].median()), "p10": float(rat[cs[0]].quantile(.1)), "p90": float(rat[cs[0]].quantile(.9))}
    res = {"n_provincias_comparadas": len(provs), "ratio_mediana_entre_provincias": float(P.ratio_ss_epa_mediana.median()),
           "ratio_p10": float(P.ratio_ss_epa_mediana.quantile(.1)), "ratio_p90": float(P.ratio_ss_epa_mediana.quantile(.9)),
           "ratio_min": float(P.ratio_ss_epa_mediana.min()), "ratio_max": float(P.ratio_ss_epa_mediana.max()),
           "corr_yoy_mediana": float(P.corr_yoy.median()), "n_prov_corr_yoy_lt_0.5": int((P.corr_yoy < 0.5).sum()),
           "ratio_mediana_provincias_por_año_t4": por_año,
           "nota": ("SS: afiliados por municipio de la cuenta de cotización (centro de trabajo/empresa), cota inferior (celdas <5 omitidas), "
                    "último día del mes, todos los regímenes; EPA: ocupados residentes, media trimestral. Conceptos distintos: el cociente no debe valer 1.")}
    return res, P


def suma_provincial():
    filas = []
    for v in ("hip_n", "hip_importe", "compraventas", "ocupados_epa", "parados_epa"):
        pp = panel(v, "provincia")
        if K(v, "ccaa") is not None:
            cc = panel(v, "ccaa")
        elif v == "ocupados_epa":
            cc = panel("ocupados_epa_prov", "ccaa")
        else:
            continue
        for ccaa_cod in sorted(cc.index):
            todas = [p for p, c in PROV2CCAA.items() if c == ccaa_cod]
            presentes = [p for p in todas if p in pp.index]
            if len(presentes) != len(todas) or not todas:
                filas.append({"variable": v, "cod_ccaa": ccaa_cod, "provincias": len(todas), "provincias_en_muestra": len(presentes), "comparable": False})
                continue
            s = pp.loc[presentes].sum(min_count=len(presentes))
            j = pd.concat([s, cc.loc[ccaa_cod]], axis=1).dropna()
            if len(j) == 0:
                continue
            rel = (j.iloc[:, 0] / j.iloc[:, 1] - 1) * 100
            filas.append({"variable": v, "cod_ccaa": ccaa_cod, "provincias": len(todas), "provincias_en_muestra": len(presentes), "comparable": True,
                          "n_trim": len(j), "dif_rel_media_pct": float(rel.mean()), "dif_rel_abs_max_pct": float(rel.abs().max()),
                          "n_trim_dif_gt_0.5pct": int((rel.abs() > 0.5).sum()), "periodo_dif_max": qlab(rel.abs().idxmax())})
    P = pd.DataFrame(filas)
    nac = {}
    for v in ("compraventas", "ocupados", "visados"):
        c = panel(v, "ccaa").sum(min_count=17)
        j = pd.concat([c, serie(v)], axis=1).dropna()
        rel = (j.iloc[:, 0] / j.iloc[:, 1] - 1) * 100
        por_año = rel.groupby(rel.index // 4).mean()
        nac[v] = {"n_trim": len(j), "dif_rel_media_pct": float(rel.mean()), "dif_rel_abs_max_pct": float(rel.abs().max()),
                  "periodo_dif_max": qlab(rel.abs().idxmax()), "dif_rel_media_por_año": {int(k): round(float(x), 3) for k, x in por_año.items()},
                  "nota": "17 CCAA; Ceuta y Melilla no están en las series de CCAA de la base"}
    pa = panel("pib_ccaa_anual", "ccaa")
    anual = {t // 4: pa[t].sum(min_count=17) / 1000.0 for t in pa.columns if t % 4 == 3}
    pn = serie("pib_nom")
    nacy = pn.groupby(pn.index // 4).agg(["sum", "size"])
    cmp_pib = {int(y): round(float(anual[y] / nacy.loc[y, "sum"]), 4) for y in anual if y in nacy.index and nacy.loc[y, "size"] == 4}
    nac["pib_ccaa_anual_17CCAA_vs_pib_nom_CNT"] = {"razon_por_año": cmp_pib,
                                                  "nota": "CRE (corrientes, sin ajuste estacional) frente a CNT (corrientes, SA y calendario); 17 CCAA sin Ceuta/Melilla"}
    pr = panel("pib_miles_eur", "provincia")
    mx = []
    for ccaa_cod in sorted(pa.index):
        todas = [p for p, c in PROV2CCAA.items() if c == ccaa_cod]
        pres = [p for p in todas if p in pr.index]
        if len(pres) != len(todas) or not todas:
            continue
        dd = [(pr.loc[pres, y].sum(min_count=len(pres)) / pa.loc[ccaa_cod, y * 4 + 3] - 1) * 100 for y in pr.columns
              if (y * 4 + 3) in pa.columns and pa.loc[ccaa_cod, y * 4 + 3] > 0]
        if dd:
            mx.append(float(np.nanmax(np.abs(dd))))
    nac["pib_provincias_vs_pib_ccaa_anual"] = {"n_ccaa_comparables": len(mx), "dif_rel_abs_max_pct": max(mx) if mx else None}
    return P, nac


def pib_repetido() -> dict:
    pa = panel("pib_ccaa_anual", "ccaa")
    r = pa.stack().dropna().reset_index()
    r.columns = ["c", "t", "valor"]
    r["y"] = r.t // 4
    g = r.groupby(["c", "y"]).valor.agg(["size", "nunique"])
    completos = g[g["size"] == 4]
    dq = pa.diff(axis=1).values
    dq = dq[~np.isnan(dq)]
    raros = completos[completos["nunique"] != 1]
    nccaa = r.groupby("t").c.nunique()
    ult = int(pa.columns.max())
    return {"ccaa_anio_con_4_trimestres": int(len(completos)), "ccaa_anio_con_4_trimestres_valores_distintos": [f"{c}/{y}" for c, y in raros.index],
            "ccaa_con_dato_en_el_ultimo_trimestre": [qlab(ult), int(nccaa.loc[ult])], "ccaa_con_dato_en_T4_del_año_anterior": int(nccaa.loc[ult - 4]) if (ult - 4) in nccaa.index else None, "con_un_unico_valor": int((completos["nunique"] == 1).sum()),
            "pct_variaciones_trimestrales_exactamente_cero": round(100 * float((dq == 0).mean()), 1),
            "advertencia": ("Una tasa trimestral (diferencia de 1 trimestre) de pib_ccaa_anual vale 0 en tres de cada cuatro trimestres y salta en el T1: "
                            "no es una variación. Solo la variación a 4 trimestres (T1 frente a T1) equivale a la tasa anual."),
            "uso_trimestral_detectado_en_src": ("grep de src/v7/r1_panel.py: d_ln y d4_ln solo se crean para pib_ccaa_q (interpolada); pib_ccaa_anual no recibe d_ln "
                                               "en el panel; 'exp_hip_importe_pib_1519' usa el PIB anual. No se ejecuta código ajeno."),
            "pib_ccaa_q": "interpolación log-lineal entre anclas T3: solo robustez (regla del repositorio)."}


# ---------------------------------------------------------------- 3. vintages, rupturas


def reproduccion_raw() -> list[dict]:
    res = []

    def rawm(archivo: str) -> pd.Series:
        r = pd.read_csv(RAW / archivo, usecols=["periodo", "valor"])
        return pd.Series(r.valor.values, index=[pidx(p) for p in r.periodo]).sort_index()

    def comp(nom, h, r, nota=""):
        j = pd.concat([h, r], axis=1, join="inner").dropna()
        j.columns = ["hechos", "raw"]
        res.append({"serie": nom, "n_trim": len(j), "dif_abs_max": float((j.hechos - j.raw).abs().max()) if len(j) else None, "nota": nota})
    comp("tipo_hip_bce", serie("tipo_hip_bce"), m2q(rawm("ecb_tipo_hipotecario_es.csv"), "mean"), "media de 3 meses")
    comp("euribor_1y", serie("euribor_1y"), m2q(rawm("ecb_euribor1y.csv"), "mean"), "media de 3 meses")
    cn = rawm("ecb_nuevo_credito_vivienda_es.csv")
    comp("credito_nuevo (suma 3 meses)", serie("credito_nuevo"), m2q(cn, "sum"), "suma")
    comp("credito_nuevo (media 3 meses)", serie("credito_nuevo"), m2q(cn, "mean"), "media")
    r = pd.read_csv(RAW / "ine_epa_ocupados.csv", usecols=["periodo", "valor"])
    comp("ocupados nacional", serie("ocupados"), pd.Series(r.valor.values, index=[pidx(p) for p in r.periodo]).sort_index(), "EPA387796")
    return res


def tarea3_vintages() -> dict:
    ed = DF.groupby("v").agg(n_edicion=("edicion", "nunique"), n_fecha_dato=("fecha_dato", "nunique")).reset_index()
    fechas = []
    for f in glob.glob(str(RAW / "**" / "_manifest*.csv"), recursive=True):
        m = pd.read_csv(f)
        col = next((c for c in ("descargado_utc", "fecha_descarga") if c in m.columns), None)
        if col is not None:
            fechas.append(pd.Series(m[col].astype(str).str[:10]))
    fechas = pd.concat(fechas)
    fechas = fechas[fechas.str.match(r"^\d{4}-\d{2}-\d{2}$")]
    comp = pd.read_csv(RAW / "v9" / "actualizaciones" / "comparacion_ediciones.csv")
    return {"ediciones_por_variable_hechos": {r.v: [int(r.n_edicion), int(r.n_fecha_dato)] for r in ed.itertuples()},
            "variables_con_mas_de_una_edicion": [r.v for r in ed.itertuples() if r.n_edicion > 1],
            "fechas_descarga_manifiestos": {"min": str(fechas.min()), "max": str(fechas.max()), "n_distintas": int(fechas.nunique()),
                                            "fecha_modal": str(fechas.value_counts().index[0])},
            "comparacion_ediciones_v9": {"filas": int(len(comp)), "novedad_no": int((comp.novedad == "no").sum()),
                                         "nota": "compara solo el último periodo del proyecto con la edición vigente a 2026-10-14; no mide revisiones de la historia"},
            "reproduccion_hechos_vs_raw": reproduccion_raw(),
            "conclusion": ("Una sola descarga por serie (lote del 2026-10-09 al 2026-10-15) y una sola edición en hechos: no hay vintages comparables, "
                           "así que no se mide ninguna revisión (CNT, EPA, HPT, BdE, BCE). Hace falta una segunda descarga fechada.")}


def z_misma_estacion(s: pd.Series, t0: int, lag: int = 1, dif: bool = False) -> dict:
    s = grid(s.dropna().astype(float))
    ch = (s - s.shift(lag)) if dif else np.log(s / s.shift(lag)) * 100
    ch = ch.dropna()
    est = ch[(ch.index % 4) == (t0 % 4)]
    if t0 not in est.index:
        return {"cambio": None, "z_misma_estacion": None}
    z = zrob1(est, 8)
    return {"cambio": float(ch.loc[t0]), "z_misma_estacion": float(z.loc[t0]) if z is not None else None, "n_misma_estacion": len(est)}


def rup_epa() -> dict:
    t0 = qi("2021T1")
    out = {"nacional": {"ocupados_log_qoq": z_misma_estacion(serie("ocupados"), t0),
                        "tasa_paro_dif_qoq": z_misma_estacion(serie("tasa_paro_epa"), t0, 1, True)}}
    pe, pa_ = panel("ocupados_epa", "provincia"), panel("parados_epa", "provincia")
    tasa = pa_ / (pa_ + pe) * 100
    for nom, P, dif in (("ocupados_epa_prov_log", pe, False), ("tasa_paro_prov_dif", tasa, True), ("tasa_paro_epa_ccaa_dif", panel("tasa_paro_epa", "ccaa"), True)):
        zs = np.array([z for z in (z_misma_estacion(P.loc[c].dropna(), t0, 1, dif).get("z_misma_estacion") for c in P.index) if z is not None])
        out[nom] = {"n_series": len(zs), "z_mediana": float(np.median(zs)), "n_abs_z_gt3": int((np.abs(zs) > 3).sum()), "n_abs_z_gt5": int((np.abs(zs) > 5).sum())}
    rel = ((panel("ocupados", "ccaa").sum(min_count=17) / serie("ocupados") - 1) * 100).dropna()
    out["suma_ccaa_vs_nacional_ocupados_pct"] = {"media_2007_2020": float(rel[[t for t in rel.index if t // 4 <= 2020]].mean()),
                                                 "media_2021_2026": float(rel[[t for t in rel.index if t // 4 >= 2021]].mean()),
                                                 "2020T4_y_2021T1": [float(rel.get(qi("2020T4"), np.nan)), float(rel.get(qi("2021T1"), np.nan))]}
    out["nota"] = ("El INE declara el cambio de factores de elevación de 2021T1 como «no relevante» (inventario). Aquí solo se contrasta el cambio trimestral de "
                   "2021T1 con los demás primeros trimestres (z robusto de la misma estación); 2021T1 coincide con la salida de la fase aguda del COVID.")
    return out


def rup_etcl() -> dict:
    s = serie("salario")
    t0 = qi("2008T1")
    out = {"salario_nacional_log_qoq_2008T1": z_misma_estacion(s, t0), "salario_nacional_log_qoq_2008T2": z_misma_estacion(s, t0 + 1),
           "nivel_2007T4": float(s.get(t0 - 1, np.nan)), "nivel_2008T1": float(s.get(t0, np.nan))}
    z = zrob1(yoy_log(s).dropna(), 12)
    out["yoy_2008T1_a_2008T4_z_robusto"] = {qlab(t): round(float(z.loc[t]), 2) for t in range(t0, t0 + 4) if z is not None and t in z.index}
    yq = pd.concat([s, panel("salario_ccaa", "ccaa").mean()], axis=1, join="inner").dropna()
    r = yq.iloc[:, 0] / yq.iloc[:, 1]
    out["razon_salario_nacional_sobre_media_simple_ccaa"] = {"n": len(r), "media": float(r.mean()), "desv": float(r.std()), "min": float(r.min()), "max": float(r.max())}
    return out


def rup_cnt() -> dict:
    out = {}
    for v in ("pib_nom", "pib_vol_idx", "rdb", "renta_hog", "renta_hog_real", "deflactor"):
        s = serie(v)
        z = zrob1(np.log(grid(s)).diff().dropna() * 100, 12)
        k = z.abs().idxmax()
        out[v] = {"n": len(s), "huecos_trimestres": int(len(grid(s)) - len(s)), "z_max_qoq": round(float(z.loc[k]), 2), "periodo_z_max": qlab(k),
                  "n_abs_z_gt5": int((z.abs() > 5).sum())}
    j = pd.concat([serie("deflactor"), (serie("pib_nom") / serie("pib_vol_idx"))], axis=1).dropna()
    r = j.iloc[:, 0] / j.iloc[:, 1]
    df_ = serie("deflactor")
    out["deflactor_frente_a_pib_nom_sobre_vol"] = {"razon_cv": float(r.std() / r.mean()), "razon_min": float(r.min()), "razon_max": float(r.max()),
                                                  "media_2020_deflactor": float(df_[[t for t in df_.index if t // 4 == 2020]].mean())}
    jj = pd.concat([serie("renta_hog"), serie("rdb")], axis=1).dropna()
    rh = jj.iloc[:, 0] / jj.iloc[:, 1]
    out["renta_hog_sobre_rdb"] = {"min": float(rh.min()), "max": float(rh.max()), "identicas": bool((jj.iloc[:, 0] - jj.iloc[:, 1]).abs().max() < 1e-6)}
    rr = (serie("renta_hog_real") - serie("renta_hog") / serie("deflactor") * 100).abs().dropna()
    out["renta_hog_real_vs_renta_hog_sobre_deflactor_resid_max"] = float(rr.max()) if len(rr) else None
    out["nota"] = "Sin cambio de base de la CNT documentado en el repositorio («no consta»); no hay vintages para medir revisiones."
    return out


def rup_hipotecas() -> dict:
    n = panel("hip_n", "ccaa").sum(min_count=17).dropna()
    z = zrob1(np.log(grid(n)).diff().dropna() * 100, 12)
    yz = zrob1(yoy_log(n).dropna(), 12)
    return {"suma_17ccaa_log_qoq_top5_z": {qlab(t): round(float(z.loc[t]), 2) for t in z.abs().sort_values(ascending=False).head(5).index},
            "suma_17ccaa_n_abs_z_gt5_qoq": int((z.abs() > 5).sum()),
            "suma_17ccaa_yoy_top3_z": {qlab(t): round(float(yz.loc[t]), 2) for t in yz.abs().sort_values(ascending=False).head(3).index},
            "primer_periodo_provincial": qlab(int(panel("hip_n", "provincia").columns.min())), "primer_periodo_ccaa": qlab(int(panel("hip_n", "ccaa").columns.min())),
            "metodo_dato_ccaa": "agregado_suma_3_meses_y_provincias (hechos): suma provincial = CCAA es identidad por construcción, no comprobación independiente",
            "fecha_cambio_de_base": "no consta (tabla 76317 «base nueva» según el manifiesto; sin fecha en el repositorio)",
            "nota": "las series provinciales cubren 41 de 52 provincias en la muestra no sellada; el total nacional solo se reconstruye con las 17 CCAA."}


# ---------------------------------------------------------------- 4. P3


def p3_busqueda() -> dict:
    pats = {"jarocinski_karadi": r"jarocin|jkshocks|\bJK\b", "ea_mpd_altavilla": r"altavilla|EA-MPD|Monetary Policy Event-Study|event-study database",
            "alta_frecuencia_sorpresas": r"alta frecuencia|high-frequency|sorpresa|surprise",
            "exposicion_tipo_variable": r"cuota.{0,30}tipo variable|tipo variable|hipoteca variable|peso de la hipoteca variable|SVLHPHH"}
    mani = []
    for f in sorted(glob.glob(str(RAW / "**" / "_manifest*.csv"), recursive=True)):
        t = pd.read_csv(f).fillna("").astype(str)
        mani.append((f.replace(str(RAIZ) + "/", ""), pd.Series([" ".join(r) for r in t.values.tolist()], dtype=str)))
    docs = [(f.replace(str(RAIZ) + "/", ""), Path(f).read_text(encoding="utf-8", errors="ignore")) for f in sorted(glob.glob(str(RAIZ / "docs" / "**" / "*.md"), recursive=True))]
    res = {}
    for k, p in pats.items():
        h_m = [{"manifiesto": f, "filas": int(s.str.contains(p, case=False, regex=True).sum())} for f, s in mani if s.str.contains(p, case=False, regex=True).any()]
        h_d = sorted([(f, len(re.findall(p, t, flags=re.I))) for f, t in docs if re.search(p, t, flags=re.I)], key=lambda x: (-x[1], x[0]))
        res[k] = {"manifiestos": h_m, "docs_n_ficheros": len(h_d), "docs_top5": [{"fichero": a, "menciones": b} for a, b in h_d[:5]]}
    jk = pd.read_csv(RAW / "v8" / "jk_shocks_ecb_mensual.csv", usecols=["periodo", "serie", "valor"])
    mp = jk[jk.serie == "MP_median"]
    res["jk_cobertura"] = {"fichero": "data/raw/v8/jk_shocks_ecb_mensual.csv", "series": sorted(jk.serie.unique().tolist()),
                           "primer_mes": mp.periodo.min(), "ultimo_mes": mp.periodo.max(), "n_meses": int(len(mp)),
                           "n_meses_valor_no_nulo": int((mp.valor.abs() > 1e-12).sum()),
                           "frecuencia": "mensual (agregación de los shocks de cada reunión del BCE); el fichero no trae la fecha-hora de cada reunión",
                           "licencia_segun_repositorio": ("conflicto: docs/v8 y docs/v9/cobertura la marcan no redistribuible; src/v8/fetch_v8.py cita CC BY 4.0 para datos; "
                                                          "v9 comparacion_ediciones: «sin licencia explícita». No verificado.")}
    hv = DF[(DF.v == "bce_hip_tipo_nuevas") & (DF.c == "ES")]
    cv = DF[(DF.v == "bce_cuota_tipo_variable") & (DF.c == "ES")].sort_values("p")
    res["exposicion_en_la_base"] = {
        "bce_cuota_tipo_variable": {"nivel": "pais (28 códigos)", "ES_primer": cv.periodo.min(), "ES_ultimo": cv.periodo.max(),
                                    "ES_min": float(cv.valor.min()), "ES_max": float(cv.valor.max()), "ES_ultimo_valor": float(cv.valor.iloc[-1])},
        "bce_hip_tipo_nuevas": {"nivel": "pais (21)", "desagregaciones_ES": sorted(hv.d.unique().tolist()),
                                "nota": "tipo de nuevas operaciones por periodo de fijación inicial (códigos BCE); significado exacto de cada código: no verificado en el repositorio"},
        "territorial_provincial_o_municipal": "no existe en el repositorio ninguna variable de peso de la hipoteca variable (stock o flujo) por provincia o municipio"}
    return res


P3_DATOS_NECESARIOS = [
    {"dato": "Euro Area Monetary Policy Event-Study Database (EA-MPD; Altavilla et al., 2019) con ventana de cada reunión del BCE", "uso": "sorpresas por evento en lugar del agregado mensual JK", "estado": "no está en el repositorio; licencia y acceso: no verificado"},
    {"dato": "Actualización de los shocks JK posterior a 2025-10 y con fechas de reunión", "uso": "alargar la muestra hasta 2026", "estado": "el repositorio llega a 2025-10; condiciones de reutilización: no verificado"},
    {"dato": "Stock de préstamos hipotecarios a vivienda por tipo de interés (variable, fijo, mixto) por provincia o CCAA (BdE, CIR/AnaCredit, Registradores, Notariado)", "uso": "peso de la hipoteca variable como exposición", "estado": "no está en el repositorio; disponibilidad territorial y licencia: no verificado"},
    {"dato": "Hipotecas INE (HPT) por tipo de interés (fijo/variable) por CCAA o provincia (flujo de nuevas)", "uso": "exposición de flujo por CCAA", "estado": "no está en la base; si existe con detalle territorial: no verificado"},
    {"dato": "Encuesta Financiera de las Familias (BdE): hogares con deuda hipotecaria a tipo variable", "uso": "exposición por CCAA con muestra pequeña", "estado": "no está; representatividad territorial y licencia: no verificado"},
    {"dato": "Tipo inicial y fecha de formalización por hipoteca agregados por municipio o provincia (Notariado, Registradores)", "uso": "exposición por cohorte", "estado": "terceros_1_0: solo agregados propios; disponibilidad: no verificado"},
]

# ---------------------------------------------------------------- 5. P9


def p9_calendario() -> dict:
    man = pd.read_csv(RAW / "_manifest.csv")
    reg = [("compraventas ETDP 6150 (mensual)", "ine_etdp_compraventas.csv", "M"), ("hipotecas INE HPT 76317 (mensual)", "ine_v2_hipotecas_prov.csv", "M"),
           ("visados MIVAU (mensual)", "mivau_visados.csv", "M"), ("ocupados EPA (trimestral)", "ine_epa_ocupados.csv", "T"),
           ("crédito nuevo BCE (mensual)", "ecb_nuevo_credito_vivienda_es.csv", "M"), ("Euribor 1 año (mensual)", "ecb_euribor1y.csv", "M")]
    filas = []
    for nom, arch, fr in reg:
        r = man[man.archivo == arch].iloc[0]
        ult = pd.Timestamp(r.ultima_fecha)
        fin = ult + (pd.offsets.QuarterEnd(0) if fr == "T" else pd.offsets.MonthEnd(0))
        desc = pd.Timestamp(str(r.descargado_utc)[:10])
        filas.append({"indicador": nom, "frec": fr, "primer_periodo": str(r.primera_fecha)[:7], "ultimo_periodo": str(r.ultima_fecha)[:7], "n_periodos": (len(pd.period_range(str(r.primera_fecha)[:7], str(r.ultima_fecha)[:7], freq="Q" if fr == "T" else "M")) if fr == "M" or True else 0),
                      "descarga": str(desc.date()), "lag_dias_cota_superior": int((desc - fin).days)})
    ss = DF[DF.v == "ss_afiliados_cota_inferior"]
    mx = ss.periodo.max()
    cm = pd.read_csv(RAW / "v11" / "ss_afiliacion_municipio" / "_manifest.csv")
    d_ss = str(cm.fecha_descarga.iloc[0])[:10]
    filas.append({"indicador": "afiliación SS municipal (último día; mensual solo desde 2022-01)", "frec": "M", "primer_periodo": ss.periodo.min(), "ultimo_periodo": mx,
                  "n_periodos": int(ss.p.nunique()), "descarga": d_ss, "lag_dias_cota_superior": int((pd.Timestamp(d_ss) - (pd.Timestamp(mx + "-01") + pd.offsets.MonthEnd(0))).days)})
    T = pd.DataFrame(filas)
    T["meses_2026T3_disponibles"] = [int(max(0, min(3, int(u[5:7]) - 6))) if (u.startswith("2026") and fr == "M") else 0 for fr, u in zip(T.frec, T.ultimo_periodo, strict=True)]
    return {"tabla": T,
            "calendario_declarado": {"fuente": "docs/v7/hipotesis.md l.85, docs/v7/desviaciones.md l.22, docs/v7/tareas_autor.md l.7, docs/v8/hipotesis.md l.174",
                                     "ventana_de_evaluacion_declarada": "2026T3 a 2027T2 (4 trimestres), con datos publicados «hacia el verano de 2027»",
                                     "trimestres_posteriores_a_2026-10_en_la_ventana": 3,
                                     "detalle": "2026T4, 2027T1 y 2027T2 son posteriores a 2026-10; 2026T3 cierra en septiembre y solo está publicado en parte (afiliación) a 2026-10-17",
                                     "evaluacion_v15": "no consta: el repositorio no declara fecha ni ventana de la evaluación de V15 (el sellado V15 aún no existe)",
                                     "calendarios_oficiales_INE_BdE_MIVAU": "no constan en el repositorio (no se asume ninguno)"},
            "nota": ("lag_dias_cota_superior = fecha de descarga menos fin del último periodo: cota superior del retraso de publicación del último dato "
                     "(el dato ya estaba publicado a esa fecha); no es el calendario oficial.")}


def metodo_y_ceros() -> dict:
    m = DF.groupby(["v", "nivel", "metodo_dato"]).size().reset_index(name="filas")
    interp = m[m.metodo_dato.fillna("").str.contains("interpol|imput|estim", case=False)]
    nm = DF.groupby("v").metodo_dato.nunique()
    t = DF[(DF.v == "bce_hip_tipo_nuevas") & (DF.valor == 0)]
    s0 = DF[(DF.v == "ss_afiliados_cota_inferior") & (DF.valor == 0)]
    return {"filas_con_metodo_interpolado_o_imputado": [{"variable": r.v, "nivel": r.nivel, "metodo": r.metodo_dato, "filas": int(r.filas)} for r in interp.itertuples()],
            "pct_filas_interpoladas_o_imputadas_grupo": round(100 * float(interp.filas.sum()) / float(len(DF)), 3),
            "bce_hip_tipo_nuevas_valores_cero": {"filas": int(len(t)), "paises": sorted(t.c.unique().tolist()), "desagregaciones": sorted(t.d.unique().tolist()),
                                                 "nota": "tipo exactamente 0,00: posible código de ausencia o fijación sin operaciones; no verificado"},
            "ss_afiliados_cota_inferior_ceros": {"filas": int(len(s0)), "pct_filas": round(100 * len(s0) / float((DF.v == "ss_afiliados_cota_inferior").sum()), 2),
                                                 "nota": "cero = todas las celdas del municipio <5 (censura), no ausencia de afiliados"}}


# ---------------------------------------------------------------- principal


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    F, top_g, top_grp, unid, dup_keys, transv = tarea1_atipicos()
    transv.round(4).to_csv(OUT / "rupturas_transversales.csv", index=False)
    F.to_csv(OUT / "atipicos_resumen.csv", index=False)
    top_g.round(4).to_csv(OUT / "atipicos_top40.csv", index=False)
    top_grp.round(4).to_csv(OUT / "atipicos_top3_por_variable.csv", index=False)
    unid.round(4).to_csv(OUT / "unidades_rangos.csv", index=False)
    imp, dups = importe_medio(), duplicadas_nacionales()
    tipos, ident = tarea2_tipos()
    hip = tarea2_hipotecas()
    ss_epa, P = tarea2_ss_epa()
    P.round(4).to_csv(OUT / "ss_vs_epa_provincias.csv", index=False)
    SP, nac = suma_provincial()
    SP.round(4).to_csv(OUT / "suma_provincial_vs_ccaa.csv", index=False)
    pibr = pib_repetido()
    vint = tarea3_vintages()
    rup = {"epa_2021T1": rup_epa(), "etcl_2008T1": rup_etcl(), "cnt": rup_cnt(), "hipotecas_76317": rup_hipotecas()}
    p3 = p3_busqueda()
    p9 = p9_calendario()
    p9["tabla"].to_csv(OUT / "p9_indicadores_calendario.csv", index=False)
    pd.DataFrame(P3_DATOS_NECESARIOS).to_csv(OUT / "p3_datos_necesarios.csv", index=False)
    pd.DataFrame([{"par": p["par"], "n_trim": p["n_trim"], "primero": p["primero"], "ultimo": p["ultimo"], "dif_media_pp_AmenosB": p["dif_media_pp_AmenosB"],
                   "dif_abs_max_pp": p["dif_abs_max_pp"], "corr_niveles": p["corr_niveles"], "corr_cambio_4t": p["corr_cambio_4t"],
                   "n_rachas_dif_gt_0.5pp": len(p["rachas_dif_abs_gt_0.5pp_4t"]), "n_rachas_signo_opuesto": len(p["rachas_cambio_4t_signo_opuesto"])}
                  for p in tipos]).round(4).to_csv(OUT / "coherencia_tipos.csv", index=False)
    pd.DataFrame([{k: v for k, v in c.items() if not isinstance(v, (list, dict))} | {"n_rachas_signo_opuesto": len(c["rachas_yoy_signo_opuesto_4t"]),
                                                                                   "n_rachas_dif_gt10pp": len(c["rachas_dif_yoy_gt10pp_4t"])}
                  for c in hip["comparacion"]]).round(4).to_csv(OUT / "coherencia_hipotecas_credito.csv", index=False)

    n_series = int(F.n_series.sum())
    resumen_at = {"n_grupos_variable_nivel": len(F), "n_series": n_series, "atip_tasa_total": int(F.atip_tasa.sum()),
                  "series_con_atip_tasa": int(F.series_con_atip_tasa.sum()), "series_mad_nula_tasa": int(F.series_mad_nula.sum()),
                  "series_mad_casi_nula_tasa": int(F.series_mad_casi_nula.sum()), "atip_tasa_en_mad_casi_nula": int(F.atip_tasa_en_mad_casi_nula.sum()),
                  "desv_en_mad_nula": int(F.desv_distintas_de_mediana_en_mad_nula.sum()), "atip_nivel_total": int(F.atip_nivel.sum()),
                  "claves_duplicadas_hechos": dup_keys}
    por_var = F[F.atip_tasa > 0].sort_values("atip_tasa", ascending=False)[["variable", "nivel", "desag", "n_series", "atip_tasa", "pct_atip_tasa", "series_con_atip_tasa"]].head(15)
    resultado = {
        "rama": "v15/auditoria/financiacion_macro",
        "pregunta": ("¿Qué series de financiación y macro son fiables y coherentes para V15 (P2, P3, P9)? Atípicos, coherencia entre fuentes, "
                     "sumas territoriales, vintages, rupturas, y qué falta para P3 y P9."),
        "capa": "C4",
        "datos": ["hechos.parquet (muestra no sellada): variables de financiación, empleo, renta, macro y otras (inventario V15)",
                  "data/raw: manifiestos y reproducción nacional (BCE, EPA)", "data/raw/v8/jk_shocks_ecb_mensual.csv (solo cobertura)"],
        "N": {"series": n_series, "variables": int(F.variable.nunique()), "grupos_variable_nivel": len(F)},
        "metodo": ("Auditoría descriptiva determinista (SEED=20261010): z robusto con mediana y MAD (|z|>5) sobre niveles y tasas (log×100 a 4 trimestres o 12 meses; "
                   "diferencia para tipos y variables en %/pp), separando MAD nula y casi nula (1,4826·MAD<0,1·sd); coherencia por correlación de cambios, diferencias y rachas; "
                   "sumas provincial-CCAA-nacional; cruces por código INE."),
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {
            "atipicos_resumen": resumen_at, "atipicos_top_grupos": json.loads(por_var.to_json(orient="records")),
            "atipicos_top10": json.loads(top_g.head(10).round(3).to_json(orient="records")),
            "unidades": {"importe_medio_hipoteca": imp, "saltos_orden_magnitud_total": int(unid.saltos_orden_magnitud_entre_periodos_adyacentes.sum()),
                         "variables_con_negativos": sorted(unid.loc[unid.n_negativos > 0, "variable"].unique().tolist())},
            "series_nacionales_identicas": dups, "coherencia_tipos": tipos, "identidades_derivadas": ident, "coherencia_hipotecas_credito": hip,
            "ss_vs_epa_provincias": ss_epa,
            "suma_provincial_vs_ccaa": {"filas_comparables": int(SP.comparable.sum()), "filas_total": len(SP),
                                        "dif_rel_abs_max_pct_por_variable": {v: float(g.dif_rel_abs_max_pct.max()) for v, g in SP[SP.comparable].groupby("variable")},
                                        "ccaa_comparables": {v: sorted(g.cod_ccaa.tolist()) for v, g in SP[SP.comparable].groupby("variable")}},
            "suma_ccaa_vs_nacional_y_pib": nac, "pib_ccaa_anual_repetido": pibr, "vintages": vint, "rupturas": rup, "rupturas_transversales": {"n_filas": int(len(transv)), "top10": json.loads(transv.assign(a=transv.z_robusto_mediana_transversal.abs()).sort_values(["a", "variable", "periodo"], ascending=[False, True, True]).head(10).drop(columns="a").round(3).to_json(orient="records")) if len(transv) else [], "por_variable": {k: int(n) for k, n in transv.groupby("variable").size().items()} if len(transv) else {}}, "metodo_y_ceros": metodo_y_ceros(),
            "p3_exposicion_y_sorpresas": {"busqueda": p3, "datos_necesarios_no_verificados": P3_DATOS_NECESARIOS},
            "p9_indicadores_adelantados": {"tabla": json.loads(p9["tabla"].to_json(orient="records")), "calendario_declarado": p9["calendario_declarado"], "nota": p9["nota"]},
        },
        "fuera_muestra": None,
        "notas": ["Auditoría C4 sin efectos; hechos filtrado con NOT coalesce(muestra_sellada_v6,false) (41 de 52 provincias en series provinciales); no se lee la muestra sellada.",
                  "Sin series de Notariado, Registradores ni AEAT en la salida (variables aeat_ excluidas del grupo).",
                  "ipc_general, ss_afiliados provinciales totales, eu_*, bis_rpp y oecd_house_prices no están en hechos (solo en data/raw o como derivadas)."],
    }
    (OUT / "resultado.json").write_text(json.dumps(limpia(resultado), ensure_ascii=False, indent=1), encoding="utf-8")
    print("OK", OUT)


if __name__ == "__main__":
    main()
