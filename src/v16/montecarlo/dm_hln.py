"""Q10 · Diebold-Mariano con corrección HLN frente al AR(4), h=1, ventana expansiva, P≈75; Clark-West como alternativa.

Proceso generador en docs/v16/validacion_montecarlo/dm_hln.md. Uso: python dm_hln.py [R]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.montecarlo import _comun_series as C  # noqa: E402

P, R_INI, H = 75, 30, 1
PHI = np.array([0.5, 0.1, 0.05, -0.05])


def generar(rng, beta, sig_x=1.0):
    n = R_INI + P + 4 + 50
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = 0.3 * x[t - 1] + sig_x * rng.standard_normal()
    y = np.zeros(n)
    e = rng.standard_normal(n)
    for t in range(4, n):
        y[t] = 0.1 + PHI @ y[t - 4:t][::-1] + beta * x[t - 1] + e[t]
    return y[50:], x[50:]


def pronosticos(y, x):
    """Ventana expansiva: AR(4) (restringido) y AR(4)+x_{t-1} (anidante); h=1."""
    n = len(y)
    Z0 = np.column_stack([np.ones(n - 4)] + [y[4 - j:n - j] for j in range(1, 5)])  # filas t=4..n-1
    Z1 = np.column_stack([Z0, x[3:n - 1]])
    yy = y[4:]
    t0 = len(yy) - P
    e0 = np.empty(P); e1 = np.empty(P); f0 = np.empty(P); f1 = np.empty(P)
    for i in range(P):
        m = t0 + i
        for Z, e, f in ((Z0, e0, f0), (Z1, e1, f1)):
            b = np.linalg.lstsq(Z[:m], yy[:m], rcond=None)[0]
            f[i] = Z[m] @ b
            e[i] = yy[m] - f[i]
    return e0, e1, f0, f1


def pruebas(e0, e1, f0, f1):
    """Devuelve p-valores unilaterales (H1: el modelo grande es mejor) y bilaterales."""
    d = e0 ** 2 - e1 ** 2
    p = len(d)
    dm = d.mean() / np.sqrt(d.var(ddof=0) / p)       # h=1: varianza larga = gamma0
    hln = dm * np.sqrt((p + 1 - 2 * H + H * (H - 1) / p) / p)
    p_hln_u = 1 - stats.t.cdf(hln, p - 1)
    p_hln_b = 2 * (1 - stats.t.cdf(abs(hln), p - 1))
    p_dm_u = 1 - stats.norm.cdf(dm)
    cw_t = e0 ** 2 - (e1 ** 2 - (f0 - f1) ** 2)
    cw = cw_t.mean() / np.sqrt(cw_t.var(ddof=1) / p)
    p_cw = 1 - stats.norm.cdf(cw)
    p_cw_t = 1 - stats.t.cdf(cw, p - 1)
    return p_hln_u, p_hln_b, p_dm_u, p_cw, p_cw_t, 1 - (e1 ** 2).mean() / (e0 ** 2).mean()


def una(k, beta):
    rng = C.rng(4, k)
    y, x = generar(rng, beta)
    return pruebas(*pronosticos(y, x))


def main(R=2000):
    esc = {"nulo_anidado": 0.0, "alt_reduccion10": 1 / 3}
    rows = {}
    for nm, beta in esc.items():
        Rk = R if nm.startswith("nulo") else 1000
        a = np.array(C.paralelo(una, [(k + (0 if beta == 0 else 10 ** 6), beta) for k in range(Rk)]))
        rows[nm] = {"R": Rk, "tam_HLN_unilateral": float((a[:, 0] < .05).mean()), "tam_HLN_bilateral": float((a[:, 1] < .05).mean()),
                    "tam_DM_normal_unilateral": float((a[:, 2] < .05).mean()), "CW_normal_unilateral": float((a[:, 3] < .05).mean()),
                    "CW_t_unilateral": float((a[:, 4] < .05).mean()), "reduccion_ECM_media": float(a[:, 5].mean())}
    tabla = pd.DataFrame([{"escenario": e, **v} for e, v in rows.items()])
    n = rows["nulo_anidado"]
    v_hln = C.veredicto(n["tam_HLN_unilateral"], n["R"])
    v_cw = C.veredicto(n["CW_normal_unilateral"], n["R"])
    v_cwt = C.veredicto(n["CW_t_unilateral"], n["R"])
    if v_hln["veredicto"] == "APTO":
        glob = {"veredicto": "APTO (DM-HLN)", "fallos": []}
    elif v_cw["veredicto"] == "APTO" or v_cwt["veredicto"] == "APTO":
        glob = {"veredicto": "NO APTO DM-HLN para pares anidados; alternativa Clark-West APTA", "fallos": v_hln["fallos"]}
    else:
        glob = {"veredicto": "NO APTO → diseño solo descriptivo", "fallos": v_hln["fallos"] + [f"Clark-West: {'; '.join(v_cw['fallos'])}"]}
    r = C.resultado_base("dm_hln", "Q10 (adenda punto 3)", {"P": P, "ventana_inicial": R_INI, "h": H}, "DM-HLN vs AR(4); alternativa Clark-West")
    r["estimacion"] = {"tamano_HLN_unilateral": n["tam_HLN_unilateral"], "tamano_CW": n["CW_normal_unilateral"],
                       "potencia_HLN": rows["alt_reduccion10"]["tam_HLN_unilateral"], "potencia_CW": rows["alt_reduccion10"]["CW_normal_unilateral"],
                       "reduccion_ECM_alt": rows["alt_reduccion10"]["reduccion_ECM_media"], "cobertura": "no aplica (prueba)"}
    r["ic95"] = C.ic_binomial(n["tam_HLN_unilateral"], n["R"])
    r["diagnosticos"] = {"R": R, "veredicto": glob, "v_HLN": v_hln, "v_CW_normal": v_cw, "v_CW_t": v_cwt, "detalle": rows}
    r["fuera_muestra"] = {"modelo": "AR(4)+x_{t-1} frente a AR(4) (simulado)", "rmse": None, "dm_vs_ar4": "ver diagnosticos.detalle"}
    r["notas"] = ["Prueba unilateral (H1: el modelo grande reduce el ECM). Con h=1 la varianza de largo plazo es gamma0.",
                  "El ECM simulado reduce ~10 % en la alternativa (beta=1/3, var(x)≈1,1)."]
    md = (f"## Resultados (R={R} bajo el nulo, 1.000 bajo la alternativa)\n\n" + tabla.to_markdown(index=False)
          + f"\n\n**Veredicto: {glob['veredicto']}** {'; '.join(glob['fallos'])}\n")
    C.escribir_salidas("dm_hln", r, tabla, md)
    print(rows, glob)


if __name__ == "__main__":
    main(*[int(x) for x in sys.argv[1:]])
