# V9-PREP · Bloque 1 · Fuentes de datos (València ciudad, Comunitat Valenciana, España; foco 2020-2026)

Fecha de comprobación: 2026-10-14. Método: WebFetch/WebSearch (no hay curl en este entorno); «RESPONDE» = la URL devolvió contenido; «403» = bloqueada desde aquí. Todos los datos del proyecto proceden de data/raw (solo lectura). Fuente de verdad: `fuentes.csv` (38 filas, 17 columnas).

## Resumen

- 38 fuentes. Sin ninguna copia en el proyecto (columna en_proyecto = no): F07, F08, F09, F10, F12, F13, F15, F16, F17, F21, F24, F36 (F11, F14, F22, F23, F25, F26, F30, F34 son parcial).
- Respuesta a «¿publican fianzas?»: Galicia no (solo metodología del IGE, F08); Andalucía no, y la obligación de depositar se habría suprimido el 24-01-2026 (F09, a confirmar en BOJA); Baleares no (F10); Madrid no (F11, solo alquiler medio por CP). Sí publican: Cataluña (Incasòl, F06), Comunitat Valenciana (F05), Euskadi (EMAL, F07, informes y no datos abiertos).
- Discrepancias con docs: (1) Incasòl: metadatos dicen «Ver términos de uso», docs/v5/licencias_datos.md dice CC BY 4.0. (2) EFF microdatos: BdE anuncia disponibilidad para uso científico desde 2025-02-05; docs/v3/fuentes_fallidas.md dice no descargables. (3) INE: el pie dice CC BY-SA 4.0 pero el icono enlaza CC BY 4.0 (F01-F03, F22).
- Prioridad alta: F01, F02, F03, F04, F05, F12, F18, F19, F20, F31, F32, F33.

## Fichas

**F01 Censo Anual de Población (INE).** Sección censal, 1 de enero, desde 2021/2022; últimos datos 29-04-2026. Nacionalidad por sección: no confirmada. En proyecto: parcial (servergis). Hueco: stock de extranjeros por sección.

**F02 VUT experimental (INE).** Sección, semestral (mayo/noviembre desde 2024). En proyecto: sí (v3 sección, hasta 2026-05). Ruptura de referencia en 2024.

**F03 IPVA (INE).** Municipios y capitales con distritos, no secciones; IPVA 2024 publicado 11-05-2026: España +3,5% (nuevos +8,8%, existentes +2,8%), CV +5,0%, València +5,9%. En proyecto: parcial (hasta 2024); desglose nuevos/existentes en tablas sin confirmar.

**F04 SERPAVI (MIVAU).** Sección, distrito, municipio; 2011-2024 en el proyecto; el País Vasco se incorpora por provincias (Gipuzkoa sep-2025; Álava y Bizkaia mar-2026, notas de prensa). La web del Ministerio da 403 aquí.

**F05 Fianzas GVA.** CKAN responde; siete conjuntos 2020-2026, cc-by, CSV/JSON/XLSX/XML. En proyecto: sí (v5).

**F06 Incasòl.** Socrata responde; municipio (INE), 2007-2026; licencia en metadatos: términos de uso (discrepancia).

**F07 EMAL Euskadi.** Informe anual 2025 leído (pp. 1-6): 91.440 fianzas vigentes, 86.522 de vivienda colectiva habitual libre, renta media 801,4 EUR/mes; barrios de capitales; sin datos abiertos. No en proyecto.

**F08-F11 Fianzas de Galicia, Andalucía, Baleares y Madrid.** Ninguna publica serie localizada (ver resumen). URLs en el CSV.

**F12-F13 Eurostat plataformas.** `tour_ce_oan3` (NUTS 3 anual 2018-2025; ES523 total 4.503.992 noches en 2018, 1.862.635 en 2020, 8.128.113 en 2025) y `tour_ce_omn12` (NUTS 2 mensual, ES52). Sin nivel LAU. Ruptura 2025 (3 plataformas).

**F14 Inside Airbnb.** Valencia, edición del 20-09-2026; CC BY 4.0. En proyecto: parcial (agregados, C4).

**F15 OHsu.** calab.es responde; el visor de alquiler no se ha podido confirmar. **F16** Índice de precios de referencia GVA: solo prensa.

**F17 Cátedra UPV.** Informes trimestrales 3T-2019 a 3T-2026; sin descarga de datos ni licencia.

**F18 Datos abiertos Ajuntament de València.** CKAN responde (cc-by); «Vivienda libre (precio m2)» modificado 2026-10-13, la copia del proyecto llega a 2022-04.

**F19 Oficina d'Estadística de València.** Por sección, barrio y distrito; tablas concretas sin localizar.

**F20 Registro de Turismo CV.** `tur-gestur-vt` diario, cc-by; en proyecto: corte 2026-10-09. Retirada de 886 + 10.601 viviendas en 2025 según prensa (ruptura).

**F21 Afiliación SS por municipio.** Página oficial: solo totales nacionales. Réplica municipal solo por Comunidad de Madrid (CC BY 4.0). Hueco abierto.

**F22 Teléfonos móviles (INE).** CCAA, provincia, municipio; el receptor termina en dic-2025 (integrado en FRONTUR, según el aviso citado en la búsqueda). Baja.

**F23 Catastro INSPIRE.** ATOM por municipio, WFS, dos actualizaciones al año; términos de la licencia no leídos.

**F24 SIU.** URL no verificada (403). Baja.

**F25 Notariado.** penotariado.com responde; municipio y CP; sin licencia; mantener «privada, no redistribuible».

**F26 Registradores ERI.** 2T 2026 (nº 89) existe; PDF escaneado, sin cifra leída.

**F27-F28 Hipotecas y ETDP (INE).** En proyecto.

**F29 Microdatos EPA/ECV (INE).** Ficheros anonimizados con cita y acceso seguro por solicitud; operaciones concretas sin confirmar.

**F30 EFF 2022 microdatos (BdE).** Disponibles para uso científico (anuncio 05-02-2025); procedimiento no leído.

**F31 Proyección de Hogares 2026-2041 (INE).** CV: 2.215.478 (2026) a 2.569.459 (2041), +16,0%; España +11,1%. Ya en proyecto (tabla 54562, 2026-06-17).

**F32 Padrón por nacionalidad.** En proyecto hasta 2022 a nivel de distrito/sección; hueco 2023-2026.

**F33 ADRH (INE).** Edición 2023 publicada 21-10-2025; en proyecto 2019-2023; edición 2024 pendiente.

**F34 AEAT por CP.** Solo CP con más de 900 declaraciones. Baja.

**F35 Censo 2021 viviendas vacías.** 3.837.328 vacías y 2.514.511 de uso esporádico (INE). En proyecto.

**F36 Idealista y Fotocasa.** Privadas, no redistribuibles; solo hipótesis.

**F37 BdE.** Sin tabla oficial de indicadores localizada; DO 2432 sobre alquiler. **F38 MIVAU Observatorio.** Cifras del boletín 57 solo de prensa.

## Limitaciones

No se ha podido abrir mivau.gob.es (403) ni leer el PDF de Registradores (imagen). Las licencias marcadas «no consta» no se han leído en el aviso legal original. Ninguna cifra de prensa se ha usado como dato.
