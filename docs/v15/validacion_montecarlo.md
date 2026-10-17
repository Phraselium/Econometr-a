# V15 · Validación por Monte Carlo de las herramientas pendientes (fase 5 de V16)

Generado por `python3 src/v16/f5_validacion.py v15`; publicado como metodologia/validacion_montecarlo_v15.md. Cada herramienta se valida con un proceso generador que reproduce la estructura de los datos de entrenamiento (unidades, periodos, clusters, calendario de tratamiento, distancias) con resultados SIMULADOS: ningún dato real de resultado ni ninguna muestra sellada. Criterio: el de la fase 5 de V16 (tamaño al 5 % en [0,04; 0,06] con R ≥ 2.000 y cobertura al 95 % en [0,92; 0,97]); cada sección declara su proceso generador y sus rectificaciones. Una herramienta NO APTA no se usa en la fase 6 (su diseño queda descriptivo).

«Cifras determinantes» son las de la inferencia que decide el veredicto (principal o alternativa nombrada); las columnas de rango juntan todos los escenarios y variantes de referencia (p. ej. Webb en SDID o HC1 en Conley), que no deciden el veredicto. El detalle de cada herramienta está en su sección, debajo de la tabla.

| Herramienta | Cifras determinantes | Fallos del criterio | Tamaño (rango) | Cobertura (rango) | Veredicto | Inferencia utilizable |
|---|---|---|---|---|---|---|
| akm_municipal | tamaño AKM 0,2193; tamaño AKM0 0,0083; cobertura AKM0 0,9917 | tamaño 0.2193 fuera de [0.04; 0.06] / cobertura 0.7807 fuera de [0.92; 0.97] / tamaño 0.0083 fuera de [0.04; 0.06] / cobertura 0.9917 fuera de [0.92; 0.97] / (y 14 más) | 0,0083-0,5213 | 0,7807-0,9917 | veredicto_por_escenario: M1_28_origenes_F_alta: NO APTO → diseño solo descriptivo; M2_28_origenes_F_baja: NO APTO → diseño solo descriptivo; M3_instr_sin_residenciales_F_alta: NO APTO → diseño solo descriptivo | descriptivo |
| control_sintetico | tamaño 0,0064; cobertura 0,9865 | tamaño 0.0064 fuera de [0.04; 0.06] / cobertura 0.9865 fuera de [0.92; 0.97] / tamaño 0.0969 fuera de [0.04; 0.06] / tamaño 0.0375 fuera de [0.04; 0.06] / (y 3 más) | 0,0064-0,0969 | 0,9865 | NO APTO → control sintético solo descriptivo | descriptivo |
| dfm_bvar_mcs | tamaño DM-HLN 0,0545; tamaño Clark-West 0,1895; tamaño MCS 10 % 0,123 | tamaño 0.1895 fuera de [0.04; 0.06] / tamaño 0.0310 fuera de [0.04; 0.06] / tamaño 0.1230 fuera de [0.08; 0.12] | 0,031-0,1895 |  | veredicto_DM: APTO (DM-HLN); veredicto_MCS: NO APTO → MCS solo descriptivo | DM-HLN (Clark-West y MCS al 10 % NO APTOS) |
| honest_did | tamaño M̄=0 0,144; tamaño M̄=0 con Σ verdadera 0,052; potencia M̄=1 0 | tamaño 0.1440 fuera de [0.04; 0.06] / cobertura 0.8745 fuera de [0.92; 0.97] / tamaño 0,0 (conservador extremo) / cobertura 1.0000 fuera de [0.92; 0.97] | 0-0,144 | 0,8745-1 | NO APTO → criterio M̄ solo descriptivo (no sostiene C3) | descriptivo |
| sar_sdm | tamaño Wald ρ (rango de celdas) 0,0453-0,055; cobertura efecto indirecto (rango) 0,94-0,946 |  | 0,0453-0,055 | 0,94-0,946 | APTO | Wald de ρ y efectos indirectos (SAR/SDM/SEM, contigüidad y distancia inversa a 25 km) |
| sdid_placebo_h1h2 | tamaño Webb S1 0,208; S2 0,226; S3 0,093 | no computable (N donantes <= N tratados + 5) / tamaño 0.2710 fuera de [0.04; 0.06] / cobertura 0.7325 fuera de [0.92; 0.97] / tamaño 0.2080 fuera de [0.04; 0.06] / (y 15 más) |  |  | veredicto_por_escenario: S1_H1_74donantes: NO APTO → diseño solo descriptivo; S2_H1_14donantes_10km: NO APTO → diseño solo descriptivo; S3_H2_74donantes: NO APTO → diseño solo descriptivo; S4_IPVA_provincias: NO APTO → diseño solo descriptivo | descriptivo |
| westerlund_csardl | tamaño Gτ 0,1355; cobertura velocidad CS-ARDL 0,003 | tamaño 0.1355 fuera de [0.04; 0.06] / tamaño 0.0930 fuera de [0.04; 0.06] / tamaño 0.1965 fuera de [0.04; 0.06] / tamaño 0.1810 fuera de [0.04; 0.06] / (y 5 más) | 0,0105-0,1355 | 0,003-0,9925 | veredictos: Westerlund Gtau: NO APTO → solo descriptivo; Westerlund Galpha: NO APTO → solo descriptivo; Westerlund Ptau: NO APTO → solo descriptivo; Westerlund Palpha: NO APTO → solo descriptivo; CIPS (serie I(1)): NO APTO → solo descriptivo; CS-ARDL elasticidad de largo plazo: NO APTO → solo descriptivo; CS-ARDL velocidad de ajuste media: NO APTO → solo descriptivo | descriptivo |
| wild_webb_v15 | tamaño W1 0,2155; cobertura W1 0,774 | tamaño 0.2155 fuera de [0.04; 0.06] / cobertura 0.7740 fuera de [0.92; 0.97] / tamaño 0.2135 fuera de [0.04; 0.06] / cobertura 0.7735 fuera de [0.92; 0.97] / (y 12 más) | 0,2155 | 0,774 | veredicto_por_escenario: W1_H1H2_198municipios: NO APTO → inferencia solo descriptiva; W2_H4_38provincias: NO APTO → inferencia solo descriptiva; W3_RIPVA_36provincias_pocos_tratados: NO APTO → inferencia solo descriptiva | descriptivo |

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

# control_sintetico · control sintético por municipio, 10 tratados mayores de H1, inferencia por permutación

Herramienta de V15 (preregistro_v15.md H1 prueba (vi), sección 6). Código: `src/v15/montecarlo/control_sintetico.py` y `_comun_panel_v15.py`; semilla `SeedSequence([20261010, 3, escenario*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Estructura leída:** 10 municipios tratados de la cohorte 2024T1 (los 10 primeros del sorteo de 124 de `sdid_placebo_h1h2`; el tamaño real de población no se lee, se modela abajo) y los 74 donantes nunca tratados de ese mismo sorteo (códigos y centroides reales de Incasòl/geo). Calendario: 7 trimestres previos (2022T2-2023T4, adenda 1) y 9 posteriores (2024T1-2026T1); escenario P20: 20 trimestres previos (2019T1-2023T4, como en el texto de H1).
- **Resultado simulado (log renta):** el mismo del SDID de H1 (mu_i, tendencia propia d_i ~ N(0; 0,002²), dos factores comunes AR(1), campo espacial de 25 km, AR(1) ρ = 0,5), con sd_e = 0,05 × exp(0,5 z_i − 0,125) en los donantes. **Heterogeneidad por tamaño:** los 10 tratados mayores tienen la mitad de ruido idiosincrásico (sd_e × 0,5; ruido ∝ población^(−1/2)); en el escenario «intercambiable» tienen la misma distribución que los donantes (diagnóstico: aísla el efecto de la desigualdad de ruido).
- **Efecto:** nulo = 0; referencia = −0,05 con tau_i = tau(1 + 0,5 z_i) por municipio (la verdad de cobertura es el tau_i del municipio); potencia además con el MDE80 (−0,022).
- **Estimador por municipio:** control sintético con pesos en el símplex sobre los 74 donantes ajustados a la serie previa centrada por unidad (variante con efecto fijo de unidad, Doudchenko-Imbens / Ferman-Pinto, porque los niveles no están en el casco convexo); efecto = (media posterior − media previa) del tratado menos la combinación ponderada de los donantes.
- **Inferencia por permutación (en el espacio):** cada donante hace de tratado con los otros 73 (los 74 placebos se calculan una vez por réplica y se comparten entre los 10 tratados, como en la práctica). (a) p = (1 + #{|tau_j| ≥ |tau|})/75; (b) p con el cociente RMSPE posterior/previo (Abadie et al.). IC95 por inversión del contraste (a): tau ± cuantil 95 % de |tau_j|.
- **Nota de granularidad:** con 75 unidades, p ≤ 0,05 exige rango ≤ 3, es decir, un tamaño exacto máximo de 3/75 = 0,04 incluso con intercambiabilidad perfecta (es el borde inferior del criterio).
- **Medidas:** tamaño (rechazo al 5 % bajo el nulo, promedio de los 10 tratados), cobertura del tau_i del IC95, sesgo/RMSE de tau_i, potencia. R = 2.000 réplicas.
- **Criterio:** tamaño en [0,04; 0,06] y cobertura en [0,92; 0,97]. El pre-registro no nombra una inferencia alternativa para el control sintético; si la permutación no pasa, el control sintético queda descriptivo (la prueba (vi) no puede usarse como criterio de C3).

<!-- RESULTADOS -->
## Resultados (R = 2000 nulo, 2000 cobertura, 500 MDE; 10 tratados por réplica; semilla 20261010, k = 3)

| escenario | T_pre | R_nulo | tamano_perm_tau | tamano_perm_rmspe | cobertura_ic_perm | potencia_ref_tau | potencia_ref_rmspe | potencia_mde_tau | sesgo | rmse | tam_trat_1_mayor | tam_trat_10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P7_heterogeneo | 7 | 2000 | 0.0064 | 0.0969 | 0.9865 | 0.0648 | 0.0969 | 0.0150 | -0.0000 | 0.0385 | 0.0060 | 0.0060 |
| P7_intercambiable | 7 | 2000 | 0.0422 | 0.0375 | 0.9335 | 0.1224 | 0.0404 | 0.0484 | 0.0001 | 0.0573 | 0.0410 | 0.0510 |
| P20_heterogeneo | 20 | 2000 | 0.0081 | 0.1374 | 0.9852 | 0.0976 | 0.1429 | 0.0194 | 0.0001 | 0.0365 | 0.0115 | 0.0070 |

**Veredicto: NO APTO → control sintético solo descriptivo.**

- P7_heterogeneo / perm_tau: NO APTO — tamaño 0.0064 fuera de [0.04; 0.06]; cobertura 0.9865 fuera de [0.92; 0.97]
- P7_heterogeneo / perm_rmspe: NO APTO — tamaño 0.0969 fuera de [0.04; 0.06]
- P7_intercambiable / perm_tau: APTO 
- P7_intercambiable / perm_rmspe: NO APTO — tamaño 0.0375 fuera de [0.04; 0.06]
- P20_heterogeneo / perm_tau: NO APTO — tamaño 0.0081 fuera de [0.04; 0.06]; cobertura 0.9852 fuera de [0.92; 0.97]
- P20_heterogeneo / perm_rmspe: NO APTO — tamaño 0.1374 fuera de [0.04; 0.06]

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto: NO APTO → control sintético solo descriptivo** (escenario P7_heterogeneo, el del pre-registro con la adenda).
- **Tamaño** de la permutación en el espacio por municipio: 0,0064 cuando los 10 tratados mayores son menos ruidosos que los donantes (conservador extremo), 0,0422 cuando son intercambiables (dentro del criterio, y es el máximo exacto posible con 75 unidades: 3/75 = 0,04) y 0,0081 con 20 trimestres previos. Con el cociente RMSPE el tamaño es 0,097 (heterogéneo) y 0,037 (intercambiable). La cobertura del IC por inversión es 0,986 (heterogéneo): demasiado ancho.
- **Potencia** frente a −5 %: 0,065 con la permutación por |τ| y 0,122 en el caso intercambiable; el RMSE de τ por municipio es 0,0385 (7 trimestres previos, 74 donantes) frente a un efecto de referencia de −0,05.
- **Consecuencia:** el control sintético por municipio es descriptivo; la prueba (vi) de H1 no puede usarse como criterio de C3. La desigualdad de ruido entre grandes municipios y donantes es el mecanismo, no una anomalía del código.

# dfm_bvar_mcs · H5: combinación DFM + BVAR + LASSO + ARDL frente al AR(4); DM-HLN, GW, CW y MCS

Herramienta de V15 (preregistro_v15.md H5 y sección 6; adenda 1 puntos 8 y 16). Código: `src/v15/montecarlo/dfm_bvar_mcs.py`; semilla `SeedSequence([20261010, 5, etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Dimensiones (estructura de H5):** 94 trimestres (2003T1-2026T2), ventana expansiva desde el trimestre 22, de modo que hay **73 errores fuera de muestra** a horizonte 1; 20 indicadores «mensuales agregados al trimestre».
- **Factores y dependencia:** 2 factores comunes F_t = 0,7 F_{t−1} + u_t (u ~ N(0, I)). Indicadores x_jt = λ_j'F_t + 0,7 η_jt con cargas λ ~ N(0,1) sorteadas por réplica.
- **Variables del BVAR (6):** objetivo g_t (Δlog valor tasado), compraventas c_t = 0,6 F1_t + 0,8 ε, hipotecas h_t = 0,5 F2_t + 0,8 ε, ocupados o_t AR(1) ρ = 0,5, tipo AR(1) ρ = 0,9 e inflación AR(1) ρ = 0,8.
- **Objetivo:** g_t = 0,1 + Σ_{l=1..4} φ_l g_{t−l} + δ (0,7 F1_{t−1} + 0,7 F2_{t−1}) + ε_t, ε ~ N(0,1), φ = (0,3; 0,25; 0,2; 0,1) (AR(4) con memoria larga: los cuatro rezagos importan, de modo que los modelos más parsimoniosos de la combinación pierden precisión si no hay señal; con φ de memoria corta la combinación ya mejora al AR(4) sin señal, porque el AR(4) con 21 observaciones iniciales está mal estimado, y no existe un δ ≥ 0 de igual precisión); δ controla la señal de los indicadores.
- **Modelos (re-estimados en cada origen con la ventana expansiva):**
  - AR(4) (línea base).
  - DFM: 2 componentes principales de los 20 indicadores estandarizados + g_t, regresión directa a h = 1.
  - BVAR de Minnesota de 6 variables con 2 rezagos, media a priori 0, tightness λ = 0,2, decaimiento 1/l², escala de varianzas por AR(1) univariantes; media posterior de la ecuación de g (la verosimilitud marginal de Giannone-Lenza-Primiceri de la adenda se sustituye por λ fijo: coste; se declara).
  - LASSO: g_t y 20 indicadores, λ por BIC (LassoLarsIC; la validación temporal con embargo de la adenda se sustituye por BIC por coste).
  - ARDL: rezagos de g (1-4) y de c y h (1-4), orden por BIC.
  - Combinación = media simple de los 4 pronósticos.
- **Escenarios de señal:** δ = 0 (AR(4) es el proceso verdadero: nulo de Clark-West); δ* = el valor que iguala en media el ECM de la combinación y del AR(4) con n = 94 (nulo de igual precisión finita de Diebold-Mariano; calibrado con 300 réplicas por punto de una rejilla, semillas comunes; δ* hace cero la media de la diferencia de pérdidas); δ_20 = el que reduce un 20 % la razón entre los ECM medios (potencia; el pre-registro cita MDE del 18-30 %).
- **Pruebas** (combinación frente a AR(4), pérdida cuadrática, h = 1): DM-HLN unilateral (varianza de largo plazo = γ0 porque h = 1; t de Student con P − 1 gl); Giacomini-White condicional con instrumentos (1, d_{t−1}), χ²(2) (su hipótesis nula es condicional: bajo δ* solo es la igualdad incondicional, se reporta como diagnóstico); Clark-West unilateral normal.
- **MCS (Hansen-Lunde-Nason), tamaño:** proceso de pérdidas con 6 modelos (los 5 del pre-registro + AR(4)) con igualdad de precisión por construcción: errores e_mt = s_t √ρ-correlación 0,8 con t de 8 grados de libertad y volatilidad común log-AR(1) (ρ = 0,7, sd 0,3); pérdida cuadrática; P = 73. Estadístico T_max, bootstrap de bloques móviles (longitud 4, 999 réplicas), regla de eliminación e_max; tamaño = prob. de que el MCS excluya algún modelo.
- **R = 2.000** réplicas bajo cada nulo. **Criterio:** tamaño del DM-HLN, de CW (bajo δ = 0) en [0,04; 0,06]; para el MCS al 10 % la banda es [0,08; 0,12] (análoga, declarada aquí) y al 5 % [0,04; 0,06]. No hay IC: no hay cobertura. El pre-registro no nombra alternativa distinta de GW y CW; si DM-HLN no pasa y CW pasa, «alternativa APTA (CW)»; si ninguna pasa, «NO APTO → contraste solo descriptivo».

<!-- RESULTADOS -->
## Resultados (R = 2000 bajo cada nulo; semilla 20261010, k = 5)

Calibración: δ* = 0.338; δ_20 = 0.769. Rejilla (diferencia media de pérdidas y razón de ECM medios con 300 réplicas): {'dbar_media': {0.0: -0.10027667713390669, 0.15: -0.08492132091600865, 0.3: -0.027048007604417848, 0.45: 0.08012845717508785, 0.6: 0.2235962810316844, 0.8: 0.46353984510640667, 1.0: 0.7515143966991809, 1.3: 1.2647284232139502}, 'razon_ECM_medios': {0.0: 1.086261552781152, 0.15: 1.070505219034923, 0.3: 1.0202388797576682, 0.45: 0.9476290142617368, 0.6: 0.8740179100579435, 0.8: 0.786556318341988, 1.0: 0.7159999290816585, 1.3: 0.6394765255901291}}

| escenario | delta | R | ratio_ECM_medio | dif_perdida_media | rechazo_DM_HLN | rechazo_GW_cond | rechazo_CW | rechazo_DM_HLN_10pct |
|---|---|---|---|---|---|---|---|---|
| nulo_AR4_verdadero (delta=0) | 0.0000 | 2000 | 1.0860 | -0.0968 | 0.0035 | 0.0630 | 0.1895 | 0.0085 |
| nulo_igual_ECM (delta*) | 0.3379 | 2000 | 0.9975 | 0.0090 | 0.0545 | 0.0310 | 0.6950 | 0.1060 |
| alt_ECM_-20% (delta_20) | 0.7693 | 1000 | 0.7938 | 0.4496 | 0.5800 | 0.3050 | 0.9950 | 0.7600 |

**MCS (pérdidas con igualdad de precisión, 6 modelos, P = 73):** {'tamano_mcs_10pct': 0.123, 'tamano_mcs_5pct': 0.0575, 'R': 2000, 'tam_medio_conjunto_10': 5.8335}

**Veredicto DM/CW: APTO (DM-HLN).** **Veredicto MCS: NO APTO → MCS solo descriptivo.**

- DM-HLN: APTO 
- CW (δ = 0): NO APTO tamaño 0.1895 fuera de [0.04; 0.06]
- GW: NO APTO tamaño 0.0310 fuera de [0.04; 0.06]
- MCS 10 %: NO APTO tamaño 0.1230 fuera de [0.08; 0.12]
- MCS 5 %: APTO

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto DM/CW:** APTO (DM-HLN). Con el nulo de igual ECM esperado (δ* = 0,338), el DM-HLN unilateral con 73 errores tiene tamaño 0,0545 (dentro de [0,04; 0,06]) y potencia 0,580 frente a una reducción del 20 % del ECM (el MDE del pre-registro es del 18-30 %: la potencia es moderada, no alta). Con el AR(4) como proceso verdadero (δ = 0) la combinación es peor en media y el DM unilateral casi nunca rechaza (tamaño 0,0035), como corresponde.
- **Clark-West no es utilizable** para la combinación frente al AR(4): rechaza el 0,190 de las veces cuando el AR(4) es el proceso verdadero (la combinación de modelos no anidados con parámetros estimados no cumple la teoría de modelos anidados). **GW** condicional: tamaño 0,031 bajo igualdad incondicional; solo diagnóstico (su nulo es condicional).
- **MCS** (6 modelos, P = 73, igualdad de precisión por construcción): tamaño 0,1230 al 10 % (banda declarada [0,08; 0,12]; supera el límite por 0,003, dentro de un error de Monte Carlo de ≈ 0,007: **NO APTO en el límite**) y 0,0575 al 5 % (dentro de [0,04; 0,06]). El veredicto del MCS es NO APTO → MCS solo descriptivo; la decisión depende de la banda declarada para el 10 %, y por eso H5 debe leerse con el MCS al 5 % como comprobación.
- **Alcance:** esta validación cubre el tamaño de las pruebas con los modelos sustituidos por proxies declarados (λ de Minnesota fijo en lugar de GLP; BIC en lugar de validación temporal con embargo) y ventana expansiva; no valida la elección de la línea base de K1.

# honest_did · Honest DiD (Rambachan-Roth, magnitudes relativas) en el estudio de eventos de H1

Herramienta de V15 (preregistro_v15.md sección 6: «implementación propia de V9, con tamaño del 7,3 % en 400 réplicas: se revalida o se sustituye»; adenda 1, punto 13). Código: `src/v15/montecarlo/honest_did.py`, que llama a la implementación de V9 (`honest_rr` y sus piezas, `src/v9/herramientas.py`) sin modificarla. Semilla `SeedSequence([20261010, 2, escenario*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Panel (estructura de H1, escenario S1 de sdid_placebo_h1h2):** 124 tratados y 74 donantes nunca tratados (códigos reales, centroides reales), 7 trimestres previos (2022T2-2023T4) y 9 posteriores (2024T1-2026T1), mismo proceso generador que `sdid_placebo_h1h2` (factores comunes AR(1), campo espacial, AR(1) ρ = 0,5, sd_e = 0,05 heterogénea). La referencia del estudio de eventos es e = −1 (2023T4).
- **Estudio de eventos estimado dentro de cada réplica:** b_e = (media de tratados − media de donantes) en e, menos la misma diferencia en e = −1; e = −7..−2 (6 previos) y 0..8 (9 posteriores). Covarianza estimada con varianzas robustas por unidad (varianza de las medias de cada grupo): el error de estimación de la covarianza entra en el tamaño.
- **Tendencias paralelas exactas (escenarios A-D):** para aislar el contraste de Honest DiD del sesgo de composición, el proceso de estos escenarios no lleva tendencias propias ni cargas heterogéneas de los factores (solo efectos de tiempo comunes, campo espacial de 25 km y AR(1) idiosincrásico heterocedástico). Los escenarios E y F usan el proceso completo de H1 (factores con cargas heterogéneas y tendencias propias d_i ~ N(0; 0,002²)), en el que las tendencias paralelas solo se cumplen en esperanza (información).
- **Sesgo de tendencias paralelas simulado:** a los tratados se les suma δ_e = s·(e + 1) en todos los trimestres (tendencia diferencial lineal; δ_{−1} = 0). Con s = 0,004 por trimestre las diferencias posteriores igualan a las previas, es decir, el caso frontera de Δ^RM(M̄ = 1).
- **Parámetro:** θ = ATT medio de los 9 trimestres posteriores (media muestral de tau_i, con tau_i = tau(1 + 0,5 z_i)).
- **Escenarios:** A (M̄ = 0, tendencias paralelas exactas), B (M̄ = 1, tendencia lineal frontera; es el umbral de C3 de H1), y de información: C (M̄ = 1, sin tendencia: el contraste es conservador por construcción), D (M̄ = 0 con tendencia: la hipótesis es falsa, mide el sobre-rechazo si se ignora el sesgo), E y F (proceso completo de H1 con M̄ = 0 y M̄ = 1).
- **Medidas:** tamaño = rechazo de θ = 0 con tau = 0; cobertura = 1 − rechazo de θ = θ_verdadero con tau = −0,05 (dualidad: θ ∈ IC si alguna pieza no rechaza θ; es el IC de V9 sin recorrer la rejilla); potencia = rechazo de θ = 0 con tau = −0,05 y con el MDE80 del pre-registro (−0,022). Sesgo y RMSE del estimador puntual (media de los 9 b_e posteriores) frente a θ.
- **Diagnóstico de la covarianza:** además del contraste con la covarianza estimada en cada réplica (la que usará H1), se repite con la covarianza verdadera (covarianza empírica de los coeficientes entre réplicas bajo el nulo, «Σ verdadera»). Si el tamaño solo falla con la estimada, el problema es la covarianza clusterizada por municipio (ignora la correlación espacial y los efectos comunes), no el contraste ARP.
- **Consistencia:** en 60 réplicas se comprueba que `honest_rr` (IC por inversión sobre rejilla, V9) contiene θ0 si y solo si el contraste por piezas no lo rechaza.
- **Criterio:** tamaño en [0,04; 0,06] con R = 2.000 (escenarios A y B, que son los casos frontera) y cobertura en [0,92; 0,97]. El pre-registro no nombra una inferencia alternativa para Honest DiD; la adenda (punto 13) exige además una segunda implementación independiente para sostener C3 (doble implementación: fuera de este encargo).

<!-- RESULTADOS -->
## Resultados (R = 2000 en A y B; 500 en C-F; potencia con 500; semilla 20261010, k = 2)

| escenario | Mbar | pendiente | PT_exacta | rol | R_nulo | tamano_5pct | cobertura_95 | potencia_tau_-0.05 | potencia_mde_-0.022 | tamano_Sigma_verdadera | cobertura_Sigma_verdadera | sesgo | rmse |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_PT_exacta_M0 | 0.0000 | 0.0000 | True | verdad | 2000 | 0.1440 | 0.8745 | 0.9980 | 0.6460 | 0.0520 | 0.9515 | -0.0001 | 0.0118 |
| B_frontera_lineal_M1 | 1.0000 | 0.0040 | True | verdad | 2000 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | 0.0202 | 0.0234 |
| C_sin_tendencia_M1 | 1.0000 | 0.0000 | True | info | 500 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | -0.0003 | 0.0123 |
| D_tendencia_con_M0 | 0.0000 | 0.0040 | True | info | 500 | 0.5900 | 0.4480 | 0.8120 | 0.1660 | 0.3920 | 0.5880 | 0.0194 | 0.0227 |
| E_factores_M0 | 0.0000 | 0.0000 | False | info | 500 | 0.2420 | 0.7740 | 0.9260 | 0.6040 | 0.0520 | 0.9520 | 0.0005 | 0.0166 |
| F_factores_M1 | 1.0000 | 0.0000 | False | info | 500 | 0.0000 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | -0.0007 | 0.0175 |

**Consistencia** (60 réplicas, escenario B): coincidencia de `honest_rr` con el contraste por piezas = 1.000.

**Veredicto: NO APTO → criterio M̄ solo descriptivo (no sostiene C3).**

- A_PT_exacta_M0: NO APTO — tamaño 0.1440 fuera de [0.04; 0.06]; cobertura 0.8745 fuera de [0.92; 0.97] (con Σ verdadera: APTO)
- B_frontera_lineal_M1: NO APTO — tamaño 0,0 (conservador extremo); cobertura 1.0000 fuera de [0.92; 0.97] (con Σ verdadera: NO APTO)

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto: NO APTO → criterio M̄ solo descriptivo (no sostiene C3).** La implementación de V9 se revalida con R = 2.000 y con tendencias paralelas exactas en el proceso:
  - **M̄ = 0 (escenario A):** con la covarianza que usará H1 (estimada por municipio) el tamaño es 0,144 y la cobertura 0,875: **no** pasa. Con la covarianza verdadera el mismo contraste da tamaño 0,052 y cobertura 0,952: el contraste ARP condicional de V9 es correcto (el 7,3 % de V9, con 400 réplicas y covarianza conocida, es compatible con este valor dentro del error de Monte Carlo de ±1,3 pp) y el sobre-rechazo viene de la covarianza clusterizada por municipio, que ignora la correlación espacial.
  - **M̄ = 1 (escenario B, tendencia lineal frontera):** tamaño 0,000 (conservador extremo, NO APTO) y **potencia 0,000** incluso frente a un efecto de −5 %: con el ruido declarado (SE de cada coeficiente ≈ 0,012) el IC con M̄ = 1 mide ≈ ±0,2 y nunca excluye el 0. Con la covarianza verdadera ocurre lo mismo.
- **Consecuencia:** el criterio «M̄ de ruptura ≥ 1» de H1 es inalcanzable con este nivel de ruido y no puede sostener C3, aunque haya una segunda implementación (la adenda la exige además y no está disponible aquí: sin red para instalar HonestDiD). Informativo: con tendencias propias y cargas factoriales heterogéneas (E y F) el comportamiento es el mismo (tamaño 0,242 con M̄ = 0; 0,000 con M̄ = 1).

# sar_sdm · E3: SAR, SEM y SDM con W de contigüidad y de distancia inversa (corte 25 km)

Herramienta de V15 (preregistro_v15.md E3 y sección 6; adenda 1 punto 18: periodos 2011-2019 y 2015-2024). Código: `src/v15/montecarlo/sar_sdm.py`; semilla `SeedSequence([20261010, 7, celda*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Estructura leída (códigos y geometría; ningún valor de resultado):** municipios de entrenamiento con SERPAVI en 2015 y en 2024 (corte transversal de Δlog 2015-2024; N ≈ 1.900 tras quitar los que no tienen vecinos), polígonos de `data/base/geo`.
  - **W de contigüidad (reina):** polígonos que comparten frontera o vértice, estandarizada por filas.
  - **W de distancia inversa con corte de 25 km:** w_ij = 1/d_ij si d_ij < 25 km (distancia entre centroides), estandarizada por filas.
  - Se descartan las islas (sin vecino en alguna de las dos matrices) para que ambas matrices usen la misma muestra.
- **Covariables fijas:** x1 y x2 = (I − 0,5 W)^(-1) N(0,1) estandarizadas (autocorrelación espacial moderada, como cualquier covariable municipal), constante; β = (0; 0,5; −0,3). X se fija en todas las réplicas (inferencia condicional en X).
- **Procesos:**
  - SAR: y = ρ W y + X β + ε.
  - SEM: y = X β + u, u = λ W u + ε.
  - SDM: y = ρ W y + X β + W X θ + ε, con θ = (0,3; −0,2).
  - Nulo: ρ = λ = 0 (en el SDM, ρ = 0 y θ = 0, de modo que el efecto indirecto es 0). Alternativa: ρ = λ = 0,4.
- **Errores:** ε_i ~ N(0, σ_i²). Escenario «heterocedástico» (principal): σ_i = exp(0,4 z_i − 0,08) con z_i ~ N(0,1) (heterogeneidad entre municipios); escenario «homocedástico» (diagnóstico): σ_i = 1.
- **Estimación:** máxima verosimilitud concentrada con log-determinante exacto por autovalores de W. Contrastes sobre ρ (λ): Wald con la curvatura numérica de la verosimilitud perfilada y razón de verosimilitudes (referencia). Moran de los residuos MCO con la media y la varianza exactas de Cliff-Ord para residuos de regresión.
- **Efectos (LeSage-Pace) en SAR y SDM para x1:** efecto directo = media de la diagonal de S(W), total = suma/N, indirecto = total − directo; trazas hasta el orden 60 de W; 1.000 simulaciones de (ρ, β[, θ]) de la normal con la covarianza del método delta (β(ρ) = b0 − ρ bL) y IC percentil. La verdad es el valor analítico en los parámetros del proceso. Tamaño del efecto indirecto bajo el nulo = rechazo de que el IC95 contiene 0.
- **R = 3.000 por celda.** Criterio: tamaño de las pruebas sobre ρ en [0,04; 0,06] y cobertura del IC95 de los efectos indirectos y de ρ en [0,92; 0,97] (escenario heterocedástico; el homocedástico es diagnóstico). El pre-registro no nombra alternativa para estas pruebas distinta de los errores de Conley sobre los coeficientes (fuera de este encargo).

<!-- RESULTADOS -->
## Resultados (R = 3000 por celda; N = 1483; semilla 20261010, k = 7)

| W | modelo | errores | R | tamano_wald_rho | tamano_lr_rho | tamano_moran | cobertura_rho | potencia_wald_rho | sesgo_rho | rmse_rho | tamano_indirecto | cobertura_indirecto | cobertura_directo | potencia_indirecto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| contigüidad | SAR | hetero | 3000 | 0.0550 | 0.0543 | 0.0530 | 0.9413 | 1.0000 | -0.0024 | 0.0244 | 0.0547 | 0.9447 | 0.9570 | 1.0000 |
| contigüidad | SAR | homo | 3000 | 0.0497 | 0.0497 | 0.0513 | 0.9493 | 1.0000 | -0.0019 | 0.0232 | 0.0533 | 0.9487 | 0.9500 | 1.0000 |
| contigüidad | SDM | hetero | 3000 | 0.0453 | 0.0453 | 0.0443 | 0.9527 | 1.0000 | -0.0023 | 0.0251 | 0.0517 | 0.9437 | 0.9507 | 1.0000 |
| contigüidad | SDM | homo | 3000 | 0.0537 | 0.0533 | 0.0517 | 0.9513 | 1.0000 | -0.0028 | 0.0253 | 0.0563 | 0.9443 | 0.9373 | 1.0000 |
| contigüidad | SEM | hetero | 3000 | 0.0487 | 0.0483 | 0.0473 | 0.9450 | 1.0000 | -0.0013 | 0.0264 | nan | nan | nan | nan |
| contigüidad | SEM | homo | 3000 | 0.0553 | 0.0553 | 0.0560 | 0.9527 | 1.0000 | -0.0032 | 0.0261 | nan | nan | nan | nan |
| dist_inversa_25km | SAR | hetero | 3000 | 0.0483 | 0.0477 | 0.0507 | 0.9483 | 1.0000 | -0.0043 | 0.0349 | 0.0470 | 0.9400 | 0.9447 | 1.0000 |
| dist_inversa_25km | SAR | homo | 3000 | 0.0503 | 0.0497 | 0.0457 | 0.9453 | 1.0000 | -0.0042 | 0.0341 | 0.0503 | 0.9433 | 0.9380 | 1.0000 |
| dist_inversa_25km | SDM | hetero | 3000 | 0.0550 | 0.0547 | 0.0497 | 0.9333 | 1.0000 | -0.0083 | 0.0394 | 0.0493 | 0.9460 | 0.9510 | 1.0000 |
| dist_inversa_25km | SDM | homo | 3000 | 0.0547 | 0.0557 | 0.0507 | 0.9507 | 1.0000 | -0.0058 | 0.0375 | 0.0543 | 0.9457 | 0.9460 | 1.0000 |
| dist_inversa_25km | SEM | hetero | 3000 | 0.0547 | 0.0540 | 0.0523 | 0.9457 | 1.0000 | -0.0053 | 0.0396 | nan | nan | nan | nan |
| dist_inversa_25km | SEM | homo | 3000 | 0.0547 | 0.0547 | 0.0520 | 0.9500 | 1.0000 | -0.0056 | 0.0385 | nan | nan | nan | nan |

**Veredicto: APTO.**

- SAR|contigüidad: ρ APTO  | indirecto APTO 
- SDM|contigüidad: ρ APTO  | indirecto APTO 
- SEM|contigüidad: ρ APTO  | indirecto n/a 
- SAR|dist_inversa_25km: ρ APTO  | indirecto APTO 
- SDM|dist_inversa_25km: ρ APTO  | indirecto APTO 
- SEM|dist_inversa_25km: ρ APTO  | indirecto n/a

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto: APTO** en las seis combinaciones modelo × W del escenario heterocedástico (R = 3.000 por celda, N = 1483).
- Tamaño del Wald sobre ρ (λ) entre 0,045 y 0,055; razón de verosimilitudes entre 0,045 y 0,055; Moran de los residuos entre 0,044 y 0,053. Cobertura del IC de ρ entre 0,933 y 0,953; del efecto indirecto entre 0,940 y 0,946; del directo entre 0,945 y 0,957; tamaño del efecto indirecto bajo el nulo entre 0,047 y 0,055. Sesgo de ρ ≤ 0,008 en valor absoluto.
- **Límites de la validación:** el proceso generador es el modelo bien especificado con la W verdadera, errores normales con heterocedasticidad moderada y X fija; no cubre una W equivocada ni una dependencia no espacial (factor común, tendencia regional), que es la amenaza más probable en datos reales. El resultado habilita las herramientas bajo esos supuestos; la sensibilidad a la elección de W queda para la fase de estimación (los dos W del pre-registro).

# sdid_placebo_h1h2 · SDID con placebo (H1/H2) y variante IPVA (adenda 2, B)

Herramienta de V15 (preregistro_v15.md sección 6; adenda 1 punto 13). Código: `src/v15/montecarlo/sdid_placebo_h1h2.py` y `_comun_panel_v15.py`; semilla `SeedSequence([20261010, 1, escenario*10+etapa]).spawn(R)` (una réplica = un generador).

## Proceso generador (declarado antes de simular)
**Estructura leída (códigos, calendario, geometría; ningún valor de resultado):** municipios catalanes de entrenamiento con renta de Incasòl (611), cohortes de `regulacion_zonas` (2024T1: 128; 2024T4: 113; nunca tratados: 370) y centroides de `data/base/geo`. Se toman 124 tratados de la cohorte 2024T1 (234 × 128/241, del recuento de la adenda 1) y 74 donantes nunca tratados al azar (el filtro de ≥ 5 contratos no se reproduce porque exigiría leer el número de contratos); la variante de 10 km usa los 14 donantes de esos 74 a ≥ 10 km de cualquier municipio tratado (la adenda cuenta 13).
Calendario (adenda 1, puntos 1 y 6): 7 trimestres previos (2022T2-2023T4; pesos de SDID con los 5 primeros) y 9 posteriores (2024T1-2026T1), ATT = media de los 9.
**Resultado simulado (log):** y_it = mu_i + d_i t + g1_i f1_t + g2_i f2_t + s_it + e_it + efecto.
- mu_i ~ N(0,1); d_i ~ N(0; 0,002²) por trimestre (heterogeneidad de tendencia no relacionada con el tratamiento).
- f1, f2 factores comunes AR(1) con ρ = 0,6 y sd 0,03 (dependencia transversal); g1_i ~ N(1; 0,5²); g2_i = campo espacial exponencial (alcance 60 km) N(0,1).
- s_it: campo espacial exp(-d/25 km), AR(1) ρ = 0,5, sd 0,02 (correlación espacial por distancia entre centroides reales).
- e_it: AR(1) ρ = 0,5 con sd marginal sd_e × exp(0,5 z_i − 0,125) (heterogeneidad entre municipios; sd_e = 0,05 en H1, 0,15 en H2). Valores declarados, no estimados con datos reales.
**Efecto (solo tratados, 9 trimestres posteriores):** nulo = 0. Alternativa de referencia = −0,05 (H1; literatura citada en el pre-registro) y −0,13 (H2), con heterogeneidad tau_i = tau (1 + 0,5 z_i); la verdad de la cobertura es el ATT muestral (media de tau_i). Potencia además frente al MDE80 del pre-registro (−0,022 en H1; −0,039 en H2).
**Escenarios:** S1 (H1, 124 tratados y 74 donantes), S2 (H1, 14 donantes a ≥ 10 km), S3 (H2, 74 donantes, más ruido) y S4 (variante R-IPVA, ver abajo).
**S4 (adenda 2, B):** panel anual 2015-2023 (9 previos) + 2024 (1 posterior), 124 municipios tratados con zona vigente en 2024 (cualquier CCAA, códigos de `regulacion_zonas` presentes en el entrenamiento) y 382 donantes de provincias sin zona (al azar entre los municipios de entrenamiento con SERPAVI); clusters = provincia. Mismo proceso con sd_e = 0,02, más un choque provincia-año AR(1) (ρ = 0,5, sd 0,015), efecto de referencia −0,02 (diluido: el IPVA mide el stock de contratos), MDE −0,04.

## Inferencias
- **Principal (preregistro H1):** error típico por bootstrap de placebo (Arkhangelsky et al., alg. 4), IC normal ± 1,96 SE. En el Monte Carlo B = 99 réplicas de placebo (el pre-registro usa 1.000: se reduce por coste, 45 min; con B = 99 el SE tiene un error relativo ≈ 7 %). El algoritmo literal reasigna N_tr = 124 donantes como tratados: **no es computable con 74 o 14 donantes**. Se reportan dos variantes de diagnóstico con m = N_co/2 placebo-tratados: sin reescalar y reescalada por sqrt(m/N_tr). No cuentan como la inferencia principal.
- **Alternativa nombrada en la adenda 1 (punto 5):** wild cluster bootstrap-t de Webb por municipio sobre la puntuación SDID (pesos fijos; 999 réplicas; nulo impuesto). En S4 es la inferencia especificada (clusters = provincia; adenda 2, B).
- Para S1-S3 la inferencia principal es la del placebo; si no es computable o no pasa, se prueba solo Webb; si tampoco, «NO APTO → diseño solo descriptivo».
- Criterio: tamaño al 5 % en [0,04; 0,06] con R = 2.000 bajo el nulo y cobertura del IC 95 % en [0,92; 0,97] bajo la alternativa de referencia. Potencia, sesgo y RMSE informados.

<!-- RESULTADOS -->
## Resultados (R nulo = 2000, R ref = 2000, R mde = 400; B placebo = 99; Webb 999; semilla 20261010, k = 1)

| escenario | inferencia | efecto | R | R_validas | sesgo | rmse | cobertura | rechazo(tamaño|potencia) | ancho_medio_ic | segundos | provincias_tratadas | provincias_donantes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1_H1_74donantes | placebo_literal | nulo | 2000 | 0 | nan | nan | nan | nan | nan | 317.3261 | nan | nan |
| S1_H1_74donantes | placebo_m_sin_escalar | nulo | 2000 | 2000 | -0.0003 | 0.0135 | 0.9515 | 0.0485 | 0.0521 | 317.3261 | nan | nan |
| S1_H1_74donantes | placebo_m_escalado | nulo | 2000 | 2000 | -0.0003 | 0.0135 | 0.7290 | 0.2710 | 0.0285 | 317.3261 | nan | nan |
| S1_H1_74donantes | webb_cluster | nulo | 2000 | 2000 | -0.0003 | 0.0135 | 0.7895 | 0.2080 | 0.0319 | 317.3261 | nan | nan |
| S1_H1_74donantes | placebo_literal | ref | 2000 | 0 | nan | nan | nan | nan | nan | 360.5893 | nan | nan |
| S1_H1_74donantes | placebo_m_sin_escalar | ref | 2000 | 2000 | -0.0005 | 0.0138 | 0.9430 | 0.9555 | 0.0519 | 360.5893 | nan | nan |
| S1_H1_74donantes | placebo_m_escalado | ref | 2000 | 2000 | -0.0005 | 0.0138 | 0.7325 | 0.9910 | 0.0283 | 360.5893 | nan | nan |
| S1_H1_74donantes | webb_cluster | ref | 2000 | 2000 | -0.0005 | 0.0138 | 0.8010 | 0.9875 | 0.0331 | 360.5893 | nan | nan |
| S1_H1_74donantes | placebo_literal | mde | 400 | 0 | nan | nan | nan | nan | nan | 64.3920 | nan | nan |
| S1_H1_74donantes | placebo_m_sin_escalar | mde | 400 | 400 | 0.0005 | 0.0134 | 0.9625 | 0.3875 | 0.0526 | 64.3920 | nan | nan |
| S1_H1_74donantes | placebo_m_escalado | mde | 400 | 400 | 0.0005 | 0.0134 | 0.7325 | 0.7125 | 0.0287 | 64.3920 | nan | nan |
| S1_H1_74donantes | webb_cluster | mde | 400 | 400 | 0.0005 | 0.0134 | 0.7800 | 0.6675 | 0.0323 | 64.3920 | nan | nan |
| S2_H1_14donantes_10km | placebo_literal | nulo | 2000 | 0 | nan | nan | nan | nan | nan | 342.6706 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_sin_escalar | nulo | 2000 | 2000 | 0.0002 | 0.0221 | 0.9845 | 0.0155 | 0.1196 | 342.6706 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_escalado | nulo | 2000 | 2000 | 0.0002 | 0.0221 | 0.4950 | 0.5050 | 0.0284 | 342.6706 | nan | nan |
| S2_H1_14donantes_10km | webb_cluster | nulo | 2000 | 2000 | 0.0002 | 0.0221 | 0.7715 | 0.2260 | 0.0524 | 342.6706 | nan | nan |
| S2_H1_14donantes_10km | placebo_literal | ref | 2000 | 0 | nan | nan | nan | nan | nan | 411.4694 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_sin_escalar | ref | 2000 | 2000 | 0.0004 | 0.0217 | 0.9825 | 0.3610 | 0.1203 | 411.4694 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_escalado | ref | 2000 | 2000 | 0.0004 | 0.0217 | 0.5210 | 0.9450 | 0.0286 | 411.4694 | nan | nan |
| S2_H1_14donantes_10km | webb_cluster | ref | 2000 | 2000 | 0.0004 | 0.0217 | 0.8015 | 0.8635 | 0.0534 | 411.4694 | nan | nan |
| S2_H1_14donantes_10km | placebo_literal | mde | 400 | 0 | nan | nan | nan | nan | nan | 84.6788 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_sin_escalar | mde | 400 | 400 | 0.0003 | 0.0247 | 0.9725 | 0.0800 | 0.1180 | 84.6788 | nan | nan |
| S2_H1_14donantes_10km | placebo_m_escalado | mde | 400 | 400 | 0.0003 | 0.0247 | 0.4425 | 0.6700 | 0.0280 | 84.6788 | nan | nan |
| S2_H1_14donantes_10km | webb_cluster | mde | 400 | 400 | 0.0003 | 0.0247 | 0.7600 | 0.4850 | 0.0517 | 84.6788 | nan | nan |
| S3_H2_74donantes | placebo_literal | nulo | 2000 | 0 | nan | nan | nan | nan | nan | 508.0531 | nan | nan |
| S3_H2_74donantes | placebo_m_sin_escalar | nulo | 2000 | 2000 | 0.0001 | 0.0243 | 0.9920 | 0.0080 | 0.1337 | 508.0531 | nan | nan |
| S3_H2_74donantes | placebo_m_escalado | nulo | 2000 | 2000 | 0.0001 | 0.0243 | 0.8640 | 0.1360 | 0.0730 | 508.0531 | nan | nan |
| S3_H2_74donantes | webb_cluster | nulo | 2000 | 2000 | 0.0001 | 0.0243 | 0.9050 | 0.0930 | 0.0806 | 508.0531 | nan | nan |
| S3_H2_74donantes | placebo_literal | ref | 2000 | 0 | nan | nan | nan | nan | nan | 622.9112 | nan | nan |
| S3_H2_74donantes | placebo_m_sin_escalar | ref | 2000 | 2000 | -0.0002 | 0.0240 | 0.9965 | 0.9870 | 0.1333 | 622.9112 | nan | nan |
| S3_H2_74donantes | placebo_m_escalado | ref | 2000 | 2000 | -0.0002 | 0.0240 | 0.8650 | 0.9995 | 0.0728 | 622.9112 | nan | nan |
| S3_H2_74donantes | webb_cluster | ref | 2000 | 2000 | -0.0002 | 0.0240 | 0.9185 | 0.9995 | 0.0837 | 622.9112 | nan | nan |
| S3_H2_74donantes | placebo_literal | mde | 400 | 0 | nan | nan | nan | nan | nan | 94.3444 | nan | nan |
| S3_H2_74donantes | placebo_m_sin_escalar | mde | 400 | 400 | -0.0001 | 0.0239 | 0.9900 | 0.1425 | 0.1339 | 94.3444 | nan | nan |
| S3_H2_74donantes | placebo_m_escalado | mde | 400 | 400 | -0.0001 | 0.0239 | 0.8675 | 0.5350 | 0.0732 | 94.3444 | nan | nan |
| S3_H2_74donantes | webb_cluster | mde | 400 | 400 | -0.0001 | 0.0239 | 0.9025 | 0.4825 | 0.0812 | 94.3444 | nan | nan |
| S4_IPVA_provincias | webb_cluster | nulo | 2000 | 2000 | 0.0001 | 0.0127 | 0.7170 | 0.2825 | 0.0299 | 46.0487 | 5.0000 | 31.0000 |
| S4_IPVA_provincias | webb_cluster | ref | 2000 | 2000 | 0.0003 | 0.0129 | 0.7145 | 0.6645 | 0.0292 | 45.8063 | 5.0000 | 31.0000 |
| S4_IPVA_provincias | webb_cluster | mde | 400 | 400 | 0.0003 | 0.0128 | 0.7225 | 0.9400 | 0.0294 | 8.3846 | 5.0000 | 31.0000 |

**Veredictos**

- S1_H1_74donantes: **NO APTO → diseño solo descriptivo**
- S2_H1_14donantes_10km: **NO APTO → diseño solo descriptivo**
- S3_H2_74donantes: **NO APTO → diseño solo descriptivo**
- S4_IPVA_provincias: **NO APTO → diseño solo descriptivo**
- S1_H1_74donantes / placebo_literal: NO APTO — no computable (N donantes <= N tratados + 5)
- S1_H1_74donantes / placebo_m_sin_escalar: APTO 
- S1_H1_74donantes / placebo_m_escalado: NO APTO — tamaño 0.2710 fuera de [0.04; 0.06]; cobertura 0.7325 fuera de [0.92; 0.97]
- S1_H1_74donantes / webb_cluster: NO APTO — tamaño 0.2080 fuera de [0.04; 0.06]; cobertura 0.8010 fuera de [0.92; 0.97]
- S2_H1_14donantes_10km / placebo_literal: NO APTO — no computable (N donantes <= N tratados + 5)
- S2_H1_14donantes_10km / placebo_m_sin_escalar: NO APTO — tamaño 0.0155 fuera de [0.04; 0.06]; cobertura 0.9825 fuera de [0.92; 0.97]
- S2_H1_14donantes_10km / placebo_m_escalado: NO APTO — tamaño 0.5050 fuera de [0.04; 0.06]; cobertura 0.5210 fuera de [0.92; 0.97]
- S2_H1_14donantes_10km / webb_cluster: NO APTO — tamaño 0.2260 fuera de [0.04; 0.06]; cobertura 0.8015 fuera de [0.92; 0.97]
- S3_H2_74donantes / placebo_literal: NO APTO — no computable (N donantes <= N tratados + 5)
- S3_H2_74donantes / placebo_m_sin_escalar: NO APTO — tamaño 0.0080 fuera de [0.04; 0.06]; cobertura 0.9965 fuera de [0.92; 0.97]
- S3_H2_74donantes / placebo_m_escalado: NO APTO — tamaño 0.1360 fuera de [0.04; 0.06]; cobertura 0.8650 fuera de [0.92; 0.97]
- S3_H2_74donantes / webb_cluster: NO APTO — tamaño 0.0930 fuera de [0.04; 0.06]; cobertura 0.9185 fuera de [0.92; 0.97]
- S4_IPVA_provincias / webb_cluster: NO APTO — tamaño 0.2825 fuera de [0.04; 0.06]; cobertura 0.7145 fuera de [0.92; 0.97]

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto por escenario:** S1_H1_74donantes: NO APTO → diseño solo descriptivo; S2_H1_14donantes_10km: NO APTO → diseño solo descriptivo; S3_H2_74donantes: NO APTO → diseño solo descriptivo; S4_IPVA_provincias: NO APTO → diseño solo descriptivo. Condición que falla: el error típico por placebo, tal como lo fija el pre-registro (N_tr = 124 placebo-tratados), **no es computable**: exige más donantes (74 o 14) que tratados (124). Con la inferencia alternativa de la adenda (wild cluster bootstrap de Webb por municipio) el tamaño es 0,208 (S1), 0,226 (S2) y 0,093 (S3), y la cobertura 0,801, 0,801 y 0,918. En la variante R-IPVA (clusters = provincia, ≈ 5 provincias tratadas) el tamaño es 0,282 y la cobertura 0,715.
- **Por qué:** el SDID puntual es insesgado en el proceso (sesgo ≈ 0; RMSE 0,0138 en S1), pero el error típico por municipio subestima la dispersión real (en S1 la anchura media del IC95 de Webb es 0,0331, es decir, un SE de ≈ 0,0085 frente a un RMSE de 0,0138) porque ignora la correlación espacial entre municipios próximos y las cargas factoriales espaciales (campos de 25 y 60 km del proceso generador). Ningún remuestreo por municipio recupera esa dependencia: haría falta agrupar por zona o por distancia.
- **Variantes de diagnóstico del placebo (no cumplen el pre-registro):** con m = N_co/2 placebo-tratados sin reescalar el tamaño es 0,0485 en S1 (dentro del criterio solo por coincidencia: sobrestima el SE en S2 y S3, con 0,0155 y 0,0080); reescalado por √(m/N_tr) el tamaño sube a 0,271. Ninguna variante es robusta a los tres escenarios.
- **Consecuencia para H1/H2 (adenda 1, puntos 2 y 13):** con esta inferencia el SDID no puede sostener C3; el estimador puntual sigue siendo válido como descriptivo. Condicionado a los niveles de ruido declarados (supuestos del proceso, no medidos), el MDE80 que implica el RMSE del estimador es ≈ 3,9 % en renta con 74 donantes (S1), ≈ 6,1 % con los 14 donantes a ≥ 10 km (S2; supera el 5 % de la regla de paso a exploratoria de la adenda) y ≈ 6,7 % en log(1 + contratos) (S3; por debajo del 13 %).

# westerlund_csardl · E1: Westerlund con bootstrap, CIPS y CS-ARDL (N = 40, T = 98, factor común)

Herramienta de V15 (preregistro_v15.md E1 y sección 6). Código: `src/v15/montecarlo/westerlund_csardl.py`; semilla `SeedSequence([20261010, 6, etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **Dimensiones (estructura de E1):** N = 40 provincias de entrenamiento (41 con IPC de alquiler; 38 con valor tasado), T = 98 trimestres (alquiler desde 2002T1 hasta 2026T2); 50 trimestres de rodaje descartados.
- **Regresor (log IPC de alquiler simulado), I(1) con factor común:** Δx_it = 0,2 + 0,5 γx_i f1_t + u_it, con f1 AR(1) (ρ = 0,5), γx_i ~ N(1; 0,5²) y u_it = e_it + 0,25 (e_{i−1,t} + e_{i+1,t}) (correlación espacial en anillo; e ~ N(0; 0,8²)).
- **Resultado (log valor tasado simulado):** y_it = β_i x_it + z_it, con β_i ~ N(0,8; 0,2²) (elasticidad de largo plazo por unidad; la verdad es su media muestral) y z_it = ρ_i z_{i,t−1} + 0,5 c_i f2_t + 0,7 e'_it (f2 segundo factor común AR(1) con ρ = 0,5 en las innovaciones, c_i ~ N(1; 0,5²), e' con el mismo anillo espacial). El factor común entra en las innovaciones (incrementos persistentes, como el crecimiento del precio), no como componente estacionario de nivel.
- **Nota de revisión (declarada):** la primera versión del proceso añadía además un componente estacionario de nivel λ_i f2_t en y_it. Eso crea una raíz de media móvil negativa en Δy, que ningún contraste tipo ADF con un rezago maneja (distorsión de tamaño conocida) y no se parece al crecimiento observado del precio (autocorrelación positiva). Con esa versión el tamaño del bootstrap de Westerlund salió 0,56 (Gτ), 0,72 (Gα), 0,50 (Pτ) y 0,65 (Pα), el de CIPS 0,0125 y la cobertura de CS-ARDL 0,9925. Se sustituyó por el proceso anterior de este párrafo antes de interpretar nada más; ambos resultados se declaran aquí.
  - **Nulo (sin cointegración):** ρ_i = 1 (z es I(1): regresión espuria con dependencia transversal).
  - **Alternativa (cointegración):** ρ_i = 1 + α_i con α_i ~ U(−0,06; −0,02), media −0,04 (velocidad de ajuste trimestral de referencia del pre-registro; semivida ≈ 17 trimestres).
- **Westerlund (2007):** modelo de corrección de errores por unidad Δy_s = δ_i + α_i y_{s−1} + λ_i x_{s−1} + a_i Δy_{s−1} + b_i Δx_s + b'_i Δx_{s−1} + e (1 rezago, sin adelantos) y estadísticos Gτ, Gα, Pτ, Pα (agrupados con las variables auxiliares eliminadas por unidad). **Valores p por bootstrap de Westerlund:** VAR(1) de (Δy, Δx) por unidad bajo el nulo; remuestreo de los residuos con el MISMO índice temporal para todas las unidades (conserva la dependencia transversal), reconstrucción en niveles y recálculo; contraste de cola izquierda; B = 99 réplicas (con B = 99 el contraste al 5 % es exacto: rango ≥ 95 de 100). El estadístico principal declarado es **Gτ** (admite heterogeneidad); los otros tres se reportan.
- **CIPS (Pesaran 2007):** CADF con intercepto, 1 rezago y medias transversales, media de los t. **Tamaño:** sobre la serie x (I(1) con factor), en todas las réplicas. **Potencia:** panel estacionario con φ_i ~ U(0,94; 0,98) (velocidad de ajuste media −0,04) con factor común, 1.000 réplicas. Valor crítico por bootstrap de bloques móviles de las diferencias (conjunto entre unidades, longitud 9), B = 199, raíz unitaria impuesta.
- **CS-ARDL (Chudik-Pesaran 2015):** ARDL(1,1) por unidad aumentado con las medias transversales de y y x y sus 4 rezagos (⌊T^(1/3)⌋); elasticidad de largo plazo θ = media de (b0 + b1)/(1 − φ) y velocidad de ajuste media φ − 1, sobre la alternativa (cointegración). Inferencia: bootstrap de bloques móviles (longitud 9) de las filas de regresión conjuntas, B = 99, IC normal con EE bootstrap. Cobertura de la media muestral de β_i y de la velocidad media verdadera; tamaño = 1 − cobertura.
- **Criterio:** tamaño en [0,04; 0,06] con R = 2.000 (Gτ, CIPS) y cobertura del IC95 de CS-ARDL en [0,92; 0,97]. Umbral de V15: potencia de Westerlund (Gτ) frente a −0,04 ≥ 0,5; si no, E1 solo descriptiva (independiente del veredicto de tamaño). El pre-registro no nombra inferencia alternativa para estas herramientas: si no pasan, «NO APTO → solo descriptivo».

<!-- RESULTADOS -->
## Resultados (R = 2000 nulo, 1000 alternativa; B Westerlund = 99, B CIPS = 199; semilla 20261010, k = 6)

| herramienta | R_nulo | tamano_5pct | R_alt | potencia_alpha_-0.04 | cobertura_95 | sesgo | rmse |
|---|---|---|---|---|---|---|---|
| Westerlund Gtau | 2000 | 0.1355 | 1000 | 0.3380 | nan | nan | nan |
| Westerlund Galpha | 2000 | 0.0930 | 1000 | 0.3350 | nan | nan | nan |
| Westerlund Ptau | 2000 | 0.1965 | 1000 | 0.4070 | nan | nan | nan |
| Westerlund Palpha | 2000 | 0.1810 | 1000 | 0.4590 | nan | nan | nan |
| CIPS (serie I(1)) | 2000 | 0.0105 | 1000 | 0.0780 | nan | nan | nan |
| CS-ARDL elasticidad de largo plazo | 2000 | 0.0075 | 2000 | 0.2045 | 0.9925 | -0.0187 | 1.1579 |
| CS-ARDL velocidad de ajuste media | 2000 | 0.9970 | 2000 | 1.0000 | 0.0030 | -0.1250 | 0.1262 |

**Umbral de V15:** potencia de Gτ frente a α = −0,04: 0.338 → E1 solo DESCRIPTIVA.

**Veredictos de tamaño/cobertura**

- Westerlund Gtau: **NO APTO → solo descriptivo** tamaño 0.1355 fuera de [0.04; 0.06]
- Westerlund Galpha: **NO APTO → solo descriptivo** tamaño 0.0930 fuera de [0.04; 0.06]
- Westerlund Ptau: **NO APTO → solo descriptivo** tamaño 0.1965 fuera de [0.04; 0.06]
- Westerlund Palpha: **NO APTO → solo descriptivo** tamaño 0.1810 fuera de [0.04; 0.06]
- CIPS (serie I(1)): **NO APTO → solo descriptivo** tamaño 0.0105 fuera de [0.04; 0.06]
- CS-ARDL elasticidad de largo plazo: **NO APTO → solo descriptivo** tamaño 0.0075 fuera de [0.04; 0.06]; cobertura 0.9925 fuera de [0.92; 0.97]
- CS-ARDL velocidad de ajuste media: **NO APTO → solo descriptivo** tamaño 0.9970 fuera de [0.04; 0.06]; cobertura 0.0030 fuera de [0.92; 0.97]

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Umbral de V15:** la potencia de Westerlund (Gτ, bootstrap, B = 99) frente a una velocidad de ajuste de −0,04 trimestral es **0,338** (Gα 0,335, Pτ 0,407, Pα 0,459), menor que 0,5 en los cuatro estadísticos: **E1 se reporta solo como descriptiva**, con independencia del tamaño.
- **Tamaño:** Gτ 0,136, Gα 0,093, Pτ 0,197, Pα 0,181: el bootstrap (VAR(1) por unidad, remuestreo temporal conjunto) sobre-rechaza con N = 40, T = 98 y raíces cercanas a la unidad; la potencia queda inflada por ese sobre-rechazo. **CIPS** con bootstrap de bloques es conservador (0,0105) y con potencia 0,078 frente a φ ≈ 0,96.
- **CS-ARDL:** la elasticidad de largo plazo tiene RMSE 1,158 (frente a una elasticidad de 0,8: el cociente (b0+b1)/(1−φ) es inestable por unidad) y cobertura 0,993 (IC enormes); la **velocidad de ajuste** media sale sesgada en -0,125 (verdad −0,04) con cobertura 0,0030: el ARDL(1,1) con las medias transversales de y y x y sus 4 rezagos (14 regresores con 94 observaciones) probablemente absorbe la tendencia común (ȳ y x̄ están casi colineales) y estima la reversión de la desviación respecto a la media, no la del nivel; no se ha contrastado esta explicación.
- **Veredictos:** ver lista anterior: ninguna herramienta pasa. La adenda no nombra alternativa para estas herramientas.

# wild_webb_v15 · wild cluster bootstrap de Webb

Herramienta de V15 (preregistro_v15.md H1/H2 «pocos clusters con wild cluster bootstrap de pesos Webb», sección 6; adenda 1 punto 5 y adenda 2 B). Código: `src/v15/montecarlo/wild_webb_v15.py` (usa `_comun_panel_v15`, `sdid_placebo_h1h2.estructura_s4` y `akm_municipal`); semilla `SeedSequence([20261010, 8, escenario*10+etapa]).spawn(R)`.

## Proceso generador (declarado antes de simular)
- **W1 (H1/H2):** 124 tratados de la cohorte 2024T1 y 74 nunca tratados (códigos y centroides reales de Incasòl/geo), 7 trimestres previos y 9 posteriores; clusters = municipio (G = 198). Resultado simulado con el proceso de `sdid_placebo_h1h2` (factores comunes AR(1), campo espacial de 25 km, AR(1) ρ = 0,5, sd_e = 0,05 heterogénea). Efecto en los 9 trimestres posteriores de los tratados: nulo = 0; referencia = −0,05 con tau_i = tau(1 + 0,5 z_i); MDE80 = −0,022. Estimador: MCO con efectos de municipio y trimestre (TWFE) del indicador tratado × posterior (el estimador del pre-registro es SDID/CS; aquí se valida la inferencia de Webb, que es común a los tres).
- **W2 (H4):** estructura de `akm_municipal` (1.451 municipios, 28 orígenes, cuotas 2003 reales, T = 11, provincia × año absorbidos), clusters = provincia (G = 38, muy desiguales: la más grande concentra ≈ 10 % de los municipios). Forma reducida y_it = β_rf z_it + ε_it con el error con dependencia por cuota y factor común de `akm_municipal` (σ_y = 0,05). Nulo β_rf = 0; referencia β_rf = 0,004 (≈ 0,01 × primera etapa 0,39); MDE 0,003.
- **W3 (R-IPVA, adenda 2 B):** 124 municipios tratados y 382 donantes (estructura de S4 de `sdid_placebo_h1h2`: tratados en las pocas provincias con zona, donantes en provincias sin zona), 9 años previos y 1 posterior; clusters = provincia (G ≈ 36, de ellos ≈ 5 tratados: pocos clusters tratados). Mismo proceso de S4 (choque provincia-año AR(1)). Efecto de referencia −0,02, MDE −0,04. TWFE con efectos de municipio y año.
- **Inferencias comparadas:** (a) wild cluster bootstrap-t de Webb (6 puntos) con nulo impuesto (WCR) para el contraste y no impuesto (WCU) para el IC95 percentil-t; (b) error agrupado CR1 con t(G − 1) como referencia. B = 9.999 réplicas bootstrap (como en V15; el cierre algebraico por cluster hace barato usar más de 999) y, como sensibilidad, B = 999 con las primeras 999 columnas.
- **Cierre algebraico:** como el efecto fijo de unidad está anidado en el cluster, el estadístico bootstrap se calcula sobre sumas por cluster (sin rehacer la regresión por réplica); es exactamente la regresión bootstrap con los residuos reponderados (Roodman et al., 2019), con los efectos de tiempo recentrados.
- **Medidas:** tamaño (rechazo de β = 0 con tau = 0), cobertura del IC95 bajo la referencia (verdad = ATT muestral en W1 y W3, β_rf en W2), potencia (referencia y MDE), sesgo y RMSE. R = 2.000.
- **Criterio:** tamaño en [0,04; 0,06] y cobertura en [0,92; 0,97] para Webb. El pre-registro no nombra alternativa; si falla, «NO APTO → inferencia solo descriptiva».

<!-- RESULTADOS -->
## Resultados (R = 2000 por etapa; B = 9999; semilla 20261010, k = 8)

| escenario | inferencia | G | R | tamano_5pct | cobertura_95 | potencia_ref | potencia_mde | sesgo | rmse | ancho_ic |
|---|---|---|---|---|---|---|---|---|---|---|
| W1_H1H2_198municipios | Webb WCR/WCU B=9999 | 198 | 2000 | 0.2155 | 0.7740 | 0.9860 | 0.7100 | -0.0004 | 0.0141 | 0.0319 |
| W1_H1H2_198municipios | Webb B=999 | 198 | 2000 | 0.2135 | 0.7735 | 0.9860 | 0.7110 | -0.0004 | 0.0141 | 0.0319 |
| W1_H1H2_198municipios | CR1 t(G-1) | 198 | 2000 | 0.2165 | 0.7735 | 0.9865 | 0.7140 | -0.0004 | 0.0141 | 0.0318 |
| W2_H4_38provincias | Webb WCR/WCU B=9999 | 38 | 2000 | 0.4240 | 0.6350 | 0.5165 | 0.4980 | 0.0001 | 0.0062 | 0.0136 |
| W2_H4_38provincias | Webb B=999 | 38 | 2000 | 0.4225 | 0.6330 | 0.5155 | 0.4950 | 0.0001 | 0.0062 | 0.0136 |
| W2_H4_38provincias | CR1 t(G-1) | 38 | 2000 | 0.5495 | 0.4570 | 0.6215 | 0.6030 | 0.0001 | 0.0062 | 0.0083 |
| W3_RIPVA_36provincias_pocos_tratados | Webb WCR/WCU B=9999 | 36 | 2000 | 0.1230 | 0.7760 | 0.3600 | 0.7350 | 0.0005 | 0.0214 | 0.0579 |
| W3_RIPVA_36provincias_pocos_tratados | Webb B=999 | 36 | 2000 | 0.1230 | 0.7780 | 0.3655 | 0.7420 | 0.0005 | 0.0214 | 0.0578 |
| W3_RIPVA_36provincias_pocos_tratados | CR1 t(G-1) | 36 | 2000 | 0.3150 | 0.7120 | 0.5355 | 0.8450 | 0.0005 | 0.0214 | 0.0425 |

**Veredictos (Webb B = 9.999)**

- W1_H1H2_198municipios: **NO APTO → inferencia solo descriptiva**
- W2_H4_38provincias: **NO APTO → inferencia solo descriptiva**
- W3_RIPVA_36provincias_pocos_tratados: **NO APTO → inferencia solo descriptiva**

- W1_H1H2_198municipios / Webb WCR/WCU B=9999: NO APTO — tamaño 0.2155 fuera de [0.04; 0.06]; cobertura 0.7740 fuera de [0.92; 0.97]
- W1_H1H2_198municipios / Webb B=999: NO APTO — tamaño 0.2135 fuera de [0.04; 0.06]; cobertura 0.7735 fuera de [0.92; 0.97]
- W1_H1H2_198municipios / CR1 t(G-1): NO APTO — tamaño 0.2165 fuera de [0.04; 0.06]; cobertura 0.7735 fuera de [0.92; 0.97]
- W2_H4_38provincias / Webb WCR/WCU B=9999: NO APTO — tamaño 0.4240 fuera de [0.04; 0.06]; cobertura 0.6350 fuera de [0.92; 0.97]
- W2_H4_38provincias / Webb B=999: NO APTO — tamaño 0.4225 fuera de [0.04; 0.06]; cobertura 0.6330 fuera de [0.92; 0.97]
- W2_H4_38provincias / CR1 t(G-1): NO APTO — tamaño 0.5495 fuera de [0.04; 0.06]; cobertura 0.4570 fuera de [0.92; 0.97]
- W3_RIPVA_36provincias_pocos_tratados / Webb WCR/WCU B=9999: NO APTO — tamaño 0.1230 fuera de [0.04; 0.06]; cobertura 0.7760 fuera de [0.92; 0.97]
- W3_RIPVA_36provincias_pocos_tratados / Webb B=999: NO APTO — tamaño 0.1230 fuera de [0.04; 0.06]; cobertura 0.7780 fuera de [0.92; 0.97]
- W3_RIPVA_36provincias_pocos_tratados / CR1 t(G-1): NO APTO — tamaño 0.3150 fuera de [0.04; 0.06]; cobertura 0.7120 fuera de [0.92; 0.97]

<!-- LECTURA -->
## Lectura (posterior a los resultados)
- **Veredicto:** W1_H1H2_198municipios: NO APTO → inferencia solo descriptiva; W2_H4_38provincias: NO APTO → inferencia solo descriptiva; W3_RIPVA_36provincias_pocos_tratados: NO APTO → inferencia solo descriptiva.
- El bootstrap de Webb es algebraicamente correcto (comprobado contra la regresión bootstrap explícita en tests/v15/test_mc_v15.py) y B = 9.999 no cambia nada frente a B = 999 (tamaño 0,2155 frente a 0,2135 en W1). Lo que falla es el supuesto de cluster: con 198 municipios (W1) el tamaño es 0,215 (el error agrupado CR1 da 0,216); con 38 provincias y dependencia por cuotas (W2) 0,424 (CR1: 0,549); con ≈ 5 provincias tratadas de 36 (W3) 0,123 (CR1: 0,315).
- **Interpretación:** Webb mejora a CR1 cuando hay pocos clusters (W3: de 0,315 a 0,123) pero no corrige la dependencia entre clusters (correlación espacial y por cuotas del proceso generador). Para H1/H2 y H4 no puede ser la inferencia que sostenga C3 si la dependencia entre clusters es del orden del proceso declarado.

