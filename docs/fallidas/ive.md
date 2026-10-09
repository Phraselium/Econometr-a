# Fallos IVE / PEGV (pegv.gva.es, ive.es) - 2026-10-09

Registro de intentos fallidos del descargador para el Institut Valencià d'Estadística (IVE) y el
Portal Estadístic de la Generalitat (PEGV). No se ha intentado saltar el proxy ni desactivar TLS.
`docs/fuentes_fallidas.md` no se ha modificado.

## 1. Descargas directas (paso 2 de la escalera), cabeceras de navegador (Chrome, Accept, es-ES)

| URL probada | HTTP | Resultado / diagnóstico |
|---|---|---|
| https://pegv.gva.es/es/ | 000 | Túnel cortado (reset) |
| https://www.pegv.gva.es/es/ | 000 | Túnel cortado |
| https://pegv.gva.es/va/ | 000 | Túnel cortado |
| https://pegv.gva.es/ (2 intentos) | 000 | Túnel cortado |
| https://pegv.gva.es/es/estadisticas/ | 000 | Túnel cortado |
| https://www.ive.es/ (2 intentos) | 000 | Túnel cortado |
| https://www.ive.es/es/ | 000 | Túnel cortado |
| http://www.pegv.gva.es/ca/padro-municipal-continu-explotacio-estadistica.-resultats-per-a-la-comunitat-valenciana (URL de la ficha CKAN del padrón) | 503 | "upstream connect error ... connection timeout" (respuesta del relé del proxy, no del servidor de la GVA) |

Estado del proxy (`$HTTPS_PROXY/__agentproxy/status`): sin 403/407 (no es bloqueo de política). Los
fallos figuran como `recentRelayFailures` de tipo `ws_closed_mid_exchange` en `pegv.gva.es:443`
(2026-10-09T18:41:36Z) y `www.ive.es:443` (2026-10-09T18:44:01Z), con cortes tras 8-13 s. Según
`/root/.ccr/README.md` es un fallo de túnel, no un rechazo del destino. Se reintenta más tarde.

## 2. Búsqueda de series IVE en el portal de datos abiertos (paso 1)

Datasets CKAN de la Generalitat (dadesobertes.gva.es) usados: ver `src/fetch_gva.py`.

No encontrado en CKAN (búsquedas: `compravenda`, `compraventa`, `preu habitatge`, `precio vivienda`,
`habitatge`, `vivienda`, `licencias`, `visados`): **compraventas de vivienda por municipio** y
**precios de vivienda del IVE**. Sin datasets de visados ni licencias de la GVA en el catálogo.
Alternativa para precios: `data/raw/vlc_precio_vivienda_libre.csv` (Ajuntament de València, ya descargado
por `src/fetch_valencia.py`, solo 2021T2-2022T2).

## 3. Lo que sí se ha obtenido (sin PDF)

No ha sido necesario extraer PDF. Todo lo descargado es CSV o ZIP de datos.
- Registro de viviendas de uso turístico (Registre de Turisme CV): CSV histórico con altas y bajas
  (2025) y lista vigente (2026-10-09). Salida: `data/raw/gva_vut_municipio.csv`.
- Padrón municipal continuo, explotación por distritos y secciones (IVE): ZIP por año, 2005-2022,
  castellano. Totales y procedencia por municipio. Salida: `data/raw/gva_padron_extranjeros_municipio.csv`.
  Los grupos de procedencia solo se exportan para 2022 (los nombres de grupos de los otros años no
  coinciden con el diseño de 2022). Esto corrige la nota de `docs/fallidas/padron_valencia.md`: el
  desglose por nacionalidad sí existe a nivel de sección, en estos ZIP del IVE.

## 4. Incidencias de descarga (no son fallos de fuente)

- `tur-gestur-vt` CSV: un intento dio `Recv failure: Connection reset by peer`; el reintento con
  backoff funcionó (HTTP 200, 15 MB).
- `padro-...-2005` a `-2021` y `-2022` descargados con `download()`: sin errores de red en la
  ejecución final.
