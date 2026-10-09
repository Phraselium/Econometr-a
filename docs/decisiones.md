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
- Búsqueda de especificaciones: conjunto de candidatos CERRADO y declarado antes de estimar; se registra cada modelo. [Revisado por instrucción del usuario] Criterio principal: R² ajustado en la muestra común, corregido por la búsqueda con Bonferroni y con bootstrap por bloques de la selección completa (bloque 8, B=999); se reportan los ganadores por AIC y BIC y las cotas extremas de Leamer.
- Fuera de muestra: ventana expansiva desde 2018Q1, re-estimando también el largo plazo con datos hasta t−1; referencias: media histórica, paseo aleatorio con deriva y AR(4); Diebold-Mariano HAC.
- Dummies adicionales (instrucción del usuario): `quiebre_epa_2021` y escalón de tipos desde 2022Q3; versión pre-COVID (hasta 2019Q4: «termina en 2020» se interpreta excluyendo el shock de 2020 — opción conservadora); Bai-Perron sobre el ECM.
- Orden de integración decidido también con las series largas de precio (valor tasado y BdE desde 1995).
- Quiebres candidatos: 2014Q1, 2020Q1 (COVID), 2022Q3 (subida de tipos del BCE). Bai-Perron (ruptures) con máximo 3 quiebres y tramo mínimo de 12 trimestres.
- Inmigración en F2: solo como candidato en la búsqueda (stock `ln_pob_extranj`); el análisis específico (stock vs flujo, IV) es F3. Antes de 2021 la población es semestral interpolada → Δ1 tiene una MA mecánica; se contrasta con Δ4.

## F3 (inmigración) — fijado antes de estimar
- Stock vs flujo. Stock: `ln_pob_extranj` trimestral (usar Δ4 por la MA mecánica pre-2021). Flujo: `inmig_anual_eurostat` como tasa sobre población total del año anterior (anual, 1998-2024, dummy `quiebre_emcr_2021`). El flujo trimestral no existe (ver limitaciones) → la comparación stock/flujo se hace en frecuencia anual, y en trimestral solo stock.
- Dinámica 0-8 trimestres: proyecciones locales (Jordà 2005) de Δ_h ln IPV (y del IPC alquiler) sobre Δ4 ln pob_extranj, con 4 retardos de Δln IPV, Δln ocupados y Δtipo como controles, HAC con h+4 retardos. Se interpreta como asociación dinámica (sin identificación).
- Identificación: IV shift-share (Card 2001) en `panel_ccaa_a` (17 CCAA, anual). Endógena: Δ población extranjera / población total del año anterior. Instrumento: Σ_g s_{c,g,2002} · crecimiento nacional del grupo g excluyendo la propia CCAA (leave-one-out). Año base 2002 (primer año disponible; anterior a la muestra de estimación, que empieza en 2003/2008 según la variable de resultado). Resultados: Δln IPV CCAA (2008+), Δln valor tasado (2003+), Δln SERPAVI (2012+, alquiler). Efectos fijos de año y de CCAA (equivalentes a tendencias específicas en niveles) — instrucción del usuario: FE + tendencias. Sobreidentificación: instrumentos separados por grupo de países (Hansen J). Controles: Δln ocupados (como robustez, porque puede ser un mal control). Inferencia: cluster por CCAA + wild cluster bootstrap (Webb, 9.999 réplicas, semilla 20261009). Diagnósticos de shift-share: F de primera etapa robusto a cluster, pesos de Rotemberg (Goldsmith-Pinkham, Sorkin y Swift 2020), prueba de pre-tendencias (resultado 2003-2007 sobre instrumento posterior). Si F < 10 o los diagnósticos fallan → se informa como asociación, no causal.
- Desagregación por nacionalidad: grupos de países de 77019 (coherentes en el quiebre UE28/UE27) en el panel anual; a nivel nacional, solo descriptivo (colinealidad).
- Canal comprador: compras de vivienda por extranjeros (MIVAU por CCAA, Notariado CGN) como resultado separado del canal población.

## F4 (oferta) — fijado antes de estimar
- Elasticidad de la oferta: ecuación de construcción nueva ln(iniciadas MIVAU) [principal], ln(permisos) y ln(terminadas) [alternativas] sobre ln(precio real) retardado, ln(costes reales) y tipo real; largo plazo por DOLS y corto plazo ECM; IV del precio con desplazadores de demanda (ln ocupados, ln pob_extranj) como robustez de endogeneidad (F de primera etapa).
- Comparabilidad con el Banco de España: el 0,45 del Informe Anual 2025 procede de Caldera y Johansson (2013) / Cavalleri et al. (2019) y es una elasticidad de la inversión residencial (flujo) a precios reales de largo plazo; se compara con nuestra elasticidad de iniciadas, advirtiendo la diferencia de concepto. Esas dos referencias figuran como NO VERIFICADAS.
- Déficit 2021-2025: déficit = Σ (Δhogares − viviendas terminadas) (equivale al BdE: terminadas − creación neta de hogares, con signo cambiado; se reporta como número positivo cuando faltan viviendas). Principal: hogares EPA con corrección del cambio de 2021 (se excluye el salto de nivel de 2021T1, sustituyendo su Δ por la media de Δ de los 4 trimestres adyacentes; alternativa: Δ de 2021T1 = 0); se replica el cálculo del BdE (~750.000; 700.000 en el IEF otoño 2025) y las diferencias se documentan sin ajustarlas. Variantes: (a) hogares ECP 60131 (coherente con la definición del BdE) − terminadas MIVAU libres; (b) hogares EPA excluyendo el salto de nivel de 2021T1; (c) con parque MIVAU anual (Δparque vs Δhogares). Se informa como flujo acumulado de desequilibrio desde 2021, sin suponer un equilibrio inicial; un «déficit» en niveles requiere ese supuesto y solo se da como escenario.
- Advertencia: las terminadas MIVAU son vivienda LIBRE; el BdE cita 92.000 terminadas en 2025 → contrastar nivel y documentar la diferencia.

## F5 (panel CCAA) — fijado antes de estimar
- Especificación principal en `panel_ccaa_a` (anual, 17 CCAA): Δln IPV_ct sobre Δln ocupados, Δ(pob extranjera/pob total), Δln pob española y terminadas por 1.000 habitantes retardadas; efectos fijos de CCAA y año (el tipo de interés queda absorbido). Robustez: tendencias específicas por CCAA; panel trimestral con Δ4.
- Estimadores: FE (linearmodels PanelOLS) con EE cluster por CCAA, Driscoll-Kraay y wild cluster bootstrap; CCE-MG y CCE-pooled (Pesaran 2006) implementados con promedios transversales; test CD de Pesaran para dependencia transversal.
- Heterogeneidad: interacciones con C. Valenciana, Madrid, Cataluña, Baleares, Canarias, Andalucía y coeficientes CCE por CCAA (con la advertencia de N_t pequeño por unidad).

## F6 (València) — fijado antes de estimar
- Series municipales con N ≥ 40 trimestres (valor tasado, compraventas MIVAU): comparación con C. Valenciana y España (tasas, diferenciales, beta de València frente a España con HAC). Series con N < 40 (padrón por nacionalidad, SERPAVI, VUT, Notariado municipal): análisis DESCRIPTIVO, dicho explícitamente; sin inferencia causal.
- VUT: serie GVA 2010-2024 sin encadenar con la lista vigente de 2026 (renumeración y purga).

## Hallazgos durante F2
- 2026-10-09 · F2 · `p_bde` (BdE be2507, precio de la vivienda libre) es idéntica a `p_tasado` (MIVAU valor tasado) en los 126 trimestres (|dif| máx 2e-13): el BdE republica la serie del Ministerio. Solo hay UNA serie larga de precio desde 1995; las robusteces con ambas no son independientes. Se usa `p_tasado` y se cita así.
- 2026-10-09 · F2 · Con ventana expansiva, el paseo aleatorio con deriva coincide con la media histórica; se usa deriva de los últimos 20 trimestres para diferenciarlos (documentado en output/f2).
- 2026-10-09 · F3-F6 · Se lanzan en paralelo a la puerta de F2. No modifican `src/econ_utils.py` (API congelada; F2 solo puede añadir funciones compatibles).
- 2026-10-09 · F6 · SERPAVI por distritos de València no está en data/processed (solo en raw). Se añadirá su exportación a `valencia.csv` en build_dataset.py DESPUÉS de que terminen F3-F5 (que leen data/processed y `make clean` reescribe todos los ficheros), dentro de la puerta de F6. No altera F1 (solo añade filas a valencia.csv).
- 2026-10-09 · F6 · MIVAU no publica compraventas de extranjeros por municipio: la cuota de compradores extranjeros solo existe para CV y España (y Notariado municipal 'Total general' 2021-2025, robustez).
- 2026-10-09 · F3 · `trans_extranjeros` (MIVAU 340101i0) = compraventas de vivienda por extranjeros RESIDENTES (no incluye no residentes, que están en `mivau_transacciones_residencia.csv`). Coherente entre panel y nacional (suma CCAA = nacional ±0,1 %). Salto 2008→2009 (18.180 → 26.784) con compraventas totales cayendo: posible cambio de cobertura; se trata como canal comprador de ROBUSTEZ y el coeficiente 2SLS de −42 no se interpreta sin revisión.
- 2026-10-09 · infraestructura · `econ_utils.Registry` reescrito: acumula filas en memoria y escribe el CSV completo de forma atómica (temporal + os.replace) al terminar. Causa: ejecuciones concurrentes (revisores y agentes) intercalaban filas en modo append → registros f2/f3 corruptos (revision_f3.md). `make models` y `make clean` se serializan con `flock`. API sin cambios.
- 2026-10-09 · F2 · Tras corregir el ARDL bounds: cointegración 1/3 con precio NOMINAL (evidencia mixta) y 3/3 con precio REAL. Decisión: se mantiene lo pre-registrado (nominal como especificación de réplica) pero la ecuación de largo plazo que se interpreta en F7 es la REAL, porque es la única con cointegración respaldada por los tres contrastes. Es una desviación del pre-registro motivada por los contrastes, no por el ajuste; se reportan ambas.
- 2026-10-09 · F6 · APROBADA (re-revisión). Notas para F7: citar la cuota de extranjeros CV>España solo como hecho descriptivo (77/77 trimestres), no con el p≈4e-20; EE de la beta por tramos (24-26 trimestres) solo aproximados.

## Revisión F3 (iteración 1)
- 2026-10-09 · F3 · `ipc_alquiler` (IPC alquiler por CCAA) se añadió como resultado DESPUÉS del diseño prefijado (que solo fijaba SERPAVI para alquiler); no es resultado principal prefijado y no sobrevive a Holm. · — · transparencia sobre búsqueda.
- 2026-10-09 · F3 · Pretendencia 1996-2001 no computable en el script: `data/processed` no tiene precios por CCAA antes de 2002 (solo en data/raw). Se reporta la cifra de la revisión (raw) como externa y se deja pendiente su incorporación a processed. · Leer raw desde el script · regla de leer solo de processed.
2026-10-09 · F1 (corrección) · Parser MIVAU: Extremadura (1) mal clasificada como provincia; corregido; solo afecta a terminadas/visados por CCAA.

## F7 (síntesis) — niveles de evidencia fijados por el orquestador a partir de las fases aprobadas
- P1: asociación. Ecuación final = LR real (DOLS) + ECM real preferido por R² aj, con p Bonferroni y bootstrap de la selección; la nominal como réplica. Cointegración: real 3/3, nominal 1/3 (se reportan ambos).
- P2: asociación (IV no supera bootstrap, pretendencias y Holm). Asociación positiva con alquiler; nula/no robusta con precio de compra.
- P3: déficit = aritmética contable (descriptivo, fuentes oficiales); elasticidad de oferta = asociación débil/descriptiva; 0,45 del BdE NO VERIFICADA y no rechazada en Δ4.
- P4: asociación; «no se detecta heterogeneidad» (no homogeneidad). València: comparativa con HAC para valor tasado (N≥40); el resto descriptivo.
- P5: quiebres detectados (2014 Chow; Bai-Perron 2011Q4, 2019Q2, 2023Q2 en niveles); 2020 y 2022 no rechazados por Chow en el ECM real; corrección de error inestable → el modelo no es estable.
- Las cifras del informe se leen de output/ por src/report.py (ninguna escrita a mano en el texto).
