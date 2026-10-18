"""Replica ciega Q9-g: GSADF sobre el factor comun de ln(valor tasado) - ln(IPC alquiler)."""
import json
import numpy as np
import pandas as pd

SEED = 20261010
B = 499
BASE = "/home/user/Econometr-a/"
ENT = BASE + "data/processed/v16/entrenamiento/"


def cargar():
    p = pd.read_parquet(ENT + "base_precio.parquet")
    a = pd.read_parquet(ENT + "base_alquiler.parquet")
    p = p[(p.variable == "valor_tasado") & (p.nivel == "provincia") & (p.frecuencia == "T")]
    a = a[(a.variable == "ipc_alquiler_indice") & (a.nivel == "provincia") & (a.frecuencia == "T")]
    per = [f"{y}T{q}" for y in range(2002, 2027) for q in range(1, 5)][:98]
    P = p.pivot_table(index="periodo", columns="territorio_codigo", values="valor").reindex(per)
    A = a.pivot_table(index="periodo", columns="territorio_codigo", values="valor").reindex(per)
    cols = [c for c in P.columns if c in A.columns and P[c].notna().all() and A[c].notna().all()]
    R = np.log(P[cols]) - np.log(A[cols])
    return R, per


def factor(R):
    X = R.values
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    u, s, vt = np.linalg.svd(Z, full_matrices=False)
    f = u[:, 0] * s[0]
    if np.corrcoef(f, Z.mean(1))[0, 1] < 0:
        f = -f
    return f


def gsadf(y, r0):
    """Sup de t-ADF (constante, sin rezagos) sobre ventanas con >= r0 observaciones."""
    T = len(y)
    x = y[:-1]
    d = np.diff(y)
    def cs(v):
        return np.concatenate([[0.0], np.cumsum(v)])
    Sx, Sd, Sxx, Sdd, Sxd = cs(x), cs(d), cs(x * x), cs(d * d), cs(x * d)
    best = -np.inf
    for s in range(0, T - r0 + 1):
        e = np.arange(s + r0 - 1, T)       # ultimo indice de y de la ventana
        n = e - s                          # numero de observaciones de la regresion
        i0, i1 = s, e                      # d indices s..e-1
        sx = Sx[i1] - Sx[i0]; sd = Sd[i1] - Sd[i0]
        sxx = Sxx[i1] - Sxx[i0]; sdd = Sdd[i1] - Sdd[i0]; sxd = Sxd[i1] - Sxd[i0]
        mx, md = sx / n, sd / n
        cxx = sxx - n * mx * mx
        cxd = sxd - n * mx * md
        cdd = sdd - n * md * md
        beta = cxd / cxx
        sse = cdd - beta * cxd
        se = np.sqrt(np.maximum(sse, 1e-300) / (n - 2) / cxx)
        best = max(best, np.max(beta / se))
    return best


def main():
    R, per = cargar()
    f = factor(R)
    T = len(f)
    r0 = int(np.floor(T * (0.01 + 1.8 / np.sqrt(T))))
    est = gsadf(f, r0)
    rng = np.random.default_rng([SEED, 9])
    d = np.diff(f)
    stats = np.empty(B)
    for b in range(B):
        w = rng.standard_normal(len(d))
        ys = np.concatenate([[f[0]], f[0] + np.cumsum(d * w)])
        stats[b] = gsadf(ys, r0)
    vc = float(np.quantile(stats, 0.95))
    pv = float((1 + np.sum(stats >= est)) / (B + 1))
    ref = dict(provincias=33, T=98, gsadf=5.92, vc95=3.34, B=499, p=0.004)
    dif = est - ref["gsadf"]
    rel = dif / ref["gsadf"]
    concl_mia = bool(est > vc)
    concl_ref = ref["gsadf"] > ref["vc95"]
    coincide = abs(rel) <= 0.05 and concl_mia == concl_ref
    res = dict(
        id="q9g", semilla=SEED, N_provincias=int(R.shape[1]), T=int(T), r0=r0, B=B,
        gsadf=float(est), vc95_bootstrap=vc, p_bootstrap=pv, rechaza_5pct=concl_mia,
        var_explicada_pc1=float(np.linalg.svd((R.values - R.values.mean(0)) / R.values.std(0, ddof=1), compute_uv=False)[0] ** 2 / R.shape[1] / (T - 1) * (T - 1) / (T - 1) ** 0 / (T - 1) * (T - 1)) if False else None,
        referencia=ref, dif_abs=float(dif), dif_rel=float(rel),
        veredicto="COINCIDE" if coincide else "DISCREPA",
        notas="ratio ln valor_tasado - ln ipc_alquiler_indice, provincias con 98 trimestres completos 2002T1-2026T2; PC1 estandarizada; GSADF constante sin rezagos; bootstrap salvaje bajo raiz unitaria sin deriva.",
    )
    with open(BASE + "output/v16/replica/q9g/resultado.json", "w") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
