# V11-DATOS · Descargas manuales para el autor

Lo que no se puede descargar desde el entorno de trabajo, por uno de dos motivos:
- **servidor**: el organismo bloquea el acceso automatizado (403 por IP, Cloudflare, hCaptcha);
- **entorno**: el proxy de la sesión cierra el túnel.

Están ordenadas por utilidad para el canal demográfico. Para cada una se indica:
- qué es y para qué sirve;
- URL;
- pasos en el navegador;
- fichero esperado;
- carpeta en GitHub;
- prioridad.

**Cómo subirlo:**
1. En GitHub, rama `claude/housing-price-spain-econometric-95dhj3` → «Add file» → «Upload files».
2. Ruta exacta `data/manual/v11/<fuente>/` (escribir la ruta en el nombre del fichero crea la carpeta).
3. No renombrar las columnas.
4. `make datos_v11` lo detecta con `src/v11/incorporar_manual.py`:
   - valida los totales;
   - lo registra con origen «descarga manual del autor»;
   - `make base` lo incorpora.

## 1. OPI: extranjeros con certificado de registro o tarjeta de residencia en vigor por provincia y nacionalidad (IMPRESCINDIBLE)
- **Para qué.** Stock de residentes extranjeros documentados por provincia y país, desde 2002. Es el instrumento migratorio
  (cuotas iniciales por país × provincia) y distingue régimen general y de libre circulación (UE), que la ECP no da.
- **URL.** https://www.inclusion.gob.es/web/opi/estadisticas/catalogo/extranjeros_con_certificado
- **Pasos.**
  1. Entrar en «Residentes» o «Extranjeros con certificado de registro o tarjeta de residencia en vigor».
  2. Abrir «Series» o «Tablas» de cada fecha de referencia (31-12 de cada año; 30-6 desde 2018).
  3. Descargar los Excel de «por provincia y nacionalidad» (o «por comunidad autónoma, provincia y país de nacionalidad») y «por régimen».
  4. Si existe «Series históricas» en un único fichero, basta ese.
- **Fichero.** `opi_residentes_<AAAA>_<MM>.xlsx` (uno por fecha) o `opi_series.xlsx`.
- **Carpeta.** `data/manual/v11/opi_residentes/`
- **Validación.** Total nacional por fecha frente a la nota de prensa de la OPI (p. ej., 31-12-2024 y 30-6-2025).

## 2. Interior: protección internacional y protección temporal por provincia (IMPRESCINDIBLE para el shock de 2022)
- **Para qué.** Shock de llegada con fecha (Ucrania, marzo de 2022) por provincia; solicitudes de asilo por provincia y nacionalidad.
- **URL.** https://www.interior.gob.es/opencms/es/servicios-al-ciudadano/tramites-y-gestiones/oficina-de-asilo-y-refugio/datos-e-informacion-estadistica/
- **Pasos.**
  1. Entrar en «Datos e información estadística».
  2. Descargar «Avance mensual de datos de protección internacional» de cada mes (PDF o Excel) desde 2019.
  3. Descargar «Protección temporal: personas desplazadas desde Ucrania», con el desglose por provincia o comunidad, si existe.
  4. Descargar los anuarios «Asilo en cifras» (2008-2024; tablas por provincia de presentación y nacionalidad).
- **Fichero.** `asilo_avance_<AAAA>_<MM>.pdf|xlsx`, `proteccion_temporal_<AAAA>_<MM>.pdf|xlsx`, `asilo_en_cifras_<AAAA>.pdf`.
- **Carpeta.** `data/manual/v11/interior_asilo/`
- **Validación.** Totales nacionales mensuales frente a Eurostat `migr_asyappctzm` y `migr_asytpfm` (ya en data/raw/v11).
- **Nota.** Los PDF se registran pero no se incorporan a la base hasta extraer sus tablas (pdf-extractor del proyecto).

## 3. Generalitat Valenciana: afiliados por municipio de residencia y nacionalidad (ÚTIL)
- **Para qué.** Afiliación de extranjeros por municipio. El fichero de la Seguridad Social no distingue la nacionalidad a escala municipal.
- **URL.**
  - CKAN: https://dadesobertes.gva.es/dataset/estadistica-de-treballadors-afiliats-a-la-ss-per-lloc-de-residencia-segons-nacionalitat-i-sexe
  - Consulta: https://bdo.gva.es/bdo/res_optimo_static.php?cons=V0201_C2D0244&idioma=cas&form=csvcoma&nperiodo=20
- **Pasos.**
  1. Abrir la consulta CSV.
  2. Si limita a 20 periodos, cambiar `nperiodo` a un número mayor o descargar en varias tandas.
  3. Repetir con `V0018_C1D0015` (extranjeros según sexo).
- **Fichero.** `bdo_V0201_C2D0244.csv`, `bdo_V0018_C1D0015.csv`.
- **Carpeta.** `data/manual/v11/gva_bdo_afiliacion/`
- **Validación.** Suma de la provincia 46 frente a la afiliación por municipio de residencia de la Seguridad Social del mismo trimestre.

## 4. Barcelona: cortes trimestrales del registro de viviendas de uso turístico, 2018T2-2026T3 (ÚTIL)
- **Para qué.** Altas y bajas de HUT por barrio con fecha. El registro vigente solo da el año de expediente.
- **URL.** https://opendata-ajuntament.barcelona.cat/data/es/dataset/habitatges-us-turistic
- **Pasos.**
  1. En «Recursos», descargar cada zip trimestral (`2018_2T_hut_comunicacio.csv.zip` … `2026_3T_hut_comunicacio_opendata.csv.zip`; 33 ficheros).
  2. Superar el hCaptcha una vez; las demás descargas suelen ir seguidas.
- **Fichero.** Los zip con su nombre original.
- **Carpeta.** `data/manual/v11/bcn_hut_trimestral/`
- **Validación.** Número de registros del último corte frente al recurso vigente de la API (datastore).
- **Nota.** 2026T3 se marca posterior_prereg.

## 5. Generalitat Valenciana: cortes antiguos del registro turístico vía web.archive.org (ÚTIL)
- **Para qué.** Cortes con altas y bajas anteriores a 2025 (el histórico abierto llega a 2025-01-26).
- **URL.** https://web.archive.org/web/*/dadesobertes.gva.es/dataset/*turisme* y https://web.archive.org/web/*/https://dadesobertes.gva.es/dataset/8a1c4fa3-4696-4b3b-8a1a-6bff038abf0c*
- **Pasos.**
  1. En el calendario de Wayback, abrir las instantáneas de los recursos CSV («Lista de Viviendas de uso turístico»).
  2. Descargar una por año (2018-2024) desde «/web/<fecha>id_/<url del csv>» (el sufijo `id_` da el fichero original).
- **Fichero.** `gva_vut_<AAAA-MM-DD>.csv`.
- **Carpeta.** `data/manual/v11/gva_vut_wayback/`
- **Validación.** Recuento de registros en ALTA frente a las notas de Turisme CV de esas fechas.

## 6. Catastro: valores de referencia por municipio (ÚTIL; probablemente requiere solicitud)
- **Para qué.** Nivel de precios administrativo por municipio desde 2022.
- **URL.**
  - https://www.catastro.hacienda.gob.es/es-ES/estadisticas.html (no tiene estadística de valores de referencia);
  - https://www.sedecatastro.gob.es/ → «Valor de referencia» (consulta individual).
- **Pasos.**
  1. Comprobar en «Estadísticas → Otras estadísticas» si aparece una estadística de valores de referencia.
  2. Si no aparece, presentar la solicitud 2 de docs/v11/solicitudes.md.
- **Fichero.** `valores_referencia_<AAAA>.xlsx`.
- **Carpeta.** `data/manual/v11/catastro_valores_referencia/`
- **Validación.** Número de inmuebles por municipio frente a la estadística catastral URBANA del mismo año.

## 7. Universidades: matrícula y residencias por universidad (OPCIONAL)
- **URL.**
  - Ministerio (SIIU/EDUCAbase): https://estadisticas.universidades.gob.es/ → «Estudiantes» → «Matriculados por universidad»;
  - UPV: https://www.upv.es (sección «La UPV en cifras»);
  - UV: https://www.uv.es/sap/docs/reculls/ («Recull de dades estadístiques», PDF por curso).
- **Pasos.**
  1. Descargar en CSV o Excel la matrícula de grado y máster por universidad y curso (2010/11 en adelante).
  2. Descargar las plazas en residencias o colegios mayores, si existen.
- **Fichero.** `siiu_matricula_universidad.csv`, `upv_cifras_<curso>.xlsx`.
- **Carpeta.** `data/manual/v11/universidades/`
- **Validación.** Total UV 2024/25 = 51.697 (tabla del SAP ya descargada).

## 8. GTFS de Metrovalencia (FGV) (OPCIONAL)
- **URL.**
  - https://www.fgv.es (Datos abiertos / Open data);
  - Punto de Acceso Nacional: https://nap.transportes.gob.es (requiere registro).
- **Pasos.** Descargar el zip GTFS vigente (y versiones anteriores si están).
- **Fichero.** `metrovalencia_gtfs_<AAAA-MM-DD>.zip`.
- **Carpeta.** `data/manual/v11/fgv_gtfs/`
- **Validación.** Que contenga `stops.txt`, `routes.txt` y `trips.txt`.

## Orden recomendado
1, 2 (instrumento y shock migratorio), 3 (afiliación por nacionalidad), 4 y 5 (turismo con fechas), 6, 7 y 8.
