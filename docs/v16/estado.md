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

## Siguiente
- Fase 1: adquisición. Lo que requiera al autor va primero a tareas_autor. Después vienen la base de intervenciones, el registro de licencias, la normalización, la auditoría y el inventario.

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

| Fase | Tokens de subagentes |
|---|---|
| F1 | 1.689.072 |
| F2 | 323.309 |
| F3 | 1.160.356 |

Total V16: 3.172.737 tokens

<!-- fin subagentes -->
