# V18 · Estado

V18: bibliografía, replicación de estudios y estimación del impacto de cada factor (docs/v18/plan.md). V17 cerrada dentro de V18 (fases 0-3 y 5; docs/v17/resumen.md).

## Hecho
- 2026-10-20 · **Infraestructura C.**
  - Subagentes nuevos: bibliotecario y replicador-estudio (.claude/agents/).
  - Comandos /v18-fase0 … /v18-fase6 y /v18-estado; objetivos make v18_f0 … v18_f6, v18 y check_v18 (dentro de make check).
  - Puerta del plan de replicación (src/v18/etiqueta.py): etiqueta local plan-replicacion-v18 con su commit en la rama remota. La guarda (g) del hook rechaza las fases 3 a 6 y make v18 sin ella; src/v18/fase.py lo comprueba también.
  - check_v18: cifras V18 con id, fuente, capa y clasificación; sin lenguaje causal por debajo de IDENTIFICADO; ninguna estimación anterior a la etiqueta; ningún PDF versionado, citas de 15 palabras como máximo y sha256 de cada PDF.
  - data/bib/ fuera de git salvo data/bib/CHECKSUMS.sha256; registro de subagentes con tope de 6 millones por fase.

- 2026-10-20 · **Fase 0 cerrada.** V17 completa (check_v17 sin errores). Inventario de 103 variables (output/v18/f0/): E1, E2, E3, E5, E6 (piloto en València), E7, E8, E9 y F1-F3 replicables en parte; E4, E10, E11 y E12 NO ESTIMABLES con los datos actuales. Paneles provinciales con 39 provincias (11 selladas fuera). 14 tareas del autor al principio de docs/v18/tareas_autor.md.

- 2026-10-20 · **Fase 1 (bibliografía).** Criterios fijados antes de buscar (docs/v18/bib/criterios.md). Tres bibliotecarios: 181 fichas en 13 factores (docs/v18/bib/), con tabla de efectos y unidad por factor. DOI verificados con el verificador de V15 (src/v18/f1_bibliografia.py; caché docs/v18/bib/crossref_cache.json): 125 VERIFICADAS, 45 NO VERIFICADAS (sin DOI o sin registro), 11 DISCREPANTES por versión de trabajo frente a publicada. Catálogo: output/v18/f1/. PDFs y paquetes solo en disco con sha256. Pendientes: repetir la búsqueda sistemática con OpenAlex (cuota agotada el 2026-10-20) y cuartiles Scimago (tarea del autor).
  - Hallazgos: González y Ortega 2013 es 2000-2010 y «un cuarto» (el «un tercio» 1998-2008 es el IZA 2009); Monràs y García-Montalvo usan contratos del Incasòl, no anuncios (E2 pasa a replicable en principio); sin estudios con datos españoles en E10 y E11; única evidencia española con diseño en ayudas: Jiménez Zambrano y Pérez Asenjo (2026, deducción de 2011).

- 2026-10-20 · **Fase 2 cerrada.** Tres reproducciones con el paquete de su autor, las tres «coincide»: Chaves-Fonseca (2026, tabla 2: 0,0197 frente a 0,020 por 100 anuncios), Mense (2025, tabla 3A: −0,1916 frente a −0,192) y Borusyak-Hull-Jaravel (2022, ADH tabla 4: 11 de 11; herramienta shift-share src/v18/reproduccion/bhj_lib.py validada). Los demás estudios clave no tienen paquete con datos y pasan a la fase 3 solo con su especificación (docs/v18/reproduccion.md). Sin parada G.

- 2026-10-20 · **Fase 3.** Plan de replicación (docs/v18/plan_replicacion.md) revisado por revisor-preregistro (APTO CON CAMBIOS, 28 hallazgos) y abogado-del-diablo (resiste con limitaciones); decisión del autor K2 (toda cifra V18 en C4; fórmula condicional solo en secciones técnicas; evaluate_v18 diferido); adenda (docs/v18/plan_replicacion_adenda.md) que responde a todos los hallazgos: ventana trimestral de E2 2019T1-2022T1, E2 por tramo NO ESTIMABLE, padrón por nacionalidad cortado en 2022, multiverso enumerado (245 variantes + 200 de holgura), B5 sin filtro por significación, 7 hipótesis para evaluate_v18. Barcelona pierde Gràcia, Sant Andreu y Nou Barris (sellados V15/V16): 48 clusters.

- 2026-10-20 · **Monte Carlo de herramientas (sección 1.13).** Nueve herramientas validadas con procesos simulados que reproducen la estructura de los diseños de V18 (grupo B; decisión K5): cs_webb APTO CONDICIONADO (solo diseños municipales; NO APTO con 8 clusters), sa_webb APTO, dcdh_aleatorizacion APTO (Webb con 8 clusters NO APTO), honest_did APTO CONDICIONADO (solo M̄ = 0), sdid_conley_taber APTO (con tratados intercambiables), aleatorizacion APTO, lp_iv NO APTO, svar_proxy NO APTO, meta_bayes NO APTO (conservador). R = 2.000 a 5.000. Sin parada G.

- 2026-10-20 · **Fase 3 cerrada.** Etiqueta plan-replicacion-v18 (ad4385c, en la rama remota; la subida de la etiqueta es tarea del autor). Sellado de entrenamiento docs/v18/sellado_v18.json (K4).
- 2026-10-20 · **Fase 4 cerrada** (make check limpio). Monte Carlo de 15 herramientas (K5; BHJ con pocos choques, Driscoll-Kraay con T corto, LP-IV, SVAR con proxy, BVAR y metaanálisis NO APTOS). Estimaciones (output/v18/estimacion/), todas C4:
  - E2-R1 (Ley 11/2020, renta): −0,0384, SUGESTIVO con frase de limitación obligatoria (K9); réplica ciega coincide; dos rondas del abogado del diablo.
  - NO CONCLUYENTE: E3-R1 (inmigración), E1-R4 (Sagrada Família, K8 bis).
  - ASOCIACIÓN: E8-R1 (ITP), E2-R1c, E1-R3, E10-A1, E12-A2, F1-F3 (corto plazo; sin cointegración), E7 BVAR (informativa).
  - NO ESTIMABLE: E4, E5, E6, E7 (primera etapa débil), E9, E11 y la mayoría de ampliaciones.
  - Ninguna IDENTIFICADO; sin parada G. Paquete de herramientas renombrado a src/v18/herr18 (choque con src/v8/herramientas).

- 2026-10-20 · **Fase 5 (código y salidas; pendiente de revisión del orquestador).** src/v18/f5_magnitudes.py y f5_contabilidad.py (en FASES["f5"]), tests/v18/test_f5.py, salidas en output/v18/f5/ (magnitudes, magnitudes_estudios, sensibilidad_b5, contabilidad, contabilidad_ilustracion, comparacion_v8, respuesta, hechos.json, informe.md). B5: solo E2-R1 (SUGESTIVO) es estimación propia válida y E2 no alcanza magnitud preferida (decisión distinta en las tres priors; I² = 0,95); E3 y E5 sin magnitud preferida (I² > 75 %); E1, E4 y E6 con magnitud solo de la literatura; E7-E9 con rango sin error típico. Contabilidad principal sin filas con cifra (100 % sin explicar); ilustración aparte con literatura. Decisiones en K10. check_v18, check_v17, check_v15 y ruff sin errores. Tokens del modelizador: ≈ 350.000 (a registrar en docs/v18/subagentes.csv).

- 2026-10-20 · **Fase 6, primera parte (infraestructura del Documento de Trabajo; pendiente de make del orquestador).** src/v18/f6_hechos.py (570 cifras -> output/v18/f6/hechos.json; FASES["f6"] = f6_hechos, cifras_clave, f6_documento); cifras_clave lee ese fichero y añade la columna clasificacion_v18 (423 filas V18- nuevas; las anteriores sin cambios, comprobado sobre una copia); check_v13 admite V18- solo con origen output/v18/f6/hechos.json; prefijos V18- en tests/test_k4a_cifras.py; render.muestra_rango trata V18 como V17. src/v18/f6_documento.py: esqueleto en output/v18/documento/plantilla/ -> documento_v18.md (falla si un marcador no existe) y tablas_v18.xlsx (impactos, magnitudes, estimaciones, contabilidad). publicacion.py copia ambos a publicacion/documento_v18/. check_v18, control 6: documento publicado y lenguaje causal por sección. Escrituras autorizadas de cifras_clave.csv/.md registradas. Decisiones en K11.

## Siguiente
- Orquestador: `python3 src/v5/cifras_clave.py`, `python3 src/v18/f6_documento.py`, `make publicacion` y `make check` (hasta entonces check_v18 da 2 errores, publicacion/documento_v18/ no existe, y tests/v7_1/test_publicacion y tests/v18/test_infra_v18::test_repositorio_pasa fallan).
- Fase 6, segunda parte: redacción del Documento de Trabajo sobre la plantilla, árbitro-final y verificador-cifras.

## Subagentes y tokens

Generada por src/v18/registro_subagentes.py (fuente: docs/v18/subagentes.csv). Tokens aproximados según el informe de cada subagente. Tope por fase: 6.000.000 (parada G).

| Fecha | Fase | Rol | Tarea | Tokens | Ficheros |
|---|---|---|---|---|---|
| 2026-10-20 | F0 | general-purpose | inventario de datos por estudio (E1-E12, F1-F3) y tareas del autor | 259.633 | src/v18/f0_inventario.py; output/v18/f0/; docs/v18/tareas_autor.md |
| 2026-10-20 | F1 | bibliotecario | grupo B: inmigración, oferta y suelo, obra nueva, vivienda pública (47 fichas) | 470.079 | docs/v18/bib/{inmigracion,oferta_suelo,obra_nueva,vivienda_publica}/ |
| 2026-10-20 | F1 | bibliotecario | grupo A: turismo, topes, grandes tenedores, vacías (51 fichas) | 550.339 | docs/v18/bib/{turismo,topes,grandes_tenedores,vacias}/ |
| 2026-10-20 | F1 | bibliotecario | grupo C: ayudas, tipos, fiscalidad, no residentes, modelos de conjunto (83 fichas) | 610.266 | docs/v18/bib/{ayudas,tipos,fiscalidad,no_residentes,modelos_conjunto}/ |
| 2026-10-20 | F2 | replicador-estudio | Chaves-Fonseca 2026 (tabla 2, precios): coincide | 41.311 | src/v18/reproduccion/chavesfonseca2026.py; output/v18/reproduccion/chavesfonseca2026/ |
| 2026-10-20 | F2 | replicador-estudio | Mense 2025 (tabla 3A, IV con lluvia): coincide | 65.000 | src/v18/reproduccion/mense_2025.py; output/v18/reproduccion/mense_2025/ |
| 2026-10-20 | F2 | replicador-estudio | Borusyak-Hull-Jaravel 2022 (ADH, tabla 4): coincide; bhj_lib | 76.806 | src/v18/reproduccion/{bhj_lib,borusyak_hull_jaravel_2022}.py; output/v18/reproduccion/borusyak_hull_jaravel_2022/ |
| 2026-10-20 | F3 | general-purpose | plan de replicación (B1), E1-E12 y F1-F4 | 354.665 | docs/v18/plan_replicacion.md |
| 2026-10-20 | F3 | abogado-del-diablo | ataque a los diseños del plan de replicación (T1-T5, E1-E12, F) | 127.140 | docs/v18/revision_plan/abogado_del_diablo.md |
| 2026-10-20 | F3 | revisor-preregistro | revisión del plan de replicación (28 hallazgos; APTO CON CAMBIOS) | 181.919 | docs/v18/revision_plan/revisor_preregistro.md |
| 2026-10-20 | F3 | general-purpose | adenda del plan de replicación (respuesta a 28 + AD hallazgos) | 321.538 | docs/v18/plan_replicacion_adenda.md; src/v18/f0_inventario.py |
| 2026-10-20 | F4 | general-purpose | sellado de entrenamiento (sellado_v18.json, sellado.py) | 294.114 | src/v18/{f3_sellado,sellado}.py; docs/v18/sellado_v18.json |
| 2026-10-20 | F4 | montecarlo | grupo A: BHJ, Webb TWFE, IV débil, Driscoll-Kraay, Conley | 185.171 | output/v18/montecarlo/{bhj,webb_twfe,iv_debil,driscoll_kraay,conley}/ |
| 2026-10-20 | F4 | montecarlo | grupo B: CS y SA con Webb, dCDH, Honest DiD, SDID y Conley-Taber, aleatorización, LP-IV, SVAR proxy, metaanálisis | 453.618 | output/v18/montecarlo/ |
| 2026-10-20 | F4 | modelizador | E2 topes (Ley 11/2020) y E8 ITP | 569.802 | src/v18/estimacion/{e2,e8}_*.py; output/v18/estimacion/{e2,e8}/ |
| 2026-10-20 | F4 | modelizador | F1-F3 (sin cointegración: solo corto plazo) y E7 tipos (primera etapa débil: NO ESTIMABLE) | 511.431 | src/v18/estimacion/{f_*,e7_tipos}.py; output/v18/estimacion/{f_conjunto,e7}/ |
| 2026-10-20 | F4 | modelizador | E3 (NO CONCLUYENTE), E5 y E9 (NO ESTIMABLES) | 751.395 | src/v18/estimacion/{e3_*,e5_*,e9_*,_e359_*,e359_*}.py; output/v18/estimacion/{e3,e5,e9}/ |
| 2026-10-20 | F4 | abogado-del-diablo | ronda 1 B6: E2-R1, E2-R1c, E8-R1 | 119.872 | docs/v18/revision_estimaciones/ronda1_e2_e8.md |
| 2026-10-20 | F4 | replicador-ciego | réplica ciega E2-R1 (coincide) y E8-R1 (coincide) | 165.658 | src/v18/replica/; output/v18/replica/ |
| 2026-10-20 | F4 | modelizador | E7-R3/A1 BVAR (MC NO APTO; informativas), E4, E10-E12 | 365.382 | src/v18/estimacion/{e7_bvar*,e4_e10_e12}.py; output/v18/estimacion/{e7_bvar,e4,e10,e11,e12}/ |
| 2026-10-20 | F4 | modelizador | E1 turismo (R3 ASOCIACIÓN, R4 nulo acotado SUGESTIVO, resto NO ESTIMABLE) y E6 obra nueva (NO ESTIMABLE) | 635.935 | src/v18/estimacion/{e1,e6}_*.py; output/v18/estimacion/{e1,e6}/ |
| 2026-10-20 | F4 | replicador-ciego | réplica ciega E1-R4 (difiere en la muestra; TOST no acota) | 96.878 | src/v18/replica/e1_r4.py; output/v18/replica/e1_r4/ |
| 2026-10-20 | F4 | modelizador | B6: robustez de E2-R1, claves de sellado nuevas, K7 en scripts | 247.707 | src/v18/estimacion/e2_robustez.py; output/v18/estimacion/e2/robustez_b6.csv |
| 2026-10-20 | F4 | modelizador | corrección de E1-R4 (geometría, TOST con Webb) | 78.403 | src/v18/estimacion/e1_*.py; output/v18/estimacion/e1/ |
| 2026-10-20 | F4 | abogado-del-diablo | ronda 2 B6: E2-R1 (SUGESTIVO con limitación) | 71.619 | docs/v18/revision_estimaciones/ronda2_e2r1.md |
| 2026-10-20 | F4 | modelizador | E1-R4 principal sin adelantos (NO CONCLUYENTE; v3 con adelantos SUGESTIVO nulo acotado) | 100.844 | src/v18/estimacion/e1_*.py; output/v18/estimacion/e1/ |
| 2026-10-20 | F4 | modelizador | K9 en E2-R1: paro trimestral (−0,0384), frase de limitación, D1 corregida | 86.575 | src/v18/estimacion/e2_*.py; output/v18/estimacion/e2/ |
| 2026-10-20 | F5 | modelizador | magnitudes preferidas (B5) y contabilidad de la subida | 350.040 | src/v18/f5_*.py; output/v18/f5/ |
| 2026-10-20 | F6 | general-purpose | infraestructura del Documento de Trabajo: cifras V18 en cifras_clave, generador, tablas, publicación, control | 270.213 | src/v18/f6_*.py; output/v18/f6/; output/v18/documento/ |
| 2026-10-20 | F6 | redactor | redacción del Documento de Trabajo (16 secciones) | 496.360 | output/v18/documento/plantilla/ |
| 2026-10-21 | F6 | general-purpose | cifras V18-AUX y marcadores de los 14 huecos | 234.898 | src/v18/f6_hechos.py; output/v18/documento/plantilla/ |
| 2026-10-21 | F6 | arbitro-final | revisión del Documento de Trabajo (REVISAR, 23 hallazgos) | 157.261 | docs/v18/revision_documento/arbitro_ronda1.md |
| 2026-10-21 | F6 | verificador-cifras | verificación de cifras del Documento (0 discrepancias numéricas; 4 de texto; 7 cifras libres) | 145.784 | docs/v18/revision_documento/verificador_ronda1.md |
| 2026-10-21 | F6 | general-purpose | revisión del Documento (23 hallazgos del árbitro y verificador) | 518.924 | output/v18/documento/plantilla/; src/v18/f5_*.py; src/v18/f6_*.py |
| 2026-10-21 | F6 | arbitro-final | ronda 2 del Documento (REVISAR menor: 21/23 resueltos, 10 nuevos editoriales) | 130.505 | docs/v18/revision_documento/arbitro_ronda2.md |
| 2026-10-21 | F6 | general-purpose | revisión menor ronda 2 (N1-N10; columna 1995-2007 en ventana común) | 295.280 | src/v18/f5_contabilidad.py; src/v18/f6_*.py; output/v18/documento/plantilla/ |

| Fase | Tokens de subagentes |
|---|---|
| F0 | 259.633 |
| F1 | 1.630.684 |
| F2 | 183.117 |
| F3 | 985.262 |
| F4 | 4.734.404 |
| F5 | 350.040 |
| F6 | 2.249.225 |

Total V18: 10.392.365 tokens

<!-- fin subagentes -->
