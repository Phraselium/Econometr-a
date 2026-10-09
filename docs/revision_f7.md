# Revisión F7 (puerta final): `output/informe.md`

Revisor independiente (opus). Fecha: 2026-10-09. Commit revisado: `e5b138e`.

## Veredicto: **REHACER** (acotado)

La reproducibilidad y la trazabilidad están bien: todo se reproduce exactamente y no hay ninguna cifra inventada. Pero el informe final tiene:
- una contradicción factual sobre un diagnóstico clave (el ect real desde 2014);
- código Python sin evaluar en el texto;
- una referencia fantasma;
- una tabla de robustez cuya única celda «sí» sale de comparar especificaciones nominales con la base real.

Todos los cambios son de `src/report.py` y `docs/limitaciones.md` (texto y ensamblado de tablas). Ninguna estimación cambia, salvo, opcionalmente, guardar coeficientes que ya se estiman (cambio 4).

---

## 1. Reproducibilidad: OK

- Hice una copia aislada (`git clone` local de `e5b138e`) en el scratchpad, sin red (`HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9`) y sin `FORCE`.
- Ejecuté `make all` dos veces: **exit 0 en ambas** (≈3,5 min cada una). Todas las descargas salen de `[cache]`.
- Los md5 de `output/informe.md`, `output/tablas/*.csv` (11) y `output/registro_busqueda.csv` son **idénticos entre las dos ejecuciones e idénticos a lo versionado**.
- `git status` del clon queda limpio tras las dos ejecuciones: `data/processed`, `output/f*` y `docs/diccionario_variables.md` también son bit a bit iguales a lo versionado.
- El registro tiene 3.812 filas (F2 3.483 = 1.728 + 1.728 + 27; F3 150; F4 128; F5 23; F6 28), igual que el informe.

## 2. Trazabilidad: OK (11 cifras, ninguna inventada)

| # | Cifra en el informe | Tabla de output | Resumen de fase / revisión |
|---|---|---|---|
| 1 | LP real: empleo 1,4824 (0,3301); costes −0,6598 (0,2512) | `f2/ecuacion_real.csv`; `tablas/ecuacion_final_lp.csv` | Coincide con el DOLS de control de `revision_f2.md` R4(b) (1,48/0,33; −0,66/0,25) |
| 2 | ect real −0,1064 (0,0348), p = 0,002 | `f2/ecuacion_real.csv`; `f2/real_robustez.csv` | `comparacion_nominal_real.csv` |
| 3 | Bootstrap de la selección 9,6 % (real) / 1,5 % (nominal) | `f2/comparacion_nominal_real.csv` (0,0961 / 0,0150) | `resumen_f2.md` l. 26 (1,5 % nominal) |
| 4 | DM frente a AR(4): p = 0,509; RMSE 0,0244 frente a 0,0165 | `f2/real_oos_dm.csv` | — |
| 5 | Chow 2014Q1 real p = 0,004 (F = 3,09) | `f2/real_chow.csv` | — |
| 6 | Déficit 866.100; ECP 810.936; diferencias 116.100 = 55.164 + 60.936 | `tablas/deficit.csv` | `f4/resumen_f4.md`; `limitaciones.md` |
| 7 | IV 2SLS IPV −1,615 (1,078), F = 17,9, IC [−3,90; 0,67] | `f3/panel_primera_etapa.csv`; `f3/ic95_2sls_principal.csv` | `resumen_f3.md` |
| 8 | Holm mínimo 0,051 sobre 150 | `f3/correccion_busqueda.csv` (min p_holm = 0,05095; 150 filas) | `resumen_f3.md` |
| 9 | Panel b2 0,0011 (0,0040), p wild 0,774; poolability p wild 0,363 | `f5/tabla_fe_principal.csv`; `f5/poolability.csv` | `resumen_f5.md` |
| 10 | València: beta frente a España 1,729 (0,105) | `f6/beta_todos.csv` | `resumen_f6.md` (1,73) |
| 11 | Iniciadas: Δ4 1,39 (0,63), Holm H0 = 0,45: p = 0,272; DOLS 1,44 (0,21) | `f4/contraste_H0_045_principales.csv` | `resumen_f4.md` (0,273) |

## 3. Honestidad y diagnósticos

**Bien:**
- No hay ninguna lectura causal.
- Los niveles de evidencia de P1-P5 coinciden con `decisiones.md` (F7).
- Se reportan:
  - BG/RESET/VIF del DOLS real (§3.5);
  - el cambio de signo del ect antes de la COVID;
  - Bonferroni (K por término);
  - el 9,6 % del bootstrap de la selección;
  - que no mejora al AR(4) fuera de muestra;
  - EG, Johansen y ARDL, nominal y real (§3.4);
  - las interpolaciones;
  - los datos no validados (§2).

**Problemas:**

- **(A) Contradicción sobre el ect desde 2014 [bloqueante].**
  - §7.2 y `f2/real_robustez.csv`: ECM real 2014Q1-2026Q2 con ect = −0,1117 (0,0291), **p < 0,001**.
  - §9 (bloque real, copiado de `limitaciones.md`): «…y **no es significativo desde 2014**». Es falso para el precio real.
  - El −0,068 (0,045) de §9 es el ECM **nominal** (`f2/estabilidad_muestras.csv`), y se presenta sin etiqueta.
  - Además, el ECM real 2014+ usa el ect de la muestra completa (no lo re-estima, `src/f2_nacional.py` l. 1002), a diferencia del pre-COVID. Hay que decirlo.
  - Lectura correcta:
    - real: el ect cambia de signo antes de 2020 y es significativo desde 2014, con ect de muestra completa;
    - nominal: no es significativo desde 2014.
- **(B) Bloque F2 nominal de §9 sin etiquetar.** «1,5 %», «Chow p = 0,012» y «RESET rechaza en la ecuación preferida» son del modelo **nominal**. Al lado del 9,6 % y del RESET p = 0,184 del real, el lector los toma por contradicciones. Hay que titular ese bloque «precio nominal (réplica)».
- **(C) §7.2, ect recursivo.** `f2/ect_recursivo.csv` es el ECM **nominal** (termina en −0,0968). Se presenta dentro de la estabilidad real sin etiqueta.
  - La frase «el DOLS cambia de signo en costes y permisos antes de 2020 (`f2/dols_subperiodos.csv`)» no se cumple en ese archivo: en permisos, k = 1 nominal da 0,1145 → 0,0172, el mismo signo.
  - Sí se cumple en `f2/robustez_quiebres.csv` (nominal, k = 2). Para el real pre-COVID cambian permisos y tipo, no los costes.
- **(D) Raíces unitarias ausentes.** El informe no menciona que `ln_ipv_real` sale «ambigua» (Zivot-Andrews rechaza con quiebre en 2015Q1). Era la condición (c) de la re-revisión de F2.
- **(E) P5: 2008 no se trata.** La pregunta incluye 2008, pero la muestra principal empieza en 2008Q1, así que el quiebre de 2008 no es contrastable. Hay que decirlo explícitamente. También falta advertir de la baja potencia en 2022Q3 (n2 = 16).

## 4. Ecuación final y tabla de robustez

**Ecuación final:** correcta. Lleva coeficientes, EE HAC(4), IC95 % y p. En el LP añade Bonferroni/Holm sobre la familia de 8 pendientes; en el CP, K por término. Advierte de que el DOLS falla BG, RESET y VIF.

**Tabla de robustez:** induce a error.

- **(F) [bloqueante] Mezcla de conceptos en las columnas.**
  - Filas de LP con base **real**: la columna `desde_2014` toma el DOLS **nominal** k = 1 (`report.py` l. 440-462), y `dummies_EPA21_tipos22` también es nominal.
  - Fila «Empleo CP»: base real Δocupados(t−1), pero `pre_COVID`, `desde_2014` y `nominal` son Δocupados(t) **nominal** (l. 499-500).
  - La única celda «sí» del informe (y el «sobreviven 1» del resumen ejecutivo) sale por tanto de comparar otra variable (t frente a t−1) con otro precio.
  - Los ECM reales pre-COVID y 2014+ existen (`real_rob_preCOVID`, `real_rob_3` en el registro), pero solo se guarda el ect.
  - En «Costes» los «3 cambios de signo» comparan costes nominales con reales.
  - La marca `{nominal}` está en la celda, pero la regla la cuenta como alternativa de muestra.
- **(G) La regla no incorpora la búsqueda.** Una fila puede quedar en «sí» aunque ningún término sobreviva a Bonferroni (Empleo CP: p_Bonf = 1). Con K = 576-1.728 y el 9,6 % del bootstrap, «sí» transmite más solidez de la que hay.
- **(H) Menor.** Las celdas pre-COVID LP «sin p» cuentan como no-fallo.
  - `n_cambios_signo` = 0 en «Tipo» aunque hay valores de los dos signos: solo se calcula cuando la base es significativa. Conviene dejar NA.
  - El marcado «~» de los p aproximados por la normal está claro.

## 5. P3 frente al BdE

- 750.000 (IA 2025, p. 157) y 700.000 (IEF otoño 2025) están citados.
- La diferencia de 116.100 se documenta sin ajustar y se descompone en 55.164 (fuente de hogares) + 60.936 (protegidas). Ambas descomposiciones se marcan como inferencia.
- 0,45 con Caldera-Johansson (2013) y Cavalleri et al. (2019) figura como **NO VERIFICADA** (§5.3, §10.9, referencias).
- **(I) Menor.**
  - La diferencia con el IEF (166.100, en `tablas/deficit.csv`) no aparece en el texto.
  - 60.936 es un **residuo** (BdE implícito − nuestras terminadas; incluye el redondeo de «750.000»). Debe decirse «residuo atribuido a…», no «por la vivienda protegida».

## 6. Referencias

- **(J) [bloqueante, trivial] «Kinnon (1996)» [NO VERIFICADA] es un artefacto del patrón `Autor (año)` sobre «MacKinnon (1996)».** Infla el recuento («NO VERIFICADA: 3»; deben ser 2).
- Por lo demás, `tablas/referencias.csv` coincide con `docs/literatura.md`: Caldera-Johansson y Cavalleri NO VERIFICADAS; IEF, Bover-Jimeno y Martínez Pagés PARCIAL.

**Comprobación web (4):**
- González y Ortega (2013), *JRS* 53(1), 37-59: correcta según IZA DP 4333 ([IZA](https://www.iza.org/en/publications/dp/4333/immigration-and-housing-booms-evidence-from-spain)).
- Juodis y Reese (2022), *JBES* 40(3), 1191-1203, DOI 10.1080/07350015.2021.1906687: correcta ([Lund](https://portal.research.lu.se/en/publications/the-incidental-parameters-problem-in-testing-for-remaining-cross-/)).
- BdE IA 2025, DOI 10.53479/43565: resuelve a «Informe Anual 2025», 18/06/2026 ([repositorio BdE](https://repositorio.bde.es/handle/123456789/43565)). Las cifras de pp. 155-157 no se re-verificaron aquí.
- Caldera y Johansson (2013), *JHE* 22(3), 231-249: el registro bibliográfico existe ([IDEAS](https://ideas.repec.org/a/eee/jhouse/v22y2013i3p231-249.html)). Estima la elasticidad de la **construcción nueva** con un modelo stock-flujo (WP OCDE 837), lo que apoya la inferencia «flujo/inversión» de §5.3.
  - El valor 0,45 para España no se comprobó, así que debe seguir NO VERIFICADA en cuanto al contenido.
  - Opcional: anotar «existencia bibliográfica comprobada (IDEAS)».

## 7. «Qué NO se puede afirmar»: incompleta

**(K)** Hay que añadir:
- que el crédito **cause** el precio: es comovimiento simultáneo y en t−1 cambia de signo;
- que la elasticidad de largo plazo al empleo tenga una magnitud precisa: 0,83-3,53 entre muestras;
- que los tipos de interés no importen a largo plazo por el tipo real ≈ 0: la relación es estadística y la especificación no está identificada;
- que la C. Valenciana se encarezca más o menos que España: el signo depende de la medida (IPV −14,1 pp frente a valor tasado +12,2 pp desde 2014);
- que exista un déficit **en niveles** de 866.100: es un flujo acumulado y requiere un equilibrio inicial. El punto 8 actual solo lo insinúa.

---

## Cambios requeridos (priorizados)

1. **(A + B) Corregir el ect desde 2014 y etiquetar nominal/real en §9.**
   - En `docs/limitaciones.md`, bloque real, sustituir «y no es significativo desde 2014» por «desde 2014 sigue siendo significativo (−0,112, EE 0,029; ect de la muestra completa, no re-estimado); en precio nominal deja de serlo (−0,068, EE 0,045)».
   - Titular el bloque F2 antiguo «precio NOMINAL (réplica)».
   - En §7.2, añadir que la fila 2014+ usa el ect de la muestra completa.
   - Revisar el resumen ejecutivo, §10.4 y `decisiones.md` (F7, P5), que no deben dar a entender que el ect real se pierde desde 2014.
2. **(J + bug) `src/report.py`.**
   - l. 1018: falta el prefijo `f` y sale código literal en §3.4. Corregirlo.
   - Excluir «Kinnon (1996)» (el patrón debe exigir un límite de palabra o ignorar coincidencias contenidas en una referencia conocida). Recuento esperado: 42/11/2.
3. **(F + G) Tabla de robustez.**
   - Las columnas `pre_COVID`, `desde_2014` y `dummies_EPA21_tipos22` deben usar el mismo concepto de precio y el mismo regresor que la base. Si no existe, `n/d`; la comparación nominal solo en la columna `nominal`.
   - Para Empleo CP real: guardar en `f2` los coeficientes de `d_ln_ocupados_l1` de `real_rob_3` y `real_rob_preCOVID`, que ya se estiman, o marcar n/d.
   - Para el LP real 2014+: n/d, o DOLS real 2014+ si ya existe.
   - Añadir a la regla: «como máximo "parcial" si el término no sobrevive a la corrección por búsqueda de su fase (Bonferroni K o Holm)».
   - Regenerar el resumen ejecutivo («sobreviven…»).
4. **(C + D + E) Texto de P1/P5.**
   - Etiquetar el ect recursivo como nominal.
   - Corregir la frase de los signos por subperíodo (citar `robustez_quiebres.csv` nominal k = 2 y el LR real pre-COVID: cambian permisos y tipo).
   - Añadir en §3.4 el orden de integración (`ln_ipv_real` ambigua; ZA 2015Q1; el bounds test vale con I(0)/I(1)).
   - En §7, decir que 2008 no es contrastable con la muestra principal (empieza en 2008Q1) y que la potencia en 2022Q3 es baja (n2 = 16).
5. **(K + I) Completar §10** con los cinco puntos de la sección 7. En §5.1:
   - añadir la diferencia con el IEF (166.100, periodo y fuente distintos);
   - llamar «residuo» a los 60.936;
   - en §4.1, etiquetar los dos IC del 2SLS (normal frente a t con 16 gl).

Menores, no bloqueantes:
- `n_cambios_signo` = NA cuando la base no es significativa.
- En el resumen ejecutivo, «Chow… (2014Q1: p = 0,004)» repite la fecha.
- Añadir junto a 1,482 «magnitud no robusta».

Tras aplicar 1-5, basta con repetir `make all` y comprobar el diff de `informe.md`/`robustez.csv`. No hace falta una revisión econométrica nueva.
