# V18 · Fase 2 · Reproducción de los estudios originales

Generado por src/v18/f2_reproduccion.py. Cada reproducción usa solo el paquete de su autor (data/bib/replicacion/, fuera de git) y no usa datos del proyecto; el código está en src/v18/reproduccion/ y las salidas en output/v18/reproduccion/. Veredicto: «coincide» (misma cifra al redondeo publicado o diferencia menor que el 5 % del coeficiente y dentro del error), «difiere con explicación» o «difiere sin explicación» (parada G).

## Reproducciones

| Clave | Método | N | Estimación | IC 95 % | Veredicto |
|---|---|---|---|---|---|
| [borusyak_hull_jaravel_2022](../../output/v18/reproduccion/borusyak_hull_jaravel_2022/informe.md) | IV shift-share a nivel de sector (ssaggregate traducido a Python; shock g; aw=s_n; cluster sic3), conjunto de controles 5 de la Tabla 4 (columna 5 del artículo) | 794 | -0.31 | [-0.5736; -0.0464] | coincide |
| [chavesfonseca2026](../../output/v18/reproduccion/chavesfonseca2026/informe.md) | IV (shift-share: ln proximidad top-3 atractivos x busquedas Google), efectos fijos de barrio y ano, controles, error tipico agrupado por barrio; traduccion Python (linearmodels) de ivreghdfe; tabla 2 col. 6 | 1029 | 0.01965 | [0.011; 0.0283] | coincide |
| [mense_2025](../../output/v18/reproduccion/mense_2025/informe.md) | IV-2SLS en panel con efectos fijos de PR y ano, error agrupado por PR; instrumento: duracion media de rachas de lluvia jul-sep (t-1); indice hedonico de alquiler por PR; columna 3 de la tabla 3 | 752 | -0.1916 | [-0.3175; -0.0658] | coincide |

## Estudios clave de la sección E

Sin paquete con datos, el estudio pasa a la fase 3 solo con su especificación (plan, fase 2).

| Factor | Estudio | Paquete | Nota | Reproducido |
|---|---|---|---|---|
| E1 | Garcia-López et al. (2020) | sin paquete público | datos de Airbnb y de alquiler de Barcelona de terceros | no |
| E1 | Chaves-Fonseca (2026) | con datos | paquete CC BY 4.0 con datos | sí, coincide |
| E2 | Jofre-Monseny, Martínez-Mazza y Segú (2023) | sin paquete público | registro de fianzas del Incasòl (microdatos no públicos) | no |
| E2 | Monràs y García-Montalvo (2023) | sin paquete público | contratos del Incasòl, no anuncios (ficha de la fase 1) | no |
| E3 | González y Ortega (2013) | sin paquete público | padrón y valor tasado; se replica con nuestros datos | no |
| E3 | Borusyak, Hull y Jaravel (2022) | con datos | método shift-share; aplicación ADH con datos (GPL-3.0) | sí, coincide |
| E4 | Fack (2006); Gibbons y Manning (2006); Grislain-Letrémy y Trevien (2022) | sin paquete público | microdatos administrativos | no |
| E5 | Saiz (2010) | sin paquete público | solo resumen en la fase 1 | no |
| E5 | Baum-Snow y Han (2024) | solo código | el paquete completo (19,4 GB) no cabe en el disco; se bajaron 3 ficheros | no |
| E6 | Mense (2025) | con datos | paquete CC0 con datos | sí, coincide |
| E6 | Asquith, Mast y Reed (2023) | solo código | CC0, sin datos (alquileres de terceros) | no |
| E7 | Jarociński y Karadi (2020); Altavilla et al. (2019) | datos de choques | series de sorpresas del BCE: se usan como dato en la fase 4, no se reproducen | no |
| E8 | Best y Kleven (2018); Besley, Meads y Surico (2014) | sin paquete público | datos fiscales administrativos | no |
| E9 | Badarinza y Ramadorai (2018); Cvijanović y Spaenjers (2021) | sin paquete público | datos de transacciones de terceros | no |
| E10 | Literatura de grandes tenedores (EE. UU. y Europa) | sin paquete descargado | Diamond et al. y Duso et al. existen, pero la descarga devolvió 403 | no |
| E11 | Segú (2020) | sin paquete público | datos fiscales franceses | no |
| E12 | Koster y van Ommeren (2019) | solo código | sin datos (registros neerlandeses) | no |

Ninguna reproducción difiere sin explicación: no hay parada G en esta fase.
