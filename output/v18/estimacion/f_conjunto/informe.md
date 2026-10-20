# F1-F4 · Modelos de conjunto (precio, alquiler, oferta y coherencia)

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.*

## Lo que dicen los datos, sin lenguaje causal

En ninguno de los nueve contrastes de cointegración de la familia F (Holm, 5 %) se rechaza la ausencia de cointegración. Por la regla AD-F de la adenda no se publican elasticidades de largo plazo de F1, F2 ni F3, ni la sobrevaloración (F1-A3), y no se hacen las comparaciones de F4. Solo se publica la dinámica de corto plazo, como ASOCIACIÓN. El resultado coincide con lo ya publicado (V7.2 y V8-M4: no se demuestra cointegración) y no cambia ninguna cifra ni conclusión publicada.

**Señales cercanas, declaradas para que conste (ninguna se publica como largo plazo).** Principales entre 0,05 y 0,10 tras Holm: F3-A2 (p bruto 0.007; Holm 0.063). Variantes que rechazan por sí solas mientras su principal no: F3-A2-v1 (p 0.001; BY q 0.003). La regla AD-F es por modelo y la familia de Holm solo cuenta los contrastes de las principales; con T = 21 y N = 31 la validación propia da tamaño 0,05 y potencia 1,0 frente a un ajuste fuerte, y menos frente a un ajuste lento. Queda como señal exploratoria para la fase de revisión.

## Contrastes de cointegración (familia F, Holm)

| id | muestra | N | estimador | coint_t | coint_F | coint_p_mc | p_ajustado | coint_rechaza_5pct | mde |
|---|---|---|---|---|---|---|---|---|---|
| F1-R1 | 1999Q1-2026Q2 | 108 | UECM p = 2; DOLS k = 1; EG | -2.2613 | 4.52 | 0.4153 | 1.0 | False | 4.5062 |
| F1-A2 | 2001-2025 | 24 | UECM p = 1; DOLS k = 1; EG | -3.1737 | 8.0005 | 0.2399 | 1.0 | False | 8.9315 |
| F1-R2 | 2002-2018 | 33 | F1-R2 DOLS-FE vector básico 2002-2018 (2000-2018 no existe) | -1.3383 | — | 0.996 | 1.0 | False | 0.7231 |
| F1-R2-alt | 2002-2018 | 33 | F1-R2-alt DOLS-FE vector alternativo 2002-2018 | -1.826 | — | 0.778 | 1.0 | False | 0.8657 |
| F1-R2-pmg | 2002-2018 | 33 | F1-R2-pmg ECM por PMG vector básico 2002-2018 | -1.3383 | — | 0.996 | 1.0 | False | 0.7231 |
| F1-A1 | 2002-2024 | 33 | F1-A1 DOLS-FE y PMG hasta 2024 y CS-ARDL | -1.9052 | — | 0.935 | 1.0 | False | 0.8795 |
| F2-R1 | 2002-2024 | 38 | F2-R1 PMG del IPC de alquiler real (hogares: población como sustituto) | -0.4064 | — | 0.996 | 1.0 | False | 0.2333 |
| F2-A1 | 2002-2024 | 38 | F2-A1 CS-ARDL del IPC de alquiler real | -0.4064 | — | 0.996 | 1.0 | False | 0.2333 |
| F3-A2 | 2004-2024 | 31 | F3-A2 PMG de ln iniciadas | -2.7842 | — | 0.007 | 0.063 | False | 3.0105 |


Variantes (BY al 10 % dentro de cada identificador) y coprincipales:

| id | estado | muestra | N | coint_p_mc | p_ajustado | coint_rechaza_5pct | valor | unidad | clasificacion_v18 |
|---|---|---|---|---|---|---|---|---|---|
| F1-R1-v2 | variante | 1999Q1-2026Q2 | 84 | 0.8911 | 1 | False | 0.1321 | elasticidad de impacto en variaciones (corto plazo; MCO clásico) | ASOCIACIÓN |
| F1-R1-v3 | variante | 2007Q1-2026Q2 | 76 | 0.4533 | 1 | False | 0.2813 | elasticidad de impacto en variaciones (corto plazo; MCO clásico) | ASOCIACIÓN |
| F1-R1-v4 | variante | 1999Q1-2026Q2 | 108 | 0.5797 | 1 | False | 0.1593 | elasticidad de impacto en variaciones (corto plazo; MCO clásico) | ASOCIACIÓN |
| F1-R1-v5 | variante | 1999Q1-2026Q2 | 108 | 0.8236 | 1 | False | 0.0801 | elasticidad de impacto en variaciones (corto plazo; MCO clásico) | ASOCIACIÓN |
| F1-P-M4 | coprincipal | 1999Q1-2026Q2 | 108 | 0.3023 | 0.3023 | False | 0.1181 | elasticidad de impacto en variaciones (corto plazo; MCO clásico) | ASOCIACIÓN |
| F1-A2-v1 | variante | 2001-2025 | 24 | 0.1909 | 0.5727 | False | 0.7018 | elasticidad de impacto en variaciones (corto plazo; MCO clásico) | ASOCIACIÓN |
| F1-A2-v2 | variante | 2001-2025 | 18 | 0.8946 | 1 | False | 0.934 | elasticidad de impacto en variaciones (corto plazo; MCO clásico) | ASOCIACIÓN |
| F1-R2-v2 | variante | 2000-2008 | 0 | — | — | — | — | — | NO ESTIMABLE |
| F1-R2-alt-v2 | variante | 2000-2008 | 0 | — | — | — | — | — | NO ESTIMABLE |
| F1-R2-pmg-v2 | variante | 2000-2008 | 0 | — | — | — | — | — | NO ESTIMABLE |
| F1-A1-v1 | variante | 2014-2024 | 38 | — | — | — | — | — | NO ESTIMABLE |
| F1-A1-v3 | variante | 2002-2024 | 33 | 0.935 | 0.935 | False | — | — | ASOCIACIÓN |
| F2-R1-v1 | variante | 2011-2024 | 35 | 0.994 | 1 | False | 0.1947 | elasticidad de impacto en variaciones (PMG, grupo medio; IC95 por bootstrap de provincias) | ASOCIACIÓN |
| F2-R1-v2 | variante | 2002-2024 | 38 | 0.994 | 1 | False | -0.1061 | elasticidad de impacto en variaciones (PMG, grupo medio; IC95 por bootstrap de provincias) | ASOCIACIÓN |
| F2-R1-v3 | variante | 2014-2024 | 38 | — | — | — | — | — | NO ESTIMABLE |
| F2-A1-v1 | variante | 2011-2024 | 35 | 0.994 | 0.994 | False | — | — | ASOCIACIÓN |
| F2-A1-v2 | variante | 2014-2024 | 38 | — | — | — | — | — | NO ESTIMABLE |
| F3-A2-v1 | variante | 2004-2024 | 33 | 0.001 | 0.003 | False | 3.5789 | elasticidad de impacto en variaciones (PMG, grupo medio; IC95 por bootstrap de provincias) | ASOCIACIÓN |
| F3-A2-v2 | variante | 2004-2024 | 31 | 0.318 | 0.477 | False | 5.9641 | elasticidad de impacto en variaciones (PMG, grupo medio; IC95 por bootstrap de provincias) | ASOCIACIÓN |
| F3-A2-v3 | variante | 2014-2024 | 36 | — | — | — | — | — | NO ESTIMABLE |
| F1-P-E1P2 | coprincipal | 2002T1-2026T2 | 33 | — | — | — | -0.746 | θ de largo plazo (NO APTO: descriptivo) | no se clasifica |
| F1-P-V72 | coprincipal | - | — | — | — | — | — | — | no se clasifica |
| F2-A2-v1 | variante | 2013-2024 | 30 | — | — | — | 0.0091 | semielasticidad del ratio por pp de coste de uso | ASOCIACIÓN |
| F2-A2-v2 | variante | 2013-2024 | 35 | — | — | — | 0.0185 | semielasticidad del ratio por pp de coste de uso | ASOCIACIÓN |
| F3-R1-v1 | variante | 1997-2004 | 72 | — | — | — | 1.0349 | elasticidad de las iniciadas respecto del precio real | ASOCIACIÓN |
| F3-R1-v2 | variante | 1997-2004 | 72 | — | — | — | 0.6094 | elasticidad de las iniciadas respecto del precio real | ASOCIACIÓN |
| F3-A1-v1 | variante | 1997-2024 | 252 | — | — | — | 0.2749 | elasticidad de las iniciadas respecto del precio real | ASOCIACIÓN |
| F3-A1-v2 | variante | 1997-2024 | 198 | — | — | — | 0.1771 | elasticidad de las iniciadas respecto del precio real | ASOCIACIÓN |


## Herramientas y banda de inferencia (Monte Carlo previo)

- driscoll_kraay_T<=30: NO APTO (tamaño 0,16-0,28 con T = 14-30; V18 montecarlo/driscoll_kraay).
- csardl: NO APTO (tamaño 0,10; V16 montecarlo/csardl y V15 westerlund_csardl).
- westerlund_cips: NO APTO (tamaño 0,09-0,20 y 0,01; V15/V16).
- cluster_sin_efectos_de_anio: NO APTO (tamaño 0,48-0,51 sin efectos de año; V18 montecarlo/driscoll_kraay).
- Contraste de límites del UECM: valores críticos simulados con la muestra de cada especificación (bloques de 4, B = 2.000), tamaño en réplicas independientes y potencia frente a α = −0,10 en la tabla de contrastes y en tabla.csv.
- Contraste de panel: validación propia con la estructura de cada diseño (factor común, N, T, k); no sustituye al Monte Carlo del agente montecarlo:

| N | T | k | tamano_5pct | potencia | R | B | banda |
|---|---|---|---|---|---|---|---|
| 33 | 17 | 3 | 0.03 | 0.84 | 200 | 99 | con valor crítico corregido |
| 33 | 17 | 5 | 0.065 | 0.17 | 200 | 99 | con valor crítico corregido |
| 33 | 23 | 3 | 0.08 | 1.0 | 200 | 99 | con valor crítico corregido |
| 38 | 23 | 4 | 0.075 | 1.0 | 200 | 99 | con valor crítico corregido |
| 35 | 14 | 4 | 0.065 | 0.14 | 200 | 99 | con valor crítico corregido |
| 38 | 23 | 3 | 0.06 | 1.0 | 200 | 99 | apta |
| 31 | 21 | 3 | 0.05 | 1.0 | 200 | 99 | apta |
| 33 | 21 | 2 | 0.02 | 1.0 | 200 | 99 | con valor crítico corregido |
| 31 | 21 | 2 | 0.025 | 1.0 | 200 | 99 | con valor crítico corregido |


## Comprobación previa por MDE (adenda 1.3)

El Anexo B no fija referencia ni δ para la familia F: no hay umbral con el que declarar NO ESTIMABLE por variación; el MDE (al 80 %, bilateral 5 %, R = 2.000, SEED 20261010, σ ya vista y declarada) se publica como diagnóstico y está en la columna `mde` de tabla.csv. Se calculó y registró antes de estimar.

## Fuera de muestra (misma muestra, bloques con embargo)

Modelo F1-ECM frente a AR(4) y ECM v1 aproximado; 105 observaciones de prueba. RMSE (en %, un paso): {'AR(4)': 1.2845, 'ECM v1 (aprox.)': 2.0549, 'F1-ECM': 1.3576, 'deriva': 2.0445}.

- DM-HLN F1-ECM frente a AR(4): {'DM': 1.328, 'p': 0.1871, 'mean_d': 0.0, 'n': 105.0}; frente a ECM v1: {'DM': -5.0624, 'p': 0.0, 'mean_d': -0.0002, 'n': 105.0}.
- Clark-West (AR(4) anidado en F1-ECM): {'CW': 1.4548, 'p_una_cola': 0.0729, 'n': 105.0}; Giacomini-White frente a AR(4): {'GW': 1.9472, 'p': 0.3777, 'n': 104.0}.
- Conjunto de confianza de modelos (10 %): ['F1-ECM', 'AR(4)']; p del MCS: {'ECM v1 (aprox.)': 0.007, 'deriva': 0.007, 'F1-ECM': 0.2342, 'AR(4)': 1.0}.

## F2-A2, F3 y F4

| id | estado | muestra | valor | ic95_lo | ic95_hi | clasificacion_v18 |
|---|---|---|---|---|---|---|
| F3-A2 | principal | 2004-2024 | 3.5186 | 2.6773 | 4.5075 | ASOCIACIÓN |
| F3-A2-v1 | variante | 2004-2024 | 3.5789 | 2.7111 | 4.3965 | ASOCIACIÓN |
| F3-A2-v2 | variante | 2004-2024 | 5.9641 | 5.1802 | 6.7192 | ASOCIACIÓN |
| F3-A2-v3 | variante | 2014-2024 | — | — | — | NO ESTIMABLE |
| F2-A2 | principal | 2013-2024 | 0.0091 | 0.0073 | 0.0109 | ASOCIACIÓN |
| F2-A2-v1 | variante | 2013-2024 | 0.0091 | 0.0073 | 0.0109 | ASOCIACIÓN |
| F2-A2-v2 | variante | 2013-2024 | 0.0185 | 0.0159 | 0.021 | ASOCIACIÓN |
| F3-R1 | principal | 1997-2004 | 0.4687 | -0.7776 | 1.7151 | ASOCIACIÓN |
| F3-R1-v1 | variante | 1997-2004 | 1.0349 | 0.369 | 1.7009 | ASOCIACIÓN |
| F3-R1-v2 | variante | 1997-2004 | 0.6094 | -0.5594 | 1.7782 | ASOCIACIÓN |
| F3-A1 | principal | 1997-2024 | -0.3722 | -0.812 | 0.0676 | ASOCIACIÓN |
| F3-A1-v1 | variante | 1997-2024 | 0.2749 | -0.7804 | 1.3302 | ASOCIACIÓN |
| F3-A1-v2 | variante | 1997-2024 | 0.1771 | -0.3758 | 0.7299 | ASOCIACIÓN |
| F3-A3 | principal | 2004-2024 | — | — | — | NO ESTIMABLE |
| F4-1 | derivada | - | — | — | — | NO ESTIMABLE |
| F4-2 | derivada | - | — | — | — | NO ESTIMABLE |
| F4-3 | derivada | - | — | — | — | NO ESTIMABLE |
| F4-4 | derivada | - | — | — | — | NO ESTIMABLE |
| F4-5 | derivada | - | — | — | — | NO ESTIMABLE |


## F1-P-E1P2 (CS-ARDL, NO APTO, descriptivo)

N = 33, T = 98: θ grupo medio -0.75, recortada -0.21, mediana 0.60; publicado en V15 E1-P2: 0,64 y en V16 Q9-c: 0,84.

## Raíces unitarias nacionales (ADF y KPSS)

| serie | adf_p_niveles | adf_p_diferencias | kpss_p_niveles |
|---|---|---|---|
| y | 0.0051 | 0.3685 | 0.1 |
| renta | 0.6109 | 0.0 | 0.01 |
| tipo_real | 0.496 | 0.0 | 0.056 |
| pob | 0.8433 | 0.1883 | 0.01 |


Lectura: si una serie del vector no es I(1), la cointegración no está bien definida; el ln del precio real rechaza la raíz unitaria en niveles (ADF) y no rechaza la estacionariedad (KPSS), de modo que el contraste de límites se interpreta con esa cautela. Placebos, pretendencias y F efectivo de Montiel Olea-Pflueger no aplican a F1-F2 (sin instrumento ni evento); en F3-R1 se publica el F de primera etapa agrupado.

## Diagnósticos

```json
{
 "series_nacionales": {
  "y": {
   "adf_p_niveles": 0.0051,
   "adf_p_diferencias": 0.3685,
   "kpss_p_niveles": 0.1
  },
  "renta": {
   "adf_p_niveles": 0.6109,
   "adf_p_diferencias": 0.0,
   "kpss_p_niveles": 0.01
  },
  "tipo_real": {
   "adf_p_niveles": 0.496,
   "adf_p_diferencias": 0.0,
   "kpss_p_niveles": 0.056
  },
  "pob": {
   "adf_p_niveles": 0.8433,
   "adf_p_diferencias": 0.1883,
   "kpss_p_niveles": 0.01
  }
 },
 "estabilidad_F1_R1": {
  "chow_en_fechas_fijas": {
   "2008Q1": 3.7009,
   "2015Q1": 1.4404
  },
  "sup_F_ruptura_unica": 6.709,
  "nota": "sin valor crítico validado: se publica como descriptivo",
  "dols_recursivo_primer_regresor": {
   "ultimos": [
    -1.901,
    -2.432,
    -2.648
   ],
   "min": -2.6475,
   "max": 1.5043,
   "primero": 1.3678,
   "n_ventanas": 13
  }
 },
 "dependencia_transversal": {
  "F1-R2": {
   "CD": 72.8308,
   "p": 0.0,
   "rho_medio": 0.7687
  },
  "F1-R2-alt": {
   "CD": 64.4806,
   "p": 0.0,
   "rho_medio": 0.6806
  },
  "F1-R2-pmg": {
   "CD": 72.8308,
   "p": 0.0,
   "rho_medio": 0.7687
  },
  "F1-A1": {
   "CD": 90.4018,
   "p": 0.0,
   "rho_medio": 0.8203
  },
  "F2-R1": {
   "CD": 58.5341,
   "p": 0.0,
   "rho_medio": 0.4603
  },
  "F2-R1-v1": {
   "CD": 63.6008,
   "p": 0.0,
   "rho_medio": 0.6969
  },
  "F2-R1-v2": {
   "CD": 58.1094,
   "p": 0.0,
   "rho_medio": 0.457
  },
  "F3-A2": {
   "CD": 25.5856,
   "p": 0.0,
   "rho_medio": 0.2589
  },
  "F3-A2-v1": {
   "CD": 36.7836,
   "p": 0.0,
   "rho_medio": 0.3493
  },
  "F3-A2-v2": {
   "CD": 73.2158,
   "p": 0.0,
   "rho_medio": 0.7409
  }
 },
 "raices_unitarias_panel": "CIPS es NO APTO (V16 montecarlo/cips_bootstrap, tamaño 0,006): no se usa; ADF nacional arriba. El contraste de panel es Gτ con bootstrap conjunto.",
 "moran": "no se calcula aquí: no hay matriz de contigüidad provincial versionada para V18; la dependencia transversal se mide con el CD de Pesaran y el bootstrap del contraste de panel conserva la dependencia entre provincias",
 "exclusiones": "Madrid, Baleares y Canarias ya están fuera por el sellado de v6; Barcelona permanece (sin variante propia: holgura no usada)."
}
```

## Notas de lectura
- Panel de 33-38 provincias (no 39): el valor tasado anual tiene huecos en cinco provincias y 11 están selladas (v6); las unidades de V15/V16 no afectan al nivel provincial.
- Renta de los hogares provincial y hogares provinciales anteriores a 2021 no están en el repositorio (`posterior_prereg`, sin red): se usa el PIB provincial corriente por habitante, real, como sustituto declarado, y la población como sustituto de los hogares en F2.
- Población nacional trimestral: 44 de los 110 trimestres de la ventana están interpolados; CLAUDE.md los limita a robustez, y F1-R1-v5 repite el modelo sin población.
- Clase provisional hasta I8 (réplica ciega, B6). Desviaciones: docs/v18/desviaciones_f_e7.md.
