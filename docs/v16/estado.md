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

## Siguiente
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

| Fase | Tokens de subagentes |
|---|---|
| F1 | 1.952.870 |
| F2 | 690.657 |
| F3 | 1.160.356 |
| F4 | 555.674 |
| F5 | 438.656 |

Total V16: 4.798.213 tokens

<!-- fin subagentes -->
