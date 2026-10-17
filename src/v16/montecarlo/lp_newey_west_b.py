"""V16 · fase 5 · Validación Monte Carlo de la proyección local con Newey-West de b fija (Kiefer-Vogelsang) sobre un choque exógeno i.i.d. (Q5-p, Q5-a).

Ejecución: python src/v16/montecarlo/lp_newey_west_b.py [--R 10000]   (SEED 20261010, k = 34)
Estructura real: solo T (≈ 100 trimestres, 2002T1-2026T2 = 98; se usa T = 100) y h = 1, 4, 8, 12. El choque y el resultado se SIMULAN.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_iv_espacial as C  # noqa: E402

HERR, K_SEM = "lp_newey_west_b", 34
T = 100
HORIZ = [1, 4, 8, 12]
RHOS = [0.90, 0.95, 0.98]
B_PRINCIPAL = 0.2
B_REF = [1.0]
SIG_U = 0.01
BETA_H4 = -0.006           # -0,6 % por DT de la sorpresa a h = 4 (magnitud de referencia de Q5-p)
NLAGS = 4
BURN = 100


def cv_fijo_b(b: float, n: int = 500, ndraw: int = 100_000) -> float:
    """Valor crítico bilateral al 5 % de la distribución límite de b fija con núcleo de Bartlett (KV 2005):
    t = W(1)/sqrt(Q(b)), Q(b) = (2/b)·[∫ B̃² − ∫_0^{1-b} B̃(r+b)B̃(r) dr], B̃ = puente browniano. Simulada con semilla fija."""
    g = C.rng(K_SEM, 999)
    m = int(round(b * n))
    out = []
    for _ in range(ndraw // 5000):
        dW = g.standard_normal((5000, n)) / np.sqrt(n)
        W = np.cumsum(dW, 1)
        r = np.arange(1, n + 1) / n
        Bt = W - r * W[:, -1:]
        i1 = (Bt ** 2).mean(1)
        i2 = (Bt[:, m:] * Bt[:, :n - m]).sum(1) / n if m < n else 0.0
        Q = (2 / b) * (i1 - i2)
        out.append(np.abs(W[:, -1]) / np.sqrt(Q))
    return float(np.quantile(np.concatenate(out), 0.95))


def dgp_texto(cv: dict) -> str:
    return f"""# lp_newey_west_b · Q5-p y Q5-a (proyección local nacional, Newey-West con b fija)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** serie nacional trimestral, T = {T} (la ventana de Q5 es 1999T1/2002T1-2026T2, 98-110 trimestres); horizontes h = {HORIZ}.
- **Choque:** ε_t i.i.d. N(0,1), exógeno (equivale a la sorpresa estandarizada de Jarociński-Karadi agregada a trimestre; sin autocorrelación ni heterocedasticidad).
- **Resultado:** y_t = ρ·y_(t-1) + θ·ε_t + σ_u·u_t, u_t i.i.d. N(0,1), σ_u = {SIG_U} (log, trimestral), con {BURN} periodos de calentamiento. ρ ∈ {RHOS} (persistencia alta, intervalo 0,90-0,98 de la tarea).
  Respuesta verdadera a h: β_h = θ·ρ^h. Nulo: θ = 0. Alternativa: θ = {BETA_H4}/ρ^4, de modo que β_4 = {BETA_H4} (−0,6 % por DT, magnitud de referencia de Q5-p) y β_h = θρ^h para el resto.
- **Estimación:** para cada h, MCO de y_(t+h) sobre constante, ε_t, {NLAGS} rezagos de ε y {NLAGS} rezagos de y (n = T − h − {NLAGS} observaciones). Coeficiente de interés: el de ε_t.
- **Inferencia principal:** Newey-West con núcleo de Bartlett y ancho de banda fijo M = b·n con b = {B_PRINCIPAL} (Kiefer-Vogelsang), valor crítico bilateral al 5 % de la distribución límite de b fija
  simulada (b = {B_PRINCIPAL}: {cv[B_PRINCIPAL]:.3f}). Declarado antes de simular; se informa también b = 1,0 (valor crítico {cv[1.0]:.3f}) y Newey-West convencional (M = 4, normal) como referencias, no candidatas.
- **Pocos clusters / dependencia transversal:** no aplica (serie nacional única). **T corto:** n entre 84 y 95.
- **Alternativa nombrada en el punto 3:** ninguna distinta (b fija es la principal). Si algún (ρ, h) falla, el veredicto es «NO APTO» para la combinación; con fallos «NO APTO → diseño solo descriptivo».
- **Criterio:** en cada una de las 12 combinaciones (ρ, h): tamaño en [0,04; 0,06] con R ≥ 2.000 (aquí R = 10.000, para que el error Monte Carlo ≈ 0,002 no domine el intervalo) y cobertura en [0,92; 0,97] bajo la alternativa.
  El veredicto global es APTO solo si pasan las 12 combinaciones.
"""


def hac_t(Xb, ub, M: float, coef: int = 1):
    """t de MCO con HAC Bartlett de ancho M real (pesos 1 - j/M para j < M). Xb: (nb,n,k), ub residuos (nb,n)."""
    nb, n, k = Xb.shape
    XtX = np.einsum("bti,btj->bij", Xb, Xb)
    inv = np.linalg.inv(XtX)
    v = Xb * ub[:, :, None]
    om = np.einsum("bti,btj->bij", v, v)
    jmax = int(np.ceil(M)) - 1
    for j in range(1, jmax + 1):
        w = 1 - j / M
        if w <= 0:
            break
        g = np.einsum("bti,btj->bij", v[:, j:], v[:, :-j])
        om += w * (g + g.transpose(0, 2, 1))
    V = inv @ om @ inv
    return np.sqrt(np.maximum(V[:, coef, coef], 1e-30))


def f_rep(rng, nb, rho=0.95, theta_alt=0.0, cv=None):
    eps = rng.standard_normal((nb, T + BURN))
    u = rng.standard_normal((nb, T + BURN))
    # respuesta acumulada del choque: s_t = ρ s_(t-1) + ε_t
    s = np.zeros((nb, T + BURN)); y0 = np.zeros((nb, T + BURN))
    for t in range(T + BURN):
        sp, yp = (s[:, t - 1], y0[:, t - 1]) if t else (0.0, 0.0)
        s[:, t] = rho * sp + eps[:, t]
        y0[:, t] = rho * yp + SIG_U * u[:, t]
    y0, s, eps = y0[:, BURN:], s[:, BURN:], eps[:, BURN:]
    res = []
    for scen, th in (("nulo", 0.0), ("alt", theta_alt)):
        y = y0 + th * s
        for h in HORIZ:
            idx = np.arange(NLAGS, T - h)
            yy = y[:, idx + h]
            cols = [np.ones((nb, len(idx))), eps[:, idx]]
            cols += [eps[:, idx - l] for l in range(1, NLAGS + 1)] + [y[:, idx - l] for l in range(1, NLAGS + 1)]
            X = np.stack(cols, 2)
            beta = np.linalg.solve(np.einsum("bti,btj->bij", X, X), np.einsum("bti,bt->bi", X, yy)[:, :, None])[:, :, 0]
            u_hat = yy - np.einsum("bti,bi->bt", X, beta)
            b1 = beta[:, 1]
            n = len(idx)
            verd = th * rho ** h
            for etiq, M, crit in (("b=0.2", B_PRINCIPAL * n, cv[B_PRINCIPAL]), ("b=1.0", 1.0 * n, cv[1.0]), ("NW M=4 normal", 4.0, 1.959964)):
                se = hac_t(X, u_hat, M)
                res.append((scen, h, etiq, b1, se, verd, crit))
    out = []
    for scen, h, etiq, b1, se, verd, crit in res:
        if scen == "nulo":
            out.append(np.column_stack([np.abs(b1) / se > crit, b1, se]))
        else:
            out.append(np.column_stack([np.abs(b1) / se > crit, np.abs(b1 - verd) / se <= crit, b1 - verd, se]))
    return np.column_stack(out)


def main(R: int = 10000):
    cv = {b: cv_fijo_b(b) for b in [B_PRINCIPAL] + B_REF}
    C.declarar_dgp(HERR, dgp_texto(cv))
    filas = []
    for rho in RHOS:
        theta = BETA_H4 / rho ** 4
        M = C.paralelo(f_rep, K_SEM * 10 + int(rho * 100) % 10 + int(rho * 100) // 10, R, n_jobs=4, n_trozos=40, rho=rho, theta_alt=theta, cv=cv)
        # reconstruir el orden de columnas: para cada escenario, h, etiqueta
        pos = 0
        datos = {}
        for scen in ("nulo", "alt"):
            for h in HORIZ:
                for etiq in ("b=0.2", "b=1.0", "NW M=4 normal"):
                    w = 3 if scen == "nulo" else 4
                    datos[(scen, h, etiq)] = M[:, pos:pos + w]
                    pos += w
        for h in HORIZ:
            for etiq in ("b=0.2", "b=1.0", "NW M=4 normal"):
                a, d = datos[("nulo", h, etiq)], datos[("alt", h, etiq)]
                tam, cob, pot = a[:, 0].mean(), d[:, 1].mean(), d[:, 0].mean()
                filas.append({"rho": rho, "h": h, "inferencia": etiq, "R": len(M), "tamano_5pct": tam, "tamano_ic95": str(C.ic_binomial(tam, len(M))),
                              "cobertura_95": cob, "potencia": pot, "sesgo": float(d[:, 2].mean()), "rmse": float(np.sqrt((d[:, 2] ** 2).mean())),
                              "beta_verdadero": theta * rho ** h})
    tab = pd.DataFrame(filas)
    pr = tab[tab.inferencia == "b=0.2"]
    fallos = {}
    for r in pr.itertuples():
        v = C.veredicto(r.tamano_5pct, int(r.R), r.cobertura_95)
        if v["veredicto"] != "APTO":
            fallos[f"rho={r.rho}, h={r.h}"] = v["fallos"]
    vf = "APTO" if not fallos else "NO APTO → diseño solo descriptivo"
    res = C.resultado_base("Q5-p / Q5-a (proyección local nacional)", f"T = {T}, h = {HORIZ}", "LP con Newey-West de b fija (b = 0,2, Bartlett)",
                           "simulados; solo T y horizontes de la pregunta")
    res["estimacion"] = {"beta_4_ref": BETA_H4}
    res["diagnosticos"] = {"veredicto": vf, "combinaciones_que_fallan": fallos, "n_combinaciones": len(pr), "cv_fijo_b": {str(k): v for k, v in cv.items()},
                           "tamano_min": float(pr.tamano_5pct.min()), "tamano_max": float(pr.tamano_5pct.max()),
                           "cobertura_min": float(pr.cobertura_95.min()), "cobertura_max": float(pr.cobertura_95.max()), "R": R, "semilla": C.SEED}
    res["notas"] = ["Sin alternativa nombrada para Q5 en el punto 3; b = 1,0 y NW convencional son solo referencias."]
    md = f"## Resultados (R = {R} por ρ; semilla {C.SEED}, k = {K_SEM})\n\n{C.md_tabla(tab)}\n\n**Veredicto: {vf}.**\n"
    if fallos:
        md += "\nCombinaciones (ρ, h) que fallan con b = 0,2:\n" + "".join(f"- {k}: {'; '.join(v)}\n" for k, v in fallos.items())
    C.escribir_salidas(HERR, res, tab, md)
    print(tab.to_string())
    print(vf)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=10000)
    main(ap.parse_args().R)
