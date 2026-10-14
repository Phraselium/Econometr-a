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
