"""V15 fase 1.2 · Auditoría de datos, grupo PRECIOS DE COMPRA (capa C4, descriptivo, sin efectos estimados).

Fuentes: MIVAU valor tasado (nacional, CCAA, provincia, municipios), INE IPV (general, nueva, usada), BdE p_bde,
Registradores datos abiertos (precio m2 con ventana de 4 trimestres), Notariado (precio m2 nacional, semestral),
Anuario ERI (solo revisiones) e INE ETDP (solo volumen, cuota de vivienda nueva).
Todos los cruces territoriales son por código INE (data/base/territorios.parquet). Determinista (SEED=20261010).
Salida: output/v15/auditoria/precios_compra/ (CSV resumen, resultado.json). Sin series por periodo de Notariado,
Registradores ni ERI: solo estadísticos resumen. Uso: python3 src/v15/auditoria/precios_compra.py
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
RAIZ = Path(__file__).resolve().parents[3]
RAW = RAIZ / "data" / "raw"
PDF = RAW / "pdf"
OUT = RAIZ / "output" / "v15" / "auditoria" / "precios_compra"
UMBRAL_Z = 5.0
UMBRAL_PP = 5.0
MIN_PP_SIGNO = 1.0
MIN_TRIM_DIV = 8
MIN_OBS = 12

# ---------------------------------------------------------------- utilidades


def qidx(p: str) -> int:
    """'2015T3' -> índice trimestral entero."""
    m = re.match(r"^(\d{4})T([1-4])$", str(p))
    return int(m.group(1)) * 4 + int(m.group(2)) - 1


def qlab(t: int) -> str:
    return f"{t // 4}T{t % 4 + 1}"


STOP = {"de", "del", "la", "las", "el", "los", "a", "y", "l", "illes", "comunidad", "comunitat", "region", "principado",
        "foral", "c", "com", "regio"}


def clave(nombre: str) -> frozenset:
    s = unicodedata.normalize("NFKD", str(nombre)).encode("ascii", "ignore").decode().lower()
    s = s.split("/")[0]
    return frozenset(w for w in re.findall(r"[a-z0-9]+", s) if w not in STOP)


def mapa_codigos() -> dict[str, dict]:
    t = pd.read_parquet(RAIZ / "data" / "base" / "territorios.parquet")
    out: dict[str, dict] = {}
    for niv in ("ccaa", "provincia"):
        d = {}
        for cod, nom in t.loc[t.nivel == niv, ["territorio_codigo", "nombre"]].itertuples(index=False):
            d[clave(nom)] = cod
        out[niv] = d
    out["prov_a_ccaa"] = dict(t.loc[t.nivel == "provincia", ["territorio_codigo", "cod_ccaa"]].itertuples(index=False))
    return out


MAPA = mapa_codigos()
SIN_MAPEAR: dict[str, set] = {}


def cod(nivel: str, nombre: str, fuente: str) -> str | None:
    if nivel == "nacional":
        return "00"
    c = MAPA[nivel].get(clave(nombre))
    if c is None:
        SIN_MAPEAR.setdefault(fuente, set()).add(f"{nivel}:{nombre}")
    return c


def yoy(s: pd.Series, lag: int = 4) -> pd.Series:
    """Tasa interanual en % sobre rejilla trimestral completa."""
    s = s.dropna().astype(float)
    if len(s) == 0:
        return s
    s = s.reindex(range(int(s.index.min()), int(s.index.max()) + 1))
    return (s / s.shift(lag) - 1.0) * 100.0


def yoy_v4(s: pd.Series) -> pd.Series:
    """Tasa interanual de la media móvil de 4 trimestres (igualar la ventana de Registradores)."""
    s = s.dropna().astype(float)
    if len(s) == 0:
        return s
    s = s.reindex(range(int(s.index.min()), int(s.index.max()) + 1))
    return yoy(s.rolling(4, min_periods=4).mean())


def semestral(s: pd.Series) -> pd.Series:
    """Media de dos trimestres, asignada a los trimestres 2 y 4 (para comparar con Notariado semestral)."""
    s = s.dropna().astype(float)
    s = s.reindex(range(int(s.index.min()), int(s.index.max()) + 1))
    m = (s + s.shift(1)) / 2.0
    keep = [t for t in m.index if t % 4 in (1, 3)]
    return m.loc[keep].dropna()


def zrob(x: pd.Series) -> pd.Series | None:
    x = x.dropna()
    if len(x) < MIN_OBS:
        return None
    med = float(np.median(x))
    mad = float(np.median(np.abs(x - med)))
    if mad == 0:
        return None
    return (x - med) / (1.4826 * mad)


def corr(a: pd.Series, b: pd.Series) -> tuple[float, float, int]:
    j = pd.concat([a, b], axis=1, join="inner").dropna()
    if len(j) < MIN_OBS or j.iloc[:, 0].std() == 0 or j.iloc[:, 1].std() == 0:
        return (np.nan, np.nan, len(j))
    return (float(j.iloc[:, 0].corr(j.iloc[:, 1])), float((j.iloc[:, 0] - j.iloc[:, 1]).mean()), len(j))


def corr_sp(a, b) -> float:
    j = pd.concat([pd.Series(a), pd.Series(b)], axis=1).dropna()
    if len(j) < 5:
        return np.nan
    return float(j.rank().iloc[:, 0].corr(j.rank().iloc[:, 1]))


def divergencias(x: pd.Series, y: pd.Series, paso: int = 1) -> list[dict]:
    """Rachas de >= 2 años en que las tasas tienen signo opuesto (ambas > 1 pp en valor absoluto) o difieren > 5 pp."""
    j = pd.concat([x, y], axis=1, join="inner").dropna()
    if len(j) == 0:
        return []
    a, b = j.iloc[:, 0], j.iloc[:, 1]
    opuesto = (np.sign(a) != np.sign(b)) & (a.abs() > MIN_PP_SIGNO) & (b.abs() > MIN_PP_SIGNO)
    grande = (a - b).abs() > UMBRAL_PP
    flag = opuesto | grande
    res, ini, prev = [], None, None
    for t, f in flag.items():
        if f and ini is not None and t - prev <= paso:
            prev = t
        elif f:
            if ini is not None:
                res.append((ini, prev))
            ini, prev = t, t
        else:
            if ini is not None:
                res.append((ini, prev))
            ini = None
    if ini is not None:
        res.append((ini, prev))
    out = []
    for i0, i1 in res:
        dur = i1 - i0 + paso
        if dur >= MIN_TRIM_DIV:
            seg = j.loc[i0:i1]
            tipo = "signo_opuesto" if bool(opuesto.loc[i0:i1].mean() > 0.5) else "diferencia_gt5pp"
            out.append({"inicio": qlab(i0), "fin": qlab(i1), "trimestres": int(dur), "tipo": tipo,
                        "dif_media_pp": round(float((seg.iloc[:, 0] - seg.iloc[:, 1]).mean()), 2)})
    return out


def media_anual(s: pd.Series, año: int, min_n: int) -> float:
    v = s.loc[[t for t in s.index if t // 4 == año]].dropna()
    return float(v.mean()) if len(v) >= min_n else np.nan


# ---------------------------------------------------------------- carga de fuentes


def cargar() -> dict[str, dict[tuple[str, str], pd.Series]]:
    """fuente -> {(nivel, codigo): Serie(niveles) indexada por índice trimestral}."""
    D: dict[str, dict[tuple[str, str], pd.Series]] = {}

    def add(f: str, niv: str, c: str | None, t: int, v: float) -> None:
        if c is not None and pd.notna(v):
            D.setdefault(f, {}).setdefault((niv, c), {})[t] = v

    # MIVAU valor tasado
    m = pd.read_csv(RAW / "mivau_valor_tasado_nacional_ccaa_prov.csv")
    for niv_raw, terr, per, v in m[["nivel", "territorio", "periodo", "valor"]].itertuples(index=False):
        t = qidx(per)
        if niv_raw == "nacional":
            add("p_tasado", "nacional", "00", t, v)
        elif niv_raw in ("ccaa", "ciudad_autonoma"):
            add("p_tasado", "ccaa", cod("ccaa", terr, "p_tasado") if terr != "Ceuta y Melilla" else None, t, v)
            if niv_raw == "ciudad_autonoma":
                add("p_tasado", "provincia", cod("provincia", terr, "p_tasado"), t, v)
        elif niv_raw == "provincia":
            add("p_tasado", "provincia", cod("provincia", terr, "p_tasado"), t, v)
    # BdE
    b = pd.read_csv(RAW / "bde_precio_vivienda_libre.csv").dropna(subset=["valor"])
    for ser, per, v in b[["serie", "periodo", "valor"]].itertuples(index=False):
        y, mm = int(per[:4]), int(per[5:7])
        t = y * 4 + (mm - 1) // 3
        f = {"DHIVTNOAPLPMMUVT_RLI.T": "p_bde"}.get(ser)
        if f is None:
            f = "p_bde_nueva" if "VVN" in ser else ("p_bde_usada" if "VVU" in ser else None)
        if f:
            add(f, "nacional", "00", t, v)
    # INE IPV (80270 base vigente) y 25171
    for arch, pref in (("ine_ipv_80270.csv", "ipv"), ("ine_ipv_25171.csv", "ipv15")):
        i = pd.read_csv(RAW / arch)
        for nom, per, v in i[["nombre", "periodo", "valor"]].itertuples(index=False):
            mt = re.match(r"^(.*)\. (General|Vivienda nueva|Vivienda segunda mano)\. Índice\.$", nom)
            if not mt or "T" not in per:
                continue
            terr, tipo = mt.group(1), mt.group(2)
            f = pref + {"General": "", "Vivienda nueva": "_nueva", "Vivienda segunda mano": "_usada"}[tipo]
            if terr == "Nacional" or terr.upper().startswith("TOTAL"):
                add(f, "nacional", "00", qidx(per), v)
            else:
                add(f, "ccaa", cod("ccaa", terr, f), qidx(per), v)
    # Registradores datos abiertos
    r = pd.read_csv(PDF / "registradores_opendata_compraventas.csv")
    for ser, f in (("compraventas_viv_pm2_4T_movil", "reg_pm2"), ("compraventas_viv_imp_4T_movil", "reg_imp")):
        rr = r[r.serie == ser]
        for niv, terr, per, v in rr[["nivel", "territorio", "periodo", "valor"]].itertuples(index=False):
            if niv == "nacional":
                add(f, "nacional", "00", qidx(per), v)
            else:
                add(f, niv, cod(niv, terr, f), qidx(per), v)
    # Notariado semestral nacional (Total general)
    n = pd.read_csv(PDF / "notariado_cgn_extranjeros_semestral.csv")
    n = n[(n.serie == "precio_m2") & (n.categoria == "Total general")]
    for per, v in n[["periodo", "valor"]].itertuples(index=False):
        y, s = int(per[:4]), int(per[5])
        add("not_pm2", "nacional", "00", y * 4 + (1 if s == 1 else 3), v)
    return {f: {k: pd.Series(d).sort_index() for k, d in dd.items()} for f, dd in D.items()}


def cargar_etdp() -> dict[tuple[str, str], pd.Series]:
    """Cuota de vivienda nueva: nueva / (nueva + segunda mano), compraventas INE ETDP, trimestral."""
    e = pd.read_csv(RAW / "ine_etdp_compraventas.csv")
    e = e[e.nombre.str.contains("Compraventa. Número", regex=False)]
    ext = e.nombre.str.extract(r"^(.*?)\. Vivienda (nueva|segunda mano)\. Compraventa")
    e = e.assign(terr=ext[0], tipo=ext[1]).dropna(subset=["tipo"])
    e = e[e.periodo.str.contains("M")]
    e["t"] = e.periodo.str[:4].astype(int) * 4 + (e.periodo.str[5:7].astype(int) - 1) // 3
    def clasif(x: str) -> tuple[str, str] | None:
        if x.startswith("Total Nacional"):
            return ("nacional", "00")
        c = MAPA["provincia"].get(clave(x))
        if c is not None:
            return ("provincia", c)
        c = MAPA["ccaa"].get(clave(x))
        return ("ccaa_directo", c) if c is not None else None

    e["cl"] = [clasif(x) for x in e.terr]
    e = e.dropna(subset=["cl"])
    e["niv"] = [c[0] for c in e.cl]
    e["c"] = [c[1] for c in e.cl]
    e = e.drop_duplicates(["niv", "c", "tipo", "periodo"])  # CCAA uniprovinciales aparecen como CCAA y como provincia
    q = e.groupby(["niv", "c", "tipo", "t"]).valor.agg(["sum", "size"]).reset_index()
    q = q[q["size"] == 3].rename(columns={"sum": "valor"})

    def cuota_de(g: pd.DataFrame) -> pd.Series:
        w = g.pivot_table(index="t", columns="tipo", values="valor", aggfunc="sum").dropna()
        return (w["nueva"] / (w["nueva"] + w["segunda mano"]) * 100.0).sort_index()

    out = {}
    for (niv, c), g in q.groupby(["niv", "c"]):
        if niv == "nacional":
            out[("nacional", "00")] = cuota_de(g)
        elif niv == "provincia":
            out[("provincia", c)] = cuota_de(g)
        else:
            out[("ccaa", c)] = cuota_de(g)
    # CCAA sin fila directa: suma de provincias
    pv = q[q.niv == "provincia"].assign(ccaa=lambda d: d.c.map(MAPA["prov_a_ccaa"]))
    for c, g in pv.groupby("ccaa"):
        if ("ccaa", c) not in out:
            out[("ccaa", c)] = cuota_de(g.groupby(["tipo", "t"]).valor.sum().reset_index())
    return out


# ---------------------------------------------------------------- tareas


def tarea1_atipicos(D) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    filas, top = [], []
    for f in ("p_tasado", "p_bde", "p_bde_nueva", "p_bde_usada", "ipv", "ipv_nueva", "ipv_usada", "reg_pm2", "reg_imp",
              "not_pm2"):
        for (niv, c), s in D[f].items():
            y = yoy(s)
            z = zrob(y)
            if z is None:
                filas.append({"fuente": f, "nivel": niv, "cod_ine": c, "n": int(y.notna().sum()), "n_atip": 0,
                              "z_valido": False})
                continue
            big = z[z.abs() > UMBRAL_Z]
            # secundario: variación trimestral (solo fuentes trimestrales completas)
            nq = 0
            if f != "not_pm2":
                zq = zrob(np.log(s).diff().dropna())
                nq = int((zq.abs() > UMBRAL_Z).sum()) if zq is not None else 0
            filas.append({"fuente": f, "nivel": niv, "cod_ine": c, "n": int(len(z)), "n_atip": int(len(big)),
                          "n_atip_qoq": nq, "z_valido": True})
            for t, zz in big.items():
                top.append({"fuente": f, "nivel": niv, "cod_ine": c, "periodo": qlab(int(t)), "z_robusto": round(float(zz), 2),
                            "tasa_pp": round(float(y.loc[t]), 2)})
    # municipios (sin código INE disponible en el raw: se identifica la serie)
    mu = pd.read_csv(RAW / "mivau_valor_tasado_municipios.csv")
    for serie, g in mu.groupby("serie"):
        s = pd.Series({qidx(p): v for p, v in zip(g.periodo, g.valor, strict=True)}).sort_index()
        y = yoy(s)
        z = zrob(y)
        if z is None:
            continue
        big = z[z.abs() > UMBRAL_Z]
        filas.append({"fuente": "p_tasado_municipal", "nivel": "municipio", "cod_ine": "sin_codigo:" + serie, "n": int(len(z)),
                      "n_atip": int(len(big)), "n_atip_qoq": 0, "z_valido": True})
        for t, zz in big.items():
            top.append({"fuente": "p_tasado_municipal", "nivel": "municipio", "cod_ine": "sin_codigo:" + serie,
                        "periodo": qlab(int(t)), "z_robusto": round(float(zz), 2), "tasa_pp": round(float(y.loc[t]), 2)})
    F = pd.DataFrame(filas)
    rec = (F.groupby(["fuente", "nivel"]).agg(series=("cod_ine", "size"), series_z_validas=("z_valido", "sum"),
                                              obs_tasa=("n", "sum"), atipicos=("n_atip", "sum"),
                                              atipicos_qoq=("n_atip_qoq", "sum"),
                                              series_con_atipicos=("n_atip", lambda x: int((x > 0).sum())))
           .reset_index())
    rec["pct_atipicos"] = (100 * rec.atipicos / rec.obs_tasa).round(2)
    T = pd.DataFrame(top)
    if len(T):
        T = T.reindex(T.z_robusto.abs().sort_values(ascending=False, kind="mergesort").index).head(20).reset_index(drop=True)
        # Notariado y Registradores: solo z (no se publica la tasa por periodo)
        T.loc[T.fuente.isin(["not_pm2", "reg_pm2", "reg_imp"]), "tasa_pp"] = np.nan
    # unidades dudosas: rangos
    rangos = {}
    for f in ("p_tasado", "p_bde", "reg_pm2", "not_pm2"):
        v = np.concatenate([s.values for s in D[f].values()])
        rangos[f] = {"min": round(float(v.min()), 1), "max": round(float(v.max()), 1),
                     "fuera_100_20000": int(((v < 100) | (v > 20000)).sum())}
    v = np.concatenate([s.values for s in D["reg_imp"].values()])
    rangos["reg_imp"] = {"min": round(float(v.min()), 0), "max": round(float(v.max()), 0),
                         "fuera_10000_2000000": int(((v < 10000) | (v > 2_000_000)).sum())}
    return rec, T, rangos


def tarea2_coherencia(D):
    pares = [("p_tasado", "ipv", "directa"), ("p_tasado", "reg_pm2", "ventana4"), ("ipv", "reg_pm2", "ventana4"),
             ("p_tasado", "ipv", "ventana4"), ("p_tasado", "p_bde", "directa"),
             ("p_tasado", "not_pm2", "semestral"), ("ipv", "not_pm2", "semestral"), ("reg_pm2", "not_pm2", "semestral")]
    terr_rows, div_rows = [], []

    def tasa(f, s, var):
        if var == "directa":
            return yoy(s)
        if var == "ventana4":
            return yoy_v4(s)
        return yoy(s) if f == "not_pm2" else yoy(semestral(s))

    for a, b, var in pares:
        for k in sorted(set(D[a]) & set(D[b])):
            x, y = tasa(a, D[a][k], var), tasa(b, D[b][k], var)
            r, d, n = corr(x, y)
            dv = divergencias(x, y, 2 if var == "semestral" else 1)
            terr_rows.append({"nivel": k[0], "cod_ine": k[1], "A": a, "B": b, "variante": var, "n_obs": n,
                              "corr_tasas": round(r, 3) if pd.notna(r) else np.nan,
                              "dif_media_pp_AmenosB": round(d, 2) if pd.notna(d) else np.nan,
                              "n_rachas_divergencia": len(dv), "max_trim_divergencia": max([q["trimestres"] for q in dv], default=0)})
            for q in dv:
                div_rows.append({"nivel": k[0], "cod_ine": k[1], "A": a, "B": b, "variante": var, **q})
    TR = pd.DataFrame(terr_rows)
    DV = pd.DataFrame(div_rows)
    res = (TR.groupby(["nivel", "A", "B", "variante"])
           .agg(n_territorios=("cod_ine", "size"), corr_mediana=("corr_tasas", "median"), corr_p10=("corr_tasas", lambda x: x.quantile(.1)),
                corr_p90=("corr_tasas", lambda x: x.quantile(.9)), dif_media_pp_mediana=("dif_media_pp_AmenosB", "median"),
                dif_media_pp_abs_mediana=("dif_media_pp_AmenosB", lambda x: x.abs().median()),
                terr_con_divergencia=("n_rachas_divergencia", lambda x: int((x > 0).sum())))
           .reset_index())
    res["pct_terr_con_divergencia"] = (100 * res.terr_con_divergencia / res.n_territorios).round(1)
    for c in ("corr_mediana", "corr_p10", "corr_p90", "dif_media_pp_mediana", "dif_media_pp_abs_mediana"):
        res[c] = res[c].round(3)
    return res, TR, DV


def acumulado(D):
    filas = []
    for f in ("p_tasado", "p_bde", "ipv", "ipv_nueva", "ipv_usada", "reg_pm2", "not_pm2"):
        for (niv, c), s in D[f].items():
            mn = 2 if f == "not_pm2" else 3
            a15, a25 = media_anual(s, 2015, mn), media_anual(s, 2025, mn)
            if pd.notna(a15) and pd.notna(a25):
                filas.append({"fuente": f, "nivel": niv, "cod_ine": c, "acum_2015_2025_pct": round((a25 / a15 - 1) * 100, 1)})
    A = pd.DataFrame(filas)
    # Registradores y Notariado: solo distribución por nivel (no se publica la cifra por territorio)
    prot = A.fuente.isin(["reg_pm2", "not_pm2"])
    resumen = (A.groupby(["fuente", "nivel"]).acum_2015_2025_pct
               .agg(n="size", media="mean", mediana="median", p10=lambda x: x.quantile(.1), p90=lambda x: x.quantile(.9),
                    minimo="min", maximo="max").round(1).reset_index())
    return A[~prot].reset_index(drop=True), resumen


def tarea_bde(D, base_hechos) -> dict:
    a, b = D["p_tasado"][("nacional", "00")], D["p_bde"][("nacional", "00")]
    j = pd.concat([a, b], axis=1, join="inner").dropna()
    j.columns = ["tasado", "bde"]
    d = (j.tasado - j.bde).abs()
    r, dm, n = corr(yoy(a), yoy(b))
    out = {"n_trimestres_comunes": int(len(j)), "primer": qlab(int(j.index.min())), "ultimo": qlab(int(j.index.max())),
           "corr_niveles": round(float(j.tasado.corr(j.bde)), 6), "dif_abs_max_eur_m2": round(float(d.max()), 3),
           "dif_abs_media_eur_m2": round(float(d.mean()), 4), "n_trimestres_distintos": int((d > 0.05).sum()),
           "corr_tasas_interanuales": round(r, 6), "dif_media_tasas_pp": round(dm, 4),
           "misma_serie": bool((d <= 0.05).all()),
           "comparacion_hechos_vs_raw_tasado_nacional": base_hechos}
    for k in ("p_bde_nueva", "p_bde_usada"):
        out[f"{k}_n"] = int(len(D[k][("nacional", "00")]))
    return out


def hechos_vs_raw(D) -> dict:
    con = duckdb.connect()
    h = RAIZ / "data" / "base" / "hechos.parquet"
    df = con.sql(f"select nivel,territorio_codigo c,periodo,valor from '{h}' where variable='p_tasado' and nivel in ('nacional','ccaa')").df()
    n_dif, n = 0, 0
    for (niv, c), g in df.groupby(["nivel", "c"]):
        s = D["p_tasado"].get((niv, c))
        if s is None:
            continue
        for p, v in zip(g.periodo, g.valor, strict=True):
            n += 1
            if qidx(p) not in s.index or abs(s.loc[qidx(p)] - v) > 1e-6:
                n_dif += 1
    ed = con.sql(f"""select variable, count(distinct edicion) ed, count(distinct fecha_dato) fd from '{h}'
        where variable in ('p_tasado','p_bde','ipv','ipv_nueva','ipv_usada','registr_pm2_4tm','notariado_pm2_sem','compraventas','ipv15')
        group by 1 order by 1""").df()
    return {"obs_comparadas": n, "obs_distintas": n_dif, "ediciones_por_variable_hechos": {r.variable: [int(r.ed), int(r.fd)] for r in ed.itertuples()}}


def tarea3_composicion(D, E):
    def reb(s):
        base = media_anual(s, 2015, 2)
        return s / base * 100.0

    ipv = D["ipv"][("nacional", "00")]
    filas = []
    fuentes = {"p_tasado": "ventana_trim", "reg_pm2": "ventana_trim", "not_pm2": "semestral"}
    for f in fuentes:
        s = D[f][("nacional", "00")]
        mn = 2 if f == "not_pm2" else 3
        g15, g25 = media_anual(reb(s), 2015, mn), media_anual(reb(s), 2025, mn)
        i25 = media_anual(reb(ipv), 2025, 3)
        # brecha logarítmica 2025 (2015=100 en ambos)
        brecha = np.log(g25 / i25) * 100 if pd.notna(g25) else np.nan
        filas.append({"fuente": f, "nivel": "nacional", "cod_ine": "00", "acum_precio_medio_pct": round((g25 / g15 - 1) * 100, 1),
                      "acum_ipv_pct": round((i25 / 100 - 1) * 100, 1), "brecha_log_2025_pp": round(float(brecha), 1)})
    # relación con la cuota de vivienda nueva (ETDP), tasas y cambios a 4 trimestres, 2015T1-2025T4
    cuota = E[("nacional", "00")]
    rel = []
    for f in ("p_tasado", "reg_pm2"):
        s = D[f][("nacional", "00")]
        dif = (yoy_v4(s) - yoy_v4(ipv))
        dc = cuota.rolling(4, min_periods=4).mean().diff(4)
        j = pd.concat([dif, dc], axis=1).dropna()
        j = j.loc[qidx("2015T1"):qidx("2025T4")]
        lvl = pd.concat([np.log(reb(s)) - np.log(reb(ipv)), cuota], axis=1).dropna().loc[qidx("2015T1"):qidx("2025T4")]
        rel.append({"fuente": f, "n_dif": int(len(j)), "corr_dif_tasas_vs_cambio_cuota_nueva_4t": round(float(j.iloc[:, 0].corr(j.iloc[:, 1])), 3),
                    "corr_brecha_nivel_vs_cuota_nueva": round(float(lvl.iloc[:, 0].corr(lvl.iloc[:, 1])), 3),
                    "nota_nivel": "tendencial, no inferencial"})
    # segmentos: BdE nueva/usada frente a IPV nueva/usada (2015-2025)
    seg = []
    for fb, fi in (("p_bde_nueva", "ipv_nueva"), ("p_bde_usada", "ipv_usada")):
        s, i = D[fb][("nacional", "00")], D[fi][("nacional", "00")]
        a15, a25 = media_anual(s, 2015, 3), media_anual(s, 2025, 3)
        i15, i25 = media_anual(i, 2015, 3), media_anual(i, 2025, 3)
        seg.append({"segmento": fb, "acum_bde_pct": round((a25 / a15 - 1) * 100, 1), "acum_ipv_pct": round((i25 / i15 - 1) * 100, 1)})
    # IPV nueva vs usada, y precio BdE nueva/usada
    pn, pu = D["p_bde_nueva"][("nacional", "00")], D["p_bde_usada"][("nacional", "00")]
    ratio = (pn / pu).dropna()
    ext = {"ratio_precio_nueva_usada_bde_2015": round(media_anual(ratio, 2015, 3), 3),
           "ratio_precio_nueva_usada_bde_2025": round(media_anual(ratio, 2025, 3), 3),
           "cuota_nueva_etdp_2015_pct": round(media_anual(cuota, 2015, 3), 1), "cuota_nueva_etdp_2025_pct": round(media_anual(cuota, 2025, 3), 1)}
    # CCAA: brecha 2015->2025 frente al IPV general y cambio de cuota nueva (Spearman)
    cc = []
    for f in ("p_tasado", "reg_pm2"):
        brs, dcs = [], []
        for k in sorted(set(D[f]) & set(D["ipv"]) & set(E)):
            if k[0] != "ccaa":
                continue
            s, i = D[f][k], D["ipv"][k]
            g = (media_anual(s, 2025, 3) / media_anual(s, 2015, 3)) / (media_anual(i, 2025, 3) / media_anual(i, 2015, 3))
            dcu = media_anual(E[k], 2025, 3) - media_anual(E[k], 2015, 3)
            if pd.notna(g) and pd.notna(dcu):
                brs.append(np.log(g) * 100)
                dcs.append(dcu)
        cc.append({"fuente": f, "n_ccaa": len(brs), "brecha_log_media_pp": round(float(np.mean(brs)), 1),
                   "brecha_log_sd_pp": round(float(np.std(brs, ddof=1)), 1), "spearman_brecha_vs_cambio_cuota": round(corr_sp(brs, dcs), 3)})
    return pd.DataFrame(filas), pd.DataFrame(rel), pd.DataFrame(seg), ext, pd.DataFrame(cc)


def tarea4_revisiones(D) -> dict:
    out = {}
    # (a) ERI Anuario: tasa interanual publicada en la edición t frente a la implícita en niveles de las ediciones t y t-1
    er = pd.read_csv(PDF / "registradores_eri_anuario.csv")
    def tabla(serie: str) -> dict:
        d = {}
        for n, t, e, v in er.loc[er.serie == serie, ["nivel", "territorio", "edicion", "valor"]].itertuples(index=False):
            if n in ("ccaa", "provincia"):
                c = cod(n, t, "eri")
                if c is not None and (n, c, e) not in d:
                    d[(n, c, e)] = v
        return d

    niv, var = tabla("precio_m2_viv_general"), tabla("precio_m2_viv_general_var_anual")
    difs = []
    for (n, c, e), v in var.items():
        if (n, c, e - 1) in niv and (n, c, e) in niv:
            difs.append(abs(v - (niv[(n, c, e)] / niv[(n, c, e - 1)] - 1) * 100))
    d = np.array(difs, dtype=float)
    out["eri_revision_tasa_implicita_vs_publicada"] = {"n_pares": int(len(d)), "media_abs_pp": round(float(d.mean()), 3) if len(d) else None,
                                                       "max_abs_pp": round(float(d.max()), 3) if len(d) else None,
                                                       "pct_pares_gt1pp": round(float((d > 1).mean() * 100), 1) if len(d) else None}
    # (b) Registradores datos abiertos (T4 de la ventana) frente a ERI, año natural, mismo concepto
    ro = pd.read_csv(PDF / "registradores_opendata_anual.csv")
    ro = ro[(ro.serie == "compraventas_viv_pm2") & (ro.nivel == "ccaa")]
    rel = []
    for terr, per, v in ro[["territorio", "periodo", "valor"]].itertuples(index=False):
        c = cod("ccaa", terr, "reg_od_anual")
        ve = niv.get(("ccaa", c, int(per)))
        if ve is not None:
            rel.append(abs(v / ve - 1) * 100)
    rel = np.array(rel, dtype=float)
    out["opendata_vs_eri_precio_m2_ccaa"] = {"n_pares": int(len(rel)), "dif_rel_media_pct": round(float(rel.mean()), 2) if len(rel) else None,
                                             "dif_rel_max_pct": round(float(rel.max()), 2) if len(rel) else None}
    # (c) manifiestos: descargas por archivo
    man = pd.concat([pd.read_csv(p) for p in sorted(RAW.glob("_manifest*.csv")) if "archivo" in pd.read_csv(p, nrows=0).columns])
    pr = man[man.archivo.str.contains("mivau_valor_tasado|bde_precio|ine_ipv_|ine_etdp", regex=True)]
    out["manifiestos_descargas_por_archivo"] = {a: int(n) for a, n in pr.groupby("archivo").size().items()}
    out["revision_media_abs_tasa_vintages_misma_serie"] = None
    out["nota"] = ("Una sola descarga por serie de precios (manifiestos y columna edicion de hechos): no hay vintages "
                   "comparables de MIVAU, IPV, BdE, Notariado ni Registradores abiertos. Solo el Anuario ERI tiene 3 ediciones "
                   "(2023-2025) con un único año cada una, y se compara su tasa publicada con la implícita en niveles.")
    return out


def tarea5_rupturas(D) -> tuple[dict, pd.DataFrame]:
    out = {}
    # (a) IPV: 80270 frente a 25171 (cambio de base), tasa interanual
    rows = []
    for f, f15 in (("ipv", "ipv15"), ("ipv_nueva", "ipv15_nueva"), ("ipv_usada", "ipv15_usada")):
        cs, dd, cv = [], [], []
        for k in sorted(set(D[f]) & set(D[f15])):
            a, b = D[f][k], D[f15][k]
            r, d, _ = corr(yoy(a), yoy(b))
            j = pd.concat([a, b], axis=1, join="inner").dropna()
            cs.append(r)
            dd.append(abs(((yoy(a) - yoy(b)).dropna()).abs().max()) if len(j) else np.nan)
            cv.append(float((j.iloc[:, 0] / j.iloc[:, 1]).std() / (j.iloc[:, 0] / j.iloc[:, 1]).mean()))
        rows.append({"serie": f, "n_territorios": len(cs), "corr_tasas_mediana": round(float(np.nanmedian(cs)), 4) if cs else None,
                     "dif_max_tasa_pp_mediana": round(float(np.nanmedian(dd)), 3) if dd else None,
                     "cv_cociente_niveles_mediana": round(float(np.nanmedian(cv)), 4) if cv else None})
    out["ipv_80270_vs_25171"] = rows
    # IPV: tasa publicada frente a calculada (redondeo/unidad)
    i = pd.read_csv(RAW / "ine_ipv_80270.csv")
    nac = i[i.nombre.isin(["Nacional. General. Índice.", "Nacional. General. Variación anual."])]
    p = nac.pivot_table(index="periodo", columns="nombre", values="valor")
    p.index = [qidx(x) for x in p.index]
    calc = yoy(p["Nacional. General. Índice."])
    dif = (calc - p["Nacional. General. Variación anual."]).abs().dropna()
    out["ipv_tasa_publicada_vs_calculada_nacional"] = {"n": int(len(dif)), "dif_abs_max_pp": round(float(dif.max()), 3), "dif_abs_media_pp": round(float(dif.mean()), 4)}
    # (b) Valor tasado municipal: cobertura y efecto composición
    mu = pd.read_csv(RAW / "mivau_valor_tasado_municipios.csv")
    mu["t"] = [qidx(p) for p in mu.periodo]
    cov = mu.groupby("t").serie.nunique()
    primero = mu.groupby("serie").t.min()
    out["tasado_municipal"] = {"n_series": int(mu.serie.nunique()), "n_con_inicio_2005T1": int((primero == qidx("2005T1")).sum()),
                               "n_con_inicio_2020T1": int((primero == qidx("2020T1")).sum()),
                               "municipios_por_trimestre": {qlab(t): int(cov.loc[t]) for t in (qidx("2005T1"), qidx("2010T1"), qidx("2015T1"), qidx("2019T4"), qidx("2020T1"), qidx("2025T4")) if t in cov.index},
                               "tamano_umbral": "municipios >25.000 hab. (tabla 35103500); entrada de nuevos municipios en 2020T1"}
    wide = mu.pivot_table(index="t", columns="serie", values="valor")
    yy = (wide / wide.shift(4) - 1) * 100
    bal = yy[[c for c in wide.columns if primero[c] == qidx("2005T1")]]
    med_todos, med_bal = yy.median(axis=1), bal.median(axis=1)
    sel = (med_todos - med_bal).dropna().loc[qidx("2020T1"):]
    out["tasado_municipal"]["dif_mediana_tasa_todos_vs_balanceado_pp_desde_2020"] = {"media_abs": round(float(sel.abs().mean()), 3), "max_abs": round(float(sel.abs().max()), 3)}
    nac = yoy(D["p_tasado"][("nacional", "00")])
    j = pd.concat([nac, bal.mean(axis=1)], axis=1).dropna()
    out["tasado_municipal"]["corr_tasa_media_municipios_balanceados_vs_nacional"] = round(float(j.iloc[:, 0].corr(j.iloc[:, 1])), 3)
    # tabla provincial: primera observación (cobertura)
    pr = {k: int(s.index.min()) for k, s in D["p_tasado"].items() if k[0] == "provincia"}
    out["tasado_provincial"] = {"n_provincias_con_codigo": len(pr), "primer_trimestre_min": qlab(min(pr.values())), "primer_trimestre_max": qlab(max(pr.values()))}
    # (c) Registradores: ventana (consistencia de etiqueta) y retardo de respuesta frente a valor tasado
    r = pd.read_csv(PDF / "registradores_opendata_compraventas.csv")
    v = r[["periodo", "ventana"]].drop_duplicates()

    def fin_v(w: str) -> int:
        a, b = w.split("-")
        return int(b[:4]) * 4 + int(b[5]) - 1

    inconsist = int(sum(fin_v(w) != qidx(p) for p, w in zip(v.periodo, v.ventana, strict=True)))
    out["registradores_ventana"] = {"etiquetas_ventana_inconsistentes_con_periodo": inconsist, "n_periodos": int(len(v))}
    lag = {}
    for niv_k in (("nacional", "00"),):
        x, y = yoy(D["p_tasado"][niv_k]), yoy(D["reg_pm2"][niv_k])
        cs = {L: x.corr(y.shift(-L)) for L in range(-4, 9)}
        best = max(cs, key=lambda L: cs[L] if pd.notna(cs[L]) else -9)
        lag = {"corr_L0": round(float(cs[0]), 3), "retardo_optimo_trim": int(best), "corr_optima": round(float(cs[best]), 3)}
    out["registradores_retardo_vs_tasado_nacional_tasas"] = lag
    # (d) saltos de tasa en nacional (|dif. de tasa trimestral| con z robusto), solo fuentes redistribuibles con periodo
    saltos = []
    for f in ("p_tasado", "ipv", "p_bde", "reg_pm2", "not_pm2"):
        s = D[f][("nacional", "00")]
        y = yoy(s)
        dy = y.diff(2 if f == "not_pm2" else 1).dropna()
        z = zrob(dy)
        if z is None:
            continue
        k = z.abs().idxmax()
        saltos.append({"fuente": f, "z_max_cambio_tasa": round(float(z.loc[k]), 1), "periodo": qlab(int(k)) if f not in ("reg_pm2", "not_pm2") else "omitido",
                       "n_gt5": int((z.abs() > UMBRAL_Z).sum())})
    return out, pd.DataFrame(saltos)


# ---------------------------------------------------------------- principal


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    D = cargar()
    E = cargar_etdp()
    if SIN_MAPEAR:
        print("SIN MAPEAR a código INE:", {k: sorted(v)[:8] for k, v in SIN_MAPEAR.items()})
    rec, top, rangos = tarea1_atipicos(D)
    rec.to_csv(OUT / "atipicos_recuento.csv", index=False)
    top.to_csv(OUT / "atipicos_top20.csv", index=False)
    res, TR, DV = tarea2_coherencia(D)
    res.to_csv(OUT / "coherencia_pares.csv", index=False)
    TR.to_csv(OUT / "coherencia_territorios.csv", index=False)
    DV.to_csv(OUT / "divergencias_periodos.csv", index=False)
    acum, acum_res = acumulado(D)
    acum.to_csv(OUT / "acumulado_2015_2025.csv", index=False)
    acum_res.to_csv(OUT / "acumulado_2015_2025_resumen.csv", index=False)
    hv = hechos_vs_raw(D)
    bde = tarea_bde(D, {k: hv[k] for k in ("obs_comparadas", "obs_distintas")})
    comp, rel, seg, ext, cc = tarea3_composicion(D, E)
    comp.to_csv(OUT / "composicion_brecha.csv", index=False)
    rel.to_csv(OUT / "composicion_relacion_cuota_nueva.csv", index=False)
    cc.to_csv(OUT / "composicion_ccaa.csv", index=False)
    rev = tarea4_revisiones(D)
    rev["ediciones_por_variable_hechos"] = hv["ediciones_por_variable_hechos"]
    rup, saltos = tarea5_rupturas(D)
    saltos.to_csv(OUT / "rupturas_saltos_nacional.csv", index=False)

    def pick(a, b, var, niv):
        q = res[(res.A == a) & (res.B == b) & (res.variante == var) & (res.nivel == niv)]
        return q.iloc[0].to_dict() if len(q) else None

    clave_pares = {f"{n}|{a}|{b}|{v}": pick(a, b, v, n) for n in ("nacional", "ccaa", "provincia")
                   for a, b, v in (("p_tasado", "ipv", "directa"), ("p_tasado", "reg_pm2", "ventana4"), ("ipv", "reg_pm2", "ventana4"),
                                   ("p_tasado", "not_pm2", "semestral"), ("ipv", "not_pm2", "semestral"), ("reg_pm2", "not_pm2", "semestral"))
                   if pick(a, b, v, n)}
    resultado = {
        "rama": "v15/auditoria/precios_compra",
        "pregunta": "¿Qué medida de precio de compra es fiable como principal en V15 y cuáles solo como robustez? Atípicos, coherencia entre fuentes, sesgo de composición, revisiones y rupturas.",
        "capa": "C4",
        "datos": ["MIVAU valor tasado (nacional, CCAA, provincia, municipios >25.000 hab.)", "INE IPV 80270 y 25171", "BdE p_bde (be2507)",
                  "Registradores datos abiertos precio m2 (suma móvil 4T)", "Notariado precio m2 nacional semestral (CGN)",
                  "Anuario ERI 2023-2025 (solo revisiones)", "INE ETDP 6150 (solo volumen/cuota de nueva)"],
        "N": {"series_precio": int(sum(len(v) for v in D.values())), "series_municipales": rup["tasado_municipal"]["n_series"]},
        "metodo": ("Auditoría descriptiva determinista (SEED=20261010): tasa interanual, z robusto con mediana y MAD (|z|>5), correlación de tasas, "
                   "diferencia media, rachas >=8 trimestres con signo opuesto (ambas |tasa|>1 pp) o diferencia >5 pp, acumulado de medias anuales 2015-2025, "
                   "brecha logarítmica precio medio frente a IPV. Cruces por código INE."),
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {
            "atipicos_recuento": json.loads(rec.to_json(orient="records")),
            "atipicos_top20": json.loads(top.to_json(orient="records")),
            "rangos_unidades": rangos,
            "p_bde_vs_p_tasado": bde,
            "coherencia_resumen": clave_pares,
            "acumulado_2015_2025_nacional": {f: acum_res.loc[(acum_res.fuente == f) & (acum_res.nivel == "nacional"), "mediana"].tolist()
                                             for f in acum_res.fuente.unique()},
            "composicion_nacional": json.loads(comp.to_json(orient="records")),
            "composicion_relacion_cuota_nueva": json.loads(rel.to_json(orient="records")),
            "composicion_segmentos_bde_vs_ipv": json.loads(seg.to_json(orient="records")),
            "composicion_extra": ext,
            "composicion_ccaa": json.loads(cc.to_json(orient="records")),
            "revisiones": rev,
            "rupturas": rup,
            "rupturas_saltos_nacional": json.loads(saltos.to_json(orient="records")),
            "codigos_sin_mapear": {k: sorted(v) for k, v in SIN_MAPEAR.items()},
            "n_rachas_divergencia_total": int(len(DV)),
        },
        "fuera_muestra": None,
        "notas": ["Auditoría C4: sin efectos ni regresiones. Sin series por periodo de Notariado, Registradores ni ERI en output.",
                  "Tasas de Registradores: suma móvil de 4 trimestres (suaviza y retrasa); se comparan en variante ventana4.",
                  "Notariado: precio m2 nacional semestral; sin serie territorial de precio por m2 en el repositorio.",
                  "Municipios MIVAU sin código INE en el raw: atípicos y cobertura se reportan por nombre de serie, sin cruces."],
    }
    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=lambda o: None if pd.isna(o) else float(o) if isinstance(o, np.floating) else int(o)), encoding="utf-8")
    print("OK", OUT)


if __name__ == "__main__":
    main()
