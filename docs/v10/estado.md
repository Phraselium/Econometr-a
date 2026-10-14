# Estado V10-DIFUSIÓN (para retomar con `claude --continue`)

Rama local `r10/difusion` → remota `claude/housing-price-spain-econometric-95dhj3`.

## Hecho
- **B1, base única** (D1):
  - `make base` con src/v10/geo.py y src/v10/base.py: 5,27 M filas (5,21 M públicas), 187 variables y 55.664 territorios;
  - geometrías en data/base/geo/;
  - tests en tests/v10/test_base.py.

## Siguiente paso exacto
- **B2, atlas descriptivo** (src/v10/atlas.py → output/v10/atlas/ y publicacion/atlas_descriptivo.md):
  - a) ECV y EPA: esfuerzo, sobrecarga, hacinamiento y tenencia, con IC del diseño muestral;
  - b) IPVA de contratos nuevos frente a existentes;
  - c) València por sección y barrio;
  - d) Comunitat Valenciana por municipio y España por provincia;
  - e) ciudades comparables.

## Subagentes
- Ninguno.
