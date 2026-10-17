V15 · Estudio completo de la vivienda en España con toda la información disponible, en la línea del repositorio. Objetivo: el análisis más profundo y riguroso que permitan los datos. La credibilidad manda sobre la cantidad: un resultado nulo bien identificado vale más que diez asociaciones frágiles. Sé crítico con los datos, con los métodos, con la literatura y con los resultados previos de este repositorio.

Lo primero, antes de nada más: guarda este mensaje completo, sin resumir, en docs/v15/plan.md, haz commit y añade a CLAUDE.md la línea «V15 en curso: leer docs/v15/plan.md y docs/v15/estado.md al empezar cualquier sesión o tras compactar el contexto». Si el contexto se compacta, vuelve a leer plan.md y estado.md antes de seguir.

══════════════════════════════════════
A. REGLAS (prevalecen sobre todo lo demás)
══════════════════════════════════════
- Lectura previa: CLAUDE.md, proyecto.json, metodologia/capas.md, anexo_metodologico.md, historial_conclusiones.md, preregistro_v7.md, preregistro_v8.md, preregistro_v9.md y su addendum, docs/v8/decisiones.md, docs/v9/, docs/v10/diccionario_base.md, docs/v11/ a docs/v14/ (en especial docs/v14/licencias.md y escenarios), docs/literatura.md y docs/limitaciones.md.
- La versión pública 1.0 no se toca: ninguna cifra de cifras_clave cambia de valor (check_v13). V15 solo añade cifras V15-* y se publicará como 1.1.
- data/sealed y la evaluación de 2027 no se tocan. Prohibido make clean, make all, make v7 y make evaluate_v7. Ficheros con Write o heredoc entrecomillado.
- Capas C1, C2, C3 (instrumento externo o diseño que supera todas sus pruebas), C3s (restricciones de signo explícitas) y C4. Nunca promover de capa. Sin lenguaje causal fuera de C3/C3s. Ningún modelo se elige por p-valor. Atribuciones con bandas. Multiverso de 50.000 especificaciones como máximo. Holm para confirmatorias y BH para exploratorias. Toda especificación al Registry de src/econ_utils.py.
- Predicción: misma muestra contra AR(4) y ECM v1; validación temporal en bloques con embargo. Solo «predice mejor» si supera a la línea base más exigente (Diebold-Mariano o Giacomini-White, Clark-West si hay anidamiento) y entra en el Model Confidence Set.
- Cruces territoriales solo por código INE. Interpolaciones y fuentes no validadas solo en robustez. Si dos métodos discrepan, se reportan ambos.
- Terceros según proyecto.json (terceros_1_0): Anuario ERI, Notariado y AEAT solo como agregados propios citando la fuente; Registradores (datos abiertos) bajo ODbL. Ninguna serie no redistribuible sale del repositorio de desarrollo.
- Neutralidad: se evalúan afirmaciones e instrumentos, nunca partidos ni personas.
- Trabajo en docs/v15/ (plan.md, estado.md, decisiones.md, bloqueos.md, tareas_autor.md), src/v15/, output/v15/ y tests/v15/. Actualiza estado.md tras cada tarea (hecho, siguiente, subagentes y tokens). Commit por tarea; push solo a la rama designada.
- Un solo `make check` a la vez, nunca en paralelo con otro proceso que escriba en el repositorio.
- Excel: azul los datos introducidos (con su fuente en nota), negro lo calculado en la hoja, verde lo que viene de otra pestaña. Sin paneles inmovilizados. Maquetación limpia.

══════════════════════════════════════
B. INFRAESTRUCTURA (hazla entera antes de la fase 0)
══════════════════════════════════════
B1. Guardas en .claude/settings.json (fusiona con lo existente):
   - permissions.deny: lectura y escritura de data/sealed/**; Bash con make clean, make all, make v7, make evaluate_v7, git push --force, git filter-repo, rm -rf data y rm -rf output.
   - Hooks PreToolUse para Bash en .claude/hooks/:
     (a) rechazar heredocs sin comillas;
     (b) rechazar comandos que mencionen data/sealed salvo vía src/holdout.py;
     (c) rechazar un segundo make check si ya hay uno en marcha (bloqueo en /tmp);
     (d) rechazar make v15_f4* y make v15_f5* si proyecto.json no tiene osf_prereg_v15.
   - tests/v15/test_guardas.py que demuestre que cada guarda bloquea. Después intenta tú `make clean` y leer data/sealed, y confirma que fallan. Si no fallan, para y avísame.

B2. Subagentes en .claude/agents/ (frontmatter name, description, tools, model; tope de tokens en la descripción; devuelven rutas, un resumen de 200 palabras como máximo y resultado.json, nunca datos crudos):
   - inventariador (haiku; Read, Grep, Glob): variables, coberturas y definiciones desde manifiestos y diccionarios.
   - auditor-datos (sonnet; Read, Grep, Glob, Bash de lectura y python): audita un grupo de fuentes → output/v15/auditoria/<grupo>/.
   - lector-literatura (sonnet; WebSearch, WebFetch, Read, Write solo en docs/v15/literatura/): una pregunta por invocación; fichas solo de lo leído; todo NO VERIFICADA hasta pasar el verificador.
   - montecarlo (sonnet; Read, Write, Bash): valida un estimador con el proceso generador declarado.
   - modelizador (sonnet; Read, Write, Edit, Bash): un módulo pX en src/v15 con su resultado.json; no toca módulos ajenos ni econ_utils.py.
   - revisor-preregistro y arbitro-final (opus; Read, Grep, Glob; sin Write ni Bash): críticos independientes que no hayan participado en el trabajo, con hallazgos numerados y veredicto.
   Si algún modelo no está disponible, usa el más cercano y anótalo en decisiones.md.

B3. Herramientas deterministas en src/v15/:
   - verificar_referencias.py: DOI → Crossref (título, autores, año, revista); revista → cuartil Scimago desde un CSV versionado con fecha; marca VERIFICADA / NO VERIFICADA / DISCREPANTE y falla si una ficha cita un DOI inexistente.
   - registro_subagentes.py: anota en estado.md el rol, la tarea, los tokens aproximados y los ficheros tocados.

B4. Comandos en .claude/commands/ (v15-fase0 … v15-fase5 y v15-estado) y objetivos de Makefile (v15_f0 … v15_f5, v15 y check_v15 dentro de make check). Cada comando lee plan.md y estado.md, ejecuta solo su fase y termina con make check en solitario, commit, push y un resumen.

B5. Comprueba: tests de las guardas en verde y make check limpio. Commit «V15 infraestructura».

══════════════════════════════════════
C. FASES
══════════════════════════════════════
FASE 0 · Punto de partida
1. Comprueba que V14.4 está aplicada (todas las fuentes en «agregados», las 16 cifras reincorporadas). Si no, aplícala según docs/v14 y verifica.
2. docs/v15/punto_partida.md (3 páginas como máximo):
   - preguntas sin respuesta en V5-V12 y la causa (datos, potencia, identificación o variación);
   - resultados previos frágiles y por qué;
   - errores o debilidades que veas aunque no estén en ERRATA: se listan para revisión, no se corrigen aquí.

FASE 1 · Auditoría de datos (en paralelo: inventariador + hasta 3 auditor-datos por grupo: precios de compra, alquiler, oferta y parque, demografía y hogares, turismo, financiación y macro, renta y microdatos)
1. Inventario único de todas las variables (base V10-V14, data/raw, data/manual). Para cada una:
   - frecuencia y cobertura;
   - nivel territorial;
   - definición exacta (tasado frente a transacción, contratos vigentes frente a nuevos, stock frente a flujo);
   - fuente, licencia y vintage;
   - rupturas (EPA 2021, seccionado, cambios de base del IPV y del IPVA);
   - porcentaje de imputación.
   Resultado: docs/v15/inventario_variables.md y su .csv.
2. Calidad (output/v15/auditoria/):
   - atípicos robustos (MAD);
   - coherencia entre fuentes de precio de compra (MIVAU, Notariado, Registradores, INE IPV) y de alquiler (SERPAVI, IPVA, fianzas, IPC): niveles, tasas y periodos de divergencia;
   - revisiones entre vintages;
   - sesgo de composición en precios medios frente a índices ajustados por calidad;
   - unidades dudosas (AEAT 2013-2015);
   - reparto espacial de V12-B1: reparto alternativo por viviendas del Catastro como variable alternativa, documentando cuál usa cada análisis.
3. Potencia por pregunta candidata: clusters efectivos (17 comunidades, 50 provincias, municipios, barrios), T y efecto mínimo detectable al 80 %. Sin potencia, se descarta antes de estimar.
Ningún efecto estimado en esta fase.

FASE 2 · Bibliografía crítica (en paralelo: hasta 3 lector-literatura, uno por pregunta; después verificar_referencias.py sobre todo)
1. docs/v15/literatura.md, por pregunta:
   - evidencia internacional y española;
   - diseño, validez externa para España y discrepancias.
   Fuentes: Crossref, OpenAlex y versiones abiertas (Banco de España, BCE, NBER, SSRN, repositorios). Nunca se cita lo no leído al menos en su resumen; nunca se inventan referencias ni resultados.
2. Puntos de partida a verificar, no a dar por buenos:
   - oferta (Saiz; Glaeser y Gyourko; estudios españoles);
   - coste de uso (Poterba; Himmelberg, Mayer y Sinai);
   - burbujas (Phillips, Shi y Yu);
   - paneles con dependencia transversal (Pesaran);
   - DiD escalonado (Callaway y Sant'Anna; de Chaisemartin y D'Haultfoeuille; Borusyak, Jaravel y Spiess; Rambachan y Roth; SDID de Arkhangelsky et al.; control sintético);
   - shift-share (Borusyak, Hull y Jaravel; Goldsmith-Pinkham, Sorkin y Swift; Adão, Kolesár y Morales);
   - proyecciones locales (Jordà);
   - pisos turísticos (García-López et al. sobre Barcelona y posteriores);
   - inmigración (Saiz; González y Ortega para España);
   - topes al alquiler (Diamond, McQuade y Qian; evaluaciones europeas y de la Ley 12/2023);
   - transmisión de tipos en España (Banco de España);
   - predicción y combinación de pronósticos.
3. Por pregunta: qué resultado sería sorprendente replicar o no replicar, y por qué.

FASE 3 · Preguntas y pre-registro (PUERTA OBLIGATORIA)
1. Elige entre 6 y 10 preguntas con potencia, priorizando identificación creíble. Candidatas (descarta o reformula con argumentos):
   - P1 Oferta: elasticidad por municipio o provincia instrumentada con restricciones físicas (pendiente, agua, suelo protegido; Catastro, INSPIRE, MDT) y su relación con la respuesta del precio a shocks de demanda.
   - P2 Fundamentales: precio frente a coste de uso y alquiler; cointegración en panel con dependencia transversal (CIPS, Westerlund, CS-ARDL, PMG/MG); velocidad de ajuste.
   - P3 Tipos: proyecciones locales ante sorpresas de alta frecuencia del BCE, con exposición por peso de la hipoteca variable; Driscoll-Kraay.
   - P4 Inmigración: shift-share municipal y por barrio de València (padrón 2001-2026, afiliación BDO); AKM, Rotemberg y pretendencias.
   - P5 Pisos turísticos: Barcelona por barrio (HUT 2018-2026), Comunitat Valenciana y València; regulación municipal y COVID; DiD escalonado con Honest DiD.
   - P6 Topes y zonas tensionadas: periodos 2024-2026; SDID y control sintético por municipio; precio, contratos y desplazamiento a temporada o compra.
   - P7 Demografía y necesidad: hogares (V12-B3) frente a obra nueva (B4) por municipio; presión de demanda y respuesta del precio.
   - P8 Distribución: esfuerzo de acceso por renta, edad, nacionalidad y tenencia (ECV y Censo); Oaxaca-Blinder o reponderación DFL 2018-2025.
   - P9 Predicción: DFM, combinación, BVAR, penalizados con validación temporal y nowcasting (compraventas, hipotecas, visados), frente a AR(4) con DM/GW/CW y MCS.
   - P10 Espacial: SAR, SDM y SEM municipales, efectos directos e indirectos, errores de Conley.
2. docs/v15/preregistro_v15.md, por pregunta:
   - hipótesis, estimando, diseño y supuestos;
   - pruebas para C3 (pretendencias, placebos temporales y espaciales, sensibilidad, exclusión de unidades, pocos clusters con wild cluster bootstrap de pesos Webb, aleatorización);
   - especificación principal y multiverso declarado;
   - corrección múltiple;
   - potencia y efecto mínimo detectable;
   - qué resultado cambiaría cada conclusión del historial;
   - qué se hace si no pasa las pruebas.
3. Validación sellada nueva con src/holdout.py (sellar_v15 y evaluate_v15, con registro de accesos), ANTES de cualquier estimación:
   - datos publicados después del depósito del pre-registro (lista de publicaciones y fechas esperadas);
   - un bloque espacial elegido al azar con SEED=20261010.
   Declara qué muestras ya se vieron en versiones anteriores: son solo informativas.
4. revisor-preregistro: debilidades, sesgos de elección y alternativas. Incorpora o rebate cada punto en un addendum.
5. Etiqueta local prereg-v15 y texto exacto para OSF en docs/v15/tareas_autor.md.
6. DETENTE. Las fases 4 y 5 no empiezan hasta que yo ponga osf_prereg_v15 en proyecto.json (el hook lo garantiza). Al reanudar, comprueba que la fecha del depósito es anterior a cualquier estimación.

FASE 4 · Estimación (solo tras la puerta)
1. montecarlo valida cada herramienta nueva (SDID, control sintético, Honest DiD, AKM, Conley, MCS, DFM, BVAR, espaciales) con nuestro proceso generador (T, N, dependencia transversal, pocos clusters) antes de usarla → metodologia/validacion_montecarlo_v15.md.
2. Hasta 3 modelizador en paralelo sobre preguntas independientes, en worktrees ../wt-v15-pX según la regla del repositorio. Primero la especificación pre-registrada, después el multiverso declarado. Cualquier desviación va a metodologia/desviaciones_v15.md con su motivo.
3. Diagnósticos según el caso:
   - raíces unitarias y cointegración con dependencia transversal;
   - rupturas (Bai-Perron);
   - heterocedasticidad y autocorrelación;
   - instrumentos débiles (F efectivo de Montiel Olea-Pflueger, intervalos AR);
   - pretendencias y potencia de Roth;
   - balance;
   - ajuste preintervención;
   - Moran en residuos;
   - exclusión de Madrid, Barcelona, Baleares, Canarias y València.
4. Doble implementación (tests/doble_impl) de cada candidata a C3/C3s.
5. evaluate_v15: una vez por hipótesis confirmatoria, registrada.

FASE 5 · Síntesis crítica e integración
1. output/v15/informe_v15.md:
   - por pregunta, resultado, capa, bandas, pruebas superadas y fallidas;
   - comparación con la literatura y por qué puede diferir;
   - limitaciones;
   - qué cambia en el historial.
   Toda cifra sale de cifras_clave (V15-*). Sin lenguaje valorativo.
2. Adenda al historial de conclusiones y verificador V15.
3. tablas_v15.xlsx, figuras con el estilo del repositorio, sección en el manuscrito Quarto y páginas web.
4. arbitro-final (tope de 100.000 tokens) como árbitro de revista Q1 de economía urbana: ACEPTAR, REVISAR o REHACER, con hallazgos numerados. Corrige o rebate por escrito cada uno.
5. make v15, check_v15 en make check (ninguna cifra 1.0 cambia; toda cifra V15 con ficha y capa; sin lenguaje causal fuera de C3/C3s), make publicacion, make web y make check limpios; git sin cambios tras check. Prepara la 1.1 con make arbol_publico y el escaneo de terceros.

══════════════════════════════════════
D. CONDICIONES DE PARADA (detente y explícame)
══════════════════════════════════════
- La puerta de la fase 3 (obligatoria).
- Que alguna guarda de B1 no bloquee lo que debe.
- Que alguna cifra de la 1.0 fuese a cambiar de valor.
- Cualquier necesidad de acceder a data/sealed o a la evaluación de 2027.
- Un hallazgo que contradiga una conclusión publicada en la 1.0: no se publica, se documenta y se espera.
- Un error de versiones anteriores que cambie una cifra publicada: a ERRATA en versión posterior, nunca se reescribe.
- Datos con licencia incompatible o descargas no automatizables: a tareas_autor.md, y sigues con lo demás.

En cada parada, resumen de 250 palabras como máximo: qué se ha hecho, qué preguntas sobreviven y por qué, qué se ha descartado y por qué, tokens de subagentes y qué me toca hacer.

Empieza ahora: plan.md, infraestructura B, y fases 0 a 3 seguidas hasta la puerta.
