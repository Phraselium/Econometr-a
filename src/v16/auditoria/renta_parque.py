"""Auditoría V16 fase 1: renta_parque (ADRH, Catastro urbano 2026, inventario ECV/EPF). C4, descriptivo. SEED=20261010.
Filtra muestra_sellada_v6 == False y unidades donde holdout.unidad_sellada_v16 es True (solo booleanos)."""
import difflib
import gc
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.holdout import unidad_sellada_v16  # noqa: E402
from src.v16.auditoria._comun import RAIZ, SEED, base_resultado, escribe, zrob  # noqa: E402

np.random.seed(SEED)
D = {}
P = RAIZ / "data/processed/v16"
V_PER, V_HOG, V_GIN = "ine_adrh_renta_neta_media_persona_eur", "ine_adrh_renta_neta_media_hogar_eur", "ine_adrh_gini_indice"
PAR = {"adrh_renta_neta_persona": V_PER, "adrh_renta_neta_hogar": V_HOG, "adrh_gini": V_GIN}
COLS = ["territorio_codigo", "nivel", "periodo", "variable", "desagregacion", "valor", "unidad", "metodo_dato", "muestra_sellada_v6"]


def filtra(df):
    """Quita muestra v6 marcada y unidades fuera del entrenamiento V16/V15 (booleanos de holdout)."""
    df = df[~df.muestra_sellada_v6].copy()
    keep = pd.Series(True, index=df.index)
    for nv in ("municipio", "distrito", "seccion"):
        m = (df.nivel.astype(str) == nv).values
        if m.any():
            u = pd.Series(df.loc[m, "territorio_codigo"].astype(str).unique())
            s = dict(zip(u, unidad_sellada_v16(u, nv).values))
            keep[m] = ~df.loc[m, "territorio_codigo"].astype(str).map(s).values
    return df[keep]


def categ(df):
    for c in ("nivel", "periodo", "variable", "desagregacion", "unidad", "metodo_dato"):
        if c in df:
            df[c] = df[c].astype("category")
    return df


# ---------------------------------------------------------------- carga versionado
v = pq.read_table(P / "renta_parque.parquet", columns=COLS).to_pandas()
D["0_filas_versionado"] = int(len(v))
vf = categ(filtra(v))
del v
gc.collect()
D["0_filas_tras_filtro"] = int(len(vf))
D["0_filas_por_nivel_tras_filtro"] = {k: int(x) for k, x in vf.groupby("nivel", observed=True).size().items()}

# ---------------------------------------------------------------- 1. ADRH nuevo frente a la base (solape sección)
h = pq.read_table(RAIZ / "data/base/publica/hechos.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable", "valor", "unidad", "muestra_sellada_v6", "metodo_dato"],
                  filters=[("variable", "in", list(PAR)), ("nivel", "=", "seccion")]).to_pandas()
h = filtra(h)
D["1_base_filas_filtradas"] = int(len(h))
D["1_base_periodos"] = sorted(h.periodo.astype(str).unique())
D["1_base_metodo_dato"] = {str(k): int(x) for k, x in h.metodo_dato.value_counts().items()}
filtros = [("variable", "in", list(PAR.values())), ("nivel", "=", "seccion"), ("periodo", "in", ["2019", "2020", "2021", "2022", "2023"])]
c = pq.read_table(P / "renta_parque_adrh_completo.parquet", columns=COLS, filters=filtros).to_pandas()
c = filtra(c)
D["1_completo_seccion_2019_23_filas_filtradas"] = int(len(c))
cmp_ = {}
for vb, vn in PAR.items():
    a = h[h.variable == vb][["territorio_codigo", "periodo", "valor"]].rename(columns={"valor": "base"})
    b = c[(c.variable == vn) & (c.desagregacion.astype(str) == "")][["territorio_codigo", "periodo", "valor", "metodo_dato"]].rename(columns={"valor": "api"})
    m = a.merge(b, on=["territorio_codigo", "periodo"], how="outer", indicator=True)
    out = {"solo_base": int((m._merge == "left_only").sum()), "solo_api": int((m._merge == "right_only").sum()), "ambos": int((m._merge == "both").sum())}
    out["por_periodo"] = {p: {str(k): int(x) for k, x in g._merge.value_counts().items() if x} for p, g in m.groupby("periodo")}
    bo = m[m._merge == "both"].copy()
    bo["dif"] = bo.api - bo.base
    bo["rel"] = bo.dif / bo.base.abs().replace(0, np.nan)
    ex = bo.dif.abs() < 1e-9
    out["identicos_n"] = int(ex.sum())
    out["identicos_pct"] = round(100 * float(ex.mean()), 3)
    out["dif_abs_max"] = float(bo.dif.abs().max())
    out["dif_abs_media"] = float(bo.dif.abs().mean())
    out["dif_rel_abs_p50_p99_max"] = [float(bo.rel.abs().quantile(q)) for q in (.5, .99, 1)]
    out["dif_media_con_signo"] = float(bo.dif.mean())
    out["dif_no_nulas_n_por_periodo"] = {p: int((g.dif.abs() > 1e-9).sum()) for p, g in bo.groupby("periodo")}
    out["metodo_dato_api_en_solape"] = {str(k): int(x) for k, x in bo.metodo_dato.value_counts().items()}
    out["coincide_redondeo_0dec_pct"] = round(100 * float((bo.api.round(0) == bo.base.round(0)).mean()), 3)
    out["coincide_redondeo_2dec_pct"] = round(100 * float((bo.api.round(2) == bo.base.round(2)).mean()), 3)
    cmp_[vb] = out
D["1_comparacion_base_vs_api"] = cmp_
D["1_2021_en_base_seccion"] = bool("2021" in set(D["1_base_periodos"]))
D["1_2021_en_api_seccion_filas_renta_persona"] = int(((c.periodo.astype(str) == "2021") & (c.variable == V_PER)).sum())
del h, c
gc.collect()

# ---------------------------------------------------------------- 2. coherencia jerárquica y atípicos
vp = vf[(vf.variable == V_PER) & (vf.desagregacion.astype(str) == "")].copy()
vpop = vf[(vf.variable == "ine_adrh_poblacion_personas") & (vf.desagregacion.astype(str) == "")][["territorio_codigo", "nivel", "periodo", "valor"]].rename(columns={"valor": "pob"})
for d_ in (vp, vpop):
    for k in ("periodo", "territorio_codigo", "nivel"):
        d_[k] = d_[k].astype(str)
vp["metodo_dato"] = vp.metodo_dato.astype(str)
vp = vp.merge(vpop, on=["territorio_codigo", "nivel", "periodo"], how="left")
D["2_pob_inventario"] = {"filas_pob": int(len(vpop)), "renta_filas_sin_pob": int(vp.pob.isna().sum())}
mun = vp[vp.nivel == "municipio"].set_index(["territorio_codigo", "periodo"])
jer = {}
for nv in ("seccion", "distrito"):
    s = vp[(vp.nivel == nv) & vp.pob.notna() & (vp.pob > 0)].copy()
    s["mun"] = s.territorio_codigo.str[:5]
    tot = vpop[vpop.nivel == nv].copy()
    tot["mun"] = tot.territorio_codigo.str[:5]
    totm = tot.groupby(["mun", "periodo"]).pob.sum().rename("pob_total_nivel")
    g = s.assign(rw=s.valor * s.pob).groupby(["mun", "periodo"]).agg(rw=("rw", "sum"), w=("pob", "sum"), n=("valor", "size"))
    g["media_pond"] = g.rw / g.w
    g = g.join(totm)
    g["cobertura_pob"] = g.w / g.pob_total_nivel
    g.index = g.index.set_names(["territorio_codigo", "periodo"])
    j = g.join(mun[["valor", "metodo_dato", "pob"]].rename(columns={"valor": "valor_mun", "pob": "pob_mun"}), how="inner")
    j["rel"] = (j.media_pond - j.valor_mun) / j.valor_mun
    r = {"pares_municipio_anio": int(len(j))}
    for lab, jj in (("todos", j), ("cobertura>=0.95", j[j.cobertura_pob >= .95]), ("cobertura>=0.95_y_municipio_observado", j[(j.cobertura_pob >= .95) & (j.metodo_dato == "observado")])):
        rr = jj.rel
        r[lab] = {"n": int(len(jj)), "rel_abs_p50": float(rr.abs().quantile(.5)) if len(jj) else None, "rel_abs_p95": float(rr.abs().quantile(.95)) if len(jj) else None,
                  "rel_abs_p99": float(rr.abs().quantile(.99)) if len(jj) else None, "rel_media_con_signo": float(rr.mean()) if len(jj) else None,
                  "n_dif_>1%": int((rr.abs() > .01).sum()), "n_dif_>5%": int((rr.abs() > .05).sum()), "n_dif_>10%": int((rr.abs() > .10).sum())}
    jp = j[j.cobertura_pob >= .999]
    r["suma_pob_nivel_vs_pob_municipio_rel_abs_p50_p99"] = [float(((jp.pob_total_nivel - jp.pob_mun) / jp.pob_mun).abs().quantile(q)) for q in (.5, .99)] if len(jp) else None
    jj = j[j.cobertura_pob >= .95].dropna(subset=["rel"])
    top = jj.reindex(jj.rel.abs().sort_values(ascending=False).index).head(8)
    r["top8_diferencias_cob>=0.95"] = [{"cod": i[0], "per": i[1], "rel": round(float(x.rel), 3), "n_sub": int(x.n)} for i, x in top.iterrows()]
    jer[nv] = r
D["2_jerarquia_municipio_vs_media_ponderada_subunidades"] = jer

sal = {}
for nv in ("municipio", "distrito", "seccion"):
    s = vp[(vp.nivel == nv) & (vp.valor > 0)].pivot_table(index="territorio_codigo", columns="periodo", values="valor")
    ys = [y for y in sorted(s.columns) if y <= "2023"]
    lg = np.log(s[ys]).diff(axis=1).iloc[:, 1:]
    o = {"unidades": int(len(s)), "transiciones": list(lg.columns)}
    zt = lg.apply(zrob)
    o["transversal_n_|z|>5_por_transicion"] = {y: int((zt[y].abs() > 5).sum()) for y in lg.columns}
    o["transversal_pct_|z|>5"] = round(100 * float((zt.abs() > 5).sum().sum() / lg.notna().sum().sum()), 3)
    o["tasa_mediana_por_transicion_%"] = {y: round(100 * float(lg[y].median()), 2) for y in lg.columns}
    o["tasa_abs_>50%_n"] = int((lg.abs() > np.log(1.5)).sum().sum())
    full = lg.dropna(thresh=6)
    med = full.median(axis=1)
    mad = full.sub(med, axis=0).abs().median(axis=1).clip(lower=.005)
    zu = 0.6745 * full.sub(med, axis=0).div(mad, axis=0)
    o["por_unidad_series_>=6_tasas"] = int(len(full))
    o["por_unidad_n_saltos_|z|>5"] = int((zu.abs() > 5).sum().sum())
    o["por_unidad_n_unidades_con_algun_salto"] = int((zu.abs() > 5).any(axis=1).sum())
    stack = zu.stack()
    stack = stack[stack.abs() > 5].abs().sort_values(ascending=False).head(6)
    o["por_unidad_top"] = [{"cod": a, "transicion": b, "z": round(float(z), 1), "tasa_%": round(100 * float(lg.loc[a, b]), 1)} for (a, b), z in stack.items()]
    sal[nv] = o
D["2_saltos_anuales_renta_neta_persona"] = sal

rup = {}
for nv in ("seccion", "distrito", "municipio"):
    s = vp[vp.nivel == nv]
    cj = {p: set(g.territorio_codigo) for p, g in s.groupby("periodo")}
    ys = sorted(y for y in cj if y <= "2023")
    rup[nv] = {"n_con_dato": {y: len(cj[y]) for y in ys}, "entran": {y: len(cj[y] - cj[ys[i]]) for i, y in enumerate(ys[1:])},
               "salen": {y: len(cj[ys[i]] - cj[y]) for i, y in enumerate(ys[1:])}}
    ev = set.union(*[cj[y] for y in ys])
    rup[nv]["unidades_en_algun_anio"] = len(ev)
    rup[nv]["unidades_en_los_9_anios"] = len(set.intersection(*[cj[y] for y in ys]))
    hu = 0
    for u in ev:
        ps = [ys.index(y) for y in ys if u in cj[y]]
        hu += int(len(ps) != ps[-1] - ps[0] + 1)
    rup[nv]["unidades_con_huecos_internos"] = hu
m = vp[vp.nivel == "municipio"]
cm = {p: set(g.territorio_codigo) for p, g in m.groupby("periodo")}
ent = cm["2020"] - cm["2019"]
rup["municipio_salto_2019_2020"] = {"entran": len(ent), "provincias_de_los_que_entran_top": {k: int(x) for k, x in pd.Series([c_[:2] for c_ in ent]).value_counts().head(8).items()},
                                    "metodo_dato_de_los_que_entran_2020": {k: int(x) for k, x in m[(m.periodo == "2020") & m.territorio_codigo.isin(ent)].metodo_dato.value_counts().items()}}
s = vp[vp.nivel == "seccion"].assign(mun=lambda x: x.territorio_codigo.str[:5])
nm = s.groupby(["periodo", "mun"]).territorio_codigo.nunique().unstack(0)
cols_ = [x for x in sorted(nm.columns) if x <= "2023"]
rup["municipios_cuyo_n_secciones_cambia"] = {f"{a}->{b}": int(((nm[a] != nm[b]) & nm[a].notna() & nm[b].notna()).sum()) for a, b in zip(cols_[:-1], cols_[1:])}
D["2_rupturas_cobertura_seccionado"] = rup

# ---------------------------------------------------------------- 3. valores que no son del propio municipio
vmu = vf[(vf.nivel == "municipio") & (vf.variable.astype(str).str.startswith("ine_adrh"))]
D["3_municipio_por_metodo_dato"] = {str(k): int(x) for k, x in vmu.metodo_dato.value_counts().items()}
nonobs = vmu[vmu.metodo_dato.astype(str) != "observado"].copy()
nonobs["prov"] = nonobs.territorio_codigo.astype(str).str[:2]
D["3_no_observado_por_provincia_top10"] = {k: int(x) for k, x in nonobs.prov.value_counts().head(10).items()}
D["3_no_observado_n_provincias"] = int(nonobs.prov.nunique())
D["3_no_observado_municipios_distintos"] = int(nonobs.territorio_codigo.nunique())
D["3_no_observado_por_variable"] = {str(k): int(x) for k, x in nonobs.variable.value_counts().items()}
D["3_no_observado_por_periodo"] = {str(k): int(x) for k, x in nonobs.periodo.value_counts().sort_index().items()}
D["3_subarea_navarra_provincias"] = sorted(nonobs[nonobs.metodo_dato.astype(str) == "valor_subarea_estrategia_territorial_navarra"].prov.unique().tolist())
for nv in ("distrito", "seccion", "provincia", "ccaa"):
    q = vf[(vf.nivel == nv) & (vf.metodo_dato.astype(str) != "observado") & (vf.variable.astype(str).str.startswith("ine_adrh"))]
    D[f"3_no_observado_en_nivel_{nv}"] = int(len(q))
r = vp[vp.nivel == "municipio"].copy()
r["prov"] = r.territorio_codigo.str[:2]
rep = r[r.metodo_dato == "observado"].groupby(["prov", "periodo", "valor"]).territorio_codigo.nunique()
rep = rep[rep >= 4]
D["3_valores_identicos_en_>=4_municipios_misma_provincia_y_anio_marcados_observado"] = {
    "n_grupos": int(len(rep)), "n_municipios_afectados": int(rep.sum()),
    "ejemplos": [{"prov": a, "per": b, "valor": float(c_), "n": int(n)} for (a, b, c_), n in rep.sort_values(ascending=False).head(5).items()]}
po = r[(r.metodo_dato == "observado") & (r.pob < 100)]
D["3_municipios_observado_con_pob_<100"] = {"n": int(len(po)), "periodos": sorted(po.periodo.unique().tolist())}
pn = r[(r.metodo_dato != "observado")]
D["3_no_observado_renta_persona_con_pob_conocida"] = {"n": int(pn.pob.notna().sum()), "pob_mediana": float(pn.pob.median()) if pn.pob.notna().any() else None,
                                                     "pob_<100_pct": round(100 * float((pn.pob < 100).mean()), 1)}
tb = pq.read_table(P / "renta_parque_adrh_completo.parquet", columns=["nivel", "metodo_dato", "muestra_sellada_v6"], filters=[("muestra_sellada_v6", "=", False)])
gr = tb.group_by(["nivel", "metodo_dato"]).aggregate([([], "count_all")]).to_pandas()
D["3_completo_muestra_v6_no_marcada_recuento_nivel_metodo"] = {f"{a}|{b}": int(n) for a, b, n in zip(gr.nivel, gr.metodo_dato, gr.count_all)}
del tb, gr, nonobs, r, po, pn
gc.collect()

# ---------------------------------------------------------------- 4. alias manuales
src = (RAIZ / "src/v16/datos/renta_parque.py").read_text(encoding="utf-8")
ini = src.index("ALIAS = {")
fin = src.index("\n}", ini)
alias = {}
for ln in src[ini:fin].splitlines()[1:]:
    ln = ln.strip()
    if ln.startswith("("):
        k, vv = ln.rstrip(",").split("):")
        alias[eval(k + ")")] = eval(vv)
t = pq.read_table(RAIZ / "data/base/publica/territorios.parquet", columns=["territorio_codigo", "nivel", "nombre", "cod_provincia", "vigente_2025"]).to_pandas()
tm = t[t.nivel == "municipio"].set_index("territorio_codigo")
corr = pd.read_csv(RAIZ / "docs/v16/fuentes/renta_parque_correspondencia.csv", dtype=str, keep_default_na=False)
al = []
for (pv, nom), cod in alias.items():
    ok = cod in tm.index
    nm_ine = tm.nombre.get(cod)
    sim = difflib.SequenceMatcher(None, nom.lower(), str(nm_ine).lower()).ratio() if ok else None
    cand = tm[tm.index.str[:2] == pv].nombre
    best = max(cand.items(), key=lambda kv: difflib.SequenceMatcher(None, nom.lower(), kv[1].lower()).ratio())
    fila = corr[(corr.nombre_adrh == nom) & (corr.provincia_inferida == pv)]
    al.append({"provincia": pv, "nombre_adrh": nom, "codigo_alias": cod, "existe_en_territorios": bool(ok), "nombre_territorios": nm_ine, "provincia_coincide": cod[:2] == pv,
               "vigente_2025": bool(tm.vigente_2025.get(cod)) if ok else None, "similitud_nombre": round(sim, 2) if sim is not None else None,
               "mejor_candidato_por_similitud": {"cod": best[0], "nombre": best[1]}, "es_el_mejor_candidato": best[0] == cod,
               "estado_en_correspondencia": fila.estado.iloc[0] if len(fila) else None, "codigo_en_correspondencia": fila.codigo_ine.iloc[0] if len(fila) else None,
               "n_series": int(fila.n_series.iloc[0]) if len(fila) else None})
D["4_alias"] = al
D["4_alias_n"] = len(al)
D["4_alias_codigo_y_provincia_ok"] = int(sum(a["existe_en_territorios"] and a["provincia_coincide"] for a in al))
D["4_alias_no_es_el_mejor_candidato_por_similitud"] = [a["nombre_adrh"] for a in al if not a["es_el_mejor_candidato"]]
D["4_correspondencia_estados"] = {k: int(x) for k, x in corr.estado.value_counts().items()}
cc = corr[corr.codigo_ine != ""]
dup = cc.groupby("codigo_ine").nombre_adrh.nunique()
D["4_codigos_ine_con_>1_nombre_adrh"] = {k: cc[cc.codigo_ine == k].nombre_adrh.tolist() for k in dup[dup > 1].index[:10]}
D["4_sin_coincidencia"] = corr[corr.estado == "sin_coincidencia"][["provincia_inferida", "nombre_adrh", "n_series"]].to_dict("records")

# ---------------------------------------------------------------- 5. Catastro URBANA2026
cat = vf[(vf.variable == "catastro_urbano_superficie_suelo_m2") & (vf.nivel == "municipio")][["territorio_codigo", "valor"]].copy()
cat["territorio_codigo"] = cat.territorio_codigo.astype(str)
D["5_catastro_municipios_tras_filtro"] = int(len(cat))
cat_all = pq.read_table(P / "renta_parque.parquet", columns=["territorio_codigo", "variable"], filters=[("variable", "=", "catastro_urbano_superficie_suelo_m2")]).to_pandas()
D["5_catastro_municipios_total"] = int(len(cat_all))
D["5_catastro_provincias_ausentes_de_las_52"] = sorted(set(f"{i:02d}" for i in range(1, 53)) - set(cat_all.territorio_codigo.str[:2]))
terr_mun = set(tm.index[tm.vigente_2025.astype(bool)])
falta = sorted(terr_mun - set(cat_all.territorio_codigo))
D["5_municipios_vigentes_sin_catastro"] = len(falta)
D["5_municipios_vigentes_sin_catastro_por_provincia"] = {k: int(x) for k, x in pd.Series(falta).str[:2].value_counts().items()}
ha = pq.read_table(P / "oferta_suelo_terceros.parquet", columns=["territorio_codigo", "variable", "valor"], filters=[("variable", "=", "ine_geo_superficie_municipio_ha")]).to_pandas()
ha = ha.drop_duplicates("territorio_codigo").set_index("territorio_codigo").valor.rename("ha")
try:
    import geopandas as gpd
    gm = gpd.read_parquet(RAIZ / "data/base/geo/municipios.parquet")
    ar = (gm.to_crs(3035).geometry.area / 1e4)
    ar.index = gm.cod_municipio.astype(str)
    ar = ar[~ar.index.duplicated()].rename("ha_geo")
    D["5_poligono_ha_vs_ine_ha_cociente_mediana_p5_p95"] = [float((ar / ha).dropna().quantile(q)) for q in (.5, .05, .95)]
except Exception as e:  # noqa: BLE001
    D["5_geo_error"] = str(e)[:200]
q = cat.set_index("territorio_codigo").valor.rename("m2").to_frame().join(ha, how="left")
q["fraccion_si_m2"] = q.m2 / (q.ha * 1e4)
q["fraccion_si_ha"] = q.m2 / q.ha
D["5_superf_urb_con_ha_municipal"] = int(q.ha.notna().sum())
D["5_fraccion_suelo_urbano_si_m2_(p1,p50,p99,max)"] = [float(q.fraccion_si_m2.quantile(x)) for x in (.01, .5, .99, 1)]
D["5_fraccion_suelo_urbano_si_ha_(p1,p50,p99,max)"] = [float(q.fraccion_si_ha.quantile(x)) for x in (.01, .5, .99, 1)]
D["5_n_fraccion_si_m2_>1"] = int((q.fraccion_si_m2 > 1).sum())
D["5_n_fraccion_si_ha_>1"] = int((q.fraccion_si_ha > 1).sum())
uu = vf[(vf.variable == "catastro_urbano_unidades_numero") & (vf.nivel == "municipio")].set_index("territorio_codigo").valor
uu.index = uu.index.astype(str)
q["uni"] = uu.reindex(q.index)
D["5_mediana_superficie_suelo_m2_por_unidad_urbana"] = float((q.m2 / q.uni).median())
D["5_superficie_suelo_<=0"] = int((q.m2 <= 0).sum())
ex = q[q.fraccion_si_m2 > 1].sort_values("fraccion_si_m2", ascending=False).head(8)
D["5_top_fraccion_si_m2>1"] = [{"cod": i, "m2": float(x.m2), "ha": float(x.ha), "fraccion": round(float(x.fraccion_si_m2), 2)} for i, x in ex.iterrows()]
vc = vf[(vf.nivel == "municipio") & vf.variable.isin(["catastro_urbano_valor_catastral_eur", "catastro_urbano_valor_suelo_eur", "catastro_urbano_valor_construccion_eur"])]
vc = vc.assign(variable=vc.variable.astype(str)).pivot_table(index="territorio_codigo", columns="variable", values="valor")
rel = ((vc.catastro_urbano_valor_suelo_eur + vc.catastro_urbano_valor_construccion_eur) / vc.catastro_urbano_valor_catastral_eur - 1).abs()
D["5_valor_suelo_mas_construccion_vs_total_rel_max_p99"] = [float(rel.max()), float(rel.quantile(.99))]
D["5_n_municipios_valor_catastral_<=0"] = int((vc.catastro_urbano_valor_catastral_eur <= 0).sum())

# ---------------------------------------------------------------- 2b/3b/4b. comprobaciones adicionales
# jerarquía: desglose por año y solo municipios con >= 2 subunidades
jj = {}
for nv in ("seccion", "distrito"):
    s = vp[(vp.nivel == nv) & vp.pob.notna() & (vp.pob > 0)].copy()
    s["mun"] = s.territorio_codigo.str[:5]
    g = s.assign(rw=s.valor * s.pob).groupby(["mun", "periodo"]).agg(rw=("rw", "sum"), w=("pob", "sum"), n=("valor", "size"))
    g["mp"] = g.rw / g.w
    g.index = g.index.set_names(["territorio_codigo", "periodo"])
    j = g[g.n >= 2].join(mun[["valor", "pob"]].rename(columns={"valor": "vm", "pob": "pm"}), how="inner")
    j["rel"] = (j.mp - j.vm) / j.vm
    j["cob"] = j.w / j.pm
    o = {"pares_con_>=2_subunidades": int(len(j)), "rel_abs_p50": float(j.rel.abs().quantile(.5)), "rel_abs_p95": float(j.rel.abs().quantile(.95)), "rel_abs_p99": float(j.rel.abs().quantile(.99)),
         "n_>1%": int((j.rel.abs() > .01).sum()), "n_>5%": int((j.rel.abs() > .05).sum())}
    o["n_>5%_por_periodo"] = {p: int(x) for p, x in j[j.rel.abs() > .05].groupby("periodo").size().items()}
    o["pares_por_periodo"] = {p: int(x) for p, x in j.groupby("periodo").size().items()}
    jc = j[(j.cob > .98) & (j.cob < 1.02)]
    o["con_cobertura_pob_entre_0.98_y_1.02"] = {"n": int(len(jc)), "rel_abs_p99": float(jc.rel.abs().quantile(.99)), "n_>1%": int((jc.rel.abs() > .01).sum()), "n_>5%": int((jc.rel.abs() > .05).sum())}
    o["cobertura_pob_(suma_subunidades/pob_municipio)_p1_p50_p99"] = [float(j.cob.quantile(q)) for q in (.01, .5, .99)]
    jj[nv] = o
D["2b_jerarquia_solo_municipios_con_>=2_subunidades"] = jj

# claves duplicadas y marcado de Navarra en el versionado completo (sin filtrar)
vv = pq.read_table(P / "renta_parque.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable", "desagregacion", "metodo_dato"]).to_pandas()
D["3b_claves_duplicadas_versionado"] = int(vv.duplicated(["territorio_codigo", "nivel", "periodo", "variable", "desagregacion"]).sum())
nv_ = vv[vv.metodo_dato == "valor_subarea_estrategia_territorial_navarra"]
D["3b_subarea_navarra_versionado"] = {"filas": int(len(nv_)), "niveles": {k: int(x) for k, x in nv_.nivel.value_counts().items()}, "provincias": sorted(nv_.territorio_codigo.str[:2].unique().tolist()),
                                      "variables": {k: int(x) for k, x in nv_.variable.value_counts().items()}, "periodos": sorted(nv_.periodo.unique().tolist())}
mp = vv[(vv.variable == V_PER) & (vv.nivel == "municipio") & (vv.desagregacion == "")]
con_dato = set(mp.territorio_codigo)
sin = sorted(terr_mun - con_dato)
D["3b_municipios_vigentes_sin_ningun_dato_renta_persona_municipal"] = {"n": len(sin), "por_provincia": {k: int(x) for k, x in pd.Series(sin).str[:2].value_counts().head(12).items()},
                                                                       "n_provincia_31": int(sum(x[:2] == "31" for x in sin))}
rn = mp.groupby("territorio_codigo").periodo.nunique()
D["3b_municipios_vigentes_sin_dato_nombres"] = {x: tm.nombre.get(x) for x in sin}
D["3b_municipios_con_renta_persona_por_n_anios"] = {int(k): int(x) for k, x in rn.value_counts().sort_index().items()}
del vv, mp
# alias: candidatos de los 18 sin coincidencia
cand = {}
tmn = tm[~tm.nombre.str.startswith("municipio ")]
for rr in D["4_sin_coincidencia"]:
    if rr["provincia_inferida"] == "NAC":
        continue
    pvv = rr["provincia_inferida"]
    cs = tmn[tmn.index.str[:2] == pvv].nombre
    top = sorted(cs.items(), key=lambda kv: -difflib.SequenceMatcher(None, rr["nombre_adrh"].lower(), kv[1].lower()).ratio())[:2]
    cand[f"{pvv}|{rr['nombre_adrh']}"] = [{"cod": a, "nombre": b, "sim": round(difflib.SequenceMatcher(None, rr["nombre_adrh"].lower(), b.lower()).ratio(), 2)} for a, b in top]
D["4b_sin_coincidencia_mejores_candidatos_misma_provincia"] = cand
D["4b_territorios_municipios_con_nombre_provisional_municipio_"] = int(tm.nombre.str.startswith("municipio ").sum())
sup = ["Noáin", "Valle de Elorz"]
D["4b_territorios_31_nombres_noain_elorz"] = {a: b for a, b in tm.nombre.items() if a[:2] == "31" and any(s_.lower() in b.lower() for s_ in sup)}
D["4b_territorios_12_castell"] = {a: b for a, b in tm.nombre.items() if a[:2] == "12" and "plana" in b.lower()}
# Catastro: municipios vigentes sin catastro fuera de las 4 provincias forales
D["5b_sin_catastro_fuera_de_01_20_31_48"] = {a: tm.nombre.get(a) for a in falta if a[:2] not in ("01", "20", "31", "48")}
D["5b_max_fraccion_si_m2"] = {i: {"nombre": tm.nombre.get(i), "fraccion": round(float(x), 3)} for i, x in q.fraccion_si_m2.nlargest(3).items()}

# ---------------------------------------------------------------- 6. inventario ECV y EPF
RW = RAIZ / "data/raw/v16/renta_parque"
PES = ("DB090", "DB095", "RB050", "RB060", "PB040", "PB060", "RX030", "FACTOR")


def cab(zf, n):
    with zf.open(n) as f:
        t_ = f.readline().decode("latin-1", "ignore").strip().replace("\t", ";").replace(",", ";")
    return [x.strip().strip('"') for x in t_.split(";")]


def mira(z):
    """Lista ficheros de usuario (d, h, p, r), tamaño y pesos en cabecera; baja un nivel si hay un ZIP interior de datos."""
    try:
        with zipfile.ZipFile(z) as zf:
            nl = zf.namelist()
            res_ = {"miembros": nl[:8], "ficheros": {}}
            def csvs(zz, pref=""):
                for n in zz.namelist():
                    if n.lower().endswith(".csv") and "disreg" not in n.lower():
                        c_ = cab(zz, n)
                        res_["ficheros"][pref + n] = {"mb": round(zz.getinfo(n).file_size / 1e6, 1), "n_columnas": len(c_), "pesos": [x for x in c_ if x.upper().startswith(PES) and not x.endswith("_F")]}
            csvs(zf)
            for n in nl:
                if n.lower().endswith(".zip") and "disreg" not in n.lower():
                    with zipfile.ZipFile(io.BytesIO(zf.read(n))) as zi:
                        csvs(zi, n + "/")
            return res_
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:120]}


rutas = {"ecv_transversal_2013_2017": sorted((RW / "ecv").glob("datos_*.zip")), "ecv_transversal_2004_2012": sorted((RW / "ecv/transversal_2004_2012").glob("*.zip")),
         "ecv_longitudinal": sorted((RW / "ecv/longitudinal").glob("*.zip")), "ecv_transversal_2018_2025_v9": sorted((RAIZ / "data/raw/v9/ine_microdatos/ecv").glob("datos_*.zip"))}
inv_ = {}
for k, fs in rutas.items():
    mir = {f.stem: mira(f) for f in fs}
    resumen = {}
    for ola, mm in mir.items():
        fich = mm.get("ficheros", {})
        resumen[ola] = {"n_ficheros_csv": len(fich), "pesos": sorted({p for x in fich.values() for p in x["pesos"]}), "error": mm.get("error"),
                        "mb_csv": round(sum(x["mb"] for x in fich.values()), 1)}
    inv_[k] = {"n_zips": len(fs), "olas": resumen}
epf = {}
for sub in ("epf2006", "bienestar"):
    dd = RW / "epf" / sub
    epf[sub] = [{"fichero": f.name, "mb": round(f.stat().st_size / 1e6, 1)} for f in sorted(dd.glob("*"))] if dd.exists() else []
    for f in sorted(dd.glob("datos*.zip")):
        with zipfile.ZipFile(f) as zf:
            epf[f"microdatos_{sub}"] = {i.filename: round(i.file_size / 1e6, 1) for i in zf.infolist()}
    for f in sorted(dd.glob("disreg*.zip")):
        with zipfile.ZipFile(f) as zf:
            epf[f"disreg_{sub}"] = zf.namelist()
            pes = {}
            for n in zf.namelist():
                if not n.lower().endswith(".xlsx"):
                    pes[n] = "no es xlsx; no leído"
                    continue
                try:
                    x = pd.read_excel(io.BytesIO(zf.read(n)), header=None)
                    pes[n] = sorted({str(s_) for s_ in x.stack().dropna().tolist() if str(s_).upper().startswith("FACTOR")})[:6]
                except Exception as e:  # noqa: BLE001
                    pes[n] = f"no legible: {str(e)[:60]}"
            epf[f"pesos_en_disreg_{sub}"] = pes
zz = RW / "ecv/longitudinal/b2013_periodo_2008-2011.zip"
inv_["ecv_longitudinal_b2013_2008-2011_miembros"] = zipfile.ZipFile(zz).namelist()[:10]
inv_["epf"] = epf
D["6_inventario_ecv_epf"] = inv_
D["6_nota"] = "solo inventario; la validación de ECV frente a Eurostat corresponde al módulo f2_esfuerzo"

res = base_resultado(
    "v16/auditoria/renta_parque",
    "¿Son coherentes, comparables y correctamente marcados los datos de renta (ADRH), parque (Catastro urbano 2026) y los microdatos ECV/EPF de la familia renta_parque?",
    ["data/processed/v16/renta_parque.parquet", "data/processed/v16/renta_parque_adrh_completo.parquet (no versionado)", "data/base/publica/hechos.parquet", "data/base/publica/territorios.parquet",
     "data/base/geo/municipios.parquet", "data/processed/v16/oferta_suelo_terceros.parquet (solo ha municipales INE)"],
    int(len(vf)), "Cotejo valor a valor, medias ponderadas jerárquicas, |z robusto (mediana, MAD)| > 5, recuentos por metodo_dato, verificación de alias, cociente de superficies; sin estimación.",
    D, "Filtrado muestra_sellada_v6 == False y holdout.unidad_sellada_v16 (booleanos). Auditoría descriptiva (C4); sin efectos estimados. Detalle en informe.md.")
_inf = Path(__file__).with_name("renta_parque_informe.md")
escribe("renta_parque", res, _inf.read_text(encoding="utf-8") if _inf.exists() else "(informe pendiente)")
print(json.dumps(D, ensure_ascii=False, default=str)[:40000])
