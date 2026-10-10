# Decisiones v5

## Setup
- Rama r5/main desde r4/main (9673a4c, v4 cerrada). Push a la rama remota designada.
- CLAUDE.md pasa a v5: rutas docs/v5, output/v5; reglas nuevas (cifras_clave, ficheros versionados, recuentos oficiales, suma provincial = nacional).
- Presupuesto: la suma de los límites por módulo (4,5 M) supera el total menos la reserva (3,78 M). Manda el corte global del 80 % (3,36 M). Los entregables E los redacta el orquestador para ahorrar.
- Pendiente técnico detectado al empezar: `data/raw/gva_vut_municipio.csv` (67 MB) está versionado (>50 MB) → R1.
- R1 técnico. `gva_vut_municipio.csv` (67 MB):
  - deja de versionarse y pasa a .gitignore con checksum;
  - la copia versionada es `gva_vut_municipio.csv.gz` (1,2 MB, idéntica al leerla);
  - la leen build_dataset.py y m4_run.py; fetch_gva.py trata el .gz como caché y lo regenera al descargar.
- R1 técnico. Se añaden checksums de los 7 JSON ADRH (>50 MB, ignorados). Los pares «por persona» y «por hogar» son el mismo fichero de origen: cada capa trae varios indicadores (dato1-dato9), así que no es un error.

## Diseño de cifras clave (A1) y entregables (E)
- `src/v5/cifras_clave.py` construye `output/v5/cifras_clave.csv` y `.md` a partir de los resultado.json y hechos.json de v4 y v5. No hay cifras tecleadas a mano.
  - Columnas: id, indicador, valor, min, max, unidad, periodo, cobertura, fuentes, capa, fecha_dato, ficha, origen (script:clave).
- Los entregables v5 se escriben como plantillas (`docs/v5/plantillas/*.md`) con marcadores `{{id}}` o `{{id:campo}}`. `src/v5/render.py` los rellena en output/v5/.
- `src/v5/check_v5.py` entra en `make check` y comprueba:
  1. ningún marcador queda sin resolver, y toda cifra con etiqueta de capa en un entregable procede de un marcador;
  2. suma provincial = nacional en las tablas declaradas;
  3. los recuentos de programas solo usan documentos oficiales;
  4. ningún script de `make all` lee ficheros de data/raw no versionados (comprobación estática de nombres literales, excluidos los fetch);
  5. el léxico valorativo o partidista en E4, E5 y E8 (reutiliza check_texto).

## R1 técnico (orquestador)
- BK-045. Orden cronológico de las ediciones del Notariado en extract_notariado.py; queda en ERRATA.md.
- BK-046. Nombres de los 19 distritos SERPAVI de València:
  - nombres tomados de la capa oficial de distritos del Ajuntament (geoportal, CC BY 4.0, descargada el 2026-10-10, en data/raw/v5);
  - supuesto declarado: el código 46250dd corresponde al distrito municipal dd (19 = 19);
  - salida en output/v5/R1T, sin tocar output/f6 (v1 cerrada).
- BK-044. Fe de erratas de las notas de v2 en ERRATA.md, sin reescribir output/v2.
- BK-047. El blob de 95 MB de serpavi_v2_municipios.csv sigue en el historial remoto (a011c2f). No se reescribe, porque el force push está denegado; queda documentado.
- Los subagentes trabajan en el árbol principal con rutas disjuntas (src/v5/<módulo>_*, output/v5/<MÓDULO>), sin commit. No hacen falta worktrees porque no hay ficheros compartidos; esto cumple el límite de 3.

## R1a, R1b y R1c (subagentes)
- **R1a.**
  - Una frase de la ficha R1A-V1 con lenguaje causal («se debe a») se reescribe sin él.
  - BK-014 (alquiler de temporada) queda NO ANALIZADA: el agente no probó endpoints de red, así que sigue en el backlog.
- **R1b.** r1b_donut leía `serpavi_v2_municipios.csv` (95 MB, sin versionar) y pasa a leer el `.csv.gz` versionado. Lo detectó check_v5.
- **R1c.** La tenencia en propiedad es C1 (EFF, ECV y Censo, 72-76 %). En v4 el Censo era C4 por ser fuente única; ahora hay tres fuentes independientes.

## A2-A3 (subagente) y A6 (orquestador)
- **A23-V2** («el alquiler de contratos nuevos se ha duplicado»).
  - El agente había puesto una capa mixta con CONTRADICHA.
  - Por la regla B5, la cuantía nacional es de fuente única (IPVA, C4): ANALIZADA, NO CONCLUYENTE a escala nacional.
  - La contradicción en Cataluña y C. Valenciana (C1) se dice en la regla.
- **A6.** Consolidación documental de v4 M0, sin nuevas estimaciones (output/v5/A6/nota.md). check_v5 impide etiquetar los topes como C3.

## A4 (subagente + orquestador)
- **Coste oficial en nivel.**
  - Solo se obtuvo el MBC de 1993 (RD 1020/1993), actualizado con el índice de costes de Eurostat: 422-932 €/m², derivado y único para toda España.
  - Fallaron los módulos de protegida de las CCAA y el presupuesto de ejecución material de visados (docs/v5/fuentes_fallidas.md).
- **Corrección del orquestador.**
  - El MBC es un módulo de valoración fiscal y puede quedar por debajo del coste de mercado. Por eso C2 exige que la clase se mantenga en la UNIÓN del rango oficial derivado y el rango supuesto de v4 (422-1.500 €/m²).
  - Provincias C2 en 2021-2025: 8 de clase 1 y 3 de clase 2 (el agente daba 27 y 4).
  - En 2012-2025 la estabilidad solo se mide con el rango oficial, porque no hay clasificación v4 comparable; se marca así.
- **Clase 4 («no falta»).** Ninguna provincia en 2021-2025; 247 municipios.
- **Concentración del déficit.**
  - 2021-2025: 6 provincias suman el 50 % y 18 el 80 %.
  - 2021-2024: 6 y 17.
  - La suma provincial es igual a la nacional (700.934 y 562.692).
  - Las cuatro provincias forales solo tienen altas del Ministerio.

## A5 (subagente)
- **Documentos.** 25 documentos oficiales con texto extraíble:
  - 6 programas de 2023 y 1 resumen oficial;
  - la Ley 12/2023 y el RD 326/2026 (Plan Estatal 2026-2030);
  - 13 proposiciones de ley de la XV legislatura.
- **Exclusiones.** 3 programas de v4 solo existen en copias de medios: «no oficial», fuera de los recuentos. 4 formaciones no tienen programa localizado.
- **Conciliación con v4.** 41 de las 88 medidas de v4 quedan como no verificables porque no hay documento oficial. Las 47 restantes están todas en el texto oficial.
- **Búsqueda por palabras clave** (diccionario declarado en docs/v5/programas/diccionario.md).
  - Precisión: 50 % son medidas pertinentes y 78 % son medidas o menciones (40 coincidencias auditadas).
  - Recall en las citas de v4: 44 de 47, pero con calibración en la misma muestra.
  - Los recuentos son COTAS de coincidencias, no de medidas validadas (C4).
  - La dirección automática es poco fiable. La matriz D1 usará los recuentos solo como contexto, nunca para evaluar.
- **Recuentos y normas.** Las normas (ley y RD) se cuentan aparte. check_v5 deja de contarlas en «a favor».
- **Requisito de sistema.** a5_run.py usa `pdftotext` (poppler-utils), que se declara en el README de replicación.

## A1 (orquestador)
- `src/v5/cifras_clave.py` genera output/v5/cifras_clave.csv y .md (91 filas):
  - hechos.json de los módulos v5;
  - adaptadores de v4 que leen de sus JSON y CSV: déficit 2021-2024 C1 y C2, ΔH 2021-2025, terminadas 2019-2024, latente por convivencia, compradores extranjeros.
- Va en `make all`, después de los módulos v5. El .md incluye la definición de las clases territoriales (1-4 y 9).
- Alquiler de stock (A23-A2):
  - el C1 de cuantía es el NÚCLEO IPC + IPVA (10,9-22,9 %, dentro de ±15 % en nivel; encuesta frente a datos tributarios, independientes);
  - SERPAVI (+43 %) va aparte como discrepante (C4);
  - antes el rango 10,9-43 % salía como C1. Es coherente con la decisión C6 de v4.
- Pre-registro de B3: commit 8803f049c0f46ae4db8a79221470594295931d86 (etiqueta local `prereg-v5`; el push de etiquetas devuelve 403, véase bloqueos.md).

## Revisión del módulo R: REHACER (B1-B3) → corregido por el orquestador
- **B1.** El backlog añade la tabla «Estado tras R1», con lo abierto, el motivo y el coste.
- **B2.** En la discrepancia VUT, las bajas son solo una cota inferior, así que el residual por definición solo tiene cota superior (≤74 %). El «53-74 %» se retira.
- **B3.** No residentes: «con controles el coeficiente no se distingue de cero; el IC95 es compatible con cero y con hasta un 60 % de la bivariada». Se retiran «desaparece» y «costa e islas confunden».
- **No bloqueantes.**
  - N1: la tenencia en propiedad es C1 con una tolerancia de 5 pp entre fuentes, que pasa a ser regla declarada; fecha del dato «2021-11 / 2022».
  - N2: `holdout.load_full` se usa en R1b para un análisis C4. El acceso queda registrado y no hay hipótesis confirmatorias pendientes sobre esos datos, así que no hay fuga.
  - N3: corregida la errata.
  - N4: GSADF «fechados sin ajuste múltiple».
  - N5: un solo hilo fijado en los scripts.
  - N6: la sección R1A de fuentes fallidas remite a A23.
- Son las correcciones que propuso el propio revisor y no cambian ninguna estimación, así que el módulo R queda APROBADO sin otra iteración.

## Revisión del módulo A: REHACER (B1-B4) → corregido por el orquestador
- **B1.** Pasan a C4 las filas de fuente única de A23:
  - el IPV por sí solo (P1);
  - el €/m² de Registradores y el de Notariado (P6, P7: difieren un 17 %);
  - las reponderaciones (P4, P8, P9);
  - el contrafactual sin tope (A8).
  Se elimina A1 (IPC 2015-2025), que duplicaba el indicador con otro periodo. El núcleo de alquiler de stock se da solo como rango (sin mediana) y con la tolerancia.
- **B2.** Todas las clases territoriales pasan a C4 (regla B5: el déficit provincial 2021-2025 es C4). «Robusta (diagnóstico)» indica que la clase se mantiene en todo el rango 422-1.500 €/m², en todos los márgenes y holguras y con el signo del déficit estable; es un diagnóstico, no una capa. La concentración provincial también es C4.
- **B3.** `src/v5/a5_hechos.py` genera los hechos de A5 a partir del inventario, la conciliación y la validación: 22 documentos oficiales, no 25. La precisión del 50 % y el 78 % va en las notas de resultado.json.
- **B4.**
  - a4_run escribe `control_sumas.json`, que compara la suma provincial con la serie nacional publicada de terminadas y con los hogares.
  - check_v5 falla si falta el control en A4 o B1.
  - check_v5 comprueba también los recuentos «en contra» y los topes con capa C3 en los JSON.
- **No bloqueantes.**
  - Fechas del dato en lugar de la fecha de cálculo.
  - Verbos de atribución sustituidos por «diferencia contable».
  - Ámbito de la ficha A23-V2.
  - Nombres de formaciones fuera de a5_run (se leen del inventario) y de fuentes_fallidas.
  - Latente por convivencia leída del texto de origen.
  - García-López marcado VERIFICADA (DOI en Crossref, JUE Q1).
- Son las correcciones que propuso el revisor y no hay nuevas estimaciones: el módulo A queda APROBADO.

## B1 (subagente)
- **Método stock-flujo por componentes** (output/v5/B1/metodo.md): A + R + V + F − M − K. La demanda desplazada D y la segunda residencia S van aparte.
- **L, vivienda liberada por envejecimiento: NO se resta en la cifra central.** La proyección de hogares del INE (F) ya descuenta las disoluciones, así que restarla las contaría dos veces. La fórmula literal (restando L) se da solo como variante.
- **R, bajas estimadas.** Sale negativa en 38 provincias con los dos métodos y se acota a 0. Es una cota inferior sin información, y queda abierta en el backlog.
- **Sin dato provincial:** hogares compartidos, hacinamiento, habitaciones y traslados a residencias.
- **Capa.** El total es C4; solo F (INE) es C2.

## B3 (subagente; pre-registro prereg-v5)
- **Potencia.** Con un efecto mínimo detectable de 0,62 DT (más de 0,5), el resultado es DESCRIPTIVO HONESTO, como fija el pre-registro.
- **Hipótesis.**
  - Se rechaza solo H-B3-6 (convergencia, Holm 0,0013). Con el precio inicial de Registradores el coeficiente baja a la mitad, por posible error de medida.
  - H-B3-1 (Bartik) y H-B3-2 (población) no se rechazan.
- **Shapley.** El orden de las familias no coincide entre las fuentes de Y1, así que queda en C4.
- **Desviaciones** (exploratorias; output/v5/B3/desviaciones.md):
  - la renta se mide con el PIB per cápita de la CRE, porque ADRH provincial no está disponible;
  - el alquiler llega a 2024 (N = 46);
  - se excluyen Ceuta y Melilla;
  - en un corte transversal no hay AR(4): se usa LOO-CV frente a un modelo de solo media.
- **Aviso.** F4 (suelo y rigidez, de A4) usa precios de 2021-2025, así que su asociación con Y1 puede ser mecánica.

## C-a (subagente): Europa, crédito a promotores y compras al contado
- **Capa C4 en los tres ángulos.**
  - Eurostat toma los datos de España del INE, así que coinciden por construcción, no por independencia.
  - INE (ETDP e hipotecas) y Registradores comparten origen registral.
  - Se mantiene el criterio estricto. La columna `candidata_C1_si_se_acepta_coherencia` queda solo como información.
- **Crédito a promotores.** Una sola asociación sobrevive a Holm, de 36 pruebas. Fuera de muestra no mejora a AR(4). La comparación con el ECM v1 no aplica, porque ese modelo es del precio.
- **Contado.** Entre el 30 % y el 58 % de las compraventas, según qué parte de las hipotecas sea de compra. La demanda inversora no equivale al contado.

## B2 y B4 (subagentes)
- **B2.**
  - D2030 = D2025 (A4, bajas 0) + F (INE) − terminadas + bajas, en tres escenarios: (a) ritmo 2023-2025, (b) cartera, (c) tendencia, este último solo como sensibilidad.
  - El retardo entre iniciadas y terminadas es de 3,2 años.
  - **Limitación:** el retardo se calcula con acumulados desde 1991 e incluye obras iniciadas y nunca terminadas (2008-2012), así que está sesgado al alza.
  - **Diferencia de partida frente a B1:** B1 parte de la mediana de combinaciones de A4 (788.153); B2 parte del déficit con bajas 0 (700.934), porque proyecta las bajas aparte.
- **B4.**
  - Triangulación sin reestimar.
  - «Estable» exige un τ de Kendall ≥ 0,67 en el orden de las 4 familias comunes.
  - **Limitación:** la τ compara estimandos distintos (cuota de R² transversal frente a contribución temporal), así que es esperable que no coincidan. La conclusión «no estables» se lee como «los métodos no permiten ordenar las familias».

## Revisión del módulo B: REHACER (bloqueantes 1-3) → corregido por el orquestador
1. **Fichas de B4.** Se quitan los verbos de atribución («puede explicar», «contribuye», «permite», «el efecto»). check_texto rechaza ahora esos verbos en las fichas C4 de v5.
2. **B4-V2.** El intervalo de precio pasa a ≤2,7-8,3 %, igual que la magnitud.
3. **H-B3-6 (convergencia).** Los hechos llevan siempre el control con el precio inicial de Registradores (b ≈ −9 pp por DT; p principal 0,058, no significativo; p de permutación 0,016).
- **No bloqueantes.**
  - Gabriel y Nothaft (JUE, Q1) pasa a VERIFICADA.
  - Desviaciones de Oster y K en B3.
  - Las filas sin cifra (NaN) no entran en cifras_clave.
  - Las notas de B3 pasan a ser una lista.
  - Anglicismo corregido.
  - El método de B1 se amplía en el informe técnico (E1).
  - Queda abierto, por impacto bajo, separar B2-H6 en tres hechos.
- Son las correcciones que propuso el revisor y no cambian ninguna estimación: el módulo B queda APROBADO.

## Revisión del módulo C: REHACER (B1-B2) → corregido por el orquestador
- **B1.** CC-V2 (descalificación de protegida) pasa a C4 y ANALIZADA, NO CONCLUYENTE.
  - Los escenarios no recorren el supuesto de 15-30 años y la cota inferior lógica es 0.
  - Las cifras de salidas se rotulan como escenarios ilustrativos y van en C4.
  - La fecha del dato es la última de la serie.
- **B2.** CA ya no dice que el valor de España sea C1: Eurostat toma el dato del INE (coherencia, no independencia).
- **No bloqueantes.**
  - CB-V1: p de Holm con 4 decimales; se citan las especificaciones nulas.
  - CB-V3: se nombran los dos métodos (Censo frente a ECV).
- Tras estas correcciones (las que propuso el revisor), el módulo C queda APROBADO.

## Revisión del módulo D: REHACER (B1-B3) → corregido por un agente de corrección
- **B1 (D2).** Se elimina el lenguaje prescriptivo.
  - La columna pasa a ser «Instrumentos con evidencia en contra o con signo no estable en esta clase (con fuente)» y solo admite literatura VERIFICADA o resultados propios con su capa.
  - «No evaluable» y la evidencia no verificada van en campos aparte.
  - Se añade el signo C2 por grupo de las ayudas.
  - Desaparece «C2 débil».
- **B2 (D3).** Nuevas categorías: «comparable en parte» (6) y «control de la misma fuente» (4).
  - Titular: 2 coincidencias de fuentes distintas y comparables, 1 difiere, 9 no comparables.
  - Se elimina el duplicado R06 = R05.
  - Se anota la tensión entre el déficit C1 2021-2024 y B2-H2.
- **B3 (D1).** Regla común para la clase territorial: «No evaluable (sin signo)» para todo instrumento sin signo, sea de oferta o regulatorio. Se retira la frase sin referencia de I01.
- **No bloqueantes.**
  - Etiquetas de verificación.
  - R04 queda «sin URL localizada» (no se inventa).
  - I16 e I01 con su intervalo.
- Son las correcciones que propuso el revisor: el módulo D queda APROBADO.

## E (redactores y orquestador)
- Todas las cifras de los entregables salen de cifras_clave mediante plantillas. check_v5 rechaza cualquier cifra tecleada en ellas.
- **Extensión del artículo del Colegio (E4).** E-2 lo entregó con 1.463 palabras. El orquestador lo amplía a unas 2.040 (mínimo pedido: 2.000), con:
  - emancipación como cota C2;
  - Cataluña en contratos nuevos (C1);
  - una sección de convergencia con otros organismos;
  - viñetas C4 sobre Europa, crédito, contado y no residentes.
- **Artículos (E3).** Son borradores de entre 1.500 y 3.200 palabras, más cortos de lo previsto, porque el redactor llegó al 80 % del presupuesto. La ampliación pasa al backlog (BK-E3, coste M) y a las tareas del autor antes del envío a revistas. Los cuartiles de Housing Studies, Investigaciones Regionales, SERIEs, Papers in Regional Science y JCRE quedan «no verificados».
- **Cifra tecleada en B4.** B4-v3-vut-cantidad estaba tecleada en b4_run.py. Ahora se lee de output/v3/PB/cotas.json, con el mismo valor.

## Revisión del módulo E: REHACER (B1-B3) → corregido por el orquestador (con cargo a la reserva)
- **B1.** E-B1-F (componente F) pasa a «hogares», con su fuente propia (proyección del INE).
- **B2.**
  - render.py da el rango cuando no hay valor central, en lugar de «— unidad».
  - cifras_clave convierte en texto las listas de fuentes.
  - Se eliminan las unidades duplicadas en las plantillas. Un barrido automático de repeticiones, NaN y listas da 0 casos.
- **B3.** La concentración provincial (C4) se rotula [C4] en el artículo del Colegio.
- **No bloqueantes.**
  - Concordancias de D3 (`:num`).
  - Sobrecarga en puntos.
  - Nota de B4 en la revisión humana.
  - Títulos de las diapositivas 13-14 sin valoración.
  - [C4] en la frase sobre València.
  - Periodos del artículo del Colegio.
  - Titular de LinkedIn 06.
  - Declaración de independencia e IA en el informe técnico y en el artículo del Colegio.
  - LICENSE doble (MIT para el código, CC BY 4.0 para los textos).
  - Tildes en las fichas CB.
  - Saludo del correo.
- Queda anotado, sin corregir, que el artículo del Colegio tiene unas 1.740 palabras de prosa sin las citas entre paréntesis (2.040 con ellas). Ampliarlo es tarea del autor antes del envío.
- **El módulo E queda APROBADO.** E llegó al 85 % de su límite; la revisión y estas correcciones se cargan a la reserva de cierre.

## Cierre v5
- Doble ejecución de `make all` sin red (HTTPS_PROXY a 127.0.0.1:9, un hilo) en un clon limpio de 9ab13fd:
  - rc=0 las dos veces (1.852 s y 1.799 s);
  - md5 idénticos en output/ y data/processed, salvo `output/v2/BM/tiempos.json`;
  - todas las salidas v1-v5 coinciden con lo versionado.
- Módulos R, A, B, C, D y E APROBADOS por el revisor, cada uno tras una ronda de correcciones. Todo lo aprobado está en r5/main y en la rama remota designada.
- La etiqueta `v5.0` se crea en local. El remoto rechaza las etiquetas (docs/v5/bloqueos.md); publicarla es tarea del autor.
- Tokens de subagentes: 3.093.637 de 4.200.000 (74 %), por debajo del corte global (3.360.000). Por módulo:
  - R 601.209
  - A 471.653
  - B 523.477
  - C 416.137
  - D 499.772
  - E 511.524
  - Revisión E (reserva): 69.865
