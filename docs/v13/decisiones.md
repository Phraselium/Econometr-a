# V13 · Decisiones

## D1. Versión pública única y fuente única de metadatos
- La versión pública es la **1.0** (16-10-2026). v1-V12 pasan a versiones internas de desarrollo; la correspondencia está en CHANGELOG.md.
- La versión pública, la fecha, la URL del repositorio, la web y el DOI se configuran solo en `proyecto.json`. Lo leen src/v5/render.py
  (marcadores `{{proyecto.<campo>}}` en docs/v5/plantillas), src/consulta/generar.py, src/v10/web.py y src/v13/metadatos.py
  (genera CITATION.cff y .zenodo.json; `make metadatos`, también dentro de `make publicacion`).
- Se eligió un fichero JSON en lugar de una variable del Makefile porque lo leen scripts de Python y plantillas, no solo make.
- README.md, LEEME_PRIMERO.md, CLAUDE.md y README_REPLICACION.md se escriben a mano (son puertas de entrada legibles); check_v13
  comprueba que declaran la versión pública y la URL configuradas.
- En los entregables, «versión de referencia vX» pasa a «versión interna vX» cuando se refiere a un tema; la frase «versión de
  referencia / vigente / pública / de consulta N» queda reservada a la versión pública. check_v13 lo hace cumplir.
