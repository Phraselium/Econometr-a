# Validacion Monte Carlo de las herramientas de panel (V7-R2)

Capa C4 (metodologica). Datos SOLO simulados; sin datos reales. SEED=20261010; 200 replicas por escenario; N=17, T=78; Westerlund con 99 remuestras por bloques; CIPS y Pedroni con valores nulos simulados (500 replicas, paseos aleatorios independientes; medias/varianzas tabuladas de Pedroni NO VERIFICADAS y no usadas). Script: src/v7/r2_montecarlo.py; datos: output/v7/R2/montecarlo.csv.

## DGP
ECM por unidad con phi_i~U(-0,4;-0,1); theta=(1,0; -0,5) comun; efectos fijos en el nivel (c_i~N(0,4)); corto plazo heterogeneo (delta_ik~U(0;0,6), lambda_i~U(0;0,3)); x_k con deriva 0,05. Factor comun AR(0,5) en dx e y (cargas N(1;0,25)) en los escenarios con factor. Estimacion: ARDL(2,1) en forma ECM.
- A: cointegrado, sin factor. B: cointegrado, con factor (dependencia transversal).
- C: sin cointegracion (phi=0), sin factor. D: sin cointegracion, con factor (tamano de los tests).
- E: cointegrado con theta_i heterogeneo (sd 0,5), sin factor (potencia del Hausman; PMG mal especificado).

## Criterios declarados
- |sesgo relativo| <= 10 %; cobertura IC95 de theta en [0,90; 0,98]; tamano nominal 5 % en [0,02; 0,10].
- Tolerancia: 1 error estandar MC de una tasa en 5 % con 200 replicas = 0.015. Reglas de veredicto en `veredictos()`: estimadores juzgados en A y B (theta1 y theta2); tests en todos los escenarios con H0 verdadera (Hausman: A y B; CIPS: y es I(1) en los cinco escenarios).

## Escenario A_coint_sin_factor

| herramienta | metrica | verdadero | sesgo | sesgo rel | RMSE | cobertura |
|---|---|---|---|---|---|---|
| MG | theta1 | 1.0 | -0.013 | -0.013 | 0.071 | 0.92 |
| MG | theta2 | -0.5 | 0.031 | 0.063 | 0.068 | 0.915 |
| MG | phi_media | -0.251 | -0.047 | -0.189 | 0.05 | nan |
| PMG | theta1 | 1.0 | -0.002 | -0.002 | 0.038 | 0.865 |
| PMG | theta2 | -0.5 | 0.005 | 0.01 | 0.033 | 0.875 |
| PMG | phi_media | -0.251 | -0.022 | -0.087 | 0.026 | nan |
| DFE | theta1 | 1.0 | -0.004 | -0.004 | 0.045 | 0.89 |
| DFE | theta2 | -0.5 | 0.011 | 0.022 | 0.042 | 0.915 |
| DFE | phi_media | -0.251 | 0.01 | 0.039 | 0.02 | nan |
| CS-ARDL | theta1 | 1.0 | -0.049 | -0.049 | 0.13 | 0.85 |
| CS-ARDL | theta2 | -0.5 | 0.109 | 0.218 | 0.159 | 0.715 |
| CS-ARDL | phi_media | -0.251 | -0.104 | -0.417 | 0.108 | nan |

| test | tasa de rechazo al 5 % |
|---|---|
| Westerlund_Gt | 1.0 |
| Westerlund_Ga | 1.0 |
| Westerlund_Pt | 1.0 |
| Westerlund_Pa | 1.0 |
| Pedroni_panelADF | 1.0 |
| Pedroni_groupADF | 1.0 |
| Hausman_MG_PMG | 0.135 |
| CIPS_sobre_y_I(1) | 0.38 |
| CIPS_sobre_serie_estacionaria | 1.0 |

## Escenario B_coint_con_factor

| herramienta | metrica | verdadero | sesgo | sesgo rel | RMSE | cobertura |
|---|---|---|---|---|---|---|
| MG | theta1 | 1.0 | -0.026 | -0.026 | 0.076 | 0.92 |
| MG | theta2 | -0.5 | 0.011 | 0.021 | 0.081 | 0.895 |
| MG | phi_media | -0.252 | -0.017 | -0.068 | 0.024 | nan |
| PMG | theta1 | 1.0 | -0.007 | -0.007 | 0.029 | 0.86 |
| PMG | theta2 | -0.5 | -0.0 | -0.0 | 0.028 | 0.885 |
| PMG | phi_media | -0.252 | -0.0 | -0.001 | 0.014 | nan |
| DFE | theta1 | 1.0 | -0.012 | -0.012 | 0.046 | 0.85 |
| DFE | theta2 | -0.5 | -0.016 | -0.031 | 0.052 | 0.895 |
| DFE | phi_media | -0.252 | 0.049 | 0.194 | 0.055 | nan |
| CS-ARDL | theta1 | 1.0 | -0.064 | -0.064 | 0.13 | 0.825 |
| CS-ARDL | theta2 | -0.5 | 0.086 | 0.171 | 0.215 | 0.77 |
| CS-ARDL | phi_media | -0.252 | -0.108 | -0.43 | 0.111 | nan |

| test | tasa de rechazo al 5 % |
|---|---|
| Westerlund_Gt | 1.0 |
| Westerlund_Ga | 1.0 |
| Westerlund_Pt | 1.0 |
| Westerlund_Pa | 0.99 |
| Pedroni_panelADF | 0.98 |
| Pedroni_groupADF | 0.985 |
| Hausman_MG_PMG | 0.08 |
| CIPS_sobre_y_I(1) | 0.555 |
| CIPS_sobre_serie_estacionaria | 1.0 |

## Escenario C_sin_coint_sin_factor

| test | tasa de rechazo al 5 % |
|---|---|
| Westerlund_Gt | 0.005 |
| Westerlund_Ga | 0.005 |
| Westerlund_Pt | 0.01 |
| Westerlund_Pa | 0.01 |
| Pedroni_panelADF | 0.03 |
| Pedroni_groupADF | 0.035 |
| Hausman_MG_PMG | 0.275 |
| CIPS_sobre_y_I(1) | 0.11 |
| CIPS_sobre_serie_estacionaria | 1.0 |

## Escenario D_sin_coint_con_factor

| test | tasa de rechazo al 5 % |
|---|---|
| Westerlund_Gt | 0.005 |
| Westerlund_Ga | 0.0 |
| Westerlund_Pt | 0.01 |
| Westerlund_Pa | 0.005 |
| Pedroni_panelADF | 0.08 |
| Pedroni_groupADF | 0.08 |
| Hausman_MG_PMG | 0.26 |
| CIPS_sobre_y_I(1) | 0.115 |
| CIPS_sobre_serie_estacionaria | 1.0 |

## Escenario E_coint_theta_heterogeneo

| herramienta | metrica | verdadero | sesgo | sesgo rel | RMSE | cobertura |
|---|---|---|---|---|---|---|
| MG | theta1 | 0.997 | -0.015 | -0.015 | 0.069 | 1.0 |
| MG | theta2 | -0.496 | 0.026 | 0.053 | 0.072 | 1.0 |
| MG | phi_media | -0.251 | -0.046 | -0.182 | 0.049 | nan |
| PMG | theta1 | 0.997 | 0.16 | 0.16 | 0.29 | 0.275 |
| PMG | theta2 | -0.496 | -0.212 | -0.428 | 0.317 | 0.17 |
| PMG | phi_media | -0.251 | 0.085 | 0.339 | 0.09 | nan |
| DFE | theta1 | 0.997 | 0.12 | 0.121 | 0.202 | 0.915 |
| DFE | theta2 | -0.496 | -0.102 | -0.205 | 0.189 | 0.96 |
| DFE | phi_media | -0.251 | 0.127 | 0.504 | 0.131 | nan |
| CS-ARDL | theta1 | 0.997 | -0.049 | -0.049 | 0.116 | 0.97 |
| CS-ARDL | theta2 | -0.496 | 0.086 | 0.173 | 0.136 | 0.96 |
| CS-ARDL | phi_media | -0.251 | -0.098 | -0.389 | 0.101 | nan |

| test | tasa de rechazo al 5 % |
|---|---|
| Westerlund_Gt | 1.0 |
| Westerlund_Ga | 1.0 |
| Westerlund_Pt | 1.0 |
| Westerlund_Pa | 1.0 |
| Pedroni_panelADF | 1.0 |
| Pedroni_groupADF | 1.0 |
| Hausman_MG_PMG | 0.63 |
| CIPS_sobre_y_I(1) | 0.43 |
| CIPS_sobre_serie_estacionaria | 1.0 |

## Juicio de aptitud por herramienta

| herramienta | veredicto |
|---|---|
| MG | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.063, cobertura 0.895-0.920, max|sesgo rel| media phi=0.189; con theta_i heterogeneo (E): sesgo rel theta1=-0.015, cobertura=1.000). Reserva adicional: sesgo de la media de phi > 10 % (0.189) |
| PMG | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.010, cobertura 0.860-0.885, max|sesgo rel| media phi=0.087; con theta_i heterogeneo (E): sesgo rel theta1=0.160, cobertura=0.275) |
| DFE | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.031, cobertura 0.850-0.915, max|sesgo rel| media phi=0.194; con theta_i heterogeneo (E): sesgo rel theta1=0.121, cobertura=0.915). Reserva adicional: sesgo de la media de phi > 10 % (0.194) |
| CS-ARDL | no apta: sesgo relativo de theta fuera de +-10 % (max|sesgo rel| theta=0.218, cobertura 0.715-0.850, max|sesgo rel| media phi=0.430; con theta_i heterogeneo (E): sesgo rel theta1=-0.049, cobertura=0.970) |
| CIPS_sobre_y_I(1) | no apta: tamano fuera de [0,02; 0,10] (tamano 0.110-0.555; potencia 1.000-1.000) |
| Hausman_MG_PMG | no apta: tamano fuera de [0,02; 0,10] (tamano 0.080-0.135; potencia 0.630-0.630) |
| Pedroni_groupADF | apta (tamano 0.035-0.080; potencia 0.985-1.000) |
| Pedroni_panelADF | apta (tamano 0.030-0.080; potencia 0.980-1.000) |
| Westerlund_Ga | apta con reservas: conservador (tamano 0.000-0.005; potencia 1.000-1.000) |
| Westerlund_Gt | apta con reservas: conservador (tamano 0.005-0.005; potencia 1.000-1.000) |
| Westerlund_Pa | apta con reservas: conservador (tamano 0.005-0.010; potencia 0.990-1.000) |
| Westerlund_Pt | apta con reservas: conservador (tamano 0.010-0.010; potencia 1.000-1.000) |

## Lectura y limites
- Rechazo en C/D = tamano; rechazo en A/B/E = potencia. Para CIPS, potencia = rechazo sobre una serie AR(0,7) estacionaria.
- En el DGP la y de A, B y E es I(1) pero con un componente estacionario grande: CIPS (p=1, solo constante) sobre-rechaza ahi; no se probaron retardos mayores ni la version con tendencia.
- Westerlund y Pedroni: p por simulacion/bootstrap, no por momentos tabulados. Westerlund usa una variante (pooled ponderado 1/sigma_i^2, sin leads de dx), no el codigo original; en estos DGP queda conservador.
- PMG: EE de theta por informacion; infracubre incluso con theta comun (T=78, phi_i heterogeneo, ARDL(2,1)). Con theta_i heterogeneo (E) el PMG sesga y el Hausman tiene potencia limitada.
- CS-ARDL con p_T=floor(T^{1/3})=4 anade 3x5=15+ regresores a ~73 observaciones por unidad: coste de grados de libertad.
- Resultados de simulacion con dos parametros y 200 replicas; no extrapolar a otros DGP. Ninguna cifra procede de datos reales.
