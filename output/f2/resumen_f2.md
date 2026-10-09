# Resumen F2 (nacional)

Lenguaje: asociaciones, sin identificación causal. Semilla 20261009. Total de especificaciones registradas: 1741 (de ellas 1728 de la búsqueda de corto plazo).

## P1. Ecuación final

**Largo plazo (DOLS ±2, HAC(4), N=72):** ln_ipv = -16.469 + 1.951[0.480]·ln_ocupados - 0.017[0.017]·tipo_hip + 0.059[0.045]·ln_permisos_l4 + 0.266[0.165]·ln_costes (EE HAC entre corchetes; dummies trimestrales incluidas).

**Corto plazo (preferido por R² ajustado, N=73):**

|                     |      coef |   EE_HAC |      t |         p |   p_Bonf(K) |    K |
|:--------------------|----------:|---------:|-------:|----------:|------------:|-----:|
| Intercept           |  0.0128   | 0.002764 |  4.633 | 3.601e-06 |   nan       |  nan |
| ect_l1              | -0.09679  | 0.0309   | -3.132 | 0.001736  |     1       | 1728 |
| q2                  | -0.006125 | 0.005038 | -1.216 | 0.2241    |   nan       |  nan |
| q3                  | -0.009226 | 0.00417  | -2.212 | 0.02694   |   nan       |  nan |
| q4                  | -0.02599  | 0.004899 | -5.306 | 1.123e-07 |   nan       |  nan |
| d_ln_ocupados       |  0.4736   | 0.1739   |  2.723 | 0.00646   |     1       |  576 |
| d_ln_costes         | -0.1047   | 0.05433  | -1.928 | 0.05387   |     1       |  864 |
| d_ln_renta_hog_real | -0.08782  | 0.08122  | -1.081 | 0.2796    |     1       |  864 |
| d_ln_ipv_l1         |  0.4421   | 0.113    |  3.914 | 9.07e-05  |     0.05225 |  576 |
| d_ln_credito_nuevo  |  0.04071  | 0.01297  |  3.14  | 0.001691  |     1       |  864 |


## 1. Raíces unitarias

ADF (AIC, maxlag 8; constante y constante+tendencia en niveles), KPSS (nivel y tendencia), Zivot-Andrews (maxlag 4). Regla: I(0) si ADF rechaza y KPSS no; I(1) si ADF no rechaza (c y ct), KPSS rechaza y la primera diferencia es estacionaria; resto 'ambigua'. Se ofrecen la muestra 2008Q1-2026Q2 y la muestra LARGA (todo lo disponible por serie; ln_p_tasado y ln_p_bde desde 1995).

| serie             | muestra       | rango         |   N | conclusion   |   adf_c_p |   adf_ct_p |   kpss_c_p |   kpss_ct_p |   za_p | za_quiebre   |
|:------------------|:--------------|:--------------|----:|:-------------|----------:|-----------:|-----------:|------------:|-------:|:-------------|
| ln_ipv            | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | ambigua      |     0.821 |      0.277 |      0.024 |       0.010 |  0.178 | 2014Q4       |
| ln_ipv            | larga         | 2007Q1-2026Q2 |  78 | ambigua      |     0.866 |      0.898 |      0.043 |       0.010 |  0.156 | 2010Q4       |
| ln_ipv_real       | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | ambigua      |     0.477 |      0.247 |      0.100 |       0.010 |  0.010 | 2015Q1       |
| ln_ipv_real       | larga         | 2007Q1-2026Q2 |  78 | ambigua      |     0.699 |      0.880 |      0.100 |       0.010 |  0.045 | 2011Q3       |
| ln_p_tasado       | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | ambigua      |     0.951 |      0.987 |      0.090 |       0.010 |  0.999 | 2022Q4       |
| ln_p_tasado       | larga         | 1995Q1-2026Q2 | 126 | I(1)         |     0.255 |      0.094 |      0.010 |       0.010 |  0.155 | 2000Q4       |
| ln_p_bde          | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | ambigua      |     0.951 |      0.987 |      0.090 |       0.010 |  0.999 | 2022Q4       |
| ln_p_bde          | larga         | 1995Q1-2026Q2 | 126 | I(1)         |     0.255 |      0.094 |      0.010 |       0.010 |  0.155 | 2000Q4       |
| ln_ocupados       | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | I(1)         |     0.936 |      0.480 |      0.010 |       0.010 |  0.291 | 2011Q4       |
| ln_ocupados       | larga         | 2002Q1-2026Q2 |  98 | I(1)         |     0.528 |      0.535 |      0.014 |       0.010 |  0.566 | 2011Q2       |
| tipo_hip          | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | ambigua      |     0.003 |      0.028 |      0.062 |       0.010 |  0.009 | 2022Q2       |
| tipo_hip          | larga         | 2003Q1-2026Q2 |  94 | I(1)         |     0.096 |      0.113 |      0.014 |       0.040 |  0.049 | 2008Q3       |
| tipo_hip_real     | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | I(1)         |     0.494 |      0.145 |      0.010 |       0.100 |  0.225 | 2021Q2       |
| tipo_hip_real     | larga         | 2003Q1-2026Q2 |  94 | I(1)         |     0.298 |      0.372 |      0.041 |       0.010 |  0.741 | 2007Q1       |
| ln_permisos       | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | I(1)         |     0.458 |      0.202 |      0.089 |       0.010 |  0.767 | 2012Q3       |
| ln_permisos       | larga         | 2000Q1-2026Q2 | 106 | I(1)         |     0.574 |      0.961 |      0.010 |       0.010 |  0.673 | 2007Q3       |
| ln_costes         | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | I(1)         |     0.982 |      0.955 |      0.010 |       0.010 |  0.019 | 2021Q1       |
| ln_costes         | larga         | 1995Q1-2026Q2 | 126 | I(1)         |     0.918 |      0.716 |      0.010 |       0.011 |  0.696 | 2014Q3       |
| ln_renta_hog_real | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | I(1)         |     0.984 |      0.776 |      0.010 |       0.010 |  0.502 | 2011Q4       |
| ln_renta_hog_real | larga         | 1999Q1-2026Q2 | 110 | I(1)         |     0.611 |      0.328 |      0.010 |       0.018 |  0.226 | 2011Q3       |
| ln_pob_extranj    | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | ambigua      |     0.785 |      0.339 |      0.019 |       0.010 |  0.047 | 2013Q1       |
| ln_pob_extranj    | larga         | 2002Q1-2026Q3 |  99 | I(1)         |     0.812 |      0.590 |      0.010 |       0.010 |  0.989 | 2013Q1       |
| ln_pob_total      | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | I(1)         |     0.997 |      0.943 |      0.010 |       0.010 |  0.849 | 2020Q4       |
| ln_pob_total      | larga         | 1995Q1-2026Q3 | 127 | I(1)         |     0.594 |      0.054 |      0.010 |       0.010 |  0.050 | 2001Q3       |
| ln_hogares_epa    | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | I(1)         |     0.922 |      0.719 |      0.010 |       0.035 |  0.829 | 2021Q3       |
| ln_hogares_epa    | larga         | 2002Q1-2026Q2 |  98 | ambigua      |     0.050 |      0.170 |      0.010 |       0.010 |  0.797 | 2006Q2       |
| ln_credito_nuevo  | 2008Q1-2026Q2 | 2008Q1-2026Q2 |  74 | ambigua      |     0.514 |      0.160 |      0.087 |       0.010 |  0.008 | 2010Q4       |
| ln_credito_nuevo  | larga         | 2003Q1-2026Q2 |  94 | I(1)         |     0.453 |      0.936 |      0.024 |       0.010 |  0.019 | 2010Q4       |



## 2. Réplica del punto de partida (2008Q1-2025Q4)

N exacto: LR 72 (2008Q1-2025Q4); ECM 72 (2008Q1-2025Q4). EE HAC(4). El ect de la réplica es el residuo del LR estático calculado también para 2007Q4 (los niveles existen), de ahí N=72 en el ECM. El punto de partida no reporta constante del ECM (aquí sí se estima).

**LR estático**

|                |   punto_partida |   replica |     EE_HAC |           p |
|:---------------|----------------:|----------:|-----------:|------------:|
| Intercept      |          -6.59  |  -7.181   |   2.432    |   0.003153  |
| ln_ocupados    |           0.878 |   0.8784  |   0.3133   |   0.005053  |
| tipo_hip       |          -0.042 |  -0.04181 |   0.008928 |   2.83e-06  |
| ln_permisos_l4 |           0.156 |   0.1564  |   0.02177  |   6.794e-13 |
| ln_costes      |           0.465 |   0.4652  |   0.1365   |   0.0006546 |
| R2_aj (LR)     |         nan     |   0.9477  | nan        | nan         |
| N (LR)         |          72     |  72       | nan        | nan         |

**ECM dos etapas**

|                  |   punto_partida |   sin_dum |    EE_sin |       p_sin |   con_dum |     EE_con |       p_con |
|:-----------------|----------------:|----------:|----------:|------------:|----------:|-----------:|------------:|
| d_ln_ocupados    |          0.686  |   0.6824  |   0.1967  |   0.0005221 |   0.6026  |   0.1962   |   0.00213   |
| d_tipo_hip       |         -0.0147 |  -0.01519 |   0.00442 |   0.0005911 |  -0.01387 |   0.004559 |   0.002348  |
| d_ln_permisos_l4 |          0.025  |   0.03032 |   0.01619 |   0.06104   |   0.02915 |   0.01238  |   0.01851   |
| d_ln_ipv_l1      |          0.254  |   0.3133  |   0.1019  |   0.002109  |   0.4159  |   0.106    |   8.732e-05 |
| d_ln_pob_extranj |          0.321  |   0.1629  |   0.1322  |   0.2177    |   0.09909 |   0.1194   |   0.4066    |
| ect_rep_l1       |         -0.1265 |  -0.1187  |   0.03109 |   0.0001353 |  -0.1095  |   0.02659  |   3.817e-05 |
| R2_aj            |          0.6    |   0.5902  | nan       | nan         |   0.6227  | nan        | nan         |
| N                |         72      |  72       | nan       | nan         |  72       | nan        | nan         |

Las pendientes del LR reproducen el punto de partida casi exactamente (0,878 / −0,042 / 0,156 / 0,465); solo cambia la constante (consistente con el rebase del IPV a base 2025 y de otros índices). En el ECM los coeficientes de ocupados, tipo, permisos y ect son próximos; la mayor diferencia es d_ln_pob_extranj (0,16 frente a 0,321 y no significativo), compatible con la revisión/interpolación de la población extranjera (ECP). Es una conjetura: no se dispone de la base del punto de partida para verificarlo. Con dummies el R² aj sube.



## 3. Cointegración (se reportan SIEMPRE los tres contrastes)

EG (statsmodels.coint, MacKinnon, AIC), Johansen (det_order=0, k_ar_diff por AIC del VAR/VECM ≤4, traza al 5 %; no admite dummies estacionales), ARDL bounds (caso 3, ardl_select_order AIC maxlag 4/orden de regresores ≤2, dummies trimestrales fijas; los regresores se fuerzan a orden ≥1 para el UECM). Decisión: ≥2 de 3 (docs/decisiones.md).

| sistema                                               |   N |    EG_p |   J_kardiff |   J_traza0 |   J_cv95 |   J_rango_traza |   J_rango_maxeig | ARDL_orden         |   ARDL_N |   ARDL_F |   ARDL_I1_5 |   n_rechazos | decision                          |
|:------------------------------------------------------|----:|--------:|------------:|-----------:|---------:|----------------:|-----------------:|:-------------------|---------:|---------:|------------:|-------------:|:----------------------------------|
| ln_ipv 2008Q1-2026Q2 (principal) / base               |  74 | 0.398   |           4 |      117   |     69.8 |               3 |                3 | (4, 2, 1, 0, 1)    |       70 |     3.85 |        3.79 |            2 | cointegración (2/3, discrepancia) |
| ln_ipv 2008Q1-2026Q2 (principal) / +pob_extranj       |  74 | 0.159   |           4 |      153   |     95.8 |               3 |                3 | (4, 0, 0, 0, 1)    |       70 |     3.88 |        3.79 |            2 | cointegración (2/3, discrepancia) |
| ln_ipv 2008Q1-2026Q2 (principal) / +renta             |  74 | 0.912   |           4 |      172   |     95.8 |               4 |                4 | (4, 2, 1, 0, 1)    |       70 |     3.85 |        3.79 |            2 | cointegración (2/3, discrepancia) |
| ln_ipv 2008Q1-2026Q2 (principal) / +pob_total         |  74 | 0.415   |           4 |      193   |     95.8 |               3 |                3 | (4, 0, 0, 0, 1, 1) |       70 |     7.47 |        3.63 |            2 | cointegración (2/3, discrepancia) |
| ln_ipv_real (tipo real, costes reales) / base         |  74 | 0.0227  |           4 |      133   |     69.8 |               3 |                3 | (4, 0, 0, 2)       |       70 |     2.67 |        4.01 |            2 | cointegración (2/3, discrepancia) |
| ln_ipv_real (tipo real, costes reales) / +pob_extranj |  74 | 0.0656  |           4 |      200   |     95.8 |               5 |                5 | (4, 0, 0, 2, 1)    |       70 |     3.54 |        3.79 |            1 | evidencia mixta (1/3)             |
| ln_ipv_real (tipo real, costes reales) / +renta       |  74 | 0.0345  |           4 |      198   |     95.8 |               4 |                3 | (4, 0, 0, 2)       |       70 |     2.67 |        4.01 |            2 | cointegración (2/3, discrepancia) |
| ln_ipv_real (tipo real, costes reales) / +pob_total   |  74 | 0.0453  |           4 |      224   |     95.8 |               4 |                3 | (4, 0, 0, 2, 1)    |       70 |     3.54 |        3.79 |            2 | cointegración (2/3, discrepancia) |
| ln_p_tasado 2003Q1-2026Q2 / base                      |  94 | 0.431   |           4 |       92.9 |     69.8 |               2 |                2 | (4, 1, 0, 0, 1)    |       90 |     2.79 |        3.79 |            1 | evidencia mixta (1/3)             |
| ln_p_tasado 2003Q1-2026Q2 / +pob_extranj              |  94 | 0.0211  |           4 |      148   |     95.8 |               6 |                2 | (4, 1, 0, 0, 1, 1) |       90 |     2.62 |        3.63 |            2 | cointegración (2/3, discrepancia) |
| ln_p_tasado 2003Q1-2026Q2 / +renta                    |  94 | 0.615   |           4 |      138   |     95.8 |               4 |                1 | (4, 1, 0, 0, 1)    |       90 |     2.79 |        3.79 |            1 | evidencia mixta (1/3)             |
| ln_p_tasado 2003Q1-2026Q2 / +pob_total                |  94 | 0.00342 |           4 |      137   |     95.8 |               4 |                1 | (4, 1, 0, 0, 1, 1) |       90 |     2.28 |        3.63 |            2 | cointegración (2/3, discrepancia) |
| ln_p_bde 2003Q1-2026Q2 / base                         |  94 | 0.431   |           4 |       92.9 |     69.8 |               2 |                2 | (4, 1, 0, 0, 1)    |       90 |     2.79 |        3.79 |            1 | evidencia mixta (1/3)             |
| ln_p_bde 2003Q1-2026Q2 / +pob_extranj                 |  94 | 0.0211  |           4 |      148   |     95.8 |               6 |                2 | (4, 1, 0, 0, 1, 1) |       90 |     2.62 |        3.63 |            2 | cointegración (2/3, discrepancia) |
| ln_p_bde 2003Q1-2026Q2 / +renta                       |  94 | 0.615   |           4 |      138   |     95.8 |               4 |                1 | (4, 1, 0, 0, 1)    |       90 |     2.79 |        3.79 |            1 | evidencia mixta (1/3)             |
| ln_p_bde 2003Q1-2026Q2 / +pob_total                   |  94 | 0.00342 |           4 |      137   |     95.8 |               4 |                1 | (4, 1, 0, 0, 1, 1) |       90 |     2.28 |        3.63 |            2 | cointegración (2/3, discrepancia) |



## 4. Largo plazo

DOLS ±2 con HAC(4) (estimador preferido, vector base con dummies trimestrales en la relación). Celdas: coef (EE HAC). Signos esperados de docs/literatura.md.

| var               | DOLS +pob_extranj   | DOLS +renta     | DOLS base (+q)   | DOLS base + epa21 + tipo22   | EG estático (+q)   | EG estático (const)   | UECM implícito (delta, HAC)   | signo_esperado   |
|:------------------|:--------------------|:----------------|:-----------------|:-----------------------------|:-------------------|:----------------------|:------------------------------|:-----------------|
| const             | -29.789 (2.257)     | -23.131 (4.271) | -16.469 (3.870)  | -19.316 (4.262)              | -7.010 (2.527)     | -7.038 (2.416)        | nan                           | nan              |
| ln_costes         | -0.913 (0.169)      | 0.005 (0.169)   | 0.266 (0.165)    | 0.320 (0.199)                | 0.513 (0.147)      | 0.511 (0.141)         | 1.244 (0.434)                 | +                |
| ln_ocupados       | 2.672 (0.294)       | 0.939 (0.478)   | 1.951 (0.480)    | 2.235 (0.481)                | 0.837 (0.327)      | 0.840 (0.312)         | 0.253 (0.906)                 | +                |
| ln_permisos_l4    | -0.005 (0.022)      | 0.068 (0.044)   | 0.059 (0.045)    | 0.011 (0.048)                | 0.163 (0.023)      | 0.163 (0.022)         | 0.223 (0.081)                 | -                |
| ln_pob_extranj    | 0.768 (0.146)       | nan             | nan              | nan                          | nan                | nan                   | nan                           | +                |
| ln_renta_hog_real | nan                 | 1.457 (0.388)   | nan              | nan                          | nan                | nan                   | nan                           | +                |
| tipo_hip          | -0.006 (0.009)      | 0.011 (0.020)   | -0.017 (0.017)   | -0.006 (0.019)               | -0.044 (0.009)     | -0.044 (0.009)        | -0.123 (0.037)                | -                |



## 5. Búsqueda de corto plazo (conjunto CERRADO, declarado antes de resultados)

**Siempre**: ect(t−1) del DOLS preferido (vector base con dummies trimestrales) + q2,q3,q4. **Candidatos** (cada variable con a lo sumo uno de sus retardos): d_ln_ocupados {0,1}; d_tipo_hip {0,1}; d_ln_permisos {t−4}; d_ln_costes {0}; d_ln_renta_hog_real {0}; inmigración {ninguna, d_ln_pob_extranj, d4_ln_pob_extranj/4, d_ln_pob_total} (alternativas excluyentes: nunca stock extranjero y población total a la vez); d_ln_ipv {1, 4}; d_ln_credito_nuevo {0}. Total de modelos enumerados: **1728** (más los modelos de réplica/LR/robustez del registro: 1737 filas en total al terminar la fase). Muestra común: 2008Q2-2026Q2, **N=73** (límite: d_ln_ipv(t−4)). Criterio principal: R² ajustado (como el punto de partida), corregido por la búsqueda (Bonferroni con K = modelos que contienen el término y bootstrap de la selección). También se reportan AIC y BIC. Asociaciones, no causalidad.

**Ganadores (misma muestra)**

| criterio                | id        | terminos                                                                             |   N |   R2_aj |     AIC |     BIC |   RMSE_OOS |
|:------------------------|:----------|:-------------------------------------------------------------------------------------|----:|--------:|--------:|--------:|-----------:|
| R2 ajustado (principal) | busq_0652 | d_ln_ocupados + d_ln_costes + d_ln_renta_hog_real + d_ln_ipv_l1 + d_ln_credito_nuevo |  73 | 0.74853 | -440.42 | -417.52 |   0.013168 |
| AIC                     | busq_0580 | d_ln_ocupados + d_ln_ipv_l1 + d_ln_credito_nuevo                                     |  73 | 0.74767 | -441.89 | -423.57 |   0.013121 |
| BIC                     | busq_0580 | d_ln_ocupados + d_ln_ipv_l1 + d_ln_credito_nuevo                                     |  73 | 0.74767 | -441.89 | -423.57 |   0.013121 |
| RMSE OOS                | busq_0196 | d_tipo_hip + d_ln_ipv_l1 + d_ln_credito_nuevo                                        |  73 | 0.71908 | -434.06 | -415.73 |   0.011774 |
| vacío (ect+dummies)     | busq_0001 | (vacío)                                                                              |  73 | 0.44964 | -387.67 | -376.22 |   0.019588 |

**Correlación stock extranjeros vs población total**

|   corr_niveles(ln_pob_extranj, ln_pob_total) |   corr_dif(d_ln_pob_extranj, d_ln_pob_total) |   corr_dif(d_ln_pob_extranj4, d_ln_pob_total) |
|---------------------------------------------:|---------------------------------------------:|----------------------------------------------:|
|                                        0.874 |                                        0.887 |                                         0.851 |

**EBA y Bonferroni/Holm (K = nº de modelos con el término)**

| termino             |   K_modelos |   frac_signif_5pct |   signo_pos |   coef_min |   coef_max |   Leamer_inf |   Leamer_sup |   coef_pref |   EE_pref |     p_pref |   p_bonf_K |   p_holm_K | robusto_EBA(Leamer no cruza 0)   |
|:--------------------|------------:|-------------------:|------------:|-----------:|-----------:|-------------:|-------------:|------------:|----------:|-----------:|-----------:|-----------:|:---------------------------------|
| ect_l1              |        1728 |             1      |       0     |    -0.252  |  -0.0817   |     -0.36    |     -0.00252 |     -0.0968 |    0.0309 |   0.00174  |     1      |     1      | True                             |
| d_ln_ocupados       |         576 |             0.988  |       1     |     0.334  |   0.974    |     -0.0271  |      1.67    |      0.474  |    0.174  |   0.00646  |     1      |     1      | False                            |
| d_ln_ocupados_l1    |         576 |             0.361  |       1     |     0.0483 |   0.656    |     -0.499   |      1.28    |    nan      |  nan      | nan        |   nan      |   nan      | False                            |
| d_tipo_hip          |         576 |             0.245  |       0.203 |    -0.0127 |   0.00555  |     -0.0226  |      0.0186  |    nan      |  nan      | nan        |   nan      |   nan      | False                            |
| d_tipo_hip_l1       |         576 |             0.667  |       0     |    -0.0146 |  -0.000662 |     -0.0243  |      0.00516 |    nan      |  nan      | nan        |   nan      |   nan      | False                            |
| d_ln_permisos_l4    |         864 |             0      |       0.848 |    -0.0116 |   0.0267   |     -0.0369  |      0.0675  |    nan      |  nan      | nan        |   nan      |   nan      | False                            |
| d_ln_costes         |         864 |             0.0787 |       0.473 |    -0.178  |   0.155    |     -0.329   |      0.336   |     -0.105  |    0.0543 |   0.0539   |     1      |     1      | False                            |
| d_ln_renta_hog_real |         864 |             0.361  |       0.667 |    -0.157  |   0.303    |     -0.432   |      0.473   |     -0.0878 |    0.0812 |   0.28     |     1      |     1      | False                            |
| d_ln_pob_extranj    |         432 |             0.134  |       0.4   |    -0.568  |   0.284    |     -0.977   |      0.636   |    nan      |  nan      | nan        |   nan      |   nan      | False                            |
| d_ln_pob_extranj4   |         432 |             0.13   |       0.412 |    -0.527  |   0.201    |     -0.926   |      0.6     |    nan      |  nan      | nan        |   nan      |   nan      | False                            |
| d_ln_pob_total      |         432 |             0      |       0.484 |    -3.47   |   2.48     |     -7.24    |      6.14    |    nan      |  nan      | nan        |   nan      |   nan      | False                            |
| d_ln_ipv_l1         |         576 |             1      |       1     |     0.286  |   0.532    |      0.0656  |      0.758   |      0.442  |    0.113  |   9.07e-05 |     0.0522 |     0.0522 | True                             |
| d_ln_ipv_l4         |         576 |             1      |       1     |     0.28   |   0.586    |      0.00684 |      0.914   |    nan      |  nan      | nan        |   nan      |   nan      | True                             |
| d_ln_credito_nuevo  |         864 |             1      |       1     |     0.0271 |   0.0501   |      0.00689 |      0.0785  |      0.0407 |    0.013  |   0.00169  |     1      |     1      | True                             |

**Bootstrap de la selección** (bloques móviles de 8, B=999, semilla 20261009; se re-ejecuta TODA la búsqueda en cada réplica por R² aj; el ect se mantiene fijo, es regresor generado: limitación). El modelo preferido original vuelve a ser ganador en 1.5% de las réplicas.

| termino             |   frec_en_ganador |   coef_post_med |   IC95_inf |   IC95_sup |   n_rep_condicional |
|:--------------------|------------------:|----------------:|-----------:|-----------:|--------------------:|
| ect_l1              |             1     |        -0.104   |    -0.297  |   0.000386 |                 999 |
| d_ln_ocupados       |             0.755 |         0.567   |     0.212  |   2        |                 754 |
| d_ln_ocupados_l1    |             0.238 |         0.351   |     0.142  |   1.83     |                 238 |
| d_tipo_hip          |             0.309 |        -0.0119  |    -0.0295 |   0.0133   |                 309 |
| d_tipo_hip_l1       |             0.397 |        -0.00871 |    -0.0322 |   0.0209   |                 397 |
| d_ln_permisos_l4    |             0.216 |         0.0116  |    -0.0373 |   0.0398   |                 216 |
| d_ln_costes         |             0.406 |        -0.0862  |    -0.231  |   0.352    |                 406 |
| d_ln_renta_hog_real |             0.589 |        -0.113   |    -0.293  |   0.282    |                 588 |
| d_ln_pob_extranj    |             0.101 |        -0.233   |    -0.52   |   0.416    |                 101 |
| d_ln_pob_extranj4   |             0.171 |        -0.215   |    -0.634  |   0.699    |                 171 |
| d_ln_pob_total      |             0.397 |         2.22    |    -5.87   |   6.07     |                 397 |
| d_ln_ipv_l1         |             0.624 |         0.362   |    -0.186  |   0.617    |                 623 |
| d_ln_ipv_l4         |             0.291 |         0.221   |    -0.197  |   0.514    |                 291 |
| d_ln_credito_nuevo  |             0.947 |         0.0381  |     0.0114 |   0.0712   |                 946 |

Modelos más frecuentes como ganadores:

| modelo    | terminos                                                                                   |   frec_ganador |
|:----------|:-------------------------------------------------------------------------------------------|---------------:|
| busq_0604 | d_ln_ocupados + d_ln_renta_hog_real + d_ln_ipv_l1 + d_ln_credito_nuevo                     |          0.037 |
| busq_1564 | d_ln_ocupados_l1 + d_tipo_hip_l1 + d_ln_renta_hog_real + d_ln_ipv_l1 + d_ln_credito_nuevo  |          0.026 |
| busq_0622 | d_ln_ocupados + d_ln_renta_hog_real + d_ln_pob_total + d_ln_ipv_l1 + d_ln_credito_nuevo    |          0.023 |
| busq_1180 | d_ln_ocupados_l1 + d_ln_renta_hog_real + d_ln_ipv_l1 + d_ln_credito_nuevo                  |          0.021 |
| busq_0618 | d_ln_ocupados + d_ln_renta_hog_real + d_ln_pob_extranj4 + d_ln_ipv_l4 + d_ln_credito_nuevo |          0.018 |



## 5b. Fuera de muestra

Ventana expansiva, 1 paso, 2018Q1-2026Q2 (34 predicciones). En cada origen el LARGO PLAZO (DOLS y ect) se re-estima solo con datos hasta t−1 (los adelantos obligan a terminar la muestra del DOLS en t−3); los regresores contemporáneos del ECM se toman observados (predicción condicional). Referencias: AR(4)+dummies, media histórica expansiva de d_ln_ipv y paseo con deriva (deriva = media de los últimos 20 trimestres; con deriva estimada en ventana expansiva coincidiría con la media histórica). DM: HAC(h−1=0) con corrección HLN; DM<0 favorece al modelo.

| modelo                       |    RMSE |   n_oos |   DM vs AR4+q |   p vs AR4+q |   DM vs media historica |   p vs media historica |   DM vs paseo con deriva (20T) |   p vs paseo con deriva (20T) |
|:-----------------------------|--------:|--------:|--------------:|-------------:|------------------------:|-----------------------:|-------------------------------:|------------------------------:|
| Preferido (R2aj)             | 0.01317 |      34 |       1.076   |    0.2899    |                  -4.06  |              0.0002834 |                       -0.01912 |                      0.9849   |
| Ganador BIC                  | 0.01312 |      34 |       1.04    |    0.306     |                  -4.104 |              0.0002504 |                       -0.04679 |                      0.963    |
| Ganador AIC                  | 0.01312 |      34 |       1.04    |    0.306     |                  -4.104 |              0.0002504 |                       -0.04679 |                      0.963    |
| Mejor RMSE OOS               | 0.01177 |      34 |       0.05891 |    0.9534    |                  -5.264 |              8.461e-06 |                       -1.042   |                      0.3051   |
| Vacío (ect+q)                | 0.01959 |      34 |       3.941   |    0.0003977 |                  -1.493 |              0.1449    |                        3.207   |                      0.002979 |
| [ref] AR4+q                  | 0.01171 |      34 |     nan       |  nan         |                 nan     |            nan         |                      nan       |                    nan        |
| [ref] media historica        | 0.02195 |      34 |     nan       |  nan         |                 nan     |            nan         |                      nan       |                    nan        |
| [ref] paseo con deriva (20T) | 0.0132  |      34 |     nan       |  nan         |                 nan     |            nan         |                      nan       |                    nan        |



## 6. Diagnósticos

Contrastes sobre MCO clásico (los EE de los coeficientes son HAC). DW, BG(4) p, BP p, JB p, RESET p (potencias 2-3), CUSUM p, VIF máx (sin dummies q).

|                     |   n |   k |    DW |    BG4_p |   BP_p |     JB_p |   RESET_p |   CUSUM_p |   VIF_max |
|:--------------------|----:|----:|------:|---------:|-------:|---------:|----------:|----------:|----------:|
| Réplica ECM sin q   |  72 |   7 | 2.3   | 0.0289   |  0.462 | 0.0159   |   0.648   |   0.192   |      1.58 |
| Réplica ECM con q   |  72 |  10 | 2.6   | 0.000822 |  0.689 | 3.74e-10 |   0.229   |   0.252   |      1.58 |
| Réplica LR estático |  72 |   5 | 0.33  | 1.03e-15 |  0.303 | 0.0472   |   0.0217  |   0.00391 |      7.54 |
| Preferido (R2aj)    |  73 |  10 | 2.23  | 0.113    |  0.887 | 0.334    |   0.0281  |   0.562   |      2.14 |
| Ganador BIC         |  73 |   8 | 2.29  | 0.0684   |  0.916 | 0.305    |   0.0167  |   0.531   |      1.9  |
| Ganador AIC         |  73 |   8 | 2.29  | 0.0684   |  0.916 | 0.305    |   0.0167  |   0.531   |      1.9  |
| DOLS base (LR)      |  72 |  28 | 0.712 | 1.99e-06 |  0.166 | 0.42     |   0.00368 |   0.288   |     50.6  |
| Preferido pre-COVID |  47 |  10 | 2.01  | 0.0146   |  0.861 | 0.667    |   0.0529  |   0.225   |      1.88 |

**Breusch-Godfrey: añadir retardos de d_ln_ipv**

| paso      | terminos_extra   |   BG4_p |   DW |
|:----------|:-----------------|--------:|-----:|
| preferido |                  |  0.1133 | 2.23 |

**Chow (ECM preferido)**

| fecha   |     F |       p |   n1 |   n2 |   k |
|:--------|------:|--------:|-----:|-----:|----:|
| 2014Q1  | 2.596 | 0.01214 |   23 |   50 |  10 |
| 2020Q1  | 1.628 | 0.124   |   47 |   26 |  10 |
| 2022Q3  | 1.103 | 0.3774  |   57 |   16 |  10 |

**Bai-Perron (min 12, máx 3, BIC; dummies q partialled out)**

| ecuacion                             |   N |   n_quiebres | fechas                 | bic                                                                                          |
|:-------------------------------------|----:|-------------:|:-----------------------|:---------------------------------------------------------------------------------------------|
| ECM preferido                        |  73 |            0 |                        | {0: np.float64(-637.6), 1: np.float64(-627.8), 2: np.float64(-632.9), 3: np.float64(-631.5)} |
| LR (niveles, DOLS base sin retardos) |  74 |            3 | 2012Q1, 2020Q2, 2023Q2 | {0: np.float64(-457.8), 1: np.float64(-510.6), 2: np.float64(-542.1), 3: np.float64(-565.9)} |

Figuras: output/f2/cusum.png, output/f2/ect_recursivo.png.

**Robustez: escalones y pre-COVID**

| modelo                                    |   N | ect              |     p_ect |   R2_aj |   BG4_p |   BP_p |   JB_p |   RESET_p | extras                                                                                    |
|:------------------------------------------|----:|:-----------------|----------:|--------:|--------:|-------:|-------:|----------:|:------------------------------------------------------------------------------------------|
| Preferido                                 |  73 | -0.0968 (0.0309) | 0.001736  |  0.7485 | 0.1133  | 0.8875 | 0.3342 |  0.02806  |                                                                                           |
| + epa21 + tipo22 (escalones)              |  73 | -0.0849 (0.0316) | 0.007196  |  0.755  | 0.1687  | 0.8629 | 0.5817 |  0.01898  | epa21=0.0078 (0.0027); tipo22=-0.0019 (0.0045)                                            |
| + escalones Bai-Perron (ECM y LR)         |  73 | -0.1302 (0.0376) | 0.0005398 |  0.7678 | 0.4754  | 0.9164 | 0.9152 |  0.006727 | esc_2012Q1=-0.0102 (0.0050); esc_2020Q2=0.0049 (0.0028); esc_2023Q2=0.0032 (0.0043)       |
| Pre-COVID (hasta 2019Q4; ect re-estimado) |  47 | -0.0536 (0.0250) | 0.03245   |  0.7036 | 0.01462 | 0.8612 | 0.6668 |  0.05294  | LR pre-COVID: ln_ocupados=2.518; tipo_hip=-0.028; ln_permisos_l4=-0.027; ln_costes=-0.418 |

Los escalones se usan solo como robustez: en una ecuación en diferencias un escalón equivale a un cambio de deriva, y con tramos de 12-16 trimestres la potencia del Chow es baja.



## 7. Problemas abiertos

- El ECM preferido rechaza RESET_p (p=0.028).
- La réplica ECM (con q) rechaza BG4_p (p=0.001).
- La réplica ECM (con q) rechaza JB_p (p=0.000).
- Cointegración del vector base: cointegración (2/3, discrepancia); los tres contrastes no concuerdan.
- El coeficiente del ect no sobrevive a Bonferroni con K=nº total de modelos.
- Inestabilidad de la selección: el preferido gana solo en 1.5% de las réplicas bootstrap.
- ln_p_tasado y ln_p_bde son idénticas en nacional_q (diferencia máx. 0): los dos sistemas de robustez no son independientes.
- Johansen rechaza rangos altos en todos los sistemas (traza con 5-6 variables y N≈74): probable sobre-rechazo en muestra pequeña; EG y ARDL discrepan.
- Bonferroni con K=1728 deja casi todo no significativo (solo d_ln_ipv_l1 se acerca); la significación del ECM preferido es en gran parte fruto de la búsqueda.
- El preferido por R² aj gana en <2 % de réplicas bootstrap: la selección es inestable; solo ect y d_ln_credito_nuevo/d_ln_ocupados entran de forma estable.
- El ect del ECM es un regresor generado (DOLS estimado en la misma muestra); no se corrige su incertidumbre. En el bootstrap se mantiene fijo.
- Johansen sin dummies estacionales (limitación de coint_johansen); EG/ARDL sí las admiten en ARDL.
- Población extranjera interpolada log-lineal antes de 2021 (MA mecánica en Δ1); d4/4 como contraste.
- Chow 2022Q3 y Bai-Perron con tramos cortos: baja potencia; los escalones son solo robustez.
- OOS con regresores contemporáneos observados (predicción condicional); el LR sí se re-estima sin ver el futuro.
- IPV no desestacionalizado; las dummies absorben solo estacionalidad determinista.
