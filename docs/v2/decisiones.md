# Decisiones v2 (orquestador)

Formato: fecha · ámbito · decisión · motivo.

- 2026-10-10 · git · Ramas locales r2/main y r2/<rama> (worktrees ../wt-<rama>). El push se hace SOLO a la rama remota designada para esta sesión (`git push origin r2/main:claude/housing-price-spain-econometric-95dhj3`): las instrucciones de la sesión prohíben empujar a otras ramas remotas. Las ramas r2/<rama> se fusionan en r2/main tras APROBAR y viajan dentro de ella.
- 2026-10-10 · datos · `data/raw/gva_vut_municipio.csv` (64 MB) ya está versionado desde v1; migrarlo a LFS exigiría reescribir el historial y sacarlo de git rompería `make all` sin red. Se mantiene versionado como excepción documentada con checksum en data/CHECKSUMS.sha256. Los demás >50 MB siguen en .gitignore con checksum.
- 2026-10-10 · holdout · `src/holdout.py` localiza data/sealed en el repositorio principal (git common dir), no en el worktree, y registra cada acceso en data/sealed/_accesos.log (copia del log versionada en docs/v2/holdout_accesos.md). Las ramas leen SOLO los ficheros de entrenamiento que genera holdout.py.
- 2026-10-10 · holdout · Limitación conocida: los últimos 8 trimestres nacionales ya se usaron en v1 (informe v1). El sellado es estricto para v2, pero no «virgen» a nivel nacional; las hipótesis confirmatorias se evalúan preferentemente en las provincias selladas.
- 2026-10-10 · B0 · La base de eventos de política se construye con un data-fetcher en modelo sonnet (no haiku) porque exige leer normativa en el BOE y verificar fechas y alcance; cada evento con URL oficial comprobada.
- 2026-10-10 · literatura · Caldera y Johansson (2013) pasa a VERIFICADA (DOI en Crossref) en v2; en el informe v1 figura como NO VERIFICADA y no se modifica (v1 aprobado). El informe v2 usará el estado v2. Cavalleri et al. (2019): DOI existe pero Crossref no lista autores → se mantiene como parcialmente verificada.
- 2026-10-10 · literatura · Cuartiles Scimago leídos de resultados de búsqueda (la ficha directa devuelve 403); en la mayoría corresponden a la edición 2025, no al año de publicación: se indica en la tabla.
