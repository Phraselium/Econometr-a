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
5. **Residuo:** con la EVR (2003-2020) el residuo nacional es negativo (−0,60 millones en 2008-2013, −0,48 en
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
   script solo los lee si falta data/cache/v12/od_seleccion.csv.gz (flujos con origen o destino en alguna de las áreas;
   caché interna NO difundible, fuera de output/ tras la revisión final).
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
   2013-2017 la regularización catastral añade unidades no declaradas (en las provincias con las dos fuentes, el Catastro supera al MIVAU en 348.840
   unidades en esos cinco años); esos años no se leen como construcción.
2. **MIVAU:** viviendas LIBRES terminadas (certificados de fin de obra) + calificaciones definitivas de vivienda
   PROTEGIDA. La protegida solo trae nombre de provincia: concordancia nombre → código INE versionada
   (concordancia_mivau_protegida_provincias.csv); en las CCAA uniprovinciales (Madrid, Asturias, Murcia, etc.) las
   terminadas solo se publican por CCAA y se asignan a su única provincia por código.
3. **Cobertura:** País Vasco y Navarra no tienen Catastro estatal (catastros forales) y Ceuta y Melilla no tienen la
   serie del MIVAU: quedan sin contraste.
4. **Capa del contraste provincial 2021-2024:** si Catastro y MIVAU difieren < 10 %, la oferta de esa provincia es C1
   (dos fuentes coinciden: 10 provincias con el umbral del 10 % fijado en la revisión final); si no, C4 y se reportan ambas. Los hogares nuevos provinciales son de la ECP.
   Mismo conjunto para las tres magnitudes (46 provincias con Catastro y MIVAU; sin País Vasco, Navarra, Ceuta ni
   Melilla): +934.562 hogares; 355.508 viviendas netas (Catastro) y 346.403 terminadas (MIVAU).
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
   exterior es mayor (0,45). Son asociaciones entre municipios: no dicen si la propiedad de sociedades sigue a los
   precios, los precios a la propiedad o ambos a un tercer factor (turismo, tamaño urbano).
6. **2012-2023:** titulares catastrales urbanos por unidad urbana: 0,823 (2012) → 0,849 (2023). Otra definición: no
   se encadena con 2024-2026 (F0).
7. **AEAT (Comunitat Valenciana):** declaraciones con rentas de bienes inmuebles (aprox., F0) / declaraciones: 53,3 %
   (2016) → 63,7 % (2024). Incluye la imputación de inmuebles no alquilados: no mide caseros. 2013-2015 se guarda
   (rendimientos del capital inmobiliario) con unidades por verificar; no se publica como cifra.
8. **Verificador:** ficha V12-V02 sustituye a V02 («fondos y grandes tenedores … responsables de la subida»): pasa de
   «NO ANALIZADA: FALTAN DATOS» a «ANALIZADA, NO CONCLUYENTE». Hay magnitud (C4, fuente única); la parte causal no
   tiene diseño que la contraste. Se conecta a publicación y web en B8.

## B7 · Turismo y presión residencial (src/v12/b7_turismo.py → output/v12/b7)
1. **Dos fuentes de stock que miden cosas distintas:** INE (anuncios en plataformas, experimental, semestral desde
   2021-08) y registro de la GVA (inscripciones; cortes observados 2025-01-26 y 2026-10-14). Comunitat Valenciana:
   51.268 viviendas turísticas según el INE (2026-05; 2,0 % del parque) y 90.124 inscritas en el registro
   (2026-10-14). Coinciden (< 25 % de diferencia; dato descriptivo, sin C1) en 132 de 452 municipios: en el resto se reportan las dos y no se
   elige una. València: 5.393 (INE, 1,4 %) y 5.766 (registro).
2. **Serie reconstruida del registro (2015-2025):** sale de las fechas de alta de las viviendas que siguen inscritas;
   no recoge bajas, es cota inferior del stock pasado y solo entra como robustez.
3. **Agregación:** el porcentaje del INE se agrega con el parque implícito de cada sección (viviendas turísticas ÷
   porcentaje); sección → barrio en València con la misma correspondencia por área que B1.
4. **Asociaciones (C4):** municipios de la Comunitat Valenciana ≥ 10.000 hab.; tres medidas de turismo (INE %,
   registro por 1.000 hab., turistas de teléfonos móviles por habitante en 2024) frente a crecimiento de población
   2021-2025, alquiler 2024 y su variación 2019-2024, cuota de personas jurídicas y de titulares con > 10 viviendas
   (B5). 15 especificaciones al Registry, Holm. La vivienda turística es mayor donde crece más la población, el alquiler
   es más alto y hay más propiedad de sociedades; no se asocia con la cuota de grandes titulares. Descriptivo.
5. **Cataluña y Barcelona:** HUT del Idescat (2025) frente al INE (media de 2025) por municipio (coinciden en 209 de
   898) y HUT de Barcelona por año del expediente (Ajuntament).

## B6 · Condiciones de vivienda por origen (src/v12/b6_condiciones.py → output/v12/b6)
1. **Fuentes:** ECV 2018-2025 (microdatos; definiciones y estimadores de src/v10/atlas_microdatos.py, reutilizados) y
   Censo 2021 (muestra de hogares, extracto corregido en B3). La EPA no recoge tenencia ni gasto en vivienda: no se usa
   aquí (la emancipación por nacionalidad ya está en V10).
2. **Grupos:** nacionalidad (española, resto de la UE, fuera de la UE), país de nacimiento (RB280, desde que la ECV lo
   publica), periodo de llegada a España (Censo), edad, quintil de renta equivalente y tipo de hogar.
3. **Misma edad y renta:** años 2023-2025 agrupados; tasa de los españoles reponderada a la composición por edad
   (18-34, 35-49, 50-64, 65+) × quintil de renta del grupo extranjero (estandarización directa); IC bootstrap por hogar
   (200 réplicas, SEED). Con la misma edad y renta: sobrecarga > 40 % +14,7 puntos (IC 13,3-16,3), hacinamiento +8,2
   (6,4-9,9), alquiler de mercado +41,8; el esfuerzo del alquiler entre quienes alquilan a precio de mercado no difiere
   (> 30 %: −0,9, IC −3,2 a 1,8). Lectura descriptiva: la diferencia en sobrecarga va con la tenencia (mucho más
   alquiler de mercado), no con pagar más por el mismo alquiler a igual renta; no se atribuye a la nacionalidad.
4. **Censo 2021:** hogares con persona de referencia extranjera: 46,7 % en propiedad y 40,5 % en alquiler (españoles
   78,5 % y 13,5 %); < 15 m² por ocupante 18,2 % (5,4 %). La propiedad aumenta con el tiempo desde la llegada (40,8 %
   llegados en 2016-2021; 66,6 % antes de 2001).
5. **Celdas pequeñas:** ECV, < 50 observaciones se suprimen y además se exige ≥ 10 casos con el atributo y error
   relativo ≤ 30 %; Censo, ≥ 10 hogares y error relativo ≤ 30 % (IC binomial con f = 0,1). Suprimidas: 3 (ECV anual),
   5 (cruces), 0 (Censo).
6. **Reproducibilidad:** los microdatos de la ECV no se versionan; sin ellos `make v12` conserva las salidas
   versionadas de la ECV y rehace la parte del Censo.

## B8 · Integración
1. **Corrección de B1 (antes de publicar nada):** a nivel municipal entraban también los municipios < 10.000 hab.,
   que no tienen flujos en los microdatos, con todo su crecimiento en el residuo. El nivel municipal se restringe a los
   municipio-año identificados en los flujos (unos 670-780 por año). Provincia, CCAA y España no cambian. Se
   regeneran B2, B5 y B7 (que leen B1 municipal); cambian ligeramente las asociaciones (p. ej. cuota de personas
   jurídicas frente a saldo exterior: 0,42 → 0,45). No había cifras publicadas: no procede ERRATA.
2. **Comparación hogares/oferta en la misma muestra:** la primera versión sumaba los hogares de todas las provincias y la
   oferta solo de las que tienen Catastro estatal; corregido antes de publicar (46 provincias para las tres magnitudes).
3. **Base:** src/v12/base_v12.py añade a la base variables `v12_*` (C4): contabilidad demográfica anual (B1),
   descomposición de hogares 2011-2021 en los dos órdenes (B3), cuota de hogares con persona de referencia extranjera
   (solo celdas publicables), presión obra/hogares (B4) y cuotas de titularidad (B5).
4. **Cifras difundibles:** src/v12/hechos_v12.py escribe 54 cifras (ids `V12-`) en output/v12/hechos/hechos.json, que
   src/v5/cifras_clave.py incorpora; atlas, lo_que_sabemos, por_que_ha_subido y la web citan por id (nada tecleado).
5. **Publicación:** atlas_v12.md (plantilla docs/v12/plantillas/atlas_v12.md, resumen en inglés), tablas_v12.xlsx
   (entradas en azul con fuente, cálculos como fórmulas en negro, vínculos entre hojas en verde, sin paneles
   inmovilizados, zip con fechas fijas) y fichas_v12.json del verificador: solo vía `make publicacion`.
6. **Web:** páginas «De dónde viene la población», «Quién es propietario» y «Dónde se construye»; fichas territoriales
   con filas «V12 ·» (CCAA, provincia, municipio ≥ 50.000 hab. y barrio); el verificador muestra V12-V02 y retira V02
   (campo `sustituye`).

## Revisión final (subagente revisor, ~82.000 tokens; veredicto REHACER → correcciones)
1. **Celdas suprimidas recuperables (B3):** en hogares por nacionalidad se publicaba el error relativo de las celdas
   suprimidas, del que se despeja la cuota. Ahora va en blanco si la celda no es publicable (también en la ECV, B6).
2. **Regularización catastral (B4):** se restaba al Catastro (sin País Vasco ni Navarra) un MIVAU con todas las
   provincias. Se calcula en la misma muestra (provincias con las dos fuentes). El valor escrito antes en B4.1 era de
   una versión previa; la cifra vigente es la de cifras_clave (V12-B4-regularizacion).
3. **Unidad de la brecha (B6):** la comparación a igual edad y renta es entre PERSONAS adultas (ponderadas con RB050)
   según su propia nacionalidad, no entre hogares: se corrige la redacción en cifras, atlas, lo_que_sabemos y F22.
4. **Supresión complementaria (València por sección y barrio):** si en un territorio-año solo quedaba oculto un país,
   EXT − Σ publicados lo revelaba; se oculta también el país publicado más pequeño.
5. **Jefatura (B3):** las tablas publicadas vacían tasa y recuentos con < 10 personas de referencia en la muestra o
   error relativo > 30 %; la descomposición sigue usando la tabla completa y solo publica totales.
6. **Caché OD y saldos por edad (B2):** la caché origen-destino (celdas < 5) sale de output/ a data/cache/v12 (interna,
   no difundible, con LEEME); en los saldos interiores por edad × nacionalidad se vacían las celdas con < 10 altas o
   < 10 bajas.
7. **Neutralidad:** `pct_var_explicada_por_EXT` → `cuota_variacion_EXT_sobre_total`; «efecto» → «componente» en la
   descomposición reciente de hogares (B3).
8. **Periodo y cobertura** de las cifras de oferta en atlas, lo_que_sabemos y por_que_ha_subido (2021-2024; 46
   provincias con Catastro estatal y MIVAU).
9. **Umbral de C1 en la oferta provincial:** de 25 % a 10 %; en vivienda turística (B7) no se asigna C1 (INE y
   registro miden cosas distintas). El atlas lo dice expresamente.
10. **Familias de Holm:** se ajusta por bloque (B2: 32 especificaciones; B5: 18; B7: 15), porque cada bloque responde a
    una pregunta distinta con variables distintas; ninguna conclusión depende de un único p ajustado.
