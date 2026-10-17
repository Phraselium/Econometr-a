"""V16 · fase 5 · Validación Monte Carlo de la prueba conjunta de heterogeneidad BLP/GATES (Chernozhukov, Demirer, Duflo, Fernández-Val), R20.

Ejecución: python src/v16/montecarlo/blp_gates.py [--R 2000] [--S 11]   (SEED 20261010, k = 35)
Estructura real: municipios de entrenamiento con SERPAVI de alquiler (€/m2, mediana) en 2021 y 2024 (solo disponibilidad) y su provincia (cluster).
Moderadores, tratamiento y resultado se SIMULAN.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import ExtraTreesRegressor

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_iv_espacial as C  # noqa: E402

HERR, K_SEM = "blp_gates", 35
SIG, TAU0, TAU_HET = 0.08, 0.03, 0.03      # DT del ruido, efecto medio, amplitud de la heterogeneidad (alternativa)
P_TRAT = 0.5
KG = 5
MODERADORES = ["renta", "poblacion", "pct_extranjeros", "pct_vut", "obra_nueva_pc"]


def estructura() -> dict:
    a = pd.read_parquet(C.ENT / "base_alquiler.parquet", columns=["variable", "nivel", "territorio_codigo", "periodo", "valor"])
    a = a[(a.nivel == "municipio") & (a.variable == "serpavi_alquiler_m2_mediana") & a.periodo.isin(["2021", "2024"]) & a.valor.notna()]
    ok = a.groupby("territorio_codigo").periodo.nunique()
    cod = np.array(sorted(ok[ok == 2].index))
    prov = pd.factorize(pd.Series(cod).str[:2])[0]
    return {"N": len(cod), "G": int(prov.max() + 1), "prov": prov}


def dgp_texto(e: dict, S: int) -> str:
    return f"""# blp_gates · prueba conjunta de heterogeneidad BLP/GATES (una por pregunta con diseño; R20)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** {e['N']:,} municipios de entrenamiento con SERPAVI de alquiler en 2021 y 2024 (solo disponibilidad del dato) en {e['G']} provincias (clusters de tamaño real, de 1 a {int(np.bincount(e['prov']).max())}).
- **Moderadores (fijados por la adenda):** renta media, población, % de extranjeros, % de vivienda turística y obra nueva per cápita. Se simulan con una cópula gaussiana (correlación 0,3 entre moderadores)
  con un 30 % de la varianza común dentro de la provincia; marginales: renta lognormal, población lognormal de cola pesada, % de extranjeros beta, % VUT con cero en el 40 % y lognormal en el resto, obra nueva gamma. Se estandarizan para el efecto.
- **Tratamiento:** asignado por provincia (cluster) al azar con probabilidad p = {P_TRAT} (conocida): estructura de pocos clusters, como las preguntas de diseño por CCAA/provincia.
- **Resultado (Δlog, un periodo):** Y_i = g(Z_i) + v_prov(i) + τ(Z_i)·D_i + {SIG}·ε_i, con g no lineal (suma de efectos suaves y una interacción), v_prov ~ N(0,{SIG * 0.6:.3f}²) (choque de provincia), ε ~ N(0,1).
  **Nulo (efecto homogéneo):** τ(Z) = {TAU0}. **Alternativa (heterogeneidad):** τ(Z) = {TAU0} + {TAU_HET}·h(Z), h = combinación estandarizada de pct_vut (no lineal) y renta (media 0, DT 1).
- **Procedimiento:** {S} particiones aleatorias de las PROVINCIAS (mitad auxiliar A, mitad principal M; partir por cluster evita fugas). En A: ExtraTrees (60 árboles, hoja ≥ 15) por brazo → B(Z) = m0(Z), S(Z) = m1(Z) − m0(Z).
  En M: BLP: Y ~ 1 + B + S + (D−p) + (D−p)(S−S̄), ponderado 1/(p(1−p)); GATES: Y ~ 1 + B + S + Σ_k γ_k (D−p)·1(S ∈ cuantil k), K = {KG}. Covarianza CR1 por provincia (en M).
- **Prueba conjunta (principal):** Wald de igualdad de los {KG} GATES (γ1 = … = γ{KG}), referencia F(4, G_M − 1). Agregación entre particiones (CDDF): p = min(1, 2·mediana de los p). Secundarias informadas: BLP β2 = 0 y γ5 = γ1.
  IC del efecto medio (β1 del BLP): por partición al 97,5 % con t(G_M − 1), mediana de los límites (ajuste CDDF); cobertura frente al efecto medio poblacional τ0 = {TAU0} (la heterogeneidad h tiene media 0).
- **Alternativa nombrada en el punto 3:** ninguna (la prueba conjunta se adopta tal cual). Si no pasa → «NO APTO → diseño solo descriptivo» (los subgrupos ya son descriptivos C4).
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 bajo efecto homogéneo, cobertura del IC del efecto medio en [0,92; 0,97]; se informa la potencia bajo la alternativa. Un tamaño de 0,0 es NO APTO.
"""


def moderadores(rng, e, n_extra=None):
    N, G, prov = e["N"], e["G"], e["prov"]
    L = np.full((5, 5), 0.3) + 0.7 * np.eye(5)
    Lc = np.linalg.cholesky(L)
    zp = rng.standard_normal((G, 5))[prov]
    z = (np.sqrt(0.3) * zp + np.sqrt(0.7) * rng.standard_normal((N, 5))) @ Lc.T
    u = stats.norm.cdf(z)
    renta = np.exp(0.3 * z[:, 0])
    pob = np.exp(1.5 * z[:, 1])
    ext = stats.beta.ppf(u[:, 2], 2, 14)
    vut = np.where(u[:, 3] < 0.4, 0.0, np.exp(0.8 * stats.norm.ppf((u[:, 3] - 0.4) / 0.6 * 0.999 + 0.0005)))
    obra = stats.gamma.ppf(u[:, 4], 2, scale=1.0)
    Z = np.column_stack([renta, pob, ext, vut, obra])
    zs = (Z - Z.mean(0)) / Z.std(0)
    return Z, zs


def cr1_cov(X, res, cl, Gc, w):
    k = X.shape[1]
    XtWX = (X * w[:, None]).T @ X
    inv = np.linalg.inv(XtWX)
    sc = np.zeros((Gc, k))
    np.add.at(sc, cl, X * (w * res)[:, None])
    meat = sc.T @ sc
    n = len(res)
    f = Gc / (Gc - 1) * (n - 1) / (n - k)
    return inv @ meat @ inv * f


def una_particion(rng, Z, zs, Y, D, prov, G, S_unused=None):
    provs = rng.permutation(G)
    inA = np.isin(prov, provs[: G // 2])
    A, M = np.where(inA)[0], np.where(~inA)[0]
    kw = dict(n_estimators=60, min_samples_leaf=15, max_features=0.6, n_jobs=1, random_state=int(rng.integers(1 << 31)))
    m1 = ExtraTreesRegressor(**kw).fit(Z[A][D[A] == 1], Y[A][D[A] == 1]) if (D[A] == 1).sum() > 30 else None
    m0 = ExtraTreesRegressor(**kw).fit(Z[A][D[A] == 0], Y[A][D[A] == 0]) if (D[A] == 0).sum() > 30 else None
    if m1 is None or m0 is None:
        return None
    B = m0.predict(Z[M]); Sx = m1.predict(Z[M]) - B
    Sx = Sx + 1e-9 * rng.standard_normal(len(Sx))             # desempata si el proxy es casi constante
    d, y = D[M].astype(float), Y[M]
    cl = pd.factorize(prov[M])[0]; Gm = cl.max() + 1
    if Gm < 8:
        return None
    w = np.full(len(M), 1 / (P_TRAT * (1 - P_TRAT)))
    dc = d - P_TRAT
    # BLP
    X = np.column_stack([np.ones(len(M)), B, Sx, dc, dc * (Sx - Sx.mean())])
    b = np.linalg.solve((X * w[:, None]).T @ X, (X * w[:, None]).T @ y)
    V = cr1_cov(X, y - X @ b, cl, Gm, w)
    se = np.sqrt(np.diag(V))
    p_b2 = 2 * stats.t.sf(abs(b[4] / se[4]), Gm - 1)
    tq = stats.t.ppf(0.9875, Gm - 1)
    ic = (b[3] - tq * se[3], b[3] + tq * se[3])
    # GATES
    q = np.quantile(Sx, np.linspace(0, 1, KG + 1)[1:-1])
    g = np.searchsorted(q, Sx)
    Gd = np.column_stack([dc * (g == k) for k in range(KG)])
    X2 = np.column_stack([np.ones(len(M)), B, Sx, Gd])
    b2 = np.linalg.solve((X2 * w[:, None]).T @ X2, (X2 * w[:, None]).T @ y)
    V2 = cr1_cov(X2, y - X2 @ b2, cl, Gm, w)
    gam = b2[3:]; Vg = V2[3:, 3:]
    Rm = np.zeros((KG - 1, KG)); Rm[:, 0] = -1; Rm[np.arange(KG - 1), np.arange(1, KG)] = 1
    r = Rm @ gam
    try:
        W = float(r @ np.linalg.solve(Rm @ Vg @ Rm.T, r))
    except np.linalg.LinAlgError:
        return None
    p_joint = float(stats.f.sf(W / (KG - 1), KG - 1, Gm - 1))
    dd = gam[-1] - gam[0]
    sd = np.sqrt(Vg[-1, -1] + Vg[0, 0] - 2 * Vg[0, -1])
    p_51 = 2 * stats.t.sf(abs(dd / sd), Gm - 1)
    return p_joint, p_b2, p_51, ic[0], ic[1], b[3]


def f_rep(rng, nrep, e=None, S=11):
    N, G, prov = e["N"], e["G"], e["prov"]
    out = np.zeros((nrep, 12))
    for r in range(nrep):
        Z, zs = moderadores(rng, e)
        gz = 0.05 * zs[:, 0] + 0.04 * np.tanh(zs[:, 1]) + 0.03 * zs[:, 3] * (zs[:, 2] > 0) + 0.02 * zs[:, 4] ** 2
        v = SIG * 0.6 * rng.standard_normal(G)[prov]
        Dg = (rng.permutation(G) < G // 2) if True else None
        D = Dg[prov].astype(int)
        hz = (np.log1p(Z[:, 3]) * 1.0 + 0.5 * zs[:, 0])
        hz = (hz - hz.mean()) / hz.std()
        eps = SIG * rng.standard_normal(N)
        fila = []
        for tau in (TAU0 + 0 * hz, TAU0 + TAU_HET * hz):
            Y = gz + v + tau * D + eps
            res = [una_particion(rng, Z, zs, Y, D, prov, G) for _ in range(S)]
            res = [x for x in res if x is not None]
            if len(res) < max(3, S // 2):
                fila += [np.nan] * 6
                continue
            a = np.array(res)
            pj, pb, p51 = [min(1.0, 2 * np.median(a[:, i])) for i in range(3)]
            lo, hi = np.median(a[:, 3]), np.median(a[:, 4])
            fila += [pj, pb, p51, lo, hi, np.median(a[:, 5])]
        out[r, :12] = fila
    return out


def main(R: int = 2000, S: int = 11):
    e = estructura()
    C.declarar_dgp(HERR, dgp_texto(e, S))
    M = C.paralelo(f_rep, K_SEM, R, n_jobs=4, n_trozos=40, e=e, S=S)
    M = M[~np.isnan(M).any(1)]
    Rv = len(M)
    nul, alt = M[:, :6], M[:, 6:]
    filas = []
    for j, nm in enumerate(["conjunta: igualdad de los 5 GATES (principal)", "BLP beta2 = 0 (secundaria)", "GATES gamma5 = gamma1 (secundaria)"]):
        tam = (nul[:, j] < 0.05).mean(); pot = (alt[:, j] < 0.05).mean()
        filas.append({"prueba": nm, "R": Rv, "tamano_5pct": tam, "tamano_ic95": str(C.ic_binomial(tam, Rv)), "potencia_heterogeneidad": pot,
                      "cobertura_ate_95": float(((alt[:, 3] <= TAU0) & (TAU0 <= alt[:, 4])).mean()) if j == 0 else float("nan"),
                      "sesgo_ate": float((alt[:, 5] - TAU0).mean()) if j == 0 else float("nan"),
                      "rmse_ate": float(np.sqrt(((alt[:, 5] - TAU0) ** 2).mean())) if j == 0 else float("nan")})
    tab = pd.DataFrame(filas)
    cob = float(((nul[:, 3] <= TAU0) & (TAU0 <= nul[:, 4])).mean())
    p0 = tab.iloc[0]
    v = C.veredicto(float(p0.tamano_5pct), Rv, cob)
    vf = "APTO" if v["veredicto"] == "APTO" else "NO APTO → diseño solo descriptivo"
    res = C.resultado_base("R20 (prueba conjunta BLP/GATES)", f"{e['N']} municipios, {e['G']} provincias, {S} particiones",
                           "BLP/GATES con ExtraTrees, partición por provincia, Wald de igualdad de GATES, agregación 2×mediana", "simulados; estructura real (municipios y provincias)")
    res["estimacion"] = {"tau0": TAU0, "sesgo_ate": float(p0.sesgo_ate), "rmse_ate": float(p0.rmse_ate)}
    res["diagnosticos"] = {"veredicto": vf, "criterio": v, "tamano": float(p0.tamano_5pct), "cobertura_ate_nulo": cob,
                           "cobertura_ate_alt": float(p0.cobertura_ate_95), "potencia": float(p0.potencia_heterogeneidad), "R_validas": Rv, "R_pedidas": R, "S": S, "semilla": C.SEED}
    res["notas"] = ["La cobertura del criterio se mide en el escenario de efecto homogéneo (la del efecto medio bajo heterogeneidad se informa aparte)."]
    md = (f"## Resultados (R = {Rv} réplicas válidas de {R}, S = {S} particiones; semilla {C.SEED}, k = {K_SEM})\n\n{C.md_tabla(tab)}\n\n"
          f"Cobertura del IC 95 % del efecto medio bajo efecto homogéneo: {cob:.4f}.\n\n**Veredicto: {vf}.**\n")
    if v["fallos"]:
        md += "\nCondición que falla: " + "; ".join(v["fallos"]) + ".\n"
    C.escribir_salidas(HERR, res, tab, md)
    print(tab.to_string(), cob)
    print(vf)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--S", type=int, default=11)
    a = ap.parse_args()
    main(a.R, a.S)
