# Desviaciones del pre-registro (C3)

1. Las fianzas trimestrales de Incasòl solo existen desde 2019Q1 (2017-2018 solo anual). La ventana previa es 2019Q1-2020Q3 (7 trimestres), el periodo de análisis 2019Q1-2023Q4 y la ventana de tratamiento 2020Q4-2022Q1 (o 2021Q3).
2. Placebo de fecha falsa 2018Q4: no es trimestral (no hay trimestres de 2018). Se hacen dos versiones: fecha falsa 2019Q4 con post 2019Q4-2020Q2 (se excluye 2020Q3 por la anticipación que documentan JMS) y versión anual (2019 frente a 2018, panel anual 2016-2019).
3. Rambachan-Roth: no hay paquete instalado. Se usan la cota de magnitudes relativas con M̄=1 y la de tendencia lineal (suavidad con M=0) con IC por bootstrap de unidades (999). No es el IC condicional/híbrido de Rambachan-Roth.
4. Control del multiverso: hipotesis.md dice «no sujetos con más de 20.000 habitantes como en JMS 2023». La ficha de literatura (A3) describe sus controles como mercado tenso por debajo del umbral. Se corren los dos más «todos los no sujetos» (principal). «Mercado tenso» se aproxima con el crecimiento anual de la renta de fianzas 2014-2019 ≥ 4,15 %.
5. Población: Censo 2021 (suma de grandes grupos de edad por municipio), fija en el tiempo. No hay padrón anual en los datos.
6. Barcelona se excluye en la especificación principal (como JMS y la potencia); su inclusión es una decisión del multiverso.
7. dCDH: no hay paquete. Se usa DID_M (efecto en el momento del cambio, 2020Q4 frente a 2020Q3), que con un único momento de tratamiento coincide con ATT(g,g) de CS.
8. Contratos: ln del nº de fianzas (sin denominador de población; la población fija se absorbe en los efectos fijos de municipio). Sin controles (paro, ERTO) que sí usan JMS.
9. El resultado de renta es la media de las medias de banda ponderada por nº de contratos; las bandas cambian entre años.
10. Potencia de la validación SERPAVI: la estructura (municipios con los 4 años) viene de SERPAVI y la varianza es la de las fianzas anuales (aproximación; SERPAVI es un stock IRPF y su varianza real no se miró).
11. Parche de pandas 3 (retirado). La primera versión aplicó en memoria un parche a `DataFrame.apply(pd.to_numeric, errors='ignore')` y un test en seco con `holdout.LOG` redirigido. La versión actual de `holdout.py` (c5e8aae) ya no contiene esa llamada: el parche era código muerto y se eliminó. `holdout.py` sí fue modificado por c5e8aae, después del ancla 204c073. El test en seco ahora llama a `fn` con un panel sintético, sin tocar `holdout`. Ninguna estimación cambia.
12. Muestra: panel equilibrado 2019Q1-2023Q4 (misma muestra para event study, pretendencias, estimación principal y sensibilidad). Las réplicas JMS usan paneles equilibrados de su propio periodo.
14. Validación por fuente: DiD 2x2 con pre 2018-2019 y post 2021-2022; descarta 2020 y 2023 (el pre-registro dice SERPAVI 2018-2023).
15. Umbrales de placebo fijados después del pre-registro: cualquier placebo con p < 0,05 (t o aleatorización) cuenta como fallo de b.
16. Criterio c (revisión de la oleada 2): RV_q=1 frente al mayor R² parcial entre R²_y y R²_d, y |δ| de Oster > 1. H3-3a depende de tomar la pendiente previa como covariable observada: sin ella RV_q=1 supera al resto (la capa no cambia porque falla a). Criterio b de H3-3: parcial, sin placebo de resultado. Se informa el M̄ de ruptura de Rambachan-Roth.
13. fuera_muestra: no se compara con AR(4)/ECM v1 (es un efecto de política); la validación fuera de muestra es la sellada por fuente.
