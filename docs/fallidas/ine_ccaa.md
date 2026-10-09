# Fuentes INE por CCAA: fallos y alternativas

Revisión de las variantes CCAA de tablas ECP y EPA (servicios.ine.es/wstempus, 2026-10-09).

| archivo previsto | tabla probada | URL probada | error / hallazgo | alternativa |
|---|---|---|---|---|
| ine_ecp_ccaa_paises.csv (variante 56947) | 56947 | .../DATOS_TABLA/56947?nult=300 | HTTP 200 con `{"status": "No puede mostrarse por restricciones de volumen"}`; la tabla no se sirve | Usar 77019 (misma estructura CCAA x agrupación de países, desde 2002) |
| ine_hogares_ccaa.csv (variante CCAA de 60131) | 60133 | .../DATOS_TABLA/60133 | No es CCAA: 53 unidades provinciales (Albacete, Alicante, ...). 60135 es sólo nacional (5 series) | Sin tabla CCAA en la op. ECP. Opción: agregar las 53 provincias a 17 CCAA + Ceuta/Melilla con tabla de correspondencia (no implementado) |
| ine_epa_hogares_ccaa.csv | 65269 y hermanas 65270-65284 | .../DATOS_TABLA/65269 | Ninguna tabla EPA de hogares tiene desglose CCAA (todas nacionales) | Sin alternativa directa en EPA; la población por CCAA sí existe (65285, descargada) |
| ine_ecp_ccaa_nacionalidad.csv (candidatas 59587, 59591, 56951, 79544) | 59587 / 59591 / 56951 / 79544 | .../DATOS_TABLA/{id} | 59587 (CCAA) empieza en 2025; 59591 y 56951 son provinciales; 79544 es municipal desde 2021 | Se usa 77019 (CCAA desde 2002) |

Nota: 77019 devuelve una sola observación por año (1 de enero) que el script etiqueta "2002T1", "2003T1", ... (24 periodos, 2002-2025). Es anual, no trimestral.
