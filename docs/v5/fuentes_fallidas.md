# Fuentes fallidas v5

Cada entrada: fuente, endpoint probado, edición, fecha de la prueba, error.


## R1c (2026-10-10)
- Catastro: titulares por naturaleza (persona fisica o juridica) y titularidad publica: sin fichero abierto (comprobado en v4: URBANA solo trae unidades, valor y superficie). Sin dato; solicitud S1 (docs/v4/solicitudes.md).
- Censo 2021, regimen de tenencia por edad de la persona de referencia: sin tabla en Tempus (operaciones CENSOP 463 y CENSOPV 8, probado 2026-10-10); solicitud S7. Se usan EFF 2022 y ECV 2022-2025 (INE 9994) como fuentes por edad.
- Notariado: compradores persona juridica: el repositorio solo trae extranjeros y actos; sin dato.
- INE ICC (indice de costes de construccion): no existe como operacion en Tempus (busqueda en OPERACIONES_DISPONIBLES, 2026-10-10); se usan Eurostat sts_copi_q (en repositorio) e INE ETCL tablas 6030. Afiliacion a la Seguridad Social, seccion F, por provincia: no localizada en fuente abierta accesible. Tabla EPA 66088 (ocupados por sector y CCAA) solo trae 2005-2007 (base antigua); se usa 65354 (provincia, 2007T4-2026T1).
- BK-034 (corregido): la tabla INE 59531 (Censo 2021, consumo electrico, DATOS_TABLA?nult=1) SI publica vacias y uso esporadico por entidad municipal: 3.185 entidades (510 marcadas con asterisco agrupan municipios pequenos) que suman el total nacional. No hay desglose por seccion censal. Fuente unica (C4).
