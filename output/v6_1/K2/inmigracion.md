# K2 · Inmigración: análisis de especificación «una dimensión cada vez» (v6.1)

Fecha del dato: 2026-10-11. Capa **C4** (exploratorio, asociación; nada causal). Script: `src/v6_1/k2_inmigracion.py` (SEED 20261010, un hilo, sin red).
medida_precio: valor tasado MIVAU por defecto; las demás se declaran en cada fila. Alquiler: stock (IPC, SERPAVI); los contratos nuevos (fianzas) no entran (N≈15 en entrenamiento). 181 especificaciones registradas en `registro.csv`; Holm y BH dentro de cada bloque en `registro_holm.csv`.

## Datos y supuestos
- Muestra: las 41 provincias de entrenamiento de v6 (output/v6/M0/paneles) y, para los datos de v2, las 38 que coinciden con el entrenamiento de v2 (2002-2023). Las 11 provincias selladas de v6 no se usan, así que **no se reproduce exactamente la muestra de 49 provincias de v2** (BI publicado: alquiler 3,06 [1,14; 4,98], compra −1,04 [−6,08; 4,00], F 14,4).
- CCAA y nacional son series publicadas (v1) que agregan todas las provincias; se usan solo descriptivamente. No hay dato municipal de extranjeros en data/processed: en municipio se une la variable provincial (pseudo-replicación; cluster provincia).
- Unidades: % de variación (o de nivel) de la medida por +1 pp del regresor; en €/mes y €/m² con el alquiler medio SERPAVI (413 €/mes) y el precio medio tasado (1257 €/m²) del panel. IC95 con t(G−1), errores agrupados por provincia (por CCAA con IPV).
- Notariado: solo hay panel de la Comunitat Valenciana (3 provincias) en data/processed, sin panel provincial: no entra. IPV del INE es de CCAA.
- La probabilidad de inclusión (PIP) es una aproximación con BIC sobre datos con EF; reproduce la de v6/M2 (núcleo) pero no es idéntica (g-prior).

## A. Camino acumulado: de la base de v2 (BI) a la especificación de v6 (M2)
Cada fila cambia una dimensión respecto de la anterior; «anterior» es el coeficiente del paso previo estimado en la misma muestra (salvo cuando cambia el periodo).

| paso | mercado | medida | periodo | N | coef_ic95 | p | p_holm | anterior | cambio | F1 |
|---|---|---|---|---|---|---|---|---|---|---|
| P0 | alquiler | IPC alquiler (stock) | 2009-2021 | 494 | 2,66 [0,27; 5,05] | 0,030 | 1,000 | n/d | n/d | 3,5 |
| P0 | compra | valor tasado MIVAU | 2009-2021 | 484 | 0,09 [-5,69; 5,87] | 0,975 | 1,000 | n/d | n/d | 6,7 |
| P1 | alquiler | IPC alquiler (stock) | 2009-2021 | 494 | 0,76 [0,10; 1,43] | 0,026 | 1,000 | 2,66 | -1,90 | n/d |
| P1 | compra | valor tasado MIVAU | 2009-2021 | 484 | 4,58 [2,60; 6,57] | 0,000 | 0,005 | 0,09 | 4,49 | n/d |
| P2 | alquiler | IPC alquiler (stock) | 2009-2021 | 494 | 0,34 [-0,10; 0,78] | 0,126 | 1,000 | 0,76 | -0,43 | n/d |
| P2 | compra | valor tasado MIVAU | 2009-2021 | 484 | 1,54 [0,58; 2,49] | 0,002 | 0,263 | 4,58 | -3,04 | n/d |
| P3 | alquiler | IPC alquiler (stock) | 2009-2021 | 494 | 0,40 [-0,12; 0,91] | 0,130 | 1,000 | 0,34 | 0,06 | n/d |
| P3 | compra | valor tasado MIVAU | 2009-2021 | 484 | 1,94 [0,70; 3,17] | 0,003 | 0,324 | 1,54 | 0,40 | n/d |
| P4 | alquiler | IPC alquiler (stock) | 2009-2021 | 494 | 0,69 [-0,08; 1,46] | 0,076 | 1,000 | 0,40 | 0,29 | n/d |
| P4 | compra | valor tasado MIVAU | 2009-2021 | 484 | 3,89 [2,02; 5,75] | 0,000 | 0,019 | 1,94 | 1,95 | n/d |
| P5 | alquiler | IPC alquiler (stock) | 2016-2023 | 304 | 0,94 [0,27; 1,61] | 0,007 | 0,723 | 0,69 | 0,25 | n/d |
| P5 | compra | valor tasado MIVAU | 2016-2023 | 304 | 3,36 [1,20; 5,52] | 0,003 | 0,345 | 3,88 | -0,52 | n/d |
| P6 | alquiler | SERPAVI VC (stock) | 2016-2023 | 282 | 2,62 [1,51; 3,72] | 0,000 | 0,004 | 1,14 | 1,47 | n/d |
| P6 | compra | valor tasado MIVAU | 2016-2023 | 304 | 3,36 [1,20; 5,52] | 0,003 | 0,345 | 3,36 | 0,00 | n/d |
| P7 | alquiler | SERPAVI VC (stock) | 2016-2023 | 282 | 2,62 [1,51; 3,72] | 0,000 | 0,004 | 2,62 | 0,00 | n/d |
| P7 | compra | valor tasado MIVAU | 2016-2023 | 304 | 3,36 [1,20; 5,52] | 0,003 | 0,345 | 3,36 | 0,00 | n/d |
| P8 | alquiler | SERPAVI VC (stock) | 2016-2023 | 306 | 0,30 [-1,06; 1,66] | 0,657 | 1,000 | 2,62 | -2,31 | n/d |
| P8 | compra | valor tasado MIVAU | 2016-2023 | 328 | -2,23 [-4,67; 0,20] | 0,071 | 1,000 | 3,15 | -5,39 | n/d |
| P9 | alquiler | SERPAVI VC (stock) | 2016-2023 | 282 | 0,18 [-1,48; 1,83] | 0,828 | 1,000 | -0,30 | 0,48 | n/d |
| P9 | compra | valor tasado MIVAU | 2016-2023 | 304 | -1,40 [-4,45; 1,64] | 0,356 | 1,000 | -1,88 | 0,48 | n/d |
| P10 | alquiler | SERPAVI VC (stock) | 2016-2024 | 282 | 0,18 [-1,48; 1,83] | 0,828 | 1,000 | 0,18 | 0,00 | n/d |
| P10 | compra | valor tasado MIVAU | 2016-2024 | 342 | -1,31 [-4,31; 1,69] | 0,383 | 1,000 | -1,40 | 0,10 | n/d |

## B. Una dimensión cada vez desde la base MCO (EF provincia y año, flujo, IPC / valor tasado real, 2009-2021)
«base_misma_muestra» es la base estimada en las filas válidas para ambas especificaciones.

| dimension | paso | mercado | medida | nivel | periodo | N | coef_ic95 | p | p_holm | base_misma_muestra | cambio |
|---|---|---|---|---|---|---|---|---|---|---|---|
| definicion | def_dstock | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 0,34 [-0,10; 0,78] | 0,126 | 1,000 | 0,76 | -0,43 |
| definicion | def_dstock | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 1,54 [0,58; 2,49] | 0,002 | 0,263 | 4,58 | -3,04 |
| definicion | def_dcuota | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 0,40 [-0,12; 0,91] | 0,130 | 1,000 | 0,76 | -0,37 |
| definicion | def_dcuota | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 1,94 [0,70; 3,17] | 0,003 | 0,324 | 4,58 | -2,64 |
| definicion | def_cuota_t1 | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | -0,06 [-0,22; 0,11] | 0,491 | 1,000 | 0,76 | -0,82 |
| definicion | def_cuota_t1 | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | -1,02 [-1,56; -0,48] | 0,000 | 0,055 | 4,58 | -5,60 |
| periodo | periodo_2009_2014 | alquiler | IPC alquiler (stock) | provincia | 2009-2014 | 228 | -0,16 [-1,96; 1,64] | 0,856 | 1,000 | -0,16 | 0,00 |
| periodo | periodo_2009_2014 | compra | valor tasado MIVAU | provincia | 2009-2014 | 218 | -0,46 [-7,63; 6,70] | 0,896 | 1,000 | -0,46 | 0,00 |
| periodo | periodo_2015_2021 | alquiler | IPC alquiler (stock) | provincia | 2015-2021 | 266 | 0,65 [-0,11; 1,42] | 0,089 | 1,000 | 0,65 | 0,00 |
| periodo | periodo_2015_2021 | compra | valor tasado MIVAU | provincia | 2015-2021 | 266 | 1,92 [-0,65; 4,48] | 0,138 | 1,000 | 1,92 | 0,00 |
| periodo | periodo_2009_2019 | alquiler | IPC alquiler (stock) | provincia | 2009-2019 | 418 | 0,80 [0,10; 1,49] | 0,026 | 1,000 | 0,80 | 0,00 |
| periodo | periodo_2009_2019 | compra | valor tasado MIVAU | provincia | 2009-2019 | 408 | 4,63 [2,48; 6,79] | 0,000 | 0,013 | 4,63 | 0,00 |
| metodo | metodo_pooled | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 0,54 [0,27; 0,81] | 0,000 | 0,033 | 0,76 | -0,23 |
| metodo | metodo_pooled | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 2,35 [1,49; 3,21] | 0,000 | 0,000 | 4,58 | -2,23 |
| metodo | metodo_unidad | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 1,42 [0,89; 1,94] | 0,000 | 0,000 | 0,76 | 0,65 |
| metodo | metodo_unidad | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 6,59 [5,06; 8,12] | 0,000 | 0,000 | 4,58 | 2,01 |
| metodo | metodo_anio | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 0,21 [-0,09; 0,51] | 0,159 | 1,000 | 0,76 | -0,55 |
| metodo | metodo_anio | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 0,90 [0,10; 1,71] | 0,029 | 1,000 | 4,58 | -3,68 |
| metodo | metodo_dobles_tend | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 0,44 [-0,38; 1,27] | 0,285 | 1,000 | 0,76 | -0,32 |
| metodo | metodo_dobles_tend | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 1,05 [-1,47; 3,56] | 0,404 | 1,000 | 4,58 | -3,53 |
| metodo | metodo_2sls | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 2,66 [0,27; 5,05] | 0,030 | 1,000 | 0,76 | 1,90 |
| metodo | metodo_2sls | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 0,09 [-5,69; 5,87] | 0,975 | 1,000 | 4,58 | -4,49 |
| colinealidad con poblacion | metodo_2sls_pob | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 2,69 [0,31; 5,08] | 0,028 | 1,000 | 0,76 | 1,93 |
| colinealidad con poblacion | metodo_2sls_pob | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 0,66 [-5,49; 6,81] | 0,829 | 1,000 | 4,58 | -3,92 |
| colinealidad con poblacion | mco_pob | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 0,73 [0,07; 1,39] | 0,030 | 1,000 | 0,76 | -0,03 |
| colinealidad con poblacion | mco_pob | compra | valor tasado MIVAU | provincia | 2009-2021 | 484 | 4,36 [2,36; 6,35] | 0,000 | 0,010 | 4,58 | -0,23 |
| medida alquiler | alq_serpavi | alquiler | SERPAVI VC (stock) | provincia | 2009-2021 | 350 | 3,59 [2,33; 4,85] | 0,000 | 0,000 | 0,97 | 2,62 |
| medida alquiler | medida_alq_IPC_muestra_comun | alquiler | IPC alquiler (stock) | provincia | 2012-2021 | 350 | 0,97 [0,14; 1,79] | 0,023 | 1,000 | n/d | n/d |
| medida alquiler | medida_alq_SERPAVI_muestra_comun | alquiler | SERPAVI VC (stock) | provincia | 2012-2021 | 350 | 3,59 [2,33; 4,85] | 0,000 | 0,000 | n/d | n/d |
| medida precio | medida_precio_tasado_real | compra | valor tasado MIVAU (real) | provincia | 2016-2021 | 210 | 2,39 [-0,36; 5,14] | 0,087 | 1,000 | n/d | n/d |
| medida precio | medida_precio_tasado_nominal | compra | valor tasado MIVAU (nominal) | provincia | 2016-2021 | 210 | 2,39 [-0,36; 5,14] | 0,087 | 1,000 | n/d | n/d |
| medida precio | medida_precio_registradores | compra | Registradores (m2) | provincia | 2016-2021 | 210 | 0,85 [-2,65; 4,35] | 0,626 | 1,000 | n/d | n/d |
| medida precio | medida_precio_ipv_ine | compra | IPV INE (CCAA asignado a la provincia) | provincia | 2016-2021 | 210 | 0,68 [-0,39; 1,74] | 0,185 | 1,000 | n/d | n/d |
| nivel | nivel_provincia_ref_dstock | alquiler | IPC alquiler (stock) | provincia | 2009-2021 | 494 | 0,34 [-0,10; 0,78] | 0,126 | 1,000 | n/d | n/d |
| nivel | nivel_provincia_ref_dstock | compra | valor tasado MIVAU (nominal) | provincia | 2009-2021 | 484 | 1,54 [0,58; 2,49] | 0,002 | 0,263 | n/d | n/d |
| nivel | nivel_CCAA | alquiler | IPC alquiler (stock) | CCAA | 2009-2021 | 221 | 0,69 [0,06; 1,32] | 0,035 | 1,000 | n/d | n/d |
| nivel | nivel_CCAA | compra | valor tasado MIVAU (nominal) | CCAA | 2009-2021 | 216 | 0,77 [-1,01; 2,56] | 0,373 | 1,000 | n/d | n/d |
| nivel | nivel_CCAA_ipv | compra | IPV INE (CCAA) | CCAA | 2009-2021 | 221 | -0,04 [-1,25; 1,16] | 0,938 | 1,000 | n/d | n/d |
| nivel | nivel_CCAA_serpavi | alquiler | SERPAVI VC (stock) | CCAA | 2012-2021 | 150 | 1,47 [0,73; 2,22] | 0,001 | 0,098 | n/d | n/d |
| nivel | nivel_nacional_x_stock_y_alq | alquiler | IPC alquiler (stock) | nacional | 2004-2021 | 18 | 2,44 [1,97; 2,90] | 0,000 | 0,000 | n/d | n/d |
| nivel | nivel_nacional_x_stock_y_pre_nom | compra | valor tasado MIVAU (nominal) | nacional | 2004-2021 | 18 | 6,28 [1,08; 11,49] | 0,021 | 1,000 | n/d | n/d |
| nivel | nivel_nacional_x_stock_y_pre_ipv | compra | IPV INE | nacional | 2004-2021 | 14 | 1,97 [-4,11; 8,04] | 0,494 | 1,000 | n/d | n/d |
| nivel | nivel_municipio_2012_2021 | alquiler | SERPAVI VC (stock) | municipio (x provincial unida) | 2012-2021 | 13561 | 1,10 [0,48; 1,72] | 0,001 | 0,118 | n/d | n/d |
| nivel | nivel_municipio_2012_2021 | compra | valor tasado MIVAU municipal (nominal) | municipio (x provincial unida) | 2012-2021 | 1882 | 2,63 [0,19; 5,08] | 0,036 | 1,000 | n/d | n/d |
| nivel | nivel_municipio_2009_2021 | alquiler | SERPAVI VC (stock) | municipio (x provincial unida) | 2009-2021 | 13561 | 1,10 [0,48; 1,72] | 0,001 | 0,118 | n/d | n/d |
| nivel | nivel_municipio_2009_2021 | compra | valor tasado MIVAU municipal (nominal) | municipio (x provincial unida) | 2009-2021 | 2442 | 2,94 [0,86; 5,02] | 0,007 | 0,711 | n/d | n/d |

## C. Colinealidad con la población y con la demanda externa
| medida | valor |
|---|---|
| cuota (t-1) y ln poblacion (t-1), panel v6, conjunta | 0,14 |
| idem, entre provincias | 0,14 |
| idem, dentro de provincia (EF dobles) | 0,66 |
| VIF cuota y ln poblacion (EF dobles) | 1,79 |
| VIF cuota con el nucleo de M2 | 2,53 |
| VIF ln poblacion con el nucleo de M2 | 3,63 |
| flujo/poblacion (base v2) y ln poblacion, dentro | 0,10 |
| variacion del stock y ln poblacion, dentro | -0,10 |
| cuota y compras de extranjeros residentes (MIVAU), conjunta / entre / dentro | 0,88 / 0,90 / -0,05 |
| cuota y costa (entre, 38 provincias) | 0,49 |
| cuota y vivienda no principal 2021 (Censo, entre) | 0,10 |
| cuota y no residentes 2015-2016 (R1A, entre) | 0,67 |

## D. ¿La cuota capta provincias de demanda externa? Cuota (t-1) en niveles, EF dobles (v6)
`controles_base`: sin controles, con ln población o con el núcleo de M2. `externa`: costa×año, vivienda no principal 2021×año (Censo), compras de extranjeros residentes (MIVAU, t-1), no residentes 2015-2016 (R1A) y combinaciones. Islas: 0 provincias insulares en entrenamiento (07, 35 y 38 están selladas). Filas `pooled` (sin EF de provincia, EF de año) y `FD` (primeras diferencias) al final.

| medida_ | controles_base | externa | N | coef_ic95 | abs | p | p_holm |
|---|---|---|---|---|---|---|---|
| valor tasado MIVAU | sin_controles | sin_externa | 342 | 4,26 [2,11; 6,41] | 53,6 EUR/m2 | 0,000 | 0,034 |
| valor tasado MIVAU | sin_controles | costa_x_anio | 342 | 1,88 [-0,37; 4,13] | 23,6 EUR/m2 | 0,099 | 1,000 |
| valor tasado MIVAU | sin_controles | no_principal_x_anio | 342 | 3,54 [0,91; 6,17] | 44,5 EUR/m2 | 0,010 | 0,960 |
| valor tasado MIVAU | sin_controles | compras_ext_residentes | 342 | 4,15 [2,00; 6,29] | 52,1 EUR/m2 | 0,000 | 0,044 |
| valor tasado MIVAU | sin_controles | costa+no_principal+compras_ext | 342 | 1,60 [-0,79; 3,99] | 20,1 EUR/m2 | 0,183 | 1,000 |
| valor tasado MIVAU | sin_controles | no_residentes_1516_x_anio | 342 | 3,23 [0,89; 5,58] | 40,7 EUR/m2 | 0,008 | 0,808 |
| valor tasado MIVAU | con_poblacion | sin_externa | 342 | -1,76 [-4,70; 1,18] | -22,2 EUR/m2 | 0,232 | 1,000 |
| valor tasado MIVAU | con_poblacion | costa_x_anio | 342 | -1,99 [-4,90; 0,91] | -25,1 EUR/m2 | 0,173 | 1,000 |
| valor tasado MIVAU | con_poblacion | no_principal_x_anio | 342 | -1,89 [-4,89; 1,12] | -23,7 EUR/m2 | 0,211 | 1,000 |
| valor tasado MIVAU | con_poblacion | compras_ext_residentes | 342 | -1,60 [-4,46; 1,26] | -20,1 EUR/m2 | 0,265 | 1,000 |
| valor tasado MIVAU | con_poblacion | costa+no_principal+compras_ext | 342 | -1,96 [-4,97; 1,04] | -24,7 EUR/m2 | 0,193 | 1,000 |
| valor tasado MIVAU | con_poblacion | no_residentes_1516_x_anio | 342 | -1,59 [-4,59; 1,41] | -20,0 EUR/m2 | 0,290 | 1,000 |
| valor tasado MIVAU | con_nucleo | sin_externa | 342 | -1,31 [-4,31; 1,69] | -16,4 EUR/m2 | 0,383 | 1,000 |
| valor tasado MIVAU | con_nucleo | costa_x_anio | 342 | -1,45 [-4,28; 1,38] | -18,2 EUR/m2 | 0,307 | 1,000 |
| valor tasado MIVAU | con_nucleo | no_principal_x_anio | 342 | -1,41 [-4,50; 1,67] | -17,8 EUR/m2 | 0,359 | 1,000 |
| valor tasado MIVAU | con_nucleo | compras_ext_residentes | 342 | -1,18 [-4,09; 1,74] | -14,8 EUR/m2 | 0,418 | 1,000 |
| valor tasado MIVAU | con_nucleo | costa+no_principal+compras_ext | 342 | -1,42 [-4,37; 1,52] | -17,9 EUR/m2 | 0,334 | 1,000 |
| valor tasado MIVAU | con_nucleo | no_residentes_1516_x_anio | 342 | -1,04 [-4,18; 2,10] | -13,1 EUR/m2 | 0,506 | 1,000 |
| Registradores (m2) | sin_controles | sin_externa | 342 | 4,75 [2,33; 7,17] | 59,7 EUR/m2 | 0,000 | 0,039 |
| Registradores (m2) | sin_controles | costa_x_anio | 342 | 2,66 [-0,62; 5,94] | 33,5 EUR/m2 | 0,108 | 1,000 |
| Registradores (m2) | sin_controles | no_principal_x_anio | 342 | 3,60 [0,78; 6,41] | 45,2 EUR/m2 | 0,014 | 1,000 |
| Registradores (m2) | sin_controles | compras_ext_residentes | 342 | 4,55 [2,18; 6,92] | 57,2 EUR/m2 | 0,000 | 0,049 |
| Registradores (m2) | sin_controles | costa+no_principal+compras_ext | 342 | 2,12 [-0,94; 5,19] | 26,7 EUR/m2 | 0,169 | 1,000 |
| Registradores (m2) | sin_controles | no_residentes_1516_x_anio | 342 | 3,89 [1,27; 6,51] | 48,9 EUR/m2 | 0,005 | 0,486 |
| Registradores (m2) | con_poblacion | sin_externa | 342 | -1,39 [-4,02; 1,25] | -17,4 EUR/m2 | 0,293 | 1,000 |
| Registradores (m2) | con_poblacion | costa_x_anio | 342 | -1,58 [-4,38; 1,22] | -19,8 EUR/m2 | 0,261 | 1,000 |
| Registradores (m2) | con_poblacion | no_principal_x_anio | 342 | -1,73 [-4,43; 0,97] | -21,8 EUR/m2 | 0,202 | 1,000 |
| Registradores (m2) | con_poblacion | compras_ext_residentes | 342 | -0,86 [-3,37; 1,66] | -10,8 EUR/m2 | 0,494 | 1,000 |
| Registradores (m2) | con_poblacion | costa+no_principal+compras_ext | 342 | -1,42 [-4,29; 1,45] | -17,8 EUR/m2 | 0,323 | 1,000 |
| Registradores (m2) | con_poblacion | no_residentes_1516_x_anio | 342 | -1,42 [-4,21; 1,37] | -17,9 EUR/m2 | 0,308 | 1,000 |
| Registradores (m2) | con_nucleo | sin_externa | 342 | -1,16 [-3,61; 1,29] | -14,6 EUR/m2 | 0,342 | 1,000 |
| Registradores (m2) | con_nucleo | costa_x_anio | 342 | -1,36 [-3,83; 1,12] | -17,0 EUR/m2 | 0,274 | 1,000 |
| Registradores (m2) | con_nucleo | no_principal_x_anio | 342 | -1,56 [-4,16; 1,05] | -19,6 EUR/m2 | 0,235 | 1,000 |
| Registradores (m2) | con_nucleo | compras_ext_residentes | 342 | -0,70 [-3,07; 1,67] | -8,8 EUR/m2 | 0,551 | 1,000 |
| Registradores (m2) | con_nucleo | costa+no_principal+compras_ext | 342 | -1,21 [-3,91; 1,49] | -15,2 EUR/m2 | 0,369 | 1,000 |
| Registradores (m2) | con_nucleo | no_residentes_1516_x_anio | 342 | -0,98 [-3,55; 1,59] | -12,3 EUR/m2 | 0,444 | 1,000 |
| SERPAVI VC (stock) | sin_controles | sin_externa | 282 | 2,67 [1,31; 4,04] | 11,0 EUR/mes | 0,000 | 0,041 |
| SERPAVI VC (stock) | sin_controles | costa_x_anio | 282 | 1,55 [0,15; 2,95] | 6,4 EUR/mes | 0,031 | 1,000 |
| SERPAVI VC (stock) | sin_controles | no_principal_x_anio | 282 | 2,52 [1,05; 3,99] | 10,4 EUR/mes | 0,001 | 0,156 |
| SERPAVI VC (stock) | sin_controles | compras_ext_residentes | 282 | 2,63 [1,15; 4,10] | 10,8 EUR/mes | 0,001 | 0,110 |
| SERPAVI VC (stock) | sin_controles | costa+no_principal+compras_ext | 282 | 1,55 [0,05; 3,05] | 6,4 EUR/mes | 0,043 | 1,000 |
| SERPAVI VC (stock) | sin_controles | no_residentes_1516_x_anio | 282 | 2,32 [0,86; 3,79] | 9,6 EUR/mes | 0,003 | 0,310 |
| SERPAVI VC (stock) | con_poblacion | sin_externa | 282 | -0,30 [-1,74; 1,13] | -1,2 EUR/mes | 0,672 | 1,000 |
| SERPAVI VC (stock) | con_poblacion | costa_x_anio | 282 | -0,28 [-1,69; 1,13] | -1,2 EUR/mes | 0,690 | 1,000 |
| SERPAVI VC (stock) | con_poblacion | no_principal_x_anio | 282 | -0,36 [-1,88; 1,17] | -1,5 EUR/mes | 0,637 | 1,000 |
| SERPAVI VC (stock) | con_poblacion | compras_ext_residentes | 282 | -0,27 [-1,71; 1,18] | -1,1 EUR/mes | 0,709 | 1,000 |
| SERPAVI VC (stock) | con_poblacion | costa+no_principal+compras_ext | 282 | -0,27 [-1,72; 1,18] | -1,1 EUR/mes | 0,708 | 1,000 |
| SERPAVI VC (stock) | con_poblacion | no_residentes_1516_x_anio | 282 | -0,22 [-1,60; 1,17] | -0,9 EUR/mes | 0,753 | 1,000 |
| SERPAVI VC (stock) | con_nucleo | sin_externa | 282 | 0,18 [-1,48; 1,83] | 0,7 EUR/mes | 0,828 | 1,000 |
| SERPAVI VC (stock) | con_nucleo | costa_x_anio | 282 | 0,14 [-1,47; 1,75] | 0,6 EUR/mes | 0,861 | 1,000 |
| SERPAVI VC (stock) | con_nucleo | no_principal_x_anio | 282 | 0,24 [-1,46; 1,95] | 1,0 EUR/mes | 0,775 | 1,000 |
| SERPAVI VC (stock) | con_nucleo | compras_ext_residentes | 282 | 0,21 [-1,44; 1,86] | 0,9 EUR/mes | 0,798 | 1,000 |
| SERPAVI VC (stock) | con_nucleo | costa+no_principal+compras_ext | 282 | 0,30 [-1,30; 1,90] | 1,2 EUR/mes | 0,705 | 1,000 |
| SERPAVI VC (stock) | con_nucleo | no_residentes_1516_x_anio | 282 | 0,37 [-1,23; 1,97] | 1,5 EUR/mes | 0,639 | 1,000 |
| valor tasado MIVAU | pooled | sin_externa | 342 | 1,02 [-0,18; 2,22] | 12,8 EUR/m2 | 0,093 | 1,000 |
| valor tasado MIVAU | pooled | costa+no_principal | 342 | 1,26 [-0,19; 2,70] | 15,8 EUR/m2 | 0,086 | 1,000 |
| valor tasado MIVAU | pooled | costa+no_principal+compras_ext | 342 | 2,80 [0,79; 4,80] | 35,2 EUR/m2 | 0,008 | 0,753 |
| Registradores (m2) | pooled | sin_externa | 342 | 1,50 [-0,08; 3,07] | 18,8 EUR/m2 | 0,062 | 1,000 |
| Registradores (m2) | pooled | costa+no_principal | 342 | 1,49 [-0,15; 3,14] | 18,8 EUR/m2 | 0,073 | 1,000 |
| Registradores (m2) | pooled | costa+no_principal+compras_ext | 342 | 3,96 [1,41; 6,51] | 49,8 EUR/m2 | 0,003 | 0,345 |
| SERPAVI VC (stock) | pooled | sin_externa | 282 | 0,67 [-0,34; 1,69] | 2,8 EUR/mes | 0,186 | 1,000 |
| SERPAVI VC (stock) | pooled | costa+no_principal | 282 | 1,20 [-0,11; 2,51] | 4,9 EUR/mes | 0,072 | 1,000 |
| SERPAVI VC (stock) | pooled | costa+no_principal+compras_ext | 282 | 1,83 [0,06; 3,61] | 7,6 EUR/mes | 0,044 | 1,000 |
| valor tasado MIVAU | FD | sin_externa | 304 | -0,32 [-3,05; 2,40] | -4,1 EUR/m2 | 0,811 | 1,000 |
| valor tasado MIVAU | FD | tendencia_costa+tendencia_no_principal | 304 | 0,41 [-2,05; 2,87] | 5,1 EUR/m2 | 0,739 | 1,000 |
| valor tasado MIVAU | FD | + compras_ext (var.) | 304 | 0,41 [-2,03; 2,85] | 5,1 EUR/m2 | 0,736 | 1,000 |
| SERPAVI VC (stock) | FD | sin_externa | 246 | -0,65 [-1,75; 0,46] | -2,7 EUR/mes | 0,242 | 1,000 |
| SERPAVI VC (stock) | FD | tendencia_costa+tendencia_no_principal | 246 | -0,43 [-1,44; 0,57] | -1,8 EUR/mes | 0,388 | 1,000 |
| SERPAVI VC (stock) | FD | + compras_ext (var.) | 246 | -0,43 [-1,43; 0,58] | -1,8 EUR/mes | 0,396 | 1,000 |

## E. BMA aproximado (BIC)
| mercado | conjunto | PIP cuota (BIC) | media posterior %/pp | PIP poblacion | N | modelos |
|---|---|---|---|---|---|
| compra | nucleo_M2 | 0,827 | -1,34 | 1,00 | 342 | 256 |
| compra | nucleo+demanda_externa | 0,939 | -1,64 | 1,00 | 342 | 2048 |
| alquiler | nucleo_M2 | 0,058 | 0,00 | 1,00 | 282 | 256 |
| alquiler | nucleo+demanda_externa | 0,062 | 0,00 | 1,00 | 282 | 2048 |

## F. Qué dimensión mueve el resultado entre v1-v3 y v6
1. **Método** (2SLS frente a MCO): invierte el orden entre mercados (paso P1: cambio -1,90 en alquiler y 4,49 en compra).
2. **Población como control** (paso P8): cambia el signo en compra (3,15 a -2,23) y anula la asociación en alquiler.
3. **Medida de alquiler** (IPC frente a SERPAVI): multiplica el coeficiente en alquiler por 3,7 en la muestra común.
4. Definición (flujo, stock, cuota), periodo, nivel y fuente de datos (v2/v6, idénticas: r≈1) mueven la magnitud pero no son la causa del cambio de orden. Medida de precio en 2016-2021: valor tasado 2,39 [-0,36; 5,14], Registradores 0,85 [-2,65; 4,35], IPV 0,68 [-0,39; 1,74] (comparable, intervalos solapados).

## G. Conclusión única (C4)
Con los datos de entrenamiento (provincias de entrenamiento de v6; 38 con datos de v2) la asociación de la inmigración con el precio de compra y con el alquiler de stock **no tiene un signo ni un orden entre mercados estables**: cambia con el método, con la medida de alquiler y, sobre todo, con el control por población. (1) Método: la base de v2 (flujo/población, 2SLS shift-share, 2009-2021) da 2,66 [0,27; 5,05] %/pp en alquiler (IPC) y 0,09 [-5,69; 5,87] en valor tasado; con MCO y los mismos EF da 0,76 [0,10; 1,43] y 4,58 [2,60; 6,57]: el orden alquiler > compra de v2 corresponde al 2SLS y el orden compra > alquiler de v6 al MCO (ya presente en la columna MCO de v2). La primera etapa en estas provincias es débil (F = 3,5 frente a 14,4 en las 49 provincias de v2; las 11 provincias selladas de v6 no se usan). (2) Población: la cuota de extranjeros (t-1) y el ln de la población (t-1) se correlacionan 0,66 dentro de provincia (0,14 en conjunta); al añadir la población, el coeficiente sobre el valor tasado pasa de 3,15 a -2,23 %/pp (IC95 [-4,67; 0,20]) y el de SERPAVI de 2,62 a 0,30. (3) Medida de alquiler: en la muestra común 2012-2021 el coeficiente es 3,59 [2,33; 4,85] con SERPAVI y 0,97 [0,14; 1,79] con IPC. (4) Demanda externa: sin población, los controles costa×año, vivienda no principal×año y compras de extranjeros residentes (MIVAU) reducen el coeficiente de 4,26 a 1,60 %/pp (valor tasado) y de 2,67 a 1,55 (SERPAVI), compatible con que la cuota recoja en parte provincias de costa; con población (o con el núcleo de M2) el coeficiente apenas cambia (-1,31 a -1,42 en valor tasado; 0,18 a 0,30 en SERPAVI). Las tres provincias insulares están en la parte sellada de v6, así que las islas no se pueden contrastar. Con el BMA aproximado (BIC) la probabilidad de inclusión de la cuota es 0,83 en compra y 0,06 en alquiler (v6/M2: 0,77 y 0,06), pero la media posterior en compra es -1,34 %/pp: una inclusión alta no implica signo positivo. **Capa C4; veredicto «ANALIZADA, NO CONCLUYENTE»; asociación, sin lectura causal.**
