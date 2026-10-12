# Estado del proyecto «Vivienda en España» (v1-v6.2): inventario para diseñar la V7

Fecha: 2026-10-12. Inventario de solo lectura, sobre la rama r6.2/main en 462ebf1 (cierre de v6.2). Autor del proyecto: Borja Romero, economista.

**Cómo se hizo.**
- Cuatro escáneres (subagentes haiku) leyeron el repositorio con head, grep y consultas puntuales. No se ejecutó ningún modelo ni se leyó data/sealed.
- El orquestador sintetizó y contrastó los puntos críticos: paneles, sellados y versiones de librerías.
- Las notas de cada escáner están en `_notas_*.md` y se integran aquí como anexos (secciones B-D). Donde el orquestador corrigió algo, se indica con **[corrección]**.

**Advertencia de exactitud.**
- Las cifras de las tablas detalladas se transcribieron de `resultado.json` y de documentos. Las celdas «n/t» no se extrajeron.
- Antes de citar una cifra, consulta `output/v5/cifras_clave.csv`, la única fuente de las cifras publicadas.

---

## 0. Resumen ejecutivo

- **Qué existe.** Seis versiones cerradas (v1-v6.2) y una base de evidencia reproducible: `make all` sin red tarda unas 2 h 10 min, con md5 idénticos en dos ejecuciones. Hay 89 tests en `make check`.
- **Entregables.** Informe técnico, working paper, policy brief, una página y verificador de afirmaciones con 40 fichas. Todas sus cifras salen de una tabla única (`cifras_clave.csv`).
- **Datos.** Los paneles más largos son el **nacional trimestral** (1995-2026) y el **CCAA trimestral** (17 CCAA, 1995Q1-2026Q2; completo desde 2007 en precio, compraventas, extranjeros, IPC alquiler y ocupados).
  - El **provincial** es anual o trimestral, 2002-2024 en los paneles de v2.
  - Los paneles **municipal** y **de distrito** son anuales (2011/2015-2024).
  - **No existen por CCAA en trimestral:** renta, PIB, hogares, crédito, tipo hipotecario, costes y licencias.
- **Modelos.** En v1-v6.2 se probaron muchos estimadores: DOLS, ECM, Johansen, ARDL, FE, CCE, CIPS, 2SLS shift-share, SDiD, DiD, Manski, GSADF, BMA, elastic net, RF, GBM, MLP/GNN, DML, entre otros.
  - **No se estimaron** PMG, DFE ni la cointegración de panel de Pedroni o Westerlund.
  - El **MG** solo aparece en v6, como robustez.
  - **CIPS** se hizo en v1, como raíz unitaria por CCAA (no como cointegración).
  - Ningún resultado alcanzó la capa C3 (efecto identificado).
- **Resultados.**
  - **Hechos C1:** hogares, terminadas, precio, alquiler, contratos nuevos y propiedad.
  - **Cotas C2:** el déficit 2021-2024 (389.361-710.542 viviendas sin bajas), la demanda latente, el stock desplazado por VUT y los hogares proyectados.
  - **Exploratorio C4:** todo lo demás (inmigración, empleo, renta, turísticos, topes, tipos, necesidad, modelos predictivos).
- **Validación.** Hubo tres sellados: v2 (temporal 2024Q3-2026Q2 y 3 provincias), v3 (distritos y la oleada VUT 2026M05) y v6 (11 provincias y los últimos años; 80 aperturas, 27 de ellas segunda mirada en K1).
  - **Panel CCAA trimestral:** nunca se selló, y v1 lo usó entero hasta 2025-2026. Ningún periodo existente de ese panel es muestra limpia.
  - **Única validación limpia posible en V7:** datos que se publiquen **después** del pre-registro de V7 (2026T3 en adelante, o el año 2026).
  - **Validación espacial alternativa:** CCAA o provincias nunca selladas. No es limpia, porque esas unidades estuvieron en el entrenamiento de v1, v2 y v6.

---

## A. Repositorio, versiones, herramientas
### Repositorio
- Rama de trabajo r6.2/main en 462ebf1, «v6.2 cerrada». El remoto es la rama claude/housing-price-spain-econometric-95dhj3.
- Etiquetas locales: prereg-v2, prereg-v3, prereg-v5, prereg-v6, v5.0, v5.1, v6.0, v6.1 y v6.2.
- Etiquetas en el remoto: 0. El envío de etiquetas falla (HTTP 403 o el remoto corta la conexión).
- Commits de cierre:

  | Versión | Commit |
  |---|---|
  | v5.0 | cc69e02 |
  | v5.1 | bac2fda |
  | v6.0 | 08d7629 |
  | v6.1 | 7a63f9f |
  | v6.2 | 462ebf1 |

### Entorno
- Python 3.13.16.
- Librerías instaladas:

  | Librería | Versión |
  |---|---|
  | statsmodels | 0.15.0 |
  | linearmodels | 7.0 |
  | lightgbm | 4.7.0 |
  | xgboost | 3.4.1 |
  | shap | 0.53.0 |
  | econml | 0.17.0 |
  | doubleml | 0.11.4 |
  | torch | 2.14.1+cpu |
  | scikit-learn | 1.9.1 |
  | pandas | 3.0.5 |
  | numpy | 2.5.3 |
  | scipy | 1.18.1 |

- No instaladas: pymc, arviz, numpyro, jax, arch, torch_geometric, bartpy, pysal, libpysal y spreg. En v6, BART y PyMC se sustituyeron por alternativas propias (bootstrap bayesiano de bosque, GraphSAGE implementado en torch); ver output/v6/M3A y M4/notas.

### Tiempos y pruebas
- `make all` sin red, un solo hilo:

  | Versión | Ejecución 1 | Ejecución 2 |
  |---|---|---|
  | v6.0 | 7.564 s | 7.776 s |
  | v6.1 | 7.498 s | 6.947 s |
  | v6.2 | 7.928 s | 8.054 s |

  Unas 2 h 10 min por ejecución.
- `make check`: unos 6 min, 89 tests (pytest), más check_texto, check_v5 y check_v6.

### Consumo de subagentes
| Versión | Tokens | Presupuesto |
|---|---|---|
| v6 | 1.541.747 | 2,2 M |
| v6.1 | 1.132.386 | 1,4 M |
| v6.2 | 462.880 | 0,6 M |

Las cifras de v1-v5.1 están en docs/*/estado.md.

Fecha de la consulta: 2026-10-12. Tarea de solo lectura: no se han ejecutado modelos ni `make`, no se ha leído `data/sealed`, y el único fichero escrito es este. Las secciones B, C, E y F no se pidieron.



**Estructura.** `src/` tiene los módulos de v1 y v2 en la raíz (`build_dataset*.py`, `fetch_*.py`, `f2_nacional.py`…, `holdout.py`, `econ_utils.py`) y una subcarpeta por versión (`v2`, `v3`, `v4`, `v5`, `v5_1`, `v6`, `v6_1`, `v6_2`). `output/` tiene subcarpetas `v2` a `v6_2` más `tablas/`, `f2`–`f6` y los registros de búsqueda. `docs/` tiene `v2` a `v6_2` (con `v5_1`), más `estado_proyecto/` (solo `_notas_entorno.md` antes de esta nota). `historico/` contiene solo `README.md` y `output/`. El árbol de trabajo estaba limpio en el momento de la consulta.

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

**Tiempos de `make all`.** README_REPLICACION.md dice «≈2 h 10 min» y registra 7.564 s y 7.776 s (v6.0), 7.498 s y 6.947 s (v6.1). historico/docs/v6_2/estado.md registra 7.928 s y 8.054 s. Usa el punto como separador de miles, así que «7.564 s» son unos 7.564 segundos, unas 2 h 6 min. Con esa lectura coincide con «≈2 h 10 min». Conviene escribirlo sin ambigüedad. La mayor parte del tiempo es v6 M3 (ML y deep learning).

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

#

---

## B. Datos

**[corrección]** El panel provincial de v2 (`data/processed/v2/train/panel_prov_*`) tiene **49 provincias** porque excluye las 3 provincias selladas en v2 (11, 16 y 45). Los paneles de entrenamiento de v6 (`output/v6/M0/paneles/*_train`) tienen **41** porque excluyen las 11 selladas en v6. No son lagunas de datos.

**Panel trimestral por CCAA desde 2007** (`data/processed/panel_ccaa_q.csv`, 17 CCAA; lo comprobó el orquestador):

| Variable | Periodo | NaN | Observación |
|---|---|---|---|
| IPV INE (general, nueva, usada) | 2007Q1-2026Q2 | 0 % | completa |
| Valor tasado MIVAU | 2007Q1-2026Q2 | 1 % | casi completa |
| Ocupados EPA | 2007Q1-2026Q2 | 0 % | ruptura de base 2021 documentada |
| Compraventas ETDP | 2007Q1-2026Q2 | 0 % | agregado de la serie mensual |
| Transacciones totales (MIVAU) | 2007Q1-2026Q1 | 2 % | — |
| Transacciones de extranjeros (MIVAU) | 2007Q1-2026Q2 | 0 % | — |
| Visados (iniciadas, proxy) | 2008Q1-2026Q2 | 8 % | empieza en 2008 |
| Terminadas (fin de obra, proxy) | 2008Q1-2026Q2 | 5 % | empieza en 2008 |
| IPC alquiler | 2007Q1-2026Q2 | 0 % | — |
| Población total y extranjera | 2007Q1-2025Q1 | 6 % | **interpolada** desde el dato anual (918 filas loglineales) |
| Población EPA | 2007Q1-2026Q2 | 0 % | — |
| **Variables que no existen en trimestral por CCAA** | — | — | PIB y renta (solo anual CCAA, CRE); hogares (solo nacional, ECP 2021+); tipo hipotecario y crédito (nacional; hipotecas provinciales mensuales en el raw sin agregar al panel); paro (no está en el panel; derivable de la EPA); costes (nacional); SERPAVI e IPVA (anual); compraventas al contado (no existen); turísticos (INE experimental desde 2020-08); eventos regulatorios (fichero de eventos, sin dummy trimestral CCAA en el panel v1); llegada neta por CCAA (semestral desde 2023) |

Fecha de la pasada: 2026-10-12. Sin ejecución de modelos. `data/sealed` no consultado. Fuentes: `data/raw/_manifest.csv` (110 ficheros), `_manifest_series_ine_v2.csv` (18.090 series INE, solo agregados), `docs/diccionario_variables.md`, `docs/v6/diccionario.md`, `docs/fuentes_fallidas.md`, `docs/v*/fuentes_fallidas.md`, `docs/v5/solicitudes.md`, `data/processed/*`, `output/v6/M0/paneles/*`.

Leyenda: T = trimestral, M = mensual, S = semestral, A = anual. "Validado" = lo que consta en el diccionario (sí / plausibilidad / no consta).

### 1. Datasets de data/raw

#### 1.1 Nivel raíz (ficheros normalizados `fecha, periodo, serie, valor, unidad, fuente, url, ...`)

| Fichero | Fuente | Descarga (UTC) | Nivel | Frec. | Periodo | Método | Validado | Scripts (src/) |
|---|---|---|---|---|---|---|---|---|
| ine_ipv_80270.csv | INE IPV tabla 80270 | 2026-10-09 | Nac, CCAA | T | 2007Q1–2026Q2 | API | sí | fetch_ine, build_dataset |
| ine_ipv_25171.csv | INE IPV tabla 25171 (base 2015) | 2026-10-09 | Nac, CCAA | T | 2007Q1–2025Q4 | API | sí (robustez) | fetch_ine, ca_run |
| eurostat_hpi.csv / eu_hpi.csv | Eurostat prc_hpi_q | 2026-10-09 / 10-10 | Nac / UE | T | 2005Q4–2026Q2 | API | sí | fetch_eurostat, build_dataset_v2 |
| mivau_valor_tasado_nacional_ccaa_prov.csv | MIVAU Boletín (tabla 35101000) | 2026-10-09 | Nac, CCAA, prov | T | 1995Q1–2026Q2 | XLS | sí | fetch_mivau, build_dataset |
| mivau_valor_tasado_municipios.csv | MIVAU Boletín | 2026-10-09 | Municipio (309 series) | T | 2005–2026T1 | XLS | no consta | fetch_mivau, build_dataset_v2 |
| bde_precio_vivienda_libre.csv | BdE be2507 | 2026-10-09 | Nac | T | 1995Q1–2026Q2 | descarga CSV | sí | fetch_bde, build_dataset |
| vlc_precio_vivienda_libre.csv | Ajuntament de València (CKAN) | 2026-10-09 | Municipio (València) | T | 2021Q2–2022Q1 | API | no consta (fuente primaria sin indicar) | fetch_valencia |
| bis_rpp.csv | BIS | 2026-10-10 | Países | T | 2000–2026T1 | API | no consta | fetch_ue_v2 |
| oecd_house_prices.csv | OCDE | 2026-10-10 | Países | T | 2000–2026-07 | API | no consta | build_dataset_v2 |
| ine_epa_ocupados.csv / _ccaa.csv | INE EPA 65302 / EPA387796 | 2026-10-09 | Nac / CCAA (420 series) | T | 2002–2026T1 | API | sí | fetch_ine, build_dataset |
| ine_epa_hogares.csv | INE EPA 65269 | 2026-10-09 | Nac | T | 2002–2026T1 | API | sí | fetch_ine, k4b_run |
| ine_epa_poblacion_ccaa.csv | INE EPA | 2026-10-09 | CCAA | T | 2002–2026T1 | API | no consta | fetch_ine |
| ine_v2_epa_prov.csv | INE EPA tabla 65345 (ocupados y parados) | 2026-10-10 | Provincia (106 series) | T | 2002–2026T1 | API | no consta | fetch_ine_v2, build_dataset_v2 |
| ine_etdp_compraventas.csv | INE ETDP tabla 6150 | 2026-10-09 | Nac, CCAA (360 series) | M | 2007-01–2026-07 | API | sí | fetch_ine, build_dataset |
| ine_v2_etdp_prov.csv | INE ETDP (régimen y estado) | 2026-10-10 | Provincia (265 series) | M | 2007-01–2026-07 | API | no consta | fetch_ine_v2 |
| ine_ipc_alquiler.csv | INE IPC 290887 | 2026-10-09 | Nac | M | 2002-01–2026-08 | API | sí | fetch_ine, build_dataset |
| ine_v2_ipc_alquiler_prov.csv | INE IPC subgrupo alquiler (tabla 76142) | 2026-10-10 | Provincia (106) | M | 2002-01–2026-08 | API | no consta | fetch_ine_v2 |
| ine_ipva_nacional_ccaa.csv | INE IPVA (59058…) | 2026-10-09 | Nac, CCAA | A | 2011–2024 | API | no consta | fetch_ine |
| ine_ipva_municipal.csv | INE IPVA | 2026-10-09 | Municipio (1.530) | A | 2011–2024 | API | no consta | fetch_ine, extract_serpavi |
| ine_v2_ipva.csv | INE IPVA | 2026-10-10 | Prov. (3.420 series) | A | 2011–2024 | API | no consta | fetch_ine_v2 |
| ine_cnt_pib_oferta_corrientes.csv / _volumen.csv | INE CNT | 2026-10-09 | Nac | T | 1995Q1–2026T1 | API | sí (deflactor) | fetch_ine |
| ine_cnt_demanda_corrientes.csv / _volumen.csv | INE CNT | 2026-10-09 | Nac | T | 1995Q1–2026T1 | API | no consta | fetch_ine |
| ine_cnt_renta_disponible.csv | INE CNT | 2026-10-09 | Nac | T | 1999Q1–2026T1 | API | no consta | fetch_ine |
| ine_v2_cre.csv | INE CRE tabla 80109 (PIB corrientes) | 2026-10-10 | CCAA y provincia (53) | A | 2000–2025 | API | no consta | fetch_ine_v2, build_dataset_v2 |
| ine_ecp_nacional.csv | INE ECP 77023 / 320, 701 | 2026-10-09 | Nac | S (hasta 2020), T (2021+) | 1971–2026-07 | API | sí | fetch_ine, build_dataset |
| ine_ecp_56936.csv / 59585.csv | INE ECP | 2026-10-09 | Nac | T | 2002–2025 / 2025Q2–2026Q3 | API | no consta | fetch_ine |
| ine_ecp_ccaa_paises.csv / _nacionalidad.csv | INE ECP 77023 | 2026-10-09 | CCAA (17) | A / 1 ene | 2002–2025 | API | sí (suma 17 CCAA) | fetch_ine, build_dataset |
| ine_v2_padron_prov_pais.csv / _edad_nac.csv | INE ECP (padrón) | 2026-10-10 | Provincia | A | 2002–2026-01 | API | no consta | fetch_ine_v2, m0_run |
| ine_v2_migraciones_prov.csv | INE EM/EMCR 24420-24421 | 2026-10-10 | Provincia (3.922) | S/A | 2008–2022 | API | no consta | fetch_ine_v2, m2_run |
| ine_migraciones_total_anual.csv | INE EMCR 69687 | 2026-10-09 | Nac | A | 2021–2024 | API | sí (inmig_anual) | fetch_ine |
| ine_migraciones_nacionalidad.csv / _ccaa_nacionalidad.csv | INE EMCR | 2026-10-09 | Nac / CCAA | S | 2023S1–2026S1 | API | no consta | fetch_ine |
| ine_hogares_60131.csv | INE ECP 60131 | 2026-10-09 | Nac | T | 2021Q1–2026Q3 | API | sí (hogares_ecp) | fetch_ine, cb_run |
| ine_v2_hogares_prov.csv | INE ECP hogares | 2026-10-10 | Provincia (265) | T | 2021–2026 | API | no consta | fetch_ine_v2, a4_run |
| ine_v2_hipotecas_prov.csv | INE HPT 76317 (hipotecas constituidas) | 2026-10-10 | Provincia (106) | M | 2003–2026-07 | API | no consta | fetch_ine_v2, ca_run |
| ine_vut_nacional_ccaa_prov.csv | INE Estadística experimental VTE 39364 | 2026-10-09 | Nac, CCAA, prov (268) | M (feb/ago hasta 2024; mayo desde 2024-11) | 2020-08–2026-05 | API | no consta | fetch_mivau, build_dataset |
| ine_v2_vut.csv | INE VTE 39363/39364 | 2026-10-10 | Provincia (8.310 series) | M | 2020-08–2026-05 | API | no consta | fetch_ine_v2, r1a_run |
| ine_vut_valencia_municipio.csv / _provincia.csv | INE VTE | 2026-10-09 | Municipio/prov. València | M | 2020-08–2026-05 | API | no consta | fetch_mivau |
| mivau_visados.csv | MIVAU Boletín 32100500 (PROXY viv. libres iniciadas) | 2026-10-09 | Nac, CCAA | M | 2008-01–2026-06 | XLS | sí (plausibilidad) | fetch_mivau, build_dataset |
| mivau_fin_obra.csv | MIVAU Boletín 32101000 (PROXY viv. libres terminadas) | 2026-10-09 | Nac | M | 2008-01–2026-06 | XLS | sí | fetch_mivau, build_dataset |
| mivau_v2_iniciadas_terminadas_prov.csv | MIVAU Boletín (iniciadas/terminadas) | 2026-10-10 | CCAA (18), prov. | M/A | 1991–2026-06 | XLS | no consta | t1_run, t4_run, build_dataset_v2 |
| mivau_v2_protegida.csv | MIVAU Boletín (protegida) | 2026-10-10 | CCAA (19), prov. | M/A | 1991–2026-06 | XLS | no consta | t1_run, t4_run |
| mivau_v2_suelo.csv | MIVAU Boletín (suelo) | 2026-10-10 | CCAA (18) | T | 2004–2026-04 | XLS | no consta | build_dataset_v2, m3_run |
| mivau_parque.csv | MIVAU Boletín (parque) | 2026-10-09 | Nac, CCAA | A | 2001–2025 | XLS | no consta | t1_run, t3_run |
| mivau_fin_obra / mivau_transacciones_* / mivau_transacciones_municipios.csv | MIVAU Boletín (tx notarios: 34010110, 340101i0, 340101j0/k0) | 2026-10-09 | Nac, CCAA (17), municipio (305) | T | 2004–2026T1 (total), 2007–2026T1 (extranjeros, residencia) | XLS | sí (total, extranjeros) | fetch_mivau, build_dataset |
| eurostat_costes.csv | Eurostat sts_copi_q (índice 2021=100) | 2026-10-09 | Nac | T | 1980–2026T1 | API | sí | fetch_eurostat |
| eurostat_produccion_construccion.csv | Eurostat sts_copr_q | 2026-10-09 | Nac | T | 2005–2026T1 | API | sí | fetch_eurostat, m3_run |
| eurostat_permisos.csv | Eurostat sts_cobp_q | 2026-10-09 | Nac | T | 2000–2026T1 | API | sí | fetch_eurostat |
| eurostat_renta_hogares.csv | Eurostat nasq_10_nf_tr | 2026-10-09 | Nac | T | 1999–2026T1 | API | sí | fetch_eurostat |
| eurostat_empleo_nuts2.csv | Eurostat (empleo NUTS2) | 2026-10-09 | NUTS2 (19) | A | 2008–2025 | API | no consta | fetch_eurostat |
| eurostat_inmigracion_anual.csv | Eurostat migr_imm1ctz | 2026-10-09 | Nac | A | 1998–2024 | API | sí (inmig_anual_eurostat) | fetch_eurostat, m2_run |
| eu_hicp.csv, eu_hicp_rent.csv, eu_income_emp.csv, eu_migr_pop.csv, eu_permits.csv, eu_rates.csv | Eurostat (UE) | 2026-10-10 | Países | A/T/M | 2000–2026 | API | no consta | fetch_ue_v2, ca_run |
| ecb_tipo_hipotecario_es.csv | BCE MIR (nuevas op. vivienda) | 2026-10-09 | Nac | M | 2003-01–2026-08 | API | sí | fetch_ecb, build_dataset |
| ecb_nuevo_credito_vivienda_es.csv / ecb_stock_credito_vivienda_es.csv | BCE MIR / BSI | 2026-10-09 | Nac | M | 2003-01–2026-08 | API | sí | fetch_ecb, build_dataset |
| ecb_euribor1y.csv | BCE Euribor 1 año | 2026-10-09 | Euro área | M | 1994-01–2026-09 | API | sí | fetch_ecb |
| ecb_tipo_oficial.csv | BCE MRR (cambios de tipo) | 2026-10-09 | Euro área | cambios (48) | 1999–2026-09 | API | sí | fetch_ecb |
| ecb_hicp_es.csv | BCE IAPC España | 2026-10-09 | Nac | M | 1996-01–2025-12 | API | no consta (serie termina 2025-12) | fetch_ecb, m0_run |
| bde_tipo_hipotecario_referencia.csv | BdE be1901 | 2026-10-09 | Nac | M | 1973-01–2026-09 | descarga | sí | fetch_bde |
| bde_tipos_hipotecas_nuevas.csv | BdE (tipos hipotecas nuevas) | 2026-10-10 | Nac (6 series) | M | 2003-01–2026-08 | descarga | no consta | fetch_bde_v2 |
| bde_credito_finalidad.csv | BdE (crédito por finalidad) | 2026-10-10 | Nac (14 series) | M | 1992-12–2026-08 | descarga | no consta | fetch_bde_v2, m0_run |
| gva_vut_municipio.csv | Generalitat Valenciana registro turismo (CKAN) | 2026-10-09 | Municipio (495) | M | 2010–2026-10 | API | no consta | fetch_gva, r1a_run |
| gva_padron_extranjeros_municipio.csv | IVE padrón (CKAN, distritos/municipio) | 2026-10-09 | Municipio (543) | A | 2005–2022 | API | no consta | fetch_gva |
| ine_padron_valencia.csv / ine_padron_vlc_nacionalidad.csv | INE padrón València | 2026-10-09 | Municipio (València) | A | 1996–2026-07 / 1998–2022 | API / PC-Axis | no consta | fetch_padron_valencia |
| ine_diccionario_municipios_2026.xlsx | INE diccionario de municipios | — | — | — | 2026 | descarga | — | build_dataset_v2 |
| catastro_urbana_municipios.csv (+ .gz) | Catastro, Datos municipios (Urbano) | 2026-10-10 | Municipio (7.610), prov. | A | 2011-12–2025-12 | descarga | no consta | build_dataset_v2, k4b_run |
| v2_eventos_politica.csv | BOE / boletines (41 eventos) | 2026-10-10 | CCAA, prov., municipio | evento | 2013-06–2026-07 | manual | no consta | build_dataset_v2, build_eventos |
| v2_zonas_tensionadas.csv | BOE/CCAA (318 declaraciones) | 2026-10-10 | Municipio | evento | 2024-03–2026-07 | manual | no consta | build_dataset_v2, build_eventos |
| pdf/notariado_cgn_extranjeros_semestral.csv | Consejo General del Notariado (CIEN, XLSX) | — | Nac (categoría extranjero) | S | 2007S1–2025S2 | PDF/XLSX extraído | sí (validacion) | extract_notariado |
| pdf/notariado_cv_prov_trimestral.csv | Notariado (PDF, CV) | — | Provincia (solo CV) | T | 2018Q1–2025Q4 | PDF extraído | sí | extract_notariado |
| pdf/notariado_cv_municipios_anual.csv | Notariado (PDF, CV) | — | Municipio (solo CV) | A | 2021–2025 | PDF extraído | sí | extract_notariado |
| pdf/notariado_cv_actos_mensual.csv | Notariado (PDF, CV) | — | CV | M | 2019-01–2026-03 | PDF extraído | sí | extract_notariado |
| pdf/registradores_opendata_anual.csv | Colegio de Registradores (OpenData) | — | Nac | A | 2007–2025 | CKAN/PDF | sí (validacion) | extract_registradores |
| pdf/registradores_opendata_compraventas.csv | Registradores (ventanas) | — | nivel no verificado | T | 2007Q1–2026Q1 | CKAN | sí | extract_registradores |
| pdf/registradores_eri_anuario.csv | Registradores, Anuario ERI | — | Nac (% extranjeros) | A | 2016–2025 | PDF extraído | sí | extract_registradores |
| pdf/serpavi_esp_agregado.csv / serpavi_ccaa.csv / serpavi_provincias.csv | MIVAU-SERPAVI (AEAT IRPF), XLSX | — | Nac, CCAA, prov. | A | 2011–2024 | XLSX extraído | sí (validacion) | extract_serpavi |
| pdf/serpavi_municipios_46.csv / serpavi_v2_municipios.csv (+ .gz) | SERPAVI | — | Municipio (46 / 32.402 series) | A | 2011–2024 | XLSX extraído | sí / no consta | extract_serpavi, extract_serpavi_v2 |
| pdf/serpavi_valencia_distritos / secciones.csv | SERPAVI | — | Distrito / sección (València) | A | 2011–2024 | XLSX extraído | sí | extract_serpavi_v2 |
| v2_orig/ (catastro, mivau), gva_orig/ (padrón distritos 2005–2022 zip; VUT histórico 2025; vut_lista_actual) | Originales sin procesar | — | — | — | — | — | — | solo entrada |
| mivau_xls/ (11 XLS: 32100500, 32101000, 33100500, 34010110, 340101d0/i0/j0/k0, 34010210, 35101000, 35103500) | MIVAU Boletín | 2026-10-09 | — | — | — | origen de los CSV anteriores | — | fetch_mivau |
| ine_padron_pcaxis/ (51 ficheros PC-Axis 1998–2019; 00046004/5 y 00046002/3) | INE padrón (PC-Axis) | — | Municipio/València (alcance no verificado) | A | 1998–2019 | PC-Axis | no consta | fetch_padron_valencia |

#### 1.2 Subcarpetas de versiones

| Carpeta | Contenido principal | Fuente | Periodo | Scripts |
|---|---|---|---|---|
| v3/ (23) | airbnb_insideairbnb_agregados (2025-12–2026-09, anuncios activos); hut_registro_turismo_cat (Catalunya, snapshot 2026-10); incasol_fianzas_municipio (138.315 filas, 2007–2026-01, por banda); eff_tenencia_edad (BdE EFF, 2002–2022); ine_ecv_tenencia_edad (2004–2025); eurostat_emancipacion (2004–2025); ine_v3_censo2021 (municipio y sección, 2021); ine_v3_vut_municipio_pct (2020-08–2026-05); ine_v3_vut_seccion (145.101 filas, 2021-02–2026-05); ine_v3_gis_seccion (ADRH/censo, 2019–2025); serpavi_distritos/secciones_nacional (2011–2024); madrid_alquiler_cp (2023–2024, origen no verificado); zonas_tensionadas_v3 (BOE/CCAA); eventos_v3 (8 eventos); cataluna_contencion_rentas_v3 (2020-09–2024-10) | Mixta: INE, BdE, Eurostat, Incasòl (Socrata), HUT Catalunya, Inside Airbnb, BOE | — | k4b_run, l1_verifica, m0_run, r1a_run, fetch_*_v3 |
| v4/ (6) | catastro_solares_municipios (114.065 filas, 2012–2026, municipio); ine_v4_t50256, t50272, t59523, t59529 (INE Tempus); medidas_programas | Catastro, INE | 2006–2026 | m3_fetch, m3_run, l1_verifica |
| v5/ (57) | Tablas CA (ca_*: BdE be0418, ECB, Eurostat demo/ilc), cb_* (AEAT IRPF 2019–2024 y IRPFviv 2024; CGPJ lanzamientos 2013–2025 y series TSJ 1T2026; INE ECV t9997; t59953), cc_* (BOE legislación 1992–2026; Eurostat ilc_lvho07b/c, lvho28), gva_fianzas_2020–2022, a4_mbc_rd1020 y d3_referencias | Mixta | Variable | ca_run, cb_run, cc_run, d3 |
| v5_1/ (2) | ine_t2_t6154.csv (ETDP 6154, transmisiones por título); t1/ | INE | — | T1/T2 |
| v3_orig/ (10) | Originales (C2021 indicadores, censo API, Eurostat json, ine_t39366, ine_t59525, madrid_alquiler_cp_1934258, vut_seccion, GIS) | — | — | — |
| vlc_fuente/ (1) | precio_vivienda-cas.csv (fuente de vlc_precio_vivienda_libre) | Ajuntament València | 2021–2022 | fetch_valencia |

Cómputo del `_manifest_series_ine_v2.csv` (18.090 series, por tabla/fuente, solo agregados): INE VTE 39364 y 39363 (8.310), INE EM/EMCR 24420-24421 (3.922), INE IPVA 59058/59005/59059/59060/59061 (3.420), ECP 77023 población por edad y nacionalidad (795), ECP 77023 población por provincia y país (742), ECP hogares 60133 (265), ETDP 6150 (265), EPA 65345 (106), HPT 76317 (106), IPC alquiler 76142 (106), CRE 80109 (53).

### 2. Paneles procesados

Notas generales: `panel_ccaa_q` y `nacional_q` cubren 1995–2026; el `*_metodo` distingue observado / agregado / interpolado_loglineal / anual_asignado / desestacionalizado_stl; sólo `pob_*` tiene interpolación real (la bandera `_interp` vale 1 sólo para `pob_*`; `compraventas_interp`, `visados_interp`, `terminadas_interp`, `ipc_alquiler_interp` valen 0 en 2007+).

| Fichero | Dimensiones | Periodo | Columnas (resumen) | % NaN relevantes |
|---|---|---|---|---|
| data/processed/nacional_q.csv | 127 × 195 (T) | 1995Q1–2026Q3 | ipv, ipv_nueva/usada, ipv15, p_tasado, p_bde, hpi_eurostat, ocupados(_sa), renta_hog(_real), deflactor, ipc_alquiler(_yoy), credito_nuevo/stock, permisos, costes, prod_constr, visados, terminadas, compraventas(_sa), trans_total/extranjeros, pob_total/extranj, hogares_epa/ecp, tipo_hip, euribor, tipo_bce, tipo_hip_real, inflacion_deflactor, inmig_anual, registradores_*, notariado_cgn_extranj, serpavi | ipv 39; hpi_eurostat 35; visados 43; terminadas 42; compraventas 39; prod_constr 32; credito 26; ocupados 23; renta_hog 13; resto ≤1 |
| data/processed/nacional_a.csv | 28 × 44 (A) | 1998–2025 | ipv, ocupados, pob_extranj, hogares_epa, terminadas, visados, inmig_anual_eurostat, inmig_anual, quiebres 2021, ln_/d_ln_ | inmig_anual 86; visados 43; terminadas 36; ipv 32 |
| data/processed/panel_ccaa_q.csv | 2.142 × 78 (17 CCAA × 126 T) | 1995Q1–2026Q2 | ipv(_nueva/_usada), p_tasado, ocupados, compraventas, trans_total/extranjeros, visados, terminadas, ipc_alquiler, pob_total/extranj/espanola (+_metodo, _interp), epa_pob_total, ln_/d_/d4_ | ipv 38; compraventas 38; trans_extranjeros 38; visados 43; terminadas 41; pob_* 26 (sobre el total); ocupados 22 |
| data/processed/panel_ccaa_a.csv | 408 × 104 (17 × 24) | 2002–2025 | pob_* por origen (total, extranj., española, continentes, UE), ipv, p_tasado, ocupados, compraventas, trans, visados, terminadas, ipc_alquiler, serpavi_vc_mediana, notariado_cgn_extranj, registradores_extranj_pct, *_metodo, *_interp | ipv 21; visados 33; terminadas 25; serpavi 47; registradores_extranj_pct 58 |
| data/processed/panel_ccaa_nacionalidad.csv | 5.610 × 9 (T, CCAA × nacionalidad) | 2002Q1–2026Q3 | inmig_flujo, pob_stock, tipo_registro, serie_ine | inmig_flujo 87; pob_stock 13 |
| data/processed/valencia.csv | 3.610 × 10 (formato largo: territorio, variable, valor, origen, rol, validado, metodo, interp) | 1995Q1–2026Q2 | 23 territorios | sin NaN |
| data/processed/validacion_gva.csv | 12 × 8 (controles) | — | bloque, check, error_max | error_max 42% (esperado) |
| data/processed/v2/train/nacional_q_v2.csv | 118 × 239 (T) | 1995Q1–2024Q2 | versión v2 de nacional_q | ipv 41; visados 46; terminadas 44 |
| data/processed/v2/train/panel_prov_q.csv | 4.410 × 182 (49 cód. prov. × T) | 2002Q1–2024Q2 | p_tasado(_suelo), ipc_alquiler, compraventas_*, hipotecas, iniciadas, terminadas, pob, paro, etc. (+_metodo/_interp) | p_tasado 1; p_suelo 13; compraventas 22 |
| data/processed/v2/train/panel_prov_a.csv | 1.078 × 182 (49 cód. × A) | 2002–2023 | p_tasado, p_suelo, ipc_alquiler, ocupados, parados, compraventas_*, hipotecas_*, iniciadas/terminadas_libres, protegida, pob_*, vut_* | zona_tensionada_share 100; iniciadas 39; terminadas 30; protegida 30; compraventas 23; p_suelo 14 |
| data/processed/v2/train/panel_muni_a.csv | 71.720 × 38 (3.258 municipios × A) | 2002–2023 | serpavi_mediana_vc/vu, serpavi_n_*, p_tasado, trans_total, vut_viviendas, uu_residenciales, ipva_*, zona_tensionada, metodo_*, ln_* | zona_tensionada 100; ipva 88–89; p_tasado 93; trans 92; serpavi_vc 65 |
| data/processed/v2/train/panel_ue_a.csv | 682 × 77 (31 países × A) | 2002–2023 | hpi (BIS, OCDE), precio/ingreso, precio/alquiler, alquiler HICP, permisos, inmig_por_1000 | hpi 25; hpi_oecd 22; precio_ingreso 22 |
| data/processed/v2/train/panel_ue_q.csv, eventos_q.csv, nacional_q_v2 | — | — | eventos_q: 3.150 filas (trimestre × evento, 2002Q1–2024Q2, dummy_vigente) | codigos_ine_* 57 (ámbito nacional) |
| data/processed/v3/sellado_v3.json | Metadatos de partición v3 (fracción 0,2; semilla 20261010; última oleada 2026M05) | — | — | — |

Nota: `panel_prov_a` tiene 49 códigos de provincia distintos (no 52); no se ha verificado cuáles faltan. Los metadatos de partición train/sellado se leen sólo como metadatos (no se ha abierto `data/sealed`).

#### 2.1 Paneles de entrenamiento output/v6/M0/paneles/*_train.csv.gz (M0)

| Fichero | Dimensiones | Periodo | Columnas | % NaN |
|---|---|---|---|---|
| nacional_trim_desc.csv / nacional_anual_a23_desc.csv | nacional, desc. | — | — | — (no leídos en esta pasada) |
| ccaa_ipv_anual_desc.csv, ccaa_seguridad_juridica_transversal_desc.csv | CCAA, desc. | — | — | — (no leídos) |
| prov_compra_anual_train.csv.gz | 410 × 27 (41 prov. × 10 A) | 2015–2024 | ln_pm2_tasado, ln_pm2_registradores, ln_cv_etdp, ln_cv_registradores, share_nueva_etdp, ln_hip_viv_num, share_contado_proxy, share_compra_ext_res_pct, no_res_share_R1A_pct, ln_pob, share_ext_pob, share_20_34, jefatura_proxy_pct, paro_tasa, ln_ocupados_miles, ln_pib_pc, ln_vut, ln_terminadas_libres, ln_iniciadas_libres, bajas_tasa_C_amplia_pct, ln_suelo_pm2_m50k, ln_llegada_total_ext | no_res_share_R1A 81; jefatura_proxy 60; ln_suelo 64; ln_vut 50; ln_llegada_total_ext 30 |
| prov_alquiler_anual_train.csv.gz | 369 × 13 (41 × 9) | 2015–2023 | ln_alq_m2_serpavi_vc, ln_alq_mes_serpavi_vc, ln_n_contratos_serpavi_vc, ln_ipc_alq_idx, d_ln_ipc_alq, ln_ratio_precio_alquiler, rentabilidad_bruta_pct, ln_vut, n_mun_tensionados, n_mun_topes_cat | ln_vut 56; d_ln_ipc 11; resto ≈7 |
| prov_contratos_nuevos_anual_train.csv.gz | 369 × 8 | 2015–2023 | ln_fianza_media_gva_eur, ln_n_fianzas_gva, pct_fianzas_600_incasol, ln_n_fianzas_incasol, ln_ipva_nuevo_idx | 69–97 |
| prov_trim_compra_train.csv.gz | 1.640 × 12 (41 × 4 T × 10 A) | 2015–2024 | ln_pm2_tasado, ln_cv_etdp, ln_ipc_alq_idx, ln_hip_viv_num (+ niveles) | ninguna |
| mun_compra_anual_train.csv.gz | 20.530 × 4 | 2015–2024 | ln_pm2_tasado_mun | 91 |
| mun_alquiler_anual_train.csv.gz | 18.181 × 6 | 2015–2023 | ln_alq_m2_serpavi_mun, tensionada_mun, tope_cat_mun | 19 |
| mun_contratos_anual_train.csv.gz | 18.181 × 7 | 2015–2023 | ln_fianza_media_gva_mun, ln_n_fianzas_gva/incasol, pct_fianzas_600_incasol | 58–95 |
| dis_alquiler_anual_train.csv.gz | 40.673 × 7 (distrito, 41 prov.) | 2011–2023 | ln_alq_m2_serpavi_dis, p25/p75, ln_vut_plazas_dis | serpavi 32; vut 67 |
| prov_estatico.csv, mun_estatico.csv, potencia.csv, cobertura_train.json, hechos.json | estáticos / metadatos | — | — | — |

Los paneles M0 tienen 41 provincias, no 52: el panel de compra y alquiler se limita a las provincias con cobertura en fianzas/SERPAVI.

### 3. Matriz de cobertura (variable × nivel × frecuencia)

Celdas: frecuencia (T/M/S/A) y periodo disponible. "—" = no existe en data/raw ni en processed. "PROXY" = proxy declarado.

| Variable | Nacional | CCAA | Provincia | Municipio | Distrito / Sección |
|---|---|---|---|---|---|
| Precio IPV (INE) | T 2007Q1–2026Q2 | T 2007Q1–2026Q2 (17) | — | — | — |
| Valor tasado MIVAU (p_tasado) | T 1995Q1–2026Q2 | T 1995Q1–2026Q2 | A 2002–2023 (panel_prov_a) | T 2005–2026T1 (309 series) | — |
| Precio BdE (p_bde) | T 1995Q1–2026Q2 | — | — | — | — |
| Notariado (CGN) | S 2007S1–2025S2 (extranj.) | — (CV: M 2019–2026-03) | CV: T 2018–2025T4 | CV: A 2021–2025 | — |
| Registradores (compraventas, anual) | A 2007–2025 | — | — | — | — |
| Registradores (ventanas trimestrales) | T 2007Q1–2026Q1 (nivel no verificado) | — | — | — | — |
| Registradores (ERI, % extranjeros) | A 2016–2025 | — | — | — | — |
| IPC alquiler | M 2002-01–2026-08; T 2002Q1–2026Q2 | T 2002Q1–2026Q2 (17) | M 2002–2026-08 (ine_v2) | — | — |
| SERPAVI (alquiler, €/m²) | A 2011–2024 | A 2011–2024 | A 2011–2024 | A 2011–2024 (32.402 series; 46 mun. en CSV aparte) | Distritos A 2011–2024 (València y nacional); secciones A 2011–2024 (nacional, 398k filas) |
| IPVA (índice alquiler INE) | A 2011–2024 | A 2011–2024 | A 2011–2024 | A 2011–2024 (1.530) | — |
| Fianzas de alquiler | — | CAT (Incasòl, 2007–2026-01); CV (GVA, 2020–2026); MAD, EUS, BAL no disponible | CV/CAT derivado A 2015–2023 | CV/CAT A 2007–2026 (Incasòl por banda) | — |
| Empleo (ocupados) | T 2002Q1–2026Q1 (EPA); desest. (_sa) | T 2002Q1–2026Q1 (17) | T 2002Q1–2026Q1 (106, ine_v2_epa) | — | — |
| Paro (parados) | nac: derivable de EPA (no verificado en el raw); T | CCAA: no verificado | A 2002–2023 (panel_prov_a, parados) | — | — |
| Renta de hogares | T 1999Q1–2026Q1 (Eurostat); INE renta disponible T 1999Q1–2026Q1 | — | — | — | — |
| PIB | T 1995Q1–2026Q1 (INE CNT corr./vol.) | A 2000–2025 (ine_v2_cre, 17 CCAA) | A 2000–2025 (ine_v2_cre, 53 cód.) | — | — |
| Población | T 2002–2025 (ECP, 2021+ trimestral; 1 ene/jul antes); A 1971–2026 | T 2002–2025 (ECP 77023, 1 ene; interp. T2–T4); EPA T 2002–2026T1 | A 2002–2026-01 (ine_v2_padron_prov_pais) | Valencia A 1996–2026 (ine_padron_valencia) | — |
| Llegada neta / inmigración | A 2021–2024 (EMCR 69687); A 1998–2024 (Eurostat); S 2023S1–2026S1 (nacionalidad) | S 2023S1–2026S1 (ccaa × nacionalidad) | A 2008–2022 (ine_v2_migraciones, 3.922 series) | — | — |
| Extranjeros (stock) | T 2002–2025 (ECP701, interp. desde 2021) | T 2002–2025 (ECP701 por CCAA, 17) | A 2002–2026-01 (padrón por país) | A 2005–2022 (GVA, 543 mun.); València A 1998–2022 | — |
| Hogares | T 2002Q1–2026Q1 (EPA; serie principal); T 2021Q1–2026Q3 (ECP 60131, solo nacional, sin retropolación) | — (no trimestral CCAA) | T/A 2021–2026 (ine_v2_hogares_prov) | — | — |
| Tipo hipotecario | M 2003-01–2026-08 (BCE MIR); M 1973–2026-09 (BdE); T mediana (agregado) | — | — | — | — |
| Nuevas hipotecas / crédito | M 2003-01–2026-08 (crédito nuevo y stock BCE); M 1992-12–2026-08 (BdE finalidad, 14 series); M 2003–2026-08 (BdE tipos) | — | M 2003–2026-07 (ine_v2_hipotecas, constituidas) | — | — |
| Compraventas (total) | M 2007-01–2026-07 (ETDP); T agregado | M 2007-01–2026-07 (17 CCAA, ETDP 6150) | M 2007–2026-07 (ine_v2_etdp, 265 series) | — (Notariado/MIVAU municipal, no ETDP) | — |
| Compraventas extranjeros | T 2007Q1–2026Q1 (MIVAU tx extranjeros); Notariado S 2007–2025 | T 2007Q1–2026Q2 (17) | — | — | — |
| Compraventas al contado | — (no hay serie nativa; proxy `share_contado_proxy` en panel prov. anual, NaN 3%) | — | proxy A 2015–2024 | — | — |
| Terminadas (PROXY libres) | M 2008-01–2026-06 (fin_obra); T 2008Q1–2026Q2 | T 2008Q1–2026Q2 (17) | M/A 1991–2026-06 (iniciadas_terminadas_prov) | — | — |
| Iniciadas (PROXY, visados) | M 2008-01–2026-06 (visados); T 2008Q1–2026Q2 | T 2008Q1–2026Q2 (17) | M/A 1991–2026-06 (iniciadas_terminadas_prov) | — | — |
| Licencias de obra (tabla MIVAU) | — (fallido; sin serie nacional reciente) | Endpoint identificado (1002NN30, hasta 2022); no descargado | — (endpoint provincial, sin dato) | — | — |
| Costes de construcción | T 1980Q1–2026Q1 (Eurostat sts_copi_q, 2021=100); sin ICC INE | — | — | — | — |
| VUT (viviendas turísticas) | M 2020-08–2026-05 (INE experimental) | M 2020-08–2026-05 (17) | M 2020-08–2026-05 (ine_v2_vut, 8.310 series); GVA registro M 2010–2026-10 | Municipio: INE 2020-08–2026-05 (8.207 filas); GVA 2010–2026 (495 mun.); HUT Catalunya snapshot 2026-10 | Sección: INE 2021-02–2026-05 (145k filas); distrito València VUT plazas (SERPAVI-dis) |
| Eventos regulatorios | v2_eventos_politica (41, 2013–2026-07, ámbito nac./CCAA/prov.) | Id. (CCAA en v2_eventos) | Codigos INE provincia (12 códigos en eventos) | v2_zonas_tensionadas (318 declaraciones, 2024-03–2026-07; municipio) | — |
| Catastro | A 2011-12–2025-12 (agregado) | A 2011–2025 (por CCAA, derivable) | A 2011–2025 (derivable, catastro_urbana) | A 2011–2025 (7.610 cód.); solares A 2012–2026 (v4) | — |

Observación de cobertura: la mayoría de las variables de vivienda son de nivel nacional o CCAA; provincial es sólo para INE (EPA, ETDP, IPC, IPVA, hipotecas, padrón, PIB CRE, VUT), SERPAVI y Catastro; municipal sólo para valor tasado, SERPAVI, IPVA, VUT, Catastro, GVA (CV) y fianzas (CAT y CV). Notariado y Registradores no tienen cobertura territorial completa (Notariado sólo CV a nivel municipal y provincial).

### 4. Panel trimestral CCAA desde 2007 y panel anual provincial

#### 4.1 Trimestral por CCAA (panel_ccaa_q, 17 CCAA × 2007Q1–2026Q2, 78 cols)

Completas (NaN 0% desde 2007Q1, observadas o agregadas):
- ipv, ipv_nueva, ipv_usada (INE IPV, 2007Q1–2026Q2)
- trans_extranjeros (MIVAU, 2007Q1–2026Q2)
- compraventas (ETDP suma 3 meses; NaN 0%, sin interpolación)
- ipc_alquiler (INE IPC; NaN 0% desde 2002Q1)
- ocupados (EPA; NaN 0% desde 2002Q1, cambio base 2021 documentado)
- epa_pob_total (EPA, NaN 0%)

Con huecos menores (NaN 1–8%):
- p_tasado (1%, MIVAU 1995Q1–2026Q2)
- trans_total (2%, 2004Q1–2026Q1; no cubre 2026Q2)
- terminadas (5%, 68 filas NaN; proxy MIVAU)
- visados (8%, 102 filas NaN; proxy MIVAU, no visados CSCAE)

Interpoladas o asignadas (no observadas trimestralmente):
- pob_total, pob_extranj, pob_espanola (6% NaN; 2002Q1–2025Q1): 918 filas con `interpolado_loglineal` (bandera `_interp`=1), 323 filas `anual_asignado`; el último dato es 2025Q1, no llega a 2026.
- compraventas_interp, visados_interp, terminadas_interp, ipc_alquiler_interp: bandera presente pero valor 0 en 2007+; son agregados, no interpolaciones.
- Las columnas `*_metodo` distinguen la transformación; sólo pob_* usa interpolación.

No existen trimestrales por CCAA en el panel (sólo nacional o anual/semestral):
- PIB por CCAA (sólo anual, ine_v2_cre)
- Renta de hogares por CCAA (no hay serie Eurostat/INE trimestral por CCAA)
- Hogares por CCAA (ECP 60131 sólo nacional; ine_v2_hogares_prov es provincial)
- Hipotecas/crédito por CCAA trimestral (sólo provincial mensual en ine_v2_hipotecas, o nacional BCE/BdE)
- Tipo hipotecario por CCAA (sólo nacional)
- Costes de construcción por CCAA (sólo nacional, Eurostat)
- Licencias de obra (no descargadas; intento fallido)
- Notariado y Registradores por CCAA trimestrales (Notariado CV mensual sólo para CV)
- Parados por CCAA (no consta en el panel)
- SERPAVI y IPVA por CCAA (sólo anual)

#### 4.2 Anual provincial (panel_prov_a, 49 códigos, 2002–2023)

Hay 49 códigos de provincia distintos en el fichero, no 52. Completas o casi (NaN ≤5%): p_tasado (1%), hipotecas_n e importe (5%), ipc_alquiler, ocupados, parados, pob_total, pob_extranj.

Con huecos relevantes:
- p_suelo (14%), compraventas_* (23%), terminadas_libres (30%), protegida (30%), iniciadas_libres (39%).
- zona_tensionada_share (100%, sin datos en el panel; ver v2_zonas_tensionadas a nivel municipal).

Interpolaciones: `panel_prov_q` (2002Q1–2024Q2) lleva banderas `_metodo` e `_interp` por variable; `panel_prov_a` no tiene banderas de interpolación en su versión anual.

Presentes además en panel_prov_a (verificado por columnas): parados, hipotecas_n/importe, vut_viviendas, serpavi_* (mediana y nº inmuebles vc/vu), ipva_indice/var, pib_prov, pib_pc, y sus versiones ln_ / d_ln_. Verificado: panel_prov_a no tiene columnas `_interp` ni `_metodo` salvo `vut_viviendas_metodo`.

Ausentes en provincial anual del panel: Notariado (sólo CV en su PDF), Registradores (sólo nacional o agregado CCAA), renta de hogares (no hay), costes de construcción (sólo nacional), licencias de obra (no existen).

Paneles de 41 provincias (output/v6/M0, 2015–2024/2023): cobertura más corta; el panel de compra incluye pm2 tasado, cv ETDP, hipotecas y tasa de paro; el de alquiler incluye SERPAVI 2015–2023.

### 5. Fuentes fallidas y solicitudes pendientes (compacto)

Fallidas (sin fichero o sin acceso verificado):
- MIVAU licencias de obra, nacional o provincial (Boletín, endpoint sin tabla) y CCAA (serie hasta 2022, no descargada).
- MIVAU SIU (suelo urbanizable, capacidad residencial por municipio): connect_rejected.
- MIVAU ruina, cambios de uso, agregaciones: sin endpoint.
- MIVAU Registro Único de Arrendamientos: 403 (sin datos).
- Catastro titulares persona física/jurídica por municipio o provincia: consulta dinámica (jaxi); sin fichero abierto.
- AEAT IRPF por municipio (capital inmobiliario): consulta dinámica; error TLS en agenciatributaria.es.
- INE: ECH (no existe), renta disponible de hogares trimestral (no existe a nivel hogares), inmigración total trimestral (no publicada), inmigración trimestral por CCAA sin nacionalidad (no localizada); Tabla 69691 (EMCR por CCAA) pendiente.
- INE ICC (índice de costes de construcción): no existe en Tempus.
- INE ECV y EPA tenencia por edad de la persona de referencia; Censo 2021 por edad de la persona de referencia y por sección (CENSOP 463, CENSOPV 8, 404 de la API del censo).
- INE ADRH por sección (redirige), tabla de variaciones del seccionado (no localizada).
- INE VUT por sección en algunas tablas (ver v3 fuentes_fallidas).
- BdE: esfuerzo teórico anual (no encontrado), índices de vivienda 404, carpeta csv 403, EFF microdatos (solicitud), EFF 2014/2017 artículo (404).
- BCE: IAPC España termina 2025-12 (estado E); tipo BCE MRR de fechas de cambio (48 obs.).
- Valencia/GVA: fianzas GVA con bloqueo de proxy (ws_closed) en v3; fianzas CV disponibles en v5 (2020–2026).
- Madrid, Euskadi, Baleares: fianzas sin dato (0 resultados o 404); Barcelona opendata: anti-bot; Google Trends: sin API.
- Portales inmobiliarios (Idealista, Fotocasa, MESVAL): no consultados o privados.
- Registro de Turismo Catalunya con fechas de alta/baja: dataset sin columnas necesarias.
- Inside Airbnb: instantáneas anteriores a 2025-12 no descargadas.
- Notariado: compradores persona jurídica (sin dato); fuera de CV sin cobertura territorial.
- Registradores: compras por personas jurídicas (sin serie).
- Programa electoral y proposiciones de ley (v4 M5a): fuera de alcance, pendientes.

Pendientes de solicitud formal (docs/v5/solicitudes.md, sin respuesta registrada; tarea del autor):
- S1 Catastro: inmuebles residenciales por municipio y naturaleza del titular.
- S2 SIU (MITMA): suelo urbanizable 2016–2025 por municipio.
- S3 AEAT: IRPF capital inmobiliario por municipio.
- S4 Registros autonómicos de fianzas (CAT, CV, Madrid, Euskadi, Baleares).
- S5 Licencias de obra (PEM por m²).
- S6 Registro Único de Arrendamientos (contratos de corta duración).
- S7 INE: tabulación a medida de Censos 2011 y 2021 (hogares, hacinamiento, vacías).
- S8 Ayuntamientos grandes ciudades: plazo medio de licencias.
- S9 Portales inmobiliarios e Inside Airbnb histórico 2012–2016.
- S10 CGPJ y Ministerio del Interior: duración de juicios de desahucio.

---

## C. Modelos estimados

### C.1 v1-v4

Fecha de la tarea: 2026-10-12. Alcance: v1 (output/f2..f6, output/informe.md, docs/revision_f*.md), v2 (output/v2/*, docs/v2/*), v3 (output/v3/*, docs/v3/*) y v4 (output/v4/*, docs/v4/*). Estado tomado de docs/v6_1/historial_conclusiones.md. No se ha ejecutado ningún modelo ni leído data/sealed. Las cifras se transcriben de los ficheros citados; las celdas marcadas «n/t» no se han extraído en esta pasada.

Leyenda de estado: vigente = se mantiene tal cual; matizado = se mantiene con reservas o cambia de lectura; retirado = la cifra o la lectura se ha sustituido. «Sin entrada» = el historial no tiene fila para ese modelo.

### Tabla 1. Modelos y familias

| Versión | id/rama | Pregunta | Mercado | Nivel | Muestra y N | Variable dependiente y transformación | Regresores principales y retardos | Estimador | EE | Coeficientes principales (p bruto / ajustado) | Diagnósticos | Fuera de muestra (RMSE; base; DM) | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | f2 P1 DOLS ±2 | Ecuación de largo plazo del precio real | precio (IPV real) | nacional | 2008T1-2025T4, N=72 | ln IPV real (nivel) | ln ocupados; tipo hipotecario real; ln permisos (ret. 4); ln costes real; dummies trimestrales; adelantos/retardos DOLS ±2 | DOLS | HAC | ln ocupados 1,482 (EE 0,330), p<0,001, Holm <0,001; ln costes −0,660 (0,251), p 0,009, Holm 0,052; tipo 0,002 p 0,782; permisos_l4 0,032 p 0,272 | n/t | n/t | matizado (cambia el signo del empleo según medida; «no concluyente») | output/informe.md §3.1; output/f2/*.md |
| v1 | f2 P1 ECM | Corrección de error de corto plazo | precio | nacional | 2008-2025, N=72 | Δ ln IPV real | ect_l1; Δ ln ocupados; Δ ln costes; Δ ln renta; Δ ln IPV_l1; estacionales | ECM (preferido por R² aj.) | HAC | ect_l1 −0,097 (0,031), p 0,002; Δ ocupados 0,474 (0,174), p 0,006; Δ costes −0,105 (0,054), p 0,054 | Chow, Bai-Perron, CUSUM (output/f2/chow.md, bai_perron.md, cusum.png); estabilidad del ECT | Preferido: RMSE 0,01317; DM vs AR4+q 1,076, p 0,290 (oos_dm.md). Historial dice DM p 0,509: **discrepancia a revisar** | matizado (línea base; no mejora AR(4)) | output/f2/ecm_preferido.md; oos_dm.md |
| v1 | f2 cointegración | Cointegración (EG, Johansen, ARDL bounds) | precio | nacional | 2008-2025 | niveles en log | sistemas definidos en cointegracion.md | EG, Johansen (traza/maxeig), ARDL bounds | n/a | n/t (decisión en output/f2/cointegracion.md) | Johansen y ARDL con rechazos listados | n/a | matizado | output/f2/cointegracion.md |
| v1 | f2 DOLS subperiodos | Estabilidad del DOLS por subperiodo | precio | nacional | subperiodos | ln IPV real | ln ocupados, tipo hip., ln permisos_l4, ln costes | DOLS vs EG | HAC | ocupados 1,298 (0,419) DOLS / 0,866 (0,329) EG (2008-2025) | n/t | n/a | matizado | output/f2/dols_subperiodos.md |
| v1 | f3 P2 panel IV | Inmigración → precio y alquiler (shift-share) | alquiler stock y precio | CCAA (17) | N 306 (IPV), 386 (tasado), 198 (SERPAVI), 391 (IPC alq.) | IPV; valor tasado; alquiler SERPAVI; IPC alquiler (Δ/nivel según fuente) | flujo o cuota de inmigración; FE CCAA y año | MCO y 2SLS shift-share | cluster CCAA (17) | IPC alquiler MCO 0,534 (0,167), p WCB 0,004; 2SLS 0,437 (0,293), p WCB 0,119; IPV MCO −0,454 (0,503); 2SLS −1,615 (1,078), p WCB 0,210 | F 1ª etapa 10,6-54,4; Rotemberg, pretendencias, J de sobreidentificación (output/f3) | n/t en esta pasada | matizado (signo + en alquiler, C4; con población no se distingue de 0) | output/informe.md §4.1; output/f3/panel_principal.md |
| v1 | f3 serie nacional | Inmigración y precio nacional | alquiler, precio | nacional | serie trimestral/anual | niveles y Δ | flujo y stock de inmigración; LP | proyecciones locales (LP); HAC | HAC | n/t (output/f3/nacional_lp.md, nacional_anual.md) | separabilidad, diagnósticos LP | n/t | matizado | output/f3/nacional_lp.md |
| v1 | f4 P3 DOLS oferta | Elasticidad de la oferta (iniciadas) al precio real | oferta (iniciadas libres) | nacional | 2009T4-2025T4, N=63 | ln iniciadas (código visados) | precio real retardado (k=4); ±2 DOLS | DOLS ±2 | HAC | β 1,44 (0,21), IC95 [1,04; 1,85], p H0=0,45 <0,001; terminadas 4,26; permisos 3,11 | n/t | n/t | matizado (descriptivo) | output/informe.md §5.2; output/f4/dols_resultados.md |
| v1 | f4 OLS / 2SLS oferta | Mismo, por otros estimadores | oferta | nacional | 2009T4-2025T4, N=63 | igual | igual; instrumento de renta | MCO estático; Δ4; 2SLS niveles | HAC | MCO estático 1,34 (0,27); 2SLS 2,22 (0,66), IC95 [0,93; 3,52], p 0,007 | Johansen/EG/ARDL en f4/cointegracion.md | n/t | matizado | output/f4/ols_estatico.md; iv_resultados.md |
| v1 | f4 déficit contable | Déficit acumulado 2021-2025 | vivienda (flujo) | nacional | 2021-2025 | viviendas (hogares − terminadas) | contable | descomposición contable | n/a | 866.100 (EPA corregida); 810.936 (ECP) | contraste con BdE (output/f4/contraste_bde.md) | n/a | retirado en esa cifra (v5.1 sin bajas 700.934-757.257; con bajas 763.416) | output/f4/deficit_anual_principal.md; output/informe.md §5.1 |
| v1 | f5 P4 FE | Δ ln IPV vs flujo y cuota de extranjeros | precio (IPV) | CCAA (17) | 2009-2025, N=289 | Δ ln IPV | b1 Δ ln ocupados; b2 Δ cuota extranjeros (pp); b3 Δ ln pob. española; b4 terminadas/1000 hab (t-1) | FE CCAA + año | cluster CCAA; Driscoll-Kraay; wild bootstrap | b2 0,0011 (0,0040), p cluster 0,777, p WCB 0,774; b3 2,170 (1,021), p 0,034; b4 0,0026 (0,0011), p 0,021 | Tendencias (output/f5/tabla_fe_tendencias.md), poolability | n/t | matizado (no concluyente en cuota) | output/f5/tabla_fe_principal.md; output/informe.md §6.1 |
| v1 | f5 CCE | Mismo modelo con factores comunes | precio | CCAA (17) | N=289 | Δ ln IPV | b1-b4 como arriba | CCE-MG y CCE-P (Pesaran 2006) | Pesaran 2006 | CCE-MG b2 0,025 (0,014), p 0,072; CCE-P b2 0,022 (0,011), p 0,040 (sin ajuste; no sobrevive a corrección por búsqueda según revisión) | CD de Pesaran: FE −2,54 (p 0,011); CCE-MG −0,80 (p 0,42); CCE-P −2,32 (p 0,021); CIPS (ver nota) | n/t | matizado (revisión_f5: el CD negativo es artefacto; CCE-MG no valida CCE) | output/f5/tabla_cce.md; cd_pesaran.md; historico/docs/revision_f5.md §3.5-3.6 |
| v1 | f5 CIPS | Raíz unitaria de panel (CIPS, Pesaran 2007) por CCAA | variables de panel | CCAA (17), N=17, T=18 | 2008-2025 | ln IPV, ln ocupados, cuota extranjera (niveles y 1ª dif.) | retardos 0 y 1 | CIPS (test de raíz, no cointegración) | simulado | ln IPV en 1ª dif. CIPS −3,293 (p sim 0,000); ln ocupados 1ª dif. −4,544 (0,000); cuota extranjera en nivel no rechaza | n/a | n/a | matizado | output/f5/cips.md |
| v1 | f6 València | Beta de Δ4 frente a comparadores (valor tasado) | compra (valor tasado) | municipio/provincia València | N≥40 | Δ4 ln valor tasado | comparadores | TWFE / beta por municipios | n/t | n/t (output/f6/beta_todos.md; beta_valencia_vs_comparadores.md) | Chow, Bai-Perron (f6) | n/t | matizado | output/f6/beta_todos.md |
| v2 | BA | Crecimiento del alquiler provincial (H1 demográfica) | alquiler IPC | provincia (49) | 2008T1-2024T2, N=3.185 (H1 trim.) | Δ4 ln IPC alquiler | Δ4 ln pob 20-34; Δ4 ln pob extranjera; Δ4 ln ocupados | MCO FE provincia + trimestre | cluster provincia; WCB Webb 9.999 | pob 20-34 0,149 [0,046; 0,252], p bruto 0,008; pob extranjera −0,018 [−0,054; 0,017], p 0,300; ocupados −0,001, p 0,778. Holm-7 H1 = 1,0 (BS) | Población interpolada (marcada) | RMSE 0,01169 vs AR(4) 0,01244 (DM 0,46); vs ECM v1 0,01417 | matizado (EXPLORATORIO; H1 pasa por Holm 1,0 en BS) | output/v2/BA/resultado.json |
| v2 | BD | Descomposición de crecimiento acumulado (alquiler y compra) | alquiler y precio real de compra | provincia (49) | N alquiler 3.185; compra 3.156 | Δ acumulado | familias de variables; coste de uso | MCO FE M1 y M2, contribuciones | IC por descomposición | alquiler P3-P4 observado 5,66 [4,81; 6,58]; demografía 20-34 0,34 [−0,11; 0,85] (descriptivo) | Sin contrastes | n/a | EXPLORATORIO (descriptivo) | output/v2/BD/resultado.json |
| v2 | BI (H3) | Inmigración vs alquiler/compra (shift-share 2002) | alquiler y compra | provincia (49) | 2009-2021, N=621 | alquiler IPC; valor tasado real | flujo/población de inmigración instrumentada | 2SLS FE provincia + año | cluster provincia; WCB Webb 9.999 | alquiler 3,06 [1,14; 4,98]; compra −1,04 [−6,08; 4,00]; dif. 4,10 [−0,33; 8,52]; p IUT 0,029; Holm-7 H3 = 0,176 (BS) | F 1ª etapa 14,4 en 49 prov. (3,5 en entrenamiento de v6); AR CI alquiler [1,35; 6,0] | RMSE 0,00941 vs AR(4) 0,0107; DM 1,43 | matizado: «cambia la lectura» (MCO invierte el orden; 1ª etapa débil) | output/v2/BI/resultado.json |
| v2 | BM (H7) | ¿Algún modelo de ML/TVP supera AR(4) y ECM v1 a 4 trimestres? | alquiler (Δ4) | nacional y provincia | orígenes 2012T1-2023T2; A=38, B=2.254, C=2.209; 63 configuraciones | ln precio/alquiler (Δ) | elastic net, post-lasso, RF, LightGBM, ARDL, ECM umbral, BVAR, TVP-VAR | validación en bloques con embargo (h=4) | n/a | mejor A: TVPVAR RMSE 0,0726 vs AR(4) 0,0699 (no supera); p BH vs AR(4) 0,76 | Embargo 4; BH por objetivo | B LGBM 0,0124; C EN 0,0528 (base de comparación no especificada en el JSON) | matizado (no supera la base; EXPLORATORIO) | output/v2/BM/resultado.json |
| v2 | BO (H4) | Elasticidad de iniciadas libres al precio real; interacción con suelo | oferta (iniciadas libres) | provincia (47) | 2005-2023, N=879 | ln iniciadas | precio real; precio × suelo | MCO FE provincia + año | cluster provincia; WCB Webb 9.999 | precio 0,794 [0,110; 1,479], p IUT 0,011 (uni); interacción −0,616 [−1,29; 0,06], p IUT 0,046; Holm-7 H4 = 0,232 (BS) | Intersección-unión; robustez 2SLS | P3 iniciadas/suelo: RMSE 0,0586 vs AR(4) 0,0394 (DM −1,39, p 0,18) | matizado: H4 no sobrevive a Holm-7 | output/v2/BO/resultado.json |
| v2 | BP (H5) | Efecto del tope de rentas catalán (Ley 11/2020) sobre alquiler | alquiler IPC (stock) | provincia (4 tratadas + 45 donantes) | 2016T1-2023T4, N=32 trim. | ln IPC alquiler | tratamiento 2020T4-2022T1 | Synthetic DiD (propio) | permutación espacial, B=1000 | efecto 0,0037 [−0,0002; 0,0076]; p permutación 0,065; Holm-m6 0,325; Holm-7 pendiente en BS | Falla pretendencias | pseudo-OOS RMSE 0,00626; DM −0,71 (no aplica a política) | matizado (no concluyente) | output/v2/BP/resultado.json |
| v2 | BV (H2) | Precio real de compra vs crédito nuevo y coste de uso | precio (compra) | provincia (49) | 2004T1-2024T2, N=3.981 | Δ4 ln precio real (tasado − deflactor) | Δ4 ln hipotecas importe; coste de uso × exposición; Δ4 ln ocupados | MCO FE provincia + trimestre | cluster provincia; WCB 9.999 | crédito 0,00873 [0,0033; 0,0141], p Holm-m2 0,0018; coste de uso × exposición −0,00441 [−0,0058; −0,0030], p Holm-m2 <0,001; Holm-7 H2 = 0,779 (BS) | Holm/BH intra-H2 (m=2) | RMSE 0,0605 vs AR(4) 0,0418 (DM −1,60) | matizado: asociación sin valor predictivo en sellado | output/v2/BV/resultado.json |
| v2 | BS (síntesis) | Holm-7 de las 7 confirmatorias y evaluación sellada | varios | varios | 52 prov. sellado 2024T3-2026T2 | (H1) Δ alquiler | (H1) AR(4) + demografía | Holm-7 y DM sellado | n/a | Holm-7: H1 1,0; H2 0,779; H3 0,176; H4 0,232; H5 1,0; H6 0,098; H7 1,0 | Sellado: H1 RMSE 0,01079; DM 3,98; p 0,005 | H1 vs AR(4) sellado | matizado (H1 supera AR(4) en sellado, sin Holm-7 en el resto) | output/v2/BS/resultado.json; output/v2/informe_v2.md |
| v2 | docs/v2 (revisiones) | Revisión por rama (BA, BD, BI, BM, BO, BP, BS, BV) | varios | varios | varios | varios | varios | varios | varios | varios | revision_*.md | varios | n/a | docs/v2/revision_*.md |
| v3 | C1 (H3-1, H3-2) | Turísticos (VUT por 100 viviendas) y alquiler SERPAVI | alquiler SERPAVI | sección censal | 2016-2024, N=70.628 | Δ alquiler SERPAVI (VC, mediana €/m²) | VUT por 100 viviendas; shift-share leave-one-out | MCO FE sección + año×municipio; 2SLS shift-share LOO | cluster distrito | H3-1 0,00026 [−0,00074; 0,00126], p aj. 0,467; H3-2 p aj. 0,501 | No aplica OOS | n/a | matizado (no concluyente; capa C4) | output/v3/C1/resultado.json |
| v3 | C3 (H3-3a, H3-3b) | Topes de renta (Ley 11/2020): renta y contratos nuevos | renta y contratos nuevos (fianzas) | municipio (61 sujetos) | 2019T1-2023T4, N=191 | renta (H3-3a); nº contratos nuevos (H3-3b) | tratamiento 2020T4 | DiD Callaway-Sant'Anna (un solo momento); TWFE; DID_M | cluster municipio | H3-3a CS −5,41 % [−7,09; −3,70] (−37 €/mes), p aj. 0,048; H3-3b ic95 [−9,93; 0,47] p aj. 0,0002 (**inconsistencia a revisar**) | Falla criterios a y c; placebos P3; Rambachan-Roth; Oster | No aplica (efecto de política) | matizado: C4; cambia de mercado (contratos, no stock) | output/v3/C3/resultado.json |
| v3 | GL | Réplica de García-López (2020) en Barcelona | alquiler SERPAVI | sección/distrito Barcelona | 2021-2024, N=3.260 | Δ alquiler SERPAVI | VUT por 100 viviendas | MCO FE sección + año (réplica sin IV) | cluster distrito | −0,00417 [−0,00779; −0,00054], p aj. 0,269 | n/a | n/a | matizado (no reproduce con p ajustado) | output/v3/GL/resultado.json |
| v3 | PA | Hechos contables del problema de la vivienda | vivienda (varios) | nacional/provincia/municipio | 52 provincias; 3.139 municipios vacancia | varias | sin regresores | descriptivo (rango entre fuentes) | n/a | 24 hechos; A1 2002-2007 −792.283 viviendas | n/a | C1 no predice | vigente (C1/C2 descriptivo) | output/v3/PA/resultado.json |
| v3 | PB | Cotas de atribución de precios y alquileres | precio y alquiler (cota de cantidad) | nacional / municipio (3.479) | 52 provincias; B1 3.479 municipios | % de subida explicada | turísticos, inmigración, tipos, grandes tenedores | Cotas de Manski (identificación parcial) | n/a | B1 precio mín. 8,33 %; central 2,75 %; no explicado 25,03 %; B2 cuota máx. 100 % (no informativa) | Supuestos explícitos | n/a | vigente (cota C2; no causal) | output/v3/PB/resultado.json |
| v3 | PD | Políticas contrafactuales de acceso a la vivienda | oferta / esfuerzo de acceso | nacional | 317.520 escenarios | simulación stock-flujo | parámetros de rejilla | simulación; dominancia y minimax regret | n/a | P1 necesarias mediana 261.346 (rango 103.560-413.004) | n/a | n/a | EXPLORATORIO (sin contraste) | output/v3/PD/resultado.json |
| v3 | POT | Potencia de los diseños P-C | varios | sección/distrito | N=70.628 | n/a | n/a | EMD y WCB (500 réplicas) | n/a | sin estimación | potencia | n/a | DESCRIPTIVO | output/v3/POT/resultado.json |
| v3 | docs/v3 | Plan, hipótesis, revisiones de oleada | varios | varios | varios | varios | varios | varios | varios | varios | revision_oleada1-3.md | varios | n/a | docs/v3/*.md |
| v4 | M0 | Conciliación del déficit 2021-2025 y terminadas | vivienda (flujo) | nacional | 2021-2025 | viviendas | descomposición aditiva | contable; triangulación MIVAU-Catastro (±15 %) | n/a | 700.934 [559.752; 969.059] | n/a | n/a | matizado (conciliación; sustituye cifras de v1) | output/v4/M0/resultado.json |
| v4 | M1 | Concentración del déficit (hogares − altas) | vivienda (déficit) | nacional, provincia (52), municipio (703) | 2021-2025 | déficit | altas netas; hogares | contable (4 combinaciones; bajas 0-0,2 %) | n/a | mediana nacional 744.100 [657.059; 933.231] | signo único | n/a | matizado (rango; C4) | output/v4/M1/resultado.json |
| v4 | M2 | Por qué se crean hogares (Shapley) | hogares (demanda) | nacional y provincia | 2006-2025, 5 periodos | Δ hogares | tamaño nativos, tamaño extranjeros, estructura edad, tasa de jefatura | descomposición Shapley (4 factores) | n/a | 2006-2007: ΔH 446.014 (extranjeros 37 %; nativos 21,5 %) | n/a | n/a | matizado (descriptivo; 53-76 % de ΔH en 2020-2025 según corrección EPA) | output/v4/M2/resultado.json |
| v4 | M3 | ¿Se puede construir donde falta? (brecha Glaeser-Gyourko) | oferta (suelo) | provincia (52), municipio (703) | 324 especificaciones | brecha precio-coste | suelo, precio, coste supuesto | brecha con coste supuesto; multiverso | n/a | brecha provincial central −734 a 2.208 (coste supuesto) | Estabilidad de clase modal | n/a | EXPLORATORIO (C4; sin lenguaje causal) | output/v4/M3/resultado.json |
| v4 | M4 | Peso de PJ y extranjeros en stock y flujos | parque de vivienda | provincia (52), ciudades (7) | 19 años de extranjeros | cuotas y ratios | sin regresores | descriptivo | n/a | stock nacional 26.623.708 viviendas (principal 18.536.616) | n/a | n/a | DESCRIPTIVO | output/v4/M4/resultado.json |
| v4 | M5 | Qué instrumentos funcionarían (rúbrica) | política | instrumentos (23 filas) | 23 instrumentos | signo esperado | rejilla de elasticidades | rúbrica idéntica; incidencia | n/a | signo estable estricto: P1, I10/I27/N7 | n/a | n/a | EXPLORATORIO (C4); C2 de P-D | output/v4/M5/resultado.json |
| v4 | M7 | Exuberancia de precios (GSADF) | precio/alquiler | nacional y 11 CCAA | 2015T1-2024T4, N=78 | ratio precio/alquiler (IPV, valor tasado) | sin regresores | GSADF con valores críticos por simulación y WCB (499) | n/a | IPV/IPC alquiler nacional 3,097 (p 0,014); valor tasado/IPC 4,344 (p 0,008) | No reverificado en v6_1 para nacional | n/a | matizado (CCAA: ninguna supera en v6; test de exuberancia no identifica burbujas) | output/v4/M7/resultado.json |
| v4 | docs/v4 | Plan y revisiones (A, B, C, C_it2) | varios | varios | varios | varios | varios | varios | varios | varios | revision_oleada*.md | varios | n/a | docs/v4/*.md |

### Tabla 2. Problemas detectados en el inventario (a revisar, no corregidos)

1. v1 ECM preferido: el historial da DM p 0,509 frente a p 0,290 en output/f2/oos_dm.md. Puede ser otra especificación o muestra. Hay que aclararlo antes de citar cualquiera de las dos cifras.
2. v3 C3, H3-3b: el IC95 [−9,93; 0,47] incluye 0 mientras que p ajustado = 0,0002. Es inconsistente con el JSON; conviene revisar la unidad o la fuente de cada campo.
3. v2 BP: la corrección Holm-7 figura como «pendiente» en el JSON; BS no la reporta.
4. v2 BM: el JSON no especifica la base de comparación de B y C; no es posible leer el DM de estos modelos sin el registro.
5. v1 CCE: el p = 0,040 de CCE-P no sobrevive a la corrección por búsqueda según historico/docs/revision_f5.md; el CD no es interpretable sobre residuos de FE bidireccional (Juodis-Reese 2022).

### Respuesta explícita: PMG, MG, DFE, cointegración de panel y CIPS

Búsqueda (grep -rnw en src/, docs/, output/, por PMG, MG, DFE, CIPS, CCE, CCE-MG, CCE-P, Pedroni, Westerlund, Pesaran, y frases «pooled mean group», «mean group», «cointegración de panel»):

- **PMG (Pooled Mean Group)**: no se estimó. No aparece en src/ ni en output/. Sin resultado.
- **DFE (Dynamic Fixed Effects)**: no se estimó. Sin resultado.
- **MG (Mean Group, Pesaran-Smith)**: sí, pero solo en v6, como robustez. Ruta: src/v6/m1a_run.py (MG y CCEMG), src/v6/m1b_run.py línea 195, output/v6/M1B/tablas/cce_mg.csv. Ejemplo: MG Δ ln pm2 tasado ~ ln_pib_pc = 0,248 (EE 0,022), N unidades 41. Versión v6, fuera del alcance v1-v4, pero citado por completitud.
- **CCE-MG y CCE-P (Pesaran 2006)**: sí, en v1 (f5) y v6. Rutas: src/f5_panel.py (líneas 173-212), output/f5/tabla_cce.csv, output/f5/cd_pesaran.csv. Resultado en la tabla 1 (fila v1 f5 CCE).
- **CIPS (Pesaran 2007)**: sí, en v1 f5, como test de raíz unitaria de panel por CCAA (N=17, T=18), no como test de cointegración. Ruta: src/f5_panel.py (líneas 235-272), output/f5/cips.md y cips.csv. Resultado: ln IPV en 1ª diferencia rechaza raíz unitaria (CIPS −3,293, p 0,000); ln IPV en nivel no rechaza.
- **Pedroni y Westerlund (cointegración de panel)**: no se estimaron. Aparecen solo como no ejecutados: output/v6/M1B (campo «no_ejecutados», src/v6/m1b_salidas.py línea 70), con la razón «T anual=9». En v1, historico/docs/revision_f2.md y docs/literatura.md los citan.
- **«Cointegración de panel»**: no se estimó en v1-v4 (la cointegración de v1 es de series nacionales: EG, Johansen y ARDL en output/f2/cointegracion.md).

### Notas de la tarea

- No se ha ejecutado ningún modelo ni leído data/sealed. Solo se han leído ficheros de output/ y docs/ y se han usado consultas puntuales sobre src/.
- Filas con «n/t» o «n/a» indican campos no extraídos en esta pasada, no ausencia del modelo.
- Ninguna cifra de este inventario reemplaza la cifra publicada; las discrepancias de la tabla 2 se han dejado para revisión.

### C.2 v5-v6.2

Fecha de la lectura: 2026-10-12. Tarea de solo lectura. No se ha ejecutado ningún modelo, no se ha leído `data/sealed` y no se han modificado ficheros del proyecto. Fuentes: `output/*/resultado.json` (esquema común: rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra, notas) y los ficheros de tabla citados en cada apartado.

**Discrepancias con la lista pedida:**
- Existen `output/v5/A6`, `output/v5/R1T`, `output/v6/M0`, `output/v6_1/K4A-K4C` (K4D es carpeta sin `resultado.json`), `output/v6_2/L1` y `L2`. No se listan en la petición y se incluyen abajo.
- `output/v5_1` tiene T1, T2, T3, T4 y T6. **No existen T5 ni T7** (ni carpeta con `resultado.json`).
- Los ficheros pedidos `tabla_modelos.md`, `mejor_modelo.csv` existen en `output/v6/M4/`. `peso_variables.md` existe en `output/v6/M2/`.

---

### 1. Modelos por versión

Leyenda de «p»: p bruto / p ajustado (Holm, BH o wild bootstrap según indique el registro). «FM» = fuera de muestra.

#### 1.1 v5 (entregables; `output/v5/*/resultado.json`)

| Familia | Pregunta | Mercado / nivel | N | Dependiente y transformación | Regresores / retardos | Estimador | EE | Coeficientes principales, p bruto / ajustado | Diagnósticos | FM (RMSE, base, DM) | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1A | Peso inicial de no residentes extranjeros y subida de precio provincial 2015-2025; conciliación VUT | Compra; provincia (corte) | 50 unidades BK-002 (43 provincias) | Δln precio provincial | Peso no residentes (pp); controles en E2 | MCO corte transversal, 8 especificaciones, bootstrap 2000 | HC3 | Bivariada 0,0096 por pp, IC [0,0046; 0,0147], p ajustado Holm 0,0015. Con controles 0,0002, p ajustado 1,0. | R2 aj. 0,60; Pearson 0,56; Spearman 0,56 | No aplica (corte) | Cerrado; C4 | `output/v5/R1A/` |
| R1B | Donut post-COVID (BK-041); multiverso (BK-040); GSADF con tamaño corregido (BK-023) | Municipal (306 municipios >25k hab. tasado; 2.668 SERPAVI) | Donut 128 y 6; multiverso 320 | Crecimiento anual de precio; GSADF sobre ratio | Distancia a área (FE) | Diferencia de pendientes; GSADF | Agrupados por área | Multiverso: 77 % de especificaciones con diferencia positiva; ninguna significativa tras Holm (320 espec.) | Permutaciones B=200 | No aplica | Cerrado; C4 | `output/v5/R1B/` |
| R1C | Propiedad de la vivienda; capacidad de construcción | Nacional y CCAA (34 celdas) | 34 | Tabulación; ratio ocupados/iniciadas | No aplica | Descriptivo, Spearman entre CCAA | No aplica | Tenencia total 74,5 % (C1); Spearman Holm 0,0055 | 8 celdas sin dato | No aplica | Cerrado; C1 (tenencia) / C4 (resto) | `output/v5/R1C/` |
| R1T | Pendientes técnicos (cruce SERPAVI-distritos) | Valencia, distritos | 19 | No aplica | No aplica | Cruce de códigos | No aplica | No aplica | Supuesto: distritos censales = distritos municipales | No aplica | Técnico | `output/v5/R1T/` |
| A23 | Conciliación precio: IPV INE frente a núcleo MIVAU/Notariado/Registradores; alquiler (A2, A3) | Nacional, CCAA y provincia | 11 años de precio; 17 CCAA | Variación acumulada de medias anuales | No aplica (puente) | Puente en log con pesos Laspeyres | No aplica | IPV +79,9 %; núcleo +44,2 a +56,1 % (mediana 47,2 %); efecto nueva/usada 0,004 pp | Independencia entre fuentes documentada | No aplica (descriptivo) | Cerrado; C1 (núcleo) / C4 | `output/v5/A23/` |
| A4 | Dónde falta vivienda y es rentable construir con el coste oficial | Provincia (52) y municipio (703) | 52 / 703 | Clase por rejilla coste × margen × tipo × edificabilidad × suelo | No aplica | Clasificación determinista (MBC 1993 actualizado con Eurostat) | No aplica | Rango coste 421,8-932,1 €/m²; provincias 2021-2025 por clase: clase 1 = 37 (8 robustas), clase 2 = 11 (3), clase 3 = 2, clase 9 = 2 | Reconciliación provincia-nacional cuadra | No aplica | Cerrado; C4 (regla B5) | `output/v5/A4/` (`clasificacion_provincias.csv`, `clasificacion_municipios.csv`) |
| A5 | Instrumentos en documentos oficiales programáticos y normativos | Documentos (22) | 22 documentos, 1.099 coincidencias | Recuento de palabras clave | No aplica | Recuento con diccionario trilingüe | No aplica | No aplica (recuento, no medida validada) | Validación de precisión parcial | No aplica | Cerrado; C4 | `output/v5/A5/` |
| A6 | Topes fuera de C3; no replicación de García-López | Nacional | n/d | Stock frente a flujo | No aplica | Consolidación documental de v4 M0 | No aplica | Atenuación stock-flujo 0,55-0,75; β −0,0042, IC [−0,0078; −0,0005], p ajustado 0,27 | No aplica | No aplica | Cerrado; C4 | `output/v5/A6/` |
| B1 | Necesidad de vivienda 2026-2035 (A+R+V+F−M−K; L ya neta en F) | Provincia (52) y nacional | 52 | Necesidad anual en viviendas, rango min-central-max | Componentes de fuente | Suma por componentes | Rango, no EE | Central nacional 214.868 viviendas/año (93.628-309.921); 48 provincias con presión; 4 con R en un solo método | Control de sumas sin fallos | No aplica | Cerrado; C4 | `output/v5/B1/` |
| B2 | Déficit 2021-2030 por provincia (D2030 = D2025 + F − T + B) | Provincia (52) y nacional | 52 | Déficit en viviendas | F, T (3 escenarios), B | Proyección contable | Rango | Déficit 2025 nacional 700.934; 2030 central 1.296.672 (872.529-1.447.953) | Control de sumas | No aplica | Cerrado; C4 | `output/v5/B2/` |
| B3 | Ocho familias de determinantes a la vez (Bartik, población, etc.) | Transversal, provincia/municipio | 50 (principal Y1-P1); 46-47 otros | Δ log de precio por unidad de DT | 13 regresores estandarizados | MCO conjunto; Shapley | HC3 y Conley (100 y 200 km) | H-B3-1 (Bartik) b 0,0236 por DT; IC [−0,0006; 0,0479]; Holm 8 familias 0,335; Holm 3 confirmatorias 0,112 | R2 0,912; R2 aj. 0,880; LOO-CV RMSE 0,066 | LOO-CV (no aplica embargo) | Cerrado; C4 (descriptivo) | `output/v5/B3/` |
| B4 | Triangulación de salidas v2, B3 y otras (contribuciones) | Nacional y CCAA | 71 entradas, 29 huecos | Pp de Δln, cuotas de R2 | No aplica | Triangulación | No aplica | Contribuciones no estables entre ventanas | Ventanas desplazadas | No aplica | Cerrado; C4 | `output/v5/B4/` |
| CA | Posición de España en la UE-27 y regresiones descriptivas de precio; ADL(4) para predicción | Europa (10 indicadores), crédito (6 trimestres) | 10 / 6 | Percentil y desviación frente a la mediana | ADL(4) + crédito construcción + inmob. (retardo 4) | Descriptivo; ADL 1 paso, ventana expansiva, embargo 4 | No aplica | Holm sobre 36 pruebas, mínimo 0,032 | RMSE 0,141 frente a AR(4) | ADL frente a AR(4) (DM) | Cerrado; C4 | `output/v5/CA/` |
| CB | Correlación de usurpación con alquiler (Spearman, permutación 10.000) | CCAA (17) y secciones censales (36.333) | 17 | Spearman (ρ) | Usurpación por 100k; porcentaje de alquiler | Spearman con permutación | No aplica | C5-S2 ρ 0,66, p 0,006, p Holm 0,038; C5-S1 ρ 0,57, p Holm 0,074 | Seed 20261010; fechas distintas Censo/AEAT/ECV | No aplica | Cerrado; C4 | `output/v5/CB/` |
| CC | Sobrecarga de costes y cotas de salidas 2026-2035 (plazo-calificación) | Grupos de hogares | 11 años de sobrecarga | Cambio en pp 2015-2025; cota de salidas | No aplica | Descriptivo + convolución en 3 escenarios | No aplica | Cambio 2015-2025 pp: QU1 −13,2; RENT_MKT −16,5; OWN_L −5,3 | Cuadre suma CCAA-nacional máx. 6.024 | No aplica | Cerrado; C7 descriptivo, C2 cota | `output/v5/CC/` |
| D1 | Traslado a precio de ayudas por instrumento (36 instrumentos, 52 provincias) | Provincia por clase A4 | 36 × 52 | Incidencia \|εd\|/(εs+\|εd\|) | No aplica | Rúbrica determinista | No aplica | Traslado clase A1 min/central/max 27,8 / 58,4 / 81,8 %; clase A2 88,1 / 100 / 100 %; clase A3 50,1 / 76,4 / 89,8 % | Métodos A y B reportados ambos | No aplica | Cerrado; C4, signos en C2 | `output/v5/D1/` |
| D2 | Cruce de necesidad, déficit y política por territorio | Provincia y clase | 52 | Cobertura de P-D y vacías (%) | No aplica | Cruce de tablas; reparto por cuota de necesidad (supuesto) | No aplica | Clase 1: cobertura P-D 11,6-46,5 %; vacías 30,2 %. Necesidad anual 214.868 | Control de sumas: todo OK | No aplica | Cerrado; C4 | `output/v5/D2/` |
| D3 | Comparación de rangos con referencias externas | Nacional | 22 | Coincide / difiere | No aplica | Regla de solape o diferencia ≤15 % | No aplica | Coincide 2; difiere 1; comparable en parte 6; no comparable 9 | 4 referencias no localizadas | No aplica | Cerrado; descriptivo | `output/v5/D3/` |

#### 1.2 v5.1 (`output/v5_1/T1-T6`; T5 y T7 sin fichero)

| Familia | Pregunta | Mercado / nivel | N | Dependiente | Regresores / retardos | Estimador | EE | Resultados principales | Diagnósticos | FM | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | Bajas netas del parque 2011-2025 (4 fuentes: identidad censal, Catastro, demoliciones) | Provincia (52) | 52 provincias; 13 años B | Tasa anual de bajas | No aplica | Cálculo contable; t de una muestra con Holm (solo descriptivo) | No aplica | Tasa nacional 2015-2024: central 2,56 %/año (rango 0,00-5,18 %); identidad censal −0,33 % (por discrepancia de signo, no concluyente) | Las fuentes no coinciden dentro del margen | No aplica (AR(4) y ECM no aplican) | C4 | `output/v5_1/T1/` |
| T2 | Viviendas liberadas por envejecimiento 2026-2035 (defunciones, residencias, traslado) | Provincia (52) | 52 | Liberadas por año | Parámetros de residencia (4-8 % de 75+), estancia 2,5-4 años, 30-60 % solos, sobremortalidad ×2 | Contabilidad de flujo por provincia | No aplica (rangos de supuestos) | Liberadas 2026-2035 central 1.856.431 (936.056-3.168.590); 185.643 por año | Control de sumas por tipos | No aplica | C4 | `output/v5_1/T2/` |
| T3 | Déficit 2021-2025 y necesidad 2026-2035 con bajas (T1) y liberadas no llegadas al mercado (T2) | Provincia (52) | 52 | Déficit y necesidad | Bajas T1 y liberadas X | Contabilidad con rangos | Rango | Déficit 2021-2024 sin bajas 562.692-688.692; con bajas T1 central 653.097 (562.692-744.144); máximo antiguo 902.808 | Control de sumas y de liberadas | No aplica | C4 (el déficit sin bajas es C1) | `output/v5_1/T3/` |
| T4 | Dirección del déficit 2026-2030 en todos los escenarios (rejilla 5 × 3 × 3 × 4) | Provincia (52) | 52; 180 escenarios por horizonte | Déficit 2030 | dD = F − T + B + X | Rejilla de escenarios | Rango | Déficit 2030 nacional central 1.349.025 (788.180-1.773.555); con X 1.516.129 | Recuento por etapas | No aplica | C4 en magnitud; dirección C2 | `output/v5_1/T4/` |
| T6 | ¿Hay datos abiertos de alquiler de temporada o por habitaciones (BK-014) y MESVAL (BK-017)? | Nacional | n/d | No aplica | No aplica | Prueba de fuentes | No aplica | Ninguna fuente probada contiene duración del contrato ni modalidad de temporada | Fecha de prueba 2026-10-11 | No aplica | Técnico | `output/v5_1/T6/` |

#### 1.3 v6 (validación sellada v6; `output/v6/*`)

| Familia | Pregunta | Mercado / nivel | N | Dependiente y transformación | Regresores / retardos | Estimador | EE | Resultados principales (p bruto / ajustado) | Diagnósticos | FM (RMSE, base, DM) | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M0 | Construcción de paneles, sellado v6 y potencia (Fisher-z) | Compra, alquiler (provincia y municipio); índice tasado | 100.353 | No aplica | No aplica | Descriptivo | No aplica | No estima modelos. Validación sellada contaminada descriptivamente por usos v4-v5 | Sellado `sellar_v6` | No aplica | Cerrado; C4 | `output/v6/M0/` |
| M1A | Efecto de la cuota de extranjeros, de la población, del PIB y de la oferta sobre el alquiler SERPAVI (TWFE) | Alquiler de stock; provincia (105 obs, 35 unidades) y municipio (4.865) | 105 / 4.865 | Log del alquiler €/m²/mes | Regresores en t−1 | TWFE con y sin tendencias | Wild cluster bootstrap Webb (B=999), por CCAA; Driscoll-Kraay; Conley | ln_pob: b 0,875, p 0,026, p ajustado 0,182 (provincia); municipio b 0,972, p 0,023, p ajustado 0,161. Resto de variables p ajustado 1,0. | RMSE 0,023 frente a 0,092 del AR(4) | Frente a M1 y AR(4) (EF) | EXPLORATORIO (C4); ningún coeficiente significativo tras ajuste | `output/v6/M1A/` (`tabla_coeficientes.csv`, 121 filas) |
| M1B | Compra: precio, volumen y relación compra-alquiler; FE unidad+año (preregistrada) y unidad+tendencia | Compra; provincia y municipio; valor tasado MIVAU | 64 (S1 prereg) y otras | Log del precio tasado | Regresores en t−1; ln_pob, share_ext_pob | MCO con EF; SDM | WCB restringido por CCAA (B=999); CR1 | S1 Holm: ln_pob b 0,599, p wild 0,517, p Holm 1,0. Holm mín. 0,496; BH mín. 0,0 | Clusters: 8 CCAA (provincial) | M1b-ADL frente a AR(4) y ECM v1; orígenes 2018/2020/2022 | EXPLORATORIO; ningún contraste cumple | `output/v6/M1B/` |
| M2 | Peso predictivo de cada variable (BMA, elastic net, PDS) | Provincia; alquiler (106 obs. completas) y compra | 106 / más | Log, % de efecto | Variables en t−1 con FE | BMA (g = max(N, K²), uniforme y beta-binomial), elastic net + PDS, multiverso | Intervalo creíble 95 % | PIP alquiler: ln_pob 1,00; share_ext_pob 0,30. PIP compra núcleo de share_ext 0,77 (completo). BH q=0,10 sobre 4.586 contrastes | PIP = soporte asociativo, no causal | No aplica (FM en M4) | EXPLORATORIO; nada causal | `output/v6/M2/` (`peso_variables.md`, `peso_variables.csv`) |
| M3A | Predicción de alquiler con RF y LightGBM (30 configuraciones por familia y nivel) | Alquiler; provincia, municipio, distrito | 8.554 (distrito, muestra común) | Log del alquiler | AR por unidad (p por AIC 1-4) | RF y gradient boosting; búsqueda aleatoria | No aplica | Mejor provincia RF: RMSE 0,0105 (AR 0,0303; ECM v1 aprox. 0,0110) | Bloques espacio-temporal; DM-HLN Holm y BH en `dm_hln_validacion_interna.csv` | Validación interna; mejor provincia RF RMSE 0,0105 | EXPLORATORIO (predicción) | `output/v6/M3A/` |
| M3B | Predicción de compra: RF, LightGBM, BART sustituido por bosque bootstrap bayesiano, MixedLM (sustituto de PyMC), MLP y GCN (solo municipio) | Compra (precio y volumen); provincia trimestral y municipio anual | 1.476 (trimestral) | Log del precio tasado | Ver `registro_*.csv` | ML, BART sustituto, MLP y GCN | No aplica | MUN_PRECIO_ANUAL: mejor ML BBF, RMSE 4,98 % frente a 8,95 % del AR; DM −1,56, p 0,178. PROV_PRECIO_TRIM: RMSE 1,93 % | Top SHAP: tipo hipotecario t−1, crédito; SHAP descriptivo | Validación en bloques | EXPLORATORIO; SHAP sin lectura causal | `output/v6/M3B/` |
| M4 | Predicción a un paso con modelos ajustados en la validación sellada | Alquiler, compra precio y volumen; provincia y municipio | 53 modelos, 9 tareas | Log, RMSE en % | Modelos ya ajustados | Evaluación de 53 modelos; `evaluate_v6` | No aplica | Alquiler provincia GB: RMSE 1,61 % frente a persistencia 4,21 % (DM-HLN −9,39; p Holm en `tabla_modelos.md`); MUN_PRECIO_ANUAL: mejor = ECM v1, RMSE 3,93 %; persistencia 6,33 % | 0 variables relevantes con seguridad | DM-HLN en `dm_hln` y p Holm dentro de tarea | EXPLORATORIO; predicción | `output/v6/M4/` (`tabla_modelos.md`, `mejor_modelo.csv`) |

#### 1.4 v6.1 (`output/v6_1/K1-K4C`)

| Familia | Pregunta | Mercado / nivel | N | Dependiente | Regresores / retardos | Estimador | EE | Resultados principales | Diagnósticos | FM | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | ¿Predice algún modelo mejor que la base más exigente? (K1) | 9 tareas (provincia, municipio) sellado v6 | 9 tareas; 11 provincias selladas | RMSE en % | Modelos de M1-M4, ECM v1 como base | DM-HLN y permutación por inversión de signo; Holm por tarea y grupo | No aplica | Predice mejor que la base en 6 tareas; no distinguible en 3. MUN_PRECIO_ANUAL: el mejor (bosque bayesiano) 4,13 % frente a ECM v1 3,93 %: no la supera | Clasificación de clases | Frente a ECM v1 y AR(4) | EXPLORATORIO (C4): predicción | `output/v6_1/K1/` (`tabla_modelos_k1.md/.csv`) |
| K2 | Inmigración y precio/alquiler: MCO/2SLS con EF provincia-año; cuota de extranjeros y población | Provincia y CCAA | 328 (compra), 1 familia de 137 especificaciones | % por +1 pp de cuota | Cuota (t−1), población, demanda externa | MCO/2SLS; BMA aproximado (BIC) | Agrupados | Cuota compra sin población 4,26 %/pp; con núcleo −1,31 % (IC [−4,31; 1,69]); p Holm 1,0. Primera etapa F 3,52 (38 provincias) | VIF 1,79 | No aplica | ANALIZADA, NO CONCLUYENTE; C4 | `output/v6_1/K2/` |
| K3 | **[corrección]** Iniciadas y alquiler (retardos y adelantos con EF provincia y año), léxico de importancia y rango del ratio precio/alquiler según la medida | Provincia | 175 | Ratios precio/alquiler | Variables de precio inicial y rezagos | OLS, cluster por provincia | Cluster provincia | Coeficientes A_conjunta: p ajustado 1,0 (ini_l2, ini_l1); ini_1000 p ajustado 0,57 | Rango de ratio 2015 [18,9; 20,3] | No aplica | ANALIZADA; C4 | `output/v6_1/K3/` |
| K4A | Auditoría dirigida con consultas y tests | Proyecto | 11 | No aplica | No aplica | Auditoría | No aplica | 11 hallazgos: 0 críticos, 2 altos, 3 medios, 6 bajos | No aplica | No aplica | Técnico | `output/v6_1/K4A/` |
| K4B | Doble implementación independiente | Proyecto | 15 | No aplica | No aplica | Recalculo | No aplica | Coinciden 5; parciales 5; no reconstruibles 5; no coinciden 0 | No aplica | No aplica | Técnico | `output/v6_1/K4B/` |
| K4C | Extracción determinista de cifras y comprobación de enlaces | Entregables | 1.916 | No aplica | No aplica | Extracción | No aplica | Enlaces rotos 32 → 0; 5 contradicciones (corregidas) | No aplica | No aplica | Técnico | `output/v6_1/K4C/` |

#### 1.5 v6.2 (`output/v6_2/L1-L3`)

| Familia | Pregunta | Mercado / nivel | N | Dependiente | Regresores / retardos | Estimador | EE | Resultados principales | Diagnósticos | FM | Estado | Ruta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | Verificación de fichas y reproducción literal | Entregables | 17 fichas completas; 49 breves | No aplica | No aplica | Recálculo literal | No aplica | 17 fichas reproducidas; 15 de la revisión humana | ruff limpio, sin fallos | No aplica | Técnico | `output/v6_2/L1/` |
| L2 | Segunda doble implementación independiente (sin leer src) | Entregables | 15 | No aplica | No aplica | Recálculo | No aplica | Coinciden 15 de 15 | 11 huecos en anexo, ninguno bloquea | No aplica | Técnico | `output/v6_2/L2/` |
| L3 | Déficit 2021-2025 sin bajas bajo 8 correcciones de hogares × 3 fuentes de terminadas | Nacional | 288 combinaciones | Déficit en viviendas | No aplica | Contable determinista | No aplica | 2021-2024 sin bajas 389.361-710.542 (punto medio 549.952); 2021-2025 sin bajas 523.606-887.950 | Por año y corrección | No aplica | C2 (sin bajas) / C4 (con bajas) | `output/v6_2/L3/` (`deficit_alternativas.csv`) |

---

#

---

## D. Validaciones selladas

**[corrección y síntesis del orquestador]**
- El **panel CCAA trimestral** (`panel_ccaa_q`) no figura en el catálogo de sellado de v2 (`src/holdout.py:CATALOGO`). v1 lo usó entero (2008-2025, con validación fuera de muestra móvil, no sellada). **Ningún periodo existente del panel CCAA es muestra limpia.**
- Paneles provinciales:
  - v2 selló 2024Q3-2026Q2 (temporal) y las provincias 11, 16 y 45. Se abrió 8 veces (H1-H7).
  - v6 selló 11 provincias y el último año (compra 2025, alquiler 2024). Se abrió 53 veces en M4 y 27 en K1.
  - Las provincias no selladas estuvieron siempre en el entrenamiento.
- Validación limpia para V7: solo **datos publicados después del pre-registro de V7** (2026T3 en adelante para trimestrales; 2026 para anuales; SERPAVI 2025 cuando se publique). Una validación espacial con CCAA o provincias nunca selladas es **útil pero no limpia**, porque ya se vieron en el entrenamiento de versiones anteriores.

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

#

---

## E. Resultados por pregunta

### E.1 Historial de conclusiones y cifras publicables

#### 4.1 Tabla compacta (fuente: `docs/v6_1/historial_conclusiones.md`, con adenda v6.2 L4)

| Tema | Conclusión vigente | Capa | Estado |
|---|---|---|---|
| Inmigración → alquiler (CCAA, v1) | Signo positivo, no robusto a todos los niveles | C4 | Se mantiene (asociación) |
| Inmigración → precio (CCAA, v1) | No concluyente | C4 | Se mantiene |
| Cuota de extranjeros → precio (CCAA, v1) | No concluyente | C4 | Se mantiene |
| Inmigración → alquiler y compra (provincia, v2/BI) | Alquiler +3,06 %/pp [1,14; 4,98]; compra n.s. | C4 | Se mantiene |
| Población extranjera → alquiler (v2/BA) | Negativo n.s. | C4 | Se mantiene |
| Cotas Manski de cantidad de hogares extranjeros (v3/PB) | Cota no informativa (100 %) | C2 | Se mantiene |
| Nacionalidad y hogares creados (v4/M2) | 53-76 % de ΔH según corrección EPA | C4 | Se mantiene (descriptivo) |
| Peso de no residentes y precio (v5/R1A) | No concluyente | C4 | Se mantiene |
| Cuota de extranjeros → alquiler/compra (v6/M1, v6/M2) | Cambia la lectura: PIP alta en compra con núcleo, baja en alquiler. K2 lo reclasifica como «analizada, no concluyente» | C4 | Cambia; K2 analizada |
| Inmigración → empleo (v1, v2/BV, v6) | Signo según método; no concluyente | C4 | Se mantiene |
| Renta → alquiler y compra (v1, v6) | Cero en alquiler, positivo en compra (p 0,13), sin concluir | C4 | Cambia de mercado; no concluyente |
| Oferta (iniciadas) → precio (v2/BO, v6) | Oferta responde al precio (β 0,79); otra dirección según medida | C4 | Se mantiene |
| Turísticos (VUT) → alquiler (v3/C1, v6) | Signo no estable; n.s. | C4 | Se mantiene (no concluyente) |
| Turísticos: cota de stock desplazado (v3/PB) | Máximo 2,4-2,75 % del stock de alquiler | C2 | Se mantiene |
| Topes de renta (v2/BP; v3/C3) | Efecto −5,4 % en contratos nuevos (fianzas); falla pretendencias | C4 | Cambia de mercado (contratos nuevos, no stock) |
| Zonas tensionadas (v2/BS) | τ −0,0117, Holm 0,098 | C4 | Se mantiene; no estimable en v6 |
| Tipos hipotecarios → precio (v1) | Sin efecto de largo plazo | C4 | Se mantiene |
| Crédito y coste de uso (v2/BV, v3/PB) | Sin valor predictivo en sellado | C4 / C2 | Se mantiene |
| Déficit acumulado 2021-2025 (v1) | Cambió: v5.1 sin bajas 700.934-757.257 (C1); con bajas C4 central 763.416 | C1/C4 | Cambia (v5.1) |
| Déficit 2021-2024 sin bajas (v6.2/L3) | 389.361-710.542 viviendas | C2 | Vigente |
| Bajas y déficit con bajas (v4→v5.1) | Supuesto de 902.808 (C2) → T1 hasta 744.144 (C4) | C2 → C4 | Cambia (corregido en v5.1) |
| Necesidad 2026-2035 (v5→v5.1) | 99.000-292.000 viviendas/año; dirección 2026-2030 «empeora» (C2) | C4 | Cambia; liberadas no se restan |
| Exuberancia GSADF (v4/M7, v6/M1B) | Ninguna CCAA supera el valor crítico | C4 | Se mantiene |
| Precio de compra: IPV frente a núcleo (v5/A23) | IPV +79,9 %; núcleo +44,2 a +56,1 % | C1 (núcleo) / C4 | Se mantiene |
| Elasticidad precio-alquiler (v6/M1B) | 0,43-1,33 (FE); 1,6-2,1 (DOLS); depende de la especificación | C4 | Se mantiene |
| Predicción frente a AR(4) (v1) | ECM no mejora al AR(4) (DM p 0,509) | C4 | Se mantiene (línea base) |
| Demografía 20-34 (v2/BA) | RMSE 0,0108 frente a 0,0122 del AR(4) | C4 | Se mantiene (predictivo, no robusto) |
| ML sellado (v6/M4, v6.1/K1) | Alquiler provincia: 1,61 % frente a 4,21 % (persistencia); 6 de 9 tareas predicen mejor que la base; ninguna variable relevante con seguridad | C4 | Se mantiene (predicción) |
| Inmigración (v6.2/L4): asociación total y directa | Total: compra +4,3 %/pp; directa (con población): compra −1,3 (IC −4,3; 1,7), alquiler 0,18 (IC −1,5; 1,8). Controlar población es mal control | C4 | Se mantiene K2: analizada, no concluyente |

#### 4.2 Cifras publicables (`docs/v6_2/cifras_publicables.md`, generado por `src/v6_2/l5_publicables.py`)

**Aptas para difusión (C1 o cota C2):**

| id | Indicador | Valor (rango) | Capa | Periodo |
|---|---|---|---|---|
| dh_2125 | Aumento de hogares | 997.586 (981.823-1.013.350) | C1 | 2021-2025 |
| terminadas_1924 | Viviendas terminadas/año (territorio común) | 72.264-94.426 | C1 | 2019-2024 |
| L3-DEF-2124-SINBAJAS | Déficit 2021-2024 sin bajas | 389.361-710.542 | C2 | 2021-2024 |
| A23-P2 | Precio de compra, núcleo 2015-2025 | 47,2 % (44,2-56,1 %) | C1 | 2015-2025 |
| A23-A2 | Alquiler de stock 2015-2024 | 10,9-22,9 % | C1 | 2015-2024 |
| A23-A10 | Contratos nuevos Comunitat Valenciana 2021-2024 | 28,5 % (26,1-30,8 %) | C1 | 2021-2024 |
| A23-A9 | Contratos nuevos Cataluña 2021-2024 | 16,9 % (16,6-17,2 %) | C1 | 2021-2024 |
| E-B1-F | Crecimiento de hogares proyectado (10 años) | 1.308.531-1.772.410 | C2 | 2026-2035 |
| R1C-001 | Hogares propietarios de vivienda principal | 74,5 % (72,1-75,9 %) | C1 | 2021-2022 |

**No citar fuera de contexto (C4 o dependiente de supuestos):**

| id | Indicador | Valor (rango) | Capa |
|---|---|---|---|
| L3-DEF-2124-CONBAJAS | Déficit 2021-2024 con bajas 0,1-0,2 % | 389.361-924.658 | C2 |
| T3-H5b | Necesidad anual 2026-2035 (base sin X) | 210.424 (99.388-292.083) | C4 |
| T3-H5 | Necesidad anual 2026-2035 (con X) | 245.989 (123.936-338.663) | C4 |
| B1-H1 | Necesidad total por año (52 provincias) | 214.868 (93.628-309.921) | C4 |
| D1-H11 | Traslado a precio, clase A4 1 (método A) | 58,4 % (27,8-81,8 %) | C4 |
| D1-H12 | Traslado a precio, clase A4 2 (método A) | 100,0 % (88,1-100,0 %) | C4 |
| K2-CUOTA-COMPRA-SINPOB-SIN | Cuota de extranjeros (compra, sin población) | 4,3 % por pp (2,1-6,4 %) | C4 |
| K2-CUOTA-COMPRA-SIN | Cuota de extranjeros (compra, con núcleo) | −1,3 % por pp (−4,3 a 1,7 %) | C4 |
| K1-N-MEJOR | Tareas donde el mejor modelo supera la base exigente | 6 tareas | C4 |
| latente_convivencia | Demanda latente de jóvenes por convivencia | 188.000-506.000 hogares | C2 |
| B4-v3-vut-cantidad | Stock de alquiler desplazado por VUT (máximo) | 2,4-2,7 % | C2 |
| L3-DEF-2124-BAJAST1 | Déficit 2021-2024 con bajas T1 | 654.646 (389.361-765.994) | C4 |
| L3-DEF-2124-SENS | Sensibilidad sin variantes a y d1 | 596.371-710.542 | C2 |

**Históricas (no citar; sustituidas, ver ERRATA.md):**

| id | Indicador | Valor (rango) | Capa | Sustituida por |
|---|---|---|---|---|
| deficit_2124_c1 | Déficit 2021-2024 sin bajas | 562.692-688.692 | C1 | L3-DEF-2124-SINBAJAS |
| deficit_2124_c2 | Déficit 2021-2024 con bajas supuestas (cota) | 562.692-902.808 | C2 | L3-DEF-2124-CONBAJAS |
| T3-H2 | Déficit 2021-2024 con bajas T1 | 653.097 (562.692-744.144) | C4 | L3-DEF-2124-BAJAST1 |

---

#

### E.2 Resultados regionales ya disponibles (CCAA y provincia)

**Por CCAA**
- **GSADF (burbuja):** el ratio precio/alquiler por CCAA (11 CCAA, 2015T1-2024T4) se evaluó en v4 M7 y v6 M1B. Ninguna CCAA supera el valor crítico. Nacional: estadísticos 3,10-4,82, veredicto de la fuente, no reverificado en K2. Fuente: `docs/v6_1/historial_conclusiones.md`; R1B (GSADF con tamaño corregido, BH/Holm) en `output/v5/R1B/`.
- **Coeficientes M1A/M1B por CCAA:** la inferencia usa wild cluster bootstrap por CCAA (8 clusters en provincial, 7 en municipal, 11 en trimestral). Coeficientes en `output/v6/M1A/tabla_coeficientes.csv` y `output/v6/M1B/tablas/fe_prov.csv`. Ninguno significativo tras ajuste.
- **Peso de inmigración (K2) por CCAA:** `output/v6_1/K2/`. Sin conclusión.
- **Riesgo de conteo:** la muestra de CCAA es de 17 unidades; las estimaciones por CCAA no tienen potencia suficiente.

**Por provincia**
- **Clases A4 por provincia (52):** `output/v5/A4/clasificacion_provincias.csv`. Número de provincias por clase 2021-2025: clase 1 = 37 (8 robustas), clase 2 = 11 (3), clase 3 = 2 (0), clase 4 = 0, clase 9 = 2 (1). Significatividad: C4, sin contraste.
- **Necesidad por provincia (B1):** `output/v5/B1/tablas/`. 48 provincias con presión; 4 con R en un solo método. C4.
- **Déficit por provincia (B2, T3, T4):** `output/v5/B2/tablas/`, `output/v5_1/T3/`, `output/v5_1/T4/`. Proyección bajo supuestos. C4.
- **Déficit provincial tras bajas (T3):** rango por provincia en `output/v5_1/T3/`. C4.
- **Coeficientes M1A (provincia y municipio):** `output/v6/M1A/tabla_coeficientes.csv`. Ninguno significativo tras ajuste (ln_pob p 0,026 → p ajustado 0,182).
- **PIP y peso de variables por provincia (M2):** `output/v6/M2/peso_variables.csv`, `peso_alquiler_prov.csv`, `peso_compra_prov.csv`. Soporte asociativo, no causal.
- **SHAP y dependencia parcial (M3B):** `output/v6/M3B/`. Descriptivo, sin lectura causal.
- **Demanda (K2, K3):** sin conclusión.

---

#

---

## F. Política

(D1, D2 y documentos relacionados)

**Instrumentos evaluados:**
- `output/v4/M5/matriz_instrumentos.csv`: 23 filas (instrumentos agrupados, con columnas de mecanismo, evidencia, efecto, plazo, coste fiscal y riesgos).
- `output/v5/D1/matriz_instrumentos.csv`: 37 filas (I01-I29, N1-N9, P1). Incluye el campo `capa` por instrumento.
- Instrumentos con capa C2 en el signo y C4 en la magnitud: I02/N8, I06, I07, I08/N9, I10/N7, I27, P1.
- Instrumentos sin signo evaluable (D1, `sin_signo_evaluable`): I03, I04, I05, I09, I11, I13, I14, I15, I19, I20, I22, I24, I25, I26, N1, N3, N5, N6 (18 en total).

**Instrumentos sin evaluar:**
- I17 e I23 no tienen definición en v4 (`resultado.json` de D1 lo declara).

**Método de simulación (D1):**
- Incidencia = |εd| / (εs + |εd|), con εs por clase: clase A según la respuesta de oferta de A4; clase B según la rejilla P-D.
- Determinista, sin especificaciones econométricas nuevas (registro.csv vacío por diseño).
- Métodos A y B se reportan ambos cuando discrepan.

**Parámetros y rango de elasticidades:**
- Rejilla de elasticidad de demanda: εd entre 0,3 y 1,5 (`output/v5/D1/` y nota D1-H11).
- Rejilla de elasticidad de oferta εs: clase A por A4; clase B por rejilla P-D. Rango exacto de εs no extraído en esta lectura.
- **Origen de las elasticidades:** `output/v5/D1/literatura_instrumentos.csv`. Ejemplo verificado: Jofre-Monseny et al. (2023, Q1, VERIFICADA) para topes de renta. Otros: Baum-Snow y Marion (2009), Diamond y McQuade (2019), Eriksen y Rosenthal (2010), marcados VERIFICADA, con magnitud no extraída. Cualquier referencia sin verificar debe figurar como «NO VERIFICADA».

**Resultados por clase territorial A4 (D1, método A, traslado al precio):**

| Clase A4 | Min | Central | Max |
|---|---|---|---|
| 1 | 27,8 % | 58,4 % | 81,8 % |
| 2 | 88,1 % | 100 % | 100 % |
| 3 | 50,1 % | 76,4 % | 89,8 % |

- Clase A4 2: el 100 % se traslada al precio (un valor de tope, no un resultado de precisión).
- Clase 1 de D2: cobertura de P-D 11,6-46,5 %; vacías 30,2 %.
- Método B: rango por clase en `output/v5/D1/` (no extraído en esta lectura).

**Documentos relacionados:**
- `output/v5/D2/politica_territorio.md` y `output/v5/D2/resumen_por_clase.csv` (cruce de tablas, reparto de P-D por cuota de necesidad).
- `output/v5/D3/` (comparación con referencias externas: coincide 2, difiere 1, comparable en parte 6, no comparable 9).

---

#

---

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
- `historico/docs/v6_1/auditoria.md`, medios abiertos (ver `docs/v6_1/backlog.md`): K4a-04 (min/max con otro sentido en 48 filas), K4a-05 (fianza GVA bruta frente a truncada; cambiaría paneles sellados de v6, coste S), K4c-03 (26 cifras del verificador; el backlog lo llama K4c-26), K4d-07 (cuartiles, tarea del autor).
- Bajos abiertos en la auditoría: K4a-06, K4a-08, K4a-10, R-04, R-05, R-06, K4c-04 y K4c-07.
- `docs/v6_1/backlog.md`, abiertos: K4a-03b (recalcular D2, M), K4b-NR (5 cifras no reconstruibles solo con el texto; anexo metodológico), K4b-dh (mezcla de stock y media anual, S), K4d-ref (50 referencias «cuartil no verificado» y 76 NO VERIFICADA; Scimago devuelve 403, la verifica el autor, S), K2-49 (reestimar inmigración con 49 provincias; exige mirar provincias selladas en v6, L), BK-E3 (ampliar artículos, M), BK-014 y BK-017 (temporada, habitaciones y MESVAL; sin datos oficiales, L).
- `docs/v5/backlog.md`: tabla de unas 90 filas. Ejemplos con coste de datos: BK-003 (titularidad del parque; Catastro no publica), BK-008 (coste de construcción sin fuente verificable), BK-009 (empleo de construcción por territorio), BK-010 (plazos de licencias), BK-011 (SIU inaccesible por el proxy).

**Limitaciones.**
- `docs/limitaciones.md` (48 líneas): secciones por fase, F2 con ecuación nominal, y un bloque de precio real.
- `docs/v3/limitaciones.md` (27 líneas).
- Sección Limitaciones del working paper: `docs/v5/plantillas/working_paper.md` y `output/v5/working_paper.md`.

**Objeciones de revisores sin resolver.**
- `historico/docs/v6_1/carta_respuesta.md`, «No viable» (solo se declaran como limitación): A-04 (recuento de especificaciones entre versiones), A-05 (WCB y paneles municipales), A-06 (intervalos Anderson-Rubin y shift-share), A-09 (publicar ecuaciones del método de traslado), A-13 (muestra futura), P-10 (costes y magnitudes por euro), P-11 (recalcular D2 con T3), P-12 (fecha de publicación de etiquetas). A-02 y A-03 están «aceptadas en parte» con limitación.
- `historico/docs/v6_2/revision.md`, H8 (baja, anexo): A1 no tabula los 8 trimestres de la EPA de 2021 y 2025; A16 depende de la clase A4, que no se reconstruye desde la ficha. Pasa al backlog.

**Tipos de error recurrentes** (de ERRATA y las auditorías):
- Cruces por nombre con tildes o grafías distintas (SERP2IPVA, Valencia/Valéncia, Incasòl).
- Imputaciones silenciosas (`fillna(1.0)` en A23-A10).
- Redondeos al escribir (`%.6g` en recuentos grandes).
- Fechas de ejecución o de edición ordenadas como texto (Notariado) y fechas de descarga usadas como fecha del dato (manifiesto de Censo, B1).
- Ventanas desalineadas (stock a 1 de enero frente a media anual en `dh_2125`; Censo 2021 con fecha de 1-ene).
- Agregados que suman varias veces (Incasòl: año, acumulados y trimestres a la vez).
- Notas de resultados que quedan desactualizadas tras una evaluación sellada.

#

**Incidencias detectadas por el inventario (abiertas; no se corrigen en esta tarea de solo lectura):**
- v1 ECM: el DM frente a AR(4) es p 0,290 en output/f2/oos_dm.md y p 0,509 en el historial. Puede tratarse de otra especificación.
- v3 C3 H3-3b: el IC95 incluye el 0, pero el p ajustado es 0,0002. Hay que revisar el campo.
- v2 BP: el Holm-7 figura como «pendiente» en el JSON.
- K4c-03 y K4c-26 son el mismo pendiente con dos nombres.
- Pendiente de nuestra comprobación: rango exacto de εs en D1 (método B) y p ajustados por coeficiente de M3B.

---

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

**Este inventario:** 512.221 tokens de subagentes haiku, frente a los 0,25 M pedidos (exceso de 262.221). Los escáneres no respetaron su tope individual; la síntesis la hizo el orquestador sin subagentes adicionales.

---

## I. Recomendaciones para V7: modelos econométricos regionales

**Factible con los datos actuales**

**CCAA trimestral (17 × 2007T1-2026T2, unas 78 observaciones por CCAA).** Base suficiente para paneles dinámicos heterogéneos.
- Variables: precio (IPV y tasado), compraventas (totales y de extranjeros), IPC alquiler, ocupados, iniciadas y terminadas (desde 2008) y población (interpolada).
- Variables nacionales comunes: tipo hipotecario, crédito, Euribor, costes y renta.
- Estimadores **no probados** que tiene sentido probar:
  - PMG, MG y DFE para la relación de largo plazo precio–fundamentales;
  - cointegración de panel (Westerlund, con bootstrap por la dependencia transversal; Pedroni);
  - CCE-ECM o CS-ARDL para los factores comunes;
  - proyecciones locales de panel ante shocks nacionales de tipos.
- Con T de unas 70-78 el problema de T corta de v6 (anual, T = 9) desaparece.

**Provincia anual (52 × 2002-2024; SERPAVI desde 2011).** Paneles FE o CCE con regresores de flujo (padrón, EPA provincial, ETDP, hipotecas e iniciadas/terminadas del Ministerio), con N grande y T moderada.
- La provincia trimestral (panel_prov_q, 2002T1-2024T2) permite paneles dinámicos de precio tasado y compraventas.

**Variables que faltan o son débiles.**
- Renta y PIB solo anuales por CCAA.
- Hogares solo nacionales y trimestrales desde 2021; provinciales desde 2021.
- Paro CCAA trimestral sin integrar en el panel.
- Crédito e hipotecas por CCAA: hay que agregar las hipotecas provinciales mensuales del INE (HPT).
- Costes y licencias solo nacionales, o sin dato.
- Compraventas al contado: no existen.
- VUT solo desde 2020.
- Llegada neta por CCAA solo semestral desde 2023. El flujo provincial va de 2008 a 2022.
- Población trimestral interpolada: se aconseja usarla solo en niveles anuales o como control.
- Eventos regulatorios: hay que construir la dummy CCAA a partir de v2_eventos_politica.

**Riesgos de inferencia.**
- **Pocas unidades.** 17 CCAA dan pocos clusters: hay que usar wild cluster bootstrap (Webb), Driscoll-Kraay y CCE.
- **Heterogeneidad.** Con MG/PMG cada coeficiente individual tiene muy poca potencia.
- **Muchas comparaciones.** La historia del proyecto ya acumula miles de especificaciones. Hacen falta pre-registro, un registro de especificaciones (econ_utils.Registry) y Holm/BH por familia; conviene declarar las especificaciones vistas en v1-v6.
- **Colinealidad.** Población, extranjeros y empleo están muy relacionados (correlación cuota-población dentro de provincia 0,66). Controlar por población es un mal control para inmigración (L4).
- **Dependencia transversal.** Los shocks nacionales (tipos, crédito) son comunes. Hay que usar CD de Pesaran sobre residuos adecuados, no sobre FE bidireccionales.
- **Rupturas.** EPA 2021T1, base de ocupados 2021, IPV base 2015 frente a 2007, y COVID 2020.

**Validación nueva posible.**
- **Limpia:** solo una muestra **futura**. Pre-registrar V7 con fecha verificable (release o DOI, no una etiqueta local) y evaluar con los datos que se publiquen después: IPV 2026T3-2027T2, ETDP, EPA, valor tasado; anual 2026. Es predicción en tiempo pseudorreal con un año de espera.
- **No limpia pero informativa:** validación espacial dejando fuera CCAA nunca selladas (Cantabria, Castilla y León, Cataluña, C. Valenciana, Extremadura, Galicia, País Vasco) y validación temporal en bloques con embargo dentro de 2007-2026T2. Debe declararse como «ya vista en v1».
- Comparar siempre en la misma muestra con AR(4), ECM v1 y las líneas base exigentes de K1 (AR con factor común, efectos fijos, crecimiento nacional).

**Presupuesto razonable.** Entre 0,8 y 1,2 M tokens de subagentes, con este reparto:

| Bloque | Tokens |
|---|---|
| Paneles CCAA trimestral y provincial ampliados (paro, hipotecas agregadas, dummies regulatorias) | 0,15 |
| Pre-registro y potencia | 0,1 |
| PMG/MG/DFE, cointegración de panel y CS-ARDL | 0,25 |
| Provincia anual y trimestral | 0,2 |
| Predicción y líneas base | 0,15 |
| Revisión y cierre | 0,15 |

- Coste de máquina: 2 × `make all`, más unos 30-60 min de los nuevos modelos.
- Hay que evitar los subagentes haiku para síntesis con tope estricto: en este inventario superaron su presupuesto.
