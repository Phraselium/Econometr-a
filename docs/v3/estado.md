# Estado v3

| Tarea | Oleada | Estado | Capa | Resultado principal | Tokens subagentes |
|---|---|---|---|---|---|
| Setup (r3/main, CLAUDE.md, make check, docs/v3) | 0 | hecho | — | — | 0 |
| D1 datos INE (municipal y sección) | 1 | parcial | — | Censo 2021 sección (indicadores, edad 3 grupos), VUT municipal %, cartografía 2021; VUT y ADRH sección no disponibles | ~0 (sin subagentes) |
| Literatura v3 (replicación, magnitudes, métodos) | 1 | hecho | — | 25 VERIFICADA / 3 NO; GL2020 réplica parcial (alquiler); MESVAL no replicable (Fotocasa); JMS2023 parcial | 166.408 |
| D1 INE (censo, VUT sección, ADRH) | 1 | hecho | — | Censo 2021 por sección (36.333) y municipio; VUT municipal. VUT por sección/distrito 2021M02-2026M05 (12 oleadas) y ADRH/censo anual por sección obtenidos por el orquestador del GIS del INE | 123.392 |
| Sellado v3 (20 % distritos estratificado + 2026M05) | 1 | hecho | — | 2.136 distritos | 0 |
| P-A hechos (C1) | 1 | hecho | C1 | Déficit 2021-25: 701 mil [560-969] (BdE ≈750 mil dentro); 2012-21: −132 mil (excedente). Hogares latentes 25-34: 188-748 mil. Vacías en tercil alto de presión: 27,5-44,7 %. Precio/renta 2023: 3,0-3,8. Propietarios <35 años 2022: 30,7-31,8 %. Precio/alquiler 2015-24: medidas de signo contrario | 232.682 |
| Potencia P-C + réplica GL Barcelona | 1 | hecho | C4 | GO: C1 (FE), C1-SSIV 6 ciudades, C3; NO-GO: C2, C4. GL: T=0,039 log-p/pp; BCN −0,004 [−0,008; −0,0005] NO REPLICADO (signo contrario); València PARCIAL; resto NO REPLICADO | 88.207 |
| P-B cotas (C2) | 1 | hecho | C2 | B1 VUT: desplazamiento ≤2,7 % del stock de alquiler; precio ≤8,3 % (|ε|=0,33; rango 1,2-11) frente a +6,3 % IPC alquiler; 25 % de la subida en municipios sin crecimiento de VUT. B2 inmigración ≤80 % de Δhogares 2014-25; no explica 2008-14. B4 tipos: puede cubrir 2014-21; signo contrario 2022-25. B3 en espera | 127.032 |
| D2 fianzas, SERPAVI sección, EFF, emancipación, eventos | 1 | hecho (parcial) | — | SERPAVI sección/distrito nacional 2011-2024; Incasòl municipal 2007-2026; Eurostat emancipación; eventos BOE (6/8 verificados). Fallidas: SIU, GVA, BCN barrios, EFF, ECV | 99.401 |
| EFF/ECV tenencia por edad (pdf-extractor) | 1 | hecho | — | EFF 8 oleadas 2002-2022 (validada, error 0); ECV 2004-2025 por edad | 99.567 |
| D3 Airbnb/HUT, Barcelona por barrio | 1 | hecho (parcial) | — | IA: 36 instantáneas ES (9 ciudades, 2025-12 a 2026-09; BCN 18.177→15.236 anuncios, habitación −29 %, entera −10 %); HUT: 104.502 HUT Alta (foto 2026-10-05, sin fechas alta/baja); BCN opendata, Google Trends y atractivos bloqueados | ~0 (sin subagentes) |

**Hecho:** setup; literatura v3; D2 (scripts src/v3/fetch_*_v3.py, build_zonas_eventos_v3.py).
**Pendiente de datos:** D1 INE (en curso); Barcelona por barrio (bloqueado, anti-bot); Madrid por distrito; GVA fianzas; SIU (solicitud); obligatoriedad RD 1312/2024 sin verificar.
**Siguiente:** P-A, P-B, potencia y réplica GL (en curso) → make check → reviewer oleada 1 → go/no-go P-C.
**Tokens de subagentes v3:** 1.040.211 / 3.500.000 (cierre al 80 %: 2.800.000).
