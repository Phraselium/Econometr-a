Análisis a posteriori (V17). Fuentes descargadas para la auditoría.

Familia «credito», V17 fase 1. Fecha de descarga: 2026-10-19. Manifiesto con endpoint, edición, licencia y sha256: data/raw/v17/credito/_manifest.csv. Todo se descargó con peticiones únicas a ficheros que el organismo ofrece (robots.txt de bde.es y registradores.org sin prohibición aplicable; pausas de 5 s). Nada transformado.

## 1. Descargado: Banco de España (redistribuible con atribución)

Licencia (todos los ficheros BdE): «Términos de uso de la información estadística» https://www.bde.es/wbe/es/estadisticas/recursos/terminos/terminos-de-uso.html. Texto relevante: «La reutilización de la información estadística está permitida bajo las siguientes condiciones: 1. Integridad de la información: no se podrá alterar el contenido de la información ni sus metadatos [...] 2. Citación de la fuente: [...] Fuente: Sitio web del Banco de España (www.bde.es) / Fuente: Elaboración propia con datos extraídos del sitio web del Banco de España (www.bde.es) 3. Fecha de actualización [...] 6. Neutralidad institucional: no se podrá indicar, insinuar o sugerir que el Banco de España participa, patrocina o apoya la reutilización». Redistribuible: sí, con esas condiciones. Codificación original ISO-8859-1.

### bde_si_1_5.csv (sha256 f8106059...cdf0bef)
- Endpoint: https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/si_1_5.csv. Edición: Síntesis de indicadores del mercado inmobiliario, last-modified 2026-10-16; 93 series, mensual/trimestral/anual, datos hasta SEP 2026. Cobertura: España (más Madrid, Barcelona y costa en algunas series).
- Variables útiles para la auditoría (índice de columna base 0 del fichero; alias en la fila 2):
  - col 38, RPV (relación préstamo-valor) de transacción, %, trimestral, 2004T1-2026T2 (65,3 a 63,7).
  - col 39, porcentaje de préstamos con RPV > 80 %, trimestral, 2004T1-2026T2 (15,7 a 9,6).
  - col 37, plazo medio de las hipotecas, meses, trimestral, 2004T2-2026T2.
  - col 43, precio de la vivienda / renta bruta por hogar, años, trimestral, 1987T1-2026T2 (2,90 a 8,36).
  - col 44, esfuerzo teórico anual sin deducciones, %, trimestral, 1987T1-2026T2 (42,27 a 38,01).
  - col 62 y 63, rentabilidad anual de la vivienda y rentabilidad bruta por alquiler (12 meses), %, trimestral, 1987-2026.
  - col 58, importe de nuevos préstamos inmobiliarios de entidades de depósito, miles de euros, mensual, 2017-03 a 2026-07.
  - col 57, número de créditos con garantía hipotecaria, mensual, 2018-05 a 2026-07.
  - col 47-49, riqueza inmobiliaria de los hogares y su ratio sobre renta; col 55-56, crédito a hogares para vivienda (tasa y saldo/PIB).
  - col 24-27 y 31-33, compraventas ante notario (origen: Centro de Información del Notariado, mensual 2007-01 a 2026-04; trimestral por tipo y por zona) y compraventas totales (origen INE/registros, 2004-2026-07).
- Notas: las series de origen tercero (notariado) se redistribuyen por el BdE; su licencia propia es la del Notariado (apartado 3). El RPV es el de las tasaciones/escrituras que el BdE recoge como «accesibilidad» y es una medida de transacción, no el LTV al inicio de cada hipoteca (diferencia que el documento de trabajo del BdE «Beyond the LTV ratio», https://repositorio.bde.es/handle/123456789/9810, discute; NO VERIFICADO el contenido, solo resumen).

### bde_be1911.csv (sha256 86f6270d...ad1acd2)
- Endpoint: https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/be1911.csv. Boletín Estadístico, capítulo 19, cuadro 11. Importes totales estimados de nuevas operaciones de crédito, hogares e ISFLSH, millones de euros, mensual, ENE 2003 a AGO 2026, España. Col 1 vivienda; col 5 consumo; col 8 otros fines; resto por plazos de fijación o importes.

### bde_be1903.csv (sha256 0066548167bbad45d3a41cf66c928052a8b0864f53cbeec95b0932ecce0de235) y bde_be1906.csv (sha256 7c5d94b03c70ceb2a849fc8795f5b4f51d1fe051e79b614593d55e005aa58aa5)
- Endpoints: .../csv/be1903.csv (TEDR, tipo de interés efectivo definido restrictivamente) y .../csv/be1906.csv (TAE). Nuevas operaciones de crédito a la vivienda de hogares, %, mensual, ENE 2003 a AGO 2026, España. Duplican en parte data/raw/bde_tipos_hipotecas_nuevas.csv (be1906, edición de 2026-10-10); se guardan como edición de 2026-10-19.

## 2. Descargado: Colegio de Registradores (NO redistribuible)

Licencia: Aviso legal de CORPME, https://www.registradores.org/aviso-legal: «queda prohibido modificar, copiar, reproducir, comunicar públicamente, poner a disposición, transformar o distribuir [...] la totalidad o parte de los contenidos [...] para propósitos públicos o comerciales, si no se cuenta con autorización previa, expresa y por escrito de CORPME». Redistribuible: **no**. Los PDF están en data/raw/v17/credito/_terceros/registradores/ (carpeta ignorada por git, solo quedan los sha256 en el manifiesto). Descarga de las publicaciones que ofrece el propio portal (https://www.registradores.org/actualidad/portal-estadistico-registral/estadisticas-de-propiedad); no hay Excel ni API. Para citar cifras en entregables, solo agregados con atribución y cita corta; consultar al autor si se quiere reproducir tablas.
- ERI_4T_2025.pdf (122 págs.; publicación trimestral n.º 87, febrero 2026): sha256 1de45e66a45e87f370548f497dc233143ed4adefdf35ecaaafe8d8f32b201783. Secciones: nacionalidad de las compras de vivienda (cap. 6), número de hipotecas sobre vivienda (cap. 11), importe de nuevo crédito por compraventa y por m² (cap. 13-14), tipos y plazos, cuota/coste salarial, certificaciones hipotecarias con desglose personas físicas/jurídicas y extranjeros (cap. 19). Cobertura: España, CCAA y provincias, trimestral, con series históricas.
- ERI_2T_2026.pdf (122 págs.): sha256 e01b314f7a789a64406d3f6568f5279c293444c48b7c2306537bfdb14e48d0f0. Edición más reciente disponible.
- ERI_Anuario_2025.pdf (182 págs.): sha256 c618eb8625acf4668f4ee344f056defa006d9dc167d3b22e916e91abb4ce84a7. Anual 2025.
- Limitaciones: Registradores publica compras de vivienda por nacionalidad del comprador y personas jurídicas en las hipotecas y certificaciones; no publica una serie de compras al contado. Las compras sin hipoteca solo se pueden aproximar por diferencia (compraventas registradas menos hipotecas sobre vivienda, o con el INE H ya en el repositorio): es aproximación, no dato directo, y debe marcarse así.
- Pendiente de extracción (otra fase): las tablas están en PDF; extraer con pdftotext y validar a mano.

## 3. Fallidas / requiere al autor

### 3a. Notariado (Portal Estadístico del Notariado, CIEN y penotariado.com): requiere al autor
- Endpoints: https://penotariado.com (portal interactivo; a 2026-10-19 devuelve «El acceso al portal no está disponible por tareas de mantenimiento») y https://www.notariado.org/liferay/web/cien/estadisticas-principales/hipotecas (gráficos interactivos Liferay, sin fichero de datos).
- Motivo: no hay API ni descarga de ficheros; los datos se consultan mediante visores. robots.txt de notariado.org (https://www.notariado.org/robots.txt) declara «Crawl-delay: 5», «Content-Signal: ai-train=no, ai-input=no» y bloquea las rutas de los portlets (/*p_p_id*, /*p_p_lifecycle*, /*q=*), que son las que sirven los datos. Aviso legal (https://www.notariado.org/liferay/web/cien/aviso-legal): sin licencia ni cesión de derechos de reproducción o comunicación pública «con fines comerciales» sin autorización expresa del CGN. Extraer los gráficos automáticamente sería scraping contra esas condiciones; no se ha hecho.
- Paso exacto para el autor: (1) cuando el portal vuelva a estar operativo, entrar en https://penotariado.com, módulo Inmobiliario, y exportar manualmente (si ofrece botón de descarga) compraventa de vivienda por forma de pago (con/sin préstamo hipotecario), por tipo de comprador (persona física, jurídica) y por nacionalidad, nacional/CCAA/provincia, mensual o trimestral; (2) si no hay exportación, escribir al Consejo General del Notariado (Centro de Información Estadística) solicitando autorización de reutilización de esos agregados con atribución. Hasta entonces, la única cifra notarial en el repositorio son las series de compraventas ante notario que el BdE redistribuye en bde_si_1_5.csv (col 24-30), sin desglose por pago ni comprador.
- Cifras de prensa citadas por buscadores (p. ej. 43 % con hipoteca en junio de 2024; 53 % en abril): NO se usan; son prensa y no se han contrastado con el original.

### 3b. Banco de España: LTI de las nuevas hipotecas y desequilibrio/sobrevaloración del precio
- Endpoint buscado: tablas del Boletín Estadístico (cap. 19, cap. 4) y página de estadísticas del BdE; Síntesis del mercado inmobiliario (si_1_5). Fecha: 2026-10-19.
- LTI (préstamo/renta del acreditado): no existe serie descargable en el Boletín Estadístico ni en la Síntesis. El BdE lo analiza en el Informe de Estabilidad Financiera (otoño 2025: https://www.bde.es/wbe/es/publicaciones/estabilidad-financiera-politica-macroprudencial/informe-estabilidad-financiera/informe-de-estabilidad-financiera-otono-2025.html, recuadros 2.1, 4.1 y 6.1) solo en gráficos PDF, sin fichero de datos. No descargado. Opciones para el autor: pedir al BdE (Dirección General de Estabilidad Financiera) los datos de los gráficos, o transcribir cifras del PDF citando página (leer el recuadro, no el resumen).
- Capítulo 4 del Boletín Estadístico (be0401-be0408) es el balance de entidades de crédito: sin LTV, LTI ni esfuerzo; no se descarga.
- Desequilibrio/sobrevaloración: el BdE no publica una serie descargable. Sustitutos oficiales ya descargados: precio/renta (col 43) y esfuerzo teórico (col 44) y rentabilidad por alquiler (col 63) de bde_si_1_5.csv. La estimación de sobrevaloración por modelo aparece solo en informes (Informe Anual, IEF, documentos ocasionales); NO VERIFICADA su cifra aquí. Pendiente de lector-literatura.
- Esfuerzo financiero de los hogares (carga de deuda/renta): el recuadro 2.1 del IEF otoño 2025 (https://www.bde.es/f/webbe/Secciones/Publicaciones/InformesBoletinesRevistas/InformesEstabilidadFinancera/25/IEF_2025_2_Rec2_1.pdf) lo trata, sin datos; no descargado el PDF en esta fase.

### 3c. Compras al contado, personas jurídicas y no residentes: lo que falta
- Compras al contado y por persona jurídica en Notariado: ver 3a (requiere al autor).
- No residentes por nacionalidad: en Registradores (ERI, sección 6, tabla «Compraventas de vivienda registradas según nacionalidad del comprador»; extranjeros ≈ 13,8 % de las compras de 2025 según prensa, a verificar en el anuario). Por residencia, MIVAU ya está en data/raw/mivau_transacciones_residencia.csv (no repetido). INE H (hipotecas sobre vivienda) ya está en data/raw/ine_v2_hipotecas_prov.csv.
- Compras por personas jurídicas (no hipotecarias) en Registradores: no aparecen como serie propia; solo en hipotecas y certificaciones (ERI cap. 11 y 19).

## 4. Resumen de redistribución
| Fichero | Redistribuible |
|---|---|
| bde_si_1_5.csv, bde_be1911.csv, bde_be1903.csv, bde_be1906.csv | sí, con atribución e integridad (series de origen notarial dentro de si_1_5: dudoso) |
| _terceros/registradores/*.pdf | no |
