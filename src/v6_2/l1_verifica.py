"""L1 (v6.2): comprobación del anexo metodológico (output/v6_2/anexo_metodologico.md).

Sigue LITERALMENTE las fichas del anexo: lee solo data/raw (y, donde el anexo lo declara, una tabla intermedia
versionada de output/), recalcula cada cifra y la compara con output/v5/cifras_clave.csv (o con
output/v6_2/L3/hechos.json para las cifras L3). Sin red. SEED=20261010. No lee data/sealed.
Salida: output/v6_2/L1/verificacion.csv y output/v6_2/L1/resultado.json.
"""
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v6_2" / "L1"
OUT.mkdir(parents=True, exist_ok=True)
R: dict[str, dict] = {}
TOL = 0.15


def put(k, valor, mn, mx, fuente_tipo, nota=""):
    R[k] = dict(valor=valor, min=mn, max=mx, fuente_tipo=fuente_tipo, nota=nota)


def rd(f, **kw):
    return pd.read_csv(RAW / f, **kw)


def nucleo(c: dict) -> list:
    """Mayor conjunto de fuentes cuyos niveles acumulados (1+x) distan <= 15 % entre el mayor y el menor."""
    ks = sorted(c, key=lambda k: c[k])
    best: list = []
    for i in range(len(ks)):
        for j in range(i, len(ks)):
            if (1 + c[ks[j]]) / (1 + c[ks[i]]) - 1 <= TOL and j - i + 1 > len(best):
                best = ks[i:j + 1]
    return best


# ============ F1. Hogares (ECP, EPA) =========================================
h = rd("ine_hogares_60131.csv")
ECP = h[h.nombre == "Total Nacional. Total. Hogares en viviendas familiares. Número."].set_index("periodo").valor
e = rd("ine_epa_hogares.csv")
EPA = e[e.nombre == "Hogares. Total Nacional. Ambos sexos. Total. Total."].set_index("periodo").valor * 1000


def media_anual(s, y):
    return float(s[[f"{y}T{q}" for q in (1, 2, 3, 4)]].mean())


# dh_2125: EPA (media anual 2025 - media anual 2021) y ECP (2025T1 - 2021T1); central = punto medio
d_epa = media_anual(EPA, 2025) - media_anual(EPA, 2021)
d_ecp = float(ECP["2025T1"] - ECP["2021T1"])
lo, hi = sorted([d_epa, d_ecp])
put("dh_2125", (lo + hi) / 2, lo, hi, "raw")

# ============ F2. Terminadas MIVAU ===========================================
g = rd("mivau_v2_iniciadas_terminadas_prov.csv", dtype={"periodo": str})
p = rd("mivau_v2_protegida.csv", dtype={"periodo": str})
pq = rd("mivau_parque.csv", dtype={"periodo": str})


def serie(df, nombre):
    x = df[df.serie == nombre]
    return x.groupby(x.periodo.str[:4].astype(int)).valor.sum()


LIB = serie(g, "viv_libres_terminadas_anual_nacional")
PROT = serie(p, "prot_definitiva_anual_nacional")
PARQ = serie(pq, "parque_total_viviendas_nacional")
LIB_C, PROT_C = LIB.copy(), PROT.copy()
for cc in ("pais_vasco", "navarra_comunidad_foral_de"):
    LIB_C = LIB_C.sub(serie(g, f"viv_libres_terminadas_anual_ccaa_{cc}"), fill_value=0)
    PROT_C = PROT_C.sub(serie(p, f"prot_definitiva_anual_ccaa_{cc}"), fill_value=0)
COMUN = (LIB_C + PROT_C).loc[2019:2024]
put("terminadas_1924", None, float(COMUN.min()), float(COMUN.max()), "raw")

# ============ F3. Déficit 2021-2024 (v4 M0, histórico) =======================
ANIOS = [2021, 2022, 2023, 2024]
CORR = 242_400.0
dh_epa_c = float(EPA["2024T4"] - EPA["2020T4"]) + CORR
dh_ecp = float(ECP["2024T4"] - ECP["2021T1"])
T_con = float((LIB.reindex(ANIOS) + PROT.reindex(ANIOS).fillna(0)).sum())
T_sin = float(LIB.reindex(ANIOS).sum())
PARK0 = PARQ.reindex([y - 1 for y in ANIOS]).values
comb = [dh - (t - float(np.nansum(b * PARK0))) for dh in (dh_epa_c, dh_ecp) for t in (T_con, T_sin) for b in (0.0, 0.001, 0.002)]
sb = [dh - t for dh in (dh_epa_c, dh_ecp) for t in (T_con, T_sin)]
put("deficit_2124_c1", None, min(sb), max(sb), "raw", "12 combinaciones; C1 = las 4 sin bajas")
put("deficit_2124_c2", None, min(comb), max(comb), "raw")

# ============ F3b. Déficit L3 (v6.2) ==========================================
cat = rd("catastro_urbana_municipios.csv.gz", usecols=["periodo", "valor", "unidad"])
uu = cat[cat.unidad == "unidades_urbanas_residenciales"].groupby("periodo").valor.sum()
cat_d = {y: float(uu[y + 1] - uu[y]) for y in ANIOS}             # ejercicio N = 1-ene-N
comp_pvna = float(((LIB + PROT) - (LIB_C + PROT_C)).reindex(ANIOS).sum())   # País Vasco + Navarra (MIVAU)
T_cat = sum(cat_d.values()) + comp_pvna
var = EPA.diff()
base = float(EPA["2024T4"] - EPA["2020T4"])
salto = float(EPA["2021T1"] - EPA["2020T4"])
t2 = float(np.mean([var["2020T4"], var["2021T2"]]))
t4 = float(np.mean([var["2020T3"], var["2020T4"], var["2021T2"], var["2021T3"]]))
rr = float(ECP["2021T1"] / EPA["2021T1"])
pre = float(np.mean([var[k] for k in ("2020T1", "2020T2", "2020T3", "2020T4")]))
H = {"v1": base + CORR, "a": base, "b": base - salto + t2, "b4": base - salto + t4, "c": base - salto,
     "d1": float(ECP["2024T4"]) - float(EPA["2020T4"]) * rr, "d2": float(ECP["2024T4"]) - (float(ECP["2021T1"]) - pre),
     "e": float(ECP["2024T4"] - ECP["2021T1"])}
T = {"con": T_con, "sin": T_sin, "cat": T_cat}
sb3 = [H[k] - T[t] for k in H for t in T]
cb3 = [H[k] - (T[t] - float(np.nansum(b * PARK0))) for k in H for t in T for b in (0.001, 0.002)]
lo3, hi3 = min(sb3), max(sb3)
put("L3-DEF-2124-SINBAJAS", (lo3 + hi3) / 2, lo3, hi3, "raw", json.dumps({k: round(v) for k, v in H.items()}))
put("L3-DEF-2124-CONBAJAS", (lo3 + max(cb3)) / 2, lo3, max(cb3), "raw")

# ============ F4. Alquiler y precios (A23) ===================================
ip = rd("ine_ipc_alquiler.csv")
ix = ip[ip.nombre == "Nacional. Alquiler de vivienda. Índice."]
ipc_a = ix.groupby(ix.periodo.str[:4].astype(int)).valor.mean()
v = rd("ine_v2_ipva.csv")
ipn = v[(v.nivel == "nacional") & (v.medida == "IPVA_indice")].pivot_table(index="periodo", columns="desglose", values="valor")
srp = rd("pdf/serpavi_esp_agregado.csv")
serp = srp[srp.serie == "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_constante"].set_index("periodo").valor
comp = {"IPC": ipc_a[2024] / ipc_a[2015] - 1, "SERPAVI": serp[2024] / serp[2015] - 1,
        "IPVA_existente": ipn["Contrato existente"][2024] / 100 - 1, "IPVA_total": ipn["Total"][2024] / ipn["Total"][2015] - 1}
nu = nucleo(comp)
put("A23-A2", None, 100 * min(comp[k] for k in nu), 100 * max(comp[k] for k in nu), "raw", f"núcleo={nu}; {comp}")

vt = rd("mivau_valor_tasado_nacional_ccaa_prov.csv")
s = vt[vt.serie == "valor_tasado_libre_nacional"]
s = s.groupby(s.periodo.str[:4].astype(int)).valor.agg(["mean", "count"])
s = s[s["count"] == 4]["mean"]
rg = rd("pdf/registradores_opendata_anual.csv")
rs = rg[(rg.serie == "compraventas_viv_pm2") & (rg.nivel == "nacional")]
rs = pd.Series(rs.valor.to_numpy(), index=rs.periodo.astype(int).to_numpy())
cg = rd("pdf/notariado_cgn_extranjeros_semestral.csv")
cg = cg[(cg.serie == "precio_m2") & (cg.categoria == "Total general")]
cg = cg.groupby(cg.periodo.str[:4].astype(int)).valor.agg(["mean", "count"])
cg = cg[cg["count"] == 2]["mean"]
cp = {"MIVAU_tasado": s[2025] / s[2015] - 1, "Notariado": cg[2025] / cg[2015] - 1, "Registradores": rs[2025] / rs[2015] - 1}
nu = nucleo(cp)
put("A23-P2", 100 * float(np.median(list(cp.values()))), 100 * min(cp[k] for k in nu), 100 * max(cp[k] for k in nu), "raw",
    f"{cp}")

vc = v[(v.nivel == "provincia") & (v.tabla == 59005) & (v.medida == "IPVA_indice") & (v.desglose == "Nuevo contrato")]
vc = vc.pivot_table(index="periodo", columns="territorio", values="valor")
sp = rd("pdf/serpavi_provincias.csv")
w = sp[(sp.variable == "n_contratos") & (sp.tipologia == "VC") & (sp.periodo == 2024)]
# cruce POR NOMBRE, como el código publicado (SERP2IPVA): «Alicante» -> Alicante/Alacant; «Castellón/Castelló» igual;
# la fila de Valencia se llama «Valencia/Valéncia» (tilde aguda) y NO cruza -> NaN -> media de la CCAA (corrección v6.1)
w = w.set_index(w.nombre.replace({"Alicante": "Alicante/Alacant", "Castellón": "Castellón/Castelló", "Valencia": "Valencia/València"})).valor
prov = {"Alicante/Alacant": 3, "Castellón/Castelló": 12, "Valencia/València": 46}
wv = pd.Series({t: w.get(t, np.nan) for t in prov})
w_cod = sp[(sp.variable == "n_contratos") & (sp.tipologia == "VC") & (sp.periodo == 2024)].set_index("codigo").valor
wv_alt = pd.Series({t: w_cod.get(c, np.nan) for t, c in prov.items()})   # cruce por código (variante, no publicada)
wv = wv.fillna(wv.mean())
gn = pd.Series({t: 100 * (vc.loc[2024, t] / vc.loc[2021, t] - 1) for t in prov})
ipva_cv = float(np.average(gn, weights=wv)) / 100
fz = pd.concat([pd.read_csv(RAW / f"v5/gva_fianzas_{y}.csv", sep=";") for y in range(2020, 2027)])
fz["imp"] = pd.to_numeric(fz.importe_fianza, errors="coerce")
fz = fz[(fz.imp >= 100) & (fz.imp <= 5000)]
md = fz.groupby(fz.anyo_datos.astype(int)).imp.median()
gva = float(md[2024] / md[2021] - 1)
cv = {"IPVA_nuevo": ipva_cv, "GVA": gva}
nu = nucleo(cv)
lo, hi = 100 * min(cv[k] for k in nu), 100 * max(cv[k] for k in nu)
gn_alt = float(np.average(gn, weights=wv_alt))
put("A23-A10", (lo + hi) / 2, lo, hi, "raw", f"{cv}; pesos={wv.to_dict()}; IPVA_nuevo con cruce por código={gn_alt:.2f} %")

# ============ F5. Tenencia (R1C-001) =========================================
eff = rd("v3/eff_tenencia_edad_v3.csv")
v_eff = float(eff[(eff.serie == "eff_pct_hogares_vivienda_principal|edad=total|ed=DO 2413 (EFF2022)") & (eff.periodo == 2022)].valor.iloc[0])
ecv = rd("v3/ine_ecv_tenencia_edad_v3.csv")
SEC = "ecv_pct_hogares_tenencia|{}|edad_persona_referencia=Total|sexo=Ambos sexos"
v_ecv = float(ecv[(ecv.serie == SEC.format("Propiedad")) & (ecv.periodo == 2022)].valor.iloc[0])
c59 = rd("v4/ine_v4_t59523.csv").set_index("serie_nombre").valor
v_cen = 100 * c59["Total Nacional, En propiedad, Total (tamaño de municipio)"] / c59["Total Nacional, Total (régimen de tenencia), Total (tamaño de municipio)"]
vals = [v_eff, v_ecv, v_cen]
put("R1C-001", float(np.mean(vals)), min(vals), max(vals), "raw")

# ============ F6. Viviendas turísticas (B4-v3-vut-cantidad) ==================
vut = rd("ine_v2_vut.csv", dtype=str, usecols=["periodo", "valor", "nivel", "medida"])
vut = vut[(vut.nivel == "nacional") & (vut.medida == "viviendas_turisticas")].set_index("periodo").valor.astype(float)
dv = vut["2024M08"] - vut["2020M08"]
ci = rd("v3/ine_v3_censo2021_seccion_indicadores.csv.gz", usecols=["serie", "valor", "codigo"], dtype={"codigo": str})
st_cen = float(ci[ci.serie == "t20_2"].drop_duplicates("codigo").valor.sum())
cuota = sum(float(ecv[(ecv.serie == SEC.format(k)) & (ecv.periodo == 2021)].valor.iloc[0])
            for k in ("Alquiler a precio de mercado", "Alquiler inferior al precio de mercado"))
st_ecv = cuota / 100 * float(ECP["2021T4"])
q = [100 * dv / st_cen, 100 * dv / st_ecv]
put("B4-v3-vut-cantidad", q[0], min(q), max(q), "raw", f"dVUT={dv:.0f}; stock censo={st_cen:.0f}; stock ECV={st_ecv:.0f}")

# ============ F7. Demanda latente por convivencia ============================
es_ = rd("v3/eurostat_emancipacion_tenencia_v3.csv")
es_ = es_[es_.fuente.str.contains("lvps08") & es_.serie.str.contains("Y25-34_T_con_padres") & (es_.codigo == "ES")].set_index("periodo").valor
j = json.loads((RAW / "v3/pa_aux/ine_t65944.json").read_text())
ep = {}
for x in j:
    m = re.match(r"Total Nacional\. Ambos sexos\. De (25 a 29|30 a 34) años\. (Total|Hijo/a)\. Personas", x["Nombre"])
    if m:
        for d in x["Data"]:
            ep[(int(d["Anyo"]), m.group(2))] = ep.get((int(d["Anyo"]), m.group(2)), 0) + d["Valor"]
t_epa = {y: 100 * ep[(y, "Hijo/a")] / ep[(y, "Total")] for y in (2008, 2025)}
pob25 = ep[(2025, "Total")] * 1000
lat = [(t25 - t08) / 100 * pob25 / k for (t08, t25) in ((es_[2008], es_[2025]), (t_epa[2008], t_epa[2025])) for k in (1.5, 2.0)]
put("latente_convivencia", None, round(min(lat), -3), round(max(lat), -3), "raw", f"{[round(x) for x in lat]}")

# ============ F8. Proyección de hogares (B1-H4, E-B1-F) ======================


def kn(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = s.split("/")[0].split(",")[0]
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z]", "", s)


PROVS = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_provincias.csv", dtype={"cod_prov": str}).provincia  # solo nombres (52)
hp = rd("v5/ine_b1_t54562_proy_hogares.csv")
hp = hp[hp.nombre.str.endswith(". Total. ")].copy()
hp["k"] = hp.nombre.str.replace(". Total. ", "", regex=False).map(kn)
hnac = hp[hp.k == "totalnacional"].set_index("anyo").valor
hp = hp[hp.k != "totalnacional"].drop_duplicates(["k", "anyo"]).pivot(index="k", columns="anyo", values="valor")
pp = rd("v5/ine_b1_t36726_proy_poblacion_prov.csv")
mm = pp.nombre.str.extract(r"^Total\. Población\. (.+?)\. Proyección a corto plazo\. (.+?)\. $")
pp = pp[mm[1] == "Todas las edades"].assign(k=mm[0].map(kn)).drop_duplicates(["k", "anyo"]).pivot(index="k", columns="anyo", values="valor")
ks = [kn(x) for x in PROVS]
f_ine = pd.Series({k: hp.loc[k, 2036] - hp.loc[k, 2026] for k in ks})
f_alt = pd.Series({k: hp.loc[k, 2026] * (pp.loc[k, 2036] / pp.loc[k, 2026] - 1) for k in ks})
F = (float(f_ine.sum()), float(np.minimum(f_ine, f_alt).sum()), float(np.maximum(f_ine, f_alt).sum()))
put("B1-H4", F[0], F[1], F[2], "raw", f"nacional INE 2036-2026 = {hnac[2036] - hnac[2026]:.0f}")
put("E-B1-F", F[0], F[1], F[2], "raw")

# ============ F9. Necesidad B1-H1 (tabla intermedia versionada) ==============
bn = pd.read_csv(RAIZ / "output/v5/B1/tablas/B1_nacional.csv").set_index("componente")
c_ = {s_: bn[s_] for s_ in ("min", "central", "max")}
n10 = {"central": sum(c_["central"][k] for k in "ARVF") - c_["central"]["M"] - c_["central"]["K"],
       "min": sum(c_["min"][k] for k in "ARVF") - c_["max"]["M"] - c_["max"]["K"],
       "max": sum(c_["max"][k] for k in "ARVF") - c_["min"]["M"] - c_["min"]["K"]}
put("B1-H1", n10["central"] / 10, n10["min"] / 10, n10["max"] / 10, "tabla intermedia (output/v5/B1/tablas/B1_nacional.csv)")

# ============ F10. Traslado de ayudas D1-H11/H12 (tabla intermedia A4) =======
a4 = pd.read_csv(RAIZ / "output/v5/A4/clasificacion_provincias.csv", dtype={"cod_prov": str})
ED = (0.3, 0.6, 1.0, 1.5)
for c in (1, 2):
    r = a4[a4.clase_2021_2025 == c].resp_oferta.clip(lower=0)
    lo_, ce, hi_ = r.quantile(.25), r.median(), r.quantile(.75)
    pz = [ed / (es + ed) for es in (lo_, ce, hi_) for ed in ED]
    put(f"D1-H1{c}", 100 * float(np.median([ed / (ce + ed) for ed in ED])), 100 * min(pz), 100 * max(pz),
        "tabla intermedia (output/v5/A4/clasificacion_provincias.csv)", f"n={len(r)}; es={lo_:.3f}/{ce:.3f}/{hi_:.3f}")

# ============ Comparación =====================================================
ck = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv").set_index("id")
l3 = {x["id"]: x for x in json.loads((RAIZ / "output/v6_2/L3/hechos.json").read_text())}


def red(x, ref):
    """Redondeo de comparación: al decimal publicado (porcentajes 1 decimal; recuentos a la unidad; latente a miles)."""
    if x is None or ref is None or (isinstance(ref, float) and np.isnan(ref)):
        return None
    return round(float(x), 1) if abs(float(ref)) < 1000 else round(float(x))


filas = []
for k, r in R.items():
    pub = l3.get(k) if k.startswith("L3-") else (ck.loc[k].to_dict() if k in ck.index else None)
    ok = True
    for campo in ("valor", "min", "max"):
        pv = pub.get(campo) if pub else None
        pv = None if pv is None or (isinstance(pv, float) and np.isnan(pv)) else float(pv)
        cv_ = r[campo]
        if pv is None and cv_ is None:
            continue
        if pv is None or cv_ is None:
            ok = ok and pv is None   # el anexo calcula un central que la cifra publicada deja vacío: no cuenta como fallo
            continue
        tol = 0.051 if abs(pv) < 1000 else 1.0
        ok = ok and abs(red(cv_, pv) - (round(pv, 1) if abs(pv) < 1000 else round(pv))) <= tol
    filas.append(dict(id=k, reproduce=ok, fuente=r["fuente_tipo"], valor=r["valor"], min=r["min"], max=r["max"],
                      pub_valor=pub.get("valor") if pub else None, pub_min=pub.get("min") if pub else None,
                      pub_max=pub.get("max") if pub else None, nota=r["nota"][:300]))
t = pd.DataFrame(filas)
t.to_csv(OUT / "verificacion.csv", index=False)
print(t[["id", "reproduce", "valor", "min", "max", "pub_valor", "pub_min", "pub_max"]].to_string())
