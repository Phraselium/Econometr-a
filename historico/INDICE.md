# Índice del histórico (versiones superadas)

La versión de referencia es la **v7.1**: lo vigente está en [publicacion/](../publicacion/MANIFIESTO.md), [metodologia/](../metodologia/MANIFIESTO.md) y [reproducir/](../reproducir/MANIFIESTO.md). Aquí se ordena lo superado, de la primera versión a la v6.2.

**Qué se ha movido y qué no.**
- **Se han movido** con `git mv`, sin modificarlos, los documentos de versiones cerradas que no lee ningún script, test, plantilla ni el Makefile: planes, estados, bloqueos, revisiones internas, auditorías, arbitrajes simulados y síntesis antiguas. Están en historico/docs/ y historico/output/, con la misma ruta relativa que tenían. `git log --follow <fichero>` muestra su historia completa: no se ha reescrito la historia de git.
- **No se han movido** las salidas de los modelos de cada versión (output/v1-v6_3, output/v7) ni los documentos que algún script o test lee (pre-registros, diccionarios, decisiones, fuentes fallidas, guías). `make all` y `make v7` las regeneran en su ruta, y los entregables vigentes leen parte de ellas (cifras_clave). La tabla siguiente indica dónde está cada versión.

## Versiones

| Versión | Fecha | Etiqueta local (commit) | Salidas | Documentos | Qué la sustituye |
|---|---|---|---|---|---|
| v1 (f2-f7) | 2026-10 | — | output/ (raíz: informe.md, f2-f6) | docs/revision_f1*.md, docs/revision_f3.md; resto en historico/docs/ | v2 y v3: capas de evidencia y validación sellada |
| v2 | 2026-10-10 | prereg-v2 (f59574a) | output/v2/ | docs/v2/ (pre-registro, decisiones, accesos al sellado); planes y revisiones en historico/docs/v2/ | v3 |
| v3 | 2026-10-10 | prereg-v3 (204c073) | output/v3/; síntesis en historico/output/v3/ | docs/v3/; planes y revisiones en historico/docs/v3/ | v4 y v5 |
| v4 | 2026-10-10 | — | output/v4/; síntesis en historico/output/v4/ | docs/v4/; planes y revisiones en historico/docs/v4/ | v5 |
| v5.0 | 2026-10-10 | v5.0 (434c75f), prereg-v5 (1e057cd) | output/v5/ (módulos; los entregables se regeneran como v7.1) | docs/v5/ (plantillas vigentes) | v5.1 |
| v5.1 | 2026-10-11 | v5.1 (02364d3) | output/v5_1/ | docs/v5_1/; plan y estado en historico/docs/v5_1/ | v6 |
| v6.0 | 2026-10-11 | v6.0 (57f3478), prereg-v6 (278cc9e) | output/v6/ | docs/v6/ (hipótesis, diccionario); plan, estado y auditoría en historico/docs/v6/ | v6.1 |
| v6.1 | 2026-10-11 | v6.1 (7a63f9f) | output/v6_1/ | docs/v6_1/ (historial de conclusiones, backlog); auditoría, arbitrajes y carta de respuesta en historico/docs/v6_1/ | v6.2 |
| v6.2 | 2026-10-12 | v6.2 (462ebf1) | output/v6_2/ (el anexo metodológico sigue vigente en metodologia/) | docs/v6_2/ (guía del revisor de v6.2, cifras publicables); plan y revisión en historico/docs/v6_2/ | v7.1 (referencia) |
| v6.3 | 2026-10-12 | (dentro de V7) | output/v6_3/ | ERRATA.md | v7.1 |
| v7.0 | 2026-10-12 | v7.0 (3d1170c), prereg-v7 (3fad305) | output/v7/ (vigente: la v7.1 la amplía) | docs/v7/ (vigente: pre-registro y evaluación diferida) | v7.1 |

Las etiquetas son locales: el remoto rechaza la subida de etiquetas. Publicarlas es una tarea del autor (docs/v7_1/tareas_autor.md).

## Ficheros trasladados en v7.1

| Ruta original | Ruta nueva |
|---|---|
| docs/bloqueos.md | [historico/docs/bloqueos.md](docs/bloqueos.md) |
| docs/preguntas.md | [historico/docs/preguntas.md](docs/preguntas.md) |
| docs/revision_f2.md | [historico/docs/revision_f2.md](docs/revision_f2.md) |
| docs/revision_f4.md | [historico/docs/revision_f4.md](docs/revision_f4.md) |
| docs/revision_f5.md | [historico/docs/revision_f5.md](docs/revision_f5.md) |
| docs/revision_f6.md | [historico/docs/revision_f6.md](docs/revision_f6.md) |
| docs/revision_f7.md | [historico/docs/revision_f7.md](docs/revision_f7.md) |
| docs/v2/estado.md | [historico/docs/v2/estado.md](docs/v2/estado.md) |
| docs/v2/eventos_politica.md | [historico/docs/v2/eventos_politica.md](docs/v2/eventos_politica.md) |
| docs/v2/plan.md | [historico/docs/v2/plan.md](docs/v2/plan.md) |
| docs/v2/revision_BA.md | [historico/docs/v2/revision_BA.md](docs/v2/revision_BA.md) |
| docs/v2/revision_BD.md | [historico/docs/v2/revision_BD.md](docs/v2/revision_BD.md) |
| docs/v2/revision_BI.md | [historico/docs/v2/revision_BI.md](docs/v2/revision_BI.md) |
| docs/v2/revision_BM.md | [historico/docs/v2/revision_BM.md](docs/v2/revision_BM.md) |
| docs/v2/revision_BO.md | [historico/docs/v2/revision_BO.md](docs/v2/revision_BO.md) |
| docs/v2/revision_BP.md | [historico/docs/v2/revision_BP.md](docs/v2/revision_BP.md) |
| docs/v2/revision_BV.md | [historico/docs/v2/revision_BV.md](docs/v2/revision_BV.md) |
| docs/v2/revision_final.md | [historico/docs/v2/revision_final.md](docs/v2/revision_final.md) |
| docs/v3/bloqueos.md | [historico/docs/v3/bloqueos.md](docs/v3/bloqueos.md) |
| docs/v3/estado.md | [historico/docs/v3/estado.md](docs/v3/estado.md) |
| docs/v3/plan.md | [historico/docs/v3/plan.md](docs/v3/plan.md) |
| docs/v3/revision_oleada1.md | [historico/docs/v3/revision_oleada1.md](docs/v3/revision_oleada1.md) |
| docs/v3/revision_oleada2.md | [historico/docs/v3/revision_oleada2.md](docs/v3/revision_oleada2.md) |
| docs/v3/revision_oleada3.md | [historico/docs/v3/revision_oleada3.md](docs/v3/revision_oleada3.md) |
| docs/v4/bloqueos.md | [historico/docs/v4/bloqueos.md](docs/v4/bloqueos.md) |
| docs/v4/estado.md | [historico/docs/v4/estado.md](docs/v4/estado.md) |
| docs/v4/plan.md | [historico/docs/v4/plan.md](docs/v4/plan.md) |
| docs/v4/preguntas_abiertas.md | [historico/docs/v4/preguntas_abiertas.md](docs/v4/preguntas_abiertas.md) |
| docs/v4/revision_oleadaA.md | [historico/docs/v4/revision_oleadaA.md](docs/v4/revision_oleadaA.md) |
| docs/v4/revision_oleadaB.md | [historico/docs/v4/revision_oleadaB.md](docs/v4/revision_oleadaB.md) |
| docs/v4/revision_oleadaC.md | [historico/docs/v4/revision_oleadaC.md](docs/v4/revision_oleadaC.md) |
| docs/v4/revision_oleadaC_it2.md | [historico/docs/v4/revision_oleadaC_it2.md](docs/v4/revision_oleadaC_it2.md) |
| docs/v5_1/bloqueos.md | [historico/docs/v5_1/bloqueos.md](docs/v5_1/bloqueos.md) |
| docs/v5_1/estado.md | [historico/docs/v5_1/estado.md](docs/v5_1/estado.md) |
| docs/v5_1/fuentes_fallidas.md | [historico/docs/v5_1/fuentes_fallidas.md](docs/v5_1/fuentes_fallidas.md) |
| docs/v5_1/instrucciones_subagentes.md | [historico/docs/v5_1/instrucciones_subagentes.md](docs/v5_1/instrucciones_subagentes.md) |
| docs/v5_1/plan.md | [historico/docs/v5_1/plan.md](docs/v5_1/plan.md) |
| docs/v6/auditoria.md | [historico/docs/v6/auditoria.md](docs/v6/auditoria.md) |
| docs/v6/bloqueos.md | [historico/docs/v6/bloqueos.md](docs/v6/bloqueos.md) |
| docs/v6/estado.md | [historico/docs/v6/estado.md](docs/v6/estado.md) |
| docs/v6/instrucciones_subagentes.md | [historico/docs/v6/instrucciones_subagentes.md](docs/v6/instrucciones_subagentes.md) |
| docs/v6/plan.md | [historico/docs/v6/plan.md](docs/v6/plan.md) |
| docs/v6/revision_final.md | [historico/docs/v6/revision_final.md](docs/v6/revision_final.md) |
| docs/v6_1/auditoria.md | [historico/docs/v6_1/auditoria.md](docs/v6_1/auditoria.md) |
| docs/v6_1/bloqueos.md | [historico/docs/v6_1/bloqueos.md](docs/v6_1/bloqueos.md) |
| docs/v6_1/carta_respuesta.md | [historico/docs/v6_1/carta_respuesta.md](docs/v6_1/carta_respuesta.md) |
| docs/v6_1/estado.md | [historico/docs/v6_1/estado.md](docs/v6_1/estado.md) |
| docs/v6_1/informe_arbitro_academico.md | [historico/docs/v6_1/informe_arbitro_academico.md](docs/v6_1/informe_arbitro_academico.md) |
| docs/v6_1/informe_arbitro_politica.md | [historico/docs/v6_1/informe_arbitro_politica.md](docs/v6_1/informe_arbitro_politica.md) |
| docs/v6_1/instrucciones_subagentes.md | [historico/docs/v6_1/instrucciones_subagentes.md](docs/v6_1/instrucciones_subagentes.md) |
| docs/v6_1/k4b_especificacion.md | [historico/docs/v6_1/k4b_especificacion.md](docs/v6_1/k4b_especificacion.md) |
| docs/v6_1/plan.md | [historico/docs/v6_1/plan.md](docs/v6_1/plan.md) |
| docs/v6_1/revision_K2.md | [historico/docs/v6_1/revision_K2.md](docs/v6_1/revision_K2.md) |
| docs/v6_1/revision_final.md | [historico/docs/v6_1/revision_final.md](docs/v6_1/revision_final.md) |
| docs/v6_1/tareas_autor.md | [historico/docs/v6_1/tareas_autor.md](docs/v6_1/tareas_autor.md) |
| docs/v6_2/bloqueos.md | [historico/docs/v6_2/bloqueos.md](docs/v6_2/bloqueos.md) |
| docs/v6_2/estado.md | [historico/docs/v6_2/estado.md](docs/v6_2/estado.md) |
| docs/v6_2/instrucciones_subagentes.md | [historico/docs/v6_2/instrucciones_subagentes.md](docs/v6_2/instrucciones_subagentes.md) |
| docs/v6_2/plan.md | [historico/docs/v6_2/plan.md](docs/v6_2/plan.md) |
| docs/v6_2/revision.md | [historico/docs/v6_2/revision.md](docs/v6_2/revision.md) |
| archive/output/v3/articulo.md | [historico/output/v3/articulo.md](output/v3/articulo.md) |
| archive/output/v3/informe_politica.md | [historico/output/v3/informe_politica.md](output/v3/informe_politica.md) |
| archive/output/v3/lo_que_sabemos.md | [historico/output/v3/lo_que_sabemos.md](output/v3/lo_que_sabemos.md) |
| archive/output/v4/policy_brief.md | [historico/output/v4/policy_brief.md](output/v4/policy_brief.md) |
| archive/output/v4/working_paper.md | [historico/output/v4/working_paper.md](output/v4/working_paper.md) |
| archive/README.md | [historico/archivo_v6_README.md](archivo_v6_README.md) |

El traslado anterior (v6.1, carpeta archive/) se documenta en [archivo_v6_README.md](archivo_v6_README.md): sus ficheros están ahora en historico/output/.
