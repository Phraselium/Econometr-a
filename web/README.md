# web/: sitio público (GitHub Pages)

- `make web` construye el sitio en `web/_site` (no versionado) con `src/v10/web.py`.
- Usa plantillas Jinja2 (`plantillas/`), CSS y JS propios (`src/`) y librerías vendorizadas (`vendor/`: Observable Plot, D3 y Leaflet, con sus licencias). Se construye sin red y, al navegar, no hace peticiones a terceros.
- Despliegue: `.github/workflows/pages.yml`, en cada push a `main`. El autor debe activar Pages con origen «GitHub Actions».
- URL prevista: https://phraselium.github.io/vivienda-espana-evidencia/
- Solo publica datos redistribuibles (`data/base/publica`) y agregados propios. Cada cifra, gráfico y mapa muestra su capa, su fuente y la fecha del dato.
