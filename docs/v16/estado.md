# V16 · Estado

Plan: docs/v16/plan.md (íntegro). Pre-registros internos sin sello de tiempo externo. La versión 1.0 no cambia de valor. V16 añade cifras V16-* y se publicará como 2.0.

## Hecho
- **Plan.** Guardado íntegro (7615269) y aviso en CLAUDE.md.
- **B1 · Guardas** (decisiones K1).
  - La guarda (d) exige prereg-v15 en el remoto en 542b4fd.
  - La guarda nueva (f) exige prereg-v16 en el remoto para las fases 5 a 7 y el objetivo v16.
  - check_v16 controla que las estimaciones no sean anteriores a su etiqueta.
  - Tests: tests/v16/test_guardas.py (26).
  - Pruebas en vivo: el hook bloqueó las fases 6 y completa de V16 y la fase 4 de V15; los lanzadores de fase llamados sin make terminan con código 1.
- **B2 · Subagentes nuevos.** adquisidor-datos, ingeniero-datos, replicador-ciego, abogado-del-diablo, redactor y verificador-cifras (K2).
- **B3 · Comandos y make.**
  - Comandos /v16-fase0 … /v16-fase7 y /v16-estado.
  - Objetivos make v16_f0 … v16_f7, v16 y check_v16, este último dentro de make check.
  - src/v16/fase.py y src/v16/registro_subagentes.py (tokens por fase y aviso de 6 millones).
- **Bloqueo B-1.** El remoto rechaza las etiquetas (HTTP 403). Los comandos para publicarlas están en tareas_autor.
- **F0.1 · Pre-registro interno.**
  - proyecto.json lleva `preregistro_tipo: "interno, sin sello externo"` y ninguna clave osf_prereg (check_v16 lo comprueba).
  - La puerta de V15 (src/v15/puerta.py) y la guarda (d) usan la etiqueta, no OSF.
  - La sección OSF de docs/v15/tareas_autor.md queda sustituida.
  - La publicación de las etiquetas sigue bloqueada (B-1).
- **F0.2 · Correcciones previas** (output/v16/f0/comprobaciones.json, `todo_ok`).
  - 3.642.696 filas v6 marcadas y 0 sin marcar, en la base y en la capa pública.
  - 11 de 11 bajadas de capa en output/v5 y en publicacion.
  - Los tres metadatos corregidos.
  - make check limpio al cerrar la fase.
- **F0.3 · Una página.** La plantilla docs/v5/plantillas/una_pagina.md se ha reorganizado en tres bloques:
  - hechos C1 con dos fuentes independientes;
  - estadísticas oficiales de fuente única C4 (ejemplos nuevos: E-T7-prod y V10-ATL-A1);
  - cotas C2.
  Ningún valor cambia. La página se ha regenerado con make publicacion.
- **F0.4 · Lo ya visto.** docs/v16/lo_ya_visto.md (107 filas de cifras_clave, auditorías de V15 y pre-registro de V15), generado por src/v16/f0_lo_ya_visto.py.
- **Duda para el autor:** la independencia de dh_2125 (ECP y EPA), en tareas_autor §2.
- Fase 0 sin subagentes (0 tokens).
- **F1 · Datos** (inventario: docs/v16/inventario_fuentes.csv, 655 ficheros; licencias en los manifiestos por familia, K5).
  - Familias descargadas: renta_parque, oferta_suelo, demanda_internacional, alquiler_turismo y tension_social.
  - Base de intervenciones: 476 filas.
  - Normalización a formato largo: 5 familias, cada una con sus tests.
  - Auditorías: output/v16/auditoria/<familia>. Correcciones: partidos judiciales de 2025 excluidos y K6 (fuentes no independientes).
  - Lo que depende del autor: tareas_autor §3 y §4.
  - K8: la muestra v6 cubre 8 CCAA enteras.
- **F2 · Hechos y diagnóstico** (C4 salvo 3 C1; ninguna discrepancia con la 1.0):
  - output/v16/f2_hechos: 56 cifras;
  - f2_contabilidad: hogares 2021-2025 y factor común provincial;
  - f2_esfuerzo: ECV 2004-2025, validada con Eurostat en 2013-2025, con Oaxaca-Blinder, DFL y RIF;
  - f2_atlas: 32 indicadores en 7 escalas, con supresión e incertidumbre.
  - Las cifras V16-* pasan a cifras_clave en la fase 7, con la 2.0.
- **F3 · Literatura y mecanismos.**
  - docs/v16/literatura.md: 7 instrumentos y 115 fichas (72 VERIFICADAS, 43 NO VERIFICADAS, ninguna DISCREPANTE).
  - Metaanálisis con regla fija (K7): ningún grupo llega a 5 estudios con error estándar.
  - Marco de cuatro cuadrantes calibrado: output/v16/f3.
- **F4 · Pre-registro interno V16.**
  - Potencia con placebos: output/v16/potencia.
  - Bloque sellado V16: src/holdout.py; 28 celdas, 777 municipios y 1.118 distritos, sin solapes con v6 ni V15.
  - docs/v16/preregistro_v16.md más una adenda vinculante que responde punto por punto a revisor-preregistro y abogado-del-diablo: nada confirmatorio nuevo; V16 C4 como máximo; dos ramas de control (21 + 83); rejilla fija.
  - Sellado ejecutado: docs/v16/sellado_v16.json; entrenamiento en data/processed/v16/entrenamiento.
  - H1-H5 de V15 intactas.
  - Desviación D1 y decisión K9.
- **Etiquetas publicadas (K10).**
  - Las 11 prereg-* están en el remoto, comprobadas en esta sesión.
  - Puertas con etiqueta y criterio provisional; tests y autocomprobación actualizados.
  - Registro: docs/preregistros.md, que check_v16 verifica.
  - CHANGELOG corregido.
- **Fase 5: Monte Carlo (K12).**
  - 16 herramientas V16 validadas con el criterio de la adenda (punto 11).
  - Utilizables: SDID con Conley-Taber, Conley por sección (con salvedad), GSADF con bootstrap salvaje, Benjamini-Yekutieli y TOST condicionado.
  - El resto es NO APTO y queda descriptivo.
  - Tabla en docs/v16/validacion_montecarlo.md.
  - V15 (K13): 8 herramientas. Solo SAR/SDM y DM-HLN son APTAS; tabla en docs/v15/validacion_montecarlo.md.
- **Fase 6 (en curso).**
  - Grupo A (Q1, Q2, Q7, Q8) y grupo B (Q3, Q4, Q6) estimados en entrenamiento, C4 y pendientes de sellado. Desviaciones D2 (B) y D3 (A).
  - Q1b no es estimable en el entrenamiento.
  - Q3-b es el único resultado con inferencia válida.
  - Grupo C (Q5, Q9, Q10 y la rejilla de 83 celdas) estimado. Desviaciones D4.
  - Control BY (src/v16/f6_fdr.py): ninguna prueba cumple la condición (a). Q3-b la cumplía antes de K16; Q9-g tiene q = 0,306 (era 0,153 antes de K16).
  - Parada D (B-2) por Q9-g, resuelta por el autor el 2026-10-18: pista no confirmada C4 (K15).
  - V15 en entrenamiento (K14): H1-H5 y E1-E4 estimados, todo C4 y `pendiente_sellada`.
    - Con inferencia válida: H5 (DM-HLN p = 0,894; el AR(4) no se supera) y E3 (ρ SAR = 0,39).
    - El resto solo con estimación puntual.
    - Desviaciones DV15-A y DV15-B.
  - make check en solitario, 0 errores, sin cambios en git (2026-10-17). Se corrigió una colisión de importación en src/v15/montecarlo/honest_did.py: ahora importa src.v9.herramientas por paquete.

## Siguiente
- Parada D (B-2) resuelta con K15.
- **Réplica ciega (K16).**
  - Coinciden: Q9-g, E3 y H1.
  - Q3-b, H5 y H4 discrepaban y se resolvieron:
    - núcleo de Conley corregido: Conley pasa a NO APTO, y Q3-b y H3 quedan puntuales;
    - H5: tres errores corregidos; razón 1,51 frente a 1,15 en la réplica, misma conclusión;
    - H4: imputación retirada, 0,305.
  - En la rama de diseños, el q de Q9-g es ahora 0,306.
- **Triangulación** (src/v16/f6_triangulacion.py, output/v16/triangulacion/):
  - Ningún grupo de la literatura admite metaanálisis, así que se compara el signo.
  - Se apartan Q2c y Q6-v, explicados y descriptivos.
  - Entre diseños, el único par con signo distinto es H3 frente a Q2c.
- **Revisión adversarial (K17).** Tres revisiones, con respuesta en output/v16/critica/respuestas.md.
  - Correcciones: la principal de Q2c y el multiverso de Q6.
  - Pistas citables: H1 (solo signo), H5, E3 y Q6-p. Correlaciones frágiles: Q3-b y H4.
  - Q9-g va solo a la Parte VII.
- **Doble implementación:** no aplica; ninguna cifra es candidata a C3 o C3s.
- **Fase 6 cerrada (2026-10-18)** con make check en solitario: 0 errores, git sin cambios.
- **evaluate_v16:** no aplica; ninguna pregunta cumple (a) y (b).
- **evaluate_v15:** según su calendario.
- **PARADA B-3 (2026-10-18).** La auditoría de alcance de los errores K16 encuentra que E4 afecta a 8 filas de publicacion/tablas_v8.xlsx (V8-M5, IV3). Entrada en ERRATA, pendiente de decisión del autor. No cambia ninguna cifra de cifras_clave ni ninguna capa. La fase 7 espera.
- Antes de la fase 7 (encargo del 2026-10-18):
  - K18 aclara el q de Q9-g (0,153 → 0,306) y el rango de H5 (1,15-1,51).
  - Réplicas ciegas: Q2a y H3 coinciden; Q6-p tenía un error, ya corregido.
  - Alcance de los errores en v1-V12: docs/v16/alcance_errores_k16.md.
- **Fase 7: informe integral.** Redactor, verificador de cifras y árbitro final; integrar en cifras_clave las cifras V16-* citables (K17); tablas_v16.xlsx, web y make v16.
- Fases 5-7 de V16:
  - fase 5: Monte Carlo de las herramientas;
  - fase 6: estimación exploratoria con la rejilla fija y los diseños de la adenda;
  - fase 7: informe integral y 2.0.

## Subagentes y tokens

Generada por src/v16/registro_subagentes.py (fuente: docs/v16/subagentes.csv). Tokens aproximados según el informe de cada subagente. Tope por fase: 6.000.000 (parada D).

| Fecha | Fase | Rol | Tarea | Tokens | Ficheros |
|---|---|---|---|---|---|
| 2026-10-17 | F1 | adquisidor-datos | oferta_suelo | 121.582 | data/raw/v16/oferta_suelo;docs/v16/fuentes/oferta_suelo.md |
| 2026-10-17 | F1 | adquisidor-datos | demanda_internacional | 140.999 | data/raw/v16/demanda_internacional;docs/v16/fuentes/demanda_internacional.md |
| 2026-10-17 | F1 | adquisidor-datos | intervenciones | 240.498 | data/raw/v16/intervenciones;docs/v16/fuentes/intervenciones.md |
| 2026-10-17 | F1 | adquisidor-datos | alquiler_turismo | 119.161 | data/raw/v16/alquiler_turismo;docs/v16/fuentes/alquiler_turismo.md |
| 2026-10-17 | F1 | ingeniero-datos | datos_demanda_internacional | 61.558 | src/v16/datos/demanda_internacional.py;data/processed/v16/demanda_internacional.parquet |
| 2026-10-17 | F1 | adquisidor-datos | tension_social | 82.901 | data/raw/v16/tension_social;docs/v16/fuentes/tension_social.md |
| 2026-10-17 | F1 | ingeniero-datos | datos_tension_social | 139.695 | src/v16/datos/tension_social.py;data/processed/v16/tension_social.parquet |
| 2026-10-17 | F1 | ingeniero-datos | datos_oferta_suelo | 50.757 | src/v16/datos/oferta_suelo.py;data/processed/v16/oferta_suelo.parquet |
| 2026-10-17 | F1 | ingeniero-datos | datos_alquiler_turismo | 199.177 | src/v16/datos/alquiler_turismo.py;data/processed/v16/alquiler_turismo.parquet |
| 2026-10-17 | F3 | lector-literatura | L3_oferta_elasticidad | 148.156 | docs/v16/literatura/L3_oferta_elasticidad.md |
| 2026-10-17 | F3 | lector-literatura | L1_control_alquileres | 270.191 | docs/v16/literatura/L1_control_alquileres.md |
| 2026-10-17 | F1 | auditor-datos | auditoria_lote1 | 190.358 | output/v16/auditoria;src/v16/auditoria |
| 2026-10-17 | F3 | lector-literatura | L4_fiscalidad_compra | 133.818 | docs/v16/literatura/L4_fiscalidad_compra.md |
| 2026-10-17 | F3 | lector-literatura | L5_ayudas_demanda | 129.764 | docs/v16/literatura/L5_ayudas_demanda.md |
| 2026-10-17 | F3 | lector-literatura | L7_vivienda_publica_vacias | 126.467 | docs/v16/literatura/L7_vivienda_publica_vacias.md |
| 2026-10-17 | F3 | lector-literatura | L6_extranjeros_golden_visa | 186.938 | docs/v16/literatura/L6_extranjeros_golden_visa.md |
| 2026-10-17 | F3 | lector-literatura | L2_vivienda_turistica_regulacion | 165.022 | docs/v16/literatura/L2_vivienda_turistica_regulacion.md |
| 2026-10-17 | F1 | adquisidor-datos | renta_parque | 156.933 | data/raw/v16/renta_parque;docs/v16/fuentes/renta_parque.md |
| 2026-10-17 | F1 | auditor-datos | auditoria_alquiler_turismo | 185.453 | output/v16/auditoria/alquiler_turismo |
| 2026-10-17 | F2 | econometrician | f2_hechos | 191.483 | src/v16/f2_hechos.py;output/v16/f2_hechos |
| 2026-10-17 | F2 | econometrician | f2_contabilidad | 131.826 | src/v16/f2_contabilidad.py;output/v16/f2_contabilidad |
| 2026-10-17 | F1 | ingeniero-datos | datos_renta_parque | 146.666 | src/v16/datos/renta_parque.py;data/processed/v16/renta_parque.parquet |
| 2026-10-17 | F1 | auditor-datos | auditoria_renta_parque | 117.132 | output/v16/auditoria/renta_parque |
| 2026-10-17 | F4 | econometrician | f4_potencia | 215.590 | src/v16/f4_potencia.py;output/v16/potencia |
| 2026-10-17 | F4 | revisor-preregistro | revision_prereg | 174.748 | docs/v16/preregistro_v16_adenda.md |
| 2026-10-17 | F4 | abogado-del-diablo | critica_prereg | 165.336 | docs/v16/preregistro_v16_adenda.md |
| 2026-10-17 | F2 | econometrician | f2_atlas | 182.197 | src/v16/f2_atlas.py;output/v16/f2_atlas |
| 2026-10-17 | F2 | econometrician | f2_esfuerzo | 185.151 | src/v16/f2_esfuerzo.py;output/v16/f2_esfuerzo |
| 2026-10-17 | F5 | montecarlo | mc_panel | 152.118 | src/v16/montecarlo;output/v16/montecarlo |
| 2026-10-17 | F5 | montecarlo | mc_iv_espacial | 151.703 | src/v16/montecarlo;output/v16/montecarlo |
| 2026-10-17 | F5 | montecarlo | mc_series | 134.835 | src/v16/montecarlo;output/v16/montecarlo |
| 2026-10-17 | F5 | montecarlo | mc_v15 | 332.369 | src/v15/montecarlo;output/v15/montecarlo |
| 2026-10-17 | F6 | modelizador | grupo_A_q1_q2_q7_q8 | 224.084 | src/v16/q1_zonas.py;output/v16/q1;output/v16/q2;output/v16/q7;output/v16/q8 |
| 2026-10-17 | F6 | modelizador | grupo_B_q3_q4_q6 | 212.505 | src/v16/q3_seccion.py;output/v16/q3;output/v16/q4;output/v16/q6 |
| 2026-10-17 | F6 | modelizador | grupo_C_q5_q9_q10_rejilla | 192.100 | src/v16/q9_burbuja.py;output/v16/q5;output/v16/q9;output/v16/q10;output/v16/rejilla |
| 2026-10-17 | F6 | modelizador | v15_grupo_B_h4_h5_e1_e2_e3 | 180.001 | src/v15/p4_inmigracion.py;output/v15/p4;output/v15/p9;output/v15/p2;output/v15/p7;output/v15/p10 |
| 2026-10-17 | F6 | modelizador | v15_grupo_A_h1_h2_h3_e4 | 200.805 | src/v15/p6_zonas.py;output/v15/p6;output/v15/p5;output/v15/p5cv |
| 2026-10-18 | F6 | replicador-ciego | replica_q9g | 27.198 | src/v16/replica/q9g.py;output/v16/replica/q9g |
| 2026-10-18 | F6 | replicador-ciego | replica_q3b | 27.003 | src/v16/replica/q3b.py;output/v16/replica/q3b |
| 2026-10-18 | F6 | replicador-ciego | replica_e3 | 24.686 | src/v16/replica/e3.py;output/v16/replica/e3 |
| 2026-10-18 | F6 | replicador-ciego | replica_h5 | 39.909 | src/v16/replica/h5.py;output/v16/replica/h5 |
| 2026-10-18 | F6 | replicador-ciego | replica_h1 | 35.255 | src/v16/replica/h1.py;output/v16/replica/h1 |
| 2026-10-18 | F6 | replicador-ciego | replica_h4 | 38.087 | src/v16/replica/h4.py;output/v16/replica/h4 |
| 2026-10-18 | F6 | econometrician | reconciliacion_h5 | 76.212 | output/v16/replica/h5/reconciliacion.md |
| 2026-10-18 | F6 | abogado-del-diablo | critica_inmigracion_burbuja | 65.836 | output/v16/critica/respuestas.md |
| 2026-10-18 | F6 | abogado-del-diablo | critica_regulacion_turismo | 84.297 | output/v16/critica/respuestas.md |
| 2026-10-18 | F6 | abogado-del-diablo | critica_macro_fiscal | 99.404 | output/v16/critica/respuestas.md |
| 2026-10-18 | F6 | replicador-ciego | replica_q2a | 24.882 | src/v16/replica/q2a.py;output/v16/replica/q2a |
| 2026-10-18 | F6 | replicador-ciego | replica_h3 | 26.933 | src/v16/replica/h3.py;output/v16/replica/h3 |
| 2026-10-18 | F6 | replicador-ciego | replica_q6p | 34.809 | src/v16/replica/q6p.py;output/v16/replica/q6p |
| 2026-10-18 | F6 | general-purpose | alcance_errores_k16 | 319.642 | docs/v16/alcance_errores_k16.md |
| 2026-10-18 | F6 | replicador-ciego | replica_1_0_lote_a | 92.595 | src/v16/replica/v10_a.py;output/v16/replica/v10_a |
| 2026-10-18 | F6 | replicador-ciego | replica_1_0_lote_b | 83.443 | src/v16/replica/v10_b.py;output/v16/replica/v10_b |
| 2026-10-18 | F6 | replicador-ciego | replica_1_0_lote_b2 | 65.683 | src/v16/replica/v10_b2.py;output/v16/replica/v10_b2 |
| 2026-10-18 | F6 | replicador-ciego | replica_1_0_lote_d | 88.083 | src/v16/replica/v10_d.py;output/v16/replica/v10_d |
| 2026-10-18 | F6 | replicador-ciego | replica_1_0_lote_c | 99.252 | src/v16/replica/v10_c.py;output/v16/replica/v10_c |
| 2026-10-18 | F6 | replicador-ciego | replica_1_0_lote_b2 | 43.632 | src/v16/replica/v10_b2.py;output/v16/replica/v10_b2 |
| 2026-10-18 | F6 | econometrician | reconciliacion_1_0_v8 | 149.141 | output/v16/replica/v10_d/reconciliacion.md |

| Fase | Tokens de subagentes |
|---|---|
| F1 | 1.952.870 |
| F2 | 690.657 |
| F3 | 1.160.356 |
| F4 | 555.674 |
| F5 | 771.025 |
| F6 | 2.555.477 |

Total V16: 7.686.059 tokens

<!-- fin subagentes -->
