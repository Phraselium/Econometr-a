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
- **B · Datos fuera de git y depósito.**
  - docs/v13/datos_deposito.md: tamaño de data/ por carpeta (≈ 12 GB en disco, 1.212 MB versionados).
  - Clases (a)/(b)/(c) con licencia y fuente. Detalle por fichero en docs/v13/datos_inventario.csv (src/v13/inventario_datos.py).
  - `make paquete_zenodo` (src/v13/paquete_zenodo.py): ensayo con 3.760 ficheros y 1.322 MB; CHECKSUMS verificados; sin data/sealed.
    La capa pública va sin las 7 variables AEAT (D4).
  - Propuesta para sacar data/raw del árbol: D2, pendiente del autor.
  - `make datos_terceros` ya no reescribe ficheros versionados; probado con descarga real (tarea 2 de V12).
  - Hallazgos para el autor: D4 (AEAT) y D5 (derivados con Notariado y Registradores).
  - Incidencia D3: un heredoc sin comillas ejecutó `make clean` y el inicio de `make all`. Detenido; sin cambios en git ni en
    cifras; ninguna muestra sellada evaluada.
- **C · Pre-registro.**
  - 18 etiquetas locales: 9 prereg-* y 9 de versión, con commit, fecha, tipo y sha256 del documento.
  - Ninguna existe en el remoto (`git ls-remote --tags` devuelve 0), pero todos sus commits sí están en la rama remota.
  - Comandos exactos de publicación y texto del registro en OSF en docs/v13/tareas_autor.md. Todo «pendiente del autor».
- **D · Una página legible.**
  - Plantilla docs/v5/plantillas/una_pagina.md reescrita: frases de menos de 25 palabras (comprobado: 0 de 25 o más).
  - Cifras redondeadas con el rango al lado mediante dos campos nuevos de render, `breve` y `rango_breve`, que no tocan cifras_clave.
  - Capa entre corchetes; notas técnicas en enlaces a las fichas del anexo (A1, A2, A5, A7-A10, A14, B7 y B10) o al documento técnico de V7.1, V7.2 y V8.
  - Mismos 29 ids de cifras_clave; check_v13 confirma que no cambia ninguna cifra.
  - El registro de `make datos_terceros` pasa a data/descargas_terceros/, fuera de data/raw: dentro, check_v5 lo tomaba por una lectura no versionada.

## Siguiente

## Tokens de subagentes
Ninguno.
