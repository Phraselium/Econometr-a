# Fuentes fallidas v4

## M5a (2026-10-10)
- Programa electoral 2023 de un grupo con representación (grupo sin codificar nº 1): las copias https://theobjective.com/wp-content/uploads/2023/07/programa-vox-23j.pdf y https://static.poder360.com.br/2023/07/Programa-VOX-2023.pdf superan los 10 MB de WebFetch (maxContentLength). Sin medidas codificadas; no sustituido por prensa.
- Programa electoral 2023 de un grupo catalán con representación (sin codificar nº 2): no localizado en su sitio oficial (la búsqueda devuelve documentos de otras elecciones). Sin medidas.
- Programa electoral 2023 de un grupo canario con representación (sin codificar nº 3): no localizado en su sitio oficial (solo el de 2015). Sin medidas.
- Proposiciones de ley sobre vivienda de la XV legislatura (congreso.es): no consultadas por límite de presupuesto de la tarea (pendiente de una segunda pasada).
- Tres de los programas codificados se leyeron en copias alojadas por medios (elindependiente.com, theobjective.com), no en el sitio del grupo (no localizado). No se comprobó que la copia coincida con la versión oficial. La nota de prensa de resumen de uno de ellos (pp.es) solo trae un extracto y no se usó.
- Un programa 2023 hallado en elnacional.cat corresponde a un partido sin representación en el Congreso en la XV legislatura; excluido.
- Lectura parcial: un documento de 16 páginas se leyó en pp. 2-6; otro solo en pp. 45-47; otro en pp. 113-114; otro en pp. 14-16; otro en pp. 72-76 (impresas); otro en pp. 207-220; otro en pp. 21-22, 31-33 y 78-79. Medidas de vivienda fuera de esas páginas pueden no estar recogidas.
- Crossref (HTTP 429): Sinai y Waldfogel (2005) y Fack (2006) sin verificar.
- Scimago (scimagojr.com): 403 en v3; no reintentado.

| Fuente | URL | Error | Alternativa | Fecha |
|---|---|---|---|---|

## M2 (2026-10-10)
- Censos 2011 y 2021, hogares por edad de la persona de referencia: no hay tablas en Tempus (CENSOP 463, CENSOPV 8); busqueda en src/v4/m2_fetch.py. Sin descarga. Jefatura por edad: fuente unica (EPA 65944).

## M3 (2026-10-10)
- SIU (suelo urbanizable y capacidad por municipio): https://siu.mivau.gob.es/ y https://sig.mivau.gob.es/siu/ (un intento en src/v4/m3_fetch.py red): ProxyError del proxy de salida, igual que en v3. Sin alternativa descargable; sigue la solicitud de transparencia.
- Coste de construcción en nivel (PEM/m2 y superficie de visados): el Boletín Online MIVAU (BoletinOnline2 y BoletinOnline; secciones de vivienda libre, índices de costes y «Construcción de edificios (licencias municipales de obra)», orden 10000000) no publica presupuesto de ejecución material, solo número, superficie y viviendas. MBC del Catastro: no se localizó el valor en una fuente oficial accesible (BOE consolidado devuelve índice sin texto). Se usa coste supuesto 900/1.200/1.500 EUR/m2, sin verificar.
- Empleo en construcción: Eurostat empleo NUTS2 es solo total; EPA ocupados solo por sexo y edad. Plazos de licencia: sin datos abiertos.
| Catastro: titulares por tipo (persona física o jurídica) por provincia o municipio | https://www.catastro.hacienda.gob.es/documentos/estadisticas/ (URBANA2024.xls y sondeo de TITULARES*.xls) | URBANA solo trae unidades urbanas, valor y superficie; no hay fichero abierto de titulares por tipo (las URL de prueba devuelven la página 404) | Sin alternativa: peso de personas jurídicas en el stock sin dato (M4-V2 NO ANALIZADA: FALTAN DATOS) | 2026-10-10 |
| Incasòl y dades obertes de la Generalitat: tipo de arrendador (persona física o jurídica) | analisi.transparenciacatalunya.cat (qww9-bvhh; catálogo con búsquedas «arrendador», «persona jurídica») | qww9-bvhh solo trae municipio, tramo de renta y periodo; el catálogo no devuelve ningún conjunto con tipo de arrendador | Ninguna; el IHB (w8kv-kmwv) solo cubre viviendas vacías de grandes tenedores y no se usa | 2026-10-10 |
| Registradores: compras por personas jurídicas y compras de extranjeros separadas por residencia | data/raw/pdf/registradores_* | Las series extraídas solo traen % de compras de extranjeros (sin residentes y no residentes) y ninguna de personas jurídicas | Notariado y MIVAU para residentes y no residentes; INE ETDP para personas jurídicas (fuente única) | 2026-10-10 |
| EFF por percentil de riqueza (otras propiedades) | data/raw/v3/eff_tenencia_edad_v3.csv | Solo hay desglose por edad | Edad (oleada 2022) | 2026-10-10 |
