"""Q9 · CIPS (Pesaran 2007) con valores críticos por bootstrap de bloques con factor común.

Proceso generador declarado en docs/v16/validacion_montecarlo/cips_bootstrap.md (antes de simular).
Uso: python src/v16/montecarlo/cips_bootstrap.py [R_tamano] [R_potencia] [B]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.montecarlo import _comun_series as C  # noqa: E402

K = 11
N, T = 38, 95
CV_ASINT = -2.11  # Pesaran (2007), tabla II(b) (intercepto), N≈30-50, T=100, 5 %: valor aproximado


def generar(rng, phi_lo=1.0, phi_hi=1.0):
    f = np.zeros(T + 50)
    ef = rng.standard_normal(T + 50)
    for t in range(1, T + 50):
        f[t] = 0.5 * f[t - 1] + ef[t]
    gam = rng.normal(1.0, 0.5, N)
    sig = rng.uniform(0.5, 1.5, N)
    rho = rng.uniform(0.0, 0.4, N)
    eta = rng.standard_normal((N, T + 50))
    eta = eta + 0.25 * (np.roll(eta, 1, axis=0) + np.roll(eta, -1, axis=0))  # vecindad en anillo
    phi = rng.uniform(phi_lo, phi_hi, N)
    y = np.zeros((N, T + 50))
    e = np.zeros(N)
    mu = rng.normal(0, 1, N)
    for t in range(1, T + 50):
        e = rho * e + sig * eta[:, t]
        y[:, t] = (1 - phi) * mu + phi * y[:, t - 1] + gam * f[t] + e
    return y[:, 50:] + (mu[:, None] if phi_hi == 1.0 else 0.0)


def cips(Y):
    yb = Y.mean(0)
    dy = np.diff(Y, axis=1)  # (N,T-1): dy[:,j] = y[j+1]-y[j]
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
    xtx = np.einsum("nti,ntj->nij", X, X)
    xty = np.einsum("nti,nt->ni", X, z)
    inv = np.linalg.inv(xtx)
    b = np.einsum("nij,nj->ni", inv, xty)
    u = z - np.einsum("nti,ni->nt", X, b)
    s2 = (u ** 2).sum(1) / (n - 6)
    tst = b[:, 1] / np.sqrt(s2 * inv[:, 1, 1])
    return tst.mean()


def bloques(rng, d, L):
    """Bootstrap de bloques móviles sobre las columnas (tiempo) conjuntas de todas las unidades."""
    m = d.shape[1]
    nb = int(np.ceil(m / L))
    st = rng.integers(0, m - L + 1, nb)
    idx = (st[:, None] + np.arange(L)).ravel()[:m]
    return d[:, idx]


def cips_boot(Y, rng, B, L):
    dy = np.diff(Y, axis=1)
    dy = dy - dy.mean(1, keepdims=True)  # impone raíz unitaria sin deriva
    st = np.empty(B)
    for b in range(B):
        d = bloques(rng, dy, L)
        Yb = np.concatenate([Y[:, :1], Y[:, :1] + np.cumsum(d, 1)], axis=1)
        st[b] = cips(Yb)
    return st


def una(k, escenario, B, L):
    rng = C.rng(1, k)
    Y = generar(rng, *((1.0, 1.0) if escenario == "nulo" else (0.85, 0.95)))
    s = cips(Y)
    bt = cips_boot(Y, rng, B, L)
    return s, np.quantile(bt, 0.05), float((bt <= s).mean())


def main(Rt=2000, Rp=500, B=199):
    L = int(round(2 * T ** (1 / 3)))
    res = {}
    for esc, R in (("nulo", Rt), ("alternativa", Rp)):
        out = C.paralelo(una, [(k + (0 if esc == "nulo" else 10 ** 6), esc, B, L) for k in range(R)])
        s = np.array([o[0] for o in out]); cv = np.array([o[1] for o in out]); p = np.array([o[2] for o in out])
        res[esc] = {"R": R, "rech_boot": float((s < cv).mean()), "rech_pvalor": float((p <= 0.05).mean()),
                    "rech_asint": float((s < CV_ASINT).mean()), "media_cips": float(s.mean()),
                    "cv_boot_media": float(cv.mean())}
    tam = res["nulo"]["rech_boot"]
    ver = C.veredicto(tam, Rt)
    r = C.resultado_base("cips_bootstrap", "Q9 (adenda punto 3)", {"N": N, "T": T}, "CIPS + bootstrap de bloques con factor común")
    r["estimacion"] = {"tamano_boot": tam, "potencia_boot": res["alternativa"]["rech_boot"],
                       "tamano_asintotico_cv_-2.11": res["nulo"]["rech_asint"], "cobertura": "no aplica (prueba)"}
    r["ic95"] = C.ic_binomial(tam, Rt)
    r["diagnosticos"] = {"detalle": res, "bloque": L, "B": B, "veredicto": ver}
    r["notas"] = ["Cobertura no definida para una prueba de raíz unitaria; el veredicto usa el tamaño (criterio de la adenda).",
                  "La adenda no nombra alternativa para CIPS: si no pasa, Q9 queda en GSADF agregado y CIPS solo descriptivo."]
    tabla = pd.DataFrame([{"escenario": e, **v} for e, v in res.items()])
    md = (f"## Resultados (R={Rt} bajo el nulo, R={Rp} bajo la alternativa, B={B}, bloque={L})\n\n"
          + tabla.to_markdown(index=False) + f"\n\nTamaño con bootstrap: {tam:.4f} (IC binomial {r['ic95']}); con CV asintótico -2,11: "
          f"{res['nulo']['rech_asint']:.4f}. Potencia (φ_i en U(0,85; 0,95)): {res['alternativa']['rech_boot']:.4f}.\n\n"
          f"**Veredicto: {ver['veredicto']}** {'; '.join(ver['fallos'])}\n")
    C.escribir_salidas("cips_bootstrap", r, tabla, md)
    print(res, ver)


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    main(*a)
