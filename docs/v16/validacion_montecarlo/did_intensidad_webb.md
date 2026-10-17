# did_intensidad_webb · Q2a (provincial, Webb) y Q2c (municipal, agrupado por provincia)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** Q2a: 41 provincias de entrenamiento, periodos [2017, 2018, 2019, 2022, 2023, 2024, 2025] (2017-2019 frente a 2022-2025; 2020-2021 fuera), posterior = 2022+,
  distancias entre centroides de data/base/geo/provincias.parquet. Q2c: 391 municipios con IPVA de entrenamiento en 37 provincias (tamaños de cluster reales: de 1 a
  67 municipios), años [2021, 2022, 2023, 2024], posterior = 2023-2024 (la adenda fija «la misma regla que Q2a»; el corte 2023 es una convención de esta validación).
- **Exposición:** e_i ~ N(0,1) estandarizada (log de la exposición). Q2a: campo gaussiano con correlación espacial exp(-d/300 km). Q2c: 40 % de la varianza común dentro de la provincia, 60 % municipal, estandarizada.
- **Resultado Q2a:** y_it = β·e_i·post_t + σ_P·ε_it, σ_P = 0.05; ε_it = √0,5·η_it + √0,3·(λ_i1 f_t1 + λ_i2 f_t2)/√2 + √0,2·u_it con η_it espacial (correlación exp(-d/300 km) entre provincias, AR(1) ρ = 0,7 en t),
  f factores comunes AR(1) ρ = 0,7, cargas λ ~ N(0,1) independientes de la exposición (la tendencia paralela se cumple), u AR(1) ρ = 0,5.
- **Resultado Q2c:** y_it = β·e_i·post_t + σ_M·ε_it, σ_M = 0.08; ε_it = √0,35·v_{prov(i)}t (choque provincia-año común) + √0,15·f_t·λ_i + √0,5·u_it, con v, f AR(1) ρ = 0,5 y u AR(1) ρ = 0,3. Efectos fijos de unidad y de año (absorbidos).
- **Nulo:** β = 0. **Alternativa:** β = 0.04 (por DT de la exposición): sesgo, RMSE, cobertura (inversión de la prueba en β = 0.04) y potencia.
- **Inferencias.** Q2a: wild cluster bootstrap con residuos restringidos, pesos de Webb de 6 puntos, B = bootstrap-t simétrico por provincia (principal, punto 3); referencia no candidata: CR1 por provincia con t(G-1).
  Q2c: CR1 agrupado por provincia con t(G-1) (principal, punto 3); Webb por provincia se informa como referencia extra (NO es la alternativa nombrada para Q2c, que no tiene ninguna).
- **Pocos clusters:** G = 41 (Q2a) y 37 muy desiguales (Q2c). **T corto:** 7 y 4 periodos.
- **Alternativa nombrada:** Q2a: Webb es la principal, sin otra; Q2c: ninguna. Si la principal no pasa → «NO APTO → diseño solo descriptivo».
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97] (cobertura de la prueba bootstrap invertida en el valor verdadero).

<!-- RESULTADOS -->
## Resultados (R = 2000 réplicas por diseño, B = 399; semilla 20261010, k = 33)

| diseno | inferencia | R | tamano_5pct | tamano_ic95 | cobertura_95 | potencia_beta_ref | sesgo | rmse |
|---|---|---|---|---|---|---|---|---|
| Q2a provincial | Webb (principal) | 2000 | 0.1420 | [0.1267, 0.1573] | 0.8570 | 0.9955 | -0.0004 | 0.0087 |
| Q2a provincial | CR1 por provincia (referencia) | 2000 | 0.1720 | [0.1555, 0.1885] | 0.8280 | 0.9970 | -0.0004 | 0.0087 |
| Q2c municipal | CR1 por provincia (principal) | 2000 | 0.0975 | [0.0845, 0.1105] | 0.9025 | 0.9955 | -0.0000 | 0.0076 |
| Q2c municipal | Webb por provincia (referencia extra) | 2000 | 0.0605 | [0.0501, 0.0709] | 0.9375 | 0.9900 | -0.0000 | 0.0076 |


**Veredicto: Q2a NO APTO → diseño solo descriptivo; Q2c NO APTO → diseño solo descriptivo.**

- Q2a: condición que falla: tamaño 0.1420 fuera de [0.04; 0.06]; cobertura 0.8570 fuera de [0.92; 0.97].

- Q2c: condición que falla: tamaño 0.0975 fuera de [0.04; 0.06]; cobertura 0.9025 fuera de [0.92; 0.97].

**Comprobación puntual de la implementación (R = 600, B = 199, Q2a sin dependencia espacial entre provincias, resto igual):** tamaño de Webb 0,043 y de CR1 0,085. El bootstrap está bien implementado; el sobre-rechazo de Webb en el proceso del repositorio (0,142) procede de la correlación espacial entre provincias en la exposición y en el error, que el agrupamiento por provincia no recoge. Q2a queda como diseño solo descriptivo. En Q2c el CR1 por provincia sobre-rechaza (0,0975); Webb por provincia (0,0605, referencia extra, no es la alternativa nombrada) tampoco entra en [0,04; 0,06].
