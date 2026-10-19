V17 · LECTURA CON ESTÁNDAR BANCO DE ESPAÑA Y AUDITORÍA CRÍTICA DE LAS CONCLUSIONES
Objetivo: reescribir la lectura del proyecto como lo haría un Documento Ocasional del Banco de España sobre el mercado de la vivienda: inferencia convencional, juicio experto explícito y comparación con las estimaciones publicadas por el propio Banco de España, el BCE y la literatura académica. Además, auditar con la máxima dureza las conclusiones de divulgación (tablas de discurso político y de medidas, sección D) y responder a cuatro preguntas de fondo (sección D3). No se busca confirmar nada: el objetivo es encontrar dónde las afirmaciones son falsas, engañosas, incompletas o demasiado prudentes.

══════════════════════════════════════
A. REGLAS
══════════════════════════════════════
- Lectura previa: CLAUDE.md, proyecto.json, publicacion/informe_integral/, publicacion/por_que_ha_subido.md, metodologia/ (capas, validación Monte Carlo de V16, desviaciones), docs/v16/ (decisiones, estado), docs/v15/literatura.md y docs/v16/literatura.
- Nada de lo publicado cambia de valor ni de capa: check_v8, check_v9, check_v13 y check_v16 siguen pasando. V17 añade una lectura paralela con su propia columna y sus ids V17-*.
- Todo lo de V17 es análisis A POSTERIORI: se hace después de ver los resultados. Se declara así en cada tabla y en el texto. Nunca se presenta como confirmatorio ni sustituye a las capas del proyecto.
- data/sealed, las muestras selladas de V15 y V16 y las filas muestra_sellada_v6 no se leen fuera de src/holdout.py. No se ejecuta evaluate_*. Prohibido make clean, make all y make v7. Ficheros con Write o heredoc entrecomillado. Un solo make check a la vez.
- Terceros según proyecto.json: solo agregados propios con su atribución.
- Neutralidad: se evalúan afirmaciones e instrumentos, nunca partidos ni personas. Pero no hay corrección política: si una afirmación incómoda para cualquiera es cierta, se dice; si una prudente es engañosa, también.
- Referencias: VERIFICADA (DOI en Crossref) o NO VERIFICADA. Nada no leído al menos en su resumen; se indica si se leyó completo o solo el resumen. Para documentos del Banco de España, BCE, INE y Ministerio: URL y fecha de consulta. Nunca se inventa una cifra ajena: si no se encuentra, se dice. Las referencias de la sección D2 son un punto de partida para verificar, no hechos.
- Prensa: solo para localizar documentos originales. Ninguna cifra se cita desde un artículo de prensa si existe el documento original; si solo existe en prensa, se rotula así.
- Excel: azul los datos introducidos (con su fuente en nota), negro lo calculado en la hoja, verde lo que viene de otra pestaña. Sin paneles inmovilizados. Maquetación limpia.
- Trabajo en docs/v17/, src/v17/, output/v17/ y tests/v17/. Estado tras cada tarea. Commit por tarea y push solo a la rama designada. Tokens por fase en estado.md; si una fase supera 4 millones de tokens de subagentes, para y explícalo.
- Subagentes: reutiliza los de .claude/agents/ (adquisidor-datos y lector-literatura para fuentes nuevas; modelizador para la inferencia convencional; abogado-del-diablo y arbitro-final para la auditoría; redactor y verificador-cifras para el documento). Como máximo 3 que escriban a la vez, en worktrees.
- Comandos: crea /v17-fase0 … /v17-fase5 y /v17-estado, y los objetivos make v17_f0 … v17_f5, v17 y check_v17 dentro de make check.

══════════════════════════════════════
B. CAMBIOS DE ESTÁNDAR (lectura paralela, sin tocar las capas)
══════════════════════════════════════
B1. Dato oficial. Nueva etiqueta «OF» para estadísticas oficiales de fuente única (INE, Banco de España, Ministerio, Eurostat) que el proyecto clasifica como C4 solo por tener una sola fuente. En la lectura V17 se tratan como hechos, con su fuente. No cambia la capa original, que se muestra al lado.

B2. Inferencia convencional. Para cada estimación de V8, V9, V12, V15 y V16 sin inferencia por no pasar el Monte Carlo:
- calcula la inferencia que usaría un trabajo estándar: errores robustos agrupados; wild cluster bootstrap con pesos de Webb cuando hay pocos clusters; Driscoll-Kraay en paneles con dependencia transversal; Newey-West en series;
- publícala junto a la distorsión medida en vuestro Monte Carlo (tamaño real del contraste al 5 % nominal), por ejemplo: «p = 0,03; el contraste rechaza un 9 % de las veces bajo la nula».
No se publica inferencia convencional si la distorsión supera el 15 % de tamaño real; esos casos se marcan como no fiables.

B3. Corrección múltiple dentro de cada pregunta. Recalcula los ajustes por familia de pregunta (no entre preguntas distintas) como sensibilidad, junto a los vuestros.

B4. Mejor estimación razonada. Para cada canal (demanda y hogares, inmigración, tipos, oferta, turismo, regulación, fiscalidad, compradores no residentes, grandes tenedores, crédito), una «mejor estimación» que combine:
- nuestros datos con la inferencia de B2;
- las estimaciones publicadas del Banco de España y el BCE;
- la literatura con diseño creíble.
Cada una con su rango, su grado de confianza en la escala del Banco de España («la evidencia indica / sugiere / es compatible con / no permite concluir») y por qué. Es juicio experto, no un resultado identificado, y se rotula así.

B5. Medidas de referencia del Banco de España:
- Precio: el índice ajustado por calidad (IPV del INE) como medida principal de variación; los precios medios por m² como complemento, con su sesgo de composición explicado.
- Acceso: precio y alquiler deflactados por renta de los hogares (precio/renta, esfuerzo), además de por IPC.
- Sobrevaloración: los indicadores que publica el Banco de España (precio/renta, precio/alquiler, desviación respecto a un modelo econométrico), además del GSADF corregido en V16. Compara con sus valores publicados.
- Crédito: crecimiento del crédito hipotecario nuevo, LTV, LTI, esfuerzo financiero y proporción de compras sin hipoteca.

══════════════════════════════════════
C. FASES
══════════════════════════════════════
FASE 0 · Referencias del Banco de España y del INE
1. Localiza y lee lo que el Banco de España ha publicado sobre vivienda en los últimos años:
   - Informes Anuales 2023, 2024 y 2025 (capítulos de vivienda);
   - Informes de Estabilidad Financiera (sobrevaloración, crédito);
   - Documentos Ocasionales y de Trabajo sobre alquiler, déficit de vivienda, inmigración y vivienda, accesibilidad, tipos y transmisión hipotecaria, y compradores no residentes;
   - artículos analíticos y del Boletín Económico.
   Añade el BCE (Financial Stability Review y working papers sobre vivienda en la zona euro). Del INE: ECP a 1-1-2026, EVR 2024, MNP y proyecciones de población 2026-2076 y de hogares.
2. docs/v17/referencias_bde.md: para cada documento, qué estima, cómo, con qué datos y su cifra principal, con URL y fecha. Tabla de comparación: cada cifra del proyecto frente a la del Banco de España cuando midan lo mismo (déficit, sobrevaloración, esfuerzo, elasticidades, efectos de tipos, compras de no residentes). Si discrepan, por qué. En particular, el déficit del Banco de España (unas 750.000 viviendas en 2021-2025 según su Informe Anual 2025, y las cifras de los informes de 2023 y 2024) frente a nuestras cotas C2: definiciones, periodos y supuestos.

FASE 1 · Datos que faltan (en paralelo, hasta 3 adquisidor-datos)
Solo lo necesario para la auditoría y las preguntas de D3:
- Turismo local: viviendas turísticas por sección y municipio sobre el parque de alquiler local (INE, registros autonómicos, InsideAirbnb), con su distribución, no solo la media nacional.
- Migración y hogares:
  - descomposición del crecimiento de la población y de los hogares 2015-2025 por saldo natural y migración neta, separando nacidos en España y en el extranjero, y por nacionalidad (INE: ECP, EVR, MNP);
  - migración interior entre provincias y hacia las coronas metropolitanas;
  - tenencia (propiedad o alquiler) por nacionalidad o país de nacimiento (ECV, Censo 2021);
  - tamaño medio del hogar y su evolución por edad y origen.
- Crédito y compras: compras con y sin hipoteca (agregados de Notariado o Registradores), compras de no residentes y de personas jurídicas, crédito nuevo, LTV y LTI (Banco de España).
- Titularidad:
  - estadísticas catastrales de titularidad;
  - datos del Catastro obtenidos por transparencia (más de diez viviendas);
  - Observatori Metropolità de l'Habitatge de Barcelona;
  - estimaciones del Ministerio sobre la oferta de alquiler en manos de grandes propietarios;
  - informes oficiales sobre multiarrendadores.
  Con sus limitaciones: parque total frente a parque en alquiler, ciudad frente a media nacional, personas físicas frente a jurídicas.
- Parque social: vivienda social y pública en España frente a la UE (OCDE Affordable Housing Database, Eurostat, Ministerio).
- Renta: renta disponible de los hogares para deflactar (INE, contabilidad nacional) y renta por sección (ADRH).
- Oferta y capacidad:
  - suelo urbano y urbanizable por municipio (SIU del MIVAU);
  - visados, iniciadas y terminadas;
  - empleo y costes de la construcción (EPA por rama, índices de costes del INE);
  - plazos de licencias donde haya datos;
  - el potencial de viviendas previstas en las grandes áreas urbanas que cita el Banco de España.

FASE 2 · Inferencia convencional y mejor estimación (B2-B5)
Aplica B2-B5 a todo lo estimado. Resultado en output/v17/lectura_bde/, con tablas comparativas: capa del proyecto | lectura convencional | distorsión | mejor estimación | confianza.

FASE 3 · Auditoría crítica (secciones D1 y D3)
Para cada fila de D1, en paralelo con abogado-del-diablo (dos rondas):
1. El mejor argumento a favor y el mejor en contra, con datos.
2. Pruebas mínimas, según la fila:
   - Turísticos: proporción sobre el parque de alquiler local en los percentiles altos de secciones y municipios; traslación de esa cantidad a precio con las estimaciones de Garcia-López et al. (2020) y posteriores; comparación con H3 y Q2; qué dicen el Banco de España y otros estudios españoles. Reformula «a escala nacional no puede ser la causa principal» distinguiendo media nacional y mercados locales.
   - Inmigración: proporción del crecimiento de la población y de los hogares que viene de la migración neta; tenencia por origen; González y Ortega (2013) frente a H4 y Q3-b; qué dice el Banco de España. Separa la afirmación contable («la demanda nueva procede mayoritariamente de la inmigración») de la causal («la inmigración sube el alquiler más que otra demanda equivalente»). Corrige «atribuirlo a un grupo concreto no tiene base» si es falso.
   - Tipos: estimaciones del Banco de España y del BCE sobre el efecto de los tipos en el precio y en las compraventas; peso de las compras sin hipoteca y de no residentes; contrafactual (¿cuánto habría subido sin la subida de tipos?). Decide si «subieron tipos y precios» es un argumento válido o engañoso.
   - Burbuja: indicadores de sobrevaloración del Banco de España con sus valores; potencia del GSADF con nuestra muestra (Monte Carlo); crédito y apalancamiento frente a 2005-2007. Reformula con el lenguaje del Banco de España.
   - Alquiler: medidas disponibles y cuál usar para cada pregunta.
   - Precio: por qué el IPV ajustado por calidad es la medida principal; sesgo de composición de los precios medios por m², cuantificado si es posible; variación real deflactada por renta además de por IPC. Corrige «quien elige la cifra elige el mensaje» si es una falsa equivalencia.
   - Grandes tenedores: qué dicen los datos parciales (parque total frente a parque en alquiler, España frente a grandes ciudades); evidencia causal sobre precios en España y fuera (incluida la literatura sobre inversores institucionales en EE. UU.), con su validez externa. Corrige «no hay datos de titularidad».
   - ITP: evaluaciones españolas de cambios autonómicos de tipo, si existen; literatura internacional sobre impuestos a la transmisión; veredicto.
   - Más oferta: literatura sobre el efecto de la obra nueva en el alquiler cercano y el filtrado; plazos; restricciones de suelo y de capacidad constructiva en España; dónde sí y dónde no.
   - Topes: Jofre-Monseny, Martínez-Mazza y Segú (2023) frente a Monràs y García-Montalvo (2023); explica la discrepancia (registro de contratos frente a anuncios; composición; efectos por tramo de precio); estudios sobre la Ley 12/2023 y las zonas tensionadas de 2024 si existen; alquiler de temporada. Comprueba si los «efectos secundarios documentados» están documentados en España.
   - Turística (regulación): efecto local medido en España, si lo hay.
   - Vacías: parque vacío útil frente a nominal (censo, consumo eléctrico, localización) y evidencia de los recargos.
   - Ayudas a la demanda: traslación medida (Fack 2005 y 2006; Gibbons y Manning 2006; Banque de France WP 886 y posteriores) y su implicación para el beneficiario y para el resto de inquilinos; si existe, evaluación del bono alquiler joven o de los avales ICO. Corrige «sin evidencia de mejorar la asequibilidad» si es incorrecto.
   - Vivienda pública: separa el efecto sobre los ocupantes del efecto sobre los precios de mercado; escala necesaria para mover precios con el parque español frente al europeo; evidencia internacional (Viena, Países Bajos, Francia) con su validez externa.
3. Veredicto por fila: «se sostiene», «se sostiene con matices», «engañosa», «incorrecta» o «no se puede saber». Texto corregido y confianza en la escala del Banco de España.
4. Preguntas de D3: respuesta argumentada con datos y literatura, confianza y qué no se puede saber.
5. Resultado: output/v17/auditoria/, con una ficha por fila y por pregunta, y una tabla final «antes / después / por qué».

FASE 4 · Documento estilo Documento Ocasional del Banco de España
(NO SE EJECUTA: se integra en la fase 6 de V18 según las instrucciones del encabezado.)

FASE 5 · Integración
check_v17 en make check: nada de 1.0, V15 ni V16 cambia; toda cifra V17 con id y fuente; rótulo «a posteriori» en todo lo V17. make publicacion, make web y make check limpios. Commit y push.

══════════════════════════════════════
D. CONTENIDO QUE HAY QUE AUDITAR
══════════════════════════════════════
D1. Conclusiones de divulgación (texto literal)
Discurso político:
- «La culpa es de los pisos turísticos»: a escala nacional no puede ser la causa principal (≤ 2,7 % del parque de alquiler). En barrios concretos es posible, pero no está demostrado en España.
- «La culpa es de la inmigración»: correlación frágil; la literatura no tiene un signo único. La población crece y eso empuja la demanda, pero atribuirlo a un grupo concreto no tiene base.
- «Con los tipos altos bajarán los precios»: en 2022-2024 subieron los tipos y también los precios.
- «Hay burbuja» / «no hay burbuja»: ninguna de las dos se puede afirmar; no hay exuberancia estadística.
- «El alquiler ha subido un X %»: pregunta si son contratos vigentes o nuevos, y si es nominal o real.
- «El precio ha subido un X %»: de 2019 a 2025, +30 % nominal pero +7 % real por m²; con el índice del INE, +19 % real. Quien elige la cifra elige el mensaje.
- «Los grandes tenedores controlan el mercado»: no hay datos de titularidad para afirmarlo ni negarlo.
- «Bajar el ITP abarata la vivienda»: no evaluable en España.
Medidas, ordenadas por solidez:
1. Más oferta donde hay presión: prometedora. Es coherente con el déficit medido y con la literatura internacional. Es la más respaldada, pero tarda años, porque el parque se ajusta despacio.
2. Regular la renta de los contratos nuevos: prometedora para el inquilino con contrato regulado. Tiene efectos secundarios documentados: contratos de temporada, menos oferta de alquiler. En Cataluña solo hay una pista de signo.
3. Regular la vivienda turística: prometedora en la literatura internacional, no evaluable en España. Su efecto agregado está acotado; su efecto local, sin medir.
4. Movilizar vivienda vacía: prometedora para reducir la vacancia. No hay evidencia de que baje precios.
5. Ayudas a la demanda (bono joven, avales): sin evidencia de mejorar la asequibilidad. La literatura internacional muestra que parte de la ayuda acaba en el precio donde la oferta es rígida.
6. Vivienda pública e ITP: sin evidencia en España.
Críticas previas que hay que comprobar, no dar por buenas:
- el denominador nacional de la cota turística;
- la confusión entre contabilidad y causalidad en la inmigración;
- la falta de contrafactual en los tipos;
- la baja potencia del GSADF;
- la falsa equivalencia entre el IPV y los precios medios por m²;
- los datos parciales de titularidad;
- la injusticia del veredicto sobre ayudas a la demanda;
- la mezcla de ocupantes y mercado en la vivienda pública;
- los estudios españoles sobre topes y sobre el ITP que puede que no se hayan buscado.

D2. Referencias de partida (verificar DOI y contenido; no darlas por buenas)
- Turismo: Garcia-López, Jofre-Monseny, Martínez-Mazza y Segú (2020), Journal of Urban Economics 119, 103278 (efecto en el barrio medio y en el decil alto). Comparar con H3 y Q2 y usar sus estimaciones para traducir la proporción local de viviendas turísticas a precio.
- Topes: Jofre-Monseny, Martínez-Mazza y Segú (2023), Regional Science and Urban Economics 101, 103916 (registro de contratos: −4 a −6 %, sin menos oferta) frente a Monràs y García-Montalvo (FRBSF Working Paper 2023-28; anuncios: en torno a −5 %, la mitad por composición, menos oferta en la parte alta y subidas en la baja). Explicar la discrepancia y reformular el veredicto.
- Ayudas a la demanda: Fack (2005, 2006), Gibbons y Manning (2006), Banque de France WP 886: traslación de entre el 50 y el 80 %. Reformular el veredicto en términos de incidencia (beneficiario frente a resto de inquilinos).
- Inmigración: González y Ortega (2013), Journal of Regional Science 53(1), 37-59 (boom 1998-2008: aproximadamente un tercio del aumento de precios y de la obra nueva). Comparar con H4 y Q3-b; separar contabilidad de causalidad. Añadir Saiz (2007) y la literatura posterior ya en la ficha P4 de V15.
- Grandes tenedores: datos del Catastro por transparencia (en torno al 2-4 % del parque total en propietarios con más de diez viviendas, según la fuente), Observatori Metropolità de l'Habitatge de Barcelona (36 % del alquiler habitual en manos de grandes tenedores) y estimación del Ministerio (15 % de la oferta de alquiler). Distinguir parque total de parque en alquiler y ciudad de media nacional. Buscar evidencia causal sobre precios.
- Déficit y oferta: Banco de España, Informe Anual 2025 (unas 750.000 viviendas en 2021-2025, la mitad en seis provincias; unos 240.000 hogares y unas 92.000 viviendas terminadas en 2025; potencial de unas 320.000 viviendas previstas en las capitales de seis grandes áreas; compras de no residentes del 7,4 % en 2021-2025) e Informes Anuales 2023 y 2024. Comparar con nuestras cotas C2.
- Población: INE (ECP a 1-1-2026: 49.570.725 habitantes y más de 10 millones nacidos en el extranjero; EVR 2024: saldo migratorio de 626.268; proyecciones 2026-2076). Descomponer el crecimiento de la población y de los hogares por saldo natural y migratorio.
- A buscar y verificar (sin referencia fijada):
  - efecto de la obra nueva sobre los alquileres cercanos y filtrado (estudios recientes en EE. UU. y Europa, incluido Helsinki);
  - inversores institucionales y alquiler (EE. UU. y Europa);
  - impuestos a la transmisión (Best y Kleven, 2018; Besley et al., 2014) y cualquier evaluación española del ITP;
  - compradores no residentes (Badarinza y Ramadorai, 2018; Cvijanović y Spaenjers, 2021; notas del Banco de España);
  - recargos a viviendas vacías (Segú, 2020, y posteriores);
  - vivienda pública y desplazamiento de la promoción privada;
  - transmisión de los tipos al precio de la vivienda en la zona euro (BCE) y en España (Banco de España).

D3. Preguntas de fondo que el documento debe responder
1. ¿Por qué crece la población si el saldo vegetativo de los nacidos en España es negativo?
   - Cuantifica el peso del saldo migratorio, por origen y año, y su motivo según la evidencia (empleo, origen latinoamericano, reagrupación familiar, regularizaciones), separando hechos de interpretaciones.
   - Cuantifica también los otros motores del número de hogares: reducción del tamaño del hogar, envejecimiento y emancipación.
   - Di qué parte de la demanda nueva de vivienda explica cada uno, en contabilidad, y qué no se puede atribuir causalmente.
2. ¿Problema general o local?
   - Distribución territorial del déficit (provincias, áreas urbanas, coronas), del esfuerzo y de la subida de precios y alquileres.
   - Peso del componente común (nacional y europeo) frente al local.
   - Dónde se concentra la tensión y si se desplaza a las coronas.
   - Conclusión clara: qué parte del problema es general y cuál es local.
3. ¿Es factible construir donde hace falta?
   - Suelo disponible (urbano y urbanizable) frente a necesidad por área.
   - Plazos de planeamiento y licencias.
   - Capacidad del sector (empleo, costes, comparación con la producción del boom).
   - Potencial previsto en las grandes áreas según el Banco de España.
   - Transporte hacia las coronas.
   - Escenarios de producción necesarios para cerrar el déficit en 5 y 10 años frente a la producción actual, con supuestos explícitos.
   - Conclusión clara: dónde es factible, dónde no y qué lo impide.
4. Qué no sabemos y qué datos lo resolverían: lista priorizada (microdatos de transacciones y de anuncios, titularidad, licencias, suelo, registro de alquileres de corta y media duración), con quién los tiene y cómo se podrían obtener.

D4. Correcciones a las cifras citadas en la conversación con el autor
Comprueba en su fuente original cada cifra de D2 y de D3 tomada de prensa y anota en docs/v17/correcciones.md las que no coincidan. Ninguna entra en el documento sin pasar por esa comprobación.

══════════════════════════════════════
E. PARADAS
══════════════════════════════════════
- Una cifra publicada que cambiaría de valor o de capa.
- Un acceso a muestras selladas fuera de src/holdout.py.
- Una conclusión de la 1.0 o del informe integral que la auditoría muestre falsa (no solo matizable): se documenta y se espera mi decisión.
- Más de 4 millones de tokens de subagentes en una fase.

En cada parada y al final de cada fase, resumen de 250 palabras como máximo.

Empieza ahora: plan.md y fases 0, 1, 2, 3 y 5 seguidas; después V18 según el encabezado.
