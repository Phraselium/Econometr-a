"""V17 · D3 apoyo cuantitativo (preguntas 1-3). ANÁLISIS A POSTERIORI, contable y descriptivo (capa C4).

Sin lenguaje causal ni estimaciones nuevas de efectos. Sin red. SEED 20261010. Con la base (data/base/hechos.parquet) se filtra siempre
muestra_sellada_v6 == False; no se lee data/sealed ni se ejecuta evaluate_*. Los datos crudos de data/raw se leen en solo lectura.
Guarda de fuga v6 (docs/v17/decisiones.md, K5): toda tabla por CCAA, provincia o municipio pasa por holdout.excluir_sellados_v6()
(ocho CCAA de K8 y sus provincias y municipios). Excepción declarada: las series que solo se SUMAN para reconstruir el total
nacional (nacidos por provincia, MNP y EVR municipales) se leen completas, porque su resultado es el agregado nacional publicado
por el INE (nivel «nacional» de la guarda) y no se usa ningún detalle territorial.
Uso: python3 src/v17/d3_cuantitativo.py
Salidas: output/v17/d3/*.csv, informe.md, hechos.json, registro.csv
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.econ_utils import Registry  # noqa: E402
from src import holdout  # noqa: E402

SEED = 20261010
OUT = ROOT / "output" / "v17" / "d3"
HECHOS_BASE = ROOT / "data/base/hechos.parquet"
FECHA = "2026-10-19"
HECHOS: list[dict] = []
REG = Registry(OUT / "registro.csv")
CAPITALES = {"28": "28079", "08": "08019", "46": "46250", "41": "41091", "29": "29067", "50": "50297", "03": "03014", "07": "07040",
             "48": "48020", "30": "30030", "47": "47186", "14": "14021", "35": "35016"}
# NUTS 2 (esfuerzo de V16) → código INE de CCAA, para la guarda de fuga v6
NUTS2_INE = {"ES11": "12", "ES12": "03", "ES13": "06", "ES21": "16", "ES22": "15", "ES23": "17", "ES24": "02", "ES30": "13", "ES41": "07",
             "ES42": "08", "ES43": "11", "ES51": "09", "ES52": "10", "ES53": "04", "ES61": "01", "ES62": "14", "ES63": "18", "ES64": "19",
             "ES70": "05"}
# Cifras de documento (no se recalculan): ver docs/v17/referencias/ine_demografia.md y docs/v17/fuentes/oferta_capacidad.md
DOC = {"nac2026_extr": 10004581, "nac2026_esp": 39566144, "ecp2026_nota4t": 49570725,
       "nac2025": 321164, "def2025": 446982, "sv2025_tabla": -125818, "sv2025_texto": -122167,
       "proh_h2026": 19759349, "proh_h2041": 21943397, "bde_potencial_total": 7_000_000, "bde_potencial_6areas": 1_100_000,
       "bde_potencial_capitales": 320_000, "bde_madrid": 550_000, "bde_sevilla": 163_000, "bde_barcelona": 120_000,
       "bde_deficit_21_25": 750_000}


def hecho(id_, indicador, valor, minimo, maximo, unidad, periodo, cobertura, fuentes, lectura, fecha_dato, ficha, nota_extra=""):
    assert lectura in ("OF", "hecho", "cota", "asociación")
    f = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)
    HECHOS.append({"id": f"V17-D3-{id_}", "indicador": indicador, "valor": f(valor), "min": f(minimo), "max": f(maximo), "unidad": unidad,
                   "periodo": periodo, "cobertura": cobertura, "fuentes": fuentes, "capa": "C4", "lectura_v17": lectura,
                   "fecha_dato": fecha_dato, "ficha": f"output/v17/d3/informe.md#{ficha}", "nota": "a posteriori" + (f"; {nota_extra}" if nota_extra else "")})


# Tipo de rango de cada cifra (encargo final de V17): «rango» = intervalo del mismo valor (IC o cota); «referencias» = puntos de
# referencia de otra cosa (extremos anuales, años de comparación); «sin rango» si falta min o max.
RANGO = {"HOGARES-ORIGEN-NACIDOS-EXTRANJERO", "TENENCIA-PROPIEDAD-ESP", "TENENCIA-ALQUILER-ESP", "TENENCIA-PROPIEDAD-EXTR",
         "TENENCIA-ALQUILER-EXTR", "VARIANZA-COMUN-VALOR-TASADO", "VARIANZA-COMUN-IPV-CCAA", "VARIANZA-COMUN-IPVA", "VARIANZA-COMUN-SERPAVI",
         "VARIANZA-COMUN-IPC-ALQUILER", "PROD-NECESARIA-5A", "PROD-NECESARIA-10A"}


def tipo_rango(hechos: list[dict]) -> None:
    for h in hechos:
        if h["min"] is None or h["max"] is None:
            h["tipo_rango"] = "sin rango"
        else:
            h["tipo_rango"] = "rango" if h["id"].removeprefix("V17-D3-") in RANGO else "referencias"
        assert "véase" not in h["cobertura"].lower()


def num(s: pd.Series) -> pd.Series:
    """Cifras del INE en CSV con punto de millares."""
    return pd.to_numeric(s.astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")


def selladas() -> set[str]:
    """Provincias de los bloques sellados de v6 (src/holdout.py); coincide con las marcadas en la base."""
    return set(holdout.provincias_selladas_v6())


def sin_selladas(df: pd.DataFrame, col: str, nivel: str) -> pd.DataFrame:
    return holdout.excluir_sellados_v6(df, col, nivel)


def base(variable: str, nivel: str, freq: str) -> pd.DataFrame:
    return _base(variable, nivel, freq)


def _base(variable: str, nivel: str, freq: str) -> pd.DataFrame:
    d = duckdb.sql(f"select territorio_codigo c, periodo p, valor v from '{HECHOS_BASE}' where variable='{variable}' and nivel='{nivel}' "
                      f"and frecuencia='{freq}' and not muestra_sellada_v6").df()
    return sin_selladas(d, "c", nivel)   # la base no marca las filas de CCAA: la guarda las excluye


# =============================================================================== 1. DEMOGRAFÍA 2015-2025
def ecp_nacional() -> pd.DataFrame:
    e = pd.read_csv(ROOT / "data/raw/ine_ecp_nacional.csv")
    e = e[e.periodo.str.endswith("T1")].assign(anio=lambda d: d.periodo.str[:4].astype(int)).pivot(index="anio", columns="serie", values="valor")
    return e.rename(columns={"ECP320": "pob", "ECP701": "pob_ext_nac"})


def nacidos() -> pd.DataFrame:
    d = pd.read_csv(ROOT / "data/raw/v11/ine_ecp/ecp_t79278.csv.gz", dtype=str)
    d = d[d.Provincias.str[:2].str.isdigit() & (d.Nacionalidad == "Total") & d["País de nacimiento"].isin(["España", "Extranjero"])
          & d.fecha.str.endswith("-01-01")].copy()
    d["v"] = num(d.Total)
    d["anio"] = d.fecha.str[:4].astype(int)
    return d.groupby(["anio", "País de nacimiento"]).v.sum().unstack().rename(columns={"España": "nac_esp", "Extranjero": "nac_extr"})


def mnp() -> pd.DataFrame:
    m = pd.read_csv(ROOT / "data/raw/v11/ine_mnp/mnp_municipio.csv.gz", dtype={"cod_municipio": str})
    m = m[(m.anio >= 2014) & (m.cod_municipio != "EXTR")]
    t = m.groupby(["anio", "nac"])[["nacimientos", "defunciones"]].sum().unstack("nac").fillna(0)
    r = pd.DataFrame({"nacim": t["nacimientos"].sum(axis=1), "defun": t["defunciones"].sum(axis=1)})
    for g in ("ES", "EXT", "NC"):
        r[f"sv_{g}"] = t["nacimientos"][g] - t["defunciones"][g]
    r["sv"] = r.nacim - r.defun
    return r


def saldo_exterior() -> pd.DataFrame:
    f = pd.read_csv(ROOT / "data/raw/v11/ine_evr/flujos_exterior_municipio.csv.gz")
    f = f[f.anio.between(2015, 2020)].groupby("anio")[["altas_desde_extranjero", "bajas_al_extranjero"]].sum()
    f.columns = ["inmig", "emig"]
    emcr = {}
    for t, col in (("69696", "inmig"), ("69711", "emig")):
        d = pd.read_csv(ROOT / f"data/raw/v11/ine_emcr/emcr_t{t}.csv.gz", dtype=str)
        d = d[d.Provincias.isna() & d.Municipios.isna()]
        emcr[col] = pd.Series(num(d.Total).values, index=d.Periodo.astype(int).values)
    e = pd.DataFrame(emcr).sort_index().loc[2021:2024]
    r = pd.concat([f, e])
    r["saldo_ext"] = r.inmig - r.emig
    r["fuente_saldo"] = ["EVR (microdatos, suma municipal)"] * 6 + ["EMCR (tablas 69696/69711)"] * 4
    return r


def demografia() -> tuple[pd.DataFrame, pd.DataFrame]:
    e, n, sv, ex = ecp_nacional(), nacidos(), mnp(), saldo_exterior()
    filas = []
    for a in range(2015, 2026):
        p0, p1 = e.loc[a, "pob"], e.loc[a + 1, "pob"]
        r = {"anio": a, "periodo": f"1-1-{a} a 1-1-{a + 1}", "d_pob": p1 - p0,
             "d_pob_nac_ext": e.loc[a + 1, "pob_ext_nac"] - e.loc[a, "pob_ext_nac"]}
        r["d_pob_nac_esp"] = r["d_pob"] - r["d_pob_nac_ext"]
        if a in n.index and a + 1 in n.index:
            r["d_nacidos_extranjero"] = n.loc[a + 1, "nac_extr"] - n.loc[a, "nac_extr"]
            r["d_nacidos_espana"] = n.loc[a + 1, "nac_esp"] - n.loc[a, "nac_esp"]
        elif a == 2025:  # vintage mixto: 1-1-2025 serie vigente (t79278), 1-1-2026 nota ECP 4T25 (provisional); se marca
            r["d_nacidos_extranjero"] = DOC["nac2026_extr"] - n.loc[2025, "nac_extr"]
            r["d_nacidos_espana"] = DOC["nac2026_esp"] - n.loc[2025, "nac_esp"]
            r["nota"] = "nacidos 1-1-2026 de la nota ECP 4T25 (vintage distinto)"
        if a <= 2024:
            r.update(nacimientos=sv.loc[a, "nacim"], defunciones=sv.loc[a, "defun"], sv=sv.loc[a, "sv"], sv_nac_esp=sv.loc[a, "sv_ES"],
                     sv_nac_ext=sv.loc[a, "sv_EXT"], sv_nac_nc=sv.loc[a, "sv_NC"], fuente_sv="INE MNP microdatos (nacionalidad de la madre y del fallecido)")
        else:
            r.update(nacimientos=DOC["nac2025"], defunciones=DOC["def2025"], sv=DOC["nac2025"] - DOC["def2025"],
                     fuente_sv="INE EDeS/EMN 2025, provisional (nota de prensa; tabla -125.818, texto -122.167)")
        r["residuo_mig_ajustes"] = r["d_pob"] - r["sv"]
        r["peso_residuo_pct"] = 100 * r["residuo_mig_ajustes"] / r["d_pob"]
        if a in ex.index:
            r["saldo_exterior_oficial"], r["fuente_saldo"] = ex.loc[a, "saldo_ext"], ex.loc[a, "fuente_saldo"]
            r["ajuste_estadistico"] = r["residuo_mig_ajustes"] - r["saldo_exterior_oficial"]
        if a <= 2024:
            r["residuo_nac_esp"] = r["d_pob_nac_esp"] - r["sv_nac_esp"] - r["sv_nac_nc"] * 0
            r["residuo_nac_ext"] = r["d_pob_nac_ext"] - r["sv_nac_ext"]
        filas.append(r)
    d = pd.DataFrame(filas)
    d.loc[d.anio == 2020, "nota"] = "1-1-2021 = base censal del Censo 2021 (ruptura de nivel); año con pandemia"
    # grupos de nacionalidad: inmigración exterior por grupo (EVR/EMCR semestral, v2) y variación del padrón por grupo
    mg = pd.read_csv(ROOT / "data/raw/ine_v2_migraciones_prov.csv", dtype={"codigo": str})
    mg = mg[(mg.nivel == "nacional") & mg.desglose.str.startswith("nacionalidad=")]
    mg["grupo"] = mg.desglose.str.replace("nacionalidad=", "", regex=False)
    gr = ["De Sudamérica", "De Centro América y Caribe", "De Africa", "De Asia", "País de la UE28 sin España", "País de Europa menos UE28",
          "De América del Norte", "Oceanía", "Apátridas"]
    mg = mg[mg.grupo.isin(gr)].assign(anio=lambda x: x.periodo.str[:4].astype(int))
    inm = mg.groupby(["anio", "grupo", "periodo"]).valor.sum().groupby(["anio", "grupo"]).agg(["sum", "count"])
    inm = inm[inm["count"] == 2]["sum"].unstack("grupo").loc[2015:2021]
    pp = pd.read_csv(ROOT / "data/raw/ine_v2_padron_prov_pais.csv", dtype={"codigo": str})
    pp = pp[(pp.nivel == "nacional") & pp.desglose.str.replace("nacionalidad=", "", regex=False).isin(gr)]
    pp = pp.assign(anio=pp.periodo.str[:4].astype(int), grupo=pp.desglose.str.replace("nacionalidad=", "", regex=False))
    st = pp.pivot_table(index="anio", columns="grupo", values="valor", aggfunc="sum")
    return d, pd.concat({"inmigracion_exterior": inm, "stock_1_enero": st.loc[2015:]}, names=["medida"]).reset_index().rename(columns={"level_1": "anio"})


# =============================================================================== 1b. HOGARES (V16 + ampliación)
def hogares_motores(dem: pd.DataFrame) -> pd.DataFrame:
    epa = pd.read_csv(ROOT / "output/v16/f2_contabilidad/hogares_epa_2002_2021_nacional.csv")
    epa = epa[(epa.desde == 2014) & (epa.hasta == 2021)].iloc[[0]].assign(fuente="EPA (V16, tasas de jefatura Censo 2011 y 2021: ver V16)")
    ecp = pd.read_csv(ROOT / "output/v16/f2_contabilidad/hogares_ecp_anual_nacional.csv").assign(fuente="ECP (V16)")
    h = pd.concat([epa, ecp], ignore_index=True)
    h = h[["fuente", "desde", "hasta", "H0", "H1", "cambio_observado", "poblacion", "composicion_nacionalidad", "estructura_edad", "jefatura_residuo",
           "suma_componentes"]].copy()
    h["jefatura_residuo_tamano_hogar"] = h.jefatura_residuo
    for c in ("poblacion", "composicion_nacionalidad", "estructura_edad", "jefatura_residuo"):
        h[f"pct_{c}"] = 100 * h[c] / h.cambio_observado
    # periodo de enlace 2021-2026 (V16 anual, suma)
    d = dem.set_index("anio")
    h["pct_d_pob_nacidos_extranjero"] = [np.nan] + [100 * d.loc[a, "d_nacidos_extranjero"] / d.loc[a, "d_pob"] if a in d.index else np.nan for a in h.desde.iloc[1:]]
    h["nota"] = ""
    h.loc[0, "nota"] = "2014-2021: la jefatura (residuo) es negativa y mayor en valor absoluto que el cambio: la tasa de jefatura de referencia es del Censo 2021; leer con cautela (V16)"
    return h


def origen_hogares(dem: pd.DataFrame, h: pd.DataFrame) -> dict:
    """Atribución contable ILUSTRATIVA del cambio de hogares 2021-2026 a nacidos en el extranjero (mismo patrón de formación que el resto)."""
    d = dem.set_index("anio").loc[2021:2025]
    s_nac = d.d_nacidos_extranjero.sum() / d.d_pob.sum()
    s_ext = d.d_pob_nac_ext.sum() / d.d_pob.sum()
    cambio = h[(h.desde >= 2021)].cambio_observado.sum()
    pob = h[(h.desde >= 2021)].poblacion.sum()
    lo, hi = min(s_nac, s_ext, 1.0), min(max(s_nac, s_ext), 1.0)   # una cuota >100 % significa que la población nacida en España disminuye
    return {"s_nacidos_extr": s_nac, "s_nac_ext": s_ext, "cambio_hogares": cambio, "hog_lo": lo * pob, "hog_hi": hi * pob, "pob": pob,
            "sv_total": d.sv.sum(), "d_pob": d.d_pob.sum(), "resid": d.residuo_mig_ajustes.sum()}


# =============================================================================== 1c. TENENCIA (Censo 2021, muestra 10 %)
def tenencia() -> pd.DataFrame:
    h = pd.read_csv(ROOT / "data/raw/v11/ine_censo2021/hogares_muestra_municipio_nacionalidad.csv.gz", dtype={"cod_municipio": str})
    h = sin_selladas(h, "cod_municipio", "municipio")   # «PP99x» = municipios pequeños de la provincia PP: también se filtran
    h = h[h.tenencia.isin([2, 3, 4])]
    filas = []
    for g in ("nac_primera_persona", "nacido_en_espana", "llegada_espana"):
        for cat, y in h.groupby(g):
            n = y.hogares_muestra.sum()
            for cod, nom in ((2, "propiedad"), (3, "alquiler"), (4, "otra forma (cesión y similares)")):
                x = y.loc[y.tenencia == cod, "hogares_muestra"].sum()
                p = x / n
                se = np.sqrt(p * (1 - p) / n * 0.9)
                filas.append({"grupo": g, "categoria": cat, "tenencia": nom, "hogares_muestra": int(n), "pct": 100 * p, "ic95_lo": 100 * (p - 1.96 * se),
                              "ic95_hi": 100 * (p + 1.96 * se), "nota": "muestra del 10 % sin elevar; persona de mayor edad como referencia; error con corrección finita 0,9"})
    return pd.DataFrame(filas)


# =============================================================================== 2. GENERAL O LOCAL
def descomp(panel: pd.DataFrame, nboot: int = 300) -> dict:
    """panel: filas = años, columnas = provincias, valores = tasa (Δln). Cuota de varianza de la tasa: año (común), año+provincia, residuo local."""
    x = panel.dropna(axis=1)
    v = x.values
    tot = ((v - v.mean()) ** 2).sum()
    def cuotas(m):
        mu = m.mean()
        yr = m.mean(axis=1, keepdims=True) - mu
        pr = m.mean(axis=0, keepdims=True) - mu
        t = ((m - mu) ** 2).sum()
        return (m.shape[1] * (yr ** 2).sum()) / t, (m.shape[0] * (pr ** 2).sum()) / t, 1 - (m.shape[1] * (yr ** 2).sum() + m.shape[0] * (pr ** 2).sum()) / t
    c, p, l = cuotas(v)
    rng = np.random.default_rng(SEED)
    bs = np.array([cuotas(v[:, rng.integers(0, v.shape[1], v.shape[1])])[0] for _ in range(nboot)])
    # referencia de azar: permutación de los años dentro de cada provincia (rompe la co-variación entre provincias)
    pm = np.array([cuotas(np.apply_along_axis(rng.permutation, 0, v))[0] for _ in range(nboot)])
    return {"T": v.shape[0], "N": v.shape[1], "cuota_comun_anio": c, "cuota_provincia_fija": p, "cuota_local_provincia_x_anio": l,
            "ic95_lo": np.percentile(bs, 2.5), "ic95_hi": np.percentile(bs, 97.5), "azar_media": pm.mean(), "azar_p95": np.percentile(pm, 95), "var_total": tot / v.size}


def paneles(sel: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    out, niveles = [], []
    def anual_T(var, nivel="provincia"):
        d = base(var, nivel, "T")
        d["a"] = d.p.str[:4].astype(int)
        g = d.groupby(["c", "a"]).v.agg(["mean", "count"])
        g = g[g["count"] == 4]["mean"].unstack("c")
        return g
    def anual_A(var, nivel="provincia"):
        d = base(var, nivel, "A")
        d["a"] = d.p.astype(int)
        return d.pivot_table(index="a", columns="c", values="v")
    series = {"Valor tasado MIVAU (€/m², media anual)": (anual_T("valor_tasado"), 2014, 2025),
              "IPV INE por CCAA (índice, media anual)": (anual_T("ipv", "ccaa"), 2014, 2025),
              "IPC alquiler INE provincial (índice, media anual)": (anual_T("ipc_alquiler_indice"), 2014, 2025),
              "IPVA INE provincial (índice anual)": (anual_A("ipva_indice"), 2014, 2024),
              "SERPAVI alquiler €/m² mediana provincial": (anual_A("serpavi_alquiler_m2_mediana"), 2014, 2024)}
    for nom, (g, a0, a1) in series.items():
        g = g.loc[a0:a1]
        g = g.dropna(axis=1)
        r = np.log(g).diff().dropna()
        for per, (i, j) in {"2015-2019": (2015, 2019), "2020-2025": (2020, 2025), "2015-2025": (2015, 2025)}.items():
            rr = r.loc[i:min(j, a1)]
            if len(rr) < 3:
                continue
            d = descomp(rr)
            d.update(serie=nom, periodo=per if j <= a1 else f"{i}-{a1}")
            out.append(d)
            REG.log("v17-d3-panel", f"descomp_{nom[:20]}_{per}", "var(Δln) = año + provincia + local", i, min(j, a1), d["N"] * d["T"], np.nan, np.nan, np.nan,
                    coef_interes=d["cuota_comun_anio"], notas="C4 contabilidad de varianza; sin p-valores")
        acum = 100 * (g.loc[min(2024, a1)] / g.loc[2015] - 1) if a1 >= 2024 else None
        if acum is not None:
            niveles.append({"serie": nom, "periodo": f"2015-{min(a1, 2025)}", "N": acum.size, "mediana_pct": acum.median(), "p10_pct": acum.quantile(.1),
                            "p90_pct": acum.quantile(.9), "min_pct": acum.min(), "max_pct": acum.max(), "dispersion_p90_p10_pp": acum.quantile(.9) - acum.quantile(.1)})
    return pd.DataFrame(out), pd.DataFrame(niveles)


def deficit_provincial(sel: set[str]) -> tuple[pd.DataFrame, dict]:
    a = pd.read_csv(ROOT / "output/v5/A4/tablas/A4_deficit_provincial_ECP_MIVAU.csv", dtype={"cod_prov": str})
    a = a[a.periodo == "2021-2025"][["cod_prov", "provincia", "delta_hogares", "altas_libres", "altas_protegidas", "deficit_bajas0"]].copy()
    n = pd.read_csv(ROOT / "output/v5_1/T3/tablas/necesidad_provincial.csv", dtype={"cod_prov": str})[["cod_prov", "N10_min", "N10_central", "N10_max"]]
    a = a.merge(n, on="cod_prov", how="left")
    pub = a.copy()  # publicado en V5: solo se usa su SUMA nacional (total publicado), nunca el detalle de las selladas
    cols = [c for c in a.columns if c not in ("cod_prov", "provincia")]
    ns = sin_selladas(a, "cod_prov", "provincia")
    a.loc[~a.index.isin(ns.index), cols] = np.nan   # detalle provincial de las selladas en blanco (solo código y nombre)
    a["sellada_v6"] = ~a.index.isin(ns.index)
    assert set(a.loc[a.sellada_v6, "cod_prov"]) == sel
    b = a[~a.sellada_v6].sort_values("deficit_bajas0", ascending=False)
    pos = b[b.deficit_bajas0 > 0].copy()
    pos["cuota_pct"] = 100 * pos.deficit_bajas0 / pos.deficit_bajas0.sum()
    pos["acum_pct"] = pos.cuota_pct.cumsum()
    b = a.merge(pos[["cod_prov", "cuota_pct", "acum_pct"]], on="cod_prov", how="left").sort_values(["sellada_v6", "deficit_bajas0"], ascending=[True, False])
    res = {"n50": int((pos.acum_pct < 50).sum() + 1), "n80": int((pos.acum_pct < 80).sum() + 1), "n_pos": len(pos), "suma_pos": pos.deficit_bajas0.sum(),
           "n_prov": int((~b.sellada_v6).sum()), "total_pub": pub.deficit_bajas0.sum(), "n_neg": int((b.deficit_bajas0 <= 0).sum()),
           "top": ", ".join(pos.provincia.head(6)), "top_pct": pos.cuota_pct.head(6).sum()}
    return a.assign(orden=lambda d: d.deficit_bajas0.rank(ascending=False)), res | {"tabla": b}


def coronas(sel: set[str]) -> pd.DataFrame:
    partes = []
    for y in range(2015, 2025):
        f = ROOT / (f"data/raw/v11/ine_evr/od_municipios_{y}.parquet" if y <= 2020 else f"data/raw/v11/ine_emcr/od_municipios_{y}.parquet")
        o = pd.read_parquet(f)
        o["anio"] = y
        o = o[o.origen.str[:2].eq(o.destino.str[:2])]
        o = sin_selladas(sin_selladas(o, "origen", "municipio"), "destino", "municipio")
        partes.append(o.groupby(["anio", "origen", "destino"], as_index=False).n.sum())
    o = pd.concat(partes)
    filas = []
    for p, cap in CAPITALES.items():
        if p in sel:
            continue
        for y, g in o[o.origen.str[:2].eq(p) | o.destino.str[:2].eq(p)].groupby("anio"):
            sal = g[(g.origen == cap) & (g.destino != cap)].n.sum()
            ent = g[(g.destino == cap) & (g.origen != cap)].n.sum()
            filas.append({"cod_prov": p, "capital": cap, "anio": y, "salidas_a_resto_provincia": sal, "entradas_desde_resto_provincia": ent,
                          "saldo_capital_con_resto_provincia": ent - sal})
    c = pd.DataFrame(filas)
    return c


# =============================================================================== 3. FACTIBILIDAD
def ocupados_construccion() -> pd.DataFrame:
    B = ROOT / "data/raw/v17/oferta_capacidad/ine/"
    j8 = {s["COD"]: s for s in json.load(open(B / "ine_tabla_66078.json"))}["EPA677307"]["Data"]
    anual = {d["Anyo"]: d["Valor"] for d in j8}
    t = {s["COD"]: s for s in json.load(open(B / "ine_tabla_65313.json"))}["EPA398167"]["Data"]
    q = pd.DataFrame([{"anio": d["Anyo"], "fk": d["FK_Periodo"], "v": d["Valor"]} for d in t if d["Valor"] is not None])
    qa = q.groupby("anio").v.agg(["mean", "count"])
    qa = qa[qa["count"] == 4]["mean"]
    enlace = anual[2008] / qa[2008]
    s = {a: v for a, v in anual.items() if a in (2006, 2007)}
    s.update({a: v * enlace for a, v in qa.items()})
    return pd.DataFrame({"anio": list(s), "ocupados_construccion_miles": list(s.values()),
                         "nota": ["CNAE-93 anual (tabla 66078)" if a in (2006, 2007) else f"CNAE-2009 trimestral, media anual, enlazada x{enlace:.4f} con 2008 de 66078" for a in s]}), enlace


def imm_mano_obra() -> pd.Series:
    j = json.load(open(ROOT / "data/raw/v17/oferta_capacidad/ine/ine_tabla_8377.json"))[0]["Data"]
    d = pd.DataFrame([{"anio": x["Anyo"], "fk": x["FK_Periodo"], "v": x["Valor"]} for x in j if x["Valor"] is not None])
    d = d.groupby("anio").v.agg(["mean", "count"])
    return d[d["count"] == 12]["mean"]


def terminadas_anual() -> pd.Series:
    d = base("terminadas", "nacional", "T")
    d["a"] = d.p.str[:4].astype(int)
    g = d.groupby("a").v.agg(["sum", "count"])
    return g[g["count"] == 4]["sum"]


def factibilidad(dem: pd.DataFrame, def_prov: pd.DataFrame, sel: set[str]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    t = terminadas_anual()
    oc, enlace = ocupados_construccion()
    ocs = oc.set_index("anio").ocupados_construccion_miles
    mo = imm_mano_obra()
    cc = pd.read_csv(ROOT / "output/v5/cifras_clave.csv").set_index("id") if "id" in pd.read_csv(ROOT / "output/v5/cifras_clave.csv", nrows=1).columns else None
    d0 = {"C2/C4 1.0 (L3-DEF-2125, min)": 523606.0, "1.0 central (L3-DEF-2125)": 705778.0, "BdE (Informe Anual 2025)": float(DOC["bde_deficit_21_25"]),
          "1.0 (L3-DEF-2125, max)": 887950.0}
    h_anual = (DOC["proh_h2041"] - DOC["proh_h2026"]) / 15
    bajas_anual = 34320.1 / 5   # v5.1 T1, bajas centrales 2021-2025 (no se restan las liberadas por envejecimiento)
    filas = []
    prod_actual = float(np.mean([t[2024], t[2025]]))
    boom = float(t.loc[2005:2007].mean())
    prod2006 = float(t.loc[2006:2007].mean())
    prod_ocup = {a: t[a] / (ocs[a] * 1000) for a in (2007, 2024, 2025) if a in ocs.index and a in t.index}
    for nom, D in d0.items():
        for n in (5, 10):
            nec = D / n + h_anual + bajas_anual
            filas.append({"deficit_inicial_supuesto": nom, "deficit_inicial": D, "horizonte_anios": n, "hogares_nuevos_anuales_INE": h_anual,
                          "reposicion_anual_v5_1": bajas_anual, "produccion_anual_necesaria": nec, "produccion_actual_2024_2025": prod_actual,
                          "ratio_necesaria_actual": nec / prod_actual, "boom_2005_2007": boom, "ratio_necesaria_boom": nec / boom,
                          "empleo_implicito_miles_a_productividad_2007": nec / prod_ocup[2007] / 1000,
                          "empleo_implicito_miles_a_productividad_2025": nec / prod_ocup[2025] / 1000,
                          "ocupados_construccion_2025_miles": ocs.get(2025, np.nan), "ocupados_construccion_2007_miles": ocs[2007]})
    esc = pd.DataFrame(filas)
    for _, r in esc.iterrows():
        REG.log("v17-d3-escenario", f"prod_{r.deficit_inicial_supuesto[:12]}_{r.horizonte_anios}a", "(D0/N + H_INE + bajas)", 2026, 2026 + r.horizonte_anios, 1, np.nan, np.nan, np.nan,
                coef_interes=r.produccion_anual_necesaria, notas="escenario contable con supuestos explícitos; sin predicción")
    cap = pd.DataFrame({"anio": [2005, 2006, 2007, 2008, 2015, 2016, 2017, 2018, 2019, 2024, 2025]})
    cap["terminadas"] = cap.anio.map(t)
    cap["ocupados_construccion_miles"] = cap.anio.map(ocs)
    cap["terminadas_por_ocupado"] = cap.terminadas / (cap.ocupados_construccion_miles * 1000)
    cap["imm_mano_obra_indice_base1980"] = cap.anio.map(mo)
    defl = base("deflactor", "nacional", "T")
    defl["a"] = defl.p.str[:4].astype(int)
    dfl = defl.groupby("a").v.mean()
    cap["deflactor_base_indice"] = cap.anio.map(dfl)
    cap["mano_obra_real_rel_2007"] = (cap.imm_mano_obra_indice_base1980 / cap.deflactor_base_indice) / (mo[2007] / dfl[2007])
    # suelo/potencial BdE frente a necesidad en las áreas citadas (cifras de documento; áreas ≠ provincias)
    n10 = def_prov.set_index("cod_prov")
    filas = []
    for nombre, prov, pot in (("Madrid (área)", "28", DOC["bde_madrid"]), ("Barcelona (área)", "08", DOC["bde_barcelona"]), ("Sevilla (área)", "41", DOC["bde_sevilla"])):
        if prov in sel:
            filas.append({"area_bde": nombre, "provincia": prov, "potencial_bde": pot, "nota": "provincia en muestra sellada v6: necesidad no mostrada"})
            continue
        r = n10.loc[prov]
        filas.append({"area_bde": nombre, "provincia": prov, "potencial_bde": pot, "deficit_2021_2025_prov": r.deficit_bajas0, "necesidad_10a_prov_min": r.N10_min,
                      "necesidad_10a_prov_central": r.N10_central, "necesidad_10a_prov_max": r.N10_max,
                      "potencial_sobre_necesidad_10a": pot / r.N10_central if r.N10_central else np.nan,
                      "nota": "área urbana del BdE (SIU 2025) frente a provincia; no comparables 1 a 1"})
    suelo = pd.DataFrame(filas)
    info = {"prod_actual": prod_actual, "boom": boom, "t": t, "ocs": ocs, "mo": mo, "prod_ocup": prod_ocup, "h_anual": h_anual, "bajas_anual": bajas_anual, "dfl": dfl, "enlace": enlace}
    return esc, cap, info | {"suelo": suelo, "d0": d0}


# =============================================================================== principal
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    np.random.seed(SEED)
    sel = selladas()
    dem, grupos = demografia()
    dem.round(2).to_csv(OUT / "demografia_descomposicion_anual.csv", index=False)
    grupos.round(0).to_csv(OUT / "demografia_grupos_nacionalidad.csv", index=False)
    h = hogares_motores(dem)
    h.round(4).to_csv(OUT / "hogares_motores_2014_2026.csv", index=False)
    og = origen_hogares(dem, h)
    ten = tenencia()
    ten.round(3).to_csv(OUT / "tenencia_por_origen_censo2021.csv", index=False)
    dp, conc = deficit_provincial(sel)
    conc["tabla"].round(4).to_csv(OUT / "deficit_provincial_concentracion.csv", index=False)
    var, niv = paneles(sel)
    var.round(6).to_csv(OUT / "varianza_comun_local.csv", index=False)
    niv.round(2).to_csv(OUT / "variacion_acumulada_provincial.csv", index=False)
    cor = coronas(sel)
    cor.to_csv(OUT / "coronas_saldo_capital_resto_provincia.csv", index=False)
    esc, cap, inf = factibilidad(dem, dp, sel)
    esc.round(2).to_csv(OUT / "escenarios_produccion_5_10_anios.csv", index=False)
    cap.round(4).to_csv(OUT / "capacidad_construccion_boom_actual.csv", index=False)
    inf["suelo"].round(2).to_csv(OUT / "suelo_potencial_bde_vs_necesidad.csv", index=False)
    try:
        ep = pd.read_csv(ROOT / "output/v16/f2_esfuerzo/esfuerzo_cambios.csv")
        ep = ep[ep.dimension.str.lower().str.contains("ccaa|comunidad|provincia")].copy()
        ep["cod_ccaa_ine"] = ep.categoria.map(NUTS2_INE)
        assert ep.cod_ccaa_ine.notna().all(), "categoría NUTS2 sin código INE de CCAA"
        sin_selladas(ep, "cod_ccaa_ine", "ccaa").to_csv(OUT / "esfuerzo_territorial_v16.csv", index=False)
    except FileNotFoundError:
        pass
    construir_hechos(dem, h, og, ten, conc, var, niv, cor, esc, cap, inf)
    tipo_rango(HECHOS)
    json.dump(HECHOS, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)
    REG.flush()
    informe(dem, h, og, ten, conc, var, niv, cor, esc, cap, inf, grupos)
    print("ok", len(HECHOS), "hechos")


def construir_hechos(dem, h, og, ten, conc, var, niv, cor, esc, cap, inf):
    d = dem.set_index("anio")
    f_ecp = "INE ECP (ine_ecp_nacional.csv); INE MNP microdatos (data/raw/v11/ine_mnp)"
    # 1. demografía
    s = d.loc[2015:2025]
    hecho("POB-CRECIMIENTO", "Crecimiento de la población residente (ECP), 1-1-2015 a 1-1-2026", s.d_pob.sum(), s.d_pob.min(), s.d_pob.max(), "personas (valor = suma; min-max = anual)",
          "1-1-2015 a 1-1-2026", "España", f_ecp, "OF", "2026-07-01", "demografia", "ECP vigente (revisada); 1-1-2026 = 49.596.376; nota original 49.570.725")
    sv = s.sv.sum(); rs = s.residuo_mig_ajustes.sum()
    hecho("SV-ACUMULADO", "Saldo vegetativo acumulado 2015-2025 (2025 provisional)", sv, s.sv.min(), s.sv.max(), "personas", "2015-2025", "España", f_ecp + "; INE EDeS 2025 (nota)", "OF",
          "2026-02-18", "demografia", "2025: nacimientos 321.164 menos defunciones 446.982 (nota provisional)")
    hecho("RESIDUO-MIGRACION", "Crecimiento no explicado por el saldo vegetativo (saldo migratorio exterior neto y ajustes estadísticos)", rs, s.residuo_mig_ajustes.min(),
          s.residuo_mig_ajustes.max(), "personas", "2015-2025", "España", f_ecp, "hecho", "2026-07-01", "demografia", "identidad contable: ΔPoblación − saldo vegetativo")
    g = s[s.d_pob > 100000]
    hecho("RESIDUO-PESO", "Peso del residuo migratorio (más ajustes) en el crecimiento de la población", 100 * rs / s.d_pob.sum(), g.peso_residuo_pct.min(), g.peso_residuo_pct.max(), "% (valor acumulado 2015-2025; min-max anual en los años con crecimiento > 100.000)",
          "2015-2025", "España", f_ecp, "hecho", "2026-07-01", "demografia", "más de 100 % porque el saldo vegetativo resta; 2015-2016 se excluye del min-max (crecimiento casi nulo: cociente inestable)")
    e = s.dropna(subset=["saldo_exterior_oficial"])
    hecho("SALDO-EXTERIOR-OFICIAL", "Saldo migratorio exterior oficial (EVR 2015-2020, EMCR 2021-2024)", e.saldo_exterior_oficial.sum(), e.saldo_exterior_oficial.min(), e.saldo_exterior_oficial.max(),
          "personas", "2015-2024", "España", "INE EVR microdatos; INE EMCR tablas 69696 y 69711", "OF", "2025-12-11", "demografia", "2025: sin EMCR en los datos locales")
    hecho("AJUSTE-ESTADISTICO", "Diferencia entre el residuo padronal y el saldo exterior oficial (revisiones, ruptura censal 2021, bajas por caducidad)", e.ajuste_estadistico.sum(), e.ajuste_estadistico.min(),
          e.ajuste_estadistico.max(), "personas", "2015-2024", "España", f_ecp + "; INE EVR/EMCR", "hecho", "2026-07-01", "demografia", "el año 2020-2021 contiene la rebase al Censo 2021")
    n = s.dropna(subset=["d_nacidos_extranjero"])
    hecho("NACIDOS-EXTRANJERO-DELTA", "Variación de los nacidos en el extranjero residentes (1-1-2015 a 1-1-2026)", n.d_nacidos_extranjero.sum(), n.d_nacidos_extranjero.min(), n.d_nacidos_extranjero.max(),
          "personas", "2015-2025", "España", "INE ECP t79278; nota ECP 4T25 para 1-1-2026", "OF", "2026-02-12", "demografia", "último año con vintage mixto")
    hecho("NACIDOS-ESPANA-DELTA", "Variación de los nacidos en España residentes (1-1-2015 a 1-1-2026)", n.d_nacidos_espana.sum(), n.d_nacidos_espana.min(), n.d_nacidos_espana.max(), "personas", "2015-2025", "España",
          "INE ECP t79278; nota ECP 4T25", "OF", "2026-02-12", "demografia", "último año con vintage mixto")
    hecho("NACIDOS-EXTRANJERO-PESO", "Parte del crecimiento de la población que corresponde a nacidos en el extranjero", 100 * n.d_nacidos_extranjero.sum() / n.d_pob.sum(),
          100 * (n.d_nacidos_extranjero / n.d_pob)[n.d_pob > 100000].min(), 100 * (n.d_nacidos_extranjero / n.d_pob)[n.d_pob > 100000].max(), "% (valor acumulado; min-max anual con crecimiento > 100.000)", "2015-2025", "España", "INE ECP", "hecho", "2026-02-12", "demografia",
          "más de 100 % porque los nacidos en España disminuyen; contable, no dice que la inmigración cause nada; 2025 con vintage mixto")
    q = s.dropna(subset=["sv_nac_esp"])
    hecho("SV-NAC-ESPANOLA", "Saldo vegetativo de nacionalidad española (nacionalidad de la madre y del fallecido; proxy de nacidos en España)", q.sv_nac_esp.sum(), q.sv_nac_esp.min(), q.sv_nac_esp.max(),
          "personas", "2015-2024", "España", "INE MNP microdatos", "hecho", "2025-11-19", "demografia", "proxy por nacionalidad; el MNP microdatos no trae país de nacimiento de la madre")
    hecho("SV-NAC-EXTRANJERA", "Saldo vegetativo de nacionalidad extranjera (madre y fallecido)", q.sv_nac_ext.sum(), q.sv_nac_ext.min(), q.sv_nac_ext.max(), "personas", "2015-2024", "España", "INE MNP microdatos",
          "hecho", "2025-11-19", "demografia", "")
    hecho("HOGARES-CAMBIO-2021-2026", "Variación del número de hogares (ECP, V16)", og["cambio_hogares"], None, None, "hogares", "1-1-2021 a 1-1-2026", "España", "output/v16/f2_contabilidad", "OF", "2026-08-06",
          "hogares", "ECP vigente 2T26")
    ecp = h[h.fuente.str.startswith("ECP")]
    hecho("HOGARES-MOTOR-POBLACION", "Parte del cambio de hogares 2021-2026 atribuible al tamaño de la población (Shapley anual de V16, suma de los cinco años)", ecp.poblacion.sum(), None, None, "hogares", "2021-2026", "España",
          "output/v16/f2_contabilidad", "hecho", "2026-08-06", "hogares", f"{100 * ecp.poblacion.sum() / ecp.cambio_observado.sum():.1f} % del cambio")
    hecho("HOGARES-MOTOR-EDAD", "Parte atribuible a la estructura por edad (envejecimiento)", ecp.estructura_edad.sum(), None, None, "hogares", "2021-2026", "España", "output/v16/f2_contabilidad", "hecho",
          "2026-08-06", "hogares", f"{100 * ecp.estructura_edad.sum() / ecp.cambio_observado.sum():.1f} % del cambio")
    hecho("HOGARES-MOTOR-JEFATURA", "Parte atribuible a la jefatura (residuo; tamaño medio del hogar)", ecp.jefatura_residuo.sum(), None, None, "hogares", "2021-2026", "España", "output/v16/f2_contabilidad", "hecho",
          "2026-08-06", "hogares", "con tasas de jefatura constantes del Censo 2021; incluye emancipación y todo lo no medido")
    hecho("HOGARES-ORIGEN-NACIDOS-EXTRANJERO", "Parte del componente población del cambio de hogares 2021-2026 que corresponde a nacidos en el extranjero (misma formación de hogares; ilustrativo)", (og["hog_lo"] + og["hog_hi"]) / 2, og["hog_lo"], og["hog_hi"],
          "hogares", "2021-2026", "España", "INE ECP; V16", "cota", "2026-08-06", "hogares",
          f"cuota del crecimiento de población: nacidos en el extranjero {100 * og['s_nacidos_extr']:.1f} %, nacionalidad extranjera {100 * og['s_nac_ext']:.1f} %; min = cuota por nacionalidad × componente población; max = cuota por país de nacimiento (acotada a 100 %) × componente población")
    t = ten.set_index(["grupo", "categoria", "tenencia"])
    for g, k in (("nacido_en_espana", "si"), ("nacido_en_espana", "no")):
        v = t.loc[(g, k, "propiedad")]
        a = t.loc[(g, k, "alquiler")]
        hecho(f"TENENCIA-PROPIEDAD-{'ESP' if k == 'si' else 'EXTR'}", f"Hogares en propiedad, persona de mayor edad nacida {'en España' if k == 'si' else 'en el extranjero'}", v.pct, v.ic95_lo, v.ic95_hi, "% de hogares",
              "1-11-2021 (Censo)", "España sin las CCAA selladas v6 (Censo 2021, muestra del 10 %)", "INE Censo 2021 microdatos (hogares_muestra_municipio_nacionalidad)", "OF", "2025-01-01", "tenencia", "")
        hecho(f"TENENCIA-ALQUILER-{'ESP' if k == 'si' else 'EXTR'}", f"Hogares en alquiler, persona de mayor edad nacida {'en España' if k == 'si' else 'en el extranjero'}", a.pct, a.ic95_lo, a.ic95_hi, "% de hogares",
              "1-11-2021 (Censo)", "España sin las CCAA selladas v6 (Censo 2021, muestra del 10 %)", "INE Censo 2021 microdatos (hogares_muestra_municipio_nacionalidad)", "OF", "2025-01-01", "tenencia", "")
    # 2. general o local
    v = var.set_index(["serie", "periodo"])
    for nombre, clave, ident in (("Valor tasado MIVAU (€/m², media anual)", "2015-2025", "VARIANZA-COMUN-VALOR-TASADO"), ("IPV INE por CCAA (índice, media anual)", "2015-2025", "VARIANZA-COMUN-IPV-CCAA"),
                                 ("IPVA INE provincial (índice anual)", "2015-2024", "VARIANZA-COMUN-IPVA"), ("SERPAVI alquiler €/m² mediana provincial", "2015-2024", "VARIANZA-COMUN-SERPAVI"),
                                 ("IPC alquiler INE provincial (índice, media anual)", "2015-2025", "VARIANZA-COMUN-IPC-ALQUILER")):
        if (nombre, clave) in v.index:
            r = v.loc[(nombre, clave)]
            hecho(ident, f"Cuota de la varianza de la variación anual de {nombre.split(' (')[0]} debida al componente común (año)", 100 * r.cuota_comun_anio, 100 * r.ic95_lo, 100 * r.ic95_hi, "% (IC95 bootstrap por provincias)",
                  clave, f"{int(r.N)} {'CCAA' if 'CCAA' in nombre else 'provincias'} sin bloques sellados v6 (holdout.excluir_sellados_v6)", "INE; MIVAU; SERPAVI (data/base/hechos.parquet, no sellado)", "hecho", "2026-07-01", "general-local",
                  f"azar (permutación) {100 * r.azar_media:.1f} %; cuota local provincia×año {100 * r.cuota_local_provincia_x_anio:.1f} %; la cuota es descriptiva, no causal")
    hecho("DEFICIT-CONCENTRACION-50", "Provincias que suman la mitad del déficit positivo 2021-2025 (sin sellada v6)", conc["n50"], None, None, "provincias", "2021-2025", f"{conc['n_prov']} provincias no selladas",
          "output/v5/A4 (ECP INE; MIVAU)", "hecho", "2025-12-31", "general-local", f"publicado en V5 (52 provincias): 6 provincias suman el 50 %; aquí: {conc['top']}")
    hecho("DEFICIT-CONCENTRACION-80", "Provincias que suman el 80 % del déficit positivo 2021-2025 (sin sellada v6)", conc["n80"], None, None, "provincias", "2021-2025", f"{conc['n_prov']} provincias no selladas",
          "output/v5/A4", "hecho", "2025-12-31", "general-local", f"{conc['n_neg']} provincias con déficit ≤ 0")
    if len(cor):
        c = cor.groupby("cod_prov").saldo_capital_con_resto_provincia.sum()
        hecho("CORONAS-SALDO-CAPITAL", "Saldo acumulado 2015-2024 de las capitales con el resto de su provincia (negativo = la capital cede residentes a su corona)", c.sum(), c.min(), c.max(), "personas (valor = suma; min-max = capital)",
              "2015-2024", f"{c.size} capitales de provincias no selladas", "INE EVR/EMCR (od_municipios)", "hecho", "2025-12-11", "general-local", f"{int((c < 0).sum())} de {c.size} capitales con saldo negativo; solo movimientos entre municipios de la misma provincia")
    # 3. factibilidad
    t = inf["t"]
    hecho("PROD-ACTUAL", "Viviendas terminadas, media 2024-2025", inf["prod_actual"], t[2025], t[2024], "viviendas/año", "2024-2025", "España", "MIVAU fin de obra (base)", "OF", "2026-06-30", "factibilidad",
          "2025 frágil según V6.2; el Banco de España cita unas 92.000 en 2025 (solo prensa; ver correcciones.md)")
    hecho("PROD-BOOM", "Viviendas terminadas, media 2005-2007", inf["boom"], t.loc[2005:2007].min(), t.loc[2005:2007].max(), "viviendas/año", "2005-2007", "España", "MIVAU fin de obra (base)", "OF", "2026-06-30", "factibilidad", "")
    for nom in ("1.0 central (L3-DEF-2125)",):
        for n in (5, 10):
            r = esc[(esc.deficit_inicial_supuesto == nom) & (esc.horizonte_anios == n)].iloc[0]
            lo = esc[esc.horizonte_anios == n].produccion_anual_necesaria.min(); hi = esc[esc.horizonte_anios == n].produccion_anual_necesaria.max()
            hecho(f"PROD-NECESARIA-{n}A", f"Producción anual necesaria para cerrar el déficit inicial en {n} años y absorber los hogares nuevos y la reposición (escenario contable)", r.produccion_anual_necesaria, lo, hi,
                  "viviendas/año (valor = déficit central 705.778; min-max = déficit 523.606-887.950)", f"2026-{2025 + n}", "España", "output/v5/cifras_clave.csv (L3-DEF-2125); INE PROH 2026-2041; V5.1 T1", "cota", "2026-06-17", "factibilidad",
                  f"supuestos: hogares +{inf['h_anual']:,.0f}/año (proyección INE lineal), reposición {inf['bajas_anual']:,.0f}/año (V5.1, central); ratio sobre la producción actual {r.ratio_necesaria_actual:.2f}; sobre el boom {r.ratio_necesaria_boom:.2f}")
    po = inf["prod_ocup"]
    hecho("PROD-POR-OCUPADO", "Viviendas terminadas por ocupado en construcción", po[2025], po[2024], po[2007], "viviendas/ocupado (valor 2025; min 2024; max 2007)", "2007, 2024, 2025", "España", "MIVAU; INE EPA (66078 y 65313 enlazadas)", "hecho",
          "2026-07-28", "factibilidad", f"enlace CNAE-93 a CNAE-2009 por 2008: x{inf['enlace']:.4f}")
    ocs = inf["ocs"]
    hecho("OCUPADOS-CONSTRUCCION", "Ocupados en construcción 2025 frente a 2007", ocs[2025], ocs[2025], ocs[2007], "miles (valor 2025; max 2007)", "2007 y 2025", "España", "INE EPA tablas 66078 y 65313", "OF", "2026-07-28", "factibilidad",
          f"ratio 2025/2007 = {ocs[2025] / ocs[2007]:.2f}")
    m = cap.set_index("anio").mano_obra_real_rel_2007
    hecho("COSTE-MANO-OBRA-REAL", "Índice IMM de mano de obra en construcción, deflactado, 2025 respecto a 2007 (=1)", m[2025], m.dropna().min(), m.dropna().max(), "índice (2007=1; min-max: años 2005-2025 disponibles)", "2007-2025", "España", "INE IMM tabla 8377; deflactor de la base", "OF", "2026-09-21",
          "factibilidad", "deflactor de la base (IPC/PIB según serie); índice de coste de la mano de obra, no coste laboral total")
    s = inf["suelo"]
    hecho("BDE-POTENCIAL-6AREAS", "Potencial de viviendas previstas en las seis grandes áreas urbanas (cifra de documento del Banco de España)", DOC["bde_potencial_6areas"], DOC["bde_potencial_capitales"], DOC["bde_potencial_total"],
          "viviendas (valor = 6 áreas; min = capitales; max = España)", "SIU 2025", "6 áreas urbanas", "Banco de España, Informe Anual 2025, cap. 2, pp. 157-158", "OF", "2026-06-22", "factibilidad",
          "cifra de documento, no recalculada; el SIU provincial no se pudo descargar (403, V16): suelo por provincia no calculable con datos locales")
    hecho("BDE-POTENCIAL-SOBRE-5A", "Potencial BdE de las seis áreas (1,1 millones) frente a 5 años de producción necesaria (escenario central)", DOC["bde_potencial_6areas"] / (esc[(esc.horizonte_anios == 5) & (esc.deficit_inicial_supuesto == "1.0 central (L3-DEF-2125)")].produccion_anual_necesaria.iloc[0] * 5),
          None, None, "cociente", "2026-2030", "España frente a 6 áreas", "BdE; cálculo propio", "cota", "2026-06-22", "factibilidad", "compara un potencial de seis áreas con una necesidad nacional: solo orden de magnitud")


def informe(dem, h, og, ten, conc, var, niv, cor, esc, cap, inf, grupos):
    d = dem.set_index("anio")
    L = ["Análisis a posteriori (V17). Apoyo cuantitativo a las preguntas D3 1-3. Capa C4, contable y descriptivo; sin lenguaje causal.", "",
         "# V17 · D3 apoyo cuantitativo", "",
         "Generado por `src/v17/d3_cuantitativo.py` (SEED 20261010). Sin red. Con la base, siempre `muestra_sellada_v6 == False`; no se lee `data/sealed`. "
         "Cada cifra tiene id `V17-D3-*` en `hechos.json`. Registro de especificaciones: `registro.csv` (Registry de `src/econ_utils.py`).", ""]
    L += ["## 1. Población y hogares 2015-2025 <a id=\"demografia\"></a>", "",
          "Identidad: ΔPoblación = saldo vegetativo + residuo (saldo migratorio exterior neto + ajustes estadísticos). Población: ECP a 1 de enero, serie vigente (1-1-2026 = 49.596.376; la nota original daba 49.570.725). "
          "Saldo vegetativo: MNP microdatos hasta 2024; 2025 provisional de la nota EDeS/EMN (tabla -125.818; texto -122.167; se usa nacimientos menos defunciones). "
          "2024: los microdatos con residencia en España dan −116.056, igual que la nota del INE (sin excluir los residentes en el extranjero, 318.005 − 436.118 = −118.113). "
          "No hay país de nacimiento de la madre en los microdatos: el saldo vegetativo «de nacidos en España» se aproxima por NACIONALIDAD (madre y fallecido). "
          "Nacidos en el extranjero: ECP t79278 (a 1-1-2025) y nota ECP 4T25 (1-1-2026, vintage distinto).", "",
          "| Año (1-1 a 1-1) | ΔPoblación | Saldo vegetativo | Residuo migratorio y ajustes | Saldo exterior oficial | Δ nacidos en el extranjero | Δ nacidos en España | SV nac. española | SV nac. extranjera |", "|---|---|---|---|---|---|---|---|---|"]
    fm = lambda x: "—" if pd.isna(x) else f"{x:,.0f}".replace(",", ".")
    for a, r in d.iterrows():
        L.append(f"| {a}-{a + 1} | {fm(r.d_pob)} | {fm(r.sv)} | {fm(r.residuo_mig_ajustes)} | {fm(r.get('saldo_exterior_oficial'))} | {fm(r.get('d_nacidos_extranjero'))} | {fm(r.get('d_nacidos_espana'))} | {fm(r.get('sv_nac_esp'))} | {fm(r.get('sv_nac_ext'))} |")
    s = d.loc[2015:2025]
    L += ["", f"Acumulado 2015-2025: población {fm(s.d_pob.sum())}; saldo vegetativo {fm(s.sv.sum())}; residuo {fm(s.residuo_mig_ajustes.sum())} (el residuo es {100 * s.residuo_mig_ajustes.sum() / s.d_pob.sum():.0f} % del crecimiento). "
          "Lectura contable: el saldo vegetativo es negativo desde 2017 y el crecimiento procede del residuo migratorio. El residuo mezcla saldo exterior y ajustes (rebase censal 2021, revisiones); la columna «saldo exterior oficial» permite ver la diferencia. "
          "Qué NO se puede atribuir causalmente: por qué llegan (empleo, origen latinoamericano, reagrupación, regularizaciones), ni qué habría pasado sin ellos. Los datos locales no contienen esos motivos.", "",
          "Por grandes grupos de nacionalidad (inmigración exterior anual 2015-2021 y stock 1-1) en `demografia_grupos_nacionalidad.csv`. Se descarta mostrar 2022-2025 por grupos: la serie semestral v2 acaba en 2022S1 y el EMCR 2023+ solo tiene recuentos de inmigración (140 valores no vacíos).", ""]
    L += ["### Hogares: motores (reutiliza V16, `hogares_motores_2014_2026.csv`) <a id=\"hogares\"></a>", "", "| Periodo | Cambio de hogares | Población | Composición por nacionalidad | Estructura por edad | Jefatura (residuo; tamaño medio) |", "|---|---|---|---|---|---|"]
    for _, r in h.iterrows():
        L.append(f"| {r.desde}-{r.hasta} ({r.fuente.split(' ')[0]}) | {fm(r.cambio_observado)} | {fm(r.poblacion)} ({r.pct_poblacion:.0f} %) | {fm(r.composicion_nacionalidad)} | {fm(r.estructura_edad)} ({r.pct_estructura_edad:.0f} %) | {fm(r.jefatura_residuo)} |")
    L += ["", f"Atribución contable ilustrativa del componente población ({fm(og['pob'])} hogares) del cambio 2021-2026 ({fm(og['cambio_hogares'])}): entre {fm(og['hog_lo'])} y {fm(og['hog_hi'])} hogares corresponden al crecimiento de la población nacida en el extranjero (o de nacionalidad extranjera), suponiendo que forman hogares como el resto "
          f"(cuota del crecimiento de población: {100 * og['s_nacidos_extr']:.0f} % por país de nacimiento, mayor que 100 % porque la población nacida en España disminuye; {100 * og['s_nac_ext']:.0f} % por nacionalidad). Es una cota de contabilidad, no un efecto. "
          "Emancipación: no hay tasa de jefatura por edad posterior a 2021, de modo que queda dentro del residuo de jefatura (no se separa).", ""]
    tt = ten[ten.grupo == "nacido_en_espana"].set_index(["categoria", "tenencia"])
    L += ["### Tenencia por origen (Censo 2021, muestra del 10 %, persona de mayor edad del hogar) <a id=\"tenencia\"></a>", "", "| Origen | Propiedad | Alquiler | Otra |", "|---|---|---|---|"]
    for k, nom in (("si", "Nacida en España"), ("no", "Nacida en el extranjero")):
        L.append(f"| {nom} | {tt.loc[(k, 'propiedad'), 'pct']:.1f} % | {tt.loc[(k, 'alquiler'), 'pct']:.1f} % | {tt.loc[(k, 'otra forma (cesión y similares)'), 'pct']:.1f} % |")
    L += ["", "Por nacionalidad y año de llegada: `tenencia_por_origen_censo2021.csv`. ECEPOV 2021 no se ha usado (microdatos de 197 MB sin tabulación previa; pendiente).", ""]
    L += ["## 2. ¿General o local? <a id=\"general-local\"></a>", "",
          "Cuota de la varianza de la variación anual explicada por el componente común (efecto año), con IC95 por bootstrap de provincias y referencia de azar (permutación temporal dentro de cada provincia):", "",
          "| Serie | Periodo | N | T | Común (año) | IC95 | Azar | Provincia fija | Local (prov×año) |", "|---|---|---|---|---|---|---|---|---|"]
    for _, r in var.iterrows():
        L.append(f"| {r.serie} | {r.periodo} | {r.N} | {r['T']} | {100 * r.cuota_comun_anio:.0f} % | {100 * r.ic95_lo:.0f}-{100 * r.ic95_hi:.0f} | {100 * r.azar_media:.0f} % | {100 * r.cuota_provincia_fija:.0f} % | {100 * r.cuota_local_provincia_x_anio:.0f} % |")
    L += ["", "Variación acumulada 2015-2024 por provincia (dispersión), `variacion_acumulada_provincial.csv`:", "", "| Serie | N | Mediana % | P10 | P90 | Mín | Máx |", "|---|---|---|---|---|---|---|"]
    for _, r in niv.iterrows():
        L.append(f"| {r.serie} | {r.N} | {r.mediana_pct:.0f} | {r.p10_pct:.0f} | {r.p90_pct:.0f} | {r.min_pct:.0f} | {r.max_pct:.0f} |")
    L += ["", f"Concentración del déficit 2021-2025 (ECP y MIVAU, bajas 0; {conc['n_prov']} provincias sin muestra sellada): {conc['n50']} provincias suman la mitad del déficit positivo y {conc['n80']} el 80 % "
          f"({conc['top']} suman {conc['top_pct']:.0f} %); {conc['n_neg']} provincias con déficit ≤ 0. V5 publicó para las 52 provincias: 6 para el 50 % y 18 para el 80 %. Detalle: `deficit_provincial_concentracion.csv`.", "",
          "Esfuerzo: la tabla territorial de V16 (`esfuerzo_cambios`) se copia si contiene niveles territoriales (`esfuerzo_territorial_v16.csv`); no hay esfuerzo provincial propio en los datos locales. "
          "Factor europeo: no se descompone aquí (V16 ya estimó la cuota común del valor tasado: `output/v16/f2_contabilidad/precio_cuota_comun_periodo.csv`).", ""]
    if len(cor):
        c = cor.groupby("cod_prov").saldo_capital_con_resto_provincia.sum().sort_values()
        L += [f"Corona: saldo acumulado 2015-2024 de {c.size} capitales con el resto de su provincia: {fm(c.sum())} personas ({int((c < 0).sum())} capitales negativas); "
              f"mayores cesiones: {', '.join(f'{k} ({fm(v)})' for k, v in c.head(3).items())}. Solo cubre movimientos entre municipios de una misma provincia; no mide el padrón de la corona. "
              "Padrón por municipio no se ha usado (no hay serie municipal anual completa en los datos locales).", ""]
    L += ["Lectura (descriptiva): el cociente común/local depende de la serie; véase la tabla. Lo que sí se observa en los datos es que una parte de la varianza es local (prov×año) en todas las series y que el déficit está concentrado.", ""]
    L += ["## 3. Factibilidad <a id=\"factibilidad\"></a>", "",
          "**Suelo (SIU).** No hay SIU por provincia en los datos locales (descarga 403 en V16). Se usan cifras de documento del Banco de España (Informe Anual 2025, pp. 157-158): potencial de 7 millones de viviendas en España, 1,1 millones en las seis áreas urbanas y 320.000 en sus capitales. "
          "Comparación parcial con la necesidad de V5.1 (áreas ≠ provincias): `suelo_potencial_bde_vs_necesidad.csv`.", "",
          "**Producción.** Terminadas 2005-2007: media " + fm(inf["boom"]) + "; 2024-2025: " + fm(inf["prod_actual"]) + ".", "",
          "| Déficit inicial | Años | Producción necesaria (viv./año) | Frente a actual | Frente al boom | Empleo implícito a productividad 2007 (miles) | Ídem a productividad 2025 (miles) |", "|---|---|---|---|---|---|---|"]
    for _, r in esc.iterrows():
        L.append(f"| {r.deficit_inicial_supuesto} ({fm(r.deficit_inicial)}) | {r.horizonte_anios} | {fm(r.produccion_anual_necesaria)} | x{r.ratio_necesaria_actual:.2f} | x{r.ratio_necesaria_boom:.2f} | {fm(r.empleo_implicito_miles_a_productividad_2007)} | {fm(r.empleo_implicito_miles_a_productividad_2025)} |")
    L += ["", f"Supuestos: producción necesaria = D0/N + hogares nuevos anuales (INE, proyección 2026-2041: +2.184.048 hogares en 15 años = {fm(inf['h_anual'])}/año, lineal) + reposición {fm(inf['bajas_anual'])}/año (V5.1 T1, central; las viviendas liberadas por envejecimiento no se restan). "
          "Déficit inicial: rango de la 1.0 (L3-DEF-2125: 523.606 a 887.950; central 705.778) y la cifra del Banco de España (750.000). Escenario contable, no predicción.", "",
          "Capacidad (`capacidad_construccion_boom_actual.csv`): ocupados en construcción, terminadas por ocupado y coste de la mano de obra (IMM) deflactado, frente a 2007. "
          "El enlace de CNAE-93 a CNAE-2009 usa 2008 (ver `hechos.json`). Plazos de licencias y transporte a coronas: sin datos oficiales locales (ver `docs/v17/fuentes/oferta_capacidad.md`).", "",
          "## Límites", "- Contabilidad y descripción: nada aquí es un efecto causal. - ECP provisional (se revisa cada trimestre); 2025 vintage mixto. - MNP: nacionalidad, no país de nacimiento de la madre. "
          "- Provincias selladas v6 excluidas de todo cálculo con la base; las cifras de V5 sobre 52 provincias se citan solo como publicadas. - SIU provincial, plazos de licencias y ECEPOV: pendientes. "
          "- Las cifras del Banco de España son de documento; la de 92.000 terminadas en 2025 solo figura en prensa (correcciones.md).", ""]
    (OUT / "informe.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
