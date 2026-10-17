# Familia tension_social: fuentes (V16, fase 1)

Fecha de descarga: 2026-10-17. Manifiesto con sha256 y licencia por fichero: `data/raw/v16/tension_social/_manifest.csv` (67 filas). Scripts reproducibles en `data/raw/v16/tension_social/_scripts/`. Ningún fichero supera 50 MB (total 22 MB); no hay `_grandes/`.

## 1. CGPJ, efecto de la crisis en los órganos judiciales (lanzamientos y ejecuciones hipotecarias)
- Página: https://www.poderjudicial.es/cgpj/es/Temas/Estadistica-Judicial/Estadistica-por-temas/Datos-penales--civiles-y-laborales/Civil-y-laboral/Efecto-de-la-Crisis-en-los-organos-judiciales/ ; ficheros bajo `https://www.poderjudicial.es/stfls/ESTADISTICA/FICHEROS/Crisis/`. Solo xlsx (no hay CSV ni PC-Axis para esta estadística en la página).
- Edición: 2T-2026 (última publicada el 2026-10-17). robots.txt: Crawl-delay 5; se respetó (6 s) y las rutas no están vetadas.
- Descargado en `_terceros/`: lanzamientos por partido judicial 2013-2025 (anual, por causa: ejecución hipotecaria, LAU, otros; sha idéntico al de data/raw/v5); series por TSJ 2T-2026 (amplía v5, que tenía 1T-2026); **series por provincia 2T-2026 (nuevo)**: hojas «Lanzamientos pract. Total/E.hipotecaria/L.A.U./Otros prov», «Ej.Hipot por provincias», «Ver. pos.ocupas»..., trimestral desde 2013-T1; datos 2T-2026 y anual 2025 (sin inspeccionar en detalle). No se descargaron los trimestrales 2021-2025 individuales (las series ya los recogen).
- Licencia: el Aviso Legal (https://www.poderjudicial.es/cgpj/es/Poder-Judicial/Aviso-Legal/) devuelve «No hay información disponible» y el pie solo dice «Copyright © Consejo General del Poder Judicial». No hay condiciones de reutilización verificables; la DA 2.ª de la Ley 37/2007 remite a la LOPJ para resoluciones judiciales. **Redistribuible: dudoso** (coherente con data/raw/v5 y docs/v8_1/inventario_licencias.csv). Los ficheros van a `_terceros/`.
- Cobertura: partido judicial (anual, solo nombre, 2013-2025); provincia y TSJ (trimestral 2013T1-2026T2).

## 2. Tabla partido judicial -> municipio (código INE)
- Ministerio de Justicia, Nomenclátor de Partidos Judiciales (PDF, 204 págs., pie 30/12/2025): https://www.mjusticia.gob.es/es/JusticiaEspana/OrganizacionJusticia/Documents/Nomencl%C3%A1tor%20de%20Partidos%20Judiciales.pdf
- Contiene 8132 municipios con código INE y 431 partidos, numerados dentro de cada provincia. Derivado `_terceros/derivado_pj_municipio.csv` (script `parsea_nomenclator_pj.py`; marcado como derivado).
- Licencia: el aviso general (https://www.mjusticia.gob.es/es/aviso-legal) limita a uso privado; la sección de datos abiertos (https://sede.mjusticia.gob.es/informacion-ayuda/datos-abiertos-ministerio) permite reutilización con cita (Ley 37/2007), pero este PDF no figura como conjunto de datos abiertos. **Redistribuible: dudoso.**
- Nota: los ficheros CGPJ identifican el partido por nombre; el PDF por número dentro de provincia. El cruce (nombre CGPJ -> número -> municipios) queda para la fase de construcción; los partidos judiciales cambian con la demarcación (2013-2025 frente a 30/12/2025), por lo que hay que comprobar fusiones/creaciones.

## 3. Paro registrado y afiliación por municipio
- Ya en el repositorio, sin ampliar: `data/raw/v9/sepe_municipios` (paro y contratos, 2006-01 a 2026-08) y `data/raw/v11/ss_afiliacion_municipio` (2011-12 a 2026-09). Cubren hasta el último mes publicado a 2026-10-15; no falta periodo.

## 4. Migraciones
- Ya en el repositorio: EVR 1988-2021 (`data/raw/v11/ine_evr`), padrón por nacionalidad y país de nacimiento municipal 2003-2022 (`data/raw/v9/ine_padron_nacionalidad`).
- Descargado (INE, reutilización con cita, Ley 37/2007; redistribuible sí):
  - EMCR (Estadística de Migraciones y Cambios de Residencia, op. 455), municipio, **2021-2024**: tablas 69696 (inmigraciones del extranjero), 69711 (emigraciones al extranjero), 69743/69745 (inter-municipales por nacionalidad, destino/origen), 69744/69746 (por país de nacimiento), 69767 (saldos). Es una serie nueva: hay ruptura metodológica con la EVR (que acaba en 2021); no unir sin análisis.
  - Cifras oficiales del padrón por municipio y sexo (tabla 29005), 1996-2025 (1 enero): rellena 2023-2025 en población total (no por nacionalidad).
  - Padrón por sección censal, 1 enero 2022, sexo x sección x nacionalidad (continentes), 52 ficheros PC-Axis (`NN02.px`).
- Hallazgo: el INE no publica ya el padrón municipal por nacionalidad después de 2022 (la página de resultados del Padrón termina en 2022; la op. ECP solo tiene nivel provincial/nacional). La sección censal existe 2004-2022 en INEbase (`.../t20/e245/p07/aAAAA/l0/NNxx.px`; xx = 01 edad, 02 continentes, 03 principales nacionalidades, 04 UE, 05 relación nacimiento-residencia, 06 país de nacimiento); solo se descargó 2022 x02 como muestra. Para el resto de años o tablas basta parametrizar `descarga_ine.sh`.

## Fuentes fallidas
- INE EVR microdatos: `https://www.ine.es/ftp/microdatos/varires/datos_{2022..2025}.zip` devuelve 404 (verificado 2026-10-17); último disponible datos_2021.zip. La EMCR lo sustituye.

## Requiere al autor
- Nada exige registro. Opcional: confirmar con el CGPJ la reutilización de las estadísticas judiciales (Servicio de Estadística Judicial, formulario de contacto de poderjudicial.es) y con el Ministerio de Justicia la del Nomenclátor, si se quiere publicar estos datos en la capa pública.

## Normalización (V16 fase 1)

Script: `src/v16/datos/tension_social.py` (determinista, SEED=20261010, sin red). Tests: `tests/v16/test_datos_tension_social.py`. Diccionario: `docs/v16/fuentes/tension_social_variables.csv`. capa = C4 y posterior_prereg = False (el corte de V16 no está fijado).

### Salidas
- `data/processed/v16/tension_social.parquet` (versionado; solo INE, 3 248 643 filas, 6,4 MB): EMCR municipal 2021-2024 (7 tablas; también filas nacional y provincia que trae el INE), cifras oficiales del padrón por municipio y sexo 1996-2025 (1 de enero) y padrón por sección censal 2022 (sexo x nacionalidad por continentes). Nada del CGPJ.
- `data/processed/v16/tension_social_terceros.parquet` (NO versionado; redistribuible = False; 36 904 filas): lanzamientos practicados (total, ejecución hipotecaria, LAU, otros) por provincia (trimestral 2013T1-2026T2) y por partido judicial (anual 2013-2025), y ejecuciones hipotecarias presentadas por provincia (trimestral 2007T1-2026T2; se conserva la serie completa).
- `data/processed/v16/tension_social_partidos_municipios_terceros.parquet` (NO versionado): partido judicial -> municipios (código INE) del nomenclátor a 30/12/2025, con el nombre del CGPJ cuando hay cruce, y las filas del CGPJ descartadas.

### Rupturas
1. EMCR 2021-2024 frente a la EVR (1988-2021, v11): otra operación estadística y otra metodología; no se unen las series. Las tablas 69743/69745 (nacionalidad) y 69744/69746 (país de nacimiento) se interpretan como llegadas (destino) y salidas (origen): comprobado con el saldo interior de la tabla 69767 (llegadas - salidas = saldo interior en el 100 % de los municipios en 2024, ambos sexos, total).
2. Padrón: las cifras oficiales por municipio usan la relación de municipios de cada año; los códigos que desaparecen o se crean (fusiones, segregaciones) dejan series incompletas. Padrón por sección: seccionado de 1/1/2022; territorios.parquet usa el seccionado 2025. No hay padrón municipal por nacionalidad posterior a 2022 (solo la sección 2022 de esta familia).
3. CGPJ provincial: el CGPJ cuenta Ceuta en Cádiz y Melilla en Málaga (no hay filas propias); los códigos de provincia son los INE mediante una tabla explícita en el script (50 nombres; Ceuta y Melilla solo en el cruce de partidos). Las sumas de provincias reproducen el TOTAL de cada hoja en todos los trimestres.
4. CGPJ partido judicial: el fichero anual identifica el partido solo por el nombre de la cabecera y la demarcación cambia (2013-2025 frente al nomenclátor a 30/12/2025); los partidos creados, suprimidos o fusionados en el periodo no se pueden reconstruir con estos ficheros. El código es «PJ-<provincia INE>-<número en el nomenclátor>».
5. CGPJ 2025 por partido: en 24 provincias la suma de partidos difiere más de un 10 % de la serie provincial 2025 (p. ej. PJ-32-2 = 2 944 frente a 152 en toda la provincia de Ourense); las filas 2025 llevan la advertencia en metodo_dato. Las ediciones de ambos ficheros difieren (anual 2013-2025 frente a series 2T-2026). No se corrige nada.

### Cruce nombre del CGPJ -> partido del nomenclátor
- El PDF no incluye el nombre del partido (la cabecera solo va en color). Método: nombre normalizado (mayúsculas, sin tildes ni signos, variantes de las lenguas separadas por «/» y artículos recolocados) comparado con los municipios del nomenclátor DENTRO de la provincia; solo se acepta una coincidencia única y un número de partido asignado a una sola fila. Supuesto: el partido recibe el nombre de su cabecera.
- La provincia de cada fila del CGPJ (la hoja no la trae) se asigna repartiendo las 431 filas en bloques consecutivos por provincia en el orden de la hoja provincial, con el mejor ajuste a los totales provinciales anuales y penalizando los nombres que solo existen como municipio en otra provincia (programación dinámica, determinista). Ceuta (51) y Melilla (52) por tabla explícita.
- Resultado: 427 de 431 filas con cruce único. Descartadas (sin coincidencia): CANGAS DE NARCEA (33; el nomenclátor dice «Cangas del Narcea»), MAO-MAHON (07; «Maó»), VILLARCAYO DE MERINDAD DE CASTILLA LA VIEJA (09; nombre truncado en el PDF), VILLAROBLEDO (02; «Villarrobledo»). Quedan sin serie del CGPJ los partidos PJ-33-1, PJ-07-1, PJ-09-3 y PJ-02-6 (37 municipios, que siguen en la tabla de correspondencia). No se usó coincidencia aproximada.
- Los 8 132 municipios del nomenclátor existen en territorios.parquet.

### Descartes y decisiones
- Padrón (tabla 29005): todos los códigos de municipio están en territorios.parquet; se conservan 4 con vigente_2025 = False (15026, 15063, 36011, 36012). Los municipios sin ningún dato (celdas vacías del INE) no generan filas. Ningún código descartado por ausencia en territorios; igual en la EMCR (0) y en las secciones (0 descartadas; 275 códigos con vigente_2025 = False conservados).
- Celdas vacías del INE (EMCR: 63 filas; padrón: 26 292) se omiten.
- muestra_sellada_v6 = True en provincia, municipio y sección de las 11 provincias del holdout (22,8 % de las filas versionadas). Decisión conservadora: los partidos judiciales (nivel «partido_judicial», solo terceros) heredan la marca de su provincia aunque la regla no los nombre.
- No se procesaron los otros dos libros del CGPJ (datos 2T-2026 y anual 2025 por órgano) ni las hojas de concursos, despidos, monitorios y verbales posesorios; fuera del encargo.
- Los datos del CGPJ y del nomenclátor son de licencia dudosa: nada de ello entra en el parquet versionado.
