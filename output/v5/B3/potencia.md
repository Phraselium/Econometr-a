# B3 · Potencia previa (escrita ANTES de estimar; 2026-10-10)

Método: EMD = menor coeficiente estandarizado (DT de Y por DT de X) con potencia 80 % en un contraste t de dos colas,
con EE = sqrt((1-R²)·VIF/(N-K-1)). N=50 provincias; K = 12 regresores (8 familias; F2, F4, F5 y F8 aportan 2 cada una,
menos las que aportan 1); R² del modelo completo y VIF del regresor de interés son supuestos (rejilla en tablas/potencia_emd.csv).
Holm: el peor caso exige p < 0,05/m con m = 8 (familias × Y1 × P1, como fija el pre-registro) o m = 3 (solo las
confirmatorias). Sin Holm (m=1) como referencia.

| Escenario (N=50, K=12) | alfa | EMD (DT) |
|---|---|---|
| R²=0,5, VIF=2, m=1 | 0,05 | 0.473 |
| R²=0,5, VIF=2, m=3 | 0,0167 | 0.554 |
| R²=0,5, VIF=2, m=8 | 0,00625 | 0.619 |
| rango en la rejilla, m=8 (R² 0,3-0,7; VIF 1-4) | 0,00625 | 0.339 a 1.036 |

Comprobación por simulación (4.000 réplicas, SEED=20261010) en el escenario m=8 con beta = EMD analítico: potencia simulada = 0.810 (objetivo 0,80).

**Veredicto previo:** el EMD de referencia (0.62 DT, m=8) supera 0,5 DT: B3 se presenta como DESCRIPTIVO HONESTO. Un coeficiente estandarizado de ese tamaño
equivale a que una DT del regresor se asocie con 0.62 DT de la variable dependiente; la rejilla completa va de 0.34 a 1.04 DT.
Consecuencia pre-registrada: si el EMD supera 0,5 DT, la capa máxima es C4 y la redacción es «descriptivo honesto»;
un resultado no significativo NO es evidencia de ausencia de asociación. Todo lenguaje es de asociación.
