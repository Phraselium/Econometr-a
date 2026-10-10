"""CB (C5 seguridad juridica, C6 fiscalidad/tamano del arrendador, C8 empresas en stock y flujos).
Determinista, sin red. Lee data/raw/v5/cb_* (cb_fetch.py), data/raw/v3 (Censo 2021 secciones), data/raw (hogares ECH)
y output/v5/R1C/hechos.json. Escribe en output/v5/CB/.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry, holm  # noqa: E402

SEED = 20261010
rng = np.random.default_rng(SEED)
RAW = RAIZ / "data" / "raw"
V5 = RAW / "v5"
OUT = RAIZ / "output" / "v5" / "CB"
(OUT / "tablas").mkdir(parents=True, exist_ok=True)
reg = Registry(OUT / "registro.csv")
hechos = []


def norm(s):
    s = unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", " ", s)


CLAVES = [("andaluc", "Andalucia"), ("arag", "Aragon"), ("asturias", "Asturias"), ("balears", "Illes Balears"),
          ("canarias", "Canarias"), ("cantabria", "Cantabria"), ("castilla y le", "Castilla y Leon"),
          ("la mancha", "Castilla-La Mancha"), ("catalu", "Cataluna"), ("valenciana", "C. Valenciana"),
          ("extremadura", "Extremadura"), ("galicia", "Galicia"), ("madrid", "Madrid"), ("murcia", "Murcia"),
          ("navarra", "Navarra"), ("pais vasco", "Pais Vasco"), ("rioja", "La Rioja")]


def ccaa(s):
    n = norm(s)
    for k, v in CLAVES:
        if k in n:
            return v
    return None


PROV = {1: "Pais Vasco", 20: "Pais Vasco", 48: "Pais Vasco", 31: "Navarra", 26: "La Rioja", 50: "Aragon", 22: "Aragon",
        44: "Aragon", 8: "Cataluna", 17: "Cataluna", 25: "Cataluna", 43: "Cataluna", 3: "C. Valenciana",
        12: "C. Valenciana", 46: "C. Valenciana", 30: "Murcia", 7: "Illes Balears", 35: "Canarias", 38: "Canarias",
        39: "Cantabria", 33: "Asturias", 15: "Galicia", 27: "Galicia", 32: "Galicia", 36: "Galicia", 28: "Madrid",
        10: "Extremadura", 6: "Extremadura", 4: "Andalucia", 11: "Andalucia", 14: "Andalucia", 18: "Andalucia",
        21: "Andalucia", 23: "Andalucia", 29: "Andalucia", 41: "Andalucia", 2: "Castilla-La Mancha",
        13: "Castilla-La Mancha", 16: "Castilla-La Mancha", 19: "Castilla-La Mancha", 45: "Castilla-La Mancha",
        5: "Castilla y Leon", 9: "Castilla y Leon", 24: "Castilla y Leon", 34: "Castilla y Leon",
        37: "Castilla y Leon", 40: "Castilla y Leon", 42: "Castilla y Leon", 47: "Castilla y Leon",
        49: "Castilla y Leon"}


def hecho(id_, ind, v, mn, mx, unidad, periodo, cob, fuentes, capa, fecha):
    hechos.append(dict(id=id_, indicador=ind, valor=v, min=mn, max=mx, unidad=unidad, periodo=periodo,
                       cobertura=cob, fuentes=fuentes, capa=capa, fecha_dato=fecha))


def num(s):
    return float(s.replace(".", "").replace(",", "."))


# ------------------------------------------------------------------ C5: datos
def hoja(wb, nombre, años, patron):
    ws = wb[nombre]
    rows = list(ws.iter_rows(values_only=True))
    ih = next(i for i, r in enumerate(rows) if r[2] and re.match(r"\d\d-T", str(r[2])))
    h = rows[ih]
    cols = {}
    for j, x in enumerate(h):
        if x is None:
            continue
        m = re.search(patron, re.sub(r"\s+", " ", str(x)).strip())
        if m and int(m.group(1)) in años:
            cols[int(m.group(1))] = j
    out = []
    for r in rows[ih + 1:]:
        if r[1] is None:
            if out:
                break
            continue
        k = ccaa(r[1]) if r[1] != "TOTAL" else "TOTAL"
        if k is None:
            continue
        if k == "TOTAL":
            out.append(("Espana", {a: r[j] for a, j in cols.items()}))
            break
        out.append((k, {a: r[j] for a, j in cols.items()}))
    return out


wb = openpyxl.load_workbook(V5 / "cb_cgpj_series_tsj_1T2026.xlsx", data_only=True)
YRS = range(2013, 2026)
lz = []
for tipo, hj in (("total", "Lanzamientos practic. total TSJ"), ("hipotecaria", "Lanzamientos E.hipotecaria TSJ"),
                 ("LAU", "Lanzamientos L.A.U  TSJ"), ("otros", "Lanzamientos. Otros TSJ")):
    for k, d in hoja(wb, hj, YRS, r"^Total (\d{4})$"):
        for a, v in d.items():
            lz.append(dict(ccaa=k, tipo=tipo, año=a, lanzamientos=v))
lz = pd.DataFrame(lz)
lz.to_csv(OUT / "tablas" / "cgpj_lanzamientos_ccaa.csv", index=False)
vp = []
for k, d in hoja(wb, "Ver. pos.ocupas", range(2018, 2026), r"^Total (\d{4}) ingresados$"):
    for a, v in d.items():
        vp.append(dict(ccaa=k, año=a, verbales_posesorios_ingresados=v))
vp = pd.DataFrame(vp)
vp.to_csv(OUT / "tablas" / "cgpj_verbales_posesorios_ocupacion.csv", index=False)

# Interior px 11001 (hechos conocidos por allanamiento/usurpacion, CCAA)
txt = (V5 / "cb_interior_11001.px").read_bytes().decode("iso-8859-15")
ccs = re.findall(r'"([^"]+)"', re.search(r'VALUES\("Comunidades aut[^"]*"\)=(.*?);', txt, re.S).group(1))
per = [int(x) for x in re.findall(r'"(\d{4})"', re.search(r'VALUES\("periodo"\)=(.*?);', txt, re.S).group(1))]
vals = [float(x) for x in re.search(r"DATA=(.*?);", txt, re.S).group(1).split()]
M = np.array(vals).reshape(len(ccs), len(per))
us = pd.DataFrame([dict(ccaa=("Espana" if "TOTAL" in c else ccaa(c)), año=a, hechos_conocidos=M[i, j])
                   for i, c in enumerate(ccs) for j, a in enumerate(per) if "TOTAL" in c or ccaa(c)])
us.to_csv(OUT / "tablas" / "interior_allanamiento_usurpacion_ccaa.csv", index=False)

# Censo 2021 (secciones): viviendas principales por tenencia
cs = pd.read_csv(RAW / "v3" / "ine_v3_censo2021_seccion_indicadores.csv.gz", dtype={"codigo": str},
                 usecols=["serie", "valor", "codigo"])
cs = cs[cs.serie.isin(["t20_1", "t20_2", "t20_3"])].copy()
cs["ccaa"] = cs.codigo.str.zfill(10).str[:2].astype(int).map(PROV)
cen = cs.pivot_table(index="ccaa", columns="serie", values="valor", aggfunc="sum")
cen.columns = ["propiedad", "alquiler", "otra"]
cen["principales"] = cen.sum(axis=1)
cen["alq_share_censo"] = 100 * cen.alquiler / cen.principales
cen.to_csv(OUT / "tablas" / "censo2021_tenencia_ccaa.csv")
n_sec = cs.codigo.nunique()

# ECV 9997
ecv = json.load(open(V5 / "cb_ine_t9997_ecv_tenencia_ccaa.json"))
rows = []
for s in ecv:
    nm = s["Nombre"]
    if "Alquiler" in nm and "Hogar" in nm:
        k = ccaa(nm.split(".")[0]) if not nm.startswith("Total") else "Espana"
        if k is None:
            continue
        kind = "reducido" if "inferior" in nm else "mercado"
        for p in s["Data"]:
            rows.append(dict(ccaa=k, tipo=kind, año=p["Anyo"], valor=p["Valor"]))
ecv = pd.DataFrame(rows).pivot_table(index=["ccaa", "año"], columns="tipo", values="valor").reset_index()
ecv["alq_share_ecv"] = ecv.mercado + ecv.reducido
ecv.to_csv(OUT / "tablas" / "ecv_alquiler_ccaa.csv", index=False)


# AEAT viviendas declaradas 2024
def tabla_html(f):
    h = (V5 / f).read_bytes().decode("utf8", "ignore")
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]*>", "|", h))
    return re.sub(r"(\| ?)+", "|", t)


t = tabla_html("cb_aeat_irpfviv_2024_arrendamiento_ccaa_declarante.html")
arr = []
for m in re.finditer(r"\|([A-Za-zÁÉÍÓÚáéíóúñ ,\-]+)\|([\d.]+)\|([\d.]+)\|([\d.]+)\|([\d.]+)\|([\d.]+)", t):
    k = ccaa(m.group(1))
    if k:
        arr.append(dict(ccaa=k, viv_arrendadas_equiv=num(m.group(2)), ingresos_eur=num(m.group(3))))
arr = pd.DataFrame(arr)
arr.to_csv(OUT / "tablas" / "aeat_viviendas_arrendadas_ccaa_declarante_2024.csv", index=False)
tu = tabla_html("cb_aeat_irpfviv_2024_clasificacion_uso.html")
mt = re.search(r"\|Total\|([\d.]+)\|([\d.]+)\|[\d.]+\|[\d.]+\|[\d.]+\|[\d.]+\|[\d,]+\|[\d.]+\|([\d.]+)\|([\d,]+)", tu)
viv_total, viv_arr_equiv = num(mt.group(1)), num(mt.group(3))
mh = re.search(r"\|Arrendadas como vivienda habitual\|([\d.]+)\|[\d.]+\|[\d.]+\|[\d.]+\|[\d.]+\|[\d.]+\|[\d,]+\|[\d.]+\|([\d.]+)", tu)
arr_hab_equiv = num(mh.group(2))
mo = re.search(r"\|Arrendadas como otras viviendas\|([\d.]+)\|[\d.]+\|[\d.]+\|[\d.]+\|[\d.]+\|[\d.]+\|[\d,]+\|[\d.]+\|([\d.]+)", tu)
arr_otras_equiv = num(mo.group(2))

# IRPF partidas
ir = []
for y in range(2019, 2025):
    t = tabla_html(f"cb_aeat_irpf_{y}_bienes_inmobiliarios.html")
    for cod, nombre in ((102, "ingresos_integros_capital_inmobiliario"), (149, "rendimiento_neto"),
                        (150, "reduccion_arrendamiento_vivienda"), (156, "rend_neto_reducido")):
        m = re.search(rf"\|{cod}\.[^|]*\|([\d.]+)\|([\d.]+)\|", t)
        ir.append(dict(año=y, partida=cod, concepto=nombre, declarantes=num(m.group(1)), importe_eur=num(m.group(2))))
ir = pd.DataFrame(ir)
ir.to_csv(OUT / "tablas" / "aeat_irpf_capital_inmobiliario_2019_2024.csv", index=False)

# ------------------------------------------------------------------ C5: analisis
CC = [k for _, k in CLAVES]
P = pd.DataFrame(index=CC)
P["principales"] = cen.principales
P["alq_share_censo"] = cen.alq_share_censo
e = ecv.pivot(index="ccaa", columns="año", values="alq_share_ecv")
P["alq_share_ecv_2025"] = e[2025]
P["d_alq_ecv_2021_2025"] = e[2025] - e[2021]
u = us[(us.año >= 2022) & (us.año <= 2025)].groupby("ccaa").hechos_conocidos.mean()
P["usurp_x100k"] = 1e5 * u / P.principales
v = vp[(vp.año >= 2022) & (vp.año <= 2025)].groupby("ccaa").verbales_posesorios_ingresados.mean()
P["verb_pos_x100k"] = 1e5 * v / P.principales
l = lz[(lz.tipo == "LAU") & (lz.año >= 2022)].groupby("ccaa").lanzamientos.mean()
P["lau_x1000_alq"] = 1e3 * l / cen.alquiler
P.to_csv(OUT / "tablas" / "c5_panel_ccaa.csv")


def spearman_perm(x, y, B=10000):
    r, _ = stats.spearmanr(x, y)
    xs = np.asarray(x)
    cnt = sum(abs(stats.spearmanr(xs, rng.permutation(y))[0]) >= abs(r) - 1e-12 for _ in range(B))
    return float(r), (cnt + 1) / (B + 1)


SP = [("C5-S1", "usurp_x100k", "alq_share_censo"), ("C5-S2", "usurp_x100k", "alq_share_ecv_2025"),
      ("C5-S3", "verb_pos_x100k", "alq_share_ecv_2025"), ("C5-S4", "usurp_x100k", "d_alq_ecv_2021_2025"),
      ("C5-S5", "verb_pos_x100k", "d_alq_ecv_2021_2025"), ("C5-S6", "lau_x1000_alq", "alq_share_ecv_2025")]
res5 = {}
for mid, a, b in SP:
    r, p = spearman_perm(P[a], P[b])
    res5[mid] = (a, b, r, p)
ph = holm({k: v[3] for k, v in res5.items()})
for mid, (a, b, r, p) in res5.items():
    reg.log("C5", mid, f"spearman({a}, {b})", "2021-2025", "2021-2025", len(P), np.nan, np.nan, np.nan,
            coef_interes=r, p_interes=p, notas=f"N=17 CCAA; p permutacion 10000, seed {SEED}; Holm p={ph[mid]:.3f}; descriptivo")

# ------------------------------------------------------------------ C6/C8: residual
rc = P.principales.drop(["Navarra", "Pais Vasco"])  # AEAT: solo territorio de regimen fiscal comun
alq_censo_comun = cen.alquiler.drop(["Navarra", "Pais Vasco"]).sum()
alq_censo_total = cen.alquiler.sum()
pf_hab_comun = arr_hab_equiv  # AEAT 2024: viviendas arrendadas como vivienda habitual (equivalentes), regimen comun
ratio_a = pf_hab_comun / alq_censo_comun
ech = pd.read_csv(RAW / "ine_hogares_60131.csv")
ech = ech[ech.nombre.str.startswith("Total Nacional. Total.")].copy()
ech["fecha"] = pd.to_datetime(ech.fecha)
hog25 = float(ech[ech.fecha == "2025-10-01"].valor.iloc[0])
sh25 = float(ecv[(ecv.ccaa == "Espana") & (ecv.año == 2025)].alq_share_ecv.iloc[0])
stock_ecv25 = hog25 * sh25 / 100
ratio_b = pf_hab_comun / (stock_ecv25 * (1 - (alq_censo_total - alq_censo_comun) / alq_censo_total))
res_a, res_b = 1 - ratio_a, 1 - ratio_b
pj_flujo = next(h for h in json.load(open(RAIZ / "output/v5/R1C/hechos.json")) if h["id"] == "R1C-004")["valor"]
tab6 = pd.DataFrame([
    dict(magnitud="Censo 2021: viviendas principales en alquiler, Espana", valor=alq_censo_total, unidad="viviendas", fecha="2021-11", fuente="INE Censo 2021 (secciones)"),
    dict(magnitud="Censo 2021: id., regimen fiscal comun (sin Navarra y Pais Vasco)", valor=alq_censo_comun, unidad="viviendas", fecha="2021-11", fuente="INE Censo 2021"),
    dict(magnitud="AEAT: viviendas equivalentes arrendadas como vivienda habitual, personas fisicas", valor=arr_hab_equiv, unidad="viviendas", fecha="IRPF 2024", fuente="AEAT viviendas declaradas IRPF 2024"),
    dict(magnitud="AEAT: viviendas equivalentes arrendadas, total (habitual y otras)", valor=viv_arr_equiv, unidad="viviendas", fecha="IRPF 2024", fuente="AEAT"),
    dict(magnitud="Estimacion A: residual (PJ + sector publico + alquiler no declarado) sobre stock Censo 2021", valor=100 * res_a, unidad="% del stock", fecha="2021/2024", fuente="Censo 2021 y AEAT"),
    dict(magnitud="Estimacion B: id. sobre stock ECV 2025 x hogares ECH 2025T4", valor=100 * res_b, unidad="% del stock", fecha="2025", fuente="ECV 9997, ECH 60131, AEAT"),
    dict(magnitud="ETDP: compraventas con comprador PJ", valor=pj_flujo, unidad="% compraventas", fecha="2024", fuente="INE ETDP 50272 (R1C-004)"),
])
tab6.to_csv(OUT / "tablas" / "c6_c8_personas_fisicas_vs_residual.csv", index=False)
reg.log("C6", "C6-E1", "residual = 1 - AEAT_PF_habitual / stock_Censo2021 (regimen comun)", "2021", "2024", 15, np.nan, np.nan, np.nan, coef_interes=100 * res_a, notas="C4; fechas distintas; cota superior del residual PJ+publico+no declarado si el stock crece")
reg.log("C6", "C6-E2", "residual = 1 - AEAT_PF_habitual / (ECV2025 x ECH2025T4)", "2024", "2025", 15, np.nan, np.nan, np.nan, coef_interes=100 * res_b, notas="C4; estimacion alternativa; ambas se reportan")
decl24 = ir[(ir.año == 2024) & (ir.partida == 102)].iloc[0]
red24 = ir[(ir.año == 2024) & (ir.partida == 150)].iloc[0]
net24 = ir[(ir.año == 2024) & (ir.partida == 149)].iloc[0]
ratio_viv = viv_arr_equiv / decl24.declarantes
reg.log("C6", "C6-E3", "viviendas equivalentes arrendadas / declarantes con ingresos de capital inmobiliario", "2024", "2024", 1, np.nan, np.nan, np.nan, coef_interes=ratio_viv, notas="C4; promedio, no distribucion; incluye copropiedad y otros inmuebles en declarantes")

# ------------------------------------------------------------------ hechos
FA = "Cifras de AEAT, Estadistica de los declarantes del IRPF 2024 (publ. 2026)"
hecho("CB-C5-01", "Lanzamientos practicados por LAU (principalmente alquiler impagado)", int(lz[(lz.ccaa == "Espana") & (lz.tipo == "LAU") & (lz.año == 2025)].lanzamientos.iloc[0]), None, None, "lanzamientos/anio", "2025", "Espana", "CGPJ, Efecto de la crisis en los organos judiciales (1T 2026)", "C4", "2025-12")
hecho("CB-C5-02", "Lanzamientos practicados por LAU, maximo 2013-2025", int(lz[(lz.ccaa == "Espana") & (lz.tipo == "LAU")].lanzamientos.max()), None, None, "lanzamientos/anio", "2013-2025", "Espana", "CGPJ", "C4", "2025-12")
hecho("CB-C5-03", "Hechos conocidos por allanamiento/usurpacion de inmuebles", int(us[(us.ccaa == "Espana") & (us.año == 2025)].hechos_conocidos.iloc[0]), None, None, "hechos/anio", "2025", "Espana", "Ministerio del Interior, Portal Estadistico de Criminalidad", "C4", "2025-12")
hecho("CB-C5-04", "Verbales posesorios por ocupacion ilegal de viviendas ingresados", int(vp[(vp.ccaa == "Espana") & (vp.año == 2025)].verbales_posesorios_ingresados.iloc[0]), None, None, "procedimientos/anio", "2025", "Espana", "CGPJ", "C4", "2025-12")
hecho("CB-C5-05", "Viviendas principales en alquiler (Censo 2021)", int(alq_censo_total), None, None, "viviendas", "2021", "Espana", "INE Censo 2021 (secciones), fuente unica", "C4", "2021-11")
rho = {k: (round(v[2], 2), round(ph[k], 3)) for k, v in res5.items()}
hecho("CB-C6-01", "Declarantes IRPF con ingresos de capital inmobiliario", int(decl24.declarantes), None, None, "declarantes", "2024", "Territorio de regimen fiscal comun", FA, "C4", "2026-06")
hecho("CB-C6-02", "Declarantes IRPF con reduccion por arrendamiento de vivienda (art. 23.2 LIRPF)", int(red24.declarantes), None, None, "declarantes", "2024", "Territorio de regimen fiscal comun", FA, "C4", "2026-06")
hecho("CB-C6-03", "Viviendas equivalentes arrendadas por personas fisicas (habitual y otras)", int(viv_arr_equiv), None, None, "viviendas", "2024", "Territorio de regimen fiscal comun", "AEAT, Estadistica de viviendas declaradas en el IRPF 2024", "C4", "2026-06")
hecho("CB-C6-04", "Viviendas equivalentes arrendadas por personas fisicas por declarante con ingresos de capital inmobiliario", round(ratio_viv, 2), None, None, "viviendas/declarante", "2024", "Territorio de regimen fiscal comun", "AEAT (dos estadisticas)", "C4", "2026-06")
hecho("CB-C6-05", "Residual (PJ + sector publico + alquiler no declarado) sobre el stock en alquiler", round(100 * res_a, 1), round(100 * min(res_a, res_b), 1), round(100 * max(res_a, res_b), 1), "% del stock", "2021-2025", "Espana sin Navarra ni Pais Vasco", "AEAT 2024; INE Censo 2021; INE ECV 2025; INE ECH 2025T4", "C4", "2026-06")
hecho("CB-C8-01", "Compraventas con comprador persona juridica", pj_flujo, None, None, "% de compraventas", "2024", "Espana", "INE ETDP 50272 (R1C-004)", "C4", "2024-12")
json.dump(hechos, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ resultado y fichas
rmin, rmax = round(100 * min(res_a, res_b), 1), round(100 * max(res_a, res_b), 1)
resultado = dict(
    rama="CB", pregunta="C5 seguridad juridica y oferta de alquiler; C6 pequenos y grandes arrendadores; C8 peso de empresas en stock y flujos",
    capa="C4", datos="CGPJ (lanzamientos y verbales posesorios por TSJ); Interior (allanamiento/usurpacion CCAA); INE Censo 2021, ECV 9997, ECH 60131, ETDP 50272; AEAT IRPF 2019-2024 y viviendas declaradas 2024",
    N=17, metodo="Descriptivo; correlacion de Spearman (p por permutacion, 10.000, seed 20261010) con Holm sobre 6 especificaciones; residual de stock AEAT frente a Censo/ECV",
    estimacion=dict(spearman_c5={k: dict(rho=round(v[2], 2), p=round(v[3], 3), p_holm=round(ph[k], 3), x=v[0], y=v[1]) for k, v in res5.items()},
                    residual_pj_publico_no_declarado_pct=dict(censo2021=round(100 * res_a, 1), ecv2025=round(100 * res_b, 1)),
                    viviendas_equiv_por_declarante=round(ratio_viv, 2), comprador_pj_pct=pj_flujo),
    ic95=None, p_ajustado={k: round(v, 4) for k, v in ph.items()},
    nivel_evidencia="DESCRIPTIVO / EXPLORATORIO (C4)",
    diagnosticos=dict(secciones_censo=n_sec, ccaa=len(P), fechas_distintas="Censo 2021 vs AEAT 2024 vs ECV 2025", rho=rho),
    fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
    notas="Sin diseno causal. AEAT no publica distribucion por numero de inmuebles del arrendador; Catastro, Notariado, Censo (arrendador) y IS por actividad: SIN DATO (docs/v5/fuentes_fallidas.md, seccion CB). Fianzas por CCAA: solo Comunitat Valenciana (GVA).")
json.dump(resultado, open(OUT / "resultado.json", "w"), ensure_ascii=False, indent=1)
ficha = lambda i, tema, enun, v, mag, regla, lim, ev: dict(id=i, tema=tema, enunciado=enun, capa="C4", magnitud=mag, intervalo=None, cota="Sin cota (C4)", literatura="No consultada en este modulo", veredicto=v, regla=regla, limites=lim, evidencia=ev, convenciones="Cifras con fecha del dato; sin lenguaje causal")
fichas = [
    ficha("CB-V1", "Seguridad jurídica y oferta", "La ocupación ilegal reduce la oferta de alquiler.", "ANALIZADA, NO CONCLUYENTE",
          f"N=17 CCAA; Spearman usurpacion/100.000 viv. con cuota de alquiler: rho={res5['C5-S2'][2]:.2f} (p Holm {ph['C5-S2']:.4f}); verbales posesorios con cuota: rho={res5['C5-S3'][2]:.2f} (p Holm {ph['C5-S3']:.4f}). Las especificaciones sobre variaciones 2021-2025 y sobre lanzamientos por LAU no son significativas (registro.csv). El signo es positivo (mas usurpaciones donde hay mas alquiler), contrario al de la afirmacion; es compatible con que ambas magnitudes crecen con la urbanizacion. Sin diseno que identifique un efecto.",
          "Con C4 y sin identificacion, como maximo ANALIZADA, NO CONCLUYENTE.",
          "Una asociacion entre CCAA no distingue oferta, demanda ni composicion; el denominador (viviendas) y el numerador (denuncias) dependen del tamano del parque; el delito de usurpacion incluye inmuebles que no son vivienda; fianzas por CCAA no disponibles.",
          "CGPJ 1T 2026; Interior 2025; INE Censo 2021 y ECV 2025; tablas en output/v5/CB/tablas"),
    ficha("CB-V2", "Arrendadores", "La mayoría de los caseros son pequeños propietarios.", "ANALIZADA, NO CONCLUYENTE",
          f"Personas fisicas declaran {arr_hab_equiv:,.0f} viviendas equivalentes arrendadas como vivienda habitual (IRPF 2024); el residual PJ+publico+no declarado es {rmin}-{rmax} % del stock; {ratio_viv:.2f} viviendas equivalentes por declarante con ingresos de capital inmobiliario.".replace(",", "."),
          "Falta la distribucion por numero de inmuebles (1, 2-4, >=5): la AEAT no la publica; el promedio no la sustituye. Los datos acotan el peso de las personas juridicas, no el tamano de las carteras de las personas fisicas.",
          "Fechas distintas entre fuentes; Navarra y Pais Vasco fuera de la AEAT; copropiedad cuenta como declarantes separados.", "AEAT IRPF 2024; INE Censo 2021, ECV 2025, ECH 2025T4"),
    ficha("CB-V3", "Empresas en el alquiler", "Las empresas y fondos dominan el alquiler.", "ANALIZADA, NO CONCLUYENTE",
          f"Flujo de compra con comprador PJ: {pj_flujo} % de compraventas (ETDP 2024). Stock: el residual PJ+publico+no declarado del alquiler principal es {rmin} % (stock del Censo 2021) y {rmax} % (stock ECV 2025); los dos métodos discrepan y se dan ambos. Es una cota superior del peso de las empresas bajo esos supuestos.",
          "Bajo los supuestos declarados, ninguna de las dos estimaciones del residual alcanza el 50 % del stock de vivienda principal en alquiler; ambas son C4 (fechas distintas, fuente unica del Censo, discrepancia entre ellas) y no miden el peso por zonas ni por tamano de cartera.",
          "No se localizo Catastro por naturaleza del titular, Notariado ni Censo por tipo de arrendador; concentracion local (grandes ciudades) no medida.", "INE ETDP 2024; AEAT 2024; INE Censo 2021; INE ECV 2025"),
]
json.dump(fichas, open(OUT / "fichas_verificador.json", "w"), ensure_ascii=False, indent=1)
print(P.round(2).to_string())
print({k: (round(v[2], 2), round(v[3], 3), round(ph[k], 3)) for k, v in res5.items()})
print("residual", res_a, res_b, "ratio_viv", ratio_viv, "alq censo", alq_censo_total, alq_censo_comun, stock_ecv25, arr_hab_equiv, viv_arr_equiv)
print(ir.pivot(index="año", columns="concepto", values="declarantes"))
