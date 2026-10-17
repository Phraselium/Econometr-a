# conley_seccion · Q3-b (corte transversal por sección, Conley a 2 km, efectos fijos de municipio)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** 10,815 secciones de entrenamiento (de 11,574 con SERPAVI 2021 y 2024 disponibles, tras `unidad_sellada_v16`; se descartan las de
  municipios con una sola sección, cuyo efecto fijo las absorbe) en 851 municipios y 38 provincias; centroides de data/base/geo/secciones.parquet
  (distancia en km sobre esfera de 6.371 km). Vecinos medios dentro de 2 km (con la propia sección): 46.6.
- **Exposición y resultado:** x_i = m^x_{mun(i)} + √0,6·z^x_i + √0,4·ξ^x_i;  y_i = β·x_i + h_{mun(i)}·(m^y_{mun(i)} + √0,6·z^y_i + √0,4·ξ^y_i), con efectos de municipio m ~ N(0,1) (absorbidos por el FE),
  ξ ruido idiosincrásico N(0,1), h_mun = exp(0,5·N(0,1)) (heterocedasticidad entre municipios), y z = campo gaussiano espacial con media móvil triangular de radio r sobre
  ruido blanco (correlación entre secciones positiva solo a menos de 2r; varianza unitaria). Los campos de x e y son independientes bajo el nulo.
- **Escenario principal:** r = 1,0 km (la correlación se anula a 2 km, el corte de Conley). **Sensibilidad (informativa):** r = 0,5 y 1,5 km (esta última deja correlación entre 2 y 3 km).
- **Nulo:** β = 0 (tamaño). **Alternativa:** β = 0.05 (DT de y por DT de x; Q3-b no tiene magnitud de referencia): sesgo, RMSE, cobertura y potencia.
- **Estimación:** MCO de y sobre x con efectos fijos de municipio (demedia intra-municipio). Inferencia: Conley con núcleo de Bartlett (triangular) a 2 km, normal.
  Si la varianza de Conley sale no positiva (el núcleo triangular no es semidefinido positivo en 2D) la réplica cuenta como no rechazo y se informa su frecuencia.
  Referencias (no candidatas): EE robustos HC1 y EE agrupados por municipio.
- **Alternativa nombrada en el punto 3:** ninguna (Conley a 2 km es la principal). Si no pasa → «NO APTO → diseño solo descriptivo».
- **Pocos clusters / T corto:** corte transversal; dependencia por distancia; sin dimensión temporal.
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97].

<!-- RESULTADOS -->
## Resultados (R = 4000 réplicas en el escenario principal; semilla 20261010, k = 32)

| escenario | inferencia | R | tamano_5pct | tamano_ic95 | cobertura_95 | potencia_beta | sesgo | rmse | var_no_positiva |
|---|---|---|---|---|---|---|---|---|---|
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | Conley 2 km | 4000 | 0.0435 | [0.0372, 0.0498] | 0.9565 | 0.6542 | 0.0000 | 0.0209 | 0.0000 |
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | HC1 (referencia) | 4000 | 0.2362 | [0.2231, 0.2494] | 0.7638 | 0.8890 | 0.0000 | 0.0209 | nan |
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | agrupado por municipio (referencia) | 4000 | 0.0695 | [0.0616, 0.0774] | 0.9305 | 0.7260 | 0.0000 | 0.0209 | nan |
| sens: radio 0,5 km | Conley 2 km | 2000 | 0.0120 | [0.0072, 0.0168] | 0.9880 | 0.8225 | -0.0001 | 0.0145 | 0.0000 |
| sens: radio 0,5 km | HC1 (referencia) | 2000 | 0.0925 | [0.0798, 0.1052] | 0.9075 | 0.9555 | -0.0001 | 0.0145 | nan |
| sens: radio 0,5 km | agrupado por municipio (referencia) | 2000 | 0.0480 | [0.0386, 0.0574] | 0.9520 | 0.9270 | -0.0001 | 0.0145 | nan |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | Conley 2 km | 2000 | 0.0680 | [0.057, 0.079] | 0.9320 | 0.5825 | -0.0002 | 0.0271 | 0.0000 |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | HC1 (referencia) | 2000 | 0.3460 | [0.3252, 0.3668] | 0.6540 | 0.8335 | -0.0002 | 0.0271 | nan |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | agrupado por municipio (referencia) | 2000 | 0.0630 | [0.0524, 0.0736] | 0.9370 | 0.5840 | -0.0002 | 0.0271 | nan |


**Veredicto: APTO (solo escenario principal; no robusto a la sensibilidad del rango espacial).**

**Advertencia.** El tamaño en el escenario principal (correlación espacial que se anula justo en el corte de 2 km) está en el intervalo, pero no se mantiene con campos de rango menor (tamaño conservador) ni mayor (sobre-rechazo): la calibración depende de que el corte coincida con el alcance de la correlación. Q3-b es C4 (correlación) y debe llevar esta advertencia.
