# Reconciliación H5 (V16 fase 6.3): producción V15 frente a réplica ciega

Veredicto: **ambas con errores**. Los de la producción afectan al contraste principal (combinación frente a AR(4)); el de la réplica solo al ECM v1 reconstruido. La ficha (preregistro + adenda + DV15-B-1 a B-4) está cumplida por la réplica en el AR(4), el paseo con deriva, el DFM, el BVAR, el LASSO, el ARDL y la regla de muestra. Ninguna cifra se ha elegido por resultado: los errores se determinan por la letra de la ficha y su efecto se mide después. Diagnósticos en (scripts d1-d6 del directorio temporal de la sesión) (no modifican src/v15 ni src/v16/replica).

## 1. Muestra de errores
- Último trimestre de entrenamiento del parquet p9: 2026T2 (p_tasado, compraventas_sa, hip_n, ocupados). Ambas terminan en el objetivo 2026T2 (último origen 2026T1).
- Producción: `resultado.json` rotula «2013Q3-2026Q1» pero son ORÍGENES (`orig = D.index[t]`, línea 236 y 285); los objetivos reales son 2013Q4-2026Q2. Primera fila completa de indicadores: 2007Q2.
- Línea 221: `t0 = ok[0] + MIN_FILAS + h` = 2007Q2 + 25 = origen 2013Q3. DV15-B-1 fija «primer origen común 2013T1 (≈ 54 errores)». Con 24 filas completas (2007Q2..2013Q1) el origen es 2013Q1 = `ok[0] + MIN_FILAS - 1`. Réplica: origen 2013T1, P = 53 (ficha ≈ 54). **La réplica cumple; la producción pierde 2 errores y no cumple la regla (ERROR, línea 221).**
- Corrección mínima: `t0 = ok[0] + MIN_FILAS - 1`. Corrección documental: rotular origen/objetivo por separado en líneas 261, 285, 307-310.

## 2. AR(4) (primera sospecha: confirmada en producción)
- ERROR de fuga, línea 66 de `f_ar`: `rows = [i for i in range(4, t + 1) if i + h <= len(dy) - 1 ...]` incluye la fila i = t, cuyo objetivo Yh[t] es el valor que se predice (el resto de modelos usan `i + h <= t` en `pred_directo`). Corrección: `i + h <= t`.
- Ventana: la línea 66 arranca en i = 4 (1995). La adenda (prevalece) y DV15-B-1 fijan 2003T1 para AR(4), ECM y RWD. Corrección: `range(INI_idx + 3, t + 1)`. La réplica (líneas 82-85) usa filas con objetivo >= 2003T1 y objetivo <= origen: cumple.
- Efecto medido (53 orígenes desde 2013Q1): ECM AR(4) de producción 9,35e-5; sin fuga y desde 2003 9,83e-5; réplica 9,95e-5 (la diferencia restante, 1 %, es una fila inicial). El RWD coincide al 8.º decimal (1,4838e-4). La fuga favorece al AR(4) en un 5 %: sesga contra la combinación.

## 3. Modelo a modelo
| Aspecto | Ficha | Producción | Réplica | Cumple |
|---|---|---|---|---|
| DFM, 2 factores, mensuales agregados | sí; estandarizado con datos hasta el origen | SVD con 11 indicadores (incluye euribor, renta, alquiler: no mensuales); sin fuga | SVD con 7 indicadores; sin fuga | ambas (elección) |
| BVAR 6 variables, Minnesota por verosimilitud marginal, σ² = AR(1) (DV15-B-3) | Δy, Δcv, Δhip n, tipo hipotecario, Δocupados, inflación | prior en variables estandarizadas con varianza σ_y²λ²/l²; usa Δ del tipo nominal | misma prior (equivalente); usa tipo REAL en nivel | ambas con desviación menor de variable (tipo): sin norma explícita |
| LASSO, λ con embargo 4 | sí | λ escalado por sd(y); 4 bloques; embargo 4 + h | λ absoluto 1e-5..1e-2; 3 pliegues; embargo 4 | ambas; validación fina en orígenes tempranos (20-23 filas, 12 regresores) |
| ARDL BIC ≤ 4 | cv + hip | igual | igual | ambas |
| ECM v1 (DV15-B-2) | DOLS ±2, IPC acumulado de p2 | desinflador `cumsum(log1p(inf/100)/4)` (liso, aproximado) | desinflador encadenado por trimestre (líneas 56-64) | producción; réplica con ERROR |
| RWD | media desde 2003T1 | igual | igual | ambas |
| Alineación temporal | X_t predice Δy_{t+1} | `Yh[t]=lnp[t+1]-lnp[t]`, filas `i+h<=t` | `Y[s+1]` con s < origen | ambas (sin desfase de un trimestre en los modelos) |
| Series de entrada | no especificado | compraventas_sa y ocupados_sa (STL de toda la muestra) | series brutas | ver abajo |

- Error de la réplica (líneas 56-64): el IPC acumulado se encadena `lp[i] = lp[i-4] + log1p(yoy)` por clase de trimestre, cada clase con base 0 distinta. Resultado: dientes de sierra persistentes (desviación típica de la diferencia con el índice liso ≈ 1 punto log) en log(valor tasado real) y en el ECT. Afecta solo al ECM v1 de la réplica (no a la combinación ni al AR(4)). Corrección mínima: `lp = (np.log1p(D.infl.fillna(0)/100)/4).cumsum()` (o cualquier índice común de base única).
- Riesgo de producción (líneas 30 y 38): `compraventas_sa` y `ocupados_sa` son STL de toda la muestra (metodo_dato `desestacionalizado_stl`), es decir, el valor del indicador en el origen depende de datos posteriores al origen. La ficha no fija la serie, así que no se califica de error de la ficha, pero contradice el espíritu «solo con datos hasta el origen» (DV15-B-2/B-3). La decisión (brutas, o SA recursiva con datos hasta el origen) corresponde al autor antes de re-ejecutar y no debe tomarse mirando el ECM.
- No hay uso de datos posteriores al origen en ninguna otra pieza (DFM, BVAR, LASSO, ARDL, ECM, RWD revisados línea a línea; hip_n idéntica: 41 provincias en 94 trimestres, filtro de completitud inactivo).

## 4. Descomposición de la discrepancia en la razón combinación/AR(4) (53 orígenes desde 2013Q1)
- Producción tal cual: 1,70 (P = 51).
- Código de producción con origen 2013Q1 y AR(4) corregido (sin fuga, desde 2003): 1,49.
- Además, compraventas y ocupados brutos: 1,21.
- Réplica: 1,15. El resto (0,06) es de indicadores/rezagos/tipo real, todos dentro de lo no fijado por la ficha.
- Por modelo (ECM ×1e-4, 2013Q1, producción→brutas): DFM 1,20→1,16; BVAR 1,37→1,20; LASSO 2,66→1,35; ARDL 1,23→1,19. El LASSO de producción es el más sensible a la serie SA.

## 5. Conclusión y siguiente paso
- No publicar la cifra de producción (1,70; p = 0,894) ni la réplica (1,15; p = 0,819) como definitivas. Correcciones obligatorias en producción: líneas 66 y 221; rotulado de orígenes. Corrección obligatoria en réplica: líneas 56-64 (solo ECM v1). Pendiente de decisión del autor: serie bruta o SA recursiva (puntos abiertos que la ficha no resuelve: tipo nominal/real en BVAR, conjunto exacto de indicadores).
- Aún con ambas correcciones la combinación queda por encima del AR(4) en las dos implementaciones (razón > 1), coherente con el nulo esperado en la ficha; es un hecho de entrenamiento (C4, descriptivo), no una conclusión sobre la hipótesis sellada, que no se ha tocado.
