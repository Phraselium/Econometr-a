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

| Lista oficial Ley 11/2020 y zonas tensionadas (Cataluña) | 1 | hecho | — | 61 municipios (Ley 11/2020); 140 y 131 (zonas 2024) | 97.863 |

| Revisión oleada 1 (it. 1: REHACER O1-O10) y correcciones P-A/P-B/POT/GL | 1 | hecho | — | ver docs/v3/revision_oleada1.md | 132.184 + correcciones 78.877 |
| Revisión oleada 1, iteración 2 | 1 | APROBAR | — | pre-registro congelado (ancla 204c073); limitaciones v3 | 35.188 |
| Oleada 2: H3-1/H3-2 (VUT → alquiler) | 2 | hecho | C4 | H3-1 nacional entrenamiento +0,0003/pp [−0,0007; 0,0013]; sellado +0,0010 [−0,0007; 0,0028] p=0,23 (+0,14 %, +0,8 €/mes por 1,37 pp). H3-2 sellado +0,004 [−0,009; 0,017]. Fallan a-d → C4 | 135.533 |
| Holm m=4 | 2 | hecho | — | p_holm: H3-1 0,47; H3-2 0,50; H3-3a 0,048; H3-3b 0,0002 (ninguna en C3 por fallar a-c) | 0 |
| Oleada 2: H3-3 topes + réplica JMS 2023 | 2 | hecho | C4 | H3-3a renta −5,4 % [−7,1; −3,7] (−37 €/mes); sellado SERPAVI −0,8 % [−1,4; −0,1]; falla RR y sensibilidad → C4. H3-3b contratos −4,9 % [−9,9; +0,5] → C4. JMS: renta REPLICADO (esp. más cercana) | 130.585 |

| P-D simulaciones de soluciones | 3 | hecho | C2/C4 | +104-413 mil viv/año necesarias (frente a 89-101 mil terminadas): brecha positiva en todo el rango (C2); topes: signo del neto depende de L y ε (C4); vacías: 4,6-51 % de la brecha | 139.692 |

| Revisión oleada 2 (REHACER W1-W10 → APROBAR it. 2) y correcciones | 2 | APROBAR | — | regla común del verificador; estándar único C4 para traducciones a precio | 154.391 + correcciones 35.309 |
| Entregables: lo_que_sabemos, articulo, informe_politica (València), verificador | 3 | hecho | — | 14 fichas: 0 RESPALDADA, 3 PARCIALMENTE, 11 SIN EVIDENCIA SUFICIENTE | 0 (orquestador) |
| Revisión oleada 3 (REHACER Z1-Z8 → APROBAR it. 2) | 3 | APROBAR | — | limitaciones v3 completadas | 126.108 |

**Hecho:** setup; literatura v3; D2 (scripts src/v3/fetch_*_v3.py, build_zonas_eventos_v3.py).
**Pendiente de datos:** D1 INE (en curso); Barcelona por barrio (bloqueado, anti-bot); Madrid por distrito; GVA fianzas; SIU (solicitud); obligatoriedad RD 1312/2024 sin verificar.
**Siguiente:** cierre: make all sin red ×2 en clon limpio sobre el HEAD final; resumen final.
**Tokens de subagentes v3:** 2.106.329 / 3.500.000 (cierre al 80 %: 2.800.000).
- 2026-10-10: cataluna_contencion_rentas_v3.csv generado (61 Ley 11/2020; 140 + 131 Ley 12/2023; 0 en 2025). Pendiente: DOGC no accesible; prórroga 2026 no verificada. Ver decisiones.md.
