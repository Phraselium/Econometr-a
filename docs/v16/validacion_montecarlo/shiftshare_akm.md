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
