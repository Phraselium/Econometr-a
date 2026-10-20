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

## Siguiente
- Etiqueta plan-replicacion-v18 y push; sellado_v18.json; fase 4 (estimación).

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

| Fase | Tokens de subagentes |
|---|---|
| F0 | 259.633 |
| F1 | 1.630.684 |
| F2 | 183.117 |
| F3 | 985.262 |
| F4 | 4.396.963 |

Total V18: 7.455.659 tokens

<!-- fin subagentes -->
