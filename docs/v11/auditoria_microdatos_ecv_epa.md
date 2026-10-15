# V11-DATOS · Punto 9: variables de los microdatos ECV y EPA ya descargados

Ficheros: data/raw/v9/ine_microdatos/ecv/datos_2018-2025.zip y data/raw/v9/ine_microdatos/epa/datos_<t>t18-<t>t26.zip
(no versionados; `make datos_v9`). Comprobación hecha leyendo la cabecera de cada fichero (2026-10-15); no se ha
calculado ningún indicador (la tarea lo prohíbe).

## ECV (Encuesta de Condiciones de Vida), 2018-2025, ficheros D/H/P/R

| Concepto pedido | Variable | Fichero | Años presentes |
|---|---|---|---|
| Tenencia de la vivienda | HH021 | H | 2018-2025 |
| Alquiler pagado | HH060 (alquiler actual) | H | 2018-2025 |
| Gastos de vivienda | HH070 (coste total); HS070 (2018-2020) | H | 2018-2025 |
| Habitaciones | HH030 | H | 2018-2025 |
| Superficie | — (no existe en la ECV) | — | — |
| Tipo de vivienda | HH010 | H | 2018-2025 |
| Tipo de hogar | HX060 | H | 2018-2025 |
| Nacionalidad | PB220A (2018-2020, P, ≥16 años); RB290 (2021-2025, R, todos los miembros) | P/R | 2018-2025 |
| País de nacimiento | PB210 (2018-2020, P); RB280 (2021-2025, R) | P/R | 2018-2025 |
| Año de llegada | — (no publicado en el fichero anonimizado) | — | — |
| Territorio | DB040 (comunidad autónoma, NUTS-2) | D | 2018-2025 |

Codificación de origen: agregada (España, resto de la UE, resto de Europa, resto del mundo) en el fichero
anonimizado. Indicadores por origen que SE PUEDEN construir (a nivel España y, con muestras pequeñas, CCAA):
tenencia (propiedad, alquiler a precio de mercado, alquiler inferior, cesión) por nacionalidad o país de nacimiento
de la persona de referencia (vía HB… y RB/PB) o de cualquier miembro; alquiler pagado y sobrecarga del coste de
la vivienda (HH060 o HH070 frente a renta HY020); habitaciones por persona y hacinamiento según la definición de
Eurostat (HH030, edades del registro R); tipo de hogar. NO se pueden: superficie, año de llegada, nivel provincial.
Cambio de serie en 2021 (las variables de origen pasan de P a R): se documenta como ruptura.

## EPA (Encuesta de Población Activa), 2018T1-2026T2

| Concepto pedido | Variable | Presente |
|---|---|---|
| Nacionalidad | NAC1 (española, doble, extranjera) y EXREGNA1 (región de nacionalidad extranjera) | sí |
| País o región de nacimiento | REGNA1, PRONA1 (provincia de nacimiento si nació en España) | sí |
| Año de llegada | ANORE1 (años de residencia en España) | sí |
| Hogar y persona de referencia | NVIVI (vivienda), RELPP1 (relación con la persona de referencia), NPERS | sí |
| Territorio | PROV | sí (provincia) |
| Tenencia, alquiler, superficie, habitaciones | — | no existen en la EPA |

Indicadores por origen que SE PUEDEN construir: hogares por nacionalidad o región de nacimiento de la persona de
referencia (provincia × trimestre, con error muestral alto en provincias pequeñas), tamaño y composición del hogar
por origen, tiempo de residencia (cohortes de llegada) y situación laboral por origen. Las filas de 2026T3 en
adelante, si se descargan, serán posterior_prereg y no se usarán.
