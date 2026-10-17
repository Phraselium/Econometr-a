# Pre-registros internos (etiquetas git)

Generado por `python3 src/v16/preregistros.py --escribir` a partir de git. Cada pre-registro es **interno**: lo fija un commit de la rama de desarrollo y una etiqueta anotada publicada en el remoto, **sin sello de tiempo externo** (no es un pre-registro depositado). La fecha del commit y los sha256 salen de git; la de publicación, de la etiqueta anotada (docs/v16/etiquetas_prereg.csv). `make check` (check_v16) comprueba que los hashes coinciden con git y que los pre-registros vigentes (V15 y V16) no han cambiado.

Forma de citarlo en los textos: «pre-registro interno, fijado en el commit X y publicado como etiqueta el <fecha>, sin sello de tiempo externo».

| Etiqueta | Commit | Fecha del commit (UTC) | Publicada como etiqueta (UTC) | Ficheros (sha256 en el commit) | ¿Igual hoy? |
|---|---|---|---|---|---|
| prereg-v2 | 910c42a | 2026-10-10T07:13:42Z | 2026-10-17T17:42:07Z | `docs/v2/hipotesis.md` `3fa640930bd0f645…`<br>`data/processed/v2/train/_sellado.json` `a9a291f9fbef90c9…` | sí<br>no |
| prereg-v3 | 204c073 | 2026-10-10T13:33:09Z | 2026-10-17T17:42:07Z | `docs/v3/hipotesis.md` `ee40f73e5e68482e…` | sí |
| prereg-v5 | 8803f04 | 2026-10-10T19:11:04Z | 2026-10-17T17:42:07Z | `docs/v5/prereg_B3.md` `0b5d09d9f0ca778d…` | sí |
| prereg-v6 | a33c167 | 2026-10-11T08:47:34Z | 2026-10-17T17:42:08Z | `docs/v6/hipotesis.md` `9c5d9333e70fcbb9…`<br>`output/v6/M0/sellado_info.json` `006ff58397b77003…` | sí<br>no |
| prereg-v7 | 3fad305 | 2026-10-12T12:04:36Z | 2026-10-17T17:42:08Z | `docs/v7/hipotesis.md` `e82d61184dcb3d9d…` | sí |
| prereg-v8 | 91e618b | 2026-10-13T08:00:40Z | 2026-10-17T17:42:09Z | `docs/v8/hipotesis.md` `9e7d28dcb2c21763…` | sí |
| prereg-v9 | 2977349 | 2026-10-15T08:22:29Z | 2026-10-17T17:42:09Z | `docs/v9/hipotesis.md` `845269079a46a6d8…` | no |
| prereg-v9-a1 | 9cb2200 | 2026-10-15T08:32:35Z | 2026-10-17T17:42:09Z | `docs/v9/hipotesis_addendum_a1.md` `22d9eadab98fe39a…` | no |
| prereg-v9-a1b | 4639772 | 2026-10-15T08:35:36Z | 2026-10-17T17:42:09Z | `docs/v9/hipotesis_addendum_a1.md` `58a2cb8fd4aabfba…` | sí |
| prereg-v15 | 542b4fd | 2026-10-17T09:24:18Z | 2026-10-17T17:42:07Z | `docs/v15/preregistro_v15.md` `936868be91c66738…`<br>`docs/v15/preregistro_v15_adenda.md` `2df7459c3e99b793…`<br>`docs/v15/sellado_v15.json` `89f5b3da2d77fbed…` | sí<br>sí<br>sí |
| prereg-v16 | a8304ec | 2026-10-17T16:08:21Z | 2026-10-17T17:42:09Z | `docs/v16/preregistro_v16.md` `2bb1e11b5de7fc60…`<br>`docs/v16/preregistro_v16_adenda.md` `b92dd7d2373f9bbb…`<br>`docs/v16/sellado_v16.json` `127785d007898d16…` | sí<br>sí<br>sí |

## Ficheros cambiados después de su commit de pre-registro

Ninguno pertenece a un pre-registro vigente. Los sha256 completos y los commits posteriores están en [preregistros_ficheros.csv](preregistros_ficheros.csv).

- **prereg-v2** · `data/processed/v2/train/_sellado.json`: fd2559a 2026-10-10 v2: infraestructura común (src/v2_common.py + tests), holdout sella todo t ≥ 2024Q3, make models incluye src/v2
- **prereg-v6** · `output/v6/M0/sellado_info.json`: 42cf68b 2026-10-11 v6.1 K4b: doble implementación independiente de las 15 cifras (5 coinciden, 5 parciales, 5 no reconstruibles)
- **prereg-v9** · `docs/v9/hipotesis.md`: 8075f52 2026-10-15 V9 F2: hash del commit pre-registrado (prereg-v9) en hipotesis.md
- **prereg-v9-a1** · `docs/v9/hipotesis_addendum_a1.md`: 4639772 2026-10-15 V9 F2: re-revisión A1 aprobada; ventana previa de D1a corregida (MDE 0,046) y notas A1-b/A1-c

**Sin efecto en resultados publicados** (detalle por versión en docs/preregistros_desviaciones.md, publicado en metodologia/desviaciones_preregistros.md):

- **v2.** El cambio (fd2559a) es anterior a todas las evaluaciones selladas de v2. Lleva el sellado a lo que ya decía el pre-registro (entrenamiento hasta 2024Q2): una fila 2026Q3 sin variables de resultado sale del entrenamiento. Queda fuera de la ventana evaluada, 2024Q3-2026Q2, y no entra en ninguna métrica. H6 (R1B-S-BP-H6-RV) usa un panel que no cambió.
- **v6.** El cambio (42cf68b) es posterior a todas las evaluaciones selladas de v6. Solo rehace las huellas de dos paneles de contratos nuevos tras la corrección K4a-02 (ERRATA). Ninguna evaluación abrió esos paneles.
- **v9.** Solo añade el hash del commit pre-registrado.
- **v9-a1.** Lo sustituye prereg-v9-a1b.

Ninguno cambia una hipótesis ni una cifra de la versión 1.0, así que no procede entrada en ERRATA.
