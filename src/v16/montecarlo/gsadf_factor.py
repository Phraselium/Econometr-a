"""Q9-g · GSADF (Phillips-Shi-Yu 2015) sobre una serie agregada (factor común), T≈98, bootstrap wild.

Proceso generador en docs/v16/validacion_montecarlo/gsadf_factor.md. Uso: python gsadf_factor.py [R] [B]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.montecarlo import _comun_series as C  # noqa: E402

T = 98
R0 = int(np.floor(T * (0.01 + 1.8 / np.sqrt(T))))  # ventana mínima de Phillips-Shi-Yu


def gsadf(y):
    """sup sobre (inicio, fin) de la t de ADF sin rezagos (con constante) usando sumas acumuladas."""
    dy = np.diff(y)
    x = y[:-1]
    n = len(dy)
    cs = lambda v: np.concatenate([[0.0], np.cumsum(v)])
    Sx, Sxx, Sd, Sdd, Sxd = cs(x), cs(x * x), cs(dy), cs(dy * dy), cs(x * dy)
    ends = np.arange(R0, n + 1)
    best = -np.inf
    for e in ends:
        s = np.arange(0, e - R0 + 1)
        m = (e - s).astype(float)
        sx, sxx, sd, sdd, sxd = Sx[e] - Sx[s], Sxx[e] - Sxx[s], Sd[e] - Sd[s], Sdd[e] - Sdd[s], Sxd[e] - Sxd[s]
        sxx_c = sxx - sx ** 2 / m
        sxd_c = sxd - sx * sd / m
        b = sxd_c / sxx_c
        ssr = (sdd - sd ** 2 / m) - b * sxd_c
        tst = b / np.sqrt(ssr / (m - 2) / sxx_c)
        best = max(best, tst.max())
    return best


def sigma_path(rng, tipo):
    if tipo == "homo":
        return np.ones(T - 1)
    if tipo == "salto":      # volatilidad triplica en el 40 % de la muestra y vuelve a 1 en el 75 %
        s = np.ones(T - 1); s[int(0.4 * T):int(0.75 * T)] = 3.0
        return s
    if tipo == "estoc":      # log-volatilidad AR(1) persistente
        h = np.zeros(T - 1)
        for t in range(1, T - 1):
            h[t] = 0.9 * h[t - 1] + 0.35 * rng.standard_normal()
        return np.exp(h)
    raise ValueError(tipo)


def serie(rng, tipo, explosivo=False):
    e = sigma_path(rng, tipo) * rng.standard_normal(T - 1)
    y = np.zeros(T)
    a, b = int(0.45 * T), int(0.45 * T) + 15
    for t in range(1, T):
        rho = 1.05 if (explosivo and a <= t < b) else (0.6 if (explosivo and b <= t < b + 1) else 1.0)
        y[t] = rho * y[t - 1] + e[t - 1]
    return y


def una(k, tipo, explosivo, B, cv_iid):
    rng = C.rng(3, k)
    y = serie(rng, tipo, explosivo)
    s = gsadf(y)
    dy = np.diff(y)
    # bootstrap wild (Harvey et al. 2016): Δy* = Δy · w, w ~ N(0,1), raíz unitaria impuesta, y*_0 = y_0
    bs = np.empty(B)
    for b in range(B):
        yb = np.concatenate([[y[0]], y[0] + np.cumsum(dy * rng.standard_normal(len(dy)))])
        bs[b] = gsadf(yb)
    return s, np.quantile(bs, 0.95), s > cv_iid


def cv_homo(R=1000):
    return float(np.quantile([gsadf(serie(C.rng(30, k), "homo")) for k in range(R)], 0.95))


def main(R=2000, B=499):
    cv_iid = cv_homo()
    res = {}
    for esc, tipo, expl, Rk in (("nulo_homo", "homo", False, R), ("nulo_salto", "salto", False, R),
                                 ("nulo_estoc", "estoc", False, R), ("alt_homo", "homo", True, 500),
                                 ("alt_salto", "salto", True, 500)):
        off = {"nulo_homo": 0, "nulo_salto": 10 ** 6, "nulo_estoc": 2 * 10 ** 6, "alt_homo": 3 * 10 ** 6, "alt_salto": 4 * 10 ** 6}[esc]
        out = C.paralelo(una, [(off + k, tipo, expl, B, cv_iid) for k in range(Rk)])
        s = np.array([o[0] for o in out]); cv = np.array([o[1] for o in out]); iid = np.array([o[2] for o in out])
        res[esc] = {"R": Rk, "rech_boot_wild": float((s > cv).mean()), "rech_cv_iid_simulado": float(iid.mean())}
    tabla = pd.DataFrame([{"escenario": e, **v} for e, v in res.items()])
    ver = {}
    for e in ("nulo_homo", "nulo_salto", "nulo_estoc"):
        ver[e] = C.veredicto(res[e]["rech_boot_wild"], res[e]["R"])
    todos = all(v["veredicto"] == "APTO" for v in ver.values())
    # veredicto global: debe pasar con heterocedasticidad (salto y estocástica); la homocedástica se informa
    glob = all(ver[e]["veredicto"] == "APTO" for e in ("nulo_salto", "nulo_estoc"))
    vg = {"veredicto": "APTO" if glob else "NO APTO",
          "fallos": [f"{e}: {'; '.join(v['fallos'])}" for e, v in ver.items() if v["veredicto"] != "APTO"]}
    r = C.resultado_base("gsadf_factor", "Q9-g (adenda punto 3)", {"T": T, "r0_obs": R0}, "GSADF + bootstrap wild")
    r["estimacion"] = {"tamano": {e: res[e]["rech_boot_wild"] for e in ("nulo_homo", "nulo_salto", "nulo_estoc")},
                       "potencia": {e: res[e]["rech_boot_wild"] for e in ("alt_homo", "alt_salto")},
                       "tamano_cv_iid_bajo_heterocedasticidad": {e: res[e]["rech_cv_iid_simulado"] for e in ("nulo_salto", "nulo_estoc")},
                       "cobertura": "no aplica (prueba)"}
    r["ic95"] = {e: C.ic_binomial(res[e]["rech_boot_wild"], res[e]["R"]) for e in ("nulo_homo", "nulo_salto", "nulo_estoc")}
    r["diagnosticos"] = {"R": R, "B": B, "veredicto": vg, "veredicto_por_escenario": ver, "cv95_iid_simulado": cv_iid, "todos_pasan": todos}
    r["notas"] = ["Veredicto global exige APTO bajo heterocedasticidad (salto y estocástica); la adenda no nombra alternativa para GSADF (R18: por provincia es ya visto)."]
    md = (f"## Resultados (R={R} bajo el nulo, 500 bajo la alternativa, B={B})\n\n" + tabla.to_markdown(index=False)
          + f"\n\nVC al 95 % iid simulado: {cv_iid:.3f}. **Veredicto: {vg['veredicto']}** {'; '.join(vg['fallos'])}\n")
    C.escribir_salidas("gsadf_factor", r, tabla, md)
    print(res, vg)


if __name__ == "__main__":
    main(*[int(x) for x in sys.argv[1:]])
