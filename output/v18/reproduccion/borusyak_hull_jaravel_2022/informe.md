# Reproducción de Borusyak, Hull y Jaravel (2022), aplicación ADH, Tabla 4

**Rótulo: reproducción del estudio original con sus datos; no usa datos del proyecto.**

Capa C4 (exploratorio). Estudio metodológico: no hay efecto de vivienda; sirve para validar la herramienta de inferencia shift-share (agregación a nivel de shock y errores robustos a la exposición) que V18 usará en E3.

## Qué se reproduce

- Paquete: `data/bib/replicacion/borusyak_hull_jaravel_2022/ADH.zip` (GPL-3.0), leído en memoria. Stata no está disponible: se traduce `Table4_C1_C2_C4.do`, `Transformation.do` y `ssaggregate.ado` a Python (`src/v18/reproduccion/bhj_lib.py`, numpy/scipy).
- Resultado `y` (cambio del empleo manufacturero, % de la población en edad de trabajar), 1444 zonas-periodo (722 CZ, 1990-2000 y 2000-2007), 11 conjuntos de controles; sector SIC87dd (397 sectores, 794 shocks-periodo).
- Pasos: (1) IV convencional por zona (aw=wei, cluster por estado); (2) `ssaggregate` con residualización ponderada por controles, media por cuota x peso y sector «faltante» (addmissing); (3) IV a nivel de sector con el shock g, aw=s_n, cluster por sic3; (4) IC con la nula impuesta (bisección en -4..4).

## Decisiones de traducción

- Regresión de controles de ssaggregate: MCP con constante; `lstsq` de mínima norma (los residuos no cambian con colineales; Stata descarta las colineales).
- Conjunto 7: efectos fijos de sector (397 ficticias) y año en el nivel de sector; en el nivel de zona, 397 cuotas sectoriales como controles.
- Varianza por conglomerados: se comparan tres factores de muestra finita (G/(G-1); G/(G-1)·(N-1)/(N-K); ninguno). Principal: `ninguno`, elegido por coincidencia con la tabla publicada (no por significación). Resultado: sin factor reproduce 11/11 EE convencionales publicados al redondeo y 10/11 los de sector (conjunto 7: 0,204 frente a 0,205, dentro del 1 %); los otros dos factores están en tabla.csv.
- La prueba de Anderson-Rubin con nula impuesta traduce `ssiv_null_imposed.ado`: estadístico de score con residuo bajo la nula, varianza por conglomerados, chi2(1).
- No se reimplementa el EE de Adão, Kolesár y Morales (R, `TableC2_akm_se.R`); se cita la cifra del CSV del paquete (col. 5: 0,143) solo como referencia.

## Resultados (conjunto 1-11; coeficiente y error del IV a nivel de sector)

| Set | beta pub | beta Py | dif abs | dif rel | EE pub | EE Py | EE conv. pub | EE conv. Py | IC nulo pub | IC nulo Py | fs_f pub | fs_f Py | veredicto beta / EE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | -0.596 | -0.596 | -0.0004 | +0.06% | 0.114 | 0.114 | 0.099 | 0.099 | [-1.059, -0.395] | [-1.059, -0.395] | 185.6 | 185.6 | coincide / coincide |
| 2 | -0.489 | -0.489 | +0.0004 | -0.08% | 0.100 | 0.100 | 0.086 | 0.086 | [-0.832, -0.309] | [-0.832, -0.309] | 166.7 | 166.7 | coincide / coincide |
| 3 | -0.267 | -0.267 | +0.0003 | -0.12% | 0.099 | 0.099 | 0.086 | 0.086 | [-0.568, -0.028] | [-0.568, -0.028] | 123.6 | 123.6 | coincide / coincide |
| 4 | -0.314 | -0.314 | +0.0001 | -0.05% | 0.107 | 0.107 | 0.097 | 0.097 | [-0.637, -0.018] | [-0.637, -0.018] | 272.3 | 272.3 | coincide / coincide |
| 5 | -0.310 | -0.310 | +0.0000 | -0.01% | 0.134 | 0.134 | 0.104 | 0.104 | [-0.705, -0.002] | [-0.706, -0.002] | 64.6 | 64.6 | coincide / coincide |
| 6 | -0.290 | -0.290 | -0.0004 | +0.14% | 0.129 | 0.129 | 0.101 | 0.101 | [-0.699, 0.002] | [-0.699, 0.002] | 63.3 | 63.3 | coincide / coincide |
| 7 | -0.432 | -0.432 | -0.0003 | +0.07% | 0.205 | 0.204 | 0.193 | 0.193 | [-1.207, 0.122] | [-1.207, 0.122] | 27.6 | 27.9 | coincide / coincide |
| 8 | -0.200 | -0.200 | -0.0002 | +0.11% | 0.093 | 0.093 | 0.080 | 0.080 | [-0.500, -0.011] | [-0.500, -0.011] | 118.9 | 118.9 | coincide / coincide |
| 9 | -0.293 | -0.293 | -0.0002 | +0.08% | 0.125 | 0.125 | 0.099 | 0.099 | [-0.681, -0.019] | [-0.681, -0.019] | 53.3 | 53.3 | coincide / coincide |
| 10 | -0.241 | -0.241 | -0.0001 | +0.04% | 0.115 | 0.115 | 0.096 | 0.096 | [-0.604, -0.006] | [-0.604, -0.005] | 65.9 | 65.9 | coincide / coincide |
| 11 | -0.232 | -0.232 | +0.0002 | -0.07% | 0.122 | 0.122 | 0.103 | 0.103 | [-0.614, 0.033] | [-0.614, 0.033] | 56.6 | 56.6 | coincide / coincide |

## Comparación con lo publicado

- Fuente numérica: `ADH/Results/Table4_C1_C2_C4.csv` del paquete (y1..y11). El artículo (ficha, p. 33 del PDF, Tabla 4) da -0,310 (0,134) para la columna 5 y -0,293 (0,125) para la columna 6 del artículo; en el CSV esas cifras son los conjuntos 5 y 9. La numeración del CSV (11 conjuntos, incluye los de la Tabla C4) no coincide con las columnas del artículo; la identificación se hace por cifra (verificación a nivel de CSV, no por lectura de la tabla del PDF).
- Conjunto 5: beta Py -0.3100 frente a -0,310 (dif. abs. +0.0000); EE 0.1345 frente a 0,134 (dif. rel. +0.37%).
- Conjunto 9: beta Py -0.2932 frente a -0,293; EE 0.1246 frente a 0,125 (dif. rel. -0.36%).
- Coeficientes que coinciden: 11/11; errores: 11/11. Máx. |dif| beta 0.0004; máx. |dif| EE 0.0015.
- Agregación contra `industry_level_ext.dta` del paquete: {'n_comun': 796, 'n_py': 796, 'n_pub': 796, 'max_abs_dif_s_n': 2.969227086424553e-10, 'max_abs_dif_y1': 1.144846004663691e-07, 'max_abs_dif_x1': 1.5065505554190395e-07, 'max_abs_dif_y5': 9.256613964225835e-08, 'max_abs_dif_x5': 7.670600976616981e-08, 'max_abs_dif_y7': 2.784244734765906e-08, 'max_abs_dif_x7': 3.1116376364437315e-08, 'max_abs_dif_y9': 1.1537176725084919e-07, 'max_abs_dif_x9': 7.37367435998948e-08}.
- Comparación de inferencia: el error robusto a la exposición (cluster sic3) frente al convencional (cluster por estado) está en la columna `ratio_se_sector_sobre_conv_py` de tabla.csv; los IC con la nula impuesta son más anchos y asimétricos que el IC normal.

## Veredicto

**coincide.** Ver notas en resultado.json.

## Límites

- No es un resultado de vivienda ni de España; no se traslada ninguna cifra. Se valida el procedimiento.
- No se redistribuyen datos del paquete: solo coeficientes y estadísticos agregados.
- Solo el resultado `y`; los otros tres (desempleo, inactividad, salarios) y las tablas C2-C5 no se reproducen aquí.
- Pesos de Rotemberg y prueba de sobreidentificación a nivel de shock (mencionados en la ficha) no se reproducen en esta entrega.
