# Reproduccion de Mense (2025), tabla 3 (efecto de la oferta nueva sobre el alquiler medio)

**Reproduccion del estudio original con sus datos; no usa datos del proyecto.**

Estudio: Mense, A. (2025), The Impact of New Housing Supply on the Distribution of Rents, JPE Macroeconomics 3(1), doi 10.1086/733977. Paquete: Harvard Dataverse doi 10.7910/DVN/LWRXA9 (CC0 1.0). Capa C4 (reproduccion; no promueve de capa).

## Especificacion y decisiones de traduccion (R a Python)

- No hay R. Se traduce `reduced_form_replication.R` (secciones 1.2, 2.2 y 3.1.1) a Python. Se instalo `pyreadr` (no estaba) para leer los .RDS. Los shapefiles se leen dentro de los .zip, sin descomprimir.
- Variable dependiente: indice hedonico de alquiler por region de ordenacion (PR) y ano, base 2011: regresion por PR de log(alquiler/m2) sobre log(superficie), polinomio de segundo grado del ano de construccion, indicador de ano de construccion ausente, calefaccion de suelo, parquet, ascensor, cocina equipada, WC de invitados, balcon/terraza, jardin, ano (ficticias) y efectos fijos de tipo y equipamiento; solo PR con mas de 100 anuncios. `poly(Baujahr,2)` ortogonal de R se sustituye por un polinomio bruto reescalado (mismo subespacio, mismos coeficientes de ano). Las ficticias absorbidas se construyen explicitamente (lstsq) en lugar de la absorcion de `lfe`.
- Oferta y clima: agregacion de municipios a PR por interseccion de poligonos (`sf::st_intersection` sustituido por shapely/geopandas): se suma la oferta de municipios con mas del 95 % de su area dentro de la PR; el clima se pondera por la cuota de area de la PR. Se desplaza un ano (t-1).
- Endogena: unidades terminadas oct-dic de t-1 / media anual de terminaciones. Instrumento: duracion media de rachas de lluvia jul-sep de t-1. Controles: log empleo (t-1), log paro (t-1), estudiantes por 1.000 hab. (t-1). Efectos fijos de ano y PR (ficticias). Error agrupado por PR. El original usa `lfe::felm` con `robust=T`; aqui `linearmodels.IV2SLS` agrupado, sin correccion de muestra pequena (principal) y con ella (columna `se_reproducido_ajuste_gl`).
- El F de Kleibergen-Paap del original es el F de instrumentos de la primera etapa agrupada; aqui se aproxima con el cuadrado del estadistico t del instrumento (un solo instrumento, error agrupado).

## Comparacion con la tabla 3A (p. 18)

| col. | parametro | publicado (EE) | reproducido (EE) | dif. abs. | dif. rel. | veredicto |
|---|---|---|---|---|---|---|
| 1 | oferta_nueva_oct_dic (IV) | -0.199 (0.072) | -0.199 (0.072) | -0.000 | 0.2 % | coincide |
| 1 | log_empleo | 0.991 (0.143) | 0.991 (0.142) | -0.000 | 0.0 % | coincide |
| 2 | oferta_nueva_oct_dic (IV) | -0.204 (0.072) | -0.204 (0.072) | +0.000 | 0.1 % | coincide |
| 2 | log_empleo | 1.009 (0.145) | 1.009 (0.144) | -0.000 | 0.0 % | coincide |
| 2 | log_paro | -0.028 (0.038) | -0.028 (0.038) | -0.000 | 0.6 % | coincide |
| 3 | oferta_nueva_oct_dic (IV) | -0.192 (0.065) | -0.192 (0.064) | +0.000 | 0.2 % | coincide |
| 3 | log_empleo | 0.949 (0.142) | 0.949 (0.140) | +0.000 | 0.0 % | coincide |
| 3 | log_paro | -0.050 (0.040) | -0.050 (0.040) | -0.000 | 0.7 % | coincide |
| 3 | estudiantes | 0.002 (0.001) | 0.002 (0.001) | +0.000 | 8.8 % | coincide |

## Diagnosticos

| col. | N (pub. 752) | PR (pub. 94) | F KP publicado | F 1a etapa agrupada | coef. 1a etapa (pub. -0,009/-0,010) |
|---|---|---|---|---|---|
| 1 | 752 | 94 | 17.4 | 17.7 | -0.009 (0.002) |
| 2 | 752 | 94 | 17.4 | 17.6 | -0.009 (0.002) |
| 3 | 752 | 94 | 19.0 | 19.3 | -0.010 (0.002) |

## Veredicto

Columna 1: coincide; columna 2: coincide; columna 3: coincide. Resumen: coincide.

Lectura: elasticidad de corto plazo del alquiler medio a la oferta nueva anual (Alemania, 2011-2018). No es evidencia para Espana; la validez externa se evalua en la fase 3.
