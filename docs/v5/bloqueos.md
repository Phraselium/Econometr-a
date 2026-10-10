# Bloqueos v5

## Etiquetas git no publicables en el remoto
- 2026-10-10: `git push origin prereg-v5` → HTTP 403. El remoto solo acepta push a la rama designada.
- Las etiquetas `prereg-v5` (pre-registro de B3) y, al cierre, `v5.0` quedan en el repositorio local.
- Para que el pre-registro sea verificable sin la etiqueta:
  - el commit que añade docs/v5/prereg_B3.md (`git log -- docs/v5/prereg_B3.md`) es anterior a cualquier fichero de output/v5/B3;
  - el SHA del commit del pre-registro se anota en decisiones.md.
- **Tarea del autor** (docs/v5/tareas_autor.md): publicar las etiquetas desde una copia con permisos (`git push origin prereg-v5 v5.0`).
