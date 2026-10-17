# akm_municipal · H4: shift-share municipal con AKM y AKM0

Herramienta de V15 (preregistro_v15.md H4 y sección 6; adenda 1 puntos 8-10 y 13). Código: `src/v15/montecarlo/akm_municipal.py`; semilla `SeedSequence([20261010, 4, escenario*10+etapa]).spawn(trozos)` (trozos de 25 réplicas).

## Proceso generador (declarado antes de simular)
- **Estructura leída (sin valores de resultado):** municipios con SERPAVI en al menos 12 de los 14 años 2011-2024 y cuotas de nacionalidad del padrón de 2003 (28 nacionalidades individuales, sin agregados), cuotas s_ik = habitantes de la nacionalidad k / población total del municipio. N = el número resultante (≈ 1.452). Provincia = 2 primeros dígitos del código INE. T = 11 diferencias anuales (2012-2022).
- **Ecuación en diferencias anuales (adenda 1, punto 8):** y_it = β x_it + ε_it, con x_it = π z_it + v_it, z_it = c Σ_k s_ik g_kt (instrumento shift-share; c lo deja con desviación típica 1 tras restar la media de provincia × año). Efectos de municipio absorbidos por las diferencias; efectos de provincia × año por el centrado dentro de cada celda.
- **Choques de origen (placebo, independientes del resultado):** g_kt ~ N(0,1) independientes entre orígenes y AR(1) ρ = 0,5 en el tiempo (dependencia temporal arbitraria en la inferencia).
- **Errores con dependencia por cuota (el problema que AKM resuelve):** η_it = √0,4 A_it + √0,2 π_i f_t + √0,4 e_it, donde A_it = c Σ_k s_ik u_kt (choques de origen NO observados, independientes de g_kt, mismas cuotas, AR(1) ρ = 0,5), f_t = factor común AR(1) ρ = 0,7 con cargas π_i ~ N(0,1) (dependencia transversal que provincia × año no absorbe) y e_it AR(1) ρ = 0,3. ε = σ_y η^a (σ_y = 0,05 en puntos logarítmicos); v = σ_x (0,5 η^a + √0,75 η^b) con η^b independiente (endogeneidad de x: correlación 0,5), σ_x = 1.
- **Fuerza de la primera etapa:** π tal que la mediana del F efectivo (Montiel Olea-Pflueger con la varianza AKM de π̂, instrumento único) ≈ 30 en «F alta» y ≈ 4 en «F baja» (V9-D4 tuvo F de 2,8 a 4,6). Se calibra en una pasada previa con 100 réplicas y semilla propia.
- **Escenarios:** M1 (28 orígenes, F alta), M2 (28 orígenes, F baja, informativo), M3 (instrumento principal de la adenda 1 punto 10: sin orígenes residenciales (Alemania, Francia, Italia, Portugal, Reino Unido), 23 orígenes, F alta).
- **Nulo:** β = 0 (tamaño de los contrastes de β = 0). **Alternativa de referencia:** β = 0,01 (≈ 1 % de alquiler por desviación típica de x, orden de Saiz) para cobertura, sesgo, RMSE; potencia además con β = 0,008 (MDE80 del pre-registro).
- **Inferencias:** (a) AKM (Adão-Kolesár-Morales): varianza por origen con series temporales arbitrarias dentro del origen, normal; (b) AKM0: inversión del contraste con residuos bajo el nulo (equivalente en este caso exactamente identificado a Anderson-Rubin con la varianza de shocks); (c) error agrupado por provincia con t(40) solo como referencia del sobre-rechazo (no es candidato).
- **Estimador:** 2SLS exactamente identificado = cociente Σ z̃ỹ / Σ z̃x̃.
- **Criterio:** tamaño en [0,04; 0,06] con R = 3.000 y cobertura del IC95 en [0,92; 0,97] para la inferencia AKM; si no pasa, la alternativa nombrada en la adenda (punto 5) es Anderson-Rubin (AKM0). Un F efectivo ≥ umbral MOP (τ = 10 %, instrumento único) es condición de C3 de H4; aquí se reporta la distribución del F y el tamaño condicional a F ≥ 10 y a F ≥ 23,1 (valor orientativo; NO VERIFICADO).

<!-- RESULTADOS -->
## Resultados (R = 3000 por escenario; semilla 20261010, k = 4)

| escenario | inferencia | N | K | n_ef_choques | F_mediana | R | tamano_5pct | tamano_si_F>=10 | tamano_si_F>=23.1 | cobertura_95 | potencia_beta_ref | potencia_mde | sesgo | rmse | acotado_AKM0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1_28_origenes_F_alta | AKM | 1451 | 28 | 9.5294 | 24.0871 | 3000 | 0.2193 | 0.2632 | 0.2967 | 0.7807 | 0.3347 | 0.3023 | -0.2341 | 12.5590 | nan |
| M1_28_origenes_F_alta | AKM0 (AR) | 1451 | 28 | 9.5294 | 24.0871 | 3000 | 0.0083 | 0.0089 | 0.0085 | 0.9917 | 0.0210 | 0.0167 | -0.2341 | 12.5590 | 0.2917 |
| M1_28_origenes_F_alta | agrupado provincia t(40) | 1451 | 28 | 9.5294 | 24.0871 | 3000 | 0.5213 | 0.5591 | 0.5837 | 0.4787 | 0.5917 | 0.5650 | -0.2341 | 12.5590 | nan |
| M2_28_origenes_F_baja | AKM | 1451 | 28 | 9.5294 | 2.8915 | 3000 | 0.1700 | 0.3400 | 0.3344 | 0.8300 | 0.2377 | 0.2180 | -0.0199 | 6.2151 | nan |
| M2_28_origenes_F_baja | AKM0 (AR) | 1451 | 28 | 9.5294 | 2.8915 | 3000 | 0.0077 | 0.0100 | 0.0127 | 0.9923 | 0.0120 | 0.0113 | -0.0199 | 6.2151 | 0.0517 |
| M2_28_origenes_F_baja | agrupado provincia t(40) | 1451 | 28 | 9.5294 | 2.8915 | 3000 | 0.4267 | 0.6413 | 0.6083 | 0.5733 | 0.4753 | 0.4653 | -0.0199 | 6.2151 | nan |
| M3_instr_sin_residenciales_F_alta | AKM | 1451 | 23 | 6.0758 | 36.4671 | 3000 | 0.3283 | 0.3899 | 0.4175 | 0.6717 | 0.4310 | 0.4047 | -0.0006 | 0.3675 | nan |
| M3_instr_sin_residenciales_F_alta | AKM0 (AR) | 1451 | 23 | 6.0758 | 36.4671 | 3000 | 0.0047 | 0.0046 | 0.0053 | 0.9953 | 0.0080 | 0.0077 | -0.0006 | 0.3675 | 0.1693 |
| M3_instr_sin_residenciales_F_alta | agrupado provincia t(40) | 1451 | 23 | 6.0758 | 36.4671 | 3000 | 0.7050 | 0.7461 | 0.7534 | 0.2950 | 0.7123 | 0.7040 | -0.0006 | 0.3675 | nan |

**Estructura y primera etapa**

- M1_28_origenes_F_alta: {'N': 1451, 'K': 28, 'provincias': 38, 'n_efectivo_choques': 9.529369555447008, 'pi': 0.39016432661489414, 'F_mediana': 24.08713547564616, 'F_p10': 4.265667455109525, 'F_p90': 123.78826708091445, 'prop_F_ge_10': 0.7523333333333333}
- M2_28_origenes_F_baja: {'N': 1451, 'K': 28, 'provincias': 38, 'n_efectivo_choques': 9.529369555447008, 'pi': 0.12851320478748243, 'F_mediana': 2.8914769367900135, 'F_p10': 0.09606211704791613, 'F_p90': 24.045830237773014, 'prop_F_ge_10': 0.23233333333333334}
- M3_instr_sin_residenciales_F_alta: {'N': 1451, 'K': 23, 'provincias': 38, 'n_efectivo_choques': 6.0757939684987585, 'pi': 0.36532812294271516, 'F_mediana': 36.46714298905887, 'F_p10': 4.0694678365284975, 'F_p90': 204.78627845803578, 'prop_F_ge_10': 0.802}

**Veredictos**

- M1_28_origenes_F_alta: **NO APTO → diseño solo descriptivo**
- M2_28_origenes_F_baja: **NO APTO → diseño solo descriptivo**
- M3_instr_sin_residenciales_F_alta: **NO APTO → diseño solo descriptivo**

- M1_28_origenes_F_alta / AKM: NO APTO — tamaño 0.2193 fuera de [0.04; 0.06]; cobertura 0.7807 fuera de [0.92; 0.97]
- M1_28_origenes_F_alta / AKM0 (AR): NO APTO — tamaño 0.0083 fuera de [0.04; 0.06]; cobertura 0.9917 fuera de [0.92; 0.97]
- M1_28_origenes_F_alta / agrupado provincia t(40): NO APTO — tamaño 0.5213 fuera de [0.04; 0.06]; cobertura 0.4787 fuera de [0.92; 0.97]
- M2_28_origenes_F_baja / AKM: NO APTO — tamaño 0.1700 fuera de [0.04; 0.06]; cobertura 0.8300 fuera de [0.92; 0.97]
- M2_28_origenes_F_baja / AKM0 (AR): NO APTO — tamaño 0.0077 fuera de [0.04; 0.06]; cobertura 0.9923 fuera de [0.92; 0.97]
- M2_28_origenes_F_baja / agrupado provincia t(40): NO APTO — tamaño 0.4267 fuera de [0.04; 0.06]; cobertura 0.5733 fuera de [0.92; 0.97]
- M3_instr_sin_residenciales_F_alta / AKM: NO APTO — tamaño 0.3283 fuera de [0.04; 0.06]; cobertura 0.6717 fuera de [0.92; 0.97]
- M3_instr_sin_residenciales_F_alta / AKM0 (AR): NO APTO — tamaño 0.0047 fuera de [0.04; 0.06]; cobertura 0.9953 fuera de [0.92; 0.97]
- M3_instr_sin_residenciales_F_alta / agrupado provincia t(40): NO APTO — tamaño 0.7050 fuera de [0.04; 0.06]; cobertura 0.2950 fuera de [0.92; 0.97]

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto:** M1_28_origenes_F_alta: NO APTO → diseño solo descriptivo; M2_28_origenes_F_baja: NO APTO → diseño solo descriptivo; M3_instr_sin_residenciales_F_alta: NO APTO → diseño solo descriptivo.
- **AKM** (28 orígenes, N_efectivo de choques = 9,5): tamaño 0,219, cobertura 0,781; con el instrumento sin orígenes residenciales (23 orígenes, N_efectivo = 6,1) el tamaño es 0,328. La varianza AKM se apoya en pocos choques dominantes y los subestima; el error agrupado por provincia es peor (0,521: no capta la dependencia por cuotas).
- **AKM0 / Anderson-Rubin** (la alternativa de la adenda, punto 5): tamaño 0,0083, cobertura 0,992: conservador (fuera de [0,04; 0,06]) y con potencia 0,021 frente a β = 0,01 (Saiz). El IC invertido es no acotado en el 71 % de las réplicas.
- **F efectivo:** con la primera etapa calibrada para una mediana de ≈ 24 el F de cada réplica es muy variable (percentil 10 ≈ 4); el tamaño condicional a F ≥ 10 es 0,263: el umbral F ≥ 10 no corrige el sobre-rechazo.
- **Consecuencia:** H4 no puede alcanzar C3 con AKM ni con AKM0 con 28 orígenes (≈ 10 choques efectivos); queda como descriptivo/C4. Los pesos de Rotemberg y los intervalos AR (sin criterio de C3) pueden publicarse como diagnóstico.
