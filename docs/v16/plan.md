V16 · ESTUDIO INTEGRAL DE LA VIVIENDA Y EL ALQUILER EN ESPAÑA (ampliación de V15)
Objetivo: un informe exhaustivo, científico y honesto, con toda la información disponible y la que falta por conseguir, que sirva para (1) entender el problema de la vivienda y del alquiler, (2) distinguir medidas probadas de propaganda y (3) consultar como manual de referencia para el discurso político crítico. Profundidad máxima en todas las escalas (España, comunidad, provincia, área urbana funcional, municipio, distrito, barrio, sección censal) y dimensiones (tenencia, edad, renta, nacionalidad, tipo y antigüedad de vivienda, obra nueva o usada, contrato nuevo o vigente). La honestidad manda: se publica lo que salga, sea cómodo o incómodo para quien sea, y lo que no se puede saber se dice con la razón. Se evalúan afirmaciones e instrumentos con la misma vara, nunca partidos ni personas.

PRIMER PASO: guarda este mensaje completo, sin resumir, en docs/v16/plan.md, haz commit y cambia en CLAUDE.md la línea de V15 por «V16 en curso (ampliación de V15; pre-registros internos sin sello externo): leer docs/v16/plan.md y docs/v16/estado.md al empezar cualquier sesión o tras compactar». Tras cualquier compactación, vuelve a leer plan.md y estado.md.

══════════════════════════════════════════════
A. REGLAS
══════════════════════════════════════════════
- Lectura previa: CLAUDE.md, proyecto.json, metodologia/ completa, docs/v15/ completa (punto_partida, inventario_variables, auditorías, potencia, literatura, preregistro_v15 y sus dos adendas, contaminacion_v6, cambios_publicacion_web, tareas_autor), docs/v14/licencias.md y docs/limitaciones.md.
- Siguen vigentes todas las reglas del repositorio:
  - capas C1/C2/C3/C3s/C4 sin promoción;
  - sin lenguaje causal fuera de C3/C3s;
  - ningún modelo elegido por p-valor;
  - Holm para confirmatorias y BH para exploratorias;
  - Registry;
  - AR(4) y ECM v1 como líneas base en la misma muestra;
  - cruces solo por código INE;
  - interpolaciones solo en robustez;
  - reporte de discrepancias entre métodos.
- Pre-registro interno, sin sello externo: los pre-registros de V15 (etiqueta prereg-v15, commit 542b4fd) y V16 (etiqueta prereg-v16) se fijan con etiquetas git publicadas en el remoto antes de estimar. H1-H5 de V15 no se modifican ni se reformulan y se evalúan según su calendario (H1/H2 hacia marzo de 2027, H5 hacia octubre de 2027, H4 en el último trimestre de 2027). Solo es confirmatorio lo publicado después del corte del 17-10-2026; lo ya visto es informativo. En todos los textos, estos resultados se describen como «pre-registro interno sin sello de tiempo externo», nunca como pre-registro depositado.
- La 1.0 no cambia de valor; solo se permiten bajadas de capa y correcciones de metadatos documentadas en ERRATA (check_v8, check_v9 y check_v13). V16 añade cifras V16-* y se publicará como 2.0.
- No se leen fuera de src/holdout.py: data/sealed, la evaluación de 2027, las muestras selladas de V15 y las filas marcadas muestra_sellada_v6. Prohibido make clean, make all, make v7 y make evaluate_v7. Ficheros con Write o heredoc entrecomillado. Un solo make check a la vez.
- Terceros según proyecto.json (terceros_1_0): solo agregados propios de fuentes con condiciones ambiguas; ninguna serie no redistribuible sale del repositorio de desarrollo. Cada fuente nueva pasa por el registro de licencias antes de usarse.
- Excel: azul los datos introducidos (con su fuente en nota), negro lo calculado en la hoja, verde lo que viene de otra pestaña. Sin paneles inmovilizados. Maquetación limpia.
- Trabajo en docs/v16/ (plan, estado, decisiones, bloqueos, tareas_autor), src/v16/, output/v16/ y tests/v16/. Estado tras cada tarea (hecho, siguiente, subagentes, tokens). Commit por tarea; push solo a la rama designada.
- Presupuesto: informa de los tokens por fase en estado.md. Si una fase supera 6 millones de tokens de subagentes, para y explícame en qué se han ido y cuánto falta.

══════════════════════════════════════════════
B. INFRAESTRUCTURA (reutiliza la de V15 y amplíala)
══════════════════════════════════════════════
B1. Guardas:
   - Mantén las de V15, pero cambia la guarda (d), que exigía osf_prereg_v15: ahora exige que la etiqueta prereg-v15 exista en el remoto y apunte a 542b4fd.
   - Añade un hook que rechace make v16_f5* y posteriores si la etiqueta prereg-v16 no existe en el remoto.
   - Añade a check_v16 un control que falle si algún commit con estimaciones de V15 o V16 es anterior a su etiqueta.
   - Tests en tests/v16/test_guardas.py. Intenta tú saltarte cada guarda y confirma que falla.

B2. Subagentes nuevos en .claude/agents/, además de los de V15:
   - adquisidor-datos (sonnet; WebSearch, WebFetch, Bash, Write en data/raw/v16 y docs/v16/fuentes/): descarga una familia de fuentes, registra endpoint, edición, fecha, licencia y checksum; nunca hace scraping que vulnere condiciones de uso.
   - ingeniero-datos (sonnet): normaliza al formato largo de la base con códigos INE, unidades y rupturas declaradas.
   - replicador-ciego (sonnet; sin acceso a src/v16/pX ni a output/v16/pX): reimplementa un análisis solo desde su ficha del pre-registro y compara.
   - abogado-del-diablo (opus; solo lectura): intenta romper cada resultado candidato con explicaciones alternativas, datos que lo contradigan y fallos de diseño.
   - redactor (sonnet; Read, Write solo en output/v16/informe/): redacta solo desde resultado.json y cifras_clave, sin añadir números.
   - verificador-cifras (haiku; solo lectura y python): comprueba que cada número del informe existe en cifras_clave con su id, capa y periodo.
   Si algún modelo no está disponible, el más cercano, anotado en decisiones.

B3. Comandos /v16-fase0 … /v16-fase7 y /v16-estado en .claude/commands/, y objetivos make v16_f0 … v16_f7, v16 y check_v16 dentro de make check. Cada fase declara qué va en paralelo (como máximo 3 subagentes que escriben, en worktrees ../wt-v16-<tarea>; los de solo lectura pueden ser más) y termina con make check en solitario, commit, push y resumen.

══════════════════════════════════════════════
C. FASES
══════════════════════════════════════════════
FASE 0 · Punto de partida
1. Publica en el remoto del repositorio de desarrollo la etiqueta prereg-v15 (commit 542b4fd) y las demás etiquetas prereg-* locales, y comprueba que existen. Elimina osf_prereg_v15 y osf_prereg_v16 de proyecto.json, de los controles y de tareas_autor.md, y añade preregistro_tipo: "interno, sin sello externo".
2. Comprueba que siguen aplicadas las correcciones previas: filas v6 marcadas, 11 bajadas de capa, tres metadatos corregidos y make check limpio.
3. Una página: tras las 11 bajadas de C1 a C4, reescribe la plantilla de origen de una_pagina.md para que su estructura refleje qué es un hecho con dos fuentes independientes y qué es una estadística oficial de fuente única. No cambies ningún valor; muéstrame el antes y el después en el resumen de la fase.
4. docs/v16/lo_ya_visto.md: conclusiones de V5-V15 con su estimación y sus pruebas (V8, V9-D1, V9-D4, V12 y auditorías de V15). Todo pre-registro de V16 las declarará.

FASE 1 · Material crudo que falta (en paralelo: hasta 3 adquisidor-datos por familia; lo que requiera al autor va a tareas_autor.md al principio y la fase sigue con lo demás)
Comprueba disponibilidad, licencia y cobertura de cada fuente antes de descargar. Prioriza por valor para las preguntas.
- Renta y hogares: Atlas de Distribución de Renta de los Hogares del INE (sección censal, toda la serie); EPF (microdatos, gasto en vivienda); ECV (microdatos, todas las olas); Censo 2021 (microdatos y viviendas no principales y vacías por sección); EFF del Banco de España (acceso por solicitud: tareas_autor).
- Parque y vacías: estadística experimental del INE de viviendas vacías por consumo eléctrico; estadísticas catastrales municipales; descarga masiva alfanumérica del Catastro (datos no protegidos; requiere registro con certificado: tareas_autor) para el parque por año de construcción, uso y superficie.
- Oferta y suelo (reabre P1):
  - Sistema de Información Urbana del MIVAU (suelo urbano y urbanizable por municipio);
  - MDT del IGN (pendientes); SIOSE y CORINE (usos del suelo); Red Natura 2000 y dominio público (MITECO); costas;
  - visados de dirección de obra y certificados de fin de obra; licencias;
  - índices de costes de construcción del INE; valor del suelo urbano del MIVAU;
  - calificaciones de vivienda protegida y parque público (MIVAU, GVA, Generalitat de Catalunya, Comunidad de Madrid).
- Demanda y financiación:
  - tipos y volúmenes de nuevas operaciones hipotecarias (Banco de España); hipotecas por provincia (INE);
  - compras por extranjeros por nacionalidad y por personas jurídicas (agregados de Registradores y Notariado según su licencia);
  - base de sorpresas de política monetaria del BCE (Euro Area Monetary Policy Event-Study Database o Jarociński-Karadi) como instrumento externo.
- Alquiler y turismo:
  - InsideAirbnb (CC BY 4.0) para todas las ciudades españolas disponibles;
  - registros autonómicos de viviendas turísticas (GVA, Catalunya, Madrid, Andalucía, Baleares, Canarias);
  - registro único de arrendamientos de corta duración si publica datos;
  - fianzas por tipo de contrato donde se distinga temporada;
  - EOAT y pernoctaciones.
- Tensión social: lanzamientos del CGPJ por partido judicial y causa (alquiler o hipoteca); paro y afiliación municipales; migraciones (EVR, padrón continuo).
- Portales: datos de idealista o Fotocasa solo por acuerdo o API con licencia (tareas_autor); nunca scraping contra sus condiciones.
- Comparación internacional: OCDE (indicadores analíticos de precios de vivienda), Eurostat (HPI, sobreesfuerzo, tenencia) y BIS (precios reales).
- Base de intervenciones (imprescindible; la construyes tú): calendario fechado y por territorio de cada medida, con su fuente normativa (BOE, diarios autonómicos y municipales):
  - Ley 12/2023 y declaraciones de zona tensionada con sus criterios;
  - tope del 2 % y 3 % de actualización de rentas;
  - bono alquiler joven y sus requisitos;
  - avales ICO;
  - planes estatales;
  - cambios del ITP y del AJD por comunidad y año (fuente: panorama de fiscalidad autonómica del Consejo General de Economistas);
  - recargos del IBI a vacías;
  - moratorias y planes de vivienda turística (PEUAT de Barcelona y sus zonas, València, Madrid);
  - fin de la golden visa;
  - suspensiones de desahucios;
  - incentivos fiscales al alquiler;
  - vivienda pública anunciada frente a entregada.
- Cada fuente: normalización con ingeniero-datos, licencia en el registro, auditoría de calidad (como en la fase 1 de V15) y entrada en el inventario.

FASE 2 · Hechos y diagnóstico (sin estimar efectos; no requiere pre-registro)
1. Hechos C1/C2 actualizados con las nuevas fuentes:
   - precios reales y nominales;
   - esfuerzo de acceso (sobreesfuerzo del 30 % y 40 %, enfoque de renta residual) por renta, edad, tenencia, nacionalidad y territorio;
   - contratos nuevos frente a vigentes;
   - parque, vacías y no principales;
   - obra nueva frente a formación de hogares;
   - vivienda pública por habitante frente a la UE;
   - lanzamientos;
   - comparación internacional.
   Una cifra solo es C1 si tiene dos fuentes realmente independientes; aplica la misma vara que llevó a las 11 bajadas.
2. Contabilidad, no causalidad:
   - descomposición de la variación del número de hogares (demografía, jefatura, migración);
   - descomposición del precio en componentes comunes y locales (factores dinámicos);
   - descomposición de los cambios en el esfuerzo (renta frente a precio) con Oaxaca-Blinder, reponderación DFL y regresiones RIF por cuantil.
3. Atlas multiescala descriptivo de todo lo anterior, con incertidumbre (intervalos y supresión de celdas pequeñas).

FASE 3 · Literatura y mecanismos
Amplía docs/v15/literatura.md con los mismos controles (Crossref; nada no leído; VERIFICADA o NO VERIFICADA; cuartiles cuando el autor descargue Scimago):
- Para cada instrumento de política:
  - mecanismo teórico;
  - evidencia internacional con diseño creíble;
  - evidencia española;
  - efectos secundarios documentados y magnitudes.
  Donde haya suficientes estudios comparables, metaanálisis con efectos aleatorios y prueba de sesgo de publicación (embudo, Egger, PET-PEESE). Esos metaanálisis darán las distribuciones a priori de la fase 6.
- Marco estructural: modelo de stock y flujo de cuatro cuadrantes (DiPasquale-Wheaton) calibrado para España y para las grandes áreas urbanas, para saber qué respuesta cabe esperar de cada shock y comprobar si los datos la muestran.

FASE 4 · Preguntas nuevas, diseños y pre-registro interno V16
1. Preguntas confirmatorias NUEVAS. No repitas H1-H5 de V15; amplía con diseños o datos distintos y declara el solapamiento. Mínimo:
   - Q1 Zonas tensionadas, en lo que V15 no cubre:
     - regresión discontinua en los umbrales legales de declaración (verifica los criterios del art. 18 de la Ley 12/2023 y si la variable de asignación se puede construir);
     - SDID y control sintético aumentado con donantes de otras comunidades vía IPVA;
     - resultados adicionales: desplazamiento a alquiler de temporada y a venta, y precio de compra.
   - Q2 Vivienda turística, más allá de H3:
     - InsideAirbnb y registros autonómicos;
     - diferencias en diferencias con las moratorias;
     - regresión discontinua espacial en los límites de zonas de planes urbanísticos (por ejemplo, el PEUAT);
     - shift-share con la demanda turística exógena.
   - Q3 Inmigración, más allá de H4: separar la demanda en alquiler de la de compra y la escala de barrio, con AKM, pruebas de Rotemberg y pretendencias.
   - Q4 Oferta: elasticidad municipal instrumentada con restricciones físicas y de planeamiento (tipo Saiz), y si los municipios menos elásticos responden más en precio a los shocks de demanda de Q3.
   - Q5 Tipos de interés: proyecciones locales y SVAR con instrumento externo (sorpresas del BCE), con exposición por peso de la hipoteca variable, sobre precio, compraventas y alquiler.
   - Q6 Fiscalidad de la compra: cambios del ITP por comunidad y su efecto en compraventas y precio, con diferencias en diferencias escalonadas.
   - Q7 Ayudas a la demanda (bono alquiler joven, avales ICO): incidencia sobre las rentas, con discontinuidad por edad o renta si los microdatos lo permiten.
   - Q8 Fin de la golden visa: compras de no residentes extracomunitarios frente a comunitarios, con diferencias en diferencias.
   - Q9 Fundamentales y burbuja: coste de uso, precio frente a alquiler y renta, cointegración en panel con dependencia transversal (CIPS, Westerlund, CS-ARDL, PMG/MG) y GSADF por territorio, con corrección múltiple.
   - Q10 Predicción, más allá de H5: MIDAS, nowcasting con indicadores adelantados e intervalos de predicción conformes, frente a AR(4) (DM/GW/CW y Model Confidence Set).
   Descarta o reformula con argumentos lo que no tenga potencia o identificación (recalcula la potencia con los datos nuevos), y dilo.
2. Búsqueda multiescala declarada:
   - rejilla completa y fija de escalas × dimensiones × resultados, escrita antes de estimar;
   - modelos jerárquicos bayesianos con reducción hacia la media (partial pooling), con priors de los metaanálisis de la fase 3 y comprobados con predictive checks;
   - heterogeneidad con bosques causales (generalized random forests, partición honesta) y DML para controles de alta dimensión;
   - control de falsos descubrimientos sobre TODA la rejilla (BH jerárquico, q-valores).
   Un hallazgo local cuenta solo si (a) sobrevive al control, (b) tiene un tamaño plausible (errores de tipo S y M de Gelman-Carlin) y (c) se replica en la muestra espacial sellada o en unidades independientes comparables. Si no, es C4 «pista».
3. Pruebas para alcanzar C3, por diseño:
   - pretendencias con Honest DiD y potencia de Roth;
   - placebos en fechas, unidades y resultados que no deberían moverse (controles negativos);
   - inferencia por aleatorización;
   - wild cluster bootstrap con pesos de Webb;
   - errores de Conley;
   - F efectivo de Montiel Olea-Pflueger e intervalos AR;
   - en la regresión discontinua: densidad (McCrary y Cattaneo-Jansson-Ma), balance de covariables y anchos óptimos y robustos (rdrobust);
   - sensibilidad a confusores no observados (Oster, robustness value de Cinelli-Hazlett, E-values);
   - exclusión de grandes ciudades e islas;
   - triangulación: el mismo signo con al menos dos diseños de identificación distintos.
4. Validación sellada: no toques la de V15. Para las fuentes nuevas, sella con sellar_v16 un bloque espacial y todo dato posterior a la etiqueta prereg-v16. Declara lo ya visto.
5. docs/v16/preregistro_v16.md:
   - preguntas, estimandos, diseños, supuestos y pruebas;
   - rejilla y multiverso (máximo 50.000);
   - correcciones, potencia y efecto mínimo detectable;
   - qué cambiaría cada conclusión del historial y qué se hace si fallan las pruebas.
   Complementa a preregistro_v15: H1-H5 no se modifican; V16 solo pre-registra preguntas, datos y rejillas nuevas, y declara su solapamiento con V15. revisor-preregistro y abogado-del-diablo lo critican; adenda punto por punto.
6. Etiqueta prereg-v16, publícala en el remoto y comprueba que existe. Sin parada: continúa con la fase 5.

FASE 5 · Herramientas validadas
montecarlo valida cada estimador nuevo con nuestro proceso generador (pocos clusters, dependencia transversal, T corto, adopción escalonada, correlación espacial) → metodologia/validacion_montecarlo_v16.md. Ninguna herramienta se usa sin pasar su validación.

FASE 6 · Estimación y comprobación de que los resultados son correctos
Ejecuta también las estimaciones de V15 según su pre-registro. Sus evaluaciones selladas temporales se hacen solo cuando llegue cada fecha del calendario; hasta entonces, quedan «pendientes» en el informe.
Hasta 3 modelizador en paralelo por pregunta independiente (worktrees). Por cada pregunta, en este orden:
1. La especificación pre-registrada; después, el multiverso y la rejilla multiescala.
2. Diagnósticos según el caso:
   - raíces unitarias y cointegración con dependencia transversal;
   - rupturas (Bai-Perron);
   - heterocedasticidad y autocorrelación;
   - Moran en residuos;
   - balance;
   - ajuste preintervención.
3. replicador-ciego reimplementa desde la ficha. Si discrepa, no se publica hasta resolverlo.
4. Doble implementación (tests/doble_impl) de toda cifra candidata a C3/C3s.
5. abogado-del-diablo intenta romper cada resultado candidato. Cada objeción se contrasta con datos o se declara como limitación.
6. Evaluación sellada (evaluate_v16; evaluate_v15 según su calendario): una vez por hipótesis, registrada.
7. Triangulación entre diseños y comparación con los metaanálisis: si el resultado se aparta de la literatura, se explica por qué o se rebaja la capa.
8. Toda desviación del pre-registro, a metodologia/desviaciones_v16.md.

FASE 7 · Informe integral (versión final)
1. publicacion/informe_integral/, generado con make, con esta estructura:
   - Resumen ejecutivo (máximo 2 páginas): SOLO los hallazgos que superen todas sus pruebas, con capa y rango. Si una pregunta no tiene hallazgos robustos, se dice en una línea con la razón. Las hipótesis de V15 con evaluación sellada pendiente se presentan como pendientes, con su fecha. Sin relleno.
   - Parte I · Diagnóstico: los hechos de la fase 2 a todas las escalas.
   - Parte II · Mecanismos: qué mueve el precio y el alquiler, qué sabemos y qué no, con el marco de cuatro cuadrantes.
   - Parte III · Catálogo de medidas: una ficha por instrumento (mecanismo, evidencia internacional, evidencia española, nuestra estimación, coste, efectos secundarios y veredicto en la escala «eficacia probada / prometedora / sin evidencia / evidencia en contra / no evaluable con los datos disponibles»).
   - Parte IV · Territorios: atlas multiescala con los hallazgos locales que sobrevivan y las pistas marcadas como tales.
   - Parte V · Escenarios y predicción: necesidad de vivienda, simulaciones condicionales y predicción con sus límites.
   - Parte VI · Manual de verificación: cómo reconocer un argumento engañoso, con ejemplos reales de afirmaciones evaluadas, entre otros:
     - periodos elegidos a conveniencia;
     - nominal frente a real;
     - contratos vigentes frente a nuevos;
     - medias frente a índices;
     - correlación presentada como causa;
     - efecto base;
     - escala que esconde la heterogeneidad;
     - anuncios frente a entregas.
     Verificador ampliado con todas las afirmaciones que el estudio permite evaluar.
   - Parte VII · Lo que no se puede afirmar y por qué.
   - Anexos: métodos, pruebas superadas y fallidas por resultado, pre-registros V15 y V16, desviaciones, licencias y reproducibilidad.
   Cada resultado de V15 y V16 declara que su pre-registro es interno (etiqueta git en el remoto, commit y fecha) y que no tiene sello de tiempo externo.
2. redactor escribe solo desde resultado.json y cifras_clave. verificador-cifras comprueba cada número. arbitro-final, como árbitro de revista Q1 de economía urbana, da su veredicto (ACEPTAR, REVISAR o REHACER); cada hallazgo se corrige o se rebate por escrito.
3. tablas_v16.xlsx con la convención de colores; figuras con el estilo del repositorio; páginas web; sección del manuscrito Quarto; verificador; fichas del anexo de todas las cifras V16-*.
4. make v16; check_v16 en make check (la 1.0 no cambia de valor; toda cifra V16 con ficha y capa; sin lenguaje causal fuera de C3/C3s; todo número del informe en cifras_clave; ninguna estimación anterior a su etiqueta de pre-registro); make publicacion, make web y make check limpios. Prepara la 2.0 con make arbol_publico y el escaneo de terceros.

══════════════════════════════════════════════
D. PARADAS (detente y explícame)
══════════════════════════════════════════════
- Una guarda que no bloquea.
- Una cifra de la 1.0 que cambiaría de valor.
- Un acceso a muestras selladas fuera de src/holdout.py.
- Un hallazgo que contradiga una conclusión publicada: se documenta, no se publica y se espera.
- Más de 6 millones de tokens de subagentes en una fase.
Las descargas que dependen de mí no paran el trabajo: van a tareas_autor.md y se sigue.

En cada parada, y al terminar cada fase, resumen de 250 palabras como máximo: qué se ha hecho, qué preguntas sobreviven y por qué, qué se descarta y por qué, tokens y qué me toca hacer.

Empieza ahora: plan.md, infraestructura B y fases 0 a 7 seguidas, deteniéndote solo en las paradas de la sección D.
