# Cobertura de datos V9 (fuente × nivel territorial × periodo) y estado por diseño

Fecha: 2026-10-14. «Proyecto» = ya estaba en data/raw antes de V9; «V9» = descargado en esta tarea (data/raw/v9).

## Matriz

| Fuente | Sección | Barrio o distrito | Municipio | Provincia o CCAA | País (UE) | Periodo | Frecuencia | Origen | Huecos |
|---|---|---|---|---|---|---|---|---|---|
| Censo anual INE, población por país de nacionalidad (22 grupos) | ✔ | — | ✔ | ✔ | — | 2021-2025 | anual | V9 | Sin país individual (solo 22 grupos); antes de 2021, padrón (proyecto) |
| Padrón València por barrio y nacionalidad | — | ✘ (2023-2026) | — | — | — | 2005-2022 (proyecto) | anual | proyecto | 2023-2026 no descargable; sustituto: censo anual por sección |
| EMAL Euskadi (fianzas) | — | ✔ zonas de capitales | ✔ (>20.000 hab.) | ✔ TH | — | 2016T1-2025T4 | trimestral | V9 | Stock vigente detallado solo en XLSX; municipios <20.000 solo en estratos |
| Incasòl Cataluña (fianzas) | — | — | ✔ | ✔ | — | 2007-2026T1 | trimestral | proyecto + V9 (no redistribuible) | Mismos periodos que v3 (sin novedad) |
| Fianzas GVA | — | — | ✔ | ✔ | — | 2020-2026 | mensual | proyecto (V9 idéntico) | Sin desagregar por duración (temporada) |
| SERPAVI | ✔ | ✔ | ✔ | ✔ | — | 2011-2024 | anual | proyecto | 2025 no publicado |
| IPVA INE (nuevos/existentes) | — | ✔ distritos de capitales | ✔ (total, >10.000 hab.) | ✔ (por antigüedad) | — | 2015-2024 | anual | proyecto + V9 | Nuevos/existentes no por municipio |
| INE viviendas turísticas | ✔ | — | ✔ | ✔ | — | 2020M08-2026M05 | semestral | proyecto | Noviembre 2026 aún no publicado |
| Registro VUT GVA | (dirección) | — | ✔ | ✔ | — | cortes 2025-01-26 y 2026-10-14; mensual reconstruido 2015-01 a 2025-01 | corte o mensual | V9 | Bajas posteriores a 2025-01 no fechadas |
| Inside Airbnb | ✔ (5 ciudades) | ✔ (barrio IAB, VLC y BCN) | ✔ | — | — | solo 2026-09 | edición | V9 | Ediciones históricas no públicas (2019-2025) |
| Eurostat plataformas | — | — | — | ✔ NUTS 2-3 | ✔ | 2018-2025/26 | mensual y anual | V9 | Sin nivel LAU (municipio) |
| BCE MIR, tipos por fijación y volumen | — | — | — | — | ✔ (21) | 2003-01 a 2026-08 | mensual | V9 | Volúmenes solo totales, no por fijación |
| Eurostat HPI y alquileres UE | — | — | — | — | ✔ | hasta 2026T2 | trimestral | proyecto (v8) | Al día |
| Microdatos EPA | — | — | — | ✔ (CCAA o provincia) | — | 2018T1-2026T2 | trimestral | V9 (no versionado) | Sin municipio |
| Microdatos ECV | — | — | — | ✔ (CCAA) | — | 2018-2025 | anual | V9 (no versionado) | Muestra pequeña por edad y CCAA |
| Afiliación SS por municipio | — | — | ✘ | (provincial y CNAE en la web) | — | — | mensual | ✘ | Página dinámica (fuentes_fallidas.md) |
| Aena, pasajeros | — | — | — | — | — | — | mensual | ✘ | Sin descarga directa |

## Fuentes añadidas en V9 COMPLETO, F1 (2026-10-15)

| Fuente | Sección | Barrio | Municipio | Provincia | País | Periodo | Origen | Huecos |
|---|---|---|---|---|---|---|---|---|
| IDESCAT turall: HUT y apartamentos turísticos | — | — | ✔ | ✔ | — | 2015-2025 (anual, 31-dic) | V9 | Sin 2014 y anteriores; hoteles sin nivel municipal |
| Registre de Turisme (agregado) / IEET | — | — | ✔ | — | — | corte 2026-10 / 2017S1-2025S1 | V9 (no redistribuible) | Registre sin fecha de alta; IEET sin código de municipio |
| Open Data BCN, HUT vigentes | — | ✔ (73 barrios; 66 con HUT) | 08019 | — | — | año de expediente 2008-2026 | V9 | Bajas no observadas; cortes trimestrales bloqueados (anti-bot) |
| Padrón continuo por nacionalidad y país de nacimiento (40 grupos, incl. Venezuela, Colombia, Ucrania) | — | — | ✔ | ✔ | — | 2003-2022 | V9 | 2023-2025: censo anual (22 grupos, sin país individual) |
| EM / EMCR (migraciones) | — | — | (EMCR intermunicipal, no descargado) | ✔ | — | 2008-2021 / 2021-2024 | V9 | Antes de 2008 (EVR) no disponible |
| Censo 2011, viviendas por tipo | — | — | (3456, >2.000 hab., no descargado) | ✔ | — | 2011 | V9 | Censo 2001 no descargable |
| Callejero censo electoral: sección × CP | ✔ | — | ✔ | — | — | 2025-06-30 | V9 | Un solo corte (CP estables) |
| SEPE paro y contratos | — | — | ✔ | ✔ | — | 2006-01 a 2026 | V9 | «<5» suprimidos |
| BCE RAI, cuota a tipo variable | — | — | — | — | ✔ (27 + U2) | 2003-01 a 2026-08 | V9 | Inicio desigual por país |
| Eurostat IPCA alquileres (CP041) | — | — | — | — | ✔ | 1996-01 a 2026-08 | V9 | — |

## Estado por diseño de V9 COMPLETO (F3) — decide qué se estima

| Diseño | Datos | Estado | Qué hay | Qué falta / consecuencia |
|---|---|---|---|---|
| D1 Zonas tensionadas y topes (Cataluña, Euskadi) | **Completos** | Se estima | Tratamiento: Ley 11/2020 (332 municipios, 2020-09-22 a 2022-03, STC 37/2022), zonas tensionadas Cataluña (140 desde 2024-03-16; 131 desde 2024-07), Euskadi (18 declaraciones municipales 2024-10 a 2026-05) con fecha del BOE; resultados Incasòl municipal trimestral 2007-2026T1 (renta media y contratos; no redistribuible), EMAL municipal 2016-2025, IPVA municipal anual 2011-2024 | Euskadi: las zonas declaradas en 2025-2026 tienen ≤4 trimestres posteriores en EMAL (hasta 2025T4): solo el subdiseño de Cataluña tiene potencia confirmatoria (F2) |
| D2 Pisos turísticos × COVID (Cataluña) | **Completos** | Se estima | Exposición pre-2020: HUT por municipio IDESCAT 2019 (plazas por vivienda o por habitante); Barcelona por barrio (aprox.); resultados Incasòl trimestrales | Inside Airbnb histórico no necesario (la exposición es el registro oficial) |
| D3 València 2025-2026 (caída del registro VUT) | **Completos con limitaciones** | Se estima como descriptivo si la potencia es baja | Registro GVA por CP (cortes 2025-01 y 2026-10), VUT INE por sección → CP (callejero), fianzas GVA por CP 2020-2026, censo anual por sección, ADRH por sección | Solo dos cortes del registro: diferencias largas, no evento; ≈ 30-60 CP en València ciudad |
| D4 Inmigración (réplica Sanchis-Guarner) | **Completos** | Se estima | Cuotas iniciales por país y municipio/provincia (padrón 2003); crecimiento nacional por país (padrón 2003-2022 + Eurostat migr_pop1ctz); valor tasado (MIVAU), IPC alquiler provincial (2002-), IPVA municipal (2011-); migración interna EM 2008-2021 y EMCR 2021-2024 | Réplica 2001-2012: cuotas en 2003 (primer año con país), no 2001; EVR pre-2008 ausente: efecto total vs parcial solo 2008-2021 |
| D5 Tipos × exposición (zona euro) | **Completos** | Se estima | Shocks JK mensuales 1999-2025 (no redistribuible), cuota a tipo variable por país (RAI, desde 2003), HPI trimestral (prc_hpi_q, 2005-), IPCA alquiler mensual 1996-2026 | Exposición pre-periodo: media 2003-2007 de la cuota a tipo variable (fija, no endógena al ciclo posterior) |
| D6 Bono Alquiler Joven, RD en 35 años | **Insuficientes** | **No se estima** | ECV: año de nacimiento y mes/año de encuesta, sin mes de nacimiento (PB130 no publicado); EPA: edad en tramos quinquenales | Sin edad exacta ni receptores identificados: la RD no es posible (hipotesis.md, D6) |
| D7 Contabilidad hogares-viviendas | **Completos (2011-2025)** | Se estima (contable, C1/C4) | Censo 2011 (3457), Censo 2021 (municipal), ECP hogares 2021-2026, padrón por nacionalidad, EM/EMCR, terminadas MIVAU, proyección de hogares | Censo 2001 no descargable: la descomposición 2001-2011 solo nacional (EPA), marcada |

## Estado por diseño del plan v9 (versión de V9-DATOS, 2026-10-14; histórico)


| Diseño | ¿Datos completos? | Qué hay | Qué falta |
|---|---|---|---|
| Zonas tensionadas (Cataluña y Euskadi): DiD escalonado con Honest DiD | **Parcial** | Incasòl municipal trimestral 2007-2026T1 (no redistribuible); EMAL municipal y por zonas 2016-2025; SERPAVI 2011-2024; IPVA; fianzas GVA como control | Fechas oficiales de declaración por municipio (DOGC, BOPV, BOE): se transcriben de la norma, no hay fichero abierto. SERPAVI 2025 |
| Pisos turísticos, shock COVID en Cataluña | **No** | INE VUT desde 2020M08; Eurostat plataformas NUTS 3 desde 2018; Inside Airbnb solo 2026-09 | Ediciones históricas de Inside Airbnb (2019-2021), que hay que pedir a Inside Airbnb, o el registro turístico de Cataluña con fechas de alta |
| Pisos turísticos, caída 2025-2026 en València | **Parcial** | Registro VUT de la GVA (cortes 2025-01 y 2026-10, panel por municipio y código postal); INE VUT por sección hasta 2026M05; censo por sección 2021-2025; fianzas GVA; Inside Airbnb 2026-09 | Bajas fechadas después de enero de 2025 (solo dos cortes); cortes intermedios (se pueden guardar desde ahora con `make datos_v9` periódico); padrón por barrio 2023-2026 (sustituido por el censo) |
| Shock migratorio por país de origen (réplica de Sanchis-Guarner) | **Parcial** | Censo anual por sección, municipio y 22 grupos de nacionalidad 2021-2025; flujos UE por ciudadanía (v8, Eurostat migr_imm1ctz); padrón por nacionalidad antes de 2021 (proyecto, municipal) | Cuotas iniciales por país individual a nivel municipal antes de 2021 con los mismos grupos (padrón continuo del INE por país, por descargar); afiliación de extranjeros por municipio (fallida) |
| Tipos de interés con exposición en panel europeo | **Sí** | Tipos por fijación y volúmenes BCE 2003-2026, 21 países; HPI y alquileres Eurostat hasta 2026T2 (v8); shocks JK (v8, no redistribuible) | — (el volumen por fijación no existe; se usa la cuota a tipo variable por país) |
| Bono Alquiler Joven, discontinuidad por edad | **Parcial** | Microdatos EPA 2018-2026T2 y ECV 2018-2025 (edad, tenencia, alquiler pagado) | Beneficiarios por edad y CCAA (no publicados); fecha de entrada en vigor por CCAA (normativa, a transcribir) |
| Reconciliación del déficit y descomposición de hogares | **Sí** | Censo anual 2021-2025; proyección de hogares, EPA y terminadas (proyecto) | — |
