# Fuentes fallidas v2 (MIVAU licencias, Catastro titularidad, AEAT IRPF municipios)

Nota: la ruta `docs/v2/fallidas/mivau_catastro_aeat.md` citada en el encargo no existe en el repo; este es el registro de fallos v2 (regla data-fetcher).

## 1. MIVAU: licencias municipales de obra (viviendas a construir), por provincia

- **URL probada:** índice del Boletín Online `https://apps.fomento.gob.es/BoletinOnline2/?nivel=2&orden=NNNNNNNN` para los órdenes 25000000 a 59000000 (todas las secciones).
- **Resultado:** ninguna tabla de licencias. Las secciones de vivienda son protegida (31xxxxxx), libre iniciada/terminada (32xxxxxx), parque (33xxxxxx), transacciones (34xxxxxx), valor tasado (35xxxxxx), suelo (36xxxxxx), tasaciones (46xxxxxx). Las de licencias no aparecen.
- **Búsqueda web:** sin serie nacional por provincia reciente. Solo aparecen anuarios autonómicos antiguos (1990-2004) y un conjunto regional de Aragón (2000-2019).
- **Error:** no hay endpoint. No se ha generado `mivau_v2_licencias.csv`.
- **Alternativa propuesta:** solicitar la serie al Ministerio (Secretaría General / Dirección General de Arquitectura, Vivienda y Suelo) o usar el INE/ datos.gob.es si existe una serie nacional actualizada. Hasta entonces, la oferta se aproxima con viviendas libres iniciadas y terminadas por provincia (`mivau_v2_iniciadas_terminadas_prov.csv`), que sí están disponibles.

## 2. Catastro: titulares personas físicas / jurídicas por municipio (anual)

- **URL probada:** `https://www.catastro.hacienda.gob.es/es-ES/estadisticas_3_1.html` (Titularidad, años 2006-2026, niveles nacional, CCAA, provincias y municipios).
- **Endpoint probado:** `https://www.catastro.hacienda.gob.es/jaxi/tabla.do?path=/est2025/catastro/titulares/&file=01001.px&type=pcaxis&L=0` (también 02001 y 03001). Devuelve HTTP 200 con una página HTML de visor JAXI (~30 KB), no un fichero PC-Axis.
- **Motivo del fallo:** el visor es una consulta dinámica (selección de dimensiones y envío de formulario). Descargarla equivale a scraping de página dinámica, que el proyecto no permite. No hay fichero publicado.
- **Alternativa propuesta:** solicitud formal de la tabla de titulares por municipio a la Dirección General del Catastro (Área de Estadística), o usar el número de unidades urbanas residenciales de `catastro_urbana_municipios.csv` como proxy de parque (sin la dimensión de titularidad).
- **Sustitución disponible (sí descargada):** Datos municipios > Urbano, ficheros publicados `https://www.catastro.hacienda.gob.es/documentos/estadisticas/URBANA{año}.xls` (2012-2026). Nota: las columnas cambian entre ejercicios (2012 C_INE sin nombres; 2019+ COD_INE_*); el parser de `src/fetch_catastro.py` lo gestiona.

## 3. AEAT: Estadística de los declarantes del IRPF por municipios (rendimientos del capital inmobiliario)

- **URLs probadas:**
  - `https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpfmunicipios/2022/docf763858820a87bad202022caf95a9d485a438a37a.html` (metodología y preguntas frecuentes; HTTP 200)
  - `.../irpfmunicipios/2022/jrubik13037deb09ada4cfd8419c0a25f34de2659073da.html` y `.../jrubik3f4ce804752cced1f00ae6b978c1f29b8d719818.html` (datos municipales por ámbito territorial y tamaño de población; HTTP 200)
  - `.../irpf/2023/home_parcialf78aea21b3550dfb02f0cbe6eefac18e5dbdd8b9.html` (estadística por partidas; HTTP 200)
  - `https://sede.agenciatributaria.gob.es/static_files/Sede/Tema/Estadisticas/Estadisticas_impuesto/Irpf_patrimonio/Irpfmunicipios/Documentacion/Nota_presentacion_IRPFM_2013.pdf` (nota de presentación 2013; HTTP 200, PDF)
- **Error:** las páginas de datos muestran la tabla municipal con una consulta dinámica ("Visualizar datos", selectores de CCAA y tamaño). No enlazan ningún fichero xls/csv/zip. Un índice `.../Irpfmunicipios/index.html` devuelve 404.
- **Error de TLS en `www.agenciatributaria.es`:** la petición falla por "CA signature digest algorithm too weak" con el almacén por defecto. No se ha desactivado la verificación. Se ha usado solo el host `sede.agenciatributaria.gob.es`.
- **Alternativa propuesta:** solicitar al Servicio de Estudios Tributarios y Estadísticas de la AEAT el fichero de la estadística por municipios (2013-2022), o la publicación por partidas a nivel provincial si existe en fichero. Mientras tanto, no se incluye ninguna serie de capital inmobiliario en el modelo.
- **Fichero generado:** ninguno (`aeat_irpf_capital_inmobiliario.csv` no se crea). `src/fetch_aeat.py` hace una única petición de comprobación y termina con código 0.
