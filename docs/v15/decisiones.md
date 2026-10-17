# V15 · Decisiones

## G1. Guardas: el hook bloquea antes que permissions.deny (B1)
- El hook PreToolUse se ejecuta antes que las reglas de permiso. Por eso, en Bash, el rechazo que se ve es el del hook. permissions.deny queda como segunda barrera; en la herramienta Read es la única.
- **Prueba hecha.** `make clean` y listar la muestra sellada fallaron por el hook. Leer un fichero de la muestra sellada con Read falló por permissions.deny.
- **Qué deja pasar la regla (a).** Un heredoc entrecomillado es inerte para el shell, así que la regla no mira su cuerpo.
- **Qué deja pasar la regla (e).** No cuenta el texto de un heredoc que solo escribe un fichero con cat o tee, como una nota que dice «nunca make all». Sí cuenta el cuerpo de un heredoc que alimenta un intérprete (bash, python…).
- **Bloqueo de make check.** El Makefile escribe el PID de make en /tmp/econometra_make_check.lock y lo borra al terminar bien. Si el check falla, el fichero queda, pero con un PID muerto, y la guarda lo ignora. Además, la guarda busca procesos `make check` vivos en /proc.

## G2. Modelos de los subagentes (B2)
Se usan los alias del plan: haiku para el inventariador; sonnet para auditor-datos, lector-literatura, montecarlo y modelizador; opus para revisor-preregistro y arbitro-final. Si un alias no está disponible en la sesión, se usará el más cercano y se anotará aquí.

## G3. Verificación de referencias sin red (B3)
- Crossref se consulta una vez por DOI y la respuesta reducida se guarda en docs/v15/literatura/crossref_cache.json, versionada con la fecha de consulta. Así `make v15_f2` y los tests funcionan sin red.
- El cuartil sale solo de docs/v15/scimago_cuartiles.csv, versionado con la fecha de consulta. Una revista que no esté ahí queda «cuartil no verificado». Nunca se supone un cuartil.
