# V17 · Estado

V17 se ejecuta dentro de V18 (docs/v17/decisiones.md, K0): fases 0-3 y 5; la 4 se integra en la fase 6 de V18. Todo a posteriori.

## Hecho
- 2026-10-19 · Plan guardado (docs/v17/plan.md). Infraestructura:
  - comandos /v17-fase0 … /v17-fase5 y /v17-estado;
  - objetivos make v17_f0 … v17_f5 y v17;
  - check_v17 dentro de make check (rótulo «a posteriori», cifras V17 en C4 con lectura propia, sin promoción en cifras_clave) y sus tests en tests/v17;
  - registro de subagentes con tope de 4 millones por fase;
  - la guarda de salidas cerradas deja abiertas output/v17 y output/v18.

- 2026-10-19 · Fase 0 (en curso): fichas del INE y comprobación D4 (docs/v17/correcciones.md); 16 documentos del Banco de España y del BCE (docs/v17/referencias/bde_bce_documentos.md). Pendiente: Informes Anuales e IEF.
- 2026-10-19 · Fase 1: inventario (output/v17/f1/); crédito y compras, titularidad, parque social, oferta y capacidad, y turismo local descargados en data/raw/v17/. Pendientes del autor en docs/v18/tareas_autor.md.
- 2026-10-19 · Fase 2 (en curso): encargo común (docs/v17/brief_f2_inferencia.md) y dos modelizadores (micro V15-V16; series y V8, V9 y V12).

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

| Fase | Tokens de subagentes |
|---|---|
| F0 | 822.687 |
| F1 | 346.740 |
| F2 | 443.477 |
| F3 | 179.305 |

Total V17: 1.792.209 tokens

<!-- fin subagentes -->
