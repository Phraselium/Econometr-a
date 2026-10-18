## Anexos

Este bloque reúne los métodos, las pruebas superadas y fallidas por resultado, los pre-registros, las desviaciones y las licencias. Los anexos de erratas y de reproducibilidad van aparte.

### A. Métodos

Aquí se resume lo esencial. El detalle está en metodologia/ y en la ficha de cada cifra (metodologia/anexo_metodologico.md).

**Capas y escala de evidencia.** Cada cifra lleva una capa: [C1] hecho con al menos dos fuentes independientes; [C2] cota con supuestos explícitos; [C3] y [C3s] resultado con identificación; [C4] exploratorio o descriptivo. Una capa nunca sube. La escala de evidencia va de mayor a menor: identificación (C3 y C3s), asociación robusta, exploratorio, descriptivo. Todo V15 y V16 es [C4]. Definiciones en metodologia/capas.md. <!-- check:cifra-libre (nombres de capa y de versión) -->

**Pre-especificación.** Las especificaciones principales, el multiverso y las pruebas se fijan antes de estimar, en un pre-registro interno (apartado C). Ningún modelo se elige por su p-valor. Toda especificación probada va al registro del proyecto. La regla es anotar las desviaciones antes de ver el resultado afectado; la desviación D9 no la cumple y así se declara en el apartado C. <!-- check:cifra-libre (desviación D9) -->

**Validación de herramientas por Monte Carlo.** Una herramienta de inferencia solo se usa si pasa la validación con el proceso generador del proyecto: pocos clusters, dependencia transversal, T corto, adopción escalonada y correlación espacial. Casi ninguna herramienta de inferencia la pasó. Los resultados están en metodologia/validacion_montecarlo_v16.md y metodologia/validacion_montecarlo_v15.md. <!-- check:cifra-libre (nombres de versión) -->

- **Utilizables en V16:** SDID con Conley-Taber en el escenario A (en el límite superior del tamaño); GSADF sobre el factor con bootstrap salvaje; Benjamini-Yekutieli en lugar del BH jerárquico; TOST solo cuando Δ/EE ≥ 2. <!-- check:cifra-libre (versión y umbral Δ/EE ≥ 2 del diseño) -->
- **Utilizables en V15:** SAR, SDM y SEM con Wald de ρ. <!-- check:cifra-libre (versión) -->
- **DM-HLN (estado único).** Apto bajo el proceso generador de V15 y no apto bajo el de V16. No se usa como prueba en ningún resultado. <!-- check:cifra-libre (nombres de versión) -->
- **No aptas, solo descriptivas:** CS con Webb, dCDH, rejilla TWFE, shift-share con AKM, DiD de intensidad, proyección local con Newey-West de ancho fijo, BLP/GATES, CIPS, CS-ARDL, bayesiano jerárquico, Honest DiD, control sintético, Westerlund y Clark-West.
- **Conley a dos kilómetros** pasó a no apto tras corregir un error en el núcleo (réplica ciega). Q3-b y H3 quedan solo con estimación puntual. <!-- check:cifra-libre (ids de resultado) -->
- Con una herramienta no apta, el resultado se da como estimación puntual, sin p ni intervalo.

**Control de falsos descubrimientos.** Benjamini-Yekutieli con q = 0,10 y denominador fijo por rama: 21 pruebas en la rama de diseños y 83 celdas en la rejilla. Las pruebas sin p válido cuentan en el denominador y no pueden rechazarse. Para las hipótesis de V15, Holm sobre la familia confirmatoria. Solo un p con q ≤ 0,10 abre la puerta a un hallazgo; además se exigen una magnitud plausible y la réplica en la muestra sellada. <!-- check:cifra-libre (q = 0,10, 21 y 83: números del diseño; versión) -->

**Comprobaciones de que el resultado es correcto.**
- Réplica ciega: otro analista reimplementa desde la ficha, sin leer el código. Si discrepa, no se publica hasta resolver. El cegado fue parcial (decisión K19): en varios lotes el replicador vio los valores publicados antes de estimar, y consta en cada resultado.json. <!-- check:cifra-libre (decisión K19) -->
- Abogado del diablo: tres revisiones de solo lectura intentan romper cada resultado citable. Cada objeción se corrige, se contrasta con datos o se declara como limitación (output/v16/critica/respuestas.md). <!-- check:cifra-libre (tres revisiones del diseño) -->
- Triangulación: comparación de signo con otros diseños y con la literatura. Ningún grupo de la literatura reúne estudios comparables para un metaanálisis. Las fichas llevan la etiqueta «DOI verificado; cuartil no verificado» y casi todas se leyeron en resumen.
- Detalle y resultados en el anexo de reproducibilidad.

**Muestras selladas.** Ninguna se ha abierto. Las evaluaciones de V15 se harán según su calendario, una vez por hipótesis y solo a través de src/holdout.py. evaluate_v16 no aplica: ninguna pregunta de V16 cumple las condiciones del hallazgo, así que V16 no tiene evaluación sellada pendiente. <!-- check:cifra-libre (nombre de versión y de fichero) -->

**Neutralidad.** Se evalúan afirmaciones e instrumentos con la misma vara. No se evalúan partidos ni personas.

### B. Pruebas superadas y fallidas por resultado

Todos los resultados de esta sección son [C4]. «Superada» y «fallida» se refieren a pruebas puntuales, porque casi ninguna herramienta de inferencia pasó el Monte Carlo. Una prueba «no evaluable» no cuenta como superada. El pre-registro de cada resultado es interno, sin sello de tiempo externo.

#### B.1 Resultados de V15 <!-- check:cifra-libre (nombre de versión) -->

##### H1 · Zonas tensionadas y renta de contratos nuevos <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la declaración de zona tensionada (Cataluña, Ley 12/2023) con la renta media de los contratos nuevos? <!-- check:cifra-libre (número de ley) --> |
| Diseño | Callaway-Sant'Anna y SDID por cohortes, estimación puntual. Incasòl trimestral, municipios, entrenamiento. |
| Capa | [C4], descriptivo. Pista solo en el signo, sin magnitud. |
| Superadas | El signo se mantiene al excluir Barcelona y el decil superior, y al excluir la capital de la provincia de Barcelona (CS y SDID). Soporte común de donantes suficiente. La réplica ciega coincide. |
| Fallidas o no evaluables | Pretendencias de CS. Contraste SDID de los dos últimos trimestres previos. Placebo temporal (CS y SDID). Control sintético de los diez mayores municipios, con mediana de signo contrario. Las cotas de Lee no permiten citar magnitud. Honest DiD, potencia de Roth, Webb y placebo SDID: no evaluables, por herramienta no apta. <!-- check:cifra-libre (diez municipios del diseño) --> |
| Pre-registro | Interno, sin sello de tiempo externo: etiqueta prereg-v15 en el remoto, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### H2 · Zonas tensionadas y número de contratos <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la declaración de zona tensionada con el número de contratos nuevos? |
| Diseño | PPML con efectos de municipio y trimestre, más CS y SDID sobre log(1+n) como robustez. Puntual. <!-- check:cifra-libre (log(1+n): fórmula de la transformación) --> |
| Capa | [C4], descriptivo. No se cita como pista. |
| Superadas | Contraste SDID de los dos últimos trimestres previos y placebo temporal de SDID, compatibles. Placebo espacial de CS, dentro de la escala permutada. |
| Fallidas o no evaluables | Pretendencias de CS y placebo temporal de CS. El rango del multiverso de CS incluye ambos signos. Ceros imputados. Sin inferencia válida. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### H3 · Vivienda turística y alquiler por sección <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | Dentro de cada sección, ¿se asocia el porcentaje de viviendas turísticas con el alquiler declarado (SERPAVI, stock de contratos)? |
| Diseño | MCO con efectos fijos de sección y de municipio × año. Exposición estandarizada por la desviación típica intra-sección. Puntual. |
| Capa | [C4], descriptivo. No concluyente, no nula. |
| Superadas | El signo se mantiene al excluir las grandes ciudades y el uno por ciento superior de exposición. La réplica ciega coincide. |
| Fallidas o no evaluables | Coeficiente principal ({{V15-H3-beta:sig}} % por desviación típica) por debajo del efecto mínimo detectable ({{V15-H3-mde:sig}} % por desviación típica). Mediana del multiverso: {{V15-H3-rango:sig}} % por desviación típica. Conley a dos kilómetros: no apto. Error agrupado por municipio en panel corto: sin validar. Placebo de adelanto sin inferencia válida. Muchas secciones sin variación intra-sección. Valor de Cinelli-Hazlett prácticamente nulo. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. Réplica, no confirmatoria. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### H4 · Inmigración y alquiler municipal <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la población extranjera predicha por cuotas de origen con el alquiler municipal? |
| Diseño | 2SLS shift-share (cuotas de 2003 × crecimiento nacional sin la provincia), efectos de provincia × año. Puntual. <!-- check:cifra-libre (año base del diseño) --> |
| Capa | [C4]. Correlación frágil: {{V15-H4-beta:num}} % por punto porcentual. |
| Superadas | Primera etapa fuerte en términos descriptivos (F robusto {{V15-H4-F:num}}). Balance de 2003 cercano a cero. El signo se mantiene al excluir Barcelona y València y el uno por ciento superior de exposición. La réplica ciega, tras corregir la muestra, coincide. <!-- check:cifra-libre (año) --> |
| Fallidas o no evaluables | Cambia de signo al quitar los cinco orígenes de mayor peso. Número efectivo de choques bajo ({{V15-H4-neff:num}}). AKM, AKM0 y agrupación por provincia: no aptos. Con el control del instrumento retardado, la estimación cae a casi cero. Con 28 orígenes, el signo es contrario. Sin p ni intervalo. Mediana del multiverso: {{V15-H4-mediana:num}} % por punto porcentual [C4]. <!-- check:cifra-libre (número de orígenes del diseño) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### H5 · Predicción del valor tasado nacional <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Predice la combinación el Δlog trimestral del valor tasado nacional mejor que el AR(4) y el ECM v1, en la misma muestra? <!-- check:cifra-libre (nombres de modelo) --> |
| Diseño | Ventana expansiva, h = 1. Combinación de DFM, BVAR, LASSO y ARDL. DM-HLN unilateral. <!-- check:cifra-libre (horizonte h = 1 del diseño) --> |
| Capa | [C4], predictivo. Pista: la combinación no supera al AR(4). <!-- check:cifra-libre (nombre de modelo) --> |
| Superadas | La réplica ciega, tras corregir tres errores, coincide en la conclusión. Ninguna fila posterior al origen entra en la estimación. En error cuadrático, la combinación queda por delante del ECM v1. <!-- check:cifra-libre (nombre de modelo y número de errores corregidos) --> |
| Fallidas o no evaluables | Razón del ECM frente al AR(4): mayor que uno en todas las implementaciones. Rango entre implementaciones (réplica ciega y producción pre-registrada): {{V15-H5-razon-replica:min_num}} a {{V15-H5-razon-replica:max_num}} [C4]. La pre-registrada: {{V15-H5-razon-ecm:num}} [C4]. DM-HLN: sin valor probatorio (estado en el apartado A). Clark-West y Giacomini-White: no aptos. MCS: descriptivo. Potencia inferior a la pre-registrada (menos errores). <!-- check:cifra-libre (nombres de modelo) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. Evaluación sellada hacia octubre de 2027. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### E1 · Largo plazo entre valor tasado y alquiler (panel provincial) <!-- check:cifra-libre (id de análisis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Hay una relación de largo plazo entre el valor tasado y el alquiler en las provincias de entrenamiento? |
| Diseño | ECM por unidad: CS-ARDL, MG y PMG. Todo puntual. |
| Capa | [C4], descriptivo. |
| Superadas | Ninguna prueba de inferencia aplicable. |
| Fallidas o no evaluables | Westerlund, CIPS y CS-ARDL: no aptos. PMG con coste de uso: no identificado. Elasticidad {{V15-E1-theta:num}}, con un rango del multiverso ({{V15-E1-theta:rango}}) que cambia de signo. Semivida del desajuste: {{V15-E1-semivida}}. La cointegración no se contrasta. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### E2 · Presión demográfica no cubierta por la obra y alquiler <!-- check:cifra-libre (id de análisis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia el exceso de hogares sobre la obra con el crecimiento del alquiler? |
| Diseño | Correlaciones de Pearson y Spearman, 24 especificaciones, provincias. <!-- check:cifra-libre (número de especificaciones del diseño) --> |
| Capa | [C4], descriptivo. |
| Superadas | El signo es positivo en todas las especificaciones con dato. |
| Fallidas o no evaluables | Sin intervalo ni herramienta de inferencia. Pocas provincias. Catastro municipal parcial. Regularización catastral previa a 2018. Demografía y población coinciden salvo por la escala. <!-- check:cifra-libre (año) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### E3 · Dependencia espacial del alquiler municipal <!-- check:cifra-libre (id de análisis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Hay dependencia espacial en el crecimiento del alquiler municipal (SERPAVI)? |
| Diseño | SAR, SEM y SDM por máxima verosimilitud, con W de contigüidad y de distancia inversa. |
| Capa | [C4], asociación espacial exploratoria. |
| Superadas | Wald de ρ: herramienta apta. Moran positivo en dos ventanas y con dos matrices W. El resultado se mantiene al excluir Barcelona y València. La réplica ciega coincide. ρ = {{V15-E3-rho:num}}, con rango de multiverso {{V15-E3-rho:rango}}. |
| Fallidas o no evaluables | ρ puede recoger una tendencia regional común, no contagio. El intervalo subestima la incertidumbre de especificación; se cita el rango del multiverso. Selección de la muestra por vecinos. Los efectos indirectos del SDM dependen de W. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### E4 · Turismo con periodo previo y alquiler (Cataluña y Comunitat Valenciana) <!-- check:cifra-libre (id de análisis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la exposición turística, con periodo previo, con el alquiler en un estudio de eventos de dosis continua? |
| Diseño | Efectos fijos de municipio y año, referencia 2017. Coeficientes puntuales. <!-- check:cifra-libre (año de referencia) --> |
| Capa | [C4], exploratorio. |
| Superadas | Regla puntual de pretendencias: la cumplen {{V15-E4-compat:num}} de {{V15-E4-compat:max}}. |
| Fallidas o no evaluables | La incumplen las demás especificaciones. Honest DiD y potencia de Roth: no evaluables. La exposición del registro valenciano está reconstruida: solo robustez. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

#### B.2 Resultados de V16 <!-- check:cifra-libre (nombre de versión) -->

V16 no añade hipótesis confirmatorias (desviación D1) y todo es [C4]. Pre-registro interno de V16, sin sello de tiempo externo: etiqueta prereg-v16 en el remoto, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (versión, desviación, etiqueta, hash y fecha) -->

##### Q1 · Zonas tensionadas (Q1a, Q1b, Q1c) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué diferencia hay, en el entrenamiento, entre mercados con y sin zona tensionada declarada? |
| Diseño | Q1a: recuento de elegibilidad (art. 18). Q1b: SDID con Conley-Taber. Q1c: Callaway-Sant'Anna sin regresores sobre compraventas provinciales. <!-- check:cifra-libre (ids de pregunta y artículo) --> |
| Capa | [C4], descriptivo. Sin hallazgo ni pista. Q1c no se cita con cifras. <!-- check:cifra-libre (id de pregunta) --> |
| Superadas | Q1c: el signo se mantiene al excluir las grandes ciudades. Valor de Cinelli-Hazlett por encima del umbral de fragilidad. Moran y Breusch-Pagan sin señal. <!-- check:cifra-libre (id de pregunta) --> |
| Fallidas o no evaluables | Q1b: sin periodo posterior al tratamiento (2025 es el primer inicio fuera de Cataluña) y sin potencia. Q1c: Oster indica fragilidad; el balance entre tratadas y no tratadas es muy desigual; Bai-Perron encuentra rupturas antes del primer tratamiento. CS con Webb y BLP/GATES: no aptos. Honest DiD y controles negativos: no evaluables. <!-- check:cifra-libre (ids de pregunta y año) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q2 · Vivienda turística (Q2a, Q2b, Q2c) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué asociación hay entre la exposición a vivienda turística y la evolución del alquiler? |
| Diseño | Q2a: DiD de intensidad provincial en forma reducida. Q2b: Andalucía, solo robustez. Q2c: IPVA municipal con efectos fijos de municipio y año (especificación de la adenda tras la corrección K17). <!-- check:cifra-libre (ids de pregunta y decisión) --> |
| Capa | [C4], descriptivo. Q2a, no concluyente. Q2c, de signo inestable y sin cita. <!-- check:cifra-libre (ids de pregunta) --> |
| Superadas | Q2a: Oster y Cinelli-Hazlett pasan; el signo se mantiene al excluir las grandes ciudades; Moran y Breusch-Pagan sin señal. Q2c: Cinelli-Hazlett pasa. <!-- check:cifra-libre (ids de pregunta) --> |
| Fallidas o no evaluables | Q2a: DiD de intensidad con Webb, no apto; Honest DiD, no evaluable; ruptura de Bai-Perron en la brecha entre terciles; shift-share retirado por falta de pernoctaciones por país. Q2c: Oster falla; heterocedasticidad; signo opuesto al de la literatura. BLP/GATES: no apto. <!-- check:cifra-libre (ids de pregunta) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q3 · Inmigración, más allá de H4 (Q3-c1, Q3-c2, Q3-b, BLP/GATES) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la población extranjera con el valor tasado, las compraventas y el alquiler por sección? |
| Diseño | Shift-share de forma reducida en provincias (Q3-c) y correlación transversal por sección con efectos de municipio (Q3-b). Puntual. <!-- check:cifra-libre (ids de pregunta) --> |
| Capa | [C4]. Q3-b, correlación frágil: {{V16-Q3-b-beta:sig}} (log por desviación típica). <!-- check:cifra-libre (id de pregunta) --> |
| Superadas | Q3-b: Oster y Cinelli-Hazlett no indican fragilidad; el signo se mantiene al excluir las grandes ciudades; la réplica ciega queda resuelta tras corregir Conley. Q3-c: mismo signo en todo el multiverso. <!-- check:cifra-libre (ids de pregunta) --> |
| Fallidas o no evaluables | Q3-b: pretendencia del mismo orden ({{V16-Q3-b-pretendencia:sig}}); Conley, no apto; Moran de residuos con señal; desequilibrio de renta. Q3-c: AKM y AKM0, no aptos; el origen de mayor peso aporta una fracción {{V16-Q3-rotemberg-1:num}} del estimador; los signos de Q3-c1 y Q3-c2 son opuestos. BLP/GATES: no apto (diferencia de GATES, cuartil 4 menos 1: {{V16-Q3-blp-gates:sig}}). Mediana del multiverso de Q3-b: {{V16-Q3-b-mediana:sig}} [C4], menor que el coeficiente principal. <!-- check:cifra-libre (ids de pregunta) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q4 · Oferta y restricción física (Q4a, Q4b) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia el porcentaje de Red Natura con la obra nueva neta, y con la respuesta del alquiler al choque de demanda de Q3? <!-- check:cifra-libre (id de pregunta) --> |
| Diseño | Q4a: MCO con efectos de provincia y año. Q4b: primeras diferencias con interacción choque × Red Natura. Puntual. <!-- check:cifra-libre (ids de pregunta) --> |
| Capa | [C4], descriptivo. Sin hallazgo. |
| Superadas | Q4a y Q4b: el signo se mantiene al excluir las grandes ciudades. Q4a: el signo se mantiene en el periodo de regularización catastral. <!-- check:cifra-libre (ids de pregunta) --> |
| Fallidas o no evaluables | Q4a: dependencia espacial fuerte en los residuos. Q4b: placebo de choque adelantado con el mismo signo y mayor tamaño. La Red Natura no es exógena. Agrupación provincial, no apta. Costa, pendiente, agua y planeamiento: sin datos. <!-- check:cifra-libre (ids de pregunta) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q5 · Sorpresas monetarias <!-- check:cifra-libre (id de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocian las sorpresas monetarias (Jarociński-Karadi) con el valor tasado y el IPC de alquiler a cuatro trimestres? |
| Diseño | Proyección local con cuatro rezagos. Puntual. |
| Capa | [C4], descriptivo. No se cita como pista. |
| Superadas | Ninguna prueba de inferencia aplicable. |
| Fallidas o no evaluables | Proyección local con Newey-West de ancho fijo, no apta. Autocorrelación de residuos. Primera etapa de signo equivocado. El multiverso no apoya el signo. El placebo es comparable y la respuesta cambia de signo. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q6 · Fiscalidad de la compra (Q6-v, Q6-p) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocian los cambios del tipo general del ITP con las compraventas y el valor tasado? |
| Diseño | Wald-DID (de Chaisemartin y D'Haultfœuille) con dosis continua, panel provincial anual. Solo puntual. Diferencias entre años consecutivos (corregido en la réplica ciega). |
| Capa | [C4]. Q6-p, no concluyente: {{V16-Q6-p-beta:sig}} log por punto de tipo. Q6-v, descriptivo, sin cifra. <!-- check:cifra-libre (ids de pregunta) --> |
| Superadas | Q6-p: placebo de ΔY retardado pequeño y signo estable sin las grandes ciudades. Control negativo con la población, cercano a cero. <!-- check:cifra-libre (id de pregunta) --> |
| Fallidas o no evaluables | Q6-v: placebo mayor y de signo contrario; signo opuesto a la referencia. Los {{V16-Q6-cambios:num}} cambios se concentran en 2012-2013. Inferencia por aleatorización, Honest DiD, Cinelli-Hazlett y TOST: no evaluables. Compraventas = total de vivienda. <!-- check:cifra-libre (id de pregunta y años) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q7 · Ayudas al alquiler joven <!-- check:cifra-libre (id de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Cambió en el corte de edad del bono la diferencia de alquiler pagado entre inquilinos de mercado, entre dos periodos? |
| Diseño | Diferencia en discontinuidades lineal local con pesos de la encuesta, anchos de tres, cinco y siete años. Sin intervalo. |
| Capa | [C4], descriptivo: valor {{V16-Q7-1:valor}}; rango de especificaciones {{V16-Q7-1:rango}}. Sin hallazgo ni pista. |
| Superadas | Los anchos de tres, cinco y siete años dan el mismo signo. |
| Fallidas o no evaluables | Los umbrales placebo dan resultados del mismo orden (valor {{V16-Q7-4:valor}}; rango {{V16-Q7-4:rango}}), así que el resultado no se lee como específico del corte. Potencia en el límite. Sin intervalo (Kolesár-Rothe no mostrado). Edad discreta: sin rdrobust. El Plan Estatal 2018-2021 ya tenía un programa para menores de 35 años: se mide un cambio de generosidad, no un programa nuevo. Oster, Cinelli-Hazlett y exclusión de grandes ciudades: no aplican o no son evaluables. <!-- check:cifra-libre (periodo del plan y umbral de edad) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q8 · Compras de no residentes <!-- check:cifra-libre (id de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Cómo ha evolucionado la cuota de compras de no residentes antes y después de abril de 2025? |
| Diseño | Descriptivo: cuotas y niveles por trimestre y comparación de ventanas de cuatro trimestres. |
| Capa | [C4], descriptivo. Variación de la cuota: {{V16-Q8-3:valor}}. |
| Superadas | No hay contraste de hipótesis. La comparación con el año anterior se declara. |
| Fallidas o no evaluables | La fuente no separa UE de extra-UE. No identifica los visados de oro. Sin autorizaciones por programa. Sin placebo ni diferencias en diferencias. La cuota de Q8 (Boletín en línea, agregado de entrenamiento) difiere de la de R1A-H1 (tabla 1.6, España) por fuente y ventana. <!-- check:cifra-libre (id de resultado y tabla 1.6) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q9 · Fundamentales y burbuja (Q9-g, Q9-c) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Hay exuberancia en el factor común del cociente valor tasado / IPC de alquiler, y qué elasticidad de largo plazo hay entre ambos? |
| Diseño | Q9-g: GSADF con bootstrap salvaje. Q9-c: CS-ARDL, MG, PMG y CIPS, puntuales. <!-- check:cifra-libre (ids de pregunta) --> |
| Capa | [C4], pista no confirmada. Solo en la Parte VII. <!-- check:cifra-libre (número de parte) --> |
| Superadas | Calibración del GSADF del factor con bootstrap salvaje (tamaño aceptable). Réplica ciega: coincide. |
| Fallidas o no evaluables | Q9-g: estadístico {{V16-Q9-g:num}}; valor crítico del 95 % {{V16-Q9-g:min_num}}; p sin ajuste {{V16-Q9-gp:sig}}. q de Benjamini-Yekutieli: {{V16-FDR-Q9-g-q:sig}}, por encima del umbral. Heterocedasticidad de la variación del factor. Potencia limitada. Fechas marcadas en tramos en que el cociente baja o está plano. La alternativa con SERPAVI anual no rechaza y no tiene potencia. Q9-c: CS-ARDL no apto; el rango del multiverso incluye ambos signos (estimación {{V16-Q9-c:num}}, rango {{V16-Q9-c:rango}}). CIPS: descriptivo, sin valor crítico. <!-- check:cifra-libre (ids de pregunta y nivel del 95 %) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q10 · Predicción nacional (Q10-1, Q10-2, Q10-3) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Mejoran MIDAS y el nowcasting al AR(4) y al ECM v1 en la predicción a un trimestre del IPV, del IPC de alquiler y de las compraventas? Alcance: agregado nacional trimestral. <!-- check:cifra-libre (nombres de modelo) --> |
| Diseño | Ventana expansiva. Razones de ECM. Intervalos conformes. |
| Capa | [C4], descriptivo. Las cifras de Q10 no se citan. <!-- check:cifra-libre (id de pregunta) --> |
| Superadas | Frente al ECM v1 reducido, el AR(4) es mejor en el IPV. Cobertura empírica de los intervalos conformes cercana a la nominal en el nowcasting del alquiler. <!-- check:cifra-libre (nombres de modelo) --> |
| Fallidas o no evaluables | Q10-1: MIDAS no mejora al AR(4). Q10-2: el nowcasting tampoco. Q10-3: la mejora aparente sale de 2020 y desaparece al excluirlo. DM-HLN: sin valor probatorio (estado en el apartado A). Clark-West: no apto. Datos revisados, no en tiempo real. <!-- check:cifra-libre (ids de pregunta, modelo y año) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Rejilla fija multiescala

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué asociación puntual hay en cada celda de la rejilla de escalas × resultados para Q1, Q2, Q3, Q4 y Q6? <!-- check:cifra-libre (ids de pregunta) --> |
| Diseño | 83 celdas, TWFE con efectos de unidad y periodo, cinco variantes por celda. Estimación puntual. <!-- check:cifra-libre (celdas del diseño) --> |
| Capa | [C4], descriptivo. Sin hallazgo local. |
| Superadas | Cada celda se estimó. El signo mediano se mantiene entre variantes. |
| Fallidas o no evaluables | TWFE, no apto (tamaño y cobertura fuera de rango): ninguna celda tiene p válido. Los diagnósticos de diseño no se ejecutan por celda. Cuentan en el denominador de Benjamini-Yekutieli y no pueden rechazarse. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Control de falsos descubrimientos, triangulación y potencia (V16) <!-- check:cifra-libre (nombre de versión) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué pruebas sobreviven al control, coinciden entre diseños y con la literatura, y con qué potencia se diseñaron? |
| Diseño | Benjamini-Yekutieli por rama. Comparación de signo entre diseños y con la literatura. Potencia por aleatorización placebo. |
| Capa | [C4], descriptivo. |
| Superadas | Solo una prueba de la rama de diseños tiene p válido (Q9-g). H1-CS y H1-SDID coinciden en signo, y H3 con Q2a. <!-- check:cifra-libre (ids de análisis) --> |
| Fallidas o no evaluables | Q9-g no pasa el control ({{V16-FDR-Q9-g-q:sig}}). Q2c y Q6-v se apartan de la literatura y quedan descriptivos. H4, Q3-c1 y Q3-b no tienen grupo comparable en la literatura. Ningún grupo permite metaanálisis. Ningún resultado sube de capa por coincidir con la literatura. <!-- check:cifra-libre (ids de análisis) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Fase de hechos y contabilidad (hechos, esfuerzo, contabilidad, atlas)

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué hechos se sostienen con dos fuentes independientes, y cómo se reparte contablemente el cambio de hogares, precio y esfuerzo? |
| Diseño | Cambios acumulados con media anual, coincidencia dentro de una tolerancia de tres puntos o del quince por ciento. Descomposiciones de Shapley, factores dinámicos, Oaxaca-Blinder, DFL y RIF. Atlas descriptivo con supresión de celdas pequeñas. |
| Capa | [C1] solo para tres cifras nuevas (precios 2019-2025 y brecha de alquiler en Cataluña); el resto, [C4]. Descriptivo. El IPV del INE (ajustado por calidad, una sola fuente) se da como [C4] junto a las medidas por m². <!-- check:cifra-libre (periodo y nombres de capa) --> |
| Superadas | Reproducen los controles de la 1.0. Identidad contable de hogares sin error. Esfuerzo de la ECV, compatible con el de Eurostat en los años recientes. |
| Fallidas o no evaluables | ECV y Eurostat son la misma encuesta: no hay [C1] en esfuerzo. Los años antiguos no coinciden con Eurostat. Intervalos aproximados. Vivienda pública por habitante frente a la UE: sin dato descargado. No hay contrastes de hipótesis: no aplica el control de falsos descubrimientos. <!-- check:cifra-libre (nombre de capa) --> |
| Pre-registro | No requiere pre-registro (hechos y contabilidad, sin estimar efectos). Para el resto de V16: interno, sin sello de tiempo externo (prereg-v16, commit a8304ec, 2026-10-17). <!-- check:cifra-libre (versión, etiqueta, hash y fecha) --> |

### C. Pre-registros de V15 y V16

Los dos son internos y no tienen sello de tiempo externo. Una etiqueta git publicada en el remoto no es un sello de tiempo externo. El plan inicial de depositar el pre-registro fuera se sustituyó por esta declaración: el proyecto registra `preregistro_tipo` como «interno, sin sello externo». <!-- check:cifra-libre (versión) -->

| Versión | Etiqueta en el remoto | Commit | Fecha del commit | Etiqueta publicada | Sello externo |
|---|---|---|---|---|---|
| V15 | prereg-v15 | 542b4fd | 2026-10-17 | 2026-10-17 | No | <!-- check:cifra-libre (etiquetas, hashes y fechas del registro de etiquetas) -->
| V16 | prereg-v16 | a8304ec | 2026-10-17 | 2026-10-17 | No | <!-- check:cifra-libre (etiquetas, hashes y fechas del registro de etiquetas) -->

Registro completo, con fechas en UTC y la huella de cada fichero: docs/preregistros.md y docs/preregistros_ficheros.csv. Las etiquetas de las versiones anteriores están en el mismo registro.

**Qué cubre cada uno.**
- **V15.** Cinco hipótesis (H1 a H5) y cuatro análisis exploratorios (E1 a E4). H1, H2 y H4 forman la familia Holm; H3 es una réplica; H5 es predictiva. Las hipótesis no se modifican ni se reformulan. Sus evaluaciones selladas están pendientes (calendario: docs/v15/preregistro_v15_adenda.md, sección C; fecha límite 31-12-2027). <!-- check:cifra-libre (ids de hipótesis y análisis, fecha límite) -->
- **V16.** Diez preguntas (Q1 a Q10) y una rejilla fija de 83 celdas. No añade hipótesis confirmatorias. Todo es [C4] como máximo. La adenda es vinculante. No tiene evaluación sellada pendiente: evaluate_v16 no aplica. <!-- check:cifra-libre (ids de pregunta, celdas y nombre de función) -->

**Desviaciones.** La regla es anotarlas antes de ver el resultado afectado. Se citan por su número, tal como figuran en el fichero de desviaciones.
- **V16** (fuente: docs/v16/desviaciones.md; se publicará en metodologia/desviaciones_v16.md con `make publicacion`; D1 a D9): D1, sin preguntas confirmatorias nuevas; D2, operacionalización forzada por los datos en Q3, Q4 y Q6; D3, precisiones en Q1, Q2, Q7 y Q8; D4, Q5, Q9, Q10 y rejilla; D5, correcciones tras la réplica ciega; D6, correcciones tras la revisión adversarial; D7, Q6 con años consecutivos; D8, GSADF de V7.2 corregido y 4.999 simulaciones; D9, omisiones frente al plan: metaanálisis con Egger y PET-PEESE, modelo bayesiano jerárquico con priors de metaanálisis, GRF y DML, BH jerárquico sustituido por BY, calibración de los cuatro cuadrantes para las grandes áreas urbanas y condición (b) de Gelman-Carlin. <!-- check:cifra-libre (ids de desviación D1 a D9, de pregunta y simulaciones) -->
- **D9 se anotó después de ver los resultados**, el 2026-10-18, tras el arbitraje del informe integral. Incumple, por tanto, la regla de anotar antes. Recoge las omisiones frente al plan que antes solo constaban en docs/v16/decisiones.md y en la adenda. Incluye la calibración de los cuatro cuadrantes para las grandes áreas urbanas, que no se hizo: el marco se calibró solo para España porque no hay series de parque, terminadas y coste de uso por área urbana con la cobertura necesaria. <!-- check:cifra-libre (desviación D9, fecha del registro, cuatro cuadrantes: nombre del marco) -->
- **V15** (docs/v15/desviaciones.md): DV15-A (H1, H2, H3, E4), DV15-B (H4, H5, E1, E2, E3) y DV15-K16 (correcciones tras la réplica ciega). <!-- check:cifra-libre (ids de desviación e hipótesis) -->
- **Versiones cerradas anteriores.** Cambios posteriores a algunos commits de pre-registro: metodologia/desviaciones_preregistros.md. Ninguno cambia una hipótesis ni una cifra de la 1.0. <!-- check:cifra-libre (versión) -->

### D. Licencias

No se inventa ninguna licencia: cada una se toma del registro de la fuente.

- **Qué se publica.** La carpeta publicacion/ la genera `make publicacion`; su inventario y las huellas de cada fichero están en publicacion/MANIFIESTO.md. Las series no redistribuibles no salen del repositorio de desarrollo. La capa pública de la base solo lleva datos redistribuibles.
- **Cifras de terceros de la 1.0.** publicacion/cifras_no_publicadas_1_0.csv recoge las cifras que no se publican, según proyecto.json (campo `terceros_1_0`). <!-- check:cifra-libre (versión) -->
- **Condiciones de uso de Registradores, Notariado y AEAT.** docs/v14/licencias.md, con las cláusulas literales y la clave CLARO, AMBIGUO o NO CONSTA. Es un informe, no una decisión. Atribución exigida para el conjunto abierto de Registradores (compraventas de uso residencial por provincia): Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. <!-- check:cifra-libre (versión de la licencia ODbL y de documento) -->
- **Fuentes nuevas de V16.** docs/v16/inventario_fuentes.csv recoge, por fichero, la edición, la licencia declarada por el proveedor, si es redistribuible (sí, no o dudoso), la huella sha256 y si está versionado. Lo marcado «dudoso» o «no» no se redistribuye. <!-- check:cifra-libre (versión) -->
- **Incasòl (fianzas).** Marcada como no redistribuible en las fuentes de las cifras de V9; solo se publican agregados propios. <!-- check:cifra-libre (versión) -->
- **Huellas de los datos de origen.** data/CHECKSUMS.sha256. <!-- check:cifra-libre (umbrales, categorías y números del diseño; leyes y documentos) -->
- **Literatura.** Las fichas de docs/v16/literatura.md llevan la etiqueta «DOI verificado; cuartil no verificado» (existe en Crossref o DataCite) o «NO VERIFICADA» (sin DOI localizado). Casi todas se leyeron en resumen o en versión de trabajo y son orientativas. <!-- check:cifra-libre (versión) -->
