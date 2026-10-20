## Anexo A. Fichas bibliográficas

La fase 1 fijó los criterios antes de buscar (docs/v18/bib/criterios.md): diseño cuasi experimental o estructural, datos de España o de mercados europeos comparables, y publicación en revista con revisión, documento de banco central o serie reconocida de documentos de trabajo. Se hizo una ficha por estudio, agrupadas por factor (docs/v18/bib/<factor>/), con una tabla de efectos y su unidad. El catálogo está en output/v18/f1/catalogo.csv. [FALTA CIFRA: recuentos del catálogo (fichas, texto completo, solo resumen, con paquete de replicación; VERIFICADA, NO VERIFICADA y DISCREPANTE) en output/v18/f1/informe.md]

Los PDF y los paquetes de replicación están solo en disco, con sha256 en data/bib/CHECKSUMS.sha256, y no se versionan. Al repositorio van la ficha, el enlace, el DOI, la licencia y las notas, con citas breves. Estado: VERIFICADA es DOI comprobado con Crossref o DataCite; el cuartil de Scimago no está verificado (tarea del autor). DISCREPANTE es una ficha de versión de trabajo cuyo DOI corresponde a la versión publicada (otro año o título), y se trata como NO VERIFICADA. No se cita ninguna cifra de la versión publicada sin leerla.

Estudios con error típico en la unidad para inmigración (E3): {{V18-B5-E3:cobertura}}.

**Referencias de la magnitud preferida y de la etiqueta I6.**

| Factor | Estudio | Estado de la ficha | ¿Entra en la magnitud preferida? Motivo |
|---|---|---|---|
| E1 | Segú (2018) | NO VERIFICADA | Sí (único estudio) |
| E1 | Garcia-López et al. (2020) | VERIFICADA | No: unidad no convertible (por 100 anuncios en el área estadística básica) |
| E1 | Chaves-Fonseca (2026) | VERIFICADA | No: unidad no convertible (por 100 anuncios, sobre el precio de compra) |
| E1 | Duso et al. (2024) | VERIFICADA | No: unidad no convertible (€/m² por anuncio en un radio) |
| E2 | Jofre-Monseny et al. (2023) | VERIFICADA | Sí |
| E2 | Monràs y García-Montalvo (2023) | VERIFICADA | Sí (peso nulo al contar una vez el episodio compartido) |
| E2 | Breuille et al. (2025) | NO VERIFICADA | Sí |
| E2 | Hahn et al. (2021) | VERIFICADA | Sí |
| E2 | Pérez García (2026) | VERIFICADA | No: otro régimen (zonas de 2024), otra unidad y sin pretendencias paralelas |
| E2 | Abel (2024) | NO VERIFICADA | No: mide la oferta |
| E3 | González y Ortega (IZA, 2009) | NO VERIFICADA | Sí (versión que da la unidad) |
| E3 | González y Ortega (Chicago Fed, 2011) | NO VERIFICADA | No: misma obra; entra en la sensibilidad |
| E3 | Sanchis-Guarner (2017) | DISCREPANTE | Sí |
| E3 | Saiz (2007) | VERIFICADA | Sí |
| E3 | Sá (2015) | VERIFICADA | Sí |
| E3 | Ünal (2022) | NO VERIFICADA | Sí |
| E3 | Accetturo (2012) | DISCREPANTE | No: elasticidad respecto a la población extranjera, no a la total |
| E3 | Torres y Montero (2023) | VERIFICADA | No: sin error típico |
| E4 | Fack (2005) | VERIFICADA | Sí |
| E4 | Eerola et al. (2026) | VERIFICADA | Sí |
| E4 | Kangasharju (2008) | VERIFICADA | No: sin error típico |
| E4 | Hyslop y Rea (2018) | VERIFICADA | No: sin error típico |
| E5 | Taltavull (2006) | NO VERIFICADA | Sí |
| E5 | Baum-Snow y Han (versión de trabajo) | DISCREPANTE | Sí |
| E5 | Paciorek (2012) | VERIFICADA | Sí |
| E6 | Mense (2025) | VERIFICADA | Sí (único estudio) |
| E6 | Asquith, Mast y Reed (2020) | DISCREPANTE | No: otra unidad |
| E7 | San Juan (2023) | VERIFICADA | No: intervalos solo en un gráfico |
| E7 | BCE, Boletín Económico 6/2022 | NO VERIFICADA | No: sin error típico |
| E8 | Dölls et al. (2020) | VERIFICADA | No: sin error típico recuperado |
| E9 | Sá (2016) | VERIFICADA | No: sin error típico extraído |
| E9 | Álvarez, Blanco y García-Posada (2020) | NO VERIFICADA | No: regresión transversal sin instrumento |

Los valores por estudio están en output/v18/f5/magnitudes_estudios.csv y no en cifras_clave (véase la sección 4).

## Anexo B. Reproducciones

La fase 2 reproduce con el paquete de su autor, y sin datos del proyecto, los estudios que lo tienen abierto. El veredicto es «coincide» (la misma cifra al redondeo publicado, o una diferencia menor que la fijada en el plan y dentro del error), «difiere con explicación» o «difiere sin explicación» (parada). Ninguna reproducción difiere sin explicación. [FALTA CIFRA: coeficientes e intervalos reproducidos y publicados de las tres reproducciones (output/v18/reproduccion/*/informe.md y docs/v18/reproduccion.md)]

| Estudio | Método reproducido | Veredicto |
|---|---|---|
| Chaves-Fonseca (2026), tabla 2 | IV shift-share (proximidad a atractivos por búsquedas de Google), efectos fijos de barrio y año, errores agrupados por barrio; Madrid, precios | coincide |
| Mense (2025), tabla 3A | IV-2SLS en panel con efectos fijos de región y año, instrumento de lluvia; alquiler | coincide |
| Borusyak, Hull y Jaravel (2022), tabla 4 | IV shift-share a nivel de sector, aplicación de Autor, Dorn y Hanson | coincide; la herramienta (src/v18/reproduccion/bhj_lib.py) queda validada |

Sin reproducción por falta de paquete con datos: Garcia-López et al. (2020), Jofre-Monseny et al. (2023), Monràs y García-Montalvo (2023), González y Ortega (2013), Fack, Gibbons y Manning y Grislain-Letrémy y Trevien (E4), Saiz (2010), Best y Kleven (2018) y Besley et al. (2014), Badarinza y Ramadorai (2018) y Cvijanović y Spaenjers (2021), la literatura de grandes tenedores, Segú (2020) y Koster y van Ommeren (2019). Baum-Snow y Han (2024) solo tiene código y su paquete completo no cabe en el disco; Asquith, Mast y Reed (2023) solo tiene código, sin datos. Jarociński y Karadi (2020) y Altavilla et al. (2019) aportan series de choques, que se usan como dato.

## Anexo C. Planes de replicación

El pre-registro interno lo forman el plan de replicación (docs/v18/plan_replicacion.md, commit d4e9869) y su adenda (docs/v18/plan_replicacion_adenda.md), que prevalece donde difiera. La etiqueta git local plan-replicacion-v18 señala el commit de la adenda (ad4385c), que está en la rama remota claude/housing-price-spain-econometric-95dhj3. La puerta de la fase 4 exige la etiqueta y que su commit esté en la rama remota; la subida de la etiqueta al remoto queda como tarea del autor.

- **Contenido.** Para cada estudio y ampliación: la especificación del original, su traslado a los datos del proyecto, las ampliaciones previstas y las pruebas. Incluye las reglas de inferencia, la clasificación V18, el multiverso enumerado, la estimabilidad por MDE, el sellado temporal y espacial, la magnitud preferida y la contabilidad.
- **Revisión.** Revisor del pre-registro (apto con cambios) y abogado del diablo (resiste con limitaciones). La adenda responde a todos los hallazgos de ambos sin haber mirado ningún resultado de V18; el autor decidió la regla de capas y lenguaje (K2).
- **Sellado de entrenamiento.** docs/v18/sellado_v18.json, generado con solo metadatos después de la etiqueta y antes de la primera estimación.
- **Desviaciones.** Toda desviación respecto al plan está en docs/v18/desviaciones*.md con fecha y motivo.

## Anexo D. Pruebas por estimación

Las pruebas son las de B4 de cada diseño (pretendencias y potencia de Roth, placebos de fecha y de resultado, Honest DiD, primera etapa y F efectivo, número efectivo de choques, robustez a la exclusión de unidades atípicas y a la medida de precio o alquiler). Madrid, Baleares y Canarias ya están fuera por el sellado de v6, de modo que «sin Madrid» y «sin islas» no cambian la muestra provincial. Los valores completos y los intervalos están en tablas_v18.xlsx (pestañas «estimaciones» y «magnitudes»).

**D.1 Estimaciones con cifra.** «IC incluye el cero» describe el intervalo de la ficha (IC95, salvo indicación). Todas son de capa C4.

| Id | Magnitud y unidad | Estimación | ¿IC incluye el cero? | Clase V18 |
|---|---|---|---|---|
| E1-R3 | Log del alquiler por punto de densidad HUT (estudio de eventos) | {{V18-E1-R3:sig}} | No | {{V18-E1-R3:clasificacion}} |
| E1-R4 | Log, secciones del radio frente al anillo (Sagrada Família) | {{V18-E1-R4:sig}} | Sí | {{V18-E1-R4:clasificacion}} |
| E1-P-H3 | Log del alquiler por desviación típica intra-sección (coprincipal) | {{V18-E1-P-H3:sig}} | Sí | {{V18-E1-P-H3:clasificacion}} |
| E2-R1 | Log de la renta media de contratos nuevos | {{V18-E2-R1:sig}} | No | {{V18-E2-R1:clasificacion}} |
| E2-R1c | Log de contratos por 1.000 habitantes | {{V18-E2-R1c:sig}} | Sí | {{V18-E2-R1c:clasificacion}} |
| E2-R1-REV | Reversión tras la STC 37/2022 (log de la renta) | {{V18-E2-R1-REV:sig}} | Sí | {{V18-E2-R1-REV:clasificacion}} |
| E3-R1 | €/m² por punto de población (IV, Webb-AR) | {{V18-E3-R1-beta:sig}} | Sí | {{V18-E3-R1-beta:clasificacion}} |
| E5-A1 | Interacción del instrumento de inmigración con solares (Δ ln P) | {{V18-E5-A1-psi:sig}} | Sí | {{V18-E5-A1-psi:clasificacion}} |
| E7-R1 | % del precio por +100 pb a ocho trimestres (LP-IV); AR no acotado | {{V18-E7-R1:sig}} | No aplicable | {{V18-E7-R1:clasificacion}} |
| E7-R3 | % del precio por +100 pb del euríbor a ocho trimestres (BVAR; banda del 68 %) | {{V18-E7-R3:sig}} | No (banda del 68 %) | {{V18-E7-R3:clasificacion}} |
| E7-A2 | Respuesta relativa entre provincias (panel) | {{V18-E7-A2:sig}} | No | {{V18-E7-A2:clasificacion}} |
| E8-R1 | Log del valor tasado a cuatro trimestres por punto del tipo general del ITP | {{V18-E8-R1:sig}} | No (aleatorización) | {{V18-E8-R1:clasificacion}} |
| E10-A1 | % del alquiler por m² por punto de viviendas de grandes tenedores | {{V18-E10-A1:sig}} | Sí | {{V18-E10-A1:clasificacion}} |
| E12-A1 | Viviendas libres iniciadas por vivienda protegida calificada (IV) | {{V18-E12-A1:num}} | Sí (conjunto AR) | {{V18-E12-A1:clasificacion}} |
| E12-A2 | % del valor tasado real por vivienda protegida calificada (IV) | {{V18-E12-A2:num}} | AR no acotado | {{V18-E12-A2:clasificacion}} |
| F1-R1 | Elasticidad de impacto, precio frente a renta de los hogares (nacional) | {{V18-F1-R1:sig}} | Sí | {{V18-F1-R1:clasificacion}} |
| F1-R2-pmg | Elasticidad de corto plazo, panel provincial (PMG) | {{V18-F1-R2-pmg:sig}} | No | {{V18-F1-R2-pmg:clasificacion}} |
| F2-R1 | Elasticidad de corto plazo del alquiler a la renta (PMG) | {{V18-F2-R1:sig}} | No | {{V18-F2-R1:clasificacion}} |
| F3-A2 | Elasticidad de corto plazo de las iniciadas al valor tasado (PMG) | {{V18-F3-A2:sig}} | No | {{V18-F3-A2:clasificacion}} |

**D.2 Estimaciones NO ESTIMABLES: la comprobación previa.** Se publica la magnitud mínima detectable (MDE), el F efectivo o el recuento de datos, no el coeficiente.

| Id | Comprobación | Cifra | Clase V18 |
|---|---|---|---|
| E1-R1 | Barrios con el cambio mínimo de stock | {{V18-E1-R1:sig}} | {{V18-E1-R1:clasificacion}} |
| E1-R2 | F efectivo de la primera etapa | {{V18-E1-R2:sig}} | {{V18-E1-R2:clasificacion}} |
| E1-A1 | MDE | {{V18-E1-A1:sig}} | {{V18-E1-A1:clasificacion}} |
| E2-A1 | MDE | {{V18-E2-A1:sig}} | {{V18-E2-A1:clasificacion}} |
| E2-A4 | MDE | {{V18-E2-A4:sig}} | {{V18-E2-A4:clasificacion}} |
| E3-R2 | MDE (elasticidad) | {{V18-E3-R2-MDE80:sig}} | {{V18-E3-R2-MDE80:clasificacion}} |
| E3-A1 | MDE (% por punto) | {{V18-E3-A1-MDE80:num}} | {{V18-E3-A1-MDE80:clasificacion}} |
| E5-R1 | F efectivo de la primera etapa | {{V18-E5-R1-F:sig}} | {{V18-E5-R1-F:clasificacion}} |
| E6-R1 | MDE (log) | {{V18-E6-R1:sig}} | {{V18-E6-R1:clasificacion}} |
| E8-R2 | MDE (log por punto) | {{V18-E8-R2:sig}} | {{V18-E8-R2:clasificacion}} |
| E9 | Número efectivo de choques (sin pesos) | {{V18-E9-1HHI-origenes:num}} | {{V18-E9-1HHI-origenes:clasificacion}} |

**D.3 E2-R1: robustez a posteriori (B6).** Los resultados de esta tabla se añadieron después de ver los de E2-R1 y no deciden su clase.

| Id | Prueba | Estimación | ¿IC incluye el cero? |
|---|---|---|---|
| E2-B6-A | Salto en 2022T2 sobre la extrapolación de la recta de la vigencia | {{V18-E2-B6-A:sig}} | Sí |
| E2-B6-B | HUT 2019 y ln(población) 2019 por trimestre | {{V18-E2-B6-B:sig}} | No |
| E2-B6-C | Controles emparejados por el crecimiento previo de la renta | {{V18-E2-B6-C:sig}} | No |
| E2-B6-D | Diferencias en diferencias sintéticas con controles ponderados | {{V18-E2-B6-D:sig}} | No |
| E2-R1c-v1 | Contratos por hogar inquilino del Censo 2021 | {{V18-E2-B6-R1CV1:sig}} | Sí |

## Anexo E. Monte Carlo de las herramientas

Cada herramienta nueva se validó antes de usarse con procesos generadores que reproducen la estructura de los diseños de V18 (output/v18/montecarlo/<herramienta>/). Se simula bajo el nulo y bajo la alternativa, con semilla fija y sin ningún dato real de resultado ni muestra sellada. Un resultado es apto si el tamaño al 5 % y la cobertura al 95 % caen en las bandas de la adenda 1.12. [FALTA CIFRA: tamaños empíricos y coberturas por herramienta y condición (output/v18/montecarlo/*/resultado.json)]

| Herramienta | Veredicto | Condición |
|---|---|---|
| Callaway-Sant'Anna con Webb | APTO CONDICIONADO | Diseños municipales con muchos tratados y controles; NO APTO con ocho clusters |
| Sun-Abraham con Webb | APTO | Frágil si las comunidades de control son pocas |
| de Chaisemartin-D'Haultfœuille con aleatorización del calendario | APTO | Aleatorización entre ocho comunidades; el bootstrap de Webb con ocho clusters es NO APTO |
| Aleatorización | APTO | Entre municipios y entre comunidades |
| Honest DiD | APTO CONDICIONADO | Solo sin desviación de tendencias paralelas; con desviaciones mayores es válido pero conservador y sin potencia |
| DiD sintético con Conley-Taber | APTO | Si los tratados son intercambiables con los controles; no si son más variables |
| Webb en TWFE | APTO y APTO CONDICIONADO | Según el diseño |
| Conley | Mixto | Apto si el alcance de la dependencia no supera el corte; NO APTO si lo duplica |
| IV débil | Mixto | APTO con instrumento fuerte; APTO CONDICIONADO o NO APTO en los diseños más débiles |
| BHJ con pocos choques | NO APTO | Con pocos choques efectivos |
| Driscoll-Kraay con T corto | NO APTO | Con series temporales cortas |
| Proyección local con instrumento | NO APTO | Newey-West subestima la incertidumbre; el AR aumentado con EHW es el más cercano al nominal bajo el nulo; con T corto la respuesta a horizontes largos queda atenuada |
| SVAR con proxy | NO APTO | AR por método delta apto solo con F cercano a diez |
| BVAR recursivo | NO APTO | Bandas conservadoras o con cobertura distinta de la nominal |
| Metaanálisis bayesiano | NO APTO por conservador | Intervalos que cubren de más; con dos estudios y heterogeneidad el efecto fijo no cubre la media verdadera |

En la simulación, la inferencia por aleatorización del calendario es la única apta con ocho comunidades (E8). Las herramientas NO APTAS se publican con esa etiqueta y la clasificación no se apoya en ellas.

## Anexo F. Pre-registro interno y análisis a posteriori

**Qué es pre-registro interno sin sello de tiempo externo.**

- El plan de replicación (commit d4e9869) y su adenda, con la etiqueta git local plan-replicacion-v18 sobre el commit ad4385c, fechada el 2026-10-20. El commit está en la rama remota claude/housing-price-spain-econometric-95dhj3; la etiqueta aún no está en el remoto (tarea del autor).
- No es un pre-registro depositado en un registro externo y no debe describirse como tal. Lo fija solo el historial de git del proyecto.
- Las especificaciones, las variantes enumeradas, las reglas de estimabilidad por MDE, de clasificación y de magnitud preferida, la designación de la estimación propia de cada factor y las hipótesis de la evaluación diferida se fijaron en ese plan y su adenda, antes de la primera estimación de V18 y sin haber mirado ningún resultado.
- Los resultados de V18 se describen siempre como resultados de un pre-registro interno sin sello de tiempo externo, con su etiqueta, su commit y su fecha.

**Qué es a posteriori.**

- *Todo V17.* La auditoría de afirmaciones y medidas, la demografía, el análisis general o local, la factibilidad y las cifras V17-* se hicieron sin pre-registro y se integran aquí como análisis a posteriori de capa C4.
- *La robustez B6 de E2-R1 y E2-R1c.* Se añadió después de ver los resultados, por petición del abogado del diablo (anexo D.3). No cambia la especificación principal ni su clase por sí sola.
- *Las desviaciones.* Toda desviación respecto al plan (docs/v18/desviaciones*.md) se declaró con fecha y motivo. Entre ellas: el paro registrado de E2 (una versión anterior de la desviación era errónea y se corrigió); la geometría y la lectura de la ficha de E1-R4 (K8 bis); la lectura restrictiva de la contabilidad (K10); el deflactor del PIB en lugar del IPC; los ocho grupos de origen en E3.
- *Decisiones tomadas tras ver resultados de otras especificaciones.* K7 (clasificación de E8-R1 y E2-R1c tras la ronda 1 del abogado del diablo), K8 y K8 bis (E1-R4) y K9 (E2-R1 tras la ronda 2, con su frase de limitación).
- *Datos descargados después de la etiqueta.* Marcados `posterior_prereg`.
- *La ilustración de la contabilidad* con magnitudes de la literatura.
- *Réplicas del plan sobre preguntas ya vistas.* Las especificaciones que repiten una pregunta cuyo resultado ya se conocía llevan la marca `repite_visto` (plan, 0.2).

**Capa y lenguaje.** Toda cifra V18 es de capa C4 con nivel de evidencia EXPLORATORIO. Ninguna estimación es IDENTIFICADO, de modo que no se usa en ningún lugar la fórmula condicional prevista. El documento no formula ninguna cifra V18 como causa: cada una es una asociación condicionada al diseño. El generador del documento (src/v18/f6_documento.py) toma todas las cifras de output/v5/cifras_clave.csv y falla si un marcador no existe.
