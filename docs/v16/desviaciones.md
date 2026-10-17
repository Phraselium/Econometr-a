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
