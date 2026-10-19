# V17 · Estado

V17 se ejecuta dentro de V18 (docs/v17/decisiones.md, K0): fases 0-3 y 5; la 4 se integra en la fase 6 de V18. Todo a posteriori.

## Hecho
- 2026-10-19 · Plan guardado (docs/v17/plan.md). Infraestructura:
  - comandos /v17-fase0 … /v17-fase5 y /v17-estado;
  - objetivos make v17_f0 … v17_f5 y v17;
  - check_v17 dentro de make check (rótulo «a posteriori», cifras V17 en C4 con lectura propia, sin promoción en cifras_clave) y sus tests en tests/v17;
  - registro de subagentes con tope de 4 millones por fase;
  - la guarda de salidas cerradas deja abiertas output/v17 y output/v18.

## Siguiente
- Fase 0: referencias del Banco de España, el BCE y el INE.

## Subagentes y tokens

Generada por src/v17/registro_subagentes.py (fuente: docs/v17/subagentes.csv). Tokens aproximados según el informe de cada subagente. Tope por fase: 4.000.000 (parada E).

| Fecha | Fase | Rol | Tarea | Tokens | Ficheros |
|---|---|---|---|---|---|
| 2026-10-19 | F0 | lector-literatura | INE demografía y comprobación D4 | 111.859 | docs/v17/referencias/ine_demografia.md; docs/v17/correcciones.md; output/v17/f0/ine_demografia.json |
| 2026-10-19 | F0 | lector-literatura | documentos BdE y BCE | 271.318 | docs/v17/referencias/bde_bce_documentos.md; output/v17/f0/bde_bce_documentos.json |
| 2026-10-19 | F1 | adquisidor-datos | crédito y compras | 97.021 | data/raw/v17/credito/; docs/v17/fuentes/credito.md |
| 2026-10-19 | F1 | adquisidor-datos | titularidad y parque social | 154.638 | data/raw/v17/titularidad/; data/raw/v17/parque_social/; docs/v17/fuentes/ |

| Fase | Tokens de subagentes |
|---|---|
| F0 | 383.177 |
| F1 | 251.659 |

Total V17: 634.836 tokens

<!-- fin subagentes -->
