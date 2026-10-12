# Inventario del repositorio, validaciones selladas, calidad y consumo

Fecha de la consulta: 2026-10-12. Tarea de solo lectura: no se han ejecutado modelos ni `make`, no se ha leído `data/sealed`, y el único fichero escrito es este. Las secciones B, C, E y F no se pidieron.

## A. Repositorio

**Estructura.** `src/` tiene los módulos de v1 y v2 en la raíz (`build_dataset*.py`, `fetch_*.py`, `f2_nacional.py`…, `holdout.py`, `econ_utils.py`) y una subcarpeta por versión (`v2`, `v3`, `v4`, `v5`, `v5_1`, `v6`, `v6_1`, `v6_2`). `output/` tiene subcarpetas `v2` a `v6_2` más `tablas/`, `f2`–`f6` y los registros de búsqueda. `docs/` tiene `v2` a `v6_2` (con `v5_1`), más `estado_proyecto/` (solo `_notas_entorno.md` antes de esta nota). `archive/` contiene solo `README.md` y `output/`. El árbol de trabajo estaba limpio en el momento de la consulta.

**Commits de cierre** (`git log --oneline | grep -i cerrad`):

| Versión | Commit | Mensaje (resumen) |
|---|---|---|
| v4 | 9673a4c | cerrada: make all ×2 sin red en clon limpio |
| v5.0 | cc69e02 | cerrada: make all ×2, md5 idénticos salvo tiempos.json |
| v5.1 | bac2fda | cerrada: make all ×2, tareas del autor |
| v6.0 | 08d7629 | cerrada: make all ×2, md5 idénticos |
| v6.1 | 7a63f9f | cerrada: make all ×2, salidas propagadas |
| v6.2 | 462ebf1 | cerrada: make all ×2 en clon limpio; diferencias explicadas |

No hay commit «cerrada» para v2 ni v3 con ese patrón.

**Etiquetas** (`git tag -l` y `git rev-list -n1`; solo locales, según el enunciado):

| Etiqueta | Commit |
|---|---|
| prereg-v2 | 910c42a |
| prereg-v3 | 204c073 |
| prereg-v5 | 8803f04 |
| prereg-v6 | a33c167 |
| v5.0 | cc69e02 |
| v5.1 | bac2fda |
| v6.0 | 08d7629 |
| v6.1 | 7a63f9f |
| v6.2 | 462ebf1 |

**Makefile.**
- `all`: `data clean models report`.
- `data`: descarga por fuentes (`FETCH`).
- `clean`: `build_dataset.py`, `build_dataset_v2.py` y `holdout.py build`.
- `models`: `MODELS` (puntos de entrada de v2) y después `MODELS_V3`, `V4`, `V5`, `V6`, `V6_2`, `V6_1`. Se ejecutan en serie con `flock`.
- `report`: `src/report.py` y luego `verificador`.
- `check`: `ruff check src tests`, `pytest -q tests`, `v3/check_texto.py`, `v5/check_v5.py` y `v6/check_v6.py`.
- `verificador`: `v3`, `v4` y `v5` `verificador.py`.
- `distclean`: borra `data/processed/*` y `output/*`.

**Órdenes de ejecución:**
- V3: `pa_run pb_run pot_run gl_run c1_run c3_run holm_v3 pd_run`.
- V4: `m0_run m2_run m1_run m3_run m4_run m7_run m5_run`.
- V5: `r1t r1c r1a r1b a23 a4 a5 a5_validacion a5_hechos b1 b2 b3_potencia b3 b4 ca cb cc d1 d2`, después `../v5_1/t1`–`t4`, `e_hechos`, `cifras_clave`, `d3_run`, `cifras_clave`, `render`.
- V6: `m0_run m1a_run m1b_run m2_run m3a_run m3a_bayes m3a_dl m3a_informe m3b_run m4_run`.
- V6_2: `l3_deficit l3_ficha l1_verifica`. El Makefile lo sitúa antes de V6_1.
- V6_1: `k1_run k2_inmigracion k3_run k6_fichas k4b_run ../v5/cifras_clave ../v5/render k4b_comparar k4c_cifras k4d_docs ../v6_2/l5_publicables`.

**Tiempos de `make all`.** README_REPLICACION.md dice «≈2 h 10 min» y registra 7.564 s y 7.776 s (v6.0), 7.498 s y 6.947 s (v6.1). docs/v6_2/estado.md registra 7.928 s y 8.054 s. Usa el punto como separador de miles, así que «7.564 s» son unos 7.564 segundos, unas 2 h 6 min. Con esa lectura coincide con «≈2 h 10 min». Conviene escribirlo sin ambigüedad. La mayor parte del tiempo es v6 M3 (ML y deep learning).

**Tests.** `tests/` tiene 52 funciones `test_` en 10 ficheros, más `tests/doble_impl/` con 3:
- `test_ba_h1_dryrun.py` (1): simulacro de H1.
- `test_bm_h7_sellado.py` (7) y `test_bp_h6_sellado.py` (7) y `test_bv_h2_sellado.py` (2): sellado de H7, H6 y H2 (por nombre).
- `test_check_texto.py` (3): control de texto v3.
- `test_k4a_cifras.py` (10) y `test_k4a_paneles.py` (7): unicidad de ids y claves, rangos y cifras de K4a.
- `test_k4c_cifras.py` (2) y `test_l5_cifras.py` (3): cifras de K4c y L5.
- `test_v2_common.py` (10): utilidades comunes de v2.
- `tests/doble_impl/test_doble_impl.py` (3): doble implementación de K4b/L2.

**Utilidades reutilizables.**
- `src/econ_utils.py`: `load_nacional`, `common_sample`, `ols_hac`, `tabla`, `df_md`, `tabla_md`, `dols`, `diagnostics`, `chow`, `bai_perron`, `dm_test`, `holm`. Clase `Registry` (registro de especificaciones con control de falsos descubrimientos).
- `src/holdout.py`: `provincias_selladas`, `build`, `load_train`, `evaluate`, `load_full`, `distritos_sellados_v3`, `es_sellado_v3`, `sellar_v3`, `sellar_fuente_v3`, `evaluate_v3`, `provincias_selladas_v6`, `municipio_sellado_v6`, `distrito_sellado_v6`, `sellar_v6`, `evaluate_v6`. Registra cada acceso.
- `src/v3/check_texto.py`: control de léxico valorativo y de promoción de capa en los textos v3.
- `src/v5/check_v5.py`: plantillas sin marcadores, capa y fecha en `cifras_clave.csv`, y suma provincial = nacional.
- `src/v6/check_v6.py`: validación v6 separada de v2, ninguna causalidad desde SHAP o importancias, y `medida_precio` en cada resultado de compra.
- `src/v5/render.py`: rellena las plantillas de entregables con `cifras_clave.csv`.
- `src/v5/cifras_clave.py`: tabla única de cifras clave, de los `hechos.json` y de adaptadores de v4.
- `src/v5/verificador.py`: une las fichas de verificación de v3, v4 y v5, sustituye fichas y aplica la regla de capa C4.

## D. Validaciones selladas

**Reglas en el código.**
- v2 (`holdout.py`): 3 provincias selladas (11, 16, 45) con semilla fija, y el sellado temporal 2024Q3–2026Q2 (8 trimestres). En anuales, años ≥ 2025.
- v3: sellado por distrito, 20 % de los distritos por bloques espaciales (`distritos_sellados_v3`). Además, la última oleada de VUT (2026M05) queda sellada para todas las unidades. Un municipio se sella si ≥ 50 % de sus distritos lo están.
- v6: 11 provincias por bloques de CCAA. Se excluyen las CCAA con provincias selladas en v2 y Ceuta y Melilla. El sellado temporal es 2025 en compra y 2024 en alquiler, para todas las provincias.

**Tabla por versión** (`output/v6/M0/sellado_info.json`, `docs/v2/holdout_accesos.md`, `docs/v3/decisiones.md`):

| Versión | Unidades selladas | Periodos sellados | Nº de aperturas (log) | Contaminación o segundas miradas |
|---|---|---|---|---|
| v2 | 3 provincias (11 Cádiz, 16 Cuenca, 45 Toledo): CCAA 01 y 08. Todas las provincias en la ventana temporal | 2024Q3–2026Q2; anuales ≥ 2025 | 8 aperturas: H1, H2, H3-1, H3-2, H3-3a, H3-3b, H6, H7 | Notas de BA, BV y BM desactualizadas (ERRATA). |
| v3 | Distritos: 20 % (lista en data/processed/v3/sellado_v3). Municipios con ≥ 50 % de distritos sellados. Última oleada VUT 2026M05 | 2026M05 y periodos de la oleada sellada | 0 entradas propias en el log. Se usa `load_full`, que exige las 4 evaluaciones de v2 | O1 (decisiones v3): `describe()` global sobre el VUT incluyó 2026M05; `pot_run` estimó P-C3 con municipios sellados. P-C3 no tiene muestra sellada espacial limpia |
| v6 | 11 provincias: 07, 22, 26, 28, 30, 31, 33, 35, 38, 44, 50 (CCAA 02, 03, 04, 05, 13, 14, 15, 17). Municipios: 593 de 3.063 (compra) y 722 de 3.063 (alquiler). Distritos: 2.136 excluidos de ambos lados | Temporal: compra 2025 (y 2026 en trimestral), alquiler 2024 | 80 aperturas: 53 de M4 y 27 de K1 (D3) | B5 (docs/v6/hipotesis.md): el corte temporal cae en la ventana ya abierta en v2 (8 contrastes). M4 separa (i) provincias selladas en años de entrenamiento y (ii) último año. K1 reabre la muestra v6 con una evaluación por línea base (D3, segunda mirada no confirmatoria). D4: la corrección de Incasòl cambió el sha256 de `prov_contratos_nuevos_anual` y `mun_contratos_anual` (sellados, no evaluados) |

Los ficheros `*_sellado*.json` de v2 y v6 están versionados. `sellado_info.json` da, para `dis_alquiler_anual`, 3.786 de 10.552 unidades selladas (solo 2024). No consta si la unidad es observación o distrito; conviene aclararlo.

**Sin usar en ninguna validación (candidatos a V7):**
- CCAA sin sellado espacial en v2 ni v6: 06 Cantabria, 07 Castilla y León, 09 Cataluña, 10 Comunitat Valenciana, 11 Extremadura, 12 Galicia y 16 País Vasco (7 CCAA). Sus periodos sí están en la validación temporal de v2 y v6.
- Provincias sin sellado espacial: 36 de 01–50 y 51–52 (Ceuta y Melilla), en total 38.
- Periodos futuros: nada de 2026Q3 ni de 2026 anual (el sellado llega a 2026Q2 y 2026M05). Hay que comprobar en `data/raw` si ya existen datos posteriores.
- Municipios y distritos sin sellado: unos 2.470 municipios de compra fuera del sello v6 y alrededor del 64 % de los distritos de alquiler.

Ojo: los periodos de entrenamiento anteriores a las ventanas (2008–2024 según el panel) no son validación, sino entrenamiento. Por eso no sirven para V7 como muestra limpia.

## G. Calidad

**ERRATA.md.** Tiene 11 entradas (2026-10-10 a 2026-10-12):
1. v2: notas de BA, BV y BM desactualizadas sobre la evaluación sellada.
2. v1: orden de texto en la edición de Notariado (`1T2026` antes que `2019-2020`).
3. v4: CSV de 67 MB versionado (contra la regla de 50 MB).
4. v5: ventana Censo 2011–2021 de B1 con un año de terminadas de más.
5. v5–v6: `float_format="%.6g"` en `cifras_clave.csv` redondeaba recuentos ≥ 1 M.
6. v6: Incasòl sumaba año completo, acumulados y trimestres; cuota «>600 €/mes» mezclaba unidades.
7. v5: `fillna(1.0)` en Valencia (SERPAVI sin dato) en A23-A10.
8. v5: el informe citaba mal la fuente del rango de déficit y la constante de la EPA.
9. v4–v6.1: déficit 2021–2024 publicado como hecho C1 pese a depender de una corrección constante.
10. v5–v6.1: cruce por nombre «Valencia/Valéncia» fallaba en SERP2IPVA.
11. v5: referencia a una tabla equivocada en la cifra 8 de la revisión humana.

**Hallazgos pendientes.**
- `docs/v6_1/auditoria.md`, medios abiertos (ver `docs/v6_1/backlog.md`): K4a-04 (min/max con otro sentido en 48 filas), K4a-05 (fianza GVA bruta frente a truncada; cambiaría paneles sellados de v6, coste S), K4c-03 (26 cifras del verificador; el backlog lo llama K4c-26), K4d-07 (cuartiles, tarea del autor).
- Bajos abiertos en la auditoría: K4a-06, K4a-08, K4a-10, R-04, R-05, R-06, K4c-04 y K4c-07.
- `docs/v6_1/backlog.md`, abiertos: K4a-03b (recalcular D2, M), K4b-NR (5 cifras no reconstruibles solo con el texto; anexo metodológico), K4b-dh (mezcla de stock y media anual, S), K4d-ref (50 referencias «cuartil no verificado» y 76 NO VERIFICADA; Scimago devuelve 403, la verifica el autor, S), K2-49 (reestimar inmigración con 49 provincias; exige mirar provincias selladas en v6, L), BK-E3 (ampliar artículos, M), BK-014 y BK-017 (temporada, habitaciones y MESVAL; sin datos oficiales, L).
- `docs/v5/backlog.md`: tabla de unas 90 filas. Ejemplos con coste de datos: BK-003 (titularidad del parque; Catastro no publica), BK-008 (coste de construcción sin fuente verificable), BK-009 (empleo de construcción por territorio), BK-010 (plazos de licencias), BK-011 (SIU inaccesible por el proxy).

**Limitaciones.**
- `docs/limitaciones.md` (48 líneas): secciones por fase, F2 con ecuación nominal, y un bloque de precio real.
- `docs/v3/limitaciones.md` (27 líneas).
- Sección Limitaciones del working paper: `docs/v5/plantillas/working_paper.md` y `output/v5/working_paper.md`.

**Objeciones de revisores sin resolver.**
- `docs/v6_1/carta_respuesta.md`, «No viable» (solo se declaran como limitación): A-04 (recuento de especificaciones entre versiones), A-05 (WCB y paneles municipales), A-06 (intervalos Anderson-Rubin y shift-share), A-09 (publicar ecuaciones del método de traslado), A-13 (muestra futura), P-10 (costes y magnitudes por euro), P-11 (recalcular D2 con T3), P-12 (fecha de publicación de etiquetas). A-02 y A-03 están «aceptadas en parte» con limitación.
- `docs/v6_2/revision.md`, H8 (baja, anexo): A1 no tabula los 8 trimestres de la EPA de 2021 y 2025; A16 depende de la clase A4, que no se reconstruye desde la ficha. Pasa al backlog.

**Tipos de error recurrentes** (de ERRATA y las auditorías):
- Cruces por nombre con tildes o grafías distintas (SERP2IPVA, Valencia/Valéncia, Incasòl).
- Imputaciones silenciosas (`fillna(1.0)` en A23-A10).
- Redondeos al escribir (`%.6g` en recuentos grandes).
- Fechas de ejecución o de edición ordenadas como texto (Notariado) y fechas de descarga usadas como fecha del dato (manifiesto de Censo, B1).
- Ventanas desalineadas (stock a 1 de enero frente a media anual en `dh_2125`; Censo 2021 con fecha de 1-ene).
- Agregados que suman varias veces (Incasòl: año, acumulados y trimestres a la vez).
- Notas de resultados que quedan desactualizadas tras una evaluación sellada.

## H. Consumo

**Tokens de subagentes** (según cada `estado.md`):

| Versión | Total | Desglose (módulo u oleada) |
|---|---|---|
| v2 | 4.909.395 | sin desglose en la línea de resumen |
| v3 | 2.106.329 (de 3,5 M) | por tarea |
| v4 | 1.475.500 (de 2,5 M) | A 408.598; B 439.886; C 589.719; sin asignar 37.297 |
| v5 | 3.093.637 (de 4,2 M) | R 601.209; A 471.653; B 523.477; C 416.137; D 499.772; E 511.524 |
| v5.1 | 660.860 (de 1 M) | por tarea |
| v6 | 1.541.747 (de 2,2 M) | por tarea (M0–M4; M3 el mayor) |
| v6.1 | 1.132.386 (de 1,4 M) | K1 ≈90k; K4b ≈175k; K4a ≈235k; K2 ≈250k; revisor ≈74k; K3 ≈50k; K4c/K4d 139.884; K5 72.773; revisor final 50.799 |
| v6.2 | 462.880 (de 0,6 M) | L1 223.573; L2 129.888; L3 55.691; revisor 53.728 |

**Tiempos de ejecución:** `make all` tarda unas 2 h 6–2 h 12 (ver A). v6.2 registra 7.928 s y 8.054 s.

**Discrepancias detectadas en este inventario:**
1. `tests/doble_impl/test_doble_impl.py` tiene 3 funciones `test_`, pero `docs/v6_2/estado.md` habla de 17 tests. Puede deberse a parametrización; no se ha comprobado.
2. El nombre del pendiente de 26 cifras del verificador es K4c-03 en la auditoría y K4c-26 en el backlog.
3. En `docs/v2/holdout_accesos.md` no aparecen aperturas propias de v3. El control se apoya en `evaluate_v3` y en el sellado por distrito, por lo que el log no registra la muestra v3.
4. «Unidades selladas» de `dis_alquiler_anual` (3.786 de 10.552) mezcla unidades y observaciones según el campo.
