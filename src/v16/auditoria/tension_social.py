"""Auditoría V16 fase 1: familia tension_social (C4, descriptivo, sin efectos). SEED=20261010.
Lee data/processed/v16 y data/base (siempre muestra_sellada_v6 == False) y escribe en output/v16/auditoria/tension_social/."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.auditoria._comun import RAIZ, SEED, base_resultado, escribe, zrob  # noqa: E402

np.random.seed(SEED)
P = RAIZ / "data/processed/v16"
D = {}

# ---------- A. CGPJ: partido judicial frente a provincia (lanzamientos totales)
t = pd.read_parquet(P / "tension_social_terceros.parquet")
t = t[~t.muestra_sellada_v6].copy()
t["prov"] = t.territorio_codigo.str.extract(r"^PJ-(\d\d)-")[0].fillna(t.territorio_codigo)
V = "cgpj_lanzamientos_total_numero"
pv = t[(t.variable == V) & (t.nivel == "provincia")].assign(y=lambda d: d.periodo.str[:4]).groupby(["territorio_codigo", "y"]).valor.sum().unstack()
pj = t[(t.variable == V) & (t.nivel == "partido_judicial")].groupby(["prov", "periodo"]).valor.sum().unstack()
ix = pj.index.intersection(pv.index)
rat = (pj.loc[ix] / pv.loc[ix, pj.columns]).round(3)
D["A_n_provincias_no_selladas_con_ambas_series"] = len(ix)
D["A_desviacion_mediana_abs_por_anyo"] = (rat - 1).abs().median().round(4).to_dict()
D["A_provincias_desv_gt10pct_por_anyo"] = {c: int(((rat[c] - 1).abs() > .10).sum()) for c in rat.columns}
D["A_2025_provincias_desv_gt10pct"] = rat.index[(rat["2025"] - 1).abs() > .10].tolist()
# Ribadavia (PJ-32-2): desglose de la celda y efecto
rb = t[(t.territorio_codigo == "PJ-32-2") & (t.periodo.isin(["2024", "2025"]))].pivot_table(index="variable", columns="periodo", values="valor")
D["A_PJ-32-2_2024_2025"] = rb.to_dict()
suma32 = float(pj.loc["32", "2025"]); r32 = float(pj.loc["32", "2025"] - rb.loc[V, "2025"] + rb.loc[V, "2024"]) if "32" in pj.index else None
D["A_32_suma_PJ_2025"] = suma32
D["A_32_serie_provincial_2025"] = float(pv.loc["32", "2025"])
D["A_32_suma_sin_PJ-32-2"] = suma32 - float(rb.loc[V, "2025"])
# nacional sin el valor anómalo
D["A_total_PJ_2025_ix"] = float(pj.loc[ix, "2025"].sum())
D["A_total_PJ_2025_sin_PJ-32-2"] = float(pj.loc[ix, "2025"].sum() - rb.loc[V, "2025"])
D["A_total_provincial_2025_ix"] = float(pv.loc[ix, "2025"].sum())
# robustez: ¿desplazamiento de filas? correlación 2024-2025 entre partidos con desfases
w = t[(t.variable == V) & (t.nivel == "partido_judicial") & t.periodo.isin(["2024", "2025"])].pivot_table(index="territorio_codigo", columns="periodo", values="valor").drop("PJ-32-2", errors="ignore")
w = w.sort_index()
a, b = w["2024"].to_numpy(), w["2025"].to_numpy()
D["A_corr_2024_2025_sin_PJ-32-2"] = round(float(np.corrcoef(a, b)[0, 1]), 3)
D["A_corr_desfasada_k=1,2,3"] = {k: round(float(np.corrcoef(a[:-k], b[k:])[0, 1]), 3) for k in (1, 2, 3)}
# atípicos robustos del salto 2025/2024 por partido
lg = np.log((w["2025"] + 1) / (w["2024"] + 1))
z = zrob(lg)
D["A_partidos_|z|>5_salto_2025_vs_2024"] = {k: int(v) for k, v in w["2025"][z.abs() > 5].items()}
# dispersión de crecimientos 2019-2025: provincia frente a suma de partidos (2025 sin PJ-32-2)
disp = {}
for y in range(2019, 2026):
    g1 = np.log(pv.loc[ix, str(y)] / pv.loc[ix, str(y - 1)])
    s = pj.loc[ix].copy()
    if y == 2025:
        s.loc["32", "2025"] -= rb.loc[V, "2025"]
    g2 = np.log(s[str(y)] / s[str(y - 1)])
    disp[y] = {"sd_prov": round(float(g1.replace([np.inf, -np.inf], np.nan).std()), 3), "sd_partidos": round(float(g2.replace([np.inf, -np.inf], np.nan).std()), 3)}
D["A_sd_crecimiento_log"] = disp
# otras provincias con desviaciones persistentes antes de 2025 (causa: partidos descartados / Ceuta-Melilla)
D["A_prov_con_desv_>3%_en_2013-2024_en_mas_de_6_anyos"] = rat.index[((rat.loc[:, "2013":"2024"] - 1).abs() > .03).sum(axis=1) > 6].tolist()
D["A_celdas_prov-anyo_2013-2024_con_desv_>10%"] = [f"{i}:{c}={rat.loc[i, c]}" for i in rat.index for c in rat.columns[:-1] if abs(rat.loc[i, c] - 1) > .10]
# desglose coherencia hipotecaria + LAU + otros = total en partidos
c = t[(t.nivel == "partido_judicial")].pivot_table(index=["territorio_codigo", "periodo"], columns="variable", values="valor")
c["dif"] = c.cgpj_lanzamientos_total_numero - c[["cgpj_lanzamientos_hipotecaria_numero", "cgpj_lanzamientos_lau_numero", "cgpj_lanzamientos_otros_numero"]].sum(axis=1)
D["A_partido-anyo_con_total_distinto_de_suma_de_causas"] = int((c.dif.abs() > 0).sum())
D["A_filas_partido_anyo"] = int(len(c))

# ---------- B. Padrón municipal 1996-2025 (cifras oficiales)
s = pd.read_parquet(P / "tension_social.parquet")
s = s[~s.muestra_sellada_v6]
pad = s[(s.variable == "ine_padron_poblacion_personas") & (s.nivel == "municipio")]
tot = pad[pad.desagregacion == "sexo=total"].assign(y=lambda d: d.periodo.astype(int)).pivot_table(index="territorio_codigo", columns="y", values="valor")
hm = pad[pad.desagregacion != "sexo=total"].assign(y=lambda d: d.periodo.astype(int)).groupby(["territorio_codigo", "y"]).valor.sum().unstack()
D["B_anyos_padron"] = sorted(int(c) for c in tot.columns)
D["B_anyos_ausentes_1996-2025"] = [y for y in range(1996, 2026) if y not in tot.columns]
D["B_municipios_no_sellados"] = int(len(tot))
D["B_municipios_por_anyo_min_max"] = [int(tot.count().min()), int(tot.count().max())]
dif = (tot - hm.reindex_like(tot)).abs()
D["B_total_distinto_de_hombres+mujeres_celdas"] = int((dif > 0).sum().sum())
D["B_municipios_con_huecos_en_su_rango"] = int(sum(1 for _, r in tot.iterrows() if r.notna().sum() < (r.last_valid_index() - r.first_valid_index() + 1 - sum(1 for y in range(r.first_valid_index(), r.last_valid_index() + 1) if y not in tot.columns))))
D["B_municipios_sin_dato_2025"] = int(tot[2025].isna().sum())
D["B_valores_<=0"] = int((tot <= 0).sum().sum())
lg = np.log(tot).diff(axis=1)
# solo años consecutivos (se salta 1997)
cols = [c for c in tot.columns if c - 1 in tot.columns]
zz = {}
for cy in cols:
    zz[cy] = zrob(lg[cy].dropna())
at = []
for cy, zs in zz.items():
    big = zs[(zs.abs() > 5) & (tot.loc[zs.index, cy - 1] >= 5000)]
    for m, v in big.items():
        at.append((m, int(cy), round(float(v), 1), int(tot.loc[m, cy - 1]), int(tot.loc[m, cy])))
D["B_atipicos_|z|>5_municipios_>=5000hab_n"] = len(at)
D["B_atipicos_top10_por_|z|"] = sorted(at, key=lambda x: -abs(x[2]))[:10]
D["B_atipicos_por_anyo"] = pd.Series([a[1] for a in at]).value_counts().sort_index().to_dict()
D["B_atipicos_todos_tamanos_n"] = int(sum(int((z.abs() > 5).sum()) for z in zz.values()))
# suma nacional por año (no sellados) y comparación provincial con data/base (padrón por nacionalidad, total)
h = pd.read_parquet(RAIZ / "data/base/hechos.parquet", filters=[("variable", "=", "padron_pob_nacionalidad"), ("desagregacion", "=", "nacionalidad=Total")])
h = h[(~h.muestra_sellada_v6) & (h.nivel == "provincia")]
hb = h.assign(y=h.periodo.astype(int)).pivot_table(index="territorio_codigo", columns="y", values="valor")
prov_v16 = tot.groupby(tot.index.str[:2]).sum(min_count=1)
ix2 = prov_v16.index.intersection(hb.index)
yy = [y for y in hb.columns if y in prov_v16.columns]
r2 = (prov_v16.loc[ix2, yy] / hb.loc[ix2, yy] - 1)
D["B_comparacion_base_provincial"] = {"n_prov": len(ix2), "anyos": [int(min(yy)), int(max(yy))], "desv_rel_mediana_abs": round(float(r2.abs().stack().median()), 5),
                                      "desv_rel_max_abs": round(float(r2.abs().stack().max()), 5), "celdas_>0.5%": int((r2.abs() > .005).sum().sum()),
                                      "peores": [(i, int(c), round(float(r2.loc[i, c]), 4)) for i, c in r2.abs().stack().sort_values(ascending=False).head(5).index]}
# comparación municipal con data/raw/v9
f9 = RAIZ / "data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz"
try:
    r9 = pd.read_csv(f9, nrows=3)
    D["B_v9_columnas"] = r9.columns.tolist()
except Exception as e:  # noqa: BLE001
    D["B_v9_error"] = str(e)

# ---------- C. EMCR (2021-2024) frente a EVR (hasta 2021): solape 2021, inmigración y emigración exterior municipal
em = s[(s.variable == "ine_emcr_inmigraciones_exterior_personas") & (s.desagregacion == "sexo=ambos_sexos") & (s.nivel == "municipio") & (s.periodo == "2021")].set_index("territorio_codigo").valor
emg = s[(s.variable == "ine_emcr_emigraciones_exterior_personas") & (s.desagregacion == "sexo=ambos_sexos") & (s.nivel == "municipio") & (s.periodo == "2021")].set_index("territorio_codigo").valor
hh = pd.read_parquet(RAIZ / "data/base/hechos.parquet", filters=[("variable", "in", ["evr_inmigracion_exterior", "evr_emigracion_exterior", "emcr_md_inmigracion_exterior", "emcr_md_emigracion_exterior"]), ("periodo", "=", "2021")])
hh = hh[~hh.muestra_sellada_v6]
ev_i = hh[hh.variable == "evr_inmigracion_exterior"].groupby("territorio_codigo").valor.sum()
ev_e = hh[hh.variable == "evr_emigracion_exterior"].groupby("territorio_codigo").valor.sum()
md_i = hh[hh.variable == "emcr_md_inmigracion_exterior"].groupby("territorio_codigo").valor.sum()
C = {}
for nom, a_, b_ in [("inmig_EMCR_vs_EVR", em, ev_i), ("emig_EMCR_vs_EVR", emg, ev_e), ("inmig_EMCR_vs_EMCR-microdatos(base)", em, md_i)]:
    j = pd.concat([a_.rename("a"), b_.rename("b")], axis=1, join="inner")
    rel = (j.a - j.b) / j.b.replace(0, np.nan)
    C[nom] = {"n_municipios": int(len(j)), "suma_a": float(j.a.sum()), "suma_b": float(j.b.sum()), "ratio_sumas": round(float(j.a.sum() / j.b.sum()), 4),
              "corr_niveles": round(float(np.corrcoef(j.a, j.b)[0, 1]), 4), "exactos_%": round(float((j.a == j.b).mean() * 100), 1),
              "desv_rel_mediana": round(float(rel.median()), 4), "desv_rel_p5_p95": [round(float(x), 3) for x in rel.quantile([.05, .95])]}
D["C_solape_2021"] = C
D["C_municipios_EMCR_2021_vs_EVR"] = [int(len(em)), int(len(ev_i))]
# Serie temporal nacional EMCR (suma de municipios no sellados) y EVR 2015-2021 para ver la ruptura
evs = pd.read_parquet(RAIZ / "data/base/hechos.parquet", filters=[("variable", "=", "evr_inmigracion_exterior"), ("nivel", "=", "municipio")])
evs = evs[~evs.muestra_sellada_v6].groupby("periodo").valor.sum()
D["C_EVR_inmig_exterior_suma_municipios_2017-2021"] = {k: float(v) for k, v in evs.loc["2017":"2021"].items()}
ems = s[(s.variable == "ine_emcr_inmigraciones_exterior_personas") & (s.desagregacion == "sexo=ambos_sexos") & (s.nivel == "municipio")].groupby("periodo").valor.sum()
D["C_EMCR_inmig_exterior_suma_municipios_2021-2024"] = {k: float(v) for k, v in ems.items()}
# cobertura EVR: municipios con dato 2021 frente a EMCR
D["C_EVR_solo_municipios_>=10000hab_segun_metodo_dato"] = True

# ---------- A2. Triangulación con el total por TSJ/CCAA (CCAA con todas sus provincias fuera de la muestra sellada)
TER = RAIZ / "data/raw/v16/tension_social/_terceros/"
ta = pd.read_excel(TER / "cgpj_datos_crisis_anual2025.xlsx", sheet_name="Lanzamientos practic. total TSJ", header=None).iloc[6:24, [1, 2, 3]]
ta.columns = ["n", "a24", "a25"]
ta = ta.set_index("n")
ty = pd.read_excel(TER / "cgpj_series_tsj_2T2026.xlsx", sheet_name="Lanzamientos practic. total TSJ", header=None)
hdr = ty.iloc[6].tolist()
ts_ = ty.iloc[7:24].set_index(1)
c25 = [i for i, h in enumerate(hdr) if isinstance(h, str) and h.startswith("25-T")]
CC = {"ANDALUCÍA": "04 11 14 18 21 23 29 41", "CASTILLA - LA MANCHA": "02 13 16 19 45", "CASTILLA Y LEÓN": "05 09 24 34 37 40 42 47 49",
      "CATALUÑA": "08 17 25 43", "COMUNITAT VALENCIANA": "03 12 46", "EXTREMADURA": "06 10", "GALICIA": "15 27 32 36", "PAÍS VASCO": "01 20 48", "CANTABRIA": "39"}
pv25 = t[(t.variable == V) & (t.nivel == "provincia") & t.periodo.str.startswith("2025")].groupby("territorio_codigo").valor.sum()
pj25 = pj["2025"].copy()
pj25["32"] -= float(rb.loc[V, "2025"])
tri = {}
for k, v in CC.items():
    ps = v.split()
    tri[k] = {"TSJ_anual_2025": float(ta.loc[k, "a25"]), "TSJ_serie_2T2026_2025": float(ts_.loc[k, c25].astype(float).sum()),
              "suma_provincias_serie": float(pv25.reindex(ps).sum()), "suma_partidos_2025_sin_PJ-32-2": float(pj25.reindex(ps).sum())}
    tri[k]["desv_partidos_%"] = round(100 * (tri[k]["suma_partidos_2025_sin_PJ-32-2"] / tri[k]["TSJ_anual_2025"] - 1), 1)
D["A2_triangulacion_CCAA_2025"] = tri
D["A2_TSJ_total_nacional_2025"] = float(ta.loc["TOTAL", "a25"])
D["A2_TSJ_total_nacional_2024"] = float(ta.loc["TOTAL", "a24"])
allpj = pd.read_parquet(P / "tension_social_terceros.parquet")
D["A2_suma_nacional_partidos_2024_y_2025_todas_las_provincias"] = {y: float(allpj[(allpj.variable == V) & (allpj.nivel == "partido_judicial") & (allpj.periodo == y)].valor.sum()) for y in ("2024", "2025")}

res = base_resultado("v16/auditoria/tension_social", "¿Son coherentes entre sí y con la base las series de tensión social (CGPJ, padrón, EMCR)?",
                     "data/processed/v16/tension_social*.parquet; data/base/hechos.parquet (muestra_sellada_v6=False); data/raw/v16/tension_social/_terceros (solo lectura)",
                     int(len(t) + len(s)), "mediana/MAD (|z|>5), cocientes de agregación, comparación de niveles entre fuentes; sin estimación de efectos", D,
                     ["Solo agregados propios del CGPJ; los datos de terceros no se reproducen.", "Excluye las 11 provincias de la muestra sellada (muestra_sellada_v6)."])
INF = (Path(__file__).resolve().parents[3] / "output/v16/auditoria/tension_social/informe.md")
if __name__ == "__main__":
    informe = INF.read_text(encoding="utf-8") if INF.exists() else "(informe pendiente)"
    escribe("tension_social", res, informe)
    import json
    print(json.dumps(D, ensure_ascii=False, indent=1, default=str)[:9000])
