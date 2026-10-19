Análisis a posteriori (V17). Fuentes descargadas para la auditoría.

Familia «turismo_local», V17 fase 1. Fecha de descarga: 2026-10-19. Manifiesto con endpoint, edición, licencia y sha256: data/raw/v17/turismo_local/_manifest.csv. Ya existían y no se repiten: INE VTE (data/raw/ine_v2_vut.csv, data/raw/v16/alquiler_turismo), Censo 2021 (data/raw/v11/ine_censo2021) y la carpeta data/raw/v3_orig/vut_seccion.

## 1. InsideAirbnb: listings.csv resumido, última edición (descargado)

- Página de origen: https://insideairbnb.com/get-the-data/ (robots.txt: solo bloquea a ia_archiver en /get-the-data; no bloquea la descarga). Endpoint de cada fichero: https://data.insideairbnb.com/spain/<región>/<ciudad>/<fecha>/visualisations/listings.csv (enlaces ofrecidos en esa página). Una descarga por fichero, con 5 s de pausa; no se descargó el listings detallado, ni calendar ni reviews.
- Ediciones (scrape): Barcelona 2026-09-17, Madrid 2026-09-17, Mallorca 2026-09-19, València 2026-09-20, Girona 2026-09-25, Sevilla 2026-09-25, Euskadi 2026-09-25, Málaga 2026-09-28, Menorca 2026-09-28. Total 110.022 líneas, 31 MB (menos de 50 MB: no se ignora en git; ver redistribución). Carpeta data/raw/v17/turismo_local/insideairbnb/, ficheros listings_resumen_<ciudad>_<fecha>.csv, sin transformar. sha256 en el manifiesto.
- Columnas (cabecera de Barcelona): id, name, host_id, host_profile_id, host_name, neighbourhood_group, neighbourhood, latitude, longitude, room_type, price, minimum_nights, number_of_reviews, last_review, reviews_per_month, calculated_host_listings_count, availability_365, number_of_reviews_ltm, license.
- Licencia: «This data is licensed under a Creative Commons Attribution 4.0 International License» (texto de la página get-the-data), https://creativecommons.org/licenses/by/4.0/ . Políticas de uso (https://insideairbnb.com/data-policies/): «Only take the data you need. Do not scrape data from the site [...] Do not republish the data [...] Inside Airbnb data should be attributed and cited appropriately». Redistribuible: DUDOSO. CC BY 4.0 lo permitiría con atribución, pero la política del proyecto pide no republicar. Recomendación: no incluir los ficheros en la capa pública de la base ni en publicacion/; usar solo agregados propios con atribución. Los ficheros están en data/raw/ (cuya política es la del repositorio); el autor decide si se mantienen versionados o se ignoran por la petición de no republicar.
- Cobertura: los anuncios activos en el scrape de cada ciudad; no son viviendas turísticas con registro (ver la nota sobre sesgos en la política «Data Assumptions» de Inside Airbnb, no leída entera). Las unidades son anuncios, no viviendas; hay anuncios de habitaciones (room_type) y multianuncios del mismo anfitrión (calculated_host_listings_count). Cobertura geográfica: solo estas 9 áreas, que no son un recuento nacional ni sección censal (hay latitud y longitud para asignar secciones; el cruce territorial en el proyecto es solo por código INE, V7).

## 2. InsideAirbnb: edición de 2019 o 2020 (NO descargada, requiere al autor)

- La página ofrece solo los últimos 12 meses. Política «Free vs Archived Data»: los datos anteriores están archivados y «must be requested via an Archived Data Request»; las peticiones se evalúan según cantidad, uso previsto e identidad del solicitante y pueden rechazarse o pedir pago.
- Paso exacto: el autor envía una «Archived Data Request» desde https://insideairbnb.com/data-policies/ (enlace «Data Request» de esa página) pidiendo listings.csv de 2019 o 2020 de las ciudades españolas (Barcelona, Madrid, València, Málaga, Sevilla, Palma/Mallorca...), indicando uso (auditoría independiente de la relación entre turismo y alquiler). No se intentó la petición ni se buscaron URL antiguas por patrón.

## 3. Censo 2021, viviendas en alquiler por sección censal (YA ESTÁ EN EL REPOSITORIO)

- Comprobado en data/raw/v11/ine_censo2021: tiene tablas por municipio (por ejemplo tpx 59518, 59523, 59529: régimen de tenencia por tamaño de municipio, provincia y municipios de más de 50.000 habitantes) y microdatos de muestra por municipio, pero NO por sección.
- Por sección censal está en data/raw/v3_orig/C2021_Indicadores.csv (fichero «Indicadores para secciones censales», Censo 2021, publicación del INE 30-6-2023, datos provisionales por reasignaciones de sección) y el diccionario data/raw/v3_orig/indicadores_seccen_c2021.xlsx. Variables de tenencia: grupo T20 «Viviendas principales según régimen de tenencia (3 datos)», columnas t20_1 a t20_3 (propiedad, alquiler y otro régimen; verificar el orden exacto en el diccionario antes de usar) y t19 (principales y no principales). Endpoints: https://www.ine.es/censos2021/C2021_Indicadores.csv y https://www.ine.es/censos2021/indicadores_seccen_c2021.xlsx .
- Verificación: se volvió a descargar el 2026-10-19 en una carpeta temporal y el sha256 es idéntico al de v3_orig (CSV f1749637f2b14da34b80f845accd5d13468905e7bddc166aaf333855524391d8; xlsx 9b9905d8a2a914d41b6a51c3ee990d900edc0349584b13d71e94f0d8aeba4e92). Se borró la copia: no se duplica el fichero de 8 MB. Licencia: reutilización del INE con cita (la página del INE indica CC BY-SA 4.0 en el pie del sitio; texto de la condición no verificado literalmente, confirmar antes de redistribuir). Redistribuible: sí, con cita (la parte CC BY-SA, en caso de aplicar, obliga a compartir igual).
- Limitación ya registrada en docs/v3/fuentes_fallidas.md: el fichero de indicadores no desglosa viviendas vacías ni de uso esporádico.

## Fallidas y pendientes

| Elemento | Resultado |
|---|---|
| InsideAirbnb 2019 o 2020 | Archivado; requiere petición del autor (apartado 2) |
| InsideAirbnb, otras ciudades españolas | Solo están las 9 áreas listadas; no hay Palma separada (Mallorca) ni Canarias |
| Censo 2021 alquiler por sección | No hay que descargar nada: ya en data/raw/v3_orig |
