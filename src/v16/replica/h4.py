"""Replica ciega H4 (V16 fase 6.3): 2SLS shift-share municipal, SERPAVI VC.
Solo lee data/processed/v15/p4_inmigracion.parquet. SEED=20261010."""
import json
import os
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
R = "/home/user/Econometr-a"
OUT = f"{R}/output/v16/replica/h4"
os.makedirs(OUT, exist_ok=True)

d = pd.read_parquet(f"{R}/data/processed/v15/p4_inmigracion.parquet")
pad = d[(d.variable == "padron_municipal_nacionalidad") & (d.nivel == "municipio")].copy()
pad["nac"] = pad.desagregacion.str.replace("nacionalidad=", "", regex=False)
pad["year"] = pad.periodo.astype(int)
pad = pad[pad.periodo.str.fullmatch(r"\d{4}")]
W = pad.pivot_table(index=["territorio_codigo", "year"], columns="nac", values="valor", aggfunc="first")

AGG = ["Extranjera", "Total", "Española", "De Africa", "De América", "De Asia", "Europa (sin España)",
       "Oceanía y Apátridas", "País de Europa menos UE27_2020", "País de Europa menos UE28",
       "País de la UE27_2020 sin España", "País de la UE28 sin España"]
C28 = [c for c in W.columns if c not in AGG]
assert len(C28) == 28, C28
RES = ["Alemania", "Francia", "Italia", "Portugal", "Reino Unido"]
ORIG = [c for c in C28 if c not in RES]
BASE = 2003

munis = sorted(W.index.get_level_values(0).unique())
N = {c: W[c].unstack("year") for c in C28 + ["Extranjera", "Total"]}
tot = N["Total"]; ext = N["Extranjera"]

# cuotas base
S = pd.DataFrame({c: N[c][BASE] / tot[BASE] for c in ORIG})
# choques leave-one-out
years = list(range(2011, 2023))
Z = {}
for t in years:
    num = pd.DataFrame(index=munis)
    G = {}
    for c in ORIG:
        a1 = N[c][t]; a0 = N[c][t - 1]
        T1 = a1.sum(); T0 = a0.sum()
        n1 = T1 - a1; n0 = T0 - a0
        G[c] = (n1 - n0) / n0.replace(0, np.nan)
    G = pd.DataFrame(G)
    Z[t] = (S * G).sum(axis=1, min_count=1)
Z = pd.DataFrame(Z)
X = {t: 100 * (ext[t] - ext[t - 1]) / tot[t - 1] for t in years}
X = pd.DataFrame(X)

s = d[(d.variable == "serpavi_alquiler_m2_mediana") & (d.nivel == "municipio") &
      (d.desagregacion == "tipologia=VC") & d.periodo.str.fullmatch(r"\d{4}")]
P = s.pivot_table(index="territorio_codigo", columns=s.periodo.astype(int), values="valor")
P = P.where(P > 0)
Y = 100 * np.log(P).diff(axis=1)

rows = []
for t in range(2012, 2023):
    if t not in Y.columns:
        continue
    df = pd.DataFrame({"y": Y[t], "x": X[t], "z": Z[t]}).dropna()
    df["year"] = t
    df["muni"] = df.index
    rows.append(df)
D = pd.concat(rows)
D = D[~D.muni.isin(["08019", "46250"])]
cnt = D.groupby("muni").y.transform("size")
D = D[cnt >= 6].copy()
D["prov"] = D.muni.str[:2]
D["pv"] = D.prov + "_" + D.year.astype(str)


def demean(M, groups):
    """Absorbe efectos fijos (alternando proyecciones)."""
    M = M.copy()
    for _ in range(200):
        old = M.copy()
        for g in groups:
            M = M - M.groupby(g.values).transform("mean")
        if np.abs(M.values - old.values).max() < 1e-10:
            break
    return M


def fit(D, fe):
    V = D[["y", "x", "z"]]
    V = demean(V, fe(D)) if fe else V - V.mean()
    y, x, z = V.y.values, V.x.values, V.z.values
    ols = (x @ y) / (x @ x)
    pi = (z @ x) / (z @ z)
    xh = pi * z
    b = (xh @ y) / (xh @ x)
    F = pi ** 2 * (z @ z) / (((x - pi * z) ** 2).sum() / (len(x) - 1))
    return ols, b, F


res = {}
# principal: efectos de provincia x año (en diferencias, el efecto de municipio ya esta absorbido)
res["pv_anio"] = fit(D, lambda D: [D.pv])
res["pv_anio_mas_muni"] = fit(D, lambda D: [D.pv, D.muni])
res["anio"] = fit(D, lambda D: [D.year])
for k, v in res.items():
    print(k, v)

ols, b, F = res["pv_anio"]
out = {
    "id": "h4", "semilla": SEED,
    "N": int(len(D)), "municipios": int(D.muni.nunique()),
    "n_orig_instrumento": len(ORIG),
    "coef_2sls_pct_por_pp": float(b), "coef_ols_pct_por_pp": float(ols),
    "F_primera_etapa_simple": float(F),
    "variantes": {k: {"ols": float(v[0]), "2sls": float(v[1]), "F": float(v[2])} for k, v in res.items()},
    "referencia": {"2sls": 0.29, "ols": 0.07, "N": 13442, "municipios": 1276},
}
dif = b - 0.29
out["comparacion"] = {"dif_abs": float(dif), "dif_rel": float(dif / 0.29), "N_igual": bool(len(D) == 13442)}
out["veredicto"] = "COINCIDE" if (len(D) == 13442 and abs(dif / 0.29) <= 0.10) else "DISCREPA"
json.dump(out, open(f"{OUT}/resultado.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
