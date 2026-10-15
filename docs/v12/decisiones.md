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

## B3 · Hogares y presión (src/v12/b3_hogares.py → output/v12/b3)
1. **Fuente nueva:** microdatos de personas del Censo 2011 (INE, con factor de elevación) y del Censo 2021 (muestra
   del 10 % de los hogares, sin factor). Fetcher src/v11/fetch_ine_censos_microdatos.py (en src/v11 para que lo ejecute
   `make datos_v11`); los zips no se versionan (tamaño) y los agregados sí (jefatura_{2011,2021}.csv.gz).
2. **Persona de referencia común:** la de MAYOR edad del hogar. En 2021 la primera persona (NORDEN = 01) es siempre la
   de más edad; en 2011 el orden es otro, y con «primera persona» las tasas por edad salían en dientes de sierra y no
   comparables. Con la regla común, 2011 reproduce los 18.083.692 hogares publicados por el INE.
3. **Calibración 2021:** factor uniforme por provincia = hogares de la ECP a 1-1-2021 ÷ hogares de la muestra.
4. **Descomposición 2011-2021:** H = P · Σ s_a · h_a; se publican los dos órdenes (A: población → estructura →
   jefatura; B: el inverso) porque el reparto cambia con el orden. España: +455.531 hogares; población +195.104
   (A) / +197.884 (B); estructura por edad +966.831 / +1.176.650; jefatura −706.404 / −919.003. La jefatura baja sobre
   todo entre los 25 y los 39 años (30-34: 0,365 → 0,275). Es contabilidad: no dice por qué cambia la jefatura.
5. **2021-2026 (provincia):** hogares esperados con la jefatura por edad de 2021 y la población por edad de la ECP;
   la diferencia con los hogares ECP observados es el cambio implícito de jefatura (+12.553 en la suma de provincias,
   frente a +1.222.836 hogares observados): en este periodo casi todo el aumento de hogares es población y edad.
6. **Hogares por nacionalidad (Censo 2021, muestra):** cuota de hogares cuya persona de referencia tiene nacionalidad
   extranjera, con IC95 (muestreo aleatorio de hogares, f = 0,1). Se suprimen celdas con < 10 hogares en la muestra
   o error relativo > 30 % (26 municipios). España: 9,73 % (IC95 9,69-9,77).
7. **Corrección del extracto V11 del Censo 2021:** VARANOE (año de llegada a España) viene codificado por tramos
   (0001 < 1981 … 0005 2011-2015) y años sueltos 2016-2021; el fetcher lo leía como año y casi todo caía en «<2000».
   Corregido en src/v11/fetch_ine_censo2021.py y regenerado el extracto (con la edad de la persona de referencia).
   Ninguna cifra publicada usaba esa variable (la base solo usa nacionalidad × tenencia): no procede ERRATA.
8. **Formato:** las salidas de V12 se escriben con `%.10g` (con `%.6g` las cifras de millones perdían dígitos).

## B4 · Respuesta de la oferta (src/v12/b4_oferta.py → output/v12/b4)
1. **Obra nueva neta del Catastro:** variación anual de unidades urbanas residenciales; el fichero «t» es el stock a
   31-12-(t−1), así que la variación entre los ficheros t+1 y t es la del año t. Incluye altas administrativas: en
   2013-2017 la regularización catastral añade unidades no declaradas (el Catastro supera al MIVAU en 397.570
   unidades en esos cinco años); esos años no se leen como construcción.
2. **MIVAU:** viviendas LIBRES terminadas (certificados de fin de obra) + calificaciones definitivas de vivienda
   PROTEGIDA. La protegida solo trae nombre de provincia: concordancia nombre → código INE versionada
   (concordancia_mivau_protegida_provincias.csv); en las CCAA uniprovinciales (Madrid, Asturias, Murcia, etc.) las
   terminadas solo se publican por CCAA y se asignan a su única provincia por código.
3. **Cobertura:** País Vasco y Navarra no tienen Catastro estatal (catastros forales) y Ceuta y Melilla no tienen la
   serie del MIVAU: quedan sin contraste.
4. **Capa del contraste provincial 2021-2024:** si Catastro y MIVAU difieren < 25 %, la oferta de esa provincia es C1
   (dos fuentes coinciden: 25 provincias); si no, C4 y se reportan ambas. Los hogares nuevos provinciales son de la ECP.
   España: +981.823 hogares; 358.254 viviendas netas (Catastro) y 373.601 terminadas (MIVAU).
5. **Presión municipal:**
   - 2021-2025: hogares nuevos ESTIMADOS = Δ población del censo anual ÷ personas por hogar de 2021 (muestra
     censal); obra nueva = Catastro en el mismo intervalo. Marcado como estimación.
   - 2011-2021: hogares de los censos (municipios > 20.000 hab.) frente a Catastro 2012-2020 (robustez).
   - Ratio obra/hogares y cuatro categorías. Es una relación contable: no mide necesidad ni déficit (para eso, v7.1).
6. **INSPIRE:** viviendas por año de construcción (stock superviviente, cota inferior) frente al Catastro estadístico
   en los 96 municipios cubiertos.

## B5 · Quién es propietario (src/v12/b5_propiedad.py → output/v12/b5)
1. **Medida:** viviendas (inmuebles de uso residencial, ficheros _V del Catastro) cuyo sujeto pasivo del IBI tiene
   más de 5 / más de 10 / más de 100 inmuebles residenciales EN EL ÁMBITO, y viviendas de personas jurídicas privadas
   (PJ), entidades públicas (PE) y personas físicas (PF). «> 5» = tramos 6-10, 11-25, 26-100 y > 100.
2. **Cuatro ámbitos, cuatro lecturas:** el fichero nacional cuenta los inmuebles del titular en toda España (sin País
   Vasco ni Navarra); el municipal, solo en el municipio. La cuota municipal es una COTA INFERIOR. España 2026: 4,2 %
   de las viviendas en manos de titulares con > 10, 2,1 % con > 100, 4,6 % de personas jurídicas privadas, 1,1 % de
   entidades públicas, 93,4 % de personas físicas. Municipios ≥ 10.000 hab. (2026): mediana 2,5 % con > 10.
   El fichero nacional de 2024 no trae uso residencial: la serie nacional empieza en 2025.
3. **Códigos de CCAA y provincia:** sus ficheros solo traen nombres; el código INE se toma del propio fichero municipal
   (cada fila trae CODINE y el nombre de su provincia y CCAA). Sin nombres tecleados a mano.
4. **Tipo fino (_TPF, España y provincia):** personas físicas de nacionalidad española 87,6 %, de nacionalidad
   extranjera 5,8 % (residan o no en España), sociedades 4,3 %, administraciones públicas 1,1 %, entidades extranjeras
   0,1 % (2026). Descriptivo: se informa del titular, no se valora.
5. **Asociación (C4):** Spearman entre las cuotas municipales de 2025 (> 10 y PJ) y nueve variables; IC bootstrap
   (1.000 réplicas, SEED) y Holm; 18 especificaciones al Registry. La cuota de personas jurídicas es mayor donde el
   alquiler y el precio son más altos (ρ ≈ 0,49 y 0,46), donde hay más viviendas turísticas (0,30) y donde el saldo
   exterior es mayor (0,42). Son asociaciones entre municipios: no dicen si la propiedad de sociedades sigue a los
   precios, los precios a la propiedad o ambos a un tercer factor (turismo, tamaño urbano).
6. **2012-2023:** titulares catastrales urbanos por unidad urbana: 0,823 (2012) → 0,849 (2023). Otra definición: no
   se encadena con 2024-2026 (F0).
7. **AEAT (Comunitat Valenciana):** declaraciones con rentas de bienes inmuebles (aprox., F0) / declaraciones: 53,3 %
   (2016) → 63,7 % (2024). Incluye la imputación de inmuebles no alquilados: no mide caseros. 2013-2015 se guarda
   (rendimientos del capital inmobiliario) con unidades por verificar; no se publica como cifra.
8. **Verificador:** ficha V12-V02 sustituye a V02 («fondos y grandes tenedores … responsables de la subida»): pasa de
   «NO ANALIZADA: FALTAN DATOS» a «ANALIZADA, NO CONCLUYENTE». Hay magnitud (C4, fuente única); la parte causal no
   tiene diseño que la contraste. Se conecta a publicación y web en B8.
