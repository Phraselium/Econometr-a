# V17 · Decisiones

## K0. V17 se ejecuta dentro de V18 (2026-10-19, orden del autor)
- El plan de V17 (docs/v17/plan.md) no se llegó a ejecutar en su momento. El autor ordena ejecutarlo dentro de V18.
- Se ejecutan completas las fases 0, 1, 2 y 3 de V17, y la 5 (integración y check_v17).
- La fase 4 (documento estilo Documento Ocasional del Banco de España) NO se ejecuta. Su contenido se integra en el Documento de Trabajo de la fase 6 de V18. Ese documento debe incluir también las secciones de V17 sobre demografía, problema general o local, factibilidad de construir, discurso público y medidas auditadas.
- CLAUDE.md sigue apuntando a V18, con una línea añadida que remite a docs/v17/plan.md.
- Todo lo de V17 es a posteriori (plan V17, sección A).

## K1. Subagentes sin worktree (2026-10-19)
- El plan pide worktrees para los subagentes que escriben.
- Quedan unos 4 GB de disco, y cada worktree con data/ enlazada y salidas ocupa varios GB.
- Los subagentes de V17 escriben en ficheros disjuntos (un grupo por fichero, nombres distintos en src/v17/, output/v17/ y tests/v17/) y nunca en src/econ_utils.py ni en data/ de versiones anteriores. Por eso trabajan en el árbol principal.
- Siguen siendo como máximo 3 a la vez.
- El orquestador revisa el diff de cada uno antes del commit.

## K2. Ficheros de terceros fuera de git (2026-10-19)
- Los PDF de data/raw/v17 se dejan fuera de git (.gitignore), con su sha256 en el _manifest.csv de cada carpeta.
- InsideAirbnb también queda fuera: su licencia es CC BY 4.0, pero su política pide no republicar los datos.
- Solo se versionan agregados propios.
- Los Registradores se guardan en _terceros/, también ignorada.
