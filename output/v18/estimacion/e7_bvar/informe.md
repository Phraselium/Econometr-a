# E7-R3 y E7-A1 · BVAR recursivo (réplica de San Juan, 2023 y ampliación a 2026T2)

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.*

## Lectura

- **Validación previa de la herramienta.** Monte Carlo de la cobertura de las bandas del BVAR (output/v18/montecarlo/bvar): **NO APTO**. Condición en que falla: T=60|rho=0.97|nulo|compraventas: cobertura 68 % 0.987 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|nulo|precio: cobertura 68 % 0.964 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|nulo|visados: cobertura 68 % 0.988 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|alternativa|compraventas: cobertura 90 % 0.952 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|alternativa|precio: cobertura 68 % 0.016 f… Por eso la estimación se publica **solo como informativa**: las bandas no deben leerse como intervalos con cobertura conocida.

- **E7-R3** (2008Q1-2022Q4, 52 filas): a 8 trimestres de +100 pb en el euríbor, precio -1.55 % (68 % [-2.28; -0.87], 90 % [-2.84; -0.38]), compraventas -4.83 % (68 % [-9.55; -0.45]), visados -6.63 % (68 % [-14.00; 0.63]). Referencia de San Juan: −2 %, −3 % y −11 % (intervalos al 68 %).
- **E7-A1** (2008Q1-2026Q2, 66 filas): a 8 trimestres de +100 pb en el euríbor, precio -0.32 % (68 % [-1.90; 1.21], 90 % [-2.98; 2.27]), compraventas -2.02 % (68 % [-7.26; 3.26]), visados -1.11 % (68 % [-8.55; 6.43]). Referencia de San Juan: −2 %, −3 % y −11 % (intervalos al 68 %).

- **Clase: ASOCIACIÓN** (tope fijado en el plan: identificación recursiva sin variación externa; fuera de la familia de Holm). Es una réplica de un resultado del Banco de España, y se dice. No hay p-valor: las bandas son de credibilidad.

## Diferencias con el original (desviaciones: docs/v18/desviaciones_e4_e7b_e10_e12.md)

- Muestra: 2008T1-2022T4 en lugar de 2004-2022 (compraventas desde 2007T1 y visados observados desde 2008T1; las interpoladas solo entran en robustez). R3-v2: 2008T1-2019T4.
- Crédito: flujo (base:credito_nuevo), no el saldo (R-27). IPC, no IPCA. Visados: faltan 2016T2 y 2017T2 y se omiten las filas afectadas.
- Choque: innovación recursiva del euríbor a 1 año normalizada a +100 pb en su impacto; San Juan escala un choque al tipo hipotecario: la unidad no es idéntica y I6 es solo una etiqueta.
- BVAR(2) con prior de Minnesota (λ = 0,2, suma de coeficientes con peso 0,5; variante laxa λ = 0,5) y tres ficticias estacionales: San Juan no declara el prior ni el orden de rezagos.

## Tabla de especificaciones (h = 8)

| id | estado | muestra | N | variable | mediana | lo68 | hi68 | lo90 | hi90 | p_respuesta_negativa | prior | solo_informativa | clasificacion_v18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E7-R3 | principal | 2008Q1-2022Q4 | 52 | precio | -1.551 | -2.28 | -0.867 | -2.837 | -0.382 | 0.98 | principal | True | ASOCIACIÓN |
| E7-R3-cv | principal | 2008Q1-2022Q4 | 52 | compraventas | -4.825 | -9.548 | -0.447 | -13.071 | 2.682 | 0.86 | principal | True | ASOCIACIÓN |
| E7-R3-vis | principal | 2008Q1-2022Q4 | 52 | visados | -6.628 | -14.002 | 0.626 | -19.309 | 6.122 | 0.82 | principal | True | ASOCIACIÓN |
| E7-R3-v1 | variante | 2008Q1-2022Q4 | 52 | precio | -1.543 | -2.582 | -0.498 | -3.406 | 0.255 | 0.92 | laxa | True | ASOCIACIÓN |
| E7-R3-v1-cv | variante | 2008Q1-2022Q4 | 52 | compraventas | -0.357 | -6.741 | 5.93 | -11.538 | 10.778 | 0.53 | laxa | True | ASOCIACIÓN |
| E7-R3-v1-vis | variante | 2008Q1-2022Q4 | 52 | visados | -4.771 | -14.385 | 5.18 | -21.615 | 13.03 | 0.69 | laxa | True | ASOCIACIÓN |
| E7-R3-v2 | variante | 2008Q1-2019Q4 | 40 | precio | -0.506 | -1.414 | 0.375 | -2.101 | 1.041 | 0.72 | principal | True | ASOCIACIÓN |
| E7-R3-v2-cv | variante | 2008Q1-2019Q4 | 40 | compraventas | 0.407 | -4.118 | 5.234 | -8.062 | 9.391 | 0.46 | principal | True | ASOCIACIÓN |
| E7-R3-v2-vis | variante | 2008Q1-2019Q4 | 40 | visados | -1.209 | -9.953 | 7.192 | -17.813 | 13.877 | 0.56 | principal | True | ASOCIACIÓN |
| E7-A1 | principal | 2008Q1-2026Q2 | 66 | precio | -0.321 | -1.897 | 1.206 | -2.981 | 2.27 | 0.58 | principal | True | ASOCIACIÓN |
| E7-A1-cv | principal | 2008Q1-2026Q2 | 66 | compraventas | -2.021 | -7.263 | 3.258 | -11.173 | 7.22 | 0.65 | principal | True | ASOCIACIÓN |
| E7-A1-vis | principal | 2008Q1-2026Q2 | 66 | visados | -1.108 | -8.553 | 6.431 | -14.092 | 11.994 | 0.56 | principal | True | ASOCIACIÓN |
| E7-A1-v1 | variante | 2008Q1-2026Q2 | 50 | precio | -0.634 | -2.037 | 0.725 | -3.062 | 1.711 | 0.68 | principal | True | ASOCIACIÓN |
| E7-A1-v1-cv | variante | 2008Q1-2026Q2 | 50 | compraventas | -3.035 | -7.983 | 1.87 | -12.005 | 5.499 | 0.74 | principal | True | ASOCIACIÓN |
| E7-A1-v1-vis | variante | 2008Q1-2026Q2 | 50 | visados | -3.219 | -9.011 | 2.536 | -13.455 | 7.123 | 0.71 | principal | True | ASOCIACIÓN |


## Diagnósticos del pre-registro

```json
{
 "series_adf_kpss": {
  "cv": {
   "adf_p_niveles": 0.9334,
   "adf_p_diferencias": 0.0004,
   "kpss_p_niveles": 0.01
  },
  "p": {
   "adf_p_niveles": 0.9145,
   "adf_p_diferencias": 0.5977,
   "kpss_p_niveles": 0.0905
  },
  "vis": {
   "adf_p_niveles": 0.7188,
   "adf_p_diferencias": 0.0005,
   "kpss_p_niveles": 0.0724
  },
  "pib": {
   "adf_p_niveles": 0.8958,
   "adf_p_diferencias": 0.0,
   "kpss_p_niveles": 0.01
  },
  "ipc": {
   "adf_p_niveles": 0.0313,
   "adf_p_diferencias": 0.0037,
   "kpss_p_niveles": 0.1
  },
  "eur": {
   "adf_p_niveles": 0.0062,
   "adf_p_diferencias": 0.0,
   "kpss_p_niveles": 0.1
  },
  "cred": {
   "adf_p_niveles": 0.514,
   "adf_p_diferencias": 0.0727,
   "kpss_p_niveles": 0.0868
  }
 },
 "estabilidad": {
  "R3_raiz_maxima_media_posterior": 0.943,
  "R3_proporcion_extracciones_explosivas": 0.15,
  "A1_raiz_maxima_media_posterior": 0.99,
  "A1_proporcion_extracciones_explosivas": 0.746
 },
 "sensibilidad_orden_R3_h8": {
  "euribor_primero": {
   "precio": {
    "mediana": -1.039,
    "lo68": -1.926,
    "hi68": -0.183,
    "lo90": -2.619,
    "hi90": 0.444,
    "p_negativa": 0.884
   },
   "compraventas": {
    "mediana": -3.912,
    "lo68": -9.324,
    "hi68": 0.908,
    "lo90": -13.933,
    "hi90": 4.319,
    "p_negativa": 0.792
   },
   "visados": {
    "mediana": -3.197,
    "lo68": -11.638,
    "hi68": 5.339,
    "lo90": -17.942,
    "hi90": 12.206,
    "p_negativa": 0.651
   }
  },
  "sin_credito": {
   "precio": {
    "mediana": -1.448,
    "lo68": -2.121,
    "hi68": -0.757,
    "lo90": -2.622,
    "hi90": -0.292,
    "p_negativa": 0.975
   },
   "compraventas": {
    "mediana": -4.788,
    "lo68": -9.411,
    "hi68": -0.406,
    "lo90": -12.974,
    "hi90": 2.859,
    "p_negativa": 0.86
   },
   "visados": {
    "mediana": -6.192,
    "lo68": -13.143,
    "hi68": 1.048,
    "lo90": -18.246,
    "hi90": 6.371,
    "p_negativa": 0.807
   }
  },
  "precio_primero": {
   "precio": {
    "mediana": -1.567,
    "lo68": -2.297,
    "hi68": -0.872,
    "lo90": -2.814,
    "hi90": -0.394,
    "p_negativa": 0.982
   },
   "compraventas": {
    "mediana": -4.727,
    "lo68": -9.343,
    "hi68": -0.486,
    "lo90": -13.083,
    "hi90": 2.675,
    "p_negativa": 0.865
   },
   "visados": {
    "mediana": -6.574,
    "lo68": -13.91,
    "hi68": 0.616,
    "lo90": -19.193,
    "hi90": 5.91,
    "p_negativa": 0.819
   }
  }
 },
 "I5_mismo_signo_precio_h8": {
  "R3": {
   "v1": true,
   "v2": true
  },
  "A1": true
 },
 "mc_bandas": {
  "veredicto": "NO APTO",
  "condicion": "T=60|rho=0.97|nulo|compraventas: cobertura 68 % 0.987 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|nulo|precio: cobertura 68 % 0.964 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|nulo|visados: cobertura 68 % 0.988 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|alternativa|compraventas: cobertura 90 % 0.952 fuera de [0.87; 0.93] (conservadora); T=60|rho=0.97|alternativa|precio: cobertura 68 % 0.016 fuera de [0.63; 0.73] (insuficiente) / cobertura 90 % 0.180 fuera de [0.87; 0.93] (insuficiente); T=60|rho=0.97|alternativa|visados: cobertura 68 % 0.420 fuera de [0.63; 0.73] (insuficiente); T=74|rho=0.97|nulo|compraventas: cobertura 68 % 0.981 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=74|rho=0.97|nulo|precio: cobertura 68 % 0.940 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 0.999 fuera de [0.87; 0.93] (conservadora); T=74|rho=0.97|nulo|visados: cobertura 68 % 0.977 fuera de [0.63; 0.73] (conservadora) / cobertura 90 % 1.000 fuera de [0.87; 0.93] (conservadora); T=74|rho=0.97|alternativa|compraventas: cobertura 68 % 0.608 fuera de [0.63; 0.73] (insuficiente) / cobertura 90 % 0.934 fuera de [0.87; 0.93] (conservadora); T=74|rho=0.97|alternativa|precio: cobertura 68 % 0.005 fuera de [0.63; 0.73] (insuficiente) / cobertura 90 % 0.117 fuera de [0.87; 0.93] (insuficiente); T=74|rho=0.97|alternativa|visados: cobertura 68 % 0.316 fuera de [0.63; 0.73] (insuficiente) / cobertura 90 % 0.825 fuera de [0.87; 0.93] (insuficiente)",
  "ruta": "output/v18/montecarlo/bvar/informe.md"
 },
 "gate_MDE_1.3": "No aplica de forma frecuentista: un BVAR con prior informativa no tiene un MDE por contraste. Se publican las bandas al 68 % y al 90 % y su anchura; la especificación no entra en la familia de Holm (tope ASOCIACIÓN) ni en B5. Declarado en docs/v18/desviaciones_e4_e7b_e10_e12.md.",
 "datos": {
  "filas_R3": 52,
  "filas_A1": 66,
  "visados_ausentes": [
   "2016T2",
   "2017T2"
  ],
  "credito": "flujo (credito_nuevo), no saldo"
 }
}
```

## Respuesta del precio (E7-R3, % por +100 pb del euríbor; mediana y bandas)

| h | mediana | lo68 | hi68 | lo90 | hi90 |
|---|---|---|---|---|---|
| 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 1 | -0.267 | -0.44 | -0.094 | -0.56 | 0.015 |
| 2 | -0.676 | -0.937 | -0.412 | -1.136 | -0.239 |
| 3 | -1.065 | -1.419 | -0.722 | -1.678 | -0.482 |
| 4 | -1.38 | -1.814 | -0.953 | -2.121 | -0.669 |
| 5 | -1.587 | -2.096 | -1.094 | -2.459 | -0.766 |
| 6 | -1.676 | -2.261 | -1.12 | -2.694 | -0.756 |
| 7 | -1.661 | -2.313 | -1.043 | -2.811 | -0.613 |
| 8 | -1.551 | -2.28 | -0.867 | -2.837 | -0.382 |
| 9 | -1.365 | -2.175 | -0.6 | -2.788 | -0.059 |
| 10 | -1.128 | -1.999 | -0.283 | -2.657 | 0.319 |
| 11 | -0.86 | -1.797 | 0.064 | -2.515 | 0.773 |
| 12 | -0.573 | -1.565 | 0.415 | -2.336 | 1.235 |
