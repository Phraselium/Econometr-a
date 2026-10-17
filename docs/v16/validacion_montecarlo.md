# V16 · Validación de herramientas por Monte Carlo (fase 5)

Generado por `python3 src/v16/f5_validacion.py`. Cada herramienta se valida con un proceso generador que reproduce la estructura de los datos de entrenamiento de V16 (unidades, periodos, clusters, calendario de tratamiento, distancias) con resultados SIMULADOS: ningún dato real de resultado ni ninguna muestra sellada. Criterio (adenda del pre-registro, punto 11): tamaño al 5 % en [0,04; 0,06] con R ≥ 2.000 réplicas y cobertura al 95 % en [0,92; 0,97]. Una herramienta NO APTA no se usa en la fase 6 (su diseño queda descriptivo).

«Cifras determinantes» son las de la inferencia que decide el veredicto (principal o alternativa nombrada); las columnas de rango juntan todos los escenarios y variantes de referencia (p. ej. Webb en SDID o HC1 en Conley), que no deciden el veredicto. El detalle de cada herramienta está en su sección, debajo de la tabla.

| Herramienta | Cifras determinantes | Fallos del criterio | Tamaño (rango) | Cobertura (rango) | Veredicto | Inferencia utilizable |
|---|---|---|---|---|---|---|
| bayes_jerarquico | cobertura μ mín. 0,94 | no_nulo cob_mu=0.972 / homogeneo cob_mu=0.976 / homogeneo cob_seccion=0.985 |  | 0,9355-0,9461 | NO APTO | descriptivo |
| bh_jerarquico | FDR máx. BH 0,1216; FDR máx. BY 0,0473 | FDR máx. 0.1216 > 0.1 | 0,0473-0,1216 |  | NO APTO BH jerárquico; alternativa Benjamini-Yekutieli APTA | Benjamini-Yekutieli (en lugar de BH jerárquico) |
| blp_gates | tamaño 0,005; cobertura 0,9885 | tamaño 0.0050 fuera de [0.04; 0.06] / cobertura 0.9885 fuera de [0.92; 0.97] | 0,005 | 0,985-0,9885 | NO APTO → diseño solo descriptivo | descriptivo |
| cips_bootstrap | tamaño bootstrap 0,006 | tamaño 0.0060 fuera de [0.04; 0.06] | 0,006-0,0925 |  | NO APTO | descriptivo |
| conley_seccion | tamaño Conley 0,0435; cobertura 0,9565 |  | 0,0435-0,2362 | 0,9565 | APTO (solo escenario principal; no robusto a la sensibilidad del rango espacial) | Conley 2 km (solo escenario principal; no robusto al rango espacial) |
| cs_webb | tamaño 0,0655; cobertura 0,9015 | tamaño 0.0655 fuera de [0,04; 0,06] / cobertura 0.9015 fuera de [0,92; 0,97] / tamaño 0.3145 fuera de [0,04; 0,06] / cobertura 0.6905 fuera de [0,92; 0,97] | 0,0655 | 0,9015 | NO APTO → diseño solo descriptivo | descriptivo |
| csardl | tamaño 0,1015; cobertura 0,8985 | tamaño 0.1015 fuera de [0.04; 0.06] / cobertura 0.8985 fuera de [0.92; 0.97] | 0,1015 | 0,8955-0,8985 | NO APTO | descriptivo |
| dcdh_aleatorizacion | tamaño 0,0775; cobertura 0,967 | tamaño 0.0775 fuera de [0,04; 0,06] | 0,0775 | 0,967 | NO APTO → diseño solo descriptivo | descriptivo |
| did_intensidad_webb | tamaño Q2a 0,142; cobertura Q2a 0,857 | tamaño 0.1420 fuera de [0.04; 0.06] / cobertura 0.8570 fuera de [0.92; 0.97] / tamaño 0.0975 fuera de [0.04; 0.06] / cobertura 0.9025 fuera de [0.92; 0.97] |  |  | Q2a: NO APTO → diseño solo descriptivo; Q2c: NO APTO → diseño solo descriptivo | descriptivo |
| dm_hln | tamaño HLN 0,002; tamaño Clark-West 0,033 | tamaño 0.0020 fuera de [0.04; 0.06] / Clark-West: tamaño 0.0330 fuera de [0.04; 0.06] / tamaño 0.0330 fuera de [0.04; 0.06] / tamaño 0.0320 fuera de [0.04; 0.06] | 0,002-0,033 |  | NO APTO → diseño solo descriptivo | descriptivo |
| gsadf_factor | tamaño (salto) 0,0455; tamaño (estocástica) 0,0455; tamaño (homocedástico) 0,017 | nulo_homo: tamaño 0.0170 fuera de [0.04; 0.06] / tamaño 0.0170 fuera de [0.04; 0.06] | 0,017-0,3715 |  | APTO | bootstrap salvaje (válido con heterocedasticidad; conservador si homocedástico) |
| lp_newey_west_b | tamaño mín. 0,0642; tamaño máx. 0,0925 |  | 0,0642-0,0925 | 0,813-0,9313 | NO APTO → diseño solo descriptivo | descriptivo |
| rejilla_twfe | tamaño municipio 0,203; tamaño provincia 0,1105 | tamaño 0.2030 fuera de [0,04; 0,06] / cobertura 0.8055 fuera de [0,92; 0,97] / tamaño 0.1105 fuera de [0,04; 0,06] | 0,1105-0,203 | 0,8055-0,9545 | municipio: NO APTO → diseño solo descriptivo; provincia: NO APTO → diseño solo descriptivo | descriptivo |
| sdid_conley_taber | tamaño Conley-Taber A 0,0575; cobertura A 0,943 | tamaño 0.7795 fuera de [0,04; 0,06] / cobertura 0.2070 fuera de [0,92; 0,97] / tamaño 0.0650 fuera de [0,04; 0,06] / tamaño 0.7920 fuera de [0,04; 0,06] / cobertura 0.1970 fuera de [0,92; 0,97] | 0,0575-0,792 | 0,197-0,943 | APTO (Conley-Taber, escenario A; en el límite superior del tamaño, ver notas) | Conley-Taber (escenario A; tamaño en el límite superior) |
| shiftshare_akm | tamaño AKM 0,3762; tamaño AKM0 0,0108; cobertura AKM0 0,9892 | tamaño 0.3762 fuera de [0.04; 0.06] / cobertura 0.6238 fuera de [0.92; 0.97] / tamaño 0.0108 fuera de [0.04; 0.06] / cobertura 0.9892 fuera de [0.92; 0.97] / tamaño 0.4520 fuera de [0.04; 0.06] / cobertura 0.5480 fuera de [0.92; 0.97] | 0,0108-0,452 | 0,6238-0,9892 | NO APTO → diseño solo descriptivo | descriptivo |
| tost | tamaño en el borde (razón mediana) 0,0006 | tamaño en el borde < 0,04 (hasta 0,0) para Δ/EE pequeña: 10 de 15 diseños del repositorio con tamaño < 0,04 (df=12) / APTO solo si Δ/EE >= 2.0 (df=12), 2.0 (df=37) | 0,0006 |  | NO APTO como regla general; APTO condicionado a Δ/EE >= umbral (en otro caso «no concluyente») | TOST solo si Δ/EE ≥ umbral; si no, «no concluyente» |

# Validación Monte Carlo V16 · bayes_jerarquico (modelo normal-normal sección ⊂ municipio ⊂ provincia)

Código: `src/v16/montecarlo/bayes_jerarquico.py` · semilla `default_rng([20261010, 7, k])`.

## Proceso generador (declarado antes de simular)
- **Estructura real (solo códigos):** 8 provincias elegidas al azar entre las 41 con secciones SERPAVI de `base_alquiler` (entrenamiento), hasta 25 municipios por provincia y hasta 12 secciones por municipio, con los recuentos reales de secciones por municipio (≈ 181 municipios, ≈ 530 secciones). Los efectos y las estimaciones se simulan.
- **Modelo:** β̂_s ~ N(θ_s, se_s²), θ_s = μ + u_p + v_m + w_s; u ~ N(0, τu²), v ~ N(0, τv²), w ~ N(0, τw²); se_s = 0,06·exp(N(0; 0,5²)).
- **Priors (adenda punto 12, familia Q1):** μ ~ normal(0; 0,07); τu, τv, τw ~ semi-normal(0; 0,07). Sensibilidad con s×0,5 y s×2.
- **Verdades:** «prior» (μ y τ sorteados del propio prior, calibración bayesiana); «no nulo» (μ = −0,05; τ = 0,02/0,03/0,04); «nulo» (μ = 0); «homogéneo» (τ = 0,005, casi sin heterogeneidad).
- **Implementación (declarada):** PyMC no se usa. Muestreador Gibbs propio, con las varianzas de sección marginalizadas para (μ, u, v) y rejilla de 90 puntos (griddy Gibbs) para las tres desviaciones típicas; 1.200 iteraciones, 300 de calentamiento; μ se actualiza con u_p marginalizado (Gibbs parcialmente colapsado, orden μ → u → v → desviaciones → w), corrección hecha tras una primera pasada en que μ cubría 0,858 en el escenario «prior» por mala mezcla (documentada, no se usó).
- **Medidas:** cobertura del IC creíble al 95 % de μ, de los efectos de sección, de municipio y de provincia (criterio [0,92; 0,97]), sesgo y RMSE de μ, y P(0 fuera del IC) (tamaño/potencia informativos). R = 2.000 (nulo) y 1.000 (resto; 500 en sensibilidad: la cobertura, no el tamaño, es el criterio).

<!-- RESULTADOS -->
## Resultados

| escenario   |   escala_prior |    R |   cob_mu |   cob_seccion |   cob_municipio |   cob_provincia |   sesgo_mu |   rmse_mu |   P(0 fuera IC95 mu) |
|:------------|---------------:|-----:|---------:|--------------:|----------------:|----------------:|-----------:|----------:|---------------------:|
| prior       |            1   | 1000 |    0.94  |        0.9473 |          0.9434 |          0.9394 |    -0.0006 |    0.0238 |                0.529 |
| no_nulo     |            1   | 1000 |    0.972 |        0.9461 |          0.9386 |          0.9394 |     0.0013 |    0.008  |                0.998 |
| nulo        |            1   | 2000 |    0.952 |        0.9462 |          0.9374 |          0.9355 |    -0.0002 |    0.0081 |                0.048 |
| homogeneo   |            1   | 1000 |    0.976 |        0.9851 |          0.9661 |          0.9585 |     0.0002 |    0.0029 |                1     |
| no_nulo     |            0.5 |  500 |    0.92  |        0.9458 |          0.9388 |          0.924  |     0.0037 |    0.0086 |                1     |
| no_nulo     |            2   |  500 |    0.954 |        0.9464 |          0.9384 |          0.928  |    -0.0002 |    0.0083 |                0.998 |

**Veredicto: NO APTO** no_nulo cob_mu=0.972; homogeneo cob_mu=0.976; homogeneo cob_seccion=0.985

# Validación Monte Carlo V16 · bh_jerarquico (control de falsos descubrimientos en dos niveles)

Código: `src/v16/montecarlo/bh_jerarquico.py` · semilla `default_rng([20261010, 5, k])`.

## Proceso generador (declarado antes de simular)
- **Estructura real:** rejilla fija (83 celdas, familias Q1 18, Q2 24, Q3 21, Q4 7, Q6 13; resultado y escala leídos de `output/v16/potencia/rejilla_fija.csv`) y rama de diseños (18 pruebas en la tabla del punto 3, familia = pregunta; el encargo hablaba de 21: se simulan 18 y 21 con 3 pruebas hipotéticas añadidas a Q1, Q2 y Q3).
- **Estadísticos:** z normales con correlación por factores latentes: factor de **resultado** (celdas que comparten resultado, aunque sean de distinta familia) y factor de **escala** (misma pregunta y escala). Correlación débil (0,2; 0,1), moderada (0,4; 0,2) o fuerte (0,7; 0,2). **Signos** positivos o mixtos (cargas ±).
- **Nulos mixtos:** global (todas nulas); 20 % de celdas no nulas al azar; 40 % de las familias activas con 50 % de celdas no nulas. Efecto no nulo: desplazamiento de 3 en z. p-valores bilaterales (y un contraste unilateral con signos mixtos).
- **Procedimiento:** p de familia por Simes, BH entre familias a q = 0,10, y BH dentro de cada familia rechazada a q = 0,10. Alternativa nombrada: Benjamini-Yekutieli (Simes con factor armónico y BY en ambos pasos).
- **Medidas:** FDR = E[V/max(R,1)] y FWER = P(V ≥ 1) a nivel de celda, potencia por celda; PRDS empírico: en pares nulos que comparten factor se comprueba que P(p_j ≤ 0,10 | p_i ≤ s) crece al bajar s. R = 2.000 por escenario.
- **Criterio:** FDR realizada ≤ q = 0,10 en todos los escenarios bilaterales (el tamaño al 5 % no aplica a un procedimiento múltiple; adaptación declarada). La cota 2q = 0,20 de la adenda se informa.

<!-- RESULTADOS -->
## Resultados (R=2000 réplicas por escenario)

| estructura            | correlacion   | signos    | nulos     | metodo   |    FDR |   FWER |   potencia_celda |
|:----------------------|:--------------|:----------|:----------|:---------|-------:|-------:|-----------------:|
| rejilla_83            | debil         | positivos | global    | bh       | 0.102  | 0.102  |         nan      |
| rejilla_83            | debil         | positivos | global    | by       | 0.014  | 0.014  |         nan      |
| rejilla_83            | debil         | positivos | celdas_20 | bh       | 0.1033 | 0.7375 |           0.7351 |
| rejilla_83            | debil         | positivos | celdas_20 | by       | 0.0309 | 0.25   |           0.4901 |
| rejilla_83            | debil         | positivos | familias  | bh       | 0.0708 | 0.558  |           0.8287 |
| rejilla_83            | debil         | positivos | familias  | by       | 0.0162 | 0.17   |           0.6195 |
| rejilla_83            | debil         | mixtos    | global    | bh       | 0.0925 | 0.0925 |         nan      |
| rejilla_83            | debil         | mixtos    | global    | by       | 0.014  | 0.014  |         nan      |
| rejilla_83            | debil         | mixtos    | celdas_20 | bh       | 0.0991 | 0.716  |           0.7425 |
| rejilla_83            | debil         | mixtos    | celdas_20 | by       | 0.0274 | 0.225  |           0.4959 |
| rejilla_83            | debil         | mixtos    | familias  | bh       | 0.0705 | 0.5725 |           0.8307 |
| rejilla_83            | debil         | mixtos    | familias  | by       | 0.0174 | 0.1755 |           0.6303 |
| rejilla_83            | moderada      | positivos | global    | bh       | 0.099  | 0.099  |         nan      |
| rejilla_83            | moderada      | positivos | global    | by       | 0.013  | 0.013  |         nan      |
| rejilla_83            | moderada      | positivos | celdas_20 | bh       | 0.1032 | 0.6905 |           0.7313 |
| rejilla_83            | moderada      | positivos | celdas_20 | by       | 0.0274 | 0.215  |           0.4861 |
| rejilla_83            | moderada      | positivos | familias  | bh       | 0.0678 | 0.535  |           0.8257 |
| rejilla_83            | moderada      | positivos | familias  | by       | 0.0165 | 0.1635 |           0.6184 |
| rejilla_83            | moderada      | mixtos    | global    | bh       | 0.1055 | 0.1055 |         nan      |
| rejilla_83            | moderada      | mixtos    | global    | by       | 0.0135 | 0.0135 |         nan      |
| rejilla_83            | moderada      | mixtos    | celdas_20 | bh       | 0.1003 | 0.685  |           0.7387 |
| rejilla_83            | moderada      | mixtos    | celdas_20 | by       | 0.0284 | 0.2195 |           0.4954 |
| rejilla_83            | moderada      | mixtos    | familias  | bh       | 0.0726 | 0.5445 |           0.8301 |
| rejilla_83            | moderada      | mixtos    | familias  | by       | 0.0178 | 0.176  |           0.6259 |
| rejilla_83            | fuerte        | positivos | global    | bh       | 0.0965 | 0.0965 |         nan      |
| rejilla_83            | fuerte        | positivos | global    | by       | 0.0115 | 0.0115 |         nan      |
| rejilla_83            | fuerte        | positivos | celdas_20 | bh       | 0.1041 | 0.618  |           0.7363 |
| rejilla_83            | fuerte        | positivos | celdas_20 | by       | 0.0289 | 0.198  |           0.49   |
| rejilla_83            | fuerte        | positivos | familias  | bh       | 0.0671 | 0.487  |           0.8102 |
| rejilla_83            | fuerte        | positivos | familias  | by       | 0.0151 | 0.143  |           0.5974 |
| rejilla_83            | fuerte        | mixtos    | global    | bh       | 0.082  | 0.082  |         nan      |
| rejilla_83            | fuerte        | mixtos    | global    | by       | 0.0125 | 0.0125 |         nan      |
| rejilla_83            | fuerte        | mixtos    | celdas_20 | bh       | 0.1028 | 0.621  |           0.737  |
| rejilla_83            | fuerte        | mixtos    | celdas_20 | by       | 0.0307 | 0.2165 |           0.4923 |
| rejilla_83            | fuerte        | mixtos    | familias  | bh       | 0.0691 | 0.487  |           0.8246 |
| rejilla_83            | fuerte        | mixtos    | familias  | by       | 0.0175 | 0.1515 |           0.6286 |
| disenos_18            | debil         | positivos | global    | bh       | 0.1    | 0.1    |         nan      |
| disenos_18            | debil         | positivos | global    | by       | 0.0185 | 0.0185 |         nan      |
| disenos_18            | debil         | positivos | celdas_20 | bh       | 0.1164 | 0.3585 |           0.7326 |
| disenos_18            | debil         | positivos | celdas_20 | by       | 0.0451 | 0.1435 |           0.5259 |
| disenos_18            | debil         | positivos | familias  | bh       | 0.0972 | 0.294  |           0.7611 |
| disenos_18            | debil         | positivos | familias  | by       | 0.033  | 0.095  |           0.5732 |
| disenos_18            | debil         | mixtos    | global    | bh       | 0.1095 | 0.1095 |         nan      |
| disenos_18            | debil         | mixtos    | global    | by       | 0.024  | 0.024  |         nan      |
| disenos_18            | debil         | mixtos    | celdas_20 | bh       | 0.1216 | 0.3655 |           0.7389 |
| disenos_18            | debil         | mixtos    | celdas_20 | by       | 0.0451 | 0.143  |           0.5376 |
| disenos_18            | debil         | mixtos    | familias  | bh       | 0.0899 | 0.2765 |           0.7723 |
| disenos_18            | debil         | mixtos    | familias  | by       | 0.0292 | 0.0935 |           0.5941 |
| disenos_18            | moderada      | positivos | global    | bh       | 0.107  | 0.107  |         nan      |
| disenos_18            | moderada      | positivos | global    | by       | 0.0255 | 0.0255 |         nan      |
| disenos_18            | moderada      | positivos | celdas_20 | bh       | 0.1164 | 0.3475 |           0.7319 |
| disenos_18            | moderada      | positivos | celdas_20 | by       | 0.043  | 0.133  |           0.5218 |
| disenos_18            | moderada      | positivos | familias  | bh       | 0.0875 | 0.2575 |           0.7661 |
| disenos_18            | moderada      | positivos | familias  | by       | 0.03   | 0.086  |           0.5718 |
| disenos_18            | moderada      | mixtos    | global    | bh       | 0.09   | 0.09   |         nan      |
| disenos_18            | moderada      | mixtos    | global    | by       | 0.0185 | 0.0185 |         nan      |
| disenos_18            | moderada      | mixtos    | celdas_20 | bh       | 0.1158 | 0.344  |           0.7208 |
| disenos_18            | moderada      | mixtos    | celdas_20 | by       | 0.0438 | 0.128  |           0.5126 |
| disenos_18            | moderada      | mixtos    | familias  | bh       | 0.0917 | 0.271  |           0.7719 |
| disenos_18            | moderada      | mixtos    | familias  | by       | 0.0329 | 0.1015 |           0.5808 |
| disenos_18            | fuerte        | positivos | global    | bh       | 0.0865 | 0.0865 |         nan      |
| disenos_18            | fuerte        | positivos | global    | by       | 0.023  | 0.023  |         nan      |
| disenos_18            | fuerte        | positivos | celdas_20 | bh       | 0.1106 | 0.3035 |           0.7322 |
| disenos_18            | fuerte        | positivos | celdas_20 | by       | 0.042  | 0.122  |           0.5248 |
| disenos_18            | fuerte        | positivos | familias  | bh       | 0.0903 | 0.2395 |           0.7482 |
| disenos_18            | fuerte        | positivos | familias  | by       | 0.0311 | 0.0885 |           0.5542 |
| disenos_18            | fuerte        | mixtos    | global    | bh       | 0.082  | 0.082  |         nan      |
| disenos_18            | fuerte        | mixtos    | global    | by       | 0.0205 | 0.0205 |         nan      |
| disenos_18            | fuerte        | mixtos    | celdas_20 | bh       | 0.1001 | 0.286  |           0.7389 |
| disenos_18            | fuerte        | mixtos    | celdas_20 | by       | 0.0375 | 0.1115 |           0.5369 |
| disenos_18            | fuerte        | mixtos    | familias  | bh       | 0.0874 | 0.247  |           0.77   |
| disenos_18            | fuerte        | mixtos    | familias  | by       | 0.0356 | 0.105  |           0.5909 |
| disenos_21            | debil         | positivos | global    | bh       | 0.1005 | 0.1005 |         nan      |
| disenos_21            | debil         | positivos | global    | by       | 0.0205 | 0.0205 |         nan      |
| disenos_21            | debil         | positivos | celdas_20 | bh       | 0.1118 | 0.376  |           0.7379 |
| disenos_21            | debil         | positivos | celdas_20 | by       | 0.0441 | 0.1495 |           0.5251 |
| disenos_21            | debil         | positivos | familias  | bh       | 0.0898 | 0.3045 |           0.7708 |
| disenos_21            | debil         | positivos | familias  | by       | 0.0292 | 0.101  |           0.5755 |
| disenos_21            | debil         | mixtos    | global    | bh       | 0.099  | 0.099  |         nan      |
| disenos_21            | debil         | mixtos    | global    | by       | 0.02   | 0.02   |         nan      |
| disenos_21            | debil         | mixtos    | celdas_20 | bh       | 0.1157 | 0.3865 |           0.7329 |
| disenos_21            | debil         | mixtos    | celdas_20 | by       | 0.044  | 0.1465 |           0.5161 |
| disenos_21            | debil         | mixtos    | familias  | bh       | 0.0965 | 0.315  |           0.7831 |
| disenos_21            | debil         | mixtos    | familias  | by       | 0.0341 | 0.1115 |           0.5894 |
| disenos_21            | moderada      | positivos | global    | bh       | 0.0815 | 0.0815 |         nan      |
| disenos_21            | moderada      | positivos | global    | by       | 0.0155 | 0.0155 |         nan      |
| disenos_21            | moderada      | positivos | celdas_20 | bh       | 0.1187 | 0.3805 |           0.7371 |
| disenos_21            | moderada      | positivos | celdas_20 | by       | 0.0453 | 0.1485 |           0.5246 |
| disenos_21            | moderada      | positivos | familias  | bh       | 0.0906 | 0.2885 |           0.7563 |
| disenos_21            | moderada      | positivos | familias  | by       | 0.0305 | 0.0955 |           0.5624 |
| disenos_21            | moderada      | mixtos    | global    | bh       | 0.095  | 0.095  |         nan      |
| disenos_21            | moderada      | mixtos    | global    | by       | 0.021  | 0.021  |         nan      |
| disenos_21            | moderada      | mixtos    | celdas_20 | bh       | 0.1196 | 0.3755 |           0.7439 |
| disenos_21            | moderada      | mixtos    | celdas_20 | by       | 0.0473 | 0.152  |           0.5341 |
| disenos_21            | moderada      | mixtos    | familias  | bh       | 0.0914 | 0.3035 |           0.7891 |
| disenos_21            | moderada      | mixtos    | familias  | by       | 0.0304 | 0.1005 |           0.5863 |
| disenos_21            | fuerte        | positivos | global    | bh       | 0.087  | 0.087  |         nan      |
| disenos_21            | fuerte        | positivos | global    | by       | 0.025  | 0.025  |         nan      |
| disenos_21            | fuerte        | positivos | celdas_20 | bh       | 0.1075 | 0.3005 |           0.7288 |
| disenos_21            | fuerte        | positivos | celdas_20 | by       | 0.0356 | 0.1095 |           0.5261 |
| disenos_21            | fuerte        | positivos | familias  | bh       | 0.0886 | 0.25   |           0.7488 |
| disenos_21            | fuerte        | positivos | familias  | by       | 0.0289 | 0.0845 |           0.5492 |
| disenos_21            | fuerte        | mixtos    | global    | bh       | 0.08   | 0.08   |         nan      |
| disenos_21            | fuerte        | mixtos    | global    | by       | 0.016  | 0.016  |         nan      |
| disenos_21            | fuerte        | mixtos    | celdas_20 | bh       | 0.115  | 0.343  |           0.741  |
| disenos_21            | fuerte        | mixtos    | celdas_20 | by       | 0.042  | 0.1305 |           0.5213 |
| disenos_21            | fuerte        | mixtos    | familias  | bh       | 0.0961 | 0.273  |           0.773  |
| disenos_21            | fuerte        | mixtos    | familias  | by       | 0.0313 | 0.0985 |           0.5798 |
| rejilla_83_unilateral | moderada      | mixtos    | global    | bh       | 0.0885 | 0.0885 |         nan      |
| rejilla_83_unilateral | moderada      | mixtos    | global    | by       | 0.013  | 0.013  |         nan      |
| rejilla_83_unilateral | moderada      | mixtos    | celdas_20 | bh       | 0.0985 | 0.748  |           0.8332 |
| rejilla_83_unilateral | moderada      | mixtos    | celdas_20 | by       | 0.0292 | 0.2595 |           0.6148 |
| rejilla_83_unilateral | moderada      | mixtos    | familias  | bh       | 0.067  | 0.5585 |           0.9047 |
| rejilla_83_unilateral | moderada      | mixtos    | familias  | by       | 0.0143 | 0.158  |           0.7391 |

Violaciones PRDS empíricas (proporción de pares): {'rejilla_83|positivos|bilateral': 0.0, 'rejilla_83|mixtos|bilateral': 0.0, 'rejilla_83|mixtos|unilateral': 0.0, 'disenos_18|mixtos|bilateral': 0.0}

**Veredicto: NO APTO BH jerárquico; alternativa Benjamini-Yekutieli APTA** FDR máx. 0.1216 > 0.1

# blp_gates · prueba conjunta de heterogeneidad BLP/GATES (una por pregunta con diseño; R20)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** 1,728 municipios de entrenamiento con SERPAVI de alquiler en 2021 y 2024 (solo disponibilidad del dato) en 38 provincias (clusters de tamaño real, de 1 a 203).
- **Moderadores (fijados por la adenda):** renta media, población, % de extranjeros, % de vivienda turística y obra nueva per cápita. Se simulan con una cópula gaussiana (correlación 0,3 entre moderadores)
  con un 30 % de la varianza común dentro de la provincia; marginales: renta lognormal, población lognormal de cola pesada, % de extranjeros beta, % VUT con cero en el 40 % y lognormal en el resto, obra nueva gamma. Se estandarizan para el efecto.
- **Tratamiento:** asignado por provincia (cluster) al azar con probabilidad p = 0.5 (conocida): estructura de pocos clusters, como las preguntas de diseño por CCAA/provincia.
- **Resultado (Δlog, un periodo):** Y_i = g(Z_i) + v_prov(i) + τ(Z_i)·D_i + 0.08·ε_i, con g no lineal (suma de efectos suaves y una interacción), v_prov ~ N(0,0.048²) (choque de provincia), ε ~ N(0,1).
  **Nulo (efecto homogéneo):** τ(Z) = 0.03. **Alternativa (heterogeneidad):** τ(Z) = 0.03 + 0.03·h(Z), h = combinación estandarizada de pct_vut (no lineal) y renta (media 0, DT 1).
- **Procedimiento:** 11 particiones aleatorias de las PROVINCIAS (mitad auxiliar A, mitad principal M; partir por cluster evita fugas). En A: ExtraTrees (60 árboles, hoja ≥ 15) por brazo → B(Z) = m0(Z), S(Z) = m1(Z) − m0(Z).
  En M: BLP: Y ~ 1 + B + S + (D−p) + (D−p)(S−S̄), ponderado 1/(p(1−p)); GATES: Y ~ 1 + B + S + Σ_k γ_k (D−p)·1(S ∈ cuantil k), K = 5. Covarianza CR1 por provincia (en M).
- **Prueba conjunta (principal):** Wald de igualdad de los 5 GATES (γ1 = … = γ5), referencia F(4, G_M − 1). Agregación entre particiones (CDDF): p = min(1, 2·mediana de los p). Secundarias informadas: BLP β2 = 0 y γ5 = γ1.
  IC del efecto medio (β1 del BLP): por partición al 97,5 % con t(G_M − 1), mediana de los límites (ajuste CDDF); cobertura frente al efecto medio poblacional τ0 = 0.03 (la heterogeneidad h tiene media 0).
- **Alternativa nombrada en el punto 3:** ninguna (la prueba conjunta se adopta tal cual). Si no pasa → «NO APTO → diseño solo descriptivo» (los subgrupos ya son descriptivos C4).
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 bajo efecto homogéneo, cobertura del IC del efecto medio en [0,92; 0,97]; se informa la potencia bajo la alternativa. Un tamaño de 0,0 es NO APTO.

<!-- RESULTADOS -->
## Resultados (R = 2000 réplicas válidas de 2000, S = 11 particiones; semilla 20261010, k = 35)

| prueba | R | tamano_5pct | tamano_ic95 | potencia_heterogeneidad | cobertura_ate_95 | sesgo_ate | rmse_ate |
|---|---|---|---|---|---|---|---|
| conjunta: igualdad de los 5 GATES (principal) | 2000 | 0.0050 | [0.0019, 0.0081] | 0.1880 | 0.9850 | -0.0004 | 0.0226 |
| BLP beta2 = 0 (secundaria) | 2000 | 0.0050 | [0.0019, 0.0081] | 0.2120 | nan | nan | nan |
| GATES gamma5 = gamma1 (secundaria) | 2000 | 0.0025 | [0.0003, 0.0047] | 0.1840 | nan | nan | nan |


Cobertura del IC 95 % del efecto medio bajo efecto homogéneo: 0.9885.

**Veredicto: NO APTO → diseño solo descriptivo.**

Condición que falla: tamaño 0.0050 fuera de [0.04; 0.06]; cobertura 0.9885 fuera de [0.92; 0.97].

# Validación Monte Carlo V16 · cips_bootstrap (Q9, CIPS con bootstrap de bloques)

Código: `src/v16/montecarlo/cips_bootstrap.py` · semilla `default_rng([20261010, 1, k])` · salidas en `output/v16/montecarlo/cips_bootstrap/`.

## Proceso generador (declarado antes de simular)
- **Dimensiones:** N = 38 unidades (provincias de entrenamiento), T = 95 trimestres (2002T1-2026T2). Ningún valor real.
- **Dependencia transversal:** factor común f_t AR(1) con ρ = 0,5 y cargas γ_i ~ N(1; 0,5²); correlación espacial en anillo (peso 0,25 con los dos vecinos).
- **Autocorrelación y heterogeneidad:** errores AR(1) con ρ_i ~ U(0; 0,4) (valor declarado, no calibrado con datos), σ_i ~ U(0,5; 1,5).
- **Nulo:** y_it = y_i,t-1 + γ_i f_t + e_it (raíz unitaria en todas las unidades). **Alternativa:** φ_i ~ U(0,85; 0,95), constante μ_i, factor estacionario.
- **Estadístico:** CIPS = media de las t de CADF(1) con constante (medias transversales y rezago 1).
- **Inferencia:** bootstrap de bloques móviles (longitud 2·T^(1/3) ≈ 9) sobre las primeras diferencias de todas las unidades a la vez (conserva el factor común), sin deriva, B = 399 (por defecto) y valor crítico = cuantil 5 % del CIPS*. Se compara con el VC asintótico aproximado de Pesaran (2007), −2,11.
- **Réplicas:** 2.000 bajo el nulo, 500 bajo la alternativa. Cobertura: no definida para una prueba; el veredicto usa el tamaño.

<!-- RESULTADOS -->
## Resultados (R=2000 bajo el nulo, R=500 bajo la alternativa, B=399, bloque=9)

| escenario   |    R |   rech_boot |   rech_pvalor |   rech_asint |   media_cips |   cv_boot_media |
|:------------|-----:|------------:|--------------:|-------------:|-------------:|----------------:|
| nulo        | 2000 |       0.006 |        0.0055 |       0.0925 |     -1.7888  |        -2.35664 |
| alternativa |  500 |       0.868 |        0.856  |       1      |     -2.63409 |        -2.47712 |

Tamaño con bootstrap: 0.0060 (IC binomial [0.0026, 0.0094]); con CV asintótico -2,11: 0.0925. Potencia (φ_i en U(0,85; 0,95)): 0.8680.

**Veredicto: NO APTO** tamaño 0.0060 fuera de [0.04; 0.06]

Diagnóstico exploratorio (R=120, B=149, src/v16/montecarlo/cips_bootstrap_diagnostico.py; no es parte del veredicto): bloques de 9, 20 y 40 dan tamaño 0,0 en los tres casos (sobrecorrección: VC demasiado negativo); un bootstrap sieve AR(1) con remuestreo conjunto de residuos da 0,075 (ruido ±0,05); VC asintótico -2,11: 0,092.

# conley_seccion · Q3-b (corte transversal por sección, Conley a 2 km, efectos fijos de municipio)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** 10,815 secciones de entrenamiento (de 11,574 con SERPAVI 2021 y 2024 disponibles, tras `unidad_sellada_v16`; se descartan las de
  municipios con una sola sección, cuyo efecto fijo las absorbe) en 851 municipios y 38 provincias; centroides de data/base/geo/secciones.parquet
  (distancia en km sobre esfera de 6.371 km). Vecinos medios dentro de 2 km (con la propia sección): 46.6.
- **Exposición y resultado:** x_i = m^x_{mun(i)} + √0,6·z^x_i + √0,4·ξ^x_i;  y_i = β·x_i + h_{mun(i)}·(m^y_{mun(i)} + √0,6·z^y_i + √0,4·ξ^y_i), con efectos de municipio m ~ N(0,1) (absorbidos por el FE),
  ξ ruido idiosincrásico N(0,1), h_mun = exp(0,5·N(0,1)) (heterocedasticidad entre municipios), y z = campo gaussiano espacial con media móvil triangular de radio r sobre
  ruido blanco (correlación entre secciones positiva solo a menos de 2r; varianza unitaria). Los campos de x e y son independientes bajo el nulo.
- **Escenario principal:** r = 1,0 km (la correlación se anula a 2 km, el corte de Conley). **Sensibilidad (informativa):** r = 0,5 y 1,5 km (esta última deja correlación entre 2 y 3 km).
- **Nulo:** β = 0 (tamaño). **Alternativa:** β = 0.05 (DT de y por DT de x; Q3-b no tiene magnitud de referencia): sesgo, RMSE, cobertura y potencia.
- **Estimación:** MCO de y sobre x con efectos fijos de municipio (demedia intra-municipio). Inferencia: Conley con núcleo de Bartlett (triangular) a 2 km, normal.
  Si la varianza de Conley sale no positiva (el núcleo triangular no es semidefinido positivo en 2D) la réplica cuenta como no rechazo y se informa su frecuencia.
  Referencias (no candidatas): EE robustos HC1 y EE agrupados por municipio.
- **Alternativa nombrada en el punto 3:** ninguna (Conley a 2 km es la principal). Si no pasa → «NO APTO → diseño solo descriptivo».
- **Pocos clusters / T corto:** corte transversal; dependencia por distancia; sin dimensión temporal.
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97].

<!-- RESULTADOS -->
## Resultados (R = 4000 réplicas en el escenario principal; semilla 20261010, k = 32)

| escenario | inferencia | R | tamano_5pct | tamano_ic95 | cobertura_95 | potencia_beta | sesgo | rmse | var_no_positiva |
|---|---|---|---|---|---|---|---|---|---|
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | Conley 2 km | 4000 | 0.0435 | [0.0372, 0.0498] | 0.9565 | 0.6542 | 0.0000 | 0.0209 | 0.0000 |
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | HC1 (referencia) | 4000 | 0.2362 | [0.2231, 0.2494] | 0.7638 | 0.8890 | 0.0000 | 0.0209 | nan |
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | agrupado por municipio (referencia) | 4000 | 0.0695 | [0.0616, 0.0774] | 0.9305 | 0.7260 | 0.0000 | 0.0209 | nan |
| sens: radio 0,5 km | Conley 2 km | 2000 | 0.0120 | [0.0072, 0.0168] | 0.9880 | 0.8225 | -0.0001 | 0.0145 | 0.0000 |
| sens: radio 0,5 km | HC1 (referencia) | 2000 | 0.0925 | [0.0798, 0.1052] | 0.9075 | 0.9555 | -0.0001 | 0.0145 | nan |
| sens: radio 0,5 km | agrupado por municipio (referencia) | 2000 | 0.0480 | [0.0386, 0.0574] | 0.9520 | 0.9270 | -0.0001 | 0.0145 | nan |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | Conley 2 km | 2000 | 0.0680 | [0.057, 0.079] | 0.9320 | 0.5825 | -0.0002 | 0.0271 | 0.0000 |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | HC1 (referencia) | 2000 | 0.3460 | [0.3252, 0.3668] | 0.6540 | 0.8335 | -0.0002 | 0.0271 | nan |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | agrupado por municipio (referencia) | 2000 | 0.0630 | [0.0524, 0.0736] | 0.9370 | 0.5840 | -0.0002 | 0.0271 | nan |


**Veredicto: APTO (solo escenario principal; no robusto a la sensibilidad del rango espacial).**

**Advertencia.** El tamaño en el escenario principal (correlación espacial que se anula justo en el corte de 2 km) está en el intervalo, pero no se mantiene con campos de rango menor (tamaño conservador) ni mayor (sobre-rechazo): la calibración depende de que el corte coincida con el alcance de la correlación. Q3-b es C4 (correlación) y debe llevar esta advertencia.

# cs_webb · Q1c · Callaway-Sant'Anna con wild cluster bootstrap de Webb por provincia

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/cs_webb.py)
```
Monte Carlo V16 (fase 5) · Callaway-Sant'Anna con wild cluster bootstrap de Webb por provincia, Q1c.

Proceso generador (declarado en docs/v16/validacion_montecarlo/cs_webb.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): las 41 provincias de entrenamiento; trimestres 2019T1-2026T2 (30); tratamiento =
  provincia con alguna zona vigente, con la cohorte del primer trimestre completo posterior a la fecha de efecto (intervenciones.csv);
  comparación = nunca tratadas. Cada provincia es su propio cluster.
  RESULTADO SIMULADO (log compraventas trimestral): y_it = mu_i + delta_i t + g_i1 f_1t + g_i2 f_2t + s_it + e_it
    f_1, f_2: factores comunes AR(1) rho 0,8, sd 0,08; g_i1 ~ N(1; 0,4); g_i2 = campo espacial exp(-d/300 km) con sd 0,5
    s_it: campo gaussiano espacial exp(-d/150 km) entre centroides, AR(1) rho 0,6, sd 0,04
    e_it: AR(1) rho 0,5, sd marginal 0,06 * exp(0,3 z_i - 0,045); delta_i ~ N(0; 0,002) tendencia propia. Valores declarados.
  EFECTO: nulo = 0; alternativas 0,05 y 0,10 (log) con heterogeneidad tau_i = tau (1 + 0,5 z_i) y dinámica 1 - exp(-(e+1)/2) tras la entrada;
  la verdad es el ATT agregado muestral (misma ponderación que el estimador).
Estimador: ATT(g,t) con nunca tratadas y periodo base g-1, agregado «simple» (peso por tamaño de cohorte sobre las celdas t >= g).
Inferencia: multiplicador wild cluster bootstrap-t de Webb (6 puntos) sobre la función de influencia, B = 999, por provincia.
```

<!-- RESULTADOS -->
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
| escenario | tau | variante | R | sesgo | rmse | cobertura | rechazo | ancho_medio_ic |
|---|---|---|---|---|---|---|---|---|
| nulo | 0.0000 | a_multiplicador_IF | 2000 | 0.0012 | 0.0452 | 0.6855 | 0.3145 | 0.0938 |
| nulo | 0.0000 | b_WCR_nulo_impuesto | 2000 | 0.0012 | 0.0452 | 0.9325 | 0.0655 | 0.1284 |
| alt_005 | 0.0500 | a_multiplicador_IF | 2000 | 0.0003 | 0.0458 | 0.6905 | 0.4765 | 0.0951 |
| alt_005 | 0.0500 | b_WCR_nulo_impuesto | 2000 | 0.0003 | 0.0458 | 0.9015 | 0.1965 | 0.1428 |
| alt_010 | 0.1000 | a_multiplicador_IF | 1000 | -0.0019 | 0.0447 | 0.7320 | 0.7170 | 0.1024 |
| alt_010 | 0.1000 | b_WCR_nulo_impuesto | 1000 | -0.0019 | 0.0447 | 0.9080 | 0.4190 | 0.1753 |
| control_iid_nulo | 0.0000 | a_multiplicador_IF | 1000 | 0.0009 | 0.0260 | 0.7940 | 0.2040 | 0.0735 |
| control_iid_nulo | 0.0000 | b_WCR_nulo_impuesto | 1000 | 0.0009 | 0.0260 | 0.9770 | 0.0230 | 0.0944 |

## Veredicto
**NO APTO → diseño solo descriptivo**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{
 "principal_b": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.0655 fuera de [0,04; 0,06]",
   "cobertura 0.9015 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.0655,
  "R_nulo": 2000,
  "cobertura_alt": 0.9015,
  "R_alt": 2000,
  "cobertura_nulo": 0.9325,
  "sesgo_nulo": 0.0012394246068562,
  "rmse_nulo": 0.0452323578014545,
  "se_mc_tamano": 0.005532167296819575,
  "se_mc_cobertura": 0.0066632480818291625
 },
 "descartada_a": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.3145 fuera de [0,04; 0,06]",
   "cobertura 0.6905 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.3145,
  "R_nulo": 2000,
  "cobertura_alt": 0.6905,
  "R_alt": 2000,
  "cobertura_nulo": 0.6855,
  "sesgo_nulo": 0.0012394246068562,
  "rmse_nulo": 0.0452323578014545,
  "se_mc_tamano": 0.010382431073693675,
  "se_mc_cobertura": 0.010337063170939801
 }
}
```

## Notas y límites
Inferencia principal = wild cluster bootstrap de Webb por provincia con el nulo impuesto (variante b). La adenda no nombra alternativa para Q1c: si falla, el diseño es solo descriptivo. Variante a (multiplicador sobre la función de influencia sin restringir) descartada de entrada: tamaño 0.315 y cobertura 0.691, porque las cohortes de una sola provincia (4 de 5) tienen residuo de influencia cero y la varianza se subestima; se informa pero no se usa. Variante b: tamaño 0.0655, cobertura bajo nulo 0.9325, bajo tau=0,05 0.9015. Control de implementación sin dependencia (ruido iid): tamaño 0.023, cobertura 0.977 (el procedimiento es conservador sin dependencia y pierde la cobertura con dependencia transversal y espacial, con 8 tratadas en 5 cohortes y 33 comparaciones). Potencia (variante b): 0.197 a tau=0,05 y 0.419 a tau=0,10; sin magnitud de referencia comparable (la condición (b) no se cumple). Sesgo despreciable (0.0012); el fallo es de inferencia, no de punto.

## Reproducción
`python3 src/v16/montecarlo/cs_webb.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/cs_webb/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.

# Validación Monte Carlo V16 · csardl (Q9-c, CS-ARDL)

Código: `src/v16/montecarlo/csardl.py` · semilla `default_rng([20261010, 2, k])`.

## Proceso generador (declarado antes de simular)
- **Dimensiones:** N = 38, T = 95. Resultado y_it (log valor tasado simulado) y regresor x_it (log IPC de alquiler simulado).
- **Modelo:** ARDL(1,1): y_it = φ_i y_i,t-1 + β0_i x_it + β1_i x_i,t-1 + γ^y_i f_t + 0,7 e_it, con φ_i ~ U(0,5; 0,8) y elasticidad de largo plazo θ_i = (β0+β1)/(1−φ) ~ N(0,8; 0,2²) (heterogeneidad). x_it = ρ^x_i x_i,t-1 + γ^x_i f_t + u_it, ρ^x_i ~ U(0,3; 0,7).
- **Dependencia transversal:** un factor común f_t AR(1) ρ = 0,6, cargas N(1; 0,5²) en x e y; correlación espacial en anillo (0,25) en u y e. Pocos clusters: no aplica (inferencia por bloques de tiempo, no por cluster).
- **Estimador:** CS-ARDL por unidad con medias transversales de y y x y sus ⌊T^(1/3)⌋ = 4 rezagos; θ̂_MG = media de (b0+b1)/(1−φ̂).
- **Objetivo:** media muestral de los θ_i verdaderos. Inferencia: bootstrap de bloques móviles (longitud ≈ 9) de las filas de regresión conjuntas para las N unidades, B = 99, IC normal con EE bootstrap (y percentil centrado como diagnóstico).
- **Tamaño** = 1 − cobertura del mismo IC; **potencia** frente a θ = 0 y frente a un desplazamiento declarado de 0,2 (Q9-c no tiene magnitud de referencia). R = 2.000.

<!-- RESULTADOS -->
## Resultados (R=2000, B=99, bloque=9)

| medida                       |      valor |
|:-----------------------------|-----------:|
| sesgo                        | -0.0390991 |
| rmse                         |  0.0656413 |
| cobertura_normal_boot        |  0.8985    |
| cobertura_percentil_centrado |  0.8955    |
| tamano_5pct                  |  0.1015    |
| potencia_theta0              |  0.974     |
| potencia_desplazamiento_0.2  |  0.8705    |
| se_boot_medio                |  0.106951  |
| sd_estimador                 |  0.0597647 |

IC normal con EE bootstrap: cobertura 0.8985 (tamaño 0.1015). IC percentil centrado: 0.8955.

**Veredicto: NO APTO** tamaño 0.1015 fuera de [0.04; 0.06]; cobertura 0.8985 fuera de [0.92; 0.97]

# dcdh_aleatorizacion · Q6 · de Chaisemartin-D'Haultfoeuille continuo con aleatorización del calendario entre CCAA

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/dcdh_aleatorizacion.py)
```
Monte Carlo V16 (fase 5) · de Chaisemartin-D'Haultfoeuille (tratamiento continuo, no absorbente) con inferencia por aleatorización
del calendario entre CCAA, Q6.

Proceso generador (declarado en docs/v16/validacion_montecarlo/dcdh_aleatorizacion.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): 41 provincias de entrenamiento agrupadas en sus CCAA (9 no selladas + Ceuta y Melilla
  como clusters sin cambio de tipo); tratamiento = tipo general del ITP por CCAA y año 2011-2024, construido con las filas de
  intervenciones.csv (el último valor con fecha de efecto en el año o antes). Panel anual, 14 años.
  RESULTADO SIMULADO (log compraventas usadas anual): y_it = mu_i + delta_i t + g_i1 f_1t + g_i2 f_2t + u_c(i),t + s_it + e_it + beta_i D_it
    f_1, f_2 AR(1) rho 0,7, sd 0,10; g_i1 ~ N(1; 0,4); g_i2 = campo espacial (300 km) sd 0,5
    u_ct: choque CCAA-año AR(1) rho 0,5, sd 0,04 * exp(0,3 z_c - 0,045) (heterocedasticidad entre CCAA)
    s_it: campo espacial exp(-d/150 km), AR(1) rho 0,5, sd 0,04;  e_it: AR(1) rho 0,5, sd 0,06 * exp(0,3 z_i - 0,045); delta_i ~ N(0; 0,003)
  EFECTO (contemporáneo por punto de tipo): nulo = 0; alternativas -0,07 por punto (volumen, Fritzsche-Vandrei) y -0,01 (precio),
  beta_i = beta (1 + 0,5 z_i); la verdad es la media de beta_i ponderada por |dD| en las celdas que cambian.
Estimador DID_M continuo: beta = sum_{(g,t) con cambio} sign(dD)(dY - media de dY de los que no cambian en t) / sum |dD|; el año anterior a
  cada cambio no se usa como control (anticipación).
Inferencia: p-valor y IC por aleatorización: se reasignan los calendarios completos de tipo entre CCAA (B = 499 permutaciones al azar de
  las 11 CCAA/clusters); IC = beta +- cuantil 95 % de |beta permutado| (consistente con el contraste). No hay alternativa nombrada: si falla, NO APTO.
```

<!-- RESULTADOS -->
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
| escenario | beta | R | sesgo | rmse | cobertura | rechazo | ancho_medio_ic |
|---|---|---|---|---|---|---|---|
| nulo | 0.0000 | 2000 | 0.0002 | 0.0205 | 0.9225 | 0.0775 | 0.0698 |
| alt_vol_-0.07 | -0.0700 | 2000 | 0.0001 | 0.0215 | 0.9670 | 0.8720 | 0.0984 |
| alt_precio_-0.01 | -0.0100 | 1000 | -0.0008 | 0.0207 | 0.9250 | 0.1270 | 0.0698 |
| control_iid_nulo | 0.0000 | 1000 | 0.0004 | 0.0170 | 0.9240 | 0.0760 | 0.0565 |

## Veredicto
**NO APTO → diseño solo descriptivo**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{
 "principal": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": true,
  "fallos": [
   "tamaño 0.0775 fuera de [0,04; 0,06]"
  ],
  "tamano": 0.0775,
  "R_nulo": 2000,
  "cobertura_alt": 0.967,
  "R_alt": 2000,
  "cobertura_nulo": 0.9225,
  "sesgo_nulo": 0.0002181454105478,
  "rmse_nulo": 0.0205063355326322,
  "se_mc_tamano": 0.005978869040211535,
  "se_mc_cobertura": 0.003994433626936366
 }
}
```

## Notas y límites
Inferencia por aleatorización del calendario entre CCAA (11 clusters; 8 con cambios de tipo, 59 celdas de cambio). Q6 no tiene alternativa nombrada distinta: si falla, NO APTO. Tamaño 0.0775 (error MC 0.0060); cobertura bajo nulo 0.9225 y bajo beta=-0,07 0.9670. Control iid (sin factores, campos ni choques de CCAA): tamaño 0.076: el exceso de rechazo no viene de la dependencia simulada sino de que el calendario permutado no es intercambiable (distinto número de provincias por CCAA y calendarios con distinta dispersión de cambios). Potencia: 0.872 a -0,07 por punto (volumen) y 0.127 a -0,01 (precio). Con solo 8 CCAA con cambios la prueba tiene resolución limitada; cualquier uso de Q6 queda como descriptivo.

## Reproducción
`python3 src/v16/montecarlo/dcdh_aleatorizacion.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/dcdh_aleatorizacion/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.

# did_intensidad_webb · Q2a (provincial, Webb) y Q2c (municipal, agrupado por provincia)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** Q2a: 41 provincias de entrenamiento, periodos [2017, 2018, 2019, 2022, 2023, 2024, 2025] (2017-2019 frente a 2022-2025; 2020-2021 fuera), posterior = 2022+,
  distancias entre centroides de data/base/geo/provincias.parquet. Q2c: 391 municipios con IPVA de entrenamiento en 37 provincias (tamaños de cluster reales: de 1 a
  67 municipios), años [2021, 2022, 2023, 2024], posterior = 2023-2024 (la adenda fija «la misma regla que Q2a»; el corte 2023 es una convención de esta validación).
- **Exposición:** e_i ~ N(0,1) estandarizada (log de la exposición). Q2a: campo gaussiano con correlación espacial exp(-d/300 km). Q2c: 40 % de la varianza común dentro de la provincia, 60 % municipal, estandarizada.
- **Resultado Q2a:** y_it = β·e_i·post_t + σ_P·ε_it, σ_P = 0.05; ε_it = √0,5·η_it + √0,3·(λ_i1 f_t1 + λ_i2 f_t2)/√2 + √0,2·u_it con η_it espacial (correlación exp(-d/300 km) entre provincias, AR(1) ρ = 0,7 en t),
  f factores comunes AR(1) ρ = 0,7, cargas λ ~ N(0,1) independientes de la exposición (la tendencia paralela se cumple), u AR(1) ρ = 0,5.
- **Resultado Q2c:** y_it = β·e_i·post_t + σ_M·ε_it, σ_M = 0.08; ε_it = √0,35·v_{prov(i)}t (choque provincia-año común) + √0,15·f_t·λ_i + √0,5·u_it, con v, f AR(1) ρ = 0,5 y u AR(1) ρ = 0,3. Efectos fijos de unidad y de año (absorbidos).
- **Nulo:** β = 0. **Alternativa:** β = 0.04 (por DT de la exposición): sesgo, RMSE, cobertura (inversión de la prueba en β = 0.04) y potencia.
- **Inferencias.** Q2a: wild cluster bootstrap con residuos restringidos, pesos de Webb de 6 puntos, B = bootstrap-t simétrico por provincia (principal, punto 3); referencia no candidata: CR1 por provincia con t(G-1).
  Q2c: CR1 agrupado por provincia con t(G-1) (principal, punto 3); Webb por provincia se informa como referencia extra (NO es la alternativa nombrada para Q2c, que no tiene ninguna).
- **Pocos clusters:** G = 41 (Q2a) y 37 muy desiguales (Q2c). **T corto:** 7 y 4 periodos.
- **Alternativa nombrada:** Q2a: Webb es la principal, sin otra; Q2c: ninguna. Si la principal no pasa → «NO APTO → diseño solo descriptivo».
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97] (cobertura de la prueba bootstrap invertida en el valor verdadero).

<!-- RESULTADOS -->
## Resultados (R = 2000 réplicas por diseño, B = 399; semilla 20261010, k = 33)

| diseno | inferencia | R | tamano_5pct | tamano_ic95 | cobertura_95 | potencia_beta_ref | sesgo | rmse |
|---|---|---|---|---|---|---|---|---|
| Q2a provincial | Webb (principal) | 2000 | 0.1420 | [0.1267, 0.1573] | 0.8570 | 0.9955 | -0.0004 | 0.0087 |
| Q2a provincial | CR1 por provincia (referencia) | 2000 | 0.1720 | [0.1555, 0.1885] | 0.8280 | 0.9970 | -0.0004 | 0.0087 |
| Q2c municipal | CR1 por provincia (principal) | 2000 | 0.0975 | [0.0845, 0.1105] | 0.9025 | 0.9955 | -0.0000 | 0.0076 |
| Q2c municipal | Webb por provincia (referencia extra) | 2000 | 0.0605 | [0.0501, 0.0709] | 0.9375 | 0.9900 | -0.0000 | 0.0076 |


**Veredicto: Q2a NO APTO → diseño solo descriptivo; Q2c NO APTO → diseño solo descriptivo.**

- Q2a: condición que falla: tamaño 0.1420 fuera de [0.04; 0.06]; cobertura 0.8570 fuera de [0.92; 0.97].

- Q2c: condición que falla: tamaño 0.0975 fuera de [0.04; 0.06]; cobertura 0.9025 fuera de [0.92; 0.97].

**Comprobación puntual de la implementación (R = 600, B = 199, Q2a sin dependencia espacial entre provincias, resto igual):** tamaño de Webb 0,043 y de CR1 0,085. El bootstrap está bien implementado; el sobre-rechazo de Webb en el proceso del repositorio (0,142) procede de la correlación espacial entre provincias en la exposición y en el error, que el agrupamiento por provincia no recoge. Q2a queda como diseño solo descriptivo. En Q2c el CR1 por provincia sobre-rechaza (0,0975); Webb por provincia (0,0605, referencia extra, no es la alternativa nombrada) tampoco entra en [0,04; 0,06].

# Validación Monte Carlo V16 · dm_hln (Q10, Diebold-Mariano con HLN; alternativa Clark-West)

Código: `src/v16/montecarlo/dm_hln.py` · semilla `default_rng([20261010, 4, k])`.

## Proceso generador (declarado antes de simular)
- **Dimensiones:** h = 1; ventana expansiva con 30 observaciones iniciales y P = 75 errores fuera de muestra.
- **Verdad:** y_t = 0,1 + 0,5 y_t-1 + 0,1 y_t-2 + 0,05 y_t-3 − 0,05 y_t-4 + β x_t-1 + e_t, e ~ N(0,1), x AR(1) con 0,3 (valores declarados, no calibrados con datos reales).
- **Modelos (anidados):** AR(4) con constante frente a AR(4) + x_t-1, reestimados cada periodo por MCO.
- **Nulo:** β = 0 (el modelo grande añade un regresor irrelevante: caso anidado clásico en que DM sobrerrechaza o subrechaza). **Alternativa:** β = 1/3 (reducción poblacional del ECM ≈ 10 %, la relevancia mínima de la adenda).
- **Pruebas:** DM-HLN (t con P−1 g. de l.; unilateral, H1: el modelo grande reduce el ECM; también bilateral); DM con normal; Clark-West (normal y t) como alternativa nombrada para pares anidados.
- **Réplicas:** 2.000 bajo el nulo, 1.000 bajo la alternativa.

<!-- RESULTADOS -->
## Resultados (R=2000 bajo el nulo, 1.000 bajo la alternativa)

| escenario       |    R |   tam_HLN_unilateral |   tam_HLN_bilateral |   tam_DM_normal_unilateral |   CW_normal_unilateral |   CW_t_unilateral |   reduccion_ECM_media |
|:----------------|-----:|---------------------:|--------------------:|---------------------------:|-----------------------:|------------------:|----------------------:|
| nulo_anidado    | 2000 |                0.002 |               0.069 |                      0.002 |                  0.033 |             0.032 |            -0.0214849 |
| alt_reduccion10 | 1000 |                0.277 |               0.167 |                      0.287 |                  0.824 |             0.82  |             0.0838235 |

**Veredicto: NO APTO → diseño solo descriptivo** tamaño 0.0020 fuera de [0.04; 0.06]; Clark-West: tamaño 0.0330 fuera de [0.04; 0.06]

# Validación Monte Carlo V16 · gsadf_factor (Q9-g, GSADF sobre el factor común)

Código: `src/v16/montecarlo/gsadf_factor.py` · semilla `default_rng([20261010, 3, k])`.

## Proceso generador (declarado antes de simular)
- **Dimensión:** serie agregada de T = 98 trimestres; ventana mínima r0 = ⌊T(0,01 + 1,8/√T)⌋ = 18.
- **Nulo (raíz unitaria):** y_t = y_t-1 + σ_t ε_t, ε ~ N(0,1). Tres escenarios de volatilidad: homocedástico; **salto** (σ = 3 entre el 40 % y el 75 % de la muestra, 1 fuera); **estocástica** (log σ AR(1) con 0,9 y desviación 0,35).
- **Alternativa:** episodio explosivo ρ = 1,05 durante 15 trimestres (desde el 45 %) con colapso posterior, en volatilidad homocedástica y con salto.
- **Estadístico:** supremo de las t de ADF (sin rezagos, con constante) sobre todas las ventanas (inicio, fin) con longitud ≥ r0.
- **Inferencia:** bootstrap wild (Harvey et al. 2016): Δy* = Δy·w, w ~ N(0,1), raíz unitaria impuesta, B = 499; VC = cuantil 95 %. Se informa también el VC iid simulado (1.000 réplicas) para ver qué pasaría sin bootstrap.
- **Réplicas:** 2.000 bajo cada nulo, 500 bajo cada alternativa. Cobertura: no aplica.

<!-- RESULTADOS -->
## Resultados (R=2000 bajo el nulo, 500 bajo la alternativa, B=499)

| escenario   |    R |   rech_boot_wild |   rech_cv_iid_simulado |
|:------------|-----:|-----------------:|-----------------------:|
| nulo_homo   | 2000 |           0.017  |                 0.052  |
| nulo_salto  | 2000 |           0.0455 |                 0.288  |
| nulo_estoc  | 2000 |           0.0455 |                 0.3715 |
| alt_homo    |  500 |           0.064  |                 0.202  |
| alt_salto   |  500 |           0.132  |                 0.454  |

VC al 95 % iid simulado: 1.915. **Veredicto: APTO** nulo_homo: tamaño 0.0170 fuera de [0.04; 0.06]

# lp_newey_west_b · Q5-p y Q5-a (proyección local nacional, Newey-West con b fija)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** serie nacional trimestral, T = 100 (la ventana de Q5 es 1999T1/2002T1-2026T2, 98-110 trimestres); horizontes h = [1, 4, 8, 12].
- **Choque:** ε_t i.i.d. N(0,1), exógeno (equivale a la sorpresa estandarizada de Jarociński-Karadi agregada a trimestre; sin autocorrelación ni heterocedasticidad).
- **Resultado:** y_t = ρ·y_(t-1) + θ·ε_t + σ_u·u_t, u_t i.i.d. N(0,1), σ_u = 0.01 (log, trimestral), con 100 periodos de calentamiento. ρ ∈ [0.9, 0.95, 0.98] (persistencia alta, intervalo 0,90-0,98 de la tarea).
  Respuesta verdadera a h: β_h = θ·ρ^h. Nulo: θ = 0. Alternativa: θ = -0.006/ρ^4, de modo que β_4 = -0.006 (−0,6 % por DT, magnitud de referencia de Q5-p) y β_h = θρ^h para el resto.
- **Estimación:** para cada h, MCO de y_(t+h) sobre constante, ε_t, 4 rezagos de ε y 4 rezagos de y (n = T − h − 4 observaciones). Coeficiente de interés: el de ε_t.
- **Inferencia principal:** Newey-West con núcleo de Bartlett y ancho de banda fijo M = b·n con b = 0.2 (Kiefer-Vogelsang), valor crítico bilateral al 5 % de la distribución límite de b fija
  simulada (b = 0.2: 2.538). Declarado antes de simular; se informa también b = 1,0 (valor crítico 4.793) y Newey-West convencional (M = 4, normal) como referencias, no candidatas.
- **Pocos clusters / dependencia transversal:** no aplica (serie nacional única). **T corto:** n entre 84 y 95.
- **Alternativa nombrada en el punto 3:** ninguna distinta (b fija es la principal). Si algún (ρ, h) falla, el veredicto es «NO APTO» para la combinación; con fallos «NO APTO → diseño solo descriptivo».
- **Criterio:** en cada una de las 12 combinaciones (ρ, h): tamaño en [0,04; 0,06] con R ≥ 2.000 (aquí R = 10.000, para que el error Monte Carlo ≈ 0,002 no domine el intervalo) y cobertura en [0,92; 0,97] bajo la alternativa.
  El veredicto global es APTO solo si pasan las 12 combinaciones.

<!-- RESULTADOS -->
## Resultados (R = 10000 por ρ; semilla 20261010, k = 34)

| rho | h | inferencia | R | tamano_5pct | tamano_ic95 | cobertura_95 | potencia | sesgo | rmse | beta_verdadero |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.9000 | 1 | b=0.2 | 10000 | 0.0698 | [0.0648, 0.0748] | 0.9270 | 0.9830 | 0.0002 | 0.0018 | -0.0082 |
| 0.9000 | 1 | b=1.0 | 10000 | 0.0653 | [0.0605, 0.0701] | 0.9301 | 0.9334 | 0.0002 | 0.0018 | -0.0082 |
| 0.9000 | 1 | NW M=4 normal | 10000 | 0.0883 | [0.0827, 0.0939] | 0.9030 | 0.9960 | 0.0002 | 0.0018 | -0.0082 |
| 0.9000 | 4 | b=0.2 | 10000 | 0.0834 | [0.078, 0.0888] | 0.8941 | 0.5313 | 0.0007 | 0.0028 | -0.0060 |
| 0.9000 | 4 | b=1.0 | 10000 | 0.0780 | [0.0727, 0.0833] | 0.9002 | 0.4543 | 0.0007 | 0.0028 | -0.0060 |
| 0.9000 | 4 | NW M=4 normal | 10000 | 0.1081 | [0.102, 0.1142] | 0.8725 | 0.6271 | 0.0007 | 0.0028 | -0.0060 |
| 0.9000 | 8 | b=0.2 | 10000 | 0.0871 | [0.0816, 0.0926] | 0.8643 | 0.1833 | 0.0010 | 0.0033 | -0.0039 |
| 0.9000 | 8 | b=1.0 | 10000 | 0.0828 | [0.0774, 0.0882] | 0.8778 | 0.1663 | 0.0010 | 0.0033 | -0.0039 |
| 0.9000 | 8 | NW M=4 normal | 10000 | 0.1111 | [0.1049, 0.1173] | 0.8356 | 0.2395 | 0.0010 | 0.0033 | -0.0039 |
| 0.9000 | 12 | b=0.2 | 10000 | 0.0894 | [0.0838, 0.095] | 0.8772 | 0.1087 | 0.0011 | 0.0035 | -0.0026 |
| 0.9000 | 12 | b=1.0 | 10000 | 0.0800 | [0.0747, 0.0853] | 0.8862 | 0.0990 | 0.0011 | 0.0035 | -0.0026 |
| 0.9000 | 12 | NW M=4 normal | 10000 | 0.1160 | [0.1097, 0.1223] | 0.8418 | 0.1430 | 0.0011 | 0.0035 | -0.0026 |
| 0.9500 | 1 | b=0.2 | 10000 | 0.0642 | [0.0594, 0.069] | 0.9313 | 0.9560 | 0.0002 | 0.0017 | -0.0070 |
| 0.9500 | 1 | b=1.0 | 10000 | 0.0601 | [0.0554, 0.0648] | 0.9372 | 0.8769 | 0.0002 | 0.0017 | -0.0070 |
| 0.9500 | 1 | NW M=4 normal | 10000 | 0.0843 | [0.0789, 0.0897] | 0.9095 | 0.9829 | 0.0002 | 0.0017 | -0.0070 |
| 0.9500 | 4 | b=0.2 | 10000 | 0.0749 | [0.0697, 0.0801] | 0.8962 | 0.5220 | 0.0007 | 0.0028 | -0.0060 |
| 0.9500 | 4 | b=1.0 | 10000 | 0.0721 | [0.067, 0.0772] | 0.9032 | 0.4461 | 0.0007 | 0.0028 | -0.0060 |
| 0.9500 | 4 | NW M=4 normal | 10000 | 0.1014 | [0.0955, 0.1073] | 0.8719 | 0.6193 | 0.0007 | 0.0028 | -0.0060 |
| 0.9500 | 8 | b=0.2 | 10000 | 0.0829 | [0.0775, 0.0883] | 0.8632 | 0.2373 | 0.0012 | 0.0035 | -0.0049 |
| 0.9500 | 8 | b=1.0 | 10000 | 0.0784 | [0.0731, 0.0837] | 0.8790 | 0.2078 | 0.0012 | 0.0035 | -0.0049 |
| 0.9500 | 8 | NW M=4 normal | 10000 | 0.1102 | [0.1041, 0.1163] | 0.8359 | 0.3008 | 0.0012 | 0.0035 | -0.0049 |
| 0.9500 | 12 | b=0.2 | 10000 | 0.0876 | [0.0821, 0.0931] | 0.8457 | 0.1429 | 0.0015 | 0.0040 | -0.0040 |
| 0.9500 | 12 | b=1.0 | 10000 | 0.0808 | [0.0755, 0.0861] | 0.8576 | 0.1279 | 0.0015 | 0.0040 | -0.0040 |
| 0.9500 | 12 | NW M=4 normal | 10000 | 0.1155 | [0.1092, 0.1218] | 0.8094 | 0.1839 | 0.0015 | 0.0040 | -0.0040 |
| 0.9800 | 1 | b=0.2 | 10000 | 0.0686 | [0.0636, 0.0736] | 0.9240 | 0.9203 | 0.0003 | 0.0017 | -0.0064 |
| 0.9800 | 1 | b=1.0 | 10000 | 0.0643 | [0.0595, 0.0691] | 0.9281 | 0.8340 | 0.0003 | 0.0017 | -0.0064 |
| 0.9800 | 1 | NW M=4 normal | 10000 | 0.0884 | [0.0828, 0.094] | 0.9016 | 0.9634 | 0.0003 | 0.0017 | -0.0064 |
| 0.9800 | 4 | b=0.2 | 10000 | 0.0788 | [0.0735, 0.0841] | 0.8894 | 0.5035 | 0.0008 | 0.0029 | -0.0060 |
| 0.9800 | 4 | b=1.0 | 10000 | 0.0725 | [0.0674, 0.0776] | 0.8964 | 0.4236 | 0.0008 | 0.0029 | -0.0060 |
| 0.9800 | 4 | NW M=4 normal | 10000 | 0.1060 | [0.1, 0.112] | 0.8638 | 0.6063 | 0.0008 | 0.0029 | -0.0060 |
| 0.9800 | 8 | b=0.2 | 10000 | 0.0874 | [0.0819, 0.0929] | 0.8472 | 0.2594 | 0.0015 | 0.0038 | -0.0055 |
| 0.9800 | 8 | b=1.0 | 10000 | 0.0787 | [0.0734, 0.084] | 0.8601 | 0.2298 | 0.0015 | 0.0038 | -0.0055 |
| 0.9800 | 8 | NW M=4 normal | 10000 | 0.1116 | [0.1054, 0.1178] | 0.8143 | 0.3270 | 0.0015 | 0.0038 | -0.0055 |
| 0.9800 | 12 | b=0.2 | 10000 | 0.0925 | [0.0868, 0.0982] | 0.8130 | 0.1739 | 0.0020 | 0.0045 | -0.0051 |
| 0.9800 | 12 | b=1.0 | 10000 | 0.0856 | [0.0801, 0.0911] | 0.8308 | 0.1507 | 0.0020 | 0.0045 | -0.0051 |
| 0.9800 | 12 | NW M=4 normal | 10000 | 0.1217 | [0.1153, 0.1281] | 0.7750 | 0.2171 | 0.0020 | 0.0045 | -0.0051 |


**Veredicto: NO APTO → diseño solo descriptivo.**

Combinaciones (ρ, h) que fallan con b = 0,2:
- rho=0.9, h=1: tamaño 0.0698 fuera de [0.04; 0.06]
- rho=0.9, h=4: tamaño 0.0834 fuera de [0.04; 0.06]; cobertura 0.8941 fuera de [0.92; 0.97]
- rho=0.9, h=8: tamaño 0.0871 fuera de [0.04; 0.06]; cobertura 0.8643 fuera de [0.92; 0.97]
- rho=0.9, h=12: tamaño 0.0894 fuera de [0.04; 0.06]; cobertura 0.8772 fuera de [0.92; 0.97]
- rho=0.95, h=1: tamaño 0.0642 fuera de [0.04; 0.06]
- rho=0.95, h=4: tamaño 0.0749 fuera de [0.04; 0.06]; cobertura 0.8962 fuera de [0.92; 0.97]
- rho=0.95, h=8: tamaño 0.0829 fuera de [0.04; 0.06]; cobertura 0.8632 fuera de [0.92; 0.97]
- rho=0.95, h=12: tamaño 0.0876 fuera de [0.04; 0.06]; cobertura 0.8457 fuera de [0.92; 0.97]
- rho=0.98, h=1: tamaño 0.0686 fuera de [0.04; 0.06]
- rho=0.98, h=4: tamaño 0.0788 fuera de [0.04; 0.06]; cobertura 0.8894 fuera de [0.92; 0.97]
- rho=0.98, h=8: tamaño 0.0874 fuera de [0.04; 0.06]; cobertura 0.8472 fuera de [0.92; 0.97]
- rho=0.98, h=12: tamaño 0.0925 fuera de [0.04; 0.06]; cobertura 0.8130 fuera de [0.92; 0.97]

# rejilla_twfe · especificación principal de la rejilla fija (TWFE, exposición continua)

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/rejilla_twfe.py)
```
Monte Carlo V16 (fase 5) · TWFE de la rejilla fija (output/v16/potencia/rejilla_fija.csv), dos escalas representativas.

Proceso generador (declarado en docs/v16/validacion_montecarlo/rejilla_twfe.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): MUNICIPIO = unidades de entrenamiento con SERPAVI (2.014; clusters = su provincia);
  PROVINCIA = las 41 provincias de entrenamiento (cada una es su cluster). Ventana 2019-2025 (7 años => 6 diferencias).
  Especificación principal (rejilla): Dlog resultado_it = a_i + l_t + b x_it + u_it, con x_it = z_i * 1[t >= 2023] (exposición continua
  estandarizada, DiD de intensidad), efectos fijos de unidad y de periodo.
  EXPOSICIÓN z_i: campo gaussiano espacial estandarizado (alcance 150 km municipal; 300 km provincial) => correlación espacial.
  RESULTADO SIMULADO (log, en niveles; se toman diferencias): y_it = mu_i + d_i t + g_i1 f_1t + g_i2 f_2t + eta_p(i),t + s_it + e_it
    municipio: f AR(1) rho 0,6 sd 0,03; g_i1 ~ N(1; 0,5); g_i2 campo (150 km) N(0,1); eta provincia-año AR(1) rho 0,5 sd 0,02;
      s_it campo exp(-d/100 km) AR(1) rho 0,5 sd 0,02; e_it AR(1) rho 0,5 sd 0,05 exp(0,4 z_h - 0,08); d_i ~ N(0; 0,005)
    provincia: f AR(1) rho 0,6 sd 0,05; g_i1 ~ N(1; 0,4); g_i2 campo (300 km) N(0; 0,5); s_it campo (150 km) AR(1) 0,5 sd 0,03;
      e_it AR(1) rho 0,5 sd 0,05 exp(0,3 z_h - 0,045); d_i ~ N(0; 0,003)
  EFECTO sobre el crecimiento: nulo b = 0; alternativas b = 0,04 (magnitud de referencia Q2: 0,04 por DT de exposición; cobertura) y
  b = 0,01 (potencia); heterogeneidad b_i = b (1 + 0,5 z_h); verdad = media de b_i ponderada por x_it^2 (la que estima TWFE sin sesgo si
  b_i es independiente de x).
Inferencia: municipio = errores agrupados por provincia (CR1, t con G-1 gl); provincia = wild cluster bootstrap-t de Webb con el nulo
  impuesto (B = 999), cluster = provincia. Informativo (no cambia el veredicto): wild de Webb en la escala municipal no se calcula.
```

<!-- RESULTADOS -->
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
| escala | escenario | b | n_unidades | n_clusters | R | sesgo | rmse | cobertura | rechazo | ancho_medio_ic |
|---|---|---|---|---|---|---|---|---|---|---|
| municipio | nulo | 0.0000 | 2014 | 41 | 2000 | 0.0001 | 0.0052 | 0.7970 | 0.2030 | 0.0126 |
| municipio | alt_ref_0.04 | 0.0400 | 2014 | 41 | 2000 | 0.0001 | 0.0056 | 0.8055 | 0.9995 | 0.0132 |
| municipio | alt_pot_0.01 | 0.0100 | 2014 | 41 | 1000 | -0.0001 | 0.0056 | 0.7970 | 0.7800 | 0.0129 |
| municipio | control_iid_nulo | 0.0000 | 2014 | 41 | 1000 | -0.0000 | 0.0009 | 0.9490 | 0.0510 | 0.0036 |
| provincia | nulo | 0.0000 | 41 | 41 | 2000 | 0.0001 | 0.0092 | 0.8890 | 0.1105 | 0.0308 |
| provincia | alt_ref_0.04 | 0.0400 | 41 | 41 | 2000 | 0.0000 | 0.0092 | 0.9545 | 0.9600 | 0.0398 |
| provincia | alt_pot_0.01 | 0.0100 | 41 | 41 | 1000 | -0.0002 | 0.0092 | 0.9130 | 0.2780 | 0.0319 |
| provincia | control_iid_nulo | 0.0000 | 41 | 41 | 1000 | -0.0001 | 0.0066 | 0.9540 | 0.0440 | 0.0278 |

## Veredicto
**municipio: NO APTO → diseño solo descriptivo; provincia: NO APTO → diseño solo descriptivo**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{
 "municipio": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.2030 fuera de [0,04; 0,06]",
   "cobertura 0.8055 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.203,
  "R_nulo": 2000,
  "cobertura_alt": 0.8055,
  "R_alt": 2000,
  "cobertura_nulo": 0.797,
  "sesgo_nulo": 8.460748974844136e-05,
  "rmse_nulo": 0.005193202568052,
  "se_mc_tamano": 0.00899419257076476,
  "se_mc_cobertura": 0.00885069912492793
 },
 "provincia": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": true,
  "fallos": [
   "tamaño 0.1105 fuera de [0,04; 0,06]"
  ],
  "tamano": 0.1105,
  "R_nulo": 2000,
  "cobertura_alt": 0.9545,
  "R_alt": 2000,
  "cobertura_nulo": 0.889,
  "sesgo_nulo": 9.559865025309044e-05,
  "rmse_nulo": 0.0091650654084672,
  "se_mc_tamano": 0.0070103405766053905,
  "se_mc_cobertura": 0.004659922209651143
 }
}
```

## Notas y límites
Escalas representativas de la especificación principal de la rejilla: municipio (2014 unidades, 41 provincias, CR1 con t(G-1)) y provincia (41, wild bootstrap-t de Webb con nulo impuesto). La adenda no nombra alternativa para la rejilla: si la principal falla, la escala es solo descriptiva. Tamaño municipal 0.2030, provincial 0.1105; cobertura bajo b=0,04: 0.8055 y 0.9545. Control iid (exposición y ruido independientes): tamaño 0.051 (municipio) y 0.044 (provincia), de modo que el procedimiento está bien implementado y el exceso de rechazo procede de la correlación espacial de la exposición con cargas de factores y choques espaciales que cruzan fronteras de provincia (el agrupamiento por provincia no los absorbe). Potencia: municipio {'b=0.04': 0.9995, 'b=0.01': 0.78}, provincia {'b=0.04': 0.96, 'b=0.01': 0.278}. Consecuencia: las 83 celdas de la rejilla con TWFE y exposición espacial no deben llevar p-valor calibrado; se leen como descriptivas, o con una inferencia espacial (Conley) validada aparte.

## Reproducción
`python3 src/v16/montecarlo/rejilla_twfe.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/rejilla_twfe/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.

# sdid_conley_taber · Q1b · SDID con Conley-Taber (principal) y wild bootstrap de Webb (alternativa)

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/sdid_conley_taber.py)
```
Monte Carlo V16 (fase 5) · SDID con inferencia de Conley-Taber (principal) y wild cluster bootstrap de Webb (alternativa), Q1b.

Proceso generador (declarado en docs/v16/validacion_montecarlo/sdid_conley_taber.md ANTES de simular):
  ESTRUCTURA (leída de entrenamiento y de intervenciones.csv, sin valores del resultado): municipios de entrenamiento con SERPAVI completo
  en 2019-2022 y 2024; tratados = municipios con zona tensionada declarada fuera de Cataluña; donantes = municipios de CCAA sin zonas;
  clusters = provincia; años 2019..2024 con 2023 fuera del estimador (pre 2019-2022, post 2024).
  RESULTADO SIMULADO (log SERPAVI €/m²): y_it = mu_i + d_i*t + sum_k g_ik f_kt + eta_{p(i),t} + s_it + e_it
    f_1, f_2 factores comunes AR(1) rho 0,6, sd 0,03; g_i1 ~ N(1; 0,5), g_i2 = campo espacial (alcance 150 km) N(0,1)
    eta: choque provincia-año AR(1) rho 0,5, sd 0,02;  s_it: campo gaussiano espacial exp(-d/100 km), AR(1) rho 0,5, sd 0,02
    e_it: AR(1) rho 0,5, sd marginal 0,05 * exp(0,4 z_i - 0,08) (heterocedasticidad entre municipios)
    d_i ~ N(0; 0,005) tendencia propia. Valores declarados, no estimados con datos reales.
  EFECTO (solo en el año post): nulo = 0; alternativa = -0,0075 (magnitud de referencia de la adenda) con heterogeneidad
  tau_i = tau (1 + 0,5 z_i); la verdad de la cobertura es el ATT muestral (media de tau_i en tratados).
Escenarios: A (estructura real: 2 tratados, 1 provincia) y B (diseño ampliado: patrón de las 8 zonas declaradas 15:2, 20:2, 48:3, 01:1).
```

<!-- RESULTADOS -->
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
| escenario | inferencia | efecto | n_tratados | n_donantes | R | sesgo | rmse | cobertura | rechazo | ancho_medio_ic |
|---|---|---|---|---|---|---|---|---|---|---|
| A | ct | nulo | 2 | 930 | 2000 | -0.0016 | 0.0588 | 0.9425 | 0.0575 | 0.2297 |
| A | webb | nulo | 2 | 930 | 2000 | -0.0016 | 0.0588 | 0.2205 | 0.7795 | 0.0263 |
| A | ct | ref | 2 | 930 | 1000 | -0.0011 | 0.0591 | 0.9430 | 0.0620 | 0.2280 |
| A | webb | ref | 2 | 930 | 1000 | -0.0011 | 0.0591 | 0.2070 | 0.8180 | 0.0266 |
| A | ct | mde | 2 | 930 | 300 | -0.0045 | 0.0580 | 0.9567 | 0.3233 | 0.2277 |
| A | webb | mde | 2 | 930 | 300 | -0.0045 | 0.0580 | 0.1567 | 0.9000 | 0.0220 |
| B | ct | nulo | 2 | 930 | 2000 | -0.0017 | 0.0605 | 0.9350 | 0.0650 | 0.2294 |
| B | webb | nulo | 2 | 930 | 2000 | -0.0017 | 0.0605 | 0.2080 | 0.7920 | 0.0264 |
| B | ct | ref | 2 | 930 | 1000 | -0.0010 | 0.0608 | 0.9290 | 0.0760 | 0.2274 |
| B | webb | ref | 2 | 930 | 1000 | -0.0010 | 0.0608 | 0.1970 | 0.7990 | 0.0270 |
| B | ct | mde | 2 | 930 | 300 | -0.0050 | 0.0577 | 0.9600 | 0.3167 | 0.2275 |
| B | webb | mde | 2 | 930 | 300 | -0.0050 | 0.0577 | 0.1433 | 0.9033 | 0.0228 |

## Veredicto
**APTO (Conley-Taber, escenario A; en el límite superior del tamaño, ver notas)**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{
 "A_ct": {
  "apto": true,
  "tamano_ok": true,
  "cobertura_ok": true,
  "fallos": [],
  "tamano": 0.0575,
  "R_nulo": 2000,
  "cobertura_alt": 0.943,
  "R_alt": 1000,
  "cobertura_nulo": 0.9425,
  "sesgo_nulo": -0.0016154805824415,
  "rmse_nulo": 0.0587989633217807,
  "se_mc_tamano": 0.005205465877325487,
  "se_mc_cobertura": 0.007331507348424336
 },
 "A_webb": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.7795 fuera de [0,04; 0,06]",
   "cobertura 0.2070 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.7795,
  "R_nulo": 2000,
  "cobertura_alt": 0.207,
  "R_alt": 1000,
  "cobertura_nulo": 0.2205,
  "sesgo_nulo": -0.0016154805824415,
  "rmse_nulo": 0.0587989633217807,
  "se_mc_tamano": 0.009270376205958419,
  "se_mc_cobertura": 0.012812142677944232
 },
 "B_ct": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": true,
  "fallos": [
   "tamaño 0.0650 fuera de [0,04; 0,06]"
  ],
  "tamano": 0.065,
  "R_nulo": 2000,
  "cobertura_alt": 0.929,
  "R_alt": 1000,
  "cobertura_nulo": 0.935,
  "sesgo_nulo": -0.0016752745748473,
  "rmse_nulo": 0.0605052989557364,
  "se_mc_tamano": 0.005512485827646181,
  "se_mc_cobertura": 0.008121514637061239
 },
 "B_webb": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.7920 fuera de [0,04; 0,06]",
   "cobertura 0.1970 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.792,
  "R_nulo": 2000,
  "cobertura_alt": 0.197,
  "R_alt": 1000,
  "cobertura_nulo": 0.208,
  "sesgo_nulo": -0.0016752745748473,
  "rmse_nulo": 0.0605052989557364,
  "se_mc_tamano": 0.009075681792570737,
  "se_mc_cobertura": 0.012577400367325514
 }
}
```

## Notas y límites
Hallazgo de estructura: con los datos de entrenamiento, el diseño literal de la adenda (tratados = municipios con zona vigente fuera de Cataluña, con SERPAVI completo 2019-2022 y 2024) tiene 2 municipios en 1 provincia (['15']) y 930 donantes en 30 provincias; las zonas de esos dos municipios entran en vigor en 2025-2026, es decir, DESPUÉS del año post (2024): en entrenamiento hay 0 municipios con zona vigente en 2024 fuera de Cataluña. El resto de zonas fuera de Cataluña (Álava, Gipuzkoa, Bizkaia) está en territorios forales sin SERPAVI, por lo que el escenario B del docstring (reparto 15:2, 20:2, 48:3, 01:1) no pudo construirse y resultó ser el mismo conjunto de 2 tratados con otra realización de la geometría simulada (B = réplica independiente de A, no un diseño distinto). Veredicto sobre A (proceso del repositorio, declarado antes de simular). Resultados A: Conley-Taber tamaño 0.0575 (error MC 0.0052), cobertura bajo tau=-0,0075 0.9430, bajo el nulo 0.9425. La réplica B queda fuera del intervalo (tamaño 0.0650, cobertura 0.9290); agrupando A y B (4.000 réplicas nulas) el tamaño es 0.0612 (error MC 0.0038): la calibración es CASI en el límite del criterio, no holgada. Alternativa Webb (solo se informa): tamaño 0.7795 y cobertura 0.2070; con un único cluster tratado el bootstrap degenera (no se debe usar). Potencia de Conley-Taber a -7,1 % (MDE de la adenda): 0.323; a -0,75 % es prácticamente el tamaño. El IC medio mide 0.230 de ancho (en log): con 2 municipios tratados el diseño no distingue efectos de la magnitud de la literatura y su lectura es la de un nulo no concluyente. Los pesos SDID se estiman por FISTA (40 iteraciones) con regularización a la Arkhangelsky et al.; en la alternativa Webb los pesos se mantienen fijos.

## Reproducción
`python3 src/v16/montecarlo/sdid_conley_taber.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/sdid_conley_taber/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.

# shiftshare_akm · Q3-c1 y Q3-c2 (shift-share en forma reducida, inferencia AKM)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** 41 provincias de entrenamiento × 14 años (2011-2024); 28 orígenes
  (nacionalidades individuales del padrón de 2003, sin agregados); cuotas s_ik = población de nacionalidad k / población total de la provincia i en 2003
  (data/processed/v16/entrenamiento/padron_nacionalidad.parquet, agregado de municipio a provincia). Número efectivo de choques 1/HHI de las ponderaciones de Rotemberg-tipo
  (cuota agregada de cada origen) = **9.3** (la adenda prevé ≈ 12).
- **Regresor:** x_it = c · Σ_k s_ik g_kt, con g_kt = choque nacional del origen k (N(0,1) independiente entre orígenes, AR(1) en t con ρ = 0.5); c fija la DT de x
  tras quitar efectos fijos a ≈ 0.1 puntos (unidad: punto de población extranjera predicha).
- **Resultado:** y_it = β x_it + σ·ε_it, σ = 0.15; ε_it = √0,5·A_it + √0,2·π_i f_t + √0,3·e_it, con
  A_it = Σ_k s_ik u_kt / norma (choques de origen NO observados u_kt, independientes de g_kt pero con las mismas cuotas: dependencia transversal por cuota, AR(1) ρ = 0.5),
  f_t factor común AR(1) ρ = 0.7 con cargas π_i ~ N(0,1), e_it AR(1) ρ = 0.5. Los efectos fijos de provincia y año se absorben y no se simulan.
- **Nulo:** β = 0 (tamaño). **Alternativa:** β = 1.0 (magnitud de referencia de Q3-c1, elasticidad de Saiz por punto): sesgo, RMSE, cobertura y potencia.
- **Estimación:** MCO con efectos fijos de provincia y año (TWFE). Inferencias: (a) AKM (varianza por choque, normal); (b) AKM0 (inversión de la prueba con residuos bajo el nulo, normal);
  (c) EE agrupados por provincia, t(40): solo como referencia del sobre-rechazo, no es candidata.
- **Sensibilidad (informativa):** peso de A en ε de 0,25 y 0,75. El veredicto usa el escenario principal (0,5).
- **Pocos clusters / T corto:** 41 provincias, 14 años, 28 choques (≈ 9 efectivos).
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97]. Alternativa nombrada en el punto 3: ninguna distinta de AKM en la tabla; AKM0 se prueba como variante de la misma familia (se declara aquí; si AKM falla y AKM0 pasa, el veredicto es «alternativa APTA (AKM0)»).

<!-- RESULTADOS -->
## Resultados (R = 5000 réplicas en el escenario principal; semilla 20261010, k = 31)

| escenario | inferencia | R | tamano_5pct | tamano_ic95 | cobertura_95 | potencia_beta1 | sesgo | rmse | longitud_ic_mediana | ic_acotado |
|---|---|---|---|---|---|---|---|---|---|---|
| principal wA=0,5 | convencional (EE por provincia) | 5000 | 0.4520 | [0.4382, 0.4658] | 0.5480 | 0.9936 | -0.0056 | 0.2491 | nan | 1.0000 |
| principal wA=0,5 | AKM | 5000 | 0.3762 | [0.3628, 0.3896] | 0.6238 | 0.9848 | -0.0056 | 0.2491 | 0.4178 | 1.0000 |
| principal wA=0,5 | AKM0 | 5000 | 0.0108 | [0.0079, 0.0137] | 0.9892 | 0.1242 | -0.0056 | 0.2491 | 2.3846 | 0.0682 |
| sens wA=0,25 | convencional (EE por provincia) | 2500 | 0.3580 | [0.3392, 0.3768] | 0.6420 | 0.9980 | 0.0037 | 0.1949 | nan | 1.0000 |
| sens wA=0,25 | AKM | 2500 | 0.3560 | [0.3372, 0.3748] | 0.6440 | 0.9956 | 0.0037 | 0.1949 | 0.3400 | 1.0000 |
| sens wA=0,25 | AKM0 | 2500 | 0.0092 | [0.0055, 0.0129] | 0.9908 | 0.1132 | 0.0037 | 0.1949 | 1.9432 | 0.0696 |
| sens wA=0,75 | convencional (EE por provincia) | 2500 | 0.5068 | [0.4872, 0.5264] | 0.4932 | 0.9824 | 0.0071 | 0.3078 | nan | 1.0000 |
| sens wA=0,75 | AKM | 2500 | 0.4128 | [0.3935, 0.4321] | 0.5872 | 0.9644 | 0.0071 | 0.3078 | 0.4788 | 1.0000 |
| sens wA=0,75 | AKM0 | 2500 | 0.0092 | [0.0055, 0.0129] | 0.9908 | 0.1296 | 0.0071 | 0.3078 | 2.6237 | 0.0696 |


**Veredicto: NO APTO → diseño solo descriptivo.**

- AKM: NO APTO — tamaño 0.3762 fuera de [0.04; 0.06]; cobertura 0.6238 fuera de [0.92; 0.97]
- AKM0: NO APTO — tamaño 0.0108 fuera de [0.04; 0.06]; cobertura 0.9892 fuera de [0.92; 0.97]
- convencional (EE por provincia): NO APTO — tamaño 0.4520 fuera de [0.04; 0.06]; cobertura 0.5480 fuera de [0.92; 0.97]

**Lectura.** Con n efectivo de choques = 9.3 las cuotas están concentradas en pocos orígenes: el EE por provincia ignora la dependencia por cuota (sobre-rechazo), AKM subestima la varianza porque el residuo estimado absorbe el choque dominante (A_k - b·B_k ≈ 0) y AKM0 queda en el extremo conservador (el estadístico autonormalizado con pocos términos dominantes rara vez supera 1,96). Ninguna pasa [0,04; 0,06]: el diseño es solo descriptivo.

# Validación Monte Carlo V16 · tost (equivalencia, nulo informativo, adenda punto 10)

Código: `src/v16/montecarlo/tost.py` · semilla `default_rng([20261010, 8, k])`.

## Proceso generador (declarado antes de simular)
- **Estimación:** θ̂ ~ N(θ, EE²) con EE estimado con df grados de libertad (12 ≈ 13 provincias agrupadas, 37 ≈ N−1 con N = 38, e infinito = EE conocido).
- **Prueba:** TOST al 5 % (dos pruebas t unilaterales frente a ±Δ; equivale a que el IC al 90 % quede dentro de (−Δ, Δ)).
- **Tamaño:** en el borde θ = ±Δ, para Δ/EE ∈ {0,5; 1; 1,5; 2; 2,5; 3; 3,5; 4; 5; 6; 8}. Potencia en θ = 0 y θ = Δ/2.
- **Proceso del repositorio:** Δ = magnitud de referencia (`ref_pct`) y EE = MDE80/2,8 de `output/v16/potencia/potencia.csv` (15 filas con ambos); se evalúa en qué razones Δ/EE cae el repositorio.
- **R = 20.000** por celda (cálculo barato). Cobertura: no aplica.

<!-- RESULTADOS -->
## Resultados (R=20000 por celda)

|   df |   delta_sobre_EE |   tamano_borde |   tamano_borde_neg |   potencia_theta0 |   potencia_theta_mitad | apto   |
|-----:|-----------------:|---------------:|-------------------:|------------------:|-----------------------:|:-------|
|   12 |              0.5 |         0      |             0      |            0      |                 0      | False  |
|   12 |              1   |         0.0006 |             0.0008 |            0.0008 |                 0.0009 | False  |
|   12 |              1.5 |         0.0126 |             0.013  |            0.0391 |                 0.0296 | False  |
|   12 |              2   |         0.0402 |             0.0404 |            0.2314 |                 0.1522 | True   |
|   12 |              2.5 |         0.0482 |             0.0508 |            0.5282 |                 0.2861 | True   |
|   12 |              3   |         0.0464 |             0.0499 |            0.7614 |                 0.408  | True   |
|   12 |              3.5 |         0.049  |             0.0502 |            0.9031 |                 0.5002 | True   |
|   12 |              4   |         0.0516 |             0.0491 |            0.9656 |                 0.5917 | True   |
|   12 |              5   |         0.0494 |             0.0486 |            0.9976 |                 0.7582 | True   |
|   12 |              6   |         0.0463 |             0.0507 |            1      |                 0.8784 | True   |
|   12 |              8   |         0.0509 |             0.0518 |            1      |                 0.9824 | True   |
|   37 |              0.5 |         0      |             0      |            0      |                 0      | False  |
|   37 |              1   |         0      |             0      |            0      |                 0      | False  |
|   37 |              1.5 |         0.0052 |             0.0046 |            0.0154 |                 0.0116 | False  |
|   37 |              2   |         0.0406 |             0.0382 |            0.2579 |                 0.1594 | True   |
|   37 |              2.5 |         0.052  |             0.0464 |            0.581  |                 0.3166 | True   |
|   37 |              3   |         0.0505 |             0.0486 |            0.8056 |                 0.4247 | True   |
|   37 |              3.5 |         0.049  |             0.0506 |            0.9258 |                 0.5269 | True   |
|   37 |              4   |         0.047  |             0.0513 |            0.9778 |                 0.6206 | True   |
|   37 |              5   |         0.0503 |             0.0488 |            0.9984 |                 0.789  | True   |
|   37 |              6   |         0.0523 |             0.0506 |            1      |                 0.9048 | True   |
|   37 |              8   |         0.0486 |             0.0518 |            1      |                 0.9886 | True   |
|  inf |              0.5 |         0      |             0      |            0      |                 0      | False  |
|  inf |              1   |         0      |             0      |            0      |                 0      | False  |
|  inf |              1.5 |         0      |             0      |            0      |                 0      | False  |
|  inf |              2   |         0.0409 |             0.0405 |            0.2767 |                 0.1725 | True   |
|  inf |              2.5 |         0.0488 |             0.0502 |            0.6052 |                 0.3338 | True   |
|  inf |              3   |         0.0509 |             0.051  |            0.8234 |                 0.444  | True   |
|  inf |              3.5 |         0.0478 |             0.0486 |            0.9359 |                 0.5357 | True   |
|  inf |              4   |         0.0517 |             0.0505 |            0.9804 |                 0.6337 | True   |
|  inf |              5   |         0.0516 |             0.0491 |            0.9991 |                 0.8016 | True   |
|  inf |              6   |         0.051  |             0.0487 |            1      |                 0.91   | True   |
|  inf |              8   |         0.05   |             0.0478 |            1      |                 0.9898 | True   |

Razones Δ/EE del repositorio: mediana 1.04, rango [0.24; 7.30].

**Veredicto: NO APTO como regla general; APTO condicionado a Δ/EE >= umbral (en otro caso «no concluyente»)**. tamaño en el borde < 0,04 (hasta 0,0) para Δ/EE pequeña: 10 de 15 diseños del repositorio con tamaño < 0,04 (df=12); APTO solo si Δ/EE >= 2.0 (df=12), 2.0 (df=37)

