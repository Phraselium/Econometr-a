# Puerta G0 · viabilidad por rama (decisión del orquestador, 2026-10-10)

Cobertura medida en data/processed/v2/train (sin la muestra sellada): 49 provincias de entrenamiento × 2002Q1-2024Q2.

| Rama | Datos clave en entrenamiento | N | Decisión |
|---|---|---|---|
| BA alquiler | IPC alquiler provincial 2002Q1-2024Q2; SERPAVI provincial 2011-2023 y municipal (24.809 obs.); pob. 20-34 y extranjera (interpolada intra-anual, marcada) | 4.410 prov-trim. | VIABLE. Absorbe el módulo de viviendas turísticas de BT (exploratorio) |
| BV compra | Valor tasado 49 prov. 2002-2024; hipotecas (importe) 2003+; compraventas 2007+; coste de uso aprox. 2003+ | 4.214 | VIABLE. No residentes: sin datos provinciales → solo nacional/CCAA, exploratorio |
| BI inmigración | Flujos provinciales 2008-2021 (anual, 686 obs.); padrón por agrupación de países 2002+ (cuotas base 2002) | 686 prov-año | VIABLE para Bartik/GPSS. BHJ con ~10 agrupaciones de países (pocos shocks) → limitación declarada. DML/causal forests: exploratorio |
| BO oferta y suelo | Iniciadas/terminadas libres 47 prov. 2008+; suelo 47 prov. 2004+; protegida; panel UE (31 países) | 3.008 | VIABLE |
| BT turismo/no residentes/inversores | VUT INE 2020Q3-2024Q1 (provincial 392 obs.; municipal 12.884 obs. anuales 2020-2023); sin titularidad catastral, sin AEAT, sin no residentes por provincia | — | RECORTADA: el módulo VUT pasa a BA (exploratorio); inversores y no residentes DESCARTADOS por falta de datos (docs/v2/fuentes_fallidas.md) |
| BP política | IPC alquiler provincial; tope catalán 2020Q4-2022Q1 (4 tratadas); zonas tensionadas 2024 (H6, sellado) | 49 × 90 | VIABLE. H5 en entrenamiento; H6 solo en la muestra sellada |
| BM modelos | Nacional (N=90 trimestres de entrenamiento) y paneles provinciales | — | VIABLE. Deep learning solo si supera a gradient boosting (DM-HLN) |
| BD descomposición | Salidas de BA/BV/BI/BO | — | Tras las ramas |
| BS síntesis | Todas | — | Al final |

## Orden de ejecución (máx. 3 en paralelo)
1. Infraestructura común (src/v2_common.py: carga vía holdout, bloques con embargo, AR(4) nacional y de panel, ECM v1, DM-HLN) en r2/main.
2. Ola 1: BA, BV, BI. 3. Ola 2: BO, BP, BM. 4. BD. 5. BS.
