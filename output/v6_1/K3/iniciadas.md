# K3.1 Viviendas iniciadas y alquiler: orden temporal (C4, exploratorio)

Panel provincial de entrenamiento (SERPAVI alquiler de stock, €/m²; iniciadas libres por 1.000 hab., MIVAU). N conjunta A = 175 obs. en 35 provincias (SERPAVI 2015-2023, 38-39 provincias, Δln alquiler desde 2016). EF de provincia y año; errores agrupados por provincia; Holm sobre todos los coeficientes. Sin lenguaje causal.

| Modelo | Regresor | Coef. | IC95 % | p | p Holm | N |
|---|---|---|---|---|---|---|
| A_conjunta | ini_l2 | -0.0013 | [-0.0040; 0.0014] | 0.349 | 1.000 | 175 |
| A_conjunta | ini_l1 | -0.0007 | [-0.0035; 0.0021] | 0.631 | 1.000 | 175 |
| A_conjunta | ini_1000 | 0.0027 | [0.0001; 0.0052] | 0.041 | 0.572 | 175 |
| A_conjunta | ini_f1 | -0.0002 | [-0.0017; 0.0014] | 0.831 | 1.000 | 175 |
| A_conjunta | ini_f2 | 0.0007 | [-0.0016; 0.0031] | 0.540 | 1.000 | 175 |
| A_ini_l2 | ini_l2 | -0.0010 | [-0.0030; 0.0010] | 0.337 | 1.000 | 246 |
| A_ini_l1 | ini_l1 | -0.0001 | [-0.0025; 0.0024] | 0.947 | 1.000 | 281 |
| A_ini_1000 | ini_1000 | 0.0021 | [0.0000; 0.0042] | 0.046 | 0.600 | 281 |
| A_ini_f1 | ini_f1 | 0.0010 | [-0.0014; 0.0034] | 0.405 | 1.000 | 245 |
| A_ini_f2 | ini_f2 | 0.0005 | [-0.0016; 0.0027] | 0.619 | 1.000 | 210 |
| B_inversa | dlna_l1 | 0.0284 | [-14.4261; 14.4829] | 0.997 | 1.000 | 210 |
| B_inversa | dlna_l2 | 2.9219 | [-8.9319; 14.7757] | 0.629 | 1.000 | 210 |
| B_dlna_l1 | dlna_l1 | 6.2841 | [-6.2629; 18.8311] | 0.326 | 1.000 | 245 |
| B_dlna_l2 | dlna_l2 | 2.9234 | [-8.4836; 14.3304] | 0.615 | 1.000 | 210 |

A: Δln alquiler_t sobre iniciadas/1.000 hab. en t-2, t-1, t, t+1, t+2. B: iniciadas_t sobre Δln alquiler en t-1, t-2.

Coeficientes con p Holm < 0,05: 0 de 14.

**Conclusión (C4, ANALIZADA, NO CONCLUYENTE).** Se describe el orden temporal; no se estima ningún efecto de construir. Retardos (t-2, t-1) y adelantos (t+1, t+2): ninguno distinto de cero (p Holm 1.00 el menor). El contemporáneo es 0.0027 (p=0.041; p Holm 0.57), no robusto al ajuste múltiple. En la inversa (B), el crecimiento previo del alquiler tampoco predice las iniciadas (p Holm 1,00; los coeficientes B son enormes en escala porque Δln alquiler es ~0,05). Lectura: con N≈175-280 no se detecta orden temporal en ningún sentido; la PIP de iniciadas en alquiler (M2) no indica que construir suba el alquiler ni la dirección contraria.
