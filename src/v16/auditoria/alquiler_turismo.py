"""Auditoría V16 fase 1: alquiler_turismo (C4, descriptivo). SEED=20261010.

Todo se filtra con muestra_sellada_v6 == False (provincias 07, 22, 26, 28, 30, 31, 33, 35, 38, 44, 50 quedan fuera).
Los datos de terceros (OpenRTA) solo se usan para recuentos propios; no se escriben registros individuales.
No se abre ningún fichero de la muestra sellada.
"""
import glob
import gzip
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.auditoria._comun import RAIZ, SEED, base_resultado, escribe, zrob  # noqa: E402

np.random.seed(SEED)
RAW = RAIZ / "data/raw"
V16 = RAW / "v16/alquiler_turismo"
SALIDA = RAIZ / "output/v16/auditoria/alquiler_turismo"
d = pd.read_parquet(RAIZ / "data/processed/v16/alquiler_turismo.parquet")
d = d[~d.muestra_sellada_v6].copy()
# CCAA cuyas provincias son todas de la muestra sellada (Aragon, Asturias, Baleares, Canarias, Madrid, Murcia, Navarra, La Rioja):
# sus filas de nivel ccaa llevan muestra_sellada_v6 == False pero equivalen a provincias selladas; se excluyen de todos los calculos
CCAA_SELLADAS = {"02", "03", "04", "05", "13", "14", "15", "17"}
_m = (d.nivel == "ccaa") & d.territorio_codigo.isin(CCAA_SELLADAS)
N_FILAS_CCAA_SELLADAS_FILTRO_FALSE = int(_m.sum())
d = d[~_m].copy()
tr = pd.read_parquet(RAIZ / "data/processed/v16/alquiler_turismo_terceros.parquet")
tr = tr[~tr.muestra_sellada_v6].copy()
D = {}
AREA = {"08": "Barcelona", "17": "Girona", "20": "Euskadi", "01": "Euskadi", "48": "Euskadi", "29": "Malaga",
        "41": "Sevilla", "46": "Valencia", "25": "Lleida"}


def r(x, n=3):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def corr(a, b, how="pearson"):
    j = pd.concat([a, b], axis=1).dropna()
    if len(j) < 4:
        return None
    return r(j.iloc[:, 0].corr(j.iloc[:, 1], method=how))


def comp(a, b):
    """Compara dos series indexadas por territorio: niveles y razón a/b."""
    j = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    j = j[(j.a > 0) & (j.b > 0)]
    if len(j) < 4:
        return {"n": int(len(j))}
    rz = j.a / j.b
    return {"n": int(len(j)), "corr_pearson": corr(j.a, j.b), "corr_spearman": corr(j.a, j.b, "spearman"),
            "corr_log": corr(np.log(j.a), np.log(j.b)), "ratio_medio": r(rz.mean()), "ratio_mediana": r(rz.median()),
            "ratio_agregado": r(j.a.sum() / j.b.sum()), "suma_a": r(j.a.sum(), 0), "suma_b": r(j.b.sum(), 0),
            "ratio_p10_p90": [r(rz.quantile(.1)), r(rz.quantile(.9))]}


# ======================= 1. Inside Airbnb =======================
ia = d[d.fuente.str.startswith("Inside Airbnb")].copy()
ia["ronda"] = ia.periodo.str[:7]
ia["prov"] = ia.territorio_codigo.str[:2]
rondas = sorted(ia.ronda.unique())
D["1_ia_resumen"] = {"rondas": rondas, "provincias": sorted(ia.prov.unique()),
                     "nota": "Madrid y Mallorca/Menorca (28, 07) quedan fuera por la muestra sellada v6; cobertura efectiva: Barcelona, Girona, Euskadi, Malaga, Sevilla y Valencia"}


def pivot_mun(var, nivel="municipio"):
    x = ia[(ia.variable == var) & (ia.nivel == nivel)]
    return x.pivot_table(index="territorio_codigo", columns="ronda", values="valor", aggfunc="sum")


tt = pivot_mun("ia_anuncios_total_numero")
saltos = {}
for var in ["ia_anuncios_total_numero", "ia_anuncios_activos_numero", "ia_anuncios_vivienda_entera_numero"]:
    p = pivot_mun(var)
    lista, n_pares, n25 = [], 0, 0
    for a, b in zip(rondas[:-1], rondas[1:]):
        ok = tt[a].notna() & tt[b].notna() & (tt[a] >= 20) & (tt[b] >= 20)
        n_pares += int(ok.sum())
        q = p.loc[ok.index[ok]]
        rt = q[b] / q[a] - 1
        n25 += int((rt.abs() > .25).sum())
        for cod, v in rt.items():
            if abs(v) > 0.5:
                lista.append({"par": f"{a}->{b}", "cod": cod, "area": AREA.get(cod[:2]), "antes": r(q.loc[cod, a], 0),
                              "despues": r(q.loc[cod, b], 0), "var": r(v)})
    saltos[var] = {"pares_municipio_ronda_>=20_en_ambas": n_pares, "n_saltos_>25%": n25, "n_saltos_>50%": len(lista), "saltos_>50%": lista}
D["1a_saltos_municipio"] = saltos
cob = {}
for a, b in zip(rondas[:-1], rondas[1:]):
    ent = tt.index[tt[a].isna() & tt[b].notna()]
    sal = tt.index[tt[a].notna() & tt[b].isna()]
    cob[f"{a}->{b}"] = {"municipios_entran": int(len(ent)), "anuncios_entran": r(tt.loc[ent, b].sum(), 0),
                        "municipios_salen": int(len(sal)), "anuncios_salen": r(tt.loc[sal, a].sum(), 0)}
D["1a_cambio_cobertura_municipios"] = cob
ar = tt.copy()
ar["area"] = ar.index.str[:2].map(AREA)
tot = ar.groupby("area")[rondas].sum()
D["1a_total_por_area"] = {a: {c: r(tot.loc[a, c], 0) for c in tot.columns} for a in tot.index}
D["1a_var_area_consecutiva"] = {a: {f"{x}->{y}": r(tot.loc[a, y] / tot.loc[a, x] - 1) for x, y in zip(rondas[:-1], rondas[1:])} for a in tot.index}
sec = pivot_mun("ia_anuncios_total_numero", "seccion")
D["1a_secciones"] = {"n_secciones_por_ronda": {c: int(sec[c].notna().sum()) for c in sec.columns},
                     "secciones_variacion_>50%_(>=20_anuncios_en_ambas)": int(sum(((sec[b] / sec[a] - 1).abs().where((sec[a] >= 20) & (sec[b] >= 20)) > .5).sum() for a, b in zip(rondas[:-1], rondas[1:]))),
                     "secciones_pares_evaluables": int(sum(((sec[a] >= 20) & (sec[b] >= 20)).sum() for a, b in zip(rondas[:-1], rondas[1:])))}
act = pivot_mun("ia_anuncios_activos_numero")
D["1a_cuota_activos_sobre_total_por_area"] = {a: {c: r(act.loc[act.index.str[:2].map(AREA) == a, c].sum() / tt.loc[tt.index.str[:2].map(AREA) == a, c].sum()) for c in tt.columns} for a in sorted(set(AREA.values()))}
z_out = []
for a, b in zip(rondas[:-1], rondas[1:]):
    ok = (tt[a] >= 20) & (tt[b] >= 20)
    lv = np.log(tt.loc[ok, b] / tt.loc[ok, a])
    z = zrob(lv)
    for cod in z.index[z.abs() > 5]:
        z_out.append({"par": f"{a}->{b}", "cod": cod, "area": AREA.get(cod[:2]), "log_var": r(lv[cod]), "z": r(z[cod], 1)})
D["1a_atipicos_z>5_variacion_log_entre_rondas"] = {"n": len(z_out), "lista": z_out[:25]}

# 1b IA vs registros VUT (ronda 2026-09)
ia_all = tt["2026-09"].dropna()
g = pd.read_csv(RAW / "v9/gva_vut/cortes/vut_actual_2026-10-14.csv.gz", sep=";", encoding="latin-1", usecols=["cod_provincia", "cod_municipio", "signatura", "fecha_alta"])
g["cod"] = g.cod_provincia.astype(int).astype(str).str.zfill(2) + g.cod_municipio.astype(int).astype(str).str.zfill(3)
gv_n = g.groupby("cod").size()
D["2_gva_2026"] = {"filas": int(len(g)), "signaturas_duplicadas": int(g.signatura.duplicated().sum()), "filas_sin_fecha_alta": int(g.fecha_alta.isna().sum()),
                   "municipios": int(g.cod.nunique())}
gp = pd.read_csv(RAW / "v9/gva_vut/gva_vut_panel_municipio.csv", dtype={"ine5": str})
gc = gp[gp.tipo == "corte"].pivot_table(index="ine5", columns="fecha", values="stock")
D["2_gva_cortes"] = {"fechas": [str(c) for c in gc.columns], "total": {str(c): r(gc[c].sum(), 0) for c in gc.columns}}
gm = gp[gp.tipo == "mensual_reconstruido"].pivot_table(index="ine5", columns="fecha", values="stock", aggfunc="sum")
tot_m = gm.sum()
D["2_gva_mensual_reconstruido"] = {"primer": str(tot_m.index[0]), "ultimo": str(tot_m.index[-1]), "stock_ultimo": r(tot_m.iloc[-1], 0),
                                   "meses_con_caida_mensual_>2%": [str(i) for i, v in tot_m.pct_change().items() if v < -0.02]}
e = pd.read_csv(RAW / "v11/euskadi_vut/reate_viviendas_2026-10-15.csv.gz")
e["cod"] = e.cod_municipio.astype(str).str.zfill(5)
e["f"] = pd.to_datetime(e.fecha_inscripcion)
eu_n = e.groupby("cod").size()
D["2_euskadi_reate"] = {"filas": int(len(e)), "registros_duplicados": int(e["Nº registro"].duplicated().sum()), "sin_fecha": int(e.f.isna().sum()),
                        "altas_desde_2026-01": int((e.f > "2025-12-31").sum())}
c = pd.read_csv(RAW / "v9/cat_turisme/registre_turisme_agregat_municipi.csv.gz")
c = c[c.tipus_establiment == "Habitatges d'ús turístic"].copy()
c["cod"] = c.cod_ine.astype(int).astype(str).str.zfill(5)
cat_n = c.groupby("cod").n.sum()
ra = tr[(tr.variable == "andalucia_rta_registros_numero") & tr.desagregacion.isin(["grupo=Completa", "grupo=Por habitaciones"])]
vut = {"Valencia_GVA": gv_n, "Euskadi_REATE": eu_n, "Cataluna_HUT": cat_n, "Andalucia_OpenRTA": ra.groupby("territorio_codigo").valor.sum()}
PREF = {"Valencia": ("46",), "Euskadi": ("01", "20", "48"), "Cataluna": ("08", "17", "25"), "Andalucia": ("29", "41")}
reg = {}
for nom, s in vut.items():
    pref = PREF[nom.split("_")[0]]
    for ia_var, etq in [("ia_anuncios_vivienda_entera_numero", "entera"), ("ia_anuncios_activos_numero", "activos")]:
        p = pivot_mun(ia_var)["2026-09"].dropna()
        p = p[p.index.str.startswith(pref)]
        for umbral in (1, 20):
            x = p[ia_all.reindex(p.index) >= umbral]
            reg[f"{nom}__IA_{etq}__umbral{umbral}"] = comp(x, s.reindex(x.index))
D["1b_ia_vs_vut_niveles_2026-09"] = reg
cb = {}
pe = pivot_mun("ia_anuncios_vivienda_entera_numero")
m = (tt["2025-12"] >= 20) & (tt["2026-09"] >= 20)
dia = (pe["2026-09"] - pe["2025-12"])[m]
st0 = e[e.f <= "2025-12-31"].groupby("cod").size()
st1 = e[e.f <= "2026-09-25"].groupby("cod").size()
dd = st1 - st0.reindex(st1.index).fillna(0)
x = dia[dia.index.str.startswith(PREF["Euskadi"])]
cb["Euskadi_REATE_altas_2026_sin_bajas"] = {"n_municipios": int(len(x)), "corr_variaciones_abs": corr(x, dd.reindex(x.index).fillna(0)),
                                          "suma_variacion_IA_entera": r(x.sum(), 0), "suma_altas_REATE": r(dd.reindex(x.index).fillna(0).sum(), 0)}
dg = gc.iloc[:, -1] - gc.iloc[:, 0]
x = dia[dia.index.str.startswith("46")]
cb["GVA_corte_2025-01_a_2026-10 (periodos no alineados con IA)"] = {"n_municipios_IA": int(len(x)), "variacion_GVA_en_esos_municipios": r(dg.reindex(x.index).sum(), 0),
                                                                   "variacion_IA_entera": r(x.sum(), 0), "variacion_GVA_total_CV": r(dg.sum(), 0)}
D["1b_ia_vs_vut_variaciones"] = cb

# 1c IA vs VTE
vt = d[(d.variable == "ine_vte_viviendas_turisticas") & (d.nivel == "municipio")].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
comun = vt.index.intersection(tt.index)
cv = {"municipios_comunes_IA_VTE": int(len(comun))}
for ria, vper in [("2025-12", "2025-11"), ("2026-06", "2026-05"), ("2026-09", "2026-05")]:
    for var, etq in [("ia_anuncios_vivienda_entera_numero", "entera"), ("ia_anuncios_activos_numero", "activos")]:
        p = pivot_mun(var)[ria].reindex(comun)
        t_ = tt[ria].reindex(comun)
        for umb in (1, 20):
            cv[f"IA_{etq}_{ria}__VTE_viviendas_{vper}__umbral{umb}"] = comp(p[t_ >= umb], vt[vper].reindex(comun)[t_ >= umb])
for var, etq in [("ia_anuncios_vivienda_entera_numero", "entera"), ("ia_anuncios_activos_numero", "activos")]:
    p = pivot_mun(var)
    okc = comun[(tt["2025-12"].reindex(comun) >= 20) & (tt["2026-06"].reindex(comun) >= 20)]
    ya = np.log(p["2026-06"].reindex(okc) / p["2025-12"].reindex(okc))
    yb = np.log(vt["2026-05"].reindex(okc) / vt["2025-11"].reindex(okc))
    j = pd.concat([ya, yb], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    cv[f"variacion_log_IA_{etq}_2025-12_2026-06_vs_VTE_2025-11_2026-05"] = {
        "n": int(len(j)), "corr": corr(j.iloc[:, 0], j.iloc[:, 1]), "dif_media_pp": r(100 * (j.iloc[:, 0] - j.iloc[:, 1]).mean(), 1),
        "signo_opuesto_n": int((np.sign(j.iloc[:, 0]) * np.sign(j.iloc[:, 1]) < 0).sum())}
D["1c_ia_vs_vte"] = cv
pent = pivot_mun("ia_anuncios_vivienda_entera_numero")
gr = {}
for cod, nom in [("08019", "Barcelona"), ("29067", "Malaga"), ("41091", "Sevilla"), ("46250", "Valencia"), ("20069", "Donostia"), ("48020", "Bilbao")]:
    if cod in vt.index and cod in pent.index:
        gr[nom] = {"VTE_2025-11": r(vt.loc[cod, "2025-11"], 0), "VTE_2026-05": r(vt.loc[cod, "2026-05"], 0),
                   "IA_entera_2025-12": r(pent.loc[cod, "2025-12"], 0), "IA_entera_2026-06": r(pent.loc[cod, "2026-06"], 0),
                   "IA_total_2026-06": r(tt.loc[cod, "2026-06"], 0)}
D["1c_grandes_ciudades_VTE_vs_IA"] = gr
ciu = {}
_reg = {"08019": cat_n, "17079": cat_n, "46250": gv_n, "29067": vut["Andalucia_OpenRTA"], "41091": vut["Andalucia_OpenRTA"], "20069": eu_n, "48020": eu_n}
for cod, s_ in _reg.items():
    ciu[cod] = {"IA_entera_2026-09": r(pent.loc[cod, "2026-09"], 0) if cod in pent.index else None, "IA_total_2026-09": r(tt.loc[cod, "2026-09"], 0) if cod in tt.index else None,
                "registro_VUT": r(s_.get(cod), 0), "VTE_2026-05": r(vt.loc[cod, "2026-05"], 0) if cod in vt.index else None}
D["1b_ciudades_IA_registro_VTE"] = ciu
_gva = gc.loc["46250"] if "46250" in gc.index else None
D["1b_valencia_gva_cortes"] = {str(k_): r(v_, 0) for k_, v_ in _gva.items()} if _gva is not None else None
vtn = d[(d.variable == "ine_vte_viviendas_turisticas") & (d.nivel == "municipio")].groupby("periodo").valor.agg(["size", "sum"])
D["1c_vte_municipios_y_suma_por_corte"] = {str(i): [int(row["size"]), r(row["sum"], 0)] for i, row in vtn.iterrows()}
vnac = d[(d.variable == "ine_vte_viviendas_turisticas") & (d.nivel == "nacional")].set_index("periodo").valor
vprov = d[(d.variable == "ine_vte_viviendas_turisticas") & (d.nivel == "provincia")].groupby("periodo").valor.sum()
vmun = vtn["sum"]
D["1c_vte_nacional_y_ratios"] = {str(i): {"nacional": r(vnac[i], 0), "suma_provincias_no_selladas/nacional": r(vprov[i] / vnac[i]),
                                         "suma_municipios_no_selladas/nacional": r(vmun[i] / vnac[i])} for i in vnac.index if i in vprov.index}

# 1d moneda y precio
mon = {"snapshots_leidos": 0, "moneda_quote": {}, "precio_con_$": 0, "precio_con_euro": 0, "precio_igual_a_cotizacion_noche": [0, 0]}
for f in sorted(glob.glob(str(V16 / "original/insideairbnb/listings_*.csv.gz"))) + sorted(glob.glob(str(RAW / "v9/insideairbnb/listings_*.csv.gz"))):
    nom = Path(f).name
    if any(k in nom for k in ("madrid", "mallorca", "menorca")):
        continue
    cols = pd.read_csv(f, nrows=0).columns
    use = [c_ for c_ in ["price", "price_quote_raw", "price_quote_price_per_night"] if c_ in cols]
    x = pd.read_csv(f, usecols=use)
    mon["snapshots_leidos"] += 1
    pr = x.price.dropna().astype(str)
    mon["precio_con_$"] += int(pr.str.startswith("$").sum())
    mon["precio_con_euro"] += int(pr.str.contains("€").sum())
    if "price_quote_raw" in x:
        cur = x.price_quote_raw.dropna().astype(str).str.extract(r'"currency":\s*"([A-Z]{3})"')[0].value_counts()
        for k, v in cur.items():
            mon["moneda_quote"][k] = mon["moneda_quote"].get(k, 0) + int(v)
        pp = pd.to_numeric(pr.str.replace("[$,€]", "", regex=True), errors="coerce").reindex(x.index)
        q = x.price_quote_price_per_night
        mk = pp.notna() & q.notna()
        mon["precio_igual_a_cotizacion_noche"][0] += int(np.isclose(pp[mk], q[mk], atol=0.01).sum())
        mon["precio_igual_a_cotizacion_noche"][1] += int(mk.sum())
D["1d_precio_moneda"] = mon
pm = ia[(ia.variable == "ia_precio_noche_mediana") & (ia.nivel == "municipio")].pivot_table(index="territorio_codigo", columns="ronda", values="valor")
pn = ia[(ia.variable == "ia_precio_noche_n_numero") & (ia.nivel == "municipio")].pivot_table(index="territorio_codigo", columns="ronda", values="valor")
D["1d_precio_mediana_ciudades"] = {nom: {c_: r(pm.loc[cod, c_], 1) for c_ in pm.columns if pd.notna(pm.loc[cod, c_])}
                                   for cod, nom in [("08019", "Barcelona"), ("29067", "Malaga"), ("41091", "Sevilla"), ("46250", "Valencia"), ("20069", "Donostia"), ("48020", "Bilbao")] if cod in pm.index}
pz = [[cod, c_, r(pm.loc[cod, c_], 1)] for cod in pm.index for c_ in pm.columns if pd.notna(pm.loc[cod, c_]) and (pm.loc[cod, c_] < 10 or pm.loc[cod, c_] > 1500)]
D["1d_precio_mediana_fuera_de_10_1500"] = {"n": len(pz), "lista": pz[:15]}
zp = []
for c_ in pm.columns:
    ok = pn[c_] >= 20
    lz = zrob(np.log(pm.loc[ok.index[ok], c_]))
    zp += [[cod, c_, r(pm.loc[cod, c_], 1), r(lz[cod], 1)] for cod in lz.index[lz.abs() > 5]]
D["1d_precio_z>5_entre_municipios_n>=20"] = {"n": len(zp), "lista": zp[:15]}

# ======================= 2. Registros VUT =======================
alt = tr[tr.variable == "andalucia_rta_altas_acumuladas_numero"]
nm = sum(1 for _, gk in alt.groupby(["territorio_codigo", "desagregacion"]) if (np.diff(gk.sort_values("periodo").valor.values) < 0).any())
D["2_openrta_acumulado"] = {"series_municipio_grupo": int(alt.groupby(["territorio_codigo", "desagregacion"]).ngroups), "series_no_monotonas": nm,
                            "registros_total_no_sellada": r(tr[tr.variable == "andalucia_rta_registros_numero"].valor.sum(), 0),
                            "VFT_completa_mas_habitaciones": r(ra.valor.sum(), 0)}
import re  # noqa: E402
import collections  # noqa: E402
_tx = gzip.open(V16 / "_terceros/openrta_all_2026-10-17.csv.gz", "rt", encoding="utf-8").read()
_cod = re.findall(r"\b[A-Z]{1,5}/[A-Z]{2}/\d{3,6}\b", _tx)
_c = collections.Counter(_cod)
D["2_openrta_codigos_registro_repetidos"] = {"codigos_encontrados": len(_cod), "distintos": len(_c), "repeticiones_extra": int(sum(v - 1 for v in _c.values())),
                                            "max_repeticiones": int(max(_c.values())),
                                            "nota": "regex sobre el texto crudo (esquema mixto de 72/92 columnas): un codigo puede figurar en mas de un campo; cota superior de duplicados"}
del _tx
h = pd.read_csv(RAW / "v9/gva_vut/cortes/vut_historico_2025-01-26.csv.gz", sep=";", encoding="latin-1", usecols=["Signatura", "Estado", "Fecha alta", "Fecha baja"])
h["fa"] = pd.to_datetime(h["Fecha alta"], format="%d/%m/%Y", errors="coerce")
h["fb"] = pd.to_datetime(h["Fecha baja"], format="%d/%m/%Y", errors="coerce")
D["2_gva_historico"] = {"filas": int(len(h)), "signaturas_duplicadas": int(h.Signatura.duplicated().sum()),
                        "altas_por_anio_2019_2024": {str(a): int((h.fa.dt.year == a).sum()) for a in range(2019, 2025)},
                        "bajas_por_anio_2019_2024": {str(a): int((h.fb.dt.year == a).sum()) for a in range(2019, 2025)},
                        "altas_antes_2015": int((h.fa.dt.year < 2015).sum()), "baja_anterior_a_alta": int((h.fb < h.fa).sum()),
                        "estado_BAJA_sin_fecha_baja": int(((h.Estado == "BAJA") & h.fb.isna()).sum())}
sg26 = set(g.signatura.astype(str))
hs = set(h[h.Estado == "ALTA"].Signatura.astype(str))
D["2_gva_signaturas_alta_2025_en_2026"] = {"alta_2025": len(hs), "presentes_en_2026": len(hs & sg26), "nuevas_2026": len(sg26 - hs)}
D["2_madrid_vut"] = {"estado": "no auditado: provincia 28 en la muestra sellada v6 (0 filas tras el filtro)",
                     "cortes_declarados_en_ficha": "14 cortes 2025-04 a 2026-10; faltan 2025-08, 2025-10, 2025-11, 2026-02; formato MUNICIPIO/ISO-8859-1 en 2025-04 a 2025-09"}
D["2_filtrado"] = {"filas_ccaa_de_regiones_selladas_con_marca_False_excluidas": N_FILAS_CCAA_SELLADAS_FILTRO_FALSE, "filas_tras_filtro": int(len(d)), "fuentes_tras_filtro": sorted(d.fuente.str[:30].unique())}

# ======================= 3. INE =======================
ine = d[d.fuente.str.startswith("INE")].copy()
ine["op"] = ine.fuente.str.extract(r"INE, (\w+)")[0]
D["3_duplicados_clave_parquet"] = int(d.duplicated(["territorio_codigo", "nivel", "periodo", "variable", "desagregacion", "fuente"]).sum())
claves, conf, ntab = {}, 0, 0
for f in sorted(glob.glob(str(V16 / "original/ine_turismo/*.json.gz"))):
    ntab += 1
    t_ = Path(f).name.split("_")[2]
    for s in json.load(gzip.open(f)):
        for q in s["Data"]:
            if q.get("Valor") is None:
                continue
            kk = (s["COD"], q["Fecha"])
            if kk in claves:
                if claves[kk][0] != t_:
                    claves[kk][2] += 1
                    if abs(claves[kk][1] - q["Valor"]) > 1e-9:
                        conf += 1
            else:
                claves[kk] = [t_, q["Valor"], 0]
D["3_solapes_crudo_mismo_COD_fecha"] = {"tablas": ntab, "claves": len(claves), "solapes_entre_tablas": int(sum(v[2] for v in claves.values())), "discrepancias_de_valor": conf}
del claves
imp = {}
oc = ine[ine.unidad == "%"]
imp["porcentaje_fuera_0_100"] = [int(((oc.valor < 0) | (oc.valor > 100)).sum()), int(len(oc))]
pv = ine[ine.variable == "ine_vte_plazas_por_vivienda_turistica"]
imp["VTE_plazas_por_vivienda_>20"] = int((pv.valor > 20).sum())
imp["VTE_plazas_por_vivienda_<1"] = int((pv.valor < 1).sum())
imp["VTE_plazas_por_vivienda_p1_p50_p99"] = [r(pv.valor.quantile(q), 2) for q in (.01, .5, .99)]
pc = ine[ine.variable == "ine_vte_porcentaje_de_viviendas_turisticas_sobre_el_total_de_viviendas_censadas"]
imp["VTE_pct_viviendas_>30"] = int((pc.valor > 30).sum())
imp["valores_negativos_en_niveles"] = int(((~ine.unidad.str.contains("%|índice|tasa", regex=True)) & (ine.valor < 0)).sum())
a_ = d[d.variable == "ine_vte_plazas"].set_index(["territorio_codigo", "nivel", "periodo"]).valor
b_ = d[d.variable == "ine_vte_viviendas_turisticas"].set_index(["territorio_codigo", "nivel", "periodo"]).valor
c_ = d[d.variable == "ine_vte_plazas_por_vivienda_turistica"].set_index(["territorio_codigo", "nivel", "periodo"]).valor
jj = pd.concat([a_ / b_, c_], axis=1).dropna()
jj.columns = ["calc", "pub"]
imp["VTE_plazas/viviendas_calculado_vs_publicado_dif>0.1"] = [int(((jj.calc - jj.pub).abs() > .1).sum()), int(len(jj))]
D["3_unidades_y_rangos"] = imp
ine_m = ine[(ine.frecuencia == "M") & (~ine.unidad.str.contains("índice|tasa", regex=True)) & (ine.op.isin(["EOAP", "EOH", "EOT", "OAT"])) & (ine.valor > 0)]
rows, nser = [], 0
for key, gk in ine_m.groupby(["variable", "territorio_codigo", "nivel", "desagregacion"], sort=True):
    s = gk.assign(p=pd.PeriodIndex(gk.periodo, freq="M")).drop_duplicates("p").set_index("p").valor.sort_index()
    if len(s) < 40:
        continue
    s = s.reindex(pd.period_range(s.index[0], s.index[-1], freq="M"))
    y = np.log(s / s.shift(12)).dropna()
    if len(y) < 30:
        continue
    nser += 1
    z = zrob(y)
    rows += [(key[0], key[1], key[2], str(p_), float(y[p_]), float(z[p_])) for p_ in z.index[z.abs() > 5]]
at = pd.DataFrame(rows, columns=["variable", "cod", "nivel", "periodo", "log_yoy", "z"])
at["covid"] = (at.periodo >= "2020-03") & (at.periodo <= "2022-06")
at["op"] = at.variable.str.extract(r"ine_(\w+?)_")[0]
fc = at[~at.covid]
D["3_atipicos_yoy_log_z>5"] = {"series_mensuales_evaluadas": nser, "n_atipicos": int(len(at)), "n_en_ventana_covid_2020-03_2022-06": int(at.covid.sum()),
                               "n_fuera_covid": int(len(fc)), "por_operacion_fuera_covid": fc.op.value_counts().to_dict(),
                               "series_distintas_fuera_covid": int(fc.groupby(["variable", "cod", "nivel"]).ngroups),
                               "mayores_fuera_covid": fc.assign(a=lambda x: x.z.abs()).sort_values("a", ascending=False).head(10)[["variable", "cod", "nivel", "periodo", "log_yoy", "z"]].round(2).to_dict("records")}
cuts = list(vt.columns)
vz = {}
for a, b in zip(cuts[:-1], cuts[1:]):
    ok = (vt[a] >= 20) & (vt[b] > 0)
    lv = np.log(vt.loc[ok, b] / vt.loc[ok, a])
    z = zrob(lv)
    vz[f"{a}->{b}"] = {"n": int(ok.sum()), "mediana_logvar": r(lv.median()), "n_z>5": int((z.abs() > 5).sum()),
                       "n_pasan_a_0_o_ausentes": int(((vt[a] > 0) & (vt[b].fillna(0) == 0)).sum()), "var_total_pct": r(100 * (vt[b].sum() / vt[a].sum() - 1), 1)}
D["3_vte_variacion_entre_cortes_municipal"] = vz
rup = {}
for va, vb in [("ine_eoap_grado_de_ocupacion_por_plazas", "ine_eoap_grado_de_ocupacion_por_plazas_total_categorias"),
               ("ine_eoap_numero_de_plazas_estimadas", "ine_eoap_numero_de_plazas_estimadas_total_categorias"),
               ("ine_eoap_numero_de_apartamentos_estimados", "ine_eoap_numero_de_apartamentos_estimados_total_categorias"),
               ("ine_eoh_numero_de_plazas_estimadas", "ine_eoh_numero_de_plazas_estimadas_total_categorias"),
               ("ine_eoh_grado_de_ocupacion_por_plazas", "ine_eoh_grado_de_ocupacion_por_plazas_total_categorias"),
               ("ine_eot_numero_de_plazas_estimadas", "ine_eot_numero_de_plazas_estimadas_total_categorias")]:
    xa = d[d.variable == va].pivot_table(index=["territorio_codigo", "nivel"], columns="periodo", values="valor")
    xb = d[d.variable == vb].pivot_table(index=["territorio_codigo", "nivel"], columns="periodo", values="valor")
    com = xa.index.intersection(xb.index)
    cols = xa.columns.intersection(xb.columns)
    if len(com) == 0 or len(cols) == 0:
        rup[f"{va}"] = {"territorios_comunes": 0}
        continue
    rel = ((xa.loc[com, cols] - xb.loc[com, cols]) / xb.loc[com, cols]).abs()
    rup[f"{va}"] = {"territorios_comunes": int(len(com)), "periodos_comunes": int(len(cols)), "pares_validos": int(rel.notna().sum().sum()),
                    "dif_relativa_media_abs": r(np.nanmean(rel.values)), "dif_relativa_max": r(np.nanmax(rel.values))}
D["3_serie_antigua_vs_total_categorias_en_solape"] = rup
sal = {}
for var in ["ine_eoap_numero_de_plazas_estimadas", "ine_eoh_numero_de_plazas_estimadas", "ine_eot_numero_de_plazas_estimadas"]:
    x = d[(d.variable == var) & (d.frecuencia == "M")].pivot_table(index=["territorio_codigo", "nivel"], columns="periodo", values="valor")
    lg = np.log(x).diff(axis=1)
    z = lg.apply(zrob, axis=1)
    fl = (z.abs() > 5) & lg.abs().gt(0.15)
    sal[var] = {"series": int(len(x)), "saltos_>15%_y_z>5": int(fl.sum().sum()), "de_ellos_en_enero": int(sum(fl[cc].sum() for cc in x.columns if str(cc).endswith("-01"))),
                "periodos_con_mas_saltos": fl.sum().sort_values(ascending=False).head(4).to_dict()}
D["3_saltos_mensuales_plazas"] = sal
ip = d[d.variable == "ine_ipap_total_modalidades"].set_index("periodo").valor.sort_index()
_faltan = sorted(set(pd.period_range(ip.index[0], ip.index[-1], freq="M").astype(str)) - set(ip.index))
ip = ip.reindex(pd.period_range(ip.index[0], ip.index[-1], freq="M").astype(str))
ipy = d[d.variable == "ine_ipap_total_modalidades_tasa_de_variacion_interanual"].set_index("periodo").valor.sort_index()
jy = pd.concat([(100 * (ip / ip.shift(12) - 1)).rename("calc"), ipy.rename("pub")], axis=1).dropna()
D["3_ipap_coherencia_tasa"] = {"meses_faltantes_en_indice": _faltan, "n": int(len(jy)), "dif_abs_media_pp": r((jy.calc - jy.pub).abs().mean()), "dif_abs_max_pp": r((jy.calc - jy.pub).abs().max()),
                               "n_dif_>0.3pp": int(((jy.calc - jy.pub).abs() > .3).sum()), "indice_inicio_fin": [r(ip.iloc[0]), r(ip.iloc[-1])],
                               "saltos_mensuales_>5pct": [[str(i), r(v)] for i, v in (100 * ip.pct_change()).items() if abs(v) > 5][:10]}


def suma12(var_list, fin, nivel):
    out = None
    cols = [str(p) for p in pd.period_range(end=pd.Period(fin, "M"), periods=12, freq="M")]
    for v in var_list:
        x = d[(d.variable == v) & (d.nivel == nivel) & (d.frecuencia == "M")].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
        if not set(cols) <= set(x.columns):
            return None
        s = x[cols].sum(axis=1, min_count=12)
        out = s if out is None else out.add(s, fill_value=np.nan)
    return out


ev = {}
pern = ["ine_eoap_pernoctaciones_residentes_en_espana", "ine_eoap_pernoctaciones_residentes_en_el_extranjero"]
for nivel in ["provincia", "municipio"]:
    vp = d[(d.variable == "ine_vte_plazas") & (d.nivel == nivel)].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    vv = d[(d.variable == "ine_vte_viviendas_turisticas") & (d.nivel == nivel)].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    for fin0, fin1 in [("2024-11", "2025-11"), ("2025-05", "2026-05")]:
        s0, s1 = suma12(pern, fin0, nivel), suma12(pern, fin1, nivel)
        if s1 is None or s0 is None:
            continue
        com = s1.dropna().index.intersection(vp.index)
        o = {"n_territorios": int(len(com)), "EOAP_pernoct12m_vs_VTE_plazas": comp(s1.reindex(com), vp.loc[com, fin1]),
             "EOAP_pernoct12m_vs_VTE_viviendas": comp(s1.reindex(com), vv.loc[com, fin1])}
        if fin0 in vp.columns:
            j = pd.concat([np.log(s1.reindex(com) / s0.reindex(com)), np.log(vp.loc[com, fin1] / vp.loc[com, fin0])], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
            o["variacion_log_12m_EOAP_pernoct_vs_VTE_plazas"] = {"n": int(len(j)), "corr": corr(j.iloc[:, 0], j.iloc[:, 1]), "dif_media_pp": r(100 * (j.iloc[:, 0] - j.iloc[:, 1]).mean(), 1),
                                                                "signo_opuesto_n": int((np.sign(j.iloc[:, 0]) * np.sign(j.iloc[:, 1]) < 0).sum())}
        ev[f"{nivel}_{fin1}"] = o
D["3_eoap_pernoctaciones_vs_vte"] = ev
pl = d[(d.variable == "ine_eoap_numero_de_plazas_estimadas") & (d.nivel == "provincia")].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
vp = d[(d.variable == "ine_vte_plazas") & (d.nivel == "provincia")].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
com = pl.index.intersection(vp.index)
D["3_eoap_plazas_vs_vte_plazas_provincia_2025-11"] = comp(pl.loc[com, "2025-11"], vp.loc[com, "2025-11"])
oat = d[(d.variable == "ine_oat_pernoctaciones_total") & (d.frecuencia == "M")]
eoap = {}
for nv in ["nacional", "ccaa"]:
    e_ = None
    for v in pern:
        x = d[(d.variable == v) & (d.nivel == nv)].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
        e_ = x if e_ is None else e_ + x
    o_ = oat[oat.nivel == nv].pivot_table(index="territorio_codigo", columns="periodo", values="valor", aggfunc="first")
    com = e_.index.intersection(o_.index)
    cols = [cc for cc in e_.columns.intersection(o_.columns) if "2018" <= cc <= "2026-03"]
    if len(com) == 0:
        continue
    ra_ = o_.loc[com, cols] / e_.loc[com, cols]
    eoap[nv] = {"territorios": int(len(com)), "periodos": len(cols), "razon_OAT_EOAP_mediana": r(np.nanmedian(ra_.values)),
                "razon_p10_p90": [r(np.nanpercentile(ra_.values, 10)), r(np.nanpercentile(ra_.values, 90))]}
    if nv == "nacional":
        a1 = pd.Series(o_.loc[com].iloc[0][cols].values.astype(float), index=pd.PeriodIndex(cols, freq="M"))
        b1 = pd.Series(e_.loc[com].iloc[0][cols].values.astype(float), index=pd.PeriodIndex(cols, freq="M"))
        ya, yb = np.log(a1 / a1.shift(12)).replace([np.inf, -np.inf], np.nan).dropna(), np.log(b1 / b1.shift(12)).replace([np.inf, -np.inf], np.nan).dropna()
        jy2 = pd.concat([ya.rename("oat"), yb.rename("eoap")], axis=1).dropna()
        eoap[nv].update({"corr_niveles": corr(a1, b1), "n_yoy": int(len(jy2)), "corr_yoy_log": corr(jy2.oat, jy2.eoap), "dif_media_yoy_pp": r(100 * (jy2.oat - jy2.eoap).mean(), 1),
                         "dif_media_yoy_pp_sin_2020_2021": r(100 * (jy2[(jy2.index < "2020-03") | (jy2.index > "2021-12")].oat - jy2[(jy2.index < "2020-03") | (jy2.index > "2021-12")].eoap).mean(), 1),
                         "corr_yoy_log_sin_2020_2021": corr(jy2[(jy2.index < "2020-03") | (jy2.index > "2021-12")].oat, jy2[(jy2.index < "2020-03") | (jy2.index > "2021-12")].eoap),
                         "razon_por_anio": {a: r(a1[a1.index.year == int(a)].sum() / b1[b1.index.year == int(a)].sum()) for a in ["2018", "2019", "2022", "2023", "2024", "2025"]}})
D["3_oat_vs_eoap_pernoctaciones"] = eoap
oa = d[d.variable == "ine_oat_pernoctaciones_total"]
D["3_oat_periodos"] = {"anuales": sorted(oa[oa.frecuencia == "A"].periodo.unique()), "mensual_primero_ultimo": [oa[oa.frecuencia == "M"].periodo.min(), oa[oa.frecuencia == "M"].periodo.max()],
                       "desagregaciones": sorted(oa.desagregacion.unique())}

# ======================= 4. Zonas sin código INE =======================
cr = pd.read_csv(RAIZ / "docs/v16/fuentes/alquiler_turismo_correspondencia.csv", dtype=str)
zonas = cr[cr.estado == "zona_turistica_sin_codigo_ine"]
SELL = ("Canarias", "Baleares", "Asturias", "Murcia", "Navarra", "Rioja", "Madrid", "Pamplona", "Puerto de la Cruz", "Santa Cruz Tenerife", "Aragón")
D["4_descartes"] = {"series_zona_sin_codigo": int(len(zonas)), "por_tabla": zonas.ambito.value_counts().to_dict(),
                    "estados_n_series": cr.groupby("estado").n.apply(lambda x: int(x.astype(float).sum())).to_dict()}


def zser(tabla):
    return json.load(gzip.open(V16 / f"original/ine_turismo/ine_tabla_{tabla}_2026-10-17.json.gz"))


def isel(nombre):
    return any(k.lower() in nombre.lower() for k in SELL)


def tramo(s):
    return {(pd.to_datetime(q["Fecha"], unit="ms") + pd.Timedelta(hours=12)).strftime("%Y-%m"): q["Valor"] for q in s["Data"] if q.get("Valor") is not None}


cols12 = [str(p) for p in pd.period_range("2025-09", "2026-08", freq="M")]


def duplicada(n):
    """versiones solapadas de una misma zona: nombre con año, entre paréntesis o 'Conurbacion'"""
    return any(k in n for k in ("2015", "2016", "2026", "(", "Conurbacion"))


zon, excl = {}, 0
for s in zser(2039):
    n = s["Nombre"]
    if not n.startswith("Nacional. Pernoctaciones."):
        continue
    if isel(n):
        excl += 1
        continue
    v = tramo(s)
    if all(cc in v for cc in cols12):
        zon[n] = sum(v[cc] for cc in cols12)


def nac12(variables):
    x = d[d.variable.isin(variables) & (d.nivel == "nacional")]
    return x[x.periodo.isin(cols12)].valor.sum()


nac_eoh = nac12(["ine_eoh_pernoctaciones_total_categorias_residentes_en_espana", "ine_eoh_pernoctaciones_total_categorias_residentes_en_el_extranjero"])
nac_eoap = nac12(["ine_eoap_pernoctaciones_residentes_en_espana", "ine_eoap_pernoctaciones_residentes_en_el_extranjero"])
zsum = sum(zon.values())
zsum_d = sum(v for n, v in zon.items() if not duplicada(n))
zs = {"tabla2039_pernoctaciones_12m_2025-09_2026-08": {"series_zona_incluidas": len(zon), "series_excluidas_por_muestra_sellada": excl, "suma_zonas_bruta": r(zsum, 0),
                                                       "suma_zonas_sin_versiones_solapadas": r(zsum_d, 0), "nacional_EOH_total_categorias": r(nac_eoh, 0), "nacional_EOAP": r(nac_eoap, 0),
                                                       "cuota_bruta_sobre_EOH": r(zsum / nac_eoh), "cuota_sin_solapes_sobre_EOH": r(zsum_d / nac_eoh),
                                                       "nota": "la tabla 2039 no declara operación; se compara con EOH (la suma bruta contiene versiones solapadas de la misma zona)"}}
pzn = {}
for s in zser(2022):
    n = s["Nombre"]
    if n.startswith("Nacional. Número de plazas estimadas.") and not isel(n):
        v = tramo(s)
        if "2026-08" in v:
            pzn[n] = v["2026-08"]
pn_ = d[(d.variable == "ine_eoap_numero_de_plazas_estimadas") & (d.nivel == "provincia") & (d.periodo == "2026-08")].valor.sum()
zs["tabla2022_plazas_apartamentos_2026-08"] = {"series_zona": len(pzn), "suma_zonas": r(sum(pzn.values()), 0), "suma_zonas_sin_solapes": r(sum(v for n, v in pzn.items() if not duplicada(n)), 0),
                                              "suma_provincias_EOAP_no_selladas": r(pn_, 0)}
oz = {}
for s in zser(48432):
    n = s["Nombre"]
    if n.startswith("Pernoctaciones. Total.") and not isel(n):
        oz[n] = {q["Anyo"]: q["Valor"] for q in s["Data"] if q.get("Valor") is not None}
anios = sorted({a for v in oz.values() for a in v})
oatn = d[(d.variable == "ine_oat_pernoctaciones_total") & (d.nivel == "nacional") & (d.frecuencia == "A")]
zs["tabla48432_OAT_zonas"] = {"series": len(oz), "suma_zonas_por_anio": {str(a): r(sum(v.get(a, 0) for v in oz.values()), 0) for a in anios},
                              "OAT_nacional_anual": {p_: r(v, 0) for p_, v in oatn.set_index("periodo").valor.items()}}
D["4_peso_zonas_descartadas"] = zs
amb = cr[(cr.fuente == "ine_tempus:ine_vte") & (cr.estado == "ambigua_municipio")]
D["4_vte_ambiguas"] = {"series": int(amb.n.astype(float).sum()), "ejemplos": amb.nombre_fuente.head(6).tolist()}

# ======================= salida =======================
SALIDA.mkdir(parents=True, exist_ok=True)
INF = Path(__file__).with_name("alquiler_turismo_informe.py")
res = base_resultado(
    "v16/auditoria/alquiler_turismo",
    "Calidad de la familia alquiler_turismo: coherencia temporal de Inside Airbnb, contraste con registros VUT e INE (VTE, EOAP, OAT), rupturas, atípicos y peso de lo descartado",
    "data/processed/v16/alquiler_turismo.parquet (muestra_sellada_v6 == False); terceros solo como recuentos propios; crudos data/raw/v16, v9 (gva_vut, cat_turisme), v11 (euskadi_vut)",
    int(len(d)),
    "Mediana y MAD (|z robusto|>5) en tasas interanuales; comparación de niveles (Pearson, Spearman, log), razón media y variaciones entre fuentes; recuento de duplicados y solapes; sin estimación de parámetros",
    D,
    ["Auditoría descriptiva C4; sin estimación de parámetros", f"{N_FILAS_CCAA_SELLADAS_FILTRO_FALSE} filas de nivel ccaa de regiones enteramente selladas llevan muestra_sellada_v6 == False y se excluyen de los cálculos", "Madrid, Mallorca, Menorca, Canarias, Asturias, Navarra, etc. están en la muestra sellada v6 y no se auditan",
     "Registros VUT con sesgo de supervivencia (OpenRTA, REATE sin bajas)", "Inside Airbnb cubre el área de captura, no el municipio completo"])
if INF.exists():
    spec = importlib.util.spec_from_file_location("inf", INF)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    escribe("alquiler_turismo", res, mod.informe(D))
else:
    escribe("alquiler_turismo", res, "# pendiente\n")
print("ok")
