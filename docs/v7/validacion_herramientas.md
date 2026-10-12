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
| MG_jackknife | phi_media | -0.251 | 0.017 | 0.067 | 0.029 | nan |
| MG | phi_media | -0.251 | -0.047 | -0.189 | 0.05 | nan |
| PMG | theta1 | 1.0 | -0.002 | -0.002 | 0.038 | 0.865 |
| PMG | theta2 | -0.5 | 0.005 | 0.01 | 0.033 | 0.875 |
| PMG | phi_media | -0.251 | -0.022 | -0.087 | 0.026 | nan |
| PMG_sandwich | theta1 | 1.0 | -0.002 | -0.002 | 0.038 | 0.79 |
| PMG_sandwich | theta2 | -0.5 | 0.005 | 0.01 | 0.033 | 0.835 |
| PMG_sandwich | phi_media | -0.251 | -0.022 | -0.087 | 0.026 | nan |
| PMG_boot | theta1 | 1.0 | -0.004 | -0.004 | 0.037 | 0.9 |
| PMG_boot | theta2 | -0.5 | 0.003 | 0.005 | 0.031 | 0.92 |
| PMG_boot | phi_media | -0.252 | -0.022 | -0.089 | 0.027 | nan |
| DFE | theta1 | 1.0 | -0.004 | -0.004 | 0.045 | 0.89 |
| DFE | theta2 | -0.5 | 0.011 | 0.022 | 0.042 | 0.915 |
| DFE_jackknife | phi_media | -0.251 | 0.03 | 0.121 | 0.038 | nan |
| DFE | phi_media | -0.251 | 0.01 | 0.039 | 0.02 | nan |
| CS-ARDL | theta1 | 1.0 | -0.049 | -0.049 | 0.13 | 0.85 |
| CS-ARDL | theta2 | -0.5 | 0.109 | 0.218 | 0.159 | 0.715 |
| CS-ARDL | phi_media | -0.251 | -0.104 | -0.417 | 0.108 | nan |
| CS-DL | theta1 | 1.0 | -0.06 | -0.06 | 0.116 | 0.84 |
| CS-DL | theta2 | -0.5 | 0.112 | 0.224 | 0.149 | 0.765 |
| CS-DL | phi_media | -0.251 | nan | nan | nan | nan |
| MG_dm | theta1 | 1.0 | -0.015 | -0.015 | 0.072 | 0.87 |
| MG_dm | theta2 | -0.5 | 0.036 | 0.073 | 0.079 | 0.88 |
| MG_dm | phi_media | -0.251 | -0.046 | -0.184 | 0.049 | nan |
| PMG_dm | theta1 | 1.0 | -0.001 | -0.001 | 0.041 | 0.86 |
| PMG_dm | theta2 | -0.5 | 0.008 | 0.015 | 0.039 | 0.865 |
| PMG_dm | phi_media | -0.251 | -0.019 | -0.077 | 0.024 | nan |

| test | tasa de rechazo al 5 % |
|---|---|
| Westerlund_Gt | 1.0 |
| Westerlund_Ga | 1.0 |
| Westerlund_Pt | 1.0 |
| Westerlund_Pa | 1.0 |
| Pedroni_panelADF | 1.0 |
| Pedroni_groupADF | 1.0 |
| Hausman_info | 0.135 |
| Hausman_sandwich | 0.13 |
| Hausman_VMG | 0.06 |
| CIPS_RW_puro | 0.08 |
| CIPS_sobre_y_del_DGP | 0.38 |
| CIPS_sobre_serie_estacionaria | 1.0 |

## Escenario B_coint_con_factor

| herramienta | metrica | verdadero | sesgo | sesgo rel | RMSE | cobertura |
|---|---|---|---|---|---|---|
| MG | theta1 | 1.0 | -0.026 | -0.026 | 0.076 | 0.92 |
| MG | theta2 | -0.5 | 0.011 | 0.021 | 0.081 | 0.895 |
| MG_jackknife | phi_media | -0.252 | 0.033 | 0.132 | 0.042 | nan |
| MG | phi_media | -0.252 | -0.017 | -0.068 | 0.024 | nan |
| PMG | theta1 | 1.0 | -0.007 | -0.007 | 0.029 | 0.86 |
| PMG | theta2 | -0.5 | -0.0 | -0.0 | 0.028 | 0.885 |
| PMG | phi_media | -0.252 | -0.0 | -0.001 | 0.014 | nan |
| PMG_sandwich | theta1 | 1.0 | -0.007 | -0.007 | 0.029 | 0.795 |
| PMG_sandwich | theta2 | -0.5 | -0.0 | -0.0 | 0.028 | 0.8 |
| PMG_sandwich | phi_media | -0.252 | -0.0 | -0.001 | 0.014 | nan |
| PMG_boot | theta1 | 1.0 | -0.01 | -0.01 | 0.031 | 0.87 |
| PMG_boot | theta2 | -0.5 | 0.002 | 0.003 | 0.027 | 0.88 |
| PMG_boot | phi_media | -0.252 | -0.0 | -0.0 | 0.013 | nan |
| DFE | theta1 | 1.0 | -0.012 | -0.012 | 0.046 | 0.85 |
| DFE | theta2 | -0.5 | -0.016 | -0.031 | 0.052 | 0.895 |
| DFE_jackknife | phi_media | -0.252 | 0.067 | 0.265 | 0.075 | nan |
| DFE | phi_media | -0.252 | 0.049 | 0.194 | 0.055 | nan |
| CS-ARDL | theta1 | 1.0 | -0.064 | -0.064 | 0.13 | 0.825 |
| CS-ARDL | theta2 | -0.5 | 0.086 | 0.171 | 0.215 | 0.77 |
| CS-ARDL | phi_media | -0.252 | -0.108 | -0.43 | 0.111 | nan |
| CS-DL | theta1 | 1.0 | -0.079 | -0.079 | 0.125 | 0.835 |
| CS-DL | theta2 | -0.5 | 0.092 | 0.184 | 0.132 | 0.835 |
| CS-DL | phi_media | -0.252 | nan | nan | nan | nan |
| MG_dm | theta1 | 1.0 | 0.002 | 0.002 | 0.147 | 0.94 |
| MG_dm | theta2 | -0.5 | 0.015 | 0.029 | 0.159 | 0.935 |
| MG_dm | phi_media | -0.252 | -0.013 | -0.052 | 0.027 | nan |
| PMG_dm | theta1 | 1.0 | -0.001 | -0.001 | 0.039 | 0.84 |
| PMG_dm | theta2 | -0.5 | -0.008 | -0.016 | 0.041 | 0.83 |
| PMG_dm | phi_media | -0.252 | 0.013 | 0.052 | 0.025 | nan |

| test | tasa de rechazo al 5 % |
|---|---|
| Westerlund_Gt | 1.0 |
| Westerlund_Ga | 1.0 |
| Westerlund_Pt | 1.0 |
| Westerlund_Pa | 0.99 |
| Pedroni_panelADF | 0.98 |
| Pedroni_groupADF | 0.985 |
| Hausman_info | 0.08 |
| Hausman_sandwich | 0.065 |
| Hausman_VMG | 0.03 |
| CIPS_RW_puro | 0.06 |
| CIPS_sobre_y_del_DGP | 0.555 |
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
| Hausman_info | 0.275 |
| Hausman_sandwich | 0.28 |
| Hausman_VMG | 0.235 |
| CIPS_RW_puro | 0.06 |
| CIPS_sobre_y_del_DGP | 0.11 |
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
| Hausman_info | 0.26 |
| Hausman_sandwich | 0.24 |
| Hausman_VMG | 0.245 |
| CIPS_RW_puro | 0.075 |
| CIPS_sobre_y_del_DGP | 0.115 |
| CIPS_sobre_serie_estacionaria | 1.0 |

## Escenario E_coint_theta_heterogeneo

| herramienta | metrica | verdadero | sesgo | sesgo rel | RMSE | cobertura |
|---|---|---|---|---|---|---|
| MG | theta1 | 0.997 | -0.015 | -0.015 | 0.069 | 1.0 |
| MG | theta2 | -0.496 | 0.026 | 0.053 | 0.072 | 1.0 |
| MG_jackknife | phi_media | -0.251 | 0.015 | 0.061 | 0.028 | nan |
| MG | phi_media | -0.251 | -0.046 | -0.182 | 0.049 | nan |
| PMG | theta1 | 0.997 | 0.16 | 0.16 | 0.29 | 0.275 |
| PMG | theta2 | -0.496 | -0.212 | -0.428 | 0.317 | 0.17 |
| PMG | phi_media | -0.251 | 0.085 | 0.339 | 0.09 | nan |
| PMG_sandwich | theta1 | 0.997 | 0.16 | 0.16 | 0.29 | 0.385 |
| PMG_sandwich | theta2 | -0.496 | -0.212 | -0.428 | 0.317 | 0.285 |
| PMG_sandwich | phi_media | -0.251 | 0.085 | 0.339 | 0.09 | nan |
| DFE | theta1 | 0.997 | 0.12 | 0.121 | 0.202 | 0.915 |
| DFE | theta2 | -0.496 | -0.102 | -0.205 | 0.189 | 0.96 |
| DFE_jackknife | phi_media | -0.251 | 0.183 | 0.729 | 0.188 | nan |
| DFE | phi_media | -0.251 | 0.127 | 0.504 | 0.131 | nan |
| CS-ARDL | theta1 | 0.997 | -0.049 | -0.049 | 0.116 | 0.97 |
| CS-ARDL | theta2 | -0.496 | 0.086 | 0.173 | 0.136 | 0.96 |
| CS-ARDL | phi_media | -0.251 | -0.098 | -0.389 | 0.101 | nan |
| CS-DL | theta1 | 0.997 | -0.066 | -0.067 | 0.116 | 0.95 |
| CS-DL | theta2 | -0.496 | 0.092 | 0.186 | 0.136 | 0.945 |
| CS-DL | phi_media | -0.251 | nan | nan | nan | nan |
| MG_dm | theta1 | 0.997 | 0.011 | 0.011 | 0.094 | 1.0 |
| MG_dm | theta2 | -0.496 | 0.005 | 0.011 | 0.102 | 0.985 |
| MG_dm | phi_media | -0.251 | -0.018 | -0.071 | 0.028 | nan |
| PMG_dm | theta1 | 0.997 | 0.163 | 0.164 | 0.265 | 0.3 |
| PMG_dm | theta2 | -0.496 | -0.193 | -0.388 | 0.284 | 0.25 |
| PMG_dm | phi_media | -0.251 | 0.088 | 0.352 | 0.093 | nan |

| test | tasa de rechazo al 5 % |
|---|---|
| Westerlund_Gt | 1.0 |
| Westerlund_Ga | 1.0 |
| Westerlund_Pt | 1.0 |
| Westerlund_Pa | 1.0 |
| Pedroni_panelADF | 1.0 |
| Pedroni_groupADF | 1.0 |
| Hausman_info | 0.63 |
| Hausman_sandwich | 0.685 |
| Hausman_VMG | 0.605 |
| CIPS_RW_puro | 0.055 |
| CIPS_sobre_y_del_DGP | 0.43 |
| CIPS_sobre_serie_estacionaria | 1.0 |

## Juicio de aptitud por herramienta

| herramienta | veredicto |
|---|---|
| MG | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.063, cobertura 0.895-0.920, max|sesgo rel| media phi=0.189; con theta_i heterogeneo (E): sesgo rel theta1=-0.015, cobertura=1.000). Sesgo de muestra finita CONOCIDO de phi (Hurwicz-Nickell, T=78): 0.189; con jackknife por mitades temporales 0.132 |
| PMG | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.010, cobertura 0.860-0.885, max|sesgo rel| media phi=0.087; con theta_i heterogeneo (E): sesgo rel theta1=0.160, cobertura=0.275) |
| PMG_sandwich | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.010, cobertura 0.790-0.835, max|sesgo rel| media phi=0.087; con theta_i heterogeneo (E): sesgo rel theta1=0.160, cobertura=0.385) |
| PMG_boot | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.010, cobertura 0.870-0.920, max|sesgo rel| media phi=0.089) |
| DFE | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.031, cobertura 0.850-0.915, max|sesgo rel| media phi=0.194; con theta_i heterogeneo (E): sesgo rel theta1=0.121, cobertura=0.915). Sesgo de muestra finita CONOCIDO de phi (Hurwicz-Nickell, T=78): 0.194; con jackknife por mitades temporales 0.265 |
| CS-ARDL | no apta: sesgo relativo de theta fuera de +-10 % (max|sesgo rel| theta=0.218, cobertura 0.715-0.850, max|sesgo rel| media phi=0.430; con theta_i heterogeneo (E): sesgo rel theta1=-0.049, cobertura=0.970) |
| CS-DL | no apta: sesgo relativo de theta fuera de +-10 % (max|sesgo rel| theta=0.224, cobertura 0.765-0.840, max|sesgo rel| media phi=nan; con theta_i heterogeneo (E): sesgo rel theta1=-0.067, cobertura=0.950) |
| MG_dm | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.073, cobertura 0.870-0.940, max|sesgo rel| media phi=0.184; con theta_i heterogeneo (E): sesgo rel theta1=0.011, cobertura=1.000) |
| PMG_dm | apta con reservas: punto apto pero IC95 infra/sobre-cubre (max|sesgo rel| theta=0.016, cobertura 0.830-0.865, max|sesgo rel| media phi=0.077; con theta_i heterogeneo (E): sesgo rel theta1=0.164, cobertura=0.300) |
| CIPS_RW_puro | apta (tamano 0.055-0.080; potencia 1.000-1.000) |
| Hausman_VMG | apta (tamano 0.030-0.060; potencia 0.605-0.605) |
| Hausman_info | solo diagnostico (tamano fuera de [0,02; 0,10]; tamano 0.080-0.135; potencia 0.630-0.630) |
| Hausman_sandwich | solo diagnostico (tamano fuera de [0,02; 0,10]; tamano 0.065-0.130; potencia 0.685-0.685) |
| Pedroni_groupADF | apta (tamano 0.035-0.080; potencia 0.985-1.000) |
| Pedroni_panelADF | apta (tamano 0.030-0.080; potencia 0.980-1.000) |
| Westerlund_Ga | apta con reservas: conservador (tamano 0.000-0.005; potencia 1.000-1.000) |
| Westerlund_Gt | apta con reservas: conservador (tamano 0.005-0.005; potencia 1.000-1.000) |
| Westerlund_Pa | apta con reservas: conservador (tamano 0.005-0.010; potencia 0.990-1.000) |
| Westerlund_Pt | apta con reservas: conservador (tamano 0.010-0.010; potencia 1.000-1.000) |

## Lectura y limites (revision tras correcciones)
- Rechazo en C/D = tamano; en A/B/E = potencia. CIPS: tamano sobre un paseo aleatorio puro (N=17, T=78; con y sin factor) = 0,055-0,080 (apta). Sobre la y del DGP (I(1) mas un componente estacionario grande) rechaza 0,11-0,56: no es un problema de CIPS sino de ese DGP, y se informa como `CIPS_sobre_y_del_DGP` solo a titulo informativo. Potencia: serie AR(0,7). No se probaron truncacion K1/K2 ni tendencia.
- PMG: EE por informacion cubre 0,86-0,885; el sandwich Huber-White cubre peor (0,79-0,84); el bootstrap por unidades (B=49, solo 100 replicas en A y B) cubre 0,87-0,92: el mas cercano a [0,90; 0,98] pero sin cumplirlo en B. Para inferencia con datos reales: `pmg_bootstrap` con B>=199 y tratar el IC como aproximado (reserva). Con theta_i heterogeneo (E) el PMG sesga 16-43 % y cubre 0,17-0,39: usar MG si el Hausman rechaza.
- CS-ARDL y CS-DL: la revision de la implementacion (p_T=floor(T^(1/3))=4, theta_i=-b_x/phi, media MG) no halla error; ambas sesgan theta2 un 17-22 % (coste de grados de libertad con T=78 y ~20 regresores) y cubren 0,72-0,84: NO APTAS. No usar. La dependencia transversal se trata con demeaning transversal (`cs_demean`): MG_dm tiene sesgo <=7 % y cobertura 0,87-0,94 (apta con reservas); PMG_dm cubre 0,83-0,87. En este DGP el factor es estacionario y MG/PMG sin ajuste ya tienen sesgo <=6 %.
- Hausman: la version V_MG - V_PMG (info o sandwich) sobre-rechaza (0,065-0,135): SOLO DIAGNOSTICO. La version con la varianza no parametrica de MG (`var_diff='mg'`, defecto) tiene tamano 0,03-0,06 pero potencia moderada (0,61 con theta_i sd 0,5): apta, conservadora. No se implemento el bootstrap de la diferencia.
- Sesgo de phi en MG y DFE: sesgo de muestra finita conocido (Hurwicz-Nickell; ~-19 % MG, +4 % a +19 % DFE). El jackknife por mitades temporales (`jackknife_phi`) no lo corrige de forma fiable (MG: +7 % en A, +13 % en B; DFE empeora): NO se aplica; se reporta el sesgo.
- Westerlund y Pedroni: p por bootstrap/simulacion, no por momentos tabulados. Westerlund es una variante (pooled ponderado 1/sigma_i^2, sin leads de dx), conservadora aqui.
- Resultados de simulacion con 200 replicas por escenario; no extrapolar a otros DGP. Ninguna cifra procede de datos reales.
