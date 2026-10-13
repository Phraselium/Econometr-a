# V8.1: coherencia de V8, capa de consulta y datos de terceros

Autor: Borja Romero, economista (firma individual, independiente). Sin estimaciones nuevas: ninguna cifra publicada cambia (CHANGELOG.md; ERRATA.md sin entradas nuevas).

- **V8 es la versión de referencia** de modelización: output/v8/por_que_ha_subido.md, output/v8/informe_econometrico.md, output/v8/tablas_modelos_destacados.md y output/v8/tablas_v8.xlsx, también en publicacion/.
- **Coherencia.** El multiverso se lee también por variables, además de por familias. La regla de periodo del alquiler queda como «no evaluable». Se añaden avisos de colinealidad (población total y extranjera) y sobre el signo del tipo real, la remisión a las cifras de contratos nuevos junto al IPC de alquiler, la discrepancia de fuentes en la provincia de Valencia y la parte no atribuida de la subida de 2022-2026.
- **Capa de consulta.** consulta/ (guía para asistentes, hallazgos, preguntas frecuentes, glosario, índice y versión) y llms.txt, generados por `make consulta`.
- **Datos de terceros.** Los ficheros sin redistribución claramente permitida salen del repositorio (docs/v8_1/datos_retirados.md). `make datos_terceros` los descarga y verifica su sha256 antes de `make all`.
- **Reproducción.** `make datos_terceros`, `make all`, `make v8`, `make publicacion`, `make consulta` y `make check` (sin red tras la descarga).

Pre-registros: docs/v7/hipotesis.md (`prereg-v7`) y docs/v8/hipotesis.md (`prereg-v8`). Evaluación diferida en 2027: `make evaluate_v7` y `make evaluate_v8`.
