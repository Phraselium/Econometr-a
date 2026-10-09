# Diccionario de variables

> Generado por `src/build_dataset.py` (no editar a mano). Reconstrucción: `make clean`.

Convenciones comunes:

- **Trimestre**: `trimestre` = `2008Q1`; `fecha` = primer día del trimestre.
- **Logs**: `ln_<var>` = ln(var) con NaN si var <= 0. **Diferencias**: `d_ln_<var>` = Δ1 trimestral del log; `d4_ln_<var>` = Δ4 (interanual) del log.
- **Tipos (en %)**: sin log; `d_<var>` = Δ1 trimestral en puntos porcentuales.
- **Agregación mensual→trimestral**: media o suma de los 3 meses, exigiendo los 3 meses (si falta alguno, NaN). Stock: valor del último mes del trimestre.
- **Interpolación**: nunca fuera del rango observado; los huecos finales quedan NaN. Columnas `<var>_interp` marcan filas interpoladas.
- **Huecos internos**: NaN entre el primer y el último dato no NaN.
- **Retardos** no se crean aquí (se hacen en los scripts de modelos).

## A. `data/processed/nacional_q.csv` (trimestral, nacional)

| Variable | Fuente | Archivo raw | Código / serie | Unidad | Frecuencia original | Agregación | Transformaciones | Interpolación / nº obs. afectadas | Primer dato | Último dato | Huecos internos |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `ipv` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | IPV1209 (Nacional. General. Índice.) | índice | trimestral (2007T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2007Q1 | 2026Q2 | 0 |
| `ipv_nueva` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | IPV1613 (Vivienda nueva. Índice.) | índice | trimestral (2007T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2007Q1 | 2026Q2 | 0 |
| `ipv_usada` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | IPV1618 (Vivienda segunda mano. Índice.) | índice | trimestral (2007T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2007Q1 | 2026Q2 | 0 |
| `ipv15` | INE IPV, tabla 25171 (base 2015, robustez) | `ine_ipv_25171.csv` | IPV769 (Nacional. General. Índice.) | índice | trimestral (2007T1-2025T4) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2007Q1 | 2025Q4 | 0 |
| `p_tasado` | MIVAU, Boletín (tabla 35101000) | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_nacional | €/m2 | trimestral (1995T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 1995Q1 | 2026Q2 | 0 |
| `p_bde` | Banco de España, be2507 | `bde_precio_vivienda_libre.csv` | DHIVTNOAPLPMMUVT_RLI.T (total nacional) | €/m2 | trimestral (fecha = mes de cierre) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 1995Q1 | 2026Q2 | 0 |
| `hpi_eurostat` | Eurostat prc_hpi_q | `eurostat_hpi.csv` | Q\|TOTAL\|I15_Q\|ES | índice 2015=100 | trimestral (2005T4+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2005Q4 | 2026Q2 | 0 |
| `ocupados` | INE EPA, tabla 65302 / EPA387796 | `ine_epa_ocupados.csv` | EPA387796 (Total Nacional. Ambos sexos. Total. Ocupados.) | miles de personas (NSA) | trimestral (2002T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2002Q1 | 2026Q2 | 0 |
| `ocupados_sa` | Derivada (STL) | `ine_epa_ocupados.csv` | EPA387796 | miles (SA) | trimestral | STL(period=4, robust=True) sobre log; nivel = exp(log - estacional) | ln_, d_ln_, d4_ln_ | ninguna | 2002Q1 | 2026Q2 | 0 |
| `renta_hog` | Eurostat nasq_10_nf_tr | `eurostat_renta_hogares.csv` | Q\|CP_MEUR\|RECV\|S14_S15\|B6G\|SCA\|ES | M€ corrientes (SCA) | trimestral (1999T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 1999Q1 | 2026Q2 | 0 |
| `deflactor` | Derivada: INE CNT | `ine_cnt_pib_oferta_corrientes.csv / ine_cnt_pib_oferta_volumen.csv` | CNTR6548 (PIB mercado, corrientes, NSA) / CNTR6721 (PIB mercado, volumen encadenado, NSA) | índice 2020=100 | trimestral (1995T1+) | cociente nominal/volumen, reescalado a media 2020 = 100 | ln_, d_ln_, d4_ln_ | ninguna | 1995Q1 | 2026Q2 | 0 |
| `renta_hog_real` | Derivada | `eurostat_renta_hogares.csv + INE CNT` | renta_hog / deflactor x 100 | M€ a precios de 2020 | trimestral | cociente | ln_, d_ln_, d4_ln_ | ninguna | 1999Q1 | 2026Q2 | 0 |
| `tipo_hip` | BCE MIR, nuevas operaciones vivienda | `ecb_tipo_hipotecario_es.csv` | MIR.M.ES.B.A2C.AM.R.A.2250.EUR.N | % anual | mensual (2003-01+) | media de 3 meses (exige 3) | d_ (Δ1 pp) | ninguna | 2003Q1 | 2026Q2 | 0 |
| `euribor` | BCE, Euribor 1 año | `ecb_euribor1y.csv` | FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA | % anual | mensual (1994-01+) | media de 3 meses | d_ (Δ1 pp) | ninguna | 1995Q1 | 2026Q3 | 0 |
| `tipo_bce` | BCE, tipo MRR (operaciones principales) | `ecb_tipo_oficial.csv` | FM.B.U2.EUR.4F.KR.MRR_FR.LEV | % anual | cambios de tipo (48 obs.) | escalonado diario (último valor vigente hasta la última fecha observada) y media trimestral de días | d_ (Δ1 pp) | log-lineal entre observaciones; tipo_bce_interp (ver nº); nº obs. = 80 | 1999Q1 | 2026Q2 | 0 |
| `tipo_hip_real` | Derivada | `ecb_tipo_hipotecario_es.csv + INE CNT` | tipo_hip - inflacion_deflactor | pp | trimestral | resta | d_ (Δ1 pp) | ninguna | 2003Q1 | 2026Q2 | 0 |
| `inflacion_deflactor` | Derivada | `INE CNT` | 100 x (deflactor_t / deflactor_{t-4} - 1) | % interanual | trimestral | tasa interanual exacta | d_ (Δ1 pp) | ninguna | 1996Q1 | 2026Q2 | 0 |
| `ipc_alquiler` | INE IPC, subclase alquiler de vivienda | `ine_ipc_alquiler.csv` | IPC290887 (Nacional. Alquiler de vivienda. Índice.) | índice | mensual (2002-01+) | media de 3 meses | ln_, d_ln_, d4_ln_ | ninguna | 2002Q1 | 2026Q2 | 0 |
| `ipc_alquiler_yoy` | INE IPC, subclase alquiler de vivienda | `ine_ipc_alquiler.csv` | IPC290886 (Variación anual) | % interanual | mensual (2002-01+) | media de 3 meses | d_ (Δ1 pp) | ninguna | 2002Q1 | 2026Q2 | 0 |
| `credito_nuevo` | BCE MIR, nuevo crédito vivienda | `ecb_nuevo_credito_vivienda_es.csv` | MIR.M.ES.B.A2C.A.B.A.2250.EUR.N | M€ (flujo) | mensual (2003-01+) | suma de 3 meses | ln_, d_ln_, d4_ln_ | ninguna | 2003Q1 | 2026Q2 | 0 |
| `credito_stock` | BCE BSI, stock crédito vivienda | `ecb_stock_credito_vivienda_es.csv` | BSI.M.ES.N.A.A22.A.1.U2.2250.Z01.E | M€ (stock) | mensual (2003-01+) | valor de fin de trimestre (mes 3) | ln_, d_ln_, d4_ln_ | ninguna | 2003Q1 | 2026Q2 | 0 |
| `permisos` | Eurostat sts_cobp_q | `eurostat_permisos.csv` | Q\|BPRM_DW\|CPA_F41001_X_410014\|SCA\|I21\|ES | índice 2021=100 (SCA) | trimestral (2000T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2000Q1 | 2026Q2 | 0 |
| `costes` | Eurostat sts_copi_q | `eurostat_costes.csv` | Q\|COST\|CPA_F41001_X_410014\|NSA\|I21\|ES | índice 2021=100 (NSA) | trimestral (1980T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 1995Q1 | 2026Q2 | 0 |
| `prod_constr` | Eurostat sts_copr_q | `eurostat_produccion_construccion.csv` | Q\|PRD\|F\|SCA\|I21\|ES | índice 2021=100 (SCA) | trimestral (2005T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2005Q1 | 2026Q2 | 0 |
| `visados` | MIVAU Boletín, tabla 32100500 (PROXY) | `mivau_visados.csv` | viv_libres_iniciadas_nacional | viviendas (flujo) | mensual (2008-01+) | suma de 3 meses. Proxy: viviendas libres iniciadas MIVAU, no visados CSCAE | ln_, d_ln_, d4_ln_ | ninguna | 2008Q1 | 2026Q2 | 2 |
| `terminadas` | MIVAU Boletín, tabla 32101000 (PROXY) | `mivau_fin_obra.csv` | viv_libres_terminadas_nacional | viviendas (flujo) | mensual (2008-01+) | suma de 3 meses. Proxy: viviendas libres terminadas MIVAU, no certificados de fin de obra CSCAE | ln_, d_ln_, d4_ln_ | ninguna | 2008Q1 | 2026Q2 | 0 |
| `compraventas` | INE ETDP, tabla 6150 | `ine_etdp_compraventas.csv` | ETDP1826 (Total Nacional. General. Compraventa. Número.) | número (flujo) | mensual (2007-01+) | suma de 3 meses | ln_, d_ln_, d4_ln_ | ninguna | 2007Q1 | 2026Q2 | 0 |
| `compraventas_sa` | Derivada (STL) | `ine_etdp_compraventas.csv` | ETDP1826 | número (SA) | trimestral | STL(period=4, robust=True) sobre log; nivel = exp(log - estacional) | ln_, d_ln_, d4_ln_ | ninguna | 2007Q1 | 2026Q2 | 0 |
| `trans_total` | MIVAU Boletín, tabla 34010110 (notarios) | `mivau_transacciones_total.csv` | tx_total_nacional | transacciones (flujo) | trimestral (2004T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2004Q1 | 2026Q1 | 0 |
| `trans_extranjeros` | MIVAU Boletín, tabla 340101i0 / residentes extranjeros | `mivau_transacciones_extranjeros.csv` | tx_extranj_residentes_total_nacional | transacciones (flujo) | trimestral (2007T1+) | nativo | ln_, d_ln_, d4_ln_ | ninguna | 2007Q1 | 2026Q2 | 0 |
| `pob_total` | INE ECP, serie nacional | `ine_ecp_nacional.csv` | ECP320 (Total Nacional. Todas las edades. Total.) | personas (a 1 de enero/julio, stock) | semestral 1971-2020 (ene/jul); trimestral 2021+ | stock: trimestre de la fecha; trimestres intermedios interpolados | ln_, d_ln_, d4_ln_ | log-lineal entre observaciones; pob_total_interp (ver nº); nº obs. = 52 | 1995Q1 | 2026Q3 | 0 |
| `pob_extranj` | INE ECP, serie nacional | `ine_ecp_nacional.csv` | ECP701 (Total Nacional. Extranjera. Todas las edades. Total.) | personas (stock) | semestral 2002-2020; trimestral 2021+ | como pob_total | ln_, d_ln_, d4_ln_ | log-lineal entre observaciones; pob_extranj_interp (ver nº); nº obs. = 38 | 2002Q1 | 2026Q3 | 0 |
| `hogares` | INE ECP, tabla 60131 | `ine_hogares_60131.csv` | ECP355533 (Total Nacional. Total. Hogares en viviendas familiares.) | hogares (stock) | trimestral (2021T1+) | nativo; sin interpolación ni retropolación | ln_, d_ln_, d4_ln_ | ninguna | 2021Q1 | 2026Q3 | 0 |
| `inmig_anual` | INE EMCR, tabla 69687 (ANUAL) | `ine_migraciones_total_anual.csv` | EM1765217 (Todas las edades. Total. Dato base. Inmigraciones procedentes del extranjero.) | personas (flujo anual) | anual (2021-2024) | anual asignado solo al primer trimestre del año (no trimestralizar) | ninguna (anual) | ninguna | 2021Q1 | 2024Q1 | 9 |

Variables derivadas con la misma regla de transformación: `ln_`, `d_ln_`, `d4_ln_` para niveles positivos; `d_` para tipos y tasas (ver lista de columnas en el CSV).

**Notas de método**
- `ipc_alquiler` usa el índice de la subclase alquiler (IPC290887) y `ipc_alquiler_yoy` la variación anual (IPC290886); en el CSV la tasa aparece como `ipc_alquiler_yoy` con `d_`.
- `deflactor` = PIB nominal NSA (CNTR6548) / PIB volumen encadenado NSA (CNTR6721), reescalado para que la media de 2020 sea 100 (el volumen encadenado tiene media 2020 = 100). Es un deflactor implícito aproximado, no el oficial del INE.
- `renta_hog_real` = renta_hog / deflactor × 100 (M€ a precios de 2020).
- `tipo_hip_real` = tipo_hip − inflacion_deflactor (tasa interanual del deflactor, en pp). La HICP de BCE (`ecb_hicp_es.csv`) termina en 2025-12 y no se usa.
- `visados`: faltan abril-junio de 2016 y de 2017 en el origen (MIVAU), así que 2016T2 y 2017T2 quedan NaN (regla de los 3 meses).
- `ocupados_sa` y `compraventas_sa`: STL(period=4, robust=True) sobre log, en el bloque contiguo más largo de datos; nivel = exp(log − estacional). Solo para estas dos series.
- `pob_total` (ECP320) y `pob_extranj` (ECP701) son semestrales hasta 2020 (1 ene y 1 jul) y trimestrales desde 2021. Los trimestres intermedios (T2 y T4 de 1995-2020) se interpolan en logaritmos entre observaciones. La cifra de interpolados figura en la columna de la tabla y en `pob_*_interp`. Validación cruzada: ECP701 de `ine_ecp_56936.csv` (2002-2025) y de `ine_ecp_59585.csv` (2025T2+), ver sección de comprobaciones.
- `tipo_bce_interp`: True cuando el trimestre no tiene cambio de tipo (el valor es el vigente desde un cambio anterior).
- `visados` y `terminadas` son proxies del Boletín MIVAU (viviendas libres iniciadas/terminadas), no los visados de dirección de obra del CSCAE ni los certificados de fin de obra.
- `hogares`: serie trimestral solo desde 2021T1 (tabla 60131). No se interpola ni se retropola; antes de 2021 es NaN.
- `inmig_anual`: flujo anual (EMCR, tabla 69687) asignado al **primer trimestre** de cada año. No es un flujo trimestral; no usar sin agregación anual.
- `inmig_q` (59011 total nacional) **no se incluye**: la tabla no tiene serie total y las nacionalidades están casi todas vacías (ver `docs/fuentes_fallidas.md`).
- `credito_stock`: fin de trimestre. `credito_nuevo`: suma de 3 meses (M€).

### Dummies y muestra

- `q1`…`q4`: dummies trimestrales. `muestra_base` = True desde 2008Q1 hasta el último trimestre con `ipv` no NaN.

## B. `data/processed/panel_ccaa_q.csv` (17 CCAA × trimestre, formato largo)

Códigos INE de CCAA: 01 Andalucía, 02 Aragón, 03 Asturias (Principado de), 04 Balears (Illes), 05 Canarias, 06 Cantabria, 07 Castilla y León, 08 Castilla-La Mancha, 09 Cataluña, 10 Comunitat Valenciana, 11 Extremadura, 12 Galicia, 13 Madrid (Comunidad de), 14 Murcia (Región de), 15 Navarra (Comunidad Foral de), 16 País Vasco, 17 La Rioja. **Ceuta (18) y Melilla (19) excluidas.** Los nombres se normalizan con `slug()` (sin acentos) y `SLUG_ALIAS` (p. ej. 'Comunidad Valenciana' de MIVAU = 'Comunitat Valenciana' de INE).

| Variable | Fuente | Archivo raw | Código / serie | Unidad | Frecuencia | Agregación | Transformaciones | Cobertura (CCAA con datos) | Primer dato (mín. entre CCAA) | Último dato (máx. entre CCAA) |
|---|---|---|---|---|---|---|---|---|---|---|
| `ipv` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | IPV1392 (CCAA General) | índice | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2007Q1 | 2026Q2 |
| `ipv_nueva` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | '<CCAA>. Vivienda nueva. Índice.' | índice | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2007Q1 | 2026Q2 |
| `ipv_usada` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | '<CCAA>. Vivienda segunda mano. Índice.' | índice | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2007Q1 | 2026Q2 |
| `p_tasado` | MIVAU, tabla 35101000 | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_ccaa_<slug> | €/m2 | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 1995Q1 | 2026Q2 |
| `ocupados` | INE EPA, tabla 65302 | `ine_epa_ocupados_ccaa.csv` | '<CCAA>. Ambos sexos. Total. Ocupados. Valor absoluto.' | miles | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2002Q1 | 2026Q2 |
| `compraventas` | INE ETDP, tabla 6150 | `ine_etdp_compraventas.csv` | '<CCAA>. General. Compraventa. Número.' | número | mensual | suma de 3 meses | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2007Q1 | 2026Q2 |
| `trans_total` | MIVAU, tabla 34010110 | `mivau_transacciones_total.csv` | tx_total_ccaa_<slug> | transacciones | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2004Q1 | 2026Q1 |
| `trans_extranjeros` | MIVAU, tabla 340101i0 (total) | `mivau_transacciones_extranjeros.csv` | tx_extranj_residentes_total_ccaa_<slug> | transacciones | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2007Q1 | 2026Q2 |
| `visados` | MIVAU, tabla 32100500 (PROXY) | `mivau_visados.csv` | viv_libres_iniciadas_ccaa_<slug> | viviendas | mensual | suma de 3 meses | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2008Q1 | 2026Q2 |
| `terminadas` | MIVAU, tabla 32101000 (PROXY) | `mivau_fin_obra.csv` | viv_libres_terminadas_ccaa_<slug> | viviendas | mensual | suma de 3 meses | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 16/17 | 2008Q1 | 2026Q2 |
| `ipc_alquiler` | INE IPC, alquiler de vivienda | `ine_ipc_alquiler.csv` | '<CCAA>. Alquiler de vivienda. Índice.' | índice | mensual | media de 3 meses | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | 17/17 | 2002Q1 | 2026Q2 |

**Huecos de origen**: `terminadas` (MIVAU 32101000) no tiene Extremadura en el Boletín, así que esa CCAA queda NaN en esa variable. `p_tasado` de Navarra tiene solo los trimestres en que MIVAU publica esa CCAA (ver `DUP_NOTES`).

**No incluido en el panel (sin dato en `data/raw`)**: `pob_total` y `pob_extranj` por CCAA. Las tablas de población de INE descargadas (56936, 59585 y ECP320/701 de `ine_ecp_nacional.csv`) son solo nacionales; no hay ECP por comunidad. `inmig` por CCAA agregada: la tabla 59013 no tiene total y tiene pocas celdas con valor (ver sección D). Ceuta y Melilla no se incluyen.

## B2. `data/processed/panel_ccaa_nacionalidad.csv`

Flujos de inmigración de la tabla INE 59013 (CCAA × nacionalidad, trimestral desde 2023T2). Solo celdas con valor: **714 filas** (de 1.159 series × 14 trimestres; el resto está vacío en el origen y no se rellena). Stock de población extranjera por CCAA × nacionalidad: **no disponible** en `data/raw` (las tablas ECP de nacionalidad son nacionales). El instrumento shift-share requiere ese stock; falta.

## C. `data/processed/valencia.csv` (territorio × trimestre × variable)

| Variable | Territorio | Archivo raw | Código / serie | Unidad | Frecuencia original | Tratamiento | Primer | Último | Nº trimestres |
|---|---|---|---|---|---|---|---|---|---|
| `p_tasado` | Comunitat Valenciana | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_ccaa_comunidad_valenciana | €/m2 | trimestral | nativo | 1995Q1 | 2026Q2 | 126 |
| `p_tasado` | España | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_nacional | €/m2 | trimestral | nativo | 1995Q1 | 2026Q2 | 126 |
| `p_tasado` | Provincia de València | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_provincia_valencia_valencia | €/m2 | trimestral | nativo | 1995Q1 | 2026Q2 | 126 |
| `p_tasado` | València (municipio) | `mivau_valor_tasado_municipios.csv` | valor_tasado_mun_valencia | €/m2 | trimestral | nativo | 2005Q1 | 2026Q2 | 86 |
| `trans_total` | Comunitat Valenciana | `mivau_transacciones_total.csv` | tx_total_ccaa_comunitat_valenciana | transacciones | trimestral | nativo | 2004Q1 | 2026Q1 | 89 |
| `trans_total` | España | `mivau_transacciones_total.csv` | tx_total_nacional | transacciones | trimestral | nativo | 2004Q1 | 2026Q1 | 89 |
| `trans_total` | València (municipio) | `mivau_transacciones_municipios.csv` | tx_municipio_valencia | transacciones | trimestral | nativo | 2004Q1 | 2026Q1 | 89 |
| `trans_extranjeros` | Comunitat Valenciana | `mivau_transacciones_extranjeros.csv` | tx_extranj_residentes_total_ccaa_comunitat_valenciana | transacciones | trimestral | nativo (sin dato municipal en raw) | 2007Q1 | 2026Q2 | 78 |
| `trans_extranjeros` | España | `mivau_transacciones_extranjeros.csv` | tx_extranj_residentes_total_nacional | transacciones | trimestral | nativo (sin dato municipal en raw) | 2007Q1 | 2026Q2 | 78 |
| `ipv` | Comunitat Valenciana | `ine_ipv_80270.csv` | IPV1392 (Comunitat Valenciana. General. Índice.) | índice | trimestral | nativo | 2007Q1 | 2026Q2 | 78 |
| `ipv` | España | `ine_ipv_80270.csv` | IPV1209 (Nacional. General. Índice.) | índice | trimestral | nativo | 2007Q1 | 2026Q2 | 78 |
| `vut_viviendas_turisticas` | València (municipio) | `ine_vut_valencia_municipio.csv` | ine_vut_valencia_valencia_viviendas_turisticas | nº viviendas | semestral (feb/ago) | sin interpolar; feb→T1, ago→T3 | 2020Q3 | 2026Q2 | 13 |
| `vut_plazas` | València (municipio) | `ine_vut_valencia_municipio.csv` | ine_vut_valencia_valencia_plazas | plazas | semestral | sin interpolar | 2020Q3 | 2026Q2 | 13 |
| `vut_plazas_por_vivienda` | València (municipio) | `ine_vut_valencia_municipio.csv` | ine_vut_valencia_valencia_plazas_por_vivienda | plazas/vivienda | semestral | sin interpolar | 2020Q3 | 2026Q2 | 13 |
| `vut_pct_sobre_total` | València (municipio) | `ine_vut_valencia_municipio.csv` | ine_vut_valencia_valencia_pct_viv_turisticas_sobre_total | proporción | semestral | sin interpolar | 2020Q3 | 2026Q2 | 13 |
| `ipva` | València (municipio) | `ine_ipva_municipal.csv` | IPVA8471 (Valencia. Índice. Total.) | índice | anual | sin interpolar; año→T1 | 2011Q1 | 2024Q1 | 14 |

Formato largo: filas solo con valor (sin NaN). Los datos semestrales y anuales no se interpolan. **Excluido**: `vlc_precio_vivienda_libre.csv` (ver sección D).

## D. Fuentes raw no utilizadas, excluidas o con duplicados

Duplicados idénticos en origen (se usa el primer código, verificado valor a valor):

- MIVAU CCAA 15 (tx_total): alias ['tx_total_ccaa_navarra_c_foral_de', 'tx_total_ccaa_navarra_comunidad_foral_de']; se usa 'tx_total_ccaa_navarra_c_foral_de' (más observaciones)
- MIVAU CCAA 15 (valor_tasado_libre): alias ['valor_tasado_libre_ccaa_navarra_com_foral_de', 'valor_tasado_libre_ccaa_navarra_comunidad_foral_de']; se usa 'valor_tasado_libre_ccaa_navarra_comunidad_foral_de' (más observaciones)
- balears_illes / 'General. Compraventa. Número.': ['ETDP1806', 'ETDP3909'] idénticas en origen; se usa ETDP1806
- cantabria / 'General. Compraventa. Número.': ['ETDP1796', 'ETDP3904'] idénticas en origen; se usa ETDP1796
- rioja_la / 'General. Compraventa. Número.': ['ETDP1741', 'ETDP3884'] idénticas en origen; se usa ETDP1741

| Archivo | Motivo |
|---|---|
| `bde_tipo_hipotecario_referencia.csv` | BdE D_1T9H0000 (tipo medio adquisición vivienda libre). Se usa el MIR del BCE según especificación. |
| `ecb_hicp_es.csv` | IAPC España (ICP ANR), termina 2025-12. El deflactor del PIB se usa como inflación; no entra en nacional_q. |
| `ine_cnt_demanda_corrientes.csv / ine_cnt_demanda_volumen.csv` | Mismo PIB a precios de mercado que la oferta; el deflactor usa ine_cnt_pib_oferta_*. |
| `ine_cnt_renta_disponible.csv` | Serie 80333 es capacidad/necesidad de financiación, no renta de hogares. |
| `eurostat_empleo_nuts2.csv, eurostat_inmigracion_anual.csv` | No especificados en la base; disponibles para trabajo posterior. |
| `ine_migraciones_nacionalidad.csv (59011)` | No existe serie total: las 61 nacionalidades solo tienen dato en ~10 celdas por trimestre. Sumar daría cifras parciales; no se usa (inmig_q omitida). |
| `ine_ecp_56936.csv` | Población solo a nivel nacional por nacionalidad y edad (sin CCAA). Se usa solo para validar ECP701. |
| `ine_ecp_59585.csv` | Continuación 2025T2+ (ECP4961, ECP701). Se usa solo para validar ECP701. |
| `ine_ipva_nacional_ccaa.csv, ine_vut_nacional_ccaa_prov.csv` | No especificados para este módulo. |
| `mivau_parque.csv, mivau_transacciones_residencia.csv` | No especificados. |
| `ine_ipv_25171.csv` | Solo IPV769 (base 2015) como robustez: incluido en nacional_q (ipv15). |
| `vlc_precio_vivienda_libre.csv` | Excluido de valencia.csv: 5 trimestres (2021T2-2022T2), fuente primaria no indicada, las series están etiquetadas 'barcelona/madrid/...' con cabecera CKAN; no sirve para el modelo. |

## Cobertura de la muestra base 2008Q1+

| Variable | N en 2008Q1+ | Primer dato (no NaN) | Último dato (no NaN) |
|---|---|---|---|
| `ln_ipv` | 74 | 2008Q1 | 2026Q2 |
| `ln_ocupados` | 74 | 2008Q1 | 2026Q2 |
| `tipo_hip` | 74 | 2008Q1 | 2026Q2 |
| `ln_permisos` | 74 | 2008Q1 | 2026Q2 |
| `ln_costes` | 74 | 2008Q1 | 2026Q2 |
| `ln_renta_hog_real` | 74 | 2008Q1 | 2026Q2 |
| `ln_pob_extranj` | 74 | 2008Q1 | 2026Q2 |
| `ln_terminadas` | 74 | 2008Q1 | 2026Q2 |
| `ln_hogares` | 22 | 2021Q1 | 2026Q2 |

- **N completo** (filas con las 9 variables no NaN, 2008Q1+): **22**; **último trimestre común**: **2026Q2**.
- `ln_hogares` solo existe desde 2021T1 (tabla 60131) y restringe la muestra común. Sin ella (8 variables): N = **74**, último trimestre común = **2026Q2**.
- Los N de la tabla son de las variables `ln_` (en niveles logarítmicos); las diferencias `d_ln_` pierden 1 trimestre al inicio y `d4_ln_` pierde 4.

