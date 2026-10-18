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

- **B-2 resuelto (2026-10-18).** El autor eligió la opción 1: pista no confirmada (C4), coherente con V7.2; no aplica la parada D (decisión K15).
- **Nota (2026-10-18).** Tras K16 el q de Q9-g es 0,306, no 0,153. La lectura no cambia.

## B-3. Parada: un error corregido en V16 afecta a una tabla publicada de la 1.0 (2026-10-18)
- **Qué.** La auditoría docs/v16/alcance_errores_k16.md busca en v1-V12 los cinco errores corregidos en V15/V16. Solo E4 (cuotas del año base imputadas a 0) aparece en código que alimenta material publicado: V8-M5, el IV3 Bartik.
- **Efecto.**
  - Cambian 8 filas de publicacion/tablas_v8.xlsx, hoja «Atribucion»: entre un 1 % y un 11 %.
  - No cambia ninguna cifra de cifras_clave.
  - No cambia ninguna capa ni ninguna conclusión. Las filas no votan en la regla §9 y el F efectivo sigue por debajo de 3,4.
- **Registro.** Entrada en ERRATA.md con «pendiente de decisión del autor».
- **Por qué se para.** El encargo del autor del 2026-10-18 lo pide: «Si afecta a algo publicado en la 1.0, entrada en ERRATA y para».
- **Qué se necesita del autor.** Elegir una de tres opciones:
  - (a) Corregir en una versión posterior: excluir las dos CCAA, regenerar M5 → F5 → F6 → publicación con orden expresa y fijar la errata como aplicada.
  - (b) Dejar la errata como aviso sin regenerar, porque no cambia ninguna cifra de cifras_clave ni ninguna conclusión.
  - (c) Imputar la celda con años vecinos y reportar ambas versiones.
- **Fase 7.** Queda en espera hasta la decisión.
- **Al margen, sin cuantificar.** En IV2 de M5, los flujos ausentes se ponen a 0 antes de diferenciar. Afecta al choque, no a la cuota, y las cifras H8-7 tienen F = 0,05 sin respaldo tras Holm, así que su capa no cambiaría.

## B-4. Parada: la réplica ciega de cifras de la 1.0 encuentra errores que cambiarían cifras publicadas (2026-10-18)
- **Qué.** Réplica ciega de las 31 cifras de una_pagina.md (incluye las 7 C1 y dh_2125), en cuatro lotes, con reconciliación de las que discrepaban. Detalle en K19.
- **Errores del original que cambian valores publicados (GSADF de V7.2; src/v5/r1b_gsadf.py).**
  - E1: el BIC compara modelos con distinto n.
  - E2: Navarra queda truncada por un `dropna` conjunto.
  - Efecto corregido: V72-GSADF-ccaa-bh 7 → 0, niveles-bh 2 → 0, ratios-p05 3 → 1. ratios-bh sigue en 0 con la familia de 8, pero es inestable con 499 réplicas.
  - Son cifras de una_pagina.md. Ninguna capa cambia (C4) y el veredicto de la ficha de burbuja tampoco.
- **Correcciones de texto en V8, sin cambio de valor.** El periodo de V8-H8-9-est, el rótulo de la media y la banda de V8-QNA-pp-c-P5, y la regla Y10 de V8-VOTOS-c-P5.
- **Registro.** Entradas en ERRATA.md, «pendiente de decisión del autor». No se ha tocado nada publicado.
- **Relación con K15.** La lectura de Q9-g se apoyaba en «0 cocientes tras BH». Con E1 corregido sigue siendo 0 con la familia de 8, pero el 0 publicado no es estable a la semilla con 499 réplicas.
- **Qué se necesita del autor.**
  - (1) Si se corrigen E1 y E2 y se regenera V7.2 → cifras_clave → una_pagina → publicacion. Hace falta orden expresa: cambia valores publicados. Hay que decidir además el número de réplicas (499 o más) y la familia de BH.
  - (2) Si se aplican las correcciones de texto de V8.
- **Fase 7.** Queda en espera.

