"""Auditoría V16 fase 1: demanda_internacional (C4, descriptivo). SEED=20261010."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.auditoria._comun import RAIZ, SEED, base_resultado, escribe, zrob  # noqa: E402

np.random.seed(SEED)
R = RAIZ / "data/raw"
d = pd.read_parquet(RAIZ / "data/processed/v16/demanda_internacional.parquet")
d = d[~d.muestra_sellada_v6]
tr = pd.read_parquet(RAIZ / "data/processed/v16/demanda_internacional_terceros.parquet")
D = {}


def ser(var, fre="M"):
    x = d[(d.variable == var) & (d.frecuencia == fre)]
    return x.set_index("periodo").valor.astype(float).sort_index()


def ventanas_signo_opuesto(a, b, minlen=3):
    """Ventanas consecutivas en que las tasas interanuales (o variaciones) tienen signo opuesto."""
    j = pd.concat([a, b], axis=1).dropna()
    op = (np.sign(j.iloc[:, 0]) * np.sign(j.iloc[:, 1]) < 0)
    out, ini = [], None
    for i, (k, v) in enumerate(op.items()):
        if v and ini is None:
            ini = k
        if (not v or i == len(op) - 1) and ini is not None:
            fin = k if v else op.index[i - 1]
            n = list(op.index).index(fin) - list(op.index).index(ini) + 1
            if n >= minlen:
                out.append((str(ini), str(fin), n))
            ini = None
    return out


def compara(a, b, nom, lag=12, es_tasa=False):
    """Compara dos series con el mismo índice temporal: nivel, diferencia de variación a lag, correlación, signo opuesto."""
    j = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    ya = j.a - j.a.shift(lag) if es_tasa else 100 * (j.a / j.a.shift(lag) - 1)
    yb = j.b - j.b.shift(lag) if es_tasa else 100 * (j.b / j.b.shift(lag) - 1)
    y = pd.concat([ya, yb], axis=1).dropna()
    return {"n": int(len(j)), "periodo": [str(j.index[0]), str(j.index[-1])],
            "dif_nivel_media": round(float((j.a - j.b).mean()), 4), "dif_nivel_max_abs": round(float((j.a - j.b).abs().max()), 4),
            "corr_niveles": round(float(j.a.corr(j.b)), 4),
            "corr_variacion": round(float(y.iloc[:, 0].corr(y.iloc[:, 1])), 4), "dif_variacion_media": round(float((y.iloc[:, 0] - y.iloc[:, 1]).mean()), 3),
            "dif_variacion_mad": round(float((y.iloc[:, 0] - y.iloc[:, 1]).abs().median()), 3),
            "ventanas_signo_opuesto_>=3": ventanas_signo_opuesto(y.iloc[:, 0], y.iloc[:, 1])}


# ---------- 1. BdE por periodo de fijación y coherencia con las series ya en el repositorio
b03 = ser("bde_tedr_vivienda_total_be1903")
b04 = ser("bde_tedr_vivienda_total_be1904")
D["1_be1903_vs_be1904_total"] = compara(b03, b04, "be1903/be1904", es_tasa=True)
D["1_be1903_vs_be1904_total"]["max_abs_dif"] = round(float((b03 - b04).abs().max()), 6)
raw = pd.read_csv(R / "bde_tipos_hipotecas_nuevas.csv")
rt = raw[raw.serie == "DN_1TI2T0135"].set_index("periodo").valor.astype(float)
ra = raw[raw.serie == "DN_1TI2T0082"].set_index("periodo").valor.astype(float)
ec = pd.read_csv(R / "ecb_tipo_hipotecario_es.csv").set_index("periodo").valor.astype(float)
D["1_TEDR_v16_be1903_vs_raw_bde_tipos_DN_1TI2T0135"] = {"max_abs_dif": round(float((b03 - rt).abs().max()), 6), "n_comunes": int(pd.concat([b03, rt], axis=1).dropna().shape[0])}
D["1_TEDR_BdE_vs_BCE_MIR_AAR_ES"] = compara(rt, ec, "TEDR vs MIR", es_tasa=True)
D["1_TAE_BdE_vs_BCE_MIR_AAR_ES"] = compara(ra, ec, "TAE vs MIR", es_tasa=True)
# BdE TEDR hasta 1 año... mas de 10 años: ponderación por importes frente al total
cub = ["hasta_1a", "1a_5a", "5a_10a", "mas_10a"]
T = pd.concat({c: ser(f"bde_tedr_vivienda_fij_{c}") for c in cub}, axis=1)
I = pd.concat({c: ser(f"bde_importe_vivienda_fij_{c}") for c in cub}, axis=1)
It = ser("bde_importe_vivienda_total_be1911")
It2 = ser("bde_importe_vivienda_total_be1912")
D["1_importes_suma_tramos_vs_total_be1911"] = {"ratio_mediana": round(float((I.sum(axis=1) / It).median()), 4), "ratio_min_max": [round(float((I.sum(axis=1) / It).min()), 4), round(float((I.sum(axis=1) / It).max()), 4)],
                                                "be1911_vs_be1912_max_abs_dif": round(float((It - It2).abs().max()), 4), "be1911_vs_be1912_ratio_mediana": round(float((It / It2).median()), 4)}
pond = (T * I).sum(axis=1, min_count=4) / I.sum(axis=1, min_count=4)
cmp_ = pd.concat([pond.rename("pond"), b03.rename("tot")], axis=1).dropna()
D["1_TEDR_total_vs_media_ponderada_de_tramos"] = {"n": int(len(cmp_)), "dif_media_pp": round(float((cmp_.pond - cmp_.tot).mean()), 3), "dif_max_abs_pp": round(float((cmp_.pond - cmp_.tot).abs().max()), 3),
                                                  "meses_|dif|>0.25pp": [str(k) for k in cmp_.index[(cmp_.pond - cmp_.tot).abs() > .25]][:15]}
# dispersión de los tramos: ¿tramos sin dato (NaN) o muestras pequeñas?
D["1_NaN_por_tramo_TEDR"] = {c: int(T[c].isna().sum()) for c in cub}
D["1_cuota_importe_hasta_1a_mediana_por_tramo_de_anyos"] = {str(y): round(float((lambda q: q[q.index.str.startswith(str(y))].median())(I["hasta_1a"] / I.sum(axis=1))), 3) for y in (2003, 2008, 2012, 2016, 2019, 2022, 2024, 2025)}
# atípicos robustos (variación mensual) por serie
at = {}
for nm, s in list(T.items()) + [("total", b03), ("MIR_ECB", ec), ("TAE_BdE", ra)]:
    z = zrob(s.diff().dropna())
    k = z[z.abs() > 5]
    at[nm] = {"n": int(len(k)), "ejemplos": [(str(i), round(float(v), 1)) for i, v in k.abs().sort_values(ascending=False).head(4).items()]}
D["1_atipicos_|z|>5_variacion_mensual"] = at
# ruptura de base: el be1903 y el be1904 incluyen o no renegociaciones desde 2015-01 (series excl. reneg. empiezan 2014-12/2015-01)
ex = ser("bde_tedr_vivienda_excl_renegociaciones")
D["1_total_vs_excl_renegociaciones"] = compara(b03, ex, "total vs excl. reneg.", es_tasa=True)
# último dato y huecos
for nm, s in [("be1903", b03), ("ECB_MIR", ec)]:
    idx = pd.period_range(s.index[0], s.index[-1], freq="M").astype(str)
    D[f"1_huecos_{nm}"] = [m for m in idx if m not in s.index]

# ---------- 2. OCDE frente a Eurostat HPI y BIS (España)
oe = d[(d.variable == "oecd_hpi") & (d.territorio_codigo == "ES")].set_index("periodo").valor.astype(float).sort_index()
oe.index = [p.replace("T", "-Q") for p in oe.index]
rr = pd.read_csv(R / "eurostat_hpi.csv")
eu = {k: rr[(rr.purchase == k) & (rr.unit == "I15_Q")].set_index("periodo").valor.astype(float).sort_index() for k in ("TOTAL", "DW_EXST", "DW_NEW")}
bis = pd.read_csv(R / "bis_rpp.csv")
bis = bis[(bis.territorio == "ES") & (bis.precio == "nominal") & (bis.unidad == "Índice 2010 = 100")].set_index("periodo").valor.astype(float).sort_index()
bisr = pd.read_csv(R / "bis_rpp.csv")
bisr = bisr[(bisr.territorio == "ES") & (bisr.precio == "nominal") & (bisr.unidad.str.contains("Variación"))].set_index("periodo").valor.astype(float).sort_index()
# tasas interanuales con lag 4
C2 = {}
for nm, o in [("Eurostat_TOTAL", eu["TOTAL"]), ("Eurostat_DW_EXST", eu["DW_EXST"]), ("Eurostat_DW_NEW", eu["DW_NEW"]), ("BIS_nominal", bis)]:
    # compara tasas interanuales de OCDE y la otra, ignorando el nivel (base distinta)
    j = pd.concat([oe.rename("a"), o.rename("b")], axis=1).dropna()
    ya = 100 * (j.a / j.a.shift(4) - 1)
    yb = 100 * (j.b / j.b.shift(4) - 1)
    y = pd.concat([ya, yb], axis=1).dropna()
    dif = y.iloc[:, 0] - y.iloc[:, 1]
    C2[nm] = {"n": int(len(y)), "periodo": [y.index[0], y.index[-1]], "corr_tasas": round(float(y.iloc[:, 0].corr(y.iloc[:, 1])), 4),
              "dif_media_pp": round(float(dif.mean()), 3), "dif_abs_mediana_pp": round(float(dif.abs().median()), 3), "dif_max_abs_pp": round(float(dif.abs().max()), 2),
              "trimestre_max_dif": str(dif.abs().idxmax()),
              "ventanas_signo_opuesto_>=2": ventanas_signo_opuesto(y.iloc[:, 0], y.iloc[:, 1], 2),
              "trimestres_|dif|>3pp": int((dif.abs() > 3).sum())}
D["2_OCDE_HPI_ES_vs_otras_tasas_interanuales"] = C2
# nivel: razón OCDE / Eurostat (ambos 2015=100) debería ser ~1 en 2015
D["2_OCDE_nivel_2015_media_vs_Eurostat_TOTAL_2015"] = [round(float(oe[[p for p in oe.index if p.startswith("2015")]].mean()), 2), round(float(eu["TOTAL"][[p for p in eu["TOTAL"].index if p.startswith("2015")]].mean()), 2)]
# Eurostat: tasa interanual publicada (RCH_A) frente a la recalculada del índice
ch = rr[(rr.purchase == "TOTAL") & (rr.unit == "RCH_A")].set_index("periodo").valor.astype(float).sort_index()
yy = (100 * (eu["TOTAL"] / eu["TOTAL"].shift(4) - 1)).dropna()
jj = pd.concat([ch.rename("pub"), yy.rename("calc")], axis=1).dropna()
D["2_Eurostat_RCH_A_publicada_vs_recalculada"] = {"n": int(len(jj)), "max_abs_dif_pp": round(float((jj.pub - jj.calc).abs().max()), 3)}
# BIS: variación publicada vs recalculada
bb = pd.read_csv(R / "bis_rpp.csv"); bn = bb[(bb.territorio == "ES") & (bb.precio == "nominal") & (bb.unidad == "Índice 2010 = 100")].set_index("periodo").valor.sort_index()
cal = (100 * (bn / bn.shift(4) - 1)).dropna(); jb = pd.concat([bisr.rename("pub"), cal.rename("calc")], axis=1).dropna()
D["2_BIS_variacion_publicada_vs_recalculada"] = {"n": int(len(jb)), "max_abs_dif_pp": round(float((jb.pub - jb.calc).abs().max()), 3)}
D["2_ultimo_periodo"] = {"OCDE": oe.index[-1], "Eurostat": eu["TOTAL"].index[-1], "BIS": bis.index[-1]}
# atípicos en OCDE HPI ES
z = zrob(oe.pct_change().dropna())
D["2_OCDE_HPI_ES_atipicos_|z|>5_variacion_trimestral"] = [(i, round(float(v), 1)) for i, v in z[z.abs() > 5].items()]
# OCDE: ¿coincide la nueva descarga con el fichero antiguo (27 países)? ES, periodos comunes
old = pd.read_csv(R / "oecd_house_prices.csv"); old = old[(old.territorio == "ESP") & (old.frecuencia == "Q") & (old.medida == "HPI")]
D["2_oecd_antiguo_ES_HPI_filas"] = int(len(old))
if len(old):
    o2 = old.set_index("periodo").valor.astype(float)
    o2.index = [str(p).replace("Q", "Q") for p in o2.index]
    k = o2.index.intersection(oe.index)
    D["2_OCDE_nuevo_vs_antiguo_ES_HPI"] = {"n_comunes": int(len(k)), "max_abs_dif": round(float((o2[k] - oe[k]).abs().max()), 4) if len(k) else None, "ejemplo_idx": list(o2.index[:2])}

# ---------- 3. Choques JK: mensuales frente a diarios agregados
jd = pd.read_csv(RAIZ / "data/raw/v16/demanda_internacional/bce_sorpresas/jk_shocks_ecb_mpd_me_d.csv")
jm = pd.read_csv(RAIZ / "data/raw/v16/demanda_internacional/bce_sorpresas/jk_shocks_ecb_mpd_me_m.csv")
D["3_columnas_diario"] = jd.columns.tolist()
D["3_columnas_mensual"] = jm.columns.tolist()
dcol = jd.columns[0]
jd["mes"] = pd.to_datetime(jd[dcol]).dt.to_period("M").astype(str)
jm["mes"] = jm.year.astype(int).astype(str) + "-" + jm.month.astype(int).astype(str).str.zfill(2)
jm = jm.rename(columns={"pc1_hf": "pc1", "STOXX50_hf": "STOXX50"})
vars_ = [c for c in ["pc1", "STOXX50", "MP_pm", "CBI_pm", "MP_median", "CBI_median"] if c in jd.columns and c in jm.columns]
res3 = {}
for v in vars_:
    s = jd.groupby("mes")[v].sum()
    m = jm.set_index("mes")[v]
    j = pd.concat([s.rename("suma_diarios"), m.rename("mensual")], axis=1).fillna({"suma_diarios": 0}).dropna(subset=["mensual"])
    dif = (j.suma_diarios - j.mensual)
    res3[v] = {"n_meses": int(len(j)), "corr": round(float(j.suma_diarios.corr(j.mensual)), 5), "max_abs_dif": round(float(dif.abs().max()), 6),
               "meses_|dif|>1e-6": int((dif.abs() > 1e-6).sum()), "ratio_pendiente": round(float(np.polyfit(j.suma_diarios, j.mensual, 1)[0]), 4)}
    # media por reunión alternativa si hay varias reuniones en el mes
    mm = jd.groupby("mes")[v].mean()
    j2 = pd.concat([mm.rename("media_diarios"), m.rename("mensual")], axis=1).dropna()
    res3[v]["max_abs_dif_con_media"] = round(float((j2.media_diarios - j2.mensual).abs().max()), 6)
    res3[v]["meses_sin_reunion_con_mensual_distinto_de_0"] = int(((~jm.mes.isin(jd.mes)) & (jm[v].abs() > 0)).sum())
D["3_JK_mensual_vs_suma_diarios"] = res3
D["3_reuniones_por_mes_max"] = int(jd.groupby("mes").size().max())
D["3_diario_filas_NaN"] = int(jd.isna().sum().sum())
D["3_identidad_MP+CBI=pc1_max_abs"] = {a: round(float((jd[f"MP_{a}"] + jd[f"CBI_{a}"] - jd["pc1"]).abs().max()), 6) for a in ("pm", "median") if f"MP_{a}" in jd}
z = zrob(jd["pc1"])
D["3_diario_pc1_atipicos_|z|>5_n"] = int((z.abs() > 5).sum())
D["3_diario_pc1_atipicos_top5"] = [(str(jd.loc[i, dcol]), round(float(jd.loc[i, "pc1"]), 3), round(float(z[i]), 1)) for i in z.abs().sort_values(ascending=False).head(5).index]
# EA-MPD (terceros, solo agregado propio): n de fechas comunes con JK diario
ea = tr[tr.variable == "bce_eampd_ois_1y"]
D["3_EA-MPD_fechas_vs_JK_diario"] = {"fechas_EA-MPD_ois_1y": int(len(ea)), "reuniones_JK": int(len(jd)), "comunes": int(len(set(ea.periodo) & set(jd[dcol].astype(str))))}

res = base_resultado("v16/auditoria/demanda_internacional", "¿Son coherentes los tipos del BdE, los índices de precios internacionales y los choques del BCE?",
                     "data/processed/v16/demanda_internacional*.parquet; data/raw/{bde_tipos_hipotecas_nuevas,ecb_tipo_hipotecario_es,eurostat_hpi,bis_rpp,oecd_house_prices}.csv; data/raw/v16/demanda_internacional/bce_sorpresas",
                     int(len(d)), "mediana/MAD (|z|>5), correlación de tasas, diferencias medias, ventanas de signo opuesto, identidades contables", D,
                     ["EA-MPD (terceros) solo se usa para contar fechas comunes; no se reproducen valores.", "Ningún efecto estimado."])
INF = RAIZ / "output/v16/auditoria/demanda_internacional/informe.md"
if __name__ == "__main__":
    escribe("demanda_internacional", res, INF.read_text(encoding="utf-8") if INF.exists() else "(informe pendiente)")
    print(json.dumps(D, ensure_ascii=False, indent=1, default=str)[:14000])
