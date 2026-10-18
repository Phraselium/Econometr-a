"""Replica ciega E3 (P10): SAR por ML, W reina por filas, dlog SERPAVI VC 2015-2024."""
import json
import os
import numpy as np
import pandas as pd
import shapely
from shapely import wkb, wkt
from shapely.strtree import STRtree
from scipy import optimize, sparse

SEED = 20261010
np.random.seed(SEED)
RAIZ = str(__import__("pathlib").Path(__file__).resolve().parents[3])
OUT = f"{RAIZ}/output/v16/replica/e3"
os.makedirs(OUT, exist_ok=True)

d = pd.read_parquet(f"{RAIZ}/data/processed/v15/p10_espacial.parquet")
d = d[(d.desagregacion == "tipologia=VC")]
pr = d[d.variable == "serpavi_alquiler_m2_mediana"].pivot_table(
    index="territorio_codigo", columns="periodo", values="valor")
ct = d[d.variable == "serpavi_n_contratos_recuento"].pivot_table(
    index="territorio_codigo", columns="periodo", values="valor")
df = pd.DataFrame({"p0": pr["2015"], "p1": pr["2024"], "c0": ct["2015"]}).dropna()
df = df[(df.p0 > 0) & (df.p1 > 0) & (df.c0 > 0)]

g = pd.read_parquet(f"{RAIZ}/data/base/geo/municipios.parquet")[["cod_municipio", "geometry"]]
g = g[g.cod_municipio.isin(df.index)].drop_duplicates("cod_municipio").set_index("cod_municipio")
def geom(x):
    if isinstance(x, (bytes, bytearray)):
        return wkb.loads(bytes(x))
    if isinstance(x, str):
        try:
            return wkt.loads(x)
        except Exception:
            return wkb.loads(bytes.fromhex(x))
    return x
geoms = np.array([geom(x) for x in g.geometry], dtype=object)
geoms = np.array([shapely.make_valid(x) if not x.is_valid else x for x in geoms], dtype=object)
tree = STRtree(geoms)
i, j = tree.query(geoms, predicate="intersects")
m = i != j
A = sparse.coo_matrix((np.ones(m.sum()), (i[m], j[m])), shape=(len(g),) * 2).tocsr()
A.data[:] = 1.0
A = ((A + A.T) > 0).astype(float)
con = np.asarray(A.sum(1)).ravel() > 0
idx = g.index[con]
A = A[con][:, con]
df = df.loc[idx]
N = len(df)
deg = np.asarray(A.sum(1)).ravel()
W = sparse.diags(1 / deg) @ A
W = W.tocsr()
# autovalores via forma simetrica D^-1/2 A D^-1/2
S = (sparse.diags(deg ** -0.5) @ A @ sparse.diags(deg ** -0.5)).toarray()
eig = np.linalg.eigvalsh(S)

y = np.log(df.p1.values) - np.log(df.p0.values)
X = np.column_stack([np.ones(N), np.log(df.p0.values), np.log(df.c0.values)])
Wy = W @ y
b0 = np.linalg.lstsq(X, y, rcond=None)[0]
bL = np.linalg.lstsq(X, Wy, rcond=None)[0]
e0 = y - X @ b0
eL = Wy - X @ bL


def ll(rho):
    e = e0 - rho * eL
    s2 = e @ e / N
    return -N / 2 * np.log(s2) + np.sum(np.log(1 - rho * eig))


lo, hi = 1 / eig.min() + 1e-6, 1 / eig.max() - 1e-6
r = optimize.minimize_scalar(lambda t: -ll(t), bounds=(lo, hi), method="bounded",
                             options={"xatol": 1e-10})
rho = r.x
h = 1e-4
H = -(ll(rho + h) - 2 * ll(rho) + ll(rho - h)) / h ** 2
se = 1 / np.sqrt(H)
ic = [rho - 1.959964 * se, rho + 1.959964 * se]
beta = b0 - rho * bL

ref, ic_ref = 0.39, [0.34, 0.45]
dif = rho - ref
ov = max(0, min(ic[1], ic_ref[1]) - max(ic[0], ic_ref[0]))
solape = ov / min(ic[1] - ic[0], ic_ref[1] - ic_ref[0])
solape_union = ov / (max(ic[1], ic_ref[1]) - min(ic[0], ic_ref[0]))
ver = "COINCIDE" if abs(dif) <= 0.02 and solape > 0.8 else "DISCREPA"
res = {
    "id": "e3", "SEED": SEED, "N": int(N), "modelo": "SAR ML, W reina por filas, dlog SERPAVI VC 2015-2024",
    "rho": round(float(rho), 4), "se_wald": round(float(se), 4),
    "ic95_wald": [round(float(ic[0]), 4), round(float(ic[1]), 4)],
    "beta": dict(zip(["const", "log_alq_ini", "log_contratos_ini"], map(float, beta))),
    "referencia": {"rho": ref, "ic95": ic_ref},
    "dif_abs": round(float(dif), 4), "dif_rel": round(float(dif / ref), 4),
    "solape_ic_sobre_el_menor": round(float(solape), 3),
    "solape_ic_sobre_la_union": round(float(solape_union), 3),
    "rho_en_ic_ref": bool(ic_ref[0] <= rho <= ic_ref[1]),
    "ref_en_ic_propio": bool(ic[0] <= ref <= ic[1]),
    "veredicto": ver,
}
json.dump(res, open(f"{OUT}/resultado.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps(res, indent=2, ensure_ascii=False))
