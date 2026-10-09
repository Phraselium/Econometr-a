# Revisión independiente, puerta de la FASE 1 (Datos)

Fecha: 2026-10-09. Revisor independiente: no construí los datos y he comprobado todo por mi cuenta.

**Alcance**
- Puntos 1, 2, 5 y 6 de la checklist.
- Puntos 3 y 4, solo en lo que afecta a la construcción de los datos.
- No he modificado `data/raw`, `data/processed`, `src` ni el diccionario.

## Veredicto: **REHACER** (acotado)

La base es sólida en lo esencial:
- `make all` es reproducible sin red, también desde un clon limpio.
- Todas las cifras que he cotejado coinciden exactamente con `data/raw`.
- No he encontrado cifras inventadas.
- Los 6 cambios de `docs/revision_f1_fuentes.md` están aplicados.

Aun así, hay **4 defectos bloqueantes** de construcción. Afectan a variables con `rol=principal` o a la interpretación de las banderas en F2-F5. Los 4 se corrigen en `src/build_dataset.py` en poco tiempo, sin descargar nada nuevo: todo lo necesario ya está en `data/raw`.

---

## 1. Reproducibilidad

| Prueba | Resultado |
|---|---|
| `make all` en el repo, con la red bloqueada (`HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9`, FORCE sin definir) | exit 0, 21 s. Todos los fetch/extract salen por caché: 24/24 INE, 24/24 MIVAU, 7/7 Eurostat; Notariado, Registradores, SERPAVI y GVA "sin red". |
| `data/processed/*.csv`: sha256 antes y después | **idénticos byte a byte** |
| `data/raw/**`: sha256 de los 195 ficheros antes y después | **sin cambios** |
| `git status` tras `make all` | limpio (el diccionario regenerado también es idéntico) |
| **Clon limpio** (`git clone` local → `make all` sin red) | exit 0; `data/processed` idéntico al del repo. Los originales que ignora `.gitignore` (`gva_orig/vut_*.csv` y `serpavi_bd_*.xlsx`) no hacen falta, porque hay caché a nivel de salida. |
| `models` y `report` | Todavía no hay `src/f[2-6]_*.py` ni `src/report.py`. Es esperable en F1. |

**Tamaño y ficheros grandes**
- `.git` ocupa 107 MB.
- Hay tres blobs de más de 50 MB en el historial:
  - `data/raw/gva_vut_municipio.csv`: 66,9 MB, versionado.
  - `gva_orig/vut_historico_2025.csv`: 53 MB. Está en el historial aunque ahora lo ignora `.gitignore`.
  - `ine_padron_pcaxis/t_es_csv_bdsc_33946.csv`: 52 MB.
- Ninguno supera el límite duro de GitHub (100 MB), y la rama ya está publicada en `origin`. **No es un riesgo para la reproducibilidad**: el clon funciona.
- Sí es un riesgo de crecimiento: cada refresco con `FORCE=1` añade otros ~65 MB al historial.
- Recomendación (no bloqueante):
  - guardar `gva_vut_municipio.csv` como `.csv.gz` (pandas lo lee directamente), o quitar las columnas repetidas `fuente`, `dataset_ckan` y `ckan_modificado`, o pasarlo a Git LFS;
  - lo mismo para `t_es_csv_bdsc_33946.csv`.

## 2. Cambios exigidos por `revision_f1_fuentes.md`: comprobación

| Cambio | ¿Aplicado? | Comprobación propia |
|---|---|---|
| Notariado municipios: geometría, completitud y "Total general" | **Sí** | Volví a leer los 5 PDF (4T2021-4T2025) con pdfplumber. Cada uno tiene 19 cabeceras "- hasta" y 19 "Total general". València = **2.302 / 2.171 / 3.314 / 2.960 / 2.538**, idéntico en `raw/pdf/notariado_cv_municipios_anual.csv` y en `valencia.csv`. `municipios_completitud = si`. `valencia.csv` usa solo "Total general" (4T2022 no es aditivo: hay 995 de error en "Otras nacionalidades", documentado). |
| Caché sin red (Notariado) | **Sí** | Lo comprueba la prueba de `make all` sin red y la del clon limpio. |
| Registradores: suma móvil de 4T y serie anual | **Sí** | Series `*_4T_movil` con la columna `ventana`. Serie anual aparte (`registradores_opendata_anual.csv`, T4 = año natural). Las filas de los implícitos frente al CGN figuran como `plausibilidad`. **Defecto menor:** las unidades de `*_pm2_4T_movil` e `*_imp_4T_movil` dicen "(suma movil 4 trimestres)", y un €/m² o un importe medio no se suman: son una media o ratio de la ventana. |
| SERPAVI con composición constante | **Sí** | Hay tres variantes (variable, constante y encadenada). `nacional_q.serpavi_esp_constante` (17 CCAA, sin Navarra ni País Vasco) tiene rol robustez. La validación declara "NO independiente (ambos AEAT)". |
| VUT GVA sin encadenar con la lista actual | **Sí** | `vut_foto_*` está excluida de `valencia.csv`, y `vut_stock_gva` acaba en 2024Q4. **Menor:** el raw no lleva la columna `nota` que pedía la revisión anterior, y no existe `gva_validacion.csv` (punto 7 de aquella revisión). La afirmación "0 (reconstrucción independiente)" del diccionario solo se apoya en el informe del revisor. |
| VUT INE: municipio frente a provincia | **Sí** | Son dos ficheros distintos. Provincia 2024-08 = 17.853, igual que en `ine_vut_nacional_ccaa_prov.csv`. Municipio 2024-08 = 7.976 (tabla 39366, VTE25605). **Defecto de documentación:** desde 2024-11 el INE publica en **noviembre y mayo** (no en febrero y agosto). `valencia.csv` asigna esos datos a T4/T2 (2024Q4, 2025Q2, 2025Q4, 2026Q2), pero el diccionario dice "feb→T1, ago→T3". Además, 2024Q3 y 2024Q4 solo distan 3 meses. |
| (Punto 4 de la revisión anterior) orden de ediciones de los actos | **No** | Sigue pendiente (`docs/fallidas/notariado.md`). No bloquea, porque `notariado_cv_actos_mensual` no se exporta. |

## 3. Cotejo de cifras de `data/processed` con `data/raw`

Elegí las cifras al azar (semilla 20261009) y las recalculé desde el raw:

| # | Fichero / variable / periodo | Procesado | Raw | ¿Coincide? |
|---|---|---|---|---|
| 1 | `nacional_q.p_tasado` 2025Q4 | 2230,0 | `valor_tasado_libre_nacional` 2025T4 = 2230,0 | ✓ |
| 2 | `nacional_q.trans_extranjeros` 2020Q3 | 11277 | `tx_extranj_residentes_total_nacional` 2020T3 = 11277 | ✓ |
| 3 | `nacional_q.credito_nuevo` 2019Q1 (suma de 3 meses) | 10596 | 3206 + 3404 + 3986 = 10596 | ✓ |
| 4 | `nacional_q.euribor` 2016Q3 (media de 3 meses) | −0,0538143 | (−0,0560476 − 0,0483043 − 0,0570909)/3 | ✓ |
| 5 | `panel_ccaa_q.compraventas` Illes Balears 2014Q2 | 2190 | ETDP1806: 694 + 772 + 724 | ✓ |
| 6 | `panel_ccaa_a.pob_africa` Asturias 2016 | 5156 | ECP190260 2016T1 = 5156 | ✓ |
| 7 | `panel_ccaa_a.notariado_cgn_extranj` País Vasco 2010 | 713 | 2010S1 463 + 2010S2 250 | ✓ |
| 8 | `valencia.vut_stock_gva` provincia 2013Q2 (fin de trimestre) | 5552 | `vut_stock_prov_46` 2013-06 = 5552 | ✓ |
| 9 | `valencia.notariado_viv_ext_prov` 2020Q1 | 1504 | `viv_vendidas_ext` Valencia 2020T1 = 1504 | ✓ |
| 10 | `valencia.pob_extranjera` 2008 | 114260 | `vlc_46250\|Ambos sexos\|Extranjera` 2008 = 114260 | ✓ |
| 11 | `nacional_q.tipo_bce` 2022Q3 y 2026Q2 (media de días) | 0,497283 / 2,188462 | (49·0,5 + 17·1,25)/92 ; (77·2,15 + 14·2,4)/91 | ✓ |
| 12 | `ipv` (80270) con base 2025 | media 2025 = 100,000 | IPV1209 2025T1-T4 | ✓ |

Además:
- Los huecos de `visados` 2016Q2 y 2017Q2 son reales en origen: faltan abril-junio en `mivau_visados.csv`.
- Los controles automáticos de `build_dataset.py` (77019 por grupos, padrón València, hogares EPA, CGN) pasan.

**No he encontrado ninguna cifra inventada.**

## 4. Construcción de datos: hallazgos

### 4.1 BLOQUEANTE: deflactor NSA aplicado a una renta SCA, que crea una estacionalidad espuria en `renta_hog_real` (rol principal)

- `deflactor` = CNTR6548 / CNTR6721, es decir, PIB nominal y volumen **sin ajuste estacional**. Las cifras de volumen encadenado NSA no tienen una estacionalidad comparable entre trimestres.
- La `Δln deflactor` media por trimestre (2008Q1+) es T1 −0,56 %, T2 +0,94 %, **T3 −1,22 %, T4 +2,43 %**. Es estacionalidad pura.
- `renta_hog` es **SCA** (Eurostat) y se divide entre ese deflactor NSA. El resultado es que `d_ln_renta_hog_real` medio sale T1 +0,99 %, T2 −0,79 %, **T3 +2,57 %, T4 −1,76 %**: es un ciclo estacional fabricado en una variable desestacionalizada.
- Consecuencia en F2:
  - autocorrelación de orden 4 inducida;
  - posibles correlaciones espurias con el IPV, que es NSA;
  - sesgo en la cointegración si no se ponen dummies, y aun con ellas se mezcla SA con NSA.
- **Corrección:** `deflactor` = CNTR6597 / CNTR6652 (PIB SA a precios corrientes y en volumen). Las dos series **ya están** en `ine_cnt_pib_oferta_corrientes.csv` y `_volumen.csv`. Después hay que recalcular `renta_hog_real`, `inflacion_deflactor` y `tipo_hip_real`, y documentarlo en el diccionario.

### 4.2 BLOQUEANTE: quiebre metodológico de la EPA en 2021T1, sin documentar, en `hogares_epa` (serie principal de hogares)

- `d_ln_hogares_epa` en 2021Q1 = **−1,11 %** (de 18.817,8 a 18.610,0 miles). Es el **único descenso** de la serie y su mayor variación absoluta desde 2002.
- El INE documenta dos cambios desde 2021T1:
  - la definición de hogar pasa a basarse en el presupuesto compartido, no en la vivienda (Reglamento UE 2019/1700);
  - los factores de elevación pasan a la base poblacional del Censo 2021, mientras que 2002-2020 sigue en base 2011.
  - Fuentes: INE, "Medida del efecto de los cambios en la EPA 2021" y nota de prensa `cbEPA2021`.
- El diccionario presenta `hogares_epa` como serie continua 2002T1+ "nativa" y no menciona el quiebre.
- **Corrección:**
  1. documentarlo en el diccionario;
  2. añadir `quiebre_epa_2021` (dummy de escalón desde 2021Q1) a `nacional_q`;
  3. advertir que la creación neta de hogares de 2021Q1 no debe interpretarse como dato real;
  4. revisar si `ocupados` (65302) sufre el mismo cambio de base. El INE dice que el efecto en los agregados principales "no es relevante", pero hay que anotarlo.

### 4.3 BLOQUEANTE: la bandera `<var>_interp` es engañosa y no es coherente entre ficheros

Sí es engañosa. El nombre sugiere "valor imputado", pero marca a la vez cinco cosas distintas:
- interpolación de verdad, que crea información y genera un MA mecánico en Δ;
- agregación mensual→trimestral, que es información observada;
- valor de fin de periodo;
- desestacionalización STL;
- asignación desde frecuencias menores.

Consecuencias:
- `tipo_hip_interp`, `euribor_interp`, `compraventas_interp`, `credito_*_interp` e `ipc_alquiler_interp` son TRUE en el **100 %** de sus observaciones. Un filtro `~<var>_interp` en F2 eliminaría la serie entera, y un contraste de sensibilidad "sin interpolados" no tendría sentido.
- El mismo concepto se marca de forma distinta según el fichero:
  - el stock a fin de trimestre es TRUE en `nacional_q.credito_stock_interp` y `interp=False` en `valencia.vut_stock_gva`;
  - la suma de 3 meses de `compraventas`, `visados`, `terminadas` e `ipc_alquiler` está marcada en `nacional_q`, pero **no tiene bandera** en `panel_ccaa_q`;
  - `panel_ccaa_a` marca TRUE en todas las medias anuales.

**Corrección propuesta:**
- Sustituir la bandera booleana por **`<var>_metodo`** (categórica), con valores `nativo`, `media_3m`, `suma_3m`, `fin_periodo`, `media_dias_escalonado`, `stl`, `interpolado_loglin`, `asignado_anual_T4`, `asignado_semestral` y `asignado_anual_T1`.
- Mantener `<var>_interp` = TRUE **solo** si `metodo == interpolado_loglin`.
- Aplicar el mismo criterio en los 4 ficheros: en `valencia.csv` sería la columna `metodo`.
- Con este criterio, las únicas banderas `_interp` reales son `pob_total` y `pob_extranj` (26 cada una en 2008Q1+; 52 y 38 en total) y las `pob_*` del panel trimestral (867 en 2008Q1+).

### 4.4 BLOQUEANTE (menor): `inmig_anual` con rol=principal y N=4; la serie larga ya está en `data/raw` y no se usa

- `inmig_anual` (EMCR 69687) solo cubre 2021-2024: **4 observaciones**. Con rol "principal" no sirve para ningún modelo.
- `data/raw/eurostat_inmigracion_anual.csv` (migr_imm1ctz, ES) tiene el total **1998-2024** (27 años). En 2021 coincide: 887.960 = EM1765217.
- El paso de la Estadística de Variaciones Residenciales / Estadística de Migraciones a la EMCR en 2021 es un quiebre: 2019 = 750.480; 2020 = 467.918 (COVID); 2021 = 887.960.
- **Corrección:**
  - exportar `inmig_anual_eurostat` (1998-2024) con la bandera `quiebre_emcr_2021`;
  - pasar `inmig_anual` (EMCR) a robustez;
  - documentar que el desglose FOR/NAT por ciudadanía solo es completo desde 2020.

### 4.5 No bloqueantes (construcción)

1. **`panel_ccaa_q`: la población es anual disfrazada de trimestral.**
   - En `pob_total`, `pob_extranj` y `pob_espanola`, 3 de cada 4 trimestres están interpolados: 867 de 1.173 observaciones en 2008Q1+.
   - Su `d_ln_` es **constante dentro de cada año** (p. ej. 0,002436 en 2010Q2-2011Q1).
   - Hay que poner en el diccionario una advertencia explícita: "en paneles usar solo T1 / `panel_ccaa_a`, o Δ4; nunca Δ1 trimestral como regresor". Usarla en trimestral multiplica el N por 4 y crea autocorrelación mecánica.
   - El panel trimestral con población termina en **2025Q1**, porque 77019 llega a 1-ene-2025. La serie nacional llega a 2026Q3.
2. **`panel_ccaa_a` (F3) no incluye `trans_extranjeros`** (MIVAU por CCAA, 2007+), aunque es la variable de resultado más directa para la demanda extranjera. Tampoco incluye `visados`, `terminadas` (control de oferta) ni `ipc_alquiler`. Hay que añadirlos como suma o media de 4 trimestres.
3. **Grupos de países con quiebre UE28/UE27 (2020/2021).**
   - He comprobado que **Europa sin España = UE28_sin_ES + Europa_no_UE28 (2002-2020) = UE27_sin_ES + Europa_no_UE27 (2021+)** cuadra con `pob_extranj` (máx. 2 personas de error, sumando los 8 grupos).
   - Hay que exportar `pob_europa_sin_espana` como grupo coherente para el shift-share.
   - Quedan **7 grupos de origen** (Europa, África, Sudamérica, Centroamérica-Caribe, Norteamérica, Asia, Oceanía + apátridas). Para identificar por shocks (Borusyak et al.) son muy pocos; la identificación tendría que venir de las cuotas (Goldsmith-Pinkham et al.), con 17 unidades. Esto hay que decirlo en F3.
4. **Flujos de inmigración por CCAA:**
   - la tabla 69691 (EMCR, CCAA anual sin nacionalidad) aparece citada como alternativa en `fuentes_fallidas.md`, pero no se ha descargado;
   - 59013 solo cubre desde 2023T2.
   - F3 tendrá que usar Δ stocks de 77019. Si se quiere el flujo, hay que descargar 69691 o documentar por qué no.
5. **`tipo_bce` 2026Q3 = NaN** a pesar de que hubo un cambio el 2026-09-16. Es la regla conservadora de no extrapolar más allá de la última fecha observada. No afecta a la muestra hasta 2026Q2.
6. **`notariado_viv_extranj` (València ciudad):** con mi relectura independiente de los 5 PDF (sección 2) se puede pasar `validado` de `plausibilidad` a **sí**. El rol debe seguir siendo robustez porque N = 5.
7. **Coherencia de ECP:** las observaciones de 1 de enero y 1 de julio se asignan a T1 y T3, y desde 2021 la serie es trimestral, con stock a principio de trimestre. Es correcto, pero hay que anotar en F2 que el stock de inicio de trimestre va **adelantado** respecto a los flujos del trimestre.
8. Diferencias `d_ln_` de series sparse (`registradores_compraventas_anual`, `notariado_cgn_extranj`, `serpavi_esp_constante`): todas son NaN, y solo `d4_ln_` tiene valores. Conviene no generarlas, o decirlo en el diccionario.
9. `docs/fallidas/serpavi.md` todavía no menciona la variante de composición constante ni la no-independencia frente al IPVA (sí están en `serpavi_validacion.csv`).

## 5. `docs/diccionario_variables.md` frente a `data/processed`

Es coherente en lo esencial:
- columnas, N, primer y último dato, recuentos de banderas (p. ej. `pob_total_interp` 52, `pob_extranj_interp` 38, `tipo_bce_interp` 80, `pob_*_interp` del panel 1.173 = 17 × 23 × 3);
- muestra base 74 (2008Q1-2026Q2);
- roles, origen, validado y error_max.

Lo regenera `build_dataset.py`, así que no puede desalinearse de los datos.

Discrepancias encontradas:
- el calendario semestral del VUT INE (§2);
- el quiebre de la EPA no documentado (§4.2);
- el deflactor descrito como válido sin advertir que mezcla SA y NSA (§4.1);
- las unidades "suma móvil" aplicadas a €/m² (§2);
- `pob_extranj` nacional: el error_max "0 frente a ECP701" es una comprobación de consistencia entre tablas del INE, no un contraste independiente. Hay que dejarlo como `plausibilidad` (ya lo está) y no presentarlo como una validación externa.

## 6. Fuentes fallidas (`docs/fuentes_fallidas.md`, `docs/fallidas/*.md`)

Son completas y veraces en lo que he podido comprobar:
- URLs probadas, códigos HTTP y alternativas;
- sin OCR;
- el bug de los municipios del Notariado, documentado con cifras que coinciden con las mías;
- el defecto de origen de 4T2022 (995);
- la imposibilidad de reconstruir trimestres de Registradores sin valor semilla;
- el quiebre de grupos UE en 2020.

Omisiones:
1. 69691 (CCAA, anual) aparece como alternativa, pero no se dice que no se haya descargado (§4.5.4).
2. No consta el cambio de calendario del VUT INE (feb/ago → may/nov).
3. Sigue pendiente el orden de ediciones de los actos.

## 7. Referencias (`docs/literatura.md`)

He comprobado 4 referencias con búsqueda web:

| Referencia | Comprobación | Resultado |
|---|---|---|
| González y Ortega (2013), *J. Regional Science* 53(1), 37-59; flujo 17 % → precios +52 %, construcción 37 % | IZA DP 4333 y ficha de UPF | ✓ Revista, volumen, páginas y magnitudes coinciden. |
| Accetturo et al. (2014), *RSUE* 45, 45-56; DT BdI 866 | IDEAS/RePEc | ✓ Bibliografía correcta. Las magnitudes vienen del DT, como se declara. |
| Banco de España, Informe Anual 2025 (18/06/2026): déficit de ~750.000 en 2021-2025, 240.000 hogares frente a 92.000 terminadas, 3,7 %, elasticidad de ~0,45 | Prensa del 18/06/2026 (elDiario.es, Euronews, El Debate, Brainsre) | ✓ Todas las cifras aparecen. La de 0,45 solo la vi en una fuente secundaria; el documento dice que se tomó del PDF oficial. |
| Sá (2015), *EJ* 125(587), 1393-1424; signo negativo | IZA DP 5893 y IDEAS | ✓ Bibliografía y signo correctos. La cifra de −1,6 % está bien marcada como "de la versión de trabajo, no comprobada en el artículo publicado". |

Defecto menor: Caldera y Johansson (2013) y Cavalleri et al. (2019) aparecen en "Bibliografía verificada" con la nota "no verificada de forma independiente". Deben etiquetarse **NO VERIFICADA** y añadirse a la lista de lagunas.

Signos esperados: la tabla es coherente con las referencias. El signo de la inmigración es ambiguo en Reino Unido (Sá), y eso está bien señalado. No hay discrepancias que afecten a los datos.

## 8. Cobertura para F2-F6

N cuenta los valores no NaN en 2008Q1-2026Q2 (74 trimestres como máximo). Para las series anuales, cuenta años.

| Variable clave | Fichero | N trimestral 2008Q1+ / años | Nota | ¿Apta? |
|---|---|---|---|---|
| `ipv` (80270, base 2025) | nacional_q | 74 | nativa | **sí** (F2) |
| `p_tasado`, `p_bde`, `hpi_eurostat` | nacional_q | 74 | nativas | sí (robustez del precio) |
| `ocupados` / `ocupados_sa` | nacional_q | 74 | quiebre de base EPA 2021 por documentar | sí |
| `renta_hog_real` | nacional_q | 74 | **estacionalidad espuria (§4.1)** | **no, hasta corregir** |
| `tipo_hip`, `euribor`, `tipo_bce` | nacional_q | 74 / 75 / 74 | agregados mensuales; tipo_bce como media de días | sí |
| `credito_nuevo`, `credito_stock` | nacional_q | 74 | — | sí |
| `permisos`, `costes`, `terminadas` | nacional_q | 74 | terminadas es un proxy MIVAU | sí |
| `visados` | nacional_q | 72 | 2 huecos de origen | sí (con NaN) |
| `compraventas`, `trans_extranjeros` | nacional_q | 74 | — | sí |
| `pob_extranj`, `pob_total` | nacional_q | 74 (26 interpolados, T2 y T4 de 2008-2020) | MA mecánico en Δ1 antes de 2021 | sí (mejor Δ4 o HAC) |
| `hogares_epa` | nacional_q | 74 | **quiebre 2021T1 (§4.2)** | sí, **con dummy** |
| `hogares_ecp` | nacional_q | 23 (2021Q1+) | — | no (solo robustez) |
| `inmig_anual` (EMCR) | nacional_q | 4 años | — | **no** |
| Inmigración anual Eurostat (raw, sin exportar) | — | 27 años (1998-2024) | quiebre 2021 | sí, anual (tras §4.4) |
| `notariado_cgn_extranj` | nacional_q / panel_a | 36 semestres; 19 años × 17 CCAA | — | sí (semestral o anual) |
| `registradores_compraventas_anual` | nacional_q | 18 años | — | robustez |
| `serpavi_esp_constante` | nacional_q | 14 años | — | robustez |
| `ipv` CCAA | panel_ccaa_q | 17 × 74 | — | sí (F5) |
| `p_tasado` CCAA | panel_ccaa_q | 17 × 58-74 | Navarra incompleta | sí |
| `trans_extranjeros` CCAA | panel_ccaa_q | 17 × 74 | **no está en panel_a** | sí (F5); hay que añadirla a panel_a para F3 |
| `terminadas` CCAA | panel_ccaa_q | 16 × 74 | sin Extremadura | sí (panel desequilibrado) |
| `pob_extranj` CCAA | panel_ccaa_q | 17 × 69 (867 interpolados) | anual disfrazada de trimestral | **solo anual** (panel_a: 17 × 24) |
| `pob_<grupo>` CCAA (77019) | panel_ccaa_a | 17 × 24 años (2002-2025); UE28/UE27 partidas | — | sí (F3), con un grupo Europa coherente |
| Flujos de inmigración por CCAA | panel_ccaa_nacionalidad | solo 2023T2+ (714 celdas) | — | no (usar Δ stock o descargar 69691) |
| `serpavi_vc_mediana` CCAA | panel_ccaa_a | 215 de 238 (2011-2024) | — | robustez |
| `registradores_extranj_pct` CCAA | panel_ccaa_a | 170 (2016-2025) | — | robustez |
| València: `p_tasado` municipio | valencia | 74 | — | sí (F6) |
| València: `trans_total` municipio | valencia | 73 | — | sí |
| València: `vut_stock_gva` | valencia | 60 (2010Q1-2024Q4) | quiebres regulatorios | sí, con dummies |
| València: `pob_extranjera` municipio | valencia | 25 años (1998-2022); 15 desde 2008 | — | solo anual / descriptivo |
| València: `ipva`, `serpavi_vc_mediana` | valencia | 14 años | — | descriptivo / robustez |
| València: `notariado_viv_*_prov` | valencia | 32 (2018-2025) | — | robustez (muestra corta) |
| València: `notariado_viv_extranj` municipio | valencia | 5 años | — | no (descriptivo) |
| València: VUT INE | valencia | 13 semestres, calendario irregular | — | no (descriptivo) |

## 9. Cambios priorizados

**Bloqueantes** (antes de F2):
1. **Deflactor SA.** Usar `deflactor` = CNTR6597 / CNTR6652 y recalcular `renta_hog_real`, `inflacion_deflactor` y `tipo_hip_real`. Comprobar que la Δln media por trimestre deja de tener patrón estacional (§4.1).
2. **Quiebre EPA 2021T1.** Documentar el quiebre de `hogares_epa` (definición de hogar y base del Censo 2021), añadir la dummy `quiebre_epa_2021` y anotar el posible efecto en `ocupados` (§4.2).
3. **Banderas.** Sustituir el booleano `_interp` por `<var>_metodo` (categórico) con el mismo criterio en los 4 ficheros. `_interp` = TRUE solo para interpolación log-lineal (§4.3).
4. **Inmigración anual.** Exportar `inmig_anual_eurostat` 1998-2024 con la dummy `quiebre_emcr_2021` y pasar `inmig_anual` (EMCR, N=4) a robustez (§4.4).

**No bloqueantes** (antes de F3/F5, por prioridad):
5. Añadir a `panel_ccaa_a` las variables `trans_extranjeros`, `visados`, `terminadas` e `ipc_alquiler`, y el grupo coherente `pob_europa_sin_espana`.
6. Advertir en el diccionario que `panel_ccaa_q.pob_*` es anual (usar `panel_ccaa_a` o Δ4) y que la población del panel trimestral termina en 2025Q1.
7. Corregir en el diccionario el calendario del VUT INE (may/nov → T2/T4 desde 2024-11) y las unidades de Registradores (`pm2` e `imp` no son sumas).
8. Crear `gva_validacion.csv` (stock reconstruido, CV = Σ municipios, padrón frente a INE) y la columna `nota` para `vut_foto_*`.
9. Pasar `notariado_viv_extranj` a `validado=sí` (relectura independiente hecha), manteniendo rol robustez.
10. Literatura: marcar Caldera y Johansson (2013) y Cavalleri et al. (2019) como **NO VERIFICADA**.
11. Comprimir `gva_vut_municipio.csv` y `t_es_csv_bdsc_33946.csv` (`.csv.gz`) o pasarlos a LFS; documentar que 69691 no se ha descargado (o descargarlo); arreglar el orden de ediciones de los actos del Notariado.
12. Actualizar `docs/fallidas/serpavi.md` (composición constante; IPVA no independiente).

Fuentes web consultadas:
- https://www.iza.org/en/publications/dp/4333/immigration-and-housing-booms-evidence-from-spain
- https://ideas.repec.org/p/bdi/wptemi/td_866_12.html
- https://www.eldiario.es/economia/banco-espana-eleva-750-000-viviendas-faltan-anticipa-deficit-agravara-proximos-anos_1_13313634.html
- https://es.euronews.com/business/2026/06/18/el-banco-de-espana-senala-un-deficit-de-750000
- https://brainsre.news/banco-espana-deficit-vivienda-espana-3-7/
- https://ideas.repec.org/p/iza/izadps/dp5893.html
- https://www.ine.es/inebaseDYN/epa30308/docs/epa_cambios2021.pdf
- https://www.ine.es/inebaseDYN/epa30308/docs/medida_efecto_epa_cambios2021.pdf
- https://ine.es/dyngs/Prensa/cbEPA2021.htm
