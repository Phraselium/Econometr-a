# F5: atribucion y «factor mas relevante»

svar_hd: C3s, condicionado a los supuestos de signo y de cero de M2 (V3: solo impacto; magnitudes posiblemente atenuadas, Y6). El resto de metodos son C4 (asociacion): sin lectura causal.

## Designaciones (regla §9 fijada)

| Mercado | Periodo | Votos (svar_hd/dom/lpiv/contab) | Evaluado | Cond.1 | Cond.2 | Cond.3 | Resultado |
|---|---|---|---|---|---|---|---|
| compra | P1 | empleo_renta/abstiene/abstiene/abstiene | empleo_renta (1) | no | si | si | no designado |
| compra | P2 | empleo_renta/factor_europeo/abstiene/abstiene | empleo_renta (1) | no | no | no | no designado |
| compra | P3 | empleo_renta/empleo_renta/abstiene/demografia | empleo_renta (2) | no | si | no | no designado |
| compra | P4 | empleo_renta/credito_tipos/credito_tipos/abstiene | credito_tipos (2) | no | no | no | no designado |
| compra | P5 | credito_tipos/credito_tipos/abstiene/demografia | credito_tipos (2) | no | no | no | no designado |
| alquiler | P1 | abstiene/factor_europeo/abstiene/abstiene | factor_europeo (1) | no | no | no | no designado |
| alquiler | P2 | empleo_renta/empleo_renta/abstiene/abstiene | empleo_renta (2) | no | no | no | no designado |
| alquiler | P3 | demografia/demanda_externa/abstiene/abstiene | demografia (1) | no | no | no | no designado |
| alquiler | P4 | demanda_vivienda/credito_tipos/abstiene/abstiene | demanda_vivienda (1) | no | no | no | no designado |
| alquiler | P5 | credito_tipos/credito_tipos/abstiene/abstiene | credito_tipos (2) | no | no | no | no designado |

Designados: 0 de 10 celdas.

## Tabla comun fuera de muestra (J7; RMSE en pp de crecimiento trimestral real; prueba 2016T2-2026T1)

| mercado   | modelo   |   rmse_pp | evaluable   |   p_holm_vs_ar4 |   p_holm_vs_exigente | mejor_que_exigente   |
|:----------|:---------|----------:|:------------|----------------:|---------------------:|:---------------------|
| compra    | ar4      |    1.1757 | si          |        nan      |             nan      | False                |
| compra    | ecm_v1   |    2.617  | si          |          0.0123 |               0.0123 | False                |
| compra    | ar_fc    |    1.2735 | si          |          0.1315 |               0.1315 | False                |
| compra    | bvar_m2  |    1.3736 | si          |          0.1315 |               0.1315 | False                |
| alquiler  | ar4      |    0.8034 | si          |        nan      |             nan      | False                |
| alquiler  | ecm_v1   |    1.6915 | si          |          0.0005 |               0.0005 | False                |
| alquiler  | ar_fc    |    0.8318 | si          |          0.5955 |               0.5955 | False                |
| alquiler  | bvar_m2  |    0.9759 | si          |          0.1266 |               0.1266 | False                |

Ver regla_s9.csv, ranking.csv, regional_ranking.csv, atribucion_combinada.csv y fichas.md.