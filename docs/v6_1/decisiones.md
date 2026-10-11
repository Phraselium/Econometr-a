# Decisiones v6.1

- **D1 · Rama y rutas.** La rama es `r6.1/main`, creada desde 08d7629. Lo nuevo va en src/v6_1/, output/v6_1/ y docs/v6_1/.
- **D2 · Correcciones a versiones cerradas.** Solo se tocan los ficheros de v1-v6 si la auditoría K4 encuentra un error. Cada corrección que cambie una cifra publicada va a ERRATA.md.
- **D3 · K1 y la muestra sellada.** Las líneas base nuevas abren la muestra sellada v6 con identificadores nuevos de evaluate_v6, una vez por línea base y con prefijo `k1_`.
  - Lo hace un script src/v6/m4_lineas_base.py (el nombre m4_ es el que permite check_v6), que queda fuera de make como m4_sellado.py.
  - El reanálisis que sí entra en make (src/v6_1/k1_run.py) lee solo los JSON versionados de las predicciones.
  - Se declara que esto supone una segunda mirada a la misma muestra para nuevos comparadores, no para los modelos ya evaluados: sus predicciones selladas no cambian.
