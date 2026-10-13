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
- F3 cerrada (Y6, Y7; `make check` rc=0, 168 passed).
- F4: los diez módulos M0-M9 están hechos y en `make v8` (V8_ORDEN). `ms_fit` corregido en la herramienta: ahora es determinista (M0 re-ejecutado, mismas salidas). Corriendo en paralelo: la puerta `make check` y el revisor opus de F4 (docs/v8/revision_F4.md).
- Resumen F4 (todo C4 salvo M2, que es C3s):
  - M2: H8-1…H8-4 no respaldadas (p Holm 0,43-0,82). En P5 compra domina la parte determinista (Y8).
  - M5: instrumentos débiles; H8-5…H8-7 no rechazadas.
  - M1: H8-8 no rechazada; H8-9 rechazada (r = 0,60; p Holm 0,020).
  - M0: 2 de 70 efectos por periodo cumplen la regla, 0 tras BH.
  - M7: 3 de 74 combinaciones cumplen el multiverso.
  - M9: ningún ML supera a la base más exigente.

## Siguiente paso exacto
- Revisión F4 hecha (docs/v8/revision_F4.md): APROBAR CON CORRECCIONES, M2 REHACER (J1: el escalón EPA creaba la «parte determinista» de P5). Desviaciones, Y9 y la regla operativa de F5 (R0-R8) anotadas antes de calcular F5.
- En curso, cuatro subagentes de corrección: M2 (J1, J2, prob_mayor); F1+M0+M5 (J8, J9, J3, J4, J18); M3+M6+M7 (J5, J6, J15-J17); M1+M4+M8+M9 (J10-J13, J19, J23).
- Al terminar: `make check`, commit y push de la puerta F4. Después F5 (`src/v8/f5_atribucion.py` con R0-R8 y la tabla común AR(4)/ECM v1 de J7).

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
