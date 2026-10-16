# GitHub Pages desde el repositorio nuevo (vivienda-espana-evidencia)

La web se construye con .github/workflows/pages.yml, que va en el árbol público tal cual.

## Qué hace el workflow (V14.2)
1. Se ejecuta en cada push a `main` y a mano («Run workflow»).
2. Instala requirements-web.txt.
3. **Trae los datos.** En el repositorio nuevo data/ no se versiona, así que, si falta data/base/publica/hechos.parquet, ejecuta `python src/v14/datos.py`. Ese script:
   - descarga el paquete del depósito desde `zenodo_url_paquete` de proyecto.json;
   - verifica cada sha256;
   - copia solo data/.

   El paquete se guarda en la caché de Actions (`_descarga/`, con una clave que depende de proyecto.json).
4. Construye el monitor (`src/v10/monitor.py --sin-red`) y la web (`src/v10/web.py`), y despliega web/_site en Pages.

Mientras `zenodo_url_paquete` sea «PENDIENTE», el paso de datos falla con un mensaje claro y no se publica nada. Por eso la web se activa después del punto 4 de tareas_autor.md (DOI y URL del paquete).

## Configuración (una vez, en GitHub)
1. Repositorio Phraselium/vivienda-espana-evidencia → Settings → Pages → Build and deployment → Source: **GitHub Actions**.
2. Los permisos van en el propio workflow (`contents: read`, `pages: write`, `id-token: write`); no hace falta cambiar nada en Settings → Actions.
3. Tras subir proyecto.json con la URL del paquete, lance el workflow: Actions → web → Run workflow. También se lanza solo con el push.
4. Compruebe https://phraselium.github.io/vivienda-espana-evidencia/: el pie debe decir «Versión 1.0» y mostrar el DOI.

## Prueba en local
- **Repositorio de desarrollo** (2026-10-16, con los datos presentes): `make web` construyó 324 páginas, 27 indicadores, 4 mapas y 311 fichas territoriales (77,0 MB).
  - La descarga hechos.parquet no lleva variables `aeat_*` (terceros_1_0.aeat = excluir).
  - Lleva publicacion/cifras_no_publicadas_1_0.csv.
- **Árbol público** (bloque 5 de V14.2, origen e023bf6): `make datos` con el paquete copiado a mano en `_descarga/` y después `make web`. Resultado: 324 páginas y git sin cambios (docs/v14/arbol_1_0.md). Es lo mismo que hace el workflow, salvo la descarga desde Zenodo, que necesita la URL del punto 4.

Para probarlo en su máquina:
```bash
cd vivienda-espana-evidencia
mkdir -p _descarga && cp -r <ruta>/_deposito/vivienda-espana-evidencia-1.0 _descarga/
make datos && make web
python3 -m http.server -d web/_site 8000   # http://localhost:8000
```
