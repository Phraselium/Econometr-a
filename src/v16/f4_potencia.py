"""V16-F4.1 · Potencia y efecto mínimo detectable (MDE) de las preguntas nuevas Q1-Q10 → output/v16/potencia/.

PRE-REGISTRO: este módulo NO estima ningún efecto ni asociación entre tratamiento o exposición real y resultado.
- Los tratamientos son PLACEBO (unidades, fechas y exposiciones al azar, independientes del resultado), con la estructura de
  clusters y de periodos del diseño previsto; MDE80 = 2,8 × DT placebo = (z0,975 + z0,80) × EE empírico; la tasa de rechazo placebo al
  5 % con la agrupación prevista es el diagnóstico de la inferencia (método de src/v15/f1_potencia.py, cuyas funciones se importan).
- Regulaciones (Q1, Q2, Q6): solo unidades NO tratadas y periodos anteriores a la regulación real.
- RD (Q1, Q7): umbrales PLACEBO lejos del umbral legal. Para el umbral real solo se cuentan unidades (cobertura de la variable de
  asignación), nunca se mira el resultado.
- Series nacionales (Q5, Q9, Q10): simulación con el T disponible.
Muestras prohibidas: nunca se lee data/sealed. Se excluyen (a) filas con muestra_sellada_v6, (b) unidades de holdout.unidad_sellada_v16
(v6 + V15 + V16 a la vez), (c) CCAA completas selladas en v6 (K8), (d) periodos posteriores al último visto de V15
(docs/v15/sellado_v15.json) y filas posterior_prereg. Se declara cuántas unidades quedan (exclusiones.csv).
SEED = 20261010. `--smoke` ejecuta una submuestra.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
SAL = RAIZ / "output" / "v16" / "potencia"
SEED = 20261010
SMOKE = "--smoke" in sys.argv
REPS = 20 if SMOKE else 500
MC = 30 if SMOKE else 300
HECHOS = RAIZ / "data/base/hechos.parquet"
P16 = RAIZ / "data/processed/v16"
FASE = "v16-f4-potencia"


def _cargar(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m
    spec.loader.exec_module(m)
    return m


V15 = _cargar("v15_f1_potencia", RAIZ / "src/v15/f1_potencia.py")
V15.REPS = REPS
import holdout as HO  # noqa: E402  (solo funciones booleanas; no abre data/sealed)
from econ_utils import Registry  # noqa: E402

REG = None   # se crea en main(): importar el módulo (tests) no debe tocar registro.csv
ULTIMO_VISTO = json.loads((RAIZ / "docs/v15/sellado_v15.json").read_text(encoding="utf-8"))["ultimo_periodo_visto"]
GEO_PROV = pd.read_parquet(RAIZ / "data/base/geo/provincias.parquet", columns=["cod_provincia", "cod_ccaa"]).astype(str)
PROV2CCAA = dict(zip(GEO_PROV.cod_provincia.str.zfill(2), GEO_PROV.cod_ccaa.str.zfill(2)))
V6_PROV = set(HO.provincias_selladas_v6())
CCAA_V6 = {PROV2CCAA[p] for p in V6_PROV}
EXCL: list[dict] = []
FILAS: list[dict] = []
COLS = ["pregunta", "subdiseno", "datos", "nivel", "periodo", "n_unidades_antes", "n_unidades_despues", "n_obs", "T", "clusters", "tratadas",
        "construible", "identificacion", "sd_placebo", "mde80", "unidad_mde", "mde80_pct", "rechazo_placebo_5pct", "referencia_literatura",
        "ref_pct", "mde_vs_literatura", "recomendacion", "motivo", "tarea_autor"]


# ----------------------------------------------------------------------------------------------------- datos y exclusiones
def limpiar(df: pd.DataFrame, nivel: str, clave: str, nombre: str) -> pd.DataFrame:
    """df con columnas u, t, valor, s6, post. Aplica TODAS las exclusiones y anota cuántas unidades quedan."""
    n0 = df.u.nunique()
    f0 = len(df)
    df = df[~df.s6.fillna(False).astype(bool) & ~df.post.fillna(False).astype(bool)]
    cod = pd.Series(df.u.unique())
    if nivel == "ccaa":
        fuera = set(cod[cod.str.zfill(2).isin(CCAA_V6)])
    elif nivel in ("municipio", "distrito", "seccion", "provincia", "partido_judicial"):
        fuera = set(cod[HO.unidad_sellada_v16(cod, nivel).values]) if len(cod) else set()
    else:
        fuera = set()
    df = df[~df.u.isin(fuera)]
    if clave in ULTIMO_VISTO:
        df = df[df.t <= ULTIMO_VISTO[clave]]
    EXCL.append({"panel": nombre, "nivel": nivel, "unidades_antes": n0, "unidades_selladas_excluidas": len(fuera), "unidades_despues": df.u.nunique(),
                 "filas_antes": f0, "filas_despues": len(df), "corte_temporal_v15": ULTIMO_VISTO.get(clave, "sin restricción")})
    return df.reset_index(drop=True)


def leer(variable: str, nivel: str, freq: str, nombre: str, desag: str | None = None, fuente: str | Path | None = None, donde: str = "TRUE") -> pd.DataFrame:
    ruta = HECHOS if fuente is None else P16 / fuente
    cond = f"AND desagregacion LIKE '{desag}%'" if desag else ""
    df = duckdb.sql(f"""SELECT territorio_codigo AS u, periodo AS t, valor, muestra_sellada_v6 AS s6, posterior_prereg AS post
                        FROM read_parquet('{ruta}') WHERE variable='{variable}' AND nivel='{nivel}' AND frecuencia='{freq}' {cond} AND {donde}""").df()
    return limpiar(df, nivel, f"{variable}|{nivel}|{freq}", nombre)


def logp(d: pd.DataFrame, min_t: int = 0) -> pd.DataFrame:
    d = d[d.valor > 0].copy()
    d["y"] = np.log(d.valor)
    if min_t:
        d = d[d.groupby("u").t.transform("count") >= min_t]
    return d.reset_index(drop=True)


def sub(p: pd.DataFrame, rng, frac: float = 0.2) -> pd.DataFrame:
    if not SMOKE:
        return p
    u = p.u.unique()
    k = rng.choice(u, size=max(8, int(len(u) * frac)), replace=False)
    return p[p.u.isin(k)].reset_index(drop=True)


def ccaa_de(u: pd.Series) -> pd.Series:
    return u.str[:2].map(PROV2CCAA)


# -------------------------------------------------------------------------------------------- placebo (extensiones de V15)
def placebo_did_grupo(p, n_grupos_trat, adopciones, grupo, rng) -> dict:
    """Como V15.placebo_did pero el tratamiento se asigna a GRUPOS enteros (CCAA): imita la regulación autonómica."""
    fe = V15.FE2(p.u, p.t)
    yr = fe(p.y.values)
    g_u = pd.Series(grupo.values, index=p.u.values).groupby(level=0).first().reindex(fe.u).values
    gcod, gl = pd.factorize(g_u)
    g = gcod[fe.iu]
    orden = {t: k for k, t in enumerate(sorted(fe.t))}
    tk = p.t.map(orden).values
    bs, rech = [], 0
    for _ in range(REPS):
        tr = rng.choice(len(gl), size=min(n_grupos_trat, len(gl) - 1), replace=False)
        adop_g = np.full(len(gl), 10**6)
        adop_g[tr] = [orden[a] for a in rng.choice(adopciones, size=len(tr))]
        d = (tk >= adop_g[g]).astype(float)
        b, se = V15._coef(yr, fe(d), g)
        bs.append(b)
        rech += abs(b / se) > 1.96
    return {"sd_placebo": float(np.std(bs)), "tamano_5pct": rech / REPS}


def placebo_interaccion(p, grupo, rng, rho=0.8, comun=0.5) -> dict:
    """Exposición continua placebo × moderador placebo fijo por unidad (p. ej. inelasticidad): MDE de la interacción."""
    fe = V15.FE2(p.u, p.t)
    yr = fe(p.y.values)
    g = pd.factorize(grupo)[0]
    gu = pd.Series(g).groupby(fe.iu).first().reindex(range(len(fe.u))).values
    orden = {t: k for k, t in enumerate(sorted(fe.t))}
    tk = p.t.map(orden).values
    T, N, G = len(orden), len(fe.u), g.max() + 1
    bs, rech = [], 0
    for _ in range(REPS):
        sh = np.sqrt(comun) * rng.standard_normal((G, T))[gu] + np.sqrt(1 - comun) * rng.standard_normal((N, T))
        x = np.empty_like(sh)
        x[:, 0] = sh[:, 0]
        for k in range(1, T):
            x[:, k] = rho * x[:, k - 1] + np.sqrt(1 - rho**2) * sh[:, k]
        m = np.sqrt(comun) * rng.standard_normal(G)[gu] + np.sqrt(1 - comun) * rng.standard_normal(N)
        m = (m - m.mean()) / m.std()
        x1 = x[fe.iu, tk]
        x2 = x1 * m[fe.iu]
        X = np.column_stack([fe(x1 / x1.std()), fe(x2 / x2.std())])
        XtXi = np.linalg.inv(X.T @ X)
        b = XtXi @ X.T @ yr
        e = yr - X @ b
        S = np.zeros((G, 2))
        for j in range(2):
            S[:, j] = np.bincount(g, X[:, j] * e, minlength=G)
        V = XtXi @ (G / max(G - 1, 1) * S.T @ S) @ XtXi
        bs.append(b[1])
        rech += abs(b[1] / np.sqrt(V[1, 1])) > 1.96
    return {"sd_placebo": float(np.std(bs)), "tamano_5pct": rech / REPS}


def rd_local(x, y, w, cl, c, h):
    """Salto local lineal en c (kernel triangular, ancho h), EE agrupados por cl. x puede ser discreto."""
    m = (x >= c - h) & (x < c + h)
    if m.sum() < 30:
        return np.nan, np.nan, int(m.sum())
    xs, ys, ws, cs = x[m] - c, y[m], w[m], cl[m]
    k = np.clip(1 - np.abs(xs) / h, 0, None) * ws
    d = (xs >= 0).astype(float)
    X = np.column_stack([np.ones_like(xs), d, xs, d * xs])
    A = X.T @ (X * k[:, None])
    try:
        Ai = np.linalg.inv(A)
    except np.linalg.LinAlgError:
        return np.nan, np.nan, int(m.sum())
    b = Ai @ (X.T @ (k * ys))
    e = ys - X @ b
    sc = pd.factorize(cs)[0]
    G = sc.max() + 1
    S = np.column_stack([np.bincount(sc, k * X[:, j] * e, minlength=G) for j in range(4)])
    V = Ai @ (G / max(G - 1, 1) * S.T @ S) @ Ai
    return float(b[1]), float(np.sqrt(V[1, 1])), int(m.sum())


def rd_placebo(x, y, w, cl, cortes, h) -> dict:
    r = [rd_local(x, y, w, cl, c, h) for c in cortes]
    r = [t for t in r if not np.isnan(t[0])]
    b = np.array([t[0] for t in r])
    se = np.array([t[1] for t in r])
    return {"sd_placebo": float(np.std(b)), "ee_medio": float(np.mean(se)), "tamano_5pct": float(np.mean(np.abs(b / se) > 1.96)),
            "n_cortes": len(r), "n_local_medio": float(np.mean([t[2] for t in r]))}


# --------------------------------------------------------------------------------------------------------------- filas
def recomendar(datos: str, ident: str, mde, ref, rech) -> str:
    """Regla fijada ANTES de ver resultados (datos: si/parcial/no; ident: adecuada/debil/ninguna)."""
    if datos == "no":
        return "descartada"
    if ident == "ninguna":
        return "reformulada"
    ok = (rech is None) or (isinstance(rech, float) and np.isnan(rech)) or rech <= 0.075
    if mde is None or np.isnan(mde) or ref is None or np.isnan(ref):
        return "exploratoria (BH)"
    if mde <= ref and ident == "adecuada" and ok and datos == "si":
        return "confirmatoria"
    if mde <= ref:
        return "exploratoria (BH)"
    if mde <= 1.5 * ref:
        return "exploratoria (BH)"
    return "reformulada" if ident == "adecuada" else "descartada"


def fila(p, sub_, datos, nivel, periodo, antes, despues, n_obs, T, clusters, tratadas, construible, ident, res=None, unidad="log puntos",
         ref_txt="", ref=np.nan, motivo="", tarea="", datos_ok="si", mde=None, rec=None, es_log=True):
    sd = np.nan if res is None else res["sd_placebo"]
    rech = np.nan if res is None else res.get("tamano_5pct", np.nan)
    if mde is None:
        mde = np.nan if res is None else 2.8 * sd
    mpct = 100 * mde if (es_log and not np.isnan(mde)) else np.nan
    cmp_ = mpct if es_log else mde
    rec = rec or recomendar(datos_ok, ident, cmp_, ref, rech)
    vs = "sin magnitud comparable" if (ref is None or np.isnan(ref) or np.isnan(cmp_)) else ("MDE por debajo de lo plausible" if cmp_ <= ref else "MDE por encima de lo plausible")
    FILAS.append({"pregunta": p, "subdiseno": sub_, "datos": datos, "nivel": nivel, "periodo": periodo, "n_unidades_antes": antes,
                  "n_unidades_despues": despues, "n_obs": n_obs, "T": T, "clusters": clusters, "tratadas": tratadas, "construible": construible,
                  "identificacion": ident, "sd_placebo": None if np.isnan(sd) else round(sd, 5), "mde80": None if np.isnan(mde) else round(mde, 4),
                  "unidad_mde": unidad, "mde80_pct": None if np.isnan(mpct) else round(mpct, 2),
                  "rechazo_placebo_5pct": None if (rech is None or np.isnan(rech)) else round(float(rech), 3), "referencia_literatura": ref_txt,
                  "ref_pct": None if (ref is None or np.isnan(ref)) else round(float(ref), 3), "mde_vs_literatura": vs, "recomendacion": rec,
                  "motivo": motivo, "tarea_autor": tarea})
    if REG is not None:
      REG.log(FASE, f"{p}:{sub_}"[:80], "placebo (sin efecto real)", periodo.split("-")[0] if periodo else "", periodo.split("-")[-1] if periodo else "",
            int(n_obs) if n_obs == n_obs and n_obs is not None else 0, np.nan, np.nan, np.nan, coef_interes=np.nan, p_interes=np.nan,
            notas=f"mde80={None if np.isnan(mde) else round(mde, 4)} {unidad}; rechazo={rech}")


def info(nombre):
    e = [x for x in EXCL if x["panel"] == nombre][-1]
    return e["unidades_antes"], e["unidades_despues"]


# ------------------------------------------------------------------------------------------------------------ literatura
META = pd.read_csv(RAIZ / "output/v16/f3/metaanalisis.csv")


def lit(instr: str, patron: str) -> tuple[str, float]:
    m = META[(META.instrumento == instr) & META.resultado.str.contains(patron, case=False, regex=True) & META["mediana"].notna()]
    if m.empty:
        return f"{instr}/{patron}: sin fila en output/v16/f3/metaanalisis.csv", np.nan
    r = m.iloc[0]
    return (f"{instr} «{r.resultado}»: mediana {r['mediana']:g} (rango {r['min']:g} a {r['max']:g}; {int(r.estudios)} estudio(s); {r.unidad_efecto[:60]}; "
            f"NO VERIFICADA, solo orientativa)"), abs(float(r["mediana"]))


def main() -> int:
    global REG
    REG = Registry(SAL / "registro.csv")
    rng = np.random.default_rng(SEED)
    SAL.mkdir(parents=True, exist_ok=True)
    zt = duckdb.sql(f"SELECT territorio_codigo AS u, min(periodo) AS adop FROM read_parquet('{HECHOS}') WHERE variable='zt_vigente' AND valor=1 GROUP BY 1").df()
    zt_todos = set(zt.u)
    zt_ns = set(zt.u[~HO.unidad_sellada_v16(zt.u, "municipio").values])
    cat = ("08", "17", "25", "43")
    prov_zt = {u[:2] for u in zt_todos}
    extra = {}

    # =============================================================================================== Q1 zonas tensionadas
    ref1_txt, ref1 = lit("L1_control_alquileres", "contratos_regulados")
    ref1_txt += "; propio: V9-D1b −5,9 % (contratos nuevos, Cataluña)"
    # --- Q1a RD: construcción de la variable de asignación (art. 18 Ley 12/2023); solo cobertura y conteos
    sp = logp(leer("serpavi_alquiler_m2_mediana", "municipio", "A", "q1_serpavi_mun", desag="tipologia=VC"))
    adrh = leer("ine_adrh_renta_neta_media_hogar_eur", "municipio", "A", "q1_adrh_mun", fuente="renta_parque.parquet")
    w = sp.pivot_table(index="u", columns="t", values="valor")
    renta = adrh[adrh.t == "2023"].set_index("u").valor
    ipc = duckdb.sql(f"SELECT periodo, valor FROM read_parquet('{HECHOS}') WHERE variable='inflacion_ipc_yoy' AND nivel='nacional' AND frecuencia='T' AND periodo LIKE '%T4'").df().set_index("periodo").valor
    ipc5 = float(np.sum(np.log1p(ipc.loc[[f"{a}T4" for a in range(2020, 2025)]] / 100)))   # IPC acumulado 2019T4→2024T4 (log)
    umbral = np.log1p(np.expm1(ipc5) + 0.03)
    g5 = (np.log(w["2024"]) - np.log(w["2019"])).dropna()
    esf = (w["2023"] * 70 / (renta.reindex(w.index) / 12)).dropna()   # supuesto: 70 m² útiles; sin gastos ni suministros (infraestima)
    ven = g5[(g5 - umbral).abs() <= 0.10]
    zt_en_g5 = [u for u in g5.index if u in zt_ns]
    n_mun_ns = len(set(duckdb.sql(f"SELECT DISTINCT territorio_codigo u FROM read_parquet('{P16/'renta_parque.parquet'}') WHERE nivel='municipio'").df().u)
                   - set(HO.municipios_sellados_v16()) - set(HO.municipios_sellados_v15()))
    extra["q1_rd_cobertura"] = {
        "municipios_ADRH_no_sellados": int(adrh.u.nunique()), "municipios_SERPAVI_alquiler_no_sellados": int(w.shape[0]),
        "con_crecimiento_5a_2019_2024": int(len(g5)), "umbral_crecimiento_5a_log (IPC acumulado + 3 p.p.)": round(float(umbral), 4),
        "con_cociente_alquiler_renta (proxy, 70 m2 sin suministros)": int(len(esf)), "cociente_alquiler_renta>0,30": int((esf > 0.30).sum()), "cociente_alquiler_renta_maximo": round(float(esf.max()), 3), "cociente_alquiler_renta_p95": round(float(esf.quantile(0.95)), 3),
        "dentro_de_±10_log_puntos_del_umbral_de_precio": int(len(ven)),
        "ZT_vigentes_no_selladas_con_crecimiento_5a": len(zt_en_g5), "precio_de_compra_municipal_5a": 0,
        "ZT_vigentes_totales (todas)": len(zt_todos), "ZT_vigentes_no_selladas": len(zt_ns)}
    a0, d0 = info("q1_serpavi_mun")
    fila("Q1", "RD en umbrales del art. 18 (variable de asignación)", "SERPAVI €/m² municipal + ADRH renta + IPC; cobertura, sin resultado",
         "municipio", "2019-2024", a0, d0, len(g5), 6, "municipios", len(zt_en_g5), f"parcial: crecimiento de alquiler 5 a en {len(g5)} municipios; "
         f"cociente esfuerzo (proxy) en {len(esf)}; precio de compra municipal 0; suministros 0", "ninguna", unidad="n/d",
         ref_txt=ref1_txt, ref=ref1, datos_ok="parcial", rec="reformulada",
         motivo="La declaración es discrecional (la CCAA la solicita y el Ministerio la resuelve tras memoria justificativa): el umbral no asigna el tratamiento de forma "
                "determinista ni probabilística conocida (a lo sumo RD borroso con cumplimiento bajo). El criterio de compra no se construye (sin precio de compra "
                "municipal) y faltan suministros. Se reformula como diagnóstico descriptivo de elegibilidad, no como identificación.",
         tarea="Tarea 3 (precio de compra municipal: Registradores/Notariado, MIVAU); fianzas por tipo (tarea 7)", es_log=False)
    # --- Q1a' RD placebo (umbrales falsos, resultado posterior pero previo a la ZT; solo no-Cataluña): MDE de un RD borroso con N similar
    w16 = w[[c for c in ("2016", "2021", "2023") if c in w.columns]].dropna()
    w16 = w16[~w16.index.str[:2].isin(cat)]
    x = (np.log(w16["2021"]) - np.log(w16["2016"])).values
    y = (np.log(w16["2023"]) - np.log(w16["2021"])).values
    q_real = float((g5 < umbral).mean())
    qs = [q for q in np.arange(0.15, 0.86, 0.05) if abs(q - q_real) > 0.20]
    cortes = np.quantile(x, qs)
    h = 1.5 * float(np.std(x)) * 0.5
    r = rd_placebo(x, y, np.ones(len(x)), w16.index.str[:2].values, cortes, h)
    r["sd_placebo"] = r["sd_placebo"]
    a1, d1 = info("q1_serpavi_mun")
    fila("Q1", "RD con umbrales PLACEBO (cuantiles lejos del umbral real), local lineal, EE por provincia", "SERPAVI €/m² Δlog 2021→2023 sobre Δlog 2016→2021",
         "municipio (sin Cataluña)", "2016-2023", a1, int(len(w16)), len(w16), 3, f"{pd.Series(w16.index.str[:2]).nunique()} provincias", 0,
         "sí (cortes placebo)", "debil", res={"sd_placebo": r["sd_placebo"], "tamano_5pct": r["tamano_5pct"]}, ref_txt=ref1_txt, ref=ref1,
         motivo=f"{r['n_cortes']} cortes placebo, ~{r['n_local_medio']:.0f} municipios por ventana; MDE de un RD NÍTIDO. Con cumplimiento c < 1 el MDE del efecto "
                "sobre los tratados es MDE/c.", tarea="")
    # --- Q1b SDID / control sintético aumentado (cota superior de MDE: DiD placebo en la muestra de donantes)
    zt_u = zt_ns
    ipva = logp(leer("ipva_tam_indice", "municipio", "A", "q1_ipva_mun", desag="tamano=Total"), min_t=8)
    ipva = ipva[ipva.t <= "2023"]
    for nombre, pan, adop, pos in (("SERPAVI municipal", sp[sp.t <= "2023"], ["2023"], 1), ("SERPAVI municipal", sp[sp.t <= "2023"], ["2021"], 3),
                                   ("IPVA municipal (contratos totales)", ipva, ["2023"], 1)):
        pan = pan[~pan.u.isin(zt_todos) & ~pan.u.str[:2].isin(cat)]
        pan = pan[pan.groupby("u").t.transform("count") >= 8].reset_index(drop=True)
        pan = sub(pan, rng)
        n_tr = int(len({u for u in zt_u if u[:2] not in cat}))
        n_tr = max(10, min(n_tr, pan.u.nunique() // 3))
        res = V15.placebo_did(pan, n_tr, adop, pan.u.str[:2], rng)
        a, d = info("q1_serpavi_mun" if "SERPAVI" in nombre else "q1_ipva_mun")
        fila("Q1", f"SDID/ASCM (cota: DiD placebo, donantes de otras CCAA), {nombre}, {pos} año(s) posterior(es)", nombre, "municipio", "2011-2023", a, d,
             len(pan), pan.t.nunique(), "provincias", n_tr, "sí (donantes: municipios nunca tratados, sin Cataluña)", "adecuada" if pos > 1 else "debil",
             res=res, ref_txt=ref1_txt, ref=ref1,
             motivo=("La base solo llega a 2024: 1 año posterior para las ZT de 2024 (SERPAVI/IPVA terminan en 2024). " if pos == 1 else "")
             + "SDID reduce la varianza respecto al DiD: el MDE es una cota superior.", tarea="")
    # IPVA provincial por tipo de contrato (contratos nuevos), 2021-2024
    ipn = []
    for ct in ("Nuevo contrato", "Contrato existente"):
        d_ = logp(leer("ipva_indice", "provincia", "A", f"q1_ipva_prov_{ct[:5]}", desag=f"contrato={ct}"))
        d_ = d_[(d_.t <= "2023") & ~d_.u.isin(prov_zt)]
        a, d = info(f"q1_ipva_prov_{ct[:5]}")
        res = V15.placebo_did(d_, max(3, d_.u.nunique() // 6), ["2023"], ccaa_de(d_.u), rng)
        fila("Q1", f"IPVA provincial, {ct}, DiD placebo (1 año posterior)", "ipva_indice provincia", "provincia", "2021-2023", a, d, len(d_), d_.t.nunique(),
             f"{ccaa_de(d_.u).nunique()} CCAA", max(3, d_.u.nunique() // 6), "sí", "debil", res=res, ref_txt=ref1_txt, ref=ref1,
             motivo="T = 3 antes de la ZT (2021-2023): sin pretendencias evaluables (Honest DiD sin potencia).", tarea="")
    # --- Q1c resultados adicionales: venta y precio de compra a escala provincial (solo hay provincial/CCAA)
    for var, nom in (("compraventas", "compraventas (volumen)"), ("valor_tasado", "valor tasado (precio de compra)")):
        d_ = logp(leer(var, "provincia", "T", f"q1_{var}_prov"), min_t=40)
        d_ = d_[(d_.t <= "2023T4") & ~d_.u.isin(prov_zt) & ~d_.u.str[:2].isin(cat)]
        a, d = info(f"q1_{var}_prov")
        ntr = max(3, int(round(d_.u.nunique() * 8 / 41)))
        d_ = sub(d_, rng)
        res = V15.placebo_did(d_, ntr, ["2021T4"], ccaa_de(d_.u), rng)
        fila("Q1", f"Desplazamiento a venta / precio de compra: {nom}, DiD placebo provincial (9 trimestres posteriores)", var, "provincia", "2007T1-2023T4", a, d,
             len(d_), d_.t.nunique(), f"{ccaa_de(d_.u).nunique()} CCAA", ntr, "parcial: ZT municipales diluidas en provincia", "debil", res=res,
             ref_txt=lit("L1_control_alquileres", "compraventa_precio")[0], ref=lit("L1_control_alquileres", "compraventa_precio")[1],
             motivo="La ZT es municipal y el resultado provincial: atenuación por dilución. No hay precio de compra municipal en la base.",
             tarea="Tarea 3 (precio de compra municipal)")
    fila("Q1", "Desplazamiento a alquiler de temporada", "Inside Airbnb desde 2025-12 (sin periodo previo)", "municipio", "2025-12 a 2026-09", np.nan, np.nan, np.nan, 10,
         "", 0, "no: sin periodo anterior a las ZT de 2024", "ninguna", unidad="n/d", datos_ok="no",
         motivo="Inside Airbnb en la base empieza en 2025-12 y las ZT son de 2024-2026: no hay pretendencias. Solo descriptivo.",
         tarea="Tarea 3.1 (Inside Airbnb histórico) y 3.7 (fianzas por tipo)", es_log=False)

    # =============================================================================================== Q2 vivienda turística
    ref2_txt, ref2 = lit("L2_vivienda_turistica_regulacion", "alquiler residencial")
    ia = leer("ia_anuncios_total_numero", "seccion", "D", "q2_ia_seccion", fuente="alquiler_turismo.parquet")
    ia_m = leer("ia_anuncios_total_numero", "municipio", "D", "q2_ia_municipio", fuente="alquiler_turismo.parquet")
    a, d = info("q2_ia_seccion")
    fila("Q2", "Inside Airbnb (secciones/municipios no sellados): cobertura", "ia_anuncios_total_numero", "sección", f"{ia.t.min()} a {ia.t.max()}", a, d, len(ia),
         int(ia.t.nunique()), f"{ia_m.u.nunique()} municipios", 0, "no para DiD: solo posterior a las moratorias", "ninguna", unidad="n/d", datos_ok="no",
         motivo=f"{ia.t.nunique()} instantáneas entre 2025-12 y 2026-09 en {d} secciones y {ia_m.u.nunique()} municipios no sellados; Madrid, Mallorca y Canarias "
                "están selladas (K8). Sin periodo previo no hay DiD con las moratorias; solo descriptivo de la oferta.", tarea="Tarea 3.1", es_log=False)
    ipm = ipva[ipva.t <= "2023"]
    pan = ipm[~ipm.u.str[:2].isin(cat) & ~ipm.u.isin(zt_todos)]
    pan = pan[pan.groupby("u").t.transform("count") >= 8].reset_index(drop=True)
    pan = sub(pan, rng)
    res = V15.placebo_did(pan, 1, ["2023"], pan.u, rng)
    a, d = info("q1_ipva_mun")
    fila("Q2", "DiD con moratorias: 1 ciudad tratada no sellada (València 2024-05), 1 año posterior, IPVA municipal", "ipva_tam_indice", "municipio", "2011-2023", a, d,
         len(pan), pan.t.nunique(), "municipio", 1, "sí, con una unidad tratada", "ninguna", res=res, ref_txt=ref2_txt, ref=ref2, rec="descartada",
         motivo="Moratorias: Baleares, Canarias y Madrid están selladas por K8; queda València (2024-05) con 1 unidad y 1 año posterior. Con 1 unidad tratada no hay "
                "inferencia por clusters; Barcelona (PEUAT 2017, DL 3/2023) solapa con H3/E4 y las topes de Cataluña.", tarea="")
    ge = duckdb.sql(f"SELECT count(DISTINCT territorio_codigo) n FROM read_parquet('{HECHOS}') WHERE nivel='seccion' AND territorio_codigo LIKE '08019%'").df().n[0]
    sec_bcn = pd.Series(duckdb.sql(f"SELECT DISTINCT territorio_codigo u FROM read_parquet('{HECHOS}') WHERE nivel='seccion' AND territorio_codigo LIKE '08019%'").df().u)
    n_bcn = int((~HO.unidad_sellada_v16(sec_bcn, "seccion").values).sum())
    fila("Q2", "RD espacial en los límites de zonas del PEUAT (Barcelona 2017) / PEUAT de Madrid", "geometría de zonas: no está en el repositorio", "sección", "—",
         int(ge), n_bcn, np.nan, np.nan, "", 0, "no: faltan los polígonos de zonas; Madrid (PEUAT 2019) está sellada", "ninguna", unidad="n/d", datos_ok="no",
         motivo=f"Solo hay geometría de municipios, secciones y barrios de València (data/base/geo). Barcelona conserva {n_bcn} de {ge} secciones sin sellar, pero sin "
                "polígonos de zona no se puede construir la distancia al límite; Madrid (28) está sellada entera por v6.",
         tarea="Cartografía de zonas del PEUAT de Barcelona (Ajuntament, open data) y de Madrid (en el sellado)", es_log=False)
    # shift-share con demanda turística exógena (provincial, IPC alquiler trimestral)
    ia_p = logp(leer("ipc_alquiler_indice", "provincia", "T", "q2_ipcalq_prov"), min_t=60)
    ia_p = sub(ia_p, rng)
    res = V15.placebo_continuo(ia_p, ccaa_de(ia_p.u), rng)
    a, d = info("q2_ipcalq_prov")
    fila("Q2", "Shift-share con demanda turística exógena (cuota provincial de pernoctaciones de no residentes × viajeros nacionales), IPC alquiler provincial", "ipc_alquiler_indice",
         "provincia", "2002T1-2026T2", a, d, len(ia_p), ia_p.t.nunique(), f"{ccaa_de(ia_p.u).nunique()} CCAA", 0, "sí; choque nacional único por trimestre (sin país de origen)", "debil",
         res=res, unidad="log puntos por 1 DT de exposición", ref_txt=ref2_txt, ref=ref2,
         motivo="Sin choques por país de origen el shift-share es exposición × choque común (DiD de intensidad): no hay variación de choques para AKM.", tarea="")
    an = [u for u in sp.u.unique() if u[:2] in ("04", "11", "14", "18", "21", "23", "29", "41")]
    pa = sp[sp.u.isin(an) & (sp.t >= "2015")]
    pa = pa[pa.groupby("u").t.transform("count") >= 8].reset_index(drop=True)
    pa = sub(pa, rng)
    res = V15.placebo_continuo(pa, pa.u.str[:2], rng)
    reg_and = leer("andalucia_rta_altas_acumuladas_numero", "municipio", "A", "q2_rta_andalucia", fuente="alquiler_turismo_terceros.parquet")
    a, d = info("q2_serpavi_and") if any(x["panel"] == "q2_serpavi_and" for x in EXCL) else info("q1_serpavi_mun")
    fila("Q2", "Registro autonómico de Andalucía (RTA, altas acumuladas por año) × SERPAVI municipal", "andalucia_rta_altas_acumuladas (terceros) + SERPAVI", "municipio",
         "2015-2024", a, pa.u.nunique(), len(pa), pa.t.nunique(), "8 provincias", 0, f"sí: {reg_and.u.nunique()} municipios con altas fechadas", "debil", res=res,
         unidad="log puntos por 1 DT", ref_txt=ref2_txt, ref=ref2,
         motivo="Registro andaluz con año de alta (datos de terceros, solo agregados). Solo 8 provincias como clusters: usar bootstrap salvaje con pesos de Webb.", tarea="")
    # VUT INE por municipio (1 desag. 2021-2024) × IPVA: nuevo frente a H3 (secciones SERPAVI)
    ipva24 = logp(leer("ipva_tam_indice", "municipio", "A", "q2_ipva_mun_2024", desag="tamano=Total"))
    pm = ipva24[ipva24.t >= "2021"]
    pm = pm[pm.groupby("u").t.transform("count") == 4].reset_index(drop=True)
    pm = sub(pm, rng)
    res = V15.placebo_continuo(pm, pm.u.str[:2], rng)
    a, d = info("q2_ipva_mun_2024")
    fila("Q2", "Exposición INE-VUT municipal (2021-2024) × IPVA municipal (otro resultado que H3)", "ipva_tam_indice + ine_vut_*", "municipio", "2021-2024", a, d, len(pm), 4,
         f"{pm.u.str[:2].nunique()} provincias", 0, "sí", "debil", res=res, unidad="log puntos por 1 DT", ref_txt=ref2_txt, ref=ref2,
         motivo="T = 4. Solapa con H3 en la exposición; lo nuevo es el resultado (IPVA) y la escala municipal.", tarea="")

    # =============================================================================================== Q3 inmigración
    pad = pd.read_csv(RAIZ / "data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz", dtype={"cod_municipio": str, "cod_provincia": str})
    pad["u"] = pad.cod_municipio.str.zfill(5)
    n_pad0 = pad.u.nunique()
    u_ok = pd.Series(pad.u.unique())
    u_ok = set(u_ok[~HO.unidad_sellada_v16(u_ok, "municipio").values])
    pad = pad[pad.u.isin(u_ok)]
    EXCL.append({"panel": "q3_padron_nacionalidad", "nivel": "municipio", "unidades_antes": n_pad0, "unidades_selladas_excluidas": n_pad0 - len(u_ok),
                 "unidades_despues": len(u_ok), "filas_antes": np.nan, "filas_despues": len(pad), "corte_temporal_v15": "2022 (fin del padrón por nacionalidad)"})
    agreg = pad.nacionalidad.isin(["Total", "Española", "Extranjera", "Europa (sin España)", "Oceanía y Apátridas"]) | pad.nacionalidad.str.startswith(("De ", "País de "))
    o = pad[(pad.anio == 2022) & ~agreg].groupby("nacionalidad").poblacion.sum()   # solo países, sin agregados
    s = o / o.sum()
    n_orig = int(o.size)
    hhi = float((s**2).sum())
    extra["q3_origenes"] = {"n_origenes": n_orig, "n_efectivo_1/HHI": round(1 / hhi, 2), "mayor_cuota": round(float(s.max()), 3),
                            "municipios_padron_no_sellados": len(u_ok)}
    spm = sp[(sp.t <= "2022")]
    b = spm[spm.groupby("u").t.transform("count") >= 8].reset_index(drop=True)
    b = sub(b, rng)
    res = V15.placebo_continuo(b, b.u.str[:2], rng)
    a, d = info("q1_serpavi_mun")
    fila("Q3", "Alquiler municipal (SERPAVI) con exposición shift-share padrón 2003-2022 (H4 ya la usa); aquí solo con escala de barrio ausente", "SERPAVI €/m² + padrón por nacionalidad",
         "municipio", "2011-2022", a, b.u.nunique(), len(b), b.t.nunique(), "provincias", 0, f"sí: {n_orig} orígenes, n efectivo 1/HHI = {1/hhi:.1f}", "debil", res=res,
         unidad="log puntos por 1 DT", ref_txt="sin agregado en metaanalisis.csv (no hay grupo de inmigración); ver docs/v15/literatura.md", ref=np.nan,
         motivo="Solapa con H4 (mismo diseño); lo nuevo es la separación alquiler/compra y las pruebas AKM/Rotemberg.", tarea="")
    for var, nom in (("compraventas", "compra: compraventas (volumen)"), ("valor_tasado", "compra: valor tasado (precio)")):
        d_ = logp(leer(var, "provincia", "A", f"q3_{var}_prov"), min_t=8)
        d_ = d_[d_.t <= "2022"]
        res = V15.placebo_continuo(d_, ccaa_de(d_.u), rng)
        a, d = info(f"q3_{var}_prov")
        fila("Q3", f"Demanda de compra, {nom}, provincial 2007-2022, exposición shift-share placebo", var, "provincia", "2007-2022", a, d, len(d_), d_.t.nunique(),
             f"{ccaa_de(d_.u).nunique()} CCAA", 0, "parcial: sin precio de compra municipal ni compras por nacionalidad", "debil", res=res, unidad="log puntos por 1 DT",
             ref_txt="sin agregado", ref=np.nan, motivo="Separa compra de alquiler solo a escala provincial.", tarea="Tarea 3 (compras por nacionalidad, Registradores/Notariado)")
    sc = logp(leer("serpavi_alquiler_m2_mediana", "seccion", "A", "q3_serpavi_seccion", desag="tipologia=VC", donde="periodo IN ('2021','2024')"))
    wv = sc.pivot_table(index="u", columns="t", values="y").dropna()
    dl = (wv["2024"] - wv["2021"])
    dl = dl[dl.index.str[:5].map(dl.index.str[:5].value_counts()) >= 5]
    res = V15.placebo_seccion(dl, pd.Series(dl.index.str[:5], index=dl.index), rng)
    a, d = info("q3_serpavi_seccion")
    fila("Q3", "Escala de barrio: Δlog 2021→2024 por sección, covariable placebo con componente municipal, EE por municipio", "serpavi_alquiler_m2_mediana sección",
         "sección", "2021-2024", a, d, len(dl), 2, f"{dl.index.str[:5].nunique()} municipios", 0, "parcial: padrón por sección solo 2022; el censo anual da población total", "debil",
         res=res, unidad="log puntos por 1 DT", ref_txt="sin agregado", ref=np.nan,
         motivo="Sin nacionalidad por sección y año no hay shift-share de barrio; sólo corte con exposición de 2022.", tarea="Padrón por sección y nacionalidad por año (INE, petición)")

    # =============================================================================================== Q4 oferta (tipo Saiz)
    rnv = duckdb.sql(f"SELECT DISTINCT variable FROM read_parquet('{P16/'oferta_suelo_terceros.parquet'}')").df().variable.tolist()
    vrn = [v for v in rnv if v.startswith("miteco_rn2000_porcentaje")][0]
    rn = leer(vrn, "municipio", "A", "q4_rn2000", fuente="oferta_suelo_terceros.parquet")
    a_rn, d_rn = info("q4_rn2000")
    w4 = sp.pivot_table(index="u", columns="t", values="y")
    dl4 = (w4["2024"] - w4["2015"]).dropna()
    dl4 = dl4[dl4.index.isin(rn.u)]
    res = V15.placebo_seccion(dl4, pd.Series(dl4.index.str[:2], index=dl4.index), rng)
    fila("Q4", "Elasticidad con restricciones físicas: Red Natura (único índice disponible), corte Δlog alquiler 2015→2024, EE por provincia", "serpavi + miteco_rn2000_porcentaje",
         "municipio", "2015-2024", a_rn, len(dl4), len(dl4), 2, f"{dl4.index.str[:2].nunique()} provincias", 0,
         "parcial: Red Natura y superficie sí; pendiente, costa (DPMT), SIU y CORINE no", "debil", res=res, unidad="log puntos por 1 DT", ref_txt=lit("L3_oferta_elasticidad", "^precio de la vivienda$")[0],
         ref=np.nan, motivo="Sin pendiente ni costa el índice de inelasticidad es Red Natura (planeamiento/protección), que no es exógena a la urbanización: la restricción de exclusión es débil. "
         "Además el precio municipal es de alquiler, no de compra.", tarea="Tarea 3.3 (SIU, MDT05, DPMT, CORINE)")
    pz = sp[sp.t >= "2015"]
    pz = pz[pz.u.isin(rn.u)]
    pz = pz[pz.groupby("u").t.transform("count") >= 8].reset_index(drop=True)
    pz = sub(pz, rng)
    res = placebo_interaccion(pz, pz.u.str[:2], rng, rho=0.8)
    fila("Q4", "Heterogeneidad por inelasticidad: interacción choque de demanda municipal × índice de restricción, EF unidad y año", "serpavi + rn2000", "municipio", "2015-2024", a_rn,
         pz.u.nunique(), len(pz), pz.t.nunique(), f"{pz.u.str[:2].nunique()} provincias", 0, "parcial (solo Red Natura)", "debil", res=res, unidad="log puntos por 1 DT de la interacción",
         ref_txt="sin agregado", ref=np.nan, motivo="La interacción exige un choque de demanda municipal que dependa de Q3 (T corto) y un moderador exógeno.", tarea="Tarea 3.3")
    oc = leer("obra_nueva_neta_catastro", "municipio", "A", "q4_obra_catastro")
    a, d = info("q4_obra_catastro")
    extra["q4_primera_etapa"] = {"municipios_con_obra_nueva_catastro": int(oc.u.nunique()), "municipios_con_Red_Natura": int(rn.u.nunique()),
                                 "interseccion": int(len(set(oc.u) & set(rn.u)))}

    # =============================================================================================== Q5 tipos de interés
    jk = duckdb.sql(f"SELECT periodo, valor FROM read_parquet('{P16/'demanda_internacional.parquet'}') WHERE variable='bce_jk_mp_pm_m'").df()
    jk["q"] = jk.periodo.str[:4] + "T" + ((jk.periodo.str[5:7].astype(int) - 1) // 3 + 1).astype(str)
    jkq = jk.groupby("q").valor.sum()
    for var, nom in (("p_tasado", "valor tasado"), ("ipv", "IPV"), ("compraventas", "compraventas"), ("ipc_alquiler", "IPC alquiler")):
        sr = duckdb.sql(f"SELECT periodo, valor FROM read_parquet('{HECHOS}') WHERE variable='{var}' AND nivel='nacional' AND frecuencia='T' AND valor>0 ORDER BY periodo").df().set_index("periodo").valor
        sr = sr[(sr.index >= jkq.index.min()) & (sr.index <= jkq.index.max())]
        for hh in (4, 8):
            res = V15.placebo_lp(np.log(sr), hh, rng)
            EXCL.append({"panel": f"q5_{var}", "nivel": "nacional", "unidades_antes": 1, "unidades_selladas_excluidas": 0, "unidades_despues": 1, "filas_antes": len(sr),
                         "filas_despues": len(sr), "corte_temporal_v15": ULTIMO_VISTO.get(f"{var}|nacional|T", "—")})
            fila("Q5", f"Proyección local con sorpresas de Jarociński-Karadi (placebo iid), h = {hh}", f"{nom} nacional, log + choque BCE trimestral", "nacional",
                 f"{sr.index.min()}-{sr.index.max()}", 1, 1, res["T"], res["T"], "serie única", 0, "sí en serie; exposición por peso de hipoteca variable NO (no hay por provincia)",
                 "debil", res=res, unidad="log puntos por 1 DT de sorpresa", ref_txt="sin agregado de la literatura (no hay grupo de tipos en metaanalisis.csv)", ref=np.nan,
                 motivo="Serie temporal única: sin dimensión transversal la identificación descansa solo en la exogeneidad de la sorpresa (muestra 2000-2025 con pocas sorpresas grandes).",
                 tarea="Peso de hipoteca variable por provincia/municipio (ECV/EFF/BdE); decisión sobre licencia EA-MPD (tarea 4)")
    # =============================================================================================== Q6 fiscalidad (ITP)
    iv = pd.read_csv(RAIZ / "output/v16/f1/intervenciones.csv", dtype=str)
    itp = iv[iv.instrumento == "itp"].copy()
    itp["valor"] = pd.to_numeric(itp.valor, errors="coerce")
    itp["fecha"] = pd.to_datetime(itp.fecha_efecto, errors="coerce")
    itp = itp.dropna(subset=["valor", "fecha"]).sort_values(["territorio", "fecha"])
    itp["dif"] = itp.groupby("territorio").valor.diff()
    ev = itp[(itp.dif.abs() > 0) & (itp.fecha >= "2011-01-01")]
    sellada_nom = {"Aragón", "Principado de Asturias", "Illes Balears", "Canarias", "La Rioja", "Comunidad de Madrid", "Región de Murcia", "Navarra"}
    ev_ns = ev[~ev.territorio.isin(sellada_nom)]
    ev_ns = ev_ns[ev_ns.fecha <= "2024-12-31"]
    mean_abs = float(ev_ns.dif.abs().mean())
    ref6_txt, ref6u = lit("L4_fiscalidad_compra", "^precio$")
    ref6 = ref6u * mean_abs
    extra["q6_eventos_ITP"] = {"eventos_con_cambio_no_sellados_2011_2024": int(len(ev_ns)), "ccaa_con_evento": int(ev_ns.territorio.nunique()), "cambio_medio_abs_pp": round(mean_abs, 2),
                               "eventos_totales_todas_ccaa": int(len(ev))}
    cuarts = sorted({f"{d.year}T{(d.month - 1) // 3 + 1}" for d in ev_ns.fecha if d.year <= 2023})
    for var, nom in (("compraventas", "compraventas (volumen)"), ("valor_tasado", "valor tasado (precio)")):
        d_ = logp(leer(var, "provincia", "T", f"q6_{var}_prov"), min_t=40)
        d_ = d_[d_.t <= "2024T4"].reset_index(drop=True)
        d_ = sub(d_, rng)
        ng = max(2, ev_ns.territorio.nunique())
        adop = [c for c in cuarts if c in set(d_.t)] or ["2013T1"]
        res = placebo_did_grupo(d_, ng, adop, ccaa_de(d_.u), rng)
        a, d = info(f"q6_{var}_prov")
        fila("Q6", f"DiD escalonado placebo (cambios de ITP: calendario real de {len(ev_ns)} eventos, tratamiento asignado a CCAA al azar), {nom}", var, "provincia",
             "2007T1-2024T4", a, d, len(d_), d_.t.nunique(), f"{ccaa_de(d_.u).nunique()} CCAA", ng, f"sí: {len(ev_ns)} cambios fechados en CCAA no selladas (tipo general)",
             "debil", res=res, ref_txt=ref6_txt + f"; × cambio medio {mean_abs:.1f} p.p.", ref=ref6,
             motivo="Solo ~9 CCAA no selladas como clusters: inferencia con bootstrap salvaje de Webb (los EE agrupados sobrerrechazan). Efecto sobre el ITP general; "
                    "tipos reducidos y forales no recogidos (NO VERIFICADO).", tarea="Contrastar ITP con las leyes autonómicas (secundaria hoy)")
    # =============================================================================================== Q7 ayudas a la demanda
    ecv = _cargar("atlas_v10", RAIZ / "src/v10/atlas_microdatos.py")
    anios = list(range(2018, 2026)) if not SMOKE else [2019, 2022]
    pers = []
    for an_ in anios:
        pz_ = ecv.ecv_anio(an_)
        pz_ = pz_[pz_.RB050 > 0].copy()
        pz_["ccaa"] = pz_.DB040.map(ecv.CCAA_NUTS)
        pz_["edad"] = pd.to_numeric(pz_.RB081, errors="coerce")
        pz_["tenencia"] = pd.to_numeric(pz_.HH021, errors="coerce")
        pz_["hid"] = pz_.HB030.astype(str) + "_" + str(an_)
        pers.append(pz_[["anio", "ccaa", "edad", "tenencia", "HH060", "HY070N", "RB050", "hid"]])
    ec = pd.concat(pers, ignore_index=True)
    n_tot = ec.ccaa.nunique()
    ec = ec[~ec.ccaa.isin(CCAA_V6)]
    EXCL.append({"panel": "q7_ecv_micro", "nivel": "persona (ECV)", "unidades_antes": n_tot, "unidades_selladas_excluidas": n_tot - ec.ccaa.nunique(),
                 "unidades_despues": ec.ccaa.nunique(), "filas_antes": len(ec), "filas_despues": len(ec), "corte_temporal_v15": "n/a (microdatos, no sellados temporalmente)"})
    inq = ec[(ec.tenencia == 3) & (ec.HH060 > 0) & ec.edad.between(30, 40)]
    cuenta = inq.groupby("anio").agg(personas=("hid", "size"), hogares=("hid", "nunique")).assign(
        con_ayuda_vivienda_pooled=inq.assign(a=(inq.HY070N.fillna(0) > 0)).groupby("anio").a.sum())
    cuenta.to_csv(SAL / "q7_inquilinos_30_40_por_ola.csv")
    pre = inq[inq.anio <= 2021]
    post = inq[inq.anio >= 2023]
    ventana = inq[inq.edad.between(33, 37)]
    n_pre_h = pre.hid.nunique() if not SMOKE else max(pre.hid.nunique(), 1)
    n_post_h = post.hid.nunique() if len(post) else n_pre_h
    base = ec[(ec.tenencia == 3) & (ec.HH060 > 0) & ec.edad.between(24, 46) & (ec.anio <= 2021)].copy()
    base["y"] = np.log(base.HH060)
    base["y"] -= base.groupby("anio").y.transform("mean")
    cortes = [28, 29, 30, 31, 39, 40, 41, 42]
    r = rd_placebo(base.edad.values, base.y.values, base.RB050.values / base.RB050.mean(), base.hid.values, cortes, h=4)
    esc = float(np.sqrt(max(len(pre), 1) / max(len(post), 1))) if len(post) else 1.0
    sd = r["sd_placebo"] * esc
    mean_rent = float(post.HH060.mean()) if len(post) else float(pre.HH060.mean())
    ref7 = 100 * 0.33 * 250 / mean_rent
    ref7_txt = lit("L5_ayudas_demanda", "^Alquiler de perceptores$")[0] + f"; bono 250 €/mes frente a alquiler medio ECV 30-40 de {mean_rent:.0f} €/mes (cota ITT con 100 % de cobertura)"
    extra["q7_conteos"] = {"inquilinos_mercado_30_40_por_ola": cuenta.personas.to_dict(), "hogares_30_40_pre_2018_2021": int(n_pre_h), "hogares_30_40_post_2023_2025": int(n_post_h),
                           "personas_33_37_todas_las_olas": int(len(ventana)), "factor_escala_N": round(esc, 3)}
    fila("Q7", "RD por edad 35 del bono alquiler joven (RD 42/2022): umbrales PLACEBO 28-31 y 39-42 con olas 2018-2021, escalado al N de 2023-2025", "ECV microdatos (HH060, RB081, HH021)",
         "persona (hogares inquilinos)", "2018-2025", n_tot, ec.ccaa.nunique(), len(inq), len(anios), "hogares", int(len(post)),
         "parcial: edad discreta (años), sin condición de perceptor, sin ingreso del solicitante; HY070N mide ayudas de vivienda en general",
         "debil", res={"sd_placebo": sd, "tamano_5pct": r["tamano_5pct"]}, ref_txt=ref7_txt, ref=ref7, rec="reformulada",
         motivo="OVERRIDE declarado de la regla (la referencia es una cota ITT con cobertura plena; con cobertura real el efecto esperado es menor que el MDE): reformulada. "
                f"Se cuentan {len(inq)} observaciones de inquilinos de 30-40 años en 2018-2025 ({int(len(post))} en 2023-2025); la edad de la ECV es la de 31-dic del año anterior, "
                "no la del trámite (error de medida en el umbral); el umbral no es nítido (cobertura, ingresos, renta máxima de 600 €). Los MDE son sobre log HH060 del hogar inquilino.",
         tarea="Microdatos de perceptores (MIVAU/CCAA) o convocatorias autonómicas con fechas de resolución")
    fila("Q7", "Avales ICO (2024-05, ≤35 años): incidencia en rentas/compras", "hip_n CCAA T; sin edad", "ccaa", "2024T2+", 17, 9, np.nan, 9, "CCAA", 0,
         "no: tratamiento nacional sin variación entre CCAA ni edad en la base", "ninguna", unidad="n/d", datos_ok="no",
         motivo="El convenio es estatal (adhesión autonómica posterior sin fechas en la base); hip_n no distingue edad. Sin grupo de control.",
         tarea="Adhesión de cada CCAA al aval y edad del prestatario (ICO/Banco de España)", es_log=False)
    # =============================================================================================== Q8 golden visa
    rx = leer("registradores_extranj_pct", "ccaa", "A", "q8_registradores_extranj_ccaa")
    a, d = info("q8_registradores_extranj_ccaa")
    fila("Q8", "Fin de la golden visa (LO 1/2025, 2025-04-03): compras de extracomunitarios frente a comunitarios", "registradores_extranj_pct (CCAA, A); notariado_cgn_extranj; sin nacionalidad",
         "ccaa", f"{rx.t.min()}-{rx.t.max()}", a, d, len(rx), rx.t.nunique(), "CCAA", 0, "no: no hay compras por nacionalidad ni golden visa (OPI) en la base", "ninguna", unidad="n/d", datos_ok="no",
         motivo="La base solo trae el % de compras de extranjeros sin distinguir UE/no UE (CCAA anual y nacional trimestral); la serie de autorizaciones por nacionalidad (OPI) no está "
                "descargada y Notariado prohíbe la transformación. Post-tratamiento: ≤ 5 trimestres. Sin control posible.",
         tarea="Tarea 3.2 (OPI, golden visa por nacionalidad y año); permiso de Registradores/Notariado para compras por nacionalidad", es_log=False)
    # =============================================================================================== Q9 fundamentales y burbuja
    vt = logp(leer("valor_tasado", "provincia", "T", "q9_valor_tasado_prov"), min_t=60)
    ia_ = logp(leer("ipc_alquiler_indice", "provincia", "T", "q9_ipc_alquiler_prov"), min_t=60)
    piv = vt.pivot_table(index="t", columns="u", values="y")
    pir = ia_.pivot_table(index="t", columns="u", values="y")
    com = sorted(set(piv.columns) & set(pir.columns))
    ratio = (piv[com] - pir[com]).dropna(how="any")
    N9, T9 = ratio.shape[1], ratio.shape[0]
    a, d = info("q9_valor_tasado_prov")
    cips = mc_cips(N9, T9, rng)
    gs = mc_gsadf(T9, rng)
    extra["q9_cips"] = cips
    extra["q9_gsadf"] = gs
    fila("Q9", "CIPS/Pesaran y Westerlund en panel de precio/alquiler (razón de índices) con dependencia transversal; potencia por Monte Carlo", "valor_tasado / ipc_alquiler_indice provincial",
         "provincia", f"{ratio.index.min()}-{ratio.index.max()}", a, N9, N9 * T9, T9, "N provincias", 0, "sí (razón de índices; no nivel de renta ni coste de uso por provincia)",
         "adecuada", mde=cips["rho_min_detectable_80"], unidad=f"ρ mínimo detectable (vida media {cips['vida_media_trimestres']} trimestres); rechazo nulo={cips['tamano_5pct']}",
         ref_txt="sin magnitud comparable (contraste de raíz unitaria)", ref=np.nan, es_log=False,
         motivo=f"Tamaño simulado {cips['tamano_5pct']} al 5 % con N={N9}, T={T9}: usar valores críticos propios (bootstrap), no los tabulados. Contraste de estacionariedad de la razón; la razón de índices no es la razón de niveles (falta el nivel de alquiler provincial).", tarea="Nivel de alquiler provincial (SERPAVI provincial 2011-2024 como alternativa)")
    fila("Q9", "GSADF por provincia (burbuja explosiva); potencia con episodio de 20 trimestres", "mismo panel", "provincia", f"{ratio.index.min()}-{ratio.index.max()}", a, N9, N9 * T9, T9,
         "N provincias", 0, "sí", "adecuada", mde=gs["rho_min_detectable_80"], unidad=f"ρ explosivo mínimo detectable (por provincia, α=5 %); potencia Bonferroni {gs['potencia_bonferroni']}",
         ref_txt="sin magnitud comparable", ref=np.nan, es_log=False, rec="reformulada",
         motivo="Ningún ρ de 1,01 a 1,05 alcanza el 80 % por territorio (a ρ=1,05: " + str(round(gs["potencia_por_rho"][1.05], 2)) + "; con Bonferroni " + str(round(gs["potencia_bonferroni_por_rho"][1.05], 2)) + "): reformulada como GSADF agregado sobre el factor común. Con T pequeño solo se detectan episodios largos y fuertes; con corrección por N territorios (BH/Bonferroni) la potencia baja.", tarea="")
    # =============================================================================================== Q10 predicción
    for var, nom in (("p_tasado", "valor tasado (solapa H5)"), ("ipv", "IPV"), ("ipc_alquiler", "IPC alquiler"), ("compraventas", "compraventas")):
        sr = duckdb.sql(f"SELECT periodo, valor FROM read_parquet('{HECHOS}') WHERE variable='{var}' AND nivel='nacional' AND frecuencia='T' AND valor>0 ORDER BY periodo").df().set_index("periodo").valor
        y = np.log(sr)
        ini = int(max(24, len(y) * 0.4))
        e = V15.ar4_errores(y, inicio=ini)
        for hh in (1, 4):
            eh = e[::hh]
            for rho in (0.9, 0.7):
                rr = V15.mde_dm(eh, rng, rho) if not SMOKE else float("nan")
                fila("Q10", f"DM-HLN frente a AR(4), h = {hh} (errores no solapados), ρ = {rho}", f"{nom}, Δlog", "nacional", f"{y.index[ini]}-{y.index[-1]}", 1, 1, len(eh), len(eh),
                     "serie única", 0, "sí", "adecuada", mde=rr, unidad="reducción relativa mínima del ECM (detectable al 80 %)", ref_txt="ningún modelo bate al AR(4) (v1, K1, V8)", ref=np.nan,
                     es_log=False, motivo=(f"{len(eh)} errores recursivos. Conformal 90 %: error típico de cobertura ±{100*np.sqrt(0.09/max(len(eh),1)):.1f} p.p. con esa calibración. "
                                           "MIDAS y nowcasting con indicadores adelantados no cambian T." if hh == 1 and rho == 0.9 else ""), tarea="")
    # =============================================================================================== exportar
    exportar(extra)
    return 0


# ------------------------------------------------------------------------------------------------------ Monte Carlo (Q9)
def _cadf_t(Y: np.ndarray) -> np.ndarray:
    T, N = Y.shape
    dy = np.diff(Y, axis=0)
    ybar = Y.mean(axis=1)
    out = np.empty(N)
    for i in range(N):
        X = np.column_stack([np.ones(T - 1), Y[:-1, i], ybar[:-1], np.diff(ybar)])
        b, *_ = np.linalg.lstsq(X, dy[:, i], rcond=None)
        e = dy[:, i] - X @ b
        s2 = e @ e / (T - 1 - 4)
        out[i] = b[1] / np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    return out


def _panel_sim(N, T, rho, rng):
    lam = rng.normal(1, 0.5, N)
    f = np.cumsum(rng.standard_normal(T + 50))
    e = np.zeros((T + 50, N))
    z = rng.standard_normal((T + 50, N))
    for t in range(1, T + 50):
        e[t] = rho * e[t - 1] + z[t]
    return (f[:, None] * lam[None, :] + e)[50:]


def mc_cips(N: int, T: int, rng) -> dict:
    nul = np.array([np.mean(np.clip(_cadf_t(_panel_sim(N, T, 1.0, rng)), -6.19, 2.61)) for _ in range(MC)])
    crit = np.quantile(nul, 0.05)
    # tamaño: segunda tanda independiente
    nul2 = np.array([np.mean(np.clip(_cadf_t(_panel_sim(N, T, 1.0, rng)), -6.19, 2.61)) for _ in range(MC)])
    pot = {}
    for rho in (0.99, 0.98, 0.97, 0.95, 0.92, 0.90):
        st = np.array([np.mean(np.clip(_cadf_t(_panel_sim(N, T, rho, rng)), -6.19, 2.61)) for _ in range(MC)])
        pot[rho] = float(np.mean(st < crit))
    ok = [r for r, p in pot.items() if p >= 0.8]
    rmin = max(ok) if ok else float("nan")
    return {"N": N, "T": T, "potencia_por_rho": pot, "valor_critico_5pct": round(float(crit), 3), "tamano_5pct": round(float(np.mean(nul2 < crit)), 3),
            "rho_min_detectable_80": rmin, "vida_media_trimestres": None if np.isnan(rmin) else round(float(np.log(0.5) / np.log(rmin)), 1), "reps": MC}


def _gsadf(y: np.ndarray, w0: int) -> float:
    x, z = y[:-1], np.diff(y)
    cs = lambda a: np.concatenate([[0], np.cumsum(a)])
    Sx, Sz, Sxx, Sxz, Szz = cs(x), cs(z), cs(x * x), cs(x * z), cs(z * z)
    n_all = len(x)
    best = -np.inf
    for e in range(w0, n_all + 1):
        s = np.arange(0, e - w0 + 1)
        n = e - s
        sx, sz, sxx, sxz, szz = Sx[e] - Sx[s], Sz[e] - Sz[s], Sxx[e] - Sxx[s], Sxz[e] - Sxz[s], Szz[e] - Szz[s]
        den = n * sxx - sx**2
        b = (n * sxz - sx * sz) / den
        a = (sz - b * sx) / n
        sse = szz - 2 * a * sz - 2 * b * sxz + n * a**2 + 2 * a * b * sx + b**2 * sxx
        se = np.sqrt(np.maximum(sse, 1e-12) / (n - 2) * n / den)
        best = max(best, float(np.max(b / se)))
    return best


def mc_gsadf(T: int, rng) -> dict:
    w0 = int(np.floor(T * (0.01 + 1.8 / np.sqrt(T))))
    reps = MC * 2 if not SMOKE else 40
    nul = np.array([_gsadf(np.cumsum(rng.standard_normal(T)), w0) for _ in range(reps)])
    c05, cb = np.quantile(nul, 0.95), np.quantile(nul, 1 - 0.05 / 35)
    pot, potb = {}, {}
    for rho in (1.01, 1.02, 1.03, 1.05):
        s5, sb = [], []
        for _ in range(MC if not SMOKE else 20):
            e = rng.standard_normal(T)
            y = np.zeros(T)
            t0 = int(rng.integers(T // 4, T - 25))
            for t in range(1, T):
                y[t] = (rho * y[t - 1] if t0 <= t < t0 + 20 else y[t - 1]) + e[t]
            g = _gsadf(y, w0)
            s5.append(g > c05)
            sb.append(g > cb)
        pot[rho], potb[rho] = float(np.mean(s5)), float(np.mean(sb))
    ok = [r for r, p in pot.items() if p >= 0.8]
    return {"T": T, "ventana_minima": w0, "valor_critico_5pct": round(float(c05), 3), "valor_critico_bonferroni_35": round(float(cb), 3),
            "potencia_por_rho": pot, "potencia_bonferroni_por_rho": potb, "rho_min_detectable_80": min(ok) if ok else float("nan"),
            "potencia_bonferroni": potb.get(min(ok)) if ok else float("nan"), "reps_nulo": reps}


# ------------------------------------------------------------------------------------------------------------ rejilla
def rejilla() -> pd.DataFrame:
    resultados = {
        "alquiler": ["serpavi_alquiler_m2_mediana", "serpavi_alquiler_mes_mediana", "serpavi_n_contratos_recuento", "ipva_tam_indice", "ipva_indice", "ipc_alquiler_indice", "ipc_alquiler",
                     "incasol_renta_media", "incasol_contratos", "emal_renta_mensual_eur", "fianzas_importe_mediana"],
        "compra": ["valor_tasado", "p_tasado", "ipv", "ipva", "notariado_cuantia_media_esp"],
        "volumen": ["compraventas", "hip_n", "hip_importe"],
        "oferta": ["iniciadas", "terminadas", "obra_nueva_neta_catastro", "visados"],
        "tension": ["cgpj_lanzamientos_total_numero", "cgpj_lanzamientos_lau_numero", "cgpj_ejecuciones_hipotecarias_numero"],
    }
    todas = [v for lst in resultados.values() for v in lst]
    lista = ",".join(f"'{v}'" for v in todas)
    inv = []
    for fuente in (HECHOS, P16 / "tension_social_terceros.parquet"):
        inv.append(duckdb.sql(f"""SELECT variable, nivel, count(DISTINCT territorio_codigo) FILTER (WHERE NOT coalesce(muestra_sellada_v6,false)) AS u
                                  FROM read_parquet('{fuente}') WHERE variable IN ({lista}) GROUP BY 1,2""").df())
    inv = pd.concat(inv)
    inv = inv[inv.u > 0]
    cat_ = {v: k for k, lst in resultados.items() for v in lst}
    dims = {"regulación del alquiler (Q1)": ["municipio", "provincia", "ccaa"], "vivienda turística (Q2)": ["seccion", "distrito", "municipio", "provincia", "ccaa"],
            "inmigración (Q3)": ["seccion", "municipio", "provincia"], "oferta y restricciones (Q4)": ["municipio"], "tipos de interés (Q5)": ["nacional"],
            "fiscalidad de la compra (Q6)": ["provincia", "ccaa"], "ayudas a la demanda (Q7)": ["nacional", "ccaa"], "demanda internacional (Q8)": [],
            "fundamentales y burbuja (Q9)": ["provincia", "ccaa", "nacional"]}
    filas = []
    for dim, escalas in dims.items():
        for esc in escalas:
            for _, r in inv[inv.nivel == esc].iterrows():
                filas.append({"dimension": dim, "escala": esc, "resultado": r.variable, "familia_resultado": cat_[r.variable], "unidades_no_selladas": int(r.u)})
    return pd.DataFrame(filas).drop_duplicates()


def exportar(extra: dict) -> None:
    t = pd.DataFrame(FILAS)[COLS]
    t.to_csv(SAL / "potencia.csv", index=False)
    pd.DataFrame(EXCL).to_csv(SAL / "exclusiones.csv", index=False)
    g = rejilla()
    g.to_csv(SAL / "rejilla_candidata.csv", index=False)
    prior = {"Q1": ["H1", "H2"], "Q2": ["H3", "E4"], "Q3": ["H4"], "Q9": ["E1"], "Q10": ["H5"]}
    orden = {"confirmatoria": 0, "exploratoria (BH)": 1, "reformulada": 2, "descartada": 3}
    resumen = {}
    for q, x in t.groupby("pregunta"):
        mejor = min(x.recomendacion, key=lambda r: orden[r])
        m = x[x.recomendacion == mejor]
        mm = m.mde80_pct.dropna()
        resumen[q] = {"recomendacion_global": mejor, "mde80_pct_mejor_subdiseno": None if mm.empty else float(mm.min()), "subdisenos": int(len(x))}
    n_ok = {k: int(v) for k, v in pd.DataFrame(EXCL).groupby("panel").unidades_despues.max().items()}
    (SAL / "resultado.json").write_text(json.dumps({
        "rama": "v16-f4-potencia", "pregunta": "Potencia y efecto mínimo detectable (MDE80) de Q1-Q10 con los datos nuevos, antes del pre-registro", "capa": "C4",
        "datos": "data/base/hechos.parquet + data/processed/v16/*.parquet (incl. *_terceros agregados) + ECV microdatos; sin muestras selladas (v6, V15, V16)",
        "N": int(len(t)), "metodo": f"aleatorización placebo ({REPS} réplicas), SEED={SEED}; MDE80 = 2,8 × DT placebo; RD con umbrales placebo; Monte Carlo CIPS/GSADF ({MC} réplicas); DM-HLN por simulación",
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {"unidades_tras_exclusiones": n_ok, "resumen_por_pregunta": resumen, "extra": extra, "smoke": SMOKE},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Ningún efecto ni asociación real estimados. Tratamientos placebo; solo unidades no tratadas y periodos previos en regulaciones; umbrales RD placebo."},
        ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    informe(t, extra, g, resumen)
    REG.flush()
    print(t[["pregunta", "subdiseno", "n_unidades_despues", "mde80", "mde80_pct", "rechazo_placebo_5pct", "recomendacion"]].to_string(max_colwidth=60))


def informe(t, extra, g, resumen) -> None:
    ex = pd.DataFrame(EXCL)
    L = ["# V16 · Potencia y MDE de Q1-Q10 (fase 4.1)", "",
         f"Generado por `python3 src/v16/f4_potencia.py` (SEED={SEED}, {REPS} réplicas placebo). Capa C4, nivel DESCRIPTIVO. **No se ha estimado ningún efecto ni asociación real**: "
         "tratamientos y exposiciones placebo independientes del resultado; en regulaciones solo unidades no tratadas y periodos previos; umbrales RD placebo. "
         "MDE80 = 2,8 × DT placebo; «rechazo placebo» debería rondar 0,05 (se acepta ≤ 0,075).", "",
         "## Exclusiones (declaradas)",
         "Nunca se lee data/sealed. Fuera: filas muestra_sellada_v6; unidades de `holdout.unidad_sellada_v16` (v6 + V15 + V16); las 8 CCAA selladas por v6 en los paneles de CCAA (K8); "
         "periodos posteriores al último visto de V15; filas posterior_prereg. Unidades que quedan por panel en [exclusiones.csv](exclusiones.csv):", "",
         "| panel | nivel | antes | selladas | quedan |", "|---|---|---|---|---|"]
    for _, r in ex.iterrows():
        L.append(f"| {r.panel} | {r.nivel} | {r.unidades_antes} | {r.unidades_selladas_excluidas} | {r.unidades_despues} |")
    L += ["", "## Resumen por pregunta", "", "| Q | MDE80 (mejor subdiseño) | magnitud de la literatura | recomendación global |", "|---|---|---|---|"]
    for q, r in resumen.items():
        x = t[t.pregunta == q]
        refs = x.ref_pct.dropna()
        L.append(f"| {q} | {'—' if r['mde80_pct_mejor_subdiseno'] is None else str(round(r['mde80_pct_mejor_subdiseno'], 2)) + ' %'} | "
                 f"{'sin agregado' if refs.empty else str(round(refs.iloc[0], 2)) + ' %'} | {r['recomendacion_global']} |")
    L += ["", "## Detalle por subdiseño (potencia.csv)", ""]
    for _, r in t.iterrows():
        L.append(f"- **{r.pregunta} · {r.subdiseno}** — datos: {r.datos}; nivel {r.nivel}; {r.periodo}; unidades {r.n_unidades_antes}→{r.n_unidades_despues}; T={r['T']}; "
                 f"clusters {r.clusters}; construible: {r.construible}; identificación {r.identificacion}. MDE80 = {r.mde80} {r.unidad_mde}"
                 f"{'' if pd.isna(r.mde80_pct) else f' (≈ {r.mde80_pct} %)'}; rechazo placebo {r.rechazo_placebo_5pct}. Literatura: {r.referencia_literatura} → {r.mde_vs_literatura}. "
                 f"**{r.recomendacion}.** {r.motivo} {('Desbloquea: ' + r.tarea_autor) if r.tarea_autor else ''}")
    L += ["", "## Hallazgos de construcción de datos (conteos, sin resultados)"]
    for k, v in extra.items():
        L.append(f"- `{k}`: {json.dumps(v, ensure_ascii=False, default=str)}")
    L += ["", "## (i) Rejilla multiescala candidata para el control de falsos descubrimientos",
          f"Celdas escala × dimensión × resultado con datos no sellados: **{len(g)}** ([rejilla_candidata.csv](rejilla_candidata.csv)); "
          f"{g.escala.nunique()} escalas, {g.dimension.nunique()} dimensiones, {g.resultado.nunique()} resultados distintos. Es el denominador mínimo de BH jerárquico "
          "(se multiplica por ventanas y especificaciones en el pre-registro; el tope del multiverso es 50.000).", "",
          g.groupby("escala").size().rename("celdas").to_frame().to_markdown(), "",
          "## (ii) Solape con V15 (qué es nuevo y qué solapa)", "",
          "| Q | V15 | Nuevo (datos / diseño / resultado) | Solapa |", "|---|---|---|---|",
          "| Q1 | H1, H2 | Diseño (RD en umbrales legales; SDID/ASCM con donantes de otras CCAA); resultado (IPVA, venta, precio de compra) | Mismas ZT y SERPAVI/Incasòl |",
          "| Q2 | H3, E4 | Datos (Inside Airbnb, registro de Andalucía); diseño (DiD con moratorias, RD espacial, shift-share) | Exposición INE-VUT y SERPAVI de H3 |",
          "| Q3 | H4 | Resultado (compra frente a alquiler), escala (barrio), inferencia (AKM, Rotemberg) | Exposición shift-share y padrón 2003-2022 |",
          "| Q4 | — (P1 descartada por V15) | Datos (Red Natura, superficie) y diseño (interacción) | — |",
          "| Q5 | — (P3 en la fase de potencia) | Datos (sorpresas JK), diseño (LP/SVAR-IV) | Series nacionales de precio |",
          "| Q6 | — | Datos (calendario ITP) y diseño (DiD escalonado) | — |",
          "| Q7 | — | Datos (ECV) | — |", "| Q8 | — | — | — |",
          "| Q9 | E1 | Diseño (CIPS, Westerlund, CS-ARDL, GSADF por territorio) | Panel provincial de precio/alquiler |",
          "| Q10 | H5 | Modelos (MIDAS, nowcasting, conformal), objetivos (IPV, IPC alquiler, compraventas) | AR(4) y valor tasado nacional |"]
    (SAL / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
