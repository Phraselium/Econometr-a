# Tareas del autor (V10)

Ninguna de estas acciones puede hacerse desde la sesión de trabajo. Están en orden.

1. **Crear `main` y ponerla por defecto.**
   - Fusionar la rama de trabajo (`claude/housing-price-spain-econometric-95dhj3`) en `main`, o crear `main` desde ella.
   - Después: Settings → Branches → Default branch → `main`.
   - El script de V8.1 (docs/v8_1/publicacion_github.sh, fase 1) ya hace este paso con confirmación.
2. **Activar GitHub Pages.**
   - Settings → Pages → Build and deployment → Source: «GitHub Actions».
   - El primer push a `main` que toque `data/base`, `output/v10`, `figuras`, `web` o `publicacion` lanza `.github/workflows/pages.yml`; también se puede lanzar a mano desde Actions → web → Run workflow.
   - URL prevista: https://phraselium.github.io/vivienda-espana-evidencia/
3. **Permisos de Actions** para el monitor.
   - Settings → Actions → General → Workflow permissions: «Read and write» y «Allow GitHub Actions to create and approve pull requests».
   - Sin esto, `.github/workflows/actualizar.yml` no puede abrir el pull request mensual.
4. **Revisar el primer pull request del monitor.**
   - Se lanza el día 3 de cada mes, o a mano: Actions → actualizar → Run workflow.
   - Comprobar el resultado de `make check` en el cuerpo del PR, las series con «posterior al pre-registro: sí» (solo descriptivas) y los fallos de descarga.
   - Fusionar solo si todo es correcto.
   - Si cambian las fianzas de la GVA respecto a data/raw/v5, el test de comparación fallará a propósito: revisar antes de aceptar.
5. **Releases y DOI.**
   - Seguir docs/v8_1/INSTRUCCIONES_PUBLICACION.md: fase 1, etiquetas y releases antiguas; fase 2, release v8.1 con Zenodo.
   - Para V10 se propone una release `v10.0` después de v8.1, con el mismo procedimiento: Zenodo genera un DOI nuevo por release.
   - Escribir el DOI en docs/v8/notas_release.md. `make consulta` y `make web` lo propagan a consulta/version.json y al pie de la web.
6. **Datos que quedaron pendientes** (V9-DATOS-COMPLETO, bloques 1-9, aplazados; docs/v9/estado_datos.md):
   - Catastro INSPIRE por sección (antigüedad y usos del parque);
   - GTFS (accesibilidad);
   - ediciones históricas de Inside Airbnb (petición del autor);
   - afiliación municipal.
   - Si se quiere usar la Wayback Machine para recuperar cortes antiguos de registros, hay que añadir web.archive.org a los dominios permitidos del entorno.
7. **Historial de git.** Los commits bc0f83b y 4e0c4a8 contienen, en data/base/publica/hechos.parquet, dos variables agregadas del Colegio de Registradores (docs/v10/decisiones.md, D5). La versión actual ya no las publica.
   - Si el autor quiere eliminarlas también del historial, tendría que reescribirlo él mismo (no se ha hecho).
   - Basta con no fusionar esos commits por separado: la fusión de la rama trae el estado final.
8. **Manuscrito.** Instalar Quarto y ejecutar `quarto render paper/manuscrito.qmd`. Las secciones de v9 están marcadas [PENDIENTE].
