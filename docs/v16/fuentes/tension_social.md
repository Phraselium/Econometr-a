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
