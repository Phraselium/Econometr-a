"""T2 · Viviendas liberadas por envejecimiento 2026-2035 (y escenario 2036-2040). Determinista, sin red.

Una vivienda se libera cuando se disuelve el ultimo miembro del hogar: (i) fallecimiento del ultimo
miembro (mayores de 75 anos, misma formula que B1) o (ii) traslado a residencia de quien vivia solo.
NO se resta de la necesidad: la proyeccion de hogares del INE ya la descuenta.
Uso: python3 src/v5_1/t2_run.py [--smoke]
"""
from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
for p in ("src", "src/v3", "src/v4", "src/v5"):
    sys.path.insert(0, str(RAIZ / p))
import b1_run as b1  # noqa: E402
import econ_utils  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
OUT = RAIZ / "output" / "v5_1" / "T2"
SMOKE = "--smoke" in sys.argv
PER = {"2026-2035": (2026, 2035), "2036-2040": (2036, 2040)}
# Supuestos (C4). Ternas (min, central, max) de LIBERACION: en cada ruta el valor "min" es el que menos libera.
H_FACT = b1.H_FACT
DISOL = b1.DISOL
R_INST = {"min": 0.04, "central": 0.06, "max": 0.08}     # % de 75+ en residencia (supuesto; ver metodo.md)
ESTANCIA = {"min": 4.0, "central": 3.0, "max": 2.5}      # anos medios de estancia -> entradas = stock/estancia
SOLO = {"min": 0.30, "central": 0.45, "max": 0.60}       # fraccion de entrantes que vivian solos (hogar se disuelve)
RR_MORT = 2.0                                           # sobremortalidad en residencia (supuesto)
CAPITAL = {"01": "01059", "12": "12040", "20": "20069", "31": "31201", "48": "48020"}
CAP_NOM = {"02": "Albacete", "03": "Alicante", "04": "Almeria", "05": "Avila", "06": "Badajoz", "07": "Palma",
           "08": "Barcelona", "09": "Burgos", "10": "Caceres", "11": "Cadiz", "13": "Ciudad Real", "14": "Cordoba",
           "15": "Coruna", "16": "Cuenca", "17": "Girona", "18": "Granada", "19": "Guadalajara", "21": "Huelva",
           "22": "Huesca", "23": "Jaen", "24": "Leon", "25": "Lleida", "26": "Logrono", "27": "Lugo", "28": "Madrid",
           "29": "Malaga", "30": "Murcia", "32": "Ourense", "33": "Oviedo", "34": "Palencia",
           "35": "Palmas de Gran", "36": "Pontevedra", "37": "Salamanca", "38": "Santa Cruz de Tenerife",
           "39": "Santander", "40": "Segovia", "41": "Sevilla", "42": "Soria", "43": "Tarragona", "44": "Teruel",
           "45": "Toledo", "46": "Valencia", "47": "Valladolid", "49": "Zamora", "50": "Zaragoza", "51": "Ceuta",
           "52": "Melilla"}
FECHAS = {
    "mort": "INE tabla 67235, mortalidad por provincia 2024 (mod. 2025-11)",
    "pob": "INE tabla 36726, Proyecciones de Poblacion 2024-2074 (corto plazo), 2026-2041",
    "hog": "INE tabla 54562, Proyeccion de Hogares (mod. 2026-06-17)",
    "censo": "INE Censo 2021 (1-nov-2021), secciones",
    "ecv": "INE ECV tabla 9994, tenencia por edad de la persona de referencia, 2025",
    "her": "INE ETDP tabla 6154, viviendas transmitidas por titulo (herencia), 2014-2025",
}


def nrm(s: str) -> str:
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


def tipos_municipio() -> pd.DataFrame:
    """Municipio (todos los del Censo) -> tipo. Regla: capital; 'entorno_grande' = no capital con >=50.000 hab. (Censo 2021)
    de la misma provincia; 'resto'. Clase A4 del municipio si esta en clasificacion_municipios.csv."""
    ind = pd.read_csv(RAIZ / "data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz", dtype={"codigo": str},
                      usecols=["serie", "codigo", "valor"])
    ind = ind[ind.serie.isin(["t1_1", "t19_1", "t20_1", "t20_2"])]
    ind["mun"] = ind.codigo.str.zfill(10).str[:5]
    g = ind.groupby(["mun", "serie"]).valor.sum().unstack()
    g.columns = ["pob", "ppal", "propiedad", "alquiler"] if list(g.columns) == ["t19_1", "t1_1", "t20_1", "t20_2"] else g.columns
    g = g.rename(columns={"t1_1": "pob", "t19_1": "ppal", "t20_1": "propiedad", "t20_2": "alquiler"})
    ed = pd.read_csv(RAIZ / "data/raw/v3/ine_v3_censo2021_seccion_edad.csv", dtype={"codigo": str},
                     usecols=["serie", "codigo", "valor"])
    ed = ed[ed.serie == "EDAD_65+"]
    g["pob65"] = ed.groupby(ed.codigo.str.zfill(10).str[:5]).valor.sum()
    g = g.reset_index()
    g["cod_prov"] = g.mun.str[:2]
    a4 = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_municipios.csv", dtype={"cod_mun": str, "cod_prov": str})
    cap = dict(CAPITAL)
    for c, nm in CAP_NOM.items():
        s = a4[(a4.cod_prov == c) & a4.municipio.map(nrm).str.startswith(nrm(nm))]
        assert len(s) == 1, (c, nm, s.municipio.tolist())
        cap[c] = s.cod_mun.iloc[0]
    assert len(cap) == 52 and all(m in set(g.mun) for m in cap.values())
    g["tipo"] = np.where(g.mun.isin(cap.values()), "capital", np.where(g["pob"] >= 50000, "entorno_grande", "resto"))
    g = g.merge(a4[["cod_mun", "clase_2021_2025"]].rename(columns={"cod_mun": "mun"}), on="mun", how="left")
    return g.fillna({"pob65": 0})


def tenencia_65() -> dict:
    x = pd.read_csv(RAIZ / "data/raw/v3/ine_ecv_tenencia_edad_v3.csv")
    y = x[x.serie.str.contains("65 y más") & x.serie.str.contains("Ambos") & (x.periodo == 2025)]
    v = {k: float(y[y.serie.str.contains("|" + k + "|", regex=False)].valor.iloc[0]) / 100
         for k in ("Propiedad", "Alquiler a precio de mercado", "Alquiler inferior al precio de mercado", "Cesión")}
    return {"propiedad": v["Propiedad"], "alquiler": v["Alquiler a precio de mercado"]
            + v["Alquiler inferior al precio de mercado"], "cesion": v["Cesión"]}


def herencias() -> pd.DataFrame:
    h = pd.read_csv(RAIZ / "data/raw/v5_1/ine_t2_t6154.csv")
    h = h[h.nombre.str.contains(". Herencia. Total viviendas")].copy()
    h["k"] = h.nombre.str.split(". Herencia").str[0].map(b1.kn)
    return h.drop_duplicates(["k", "anyo"]).pivot(index="k", columns="anyo", values="valor")


def muertes_prov(pp, qk, k, y0, y1):
    sub = pp[(pp.k == k) & (pp.e >= 75)]
    pv = sub.pivot(index="e", columns="anyo", values="valor")
    band = pv.index.map(lambda e: min(95, 75 + 5 * ((e - 75) // 5)))
    qb = np.array([qk.loc[k, b] for b in band])
    anios = list(range(y0, y1 + 1))
    d = pv.loc[:, anios].mul(qb, axis=0).sum()
    return d.sum(), pv.loc[:, anios].sum().sum(), pv[y0].sum()


def entregables(res, bp, t, ten, h65, ctrl) -> None:
    r1, r2 = res["2026-2035"], res["2036-2040"]
    need = float(bp.N_anual_central.sum())
    need_lo, need_hi = float(bp.N_anual_min.sum()), float(bp.N_anual_max.sum())
    a = {k: v / 10 for k, v in r1.items() if isinstance(v, float)}
    b = {k: v / 5 for k, v in r2.items() if isinstance(v, float)}
    herencia = r1["herencias_anual_2023_25_modelo"]
    prop_muerte = float(((t[t.periodo == "2026-2035"].via_fallecimiento_central * t[t.periodo == "2026-2035"].frac_propietaria).sum()) / 10)
    x_lo, x_hi = a["no_llega_min"], a["no_llega_max"]
    stress = 0.5 * a["liberadas_central"]
    d1, d2 = "2026-01-01", "2026-06-17"
    fuentes = ["INE 54562", "INE 36726", "INE 67235", "INE Censo 2021", "INE ECV 9994", "INE ETDP 6154"]
    H = []

    def h(i, ind, v, lo, hi, u, per, cob, capa, fecha, f=fuentes):
        H.append(dict(id=i, indicador=ind, valor=round(v, 1), min=round(lo, 1), max=round(hi, 1), unidad=u, periodo=per,
                      cobertura=cob, fuentes=f, capa=capa, fecha_dato=fecha))
    h("T2-H1", "Viviendas liberadas por fallecimiento del ultimo miembro y traslado a residencia, acumuladas", r1["liberadas_central"],
      r1["liberadas_min"], r1["liberadas_max"], "viviendas", "2026-2035", "52 provincias", "C4", "2026-06-17")
    h("T2-H2", "Viviendas liberadas al ano (media)", a["liberadas_central"], a["liberadas_min"], a["liberadas_max"], "viviendas/ano",
      "2026-2035", "52 provincias", "C4", "2026-06-17")
    h("T2-H3", "Viviendas liberadas por fallecimiento (formula B1 con correccion por muertes en residencia), acumuladas",
      r1["via_fallecimiento_central"], r1["via_fallecimiento_central"], r1["via_fallecimiento_central"], "viviendas", "2026-2035",
      "52 provincias", "C4", "2026-06-17")
    h("T2-H4", "Viviendas liberadas por traslado a residencia de quien vivia solo, acumuladas", r1["via_residencia_central"],
      r1["via_residencia_central"], r1["via_residencia_central"], "viviendas", "2026-2035", "52 provincias", "C4", "2026-06-17")
    h("T2-H5", "Escenario: viviendas liberadas acumuladas", r2["liberadas_central"], r2["liberadas_min"], r2["liberadas_max"],
      "viviendas", "2036-2040", "52 provincias (escenario, mortalidad 2024 constante)", "C4", "2026-06-17")
    h("T2-H6", "Viviendas liberadas que llegan al mercado (venta o alquiler), al ano", a["mercado_central"], a["mercado_min"],
      a["mercado_max"], "viviendas/ano", "2026-2035", "52 provincias", "C4", "2026-06-17")
    h("T2-H7", "Viviendas liberadas que NO llegan al mercado al ano (X data-based: vacias y secundarias del Censo 2021)",
      a["no_llega_central"], x_lo, x_hi, "viviendas/ano", "2026-2035", "52 provincias", "C4", "2021-11-01")
    h("T2-H8", "Aumento posible de la necesidad efectiva (no_llega / necesidad central B1)", 100 * a["no_llega_central"] / need,
      100 * x_lo / need, 100 * x_hi / need, "%", "2026-2035", "52 provincias", "C4", "2026-06-17")
    h("T2-H9", "Prueba de estres X=50 % (sin dato): aumento posible de la necesidad", 100 * stress / need, 100 * stress / need,
      100 * stress / need, "%", "2026-2035", "52 provincias", "C4", "2026-06-17")
    h("T2-H10", "Cuota de las liberadas (central) en provincias A4 clase 1-2", 100 * r1["en_prov_clase12_central"] / r1["liberadas_central"],
      100 * r1["en_prov_clase12_central"] / r1["liberadas_central"], 100 * r1["en_prov_clase12_central"] / r1["liberadas_central"],
      "%", "2026-2035", "52 provincias", "C4", "2026-06-17", ["output/v5/A4 clasificacion_provincias", "INE 36726"])
    cl = r1["liberadas_central"] - r1["en_mun_sin_clase_central"]
    h("T2-H11", "Cuota en municipios A4 clase 1-2 sobre las liberadas en municipios con clase (703 municipios con precio)",
      100 * r1["en_mun_clase12_central"] / cl, 100 * r1["en_mun_clase12_central"] / cl, 100 * r1["en_mun_clase12_central"] / cl, "%",
      "2026-2035", "703 municipios clasificados", "C4", "2026-06-17", ["output/v5/A4 clasificacion_municipios", "INE Censo 2021"])
    h("T2-H12", "Cuota de las liberadas en municipios sin clase A4 (sin precio)", 100 * r1["en_mun_sin_clase_central"] / r1["liberadas_central"],
      100 * r1["en_mun_sin_clase_central"] / r1["liberadas_central"], 100 * r1["en_mun_sin_clase_central"] / r1["liberadas_central"], "%",
      "2026-2035", "municipios sin clasificar", "C4", "2026-06-17")
    h("T2-H13", "Herencias de vivienda inscritas al ano (media 2023-2025)", herencia, herencia, herencia, "viviendas/ano", "2023-2025",
      "52 provincias", "C4", "2025-12-31", ["INE ETDP 6154"])
    h("T2-H14", "Liberadas por fallecimiento en vivienda en propiedad al ano (modelo)", prop_muerte, prop_muerte, prop_muerte,
      "viviendas/ano", "2026-2035", "52 provincias", "C4", "2026-06-17")
    h("T2-H15", "Liberadas al ano frente a la necesidad central B1 (no se resta de ella)", 100 * a["liberadas_central"] / need,
      100 * a["liberadas_min"] / need_hi, 100 * a["liberadas_max"] / need_lo, "%", "2026-2035", "52 provincias", "C4", "2026-06-17",
      ["output/v5/B1"])
    json.dump(H, open(OUT / "hechos.json", "w"), indent=1, ensure_ascii=False)
    frase = ("La vivienda liberada NO se resta de la necesidad: la proyeccion de hogares del INE (tabla 54562) ya la descuenta; "
             "la sensibilidad X es un posible AUMENTO de la necesidad efectiva respecto a la que el INE da por absorbida.")
    res_json = {
        "rama": "v5_1/T2",
        "pregunta": "Cuantas viviendas libera el envejecimiento (fallecimiento y traslado a residencia) en 2026-2035 y cuantas llegan al mercado, donde y con que sensibilidad",
        "capa": "C4",
        "datos": FECHAS,
        "N": 52,
        "metodo": "Contabilidad de flujo por provincia: defunciones 75+ (proyeccion INE x riesgo de muerte 2024) x jefatura 65+ x disolucion, "
                  "con correccion por muertes en residencia, mas traslados a residencia de quien vivia solo; reparto a municipios por poblacion 65+ del Censo 2021; "
                  "tenencia ECV 65+ escalada con el Censo; fraccion de mercado con X = vacias y secundarias del Censo 2021. " + frase,
        "estimacion": {"liberadas_2026_2035": {"central": r1["liberadas_central"], "min": r1["liberadas_min"], "max": r1["liberadas_max"]},
                       "liberadas_anuales_2026_2035": {"central": a["liberadas_central"], "min": a["liberadas_min"], "max": a["liberadas_max"]},
                       "escenario_2036_2040": {"central": r2["liberadas_central"], "min": r2["liberadas_min"], "max": r2["liberadas_max"]},
                       "mercado_anual": {"central": a["mercado_central"], "min": a["mercado_min"], "max": a["mercado_max"]},
                       "no_llega_anual": {"central": a["no_llega_central"], "min": x_lo, "max": x_hi},
                       "aumento_necesidad_efectiva_pct": {"central": 100 * a["no_llega_central"] / need, "min": 100 * x_lo / need,
                                                          "max": 100 * x_hi / need, "estres_X50": 100 * stress / need},
                       "no_restar_de_necesidad": frase, "por_tipo_municipio_central_2026_2035": r1["por_tipo_central"]},
        "ic95": None, "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO",
        "diagnosticos": {"control_sumas": ctrl, "comparable_B1_fallecimiento_sin_ajuste_anual": a["comparable_B1_fallecimiento_sin_ajuste"],
                         "h65": h65, "tenencia_65_ECV": ten, "holm_bh": "no aplica: sin contraste de hipotesis; las especificaciones son escenarios de contabilidad"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": ["Rangos de supuestos, no intervalos de confianza.",
                  "Parametros de residencias (4-8 % de 75+, estancia 2,5-4 anos, 30-60 % solos, sobremortalidad x2): SIN DATO propio (Censo 2021 por edad en establecimientos colectivos e IMSERSO no accesibles); NO VERIFICADOS.",
                  "2036-2040 es escenario: mortalidad de 2024 constante (sesgo al alza), proyeccion INE corto plazo.",
                  "Tipo de municipio: regla propia (capital; resto con >=50.000 hab. del Censo 2021; resto). Atlas de Areas Urbanas no disponible (403). El reparto por municipio usa poblacion 65+ como proxy de 75+.",
                  "Solo defunciones de 75+ (como B1); no se cuentan 65-74.", frase,
                  "Destino posterior (venta/alquiler/uso) sin dato: no existe en el INE el seguimiento de la vivienda heredada."],
    }
    json.dump(res_json, open(OUT / "resultado.json", "w"), indent=1, ensure_ascii=False)
    fic = [
        {"id": "T2-V1", "tema": "Envejecimiento", "enunciado": "El envejecimiento resolvera el problema de la vivienda.", "capa": "C4",
         "magnitud": f"Liberadas por fallecimiento y traslado a residencia: {a['liberadas_central']:.0f} viviendas/ano central (rango {a['liberadas_min']:.0f}-{a['liberadas_max']:.0f}) en 2026-2035, "
                     f"frente a una necesidad central de {need:.0f} viviendas/ano (B1). Ya estan descontadas en la proyeccion de hogares del INE, asi que no restan necesidad. "
                     f"Llegan al mercado {a['mercado_central']:.0f}/ano ({a['mercado_min']:.0f}-{a['mercado_max']:.0f}). {100*r1['en_prov_clase12_central']/r1['liberadas_central']:.0f} % en provincias A4 clase 1-2.",
         "intervalo": f"{a['liberadas_min']:.0f} a {a['liberadas_max']:.0f} viviendas/ano (C4)", "cota": "—", "literatura": "—",
         "veredicto": "ANALIZADA, NO CONCLUYENTE",
         "regla": "Capa C4: parametros de residencias sin dato propio y destino de la vivienda liberada sin dato. Cifra de orden de magnitud; no se resta de la necesidad.",
         "limites": "Solo 75+; reparto municipal por poblacion 65+; mortalidad 2024 constante; no contrasta la calidad ni la ubicacion de la vivienda.",
         "evidencia": ["output/v5_1/T2/tablas/liberadas_provincia.csv", "output/v5_1/T2/resultado.json"]},
        {"id": "T2-V2", "tema": "Herencias", "enunciado": "Las herencias liberaran vivienda suficiente.", "capa": "C4",
         "magnitud": f"Herencias inscritas: {herencia:.0f} viviendas/ano (2023-2025, INE ETDP, fuente unica: C4). Liberadas por fallecimiento en propiedad: {prop_muerte:.0f}/ano (modelo, C4). "
                     f"Fraccion que llega al mercado {100*a['mercado_min']/a['liberadas_min']:.0f}-{100*a['mercado_max']/a['liberadas_max']:.0f} % (supuesto C4: X entre vacias y vacias+secundarias del Censo 2021). "
                     f"No llegan {x_lo:.0f}-{x_hi:.0f} viviendas/ano, un aumento posible de la necesidad efectiva de {100*x_lo/need:.0f}-{100*x_hi/need:.0f} % (prueba de estres X=50 %: {100*stress/need:.0f} %).",
         "intervalo": f"{a['mercado_min']:.0f} a {a['mercado_max']:.0f} viviendas/ano al mercado (C4)", "cota": "—", "literatura": "—",
         "veredicto": "ANALIZADA, NO CONCLUYENTE",
         "regla": "El dato registral de las herencias es de fuente unica (INE) y el destino posterior (venta, alquiler, uso familiar, vacia) no tiene dato: la cifra de mercado es C4 por la menor capa de sus componentes. La suficiencia depende de ese destino.",
         "limites": "Una inscripcion de herencia puede incluir segundas viviendas o vacias; no hay seguimiento de la vivienda heredada.",
         "evidencia": ["output/v5_1/T2/tablas/liberadas_provincia.csv", "data/raw/v5_1/ine_t2_t6154.csv"]}]
    json.dump(fic, open(OUT / "fichas_verificador.json", "w"), indent=1, ensure_ascii=False)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    reg = econ_utils.Registry(OUT / "registro.csv")
    nombres = pd.read_csv(RAIZ / "output/v5/B1/tablas/B1_provincias.csv", dtype={"cod_prov": str})
    cods = sorted(nombres.cod_prov)
    if SMOKE:
        cods = ["46", "28", "52"]
    nom = dict(zip(nombres.cod_prov, nombres.provincia))
    kcod = {c: b1.kn(nom[c]) for c in cods}
    pp, pnac = b1.lee_proy_pob()
    mort = b1.lee_mortalidad()
    qk5 = mort.pivot(index="k", columns="e0", values="valor") / 1000.0
    qk = 1.0 - (1.0 - qk5.clip(upper=0.999)) ** 0.2
    qk[95] = qk[90]
    jef = pd.read_csv(RAIZ / "output/v4/M2/tablas/tasas_jefatura_4grupos.csv")
    h65 = float(jef["65+"].iloc[-1])
    ten = tenencia_65()
    mun = tipos_municipio()
    her = herencias()
    a4p = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_provincias.csv", dtype={"cod_prov": str}).set_index("cod_prov")
    bp = nombres.set_index("cod_prov")
    cat_nac = {}
    # tasas nacionales de tenencia del Censo (para escalar la ECV 65+ por municipio)
    nat = mun[["ppal", "propiedad", "alquiler"]].sum()
    s_own_nat, s_alq_nat = nat.propiedad / nat.ppal, nat.alquiler / nat.ppal
    filas = []
    for per, (y0, y1) in PER.items():
        for c in cods:
            k = kcod[c]
            D, pobanos, p0 = muertes_prov(pp, qk, k, y0, y1)
            # Ruta fallecimiento (formula B1: h65 * factor * disolucion * defunciones 75+); correccion por muertes en residencia
            def total(s_d, s_r, hf, dd):
                r = R_INST[s_r]
                s_res = r * RR_MORT / (r * RR_MORT + 1 - r)           # cuota de defunciones 75+ ocurridas en residencia
                solo_d = SOLO[s_d]
                muerte = h65 * hf * dd * D * (1 - s_res * solo_d)
                entra = pobanos * (R_INST[s_r] / ESTANCIA[s_r]) * SOLO[s_r]   # entradas por ano * anos * fraccion que vivia solo
                return muerte, entra
            # min: menos entradas y mayor correccion por muertes en residencia; max al reves
            m_lo, e_lo = total("max", "min", H_FACT[0], DISOL[0])
            m_ce, e_ce = total("central", "central", H_FACT[1], DISOL[1])
            m_hi, e_hi = total("min", "max", H_FACT[2], DISOL[2])
            m_b1 = h65 * H_FACT[1] * DISOL[1] * D
            v = {"min": (m_lo, e_lo), "central": (m_ce, e_ce), "max": (m_hi, e_hi)}
            m = mun[mun.cod_prov == c].copy()
            w = m.pob65 / m.pob65.sum()
            # tenencia por municipio: ECV 65+ escalada con la estructura relativa del Censo
            own = ten["propiedad"] * (m.propiedad / m.ppal / s_own_nat).fillna(1)
            alq = ten["alquiler"] * (m.alquiler / m.ppal / s_alq_nat).fillna(1)
            ces = pd.Series(ten["cesion"], index=m.index)
            tot = own + alq + ces
            own, alq, ces = own / tot, alq / tot, ces / tot
            b = bp.loc[c]
            x_lo = b.vacias_2021 / b.viv_total_2021
            x_hi = (b.vacias_2021 + b.esporadicas_2021) / b.viv_total_2021
            # fraccion que llega al mercado: propietaria 1-X; alquilada 0,8-1,0 (vuelve al titular); cesion 0,3-0,8
            fm_min = own * (1 - x_hi) + alq * 0.8 + ces * 0.3
            fm_max = own * (1 - x_lo) + alq * 1.0 + ces * 0.8
            pres_m = m.clase_2021_2025.isin([1, 2])
            for t in ("capital", "entorno_grande", "resto"):
                q = m.tipo == t
                ww = w[q]
                if ww.sum() == 0 and True:
                    filas.append(dict(cod_prov=c, provincia=nom[c], tipo_municipio=t, periodo=per, n_municipios=0))
                    continue
                r = dict(cod_prov=c, provincia=nom[c], tipo_municipio=t, periodo=per, n_municipios=int(q.sum()),
                         clase_A4_prov=int(a4p.loc[c, "clase_2021_2025"]), prov_con_necesidad=bool(a4p.loc[c, "clase_2021_2025"] in (1, 2)),
                         peso_pob65=float(ww.sum()))
                for s in ("min", "central", "max"):
                    r[f"liberadas_{s}"] = float(ww.sum() * (v[s][0] + v[s][1]))
                r["via_fallecimiento_central"] = float(ww.sum() * v["central"][0])
                r["via_residencia_central"] = float(ww.sum() * v["central"][1])
                r["comparable_B1_fallecimiento_sin_ajuste"] = float(ww.sum() * m_b1)
                wp = (ww * own[q]).sum() / ww.sum()
                r["frac_propietaria"] = float(wp)
                r["frac_alquilada"] = float((ww * alq[q]).sum() / ww.sum())
                r["frac_cesion"] = float((ww * ces[q]).sum() / ww.sum())
                r["fraccion_mercado_min"] = float((ww * fm_min[q]).sum() / ww.sum())
                r["fraccion_mercado_max"] = float((ww * fm_max[q]).sum() / ww.sum())
                r["frac_en_municipios_clase12"] = float((ww * pres_m[q]).sum() / ww.sum())
                r["frac_en_municipios_sin_clase"] = float((ww * m.clase_2021_2025[q].isna()).sum() / ww.sum())
                r["herencias_viv_anual_2023_25_prov"] = float(her.loc[k, [2023, 2024, 2025]].mean() * ww.sum())
                filas.append(r)
            reg.log("T2", f"liberadas_{c}_{per}", "L=h65*hf*disol*D75*(1-s_res*solo)+pob75*r/estancia*solo", y0, y1,
                    len(m), np.nan, np.nan, np.nan, coef_interes=v["central"][0] + v["central"][1],
                    notas="especificacion de contabilidad; sin contraste de hipotesis, p no aplica")
    t = pd.DataFrame(filas)
    t = t[t.n_municipios > 0].copy()
    ncols = [c for c in t.columns if c.startswith("liberadas_")] + ["via_fallecimiento_central", "via_residencia_central",
                                                                      "comparable_B1_fallecimiento_sin_ajuste"]
    t.to_csv(OUT / "tablas" / "liberadas_provincia.csv", index=False, float_format="%.4f")
    t["mercado_min"] = t.liberadas_min * t.fraccion_mercado_min
    t["mercado_max"] = t.liberadas_max * t.fraccion_mercado_max
    t["mercado_central"] = t.liberadas_central * (t.fraccion_mercado_min + t.fraccion_mercado_max) / 2
    t["no_llega_central"] = t.liberadas_central - t.mercado_central
    t["no_llega_min"] = t.liberadas_central * (1 - t.fraccion_mercado_max)   # X minimo
    t["no_llega_max"] = t.liberadas_central * (1 - t.fraccion_mercado_min)   # X maximo
    # --- agregados
    res = {}
    for per, (y0, y1) in PER.items():
        s = t[t.periodo == per]
        n = y1 - y0 + 1
        res[per] = {
            "anios": n,
            **{k: float(s[k].sum()) for k in ncols + ["mercado_min", "mercado_central", "mercado_max", "no_llega_central", "no_llega_min", "no_llega_max"]},
            "por_tipo_central": {k: float(v) for k, v in s.groupby("tipo_municipio").liberadas_central.sum().items()},
            "en_prov_clase12_central": float(s[s.prov_con_necesidad].liberadas_central.sum()),
            "en_mun_clase12_central": float((s.liberadas_central * s.frac_en_municipios_clase12).sum()),
            "en_mun_sin_clase_central": float((s.liberadas_central * s.frac_en_municipios_sin_clase).sum()),
            "herencias_anual_2023_25_modelo": float(s.herencias_viv_anual_2023_25_prov.sum()),
            "propietarias_central": float((s.liberadas_central * s.frac_propietaria).sum()),
            "alquiladas_central": float((s.liberadas_central * s.frac_alquilada).sum()),
            "cesion_central": float((s.liberadas_central * s.frac_cesion).sum()),
        }
    # --- control de sumas
    ctrl = []
    p1 = t[t.periodo == "2026-2035"]
    prov = p1.groupby("cod_prov").liberadas_central.sum()
    ctrl.append({"tabla": "liberadas_central_2026_2035: suma tipos = suma provincias", "suma_provincial": float(prov.sum()),
                 "nacional": float(p1.liberadas_central.sum()), "tolerancia_rel": 1e-9})
    # pob 75+ 2026: suma provincial vs nacional (INE)
    p75 = pp[(pp.e >= 75) & (pp.anyo == 2026) & pp.k.isin(kcod.values())].valor.sum()
    pn = pd.read_csv(b1.V5 / "ine_b1_t36726_proy_poblacion_prov.csv")
    mm = pn.nombre.str.extract(r"^Total\. Población\. (.+?)\. Proyección a corto plazo\. (\d+)")
    nac75 = float(pn[(mm[0] == "Total Nacional") & (mm[1].astype(float) >= 75) & (pn.anyo == 2026)].valor.sum())
    ctrl.append({"tabla": "poblacion_75mas_2026 (suma provincial vs Total Nacional, INE 36726; 100+ incluido)",
                 "suma_provincial": float(p75), "nacional": nac75, "tolerancia_rel": 1e-3})
    hn = pd.read_csv(RAIZ / "data/raw/v5_1/ine_t2_t6154.csv")
    hn = hn[hn.nombre.str.startswith("Total Nacional. Herencia. Total viviendas")].set_index("anyo").valor
    ctrl.append({"tabla": "herencias_viviendas_2025 (suma 52 provincias vs Total Nacional ETDP)",
                 "suma_provincial": float(her.loc[list(kcod.values()), 2025].sum()), "nacional": float(hn.loc[2025]),
                 "tolerancia_rel": 0.001})
    ctrl.append({"tabla": "pesos_municipio_suman_1 (por provincia, tipos)", "suma_provincial": float(p1.groupby("cod_prov").peso_pob65.sum().sum()),
                 "nacional": float(len(prov)), "tolerancia_rel": 1e-9})
    for cc in ctrl:
        cc["ok"] = bool(cc["nacional"] is None or abs(cc["suma_provincial"] - cc["nacional"]) <= cc["tolerancia_rel"] * abs(cc["nacional"]))
    json.dump(ctrl, open(OUT / "control_sumas.json", "w"), indent=1, ensure_ascii=False)
    json.dump({"resumen": res, "ten65": ten, "h65": h65}, open(OUT / "tablas" / "agregados.json", "w"), indent=1, ensure_ascii=False)
    t.to_csv(OUT / "tablas" / "liberadas_detalle.csv", index=False, float_format="%.4f")
    reg.flush()
    entregables(res, bp, t, ten, h65, ctrl)
    print(json.dumps(res["2026-2035"], indent=1, ensure_ascii=False))
    print(all(c["ok"] for c in ctrl))


if __name__ == "__main__":
    main()
