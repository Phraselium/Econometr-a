# Estado v3

| Tarea | Oleada | Estado | Capa | Resultado principal | Tokens subagentes |
|---|---|---|---|---|---|
| Setup (r3/main, CLAUDE.md, make check, docs/v3) | 0 | hecho | — | — | 0 |
| D2 descarga datos nuevos | 1 | parcial | — | Incasòl 138k filas; SERPAVI secciones 4,6M obs; Eurostat emancipación; eventos BOE (6 verificados) | 0 (sin subagentes) |
| Literatura v3 (replicación, magnitudes, métodos) | 1 | hecho | — | 25 VERIFICADA / 3 NO; GL2020 réplica parcial (alquiler); MESVAL no replicable (Fotocasa); JMS2023 parcial | 166.408 |
| D1 INE (censo, VUT sección, ADRH) | 1 | en curso | — | — | — |
| D2 fianzas, SERPAVI sección, EFF, emancipación, eventos | 1 | hecho (parcial) | — | SERPAVI sección/distrito nacional 2011-2024; Incasòl municipal 2007-2026; Eurostat emancipación; eventos BOE (6/8 verificados). Fallidas: SIU, GVA, BCN barrios, EFF, ECV | 99.401 |
| EFF/ECV tenencia por edad (pdf-extractor) | 1 | en curso | — | — | — |
| D3 Airbnb/HUT, Barcelona por barrio | 1 | en curso | — | — | — |

**Hecho:** setup; D2: src/v3/fetch_serpavi_seccion_v3.py, fetch_incasol_fianzas_v3.py, fetch_madrid_alquiler_cp_v3.py, fetch_eurostat_emancipacion_v3.py, build_zonas_eventos_v3.py; salidas en data/raw/v3/; fallidas en docs/v3/fuentes_fallidas.md.
**Pendiente D2:** EFF tablas publicadas; INE ECV/EPA; Barcelona barrios y Madrid distritos; GVA fianzas (reintento); SIU (fallida; solicitud); verificar obligatoriedad RD 1312/2024 y DL 3/2023 y 9/2024.
**Siguiente:** completar pendientes D2 y luego oleada 1 (literatura, solicitudes de transparencia; P-A, P-B, potencia P-C, replicación García-López).
**Tokens de subagentes v3:** 265.809 / 3.500.000 (cierre al 80 %: 2.800.000).
