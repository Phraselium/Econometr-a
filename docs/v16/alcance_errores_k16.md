# Alcance de los errores de K16 (y K18) en versiones anteriores (v1-V12)

Fecha: 2026-10-18. Encargo: comprobar si cinco errores de implementación corregidos en V15/V16 aparecen también en el código de v1-V12 y si cambian alguna cifra publicada en la 1.0. Los cinco errores son E1-E4 de K16 y E5 de K18, Q6.

Reglas seguidas:
- No se ha escrito nada en el repositorio salvo este fichero.
- No se ha ejecutado make ni git.
- No se ha abierto data/sealed ni se ha llamado a holdout.evaluate*.
- La única re-ejecución se hizo sobre una copia de src/v8/m5_lpiv.py en el scratchpad de la sesión, con salidas allí. La copia sin cambios reproduce exactamente output/v8/M5.

«Publicado en 1.0» quiere decir que la cifra está en publicacion/ (cifras_clave.csv, los .md o los .xlsx) o en metodologia/.

## Resultado en una línea
Solo E4 afecta a algo publicado: 8 filas de la hoja «Atribucion» de **publicacion/tablas_v8.xlsx** (IV3 Bartik de V8-M5). Cambian los valores, pero no la capa (C4), ni ninguna designación, ni ninguna cifra de cifras_clave.csv. E1, E2, E3 y E5 no tienen efecto en cifras publicadas.

## Método de búsqueda

### Rutas revisadas
- src/*.py en la raíz: f2-f6, build_dataset*.py, econ_utils.py, v2_common.py, holdout.py.
- src/v2, v3, v4, v5, v5_1, v6, v6_1, v6_2, v6_3, v7, v7_1, v7_2, v8 (con herramientas/), v8_1, v9, v10, v11 y v12.
- src/v15 y src/v16 solo como referencia del error corregido.

### Patrones buscados (ripgrep)

**E1**
- `sparse_distance_matrix|cKDTree|KDTree|query_pairs|query_ball|distance_matrix|pdist|cdist|haversin|conley|Conley`.
- Lectura de cada estimador de Conley encontrado, para ver cómo trata la diagonal.

**E2**
- Definiciones: `def .*(ar4|ar_|oos|fuera|backtest|evaluar_oos|pred_ar|m_ar4|ar_pred)`.
- Condiciones de fila: `\+ ?h ?<=?`, `<= ?len\(.*\) ?- ?1`, `range\(4, ?t`, `ok\[0\] ?\+`.
- Bucles de origen.
- Todas las llamadas a `dm_test|dm_hln|lstsq` en módulos de predicción.

**E3**
- En el código: `_sa\b|ocupados_sa|compraventas_sa|stl|STL|seasonal|desestacionaliz|x13|hpfilter`.
- En los datos: columnas `*_sa` en data/processed, data/base y output (csv, csv.gz y parquet).
- Consumidores de nacional_q / nacional_q_v2 y selección dinámica de columnas (`startswith("ln_")`, `filter(regex)`, bucles sobre `df.columns`).
- Columnas desestacionalizadas en los paneles v6-v8.

**E4**
- `bartik|shift.?share|cuota.*base|share|rotemberg|BHJ` y, dentro de esos módulos, `nan_to_num|fillna\(0`.
- Comprobación con datos de si hay celdas del año base sin dato.

**E5**
- `groupby(...)[...].(diff|shift|pct_change)`, `transform(lambda s: ...diff())` y variables agrupadas (`g[...]`, `gb[...]`, `gg.shift`).
- `.diff(` y `.shift(` en v4-v12.
- Comprobación con datos de huecos de filas por unidad en todos los paneles que consumen esos módulos (código en el scratchpad).

## Tabla

| Error | Módulo y línea | Versión | Cifras que produce | ¿Publicada en 1.0? | ¿Cambia el valor? | ¿Cambia la capa? |
|---|---|---|---|---|---|---|
| E1 | src/v3/c1_est.py:123-141, `conley` (`query_pairs` excluye i = j; la diagonal entra una vez por `(s**2).sum()`) | v3 | EE de Conley de C1 (VUT por sección) | sí (C1 v3, vía E/hechos) | no: el núcleo es correcto | no |
| E1 | src/v5/b3_run.py:67-71, `cov_conley` (W denso; diagonal 1 una sola vez) | v5 | p «mayor de HC3/Conley» de B3 (B3-*, E-B3-*) | sí | no | no |
| E1 | src/v6/m1a_lib.py:100-121, `conley_cov` (K denso; los retardos temporales solo dentro de la localización) | v6 | se_conley de M1A (distritos) | sí (M1A en cifras_clave) | no | no |
| E1 | src/v9/herramientas.py:454-465, `conley` (K = d ≤ corte, diagonal una vez) | v9 | D3 (Conley 5/10 km) y F5 | sí (V9 F5) | no | no |
| E1 | src/v9/d4_inmigracion.py:129 (`conley` con corte −1 y K = 0) | v9 | pretendencias de Rotemberg | sí (D4) | no: solo se usa `se_hc1`; el EE de Conley no se lee | no |
| E2 | src/v2_common.py:178 y bm_lib.py:265 (`pos + h <= posL`), block_splits con embargo | v2 | OOS de BA, BV, BM, BO, BI, BP y H1/H2/H7 sellados | sí | no: condición correcta | no |
| E2 | src/f2_nacional.py:351-374 y 863-876 (`C.index < T`, h = 1); f6_valencia.py:111 | v1 | RMSE OOS y DM de F2 y F6 | sí (informe v1) | no | no |
| E2 | src/v5/ca_run.py:262-280 (tr = `iloc[:t-4]`) | v5 | OOS ADL frente a AR(4), CA | sí (CA) | no | no |
| E2 | src/v6/m1a_run.py:446-505; m1b_run.py:609-660; m3b_run.py:299-304; m3a_lib.py:213; m4_sellado.py/m4_lineas_base.py | v6 / v6.1 | OOS M1A, M1B, M3A, M3B, M4 y K1 | sí | no: entrenamiento con tiempo < origen − embargo; un solo origen bien delimitado en M1A | no |
| E2 | src/v7/r5_prediccion.py:119-136, 214-227, 341-360 (`y[:, :o+1]`; GBM `t + k <= T − 1` dentro del recorte) | v7 | backtest R5 y congelación | sí (R5) | no | no |
| E2 | src/v8/f5_atribucion.py:400-470; m6_colinealidad.py:162; m9_ml.py:232; f6_congelar.py:72 | v8 | V8-OOS-* (tabla común) | sí (V8 F6) | no | no |
| E2 (fuera del patrón) | src/v8/m0_periodos.py:372 y m4_largo_plazo.py:342: CV en bloques **bilateral** con embargo; src/f4_oferta.py:221 (DOLS con adelantos, «condicional») | v8 / v1 | RMSE de M0 y M4; rmse_1paso de F4 | sí | no: es un diseño declarado como CV en bloques o condicional, no una ventana expansiva con fuga | no |
| E3 | src/build_dataset.py:385-386 crea ocupados_sa y compraventas_sa (y ln_, d_, d4_), en nacional_q y nacional_q_v2 | v1 / v2 | — | — | ningún módulo de v1-V12 las lee: los únicos consumidores son src/v15/p9_prediccion.py y f3_sellado.py; v8 construye sus paneles desde data/raw sin columnas SA | no |
| E4 | src/f3_inmigracion.py:187-194; src/v2/bi_core.py:55-70 (y v6_1/k2 y v5/r1b, que lo reutilizan) | v1, v2, v6.1, v5 | IV Card y BI (R1B-S-BI-delta, K2) | sí | no: la cuota NaN da z NaN (`min_count`), sin imputación | no |
| E4 | src/v3/c1_est.py:241-261 | v3 | IV VUT de C1 | sí | no: share0 NaN se elimina (`dropna(subset=["z"])`) | no |
| E4 | src/v5/b3_data.py:81-91 (pesos `w/w.sum()` con NaN que suman 0) | v5 | F1_bartik (B3-H-B3-1-b, H-B3-1) | sí | no: 0 celdas sin dato en 2011, 2015, 2021, 2024 y 2025 (comprobado) | no |
| E4 | src/v9/paneles.py:215-216 (`F0.fillna(0)`) | v9 | D4 | sí (V9) | no: 0 celdas sin dato en 2003 y 2012 (52 × 28) | no |
| E4 | src/v8/m5_lpiv.py:196-197 (IV2: flujos ausentes → 0; es el shock, no la cuota) | v8 | H8-7 | sí (V8-H8-7-*) | no por E4; no se cuantifica (ver nota 4) | no |
| **E4** | **src/v8/m5_lpiv.py:214-217 (IV3 Bartik: `E.fillna(0.0)` antes de las cuotas de 2008)** | **v8** | **8 filas IV3_bartik_h1-2 (lpiv, ccaa_panel, empleo_renta, P2-P5 × compra/alquiler) en output/v8/M5/atribucion.csv → F5/atribucion_combinada.csv → hoja «Atribucion» de publicacion/tablas_v8.xlsx; M5_IV3_* en coeficientes.csv** | **sí: tablas_v8.xlsx; el texto de informe_econometrico_v8.md solo cita «F efectivo por debajo de diez»; ninguna fila en cifras_clave.csv** | **sí (ver más abajo)** | **no (sigue C4, no vota)** |
| E5 | paneles con huecos: v6 M0 mun_compra (427 saltos), mun_alquiler y mun_contratos (359), dis_alquiler (204) | v6 | M1A, M1B, M2, M3A, M3B, M4 | sí | no: los retardos se hacen por cruce en (unidad, año + k) (m3b_run.py:56 `lag`, m1b_run.py:65, m3a_lib.py:126-130, m2_run.py:44-63, m4_lineas_base `lag2` por índice) o por niveles (event study anio − g); la única diferencia agrupada (m1a_run.py:229-231) ya comprueba `anio.diff() == 1` | no |
| E5 | groupby(...).diff/shift en paneles completos: v2 (bi_core, ba_lib, bo_lib, bo_run, bv_lib, bd_lib, bi_h3, v2_common `_grid`), f3, v6/m0_run.py:715, v6_1/k2_datos.py, k3_run.py, v7 r1_panel.py y r4b_run.py, v8 f1_paneles.py, m4, m5, m9, build_dataset*.py | v1-v8 | muchas | sí | no: 0 saltos de periodo por unidad en panel_ccaa_a/q, v2 panel_prov_a/q, panel_muni_a, panel_ue_a/q, v7 y v8, y los provinciales de v6 M0; K2 rellena una rejilla completa (`_grid`); después de los dropna intermedios comprobados (b_var de M1B) tampoco hay saltos | no |
| E5 | v11/base_v11.py:246-248; v12/b4_oferta.py:43-44 | V11 / V12 | obra nueva neta del Catastro | sí (V12) | no: ya filtran el salto ≠ 1 | no |
| E5 | v4/m0_run.py:162-174 (Catastro y parque nacionales); v6_2/l3_deficit.py:53; v5/r1b_sens.py:237; v7_1/s3_hechos.py:34; v9/f2_potencia.py:238 | v4-v9 | terminadas_1924, L3, R1B, S3, F2 | sí | no: series y pivotes con años y trimestres consecutivos (comprobados en el crudo: Catastro 2012-2026, parque 2001-2025) | no |

## E4 en V8-M5 IV3: comprobación cuantitativa

**Qué pasa.** En Eurostat lfst_r_lfe2en2, el año base 2008 tiene 13 celdas NUTS2 × sector sin dato (confidenciales):
- ES22 (Navarra) y ES23 (La Rioja), sector L;
- cinco sectores de ES63 (Ceuta) y seis de ES64 (Melilla).

`construye_bartik` las pone a 0 antes de calcular las cuotas. Navarra y La Rioja están entre las 17 CCAA del panel, así que su cuota del sector L en 2008 se impone a 0. Ceuta y Melilla solo entran en el total nacional del leave-one-out (el shock, no la cuota).

**Declaración.** La imputación figura en docs/v8/diccionario.md:447 y diccionario_m5.md:9 («Celdas confidenciales (p. ej. sector L) = 0»). No figura en metodologia/desviaciones_v8.md ni en ninguna pieza de publicacion/. Por eso es E4 en sentido estricto respecto a lo publicado.

**Corrección mínima, igual que K16-H4.** Sin cuota del año base, la unidad queda fuera: se pone NaN en las cuotas de ES22 y ES23 y se descartan las filas con z NaN. N baja de 272 a 240 en h0 (2 CCAA menos).

Resultados (copia en el scratchpad; la base reproduce output/v8/M5 sin diferencias):

| Desenlace, h1-2 | β base → corregido | F efectivo | p AR | Capa |
|---|---|---|---|---|
| valor tasado real | −1,413 → −1,304 | 0,58 → 0,74 | 0,649 → 0,637 | C4 → C4 |
| alquiler real | −0,426 → −0,376 | 0,99 → 1,03 | 0,197 → 0,298 | C4 → C4 |
| IPV real | 2,040 → 1,862 | 1,07 → 1,23 | 0,087 → 0,094 | C4 → C4 |

En h0-h2 ningún F efectivo pasa de 3,4 y ningún `cumple_c3` cambia.

Filas publicadas que cambian (tablas_v8.xlsx, hoja Atribucion, `contribucion_pp`):

| Fila | Base | Corregido |
|---|---|---|
| compra P2 | 24,32 | 22,77 |
| compra P3 | −18,14 | −17,00 |
| compra P4 | 0,73 | 0,72 |
| compra P5 | −9,09 | −8,58 |
| alquiler P2 | 7,32 | 6,57 |
| alquiler P3 | −5,46 | −4,90 |
| alquiler P4 | 0,22 | 0,21 |
| alquiler P5 | −2,74 | −2,48 |

- Cambian también `pct_total` y la «variación media observada» de la nota, porque la muestra pasa de 17 a 15 CCAA.
- En alquiler, la banda AR del 68 % pasa a estar acotada en M5.

Lo que **no** cambia:
- hipotesis_m5.csv es idéntico (H8-5, H8-6 y H8-7, que son las únicas cifras de M5 en cifras_clave).
- Las 8 filas llevan `vota_s9 = no` («efecto relativo entre CCAA… no comparable»). F5 solo vota con filas nacionales (f5_atribucion.py:115), así que regla §9, ranking y designaciones no se mueven.
- La frase de informe_econometrico_v8.md:73 («F efectivo por debajo de diez») sigue siendo cierta.

Otra corrección posible sería imputar la celda con años vecinos en lugar de excluir la unidad. No se ha probado. Si el autor la prefiere, hay que reportar ambas, según la regla de CLAUDE.md.

## Conclusión por error

**E1 (núcleo de Conley con la diagonal doble): sin efecto en cifras publicadas.**
- Los cuatro estimadores de Conley de v3, v5, v6 y v9 no usan `sparse_distance_matrix`.
- Tres de ellos (v5, v6, v9) construyen un núcleo denso con K(0) = 1, que cuenta cada observación una sola vez.
- El de v3 suma Σs² y añade 2·Σ sobre `query_pairs`, que excluye i = j.
- Ninguno omite la diagonal.
- El error es exclusivo de src/v15/pa_panel.py y src/v16 (K16).

**E2 (fuga en el AR/ARDL con ventana expansiva o primer origen desplazado): sin efecto en cifras publicadas.**
- Todas las rutas de predicción anteriores a V15 entrenan con objetivos ≤ origen: `pos + h <= posL` en v2_common, el recorte `y[:, :o+1]` en v7, tiempo < origen − embargo en v5, v6 y v8.
- Ninguna usa `len(y)` como cota.
- Los orígenes están fijados por fecha o por `block_splits` y no hay desplazamientos de índice.
- Los diseños bilaterales de v8 M0/M4 y el rmse_1paso de F4 no son E2: están declarados como CV en bloques o como condicionales.

**E3 (STL con toda la muestra en evaluación pseudo fuera de muestra o sellada): sin efecto en cifras publicadas.**
- Las series `*_sa` de build_dataset.py existen en nacional_q y nacional_q_v2, pero ningún módulo de v1-V12 las lee, ni de forma explícita ni por selección dinámica de columnas.
- Las evaluaciones selladas de v2 (H1, H2, H7), v6 (M4/K1), v7 y v8 usan series brutas con dummies trimestrales o diferencias interanuales.
- No hay otra desestacionalización propia en src antes de V15.
- La única ruta afectada fue V15-H5 (ya corregida en K16).
- No hizo falta ninguna evaluación sellada.

**E4 (cuotas del año base imputadas a 0 sin declararlo): AFECTA a publicacion/tablas_v8.xlsx, hoja Atribucion, 8 filas IV3_bartik_h1-2 de V8-M5.**
- Cambian los valores: las contribuciones bajan entre un 2 % y un 10 % en valor absoluto; N pasa de 17 a 15 CCAA.
- No cambia la capa (C4), ni la votación, ni las designaciones, ni ninguna cifra de cifras_clave.csv.
- La imputación solo estaba declarada en el diccionario interno de V8.
- Si el autor acepta la corrección, hace falta una entrada en ERRATA.md y regenerar M5 → F5 → F6 → publicacion (orden expresa: CLAUDE.md, V14). No se ha hecho aquí.
- El resto de shift-share (v1 F3, v2 BI y derivados, v3 C1, v5 B3, v9 D4) no imputa: o propaga NaN, o no tiene huecos en el año base (comprobado con datos).

**E5 (diff/shift por unidad que salta huecos): sin efecto en cifras publicadas.**
- Los únicos paneles con huecos de filas son los municipales y de distrito de v6 M0.
- Sus consumidores construyen los retardos cruzando en (unidad, año + k), trabajan en niveles, o comprueban `anio.diff() == 1` (M1A).
- Los demás diff/shift agrupados operan sobre rejillas completas (comprobado: 0 saltos en todos los paneles de v1, v2, v6 provincial, v7 y v8).
- V11 y V12 ya filtran saltos ≠ 1.

## Notas
1. «Publicado en 1.0» se ha comprobado contra publicacion/cifras_clave.csv (1.207 filas, igual que output/v5/cifras_clave.csv), los .md y los .xlsx de publicacion/, y metodologia/.
2. La re-ejecución de M5 tarda unos 35 s por variante. El script de comparación y las salidas están en el scratchpad de la sesión (…/scratchpad/m5/). No forman parte del repositorio.
3. Este encargo pedía un único fichero, así que no se ha tocado docs/v16/estado.md ni ERRATA.md. Queda pendiente actualizar estado.md y, si el autor lo decide, la errata de tablas_v8.xlsx.
4. Observación ajena a E4: en IV2 de M5 (m5_lpiv.py:196-197), los años sin flujo de un origen se ponen a 0 antes de diferenciar, lo que puede crear shocks espurios. Afecta al shock, no a la cuota. Las cifras H8-7 publicadas tienen F = 0,05 y siguen sin respaldo por Holm, así que su capa no cambia. No se ha cuantificado.

**Incidencia de proceso (2026-10-18).** Durante la auditoría, la ejecución de comprobación de V9-D4 vació output/v9/d4/registry.csv en el repositorio (le quitó 38 filas). El orquestador lo detectó en `git status` antes de hacer commit y lo restauró desde git (`git checkout`). El registro versionado no cambió en ningún commit, y ninguna cifra se vio afectada.
