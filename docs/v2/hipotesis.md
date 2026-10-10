# Hipótesis v2 (pre-registro)

Redactado por el orquestador ANTES de ver ningún resultado de las ramas v2. Se congela con el tag git `prereg-v2`. Cualquier cambio posterior se anota en docs/v2/decisiones.md como desviación, con motivo.

## Reglas comunes
- Datos: data/processed/v2/train/* (vía `holdout.load_train`). Muestra sellada: 2024Q3-2026Q2 y las provincias 11 (Cádiz), 16 (Cuenca) y 45 (Toledo) en todos los periodos; en paneles anuales, 2025+ sellado y 2024 en embargo.
- Confirmatorias (H1-H7): una especificación principal fijada aquí; inferencia con EE cluster por provincia (+ wild cluster bootstrap) o HAC; corrección de Holm sobre la familia de las 7 confirmatorias. La evaluación en la muestra sellada se hace UNA vez, con `holdout.evaluate("Hk", ...)`, solo para las hipótesis que lo indican.
- Todo lo demás es EXPLORATORIO y se etiqueta así.
- Escala de evidencia: CAUSAL (identificación que pasa sus tests: pretendencias, F de primera etapa, placebos) > ASOCIACIÓN ROBUSTA (sobrevive a Holm, a submuestras y a la muestra sellada cuando aplica) > EXPLORATORIO > DESCRIPTIVO.

## Periodos candidatos (fijados ex ante)
| Periodo | Trimestres | Justificación previa |
|---|---|---|
| P0 boom final | 2002Q1-2007Q4 | expansión crediticia; solo donde hay datos |
| P1 ajuste | 2008Q1-2013Q4 | crisis financiera y caída de precios |
| P2 recuperación | 2014Q1-2019Q4 | quiebre de 2014 detectado en v1 (Chow); recuperación del empleo y del crédito |
| P3 COVID | 2020Q1-2021Q4 | pandemia, moratorias, tope de rentas en Cataluña (2020Q4-2022Q1) |
| P4 subida de tipos | 2022Q1-2024Q2 | BCE sube tipos desde julio de 2022; inflación; Ley 12/2023 |
| P5 sellado | 2024Q3-2026Q2 | zonas tensionadas en Cataluña (2024), bajada de tipos; solo evaluación |

## Hipótesis confirmatorias
| Id | Rama | Hipótesis | Signo esperado | Especificación principal | Muestra sellada |
|---|---|---|---|---|---|
| H1 | BA | El crecimiento del alquiler provincial (Δ4 ln IPC alquiler) se asocia positivamente con el crecimiento de la población de 20-34 años y de la población extranjera | + | Panel provincial trimestral 2008Q1-2024Q2, Δ4 ln alquiler sobre Δ4 ln pob 20-34, Δ4 ln pob extranjera, Δ4 ln ocupados, efectos fijos de provincia y de trimestre; EE cluster provincia | Sí: el modelo con estas variables reduce el RMSE frente al AR(4) de panel en 2024Q3-2026Q2 (DM-HLN) |
| H2 | BV | El crecimiento del precio de compra provincial (Δ4 ln valor tasado) se asocia positivamente con el crédito hipotecario nuevo y negativamente con el coste de uso | + crédito / − coste de uso | Panel provincial trimestral, Δ4 ln p_tasado sobre Δ4 ln hipotecas_importe (provincial), coste_uso_aprox (nacional, identificado por interacción con la exposición hipotecaria provincial 2005-2007), Δ4 ln ocupados, FE provincia y trimestre | Sí: mejora del RMSE frente al AR(4) de panel |
| H3 | BI | La inmigración (flujo instrumentado con shift-share por agrupación de países, cuotas 2002) eleva más el alquiler que el precio de compra | β_alquiler > 0 y β_alquiler > β_compra | Panel provincial anual 2009-2021 (flujos 2008-2021), Δ ln alquiler (IPC) y Δ ln p_tasado sobre flujo/población t−1; 2SLS con FE provincia y año; EE cluster provincia | No aplica (los flujos terminan en 2022) |
| H4 | BO | La elasticidad de las viviendas iniciadas al precio real es positiva y mayor en provincias con suelo relativamente más barato | + ; interacción − con ln p_suelo | Panel provincial anual 2005-2023, Δ ln iniciadas sobre Δ ln precio real (t−1) e interacción con ln p_suelo 2005-2007; FE provincia y año | No aplica |
| H5 | BP | El tope de rentas de Cataluña (Ley 11/2020, vigente 2020Q4-2022Q1) redujo el crecimiento del IPC de alquiler en las 4 provincias catalanas frente al contrafactual | − | Synthetic DiD (Arkhangelsky et al. 2021) con las 45 provincias no catalanas no selladas (52 − 4 catalanas − 3 selladas) como donantes, 2016Q1-2023Q4; control sintético y DiD como robustez; pretendencias obligatorias | No aplica (periodo en entrenamiento) |
| H6 | BP | La declaración de zonas tensionadas en Cataluña (2024) redujo el crecimiento del IPC de alquiler en las provincias catalanas frente al contrafactual | − | Misma estrategia que H5 con datos de entrenamiento hasta 2024Q2 para el ajuste; efecto medido en 2024Q3-2026Q2 | Sí: es la propia evaluación (una sola vez) |
| H7 | BM | Algún modelo con variables (panel o ML) supera al AR(4) y al ECM v1 fuera de muestra a 4 trimestres | mejora del RMSE | Validación en bloques con embargo en entrenamiento para elegir UN modelo; ese modelo se evalúa una vez en la muestra sellada (nacional y provincias selladas) con DM-HLN | Sí |

## Exploratorio (no confirmatorio)
- Contribuciones por periodo de cada familia de variables (BD), con contrafactuales e intervalos.
- Heterogeneidad (DML, causal forests) en BI; importancias (SHAP, ALE, permutación por familia) en BM.
- Viviendas turísticas y alquiler municipal (SERPAVI 2011-2024): ver docs/v2/decisiones.md (BT recortada).
- Panel UE: elasticidades comparadas de precio y alquiler.

## Signos esperados (resumen; detalle en docs/literatura.md, parte v2)
Alquiler: + población joven y extranjera, + empleo, + viviendas turísticas, − oferta (terminadas), − regulación (efecto de corto plazo discutido). Compra: + crédito, − coste de uso / tipos, + empleo, − oferta, + no residentes (sin datos provinciales).
