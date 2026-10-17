# blp_gates · prueba conjunta de heterogeneidad BLP/GATES (una por pregunta con diseño; R20)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** 1,728 municipios de entrenamiento con SERPAVI de alquiler en 2021 y 2024 (solo disponibilidad del dato) en 38 provincias (clusters de tamaño real, de 1 a 203).
- **Moderadores (fijados por la adenda):** renta media, población, % de extranjeros, % de vivienda turística y obra nueva per cápita. Se simulan con una cópula gaussiana (correlación 0,3 entre moderadores)
  con un 30 % de la varianza común dentro de la provincia; marginales: renta lognormal, población lognormal de cola pesada, % de extranjeros beta, % VUT con cero en el 40 % y lognormal en el resto, obra nueva gamma. Se estandarizan para el efecto.
- **Tratamiento:** asignado por provincia (cluster) al azar con probabilidad p = 0.5 (conocida): estructura de pocos clusters, como las preguntas de diseño por CCAA/provincia.
- **Resultado (Δlog, un periodo):** Y_i = g(Z_i) + v_prov(i) + τ(Z_i)·D_i + 0.08·ε_i, con g no lineal (suma de efectos suaves y una interacción), v_prov ~ N(0,0.048²) (choque de provincia), ε ~ N(0,1).
  **Nulo (efecto homogéneo):** τ(Z) = 0.03. **Alternativa (heterogeneidad):** τ(Z) = 0.03 + 0.03·h(Z), h = combinación estandarizada de pct_vut (no lineal) y renta (media 0, DT 1).
- **Procedimiento:** 11 particiones aleatorias de las PROVINCIAS (mitad auxiliar A, mitad principal M; partir por cluster evita fugas). En A: ExtraTrees (60 árboles, hoja ≥ 15) por brazo → B(Z) = m0(Z), S(Z) = m1(Z) − m0(Z).
  En M: BLP: Y ~ 1 + B + S + (D−p) + (D−p)(S−S̄), ponderado 1/(p(1−p)); GATES: Y ~ 1 + B + S + Σ_k γ_k (D−p)·1(S ∈ cuantil k), K = 5. Covarianza CR1 por provincia (en M).
- **Prueba conjunta (principal):** Wald de igualdad de los 5 GATES (γ1 = … = γ5), referencia F(4, G_M − 1). Agregación entre particiones (CDDF): p = min(1, 2·mediana de los p). Secundarias informadas: BLP β2 = 0 y γ5 = γ1.
  IC del efecto medio (β1 del BLP): por partición al 97,5 % con t(G_M − 1), mediana de los límites (ajuste CDDF); cobertura frente al efecto medio poblacional τ0 = 0.03 (la heterogeneidad h tiene media 0).
- **Alternativa nombrada en el punto 3:** ninguna (la prueba conjunta se adopta tal cual). Si no pasa → «NO APTO → diseño solo descriptivo» (los subgrupos ya son descriptivos C4).
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 bajo efecto homogéneo, cobertura del IC del efecto medio en [0,92; 0,97]; se informa la potencia bajo la alternativa. Un tamaño de 0,0 es NO APTO.

<!-- RESULTADOS -->
## Resultados (R = 2000 réplicas válidas de 2000, S = 11 particiones; semilla 20261010, k = 35)

| prueba | R | tamano_5pct | tamano_ic95 | potencia_heterogeneidad | cobertura_ate_95 | sesgo_ate | rmse_ate |
|---|---|---|---|---|---|---|---|
| conjunta: igualdad de los 5 GATES (principal) | 2000 | 0.0050 | [0.0019, 0.0081] | 0.1880 | 0.9850 | -0.0004 | 0.0226 |
| BLP beta2 = 0 (secundaria) | 2000 | 0.0050 | [0.0019, 0.0081] | 0.2120 | nan | nan | nan |
| GATES gamma5 = gamma1 (secundaria) | 2000 | 0.0025 | [0.0003, 0.0047] | 0.1840 | nan | nan | nan |


Cobertura del IC 95 % del efecto medio bajo efecto homogéneo: 0.9885.

**Veredicto: NO APTO → diseño solo descriptivo.**

Condición que falla: tamaño 0.0050 fuera de [0.04; 0.06]; cobertura 0.9885 fuera de [0.92; 0.97].
