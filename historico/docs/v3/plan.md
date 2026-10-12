# Plan v3 — qué se puede afirmar con seguridad sobre el problema de la vivienda y sus soluciones

V1 y V2 están cerradas y no se rehacen (output/informe.md, output/v2/informe_v2.md). La v3 reutiliza datos, `src/econ_utils.py`, `src/holdout.py`, subagentes y Makefile.

## Capas (organizan todo el trabajo y el informe)
| Capa | Qué entra | Prueba exigida |
|---|---|---|
| C1 HECHOS | medidas descriptivas o contables | ≥2 fuentes independientes y una incertidumbre de medida (rango entre fuentes o error muestral) |
| C2 COTAS | identificación parcial (Manski), estadísticos suficientes | supuestos débiles y explícitos; la cota se da con el supuesto extremo que la hace máxima o mínima |
| C3 EFECTOS | efectos causales | diseño con pretendencias (Rambachan-Roth), placebos de tratamiento y de resultado, sensibilidad (Oster, Cinelli-Hazlett), validación sellada y potencia suficiente |
| C4 EXPLORATORIO | todo lo demás | etiqueta explícita |

«Afirmable con seguridad» = C1, C2 y C3 robusto (≥2 diseños con supuestos distintos que coinciden). Ningún resultado cambia de capa por presentación.

## Oleadas y puertas
1. **Oleada 1**: datos nuevos (D1 INE: censo 2021, VUT por sección, Atlas de renta; D2: fianzas, SERPAVI por sección, EFF publicada, ECV/EPA emancipación, SIU, eventos). Literatura (verificación solo de referencias nuevas, tabla de magnitudes, protocolo de replicación). P-A hechos (C1). P-B cotas (C2). Potencia de P-C. Replicación de García-López et al. (2020) en Barcelona. Solicitudes de transparencia. **Puerta go/no-go de P-C** + reviewer (oleada 1).
2. **Oleada 2**: P-C solo para diseños con potencia suficiente (efecto mínimo detectable ≤ efecto económicamente relevante declarado ex ante), pre-registro `prereg-v3` antes de estimar, sellado espacial; extensión de las tres replicaciones. Reviewer (oleada 2).
3. **Oleada 3**: P-D simulaciones con rangos de elasticidades y criterio de dominancia o mínimo arrepentimiento; verificador (`make verificador`); entregables. P-E solo si sobra presupuesto. Reviewer (oleada 3). Cierre: `make all` sin red ×2 en clon limpio.

## Presupuesto de subagentes
3,5 M tokens en total; ≤0,35 M por diseño; smoke test ≤0,15 M; al 80 % (2,8 M) se pasa a cerrar. Máx. 3 subagentes en paralelo.

## Entregables
output/v3/lo_que_sabemos.md · output/v3/articulo.md · output/v3/informe_politica.md (módulo València) · output/v3/verificador/ (`make verificador`) · docs/v3/solicitudes_transparencia.md.
