# Estado V10-DIFUSIÓN (para retomar con `claude --continue`)

Rama local `r10/difusion` → remota `claude/housing-price-spain-econometric-95dhj3`.

## Hecho
- **B1, base única** (D1):
  - `make base` con src/v10/geo.py y src/v10/base.py: 5,27 M filas (5,21 M públicas), 187 variables y 55.664 territorios;
  - geometrías en data/base/geo/;
  - tests en tests/v10/test_base.py.

- **B2, atlas** (D3): `make atlas` → output/v10/atlas/ (11 tablas) y publicacion/atlas_descriptivo.md (12 hallazgos).
- **B3, figuras** (D4): `make figuras` → figuras/ (14 figuras en 3 formatos, con fichas).

- **B4, web** (D6): `make web` → web/_site; 320 páginas; tests en tests/v10/test_web.py; .github/workflows/pages.yml.
- **B5, monitor** (D7): src/v10/monitor.py (12 series); .github/workflows/actualizar.yml.
- **D5:** licencias de la capa pública corregidas (Registradores fuera).

## Siguiente paso exacto
- **B6, paquete académico:**
  - paper/ en Quarto (.qmd), con tablas y figuras de la base y la bibliografía de docs/v9_prep/referencias.bib;
  - publicacion/tablas_atlas.xlsx, mediante output/v10/tablas_atlas.xlsx y `make publicacion`.
- **B7, orden del repositorio:** historico/ e índice; README, LEEME_PRIMERO, llms.txt y consulta/.
- **Cierre:** revisor y resumen.

## Subagentes
- Ninguno.
