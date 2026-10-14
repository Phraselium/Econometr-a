# Revisión independiente final de V10-DIFUSIÓN

Revisor independiente. Revisado el árbol de trabajo de la rama `r10/difusion` (con los cambios del bloque 7 sin commit) el 2026-10-14. No se ha leído data/sealed. No se han ejecutado `make all`, `make check` ni descargas. Sí se han ejecutado consultas de lectura con python3 y duckdb, y `python3 -m pytest -q tests/v10`, que da **31 passed**.

## Veredicto global: **REHACER**

La corrección es acotada: dos bloqueantes de capa y cuatro hallazgos importantes. La coherencia de cifras, la exclusión de `posterior_prereg`, la accesibilidad y el filtrado de licencias de los hechos públicos son correctos.

## Lo que se ha comprobado y está bien

- **Cifras: publicación y base.**
  - publicacion/cifras_clave.csv es igual a output/v5/cifras_clave.csv (1.092 filas).
  - data/base/publica/cifras_clave.parquet coincide celda a celda con el CSV: 0 diferencias tras normalizar los nulos.
  - El md5 de los parquet públicos (hechos, territorios, cifras_clave) es idéntico al de HEAD. El contenido de hechos también es idéntico: mismo hash agregado y EXCEPT vacío.
- **Cifras: atlas, texto y web.** Se han recalculado 14 cifras V10-ATL desde output/v10/atlas/*.csv, y todas coinciden con cifras_clave y con el texto del atlas.
  - Cifras: A1 26,7965; A2 7,172; A3 38,0701; A4 43,8489; A5 0,0567; A10 27,1416; A11 31,6787; B1 16,404 (nuevo 137,041 / existente 120,637); C1 19,4111 y C2 13,3068 (suma de secciones: 788.842→841.558 hab.; 104.970→163.356 extranjeros); D1 42,26 [28,59-66,87], 52 provincias; D2 31,93 [19,10-48,52], 68 municipios; E-46250 39,77 y E-03014 31,27.
  - Web frente a la base:
    - En fichas/provincia_46.html, el valor tasado (1.504,3) es la media de los cuatro trimestres de 2024 de `p_tasado` en hechos.parquet (1.504,35). La población 2025 (2.763.996), el porcentaje de extranjeros (15,9), el alquiler (6,69) y la carga de 44,4 coinciden con d_espana_provincias.csv.
    - En cv_municipios.geojson, Agost tiene 25,64 / 3,378 / 9,112, igual que d_cv_municipios.csv.
    - SERPAVI de València: 5,8537 y 8,1818 en la base, igual que en e_ciudades_comparables.
- **C1 del ECV.** Las 32 filas C1 de a_quien_ecv.csv tienen contraste con Eurostat y todas coinciden (diferencia máxima 0,05 p.). El hacinamiento no cumple el criterio (hasta 1,0 p.) y se queda correctamente en C4.
- **posterior_prereg.**
  - El atlas lee la base con `WHERE NOT posterior_prereg` (src/v10/atlas.py:34).
  - Los 27 JSON de indicadores y los 4 GeoJSON no tienen periodos de 2026T3 en adelante.
  - El panel filtra esas filas (src/v10/web.py:165).
  - El monitor las marca con la columna `posterior_prereg` («sí/no») (src/v10/monitor.py:173 y web.py:459).
  - En la EPA, 2026 solo llega a T1-T2.
- **Licencias en hechos y descargas de datos.**
  - hechos.parquet público: 10.104.941 filas, todas `redistribuible=True`. No hay ninguna variable de Registradores, Notariado, Incasòl, JK, CGPJ ni Interior.
  - SERPAVI cita AEAT-IRPF solo como origen administrativo del MIVAU.
  - Los ficheros de inventario_licencias.csv no permitidos de AEAT, CGPJ, Interior y Madrid no aparecen en el campo fuente de variables.parquet.
- **Accesibilidad.**
  - Las 9 páginas tienen `lang="es"`, título, enlace para saltar con `:focus` visible y texto alternativo en las 17 imágenes.
  - Mapas e indicadores tienen tabla equivalente (mapas.html:34, indicadores.html:37, app.js:24-31).
  - Contraste WCAG: texto suave 8,9:1; enlaces 6,6:1; etiquetas de capa con contraste mínimo de 5,3:1 (C4) y el naranja de foco 4,8:1. Todo cumple AA.
- **Neutralidad.** No hay menciones de partidos ni de personas en el atlas, la web, figuras/fichas.json ni el paper. Las frases sobre causas son negaciones explícitas («describe coincidencias, no causas»).
- **Fichas de figura.** Las 14 fichas de figuras/fichas.json tienen capa, fuente, fecha y texto alternativo.
- **Entradas versionadas.** Todo lo que lee base.py está versionado: data/processed (24/24 CSV), data/raw/v10/monitor y data/raw/v9/*/_manifest.

## Hallazgos

1. **[BLOQUEANTE] C1 sin ≥2 fuentes en cifras difundibles: V10-ATL-C1 y V10-ATL-C2.**
   - Evidencia:
     - src/v10/atlas_texto.py:116-122 asigna «C1 (recuento oficial del INE)» con una sola fuente («INE censo anual (suma de secciones)»).
     - CLAUDE.md:5 exige ≥2 fuentes para C1, y el único criterio C1 documentado en V10 (decisiones.md:63) es el contraste con Eurostat.
     - Los mismos datos figuran como C4 en c_valencia_seccion.csv y c_valencia_barrio.csv.
   - Corrección: pasar las dos cifras a C4 (o contrastarlas con una segunda fuente, por ejemplo el Padrón municipal de València, y documentarlo en decisiones). Después, regenerar cifras_clave, la publicación y la base.

2. **[BLOQUEANTE] La etiqueta de capa de la figura F01 muestra «C1» aunque incluye series C4.**
   - Evidencia: src/v10/web.py:322 usa `f.capa.split(' ')[0]`. La capa de F01 en fichas.json es «C1 en propiedad y alquiler de mercado…; C4 en alquiler inferior al de mercado y cesión», y la web muestra solo «C1» (index.html:93).
   - Corrección: si la capa es mixta, mostrar «C1/C4» o la capa mínima (C4) y el detalle en la nota, y añadir un test.

3. **[IMPORTANTE] C1 asignada por tabla y no por el criterio de ≥2 fuentes en la base y la web.**
   - Evidencia:
     - src/v10/base.py:457-480 (META_V9) marca C1 en IPVA, BCE, el registro de la GVA, Eurostat de plataformas, Incasòl y zt_vigente, todas de una sola fuente.
     - Ejemplos visibles: el catálogo de la web pone `p_tasado` nacional en C1 con la fuente única «mivau_valor_tasado…», y la ficha provincial muestra «Población extranjera 15,9 % C1 INE censo anual».
     - Hay además una incoherencia: `p_tasado` es C1 en la base y C4 en el atlas.
   - Corrección: documentar en decisiones qué significa C1 en la base (estadística oficial frente a hecho con ≥2 fuentes) o rebajar a C4 lo que no tenga contraste, y hacer que el test valide la regla.

4. **[IMPORTANTE] Lenguaje valorativo e implícitamente causal en los títulos.**
   - Evidencia: «Atlas descriptivo: quién sufre la subida y dónde» (publicacion/atlas_descriptivo.md:3), «Quién lo sufre» / «Quién sufre la subida» (navegación de las 9 páginas y quien.html:6,29) e index.html:76.
     - «Sufre» es valorativo.
     - «la subida» atribuye la sobrecarga al aumento de precios, cuando el atlas mide la sobrecarga, no el efecto de la subida.
   - Corrección: «Quién soporta más esfuerzo en vivienda y dónde» o «Esfuerzo y sobrecarga por grupos», también en la versión en valenciano («Qui ho pateix»).

5. **[IMPORTANTE] Dependencia circular en la reproducción.**
   - Evidencia:
     - base.py:666 lee publicacion/cifras_clave.csv.
     - Esa tabla depende del atlas (hechos.json → src/v5/cifras_clave.py → `make publicacion`), y el atlas lee data/base/publica/hechos.parquet.
     - No hay ningún objetivo del Makefile que fije el orden `base → atlas → publicacion → base`; `all` no incluye base, atlas ni web (Makefile:30).
     - Hoy todo es coherente, pero un `make base` ejecutado antes de `make publicacion` deja cifras_clave.parquet desfasado.
   - Corrección: un objetivo `v10` con el orden explícito (o que base escriba cifras_clave en un paso posterior a publicacion) y un test de identidad que se ejecute en `make check` (decisiones.md:41 lo declara; hay que confirmar que falla si el orden se rompe).

6. **[IMPORTANTE] El filtro de licencias permite por defecto.**
   - Evidencia: base.py:523 usa `lic.get(nombre, "permitida")`, de modo que los ficheros ausentes del inventario cuentan como permitidos. 35 de los 42 orígenes de hechos públicos no figuran por nombre en docs/v8_1/inventario_licencias.csv, y varias variables tienen como fuente «ver diccionario del panel de origen» o «derivada», sin fichero trazable.
   - No se ha encontrado ninguna fila indebida, pero la garantía depende de las expresiones regulares.
   - Corrección: denegar por defecto, completar el inventario para los paneles de data/processed y la v9, y testear que todo origen público tiene estado «permitida».

7. **[MENOR] Cifras derivadas de fuentes no redistribuibles en las descargas.** web/_site/descargas/cifras_clave.csv contiene 72 cifras agregadas de elaboración propia que citan Incasòl, Registradores o Notariado (por ejemplo, A23-A13, A23-P2). Son estadísticos propios publicados desde V5-V8, no datos crudos. Conviene dejarlo explícito en D5 y en el LÉEME de descargas.

8. **[MENOR] Intervalo de confianza imposible.** V10-ATL-A5 tiene un límite inferior del IC de −0,009 % para una proporción. Corrección: IC logit o Wilson, o truncar en 0 y anotarlo.

9. **[MENOR] Año de Catastro sin declarar.** La `fecha_dato` de d_cv_municipios.csv no indica el año de Catastro usado (atlas.py:201-213). En la base, Catastro 2026 está marcado `posterior_prereg` y se excluye. Corrección: añadir el año.

10. **[MENOR] Tipos de cifras_clave.parquet.** Guarda todas las columnas como texto (valor, min y max incluidos). La identidad con el CSV se cumple, pero al consumidor le llegan cadenas. Conviene documentarlo o tipar las columnas numéricas.

11. **[MENOR] Reloj del sistema en el monitor.** monitor.py:162 usa `dt.date.today().year` para marcar el «acumulado parcial». Fuera del modo sin red, el resultado depende de la fecha de ejecución. En modo sin red se conserva la fecha previa (correcto).

## Tokens usados

Aproximadamente 80.000.
