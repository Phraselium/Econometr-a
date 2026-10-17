# V15 · Pre-registro (fase 3)

Versión: borrador de depósito, 2026-10-17. Autor: Borja Romero. Repositorio: el de proyecto.json. Etiqueta local: `prereg-v15`. Registro externo: OSF; el autor lo deposita y anota el identificador en proyecto.json (`osf_prereg_v15`).

Este documento se escribe **antes de estimar ningún efecto de V15**.

**Lo que ya se ha hecho con datos:**
- inventario (docs/v15/inventario_variables.md);
- auditorías descriptivas de calidad (output/v15/auditoria/);
- cálculo de potencia con tratamientos placebo independientes del resultado (output/v15/potencia/);
- revisión de literatura (docs/v15/literatura.md).

En la fase 3 se sella la validación (sección 2). Cualquier desviación de lo que sigue irá a metodologia/desviaciones_v15.md con su motivo.

## 0. Reglas comunes

- **Capas** (metodologia/capas.md): C1, C2, C3, C3s y C4. Nunca se promueve de capa. Solo C3 o C3s admiten lenguaje causal; por debajo, «asociación».
- **Medidas.** Toda especificación va al Registry de src/econ_utils.py. Cada resultado declara su medida de precio o de alquiler (stock de contratos frente a contratos nuevos; tasación frente a transacción) y su capa máxima alcanzable.
- **Corrección múltiple.**
  - *Familia confirmatoria* (H1-H5): Holm, α = 0,05, m = 5.
  - *Exploratorias* (E1-E4 y todo el multiverso): Benjamini-Hochberg al 10 %.
  - El multiverso de V15 no supera 50.000 especificaciones en total. Las cifras por pregunta se declaran abajo y suman 4.104.
- **Multiplicidad entre versiones (declarada).** Desde v1 se han registrado al menos 43.510 especificaciones hasta V7.2, más V8 y V9.
  - La inmigración (P4) y la regulación del alquiler (P6) se han contrastado en cinco versiones o más.
  - Los pisos turísticos (P5), en v3, v6, V8 y V9.
  - La predicción (P9), en todas desde v1.

  Por eso **ningún resultado de V15 se lee aislado**: el informe comparará cada estimación con todas las anteriores de la misma pregunta (metodologia/historial_conclusiones.md).
- **Inferencia.**
  - Con pocos clusters (menos de 50), wild cluster bootstrap con pesos de Webb (9.999 réplicas, SEED=20261010).
  - Si la tasa de rechazo placebo de output/v15/potencia supera 0,075 con la agrupación prevista, se usa la agrupación alternativa declarada en cada pregunta.
- **Exclusión de unidades.** Toda estimación principal se repite excluyendo Madrid, Barcelona, Illes Balears, Canarias y València (si están en la muestra) y sin las unidades del 1 % superior de exposición.
- **Validación.** Muestra sellada nueva de V15 (sección 2). Las muestras de versiones anteriores ya vistas son solo informativas.
- **Datos.**
  - Cruces solo por código INE.
  - Las series no redistribuibles (Incasòl, Registradores ERI, Inside Airbnb) solo salen del repositorio como resultados agregados.
  - Las interpolaciones o series reconstruidas (registro GVA reconstruido) solo entran en robustez.

## 1. Preguntas seleccionadas y descartadas

| Id | Pregunta | Papel | Capa máxima | Motivo |
|---|---|---|---|---|
| P6 | Zonas tensionadas (Ley 12/2023) en Cataluña: renta y número de contratos nuevos | **H1, H2** confirmatorias | C3 | Hay potencia (MDE ≈ 2,2 %, frente a los ≈ 5 % de la literatura). Ahora hay más periodos posteriores que en V9 y SDID con Honest DiD |
| P5 | Densidad de vivienda turística (INE) y alquiler por sección | **H3** confirmatoria | C4 (asociación) | Hay potencia (MDE ≈ 0,4 % por desviación típica, frente al 2-6 % implícito en la literatura). Cruce por código INE. T = 4 y sin periodo previo: no admite C3 |
| P4 | Inmigración y alquiler: shift-share municipal con padrón 2003-2022 | **H4** confirmatoria | C3 (si supera AKM, pretendencias y primera etapa) | Hay potencia (MDE ≈ 0,7 % por desviación típica). El riesgo es de identificación, y se declara |
| P9 | Predicción frente al AR(4) | **H5** confirmatoria (predictiva) | Sin capa causal | Nulo esperado (el DM solo detecta reducciones del ECM ≥ 18-30 %). Cierra una pregunta abierta desde v1 |
| P2 | Fundamentales: cointegración precio-alquiler en panel provincial | **E1** exploratoria | C4 | Asociación de largo plazo. Su potencia se mide por Monte Carlo antes de estimar |
| P7 | Presión demográfica frente a obra nueva | **E2** exploratoria | C4 | Descriptiva: provincial desde 2018 y municipal 2021-2025. La regularización catastral contamina 2011-2021 |
| P10 | Dependencia espacial del crecimiento del alquiler municipal | **E3** exploratoria | C4 | Corte transversal único. Los efectos indirectos dependen de W |
| P5-CV | Robustez de P5 con IDESCAT (Cataluña) y registro GVA (C. Valenciana) 2015-2024 | **E4** exploratoria | C4 | Son las únicas exposiciones con periodo previo. El fechado GVA es un supuesto |
| P1 | Oferta con restricciones físicas | Descartada | — | El repositorio no tiene restricciones físicas ni precio de compra municipal (auditoría de oferta). MDE provincial 6,5 % por desviación típica con 38 unidades |
| P3 | Sorpresas monetarias | Descartada | — | Las magnitudes de la literatura (≈ 0,006-0,010 por desviación típica) quedan por debajo del MDE (0,012-0,025). No hay exposición territorial a tipo variable |
| P8 | Cambio de la brecha de esfuerzo entre orígenes | Descartada como contraste | — | MDE de 9-15 pp en el cambio 2018-2025. Los niveles ya están publicados en V12-B6 (descriptivos) |

## 2. Validación sellada nueva (src/holdout.py: sellar_v15, evaluate_v15)

Se fija y se ejecuta **antes de cualquier estimación**, en el commit que lleva la etiqueta `prereg-v15`. Tiene dos partes.

**(a) Temporal.** Se sellan todos los datos posteriores al depósito: cualquier periodo posterior al último visto de cada variable, que queda registrado en docs/v15/sellado_v15.json con la fecha de corte, y cualquier edición publicada después de esa fecha. Publicaciones esperadas:

| Fuente (variable) | Último periodo visto | Próximas publicaciones esperadas (estimación propia por calendarios previos; sin calendario oficial en el repositorio) | Uso |
|---|---|---|---|
| Incasòl (contratos y renta, municipio, trimestral) | 2026T1 | 2026T2-2026T4, entre finales de 2026 y mediados de 2027 | H1, H2 |
| SERPAVI (sección, municipio) | 2024 | 2025, hacia el segundo semestre de 2027 | H3, H4 |
| INE viviendas turísticas (sección) | 2026-05 | Ediciones semestrales 2026-11 y 2027-05 | H3 |
| Valor tasado MIVAU (provincia, nacional) e IPV INE | 2026T2 | 2026T3-2027T2, entre diciembre de 2026 y septiembre de 2027 | H5, E1 |
| IPC de alquiler (provincia) | 2026T2 | Mensual, desde noviembre de 2026 | E1 |
| Compraventas, hipotecas, visados, afiliación | 2026T2 / 2026-09 | Mensuales desde noviembre de 2026 | H5 (indicadores) |
| Censo anual de población (municipio, nacionalidad) | 2025 | 1-1-2026, hacia diciembre de 2026 | H4 (extensión) |

Los resultados confirmatorios se evalúan con evaluate_v15 una sola vez por hipótesis. La evaluación se hace cuando el bloque tiene al menos el mínimo declarado:
- H1 y H2: 2 trimestres nuevos;
- H3 y H4: 1 año nuevo de SERPAVI;
- H5: 4 trimestres nuevos.

Si a 31-12-2027 no se alcanza el mínimo, se evalúa con lo que haya y se declara.

**(b) Espacial.** Bloque elegido al azar con SEED=20261010 (código en src/holdout.py):
- Se sella el 15 % de las celdas de 0,5° × 0,5° de los centroides municipales: 33 celdas y 853 municipios.
- Los municipios con 5 distritos o más (161) nunca se sellan enteros. En ellos se sella el 15 % de los distritos (1.211 distritos sellados en total, incluidos los de municipios sellados).
- **Fuga declarada:** el agregado municipal de una gran ciudad está en entrenamiento y contiene sus distritos sellados. Por eso la evaluación por sección de esas ciudades no se combina con modelos municipales.

**Uso del bloque espacial.** Las estimaciones de V15 se hacen solo con el entrenamiento. El bloque espacial se usa una vez por hipótesis para reestimar la especificación pre-registrada:
- H1-H4: misma especificación en las unidades selladas; se compara el signo y si el intervalo contiene la estimación de entrenamiento;
- H5: no tiene parte espacial (es nacional).

**Ejecutado** el 2026-10-17 (src/v15/f3_sellado.py; decisiones G6). Las filas de municipio, distrito y sección de las 11 provincias de v6 también quedan fuera: el bloque V15 aparta ≈ 15 % de lo restante.

**Muestras ya vistas (solo informativas).**
- Sellados de v2 (3 provincias, ya evaluadas).
- Sellado de v6 (11 provincias). Sigue fuera de todo uso: no está en la base de entrenamiento.
- Todos los periodos hasta el último visto, porque V9 ya estimó P6 con Incasòl hasta 2025 y V3/V6 estimaron P5 con SERPAVI 2021-2023.

## 3. Hipótesis confirmatorias

### H1 · P6a: zonas tensionadas y renta de los contratos nuevos (Cataluña)
- **Hipótesis.** La declaración de zona tensionada (primera resolución vigente desde 2024-03-16; variable `zt_vigente`) se asocia con una renta media de los contratos nuevos menor que la del contrafactual (contraste bilateral).
- **Estimando.** ATT promedio en log de la renta media ponderada por contratos (Incasòl, municipal, trimestral). Ventana: de 2024T2 al último trimestre de entrenamiento (2026T1). Municipios de Cataluña tratados frente a no tratados.
- **Diseño.** SDID (Arkhangelsky et al.) con efectos de municipio y trimestre. Preperiodo: 2019T1-2023T4 (20 trimestres). Municipios con al menos 5 contratos en cada trimestre del preperiodo.
- **Donantes.** Municipios catalanes nunca tratados hasta 2026T1. Se excluyen los que distan menos de 10 km de un tratado (desbordamientos; Kholodilin et al., Hahn et al.). La distancia se mide entre centroides municipales (data/base/geo).
- **Supuestos.** Tendencias paralelas ponderadas (SDID), sin anticipación antes de 2024T1 y sin interferencia con los donantes lejanos.
- **Especificación principal.** SDID con pesos de unidad y de tiempo y error típico por placebo (bootstrap de placebo con 1.000 réplicas).
- **Pruebas para C3** (todas declaradas):
  - (i) pretendencias en estudio de eventos con SDID y con Callaway-Sant'Anna, además de la potencia de Roth para una pendiente lineal de 1 % por año;
  - (ii) Honest DiD (Rambachan-Roth): M̄ de ruptura, con umbral M̄ ≥ 1 para C3;
  - (iii) placebo temporal, con adopción falsa en 2022T1 sobre el preperiodo;
  - (iv) placebo espacial, con municipios aleatorios de Cataluña (1.000 permutaciones);
  - (v) exclusión de Barcelona y de los municipios con renta en el 10 % superior;
  - (vi) control sintético por municipio para los 10 tratados de mayor tamaño;
  - (vii) inferencia por aleatorización.
- **C3 si:** el ATT es significativo tras Holm en la familia, supera (i) a (iv) y M̄ ≥ 1. Si falla alguna, queda en C4 (asociación).
- **Multiverso** (BH): 2 estimadores (SDID, CS) × 3 umbrales de contratos mínimos (5, 10, 30) × 3 radios de exclusión (0, 10, 25 km) × 2 ventanas (hasta 2025T4 y hasta 2026T1) = 36.
- **Potencia.** MDE80 ≈ 2,2 % con errores por municipio (rechazo placebo 0,058). Referencia de la literatura: ≈ −5 % (Ley 11/2020) y un nulo en renta para 2024 en un preprint (Pérez García, 2026).
- **Qué cambiaría.**
  - Si es C3 con ATT negativo, cambia V9-D1a: de «C4, pretendencias rechazadas» a «C3». Sería la primera cifra causal de regulación del repositorio.
  - Si da un nulo con intervalo que excluye −5 %, matiza la lectura de los topes de la Ley 11/2020 (V9-D1b) para la Ley 12/2023: no son la misma intervención.
  - Si falla las pruebas, confirma V9-D1a (C4).
- **Si no pasa las pruebas.** Se publica como C4 con todas las pruebas fallidas listadas. No se cambia la especificación para pasarlas.

### H2 · P6b: zonas tensionadas y número de contratos nuevos
- **Igual que H1**, con el resultado log(1 + contratos nuevos) por municipio y trimestre (Incasòl).
- **Hipótesis.** Bilateral.
- **Referencia.**
  - Pérez García (2026): ≈ −13 %, robusto a tres diseños.
  - V9: «sin diferencia detectable», sin potencia.
- **Potencia.** MDE80 ≈ 4,1 % en log(1 + contratos), con 541 municipios, 270 tratados placebo y errores por municipio (rechazo placebo 0,044; output/v15/potencia). Es menor que el −13 % de la referencia.
- **Multiverso:** 36, como en H1.
- **Qué cambiaría.** Una caída C3 cambiaría la conclusión «no se detecta caída del número de contratos» (V9, C4).

### H3 · P5: densidad de vivienda turística y alquiler por sección
- **Hipótesis.** Dentro de cada sección, los años con mayor porcentaje de viviendas turísticas (INE, `ine_vut_porcentaje_vivienda_turistica`, media anual de las ediciones del año) se asocian con un alquiler declarado mayor. Es decir, la mediana SERPAVI en €/m² de vivienda colectiva de esa sección y año. Contraste bilateral.
- **Estimando.** Coeficiente de log(alquiler) sobre el porcentaje de viviendas turísticas estandarizado (por 1 desviación típica intra-sección), con efectos fijos de sección y de municipio × año. Periodo 2021-2024 en entrenamiento.
- **Supuestos.** Exogeneidad estricta condicional a los efectos fijos. No es un diseño causal: **capa máxima C4**, como mucho asociación robusta.
- **Inferencia.**
  - Principal: errores agrupados por municipio (rechazo placebo 0,058).
  - Alternativa: Conley a 2 km.
- **Pruebas.**
  - Placebo de adelanto: la exposición en t+1 no debe asociarse con el alquiler en t una vez controlada la de t.
  - Exclusión de las 5 grandes ciudades.
  - Medida alternativa del resultado: IPVA por distrito.
  - Exclusión de secciones con saltos de factor > 10 en la serie INE (auditoría de turismo).
  - Moran en residuos.
- **Multiverso** (BH): 2 resultados (SERPAVI VC, VU) × 3 exposiciones (porcentaje, viviendas por 100 hogares, plazas) × 2 efectos fijos temporales (año, municipio × año) × 2 muestras (todas, sin saltos) × 2 agrupaciones = 48.
- **Potencia.** MDE80 ≈ 0,4 % por desviación típica. Implicado por la literatura: 2-6 % por desviación típica si la dispersión del log de exposición es de orden 1.
- **Qué cambiaría.**
  - Una asociación positiva robusta por sección en toda España cambiaría «turísticos: no concluyente» (v3, v6, V8, V9), pero solo como asociación (C4).
  - Un nulo preciso por debajo de 0,5 % por desviación típica contradiría la literatura en los barrios muy expuestos, y se investigará la medida antes de leerlo.
- **Si no pasa las pruebas.** Si falla el placebo de adelanto: C4 «no concluyente».

### H4 · P4: inmigración y alquiler (shift-share municipal)
- **Hipótesis.** El crecimiento de la población extranjera predicho por cuotas de origen se asocia con el crecimiento del alquiler municipal. Contraste bilateral.
  - Cuotas por nacionalidad de 2003 en cada municipio: padrón INE, 28 países.
  - Choques: crecimiento nacional de cada nacionalidad, excluido el propio municipio (leave-one-out).
- **Estimando.** Elasticidad de 2SLS de log(alquiler SERPAVI €/m² VC) respecto a la tasa de población extranjera / población inicial. Panel municipal anual 2011-2022 con efectos de municipio y de provincia × año.
- **Diseño.**
  - Shift-share (Borusyak-Hull-Jaravel); identificación por los choques.
  - Inferencia AKM (Adão-Kolesár-Morales) y AKM0.
  - Pesos de Rotemberg reportados.
  - F efectivo de Montiel Olea-Pflueger e intervalos de Anderson-Rubin.
- **Pruebas para C3.**
  - (i) F efectivo ≥ 10.
  - (ii) Pretendencias: el instrumento de 2011-2022 no predice el crecimiento del alquiler de 2008-2011. Ese tramo no existe en SERPAVI (empieza en 2011), así que se usa el IPC de alquiler provincial como resultado previo.
  - (iii) Balance de los choques (BHJ) frente a características municipales de 2003.
  - (iv) Corrección de Jaeger-Ruist-Stuhler: controlar por el instrumento retardado.
  - (v) Exclusión de los 5 orígenes con mayor peso de Rotemberg.
  - (vi) Desbordamientos: repetir con el área de 15 km.
- **C3 si:** Holm, (i) a (v) y AKM significativo. Si no, C4.
- **Multiverso** (BH): 2 resultados (VC, VU) × 2 normalizaciones (población inicial, población del periodo anterior) × 2 conjuntos de orígenes (28 países, continentes) × 2 especificaciones temporales (provincia × año, año) × 2 años base (2003, 2008) × 2 muestras (todas, ≥ 1.000 habitantes) = 64.
- **Potencia.** MDE80 ≈ 0,7 % por desviación típica (forma reducida). La primera etapa es desconocida; si su F < 10, H4 se reporta con intervalos AR y queda en C4.
- **Qué cambiaría.**
  - Un efecto C3 positivo cambiaría «no concluyente» (v1-V9) y daría una magnitud para comparar con Saiz (≈ 1 % por 1 % de población).
  - Un nulo con AKM estrecho sería un nulo bien identificado.
  - Un instrumento débil confirma lo que ya sabíamos (V9-D4, F 4,6).
- **Si no pasa las pruebas.** C4, con la primera etapa y los pesos de Rotemberg publicados.

### H5 · P9: predicción frente al AR(4)
- **Hipótesis.** La combinación pre-registrada predice el crecimiento trimestral del valor tasado nacional (Δlog, h = 1) con menor ECM que el AR(4) en el bloque temporal sellado. DM-HLN unilateral.
  - La combinación es la media simple de cuatro modelos: DFM con indicadores mensuales agregados, BVAR de Minnesota con 6 variables, LASSO con indicadores y ARDL con compraventas e hipotecas.
- **Línea base.** AR(4) en la misma muestra, con la misma ventana expansiva desde 1995T1. Contraste adicional frente al ECM v1.
- **Contrastes adicionales.** GW (condicional), CW (anidado) y MCS al 10 % con los cinco modelos y el AR(4).
- **Potencia.** Con 73 errores de entrenamiento, el MDE es una reducción del 18-30 % del ECM. En el bloque sellado (≥ 4 trimestres) la potencia es muy baja. Se declara: el resultado esperado es «no distinguible del AR(4)».
- **Multiverso** (BH): 5 modelos × 3 horizontes (1, 2, 4) × 2 medidas (valor tasado, IPV) × 2 tratamientos de 2020 (con dummy y sin ella) = 60.
- **Qué cambiaría.** Batir al AR(4) tras Holm y en el bloque sellado cambiaría la conclusión K1 («ningún modelo supera al AR(4)»). Un nulo la confirma.

## 4. Exploratorias (BH al 10 %)

### E1 · P2: precio frente a alquiler y coste de uso (panel provincial)
- **Datos.** log(valor tasado) y log(IPC de alquiler) provinciales trimestrales, de 1995T1 (alquiler: 2002T1) a 2026T2. Provincias de entrenamiento.
- **Coste de uso.** Tipo hipotecario real + amortización (2 %) − ganancia esperada (media móvil de 8 trimestres).
- **Pruebas.** CIPS, CD de Pesaran, Westerlund con bootstrap, CS-ARDL (elasticidad de largo plazo y velocidad de ajuste) y PMG/MG como contraste.
- **Validación previa.** Antes de estimar, el agente montecarlo valida la potencia de CIPS y Westerlund con N ≈ 40 y T ≈ 98 y un factor común. Si la potencia no llega a 0,5 frente a una velocidad de ajuste de −0,04 trimestral, E1 se reporta solo como descriptiva.
- **Multiverso:** 3 estimadores × 2 medidas de precio (valor tasado, IPV por CCAA) × 2 con o sin coste de uso × 3 rezagos = 36.
- **Qué cambiaría.** Una cointegración estable con CS-ARDL y semivida de 2 a 7 años matizaría «no se establece cointegración» (V7.2), siempre como C4.

### E2 · P7: presión demográfica frente a obra nueva
- **Descripción.** Hogares nuevos estimados (V12-B3) frente a obra neta del Catastro (corrigiendo el desfase de un año; decisiones G4) y terminadas del MIVAU. Provincial 2018-2025 y municipal 2021-2025. Correlación con el crecimiento del alquiler.
- **Especificaciones.** Descriptivas, 24 en total.

### E3 · P10: dependencia espacial del alquiler municipal
- **Diseño.** Δlog SERPAVI 2015-2024. I de Moran, SAR, SEM y SDM con W de contigüidad y W de distancia inversa (corte 25 km), efectos directos e indirectos (LeSage-Pace) y errores de Conley.
- **Especificaciones.** 3 modelos × 2 W × 2 periodos = 12.

### E4 · P5-CV: exposición con periodo previo
- **Cataluña.** IDESCAT (HUT por municipio, 2015-2024) frente a Incasòl (renta de contratos nuevos, anual).
- **Comunitat Valenciana.** Registro GVA reconstruido (C4, supuesto de fechado) frente a SERPAVI municipal.
- **Diseño.** Estudio de eventos de dosis continua con pretendencias de 2015-2017 y Honest DiD.
- **Especificaciones.** 2 regiones × 2 medidas × 3 escenarios de fechado (solo C. Valenciana) × 2 ventanas = 24.

## 5. Recuento del multiverso declarado

| Bloque | Especificaciones |
|---|---|
| H1 | 36 |
| H2 | 36 |
| H3 | 48 |
| H4 | 64 |
| H5 | 60 |
| E1 | 36 |
| E2 | 24 |
| E3 | 12 |
| E4 | 24 |
| Pruebas de robustez y permutaciones (no cuentan como especificaciones: son la misma especificación con otra inferencia) | — |
| Holgura para desviaciones declaradas (máximo; cada una con su motivo en desviaciones_v15.md) | 3.764 |
| **Total máximo** | **4.104** (≤ 50.000) |

## 6. Herramientas que requieren Monte Carlo antes de usarse (fase 4)
Cada herramienta se valida con nuestro proceso generador, con el N, el T, la dependencia transversal y el número de clusters de cada pregunta:
- SDID y su error por placebo (H1, H2);
- Honest DiD (implementación propia de V9, con tamaño del 7,3 % en 400 réplicas: se revalida o se sustituye);
- control sintético;
- AKM y AKM0 (H4);
- wild cluster bootstrap de Webb;
- Conley (H3, E3);
- DFM, BVAR y MCS (H5);
- CIPS, Westerlund y CS-ARDL (E1);
- SAR y SDM (E3).

Ninguna se usa si su tamaño empírico al 5 % sale de [0,03; 0,08].

## 7. Qué no se hará
- No se elegirá ninguna especificación por su p-valor.
- No se usará SHAP ni ninguna importancia para lenguaje causal.
- No se combinarán resultados por sección de grandes ciudades con modelos municipales en la evaluación sellada.
- No se reportará la exposición reconstruida del registro GVA como principal.
- No se evaluará el bloque sellado más de una vez por hipótesis.
