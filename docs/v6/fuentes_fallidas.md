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
