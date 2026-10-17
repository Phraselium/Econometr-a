# V16 · Bloqueos

## B-1. El remoto no acepta etiquetas desde esta sesión (2026-10-17)
- **Qué pasa.** `git push origin prereg-v15` devuelve **HTTP 403** del proxy de git de la sesión (`error: RPC failed; HTTP 403`). El push de la rama designada sí funciona. Es una denegación de política: no se reintenta. Las herramientas de GitHub de la sesión no crean etiquetas.
- **Efecto.**
  - Las etiquetas prereg-* solo existen en el repositorio local de este contenedor. Sus commits sí están en la rama remota.
  - La guarda (d) mantiene cerradas las fases 4 y 5 de V15.
  - Cuando se cierre la fase 4 de V16, la guarda (f) cerrará sus fases 5 a 7 hasta que prereg-v16 esté en el remoto.
- **Salida.** El autor publica las etiquetas desde su clon con los comandos de docs/v16/tareas_autor.md. La lista de etiquetas y commits está versionada en docs/v16/etiquetas_prereg.csv, así que se pueden recrear aunque este contenedor desaparezca.

- 2026-10-17: prereg-v16 se creó en local, sobre a8304ec, y se intentó publicar 5 veces, con espera exponencial. En todas el remoto cortó la conexión («remote end hung up»). Es el mismo bloqueo B-1. Los comandos para publicarla están en tareas_autor §1. Hasta entonces, la guarda (f) bloquea las fases 5-7.

- **B-1 resuelto (2026-10-17).** El autor publicó las 11 etiquetas desde su ordenador. Desde esta sesión el remoto sigue rechazando las etiquetas (HTTP 403), pero ya no hace falta: las puertas de V15 (d) y V16 (f) quedan abiertas con la etiqueta y el criterio provisional (decisiones K10).
