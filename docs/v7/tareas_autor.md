# Tareas del autor tras V7

Complementa a docs/v6_2/tareas_autor.md, que sigue vigente.

1. **Pre-registro V7.** Publica la etiqueta local `prereg-v7` (commit 3fad305), crea una release de GitHub sobre ella y obtén un DOI en Zenodo. Anota la fecha en docs/v7/notas_release.md (`fecha_verificable`). Sin ese paso, la validación diferida no tiene fecha verificable.
2. **Release v7.0.** Publica la etiqueta local `v7.0` (commit de cierre de V7) y crea su release, con las notas de la sección v7.0 de CHANGELOG.md. Las etiquetas v5.0-v6.2 siguen pendientes de publicar.
3. **Validación diferida.** Cuando se hayan publicado 2026T3-2027T2 (hacia el verano de 2027), ejecuta **una vez y con red** `make evaluate_v7`. El sha256 de la congelación debe ser `93795a9480eccf03f382bc20253561dd37e240287921453fd0d1add40a9a0646`. Publica el resultado, sea favorable o no.
4. **Revisión humana del atlas.** Pide a un econometrista de panel que revise docs/v7/validacion_herramientas.md (la aptitud de MG, PMG y CS-DL con N=17) y la regla de triangulación (V12).
5. **Datos que faltan para V8.**
   - Renta disponible por CCAA (no está en data/raw).
   - Tipos vigentes de ITP e IVA por CCAA y fecha, para sustituir el escenario genérico de R6.
   - Una serie de vacías por CCAA.
6. **Referencias del anexo de ecuaciones.** Verifica en Crossref y Scimago las que figuran como NO VERIFICADA.
