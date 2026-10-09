# Resumen F2 (nacional)

Lenguaje: asociaciones, sin identificación causal. Semilla 20261009. Filas del registro de la fase: 1748 (de ellas 1728 de la búsqueda de corto plazo).

## P1. Ecuación final

**Estado de la relación de largo plazo.** Vector nominal principal: EG p=0.398, Johansen traza (r≥1: True), ARDL bounds F=3.25 (I0/I1 5 % = 2.88/4.01, k=4; no concluyente) → 1/3: **evidencia mixta (1/3)**. Vector en precio real: EG p=0.023, ARDL F=7.20 (I1 5 % = 4.01) → 3/3: **cointegración (3/3)**. La significatividad del coeficiente del ect (t≈−3,1) NO contrasta cointegración: bajo la nula de no cointegración su distribución no es normal ni t, y los valores críticos son más negativos que −1,96 (contrastes de tipo Banerjee-Dolado-Mestre, referencia propuesta por el revisor, aún sin añadir a la literatura verificada). El ECM se presenta por tanto como un modelo condicional con término de desequilibrio respecto a una relación de nivel NO confirmada, e inestable (Bai-Perron en niveles: 3 quiebres; pre-COVID: costes y permisos cambian de signo). Se interpreta como reversión parcial hacia una tendencia común inestable.

**Largo plazo (DOLS ±2, HAC(4), N=72; estado: evidencia mixta/inestable, no usar como estimación puntual fiable):** ln_ipv = -16.469 + 1.951[0.480]·ln_ocupados - 0.017[0.017]·tipo_hip + 0.059[0.045]·ln_permisos_l4 + 0.266[0.165]·ln_costes (EE HAC entre corchetes; dummies trimestrales incluidas).

**Corto plazo (preferido por R² ajustado, N=73; ecuación condicional, selección inestable):**

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

La especificación concreta no está identificada (gana en 1.5% de las réplicas bootstrap). Términos sostenibles como asociación: empleo (en t o t−1: 99% de las réplicas), persistencia de Δprecio (91%) y crédito contemporáneo (95%), este último solo como comovimiento (ver 6c). El ect está forzado en todos los modelos, así que su frecuencia no es informativa.


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

EG (statsmodels.coint, MacKinnon, AIC), Johansen (det_order=0, k_ar_diff por AIC del VAR/VECM ≤4, traza al 5 %; no admite dummies estacionales), ARDL bounds (caso 3; ardl_select_order AIC maxlag 4/orden ≤2 con dummies trimestrales fijas; órdenes asignados por NOMBRE de variable y regresores excluidos forzados a orden 1; F de Wald propio sobre y.L1 y x.L1 en el UECM CON dummies (bounds_test de statsmodels las descarta) y valores críticos PSS caso III con k = nº de regresores x, sin la dependiente). Decisión: ≥2 de 3 (docs/decisiones.md).

| sistema                                               |   N |    EG_p |   J_kardiff |   J_traza0 |   J_cv95 |   J_rango_traza |   J_rango_maxeig |   ARDL_p | ARDL_ordenes_x                                                                                           |   ARDL_N |   ARDL_k |   ARDL_F |   ARDL_I0_5 |   ARDL_I1_5 |   ARDL_t_yL1 | ARDL_zona      |   n_rechazos | decision                          |
|:------------------------------------------------------|----:|--------:|------------:|-----------:|---------:|----------------:|-----------------:|---------:|:---------------------------------------------------------------------------------------------------------|---------:|---------:|---------:|------------:|------------:|-------------:|:---------------|-------------:|:----------------------------------|
| ln_ipv 2008Q1-2026Q2 (principal) / base               |  74 | 0.398   |           4 |      117   |     69.8 |               3 |                3 |        4 | {'ln_ocupados': 2, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1}                                   |       70 |        4 |     3.25 |        2.88 |        4.01 |        -2.35 | no concluyente |            1 | evidencia mixta (1/3)             |
| ln_ipv 2008Q1-2026Q2 (principal) / +pob_extranj       |  74 | 0.159   |           4 |      153   |     95.8 |               3 |                3 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_pob_extranj': 1}              |       70 |        5 |     6.52 |        2.64 |        3.79 |        -2.87 | rechaza (F>I1) |            2 | cointegración (2/3, discrepancia) |
| ln_ipv 2008Q1-2026Q2 (principal) / +renta             |  74 | 0.912   |           4 |      172   |     95.8 |               4 |                4 |        4 | {'ln_ocupados': 2, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_renta_hog_real': 1}           |       70 |        5 |     2.64 |        2.64 |        3.79 |        -2.26 | no concluyente |            1 | evidencia mixta (1/3)             |
| ln_ipv 2008Q1-2026Q2 (principal) / +pob_total         |  74 | 0.415   |           4 |      193   |     95.8 |               3 |                3 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_pob_total': 1}                |       70 |        5 |     5.12 |        2.64 |        3.79 |        -3.05 | rechaza (F>I1) |            2 | cointegración (2/3, discrepancia) |
| ln_ipv_real (tipo real, costes reales) / base         |  74 | 0.0227  |           4 |      133   |     69.8 |               3 |                3 |        4 | {'ln_ocupados': 1, 'tipo_hip_real': 1, 'ln_permisos_l4': 1, 'ln_costes_real': 2}                         |       70 |        4 |     7.2  |        2.88 |        4.01 |        -5.19 | rechaza (F>I1) |            3 | cointegración (3/3)               |
| ln_ipv_real (tipo real, costes reales) / +pob_extranj |  74 | 0.0656  |           4 |      200   |     95.8 |               5 |                5 |        4 | {'ln_ocupados': 1, 'tipo_hip_real': 1, 'ln_permisos_l4': 1, 'ln_costes_real': 2, 'ln_pob_extranj': 1}    |       70 |        5 |     6.78 |        2.64 |        3.79 |        -4.59 | rechaza (F>I1) |            2 | cointegración (2/3, discrepancia) |
| ln_ipv_real (tipo real, costes reales) / +renta       |  74 | 0.0345  |           4 |      198   |     95.8 |               4 |                3 |        4 | {'ln_ocupados': 1, 'tipo_hip_real': 1, 'ln_permisos_l4': 1, 'ln_costes_real': 2, 'ln_renta_hog_real': 1} |       70 |        5 |     6.2  |        2.64 |        3.79 |        -5.2  | rechaza (F>I1) |            3 | cointegración (3/3)               |
| ln_ipv_real (tipo real, costes reales) / +pob_total   |  74 | 0.0453  |           4 |      224   |     95.8 |               4 |                3 |        4 | {'ln_ocupados': 1, 'tipo_hip_real': 1, 'ln_permisos_l4': 1, 'ln_costes_real': 2, 'ln_pob_total': 1}      |       70 |        5 |     6.79 |        2.64 |        3.79 |        -4.85 | rechaza (F>I1) |            3 | cointegración (3/3)               |
| ln_p_tasado 2003Q1-2026Q2 / base                      |  94 | 0.431   |           4 |       92.9 |     69.8 |               2 |                2 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1}                                   |       90 |        4 |     3.3  |        2.88 |        4.01 |        -2.83 | no concluyente |            1 | evidencia mixta (1/3)             |
| ln_p_tasado 2003Q1-2026Q2 / +pob_extranj              |  94 | 0.0211  |           4 |      148   |     95.8 |               6 |                2 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_pob_extranj': 1}              |       90 |        5 |     4.24 |        2.64 |        3.79 |        -2.37 | rechaza (F>I1) |            3 | cointegración (3/3)               |
| ln_p_tasado 2003Q1-2026Q2 / +renta                    |  94 | 0.615   |           4 |      138   |     95.8 |               4 |                1 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_renta_hog_real': 1}           |       90 |        5 |     2.69 |        2.64 |        3.79 |        -2.79 | no concluyente |            1 | evidencia mixta (1/3)             |
| ln_p_tasado 2003Q1-2026Q2 / +pob_total                |  94 | 0.00342 |           4 |      137   |     95.8 |               4 |                1 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_pob_total': 1}                |       90 |        5 |     3.31 |        2.64 |        3.79 |        -2.74 | no concluyente |            2 | cointegración (2/3, discrepancia) |
| ln_p_bde 2003Q1-2026Q2 / base                         |  94 | 0.431   |           4 |       92.9 |     69.8 |               2 |                2 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1}                                   |       90 |        4 |     3.3  |        2.88 |        4.01 |        -2.83 | no concluyente |            1 | evidencia mixta (1/3)             |
| ln_p_bde 2003Q1-2026Q2 / +pob_extranj                 |  94 | 0.0211  |           4 |      148   |     95.8 |               6 |                2 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_pob_extranj': 1}              |       90 |        5 |     4.24 |        2.64 |        3.79 |        -2.37 | rechaza (F>I1) |            3 | cointegración (3/3)               |
| ln_p_bde 2003Q1-2026Q2 / +renta                       |  94 | 0.615   |           4 |      138   |     95.8 |               4 |                1 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_renta_hog_real': 1}           |       90 |        5 |     2.69 |        2.64 |        3.79 |        -2.79 | no concluyente |            1 | evidencia mixta (1/3)             |
| ln_p_bde 2003Q1-2026Q2 / +pob_total                   |  94 | 0.00342 |           4 |      137   |     95.8 |               4 |                1 |        4 | {'ln_ocupados': 1, 'tipo_hip': 1, 'ln_permisos_l4': 1, 'ln_costes': 1, 'ln_pob_total': 1}                |       90 |        5 |     3.31 |        2.64 |        3.79 |        -2.74 | no concluyente |            2 | cointegración (2/3, discrepancia) |



## 4. Largo plazo

DOLS ±2 con HAC(4) (estimador preferido, vector base con dummies trimestrales en la relación). Celdas: coef (EE HAC). Signos esperados de docs/literatura.md.

| var               | DOLS +pob_extranj   | DOLS +renta     | DOLS base (+q)   | DOLS base + epa21 + tipo22   | EG estático (+q)   | EG estático (const)   | UECM implícito (delta, EE clásicos)   | signo_esperado   |
|:------------------|:--------------------|:----------------|:-----------------|:-----------------------------|:-------------------|:----------------------|:--------------------------------------|:-----------------|
| const             | -29.789 (2.257)     | -23.131 (4.271) | -16.469 (3.870)  | -19.316 (4.262)              | -7.010 (2.527)     | -7.038 (2.416)        | nan                                   | nan              |
| ln_costes         | -0.913 (0.169)      | 0.005 (0.169)   | 0.266 (0.165)    | 0.320 (0.199)                | 0.513 (0.147)      | 0.511 (0.141)         | 1.244 (0.611)                         | +                |
| ln_ocupados       | 2.672 (0.294)       | 0.939 (0.478)   | 1.951 (0.480)    | 2.235 (0.481)                | 0.837 (0.327)      | 0.840 (0.312)         | 0.253 (1.098)                         | +                |
| ln_permisos_l4    | -0.005 (0.022)      | 0.068 (0.044)   | 0.059 (0.045)    | 0.011 (0.048)                | 0.163 (0.023)      | 0.163 (0.022)         | 0.223 (0.084)                         | -                |
| ln_pob_extranj    | 0.768 (0.146)       | nan             | nan              | nan                          | nan                | nan                   | nan                                   | +                |
| ln_renta_hog_real | nan                 | 1.457 (0.388)   | nan              | nan                          | nan                | nan                   | nan                                   | +                |
| tipo_hip          | -0.006 (0.009)      | 0.011 (0.020)   | -0.017 (0.017)   | -0.006 (0.019)               | -0.044 (0.009)     | -0.044 (0.009)        | -0.123 (0.057)                        | -                |



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

**Salvedades.** (i) La especificación preferida (y los ganadores AIC/BIC) se eligió con la muestra COMPLETA, incluidos 2018-2026: la selección no es en tiempo real y el OOS es pseudo-OOS (favorece al modelo). (ii) La fila «Mejor RMSE OOS» se elige con los propios errores fuera de muestra: es un óptimo ex post, no evidencia predictiva. (iii) Crédito y empleo contemporáneos entran observados (predicción condicional sobre regresores simultáneos). (iv) Resultado: el preferido NO mejora al AR(4)+dummies ni al paseo con deriva (DM no significativos); solo bate a la media histórica.

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

**Breusch-Godfrey: añadir retardos de d_ln_ipv (preferido)**

| paso      | terminos_extra   |   BG4_p |   DW |
|:----------|:-----------------|--------:|-----:|
| preferido |                  |  0.1133 | 2.23 |

(La versión pre-COVID sí rechaza BG(4), p=0.015; no se ha aplicado el aumento de retardos allí.)



## 6b. Quiebres y estabilidad (P5: 2008, 2014, 2020, 2022)

**Chow (ECM preferido)**

| fecha   |     F |       p |   n1 |   n2 |   k |
|:--------|------:|--------:|-----:|-----:|----:|
| 2014Q1  | 2.596 | 0.01214 |   23 |   50 |  10 |
| 2020Q1  | 1.628 | 0.124   |   47 |   26 |  10 |
| 2022Q3  | 1.103 | 0.3774  |   57 |   16 |  10 |

**Bai-Perron (min 12, máx 3, BIC; dummies q eliminadas por partialling)**

| ecuacion                             |   N |   n_quiebres | fechas                 | bic                                                                                          |
|:-------------------------------------|----:|-------------:|:-----------------------|:---------------------------------------------------------------------------------------------|
| ECM preferido                        |  73 |            0 |                        | {0: np.float64(-637.6), 1: np.float64(-627.8), 2: np.float64(-632.9), 3: np.float64(-631.5)} |
| LR (niveles, DOLS base sin retardos) |  74 |            3 | 2012Q1, 2020Q2, 2023Q2 | {0: np.float64(-457.8), 1: np.float64(-510.6), 2: np.float64(-542.1), 3: np.float64(-565.9)} |

**Estabilidad del ECM preferido por muestras**

| muestra                               |   N |   R2_aj | ect_l1           | d_ln_ocupados   | d_ln_costes      | d_ln_renta_hog_real   | d_ln_ipv_l1     | d_ln_credito_nuevo   |
|:--------------------------------------|----:|--------:|:-----------------|:----------------|:-----------------|:----------------------|:----------------|:---------------------|
| 2008Q2-2026Q2 (completa)              |  73 |  0.7485 | -0.0968 (0.0309) | 0.4736 (0.1739) | -0.1047 (0.0543) | -0.0878 (0.0812)      | 0.4421 (0.1130) | 0.0407 (0.0130)      |
| 2014Q1-2026Q2                         |  50 |  0.4743 | -0.0679 (0.0445) | 0.3590 (0.1288) | -0.0714 (0.0515) | 0.0374 (0.0876)       | 0.4252 (0.2135) | -0.0014 (0.0094)     |
| 2008Q2-2019Q4 (pre-COVID, ect reest.) |  47 |  0.7036 | -0.0536 (0.0250) | 0.7443 (0.3788) | 0.1070 (0.1637)  | -0.1169 (0.1331)      | 0.2614 (0.1564) | 0.0362 (0.0138)      |

**Robustez: escalones y pre-COVID**

| modelo                                    |   N | ect              |     p_ect |   R2_aj |   BG4_p |   BP_p |   JB_p |   RESET_p | extras                                                                                    |
|:------------------------------------------|----:|:-----------------|----------:|--------:|--------:|-------:|-------:|----------:|:------------------------------------------------------------------------------------------|
| Preferido                                 |  73 | -0.0968 (0.0309) | 0.001736  |  0.7485 | 0.1133  | 0.8875 | 0.3342 |  0.02806  |                                                                                           |
| + epa21 + tipo22 (escalones)              |  73 | -0.0849 (0.0316) | 0.007196  |  0.755  | 0.1687  | 0.8629 | 0.5817 |  0.01898  | epa21=0.0078 (0.0027); tipo22=-0.0019 (0.0045)                                            |
| + escalones Bai-Perron (ECM y LR)         |  73 | -0.1302 (0.0376) | 0.0005398 |  0.7678 | 0.4754  | 0.9164 | 0.9152 |  0.006727 | esc_2012Q1=-0.0102 (0.0050); esc_2020Q2=0.0049 (0.0028); esc_2023Q2=0.0032 (0.0043)       |
| Pre-COVID (hasta 2019Q4; ect re-estimado) |  47 | -0.0536 (0.0250) | 0.03245   |  0.7036 | 0.01462 | 0.8612 | 0.6668 |  0.05294  | LR pre-COVID: ln_ocupados=2.518; tipo_hip=-0.028; ln_permisos_l4=-0.027; ln_costes=-0.418 |

**DOLS / EG por subperíodos** (DOLS ±1 por grados de libertad)

| subperiodo                             | var            | DOLS_k1          |   N_DOLS | EG_q             |   N_EG |
|:---------------------------------------|:---------------|:-----------------|---------:|:-----------------|-------:|
| 2008Q1-2025Q4                          | ln_ocupados    | 1.2979 (0.4190)  |       71 | 0.8655 (0.3291)  |     72 |
| 2008Q1-2025Q4                          | tipo_hip       | -0.0378 (0.0129) |       71 | -0.0422 (0.0091) |     72 |
| 2008Q1-2025Q4                          | ln_permisos_l4 | 0.1145 (0.0369)  |       71 | 0.1574 (0.0228)  |     72 |
| 2008Q1-2025Q4                          | ln_costes      | 0.4403 (0.1495)  |       71 | 0.4713 (0.1425)  |     72 |
| 2008Q1-2019Q4 (pre-COVID)              | ln_ocupados    | 2.0490 (0.3001)  |       47 | 0.7717 (0.3496)  |     48 |
| 2008Q1-2019Q4 (pre-COVID)              | tipo_hip       | -0.0496 (0.0085) |       47 | -0.0398 (0.0145) |     48 |
| 2008Q1-2019Q4 (pre-COVID)              | ln_permisos_l4 | 0.0172 (0.0292)  |       47 | 0.1528 (0.0268)  |     48 |
| 2008Q1-2019Q4 (pre-COVID)              | ln_costes      | -0.2396 (0.2018) |       47 | 0.1117 (0.3584)  |     48 |
| 2012Q1-2025Q4 (tras quiebre BP 2012Q1) | ln_ocupados    | 1.3313 (0.3579)  |       55 | 1.0543 (0.2440)  |     56 |
| 2012Q1-2025Q4 (tras quiebre BP 2012Q1) | tipo_hip       | -0.0376 (0.0191) |       55 | -0.0386 (0.0131) |     56 |
| 2012Q1-2025Q4 (tras quiebre BP 2012Q1) | ln_permisos_l4 | 0.0748 (0.0312)  |       55 | 0.1142 (0.0202)  |     56 |
| 2012Q1-2025Q4 (tras quiebre BP 2012Q1) | ln_costes      | 0.5918 (0.1760)  |       55 | 0.5531 (0.1584)  |     56 |
| 2014Q1-2025Q4                          | ln_ocupados    | 0.8263 (0.1610)  |       47 | 0.8144 (0.3426)  |     48 |
| 2014Q1-2025Q4                          | tipo_hip       | -0.0721 (0.0094) |       47 | -0.0513 (0.0130) |     48 |
| 2014Q1-2025Q4                          | ln_permisos_l4 | 0.1060 (0.0138)  |       47 | 0.1238 (0.0262)  |     48 |
| 2014Q1-2025Q4                          | ln_costes      | 0.9184 (0.0892)  |       47 | 0.7077 (0.1971)  |     48 |

Figuras: output/f2/cusum.png (CUSUM, p=0.562) y output/f2/ect_recursivo.png (ect recursivo).

**Lectura por fecha (asociaciones, no causalidad):**
- **2008:** la muestra del IPV empieza en 2007Q1 y la del modelo en 2008Q1/Q2, de modo que el quiebre de la crisis financiera no es contrastable con un Chow dentro de la muestra; no hay conclusión.
- **2014Q1:** el Chow rechaza la estabilidad del ECM preferido (2.60, p=0.012); Bai-Perron por BIC no encuentra quiebres en el ECM (el BIC es conservador). La estimación desde 2014Q1 (tabla de estabilidad) permite ver cuánto cambian ect y coeficientes. Es evidencia de inestabilidad moderada, con tramo previo de solo 23 observaciones.
- **2020Q1:** Chow p=0.124 (no rechaza). Sin embargo, el LR cambia mucho al excluir 2020-2026 (pre-COVID: costes y permisos cambian de signo) y Bai-Perron en niveles fecha un quiebre en 2020Q2.
- **2022Q3 (subida de tipos):** Chow p=0.377 (no rechaza, 16 obs. en el segundo tramo: baja potencia); el escalón tipo22 en el ECM no es significativo (ver robustez).
- **Estabilidad global:** CUSUM no rechaza en el ECM; el LR (niveles) no es estable (Bai-Perron: 2012Q1, 2020Q2, 2023Q2; CUSUM del DOLS p=0.288; DW=0,71). El coeficiente del ect cae a −0,05 en pre-COVID.

Los escalones se usan solo como robustez (en una ecuación en diferencias un escalón es un cambio de deriva; `epa21`=0,0078 en el ECM debe leerse como «cambio de deriva desde 2021», no como corrección del salto de la EPA; un impulso en 2021Q1 no cambia nada según la revisión).



## 6c. Crédito nuevo: comovimiento y simultaneidad (robustez, fuera de la K de búsqueda)

El volumen de crédito nuevo es operaciones × importe medio, y el importe depende del precio: la asociación contemporánea con el IPV es un comovimiento/simultaneidad, no un determinante predeterminado. Se reestima el preferido y el ganador AIC/BIC con crédito en t−1 y sin crédito (misma muestra N=73).

| modelo          | variante         |   N |   R2_aj |   BG4_p | ect_l1                   | d_ln_ocupados           | d_ln_ipv_l1             | d_ln_credito_nuevo      | d_ln_costes              | d_ln_renta_hog_real      | d_ln_credito_nuevo_l1    |
|:----------------|:-----------------|----:|--------:|--------:|:-------------------------|:------------------------|:------------------------|:------------------------|:-------------------------|:-------------------------|:-------------------------|
| Preferido R2aj  | base (crédito t) |  73 |  0.7485 | 0.1133  | -0.0968 (0.0309) p=0.002 | 0.4736 (0.1739) p=0.006 | 0.4421 (0.1130) p=0.000 | 0.0407 (0.0130) p=0.002 | -0.1047 (0.0543) p=0.054 | -0.0878 (0.0812) p=0.280 |                          |
| Preferido R2aj  | crédito en t−1   |  73 |  0.6897 | 0.03221 | -0.1013 (0.0271) p=0.000 | 0.7526 (0.1754) p=0.000 | 0.4917 (0.0967) p=0.000 |                         | -0.1492 (0.0600) p=0.013 | -0.1587 (0.1165) p=0.173 | -0.0289 (0.0111) p=0.009 |
| Preferido R2aj  | sin crédito      |  73 |  0.6518 | 0.01833 | -0.1201 (0.0303) p=0.000 | 0.6915 (0.2019) p=0.001 | 0.3614 (0.0963) p=0.000 |                         | -0.1605 (0.0608) p=0.008 | -0.1050 (0.1326) p=0.429 |                          |
| Ganador BIC/AIC | base (crédito t) |  73 |  0.7477 | 0.06837 | -0.1087 (0.0342) p=0.001 | 0.3384 (0.1502) p=0.024 | 0.4230 (0.1205) p=0.000 | 0.0421 (0.0139) p=0.002 |                          |                          |                          |
| Ganador BIC/AIC | crédito en t−1   |  73 |  0.6776 | 0.03382 | -0.1224 (0.0300) p=0.000 | 0.5326 (0.1119) p=0.000 | 0.4522 (0.1067) p=0.000 |                         |                          |                          | -0.0269 (0.0111) p=0.016 |
| Ganador BIC/AIC | sin crédito      |  73 |  0.645  | 0.01016 | -0.1388 (0.0339) p=0.000 | 0.5256 (0.1125) p=0.000 | 0.3252 (0.0998) p=0.001 |                         |                          |                          |                          |

Las otras variables cambian como muestra la tabla (compárese ect, ocupados y d_ln_ipv_l1 entre variantes).



## 6d. Signos y magnitudes frente a docs/literatura.md

**Largo plazo**

| variable                 | esperado   | DOLS             | EG_q             | UECM             | discrepancia                                                                                                      |
|:-------------------------|:-----------|:-----------------|:-----------------|:-----------------|:------------------------------------------------------------------------------------------------------------------|
| Empleo (LP)              | +          | 1.9510 (0.4801)  | 0.8366 (0.3271)  | 0.2529 (1.0978)  | signo OK; magnitud NO robusta: rango 0.84-2.67 según estimador/vector; literatura.md no da magnitud de referencia |
| Tipo hipotecario (LP)    | -          | -0.0172 (0.0171) | -0.0443 (0.0093) | -0.1235 (0.0568) |                                                                                                                   |
| Permisos t−4 (LP)        | -          | 0.0595 (0.0454)  | 0.1629 (0.0229)  | 0.2227 (0.0844)  | DISCREPANCIA de signo en algún estimador                                                                          |
| Costes construcción (LP) | +          | 0.2659 (0.1646)  | 0.5133 (0.1466)  | 1.2435 (0.6106)  |                                                                                                                   |
| Renta real (LP)          | +          | 1.4566 (0.3884)  |                  |                  |                                                                                                                   |
| Pob. extranjera (LP)     | +          | 0.7681 (0.1458)  |                  |                  |                                                                                                                   |

**Corto plazo (preferido y búsqueda)**

| variable                   | esperado   | preferido         | pct_modelos_signo_pos   | frac_signif   | discrepancia                                             |
|:---------------------------|:-----------|:------------------|:------------------------|:--------------|:---------------------------------------------------------|
| Empleo (CP)                | +          | 0.4736 (p=0.006)  | 100%                    | 99%           |                                                          |
| Tipo (CP)                  | -          | no incluido       | 20%                     | 24%           |                                                          |
| Permisos t−4 (CP)          | -          | no incluido       | 85%                     | 0%            | DISCREPANCIA: signo mayoritario en la búsqueda contrario |
| Costes (CP)                | +          | -0.1047 (p=0.054) | 47%                     | 8%            | DISCREPANCIA de signo en el preferido                    |
| Renta (CP)                 | +          | -0.0878 (p=0.280) | 67%                     | 36%           | DISCREPANCIA de signo en el preferido                    |
| Crédito (CP, comovimiento) | +          | 0.0407 (p=0.002)  | 100%                    | 100%          |                                                          |
| Pob. extranjera (CP)       | +          | no incluido       | 40%                     | 13%           | DISCREPANCIA: signo mayoritario en la búsqueda contrario |
| ect (entre −1 y 0)         | -          | -0.0968 (p=0.002) | 0%                      | 100%          |                                                          |

La elasticidad del precio al empleo no tiene magnitud de referencia en literatura.md. Los signos contrarios de permisos (+) y de costes/renta en el CP son compatibles con causalidad inversa o colinealidad y no se interpretan como efecto de oferta.



## 7. Problemas abiertos

- La réplica ECM (con q) rechaza BG4_p (p=0.000822).
- La réplica ECM (con q) rechaza JB_p (p=3.74e-10).
- El ECM preferido rechaza RESET_p (p=0.028).
- Cointegración nominal: evidencia mixta (1/3) (EG/Johansen/ARDL: False/True/False); precio real: cointegración (3/3). La regla ≥2/3 se aplica tal cual; no se cambia la especificación principal ex post.
- El p-valor del ect no es un contraste de cointegración (ver P1).
- LR inestable: Bai-Perron en niveles (2012Q1, 2020Q2, 2023Q2), cambios de signo pre-COVID; Chow 2014Q1 rechaza en el ECM (p=0.012).
- Crédito contemporáneo simultáneo con el precio (6c).
- ln_p_tasado y ln_p_bde son idénticas en nacional_q (diferencia máx. 0): los dos sistemas de robustez no son independientes.
- Johansen rechaza rangos altos (2-4) en sistemas de 5-6 variables I(1) con N≈74: probable sobre-rechazo; no puede ser el único apoyo.
- Bonferroni con K=nº de modelos que contienen el término es una cota muy conservadora (los modelos están anidados, no son hipótesis independientes) y no aplica al ect forzado; se da prioridad al bootstrap de la selección.
- OOS: el preferido no mejora al AR(4)+dummies ni al paseo con deriva; selección con muestra completa (pseudo-OOS).
- El ect del ECM es un regresor generado; no se corrige su incertidumbre; en el bootstrap se mantiene fijo.
- Johansen sin dummies estacionales (limitación de coint_johansen); ARDL sí las incluye.
- Población extranjera y población total interpoladas log-lineal antes de 2021 (MA mecánica en Δ1); d4/4 como contraste.
- IPV no desestacionalizado; las dummies absorben solo estacionalidad determinista.
