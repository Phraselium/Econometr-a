# F5: panel de CCAA (P4) - resumen

Generado por `src/f5_panel.py` (semilla 20261009).

## Respuesta a P4

**Pregunta**: ¿difieren entre CCAA (y en la C. Valenciana) las asociaciones del precio de la vivienda con empleo y poblacion extranjera?

- **Respuesta**: *no se detecta heterogeneidad* de pendientes entre CCAA. Esto es ausencia de evidencia, **no evidencia de homogeneidad**: con N=17 y T=17 la potencia es minima (el p minimo de un contraste por aleatorizacion de una region es 1/17=0.059; el CCE individual tiene 7 gl por CCAA).
- Nivel de evidencia: **asociacion condicional y fragil** (panel observacional con FE de CCAA y anio / CCE). Sin identificacion causal en esta fase; para la lectura causal remite al IV de F3 (no se repite aqui).
- C. Valenciana: ninguna interaccion distinguible del resto (p wild de b1 y b2 en tabla 4a). La unica diferencia solida es **descriptiva** y depende de la medida de precio (tabla 4c): 2014Q1-2026Q2 el IPV de la CV crece menos que el de Espana pero su valor tasado mas; desde 2021Q1 crece mas con ambas.
- FE bidireccional (17 CCAA, 2009-2025): b1 (elasticidad al empleo) = -0.028 (EE cluster 0.104, p wild=0.812); b2 = 0.0011 (EE 0.0040; 0.11 %/pp; p cluster=0.777, DK bw2=0.913, wild=0.774). R2 within ajustado = -0.040: los regresores explican poco de las desviaciones regionales respecto del ciclo comun.
- **b2 depende del timing** (2009-2024, misma muestra): flujo t-1 0.09 %/pp (p wild 0.857); cuota a mitad de anio 1.18 %/pp (p wild 0.068); flujo contemporaneo 1.89 %/pp (p wild 0.010). Tras la correccion por busqueda (Holm sobre 15 p-valores de b2, incluidos los trimestrales con el mayor de p cluster y DK) el menor p ajustado es 0.151: ninguna alineacion es significativa tras la correccion; b2 queda **entre 0.1 y 1.9 %/pp segun la alineacion**. No se afirma b2 = 0.
- CCE-MG: b1=0.056 (0.101), b2=0.025 (0.014); CCE-P: b1=-0.053 (0.097), b2=0.022 (0.011).
- Poolability: F=3.38, p clasico=5.8e-11 (sobredimensionado), **p wild Webb=0.363**; F conjunto de las 12 interacciones regionales: p clasico=3e-07, p wild=0.107.
- Dependencia transversal: el CD sobre residuos de FE y CCE **no es interpretable** (Juodis y Reese 2022; seccion 3a) y no se usa como diagnostico.

## Discusion de signos y magnitudes

- **b2 frente a la literatura** (docs/literatura.md): Saiz (2007) encuentra ~+1 % en alquileres y valores por una entrada igual al 1 % de la poblacion, y Gonzalez y Ortega (2013) efectos positivos de la inmigracion sobre el precio en Espana. Un b2 ~ 0 (flujo t-1) discrepa; el flujo contemporaneo (~+1,9 %/pp) y la cuota a mitad de anio se acercan al orden de magnitud, pero con causalidad inversa posible. F3 (FE/2SLS, ver output/f3) da estimaciones tampoco distinguibles de 0; la comparacion directa exige expresar F5 en %/pp (hecho arriba).
- **b4 (terminadas por 1.000 hab., t-1) > 0** (0.0026, EE 0.0011, p wild 0.075) frente al signo negativo esperado de la oferta (Saiz 2010; Hilber y Vermeulen 2016; tabla de signos de literatura.md). No debe leerse como efecto de oferta: es compatible con simultaneidad/inercia (se termina mas donde los precios ya subian) y con dinamica omitida (AR(1) residual ~0,3); en CCE el signo se invierte y deja de ser significativo. Se deja como discrepancia abierta.
- **b1 y F2**: b1 es una elasticidad de corto plazo (-0.03 %/1 % de empleo), no comparable con la elasticidad de largo plazo de F2 (DOLS, 1,95 con EE HAC 0,48, evidencia mixta/inestable segun F2): F5 usa desviaciones regionales anuales respecto del ciclo comun (los efectos de anio absorben lo nacional) y probable atenuacion por el error muestral de la EPA regional en diferencias. Con valor tasado como dependiente b1 es mayor (tabla 1f), asi que b1 ~ 0 no es robusto a la medida de precio.
- **CIPS** (tabla 3b): no rechaza raiz unitaria en la primera diferencia de la cuota extranjera (CIPS* -1.53, p sim 0.75) ni de ln poblacion espanola (p sim 0.41). Puede ser falta de potencia con T=17, o persistencia migratoria; si d_share fuese casi I(1), la regresion de un y I(0) estaria desequilibrada y b2, b3 tenderian a 0 con inferencia no estandar. Es una limitacion de b2 y b3.

## 0. Datos y muestra

Panel anual `panel_ccaa_a`: dependiente d_ln_ipv (IPV media anual, base 2025). Muestra principal 17 CCAA x 17 anios (2009-2025; N=289, balanceado; `terminadas` de Extremadura ya incorporada en data/processed). **Timing de b2**: la poblacion es el stock a 1 de enero del anio t, de modo que d_share_t = cuota(1-1-t) - cuota(1-1-(t-1)) mide la entrada neta ocurrida durante el anio t-1, mientras el IPV es la media del anio t (b2 principal = flujo retardado un anio). Alternativas registradas (seccion 1g): cuota a mitad de anio t (media de 1-1-t y 1-1-t+1) y flujo del anio t (cuota(1-1-t+1) - cuota(1-1-t)); ambas necesitan la cuota de 1-1-2026, por lo que se comparan en 2009-2024. b2 se mide en puntos porcentuales de cuota (pob_extranj/pob_total); el coeficiente es Delta ln IPV por pp (x100 = %/pp). `term_l1` = terminadas por 1.000 hab. de t-1.

## 1a. FE bidireccional (CCAA + anio), muestra principal

N=289, 17 CCAA, T=17. EE cluster por CCAA (17 clusters), Driscoll-Kraay (Bartlett; con T=17 ancho 2-3, poco fiable) y p-valor del wild cluster bootstrap restringido (Webb, 9999 replicas, semilla 20261009) para H0: coef=0.

| variable                     |      coef |   EE_cluster |   p_cluster |   EE_DK_bw2 |   p_DK_bw2 |   EE_DK_bw3 |   p_DK_bw3 |   p_wild_Webb |
|:-----------------------------|----------:|-------------:|------------:|------------:|-----------:|------------:|-----------:|--------------:|
| b1 dln ocupados              | -0.02801  |     0.1037   |     0.7873  |   0.1105    |   0.8      |   0.09876   |  0.7769    |        0.8124 |
| b2 d(extr/total, pp)         |  0.001139 |     0.004022 |     0.7772  |   0.01038   |   0.9127   |   0.008971  |  0.899     |        0.774  |
| b3 dln pob espanola          |  2.17     |     1.021    |     0.03449 |   0.9154    |   0.01851  |   0.9002    |  0.01663   |        0.0784 |
| b4 terminadas/1000 hab (t-1) |  0.002645 |     0.001137 |     0.02076 |   0.0008153 |   0.001337 |   0.0007215 |  0.0003004 |        0.075  |


## 1b. FE + tendencias lineales por CCAA (en diferencias = deriva de crecimiento propia por CCAA)

|                              |      coef |   EE_cluster |   p_cluster |   EE_DK_bw2 |   p_DK_bw2 |
|:-----------------------------|----------:|-------------:|------------:|------------:|-----------:|
| b1 dln ocupados              | -0.003874 |     0.1034   |     0.9702  |    0.1169   |     0.9736 |
| b2 d(extr/total, pp)         | -0.007382 |     0.006936 |     0.2883  |    0.01739  |     0.6716 |
| b3 dln pob espanola          |  1.681    |     0.8631   |     0.05267 |    1.207    |     0.1649 |
| b4 terminadas/1000 hab (t-1) |  0.003289 |     0.001334 |     0.01436 |    0.001383 |     0.0182 |


## 1c. CCE-MG y CCE-pooled (Pesaran 2006)

Cada regresion se aumenta con constante y promedios transversales de y y de las 4 X (6 auxiliares por CCAA; 7 gl por unidad en MG: muy justo). EE no parametricos (varianza empirica de los b_i). Sin efectos de anio (los promedios los sustituyen).

| estimador   | var                          |      coef |       EE |       z |       p |
|:------------|:-----------------------------|----------:|---------:|--------:|--------:|
| CCE-MG      | b1 dln ocupados              |  0.05617  | 0.1007   |  0.5576 | 0.5771  |
| CCE-MG      | b2 d(extr/total, pp)         |  0.02515  | 0.01398  |  1.799  | 0.07202 |
| CCE-MG      | b3 dln pob espanola          |  0.4014   | 1.26     |  0.3185 | 0.7501  |
| CCE-MG      | b4 terminadas/1000 hab (t-1) | -0.001202 | 0.002481 | -0.4843 | 0.6282  |
| CCE-P       | b1 dln ocupados              | -0.05288  | 0.09695  | -0.5455 | 0.5854  |
| CCE-P       | b2 d(extr/total, pp)         |  0.02177  | 0.01061  |  2.051  | 0.04025 |
| CCE-P       | b3 dln pob espanola          |  1.991    | 1.388    |  1.434  | 0.1515  |
| CCE-P       | b4 terminadas/1000 hab (t-1) | -0.00115  | 0.002154 | -0.534  | 0.5933  |


## 1d. Comparacion de estimadores (misma muestra: 17 CCAA x 2009-2025)

|                              |   FE cluster |       EE |   FE+tend |   EE tend |    CCE-MG |    EE MG |    CCE-P |     EE P |
|:-----------------------------|-------------:|---------:|----------:|----------:|----------:|---------:|---------:|---------:|
| b1 dln ocupados              |    -0.02801  | 0.1037   | -0.003874 |  0.1034   |  0.05617  | 0.1007   | -0.05288 | 0.09695  |
| b2 d(extr/total, pp)         |     0.001139 | 0.004022 | -0.007382 |  0.006936 |  0.02515  | 0.01398  |  0.02177 | 0.01061  |
| b3 dln pob espanola          |     2.17     | 1.021    |  1.681    |  0.8631   |  0.4014   | 1.26     |  1.991   | 1.388    |
| b4 terminadas/1000 hab (t-1) |     0.002645 | 0.001137 |  0.003289 |  0.001334 | -0.001202 | 0.002481 | -0.00115 | 0.002154 |


## 1g. Timing de b2 (FE bidireccional, 2009-2024, misma muestra)

La cuota es un stock a 1 de enero; las tres alineaciones se comparan en la misma muestra. El flujo contemporaneo es el mas expuesto a causalidad inversa (precio -> llegadas en el mismo anio).

| alineacion de la cuota           |        b2 |   EE_cluster |   p_cluster |   p_wild_Webb |   b2 en %/pp |   N |
|:---------------------------------|----------:|-------------:|------------:|--------------:|-------------:|----:|
| flujo del anio t-1 (principal)   | 0.0008528 |     0.004686 |     0.8558  |        0.8565 |      0.08528 | 272 |
| cuota a mitad de anio t          | 0.01183   |     0.005626 |     0.03657 |        0.0675 |      1.183   | 272 |
| flujo del anio t (contemporaneo) | 0.01894   |     0.005871 |     0.00143 |        0.0101 |      1.894   | 272 |


## 1e. Diagnosticos del FE principal

|                                  |   estadistico |           p |
|:---------------------------------|--------------:|------------:|
| Durbin-Watson (apilado)          |        1.397  | nan         |
| AR(1) medio residuos FE          |        0.3087 | nan         |
| Jarque-Bera                      |       51.25   |   7.441e-12 |
| Breusch-Pagan (sobre X demeaned) |        6.87   |   0.1429    |

|                              |   VIF (X demeaned) |
|:-----------------------------|-------------------:|
| b1 dln ocupados              |              1.04  |
| b2 d(extr/total, pp)         |              1.041 |
| b3 dln pob espanola          |              1.036 |
| b4 terminadas/1000 hab (t-1) |              1.062 |

Poolability (F de igualdad de pendientes; efectos de CCAA y anio comunes):

|                                   |     F |   gl1 |   gl2 |   p_clasico |   p_wild_Webb |
|:----------------------------------|------:|------:|------:|------------:|--------------:|
| H0: pendientes iguales entre CCAA | 3.385 |    64 |   188 |   5.788e-11 |        0.3627 |

Nota: el p clasico supone errores iid y esta sobredimensionado (heterocedasticidad, AR(1) residual ~0.3-0.4); la referencia es el p wild. Con N*k=68 pendientes y T=17 la potencia es minima. Limite de aleatorizacion: con 17 unidades, un contraste de una region por permutacion/placebo no puede dar p < 1/17 = 0.059.

## 3a. Dependencia transversal: CD de Pesaran (2004/2015) - NO CONCLUYENTE sobre residuos de FE y CCE

CD = sqrt(2/(N(N-1))) sum sqrt(T_ij) rho_ij. **Advertencia**: sobre residuos de FE bidireccional y de CCE el CD no sigue una N(0,1) (problema de parametros incidentales; Juodis y Reese 2022, verificada en docs/literatura.md): la correlacion media de residuos de un FE con efectos de anio es mecanicamente ~ -1/(N-1) = -0.062, de modo que un CD negativo 'significativo' o un CCE-MG que 'pasa' el test no son interpretables y NO se usan como diagnostico. Solo el CD de la variable d_ln_ipv (sin ajustar) es informativo: dependencia transversal fuerte (factor nacional). Para T=17 el |rho| medio esperado bajo independencia es ~ sqrt(2/(pi T)) = 0.19; el observado en residuos (0.3) es mayor, indicio (no prueba) de dependencia heterogenea remanente. No se implementa el CD ponderado de Juodis-Reese.

|                                   |      CD |          p |   rho_medio |   abs_rho_medio |
|:----------------------------------|--------:|-----------:|------------:|----------------:|
| FE bidireccional (residuos)       | -2.539  | 0.0111     |    -0.05281 |          0.3507 |
| CCE-MG (residuos)                 | -0.8021 | 0.4225     |    -0.01668 |          0.3079 |
| CCE-P (residuos)                  | -2.316  | 0.02057    |    -0.04816 |          0.3417 |
| FE solo CCAA, sin anio (residuos) | 25.29   | 3.779e-141 |     0.526   |          0.5276 |
| d_ln_ipv (variable)               | 45.05   | 0          |     0.9369  |          0.9369 |


## 3b. Raiz unitaria de panel CIPS (Pesaran 2007), con constante, truncado

Implementacion propia (CADF con promedios transversales, 0/1 retardos). Valores criticos y p-valores por simulacion (1.000 replicas, N y T de cada serie, un factor comun + ruido normal; semilla fija), no de las tablas del articulo. H0: raiz unitaria en todas las unidades. Con T=17-18 es orientativo.

|    | serie                 | transformacion   |   retardos |   N |   T |   CIPS* |   vc5%_sim |   p_sim |
|---:|:----------------------|:-----------------|-----------:|----:|----:|--------:|-----------:|--------:|
|  0 | ln IPV                | nivel            |          0 |  17 |  18 | -1.817  |     -2.233 |   0.421 |
|  1 | ln IPV                | nivel            |          1 |  17 |  18 | -1.004  |     -2.212 |   0.968 |
|  2 | ln IPV                | 1a diferencia    |          0 |  17 |  17 | -3.293  |     -2.257 |   0     |
|  3 | ln IPV                | 1a diferencia    |          1 |  17 |  17 | -1.94   |     -2.232 |   0.193 |
|  4 | ln ocupados           | nivel            |          0 |  17 |  18 | -1.961  |     -2.233 |   0.242 |
|  5 | ln ocupados           | nivel            |          1 |  17 |  18 | -1.923  |     -2.212 |   0.21  |
|  6 | ln ocupados           | 1a diferencia    |          0 |  17 |  17 | -4.544  |     -2.257 |   0     |
|  7 | ln ocupados           | 1a diferencia    |          1 |  17 |  17 | -3.128  |     -2.232 |   0     |
|  8 | cuota extranjera (pp) | nivel            |          0 |  17 |  18 | -0.7447 |     -2.233 |   1     |
|  9 | cuota extranjera (pp) | nivel            |          1 |  17 |  18 | -1.035  |     -2.212 |   0.961 |
| 10 | cuota extranjera (pp) | 1a diferencia    |          0 |  17 |  17 | -1.535  |     -2.257 |   0.748 |
| 11 | cuota extranjera (pp) | 1a diferencia    |          1 |  17 |  17 | -1.277  |     -2.232 |   0.854 |
| 12 | ln pob espanola       | nivel            |          0 |  17 |  18 | -1.145  |     -2.233 |   0.972 |
| 13 | ln pob espanola       | nivel            |          1 |  17 |  18 | -1.367  |     -2.212 |   0.773 |
| 14 | ln pob espanola       | 1a diferencia    |          0 |  17 |  17 | -1.813  |     -2.257 |   0.408 |
| 15 | ln pob espanola       | 1a diferencia    |          1 |  17 |  17 | -1.659  |     -2.232 |   0.462 |
| 16 | terminadas/1000 hab   | nivel            |          0 |  17 |  18 | -3.987  |     -2.233 |   0     |
| 17 | terminadas/1000 hab   | nivel            |          1 |  17 |  18 | -3.381  |     -2.212 |   0     |
| 18 | terminadas/1000 hab   | 1a diferencia    |          0 |  17 |  17 | -5.158  |     -2.257 |   0     |
| 19 | terminadas/1000 hab   | 1a diferencia    |          1 |  17 |  17 | -3.973  |     -2.232 |   0     |


## 1f. Robustez de muestra y variable dependiente (FE bidireccional, EE cluster)

| muestra/dependiente                        | variable                     |      coef |   EE_cluster |        p |   N |
|:-------------------------------------------|:-----------------------------|----------:|-------------:|---------:|----:|
| IPV, 2009-2025, sin term.                  | b1 dln ocupados              | -0.07369  |     0.1028   | 0.4742   | 289 |
| IPV, 2009-2025, sin term.                  | b2 d(extr/total, pp)         |  0.00404  |     0.003973 | 0.3102   | 289 |
| IPV, 2009-2025, sin term.                  | b3 dln pob espanola          |  2.523    |     1.119    | 0.02505  | 289 |
| Valor tasado, 2009-2025                    | b1 dln ocupados              |  0.1812   |     0.05595  | 0.001367 | 284 |
| Valor tasado, 2009-2025                    | b2 d(extr/total, pp)         |  0.01639  |     0.006319 | 0.01006  | 284 |
| Valor tasado, 2009-2025                    | b3 dln pob espanola          |  2.013    |     0.8605   | 0.02011  | 284 |
| Valor tasado, 2009-2025                    | b4 terminadas/1000 hab (t-1) |  0.001243 |     0.001454 | 0.3935   | 284 |
| Valor tasado 2003-2025, 17 CCAA, sin term. | b1 dln ocupados              |  0.2166   |     0.06713  | 0.001373 | 386 |
| Valor tasado 2003-2025, 17 CCAA, sin term. | b2 d(extr/total, pp)         |  0.004437 |     0.007853 | 0.5724   | 386 |
| Valor tasado 2003-2025, 17 CCAA, sin term. | b3 dln pob espanola          |  1.228    |     0.9278   | 0.1864   | 386 |

Valor tasado 2003-2025: b2 con Driscoll-Kraay bw=3: 0.0044 (EE 0.0060).

## 2. Panel trimestral (robustez): Delta4 ln IPV

Muestra comun a los tres modelos: 17 CCAA, 2009Q2-2025Q1 (N=1088), FE CCAA + FE trimestre. Delta4 solapa 4 trimestres (MA(3)): EE Driscoll-Kraay con ancho 4 y 8 ademas de cluster por CCAA. **Advertencia**: la poblacion es anual (1 de enero) interpolada log-linealmente y acaba en 2025Q1; solo entra en Delta4 (Q2, Q3) y recorta la muestra a 2025Q1. Q1 usa d4 ln terminadas retardada 1 trimestre (sin poblacion); Q3 usa terminadas por 1.000 hab. (nivel, t-1, poblacion interpolada). Las d4 de poblacion interpolada son casi deterministas por tramos: no son variacion trimestral informativa.

| modelo          | variable           |      coef |   EE_cluster |   p_cluster |   EE_DK_bw4 |   p_DK_bw4 |   EE_DK_bw8 |   p_DK_bw8 |    N |
|:----------------|:-------------------|----------:|-------------:|------------:|------------:|-----------:|------------:|-----------:|-----:|
| Q1_sin_pob      | d4_ln_ocupados     | -0.04686  |    0.0575    |    0.4153   |    0.05315  |   0.3782   |    0.05717  |    0.4127  | 1088 |
| Q1_sin_pob      | d4_ln_compraventas | -0.006504 |    0.008308  |    0.4339   |    0.009202 |   0.4799   |    0.009607 |    0.4986  | 1088 |
| Q1_sin_pob      | d4_ln_term_l1      |  0.00229  |    0.001085  |    0.03509  |    0.001784 |   0.1995   |    0.001623 |    0.1585  | 1088 |
| Q2_con_pob_d4   | d4_ln_ocupados     | -0.06793  |    0.06369   |    0.2864   |    0.04929  |   0.1685   |    0.05239  |    0.1951  | 1088 |
| Q2_con_pob_d4   | d4_ln_compraventas | -0.00538  |    0.008345  |    0.5193   |    0.008132 |   0.5084   |    0.008421 |    0.5231  | 1088 |
| Q2_con_pob_d4   | d4_ln_term_l1      |  0.002181 |    0.0009371 |    0.02016  |    0.001757 |   0.2147   |    0.001603 |    0.1741  | 1088 |
| Q2_con_pob_d4   | d4_share_extr      |  0.01417  |    0.004511  |    0.001727 |    0.009928 |   0.1537   |    0.01108  |    0.2011  | 1088 |
| Q2_con_pob_d4   | d4_ln_pob_espanola |  2.54     |    1.273     |    0.04624  |    1.027    |   0.01354  |    1.156    |    0.02821 | 1088 |
| Q3_term_por_hab | d4_ln_ocupados     | -0.05611  |    0.06371   |    0.3787   |    0.04914  |   0.2538   |    0.05207  |    0.2815  | 1088 |
| Q3_term_por_hab | d4_ln_compraventas | -0.00289  |    0.008314  |    0.7282   |    0.007469 |   0.6989   |    0.007722 |    0.7083  | 1088 |
| Q3_term_por_hab | term_pc_l1         |  0.01055  |    0.004461  |    0.01819  |    0.00437  |   0.01593  |    0.004367 |    0.01585 | 1088 |
| Q3_term_por_hab | d4_share_extr      |  0.01118  |    0.00467   |    0.01682  |    0.01015  |   0.2708   |    0.01121  |    0.3185  | 1088 |
| Q3_term_por_hab | d4_ln_pob_espanola |  2.394    |    1.209     |    0.04803  |    0.9064   |   0.008392 |    1.015    |    0.01849 | 1088 |

CD de Pesaran (residuos Q1): -4.57 (p=4.78e-06); |rho| medio 0.36.

## 4a. Heterogeneidad: interacciones de b1 (ocupados) y b2 (cuota extranjera) con dummies regionales

Cada fila es el diferencial respecto al resto de CCAA (efectos de anio y CCAA incluidos). Modelos individuales (una dummy) y conjunto (6 dummies; referencia = resto de CCAA). EE cluster y p-valor wild cluster bootstrap restringido (Webb). Holm dentro de cada familia (12 interacciones). **Aviso**: cada dummy regional marca UN solo cluster; el EE cluster (CRVE) es poco fiable (p_cluster muy bajos con p_wild altos), y el wild bootstrap con un solo cluster tratado tampoco es valido (MacKinnon y Webb 2018): los p_wild agrupados en 0.3-0.5 reflejan esa degeneracion y NO evidencia de homogeneidad. Referencia: p_wild_Webb, con cautela.

| modelo          | grupo                                                     | interaccion              |      coef |   EE_cluster |   p_cluster |   p_wild_Webb |   p_wild_Holm |
|:----------------|:----------------------------------------------------------|:-------------------------|----------:|-------------:|------------:|--------------:|--------------:|
| H_C. Valenciana | C. Valenciana                                             | dln_ocup_x_C. Valenciana |  0.02241  |     0.08174  |   0.7842    |        0.7935 |             1 |
| H_C. Valenciana | C. Valenciana                                             | dshare_x_C. Valenciana   | -0.006436 |     0.003904 |   0.1005    |        0.4438 |             1 |
| H_Madrid        | Madrid                                                    | dln_ocup_x_Madrid        |  0.5531   |     0.1287   |   2.47e-05  |        0.386  |             1 |
| H_Madrid        | Madrid                                                    | dshare_x_Madrid          | -0.01831  |     0.00396  |   6.036e-06 |        0.3338 |             1 |
| H_Cataluna      | Cataluna                                                  | dln_ocup_x_Cataluna      |  0.5743   |     0.07501  |   4.148e-13 |        0.467  |             1 |
| H_Cataluna      | Cataluna                                                  | dshare_x_Cataluna        | -0.0109   |     0.003899 |   0.005582  |        0.4849 |             1 |
| H_Baleares      | Baleares                                                  | dln_ocup_x_Baleares      |  0.1237   |     0.09226  |   0.1813    |        0.4827 |             1 |
| H_Baleares      | Baleares                                                  | dshare_x_Baleares        | -0.01614  |     0.004108 |   0.0001104 |        0.437  |             1 |
| H_Canarias      | Canarias                                                  | dln_ocup_x_Canarias      |  0.07435  |     0.09097  |   0.4145    |        0.5301 |             1 |
| H_Canarias      | Canarias                                                  | dshare_x_Canarias        | -0.003416 |     0.004379 |   0.4361    |        0.5599 |             1 |
| H_Andalucia     | Andalucia                                                 | dln_ocup_x_Andalucia     | -0.1325   |     0.08737  |   0.1308    |        0.4776 |             1 |
| H_Andalucia     | Andalucia                                                 | dshare_x_Andalucia       | -0.001575 |     0.006123 |   0.7972    |        0.7965 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_C. Valenciana |  0.113    |     0.1075   |   0.2942    |        0.466  |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_C. Valenciana   | -0.0171   |     0.003661 |   5.007e-06 |        0.1831 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Madrid        |  0.6416   |     0.1626   |   0.0001045 |        0.4073 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Madrid          | -0.0289   |     0.004534 |   9.301e-10 |        0.1258 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Cataluna      |  0.6482   |     0.1125   |   2.512e-08 |        0.4112 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Cataluna        | -0.02247  |     0.004281 |   3.355e-07 |        0.1719 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Baleares      |  0.2411   |     0.1369   |   0.07951   |        0.4547 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Baleares        | -0.02616  |     0.004382 |   8.536e-09 |        0.2246 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Canarias      |  0.1836   |     0.1213   |   0.1312    |        0.3944 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Canarias        | -0.01151  |     0.003814 |   0.002828  |        0.4724 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Andalucia     |  0.001665 |     0.1181   |   0.9888    |        0.9922 |             1 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Andalucia       | -0.00396  |     0.005945 |   0.506     |        0.5722 |             1 |

Test conjunto de las 12 interacciones = 0 (F de sumas de cuadrados, no robusto): F=4.91, p=2.97e-07; p del F por wild bootstrap = 0.107.

## 4b. Coeficientes CCE individuales por CCAA

**Advertencia**: cada unidad tiene T=17 y 10 parametros (7 gl); IC anchos; el CCE individual solo es consistente para T grande. Aqui los coeficientes; EE e IC95% en `cce_por_ccaa.csv` y `cce_por_ccaa.png`.

| ccaa                       |   b1 dln ocupados |   b2 d(extr/total, pp) |   b3 dln pob espanola |   b4 terminadas/1000 hab (t-1) |
|:---------------------------|------------------:|-----------------------:|----------------------:|-------------------------------:|
| Andalucía                  |          -0.1023  |               0.03276  |              -3.591   |                      0.005556  |
| Aragón                     |          -0.0406  |               0.01213  |              -0.03281 |                      0.00374   |
| Asturias                   |           0.08088 |               0.000207 |              -4.849   |                      0.009806  |
| Canarias                   |           0.09843 |              -0.004441 |              -4.69    |                     -0.00602   |
| Cantabria                  |           0.2764  |               0.1676   |              -2.671   |                     -0.006551  |
| Castilla y León            |           0.4735  |              -0.001346 |              -2.773   |                     -0.004879  |
| Castilla-La Mancha         |          -0.3005  |              -0.03918  |               3.761   |                     -0.00684   |
| Cataluña                   |           0.9571  |               0.09841  |              12.24    |                     -0.002862  |
| Comunidad Foral de Navarra |           0.337   |              -0.002339 |              -8.038   |                     -0.002148  |
| Comunidad de Madrid        |          -0.4064  |               0.09515  |               5.319   |                     -0.0048    |
| Comunitat Valenciana       |          -0.3724  |               0.05241  |              -1.341   |                      0.0009287 |
| Extremadura                |          -0.8312  |               0.05561  |               7.109   |                     -0.01088   |
| Galicia                    |           0.2556  |               0.05996  |               2.411   |                      0.01531   |
| Illes Balears              |          -0.1768  |              -0.02963  |               0.8544  |                     -0.01137   |
| La Rioja                   |           0.03811 |              -0.04835  |              -3.339   |                      0.0143    |
| País Vasco                 |           0.4898  |              -0.03742  |               5.841   |                      0.01032   |
| Región de Murcia           |           0.1782  |               0.01601  |               0.6096  |                     -0.02404   |

Dispersion de b2 individual: sd=0.058 (EE MG=0.014). Valencia: b1=-0.372 (EE 0.309), b2=0.052 (EE 0.017).

## 4c. C. Valenciana frente a Espana: crecimiento acumulado

Del trimestre inicial a 2026Q2 (IPV base 2025 y valor tasado MIVAU; Espana = `nacional_q`).

| periodo       | serie    |   crec_acum_CV_% |   crec_acum_Espana_% |   dif_pp |
|:--------------|:---------|-----------------:|---------------------:|---------:|
| 2014Q1-2026Q2 | ipv      |            95.88 |               109.9  |  -14.05  |
| 2014Q1-2026Q2 | p_tasado |            73.56 |                61.37 |   12.19  |
| 2021Q1-2026Q2 | ipv      |            59.17 |                56.35 |    2.819 |
| 2021Q1-2026Q2 | p_tasado |            58.53 |                44.89 |   13.64  |


## 5. Registro de busqueda y correccion para b2 (cuota extranjera)

Especificaciones registradas en `output/registro_busqueda_f5.csv`: **23**. Familia de 15 p-valores de b2 (distintas inferencias, tendencias, CCE, muestras, alineaciones temporales y b2 trimestrales; excluidas las interacciones de heterogeneidad, que son otra hipotesis) corregida por Holm y Bonferroni. Muy correlacionadas entre si, asi que ambas correcciones son conservadoras.

|                   |   p_sin_corregir |   p_Holm |   p_Bonferroni |
|:------------------|-----------------:|---------:|---------------:|
| A_FE_cl           |          0.7772  |   1      |         1      |
| A_FE_dk           |          0.9127  |   1      |         1      |
| A_FE_dk3          |          0.899   |   1      |         1      |
| A_FE_wild         |          0.774   |   1      |         1      |
| A_FE_trend        |          0.2883  |   1      |         1      |
| A_CCE_MG          |          0.07202 |   0.81   |         1      |
| A_CCE_P           |          0.04025 |   0.5233 |         0.6038 |
| T_flow_tm1        |          0.8565  |   1      |         1      |
| T_mid             |          0.0675  |   0.81   |         1      |
| T_flow_t          |          0.0101  |   0.1509 |         0.1515 |
| R_sin_term        |          0.3102  |   1      |         1      |
| R_ptasado_main    |          0.01006 |   0.1509 |         0.1509 |
| R_ptasado_2003    |          0.5724  |   1      |         1      |
| Q_Q2_con_pob_d4   |          0.1537  |   1      |         1      |
| Q_Q3_term_por_hab |          0.2708  |   1      |         1      |


## Problemas abiertos

- Timing de b2 (stock a 1 de enero frente a IPV de media anual) decide el resultado; sin instrumento no se distingue entre efecto y causalidad inversa (F3).
- T=17, N=17: pocos clusters (wild bootstrap como referencia); Driscoll-Kraay y CCE por unidad con pocos grados de libertad; CIPS y poolability con potencia dudosa; wild bootstrap invalido con un solo cluster tratado (interacciones regionales).
- CD sobre residuos de FE/CCE no interpretable; no se implementa el CD ponderado de Juodis-Reese (CDw).
- b4 > 0 sin explicacion estructural; falta probar dinamica (y retardada) en una fase posterior.
- Nota (1) de Extremadura en MIVAU 32101000 sin resolver (revision F5).
- Poblacion trimestral interpolada y hasta 2025Q1.
- Valor tasado y `p_bde` son la misma serie (decisiones.md): robusteces no independientes.
- rmse_oos no se calcula en el registro: los efectos de anio no son predecibles fuera de muestra.
