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
- **Corrección K16 (2026-10-18).** La primera ejecución sumaba dos veces la diagonal del núcleo (scipy ya la guarda con distancia 0), lo que inflaba el EE; con ese error salió APTO (tamaño 0,0435, cobertura 0,9565). La réplica ciega de Q3-b lo detectó. Esta tabla es la del núcleo correcto; el campo W del proceso generador no se ha cambiado.
  Referencias (no candidatas): EE robustos HC1 y EE agrupados por municipio.
- **Alternativa nombrada en el punto 3:** ninguna (Conley a 2 km es la principal). Si no pasa → «NO APTO → diseño solo descriptivo».
- **Pocos clusters / T corto:** corte transversal; dependencia por distancia; sin dimensión temporal.
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97].

<!-- RESULTADOS -->
## Resultados (R = 4000 réplicas en el escenario principal; semilla 20261010, k = 32)

| escenario | inferencia | R | tamano_5pct | tamano_ic95 | cobertura_95 | potencia_beta | sesgo | rmse | var_no_positiva |
|---|---|---|---|---|---|---|---|---|---|
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | Conley 2 km | 4000 | 0.0963 | [0.0871, 0.1054] | 0.9038 | 0.7802 | 0.0000 | 0.0209 | 0.0000 |
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | HC1 (referencia) | 4000 | 0.2362 | [0.2231, 0.2494] | 0.7638 | 0.8890 | 0.0000 | 0.0209 | nan |
| principal: radio del campo 1,0 km (correlación nula más allá de 2 km) | agrupado por municipio (referencia) | 4000 | 0.0695 | [0.0616, 0.0774] | 0.9305 | 0.7260 | 0.0000 | 0.0209 | nan |
| sens: radio 0,5 km | Conley 2 km | 2000 | 0.0555 | [0.0455, 0.0655] | 0.9445 | 0.9360 | -0.0001 | 0.0145 | 0.0000 |
| sens: radio 0,5 km | HC1 (referencia) | 2000 | 0.0925 | [0.0798, 0.1052] | 0.9075 | 0.9555 | -0.0001 | 0.0145 | nan |
| sens: radio 0,5 km | agrupado por municipio (referencia) | 2000 | 0.0480 | [0.0386, 0.0574] | 0.9520 | 0.9270 | -0.0001 | 0.0145 | nan |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | Conley 2 km | 2000 | 0.1245 | [0.11, 0.139] | 0.8755 | 0.6770 | -0.0002 | 0.0271 | 0.0000 |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | HC1 (referencia) | 2000 | 0.3460 | [0.3252, 0.3668] | 0.6540 | 0.8335 | -0.0002 | 0.0271 | nan |
| sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte) | agrupado por municipio (referencia) | 2000 | 0.0630 | [0.0524, 0.0736] | 0.9370 | 0.5840 | -0.0002 | 0.0271 | nan |


**Veredicto: NO APTO → diseño solo descriptivo.**

Condición que falla: tamaño 0.0963 fuera de [0.04; 0.06]; cobertura 0.9038 fuera de [0.92; 0.97].
