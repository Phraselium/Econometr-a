# V16 · Errata del GSADF de V7.2 (B-4, punto 1)

Orden expresa del autor (2026-10-18):
- corregir E1 y E2 en src/v5/r1b_gsadf.py;
- subir las réplicas del bootstrap hasta que p y recuentos sean estables en al menos 5 semillas, probando 1.999 y 4.999 y eligiendo el menor estable;
- mantener la familia BH de 8 para los cocientes, con la de 4 solo como sensibilidad;
- regenerar V7.2 → cifras_clave → una_pagina → publicacion/ → web y consulta, comprobando que solo cambian las cifras GSADF y lo que derive estrictamente de ellas.

## Dependencias (listadas antes de regenerar)

Lista obtenida buscando en src/, tests/ y las plantillas quién lee output/v5/R1B, output/v7_2/gsadf o las cifras R1B-G-* y V72-GSADF-*.

| Paso | Script | Lee | Escribe |
|---|---|---|---|
| 1 | src/v5/r1b_gsadf.py | nacional_q_v2 (src/holdout.py load_full), data/processed/panel_ccaa_q.csv, output/v4/M7 | output/v5/R1B/tablas/gsadf_corregido.csv, gsadf_tamano.json, registro_gsadf.csv |
| 2 | src/v5/r1b_run.py --solo-ensamblar | output/v5/R1B/tablas (donut, sensibilidad y GSADF) | output/v5/R1B/hechos.json (R1B-G-*), fichas_verificador.json, resultado.json, registro.csv |
| 3 | src/v7_2/gsadf_reverifica.py | nacional_q_v2, panel_ccaa_q, gsadf_corregido.csv | output/v7_2/gsadf/reverificacion.csv, registro_reverificacion.csv |
| 4 | src/v7_2/ficha_burbuja.py | reverificacion.csv, gsadf_corregido.csv, output/v5/E/hechos.json | output/v7_2/gsadf/hechos.json (V72-GSADF-*), ficha_burbuja.json, ficha_burbuja.md |
| 5 | src/v7_1/s1_atlas.py (solo la función `verificador`) | output/v7_2/gsadf/ficha_burbuja.json | output/v7_1/fichas/fichas_verificador.json, output/v7_1/verificador_v7_1.md |
| 6 | src/v5/cifras_clave.py | output/*/hechos.json | output/v5/cifras_clave.csv |
| 7 | src/v5/render.py | plantillas docs/v5/plantillas (una_pagina, lo_que_sabemos, policy_brief, que_cambio, working_paper, informe_tecnico) | output/v5 renderizado |
| 8 | `make publicacion` | output/ y docs/ | publicacion/ (una_pagina.md, lo_que_sabemos.md, verificador, cifras_clave.csv), metodologia/ |
| 9 | `make base` (src/v10/base.py) | publicacion/cifras_clave.csv | data/base (tabla de cifras) |
| 10 | `make consulta` (src/consulta/generar.py) | cifras_clave, fichas | consulta/ (preguntas «¿Hay burbuja…?») |
| 11 | `make web` | publicacion/, data/base | web/_site (no versionado) |
| 12 | src/v16/f0_lo_ya_visto.py | cifras_clave (V72-GSADF-*) | output/v16/f0/lo_ya_visto.md |

**No dependen del cambio, aunque se parezcan:**
- src/v6/m1b_lib.py tiene una copia propia de `ar_fit` con el mismo error E1. Produce E-V6-M1B-GSADF-SIG / V72-GSADF-ccaa-v6, con un recuento de 0 de 11.
  - Comprobado en copia, sin escribir en el repositorio: con E1 corregido el recuento sigue en 0, con 499 réplicas y con 4.999 réplicas en 5 semillas.
  - Cambiarían los valores críticos de 4 CCAA (m1b_gsadf_ccaa_11, 16, 18 y 19). No se regenera v6, porque la orden no lo cubre: queda en ERRATA como pendiente de decisión del autor.
- src/v16/q9_burbuja.py (Q9-g) usa su propio bootstrap salvaje, no `ar_fit`.
- tests/v7_2/test_v72.py exige que la reverificación coincida 14 de 14 y que la ficha conserve «Tampoco se puede afirmar que NO la haya».

## Estudio de estabilidad (src/v16/b4_gsadf_estabilidad.py → output/v16/b4_gsadf/)

Resultados en la sección «Resultado», tras regenerar.
