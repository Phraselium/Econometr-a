# V17 · Estado

V17 se ejecuta dentro de V18 (docs/v17/decisiones.md, K0): fases 0-3 y 5; la 4 se integra en la fase 6 de V18. Todo a posteriori.

## Hecho
- 2026-10-19 · Plan guardado (docs/v17/plan.md). Infraestructura:
  - comandos /v17-fase0 … /v17-fase5 y /v17-estado;
  - objetivos make v17_f0 … v17_f5 y v17;
  - check_v17 dentro de make check (rótulo «a posteriori», cifras V17 en C4 con lectura propia, sin promoción en cifras_clave) y sus tests en tests/v17;
  - registro de subagentes con tope de 4 millones por fase;
  - la guarda de salidas cerradas deja abiertas output/v17 y output/v18.

- 2026-10-19 · **Fase 0 cerrada.**
  - docs/v17/referencias_bde.md: índice de 35 documentos y 10 comparaciones con el proyecto.
  - Fichas en docs/v17/referencias/ (Informes Anuales 2023-2025, IEF 2023-2026, 16 documentos del BdE y del BCE, INE).
  - D4 en docs/v17/correcciones.md. Coinciden con su fuente la ECP y el saldo migratorio de 2024, y las cifras del IA2025 (750.000; 240.000 hogares; 92.000 terminadas; 320.000 viviendas previstas, nota 41, p. 147; 7,4 % de no residentes).
  - Inconsistencias internas del BdE anotadas.
- 2026-10-19 · **Fase 1 cerrada.**
  - Inventario: 28 necesidades cubiertas (output/v17/f1/).
  - data/raw/v17/: crédito, titularidad, parque social, oferta y capacidad, y turismo local.
  - Tareas del autor en docs/v18/tareas_autor.md: Notariado, SERPAVI, Catastro por transparencia, el 15 % del Ministerio, OCDE, InsideAirbnb 2019-2020 y licencias.
- 2026-10-19 · Fase 2 (B2, B3 y B5 hechos; B4 tras la fase 3):
  - Inferencia convencional de 112 estimaciones con su distorsión (output/v17/lectura_bde/tabla_comparativa.md): 36 publicables, 30 con reserva, 26 no fiables y 20 no recalculadas.
  - Medidas de referencia del BdE (output/v17/lectura_bde/medidas_referencia/).
- 2026-10-19 · Fase 3 (en curso):
  - apoyo cuantitativo a D3 (output/v17/d3/);
  - tres auditores (demanda y precios; oferta y titularidad; regulación y ayudas) con el encargo docs/v17/brief_f3_auditoria.md.

## Siguiente
- Cerrar la fase 0 (referencias_bde.md y tabla de comparación), la fase 2 (B4-B5) y la fase 3 (auditoría).

## Subagentes y tokens

Generada por src/v17/registro_subagentes.py (fuente: docs/v17/subagentes.csv). Tokens aproximados según el informe de cada subagente. Tope por fase: 4.000.000 (parada E).

| Fecha | Fase | Rol | Tarea | Tokens | Ficheros |
|---|---|---|---|---|---|
| 2026-10-19 | F0 | lector-literatura | INE demografía y comprobación D4 | 111.859 | docs/v17/referencias/ine_demografia.md; docs/v17/correcciones.md; output/v17/f0/ine_demografia.json |
| 2026-10-19 | F0 | lector-literatura | documentos BdE y BCE | 271.318 | docs/v17/referencias/bde_bce_documentos.md; output/v17/f0/bde_bce_documentos.json |
| 2026-10-19 | F1 | adquisidor-datos | crédito y compras | 97.021 | data/raw/v17/credito/; docs/v17/fuentes/credito.md |
| 2026-10-19 | F1 | adquisidor-datos | titularidad y parque social | 154.638 | data/raw/v17/titularidad/; data/raw/v17/parque_social/; docs/v17/fuentes/ |
| 2026-10-19 | F1 | adquisidor-datos | oferta, capacidad y turismo local | 94.325 | data/raw/v17/oferta_capacidad/; data/raw/v17/turismo_local/; docs/v17/fuentes/ |
| 2026-10-19 | F2 | modelizador | inferencia series, V8, V9, V12 | 169.777 | src/v17/f2_inferencia_series_v8_v9_v12.py; output/v17/lectura_bde/series_v8_v9_v12/ |
| 2026-10-19 | F1 | adquisidor-datos | oferta y turismo (cierre de la descarga del Censo en segundo plano) | 756 | - |
| 2026-10-19 | F3 | modelizador | D3 cuantitativo (demografía, general o local, factibilidad) | 179.305 | src/v17/d3_cuantitativo.py; output/v17/d3/ |
| 2026-10-19 | F2 | modelizador | inferencia micro V15-V16 | 273.700 | src/v17/f2_inferencia_v15_v16_micro.py; output/v17/lectura_bde/v15_v16_micro/ |
| 2026-10-19 | F0 | lector-literatura | Informes Anuales e IEF del Banco de España | 439.510 | docs/v17/referencias/bde_informes.md; output/v17/f0/bde_informes.json |
| 2026-10-19 | F3 | auditor | auditoría regulación y ayudas (topes, turística, ayudas; D3-4) | 289.072 | output/v17/auditoria/ (regulacion_ayudas) |
| 2026-10-19 | F3 | auditor | auditoría oferta y titularidad (6 filas; D3-2, D3-3) | 291.660 | output/v17/auditoria/ (oferta_titularidad) |
| 2026-10-19 | F3 | auditor | auditoría demanda y precios (6 filas; D3-1) | 399.678 | output/v17/auditoria/ (demanda_precios) |
| 2026-10-19 | F3 | lector-literatura | lectura completa de estudios sobre no beneficiarios (P1) | 222.238 | docs/v17/referencias/no_beneficiarios.md |

| Fase | Tokens de subagentes |
|---|---|
| F0 | 822.687 |
| F1 | 346.740 |
| F2 | 443.477 |
| F3 | 1.381.953 |

Total V17: 2.994.857 tokens

<!-- fin subagentes -->
