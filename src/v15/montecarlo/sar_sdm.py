"""V15 fase 4.1 · E3: SAR, SEM y SDM con W de contigüidad y de distancia inversa (corte 25 km) en un corte transversal municipal;
pruebas sobre ρ (λ) y efectos directos/indirectos (LeSage-Pace).

Proceso generador declarado en docs/v15/validacion_montecarlo/sar_sdm.md ANTES de simular (el script lo escribe primero).
Uso: python src/v15/montecarlo/sar_sdm.py [--R 3000] [--jobs 4]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import stats
from scipy.optimize import minimize_scalar

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v15.montecarlo import _comun_v15 as C  # noqa: E402

HERR, K = "sar_sdm", 7
BETA = np.array([0.0, 0.5, -0.3])          # constante, x1, x2
THETA = np.array([0.3, -0.2])              # coeficientes de Wx1, Wx2 en el SDM
RHO_ALT = 0.4
KMAX = 60
Z = 1.959964

DGP = """# sar_sdm · E3: SAR, SEM y SDM con W de contigüidad y de distancia inversa (corte 25 km)

Herramienta de V15 (preregistro_v15.md E3 y sección 6; adenda 1 punto 18: periodos 2011-2019 y 2015-2024). Código: `src/v15/montecarlo/sar_sdm.py`; semilla `SeedSequence([20261010, 7, celda*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Estructura leída (códigos y geometría; ningún valor de resultado):** municipios de entrenamiento con SERPAVI en 2015 y en 2024 (corte transversal de Δlog 2015-2024; N ≈ 1.900 tras quitar los que no tienen vecinos), polígonos de `data/base/geo`.
  - **W de contigüidad (reina):** polígonos que comparten frontera o vértice, estandarizada por filas.
  - **W de distancia inversa con corte de 25 km:** w_ij = 1/d_ij si d_ij < 25 km (distancia entre centroides), estandarizada por filas.
  - Se descartan las islas (sin vecino en alguna de las dos matrices) para que ambas matrices usen la misma muestra.
- **Covariables fijas:** x1 y x2 = (I − 0,5 W)^(-1) N(0,1) estandarizadas (autocorrelación espacial moderada, como cualquier covariable municipal), constante; β = (0; 0,5; −0,3). X se fija en todas las réplicas (inferencia condicional en X).
- **Procesos:**
  - SAR: y = ρ W y + X β + ε.
  - SEM: y = X β + u, u = λ W u + ε.
  - SDM: y = ρ W y + X β + W X θ + ε, con θ = (0,3; −0,2).
  - Nulo: ρ = λ = 0 (en el SDM, ρ = 0 y θ = 0, de modo que el efecto indirecto es 0). Alternativa: ρ = λ = 0,4.
- **Errores:** ε_i ~ N(0, σ_i²). Escenario «heterocedástico» (principal): σ_i = exp(0,4 z_i − 0,08) con z_i ~ N(0,1) (heterogeneidad entre municipios); escenario «homocedástico» (diagnóstico): σ_i = 1.
- **Estimación:** máxima verosimilitud concentrada con log-determinante exacto por autovalores de W. Contrastes sobre ρ (λ): Wald con la curvatura numérica de la verosimilitud perfilada y razón de verosimilitudes (referencia). Moran de los residuos MCO con la media y la varianza exactas de Cliff-Ord para residuos de regresión.
- **Efectos (LeSage-Pace) en SAR y SDM para x1:** efecto directo = media de la diagonal de S(W), total = suma/N, indirecto = total − directo; trazas hasta el orden 60 de W; 1.000 simulaciones de (ρ, β[, θ]) de la normal con la covarianza del método delta (β(ρ) = b0 − ρ bL) y IC percentil. La verdad es el valor analítico en los parámetros del proceso. Tamaño del efecto indirecto bajo el nulo = rechazo de que el IC95 contiene 0.
- **R = 3.000 por celda.** Criterio: tamaño de las pruebas sobre ρ en [0,04; 0,06] y cobertura del IC95 de los efectos indirectos y de ρ en [0,92; 0,97] (escenario heterocedástico; el homocedástico es diagnóstico). El pre-registro no nombra alternativa para estas pruebas distinta de los errores de Conley sobre los coeficientes (fuera de este encargo).
"""


# ---------------------------------------------------------------------------------------------- estructura
def estructura():
    from shapely import wkb
    from shapely.strtree import STRtree
    p10 = pd.read_parquet(C.P15 / "p10_espacial.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable"])
    s = p10[(p10.nivel == "municipio") & (p10.variable == "serpavi_alquiler_m2_mediana") & p10.periodo.isin(["2015", "2024"])]
    n = s.groupby(s.territorio_codigo.astype(str).str.zfill(5)).periodo.nunique()
    cods = sorted(n[n == 2].index)
    g = pd.read_parquet(C.RAIZ / "data" / "base" / "geo" / "municipios.parquet", columns=["cod_municipio", "geometry"])
    g["cod"] = g.cod_municipio.astype(str).str.zfill(5)
    g = g[g.cod.isin(cods)].drop_duplicates("cod").sort_values("cod").reset_index(drop=True)
    geoms = [wkb.loads(b) for b in g.geometry]
    cen = np.array([[q.centroid.y, q.centroid.x] for q in geoms])
    tree = STRtree(geoms)
    n_ = len(g)
    A = np.zeros((n_, n_))
    for i, q in enumerate(geoms):
        for j in tree.query(q, predicate="intersects"):
            if j != i:
                A[i, j] = 1.0
    d = C.dist_km(cen)
    B = np.where((d < 25.0) & (d > 0), 1.0 / np.maximum(d, 1e-6), 0.0)
    ok = (A.sum(1) > 0) & (B.sum(1) > 0)
    # eliminar islas iterativamente (tras quitar unidades pueden quedar otras sin vecinos)
    while True:
        A2, B2 = A[np.ix_(ok, ok)], B[np.ix_(ok, ok)]
        ok2 = (A2.sum(1) > 0) & (B2.sum(1) > 0)
        if ok2.all():
            break
        idx = np.where(ok)[0]
        ok[idx[~ok2]] = False
    A, B = A[np.ix_(ok, ok)], B[np.ix_(ok, ok)]
    cods = list(g.cod[ok])
    sim = {nm: np.sqrt(M_.sum(1)) for nm, M_ in (("contigüidad", A), ("dist_inversa_25km", B))}
    return {"cods": cods, "n": len(cods), "W": {"contigüidad": A / A.sum(1, keepdims=True), "dist_inversa_25km": B / B.sum(1, keepdims=True)}, "sqrt_a": sim,
            "vecinos_medios": {"contigüidad": float(A.sum(1).mean()), "dist_inversa_25km": float((B > 0).sum(1).mean())}}


class Malla:
    """Cantidades fijas por (W, X). lam = autovalores reales de W (precalculados)."""

    def __init__(self, W: np.ndarray, X: np.ndarray, modelo: str, lam: np.ndarray):
        self.W, self.n = W, W.shape[0]
        self.lam = lam
        self.rmin, self.rmax = 1 / self.lam.min() + 1e-6, 1 / self.lam.max() - 1e-6
        self.q = np.array([np.mean(self.lam ** k) for k in range(KMAX + 2)])    # tr(W^k)/n
        self.modelo = modelo
        self.X = X
        self.Z = np.column_stack([X, W @ X[:, 1:]]) if modelo == "SDM" else X
        self.WX = W @ X
        self.Pz = np.linalg.solve(self.Z.T @ self.Z, self.Z.T)
        self.ZZinv = np.linalg.inv(self.Z.T @ self.Z)

    def res(self, v):      # residuo de MCO de v sobre Z
        return v - self.Z @ (self.Pz @ v)


def autovalores(W, sqrt_a):
    """W = D^-1 A con A simétrica: S = D^(1/2) W D^(-1/2) es simétrica y tiene los mismos autovalores (reales)."""
    S = (sqrt_a[:, None] * W) / sqrt_a[None, :]
    return np.linalg.eigvalsh((S + S.T) / 2)


# ---------------------------------------------------------------------------------------------- verosimilitudes
def ll_sar(rho, e0, eL, ld):
    sse = ((e0 - rho * eL) ** 2).sum()
    return -0.5 * len(e0) * np.log(sse / len(e0)) + ld(rho)


def max_perfil(f, lo, hi):
    r = minimize_scalar(lambda t: -f(t), bounds=(lo, hi), method="bounded", options={"xatol": 1e-7})
    return r.x, -r.fun


def hess_num(f, x, lo, hi, h=1e-3):
    a, b = max(lo, x - h), min(hi, x + h)
    if b - a < 1e-6:
        return np.nan
    return (f(a) - 2 * f(x) + f(b)) / (((b - a) / 2) ** 2)


def ajusta(M: Malla, y):
    n = M.n
    ld = lambda r: np.log1p(-r * M.lam).sum()
    if M.modelo in ("SAR", "SDM"):
        Wy = M.W @ y
        e0, eL = M.res(y), M.res(Wy)
        f = lambda r: ll_sar(r, e0, eL, ld)
        rho, l1 = max_perfil(f, M.rmin, M.rmax)
        l0 = f(0.0)
        h = hess_num(f, rho, M.rmin, M.rmax)
        se = 1 / np.sqrt(-h) if (h is not np.nan and h < 0) else np.nan
        b0 = M.Pz @ y
        bL = M.Pz @ Wy
        beta = b0 - rho * bL
        sig2 = ((e0 - rho * eL) ** 2).sum() / n
        return {"par": rho, "se": se, "lr": 2 * (l1 - l0), "b0": b0, "bL": bL, "beta": beta, "sig2": sig2}
    # SEM
    X, WX, Wy = M.X, M.WX, M.W @ y

    def sse(l):
        yt, Xt = y - l * Wy, X - l * WX
        b = np.linalg.solve(Xt.T @ Xt, Xt.T @ yt)
        r = yt - Xt @ b
        return float(r @ r)
    f = lambda l: -0.5 * n * np.log(sse(l) / n) + ld(l)
    lam, l1 = max_perfil(f, M.rmin, M.rmax)
    l0 = f(0.0)
    h = hess_num(f, lam, M.rmin, M.rmax)
    se = 1 / np.sqrt(-h) if (h is not np.nan and h < 0) else np.nan
    return {"par": lam, "se": se, "lr": 2 * (l1 - l0)}


# ---------------------------------------------------------------------------------------------- efectos
def efectos(M: Malla, ajuste, g, nsim=1000, cual=1):
    """Efectos directo, indirecto y total de x_cual por simulación (LeSage-Pace). Devuelve percentiles 2,5 / 97,5 del indirecto y del directo."""
    rho, se = ajuste["par"], ajuste["se"]
    if not np.isfinite(se):
        return None
    k = len(ajuste["beta"])
    cov_b = ajuste["sig2"] * M.ZZinv + np.outer(ajuste["bL"], ajuste["bL"]) * se ** 2
    cov = np.zeros((k + 1, k + 1))
    cov[:k, :k] = cov_b
    cov[:k, k] = cov[k, :k] = -ajuste["bL"] * se ** 2
    cov[k, k] = se ** 2
    mu = np.r_[ajuste["beta"], rho]
    d = g.multivariate_normal(mu, (cov + cov.T) / 2, size=nsim, method="eigh")
    r = np.clip(d[:, k], M.rmin, M.rmax)
    pw = r[:, None] ** np.arange(KMAX + 1)[None, :]
    d0 = pw @ M.q[:KMAX + 1]
    b1 = d[:, cual]
    if M.modelo == "SDM":
        th = d[:, 3 + (cual - 1)]
        d1 = pw @ M.q[1:KMAX + 2]
        dir_ = b1 * d0 + th * d1
        tot = (b1 + th) / (1 - r)
    else:
        dir_ = b1 * d0
        tot = b1 / (1 - r)
    ind = tot - dir_
    return np.quantile(ind, [0.025, 0.975]), np.quantile(dir_, [0.025, 0.975]), float(np.median(ind))


def verdad_efectos(M: Malla, rho, cual=1):
    pw = rho ** np.arange(KMAX + 1)
    d0 = pw @ M.q[:KMAX + 1]
    if M.modelo == "SDM":
        d1 = pw @ M.q[1:KMAX + 2]
        dir_ = BETA[cual] * d0 + THETA[cual - 1] * d1
        tot = (BETA[cual] + THETA[cual - 1]) / (1 - rho)
    else:
        dir_ = BETA[cual] * d0
        tot = BETA[cual] / (1 - rho)
    return dir_, tot - dir_


# ---------------------------------------------------------------------------------------------- Moran de residuos MCO
def moran_prep(W, X):
    n, k = X.shape
    Mx = np.eye(n) - X @ np.linalg.solve(X.T @ X, X.T)
    Ws = (W + W.T) / 2
    S0 = Ws.sum()
    MW = Mx @ Ws
    t1 = np.trace(MW)
    t2 = np.sum(MW * MW.T)                  # tr(MW MW)
    mean = n / S0 * t1 / (n - k)
    # Cliff-Ord: var = (n/S0)^2 [tr(MWMW) + tr((MW)(MW)') + tr(MW)^2] / ((n-k)(n-k+2)) - mean^2
    t3 = np.sum(MW * MW)                    # tr(MW (MW)')
    var = (n / S0) ** 2 * (t2 + t3 + t1 ** 2) / ((n - k) * (n - k + 2)) - mean ** 2
    return {"Mx": Mx, "Ws": Ws, "S0": S0, "mean": mean, "sd": np.sqrt(var)}


def moran_z(Mo, y):
    e = Mo["Mx"] @ y
    I = len(y) / Mo["S0"] * (e @ Mo["Ws"] @ e) / (e @ e)
    return (I - Mo["mean"]) / Mo["sd"]


# ---------------------------------------------------------------------------------------------- réplicas
def simula(M_true: dict, modelo, rho, hetero, X, g):
    n = X.shape[0]
    sig = np.exp(0.4 * g.standard_normal(n) - 0.08) if hetero else np.ones(n)
    eps = sig * g.standard_normal(n)
    if modelo == "SEM":
        u = M_true["inv"](rho) @ eps if rho != 0 else eps
        return X @ BETA + u
    xb = X @ BETA
    if modelo == "SDM":
        xb = xb + M_true["WX"][:, 1:] @ THETA
    return M_true["inv"](rho) @ (xb + eps) if rho != 0 else xb + eps


def rep(M: Malla, Mo, tru: dict, modelo, rho, hetero, g):
    X = M.X
    y = simula(tru, modelo, rho, hetero, X, g)
    a = ajusta(M, y)
    out = {"par": a["par"], "se": a["se"]}
    z = a["par"] / a["se"] if np.isfinite(a["se"]) else np.nan
    out["wald_rej"] = float(abs(z) > Z) if np.isfinite(z) else np.nan
    out["lr_rej"] = float(a["lr"] > stats.chi2.ppf(0.95, 1))
    out["wald_cov"] = float(abs(a["par"] - rho) <= Z * a["se"]) if np.isfinite(a["se"]) else np.nan
    out["moran_rej"] = float(abs(moran_z(Mo, y)) > Z)
    if modelo in ("SAR", "SDM"):
        ef = efectos(M, a, g)
        if ef is None:
            out.update({"ind_cov": np.nan, "ind_rej": np.nan, "dir_cov": np.nan})
        else:
            (ilo, ihi), (dlo, dhi), imed = ef
            vd, vi = tru["verdad"]
            out["ind_cov"] = float(ilo <= vi <= ihi)
            out["ind_rej"] = float(not (ilo <= 0 <= ihi))
            out["dir_cov"] = float(dlo <= vd <= dhi)
            out["ind_med"] = imed
    return out


def celda(args):
    nombre_W, modelo, hetero, rho, R, sub, Wm, X, lam, Mo = args
    M = Malla(Wm, X, modelo, lam)
    n = M.n
    I = np.eye(n)
    cache = {}

    def inv(r):
        if r not in cache:
            cache[r] = np.linalg.inv(I - r * Wm)
        return cache[r]
    tru = {"inv": inv, "WX": M.WX}
    if modelo in ("SAR", "SDM"):
        # en el SDM con nulo ρ = 0 los θ también son 0 (efecto indirecto nulo)
        pass
    if modelo == "SDM" and rho == 0.0:
        tru["WX"] = M.WX * 0.0
        tru["verdad"] = (BETA[1], 0.0)
    else:
        tru["verdad"] = verdad_efectos(M, rho) if modelo in ("SAR", "SDM") else (None, None)
    gens = C.flujos(K, R, sub)
    filas = [rep(M, Mo, tru, modelo, rho, hetero, g) for g in gens]
    return pd.DataFrame(filas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=3000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    C.declarar(HERR, DGP)
    E = estructura()
    n = E["n"]
    g0 = C.rng(K, 0)
    tareas, claves = [], []
    for iw, (nw, W) in enumerate(E["W"].items()):
        # X espacialmente autocorrelada (fija en todas las réplicas)
        Ainv = np.linalg.inv(np.eye(n) - 0.5 * W)
        lam = autovalores(W, E["sqrt_a"][nw])
        X = np.column_stack([np.ones(n)] + [(lambda v: (v - v.mean()) / v.std())(Ainv @ g0.standard_normal(n)) for _ in range(2)])
        Mo = moran_prep(W, X)
        for im, modelo in enumerate(("SAR", "SEM", "SDM")):
            for ih, hetero in enumerate((True, False)):
                for ir, (nom, rho) in enumerate((("nulo", 0.0), ("alt", RHO_ALT))):
                    sub = ((iw * 3 + im) * 2 + ih) * 2 + ir
                    # una tarea por celda y trozos de réplicas para paralelizar
                    nch = 6
                    per = [a.R // nch + (1 if i < a.R % nch else 0) for i in range(nch)]
                    for c, Rc in enumerate(per):
                        tareas.append((nw, modelo, hetero, rho, Rc, sub * 100 + c, W, X, lam, Mo))
                        claves.append((nw, modelo, "hetero" if hetero else "homo", nom, c))
    t0 = time.time()
    sal = Parallel(n_jobs=a.jobs)(delayed(celda)(t) for t in tareas)
    seg = time.time() - t0
    big = {}
    for k, d in zip(claves, sal):
        big.setdefault(k[:4], []).append(d)
    filas = []
    for k in sorted(set(k[:3] for k in big)):
        nw, modelo, err = k
        dn = pd.concat(big[k + ("nulo",)])
        da = pd.concat(big[k + ("alt",)])
        f = {"W": nw, "modelo": modelo, "errores": err, "R": len(dn),
             "tamano_wald_rho": float(dn.wald_rej.mean()), "tamano_lr_rho": float(dn.lr_rej.mean()), "tamano_moran": float(dn.moran_rej.mean()),
             "cobertura_rho": float(da.wald_cov.mean()), "potencia_wald_rho": float(da.wald_rej.mean()),
             "sesgo_rho": float((da.par - RHO_ALT).mean()), "rmse_rho": float(np.sqrt(((da.par - RHO_ALT) ** 2).mean()))}
        if modelo in ("SAR", "SDM"):
            f.update({"tamano_indirecto": float(dn.ind_rej.mean()), "cobertura_indirecto": float(da.ind_cov.mean()),
                      "cobertura_directo": float(da.dir_cov.mean()), "potencia_indirecto": float(da.ind_rej.mean())})
        filas.append(f)
    tab = pd.DataFrame(filas)
    ver = {}
    for _, f in tab[tab.errores == "hetero"].iterrows():
        v_rho = C.veredicto(float(f.tamano_wald_rho), float(f.cobertura_rho), int(f.R))
        v_ind = C.veredicto(float(f.tamano_indirecto), float(f.cobertura_indirecto), int(f.R)) if f.modelo in ("SAR", "SDM") else None
        ver[f"{f.modelo}|{f.W}"] = {"rho": v_rho, "indirecto": v_ind, "apto": bool(v_rho["apto"] and (v_ind is None or v_ind["apto"]))}
    glob = "APTO" if all(v["apto"] for v in ver.values()) else "NO APTO en: " + ", ".join(k for k, v in ver.items() if not v["apto"])
    r = C.base_resultado("E3 (SAR, SEM, SDM)", {"municipios": n, "vecinos_medios": E["vecinos_medios"]}, "ML concentrada, Wald/LR sobre ρ, efectos LeSage-Pace")
    h = tab[(tab.errores == "hetero")]
    r["estimacion"] = {"tamano_wald_rho_hetero": {f"{x.modelo}|{x.W}": float(x.tamano_wald_rho) for x in h.itertuples()},
                       "cobertura_indirecto_hetero": {f"{x.modelo}|{x.W}": float(x.cobertura_indirecto) for x in h.itertuples() if x.modelo != "SEM"},
                       "sesgo_rho": {f"{x.modelo}|{x.W}": float(x.sesgo_rho) for x in h.itertuples()},
                       "rmse_rho": {f"{x.modelo}|{x.W}": float(x.rmse_rho) for x in h.itertuples()}}
    r["ic95"] = None
    r["diagnosticos"] = {"veredicto": glob, "por_celda": ver, "R": a.R, "semilla": C.SEED, "N": n, "segundos": seg}
    r["notas"] = ["Veredicto sobre el escenario heterocedástico; el homocedástico es diagnóstico.", "X fija en todas las réplicas."]
    md = (f"## Resultados (R = {a.R} por celda; N = {n}; semilla {C.SEED}, k = {K})\n\n" + C.md_tabla(tab) + f"\n**Veredicto: {glob}.**\n\n")
    for kk, v in ver.items():
        md += f"- {kk}: ρ {v['rho']['veredicto']} {'; '.join(v['rho']['fallos'])} | indirecto {v['indirecto']['veredicto'] if v['indirecto'] else 'n/a'} {'; '.join(v['indirecto']['fallos']) if v['indirecto'] else ''}\n"
    C.cerrar(HERR, r, tab, md)
    print(tab.to_string())
    print(glob, round(seg))


if __name__ == "__main__":
    main()
