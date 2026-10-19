Análisis a posteriori (V17). Fuentes descargadas para la auditoría.

Familia «oferta_capacidad», V17 fase 1. Fecha de descarga: 2026-10-19. Manifiesto con endpoint, edición, licencia y sha256: data/raw/v17/oferta_capacidad/_manifest.csv. Ficheros originales sin transformar (JSON de la API del INE tal como se devuelve; PDF del Banco de España). Todos pesan menos de 50 MB (total 24 MB). Ya existían y no se repiten: SIU (data/raw/mivau_v2_suelo.csv, data/raw/v16/oferta_suelo), visados, iniciadas y terminadas, costes Eurostat.

Nota de lectura de fechas del JSON del INE: el campo Fecha es la fecha de inicio del periodo en hora local expresada en UTC, es decir, aparece un día antes (Fecha 2007-12-31 = 2008T1; 2026-02-28 = marzo de 2026). Usar Anyo y FK_Periodo.

## 1. INE, ocupados en la construcción (EPA, rama F)

- Endpoint: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/<id>?nult=2000 (API oficial; 2 s de pausa entre peticiones).
- Tabla 65313 «Ocupados por rama de actividad, sexo y comunidad autónoma» (CNAE-2009): trimestral, 2008T1 a 2026T2, nacional y 19 CCAA y ciudades autónomas; edición con última modificación del INE 2026-07-28. Contiene la rama «Construcción» (20 series de ocupados ambos sexos: nacional más 19 territorios; valor absoluto en miles). sha256 en el manifiesto. Tabla 65123: lo mismo a nivel nacional por sexo y rama (valor absoluto y porcentajes).
- Tablas 79328 y 79281: la misma EPA con CNAE-2025, solo 2025T4 a 2026T2 (el INE cambió de clasificación en 2026). Hay ruptura de clasificación respecto a 65313: no concatenar sin enlace; para 2026 comparar ambas.
- Tablas 66078 (nacional) y 66090 (CCAA): ocupados por rama CNAE-93, ANUAL, 2006 a 2008 (el INE las marca como serie histórica; modificación 2014-07-29). Solo sirven como puente anual de 2006-2007 a CNAE-2009.
- LAGUNA: no hay en la API del INE una tabla de ocupados por rama trimestral CNAE-93 para 2002T1-2007T4. INEbase la ofrece, según la búsqueda, en «tablas que incluyen actividad CNAE-93, serie 2002-2008», pero no localizada como tabla de la API (no se verificó el enlace). No se ha descargado. Para empezar en 2002 hay que bajarla a mano de INEbase (EPA, resultados nacionales, serie histórica CNAE-93) o usar anuales 2006-2007. Anotada como pendiente, no como imposible.
- Licencia: reutilización con cita de la fuente (Ley 37/2007), aviso legal del INE https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176918 . Redistribuible: sí, con cita. Cobertura: ver arriba. Frecuencia: trimestral.

## 2. INE, índices de costes de materiales y mano de obra de la construcción (mensual)

- El INE no publica una operación llamada «Índices de Costes de la Construcción». La operación equivalente es la 104 «Índices de Precios de Materiales y Energía e Índices Nacionales de la Mano de Obra» (IMM), que el INE elabora a partir de datos del Ministerio de Transportes y Movilidad Sostenible (comprobar atribución exacta en la ficha del INE antes de citar). Se descarga esa, rotulada como tal. No se ha localizado otro «ICC» oficial con descarga abierta.
- Tabla 8377 «Índice nacional de la mano de obra en construcción (base julio 1980)»: mensual, enero de 1995 a marzo de 2026, una serie.
- Tablas 8381 y 8382 (materiales generales y específicos, base diciembre 2011) y 77209 (generales, otra codificación): mensual, 2012 a marzo de 2026 (el campo de inicio indica diciembre de 2011). Tablas 8378 y 49298 (materiales, base enero 1964, 16 series; idénticas entre sí): enero de 1995 a marzo de 2026. Tabla 10759: coeficientes de enlace entre bases (16 datos).
- Última modificación del INE de estas tablas: 2026-09-21. Licencia y redistribución: como en el apartado 1.
- Costes de construcción ya disponibles por Eurostat: data/raw/eurostat_costes.csv (no se repite). Coste laboral de la construcción (ETCL) no descargado: no lo pedía la tarea.

## 3. Plazos de concesión de licencias de obra

- Sin datos oficiales descargables. No se localizó ni una serie municipal ni una estadística del MIVAU con plazos de concesión. Los portales de datos abiertos de Madrid, Barcelona y València no devolvieron un conjunto con plazos (búsqueda web, no exhaustiva; València solo publica licencias concedidas, no plazos).
- Lo único localizado es una cifra de asociación sectorial: estudio «Licencias urbanísticas: el tributo invisible», ASPRIMA con EY Abogados, 18 de mayo de 2020. Se leyó la nota de prensa de EY (https://www.ey.com/es_es/newsroom/2020/05/el-retraso-en-la-concesion-de-licencias-de-obra-nueva-tiene-un-sobrecoste-medio-para-el-comprador-de-casi-13-000-euros-por-vivienda), no el informe, cuyo PDF no se encontró. Rótulo: NOTA DE PRENSA DE UNA ASOCIACIÓN, estudio original no localizado. Según esa nota: 12 meses de media en España para obra nueva (3 para primera ocupación), frente a un máximo recomendado de 3 meses en obras mayores; por municipio, Majadahonda 16, Pozuelo y Las Rozas y San Sebastián de los Reyes 14, Madrid, Barcelona, Palma y València 12, Málaga 8 meses. Sin metodología verificada; no usar como hecho.
- Otras menciones, solo prensa: Consejo General de la Arquitectura Técnica (CGATE), 15-18 meses, vía https://www.interempresas.net/Construccion/620787-CGATE-alerta-sobre-retrasos-de-Espana-en-concesion-de-licencias-de-obra-frente-a-Europa.html (30-1-2026, sin enlace al informe); COAM, «más de 12 y 18 meses en numerosas solicitudes» (fecha no verificada).
- No se descargó nada por este apartado. Requiere al autor: decidir si se pide a los ayuntamientos (transparencia) los plazos medios de resolución de licencias de obra mayor, o si se solicita el informe a ASPRIMA.

## 4. Banco de España, potencial de viviendas previstas (VERIFICADO)

- Documento: Banco de España, Informe Anual 2025, capítulo 2, apartado sobre suelo y planeamiento, págs. 157-158 (numeración impresa), notas 40 a 46. Endpoint: https://www.bde.es/f/webbe/SES/Secciones/Publicaciones/PublicacionesAnuales/InformesAnuales/25/InfAnual_2025.pdf . Edición: PDF creado el 22-6-2026, 306 páginas. Fichero data/raw/v17/oferta_capacidad/bde/InfAnual_2025.pdf. Consultado el 2026-10-19; leído el pasaje completo, no el capítulo entero. robots.txt de bde.es sin prohibición aplicable.
- Texto original del pasaje: «una previsión de 7 millones de viviendas potenciales para el conjunto de España. En las seis grandes áreas urbanas, en las que residen un 36 % de los hogares, las viviendas que podrían edificarse y que aún se encuentran no ejecutadas se situaría en torno a 1,1 millones (16 % del total)». Nota 41: «El potencial de viviendas previstas en las capitales de las seis grandes áreas urbanas se reduce a unas 320.000 viviendas, un 4,5 % del total, y en esos municipios residen el 16 % de los hogares.»
- La cifra de partida (320.000 en las capitales) QUEDA CONFIRMADA, pero es una nota al pie, y la cifra principal del texto es 1,1 millones en las áreas urbanas. Otros datos del pasaje: Barcelona (área) unas 120.000 (5,9 % de sus hogares), Madrid 550.000 (19 %), Sevilla 163.000 (27 %); ejecución de lo previsto: Sevilla 28 %, Madrid y Málaga 35 %, Zaragoza 46,6 %; densificación hipotética: unos 0,5 millones más, y de 1 a 1,2 millones en un máximo teórico. Fuente primaria del Banco de España: el SIU de 2025 (MIVAU), estimado con imágenes de satélite, con la cautela de la nota 42.
- Licencia: Términos de uso de la información estadística del BdE, https://www.bde.es/wbe/es/estadisticas/recursos/terminos/terminos-de-uso.html (integridad de la información, citar la fuente, indicar fecha). Redistribuible del PDF íntegro: dudoso (los términos cubren la información estadística; para el informe, citar con extractos breves y atribución).
- Prensa (solo para localizar, no se cita cifra de ella): Alimarket y brainsre.news reproducen las cifras de 1,1 millones, 550.000, 163.000 y 120.000.

## Fallidas y pendientes

| Elemento | Resultado |
|---|---|
| EPA trimestral por rama 2002T1-2007T4 (CNAE-93) | No hay tabla en la API del INE; solo anual 2006-2008. Pendiente de bajar a mano de INEbase |
| «Índices de Costes de la Construcción» con ese nombre | No existe como operación del INE; se descargó la operación IMM (materiales y mano de obra) |
| Plazos de licencias, series oficiales | No localizadas; solo nota de prensa de ASPRIMA-EY (2020) y prensa; requiere al autor |
