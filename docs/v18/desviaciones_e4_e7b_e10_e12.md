# V18 · Desviaciones y decisiones del modelizador de E7-R3/A1 (BVAR), E4, E10, E11 y E12 (fase 4)

*Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.* Redactado el 2026-10-20 por el modelizador de E7-BVAR, E4, E10, E11 y E12. Cada entrada tiene su motivo; ninguna se
eligió por un resultado (el orden del código es comprobación de datos y MDE → registro previo en el Registry → estimación). Fichero propio de este módulo, para no chocar con los demás
modelizadores; el orquestador puede fusionarlo en `desviaciones.md`. Código: `src/v18/estimacion/{e7_bvar_lib,e7_bvar,e4_e10_e12}.py` y `src/v18/montecarlo/bvar.py`.

## A. E7-R3 y E7-A1 (BVAR de San Juan, 2023) y su Monte Carlo

1. **Monte Carlo primero, y su veredicto.** La cobertura de las bandas del BVAR no estaba validada (plan 1.13). Se hizo antes de estimar (`src/v18/montecarlo/bvar.py`,
   `output/v18/montecarlo/bvar/`; R = 2.000, 500 extracciones del posterior por réplica, SEED 20261010, 500 s). **Veredicto: NO APTO.** El criterio se fijó antes de simular: las bandas son
   de credibilidad al 68 % y al 90 %, así que los márgenes del criterio del encargo (±2,5 pp al 95 %) se trasladaron a la misma distancia en errores típicos binomiales: cobertura del 68 % en
   [0,63; 0,73] y del 90 % en [0,87; 0,93]; filas decisivas: prior principal, persistencia 0,97, T = 60 (E7-R3) y T = 74 (E7-A1), con y sin efecto verdadero, h = 8, precio, compraventas
   y visados. Las 12 filas fallan: sin efecto verdadero la banda es conservadora (cobertura del 68 % entre 0,94 y 0,99); con efecto verdadero el prior de Minnesota encoge hacia el paseo aleatorio
   y el precio queda cubierto solo entre el 0,5 % y el 1,6 % (68 %) y el 12 % y el 18 % (90 %). El código no es la causa: con un prior difuso (solo información) la cobertura bajo el nulo es 0,86-0,89 y bajo la
   alternativa 0,55 con T = 60-74 (sesgo de muestra pequeña de un VAR de 7 variables y unas 52 filas), y con T = 600 y prior difuso una comprobación interna del código (R = 150, no versionada) dio 0,64 y 0,85 para el precio bajo la alternativa, cercanas a las nominales 0,68 y 0,90 dentro del error de Monte Carlo. **Consecuencia (encargo y plan 1.13):
   E7-R3 y E7-A1 se publican solo como informativas**; su tope ya era ASOCIACIÓN y quedan fuera de la familia de Holm y de B5.
2. **Muestra.** El plan fija 2004-2022 («sus siete variables»). Las compraventas nacionales empiezan en 2007T1 y los visados observados en 2008T1 (hasta 2007T4 están interpolados; CLAUDE.md limita lo
   interpolado a robustez). **E7-R3 usa 2008T1-2022T4** (52 filas de regresión) y **E7-R3-v2 2008T1-2019T4** (el plan decía 2004-2019; mismo motivo). E7-A1 usa 2008T1-2026T2 (66 filas).
3. **Crédito.** El saldo de préstamos de vivienda del Banco de España (`posterior_prereg`) no está descargado y `credito_stock_bde` no tiene clave en sellado_v18.json: se usa `base:credito_nuevo` y se rotula
   «flujo, no saldo» (regla de fallback de la adenda R-27). El flujo tiene estacionalidad fuerte: se añaden tres ficticias estacionales a todas las ecuaciones (prior plano).
4. **IPC, no IPCA.** La base solo trae `inflacion_ipc_yoy`. Se declara en cada cifra.
5. **Visados con huecos.** Faltan 2016T2 y 2017T2 en la base. Se omiten las filas de regresión afectadas (la propia, y las dos siguientes por los rezagos); no se interpolan. El Monte Carlo reproduce el patrón.
6. **Prior y rezagos.** San Juan no declara el prior ni el orden de rezagos. BVAR(2), prior de Minnesota en observaciones ficticias (Bańbura, Giannone y Reichlin, 2010): λ = 0,2, γ = 1 en niveles y 0,8 en IPC y euríbor,
   decaimiento por rezago, suma de coeficientes con peso 1/(10 λ) sobre la media inicial en logaritmos, escalas del AR(1). Variante v1 de E7-R3 («prior más laxa»): λ = 0,5 sin suma de coeficientes. Fijado antes de ver ningún resultado de datos.
7. **Choque y unidad.** El choque es la innovación recursiva del euríbor a 1 año (sexta en el orden de San Juan), normalizada a +100 pb en su impacto. San Juan escala un choque «equivalente a su desviación típica» del
   **tipo hipotecario** hasta +100 pb; el tipo hipotecario no está entre sus siete variables, así que la unidad no es idéntica y I6 es solo una etiqueta (no decide nada, adenda 1.2). La referencia (−2 %, −3 %, −11 %; intervalos al 68 %) va al lado.
8. **Comprobación de MDE (adenda 1.3).** No hay un MDE frecuentista de un BVAR con prior informativa. Se publican las bandas al 68 % y al 90 % y su anchura; la especificación no entra en la familia de Holm (tope ASOCIACIÓN, adenda 1.7) ni en B5.
9. **E7-A1-v1 («sin 2010-2013»).** Se omiten las filas de regresión de 2010T1-2013T4 (los rezagos usan los valores reales), como en E7-R1-v1.
10. **Diagnósticos B4 (no cuentan en el multiverso).** ADF y KPSS de las series; estabilidad (raíz máxima del VAR en la media posterior y proporción de extracciones explosivas: normal con prior de paseo aleatorio y variables en niveles);
    sensibilidad a la identificación (euríbor primero, sin crédito, precio primero) a h = 8, registrada en el Registry como diagnóstico.
11. **Biblioteca.** `src/v18/estimacion/e7_bvar_lib.py` (no `src/v18/herr18/`) por el encargo (auxiliares con el prefijo e7_bvar). `src/v18/montecarlo/bvar.py` se lanza como script (reimporta su propio módulo para que joblib serialice las funciones por referencia).
12. **min y max en hechos.json** son la banda del 68 % (en E7-R1 son el AR al 95 %); la del 90 % está en la nota. Respuesta en nivel (no acumulada) a 8 trimestres, 10.000 extracciones.

## B. E4 y E11 (NO ESTIMABLES)

13. **E4.** E4-X1 NO ESTIMABLE (no hay microdatos de perceptores ni convocatorias autonómicas con fecha; solo hay las cinco filas estatales del bono). Sin tratamiento medido no hay variación que comprobar por MDE: es una falta de dato, no de potencia.
    E4-X2 no se repite (Q7a, V16). E4-L1: solo literatura; **no lleva cifra propia**: la traslación mediana de los estudios con diseño ya está publicada con su id en V17 (V17-AUD-RA-AYU-TRASLACION-MEDIANA) y no se duplica. Fichas citadas sin combinar (unidades distintas).
14. **E11.** E11-X1 y X2 NO ESTIMABLES: el repositorio solo tiene las tres filas estatales del recargo del IBI (Ley 12/2023; ningún municipio con fecha) y la vacancia solo tiene dos cortes con métodos distintos (2011 y 2021 por consumo eléctrico).

## C. E10-A1 (asociación transversal)

15. **Datos.** SERPAVI municipal de **vivienda colectiva** (VC: el plan no fija tipología; se elige antes de estimar por ser la tipología de los edificios de varios hogares; no se estima la de vivienda unifamiliar). Titularidad: `v12_titularidad_pct_mas10` y `_pj` de **2024**
    (los tres cortes existen, pero el alquiler de 2024 es el último). Renta: ADRH de 2023 por sección promediada por municipio (media simple de las secciones no selladas del municipio: no hay población por sección en la regla). Población: total de `pob_censo_anual` 2024, que
    hereda la clave `pob_total|municipio|A` (regla f de la adenda 1.4: la `pob_total` municipal de la base solo trae una unidad). Coordenadas: centroides de `municipios.parquet` en ETRS89/UTM 30 N.
16. **Dos contrastes principales.** El plan nombra dos resultados (nivel de 2024 y variación 2019-2024): son E10-A1 y E10-A1-d, con las mismas variantes (v1 pct. personas jurídicas, v2 sin Barcelona = municipio 08019, v3 sin controles, v4 municipios de más de 10.000 habitantes). Fuera de Holm (tope ASOCIACIÓN, adenda 1.7); BY al 10 % en las variantes de cada resultado.
17. **Holgura nº 1 y 2** (adenda 1.8): E10-A1-vF y E10-A1-d-vF (sin los municipios con distritos sellados; adenda 1.5 exige añadir esa variante a cada diseño municipal y el Anexo A no la enumera). No apoyan ninguna clasificación.
18. **Inferencia.** Cluster por provincia con wild bootstrap de Webb (WCR, 9.999) con efectos de provincia (no hay Monte Carlo de Webb en sección cruzada con efectos de provincia: se publica con esa etiqueta); Conley a 10 km con núcleo de Bartlett
    (V18 montecarlo/conley: APTO si el alcance de la dependencia no supera el corte); Moran de los residuos con 8 vecinos y 999 permutaciones. **MDE sin umbral:** el Anexo B no da referencia ni δ para E10-A1 («—»), así que el MDE se calcula antes de estimar (R = 2.000; ruido = residuo del resultado tras los efectos con signos de
    Rademacher por provincia, σ declarada «ya vista») y se publica como diagnóstico, sin declarar NO ESTIMABLE por variación.
19. **Dato de titularidad.** El tramo se cuenta dentro del municipio (cota inferior; la mediana municipal es 0): el regresor es una cota inferior del peso de los grandes tenedores. Se dice en cada cifra.

## D. E12-A1 y E12-A2 (protegida frente a libre, estilo Chapelle)

20. **Qué se mide.** Calificaciones **definitivas** anuales de vivienda protegida (MIVAU, tabla 1.6; planes estatales y autonómicos) y viviendas **libres** iniciadas, ambas por 100 viviendas del parque del año anterior (`mivau_parque`, 2001-2025); «ΔLibre» y «ΔProtegida» del plan se leen como los incrementos de parque
    (flujos) del año. Mide la vivienda **protegida**, no la pública (rótulo en cada cifra). Cantabria, uniprovincial, se trata como la provincia 39 (como en F3). Panel balanceado 2002-2024 de 38 provincias no selladas.
21. **Instrumento.** (Calificaciones de las demás provincias no selladas)_t × cuota provincial de 1991-1995 / parque_{t−1}. «Nacional sin la propia provincia» se restringe a las provincias no selladas: nunca se leen las 11 selladas (el total nacional no tiene clave propia de sellado).
22. **Control de persistencia (AD-E12-A1).** Obra libre iniciada media de 1991-1995 por 100 viviendas del parque de 2001, interactuada con ficticias de año (la «obra libre 1991-1995 × año» del plan). La variante v1 lo quita.
23. **E12-A1-v3 NO ESTIMABLE.** La serie de viviendas libres terminadas por provincia no figura en sellado_v18.json (solo la de iniciadas y la de terminadas totales, que incluye la protegida): no se sustituye (adenda 1.8). Tarea para el orquestador: añadir su clave por sustituto (regla f) al manifiesto y regenerarlo con `src/v18/f3_sellado.py`.
24. **«Sin atípicos».** Se ejecuta como diagnóstico registrado (no es variante enumerada del Anexo A): se excluye la provincia de mayor cuota 1991-95 y la de mayor desviación de la media del resultado respecto a la mediana (el 1 % extremo con N ≈ 38 es una unidad).
25. **E12-A2.** Resultado: 100 Δ ln del valor tasado provincial anual real (media de años completos entre el deflactor nacional; el valor tasado provincial empieza en 2002, así que la primera diferencia es 2003): 2003-2024, 33 provincias con serie completa. Variantes: sin Barcelona y 2003-2013 (el plan decía 2002-2013).
26. **Pruebas de E12 (adenda).** Pretendencia: el instrumento medio de 2002-2007 no predice la variación de la obra libre de 1996-2001 frente a 1991-95 (MCO transversal, HC1). **La prueba de exclusión (cuota 1991-95 frente al crecimiento del PIB provincial de 1995-2001) no es verificable**: el PIB provincial
    de `ine_v2_cre.csv` empieza en 2000. El plan no lista un placebo de resultado para E12 en su apartado (d) y el IPC provincial no está en la base: no se hace. Driscoll-Kraay se publica con la etiqueta NO APTO (T = 23 ≤ 30); la inferencia principal es el AR por cluster (APTO, V18 montecarlo/iv_debil) y el WCR de Webb del AR en cero (APTO con 30-39 clusters, V18 montecarlo/webb_twfe).
27. **MDE de E12-A1 y umbral.** MDE de la pendiente de forma reducida por Monte Carlo (R = 2.000; ruido = residuo de y tras efectos con signos de Rademacher por provincia; variación real del instrumento; σ declarada «ya vista»), convertido a β con la primera etapa estimada (π); umbral |Chapelle| = 1,604 (Anexo B, ficha NO VERIFICADA). El plan fija 80 % de potencia, 5 % bilateral y t de Student con G − 1 grados.
    E12-A2 no tiene referencia ni δ en el Anexo B: MDE publicado sin umbral. La familia de Holm de E12 queda en las especificaciones estimables tras la comprobación (la adenda 1.7 dice «tras las comprobaciones de la sección 1.3»).

## E. Holgura usada (adenda 1.8; máximo 200)

E10-A1-vF y E10-A1-d-vF (punto 17). Total: 2. Ninguna apoya clasificaciones ni entra en I5 o B5.

## F. Qué queda para el orquestador y el autor

- Autor: tareas_autor.md, sección «V18 · fase 4» (E4, E10, E11, E12 y el saldo de crédito, los visados de 2016-2017 y las compraventas de 2004-2006 de E7-R3).
- Orquestador: clave de sellado de las viviendas libres terminadas (punto 23); réplica ciega (B6) de lo clasificable; las clases de este módulo son provisionales hasta I8.
