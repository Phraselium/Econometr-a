"""V15 fase 4.1 · E1: Westerlund (bootstrap), CIPS y CS-ARDL con N ≈ 40 provincias y T ≈ 98 trimestres con factor común.
Potencia frente a una velocidad de ajuste de −0,04 trimestral (umbral de V15: si la potencia no llega a 0,5, E1 se reporta solo como descriptiva).

Proceso generador declarado en docs/v15/validacion_montecarlo/westerlund_csardl.md ANTES de simular (el script lo escribe primero).
Uso: python src/v15/montecarlo/westerlund_csardl.py [--R 2000] [--R_alt 1000] [--B 99] [--jobs 4]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v15.montecarlo import _comun_v15 as C  # noqa: E402

HERR, K = "westerlund_csardl", 6
N, T = 40, 98
ALFA_MEDIA, ALFA_SD_HALF = -0.04, 0.02       # α_i ~ U(−0,06; −0,02)
BETA_LP, BETA_SD = 0.8, 0.2
PT = int(np.floor(T ** (1 / 3)))                 # 4 rezagos de las medias transversales
BLOQUE = int(round(2 * T ** (1 / 3)))            # 9

DGP = """# westerlund_csardl · E1: Westerlund con bootstrap, CIPS y CS-ARDL (N = 40, T = 98, factor común)

Herramienta de V15 (preregistro_v15.md E1 y sección 6). Código: `src/v15/montecarlo/westerlund_csardl.py`; semilla `SeedSequence([20261010, 6, etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Dimensiones (estructura de E1):** N = 40 provincias de entrenamiento (41 con IPC de alquiler; 38 con valor tasado), T = 98 trimestres (alquiler desde 2002T1 hasta 2026T2); 50 trimestres de rodaje descartados.
- **Regresor (log IPC de alquiler simulado), I(1) con factor común:** Δx_it = 0,2 + 0,5 γx_i f1_t + u_it, con f1 AR(1) (ρ = 0,5), γx_i ~ N(1; 0,5²) y u_it = e_it + 0,25 (e_{i−1,t} + e_{i+1,t}) (correlación espacial en anillo; e ~ N(0; 0,8²)).
- **Resultado (log valor tasado simulado):** y_it = β_i x_it + z_it, con β_i ~ N(0,8; 0,2²) (elasticidad de largo plazo por unidad; la verdad es su media muestral) y z_it = ρ_i z_{i,t−1} + 0,5 c_i f2_t + 0,7 e'_it (f2 segundo factor común AR(1) con ρ = 0,5 en las innovaciones, c_i ~ N(1; 0,5²), e' con el mismo anillo espacial). El factor común entra en las innovaciones (incrementos persistentes, como el crecimiento del precio), no como componente estacionario de nivel.
- **Nota de revisión (declarada):** la primera versión del proceso añadía además un componente estacionario de nivel λ_i f2_t en y_it. Eso crea una raíz de media móvil negativa en Δy, que ningún contraste tipo ADF con un rezago maneja (distorsión de tamaño conocida) y no se parece al crecimiento observado del precio (autocorrelación positiva). Con esa versión el tamaño del bootstrap de Westerlund salió 0,56 (Gτ), 0,72 (Gα), 0,50 (Pτ) y 0,65 (Pα), el de CIPS 0,0125 y la cobertura de CS-ARDL 0,9925. Se sustituyó por el proceso anterior de este párrafo antes de interpretar nada más; ambos resultados se declaran aquí.
  - **Nulo (sin cointegración):** ρ_i = 1 (z es I(1): regresión espuria con dependencia transversal).
  - **Alternativa (cointegración):** ρ_i = 1 + α_i con α_i ~ U(−0,06; −0,02), media −0,04 (velocidad de ajuste trimestral de referencia del pre-registro; semivida ≈ 17 trimestres).
- **Westerlund (2007):** modelo de corrección de errores por unidad Δy_s = δ_i + α_i y_{s−1} + λ_i x_{s−1} + a_i Δy_{s−1} + b_i Δx_s + b'_i Δx_{s−1} + e (1 rezago, sin adelantos) y estadísticos Gτ, Gα, Pτ, Pα (agrupados con las variables auxiliares eliminadas por unidad). **Valores p por bootstrap de Westerlund:** VAR(1) de (Δy, Δx) por unidad bajo el nulo; remuestreo de los residuos con el MISMO índice temporal para todas las unidades (conserva la dependencia transversal), reconstrucción en niveles y recálculo; contraste de cola izquierda; B = 99 réplicas (con B = 99 el contraste al 5 % es exacto: rango ≥ 95 de 100). El estadístico principal declarado es **Gτ** (admite heterogeneidad); los otros tres se reportan.
- **CIPS (Pesaran 2007):** CADF con intercepto, 1 rezago y medias transversales, media de los t. **Tamaño:** sobre la serie x (I(1) con factor), en todas las réplicas. **Potencia:** panel estacionario con φ_i ~ U(0,94; 0,98) (velocidad de ajuste media −0,04) con factor común, 1.000 réplicas. Valor crítico por bootstrap de bloques móviles de las diferencias (conjunto entre unidades, longitud 9), B = 199, raíz unitaria impuesta.
- **CS-ARDL (Chudik-Pesaran 2015):** ARDL(1,1) por unidad aumentado con las medias transversales de y y x y sus 4 rezagos (⌊T^(1/3)⌋); elasticidad de largo plazo θ = media de (b0 + b1)/(1 − φ) y velocidad de ajuste media φ − 1, sobre la alternativa (cointegración). Inferencia: bootstrap de bloques móviles (longitud 9) de las filas de regresión conjuntas, B = 99, IC normal con EE bootstrap. Cobertura de la media muestral de β_i y de la velocidad media verdadera; tamaño = 1 − cobertura.
- **Criterio:** tamaño en [0,04; 0,06] con R = 2.000 (Gτ, CIPS) y cobertura del IC95 de CS-ARDL en [0,92; 0,97]. Umbral de V15: potencia de Westerlund (Gτ) frente a −0,04 ≥ 0,5; si no, E1 solo descriptiva (independiente del veredicto de tamaño). El pre-registro no nombra inferencia alternativa para estas herramientas: si no pasan, «NO APTO → solo descriptivo».
"""


# ------------------------------------------------------------------------------------------ generador
def anillo(e):
    return e + 0.25 * (np.roll(e, 1, 0) + np.roll(e, -1, 0))


def panel(g, coint):
    n = T + 50
    f = np.zeros((2, n))
    ef = g.standard_normal((2, n))
    for t in range(1, n):
        f[:, t] = 0.5 * f[:, t - 1] + ef[:, t]
    gx = g.normal(1.0, 0.5, N)
    u = anillo(0.8 * g.standard_normal((N, n)))
    dx = 0.2 + 0.5 * gx[:, None] * f[0][None, :] + u
    x = np.cumsum(dx, axis=1)
    beta = g.normal(BETA_LP, BETA_SD, N)
    c = g.normal(1.0, 0.5, N)
    e2 = anillo(g.standard_normal((N, n)))
    rho = 1 + g.uniform(-0.06, -0.02, N) if coint else np.ones(N)
    z = np.zeros((N, n))
    for t in range(1, n):
        z[:, t] = rho * z[:, t - 1] + 0.5 * c * f[1, t] + 0.7 * e2[:, t]
    y = beta[:, None] * x + z
    return y[:, 50:], x[:, 50:], float(beta.mean()), float((rho - 1).mean())


def panel_estacionario(g):
    n = T + 50
    f = np.zeros(n)
    ef = g.standard_normal(n)
    for t in range(1, n):
        f[t] = 0.5 * f[t - 1] + ef[t]
    gam = g.normal(1.0, 0.5, N)
    phi = g.uniform(0.94, 0.98, N)
    e = anillo(g.standard_normal((N, n)))
    s = np.zeros((N, n))
    for t in range(1, n):
        s[:, t] = phi * s[:, t - 1] + gam * f[t] + 0.7 * e[:, t]
    return s[:, 50:] + g.normal(0, 1, N)[:, None]


# ------------------------------------------------------------------------------------------ Westerlund
def _solve(Xtx, Xty):
    return np.linalg.solve(Xtx, Xty[..., None])[..., 0]


def west_stats(y, x):
    s = np.arange(2, y.shape[1])
    dy = np.diff(y, axis=1)             # dy[:, j] = y[j+1] - y[j]
    dx = np.diff(x, axis=1)
    n = len(s)
    one = np.ones((y.shape[0], n))
    Xo = np.stack([one, x[:, s - 1], dy[:, s - 2], dx[:, s - 1], dx[:, s - 2]], axis=2)    # auxiliares (const, x_{s-1}, Δy_{s-1}, Δx_s, Δx_{s-1})
    ry = y[:, s - 1]
    rd = dy[:, s - 1]
    XtX = np.einsum("nti,ntj->nij", Xo, Xo)
    Pinv = np.linalg.inv(XtX)
    b_y = np.einsum("nij,nj->ni", Pinv, np.einsum("nti,nt->ni", Xo, ry))
    b_d = np.einsum("nij,nj->ni", Pinv, np.einsum("nti,nt->ni", Xo, rd))
    ty = ry - np.einsum("nti,ni->nt", Xo, b_y)
    td = rd - np.einsum("nti,ni->nt", Xo, b_d)
    syy = (ty ** 2).sum(1)
    al = (ty * td).sum(1) / syy
    e = td - al[:, None] * ty
    s2 = (e ** 2).sum(1) / (n - 6)
    tstat = al / np.sqrt(s2 / syy)
    # a1 (coeficiente de Δy_{s-1}) de la regresión completa: = b_d[2] - al * b_y[2] (FWL)
    a1 = b_d[:, 2] - al * b_y[:, 2]
    G_tau = tstat.mean()
    G_alpha = np.mean(n * al / (1 - a1))
    ap = (ty * td).sum() / syy.sum()
    ep = td - ap * ty
    s2p = (ep ** 2).sum() / (y.shape[0] * n)
    P_tau = ap / np.sqrt(s2p / syy.sum())
    P_alpha = n * ap
    return np.array([G_tau, G_alpha, P_tau, P_alpha])


def west_boot(y, x, g, B):
    dw = np.stack([np.diff(y, axis=1), np.diff(x, axis=1)], axis=2)          # (N, T-1, 2)
    Nn, m, _ = dw.shape
    Z = np.concatenate([np.ones((Nn, m - 1, 1)), dw[:, :-1, :]], axis=2)    # (N, m-1, 3)
    ZtZ = np.einsum("nti,ntj->nij", Z, Z)
    coef = np.linalg.solve(ZtZ, np.einsum("nti,ntk->nik", Z, dw[:, 1:, :]))  # (N, 3, 2)
    res = dw[:, 1:, :] - np.einsum("nti,nik->ntk", Z, coef)
    res = res - res.mean(1, keepdims=True)
    c = coef[:, 0, :]
    A = np.transpose(coef[:, 1:, :], (0, 2, 1))                               # (N, 2, 2): Δw_t = c + A Δw_{t-1}
    out = np.empty((B, 4))
    for b in range(B):
        ts = g.integers(0, m - 1, size=m - 1)
        eps = res[:, ts, :]
        d = np.empty((Nn, m, 2))
        d[:, 0, :] = dw[:, 0, :]
        for t in range(1, m):
            d[:, t, :] = c + np.einsum("nij,nj->ni", A, d[:, t - 1, :]) + eps[:, t - 1, :]
        ws = np.cumsum(d, axis=1)
        ys = np.concatenate([np.zeros((Nn, 1)), ws[:, :, 0]], axis=1) + y[:, :1]
        xs = np.concatenate([np.zeros((Nn, 1)), ws[:, :, 1]], axis=1) + x[:, :1]
        out[b] = west_stats(ys, xs)
    return out


# ------------------------------------------------------------------------------------------ CIPS
def cips(Y):
    yb = Y.mean(0)
    dy = np.diff(Y, axis=1)
    dyb = np.diff(yb)
    t = np.arange(2, Y.shape[1])
    n = len(t)
    X = np.empty((Y.shape[0], n, 6))
    X[:, :, 0] = 1.0
    X[:, :, 1] = Y[:, t - 1]
    X[:, :, 2] = yb[t - 1]
    X[:, :, 3] = dyb[t - 1]
    X[:, :, 4] = dy[:, t - 2]
    X[:, :, 5] = dyb[t - 2]
    z = dy[:, t - 1]
    inv = np.linalg.inv(np.einsum("nti,ntj->nij", X, X))
    b = np.einsum("nij,nj->ni", inv, np.einsum("nti,nt->ni", X, z))
    u = z - np.einsum("nti,ni->nt", X, b)
    s2 = (u ** 2).sum(1) / (n - 6)
    return (b[:, 1] / np.sqrt(s2 * inv[:, 1, 1])).mean()


def cips_boot(Y, g, B, L=BLOQUE):
    dy = np.diff(Y, axis=1)
    dy = dy - dy.mean(1, keepdims=True)
    m = dy.shape[1]
    nb = int(np.ceil(m / L))
    out = np.empty(B)
    for b in range(B):
        st = g.integers(0, m - L + 1, nb)
        idx = (st[:, None] + np.arange(L)).ravel()[:m]
        d = dy[:, idx]
        out[b] = cips(np.concatenate([Y[:, :1], Y[:, :1] + np.cumsum(d, 1)], axis=1))
    return out


# ------------------------------------------------------------------------------------------ CS-ARDL
def filas(y, x):
    yb, xb = y.mean(0), x.mean(0)
    t = np.arange(PT, y.shape[1])
    cols = [np.ones((y.shape[0], len(t))), y[:, t - 1], x[:, t], x[:, t - 1]]
    for s in range(PT + 1):
        cols.append(np.broadcast_to(yb[t - s], (y.shape[0], len(t))))
        cols.append(np.broadcast_to(xb[t - s], (y.shape[0], len(t))))
    return np.stack(cols, axis=2), y[:, t]


def mg(X, z):
    xtx = np.einsum("nti,ntj->nij", X, X)
    b = np.linalg.solve(xtx, np.einsum("nti,nt->ni", X, z)[..., None])[..., 0]
    return (b[:, 2] + b[:, 3]) / (1 - b[:, 1]), b[:, 1] - 1


def csardl(y, x, g, B):
    X, z = filas(y, x)
    th, sp = mg(X, z)
    est_t, est_s = th.mean(), sp.mean()
    n = X.shape[1]
    nb = int(np.ceil(n / BLOQUE))
    bt, bs = np.empty(B), np.empty(B)
    for b in range(B):
        st = g.integers(0, n - BLOQUE + 1, nb)
        idx = (st[:, None] + np.arange(BLOQUE)).ravel()[:n]
        a, c = mg(X[:, idx], z[:, idx])
        bt[b], bs[b] = a.mean(), c.mean()
    return est_t, est_s, bt.std(ddof=1), bs.std(ddof=1)


# ------------------------------------------------------------------------------------------ réplicas
def rep_west(g, coint, B_w, B_c):
    y, x, beta, speed = panel(g, coint)
    est = west_stats(y, x)
    bt = west_boot(y, x, g, B_w)
    p = (1 + (bt <= est[None, :]).sum(0)) / (B_w + 1)
    cs = cips(x)
    cb = cips_boot(x, g, B_c)
    p_c = (1 + (cb <= cs).sum()) / (B_c + 1)
    return list(p) + [p_c, est[0], cs]


def rep_cips_pot(g, B_c):
    s = panel_estacionario(g)
    cs = cips(s)
    cb = cips_boot(s, g, B_c)
    return [(1 + (cb <= cs).sum()) / (B_c + 1), cs]


def rep_cs(g, B):
    y, x, beta, speed = panel(g, True)
    et, es, st_, ss_ = csardl(y, x, g, B)
    z = 1.959964
    return [beta, speed, et, es, st_, ss_, float(abs(et - beta) <= z * st_), float(abs(es - speed) <= z * ss_), float(abs(et) > z * st_)]


def bloque(f, gens, *a):
    return [f(g, *a) for g in gens]


def correr(f, R, etapa, jobs, *a):
    gens = C.flujos(K, R, etapa)
    ch = [gens[i::40] for i in range(40)]
    sal = Parallel(n_jobs=jobs)(delayed(bloque)(f, c, *a) for c in ch)
    res = [None] * R
    for i, b in enumerate(sal):
        for j, v in enumerate(b):
            res[i + j * 40] = v
    return np.array(res, float)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--R_alt", type=int, default=1000)
    ap.add_argument("--B", type=int, default=99)
    ap.add_argument("--Bc", type=int, default=199)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    C.declarar(HERR, DGP)
    t0 = time.time()
    Mn = correr(rep_west, a.R, 1, a.jobs, False, a.B, a.Bc)
    print("west nulo", round(time.time() - t0), flush=True)
    Ma = correr(rep_west, a.R_alt, 2, a.jobs, True, a.B, a.Bc)
    print("west alt", round(time.time() - t0), flush=True)
    Mp = correr(rep_cips_pot, a.R_alt, 3, a.jobs, a.Bc)
    print("cips pot", round(time.time() - t0), flush=True)
    Mc = correr(rep_cs, a.R, 4, a.jobs, a.B)
    print("cs-ardl", round(time.time() - t0), flush=True)
    nombres = ["Westerlund Gtau", "Westerlund Galpha", "Westerlund Ptau", "Westerlund Palpha", "CIPS (serie I(1))"]
    filas_ = []
    for j, nm in enumerate(nombres):
        pot = float((Ma[:, j] <= 0.05).mean()) if j < 4 else float((Mp[:, 0] <= 0.05).mean())
        filas_.append({"herramienta": nm, "R_nulo": a.R, "tamano_5pct": float((Mn[:, j] <= 0.05).mean()), "R_alt": a.R_alt,
                       "potencia_alpha_-0.04": pot, "cobertura_95": np.nan, "sesgo": np.nan, "rmse": np.nan})
    th0, sp0, et, es, st_, ss_, c1, c2, rej = Mc.T
    e1, e2 = et - th0, es - sp0
    filas_.append({"herramienta": "CS-ARDL elasticidad de largo plazo", "R_nulo": a.R, "tamano_5pct": 1 - float(c1.mean()), "R_alt": a.R,
                   "potencia_alpha_-0.04": float(rej.mean()), "cobertura_95": float(c1.mean()), "sesgo": float(e1.mean()), "rmse": float(np.sqrt((e1 ** 2).mean()))})
    filas_.append({"herramienta": "CS-ARDL velocidad de ajuste media", "R_nulo": a.R, "tamano_5pct": 1 - float(c2.mean()), "R_alt": a.R,
                   "potencia_alpha_-0.04": float((np.abs(es) > 1.959964 * ss_).mean()), "cobertura_95": float(c2.mean()), "sesgo": float(e2.mean()), "rmse": float(np.sqrt((e2 ** 2).mean()))})
    tab = pd.DataFrame(filas_)
    ver = {}
    for _, f in tab.iterrows():
        cob = None if np.isnan(f.cobertura_95) else float(f.cobertura_95)
        ver[f.herramienta] = C.veredicto(float(f.tamano_5pct), cob, int(f.R_nulo))
    pot_g = float(tab.loc[0, "potencia_alpha_-0.04"])
    desc = pot_g < 0.5
    glob = {h: ("APTO" if v["apto"] else "NO APTO → solo descriptivo") for h, v in ver.items()}
    r = C.base_resultado("E1 (Westerlund, CIPS, CS-ARDL)", {"N": N, "T": T}, "Westerlund con bootstrap, CIPS con bootstrap, CS-ARDL con bootstrap de bloques")
    r["estimacion"] = {"tamano_Gtau": float(tab.loc[0, "tamano_5pct"]), "potencia_Gtau_alpha_-0.04": pot_g, "tamano_CIPS": float(tab.loc[4, "tamano_5pct"]),
                       "potencia_CIPS": float(tab.loc[4, "potencia_alpha_-0.04"]), "cobertura_CSARDL_theta": float(tab.loc[5, "cobertura_95"]),
                       "cobertura_CSARDL_velocidad": float(tab.loc[6, "cobertura_95"]), "sesgo_theta": float(tab.loc[5, "sesgo"]), "rmse_theta": float(tab.loc[5, "rmse"])}
    r["ic95"] = C.ic_binomial(float(tab.loc[0, "tamano_5pct"]), a.R)
    r["diagnosticos"] = {"veredictos": glob, "detalle": ver, "umbral_potencia_V15_0.5": {"potencia_Gtau": pot_g, "E1_solo_descriptiva": bool(desc)},
                         "R": a.R, "R_alt": a.R_alt, "B_westerlund": a.B, "B_cips": a.Bc, "semilla": C.SEED, "segundos": time.time() - t0}
    r["notas"] = [f"Umbral de V15 (potencia frente a −0,04 ≥ 0,5): {'NO se cumple → E1 solo descriptiva' if desc else 'se cumple'} (Gτ: {pot_g:.3f}).",
                  "Westerlund sin adelantos y 1 rezago; Pτ/Pα con variables auxiliares eliminadas por unidad (variante del agrupado de Westerlund)."]
    md = (f"## Resultados (R = {a.R} nulo, {a.R_alt} alternativa; B Westerlund = {a.B}, B CIPS = {a.Bc}; semilla {C.SEED}, k = {K})\n\n" + C.md_tabla(tab)
          + f"\n**Umbral de V15:** potencia de Gτ frente a α = −0,04: {pot_g:.3f} → {'E1 solo DESCRIPTIVA' if desc else 'E1 puede reportar inferencia'}.\n\n**Veredictos de tamaño/cobertura**\n\n"
          + "\n".join(f"- {h}: **{g}** {'; '.join(ver[h]['fallos'])}" for h, g in glob.items()) + "\n")
    C.cerrar(HERR, r, tab, md)
    print(tab.to_string())
    print(glob, "descriptiva:", desc)


if __name__ == "__main__":
    main()
