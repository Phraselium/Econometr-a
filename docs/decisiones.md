# Registro de decisiones del orquestador

Modo autónomo (F2→F7). Ante ambigüedad se elige la opción más conservadora y se anota aquí.
Formato: fecha · fase · decisión · alternativa descartada · motivo.

## Generales
- 2026-10-09 · todas · La instrucción del usuario llegó truncada en «anota el problema como limitación en docs/lim». Se interpreta como `docs/limitaciones.md` y continuar con la fase siguiente. · — · lectura literal más probable.
- 2026-10-09 · todas · Orden de ejecución: F2 primero (ecuación nacional, de la que dependen F3 y F4); después F3, F4, F5 y F6 en paralelo, cada una con su puerta; F7 al final. · Todo secuencial · F3-F6 usan bases distintas y solo comparten la ecuación de F2.
- 2026-10-09 · todas · Utilidades econométricas comunes en `src/econ_utils.py` (HAC, diagnósticos, misma muestra, registro de búsqueda). Un registro de búsqueda por fase (`output/registro_busqueda_fN.csv`) para evitar escrituras concurrentes; F7 los consolida en `output/registro_busqueda.csv`.
- 2026-10-09 · todas · Errores estándar: HAC Newey-West con 4 retardos en series temporales; en panel, cluster por CCAA (17 clusters) + Driscoll-Kraay + wild cluster bootstrap cuando sea viable. · EE clásicos · autocorrelación y pocos clusters.
- 2026-10-09 · todas · Nivel de significación de referencia 5 %; se reportan siempre p-valores, no solo estrellas.

## F2 (nacional)
- Variable dependiente principal: `ln_ipv` NOMINAL (INE IPV base 2025), como en el punto de partida, con `ln_costes` (índice nominal) en el largo plazo. Robustez: precio real (`ln_ipv − ln_deflactor`) y precio de tasación (`ln_p_tasado`, muestra larga desde 2003). · Precio real como principal · mantener comparabilidad con el modelo de partida; la versión real se reporta igual.
- Estacionalidad: el IPV y la EPA no están desestacionalizados → dummies trimestrales en TODAS las ecuaciones de corto plazo. La réplica del punto de partida se presenta con y sin dummies. · Desestacionalizar con STL · evita introducir filtros de dos colas.
- Proxy de oferta principal: permisos de construcción (Eurostat `sts_cobp_q`) retardados 4 trimestres, como el punto de partida; viviendas iniciadas/terminadas (MIVAU) como alternativas en F4.
- Largo plazo: estimador principal DOLS (Stock-Watson, ±2 adelantos/retardos, HAC) por la endogeneidad de los regresores; Engle-Granger estático solo como réplica.
- Cointegración: se exige concordancia de al menos dos de {Engle-Granger, Johansen traza, ARDL bounds} para declarar cointegración; si discrepan, se declara «evidencia mixta» (opción conservadora).
- Búsqueda de especificaciones: conjunto de candidatos CERRADO y declarado antes de estimar; se registra cada modelo; inferencia con corrección (Holm/Bonferroni sobre el nº de modelos que contienen la variable) y análisis de cotas extremas (Leamer). La ecuación preferida se elige por BIC en la muestra común, no por R² ajustado (más conservador frente al sobreajuste); el R² ajustado se reporta.
- Fuera de muestra: ventana expansiva, predicción a 1 trimestre desde 2018Q1; referencia AR(4) con dummies; Diebold-Mariano con varianza HAC.
- Quiebres candidatos: 2014Q1, 2020Q1 (COVID), 2022Q3 (subida de tipos del BCE). Bai-Perron (ruptures) con máximo 3 quiebres y tramo mínimo de 12 trimestres.
- Inmigración en F2: solo como candidato en la búsqueda (stock `ln_pob_extranj`); el análisis específico (stock vs flujo, IV) es F3. Antes de 2021 la población es semestral interpolada → Δ1 tiene una MA mecánica; se contrasta con Δ4.
