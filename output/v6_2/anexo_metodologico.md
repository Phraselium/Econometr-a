# Anexo metodológico: cómo reconstruir cada cifra publicada

Vivienda España, v6.2 (tarea L1). Autor: Borja Romero, economista. Fecha: 12-10-2026. Capa del anexo: C4 (documentación); no cambia ninguna capa ni ninguna cifra.

**Objetivo.** Un revisor externo debe poder reconstruir cada cifra solo con este anexo y `data/raw`, sin leer `src/`. Cuando una cifra depende de un modelo largo (clasificación A4, necesidad B1), el anexo da la **tabla intermedia mínima** y el fichero versionado del que sale.

**Comprobación automática.** `python3 src/v6_2/l1_verifica.py` sigue literalmente las fichas A1-A17. Lee `data/raw` y, solo donde la ficha lo declara, una tabla intermedia versionada. Compara con `output/v5/cifras_clave.csv` (L3: `output/v6_2/L3/hechos.json`) y escribe `output/v6_2/L1/verificacion.csv`. **Resultado: se reproducen las 15 cifras de la revisión humana y las 2 de L3** (17 de 17). De las 15, 12 se reproducen solo desde `data/raw` y 3 con tabla intermedia versionada (D1-H11, D1-H12 y B1-H1).


> **Validación (v6.2, L2).** Una segunda implementación independiente, escrita solo con este anexo y data/raw (tests/doble_impl), reproduce **15 de 15** cifras dentro del redondeo publicado. Se ejecuta en `make check`. Las precisiones que pidió se han incorporado como «Precisión añadida tras L2».

## Índice

- [0. Convenciones](#0-convenciones)
- [A. Fichas completas: las 15 cifras de la revisión humana y el déficit L3](#a-fichas-completas)
  - A1 dh_2125 · A2 terminadas_1924 · A3 deficit_2124_c1 (histórica) · A4 deficit_2124_c2 (histórica) · A5 L3-DEF-2124-SINBAJAS · A6 L3-DEF-2124-CONBAJAS
  - A7 A23-A2 · A8 A23-P2 · A9 A23-A10 · A10 R1C-001 · A11 B4-v3-vut-cantidad · A12 latente_convivencia
  - A13 B1-H4 y A14 E-B1-F · A15 B1-H1 · A16 D1-H11 y A17 D1-H12
- [B. Fichas breves: las 49 cifras de los entregables](#b-fichas-breves)
- [C. Resumen de reproducibilidad](#c-resumen-de-reproducibilidad)

## 0. Convenciones

- **Unidades.** Viviendas, hogares, %, €/m², €/mes. «pp» significa puntos porcentuales. En las cifras de alquiler, el stock (IPC, SERPAVI, IPVA de contratos existentes) y los contratos nuevos (IPVA de nuevo contrato, fianzas) se tratan siempre por separado.
- **Formato.** Español: coma decimal y punto de miles (1.013.350; 47,2 %). En las fórmulas los nombres de columna van en `código`.
- **Redondeo.** Los porcentajes se publican con 1 decimal; los recuentos, a la unidad; la latente por convivencia, a miles. El redondeo se aplica solo al final.
- **Rango y valor central.** «mín-máx» es el mínimo y el máximo de las combinaciones o fuentes declaradas en cada ficha. El valor central es el que la ficha define: punto medio, mediana o especificación base. Si la ficha no lo define, el valor queda vacío (—), como en cifras_clave.
- **Capas.** C1: hecho con ≥2 fuentes independientes. C2: cota con supuestos explícitos. C3: efecto identificado. C4: exploratorio o de fuente única. La capa de una cifra es la menor de sus componentes. Ninguna cifra de este anexo es C3 y nada en él es causal.
- **Periodos INE.** Trimestres `AAAAT1-T4`. La EPA de hogares es una media del trimestre. La ECP (tabla 60131) es el stock a 1 de enero, 1 de abril, 1 de julio y 1 de octubre (T1 = 1 de enero). El Catastro usa el ejercicio N = 1 de enero de N.
- **Ediciones y descarga.** Salen de `data/raw/_manifest.csv` (columna `descargado_utc`). Los ficheros que no figuran en el manifiesto (`pdf/`, `v4/`, `v5/`, `v3/pa_aux/`) llevan la edición en su columna `url` o en el nombre del recurso, y se citan así.
- **Cómo comprobar una cifra.** Busca la fila por `id` en `output/v5/cifras_clave.csv` (columnas `valor`, `min`, `max`, `fecha_dato`). Aplica la ficha y redondea como arriba. `l1_verifica.py` lo hace para A1-A17 con tolerancia de ±0,05 en porcentajes y de ±1 en recuentos.

---

## A. Fichas completas

### Bloques de datos comunes (se citan desde las fichas)

**H-ECP. Hogares, Encuesta Continua de Población (INE, tabla 60131).**
- Fichero: `data/raw/ine_hogares_60131.csv`, con el filtro `nombre == "Total Nacional. Total. Hogares en viviendas familiares. Número."`.
- Columnas `periodo` (AAAATn) y `valor` (hogares). Descarga: 2026-10-09T18:47Z. Cobertura: 2021T1-2026T3. Medida: stock a primer día del trimestre.
- Valores usados:

| periodo | hogares |
|---|---|
| 2021T1 | 18.539.223 |
| 2021T4 | 18.749.679 |
| 2024T4 | 19.476.488 |
| 2025T1 | 19.521.046 |

**H-EPA. Hogares, EPA (INE).**
- Fichero: `data/raw/ine_epa_hogares.csv`, con el filtro `nombre == "Hogares. Total Nacional. Ambos sexos. Total. Total."`.
- `valor` está en miles: se multiplica por 1.000. Descarga: 2026-10-09T19:19Z. Medida: media del trimestre.
- La serie tiene una ruptura metodológica en 2021T1: la variación 2020T4→2021T1 es −207.800.
- Valores usados:

| periodo | hogares |
|---|---|
| 2020T4 | 18.817.800 |
| 2021T1 | 18.610.000 |
| 2024T4 | 19.595.200 |

**T-MIV. Terminadas del Ministerio (MIVAU, Boletín Online).**
- Libres terminadas: `data/raw/mivau_v2_iniciadas_terminadas_prov.csv`, `serie == "viv_libres_terminadas_anual_nacional"` (año = 4 primeros caracteres de `periodo`). Descarga: 2026-10-10T06:02Z.
- Protegidas con calificación definitiva: `data/raw/mivau_v2_protegida.csv`, `serie == "prot_definitiva_anual_nacional"` (equivale a `nivel == "nacional"` y `tabla_codigo == 31306000`). Descarga: 2026-10-10T06:02Z.
- Territorio común (sin País Vasco ni Navarra): se restan las series `..._ccaa_pais_vasco` y `..._ccaa_navarra_comunidad_foral_de` de cada fichero.
- Parque: `data/raw/mivau_parque.csv`, `serie == "parque_total_viviendas_nacional"`, a 31 de diciembre. Descarga: 2026-10-09T18:53Z.

| magnitud | valor |
|---|---|
| Libres terminadas, suma 2021-2024 | 331.108 |
| Libres + protegidas, suma 2021-2024 | 374.573 |
| Parque, suma 2020-2023 (stock de inicio de cada año 2021-2024) | 107.057.889 |
| Bajas al 0,1 % anual (0,001 × suma del parque) | 107.058 |
| Bajas al 0,2 % anual | 214.116 |
| País Vasco + Navarra (libres + protegidas), suma 2021-2024 | 27.198 |

**T-CAT. Catastro.**
- Fichero: `data/raw/catastro_urbana_municipios.csv.gz`, con el filtro `unidad == "unidades_urbanas_residenciales"`. Se suma `valor` por `periodo` (ejercicio = 1 de enero). Descarga: 2026-10-10T06:11Z. Cobertura: régimen común.
- Altas del año y = UU(y+1) − UU(y): 2021 = 87.324; 2022 = 92.390; 2023 = 87.354; 2024 = 91.186 (suma 358.254).
- «Catastro completado» = 358.254 + 27.198 (País Vasco y Navarra según MIVAU) = 385.452.

---

### A1. dh_2125: aumento del número de hogares, 2021-2025

- **Definición.** Variación del número de hogares entre 2021 y 2025 según dos fuentes del INE.
- **Fuentes.** H-EPA y H-ECP. Fecha del dato: 2025T1 (ECP) y 2025T4 (EPA). Cobertura: España.
- **Fórmula.**
  1. EPA = media de 2025T1-T4 − media de 2021T1-T4 = **1.013.350**. Las dos medias quedan después de la ruptura, así que no hay corrección (la «EPA corregida» del rótulo coincide aquí con la EPA sin corregir).
  2. ECP = ECP(2025T1) − ECP(2021T1) = 19.521.046 − 18.539.223 = **981.823**.
  3. mín = 981.823; máx = 1.013.350; central = punto medio = **997.586,5**.
- **Armonización.** La cifra mezcla un stock a 1 de enero (ECP, 4 años exactos) con una diferencia de medias anuales (EPA). Es una diferencia de definición y queda declarada (doble implementación K4b). Si la ECP también se tomara en media anual, daría 970.670.
- **Supuestos y capa.** C1: las dos fuentes difieren un 3,1 %, dentro de ±15 %.
- **Resultado.** 997.586 (981.823-1.013.350) hogares.
- **Script.** `src/v4/m2_run.py:totales` (fila 2021-2025) → `output/v4/M2/hechos.json:M2-H0` → `src/v5/cifras_clave.py:v4_adaptadores`.
- **Reconstruible solo con anexo + data/raw: sí.** Verificado.

### A2. terminadas_1924: viviendas terminadas al año en territorio común, 2019-2024

- **Definición.** Mínimo y máximo anual 2019-2024 de las viviendas terminadas (libres + protegidas definitivas) del Ministerio, sin País Vasco ni Navarra.
- **Fuente.** T-MIV en territorio común. El Catastro (T-CAT, municipios constantes) solo valida que el dato está dentro de ±15 % y no entra en el rango (corrección R-10 de v6.1).
- **Fórmula.** Para cada año y: (libres + protegidas) nacional − (libres + protegidas) de País Vasco y Navarra. Resultado: 2019 = 72.264; 2020 = 81.496; 2021 = 87.741; 2022 = 82.361; 2023 = 82.847; 2024 = 94.426. mín = 72.264 (2019); máx = 94.426 (2024); sin valor central.
- **Capa.** C1 (MIVAU y Catastro dentro de ±15 % en 2019-2024).
- **Script.** `src/v4/m0_run.py:terminadas`, columna `comun_mivau_bruto_sin_PV_NA` → `src/v5/cifras_clave.py:v4_adaptadores`.
- **Precisión añadida tras L2.** «Si una serie protegida no tiene dato en un año, se toma 0.»
- **Reconstruible: sí.** Verificado.

### A3. deficit_2124_c1: déficit acumulado 2021-2024 sin bajas (HISTÓRICA, v6.1; sustituida en v6.2 por A5)

- **Definición.** Aumento de hogares menos viviendas terminadas en 2021-2024, sin bajas del parque.
- **Fuentes.** H-EPA, H-ECP y T-MIV (nacional, con País Vasco y Navarra).
- **Fórmula.** Hay 4 combinaciones sin bajas, dentro del universo de 12 de M0 (ver A4):
  - Hogares: «EPA corregida» = EPA(2024T4) − EPA(2020T4) + **242.400** = 777.400 + 242.400 = 1.019.800. ECP = ECP(2024T4) − ECP(2021T1) = 937.265.
  - Terminadas: con protegida 374.573; sin protegida 331.108.
  - Déficit = hogares − terminadas. mín = 937.265 − 374.573 = **562.692**; máx = 1.019.800 − 331.108 = **688.692**. Sin valor central: la mediana de M0 incluye las combinaciones con bajas.
- **Puntos detectados en la auditoría.**
  - La constante de 242.400 es un criterio de v1 (informe v1, §5.1) y no se deriva de estos datos; el salto observado es −207.800.
  - Las ventanas no coinciden: la EPA empieza en 2020T4 y la ECP en 2021T1.
  - La «segunda fuente de terminadas» es el Ministerio con y sin protegida, no el Catastro (ERRATA R-10).
- **Capa publicada.** C1. En v6.2, L3 la rebaja a C2: ver A5.
- **Resultado.** — (562.692-688.692) viviendas. Cifra histórica (v6.1), sustituida en v6.2 por L3-DEF-2124-SINBAJAS.
- **Script.** `src/v4/m0_run.py:deficit_2021_2024` → `output/v4/M0/resultado.json:deficit_2021_2024.c1_sin_bajas`.
- **Reconstruible: sí.** Verificado.

### A4. deficit_2124_c2: déficit 2021-2024 con bajas supuestas (HISTÓRICA, v6.1; sustituida en v6.2 por A6)

- **Fórmula.** 12 combinaciones: {EPA corregida, ECP} × {con protegida, sin protegida} × bajas {0; 0,1; 0,2 % anual}.
  - Bajas = tasa × suma del parque a 31 de diciembre de 2020-2023 (stock de inicio de cada año), es decir, 0, 107.058 o 214.116.
  - Déficit = hogares − (terminadas − bajas).
  - mín = 562.692 (ECP, con protegida, bajas 0); máx = 688.692 + 214.116 = **902.808**.
- **Capa.** C2: la tasa de bajas es un supuesto.
- **Resultado.** — (562.692-902.808) viviendas. Script: el de A3 (`c2_con_bajas`). Cifra histórica (v6.1), sustituida en v6.2 por L3-DEF-2124-CONBAJAS.
- **Reconstruible: sí.** Verificado.

### A5. L3-DEF-2124-SINBAJAS: déficit 2021-2024 sin bajas, todas las variantes (v6.2)

- **Definición.** Hogares − terminadas, 2021-2024, para todas las correcciones del salto de la EPA y todas las fuentes de terminadas.
- **Fuentes.** H-EPA, H-ECP, T-MIV y T-CAT. Fecha del dato: 2024T4.
- **Variantes de hogares.** Sea base = EPA(2024T4) − EPA(2020T4) = 777.400; salto = EPA(2021T1) − EPA(2020T4) = −207.800; ΔEPA(t) = EPA(t) − EPA(t−1).

| var. | fórmula | Δ hogares |
|---|---|---|
| v1 | base + 242.400 (constante de v1) | 1.019.800 |
| a | base (sin retirar el salto) | 777.400 |
| b | base − salto + media(ΔEPA 2020T4, ΔEPA 2021T2) = 777.400 + 207.800 + 56.450 | 1.041.650 |
| b4 | base − salto + media(ΔEPA 2020T3, 2020T4, 2021T2, 2021T3) = … + 52.575 | 1.037.775 |
| c | base − salto (variación 2021T1 = 0) | 985.200 |
| d1 | ECP(2024T4) − EPA(2020T4) × [ECP(2021T1)/EPA(2021T1)] (cociente 0,996197) | 730.255 |
| d2 | ECP(2024T4) − [ECP(2021T1) − media(ΔEPA 2020T1-T4) = 17.725] | 954.990 |
| e | ECP(2024T4) − ECP(2021T1) | 937.265 |

- **Terminadas.** MIVAU con protegida 374.573; MIVAU sin protegida 331.108; Catastro completado 385.452 (T-CAT).
- **Fórmula.**
  - Déficit = Δhogares − terminadas, en las 8 × 3 = 24 combinaciones.
  - mín = d1 − Catastro completado = **344.803**; máx = b − MIVAU sin protegida = **710.542**.
  - Central = punto medio = **527.672**.
- **Regla de capa** (declarada antes de ver los resultados):
  1. Amplitud = (máx − mín)/(máx + mín) = 34,7 %, mayor que el umbral del 15 %.
  2. Independencia. (i) Las variantes EPA b, b4 y c deben coincidir con la ECP (e) dentro de ±15 %. (ii) Catastro y MIVAU deben coincidir dentro de ±15 % en territorio común en 2021-2024.
  3. C1 solo si se cumplen 1 y 2. Como falla la amplitud, la capa es **C2**: una cota con dos supuestos explícitos, la corrección del salto y la fuente de terminadas.
- **Sensibilidad.** Si se quitan las variantes a y d1, que conservan el salto, el rango se estrecha, pero la capa sigue siendo C2.
- **Resultado.** 527.672 (344.803-710.542) viviendas, C2.
- **Script.** `src/v6_2/l3_deficit.py:hogares, terminadas, ventana, main` → `output/v6_2/L3/hechos.json`.
- **Precisión añadida tras L2.** «UU(año) = suma de `valor` de todas las filas de `unidades_urbanas_residenciales` con ese `periodo`, sin filtro adicional de régimen ni de municipios.»
- **Reconstruible: sí.** Verificado.

### A6. L3-DEF-2124-CONBAJAS: déficit 2021-2024 con bajas supuestas (v6.2)

- **Fórmula.** Las 24 combinaciones de A5 × bajas supuestas {0,1; 0,2 % anual} (107.058 y 214.116, como en T-MIV).
  - mín = mínimo sin bajas = 344.803.
  - máx = 710.542 + 214.116 = **924.658**.
  - Central = (344.803 + 924.658)/2 = **634.730**.
- **Bajas estimadas.** Las de v5.1 T1 (`output/v5_1/T1/tablas/deficit_con_bajas_estimadas.csv`) se calculan y se registran, pero no entran en esta cifra.
- **Capa.** C2: el supuesto de bajas no es un hecho.
- **Resultado.** 634.730 (344.803-924.658) viviendas.
- **Precisión añadida tras L2.** «Las bajas exactas son 0,002 × 107.057.889 = 214.115,8; el 214.116 es solo la cifra redondeada.»
- **Reconstruible: sí.** Verificado.

(L3-DEF-2125, C4, sigue el mismo método con fin en 2025T4 y terminadas de 2021-2025. La terminada de 2025 es C4 frágil. No se verifica aquí.)

### A7. A23-A2: alquiler de stock, variación 2015-2024 (núcleo)

- **Definición.** Rango de la variación acumulada 2015→2024 del alquiler de contratos vigentes en las fuentes que forman el «núcleo».
- **Fuentes.**
  - IPC: `data/raw/ine_ipc_alquiler.csv`, `nombre == "Nacional. Alquiler de vivienda. Índice."`, mensual; se usa la media anual (2015 = 88,022; 2024 = 97,643). Descarga: 2026-10-09T18:50Z.
  - IPVA: `data/raw/ine_v2_ipva.csv`, `nivel == "nacional"`, `medida == "IPVA_indice"`, `desglose ∈ {"Total", "Contrato existente"}` (tablas 59058 y otras). Descarga: 2026-10-10T06:53Z.
  - SERPAVI: `data/raw/pdf/serpavi_esp_agregado.csv`, `serie == "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_constante"` (edición 2026-03-09, «bd_SERPAVI_2011-2024 DEFINITIVO», según la `url`).
- **Fórmula.**
  1. Variaciones: IPC = 97,643/88,022 − 1 = 10,93 %. IPVA total = índice 2024/índice 2015 − 1 = 22,92 %. IPVA existente = índice 2024/100 − 1 = 20,64 %. SERPAVI = 8,657/6,053 − 1 = 43,03 %.
  2. Núcleo = el mayor conjunto de fuentes en el que (1 + máx)/(1 + mín) − 1 ≤ 15 %. Resulta {IPC, IPVA existente, IPVA total}; SERPAVI queda fuera y se publica aparte (A23-A2b).
  3. mín = 10,9 %; máx = 22,9 %; sin valor central.
- **Capa.** C1: ≥2 fuentes de ≥2 grupos (INE encuesta e IRPF).
- **Resultado.** — (10,9-22,9 %), 2015-2024.
- **Script.** `src/v5/a23_run.py:alquiler, nucleo, escribir`.
- **Precisión añadida tras L2.** «El IPVA `Contrato existente` (tabla 59005) tiene base 2021 = 100 y solo cubre 2021-2024; por eso se divide entre 100. El IPVA `Total` es la tabla 59058 (base 2015 = 100). Si dos subconjuntos empatan en tamaño, gana el de menor amplitud.»
- **Reconstruible: sí.** Verificado.

### A8. A23-P2: precio de compra, variación 2015-2025 (núcleo MIVAU, Notariado y Registradores)

- **Fuentes.**
  - MIVAU, valor tasado: `data/raw/mivau_valor_tasado_nacional_ccaa_prov.csv`, `serie == "valor_tasado_libre_nacional"`. Media anual de los 4 trimestres: 2015 = 1.475,2; 2025 = 2.127,6 €/m². Descarga: 2026-10-09T18:53Z.
  - Notariado: `data/raw/pdf/notariado_cgn_extranjeros_semestral.csv`, `serie == "precio_m2"`, `categoria == "Total general"`. Media de los dos semestres, solo los años con 2: 2015 = 1.324; 2025 = 1.949 €/m². Consejo General del Notariado, CIEN.
  - Registradores: `data/raw/pdf/registradores_opendata_anual.csv`, `serie == "compraventas_viv_pm2"`, `nivel == "nacional"`: 2015 = 1.462,65; 2025 = 2.283,52 €/m² (opendata, fichero `RP_ComprvResid_2007-2t2026`).
- **Fórmula.**
  1. Variaciones: MIVAU +44,22 %; Notariado +47,21 %; Registradores +56,12 %.
  2. Núcleo con tolerancia del 15 % en nivel: incluye las tres (1,5612/1,4422 = 1,083). El IPV del INE (+79,9 %, A23-P1) queda fuera.
  3. mín = 44,2 %; máx = 56,1 %; central = **mediana de las tres = 47,2 %** (Notariado).
- **Medida de precio.** Valor tasado, precio escriturado y precio registral (€/m²). Capa C1.
- **Script.** `src/v5/a23_run.py:precio`.
- **Precisión añadida tras L2.** «Los candidatos son MIVAU, Notariado y Registradores; el IPV (A23-P1) se excluye de antemano porque su amplitud respecto al resto supera el 15 %.»
- **Reconstruible: sí** (la serie de Notariado está versionada). Verificado.

### A9. A23-A10: contratos nuevos en la Comunitat Valenciana, 2021-2024

- **Fuentes.**
  - IPVA de nuevo contrato por provincia: `data/raw/ine_v2_ipva.csv`, `nivel == "provincia"`, `tabla == 59005`, `medida == "IPVA_indice"`, `desglose == "Nuevo contrato"`, territorios `Alicante/Alacant`, `Castellón/Castelló` y `Valencia/València`.
  - Pesos SERPAVI: `data/raw/pdf/serpavi_provincias.csv`, `variable == "n_contratos"`, `tipologia == "VC"`, `periodo == 2024`.
  - Fianzas GVA: `data/raw/v5/gva_fianzas_2020.csv` … `gva_fianzas_2026.csv` (separador `;`), columna `importe_fianza`, año `anyo_datos`.
- **Fórmula.**
  1. Variación del IPVA nuevo 2021→2024 por provincia: Alicante 22,18 %; Castellón 23,03 %; Valencia 28,92 %.
  2. Pesos: contratos SERPAVI de 2024, cruzados por nombre con el IPVA. Correspondencias: Alicante → Alicante/Alacant; Castellón/Castelló, igual; «Valencia/Valéncia» (grafía de SERPAVI) → Valencia/València. Alicante = 76.825; Castellón = 29.530; Valencia = 137.413. Media ponderada = **26,08 %**. Si faltara una provincia, se rellenaría con la media de la CCAA.
  3. Fianzas: se conservan los importes entre 100 y 5.000 €. Mediana por año: 2021 = 535 €; 2024 = 700 €. Variación = **30,84 %**.
  4. Núcleo (±15 % en nivel): las dos fuentes. mín = 26,1 %; máx = 30,8 %; central = media de los dos = **28,5 %**.
- **Historial.**
  - v5 (histórico): 26,6 % (22,4-30,8), con Valencia con peso 1.
  - v6.1: 27,7 % (24,6-30,8), con Valencia rellenada con la media de la CCAA.
  - v6.2: 28,5 % (26,1-30,8). L1 detectó que la grafía «Valéncia» impedía el cruce y se corrigió (ERRATA).
- **Capa.** C1. Medida: contratos nuevos (no stock).
- **Script.** `src/v5/a23_run.py:alquiler, gva_series`.
- **Precisión añadida tras L2.** «La clave de cruce es el nombre sin acentos, en minúsculas y cortado en "/" (`Valencia/Valéncia` y `Valencia/València` dan `valencia`). `devuelta` no se filtra.»
- **Reconstruible: sí.** Verificado con l1_verifica.py.

### A10. R1C-001: hogares con vivienda principal en propiedad

- **Fuentes.**
  - EFF 2022 (BdE): `data/raw/v3/eff_tenencia_edad_v3.csv`, `serie == "eff_pct_hogares_vivienda_principal|edad=total|ed=DO 2413 (EFF2022)"`, `periodo == 2022` → 72,1. Descarga: 2026-10-10T12:16Z.
  - ECV 2022 (INE 9994): `data/raw/v3/ine_ecv_tenencia_edad_v3.csv`, `serie == "ecv_pct_hogares_tenencia|Propiedad|edad_persona_referencia=Total|sexo=Ambos sexos"`, `periodo == 2022` → 75,9.
  - Censo 2021 (INE 59523, viviendas principales): `data/raw/v4/ine_v4_t59523.csv`. Cociente de `serie_nombre == "Total Nacional, En propiedad, Total (tamaño de municipio)"` (13.988.627) entre `"Total Nacional, Total (régimen de tenencia), Total (tamaño de municipio)"` (18.536.616) = 75,46.
- **Fórmula.** Central = media simple de las tres = **74,5**; mín = 72,1; máx = 75,9.
- **Capa.** C1: tres fuentes en un rango de 5 pp. Fecha del dato: 2021-11 (Censo) y 2022.
- **Script.** `src/v5/r1c_run.py` (bloque «Parque total»); el Censo sale de `src/v4/m4_run.py` → `tenencia_censo2021.csv`.
- **Reconstruible: sí.** Verificado.

### A11. B4-v3-vut-cantidad: máximo de stock de alquiler desplazado por viviendas turísticas

- **Definición.** Cota superior de cantidad: si cada vivienda turística nueva sustituyera 1:1 a una de alquiler, ¿qué parte del stock de alquiler desaparecería?
- **Fuentes.**
  - Viviendas turísticas (INE, estadística experimental, tablas 39363/39364): `data/raw/ine_v2_vut.csv`, `nivel == "nacional"`, `medida == "viviendas_turisticas"`. 2020M08 = 321.496; 2024M08 = 403.267; ΔVUT = 81.771. Descarga: 2026-10-10T06:52Z.
  - Stock de alquiler, opción 1, Censo 2021: `data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz`, `serie == "t20_2"` (viviendas principales en alquiler), suma de secciones = 2.978.087.
  - Stock de alquiler, opción 2, ECV × ECP: (alquiler a precio de mercado + inferior al de mercado, ECV 2021 = 18,0 %) × H-ECP 2021T4 (18.749.679) = 3.374.942.
- **Fórmula.** Cota = 100 × ΔVUT / stock: Censo **2,746 %**; ECV × ECP 2,423 %. Valor = Censo (especificación principal); mín = 2,423; máx = 2,746.
- **Supuestos y capa.** Sustitución 1:1 y traspaso completo; stock constante. C2 (cota de Manski). No es un efecto.
- **Script.** `src/v3/pb_run.py:b1` (cota `B1-nac-cantidad` en `output/v3/PB/cotas.json`) → `src/v5/b4_run.py`. (La revisión humana cita `b2`; la tabla real es `b1_nacional_sensibilidad.csv`.)
- **Precisión añadida tras L2.** `ecv_pct_hogares_tenencia|Alquiler a precio de mercado|edad_persona_referencia=Total|sexo=Ambos sexos` y `…|Alquiler inferior al precio de mercado|…` en `data/raw/v3/ine_ecv_tenencia_edad_v3.csv`, `periodo == 2021` (15,2 + 2,8).
- **Reconstruible: sí.** Verificado.

### A12. latente_convivencia: demanda latente de jóvenes por convivencia con los padres

- **Definición.** Hogares adicionales si la tasa de convivencia con los padres de las personas de 25-34 años volviera al nivel de 2008.
- **Fuentes.**
  - Eurostat ilc_lvps08 (ECV): `data/raw/v3/eurostat_emancipacion_tenencia_v3.csv`, `fuente` contiene «lvps08», `serie` contiene «Y25-34_T_con_padres», `codigo == "ES"`. 2008 = 36,6 %; 2025 = 50,2 %. Descarga: 2026-10-10T12:03Z.
  - EPA (INE tabla 65944): `data/raw/v3/pa_aux/ine_t65944.json`, `Nombre` que case con «Total Nacional. Ambos sexos. De (25 a 29|30 a 34) años. (Total|Hijo/a). Personas». Tasa = hijos/total de 25-34: 2008 = 33,61 %; 2025 = 40,35 %. Población de 25-34 en 2025 = 5.579.800 personas (miles × 1.000).
- **Fórmula.** Latente = (tasa 2025 − tasa 2008)/100 × 5.579.800 / personas por hogar joven, con 2 fuentes × {1,5; 2,0} = 4 escenarios: 505.902; 379.426; 250.607; 187.956. mín = 188.000; máx = 506.000 (redondeo a miles); sin valor central.
- **Supuestos y capa.** La tasa de 2008 es el contrafactual; 1,5-2 personas por hogar joven. C2.
- **Script.** `src/v3/pa_a23.py:a2` (serie) → `src/v4/m1_run.py:latente` → `output/v4/M2/hechos.json:M2-C1` (texto «188-506 mil») → `src/v5/cifras_clave.py`.
- **Precisión añadida tras L2.** «En `ine_t65944.json` cada serie tiene un dato por año (`Anyo`, `FK_Periodo` 28); se suman los dos tramos de edad (25-29 y 30-34) por separado para Total e Hijo/a. Los extremos se redondean con `round(x, -3)`.»
- **Reconstruible: sí.** Verificado.

### A13-A14. B1-H4 y E-B1-F: crecimiento de hogares proyectado, 2026-2035

- **Fuentes.**
  - INE Proyección de Hogares, tabla 54562 (modificada el 17-06-2026; base 1-1-2026): `data/raw/v5/ine_b1_t54562_proy_hogares.csv`, filas con `nombre` acabado en ". Total. ".
  - INE Proyecciones de Población, tabla 36726 (corto plazo): `data/raw/v5/ine_b1_t36726_proy_poblacion_prov.csv`, filas «Total. Población. <territorio>. Proyección a corto plazo. Todas las edades. ».
- **Armonización territorial.**
  - Clave = nombre en minúsculas, sin acentos, cortado en «/» y «,», y sin caracteres no alfabéticos («Balears, Illes» → `balears`).
  - Se conserva la primera fila por clave y año, y se toman las 52 provincias (la lista de nombres está en `output/v5/A4/clasificacion_provincias.csv`, columna `provincia`).
- **Fórmula.**
  - Por provincia: F_ine = H(2036) − H(2026); F_alt = H(2026) × [P(2036)/P(2026) − 1] (jefatura constante de 2026).
  - Central = Σ F_ine = **1.720.537**. Coincide con el total nacional H(2036) − H(2026).
  - mín = Σ min(F_ine, F_alt) = **1.308.531**; máx = Σ max(F_ine, F_alt) = **1.772.410**.
- **Capa.** C2 (proyección con supuesto de jefatura). Periodo: de 1-1-2026 a 1-1-2036.
- **Script.** `src/v5/b1_run.py:lee_proy_hogares, lee_proy_pob, main` (F_*) → `output/v5/B1/hechos.json:B1-H4` → `src/v5/e_hechos_e2.py` (E-B1-F).
- **Precisión añadida tras L2.** «Las colisiones de clave (Navarra, Madrid, Asturias, Murcia, La Rioja: fila de CCAA y de provincia) se resuelven con la primera fila del fichero; ambas son idénticas. La lista de 52 claves sale de aplicar la clave a `clasificacion_provincias.csv:provincia`.»
- **Reconstruible: sí.** Verificado. El intento de K4b falló porque excluía las provincias uniprovinciales.

### A15. B1-H1: necesidad total de vivienda por año, 2026-2035 (versión v5)

- **Definición.** N10 = A + R + V + F − M − K (10 años), suma de 52 provincias, dividida entre 10.
  - El rango combina extremos: mín = A, R, V y F en su mínimo, menos M y K en su máximo; máx, al revés.
  - Las viviendas liberadas por envejecimiento (L) **no** se restan (regla v5.1).
- **Tabla intermedia versionada.** `output/v5/B1/tablas/B1_nacional.csv` (suma provincial de `B1_provincias.csv`):

| comp. | mín | central | máx | definición resumida |
|---|---|---|---|---|
| A | 830.962,6 | 1.103.170,4 | 1.473.641,4 | A1 (déficit 2021-2025 de A4, mín/mediana/máx, recortado a ≥0) + A2 (latente de M1 repartida por población de 20-34) |
| R | 1.070,3 | 89.664,7 | 178.259,0 | 10 × tasa de bajas (Censo 2011-2021 + MIVAU y Catastro + MIVAU; mín/media/máx) × viviendas del Censo 2021 |
| V | 0 | 58.674 | 117.348 | vacancia friccional {0; 2; 4 %} × viviendas en alquiler de 2021, solo en las provincias de las clases A4 1-2 |
| F | 1.308.531,1 | 1.720.537,0 | 1.772.410,4 | A13 |
| M | 366.776,6 | 733.553,2 | 1.100.329,8 | {10; 20; 30 %} de las vacías de 2021 (INE 59531), solo en las clases A4 1-2 |
| K | 75.674 | 89.815 | 103.956 | cartera: iniciadas − terminadas (MIVAU), a 2 y 3 años; central = media |

- **Fórmula.**
  - Central = (1.103.170,4 + 89.664,7 + 58.674 + 1.720.537 − 733.553,2 − 89.815)/10 = **214.867,8**.
  - mín = (830.962,6 + 1.070,3 + 0 + 1.308.531,1 − 1.100.329,8 − 103.956)/10 = 93.627,8.
  - máx = 309.920,8.
- **Capa.** C4. Nota: el informe vigente cita la versión v5.1 (T3-H5b = 210.424), con las bajas estimadas de T1; esta ficha documenta la de cifras_clave (v5).
- **Script.** `src/v5/b1_run.py:main, escribe_json`.
- **Precisión añadida tras L2.** «Las columnas de `B1_nacional.csv` son `componente,min,central,max`; la fila `N10` de esa tabla incluye L y no se usa.»
- **Reconstruible: con tabla intermedia versionada.** Verificado. Cada componente sigue hasta `data/raw` en `B1_provincias.csv` (columnas `*_min/central/max`).

### A16-A17. D1-H11 y D1-H12: parte de una ayuda general que se traslada al precio, clases A4 1 y 2 (método A)

- **Fórmula de incidencia.** Parte al precio = |εd| / (εs + |εd|), con la rejilla |εd| ∈ {0,3; 0,6; 1,0; 1,5} (P-D v3).
- **εs por clase.** Es la «respuesta de oferta» A4 de las provincias de la clase, recortada a ≥0: lo = percentil 25, central = mediana, hi = percentil 75.
- **Rango y central.** mín y máx sobre las 12 combinaciones (3 εs × 4 εd). Central = mediana sobre las 4 εd con la εs central.
- **Respuesta de oferta** (reconstruible desde raw):
  - Por provincia: media de las libres terminadas de 2021-2025 / media de 2016-2020 − 1.
  - Fuente: `data/raw/mivau_v2_iniciadas_terminadas_prov.csv`, `serie` empieza por «viv_libres_terminadas_anual», `nivel == "provincia"`; si no hay provincia, se toma la CCAA uniprovincial o la ciudad autónoma.
- **Clase A4** (modelo largo: falta de vivienda, brecha precio-coste y regulación; parámetros centrales m = 0,20, r = 1,25, e = 1,2, u = 0,10). Tabla intermedia `output/v5/A4/clasificacion_provincias.csv`, columnas `provincia`, `resp_oferta`, `clase_2021_2025`:
  - **Clase 1 (37 provincias), resp_oferta:**
    - Álava 0,480; Albacete 0,253; Almería 0,643; Baleares 0,420; Barcelona 0,293; Burgos 0,535; Cáceres 0,885; Cádiz 0,565;
    - Castellón 0,813; Córdoba 0,119; A Coruña 0,525; Cuenca 0,111; Girona 0,290; Granada 0,717; Guadalajara 1,112; Huelva 0,455;
    - Huesca 0,334; León 0,415; Lleida 0,156; La Rioja 0,450; Madrid 0,269; Málaga 0,705; Murcia 1,455; Navarra 0,759;
    - Asturias 0,780; Palencia 0,841; Las Palmas 1,590; Pontevedra 0,548; Salamanca 0,176; Cantabria 0,756; Sevilla 0,919; Soria 0,638;
    - Tarragona 0,689; Toledo 0,511; Valencia 0,957; Valladolid 1,485; Zaragoza 0,167.
  - **Clase 2 (11 provincias):** Alicante −0,036; Ávila −0,001; Badajoz −0,225; Gipuzkoa −0,187; Lugo −0,355; Ourense −0,145; Santa Cruz de Tenerife 0,027; Segovia 0,098; Teruel 0,089; Bizkaia 0,022; Zamora 0,054.
- **Cálculo.**
  - Clase 1: εs = 0,334 / 0,548 / 0,780. mín = 0,3/(0,780 + 0,3) = 27,8 %; máx = 1,5/(0,334 + 1,5) = 81,8 %; central = mediana de {35,4; 52,3; 64,6; 73,2} = **58,4 %**.
  - Clase 2: los valores negativos se recortan a 0, así que εs = 0 / 0 / 0,041. mín = 0,3/0,341 = 88,1 %; máx = central = **100 %**.
- **Capa.** C4. Es una cota superior para una ayuda focalizada y no hay lenguaje causal.
- **Script.** `src/v5/d1_run.py:es_por_clase, incidencia_clase, main`; la clase sale de `src/v5/a4_run.py:clasificar, respuesta_oferta`.
- **Precisión añadida tras L2.** «Los percentiles son interpolación lineal (numpy por defecto). La clase es la columna `clase_2021_2025`. D1-H11 = clase 1; D1-H12 = clase 2.»
- **Reconstruible: con tabla intermedia versionada** (lista de provincias por clase). Verificado.

---

## B. Fichas breves

Formato de cada ficha: fuente y filtro · fórmula · script → salida · reconstruible. Valores tal como figuran en `output/v5/cifras_clave.csv`.

**Aviso.** Las fichas B no las recalcula `l1_verifica.py`. Fuentes y filtros salen de una lectura dirigida del código citado; los detalles que no se comprobaron línea a línea remiten a la función indicada. «Sí» significa que el cálculo solo usa `data/raw`, no que se haya verificado aquí.

### B1. Módulo A23: precios y alquiler (`src/v5/a23_run.py`)
- **A23-P1** (79,9 %, 2015-2025, C4). IPV del INE (tablas 25171 y 80270: `data/raw/ine_ipv_25171.csv` y `ine_ipv_80270.csv`, índice general nacional enlazado). Media anual de los 4 trimestres, 2025/2015 − 1. Función `precio` (`anual_trim(nac,"ipv")`; el enlace de bases se hace en el panel `nacional_q_v2`). **Reconstruible: con tabla intermedia** (`output/v5/A23/tablas/idx_precio_publicado_2015.csv`).
- **A23-A9** (16,9 %; 16,6-17,2, Cataluña 2021-2024, C1). IPVA nuevo contrato de las 4 provincias catalanas, ponderado con contratos SERPAVI 2024 (relleno con la media de la CCAA). Incasòl: renta media de los contratos depositados del año completo, `data/raw/v3/incasol_fianzas_municipio_v3.csv.gz`, `periodo == "<año> gener-desembre"`, media ponderada por contratos. Núcleo ±15 %; central = media de los dos. **Reconstruible: sí** (mismo método que A9).

### B2. Módulo A4: concentración (`src/v5/a4_run.py`)
- **A4-conc50-2021-2025** (6 provincias, C4). Número mínimo de provincias, ordenadas por déficit positivo 2021-2025 (`deficit_2021_2025_mediana` de `clasificacion_provincias.csv`), cuya suma alcanza el 50 % del déficit positivo total. **Con tabla intermedia** (`output/v5/A4/tablas/A4_concentracion.csv`).

### B3. Módulo B1: componentes de la necesidad (`src/v5/b1_run.py`; tabla de A15)
- **B1-H3** (R: 89.664,7; 1.070,3-178.259). **B1-H6** (M: 733.553,2; 366.776,6-1.100.329,8). **E-B1-A1** (A1: 788.153,5; 643.007-967.739,5) y **E-B1-A2** (A2: 315.016,9; 187.955,6-505.901,9; la latente de A12 sin redondear). Filas de `B1_nacional.csv`. **Con tabla intermedia.**
- **E-B1-anual-Alicante / Castellon / Valencia** (14.264; 4.267; 16.993 viviendas/año). Columna `N_anual_{min,central,max}` de la fila provincial de `output/v5/B1/tablas/B1_provincias.csv`; misma fórmula A + R + V + F − M − K. Script `src/v5/e_hechos_e2.py`. **Con tabla intermedia.**

### B4. Módulo CA: crédito, contado y comparación europea (`src/v5/ca_run.py`)
- **CA-CR-saldo-2025 / CA-CR-saldo-pico** (97,572 y 471,807 miles de millones de €; pico 2008Q3). BdE be0418: `data/raw/v5/ca_bde_be0418_credito_actividad.csv`, series `D_MEE61010` (construcción) + `D_MEE61013` (actividades inmobiliarias), meses 3, 6, 9 y 12, entre 2005Q1 y 2025Q4. Último valor y máximo, ÷1.000. Función `credito`. **Sí.**
- **CA-CT-ratio-ine** (70,05 hipotecas por 100 compraventas, 2025). Hipotecas: `data/raw/ine_v2_hipotecas_prov.csv`, `nivel == "nacional"`, `medida == "hipotecas_viviendas_numero"`, años con 12 meses. Compraventas: `data/raw/ine_etdp_compraventas.csv`, `serie == "ETDP1826"`, años con 12 meses. Ratio = 100 × hipotecas/compraventas. El rango 63,9-159,8 es el mínimo y el máximo del ratio en 2007-2025. **Sí.**
- **CA-CT-contado-cota** (29,95 %). Cota inferior del pago al contado = 100 × (1 − φ × ratio) con φ = 1 (todas las hipotecas, de compra). Función `contado`. C4 (supuesto sobre φ). **Sí.**
- **CA-EU-hpi_real-crecimiento** (42,6 %; P25-P75 UE-27: 16,87-60,91), **CA-EU-alq_real-crecimiento** (−10,3 %; −8,57-9,34) y **CA-EU-emancipacion-nivel** (30,2 años; 23,95-28,35).
  - Fuentes Eurostat en `data/raw/v5/ca_eurostat_*.csv` y `data/raw/eu_hpi.csv`, `eu_hicp_rent.csv`, `eu_hicp.csv`; la emancipación es yth_demo_030 con `sex == "T"`.
  - Precio y alquiler reales = índice nominal / IPCA, 2015 = 100; crecimiento = índice del último año/2015 − 1.
  - Valor = España en el último año con ≥20 países. min/max = **P25 y P75 de la UE-27** de ese año (no el rango de España).
  - Función `europa`. **Sí** (los ficheros exactos de cada indicador están en la lista `IND` de `europa`).

### B5. Módulo CC: sobrecarga y tenencia joven (`src/v5/cc_run.py`)
- **CC-C7a-ten-OWN_L** (3,4 %; 2015 = 8,7) y **CC-C7a-ten-RENT_MKT** (26,8 %; 2015 = 43,3). Eurostat ilc_lvho07c: `data/raw/v5/cc_eurostat_ilc_lvho07c.csv`, `geo == ES`, tenencia OWN_L o RENT_MKT, total de edades. Valor = 2025; el rango es el min-max entre 2015 y 2025. Fuente única (ECV) → C4. **Sí.**
- **CC-C7b-jov-prop** (30,6 %; 2015 = 34,2). ECV 9994: `data/raw/v3/ine_ecv_tenencia_edad_v3.csv`, `serie == "ecv_pct_hogares_tenencia|Propiedad|edad_persona_referencia=De 16 a 29 años|sexo=Ambos sexos"`. Valor = 2025; «min» = 2015, rotulado así en el periodo (hallazgo abierto K4a-04: min/max con otro sentido). **Sí.**

### B6. Módulos D1, D2 y D3 (`src/v5/d1_run.py`, `d2_run.py`, `d3_run.py`)
- **D1-H13** (clase 3: 76,4 %; 50,1-89,8). Método de A16 con las 2 provincias de clase 3 (Ciudad Real 0,363; Jaén 0,107): εs = 0,171 / 0,235 / 0,299. **Con tabla intermedia.**
- **D2-H11** (29,1 %; 11,6-46,5). Cobertura de la necesidad de clase 1 por +25.000 a +100.000 viviendas al año adicionales (P-D v3), repartidas por cuota provincial: 100 × construcción adicional asignada / necesidad B1 de la clase. **Con tabla intermedia** (`output/v5/D2/`).
- **D3-coincide / comparable_en_parte / difiere** (2, 6 y 1 referencias). Recuento de la clasificación manual de 9 referencias de organismos frente a las cifras propias (`output/v5/D3/`). **No reconstruible desde raw:** es un juicio documentado, no un cálculo.

### B7. Módulo E: hechos derivados (`src/v5/e_hechos_e1.py`, `e_hechos_t7.py`, `e_hechos_v6.py`)
- **E-E1-D2-covvac-1** (30,23 %). M central (vacías movilizables) / N10 central de la clase A4 1, a partir de `B1_provincias.csv`. **Con tabla intermedia.**
- **E-T7-prod** (78.810-100.980/año, 2019-2024, C1). T-MIV nacional con País Vasco y Navarra (libres + protegidas), mínimo y máximo anual. **Sí.**
- **E-T7-demol-2024** (0,022-0,036 % del parque). Viviendas con licencia de demolición de 2024 (MIVAU, licencias municipales; definición estrecha y amplia) / parque de 2024 (T-MIV). **Con tabla intermedia** (`output/v5_1/T1/tablas/licencias_demolicion_nacional.csv`, fila 2024, producida por `src/v5_1/t1_run.py`).
- **E-T7-lib-capital / E-T7-lib-resto** (619.768 y 1.099.268). Viviendas liberadas por envejecimiento de T2 (v5.1) repartidas entre capitales y resto de municipios con el Censo 2021. **Con tabla intermedia** (`output/v5_1/T2/`). Nunca se restan de la necesidad.
- **E-V6-M1B-GSADF-TOT** (11 CCAA). Recuento de CCAA con serie suficiente para el contraste GSADF (2015T1-2024T4; valor tasado e IPC de alquiler). **Con tabla intermedia** (`output/v6/M1B/`).

### B8. Validación sellada y modelos K (`src/v6_1/k1_run.py`, `k2_salidas.py`; `src/v6/m4_run.py`)
- **K1-N-TAREAS** (9) y **K1-N-MEJOR** (6). Recuento sobre `output/v6_1/K1/tabla_modelos_k1.csv`: tareas comparadas, y tareas en que el mejor modelo supera a la base más exigente (DM-HLN y permutación, Holm). **No reconstruible solo con raw:** depende de la validación sellada (`data/sealed`, que solo se abre con `src/holdout.py`).
- **V6-M4-RMSE-alq_provincia** (1,607) y **V6-M4-PERS-alq_provincia** (4,21). RMSE espacial sellado (11 provincias) del mejor modelo y de la persistencia; alquiler de stock SERPAVI, log-puntos × 100. **No reconstruible** (holdout sellado; una evaluación por modelo).
- **K2-CUOTA-COMPRA-SIN / -SINPOB-EXT / -SINPOB-SIN** (−1,308; 1,6; 4,264 % por +1 pp de cuota de extranjeros en t−1). Efectos fijos dobles sobre el panel provincial `output/v6/M0/paneles/prov_compra_anual`, con y sin controles. Corrección de Holm en `output/v6_1/K2/registro_holm.csv`. C4, asociación. **Con tabla intermedia** (panel versionado).

### B9. Módulo R1A: compradores e inventario turístico (`src/v5/r1a_run.py`)
- **R1A-H1 / R1A-H2** (6,83 % en 2025; 9,86 % en 2015). MIVAU Boletín, tabla 1.6: `data/raw/mivau_transacciones_residencia.csv` (función de lectura en `r1a_run.py`, línea 57), transacciones de extranjeros no residentes / total de transacciones de vivienda, nacional y anual. **Sí.**
- **R1A-H6** (1,56; 1,41-1,75 veces). Viviendas del Registre de Turisme de la GVA (`data/raw/gva_vut_municipio.csv.gz`, stock a 2024-11) / VUT del INE (`ine_v2_vut.csv`, 3 provincias valencianas). Rango entre provincias. **Sí.**

### B10. Módulos v5.1 T2, T3 y T4 (`src/v5_1/t2_run.py`, `t3_run.py`, `t4_run.py`)
- **T2-H1 / T2-H6** (1.856.430,5 acumuladas; 150.078,8 al año). Liberadas por fallecimiento del último miembro y traslado a residencia: hogares unipersonales y de 2 personas de 65+ (54562) × mortalidad (67235) × tasa de residencia; fracción al mercado según ECV y ETDP. Rejilla en `output/v5_1/T2/`. **Con tabla intermedia.**
- **T3-H2** (653.097; 562.692-744.144). Déficit 2021-2024 con bajas **estimadas** de T1: 4 fuentes de hogares y terminadas × tasa {0; central; máx} de `output/v5_1/T1/tablas/deficit_con_bajas_estimadas.csv`. **Con tabla intermedia.** Usa el universo histórico de A3; ver la sustitución L3.
- **T3-H5b** (210.424,4; 99.388,2-292.082,8) y **T3-H5** (245.988,6; con la sensibilidad X). Misma fórmula que A15 con R de T1 (bajas estimadas); H5 añade X. **Con tabla intermedia** (`output/v5_1/T3/`).
- **T3-H9** (2,7; 1,4-3,8 veces). Necesidad T3-H5b (central, mín y máx) / media de E-T7-prod en 2019-2024. **Con tabla intermedia.**
- **T4-H2 / T4-H3** (585.609; 87.247-946.852 viviendas; 15 provincias empeoran). Proyección del déficit 2025→2030 en la rejilla B2 × T1 × T2 con 54562 y MIVAU. **Con tabla intermedia** (`output/v5_1/T4/`).

## C. Resumen de reproducibilidad

| id | reconstruible solo con anexo + data/raw | verificado por l1_verifica |
|---|---|---|
| dh_2125, terminadas_1924, deficit_2124_c1*, deficit_2124_c2*, A23-A2, A23-P2, A23-A10, R1C-001, B4-v3-vut-cantidad, latente_convivencia, B1-H4, E-B1-F | sí | sí (12) |
| L3-DEF-2124-SINBAJAS, L3-DEF-2124-CONBAJAS | sí | sí (2) |
| B1-H1, D1-H11, D1-H12 | con tabla intermedia versionada | sí (3) |

\* Históricas (v6.1), sustituidas en v6.2 por las cifras L3.

Hallazgo de L1 (A9), corregido en v6.2: el peso SERPAVI de Valencia no cruzaba por la grafía «Valéncia». A23-A10 pasa a 28,5 % (26,1-30,8). Ver ERRATA.md.
