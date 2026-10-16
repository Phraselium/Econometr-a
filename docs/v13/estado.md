# V13 · Estado (consolidación para la versión pública 1.0)

Sin análisis nuevo: ningún modelo, ninguna muestra sellada, ninguna cifra de cifras_clave cambia (src/v13/check_v13.py).

## Hecho
- **A · Coherencia de las puertas de entrada.**
  - Inventario y tabla de discrepancias en docs/v13/coherencia.md: 35 declaraciones en las puertas generadas, más README, CLAUDE.md, CITATION.cff y .zenodo.json.
  - Versión pública 1.0, con la tabla de correspondencia v1-V13 en CHANGELOG.md.
  - proyecto.json es la fuente única de la versión y de las URL. Lo leen render v5, consulta, web y `make metadatos`.
  - URL del repositorio: 19 apariciones, todas con el nombre nuevo; ahora salen de proyecto.json o las comprueba el check.
  - CLAUDE.md: cabecera reescrita, sin quitar ninguna regla (se añaden las de V9-V13).
  - src/v13/check_v13.py entra en `make check`: versión vigente única, URL única, metadatos al día y cifras sin cambios (1.207 huellas).

## Siguiente

## Tokens de subagentes
Ninguno.
