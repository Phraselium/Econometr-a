# Eventos de política de vivienda (v2)

Generado por `src/build_eventos.py` (no editar a mano). CSV: `data/raw/v2_eventos_politica.csv` (eventos) y `data/raw/v2_zonas_tensionadas.csv` (un municipio o ámbito por fila, con código INE de municipio, fecha de la declaración autonómica y fecha de efecto estatal).

Fechas tomadas del XML oficial del BOE (`diario_boe/xml.php`) y contrastadas con la página pública (el `<title>` contiene el título de la norma). Estado VERIFICADO = título, fecha de publicación, vigencia/derogación coinciden con la fuente oficial. NO VERIFICADO = sin fecha ni URL oficial.

## Eventos

| id | evento | norma | publicación | vigor | fin | ámbito | mercado | estado | URL oficial |
|---|---|---|---|---|---|---|---|---|---|
| E01 | Ley 4/2013 de flexibilización y fomento del alquiler (LAU 2013) | Ley 4/2013, de 4 de junio | 2013-06-05 | 2013-06-06 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2013-5941 |
| E02 | RDL 7/2019 medidas urgentes en vivienda y alquiler | Real Decreto-ley 7/2019, de 1 de marzo | 2019-03-05 | 2019-03-06 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2019-3108 |
| E03 | Ley 5/2019 reguladora de los contratos de crédito inmobiliario | Ley 5/2019, de 15 de marzo | 2019-03-16 | 2019-06-16 |  | nacional (ES) | compra | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2019-3814 |
| E04 | RDL 8/2020 (COVID): moratoria hipotecaria vivienda habitual | Real Decreto-ley 8/2020, de 17 de marzo | 2020-03-18 | 2020-03-18 |  | nacional (ES) | compra | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2020-3824 |
| E05 | RDL 11/2020 (COVID): moratoria de alquiler y suspensión de desahucios | Real Decreto-ley 11/2020, de 31 de marzo | 2020-04-01 | 2020-04-02 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2020-4208 |
| E06 | RDL 37/2020: vulnerabilidad en vivienda (desahucios durante el estado de alarma) | Real Decreto-ley 37/2020, de 22 de diciembre | 2020-12-23 | 2020-12-23 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2020-16824 |
| E07 | RDL 16/2025: prórroga de la suspensión de desahucios hasta 31-12-2026 (derogado) | Real Decreto-ley 16/2025, de 23 de diciembre | 2025-12-24 | 2025-12-25 | 2026-01-28 | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-26458 |
| E08 | RDL 2/2026: nueva prórroga de la suspensión de desahucios (derogado) | Real Decreto-ley 2/2026, de 3 de febrero | 2026-02-04 | 2026-02-05 | 2026-02-28 | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-2547 |
| E09 | Ley catalana 11/2020 de contención de rentas | Ley 11/2020 del Parlamento de Cataluña, de 18 de septiembre | 2020-09-21 | 2020-09-22 | 2022-04-08 | CCAA (09) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2020-11363 |
| E10 | STC 37/2022: anulación parcial de la Ley catalana 11/2020 | Sentencia del Tribunal Constitucional 37/2022, de 10 de marzo | 2022-04-08 | 2022-04-08 |  | CCAA (09) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2022-5807 |
| E11 | RDL 6/2022 art. 46: limitación extraordinaria de la actualización anual de la renta | Real Decreto-ley 6/2022, de 29 de marzo | 2022-03-30 | 2022-03-31 | 2024-12-31 | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2022-4972 |
| E12 | RDL 11/2022: prórroga y modificación del tope de actualización de rentas | Real Decreto-ley 11/2022, de 25 de junio | 2022-06-26 | 2022-06-27 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2022-10557 |
| E13 | RDL 20/2022: tope de actualización de rentas hasta 31-12-2023 y desahucios hasta 30-06-2023 | Real Decreto-ley 20/2022, de 27 de diciembre | 2022-12-28 | 2022-12-28 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2022-22685 |
| E14 | Ley 12/2023 por el derecho a la vivienda | Ley 12/2023, de 24 de mayo | 2023-05-25 | 2023-05-26 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-12203 |
| E15 | Ley 12/2023 DF 6: tope del 3 % a la actualización de rentas en 2024 | Ley 12/2023, de 24 de mayo, disposición final sexta | 2023-05-25 | 2023-05-26 | 2024-12-31 | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-12203 |
| E16 | Ley 12/2023 DF 2: incentivos IRPF al arrendamiento de vivienda | Ley 12/2023, de 24 de mayo, disposición final segunda | 2023-05-25 | 2024-01-01 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-12203 |
| E17 | Resolución de 14-03-2024: sistema estatal de índices de precios de referencia del alquiler | Resolución de 14 de marzo de 2024, de la Secretaría de Estado de Vivienda y Agenda Urbana | 2024-03-15 | 2024-03-16 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-5213 |
| E18 | Actualización del sistema de índices de referencia (29-09-2025) | Resolución de 29 de septiembre de 2025, de la Secretaría de Estado de Vivienda y Agenda Ur | 2025-09-30 | 2025-10-01 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-19403 |
| E19 | Actualización del sistema de índices de referencia (16-04-2026) | Resolución de 16 de abril de 2026, de la Secretaría de Estado de Vivienda y Agenda Urbana | 2026-04-20 | 2026-04-21 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-8691 |
| E20 | IRAV: índice de referencia para la actualización de la renta (INE) | Resolución de 18 de diciembre de 2024, de la Presidencia del INE | 2024-12-20 | 2025-01-01 |  | nacional (ES) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-26685 |
| E21 | Fin de las 'golden visas' por inversión inmobiliaria (LO 1/2025) | Ley Orgánica 1/2025, de 2 de enero (modifica arts. 63-67 Ley 14/2013) | 2025-01-03 | 2025-04-03 |  | nacional (ES) | no residentes | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-76 |
| E22 | RD 1312/2024: Registro Único de Arrendamientos (alquiler de corta duración) | Real Decreto 1312/2024, de 23 de diciembre | 2024-12-24 | 2025-01-02 |  | nacional (ES) | alquiler turístico | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-26931 |
| E23 | Decreto-ley catalán 3/2023: régimen urbanístico de viviendas de uso turístico | Decreto-ley 3/2023 de Cataluña, de 7 de noviembre | 2023-11-08 | 2023-11-09 |  | CCAA (09) | alquiler turístico | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-281 |
| E24 | Decreto-ley valenciano 9/2024: viviendas de uso turístico | Decreto-ley 9/2024 del Consell, de 2 de agosto | 2024-08-07 | 2024-08-08 |  | CCAA (10) | alquiler turístico | VERIFICADO | https://www.boe.es/buscar/doc.php?id=DOGV-r-2024-90168 |
| E25 | Decreto-ley balear 4/2025 contra la oferta turística ilegal | Decreto-ley 4/2025 de Illes Balears, de 11 de abril | 2025-04-15 | 2025-04-16 |  | CCAA (04) | alquiler turístico | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-14462 |
| E26 | Ley canaria 6/2025 de ordenación sostenible del uso turístico de viviendas | Ley 6/2025 de Canarias, de 10 de diciembre | 2025-12-12 | 2025-12-13 |  | CCAA (05) | alquiler turístico | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-26358 |
| ZT01 | Zonas tensionadas (art. 18 Ley 12/2023): Cataluña, 1.ª ronda (Resolución TER/800/2024) | Resolución de 14 de marzo de 2024, de la Secretaría de Estado de Vivienda y Agenda Urbana, | 2024-03-15 | 2024-03-16 | 2027-03-16 | CCAA (09) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-5214 |
| ZT02 | Zonas tensionadas (art. 18 Ley 12/2023): Cataluña, 2.ª ronda (Resolución TER/2408/2024) | Resolución de 8 de octubre de 2024, de la Secretaría de Estado de Vivienda y Agenda Urbana | 2024-10-09 | 2024-10-10 | 2027-10-10 | CCAA (09) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-20576 |
| ZT03 | Zonas tensionadas (art. 18 Ley 12/2023): País Vasco: Errenteria | Resolución de 28 de enero de 2025, de la Secretaría de Estado de Vivienda y Agenda Urbana, | 2025-01-30 | 2025-01-31 | 2028-01-31 | municipios concretos (16) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-1721 |
| ZT04 | Zonas tensionadas (art. 18 Ley 12/2023): País Vasco: Lasarte-Oria, Zumaia, Barakaldo, Irun | Resolución de 29 de abril de 2025, de la Secretaría de Estado de Vivienda y Agenda Urbana, | 2025-04-30 | 2025-05-01 | 2028-05-01 | municipios concretos (16) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-8636 |
| ZT05 | Zonas tensionadas (art. 18 Ley 12/2023): Navarra (21), A Coruña, Galdakao (D2), Donostia | Resolución de 28 de julio de 2025, de la Secretaría de Estado de Vivienda y Agenda Urbana, | 2025-07-29 | 2025-07-30 | 2028-07-30 | municipios concretos (12;15;16) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-15728 |
| ZT06 | Zonas tensionadas (art. 18 Ley 12/2023): País Vasco: Astigarraga, Bilbao, Usurbil, Vitoria-Gasteiz | Resolución de 29 de octubre de 2025, de la Secretaría de Estado de Vivienda y Agenda Urban | 2025-10-30 | 2025-10-31 | 2028-10-31 | municipios concretos (16) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-21901 |
| ZT07 | Zonas tensionadas (art. 18 Ley 12/2023): País Vasco: Hernani, Lezo, Tolosa | Resolución de 30 de enero de 2026, de la Secretaría de Estado de Vivienda y Agenda Urbana, | 2026-02-02 | 2026-02-03 | 2029-02-03 | municipios concretos (16) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-2448 |
| ZT08 | Zonas tensionadas (art. 18 Ley 12/2023): País Vasco: Pasaia, Zestoa, Mondragón | Resolución de 23 de abril de 2026, de la Secretaría de Estado de Vivienda y Agenda Urbana, | 2026-04-27 | 2026-04-28 | 2029-04-28 | municipios concretos (16) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-9175 |
| ZT09 | Zonas tensionadas (art. 18 Ley 12/2023): Asturias (ámbitos), Santiago de Compostela, Basauri | Resolución de 24 de julio de 2026, de la Secretaría de Estado de Vivienda y Agenda Urbana, | 2026-07-29 | 2026-07-30 | 2029-07-30 | municipios concretos (03;12;16) | alquiler | VERIFICADO | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-16532 |
| N01 | Plan Reside (Madrid): restricción de viviendas de uso turístico | Modificación puntual del Plan General de Madrid (aprobación definitiva por Consejo de Gobi |  |  |  | municipio (13) | alquiler turístico | NO VERIFICADO |  |
| N02 | Normativa municipal de apartamentos turísticos de València (moratoria 2024 y modificación de normas urbanísticas 2026) | Ordenanza/normas urbanísticas del Ayuntamiento de València |  |  |  | municipio (10) | alquiler turístico | NO VERIFICADO |  |
| N03 | Normativa municipal de Barcelona sobre viviendas de uso turístico (PEUAT y fin de licencias) | Plan especial urbanístico de alojamientos turísticos (Ayuntamiento de Barcelona) |  |  |  | municipio (09) | alquiler turístico | NO VERIFICADO |  |
| N04 | Impuesto estatal a la compra de inmuebles por no residentes extracomunitarios | Proposición de ley (no publicada como norma) |  |  |  | nacional (ES) | no residentes | NO VERIFICADO |  |
| N05 | Sentencia del Tribunal Supremo sobre el Registro Único de Arrendamientos (RD 1312/2024) | Sentencia TS (referencia no confirmada) |  |  |  | nacional (ES) | alquiler turístico | NO VERIFICADO |  |
| N06 | Recargo de IBI a viviendas vacías: modulación estatal (Ley 12/2023) y recargos municipales | Texto refundido Ley Reguladora de Haciendas Locales, art. 72 (modulado por Ley 12/2023) |  |  |  | municipios concretos (ES) | compra | NO VERIFICADO |  |

Descripciones (≤30 palabras) y notas de verificación: columnas `descripcion_breve` y `nota_verificacion` del CSV.

## Zonas de mercado residencial tensionado (art. 18 Ley 12/2023)

Cada resolución trimestral de la Secretaría de Estado de Vivienda y Agenda Urbana (BOE) fija la vigencia de 3 años desde el día siguiente a su publicación. `fecha_efecto` = ese día; `fecha_fin_prevista` = +3 años. Fecha de la declaración autonómica por municipio: `fecha_declaracion_autonomica` y `fecha_publicacion_autonomica` en el CSV de zonas.

| CCAA (INE) | nº municipios/ámbitos | fecha de efecto estatal (por resolución) |
|---|---|---|
| Principado de Asturias (03) | 6 | 2026-07-30: 6 |
| Cataluña (09) | 271 | 2024-03-16: 140; 2024-10-10: 131 |
| Galicia (12) | 2 | 2025-07-30: 1; 2026-07-30: 1 |
| Navarra (15) | 21 | 2025-07-30: 21 |
| País Vasco (16) | 18 | 2025-01-31: 1; 2025-05-01: 4; 2025-07-30: 2; 2025-10-31: 4; 2026-02-03: 3; 2026-04-28: 3; 2026-07-30: 1 |

Municipios de interés para el módulo C. Valenciana: no hay zonas tensionadas declaradas en la Comunitat Valenciana a 2026-10-10 en ninguna resolución del BOE hallada (9 resoluciones revisadas).

## Notas y límites

- **Topes de renta 2 % / 3 %:** el art. 46 del RDL 6/2022 (texto consolidado) liga la actualización 2022-2023 a la variación del Índice de Garantía de Competitividad; el 3 % para 2024 consta literalmente (Ley 12/2023, DF 6). No se encontró en el articulado un «2 %» literal para 2023; esa cifra viene de prensa (OCU) y no se usa como fecha/valor oficial. No se halló prórroga para 2025; en su lugar el IRAV (INE) rige desde 2025-01-01 (E20).
- **Desahucios:** RDL 16/2025 y RDL 2/2026 figuran derogados en los metadatos del BOE (no convalidados); la fecha de fin de E08 es la del metadato BOE (la prensa cita 26-02-2026). No se incluyeron los RDL de prórroga intermedios (2021-2024), por no haberse verificado uno a uno.
- **STC 37/2022:** anula arts. 1, 6-13, 15, 16.2, DA 1-4, DT 1 y DF 4.b de la Ley 11/2020; la STC 57/2022 (otros preceptos) solo consta en fuente secundaria y no se incluye como evento.
- **Cataluña:** la resolución TER/2940/2023 (agosto de 2023) fue modificada por TER/800/2024; a efectos del BOE la primera relación (140 municipios) rige desde 2024-03-16 y la segunda (131) desde 2024-10-10, hasta 271.
- **Golden visas:** LO 1/2025 (no «Ley 1/2025»), vigencia 2025-04-03; se mantienen solicitudes previas y renovaciones.
- **Turismo:** verificados con texto oficial Cataluña (DL 3/2023), C. Valenciana (DL 9/2024), Baleares (DL 4/2025), Canarias (Ley 6/2025) y RD 1312/2024. Madrid (Plan Reside), València ciudad y Barcelona ciudad quedan NO VERIFICADOS (sin acceso a BOCM/BOP/BOPB). La mención de una sentencia del TS contra el RD 1312/2024 es de una sola fuente secundaria.
- **Fiscalidad no residentes:** no hay norma publicada de impuesto a compradores no UE (solo proposición de ley 2025, fuentes secundarias). IVA/ITP/IBI: sin evento nacional verificado más allá de E16 (IRPF alquiler).
- Todo lo no verificable está en `docs/v2/fallidas/eventos.md`.
