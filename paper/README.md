# paper/: manuscrito de trabajo (V10)

- `manuscrito.qmd`: manuscrito en Quarto con estructura de revista.
  - Toma las tablas de `output/v10/atlas` y de la base (`data/base/publica`), y las figuras de `figuras/paper`.
  - La bibliografía sale de `docs/v9_prep/referencias.bib`.
  - La sección 6 recoge los diseños de V9 (cifras de `publicacion/cifras_clave.csv`, ids `V9-`; figuras de `output/v9`).
- Las cifras del texto se calculan con código en línea al renderizar; no hay ninguna escrita a mano.
- Para renderizar hacen falta Quarto (https://quarto.org) y Python con pandas y pyarrow. Desde `paper/`: `quarto render manuscrito.qmd`, que genera HTML y PDF.
  - En los entornos de V10 y V9 Quarto no estaba instalado (sin red para instalarlo): el manuscrito no se ha renderizado; `tests/v10/test_paper.py` comprueba su estructura.
