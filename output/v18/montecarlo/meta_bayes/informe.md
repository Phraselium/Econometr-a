# V18 · Monte Carlo · Metaanálisis bayesiano de efectos aleatorios (2 a 10 estudios)

**Veredicto: NO APTO.** Condición en que falla: prior_mu_s (principal): nulo_het|K3: μ 0.986, τ 0.987 (conservador); nulo_het|K4: μ 0.975, τ 0.981 (conservador); nulo_het|K6: μ 0.965, τ 0.975 (τ fuera de banda); efecto_het|K3: μ 0.988, τ 0.987 (conservador); efecto_het|K4: μ 0.969, τ 0.982 (τ fuera de banda) | prior_mu_2s: nulo_het|K3: μ 0.985, τ 0.985 (conservador); nulo_het|K4: μ 0.977, τ 0.980 (conservador); nulo_het|K6: μ 0.967, τ 0.974 (τ fuera de banda); nulo_het|K8: μ 0.971, τ 0.962 (conservador); efecto_het|K3: μ 0.989, τ 0.986 (conservador); efecto_het|K4: μ 0.973, τ 0.982 (conservador) ... | prior_mu_s/2: calibracion_prior|K3: μ 0.850, τ 0.937 (insuficiente); calibracion_prior|K4: μ 0.888, τ 0.941 (insuficiente); calibracion_prior|K6: μ 0.896, τ 0.943 (insuficiente); calibracion_prior|K8: μ 0.906, τ 0.957 (insuficiente); calibracion_prior|K10: μ 0.920, τ 0.947 (insuficiente); nulo_het|K3: μ 0.989, τ 0.990 (conservador) ... | tau_semicauchy (sensibilidad): calibracion_prior|K3: μ 0.969, τ 0.971 (τ fuera de banda); nulo_het|K3: μ 0.987, τ 0.984 (conservador); nulo_het|K4: μ 0.977, τ 0.980 (conservador); nulo_het|K6: μ 0.964, τ 0.975 (τ fuera de banda); efecto_het|K3: μ 0.990, τ 0.986 (conservador); efecto_het|K4: μ 0.969, τ 0.982 (τ fuera de banda) | efecto_fijo (K < 3): calibracion_prior|K2: μ 0.500 (insuficiente); nulo_het|K2: μ 0.549 (insuficiente); efecto_het|K2: μ 0.564 (insuficiente).

## Proceso generador (declarado antes de simular)

Estructura (declarada; ningún dato real): K = 2, 3, 4, 6, 8 y 10 estudios en la misma unidad. Todo en unidades de s_f (el modelo es invariante a la escala; s_f = 1).
Errores típicos: se_k = s_f · exp(U(ln 0,05; ln 0,4)) (de 0,05 a 0,4 veces la escala del factor, el rango de las fichas de V18). Modelo: y_k ~ N(θ_k, se_k²), θ_k ~ N(μ, τ²).
Verdades: «calibración» (μ ~ N(0, s_f²) y τ ~ semi-normal(0, (s_f/2)²): los priors del plan; el intervalo central al 95 % debe cubrir 95 % si la cuadratura es exacta); y verdades fijas:
nulo_hom (μ = 0, τ = 0,05), nulo_het (μ = 0, τ = 0,25), efecto_hom (μ = 0,4, τ = 0,05), efecto_het (μ = 0,4, τ = 0,25) y efecto_grande (μ = 1, τ = 0,25).
Estimador: posterior por cuadratura (μ marginalizado, τ en rejilla de 400 puntos hasta 8 s_f). Prior de μ: N(0, s_f²) (principal), N(0, (2 s_f)²) y N(0, (s_f/2)²) (las tres de la adenda 1.9);
prior de τ: semi-normal(0, (s_f/2)²) (semi-Cauchy(0, s_f/2) como sensibilidad). Con K = 2: efecto fijo (media ponderada por la inversa de la varianza, IC95 normal, sin τ), como dice el plan.
Medidas: cobertura del intervalo de credibilidad equicola al 95 % de μ y de τ; «tamaño» = rechazo de μ = μ_verdadero por el intervalo = 1 − cobertura de μ (con μ = 0 es la probabilidad de que el intervalo excluya el cero);
potencia = probabilidad de que el intervalo excluya 0; concordancia de la decisión entre las tres variantes de prior (signo de la mediana y exclusión de 0), que es la regla de publicación de la adenda 1.9.

## Qué falló en V16 y qué se hace distinto

V16 (bayes_jerarquico): NO APTO con otra especificación (modelo normal-normal sección ⊂ municipio ⊂ provincia con 3 niveles): cobertura de μ 0,972-0,976 con verdades de «no nulo» y «homogéneo» y 0,985 en la sección; el intervalo era
conservador (cubría de más), no insuficiente. Aquí el modelo es el nuevo (un nivel: estudios), con K de 2 a 10 y las tres variantes de prior de la adenda; se mide la cobertura de μ y de τ por separado y se informa de si el fallo es por exceso
(conservador) o por defecto. No se asume que un prior propio centrado en 0 con verdad en 0 cubra el 95 %: la cobertura bajo una verdad fija depende del prior, y por eso se miden también las verdades fijas y no solo la calibración.

## Criterio

Criterio del encargo: APTO si el tamaño al 5 % está en [0,03; 0,08] y la cobertura al 95 % (bajo el nulo y bajo la alternativa) en [0,92; 0,97], con R >= 2.000 (o >= 1.000 si se declara). Bandas de la adenda 1.12: apta (tamaño [0,04; 0,06], cobertura [0,93; 0,97], R >= 2.000); con valor crítico corregido (tamaño [0,02; 0,04) o (0,06; 0,15]); no fiable (tamaño > 0,15 o < 0,02). SEED = 20261010. Resultados simulados: ningún dato real de resultado ni muestra sellada.

## Resultados

| escenario | K | variante | R | cobertura_mu | cobertura_tau | excluye_cero | ancho_mu | veredicto | banda_112 | direccion |
|---|---|---|---|---|---|---|---|---|---|---|
| calibracion_prior | 2 | efecto_fijo (K < 3) | 3000 | 0.5003 |  | 0.8690 | 0.3746 | NO APTO | no fiable | insuficiente |
| calibracion_prior | 3 | prior_mu_s (principal) | 3000 | 0.9527 | 0.9520 | 0.5590 | 1.0987 | APTO | apta |  |
| calibracion_prior | 3 | prior_mu_2s | 3000 | 0.9587 | 0.9533 | 0.5777 | 1.1529 | APTO | apta |  |
| calibracion_prior | 3 | prior_mu_s/2 | 3000 | 0.8500 | 0.9370 | 0.4530 | 1.1019 | NO APTO | no fiable | insuficiente |
| calibracion_prior | 3 | tau_semicauchy (sensibilidad) | 3000 | 0.9687 | 0.9707 | 0.4533 | 1.3051 | NO APTO | con valor crítico corregido | τ fuera de banda |
| calibracion_prior | 4 | prior_mu_s (principal) | 3000 | 0.9603 | 0.9510 | 0.6287 | 0.9317 | APTO | con valor crítico corregido |  |
| calibracion_prior | 4 | prior_mu_2s | 3000 | 0.9627 | 0.9507 | 0.6420 | 0.9776 | APTO | con valor crítico corregido |  |
| calibracion_prior | 4 | prior_mu_s/2 | 3000 | 0.8883 | 0.9407 | 0.5667 | 0.9455 | NO APTO | con valor crítico corregido | insuficiente |
| calibracion_prior | 4 | tau_semicauchy (sensibilidad) | 3000 | 0.9663 | 0.9587 | 0.5560 | 1.0564 | APTO | con valor crítico corregido |  |
| calibracion_prior | 6 | prior_mu_s (principal) | 3000 | 0.9553 | 0.9430 | 0.7187 | 0.7518 | APTO | apta |  |
| calibracion_prior | 6 | prior_mu_2s | 3000 | 0.9610 | 0.9433 | 0.7177 | 0.7891 | APTO | con valor crítico corregido |  |
| calibracion_prior | 6 | prior_mu_s/2 | 3000 | 0.8960 | 0.9427 | 0.6907 | 0.7582 | NO APTO | con valor crítico corregido | insuficiente |
| calibracion_prior | 6 | tau_semicauchy (sensibilidad) | 3000 | 0.9633 | 0.9520 | 0.6913 | 0.8151 | APTO | con valor crítico corregido |  |
| calibracion_prior | 8 | prior_mu_s (principal) | 3000 | 0.9467 | 0.9573 | 0.7500 | 0.6441 | APTO | apta |  |
| calibracion_prior | 8 | prior_mu_2s | 3000 | 0.9527 | 0.9567 | 0.7497 | 0.6773 | APTO | apta |  |
| calibracion_prior | 8 | prior_mu_s/2 | 3000 | 0.9060 | 0.9573 | 0.7333 | 0.6359 | NO APTO | con valor crítico corregido | insuficiente |
| calibracion_prior | 8 | tau_semicauchy (sensibilidad) | 3000 | 0.9513 | 0.9643 | 0.7297 | 0.6840 | APTO | apta |  |
| calibracion_prior | 10 | prior_mu_s (principal) | 3000 | 0.9510 | 0.9450 | 0.7773 | 0.5919 | APTO | apta |  |
| calibracion_prior | 10 | prior_mu_2s | 3000 | 0.9603 | 0.9447 | 0.7743 | 0.6227 | APTO | con valor crítico corregido |  |
| calibracion_prior | 10 | prior_mu_s/2 | 3000 | 0.9197 | 0.9473 | 0.7637 | 0.5755 | NO APTO | con valor crítico corregido | insuficiente |
| calibracion_prior | 10 | tau_semicauchy (sensibilidad) | 3000 | 0.9570 | 0.9483 | 0.7610 | 0.6212 | APTO | apta |  |
| nulo_hom | 2 | efecto_fijo (K < 3) | 3000 | 0.9170 |  | 0.0830 | 0.3807 | NO APTO | con valor crítico corregido | insuficiente |
| nulo_hom | 3 | prior_mu_s (principal) | 3000 | 1.0000 | 0.9777 | 0.0000 | 0.7447 | NO APTO | no fiable | conservador |
| nulo_hom | 3 | prior_mu_2s | 3000 | 1.0000 | 0.9770 | 0.0000 | 0.7947 | NO APTO | no fiable | conservador |
| nulo_hom | 3 | prior_mu_s/2 | 3000 | 1.0000 | 0.9787 | 0.0000 | 0.6542 | NO APTO | no fiable | conservador |
| nulo_hom | 3 | tau_semicauchy (sensibilidad) | 3000 | 1.0000 | 0.9783 | 0.0000 | 0.7648 | NO APTO | no fiable | conservador |
| nulo_hom | 4 | prior_mu_s (principal) | 3000 | 0.9997 | 0.9770 | 0.0003 | 0.5522 | NO APTO | no fiable | conservador |
| nulo_hom | 4 | prior_mu_2s | 3000 | 0.9997 | 0.9767 | 0.0003 | 0.5887 | NO APTO | no fiable | conservador |
| nulo_hom | 4 | prior_mu_s/2 | 3000 | 0.9997 | 0.9777 | 0.0003 | 0.5054 | NO APTO | no fiable | conservador |
| nulo_hom | 4 | tau_semicauchy (sensibilidad) | 3000 | 0.9997 | 0.9780 | 0.0003 | 0.5485 | NO APTO | no fiable | conservador |
| nulo_hom | 6 | prior_mu_s (principal) | 3000 | 0.9983 | 0.9770 | 0.0017 | 0.3679 | NO APTO | no fiable | conservador |
| nulo_hom | 6 | prior_mu_2s | 3000 | 0.9980 | 0.9770 | 0.0020 | 0.4053 | NO APTO | no fiable | conservador |
| nulo_hom | 6 | prior_mu_s/2 | 3000 | 0.9973 | 0.9773 | 0.0027 | 0.3448 | NO APTO | no fiable | conservador |
| nulo_hom | 6 | tau_semicauchy (sensibilidad) | 3000 | 0.9980 | 0.9793 | 0.0020 | 0.3619 | NO APTO | no fiable | conservador |
| nulo_hom | 8 | prior_mu_s (principal) | 3000 | 0.9973 | 0.9793 | 0.0027 | 0.2858 | NO APTO | no fiable | conservador |
| nulo_hom | 8 | prior_mu_2s | 3000 | 0.9977 | 0.9793 | 0.0023 | 0.3280 | NO APTO | no fiable | conservador |
| nulo_hom | 8 | prior_mu_s/2 | 3000 | 0.9933 | 0.9797 | 0.0067 | 0.2660 | NO APTO | no fiable | conservador |
| nulo_hom | 8 | tau_semicauchy (sensibilidad) | 3000 | 0.9973 | 0.9810 | 0.0027 | 0.2824 | NO APTO | no fiable | conservador |
| nulo_hom | 10 | prior_mu_s (principal) | 3000 | 0.9950 | 0.9800 | 0.0050 | 0.2409 | NO APTO | no fiable | conservador |
| nulo_hom | 10 | prior_mu_2s | 3000 | 0.9967 | 0.9800 | 0.0033 | 0.2853 | NO APTO | no fiable | conservador |
| nulo_hom | 10 | prior_mu_s/2 | 3000 | 0.9877 | 0.9800 | 0.0123 | 0.2211 | NO APTO | no fiable | conservador |
| nulo_hom | 10 | tau_semicauchy (sensibilidad) | 3000 | 0.9947 | 0.9810 | 0.0053 | 0.2390 | NO APTO | no fiable | conservador |
| nulo_het | 2 | efecto_fijo (K < 3) | 3000 | 0.5490 |  | 0.4510 | 0.3751 | NO APTO | no fiable | insuficiente |
| nulo_het | 3 | prior_mu_s (principal) | 3000 | 0.9857 | 0.9867 | 0.0143 | 0.9311 | NO APTO | no fiable | conservador |
| nulo_het | 3 | prior_mu_2s | 3000 | 0.9853 | 0.9853 | 0.0147 | 0.9970 | NO APTO | no fiable | conservador |
| nulo_het | 3 | prior_mu_s/2 | 3000 | 0.9893 | 0.9900 | 0.0107 | 0.8021 | NO APTO | no fiable | conservador |
| nulo_het | 3 | tau_semicauchy (sensibilidad) | 3000 | 0.9867 | 0.9840 | 0.0133 | 1.0008 | NO APTO | no fiable | conservador |
| nulo_het | 4 | prior_mu_s (principal) | 3000 | 0.9753 | 0.9810 | 0.0247 | 0.7733 | NO APTO | con valor crítico corregido | conservador |
| nulo_het | 4 | prior_mu_2s | 3000 | 0.9767 | 0.9797 | 0.0233 | 0.8186 | NO APTO | con valor crítico corregido | conservador |
| nulo_het | 4 | prior_mu_s/2 | 3000 | 0.9793 | 0.9827 | 0.0207 | 0.6918 | NO APTO | con valor crítico corregido | conservador |
| nulo_het | 4 | tau_semicauchy (sensibilidad) | 3000 | 0.9770 | 0.9800 | 0.0230 | 0.8013 | NO APTO | con valor crítico corregido | conservador |
| nulo_het | 6 | prior_mu_s (principal) | 3000 | 0.9647 | 0.9750 | 0.0353 | 0.5964 | NO APTO | con valor crítico corregido | τ fuera de banda |
| nulo_het | 6 | prior_mu_2s | 3000 | 0.9673 | 0.9740 | 0.0327 | 0.6286 | NO APTO | con valor crítico corregido | τ fuera de banda |
| nulo_het | 6 | prior_mu_s/2 | 3000 | 0.9657 | 0.9763 | 0.0343 | 0.5545 | NO APTO | con valor crítico corregido | τ fuera de banda |
| nulo_het | 6 | tau_semicauchy (sensibilidad) | 3000 | 0.9637 | 0.9753 | 0.0363 | 0.5988 | NO APTO | con valor crítico corregido | τ fuera de banda |
| nulo_het | 8 | prior_mu_s (principal) | 3000 | 0.9687 | 0.9620 | 0.0313 | 0.4934 | APTO | con valor crítico corregido |  |
| nulo_het | 8 | prior_mu_2s | 3000 | 0.9707 | 0.9620 | 0.0293 | 0.5221 | NO APTO | con valor crítico corregido | conservador |
| nulo_het | 8 | prior_mu_s/2 | 3000 | 0.9660 | 0.9623 | 0.0340 | 0.4661 | APTO | con valor crítico corregido |  |
| nulo_het | 8 | tau_semicauchy (sensibilidad) | 3000 | 0.9660 | 0.9623 | 0.0340 | 0.4911 | APTO | con valor crítico corregido |  |
| nulo_het | 10 | prior_mu_s (principal) | 3000 | 0.9620 | 0.9603 | 0.0380 | 0.4344 | APTO | con valor crítico corregido |  |
| nulo_het | 10 | prior_mu_2s | 3000 | 0.9663 | 0.9600 | 0.0337 | 0.4617 | APTO | con valor crítico corregido |  |
| nulo_het | 10 | prior_mu_s/2 | 3000 | 0.9583 | 0.9603 | 0.0417 | 0.4130 | APTO | apta |  |
| nulo_het | 10 | tau_semicauchy (sensibilidad) | 3000 | 0.9610 | 0.9593 | 0.0390 | 0.4315 | APTO | con valor crítico corregido |  |
| efecto_hom | 2 | efecto_fijo (K < 3) | 3000 | 0.9013 |  | 0.9123 | 0.3759 | NO APTO | con valor crítico corregido | insuficiente |
| efecto_hom | 3 | prior_mu_s (principal) | 3000 | 1.0000 | 0.9753 | 0.5517 | 0.7538 | NO APTO | no fiable | conservador |
| efecto_hom | 3 | prior_mu_2s | 3000 | 1.0000 | 0.9743 | 0.5660 | 0.8005 | NO APTO | no fiable | conservador |
| efecto_hom | 3 | prior_mu_s/2 | 3000 | 1.0000 | 0.9763 | 0.4490 | 0.6880 | NO APTO | no fiable | conservador |
| efecto_hom | 3 | tau_semicauchy (sensibilidad) | 3000 | 1.0000 | 0.9770 | 0.4993 | 0.7782 | NO APTO | no fiable | conservador |
| efecto_hom | 4 | prior_mu_s (principal) | 3000 | 0.9990 | 0.9833 | 0.8420 | 0.5566 | NO APTO | no fiable | conservador |
| efecto_hom | 4 | prior_mu_2s | 3000 | 0.9997 | 0.9833 | 0.8453 | 0.5919 | NO APTO | no fiable | conservador |
| efecto_hom | 4 | prior_mu_s/2 | 3000 | 0.9983 | 0.9820 | 0.8017 | 0.5237 | NO APTO | no fiable | conservador |
| efecto_hom | 4 | tau_semicauchy (sensibilidad) | 3000 | 0.9987 | 0.9853 | 0.8350 | 0.5533 | NO APTO | no fiable | conservador |
| efecto_hom | 6 | prior_mu_s (principal) | 3000 | 0.9963 | 0.9793 | 0.9787 | 0.3688 | NO APTO | no fiable | conservador |
| efecto_hom | 6 | prior_mu_2s | 3000 | 0.9987 | 0.9787 | 0.9793 | 0.4046 | NO APTO | no fiable | conservador |
| efecto_hom | 6 | prior_mu_s/2 | 3000 | 0.9930 | 0.9797 | 0.9767 | 0.3498 | NO APTO | no fiable | conservador |
| efecto_hom | 6 | tau_semicauchy (sensibilidad) | 3000 | 0.9960 | 0.9807 | 0.9800 | 0.3629 | NO APTO | no fiable | conservador |
| efecto_hom | 8 | prior_mu_s (principal) | 3000 | 0.9957 | 0.9777 | 0.9987 | 0.2879 | NO APTO | no fiable | conservador |
| efecto_hom | 8 | prior_mu_2s | 3000 | 0.9970 | 0.9780 | 0.9987 | 0.3270 | NO APTO | no fiable | conservador |
| efecto_hom | 8 | prior_mu_s/2 | 3000 | 0.9883 | 0.9780 | 0.9983 | 0.2693 | NO APTO | no fiable | conservador |
| efecto_hom | 8 | tau_semicauchy (sensibilidad) | 3000 | 0.9957 | 0.9787 | 0.9990 | 0.2845 | NO APTO | no fiable | conservador |
| efecto_hom | 10 | prior_mu_s (principal) | 3000 | 0.9940 | 0.9827 | 0.9993 | 0.2414 | NO APTO | no fiable | conservador |
| efecto_hom | 10 | prior_mu_2s | 3000 | 0.9950 | 0.9823 | 0.9993 | 0.2851 | NO APTO | no fiable | conservador |
| efecto_hom | 10 | prior_mu_s/2 | 3000 | 0.9833 | 0.9827 | 0.9993 | 0.2222 | NO APTO | no fiable | conservador |
| efecto_hom | 10 | tau_semicauchy (sensibilidad) | 3000 | 0.9940 | 0.9833 | 0.9993 | 0.2394 | NO APTO | no fiable | conservador |
| efecto_het | 2 | efecto_fijo (K < 3) | 3000 | 0.5637 |  | 0.8230 | 0.3756 | NO APTO | no fiable | insuficiente |
| efecto_het | 3 | prior_mu_s (principal) | 3000 | 0.9883 | 0.9873 | 0.2843 | 0.9334 | NO APTO | no fiable | conservador |
| efecto_het | 3 | prior_mu_2s | 3000 | 0.9893 | 0.9863 | 0.3023 | 0.9947 | NO APTO | no fiable | conservador |
| efecto_het | 3 | prior_mu_s/2 | 3000 | 0.9813 | 0.9887 | 0.2150 | 0.8316 | NO APTO | no fiable | conservador |
| efecto_het | 3 | tau_semicauchy (sensibilidad) | 3000 | 0.9903 | 0.9857 | 0.2383 | 1.0093 | NO APTO | no fiable | conservador |
| efecto_het | 4 | prior_mu_s (principal) | 3000 | 0.9693 | 0.9817 | 0.4827 | 0.7709 | NO APTO | con valor crítico corregido | τ fuera de banda |
| efecto_het | 4 | prior_mu_2s | 3000 | 0.9733 | 0.9817 | 0.4923 | 0.8137 | NO APTO | con valor crítico corregido | conservador |
| efecto_het | 4 | prior_mu_s/2 | 3000 | 0.9687 | 0.9820 | 0.4123 | 0.7085 | NO APTO | con valor crítico corregido | τ fuera de banda |
| efecto_het | 4 | tau_semicauchy (sensibilidad) | 3000 | 0.9690 | 0.9817 | 0.4453 | 0.8001 | NO APTO | con valor crítico corregido | τ fuera de banda |
| efecto_het | 6 | prior_mu_s (principal) | 3000 | 0.9647 | 0.9690 | 0.7370 | 0.5971 | APTO | con valor crítico corregido |  |
| efecto_het | 6 | prior_mu_2s | 3000 | 0.9703 | 0.9683 | 0.7280 | 0.6288 | NO APTO | con valor crítico corregido | conservador |
| efecto_het | 6 | prior_mu_s/2 | 3000 | 0.9543 | 0.9693 | 0.7003 | 0.5632 | APTO | apta |  |
| efecto_het | 6 | tau_semicauchy (sensibilidad) | 3000 | 0.9623 | 0.9670 | 0.7273 | 0.6003 | APTO | con valor crítico corregido |  |
| efecto_het | 8 | prior_mu_s (principal) | 3000 | 0.9650 | 0.9670 | 0.8870 | 0.4934 | APTO | con valor crítico corregido |  |
| efecto_het | 8 | prior_mu_2s | 3000 | 0.9710 | 0.9667 | 0.8720 | 0.5218 | NO APTO | con valor crítico corregido | conservador |
| efecto_het | 8 | prior_mu_s/2 | 3000 | 0.9567 | 0.9670 | 0.8713 | 0.4704 | APTO | apta |  |
| efecto_het | 8 | tau_semicauchy (sensibilidad) | 3000 | 0.9627 | 0.9657 | 0.8877 | 0.4908 | APTO | con valor crítico corregido |  |
| efecto_het | 10 | prior_mu_s (principal) | 3000 | 0.9647 | 0.9603 | 0.9563 | 0.4323 | APTO | con valor crítico corregido |  |
| efecto_het | 10 | prior_mu_2s | 3000 | 0.9683 | 0.9603 | 0.9443 | 0.4593 | APTO | con valor crítico corregido |  |
| efecto_het | 10 | prior_mu_s/2 | 3000 | 0.9560 | 0.9600 | 0.9467 | 0.4133 | APTO | apta |  |
| efecto_het | 10 | tau_semicauchy (sensibilidad) | 3000 | 0.9633 | 0.9593 | 0.9573 | 0.4293 | APTO | con valor crítico corregido |  |
| efecto_grande | 2 | efecto_fijo (K < 3) | 3000 | 0.5580 |  | 0.9980 | 0.3722 | NO APTO | no fiable | insuficiente |
| efecto_grande | 3 | prior_mu_s (principal) | 3000 | 0.9800 | 0.9843 | 0.9717 | 0.9629 | NO APTO | con valor crítico corregido | conservador |
| efecto_grande | 3 | prior_mu_2s | 3000 | 0.9860 | 0.9843 | 0.9790 | 0.9994 | NO APTO | no fiable | conservador |
| efecto_grande | 3 | prior_mu_s/2 | 3000 | 0.9057 | 0.9737 | 0.8807 | 1.0233 | NO APTO | con valor crítico corregido | insuficiente |
| efecto_grande | 3 | tau_semicauchy (sensibilidad) | 3000 | 0.9820 | 0.9823 | 0.8857 | 1.0746 | NO APTO | no fiable | conservador |
| efecto_grande | 4 | prior_mu_s (principal) | 3000 | 0.9727 | 0.9807 | 0.9980 | 0.7857 | NO APTO | con valor crítico corregido | conservador |
| efecto_grande | 4 | prior_mu_2s | 3000 | 0.9783 | 0.9810 | 0.9983 | 0.8159 | NO APTO | con valor crítico corregido | conservador |
| efecto_grande | 4 | prior_mu_s/2 | 3000 | 0.9180 | 0.9733 | 0.9853 | 0.8338 | NO APTO | con valor crítico corregido | insuficiente |
| efecto_grande | 4 | tau_semicauchy (sensibilidad) | 3000 | 0.9733 | 0.9793 | 0.9850 | 0.8264 | NO APTO | con valor crítico corregido | conservador |
| efecto_grande | 6 | prior_mu_s (principal) | 3000 | 0.9647 | 0.9727 | 1.0000 | 0.5955 | NO APTO | con valor crítico corregido | τ fuera de banda |
| efecto_grande | 6 | prior_mu_2s | 3000 | 0.9747 | 0.9737 | 1.0000 | 0.6222 | NO APTO | con valor crítico corregido | conservador |
| efecto_grande | 6 | prior_mu_s/2 | 3000 | 0.9333 | 0.9693 | 1.0000 | 0.6128 | APTO | con valor crítico corregido |  |
| efecto_grande | 6 | tau_semicauchy (sensibilidad) | 3000 | 0.9620 | 0.9720 | 1.0000 | 0.5994 | NO APTO | con valor crítico corregido | τ fuera de banda |
| efecto_grande | 8 | prior_mu_s (principal) | 3000 | 0.9600 | 0.9617 | 1.0000 | 0.5000 | APTO | apta |  |
| efecto_grande | 8 | prior_mu_2s | 3000 | 0.9740 | 0.9617 | 1.0000 | 0.5265 | NO APTO | con valor crítico corregido | conservador |
| efecto_grande | 8 | prior_mu_s/2 | 3000 | 0.9457 | 0.9607 | 1.0000 | 0.5016 | APTO | apta |  |
| efecto_grande | 8 | tau_semicauchy (sensibilidad) | 3000 | 0.9583 | 0.9633 | 1.0000 | 0.4981 | APTO | apta |  |
| efecto_grande | 10 | prior_mu_s (principal) | 3000 | 0.9560 | 0.9647 | 1.0000 | 0.4341 | APTO | apta |  |
| efecto_grande | 10 | prior_mu_2s | 3000 | 0.9657 | 0.9650 | 1.0000 | 0.4603 | APTO | con valor crítico corregido |  |
| efecto_grande | 10 | prior_mu_s/2 | 3000 | 0.9440 | 0.9640 | 1.0000 | 0.4281 | APTO | apta |  |
| efecto_grande | 10 | tau_semicauchy (sensibilidad) | 3000 | 0.9533 | 0.9650 | 1.0000 | 0.4312 | APTO | apta |  |

## Notas

- Escenarios que entran en el veredicto: calibración, nulo_het y efecto_het (los que representan el uso del plan: factores con efecto cercano a 0 o moderado y heterogeneidad); los demás son diagnóstico.
- Con K = 2 se usa el efecto fijo; su cobertura frente a μ cae con heterogeneidad (el efecto fijo estima la media ponderada de los θ_k).
- τ = 0,05 y 0,25 son verdades fijas: la cobertura de τ de un intervalo equicola cerca del borde 0 es baja por construcción.
