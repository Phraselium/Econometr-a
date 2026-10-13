# Estado V8

## Hecho
- Rama r8/main desde r7.2/main (e7bf435).
- F0: la mayor parte ya está en v7.2:
  - cifras superadas retiradas;
  - una sola cifra de déficit con bajas;
  - construcción adicional con dosis no nula;
  - ficha de burbuja nacional y regional;
  - test de cifras superadas sobre cifras_clave.
- F0, en esta versión: el marcador «[fecha de publicación: pendiente]» se rotula como pendiente del autor (las etiquetas no se pueden publicar desde el entorno).

## Hecho (continuación)
- **F1.** Paneles en data/processed/v8:
  - nacional_q_v8: 1995T1-2026T2, 251 columnas;
  - panel_ccaa_q_v8;
  - cv_prov_q_v8 y cv_prov_a_v8;
  - valencia_ciudad_v8.
  
  Diccionario en docs/v8/diccionario.md y tests en tests/v8/test_f1_paneles.py. `make v8` arranca con f1_paneles.
- **F2.** Pre-registro docs/v8/hipotesis.md, cerrado con la etiqueta local `prereg-v8` (91e618b). El push de la etiqueta falla (el remoto rechaza etiquetas): queda como tarea del autor (docs/v8/notas_release.md).

## En curso
- F4 y F5 cerradas. F5: ningún factor designado en las diez celdas; AR(4) es la base más exigente.
- F6 hecha:
  - congelación (sha256 en notas_release) y `make evaluate_v8`;
  - tablas md, csv y xlsx (fórmulas recalculadas con LibreOffice, sin errores);
  - 287 hechos V8 en cifras_clave (las 716 filas previas son idénticas a las del cierre de v7.2);
  - verificador V8 y adenda del historial;
  - entregables por_que_ha_subido.md e informe_econometrico.md desde plantillas;
  - check_v8 en `make check` (277 passed y 0 errores);
  - `make publicacion`;
  - cierre_proyecto, ideas_futuras y tareas_autor.
- En curso: `make v8` en un clon limpio sin red y el revisor final (opus, docs/v8/revision_final.md).

## Siguiente paso exacto
- Comparar las salidas del clon con las versionadas.
- Aplicar las correcciones del revisor final (como máximo 2 REHACER).
- `make publicacion` y `make check`.
- Fusionar r8/main con la rama designada; commit y push.
- Resumen final de 400 palabras como máximo.

## Tokens por módulo

| Módulo | Subagentes | Orquestador (estimación) |
|---|---|---|
| F0 | 0 | ~40k |
| F1 descarga | 121.258 | ~15k |
| F1 paneles | 214.088 | ~10k |
| F2 | 0 | ~25k |
| F3 herramientas | 384.763 | ~20k |
| F3 revisor | 163.223 | ~10k |
| F3 correcciones (VAR) | 226.757 | ~5k |
| F3 correcciones (resto) | 257.872 | ~5k |
| F4 M2 | 222.214 | ~8k |
| F4 M3 | 68.180 | ~3k |
| F4 M0+M4 | 222.386 | ~4k |
| F4 M6+M7 | 170.542 | ~4k |
| F4 M5 | 183.171 | ~4k |
| F4 M1+M8 | 138.463 | ~4k |
| F4 M9 | 101.170 | ~4k |
| F4 revisor | 237.962 | ~10k |
| F4 correcciones (4 subagentes) | 543.811 | ~15k |
| F5 | 171.139 | ~10k |
| F6 congelación y evaluate_v8 | 79.284 | ~3k |
| F6 tablas y Excel | 109.030 | ~5k |
| F6 cifras_clave, verificador y publicación | 250.775 | ~5k |
| F6 entregables, check_v8 y cierre (orquestador) | 0 | ~60k |

## M2 (SVAR con signos y ceros), hecho
- `src/v8/m2_svar.py` (`--rapido`), `tests/v8/test_m2.py`, salidas en `output/v8/M2/` (irf, fevd, hd_periodos, atribucion, hipotesis_m2, predicciones_congeladas + congelacion.json, resultado.json, resumen.md, registro.csv).
- La identificación principal pre-registrada es INVIABLE con datos reales (0 aceptadas en 9·10^6 rotaciones); operativa = V3 (solo impacto), ESS 671. H8-1…H8-4: ninguna respaldada tras Holm. Desviaciones en desviaciones.md; bloqueo en bloqueos.md.
- Siguiente: revisión de M2 por el orquestador; M3, M0, M4, M6, M7.
- Tokens de subagente (M2): no medidos por el subagente.

## F4 M1 y M8 (2026-10-13)
- **Hecho:** M1 (factor comun; H8-8 p Holm 0,669 no rechaza: P2 y P4 por debajo del 50 %; H8-9 r = 0,60, p Holm 0,020) y M8 (regional: 17 CCAA, panel FE-DK, LP panel, CV por provincia y Valencia ciudad). Scripts `src/v8/m1_factor_comun.py`, `src/v8/m8_regional.py`; salidas en `output/v8/M1/` y `output/v8/M8/`; tests `tests/v8/test_m1.py`, `test_m8.py`. Ejecucion completa ~20 s cada uno. Desviaciones anotadas en `docs/v8/desviaciones.md`.
- **Siguiente:** integracion de M1/M8 en la sintesis (atribucion con `factor_europeo`, `factor_comun`).

## M5 (instrumentos externos IV1-IV3), hecho (2026-10-13)
- Hecho: `src/v8/fetch_m5.py` (descarga única Eurostat a data/raw/v8/eurostat_migr/), `src/v8/m5_lpiv.py` (52 s), salidas en output/v8/M5/, tests/v8/test_m5.py (6 tests). Desviaciones y aclaraciones en desviaciones.md (IV1, IV2, IV2b, IV3); datos nuevos en diccionario.md.
- Resultado: instrumentos débiles (F efectivo 0,05-2,4 en IV1/IV2; ≤ 8 en IV3), AR no acotado; H8-5, H8-6 y H8-7 no rechazadas (p Holm 0,83); todo C4, sin lectura causal. Primera etapa de IV1 con signo contrario al esperado (π < 0).
- Siguiente: integrar atribucion.csv (metodo `lpiv`, C4, bandas vacías donde AR no acotado) en la síntesis M0/M6.
- Tokens de subagente: no registrados por el propio subagente.

## M0 (periodos) y M4 (largo plazo), hecho (2026-10-13)
- **Hecho:** `src/v8/m0_periodos.py` (~2,5 min) y `src/v8/m4_largo_plazo.py` (~50 s); salidas en `output/v8/M0/` y `output/v8/M4/` (coeficientes, registro, resultado.json, resumen.md; M0: periodos_detectados, regla_m0, heterogeneidad_Q, replica_segunda_particion; M4: atribucion `contabilidad_lp` y `contabilidad`, cointegracion, discrepancias_dols_fmols, fuera_muestra, raices_unitarias, contabilidad_hogares_*). Tests `tests/v8/test_m0.py` y `test_m4.py`. Desviaciones (tasa de paro no disponible, representantes de familia, estadistico de permutacion por periodo, definicion de confirmacion, SERPAVI no evaluable) en desviaciones.md.
- **Aviso de herramienta (resuelto):** `ms_fit` no era determinista con statsmodels 0.15; corregido en la herramienta (commit 213ac84).
- **Siguiente:** integrar `atribucion.csv` de M4 (`contabilidad_lp`, `contabilidad`) y `regla_m0.csv` en la sintesis; ECM v1 no replicable en la misma muestra (declarado).
- Tokens de subagente: no medidos por el subagente.

## F5 (atribución y «factor más relevante»), hecho (2026-10-13)
- **Hecho:** `src/v8/f5_atribucion.py` (~4 s), salidas en `output/v8/F5/` (atribucion_combinada, regla_s9, ranking, regional_ranking, fuera_muestra_comun, fichas.md, resultado.json, registro.csv, resumen.md, tiempos.json), `tests/v8/test_f5.py` (15 tests), `f5_atribucion` añadido a V8_ORDEN. Regla R0-R8 aplicada tal cual (desviaciones.md, dos filas nuevas con las precisiones de aplicación y el diseño de la tabla común J7 anotadas antes de calcular).
- **Resultado:** 0 factores designados de 10 celdas (compra y alquiler nacional, P1-P5). Ningún factor reúne 3 de 4 votos (máximo 2). Tabla común fuera de muestra: AR(4) es la base más exigente en ambos mercados; ECM v1 (v7 A) y BVAR de M2 no la superan.
- **Siguiente:** revisión de F5 por el orquestador; síntesis.
- Tokens de subagente (F5): no medidos por el subagente.

## F6 (congelación de predicciones y `make evaluate_v8`), hecho (2026-10-13)
- **Hecho:** `src/v8/f6_congelar.py` (AR(4), AR + factor común, ECM v1 con datos hasta 2026T2; BVAR de M2 por referencia con sha256), salidas en `output/v8/congelacion/` (predicciones_congeladas.csv, congelacion.json, manifiesto.json, ensayo_evaluate.md); `sha256_predicciones_v8` rellenado en `docs/v8/notas_release.md` (`fecha_verificable` sigue PENDIENTE); `src/v8/evaluate_v8.py` (+ `--simular`), `docs/v8/evaluate_v8_accesos.md` (sin aperturas); `tests/v8/test_f6_congelar.py`.
- **Siguiente:** añadir `f6_congelar` a V8_ORDEN y el target `evaluate_v8` en el Makefile; publicar la release (autor) y, con datos 2026T3-2027T2, ejecutar `make evaluate_v8` una sola vez.
- Tokens de subagente (F6): no medidos por el subagente.

## F6 (tablas de modelos destacados), hecho (2026-10-13)
- **Hecho:** `src/v8/f6_tablas.py` (~5 s) -> `output/v8/tablas_modelos_destacados.{md,csv}`, `output/v8/tablas_v8.xlsx` (9 hojas, colores azul/negro/verde, sin paneles, sha256 determinista), `output/v8/F6/resultado.json`; `tests/v8/test_f6_tablas.py`. Resultado: 0 modelos cumplen la regla de §8 y la del multiverso a la vez; 18 modelos destacados por (b) (error fuera de muestra), todos «NO CUMPLE LA REGLA».
- **Siguiente:** añadir `f6_tablas` a V8_ORDEN.
- Tokens de subagente (F6 tablas): no medidos por el subagente.

## F6 (integración en cifras y publicación), hecho (2026-10-13)
- **Hecho:** `src/v8/f6_hechos.py` -> `output/v8/F6/hechos.json` (ids `V8-`, leídos de output/v8; capas C3s y C4); `src/v5/cifras_clave.py` recoge también `output/v8/*/hechos.json` (filas no V8 idénticas: diff = 0; `check_v5` y `tests/test_k4a_cifras.py` aceptan la capa `C3s` y la banda SHAP); `src/v8/render_v8.py` (reutiliza `src/v5/render.py`) + `docs/v8/plantillas/{README,ensayo}.md` (README con la lista generada de ids); `src/v8/f6_verificador.py` -> `output/v8/verificador_v8.md` y `fichas_verificador_v8.json` (9 fichas V8-V1..V9) y adenda V8 en `docs/v6_1/historial_conclusiones.md`; `src/v7_1/publicacion.py` con el verificador V8, las tablas y la metodología V8 (`por_que_ha_subido.md` e `informe_econometrico_v8.md` comentados hasta que existan). Tests: `tests/v8/test_f6_hechos.py`, `tests/v8/test_f6_verificador.py`, `tests/v7_1/test_publicacion.py`.
- **Siguiente:** el orquestador escribe `docs/v8/plantillas/por_que_ha_subido.md` e `informe_econometrico.md` (ids en el README), activa sus líneas en `publicacion.py` y ejecuta `make publicacion`.
- Tokens de subagente (F6 integración): no medidos por el subagente.
