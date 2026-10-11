"""K4b: doble implementacion independiente de 15 cifras (solo data/raw, sin red, SEED=20261010).

Calcula cada cifra a partir de data/raw con una interpretacion a priori de la definicion
textual (docs/v5, informe_tecnico) y escribe output/v6_1/K4B/calculos.json.
No lee el codigo original ni cifras_clave.csv (la comparacion es otro paso: k4b_comparar.py).
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
RAW = Path(__file__).resolve().parents[2] / "data" / "raw"
OUT = Path(__file__).resolve().parents[2] / "output" / "v6_1" / "K4B"
OUT.mkdir(parents=True, exist_ok=True)
R = {}


def put(k, valor=None, mn=None, mx=None, nota=""):
    R[k] = {"valor": valor, "min": mn, "max": mx, "nota": nota}


def rd(f, **kw):
    return pd.read_csv(RAW / f, **kw)


# ---------------- hogares (ECP, EPA) ----------------
h = rd("ine_hogares_60131.csv")
ecp = h[h.nombre == "Total Nacional. Total. Hogares en viviendas familiares. Número."].set_index("periodo").valor
e = rd("ine_epa_hogares.csv")
epa = e[e.nombre == "Hogares. Total Nacional. Ambos sexos. Total. Total."].set_index("periodo").valor * 1000


def media_anual(s, y):
    return s[[f"{y}T{q}" for q in (1, 2, 3, 4)]].mean()


# EPA tiene ruptura 2020T4->2021T1 (-207,8 mil). Las ventanas se miden dentro de 2021+, sin cruzarla.
# Interpretacion a priori: aumento = variacion de la media anual 2021 -> 2025 en cada fuente.
d_ecp = media_anual(ecp, 2025) - media_anual(ecp, 2021)
d_epa = media_anual(epa, 2025) - media_anual(epa, 2021)
lo, hi = sorted([d_ecp, d_epa])
put("dh_2125", (lo + hi) / 2, lo, hi, "variacion de medias anuales 2021->2025; ECP y EPA (ambas dentro de 2021+, sin cruzar la ruptura)")
R["dh_2125"]["variante_T1"] = {"ECP 2025T1-2021T1": float(ecp["2025T1"] - ecp["2021T1"]),
                                "EPA 2025T1-2021T1": float(epa["2025T1"] - epa["2021T1"])}

# ---------------- terminadas ----------------
g = rd("mivau_v2_iniciadas_terminadas_prov.csv", dtype={"periodo": str})
p = rd("mivau_v2_protegida.csv", dtype={"periodo": str})
L = g[g.serie.str.startswith("viv_libres_terminadas_anual")]
P = p[p.serie.str.startswith("prot_definitiva_anual")]


def term(y, comun=False):
    y = str(y)
    t = L[(L.periodo == y) & (L.nivel == "nacional")].valor.sum() + P[(P.periodo == y) & (P.nivel == "nacional")].valor.sum()
    if comun:
        for d in (L, P):
            x = d[(d.periodo == y) & d.nivel.isin(["ccaa"]) & d.territorio.str.contains("Navarra|Vasco")]
            t -= x.valor.sum()
    return float(t)


serie_c = {y: term(y, True) for y in range(2019, 2025)}
put("terminadas_1924", None, min(serie_c.values()), max(serie_c.values()),
    "Ministerio: libres terminadas + protegidas definitivas, nacional menos Pais Vasco y Navarra; min-max anual 2019-2024")
R["terminadas_1924"]["serie"] = serie_c

# ---------------- deficit ----------------
T_min = sum(term(y) for y in range(2021, 2025))
cat = rd("catastro_urbana_municipios.csv.gz").assign(ejercicio=lambda d: d.periodo.astype(int))  # versionado; periodo = ejercicio
cs = cat[cat.serie.str.startswith("catastro_uu_res")].groupby("ejercicio").valor.sum()
# altas Catastro del anio Y = stock(ejercicio Y+1) - stock(ejercicio Y) (ejercicio = 1 de enero)
T_cat = float(sum(cs[y + 1] - cs[y] for y in range(2021, 2025)))
H_ecp = float(ecp["2024T4"] - ecp["2021T1"])  # ECP empieza en 2021T1: se toma como stock al inicio de 2021
H_epa = float(epa["2024T4"] - epa["2021T1"])
combos = {f"{hn}-{tn}": hv - tv for hn, hv in [("ECP", H_ecp), ("EPA", H_epa)] for tn, tv in [("Min", T_min), ("Cat", T_cat)]}
put("deficit_2124_c1", None, min(combos.values()), max(combos.values()),
    "dH(2021T1->2024T4) menos terminadas 2021-2024; 2 fuentes de hogares x 2 de terminadas (4 combinaciones; el original usa 12)")
R["deficit_2124_c1"]["combos"] = combos
R["deficit_2124_c1"]["T_min"], R["deficit_2124_c1"]["T_cat"] = T_min, T_cat

par = rd("mivau_parque.csv", dtype={"periodo": str})
pn = par[par.serie.str.contains("nacional") & par.serie.str.contains("total")]
parque = pn.set_index("periodo").valor if len(pn) else None
if parque is not None and len(parque):
    ys = [str(y) for y in range(2020, 2024)] if "2023" in parque.index else list(parque.index[-4:])
    pk = float(parque[ys].sum())
    c2max = max(combos.values()) + 0.002 * pk
    put("deficit_2124_c2", None, min(combos.values()), c2max, f"bajas 0,1-0,2 %/anio sobre parque (stock inicio de anio, suma {ys}); cota sup. = max c1 + 0,2 % x parque")
else:
    put("deficit_2124_c2", nota="parque no localizado")

# ---------------- proyeccion de hogares INE ----------------
pr = rd("v5/ine_b1_t54562_proy_hogares.csv")
pr["n"] = pr.nombre.str.strip()
nat = pr[pr.n == "Total Nacional. Total."].set_index("anyo").valor
F = float(nat[2036] - nat[2026])
_t = pr[pr.n.str.endswith(". Total.") & ~pr.n.str.startswith("Total Nacional")].copy()
_t["n"] = _t.n.str.replace(". Total.", "", regex=False)
_excl = ["Andalucía", "Aragón", "Canarias", "Castilla y León", "Castilla - La Mancha", "Cataluña", "Comunitat Valenciana",
         "Extremadura", "Galicia", "País Vasco", "Asturias, Principado de", "Navarra, Comunidad Foral de", "Murcia, Región de",
         "Madrid, Comunidad de", "Rioja, La", "Balears, Illes", "Cantabria"]
_w = _t[~_t.n.isin(_excl)].pivot_table(index="n", columns="anyo", values="valor")
F_prov = float((_w[2036] - _w[2026]).sum())
put("B1-H4", F, None, None, "H(2036)-H(2026) INE base nacional; rango min-max no reconstruible (no hay escenarios alternativos en raw)")
R["B1-H4"]["suma_provincial_49_unidades_no_concluyente"] = F_prov
put("E-B1-F", F, None, None, "idem B1-H4")

# ---------------- tenencia ----------------
eff = rd("v3/eff_tenencia_edad_v3.csv")
x = eff[eff.serie.str.contains("pct_hogares_vivienda_principal") & eff.serie.str.contains("edad=total") & eff.serie.str.contains("EFF2022") & (eff.periodo == 2022)]
v_eff = float(x.valor.iloc[0])
ecv = rd("v3/ine_ecv_tenencia_edad_v3.csv")
x = ecv[(ecv.serie == "ecv_pct_hogares_tenencia|Propiedad|edad_persona_referencia=Total|sexo=Ambos sexos") & ecv.periodo.isin([2021, 2022])]
v_ecv = float(x.valor.mean())
ci = pd.read_csv(RAW / "v3/ine_v3_censo2021_seccion_indicadores.csv.gz", usecols=["desglose", "valor"])
prop = ci[ci.desglose.str.strip() == "Viviendas en propiedad"].valor.sum()
prin = ci[ci.desglose.str.strip() == "Viviendas Principales"].valor.sum()
v_cen = float(100 * prop / prin)
vals = [v_eff, v_ecv, v_cen]
put("R1C-001", float(np.mean(vals)), min(vals), max(vals), "media y rango de EFF 2022, ECV 2021-22 (media) y Censo 2021 (propiedad/principales, suma de secciones)")
R["R1C-001"]["fuentes"] = {"EFF2022": v_eff, "ECV2021-22": v_ecv, "Censo2021": v_cen}

# ---------------- alquiler y precios ----------------
ip = rd("ine_ipc_alquiler.csv")
ix = ip[ip.nombre == "Nacional. Alquiler de vivienda. Índice."].copy()
ix["a"] = ix.periodo.str[:4].astype(int)
ma = ix.groupby("a").valor.mean()
ipc_g = float(100 * (ma[2024] / ma[2015] - 1))
v = rd("ine_v2_ipva.csv")
vn = v[(v.nivel == "nacional") & (v.medida == "IPVA_indice") & (v.desglose == "Total")].set_index("periodo").valor
ipva_g = float(100 * (vn[2024] / vn[2015] - 1))
put("A23-A2", None, min(ipc_g, ipva_g), max(ipc_g, ipva_g), "IPC alquiler (media anual del indice) e IPVA total nacional, 2015->2024; IPVA 'contrato existente' solo existe desde 2021, no se usa")
R["A23-A2"]["IPC"], R["A23-A2"]["IPVA_total"] = ipc_g, ipva_g

vt = rd("mivau_valor_tasado_nacional_ccaa_prov.csv")
s = vt[vt.serie == "valor_tasado_libre_nacional"].copy()
s["a"] = s.periodo.str[:4].astype(int)
sa = s.groupby("a").valor.mean()
g_vt = float(100 * (sa[2025] / sa[2015] - 1))
rg = rd("pdf/registradores_opendata_anual.csv")
rs = rg[(rg.serie == "compraventas_viv_pm2") & (rg.nivel == "nacional")].set_index("periodo").valor
g_rg = float(100 * (rs[2025] / rs[2015] - 1))
vals = [g_vt, g_rg]
put("A23-P2", float(np.mean(vals)), min(vals), max(vals), "SOLO 2 de 3 fuentes: valor tasado MIVAU y Registradores EUR/m2 (media anual 2025/2015). Notariado: serie nacional 2015-2025 no esta en data/raw")
R["A23-P2"]["valor_tasado"], R["A23-P2"]["registradores"] = g_vt, g_rg

# CV 2021-2024: IPVA nuevo contrato y fianzas GVA
vc = v[v.territorio.isin(["Alicante/Alacant", "Castellón/Castelló", "Valencia/València"]) & (v.medida == "IPVA_indice") & (v.desglose == "Nuevo contrato")]
vc = vc.pivot_table(index="periodo", columns="territorio", values="valor")
g_ipva = float(100 * (vc.loc[2024] / vc.loc[2021] - 1).mean()) if vc.shape[1] == 3 else np.nan  # media simple de 3 provincias (sin pesos)
med = {}
for y in (2021, 2024):
    f = pd.read_csv(RAW / f"v5/gva_fianzas_{y}.csv", sep=";")
    med[y] = float(pd.to_numeric(f.importe_fianza, errors="coerce").median())
g_fi = 100 * (med[2024] / med[2021] - 1)
vals = [x for x in (g_ipva, g_fi) if x == x]
put("A23-A10", float(np.mean(vals)) if vals else None, min(vals) if vals else None, max(vals) if vals else None,
    "IPVA nuevo contrato CV 2024/2021 y mediana de la fianza GVA 2024/2021")
R["A23-A10"]["IPVA_nuevo_CV"], R["A23-A10"]["fianza_mediana_GVA"], R["A23-A10"]["medianas"] = g_ipva, float(g_fi), med

# ---------------- no reconstruibles con lo publicado ----------------
NR = {
    "D1-H11": "Requiere clases A4 (falta/rentable), respuesta de oferta de A4 y rejilla eps_d; el informe no da formula ni parametros",
    "D1-H12": "Idem D1-H11",
    "B1-H1": "Requiere A (atraso+emancipacion), R (bajas T1), V, M (vacias movilizables por provincia), K, por 52 provincias; parametros de rejilla v3 no publicados en el texto",
    "latente_convivencia": "Requiere tasa de convivencia con padres 2008 por edad y poblacion joven; la fuente (EPA/ECV/Eurostat) y la edad no estan precisadas en el texto",
    "B4-v3-vut-cantidad": "Requiere stock de alquiler y conversion VUT->viviendas desplazadas (cota de v3) no descrita en el texto",
}
for k, m in NR.items():
    put(k, nota="NO RECONSTRUIBLE: " + m)

json.dump(R, open(OUT / "calculos.json", "w"), indent=1, ensure_ascii=False, default=float)
for k, v_ in R.items():
    print(k, v_["valor"], v_["min"], v_["max"])
