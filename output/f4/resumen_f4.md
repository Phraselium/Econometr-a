# F4 - Oferta (P3): déficit de vivienda y elasticidad de la oferta

Generado por `src/f4_oferta.py` (semilla 20261009). Todo es **asociación** salvo lo indicado en 'Nivel de evidencia'.

## Respuesta corta a P3

1. **Déficit 2021-2025 (flujo acumulado de Δhogares − terminadas, sin equilibrio inicial supuesto).** Principal (EPA corregida):
   **866,100 viviendas** (4.4 % de los hogares EPA 2025T4); con Δ2021T1=0: 831,500;
   con ECP 60131 como stock a 1 de enero (H 1-ene-2026 − H 1-ene-2021 = 1,222,836): 810,936; con Δparque MIVAU: 802,152.
   Extensión a 2026T2 (principal): 970,564. BdE: ~750.000 (IA 2025) y 700.000 (IEF otoño 2025). Las diferencias NO se ajustan (ver abajo).
2. **Elasticidad de la oferta** (iniciadas libres MIVAU, precio real retardado, DOLS ±2, HAC4, muestra común 2009Q4-2025Q4, N=63):
   iniciadas k=4: **1.44** (EE 0.21); terminadas k=8: 4.26 (0.26);
   permisos k=4: 3.11 (0.41). Rango de las 6 especificaciones DOLS por variable (precio ipv, con y sin tendencia): iniciadas 1.44-2.05,
   terminadas 4.12-4.29, permisos 3.11-4.05.
   **El DOLS principal es DESCRIPTIVO**: para la especificación principal (iniciadas k=4) la cointegración es 1 de 3 contrastes (por la regla de decisiones.md no hay cointegración) y la velocidad del ECM no es significativa, así que los t del DOLS en niveles no tienen la distribución nominal. Robustez en Δ4 (OLS-HAC(8), N=61): iniciadas k=4 β=1.39 (EE 0.63); el orden de magnitud (>1) no es solo un artefacto de los niveles, pero con menor precisión. Son varias veces el 0,45 del BdE, pero **no son comparables en concepto** (ver contraste).
3. **Evidencia sobre 0,45:** nuestro rango no lo valida ni lo refuta como elasticidad de la inversión residencial; con 2014T1+ la elasticidad de iniciadas es 2.36 (DOLS ±1, EE 0.50), todavía alejada de 0,45.

## 1. Déficit acumulado 2021-2025

Definición (decisiones.md, F4): déficit = Σ(Δhogares − terminadas), en viviendas; positivo = faltan viviendas. `hogares_epa` está en miles y se multiplica por 1.000.
**Corrección del cambio de 2021 (documentada):** la EPA cambia de definición de hogar y de factores de elevación en 2021T1 (`quiebre_epa_2021`); el Δ de 2021T1 de la serie es -207,800 hogares (salto de nivel, no creación de hogares).
Principal: Δ2021T1 := media de Δ en 2020T2, 2020T3, 2020T4 y 2021T2 = 34,600. Variante (a'): Δ2021T1 = 0. La serie sin corregir se da solo como referencia (a'').

### Tabla por año (principal)

|           |   delta_hogares |   terminadas |   deficit_anual |   deficit_acum_desde_2021 |   delta_hogares_sin_correccion |
|:----------|----------------:|-------------:|----------------:|--------------------------:|-------------------------------:|
| 2021      |         307,800 |       84,091 |         223,709 |                   223,709 |                         65,400 |
| 2022      |         311,100 |       79,935 |         231,165 |                   454,874 |                        311,100 |
| 2023      |         265,400 |       80,473 |         184,927 |                   639,801 |                        265,400 |
| 2024      |         135,500 |       86,609 |          48,891 |                   688,692 |                        135,500 |
| 2025      |         258,200 |       80,792 |         177,408 |                   866,100 |                        258,200 |
| 2026T1-T2 |         144,600 |       40,136 |         104,464 |                   970,564 |                        144,600 |

### Variantes

| variante                                         | periodo                                     |   sum_delta_hogares |   sum_terminadas |   deficit |   pct_hogares_2025T4 |
|:-------------------------------------------------|:--------------------------------------------|--------------------:|-----------------:|----------:|---------------------:|
| (a) EPA corregida (PRINCIPAL)                    | 2021T1-2025T4                               |         1,278,000.0 |        411,900.0 | 866,100.0 |                  4.4 |
| (a) EPA corregida (PRINCIPAL)                    | 2021T1-2026T2                               |         1,422,600.0 |        452,036.0 | 970,564.0 |                  4.9 |
| (a') EPA con Δ2021T1 = 0                         | 2021T1-2025T4                               |         1,243,400.0 |        411,900.0 | 831,500.0 |                  4.2 |
| (a') EPA con Δ2021T1 = 0                         | 2021T1-2026T2                               |         1,388,000.0 |        452,036.0 | 935,964.0 |                  4.7 |
| (a'') EPA sin corregir (solo referencia)         | 2021T1-2025T4                               |         1,035,600.0 |        411,900.0 | 623,700.0 |                  3.1 |
| (a'') EPA sin corregir (solo referencia)         | 2021T1-2026T2                               |         1,180,200.0 |        452,036.0 | 728,164.0 |                  3.7 |
| (b) ECP 60131 (stock a 1 de enero)               | 2021T1-2025T4 (H 1-ene-2026 − H 1-ene-2021) |         1,222,836.0 |        411,900.0 | 810,936.0 |                  4.1 |
| (b) ECP 60131 (stock a 1 de enero)               | 2021T1-2026T2 (H 1-jul-2026 − H 1-ene-2021) |         1,335,637.0 |        452,036.0 | 883,601.0 |                  4.5 |
| (c) Δparque MIVAU anual − Δhogares EPA corregida | 2021-2025                                   |         1,278,000.0 |        475,848.0 | 802,152.0 |                  4.0 |

- (b) ECP 60131 es un **stock a día 1 del trimestre** (fecha 2021-01-01 = 2021T1): los hogares de 2021-2025 son H(1-ene-2026) − H(1-ene-2021) = 19.762.059 − 18.539.223 = 1,222,836, año completo y sin imputar; déficit 810,936. La extensión a 2026T2 usa H(1-jul-2026).
- Sensibilidad de la corrección de la EPA (3 trimestres anteriores + 1 posterior, como se programó; decisiones.md dice '4 trimestres adyacentes' sin precisar la ventana): con ventana simétrica 2+2 el déficit sería 884.075 y con 4 posteriores 919.825 (cálculo de la revisión independiente); la cifra principal queda en el extremo bajo.
- (c) Δparque MIVAU anual (31-dic) − Δhogares EPA corregida; el parque incluye secundarias y vacías, y su Δ supera a las terminadas libres en 10.000-16.000 viviendas/año (tabla `parque_vs_terminadas`), consistente con protegidas y otros ajustes (no cuantificado: no hay protegidas en raw).
- (d) **Protegidas:** `data/raw/mivau_*` solo contiene tablas de vivienda LIBRE (iniciadas 32100500, terminadas 32101000); no hay protegidas, así que no se han podido añadir. Las terminadas totales serían mayores y el déficit principal una cota superior en esa magnitud.

### Contraste con el Banco de España (sin ajustar)

| concepto                                            |      BdE |   este_trabajo_principal | nota                                                                                                             |    diferencia |
|:----------------------------------------------------|---------:|-------------------------:|:-----------------------------------------------------------------------------------------------------------------|--------------:|
| Déficit acumulado 2021-2025                         | 7.5e+05  |                8.661e+05 | BdE IA 2025 p. 157: terminadas − creación neta de hogares (signo cambiado)                                       |     1.161e+05 |
| Creación neta de hogares 2025                       | 2.4e+05  |                2.582e+05 | Nosotros: EPA corregida; la fuente de hogares del BdE es una inferencia (ECP a 1 de enero, ver filas siguientes) |     1.82e+04  |
| Viviendas terminadas 2025                           | 9.2e+04  |                8.079e+04 | Nosotros: SOLO viviendas libres MIVAU (sin protegidas)                                                           |    -1.121e+04 |
| Creación neta de hogares 2025 (ECP a 1 de enero)    | 2.4e+05  |                2.41e+05  | INFERENCIA: ECP 60131 H(1-ene-2026) − H(1-ene-2025); el BdE no nombra la operación estadística                   | 1,013         |
| Media anual de hogares 2021-2024 (ECP a 1 de enero) | 2.45e+05 |                2.455e+05 | INFERENCIA, idem; BdE p. 157: 'promedio anual de 245.000 entre 2021 y 2024'                                      |   455.8       |
| Déficit en % de hogares                             | 3.7      |                4.36      | % sobre hogares EPA 2025T4                                                                                       |     0.66      |
| Déficit 2021-2025 (IEF otoño 2025)                  | 7e+05    |                8.661e+05 | IEF con datos del 1S 2025; periodo y fuente distintos                                                            |     1.661e+05 |

Diferencias, documentadas y no ajustadas:
- El BdE (IA 2025, gráficos 2.10 y 2.11, p. 155 y 157) cita como fuente 'INE y Ministerio de Transportes y Movilidad Sostenible' y define la diferencia como viviendas terminadas menos creación neta de hogares, pero **no nombra la operación estadística concreta**. Lo que sigue es **inferencia nuestra**.
- **Fuente de hogares (inferencia):** la ECP 60131 a 1 de enero reproduce los 240.000 de 2025 (241,013) y el promedio de ≈245.000 de 2021-2024 (245,456); la EPA corregida da 258,200 en 2025.
- **Terminadas:** MIVAU libres (80,792 en 2025) frente a 92.000 del BdE. Prensa cita 100.980 terminadas (libres y protegidas) en 2024 en el boletín anual del Observatorio de Vivienda y Suelo (MIVAU): **NO VERIFICADA** (no está en data/raw). Nuestras libres de 2024 son 86.609.
- **Descomposición de la diferencia de 116.100 (866.100 − 750.000):** ≈ +55.164 por la fuente de hogares (EPA corregida 1.278.000 frente a ECP 1.222.836) y ≈ +60.936 por la vivienda protegida no incluida (terminadas implícitas del BdE ≈ 472.836 frente a 411.900 libres; incluye el redondeo de 'unas 750.000'). Es una descomposición contable, no una verificación de las fuentes del BdE. Con ECP y terminadas libres el déficit es 810,936.
- **Periodo:** el IEF (700.000) usa datos hasta el primer semestre de 2025: periodo distinto.
| componente           |   este_trabajo |   BdE_implicito |   contribucion_a_deficit_nuestro_menos_BdE | nota                                                                                                     |
|:---------------------|---------------:|----------------:|-------------------------------------------:|:---------------------------------------------------------------------------------------------------------|
| Δhogares 2021-2025   |      1,278,000 |       1,222,836 |                                     55,164 | fuente de hogares: EPA corregida frente a ECP a 1 de enero (implícita en el BdE: inferencia)             |
| Terminadas 2021-2025 |        411,900 |         472,836 |                                     60,936 | implícito BdE = ΔECP − 750.000; diferencia ≈ viviendas protegidas no incluidas (y redondeo de '750.000') |

- La corrección de 2021 pesa 242,400 viviendas: sin ella el déficit sería 623,700 (por debajo de 750.000); no se usa como principal porque incorpora un salto metodológico, y no se ajusta hacia el BdE.
- Un 'déficit en niveles' requiere un equilibrio inicial; aquí solo se da el flujo acumulado desde 2021.

### Serie larga (contexto)

`serie_larga_desequilibrio.csv/png`: desequilibrio anual Δhogares − terminadas (2008+) y Δhogares − Δparque (2003+). Los acumulados desde 2008 y desde 2014 son **escenarios con equilibrio supuesto en el año anterior (2007 / 2013)**, no estimaciones; ver columnas `ESCENARIO_*`.

## 2. Elasticidad de la oferta

Muestra común 2009Q4-2025Q4 (N=63; la impone el retardo máximo del precio, 8 trimestres, y ±2 adelantos/retardos; se excluyen 2016T2 y 2017T2 sin iniciadas en las tres variables dependientes). Precio real = ln IPV − ln deflactor; costes reales = ln costes − ln deflactor; tipo hipotecario real; dummies trimestrales. Principales declaradas antes de estimar: k=4 (iniciadas, permisos), k=8 (terminadas).

### DOLS (tabla completa en `dols_resultados.csv`) - DESCRIPTIVO

La cointegración de la especificación principal es 1/3 (evidencia mixta) y el ECM no es significativo (iniciadas k=4); los t del DOLS no son válidos como inferencia de un vector de cointegración. Los DOLS k=0 (3/3) y k=2 (2/3) sí cointegran y dan 2,05 y 1,81. Se presentan como descripción de la asociación.

| dep        |   k | tendencia   |   beta |    EE |        p |   beta_costes |   beta_tipo |   n |   r2_adj |   rmse_1paso |
|:-----------|----:|:------------|-------:|------:|---------:|--------------:|------------:|----:|---------:|-------------:|
| visados    |   0 | False       |   2.05 | 0.221 | 2.03e-20 |         -3.18 |     -0.156  |  63 |    0.918 |        0.256 |
| visados    |   0 | True        |   1.93 | 0.167 | 1.31e-30 |         -4.32 |     -0.123  |  63 |    0.926 |        0.263 |
| visados    |   2 | False       |   1.81 | 0.208 | 3.46e-18 |         -2.47 |     -0.151  |  63 |    0.911 |        0.253 |
| visados    |   2 | True        |   1.76 | 0.157 | 5.11e-29 |         -3.93 |     -0.116  |  63 |    0.922 |        0.263 |
| visados    |   4 | False       |   1.44 | 0.206 | 2.35e-12 |         -2.39 |     -0.157  |  63 |    0.88  |        0.273 |
| visados    |   4 | True        |   1.53 | 0.195 | 4.1e-15  |         -4.64 |     -0.109  |  63 |    0.906 |        0.285 |
| terminadas |   4 | False       |   4.29 | 0.321 | 1.22e-40 |         -6.19 |     -0.0727 |  63 |    0.879 |        0.316 |
| terminadas |   4 | True        |   4.2  | 0.215 | 1.28e-84 |         -3.9  |     -0.122  |  63 |    0.903 |        0.284 |
| terminadas |   6 | False       |   4.23 | 0.297 | 5.81e-46 |         -8.06 |     -0.13   |  63 |    0.884 |        0.322 |
| terminadas |   6 | True        |   4.12 | 0.238 | 4.64e-67 |         -6.3  |     -0.175  |  63 |    0.9   |        0.285 |
| terminadas |   8 | False       |   4.26 | 0.261 | 5.44e-60 |         -9.77 |     -0.177  |  63 |    0.881 |        0.297 |
| terminadas |   8 | True        |   4.17 | 0.232 | 5e-72    |         -8.99 |     -0.199  |  63 |    0.883 |        0.288 |
| permisos   |   0 | False       |   4.05 | 0.313 | 2.41e-38 |          4.9  |      0.0225 |  63 |    0.854 |        0.383 |
| permisos   |   0 | True        |   3.98 | 0.3   | 2.57e-40 |          4.29 |      0.0399 |  63 |    0.852 |        0.425 |
| permisos   |   2 | False       |   3.62 | 0.369 | 1.04e-22 |          5.25 |     -0.0016 |  63 |    0.82  |        0.413 |
| permisos   |   2 | True        |   3.57 | 0.338 | 4.24e-26 |          3.71 |      0.035  |  63 |    0.826 |        0.45  |
| permisos   |   4 | False       |   3.11 | 0.406 | 1.94e-14 |          4.73 |     -0.0283 |  63 |    0.75  |        0.462 |
| permisos   |   4 | True        |   3.23 | 0.424 | 2.45e-14 |          1.56 |      0.0397 |  63 |    0.786 |        0.476 |

Robustez con valor tasado real: ver `dols_resultados.csv` (precio='tasado'); coeficientes mayores (iniciadas 2.23). Muestra larga de permisos (2003T4+, tasado real): 5.02-6.29.
`rmse_1paso` = error de predicción a un paso con regresores efectivos (ventana expansiva desde 2018T1): es condicional, no fuera de muestra genuino.

### Regresión en Δ4 (OLS-HAC(8), misma muestra Δ4 que el IV)

| modelo               | dep        |   k |   beta |   EE_HAC8 |      p |   n |   r2_adj |
|:---------------------|:-----------|----:|-------:|----------:|-------:|----:|---------:|
| ols_d4_visados_k0    | visados    |   0 |   2.52 |     0.353 | 0      |  61 |   0.444  |
| ols_d4_visados_k2    | visados    |   2 |   1.99 |     0.532 | 0.0002 |  61 |   0.252  |
| ols_d4_visados_k4    | visados    |   4 |   1.39 |     0.633 | 0.0277 |  61 |   0.0981 |
| ols_d4_terminadas_k4 | terminadas |   4 |   3.2  |     0.465 | 0      |  61 |   0.441  |
| ols_d4_terminadas_k6 | terminadas |   6 |   3.08 |     0.774 | 0.0001 |  61 |   0.407  |
| ols_d4_terminadas_k8 | terminadas |   8 |   2.53 |     0.968 | 0.0091 |  61 |   0.266  |
| ols_d4_permisos_k0   | permisos   |   0 |   2.78 |     0.486 | 0      |  61 |   0.328  |
| ols_d4_permisos_k2   | permisos   |   2 |   2.83 |     0.506 | 0      |  61 |   0.326  |
| ols_d4_permisos_k4   | permisos   |   4 |   2.74 |     0.655 | 0      |  61 |   0.295  |

### ECM

| dep        |   k |     ect |   EE_ect |    p_ect |   dP_corto |   EE_dP |     p_dP |   n |   r2_adj |   DW |
|:-----------|----:|--------:|---------:|---------:|-----------:|--------:|---------:|----:|---------:|-----:|
| visados    |   0 | -0.197  |   0.0667 | 0.00317  |       2.38 |   0.624 | 0.000134 |  59 |    0.309 | 2.05 |
| visados    |   2 | -0.159  |   0.0696 | 0.022    |       2.68 |   0.713 | 0.000168 |  59 |    0.291 | 1.99 |
| visados    |   4 | -0.0754 |   0.0595 | 0.205    |       1.25 |   0.639 | 0.0495   |  59 |    0.186 | 1.87 |
| terminadas |   4 | -0.314  |   0.0681 | 4.06e-06 |       2.51 |   1.18  | 0.033    |  59 |    0.525 | 1.99 |
| terminadas |   6 | -0.238  |   0.0813 | 0.00338  |       2.76 |   0.882 | 0.00175  |  59 |    0.467 | 1.92 |
| terminadas |   8 | -0.193  |   0.072  | 0.00731  |       2.82 |   1.06  | 0.0078   |  59 |    0.436 | 1.93 |
| permisos   |   0 | -0.13   |   0.0444 | 0.00346  |       2.02 |   0.584 | 0.000533 |  59 |    0.304 | 2    |
| permisos   |   2 | -0.106  |   0.0427 | 0.0129   |       2.35 |   0.647 | 0.000285 |  59 |    0.331 | 1.96 |
| permisos   |   4 | -0.0646 |   0.0399 | 0.105    |       1.49 |   0.829 | 0.072    |  59 |    0.23  | 2.02 |

La velocidad de ajuste (ect) es negativa en todas; para iniciadas con k=4 no es significativa (p=0.21).

### IV (2SLS, HAC 4) - desplazadores de demanda

Instrumentos: ln ocupados, ln pob_extranj, ln renta real del hogar, retardados max(k,4) trimestres; 3 instrumentos para 1 endógena. F de primera etapa robusta; J de Hansen con pesos HAC.
| dep        |   k | forma   |   beta |    EE |        p |    F1 |    J_p |   n | tendencia   |
|:-----------|----:|:--------|-------:|------:|---------:|------:|-------:|----:|:------------|
| visados    |   0 | niveles |   2.44 | 0.396 | 7.72e-10 | 106   | 0.123  |  63 | False       |
| visados    |   0 | niveles |   1.86 | 0.226 | 2.22e-16 | 164   | 0.0394 |  63 | True        |
| visados    |   2 | niveles |   2.37 | 0.545 | 1.36e-05 |  38.2 | 0.125  |  63 | False       |
| visados    |   2 | niveles |   1.7  | 0.256 | 3.27e-11 | 429   | 0.0384 |  63 | True        |
| visados    |   4 | niveles |   2.22 | 0.663 | 0.000786 |  28.6 | 0.0861 |  63 | False       |
| visados    |   4 | niveles |   1.6  | 0.289 | 3.4e-08  | 401   | 0.0423 |  63 | True        |
| terminadas |   4 | niveles |   4.16 | 0.508 | 2.22e-16 |  28.6 | 0.145  |  63 | False       |
| terminadas |   4 | niveles |   4.07 | 0.37  | 0        | 401   | 0.117  |  63 | True        |
| terminadas |   6 | niveles |   4.22 | 0.426 | 0        |  50.1 | 0.0482 |  63 | False       |
| terminadas |   6 | niveles |   4.01 | 0.363 | 0        | 289   | 0.0618 |  63 | True        |
| terminadas |   8 | niveles |   4.13 | 0.366 | 0        | 120   | 0.0514 |  63 | False       |
| terminadas |   8 | niveles |   3.84 | 0.32  | 0        | 652   | 0.0842 |  63 | True        |
| permisos   |   0 | niveles |   4.21 | 0.609 | 5e-12    | 106   | 0.403  |  63 | False       |
| permisos   |   0 | niveles |   3.68 | 0.34  | 0        | 164   | 0.145  |  63 | True        |
| permisos   |   2 | niveles |   4.17 | 0.851 | 9.4e-07  |  38.2 | 0.317  |  63 | False       |
| permisos   |   2 | niveles |   3.39 | 0.369 | 0        | 429   | 0.0706 |  63 | True        |
| permisos   |   4 | niveles |   4.07 | 1.05  | 9.9e-05  |  28.6 | 0.161  |  63 | False       |
| permisos   |   4 | niveles |   3.25 | 0.422 | 1.33e-14 | 401   | 0.0862 |  63 | True        |
| visados    |   0 | d4      |   1.08 | 0.961 | 0.259    |  10.1 | 0.0934 |  61 | False       |
| visados    |   2 | d4      |   1.04 | 0.88  | 0.239    |  15.7 | 0.106  |  61 | False       |
| visados    |   4 | d4      |   1.06 | 0.886 | 0.231    |  31.6 | 0.119  |  61 | False       |
| terminadas |   4 | d4      |   3.64 | 0.743 | 9.64e-07 |  31.6 | 0.142  |  61 | False       |
| terminadas |   6 | d4      |   4.06 | 1.18  | 0.000571 |  31.6 | 0.0583 |  61 | False       |
| terminadas |   8 | d4      |   3.17 | 1.15  | 0.00584  |  53.6 | 0.168  |  61 | False       |
| permisos   |   0 | d4      |   4.35 | 1.5   | 0.00378  |  10.1 | 0.19   |  61 | False       |
| permisos   |   2 | d4      |   3.81 | 1.15  | 0.000939 |  15.7 | 0.208  |  61 | False       |
| permisos   |   4 | d4      |   3.61 | 1.12  | 0.00122  |  31.6 | 0.218  |  61 | False       |

Lectura: en niveles, la F es alta (≥28), pero las tres variables están tendenciales (probable regresión espuria de primera etapa) y con tendencia el J rechaza en iniciadas. En Δ4, la elasticidad de iniciadas cae a 1.06 (EE 0.89, no significativa) con F1=31.6-31.6.
**Exclusión (argumentación):** ocupados, población extranjera y renta desplazan la demanda de vivienda, pero también afectan directamente a la construcción (empleo y mano de obra del sector, crédito, costes). Por eso, aunque F≥10 y J no rechace, la identificación es **solo condicional a una exclusión discutible** y los instrumentos son de la misma familia (J con poca potencia). No se afirma causalidad.

**Instrumento defendible:** solo la renta real del hogar es defendible como desplazador de demanda excluido de la ecuación de oferta; ocupados y población extranjera pueden afectar directamente a la construcción (mano de obra del sector, demanda de obra), así que su exclusión es dudosa y el IV con los tres instrumentos no identifica. Con la renta como único instrumento no se ha reestimado aquí (no se añaden modelos); queda como línea futura.

### Cointegración de la ecuación de iniciadas (los tres contrastes)

| sistema                                         |   N |   EG_t |   EG_p |   J_traza0 |   J_cv95 |   J_rango_traza |   ARDL_F |   ARDL_I0_5 |   ARDL_I1_5 |   n_rechazos | decision                          |
|:------------------------------------------------|----:|-------:|-------:|-----------:|---------:|----------------:|---------:|------------:|------------:|-------------:|:----------------------------------|
| visados (k=0) [2 huecos interpolados solo aquí] |  74 |  -4.16 | 0.0421 |       58   |     47.9 |               2 |     8.67 |        2.88 |        4.01 |            3 | cointegración (3/3)               |
| visados (k=2) [2 huecos interpolados solo aquí] |  74 |  -3.88 | 0.086  |       59.1 |     47.9 |               2 |    12.6  |        2.88 |        4.01 |            2 | cointegración (2/3, discrepancia) |
| visados (k=4) [2 huecos interpolados solo aquí] |  74 |  -3.92 | 0.0771 |       49.6 |     47.9 |               1 |     3.77 |        3.23 |        4.32 |            1 | evidencia mixta (1/3)             |
| terminadas (k=8)                                |  70 |  -3.66 | 0.138  |       76.4 |     47.9 |               4 |     3.78 |        3.23 |        4.32 |            1 | evidencia mixta (1/3)             |
| permisos (k=4)                                  |  74 |  -2.66 | 0.592  |       45.9 |     47.9 |               0 |     1.9  |        3.8  |        4.81 |            0 | sin cointegración (0/3)           |

Regla de decisiones.md: se exige ≥2 de 3. Iniciadas k=0: 3/3; k=2: 2/3; **k=4 (principal): 1/3, evidencia mixta** (ARDL en zona inconclusa). Terminadas k=8: evidencia mixta; permisos k=4: sin cointegración. Por tanto la relación de largo plazo de DOLS **no está respaldada de forma robusta** para la especificación principal. Johansen sin dummies estacionales; para iniciadas se interpolaron 2 huecos solo en estos contrastes.

### Diagnósticos (modelos principales, DOLS)

visados_k4: BG(4), RESET, DW=0.83; terminadas_k8: BG(4), RESET, DW=1.07; permisos_k4: BG(4), DW=0.52. Tabla completa en `diagnosticos.csv`. Chow/Bai-Perron (ecuación estática, `chow.csv`, `bai_perron.csv`): rechazo de estabilidad en 2014T1 en las tres (p<0,01) y Bai-Perron fecha quiebres en 2013T1 y 2014T1 (permisos) y 2018-2022; el quiebre de 2008 (colapso) queda en el arranque de la muestra, y la submuestra 2014T1+ se presenta aparte.

## 3. Contraste con el BdE (0,45)

Referencia: BdE, Informe Anual 2025, p. 156: "España presentaría una elasticidad de la oferta a largo plazo aproximadamente de 0,45 ..." (cota superior de la respuesta actual), basada en Caldera y Johansson (2013) y Cavalleri, Cournède y Özsöğüt (2019): **ambas NO VERIFICADAS** (no comprobadas de forma independiente).

| Principal | OLS estático | DOLS ±2 | IV niveles (F1; J p) | IV Δ4 | DOLS ±1 2014T1+ |
|---|---|---|---|---|---|
| visados k=4 | 1.34 (0.27) | 1.44 (0.21) | 2.22 (0.66; 29; 0.09) | 1.06 (0.89) | 2.36 (0.50) |
| terminadas k=8 | 3.69 (0.34) | 4.26 (0.26) | 4.13 (0.37; 120; 0.05) | 3.17 (1.15) | 2.86 (0.28) |
| permisos k=4 | 2.58 (0.42) | 3.11 (0.41) | 4.07 (1.05; 29; 0.16) | 3.61 (1.12) | 3.18 (0.91) |

(EE HAC entre paréntesis.) Tabla completa con IC95 y p de H0: β=0,45 en `contraste_bde.csv`; figura `elasticidades_vs_bde.png`.
Por qué no son directamente comparables: (i) el BdE habla de una «elasticidad de la oferta a largo plazo» estimada con modelos macroeconómicos entre países (IA 2025, p. 156); que sea la elasticidad de la **inversión residencial** es una **inferencia nuestra** a partir del contexto del texto y de las fuentes citadas (NO VERIFICADAS), no algo que el BdE afirme (stock/flujo agregado) a precios reales de **largo plazo** entre países; la nuestra es la de **viviendas libres iniciadas** (un flujo muy volátil, cero en ciclos bajos) al precio real retardado; (ii) el colapso de 2008-2013 puede inflar la elasticidad de las **terminadas** (baja de 4.26 a 2.86 desde 2014T1), pero **no** la de iniciadas, que sube desde 2014T1 (DOLS 2.36, OLS 3.22, IV 3.47); por tanto el colapso no explica por sí solo la magnitud de las iniciadas; (iii) los permisos son un índice (2021=100) y las terminadas un flujo con retardo de obra; (iv) los regresores (precio real, costes reales, tipo real) no coinciden con la especificación de los trabajos citados (no verificados). **Quiebre 2008/2014:** estimar desde 2014T1 reduce la de terminadas y aumenta la de iniciadas; los resultados son sensibles a la submuestra y Chow rechaza estabilidad en 2014T1 en las tres ecuaciones.

**Flujo frente a stock (aritmética, sin estimar):** una elasticidad de flujo β de iniciadas implica que un +10 % de precio real se asocia con un +14.4 % de iniciadas anuales (iniciadas libres 2025: 121,827, es decir, +17,594 viviendas/año). Sobre el parque MIVAU a 31-dic-2025 (27,099,556 viviendas) eso es 0.06 % del parque: una elasticidad de flujo alta es compatible con una oferta de stock muy inelástica, y la elasticidad de flujo no es comparable con una elasticidad de stock.

**Signo de los costes en permisos:** en el DOLS de permisos el coeficiente de los costes reales es POSITIVO (principal k=4: 4.73), contrario al signo esperado (costes más altos deberían reducir la oferta): se interpreta como comovimiento de tendencias, no como efecto de costes (en iniciadas y terminadas es negativo).

### Corrección por búsqueda

Se registraron **128 modelos** en `output/registro_busqueda_f4.csv` (114 en la familia 'elasticidad'). Con H0: β=0, 100 de 114 siguen significativos tras Holm y 95 tras Bonferroni (N total=128). **Qué informa esto:** solo que, *si los p-valores fueran válidos*, el signo positivo no se debe a haber probado muchos modelos. Los p-valores de los modelos en niveles **no son válidos** sin cointegración (los t crecen con la muestra) y β=0 no es la hipótesis relevante. Lo informativo es la dispersión: las 102 estimaciones nacionales van de **1.04 a 6.66**; las del panel con efectos de tiempo van de -1.63 a 2.42. Tablas: `correccion_busqueda.csv`, `contraste_H0_045_principales.csv`.

Contraste de H0: β=0,45 en las especificaciones principales (Holm entre las 15):

| dep        |   k | estimador     |   beta |    EE |   p_H0_045 |   p_holm_H0_045 |
|:-----------|----:|:--------------|-------:|------:|-----------:|----------------:|
| visados    |   4 | OLS estático  |   1.34 | 0.268 |     0.0008 |          0.0058 |
| visados    |   4 | DOLS ±2       |   1.44 | 0.206 |     0      |          0      |
| visados    |   4 | IV niveles    |   2.22 | 0.663 |     0.0074 |          0.037  |
| visados    |   4 | IV Δ4         |   1.06 | 0.886 |     0.489  |          0.489  |
| visados    |   4 | OLS Δ4 (HAC8) |   1.39 | 0.633 |     0.136  |          0.273  |
| terminadas |   8 | OLS estático  |   3.69 | 0.338 |     0      |          0      |
| terminadas |   8 | DOLS ±2       |   4.26 | 0.261 |     0      |          0      |
| terminadas |   8 | IV niveles    |   4.13 | 0.366 |     0      |          0      |
| terminadas |   8 | IV Δ4         |   3.17 | 1.15  |     0.018  |          0.0722 |
| terminadas |   8 | OLS Δ4 (HAC8) |   2.53 | 0.968 |     0.032  |          0.096  |
| permisos   |   4 | OLS estático  |   2.58 | 0.421 |     0      |          0      |
| permisos   |   4 | DOLS ±2       |   3.11 | 0.406 |     0      |          0      |
| permisos   |   4 | IV niveles    |   4.07 | 1.05  |     0.0005 |          0.0043 |
| permisos   |   4 | IV Δ4         |   3.61 | 1.12  |     0.0046 |          0.0279 |
| permisos   |   4 | OLS Δ4 (HAC8) |   2.74 | 0.655 |     0.0005 |          0.0043 |

No se calculó Romano-Wolf.

## 4. Panel CCAA (robustez)

Δ4 ln (terminadas / iniciadas) por CCAA sobre Δ4 ln IPV CCAA retardado (0, 4, 8 trimestres); EE cluster por CCAA y Driscoll-Kraay (bandwidth 4) (17 CCAA).
| dep        |   lag_trim | efectos        |    beta |   EE_cluster |   p_cluster |   EE_DK |     p_DK |    n |   CCAA |
|:-----------|-----------:|:---------------|--------:|-------------:|------------:|--------:|---------:|-----:|-------:|
| terminadas |          0 | FE CCAA+tiempo |  2.42   |        1.03  |    0.019    |   1.45  | 0.0956   | 1122 |     17 |
| terminadas |          0 | FE CCAA        |  2.71   |        0.282 |    0        |   0.588 | 4.4e-06  | 1122 |     17 |
| terminadas |          4 | FE CCAA+tiempo |  0.432  |        0.846 |    0.61     |   1.1   | 0.693    | 1122 |     17 |
| terminadas |          4 | FE CCAA        |  2.57   |        0.235 |    0        |   0.495 | 2.58e-07 | 1122 |     17 |
| terminadas |          8 | FE CCAA+tiempo | -0.0818 |        0.807 |    0.919    |   1.16  | 0.944    | 1122 |     17 |
| terminadas |          8 | FE CCAA        |  2      |        0.187 |    0        |   0.734 | 0.00647  | 1122 |     17 |
| visados    |          0 | FE CCAA+tiempo |  1.59   |        0.864 |    0.0663   |   1.38  | 0.249    | 1071 |     17 |
| visados    |          0 | FE CCAA        |  2.07   |        0.2   |    0        |   0.432 | 1.89e-06 | 1071 |     17 |
| visados    |          4 | FE CCAA+tiempo | -1.63   |        0.729 |    0.0253   |   0.654 | 0.0127   | 1071 |     17 |
| visados    |          4 | FE CCAA        |  1.18   |        0.215 |    5.04e-08 |   0.52  | 0.0233   | 1071 |     17 |
| visados    |          8 | FE CCAA+tiempo | -0.921  |        0.633 |    0.146    |   0.632 | 0.146    | 1071 |     17 |
| visados    |          8 | FE CCAA        |  0.123  |        0.236 |    0.603    |   0.597 | 0.837    | 1071 |     17 |

`p_WCB_webb`: wild cluster bootstrap (Webb, 9.999 réplicas, semilla 20261009, restringido bajo H0: β=0, cluster por CCAA), pre-registrado en decisiones.md.
Con efectos de tiempo la asociación desaparece (L4, L8 en terminadas; L8 en iniciadas) o cambia de signo (iniciadas L4: -1.63, p cluster 0.025, p WCB 0.032); con solo FE de CCAA es positiva y significativa salvo en iniciadas L8. **Lo estimado:** no hay evidencia de que las CCAA con mayor subida relativa de precios construyan relativamente más; no se puede atribuir la asociación nacional al 'ciclo común' (la identificación con efectos de tiempo viene de desviaciones regionales más ruidosas, hay atenuación, derrames entre CCAA y Δ4 solapadas).

## Nivel de evidencia

- OLS/DOLS/ECM: **asociación descriptiva** (cointegración 1/3 y ECM no significativo en la especificación principal) - no es una elasticidad estructural de oferta.
- IV: se informa F1 y J; en niveles todos pasan F≥10 y la mayoría J, pero la exclusión es discutible y la primera etapa en niveles es probablemente espuria por tendencias; en Δ4 el IV de iniciadas no es significativo. **No se afirma elasticidad identificada.**
- Déficit: aritmética contable con supuestos explícitos; sensible a la fuente de hogares (rango 802,152-866,100 en las variantes con corrección).

## Problemas abiertos

1. Sin viviendas protegidas en raw: las terminadas totales y el déficit no son directamente comparables con el BdE.
2. La fuente de hogares (ECP a 1 de enero) y la cobertura de terminadas del BdE son inferencias nuestras (el BdE no nombra la operación); la cifra de 100.980 terminadas en 2024 es NO VERIFICADA.
3. Caldera-Johansson (2013) y Cavalleri et al. (2019): NO VERIFICADAS; la cifra 0,45 solo está respaldada por la cita literal del IA 2025.
4. Elasticidades de niveles muy altas, sin cointegración robusta y sensibles al periodo (en terminadas cae desde 2014, en iniciadas sube): interpretar con cautela; falta una especificación con stock de vivienda/suelo y restricciones regulatorias.
5. Instrumentos de la misma familia (J con poca potencia); wild cluster bootstrap con 17 clusters puede ser todavía poco fiable.
6. Johansen sin dummies estacionales; 2 huecos de iniciadas interpolados solo en los contrastes de cointegración.
7. Parque MIVAU: estimación derivada, parcialmente mecánica con las terminadas; sin dato de 2026.
