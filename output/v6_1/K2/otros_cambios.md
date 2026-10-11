# K2 · Otras conclusiones que cambiaron de signo o de mercado (v6.1)

Fecha del dato: 2026-10-11. C4 en todas las filas; «ANALIZADA, NO CONCLUYENTE»; asociación, sin lectura causal. Cadenas ligeras, una dimensión cada vez, paso anterior en la misma muestra. Unidad: % de la medida por +10 % (niveles) o +10 pp de crecimiento anual (diferencias) de la variable; turísticos: +10 % de viviendas turísticas (t-1). Muestra: provincias de entrenamiento de v6. Holm por bloque.

## Empleo

Empleo (ocupados). v1: DOLS con empleo +1,48 (nacional, precio real, output/informe.md); v2/BV: crecimiento de ocupados +0,044 en compra (output/v2/BV); v6/M1b: efectos fijos −1,23 % (p WCB 0,49) y v6/M2: PDS +4,16 % (output/v6/M1B, M2).

| paso | dimension | mercado | medida | nivel | periodo | N | coef_ic95 | p | p_holm | anterior |
|---|---|---|---|---|---|---|---|---|---|---|
| empleo-0 | base v2: variacion anual, 2004-2023 | alquiler | IPC alquiler (stock) | provincia | 2004-2023 | 760 | -0,15 [-0,48; 0,18] | 0,371 | 1,000 | n/d |
| empleo-0 | base v2: variacion anual, 2004-2023 | compra | valor tasado MIVAU (real) | provincia | 2004-2023 | 748 | 0,94 [0,21; 1,66] | 0,013 | 0,488 | n/d |
| empleo-1 | periodo: 2016-2023 | alquiler | IPC alquiler (stock) | provincia | 2016-2023 | 304 | -0,00 [-0,29; 0,28] | 0,972 | 1,000 | -0,15 |
| empleo-1 | periodo: 2016-2023 | compra | valor tasado MIVAU (real) | provincia | 2016-2023 | 304 | 0,41 [-0,19; 1,00] | 0,176 | 1,000 | 0,94 |
| empleo-2 | metodo: niveles ln con EF dobles (v6) | alquiler | IPC alquiler (stock) | provincia | 2016-2023 | 304 | 1,34 [0,40; 2,28] | 0,006 | 0,256 | -0,00 |
| empleo-2 | metodo: niveles ln con EF dobles (v6) | compra | valor tasado MIVAU | provincia | 2016-2023 | 304 | 3,65 [1,00; 6,31] | 0,008 | 0,331 | 0,41 |
| empleo-3 | medida de alquiler: IPC -> SERPAVI | alquiler | SERPAVI VC (stock) | provincia | 2016-2023 | 306 | 2,90 [1,53; 4,27] | 0,000 | 0,005 | 1,13 |
| empleo-3 | medida de alquiler: IPC -> SERPAVI | compra | valor tasado MIVAU | provincia | 2016-2023 | 328 | 3,80 [1,48; 6,13] | 0,002 | 0,082 | 3,80 |
| empleo-4 | controles: + nucleo de M2 | alquiler | SERPAVI VC (stock) | provincia | 2016-2023 | 282 | 0,24 [-0,98; 1,45] | 0,696 | 1,000 | 3,11 |
| empleo-4 | controles: + nucleo de M2 | compra | valor tasado MIVAU | provincia | 2016-2023 | 304 | -2,37 [-4,97; 0,23] | 0,072 | 1,000 | 4,25 |

## Renta

Renta (PIB por habitante). v6/M1b: +1,34 % (p 0,13); v6/M2: PIP compra 0,84 y alquiler 0,10; mediana del multiverso −0,05 % (output/v6/M2).

| paso | dimension | mercado | medida | nivel | periodo | N | coef_ic95 | p | p_holm | anterior |
|---|---|---|---|---|---|---|---|---|---|---|
| renta-0 | base v2: variacion anual, 2004-2023 | alquiler | IPC alquiler (stock) | provincia | 2004-2023 | 760 | -0,13 [-0,43; 0,17] | 0,389 | 1,000 | n/d |
| renta-0 | base v2: variacion anual, 2004-2023 | compra | valor tasado MIVAU (real) | provincia | 2004-2023 | 748 | 0,86 [-0,02; 1,73] | 0,054 | 1,000 | n/d |
| renta-1 | periodo: 2016-2023 | alquiler | IPC alquiler (stock) | provincia | 2016-2023 | 304 | -0,08 [-0,34; 0,18] | 0,561 | 1,000 | -0,13 |
| renta-1 | periodo: 2016-2023 | compra | valor tasado MIVAU (real) | provincia | 2016-2023 | 304 | 0,07 [-0,60; 0,75] | 0,829 | 1,000 | 0,86 |
| renta-2 | metodo: niveles ln con EF dobles (v6) | alquiler | IPC alquiler (stock) | provincia | 2016-2023 | 304 | -0,58 [-1,48; 0,31] | 0,193 | 1,000 | -0,08 |
| renta-2 | metodo: niveles ln con EF dobles (v6) | compra | valor tasado MIVAU | provincia | 2016-2023 | 304 | -1,89 [-4,60; 0,82] | 0,166 | 1,000 | 0,07 |
| renta-3 | medida de alquiler: IPC -> SERPAVI | alquiler | SERPAVI VC (stock) | provincia | 2016-2023 | 306 | -0,55 [-1,93; 0,83] | 0,429 | 1,000 | -0,58 |
| renta-3 | medida de alquiler: IPC -> SERPAVI | compra | valor tasado MIVAU | provincia | 2016-2023 | 328 | -2,06 [-4,66; 0,53] | 0,116 | 1,000 | -2,06 |
| renta-4 | controles: + nucleo de M2 | alquiler | SERPAVI VC (stock) | provincia | 2016-2023 | 282 | 0,34 [-0,46; 1,14] | 0,392 | 1,000 | -0,79 |
| renta-4 | controles: + nucleo de M2 | compra | valor tasado MIVAU | provincia | 2016-2023 | 304 | 1,05 [-0,43; 2,54] | 0,159 | 1,000 | -1,89 |

## Iniciadas

Iniciadas libres en alquiler. v6/M1a: −0,17 €/mes por 1.000 (2021-2023) y +2,21 (2016-2023); v6/M2: PIP en alquiler 0,97 (núcleo) y 0,09 (completo) (output/v6/M1A, M2).

| paso | dimension | mercado | medida | nivel | periodo | N | coef_ic95 | p | p_holm | anterior |
|---|---|---|---|---|---|---|---|---|---|---|
| iniciadas-0 | base v2: variacion anual, 2004-2023 | alquiler | IPC alquiler (stock) | provincia | 2004-2023 | 760 | -0,02 [-0,03; -0,01] | 0,002 | 0,067 | n/d |
| iniciadas-0 | base v2: variacion anual, 2004-2023 | compra | valor tasado MIVAU (real) | provincia | 2004-2023 | 748 | 0,03 [-0,01; 0,07] | 0,138 | 1,000 | n/d |
| iniciadas-1 | periodo: 2016-2023 | alquiler | IPC alquiler (stock) | provincia | 2016-2023 | 304 | -0,01 [-0,02; -0,00] | 0,020 | 0,752 | -0,02 |
| iniciadas-1 | periodo: 2016-2023 | compra | valor tasado MIVAU (real) | provincia | 2016-2023 | 304 | 0,00 [-0,07; 0,08] | 0,947 | 1,000 | 0,03 |
| iniciadas-2 | metodo: niveles ln con EF dobles (v6) | alquiler | IPC alquiler (stock) | provincia | 2016-2023 | 280 | 0,07 [0,01; 0,13] | 0,022 | 0,794 | -0,02 |
| iniciadas-2 | metodo: niveles ln con EF dobles (v6) | compra | valor tasado MIVAU | provincia | 2016-2023 | 280 | 0,18 [-0,08; 0,45] | 0,164 | 1,000 | -0,04 |
| iniciadas-3 | medida de alquiler: IPC -> SERPAVI | alquiler | SERPAVI VC (stock) | provincia | 2016-2023 | 282 | 0,21 [0,04; 0,38] | 0,016 | 0,601 | 0,07 |
| iniciadas-3 | medida de alquiler: IPC -> SERPAVI | compra | valor tasado MIVAU | provincia | 2016-2023 | 304 | 0,22 [-0,03; 0,47] | 0,081 | 1,000 | 0,22 |
| iniciadas-4 | controles: + nucleo de M2 | alquiler | SERPAVI VC (stock) | provincia | 2016-2023 | 282 | 0,08 [-0,02; 0,18] | 0,131 | 1,000 | 0,21 |
| iniciadas-4 | controles: + nucleo de M2 | compra | valor tasado MIVAU | provincia | 2016-2023 | 304 | 0,00 [-0,17; 0,18] | 0,962 | 1,000 | 0,22 |
| iniciadas-5 | periodo: 2021-2023 (ventana de M1a S0), sin controles | alquiler | SERPAVI VC (stock) | provincia | 2021-2023 | 107 | 0,06 [-0,08; 0,19] | 0,394 | 1,000 | 0,08 |
| iniciadas-5 | periodo: 2021-2023 (ventana de M1a S0), sin controles | compra | valor tasado MIVAU | provincia | 2021-2023 | 114 | 0,02 [-0,20; 0,24] | 0,881 | 1,000 | 0,00 |
| iniciadas-6 | controles: + turisticos (ln_vut, solo desde 2020) | alquiler | SERPAVI VC (stock) | provincia | 2021-2023 | 107 | 0,04 [-0,11; 0,19] | 0,606 | 1,000 | 0,06 |
| iniciadas-6 | controles: + turisticos (ln_vut, solo desde 2020) | compra | valor tasado MIVAU | provincia | 2021-2023 | 114 | -0,03 [-0,25; 0,20] | 0,825 | 1,000 | 0,02 |

## Turisticos

Turísticos (VUT). v3/C1: +0,0003 por 100 viviendas (sección, no concluyente); v3/GL: −0,0042 (Barcelona); v6/M1a: −1,58 €/mes por 1.000 (provincia, 2021-2023) (output/v3/C1, GL; v6/M1A).

| paso | dimension | mercado | medida | nivel | periodo | N | coef_ic95 | p | p_holm | anterior |
|---|---|---|---|---|---|---|---|---|---|---|
| turisticos-0 | base v6 (M1a S0): provincia, SERPAVI, 2021-2023 | alquiler | SERPAVI VC (stock) | provincia | 2021-2023 | 116 | -0,17 [-0,82; 0,48] | 0,596 | 1,000 | n/d |
| turisticos-0 | base v6 (M1a S0): provincia, SERPAVI, 2021-2023 | compra | valor tasado MIVAU | provincia | 2021-2023 | 123 | -0,69 [-1,56; 0,18] | 0,118 | 1,000 | n/d |
| turisticos-1 | medida de alquiler: SERPAVI -> IPC | alquiler | IPC alquiler (stock) | provincia | 2021-2023 | 116 | -0,02 [-0,37; 0,33] | 0,895 | 1,000 | -0,17 |
| turisticos-1 | medida de alquiler: SERPAVI -> IPC | compra | valor tasado MIVAU | provincia | 2021-2023 | 123 | -0,69 [-1,56; 0,18] | 0,118 | 1,000 | -0,69 |
| turisticos-2 | metodo: primeras diferencias | alquiler | SERPAVI VC (stock) | provincia | 2022-2023 | 77 | 0,40 [-0,15; 0,94] | 0,148 | 1,000 | -0,05 |
| turisticos-2 | metodo: primeras diferencias | compra | valor tasado MIVAU | provincia | 2022-2023 | 82 | -0,02 [-0,99; 0,94] | 0,962 | 1,000 | -0,44 |
| turisticos-3 | controles: + poblacion | alquiler | SERPAVI VC (stock) | provincia | 2022-2023 | 77 | 0,38 [-0,16; 0,91] | 0,162 | 1,000 | 0,40 |
| turisticos-3 | controles: + poblacion | compra | valor tasado MIVAU | provincia | 2022-2023 | 82 | -0,09 [-0,99; 0,81] | 0,845 | 1,000 | -0,02 |
| turisticos-4 | nivel: municipio | alquiler | SERPAVI VC (stock) | municipio (v2, 41 prov. de entrenamiento) | 2021-2023 | 4492 | -0,03 [-0,09; 0,03] | 0,357 | 1,000 | n/d |
| turisticos-4 | nivel: municipio | compra | valor tasado municipal | municipio (v2, 41 prov. de entrenamiento) | 2021-2023 | 600 | -0,07 [-0,30; 0,16] | 0,527 | 1,000 | n/d |

## BMA aproximado (BIC), núcleo de M2

| mercado | variable | PIP | media posterior |
|---|---|---|---|
| compra | l1_share_ext_pob | 0,83 | -1,34 |
| compra | l1_ln_pob | 1,00 | 226,31 |
| compra | l1_ln_pib_pc | 0,60 | 7,71 |
| compra | l1_paro_tasa | 0,20 | -0,05 |
| compra | l1_ln_ocupados_miles | 0,07 | -0,46 |
| compra | l1_ln_terminadas_libres | 0,60 | 0,73 |
| compra | l1_ln_iniciadas_libres | 0,06 | 0,01 |
| compra | l1_ln_hip_viv_num | 0,24 | -0,98 |
| alquiler | l1_share_ext_pob | 0,06 | 0,00 |
| alquiler | l1_ln_pob | 1,00 | 95,06 |
| alquiler | l1_ln_pib_pc | 0,15 | 0,54 |
| alquiler | l1_paro_tasa | 0,17 | -0,01 |
| alquiler | l1_ln_ocupados_miles | 0,15 | 0,71 |
| alquiler | l1_ln_terminadas_libres | 0,06 | -0,00 |
| alquiler | l1_ln_iniciadas_libres | 0,89 | 0,75 |
| alquiler | l1_ln_hip_viv_num | 0,93 | 3,17 |

## Lectura

- Los signos de empleo, renta e iniciadas cambian al pasar de diferencias a niveles con EF y al añadir el núcleo de controles (población incluida): ninguno es estable entre pasos con IC95 que excluya 0 en la especificación final.
- Turísticos: ningún paso tiene IC95 que excluya 0; el signo cambia entre medida de alquiler, método y nivel.
- El cambio de mercado (alquiler frente a compra) y de signo entre versiones coincide con cambios de medida (IPC, SERPAVI; valor tasado), de método y de controles, no con un resultado estable.
