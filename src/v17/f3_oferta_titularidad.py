"""V17 · Fase 3 · Auditoría del grupo «oferta_titularidad». ANÁLISIS A POSTERIORI (capa C4).

Pruebas mínimas de las filas grandes_tenedores, itp_discurso, itp_medida, mas_oferta, vacias y vivienda_publica (docs/v17/plan.md,
fase 3, punto 2). Contabilidad, cotas e ilustraciones con parámetros de la literatura: nada de lo calculado aquí es un efecto causal.
Determinista, sin red, SEED = 20261010. Guarda de fuga v6 (docs/v17/decisiones.md, K5): toda lectura por debajo del nivel nacional
(CCAA, provincia, municipio) pasa por holdout.excluir_sellados_v6(); los totales nacionales (Catastro total, Censo nacional, OCDE)
se leen completos. No se lee data/sealed ni se ejecuta evaluate_*.
data/raw se lee en solo lectura. Las cifras de documento (Banco de España, O-HB, OCDE, literatura) se toman de
docs/v17/fuentes/*.md y de las fichas de literatura; no se recalculan.
Uso: python3 src/v17/f3_oferta_titularidad.py  ->  output/v17/auditoria/oferta_titularidad_hechos.json
"""
from __future__ import annotations

import json
from pathlib import Path

import sys

import duckdb
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src import holdout  # noqa: E402
OUT = ROOT / "output" / "v17" / "auditoria"
CAT = ROOT / "data/raw/v11/catastro_titularidad"
CENSO_VAC = ROOT / "data/raw/v11/ine_censo2021/censo2021_tpx59531.csv"
CENSO_TEN = ROOT / "data/raw/v11/ine_censo2021/censo2021_tpx59537.csv"
OCDE_PH42 = ROOT / "data/raw/v17/parque_social/oecd_ahd_PH4-2_social_rental_housing_stock.xlsx"
UE27 = {"Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
        "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania",
        "Slovak republic", "Slovenia", "Spain", "Sweden"}
CCAA_SELLADAS_V6 = set(holdout.ccaa_selladas_v6())   # ocho CCAA de K8 (bloques sellados de v6)
PROTEGIDA = ROOT / "data/raw/mivau_v2_protegida.csv"
INFERENCIA = ROOT / "output/v17/lectura_bde/v15_v16_micro/inferencia.csv"
D3 = ROOT / "output/v17/d3"
HECHOS_BASE = ROOT / "data/base/hechos.parquet"
FICHAS = "output/v17/auditoria/filas"

# Cifras de documento (fuente en cada hecho). No se recalculan.
DOC = {
    "bde_pf_11mas_alquiler": 2.4,        # % viviendas alquiladas de personas físicas con 11+ viviendas (BdE IA 2025, cuadro 2.11)
    "bde_particulares_alquiler": 90.0,   # «alrededor del 90 %» del alquiler en particulares (BdE IA 2025, p. 169)
    "ohb_bcn_parque_total": 17.1,        # O-HB 2022, gran tenedor sobre parque total de Barcelona ciudad, 1-1-2021
    "ohb_bcn_alquiler": 36.1,            # O-HB, sobre alquiler habitual
    "ohb_bcn_admin_alquiler": 4.44,      # O-HB 2022, figura 5: administraciones sobre el alquiler habitual estimado
    "bde_tramos_2mas": (21.8, 18.9, 6.2, 2.4),  # BdE IA 2025, cuadro 2.11: 2, 3-5, 6-10, 11+ viviendas
    "mivau_publico_alquiler": 318_000,   # MIVAU, Boletín Especial Vivienda Social 2024
    "bde_terminadas_2025": 92_000,       # BdE IA 2025, pp. 124 y 126 (verificado por el coordinador)
    "bde_potencial_barcelona": 120_000, "bde_potencial_sevilla": 163_000,
    "bde_ejecucion_sevilla": 0.28,       # BdE IA 2025, pp. 157-158: ejecución de lo previsto en el área de Sevilla
    # Empleo (encargo final, B): supuestos explícitos SIN fuente verificada, rotulados como tales
    "cuota_resid_nueva_2007": (0.45, 0.65),   # parte de los ocupados de la rama F en edificación residencial nueva, 2007
    "cuota_resid_nueva_hoy": (0.15, 0.30),    # ídem 2015-2019 y 2025 (más obra civil, no residencial y rehabilitación)
    "industrializacion": (0.0, 0.2, 0.4),     # reducción de horas por vivienda con industrialización (escenario)
    "ocde_es_social_pct": 1.13, "ocde_es_social_viv": 290_000, "ocde_ue_social_pct": 7.99,
    "ocde_fr": 14.0, "ocde_at": 23.6, "ocde_nl": 34.1, "ocde_de": 2.6, "ocde_it": 2.4, "ocde_pt": 1.06,
    "segu_reduccion_relativa": 13.0,     # Segú (2020): −13 % de la tasa de vacancia (relativa), Francia 1997-2001
    "mense_elasticidad": -0.19,          # Mense (2025): +1 % de oferta → −0,19 % del alquiler medio (Alemania, corto plazo)
    "li_elasticidad": -0.10,             # Li (2022): +10 % de parque local → −1 % de alquiler (Nueva York, NO VERIFICADA)
    "dolls_precio_por_punto": -0.03,     # Dolls et al. (2025): −3 % de precio por punto de tipo (Alemania)
    "fritzsche_volumen_por_punto": -0.07,  # Fritzsche y Vandrei (2019): −7 % de transacciones por punto
}
HECHOS: list[dict] = []


# Cobertura territorial real de cada cifra (por prefijo del id) y tipo de rango cuando hay min y max
COBERTURA = [
    ("CAT-GT-BCN", "municipio de Barcelona (08019), Catastro"),
    ("CAT-GT-PROV-MEDIANA", "38 provincias de régimen común sin bloques sellados v6"),
    ("CAT-GT-", "España de régimen común (sin País Vasco ni Navarra), fichero nacional del Catastro"),
    ("COTA-GT-", "España: alquiler de vivienda habitual (BdE, territorio fiscal común) y hogares en alquiler (Censo 2021, nacional)"),
    ("BDE-MULTI", "España, territorio fiscal común (AEAT)"),
    ("OHB-", "Barcelona ciudad"),
    ("VAC-6PROV", "provincias de Barcelona, València, Alicante, Tarragona, Málaga y Almería"),
    ("VAC-6CAP", "capitales de esas 6 provincias (no selladas)"),
    ("VAC-SEGU", "provincias de Barcelona, València, Alicante, Tarragona, Málaga y Almería y sus capitales"),
    ("VAC-PRESION", "41 provincias sin bloques sellados v6"),
    ("VAC-TASA-TERCIL", "41 provincias sin bloques sellados v6, por terciles de déficit por vivienda"),
    ("VAC-", "provincias sin bloques sellados v6 (municipios listados en la tabla 59531 y filas «Resto de provincia»)"),
    ("ITP-", "8 CCAA del panel de entrenamiento de Q6 (V16)"),
    ("PUB-UE", "19 países de la UE-27 con dato en OCDE PH4.2"),
    ("PUB-", "España (agregado nacional)"),
    ("OFERTA-ELASTICIDAD", "CCAA mediana de las 9 CCAA sin bloques sellados v6 (parque del Censo 2021)"),
    ("OFERTA-", "España (agregado nacional)"),
    ("EMPLEO-", "España (agregado nacional)"),
    ("SUELO-BARCELONA", "área urbana de Barcelona (BdE) frente a la provincia de Barcelona"),
    ("SUELO-SEVILLA", "área urbana de Sevilla (BdE) frente a la provincia de Sevilla"),
    ("D32-IPV", "9 CCAA sin bloques sellados v6"),
    ("D32-SERPAVI", "38 provincias sin bloques sellados v6"),
]
TIPO_RANGO = {"CAT-GT-PROV-MEDIANA-2026": "referencias", "CAT-GT-BCN-2024": "referencias", "COTA-GT-ALQUILER-NACIONAL": "rango",
              "COTA-GT-ALQUILER-CON-PUBLICA": "rango", "COTA-GT-ALQUILER-PRIVADOS": "rango", "VAC-6CAP-VACIAS": "referencias",
              "PUB-BRECHA-UE": "rango", "OFERTA-DEFICIT-SOBRE-PARQUE": "rango", "OFERTA-MENSE-ILUSTRACION": "rango",
              "OFERTA-ILUSTRACION-RANGO": "referencias", "OFERTA-SENSIBILIDAD-5A": "rango", "OFERTA-SENSIBILIDAD-10A": "rango",
              "SUELO-BARCELONA-RATIO": "rango", "SUELO-SEVILLA-RATIO": "rango", "D32-IPV-CCAA-SIN-SELLADAS": "rango",
              "D32-SERPAVI-REAL-2015-2024": "referencias"}


def cobertura_de(id_: str) -> str:
    return next(c for pref, c in COBERTURA if id_.startswith(pref))


def hecho(id_, indicador, valor, unidad, periodo, fuentes, lectura, ficha, minimo=None, maximo=None, nota="", tipo=None, cobertura=None):
    """tipo: «rango» (intervalo del mismo valor) o «referencias» (puntos de referencia de otra cosa); «sin rango» si falta min o max."""
    assert lectura in ("OF", "hecho", "cota", "asociación", "juicio experto")
    cobertura = cobertura or cobertura_de(id_)
    tipo = tipo or TIPO_RANGO.get(id_)
    assert cobertura and "véase" not in cobertura.lower(), id_
    f = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)
    if f(minimo) is None or f(maximo) is None:
        tipo = "sin rango"
    assert tipo in ("rango", "referencias", "sin rango"), id_
    HECHOS.append({"id": f"V17-AUD-OT-{id_}", "indicador": indicador, "valor": f(valor), "min": f(minimo), "max": f(maximo),
                   "tipo_rango": tipo, "cobertura": cobertura,
                   "unidad": unidad, "periodo": periodo, "fuentes": fuentes, "capa": "C4", "lectura_v17": lectura,
                   "ficha": (f"output/v17/auditoria/preguntas/{ficha}.md" if ficha.startswith("D3-") else f"{FICHAS}/{ficha}.md"), "nota": "a posteriori" + (f"; {nota}" if nota else "")})


def selladas() -> set[str]:
    return set(holdout.provincias_selladas_v6())


def sin_selladas(df: pd.DataFrame, col: str, nivel: str) -> pd.DataFrame:
    return holdout.excluir_sellados_v6(df, col, nivel)


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")


TRAMOS_GRANDES = ["HASTA_25", "HASTA_100", "MAYOR_100"]   # más de 10 inmuebles por titular
TIPOS = ["PF", "PJ", "PE", "PD"]


def grandes(df: pd.DataFrame) -> pd.Series:
    return sum(df[f"I_U_{t}_{tr}"] for t in TIPOS for tr in TRAMOS_GRANDES)


# ---------------------------------------------------------------- grandes tenedores
def titularidad(sel: set[str]) -> dict:
    tot = pd.read_csv(CAT / "p_spi_total_v.csv.gz")
    tpf = pd.read_csv(CAT / "p_spi_total_v_tpf.csv.gz")
    res = {}
    for _, r in tot.iterrows():
        a = int(r.anio_fichero)
        g = sum(r[f"I_U_{t}_{tr}"] for t in TIPOS for tr in TRAMOS_GRANDES)
        g100 = sum(r[f"I_U_{t}_MAYOR_100"] for t in TIPOS)
        pe = sum(r[f"I_U_PE_{tr}"] for tr in TRAMOS_GRANDES)
        tit = sum(r[f"U_{t}_{tr}"] for t in TIPOS for tr in TRAMOS_GRANDES)
        res[a] = dict(g=g, inm=r.INMUEBLES, g100=g100, pe=pe, tit=tit)
    t = tpf.set_index("anio_fichero")
    for a in res:
        tr_s = ["25I", "100I", "MAS100"]
        res[a]["soc"] = sum(t.loc[a, f"I_U_{x}_SOCIEDADES"] for x in tr_s)
        res[a]["fis"] = sum(t.loc[a, f"I_U_{x}_FIS_NA"] + t.loc[a, f"I_U_{x}_FIS_EX"] for x in tr_s)
    a = 2026
    r = res[a]
    fu = "Catastro, estadística de titularidad (data/raw/v11/catastro_titularidad/p_spi_total_v*.csv.gz)"
    hecho("CAT-GT-PARQUE-2026", "Viviendas de titulares con más de 10 inmuebles residenciales sobre el parque catastral (régimen común)",
          100 * r["g"] / r["inm"], "% del parque", "2026", fu, "OF", "grandes_tenedores",
          minimo=100 * res[2025]["g"] / res[2025]["inm"], nota="min = edición 2025; incluye todos los tipos de titular")
    hecho("CAT-GT-MAS100-2026", "Viviendas de titulares con más de 100 inmuebles sobre el parque", 100 * r["g100"] / r["inm"],
          "% del parque", "2026", fu, "OF", "grandes_tenedores")
    hecho("CAT-GT-SIN-PUBLICAS-2026", "Ídem excluyendo entidades públicas (PE)", 100 * (r["g"] - r["pe"]) / r["inm"], "% del parque",
          "2026", fu, "OF", "grandes_tenedores", nota="PE se identifica con administraciones por su coincidencia con la columna AAPP del fichero TPF")
    hecho("CAT-GT-SOCIEDADES-2026", "Viviendas de sociedades con más de 10 inmuebles sobre el parque", 100 * r["soc"] / r["inm"],
          "% del parque", "2026", fu, "OF", "grandes_tenedores")
    hecho("CAT-GT-FISICAS-2026", "Viviendas de personas físicas con más de 10 inmuebles sobre el parque", 100 * r["fis"] / r["inm"],
          "% del parque", "2026", fu, "OF", "grandes_tenedores")
    hecho("CAT-GT-TITULARES-2026", "Titulares (NIF) con más de 10 inmuebles residenciales", r["tit"], "titulares", "2026", fu, "OF",
          "grandes_tenedores", nota="por NIF; un grupo con varias sociedades aparece fragmentado")
    # Distribución provincial (tramos contados dentro de la provincia: cota inferior), sin provincias selladas v6
    mu = sin_selladas(pd.read_csv(CAT / "p_spi_mun_v.csv.gz", dtype={"CODINE": str}), "CODINE", "municipio")
    mu["prov"] = mu.CODINE.str[:2]
    cod = mu.groupby("PROVINCIA").prov.first()   # nombre de provincia → código INE (solo provincias no selladas)
    pv_all = pd.read_csv(CAT / "p_spi_prov_v.csv.gz")
    pv_all["prov"] = pv_all.PROVINCIA.map(cod)
    pv_all = sin_selladas(pv_all.dropna(subset=["prov"]), "prov", "provincia")   # las selladas no tienen código: fuera
    pv = pv_all[pv_all.anio_fichero == 2026].copy()
    pv["cuota"] = 100 * grandes(pv) / pv.INMUEBLES
    q = pv.cuota.quantile([0.1, 0.5, 0.9])
    mx = pv.loc[pv.cuota.idxmax()]
    hecho("CAT-GT-PROV-MEDIANA-2026", "Cuota de viviendas de titulares con más de 10 inmuebles, mediana provincial (tramo contado en la provincia)",
          q[0.5], "% del parque provincial", "2026", fu, "OF", "grandes_tenedores", minimo=q[0.1], maximo=q[0.9],
          nota=f"min = P10, max = P90; {len(pv)} provincias sin muestra sellada v6; máximo {mx.PROVINCIA} {mx.cuota:.1f} %; cota inferior")
    res["prov_max"] = (mx.PROVINCIA, mx.cuota)
    res["n_prov"] = len(pv)
    # Barcelona ciudad frente al O-HB (parque total)
    b = mu[(mu.CODINE == "08019")].set_index("anio_fichero")
    bc = {a: 100 * float(grandes(b.loc[[a]]).iloc[0]) / float(b.loc[a, "INMUEBLES"]) for a in b.index}
    hecho("CAT-GT-BCN-2024", "Barcelona ciudad: viviendas de titulares con más de 10 inmuebles en el municipio, sobre el parque catastral",
          bc[2024], "% del parque municipal", "2024", fu + "; O-HB (2022) da 17,1 % con datos a 1-1-2021 y otra agregación",
          "OF", "grandes_tenedores", minimo=min(bc.values()), maximo=max(bc.values()), nota="min y max = ediciones 2024-2026")
    res["bcn"] = bc
    # Cota del peso de los grandes tenedores en el ALQUILER nacional (Manski: supuestos explícitos)
    pf, p = DOC["bde_pf_11mas_alquiler"], DOC["bde_particulares_alquiler"] / 100
    lo, hi = p * pf, p * pf + (1 - p) * 100
    lo_s, hi_s = 0.85 * pf, 0.85 * pf + 15.0
    hecho("COTA-GT-ALQUILER-NACIONAL", "Cota del peso de los titulares con 11+ viviendas en el alquiler de vivienda habitual, España",
          None, "% del alquiler habitual", "2024", "BdE, Informe Anual 2025, cuadro 2.11 y p. 169 (datos AEAT)", "cota", "grandes_tenedores",
          minimo=lo, maximo=hi, nota=("supuestos: particulares = 90 % del alquiler; cota inferior = ninguna persona jurídica es gran tenedor; "
                                      f"cota superior = todas lo son; con particulares = 85 %: {lo_s:.1f}-{hi_s:.1f} %"))
    res["cota"] = (lo, hi, lo_s, hi_s)
    # ¿Cómo cuenta el Catastro el tramo? Con la guarda v6 no se suman provincias selladas: se compara, en las provincias no
    # selladas, el fichero provincial con la suma de sus municipios. Si el provincial supera a la suma municipal, cada fichero
    # cuenta el tramo por NIF dentro de su propio ámbito (y el nacional, en todo el territorio común).
    for a in (2025, 2026):
        s_prov = float(grandes(pv_all[pv_all.anio_fichero == a]).sum())
        s_mun = float(grandes(mu[mu.anio_fichero == a]).sum())
        res[f"nif_{a}"] = (s_prov, s_mun)
    hecho("CAT-GT-PROV-FRENTE-SUMA-MUN-2026", "Viviendas de titulares con más de 10 inmuebles: ficheros provinciales frente a la suma de sus municipios",
          res["nif_2026"][0] / res["nif_2026"][1], "cociente", "2026", fu, "OF", "grandes_tenedores",
          cobertura="provincias de régimen común sin bloques sellados v6",
          nota=(f"suma provincial {res['nif_2026'][0]:,.0f}; suma municipal {res['nif_2026'][1]:,.0f}; un cociente > 1 indica que cada fichero "
                "cuenta el tramo por NIF dentro de su ámbito; sustituye a CAT-GT-TOTAL-FRENTE-SUMA-PROV-2026, retirada porque sumaba "
                "provincias selladas"))
    # Ronda 1: cota con la vivienda pública como suelo explícito y cota aparte de los PRIVADOS con más de 10
    alq = float(num(pd.read_csv(CENSO_TEN, sep=";", dtype=str, encoding="utf-8-sig")
                    .query("`Régimen de tenencia de la vivienda` == 'En alquiler' and `Tamaño del hogar` == 'Total (tamaño del hogar)'")["Total"]).iloc[0])
    pub = {"Catastro PE >10 (2026)": float(r["pe"]), "OCDE PH4.2 (2019)": float(DOC["ocde_es_social_viv"]), "MIVAU (2023)": float(DOC["mivau_publico_alquiler"])}
    grid = []
    for pp in (0.85, 0.90, 0.95):
        for k, v_ in pub.items():
            ps = 100 * v_ / alq
            no_part = 100 * (1 - pp)
            grid.append(dict(p=pp, fuente_pub=k, pub=ps, total_lo=pp * pf + min(ps, no_part), total_hi=pp * pf + no_part,
                             priv_lo=pp * pf, priv_hi=pp * pf + max(0.0, no_part - ps), coherente=ps <= no_part))
    g = pd.DataFrame(grid)
    res["grid"] = g
    c = g[g.p == 0.90]
    hecho("COTA-GT-ALQUILER-CON-PUBLICA", "Cota de los titulares con más de 10 viviendas en el alquiler habitual con la vivienda pública como suelo explícito",
          None, "% del alquiler habitual", "2021-2024", "BdE IA 2025 cuadro 2.11; INE Censo 2021 (hogares en alquiler); Catastro; OCDE PH4.2; MIVAU 2024",
          "cota", "grandes_tenedores", minimo=c.total_lo.min(), maximo=c.total_hi.max(),
          nota=(f"denominador: {alq:,.0f} hogares en alquiler (Censo 2021); vivienda pública = {c.pub.min():.1f}-{c.pub.max():.1f} % del alquiler; "
                f"particulares = 90 %; con 85-95 %: {g.total_lo.min():.1f}-{g.total_hi.max():.1f} %; universos no idénticos (AEAT frente a Censo)"))
    hecho("COTA-GT-ALQUILER-PRIVADOS", "Cota de los titulares PRIVADOS (personas físicas y jurídicas) con más de 10 viviendas en el alquiler habitual",
          None, "% del alquiler habitual", "2021-2024", "ídem", "cota", "grandes_tenedores", minimo=c.priv_lo.min(), maximo=c.priv_hi.max(),
          nota=(f"particulares = 90 %; con 85-95 %: {g.priv_lo.min():.1f}-{g.priv_hi.max():.1f} %; con MIVAU la vivienda pública "
                "agota el 10 % no particular, señal de que los universos no casan"))
    multi_bde = sum(DOC["bde_tramos_2mas"])
    hecho("BDE-MULTIARRENDADORES-2024", "Viviendas alquiladas por personas físicas con 2 o más viviendas (suma de tramos del BdE)", multi_bde,
          "% de las viviendas alquiladas por personas físicas", "2024", "BdE IA 2025 cuadro 2.11 (AEAT)", "OF", "grandes_tenedores",
          nota="el informe 1 del Ministerio de Derechos Sociales con IFS-CSIC da 52,8 % (2023, Panel de Hogares): fuente, año y universo distintos")
    res["multi_bde"] = multi_bde
    hecho("OHB-BCN-GT-SIN-ADMINISTRACIONES", "Barcelona ciudad: grandes tenedores sin administraciones públicas sobre el alquiler habitual estimado",
          DOC["ohb_bcn_alquiler"] - DOC["ohb_bcn_admin_alquiler"], "% del alquiler habitual", "1-1-2021",
          "O-HB (2022), figuras 3 y 5 (36,1 % menos 4,44 % de administraciones)", "OF", "grandes_tenedores",
          nota="solo Barcelona ciudad; las administraciones son el 12,3 % de las viviendas de alquiler de grandes tenedores")
    res["y"] = res[2026]
    return res


# ---------------------------------------------------------------- vacías
def vacias(sel: set[str]) -> dict:
    v = pd.read_csv(CENSO_VAC, sep=";", dtype=str, encoding="utf-8-sig")
    v.columns = ["nac", "ccaa", "prov", "mun", "cat", "val"]
    v["val"] = num(v.val)
    m = v[v.mun.notna() & (v.mun.str.strip() != "")].copy()
    m["cmun"] = m.mun.str[:5]
    w = m.pivot_table(index="cmun", columns="cat", values="val", aggfunc="first")
    w = w.rename(columns={"Viviendas totales": "tot", "Viviendas vacías": "vac", "Viviendas de uso esporádico": "esp"})
    w["cprov"] = w.index.str[:2]
    w = sin_selladas(w.reset_index(), "cmun", "municipio").set_index("cmun").dropna(subset=["tot", "vac"])
    # Las filas «xx999 Resto de <provincia>» agregan los municipios pequeños que la tabla no lista: se separan
    resto = w[w.index.str.endswith("999")].copy()
    w = w[~w.index.str.endswith("999")].copy()
    w["tasa"] = 100 * w.vac / w.tot
    fu = "INE, Censo 2021, tabla 59531 (viviendas vacías por consumo eléctrico; data/raw/v11/ine_censo2021)"
    bins = [0, 2_000, 10_000, 50_000, np.inf]
    lab = ["<2.000", "2.000-10.000", "10.000-50.000", ">50.000"]
    w["tam"] = pd.cut(w.tot, bins=bins, labels=lab, right=False)
    g = w.groupby("tam", observed=True).agg(tot=("tot", "sum"), vac=("vac", "sum"), n=("tot", "size"))
    g["tasa"] = 100 * g.vac / g.tot
    g["cuota_vac"] = 100 * g.vac / g.vac.sum()
    for k, idk in zip(lab, ["T1", "T2", "T3", "T4"]):
        hecho(f"VAC-TASA-{idk}", f"Tasa de vacancia por consumo eléctrico, municipios con {k} viviendas", g.loc[k, "tasa"],
              "% de las viviendas", "2021", fu, "OF", "vacias", nota=f"{int(g.loc[k, 'n'])} municipios; {g.loc[k, 'cuota_vac']:.1f} % de las vacías de la muestra; sin provincias selladas v6; la tabla lista {len(w)} municipios y agrupa el resto en filas «Resto de provincia»")
    # Provincias que concentran el déficit (d3) y sus capitales
    d = sin_selladas(pd.read_csv(D3 / "deficit_provincial_concentracion.csv", dtype={"cod_prov": str}), "cod_prov", "provincia")
    d = d[~d.sellada_v6].sort_values("deficit_bajas0", ascending=False)
    top = d.head(6)
    capitales = {"08": "08019", "46": "46250", "03": "03014", "43": "43148", "29": "29067", "04": "04013"}
    assert set(top.cod_prov) == set(capitales), "las capitales deben ser las de las 6 provincias con más déficit"
    pw = v[(v.mun.isna() | (v.mun.str.strip() == "")) & v.prov.notna() & (v.prov.str.strip() != "")].copy()
    pw["cprov"] = pw.prov.str[:2]
    pw = sin_selladas(pw, "cprov", "provincia").pivot_table(index="cprov", columns="cat", values="val", aggfunc="first")
    filas = []
    for _, r in top.iterrows():
        c = r.cod_prov
        cap = capitales.get(c)
        vac_p = pw.loc[c, "Viviendas vacías"]
        vac_c = w.loc[cap, "vac"] if cap in w.index else np.nan
        tasa_c = w.loc[cap, "tasa"] if cap in w.index else np.nan
        filas.append(dict(prov=r.provincia, deficit=r.deficit_bajas0, vac_prov=vac_p, vac_cap=vac_c, tasa_cap=tasa_c,
                          tasa_prov=100 * vac_p / pw.loc[c, "Viviendas totales"]))
    t = pd.DataFrame(filas)
    s = DOC["segu_reduccion_relativa"] / 100
    hecho("VAC-6PROV-VACIAS", "Viviendas vacías (consumo eléctrico, 2021) en las 6 provincias con más déficit 2021-2025", t.vac_prov.sum(),
          "viviendas", "2021", fu + "; output/v17/d3/deficit_provincial_concentracion.csv", "OF", "vacias",
          nota=f"déficit 2021-2025 de esas provincias: {t.deficit.sum():,.0f} viviendas (V17-D3, bajas 0)")
    hecho("VAC-6CAP-VACIAS", "Viviendas vacías en las capitales de esas 6 provincias", t.vac_cap.sum(), "viviendas", "2021", fu, "OF", "vacias",
          minimo=t.tasa_cap.min(), maximo=t.tasa_cap.max(), nota="min y max = tasa de vacancia de las capitales (%)")
    hecho("VAC-SEGU-ILUSTRACION-6PROV", "Escenario: viviendas que pasarían a uso con la reducción relativa de Segú (2020) aplicada a las vacías de las 6 provincias",
          s * t.vac_prov.sum(), "viviendas", "2021", "Segú (2020), J. Public Econ. 185, 104079 (Francia, 1999-2001); INE Censo 2021",
          "juicio experto", "vacias", minimo=s * t.vac_cap.sum(), maximo=None,
          nota=(f"equivale al {100 * s * t.vac_prov.sum() / t.deficit.sum():.0f} % del déficit de esas provincias, mismo ámbito provincial "
                f"(solo capitales: {100 * s * t.vac_cap.sum() / t.deficit.sum():.0f} %); min = solo capitales; validez externa no comprobada; "
                "supone que las vacías por consumo son vacancia gravable; no es un efecto en precio ni el parque útil"))
    # Ronda 1: cobertura frente al total nacional y provincial (todas las provincias no selladas, incluidos los municipios fuera de la tabla)
    nac_vac = float(v[(v.ccaa.isna() | (v.ccaa.str.strip() == "")) & (v.cat == "Viviendas vacías")].val.iloc[0])
    pv_ns = pw   # ya sin provincias selladas
    vac_ns = float(pv_ns["Viviendas vacías"].sum())
    tot_ns = float(pv_ns["Viviendas totales"].sum())
    fuera = float(resto.vac.sum())
    assert abs(vac_ns - float(w.vac.sum()) - fuera) < 1, "las filas municipales y «resto» deben sumar el total provincial"
    cuotas = {k: float(g.loc[k, "vac"]) / vac_ns for k in lab}
    cuotas["fuera de la tabla"] = fuera / vac_ns
    menos10 = cuotas["<2.000"] + cuotas["2.000-10.000"] + cuotas["fuera de la tabla"]
    hecho("VAC-COBERTURA", "Vacías por consumo en provincias sin muestra sellada v6 (total provincial, incluidos municipios fuera de la tabla municipal)",
          vac_ns, "viviendas", "2021", fu, "OF", "vacias", minimo=None, maximo=nac_vac,
          nota=(f"max = total nacional; municipios no listados en la tabla: {fuera:,.0f} vacías ({100 * cuotas['fuera de la tabla']:.1f} %), "
                f"tasa {100 * fuera / (tot_ns - float(w.tot.sum())):.1f} %"))
    hecho("VAC-CUOTA-MUN-PEQUENOS", "Cuota de las vacías en municipios de menos de 10.000 viviendas o no listados (pequeños), sobre el total provincial no sellado",
          100 * menos10, "% de las vacías", "2021", fu, "OF", "vacias",
          minimo=100 * (cuotas["<2.000"] + cuotas["2.000-10.000"]), maximo=None,
          nota=(f"min = solo municipios listados de menos de 10.000 viviendas; en municipios de más de 50.000 viviendas: "
                f"{100 * cuotas['>50.000']:.1f} %"))
    # Ronda 1: vacancia frente a presión (déficit 2021-2025 por vivienda), provincias no selladas
    d2 = d.merge(pw[["Viviendas vacías", "Viviendas totales"]].rename(columns={"Viviendas vacías": "vac", "Viviendas totales": "tot"}),
                 left_on="cod_prov", right_index=True)
    d2["tasa_vac"] = 100 * d2.vac / d2.tot
    d2["presion"] = 100 * d2.deficit_bajas0 / d2.tot
    rho = float(d2[["tasa_vac", "presion"]].rank().corr().iloc[0, 1])
    d2["terc"] = pd.qcut(d2.presion.rank(method="first"), 3, labels=["baja", "media", "alta"])
    tg = d2.groupby("terc", observed=True).agg(vac=("vac", "sum"), tot=("tot", "sum"), deficit=("deficit_bajas0", "sum"))
    tg["tasa"] = 100 * tg.vac / tg.tot
    tg["cuota_vac"] = 100 * tg.vac / tg.vac.sum()
    tg["vac_sobre_def"] = tg.vac / tg.deficit.clip(lower=1)
    hecho("VAC-PRESION-SPEARMAN", "Correlación de rangos entre la tasa de vacancia provincial y el déficit 2021-2025 por vivienda (presión)", rho,
          "rho de Spearman", "2021 y 2021-2025", fu + "; output/v17/d3/deficit_provincial_concentracion.csv", "asociación", "vacias",
          nota=f"{len(d2)} provincias sin muestra sellada v6; descriptivo")
    hecho("VAC-TASA-TERCIL-PRESION-ALTA", "Tasa de vacancia en el tercil de provincias con más déficit por vivienda", tg.loc["alta", "tasa"],
          "% de las viviendas", "2021", fu, "OF", "vacias", minimo=tg.loc["baja", "tasa"], maximo=None,
          nota=(f"min = tercil de menos presión; el tercil alto reúne el {tg.loc['alta', 'cuota_vac']:.0f} % de las vacías y el "
                f"{100 * tg.loc['alta', 'deficit'] / tg.deficit.sum():.0f} % del déficit; vacías/déficit: alto {tg.loc['alta', 'vac_sobre_def']:.1f}, "
                f"bajo {tg.loc['baja', 'vac_sobre_def']:.1f}"))
    return dict(g=g, top=t, n_mun=len(w), s=s, cuotas=cuotas, rho=rho, tg=tg, vac_ns=vac_ns, nac=nac_vac)


# ---------------------------------------------------------------- ITP: potencia del diseño Q6
def itp() -> dict:
    inf = pd.read_csv(INFERENCIA)
    out = {}
    for rid, ref, nombre in [("Q6-p", DOC["dolls_precio_por_punto"], "valor tasado"),
                             ("Q6-v", DOC["fritzsche_volumen_por_punto"], "compraventas")]:
        r = inf[inf.id_resultado == rid].iloc[0]
        mde = (1.959964 + 0.841621) * float(r.se_conv)
        out[rid] = dict(beta=float(r.estimacion_reproducida), se=float(r.se_conv), lo=float(r.ic95_lo), hi=float(r.ic95_hi),
                        p=float(r.p_conv), mde=mde, ref=ref, tam=float(r.tamano_real))
        hecho(f"ITP-{rid}-MDE80", f"Efecto mínimo detectable al 80 % de potencia y 5 % bilateral, {rid} ({nombre}), por punto de tipo del ITP",
              mde, "log por punto de tipo", "panel de entrenamiento V16", "output/v17/lectura_bde/v15_v16_micro/inferencia.csv (aleatorización, 8 CCAA)",
              "juicio experto", "itp_medida",
              nota=(f"IC95 convencional [{r.ic95_lo:.3f}; {r.ic95_hi:.3f}], p = {r.p_conv:.3f}, tamaño real {100 * r.tamano_real:.1f} %; "
                    f"referencia de la literatura {ref:+.2f} por punto; incidencia plena en el vendedor = −0,01 por punto"))
    return out


# ---------------------------------------------------------------- vivienda pública: escala
def publica() -> dict:
    stock = DOC["ocde_es_social_viv"] / (DOC["ocde_es_social_pct"] / 100)
    nec_ue = (DOC["ocde_ue_social_pct"] - DOC["ocde_es_social_pct"]) / 100 * stock
    nec_1pp = 0.01 * stock
    p = pd.read_csv(PROTEGIDA, dtype={"periodo": str})
    p = p[(p.serie == "prot_definitiva_anual_nacional")]
    p = p[p.periodo.isin([str(a) for a in range(2021, 2026)])]
    calif = p.valor.astype(float).mean()
    prod = json.load(open(D3 / "hechos.json"))
    prod = {h["id"]: h["valor"] for h in prod}["V17-D3-PROD-ACTUAL"]
    fu = "OCDE AHD PH4.2 (24-11-2025); MIVAU calificaciones definitivas (data/raw/mivau_v2_protegida.csv); V17-D3-PROD-ACTUAL"
    # Ronda 1: ¿el 7,99 % UE es media simple o ponderada? Media simple de los países UE-27 de la figura PH4.2.1
    import openpyxl
    wb = openpyxl.load_workbook(OCDE_PH42, read_only=True)
    vals = {}
    for row in wb["Figure PH4.2.1"].iter_rows(values_only=True):
        cel = [c for c in (row or ()) if c is not None]
        for i in range(len(cel) - 1):
            if isinstance(cel[i], str) and cel[i].strip() in UE27 and isinstance(cel[i + 1], (int, float)):
                vals[cel[i].strip()] = float(cel[i + 1])
    simple = float(np.mean(list(vals.values())))
    pct_mivau_parque = 100 * DOC["mivau_publico_alquiler"] / stock   # 318.000 sobre el MISMO parque que la OCDE (no sobre hogares)
    nec_mivau = (DOC["ocde_ue_social_pct"] - pct_mivau_parque) / 100 * stock
    hecho("PUB-UE-MEDIA-SIMPLE", "Media simple del parque social de los países UE-27 presentes en la figura PH4.2.1 de la OCDE", simple, "% del parque",
          "2022 o último", "OCDE AHD PH4.2 (data/raw/v17/parque_social)", "OF", "vivienda_publica",
          nota=(f"{len(vals)} países con dato, años de referencia distintos; coincide con el agregado UE de la OCDE (7,99 %): es una media "
                "simple de países, no ponderada por parque (el fichero no declara el método; se deduce de la coincidencia)"))
    hecho("PUB-BRECHA-UE", "Viviendas sociales de alquiler adicionales para pasar del parque social español al 7,99 % de la UE (parque constante)",
          nec_ue, "viviendas", "2019 (España) y 2022 o último (UE)", fu + "; MIVAU Boletín Especial 2024", "cota", "vivienda_publica",
          minimo=nec_mivau, maximo=nec_ue,
          nota=(f"max = desde 1,13 % (OCDE 2019), min = desde {pct_mivau_parque:.2f} % (MIVAU 2023: 318.000 viviendas sobre el mismo parque "
                "de la OCDE; el 1,72 % del MIVAU es sobre hogares y no se compara con un 7,99 % sobre parque); "
                f"parque implícito OCDE {stock:,.0f}; años de toda la producción actual: {nec_mivau / prod:.0f}-{nec_ue / prod:.0f}"))
    hecho("PUB-CALIF-MEDIA-2021-2025", "Calificaciones definitivas de vivienda protegida, media anual 2021-2025", calif, "viviendas/año",
          "2021-2025", "MIVAU, Boletín Online, tabla 1.6 (data/raw/mivau_v2_protegida.csv)", "OF", "vivienda_publica",
          nota="incluye protegida para venta; no es alquiler social ni parque neto (la protección caduca)")
    hecho("PUB-ANIOS-1PP", "Años para añadir 1 punto de parque social al ritmo de calificaciones 2021-2025, si todas fueran alquiler social permanente",
          nec_1pp / calif, "años", "2021-2025", fu, "juicio experto", "vivienda_publica",
          minimo=nec_1pp / prod, nota="min = si toda la producción actual fuese social; sin descalificaciones ni crecimiento del parque")
    return dict(stock=stock, nec_ue=nec_ue, nec_mivau=nec_mivau, nec_1pp=nec_1pp, calif=calif, prod=prod, simple=simple, n_ue=len(vals))


# ---------------------------------------------------------------- más oferta: orden de magnitud
def oferta() -> dict:
    h = {x["id"]: x for x in json.load(open(D3 / "hechos.json"))}
    parque = 26_623_708  # Censo 2021, viviendas familiares (I.7 del informe integral)
    deficit = {"min": 523_606, "central": 705_778, "max": 887_950}   # L3-DEF-2125 (1.0), V17-D3
    pct = {k: 100 * v / parque for k, v in deficit.items()}
    il = {k: DOC["mense_elasticidad"] * v for k, v in pct.items()}
    hecho("OFERTA-DEFICIT-SOBRE-PARQUE", "Déficit 2021-2025 de la 1.0 (L3-DEF-2125) sobre el parque de viviendas familiares (Censo 2021)",
          pct["central"], "% del parque", "2021-2025", "output/v5/cifras_clave.csv (L3-DEF-2125); INE Censo 2021", "cota", "mas_oferta",
          minimo=pct["min"], maximo=pct["max"])
    hecho("OFERTA-MENSE-ILUSTRACION", "Ilustración: variación del alquiler medio si se cerrase el déficit central, con la elasticidad local de corto plazo de Mense (2025)",
          il["central"], "% del alquiler medio", "orden de magnitud", "Mense (2025), JPE Macroeconomics, 10.1086/733977 (Alemania)",
          "juicio experto", "mas_oferta", minimo=il["max"], maximo=il["min"],
          nota=("min y max = déficit máximo y mínimo; Mense estima respuestas locales de corto plazo en ciudades alemanas, no una "
                "elasticidad agregada de largo plazo (no se ha localizado una verificada); validez externa no comprobada"))
    # Elasticidad implícita de los escenarios V7.1 (V71-S1-*-alquiler-efecto_10k, C4) frente a la de Mense
    v = pd.read_csv(CENSO_VAC, sep=";", dtype=str, encoding="utf-8-sig")
    v.columns = ["nac", "ccaa", "prov", "mun", "cat", "val"]
    cc = v[v.ccaa.notna() & (v.ccaa.str.strip() != "") & (v.prov.isna() | (v.prov.str.strip() == "")) & (v.cat == "Viviendas totales")]
    cc = cc[~cc.ccaa.str[:2].isin(["18", "19"])].assign(cod=lambda x: x.ccaa.str[:2])   # sin Ceuta ni Melilla (panel V7)
    cc = sin_selladas(cc, "cod", "ccaa")   # guarda v6: la mediana se toma sobre las 9 CCAA no selladas (V7.1 usó 17)
    med = float(num(cc.val).median())
    cifras = pd.read_csv(ROOT / "output/v5/cifras_clave.csv")
    cifras = cifras.set_index(cifras.columns[0])
    el = {}
    for k, i in [("construccion", "V71-S1-a_construccion-alquiler-efecto_10k"), ("vacias", "V71-S1-b_vacias-alquiler-efecto_10k"),
                 ("publica", "V71-S1-c_vivienda_publica-alquiler-efecto_10k")]:
        el[k] = (float(cifras.loc[i].iloc[1]) / 100) / (10_000 / med)
    hecho("OFERTA-ELASTICIDAD-IMPLICITA-V71", "Elasticidad alquiler-parque implícita en el escenario V7.1 de construcción (−0,70 puntos % por 10.000 viviendas en la CCAA mediana)",
          el["construccion"], "% de alquiler por 1 % de parque", "2026-2036 (escenario)",
          "output/v5/cifras_clave.csv (V71-S1-a_construccion-alquiler-efecto_10k); INE Censo 2021 (parque de la CCAA mediana de las 9 no selladas)",
          "juicio experto", "mas_oferta",
          nota=(f"parque de la CCAA mediana {med:,.0f}; vacías {el['vacias']:.2f}; vivienda pública {el['publica']:.2f}; "
                f"cociente con Mense (2025, {DOC['mense_elasticidad']}): {el['construccion'] / DOC['mense_elasticidad']:.1f}; Mense es local y de "
                "corto plazo, no una referencia agregada, así que el cociente no mide optimismo"))
    hecho("OFERTA-ILUSTRACION-RANGO", "Ilustración: variación del alquiler medio al cerrar el déficit central, entre la elasticidad local de Mense y la implícita en el escenario V7.1",
          DOC["mense_elasticidad"] * pct["central"], "% del alquiler medio", "orden de magnitud", "Mense (2025); output/v5/cifras_clave.csv (V71-S1-a)",
          "juicio experto", "mas_oferta", minimo=el["construccion"] * pct["central"], maximo=DOC["mense_elasticidad"] * pct["central"],
          nota="no hay referencia agregada verificada que permita decir cuál de las dos es más realista; ninguna es un efecto estimado para España")
    cap = pd.read_csv(D3 / "capacidad_construccion_boom_actual.csv").set_index("anio")
    ocup_por_viv_2007 = cap.loc[2007, "ocupados_construccion_miles"] / cap.loc[2007, "terminadas"]
    nec5 = h["V17-D3-PROD-NECESARIA-5A"]["valor"]
    actual = h["V17-D3-PROD-ACTUAL"]["valor"]
    incr = (nec5 - actual) * ocup_por_viv_2007
    incr_bde = (nec5 - DOC["bde_terminadas_2025"]) * ocup_por_viv_2007
    hoy = h["V17-D3-OCUPADOS-CONSTRUCCION"]["valor"]
    hecho("OFERTA-EMPLEO-PROPORCIONAL-BOOM", "Ocupados en construcción proporcionales a la producción necesaria a 5 años, con la relación ocupados/terminadas de 2007",
          cap.loc[2007, "ocupados_construccion_miles"] * nec5 / h["V17-D3-PROD-BOOM"]["valor"], "miles de ocupados", "2007 y 2026-2030",
          "output/v17/d3/capacidad_construccion_boom_actual.csv; V17-D3-PROD-NECESARIA-5A; V17-D3-PROD-BOOM (media 2005-2007)",
          "juicio experto", "mas_oferta",
          nota=("se conserva por estar citada; NO es la necesidad de empleo: compara niveles como si el empleo actual estuviera libre; "
                "la lectura correcta es en incrementos (V17-AUD-OT-OFERTA-EMPLEO-INCREMENTO)"))
    hecho("OFERTA-EMPLEO-INCREMENTO", "Ocupados adicionales en construcción para pasar de la producción actual a la necesaria a 5 años (central), con la relación ocupados/terminadas de 2007",
          incr, "miles de ocupados", "2007 y 2026-2030", "output/v17/d3/capacidad_construccion_boom_actual.csv; V17-D3-PROD-NECESARIA-5A",
          "juicio experto", "mas_oferta", minimo=incr_bde, maximo=None,
          nota=(f"min = con 92.000 terminadas (BdE); total resultante {hoy + incr:,.0f} miles frente a {hoy:,.0f} hoy y al máximo de "
                f"{cap.ocupados_construccion_miles.max():,.0f} en 2007; supone que el empleo actual sigue ocupado en lo que hace hoy"))
    emp = empleo(h, cap)
    # Sensibilidad de la producción necesaria (D3-3): reposición, producción actual y absorción de vacías y secundarias
    hog = 145_603.0
    filas = []
    for rep_lbl, rep in (("6.864 (V5.1)", 6_864.0), ("0,1 % del parque", 0.001 * parque), ("0,3 % del parque", 0.003 * parque)):
        for abs_ in (0.0, 0.10, 0.25):
            for prod_lbl, prod in (("83.700 (INE/MIVAU)", actual), ("92.000 (BdE)", float(DOC["bde_terminadas_2025"]))):
                for n in (5, 10):
                    need = deficit["central"] * (1 - abs_) / n + hog + rep
                    filas.append(dict(reposicion=rep_lbl, absorcion=abs_, produccion_actual=prod_lbl, anios=n, necesaria=need, ratio=need / prod))
    sens = pd.DataFrame(filas)
    s5 = sens[sens.anios == 5]
    hecho("OFERTA-SENSIBILIDAD-5A", "Producción necesaria a 5 años (déficit central) frente a la actual: rango de sensibilidad", None,
          "veces la producción actual", "2026-2030", "V17-D3; BdE IA 2025 (92.000 terminadas)", "juicio experto", "mas_oferta",
          minimo=s5.ratio.min(), maximo=s5.ratio.max(),
          nota=("reposición 6.864/año o 0,1-0,3 % del parque; absorción de 0, 10 o 25 % del déficit por vacías y secundarias; producción actual "
                f"83.700 o 92.000; necesaria {s5.necesaria.min():,.0f}-{s5.necesaria.max():,.0f} viviendas/año"))
    s10 = sens[sens.anios == 10]
    hecho("OFERTA-SENSIBILIDAD-10A", "Ídem a 10 años", None, "veces la producción actual", "2026-2035", "ídem", "juicio experto", "mas_oferta",
          minimo=s10.ratio.min(), maximo=s10.ratio.max(), nota=f"necesaria {s10.necesaria.min():,.0f}-{s10.necesaria.max():,.0f} viviendas/año")
    # Rangos de las ratios de suelo (área del BdE frente a necesidad provincial a 10 años, mínimo-máximo)
    su = pd.read_csv(D3 / "suelo_potencial_bde_vs_necesidad.csv", dtype={"provincia": str}).dropna(subset=["necesidad_10a_prov_central"])
    rs = {}
    for _, r_ in su.iterrows():
        rs[r_.area_bde] = (r_.potencial_bde / r_.necesidad_10a_prov_max, r_.potencial_bde / r_.necesidad_10a_prov_central, r_.potencial_bde / r_.necesidad_10a_prov_min)
    b, sv = rs["Barcelona (área)"], rs["Sevilla (área)"]
    hecho("SUELO-BARCELONA-RATIO", "Potencial del área de Barcelona (BdE) sobre la necesidad provincial a 10 años", b[1], "cociente", "2025 y 2026-2035",
          "BdE IA 2025; output/v17/d3/suelo_potencial_bde_vs_necesidad.csv", "cota", "mas_oferta", minimo=b[0], maximo=b[2],
          nota="área ≠ provincia; min y max con la necesidad máxima y mínima")
    hecho("SUELO-SEVILLA-RATIO", "Potencial del área de Sevilla (BdE) sobre la necesidad provincial a 10 años", sv[1], "cociente", "2025 y 2026-2035",
          "ídem", "cota", "mas_oferta", minimo=sv[0], maximo=sv[2],
          nota="área ≠ provincia; la necesidad mínima (1.757) hace el máximo inestable (≈93); no se usa como conclusión")
    su_sev = su[su.area_bde == "Sevilla (área)"].iloc[0]
    ejec = DOC["bde_ejecucion_sevilla"] * DOC["bde_potencial_sevilla"]
    hecho("SUELO-SEVILLA-EJECUCION", "Potencial del área de Sevilla multiplicado por su ejecución histórica (28 %) sobre la necesidad provincial a 10 años",
          ejec / su_sev.necesidad_10a_prov_central, "cociente", "2025 y 2026-2035", "BdE IA 2025 (potencial y ejecución); V5.1 (necesidad)",
          "juicio experto", "mas_oferta", minimo=ejec / su_sev.necesidad_10a_prov_max, maximo=ejec / su_sev.necesidad_10a_prov_central,
          tipo="rango", cobertura="área urbana de Sevilla (BdE) frente a la provincia de Sevilla",
          nota="max = necesidad central (con la mínima, 1.757, el cociente no es informativo); supone que la ejecución futura es la histórica")
    return dict(pct=pct, il=il, el=el, incr=incr, incr_bde=incr_bde, hoy=hoy, sens=sens, rs=rs, emp=emp)


def empleo(h: dict, cap: pd.DataFrame) -> dict:
    """Cálculo con supuestos y rango (juicio experto): ocupados adicionales para pasar de la producción actual a la necesaria.

    L = ocupados de edificación residencial nueva por vivienda terminada al año = cuota_resid × ocupados rama F / terminadas.
    Referencias de L: 2007, media 2015-2019 y 2025, cada una con su rango de cuota residencial (supuesto, sin fuente verificada).
    No hay horas por vivienda en el repositorio (EPA por rama a dos dígitos o encuesta de estructura de la construcción: no
    descargadas). Industrialización: reducción de 0, 20 o 40 % de las horas por vivienda (escenario sin fuente verificada).
    Δocupados = (necesaria − actual) × L × (1 − industrialización)."""
    F, T = cap["ocupados_construccion_miles"] * 1000, cap["terminadas"]
    refs = {"2007": (F[2007] / T[2007], DOC["cuota_resid_nueva_2007"]),
            "2015-2019": (F.loc[2015:2019].mean() / T.loc[2015:2019].mean(), DOC["cuota_resid_nueva_hoy"]),
            "2025": (F[2025] / T[2025], DOC["cuota_resid_nueva_hoy"])}
    L = {k: (f * c[0], f * c[1]) for k, (f, c) in refs.items()}
    actual = (h["V17-D3-PROD-ACTUAL"]["valor"], float(DOC["bde_terminadas_2025"]))
    filas = []
    for n, idn in ((5, "5A"), (10, "10A")):
        nec = h[f"V17-D3-PROD-NECESARIA-{idn}"]
        for nec_v in (nec["min"], nec["valor"], nec["max"]):
            for a in actual:
                for ref, (lo, hi) in L.items():
                    for l_ in (lo, hi):
                        for g in DOC["industrializacion"]:
                            filas.append(dict(anios=n, necesaria=nec_v, actual=a, ref=ref, L=l_, ind=g,
                                              delta_miles=(nec_v - a) * l_ * (1 - g) / 1000))
    e = pd.DataFrame(filas)
    hoy, max07 = h["V17-D3-OCUPADOS-CONSTRUCCION"]["valor"], float(cap.ocupados_construccion_miles.max())
    hecho("EMPLEO-OCUP-POR-VIVIENDA", "Ocupados de edificación residencial nueva por vivienda terminada al año: referencias 2007, 2015-2019 y 2025 (con cuota supuesta)",
          None, "ocupados por vivienda y año", "2007, 2015-2019, 2025", "output/v17/d3/capacidad_construccion_boom_actual.csv (EPA rama F, terminadas MIVAU); supuestos de cuota residencial",
          "juicio experto", "mas_oferta", minimo=min(min(v) for v in L.values()), maximo=max(max(v) for v in L.values()), tipo="referencias",
          cobertura="España (agregado nacional)",
          nota="; ".join(f"{k}: {v[0]:.1f}-{v[1]:.1f}" for k, v in L.items())
               + "; cuota de la rama F en edificación residencial nueva SUPUESTA (2007: 45-65 %; 2015-2025: 15-30 %), sin fuente verificada; sin horas por vivienda")
    for n, idn in ((5, "5A"), (10, "10A")):
        x = e[e.anios == n]
        c = x[(x.necesaria == h[f"V17-D3-PROD-NECESARIA-{idn}"]["valor"]) & (x.ind == 0.0)]
        hecho(f"EMPLEO-INCREMENTO-RANGO-{idn}", f"Cálculo con supuestos (juicio experto): ocupados adicionales en construcción para cerrar el déficit en {n} años",
              float(c.delta_miles.median()), "miles de ocupados", f"2026-{2025 + n}",
              "V17-D3-PROD-NECESARIA, V17-D3-PROD-ACTUAL, BdE (92.000), EPA rama F; supuestos de cuota residencial e industrialización",
              "juicio experto", "mas_oferta", minimo=float(x.delta_miles.min()), maximo=float(x.delta_miles.max()), tipo="rango",
              cobertura="España (agregado nacional)",
              nota=(f"valor = mediana con déficit central y sin industrialización; rango con déficit mín.-máx., producción actual 83.700 o 92.000, "
                    f"tres referencias de productividad con cuota residencial supuesta e industrialización 0-40 %; empleo actual {hoy:,.0f} miles, "
                    f"máximo de 2007 {max07:,.0f} (holgura hasta el máximo: {max07 - hoy:,.0f})"))
    return dict(e=e, L=L, hoy=hoy, max07=max07)


# ---------------------------------------------------------------- D3-2: IPV por CCAA sin bloques sellados y variaciones deflactadas
def cuotas_varianza(m: np.ndarray) -> tuple[float, float, float]:
    """Misma descomposición que src/v17/d3_cuantitativo.py: año (común), territorio fijo y residuo local."""
    mu = m.mean()
    yr = m.mean(axis=1, keepdims=True) - mu
    pr = m.mean(axis=0, keepdims=True) - mu
    t = ((m - mu) ** 2).sum()
    c, p = m.shape[1] * (yr ** 2).sum() / t, m.shape[0] * (pr ** 2).sum() / t
    return c, p, 1 - c - p


def d3_2() -> dict:
    d = duckdb.sql(f"select territorio_codigo c, periodo p, valor v from '{HECHOS_BASE}' where variable='ipv' and nivel='ccaa' "
                   "and frecuencia='T' and not muestra_sellada_v6").df()
    d = sin_selladas(d, "c", "ccaa")   # la base no marca las CCAA selladas
    d["a"] = d.p.str[:4].astype(int)
    g = d.groupby(["c", "a"]).v.agg(["mean", "count"])
    g = g[g["count"] == 4]["mean"].unstack("c").loc[2014:2025]
    out = {}
    rng = np.random.default_rng(SEED)
    assert not set(g.columns) & CCAA_SELLADAS_V6
    for nombre, cols, a1 in (("sin_selladas", list(g.columns), 2025), ("sin_selladas_hasta_2024", list(g.columns), 2024)):
        r = np.log(g.loc[:a1, cols]).diff().dropna()
        for per, (i, j) in {"2015-2019": (2015, 2019), "2020-fin": (2020, a1), "2015-fin": (2015, a1)}.items():
            m = r.loc[i:j].values
            c, p, l = cuotas_varianza(m)
            bs = np.array([cuotas_varianza(m[:, rng.integers(0, m.shape[1], m.shape[1])])[0] for _ in range(300)])
            out[(nombre, per)] = dict(N=m.shape[1], T=m.shape[0], comun=c, fija=p, local=l, lo=np.percentile(bs, 2.5), hi=np.percentile(bs, 97.5))
    x = out[("sin_selladas", "2015-fin")]
    hecho("D32-IPV-CCAA-SIN-SELLADAS", "Cuota común (año) de la varianza de la variación anual del IPV, 9 CCAA sin bloques sellados v6, 2015-2025",
          100 * x["comun"], "% (IC95 bootstrap por CCAA)", "2015-2025", "INE IPV por CCAA (data/base/hechos.parquet)", "hecho", "D3-2",
          minimo=100 * x["lo"], maximo=100 * x["hi"],
          nota=(f"V17-D3 se ha recalculado con la guarda v6 y da la misma cifra (V17-D3-VARIANZA-COMUN-IPV-CCAA); efecto fijo {100 * x['fija']:.0f} %, "
                f"local {100 * x['local']:.0f} %; 2020-2025: {100 * out[('sin_selladas', '2020-fin')]['comun']:.0f} %; "
                f"hasta 2024: {100 * out[('sin_selladas_hasta_2024', '2015-fin')]['comun']:.0f} %"))
    # Jackknife de años (quitando un año cada vez) de la cuota común 2015-2025, 9 CCAA no selladas
    r_all = np.log(g.loc[:2025]).diff().dropna().loc[2015:2025]
    jk = [cuotas_varianza(r_all.drop(index=a).values)[0] for a in r_all.index]
    hecho("D32-IPV-CCAA-JACKKNIFE", "Cuota común del IPV 2015-2025 (9 CCAA no selladas) quitando un año cada vez: mínimo y máximo",
          100 * x["comun"], "%", "2015-2025", "INE IPV por CCAA (data/base/hechos.parquet)", "hecho", "D3-2",
          minimo=100 * min(jk), maximo=100 * max(jk), tipo="rango",
          cobertura="9 CCAA sin bloques sellados v6",
          nota=(f"año cuya exclusión más baja la cuota: {r_all.index[int(np.argmin(jk))]}; hasta 2024: "
                f"{100 * out[('sin_selladas_hasta_2024', '2015-fin')]['comun']:.0f} %"))
    out["jk"] = (min(jk), max(jk), r_all.index[int(np.argmin(jk))], r_all.index[int(np.argmax(jk))])
    # Variación acumulada 2015-2024 deflactada (deflactor del consumo de la CNT y renta disponible agregada de los hogares)
    def anual(var):
        q = duckdb.sql(f"select periodo p, valor v from '{HECHOS_BASE}' where variable='{var}' and nivel='nacional' and frecuencia='T'").df()
        q["a"] = q.p.str[:4].astype(int)
        return q.groupby("a").v.mean()
    defl = anual("deflactor")
    renta = anual("renta_hog")
    f_defl = defl.loc[2024] / defl.loc[2015]
    f_renta = renta.loc[2024] / renta.loc[2015]
    sp = duckdb.sql(f"select territorio_codigo c, periodo p, valor v from '{HECHOS_BASE}' where variable='serpavi_alquiler_m2_mediana' "
                    "and nivel='provincia' and frecuencia='A' and not muestra_sellada_v6").df()
    sp = sin_selladas(sp, "c", "provincia")
    sp["a"] = sp.p.astype(int)
    sp = sp.pivot_table(index="a", columns="c", values="v").loc[[2015, 2024]].dropna(axis=1)
    nom = sp.loc[2024] / sp.loc[2015]
    real = 100 * (nom / f_defl - 1)
    rel_renta = 100 * (nom / f_renta - 1)
    hecho("D32-SERPAVI-REAL-2015-2024", "Variación acumulada 2015-2024 del alquiler SERPAVI (mediana provincial), deflactada por el deflactor del consumo de la CNT",
          real.median(), "% real", "2015-2024", "MIVAU SERPAVI; INE CNT (data/base/hechos.parquet)", "hecho", "D3-2",
          minimo=real.min(), maximo=real.max(),
          nota=(f"{real.size} provincias sin muestra sellada v6; nominal mediana {100 * (nom.median() - 1):.0f} %; deflactor +{100 * (f_defl - 1):.1f} %; "
                f"provincias con caída real: {(real < 0).sum()}; frente a la renta disponible agregada de los hogares (+{100 * (f_renta - 1):.0f} %): "
                f"mediana {rel_renta.median():.1f} %, {(rel_renta < 0).sum()} provincias por debajo"))
    return dict(out=out, real=real, rel_renta=rel_renta, f_defl=f_defl, f_renta=f_renta, nom=nom)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sel = selladas()
    r = {"tit": titularidad(sel), "vac": vacias(sel), "itp": itp(), "pub": publica(), "of": oferta(), "d32": d3_2()}
    ids = [h["id"] for h in HECHOS]
    assert len(ids) == len(set(ids))
    (OUT / "oferta_titularidad_hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # Resumen en pantalla para redactar las fichas
    for h in HECHOS:
        print(h["id"], h["valor"], h["min"], h["max"], h["unidad"], "|", h["nota"][:200])
    print(r["vac"]["g"].round(2).to_string())
    print(r["vac"]["top"].round(1).to_string())
    print("BCN", r["tit"]["bcn"], "prov_max", r["tit"]["prov_max"])
    print("ITP", r["itp"])
    print(r["tit"]["grid"].round(2).to_string())
    print("NIF", r["tit"]["nif_2025"], r["tit"]["nif_2026"])
    print(r["vac"]["tg"].round(2).to_string(), r["vac"]["cuotas"])
    print({k: (v if isinstance(v, tuple) else {kk: round(vv, 3) for kk, vv in v.items()}) for k, v in r["d32"]["out"].items()})
    print(r["of"]["emp"]["L"])
    print(r["of"]["sens"].groupby(["anios"]).ratio.describe())
    print("suelo", r["of"]["rs"])


if __name__ == "__main__":
    main()
