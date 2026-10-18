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
  - Cambian los valores críticos de 4 CCAA (m1b_gsadf_ccaa_11, 16, 18 y 19).
  - **Aplicada** por orden del autor (2026-10-18), tras comprobar que no hace falta ningún dato sellado: M1B lee solo los paneles *_train de M0.
    - Dos copias completas de M1B: la original reproduce al byte output/v6/M1B; la corregida solo cambia el GSADF y lo que deriva de él (ERRATA, fila v6-1.0).
    - En cifras_clave solo cambian los 4 valores críticos.
- src/v16/q9_burbuja.py (Q9-g) usa su propio bootstrap salvaje, no `ar_fit`.
- tests/v7_2/test_v72.py exige que la reverificación coincida 14 de 14 y que la ficha conserve «Tampoco se puede afirmar que NO la haya».

## Estudio de estabilidad (src/v16/b4_gsadf_estabilidad.py → output/v16/b4_gsadf/)

| Réplicas | Semillas | Cocientes sin ajuste | Cocientes tras BH (familia de 8) | Cocientes tras BH (familia de 4, sensibilidad) | Tipos sin ajuste | Niveles tras BH | CCAA tras BH | CCAA sin ajuste |
|---|---|---|---|---|---|---|---|---|
| 499 | 5 | 1-2 | **0-1** | **0-1** | 0 | 0 | 0 | 5-6 |
| 1.999 | 5 | 1-2 | 0 | **0-1** | 0 | 0 | 0 | 6 |
| 4.999 | 5 | 1-2 | 0 | 1 | 0 | 0 | 0 | 6 |

- **Elegido: 4.999**, el menor número con todos los recuentos ajustados idénticos en las 5 semillas.
- El recuento de cocientes sin ajuste no se estabiliza con ningún número de réplicas, porque la serie valor tasado/IPC alquiler tiene p ≈ 0,052, en el borde. Se publica el de la semilla original y se declara.

## Resultado (regeneración con 4.999 réplicas y la semilla original)

| Cifra | Antes (1.0) | Después |
|---|---|---|
| V72-GSADF-ratios-p05 | 3 | 1 (IPV/renta, p = 0,010; valor tasado/IPC alquiler en el borde, p = 0,053) |
| V72-GSADF-ratios-bh (familia de 8) | 0 | 0 |
| V72-GSADF-ratios-bh4-sens (nueva, sensibilidad) | — | 1 |
| V72-GSADF-tipos-p05 | 0 | 0 |
| V72-GSADF-niveles-bh | 2 | 0 (valor tasado p = 0,045; BH 0,091) |
| V72-GSADF-ccaa-bh | 7 | 0 (6 sin ajuste) |
| V72-GSADF-ccaa-v6 | 0 | 0 (no se regenera; ver ERRATA, fila v6) |
| V72-GSADF-rev | 14 | 14 |
| R1B-G-ccaa | 7 [7; 19] | 0 [0; 6] |
| R1B-G-0 … G-8 (valor crítico en min) | ver ERRATA.md | estadísticos sin cambio |

**Comprobación de alcance.** Se comparó cifras_clave con la copia de antes de B-4.
- Solo cambian estas filas:
  - las R1B-G-* (valor crítico y rótulo con p y BH);
  - las V72-GSADF-* (valor y fuente: «4.999 réplicas»);
  - una fila nueva, V72-GSADF-ratios-bh4-sens;
  - las de V8 del punto 2 de B-4.
- No cambia ninguna otra cifra, capa ni periodo.
- Tamaño del contraste (R1B-G-tam, R1B-G-tam-corr): sin cambio.
- Textos regenerados: una_pagina, lo_que_sabemos, policy_brief, que_cambio, working_paper, las fichas de burbuja de v5 y de V7.2, el verificador V7.1, consulta y lo ya visto de V16.

**Conclusión.** «No se puede afirmar que haya una burbuja ni que no la haya» (ANALIZADA, NO CONCLUYENTE, C4) se mantiene. Pierde apoyo la frase «los niveles y algunas series regionales son explosivos tras BH», que se retira. El «tampoco que no la haya» se apoya ahora en que no rechazar no demuestra alineación con los fundamentales: la potencia es baja con T = 78 y hay series exuberantes sin ajuste.
- Navarra: el IPV usa ya 2007T1-2026T2. El valor tasado falta en 2015-2018 y usa el tramo continuo más largo (2007T1-2014T4), como antes.
