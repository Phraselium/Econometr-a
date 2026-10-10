# Fuentes fallidas v4

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
