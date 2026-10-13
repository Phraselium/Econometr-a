# Validación Monte Carlo — herramientas V8-F3 grupo B (no VAR)

Solo datos simulados; SEED=20261010; un hilo por proceso; determinista. Bloques ejecutados en procesos paralelos (4 núcleos): ms12 1073 s, ms23 1016 s, msbic 176 s, perm2 22 s, resto 793 s. Detalle por fila en `montecarlo.csv`.

## Etiquetas

| Herramienta | Etiqueta | Cifras |
|---|---|---|
| umbral_hansen | **apta** | tamaño 0.043 (iid) y 0.040 (heteroced.); potencia 0.890; cobertura IC umbral 0.937. Solo con regresores exógenos/fijos y errores sin autocorrelación; todos los coeficientes conmutan. |
| bai_perron_boot | **apta con bootstrap wild solo si los errores no están autocorrelacionados; con autocorrelación usar boot='block' (con reservas)** | tamaño UDmax 0.068 (iid), 0.052 (heteroced.), AR(0,5): 0.596 con wild (NO apta) vs 0.044 con bloques; potencia salto 1,0σ 1.000, 0,6σ 0.800. Fechas de los cortes solo orientativas. |
| markov_switching | **con reservas** | H0_1reg_test_1v2: tamaño del bootstrap LR 1 vs 2 (5%) = 0.05 (R=20, B=39.0); H1_2reg_test_1v2: potencia del bootstrap LR 1 vs 2 (5%) = 0.40 (R=20, B=39.0); 2reg_test_2v3: rechazo bootstrap LR 2 vs 3 (5%) = 0.00 (R=6, B=19.0); 3reg_test_2v3: rechazo bootstrap LR 2 vs 3 (5%) = 0.00 (R=6, B=19.0); verdadero_1reg: % BIC elige k verdadero = 0.97 (R=30, B=nan); verdadero_2reg: % BIC elige k verdadero = 0.97 (R=30, B=nan); verdadero_3reg: % BIC elige k verdadero = 0.80 (R=30, B=nan). Réplicas pequeñas por coste (bootstrap parametrico: cada réplica reajusta el modelo): validación INDICATIVA, no concluyente; LR sin distribución estándar. |
| dfm_baing_pca | **apta si N≥~30; no apta con N pequeño** | IC_p2 acierta r=1.000 con N=40 y 0.000 con N=10 (tiende a kmax). |
| dfm_ml | **apta (reservas: solo 1 factor AR(1) validado)** | error absoluto medio del R2 por variable 0.051 (R=15). |
| lp_ols | **apta** | cobertura IC95 NW entre 0.910 y 0.950 en h=0,1,4,8. |
| lp_iv_ar | **apta (AR); el IC normal NO es fiable con instrumento débil** | cobertura AR entre 0.925 y 0.975 (F fuerte y débil); ver nota de cada fila para F mediano y % no acotado. Panel FE: solo test de humo (sin Monte Carlo de cobertura). |
| dominancia | **apta** | error medio phi 0.014, cobertura IC bootstrap 0.903, acierto de las 2 dominantes 0.933. Descriptivo, no causal. |
| permutacion_fechas | **con reservas** | tamaño entre 0.024 y 0.056 (studentizado ≈ nominal; sin studentizar conservador); potencia 0.65 (H1_ruptura_pendiente (n=200, salto 1,0); estadístico sin studentizar), 0.73 (H1_ruptura_pendiente (n=200, salto 1,0); estadístico studentizado), 0.32 (H1_ruptura_pendiente; estadístico sin studentizar), 0.41 (H1_ruptura_pendiente; estadístico studentizado). Con pocos conjuntos de fechas posibles el p mínimo y la potencia están acotados. |
| shap_grupos | **apta para ranking de familias cuando la separación es clara; con reservas si hay familias de importancia similar** | DGP aditivo+interacción (orden verdadero F1>F2>F3>F4): % ranking correcto de familias = 1.00; DGP claro: % réplicas bootstrap con ranking completo igual (media) = 1.00; DGP claro: % pliegues temporales con ranking completo igual (media) = 1.00; DGP duro (F1≈F2): % réplicas bootstrap con ranking completo igual (media) = 0.83; DGP duro (F1≈F2): % pliegues temporales con ranking completo igual (media) = 0.75; ALE de c vs sin(2c) centrado: correlación = 0.95 |
| multiverso | **apta (tests unitarios; sin Monte Carlo)** | Registra todas las especificaciones en Registry; resumen con BH sobre toda la rejilla; tope configurable con muestreo determinista. |

## Resultados por prueba

| Herramienta | Escenario | Métrica | Valor | Objetivo | Cumple | Réplicas | B | n |
|---|---|---|---|---|---|---|---|---|
| markov_switching | H0_1reg_test_1v2 | tamaño del bootstrap LR 1 vs 2 (5%) | 0.050 | [0,02;0,10] (R pequeño: IC amplio) | sí | 20 | 39.0 | 200 |
| markov_switching | H1_2reg_test_1v2 | potencia del bootstrap LR 1 vs 2 (5%) | 0.400 | >=0,80 | NO | 20 | 39.0 | 200 |
| markov_switching | 2reg_test_2v3 | rechazo bootstrap LR 2 vs 3 (5%) | 0.000 | tamaño ≤0,10 (2reg) / potencia ≥0,80 (3reg) |  | 6 | 19.0 | 250 |
| markov_switching | 3reg_test_2v3 | rechazo bootstrap LR 2 vs 3 (5%) | 0.000 | tamaño ≤0,10 (2reg) / potencia ≥0,80 (3reg) |  | 6 | 19.0 | 250 |
| markov_switching | verdadero_1reg | % BIC elige k verdadero | 0.967 | >=0,70 | sí | 30 |  | 250 |
| markov_switching | verdadero_2reg | % BIC elige k verdadero | 0.967 | >=0,70 | sí | 30 |  | 250 |
| markov_switching | verdadero_3reg | % BIC elige k verdadero | 0.800 | >=0,70 | sí | 30 |  | 250 |
| permutacion_fechas | H0_iid (n=200, salto 1,0) / estadístico sin studentizar | tamaño (5%) | 0.024 | ≈0,05 ([0,02;0,10]) | sí | 250 | 2000.0 | 200 |
| permutacion_fechas | H0_iid (n=200, salto 1,0) / estadístico studentizado | tamaño (5%) | 0.056 | ≈0,05 ([0,02;0,10]) | sí | 250 | 2000.0 | 200 |
| permutacion_fechas | H1_ruptura_pendiente (n=200, salto 1,0) / estadístico sin studentizar | potencia (5%) | 0.648 | >=0,80 | NO | 250 | 2000.0 | 200 |
| permutacion_fechas | H1_ruptura_pendiente (n=200, salto 1,0) / estadístico studentizado | potencia (5%) | 0.728 | >=0,80 | NO | 250 | 2000.0 | 200 |
| umbral_hansen | H0_iid | tamaño (rechazo al 5%) | 0.043 | [0,02;0,10] | sí | 300 | 299.0 | 120 |
| umbral_hansen | H0_heterocedastico | tamaño (rechazo al 5%) | 0.040 | [0,02;0,10] | sí | 300 | 299.0 | 120 |
| umbral_hansen | H1_salto_pendiente | potencia (rechazo al 5%) | 0.890 | >=0,80 | sí | 300 | 299.0 | 120 |
| umbral_hansen | H1_salto_pendiente | cobertura IC95 del umbral por inversión de LR | 0.937 | [0,90;0,98] | sí | 300 | 299.0 | 120 |
| umbral_hansen | H1_salto_pendiente | sesgo mediano del umbral | -0.013 | /./<0,15 | sí | 300 | 299.0 | 120 |
| bai_perron_boot | H0_iid_wild | tamaño UDmax (5%) | 0.068 | [0,02;0,10] | sí | 250 | 199.0 | 120 |
| bai_perron_boot | H0_iid_wild | tamaño supF(1) (5%) | 0.056 | [0,02;0,10] | sí | 250 | 199.0 | 120 |
| bai_perron_boot | H0_iid_wild | P(BIC elige >=1 corte / nula) | 0.036 | informativo |  | 250 | 199.0 | 120 |
| bai_perron_boot | H0_heterocedastico_wild | tamaño UDmax (5%) | 0.052 | [0,02;0,10] | sí | 250 | 199.0 | 120 |
| bai_perron_boot | H0_heterocedastico_wild | tamaño supF(1) (5%) | 0.048 | [0,02;0,10] | sí | 250 | 199.0 | 120 |
| bai_perron_boot | H0_heterocedastico_wild | P(BIC elige >=1 corte / nula) | 0.096 | informativo |  | 250 | 199.0 | 120 |
| bai_perron_boot | H0_AR0.5_wild | tamaño UDmax (5%) | 0.596 | [0,02;0,10] | NO | 250 | 199.0 | 120 |
| bai_perron_boot | H0_AR0.5_wild | tamaño supF(1) (5%) | 0.448 | [0,02;0,10] | NO | 250 | 199.0 | 120 |
| bai_perron_boot | H0_AR0.5_wild | P(BIC elige >=1 corte / nula) | 0.492 | informativo |  | 250 | 199.0 | 120 |
| bai_perron_boot | H0_AR0.5_bloque | tamaño UDmax (5%) | 0.044 | [0,02;0,10] | sí | 250 | 199.0 | 120 |
| bai_perron_boot | H0_AR0.5_bloque | tamaño supF(1) (5%) | 0.048 | [0,02;0,10] | sí | 250 | 199.0 | 120 |
| bai_perron_boot | H0_AR0.5_bloque | P(BIC elige >=1 corte / nula) | 0.492 | informativo |  | 250 | 199.0 | 120 |
| bai_perron_boot | H1_salto1.0_wild | potencia UDmax (5%) | 1.000 | >=0,80 | sí | 250 | 199.0 | 120 |
| bai_perron_boot | H1_salto1.0_wild | error absoluto mediano de la fecha (obs.) | 2.000 | informativo |  | 250 | 199.0 | 120 |
| bai_perron_boot | H1_salto0.6_wild | potencia UDmax (5%) | 0.800 | informativo |  | 250 | 199.0 | 120 |
| bai_perron_boot | H1_salto0.6_wild | error absoluto mediano de la fecha (obs.) | 6.500 | informativo |  | 250 | 199.0 | 120 |
| lp_ols_NW | h=0 | cobertura IC95 | 0.950 | [0,90;0,98] | sí | 400 |  | 200 |
| lp_ols_NW | h=1 | cobertura IC95 | 0.910 | [0,90;0,98] | sí | 400 |  | 200 |
| lp_ols_NW | h=4 | cobertura IC95 | 0.925 | [0,90;0,98] | sí | 400 |  | 200 |
| lp_ols_NW | h=8 | cobertura IC95 | 0.938 | [0,90;0,98] | sí | 400 |  | 200 |
| lp_iv_AR | instrumento_fuerte_h=0 | cobertura IC normal 2SLS | 0.927 | [0,90;0,98] (referencia) | sí | 400 |  | 200 |
| lp_iv_AR | instrumento_fuerte_h=0 | cobertura IC Anderson-Rubin | 0.925 | [0,90;0,98] | sí | 400 |  | 200 |
| lp_iv_AR | instrumento_fuerte_h=2 | cobertura IC normal 2SLS | 0.920 | [0,90;0,98] (referencia) | sí | 400 |  | 200 |
| lp_iv_AR | instrumento_fuerte_h=2 | cobertura IC Anderson-Rubin | 0.940 | [0,90;0,98] | sí | 400 |  | 200 |
| lp_iv_AR | instrumento_debil_h=0 | cobertura IC normal 2SLS | 0.920 | [0,90;0,98] (referencia) | sí | 400 |  | 200 |
| lp_iv_AR | instrumento_debil_h=0 | cobertura IC Anderson-Rubin | 0.975 | [0,90;0,98] | sí | 400 |  | 200 |
| lp_iv_AR | instrumento_debil_h=2 | cobertura IC normal 2SLS | 0.998 | [0,90;0,98] (referencia) | NO | 400 |  | 200 |
| lp_iv_AR | instrumento_debil_h=2 | cobertura IC Anderson-Rubin | 0.975 | [0,90;0,98] | sí | 400 |  | 200 |
| dominancia | p=5 colineal | /Johnson - LMG/ máx (en R2) | 0.023 | <0,05 | sí | 1 |  | 300 |
| dominancia | p=5 colineal | error absoluto medio de phi (R2) | 0.014 | <0,03 | sí | 60 | 100.0 | 300 |
| dominancia | p=5 colineal | cobertura IC95 bootstrap de phi | 0.903 | [0,90;0,98] | sí | 60 | 100.0 | 300 |
| dominancia | p=5 colineal | % acierto en las 2 variables dominantes (orden) | 0.933 | >=0,80 | sí | 60 | 100.0 | 300 |
| dominancia | p=5 colineal | error relativo máx del VIF | 0.127 | <0,20 | sí | 60 |  | 300 |
| permutacion_fechas | H0_iid / estadístico sin studentizar | tamaño (5%) | 0.032 | ≈0,05 ([0,02;0,10]) | sí | 250 | 2000.0 | 100 |
| permutacion_fechas | H0_iid / estadístico studentizado | tamaño (5%) | 0.052 | ≈0,05 ([0,02;0,10]) | sí | 250 | 2000.0 | 100 |
| permutacion_fechas | H0_AR0.5 / estadístico sin studentizar | tamaño (5%) | 0.032 | ≈0,05 ([0,02;0,10]) | sí | 250 | 2000.0 | 100 |
| permutacion_fechas | H0_AR0.5 / estadístico studentizado | tamaño (5%) | 0.048 | ≈0,05 ([0,02;0,10]) | sí | 250 | 2000.0 | 100 |
| permutacion_fechas | H1_ruptura_pendiente / estadístico sin studentizar | potencia (5%) | 0.316 | >=0,80 | NO | 250 | 2000.0 | 100 |
| permutacion_fechas | H1_ruptura_pendiente / estadístico studentizado | potencia (5%) | 0.408 | >=0,80 | NO | 250 | 2000.0 | 100 |
| shap_grupos | DGP aditivo+interacción (orden verdadero F1>F2>F3>F4) | % ranking correcto de familias | 1.000 | >=0,90 | sí | 30 |  | 400 |
| shap_grupos | DGP claro | % réplicas bootstrap con ranking completo igual (media) | 1.000 | >=0,80 si claro; informativo si duro | sí | 10 | 20.0 | 400 |
| shap_grupos | DGP claro | % pliegues temporales con ranking completo igual (media) | 1.000 | informativo |  | 10 | 4.0 | 400 |
| shap_grupos | DGP duro (F1≈F2) | % réplicas bootstrap con ranking completo igual (media) | 0.835 | >=0,80 si claro; informativo si duro |  | 10 | 20.0 | 400 |
| shap_grupos | DGP duro (F1≈F2) | % pliegues temporales con ranking completo igual (media) | 0.750 | informativo |  | 10 | 4.0 | 400 |
| shap_grupos | arbol sustituto prof.3 | fidelidad R2 | 0.753 | informativo |  | 1 |  | 400 |
| shap_grupos | ALE de c vs sin(2c) centrado | correlación | 0.950 | >=0,90 | sí | 1 |  | 400 |
| dfm_baing | T=120,N=40,r=2 | % IC_p2 elige r verdadero | 1.000 | >=0,90 | sí | 200 |  | 120 |
| dfm_baing | T=120,N=10,r=2 | % IC_p2 elige r verdadero | 0.000 | >=0,90 | NO | 200 |  | 120 |
| dfm_ml | T=100,N=8,r=1 | error absoluto medio del R2 por variable | 0.051 | <0,10 | sí | 15 |  | 100 |

## Notas y límites

- Con R réplicas el error de Monte Carlo del tamaño nominal 5 % es ±1,96·sqrt(0,05·0,95/R): ±0,027 con R=250, ±0,043 con R=100; con R<=30 las cifras de MS son orientativas.
- Markov switching: el bootstrap parametrico es costoso (cada réplica reajusta k0 y k1); el contraste 2 vs 3 solo se probó con R muy pequeño.
- Bai-Perron: el bootstrap wild no corrige autocorrelación; con errores AR(0,5) sobre-rechaza masivamente. Usar bloques o retardos.
- Coste: bloques en paralelo, el más largo (ms12) ~18 min de reloj; msbic y perm2 se relanzaron tras corregir un error del propio script de validación (BIC del modelo de 1 régimen mal escalado; ampliación de la prueba de permutación a n=200). Las filas 2 vs 3 de MS (B=19, p mínimo 0,05) son NO concluyentes.
- Ninguna herramienta se ha estimado con datos reales. Predicción != causalidad (SHAP, ALE, dominancia son descriptivos).
