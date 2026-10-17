# V15 · Lectura de filas sub-provinciales de las provincias selladas en v6 (V10-V14)

Fecha: 2026-10-17. Encargo del autor antes del depósito de V15. Sin estimar ningún efecto. No se ha leído data/sealed ni la parte sellada de V15.

## Qué se audita
- **Sellado de v6** (src/holdout.py, `provincias_selladas_v6`): 11 provincias, 07, 22, 26, 28, 30, 31, 33, 35, 38, 44 y 50, más sus municipios y distritos.
- **Desde V10.** La base única (src/v10/base.py) marcaba `muestra_sellada_v6` **solo en las filas de nivel provincia** (65.994 filas, «informativo»). Las filas de municipio, distrito y sección de esas provincias quedaban sin marca.
- **Pregunta.** Qué módulos de V10-V14 leyeron esas filas, para qué, y si eso afecta a alguna cifra publicada o a alguna evaluación sellada.

## Método
1. **Lectores de la base o de los crudos.** Búsqueda en src/v10-v14 de lectores de data/base (hechos.parquet, publica/hechos.parquet, vivienda.duckdb) y de crudos municipales o por sección.
2. **Uso real, medido en las salidas.** Escaneo de todas las tablas de output/v10-v14 en busca de códigos de municipio (5 dígitos), distrito (7) y sección (10) que empiezan por una provincia de v6. Un código en una salida demuestra que el módulo leyó esa unidad. Se descartan las columnas numéricas que se parecen a códigos.
3. **Cifras afectadas.** Cruce con output/v5/cifras_clave.csv por fichero de origen y cobertura.
4. **Cronología.**
   - Registro de evaluaciones selladas: docs/v2/holdout_accesos.md, 160 líneas `v6:`.
   - Commits de V10-V14.
   - Búsqueda de `evaluate_v*` y `holdout` en src/v10-v14.

## Cronología decisiva
- **Evaluaciones v6.** Todas son del 2026-10-11, entre las 10:41 y las 17:45 UTC. No queda ninguna hipótesis v6 pendiente de evaluar.
- **Base V10.** Primer commit de src/v10/base.py: 2026-10-14 14:16 UTC. Todas las lecturas de V10-V14 son **posteriores** a la última evaluación v6.
- **Evaluaciones en V10-V14.** Ningún módulo llama a `evaluate_v*` ni importa holdout.
- **Evaluaciones pendientes del repositorio.** `evaluate_v7` y `evaluate_v8` (2027) son temporales: periodos desde 2026-07-01 (`posterior_prereg`). No usan el bloque espacial de v6.

## Resultado por módulo

| Módulo | Variable(s) con filas sub-provinciales v6 | Unidades v6 en la salida | Uso | Cifras de cifras_clave | Clasificación |
|---|---|---|---|---|---|
| src/v10/atlas.py (b) | IPVA por distrito de las capitales (ipva_indice, distrito) | 10 de 48 capitales | Descriptivo: dispersión entre distritos | ninguna (tabla b_ipva_distritos_capitales) | sin efecto |
| src/v10/atlas.py (d) | Renta ADRH por sección agregada a provincia; censo anual por sección | todas las secciones de las 11 provincias | Descriptivo: alquiler/renta provincial | V10-ATL-D1 (rango provincial) | sin efecto |
| src/v10/atlas.py (e) | SERPAVI municipal (serpavi_alquiler_m2_mediana) | Palma 07040 y Zaragoza 50297 | Descriptivo: ciudades comparables | V10-ATL-E-07040, V10-ATL-E-50297 | sin efecto |
| src/v10/web.py | censo anual y SERPAVI municipal; titularidad y presión V12 | fichas de municipios ≥ 50.000 hab. de las 11 provincias | Descriptivo: páginas de consulta | ninguna nueva (reproduce cifras publicadas) | sin efecto |
| src/v10/figuras.py | base pública (mapas y series) | provincial; municipal solo en la Comunitat Valenciana | Descriptivo | ninguna nueva | sin efecto |
| src/v12/b1_contabilidad.py | MNP, EVR, EMCR (microdatos con municipio de residencia), padrón y censo anual municipales (data/raw) | 12.534 filas municipio-año; totales nacionales y provinciales | Contable descriptivo (identidad con residuo) | V12-B1-* de España (20 cifras: 5 periodos × 4 componentes) | sin efecto |
| src/v12/b2_flujos.py | flujos origen-destino EMCR/EVR; SERPAVI y valor tasado municipal | área de Madrid; 17 de 74 destinos; 7.822 filas de saldos municipales | Descriptivo y asociación de rangos (Spearman con Holm, C4) | V12-B2-madrid-saldo-corona | sin efecto |
| src/v12/b3_hogares.py | microdatos de los Censos 2011 y 2021; jefatura municipal | 103 de 394 municipios > 20.000 hab. | Contable descriptivo (descomposición) | V12-B3-hogares-* y V12-B3-reciente-* (España) | sin efecto |
| src/v12/b4_oferta.py | Catastro URBANA municipal; censo anual | 198 de 759 municipios; 20.430 filas de obra neta | Descriptivo | V12-B4-* (España sin País Vasco ni Navarra) | sin efecto |
| src/v12/b5_propiedad.py | titularidad catastral municipal; SERPAVI, IPVA, valor tasado, VUT y ADRH municipales | 191 de 728 municipios del ranking | Descriptivo y asociación (Spearman con Holm, C4) | V12-B5-* (España; fichero nacional del Catastro) | sin efecto |
| src/v12/f0_correcciones.py | titularidad JAXI y Catastro municipal | 1.362 filas municipales | Descriptivo (empalme) | ninguna | sin efecto |
| src/v12/b7_turismo.py, b6_condiciones.py | — | ninguna (solo coincidencias numéricas en columnas de recuentos) | — | — | no lee filas v6 |
| src/v13/paquete_zenodo.py, src/v14/terceros_1_0.py, src/v14/escaneo_terceros.py | copia o filtra data/base/publica/hechos.parquet completo | todas | Empaquetado del depósito (sin cálculo) | ninguna | sin efecto |
| src/v11/*.py (fetch_*, base_v11.py) | descargas y construcción de la base | todas | Ingesta de datos | ninguna | sin efecto |

### Uso propio de V15 (fase 1, antes de esta auditoría)
Estas lecturas filtraban `NOT muestra_sellada_v6`, que entonces solo excluía las filas provinciales:
- auditorías descriptivas (output/v15/auditoria/), sin cifras de cifras_clave;
- inventario (docs/v15/inventario_variables.*), que es metadato de toda la base;
- cálculo de potencia (output/v15/potencia/). Sus paneles de sección y municipio incluían las 11 provincias, solo con tratamientos placebo. **Se recalcula** tras la marca (decisiones G7) y el pre-registro cita las cifras nuevas.

El entrenamiento de V15 (data/processed/v15) ya excluía esas filas: sellar_v15 aparta por código las provincias de v6.

## Clasificación y consecuencias
- **Afecta a una evaluación sellada: ninguno.** Todas las lecturas son posteriores a la última evaluación v6 (2026-10-11 17:45 UTC). Ningún módulo de V10-V14 evalúa con muestra sellada, y las evaluaciones pendientes (v7 y v8, 2027) no usan ese bloque.
- **Afecta a una cifra publicada: ninguno.** Las cifras listadas se calcularon con esas filas cuando su uso ya no comprometía ninguna evaluación. Sus valores son correctos como datos y no hay nada que corregir.
- **Sin efecto: todos los casos.** No hay entrada en ERRATA ni parada. Queda documentado que estas cifras de la 1.0 incluyen unidades del bloque espacial de v6, ya evaluado.

## Cambios hechos
1. **Marca en la base.**
   - src/v10/base.py marca ahora `muestra_sellada_v6` también en municipio, distrito y sección de las 11 provincias.
   - src/v15/marca_v6.py aplicó la misma regla a la base construida: data/base/hechos.parquet, data/base/publica/hechos.parquet y la tabla `hechos` de vivienda.duckdb. Comprueba por huella que las demás columnas no cambian.
   - Filas marcadas: 3.642.696 (antes, 65.994).
   - El diccionario (docs/v10/diccionario_base.md) se actualiza.
2. **Control en `make check`** (src/v15/check_v15.py, «lecturas v6»):
   - Todo script de src/ que lea la base debe filtrar `muestra_sellada_v6`, salvo src/holdout.py, el constructor de la base (src/v10/base.py), los scripts que la mantienen sin análisis (src/v15/marca_v6.py y src/v15/correcciones_metadatos_1_0.py) y la lista cerrada de módulos heredados de esta tabla.
   - Los heredados están en docs/v15/contaminacion_v6_heredados.csv con su sha256. Si se modifican, el control los trata como nuevos y exige el filtro.
3. **Lo que el control no cubre.** No cubre las lecturas de crudos (data/raw), que no llevan marca. En V15, los módulos de estimación solo pueden leer data/processed/v15, y check_v15 («sellado») ya lo exige.
