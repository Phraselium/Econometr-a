# V18 · Desviaciones y decisiones del modelizador de E3, E5 y E9 (fase 4)

*Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.* Redactado el 2026-10-20 por el modelizador de E3, E5 y E9, **antes de estimar ninguna especificación** de esos tres
estudios (las entradas se escriben después de mirar datos de insumo, nunca resultados: orden del código = comprobación previa de variación y de MDE → registro en el Registry →
estimación). Este fichero es propio de este módulo, para no chocar con los otros modelizadores que escriben a la vez; el orquestador puede fusionarlo en `desviaciones.md`.
Código: `src/v18/estimacion/{_e359_comun,_e359_datos,e359_adquisicion,e3_inmigracion,e5_oferta,e9_no_residentes}.py`. Fuentes nuevas (`posterior_prereg`): `data/raw/v18/`.

## A. Datos nuevos y sustituciones (afectan a E3, E5)

- **D-E359-1 · Censo de 2001 por nacionalidad y provincia (E3).** El INE no deja consultarlo (aplicación de tablas «saturada» en cinco intentos; docs/v6/fuentes_fallidas.md). Se usa
  Eurostat `cens_01rsctz` (el mismo Censo, por nacionalidad y NUTS 3), bajado el 2026-10-20 con `src/v18/estimacion/e359_adquisicion.py` (sha256 en `data/raw/v18/_manifest_e359.csv`).
  El plan (1.3 g) solo preveía NO ESTIMABLE si el Censo no se podía descargar; se descargó por otra vía, con los mismos datos del INE. Las 52 provincias entran **solo** en el
  denominador nacional de cada grupo (la nación no está sellada); el filtro de sellado se aplica a las provincias del panel.
- **D-E359-2 · Cuotas sectoriales de 2001 de E5 (y control de construcción de E3).** La afiliación provincial por CNAE de 2001 no está publicada. Se usa Eurostat
  `nama_10r_3empers` (empleo por NUTS 3 y rama; datos del INE, 2000-2023). A escala NUTS 3 solo hay seis ramas (A, B-E, F, G-J, K-N, O-U), no las diez de la A*10: el Bartik de E5-R1
  **quita F y K-N** (construcción, finanzas, inmobiliarias, y también servicios profesionales, que no se pueden separar) y queda con **4 sectores** (A, B-E, G-J, O-U). La
  variante de diez sectores (E5-R1-v4) y la de secciones CNAE-2009 con afiliación (v11) quedan NO ESTIMABLES o se reducen a una ventana (se dice en la tabla). La correspondencia
  CNAE-93 a CNAE-2009 fijada en la adenda (R-17) no hace falta: el empleo ya viene en NACE Rev. 2.
- **D-E359-3 · Grupos de origen (E3, AD-E3).** La lista fija de 16 grupos del Censo de 1991 no se puede construir con el Censo de 2001 de Eurostat, que distingue 14 países de la UE-15,
  la AELC, Europa Central y del Este, la ex-URSS europea, el resto de Europa, el norte de África, el resto de África, Norteamérica, el resto de América, Asia, Oceanía y otros. Se
  fijan **8 grupos** antes de estimar: G1 UE-15 sin España; G2 AELC (Noruega, Suiza, Islandia, Liechtenstein); G3 resto de Europa; G4 norte de África; G5 resto de África; G6 América
  Latina y Caribe (América menos Estados Unidos y Canadá); G7 Asia; G8 resto (Norteamérica, Oceanía, apátridas y no asignados). Los grupos 1 y 2 son exactamente los de la variante
  «sin UE-15, Noruega, Suiza e Islandia» del plan. Los flujos (Eurostat `migr_imm1ctz`, datos del INE) se reparten por país en los mismos 8 grupos; el grupo 8 de los flujos es el
  resto hasta el total de extranjeros y apátridas. Con 8 grupos el número efectivo de choques es menor que con 16 (se publica 1/HHI).
- **D-E359-4 · Ventanas y año 2003 (E3).** La endógena es la variación del stock de extranjeros del padrón (a 1 de enero) entre t y t+1 sobre la población a 1 de enero de t, y el choque
  son las entradas del año t: con esa definición el flujo del año 2002 usa el stock de 2002 y 2003, y la ventana principal 2002-2008 se puede construir sin el stock de 2001
  (que el padrón por provincia no publica antes de 2002). **Eurostat no publica la nacionalidad de las entradas de 2003** (el total sí): ese año queda fuera de la principal
  (2002, 2004-2008) y entra en una variante con la composición interpolada y marcada (R1-v11, holgura nº 1; CLAUDE.md limita lo interpolado a robustez). R1-v1 (1998-2008) es NO
  ESTIMABLE: antes de 2002 no hay stock provincial de extranjeros en el repositorio. R1-v3 y R2-v7 (Censo de 1991) y R1-v10 y A5-v1 (choque sin la propia provincia con el padrón por
  nacionalidad) son NO ESTIMABLES: el Censo de 1991 no está y el padrón provincial por nacionalidad solo da 33 países y 5 continentes, que no reconstruyen los 8 grupos.
- **D-E359-5 · Pesos y población (E3).** Población a 1 de enero de 1998 (R1) y de 2000 (R2, R2b) de Eurostat `demo_r_pjanaggr3` (mismos datos del INE; la «población del padrón por edad
  provincial» del plan). En A1, A2 y A5 la de 1 de enero del primer año de la ventana. La población en edad de trabajar es la de 15 a 64 años (el plan decía 16 a 64: Eurostat solo da
  15-64). El placebo de resultado es el crecimiento de la población de 65 años o más **total** (no la nacida en España: el dato por lugar de nacimiento y provincia no está).
- **D-E359-6 · Macrorregiones.** Las 9 macrorregiones del original no se enumeran en la ficha. Se usan las NUTS 1 de España sin las provincias selladas: Noroeste, Noreste, Centro,
  Este, Sur (5 regiones; Madrid y Canarias quedan vacías). Los efectos región-año absorben así las 5 regiones × los años de la ventana.

## B. Especificación (completa lo que el plan no fija, antes de estimar)

- **D-E359-7 · Inferencia principal (adenda 1.13; Monte Carlo de V18).** 1/HHI < 20 en E3, E5 y E9: la principal es **cluster por provincia con bootstrap de Webb (9.999 réplicas) más el
  intervalo de Anderson-Rubin**. Implementación: contraste de Anderson-Rubin con varianza agrupada por provincia (factor G/(G-1)·(n-1)/(n-k)), con p y su inversión por bootstrap de Webb con el
  nulo impuesto sobre la forma reducida (Webb-AR), y el AR exacto agrupado (`herramientas/iv_debil`, APTO en el Monte Carlo: p = 1, 39 clusters, tamaño 0,038-0,0485). El bootstrap de Webb
  de V18 está validado para TWFE con MCO (APTO con G = 8, 30 y 39); su combinación con la forma reducida del IV no tiene Monte Carlo propio (se dice). Para I7 se exigen los dos p
  (Webb-AR y AR exacto) por debajo del umbral. BHJ (K = 8 grupos, 4 sectores) y Driscoll-Kraay (T ≤ 30) son NO APTOS en el Monte Carlo: BHJ se publica solo como alternativa
  etiquetada «no fiable»; Driscoll-Kraay no se publica. El F efectivo se publica siempre, pero no basta (el Monte Carlo deja NO APTA la regla «F ≥ 10»).
- **D-E359-8 · MDE (adenda 1.3).** Contraste de AR agrupado (mismo estadístico y varianza que el Webb-AR; el Webb-AR de 9.999 réplicas no cabe dentro de 2.000 réplicas de potencia), R = 2.000,
  SEED = 20261010, con la variación real del regresor y del instrumento y ruido AR(1) con σ y ρ del residuo del preperiodo tras los efectos región-año y los controles (σ «no vista» en V15/V16 para estas
  unidades; se declara). Preperiodo: 1996-2001 (E3-R, E5), 2009-2013 (E3-A1, A5, valor tasado) y 2012-2013 (E3-A2, SERPAVI: solo dos diferencias). Umbral: MDE ≤ |referencia única| del Anexo B en la
  unidad de la especificación; si no, NO ESTIMABLE por variación (sin mirar el coeficiente: el orden del código lo garantiza).
- **D-E359-9 · Unidades de las variables (E3).** R1: y = diferencia anual del valor tasado en €/m² (nominal, como el original), x = 100·ΔF/P(t) en puntos de población. R2, R2b:
  y = Δ ln valor tasado, x = Δ ln población de 15 a 64 años (elasticidad). A1, A2, A5: y = 100·Δ ln precio o alquiler, x en puntos (unidad de la referencia, % por punto). R1q: y = viviendas
  libres iniciadas por 100 habitantes, x en puntos, con efectos de provincia (la cantidad es un flujo; la referencia es viviendas por inmigrante). R2q: y = Δ ln(iniciadas), x como R2.
  La población del denominador y del instrumento es la de 1 de enero del año t.
- **D-E359-10 · Pruebas B4 adaptadas a la ventana 2002-2008 (E3).**
  - Pretendencia del instrumento: media de Δ valor tasado 1996-2001 (6 diferencias, en lugar del 1995-1998 del plan, que acompañaba a una ventana que empezaba en 1998) sobre la media anual del
    instrumento de la ventana, con efectos de macrorregión; p por Webb. En A: Δ 2009-2013 (valor tasado) y Δ 2012-2013 (alquiler).
  - Placebo de fecha: el instrumento de t + 6 asignado al año t del preperiodo (1996-2001; para R-windows), con efectos región-año; p por Webb.
  - Placebo de resultado: Δ ln población de 65 años o más (total) con la misma x y z.
  - Jaeger-Ruist-Stuhler: el instrumento con las entradas de t-4 como control (t-5 exigiría flujos de 1997, que no existen); se pierden los años cuyo retardo cae en 2003.
  - Rotemberg: pesos por origen; se excluyen los **2** orígenes de más peso (no los 5 del plan: con 8 grupos en lugar de 16, un tercio de los grupos); criterio: mismo signo y estimación dentro del IC95 principal.
  - Balance: a nivel de provincia (el instrumento medio frente al empleo en construcción e industria de 2001, el logaritmo de la población de 2001, la cuota de extranjeros del Censo
    de 2001 y el PIB por habitante de 2002; contraste conjunto), no a nivel de choque (8 choques no dan potencia).
  - Potencia de las pretendencias (I3, Roth): pendiente detectable al 80 % = (1,96 + 0,84)·EE de la pendiente previa; sesgo implicado en β = pendiente/primera etapa; debe ser < ½|referencia|.
- **D-E359-11 · Variantes con datos ausentes (E3).** R1-v1, R1q-v2 (1998-2008), R1-v3, R2-v7, R1-v10, A5-v1, A1-v4 (IPV por CCAA: nueve clusters, inferencia no validada), A4 completa (tenencia por
  nacionalidad del Censo de 2011 por provincia no está en el repositorio ni en Eurostat) y A3-v1 si no hay valor tasado municipal suficiente: «no estimable», sin sustituir por otra.
- **D-E359-12 · E3-A3 y E3-P-H4 (municipal).** Cuotas = población de cada nacionalidad / población total de 2003 (padrón municipal), crecimiento nacional por origen sin el propio
  municipio (como en H4 de V15/V16), efectos provincia-año, cluster por provincia. A3 usa los 28 países individuales del padrón; P-H4 reproduce la especificación de V16 (23 orígenes sin los cinco de la UE-15
  citados, sin Barcelona ni València, municipios con al menos seis años) en la muestra V18 (exclusiones de v6, V15 y V16).

## C. E5

- **D-E5-1 · Bartik.** 4 sectores (D-E359-2); cuotas = empleo de la rama / empleo total de la provincia en 2001; crecimiento nacional del empleo de la rama sin la propia provincia
  (Δ ln del empleo de las 52 provincias de Eurostat menos el de la provincia). Ventana 2002-2023 (el empleo llega a 2023). Efectos de provincia y de año; sin pesos. R1: y = Δ ln iniciadas libres
  (solo años con iniciadas > 0 en t y t-1), x = Δ ln valor tasado real (deflactor nacional anual).
- **D-E5-2 · Rotemberg y exclusión.** Con 4 sectores se excluye el **1** sector de más peso (en lugar de los 3 del plan). La exclusión de la construcción ya está hecha en la principal.
- **D-E5-3 · Pretendencia.** Media de Δ ln iniciadas 1996-2001 sobre la media del Bartik 2002-2007.
- **D-E5-4 · NO ESTIMABLES.** E5-R2 (restricciones físicas), E5-A2 (Atlas de áreas urbanas) y E5-A3 (afiliación municipal por sección de CNAE anterior a 2011-12, que no está agregada en el
  repositorio: solo hay tres ramas), con los datos que las harían estimables.

## D. E9

- **D-E9-1 · Orden.** Antes de cualquier estimación se cuentan los choques efectivos (1/HHI de los pesos de exposición, por origen y por origen × año) con la exposición del padrón de 2003 y
  solo los orígenes con serie de riesgo; la regla de la adenda (1.13) hace NO ESTIMABLES E9-R1, R2, A1 y A2 si 1/HHI < 10. Se cuenta con los pesos de población y no se toca ningún resultado.
- **D-E9-2 · Doble cómputo E3/E9 (adenda 1.10).** Si E9 es NO ESTIMABLE no hay instrumento de E9 que correlacionar con el de E3: la fila alternativa de E9 en la contabilidad queda vacía y se dice.

## E. Registro y sellado

- **D-E359-13 · Sellado ampliado en memoria.** Tres series bajadas después de la etiqueta (Censo 2001, empleo NUTS 3, población NUTS 3) no figuran en `docs/v18/sellado_v18.json`; entran con la
  regla 1.4 (e) (no figuran en V15 ni V16; tope = último periodo descargado, recortado a 2024) mediante un manifiesto ampliado en memoria que se pasa a `sellado.filtrar`. Propuesta: añadirlas a
  `src/v18/f3_sellado.py`. Las lecturas de MIVAU (valor tasado, iniciadas, terminadas) se hacen del fichero original (desde 1995/1991, la base solo trae 2002+) con las claves de sellado de la base.
- **D-E359-14 · Holgura.** Las variantes que no estaban en el Anexo A: R1-v11 (2003 interpolado), y las estimaciones con grupos agregados por continentes para las cuotas del padrón de 2003 (v2), que el
  plan enumera pero cuya correspondencia (UE-15 aproximada por «UE-28 sin España» menos Rumanía, Bulgaria y Polonia) es aproximada. Cada una se rotula; no cuentan en I5 ni en B5.

## F. Incidencias del desarrollo (declaradas)

- **D-E359-15 · Una lectura de coeficiente antes del MDE.** Al probar la construcción del panel de E3-R1 (2026-10-20), un script de desarrollo imprimió el 2SLS de esa especificación
  (β ≈ 3,6 €/m² por punto, EE ≈ 18,8, con 2.999 réplicas) antes de que se hubiera calculado su MDE. No cambia ninguna decisión: la regla de estimabilidad es mecánica (MDE ≤ |referencia|,
  adenda 1.3) y el código definitivo calcula y registra el MDE de cada especificación **antes** de construir su estimación; a partir de ese momento los scripts de desarrollo solo imprimen
  tamaños de muestra, F efectivo y diagnósticos que no usan el resultado. Se dice también en el informe de E3.
- **D-E359-16 · Balance del instrumento a nivel de choque.** D-E359-10 anunciaba un balance a nivel de provincia (instrumento medio frente a características de 2001). La primera ejecución de desarrollo
  mostró que ese contraste falla de forma mecánica en cualquier shift-share construido con cuotas históricas (el instrumento es proporcional a la exposición de 2001, que BHJ no exige que sea
  ortogonal a nada), de modo que no discrimina. Se vuelve al balance **del plan** (1.3 d): a nivel de choque (el choque medio por origen frente a la media, ponderada por exposición, de las
  características de 2001), con Holm entre características y p > 0,10 como criterio; con 8 choques la potencia es mínima y se dice. Renta, paro y cuota urbana de 2001 no están a escala provincial:
  se usan el empleo en construcción e industria, el logaritmo de la población y la cuota de extranjeros de 2001. El contraste provincial se publica solo como información. Se decidió después de
  ver ese resultado de diagnóstico (no el del coeficiente) y vuelve al texto del plan, no se aparta de él.
- **D-E359-17 · Rótulo de las estimaciones no significativas con pruebas débiles.** La adenda define NO CONCLUYENTE (sin potencia) para diseños válidos sin significación ni equivalencia y reserva
  SUGESTIVO a diseños creíbles con alguna prueba débil; no dice qué hacer con una estimación sin significación (p de Holm ≥ 0,10), sin equivalencia y con pruebas débiles. Se rotula
  NO CONCLUYENTE (sin potencia) y se listan las pruebas débiles, porque no hay efecto que sugerir. El otro modelizador de la fase 4 (E2, E8) puede haber usado SUGESTIVO en el mismo caso: lo ve el orquestador.
- **D-E359-18 · Información no preinscrita.** Se publica además, sin que entre en la clasificación, el control de la suma de cuotas × año (BHJ con cuotas incompletas; V9-D4 y H4 lo incluían) y el
  BHJ a nivel de choque con ese control (es la condición de equivalencia con el IV de localización, comprobada numéricamente: ambos dan el mismo β). El BHJ se etiqueta «no fiable» (Monte Carlo de V18).
