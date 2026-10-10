"""B3 potencia previa (se ejecuta ANTES de estimar). Efecto mínimo detectable (EMD) en DT de Y por 1 DT de X,
con regresores y Y estandarizados, potencia 80 %, dos colas, N=50, K regresores, Holm (peor caso: m pruebas)."""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats

SEED = 20261010
OUT = Path(__file__).resolve().parents[2] / "output/v5/B3"


def emd(n, k, r2, vif, alpha, power=0.8):
    df = n - k - 1
    se = np.sqrt((1 - r2) * vif / df)          # EE de beta estandarizado: sqrt((1-R2) VIF/(n-k-1))
    tc = stats.t.ppf(1 - alpha / 2, df)
    f = lambda b: (stats.nct.sf(tc, df, b / se) + stats.nct.cdf(-tc, df, b / se)) - power
    return optimize.brentq(f, 1e-6, se * 6), se


def mc(n, k, beta, vif, r2, alpha, reps=4000):
    """Comprobación por simulación del EMD analítico (X con correlación equicorrelada que da VIF aproximado)."""
    rng = np.random.default_rng(SEED)
    r = 1 - 1 / vif                          # R² de X1 sobre las demás -> VIF
    hit = 0
    for _ in range(reps):
        X = rng.standard_normal((n, k))
        X[:, 0] = np.sqrt(r) * X[:, 1] + np.sqrt(1 - r) * X[:, 0]
        X = (X - X.mean(0)) / X.std(0)
        y = beta * X[:, 0] + np.sqrt(1 - r2) * rng.standard_normal(n)   # sigma residual = sqrt(1-R²)
        A = np.column_stack([np.ones(n), X])
        b = np.linalg.lstsq(A, y, rcond=None)[0]
        e = y - A @ b
        s2 = e @ e / (n - k - 1)
        v = s2 * np.linalg.inv(A.T @ A)[1, 1]
        hit += abs(b[1] / np.sqrt(v)) > stats.t.ppf(1 - alpha / 2, n - k - 1)
    return hit / reps


def main():
    filas = []
    for n in (50, 46):
        for k in (8, 12):
            for r2 in (0.3, 0.5, 0.7):
                for vif in (1.0, 2.0, 4.0):
                    for m in (1, 3, 8):
                        a = 0.05 / m
                        b, se = emd(n, k, r2, vif, a)
                        filas.append(dict(N=n, K=k, R2=r2, VIF=vif, m_Holm=m, alpha=a, EMD_DT=b, EE_std=se))
    t = pd.DataFrame(filas)
    t.to_csv(OUT / "tablas/potencia_emd.csv", index=False)
    ref = t[(t.N == 50) & (t.K == 12) & (t.R2 == 0.5) & (t.VIF == 2.0)]
    b8 = float(ref[ref.m_Holm == 8].EMD_DT.iloc[0])
    sim = mc(50, 12, b8, 2.0, 0.5, 0.05 / 8)
    peor = float(t[(t.N == 50) & (t.K == 12) & (t.m_Holm == 8)].EMD_DT.max())
    mejor = float(t[(t.N == 50) & (t.K == 12) & (t.m_Holm == 8)].EMD_DT.min())
    veredicto = "supera 0,5 DT: B3 se presenta como DESCRIPTIVO HONESTO" if b8 > 0.5 else "no supera 0,5 DT"
    md = f"""# B3 · Potencia previa (escrita ANTES de estimar; 2026-10-10)

Método: EMD = menor coeficiente estandarizado (DT de Y por DT de X) con potencia 80 % en un contraste t de dos colas,
con EE = sqrt((1-R²)·VIF/(N-K-1)). N=50 provincias; K = 12 regresores (8 familias; F2, F4, F5 y F8 aportan 2 cada una,
menos las que aportan 1); R² del modelo completo y VIF del regresor de interés son supuestos (rejilla en tablas/potencia_emd.csv).
Holm: el peor caso exige p < 0,05/m con m = 8 (familias × Y1 × P1, como fija el pre-registro) o m = 3 (solo las
confirmatorias). Sin Holm (m=1) como referencia.

| Escenario (N=50, K=12) | alfa | EMD (DT) |
|---|---|---|
| R²=0,5, VIF=2, m=1 | 0,05 | {float(ref[ref.m_Holm==1].EMD_DT.iloc[0]):.3f} |
| R²=0,5, VIF=2, m=3 | 0,0167 | {float(ref[ref.m_Holm==3].EMD_DT.iloc[0]):.3f} |
| R²=0,5, VIF=2, m=8 | 0,00625 | {b8:.3f} |
| rango en la rejilla, m=8 (R² 0,3-0,7; VIF 1-4) | 0,00625 | {mejor:.3f} a {peor:.3f} |

Comprobación por simulación (4.000 réplicas, SEED=20261010) en el escenario m=8 con beta = EMD analítico: potencia simulada = {sim:.3f} (objetivo 0,80).

**Veredicto previo:** el EMD de referencia ({b8:.2f} DT, m=8) {veredicto}. Un coeficiente estandarizado de ese tamaño
equivale a que una DT del regresor se asocie con {b8:.2f} DT de la variable dependiente; la rejilla completa va de {mejor:.2f} a {peor:.2f} DT.
Consecuencia pre-registrada: si el EMD supera 0,5 DT, la capa máxima es C4 y la redacción es «descriptivo honesto»;
un resultado no significativo NO es evidencia de ausencia de asociación. Todo lenguaje es de asociación.
"""
    (OUT / "potencia.md").write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
