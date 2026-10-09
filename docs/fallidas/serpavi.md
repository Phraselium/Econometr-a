# SERPAVI: intentos fallidos y notas

Resultado: paso 1 de la escalera (formato abierto, XLSX) OK. No hizo falta PDF/OCR.

| URL | Paso | Resultado | Alternativa |
|---|---|---|---|
| https://www.mivau.gob.es/vivienda/alquila-bien-es-tu-derecho/serpavi (y /preguntas-frecuentes, home) | 1 | HTTP 403 "Pagina web bloqueada" (WAF del sitio; tambien con User-Agent de navegador y via WebFetch) | El CDN `cdn.mivau.gob.es` si responde; URL del XLSX tomada del script publico CGTCastello/observatori-habitatge (`scripts/fetch_serpavi.py`) |
| https://apps.fomento.gob.es/, https://www.transportes.gob.es/ | 1 | 403 | No necesarios |
| https://datos.gob.es/apidata/catalog/dataset?title=alquiler | 1 | 403 (Incapsula) | Solo hay una solicitud de datos (no dataset) en datos.gob.es |
| https://serpavi.mivau.gob.es/ (visor) | 1 | Responde, pero es una SPA que genera un informe PDF por direccion/punto (POST con reCAPTCHA y cabecera X-Private-Data). No expone endpoint de datos masivos. No se intento eludir el captcha | Descarga masiva XLSX |
| ArcGIS FeatureServer Esri Espana (item cdda9092a8d74bcdb76c32b3904d84d3, services1.arcgis.com/nCKYwcSONQTkPA4K/.../Sistema_Estatal_de_Referencia_del_Precio_del_Alquiler_de_Vivienda/FeatureServer) | 1 | Error 499 "Token Required for subscription content"; ademas solo trae 2022 por seccion censal | XLSX |
| web.archive.org | 1 | no accesible desde el proxy | n/a |

## Fuente usada
https://cdn.mivau.gob.es/portal-web-mivau/vivienda/serpavi/2026-03-09_bd_SERPAVI_2011-2024%20-%20DEFINITIVO%20WEB.xlsx
(71 MB; hojas CCAA, Provincias, Municipios, Distritos, Secciones censales). La URL cambia en cada publicacion.
Metodologia: https://cdn.mivau.gob.es/portal-web-mivau/vivienda/serpavi/2026-03-18_Metodologia_SERPAVI.pdf

## Limitaciones
- No hay fila "Espana": `serpavi_esp_agregado.csv` es un agregado propio (media de medianas CCAA VC ponderada por n de contratos), no oficial. La composicion cambia: Navarra desde 2021, Gipuzkoa 2022, Alava/Bizkaia 2024 (17, 18, 19 CCAA).
- Anual (2011-2024), mediana de contratos declarados en IRPF (stock de arrendamientos vigentes declarados, no solo contratos nuevos); sesgo de composicion (el 2019 sube mas que el IPVA: +11% vs +5%).
- Datos de municipios/secciones pequenos: minimo de 10 viviendas por territorio.
- El XLSX original (71 MB) esta en data/raw/pdf/originales/ (considerar .gitignore).
