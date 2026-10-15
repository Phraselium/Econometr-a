# V11-DATOS · Solicitudes de acceso a la información (redactadas; NO enviadas: las presenta el autor)

Base legal: Ley 19/2013, de transparencia (y, en la Comunitat Valenciana, Ley 1/2022, de transparencia y buen
gobierno). Se actualizan las solicitudes de docs/v9/solicitudes_transparencia.md y se añaden las que nacen de los
fallos de esta tarea (docs/v11/fuentes_fallidas.md). En todas:
- se piden datos agregados, sin datos personales y con secreto estadístico (celdas de menos de 5 → «<5»);
- formato CSV o XLSX con códigos INE de municipio y de sección censal;
- se pide además la nota metodológica (definiciones, fecha de extracción).

## 1. Fianzas de arrendamiento por sección censal o barrio, 2010-2026
- **Destinatario.** Generalitat Valenciana, Conselleria competente en vivienda; registro de fianzas (EIGE / Agència Valenciana de l'Habitatge).
- **Petición.**
  - Número de fianzas depositadas y renta mensual declarada (media, mediana, p25, p75).
  - Por sección censal, o si no por barrio de València y código postal en el resto, y por mes de inicio del contrato, de 2010 a 2026.
  - Separar vivienda habitual, temporada y habitaciones, si consta.
  - Superficie y número de habitaciones si se registran.
- **Uso.** Renta y volumen de contratos por zona con fecha; sustituye las aproximaciones de dos cortes del registro de VUT.

## 2. Titularidad agregada del Catastro
- **Destinatario.** Dirección General del Catastro (Ministerio de Hacienda).
- **Petición.**
  - Viviendas (uso residencial) por municipio, y por sección censal en capitales y municipios de más de 50.000 habitantes.
  - Desglosadas por tipo de titular (persona física, jurídica, administración pública) y por tramo de inmuebles residenciales del titular en España (1, 2-4, 5-9, 10-24, 25 o más).
  - Cortes a 1 de enero de 2015 a 2026.
- **Petición complementaria (nueva en V11).** Estadística de **valores de referencia** por municipio y uso desde 2022 (media, mediana y número de inmuebles), que no aparece como fichero descargable en la sede (3 intentos el 2026-10-15).
- **Uso.** Concentración de la propiedad y nivel de precios administrativo comparable entre municipios.

## 3. Registro de Turismo de la Comunitat Valenciana con fechas de alta y baja
- **Destinatario.** Generalitat Valenciana, Turisme Comunitat Valenciana (Registre de Turisme).
- **Petición.**
  - Viviendas de uso turístico: altas y bajas por municipio (código INE), código postal y mes, de 2010 a la fecha de extracción, sin datos de titulares.
  - Motivo de la baja si consta (voluntaria, de oficio, por falta de referencia catastral).
  - Número de plazas.
- **Motivo.** El conjunto abierto «histórico» no se ha actualizado desde el 2025-01-26 (el recurso con fecha 2025-11-12 es una re-subida con el mismo contenido). El conjunto diario no trae bajas.

## 4. Bono Alquiler Joven: beneficiarios por provincia y edad
- **Destinatario.** Ministerio de Vivienda y Agenda Urbana y la Conselleria competente de cada comunidad autónoma.
- **Petición.**
  - Solicitudes, concesiones e importe concedido por provincia, convocatoria (2022-2026) y edad del beneficiario en años (de 18 a 35).
  - Si es posible, en meses respecto al límite de 35.
  - Fecha de resolución.
- **Uso.** Análisis por edad del programa; sin edad exacta no hay comparación en torno al límite.

## 5. Protección temporal, protección internacional y arraigo por municipio o provincia
- **Destinatarios.**
  - Ministerio del Interior, Oficina de Asilo y Refugio: protección internacional y protección temporal.
  - Ministerio de Inclusión, Seguridad Social y Migraciones, Secretaría de Estado de Migraciones: autorizaciones por arraigo y certificados de registro o tarjetas en vigor.
- **Peticiones.**
  - (a) Protección temporal concedida a personas desplazadas de Ucrania por provincia y municipio de residencia y mes, desde marzo de 2022.
  - (b) Solicitudes y resoluciones de protección internacional por provincia, nacionalidad y mes, desde 2008.
  - (c) Autorizaciones de residencia por arraigo (social, laboral, familiar, para la formación, sociolaboral, socioformativa, de segunda oportunidad) por provincia, municipio si es posible, nacionalidad y mes, desde 2005; también las concedidas en procesos extraordinarios de regularización.
  - (d) Extranjeros con certificado de registro o tarjeta de residencia en vigor por provincia, municipio, nacionalidad y régimen, series completas desde 2002.
- **Motivo.**
  - Las webs de la OPI (inclusion.gob.es) y de Interior rechazan el acceso automatizado (HTTP 403 o reto de Cloudflare).
  - Eurostat solo da el nivel nacional (data/raw/v11/eurostat_asilo).
  - El nivel municipal no se publica.

## 6. Licencias urbanísticas y de cambio de uso por barrio (Ajuntament de València)
- **Destinatario.** Ajuntament de València, Servei de Llicències Urbanístiques / Oficina d'Estadística.
- **Petición.** Licencias de obra mayor (nueva planta, rehabilitación) y declaraciones responsables o licencias de cambio de uso (local a vivienda, vivienda a uso turístico), por barrio y mes, 2010-2026, con número de viviendas afectadas.
- **Motivo.** No figuran en el portal de datos abiertos (opendata.vlci.valencia.es, consulta 2026-10-15).

## 7. Padrón de València por barrio, edad y nacionalidad, todos los años
- **Destinatario.** Ajuntament de València, Oficina d'Estadística.
- **Petición.**
  - Población empadronada a 1 de enero por barrio, grupo quinquenal de edad, sexo y nacionalidad (país), de 1996 a 2026.
  - Altas y bajas del padrón por barrio, causa (nacimiento, defunción, cambio de domicilio interno, procedencia o destino de otro municipio o del extranjero) y nacionalidad.
- **Motivo.** El portal abierto no lo publica. La serie del IVE por distrito y sección (2005-2022) ya está en la base.
