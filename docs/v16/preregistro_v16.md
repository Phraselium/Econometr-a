# V16 · Pre-registro interno (fase 4)

**Tipo:** pre-registro interno, sin sello de tiempo externo. Lo fija la etiqueta git `prereg-v16`, publicada en el remoto del repositorio de desarrollo; su commit y su fecha están en docs/v16/etiquetas_prereg.csv. No es un pre-registro depositado.

**Fecha de redacción:** 2026-10-17. **Autor:** Borja Romero. La adenda (docs/v16/preregistro_v16_adenda.md) prevalece donde difiera.

**Relación con V15.** Complementa docs/v15/preregistro_v15.md y sus dos adendas:
- **Lo que no cambia.** H1-H5 de V15 no se modifican ni se reformulan. Siguen siendo la única familia confirmatoria vigente y se evalúan según su calendario (H1/H2 hacia marzo de 2027, H5 hacia octubre de 2027, H4 en el último trimestre de 2027).
- **Lo que añade V16.** Solo preguntas, datos y rejillas nuevas, con su solapamiento con V15 declarado (sección 2).

**Lo hecho con datos antes de este documento** (sin estimar ningún efecto de V16):
- adquisición, normalización y auditoría de fuentes (fase 1; docs/v16/inventario_fuentes.csv, output/v16/auditoria/);
- hechos y contabilidad descriptivos (fase 2; output/v16/f2_*);
- literatura, metaanálisis y marco de cuatro cuadrantes (fase 3; docs/v16/literatura.md, output/v16/f3/);
- potencia con tratamientos placebo independientes del resultado (output/v16/potencia/).

Lo ya visto de V5-V15, con sus cifras, está en docs/v16/lo_ya_visto.md: todo él es informativo. Cualquier desviación irá a metodologia/desviaciones_v16.md con su motivo.

## 0. Reglas comunes
- **Capas.** C1, C2, C3, C3s y C4 (metodologia/capas.md); nunca se promueve de capa. Solo C3 y C3s admiten lenguaje causal; por debajo se habla de asociación.
- **Medidas.** Cada resultado declara su medida:
  - precio: IPV ajustado por calidad, o precio medio por m² de tasación, notarial o registral;
  - alquiler: stock de contratos (SERPAVI, IPC) o contratos nuevos (fianzas, IPVA nuevo).
- **Registro.** Toda especificación va al Registry de src/econ_utils.py. Ningún modelo se elige por su p-valor.
- **Corrección múltiple.** V16 no tiene familia confirmatoria propia (sección 1). Todas las pruebas de V16 son exploratorias:
  - Benjamini-Hochberg jerárquico al 10 % sobre la rejilla completa (sección 4), con q-valores;
  - en la rejilla, primero se controla la familia de cada pregunta y después las celdas dentro de cada familia rechazada (Yekutieli, 2008).
- **Líneas base.** En predicción, AR(4) y ECM v1 en la misma muestra, con validación en bloques con embargo.
- **Inferencia:**
  - con menos de 50 clusters, wild cluster bootstrap con pesos de Webb (9.999 réplicas, SEED=20261010);
  - correlación espacial: errores de Conley a 2, 10 y 25 km;
  - en IV: F efectivo de Montiel Olea-Pflueger e intervalos de Anderson-Rubin.
  - Si la tasa de rechazo placebo de output/v16/potencia supera 0,075 con la inferencia prevista, el diseño solo se reporta con la inferencia alternativa que el Monte Carlo de la fase 5 valide; si no hay ninguna, se reporta como descriptivo.
- **Exclusión de unidades:**
  - Toda estimación principal se repite sin las grandes ciudades (Barcelona, València, Sevilla, Málaga, Zaragoza si está en la muestra) y sin islas.
  - Las 8 CCAA de la muestra v6 están fuera de todo uso a escala provincial e inferior (decisiones K8).
- **Datos:**
  - cruces solo por código INE;
  - las series de terceros (Notariado, Registradores, CGPJ, Red Natura, EA-MPD) solo salen como agregados propios;
  - las interpolaciones, los valores sustitutos del ADRH y las fechas fiscales aproximadas (78 de 105 son el 1 de enero) solo entran en robustez.
- **Herramientas.** Ninguna se usa sin pasar su Monte Carlo de la fase 5 (sección 6).

## 1. Decisión sobre qué es confirmatorio en V16, y por qué
La potencia (output/v16/potencia/informe.md) se calculó con tratamientos placebo, antes de este documento. El criterio para una pregunta confirmatoria nueva, fijado aquí antes de estimar, exige tres cosas:
- (a) un MDE80 por debajo de la magnitud plausible de la literatura con diseño creíble (docs/v16/literatura.md; no la mediana de output/v16/f3, que mezcla unidades);
- (b) una tasa de rechazo placebo ≤ 0,075 con la inferencia prevista;
- (c) una identificación al menos «adecuada» y que no repita una hipótesis de V15.

**Ninguna Q1-Q10 cumple las tres:**
- Los diseños con MDE suficiente tienen inferencia mal calibrada (rechazo placebo de 0,09 a 0,15 con pocos clusters) o una identificación débil.
- Los diseños bien calibrados solapan con H3 o H4 de V15.

Por eso **V16 no añade hipótesis confirmatorias**. Todo lo de V16 es exploratorio, con la capa máxima que se indica, y H1-H5 de V15 siguen siendo la única familia confirmatoria (Holm, m = 5). Rebajar el criterio después de ver la potencia sería elegir por conveniencia: no se hace.

La regla de la tasa de rechazo vale también al revés. Si el Monte Carlo de la fase 5 calibra una inferencia (por ejemplo, wild bootstrap de Webb) para un diseño que cumple (a) y (c), ese diseño **no** pasa a confirmatorio. La decisión queda tomada aquí. Su resultado se lee como exploratorio y se declara.

## 2. Preguntas: diseño, estimando, capa máxima, solapamiento y qué cambiaría

Con el control jerárquico de la sección 4, una pregunta exploratoria puede dar un **hallazgo** solo si cumple las tres condiciones siguientes. Si no, es una **pista** (C4) o un nulo:
- (a) supera BH jerárquico al 10 %;
- (b) tiene un tamaño plausible: errores de tipo S < 0,1 y de tipo M < 2 según Gelman-Carlin, con la magnitud de la literatura como efecto verdadero hipotético;
- (c) se replica en la muestra sellada V16, con el mismo signo y el intervalo conteniendo la estimación de entrenamiento, o en unidades independientes comparables.

Para C3 hace falta además superar todas las pruebas de la sección 3 de su diseño.

### Q1 · Zonas tensionadas: lo que V15 no cubre
- **Solapa con H1 y H2 de V15:** las mismas declaraciones y los mismos datos de Incasòl. **Nuevo:** el diseño (RD, SDID y ASCM con donantes de otras CCAA), los resultados (IPVA nuevo y existente, compraventas y valor tasado) y el ámbito (toda España no sellada).
- **Q1a · RD en el criterio de precio del art. 18** de la Ley 12/2023 (subida del alquiler o del precio en 5 años > IPC + 3 p.p.). **Reformulada.**
  - El criterio de esfuerzo (> 30 % de la renta) no se puede usar: con la aproximación disponible (alquiler SERPAVI × 70 m² sobre la renta ADRH), ningún municipio no sellado lo supera (máximo 0,287).
  - Variable de asignación: crecimiento del alquiler SERPAVI 2019-2024 menos el umbral, con 942 municipios a ± 10 puntos logarítmicos.
  - La declaración la pide cada CCAA, así que es un RD **difuso** con primera etapa.
  - Estimando: efecto local de la declaración sobre Δlog del alquiler SERPAVI posterior.
  - Pruebas: densidad (McCrary y Cattaneo-Jansson-Ma), balance de covariables (renta ADRH, población, cuota extranjera), rdrobust con ancho óptimo y robusto, placebos en umbrales falsos y en el periodo previo.
  - Capa máxima: C3 si supera todo y la primera etapa tiene F ≥ 10; si no, C4.
  - MDE80 con umbrales placebo: 4,45 puntos logarítmicos, frente a −3 % a −7 % en la literatura: **sin potencia para la cota inferior**.
- **Q1b · SDID y control sintético aumentado (ASCM)** con donantes de CCAA sin zonas, en el panel municipal de SERPAVI (anual) y en el provincial de IPVA (trimestral, nuevo frente a existente).
  - Capa máxima: C3 con las pruebas de la sección 3.
  - MDE80: 7,1 % en SERPAVI municipal y 1,2-2,5 % en IPVA provincial, con rechazo placebo de 0,10 a 0,11 (sin calibrar). Inferencia: wild bootstrap de Webb, si la fase 5 lo valida.
- **Q1c · Desplazamiento a la venta** (compraventas y valor tasado provinciales). Exploratoria descriptiva, C4. MDE80 de 11,7-13,3 %: **sin potencia**, y se reporta como tal.
- **Q1d · Desplazamiento al alquiler de temporada.** **Descartada:** no hay datos anteriores a 2025. La desbloquearían el Registro Único y las fianzas por tipo de contrato (tareas_autor §3, puntos 6-7).
- **Qué cambiaría.**
  - V9-D1a (C4, no supera las pruebas) y H1/H2 de V15 no cambian por Q1: Q1 es exploratoria.
  - Un hallazgo que cumpla (a)-(c) con el mismo signo que H1 se presentará como triangulación cuando H1 se evalúe.
  - Un signo opuesto a una conclusión publicada es una parada D: se documenta, no se publica y se espera.

### Q2 · Vivienda turística, más allá de H3
- **Solapa con H3 y E4 de V15:** la exposición INE-VUT y el alquiler. **Nuevo:**
  - los datos: Inside Airbnb agregado, el registro de Andalucía con fechas de alta y el registro de Euskadi;
  - el diseño: un shift-share con la demanda turística exógena, construido con las cuotas municipales de pernoctaciones por país de origen y el crecimiento nacional de cada origen sin el propio municipio.
- **Q2a · Shift-share de demanda turística** (provincial y municipal donde haya pernoctaciones).
  - Estimando: elasticidad de la forma reducida y 2SLS del alquiler respecto a la exposición turística.
  - Pruebas: AKM, pesos de Rotemberg, pretendencias y F efectivo.
  - Capa máxima: C3 si lo supera todo. MDE80: 0,41 puntos logarítmicos por desviación típica, con rechazo placebo 0,096 (sin calibrar).
- **Q2b · Registro de Andalucía** (altas por municipio y fecha) frente al alquiler SERPAVI municipal: estudio de eventos de dosis continua. Capa máxima C4. MDE80: 1,43 por desviación típica.
- **Q2c · Exposición INE-VUT municipal (2021-2024) frente al IPVA municipal.** Capa máxima C4 (asociación). MDE80: 0,39 por desviación típica, con rechazo placebo 0,052.
  - Es la variante municipal y con otro resultado de H3, así que se lee como robustez de H3, no como prueba independiente.
- **Descartadas:**
  - **DiD con moratorias:** solo València, con un año posterior, queda como ciudad tratada no sellada, y el rechazo placebo es de 0,85.
  - **RD espacial en el PEUAT:** no hay geometría de zonas (tarea del autor).
  - **Inside Airbnb como exposición en estimación:** solo hay cuatro instantáneas no selladas desde 2025-12. Se queda en descriptivo hasta que llegue el histórico (tareas_autor §3, punto 1).
- **Qué cambiaría.** La conclusión publicada sobre la vivienda turística es «no concluyente» (v3, v6, V8 y V9; ver lo_ya_visto). Un hallazgo de Q2a que cumpla (a)-(c) y sea C3 la cambiaría a un efecto positivo con su magnitud. Si lo hiciera en sentido opuesto a una conclusión publicada, sería una parada D.

### Q3 · Inmigración, más allá de H4
- **Solapa con H4 de V15:** las mismas cuotas del padrón de 2003 y los mismos choques. **Nuevo:**
  - alquiler y compra separados (compraventas y valor tasado provinciales);
  - la escala de barrio (sección; Δlog SERPAVI 2021-2024 con cuotas por continente del padrón por sección de 2022);
  - Rotemberg y pretendencias propias.
- **Estimandos:**
  - elasticidad del alquiler, por un lado, y de la compra, por otro, respecto a la población extranjera predicha;
  - en el barrio: forma reducida por desviación típica de la exposición.
- **Pruebas:** AKM y AKM0, Rotemberg, exclusión de los cinco orígenes de mayor peso, pretendencias, control por el instrumento retardado (Jaeger-Ruist-Stuhler) y desbordamientos a 15 km.
- **Capa máxima:** C3 en el municipal si lo supera todo. C4 en barrio, porque la cuota por sección es de un solo año.
- **MDE80:**
  - alquiler municipal: 0,83 por desviación típica (rechazo 0,088);
  - compra: 2,3-4,9 (rechazo 0,10-0,13);
  - barrio: 0,98 (rechazo 0,052).
- **Qué cambiaría.** La conclusión publicada es V9-D4 (instrumento débil, C4). Un hallazgo C3 de Q3 la cambiaría.
  - La literatura sugiere menos efecto dentro de la ciudad (Saiz y Wachter): un signo distinto en barrio y municipio no se tratará como contradicción, sino como heterogeneidad que hay que describir.

### Q4 · Oferta: elasticidad municipal con restricciones físicas
- **Datos y reformulación.**
  - Restricción: % de la superficie municipal en Red Natura 2000 (terceros, en disco) y costa. La pendiente (MDT05), el agua y el planeamiento (SIU) faltan; son tareas del autor.
  - Por eso la versión tipo Saiz es parcial y se declara así.
- **Q4a.** Primera etapa: la obra nueva neta del Catastro (2012-2025) frente a la restricción física. Asociación, C4. MDE80: 2,45 por desviación típica (rechazo 0,116, sin calibrar).
- **Q4b.** Interacción entre la restricción y los choques de demanda de Q3: ¿responden más en precio los municipios menos elásticos? C4. MDE80: 0,64 (rechazo 0,116).
- **Qué cambiaría.** No hay ninguna conclusión publicada sobre la elasticidad municipal: P1 se descartó en V15. Cualquier resultado es nuevo y exploratorio.

### Q5 · Tipos de interés
- **Diseño:**
  - proyecciones locales nacionales y SVAR con instrumento externo, con las sorpresas de Jarociński-Karadi (mediana y «poor man's»; versión mensual CC BY 4.0) sobre IPV, valor tasado, compraventas e IPC de alquiler, a horizontes de 1, 4, 8 y 12 trimestres;
  - EA-MPD (terceros) solo en robustez.
- **Sin exposición territorial:** el peso de la hipoteca variable solo es nacional (BdE). La variante por exposición se descarta y se dice.
- **Capa máxima:** C3 si el instrumento es fuerte (F efectivo ≥ 10 con las sorpresas en la primera etapa sobre el tipo hipotecario) y supera los placebos de resultados que no deberían moverse. Si no, C4.
  - MDE80: 0,25-9,9 puntos logarítmicos por desviación típica de sorpresa, según la variable y el horizonte.
  - La literatura (P3 de V15) da ≈ 0,6-1,0 a horizontes cortos: **sin potencia salvo en el horizonte más corto del valor tasado**, y se dice.
- **Qué cambiaría.** V15 descartó P3. El marco de cuatro cuadrantes (output/v16/f3) predice un precio a la baja con un shock solo de tipos; en 2022-2024 los datos no muestran ese patrón. Un resultado C3 cuantificaría el componente de tipos.

### Q6 · Fiscalidad de la compra (ITP)
- **Diseño:** DiD escalonado de Callaway-Sant'Anna y Sun-Abraham.
  - Datos: 20 cambios del tipo general del ITP en 8 CCAA no selladas, entre 2011 y 2024 (output/v16/f1/intervenciones.csv; fechas en su mayoría aproximadas al 1 de enero).
  - Resultados: compraventas de vivienda usada y valor tasado provinciales.
  - Robustez: la fecha de la ley autonómica.
- **MDE80:** 9,4-18,8 %, frente a la magnitud plausible de −7 % por punto (Alemania) × 1,8 puntos de cambio medio ≈ −13 %. El rechazo placebo es de 0,15 con 8-11 clusters.
- **Decisión:** exploratoria, C4 como máximo (pocos clusters, fechas aproximadas). Inferencia por aleatorización sobre el calendario y wild bootstrap de Webb si la fase 5 los valida; si no, solo descriptiva (estudio de eventos sin p-valor).
- **Qué cambiaría.** No hay ninguna conclusión publicada.

### Q7 · Ayudas a la demanda
- **Q7a · Bono Alquiler Joven.** Reformulada como diferencia en discontinuidades por la edad de 35 años del sustentador principal en la ECV.
  - Datos: alquiler pagado por los inquilinos de mercado de 30 a 40 años, antes (2018-2021) y después (2023-2025).
  - Hay unos 2.200 y 2.500 hogares en cada ventana, y ningún microdato de perceptores.
  - MDE80: 13,2 %, frente a una cota de incidencia del 13,9 % con cobertura plena: **potencia en el límite**. Capa máxima C4, porque la edad no asigna el bono por sí sola.
- **Q7b · Avales ICO.** **Descartada:** no hay compraventas por edad del comprador.
- **Qué cambiaría.** No hay ninguna conclusión publicada.

### Q8 · Fin de la golden visa
**Descartada.** No hay compras por nacionalidad comunitaria o extracomunitaria en datos abiertos, ni autorizaciones del OPI (tareas_autor §3, punto 2). Se reabrirá con una adenda **antes** de mirar esos datos si el autor los consigue.

### Q9 · Fundamentales y burbuja
- **Solapa con E1 de V15:** el mismo panel provincial de precio y alquiler. **Nuevo:**
  - la ratio precio/renta (renta ADRH por provincia) y el coste de uso;
  - Westerlund con bootstrap y CS-ARDL frente a PMG y MG;
  - GSADF por provincia con corrección múltiple.
- **Potencia:**
  - CIPS sobrerrechaza (tamaño 0,097 con N = 38 y T = 95): solo con valores críticos por bootstrap validados en la fase 5;
  - GSADF por provincia no alcanza el 80 % de potencia con ninguna ρ explosiva entre 1,01 y 1,05, y con Bonferroni la potencia es casi nula.
- **Decisión:** exploratoria, C4. El GSADF por provincia se publica como descriptivo, con la advertencia de potencia: un «no explosivo» no prueba la ausencia de burbuja.
- **Qué cambiaría.** Lo publicado en la versión 7.2 dice «sin exuberancia de los cocientes tras el ajuste múltiple». Q9 no puede cambiarlo hacia «hay burbuja» sin superar BH jerárquico y replicarse en el bloque sellado temporal.

### Q10 · Predicción, más allá de H5
- **Solapa con H5 de V15**, que sigue siendo confirmatoria con su calendario. **Nuevo:**
  - modelos: MIDAS con indicadores mensuales, *nowcasting* con indicadores adelantados (compraventas, hipotecas, visados, afiliación) e intervalos de predicción conformes;
  - objetivos: IPV, IPC de alquiler y compraventas.
- **Contrastes:** frente al AR(4) y al ECM v1 en la misma muestra, con DM-HLN, GW, CW y MCS al 10 %.
- **MDE:** reducción del ECM del 18-76 % según objetivo y horizonte. Se espera «no distinguible del AR(4)».
- **Qué cambiaría.** La conclusión K1 («ningún modelo supera al AR(4)») solo la cambia H5 de V15. Q10 es exploratoria.

## 3. Pruebas por diseño para alcanzar C3
Las pruebas se declaran ahora; si se omite alguna, la capa máxima es C4. Cada diseño debe pasar las que le aplican:
- **DiD, SDID y estudios de eventos (Q1b, Q2b, Q6):**
  - pretendencias, con Honest DiD (Rambachan-Roth; umbral M̄ ≥ 1) y potencia de Roth para una pendiente del 1 % anual;
  - placebos de fecha (adopción falsa en el preperiodo), de unidades (permutaciones) y de resultados que no deberían moverse (controles negativos: población de más de 65 años, IPC general provincial);
  - inferencia por aleatorización y wild cluster bootstrap de Webb;
  - exclusión de grandes ciudades e islas.
- **IV y shift-share (Q2a, Q3, Q5):**
  - F efectivo de Montiel Olea-Pflueger ≥ 10 e intervalos AR;
  - AKM y AKM0;
  - pesos de Rotemberg y exclusión de los cinco mayores;
  - balance de choques (BHJ) y pretendencias;
  - errores de Conley.
- **RD (Q1a, Q7a):**
  - densidad (McCrary y Cattaneo-Jansson-Ma);
  - balance de covariables;
  - rdrobust con ancho óptimo y con 0,5 y 2 veces ese ancho;
  - umbrales placebo;
  - en el RD difuso, primera etapa con F ≥ 10.
- **Sensibilidad a confusores no observados (todas):** Oster (δ para β = 0), valor de robustez de Cinelli-Hazlett y E-values.
- **Triangulación:** C3 exige el mismo signo con al menos dos diseños de identificación distintos de la misma pregunta. Por ejemplo: Q1a y Q1b; Q2a y Q2b; Q3 municipal y por exclusión de orígenes. Con un solo diseño, la capa máxima es C4 aunque pase sus pruebas.

## 4. Búsqueda multiescala declarada (rejilla fija)
- **Rejilla.** output/v16/potencia/rejilla_candidata.csv: 194 celdas de escala × dimensión × resultado con datos no sellados.
  - Escalas: nacional, CCAA, provincia, municipio, distrito y sección.
  - Dimensiones: Q1-Q7 y Q9.
  - Se fija aquí y no se amplía después. Cada celda se estima con 2 ventanas (hasta 2019 y desde 2020) × 3 especificaciones (efectos fijos de unidad y tiempo; con tendencias por CCAA; con controles de renta y población) = 1.164 contrastes.
- **Modelos jerárquicos bayesianos** con reducción hacia la media (partial pooling) por escala anidada (sección ⊂ distrito ⊂ municipio ⊂ provincia ⊂ CCAA):
  - Priors: el metaanálisis no dio ningún agregado (decisiones K7), así que se usan normales centradas en 0 con desviación típica igual al mayor efecto absoluto de diseño creíble de la literatura de cada instrumento (docs/v16/literatura.md), y semi-Cauchy(0, 1) para las varianzas entre unidades.
  - Comprobación con *prior* y *posterior predictive checks*. Si fallan, el modelo no se usa y se dice.
- **Heterogeneidad:**
  - *generalized random forests* con partición honesta (bosques causales) sobre las celdas de Q1-Q3 con diseño;
  - DML (Chernozhukov et al.) para controles de alta dimensión, con validación en bloques espaciales;
  - nada causal sale de importancias ni de SHAP.
- **Control de falsos descubrimientos:** BH jerárquico al 10 % sobre las 1.164 pruebas (preguntas → celdas), con q-valores publicados para todas.

## 5. Validación sellada V16 (src/holdout.py: sellar_v16, evaluate_v16)
- **No se toca la de V15** ni la de v6.
- **Espacial.** El 15 % de las celdas de 0,5° × 0,5° que no están en v6 ni en V15 (generador independiente [20261010, 16]): 28 celdas y 777 municipios. En los municipios con 5 distritos o más, el 15 % de los distritos que no ha sellado V15: 1.118 distritos en total. Sin solapes (tests/v16/test_holdout_v16.py).
- **Temporal.** Todo periodo posterior al último visto de cada variable de V16, y toda edición publicada después de la fecha del commit etiquetado prereg-v16. Queda escrito en docs/v16/sellado_v16.json, que genera src/v16/f4_sellado.py en el mismo commit de la etiqueta.
- **Uso.** Cada pregunta abre la muestra sellada una sola vez (evaluate_v16; registrado antes de leer), para la condición (c) de la sección 2. Solo se puede abrir con la etiqueta prereg-v16 publicada en el remoto.
- **Ya visto (informativo).** Todos los periodos hasta el último visto y todas las unidades de entrenamiento de V16 (decisiones K8 sobre las 8 CCAA de v6).

## 6. Herramientas que requieren Monte Carlo (fase 5)
Todas se validan con el proceso generador de cada pregunta: pocos clusters, dependencia transversal, T corto, adopción escalonada y correlación espacial. Ninguna se usa si su tamaño al 5 % sale de [0,03; 0,08] o su cobertura al 95 % de [0,92; 0,97].
- SDID y ASCM;
- Callaway-Sant'Anna y Sun-Abraham con wild bootstrap de Webb e inferencia por aleatorización;
- Honest DiD;
- rdrobust en RD difuso y diferencia en discontinuidades;
- shift-share con AKM y AKM0, y F efectivo con AR;
- proyecciones locales y SVAR-IV;
- CIPS con valores críticos por bootstrap, Westerlund y CS-ARDL;
- GSADF por provincia con corrección múltiple;
- Conley;
- BH jerárquico (tasa de falsos descubrimientos real en la rejilla con nulos simulados);
- jerárquico bayesiano (cobertura);
- GRF y DML;
- MIDAS, intervalos conformes y MCS.

## 7. Recuento del multiverso
| Bloque | Especificaciones |
|---|---|
| Q1a RD: 3 anchos × 2 núcleos × 2 polinomios × 2 resultados | 24 |
| Q1b SDID/ASCM: 2 estimadores × 2 conjuntos de donantes × 3 resultados × 2 ventanas | 24 |
| Q1c desplazamiento a la venta: 2 resultados × 2 estimadores × 2 ventanas | 8 |
| Q2a shift-share: 2 niveles × 2 resultados × 2 normalizaciones × 2 conjuntos de orígenes × 2 efectos temporales | 32 |
| Q2b Andalucía: 2 resultados × 2 dosis × 2 ventanas | 8 |
| Q2c INE-VUT × IPVA: 2 resultados × 2 exposiciones × 2 agrupaciones | 8 |
| Q3: 3 resultados (alquiler, compraventas, valor tasado) × 2 normalizaciones × 2 conjuntos de orígenes × 2 años base × 2 efectos temporales; barrio: 2 × 2 × 2 | 56 |
| Q4: 2 restricciones × 2 resultados × 2 periodos × 2 especificaciones | 16 |
| Q5: 4 resultados × 4 horizontes × 2 choques × 2 rezagos | 64 |
| Q6: 2 estimadores × 2 resultados × 2 fechas × 2 ventanas | 16 |
| Q7a: 3 anchos × 2 resultados | 6 |
| Q9: 3 estimadores × 2 medidas de precio × 2 con y sin coste de uso × 3 rezagos, más GSADF de 38 provincias × 2 ratios | 112 |
| Q10: 5 modelos × 3 objetivos × 2 horizontes × 2 tratamientos de 2020 | 60 |
| Rejilla multiescala (sección 4) | 1.164 |
| Holgura para desviaciones declaradas (cada una con su motivo en desviaciones_v16.md) | 2.402 |
| **Total máximo V16** | **4.000** (≤ 50.000; con V15, 8.104) |

## 8. Qué no se hará
- No se elegirá ninguna especificación por su p-valor.
- No se rebajará el criterio de la sección 1 para convertir en confirmatoria una pregunta exploratoria.
- No se usará SHAP ni ninguna importancia para lenguaje causal.
- No se abrirá ninguna muestra sellada (v6, V15, V16) fuera de src/holdout.py, ni más de una vez por pregunta.
- No se publicará un resultado de V16 que contradiga una conclusión de la 1.0 sin parada previa (plan, sección D).
- No se describirá este documento como pre-registro depositado.
