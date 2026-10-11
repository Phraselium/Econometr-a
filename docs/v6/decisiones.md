# Decisiones v6

## Setup y validación sellada
- Rama r6/main desde r5.1/main (bac2fda, v5.1).
- **Validación sellada nueva (holdout.py: `provincias_selladas_v6`, `sellar_v6`, `evaluate_v6`).**
  - Temporal: el último año disponible de cada panel.
  - Transversal: el 20 % de las provincias por bloques completos de CCAA, en orden aleatorio con SEED+6, sin las CCAA que contienen las provincias selladas en v2 (11, 16 y 45). Resultado: 07, 22, 26, 28, 30, 31, 33, 35, 38, 44 y 50 (Baleares, Aragón, La Rioja, Madrid, Murcia, Navarra, Asturias y Canarias; 11 de 52, 21 %).
  - Los municipios y distritos de esas provincias quedan sellados: una sola partición espacial (≈20 % en cada nivel), sin fuga entre niveles en los modelos jerárquicos.
  - Los distritos sellados en v3 se excluyen de todo uso en v6.
- **Limitación declarada: contaminación descriptiva.** El último año y todas las provincias se usaron de forma DESCRIPTIVA en v4-v5 (tasas, mapas, B3). La validación v6 es nueva para la estimación y la selección de modelos, pero no es una muestra que nadie haya visto nunca. Así se dirá en todos los resultados.
- `evaluate_v6` abre la muestra sellada UNA vez por modelo o hipótesis, y queda registrado en docs/v2/holdout_accesos.md.

## G (subagente)
- Pasan a archive/ (con git mv) los entregables de v3 y v4 que ningún script ni plantilla cita. informe_tecnico y lo_que_sabemos de v4 se quedan, porque las plantillas v5 los citan.
- Makefile: se añaden `a5_validacion` y `b3_potencia`, que producen ficheros versionados que leen otros scripts. Reproducen sus salidas byte a byte.
- Quedan pendientes para el autor (docs/v6/tareas_autor.md):
  - tres scripts de datos auxiliares fuera de `make data`;
  - las etiquetas;
  - la release y el DOI;
  - la autoría de los commits.

## Revisión de M0: REHACER (B1-B5)
- **B5, declaración** (orquestador). El corte temporal de v6 (el último año: 2025 en compra y 2024 en alquiler) cae dentro de la ventana sellada de v2 (2024Q3-2026Q2). Esa ventana se abrió 8 veces para las hipótesis confirmatorias de v2, y siempre para las 3 provincias selladas de v2 (11, 16 y 45).
  - Consecuencias:
    - el año de validación v6 NO es nuevo en el tiempo;
    - lo nuevo es la combinación de año y provincias: las 11 provincias v6 no se usaron nunca como validación;
    - las variables y especificaciones de v6 no se eligieron mirando su error en esa muestra.
  - Se declara en hipotesis.md y en todo resultado de M3/M4 como «validación espacial nueva; temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5».
- **B1-B4 y determinismo.** Los corrige el agente de M0:
  - un mismo corte temporal por mercado en todos los niveles;
  - las CCAA uniprovinciales se asignan a su provincia;
  - el pre-registro se cierra sin grados de libertad;
  - gzip con mtime=0.
