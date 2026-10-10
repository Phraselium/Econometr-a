# Fuentes fallidas v4

| Fuente | URL | Error | Alternativa | Fecha |
|---|---|---|---|---|

## M2 (2026-10-10)
- Censos 2011 y 2021, hogares por edad de la persona de referencia: no hay tablas en Tempus (CENSOP 463, CENSOPV 8); busqueda en src/v4/m2_fetch.py. Sin descarga. Jefatura por edad: fuente unica (EPA 65944).

## M3 (2026-10-10)
- SIU (suelo urbanizable y capacidad por municipio): https://siu.mivau.gob.es/ y https://sig.mivau.gob.es/siu/ (un intento en src/v4/m3_fetch.py red): ProxyError del proxy de salida, igual que en v3. Sin alternativa descargable; sigue la solicitud de transparencia.
- Coste de construcción en nivel (PEM/m2 y superficie de visados): el Boletín Online MIVAU (BoletinOnline2 y BoletinOnline; secciones de vivienda libre, índices de costes y «Construcción de edificios (licencias municipales de obra)», orden 10000000) no publica presupuesto de ejecución material, solo número, superficie y viviendas. MBC del Catastro: no se localizó el valor en una fuente oficial accesible (BOE consolidado devuelve índice sin texto). Se usa coste supuesto 900/1.200/1.500 EUR/m2, sin verificar.
- Empleo en construcción: Eurostat empleo NUTS2 es solo total; EPA ocupados solo por sexo y edad. Plazos de licencia: sin datos abiertos.
