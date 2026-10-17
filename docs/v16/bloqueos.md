# V16 · Bloqueos

## B-1. El remoto no acepta etiquetas desde esta sesión (2026-10-17)
- **Qué pasa.** `git push origin prereg-v15` devuelve **HTTP 403** del proxy de git de la sesión (`error: RPC failed; HTTP 403`). El push de la rama designada sí funciona. Es una denegación de política: no se reintenta. Las herramientas de GitHub de la sesión no crean etiquetas.
- **Efecto.**
  - Las etiquetas prereg-* solo existen en el repositorio local de este contenedor. Sus commits sí están en la rama remota.
  - La guarda (d) mantiene cerradas las fases 4 y 5 de V15.
  - Cuando se cierre la fase 4 de V16, la guarda (f) cerrará sus fases 5 a 7 hasta que prereg-v16 esté en el remoto.
- **Salida.** El autor publica las etiquetas desde su clon con los comandos de docs/v16/tareas_autor.md. La lista de etiquetas y commits está versionada en docs/v16/etiquetas_prereg.csv, así que se pueden recrear aunque este contenedor desaparezca.
