# Registro de cambios

Formato: versión, fecha y cambios principales. Las correcciones de resultados ya publicados van en ERRATA.md.


## V10 (2026-10-14): difusión — base única, atlas descriptivo, figuras, web y monitor (sin modelos nuevos)

- **Base de datos única** (`make base`):
  - tabla larga en DuckDB y Parquet, con capa, fuente, edición, fecha, licencia y marcas `posterior_prereg` y `muestra_sellada_v6`;
  - dimensiones territoriales con jerarquía y geometrías;
  - capa pública solo redistribuible.
- **Atlas descriptivo** (`make atlas`):
  - quién soporta el coste de la vivienda: ECV y EPA con intervalos;
  - entrar frente a quedarse: IPVA;
  - València por sección y barrio, Comunitat Valenciana por municipio, provincias y ciudades comparables.
  - Ids `V10-ATL-*` en cifras_clave: 28 cifras nuevas; ninguna cifra publicada cambia.
- **Figuras** con estilo único y ficha (`make figuras`).
- **Web estática** (`make web`; GitHub Pages) y **monitor** mensual: el monitor abre un pull request y no publica sin revisión.
- **Manuscrito** en Quarto (las secciones de v9 están pendientes) y **Excel** del atlas.
- **Orden del repositorio.** 9 documentos de proceso de V7-V7.2 pasan a historico/.
- **Corrección de licencias** de la capa pública: la base intermedia de los commits bc0f83b y 4e0c4a8 incluía dos variables agregadas de Registradores (docs/v10/decisiones.md, D5).

## v8.1, bloque A (2026-10-13): coherencia de redacción y tablas de V8; V8 pasa a versión de referencia
- **Sin análisis nuevo.** No se estima ningún modelo ni se abre ninguna muestra sellada. **Ninguna cifra publicada cambia**: las 716 filas de cifras_clave previas a V8 y las cifras de V8 (v8.0) son idénticas (src/v8/check_v8.py, `cifras_previas`). Por eso no hay entrada nueva en ERRATA.md. Solo se añaden cifras (ids nuevos, C4, leídos de output/v8/ en src/v8/f6_hechos.py) y se precisa la redacción.
- **Lectura del multiverso por variables** (regla de §9 aplicada a cada variable): ids `V8-M7-var-…` (cumplen, total, y para cada combinación que cumple, % de mismo signo y % significativo tras BH). Se distingue de la lectura por familias. Se aclara que la regla de periodo de M0 en el alquiler es «no evaluable» (no hay medida alternativa trimestral), no incumplida (ids `V8-M0-evaluables`, `V8-M0-no-evaluable`, `V8-M0-no-evaluable-alquiler`).
- **Avisos de lectura.** Colinealidad entre población total y extranjera (ids `V8-M6-vif-…` y `V8-M6-colpob-…`); signo del tipo real con el precio (inflación en el tipo real y en el deflactor, y sentido inverso no descartado), sin lectura causal.
- **Remisiones.** El alquiler real (IPC, parque de contratos) remite a las cifras C1 de contratos nuevos A23-A9 y A23-A10 (vigentes; no figuran en cifras_superadas.csv). València: valor tasado y Registradores discrepan en la provincia y la ciudad solo tiene valor tasado. Frase de resumen sobre la parte no atribuida en la compra de 2022-2026.
- **Entregables.** Apartado V8 en lo_que_sabemos y una_pagina (plantillas de v5) y en que_cambio; README, CLAUDE.md y LEEME_PRIMERO apuntan a v8 como referencia y al verificador V8 como vigente; la adenda V8 del historial se regenera con las cifras por variable. `make publicacion` regenera antes de copiar (render v5 y render v8).
- **Tests.** tests/v8_1/test_v81.py: ningún entregable V8 ni de publicacion/ usa un id de cifras_superadas.csv ni cita una cifra superada.

## v7.2 (2026-10-13): correcciones previas a la release
- **cifras_clave.** Se retiran 8 cifras superadas: deficit_2124_c1, T3-H1, deficit_2124_c2, T3-H2, T3-H3, T3-H4, L3-DEF-2124-CONBAJAS y B1-H1. Pasan a output/v5/cifras_superadas.csv con su sustituta y motivo.
  - Queda una sola cifra de déficit con bajas: L3-DEF-2124-BAJAST1, con las bajas estimadas en v5.1. Se elimina el supuesto de bajas del 0,1-0,2 %.
  - El test de cifras superadas revisa ahora también cifras_clave.csv.
- **Construcción adicional.** Dosis no nula por CCAA: mínimo entre la necesidad T3 y la capacidad observada de visados 2007-2025. Se reestima con la misma fórmula e incertidumbre (output/v7_2/construccion). Tablas, atlas y Excel actualizados, con la hoja CONSTR_v72.
- **Rebaja de impuestos y costes de construcción.** No difundible, por sobrestimación de diseño.
- **R5.** Todas las tablas rotulan su comparador (columna comparador_tipo; base fuerte frente a base más exigente). Las cifras y la congelación no cambian (sha256 93795a94…).
- **GSADF nacional.** Reverificado con el mismo método, la misma semilla y BH: 14 de 14 series idénticas. Ficha V72-BURBUJA, que reúne el resultado nacional y el regional; «no se puede afirmar» en ningún sentido.
- **ERRATA:** 4 entradas.

## v7.1 (2026-10-12): consolidación final y estructura para publicación (versión de referencia)
- **Sin análisis nuevo.** No se estima ningún modelo nuevo ni se abre ninguna muestra sellada. La v7.1 pasa a ser la versión de referencia y la v6.2, histórica.
- **S1 · Dosis y coste** (output/v7_1/S1). Para cada instrumento de R6 y cada CCAA:
  - dosis (viviendas o compraventas), horizonte y coste fiscal anual cuando hay base;
  - coste por punto de reducción, con rango;
  - efecto por cada diez mil viviendas y por cada cien millones de euros anuales.
  
  Donde no hay base, «coste no estimable» y su motivo. Se actualizan el atlas (sección 6 bis), el Excel (3 hojas con colores de entrada, cálculo y enlace) y el verificador (V7-V2).
- **S2 · Nota metodológica** (publicacion/nota_metodologica.md): estimadores de panel regional con un factor común no estacionario. Literatura con DOI verificado; cuartiles no verificados (Scimago 403).
- **S3 · Consolidación.**
  - cifras_clave incorpora V7 y V7.1, solo con filas nuevas.
  - Entregables actualizados con el componente común, la ausencia de largo plazo regional, el traslado de las ayudas y del ITP/IVA (C4) y la dosis y el coste.
  - Sección única «Qué cambió entre versiones y por qué».
  - Pendientes de auditoría de redacción resueltos (docs/v7_1/pendientes_auditoria.md).
  - Test de cifras difundibles.
- **S4 · Ensayo de `make evaluate_v7`** con datos futuros simulados: superado. Protocolo de 2027 con el calendario del INE (docs/v7_1/evaluacion_2027.md). Desviación declarada antes de abrir: alquiler 2026T3.
- **S5 · Estructura para el lector.**
  - publicacion/, metodologia/ y reproducir/ se generan con `make publicacion` y un test lo comprueba.
  - historico/ recibe, con `git mv`, los documentos de versiones cerradas que no lee ningún script, más archive/.
  - LEEME_PRIMERO.md con itinerarios; README y MAPA actualizados; test de enlaces.
- **S6 · Paquete de publicación:** release notes, tareas del autor y guía del revisor (docs/v7_1).
- **Cambios en cifras publicadas: ninguno.** La cifra dh_2125 declara en sus fuentes que la ECP es un stock a 1 de enero y la EPA una media anual (K4b-dh); el número no cambia.

## v7.0 (2026-10-12): atlas econométrico regional

**Panel y herramientas.**
- Panel trimestral de las 17 CCAA (2007T1-2026T2), ampliado con paro, hipotecas, dummies regulatorias, exposición regional y shocks nacionales comunes.
- Panel provincial de las 52 provincias.
- MG, PMG, DFE, CS-ARDL y CS-DL, CIPS, «tipo Westerlund», Pedroni y Hausman, validados con Monte Carlo (docs/v7/validacion_herramientas.md). Con un factor común I(1) de cargas heterogéneas ningún estimador es apto, de ahí la regla de triangulación entre MG_dm, PMG_dm y CS-DL.

**Pre-registro.** Etiqueta local `prereg-v7`. Validación limpia diferida con `make evaluate_v7` y modelos congelados (sha256 en docs/v7/notas_release.md).

**Resultados** (C4; informativos, porque la muestra ya se vio en v1):
- Ninguna de las 7 hipótesis de largo plazo se confirma y no se establece cointegración.
- La velocidad de ajuste no es significativa frente al valor crítico simulado.
- I(2) no se descarta en 8 de 17 CCAA.
- Las proyecciones locales no dan una respuesta robusta a los tipos.
- Zonas tensionadas: asociación de corto plazo, sin descartar pretendencia.
- Backtest: el mejor modelo bate a la base más exigente en 6 de 17 CCAA en alquiler y en 5 de 17 en compra.

**Propuestas** (condicionales, C4). Robustas, es decir, sin subida del precio de mercado: movilización de vacías, vivienda pública e impuestos a la construcción en la mayoría de CCAA. Las ayudas a la demanda y la rebaja de ITP/IVA reducen el esfuerzo del beneficiario pero suben el precio de mercado.

**Entregables.** output/v7/atlas (17 fichas), atlas_resumen.md, tablas_regionales.xlsx, anexo de ecuaciones, guía de lectura y verificador V7 aparte.

**Reproducibilidad.** `make v7`, ejecutado dos veces en un clon limpio, da md5 idénticos.

## v6.3 (2026-10-12): correcciones de los pendientes de v6.2 (R0 de V7)

- **D2** reparte ahora la necesidad de T3 (v5.1, base sin X) en lugar de la de B1 (v5). Cobertura de P-D: del 29,1 % (11,6-46,5) al 29,7 % (11,9-47,5); necesidad de la clase 1: de 189.335 a 185.283 viviendas/año. Detalle en ERRATA.md.
- **8 de las 26 cifras del verificador** que no estaban en cifras_clave se incorporan (output/v6_3/VER); las demás son parámetros de diseño o no tienen origen trazable.
- **cifras_clave** incluye la columna `sentido_min_max`: 70 filas cuyo min/max no es un rango.
- **Nuevo test** de cruces territoriales por código INE.

## v6.2 (2026-10-12) — cierre final para revisión externa

**Anexo metodológico (L1).** output/v6_2/anexo_metodologico.md tiene una ficha por cifra publicable: 17 completas y 49 breves, con fuente, filtros, fórmula, supuestos, capa y script.

**Segunda doble implementación (L2).** Escrita solo con el anexo y data/raw, reproduce 15 de 15 cifras. Se ejecuta en `make check` (tests/doble_impl), y sus 11 precisiones se incorporaron al anexo.

**Déficit (L3).** Se recalculó con siete correcciones del salto de la EPA en 2021 y dos fuentes de terminadas. El déficit 2021-2024 pasa de C1 a cota C2: 389.361-710.542 viviendas sin bajas (596.371-710.542 sin las variantes que conservan el salto). Con las bajas estimadas, 389.361-765.994 (C4). La ficha V05 se sustituye por L3-V1 y se responde a la objeción A-01.

**Inmigración (L4).** Se separan la asociación total (sin controlar por población) y la directa (a igual población); controlar por población es un mal control. Sigue en C4, «analizada, no concluyente».

**Coherencia de cifras (L5).** docs/v6_2/cifras_publicables.md y un test contra cifras superadas.

**Revisión (L6).** docs/v6_2/guia_revisor.md y docs/v6_2/tareas_autor.md.

**Cifras publicadas que cambian** (ERRATA.md):
- déficit 2021-2024: de C1 562.692-688.692 a C2 389.361-710.542; con bajas estimadas, de 562.692-744.144 a 389.361-765.994;
- contratos nuevos de la Comunitat Valenciana: de 27,7 % a 28,5 % (26,1-30,8), por la grafía «Valéncia».

## v6.1 (2026-10-11) — cierre, auditoría crítica y consolidación

**Líneas base exigentes (K1).** La comparación de modelos de v6 se repite en la misma validación sellada, con tres bases nuevas: último valor × crecimiento nacional, AR con factor común y efectos fijos dobles. Se abrieron 27 veces, una por base y tarea. El contraste es DM-HLN más permutación exacta por provincias, con Holm.
- El mejor modelo supera a la base más exigente en 6 de 9 tareas: alquiler de stock en sus tres niveles, precio de tasación trimestral, precio provincial anual (frágil) y volumen trimestral (solo en la parte espacial).
- No es distinguible en precio municipal, con Registradores y en volumen anual.

**Reconciliación (K2).** docs/v6_1/historial_conclusiones.md. Para la inmigración, el cambio entre v2 y v6 lo mueven el método (2SLS frente a MCO), la medida de alquiler y los controles; la población puede ser mediadora. Conclusión única: C4, «ANALIZADA, NO CONCLUYENTE».

**Interpretación (K3).**
- Las iniciadas se asocian con el alquiler solo en el mismo año; sus retardos y adelantos no se distinguen de cero.
- Léxico predictivo y asociativo en lugar de «pesa», «explica» o «importa».
- Ratio precio/alquiler con un rango por medida.

**Auditoría (K4).** Hallazgos: 0 críticos, 5 altos (corregidos), 13 medios y 12 bajos. Ver historico/docs/v6_1/auditoria.md.
- Doble implementación de las 15 cifras: 6 coinciden, 4 parciales explicadas y 5 no reconstruibles solo con el texto.
- 32 tests nuevos; k4c y k4d entran en make.

**Revisión por pares simulada (K5).** Árbitro académico: revisión mayor. Árbitro de política: revisión menor. Se aplicaron 18 cambios de texto y 11 objeciones pasan a limitaciones (historico/docs/v6_1/carta_respuesta.md).

**Cierre (K6).**
- Sección «Qué cambió entre versiones y por qué» en los entregables.
- Fichas del verificador K1-V1 y K2-V1.
- docs/v6_1/backlog.md y historico/docs/v6_1/tareas_autor.md, que es la lista definitiva.

**Cifras publicadas que cambian** (ERRATA.md):
- contratos nuevos de la Comunitat Valenciana: de 26,6 % (22,4-30,8) a 27,7 % (24,6-30,8);
- recuentos de 1.000.000 o más: hasta 5 unidades.

## v6.0 (2026-10-11)

Alquiler y compraventa: qué explica y qué predice (módulos M0-M4; decisiones en docs/v6/decisiones.md). Todo es C4; ninguna cifra existente cambia de valor ni de capa.

Cifras nuevas en output/v5/cifras_clave.csv:
- Leídas de output/v6/*/hechos.json: `M0-*` (paneles y sellado), `m1a_*` (asociaciones con el alquiler de stock en €/mes), `m1b_*` (elasticidad precio-alquiler, ratio precio/alquiler, rentabilidad bruta y coste de uso, GSADF por CCAA, Durbin espacial), `m2_pip_*` (PIP del BMA por mercado), `m3a_*` y `m3b_*` (validación interna) y `V6-M4-*` (error sellado del mejor modelo y de la persistencia, variables «relevantes con seguridad»).
- Auxiliares nuevas en `src/v5/e_hechos_v6.py` (ids `E-V6-`): provincias selladas y de entrenamiento, PIP del BMA núcleo, deep learning frente a gradient boosting (M3a y M3b), persistencia en la validación interna trimestral, parte temporal sellada del volumen trimestral, recuentos de confirmatorias que pasan Holm y de CCAA con exuberancia GSADF.

Capas: todos los resultados v6 son C4 (predicción y asociación). Ninguna hipótesis confirmatoria pasa Holm (`E-V6-M1A-HOLM`, `E-V6-M1B-HOLM`); ninguna variable es «relevante con seguridad» (`V6-M4-N-REL`); la identificación disponible no alcanza C3. Validación sellada espacial nueva (11 provincias) y temporal ya vista en v2 y de forma descriptiva en v4-v5.

Entregables:
- informe_tecnico: sección nueva 11, «Alquiler y compraventa: qué explica y qué predice (v6)» (medidas, validación sellada y su limitación, mejor modelo por mercado, medida y nivel, peso de cada variable con las discrepancias M2/M4, relación entre mercados, diferencias provinciales y resultados negativos); punto nuevo en 10.1.
- working_paper: subsecciones 4.5 (resultados) y 5.5 (validación sellada y negativos).
- lo_que_sabemos: tres ítems v6 en «Probable pero no demostrado (C4)» y dos en «No se puede afirmar». «Afirmable con seguridad» no cambia (solo C1 y C2).
- policy_brief: párrafo «Alquiler y compraventa: qué predice y qué no (v6)» y punto en «Lo que este brief no afirma».
- una_pagina: línea nueva en «Lo que NO se puede afirmar».
- `src/v5/render.py`: los recuentos en «variables», «hipótesis» y «CCAA» se muestran como enteros.

Auditoría del repositorio para su publicación (módulo G, 2026-10-11; detalle en historico/docs/v6/auditoria.md):
- README.md principal y docs/MAPA.md (vigente frente a histórico).
- Salidas superadas de v3 y v4 trasladadas a historico/ con `git mv` (registro en historico/archivo_v6_README.md): output/v3/{articulo, informe_politica, lo_que_sabemos}.md y output/v4/{working_paper, policy_brief}.md. Ninguna cifra cambia.
- Makefile: `src/v5/a5_validacion.py` y `src/v5/b3_potencia.py` entran en `V5_ORDEN`; ya generaban salidas versionadas y reproducen los mismos ficheros byte a byte.
- CITATION.cff, .zenodo.json y README_REPLICACION.md pasan a la versión 5.1.
- Rutas locales absolutas eliminadas de documentos internos (docs/v2, docs/v5, docs/v5_1, docs/fallidas).

## v5.1 (2026-10-11)

Cifras y capas cambiadas en los entregables (todas desde output/v5/cifras_clave.csv):
- Déficit 2021-2024 con bajas: `deficit_2124_c2` (cota C2 hasta 902.808, bajas supuestas del 0,1-0,2 %) → `T3-H2` (C4, hasta 744.144, bajas estimadas en T1). Motivo: ningún dato observado respalda el supuesto de v4. `deficit_2124_c1` (C1, sin bajas) no cambia.
- Bajas del parque: supuesto de v4 del 0,1-0,2 % anual → tasa C4 de T1 (0 / 0,026 % / 0,052 %, máximo de las demoliciones con licencia); cota física 0 en C2. Motivo: las identidades de stock dan bajas negativas y las demoliciones con licencia son 0,02-0,04 % del parque.
- Necesidad 2026-2035: `B1-H1` / `E-B1-anual` (94.000-310.000 al año, C4) → base `T3-H5b` (99.000 / 210.000 / 292.000, C4) con la sensibilidad `T3-H5` (124.000 / 246.000 / 339.000, C4). Motivo: reposición con las bajas de T1 y componente X de T2, que suma.
- Nuevo: descomposición del rango de la necesidad (movilizables 34 %, el supuesto que más pesa) y frase frente a la producción con la misma cobertura (`T3-H9`, 1,4 / 2,7 / 3,8 veces). Motivo: revisión de v5.1 (B1).
- Proyección 2026-2030: `B2-H1` y `B2-H6` (C4; provincias 20 / 5 / 27) → `T4-H1`, `T4-H2` y `T4-H3`: dirección nacional «empeora» en C2 (180 escenarios), magnitud C4; provincias 15 / 0 / 37. A 2035, dirección indeterminada (C4). Motivo: rejilla de T4 que separa dirección y magnitud.
- Liberadas por envejecimiento: `E-B1-L` (1,42 M en diez años, C4) → `T2-H1` (1,86 M en 2026-2035, C4), con la parte que llega al mercado (`T2-H6`), el reparto por tipo de municipio y el desajuste territorial; frase explícita de que no se restan de la necesidad en todos los entregables. Motivo: T2.
- Verificador: ficha `B2-V1` → `T4-V1` (NO RESPALDADA, C2); la ponencia cita `T2-V1` para el mito del envejecimiento.
- Cifras auxiliares nuevas en `src/v5/e_hechos_t7.py` (ids `E-T7-`): demoliciones con licencia en 2024 en % del parque, terminadas con País Vasco y Navarra, pesos de la descomposición y liberadas por tipo de municipio.

## v5.0 (2026-10-10)
- Módulo R. Se recuperan pendientes:
  - no residentes por provincia;
  - conciliación VUT INE/GVA;
  - efecto donut;
  - sensibilidad de Oster y Cinelli-Hazlett en los diseños de v2;
  - GSADF con tamaño corregido;
  - tabla de quién posee las viviendas;
  - capacidad de la construcción;
  - pendientes técnicos (ficheros >50 MB, ediciones del Notariado, distritos SERPAVI).
- Módulo A. Tabla única de cifras clave (output/v5/cifras_clave.csv), puente IPV frente a núcleo de precio, alquiler de stock frente a contratos nuevos (fianzas), coste oficial y reclasificación territorial, y programas oficiales con búsqueda por palabras clave.
- Módulo B. Necesidad 2026-2035 por provincia, proyección del déficit a 2030, diferencias entre provincias (pre-registrado: `prereg-v5`) y contribuciones a la subida.
- Módulo C. Comparación europea, crédito a promotores, compras al contado, seguridad jurídica, fiscalidad del alquiler, peso de las empresas, desigualdad y salidas del régimen de protección.
- Módulo D. Matriz de instrumentos completa, política por territorio y convergencia con otros organismos.
- Módulo E. Paquete de publicación.
- Puerta `make check` ampliada (check_v5): cifras de los entregables leídas de cifras_clave, suma provincial = nacional, lecturas versionadas y recuentos oficiales.

## v4 (2026-10-10)
Geografía del déficit, descomposición de hogares, factibilidad, parque frente a mercado, evaluación de instrumentos, preguntas abiertas y verificador ampliado.

## v3, v2, v1
Véanse historico/docs/v3/estado.md, docs/v2 y output/informe.md.
