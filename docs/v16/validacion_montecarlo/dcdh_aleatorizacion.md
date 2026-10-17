# dcdh_aleatorizacion · Q6 · de Chaisemartin-D'Haultfoeuille continuo con aleatorización del calendario entre CCAA

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/dcdh_aleatorizacion.py)
```
Monte Carlo V16 (fase 5) · de Chaisemartin-D'Haultfoeuille (tratamiento continuo, no absorbente) con inferencia por aleatorización
del calendario entre CCAA, Q6.

Proceso generador (declarado en docs/v16/validacion_montecarlo/dcdh_aleatorizacion.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): 41 provincias de entrenamiento agrupadas en sus CCAA (9 no selladas + Ceuta y Melilla
  como clusters sin cambio de tipo); tratamiento = tipo general del ITP por CCAA y año 2011-2024, construido con las filas de
  intervenciones.csv (el último valor con fecha de efecto en el año o antes). Panel anual, 14 años.
  RESULTADO SIMULADO (log compraventas usadas anual): y_it = mu_i + delta_i t + g_i1 f_1t + g_i2 f_2t + u_c(i),t + s_it + e_it + beta_i D_it
    f_1, f_2 AR(1) rho 0,7, sd 0,10; g_i1 ~ N(1; 0,4); g_i2 = campo espacial (300 km) sd 0,5
    u_ct: choque CCAA-año AR(1) rho 0,5, sd 0,04 * exp(0,3 z_c - 0,045) (heterocedasticidad entre CCAA)
    s_it: campo espacial exp(-d/150 km), AR(1) rho 0,5, sd 0,04;  e_it: AR(1) rho 0,5, sd 0,06 * exp(0,3 z_i - 0,045); delta_i ~ N(0; 0,003)
  EFECTO (contemporáneo por punto de tipo): nulo = 0; alternativas -0,07 por punto (volumen, Fritzsche-Vandrei) y -0,01 (precio),
  beta_i = beta (1 + 0,5 z_i); la verdad es la media de beta_i ponderada por |dD| en las celdas que cambian.
Estimador DID_M continuo: beta = sum_{(g,t) con cambio} sign(dD)(dY - media de dY de los que no cambian en t) / sum |dD|; el año anterior a
  cada cambio no se usa como control (anticipación).
Inferencia: p-valor y IC por aleatorización: se reasignan los calendarios completos de tipo entre CCAA (B = 499 permutaciones al azar de
  las 11 CCAA/clusters); IC = beta +- cuantil 95 % de |beta permutado| (consistente con el contraste). No hay alternativa nombrada: si falla, NO APTO.
```

<!-- RESULTADOS -->
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
| escenario | beta | R | sesgo | rmse | cobertura | rechazo | ancho_medio_ic |
|---|---|---|---|---|---|---|---|
| nulo | 0.0000 | 2000 | 0.0002 | 0.0205 | 0.9225 | 0.0775 | 0.0698 |
| alt_vol_-0.07 | -0.0700 | 2000 | 0.0001 | 0.0215 | 0.9670 | 0.8720 | 0.0984 |
| alt_precio_-0.01 | -0.0100 | 1000 | -0.0008 | 0.0207 | 0.9250 | 0.1270 | 0.0698 |
| control_iid_nulo | 0.0000 | 1000 | 0.0004 | 0.0170 | 0.9240 | 0.0760 | 0.0565 |

## Veredicto
**NO APTO → diseño solo descriptivo**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{
 "principal": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": true,
  "fallos": [
   "tamaño 0.0775 fuera de [0,04; 0,06]"
  ],
  "tamano": 0.0775,
  "R_nulo": 2000,
  "cobertura_alt": 0.967,
  "R_alt": 2000,
  "cobertura_nulo": 0.9225,
  "sesgo_nulo": 0.0002181454105478,
  "rmse_nulo": 0.0205063355326322,
  "se_mc_tamano": 0.005978869040211535,
  "se_mc_cobertura": 0.003994433626936366
 }
}
```

## Notas y límites
Inferencia por aleatorización del calendario entre CCAA (11 clusters; 8 con cambios de tipo, 59 celdas de cambio). Q6 no tiene alternativa nombrada distinta: si falla, NO APTO. Tamaño 0.0775 (error MC 0.0060); cobertura bajo nulo 0.9225 y bajo beta=-0,07 0.9670. Control iid (sin factores, campos ni choques de CCAA): tamaño 0.076: el exceso de rechazo no viene de la dependencia simulada sino de que el calendario permutado no es intercambiable (distinto número de provincias por CCAA y calendarios con distinta dispersión de cambios). Potencia: 0.872 a -0,07 por punto (volumen) y 0.127 a -0,01 (precio). Con solo 8 CCAA con cambios la prueba tiene resolución limitada; cualquier uso de Q6 queda como descriptivo.

## Reproducción
`python3 src/v16/montecarlo/dcdh_aleatorizacion.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/dcdh_aleatorizacion/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.
