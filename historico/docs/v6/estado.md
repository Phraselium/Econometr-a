# Estado v6

| Tarea | Estado | Capa | Resultado principal | Tokens subagentes |
|---|---|---|---|---|
| Setup y sellado v6 en holdout.py | hecho | — | 11 provincias selladas: 07, 22, 26, 28, 30, 31, 33, 35, 38, 44, 50 + último año | 0 |

| G auditoría del repositorio | hecho | — | README y MAPA; 5 entregables de v3 y v4 pasan a archive/; Makefile completo (a5_validacion, b3_potencia); versión 5.1 en CITATION; rutas locales quitadas; tareas del autor | 139.890 |
| M0 datos, paneles, diccionario, hipótesis y potencia | hecho (pendiente de revisión) | — | 6 paneles de entrenamiento sellados (provincia anual y trimestral, municipio, distrito); 41 provincias de entrenamiento en compra; potencia baja con N<400 | 233.039 |
| Revisión M0 | REHACER (B1-B5) → corregido; APROBADA | — | docs/v6/revision_M0.md; prereg-v6 | 79.293 + 44.476 (corrección) |
| M2 incertidumbre de modelo | hecho | C4 | BMA, PDS y multiverso; población pesa en ambos mercados; renta y extranjeros pesan en compra y no en alquiler; oferta (iniciadas) pesa en alquiler y no en precio; contratos nuevos sin N | 63.186 |
| M1a econometría del alquiler | hecho | C4 | ninguna variable sobrevive a Holm en la especificación pre-registrada; sin VUT, población p=0,026 (+5 €/mes por 10.000 hab.) pero los métodos discrepan; VUT −1,6 €/mes por 1.000 (no concluyente); topes: pretendencias rechazadas; contratos nuevos descriptivos | 121.862 |
| M1b econometría de la compra y relación entre mercados | hecho | C4 | ninguna confirmatoria sobrevive a Holm; elasticidad precio-alquiler 0,4-2,1 según la especificación (asociación); ratio P/A 20,3 → 17,1 años (2015-2023); sin exuberancia en 11 CCAA; fuera de muestra el ADL no bate a AR(4) | 140.295 |
| M3a predicción y ML del alquiler | hecho | C4 (interpretación) | validación interna: RF/GB baten a AR y persistencia en los tres niveles; frente a ECM v1, solo en municipio; MLP y GraphSAGE no superan a GB (negativo); BART no disponible; jerárquico con MixedLM | 120.059 |
| M3b predicción y ML de la compra | hecho | C4 (interpretación) | precio trimestral: ML 1,93 % frente a AR(4) 3,55 % (DM p=0,0007), pero la persistencia da 1,91 % y el ML no la bate; volumen: persistencia ≈ ML; DL municipal no bate a GB (negativo); BART y PyMC sustituidos | 112.530 |
| M4 evaluación sellada y síntesis | hecho | C4 | 53 aperturas (una por modelo); mejor modelo: GB/RF en alquiler (provincia 1,61 frente a 4,21 de la persistencia), bosque en precio provincial (2,48) y trimestral (1,61), ECM v1 en precio municipal y Registradores; ninguna variable «relevante con seguridad» | 186.120 |
| Entregables v6 | hecho | — | informe técnico §11, WP §4.5 y §5.5, lo que sabemos, brief, una página, CHANGELOG v6.0, verificador | 182.300 |
| Revisión final | APROBAR (16 no bloqueantes; prioritarios corregidos) | — | docs/v6/revision_final.md | 118.697 |

**Hecho:** setup, G, M0-M4, entregables, revisión final.
**Siguiente:** v6 CERRADA. Tareas del autor en docs/v6/tareas_autor.md.
**Tokens de subagentes v6:** 1.541.747 / 2.200.000 (corte 1.760.000; reserva 220.000).
