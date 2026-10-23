## Anexo C. Reproducciones y fichas bibliográficas

### C.1 Reproducciones

La fase 2 reproduce con el paquete de su autor, y sin datos del proyecto, los estudios que lo tienen abierto. El veredicto es «coincide» (la misma cifra al redondeo publicado, o una diferencia menor que la fijada en el plan y dentro del error), «difiere con explicación» o «difiere sin explicación» (parada). Ninguna reproducción difiere sin explicación. Las tres coinciden:

| Estudio (especificación) | Publicado | Reproducido |
|---|---|---|
| Borusyak, Hull y Jaravel (2022), columna 5 de la tabla 4 del artículo; IC95 con el nulo impuesto | {{V18-AUX-REP-BHJ-PUB:sig}} (IC95 {{V18-AUX-REP-BHJ-PUB:min_sig}} a {{V18-AUX-REP-BHJ-PUB:max_sig}}) | {{V18-AUX-REP-BHJ-REP:sig}} (IC95 {{V18-AUX-REP-BHJ-REP:min_sig}} a {{V18-AUX-REP-BHJ-REP:max_sig}}) |
| Chaves-Fonseca (2026), columna 6 (IV), Madrid | {{V18-AUX-REP-CHAVES-PUB:sig}} (error típico {{V18-AUX-REP-CHAVES-PUB-ET:sig}}) | {{V18-AUX-REP-CHAVES-REP:sig}} (IC95 {{V18-AUX-REP-CHAVES-REP:min_sig}} a {{V18-AUX-REP-CHAVES-REP:max_sig}}) |
| Mense (2025), columna 3 (IV), Alemania | {{V18-AUX-REP-MENSE-PUB:sig}} (error típico {{V18-AUX-REP-MENSE-PUB-ET:sig}}) | {{V18-AUX-REP-MENSE-REP:sig}} (IC95 {{V18-AUX-REP-MENSE-REP:min_sig}} a {{V18-AUX-REP-MENSE-REP:max_sig}}) |

Los artículos de Chaves-Fonseca y de Mense publican el error típico y no el intervalo; el detalle por columna está en output/v18/reproduccion/*/tabla.csv.

| Estudio | Método reproducido | Veredicto |
|---|---|---|
| Chaves-Fonseca (2026), tabla 2 | IV shift-share (proximidad a atractivos por búsquedas de Google), efectos fijos de barrio y año, errores agrupados por barrio; Madrid, precios | coincide |
| Mense (2025), tabla 3A | IV-2SLS en panel con efectos fijos de región y año, instrumento de lluvia; alquiler | coincide |
| Borusyak, Hull y Jaravel (2022), tabla 4 | IV shift-share a nivel de sector, aplicación de Autor, Dorn y Hanson | coincide; la herramienta (src/v18/reproduccion/bhj_lib.py) queda validada |

Sin reproducción por falta de paquete con datos: Garcia-López et al. (2020), Jofre-Monseny et al. (2023), Monràs y García-Montalvo (2023), González y Ortega (2013), Fack, Gibbons y Manning y Grislain-Letrémy y Trevien (E4), Saiz (2010), Best y Kleven (2018) y Besley et al. (2014), Badarinza y Ramadorai (2018) y Cvijanović y Spaenjers (2021), la literatura de grandes tenedores, Segú (2020; impuesto sobre la vivienda vacía en Francia, otro trabajo que Segú 2018) y Koster y van Ommeren (2019). Baum-Snow y Han (2020) solo tiene código y su paquete completo no cabe en el disco; Asquith, Mast y Reed (2020) solo tiene código, sin datos. Jarociński y Karadi (2020) y Altavilla et al. (2019) aportan series de choques, que se usan como dato.

### C.2 Fichas bibliográficas

La fase 1 fijó los criterios antes de buscar (docs/v18/bib/criterios.md): diseño cuasi experimental o estructural, datos de España o de mercados europeos comparables, y publicación en revista con revisión, documento de banco central o serie reconocida de documentos de trabajo. Se hizo una ficha por estudio, agrupadas por factor (docs/v18/bib/<factor>/), con una tabla de efectos y su unidad. El catálogo está en output/v18/f1/catalogo.csv: {{V18-AUX-CAT-FICHAS:sig}} fichas, {{V18-AUX-CAT-TEXTO-COMPLETO:sig}} leídas en texto completo, {{V18-AUX-CAT-SOLO-RESUMEN:sig}} solo por el resumen y {{V18-AUX-CAT-SIN-INDICAR:sig}} sin indicar el grado de lectura; {{V18-AUX-CAT-PAQUETE:sig}} con paquete de replicación. Por el estado de la referencia: {{V18-AUX-CAT-VERIFICADA:sig}} VERIFICADA, {{V18-AUX-CAT-NO-VERIFICADA:sig}} NO VERIFICADA y {{V18-AUX-CAT-DISCREPANTE:sig}} DISCREPANTE (detalle por factor en output/v18/f1/informe.md).

Los PDF y los paquetes de replicación están solo en disco, con sha256 en data/bib/CHECKSUMS.sha256, y no se versionan. Al repositorio van la ficha, el enlace, el DOI, la licencia y las notas, con citas breves. Estado: VERIFICADA es DOI comprobado con Crossref o DataCite; el cuartil de Scimago no está verificado (tarea del autor). DISCREPANTE es una ficha de versión de trabajo cuyo DOI corresponde a la versión publicada (otro año o título), y se trata como NO VERIFICADA. No se cita ninguna cifra de la versión publicada sin leerla.

Inmigración (E3). {{V18-B5-E3:cobertura}}.

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
| E5 | Baum-Snow y Han (2020, versión de trabajo; publicado en 2024) | DISCREPANTE | Sí |
| E5 | Paciorek (2012) | VERIFICADA | Sí |
| E6 | Mense (2025) | VERIFICADA | Sí (único estudio) |
| E6 | Asquith, Mast y Reed (2020, versión de trabajo; publicado en 2023) | DISCREPANTE | No: otra unidad |
| E7 | San Juan (2023) | VERIFICADA | No: intervalos solo en un gráfico |
| E7 | BCE, Boletín Económico 6/2022 | NO VERIFICADA | No: sin error típico |
| E8 | Dolls et al. (2020) | VERIFICADA | No: sin error típico recuperado |
| E9 | Sá (2016) | VERIFICADA | No: sin error típico extraído |
| E9 | Álvarez, Blanco y García-Posada (2020) | NO VERIFICADA | No: regresión transversal sin instrumento |

Los valores por estudio están en output/v18/f5/magnitudes_estudios.csv y también en cifras_clave, con ids V18-AUX-LIT-* (tabla B.0 del anexo B).
