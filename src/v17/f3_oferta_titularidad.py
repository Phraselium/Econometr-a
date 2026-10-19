"""V17 · Fase 3 · Auditoría del grupo «oferta_titularidad». ANÁLISIS A POSTERIORI (capa C4).

Pruebas mínimas de las filas grandes_tenedores, itp_discurso, itp_medida, mas_oferta, vacias y vivienda_publica (docs/v17/plan.md,
fase 3, punto 2). Contabilidad, cotas e ilustraciones con parámetros de la literatura: nada de lo calculado aquí es un efecto causal.
Determinista, sin red, SEED = 20261010. Con la base (data/base/hechos.parquet) solo se lee la lista de provincias con
muestra_sellada_v6 para EXCLUIRLAS de toda distribución provincial o municipal; no se lee data/sealed ni se ejecuta evaluate_*.
data/raw se lee en solo lectura. Las cifras de documento (Banco de España, O-HB, OCDE, literatura) se toman de
docs/v17/fuentes/*.md y de las fichas de literatura; no se recalculan.
Uso: python3 src/v17/f3_oferta_titularidad.py  ->  output/v17/auditoria/oferta_titularidad_hechos.json
"""
from __future__ import annotations

import json
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "v17" / "auditoria"
CAT = ROOT / "data/raw/v11/catastro_titularidad"
CENSO_VAC = ROOT / "data/raw/v11/ine_censo2021/censo2021_tpx59531.csv"
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
    "ocde_es_social_pct": 1.13, "ocde_es_social_viv": 290_000, "ocde_ue_social_pct": 7.99,
    "ocde_fr": 14.0, "ocde_at": 23.6, "ocde_nl": 34.1, "ocde_de": 2.6, "ocde_it": 2.4, "ocde_pt": 1.06,
    "segu_reduccion_relativa": 13.0,     # Segú (2020): −13 % de la tasa de vacancia (relativa), Francia 1997-2001
    "mense_elasticidad": -0.19,          # Mense (2025): +1 % de oferta → −0,19 % del alquiler medio (Alemania, corto plazo)
    "li_elasticidad": -0.10,             # Li (2022): +10 % de parque local → −1 % de alquiler (Nueva York, NO VERIFICADA)
    "dolls_precio_por_punto": -0.03,     # Dolls et al. (2025): −3 % de precio por punto de tipo (Alemania)
    "fritzsche_volumen_por_punto": -0.07,  # Fritzsche y Vandrei (2019): −7 % de transacciones por punto
}
HECHOS: list[dict] = []


def hecho(id_, indicador, valor, unidad, periodo, fuentes, lectura, ficha, minimo=None, maximo=None, nota=""):
    assert lectura in ("OF", "hecho", "cota", "asociación", "juicio experto")
    f = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)
    HECHOS.append({"id": f"V17-AUD-OT-{id_}", "indicador": indicador, "valor": f(valor), "min": f(minimo), "max": f(maximo),
                   "unidad": unidad, "periodo": periodo, "fuentes": fuentes, "capa": "C4", "lectura_v17": lectura,
                   "ficha": f"{FICHAS}/{ficha}.md", "nota": "a posteriori" + (f"; {nota}" if nota else "")})


def selladas() -> set[str]:
    d = duckdb.sql(f"select distinct territorio_codigo c from '{HECHOS_BASE}' where nivel='provincia' and muestra_sellada_v6").df()
    return set(d.c)


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
    pv = pd.read_csv(CAT / "p_spi_prov_v.csv.gz")
    pv = pv[pv.anio_fichero == 2026].copy()
    mu = pd.read_csv(CAT / "p_spi_mun_v.csv.gz", dtype={"CODINE": str})
    mu["prov"] = mu.CODINE.str[:2]
    cod = mu[mu.anio_fichero == 2026].groupby("PROVINCIA").prov.first()
    pv["prov"] = pv.PROVINCIA.map(cod)
    pv = pv[~pv.prov.isin(sel) & pv.prov.notna()]
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
    w = w[~w.cprov.isin(sel)].dropna(subset=["tot", "vac"])
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
              "% de las viviendas", "2021", fu, "OF", "vacias", nota=f"{int(g.loc[k, 'n'])} municipios; {g.loc[k, 'cuota_vac']:.1f} % de las vacías de la muestra; sin provincias selladas v6; la tabla solo cubre {len(w)} municipios")
    # Provincias que concentran el déficit (d3) y sus capitales
    d = pd.read_csv(D3 / "deficit_provincial_concentracion.csv", dtype={"cod_prov": str})
    d = d[~d.sellada_v6].sort_values("deficit_bajas0", ascending=False)
    top = d.head(6)
    capitales = {"08": "08019", "46": "46250", "03": "03014", "43": "43148", "29": "29067", "04": "04013"}
    pw = v[(v.mun.isna() | (v.mun.str.strip() == "")) & v.prov.notna() & (v.prov.str.strip() != "")].copy()
    pw["cprov"] = pw.prov.str[:2]
    pw = pw.pivot_table(index="cprov", columns="cat", values="val", aggfunc="first")
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
    hecho("VAC-SEGU-ILUSTRACION-6PROV", "Ilustración: viviendas que pasarían a uso con la reducción relativa de Segú (2020) aplicada a las vacías de las 6 provincias",
          s * t.vac_prov.sum(), "viviendas", "2021", "Segú (2020), J. Public Econ. 185, 104079 (Francia, 1999-2001); INE Censo 2021",
          "juicio experto", "vacias", minimo=s * t.vac_cap.sum(), maximo=None,
          nota=(f"equivale al {100 * s * t.vac_prov.sum() / t.deficit.sum():.0f} % del déficit de esas provincias "
                f"(solo capitales: {100 * s * t.vac_cap.sum() / t.deficit.sum():.0f} %); min = solo capitales; validez externa no comprobada; "
                "supone que las vacías por consumo son vacancia gravable; no es un efecto en precio"))
    return dict(g=g, top=t, n_mun=len(w), s=s)


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
    hecho("PUB-BRECHA-UE", "Viviendas sociales de alquiler adicionales para pasar del 1,13 % de España al 7,99 % de la UE (parque constante)",
          nec_ue, "viviendas", "2019 (España) y 2022 o último (UE)", fu, "cota", "vivienda_publica",
          nota=f"parque implícito OCDE {stock:,.0f}; años de toda la producción actual: {nec_ue / prod:.0f}")
    hecho("PUB-CALIF-MEDIA-2021-2025", "Calificaciones definitivas de vivienda protegida, media anual 2021-2025", calif, "viviendas/año",
          "2021-2025", "MIVAU, Boletín Online, tabla 1.6 (data/raw/mivau_v2_protegida.csv)", "OF", "vivienda_publica",
          nota="incluye protegida para venta; no es alquiler social ni parque neto (la protección caduca)")
    hecho("PUB-ANIOS-1PP", "Años para añadir 1 punto de parque social al ritmo de calificaciones 2021-2025, si todas fueran alquiler social permanente",
          nec_1pp / calif, "años", "2021-2025", fu, "juicio experto", "vivienda_publica",
          minimo=nec_1pp / prod, nota="min = si toda la producción actual fuese social; sin descalificaciones ni crecimiento del parque")
    return dict(stock=stock, nec_ue=nec_ue, nec_1pp=nec_1pp, calif=calif, prod=prod)


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
    hecho("OFERTA-MENSE-ILUSTRACION", "Ilustración: variación del alquiler medio si se cerrase el déficit con la elasticidad de corto plazo de Mense (2025)",
          il["central"], "% del alquiler medio", "orden de magnitud", "Mense (2025), JPE Macroeconomics, 10.1086/733977 (Alemania)",
          "juicio experto", "mas_oferta", minimo=il["max"], maximo=il["min"],
          nota=("nacional y estático; Mense estima respuestas locales de corto plazo en ciudades alemanas; validez externa no comprobada; "
                "con la elasticidad local de Li (2022, NO VERIFICADA) sería "
                f"{DOC['li_elasticidad'] * pct['central']:.2f} %"))
    # Elasticidad implícita de los escenarios V7.1 (V71-S1-*-alquiler-efecto_10k, C4) frente a la de Mense
    v = pd.read_csv(CENSO_VAC, sep=";", dtype=str, encoding="utf-8-sig")
    v.columns = ["nac", "ccaa", "prov", "mun", "cat", "val"]
    cc = v[v.ccaa.notna() & (v.ccaa.str.strip() != "") & (v.prov.isna() | (v.prov.str.strip() == "")) & (v.cat == "Viviendas totales")]
    cc = cc[~cc.ccaa.str[:2].isin(["18", "19"])]           # sin Ceuta ni Melilla: 17 CCAA del panel V7
    med = float(num(cc.val).median())
    cifras = pd.read_csv(ROOT / "output/v5/cifras_clave.csv")
    cifras = cifras.set_index(cifras.columns[0])
    el = {}
    for k, i in [("construccion", "V71-S1-a_construccion-alquiler-efecto_10k"), ("vacias", "V71-S1-b_vacias-alquiler-efecto_10k"),
                 ("publica", "V71-S1-c_vivienda_publica-alquiler-efecto_10k")]:
        el[k] = (float(cifras.loc[i].iloc[1]) / 100) / (10_000 / med)
    hecho("OFERTA-ELASTICIDAD-IMPLICITA-V71", "Elasticidad alquiler-parque implícita en el escenario V7.1 de construcción (−0,70 puntos % por 10.000 viviendas en la CCAA mediana)",
          el["construccion"], "% de alquiler por 1 % de parque", "2026-2036 (escenario)",
          "output/v5/cifras_clave.csv (V71-S1-a_construccion-alquiler-efecto_10k); INE Censo 2021 (parque de la CCAA mediana)",
          "juicio experto", "mas_oferta",
          nota=(f"parque de la CCAA mediana {med:,.0f}; vacías {el['vacias']:.2f}; vivienda pública {el['publica']:.2f}; "
                f"Mense (2025) {DOC['mense_elasticidad']}: el escenario es {el['construccion'] / DOC['mense_elasticidad']:.1f} veces mayor"))
    ratio = h["V17-D3-PROD-NECESARIA-5A"]["valor"] / h["V17-D3-PROD-ACTUAL"]["valor"]
    boom_emp = 2703.4 * h["V17-D3-PROD-NECESARIA-5A"]["valor"] / h["V17-D3-PROD-BOOM"]["valor"]
    hecho("OFERTA-EMPLEO-PROPORCIONAL-BOOM", "Ocupados en construcción proporcionales a la producción necesaria a 5 años, con la relación ocupados/terminadas de 2007",
          boom_emp, "miles de ocupados", "2007 y 2026-2030", "output/v17/d3/capacidad_construccion_boom_actual.csv; V17-D3-PROD-NECESARIA-5A",
          "juicio experto", "mas_oferta", nota=(f"frente a {h['V17-D3-OCUPADOS-CONSTRUCCION']['valor']:,.0f} miles hoy; producción necesaria = "
                                               f"x{ratio:.1f} la actual; la rama F incluye obra civil y rehabilitación, por lo que «terminadas por ocupado» no es productividad residencial"))
    return dict(pct=pct, il=il, ratio=ratio, boom_emp=boom_emp)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sel = selladas()
    r = {"tit": titularidad(sel), "vac": vacias(sel), "itp": itp(), "pub": publica(), "of": oferta()}
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


if __name__ == "__main__":
    main()
