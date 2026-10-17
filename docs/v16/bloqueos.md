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

## B-2. Parada D: Q9-g frente a la conclusión de V7.2 sobre exuberancia (2026-10-17)
- **Resultado retenido.**
  - El GSADF del factor común de la ratio valor tasado / IPC de alquiler (provincias de entrenamiento, 2002T1-2026T2) da 5,92, frente a un valor crítico bootstrap de 3,34 (p = 0,004). La herramienta es APTA (K12).
  - Está en output/v16/q9/contradiccion.md, fuera de hechos.json y de cualquier publicación.
- **Conclusión publicada afectada.** V7.2 (docs/v16/lo_ya_visto.md): «hay niveles explosivos, pero no exuberancia de los cocientes tras el ajuste múltiple».
- **Lectura según el pre-registro (solo para informar la decisión; no cambia nada publicado):**
  - Condición (a): con Benjamini-Yekutieli en la rama de diseños (m = 21, q = 0,10) el q de Q9-g es 0,153 y no la cumple (output/v16/fdr/).
  - Condición (b): Q9 no tiene magnitud de referencia («no aplica»), así que no puede ser hallazgo; a lo sumo, una pista.
  - Adenda, punto 8: «explosivo» exige además réplica sellada.
  - Tras el ajuste múltiple, el resultado no contradice la conclusión de V7.2.
- **Por qué se detiene igualmente.** El plan (sección D) dice «un hallazgo que contradiga una conclusión publicada: se documenta, no se publica y se espera», y la adenda (punto 10) aplica la parada a todo «resultado» que contradiga con dirección. A nivel nominal sí hay dirección contraria, y la lectura no es inequívoca, así que decide el autor.
- **Otras explicaciones que constan.**
  - Es el factor agregado, no el GSADF por CCAA de V7.2.
  - La tendencia del cociente puede producir rechazos de un GSADF sin deriva.
  - La ventana empieza en 2002, no en 2007.
- **Qué se necesita del autor.** Una de dos:
  - (1) tratarlo como «pista no confirmada tras BY, coherente con V7.2» y seguir con la fase 6 (réplica ciega, abogado del diablo) y la fase 7;
  - (2) mantener la parada.

