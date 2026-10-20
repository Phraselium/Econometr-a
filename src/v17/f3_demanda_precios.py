"""V17 · Fase 3 · Auditoría del grupo «demanda_precios». ANÁLISIS A POSTERIORI (capa C4).

Pruebas mínimas de las filas turisticos, inmigracion, tipos, burbuja, alquiler y precio, y apoyo a la pregunta D3-1
(docs/v17/plan.md, fase 3, punto 2). Contabilidad, distribuciones, cotas e ilustraciones con parámetros de la literatura:
nada de lo calculado aquí es un efecto causal.

Determinista, sin red, SEED = 20261010. De la base (data/base/hechos.parquet) solo se usan filas con
muestra_sellada_v6 = False: toda distribución por sección, municipio o provincia EXCLUYE las provincias selladas. No se lee
data/sealed ni se ejecuta evaluate_*. data/raw se lee en solo lectura. Cruces territoriales solo por código INE (V7).
Las cifras de documento (Banco de España, BCE, literatura) se toman de docs/v17/referencias/ y de las fichas de literatura de
V15 y V16; no se recalculan. Inside Airbnb: solo agregados propios con atribución (CC BY 4.0).
Uso: python3 src/v17/f3_demanda_precios.py  ->  output/v17/auditoria/demanda_precios_hechos.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from holdout import excluir_sellados_v6  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "v17" / "auditoria"
BASE = ROOT / "data/base/hechos.parquet"
TERR = ROOT / "data/base/territorios.parquet"
NAC = ROOT / "data/processed/v8/nacional_q_v8.csv"
SI = ROOT / "data/raw/v17/credito/bde_si_1_5.csv"
PB = ROOT / "output/v3/PB/tablas/b1_nacional_sensibilidad.csv"
D3 = ROOT / "output/v17/d3"
INFER = {"series": ROOT / "output/v17/lectura_bde/series_v8_v9_v12/inferencia.csv",
         "micro": ROOT / "output/v17/lectura_bde/v15_v16_micro/inferencia.csv"}
MC_GSADF = ROOT / "output/v16/montecarlo/gsadf_factor/resultado.json"
H3 = ROOT / "output/v15/p5/resultado.json"
FICHAS = "output/v17/auditoria/filas"
PREG = "output/v17/auditoria/preguntas"

# Cifras de documento (fuente en cada hecho). No se recalculan.
DOC = {
    # Garcia-López et al. (2019/2020), versión de trabajo MPRA 96131, cuadro 4 y sección 3.4:
    "gl_rent_dens": 0.68,    # % de alquiler por punto de anuncios sobre viviendas (col. 3; e.e. 0,5: no significativo)
    "gl_rent_alto": 1.40,    # % por punto implícito en el decil alto (7 % de alquiler con ≈ 5 % de viviendas anunciadas)
    "gl_ptrans_dens": 3.9,   # % de precio de transacción por punto (col. 3)
    "gl_dens_media": 1.57,   # anuncios sobre viviendas, media de 4T2016 (%)
    "gl_dens_alta": 5.0,     # decil alto (≈ 5 % de las viviendas)
    # Tipos (zona euro): semielasticidad del precio a +1 pp del tipo hipotecario, a unos dos años
    "bce_semi": -5.0,
    "bce_semi_nl": -9.0,     # BCE, Boletín Económico 6/2022, estimación no lineal con tipos bajos        # BCE, Boletín Económico 6/2022 (proyecciones locales, lineal)
    "calza_semi": -2.3,      # Calza, Monacelli y Stracca (2013), reescalado por Williams (2015)
    "williams_semi": -6.3,   # Williams (2015), con Jordà, Schularick y Taylor (2015)
    "bde_con_hipoteca_2025": 52.0,  # % de compras con hipoteca (BdE IA2025, p. 124)
    "bde_no_residentes": 7.4,       # % de compras 2021-2025 (BdE IA2025, p. 149)
    "bde_pj": 10.0,                 # % de compras por personas jurídicas 2025 (BdE IA2025, p. 123)
    # Inmigración
    "go_pob": 1.5, "go_precio": 2.0,  # González y Ortega (2013): +1,5 % anual de población en edad de trabajar, +2 % anual de precio
    "saiz_elast": 1.0,                # Saiz (2007): entrada del 1 % de la población -> alquiler ≈ +1 %
}
HECHOS: list[dict] = []


def hecho(id_, indicador, valor, unidad, periodo, fuentes, lectura, ficha, minimo=None, maximo=None, nota="", pregunta=False):
    assert lectura in ("OF", "hecho", "cota", "asociación", "juicio experto", "juicio experto (calibración)")
    f = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)
    HECHOS.append({"id": f"V17-AUD-DP-{id_}", "indicador": indicador, "valor": f(valor), "min": f(minimo), "max": f(maximo),
                   "unidad": unidad, "periodo": periodo, "fuentes": fuentes, "capa": "C4", "lectura_v17": lectura,
                   "ficha": f"{PREG if pregunta else FICHAS}/{ficha}.md", "nota": "a posteriori" + (f"; {nota}" if nota else "")})


def base(sql_where: str) -> pd.DataFrame:
    """Lee la base SIN la muestra sellada v6: filtro de la base y guarda de fuga v6 (holdout.excluir_sellados_v6, K5),
    que también excluye las CCAA selladas y sus provincias, municipios, distritos y secciones."""
    d = duckdb.sql(f"select territorio_codigo c, nivel, variable v, periodo p, valor from '{BASE}' "
                   f"where {sql_where} and not muestra_sellada_v6").df()
    partes = [excluir_sellados_v6(g, "c", n) for n, g in d.groupby("nivel")]
    return pd.concat(partes) if partes else d


def pct(s: pd.Series, qs=(0.5, 0.9, 0.99)) -> list[float]:
    return [float(s.quantile(q)) for q in qs]


def pct_pond(x: pd.Series, w: pd.Series, qs=(0.5, 0.9, 0.99)) -> list[float]:
    o = np.argsort(x.values)
    cw = np.cumsum(w.values[o]) / w.sum()
    return [float(x.values[o][min(np.searchsorted(cw, q), len(o) - 1)]) for q in qs]


def media_anual(n: pd.DataFrame, col: str, anio: int) -> float:
    return float(n.loc[n.trimestre.str[:4] == str(anio), col].mean())


# ---------------------------------------------------------------- turísticos
def turisticos() -> dict:
    fi = "turisticos"
    pb = pd.read_csv(PB).drop_duplicates(["periodo", "stock"]).set_index(["periodo", "stock"])
    r = pb.loc[("2020M08-2024M08", "censo2021")]
    r_ecv = pb.loc[("2020M08-2024M08", "ECV2021xECP")]
    fu_pb = "output/v3/PB/tablas/b1_nacional_sensibilidad.csv (INE VUT total nacional; Censo 2021 y ECV 2021 × ECP)"
    hecho("TUR-NAC-AUMENTO-2020-2024", "Aumento de viviendas turísticas 2020M08-2024M08 sobre el parque de alquiler (reproduce B4-v3-vut-cantidad)",
          r.cota_cantidad_pct, "% del parque de alquiler", "2020M08-2024M08", fu_pb, "cota", fi, minimo=r_ecv.cota_cantidad_pct,
          maximo=r.cota_cantidad_pct, nota="numerador = AUMENTO de viviendas turísticas (81.771), no su número; min = denominador ECV")
    hecho("TUR-NAC-STOCK-2024M08", "Viviendas turísticas (stock) sobre el parque de alquiler, España",
          r.peso_alquiler_pct, "% del parque de alquiler", "2024M08", fu_pb, "hecho", fi, minimo=r_ecv.peso_alquiler_pct,
          maximo=r.peso_alquiler_pct, nota=f"403.267 viviendas turísticas; denominador Censo 2021 ({r.stock_alquiler:,.0f}); min = denominador ECV")
    # Febrero de 2024 (mismo mes que el cuadro A.3 del DO 2432) y último dato, desde la base nacional
    nac = duckdb.sql(f"select periodo p, valor from '{BASE}' where variable='vut_viviendas' and nivel='nacional'").df().set_index("p").valor
    st = float(r.stock_alquiler)
    hecho("TUR-NAC-STOCK-2024M02", "Viviendas turísticas (stock, feb. 2024) sobre viviendas principales en alquiler (Censo 2021), España",
          100 * nac["2024T1"] / st, "% del parque de alquiler", "2024M02", "INE VUT (vut_viviendas, 2024T1 = feb. 2024); Censo 2021",
          "hecho", fi, nota="coincide con la fila «Total España» (11,8 %) del cuadro A.3 de BdE DO 2432: mismo numerador y denominador")
    hecho("TUR-NAC-STOCK-2026M05", "Viviendas turísticas (stock, may. 2026) sobre el parque de alquiler (Censo 2021), España",
          100 * nac["2026T2"] / st, "% del parque de alquiler", "2026M05", "INE VUT; Censo 2021", "hecho", fi)
    res = {"nac_aumento": float(r.cota_cantidad_pct), "nac_stock": float(r.peso_alquiler_pct), "nac_stock_ecv": float(r_ecv.peso_alquiler_pct),
           "nac_feb24": 100 * nac["2024T1"] / st, "nac_may26": 100 * nac["2026T2"] / st}

    # Secciones censales (sin muestra sellada v6)
    d = base("nivel='seccion' and variable in ('ine_vut_vivienda_turistica','censo2021_t20_2','censo2021_t19_1',"
             "'censo2021_t19_2','iab_n_entire_home') and (variable<>'ine_vut_vivienda_turistica' or periodo in ('2021-08','2024-08','2026-05'))")
    w = d.pivot_table(index="c", columns=["v", "p"], values="valor")
    w.columns = [f"{a}|{b}" for a, b in w.columns]
    alq = w["censo2021_t20_2|2021"]
    viv = w["censo2021_t19_1|2021"] + w["censo2021_t19_2|2021"]
    vut = w["ine_vut_vivienda_turistica|2024-08"]
    ok = vut.notna() & alq.notna() & (alq > 0)
    x = 100 * vut[ok] / alq[ok]
    xv = 100 * vut[ok] / viv[ok]
    p = pct(x)
    pw = pct_pond(x, alq[ok])
    fu = "INE, viviendas turísticas por sección (experimental, 2024M08); Censo 2021, indicadores por sección (t20_2 alquiler; t19 viviendas)"
    n_sec = int(ok.sum())
    for q, v_, vw in zip(("P50", "P90", "P99"), p, pw):
        hecho(f"TUR-SEC-{q}", f"Viviendas turísticas sobre viviendas principales en alquiler, {q} de las secciones censales",
              v_, "% del parque de alquiler de la sección", "2024M08", fu, "hecho", fi,
              nota=f"{n_sec} secciones sin muestra sellada v6 con código 2021 coincidente; {q} ponderado por el parque de alquiler: {vw:.1f} %")
    hecho("TUR-SEC-AGREGADO", "Viviendas turísticas sobre el parque de alquiler, suma de las secciones no selladas",
          100 * vut[ok].sum() / alq[ok].sum(), "% del parque de alquiler", "2024M08", fu, "hecho", fi)
    sh = {u: 100 * alq[ok][x > u].sum() / alq[ok].sum() for u in (10, 25, 50, 100)}
    hecho("TUR-SEC-ALQ-EN-ALTA", "Parte del parque de alquiler situada en secciones con más viviendas turísticas que el 25 % de su alquiler",
          sh[25], "% del parque de alquiler", "2024M08", fu, "hecho", fi, minimo=sh[50], maximo=sh[10],
          nota=f"min = umbral 50 %; max = umbral 10 %; con umbral 100 % (más turísticas que alquiladas): {sh[100]:.1f} %")
    pv = pct(xv)
    hecho("TUR-SEC-VIV-P90", "Viviendas turísticas sobre el total de viviendas de la sección, P90", pv[1], "% de las viviendas", "2024M08", fu,
          "hecho", fi, minimo=pv[0], maximo=pv[2], nota="min = P50; max = P99 (escala comparable a la de Garcia-López et al., anuncios sobre viviendas)")
    # Aumento local 2021M08-2024M08 sobre el alquiler (análogo local de la cota de 2,7 %)
    v21 = w["ine_vut_vivienda_turistica|2021-08"]
    ok2 = ok & v21.notna()
    dx = 100 * (vut[ok2] - v21[ok2]) / alq[ok2]
    pd_ = pct(dx)
    hecho("TUR-SEC-AUMENTO-P90", "Aumento de viviendas turísticas 2021M08-2024M08 sobre el alquiler de la sección, P90", pd_[1],
          "% del parque de alquiler de la sección", "2021M08-2024M08", fu, "cota", fi, minimo=pd_[0], maximo=pd_[2],
          nota="min = P50; max = P99; análogo local de la cota nacional de sustitución uno a uno (no es efecto en precio)")
    # Último dato (may. 2026)
    v26 = w["ine_vut_vivienda_turistica|2026-05"]
    ok3 = v26.notna() & alq.notna() & (alq > 0)
    p26 = pct(100 * v26[ok3] / alq[ok3])
    hecho("TUR-SEC-P90-2026M05", "Viviendas turísticas sobre el alquiler de la sección, P90, último dato", p26[1], "% del parque de alquiler de la sección",
          "2026M05", fu.replace("2024M08", "2026M05"), "hecho", fi, minimo=p26[0], maximo=p26[2], nota="min = P50; max = P99")
    res.update(sec=p, sec_pond=pw, sec_viv=pv, sec_alta=sh, sec_aum=pd_, sec26=p26, n_sec=n_sec,
               sec_agregado=100 * vut[ok].sum() / alq[ok].sum())

    # Municipios: suma de secciones por código INE (5 primeros dígitos)
    m = pd.DataFrame({"vut": vut[ok], "alq": alq[ok], "viv": viv[ok]})
    m["mun"] = m.index.str[:5]
    m = m.groupby("mun").sum()
    m["x"] = 100 * m.vut / m.alq
    pm = pct(m.x)
    big = m[m.alq >= 5000]
    pb_ = pct(big.x)
    hecho("TUR-MUN-P90", "Viviendas turísticas sobre el alquiler del municipio, P90 de los municipios", pm[1], "% del parque de alquiler del municipio",
          "2024M08", fu + "; suma de secciones por código INE", "hecho", fi, minimo=pm[0], maximo=pm[2],
          nota=f"min = P50; max = P99; {len(m)} municipios; con 5.000 viviendas en alquiler o más ({len(big)} municipios): P50 {pb_[0]:.1f}, P90 {pb_[1]:.1f}, P99 {pb_[2]:.1f} %")
    t = duckdb.sql(f"select territorio_codigo mun, nombre from '{TERR}' where nivel='municipio'").df().set_index("mun").nombre
    top = big.sort_values("x", ascending=False).head(8)
    res.update(mun=pm, mun_big=pb_, n_mun=len(m), n_big=len(big),
               top=[(t.get(i, i), float(r_.x), int(r_.alq)) for i, r_ in top.iterrows()])
    for cod, nom in (("28079", "MADRID"), ("08019", "BARCELONA"), ("46250", "VALENCIA"), ("41091", "SEVILLA"), ("29067", "MALAGA")):
        if cod in m.index:
            res.setdefault("ciudades", {})[nom] = float(m.loc[cod, "x"])

    # Inside Airbnb (anuncios de vivienda completa, sep. 2026) sobre el alquiler de la sección
    iab = w["iab_n_entire_home|2026-09"]
    ok4 = iab.notna() & alq.notna() & (alq > 0)
    pi = pct(100 * iab[ok4] / alq[ok4])
    hecho("TUR-IAB-SEC-P90", "Anuncios de vivienda completa en Inside Airbnb sobre el alquiler de la sección, P90 (solo áreas rastreadas)", pi[1],
          "% del parque de alquiler de la sección", "2026-09", "Inside Airbnb (CC BY 4.0; agregado propio por sección en la base); Censo 2021",
          "hecho", fi, minimo=pi[0], maximo=pi[2],
          nota=f"min = P50; max = P99; {int(ok4.sum())} secciones no selladas de las áreas rastreadas; anuncios, no viviendas registradas; no oficial")
    res.update(iab=pi, n_iab=int(ok4.sum()))

    # Traslación a precio con Garcia-López et al.: % de alquiler por punto de viviendas turísticas sobre viviendas
    lo, hi = DOC["gl_rent_dens"], DOC["gl_rent_alto"]
    nac_viv = 100 * 403267 / 26623708  # parque de viviendas familiares del Censo 2021 (informe integral, I.7)
    for nombre, val in (("NAC", nac_viv), ("SEC-P50", pv[0]), ("SEC-P90", pv[1]), ("SEC-P99", pv[2])):
        hecho(f"TUR-GL-ALQ-{nombre}", f"Alquiler compatible con la densidad turística ({nombre}) según los coeficientes de Garcia-López et al. (ilustración)",
              (lo + hi) / 2 * val, "% de alquiler (nivel acumulado frente a densidad cero)", "2024M08",
              "Garcia-López et al. (2020, JUE 119, 103278; versión de trabajo MPRA 96131, cuadro 4); densidad propia", "juicio experto (calibración)", fi,
              minimo=lo * val, maximo=hi * val,
              nota=(f"densidad {val:.2f} % de las viviendas; {lo}-{hi} % de alquiler por punto (Barcelona 2012-2016, anuncios de Idealista); "
                    "fuera del soporte del estudio (≈ 5 %) es extrapolación; validez externa no comprobada; no es un efecto estimado aquí"))
    res.update(gl_nac=(lo * nac_viv, hi * nac_viv, nac_viv), gl=[(lo * v_, hi * v_) for v_ in pv])
    # Comparación con H3 (V15): pendiente por DT intra-sección
    h3 = json.loads(H3.read_text(encoding="utf-8"))
    dt = h3["diagnosticos"]["comprobacion_medida"]["dt_intra_pct_puntos"]
    b = h3["estimacion"]["beta_pct_por_DT"]
    mde = h3["diagnosticos"]["MDE80_pct_por_DT"]["conley"]
    hecho("TUR-GL-FRENTE-H3", "Pendiente por DT intra-sección que implicarían los coeficientes de Garcia-López et al., frente a H3 (V15)",
          (lo + hi) / 2 * dt, "% de alquiler por DT intra-sección", "2021-2024", "output/v15/p5/resultado.json (H3); Garcia-López et al.",
          "juicio experto (calibración)", fi, minimo=lo * dt, maximo=hi * dt,
          nota=f"DT intra-sección {dt:.2f} pp; H3 = {b:.4f} % por DT (EMD 80 % = {mde:.3f}); H3 mide contratos vigentes (SERPAVI) y GL anuncios nuevos")
    res.update(h3=(b, mde, dt, lo * dt, hi * dt))
    return res


# ---------------------------------------------------------------- inmigración (y D3-1)
def inmigracion() -> dict:
    fi = "inmigracion"
    d3 = {h["id"]: h for h in json.loads((D3 / "hechos.json").read_text(encoding="utf-8"))}
    ten = pd.read_csv(D3 / "tenencia_por_origen_censo2021.csv")
    t = ten[ten.grupo == "nacido_en_espana"].pivot_table(index="categoria", columns="tenencia", values=["hogares_muestra", "pct"], aggfunc="first")
    n_ext, n_esp = t.loc["no", ("hogares_muestra", "alquiler")], t.loc["si", ("hogares_muestra", "alquiler")]
    a_ext, a_esp = t.loc["no", ("pct", "alquiler")], t.loc["si", ("pct", "alquiler")]
    alq_ext, alq_esp = n_ext * a_ext / 100, n_esp * a_esp / 100
    cuota_hog = 100 * n_ext / (n_ext + n_esp)
    cuota_alq = 100 * alq_ext / (alq_ext + alq_esp)
    l = ten[(ten.grupo == "llegada_espana") & (ten.tenencia == "alquiler")].set_index("categoria").pct
    l_rec = l["2016-2021"]
    fu = "output/v17/d3/tenencia_por_origen_censo2021.csv (Censo 2021, muestra del 10 %, persona de mayor edad)"
    hecho("INM-CUOTA-ALQUILER-EXTR", "Hogares en alquiler cuya persona de mayor edad nació en el extranjero, sobre el total de hogares en alquiler",
          cuota_alq, "% de los hogares en alquiler", "2021", fu, "hecho", fi,
          nota=f"frente a {cuota_hog:.1f} % del total de hogares; la llegada 2016-2021 alquila un {l_rec:.1f} %".replace(".", ","))
    hecho("INM-ALQUILER-LLEGADA-RECIENTE", "Hogares en alquiler, persona de mayor edad llegada a España en 2016-2021", l["2016-2021"], "% de los hogares del grupo",
          "2021", fu, "hecho", fi, minimo=a_esp, maximo=l["2016-2021"], nota=f"min = nacidos en España ({a_esp:.1f} %)".replace(".", ","))
    # Demanda de alquiler nueva contable: hogares del componente población 2021-2026 por origen × tasa de alquiler del grupo
    hog_ext = d3["V17-D3-HOGARES-ORIGEN-NACIDOS-EXTRANJERO"]
    lo_h, hi_h = hog_ext.get("min") or hog_ext["valor"], hog_ext.get("max") or hog_ext["valor"]
    alq_nuevo_lo, alq_nuevo_hi = lo_h * a_ext / 100, hi_h * l["2016-2021"] / 100
    hecho("INM-ALQUILER-NUEVO-CONTABLE", "Hogares en alquiler implícitos en el aumento de hogares 2021-2026 atribuido a nacidos en el extranjero (contabilidad)",
          (alq_nuevo_lo + alq_nuevo_hi) / 2, "hogares", "2021-2026",
          "V17-D3-HOGARES-ORIGEN-NACIDOS-EXTRANJERO × tasa de alquiler por origen (Censo 2021)", "cota", fi,
          minimo=alq_nuevo_lo, maximo=alq_nuevo_hi,
          nota="supuesto: los hogares nuevos alquilan como los de su origen en 2021 (min: todos los nacidos fuera; max: llegada 2016-2021); contabilidad, no efecto")
    # Comparación de magnitudes con González y Ortega (2013) y Saiz (2007)
    inf = pd.read_csv(INFER["micro"]).set_index("id_resultado")
    infer = inf.loc[[i for i in ("H4-AKM0", "Q3-b", "Q3-c1-AKM0", "Q3-c2-AKM0") if i in inf.index],
                    ["estimacion_publicada", "unidad", "p_conv", "ic95_lo", "ic95_hi", "tamano_real", "publicable"]]
    # D3-1: composición del flujo por origen y vía de asilo (hechos; los motivos no se atribuyen)
    gr = pd.read_csv(D3 / "demografia_grupos_nacionalidad.csv")
    sk = gr[gr.medida == "stock_1_enero"].set_index("anio")
    sud = 100 * (sk.loc[2025, "De Sudamérica"] / sk.loc[2015, "De Sudamérica"] - 1)
    dsk = {c: sk.loc[2025, c] - sk.loc[2015, c] for c in ("De Africa", "De América del Norte", "De Asia", "De Centro América y Caribe", "De Sudamérica")}
    cuota_lat = 100 * (dsk["De Sudamérica"] + dsk["De Centro América y Caribe"]) / sum(dsk.values())
    hecho("D31-LATAM-CUOTA", "Parte de la variación 2015-2025 de la población extranjera de África, América y Asia que es de Sudamérica, Centroamérica y Caribe",
          cuota_lat, "% de la variación del grupo", "1-1-2015 a 1-1-2025", "output/v17/d3/demografia_grupos_nacionalidad.csv (INE, población por nacionalidad)",
          "hecho", "D3-1", nota=(f"población de nacionalidad sudamericana +{sud:.0f} %; nacionalidad, no país de nacimiento (las nacionalizaciones "
                                 "salen del recuento); Europa no se incluye por ruptura de la serie en 2021"), pregunta=True)
    asi = duckdb.sql(f"select substr(periodo,1,4) a, sum(valor) v from '{BASE}' where variable='asilo_solicitantes' and nivel='nacional' "
                     "and desagregacion='nacionalidad=TOTAL' and not muestra_sellada_v6 group by 1 order by 1").df().set_index("a").v
    asi_1925 = float(asi.loc["2019":"2025"].sum())
    hecho("D31-ASILO-2019-2025", "Solicitantes de protección internacional en España, suma 2019-2025", asi_1925, "personas (solicitudes)", "2019-2025",
          "base: asilo_solicitantes (Eurostat migr_asyappctzm)", "OF", "D3-1",
          nota="frente a un saldo exterior oficial de 3,76 millones en 2015-2024 (V17-D3-SALDO-EXTERIOR-OFICIAL); una solicitud no es una entrada neta",
          pregunta=True)
    go = DOC["go_precio"] / DOC["go_pob"]
    hecho("INM-GO-ELASTICIDAD", "Elasticidad implícita del precio de la vivienda a la población en González y Ortega (2013): 2 % anual de precio por 1,5 % anual de población",
          go, "% de precio por 1 % de población", "2000-2010", "González y Ortega (2013), J. Regional Science 53(1), 37-59, resumen (Crossref)",
          "juicio experto", fi, minimo=1.5 / DOC["go_pob"], maximo=2.3 / DOC["go_pob"],
          nota=("cociente de las cifras del resumen (precio +1,5 a +2,3 % anual según docs/v17/referencias/d2_versiones.md; central 2 %); "
                "la versión publicada (Wiley) no se leyó: cifras de resúmenes secundarios; comparar con Q3-c1-AKM0 y H4"))
    return {"cuota_alq": cuota_alq, "cuota_hog": cuota_hog, "a_ext": a_ext, "a_esp": a_esp, "a_rec": float(l["2016-2021"]),
            "alq_nuevo": (alq_nuevo_lo, alq_nuevo_hi), "go": go, "d3": d3, "infer": infer, "lat": cuota_lat, "sud": sud, "asilo": asi_1925, "asi": asi}


# ---------------------------------------------------------------- tipos
def tipos() -> dict:
    fi = "tipos"
    n = pd.read_csv(NAC)
    s = n.set_index("trimestre")
    tae = s.tipo_hip_nuevas_tae
    d_tae = tae.loc["2023Q3"] - tae.loc["2021Q4"]
    d_anual = media_anual(n, "tipo_hip_nuevas_tae", 2023) - media_anual(n, "tipo_hip_nuevas_tae", 2021)
    hecho("TIP-DELTA-TAE", "Subida del tipo de las nuevas hipotecas (TAE), 2021T4 al máximo de 2023T3", d_tae, "puntos porcentuales", "2021T4-2023T3",
          "data/processed/v8/nacional_q_v8.csv (tipo_hip_nuevas_tae, Banco de España)", "OF", fi, minimo=d_anual, maximo=d_tae,
          nota="min = media de 2023 menos media de 2021")
    ipv = s.ipv
    g_nom = 100 * (ipv.loc["2024Q4"] / ipv.loc["2021Q4"] - 1)
    g_real = 100 * ((ipv.loc["2024Q4"] / s.ipc_general.loc["2024Q4"]) / (ipv.loc["2021Q4"] / s.ipc_general.loc["2021Q4"]) - 1)
    hecho("TIP-IPV-2022-2024", "Variación del IPV (ajustado por calidad), 2021T4-2024T4", g_nom, "%", "2021T4-2024T4",
          "data/processed/v8/nacional_q_v8.csv (INE IPV e IPC general)", "OF", fi, minimo=g_real, maximo=g_nom, nota="min = real (IPC general)")
    # Calibración (decisión del autor, 2026-10-19): «juicio experto (calibración)», con rango completo, elasticidades y fuente;
    # nunca «sin la subida de tipos habría subido X». Cada semielasticidad se aplica al tipo con el que se estimó y se compara con
    # la medida de precio que usa (real o nominal).
    dfr = s.tipo_dfr
    d_pol = dfr.loc["2023Q4"] - dfr.loc["2021Q4"]
    hecho("TIP-DELTA-POLITICA", "Subida del tipo de la facilidad de depósito del BCE, 2021T4-2023T4", d_pol, "puntos porcentuales", "2021T4-2023T4",
          "data/processed/v8/nacional_q_v8.csv (tipo_dfr, BCE)", "OF", fi)
    cal = [  # (fuente, semielasticidad %/pp, tipo, medida de precio, subida aplicada mín., máx.)
        ("BCE BE 6/2022, lineal", DOC["bce_semi"], "hipotecario", "precio (real o nominal: no consta en lo leído)", d_anual, d_tae),
        ("BCE BE 6/2022, no lineal con tipos bajos", DOC["bce_semi_nl"], "hipotecario", "precio (no consta)", d_anual, d_tae),
        ("Calza, Monacelli y Stracca (2013), reescalado por Williams (2015)", DOC["calza_semi"], "interbancario a 3 meses (política)", "precio real", d_pol, d_pol),
        ("Williams (2015) con Jordà, Schularick y Taylor (2015)", DOC["williams_semi"], "corto (política)", "precio real", d_pol, d_pol),
    ]
    filas = []
    for fu, se, ti, me, d0, d1 in cal:
        filas.append((fu, se, ti, me, se * d0, se * d1))
    efectos = [x for f_ in filas for x in (f_[4], f_[5])]
    ef_h = [x for f_ in filas[:2] for x in (f_[4], f_[5])]
    ef_p = [x for f_ in filas[2:] for x in (f_[4], f_[5])]
    ef_c = DOC["bce_semi"] * d_anual
    hecho("TIP-CALIBRACION-EFECTO-HIPOTECARIO", "Calibración: efecto en el precio a unos dos años de la subida del tipo hipotecario 2022-2023 (semielasticidades del BCE para la zona euro: −5 %/pp lineal; −9 %/pp no lineal con tipos bajos)",
          ef_c, "% del nivel de precios", "2022-2025", "BCE, Boletín Económico 6/2022 (proyecciones locales, 1995-2019); TIP-DELTA-TAE",
          "juicio experto (calibración)", fi, minimo=min(ef_h), maximo=max(ef_h),
          nota="central = −5 %/pp × subida de la TAE media 2021→2023 (2,27 pp); rango con 2,27-2,51 pp y −5 a −9 %/pp; zona euro, no España; medida de precio no especificada en lo leído")
    hecho("TIP-CALIBRACION-EFECTO-POLITICA", "Calibración: efecto en el precio REAL a unos dos años de la subida del tipo de política 2022-2023 (semielasticidades de −2,3 y −6,3 %/pp del tipo corto)",
          sum(ef_p) / len(ef_p), "% del precio real", "2022-2025", "Calza et al. (2013) y Williams (2015); TIP-DELTA-POLITICA", "juicio experto (calibración)", fi,
          minimo=min(ef_p), maximo=max(ef_p),
          nota="extrapolación lineal de 1 pp a ≈ 4,5 pp: fuera del rango habitual de las estimaciones; comparar con el IPV real (+8,5 %)")
    desc = lambda ef, obs: 100 * ((1 + obs / 100) / (1 + ef / 100) - 1)
    hecho("TIP-CALIBRACION-DESCONTADO", "Calibración: variación del IPV 2021T4-2024T4 una vez descontado el efecto calibrado del tipo hipotecario (nominal)",
          desc(ef_c, g_nom), "%", "2021T4-2024T4", "TIP-IPV-2022-2024 y TIP-CALIBRACION-EFECTO-HIPOTECARIO", "juicio experto (calibración)", fi,
          minimo=desc(max(ef_h), g_nom), maximo=desc(min(ef_h), g_nom),
          nota="(1 + observado) / (1 + efecto) − 1; BCE −5 a −9 %/pp × 2,27-2,51 pp; ignora el desfase de dos años, la bajada de 2024-2025 y los demás choques; no es un contrafactual identificado")
    hecho("TIP-CALIBRACION-DESCONTADO-REAL", "Calibración: variación del IPV REAL 2021T4-2024T4 una vez descontado el efecto calibrado del tipo de política",
          desc(sum(ef_p) / len(ef_p), g_real), "%", "2021T4-2024T4", "TIP-IPV-2022-2024 (real) y TIP-CALIBRACION-EFECTO-POLITICA", "juicio experto (calibración)", fi,
          minimo=desc(max(ef_p), g_real), maximo=desc(min(ef_p), g_real), nota="ver TIP-CALIBRACION-EFECTO-POLITICA")
    sh = DOC["bde_con_hipoteca_2025"] / 100
    hecho("TIP-CALIBRACION-SOLO-HIPOTECA", "Calibración: efecto del tipo hipotecario si solo se transmite a la parte de compras con hipoteca (52 %)", ef_c * sh, "% del nivel de precios",
          "2022-2025", "TIP-CALIBRACION-EFECTO-HIPOTECARIO × 52 % (BdE IA2025, p. 124)", "juicio experto (calibración)", fi, minimo=min(ef_h) * sh, maximo=max(ef_h) * sh,
          nota="cota inferior del efecto en valor absoluto: los compradores al contado también descuentan con el tipo (coste de oportunidad)")
    # Demanda que acompañó a la subida: renta y hogares
    rdb = 100 * (media_anual(n, "rdb", 2024) / media_anual(n, "rdb", 2021) - 1)
    hog = 1000 * (media_anual(n, "hogares_epa", 2024) - media_anual(n, "hogares_epa", 2021))
    hecho("TIP-RDB-2021-2024", "Variación de la renta disponible bruta de los hogares (nominal), 2021-2024", rdb, "%", "2021-2024",
          "data/processed/v8/nacional_q_v8.csv (rdb, INE contabilidad trimestral)", "OF", fi, nota=f"hogares EPA +{hog:,.0f} (medias anuales)")
    # Q5 con Newey-West (V17 fase 2)
    inf = pd.read_csv(INFER["series"])
    q5 = inf[inf.id_resultado.astype(str).str.startswith("Q5-p-")][["id_resultado", "estimacion_publicada", "p_conv", "ic95_lo", "ic95_hi",
                                                                      "tamano_real", "p_holm_pregunta"]]
    return {"d_tae": d_tae, "d_anual": d_anual, "d_pol": d_pol, "g_nom": g_nom, "g_real": g_real, "filas": filas,
            "ef_h": (min(ef_h), ef_c, max(ef_h)), "ef_p": (min(ef_p), sum(ef_p) / len(ef_p), max(ef_p)),
            "desc_nom": (desc(max(ef_h), g_nom), desc(ef_c, g_nom), desc(min(ef_h), g_nom)),
            "desc_real": (desc(max(ef_p), g_real), desc(sum(ef_p) / len(ef_p), g_real), desc(min(ef_p), g_real)),
            "sh": (min(ef_h) * sh, ef_c * sh, max(ef_h) * sh),
            "rdb": rdb, "hog": hog, "q5": q5, "tae21": tae.loc["2021Q4"], "tae23": tae.loc["2023Q3"], "tae25": tae.loc["2025Q4"]}


# ---------------------------------------------------------------- burbuja
def burbuja() -> dict:
    fi = "burbuja"
    mc = json.loads(MC_GSADF.read_text(encoding="utf-8"))["estimacion"]
    hecho("BUR-GSADF-POTENCIA", "Potencia del GSADF de Q9-g (factor común, bootstrap salvaje) frente a una alternativa explosiva simulada (Monte Carlo V16); no calculada para el GSADF nacional de V7.2",
          mc["potencia"]["alt_homo"], "fracción de rechazos al 5 % nominal", "simulación T = 98", "output/v16/montecarlo/gsadf_factor/resultado.json",
          "hecho", fi, minimo=mc["potencia"]["alt_homo"], maximo=mc["potencia"]["alt_salto"],
          nota="min = alternativa homocedástica; max = alternativa con saltos; tamaño 0,017-0,046: el contraste casi nunca detecta la alternativa simulada")
    m = pd.read_csv(ROOT / "output/v17/lectura_bde/medidas_referencia/medidas.csv").set_index("id")
    pr, ra, cr = m.loc["V17-B5-PRECIO-RENTA"], m.loc["V17-B5-RENTABILIDAD-ALQUILER"], m.loc["V17-B5-CREDITO-PIB"]
    hecho("BUR-CREDITO-FRENTE-2007", "Saldo del crédito a hogares para vivienda sobre PIB: último dato frente a 2007", cr.ultimo - cr.media_2007,
          "puntos de PIB", f"{cr.fecha_ultimo} frente a 2007", "V17-B5-CREDITO-PIB (BdE, Síntesis de indicadores, SI_1_5.56)", "OF", fi,
          minimo=cr.ultimo, maximo=cr.media_2007, nota="min = último (% del PIB); max = media de 2007")
    pr_desv07 = 100 * (pr.ultimo / pr.media_2007 - 1)
    hecho("BUR-PRECIO-RENTA-FRENTE-2007", "Precio de la vivienda / renta bruta por hogar: último dato frente a 2007", pr_desv07, "%",
          f"{pr.fecha_ultimo} frente a 2007", "V17-B5-PRECIO-RENTA (BdE SI_1_5.43)", "OF", fi, minimo=pr.ultimo, maximo=pr.media_2007,
          nota=f"min = último (años de renta); max = 2007; {pr.desv_media_pct:.1f} % sobre la media 1987-2025; mide precio por m² tasado, no IPV")
    return {"pot": (mc["potencia"]["alt_homo"], mc["potencia"]["alt_salto"]), "tam": mc["tamano"], "pr": pr, "ra": ra, "cr": cr,
            "pr07": pr_desv07, "m": m}


# ---------------------------------------------------------------- precio
def precio() -> dict:
    fi = "precio"
    n = pd.read_csv(NAC)
    g = lambda c, a=2019, b=2025: media_anual(n, c, b) / media_anual(n, c, a)
    ipv, tas, ipc, rdb, hog = g("ipv"), g("p_tasado"), g("ipc_general"), g("rdb"), g("hogares_epa")
    rph = rdb / hog
    hecho("PRE-IPV-REAL-RENTA", "IPV deflactado por la renta disponible bruta por hogar, 2019-2025", 100 * (ipv / rph - 1), "%", "2019-2025 (medias anuales)",
          "data/processed/v8/nacional_q_v8.csv (INE IPV; INE renta disponible bruta de los hogares; EPA hogares)", "hecho", fi,
          minimo=100 * (ipv / rdb * (media_anual(n, "pob_total", 2025) / media_anual(n, "pob_total", 2019)) - 1), maximo=100 * (ipv / rph - 1),
          nota=f"renta por hogar +{100 * (rph - 1):.1f} %; min = deflactado por renta per cápita; IPV nominal +{100 * (ipv - 1):.1f} %, real IPC +{100 * (ipv / ipc - 1):.1f} %")
    hecho("PRE-TASADO-REAL-RENTA", "Valor tasado por m² deflactado por la renta disponible bruta por hogar, 2019-2025", 100 * (tas / rph - 1), "%",
          "2019-2025 (medias anuales)", "data/processed/v8/nacional_q_v8.csv (MIVAU valor tasado; INE renta; EPA)", "hecho", fi,
          nota=f"valor tasado nominal +{100 * (tas - 1):.1f} %, real IPC +{100 * (tas / ipc - 1):.1f} %")
    # Composición entre provincias (sin muestra sellada v6): índice de valor unitario frente a Laspeyres de pesos fijos 2019
    d = base("nivel='provincia' and variable in ('valor_tasado','compraventas') and (periodo like '2019T_' or periodo like '2025T_')")
    d["p"] = d.p.str[:4]   # media (valor tasado) o suma (compraventas) de los cuatro trimestres
    w = pd.concat([d[d.v == "valor_tasado"].pivot_table(index="c", columns=["v", "p"], values="valor", aggfunc="mean"),
                   d[d.v == "compraventas"].pivot_table(index="c", columns=["v", "p"], values="valor", aggfunc="sum")], axis=1).dropna()
    nq = d.groupby(["c", "v", "p"]).size().unstack(["v", "p"])
    w = w[(nq.reindex(w.index) == 4).all(axis=1)]   # solo provincias con los cuatro trimestres en ambos años
    P0, P1 = w[("valor_tasado", "2019")], w[("valor_tasado", "2025")]
    C0, C1 = w[("compraventas", "2019")], w[("compraventas", "2025")]
    uv = (P1 * C1).sum() / C1.sum() / ((P0 * C0).sum() / C0.sum())
    las = (P1 * C0).sum() / (P0 * C0).sum()
    hecho("PRE-COMPOSICION-PROVINCIAS", "Efecto de composición entre provincias en el valor tasado medio: valor unitario ponderado por compraventas menos Laspeyres de pesos 2019",
          100 * (uv - las), "puntos porcentuales de variación 2019-2025", "2019-2025", "base: valor_tasado y compraventas provinciales (MIVAU, INE ETDP)",
          "hecho", fi, minimo=100 * (uv - 1), maximo=100 * (las - 1),
          nota=f"{len(w)} provincias sin muestra sellada v6; min = valor unitario; max = pesos fijos 2019; solo capta composición ENTRE provincias")
    # Composición entre antigüedades (BdE SI 1.5: tasado hasta 5 años y más de 5 años)
    raw = pd.read_csv(SI, encoding="latin-1", header=None, dtype=str)
    alias = raw.iloc[2].tolist()
    fil = raw.iloc[6:]
    fil = fil[fil[0].str.match(r"^[A-Z]{3} \d{4}$", na=False)]
    anio = fil[0].str[4:].astype(int)
    def am(a, y):
        j = alias.index(a)
        return float(pd.to_numeric(fil[j].str.replace(",", "."), errors="coerce")[anio == y].mean())
    tot = am("SI_1_5.4", 2025) / am("SI_1_5.4", 2019)
    nue = am("SI_1_5.5", 2025) / am("SI_1_5.5", 2019)
    usa = am("SI_1_5.6", 2025) / am("SI_1_5.6", 2019)
    hecho("PRE-TASADO-ESTRATOS", "Valor tasado por m² 2019-2025: total frente a viviendas de hasta 5 años y de más de 5 años", 100 * (tot - 1), "%", "2019-2025",
          "BdE, Síntesis de indicadores (SI_1_5.4, SI_1_5.5, SI_1_5.6; fuente MIVAU)", "OF", fi, minimo=100 * (min(nue, usa) - 1), maximo=100 * (max(nue, usa) - 1),
          nota=f"hasta 5 años +{100 * (nue - 1):.1f} %; más de 5 años +{100 * (usa - 1):.1f} %; si el total sube menos que ambos estratos, hay composición entre ellos")
    nueva, usada = g("ipv_nueva"), g("ipv_usada")
    return {"ipv": ipv, "tas": tas, "ipc": ipc, "rph": rph, "uv": uv, "las": las, "n_prov": len(w), "tot": tot, "nue": nue, "usa": usa,
            "ipv_nueva": nueva, "ipv_usada": usada, "not": g("notariado_pm2_sem"), "reg": g("registr_pm2_4tm")}


# ---------------------------------------------------------------- alquiler
def alquiler() -> dict:
    fi = "alquiler"
    n = pd.read_csv(NAC)
    g = lambda c, a=2019, b=2025: media_anual(n, c, b) / media_anual(n, c, a)
    ia, ipc, rph = g("ipc_alquiler"), g("ipc_general"), g("rdb") / g("hogares_epa")
    hecho("ALQ-IPC-REAL-RENTA", "IPC de alquiler (contratos vigentes) deflactado por la renta disponible bruta por hogar, 2019-2025", 100 * (ia / rph - 1), "%",
          "2019-2025 (medias anuales)", "data/processed/v8/nacional_q_v8.csv (INE IPC alquiler; INE renta; EPA)", "hecho", fi,
          minimo=100 * (ia / rph - 1), maximo=100 * (ia - 1), nota=f"max = nominal; real IPC {100 * (ia / ipc - 1):.1f} %")
    # Contratos nuevos en Cataluña (Incasòl, renta media de contratos nuevos), Barcelona ciudad y total de la serie municipal
    d = base("variable='incasol_renta_media' and nivel='municipio' and periodo in ('2019','2025')")
    w = d.pivot_table(index="c", columns="p", values="valor").dropna()
    res = {"ia": ia, "ipc": ipc, "rph": rph}
    if len(w):
        gm = w["2025"] / w["2019"]
        hecho("ALQ-INCASOL-NUEVOS", "Renta media de contratos nuevos (Incasòl), mediana municipal de la variación 2019-2025", 100 * (gm.median() - 1), "%",
              "2019-2025", "base: incasol_renta_media (Incasòl, fianzas)", "OF", fi, minimo=100 * (gm.quantile(0.1) - 1), maximo=100 * (gm.quantile(0.9) - 1),
              nota=f"min = P10; max = P90; {len(w)} municipios sin muestra sellada v6 con dato en 2019 y 2025; nominal; contratos nuevos, no vigentes")
        res["incasol"] = (gm.median(), gm.quantile(0.1), gm.quantile(0.9), len(w))
        # Ponderado por contratos (mismo conjunto de municipios) y frente al IPC de alquiler de Cataluña
        c = base("variable='incasol_contratos' and nivel='municipio' and periodo in ('2019','2025')").pivot_table(index="c", columns="p", values="valor")
        k = w.join(c, rsuffix="_n").dropna()
        lasp = (k["2025"] * k["2019_n"]).sum() / (k["2019"] * k["2019_n"]).sum()
        uv = ((k["2025"] * k["2025_n"]).sum() / k["2025_n"].sum()) / ((k["2019"] * k["2019_n"]).sum() / k["2019_n"].sum())
        ipc09 = base("variable='ipc_alquiler' and nivel='ccaa' and c='09' and (periodo like '2019T_' or periodo like '2025T_')")
        ipc09 = ipc09[ipc09.c == "09"]
        g09 = ipc09[ipc09.p.str[:4] == "2025"].valor.mean() / ipc09[ipc09.p.str[:4] == "2019"].valor.mean()
        hecho("ALQ-INCASOL-NUEVOS-POND", "Renta media de contratos nuevos (Incasòl), Cataluña, ponderada por contratos de 2019 (Laspeyres municipal), 2019-2025",
              100 * (lasp - 1), "%", "2019-2025", "base: incasol_renta_media e incasol_contratos (Incasòl, fianzas)", "OF", fi,
              minimo=100 * (uv - 1), maximo=100 * (lasp - 1),
              nota=f"min = valor unitario (pesos de cada año); {len(k)} municipios; IPC de alquiler de Cataluña (contratos vigentes) +{100 * (g09 - 1):.1f} %; nominal")
        res["incasol_pond"] = (lasp, uv, g09, len(k))
    return res


ESP_NS = "España sin provincias ni CCAA selladas v6 (secciones censales)"
RANGO_COBERTURA = {   # id -> (tipo_rango, cobertura territorial real)
    "TUR-NAC-AUMENTO-2020-2024": ("rango", "España"), "TUR-NAC-STOCK-2024M08": ("rango", "España"),
    "TUR-NAC-STOCK-2024M02": ("sin rango", "España"), "TUR-NAC-STOCK-2026M05": ("sin rango", "España"),
    "TUR-SEC-P50": ("sin rango", ESP_NS), "TUR-SEC-P90": ("sin rango", ESP_NS), "TUR-SEC-P99": ("sin rango", ESP_NS),
    "TUR-SEC-AGREGADO": ("sin rango", ESP_NS), "TUR-SEC-ALQ-EN-ALTA": ("referencias", ESP_NS),
    "TUR-SEC-VIV-P90": ("referencias", ESP_NS), "TUR-SEC-AUMENTO-P90": ("referencias", ESP_NS),
    "TUR-SEC-P90-2026M05": ("referencias", ESP_NS),
    "TUR-MUN-P90": ("referencias", "España sin provincias ni CCAA selladas v6 (municipios, suma de secciones)"),
    "TUR-IAB-SEC-P90": ("referencias", "Áreas rastreadas por Inside Airbnb fuera de los bloques sellados v6 (secciones)"),
    "TUR-GL-ALQ-NAC": ("rango", "España (densidad); elasticidad de Barcelona"),
    "TUR-GL-ALQ-SEC-P50": ("rango", ESP_NS + "; elasticidad de Barcelona"),
    "TUR-GL-ALQ-SEC-P90": ("rango", ESP_NS + "; elasticidad de Barcelona"),
    "TUR-GL-ALQ-SEC-P99": ("rango", ESP_NS + "; elasticidad de Barcelona"),
    "TUR-GL-FRENTE-H3": ("rango", "Secciones de la muestra de entrenamiento de H3 (V15); elasticidad de Barcelona"),
    "INM-CUOTA-ALQUILER-EXTR": ("sin rango", "España sin las CCAA selladas v6 (Censo 2021, muestra del 10 %)"),
    "INM-ALQUILER-LLEGADA-RECIENTE": ("referencias", "España sin las CCAA selladas v6 (Censo 2021, muestra del 10 %)"),
    "INM-ALQUILER-NUEVO-CONTABLE": ("rango", "España"),
    "D31-LATAM-CUOTA": ("sin rango", "España"), "D31-ASILO-2019-2025": ("sin rango", "España"),
    "INM-GO-ELASTICIDAD": ("rango", "España, provincias (2000-2010)"),
    "TIP-DELTA-TAE": ("rango", "España"), "TIP-IPV-2022-2024": ("referencias", "España"),
    "TIP-DELTA-POLITICA": ("sin rango", "Zona del euro (tipo del BCE)"),
    "TIP-CALIBRACION-EFECTO-HIPOTECARIO": ("rango", "España (elasticidades de la zona del euro)"),
    "TIP-CALIBRACION-EFECTO-POLITICA": ("rango", "España (elasticidades internacionales)"),
    "TIP-CALIBRACION-DESCONTADO": ("rango", "España (elasticidades de la zona del euro)"),
    "TIP-CALIBRACION-DESCONTADO-REAL": ("rango", "España (elasticidades internacionales)"),
    "TIP-CALIBRACION-SOLO-HIPOTECA": ("rango", "España (elasticidades de la zona del euro)"),
    "TIP-RDB-2021-2024": ("sin rango", "España"),
    "BUR-GSADF-POTENCIA": ("rango", "Simulación con la estructura del factor común de Q9-g (provincias de V16)"),
    "BUR-CREDITO-FRENTE-2007": ("referencias", "España"), "BUR-PRECIO-RENTA-FRENTE-2007": ("referencias", "España"),
    "PRE-IPV-REAL-RENTA": ("rango", "España"), "PRE-TASADO-REAL-RENTA": ("sin rango", "España"),
    "PRE-COMPOSICION-PROVINCIAS": ("referencias", "España sin provincias ni CCAA selladas v6 (38 provincias con datos completos)"),
    "PRE-TASADO-ESTRATOS": ("referencias", "España"),
    "ALQ-IPC-REAL-RENTA": ("referencias", "España"),
    "ALQ-INCASOL-NUEVOS": ("referencias", "Cataluña, municipios con contratos en 2019 y 2025"),
    "ALQ-INCASOL-NUEVOS-POND": ("rango", "Cataluña, municipios con contratos en 2019 y 2025"),
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    r = {"turisticos": turisticos(), "inmigracion": inmigracion(), "tipos": tipos(), "burbuja": burbuja(), "precio": precio(), "alquiler": alquiler()}
    for h in HECHOS:
        k = h["id"].replace("V17-AUD-DP-", "")
        tr, cob = RANGO_COBERTURA[k]
        if h["min"] is None or h["max"] is None:
            tr = "sin rango"
        h["tipo_rango"], h["cobertura"] = tr, cob
    ids = [h["id"] for h in HECHOS]
    assert len(ids) == len(set(ids))
    (OUT / "demanda_precios_hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # Resumen legible para las fichas (no se versiona aparte: va a la salida estándar)
    t, p = r["turisticos"], r["precio"]
    print(json.dumps({k: v for k, v in t.items() if k != "top"}, default=float, indent=0)[:4000])
    print("top municipios:", t["top"])
    tp = r["tipos"]
    print("tipos", {k: tp[k] for k in ("d_tae", "d_anual", "d_pol", "g_nom", "g_real", "filas", "ef_h", "ef_p", "desc_nom", "desc_real", "sh", "rdb", "hog", "tae21", "tae23", "tae25")})
    print("precio", {k: (round(float(v), 4) if not isinstance(v, int) else v) for k, v in p.items()})
    print("alquiler", r["alquiler"])
    i = r["inmigracion"]
    print("inmigracion", {k: v for k, v in i.items() if k not in ("d3", "infer", "asi")}); print(i["asi"].to_dict()); print(i["infer"].to_string()); print(tp["q5"].to_string())
    print("burbuja", r["burbuja"]["pot"], r["burbuja"]["tam"], r["burbuja"]["pr07"])
    print(len(HECHOS), "hechos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
