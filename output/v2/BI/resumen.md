# BI · inmigración y vivienda (H3) · resumen

Muestra: 621 observaciones provincia-año (49 provincias, 2009-2021), idéntica para alquiler, compra y contraste. SEED 20261010. Todas las especificaciones en `registro.csv` (humo 2009-2015 en `smoke_*`).

**Lectura general: H3 queda EXPLORATORIO. Hay una asociación positiva y estable en el signo entre el instrumento de inmigración y el alquiler, de magnitud no identificada; el contraste alquiler>compra no es robusto.**

## Desviaciones/interpretaciones no fijadas en el pre-registro

Elecciones NO fijadas en el pre-registro (desviación/interpretación declarada): (i) 'flujo/población t-1' se lee como flujo del año t (INE EM) dividido por la población a 1 de enero del año t−1; la lectura alternativa flujo_{t-1}/pob_{t-2} se muestra aparte; (ii) momento del shock: el principal usa ΔS_t = S(1-ene t) − S(1-ene t-1), que cubre el año t-1 (desalineado con el flujo del año t); la versión alineada ΔS_{t+1} se muestra aparte y cambia el signo del contraste; (iii) el valor tasado se deflacta con el deflactor nacional (inocuo con FE de año); (iv) Europa = UE+resto de Europa (ruptura UE28/UE27 de 2021); cuotas y shock sobre las 49 provincias de entrenamiento. Si la versión desalineada se eligió antes o después de ver resultados no es auditable: se declara como grado de libertad.

## H3 (especificación pre-registrada)

| | coef. (2SLS) | EE cluster | IC95 t(48) | p WCB 2 colas | p WCB 1 cola | MCO |
|---|---|---|---|---|---|---|
| Δln IPC alquiler | 3.06 | 0.95 | [1.14; 4.98] | 0.001 | 0.001 | 0.96 (0.23) |
| Δln valor tasado real | -1.04 | 2.51 | [-6.08; 4.00] | 0.671 | 0.662 | 5.07 (0.71) |
| alquiler − compra | 4.10 | 2.20 | [-0.33; 8.52] | 0.051 | 0.029 | -4.11 (0.75) |

Unidades: % de variación anual por cada 1 p.p. de población. Conjunto AR del coef. de alquiler: [1.4; 6.0]. Correlación entre ecuaciones 0.49; el EE del contraste del sistema apilado (2.202) coincide con el de la regresión de la diferencia.

Intersección-unión (p WCB una cola): coef. alquiler>0 p=0.0010; contraste>0 p=0.0294; **p_IUT de H3 = 0.0294**, cota Holm-7 0.206 (la corrección final de la familia la aplica el orquestador).

**Nivel de evidencia de H3: EXPLORATORIO.** Componente alquiler>0 (no pre-registrado por separado, informativo): EXPLORATORIO (signo positivo estable con el instrumento completo, pero falla submuestras 2015-2021 p=0,073, controles GPSS de extranjeros 2002 p=0,115 y los placebos de resultado pasado rechazan también en precio: patrón transversal persistente; magnitud NO identificada); cota Holm-7 0.007. Compra: no informativa (IC [-6.1; 4.0], signo inestable). **CAUSAL descartado.**

## Diagnósticos de identificación (EXPLORATORIOS, con p WCB una cola; con F<10 el bootstrap no es fiable)

| especificación | resultado | coef. | EE | p cluster | p WCB 1c | F |
|---|---|---|---|---|---|---|
| principal | alq | 3.06 | 0.95 | 0.002 | 0.001 | 14.4 |
| principal | pre | -1.04 | 2.51 | 0.681 | 0.661 | 14.4 |
| principal | dif | 4.10 | 2.20 | 0.069 | 0.031 | 14.4 |
| gpss_extr02 | alq | 1.95 | 1.21 | 0.115 | 0.078 | 15.0 |
| gpss_extr02 | pre | 8.70 | 4.34 | 0.051 | 0.081 | 15.0 |
| gpss_extr02 | dif | -6.75 | 4.20 | 0.115 | 0.867 | 15.0 |
| gpss_ln_pob02 | alq | 3.17 | 1.31 | 0.019 | 0.006 | 9.0 |
| gpss_ln_pob02 | pre | -2.19 | 2.73 | 0.427 | 0.792 | 9.0 |
| gpss_ln_pob02 | dif | 5.36 | 2.60 | 0.045 | 0.009 | 9.0 |
| gpss_ln_p02 | alq | 3.11 | 1.07 | 0.005 | 0.003 | 9.9 |
| gpss_ln_p02 | pre | -0.97 | 2.80 | 0.730 | 0.643 | 9.9 |
| gpss_ln_p02 | dif | 4.08 | 2.39 | 0.094 | 0.045 | 9.9 |
| gpss_paro02 | alq | 3.70 | 1.03 | 0.001 | 0.000 | 13.1 |
| gpss_paro02 | pre | -0.33 | 3.20 | 0.919 | 0.545 | 13.1 |
| gpss_paro02 | dif | 4.03 | 2.80 | 0.157 | 0.079 | 13.1 |
| gpss_costa | alq | 2.94 | 0.84 | 0.001 | 0.001 | 18.8 |
| gpss_costa | pre | 0.35 | 2.36 | 0.882 | 0.449 | 18.8 |
| gpss_costa | dif | 2.59 | 2.11 | 0.228 | 0.112 | 18.8 |
| gpss_todas | alq | 4.61 | 3.12 | 0.146 | 0.042 | 4.6 |
| gpss_todas | pre | 9.93 | 10.14 | 0.332 | 0.108 | 4.6 |
| gpss_todas | dif | -5.32 | 8.78 | 0.547 | 0.772 | 4.6 |
| solo_Sudamerica | alq | 2.45 | 0.63 | 0.000 | 0.001 | 52.5 |
| solo_Sudamerica | pre | 2.98 | 1.34 | 0.031 | 0.012 | 52.5 |
| solo_Sudamerica | dif | -0.53 | 1.30 | 0.684 | 0.669 | 52.5 |
| sin_Sudamerica | alq | 4.34 | 2.66 | 0.109 | 0.018 | 1.7 |
| sin_Sudamerica | pre | -9.50 | 7.14 | 0.189 | 0.965 | 1.7 |
| sin_Sudamerica | dif | 13.84 | 7.77 | 0.081 | 0.005 | 1.7 |
| z_alineado_t+1 | alq | 2.37 | 0.59 | 0.000 | 0.000 | 29.9 |
| z_alineado_t+1 | pre | 4.46 | 1.64 | 0.009 | 0.002 | 29.9 |
| z_alineado_t+1 | dif | -2.09 | 1.52 | 0.175 | 0.924 | 29.9 |
| flujo_t-1 | alq | 0.80 | 0.57 | 0.164 | 0.089 | 9.7 |
| flujo_t-1 | pre | -6.05 | 3.29 | 0.072 | 0.984 | 9.7 |
| flujo_t-1 | dif | 6.86 | 3.16 | 0.035 | 0.005 | 9.7 |
| sub_2009-2014 | alq | 9.74 | 12.32 | 0.433 | 0.051 | 0.7 |
| sub_2009-2014 | pre | -45.65 | 56.55 | 0.423 | 0.963 | 0.7 |
| sub_2009-2014 | dif | 55.39 | 66.93 | 0.412 | 0.029 | 0.7 |
| sub_2015-2021 | alq | 2.50 | 1.36 | 0.073 | 0.059 | 7.6 |
| sub_2015-2021 | pre | -1.80 | 2.73 | 0.513 | 0.790 | 7.6 |
| sub_2015-2021 | dif | 4.29 | 2.85 | 0.139 | 0.030 | 7.6 |
| placebo_resultado_t-1 | alq | 4.09 | 1.15 | 0.001 | 0.000 | 22.4 |
| placebo_resultado_t-1 | pre | 5.81 | 2.68 | 0.035 | 0.011 | 22.4 |
| placebo_resultado_t-2 | alq | 3.67 | 0.85 | 0.000 | 0.000 | 22.4 |
| placebo_resultado_t-2 | pre | 10.10 | 2.69 | 0.000 | 0.000 | 22.4 |

Lectura:
- **Controles GPSS (características 2002 × año).** Al controlar por la cuota de extranjeros 2002 el coeficiente de alquiler baja a 1.95 (p cluster 0.115) y el contraste cambia de signo (-6.75); con las cinco características el F cae a 4.6 y el coeficiente es 4.61 (p 0.15). Las cuotas 2002 no están balanceadas: la cuota de Sudamérica correlaciona con ln población 2002 (r=0.61), ln precio 2002 (r=0.43) y extranjeros 2002 (r=0.36).
- **Placebo de alquiler pasado sobre x_t instrumentado**: coef. 4.09 (t−1, p 0.001) y 3.67 (t−2, p 0.000), del mismo tamaño que el principal: **el placebo rechaza**. El diseño no separa el flujo de t de dinámicas provinciales previas o de flujos pasados (shocks persistentes); el coeficiente no puede leerse como efecto del flujo del año t.
- **Solo Sudamérica** (68 % del peso de Rotemberg; F 52): alquiler 2.45, compra 2.98 (positivo y significativo) y contraste -0.53. **Sin Sudamérica** el instrumento es débil (F 1.7).
- **Contraste con instrumento alineado ΔS_{t+1}** (F 30): -2.09 (p WCB 1c 0.92): **el signo del contraste se invierte**; con 'flujo t−1' el contraste es 6.86. El contraste depende de elecciones de timing y de instrumento.
- **Subperiodos**: 2009-2014 el instrumento no tiene primera etapa (F 0.7, sin información); 2015-2021 coef. alquiler 2.50 (p cluster 0.073).

## Diagnósticos de shift-share previos

- Primera etapa: F cluster = 14.4 (moderado; F efectivo de Montiel Olea-Pflueger no implementado: con un instrumento y un regresor se reporta el F robusto, sin valores críticos). Con tendencias provinciales baja a 5.4.
- Pesos de Rotemberg (8 grupos): sin pesos negativos; Sudamérica 0.68 (F del grupo 52); los dos mayores suman 0.80. África y Europa: F por grupo < 2.
- Instrumento medio vs. características 2002: extranjeros r=0.56 (p=0.000), paro r=-0.34 (p=0.018), ln población r=-0.40 (p=0.004).
- **Pretendencias: NO informativas.** La ventana 2003-2007 (resultados sobre el instrumento medio posterior: alquiler p=0.93, precio p=0.53) coincide con el boom de llegadas a los mismos enclaves: no es un periodo pre-tratamiento. Con el instrumento de Sudamérica: alquiler p=0.11.
- Sobreidentificación (5 grupos): Hansen cluster alquiler p=0.29, precio p=0.12; Sargan homocedástico alquiler p=0.065, precio p=5.8e-06 (rechaza). El J robusto con 49 clusters tiene poca potencia.
- BHJ a nivel de shock (8 grupos × 13 años, t(7)): alquiler 3.99 (p=0.000); precio 2.90 (p=0.55). Con 8 shocks la potencia y la inferencia son pobres: no aporta evidencia de exogeneidad de los shocks.
- EE tipo AKM0 (aproximación, sin región de similitud de cuotas): alquiler EE 0.74 (p t(7) = 0.004) frente a 0.95.
- **Naturaleza del shock**: ΔS es la variación del stock de nacionales del grupo (incluye nacionalizaciones, p. ej. sudamericanos en 2010-2015), mientras que x es el flujo bruto de entradas: el shock no mide entradas.

## Stock vs flujo y timing (EXPLORATORIO)

| spec | resultado | regresor | coef. | EE | p cluster | F |
|---|---|---|---|---|---|---|
| tendencias_prov | y_alq | x | 3.90 | 1.66 | 0.023 | 5.4 |
| sin_covid | y_alq | x | 2.38 | 0.77 | 0.003 | 14.3 |
| stock_dcuota_extranj | y_alq | x_stock | 1.19 | 0.39 | 0.004 | 13.6 |
| flujo_t-1 | y_alq | x_l1 | 0.80 | 0.57 | 0.164 | 9.7 |
| x_t_y_x_t-1 | y_alq | x | 2.12 | 1.10 | 0.061 | 7.1 |
| x_t_y_x_t-1 | y_alq | x_l1 | 0.52 | 0.66 | 0.434 | 7.1 |
| z_alineado_stock_t+1 | y_alq | x | 2.37 | 0.59 | 0.000 | 29.9 |
| tendencias_prov | y_pre | x | -9.54 | 5.48 | 0.088 | 5.4 |
| sin_covid | y_pre | x | -0.92 | 2.59 | 0.724 | 14.3 |
| stock_dcuota_extranj | y_pre | x_stock | -0.40 | 0.98 | 0.683 | 13.6 |
| flujo_t-1 | y_pre | x_l1 | -6.05 | 3.29 | 0.072 | 9.7 |
| x_t_y_x_t-1 | y_pre | x | 13.29 | 3.07 | 0.000 | 7.1 |
| x_t_y_x_t-1 | y_pre | x_l1 | -7.85 | 2.49 | 0.003 | 7.1 |
| z_alineado_stock_t+1 | y_pre | x | 4.46 | 1.64 | 0.009 | 29.9 |

El coeficiente de alquiler es positivo en las variantes con el instrumento completo; con flujo t−1 y con x_t y x_{t−1} conjuntos pierde precisión. El coeficiente de compra cambia de signo entre variantes.

## Heterogeneidad (EXPLORATORIO)

- DML (cross-fitting 5 bloques de provincias × 3 repeticiones, EE cluster): PLR lasso 0.29 (p=0.059), PLR RF 0.48 (p=0.0000); PLIV lasso 2.05 (p=0.18), PLIV RF 1.42 (p=0.023). PLR sin FE de provincia.
- Causal forest (sin instrumento): coeficiente medio 0.43 [0.08; 0.79]; los coeficientes estimados son mayores con cuota extranjera 2002 y precio inicial altos y paro 2002 bajo (importancia mayor: cuota extranjera 2002 0.32). La IC del bosque no agrupa por provincia y subestima la incertidumbre.
- Interacciones IV paramétricas: ninguna significativa (p mínimo 0.35, Holm 1,00): el patrón del bosque no se confirma con instrumento.
- Presupuesto declarado 14 configuraciones, 10 usadas; hiperparámetros fijos.

## Magnitudes

- Coeficiente de alquiler 3.06 [1.1; 5.0] vs MCO 0.96, Saiz (2007, EE. UU.) ≈ 1 (aumento neto de población inmigrante, no flujo bruto) y v1 (F3, 17 CCAA) 0,44 (n.s.). Es unas 3 veces el MCO y Saiz y 7 veces v1, con F moderado y cuotas no balanceadas; la diferencia no está explicada. Entre variantes el coeficiente va de 0,8 a 5: **la magnitud no está identificada**; solo el signo positivo es estable.

## Fuera de muestra

Anual, orígenes 2013-2020 (8 × 49 provincias, bloques expansivos con embargo 1 año, misma muestra). RMSE AR(4) panel 0.0107; AR(4)+flujo observado en t 0.0094 (DM-HLN 1.43, p=0.20: sin mejora significativa); con flujo contemporáneo t+1 (NO es pronóstico) 0.0080 (p=0.06). El flujo del año t se publica a mitad de t+1: es un pseudo-pronóstico con pequeña anticipación. **ECM v1: no comparable** (solo existe trimestral, sin análogo anual en la misma muestra); se retira la comparación. No es posible añadir la inmigración al panel_ar4 trimestral (flujos hasta 2021-22).

## Lo que NO se puede afirmar

- Que la inmigración se asocie más con el alquiler que con la compra: p_IUT 0,029, cota Holm-7 0,21, IC95 del contraste incluye 0 y el signo se invierte con el instrumento alineado, con Sudamérica sola y con los controles GPSS.
- Que exista un efecto causal o un efecto local (LATE) del flujo: el placebo de alquiler pasado rechaza, las cuotas 2002 no están balanceadas, el F cae a 4,6 con controles GPSS y la ventana de pretendencias no es pre-tratamiento.
- Ninguna magnitud concreta (rango 0,8-5); ni comparación cuantitativa con Saiz (2007): unidades y definición (flujo bruto vs neto) distintas.
- Nada sobre el precio de compra (IC muy ancho, signo inestable).
- Nada sobre 2022 en adelante ni sobre las provincias selladas (H3 sin evaluación sellada).
- Heterogeneidad por costa, turismo, tamaño o precio inicial: solo aparece en métodos sin instrumento.
- Equilibrio general (salida de nativos, oferta) ni cantidades.
- Mejora predictiva con inmigración fuera de muestra (sin mejora significativa frente a AR(4)).
