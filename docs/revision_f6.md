# Revisión independiente F6 (València, P4 municipal)

Revisor: reviewer (puerta F6) · 2026-10-09 · commit revisado `c5cb994` (árbol con cambios sin confirmar en F2/F3, ajenos a F6).
Material leído: `docs/decisiones.md` (F6 y hallazgos posteriores), `docs/preguntas.md`, `output/f6/resumen_f6.md` y las 27 tablas,
3 PNG (`fig_indices_p_tasado`, `fig_alquiler_precio`, `fig_serpavi_distritos`), `src/f6_valencia.py`, `output/registro_busqueda_f6.csv`,
`docs/revision_f1.md` §8, `docs/revision_f1_fuentes.md`, `docs/diccionario_variables.md` (filas de valencia.csv) y `output/f5/valencia_vs_espana.md`.
Los contrastes propios los hice con un script aparte (scratchpad), leyendo solo `data/processed` y `data/raw`.

## Veredicto: **REHACER** (acotado: solo texto, tablas y 3-4 regresiones adicionales; datos y estructura se mantienen)

Datos, reproducibilidad y separación estimación/descriptivo están bien. Lo que falla es la parte A: la beta València-España
se presenta como un único número (1,73) cuando el propio script detecta inestabilidad (CUSUM, Chow 2020Q1, Bai-Perron) y no la
desagrega. Además, el contraste con el IPV del INE contradice la magnitud del diferencial CV-España del valor tasado, y hay
p-valores de tendencia sin validez que entran en la familia Holm. Son cambios acotados; con ellos, la fase se aprobaría.

---

## 1. Reproducibilidad — **OK**

- `make all` sin `FORCE` termina con `exit=0`. Todas las descargas y extracciones salen de caché (`[cache] …`; `extract_notariado`: "salidas ya existen; sin red").
  El único aviso es un `Pandas4Warning` en `build_dataset.py:1132`, que no afecta a F6. `report.py` todavía no existe.
- md5 de los 55 ficheros de `output/f6/` (PNG incluidos): **idénticos** antes de `make all`, después de `make all` y en dos ejecuciones más
  de `python3 src/f6_valencia.py`. `data/processed/valencia.csv` también es idéntico (md5 `95cc08c8…`). El registro `registro_busqueda_f6.csv` es estable (md5 `a5ae3454…`).
- El script no usa red y fija la semilla (`eu.SEED`), aunque no hace nada aleatorio.

## 2. Datos — **OK, con dos matices**

| Comprobación pedida | Resultado |
|---|---|
| Valor tasado municipal, N ≥ 40 | 86 trimestres seguidos (2005Q1-2026Q2), sin huecos ni interpolación. Raw `valor_tasado_mun_valencia`: 2007T4 = 2341,6; 2019T4 = 1486,1; 2026T2 = 2972,8 ✓ |
| Padrón por nacionalidad solo hasta 2022 | ✓ (1998-2022, N=25; DPOP total 1996-2025). Raw 2022: 114.336 / 792.492 = **14,4 %** ✓ |
| SERPAVI por distrito | `validado = plausibilidad` y `rol = descriptivo` en las 8 variables; se identifican por código 4625NNN y no se inventa ningún nombre ✓. Raw 2024: 4625001 = 10,897 y 4625017 = 5,875 ✓ |
| VUT GVA sin encadenar con la lista de 2026 | ✓ La serie acaba en 2024Q4 (CV 101.171; València 6.090, que coincide con revision_f1_fuentes) y la foto de 2026 no está en valencia.csv |
| VUT INE municipio vs provincia | ✓ Corregido el error de F1, cuando el «municipio» era la provincia: València 7.976 frente a provincia 17.853 en 2024Q3 (peso ≈ 45-52 %). Tabla marcada como no comparable en niveles con GVA |
| Notariado | ✓ El municipio solo aparece como «Total general» (2021-2025; 2022 = 2.171 y 2025 = 2.538, como en revision_f1_fuentes; ya no se pierde València). Rol robustez y descriptivo |
| SERPAVI València municipio | Raw `SERPAVI_MUN_46250_VC_alquiler_m2_mediana`: 2011 = 5,1546 y 2024 = 8,1818 ✓ |

He recalculado las tres cifras desde `data/processed/valencia.csv` (variación 2019Q4→2026Q2 del valor tasado):
**València +100,0 %, CV +57,1 %, España +42,5 %** (provincia +65,5 %). Coinciden con el resumen y con raw (España 2355,0 / 1652,8; CV 1935,0 / 1232,0).
**No he encontrado ninguna cifra inventada.**

Matices:
- (a) Con el **IPV del INE** (que está en valencia.csv, N=78, y F6 no usa), la variación 2019Q4→2026Q2 es **CV +61,8 % frente a España +59,5 %** (2,3 pp), cuando con el valor tasado es 57,1 frente a 42,5 (14,6 pp). F5 (`output/f5/valencia_vs_espana.md`) ya lo muestra. El "exceso" de la CV es en gran parte propio del valor tasado (composición de lo que se tasa, mezcla de nueva y usada). Para el municipio no hay IPV que permita contrastarlo. Esto se tiene que decir en la parte A (cambio 2).
- (b) La base puntual de la variación acumulada importa: tomando 2020Q1 como base, València sale +97 %; con medias anuales 2019→2025, +83 % (España +30 %). El orden se mantiene, pero conviene una frase de sensibilidad.
- (c) `fuentes_fallidas.md` dice que la nacionalidad 2023-2025 "no está publicada a nivel municipal", mientras que `docs/fallidas/ine_ccaa.md` anota que la tabla 79544 "es municipal desde 2021". Hay que aclarar esa contradicción (no bloquea).

## 3. Separación estimación / descriptivo — **OK en lo descriptivo; incoherencias en la parte A**

- En la parte B y en las tablas descriptivas no hay ningún p-valor, IC ni lenguaje causal (busqué «efecto», «impuls», «provoc», «debido», «explica», «caus», «p=», «IC95», «signific»).
  `diferencial_por_tramo` y `correlaciones_anuales` dejan claro que no hay inferencia. La sección «Qué NO se puede afirmar» es correcta.
- Incoherencias:
  1. `tabla_N_series` y la tabla del resumen marcan como «estimación (N>=40)» series que F6 **no** estima (`vut_stock_gva`, `ipv` CV/España, `trans_total` en el municipio solo en la beta). Hay que distinguir «elegible (N≥40)» de «usada en estimación».
  2. Las **tendencias lineales de la cuota de extranjeros** se rotulan «descriptivas», pero llevan EE, p-valores (~5e-13) y entran en la familia Holm como «significativas». Ver §4.4.

## 4. Econometría

### 4.1 Estacionariedad y regresión espuria de la beta

- En ln p_tasado (València y España) no se rechaza la raíz unitaria (ADF con tendencia, p ≈ 1,0). La beta se estima en Δ4 ln, que es lo correcto.
- Las propias Δ4 son muy persistentes: ADF no rechaza (p = 0,65-0,87) y KPSS rechaza la estacionariedad al 5 % (p = 0,02-0,04). Con N=82, el riesgo de una «beta» espuria no es nulo.
- **Contraste propio que la salva:** en Δ1 ln (sin solapamiento) con dummies trimestrales y HAC(4), N=85, sale β(España) = **1,73** (EE 0,18; p(β=1) = 4e-5), β(CV) = 1,48 y β(Provincia) = 1,44. La conclusión «València amplifica más que 1:1 en el conjunto de la muestra» resiste.
- Con más retardos HAC (8 y 12) el EE de β baja algo (0,098 y 0,087), así que HAC(4)/HAC(6) no es anticonservador para β. En cambio, el EE del **diferencial medio** sí sube (1,30 → 1,80 con 12 retardos; acf del diferencial 0,6 en los retardos 1-3 y aún 0,3 en el 8). La MA(3) mecánica no recoge toda la persistencia, así que HAC(4) se queda corto para el diferencial. La conclusión (no significativo) no cambia.

### 4.2 Quiebres: la beta de la muestra completa no es un parámetro estable — **falta lo principal**

Diagnósticos del propio script: BG(4) p < 1e-5, RESET p = 0,0003-0,02, CUSUM p = 0,001-0,04, Chow 2020Q1 p ≈ 0,01 y Bai-Perron con 1-3 quiebres
(España: 2009Q1 y 2018Q2). Hay dos fallos de método: el Chow es el F clásico con errores autocorrelacionados, y el Bai-Perron usa BIC sin corregir la autocorrelación, así que los dos tienden a dar demasiados rechazos.
Lo comprobé con un Wald HAC(6) de la interacción `dES × post2020` en N=82: **−0,53 (EE 0,20)**, y la constante post-2020 vale **+5,05 (EE 1,35)**. El quiebre de 2020 es robusto.

**El resumen no da la beta por subperíodos.** Mis estimaciones (HAC(4), solo para la revisión; los tramos tienen N<40):

| Tramo | N | β vs España (EE) | β vs CV (EE) |
|---|---|---|---|
| 2006Q1-2013Q4 | 32 | 1,67 (0,12) | 1,58 (0,11) |
| 2014Q1-2019Q4 | 24 | 2,80 (0,63) | 3,38 (0,63) |
| 2020Q1-2026Q2 | 26 | **1,20 (0,17)** | **1,02 (0,14)** |
| 2018Q3-2026Q2 (tras el quiebre BP) | 32 | 1,14 (0,20) | 0,94 (0,16) |

Lectura: desde 2020, València **no amplifica** el ciclo de la CV (β ≈ 1). Su mayor crecimiento es un **diferencial de nivel** de ≈ +5,6 pp/año
frente a España (+4,2 frente a la CV) y no una mayor sensibilidad. La β = 1,73 de la muestra completa mezcla la caída de 2008-2013 con un
diferencial que cambia de signo de un tramo a otro. Además, la regresión inversa da 1/β = 2,19 y el cociente de desviaciones típicas es 1,95: buena parte de la «beta» refleja que la serie municipal es mucho más volátil, lo que es coherente con más ruido de composición en las tasaciones de una sola ciudad.

Diferencial medio por tramo en la muestra completa (dummies de tramo, N=82, HAC(8)), València − España: 2006-07 +3,9 (0,4); 2008-13 −3,6 (1,3);
2014-19 +0,3 (2,5); 2020-26 **+5,6 (1,0)**. Que el **diferencial medio de toda la muestra sea ≈ 0 y no significativo** es correcto pero engañoso: es el promedio de tramos de signo contrario.

### 4.3 Endogeneidad y relación parte-todo
La beta es un co-movimiento, no un efecto, y el texto lo dice («asociación contemporánea»). Falta una advertencia: València forma parte de la provincia, de la CV y de España, así que la correlación tiene un componente mecánico de parte-todo. Pesa sobre todo frente a la provincia; en compraventas, València es el 7-15 % de la CV. Para `trans_total` se puede comparar con el «resto» (CV − València). Para el valor tasado no, porque los pesos son desconocidos.

### 4.4 Cuota de compradores extranjeros (CV frente a España)
- `cuota_CV` y `cuota_ES` no son estacionarias (ADF con tendencia p = 0,87 y 0,51; acf(1) ≈ 0,93). El t de una tendencia lineal sobre una serie I(1) diverge (regresión espuria de tendencia), así que **los p ≈ 5e-13 no son válidos** y no deben entrar en la familia Holm.
- La diferencia CV − España es persistente (acf(1) = 0,90; ADF p ≈ 0,045). El EE HAC(4) = 0,335 sube a 0,49 con 12 retardos, y el p = 7e-32 es una exageración numérica. El hecho robusto es descriptivo: **la cuota de la CV supera a la de España en los 77 trimestres** (mínimo +0,07 pp, media +3,9 pp).
- La advertencia del 2008→2009 sobre `trans_extranjeros` (decisiones.md, F3) también se aplica aquí y no aparece en F6.

### 4.5 Misma muestra y búsqueda
- Las betas y diferenciales de precio usan la misma muestra Δ4 (2006Q1-2026Q2, N=82). Las de compraventas, 2008Q1-2026Q1 (N=73), es decir, otra familia, y está declarado ✓.
- 14 modelos registrados. En el historial git el registro siempre tuvo 14 filas, así que no hay especificaciones ocultas. Holm y Bonferroni sobre 11 contrastes (sin los duplicados HAC6) ✓. Las tres β=1 de precios sobreviven a Holm (p_Holm ≤ 2e-4) y a Δ1. La β=1 de compraventas frente a España no sobrevive (p_Holm = 0,06), y así se informa.
- La búsqueda no maximiza R² (el conjunto es cerrado), así que el riesgo de sobreajuste es bajo. El `rmse_oos` del registro de las betas es **condicional al x contemporáneo**, no un pronóstico. Basta con decirlo en las notas.

### 4.6 Rentabilidad bruta alquiler/precio
La advertencia está en la nota de la tabla, en el título de la figura («mezcla fuentes») y en el resumen ✓. Faltan tres cosas: (i) SERPAVI es el **stock de contratos vigentes**, que va por detrás del mercado, así que en fases alcistas infravalora la renta de mercado; (ii) la superficie de SERPAVI (catastral) y la de la tasación pueden no coincidir (no verificado); (iii) el resumen da los extremos «3,7 % (2011) a 4,5 % (2024)» y oculta la trayectoria. Hay un pico de 5,2 % en 2017 y una caída desde 2020 (de 4,96 a 4,49), que es lo único informativo: el valor tasado de València sube más que la renta SERPAVI (índices 2015=100 en 2024: 189 frente a 175). Lo mismo ocurre con el Notariado provincial: «18,5 % → 18,8 %» oculta el máximo de 23,3 % en 2023.

## 5. Signos y magnitudes frente a `docs/literatura.md`
F6 no cita literatura ni contrasta signos con ella. No hay referencias en F6 que verificar, y por tanto ninguna está mal citada. `literatura.md` no tiene referencias sobre VUT ni alquiler turístico, ni sobre la sensibilidad ciudad-país (son lagunas, no errores). Es coherente con que F6 no afirme nada sobre el efecto de las VUT. Que la ciudad central sea más volátil que el agregado es compatible con el marco de oferta rígida a corto plazo (DiPasquale-Wheaton, marcado como no verificado en sus cifras) y con Glaeser-Gyourko (2005). No lo marco como discrepancia, pero no debe presentarse como contraste de la literatura.

## 6. Qué puede afirmarse de València y con qué evidencia

| Afirmación | Nivel de evidencia |
|---|---|
| El valor tasado de València creció **+100 %** entre 2019Q4 y 2026Q2 (CV +57 %, España +42 %) | Hecho descriptivo verificado. **Solo con valor tasado**: con el IPV, el diferencial CV-España casi desaparece (+62 frente a +59 %); para la ciudad no hay contraste independiente |
| En toda la muestra 2006-2026, València se mueve más que 1:1 con España, la CV y la provincia (β ≈ 1,4-1,7) | Estimación con N ≥ 40, HAC, que sobrevive a Holm y a Δ1 sin solapamiento. **Pero la β es inestable**: no es un parámetro estructural |
| Desde 2020, la ciudad crece ≈ 5,6 pp/año más que España, por un diferencial de nivel, con β ≈ 1 frente a la CV | Evidencia de tramo (26 trimestres, dentro de un modelo con N=82). **Asociación, no causa** |
| Diferencial medio 2006-2026 ≈ 0 | Correcto pero poco informativo (tramos de signo contrario) |
| La cuota de compradores extranjeros de la CV supera a la de España | Hecho descriptivo robusto (77/77 trimestres). Su p-valor y las tendencias no son válidos tal como están |
| Alquiler SERPAVI +75 % (2015-2024), VUT, padrón, distritos, Notariado | Solo descriptivo (N<40) |
| Inmigración, compradores extranjeros o VUT **causan** precios o alquileres en València | **No puede afirmarse** (no hay identificación; N anual corto) |

## 7. Cambios priorizados (necesarios y acotados)

1. **Beta por subperíodos (bloqueante).** Añadir en la parte A la β con interacciones de tramo en la muestra completa: `dV ~ dX*(tramo)`, con tramos 2006-13 / 2014-19 / 2020-26 y, como alternativa, las fechas Bai-Perron. N=82, HAC(6-8). Registrar los modelos en `registro_busqueda_f6.csv` y ampliar Holm. Reescribir la frase de la β para que diga que la β completa es un promedio inestable, que desde 2020 β ≈ 1 frente a la CV y que el mayor crecimiento reciente es un diferencial de nivel. Hacer lo mismo con el diferencial medio (constante por tramo) y dejar de presentar el «≈ 0 no significativo» de la muestra completa como resultado.
2. **Contraste con el IPV (bloqueante).** Añadir a `crecimiento_acumulado` y a la beta CV-España la misma métrica con `ipv` (CV, España; 2007Q1+, misma muestra), y advertir que el exceso CV-España del valor tasado no se reproduce con el IPV y que para el municipio solo hay valor tasado (composición de tasaciones). Incluir la sensibilidad a la base (2019Q4, 2020Q1, medias anuales).
3. **Cuota de extranjeros.** Quitar los p-valores de las tendencias lineales (o sustituirlos por un contraste robusto a I(1), por ejemplo Vogelsang) y sacarlas de la familia Holm. Para la diferencia CV-España, reportar HAC con más retardos (≥ 8) y el hecho descriptivo «positiva en 77/77 trimestres». Mencionar el salto de cobertura 2008→2009 de `trans_extranjeros`.
4. **Chow/Bai-Perron robustos.** Sustituir o complementar el Chow F clásico por el Wald HAC de las interacciones (cambio 1) y anotar que Bai-Perron con BIC y residuos autocorrelacionados tiende a sobreestimar el número de quiebres. Añadir una línea con la beta en Δ1 y dummies estacionales (no solapada) como robustez de la Δ4.
5. **Texto y etiquetas (menores).** (a) En `tabla_N_series`, «elegible N≥40» frente a «usada en estimación». (b) Rentabilidad bruta: añadir el retraso del stock SERPAVI, la posible diferencia de superficie y la trayectoria (pico de 2017, caída desde 2020) en lugar de solo los extremos. Notariado provincial: dar el máximo de 2023. (c) Advertencia de parte-todo en las betas (València ⊂ provincia/CV/España) y, en compraventas, beta frente a «CV sin València». (d) Notas del registro: `rmse_oos` de las betas es condicional. (e) Aclarar la contradicción sobre la tabla INE 79544 (nacionalidad municipal desde 2021) entre `fuentes_fallidas.md` y `fallidas/ine_ccaa.md`. (f) Quitar la línea duplicada `A["ln_vut_val"]` en `f6_valencia.py`.

Con los cambios 1-3 hechos (y 4-5 en lo posible), la fase puede aprobarse sin otra ronda completa: basta con que el revisor compruebe esos puntos.
