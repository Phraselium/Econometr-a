"""Replica ciega H3 (V15, P5): log SERPAVI VC sobre % viviendas turisticas INE.
EF de seccion y municipio x anio, 2021-2024; exposicion estandarizada por la DT intra-seccion.
Solo estimacion puntual. SEED=20261010."""
import json
import os
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
ROOT = "/home/user/Econometr-a"
OUT = os.path.join(ROOT, "output/v16/replica/h3")
os.makedirs(OUT, exist_ok=True)

d = pd.read_parquet(os.path.join(ROOT, "data/processed/v15/p5_turismo_seccion.parquet"))
s = d[d.nivel == "seccion"].copy()
s["anio"] = s.periodo.str[:4].astype(int)

# exposicion: media anual de las ediciones del anio
e = s[s.variable == "ine_vut_porcentaje_vivienda_turistica"]
e = e[e.anio.between(2021, 2024)].groupby(["territorio_codigo", "anio"]).valor.mean().rename("x").reset_index()

# codigo presente en ediciones INE VUT de 2021 y 2024 (cualquier variable INE)
ine = s[s.variable.str.startswith("ine_vut")]
c21 = set(ine[ine.anio == 2021].territorio_codigo)
c24 = set(ine[ine.anio == 2024].territorio_codigo)
ok = c21 & c24

# resultado: SERPAVI VC EUR/m2
y = s[(s.variable == "serpavi_alquiler_m2_mediana") & (s.desagregacion == "tipologia=VC")]
y = y[y.anio.between(2021, 2024)][["territorio_codigo", "anio", "valor"]].rename(columns={"valor": "y"})
y = y[y.y > 0]
y["ly"] = np.log(y.y)

p = y.merge(e, on=["territorio_codigo", "anio"], how="inner")
p = p[p.territorio_codigo.isin(ok)].dropna(subset=["ly", "x"]).copy()
p["mun"] = p.territorio_codigo.str[:5]
p["mun_anio"] = p.mun + "_" + p.anio.astype(str)


def prune(df):
    # elimina secciones con 1 obs; los singletons municipio-anio se conservan (absorbidos por el EF, no afectan a b)
    while True:
        n0 = len(df)
        df = df[df.groupby("territorio_codigo").ly.transform("size") > 1]
        if len(df) == n0:
            return df


p = prune(p)


def demean(v, g1, g2, tol=1e-12, it=5000):
    r = v.copy()
    for _ in range(it):
        old = r.copy()
        r = r - pd.Series(r).groupby(g1).transform("mean").values
        r = r - pd.Series(r).groupby(g2).transform("mean").values
        if np.max(np.abs(r - old)) < tol:
            break
    return r


g1 = p.territorio_codigo.values
g2 = p.mun_anio.values
# DT intra-seccion en la muestra de la especificacion
xw = p.x.values - p.groupby("territorio_codigo").x.transform("mean").values
sd = xw.std(ddof=1)
xs = p.x.values / sd
rx = demean(xs, g1, g2)
ry = demean(p.ly.values, g1, g2)
b = (rx @ ry) / (rx @ rx)
res = ry - b * rx
N = len(p)
secs = p.territorio_codigo.nunique()
muns = p.mun.nunique()
est = 100 * b  # % de alquiler por DT
ref = dict(estimacion_pct=0.00299, N=50846, secciones=12976, municipios=1523)
dif = est - ref["estimacion_pct"]
dN = (N - ref["N"]) / ref["N"]
veredicto = "COINCIDE" if abs(dif) <= 0.005 and abs(dN) <= 0.01 else "DISCREPA"
out = dict(
    id="h3", seed=SEED, datos="data/processed/v15/p5_turismo_seccion.parquet",
    metodo="OLS con EF seccion y municipio x anio (demeaning alterno); log SERPAVI VC sobre % VUT INE estandarizado por DT intra-seccion; 2021-2024; secciones con codigo en INE 2021 y 2024; sin secciones de 1 obs",
    N=int(N), secciones=int(secs), municipios=int(muns), dt_intra_seccion_pp=float(sd),
    estimacion_log=float(b), estimacion_pct_por_DT=float(est), ic95=None,
    inferencia="no apta (Conley y agrupado); solo puntual",
    comparacion=dict(referencia=ref, dif_abs_pp=float(dif), dif_N_rel=float(dN), veredicto=veredicto),
)
json.dump(out, open(os.path.join(OUT, "resultado.json"), "w"), indent=2, ensure_ascii=False)
print(json.dumps(out, indent=2, ensure_ascii=False))
