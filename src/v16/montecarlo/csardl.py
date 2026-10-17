"""Q9-c · CS-ARDL (Chudik-Pesaran 2015): elasticidad de largo plazo, grupo medio, bootstrap por bloques.

Proceso generador en docs/v16/validacion_montecarlo/csardl.md. Uso: python csardl.py [R] [B]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.montecarlo import _comun_series as C  # noqa: E402

N, T = 38, 95
THETA, SD_THETA = 0.8, 0.2
PT = int(np.floor(T ** (1 / 3)))  # 4 rezagos de las medias transversales


def generar(rng, theta=THETA):
    n = T + 50
    f = np.zeros(n)
    ef = rng.standard_normal(n)
    for t in range(1, n):
        f[t] = 0.6 * f[t - 1] + ef[t]
    th = rng.normal(theta, SD_THETA, N)            # elasticidad de largo plazo por unidad
    phi = rng.uniform(0.5, 0.8, N)                  # persistencia
    b0 = rng.uniform(0.3, 0.6, N) * th * (1 - phi) / 0.45  # efecto contemporáneo
    b1 = th * (1 - phi) - b0                        # tal que (b0+b1)/(1-phi) = th
    gx = rng.normal(1.0, 0.5, N); gy = rng.normal(1.0, 0.5, N)
    rx = rng.uniform(0.3, 0.7, N)
    ux = rng.standard_normal((N, n)); ex = rng.standard_normal((N, n))
    ux = ux + 0.25 * (np.roll(ux, 1, 0) + np.roll(ux, -1, 0))   # correlación espacial en anillo
    ex = ex + 0.25 * (np.roll(ex, 1, 0) + np.roll(ex, -1, 0))
    x = np.zeros((N, n)); y = np.zeros((N, n))
    for t in range(1, n):
        x[:, t] = rx * x[:, t - 1] + gx * f[t] + ux[:, t]
        y[:, t] = phi * y[:, t - 1] + b0 * x[:, t] + b1 * x[:, t - 1] + gy * f[t] + 0.7 * ex[:, t]
    return y[:, 50:], x[:, 50:], th.mean()


def filas(y, x):
    """Matriz de regresión por unidad (N, n, k) y respuesta (N, n): ARDL(1,1) + MTs y PT rezagos."""
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
    th = (b[:, 2] + b[:, 3]) / (1 - b[:, 1])
    return th.mean()


def una(k, B, L, theta):
    rng = C.rng(2, k)
    y, x, th0 = generar(rng, theta)
    X, z = filas(y, x)
    est = mg(X, z)
    n = X.shape[1]
    nb = int(np.ceil(n / L))
    bs = np.empty(B)
    # bootstrap por bloques móviles de las filas de la regresión (conjuntas para todas las unidades)
    for b in range(B):
        st = rng.integers(0, n - L + 1, nb)
        idx = (st[:, None] + np.arange(L)).ravel()[:n]
        bs[b] = mg(X[:, idx], z[:, idx])
    se = bs.std(ddof=1)
    lo, hi = est - 1.96 * se, est + 1.96 * se
    plo, phi_ = np.quantile(bs, [0.025, 0.975])
    # IC percentil con corrección de sesgo por centrado en el estimador: [2est - q97.5, 2est - q2.5]
    return est, th0, se, lo, hi, 2 * est - phi_, 2 * est - plo


def main(R=2000, B=99):
    L = int(round(2 * T ** (1 / 3)))
    out = C.paralelo(una, [(k, B, L, THETA) for k in range(R)])
    a = np.array(out)
    est, th0, se, lo, hi, plo, phi_ = a.T
    cob = float(((lo <= th0) & (th0 <= hi)).mean())
    cob_p = float(((plo <= th0) & (th0 <= phi_)).mean())
    sesgo = float((est - th0).mean()); rmse = float(np.sqrt(((est - th0) ** 2).mean()))
    tam = 1 - cob
    pot = float(((lo > 0) | (hi < 0)).mean())               # rechazo de θ = 0 con θ ≈ 0,8
    # tamaño frente a una referencia: H0: θ = 0,8 verdadera (tamaño = 1 - cobertura, mismo IC)
    # potencia frente a θ0 + 0,2 (desplazamiento declarado): H0: θ = θ_media_verdadera + 0,2
    pot02 = float(((th0 + 0.2 < lo) | (th0 + 0.2 > hi)).mean())
    ver = C.veredicto(tam, R, cob)
    r = C.resultado_base("csardl", "Q9-c (adenda punto 3)", {"N": N, "T": T}, "CS-ARDL(1,1) grupo medio + bootstrap por bloques")
    r["estimacion"] = {"sesgo": sesgo, "rmse": rmse, "cobertura_normal_boot": cob, "cobertura_percentil_centrado": cob_p,
                       "tamano_5pct": tam, "potencia_theta0": pot, "potencia_desplazamiento_0.2": pot02,
                       "se_boot_medio": float(se.mean()), "sd_estimador": float(est.std(ddof=1))}
    r["ic95"] = C.ic_binomial(cob, R)
    r["diagnosticos"] = {"R": R, "B": B, "bloque": L, "rezagos_MT": PT, "veredicto": ver,
                         "nota_magnitud": "Q9-c no tiene magnitud de referencia («no aplica»): la potencia es frente a θ=0 y a un desplazamiento declarado de 0,2."}
    r["notas"] = ["La adenda no nombra alternativa para CS-ARDL: si falla, Q9-c queda descriptivo."]
    tabla = pd.DataFrame([{"medida": k, "valor": v} for k, v in r["estimacion"].items()])
    md = (f"## Resultados (R={R}, B={B}, bloque={L})\n\n" + tabla.to_markdown(index=False)
          + f"\n\nIC normal con EE bootstrap: cobertura {cob:.4f} (tamaño {tam:.4f}). IC percentil centrado: {cob_p:.4f}.\n\n"
          f"**Veredicto: {ver['veredicto']}** {'; '.join(ver['fallos'])}\n")
    C.escribir_salidas("csardl", r, tabla, md)
    print(r["estimacion"], ver)


if __name__ == "__main__":
    main(*[int(x) for x in sys.argv[1:]])
