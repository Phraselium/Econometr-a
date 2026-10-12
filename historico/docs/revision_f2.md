# Revisión independiente de la puerta F2 (ecuación nacional, P1 y P5)

Revisor: reviewer (independiente; no ha participado en la estimación). Fecha: 2026-10-09.
Material revisado: `docs/decisiones.md`, `output/f2/*` (resumen y tablas), `src/f2_nacional.py`, `src/econ_utils.py`, `output/registro_busqueda_f2.csv`, `docs/literatura.md`, `docs/diccionario_variables.md`.
Todas las comprobaciones propias se hicieron con scripts en el scratchpad, sin modificar el código del proyecto.

## Veredicto: **REHACER** (cambios acotados)

La fase está bien construida: es reproducible y determinista, la búsqueda está registrada sobre una muestra común y el OOS no tiene fugas en el largo plazo. Los coeficientes se reproducen al decimal. Pero la conclusión central sobre cointegración del vector principal está mal calculada: hay un error de código en el ARDL bounds y, una vez corregido, la regla prerregistrada da **«evidencia mixta (1/3)»**, no «cointegración (2/3)». Además, el regresor más estable del corto plazo (crédito nuevo contemporáneo) tiene un problema de simultaneidad que no se trata. Hay tres cambios bloqueantes y todos son pequeños.

---

## 1. Reproducibilidad: OK

- Ejecuté dos veces `HTTPS_PROXY=http://127.0.0.1:9 make all` y las dos terminaron con exit 0 (F2 tarda unos 63 s). Las 45 salidas de `output/f2` y el registro dan **md5 idénticos** entre las dos ejecuciones.
- Tras las ejecuciones, `git status` solo cambia `output/registro_busqueda_f2.csv`. El commit tiene **1.737 filas** y el código genera **1.741**: el registro versionado está desfasado. El resto de `output/f2` (PNG incluidos) coincide byte a byte con lo versionado.
- Hay una incoherencia interna en el resumen. La cabecera dice «1741 especificaciones» y la sección 5 dice «1737 filas en total al terminar la fase». Esa cifra se calcula a mitad de la ejecución, antes de registrar los 4 modelos de robustez.

## 2. Datos e interpolaciones: OK, con dos matices

- Contrasté con `data/raw` cuatro cifras de `nacional_q`, y las cuatro cuadran:

| Cifra | Valor en `nacional_q` | Comprobación en `data/raw` |
|---|---|---|
| ocupados 2024Q2 | 21.684,7 | EPA387796 |
| IPV 2021Q1 | 71,055 | IPV1209 |
| tipo_hip 2019Q4 | 1,7567 | media de 1,82, 1,77 y 1,68 (MIR mensual) |
| credito_nuevo 2024Q2 | 17.675 | 6.031 + 5.711 + 5.933 |

- **Población interpolada antes de 2021.** La búsqueda incluye Δ1 y Δ4/4 de `ln_pob_extranj` como alternativas excluyentes, como estaba fijado. Matiz: `d_ln_pob_total` también está interpolada antes de 2021 (52 trimestres, según el diccionario) y tiene la misma MA mecánica. La lista de problemas solo lo dice para la población extranjera.
- **Quiebre EPA 2021.** En el DOLS, `epa21` entra en niveles, que es lo correcto para un salto de nivel. En el ECM entra como escalón dentro de una ecuación en diferencias, y eso es un cambio de deriva del precio desde 2021, no una corrección del salto de la EPA. Para corregir el salto habría que usar un impulso en 2021Q1. Lo comprobé: un impulso en 2021Q1 da 0,001 (0,003) y no cambia nada; Δln ocupados en 2021Q1 (−0,0054) está en el rango de otros primeros trimestres. Conclusión: el quiebre de la EPA no afecta al corto plazo. Hay que redactar así el coeficiente `epa21 = 0,0078`, que es un «cambio de deriva posterior a 2021» y no un «efecto EPA».

## 3. Estacionariedad y cointegración: **BLOQUEANTE**

**3.1 El orden de integración usa las series largas: OK.**
- `ln_p_tasado` 1995-2026 sale I(1). `ln_ipv` (solo desde 2007) sale «ambigua» en las dos muestras, así que tratarla como I(1) se apoya en la serie larga de tasación. Es razonable.
- `tipo_hip` es ambigua en 2008+ (el ADF rechaza) y sale I(1) en la muestra desde 2003. Conviene añadir una frase sobre ello.

**3.2 Error de código en el ARDL bounds (`coint_system`, `src/f2_nacional.py`).** Hay tres fallos, y los he reproducido todos.

1. **Desalineación de órdenes.** `ardl_select_order` puede excluir regresores. Cuando lo hace, `ardl_order` solo trae los órdenes de los regresores incluidos. Luego `zip(xs, o[1:])` asigna esos órdenes a variables equivocadas y deja fuera la última del vector. Por ejemplo, en «+renta» `ln_renta_hog_real` desaparece del UECM, y por eso su F (3,85) es idéntico al de la base. En el sistema real, `ln_costes_real` también se pierde.
2. **Se pierden las dummies estacionales.** `UECMResults.bounds_test` re-estima internamente el UECM sin el argumento `fixed`. El F publicado sale de un modelo sin dummies trimestrales, en contra de lo que dice el texto.
3. **El valor crítico usa una k de más.** statsmodels 0.15 usa `k = len(ardl_order)`, es decir, cuenta también la variable dependiente. Con 4 regresores aplica el valor crítico de k = 5 (I1 al 5 %: 3,79) en vez del de k = 4 (4,01). Las tablas de statsmodels están indexadas por el número de regresores x; la cota de 4,01 cuadra con PSS (2001), caso III.

Recalculé el F de Wald sobre los niveles retardados, en el UECM con dummies trimestrales, con todos los regresores con orden ≥ 1 y con el valor crítico de la k correcta:

| Sistema (2008Q1-2026Q2) | F publicado | F corregido (con q) | I0 / I1 al 5 % | ARDL |
|---|---|---|---|---|
| ln_ipv base (principal) | 3,85 «rechaza» | **3,25** | 2,88 / 4,01 | **no concluyente → no rechaza** |
| ln_ipv +renta | 3,85 | 2,65 | 2,64 / 3,79 | no rechaza |
| ln_ipv +pob_extranj | 3,88 | 6,52 | 2,64 / 3,79 | rechaza |
| ln_ipv +pob_total | 7,47 | 5,12 | 2,64 / 3,79 | rechaza |
| ln_ipv_real base | 2,67 «no rechaza» | **7,20** | 2,88 / 4,01 | **rechaza** |
| ln_p_tasado base (2003+) | 2,79 | 3,30 | 2,88 / 4,01 | no concluyente |

**Consecuencias.**
- Para el vector **principal** (nominal), EG no rechaza (p = 0,40), el ARDL no rechaza y Johansen sí rechaza. Eso es **1/3**, que según la regla prerregistrada es «evidencia mixta».
- El argumento del resumen («EG no, Johansen y ARDL sí») queda invalidado.
- En cambio, la versión **real** pasa a tener EG p = 0,023, ARDL F = 7,2 (t de y.L1 = −5,2) y Johansen a favor: **3/3**. Es la evidencia más sólida de una relación de nivel en F2. No pido cambiar la especificación principal, porque está fijada antes de estimar y cambiarla ahora sería selección ex post, pero hay que destacarlo.

**3.3 Johansen.** Rechaza r = 0 con k_ar_diff de 1, 2 y 4 y con det_order 0 y 1, también con la corrección de Reinsel-Ahn salvo en un caso (k = 1, det = 1, rango 0). Pero estima rangos de 2 a 4 en un sistema de 5 variables tratadas como I(1). Eso no es coherente con la clasificación I(1) y apunta a sobre-rechazo o a mala especificación con N ≈ 74. El texto ya lo dice; con esta fragilidad, Johansen no puede ser el único apoyo de la cointegración.

**3.4 ¿Es defendible un ECM con evidencia mixta?** Sí, pero solo con esta redacción:
- Es un «ECM condicional / ARDL con término de desequilibrio respecto a una relación de nivel no confirmada».
- El t del ect (−3,13) **no** tiene distribución normal bajo la nula de no cointegración, así que su p = 0,0017 no prueba nada. Su referencia es la tabla de Banerjee, Dolado y Mestre (1998), con valores críticos bastante más negativos que −1,96.
- Además, el LR es inestable. Bai-Perron encuentra 3 quiebres en niveles (2012Q1, 2020Q2 y 2023Q2). En pre-COVID, costes y permisos cambian de signo (−0,418 y −0,027). Con +pob_extranj, costes pasa a −0,913.
- La lectura honesta es que el ect captura una reversión parcial hacia una tendencia común inestable, no hacia un equilibrio estructural.

## 4. Endogeneidad: **BLOQUEANTE (parcial)**

- El DOLS (±2) trata la endogeneidad de los regresores en el largo plazo solo si hay cointegración, que aquí es dudosa (punto 3). Mejor no presentarlo como «resuelto».
- **El crédito nuevo contemporáneo es simultáneo con el precio.** El volumen de crédito nuevo equivale a operaciones × importe medio, y el importe medio depende del precio. Lo comprobé (mismas N = 73 y HAC(4)):
  - Si se usa `d_ln_credito_nuevo(t−1)` en lugar de t, el signo **se invierte**: −0,024 (0,014) en el preferido con regresores predeterminados y −0,027 (0,011) en el ganador BIC.
  - La regresión inversa Δln crédito ~ Δln IPV da 4,02 (0,84).
  - Por tanto, el «+0,041» del crédito es comovimiento contemporáneo, no un determinante predeterminado.
- Ocupados(t−1) en lugar de t baja el coeficiente de 0,474 a 0,235 (0,106), con el mismo signo.
- En el OOS, el preferido usa crédito y empleo observados en t: es predicción condicional sobre regresores simultáneos. Está declarado, pero favorece al modelo, que aun así pierde frente al AR(4).

## 5. Autocorrelación, heterocedasticidad, normalidad y RESET: aceptable, con limitaciones anotadas

| Modelo | BG(4) p | BP p | JB p | RESET p |
|---|---|---|---|---|
| Preferido | 0,11 | 0,89 | 0,33 | **0,028** |
| Réplica ECM con q | **0,0008** | — | **3,7e-10** | — |
| Pre-COVID | **0,015** | — | — | — |

- En el preferido, la forma funcional es dudosa (RESET).
- En la réplica con q, la autocorrelación probablemente es de orden 4; puede probarse añadiendo `d_ln_ipv_l4`.
- En pre-COVID hay autocorrelación con un retardo de la dependiente entre los regresores. En ese caso el HAC no arregla la inconsistencia: basta con aplicarle el mismo procedimiento de aumento de retardos que al preferido.
- Los residuos del DOLS tienen DW 0,71 y BG p = 2e-6. Un HAC con 4 retardos puede quedarse corto, así que conviene reportar también un ancho de banda automático (Andrews o Newey-West automático) en el DOLS.

## 6. Quiebres: correctos en cálculo, incompletos en interpretación

- **Chow 2014Q1** (F = 2,60, p = 0,012) rechaza la estabilidad del ECM preferido. El resumen **no lo discute**: solo habla de la baja potencia en 2022Q3. Hay que decirlo, y añadir como robustez el ECM sobre 2014Q1-2026Q2 (N = 50), o al menos el ect y los términos estables interactuados con el tramo.
- **Bai-Perron** da 0 quiebres en el ECM por BIC. El BIC es conservador y tiende a infraestimar quiebres, así que no contradice al Chow con fecha conocida. En el LR da 3 quiebres: es otro argumento contra un vector de cointegración estable (punto 3.4). Como robustez opcional, puede usarse el contraste de cointegración con cambio de régimen de Gregory y Hansen (1996).
- Las dummies `epa21` y `tipo22` y la versión pre-COVID están presentes y bien construidas (el ect pre-COVID se re-estima solo con datos hasta 2019Q4). En pre-COVID el ect baja a −0,054 (p = 0,032).

## 7. Misma muestra: OK en la búsqueda; un detalle en la tabla de LR

- En el registro, los 1.728 modelos `busq_*` tienen **N = 73 y 2008Q2-2026Q2, sin excepciones**.
- La comparación DOLS 1,951 frente a EG 0,878 se hace en la **misma** muestra (2008Q1-2025Q4, N = 72): correcto.
- En `largo_plazo.md`, en cambio, las columnas EG estático (const/+q) usan N = 74 (hasta 2026Q2) y el UECM implícito usa N = 70, frente a N = 72 del DOLS. Hay que re-estimar las columnas EG en la muestra del DOLS o indicar N en cada columna.

## 8. Errores estándar HAC(4): OK

Todos los coeficientes reportados usan Newey-West con 4 retardos; los diagnósticos se hacen sobre MCO clásico, y así se declara. El único matiz es el ancho de banda del DOLS (punto 5).

## 9. Sobreajuste, bootstrap y OOS

**Qué se puede afirmar con un bootstrap del 1,5 %.** Que la especificación concreta del preferido (busq_0652) **no está identificada por los datos**: ningún modelo gana más del 3,7 % de las réplicas. Solo son defendibles afirmaciones **por término**:

| Término | Afirmación sostenible | Base |
|---|---|---|
| Δ empleo (t o t−1) | Asociación positiva robusta | Gana en el 99 % de las réplicas (75,5 % t + 23,8 % t−1); IC post-selección [0,21; 2,0] en t; EBA: 98,8 % de modelos significativos, aunque los límites de Leamer cruzan 0 |
| Persistencia de Δ precio (l1 o l4) | Robusta | 91 % de las réplicas; EBA robusto |
| Δ crédito nuevo **contemporáneo** | Comovimiento robusto, **no** determinante | 94,7 % de las réplicas, IC [0,011; 0,071], pero el signo se invierte en t−1 (punto 4) |
| ect | Signo negativo en los 1.728 modelos (−0,25 a −0,08) | Está **forzado** en todos los modelos, así que su frecuencia de 1,0 no informa. IC bootstrap [−0,297; 0,0004], que toca 0 |
| Costes, renta, permisos, tipo (corto plazo), población (cualquier medida) | **Sin evidencia** | Frecuencias del 10 al 59 %, signos inestables, límites de Leamer cruzan 0 |

**Bonferroni.** Con K = «modelos que contienen el término», Bonferroni es una cota muy conservadora y conceptualmente imperfecta: no son K hipótesis independientes, sino el mismo coeficiente en especificaciones anidadas. Para el ect (forzado) no tiene sentido. Hay que presentarlo como cota y dar prioridad al bootstrap de la selección. La frase «El coeficiente del ect no sobrevive a Bonferroni» debe matizarse.

**OOS y fugas de información.**
- **Largo plazo sin fuga:** en cada origen T, `build_ect(Fw, T−1)` estima el DOLS con datos hasta T−1 (con adelantos, la muestra termina en T−3). El ect(t−1) solo usa niveles en T−1, y los coeficientes de corto plazo se estiman con t < T. Lo verifiqué en el código.
- **Fuga de selección (hay que declararla):**
  1. El preferido se eligió por R² ajustado sobre toda la muestra, incluidos 2018-2026, así que el OOS del preferido es pseudo-OOS.
  2. La fila «Mejor RMSE OOS» se elige con los propios errores fuera de muestra: es un óptimo ex post, no evidencia de capacidad predictiva.
- **Resultado no comentado:** el preferido **no mejora al AR(4) + dummies** (RMSE 0,01317 frente a 0,01171; DM = 1,08, p = 0,29) y empata con el paseo con deriva (p = 0,98). Solo bate a la media histórica.

## 10. Signos y magnitudes frente a `docs/literatura.md`: hay que marcar discrepancias

| Variable | Esperado | Estimado | Discrepancia |
|---|---|---|---|
| Empleo, largo plazo | + | DOLS 1,95 (0,48); EG 0,88 (0,31); rango entre especificaciones 0,84 a 2,67 | Signo correcto. **`literatura.md` no tiene magnitud de referencia** para la elasticidad al empleo, así que no se puede contrastar. La magnitud no es robusta: depende del estimador y del vector (+renta 0,94; pre-COVID 2,52) |
| Permisos (t−4), largo plazo | − | EG +0,163 (significativo); DOLS +0,059 (no significativo) | **Signo contrario.** Lo coherente es causalidad inversa (los permisos responden al precio; véase Bover y Jimeno 2007 sobre la reasignación hacia construcción), no un efecto de oferta |
| Costes, largo plazo | + | Base +0,27 (no significativo); +pob_extranj −0,91; pre-COVID −0,42 | **Inestable**, con signo contrario en dos variantes |
| Costes, corto plazo | + | −0,105 (p = 0,054) | **Signo contrario**, no robusto (47 % de signos positivos en el EBA) |
| Renta, corto plazo | + | −0,088 (p = 0,28) | **Signo contrario**, no significativo; probable colinealidad con Δ empleo. Renta en el largo plazo (DOLS +renta): +1,46, correcto |
| Tipo hipotecario, largo plazo | − | DOLS −0,017 (no significativo); EG −0,042 (significativo) | Signo correcto; la significación se pierde con el DOLS |
| Población extranjera, largo plazo | + | +0,77 (0,15) | Signo correcto; la magnitud no es comparable con Saiz (2007) ni con González y Ortega (2013) por las unidades (lo dice el propio `literatura.md`) |
| ect | Entre −1 y 0 | −0,097 | Correcto (ajuste de un 10 % por trimestre) |

El resumen muestra la columna `signo_esperado` pero **no comenta ninguna de estas discrepancias**.

## 11. Referencias citadas en output/f2

Los métodos citados en `output/f2` solo aparecen por su epónimo. Estas referencias ya están verificadas en `literatura.md`: Engle-Granger, Johansen, Pesaran-Shin-Smith, Zivot-Andrews, Bai-Perron y Newey-West.

Las que se usan en F2 y faltan en `literatura.md` (todas deben añadirse antes de F7):

| Referencia | Estado |
|---|---|
| Stock y Watson (1993), *Econometrica* 61(4), 783-820, DOI 10.2307/2951763 | Verificada (Crossref) |
| Diebold y Mariano (1995), *JBES* 13(3), 253-263, DOI 10.1080/07350015.1995.10524599 | Verificada (Crossref) |
| Harvey, Leybourne y Newbold (1997), *IJF* 13(2), 281-291, DOI 10.1016/S0169-2070(96)00719-4 | Verificada (Crossref) |
| Kwiatkowski, Phillips, Schmidt y Shin (1992), *J. Econometrics* 54(1-3), 159-178, DOI 10.1016/0304-4076(92)90104-Y | Verificada (Crossref) |
| Banerjee, Dolado y Mestre (1998), *JTSA* 19(3), 267-283, DOI 10.1111/1467-9892.00091 | Verificada (Crossref; la propongo yo) |
| Gregory y Hansen (1996), *J. Econometrics* 70(1), 99-126 | Verificada (Crossref; la propongo yo) |
| Leamer (cotas extremas/EBA; 1983 o 1985) | **NO VERIFICADA** (Crossref no devolvió el original) |
| MacKinnon (valores críticos de `coint`) | **NO VERIFICADA** |
| Chow, Breusch-Godfrey, Breusch-Pagan, Jarque-Bera, RESET, CUSUM, Holm, bootstrap de bloques móviles | **NO VERIFICADAS** (solo epónimos) |

## 12. Re-estimación propia (statsmodels, desde `data/processed/nacional_q.csv`, sin `econ_utils`)

| Coeficiente | Publicado | Re-estimado |
|---|---|---|
| EG réplica: ln_ocupados (N = 72, 2008Q1-2025Q4) | 0,8784 | **0,8784**; tipo −0,0418; permisos 0,1564; costes 0,4652 |
| DOLS base: ln_ocupados (HAC(4), N = 72) | 1,951 (0,480) | **1,951 (0,480)** |
| ECM preferido: d_ln_credito_nuevo (N = 73) | 0,04071 (0,01297) | **0,04071 (0,01297)**; ect −0,09679 (0,0309); R² ajustado 0,7485 |

Todo coincide.

---

## Cambios solicitados

### Bloqueantes (por prioridad)

1. **Corregir el ARDL bounds en `coint_system`.**
   - (a) Asignar los órdenes por nombre con `sel.dl_lags` (los regresores excluidos pasan a orden 1, como ya pretende el código).
   - (b) Calcular el F de Wald sobre `y.L1` y los `x.L1` en el UECM **con** `fixed = dummies q` (no usar `bounds_test`, que las descarta), y tomar el valor crítico de `pss_critical_values.crit_vals[(k, 3, ·)]` con k = número de regresores.
   - (c) Reportar también el t de y.L1.
   - Después, regenerar `cointegracion.*` y la decisión 2 de 3. Con mis cálculos, el vector principal queda en **«evidencia mixta (1/3)»** y el real en 3/3.
2. **Reescribir el estatus del largo plazo y del ECM (resumen y problemas abiertos).**
   - Decir «evidencia mixta» para el vector nominal.
   - Explicar que el p del ect no es válido como contraste de cointegración (no es normal; tabla de BDM 1998).
   - Señalar la inestabilidad del LR (Bai-Perron con 3 quiebres; cambios de signo en pre-COVID y +pob_extranj).
   - Destacar que la versión real (robustez prerregistrada) es la única con 3/3 y comparar sus coeficientes con los del nominal.
3. **Tratar la simultaneidad del corto plazo.**
   - Añadir una tabla de robustez, registrada fuera de la K de búsqueda, con `d_ln_credito_nuevo(t−1)` y `d_ln_ocupados(t−1)` en el preferido y en el ganador BIC.
   - En P1, presentar el crédito como comovimiento contemporáneo (el signo se invierte con el retardo), no como determinante.

### No bloqueantes (por prioridad)

4. Añadir al resumen la tabla de discrepancias de signo/magnitud del punto 10 (permisos +, costes −, renta − en el corto plazo; elasticidad al empleo sin referencia en `literatura.md`).
5. **OOS.**
   - Decir explícitamente que el preferido no bate al AR(4) ni al paseo con deriva.
   - Etiquetar «Mejor RMSE OOS» como óptimo ex post.
   - Declarar la fuga de selección (especificación elegida con la muestra completa).
6. **Chow 2014Q1.** Discutir el rechazo (p = 0,012) y añadir el ECM 2014Q1-2026Q2 como robustez.
7. Matizar Bonferroni: es una cota conservadora y no aplica al ect forzado. Corregir la frase «solo ect … entra de forma estable» (el ect es forzado).
8. **Coherencia de cifras y registro.** Calcular el número de filas del registro al final (1.741) y versionar el registro regenerado, porque el del commit tiene 1.737.
9. Igualar la muestra de las columnas EG de `largo_plazo.md` a la del DOLS (N = 72) o indicar N por columna. Reportar el DOLS también con ancho de banda HAC automático.
10. Redactar `epa21` en el ECM como cambio de deriva desde 2021 y no como corrección EPA. Opcional: impulso 2021Q1 (no cambia nada, coeficiente 0,001).
11. Añadir el aumento de retardos para BG en la versión pre-COVID (BG p = 0,015) y anotar la MA mecánica de `d_ln_pob_total` antes de 2021.
12. Añadir a `docs/literatura.md` las referencias de métodos del punto 11, con las verificadas y las NO VERIFICADAS marcadas.

## Afirmaciones sostenibles de P1 y P5 y nivel de evidencia

P5 no está definida en el repositorio. La interpreto como la pregunta sobre la selección o robustez de la especificación y su capacidad predictiva; el orquestador debe confirmarlo.

**P1 (ecuación nacional):**
- **Moderada:** el precio nominal (IPV) se asocia positivamente con el empleo a corto plazo (≈ 0,2-0,5 por trimestre según t o t−1) y tiene una persistencia considerable (≈ 0,44 en Δ precio t−1). Ambas cosas son robustas a la búsqueda y al bootstrap de la selección.
- **Débil o mixta:** hay una relación de largo plazo nominal con empleo (+), tipo (−), permisos y costes, con reversión de ≈ 10 % por trimestre. La cointegración no está confirmada (1/3) y el vector es inestable. La elasticidad LR al empleo es positiva, pero su magnitud (0,84 a 2,67) no es robusta, y la cifra de 1,95 no debe presentarse como estimación puntual fiable. En precios reales la evidencia de una relación de nivel es más fuerte (3/3).
- **No sostenible:**
  - un efecto del crédito como determinante (es simultáneo);
  - efectos de corto plazo de costes, renta, tipo, permisos o población (extranjera o total);
  - el signo «−» de la oferta (los permisos salen con signo +);
  - cualquier lectura causal.

**P5 (selección y predicción):**
- **Sostenible:** la especificación concreta no está identificada (el preferido gana en el 1,5 % de las réplicas). Solo los términos de empleo, persistencia, crédito contemporáneo y ect aparecen de forma sistemática.
- **Sostenible:** en el OOS 2018-2026, la ecuación no mejora a un AR(4) estacional y solo bate a la media histórica.
- **No sostenible:** que el modelo preferido tenga ventaja predictiva o que su R² ajustado (0,749) refleje capacidad explicativa no sobreajustada.

---

# Re-revisión (iteración 2 de 2) — commit 625cb59

## Veredicto final: **APROBAR**, con una condición obligatoria antes de F7 (punto R4)

## R1. Cambios bloqueantes 1-3 y no bloqueantes 4-5: aplicados correctamente

**1. ARDL.**
- Ahora los órdenes se asignan por nombre de variable, el contraste es un F de Wald propio con las dummies trimestrales y el valor crítico usa k = número de regresores x (`crit_percentiles` = (90, 95, 99), así que el índice 1 corresponde al 95 %, que es lo correcto).
- Los F coinciden con los míos: nominal base 3,246, +renta 2,645, +pob_extranj 6,518, +pob_total 5,121, real base 7,199, tasado base 3,295.
- Resultado: nominal **1/3 (evidencia mixta)** y real **3/3**.

**2.** El estado del largo plazo y del ECM está bien redactado: el p del ect no se usa como contraste de cointegración y se reconoce la inestabilidad del largo plazo.

**3.** Hay tabla de crédito (`robustez_credito.md`): en t−1 el coeficiente es −0,029 (0,011); sin crédito, el R² ajustado es 0,652 y el ect −0,120. Se presenta como comovimiento. Es correcto.

**4.** Las tablas `signos_LP` y `signos_CP` marcan las discrepancias de signo.

**5.** El OOS lleva las salvedades (pseudo-OOS, óptimo ex post) y dice que el preferido no bate al AR(4).

**Además:** se discute el Chow de 2014Q1 y se añaden la tabla de estabilidad por muestras y el DOLS por subperíodos.

## R2. Determinismo: OK

- Hice dos ejecuciones aisladas y **simultáneas** de `src/f2_nacional.py`, en copias separadas (`git archive` de HEAD más `data/processed`), sin red. Las dos terminaron con exit 0.
- Las 54 salidas de `output/f2` y el registro (1.748 filas) dan **md5 idénticos** entre sí **y con lo versionado en HEAD**.
- El registro atómico (`os.replace` al salir) y el `flock` de make eliminan el intercalado de filas. Un matiz: si el script falla a mitad, `atexit` escribe un registro parcial. Es aceptable, porque make se detiene.

## R3. Problemas residuales, no bloqueantes (pasan a docs/limitaciones.md)

- Desde 2014Q1 (N = 50), el ect vale −0,068 (0,045) y **deja de ser significativo**, y el crédito contemporáneo desaparece (−0,001). El mecanismo de corrección y el comovimiento con el crédito se apoyan sobre todo en 2008-2013. P1 debe decirlo.
- La variante con crédito en t−1 rechaza BG(4) (p = 0,03), igual que la de sin crédito (p = 0,02).
- Erratas de texto:
  - La sección 5 del resumen sigue diciendo «1737 filas»; la cabecera dice 1.748.
  - El UECM implícito ahora usa EE clásicos, y la columna se sigue llamando `EE_HAC`.

## R4. Valoración de la decisión del orquestador: interpretar en F7 el largo plazo REAL

**Es defendible.**
- La versión real estaba prerregistrada como robustez.
- La regla 2/3 se aplica tal cual.
- Ese 3/3 sobrevive aunque se descarte Johansen, que no es fiable: EG p = 0,023 y ARDL F = 7,2 con t = −5,2 bastan para 2/3.
- Queda documentada como desviación del prerregistro motivada por los contrastes y no por el ajuste.

**Condiciones.**
- **(a) Obligatoria.** `output/f2` no contiene todavía **ninguna estimación de la ecuación real**: ni DOLS real ni ECM con ect real. Hay que añadirla a `src/f2_nacional.py` antes de F7, con su tabla de signos. Sin ella, F7 no puede citar cifras.
- **(b) Hay que avisar de que la relación real es estadística, no estructural.** Mi DOLS real de control (±2, HAC(4), N = 72; no son cifras de output y no deben citarse) da:

| Variable | Coeficiente (EE) | Comentario |
|---|---|---|
| ln_ocupados | 1,48 (0,33) | |
| tipo_hip_real | 0,002 (0,008) | ≈ 0 |
| ln_permisos_l4 | 0,03 (0,03) | |
| ln_costes_real | **−0,66 (0,25)** | signo contrario al esperado |

  En pre-COVID, ocupados sube a 3,5 y el tipo real pasa a ser +0,053, también con signo contrario. Es decir, la relación cointegrada está dominada por el empleo, y los signos de costes y tipo no coinciden con `literatura.md`.
- **(c)** `ln_ipv_real` sale «ambigua» en raíces unitarias (Zivot-Andrews rechaza con quiebre en 2015Q1). El bounds test es válido con I(0) o I(1), pero hay que mencionarlo.

## Lo que queda sostenible (actualiza la sección anterior)

- **P1.** Asociación positiva y robusta con el empleo y persistencia del precio; nivel de evidencia moderado.
- **Relación de largo plazo.** Existe estadísticamente en términos reales (fuerte, 3/3), con signos de costes y tipo no interpretables. En términos nominales la evidencia es mixta.
- **Corrección de error.** Es significativa en la muestra completa, pero no desde 2014; evidencia débil.
- **Crédito.** Es comovimiento.
- **P5.** La especificación concreta no está identificada y no hay ganancia predictiva frente al AR(4).
