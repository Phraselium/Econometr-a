# V16 · Desviaciones del plan y del pre-registro

Toda desviación se anota aquí **antes** de ver el resultado afectado, con su motivo. Se publica en metodologia/desviaciones_v16.md con `make publicacion`.

## D1. No hay preguntas confirmatorias nuevas (fase 4.1 del plan)
- **Plan.** El plan pedía «preguntas confirmatorias NUEVAS» y, a la vez, descartar o reformular con argumentos lo que no tuviera potencia o identificación.
- **Resultado de la potencia** (output/v16/potencia, con tratamientos placebo):
  - ningún subdiseño reúne a la vez un MDE por debajo de la magnitud de diseño creíble, una inferencia calibrada y una identificación adecuada sin repetir H1-H5 de V15;
  - los dos revisores (revisor-preregistro y abogado-del-diablo) aceptaron esta decisión.
- **Decisión.** V16 es exploratorio y C4 como máximo (preregistro_v16.md, sección 1, y adenda, punto 1). H1-H5 de V15 siguen siendo la única familia confirmatoria.
- **Fecha:** 2026-10-17, antes de estimar.

## D2. Fase 6, grupo B (Q3, Q4, Q6): operacionalización forzada por los datos de entrenamiento
Anotadas el 2026-10-17 **antes de estimar** Q3-c, Q3-b, Q4a, Q4b, Q6-v y Q6-p. Ninguna sostiene una capa ni es principal por sí sola: son la forma en que se ejecuta la especificación principal con lo que hay en disco.
- **Q3-c1/c2, ventana.** El padrón por nacionalidad termina en 2022, así que el shift-share por origen no existe para 2023-2024. Ventana principal 2011-2022 (la adenda decía 2011-2024). Orígenes: los 28 países individuales del padrón; los agregados («De Africa», «Europa (sin España)», etc.) no se usan como orígenes.
- **Q3-c1/c2, exposición.** Población extranjera predicha en puntos de la población de 2003: x_pt = 100 · Σ_o F_{po,2003} · (N_{o,t,-p} / N_{o,2003,-p}) / pob_p,2003, con N_{o,t,-p} = stock nacional del origen o sin la provincia p (suma de las provincias de entrenamiento). Efectos fijos de provincia y año. Sin errores AKM ni AKM0 (NO APTOS): solo estimación puntual.
- **Q3-c, exclusión de grandes ciudades.** A escala provincial se excluyen las provincias de Barcelona (08), València (46), Sevilla (41) y Málaga (29). No hay islas no selladas en entrenamiento (Baleares y Canarias son v6).
- **Q3-c, desbordamientos a 15 km.** No aplica a escala provincial (unidades de cientos de km); se declara no ejecutada.
- **Q3-b, tipología.** SERPAVI por sección con tipología VC (vivienda colectiva, la mayoritaria); VU solo como variante puntual. Cuota de extranjeros 2022 = total_extranjera / total de ine_padron_seccion_poblacion_personas, estandarizada con la DT entre secciones. Se descartan los municipios con una sola sección (su efecto fijo las absorbe), como en el Monte Carlo.
- **Q3-b, BLP/GATES.** Forma lineal con interacciones (exposición × moderador centrado y estandarizado) y GATES por cuartiles de un índice de heterogeneidad ajustado con validación cruzada en dos mitades por municipio. Moderadores de la adenda (punto 13): renta ADRH (sección, último año disponible), población, cuota de extranjeros, % vivienda turística INE-VUT (primera instantánea 2021) y obra nueva per cápita (municipal, 2018-2021 sobre población de 2021). Herramienta NO APTA: solo estimación puntual descriptiva.
- **Q4a.** El Catastro da la obra neta como diferencia anual de unidades urbanas (puede ser ≤ 0). El logaritmo se toma sobre obra > 0; variante con asinh en robustez. Efectos fijos de provincia y de año; el % de Red Natura (estandarizado) no varía en el tiempo.
- **Q4b.** El «choque de Q3» se construye a escala municipal con las cuotas del padrón municipal de 2003 y el crecimiento nacional de cada origen sin la provincia; existe hasta 2022, así que la ventana es 2018-2022 (la adenda decía 2018-2024).
- **Q6-v/Q6-p, datos.** Las compraventas provinciales de entrenamiento son el total de vivienda (INE ETDP 6150), sin desglose usada/nueva: se usa el total y se dice. Quedan fuera Ceuta y Melilla (sin tipo autonómico) y País Vasco (régimen foral, sin tipo general comparable); Navarra ya es v6. Cantabria no tiene valor tasado (38 provincias en Q6-p). El tipo es el «tipo general» (el mínimo de la escala cuando hay escala), en vigor el año del cambio (fecha de efecto), según output/v16/f1/intervenciones.csv.
- **Q6, panel anual.** El año de cada cambio es el de la fecha de efecto; el año previo a cada cambio queda fuera como anticipación (observaciones de la CCAA en t-1 se excluyen del contraste y del grupo de control). Estimador: Wald-DID de de Chaisemartin-D'Haultfœuille con dosis continua (Σ switchers (ΔY − media ΔY de los estables del año) / Σ Δ tipo). Pretendencia: coeficiente placebo con ΔY retardado un año.
- **Honest DiD.** No figura en output/v16/montecarlo/veredictos.csv (no validado): no se usa; las pretendencias se publican como placebo puntual.
- **Multiverso.** Las dimensiones operativas de cada variante (orígenes, normalización, año base, efectos temporales; ventana; fecha) están en cada src/v16/q*.py y en su registro.csv; ninguna se elige por su resultado.

## D3. Precisiones de implementación de Q1, Q2, Q7 y Q8 (fase 6, grupo A)
Anotadas el 2026-10-17 **antes** de ejecutar ninguna estimación de estas preguntas. Son precisiones donde la adenda no fija un detalle operativo; ninguna cambia un diseño, una ventana ni una inferencia.
- **Q1c (Callaway-Sant'Anna).**
  - Cohorte g = primer trimestre con alguna zona tensionada vigente (base_regulacion, `zt_vigente`) en la provincia.
  - Grupo de comparación: provincias nunca tratadas. Periodo base: g−1. ATT global = media de los ATT(g,t) con t ≥ g, ponderada por el número de provincias de la cohorte.
  - Estimación puntual sin regresores (NO APTO: sin p-valor ni IC).
  - Incluye Cataluña (la adenda define el tratamiento como «alguna zona vigente»): solapa con H1/H2 y se declara.
- **Q1a.** El resultado es de la muestra sellada y no se evalúa. Se publica solo un recuento descriptivo de elegibilidad en el entrenamiento (municipios con crecimiento SERPAVI 2018-2023 por encima de IPC + 3 p.p. frente a zona vigente): sin RD ni efecto.
- **Q1b.** Se comprueba si existe periodo posterior al tratamiento en el entrenamiento; si no, «no estimable en el entrenamiento». No se inventa otra ventana.
- **Q2a (forma reducida).**
  - Exposición = log del % de viviendas turísticas INE de agosto de 2020 por provincia, estandarizada.
  - Resultado = log del IPC de alquiler provincial, media anual de los trimestres; pre 2017-2019 y post 2022-2025 (2020-2021 fuera); efectos fijos de provincia y año; cola de la regresión sin errores típicos.
  - El multiverso de 32 especificaciones del pre-registro (sección 7) era del shift-share retirado (orígenes, normalizaciones); **no se ejecuta**. Se ejecutan la principal, la exclusión de grandes ciudades (punto 14) y, como diagnósticos, un placebo de fecha y un estudio de eventos. Q2b se limita a robustez.
- **Q2c.**
  - Exposición = % de viviendas turísticas INE municipal, media anual 2021-2024; principal: log estandarizado (municipio-años con 0 % fuera); variante: nivel estandarizado.
  - Resultado = log del índice IPVA-TAM municipal (principal) y su variación anual (variante).
  - Efectos fijos de municipio y año. La agrupación por provincia no cambia la estimación puntual y no se calcula (inferencia NO APTA).
- **Q2b (solo robustez).**
  - Dosis = altas acumuladas de OpenRTA (Andalucía) por 1.000 viviendas, en nivel o en logaritmo.
  - Resultados = log SERPAVI €/m² municipal y log IPVA-TAM municipal. Ventanas 2016-2024 y 2019-2024. Sin inferencia.
- **Q7a.**
  - Corte entre 35 y 36 años de la edad del sustentador (ECV). El Plan 2018-2021 exigía «menos de 35 años» (RD 106/2018, programa de ayuda a los jóvenes); el Bono Alquiler Joven, «hasta 35 años». Se usa un único corte y se declara.
  - Anchos de 3, 5 (principal, 30-40 años) y 7 años; resultados = log del alquiler mensual (HH060) y alquiler anual / renta del hogar (HY020).
  - Pesos DB090, lineal local con pendientes distintas a cada lado y periodo. Sin intervalo, así que no se usa Kolesár-Rothe.
- **Q8.** Compras de no residentes del MIVAU (`mivau_transacciones_residencia`): suma de las 41 provincias de entrenamiento, no el total nacional (que incluye las CCAA selladas de v6). Solo descriptiva.
- **BLP/GATES (adenda, punto 13).**
  - Versión descriptiva y sin p-valor (NO APTA): BLP lineal con los cinco moderadores estandarizados y GATES por cuartiles de un CATE proxy, con partición muestral repetida 50 veces (mediana).
  - Se aplica a Q2a (provincial) y Q2c (municipal). Para Q1 no es estimable: Q1b no tiene periodo posterior, y Q1c tiene 8 provincias tratadas frente a 5 moderadores.

## D4. Fase 6, grupo C (Q5, Q9, Q10 y rejilla)
Anotadas el 2026-10-17 **antes** de ejecutar ninguna estimación de Q5, Q9, Q10 ni de la rejilla. Son precisiones operativas donde la adenda no fija el detalle, o límites de los datos de entrenamiento. Ninguna cambia un diseño; ninguna se elige por su resultado. Todo es C4 y «pendiente de evaluación sellada».
- **Herramientas.** Q5 (LP con Newey-West de b fija), Q9-c (CS-ARDL), CIPS, Q10 (DM-HLN, Clark-West; GW y MCS no figuran en veredictos.csv) y la rejilla (TWFE municipio y provincia) son NO APTAS: solo estimación puntual, sin p-valor ni IC (en `p_valores_para_BY`, p = null). Solo Q9-g (GSADF con bootstrap salvaje) es APTA: conservadora si el proceso es homocedástico (tamaño 0,017).
- **Q5.**
  - Choque: sorpresa de política monetaria de Jarociński-Karadi (`bce_jk_mp_median_m` principal; `bce_jk_mp_pm_m` «poor man's» como segundo choque), suma mensual dentro del trimestre y estandarizada (DT de la muestra de cada ventana). La serie termina en 2025-10 (2025T4): la ventana efectiva acaba ahí aunque la adenda diga 2026T2.
  - LP: y(t+h) − y(t−1) (log × 100, % acumulado) sobre el choque de t, 4 rezagos del choque y 4 rezagos de Δy (como en el proceso generador de la fase 5). Horizontes 1, 4 (principal), 8 y 12. «2 rezagos» del multiverso: 4 (principal) y 2. Los 4 resultados: valor tasado nacional, IPV nacional, compraventas nacionales y IPC de alquiler.
  - Controles negativos: población total nacional (la población de 65 años o más no está en el entrenamiento: se usa pob_total, trimestral) e inflación general yoy (el IPC de servicios no ligados a la vivienda no está en disco). Es una sustitución declarada.
  - F efectivo de Montiel Olea-Pflueger: no aplica a una LP sobre un choque externo único; se publica el F robusto (HC) de la primera etapa de Δ tipo hipotecario sobre el choque (descriptivo, sin umbral de capa).
  - Bai-Perron: se publica un sup-F de ruptura única en el coeficiente del choque (Andrews, recorte 15 %), solo descriptivo (sin valor crítico validado).
- **Q9.**
  - Ratio de Q9-g: ln(valor tasado provincial) − ln(IPC de alquiler provincial), trimestral 2002T1-2026T2, 38 provincias con ambas series; factor común = primera componente principal de las series estandarizadas (signo fijado para que correlacione positivamente con la media). GSADF con constante y sin rezagos, ventana mínima de Phillips-Shi-Yu, bootstrap salvaje de Harvey et al. con B = 499 (el de la fase 5), valor crítico del 95 %. El «índice de stock de contratos» de la adenda no existe en entrenamiento: se usa el IPC de alquiler y se declara.
  - Alternativa SERPAVI: ratio valor tasado anual / SERPAVI €/m² provincial en nivel (T = 14, sin potencia; se publica y se dice).
  - GSADF por provincia: 38 provincias × 2 ratios (la segunda es la alternativa SERPAVI, porque la renta ADRH solo tiene 3 años en entrenamiento). Descriptivo: estadístico y valor crítico bootstrap de cada provincia, sin p-valor (no validada por provincia).
  - Q9-c (CS-ARDL, MG, PMG): y = ln valor tasado, x = ln IPC de alquiler, provincial trimestral (38 unidades, 2002T1-2026T2). Principal: CS-ARDL con p = 2 rezagos y medias transversales de y, x (contemporáneas y 2 rezagos). Multiverso: {MG, PMG} × {sin, con coste de uso = tipo hipotecario real BdE} × p ∈ {1,2,3} más CS-ARDL × p ∈ {1,2,3} sin coste de uso (el coste de uso es común y colineal con las medias transversales): 15 especificaciones frente a las 36 pre-registradas. La segunda «medida de precio» no existe a escala provincial trimestral (IPV solo CCAA, 9 unidades < 10): no se ejecuta. PMG por verosimilitud concentrada en θ. Sin IC (NO APTA).
  - CIPS: estadístico descriptivo del ratio con CADF de 1 rezago; sin valor crítico (el bootstrap no es APTO).
- **Q10.**
  - Información: indicadores mensuales en su última edición (límite declarado, punto 8). Mensuales con historia larga en entrenamiento: importe de nuevas operaciones de vivienda (`bde_importe_vivienda_total_be1911`) y tipo de interés de nuevas operaciones (`bde_tedr_vivienda_total_be1903`). Los `monitor_*` solo tienen 36 meses y no se usan. Visados trimestrales (nacional) como indicador adelantado adicional en el nowcasting.
  - Objetivo h = 1: previsión del trimestre t+1 con información hasta el final de t (el nowcasting NO usa meses de t+1). MIDAS-ADL: Δy(t+1) = c + 4 rezagos AR + β·Σ_j w_j(θ1,θ2)·x_j, Almon exponencial con 6 rezagos mensuales; (θ1,θ2) en una rejilla fija 21×21 y MCO para el resto (reestimado en cada origen). Nowcasting (Q10-2): ecuación puente AR(4) + media trimestral de Δlog importe y de Δ tipo + Δlog visados.
  - Ventana expansiva, tamaño inicial 30 trimestres; el inicio es 2007T1 (Q10-1, Q10-3) y 2002T1 (Q10-2). Sin ajuste de hiperparámetros por bloques: los modelos están fijados de antemano, así que el embargo no interviene; se declara.
  - ECM v1 existe solo para el IPV (Q10-1). Se reproduce con los regresores disponibles en entrenamiento: sin ln_costes (no está en los paneles de entrenamiento) y con diferencias rezagadas un periodo (la versión original usa diferencias contemporáneas, que no están disponibles al predecir). Largo plazo: ln_ipv sobre ln_ocupados, tipo_hip y ln_visados(−4), reestimado en cada ventana. Para IPC de alquiler y compraventas no hay ECM v1: se dice.
  - Segundo horizonte del multiverso: h = 4 (directo). «2 tratamientos de 2020»: (a) sin tratar; (b) excluir de la evaluación los objetivos de 2020T1-2021T2. Modelos: AR(4), paseo con deriva, ECM v1 (solo IPV), MIDAS/nowcasting.
  - DM-HLN, Clark-West y MCS NO APTOS: se publica solo la razón de ECM (reducción puntual). Intervalos conformes: cobertura empírica a 90 % por conformal dividido con los errores pasados absolutos (descriptivo).
- **Rejilla (83 celdas).**
  - Especificación principal: log del resultado ~ exposición + EF de unidad y periodo, en la ventana de la celda (log y positivo; recuentos con valor 0 quedan fuera). Estimación puntual, sin errores típicos (NO APTA).
  - Exposiciones: Q1: fracción del año con zona tensionada vigente en el municipio (`zt_vigente`, trimestral) y, en provincia, esa fracción ponderada por la población municipal de 2021. Q2: log del % de viviendas turísticas INE (media anual; en distrito y sección, el del municipio), estandarizado. Q3: shift-share del grupo B (qb_shiftshare, base 2003, provincia o municipio; en sección, el del municipio). Q4: % de Red Natura municipal × exposición de Q3 municipal. Q6: tipo general del ITP de su CCAA (8 CCAA de q6_itp).
  - Robustez por celda (5 variantes = 415 declaradas): (a) tendencias lineales por CCAA, (b) controles (ln población provincial variable en el tiempo y renta ADRH 2019 × tendencia), (c) a + b, (d) ventana hasta 2019 y (e) ventana desde 2020 (si la ventana principal tiene ≥ 3 años en ese tramo; si no, «no estimable»). No entran en el control de falsos descubrimientos.
  - Celdas sin variación de la exposición en la ventana: «no estimable» (se cuentan como una de las 83 con p null).
- **Aclaraciones posteriores a la ejecución (2026-10-17; anotadas con su momento).**
  - Q9: las provincias con valor tasado y IPC de alquiler trimestrales completos 2002T1-2026T2 son 33, no 38 (las demás carecen de valor tasado trimestral). Se anota al ver el recuento de datos, no un resultado.
  - Q10: tras la primera ejecución se añadió AR(4) con dummies de trimestre del objetivo (`AR4_S`) como **diagnóstico** de lectura (la compraventa tiene estacionalidad que el AR(4) puro no recoge). No es especificación principal ni sustituye al AR(4); se informa junto a las demás.
  - Q3 y Q4 (rejilla): el padrón por nacionalidad termina en 2022, así que las ventanas 2011-2024 y 2018-2025 son efectivas hasta 2022.
  - Q9-g: resultado retenido por la parada D (docs/v16/bloqueos.md, B-2); no va a hechos.json ni a ninguna publicación hasta que decida el autor.

## D5. Correcciones tras la réplica ciega (2026-10-18; decisión K16)
- **Q3-b.** El núcleo de Conley contaba dos veces la diagonal. Con el núcleo corregido, Conley a 2 km es NO APTO en el Monte Carlo, así que Q3-b queda solo con estimación puntual.
- **Q9-g.** Su q de Benjamini-Yekutieli pasa de 0,153 a 0,306, porque ya es el único p válido de la rama de diseños.

## D6. Correcciones tras la revisión adversarial (2026-10-18; decisión K17)
- **Q2c.** La principal vuelve a ser la de la adenda (punto 3): Δlog IPVA municipal sobre la exposición estandarizada en nivel. La precisión de D3 («principal: log estandarizado» y log del nivel del IPVA) contradecía la adenda y queda sustituida. La versión inicial se mantiene como variante.
- **Q6.** El resumen del multiverso excluye las dCDH con la fecha adelantada un año, que equivalen al placebo.

## D7. Q6: diferencias solo entre años consecutivos (2026-10-18; K18)
Error de implementación detectado por la réplica ciega de Q6-p. Con un año sin dato, la diferencia por provincia saltaba el hueco. Corregido: Q6-p pasa de −0,0157 a −0,0020; Q6-v no cambia.


## D8. GSADF de V7.2 corregido; 4.999 réplicas en lugar de 499 (2026-10-18; B-4, orden del autor; K20)
- **Errores de código** (detectados por la réplica ciega de las cifras de la 1.0):
  - **E1.** El BIC que elige el AR(p) del proceso generador del bootstrap comparaba ajustes con distinto número de observaciones. Ahora se compara en la muestra común.
  - **E2.** Un `dropna` conjunto truncaba el IPV de Navarra a 2007T1-2014T4. Ahora cada serie tiene su propio `dropna`, en 2007T1-2026T2.
- **Réplicas.** Con 499 réplicas (hasta la 1.0), el p tiene un error típico de Monte Carlo de ≈ 0,01 cerca de 0,05. Los recuentos cambiaban con la semilla: cocientes tras BH 0 o 1, y CCAA sin ajuste 5 o 6.
  - Se probaron 1.999 y 4.999 réplicas con 5 semillas (src/v16/b4_gsadf_estabilidad.py → output/v16/b4_gsadf/).
  - Con 1.999 no es estable la sensibilidad de la familia de 4. Con 4.999 todos los recuentos ajustados son idénticos en las 5 semillas: es el menor número estable y se adopta.
  - El recuento sin ajuste de los cocientes (1 o 2) no se estabiliza con ningún número finito de réplicas: la serie valor tasado/IPC alquiler tiene un p medio de 0,052. Se publica el de la semilla original (1) y se declara el borde.
- **Familias de BH.** La de los cocientes sigue siendo la de 8 (4 cocientes y 4 referencias con tipos). La de los 4 cocientes se publica solo como sensibilidad (V72-GSADF-ratios-bh4-sens).
- **Cambios de valor:** en ERRATA.md.

## D9. Partes del plan que no se ejecutaron tal como estaban escritas (2026-10-18; anotada tras el arbitraje del informe integral)
El árbitro final (fase 7, hallazgo 14) señaló que estas omisiones solo constaban en docs/v16/decisiones.md y en la adenda. Se numeran aquí, con su motivo:
- **Metaanálisis con Egger, PET y PEESE** (fase 3).
  - La regla K7, fijada antes de ejecutarlo, exige al menos 5 estudios con error estándar y la misma unidad.
  - Ninguno de los 88 grupos de resultado la cumple, así que no hay metaanálisis ni pruebas de sesgo de publicación.
  - La triangulación compara el signo.
- **Bayesiano jerárquico con priors de los metaanálisis** (fase 6).
  - Sin metaanálisis, los priors son poco informativos y centrados en cero (K7).
  - Además, la herramienta es NO APTA en el Monte Carlo de la fase 5 (K12): solo descriptivo.
- **GRF y DML** (fase 6).
  - La adenda (punto 13) los reduce a la prueba conjunta BLP/GATES.
  - Esa prueba es NO APTA (K12): solo descriptiva, sin p.
- **BH jerárquico** (adenda, punto 2).
  - Se sustituye por Benjamini-Yekutieli, la alternativa nombrada en la adenda (punto 11).
  - Motivo: el Monte Carlo dio una FDR máxima de 0,1216 > 0,10 con el BH jerárquico (docs/v16/validacion_montecarlo.md; K12).
- **Condición (b) de Gelman-Carlin** (magnitud de referencia y error de tipo M).
  - No es aplicable donde la pregunta no tiene magnitud de referencia pre-registrada (por ejemplo, Q9; K15).
  - Ninguna pregunta cumple a la vez (a) y (b), así que no hay evaluación sellada de V16 (evaluate_v16 no aplica).
