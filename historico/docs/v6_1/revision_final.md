# Revisión final independiente v6.1

Fecha: 2026-10-11. Revisor independiente; lectura dirigida y sin acceso a data/sealed. `make check` se ejecutó sin red (HTTPS_PROXY=http://127.0.0.1:9) y terminó con 0 errores en check_texto, check_v5 y check_v6. Por el tope de tokens, en esta revisión no se ha repetido `make all` ×2 en un clon limpio: queda pendiente para el cierre, como prevé el plan.

## Veredicto: REHACER

Es un REHACER acotado, solo de texto en plantillas y sin reestimaciones. No hay hallazgos críticos ni altos. Dos hallazgos medios incumplen criterios explícitos del encargo: la cifra de K1 aparece mal compuesta en cinco entregables, y quedan afirmaciones de v6 que dicen «predicen mejor» sin matizarlas frente a la base exigente.

## Comprobaciones superadas

- **K1.** Hay tabla y clase reclasificada (`clase_rotulo`). PROV_PRECIO_ANUAL figura como «frágil» y se incluye la sensibilidad con Holm sobre las 9 tareas. En el registro de accesos (docs/v2/holdout_accesos.md), cada `k1_*` tiene una sola APERTURA y una sola evaluación.
- **K2.** Hay una conclusión única: C4, «ANALIZADA, NO CONCLUYENTE», sin lectura causal. En el historial, R-12, R-13 y R-14 están reclasificadas.
- **K3.**
  - No aparece «pesa», «explica», «importa» ni «impulsa» atribuido a ML, BMA o PIP en output/v5/*.md. Los usos que quedan se refieren a supuestos del rango o a definiciones.
  - Las iniciadas no muestran orden temporal.
  - El ratio P/A se calcula con varias medidas.
- **K4.** auditoria.md tiene severidades. Las cuatro correcciones con cifra o descripción publicada están en ERRATA.md.
- **K5.** Hay informes de los dos árbitros y una carta de respuesta.
- **K6.** Están el backlog y tareas_autor. Este último incluye:
  - releases sobre cc69e02, bac2fda, 08d7629 y v6.1;
  - Zenodo;
  - etiquetas locales señaladas como no verificables;
  - pre-registro con la fecha real de publicación.
- **Make.**
  - V6_1_ORDEN está en el Makefile.
  - src/v6/m4_lineas_base.py está fuera de make.
  - Ningún script de src/v6_1 abre data/sealed.
  - Todas las entradas leídas están versionadas.
- **Neutralidad.** No hay referencias a partidos ni lenguaje valorativo.
- **Lenguaje causal.** No hay términos causales en los entregables.

## Hallazgos

1. **Media.** Texto mal compuesto y sin denominador: «en 6,0 tareas de las tareas».
   - **Ubicación:** output/v5/informe_tecnico.md §11.3 bis (l. 646), working_paper §6.1 (l. 235), lo_que_sabemos (l. 77), policy_brief (l. 59) y una_pagina (l. 16). El origen es `{{K1-N-MEJOR:valor}} de las tareas` en docs/v5/plantillas/*.md.
   - **Corrección:** en las cinco plantillas, cambiar el texto a «en 6 de las 9 tareas». Para ello, usar `{{K1-N-MEJOR:valor}}` con formato entero, o añadir en k1_run.py una cifra `K1-N-TAREAS` (9) y no repetir la unidad. Después, regenerar con render.

2. **Media.** Quedan afirmaciones de v6 que dicen «predicen mejor que la persistencia o la inercia» sin matizar en el mismo párrafo frente a la base exigente. En concreto, el precio provincial aparece como ventaja firme, cuando K1 lo clasifica como frágil.
   - **Ubicación:** informe_tecnico §11.3 «Lectura» (l. 637), working_paper l. 151 (resumen de M4), lo_que_sabemos l. 54 y policy_brief l. 50.
   - **Corrección:** añadir en cada uno una frase como esta: «Frente a la línea base más exigente (v6.1, §11.3 bis), la ventaja se mantiene en alquiler de stock y en el precio trimestral de tasación, es frágil en el precio provincial anual y desaparece en el municipal, con Registradores y en el volumen anual.»

3. **Baja-media.** En §11.3 bis y en «qué cambió», la ventaja en «precio trimestral de tasación» se da como mantenida. Sin embargo, en tabla_modelos_k1.md el grupo temporal es «peor» (ratio 1,048) y el total «no distinguible» (0,947). Hoy solo se avisa de esto en el volumen trimestral.
   - **Corrección:** en la fila «Compra, valor tasado, provincia trimestral», poner «predice mejor en la parte espacial; peor en la temporal», igual que en la fila del volumen.

4. **Baja.** En §6.1 y sus copias, el 4,3 % aparece como «sin controles». En K2 (inmigracion.md §G (4)), ese 4,26 lleva efectos fijos y es la especificación sin población ni demanda externa. Además, el -1,3 corresponde a la muestra del paso (4), no al -2,23 [-4,67; 0,20] del paso (2).
   - **Corrección:** cambiar el texto a «con efectos fijos y sin controles de población ni de demanda externa», y añadir que con población el IC95 incluye 0.

5. **Baja.** En la tabla §11.3 bis, el cociente de MUN_PRECIO_ANUAL (1,049) aparece redondeado a «1,0». Así parece que el modelo empata con la base, cuando es algo peor.
   - **Corrección:** usar dos decimales en la columna «Cociente».

6. **Baja.** En auditoria.md, la tabla de recuento pone «Media: 0 cambian cifra publicada», pero R-10 tiene entrada en ERRATA (es de descripción y no cambia cifras).
   - **Corrección:** añadir una nota a la tabla: «R-10 en ERRATA por descripción, sin cambio de cifra».

7. **Pendiente de cierre (no bloquea).** `make all` ×2 sin red en un clon limpio y comparación de md5, como prevé el plan.

## Prioridad

1 → 2 → 3, con un único render y `make check`. 4-6 son opcionales pero baratas. Con 1-3 corregidas, el veredicto pasa a APROBAR sin necesidad de otra ronda completa: basta comprobar con grep «tareas de las tareas» y la frase de matiz en las cuatro ubicaciones del hallazgo 2.

## Respuesta del orquestador (REHACER 1 de 2: aplicado sin otra ronda completa, como indica el revisor)
1. Se escribe «{{K1-N-MEJOR:num}} de las {{K1-N-TAREAS:valor}}», que se renderiza «6 de las 9 tareas». Se añade el hecho K1-N-TAREAS y «tareas» como recuento entero en render.py.
2. Los cuatro textos que comparaban solo con la persistencia (informe §11.3, working paper §4.5, lo que sabemos y policy brief) ahora matizan el resultado frente a la línea base más exigente.
3. El informe §11.3 indica que, en el precio trimestral, el modelo queda por detrás de la base en la parte temporal.
4. La etiqueta pasa a ser «sin población ni controles de demanda externa».
5. Los cocientes se dan con dos decimales.
6. auditoria.md añade la nota sobre R-10.
Después: render, check_v5 y check_texto con 0 errores; `make check` completo antes del cierre.
