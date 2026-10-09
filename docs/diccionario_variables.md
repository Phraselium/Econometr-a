# Diccionario de variables

> Generado por `src/build_dataset.py` (no editar a mano). Reconstrucción: `make clean`.

Convenciones comunes:

- **Trimestre**: `trimestre` = `2008Q1`; `fecha` = primer día del trimestre. En `panel_ccaa_a.csv` la clave es `anio` (año natural).
- **Logs**: `ln_<var>` = ln(var) con NaN si var <= 0. **Diferencias**: `d_ln_<var>` = Δ1 del log (trimestral en `_q`, anual en `_a`); `d4_ln_<var>` = Δ4 (interanual) del log en los trimestrales.
- **Tipos y porcentajes (en %)**: sin log; `d_<var>` = Δ1 en puntos porcentuales.
- **Agregación mensual→trimestral**: media o suma de los 3 meses, exigiendo los 3 meses (si falta alguno, NaN). Stock: valor del último mes del trimestre.
- **Interpolación**: solo log-lineal entre observaciones (nunca fuera del rango observado); huecos finales = NaN. Las columnas `<var>_interp` (booleanas) marcan toda transformación temporal: interpolación, desestacionalización, agregación mensual/anual y asignación de una frecuencia menor a un trimestre (ver 'Criterio de banderas').
- **Retardos**: no se crean aquí (se hacen en los scripts de modelos).
- **origen**: `api` (API INE/BCE/Eurostat o CKAN GVA), `xls` (XLS/XLSX/CSV oficial descargado), `pdf` (PDF con texto nativo, pdfplumber; **sin OCR** en ninguna serie), `derivado` (cálculo propio sobre fuentes anteriores).
- **validado**: `sí` = fuente oficial sin transformación no trivial, o contraste/cuadre pasado; `plausibilidad` = proxy, derivada, contraste no independiente o interpolada; `no` = no validada (**obligatoriamente rol=robustez**; ninguna variable actual tiene `no`).
- **error_max**: error máximo del contraste (de `*_validacion.csv` o del informe del revisor `docs/revision_f1_fuentes.md`); `—` = sin contraste específico.
- **rol**: `principal` (entra en el modelo principal), `robustez` (solo especificaciones alternativas), `excluida` (no entra en modelos; control).

## Criterio de banderas `<var>_interp`

- TRUE cuando el valor es (a) interpolado (`pob_*` entre 1 de enero/julio), (b) un agregado temporal de frecuencia mayor (medias/sumas de 3 o 4 meses, fin de trimestre), (c) desestacionalizado (STL), (d) asignado desde una serie anual o semestral (T4 para anuales; T2/T4 para semestrales; T1 para `inmig_anual`), o (e) escalonado (`tipo_bce`: trimestre sin cambio de tipo).
- Las series trimestrales nativas no llevan bandera. Los vacíos en origen no se imputan.

## A. `data/processed/nacional_q.csv` (trimestral, nacional)

Muestra base 2008Q1+. Serie PRINCIPAL de hogares: `hogares_epa`. `hogares` (60131) pasa a llamarse `hogares_ecp` (robustez).

| Variable | Fuente | Archivo raw | Código / serie | Unidad | Frecuencia original | Agregación / asignación | Transformaciones | Bandera `_interp` (nº TRUE) | origen | validado | error_max | rol | Primer dato | Último dato | Huecos internos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ipv` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | IPV1209 (Nacional. General. Índice.) | índice | trimestral (2007T1+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 2007Q1 | 2026Q2 | 0 |
| `ipv_nueva` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | IPV1613 (Vivienda nueva. Índice.) | índice | trimestral (2007T1+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 2007Q1 | 2026Q2 | 0 |
| `ipv_usada` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | IPV1618 (Vivienda segunda mano. Índice.) | índice | trimestral (2007T1+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 2007Q1 | 2026Q2 | 0 |
| `ipv15` | INE IPV, tabla 25171 (base 2015, robustez) | `ine_ipv_25171.csv` | IPV769 (Nacional. General. Índice.) | índice | trimestral (2007T1-2025T4) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | robustez | 2007Q1 | 2025Q4 | 0 |
| `p_tasado` | MIVAU, Boletín (tabla 35101000) | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_nacional | €/m2 | trimestral (1995T1+) | nativo | ln_, d_ln_, d4_ln_ | — | xls | sí | — | principal | 1995Q1 | 2026Q2 | 0 |
| `p_bde` | Banco de España, be2507 | `bde_precio_vivienda_libre.csv` | DHIVTNOAPLPMMUVT_RLI.T (total nacional) | €/m2 | trimestral (fecha = mes de cierre) | nativo | ln_, d_ln_, d4_ln_ | — | xls | sí | — | principal | 1995Q1 | 2026Q2 | 0 |
| `hpi_eurostat` | Eurostat prc_hpi_q | `eurostat_hpi.csv` | Q\|TOTAL\|I15_Q\|ES | índice 2015=100 | trimestral (2005T4+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 2005Q4 | 2026Q2 | 0 |
| `ocupados` | INE EPA, tabla 65302 / EPA387796 | `ine_epa_ocupados.csv` | EPA387796 (Total Nacional. Ambos sexos. Total. Ocupados.) | miles de personas (NSA) | trimestral (2002T1+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 2002Q1 | 2026Q2 | 0 |
| `ocupados_sa` | Derivada (STL) | `ine_epa_ocupados.csv` | EPA387796 | miles (SA) | trimestral | STL(period=4, robust=True) sobre log; nivel = exp(log - estacional) | ln_, d_ln_, d4_ln_ | `ocupados_sa_interp` (98) | derivado | plausibilidad | — | principal | 2002Q1 | 2026Q2 | 0 |
| `renta_hog` | Eurostat nasq_10_nf_tr | `eurostat_renta_hogares.csv` | Q\|CP_MEUR\|RECV\|S14_S15\|B6G\|SCA\|ES | M€ corrientes (SCA) | trimestral (1999T1+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 1999Q1 | 2026Q2 | 0 |
| `deflactor` | Derivada: INE CNT | `ine_cnt_pib_oferta_corrientes.csv / ine_cnt_pib_oferta_volumen.csv` | CNTR6548 (PIB mercado, corrientes, NSA) / CNTR6721 (PIB mercado, volumen encadenado, NSA) | índice 2020=100 | trimestral (1995T1+) | cociente nominal/volumen, reescalado a media 2020 = 100 | ln_, d_ln_, d4_ln_ | — | derivado | plausibilidad | — | principal | 1995Q1 | 2026Q2 | 0 |
| `renta_hog_real` | Derivada | `eurostat_renta_hogares.csv + INE CNT` | renta_hog / deflactor x 100 | M€ a precios de 2020 | trimestral | cociente | ln_, d_ln_, d4_ln_ | — | derivado | plausibilidad | — | principal | 1999Q1 | 2026Q2 | 0 |
| `tipo_hip` | BCE MIR, nuevas operaciones vivienda | `ecb_tipo_hipotecario_es.csv` | MIR.M.ES.B.A2C.AM.R.A.2250.EUR.N | % anual | mensual (2003-01+) | media de 3 meses (exige 3) | d_ (Δ1 pp) | `tipo_hip_interp` (94) | api | sí | — | principal | 2003Q1 | 2026Q2 | 0 |
| `euribor` | BCE, Euribor 1 año | `ecb_euribor1y.csv` | FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA | % anual | mensual (1994-01+) | media de 3 meses | d_ (Δ1 pp) | `euribor_interp` (127) | api | sí | — | principal | 1995Q1 | 2026Q3 | 0 |
| `tipo_bce` | BCE, tipo MRR (operaciones principales) | `ecb_tipo_oficial.csv` | FM.B.U2.EUR.4F.KR.MRR_FR.LEV | % anual | cambios de tipo (48 obs.) | escalonado diario (último valor vigente hasta la última fecha observada) y media trimestral de días | d_ (Δ1 pp) | `tipo_bce_interp` (80) escalonado | api | sí | — | principal | 1999Q1 | 2026Q2 | 0 |
| `tipo_hip_real` | Derivada | `ecb_tipo_hipotecario_es.csv + INE CNT` | tipo_hip - inflacion_deflactor | pp | trimestral | resta | d_ (Δ1 pp) | — | derivado | plausibilidad | — | principal | 2003Q1 | 2026Q2 | 0 |
| `inflacion_deflactor` | Derivada | `INE CNT` | 100 x (deflactor_t / deflactor_{t-4} - 1) | % interanual | trimestral | tasa interanual exacta | d_ (Δ1 pp) | — | derivado | plausibilidad | — | principal | 1996Q1 | 2026Q2 | 0 |
| `ipc_alquiler` | INE IPC, subclase alquiler de vivienda | `ine_ipc_alquiler.csv` | IPC290887 (Nacional. Alquiler de vivienda. Índice.) | índice | mensual (2002-01+) | media de 3 meses | ln_, d_ln_, d4_ln_ | `ipc_alquiler_interp` (98) | api | sí | — | principal | 2002Q1 | 2026Q2 | 0 |
| `ipc_alquiler_yoy` | INE IPC, subclase alquiler de vivienda | `ine_ipc_alquiler.csv` | IPC290886 (Variación anual) | % interanual | mensual (2002-01+) | media de 3 meses | d_ (Δ1 pp) | `ipc_alquiler_yoy_interp` (98) | api | sí | — | principal | 2002Q1 | 2026Q2 | 0 |
| `credito_nuevo` | BCE MIR, nuevo crédito vivienda | `ecb_nuevo_credito_vivienda_es.csv` | MIR.M.ES.B.A2C.A.B.A.2250.EUR.N | M€ (flujo) | mensual (2003-01+) | suma de 3 meses | ln_, d_ln_, d4_ln_ | `credito_nuevo_interp` (94) | api | sí | — | principal | 2003Q1 | 2026Q2 | 0 |
| `credito_stock` | BCE BSI, stock crédito vivienda | `ecb_stock_credito_vivienda_es.csv` | BSI.M.ES.N.A.A22.A.1.U2.2250.Z01.E | M€ (stock) | mensual (2003-01+) | valor de fin de trimestre (mes 3) | ln_, d_ln_, d4_ln_ | `credito_stock_interp` (94) | api | sí | — | principal | 2003Q1 | 2026Q2 | 0 |
| `permisos` | Eurostat sts_cobp_q | `eurostat_permisos.csv` | Q\|BPRM_DW\|CPA_F41001_X_410014\|SCA\|I21\|ES | índice 2021=100 (SCA) | trimestral (2000T1+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 2000Q1 | 2026Q2 | 0 |
| `costes` | Eurostat sts_copi_q | `eurostat_costes.csv` | Q\|COST\|CPA_F41001_X_410014\|NSA\|I21\|ES | índice 2021=100 (NSA) | trimestral (1980T1+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 1995Q1 | 2026Q2 | 0 |
| `prod_constr` | Eurostat sts_copr_q | `eurostat_produccion_construccion.csv` | Q\|PRD\|F\|SCA\|I21\|ES | índice 2021=100 (SCA) | trimestral (2005T1+) | nativo | ln_, d_ln_, d4_ln_ | — | api | sí | — | principal | 2005Q1 | 2026Q2 | 0 |
| `visados` | MIVAU Boletín, tabla 32100500 (PROXY) | `mivau_visados.csv` | viv_libres_iniciadas_nacional | viviendas (flujo) | mensual (2008-01+) | suma de 3 meses. Proxy: viviendas libres iniciadas MIVAU, no visados CSCAE | ln_, d_ln_, d4_ln_ | `visados_interp` (72) | xls | plausibilidad | — | principal | 2008Q1 | 2026Q2 | 2 |
| `terminadas` | MIVAU Boletín, tabla 32101000 (PROXY) | `mivau_fin_obra.csv` | viv_libres_terminadas_nacional | viviendas (flujo) | mensual (2008-01+) | suma de 3 meses. Proxy: viviendas libres terminadas MIVAU, no certificados de fin de obra CSCAE | ln_, d_ln_, d4_ln_ | `terminadas_interp` (74) | xls | plausibilidad | — | principal | 2008Q1 | 2026Q2 | 0 |
| `compraventas` | INE ETDP, tabla 6150 | `ine_etdp_compraventas.csv` | ETDP1826 (Total Nacional. General. Compraventa. Número.) | número (flujo) | mensual (2007-01+) | suma de 3 meses | ln_, d_ln_, d4_ln_ | `compraventas_interp` (78) | api | sí | — | principal | 2007Q1 | 2026Q2 | 0 |
| `compraventas_sa` | Derivada (STL) | `ine_etdp_compraventas.csv` | ETDP1826 | número (SA) | trimestral | STL(period=4, robust=True) sobre log; nivel = exp(log - estacional) | ln_, d_ln_, d4_ln_ | `compraventas_sa_interp` (78) | derivado | plausibilidad | — | principal | 2007Q1 | 2026Q2 | 0 |
| `trans_total` | MIVAU Boletín, tabla 34010110 (notarios) | `mivau_transacciones_total.csv` | tx_total_nacional | transacciones (flujo) | trimestral (2004T1+) | nativo | ln_, d_ln_, d4_ln_ | — | xls | sí | — | principal | 2004Q1 | 2026Q1 | 0 |
| `trans_extranjeros` | MIVAU Boletín, tabla 340101i0 / residentes extranjeros | `mivau_transacciones_extranjeros.csv` | tx_extranj_residentes_total_nacional | transacciones (flujo) | trimestral (2007T1+) | nativo | ln_, d_ln_, d4_ln_ | — | xls | sí | — | principal | 2007Q1 | 2026Q2 | 0 |
| `pob_total` | INE ECP, serie nacional | `ine_ecp_nacional.csv` | ECP320 (Total Nacional. Todas las edades. Total.) | personas (a 1 de enero/julio, stock) | semestral 1971-2020 (ene/jul); trimestral 2021+ | stock: trimestre de la fecha; trimestres intermedios interpolados (log-lineal entre observaciones) | ln_, d_ln_, d4_ln_ | `pob_total_interp` (52) interpolados log-lineal entre observaciones | api | plausibilidad | — | principal | 1995Q1 | 2026Q3 | 0 |
| `pob_extranj` | INE ECP, serie nacional | `ine_ecp_nacional.csv` | ECP701 (Total Nacional. Extranjera. Todas las edades. Total.) | personas (stock) | semestral 2002-2020; trimestral 2021+ | como pob_total | ln_, d_ln_, d4_ln_ | `pob_extranj_interp` (38) interpolados log-lineal entre observaciones | api | plausibilidad | 0 frente a ECP701 de 56936/59585 (trimestres publicados) | principal | 2002Q1 | 2026Q3 | 0 |
| `hogares_epa` | INE EPA, tabla 65269 (hogares, total) | `ine_epa_hogares.csv` | EPA430446 (Hogares. Total Nacional. Ambos sexos. Total. Total.) | miles de hogares (valor en miles, EPA) | trimestral (2002T1+) | nativo; serie PRINCIPAL de hogares | ln_, d_ln_, d4_ln_ | — | api | sí | EPA 0,4–1,0 % mayor que ECP 60131 en el solape (ver nota) | principal | 2002Q1 | 2026Q2 | 0 |
| `hogares_ecp` | INE ECP, tabla 60131 | `ine_hogares_60131.csv` | ECP355533 (Total Nacional. Total. Hogares en viviendas familiares.) | hogares (UNIDADES, no miles: 1.000 veces hogares_epa) | trimestral (2021T1+) | nativo; sin interpolación ni retropolación; ROBUSTEZ (antes 'hogares') | ln_, d_ln_, d4_ln_ | — | api | sí | — | robustez | 2021Q1 | 2026Q3 | 0 |
| `inmig_anual` | INE EMCR, tabla 69687 (ANUAL) | `ine_migraciones_total_anual.csv` | EM1765217 (Todas las edades. Total. Dato base. Inmigraciones procedentes del extranjero.) | personas (flujo anual) | anual (2021-2024) | anual asignado solo al primer trimestre del año (no trimestralizar) | ninguna (anual) | `inmig_anual_interp` (4) | api | sí | — | principal | 2021Q1 | 2024Q1 | 9 |
| `registradores_compraventas_anual` | Colegio de Registradores, OpenData (compraventas viviendas, nacional) | `pdf/registradores_opendata_anual.csv` | compraventas_viv_num (nivel nacional) | viviendas (año natural) | anual (2007-2025) | anual = T4 de la suma móvil de 4 trimestres; asignado a T4, sin interpolar | ln_, d_ln_, d4_ln_ | `registradores_compraventas_anual_interp` (19) | xls | sí | 0 frente al Anuario 2023-2025; ≤1,4 % frente a INE ETDP | principal | 2007Q4 | 2025Q4 | 54 |
| `registradores_extranj_pct` | Colegio de Registradores, Anuario ERI (% compras de extranjeros) | `pdf/registradores_eri_anuario.csv` | viv_pct_compras_extranjeros (nivel nacional) | % de compraventas | anual (2023-2025) | asignado a T4, sin interpolar | d_ (Δ1 pp) | `registradores_extranj_pct_interp` (3) | pdf | sí | 0 (nacionales + extranjeros = 100 %) | robustez | 2023Q4 | 2025Q4 | 6 |
| `notariado_cgn_extranj` | Consejo General del Notariado, CIEN (anexo XLSX) | `pdf/notariado_cgn_extranjeros_semestral.csv` | T1 op_viv_libre, categoría 'Extranjero', España | operaciones (vivienda libre) | semestral (2007S1+) | S1 -> T2, S2 -> T4; sin interpolar | ln_, d_ln_, d4_ln_ | `notariado_cgn_extranj_interp` (38) | xls | sí | 0 (suma interna); 9,4 % frente a MIVAU (concepto distinto) | principal | 2007Q2 | 2025Q4 | 37 |
| `serpavi_esp_constante` | MIVAU-SERPAVI (XLSX) → agregado propio | `pdf/serpavi_esp_agregado.csv` | SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_constante | €/m²/mes (alquiler, VC) | anual (2011-2024) | media ponderada de medianas de 17 CCAA con pesos fijos; asignado a T4; sin interpolar | ln_, d_ln_, d4_ln_ | `serpavi_esp_constante_interp` (14) | derivado | plausibilidad | 4,39 pp frente al IPVA nacional (no independiente) | robustez | 2011Q4 | 2024Q4 | 39 |
| `pob_extranj_ccaa_sum` | Derivada: suma de 17 CCAA de INE 77019 | `ine_ecp_ccaa_paises.csv` | ECP701-equivalente por CCAA (suma de panel_ccaa_q$pob_extranj) | personas (stock) | trimestral (derivada) | control: suma de 17 CCAA (sin Ceuta y Melilla) y pob_extranj nacional | ln_, d_ln_, d4_ln_ | `pob_extranj_ccaa_sum_interp` (69) | derivado | plausibilidad | ver nota | excluida | 2002Q1 | 2025Q1 | 0 |

Variables derivadas con la misma regla de transformación: `ln_`, `d_ln_`, `d4_ln_` para niveles positivos; `d_` para tipos y tasas.

**Notas de método y de contraste**
- `hogares_epa` (EPA430446, total de hogares, miles) es la serie **principal** de hogares desde 2002T1. En el solape con `hogares_ecp` (60131, 2021T1+; 22 trimestres) la EPA es entre **0,38 % y 1,01 %** mayor (media 0,78 %). No se enlazan ambas series.
- `pob_extranj_ccaa_sum` = suma de 17 CCAA de la tabla 77019 (sin Ceuta ni Melilla) de `pob_extranj` por trimestre (requiere las 17 CCAA). No coincide con `pob_extranj` nacional (ECP701): la diferencia relativa va de **-2,09 % a +1,30 %**. Parte es Ceuta y Melilla (suma menor, ~-0,3 %) y el resto es **error de interpolación**: las CCAA son stocks anuales a 1 de enero interpolados en logaritmos, mientras que la nacional es observada cada trimestre desde 2021. Por año (% suma CCAA / nacional − 1): 2002: -2,1 a -0,6; 2008: -0,8 a -0,2; 2014: -0,4 a +0,6; 2020: -0,8 a -0,3; 2021: -0,3 a +1,3; 2025: -0,3 a -0,3. Se conserva como control (`rol=excluida`), no entra en el modelo.
- `registradores_compraventas_anual` = compraventas de viviendas nacionales (suma móvil de 4 trimestres en T4 = año natural). Se usa **solo en T4** de cada año; el dato trimestral no se reconstruye (requiere valor semilla). No mezclar con `compraventas` (INE ETDP).
- `registradores_extranj_pct` (% de compras de extranjeros), `serpavi_esp_constante` (alquiler €/m²/mes, agregado propio) y `notariado_cgn_extranj` (operaciones de extranjeros, semestral: S1→T2, S2→T4) se asignan sin interpolar.
- `serpavi_esp_constante` usa 17 CCAA con pesos fijos (15 de régimen común + Ceuta y Melilla): **excluye Navarra y País Vasco** para que la composición no cambie. Un agregado de medianas no es una mediana nacional.
- `ipv15` (IPV base 2015) solo como robustez. `ipc_alquiler_yoy` está en el CSV como tasa (%) con `d_`.
- `deflactor` = PIB nominal NSA (CNTR6548) / PIB volumen encadenado NSA (CNTR6721), reescalado a media 2020 = 100. Deflactor implícito aproximado, no el oficial del INE.
- `renta_hog_real` = renta_hog / deflactor × 100 (M€ a precios de 2020).
- `tipo_hip_real` = tipo_hip − inflacion_deflactor (pp). La HICP del BCE (`ecb_hicp_es.csv`) termina en 2025-12 y no se usa.
- `visados`: faltan abril-junio de 2016 y de 2017 en el origen (MIVAU), así que 2016T2 y 2017T2 quedan NaN (regla de los 3 meses).
- `ocupados_sa` y `compraventas_sa`: STL(period=4, robust=True) sobre log, en el bloque contiguo más largo de datos; nivel = exp(log − estacional).
- `pob_total` (ECP320) y `pob_extranj` (ECP701) son semestrales hasta 2020 (1 ene y 1 jul) y trimestrales desde 2021; T2 y T4 de 1995-2020 se interpolan en logaritmos entre observaciones.
- `tipo_bce_interp`: True cuando el trimestre no tiene cambio de tipo (valor vigente desde un cambio anterior).
- `visados` y `terminadas` son proxies del Boletín MIVAU (viviendas libres iniciadas/terminadas), no visados CSCAE ni certificados de fin de obra.
- `hogares_ecp`: serie trimestral solo desde 2021T1 (60131). No se interpola ni se retropola.
- `inmig_anual`: flujo anual (EMCR, 69687) asignado al primer trimestre de cada año. No usar sin agregación anual.
- `inmig_q` (59011) **no se incluye**: no hay serie total y las nacionalidades están casi vacías (ver `docs/fuentes_fallidas.md`).
- `credito_stock`: fin de trimestre. `credito_nuevo`: suma de 3 meses (M€).

### Dummies y muestra

- `q1`…`q4`: dummies trimestrales. `muestra_base` = True desde 2008Q1 hasta el último trimestre con `ipv` no NaN.

## B. `data/processed/panel_ccaa_q.csv` (17 CCAA × trimestre, formato largo)

Códigos INE de CCAA: 01 Andalucía, 02 Aragón, 03 Asturias (Principado de), 04 Balears (Illes), 05 Canarias, 06 Cantabria, 07 Castilla y León, 08 Castilla-La Mancha, 09 Cataluña, 10 Comunitat Valenciana, 11 Extremadura, 12 Galicia, 13 Madrid (Comunidad de), 14 Murcia (Región de), 15 Navarra (Comunidad Foral de), 16 País Vasco, 17 La Rioja. **Ceuta (18) y Melilla (19) excluidas.** Nombres normalizados con `slug()` y `SLUG_ALIAS`.

| Variable | Fuente | Archivo raw | Código / serie | Unidad | Frecuencia | Agregación | Transformaciones | Bandera / cobertura | origen | validado | error_max | rol | Primer dato (mín. CCAA) | Último dato (máx. CCAA) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `ipv` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | IPV1392 (CCAA General) | índice | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | api | sí | — | principal | 2007Q1 | 2026Q2 |
| `ipv_nueva` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | '<CCAA>. Vivienda nueva. Índice.' | índice | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | api | sí | — | principal | 2007Q1 | 2026Q2 |
| `ipv_usada` | INE IPV, tabla 80270 | `ine_ipv_80270.csv` | '<CCAA>. Vivienda segunda mano. Índice.' | índice | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | api | sí | — | principal | 2007Q1 | 2026Q2 |
| `p_tasado` | MIVAU, tabla 35101000 | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_ccaa_<slug> | €/m2 | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | xls | sí | — | principal | 1995Q1 | 2026Q2 |
| `ocupados` | INE EPA, tabla 65302 | `ine_epa_ocupados_ccaa.csv` | '<CCAA>. Ambos sexos. Total. Ocupados. Valor absoluto.' | miles | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | api | sí | — | principal | 2002Q1 | 2026Q2 |
| `compraventas` | INE ETDP, tabla 6150 | `ine_etdp_compraventas.csv` | '<CCAA>. General. Compraventa. Número.' | número | mensual | suma de 3 meses | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | api | sí | — | principal | 2007Q1 | 2026Q2 |
| `trans_total` | MIVAU, tabla 34010110 | `mivau_transacciones_total.csv` | tx_total_ccaa_<slug> | transacciones | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | xls | sí | — | principal | 2004Q1 | 2026Q1 |
| `trans_extranjeros` | MIVAU, tabla 340101i0 (total) | `mivau_transacciones_extranjeros.csv` | tx_extranj_residentes_total_ccaa_<slug> | transacciones | trimestral | nativo | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | xls | sí | — | principal | 2007Q1 | 2026Q2 |
| `visados` | MIVAU, tabla 32100500 (PROXY) | `mivau_visados.csv` | viv_libres_iniciadas_ccaa_<slug> | viviendas | mensual | suma de 3 meses | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | xls | plausibilidad | proxy MIVAU | principal | 2008Q1 | 2026Q2 |
| `terminadas` | MIVAU, tabla 32101000 (PROXY) | `mivau_fin_obra.csv` | viv_libres_terminadas_ccaa_<slug> | viviendas | mensual | suma de 3 meses | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (16/17 CCAA) | xls | plausibilidad | proxy MIVAU; sin Extremadura | principal | 2008Q1 | 2026Q2 |
| `ipc_alquiler` | INE IPC, alquiler de vivienda | `ine_ipc_alquiler.csv` | '<CCAA>. Alquiler de vivienda. Índice.' | índice | mensual | media de 3 meses | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | api | sí | — | principal | 2002Q1 | 2026Q2 |
| `pob_total` | INE 77019 (ECP, CCAA x nacionalidad) | `ine_ecp_ccaa_paises.csv` | '<CCAA>. Todas las edades. Total. Total. Población.' | personas (stock 1 ene) | anual (T1 en el CSV) | stock a 1 de enero en T1; T2-T4 interpolados log-lineal entre observaciones | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | `pob_total_interp` (1173) (17/17 CCAA) | api | plausibilidad | stock 1 ene; T2-T4 interpolados (error de interpolación, ver nacional_q) | principal | 2002Q1 | 2025Q1 |
| `pob_extranj` | INE 77019 (ECP) | `ine_ecp_ccaa_paises.csv` | '<CCAA>. Todas las edades. Extranjera. Total.' | personas (stock 1 ene) | anual | como pob_total | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | `pob_extranj_interp` (1173) (17/17 CCAA) | api | plausibilidad | suma 17 CCAA frente a nacional: -2,1 % a +1,3 % (interpolación anual; ver nacional_q) | principal | 2002Q1 | 2025Q1 |
| `pob_espanola` | INE 77019 (ECP) | `ine_ecp_ccaa_paises.csv` | '<CCAA>. Todas las edades. Española. Total.' | personas (stock 1 ene) | anual | como pob_total | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | `pob_espanola_interp` (1173) (17/17 CCAA) | api | plausibilidad | stock 1 ene; T2-T4 interpolados | principal | 2002Q1 | 2025Q1 |
| `epa_pob_total` | INE EPA, tabla 65285 | `ine_epa_poblacion_ccaa.csv` | 'Ambos sexos. <CCAA>. Total. Valor absoluto.' | miles (todas las edades) | trimestral | nativo; incluye menores de 16 (no es población de 16+) | ln_, d_ln_, d4_ln_ (dentro de cada CCAA) | — (17/17 CCAA) | api | sí | — | robustez | 2002Q1 | 2026Q2 |

**Huecos de origen**: `terminadas` (MIVAU 32101000) no tiene Extremadura en el Boletín. `p_tasado` de Navarra tiene solo los trimestres en que MIVAU publica esa CCAA (ver `DUP_NOTES`).

**Población por CCAA (sustituye la ausencia previa)**: 77019 (tabla de población por CCAA y grupo de países) publica **un dato anual a 1 de enero**; el CSV lo etiqueta como T1. Se asigna a T1 y los trimestres T2-T4 entre dos observaciones se interpolan en logaritmos (`interp_loglin`), con bandera `pob_*_interp`. No se extrapola: 2025 T2-T4 quedan NaN. `epa_pob_total` (65285) es población EPA de **todas las edades** (incluye menores de 16); se usa como contraste, no como sustituto.

**Validación**: suma de las 17 CCAA de `pob_extranj` frente a ECP701 nacional: ver `pob_extranj_ccaa_sum` en nacional_q (diferencia por Ceuta y Melilla). `pob_total` de CCAA = suma de CCAA + Ceuta y Melilla = total nacional.

**Inmigración por CCAA**: la tabla 59013 (flujos CCAA × nacionalidad) no tiene total por CCAA y sus celdas están casi vacías; el flujo anual por CCAA no está en `data/raw`. Por eso `panel_ccaa_a` **no** incluye inmigración anual por CCAA.

## B2. `data/processed/panel_ccaa_nacionalidad.csv` (flujos 59013 y stocks 77019)

Formato largo con `tipo_registro`: **`flujo_59013`** (inmigración trimestral por CCAA × nacionalidad, tabla 59013, desde 2023T2; solo celdas con valor: 714 filas; el resto está vacío en origen y no se rellena) y **`stock_77019_1ene`** (stock de población por CCAA × grupo de países a 1 de enero, tabla 77019, 4896 filas; `trimestre` = `AAAAT1`, `pob_stock` en personas; grupos: Total, Española, Extranjera y grupos de países). Ceuta y Melilla excluidas. Las columnas `inmig_flujo` y `pob_stock` son disjuntas por tipo.

## B3. `data/processed/panel_ccaa_a.csv` (17 CCAA × año, para el IV shift-share de F3)

Clave: `codigo_ine_ccaa` × `anio`. Años 2002-2025 (rellenos NaN donde no hay dato; no se extrapola). Stocks a 1 de enero; agregados anuales solo con los 4 trimestres completos; logs y Δ1 año (`d_ln_`). Banderas `<var>_interp` = TRUE en agregados temporales de trimestres o semestres.

| Variable | Fuente | Archivo raw | Código / serie | Unidad | Transformación anual | origen | validado | error_max | rol |
|---|---|---|---|---|---|---|---|---|---|
| pob_total / pob_extranj / pob_espanola / pob_<grupo> | INE 77019 | ine_ecp_ccaa_paises.csv | '<CCAA>. Todas las edades. <grupo>. Total.' | personas (stock 1 ene) | nativo (sin interpolar) | api | sí (grupos suman exactamente a Extranjera; ver checks) | 0 (aditividad) | principal (totales); robustez (grupos) |
| ipv | INE IPV 80270 (de panel_ccaa_q) | ine_ipv_80270.csv | IPV1392 y CCAA | índice | media de 4 trimestres | api | sí | — | principal |
| p_tasado | MIVAU 35101000 (de panel_ccaa_q) | mivau_valor_tasado_nacional_ccaa_prov.csv | valor_tasado_libre_ccaa_<slug> | €/m² | media de 4 trimestres | xls | sí | — | principal |
| ocupados | INE EPA 65302 (de panel_ccaa_q) | ine_epa_ocupados_ccaa.csv | Ocupados (ambos sexos, total) | miles | media de 4 trimestres | api | sí | — | principal |
| compraventas | INE ETDP 6150 (de panel_ccaa_q) | ine_etdp_compraventas.csv | Compraventas número | número | suma de 4 trimestres | api | sí | — | principal |
| serpavi_vc_mediana | MIVAU-SERPAVI (XLSX) | pdf/serpavi_ccaa.csv | alquiler_m2 mediana VC por CCAA | €/m²/mes | nativo anual | xls | plausibilidad | 6,43 pp frente al IPVA València (no independiente) | principal |
| notariado_cgn_extranj | Consejo General del Notariado (CIEN) | pdf/notariado_cgn_extranjeros_semestral.csv | T2 op_viv_libre_extranjeros, 'Extranjero', por CCAA | operaciones | suma S1+S2 (solo si ambos existen) | xls | sí | 0 (suma interna) | principal |
| registradores_extranj_pct | Colegio de Registradores, Anuario ERI | pdf/registradores_eri_anuario.csv | viv_pct_compras_extranjeros_serie8a (CCAA) | % | nativo anual (última edición por año) | pdf | sí | 0 (nacionales + extranjeros = 100 %) | robustez |

- Logs: `ln_<var>` para niveles positivos; diferencias anuales `d_ln_<var>` (Δ1 año, dentro de cada CCAA). `d_registradores_extranj_pct` = Δ1 año en pp.
- **Inmigración anual por CCAA**: no disponible en `data/raw` (ver nota B). No se incluye.
- `pob_ue28_sin_espana` (2002-2020) y `pob_ue27_sin_espana` (2021+) cambian de definición en 2020-2021 (salida del Reino Unido): no enlazar. Ver `pob_europa_no_ue28` / `pob_europa_no_ue27` por la misma razón.

## C. `data/processed/valencia.csv` (formato largo: territorio × periodo × variable)

Columnas: `territorio`, `periodo` (`2008Q1` trimestral; `2019` anual), `frecuencia`, `variable`, `valor`, `origen`, `rol`, `validado`, `interp` (bandera equivalente a `<var>_interp`: TRUE si el valor fue asignado desde frecuencia menor).

**Correcciones de esta versión**: (1) el fichero `ine_vut_valencia_municipio.csv` es ahora el **municipio** de València (2024-08 = 7.976 viviendas; el revisor describía una versión anterior con la provincia). `ine_vut_valencia_provincia.csv` es la **provincia** (2024-08 = 17.853, igual que la provincia en `ine_vut_nacional_ccaa_prov.csv`). La versión anterior de `valencia.csv` tenía en 'València (municipio)' las cifras de la provincia (p. ej. 0,92 % en 2020T3 frente a 1,64 % del municipio): esas filas se han corregido. (2) `ipva` (anual) se guarda como `periodo=AAAA`, sin asignar a T1. (3) Notariado municipal: **solo 'Total general'** de València (no se suman nacionalidades: 4T2022 no es aditiva).

| Variable | Territorio | Archivo raw | Código / serie | Unidad | Frecuencia | Transformación | origen | validado | error_max | rol | Primer | Último | Nº |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `p_tasado` | València (municipio) | `mivau_valor_tasado_municipios.csv` | valor_tasado_mun_valencia | €/m2 | trimestral | nativo | xls | sí | — | principal | 2005Q1 | 2026Q2 | 86 |
| `p_tasado` | Provincia de València | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_provincia_valencia_valencia | €/m2 | trimestral | nativo | xls | sí | — | principal | 1995Q1 | 2026Q2 | 126 |
| `p_tasado` | Comunitat Valenciana | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_ccaa_comunidad_valenciana | €/m2 | trimestral | nativo | xls | sí | — | principal | 1995Q1 | 2026Q2 | 126 |
| `p_tasado` | España | `mivau_valor_tasado_nacional_ccaa_prov.csv` | valor_tasado_libre_nacional | €/m2 | trimestral | nativo | xls | sí | — | principal | 1995Q1 | 2026Q2 | 126 |
| `trans_total` | València (municipio) | `mivau_transacciones_municipios.csv` | tx_municipio_valencia | transacciones | trimestral | nativo | xls | sí | — | principal | 2004Q1 | 2026Q1 | 89 |
| `trans_total` | Comunitat Valenciana | `mivau_transacciones_total.csv` | tx_total_ccaa_comunitat_valenciana | transacciones | trimestral | nativo | xls | sí | — | principal | 2004Q1 | 2026Q1 | 89 |
| `trans_total` | España | `mivau_transacciones_total.csv` | tx_total_nacional | transacciones | trimestral | nativo | xls | sí | — | principal | 2004Q1 | 2026Q1 | 89 |
| `trans_extranjeros` | Comunitat Valenciana | `mivau_transacciones_extranjeros.csv` | tx_extranj_residentes_total_ccaa_comunitat_valenciana | transacciones | trimestral | nativo | xls | sí | — | principal | 2007Q1 | 2026Q2 | 78 |
| `trans_extranjeros` | España | `mivau_transacciones_extranjeros.csv` | tx_extranj_residentes_total_nacional | transacciones | trimestral | nativo | xls | sí | — | principal | 2007Q1 | 2026Q2 | 78 |
| `ipv` | Comunitat Valenciana | `ine_ipv_80270.csv` | IPV1392 (Comunitat Valenciana. General. Índice.) | índice | trimestral | nativo | api | sí | — | principal | 2007Q1 | 2026Q2 | 78 |
| `ipv` | España | `ine_ipv_80270.csv` | IPV1209 (Nacional. General. Índice.) | índice | trimestral | nativo | api | sí | — | principal | 2007Q1 | 2026Q2 | 78 |
| `ipva` | València (municipio) | `ine_ipva_municipal.csv` | IPVA8471 (Valencia. Índice. Total.) | índice | anual | nativo anual (sin asignar a trimestre) | api | sí | — | principal | 2011 | 2024 | 14 |
| `vut_viviendas_turisticas` | València (municipio) | `ine_vut_valencia_municipio.csv` | ine_vut_valencia_viviendas_turisticas | viviendas | semestral (asignado a T1/T3) | asignado desde semestral (feb->T1, ago->T3) | api | plausibilidad | — | robustez | 2020Q3 | 2026Q2 | 13 |
| `vut_plazas` | València (municipio) | `ine_vut_valencia_municipio.csv` | ine_vut_valencia_plazas | plazas | semestral (asignado a T1/T3) | asignado desde semestral (feb->T1, ago->T3) | api | plausibilidad | — | robustez | 2020Q3 | 2026Q2 | 13 |
| `vut_plazas_por_vivienda` | València (municipio) | `ine_vut_valencia_municipio.csv` | ine_vut_valencia_plazas_por_vivienda | plazas/vivienda | semestral (asignado a T1/T3) | asignado desde semestral (feb->T1, ago->T3) | api | plausibilidad | — | robustez | 2020Q3 | 2026Q2 | 13 |
| `vut_pct_sobre_total` | València (municipio) | `ine_vut_valencia_municipio.csv` | ine_vut_valencia_pct_viv_turisticas_sobre_total | % | semestral (asignado a T1/T3) | asignado desde semestral (feb->T1, ago->T3) | api | plausibilidad | — | robustez | 2020Q3 | 2026Q2 | 13 |
| `vut_viviendas_turisticas` | Provincia de València | `ine_vut_valencia_provincia.csv` | ine_vut_valencia_valencia_viviendas_turisticas | viviendas | semestral (asignado a T1/T3) | asignado desde semestral (feb->T1, ago->T3) | api | plausibilidad | — | robustez | 2020Q3 | 2026Q2 | 13 |
| `vut_plazas` | Provincia de València | `ine_vut_valencia_provincia.csv` | ine_vut_valencia_valencia_plazas | plazas | semestral (asignado a T1/T3) | asignado desde semestral (feb->T1, ago->T3) | api | plausibilidad | — | robustez | 2020Q3 | 2026Q2 | 13 |
| `vut_plazas_por_vivienda` | Provincia de València | `ine_vut_valencia_provincia.csv` | ine_vut_valencia_valencia_plazas_por_vivienda | plazas/vivienda | semestral (asignado a T1/T3) | asignado desde semestral (feb->T1, ago->T3) | api | plausibilidad | — | robustez | 2020Q3 | 2026Q2 | 13 |
| `vut_pct_sobre_total` | Provincia de València | `ine_vut_valencia_provincia.csv` | ine_vut_valencia_valencia_pct_viv_turisticas_sobre_total | % | semestral (asignado a T1/T3) | asignado desde semestral (feb->T1, ago->T3) | api | plausibilidad | — | robustez | 2020Q3 | 2026Q2 | 13 |
| `pob_total` | València (municipio) | `ine_padron_valencia.csv` | DPOP21796 (València. Total. Total habitantes.) | personas | anual (1 ene) | nativo | api | sí | — | principal | 1996 | 2025 | 29 |
| `pob_espanola` | València (municipio) | `ine_padron_vlc_nacionalidad.csv` | vlc_46250\|Ambos sexos\|Española | personas | anual (1 ene) | nativo | xls | sí | — | principal | 1998 | 2022 | 25 |
| `pob_extranjera` | València (municipio) | `ine_padron_vlc_nacionalidad.csv` | vlc_46250\|Ambos sexos\|Extranjera | personas | anual (1 ene) | nativo | xls | sí | — | principal | 1998 | 2022 | 25 |
| `pob_vlc_america` | València (municipio) | `ine_padron_vlc_nacionalidad.csv` | vlc_46250\|Ambos sexos\|Total América | personas | anual (1 ene) | nativo | xls | sí | — | robustez | 1998 | 2022 | 25 |
| `pob_vlc_asia` | València (municipio) | `ine_padron_vlc_nacionalidad.csv` | vlc_46250\|Ambos sexos\|Total Asia | personas | anual (1 ene) | nativo | xls | sí | — | robustez | 1998 | 2022 | 25 |
| `pob_vlc_europa` | València (municipio) | `ine_padron_vlc_nacionalidad.csv` | vlc_46250\|Ambos sexos\|Total Europa | personas | anual (1 ene) | nativo | xls | sí | — | robustez | 1998 | 2022 | 25 |
| `pob_vlc_africa` | València (municipio) | `ine_padron_vlc_nacionalidad.csv` | vlc_46250\|Ambos sexos\|Total África | personas | anual (1 ene) | nativo | xls | sí | — | robustez | 1998 | 2022 | 25 |
| `pob_vlc_alemania` | València (municipio) | `ine_padron_vlc_nacionalidad.csv` | vlc_46250\|Ambos sexos\|Alemania | personas | anual (1 ene) | nativo | xls | sí | — | robustez | 1998 | 2022 | 25 |
| `pob_vlc_reino_unido` | València (municipio) | `ine_padron_vlc_nacionalidad.csv` | vlc_46250\|Ambos sexos\|Reino Unido | personas | anual (1 ene) | nativo | xls | sí | — | robustez | 1998 | 2022 | 25 |
| `pob_extranjera_gva` | València (municipio) | `gva_padron_extranjeros_municipio.csv` | padron_pob_extranjera_mun_46250 | personas | anual (1 ene) | nativo | api | sí | 0 personas frente al padrón INE nacionalidad (18 años) | robustez | 2005 | 2022 | 18 |
| `serpavi_vc_mediana` | València (municipio) | `serpavi_municipios_46.csv` | SERPAVI_MUN_46250_VC_alquiler_m2_mediana | €/m²/mes | anual | nativo | xls | plausibilidad | 6,43 pp frente al IPVA València 2019 (no independiente: ambos AEAT) | principal | 2011 | 2024 | 14 |
| `serpavi_vc_dist_agg` | València (municipio) | `serpavi_valencia_distritos.csv` | SERPAVI_DIST_*_VC_alquiler_m2_mediana (ponderado por n_contratos VC) | €/m²/mes | anual | derivado: media de medianas de distritos ponderada por nº contratos VC (no es una mediana) | derivado | plausibilidad | — | robustez | 2011 | 2024 | 14 |
| `notariado_viv_extranj` | València (municipio) | `notariado_cv_municipios_anual.csv` | Valencia / Total general | viviendas | anual (edición 4T del año) | nativo | pdf | plausibilidad | 0 (completitud 19/19 municipios; ciudad <= provincia) | robustez | 2021 | 2025 | 5 |
| `notariado_viv_esp_prov` | Provincia de València | `notariado_cv_prov_trimestral.csv` | viv_vendidas_esp (Valencia) | viviendas | trimestral | nativo | pdf | sí | 0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463) | principal | 2018Q1 | 2025Q4 | 32 |
| `notariado_viv_ext_prov` | Provincia de València | `notariado_cv_prov_trimestral.csv` | viv_vendidas_ext (Valencia) | viviendas | trimestral | nativo | pdf | sí | 0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463) | principal | 2018Q1 | 2025Q4 | 32 |
| `notariado_cuantia_esp_prov` | Provincia de València | `notariado_cv_prov_trimestral.csv` | cuantia_media_esp (Valencia) | € | trimestral | nativo | pdf | sí | 0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463) | principal | 2018Q1 | 2025Q4 | 32 |
| `notariado_cuantia_ext_prov` | Provincia de València | `notariado_cv_prov_trimestral.csv` | cuantia_media_ext (Valencia) | € | trimestral | nativo | pdf | sí | 0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463) | principal | 2018Q1 | 2025Q4 | 32 |
| `vut_stock_gva` | València (municipio) | `gva_vut_municipio.csv` | vut_stock_mun_46250 | viviendas (stock) | trimestral (fin de trimestre) | stock mensual: valor de fin de trimestre | api | sí | 0 (reconstrucción independiente por altas-bajas, CV y 46250) | robustez | 2010Q1 | 2024Q4 | 60 |
| `vut_stock_gva` | Provincia de València | `gva_vut_municipio.csv` | vut_stock_prov_46 | viviendas (stock) | trimestral (fin de trimestre) | stock mensual: valor de fin de trimestre | api | sí | 0 (reconstrucción independiente por altas-bajas, CV y 46250) | principal | 2010Q1 | 2024Q4 | 60 |
| `vut_stock_gva` | Comunitat Valenciana | `gva_vut_municipio.csv` | vut_stock_cv | viviendas (stock) | trimestral (fin de trimestre) | stock mensual: valor de fin de trimestre | api | sí | 0 (reconstrucción independiente por altas-bajas, CV y 46250) | principal | 2010Q1 | 2024Q4 | 60 |

Notas por variable (valencia.csv):
- `vut_viviendas_turisticas` (València (municipio)): estadística experimental INE (tabla 39366 por la URL del fichero); semestral Feb/Ago -> T1/T3, sin interpolar; no comparable en niveles con el registro GVA.
- `vut_plazas` (València (municipio)): estadística experimental INE (tabla 39366 por la URL del fichero); semestral Feb/Ago -> T1/T3, sin interpolar; no comparable en niveles con el registro GVA.
- `vut_plazas_por_vivienda` (València (municipio)): estadística experimental INE (tabla 39366 por la URL del fichero); semestral Feb/Ago -> T1/T3, sin interpolar; no comparable en niveles con el registro GVA.
- `vut_pct_sobre_total` (València (municipio)): estadística experimental INE (tabla 39366 por la URL del fichero); semestral Feb/Ago -> T1/T3, sin interpolar; no comparable en niveles con el registro GVA.
- `pob_espanola` (València (municipio)): PC-Axis INE (padrón continuo, tabla 33946); 1998-2022 (2023-2025 no publicado por nacionalidad a nivel municipal).
- `pob_extranjera` (València (municipio)): PC-Axis INE (padrón continuo, tabla 33946); 1998-2022 (2023-2025 no publicado por nacionalidad a nivel municipal).
- `pob_vlc_america` (València (municipio)): grupo con cobertura completa 1998-2022 (25 años).
- `pob_vlc_asia` (València (municipio)): grupo con cobertura completa 1998-2022 (25 años).
- `pob_vlc_europa` (València (municipio)): grupo con cobertura completa 1998-2022 (25 años).
- `pob_vlc_africa` (València (municipio)): grupo con cobertura completa 1998-2022 (25 años).
- `pob_vlc_alemania` (València (municipio)): grupo con cobertura completa 1998-2022 (25 años).
- `pob_vlc_reino_unido` (València (municipio)): grupo con cobertura completa 1998-2022 (25 años).
- `pob_extranjera_gva` (València (municipio)): contraste de transcripción: IVE/GVA frente al padrón INE por nacionalidad. Ambos publican el mismo padrón municipal, así que NO es un contraste independiente; 2005-2022.
- `serpavi_vc_mediana` (València (municipio)): alquiler €/m²/mes, vivienda colectiva (VC); mediana municipal.
- `serpavi_vc_dist_agg` (València (municipio)): 19 distritos; unidades pequeñas (mínimo 10 viviendas): descriptivo.
- `notariado_viv_extranj` (València (municipio)): viviendas compradas por extranjeros (notarios). Solo 'Total general'. Corregido tras el fallo de 4T2022/4T2025 del revisor; pendiente de revisión independiente.
- `notariado_viv_esp_prov` (Provincia de València): edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU (ratio 1,06-1,20).
- `notariado_viv_ext_prov` (Provincia de València): edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU (ratio 1,06-1,20).
- `notariado_cuantia_esp_prov` (Provincia de València): edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU (ratio 1,06-1,20).
- `notariado_cuantia_ext_prov` (Provincia de València): edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU (ratio 1,06-1,20).
- `vut_stock_gva` (València (municipio)): registro administrativo (GVA, CKAN); stock = último mes del trimestre; 2010-2024; saltos regulatorios 2016-2019, 2021 y purga 2025-26; no encadenar con vut_foto (lista 2026). municipio València.
- `vut_stock_gva` (Provincia de València): registro administrativo (GVA, CKAN); stock = último mes del trimestre; 2010-2024; saltos regulatorios 2016-2019, 2021 y purga 2025-26; no encadenar con vut_foto (lista 2026). condicionado a los saltos regulatorios.

- **Notariado municipal (València ciudad)**: solo el 'Total general'. El PDF de municipios no publica total provincial, así que la comparación provincial usa el PDF trimestral de la provincia. Excluido: el desglose por nacionalidad (suma ≠ Total en 4T2022: 995 de error, comprobado).
- **Padrón**: `pob_total` (DPOP21796, 1996-2025) y `pob_espanola`/`pob_extranjera` (padrón por nacionalidad, 1998-2022). Diferencia máxima Total − (Española + Extranjera): 0. Diferencia máxima DPOP − Total por nacionalidad (1998-2022): 0.
- **Excluidos**: `vlc_precio_vivienda_libre.csv` (5 trimestres, fuente no indicada). `notariado_cv_actos_mensual` (actos sobre inmuebles, ROBUSTEZ del revisor, no exportado en esta versión).

## D. Datos de PDF (origen = pdf)

Ninguna serie procede de OCR. Todas las series `pdf` tienen texto nativo (pdfplumber). Validación según `*_validacion.csv` y `docs/revision_f1_fuentes.md`. Regla: datos de PDF no validados = solo robustez.

| Variable | Archivo raw | Validación | error_max | rol | Nota |
|---|---|---|---|---|---|
| `registradores_extranj_pct` (nacional_q) | `pdf/registradores_eri_anuario.csv` | sí | 0 (nacionales + extranjeros = 100 %) | robustez | serie anual 2023-2025; el CSV open data (`registradores_opendata_*`) es xls y no se duplica |
| `notariado_viv_extranj` (València (municipio)) | `notariado_cv_municipios_anual.csv` | plausibilidad | 0 (completitud 19/19 municipios; ciudad <= provincia) | robustez | viviendas compradas por extranjeros (notarios). Solo 'Total general'. Corregido tras el fallo de 4T2022/4T2025 del revisor; pendiente de revisión independiente |
| `notariado_viv_esp_prov` (Provincia de València) | `notariado_cv_prov_trimestral.csv` | sí | 0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463) | principal | edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU (ratio 1,06-1,20) |
| `notariado_viv_ext_prov` (Provincia de València) | `notariado_cv_prov_trimestral.csv` | sí | 0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463) | principal | edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU (ratio 1,06-1,20) |
| `notariado_cuantia_esp_prov` (Provincia de València) | `notariado_cv_prov_trimestral.csv` | sí | 0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463) | principal | edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU (ratio 1,06-1,20) |
| `notariado_cuantia_ext_prov` (Provincia de València) | `notariado_cv_prov_trimestral.csv` | sí | 0 frente a totales anuales del PDF; suma 3 prov. vs CGN: 7,5 % (1.463) | principal | edición 4T2025; la remisión del IUI del 4T2025 es 99,90 %; no mezclar niveles con MIVAU (ratio 1,06-1,20) |
| `registradores_extranj_pct` (panel_ccaa_a) | `pdf/registradores_eri_anuario.csv` | sí | 0 (suma 100 %; CCAA = España) | robustez | por CCAA, serie 8 años |

**Validación de los PDF (resumen del revisor, `docs/revision_f1_fuentes.md`)**:
- Notariado CV provincias trimestral (4T2025): sumas exactas frente a totales del PDF; 1.463 (7,5 %) frente al CGN; IUI 99,90 %. PRINCIPAL.
- Notariado municipios: el fallo de 4T2022 y 4T2025 (València ciudad, 2.171 y 2.538) queda corregido en el extractor (19/19 municipios en las 5 ediciones; `notariado_validacion.csv`: `municipios_completitud = sí`). Sin revisión independiente posterior: `plausibilidad`, ROBUSTEZ.
- Registradores ERI anuario: sumas CCAA = provincias = España = 0 de diferencia; % de extranjeros: nacionales + extranjeros = 100 %. La tabla de nacionalidades suma 97,96 % (defecto del origen, no se usa).

## E. Fuentes raw no utilizadas, excluidas o con duplicados

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
| `ine_migraciones_nacionalidad.csv (59011)` | No existe serie total: las nacionalidades solo tienen dato en pocas celdas por trimestre. No se usa. |
| `ine_ecp_56936.csv` | Población solo a nivel nacional por nacionalidad y edad (sin CCAA). Se usa solo para validar ECP701. |
| `ine_ecp_59585.csv` | Continuación 2025T2+ (ECP4961, ECP701). Se usa solo para validar ECP701. |
| `ine_ecp_ccaa_nacionalidad.csv` | Subconjunto de 77019 (Total, Española, Extranjera). Se usa solo para comprobar que coincide con ine_ecp_ccaa_paises.csv (0 de diferencia). |
| `ine_ipva_nacional_ccaa.csv, ine_vut_nacional_ccaa_prov.csv` | No especificados para este módulo. |
| `mivau_parque.csv, mivau_transacciones_residencia.csv` | No especificados. |
| `ine_ipv_25171.csv` | Solo IPV769 (base 2015) como robustez: incluido en nacional_q (ipv15). |
| `vlc_precio_vivienda_libre.csv` | Excluido de valencia.csv: 5 trimestres (2021T2-2022T2), fuente primaria no indicada. |
| `pdf/notariado_cv_actos_mensual.csv` | ROBUSTEZ según revisor (actos sobre inmuebles, no viviendas; revisiones de hasta 6 % entre ediciones). No exportado en esta versión. |
| `pdf/serpavi_valencia_secciones.csv, pdf/serpavi_provincias.csv` | Descriptivos (secciones: ruido muestral; provincias: no requeridas en esta versión). No exportados. |
| `pdf/registradores_eri_anuario.csv (compraventas CCAA/provincias/capital)` | Redundante con registradores_opendata_anual.csv (revisor). Capitales sin cuadre: ROBUSTEZ, no exportado. |
| `gva_vut_municipio.csv (vut_foto_*)` | Lista vigente 2026: no encadenable con el stock 2010-2024 (revisor §3.4). Excluida. |
| `ine_padron_valencia.csv (series ECP182xxx de CV)` | Series de la Comunitat Valenciana por nacionalidad (ECP): solo se usan DPOP21796 (València). |

## F. Cobertura de la muestra base 2008Q1+

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
| `ln_hogares_epa` | 74 | 2008Q1 | 2026Q2 |

- **N completo** (filas con las 9 variables no NaN, 2008Q1+): **74**; **último trimestre común**: **2026Q2**.
- `ln_hogares_epa` (principal) cubre desde 2002T1 y no restringe la muestra. Con `ln_hogares_ecp` (robustez, 2021T1+) la muestra común empezaría en 2021: ver `hogares_ecp`.
- Sin hogares (8 variables): N = **74**, último trimestre común = **2026Q2**.
- Los N son de las variables `ln_`; las diferencias `d_ln_` pierden 1 trimestre al inicio y `d4_ln_` pierde 4.

