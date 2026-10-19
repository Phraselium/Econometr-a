# V17 · Fase 2 · Encargo común de inferencia convencional (B2-B3)

Análisis a posteriori (V17). Este encargo es el que reciben los modelizadores de la fase 2; se versiona para que se pueda auditar.

## Qué se pide
Para cada estimación de V8, V9, V12, V15 y V16 publicada SIN inferencia porque su herramienta no pasó el Monte Carlo (o publicada
solo como descriptiva), calcular la inferencia que usaría un trabajo publicado estándar y ponerla junto a la distorsión medida:

- **Errores convencionales.** Robustos agrupados al nivel del tratamiento. Wild cluster bootstrap con pesos de Webb (B = 9.999,
  SEED = 20261010) cuando hay menos de 40 clusters. Driscoll-Kraay en paneles con dependencia transversal. Newey-West en series
  (retardo de Newey-West 1994). Conley con el mismo radio si el diseño original era espacial. AKM0 o Borusyak-Hull-Jaravel en
  shift-share. Anderson-Rubin y F efectivo de Montiel Olea-Pflueger si hay instrumento.
- **Distorsión.** El tamaño real del contraste al 5 % nominal medido en el Monte Carlo del repositorio
  (docs/v16/validacion_montecarlo.md y output/v16/montecarlo/, y los de V15 en docs/v15). Se toma el de la herramienta y el escenario
  más parecido al diseño; se dice cuál. Si no hay Monte Carlo para esa herramienta, «sin medir».
- **Regla de publicación.** Si el tamaño real supera el 15 %, la inferencia convencional NO se publica: la fila se marca «no fiable»
  y solo lleva la estimación puntual. Si está entre el 5 % y el 15 %, se publica con la frase «p = x; el contraste rechaza un y %
  de las veces bajo la nula».
- **B3.** Ajuste por familia de pregunta (Holm y BH dentro de cada pregunta, nunca entre preguntas), como sensibilidad junto al
  ajuste original del proyecto.

## Reglas
- Misma muestra, misma especificación y mismo estimador puntual que el resultado publicado: solo cambia la inferencia. Se comprueba
  que la estimación puntual reproduce la publicada (tolerancia 1e-6 relativa); si no, se dice y se explica.
- No se leen data/sealed, las muestras selladas de V15 y V16 ni las filas muestra_sellada_v6 (filtrar siempre). No se ejecuta
  evaluate_*. No se modifican scripts ni salidas de versiones anteriores: se importan funciones o se copia la preparación de datos
  en src/v17/.
- Determinista: SEED = 20261010; sin red.
- Nada cambia de capa: la lectura convencional va en su propia columna y todo se rotula «a posteriori».

## Salida de cada grupo
- `src/v17/f2_inferencia_<grupo>.py`
- `output/v17/lectura_bde/<grupo>/inferencia.csv`, con estas columnas:
  `version, id_resultado, pregunta, estimacion_publicada, estimacion_reproducida, unidad, capa_proyecto, inferencia_original,
  metodo_convencional, n_clusters, se_conv, p_conv, ic95_lo, ic95_hi, herramienta_mc, tamano_real, fuente_mc, publicable,
  p_holm_pregunta, p_bh_pregunta, frase, nota`
- `output/v17/lectura_bde/<grupo>/resultado.json` (formato del proyecto, con "nota": "a posteriori")
- `output/v17/lectura_bde/<grupo>/informe.md`, que empieza por «Análisis a posteriori (V17).»
- Un test en `tests/v17/test_f2_<grupo>.py` que compruebe la reproducción del punto y la regla del 15 %.

Devolver: rutas, resumen de 200 palabras como máximo y tokens.
