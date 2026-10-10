# Estado v3

| Tarea | Oleada | Estado | Capa | Resultado principal | Tokens subagentes |
|---|---|---|---|---|---|
| Setup (r3/main, CLAUDE.md, make check, docs/v3) | 0 | hecho | — | — | 0 |
| Literatura v3 (replicación, magnitudes, métodos) | 1 | hecho | — | 25 VERIFICADA / 3 NO; GL2020 réplica parcial (alquiler); MESVAL no replicable (Fotocasa); JMS2023 parcial | 166.408 |
| D1 INE (censo, VUT sección, ADRH) | 1 | en curso | — | — | — |
| D2 fianzas, SERPAVI sección, EFF, emancipación, eventos | 1 | hecho (parcial) | — | SERPAVI sección/distrito nacional 2011-2024; Incasòl municipal 2007-2026; Eurostat emancipación; eventos BOE (6/8 verificados). Fallidas: SIU, GVA, BCN barrios, EFF, ECV | 99.401 |
| EFF/ECV tenencia por edad (pdf-extractor) | 1 | en curso | — | — | — |
| D3 Airbnb/HUT, Barcelona por barrio | 1 | hecho (parcial) | — | IA: 36 instantáneas ES (9 ciudades, 2025-12 a 2026-09; BCN 18.177→15.236 anuncios, habitación −29 %, entera −10 %); HUT: 104.502 HUT Alta (foto 2026-10-05, sin fechas alta/baja); BCN opendata, Google Trends y atractivos bloqueados | ~0 (sin subagentes) |

**Hecho:** setup; literatura v3; D2 (scripts src/v3/fetch_*_v3.py, build_zonas_eventos_v3.py).
**Pendiente de datos:** EFF y ECV (pdf-extractor en curso); Barcelona por barrio (D3 en curso); Madrid por distrito; GVA fianzas; SIU (solicitud); obligatoriedad RD 1312/2024 sin verificar.
**Siguiente:** al llegar D1/D3: P-A (C1), P-B (C2), potencia P-C, replicación García-López → puerta oleada 1.
**Tokens de subagentes v3:** 265.809 / 3.500.000 (cierre al 80 %: 2.800.000).
