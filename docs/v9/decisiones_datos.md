# Decisiones V9-DATOS (solo descarga y validación)

## D0 — Alcance y organización (2026-10-14)
- **Alcance.** Solo descarga, validación y documentación. No se estima nada, no se modifican salidas ni entregables y no se abren muestras selladas. Rama `v9-datos` (desde v9-prep), subida a la rama designada.
- **Infraestructura común** (orquestador):
  - src/v9/comun.py: descarga con caché, manifiesto por fuente y columna `posterior_prereg`;
  - src/v9/datos_v9.py: `make datos_v9`, que verifica sin red y descarga si falta, y consolida data/raw/v9/_manifest.csv.
- **Subagentes.** Cinco subagentes haiku en paralelo, con un tope explícito de 60.000 tokens cada uno y parada al 80 % (≤0,3 M en total, dentro del presupuesto de 0,4 M):
  - EMAL y afiliación;
  - INE (censo anual, IPVA, VUT y microdatos);
  - València (padrón, registro de viviendas turísticas de la GVA y fianzas de la GVA);
  - Inside Airbnb;
  - Eurostat, BCE, Aena e Incasòl.
- **Orquestador.** Hace la validación (tests), la cobertura, el diccionario, las licencias y .gitignore, y la integración con `make datos_terceros` y `make check`.
- **Periodos posteriores al pre-registro.** Las series de precios y alquileres con fecha llevan la columna `posterior_prereg` (True desde 2026T3, la fecha de inicio de evaluate_v7 y evaluate_v8). Esas filas no se usan en ningún cálculo y no se miran sus valores.

## D1 — Presupuesto de subagentes (2026-10-14)
- Los cinco subagentes haiku no respetaron el tope de 60.000 tokens: el uso medido por el sistema incluye la lectura de contexto. Consumo:
  - EMAL y afiliación: 107.436;
  - València: 102.121;
  - INE: 103.297;
  - Inside Airbnb: 105.041;
  - Eurostat, BCE, Aena e Incasòl: detenido por el orquestador a mitad; su consumo no consta.
- Total: unos 418.000 más el detenido. **Supera el tope de 0,4 M.** En cuanto se vio la desviación no se lanzó ningún subagente más, se detuvo el que seguía activo y el resto lo terminó el orquestador:
  - censo INE por códigos;
  - EMAL;
  - IPVA, microdatos, fianzas de la GVA, Incasòl y volúmenes del BCE;
  - validación, tests y documentación.

## D2 — Correcciones del orquestador sobre las descargas de los subagentes
- **Censo anual.** El subagente emparejaba municipios por nombre, cosa que prohíben las reglas del proyecto. Se rehízo con los códigos INE que trae cada etiqueta del CSV de jaxiT3: provincia, municipio y sección de 10 dígitos.
  - La tabla nacional con todas las secciones (65036) duplica las provinciales y no cabe en memoria: se omite.
  - Cuadres exactos con el total publicado en 2021-2025.
- **EMAL.** Había claves duplicadas porque el bloque «vigentes a fecha» heredaba el año y se ignoraba la fila de estadísticos. El periodo pasa a ser `vigente_<fecha>[_estadístico]` y ya no quedan duplicados. Cuadre: Euskadi = suma de los territorios históricos.
- **Registro VUT de la GVA.** El código `03000` (registros sin municipio) se conserva y se documenta; su stock es nulo en los cortes recientes. El panel mensual reconstruido es C4, porque depende de cómo se fechan las altas y las bajas (gva_vut/LEEME.md).
- **gzip determinista** (mtime = 0) en todos los scripts, para que dos ejecuciones den el mismo sha256. Se corrigió además una ruta errónea en la verificación de Incasòl y del BCE.
- **BCE.** Se añaden los volúmenes de nuevas operaciones (DATA_TYPE_MIR = B). El BCE solo los publica para el total, no por periodo de fijación.

## D3 — Licencias, tamaño y versionado
- **Se versionan** (licencia abierta y tamaño razonable):
  - EMAL (CC BY 4.0);
  - censo anual derivado (INE);
  - IPVA (INE);
  - registro VUT de la GVA (CC BY 4.0, cortes y paneles);
  - Eurostat y BCE derivados;
  - agregados de Inside Airbnb (sección, barrio y resúmenes por anuncio).
- **No se versionan**, con su sha256 en el manifiesto y descarga con `make datos_v9`:
  - microdatos del INE, por tamaño (unos 0,6-0,8 GB);
  - originales del censo, BCE y Eurostat, por tamaño;
  - listings completos de Inside Airbnb: contienen datos personales de anfitriones (nombre, descripción), aunque la licencia sea CC BY;
  - copias de las fianzas de la GVA: son idénticas a data/raw/v5.
- **Incasòl.** «Términos de uso» (no CC BY): no se versiona y se añade a `make datos_terceros` (inventario, CHECKSUMS y script).

## D4 — Refrescos
- **Fianzas de la GVA 2020-2026:** la versión actual es idéntica byte a byte a la del proyecto.
- **Incasòl:** sin periodos nuevos frente a v3.
- **INE VUT:** no hay edición de noviembre de 2026; la última es mayo de 2026, ya en el proyecto.
- **IPVA:** 2024 es la última edición. Se añaden las tablas por antigüedad del contrato y por distritos.
- **Panel europeo de precios (v8):** ya llega a 2026T2; no se refresca.

## D5 — Periodos posteriores al pre-registro
- Llevan la columna `posterior_prereg` las series de precios o alquileres con fecha que podrían solaparse con evaluate_v7 o evaluate_v8: EMAL e Incasòl.
- Las demás series nuevas no son las que evalúan evaluate_v7 y evaluate_v8 (IPV, IPC de alquiler, valor tasado). Los tipos del BCE llegan a 2026-08, pero no son series evaluadas.
- No se ha mirado ningún valor de 2026T3 en adelante.

## D6 — Cierre (2026-10-14)
- **Fuentes y ficheros.** `make datos_v9 --solo-verificar`: 93 ficheros registrados en 11 fuentes, todos verificados.
  - Microdatos INE: EPA, 34 trimestres (2018T1-2026T2) más 2 diseños de registro; ECV, 8 años (2018-2025); unos 1,1 GB, no versionados.
- **`make check`:** rc = 0, 319 tests aprobados (11 de V9); check_texto, check_v5, check_v6 y check_v8 con 0 errores.

# V9-DATOS-COMPLETO (2026-10-14; sin subagentes, todas las descargas las hace el orquestador)

## D7 — Bloque 0: regulación hasta octubre de 2026 e inventario
- **Ficheros de partida** (solo lectura):
  - data/raw/v3/zonas_tensionadas_v3.csv (318 declaraciones de 317 municipios; igual que data/raw/v2_zonas_tensionadas.csv);
  - data/raw/v2_eventos_politica.csv (41 eventos);
  - data/raw/v3/eventos_v3.csv (8);
  - data/raw/v3/cataluna_contencion_rentas_v3.csv (332 municipios, régimen de la Ley 11/2020).
- **Método** (src/v9/fetch_regulacion.py):
  - se escanean los 1.239 sumarios diarios del BOE entre el 2023-05-25 y el 2026-10-14 (API de datos abiertos) con un patrón de términos de vivienda: 1.992 títulos;
  - de la sección I y de las resoluciones de zonas tensionadas se descarga el XML de cada disposición (102 normas): metadatos, vigencia, derogación y referencias posteriores (convalidación o derogación);
  - las normas catalanas que no están en el BOE se toman del conjunto abierto del DOGC (Portal Jurídic, n6hn-rmy7).
- **Zonas tensionadas.**
  - Las 10 resoluciones de la Secretaría de Estado de Vivienda publicadas en el BOE hasta el 2026-10-14 son exactamente las de v3: **no hay declaraciones nuevas** entre la de julio de 2026 (BOE-A-2026-16532) y la fecha de corte.
  - El script falla si el conjunto difiere.
  - Cada nombre de municipio de v3 aparece en el texto de su resolución (segunda fuente: el propio BOE; 318 de 318).
  - La única corrección de erratas (BOE-A-2025-20246) solo cambia enlaces.
  - Se completa la fecha de declaración de Navarra (vacía en v3) con el título de la Orden Foral 157E/2025 y queda marcada la fuente de la fecha.
- **Alcance** (regimen_alcance_v9.csv; transcrito de la norma con su identificador): topes (art. 17.6 y 17.7 LAU), prórrogas, temporada y habitaciones.
  - Cataluña:
    - DL 6/2024: vigente del 2024-04-26 al 2024-05-27; derogado por no convalidación;
    - DL 1/2025;
    - DL 2/2025: convalidado por la Resolución 169/XV;
    - Ley 11/2025, arts. 66 bis y 66 ter de la Ley 18/2007: vigente desde el 2026-01-01; recurso de inconstitucionalidad admitido, sin suspensión publicada.
  - Navarra: LF 11/2026, de habitaciones.
  - Estatal:
    - RDL 8/2026: derogado;
    - RDL 26/2026 y RDL 27/2026: derogados;
    - RDL 28/2026 y RDL 29/2026: pendientes de convalidación a la fecha de corte.
  - Las medidas que empiezan desde 2026T3 llevan `posterior_prereg = sí`.
- **Banderas automáticas** de eventos_regulacion_v9.csv (`menciona_*`): búsqueda literal en el texto. Orientan la lectura, pero **no** sustituyen al articulado.
- **DL 1/2025 catalán.** Su convalidación o derogación queda **NO VERIFICADA** (fuentes_fallidas.md).
- **Inventario de series con edición nueva** (src/v9/fetch_actualizaciones.py, comparacion_ediciones.csv). Todas tienen a 2026-10-14 la misma última observación que el proyecto:
  - suelo urbano (2026T2);
  - VPO anual (2025) y mensual (2026-06);
  - viviendas libres iniciadas y terminadas;
  - crédito del BdE (2026-06 y 2026-08);
  - shocks del BCE (2025-10);
  - costes de construcción de Eurostat (2026T2).
- **Copias.** De MIVAU no se guarda copia, porque duplicaría el proyecto. Los CSV originales del BdE sí se guardan, porque el proyecto solo tenía extractos.

## D8 — V9 COMPLETO, F1: bloques 1-9 (2026-10-15)
- **Criterio de prioridad.** Se descarga primero lo que necesitan los diseños pre-registrables D1-D7. Lo que ningún diseño usa se documenta como aplazado (docs/v9/auditoria_exhaustividad.md), porque el prompt prohíbe análisis fuera de él.
- **Fuentes nuevas** (todas con manifiesto y sha256; cruces por código):

  | Script | Fuente | Periodo | Nivel | Redistribuible |
  |---|---|---|---|---|
  | fetch_cat_turisme.py | IDESCAT turall (HUT y apartamentos) | 2015-2025 | municipio (código IDESCAT → INE) | sí |
  | fetch_cat_turisme.py | Registre de Turisme (agregado) e IEET | corte 2026-10; 2017S1-2025S1 | municipio | no (`make datos_terceros`) |
  | fetch_bcn_hut.py | Open Data BCN, HUT vigentes | año de expediente 2008-2026 | barrio de Barcelona | sí (CC BY 4.0) |
  | fetch_ine_padron_nacionalidad.py | Padrón continuo por nacionalidad y por país de nacimiento | 2003-2022 | provincia y municipio | sí |
  | fetch_ine_migraciones.py | EM (24379, 24385, 24323, 24326) y EMCR (69764, 69693, 69708, 69733) | 2008-2021 y 2021-2024 | provincia | sí |
  | fetch_ine_censos.py | Censo 2011, viviendas por tipo (3457) | 2011 | provincia | sí |
  | fetch_ine_callejero.py | Callejero del censo electoral, julio de 2025 | 2025-06-30 | sección × código postal | sí |
  | fetch_sepe_municipios.py | SEPE, paro y contratos registrados | 2006-01 a 2026 | municipio | sí |
  | fetch_bce_rai.py | BCE RAI, cuota de nuevos préstamos a tipo variable | 2003-01 a 2026-08 | país | sí |
  | fetch_eurostat_alquiler.py | Eurostat prc_hicp_minr CP041 | 1996-01 a 2026-08 | país | sí |

- **Cuadres.**
  - IDESCAT: la suma municipal de HUT coincide con el total de Cataluña publicado (47.242 en 2015 y 105.399 en 2025).
  - Padrón: la suma de municipios coincide con el total provincial en todas las provincias con fila provincial (diferencia máxima 0). Las tablas uniprovinciales no traen fila provincial con código, así que el total provincial de la base se calcula siempre como suma de municipios.
  - Callejero: 36.626 secciones (seccionado 2025: 36.554, más las secciones dadas de baja en el semestre) y 10.790 códigos postales.
- **Barcelona HUT.** El año del número de expediente no es la fecha de alta: es el año de inicio del trámite. Como no hay licencias nuevas desde 2014 (PEUAT), el stock vigente aproxima el de 2019. Las bajas no se observan: la exposición por barrio se usa como **medida aproximada**, marcada.
- **SEPE en la base.** Media de los 12 meses solo para años completos. El mensual queda en data/raw/v9.
- **Padrón municipal por nacionalidad** (6,2 millones de filas): no entra en la base, que solo tiene el agregado provincial (39.520 filas). D4 lee el fichero municipal directamente de data/raw/v9.
- **Base.** `make base` pasa de 10,16 a 10,67 millones de filas; 13 variables nuevas, todas redistribuibles. Incasòl, el agregado del Registre y el IEET siguen fuera de la capa pública.
