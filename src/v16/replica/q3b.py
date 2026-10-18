"""Replica ciega Q3-b: dlog SERPAVI (VC, m2) 2021-2024 por seccion vs cuota de extranjeros 2022
(estandarizada), efectos fijos de municipio, SE Conley 2 km. SEED=20261010."""
import json
import os
import numpy as np
import pandas as pd
import shapely
from scipy.spatial import cKDTree
from scipy import stats

SEED = 20261010
np.random.seed(SEED)
R = "/home/user/Econometr-a"
ENT = R + "/data/processed/v16/entrenamiento/"
OUT = R + "/output/v16/replica/q3b/"
os.makedirs(OUT, exist_ok=True)
CIFRA = dict(coef=0.0091, lo=0.0060, hi=0.0122, p=7.6e-9)

a = pd.read_parquet(ENT + "base_alquiler.parquet")
a = a[(a.nivel == "seccion") & (a.variable == "serpavi_alquiler_m2_mediana")
      & (a.desagregacion == "tipologia=VC") & a.periodo.astype(str).isin(["2021", "2024"])]
w = a.pivot_table(index="territorio_codigo", columns="periodo", values="valor")
w.columns = w.columns.astype(int)
w = w[(w[2021] > 0) & (w[2024] > 0)].dropna()
y = np.log(w[2024]) - np.log(w[2021])
y.name = "dlog"

t = pd.read_parquet(ENT + "tension_social.parquet",
                    columns=["territorio_codigo", "periodo", "variable", "desagregacion", "valor"])
t = t[(t.variable == "ine_padron_seccion_poblacion_personas") & (t.periodo.astype(str) == "2022")]
tot = t[t.desagregacion == "sexo=ambos_sexos;nacionalidad=total"].set_index("territorio_codigo").valor
ext = t[t.desagregacion == "sexo=ambos_sexos;nacionalidad=total_extranjera"].set_index("territorio_codigo").valor
cuota = (ext / tot[tot > 0]).dropna().rename("cuota")

g = pd.read_parquet(R + "/data/base/geo/secciones.parquet", columns=["cod_seccion", "cod_municipio", "geometry"])
c = shapely.centroid(shapely.from_wkb(g.geometry.values))
g["lon"] = shapely.get_x(c)
g["lat"] = shapely.get_y(c)
g = g.set_index("cod_seccion")[["cod_municipio", "lon", "lat"]]

d = pd.concat([y, cuota], axis=1, join="inner").join(g, how="inner").dropna()
d = d[np.isfinite(d.dlog)]
n_antes = len(d)
nsec = d.groupby("cod_municipio").dlog.transform("size")
d = d[nsec > 1].copy()
d["z"] = (d.cuota - d.cuota.mean()) / d.cuota.std(ddof=1)  # DT entre secciones (muestra analitica)
sd = float(d.cuota.std(ddof=1))


def ols_conley(d, radius_km, kernel="bartlett"):
    yy = d.dlog - d.groupby("cod_municipio").dlog.transform("mean")
    xx = d.z - d.groupby("cod_municipio").z.transform("mean")
    yy = yy.values
    xx = xx.values
    n = len(d)
    G = d.cod_municipio.nunique()
    b = (xx @ yy) / (xx @ xx)
    e = yy - b * xx
    lat = np.radians(d.lat.values)
    lon = np.radians(d.lon.values)
    P = np.c_[np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)] * 6371.0088
    tree = cKDTree(P)
    pairs = tree.sparse_distance_matrix(tree, radius_km, output_type="coo_matrix")
    dist = pairs.data
    if kernel == "bartlett":
        wgt = 1 - dist / radius_km
    else:
        wgt = np.ones_like(dist)
    # diagonal: dist 0 -> wgt 1 (sparse coo may drop zero entries; add explicitly)
    m = pairs.row != pairs.col
    i, j, ww = pairs.row[m], pairs.col[m], wgt[m]
    s = xx * e
    meat = np.sum(s ** 2) + np.sum(ww * s[i] * s[j])
    sxx = xx @ xx
    se = np.sqrt(meat) / sxx
    # correccion de grados de libertad (gl = n - G - 1) no aplicada; variante abajo
    se_dof = se * np.sqrt(n / (n - G - 1))
    return b, se, se_dof, n, G, int(m.sum())


res = {}
for k in ["bartlett", "uniforme"]:
    res[k] = ols_conley(d, 2.0, k)
b, se, se_dof, n, G, npairs = res["bartlett"]
zc = stats.norm.ppf(0.975)
ic = [b - zc * se, b + zc * se]
p = 2 * stats.norm.sf(abs(b / se))

# variante: sin kernel (solo hetero-robusto) y agrupado por municipio
yy = d.dlog - d.groupby("cod_municipio").dlog.transform("mean")
xx = d.z - d.groupby("cod_municipio").z.transform("mean")
e = yy.values - b * xx.values
s = pd.Series(xx.values * e, index=d.index).groupby(d.cod_municipio).sum()
se_cl = float(np.sqrt((s ** 2).sum()) / (xx.values @ xx.values))

se_ref = (CIFRA["hi"] - CIFRA["lo"]) / (2 * zc)
dcoef = (b - CIFRA["coef"]) / CIFRA["coef"]
dee = (se - se_ref) / se_ref
veredicto = "COINCIDE" if abs(dcoef) <= 0.05 and abs(dee) <= 0.15 else "DISCREPA"
out = dict(
    id="q3b", rama="v16", pregunta="Q3-b", capa="C4", metodo="OLS con EF de municipio (demeaning), VC, cuota 2022 estandarizada, Conley 2 km (Bartlett, centroides, distancia esferica)",
    N=n, municipios=G, secciones_antes_filtro=n_antes, DT_cuota=sd,
    estimacion=b, ee_conley_2km=se, ic95=ic, p=p,
    variantes=dict(conley_uniforme=dict(coef=res["uniforme"][0], ee=res["uniforme"][1]),
                   conley_bartlett_gl=dict(ee=se_dof), cluster_municipio_ee=se_cl),
    comparacion=dict(cifra_orquestador=CIFRA, ee_orquestador_implicito=se_ref,
                     dif_abs=b - CIFRA["coef"], dif_rel_coef=dcoef, dif_rel_ee=dee,
                     mi_est_en_IC_orq=bool(CIFRA["lo"] <= b <= CIFRA["hi"]),
                     est_orq_en_mi_IC=bool(ic[0] <= CIFRA["coef"] <= ic[1]), veredicto=veredicto),
    seed=SEED)
json.dump(out, open(OUT + "resultado.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps(out, indent=2, ensure_ascii=False))
