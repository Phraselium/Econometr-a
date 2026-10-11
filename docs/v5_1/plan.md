# Plan v5.1 (ajuste fino)

| Tarea | Límite | Corte 80 % | Ejecución |
|---|---|---|---|
| T1 bajas del parque | 0,40 M | 0,32 M | subagente (econometrician) |
| T2 viviendas liberadas por envejecimiento | 0,20 M | 0,16 M | subagente, en paralelo con T1 |
| T3 rangos de necesidad y déficit | 0,12 M | 0,096 M | subagente, junto con T4, tras T1 y T2 |
| T4 dirección frente a magnitud | 0,08 M | 0,064 M | junto con T3 |
| T5 matices de lectura | 0,05 M | 0,04 M | orquestador |
| T6 backlog secundario | 0,05 M | 0,04 M | solo si sobra presupuesto |
| T7 entregables | 0,10 M | 0,08 M | subagente redactor + orquestador |
| Revisor (una vez, sobre T1-T5) | — | — | con cargo a la reserva |
| Reserva de cierre | 0,10 M | — | — |
| **Total** | **1,0 M** | **0,80 M** | — |

## Salidas e integración
- Las salidas van en output/v5_1/<T>/, con resultado.json y hechos.json en el formato estándar.
- cifras_clave.py lee también output/v5_1/*/hechos.json.
- Los entregables se regeneran en output/v5 desde las plantillas.
- check_v5 añade «liberadas nunca restadas de la necesidad» (output/v5_1/T3/control_liberadas.json).
