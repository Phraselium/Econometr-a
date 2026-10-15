# Auditoría de exhaustividad de V9-DATOS-COMPLETO (bloques 1-9; 2026-10-15)

Regla aplicada: como máximo 3 intentos y 30 minutos por fuente, serie desde el primer periodo disponible y cruces solo por código INE. Las fuentes sin licencia clara no se suben. La segunda pasada (bloque 9) repite cada fallo una vez por otra vía.

| Bloque | Fuente | Estado | Primer periodo | Segunda pasada | Detalle |
|---|---|---|---|---|---|
| 1 | IDESCAT HUT y apartamentos por municipio | ✔ | 2015 | — | cuadra con el total de Cataluña |
| 1 | IDESCAT hoteles, campings y rural por municipio | ✘ | — | ✘ (sin años a escala municipal) | no lo usa ningún diseño |
| 1 | Registre de Turisme (agregado) | ✔ no redistribuible | corte | — | sin fechas de alta |
| 1 | IEET por municipio | ✔ no redistribuible | 2017S1 | — | sin código; requiere correspondencia por nombre (no se usa en D1-D7) |
| 1 | Barcelona HUT por barrio | ✔ parcial | expediente 2008 | ✘ cortes trimestrales (anti-bot) | registro vigente por API |
| 1 | Registro turístico de Euskadi | aplazado | — | — | ningún diseño lo necesita (D1 usa EMAL) |
| 1 | Cortes antiguos del registro VUT de la GVA | ✘ | — | ✘ (web.archive.org bloqueado) | panel reconstruido del proyecto |
| 1 | INE VUT noviembre de 2026 | no publicado | — | — | edición de mayo de 2026 |
| 1 | Establecimientos turísticos de València | aplazado | — | — | D3 usa el registro VUT de la GVA |
| 2 | Catastro INSPIRE, valores de referencia, GTFS, universidades | aplazado | — | — | D3 usa como accesibilidad la distancia al centro de València calculada con la geometría del proyecto (decisiones.md, E2) |
| 3 | Padrón por nacionalidad y país de nacimiento | ✔ | 2003 | — | 107 tablas, 52 provincias |
| 3 | EM y EMCR por provincia | ✔ | 2008 | — | — |
| 3 | EVR 1988-2007 | ✘ | — | ✘ (no está en tempus ni en jaxiT3) | aproximación por padrón (marcada) |
| 3 | ECEPOV 2021 | aplazado | — | — | ningún diseño lo necesita |
| 3 | Censo 2011 por provincia | ✔ | 2011 | — | — |
| 3 | Censo 2001 por provincia | ✘ | — | ✘ (solo sistema interactivo) | D7 empieza en 2011 |
| 4 | Seccionado INE 2025 | ✔ (V10) | 2025 | — | otras ediciones solo bajo demanda (D3 usa 2025) |
| 4 | Sección ↔ código postal | ✔ | 2025-06-30 | — | callejero del censo electoral |
| 4 | Sección ↔ barrio de València | ✔ (V10) | — | — | — |
| 4 | Polígonos de códigos postales (CartoCiudad) | aplazado | — | — | sustituido por la tabla sección-CP |
| 5 | SEPE paro y contratos por municipio | ✔ | 2006-01 | — | — |
| 5 | Afiliación por municipio | ✘ | — | ✘ (IDESCAT `afi` sin SSV municipal estable) | SEPE |
| 6 | BCE, cuota de nuevos préstamos a tipo variable | ✔ | 2003-01 | — | — |
| 6 | BCE, volúmenes por fijación y país | ✘ | — | ✘ (solo U2) | RAI |
| 6 | Eurostat IPCA alquileres mensual | ✔ | 1996-01 | — | — |
| 6 | Suelo, VPO, licencias, CGPJ, BdE | ✔ (proyecto, al día: bloque 0) | — | — | comparacion_ediciones.csv |
| 7 | Microdatos ECV y EPA | ✔ (V9-DATOS) | 2018 | — | ECV sin mes de nacimiento: D6 no es posible |
| 8 | Solicitudes de transparencia | redactadas | — | — | docs/v9/solicitudes_transparencia.md |
| 9 | Segunda pasada | hecha | — | — | columna «Segunda pasada» |

Resumen: los datos de D1, D2, D4 y D5 están completos; D3 está completo con limitaciones (dos cortes del registro); D7 cubre 2011-2025 a escala provincial. D6 no tiene datos suficientes (no se estima). Ningún fallo impide un diseño que se pueda estimar.
