<!-- Generado por `make publicacion` desde docs/v7/validacion_herramientas.md. No editar a mano: se regenera y un test lo comprueba. -->

# Validacion Monte Carlo de las herramientas de panel (V7-R2, ronda 3)

Capa C4 (metodologica). Solo datos simulados, SEED=20261010, N=17, T=78. Replicas: 500 en A, C, D, F; 200 en B, E, G, J, K, L; PMG bootstrap: B=199, 200 replicas en A, B, E, F; Westerlund-tipo: 99 remuestras. `±` = EE-MC de la cobertura/tasa. Codigo: src/v7/r2_mc3.py (+ r2_montecarlo.py, ronda 2: output/v7/R2/montecarlo.csv). Datos: output/v7/R2/montecarlo_r3.csv.

## Escenarios

- A: coint., sin factor
- B: coint., factor I(0)
- C: sin coint., sin factor
- D: sin coint., factor I(0)
- E: theta_i heterogeneo
- F: factor I(1) en el residuo, cargas heterogeneas correlacionadas con las de x
- G: factor I(1), cargas homogeneas
- J: phi_i~U(-0,1;-0,02) (ajuste lento)
- K: retroalimentacion: dx con -0,1*ec
- L: rotura en c_i hacia T/3

Criterios declarados (sin cambios respecto a la ronda 1): |sesgo rel| <= 10 %; cobertura IC95 en [0,90; 0,98]; tamano en [0,02; 0,10]. Etiqueta: `apta` (ambos), `reservas` (sesgo ok, cobertura fuera), `no apta` (sesgo > 10 % en theta1 o theta2). b = max |sesgo rel|.

## Tabla final de aptitud de estimadores de theta, por escenario

| estimador | A | B | F | G | E | J | K | L |
|---|---|---|---|---|---|---|---|---|
| CS-ARDL_pT1 | no apta (b=0.15; cob 0.81-0.87±0.02) | no apta (b=0.14; cob 0.83-0.90±0.03) | no apta (b=0.12; cob 0.87-0.90±0.01) | no apta (b=0.11; cob 0.82-0.94±0.03) | no apta (b=0.12; cob 0.97-0.98±0.01) | no apta (b=0.27; cob 0.70-0.90±0.03) | no apta (b=0.48; cob 0.17-0.38±0.03) | no apta (b=0.16; cob 0.80-0.95±0.03) |
| CS-ARDL_pT1_jk | reservas (b=0.03; cob 0.61-0.63±0.02) | no apta (b=0.12; cob 0.57-0.59±0.04) | reservas (b=0.01; cob 0.63-0.65±0.02) | no apta (b=0.12; cob 0.64-0.65±0.03) | no apta (b=0.27; cob 0.80-0.81±0.03) | no apta (b=11.94; cob 0.51-0.56±0.04) | no apta (b=0.37; cob 0.52-0.53±0.04) | no apta (b=5.30; cob 0.59-0.66±0.03) |
| CS-ARDL_pT2 | no apta (b=0.16; cob 0.82-0.85±0.02) | no apta (b=0.18; cob 0.77-0.83±0.03) | no apta (b=0.15; cob 0.82-0.91±0.02) | reservas (b=0.09; cob 0.78-0.95±0.03) | reservas (b=0.06; cob 0.97-0.98±0.01) | no apta (b=0.20; cob 0.70-0.90±0.03) | no apta (b=0.50; cob 0.20-0.36±0.03) | no apta (b=0.18; cob 0.80-0.95±0.03) |
| CS-ARDL_pT2_jk | reservas (b=0.09; cob 0.56-0.57±0.02) | no apta (b=4.97; cob 0.53-0.56±0.04) | no apta (b=0.19; cob 0.58-0.62±0.02) | no apta (b=0.81; cob 0.59-0.64±0.03) | no apta (b=0.26; cob 0.75-0.79±0.03) | no apta (b=0.24; cob 0.47-0.51±0.04) | no apta (b=0.30; cob 0.49-0.53±0.04) | reservas (b=0.07; cob 0.57-0.62±0.03) |
| CS-ARDL_pT4 | no apta (b=0.14; cob 0.79-0.84±0.02) | no apta (b=0.20; cob 0.78-0.80±0.03) | no apta (b=0.17; cob 0.81-0.91±0.02) | no apta (b=0.15; cob 0.82-0.94±0.03) | no apta (b=0.16; cob 0.94-0.97±0.02) | no apta (b=0.52; cob 0.70-0.90±0.03) | no apta (b=0.55; cob 0.21-0.44±0.04) | no apta (b=0.20; cob 0.78-0.95±0.03) |
| CS-ARDL_pT4_jk | no apta (b=2.21; cob 0.40-0.41±0.02) | no apta (b=0.57; cob 0.39-0.43±0.04) | no apta (b=0.39; cob 0.44-0.47±0.02) | no apta (b=2.29; cob 0.48-0.48±0.04) | no apta (b=0.62; cob 0.56-0.61±0.04) | no apta (b=0.71; cob 0.43-0.46±0.04) | no apta (b=0.42; cob 0.41-0.46±0.04) | no apta (b=0.16; cob 0.39-0.52±0.04) |
| CS-DL_pT1 | no apta (b=0.42; cob 0.19-0.47±0.02) | no apta (b=0.41; cob 0.23-0.50±0.04) | no apta (b=0.22; cob 0.59-0.62±0.02) | no apta (b=0.23; cob 0.53-0.57±0.04) | no apta (b=0.43; cob 0.60-0.81±0.03) | no apta (b=0.50; cob 0.38-0.46±0.04) | no apta (b=0.31; cob 0.23-0.26±0.03) | no apta (b=0.21; cob 0.60-0.69±0.03) |
| CS-DL_pT1_jk | no apta (b=0.21; cob 0.59-0.67±0.02) | no apta (b=0.15; cob 0.69-0.70±0.03) | no apta (b=0.11; cob 0.70-0.71±0.02) | no apta (b=0.11; cob 0.68-0.68±0.03) | no apta (b=0.22; cob 0.83-0.89±0.03) | no apta (b=0.42; cob 0.47-0.51±0.04) | no apta (b=0.14; cob 0.60-0.66±0.03) | no apta (b=0.12; cob 0.70-0.73±0.03) |
| CS-DL_pT2 | no apta (b=0.32; cob 0.46-0.66±0.02) | no apta (b=0.32; cob 0.47-0.67±0.04) | no apta (b=0.17; cob 0.75-0.77±0.02) | no apta (b=0.18; cob 0.67-0.73±0.03) | no apta (b=0.33; cob 0.81-0.91±0.03) | no apta (b=0.47; cob 0.47-0.56±0.04) | no apta (b=0.31; cob 0.33-0.36±0.03) | no apta (b=0.17; cob 0.76-0.81±0.03) |
| CS-DL_pT2_jk | no apta (b=0.15; cob 0.66-0.68±0.02) | no apta (b=0.12; cob 0.66-0.73±0.03) | reservas (b=0.09; cob 0.66-0.68±0.02) | reservas (b=0.09; cob 0.64-0.67±0.03) | no apta (b=0.14; cob 0.83-0.91±0.03) | no apta (b=0.40; cob 0.53-0.56±0.04) | no apta (b=0.12; cob 0.64-0.65±0.03) | reservas (b=0.09; cob 0.72-0.74±0.03) |
| CS-DL_pT4 | no apta (b=0.20; cob 0.82-0.85±0.02) | no apta (b=0.20; cob 0.77-0.88±0.03) | no apta (b=0.11; cob 0.86-0.90±0.02) | no apta (b=0.12; cob 0.88-0.90±0.02) | no apta (b=0.20; cob 0.94-0.98±0.02) | no apta (b=0.44; cob 0.65-0.69±0.03) | no apta (b=0.31; cob 0.50-0.52±0.04) | no apta (b=0.12; cob 0.86-0.92±0.02) |
| CS-DL_pT4_jk | reservas (b=0.07; cob 0.50-0.52±0.02) | no apta (b=0.11; cob 0.40-0.50±0.04) | reservas (b=0.05; cob 0.47-0.49±0.02) | reservas (b=0.03; cob 0.49-0.51±0.04) | reservas (b=0.05; cob 0.74-0.78±0.03) | no apta (b=0.41; cob 0.51-0.53±0.04) | reservas (b=0.05; cob 0.49-0.53±0.04) | no apta (b=0.10; cob 0.48-0.54±0.04) |
| MG | apta (b=0.05; cob 0.91-0.92±0.01) | apta (b=0.05; cob 0.90-0.92±0.02) | no apta (b=0.54; cob 0.34-0.40±0.02) | no apta (b=0.54; cob 0.28-0.39±0.03) | reservas (b=0.02; cob 1.00-1.00±0.00) | no apta (b=0.16; cob 0.92-0.95±0.02) | no apta (b=0.31; cob 0.32-0.58±0.03) | no apta (b=0.13; cob 0.83-0.93±0.03) |
| MG_dm | apta (b=0.05; cob 0.95-0.95±0.01) | apta (b=0.02; cob 0.95-0.97±0.01) | no apta (b=0.20; cob 0.85-0.93±0.02) | apta (b=0.07; cob 0.94-0.95±0.02) | reservas (b=0.01; cob 1.00-1.00±0.00) | no apta (b=1.11; cob 0.94-0.96±0.02) | no apta (b=0.34; cob 0.39-0.63±0.03) | apta (b=0.06; cob 0.93-0.95±0.02) |
| MG_sbc | apta (b=0.01; cob 0.90-0.94±0.02) | - | - | - | - | - | - | - |
| PMG | reservas (b=0.00; cob 0.87-0.88±0.02) | reservas (b=0.00; cob 0.88-0.90±0.02) | no apta (b=0.44; cob 0.11-0.14±0.02) | no apta (b=0.57; cob 0.07-0.09±0.02) | no apta (b=0.41; cob 0.23-0.24±0.03) | no apta (b=0.18; cob 0.56-0.57±0.04) | no apta (b=2336.10; cob 0.44-0.59±0.04) | no apta (b=0.19; cob 0.31-0.44±0.04) |
| PMG_dm | reservas (b=0.00; cob 0.85-0.85±0.02) | reservas (b=0.02; cob 0.78-0.78±0.03) | no apta (b=0.14; cob 0.51-0.57±0.02) | reservas (b=0.03; cob 0.81-0.81±0.03) | no apta (b=0.39; cob 0.24-0.24±0.03) | no apta (b=16.48; cob 0.51-0.55±0.04) | no apta (b=0.14; cob 0.36-0.56±0.04) | reservas (b=0.02; cob 0.82-0.84±0.03) |
| PMG_dm_boot | apta (b=0.00; cob 0.96-0.97±0.01) | apta (b=0.02; cob 0.95-0.97±0.01) | no apta (b=0.16; cob 0.90-0.94±0.02) | - | no apta (b=0.39; cob 0.91-0.92±0.02) | - | - | - |

## Test tipo Westerlund (variante; no el estadistico original): tasa de rechazo 5 %

| herramienta | A | C | D | F | J |
|---|---|---|---|---|---|
| WL_Ga | 1.0±0.0 | 0.002±0.002 | 0.002±0.002 | 0.86±0.016 | 0.06±0.017 |
| WL_Gt | 1.0±0.0 | 0.004±0.003 | 0.002±0.002 | 0.93±0.011 | 0.095±0.021 |
| WL_Pa | 1.0±0.0 | 0.006±0.003 | 0.008±0.004 | 0.912±0.013 | 0.285±0.032 |
| WL_Pt | 1.0±0.0 | 0.006±0.003 | 0.016±0.006 | 0.924±0.012 | 0.18±0.027 |

## CIPS sobre paseo aleatorio puro (objetivo 1: tamano)

| herramienta | A | B | C | D | E |
|---|---|---|---|---|---|
| CIPS_RW|base | 0.042±0.009 | 0.06±0.017 | 0.034±0.008 | 0.064±0.011 | 0.065±0.017 |
| CIPS_RW|sbc | 0.04±0.009 | 0.065±0.017 | 0.038±0.009 | 0.076±0.012 | 0.045±0.015 |
| CIPS_RW|sbc_trunc | 0.04±0.009 | 0.065±0.017 | 0.038±0.009 | 0.076±0.012 | 0.045±0.015 |
| CIPS_RW|trend | 0.076±0.012 | 0.09±0.02 | 0.064±0.011 | 0.084±0.012 | 0.095±0.021 |
| CIPS_RW|trunc | 0.042±0.009 | 0.06±0.017 | 0.034±0.008 | 0.064±0.011 | 0.065±0.017 |

## CIPS sobre la y del DGP, I(1) + I(0) grande (objetivo 2: tamano; en A, B, E, y tambien C, D)

| herramienta | A | B | C | D | E |
|---|---|---|---|---|---|
| CIPS_Y|base | 0.35±0.021 | 0.615±0.034 | 0.092±0.013 | 0.092±0.013 | 0.435±0.035 |
| CIPS_Y|sbc | 0.144±0.016 | 0.6±0.035 | 0.036±0.008 | 0.052±0.01 | 0.215±0.029 |
| CIPS_Y|sbc_trunc | 0.144±0.016 | 0.59±0.035 | 0.036±0.008 | 0.052±0.01 | 0.215±0.029 |
| CIPS_Y|trend | 0.422±0.022 | 0.61±0.034 | 0.07±0.011 | 0.096±0.013 | 0.45±0.035 |
| CIPS_Y|trunc | 0.35±0.021 | 0.615±0.034 | 0.092±0.013 | 0.092±0.013 | 0.435±0.035 |

## Valor critico al 5 % del t de MG para phi-bar bajo H0 (sin cointegracion; escenarios C y D)

| scen | herramienta | n | cuantil_5% |
|---|---|---|---|
| A | MG_t_phi | 500 | -16.287 |
| A | MG_dm_t_phi | 500 | -16.531 |
| B | MG_t_phi | 200 | -15.877 |
| B | MG_dm_t_phi | 200 | -14.957 |
| C | MG_t_phi | 500 | -8.445 |
| C | MG_dm_t_phi | 500 | -8.581 |
| D | MG_t_phi | 500 | -8.826 |
| D | MG_dm_t_phi | 500 | -8.223 |
| E | MG_t_phi | 200 | -15.416 |
| E | MG_dm_t_phi | 200 | -16.432 |
| F | MG_t_phi | 500 | -13.859 |
| F | MG_dm_t_phi | 500 | -14.431 |
| G | MG_t_phi | 200 | -13.773 |
| G | MG_dm_t_phi | 200 | -15.086 |
| J | MG_t_phi | 200 | -10.995 |
| J | MG_dm_t_phi | 200 | -10.855 |
| K | MG_t_phi | 200 | -14.569 |
| K | MG_dm_t_phi | 200 | -14.868 |
| L | MG_t_phi | 200 | -14.656 |
| L | MG_dm_t_phi | 200 | -15.397 |

Valor critico al 5 % para H7-E2 (cuantil 5 % del t de MG para phi-bar bajo H0, el menor de C y D): **-8.83** (no -1,645: la distribucion es de tipo Dickey-Fuller y esta muy desplazada). Aplicable solo a este DGP (N=17, T=78, ARDL(2,1)); el t de MG con demeaning da -8,58 (C) y -8,22 (D).

## Seleccion de retardos por SBC (p, q <= 4; verdadero ARDL(2,1))

| scen | herramienta | n | tasa |
|---|---|---|---|
| A | SBC_elige_(2,1) | 200 | 0.52 |

## Pedroni y Hausman (ronda 2, 200 replicas; sin cambios)

| herramienta | A_coint_sin_factor | B_coint_con_factor | C_sin_coint_sin_factor | D_sin_coint_con_factor | E_coint_theta_heterogeneo |
|---|---|---|---|---|---|
| Hausman_VMG | 0.06 | 0.03 | 0.235 | 0.245 | 0.605 |
| Hausman_info | 0.135 | 0.08 | 0.275 | 0.26 | 0.63 |
| Hausman_sandwich | 0.13 | 0.065 | 0.28 | 0.235 | 0.685 |
| Pedroni_groupADF | 1.0 | 0.985 | 0.035 | 0.08 | 1.0 |
| Pedroni_panelADF | 1.0 | 0.98 | 0.03 | 0.08 | 1.0 |

## Observaciones y limites (ronda 3)

- Tiempo de ejecucion del Monte Carlo completo de la ronda 3: ~1.600 s con 4 procesos (supera los 10 min del encargo original); la ronda 2 (r2_montecarlo.py) tarda ~6 min. Los tests usan versiones reducidas (<60 s).
- Con factor I(1) y cargas heterogeneas (F) ningun estimador cumple ambos criterios: MG y PMG sin ajuste fallan (sesgo >40 %); MG_dm sesga 20 %; CS-DL con p_T=4 es el mas cercano (sesgo <=11 %, cobertura 0,86-0,90); PMG_dm con bootstrap (demeaning re-aplicado) cubre 0,90-0,94 con sesgo 16 %. Con cargas homogeneas (G) MG_dm es apto. El jackknife de mitades sobre theta de CS reduce el sesgo en algunos casos pero hunde la cobertura (EE sin corregir).
- PMG_dm con bootstrap B=199 (ver tabla): cobertura 0,95-0,97 en A y B (apta), 0,90-0,94 en F, 0,91-0,92 en E; sobrecubre algo en A/B (dentro de lo conservador).
- CIPS: tamano correcto sobre paseo aleatorio puro (base y SBC 0,034-0,076; con tendencia 0,064-0,095) pero sobrerrechaza sobre una I(1)+I(0) grande (base 0,35-0,62; SBC 0,14-0,60); la truncacion CIPS* (K1=6,19, K2=2,61, NO VERIFICADOS) no cambia nada. Ambos objetivos se reportan con el mismo criterio de tamano.
- Test tipo Westerlund: tamano 0,002-0,016 (conservador, por debajo de 0,02); potencia con phi_i en [-0,1; -0,02] (J): Gt 0,10, Ga 0,06, Pt 0,18, Pa 0,29: baja. En F rechaza 0,86-0,93: en F y, x y el factor cointegran conjuntamente, de modo que la lectura 'H0 verdadera' no es estricta.
- SBC con p, q <= 4 elige el orden verdadero ARDL(2,1) el 52 % de las veces (A); MG con SBC: ver fila MG_sbc (A).
- PMG con retroalimentacion (K) o rotura (L) o phi lento (J): no apto (inestable). MG_dm es apto con rotura (L) pero no con retroalimentacion (K).
- (H10a) No hay Stata/R ni red en esta sesion para comparar con xtpmg o un resultado publicado: queda anotado como pendiente.
- Referencias NO VERIFICADAS (sin acceso a Crossref).
