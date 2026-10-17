"""V15 fase 1.2 · Auditoría de datos, grupo TURISMO (capa C4, descriptivo, sin efectos estimados).

Fuentes: INE VUT experimental (sección/distrito), vut_* provinciales, registros autonómicos (GVA, IDESCAT, REATE, BCN HUT),
Inside Airbnb (no oficial, solo estadísticos resumen), Eurostat plataformas, INE turismo con móviles y turistas.
Cruces territoriales solo por código INE (data/base/territorios.parquet). Determinista (SEED=20261010), sin red, solo lectura.
Se excluye la muestra reservada de V6 con NOT coalesce(muestra_sellada_v6,false); el script no abre ninguna ruta de muestra reservada.
Salida: output/v15/auditoria/turismo/ (CSV resumen y resultado.json). Sin series completas de Inside Airbnb ni del registro
de Catalunya («Ver términos de uso»): solo estadísticos resumen. Uso: python3 src/v15/auditoria/turismo.py
"""
from __future__ import annotations

import io
import json
import re
import warnings
import zipfile
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
RAIZ = Path(__file__).resolve().parents[3]
RAW = RAIZ / "data" / "raw"
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
BCN_ZIPS = RAIZ / "data" / "manual" / "v11" / "bcn_hut_trimestral"
OUT = RAIZ / "output" / "v15" / "auditoria" / "turismo"
UMBRAL_Z = 5.0
MAD_MIN = 0.01          # MAD (en log) por debajo de la cual el z robusto no es informativo (MAD casi nula)
MIN_DIFF = 6            # diferencias mínimas por serie para calcular z
MIN_XSEC = 30           # series mínimas para un z de corte transversal
SALTO_ABS, SALTO_REL = 5.0, 0.5   # salto grande en series con MAD casi nula
ESTACIONALES = ("ine_vut", "ine_tmov", "turistas")
SIN_OBSERVAR = ("interpolado", "interpolacion_lineal_entre_observaciones", "anual_asignado")
NO_REDISTRIBUIBLE = ("iab_",)   # Inside Airbnb: sin valores por unidad en la salida

PREFIJOS = ("ine_vut", "vut_", "gva_vut", "bcn_hut", "idescat_", "reate_", "eurostat_plataformas", "iab_", "ine_tmov",
            "turistas", "monitor_plataformas")

warnings.filterwarnings("ignore", category=RuntimeWarning)


# ---------------------------------------------------------------- utilidades


def mes(f: pd.Series) -> pd.Series:
    """fecha_dato 'AAAA-MM-DD' -> índice de mes entero."""
    return f.str[:4].astype(int) * 12 + f.str[5:7].astype(int)


def mlab(m: int) -> str:
    y, mm = divmod(int(m) - 1, 12)
    return f"{y}-{mm + 1:02d}"


def cargar() -> pd.DataFrame:
    con = duckdb.connect()
    cond = " or ".join(f"variable like '{p}%'" for p in PREFIJOS)
    df = con.sql(f"""select territorio_codigo as cod, nivel, periodo, variable, desagregacion as desag, valor, fecha_dato,
                     metodo_dato, edicion, origen, fuente, licencia, redistribuible, posterior_prereg
                     from '{HECHOS}' where not coalesce(muestra_sellada_v6,false) and ({cond})""").df()
    df["m"] = mes(df.fecha_dato)
    return df


def cargar_resultados() -> pd.DataFrame:
    con = duckdb.connect()
    vs = ("serpavi_alquiler_m2_mediana", "incasol_renta_media", "ipva_indice", "ipva_tam_indice")
    lst = ",".join(f"'{v}'" for v in vs)
    df = con.sql(f"""select territorio_codigo as cod, nivel, periodo, variable, desagregacion as desag, valor, frecuencia
                     from '{HECHOS}' where not coalesce(muestra_sellada_v6,false) and variable in ({lst})
                     and valor is not null""").df()
    df = df[df.frecuencia == "A"].copy()
    df["año"] = df.periodo.astype(int)
    return df


def territorios() -> dict[str, set]:
    t = pd.read_parquet(RAIZ / "data" / "base" / "territorios.parquet")
    return {n: set(g.territorio_codigo) for n, g in t.groupby("nivel")}


def r(x, nd=3):
    if x is None:
        return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return round(x, nd) if np.isfinite(x) else None


def spearman(a: pd.Series, b: pd.Series) -> float:
    j = pd.concat([a, b], axis=1).dropna()
    if len(j) < 8 or j.iloc[:, 0].nunique() < 2 or j.iloc[:, 1].nunique() < 2:
        return np.nan
    return float(j.rank().iloc[:, 0].corr(j.rank().iloc[:, 1]))


def pearson_log(a: pd.Series, b: pd.Series) -> float:
    j = pd.concat([a, b], axis=1).dropna()
    if len(j) < 8:
        return np.nan
    x, y = np.log1p(j.iloc[:, 0]), np.log1p(j.iloc[:, 1])
    if x.std() == 0 or y.std() == 0:
        return np.nan
    return float(x.corr(y))


# ---------------------------------------------------------------- 1. atípicos


def z_mad(arr: np.ndarray, min_n: int):
    cnt = np.sum(~np.isnan(arr), axis=1)
    med = np.nanmedian(arr, axis=1)
    mad = np.nanmedian(np.abs(arr - med[:, None]), axis=1)
    ok = (cnt >= min_n) & (mad > MAD_MIN)
    nula = (cnt >= min_n) & ~ok
    z = np.full(arr.shape, np.nan)
    z[ok] = (arr[ok] - med[ok, None]) / (1.4826 * mad[ok, None])
    return z, ok, nula


def lag_variable(var: str, ms: np.ndarray) -> int:
    paso = np.diff(np.sort(ms))
    modo = int(pd.Series(paso).mode().iloc[0]) if len(paso) else 12
    if var.startswith(ESTACIONALES):
        return 12
    return max(modo, 1)


def tarea1_atipicos(D: pd.DataFrame):
    filas, top = [], []
    d = D[~D.metodo_dato.fillna("").isin(SIN_OBSERVAR)].copy()
    d["sid"] = d.cod + "|" + d.desag.fillna("")
    for (var, niv), g in d.groupby(["variable", "nivel"], sort=True):
        if var.startswith("vut_regulacion"):
            continue
        ms_all = np.sort(g.m.unique())
        base = {"variable": var, "nivel": niv, "series": int(g.sid.nunique()), "obs": int(len(g)), "n_periodos": int(len(ms_all))}
        W = g.drop_duplicates(["sid", "m"]).set_index(["sid", "m"]).valor.unstack("m")
        W = W.reindex(columns=range(int(W.columns.min()), int(W.columns.max()) + 1))
        X = W.values.astype(float)
        T = X if np.nanmin(X) < 0 else np.log1p(X)
        if len(ms_all) >= MIN_DIFF + 1:
            L = lag_variable(var, ms_all)
            if X.shape[1] <= L:
                continue
            dif = T[:, L:] - T[:, :-L]
            niv_ant, niv_nue = X[:, :-L], X[:, L:]
            modo = f"serie_temporal(lag={L}m)"
            cols = list(W.columns[L:])
            z, ok, nula = z_mad(dif, MIN_DIFF)
        else:
            if T.shape[0] < MIN_XSEC:
                filas.append({**base, "modo": "omitido(<30 series)", "series_z": 0, "series_mad_nula": 0, "atipicos": 0})
                continue
            if len(ms_all) == 2:
                dif = T[:, [-1]] - T[:, [0]]
                niv_ant, niv_nue = X[:, [0]], X[:, [-1]]
            else:
                dif, niv_ant, niv_nue = T[:, [0]], np.zeros((T.shape[0], 1)), X[:, [0]]
            modo = "corte_transversal"
            cols = [W.columns[-1]]
            v = dif[:, 0]
            v = v[~np.isnan(v)]
            med = float(np.median(v))
            mad = float(np.median(np.abs(v - med)))
            if mad > MAD_MIN:
                z = (dif - med) / (1.4826 * mad)
                ok = ~np.isnan(dif[:, 0])
                nula = np.zeros(dif.shape[0], bool)
            else:
                z = np.full(dif.shape, np.nan)
                ok = np.zeros(dif.shape[0], bool)
                nula = ~np.isnan(dif[:, 0])
        big = np.abs(z) > UMBRAL_Z
        n_at = int(np.nansum(big))
        sal = 0
        if nula.any():
            dl = (niv_nue - niv_ant)[nula]
            rel = dl / np.maximum(niv_ant[nula], 1.0)
            sal = int(np.nansum((np.abs(dl) >= SALTO_ABS) & (np.abs(rel) >= SALTO_REL)))
        n_obs_z = int(np.sum(~np.isnan(z)))
        filas.append({**base, "modo": modo, "series_z": int(ok.sum()), "series_mad_nula": int(nula.sum()),
                      "pct_series_mad_nula": r(100 * nula.sum() / max(ok.sum() + nula.sum(), 1), 1),
                      "obs_z": n_obs_z, "atipicos": n_at, "pct_atipicos": r(100 * n_at / max(n_obs_z, 1), 3),
                      "series_con_atipicos": int(big.any(axis=1).sum()), "saltos_grandes_en_mad_nula": sal})
        if n_at:
            ii, jj = np.where(big)
            for i, j in zip(ii, jj, strict=True):
                sid = W.index[i]
                top.append({"variable": var, "nivel": niv, "cod_ine": sid.split("|")[0], "desag": sid.split("|")[1],
                            "periodo": mlab(cols[j]), "z_robusto": r(z[i, j], 2), "cambio_log": r(dif[i, j], 3)})
    F = pd.DataFrame(filas)
    Tp = pd.DataFrame(top)
    if len(Tp):
        Tp = Tp.reindex(Tp.z_robusto.abs().sort_values(ascending=False, kind="mergesort").index).head(30).reset_index(drop=True)
        mask = Tp.variable.str.startswith(NO_REDISTRIBUIBLE)
        Tp.loc[mask, "cambio_log"] = np.nan   # Inside Airbnb: solo z y código, sin valor
    return F, Tp


def tarea1b_unidades(D: pd.DataFrame, TER: dict) -> pd.DataFrame:
    res = []

    def add(chk, var, n_inc, n_tot, det=""):
        res.append({"comprobacion": chk, "variable": var, "n_incumple": int(n_inc), "n_total": int(n_tot), "detalle": det})

    for var, g in D.groupby("variable"):
        v = g.valor.dropna()
        add("valores_negativos", var, (v < 0).sum(), len(v))
    cnt_vars = [v for v in D.variable.unique() if v.startswith(("ine_vut_vivienda", "ine_vut_plazas", "idescat_", "reate_", "bcn_hut",
                                                                  "iab_n_", "vut_registro_gva"))]
    for var in cnt_vars:
        v = D.loc[D.variable == var, "valor"].dropna()
        add("no_entero_en_recuento", var, (np.abs(v - v.round()) > 1e-9).sum(), len(v))
    p = D[D.variable == "ine_vut_porcentaje_vivienda_turistica"]
    add("porcentaje_fuera_0_100", "ine_vut_porcentaje_vivienda_turistica", ((p.valor < 0) | (p.valor > 100)).sum(), len(p))
    add("porcentaje_mayor_50", "ine_vut_porcentaje_vivienda_turistica", (p.valor > 50).sum(), len(p), "secciones con más de la mitad de viviendas turísticas")
    for niv in ("seccion", "distrito"):
        a = D[(D.variable == "ine_vut_vivienda_turistica") & (D.nivel == niv)].set_index(["cod", "m"]).valor
        b = D[(D.variable == "ine_vut_plazas") & (D.nivel == niv)].set_index(["cod", "m"]).valor
        j = pd.concat([a.rename("v"), b.rename("p")], axis=1).dropna()
        add(f"plazas_con_0_viviendas({niv})", "ine_vut_plazas", ((j.v == 0) & (j.p > 0)).sum(), len(j))
        add(f"viviendas_sin_plazas({niv})", "ine_vut_plazas", ((j.v > 0) & (j.p == 0)).sum(), (j.v > 0).sum())
        rr = (j.p / j.v)[j.v > 0]
        add(f"plazas_por_vivienda_fuera_[1,20]({niv})", "ine_vut_plazas", ((rr < 1) | (rr > 20)).sum(), len(rr),
            f"mediana {rr.median():.2f}, p99 {rr.quantile(.99):.2f}, max {rr.max():.1f}")
    iab = D[D.variable.str.startswith("iab_")].pivot_table(index="cod", columns="variable", values="valor")
    if len(iab):
        tipos = iab[["iab_n_entire_home", "iab_n_private_room", "iab_n_shared_room", "iab_n_hotel_room"]].sum(axis=1)
        add("iab_tipos_no_suman_anuncios", "iab_n_anuncios", (tipos != iab.iab_n_anuncios).sum(), len(iab))
        add("iab_licencias_mayor_anuncios", "iab_n_con_licencia", (iab.iab_n_con_licencia > iab.iab_n_anuncios).sum(), len(iab))
        add("iab_disponibilidad_fuera_0_365", "iab_disponibilidad_365_media",
            ((iab.iab_disponibilidad_365_media < 0) | (iab.iab_disponibilidad_365_media > 365)).sum(), len(iab))
    e = D[D.variable == "eurostat_plataformas_noches"].copy()
    e["tipo"] = e.desag.str.extract(r"c_resid=(\w+)")[0]
    w = e.pivot_table(index=["cod", "periodo"], columns="tipo", values="valor").dropna()
    add("eurostat_total_distinto_dom_mas_for", "eurostat_plataformas_noches", (np.abs(w.TOTAL - w.DOM - w.FOR) > 1).sum(), len(w))
    b = D[D.variable == "bcn_hut_registro"].copy()
    b["barrio"] = b.desag.str.replace("barrio_bcn=", "", regex=False)
    tot = b[b.barrio == "Total"].set_index("periodo").valor
    sb = b[b.barrio != "Total"].groupby("periodo").valor.agg(["sum", "size"])
    jj = sb.join(tot.rename("total"), how="inner")
    add("bcn_suma_barrios_distinta_total", "bcn_hut_registro", (jj["sum"] != jj.total).sum(), len(jj), f"cortes con barrios: {len(jj)}")
    for (var, niv), g in D.groupby(["variable", "nivel"]):
        if niv in TER:
            cods = g.cod.unique()
            malos = [c for c in cods if c not in TER[niv]]
            add(f"codigo_ine_no_en_territorios({niv})", var, len(malos), len(cods), ("ej.: " + ",".join(sorted(malos)[:5])) if malos else "")
    out = pd.DataFrame(res)
    return out[(out.n_incumple > 0) | out.comprobacion.str.contains("plazas|iab|eurostat|bcn|porcentaje_fuera")].reset_index(drop=True)


# ---------------------------------------------------------------- 2. coherencia


def ine_municipal(D: pd.DataFrame, var: str = "ine_vut_vivienda_turistica") -> pd.DataFrame:
    s = D[(D.variable == var) & (D.nivel == "seccion")].copy()
    s["mun"] = s.cod.str[:5]
    return s.groupby(["mun", "m"]).valor.sum().unstack("m")


def stats_par(ine: pd.Series, reg: pd.Series, prov_reg: tuple, ausente_cero: bool) -> dict:
    uni = [c for c in ine.index if c[:2] in prov_reg]
    a = ine.reindex(uni)
    b = reg.reindex(uni)
    if ausente_cero:
        b = b.fillna(0.0)
    ap, bp = a > 0, b > 0
    amb = ap & bp
    rat = b[amb] / a[amb]
    return {"n_municipios_ine_universo": int(a.notna().sum()), "n_ine_pos": int(ap.sum()), "n_reg_pos": int(bp.sum()),
            "n_ambos_pos": int(amb.sum()), "suma_ine": r(a.sum(), 0), "suma_reg": r(b.sum(), 0),
            "ratio_suma_reg_ine": r(b.sum() / a.sum(), 3) if a.sum() else None,
            "ratio_mediano": r(rat.median(), 3), "ratio_p10": r(rat.quantile(.1), 3), "ratio_p90": r(rat.quantile(.9), 3),
            "pct_ratio_fuera_0.5_2": r(100 * ((rat < .5) | (rat > 2)).mean(), 1) if len(rat) else None,
            "pct_ine_pos_reg_cero": r(100 * (ap & ~bp).sum() / max(ap.sum(), 1), 1),
            "pct_viviendas_ine_en_reg_cero": r(100 * a[ap & ~bp].sum() / max(a.sum(), 1), 2),
            "pct_reg_pos_ine_cero": r(100 * (bp & ~ap).sum() / max(bp.sum(), 1), 1),
            "spearman": r(spearman(a, b)), "pearson_log": r(pearson_log(a, b))}


def serie_corr(ine_w: pd.DataFrame, reg_w: pd.DataFrame, umbral: float = 20.0) -> dict:
    cs, cd, n = [], [], 0
    for c in ine_w.index.intersection(reg_w.index):
        j = pd.concat([ine_w.loc[c].rename("a"), reg_w.loc[c].rename("b")], axis=1).dropna()
        if len(j) < 6 or j.a.max() < umbral:
            continue
        n += 1
        if j.a.std() > 0 and j.b.std() > 0:
            cs.append(j.a.corr(j.b))
        da, db = j.a.diff().dropna(), j.b.diff().dropna()
        if da.std() > 0 and db.std() > 0:
            cd.append(da.corr(db))

    def q(x, p):
        return r(np.quantile(x, p)) if len(x) else None
    return {"n_municipios_serie": n, "corr_niveles_mediana": q(cs, .5), "corr_niveles_p25": q(cs, .25),
            "corr_cambios_mediana": q(cd, .5), "corr_cambios_p25": q(cd, .25), "corr_cambios_p75": q(cd, .75)}


def cercano(m: int, grid: np.ndarray, tol: int):
    if len(grid) == 0:
        return None
    k = int(grid[np.argmin(np.abs(grid - m))])
    return k if abs(k - m) <= tol else None


def tarea2_coherencia(D: pd.DataFrame) -> dict:
    ine_v = ine_municipal(D)
    ine_p = ine_municipal(D, "ine_vut_plazas")
    per_ine = list(ine_v.columns)
    cortes, totales, series, extras = [], [], [], {}

    def reg_wide(var: str, nivel="municipio") -> pd.DataFrame:
        g = D[(D.variable == var) & (D.nivel == nivel)]
        return g.drop_duplicates(["cod", "m"]).set_index(["cod", "m"]).valor.unstack("m")

    gva = reg_wide("vut_registro_gva_reconstruido")
    gva_c = reg_wide("vut_registro_gva")
    ide = reg_wide("idescat_hut_n")
    idp = reg_wide("idescat_hut_plazas")
    bcn_city = D[(D.variable == "bcn_hut_registro") & (D.desag == "barrio_bcn=Total")].set_index("m").valor
    reate = reg_wide("reate_viviendas_uso_turistico")

    def registrar(par, mi, mr, ine_s, reg_s, provs, ac):
        st = stats_par(ine_s, reg_s, provs, ac)
        cortes.append({"par": par, "periodo_ine": mlab(mi), "periodo_registro": mlab(mr), "gap_meses": int(mr - mi), **st})

    pr_gva = ("03", "12", "46")
    pares_gva = {}
    for mi in per_ine:
        if mi in gva.columns:
            registrar("INE_VUT vs GVA_reconstruido", mi, mi, ine_v[mi], gva[mi], pr_gva, True)
            pares_gva[mi] = mi
    m26 = max(gva_c.columns)
    registrar("INE_VUT vs GVA_corte_2026-10", max(per_ine), m26, ine_v[max(per_ine)], gva_c[m26], pr_gva, True)
    pr_cat = ("08", "17", "25", "43")
    pares_ide = {}
    for mi in per_ine:
        mr = cercano(mi, np.array(list(ide.columns)), 4)
        if mr is not None:
            registrar("INE_VUT vs IDESCAT_HUT_n", mi, mr, ine_v[mi], ide[mr], pr_cat, False)
            pares_ide[mi] = mr
            if mr in idp.columns:
                registrar("INE_plazas vs IDESCAT_HUT_plazas", mi, mr, ine_p[mi], idp[mr], pr_cat, False)
    pr_eus = ("01", "20", "48")
    mre = max(reate.columns)
    for mi in sorted(per_ine)[-2:]:
        registrar("INE_VUT vs REATE", mi, mre, ine_v[mi], reate[mre], pr_eus, False)
    ine08019 = ine_v.loc["08019"] if "08019" in ine_v.index else pd.Series(dtype=float)
    bcn_idx = np.array(list(bcn_city.index))
    filas_bcn = []
    for mi in per_ine:
        mr = cercano(mi, bcn_idx, 2)
        if mr is not None:
            filas_bcn.append((mi, mr, float(ine08019[mi]), float(bcn_city[mr])))
    BC = pd.DataFrame(filas_bcn, columns=["mi", "mr", "ine", "bcn"])
    BC["ratio_bcn_ine"] = BC.bcn / BC.ine
    extras["bcn_ciudad_vs_ine"] = {
        "n_pares": int(len(BC)), "ratio_mediano": r(BC.ratio_bcn_ine.median()), "ratio_min": r(BC.ratio_bcn_ine.min()),
        "ratio_max": r(BC.ratio_bcn_ine.max()), "corr_niveles": r(BC.ine.corr(BC.bcn)),
        "corr_cambios": r(BC.ine.diff().corr(BC.bcn.diff())), "ine_viv_primero": r(BC.ine.iloc[0], 0), "bcn_primero": r(BC.bcn.iloc[0], 0),
        "ine_viv_ultimo": r(BC.ine.iloc[-1], 0), "bcn_ultimo": r(BC.bcn.iloc[-1], 0),
        "nota": "INE VUT (anuncios en plataformas, sección) frente a registro municipal de HUT (licencias comunicadas)"}
    for _, x in BC.iterrows():
        totales.append({"par": "INE_VUT vs BCN_HUT_ciudad", "periodo_ine": mlab(int(x.mi)), "periodo_registro": mlab(int(x.mr)),
                        "suma_ine": r(x.ine, 0), "suma_registro": r(x.bcn, 0), "ratio": r(x.ratio_bcn_ine)})
    if "08019" in ide.index:
        com = [m for m in ide.columns if cercano(m, bcn_idx, 1) is not None]
        a = pd.Series({m: ide.loc["08019", m] for m in com})
        b = pd.Series({m: bcn_city[cercano(m, bcn_idx, 1)] for m in com})
        extras["bcn_vs_idescat_08019"] = {"n_pares": int(len(a)), "ratio_mediano_bcn_idescat": r((b / a).median()),
                                          "ratio_min": r((b / a).min()), "ratio_max": r((b / a).max()), "corr_niveles": r(a.corr(b)),
                                          "idescat_n_ultimo": r(a.iloc[-1], 0), "bcn_ultimo": r(b.iloc[-1], 0)}
    series.append({"par": "INE_VUT vs GVA_reconstruido", **serie_corr(ine_v[list(pares_gva)], gva[list(pares_gva)])})
    if pares_ide:
        a = ine_v[list(pares_ide)]
        b = ide[[pares_ide[m] for m in pares_ide]].copy()
        b.columns = list(pares_ide)
        series.append({"par": "INE_VUT vs IDESCAT_HUT_n", **serie_corr(a, b)})

    def tot_region(par, pares, ine_w_, reg_w_, provs, ac):
        rows = []
        for mi, mr in pares.items():
            uni = [c for c in ine_w_.index if c[:2] in provs]
            a = ine_w_.loc[uni, mi].sum()
            b = reg_w_.reindex(uni)[mr]
            b = (b.fillna(0) if ac else b).sum()
            rows.append({"par": par, "periodo_ine": mlab(mi), "periodo_registro": mlab(mr), "suma_ine": r(a, 0), "suma_registro": r(b, 0),
                         "ratio": r(b / a)})
        return rows
    totales += tot_region("INE_VUT vs GVA_reconstruido (CV)", pares_gva, ine_v, gva, pr_gva, True)
    totales += tot_region("INE_VUT vs IDESCAT_HUT_n (Cataluña)", pares_ide, ine_v, ide, pr_cat, False)
    TOT = pd.DataFrame(totales)
    div = []
    for par in TOT.par.unique():
        t = TOT[TOT.par == par].copy()
        t["mi"] = [int(x[:4]) * 12 + int(x[5:7]) for x in t.periodo_ine]
        t = t.set_index("mi")
        for mi in t.index:
            if mi - 12 in t.index:
                ti = t.loc[mi, "suma_ine"] / t.loc[mi - 12, "suma_ine"] - 1
                tr = t.loc[mi, "suma_registro"] / t.loc[mi - 12, "suma_registro"] - 1
                div.append({"par": par, "periodo": mlab(mi), "tasa_ine_pct": r(100 * ti, 1), "tasa_registro_pct": r(100 * tr, 1),
                            "signo_opuesto": bool(np.sign(ti) != np.sign(tr) and abs(ti) > .01 and abs(tr) > .01),
                            "dif_pp": r(100 * (tr - ti), 1)})
    DIV = pd.DataFrame(div)
    iab = D[D.variable.str.startswith("iab_")].pivot_table(index="cod", columns="variable", values="valor")
    iab_rows = []
    for mi in sorted(per_ine)[-2:]:
        s = D[(D.variable == "ine_vut_vivienda_turistica") & (D.nivel == "seccion") & (D.m == mi)].set_index("cod").valor
        j = iab.join(s.rename("ine"), how="left")
        j["mun"] = j.index.str[:5]
        s_all = s.copy()
        for mun, g in list(j.groupby("mun")) + [("TODAS", j)]:
            if len(g) < 100:
                continue
            ine_fuera = s_all[(s_all > 0) & ~s_all.index.isin(iab.index)]
            if mun != "TODAS":
                ine_fuera = ine_fuera[ine_fuera.index.str[:5] == mun]
            else:
                ine_fuera = ine_fuera[ine_fuera.index.str[:5].isin(set(j.mun))]
            ine_tot = s_all[s_all.index.str[:5] == mun] if mun != "TODAS" else s_all[s_all.index.str[:5].isin(set(j.mun))]
            iab_rows.append({"periodo_ine": mlab(mi), "mun_ine": mun, "n_secciones": int(len(g)), "secciones_sin_dato_ine": int(g.ine.isna().sum()),
                             "secciones_ine_pos_fuera_de_iab": int(len(ine_fuera)), "viviendas_ine_en_secciones_fuera_de_iab": r(ine_fuera.sum(), 0),
                             "pct_viviendas_ine_fuera_de_iab": r(100 * ine_fuera.sum() / max(ine_tot.sum(), 1), 1),
                             "suma_ine": r(g.ine.sum(), 0), "suma_iab_anuncios": r(g.iab_n_anuncios.sum(), 0),
                             "suma_iab_vivienda_entera": r(g.iab_n_entire_home.sum(), 0),
                             "ratio_iab_entera_ine": r(g.iab_n_entire_home.sum() / g.ine.sum()) if g.ine.sum() else None,
                             "pct_iab_con_licencia": r(100 * g.iab_n_con_licencia.sum() / max(g.iab_n_anuncios.sum(), 1), 1),
                             "spearman_ine_iab_entera": r(spearman(g.ine, g.iab_n_entire_home)),
                             "pearson_log_ine_iab_entera": r(pearson_log(g.ine, g.iab_n_entire_home)),
                             "spearman_ine_iab_anuncios": r(spearman(g.ine, g.iab_n_anuncios)),
                             "pct_secc_ine_pos_iab_cero": r(100 * ((g.ine > 0) & (g.iab_n_anuncios == 0)).sum() / max((g.ine > 0).sum(), 1), 1),
                             "pct_secc_iab_pos_ine_cero": r(100 * ((g.ine == 0) & (g.iab_n_anuncios > 0)).sum() / max((g.iab_n_anuncios > 0).sum(), 1), 1)})
    IAB = pd.DataFrame(iab_rows)
    dis = D[(D.variable == "ine_vut_vivienda_turistica") & (D.nivel == "distrito")].set_index(["cod", "m"]).valor
    sec = D[(D.variable == "ine_vut_vivienda_turistica") & (D.nivel == "seccion")].copy()
    sec["dis"] = sec.cod.str[:7]
    sec["prov"] = sec.cod.str[:2]
    sd = sec.groupby(["dis", "m"]).valor.sum()
    j = pd.concat([sd.rename("s"), dis.rename("d")], axis=1).dropna()
    niv_cons = {"distrito_vs_suma_secciones": {"n_pares": int(len(j)), "pct_distintos": r(100 * (j.s != j.d).mean(), 2),
                                               "suma_secciones": r(j.s.sum(), 0), "suma_distritos": r(j.d.sum(), 0),
                                               "dif_media_abs": r((j.s - j.d).abs().mean(), 3)}}
    vv = D[(D.variable == "vut_viviendas") & (D.metodo_dato == "observado")]
    tot_nac = sec.groupby("m").valor.sum()
    tot_prov = sec.groupby(["prov", "m"]).valor.sum()
    rows = []
    for _, x in vv.iterrows():
        mi_ = cercano(int(x.m), np.array(sorted(tot_nac.index)), 1)
        if mi_ is None:
            continue
        if x.nivel == "nacional":
            a = tot_nac.get(mi_, np.nan)
        elif x.nivel == "provincia":
            a = tot_prov.get((x.cod, mi_), np.nan)
        else:
            continue
        rows.append({"nivel": x.nivel, "cod": x.cod, "m": x.m, "pub": float(x.valor), "secc": a})
    VV = pd.DataFrame(rows)
    if len(VV):
        VV = VV[VV.secc > 0].copy()
        VV["ratio"] = VV.pub / VV.secc
        nac, prv = VV[VV.nivel == "nacional"], VV[VV.nivel == "provincia"]
        niv_cons["publicado_vs_suma_secciones"] = {
            "n_pares_nacional": int(len(nac)), "nacional_ratio_mediano": r(nac.ratio.median()),
            "nacional_ratio_min_max": [r(nac.ratio.min()), r(nac.ratio.max())],
            "n_pares_provincia": int(len(prv)), "provincia_ratio_mediano": r(prv.ratio.median()),
            "provincia_ratio_min_max": [r(prv.ratio.min()), r(prv.ratio.max())],
            "nota": "vut_viviendas observado (tabla provincial/nacional INE) frente a la suma de secciones en el mismo mes"}
    e = D[(D.variable == "eurostat_plataformas_noches") & (D.cod == "ES") & D.desag.str.contains("c_resid=TOTAL")].set_index("periodo").valor
    mo = D[D.variable == "monitor_plataformas_noches"].set_index("periodo").valor
    jj = pd.concat([e.rename("eu"), mo.rename("mon")], axis=1).dropna()
    extras["eurostat_vs_monitor_nacional"] = {"n_años": int(len(jj)), "ratio_mediano": r((jj.mon / jj.eu).median()),
                                              "ratio_min": r((jj.mon / jj.eu).min()), "ratio_max": r((jj.mon / jj.eu).max()),
                                              "nota": "tour_ce_oan3 (ES, TOTAL) frente al monitor V10 (tour_ce_omr): cociente casi constante, definiciones distintas; no son la misma magnitud"}
    return {"cortes": pd.DataFrame(cortes), "totales": TOT, "divergencias": DIV, "series": pd.DataFrame(series), "iab": IAB,
            "niveles": niv_cons, "extras": extras}


# ---------------------------------------------------------------- GVA: lectura de cortes crudos


def leer_gva(path: Path) -> pd.DataFrame:
    h = pd.read_csv(path, sep=";", encoding="latin-1", dtype=str)
    h.columns = [c.strip() for c in h.columns]
    if "Cod. Provincia" in h.columns:
        ine5 = h["Cod. Provincia"].str.strip().str.zfill(2) + h["Cod. Municipio"].str.strip().str.zfill(3)
        alta = pd.to_datetime(h["Fecha alta"].str.strip(), format="%d/%m/%Y", errors="coerce")
        baja = pd.to_datetime(h["Fecha baja"].fillna("").str.strip().replace("", np.nan), format="%d/%m/%Y", errors="coerce")
        out = pd.DataFrame({"signatura": h["Signatura"].str.strip(), "ine5": ine5, "estado": h["Estado"].str.strip().str.upper(),
                            "tipo": h["Tipo"], "alta": alta, "baja": baja})
        cols = ["Dirección", "Urbanizacion", "Edificio", "Bloque", "Escalera", "Piso", "Puerta"]
        out["clave"] = ine5 + "|" + h[cols].fillna("").apply(lambda s: s.str.strip().str.upper()).agg("|".join, axis=1)
        out["piso_puerta"] = (h["Piso"].fillna("").str.strip() != "") | (h["Puerta"].fillna("").str.strip() != "")
        return out
    ine5 = h["cod_provincia"].str.strip().str.zfill(2) + h["cod_municipio"].str.strip().str.zfill(3)
    return pd.DataFrame({"signatura": h["signatura"].str.strip(), "ine5": ine5, "estado": "ALTA",
                         "alta": pd.to_datetime(h["fecha_alta"], format="%d/%m/%Y", errors="coerce")})


# ---------------------------------------------------------------- 3. vintages


def tarea3_vintages(D: pd.DataFrame) -> dict:
    V = (D.groupby("variable").agg(n_ediciones=("edicion", "nunique"), n_fechas=("fecha_dato", "nunique"), edicion=("edicion", "first"),
                                   origen=("origen", "first"), n_filas=("valor", "size"), redistribuible=("redistribuible", "all"),
                                   n_posterior_prereg=("posterior_prereg", "sum")).reset_index())
    V["descarga"] = V.edicion.str.extract(r"(20\d\d-\d\d-\d\d)")[0]
    V["edicion"] = V.edicion.str[:60]
    out = {}
    v2 = pd.read_csv(RAW / "ine_v2_vut.csv", dtype={"codigo": str})
    v2["m"] = v2.fecha.str[:4].astype(int) * 12 + v2.fecha.str[5:7].astype(int)
    mun = v2[(v2.nivel == "municipio") & (v2.medida == "viviendas_turisticas")]
    sec = D[(D.variable == "ine_vut_vivienda_turistica") & (D.nivel == "seccion")].copy()
    sec["prov"] = sec.cod.str[:2]
    tp = sec.groupby(["prov", "m"]).valor.sum()
    tn = sec.groupby("m").valor.sum()
    pv = v2[(v2.nivel == "provincia") & (v2.medida == "viviendas_turisticas")].drop_duplicates(["codigo", "m"]).set_index(["codigo", "m"]).valor
    pv.index.names = ["prov", "m"]
    jp = pd.concat([pv.rename("tabla_provincial"), tp.rename("suma_secciones")], axis=1).dropna()
    nv = v2[(v2.nivel == "nacional") & (v2.medida == "viviendas_turisticas")].drop_duplicates("m").set_index("m").valor
    jn_ = pd.concat([nv.rename("tabla_nacional"), tn.rename("suma_secciones")], axis=1).dropna()
    out["ine_vut_tablas_tempus_vs_secciones_gis"] = {
        "tabla_municipal_tempus_con_codigo_ine": int(mun.codigo.notna().sum()), "tabla_municipal_filas": int(len(mun)),
        "municipios_en_tabla_municipal_por_nombre": int(mun.territorio.nunique()),
        "periodos_solo_en_tempus": sorted({mlab(m) for m in v2.m.unique()} - {mlab(m) for m in sec.m.unique()}),
        "n_pares_provincia": int(len(jp)), "provincia_pct_iguales": r(100 * (jp.tabla_provincial == jp.suma_secciones).mean(), 1),
        "provincia_ratio_suma": r(jp.tabla_provincial.sum() / jp.suma_secciones.sum(), 4),
        "provincia_dif_rel_max_pct": r(100 * ((jp.tabla_provincial - jp.suma_secciones).abs() / jp.suma_secciones.where(jp.suma_secciones > 0)).max(), 2),
        "n_pares_nacional": int(len(jn_)), "nacional_ratio_suma": r(jn_.tabla_nacional.sum() / jn_.suma_secciones.sum(), 4),
        "nacional_ratio_min_max": [r((jn_.tabla_nacional / jn_.suma_secciones).min(), 4), r((jn_.tabla_nacional / jn_.suma_secciones).max(), 4)],
        "nota": ("la tabla municipal de tempus (39363) del raw no trae código INE (solo nombre): no se cruza; se comparan provincia y nacional. "
                 "Descargas del mismo día (2026-10-10) de dos servicios del INE: no son revisiones")}
    cort = RAW / "v9" / "gva_vut" / "cortes"
    h = leer_gva(cort / "vut_historico_2025-01-26.csv.gz")
    u = leer_gva(cort / "vut_ultimo_periodo_2025-01-26.csv.gz")
    ah = h[h.estado == "ALTA"].groupby("ine5").size()
    au = u[u.estado == "ALTA"].groupby("ine5").size()
    jj = pd.concat([ah.rename("historico"), au.rename("ultimo")], axis=1).fillna(0)
    sh, su = set(h[h.estado == "ALTA"].signatura), set(u[u.estado == "ALTA"].signatura)
    out["gva_historico_vs_ultimo_periodo_2025-01-26"] = {
        "alta_historico": len(sh), "alta_ultimo_periodo": len(su), "en_ambos": len(sh & su), "solo_historico": len(sh - su),
        "solo_ultimo": len(su - sh), "municipios_con_diferencia": int((jj.historico != jj.ultimo).sum()), "municipios_total": int(len(jj)),
        "dif_abs_municipal_max": int((jj.historico - jj.ultimo).abs().max()),
        "nota": "misma fecha de referencia, dos recursos del mismo conjunto CKAN descargados el mismo día (2026-10-14): no es una revisión temporal"}
    g = pd.read_csv(RAW / "gva_vut_municipio.csv", dtype={"codigo": str})
    g = g[g.serie.str.startswith("vut_stock_mun_")].copy()
    g["mm"] = g.periodo.str[:4].astype(int) * 12 + g.periodo.str[5:7].astype(int)
    g["cod"] = g.serie.str[-5:]
    old = g.drop_duplicates(["cod", "mm"]).set_index(["cod", "mm"]).valor
    new = D[D.variable == "vut_registro_gva_reconstruido"].drop_duplicates(["cod", "m"]).set_index(["cod", "m"]).valor
    new.index.names = ["cod", "mm"]
    jn = pd.concat([old.rename("pull_v1_v8"), new.rename("reconstruido_v9")], axis=1)
    mm = jn.index.get_level_values("mm")
    jn = jn.loc[(mm >= 2015 * 12 + 1) & (mm <= 2024 * 12 + 12)].fillna(0)
    jn = jn[(jn.pull_v1_v8 > 0) | (jn.reconstruido_v9 > 0)]
    d = jn.reconstruido_v9 - jn.pull_v1_v8
    por_mes = jn.groupby("mm").sum()
    sel = {mlab(m): r(por_mes.loc[m, "reconstruido_v9"] / por_mes.loc[m, "pull_v1_v8"], 4)
           for m in (2015 * 12 + 12, 2018 * 12 + 12, 2020 * 12 + 12, 2022 * 12 + 12, 2024 * 12 + 12)}
    out["gva_stock_pull_v1v8_vs_reconstruccion_v9"] = {
        "n_municipio_mes": int(len(jn)), "pct_iguales": r(100 * (d == 0).mean(), 2), "dif_abs_media": r(d.abs().mean(), 3),
        "ratio_suma_v9_sobre_v1v8": sel,
        "nota": "dos descargas del registro GVA (2026-10-09 recurso modificado 2025-11-12; 2026-10-14 corte 2025-01-26)"}
    cat = pd.read_csv(RAW / "v3" / "hut_registro_turismo_cat_v3.csv.gz", dtype={"codigo": str})
    cm_ = cat[(cat.nivel == "MUNICIPIO") & (cat.serie == "HUT_establecimientos_Habitatges_d_ús_turístic_Alta")].groupby("codigo").valor.sum()
    ide = D[(D.variable == "idescat_hut_n") & (D.periodo == "2025")].set_index("cod").valor
    jc = pd.concat([cm_.rename("registro"), ide.rename("idescat")], axis=1).fillna(0)
    jc = jc[(jc.registro > 0) | (jc.idescat > 0)]
    ambos = jc[(jc.registro > 0) & (jc.idescat > 0)]
    out["cat_registro_socrata_vs_idescat_2025"] = {
        "n_municipios": int(len(jc)), "suma_registro": r(jc.registro.sum(), 0), "suma_idescat": r(jc.idescat.sum(), 0),
        "ratio_suma": r(jc.registro.sum() / jc.idescat.sum()), "pct_iguales": r(100 * (jc.registro == jc.idescat).mean(), 1),
        "ratio_mediano_ambos": r((ambos.registro / ambos.idescat).median()), "spearman": r(spearman(jc.registro, jc.idescat)),
        "nota": "valores resumen; el registro de Catalunya (licencia «Ver términos de uso») no se reproduce por municipio"}
    ex = pd.read_csv(RAW / "v9" / "bcn_hut" / "bcn_hut_barrio_anio_expediente.csv.gz")
    exb = ex.groupby("codi_barri").n_hut.sum()
    bb = D[(D.variable == "bcn_hut_registro") & (D.periodo == "2026T3") & (D.desag != "barrio_bcn=Total")].copy()
    bb["codi"] = bb.desag.str.replace("barrio_bcn=", "", regex=False).astype(int)
    q = bb.set_index("codi").valor
    jb = pd.concat([exb.rename("vigente_expediente"), q.rename("corte_2026T3")], axis=1).fillna(0)
    out["bcn_vigente_expediente_vs_corte_2026T3"] = {
        "total_vigente": int(ex.n_hut.sum()), "total_corte_2026T3": int(q.sum()), "n_barrios": int(len(jb)),
        "barrios_distintos": int((jb.vigente_expediente != jb.corte_2026T3).sum()),
        "dif_abs_max_barrio": int((jb.vigente_expediente - jb.corte_2026T3).abs().max()),
        "corr_barrios": r(jb.vigente_expediente.corr(jb.corte_2026T3), 4),
        "nota": "descargas de 2026-10-15 (API datastore) y 2026-10-16 (zip trimestral): mismo registro con un día de diferencia"}
    ia = pd.read_csv(RAW / "v3" / "airbnb_insideairbnb_agregados_v3.csv.gz")
    ia["ciudad"] = ia.serie.str.extract(r"__(\w+)$")[0]
    out["insideairbnb_instantaneas_v3"] = {"fechas_por_ciudad": {k: int(v) for k, v in ia.groupby("ciudad").periodo.nunique().items()},
                                           "nota": "scrapes distintos: son instantáneas, no revisiones de un mismo corte; en base solo 2026-09"}
    return {"tabla": V, "pares": out}


# ---------------------------------------------------------------- 4. fechado


def stock_mensual(ine5: pd.Series, alta: pd.Series, baja: pd.Series, m0: int, m1: int, sh_alta: int = 0, sh_baja: int = 0) -> pd.DataFrame:
    """Stock a fin de mes (alta <= fin de mes y (sin baja o baja > fin de mes)); desplazamientos en meses (negativo = antes)."""
    ok = baja.isna() | (baja >= alta)
    ma = (alta.dt.year * 12 + alta.dt.month + sh_alta).clip(lower=m0 - 1)
    mb = (baja.dt.year * 12 + baja.dt.month + sh_baja).clip(lower=m0 - 1)
    cols = list(range(m0 - 1, m1 + 1))
    A = pd.DataFrame({"ine5": ine5[ok], "m": ma[ok]}).groupby(["ine5", "m"]).size().unstack("m").reindex(columns=cols).fillna(0)
    sel = ok & baja.notna()
    B = pd.DataFrame({"ine5": ine5[sel], "m": mb[sel]}).groupby(["ine5", "m"]).size().unstack("m").reindex(columns=cols).fillna(0)
    B = B.reindex(A.index).fillna(0)
    return (A.cumsum(axis=1) - B.cumsum(axis=1))[list(range(m0, m1 + 1))]


def tarea4_fechado(D: pd.DataFrame):
    h = leer_gva(RAW / "v9" / "gva_vut" / "cortes" / "vut_historico_2025-01-26.csv.gz")
    u26 = leer_gva(RAW / "v9" / "gva_vut" / "cortes" / "vut_actual_2026-10-14.csv.gz")
    u25 = leer_gva(RAW / "v9" / "gva_vut" / "cortes" / "vut_ultimo_periodo_2025-01-26.csv.gz")
    m0, m1 = 2015 * 12 + 1, 2025 * 12 + 1
    S0 = stock_mensual(h.ine5, h.alta, h.baja, m0, m1)
    out = {}
    base = D[D.variable == "vut_registro_gva_reconstruido"].drop_duplicates(["cod", "m"]).set_index(["cod", "m"]).valor.unstack("m")
    base = base.reindex(columns=range(m0, m1 + 1)).fillna(0)
    com = S0.index.intersection(base.index)
    d = S0.loc[com] - base.loc[com]
    extra = [c for c in S0.index if c not in base.index]
    out["reproduccion_base"] = {"municipios_reconstruidos": int(len(S0)), "municipios_base": int(len(base)),
                                "celdas_distintas_en_comunes": int((d != 0).sum().sum()), "celdas_comunes": int(d.size),
                                "municipios_reconstruidos_no_en_base": {c: int(S0.loc[c].max()) for c in extra},
                                "total_2025-01_reconstruido": int(S0[m1].sum()), "total_2025-01_base": int(base[m1].sum()),
                                "nota": "máximo de viviendas en los municipios no incluidos en la base; el código 03000 no es un municipio INE"}
    TERM = territorios()["municipio"]
    malos = [c for c in S0.index if c not in TERM]
    out["codigos_no_ine"] = {"n": len(malos), "lista": malos[:10], "viviendas_2025-01": int(S0.loc[malos, m1].sum()) if malos else 0}
    nb = ((h.estado == "BAJA") & h.baja.isna())
    out["registros_historico"] = {
        "total": int(len(h)), "alta": int((h.estado == "ALTA").sum()), "baja": int((h.estado == "BAJA").sum()),
        "baja_sin_fecha_baja": int(nb.sum()), "alta_sin_fecha_alta": int(h.alta.isna().sum()),
        "baja_anterior_a_alta": int((h.baja < h.alta).sum()),
        "alta_antes_de_2015": int((h.alta < "2015-01-01").sum()), "alta_en_1993_1994": int(h.alta.dt.year.isin([1993, 1994]).sum()),
        "pct_1993_1994_sobre_altas_antes_2015": r(100 * h.alta.dt.year.isin([1993, 1994]).sum() / max((h.alta < "2015-01-01").sum(), 1), 1),
        "alta_posterior_a_2025-01-26": int((h.alta > "2025-01-26").sum()), "baja_posterior_a_2025-01-26": int((h.baja > "2025-01-26").sum()),
        "tipo_distinto_unidad_alojamiento": int((h.tipo != "Unidad de Alojamiento Turístico").sum())}
    out["stock_2025-01"] = {"reconstruido": int(S0[m1].sum()), "estado_ALTA_historico": int((h.estado == "ALTA").sum()),
                            "ultimo_periodo_ALTA": int((u25.estado == "ALTA").sum()), "corte_2026-10-14": int(len(u26))}
    ok = h.baja.isna() | (h.baja >= h.alta)
    filas = []
    for año in (2015, 2016, 2018, 2020, 2022, 2024):
        fin = pd.Timestamp(año, 12, 31)
        viv = ok & (h.alta <= fin) & (h.baja.isna() | (h.baja > fin))
        st = int(viv.sum())
        rec = int((viv & (h.alta > pd.Timestamp(año - 1, 12, 31))).sum())
        her = int((viv & (h.alta < pd.Timestamp("2015-01-01"))).sum())
        mig = int((viv & h.alta.dt.year.isin([1993, 1994])).sum())
        sal = int((viv & h.baja.notna() & (h.baja <= pd.Timestamp(año + 2, 12, 31))).sum())
        filas.append({"fecha": f"{año}-12", "stock": st, "pct_alta_ultimos_12m": r(100 * rec / st, 1),
                      "pct_alta_anterior_2015_heredado": r(100 * her / st, 1), "pct_alta_1993_1994_migracion": r(100 * mig / st, 1),
                      "pct_con_baja_en_siguientes_24m": r(100 * sal / st, 1)})
    COH = pd.DataFrame(filas)
    esc = {"S0_base": (0, 0), "S1_alta_6m_antes": (-6, 0), "S2_alta_12m_antes": (-12, 0), "S3_baja_12m_antes": (0, -12),
           "S4_alta_y_baja_12m_antes": (-12, -12), "S5_alta_12m_despues": (12, 0)}
    stocks = {n: stock_mensual(h.ine5, h.alta, h.baja, m0, m1, sa, sb) for n, (sa, sb) in esc.items()}
    S0b = stocks["S0_base"]
    ESC = []
    for nombre, S in stocks.items():
        for año in (2016, 2018, 2020, 2022, 2024):
            m = año * 12 + 12
            a = S0b[m]
            b = S[m].reindex(S0b.index).fillna(0)
            mask = a > 0
            rel = ((b - a).abs() / a)[mask]
            ESC.append({"escenario": nombre, "fecha": f"{año}-12", "stock_total": int(b.sum()),
                        "dif_total_vs_base_pct": r(100 * (b.sum() / a.sum() - 1), 2),
                        "mediana_dif_rel_municipal_pct": r(100 * rel.median(), 1),
                        "pct_municipios_dif_gt_10pct": r(100 * (rel > .10).mean(), 1),
                        "pct_municipios_dif_gt_25pct": r(100 * (rel > .25).mean(), 1)})
    ESC = pd.DataFrame(ESC)
    hh = h[(h.tipo == "Unidad de Alojamiento Turístico") & h.piso_puerta & h.alta.notna()].copy()
    bj = hh[hh.baja.notna()][["clave", "signatura", "baja"]].rename(columns={"signatura": "s_baja"})
    al = hh[["clave", "signatura", "alta"]].rename(columns={"signatura": "s_alta"})
    mg = bj.merge(al, on="clave")
    mg = mg[mg.s_baja != mg.s_alta]
    mg["dd"] = (mg.alta - mg.baja).dt.days
    rec = {"unidades_con_piso_o_puerta": int(len(hh))}
    for nombre, (lo, hi) in {"ventana_pm30d": (-30, 30), "ventana_-30d_a_+365d": (-30, 365)}.items():
        x = mg[(mg.dd >= lo) & (mg.dd <= hi)]
        nb_ = ((hh.baja.dt.year >= 2016) & (hh.baja.dt.year <= 2024)).sum()
        na_ = ((hh.alta.dt.year >= 2016) & (hh.alta.dt.year <= 2024)).sum()
        rec[nombre] = {"bajas_con_alta_en_mismo_domicilio": int(x.s_baja.nunique()), "altas_con_baja_en_mismo_domicilio": int(x.s_alta.nunique()),
                       "pct_bajas_2016_2024": r(100 * x[(x.baja.dt.year >= 2016) & (x.baja.dt.year <= 2024)].s_baja.nunique() / max(nb_, 1), 1),
                       "pct_altas_2016_2024": r(100 * x[(x.alta.dt.year >= 2016) & (x.alta.dt.year <= 2024)].s_alta.nunique() / max(na_, 1), 1)}
    out["recambio_administrativo_mismo_domicilio"] = rec
    a25 = h[h.estado == "ALTA"]
    com_sig = len(set(a25.signatura) & set(u26.signatura))
    c25 = a25.alta.dt.year.value_counts()
    c26 = u26[u26.alta <= "2025-01-26"].alta.dt.year.value_counts()
    mun25 = a25.groupby("ine5").size()
    mun26 = u26.groupby("ine5").size()
    jm = pd.concat([mun25.rename("a25"), mun26.rename("a26")], axis=1).fillna(0)
    def cohorte(y0, y1):
        a, b = c25[(c25.index >= y0) & (c25.index <= y1)].sum(), c26[(c26.index >= y0) & (c26.index <= y1)].sum()
        return {"alta_2025-01": int(a), "con_misma_fecha_de_alta_en_2026-10": int(b), "ratio": r(b / a, 3) if a else None}
    out["tramo_2025-01_a_2026-10"] = {
        "alta_2025-01": int(len(a25)), "vigentes_2026-10": int(len(u26)), "variacion_neta_pct": r(100 * (len(u26) / len(a25) - 1), 1),
        "signaturas_en_comun": int(com_sig),
        "formato_signatura_2025": "VT-/BL (histórico y último periodo)", "formato_signatura_2026": "CV-VUT (corte diario)",
        "altas_2026_con_fecha_hasta_2025-01-26": int((u26.alta <= "2025-01-26").sum()),
        "altas_2026_con_fecha_posterior": int((u26.alta > "2025-01-26").sum()),
        "salida_minima_implicita_pct_del_stock_2025": r(100 * (1 - (u26.alta <= "2025-01-26").sum() / len(a25)), 1),
        "cohorte_alta_1993_1994": cohorte(1993, 1994), "cohorte_alta_2015_2019": cohorte(2015, 2019),
        "cohorte_alta_2020_2024": cohorte(2020, 2024),
        "municipios_con_caida": int((jm.a26 < jm.a25).sum()), "municipios_con_aumento": int((jm.a26 > jm.a25).sum()),
        "municipios_total": int(len(jm)),
        "variacion_neta_mediana_municipal_pct": r(100 * ((jm.a26 - jm.a25) / jm.a25.where(jm.a25 > 0)).median(), 1),
        "nota": ("no hay identificador común entre el histórico (2025-01) y el corte diario (2026-10): bajas y altas del tramo no se pueden fechar ni "
                 "inferir por signatura; solo se observa el stock neto y la salida mínima implícita por fecha de alta")}
    prim = h[ok].groupby("ine5").alta.min()
    ya = int((prim < "2015-01-01").sum())
    out["inicio_exposicion_municipal"] = {
        "municipios_con_registro": int(len(prim)), "con_primera_alta_antes_2015": ya,
        "con_primera_alta_2015_2019": int(((prim >= "2015-01-01") & (prim < "2020-01-01")).sum()),
        "con_primera_alta_2020_2025": int((prim >= "2020-01-01").sum()),
        "pct_con_exposicion_ya_en_2015-01": r(100 * ya / len(prim), 1)}
    return out, COH, ESC


def leer_bcn_zip(path: Path) -> pd.DataFrame:
    z = zipfile.ZipFile(path)
    raw = z.read(z.namelist()[0])
    txt = None
    for enc in ("utf-8-sig", "latin-1"):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    txt = txt.replace("\r", "")
    txt = re.sub(r"(LATITUD_Y)(?=\d)", r"\1\n", txt, count=1)   # cabecera pegada a la primera fila (p. ej. 2023T1)
    cab = txt.split("\n", 1)[0]
    sep = ";" if cab.count(";") > cab.count(",") else ","
    return pd.read_csv(io.StringIO(txt), sep=sep, dtype=str, engine="python", on_bad_lines="skip", index_col=False)


def tarea4_bcn(D: pd.DataFrame):
    b = D[D.variable == "bcn_hut_registro"].copy()
    b["barrio"] = b.desag.str.replace("barrio_bcn=", "", regex=False)
    tot = b[b.barrio == "Total"].set_index("periodo").valor
    nb = b[b.barrio != "Total"].groupby("periodo").agg(n_barrios_base=("barrio", "nunique"), suma_barrios_base=("valor", "sum"))
    filas = []
    for z in sorted(BCN_ZIPS.glob("*.zip")):
        mt = re.match(r"(\d{4})_(\d)T_", z.name)
        per = f"{mt.group(1)}T{mt.group(2)}"
        df = leer_bcn_zip(z)
        cols = {c.upper().strip(): c for c in df.columns}
        nbar = cols.get("BARRI") or cols.get("NOM_BARRI")
        cd = cols.get("DISTRICTE") or cols.get("NOM_DISTRICTE")
        exp = cols.get("N_EXPEDIENT")
        lon = any(c.startswith("LONGITUD") for c in cols)
        filas.append({"periodo": per, "fichero": z.name, "filas_fichero": int(len(df)),
                      "expedientes_distintos": int(df[exp].nunique()) if exp else int(len(df)),
                      "con_nombre_barrio": int(df[nbar].notna().sum()) if nbar else 0,
                      "barrios_distintos_nombre": int(df[nbar].nunique()) if nbar else 0,
                      "distritos_distintos": int(df[cd].nunique()) if cd else 0,
                      "tiene_codigo_barrio": "CODI_BARRI" in cols, "con_coordenadas": bool(lon),
                      "total_base": r(tot.get(per), 0) if per in tot.index else None})
    F = pd.DataFrame(filas).set_index("periodo").join(nb, how="left").reset_index()
    F["dif_filas_vs_total_base"] = F.filas_fichero - F.total_base
    F["barrio_en_zip_no_en_base"] = (F.barrios_distintos_nombre > 0) & F.n_barrios_base.isna()
    cuts = sorted(b.periodo.unique())
    cb = sorted(nb.index)
    esperados = {f"{y}T{q}" for y in range(2018, 2027) for q in range(1, 5)} - {"2018T1"}
    resumen = {
        "cortes_en_base": len(cuts), "primer_corte_base": cuts[0], "ultimo_corte_base": cuts[-1],
        "cortes_con_barrio_en_base": len(cb), "primer_corte_con_barrio_base": cb[0],
        "barrios_en_base_ultimo_corte": int(nb.n_barrios_base.iloc[-1]),
        "trimestres_sin_corte_hasta_2026T3": sorted(t for t in esperados - set(cuts) if t <= "2026T3"),
        "zips_en_disco": int(len(F)), "zips_con_nombre_de_barrio": int((F.barrios_distintos_nombre > 0).sum()),
        "zips_con_barrio_no_cargado_en_base": int(F.barrio_en_zip_no_en_base.sum()),
        "zips_con_coordenadas": int(F.con_coordenadas.sum()),
        "cortes_con_filas_distintas_del_total_base": F.loc[F.dif_filas_vs_total_base.abs() > 0, "periodo"].tolist(),
        "veredicto": ("Existe serie temporal real por barrio en la base solo desde 2023T1 (13 cortes hasta 2026T3; faltan 2024T1 y 2026T2); "
                      "los cortes 2018T2-2022T4 figuran en la base solo como total de ciudad. Los zip originales traen nombre de barrio, distrito y "
                      "coordenadas desde 2018T2 (ver zips_con_nombre_de_barrio), de modo que la serie por barrio 2018-2022 es recuperable y no está cargada. "
                      "El manifiesto de v9 describe otro recurso (registro vigente por año de expediente): no contradice la serie trimestral. "
                      "El código de barrio de Barcelona no es INE; el cruce con SERPAVI/IPVA requiere una correspondencia barrio-sección o distrito INE "
                      "(punto en polígono con las coordenadas) que no está en el repositorio.")}
    return F, resumen


# ---------------------------------------------------------------- 5. cobertura P5


def anual_expo(D: pd.DataFrame) -> dict:
    E = {}
    g = D[(D.variable == "vut_registro_gva_reconstruido") & (D.fecha_dato.str[5:7] == "12")].copy()
    g["año"] = g.fecha_dato.str[:4].astype(int)
    cv = sorted(c for c in territorios()["municipio"] if c[:2] in ("03", "12", "46"))
    rej = pd.MultiIndex.from_product([cv, range(2015, 2025)], names=["cod", "año"]).to_frame(index=False)
    g = rej.merge(g.rename(columns={"valor": "expo"})[["cod", "año", "expo"]], on=["cod", "año"], how="left")
    g["expo"] = g.expo.fillna(0.0)   # el registro cubre toda la Comunitat: ausencia = 0 viviendas
    E["GVA_reconstruido(stock dic; ausencia=0)"] = ("municipio", g[["cod", "año", "expo"]])
    s = D[(D.variable == "ine_vut_vivienda_turistica") & (D.nivel == "seccion")].copy()
    s["año"] = s.fecha_dato.str[:4].astype(int)
    sy = s.groupby(["cod", "año"]).valor.mean().reset_index().rename(columns={"valor": "expo"})
    E["INE_VUT(media anual)"] = ("seccion", sy)
    for niv, n in (("distrito", 7), ("municipio", 5)):
        s["u"] = s.cod.str[:n]
        x = s.groupby(["u", "fecha_dato"]).valor.sum().reset_index()
        x["año"] = x.fecha_dato.str[:4].astype(int)
        x = x.groupby(["u", "año"]).valor.mean().reset_index().rename(columns={"u": "cod", "valor": "expo"})
        E[f"INE_VUT(media anual, agregada a {niv})"] = (niv, x)
    i = D[D.variable == "idescat_hut_n"].copy()
    i["año"] = i.periodo.astype(int)
    E["IDESCAT_HUT_n(anual)"] = ("municipio", i.rename(columns={"valor": "expo"})[["cod", "año", "expo"]])
    b = D[(D.variable == "bcn_hut_registro") & (D.desag == "barrio_bcn=Total") & (D.fecha_dato.str[5:7] == "12")].copy()
    b["año"] = b.fecha_dato.str[:4].astype(int)
    E["BCN_HUT_ciudad(corte 4T)"] = ("municipio", b.rename(columns={"valor": "expo"})[["cod", "año", "expo"]])
    t = D[D.variable == "ine_tmov_receptor_turistas"].copy()
    t["año"] = t.fecha_dato.str[:4].astype(int)
    ty = t.groupby(["cod", "año"]).valor.agg(["sum", "size"]).reset_index()
    ty = ty[ty["size"] == 12].rename(columns={"sum": "expo"})[["cod", "año", "expo"]]
    E["INE_turistas_receptor(año completo; demanda, no stock VUT)"] = ("municipio", ty)
    return E


def tarea5_cobertura(D: pd.DataFrame, R: pd.DataFrame, ambito: tuple | None = None, etiqueta: str = "España") -> pd.DataFrame:
    E = anual_expo(D)
    if ambito:
        E = {k: (n, e[e.cod.str.startswith(ambito)]) for k, (n, e) in E.items()}
        R = R[R.cod.str.startswith(ambito)]
    O = {"SERPAVI_alquiler_m2_mediana": R[R.variable == "serpavi_alquiler_m2_mediana"],
         "INCASOL_renta_media": R[R.variable == "incasol_renta_media"],
         "IPVA_indice": R[R.variable == "ipva_indice"],
         "IPVA_tam_indice(Total)": R[(R.variable == "ipva_tam_indice") & (R.desag == "tamano=Total")]}
    filas = []
    for en, (niv_e, ex) in E.items():
        for on, o in O.items():
            oo = o[o.nivel == niv_e].drop_duplicates(["cod", "año"])[["cod", "año", "valor"]]
            if len(oo) == 0:
                continue
            j = ex.merge(oo, on=["cod", "año"], how="inner")
            row = {"ambito": etiqueta, "exposicion": en, "resultado": on, "nivel": niv_e, "unidades_exposicion": int(ex.cod.nunique()),
                   "unidades_resultado": int(oo.cod.nunique())}
            if len(j) == 0:
                filas.append({**row, "unidades_comunes": 0, "años_solapados": "", "n_años": 0, "unidad_años": 0})
                continue
            ys = sorted(j.año.unique())
            nyr = j.groupby("cod").año.nunique()
            fp = j[j.expo > 0].groupby("cod").año.min()
            jj = j.merge(fp.rename("fp"), left_on="cod", right_index=True, how="left")
            pre = jj[jj.año < jj.fp].groupby("cod").size().reindex(nyr.index).fillna(0)
            nunca = int((~nyr.index.isin(fp.index)).sum())
            var = j.groupby("cod").expo.nunique()
            pre19 = j[j.año <= 2019].groupby("cod").año.nunique().reindex(nyr.index).fillna(0)
            filas.append({**row, "unidades_comunes": int(len(nyr)), "años_solapados": f"{ys[0]}-{ys[-1]}", "n_años": len(ys),
                          "unidad_años": int(len(j)), "unidades_>=3_años": int((nyr >= 3).sum()), "unidades_>=5_años": int((nyr >= 5).sum()),
                          "unidades_con_variacion_expo": int((var > 1).sum()), "unidades_nunca_expuestas(control)": nunca,
                          "entrantes_con_>=1_año_previo": int((pre >= 1).sum()), "entrantes_con_>=3_años_previos": int((pre >= 3).sum()),
                          "unidades_con_>=3_años_<=2019": int((pre19 >= 3).sum())})
    res = pd.DataFrame(filas)
    if ambito:
        res = res[res.unidades_comunes > 0]
    return res


def cobertura_sin_fecha(D: pd.DataFrame, R: pd.DataFrame) -> pd.DataFrame:
    """Exposiciones sin serie fechada utilizable (corte único o sin clave INE): unidades, cortes y años con resultado."""
    b = D[(D.variable == "bcn_hut_registro") & (D.desag != "barrio_bcn=Total")]
    b4 = b[b.fecha_dato.str[5:7] == "12"]
    ys = sorted(b4.fecha_dato.str[:4].astype(int).unique())
    sp = R[R.variable == "serpavi_alquiler_m2_mediana"]
    ymax = int(sp.año.max())
    filas = [
        {"exposicion": "BCN_HUT_barrio(2023T1-2026T3)", "unidades": int(b.desag.nunique()), "cortes": int(b.periodo.nunique()),
         "años_con_corte_4T": ",".join(map(str, ys)), "años_solapados_con_resultado": ",".join(str(y) for y in ys if y <= ymax),
         "unidades_con_resultado_por_codigo_INE": 0,
         "nota": "código de barrio de Barcelona no es INE; sin correspondencia barrio-sección/distrito en el repositorio"},
        {"exposicion": "REATE_viviendas(corte 2026-10-15)", "unidades": int(D[D.variable == "reate_viviendas_uso_turistico"].cod.nunique()),
         "cortes": 1, "años_con_corte_4T": "", "años_solapados_con_resultado": "", "unidades_con_resultado_por_codigo_INE": 0,
         "nota": "corte único posterior a los resultados (SERPAVI hasta 2024): sin periodo previo"},
        {"exposicion": "InsideAirbnb_sección(2026-09)", "unidades": int(D[D.variable == "iab_n_anuncios"].cod.nunique()), "cortes": 1,
         "años_con_corte_4T": "", "años_solapados_con_resultado": "", "unidades_con_resultado_por_codigo_INE": 0,
         "nota": "corte único posterior a los resultados; no oficial"},
        {"exposicion": "GVA_registro_cortes(2025-01-26 y 2026-10-14)", "unidades": int(D[D.variable == "vut_registro_gva"].cod.nunique()), "cortes": 2,
         "años_con_corte_4T": "", "años_solapados_con_resultado": "2024 (solo aproximado: corte 2025-01)", "unidades_con_resultado_por_codigo_INE": 0,
         "nota": "tramo 2025-02 a 2026-10 sin fechar (sin identificador común)"}]
    return pd.DataFrame(filas)


# ---------------------------------------------------------------- principal


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    D = cargar()
    R = cargar_resultados()
    TER = territorios()
    F, Tp = tarea1_atipicos(D)
    F.to_csv(OUT / "atipicos_recuento.csv", index=False)
    Tp.to_csv(OUT / "atipicos_top30.csv", index=False)
    U = tarea1b_unidades(D, TER)
    U.to_csv(OUT / "unidades_rangos.csv", index=False)
    C = tarea2_coherencia(D)
    C["cortes"].to_csv(OUT / "coherencia_cortes.csv", index=False)
    C["totales"].to_csv(OUT / "coherencia_totales_periodo.csv", index=False)
    C["divergencias"].to_csv(OUT / "coherencia_divergencias.csv", index=False)
    C["series"].to_csv(OUT / "coherencia_series_temporales.csv", index=False)
    C["iab"].to_csv(OUT / "ine_vs_insideairbnb_resumen.csv", index=False)
    V = tarea3_vintages(D)
    V["tabla"].to_csv(OUT / "vintages_variables.csv", index=False)
    fech, COH, ESC = tarea4_fechado(D)
    COH.to_csv(OUT / "fechado_gva_composicion_stock.csv", index=False)
    ESC.to_csv(OUT / "fechado_gva_escenarios.csv", index=False)
    BF, bres = tarea4_bcn(D)
    BF.to_csv(OUT / "bcn_cortes_zip_vs_base.csv", index=False)
    COB = pd.concat([tarea5_cobertura(D, R),
                     tarea5_cobertura(D, R, ("03", "12", "46"), "Comunitat Valenciana"),
                     tarea5_cobertura(D, R, ("46250",), "València ciudad"),
                     tarea5_cobertura(D, R, ("08019",), "Barcelona ciudad"),
                     tarea5_cobertura(D, R, ("08", "17", "25", "43"), "Cataluña")], ignore_index=True)
    COB.to_csv(OUT / "cobertura_p5.csv", index=False)
    COBS = cobertura_sin_fecha(D, R)
    COBS.to_csv(OUT / "cobertura_p5_sin_serie_fechada.csv", index=False)

    def js(df):
        return json.loads(df.to_json(orient="records"))

    resultado = {
        "rama": "v15/auditoria/turismo",
        "pregunta": "¿Qué exposición a pisos turísticos está fechada, es coherente entre fuentes y tiene resultado (alquiler/precio) en el mismo territorio para P5? Atípicos, coherencia, revisiones, fechado y cobertura.",
        "capa": "C4",
        "datos": ["INE VUT experimental (sección/distrito, 2021-02 a 2026-05)", "GVA registro VUT (cortes y reconstrucción mensual 2015-01 a 2025-01)",
                  "IDESCAT HUT/apartamentos (anual)", "REATE Euskadi (corte 2026-10-15)", "Ajuntament de Barcelona HUT (cortes trimestrales)",
                  "Inside Airbnb 2026-09 (no oficial; solo resumen)", "Eurostat plataformas", "INE turismo con móviles", "SERPAVI, Incasòl, IPVA (resultados)"],
        "N": {"filas_turismo": int(len(D)), "variables": int(D.variable.nunique()),
              "series_ine_vut_seccion": int(D[(D.variable == "ine_vut_vivienda_turistica") & (D.nivel == "seccion")].cod.nunique())},
        "metodo": ("Auditoría descriptiva determinista (SEED=20261010) sobre data/base/hechos.parquet sin muestra reservada y los zip/CSV crudos solo para "
                   "vintages y fechado. z robusto = (x - mediana)/(1,4826 MAD) sobre cambios logarítmicos (lag estacional de 12 meses para INE VUT, "
                   "INE móviles y turistas); series con MAD <= 0,01 se separan (MAD casi nula). Coherencia por código INE municipal: razón de sumas, "
                   "razón mediana, Spearman y Pearson en logaritmos, correlación de niveles y de cambios por municipio. Escenarios de fechado: "
                   "desplazamientos de 6 y 12 meses en altas y bajas del registro GVA. Cobertura P5: unidades y años con exposición y resultado."),
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {
            "atipicos_recuento": js(F), "atipicos_top30": js(Tp), "unidades_rangos": js(U),
            "coherencia_cortes": js(C["cortes"]), "coherencia_series_temporales": js(C["series"]), "coherencia_divergencias": js(C["divergencias"]),
            "coherencia_totales_periodo": js(C["totales"]),
            "ine_vs_insideairbnb": js(C["iab"]), "consistencia_niveles_ine": C["niveles"], "coherencia_extras": C["extras"],
            "vintages_variables": js(V["tabla"]), "vintages_pares": V["pares"],
            "fechado_gva": fech, "fechado_gva_composicion_stock": js(COH), "fechado_gva_escenarios": js(ESC),
            "bcn_serie_barrio": bres, "bcn_cortes": js(BF),
            "cobertura_p5": js(COB), "cobertura_p5_sin_serie_fechada": js(COBS),
        },
        "fuera_muestra": None,
        "notas": ["Auditoría C4: sin efectos ni regresiones. Muestra reservada de V6 excluida con NOT coalesce(muestra_sellada_v6,false).",
                  "Inside Airbnb y registro de Catalunya (Socrata, «Ver términos de uso»): solo estadísticos resumen; sin series por unidad.",
                  "Además de data/base y data/raw, el script lee los zip originales de Barcelona en data/manual/v11/bcn_hut_trimestral solo para recontar filas por barrio (lectura).",
                  "Umbrales fijados aquí: |z|>5, MAD_MIN=0,01, MIN_DIFF=6, salto grande en MAD casi nula = 5 unidades y 50 %."],
    }

    def default(o):
        if isinstance(o, np.floating):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.bool_):
            return bool(o)
        return str(o)

    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=default), encoding="utf-8")
    print("OK", OUT)


if __name__ == "__main__":
    main()
