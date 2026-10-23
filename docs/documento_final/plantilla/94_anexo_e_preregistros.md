## Anexo E. Pre-registros internos

### E.1 Pre-registro interno y análisis a posteriori

**Qué es pre-registro interno sin sello de tiempo externo.**

- El plan de replicación (commit d4e9869) y su adenda, con la etiqueta git local plan-replicacion-v18 sobre el commit ad4385c, fechada el 2026-10-20. El commit está en la rama remota claude/housing-price-spain-econometric-95dhj3; la etiqueta aún no está en el remoto (tarea del autor).
- No es un pre-registro depositado en un registro externo y no debe describirse como tal. Lo fija solo el historial de git del proyecto.
- Las especificaciones, las variantes enumeradas, las reglas de estimabilidad por MDE, de clasificación y de magnitud preferida, la designación de la estimación propia de cada factor y las hipótesis de la evaluación diferida se fijaron en ese plan y su adenda, antes de la primera estimación de V18 y sin haber mirado ningún resultado.
- Los resultados de V18 se describen siempre como resultados de un pre-registro interno sin sello de tiempo externo, con su etiqueta, su commit y su fecha.

**Qué es a posteriori.**

- *Todo V17.* La auditoría de afirmaciones y medidas, la demografía, el análisis general o local, la factibilidad y las cifras V17-* se hicieron sin pre-registro y se integran aquí como análisis a posteriori de capa C4.
- *La robustez B6 de E2-R1 y E2-R1c.* Se añadió después de ver los resultados, por petición del abogado del diablo (anexo B.14.3). No cambia la especificación principal ni su clase por sí sola.
- *Las desviaciones.* Toda desviación respecto al plan (docs/v18/desviaciones*.md) se declaró con fecha y motivo. Entre ellas: el paro registrado de E2 (una versión anterior de la desviación era errónea y se corrigió); la geometría y la lectura de la ficha de E1-R4 (K8 bis); la lectura restrictiva de la contabilidad (K10); el deflactor del PIB en lugar del IPC; los ocho grupos de origen en E3.
- *Decisiones tomadas tras ver resultados de otras especificaciones.* K7 (clasificación de E8-R1 y E2-R1c tras la ronda 1 del abogado del diablo), K8 y K8 bis (E1-R4), K9 (E2-R1 tras la ronda 2, con su frase de limitación) y K12 (clase propia por especificación y correcciones de esta revisión, sin estimar de nuevo).
- *La estrategia A para extraer la magnitud de Hahn et al. (E2).* Se fijó en la fase 5 (K10), antes de combinar pero después de la etiqueta y de ver E2-R1, por ser la primera de la ficha. Es una decisión a posteriori: con la estrategia B, E2 tendría magnitud preferida (sensibilidad de B5, anexo B.2).
- *Datos descargados después de la etiqueta.* Marcados `posterior_prereg`.
- *La ilustración de la contabilidad* con magnitudes de la literatura.
- *El juicio experto del documento final.* La mejor estimación por factor, su grado de confianza y la contabilidad con magnitudes de la literatura (parte V) se escribieron en la consolidación final, después de conocer todos los resultados. Son juicio experto a posteriori y se rotulan así; no cambian ninguna cifra ni clase.
- *Réplicas del plan sobre preguntas ya vistas.* Las especificaciones que repiten una pregunta cuyo resultado ya se conocía llevan la marca `repite_visto` (plan, 0.2).

**Capa y lenguaje.** Toda cifra V18 es de capa C4 con nivel de evidencia EXPLORATORIO. Ninguna estimación es IDENTIFICADO, de modo que no se usa en ningún lugar la fórmula condicional prevista. El documento no formula ninguna cifra V18 como causa: cada una es una asociación condicionada al diseño. El generador de este documento (src/documento_final/documento_final.py, con el motor de src/v18/f6_documento.py) toma todas las cifras de output/v5/cifras_clave.csv y falla si un marcador no existe.


### E.2 Etiquetas de pre-registro del proyecto

Cada pre-registro es interno: lo fija un commit de la rama de desarrollo y una etiqueta git anotada, sin sello de tiempo externo. La tabla procede de docs/preregistros.md (generado desde git por src/v16/preregistros.py), con la columna que dice si el fichero es igual hoy que en el commit. El plan de replicación de V18 se fijó con la etiqueta local plan-replicacion-v18 (commit ad4385c); su publicación en el remoto es una tarea del autor.

{{tabla.preregistros}}
