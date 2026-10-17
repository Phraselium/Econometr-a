# V16 · Fase 1 · Base de intervenciones (ficha de fuentes)

Descarga: 2026-10-17. Calendario normativo descriptivo: no evalúa ninguna medida. Ficheros en `data/raw/v16/intervenciones/`; constructor reproducible sin red en `_scripts/build_intervenciones.py` (lee los XML del BOE guardados); manifiesto en `_manifest.csv`; checksums de los XML en `_sha256_boe.txt`.

Resultado: `intervenciones.csv` con 158 filas propias (66 ITP, 39 AJD, 15 suspensiones, 5 topes, 5 bono, 5 planes, 4 avales, 4 incentivo IRPF, 7 vivienda turística, 3 IBI, 2 golden visa, 3 vivienda pública) más las 318 declaraciones de zona tensionada que `src/v16/f1_intervenciones.py` toma de `data/raw/v9/regulacion/zonas_tensionadas_v9.csv` (no se copian). Verificación por fila: 50 VERIFICADA, 106 SECUNDARIA, 2 NO VERIFICADA.

## Fuentes

### 1. BOE (disposiciones, XML) · `boe/*.xml` (35 ficheros)
- Endpoint: `https://www.boe.es/diario_boe/xml.php?id=BOE-A-AAAA-NNNNN`; localización por `https://www.boe.es/datosabiertos/api/legislacion-consolidada` y `.../api/boe/sumario/{AAAAMMDD}`.
- Edición: texto publicado y análisis jurídico a 2026-10-17. Cobertura: 2008-12-25 a 2026-04-23 (fecha de las disposiciones usadas); estatal y autonómicas publicadas en el BOE.
- Licencia: reutilización libre con cita de la fuente (aviso legal del BOE, https://www.boe.es/informacion/aviso_legal/; Ley 37/2007 y Real Decreto 181/2008). Redistribuible: sí. sha256: ver `_sha256_boe.txt`.
- Uso: topes (RDL 6/2022, 11/2022, 20/2022, Ley 12/2023, Resolución INE 18-12-2024), bono alquiler joven y planes (RD 2066/2008, 233/2013, 106/2018, 42/2022, 326/2026), avales (convenio MIVAU-ICO, BOE-A-2024-9128), desahucios (cadena de RDL sobre el RDL 11/2020, RDL 1/2024), golden visa (LO 1/2025), IBI e IRPF (Ley 12/2023), vivienda turística (RD 1312/2024, DL catalán 3/2023, DL balear 4/2025, Ley canaria 6/2025).
- Leído el texto oficial en cada fila VERIFICADA. Solo se transcribe lo que se leyó; donde un apartado no se leyó entero, la nota de la fila lo dice.

### 2. Ministerio de Hacienda, «Tributación Autonómica. Medidas AAAA», capítulo I (2009-2026) · ITP y AJD
- Endpoint: `https://www.hacienda.gob.es/SGFAL/FinanciacionTerritorial/Autonomica/Capítulo I Tributación Autonómica AAAA.pdf` (2009-2020) y `.../Capitulo-I-Tributacion-Autonomica-AAAA.pdf` (2021-2026). Ediciones anuales; la de 2026 está actualizada a 2026-09-23.
- Cobertura: CCAA de régimen común, tipo general de ITP (transmisiones onerosas de inmuebles) y de AJD (cuota gradual), 2010-2026; País Vasco y Navarra solo como fila «régimen foral» sin tipos.
- Licencia: el aviso legal del Ministerio (https://www.hacienda.gob.es/es-ES/Paginas/AvisoLegal.aspx) prohíbe reproducir y distribuir sin autorización. Redistribuible: dudoso. Los 18 PDF están en `_terceros/hacienda_tributacion_autonomica/` (ignorada por git); en el CSV solo constan los tipos impositivos, que son hechos normativos, con la edición como fuente.
- Limitación: la fuente resume el resultado del ejercicio de competencias, no cita la ley autonómica de cada cambio. No se ha contrastado ninguno con su ley autonómica (verificación SECUNDARIA). Las fechas exactas figuran solo cuando el texto las da (cambios con día); si no, `fecha_efecto` es el 1 de enero del año de la primera edición que recoge el valor y la nota lo indica. Los tipos con escala figuran como dos filas (mínimo y máximo).
- Observación: la edición 2020 rotula «año 2021» en sus resúmenes (errata de la fuente).

### 3. Panorama de la fiscalidad autonómica y foral (REAF, Consejo General de Economistas)
- No usado como fuente de datos. `economistas.es` y `reaf.economistas.es` devuelven 403 a la descarga automática; las ediciones 2018 y 2019 se localizaron en un alojamiento de terceros (sdelsol.com), con «© Servicio de Estudios de REAF Asesores Fiscales» y sin licencia de reutilización: redistribuible no, y no se guardaron en el repositorio. Pendiente: tipos reducidos (jóvenes, familias numerosas, VPO), que solo esa publicación o las leyes autonómicas dan con cifras.

### 4. La Moncloa y MIVAU (documentos oficiales) · vivienda pública anunciada y entregada
- Endpoints: resumen del Consejo de Ministros de 2026-04-21, referencia de 2026-06-02 (lamoncloa.gob.es) y nota de prensa del Boletín estadístico 2024 del Observatorio de Vivienda y Suelo (mivau.gob.es, 2025-07-04). El MIVAU devuelve 403 sin cabecera User-Agent de navegador.
- Licencia: aviso legal no comprobado. Redistribuible: dudoso (copias en `_terceros/oficiales_aviso_legal_no_comprobado/`).
- Cifras recogidas: dotación 7.000 millones del Plan Estatal 2026-2030; cuarta adenda CASA 47 con 1.629 viviendas en 22 proyectos; 14.371 calificaciones definitivas de viviendas protegidas en 2024.

### 5. Zonas tensionadas posteriores al corte de v9
- `zonas_tensionadas_v16_nuevas.csv`: solo cabecera. Los sumarios del BOE de 2026-10-15, 16 y 17 no contienen resoluciones nuevas de zonas tensionadas (búsqueda por título). Los diarios autonómicos no se revisaron.

## Lagunas y NO VERIFICADO
- ITP/AJD: ninguna ley autonómica contrastada; tipos reducidos (jóvenes, familias numerosas, VPO) no recogidos; tipos forales no recogidos; el ITP general de Cantabria 2013-2017 y el de Aragón 2015-2016 dependen de la lectura de ediciones consecutivas.
- Topes: el texto de 2022-2023 remite al IGC y no fija cifra; no se transcribe el valor del IGC ni el mensual del IRAV (el 2 % citado habitualmente no figura en el artículo 46). No se comprobó si hubo prórroga del 3 % para 2025.
- Bono alquiler joven: solo la norma estatal; faltan las convocatorias autonómicas (fechas de resolución y requisitos propios) y la vigencia posterior a 2025.
- Avales ICO: solo el convenio de 2024; modificaciones posteriores no comprobadas; fecha de firma no recogida.
- Desahucios: cadena verificada hasta RDL 2/2026 (derogado); lo posterior a 2026-02-28 no se ha revisado (los RDL de septiembre-octubre de 2026 de v9 no se leyeron).
- IBI: solo el marco estatal (Ley 12/2023, DF 3.ª). No se halló fuente sistemática de ordenanzas municipales; ninguna ordenanza verificada.
- Vivienda turística: Barcelona (PEUAT 2017) SECUNDARIA; Madrid (Plan Reside) y València (moratoria 2024) NO VERIFICADAS. Plan Especial de Hospedaje de Madrid 2019, modificación del PEUAT, Palma, Málaga y San Sebastián: no incorporados.
- Incentivo IRPF: solo el régimen de la Ley 12/2023 (50/60/70/90 %); el régimen anterior (60 %) no verificado.
- Vivienda pública: el anuncio de 183.000 viviendas solo se localizó en prensa y no se incorporó; falta la serie anual de calificaciones definitivas (boletines OVS, anuario cap. 5) y el anuncio de la incorporación de viviendas de la Sareb a SEPES.
- Consolidación: `src/v16/f1_intervenciones.py` construye el id de zona como `ZT-<municipio>-<fecha_efecto>`; Llanes (33036) tiene dos zonas con la misma fecha (2026-07-30) y el id se duplica. No lo causa este fichero; requiere añadir un discriminador al id en el script.
