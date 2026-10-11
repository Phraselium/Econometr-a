# Decisiones v6.1

- **D1 · Rama y rutas.** La rama es `r6.1/main`, creada desde 08d7629. Lo nuevo va en src/v6_1/, output/v6_1/ y docs/v6_1/.
- **D2 · Correcciones a versiones cerradas.** Solo se tocan los ficheros de v1-v6 si la auditoría K4 encuentra un error. Cada corrección que cambie una cifra publicada va a ERRATA.md.
- **D3 · K1 y la muestra sellada.** Las líneas base nuevas abren la muestra sellada v6 con identificadores nuevos de evaluate_v6, una vez por línea base y con prefijo `k1_`.
  - Lo hace un script src/v6/m4_lineas_base.py (el nombre m4_ es el que permite check_v6), que queda fuera de make como m4_sellado.py.
  - El reanálisis que sí entra en make (src/v6_1/k1_run.py) lee solo los JSON versionados de las predicciones.
  - Se declara que esto supone una segunda mirada a la misma muestra para nuevos comparadores, no para los modelos ya evaluados: sus predicciones selladas no cambian.
- **D4 · Sellado tras K4a-02.** Corregir Incasòl cambia el sha256 de dos paneles sellados (`prov_contratos_nuevos_anual` y `mun_contratos_anual`).
  - m0_run.py los vuelve a escribir sin abrirlos, y sellado_info.json se actualiza.
  - Ningún modelo de M4 ni de K1 se evaluó sobre esos paneles: los contratos nuevos no se pudieron modelizar en v6 (N≈15).
  - Por tanto, ninguna evaluación sellada queda invalidada.
- **D5 · K4b en make.** k4b_run.py lee el CSV versionado de Catastro (.csv.gz) y no el descomprimido. El resultado es idéntico.
  - k4b_comparar.py se ejecuta tras cifras_clave.
- **D6 · Hallazgos medios y bajos de K4a (03-10).** Pasan al backlog de v6.1 con su coste. Se resuelven en K6 si son baratos.
