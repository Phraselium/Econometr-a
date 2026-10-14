# Estado V10-DIFUSIÓN (para retomar con `claude --continue`)

Rama local `r10/difusion` → remota `claude/housing-price-spain-econometric-95dhj3`.

## Hecho
- **B1, base única** (D1):
  - `make base` con src/v10/geo.py y src/v10/base.py: 5,27 M filas (5,21 M públicas), 187 variables y 55.664 territorios;
  - geometrías en data/base/geo/;
  - tests en tests/v10/test_base.py.

- **B2, atlas** (D3): `make atlas` → output/v10/atlas/ (11 tablas) y publicacion/atlas_descriptivo.md (12 hallazgos).
- **B3, figuras** (D4): `make figuras` → figuras/ (14 figuras en 3 formatos, con fichas).

## Siguiente paso exacto
- **B4, web estática** en web/: generador en Python (src/v10/web.py) con Observable Plot y Leaflet vendorizados en web/vendor/.
  - Secciones: Inicio, Indicadores, Mapas, Fichas territoriales, Quién lo sufre, Verificador, Metodología y datos, Historial y Monitor.
  - Despliegue: .github/workflows/pages.yml.
- **B5, monitor:** .github/workflows/actualizar.yml.

## Subagentes
- Ninguno.
