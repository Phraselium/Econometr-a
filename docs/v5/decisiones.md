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
