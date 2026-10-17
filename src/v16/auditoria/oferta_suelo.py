"""Auditoría V16 fase 1: oferta_suelo (IMM del INE y Red Natura 2000 municipal). C4, descriptivo. SEED=20261010."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.auditoria._comun import RAIZ, SEED, base_resultado, escribe, zrob  # noqa: E402

np.random.seed(SEED)
D = {}
d = pd.read_parquet(RAIZ / "data/processed/v16/oferta_suelo.parquet")
d = d[~d.muestra_sellada_v6]

# ---------- 1. IMM
huecos, rupt, atip, esc = {}, {}, {}, {}
for v, g in d.groupby("variable"):
    s = g.set_index("periodo").valor.astype(float).sort_index()
    idx = pd.period_range(s.index[0], s.index[-1], freq="M").astype(str)
    falt = [m for m in idx if m not in s.index]
    if falt:
        huecos[v] = {"n_faltan": len(falt), "meses": falt[:12], "tramos": None}
    lg = np.log(s).diff().dropna()
    z = zrob(lg)
    k = z[z.abs() > 5]
    atip[v] = {"n": int(len(k)), "top": [(i, round(float(zz), 1), round(float(100 * lg[i]), 1)) for i, zz in k.abs().sort_values(ascending=False).head(3).items()]}
    # ruptura de nivel: salto mensual mayor del 25 % o series con valores constantes largos
    big = lg[lg.abs() > .25]
    if len(big):
        rupt[v] = [(i, round(float(100 * x), 1)) for i, x in big.items()][:6]
    run = (s.diff().fillna(1) == 0).astype(int)
    mx = int(run.groupby((run == 0).cumsum()).sum().max())
    if mx >= 6:
        esc[v] = {"racha_maxima_valores_repetidos": mx}
    if s.min() <= 0:
        esc[v] = esc.get(v, {}) | {"valores_<=0": int((s <= 0).sum())}
D["1_series"] = int(d.variable.nunique())
D["1_series_con_huecos"] = huecos
D["1_atipicos_|z|>5_variacion_mensual_n_por_serie"] = {k: v["n"] for k, v in atip.items()}
D["1_atipicos_top"] = {k: v["top"] for k, v in atip.items() if v["n"]}
D["1_saltos_mensuales_>25%"] = rupt
D["1_rachas_constantes_o_valores_no_positivos"] = esc
# fin de serie y retraso respecto a la fecha de revisión
D["1_ultimo_periodo"] = sorted(d.periodo.unique())[-1]
D["1_retraso_meses_hasta_2026-10"] = 7
# bases: nivel 2011=100 -> el valor medio de 2011 debería ser ~100 (solo desde 2012: no verificable); comprobar el nivel de 2012-01
base = {}
for v, g in d.groupby("variable"):
    s = g.set_index("periodo").valor.astype(float).sort_index()
    base[v] = {"unidad": g.unidad.iloc[0], "primero": round(float(s.iloc[0]), 2), "ultimo": round(float(s.iloc[-1]), 2), "min": round(float(s.min()), 2), "max": round(float(s.max()), 2)}
D["1_niveles"] = base
# rupturas de base: IMM1 (mano de obra) 1995-2026: salto anual de enero (convenios)
mo = d[d.variable == "ine_imm_mano_obra_construccion_indice"].set_index("periodo").valor.astype(float).sort_index()
D["1_mano_obra_variacion_mediana_mensual_%_por_mes_calendario"] = {m: round(float(100 * np.log(mo).diff()[[p for p in mo.index if p.endswith(f"-{m:02d}")]].median()), 2) for m in range(1, 13)}
# coherencia: materiales generales agregados vs construcción (Eurostat sts_copi_q si existe en data/raw/eurostat_costes.csv, España)
try:
    ec = pd.read_csv(RAIZ / "data/raw/eurostat_costes.csv")
    D["1_eurostat_costes_columnas"] = ec.columns.tolist()[:12]
except Exception as e:  # noqa: BLE001
    D["1_eurostat_costes_error"] = str(e)

# ---------- 2. Red Natura 2000 por municipio (terceros; solo agregados propios)
t = pd.read_parquet(RAIZ / "data/processed/v16/oferta_suelo_terceros.parquet")
t = t[~t.muestra_sellada_v6]
w = t.pivot_table(index="territorio_codigo", columns="variable", values="valor")
w = w.rename(columns={"miteco_rn2000_porcentaje_superficie_municipal": "pct", "miteco_rn2000_superficie_municipio_ha": "rn_ha", "ine_geo_superficie_municipio_ha": "ha"})
D["2_municipios_no_sellados"] = int(len(w))
D["2_pct_fuera_de_[0,100]"] = int(((w.pct < 0) | (w.pct > 100)).sum())
D["2_pct_NaN"] = int(w.pct.isna().sum())
w["pct_calc"] = 100 * w.rn_ha / w.ha
D["2_rn_ha_mayor_que_ha_municipio"] = {"n": int((w.rn_ha > w.ha * 1.0001).sum()), "max_exceso_%": round(float((w.pct_calc - 100).max()), 4)}
D["2_pct_igual_100_n"] = int((w.pct >= 99.999).sum())
D["2_pct_entre_95_y_100_n"] = int(((w.pct >= 95) & (w.pct < 100)).sum())
D["2_pct_guardado_vs_recalculado_max_abs_dif"] = round(float((w.pct - w.pct_calc.clip(0, 100)).abs().max()), 6)
D["2_ha_municipio_<=0"] = int((w.ha <= 0).sum())
D["2_con_algo_de_RN_n"] = int((w.pct > 0).sum())
D["2_pct_percentiles"] = {str(q): round(float(w.pct.quantile(q)), 2) for q in (.25, .5, .75, .9, .99)}
# atípicos del área municipal (log ha) dentro de cada provincia
w["prov"] = w.index.str[:2]
lz = np.log(w.ha.clip(lower=1))
w["z_area"] = lz.groupby(w.prov).transform(lambda x: zrob(x))
D["2_area_atipica_|z|>5_intraprovincial_n"] = int((w.z_area.abs() > 5).sum())
D["2_areas_extremas_ha"] = {"min": [w.ha.idxmin(), round(float(w.ha.min()), 1)], "max": [w.ha.idxmax(), round(float(w.ha.max()), 0)]}
D["2_areas_<50ha_n"] = int((w.ha < 50).sum())
D["2_suma_area_no_sellados_Mha"] = round(float(w.ha.sum() / 1e6), 3)
D["2_suma_RN_no_sellados_Mha"] = round(float(w.rn_ha.sum() / 1e6), 3)
D["2_porcentaje_RN_sobre_area_no_sellados"] = round(float(100 * w.rn_ha.sum() / w.ha.sum()), 2)
# Por provincia (no selladas): % RN agregado
pp = (w.groupby("prov").rn_ha.sum() / w.groupby("prov").ha.sum() * 100).round(1)
D["2_pct_RN_por_provincia_min_max"] = {"min": [pp.idxmin(), float(pp.min())], "max": [pp.idxmax(), float(pp.max())]}
# frontera exterior: municipios cuyo polígono toca el límite del conjunto nacional (costa o frontera internacional)
try:
    import geopandas as gpd  # noqa: F401
    from shapely import STRtree  # noqa: F401
    from shapely.ops import unary_union
    g = pd.read_parquet(RAIZ / "data/base/geo/municipios.parquet")
    import geopandas as gpd
    g = gpd.GeoDataFrame(g.drop(columns="geometry"), geometry=gpd.GeoSeries.from_wkb(g.geometry), crs="EPSG:4326").to_crs(3035)
    g["geometry"] = g.geometry.buffer(0)
    from shapely import prepare
    cc = pd.read_parquet(RAIZ / "data/base/geo/ccaa.parquet")
    cc = gpd.GeoDataFrame(cc.drop(columns="geometry"), geometry=gpd.GeoSeries.from_wkb(cc.geometry), crs="EPSG:4326").to_crs(3035)
    ext = unary_union([x.buffer(0) for x in cc.geometry]).boundary.buffer(300)  # borde exterior nacional (costa o frontera)
    prepare(ext)
    gs = g.geometry.simplify(100)
    g["comparte_ext"] = 0.0
    for i, geom in enumerate(gs):
        if geom.intersects(ext):
            g.iloc[i, g.columns.get_loc("comparte_ext")] = geom.boundary.intersection(ext).length / max(geom.boundary.length, 1)
    g = g.set_index("cod_municipio")
    # distinguimos frontera terrestre aproximando con la provincia: costeras = no frontera si no está en Pirineos... se informa el conjunto «exterior»
    ex = g.comparte_ext > 0.10
    w["exterior"] = ex.reindex(w.index).fillna(False)
    D["2_municipios_frontera_exterior_(costa+frontera)_n"] = int(w.exterior.sum())
    for nom, s in (("exterior", w[w.exterior]), ("interior", w[~w.exterior])):
        D[f"2_{nom}"] = {"n": int(len(s)), "pct_RN_mediana": round(float(s.pct.median()), 2), "pct_RN_agregado": round(float(100 * s.rn_ha.sum() / s.ha.sum()), 2), "con_RN_%": round(float(100 * (s.pct > 0).mean()), 1),
                         "pct=100_n": int((s.pct >= 99.999).sum())}
    # municipios exteriores sin ningún Natura en provincias costeras mediterráneas (sospecha de omisión de parte marina): solo recuento
    D["2_nota_geometria"] = "polígonos INE 2025 terrestres (la parte marina de los sitios queda fuera); el área municipal no incluye aguas territoriales"
except Exception as e:  # noqa: BLE001
    D["2_error_frontera"] = repr(e)
# Referencia nacional: la ficha no cita la superficie Natura publicada por MITECO
D["2_referencia_MITECO_en_ficha"] = "No hay cifra de superficie Natura 2000 de MITECO en docs/v16/fuentes/oferta_suelo.md; solo suma de áreas municipales 50,4 Mha (ficha) frente a ~50,6 Mha de España. No verificada aquí: proporción terrestre publicada en torno al 27 % (NO VERIFICADA)."

res = base_resultado("v16/auditoria/oferta_suelo", "¿Son consistentes las series IMM y el cálculo de Red Natura por municipio?",
                     "data/processed/v16/oferta_suelo*.parquet (muestra_sellada_v6=False); data/base/geo/municipios.parquet (solo geometría)", int(len(d) + len(t)),
                     "mediana/MAD (|z|>5), huecos, saltos, recálculo del porcentaje, comparación exterior/interior", D,
                     ["Terceros (MITECO Red Natura): solo agregados propios.", "La suma nacional no puede calcularse sin los municipios de la muestra sellada; se informa la de los no sellados."])
INF = RAIZ / "output/v16/auditoria/oferta_suelo/informe.md"
if __name__ == "__main__":
    escribe("oferta_suelo", res, INF.read_text(encoding="utf-8") if INF.exists() else "(informe pendiente)")
    print(json.dumps({k: v for k, v in D.items() if k.startswith("2_")}, ensure_ascii=False, indent=1, default=str)[:6000])
