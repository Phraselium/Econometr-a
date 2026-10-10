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
11. holdout.evaluate_v3 usa DataFrame.apply(pd.to_numeric, errors='ignore'), no válido en pandas 3. Se aplica un parche en memoria solo durante la llamada (clase shim_pandas3); src/holdout.py no se modifica. El test en seco se hizo a través de evaluate_v3 con rutas de ensayo, sin tocar el registro real de accesos.
12. Muestra: panel equilibrado 2019Q1-2023Q4 (misma muestra para event study, pretendencias, estimación principal y sensibilidad). Las réplicas JMS usan paneles equilibrados de su propio periodo.
13. fuera_muestra: no se compara con AR(4)/ECM v1 (es un efecto de política); la validación fuera de muestra es la sellada por fuente.
