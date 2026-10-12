# Ensayo de `make evaluate_v7` con datos futuros simulados (V7.1-S4)

**Resultado del ensayo: SUPERADO.** Se recorrió el camino real de src/v7/evaluate_v7.py, no el modo `--simular`, en un directorio temporal. Los datos 2026T3-2027T2 son simulados. No se descargó ningún dato real, no se escribió en data/raw y el registro real de accesos (docs/v7/evaluate_v7_accesos.md) quedó intacto (sí).

| Comprobación | Esperado | Obtenido |
|---|---|---|
| Formatos: periodos nuevos detectados por el lector real | 2026Q3-2027Q2 | 2026Q3, 2026Q4, 2027Q1, 2027Q2 |
| CCAA con dato nuevo por mercado | 17 y 17 | {'alquiler': 17, 'compra': 17} |
| sha256 de la congelación | 93795a94… | 93795a94… (coincide con docs/v7/notas_release.md) |
| Apertura registrada antes de evaluar | sí | sí |
| Evaluación (código de salida) | 0 | 0 |
| Segunda ejecución | se niega (3) | 3 |
| sha256 anotado distinto | se niega (2), sin registro | 2, registro no creado |
| Sin periodos nuevos | sale sin registrar | código 0, registro no creado |

## Métricas del ensayo (datos simulados; solo comprueban que el cálculo funciona)

Periodos objetivo: 2026Q3, 2026Q4, 2027Q1, 2027Q2; CCAA: 17. RMSE ×100 a h = 1 por modelo congelado:

| modelo         |   alquiler |   compra |
|:---------------|-----------:|---------:|
| ar4            |      0.342 |    1.615 |
| ar_factor      |      0.296 |    1.212 |
| ecm_v1         |      0.379 |    1.195 |
| gbm            |      0.284 |    1.661 |
| mejor_regional |      0.306 |    1.705 |
| mixto          |      0.333 |    1.476 |
| persistencia   |      0.866 |    2.02  |
| pmg            |      0.453 |    1.416 |
| ult_crec_nac   |      0.232 |    2.341 |

Estas cifras **no** se publican ni entran en cifras_clave: miden el error frente a un paseo aleatorio simulado.
