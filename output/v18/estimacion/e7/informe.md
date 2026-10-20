# E7 · Tipos de interés: proyección local con instrumento, SVAR con proxy y panel provincial

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.*

## Lectura

- **Primera etapa.** Sorpresa monetaria (mediana de Jarociński-Karadi, suma trimestral) sobre la variación trimestral del tipo hipotecario: π = -0.842 (signo contrario al esperado), F efectivo 2.58 (EHW tras aumentar con rezagos). Q5 (V16) dio F de 2,1 a 2,9 y V8, primera etapa de signo contrario: se repite la debilidad.

- **Comprobación previa por MDE (adenda 1.3).** E7-R1: MDE no detectable (potencia < 80 % en toda la rejilla) frente al umbral 2,0 (San Juan: −2 % por +100 pb) → NO ESTIMABLE por variación. E7-R2: MDE no detectable (potencia < 80 % en toda la rejilla) → NO ESTIMABLE por variación. E7-A2: MDE 67.81 frente a 2δ = 2,0. Se calculó y registró antes de estimar; las especificaciones no estimables salen de la familia de Holm y se publican como estimación informativa, fuera de clasificación.

- **Estimación a 8 trimestres (E7-R1).** 2SLS 1.28 % por +100 pb; conjunto AR 95 % (EHW) toda la recta (no acotado); p de AR en 0 = 0.906. Clase provisional: **NO ESTIMABLE**. Referencia: San Juan (2023), −2 %; no coherente con San Juan (2023) (-2.0), razón -0.64 (etiqueta, no decide). El −5 % del BCE va al lado sin función en I6.

- **SVAR con proxy (E7-R2).** Respuesta del precio a h = 8: -10.54; F robusto 0.28; AR 95 % toda la recta (no acotado); clase provisional **NO ESTIMABLE**.

- **Panel provincial (E7-A2).** β = -19.67 (IC95 t[32] -36.85 a -2.49; p de Webb 0.043); G = 33; clase **NO ESTIMABLE**; respuesta relativa entre provincias, sin el componente común.

## Herramientas (etiqueta de distorsión)

LP-IV con Newey-West (h + 1): NO APTO en el Monte Carlo de V16 y de V18 (tamaño 0,07-0,115 con instrumento fuerte); AR aumentado con EHW, el único cercano al nominal bajo el nulo (0,049-0,069), con cobertura bajo la alternativa de 0,77-0,96 por la atenuación con T = 108 (10 %, 22 % y 38 % a h = 4, 8 y 12). Se publica con esa etiqueta y la clasificación no se apoya en ella.

SVAR con proxy: NO APTO (AR por método delta: tamaño 0,057-0,072 con F ≈ 27, cobertura 0,87-0,90 bajo la alternativa; conservador con F ≈ 4). Panel: Webb y CR1 t con efectos de año, APTOS con 30-39 clusters.

## Tabla de especificaciones

| id | estado | muestra | N | h | beta_2sls | se_nw | F_efectivo | ar_tipo | ar_lo | ar_hi | p_ar0 | p_holm | mde | estimable | clasificacion_v18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E7-R1 | principal | 1999Q1-2024Q2 | 102 | 8 | 1.2765 | 12.1453 | 2.5761 | recta | — | — | 0.9061 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-v1 | variante | 1999Q1-2024Q2 | 86 | 8 | -0.9132 | 12.1343 | 1.8855 | recta | — | — | 0.9383 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-v3 | variante | 1999Q1-2024Q2 | 102 | 8 | 13.2932 | 15.0248 | 0.9288 | recta | — | — | 0.3335 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-v5 | variante | 1999Q1-2024Q2 | 102 | 8 | 126.6086 | 1393.1228 | 0.0051 | recta | — | — | 0.5362 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-v7 | variante | 1999Q1-2024Q2 | 102 | 8 | 3.269 | 7.8122 | 1.6266 | recta | — | — | 0.6324 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-v8 | variante | 1999Q1-2025Q2 | 106 | 4 | 9.4589 | 11.5548 | 2.4745 | no_acotado | -40.2494 | -8.6625 | 0.2697 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-v9 | variante | 1999Q1-2023Q2 | 98 | 12 | -5.4118 | 12.1215 | 2.573 | recta | — | — | 0.6343 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-v6 | variante | 1999Q1-2024Q2 | 102 | 8 | 1.2765 | 12.1453 | 2.5761 | recta | — | — | 0.9061 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-ipv | principal | 2008Q1-2024Q2 | 66 | 8 | 0.1671 | 81.5856 | 0.0346 | recta | — | — | 0.999 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-cv | principal | 2008Q1-2024Q2 | 66 | 8 | -73.7383 | 295.567 | 0.1496 | recta | — | — | 0.7832 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R1-alq | principal | 2003Q1-2024Q2 | 86 | 8 | 29.1878 | 29.303 | 0.3659 | no_acotado | -2.4475 | 2.0878 | 0.0436 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-P-Q5 | coprincipal | 2000Q1-2025Q2 | 102 | 4 | -12.0289 | 6.0158 | 23.2219 | acotado | -24.0561 | 2.3352 | 0.0885 | 0.2655 | 31.8323 | — | no se clasifica |
| E7-P-H8-5 | coprincipal | 1999Q1-2024Q2 | 102 | 4-8 (media) | 2.0836 | 8.4108 | 1.9666 | recta | — | — | 0.7725 | 1 | no detectable (potencia < 80 % en toda la rejilla) | — | no se clasifica |
| E7-P-H8-6 | coprincipal | 2002Q3-2024Q2 | 88 | 4-8 (media) | 1.7048 | 3.1546 | 0.623 | recta | — | — | 0.6726 | 1 | no detectable (potencia < 80 % en toda la rejilla) | — | no se clasifica |
| E7-R2 | principal | 2007Q1-2025Q3 | 73 | 8 | -10.539 | — | 0.2765 | recta | — | — | 0.5062 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R2-v1 | variante | 2007Q1-2025Q3 | 73 | 8 | -16.1136 | — | 0.2182 | recta | — | — | 0.2912 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R2-v3 | variante | 2007Q1-2025Q3 | 73 | 8 | 42.5953 | — | 0.5463 | no_acotado | -17.0312 | -2.9609 | 0.0697 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-R2-v4 | variante | 2007Q1-2025Q3 | 73 | 8 | -5.4935 | — | 1.0364 | recta | — | — | 0.6851 | — | no detectable (potencia < 80 % en toda la rejilla) | False | NO ESTIMABLE |
| E7-A2-h4 | variante | 2002Q2-2025Q2 | 3069 | 4 | 1.5649 | — | — | — | — | — | 0.8398 | — | 43.6008 | False | NO ESTIMABLE |
| E7-A2 | principal | 2002Q2-2024Q2 | 2937 | 8 | -19.6738 | — | — | — | — | — | 0.0433 | — | 67.8082 | False | NO ESTIMABLE |
| E7-A2-h12 | variante | 2002Q2-2023Q2 | 2805 | 12 | -39.4939 | — | — | — | — | — | 0.001 | — | 89.9761 | False | NO ESTIMABLE |
| E7-A2-v2 | variante | 2002Q2-2024Q2 | 2848 | 8 | -17.8021 | — | — | — | — | — | 0.0691 | — | 74.2929 | False | NO ESTIMABLE |
| E7-A2-v3 | variante | 2002Q2-2024Q2 | 2937 | 8 | -11.99 | — | — | — | — | — | 0.1562 | — | 40.0816 | False | NO ESTIMABLE |
| E7-A2-v1 | variante | — | — | — | — | — | — | — | — | — | — | — | — | False | NO ESTIMABLE |
| E7-R1-v2 | variante | — | — | — | — | — | — | — | — | — | — | — | — | False | NO ESTIMABLE |
| E7-R2-v2 | variante | — | — | — | — | — | — | — | — | — | — | — | — | False | NO ESTIMABLE |
| E7-P-H8-7 | coprincipal | — | — | — | — | — | — | — | — | — | — | — | — | False | no se clasifica |
| E7-P-D5 | coprincipal | — | — | — | — | — | — | — | — | — | — | — | — | False | no se clasifica |
| E7-A3 | principal | — | — | — | — | — | — | — | — | — | — | — | — | False | NO ESTIMABLE |
| E7-A2-X1 | principal | — | — | — | — | — | — | — | — | — | — | — | — | False | NO ESTIMABLE |


## Diagnósticos del pre-registro

```json
{
 "series": {
  "y_p": {
   "adf_p_niveles": 0.0188,
   "adf_p_diferencias": 0.3806,
   "kpss_p_niveles": 0.0272
  },
  "hip": {
   "adf_p_niveles": 0.001,
   "adf_p_diferencias": 0.0,
   "kpss_p_niveles": 0.01
  },
  "eur": {
   "adf_p_niveles": 0.0713,
   "adf_p_diferencias": 0.0,
   "kpss_p_niveles": 0.01
  },
  "pib": {
   "adf_p_niveles": 0.4743,
   "adf_p_diferencias": 0.0,
   "kpss_p_niveles": 0.01
  },
  "infl": {
   "adf_p_niveles": 0.3417,
   "adf_p_diferencias": 0.0,
   "kpss_p_niveles": 0.1
  }
 },
 "placebos_R1": {
  "choque_adelantado_8": {
   "tipo": "adelantado",
   "beta": -27.9843,
   "p_ar0": 0.6971,
   "F": 0.1005,
   "n": 107,
   "ar": "toda la recta (no acotado)"
  },
  "poblacion_total": {
   "tipo": "poblacion",
   "beta": 2.1408,
   "p_ar0": 0.3049,
   "F": 3.1524,
   "n": 102,
   "ar": "toda la recta (no acotado)"
  }
 },
 "estabilidad_primera_etapa": {
  "2008Q1": 1.4947,
  "2015Q1": 3.635
 },
 "sensibilidad_a_la_identificacion": {
  "E7-R1": {
   "beta_2sls": 1.2765,
   "F": 2.5761,
   "ar": "toda la recta (no acotado)"
  },
  "E7-R1-v3": {
   "beta_2sls": 13.2932,
   "F": 0.9288,
   "ar": "toda la recta (no acotado)"
  },
  "E7-R1-v5": {
   "beta_2sls": 126.6086,
   "F": 0.0051,
   "ar": "toda la recta (no acotado)"
  },
  "E7-R1-v7": {
   "beta_2sls": 3.269,
   "F": 1.6266,
   "ar": "toda la recta (no acotado)"
  }
 },
 "sostenido_h12": {
  "razon": -2.1972,
  "se_delta": 4.026,
  "ic95": [
   -10.0883,
   5.6938
  ],
  "n": 98,
  "respuesta_propia_tipo_h12_por_pp_sorpresa": -2.1608,
  "nota": "razón de formas reducidas a h = 12; sin cambio sostenido más allá del horizonte estimado: «fuera del horizonte estimado», sin cifra"
 },
 "primera_etapa_signo": "V8 y Q5 ya dieron signo contrario o F de 2,1 a 2,9: aquí se publica la π estimada de cada especificación",
 "diferencial_soberano": "NO ESTIMABLE: no hay serie trimestral del diferencial soberano a 10 años en el repositorio (solo anual, irt_lt_mcby_a, sin clave en sellado_v18.json); se necesita la serie mensual del BCE",
 "I5_proporcion_mismo_signo_R1": {
  "proporcion": 0.7143,
  "variantes": [
   "E7-R1-v1",
   "E7-R1-v3",
   "E7-R1-v5",
   "E7-R1-v7",
   "E7-R1-v8",
   "E7-R1-v9",
   "E7-R1-v6"
  ],
  "nota": "v2 (diferencial soberano) es NO ESTIMABLE y v4 (mediana) coincide con la principal"
 }
}
```

## IRF a 12 trimestres (E7-R1, precio, % por +100 pb)

| h | beta | se_nw | ar | ar_lo | ar_hi | F | n |
|---|---|---|---|---|---|---|---|
| 0 | 4.6186 | 3.6237 | recta | — | — | 2.4781 | 107 |
| 1 | 10.0673 | 6.9565 | no_acotado | -17.0787 | -3.7855 | 2.4781 | 107 |
| 2 | 8.9065 | 7.7848 | no_acotado | -20.2135 | -6.1566 | 2.4781 | 107 |
| 3 | 9.706 | 9.8905 | no_acotado | -32.7512 | -5.0112 | 2.4781 | 107 |
| 4 | 9.4589 | 11.5548 | no_acotado | -40.2494 | -8.6625 | 2.4745 | 106 |
| 5 | 8.8846 | 11.8539 | no_acotado | -27.5017 | -15.0618 | 2.4526 | 105 |
| 6 | 6.954 | 12.5237 | no_acotado | -30.1689 | -18.8214 | 2.5396 | 104 |
| 7 | 3.8268 | 12.1316 | recta | — | — | 2.6058 | 103 |
| 8 | 1.2765 | 12.1453 | recta | — | — | 2.5761 | 102 |
| 9 | 1.3472 | 11.8586 | recta | — | — | 2.5434 | 101 |
| 10 | -2.4751 | 10.0061 | recta | — | — | 2.9306 | 100 |
| 11 | -2.4281 | 11.3876 | recta | — | — | 2.8541 | 99 |
| 12 | -5.4118 | 12.1215 | recta | — | — | 2.573 | 98 |


## Notas
- Clase provisional hasta I8 (réplica ciega, B6).
- Sorpresas: Jarociński y Karadi (2020), actualización con EA-MPD (Altavilla et al., 2019); sin licencia declarada: solo local.
- «Controlando el diferencial soberano» (v2): NO ESTIMABLE por falta de la serie trimestral; ver docs/v18/desviaciones_f_e7.md.
- Controles de la principal: PIB y inflación; el crédito nuevo empieza en 2003T1 y recortaría la muestra (desviación declarada).
