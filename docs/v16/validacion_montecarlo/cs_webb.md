# cs_webb · Q1c · Callaway-Sant'Anna con wild cluster bootstrap de Webb por provincia

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/cs_webb.py)
```
Monte Carlo V16 (fase 5) · Callaway-Sant'Anna con wild cluster bootstrap de Webb por provincia, Q1c.

Proceso generador (declarado en docs/v16/validacion_montecarlo/cs_webb.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): las 41 provincias de entrenamiento; trimestres 2019T1-2026T2 (30); tratamiento =
  provincia con alguna zona vigente, con la cohorte del primer trimestre completo posterior a la fecha de efecto (intervenciones.csv);
  comparación = nunca tratadas. Cada provincia es su propio cluster.
  RESULTADO SIMULADO (log compraventas trimestral): y_it = mu_i + delta_i t + g_i1 f_1t + g_i2 f_2t + s_it + e_it
    f_1, f_2: factores comunes AR(1) rho 0,8, sd 0,08; g_i1 ~ N(1; 0,4); g_i2 = campo espacial exp(-d/300 km) con sd 0,5
    s_it: campo gaussiano espacial exp(-d/150 km) entre centroides, AR(1) rho 0,6, sd 0,04
    e_it: AR(1) rho 0,5, sd marginal 0,06 * exp(0,3 z_i - 0,045); delta_i ~ N(0; 0,002) tendencia propia. Valores declarados.
  EFECTO: nulo = 0; alternativas 0,05 y 0,10 (log) con heterogeneidad tau_i = tau (1 + 0,5 z_i) y dinámica 1 - exp(-(e+1)/2) tras la entrada;
  la verdad es el ATT agregado muestral (misma ponderación que el estimador).
Estimador: ATT(g,t) con nunca tratadas y periodo base g-1, agregado «simple» (peso por tamaño de cohorte sobre las celdas t >= g).
Inferencia: multiplicador wild cluster bootstrap-t de Webb (6 puntos) sobre la función de influencia, B = 999, por provincia.
```

<!-- RESULTADOS -->
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
| escenario | tau | variante | R | sesgo | rmse | cobertura | rechazo | ancho_medio_ic |
|---|---|---|---|---|---|---|---|---|
| nulo | 0.0000 | a_multiplicador_IF | 2000 | 0.0012 | 0.0452 | 0.6855 | 0.3145 | 0.0938 |
| nulo | 0.0000 | b_WCR_nulo_impuesto | 2000 | 0.0012 | 0.0452 | 0.9325 | 0.0655 | 0.1284 |
| alt_005 | 0.0500 | a_multiplicador_IF | 2000 | 0.0003 | 0.0458 | 0.6905 | 0.4765 | 0.0951 |
| alt_005 | 0.0500 | b_WCR_nulo_impuesto | 2000 | 0.0003 | 0.0458 | 0.9015 | 0.1965 | 0.1428 |
| alt_010 | 0.1000 | a_multiplicador_IF | 1000 | -0.0019 | 0.0447 | 0.7320 | 0.7170 | 0.1024 |
| alt_010 | 0.1000 | b_WCR_nulo_impuesto | 1000 | -0.0019 | 0.0447 | 0.9080 | 0.4190 | 0.1753 |
| control_iid_nulo | 0.0000 | a_multiplicador_IF | 1000 | 0.0009 | 0.0260 | 0.7940 | 0.2040 | 0.0735 |
| control_iid_nulo | 0.0000 | b_WCR_nulo_impuesto | 1000 | 0.0009 | 0.0260 | 0.9770 | 0.0230 | 0.0944 |

## Veredicto
**NO APTO → diseño solo descriptivo**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{
 "principal_b": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.0655 fuera de [0,04; 0,06]",
   "cobertura 0.9015 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.0655,
  "R_nulo": 2000,
  "cobertura_alt": 0.9015,
  "R_alt": 2000,
  "cobertura_nulo": 0.9325,
  "sesgo_nulo": 0.0012394246068562,
  "rmse_nulo": 0.0452323578014545,
  "se_mc_tamano": 0.005532167296819575,
  "se_mc_cobertura": 0.0066632480818291625
 },
 "descartada_a": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.3145 fuera de [0,04; 0,06]",
   "cobertura 0.6905 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.3145,
  "R_nulo": 2000,
  "cobertura_alt": 0.6905,
  "R_alt": 2000,
  "cobertura_nulo": 0.6855,
  "sesgo_nulo": 0.0012394246068562,
  "rmse_nulo": 0.0452323578014545,
  "se_mc_tamano": 0.010382431073693675,
  "se_mc_cobertura": 0.010337063170939801
 }
}
```

## Notas y límites
Inferencia principal = wild cluster bootstrap de Webb por provincia con el nulo impuesto (variante b). La adenda no nombra alternativa para Q1c: si falla, el diseño es solo descriptivo. Variante a (multiplicador sobre la función de influencia sin restringir) descartada de entrada: tamaño 0.315 y cobertura 0.691, porque las cohortes de una sola provincia (4 de 5) tienen residuo de influencia cero y la varianza se subestima; se informa pero no se usa. Variante b: tamaño 0.0655, cobertura bajo nulo 0.9325, bajo tau=0,05 0.9015. Control de implementación sin dependencia (ruido iid): tamaño 0.023, cobertura 0.977 (el procedimiento es conservador sin dependencia y pierde la cobertura con dependencia transversal y espacial, con 8 tratadas en 5 cohortes y 33 comparaciones). Potencia (variante b): 0.197 a tau=0,05 y 0.419 a tau=0,10; sin magnitud de referencia comparable (la condición (b) no se cumple). Sesgo despreciable (0.0012); el fallo es de inferencia, no de punto.

## Reproducción
`python3 src/v16/montecarlo/cs_webb.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/cs_webb/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.
