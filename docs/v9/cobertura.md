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

## Estado por diseño del plan v9

| Diseño | ¿Datos completos? | Qué hay | Qué falta |
|---|---|---|---|
| Zonas tensionadas (Cataluña y Euskadi): DiD escalonado con Honest DiD | **Parcial** | Incasòl municipal trimestral 2007-2026T1 (no redistribuible); EMAL municipal y por zonas 2016-2025; SERPAVI 2011-2024; IPVA; fianzas GVA como control | Fechas oficiales de declaración por municipio (DOGC, BOPV, BOE): se transcriben de la norma, no hay fichero abierto. SERPAVI 2025 |
| Pisos turísticos, shock COVID en Cataluña | **No** | INE VUT desde 2020M08; Eurostat plataformas NUTS 3 desde 2018; Inside Airbnb solo 2026-09 | Ediciones históricas de Inside Airbnb (2019-2021), que hay que pedir a Inside Airbnb, o el registro turístico de Cataluña con fechas de alta |
| Pisos turísticos, caída 2025-2026 en València | **Parcial** | Registro VUT de la GVA (cortes 2025-01 y 2026-10, panel por municipio y código postal); INE VUT por sección hasta 2026M05; censo por sección 2021-2025; fianzas GVA; Inside Airbnb 2026-09 | Bajas fechadas después de enero de 2025 (solo dos cortes); cortes intermedios (se pueden guardar desde ahora con `make datos_v9` periódico); padrón por barrio 2023-2026 (sustituido por el censo) |
| Shock migratorio por país de origen (réplica de Sanchis-Guarner) | **Parcial** | Censo anual por sección, municipio y 22 grupos de nacionalidad 2021-2025; flujos UE por ciudadanía (v8, Eurostat migr_imm1ctz); padrón por nacionalidad antes de 2021 (proyecto, municipal) | Cuotas iniciales por país individual a nivel municipal antes de 2021 con los mismos grupos (padrón continuo del INE por país, por descargar); afiliación de extranjeros por municipio (fallida) |
| Tipos de interés con exposición en panel europeo | **Sí** | Tipos por fijación y volúmenes BCE 2003-2026, 21 países; HPI y alquileres Eurostat hasta 2026T2 (v8); shocks JK (v8, no redistribuible) | — (el volumen por fijación no existe; se usa la cuota a tipo variable por país) |
| Bono Alquiler Joven, discontinuidad por edad | **Parcial** | Microdatos EPA 2018-2026T2 y ECV 2018-2025 (edad, tenencia, alquiler pagado) | Beneficiarios por edad y CCAA (no publicados); fecha de entrada en vigor por CCAA (normativa, a transcribir) |
| Reconciliación del déficit y descomposición de hogares | **Sí** | Censo anual 2021-2025; proyección de hogares, EPA y terminadas (proyecto) | — |
