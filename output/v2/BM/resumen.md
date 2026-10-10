# Resumen BM (modelos predictivos y no lineales) — EXPLORATORIO

Validación SOLO en bloques temporales con embargo (v2_common.block_splits: h=4, primer test 2012Q1, bloques de 4 orígenes, embargo 4, ventana expansiva). Misma muestra que AR(4) y ECM v1; DM-HLN (h=4, pérdida cuadrática; paneles: media transversal por periodo). Datos solo de entrenamiento (vía v2_common.load); H7 sellada NO ejecutada aquí.

Configuraciones de hiperparámetros evaluadas: 59 (presupuesto declarado 63, de las cuales 4 reservadas al bloque 5, no ejecutado). Cada una cuenta como especificación en output/v2/BM/registro.csv.

## 1. Qué modelo gana (fuera de muestra, entrenamiento)

| Objetivo | N | RMSE AR(4) | RMSE ECM v1 | Mejor candidato por RMSE medio en bloques | RMSE | DM vs AR4 (p) | DM vs ECM v1 (p) | p_BH AR4 / ECM |
|---|---|---|---|---|---|---|---|---|
| A nacional (ln IPV real) | 38 | 0.0699 | 0.1094 | TVPVAR_k0.95 | 0.0726 | -0.31 (0.760) | 0.93 (0.359) | 0.760 / 0.482 |
| B panel provincial (IPC alquiler) | 2254 | 0.0154 | 0.0168 | LGBM_nl4_n400 | 0.0124 | 0.94 (0.353) | 1.48 (0.146) | 0.989 / 0.419 |
| C panel provincial (p_tasado real) | 2209 | 0.0418 | 0.0809 | EN_l10.7_a0.4 | 0.0528 | -1.32 (0.194) | 1.34 (0.187) | 0.194 / 0.420 |

DM > 0 = el modelo es mejor que la base. El «mejor candidato» es el ELEGIDO para H7 por la regla fijada antes (output/v2/BM/regla_H7.md): menor RMSE medio en bloques, empate (<1 %) → el más simple.

Candidatos que mejoran a AR(4) y ECM v1 (RMSE menor y p<0,05 frente a ambos, sin corrección): **0** de 59; con BH sobre las configuraciones de cada objetivo: **0**.

- A nacional (ln IPV real): menor RMSE absoluto TVPVAR_k0.95 = 0.0726 (AR(4) 0.0699; ECM v1 0.1094); p vs AR(4) 0.760, p vs ECM v1 0.359.
- B panel provincial (IPC alquiler): menor RMSE absoluto LGBM_nl4_n400 = 0.0124 (AR(4) 0.0154; ECM v1 0.0168); p vs AR(4) 0.353, p vs ECM v1 0.146.
- C panel provincial (p_tasado real): menor RMSE absoluto EN_l10.7_a0.4 = 0.0528 (AR(4) 0.0418; ECM v1 0.0809); p vs AR(4) 0.194, p vs ECM v1 0.187.

Lectura: ver sección 5. El menor RMSE absoluto puede diferir del elegido por RMSE medio en bloques (promedio de RMSE por bloque, que pondera igual a cada bloque).

## 2. Modelos elegidos para H7 (a evaluar UNA vez en la muestra sellada, por el orquestador)

- A nacional (ln IPV real): **TVPVAR_k0.95** (clase tvpvar, config {"kappa": 0.95}); RMSE medio en bloques 0.0593 sobre 38 observaciones comunes; empatados (<1 %): TVPVAR_k0.95.
- B panel provincial (IPC alquiler): **LGBM_nl4_n400** (clase lgbm, config {"num_leaves": 4, "n_estimators": 400}); RMSE medio en bloques 0.0118 sobre 2254 observaciones comunes; empatados (<1 %): LGBM_nl4_n400.
- C panel provincial (p_tasado real): **EN_l10.7_a0.4** (clase enet, config {"l1_ratio": 0.7, "alpha": 0.4}); RMSE medio en bloques 0.0498 sobre 2209 observaciones comunes; empatados (<1 %): EN_l10.7_a0.4.

Evaluación sellada preparada en src/v2/bm_h7_sellado.py (`evaluar_H7`); ensayo en seco en tests/test_bm_h7_sellado.py (pseudo-sellado solo con entrenamiento). Regla de decisión: un objetivo cumple si RMSE < AR(4) y ECM v1, DM>0 frente a ambos y p_IUT=max(p) con Holm (m=3) < 0,05; H7 se cumple si algún objetivo cumple.

## 3. Familias que importan, por periodo (EXPLORATORIO)

AVISO DE COLINEALIDAD: dentro de familias (tipo hipotecario real y coste de uso ρ≈0,97; importe y nº de hipotecas ρ≈0,95; población total, 20-34 y extranjera ρ 0,7-0,9) y entre familias (en el nacional, tipo real y nº de eventos de política ρ≈-0,87; población y precio cruzado ρ>0,9) las importancias se reparten de forma arbitraria; ver colinealidad_pares_0.7.csv. Las permutaciones se hacen por familia completa (conjuntamente), lo que mitiga pero no elimina el problema. Los periodos P1-P4 de la importancia son periodos de los ORÍGENES de test (2012Q1-2023Q2), no del objetivo.

**B panel provincial (IPC alquiler) — LGBM_nl4_n400 (permutación agrupada; Δ ECM relativo al ECM del modelo)** — el modelo NO mejora significativamente al AR(4): se publica por transparencia, NO como explicación
- P1_ajuste (n=392): demografia +0.010; oferta_suelo +0.006
- P2_recuperacion (n=1176): demografia +0.015; credito_tipos +0.005
- P3_covid (n=392): demografia +0.045; oferta_suelo +0.031
- P4_tipos (n=294): empleo_renta +0.053; precio_cruzado +0.015

**B panel provincial (IPC alquiler) — RF_d8_l40 (permutación agrupada; Δ ECM relativo al ECM del modelo)** — el modelo NO mejora significativamente al AR(4): se publica por transparencia, NO como explicación
- P1_ajuste (n=392): credito_tipos +0.002; empleo_renta +0.001
- P2_recuperacion (n=1176): demografia +0.013; precio_cruzado +0.004
- P3_covid (n=392): oferta_suelo +0.041; demografia +0.019
- P4_tipos (n=294): empleo_renta +0.032; demografia +0.021

**C panel provincial (p_tasado real) — LGBM_nl4_n150 (permutación agrupada; Δ ECM relativo al ECM del modelo)** — el modelo NO mejora significativamente al AR(4): se publica por transparencia, NO como explicación
- P1_ajuste (n=350): credito_tipos +0.004; oferta_suelo +0.001
- P2_recuperacion (n=1173): demografia +0.004; credito_tipos +0.002
- P3_covid (n=392): demografia +0.015; empleo_renta +0.001
- P4_tipos (n=294): demografia +0.003; precio_cruzado +0.001

**C panel provincial (p_tasado real) — RF_d8_l10 (permutación agrupada; Δ ECM relativo al ECM del modelo)** — el modelo NO mejora significativamente al AR(4): se publica por transparencia, NO como explicación
- P1_ajuste (n=350): empleo_renta +0.002; precio_cruzado +0.000
- P2_recuperacion (n=1173): demografia +0.006; politica +0.000
- P3_covid (n=392): precio_cruzado +0.001; demografia +0.000
- P4_tipos (n=294): oferta_suelo +0.003; politica +0.000

**B panel provincial (IPC alquiler) — SHAP (TreeSHAP LightGBM; |contribución| media por familia)**
- P1_ajuste: credito_tipos 0.0117; oferta_suelo 0.0033
- P2_recuperacion: credito_tipos 0.0105; oferta_suelo 0.0026
- P3_covid: credito_tipos 0.0055; demografia 0.0013
- P4_tipos: credito_tipos 0.0087; demografia 0.0010

**C panel provincial (p_tasado real) — SHAP (TreeSHAP LightGBM; |contribución| media por familia)**
- P1_ajuste: credito_tipos 0.0515; empleo_renta 0.0057
- P2_recuperacion: credito_tipos 0.0241; oferta_suelo 0.0072
- P3_covid: credito_tipos 0.0364; oferta_suelo 0.0078
- P4_tipos: credito_tipos 0.0357; oferta_suelo 0.0045

ALE de las 3 variables con mayor |SHAP| en output/v2/BM/ale_top3.csv (efecto medio local; con regresores muy colineales el ALE sigue extrapolando poco pero no separa efectos de variables casi duplicadas).

### Post-double-selection por familia (BCH, EE Driscoll-Kraay/HAC(4); EXPLORATORIO)

Solo se reportan contrastes con ≥20 periodos distintos y diseño de rango completo (P3 y P4 tienen 8 y 6 periodos: no hay potencia para variables que solo varían en el tiempo; se omiten). BH dentro de cada objetivo. Asociación, no causalidad.

- A nacional (ln IPV real): 1 de 6 contrastes (familia × periodo) fiables con p_BH<0,05. Todo: oferta_suelo
- B panel provincial (IPC alquiler): 16 de 21 contrastes (familia × periodo) fiables con p_BH<0,05. Todo: demografia; Todo: empleo_renta; Todo: credito_tipos; Todo: oferta_suelo; Todo: politica; Todo: precio_cruzado; P0_boom: empleo_renta; P1_ajuste: demografia; P1_ajuste: credito_tipos; P1_ajuste: oferta_suelo; P1_ajuste: precio_cruzado; P2_recuperacion: demografia; P2_recuperacion: credito_tipos; P2_recuperacion: oferta_suelo; P2_recuperacion: politica; P2_recuperacion: precio_cruzado
- C panel provincial (p_tasado real): 13 de 21 contrastes (familia × periodo) fiables con p_BH<0,05. Todo: demografia; Todo: empleo_renta; Todo: credito_tipos; Todo: oferta_suelo; Todo: politica; P0_boom: demografia; P0_boom: empleo_renta; P1_ajuste: empleo_renta; P1_ajuste: credito_tipos; P1_ajuste: oferta_suelo; P2_recuperacion: credito_tipos; P2_recuperacion: oferta_suelo; P2_recuperacion: politica

Colinealidad y tamaño de T: las variables nacionales (tipos, eventos, crédito nacional) solo varían en el tiempo (T≈80 en «Todo», 20-24 por periodo), de modo que los p de PDS están probablemente sobreestimados y significación NO implica poder predictivo (ningún modelo con estas familias mejora al AR(4) fuera de muestra).

Proyecciones locales por periodo (familias principales; output/v2/BM/proyecciones_locales_periodos.csv; p solo con ≥20 periodos, es decir P1 y P2 y «Todo»; P0, P3 y P4 se publican sin p). Variables con coeficiente significativo (p<0,05, sin corregir) de signo distinto entre periodos fiables: C:n_eventos (P1_ajuste +, P2_recuperacion -). Indicio de parámetros cambiantes, no prueba (colinealidad temporal fuerte entre regresores nacionales).

## 4. Parámetros cambiantes y no linealidad (nacional, A)

- ECM de umbral (ECT>0 vs ≤0; crédito en expansión vs no): ver tabla; ninguno supera al AR(4).
- Markov-switching (2 regímenes, ECT con coeficiente cambiante; DESCRIPTIVO en muestra, N=69): estado ok; duraciones esperadas [1.8210319837581985, 3.4553399776331535]. No se usa como predictor.
- BVAR Minnesota (VAR(2), 4 variables: Δ ln IPV real, Δ ln ocupados, Δ tipo hipotecario real, Δ ln crédito nuevo): SIMPLIFICACIÓN de Giannone-Lenza-Primiceri (2015): sin hiperprior ni suma de coeficientes; λ fijo por configuración (5) y verosimilitud marginal (fórmula cerrada con observaciones ficticias) informada por split en sel['bvar_logml_medio'] (seleccion_H7.json). Prior de media cero (variables en diferencias).
- TVP-VAR: SIMPLIFICACIÓN de Primiceri (2005) con olvido exponencial (Koop-Korobilis): coeficientes paseo aleatorio con factor κ, varianza de medida EWMA (0,98), sin volatilidad estocástica; los coeficientes se filtran hasta L (fin de entrenamiento del split) y se mantienen fijos en el bloque de test (misma información que el resto de modelos).

## 5. Resultados negativos y lo que NO se puede afirmar

- Ningún modelo con variables mejora de forma significativa (p<0,05 frente a AR(4) y ECM v1) en los bloques de entrenamiento; la selección del mínimo sobre ≥19 configuraciones por objetivo es optimista y solo la evaluación sellada puede confirmar nada.
- Reducciones de RMSE no significativas: en B el LightGBM elegido reduce el RMSE un 20 % frente al AR(4), pero DM-HLN no lo distingue (p=0.35); con 46 orígenes autocorrelados la potencia es baja.
- ARDL (A): cobertura 0.89 de la muestra AR(4)∩ECM v1 (<0,90): excluido de la elección por la regla.
- Objetivo A: N de entrenamiento 8-60 (IPV desde 2007Q1; muestra común AR4∩ECM v1 de 38 orígenes y 12 bloques); no se ejecutan árboles (RF/LightGBM) por falta de datos; la potencia del DM es muy baja. Elastic net con N≈8 al inicio produce RMSE muy superiores al AR(4).
- El ECM v1 es peor que el AR(4) en los tres objetivos (RMSE mayor): mejorar al ECM v1 es un listón bajo.
- Importancias: de modelos que no mejoran al AR(4) fuera de muestra → NO son explicación (regla 4). Incluso si lo hicieran, son asociaciones predictivas, no efectos causales, con colinealidad alta.
- Bloque 5 NO ejecutado: factor dinámico provincial (reserva de 4 configuraciones sin usar) y spillovers espaciales (los paneles no traen coordenadas ni matriz de contigüidad: se omite).
- Bloque 6 NO ejecutado: torch no está instalado (se declara; no se instala). Sin deep learning no hay nada que reportar frente a gradient boosting; el resultado es «no ejecutado», no «negativo».
- Los datos de población en el modelo son «en escalera» (último 1-ene observado); el padrón se publica con retraso: en tiempo real no estaría disponible. Variables de oferta y turismo tienen mucha ausencia (imputación por mediana dentro del split; LightGBM usa NaN nativo); turismo (VUT) solo existe desde 2020Q3.
- Efectos de política (n_eventos, nacionales) solo varían en el tiempo y se confunden con cualquier shock agregado.
- Nada de lo anterior es evidencia de H7 hasta la evaluación sellada (criterio uniforme (b)): nivel EXPLORATORIO.
