# F5: panel de CCAA (P4) - resumen

Generado por `src/f5_panel.py` (semilla 20261009).

## Respuesta a P4

**Pregunta**: ¿difieren entre CCAA (y en la C. Valenciana) las asociaciones del precio de la vivienda con empleo y poblacion extranjera?

- Nivel de evidencia: **asociacion condicional** (panel observacional, FE de CCAA y anio, CCE). Sin identificacion causal en esta fase; para la lectura causal remite al IV de F3 (no se repite aqui).
- FE bidireccional (16 CCAA, 2009-2025): b1 (empleo) = 0.052 (EE cluster 0.077, p=0.501, p wild=0.498); b2 (+1 pp cuota extranjera) = -0.001 (EE 0.004, p cluster=0.869, p DK bw2=0.944, p wild=0.871).
- CCE-MG: b1=0.126 (0.090), b2=0.025 (0.016); CCE-P: b1=0.024 (0.072), b2=0.020 (0.010).
- Lectura: b1 y b2 medios no distinguibles de 0 en FE (CCE-P b2 ~ 0.02, p~0.05, no robusto a la correccion por busqueda). Heterogeneidad: poolability F=2.69 (p=2.58e-07); F conjunto de las 12 interacciones regionales=4.59 (p=1.24e-06; p wild=0.0809). Interacciones de la C. Valenciana: tabla 4a.
- Dependencia transversal: CD FE=-2.47 (p=0.0136); CCE-MG=-0.58 (p=0.564); CCE-P=-2.21 (p=0.0273).

## 0. Datos y muestra

Panel anual `panel_ccaa_a`: dependiente d_ln_ipv (IPV media anual, base 2025). Muestra principal 16 CCAA x 17 anios (2009-2025; N=272, balanceado). **Extremadura queda fuera de la muestra principal** porque `terminadas` (MIVAU) no tiene datos para esa CCAA (0 observaciones); el requisito de misma muestra obliga a recortar a 16 CCAA. Robusteces con 17 CCAA sin `terminadas` y con valor tasado desde 2003. b2 se mide en puntos porcentuales de cuota extranjera (pob_extranj/pob_total a 1 de enero); la poblacion es stock a 1 de enero y IPV/ocupados medias anuales (desfase de timing). `term_l1` = terminadas por 1.000 hab. de t-1.

## 1a. FE bidireccional (CCAA + anio), muestra principal

N=272, 16 CCAA, T=17. EE cluster por CCAA (16 clusters), Driscoll-Kraay (Bartlett; con T=17 ancho 2-3, poco fiable) y p-valor del wild cluster bootstrap restringido (Webb, 9999 replicas, semilla 20261009) para H0: coef=0.

| variable                     |       coef |   EE_cluster |   p_cluster |   EE_DK_bw2 |   p_DK_bw2 |   EE_DK_bw3 |   p_DK_bw3 |   p_wild_Webb |
|:-----------------------------|-----------:|-------------:|------------:|------------:|-----------:|------------:|-----------:|--------------:|
| b1 dln ocupados              |  0.05214   |    0.07738   |   0.5011    |   0.07388   |  0.481     |   0.06552   |  0.4269    |        0.4985 |
| b2 d(extr/total, pp)         | -0.0006437 |    0.003908  |   0.8693    |   0.009216  |  0.9444    |   0.008362  |  0.9387    |        0.8713 |
| b3 dln pob espanola          |  1.509     |    0.8337    |   0.07149   |   0.9586    |  0.1167    |   0.9206    |  0.1024    |        0.1472 |
| b4 terminadas/1000 hab (t-1) |  0.003386  |    0.0008333 |   6.593e-05 |   0.0009064 |  0.0002351 |   0.0007906 |  2.689e-05 |        0.0206 |


## 1b. FE + tendencias lineales por CCAA (en diferencias = deriva de crecimiento propia por CCAA)

|                              |      coef |   EE_cluster |   p_cluster |   EE_DK_bw2 |   p_DK_bw2 |
|:-----------------------------|----------:|-------------:|------------:|------------:|-----------:|
| b1 dln ocupados              |  0.07559  |     0.07608  |   0.3215    |    0.08406  |   0.3695   |
| b2 d(extr/total, pp)         | -0.002853 |     0.006686 |   0.67      |    0.0154   |   0.8532   |
| b3 dln pob espanola          |  1.313    |     0.8068   |   0.1051    |    1.151    |   0.2552   |
| b4 terminadas/1000 hab (t-1) |  0.004111 |     0.001131 |   0.0003472 |    0.001488 |   0.006207 |


## 1c. CCE-MG y CCE-pooled (Pesaran 2006)

Cada regresion se aumenta con constante y promedios transversales de y y de las 4 X (6 auxiliares por CCAA; 7 gl por unidad en MG: muy justo). EE no parametricos (varianza empirica de los b_i). Sin efectos de anio (los promedios los sustituyen).

| estimador   | var                          |      coef |       EE |       z |       p |
|:------------|:-----------------------------|----------:|---------:|--------:|--------:|
| CCE-MG      | b1 dln ocupados              |  0.1259   | 0.09034  |  1.394  | 0.1633  |
| CCE-MG      | b2 d(extr/total, pp)         |  0.02528  | 0.01571  |  1.609  | 0.1075  |
| CCE-MG      | b3 dln pob espanola          |  0.1965   | 1.28     |  0.1535 | 0.878   |
| CCE-MG      | b4 terminadas/1000 hab (t-1) | -0.001303 | 0.00252  | -0.5171 | 0.6051  |
| CCE-P       | b1 dln ocupados              |  0.02432  | 0.07181  |  0.3387 | 0.7349  |
| CCE-P       | b2 d(extr/total, pp)         |  0.02017  | 0.01036  |  1.946  | 0.05165 |
| CCE-P       | b3 dln pob espanola          |  1.605    | 1.411    |  1.137  | 0.2555  |
| CCE-P       | b4 terminadas/1000 hab (t-1) | -0.001406 | 0.002255 | -0.6234 | 0.533   |


## 1d. Comparacion de estimadores (misma muestra: 16 CCAA x 2009-2025)

|                              |   FE cluster |        EE |   FE+tend |   EE tend |    CCE-MG |   EE MG |     CCE-P |     EE P |
|:-----------------------------|-------------:|----------:|----------:|----------:|----------:|--------:|----------:|---------:|
| b1 dln ocupados              |    0.05214   | 0.07738   |  0.07559  |  0.07608  |  0.1259   | 0.09034 |  0.02432  | 0.07181  |
| b2 d(extr/total, pp)         |   -0.0006437 | 0.003908  | -0.002853 |  0.006686 |  0.02528  | 0.01571 |  0.02017  | 0.01036  |
| b3 dln pob espanola          |    1.509     | 0.8337    |  1.313    |  0.8068   |  0.1965   | 1.28    |  1.605    | 1.411    |
| b4 terminadas/1000 hab (t-1) |    0.003386  | 0.0008333 |  0.004111 |  0.001131 | -0.001303 | 0.00252 | -0.001406 | 0.002255 |


## 1e. Diagnosticos del FE principal

|                                  |   estadistico |           p |
|:---------------------------------|--------------:|------------:|
| Durbin-Watson (apilado)          |        1.391  | nan         |
| AR(1) medio residuos FE          |        0.3309 | nan         |
| Jarque-Bera                      |       37.36   |   7.715e-09 |
| Breusch-Pagan (sobre X demeaned) |        2.522  |   0.6408    |

|                              |   VIF (X demeaned) |
|:-----------------------------|-------------------:|
| b1 dln ocupados              |              1.04  |
| b2 d(extr/total, pp)         |              1.048 |
| b3 dln pob espanola          |              1.051 |
| b4 terminadas/1000 hab (t-1) |              1.061 |

Poolability (F de igualdad de pendientes; efectos de CCAA y anio comunes):

|                                   |    F |   gl1 |   gl2 |         p |
|:----------------------------------|-----:|------:|------:|----------:|
| H0: pendientes iguales entre CCAA | 2.69 |    60 |   176 | 2.579e-07 |

Nota: con N*k=64 pendientes y T=17 el F tiene poca potencia y distorsion de tamano con heterocedasticidad; orientativo.

## 3a. Dependencia transversal: test CD de Pesaran (2004; la version 2015 de dependencia debil usa el mismo estadistico)

CD = sqrt(2/(N(N-1))) sum sqrt(T_ij) rho_ij ~ N(0,1) bajo H0 de independencia transversal (debil).

|                                   |      CD |          p |   rho_medio |   abs_rho_medio |
|:----------------------------------|--------:|-----------:|------------:|----------------:|
| FE bidireccional (residuos)       | -2.467  | 0.01362    |    -0.05462 |          0.33   |
| CCE-MG (residuos)                 | -0.5766 | 0.5642     |    -0.01277 |          0.308  |
| CCE-P (residuos)                  | -2.207  | 0.0273     |    -0.04887 |          0.3459 |
| FE solo CCAA, sin anio (residuos) | 24.52   | 9.025e-133 |     0.5429  |          0.5429 |
| d_ln_ipv (variable)               | 42.66   | 0          |     0.9445  |          0.9445 |


## 3b. Raiz unitaria de panel CIPS (Pesaran 2007), con constante, truncado

Implementacion propia (CADF con promedios transversales, 0/1 retardos). Valores criticos y p-valores por simulacion (1.000 replicas, N y T de cada serie, un factor comun + ruido normal; semilla fija), no de las tablas del articulo. H0: raiz unitaria en todas las unidades. Con T=17-18 es orientativo.

|    | serie                 | transformacion   |   retardos |   N |   T |   CIPS* |   vc5%_sim |   p_sim |
|---:|:----------------------|:-----------------|-----------:|----:|----:|--------:|-----------:|--------:|
|  0 | ln IPV                | nivel            |          0 |  16 |  18 | -1.931  |     -2.24  |   0.268 |
|  1 | ln IPV                | nivel            |          1 |  16 |  18 | -1.143  |     -2.184 |   0.935 |
|  2 | ln IPV                | 1a diferencia    |          0 |  16 |  17 | -3.303  |     -2.269 |   0     |
|  3 | ln IPV                | 1a diferencia    |          1 |  16 |  17 | -1.905  |     -2.274 |   0.262 |
|  4 | ln ocupados           | nivel            |          0 |  16 |  18 | -1.918  |     -2.24  |   0.283 |
|  5 | ln ocupados           | nivel            |          1 |  16 |  18 | -1.804  |     -2.184 |   0.343 |
|  6 | ln ocupados           | 1a diferencia    |          0 |  16 |  17 | -4.486  |     -2.269 |   0     |
|  7 | ln ocupados           | 1a diferencia    |          1 |  16 |  17 | -3.035  |     -2.274 |   0     |
|  8 | cuota extranjera (pp) | nivel            |          0 |  16 |  18 | -0.6985 |     -2.24  |   1     |
|  9 | cuota extranjera (pp) | nivel            |          1 |  16 |  18 | -1.005  |     -2.184 |   0.972 |
| 10 | cuota extranjera (pp) | 1a diferencia    |          0 |  16 |  17 | -1.524  |     -2.269 |   0.735 |
| 11 | cuota extranjera (pp) | 1a diferencia    |          1 |  16 |  17 | -1.335  |     -2.274 |   0.789 |
| 12 | ln pob espanola       | nivel            |          0 |  16 |  18 | -1.387  |     -2.24  |   0.861 |
| 13 | ln pob espanola       | nivel            |          1 |  16 |  18 | -1.645  |     -2.184 |   0.509 |
| 14 | ln pob espanola       | 1a diferencia    |          0 |  16 |  17 | -1.826  |     -2.269 |   0.371 |
| 15 | ln pob espanola       | 1a diferencia    |          1 |  16 |  17 | -1.684  |     -2.274 |   0.46  |
| 16 | terminadas/1000 hab   | nivel            |          0 |  16 |  18 | -4.122  |     -2.24  |   0     |
| 17 | terminadas/1000 hab   | nivel            |          1 |  16 |  18 | -3.22   |     -2.184 |   0     |
| 18 | terminadas/1000 hab   | 1a diferencia    |          0 |  16 |  17 | -5.304  |     -2.269 |   0     |
| 19 | terminadas/1000 hab   | 1a diferencia    |          1 |  16 |  17 | -3.85   |     -2.274 |   0     |


## 1f. Robustez de muestra y variable dependiente (FE bidireccional, EE cluster)

| muestra/dependiente                        | variable                     |      coef |   EE_cluster |        p |   N |
|:-------------------------------------------|:-----------------------------|----------:|-------------:|---------:|----:|
| IPV, 17 CCAA 2008-2025, sin term.          | b1 dln ocupados              | -0.07285  |     0.09713  | 0.4539   | 306 |
| IPV, 17 CCAA 2008-2025, sin term.          | b2 d(extr/total, pp)         | -0.001726 |     0.004811 | 0.7202   | 306 |
| IPV, 17 CCAA 2008-2025, sin term.          | b3 dln pob espanola          |  2.989    |     1.156    | 0.01025  | 306 |
| IPV, 16 CCAA 2009-2025, sin term.          | b1 dln ocupados              | -0.007322 |     0.08819  | 0.9339   | 272 |
| IPV, 16 CCAA 2009-2025, sin term.          | b2 d(extr/total, pp)         |  0.003012 |     0.004194 | 0.4733   | 272 |
| IPV, 16 CCAA 2009-2025, sin term.          | b3 dln pob espanola          |  2.028    |     1.139    | 0.07613  | 272 |
| Valor tasado, 16 CCAA 2009-2025            | b1 dln ocupados              |  0.1827   |     0.05904  | 0.002211 | 267 |
| Valor tasado, 16 CCAA 2009-2025            | b2 d(extr/total, pp)         |  0.01294  |     0.006167 | 0.03695  | 267 |
| Valor tasado, 16 CCAA 2009-2025            | b3 dln pob espanola          |  1.371    |     0.612    | 0.02601  | 267 |
| Valor tasado, 16 CCAA 2009-2025            | b4 terminadas/1000 hab (t-1) |  0.00176  |     0.001348 | 0.1929   | 267 |
| Valor tasado 2003-2025, 17 CCAA, sin term. | b1 dln ocupados              |  0.2166   |     0.06713  | 0.001373 | 386 |
| Valor tasado 2003-2025, 17 CCAA, sin term. | b2 d(extr/total, pp)         |  0.004437 |     0.007853 | 0.5724   | 386 |
| Valor tasado 2003-2025, 17 CCAA, sin term. | b3 dln pob espanola          |  1.228    |     0.9278   | 0.1864   | 386 |

Valor tasado 2003-2025: b2 con Driscoll-Kraay bw=3: 0.0044 (EE 0.0060).

## 2. Panel trimestral (robustez): Delta4 ln IPV

Muestra comun a los tres modelos: 16 CCAA (sin Extremadura), 2009Q2-2025Q1 (N=1024), FE CCAA + FE trimestre. Delta4 solapa 4 trimestres (MA(3)): EE Driscoll-Kraay con ancho 4 y 8 ademas de cluster por CCAA. **Advertencia**: la poblacion es anual (1 de enero) interpolada log-linealmente y acaba en 2025Q1; solo entra en Delta4 (Q2, Q3) y recorta la muestra a 2025Q1. Q1 usa d4 ln terminadas retardada 1 trimestre (sin poblacion); Q3 usa terminadas por 1.000 hab. (nivel, t-1, poblacion interpolada). Las d4 de poblacion interpolada son casi deterministas por tramos: no son variacion trimestral informativa.

| modelo          | variable           |      coef |   EE_cluster |   p_cluster |   EE_DK_bw4 |   p_DK_bw4 |   EE_DK_bw8 |   p_DK_bw8 |    N |
|:----------------|:-------------------|----------:|-------------:|------------:|------------:|-----------:|------------:|-----------:|-----:|
| Q1_sin_pob      | d4_ln_ocupados     | -0.005774 |    0.04706   |    0.9024   |    0.03278  |   0.8602   |    0.03237  |   0.8585   | 1024 |
| Q1_sin_pob      | d4_ln_compraventas | -0.006392 |    0.008662  |    0.4607   |    0.008269 |   0.4397   |    0.008608 |   0.4579   | 1024 |
| Q1_sin_pob      | d4_ln_term_l1      |  0.002126 |    0.001033  |    0.0399   |    0.001609 |   0.1869   |    0.001515 |   0.161    | 1024 |
| Q2_con_pob_d4   | d4_ln_ocupados     | -0.02198  |    0.05199   |    0.6725   |    0.03161  |   0.487    |    0.03032  |   0.4687   | 1024 |
| Q2_con_pob_d4   | d4_ln_compraventas | -0.006137 |    0.008484  |    0.4697   |    0.007564 |   0.4174   |    0.007804 |   0.4319   | 1024 |
| Q2_con_pob_d4   | d4_ln_term_l1      |  0.0021   |    0.0009319 |    0.02445  |    0.001614 |   0.1936   |    0.001519 |   0.1672   | 1024 |
| Q2_con_pob_d4   | d4_share_extr      |  0.01211  |    0.004709  |    0.01029  |    0.009047 |   0.1811   |    0.0105   |   0.2491   | 1024 |
| Q2_con_pob_d4   | d4_ln_pob_espanola |  1.864    |    1.225     |    0.1284   |    1.043    |   0.07423  |    1.15     |   0.1055   | 1024 |
| Q3_term_por_hab | d4_ln_ocupados     | -0.00845  |    0.05034   |    0.8667   |    0.02856  |   0.7674   |    0.02821  |   0.7646   | 1024 |
| Q3_term_por_hab | d4_ln_compraventas | -0.002742 |    0.008563  |    0.7488   |    0.006555 |   0.6758   |    0.006815 |   0.6875   | 1024 |
| Q3_term_por_hab | term_pc_l1         |  0.01256  |    0.004053  |    0.001992 |    0.004565 |   0.006031 |    0.004483 |   0.005173 | 1024 |
| Q3_term_por_hab | d4_share_extr      |  0.008361 |    0.004489  |    0.06285  |    0.009044 |   0.3555   |    0.01036  |   0.4198   | 1024 |
| Q3_term_por_hab | d4_ln_pob_espanola |  1.643    |    1.04      |    0.1143   |    0.9598   |   0.08718  |    1.052    |   0.1185   | 1024 |

CD de Pesaran (residuos Q1): -4.54 (p=5.61e-06); |rho| medio 0.35.

## 4a. Heterogeneidad: interacciones de b1 (ocupados) y b2 (cuota extranjera) con dummies regionales

Cada fila es el diferencial respecto al resto de CCAA (efectos de anio y CCAA incluidos). Modelos individuales (una dummy) y conjunto (6 dummies; referencia = 10 CCAA restantes). EE cluster y p-valor wild cluster bootstrap restringido (Webb). Holm dentro de cada familia (12 interacciones). **Aviso**: cada dummy regional marca UN solo cluster; el EE cluster (CRVE) es poco fiable (p_cluster muy bajos con p_wild altos): la referencia es p_wild_Webb.

| modelo          | grupo                                                     | interaccion              |      coef |   EE_cluster |   p_cluster |   p_wild_Webb |   p_wild_Holm |
|:----------------|:----------------------------------------------------------|:-------------------------|----------:|-------------:|------------:|--------------:|--------------:|
| H_C. Valenciana | C. Valenciana                                             | dln_ocup_x_C. Valenciana | -0.02652  |     0.06944  |   0.7029    |        0.7286 |        1      |
| H_C. Valenciana | C. Valenciana                                             | dshare_x_C. Valenciana   | -0.004914 |     0.003676 |   0.1826    |        0.4762 |        1      |
| H_Madrid        | Madrid                                                    | dln_ocup_x_Madrid        |  0.4723   |     0.1091   |   2.22e-05  |        0.3967 |        1      |
| H_Madrid        | Madrid                                                    | dshare_x_Madrid          | -0.01873  |     0.003834 |   1.91e-06  |        0.3294 |        1      |
| H_Cataluna      | Cataluna                                                  | dln_ocup_x_Cataluna      |  0.5216   |     0.05583  |   0         |        0.4224 |        1      |
| H_Cataluna      | Cataluna                                                  | dshare_x_Cataluna        | -0.01086  |     0.003885 |   0.005611  |        0.4832 |        1      |
| H_Baleares      | Baleares                                                  | dln_ocup_x_Baleares      |  0.05007  |     0.06378  |   0.4332    |        0.5542 |        1      |
| H_Baleares      | Baleares                                                  | dshare_x_Baleares        | -0.01623  |     0.004248 |   0.0001699 |        0.4556 |        1      |
| H_Canarias      | Canarias                                                  | dln_ocup_x_Canarias      | -0.001517 |     0.06473  |   0.9813    |        0.9805 |        1      |
| H_Canarias      | Canarias                                                  | dshare_x_Canarias        | -0.004187 |     0.004671 |   0.3709    |        0.524  |        1      |
| H_Andalucia     | Andalucia                                                 | dln_ocup_x_Andalucia     | -0.2014   |     0.05972  |   0.0008686 |        0.4158 |        1      |
| H_Andalucia     | Andalucia                                                 | dshare_x_Andalucia       | -0.002304 |     0.006874 |   0.7378    |        0.742  |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_C. Valenciana |  0.02007  |     0.08489  |   0.8133    |        0.8098 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_C. Valenciana   | -0.01613  |     0.003344 |   2.621e-06 |        0.1312 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Madrid        |  0.5153   |     0.1245   |   4.932e-05 |        0.3898 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Madrid          | -0.02992  |     0.00388  |   4.081e-13 |        0.0803 |        0.9636 |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Cataluna      |  0.5533   |     0.0849   |   4.667e-10 |        0.3363 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Cataluna        | -0.02307  |     0.003768 |   4.065e-09 |        0.1271 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Baleares      |  0.1227   |     0.1002   |   0.2223    |        0.4778 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Baleares        | -0.02678  |     0.003615 |   2.609e-12 |        0.1538 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Canarias      |  0.07035  |     0.08366  |   0.4013    |        0.4744 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Canarias        | -0.01199  |     0.003711 |   0.001419  |        0.4514 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dln_ocup_x_Andalucia     | -0.1032   |     0.08293  |   0.2145    |        0.4563 |        1      |
| H_conjunto      | C. Valenciana+Madrid+Cataluna+Baleares+Canarias+Andalucia | dshare_x_Andalucia       | -0.00301  |     0.007334 |   0.6819    |        0.6955 |        1      |

Test conjunto de las 12 interacciones = 0 (F de sumas de cuadrados, no robusto): F=4.59, p=1.24e-06; p del F por wild bootstrap = 0.0809.

## 4b. Coeficientes CCE individuales por CCAA

**Advertencia**: cada unidad tiene T=17 y 10 parametros (7 gl); IC anchos; el CCE individual solo es consistente para T grande. Aqui los coeficientes; EE e IC95% en `cce_por_ccaa.csv` y `cce_por_ccaa.png`.

| ccaa                       |   b1 dln ocupados |   b2 d(extr/total, pp) |   b3 dln pob espanola |   b4 terminadas/1000 hab (t-1) |
|:---------------------------|------------------:|-----------------------:|----------------------:|-------------------------------:|
| Andalucía                  |          -0.09028 |               0.03436  |              -2.798   |                      0.005671  |
| Aragón                     |           0.02147 |               0.008276 |               1.063   |                      0.003227  |
| Asturias                   |           0.05088 |               0.005523 |              -5.03    |                      0.009227  |
| Canarias                   |           0.108   |              -0.009912 |              -5.155   |                     -0.005521  |
| Cantabria                  |           0.4089  |               0.1816   |              -3.272   |                     -0.007073  |
| Castilla y León            |           0.7314  |               0.006652 |              -3.687   |                     -0.008368  |
| Castilla-La Mancha         |          -0.4022  |              -0.04302  |               4.228   |                     -0.005949  |
| Cataluña                   |           0.6138  |               0.1044   |              12.41    |                     -0.00418   |
| Comunidad Foral de Navarra |           0.2494  |               0.001333 |              -6.928   |                     -0.0003102 |
| Comunidad de Madrid        |          -0.3928  |               0.09881  |               5.046   |                     -0.007759  |
| Comunitat Valenciana       |          -0.286   |               0.04901  |              -1.219   |                      0.001355  |
| Galicia                    |           0.5358  |               0.07123  |               5.013   |                      0.006933  |
| Illes Balears              |          -0.1753  |              -0.02448  |               0.8084  |                     -0.009233  |
| La Rioja                   |          -0.08085 |              -0.05049  |              -2.682   |                      0.01634   |
| País Vasco                 |           0.5416  |              -0.04157  |               5.358   |                      0.01031   |
| Región de Murcia           |           0.1811  |               0.01273  |              -0.01036 |                     -0.02552   |

Dispersion de b2 individual: sd=0.063 (EE MG=0.016). Valencia: b1=-0.286 (EE 0.277), b2=0.049 (EE 0.016).

## 4c. C. Valenciana frente a Espana: crecimiento acumulado

Del trimestre inicial a 2026Q2 (IPV base 2025 y valor tasado MIVAU; Espana = `nacional_q`).

| periodo       | serie    |   crec_acum_CV_% |   crec_acum_Espana_% |   dif_pp |
|:--------------|:---------|-----------------:|---------------------:|---------:|
| 2014Q1-2026Q2 | ipv      |            95.88 |               109.9  |  -14.05  |
| 2014Q1-2026Q2 | p_tasado |            73.56 |                61.37 |   12.19  |
| 2021Q1-2026Q2 | ipv      |            59.17 |                56.35 |    2.819 |
| 2021Q1-2026Q2 | p_tasado |            58.53 |                44.89 |   13.64  |


## 5. Registro de busqueda y correccion para b2 (cuota extranjera)

Especificaciones registradas en `output/registro_busqueda_f5.csv`: **21**. Familia de 19 p-valores de b2 (distintas inferencias, tendencias, CCE, muestras, F conjunto de heterogeneidad) corregida por Holm y Bonferroni. Muy correlacionadas entre si, asi que ambas correcciones son conservadoras.

|                   |   p_sin_corregir |   p_Holm |   p_Bonferroni |
|:------------------|-----------------:|---------:|---------------:|
| A_FE_cl           |          0.8693  |   1      |         1      |
| A_FE_dk           |          0.9444  |   1      |         1      |
| A_FE_dk3          |          0.9387  |   1      |         1      |
| A_FE_wild         |          0.8713  |   1      |         1      |
| A_FE_trend        |          0.67    |   1      |         1      |
| A_CCE_MG          |          0.1075  |   1      |         1      |
| A_CCE_P           |          0.05165 |   0.8781 |         0.9814 |
| R_17CCAA_sin_term |          0.7202  |   1      |         1      |
| R_16CCAA_sin_term |          0.4733  |   1      |         1      |
| R_ptasado_main    |          0.03695 |   0.6651 |         0.7021 |
| R_ptasado_2003    |          0.5724  |   1      |         1      |
| H_C. Valenciana   |          0.8217  |   1      |         1      |
| H_Madrid          |          0.5902  |   1      |         1      |
| H_Cataluna        |          0.8554  |   1      |         1      |
| H_Baleares        |          0.5753  |   1      |         1      |
| H_Canarias        |          0.8403  |   1      |         1      |
| H_Andalucia       |          0.7267  |   1      |         1      |
| H_conjunto        |          0.01813 |   0.3444 |         0.3444 |
| H_F_wild          |          0.0809  |   1      |         1      |


## Problemas abiertos

- Extremadura sin `terminadas`: muestra principal de 16 CCAA; el robusto de 17 CCAA omite ese regresor.
- T=17, N=16: pocos clusters (el wild bootstrap es la referencia), Driscoll-Kraay y CCE por unidad con muy pocos grados de libertad; CIPS y poolability con potencia/tamano dudosos.
- Cuota extranjera a 1 de enero frente a IPV de media anual; poblacion trimestral interpolada y hasta 2025Q1.
- Endogeneidad (migracion y empleo responden al precio; terminadas retardadas no resuelve simultaneidad): todo es asociacion; ver IV de F3.
- Valor tasado y `p_bde` son la misma serie (decisiones.md): robusteces con ambas no independientes.
- rmse_oos no se calcula en el registro: los efectos de anio no son predecibles fuera de muestra.
