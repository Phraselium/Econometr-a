# paper/: manuscrito de trabajo (V10)

- `manuscrito.qmd`: manuscrito en Quarto con estructura de revista.
  - Toma las tablas de `output/v10/atlas` y de la base (`data/base/publica`), y las figuras de `figuras/paper`.
  - La bibliografía sale de `docs/v9_prep/referencias.bib`.
  - Las secciones de v9 están marcadas como **[PENDIENTE]**.
- Las cifras del texto se calculan con código en línea al renderizar; no hay ninguna escrita a mano.
- Para renderizar hacen falta Quarto (https://quarto.org) y Python con pandas y pyarrow. Desde `paper/`: `quarto render manuscrito.qmd`, que genera HTML y PDF.
  - En el entorno de V10 Quarto no estaba instalado: el manuscrito no se ha renderizado; `tests/v10/test_paper.py` comprueba su estructura.
