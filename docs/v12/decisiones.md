# V12 · Decisiones (análisis descriptivo: población, propiedad y oferta)

Reglas generales:
- solo análisis descriptivo y contable; ningún modelo causal ni predictivo;
- capas C1 (≥2 fuentes coincidentes en ese nivel), C2 (cotas) y C4 (descriptivo o asociación);
- neutralidad: se describen flujos y condiciones, nunca se atribuyen responsabilidades;
- celdas pequeñas: se respeta «<5» de origen y no se publican cruces con < 10 casos ni con error relativo > 30 %.

## F0
1. **`make check` no escribe ficheros versionados**:
   - `src/v10/web.py` toma la ruta del resumen de `web.RESUMEN`; `tests/v10/test_web.py` construye la web y el resumen
     en un directorio temporal;
   - `src/v12/git_limpio.py` guarda `git status` al empezar `make check` y falla si cambia al terminar;
   - `tests/conftest.py` hace lo mismo para la sesión de pytest; `tests/v12/test_git_limpio.py` prueba el guardia.
2. **Titularidad del Catastro: dos series que NO se encadenan.**
   - **2012-2023 (JAXI):** titulares catastrales; cuenta todos los cotitulares y derechos.
   - **2024-2026 (CSV):** sujetos pasivos del IBI, un contribuyente por inmueble.
   - **Salto nacional 2023 → 2024:** −32,1 % en inmuebles urbanos (33,72 → 22,90 millones). Ratio municipal mediano 0,671 (p10-p90: 0,61-0,74). Es cambio de definición, no variación real. Va marcado en el diccionario de la base.
   - **Ámbito de los tramos:** el nº de inmuebles del titular se cuenta DENTRO de cada ámbito territorial.
     - Comprobación: la suma municipal de viviendas de personas jurídicas con > 100 inmuebles es 139.295 en 2025, frente a 290.427 en el fichero nacional.
     - Consecuencia: la concentración municipal es una cota inferior de la nacional, y los análisis de grandes tenedores usan también los ficheros nacional, autonómico y provincial.
3. **AEAT: declarantes aproximados con rentas de bienes inmuebles = importe ÷ media (2016-2024).**
   - **Error de redondeo:** ≤ 0,5/media (mediana 0,04 %).
   - **Qué incluye el concepto:** alquileres E imputación de rentas de inmuebles no alquilados, así que no mide «caseros». Cuotas > 1 (10 municipio-año) se marcan y no entran en la base.
   - **2013-2015:** otro diseño. Separa alquileres e imputaciones, pero sin media; unidades por verificar; no se usa en cálculos.

## B1 · De dónde viene la población (src/v12/b1_contabilidad.py → output/v12/b1)
1. **Identidad:** ΔP = vegetativo (MNP) + saldo exterior + saldo interior + residuo, con flujos del año natural t y
   población a 1 de enero de t y t+1. Capa C4: cada componente sale de una sola fuente; el residuo se publica siempre.
2. **Población:** padrón continuo para ΔP de 2003-2021 y censo anual para 2022-2024 (cada ΔP con la misma fuente en
   ambos extremos). Padrón y censo anual difieren +0,033 % (2021) y +0,024 % (2022) en el total nacional.
3. **Empalme EVR → EMCR en 2021:** se usa la EMCR desde 2021. En 2021 la EMCR da 887.960 inmigraciones exteriores y
   696.866 emigraciones, frente a 662.173 y 452.511 en la EVR (la EMCR estima omisiones y bajas que la EVR no registra);
   los movimientos interiores casi coinciden (1,671 frente a 1,679 millones). Las dos se guardan en empalme_2021.csv.
4. **Periodo inicial:** 2003-2007 (no 2002-2007): la población municipal por nacionalidad empieza el 1-1-2003.
5. **Residuo:** con la EVR (2003-2021) el residuo nacional es negativo (−0,60 millones en 2008-2013, −0,48 en
   2014-2019): la EVR registra peor las salidas al extranjero y el padrón da de baja por caducidad e inscripción
   indebida sin que conste como flujo. Con la EMCR (2022-2024) el residuo es casi nulo (+8.897). Por eso las
   comparaciones entre periodos usan las tasas de los componentes y se lee el residuo junto a ellas.
6. **Nacionalidad:** el residuo de cada grupo incluye las adquisiciones de nacionalidad española (pasan de EXT a ES
   sin ser flujo): residuo ES positivo y EXT negativo de magnitud parecida. No se interpreta como migración.
7. **Municipios:** solo ≥ 10.000 hab. (los menores llegan agregados como PP999 en los microdatos y solo cuentan en
   provincia, CCAA y España). Ficheros municipales comprimidos (gzip determinista).
8. **València por sección y barrio (2021-2025):**
   - No hay padrón por barrio con nacionalidad en data/raw. Se usa el censo anual por sección (deriva del padrón) y se
     pasa a barrio con la correspondencia sección-barrio: entera si ≥ 95 % del área cae en un barrio, por área si no
     (10,2 % de la población de 2025; supone densidad uniforme).
   - Solo hay cartografía del seccionado vigente y entre 2021 y 2025 se dividen o desaparecen secciones en 11 de 19
     distritos. La variación 2021→2025 es exacta por distrito (las secciones no cambian de distrito); por barrio se
     publica solo si su distrito no cambió de seccionado (37 barrios «comparables»); el resto queda en blanco.
   - Solo stocks por nacionalidad (no hay flujos por sección). Países con < 10 personas en la celda se suprimen.

## B2 · A dónde va y quién se desplaza (src/v12/b2_flujos.py → output/v12/b2)
1. **Áreas:**
   - València: ámbito oficial del PATEVAL (90 municipios, incluida la ciudad).
   - Madrid y Barcelona: municipios con centroide a ≤ 25 km del de la capital (no hay delimitación oficial en
     data/raw; 25 km recoge las coronas continuas sin llegar a las capitales comarcales externas).
   - Alicante/Alacant y Castelló de la Plana: ≤ 20 km (la misma definición operativa de V11).
2. **Corona de composición fija:** los microdatos OD agregan los municipios < 10.000 hab. de cada provincia (PP999).
   La corona es el conjunto de municipios del área identificados en TODOS los años 2002-2024 (València 28, Madrid 23,
   Barcelona 41, Alicante 5, Castellón 6), para que la serie no cambie por municipios que cruzan el umbral. El resto
   del área cuenta como «resto de España»: los saldos capital-corona son una cota inferior del intercambio con el área.
3. **Fuentes y empalme:** EVR 2002-2020 y EMCR 2021-2024 (mismo criterio que B1). Los movimientos dentro de la corona
   (entre dos municipios de la corona) no se cuentan: no cambian el reparto capital/corona.
4. **Edad:** los OD y los saldos interiores municipales traen edad (0-15, 16-34, 35-64, 65+) y nacionalidad (ES/EXT);
   los microdatos exteriores municipales solo traen nacionalidad: el saldo exterior por edad no se publica a escala
   municipal.
5. **Precios y alquileres (asociación, C4):**
   - alquiler: SERPAVI, mediana €/m² de vivienda colectiva (código INE, 2011-2024);
   - compra: valor tasado medio de vivienda libre (MIVAU, municipios > 25.000 hab.). El fichero no trae código INE:
     concordancia nombre → código versionada (concordancia_mivau_municipios.csv): coincidencia normalizada con alguna
     variante del nombre INE (partes separadas por «/», artículo pospuesto), provincia para desambiguar (Torrent,
     Mieres, Cieza) y 7 alias explícitos apuntados al NOMBRE INE (Palma, Vitoria-Gasteiz, San Cristóbal de La Laguna,
     Santa Coloma de Gramenet, El Puerto de Santa María, Santa Eulària des Riu, Maó). 309 de 309 nombres con código
     único; Córdoba, Lucena y Puente Genil aparecen dos veces por una errata en la provincia («Córdaba») y se promedian.
     El cruce posterior es por código INE.
   - Spearman entre la tasa de saldo (interior y exterior, ‰ anual, B1) de un periodo y el nivel inicial y el cambio del
     alquiler o el precio en ese periodo; municipios ≥ 10.000 hab.; España y las cinco áreas; IC95 por bootstrap
     (1.000 réplicas, SEED); 32 especificaciones en el Registry con Holm. Son asociaciones de rangos entre territorios:
     no indican qué mueve a qué.
   - Pares: alquiler medio en destino de quienes salen de cada capital, ponderado por el flujo, frente al alquiler de la
     capital (ratio).
6. **Caché versionada:** los OD completos (data/raw/v11/*/od_municipios_*.parquet) no se versionan por tamaño; el
   script solo los lee si falta output/v12/b2/od_seleccion.csv.gz (flujos con origen o destino en alguna de las áreas).
   Así `make v12` funciona en un clon limpio sin `make datos_v11`.
7. **Neutralidad:** se describen flujos por nacionalidad y edad; las personas que llegan o se desplazan forman parte
   de la demanda y de la oferta de trabajo de los municipios de destino. No se atribuyen responsabilidades.
8. **Cruces por código (V7) también en V12:** src/v12 entra en el control estricto de tests/test_v7_cruces.py; la
   columna de código de B1 pasa a llamarse `cod_territorio`; la concordancia MIVAU se aplica una sola vez como
   diccionario versionado.
9. **`make check` y consulta/:** el test de idempotencia del generador de consulta escribía en consulta/ (y
   version.json cambia con cada commit que toca output/). Ahora genera en un directorio temporal (corrección F0).
