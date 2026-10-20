# Fuentes fallidas v6

Cada entrada: fuente, endpoint probado, edición, fecha de la prueba y error.


## M0 (datos, paneles, sellado, potencia)

- M0 no descargó nada: reutilizó data/raw, data/processed y las salidas v5/v5_1 versionadas. No hubo intento de acceso a endpoints.
- Sin dato por cobertura de la fuente (no fallo de acceso): Notariado fuera de Comunitat Valenciana; valor tasado provincial de Baleares, La Rioja, Madrid, Murcia, Navarra, Asturias, Cantabria, Ceuta y Melilla; VUT municipal (`ln_vut_viviendas_mun` vacía); emigración provincial (sin flujo neto); renta disponible provincial; jóvenes en casa de los padres provincial. Ver docs/v6/diccionario.md, sección 3.

## V8-F1 (descarga, 2026-10-13)

- Endpoint: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24077?nult=2000. Error: LIMITACIÓN PARCIAL: el WS devuelve 296 obs. mensuales (2001-12 a 2026-07) aunque la tabla se anuncia desde 1961; nult=5000 y date= no amplían la serie (probado 2026-10-13). Alternativa: IPCA BCE (data/raw/ecb_hicp_es.csv, desde 1996) como serie larga; IPC 1961+ por descarga manual.
- Endpoint: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10822?nult=5000. Error: LIMITACIÓN PARCIAL: FRONTUR en 10822, 10823, 75719, 75720 y 23984 empieza en 2015-09 (serie actual); sin FRONTUR 1999-2015 por WS. Alternativa: Sin alternativa automatizada; edición antigua de la operación 330 no localizada.
- Endpoint: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/6067?nult=2000. Error: LIMITACIÓN PARCIAL: 6067 (retrospectivas) termina en 2007-Q3; la nacional actual (79662, 'Total Nacional') empieza en 2008-Q1; sin empalme aplicado. Alternativa: Usar ambas tablas con la discontinuidad marcada en el nombre; empalme solo validado.

## V11-DATOS, tercera pasada (2026-10-16)

- Endpoint: https://datos.gob.es/apidata/catalog/dataset (OPI: residentes con certificado o tarjeta; personas ucranianas con documentación). Error: 403 Incapsula, un intento (verificado 2026-10-16). Alternativa: réplica de la Comunidad de Madrid (provincia 28) y sustituto ECP/censo/padrón.
- Endpoint: https://www.valencia.es/estadistica/Padron/2014/Padron2014.pdf (y Cast/Val). Error: 404, edición 2014 no publicada (verificado 2026-10-16). Alternativa: Pob_estrangera_2014.pdf y padrón INE.
- Endpoint: https://www.valencia.es/estadistica/Padron/AltasBajas/<A>/AltasBajasPadron<A>.pdf, 2017-2026. Error: 404 (verificado 2026-10-16). Alternativa: EVR/EMCR del INE por municipio.

## V15, fase 2 (2026-10-17)

- **Scimago, ranking anual.** Endpoints: https://www.scimagojr.com/journalrank.php?out=xls&year=2024 y https://www.scimagojr.com/journalsearch.php?q=<ISSN>.
  - Error: 403, desafío de Cloudflare («Just a moment...») con dos intentos, también con cabecera de navegador (verificado 2026-10-17).
  - Consecuencia: docs/v15/scimago_cuartiles.csv no se puede generar de forma automática, y las referencias quedan «cuartil no verificado».
  - Alternativa: descarga manual del autor (tareas_autor.md).

## V18, fase 4, E3 (2026-10-20)

- **INE, Censos de Población y Viviendas 2001, resultados definitivos (nacionalidad por provincia).** Endpoint: https://www.ine.es/censo/es/consulta.jsp (aplicación de tablas a medida; flujo `seleccion_ambito.jsp`, `seleccion_colectivo.jsp`, `estructura.jsp?k=MDDB.COLECTIVO_P3`). Error: la aplicación contesta «En estos momentos el servicio se encuentra saturado» a toda consulta, también la más pequeña (Todas las personas × Provincia), en cinco intentos espaciados (verificado 2026-10-20). INEbase solo publica las cifras de población del Censo de 2001 (/t20/e242/p03/a2001/), sin nacionalidad.
  - Alternativa usada: Eurostat cens_01rsctz (mismo Censo de 2001, población por nacionalidad y NUTS 3), descargada el 2026-10-20 (docs/v18/desviaciones_e3_e5_e9.md, D-E359-1 y D-E359-3).
- **Seguridad Social, afiliación provincial por sección de la CNAE de 2001.** Sin endpoint publicado antes de 2011-12 (ficheros STAT/MUNCNAE<MMAA>.xlsx desde 2011-12). Alternativa usada para las cuotas sectoriales de 2001 del Bartik de E5: Eurostat nama_10r_3empers (empleo por NUTS 3 y rama A*6, datos del INE), D-E359-2.
