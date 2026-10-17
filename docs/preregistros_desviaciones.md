# Cambios posteriores a los commits de pre-registro (una entrada por versión)

Este documento se publica en metodologia/desviaciones_preregistros.md con `make publicacion`. Las huellas y fechas salen de git y están en docs/preregistros.md y docs/preregistros_ficheros.csv. Se escribió el 2026-10-17 sin estimar nada ni reabrir ninguna muestra sellada. La cronología de las evaluaciones procede de docs/v2/holdout_accesos.md, la copia versionada del registro de accesos de src/holdout.py.

## v2: `data/processed/v2/train/_sellado.json` (pre-registro prereg-v2, commit 910c42a, 2026-10-10T07:13:42Z)

**El cambio:**
- Commit fd2559a, 2026-10-10T07:20:44Z: «v2: infraestructura común…, holdout sella todo t ≥ 2024Q3».
- En `src/holdout.py`, el sellado temporal pasó de `2024Q3 ≤ t ≤ 2026Q2` a `t ≥ 2024Q3`.
- En nacional_q_v2, la muestra de entrenamiento pasa de 119 a 118 trimestres y la sellada, de 8 a 9.
- Es el único cambio del fichero.

**Motivo**, según docs/v2/decisiones.md (2026-10-10, «Corrección de holdout»):
- nacional_q_v2 traía una fila 2026Q3 casi vacía que había quedado en entrenamiento.
- El pre-registro (docs/v2/hipotesis.md) fija el entrenamiento hasta 2024Q2 («Panel … 2008Q1-2024Q2») y la evaluación en 2024Q3-2026Q2.
- Una fila posterior a 2026Q2 en el entrenamiento era una fuga de datos futuros. El cambio hace que el código cumpla lo que ya decía el pre-registro.

**Cronología.** El cambio es anterior a todas las evaluaciones selladas de v2:
- H1: 07:45:45Z;
- H2: 07:53:07Z;
- H6: 09:23:21Z;
- H7: 09:56:04Z;
- H3-3a, H3-3b, H3-1 y H3-2 (v3): desde 13:42Z.

Ningún modelo de v2 se entrenó con el fichero original, porque los scripts de rama se escribieron después de fd2559a. Todas las evaluaciones usaron la muestra modificada.

**Efecto en resultados publicados: ninguno.**
- Las evaluaciones miden 2024Q3-2026Q2 (en el registro, H1 «tmax: 2026Q2» y H7 «fin: 2026Q2»), así que la fila 2026Q3 no entra en ninguna métrica.
- En esa fila están vacías las variables de resultado (IPV, IPC de alquiler y demás). Con la muestra original habría quedado en entrenamiento sin resultado y no habría entrado en ninguna estimación.
- H6 usa panel_prov_q, que el cambio no tocó. De H6 depende la única cifra de cifras_clave ligada a una evaluación sellada de v2: R1B-S-BP-H6-RV, capa C4.
- No procede entrada en ERRATA.

## v6: `output/v6/M0/sellado_info.json` (pre-registro prereg-v6, commit a33c167, 2026-10-11T08:47:34Z)

**El cambio:**
- Commit 42cf68b, 2026-10-11T17:48:45Z: «v6.1 K4b: doble implementación independiente de las 15 cifras».
- Cambia el sha256 de dos paneles sellados: `prov_contratos_nuevos_anual` y `mun_contratos_anual`.
- También cambia el recuento de entrenamiento de contratos (de 1.235 a 917 observaciones, de 562 a 440 unidades).

**Motivo**, según docs/v6_1/decisiones.md D4 y ERRATA.md (2026-10-11, v6, K4a-02):
- Se corrigió un error de las fianzas de Incasòl, que sumaban año completo, acumulados y trimestres (contratos × 3,3).
- `m0_run.py` volvió a escribir esos dos paneles sin abrirlos y actualizó sus huellas.

**Cronología.** El cambio es posterior a todas las evaluaciones selladas de v6:
- M4: desde 2026-10-11T10:41:14Z;
- líneas base K1: hasta 17:45:04Z.

Ninguna de las 160 entradas v6 del registro abre un panel de contratos. Las evaluaciones usaron alquiler y compra provincial, municipal y por distrito, y compra trimestral. Los contratos nuevos no se pudieron modelizar en v6 (N ≈ 15).

**Efecto en resultados publicados: ninguno.**
- Ninguna evaluación sellada usó los paneles modificados; las que hubo se hicieron con la muestra original.
- ERRATA.md ya recoge K4a-02: solo afecta al descriptivo de contratos nuevos de M1A y no cambia ninguna cifra de cifras_clave ni ningún modelo evaluado.

## v9: `docs/v9/hipotesis.md` (prereg-v9, commit 2977349)
Commit 8075f52 (2026-10-15): solo añade el hash del propio commit pre-registrado a la sección «Sellado». Un fichero no puede contener el hash de su commit. No cambia ninguna hipótesis, especificación ni cifra: sin efecto.

## v9-a1: `docs/v9/hipotesis_addendum_a1.md` (prereg-v9-a1, commit 9cb2200)
Lo sustituye la versión de prereg-v9-a1b (commit 4639772, tres minutos después y antes de cualquier estimación de V9), que es la vigente y no ha cambiado: sin efecto.
