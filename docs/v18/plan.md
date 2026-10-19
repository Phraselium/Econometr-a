V18 · BIBLIOGRAFÍA, REPLICACIÓN DE ESTUDIOS Y ESTIMACIÓN DEL IMPACTO DE CADA FACTOR (estándar Banco de España)
Objetivo: estimar, con el rigor de un Documento de Trabajo del Banco de España, el impacto de cada factor sobre el precio de compra y el alquiler en España, y decir algo sobre causas cuando el diseño lo permita, con sus supuestos y limitaciones. Método:
(1) descargar y catalogar la bibliografía;
(2) reproducir los estudios clave con sus propios datos cuando sea posible;
(3) replicarlos y ampliarlos con toda nuestra información (más periodos, más territorios, más escalas);
(4) combinar nuestras estimaciones con la literatura;
(5) usar esas elasticidades para explicar qué parte de la subida corresponde a cada factor, por periodo y por territorio.

PRIMER PASO: guarda este mensaje completo, sin resumir, en docs/v18/plan.md, haz commit y cambia en CLAUDE.md la línea de V17 por «V18 en curso (bibliografía, replicación e impactos): leer docs/v18/plan.md y docs/v18/estado.md al empezar o tras compactar».

══════════════════════════════════════
A. REGLAS
══════════════════════════════════════
- Lectura previa: CLAUDE.md, proyecto.json, docs/v17/ (plan, estado, referencias_bde, correcciones), output/v17/ (lectura_bde, auditoria), publicacion/informe_integral/, metodologia/ (capas, validación Monte Carlo), docs/v15/literatura.md, docs/v16/literatura y la base de V10-V16.
- Si V17 no está completa, ejecuta antes sus fases 0 y 1 según docs/v17/plan.md (o el texto de V17 en el historial de commits) y anótalo.
- Nada de lo publicado cambia de valor ni de capa (check_v8, check_v9, check_v13, check_v16 y check_v17). V18 añade cifras V18-* con su propia clasificación (sección B).
- No se leen fuera de src/holdout.py: data/sealed, las muestras selladas de V15 y V16 y las filas muestra_sellada_v6. No se ejecuta evaluate_*. Las unidades selladas se excluyen de todas las estimaciones y se dice. Prohibido make clean, make all y make v7. Ficheros con Write o heredoc entrecomillado. Un solo make check a la vez.
- Terceros según proyecto.json: solo agregados propios con su atribución. Datos de replicación de otros autores: se respeta su licencia y no se redistribuyen si no lo permite.
- Bibliografía y derechos:
  - PDFs solo de fuentes de acceso abierto legítimo (repositorio del autor o de su institución, editorial en abierto, SSRN, NBER, RePEc, arXiv, Banco de España, BCE, bancos centrales, Unpaywall u OpenAlex con oa_url);
  - nunca de webs de descarga no autorizada;
  - se guardan en data/bib/pdf/ (en .gitignore), con su sha256 en data/bib/CHECKSUMS.sha256;
  - al repositorio van la ficha, el enlace, el DOI, la licencia y las notas; nunca el PDF ni párrafos copiados (citas de 15 palabras como máximo);
  - si no hay versión abierta, la ficha se hace con el resumen y se marca «solo resumen».
- Paquetes de replicación: buscarlos (web del autor, editorial, openICPSR, Dataverse, Zenodo, GitHub). Guardarlos en data/bib/replicacion/ (ignorado por git) con su licencia y checksum.
- Neutralidad: se evalúan factores e instrumentos, nunca partidos ni personas, sin corrección política. Si una conclusión es incómoda para cualquiera, se dice igual.
- Excel: azul los datos introducidos (con su fuente en nota), negro lo calculado en la hoja, verde lo que viene de otra pestaña. Sin paneles inmovilizados. Maquetación limpia.
- Trabajo en docs/v18/, src/v18/, output/v18/ y tests/v18/. Estado tras cada tarea. Commit por tarea y push solo a la rama designada. Tokens por fase en estado.md; si una fase supera 6 millones de tokens de subagentes, para y explícalo.

══════════════════════════════════════
B. ESTÁNDAR DE RIGOR (tipo Banco de España)
══════════════════════════════════════
B1. Plan de replicación fijado antes de estimar. Para cada estudio, antes de tocar nuestros datos:
- especificación del original (ecuación, muestra, controles, instrumento, inferencia);
- cómo se traslada a nuestros datos;
- qué ampliaciones se harán (periodos, territorios, escalas);
- qué pruebas se aplicarán.
Commit con la etiqueta local plan-replicacion-v18 antes de la primera estimación; check_v18 comprueba que ninguna estimación es anterior. Es un pre-registro interno, y se dice.

B2. Inferencia convencional, la de un trabajo publicado:
- errores agrupados al nivel del tratamiento;
- wild cluster bootstrap (pesos de Webb) con menos de 40 clusters;
- AKM o Borusyak-Hull-Jaravel en shift-share;
- Conley en datos espaciales;
- Driscoll-Kraay en paneles con dependencia transversal;
- Newey-West en series;
- intervalos de Anderson-Rubin y F efectivo de Montiel Olea-Pflueger con instrumentos.
Se publica siempre, con la distorsión medida por Monte Carlo (V16 y V17) cuando exista.

B3. Clasificación V18 de cada estimación (no sustituye a las capas del proyecto, que se muestran al lado):
- IDENTIFICADO: diseño cuasi experimental creíble, primera etapa fuerte (F efectivo > 10 o intervalo AR informativo), pretendencias y placebos superados, robusto a especificaciones razonables y coherente en signo y orden de magnitud con la literatura o con una explicación de por qué difiere. Se puede hablar de causa, con los supuestos.
- SUGESTIVO: diseño creíble con alguna prueba débil o fallida no decisiva. Se dice «la evidencia sugiere», con la limitación concreta.
- ASOCIACIÓN: sin identificación suficiente. Sin lenguaje causal.
- NO ESTIMABLE: faltan datos o variación; se dice qué datos lo harían estimable.

B4. Pruebas mínimas por diseño:
- Diferencias en diferencias: estudio de eventos con pretendencias; Callaway-Sant'Anna o Sun-Abraham si la adopción es escalonada; Honest DiD (Rambachan-Roth) para sensibilidad; placebos de fecha y de resultado.
- Variables instrumentales y shift-share: primera etapa, pruebas de Rotemberg, exclusión de los orígenes de más peso, pretendencias del instrumento, sobreidentificación si hay varios instrumentos.
- Regresión discontinua: densidad, balance y anchos óptimos con rdrobust.
- Series temporales y SVAR: raíces unitarias, estabilidad, sensibilidad a la identificación (restricciones alternativas) y bandas.
- Siempre: robustez a la exclusión de Madrid, Barcelona, islas y unidades atípicas; a la medida de precio (IPV, valor tasado, Registradores) y a la de alquiler (SERPAVI, IPVA, fianzas, IPC).

B5. Magnitud preferida. Para cada factor, combina nuestras estimaciones (IDENTIFICADO o SUGESTIVO) con las de la literatura en la misma unidad, mediante un metaanálisis bayesiano de efectos aleatorios. Si hay muy pocos estudios, haz una media ponderada por precisión y enséñala junto a cada estimación. Resultado: magnitud preferida con su intervalo y heterogeneidad. Si las unidades no son comparables, no se combinan y se dice.

B6. Revisión: replicador-ciego reimplementa cada estimación IDENTIFICADO o SUGESTIVO desde el plan de B1, y abogado-del-diablo la ataca (dos rondas). Si la réplica discrepa, no se clasifica hasta resolverlo.

══════════════════════════════════════
C. INFRAESTRUCTURA
══════════════════════════════════════
- Nuevos subagentes en .claude/agents/:
  - bibliotecario (sonnet; WebSearch, WebFetch, Bash, Write en data/bib/ y docs/v18/bib/): localiza la versión abierta legítima, descarga, calcula el checksum, registra la licencia y crea la ficha (pregunta, datos, diseño, identificación, resultado principal con unidad, limitaciones, paquete de replicación sí o no);
  - replicador-estudio (sonnet): reproduce un estudio con su paquete de replicación y compara con las cifras publicadas.
  Reutiliza adquisidor-datos, ingeniero-datos, modelizador, montecarlo, replicador-ciego, abogado-del-diablo, arbitro-final, redactor y verificador-cifras.
- Como máximo 3 subagentes que escriban a la vez, en worktrees.
- Comandos /v18-fase0 … /v18-fase6 y /v18-estado; objetivos make v18_f0 … v18_f6, v18 y check_v18 dentro de make check. Hook: rechazar make v18_f3 y posteriores si la etiqueta plan-replicacion-v18 no existe.

══════════════════════════════════════
D. FASES
══════════════════════════════════════
FASE 0 · Punto de partida
Comprueba V17 (referencias, datos y auditoría). Inventaria qué datos de la base sirven para cada estudio de la sección E y cuáles faltan. Lo que requiera al autor (descarga masiva del Catastro, EFF, microdatos de portales, microdatos de beneficiarios) va a docs/v18/tareas_autor.md al principio, y el trabajo sigue con lo demás.

FASE 1 · Bibliografía (en paralelo, hasta 3 bibliotecario)
1. Descarga y ficha de todas las referencias de la sección E, más las de docs/v15/literatura.md y docs/v16/literatura que tengan versión abierta.
2. Búsqueda sistemática adicional por factor (OpenAlex y Crossref; documentos del Banco de España, del BCE y de los bancos centrales europeos), con criterios escritos antes de buscar: diseño cuasi experimental o estructural, datos de España o de mercados europeos comparables, y publicación en revista con revisión, documento de banco central o working paper de una serie reconocida.
3. docs/v18/bib/: una ficha por estudio, más una tabla resumen por factor con la unidad del efecto (elasticidad, porcentaje por punto, porcentaje por desviación típica) para poder combinarlos.
4. Verificación de DOI con src/v15/verificar_referencias.py. Cuartiles cuando el autor descargue Scimago.

FASE 2 · Reproducción de los estudios originales (hasta 3 replicador-estudio)
Para cada estudio con paquete de replicación: reproduce su resultado principal con sus datos y compáralo con lo publicado (coincide / difiere, y por qué). Si no hay paquete, anótalo y pasa a la fase 3 solo con su especificación. Resultado: docs/v18/reproduccion.md.

FASE 3 · Plan de replicación con nuestros datos (B1) y etiqueta
Escribe docs/v18/plan_replicacion.md con un apartado por estudio y por ampliación. Revisión de revisor-preregistro y abogado-del-diablo; adenda. Etiqueta local plan-replicacion-v18 y push de la rama. Si el proxy no deja subir la etiqueta, anota en tareas_autor.md la orden para subirla desde el ordenador del autor y sigue: el hook comprueba la etiqueta local y que el commit esté en la rama remota.

FASE 4 · Estimación (hasta 3 modelizador en paralelo; montecarlo para cada herramienta nueva)
Para cada estudio de la sección E:
1. Réplica en nuestros datos con la especificación original, en el periodo y territorio más parecidos.
2. Ampliación a más periodos, territorios y escalas.
3. Pruebas de B4 e inferencia de B2.
4. Clasificación de B3.
5. replicador-ciego y abogado-del-diablo (B6).
Además, los modelos de conjunto de la sección F.

FASE 5 · Magnitudes preferidas y contabilidad de la subida
1. Magnitud preferida por factor (B5).
2. Contabilidad de la subida: con las magnitudes preferidas (solo IDENTIFICADO o SUGESTIVO) y la variación observada de cada factor, calcula la contribución de cada uno a la variación del precio real de compra y del alquiler:
   - por periodo (1995-2007, 2008-2013, 2014-2019, 2020-2022, 2022-2026);
   - a escala nacional, por comunidad y por provincia donde haya datos, y para las grandes ciudades.
   Propaga la incertidumbre por Monte Carlo sobre las magnitudes y deja una fila «no explicado».
   Es contabilidad con elasticidades estimadas, no una descomposición estructural: dilo. Compárala con la descomposición SVAR de V8 y con las explicaciones del Banco de España.
3. Respuesta explícita, por periodo y territorio: qué factores explican la mayor parte de la subida, con qué confianza y qué queda sin explicar.

FASE 6 · Documento de Trabajo y su integración
publicacion/documento_v18/, generado con make, con el formato de un Documento de Trabajo del Banco de España:
- Resumen ejecutivo de 1 página con la tabla de impactos: factor | magnitud preferida | intervalo | clasificación | confianza | limitación principal.
- Resumen no técnico.
- 1. Introducción.
- 2. Datos.
- 3. Métodos.
- 4. Resultados por factor: original, reproducción, réplica, ampliación y magnitud preferida.
- 5. Contabilidad de la subida por periodo y territorio.
- 6. Implicaciones para las políticas: qué cambia en la tabla de medidas y en la de discurso público auditadas en V17.
- 7. Limitaciones y qué datos las resolverían.
- Anexos: fichas bibliográficas, reproducciones, planes, pruebas por estimación, Monte Carlo y declaración de qué es pre-registro interno y qué es a posteriori.
arbitro-final actúa como revisor de Documentos de Trabajo del Banco de España: ACEPTAR, REVISAR o REHACER. verificador-cifras comprueba cada número. tablas_v18.xlsx con la convención de colores. check_v18 en make check: nada anterior cambia; toda cifra V18 con id, fuente y clasificación; sin lenguaje causal fuera de IDENTIFICADO. make publicacion, make web y make check limpios. Commit y push.

══════════════════════════════════════
E. ESTUDIOS QUE HAY QUE REPRODUCIR Y REPLICAR
══════════════════════════════════════
(Verificar todos; las cifras citadas son el punto de partida, no hechos.)

E1. Vivienda turística. Garcia-López, Jofre-Monseny, Martínez-Mazza y Segú (2020), Journal of Urban Economics 119, 103278. Diseños: efectos fijos con tendencias heterogéneas por barrio; shift-share con atractivos turísticos (dónde) y búsquedas en Google (cuándo); estudio de eventos; caso de la Sagrada Familia. Resultado de partida: +1,9 % en el alquiler del barrio medio y +7 % en el decil alto.
- Réplica: Barcelona por barrio con HUT 2018-2026 e Incasòl o SERPAVI.
- Ampliación: València, Madrid, Málaga, Palma, Sevilla, Alicante y otras con InsideAirbnb, registros autonómicos y SERPAVI por sección; regulaciones locales (PEUAT y moratorias) como diferencias en diferencias.
- Compara con H3 y Q2.

E2. Topes al alquiler.
- Jofre-Monseny, Martínez-Mazza y Segú (2023), Regional Science and Urban Economics 101, 103916: diferencias en diferencias y estudio de eventos con el registro de contratos; −4 a −6 % en la renta, sin caída de la oferta.
- Monràs y García-Montalvo (FRBSF Working Paper 2023-28): anuncios; en torno a −5 %, la mitad por composición; efectos distintos por tramo de precio.
- Réplica: Cataluña 2020-2022 con Incasòl por municipio (renta y número de contratos), incluido el análisis por tramo de renta si los datos lo permiten.
- Ampliación: zonas tensionadas de 2024 en Cataluña y las de otras comunidades cuando haya periodo posterior; desplazamiento a temporada si hay datos.
- Compara con H1, H2 y Q1. Monràs y García-Montalvo solo es replicable con anuncios: si no hay datos, NO ESTIMABLE y tarea del autor.

E3. Inmigración. González y Ortega (2013), Journal of Regional Science 53(1), 37-59: instrumento por asentamientos históricos de cada nacionalidad, provincias, 1998-2008; aproximadamente un tercio del boom de precios y de obra nueva. Saiz (2007) como referencia metodológica.
- Réplica: provincias 2001/2003-2008 con el padrón por nacionalidad y el valor tasado o el IPV.
- Ampliación: 2014-2025 en precio y alquiler (SERPAVI, IPVA); municipios; separación entre demanda de compra y de alquiler.
- Inferencia AKM o Borusyak-Hull-Jaravel; pruebas de Rotemberg.
- Compara con H4 y Q3-b.

E4. Ayudas a la demanda. Fack (2005, 2006), Gibbons y Manning (2006), Banque de France WP 886 y la literatura posterior sobre incidencia (porcentaje de la ayuda que acaba en el alquiler).
- Réplica: bono alquiler joven o ayudas autonómicas, con variación por edad, renta, territorio o fecha (discontinuidad o diferencias en diferencias), si los datos lo permiten.
- Si no, NO ESTIMABLE con su tarea del autor, y la magnitud preferida sale solo de la literatura, rotulada así.

E5. Oferta y suelo. Saiz (2010) y la literatura sobre elasticidad de la oferta y restricciones.
- Réplica: elasticidad de la oferta por área urbana o provincia con restricciones físicas (pendiente del MDT, costa, agua) y de planeamiento (SIU), instrumentando la demanda con un Bartik de empleo.
- Interacción: ¿los precios suben más ante el mismo shock de demanda donde la oferta es menos elástica?
- Compara con Q4. No uses la Red Natura como instrumento (ya falló en Q4).

E6. Obra nueva y alquileres cercanos. Literatura reciente sobre el efecto de los edificios nuevos en los alquileres de su entorno (EE. UU., Europa, Helsinki; localizarla y verificarla).
- Réplica: diferencias en diferencias por distancia a edificios nuevos con la antigüedad de construcción del Catastro por parcela y SERPAVI por sección.
- Necesita la descarga masiva del Catastro: si no está, NO ESTIMABLE y tarea del autor.

E7. Tipos de interés. Estimaciones del Banco de España y del BCE sobre la transmisión de los tipos a precios y compraventas.
- Réplica: proyecciones locales y SVAR con instrumento externo (sorpresas de alta frecuencia del BCE, Jarociński-Karadi o EA-MPD) a escala nacional; panel provincial con exposición por peso de la hipoteca variable y de las compras sin hipoteca.
- Compara con Q5 y con V8.

E8. Fiscalidad de la compra. Best y Kleven (2018), Besley et al. (2014) y evaluaciones españolas del ITP si existen.
- Réplica: cambios de tipo del ITP por comunidad (base de intervenciones de V16), diferencias en diferencias escalonadas sobre compraventas y precio; bunching en umbrales de tipos reducidos si hay datos agregados por tramo.
- Compara con Q6.

E9. Compradores no residentes. Badarinza y Ramadorai (2018), Cvijanović y Spaenjers (2021) y notas del Banco de España.
- Réplica: shocks en los países de origen (crisis, tipo de cambio, riesgo) por la exposición histórica de cada provincia a cada nacionalidad compradora, con agregados de compras por nacionalidad.
- Fin de la golden visa como diferencias en diferencias, si los datos separan UE y fuera de la UE.
- Compara con Q8.

E10. Grandes tenedores e inversores institucionales. Literatura de EE. UU. y Europa (localizar y verificar).
- Replicable solo si hay variación con datos de titularidad (entrada de grandes tenedores por zona) y alquiler. Si no, ASOCIACIÓN o NO ESTIMABLE, con lo que dicen los datos parciales de V17.

E11. Viviendas vacías. Segú (2020) y evaluaciones de recargos e impuestos sobre vacías.
- Réplica: si hay variación territorial y temporal en recargos del IBI o impuestos autonómicos (por ejemplo, el de Cataluña), diferencias en diferencias sobre la vacancia (censos 2011 y 2021, consumo eléctrico) y, si es posible, sobre el alquiler.

E12. Vivienda pública. Literatura sobre desplazamiento de la promoción privada y efecto sobre los precios.
- Réplica: si hay datos de promociones públicas por municipio y año, efecto sobre la obra privada y los precios del entorno. Si no, NO ESTIMABLE.

══════════════════════════════════════
F. MODELOS DE CONJUNTO (como el Banco de España)
══════════════════════════════════════
F1. Modelo de precio de largo plazo con corrección de error: precio real frente a renta disponible real, tipo hipotecario real, población o hogares y parque de viviendas por hogar. Nacional y panel provincial (CS-ARDL o PMG con dependencia transversal). Sirve para medir la sobrevaloración frente a fundamentales, comparar con el indicador del Banco de España y obtener elasticidades de largo plazo que se contrastan con las de la sección E.

F2. Modelo de alquiler equivalente: alquiler real frente a renta, hogares, parque y tipos, por provincia.

F3. Elasticidad de la oferta y del parque: respuesta de las iniciadas y terminadas al precio y a los costes, por provincia, con las restricciones de E5.

F4. Coherencia: las elasticidades de F1-F3 y las de la sección E deben ser compatibles en signo y orden de magnitud. Si no lo son, se explica por qué, y la contabilidad de la fase 5 usa la combinación más defendible, con las alternativas como sensibilidad.

══════════════════════════════════════
G. PARADAS
══════════════════════════════════════
- Una cifra publicada que cambiaría de valor o de capa.
- Un acceso a muestras selladas fuera de src/holdout.py.
- Una estimación IDENTIFICADO que contradiga una conclusión publicada: se documenta y se espera mi decisión.
- Una reproducción que no coincida con el estudio original por una razón que no se pueda explicar: se documenta y se sigue con los demás.
- Más de 6 millones de tokens de subagentes en una fase.
Las tareas que dependen de mí no paran el trabajo: van a tareas_autor.md y se sigue.

En cada parada y al final de cada fase, resumen de 250 palabras como máximo.

Resumen final de 500 palabras como máximo:
- la tabla de impactos;
- la contabilidad de la subida por periodo, con los territorios principales;
- qué estudios se reprodujeron y replicaron, y con qué resultado;
- qué cambia en las tablas de medidas y de discurso de V17;
- qué me queda por hacer.

Empieza ahora: plan.md, infraestructura C y fases 0 a 6 seguidas, deteniéndote solo en las paradas.
