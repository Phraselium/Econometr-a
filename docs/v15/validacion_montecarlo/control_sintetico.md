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
