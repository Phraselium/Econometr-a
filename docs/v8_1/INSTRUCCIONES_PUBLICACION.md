# Cómo publicar el proyecto en GitHub y obtener el DOI (V8.1)

Esta guía es para el autor. Explica, paso a paso y en lenguaje llano, cómo dejar el repositorio publicado con su nombre definitivo, sus versiones etiquetadas y un DOI de Zenodo. Todo lo hace un guion, `docs/v8_1/publicacion_github.sh`, que **pregunta antes de cada acción que no se puede deshacer**. Si respondes cualquier cosa distinta de «s», ese paso no se ejecuta.

## Qué necesitas

- Tu ordenador, con `git`, `gh` (la herramienta de GitHub), `python3`, `make` y `curl`.
- `gh` con tu sesión iniciada: `gh auth login`. Compruébalo con `gh auth status`.
- Una cuenta en Zenodo vinculada a tu GitHub: zenodo.org, «Log in with GitHub».
- Un clon **completo** del repositorio. Si lo clonaste con `--depth`, el guion se detendrá. Lo arreglas con `git fetch --unshallow`.
- Conexión a internet. En la fase 2 el guion descarga los datos de terceros que ya no están en el repositorio y ejecuta `make check`, que tarda unos minutos.

## Por qué hay dos fases

Zenodo archiva **para siempre** cada release que se publica mientras está activado, y le asigna un DOI. Las versiones antiguas (pre-registros, v7.0 y v8.0) deben tener su release en GitHub, pero no queremos un DOI para cada una. Así queda:

- **Fase 1**, con Zenodo **desactivado**: se ordena el repositorio y se publican las versiones antiguas.
- **Pausa**: activas Zenodo.
- **Fase 2**, con Zenodo **activado**: se publica la v8.1, que es la que recibe el DOI, y se anotan las fechas.

## Fase 1 (Zenodo desactivado)

1. Ve a https://zenodo.org/account/settings/github/ y comprueba que el interruptor del repositorio está **apagado**.
2. En tu ordenador, dentro del clon y en la rama de trabajo actualizada (`git fetch origin`), ejecuta:

   `bash docs/v8_1/publicacion_github.sh fase1`

3. El guion comprueba que el clon no es superficial y que existen los commits que se van a etiquetar. Después te pregunta, de uno en uno:
   - **Renombrar** el repositorio a `vivienda-espana-evidencia`. GitHub redirige automáticamente el nombre antiguo, así que los enlaces viejos siguen funcionando.
   - **Crear la rama `main`** con el estado final y subirla, sin reescribir nada.
   - **Poner `main` como rama por defecto.**
   - **Crear y publicar las etiquetas:**

     | Etiqueta | Commit |
     |---|---|
     | prereg-v7 | 3fad305 |
     | v7.0 | 3d1170c |
     | v7.1 | 7415932 |
     | prereg-v8 | 91e618b |
     | v8.0 | 5c68973 |
     | v8.1 | el estado final de `main` |

   - **Crear las releases antiguas**: prereg-v7, v7.0, prereg-v8 y v8.0. Ninguna se marca como «latest».
4. Al final verás la fecha de publicación de cada release y un mensaje de **PAUSA**.

## Pausa: activar Zenodo

Vuelve a https://zenodo.org/account/settings/github/ y **enciende** el interruptor del repositorio (con su nombre nuevo). Si no aparece, pulsa «Sync now».

## Fase 2 (Zenodo activado)

1. Ejecuta:

   `bash docs/v8_1/publicacion_github.sh fase2`

2. El guion te pregunta antes de **crear la release v8.1**, que se marca como «latest». Zenodo la archiva y le da un DOI.
3. Espera hasta diez minutos y busca el DOI en Zenodo. Si no aparece, sigue con el DOI como «PENDIENTE»; puedes añadirlo después volviendo a ejecutar la fase 2 (la release ya creada no se duplica: responde «N» a esa pregunta).
4. Te pregunta antes de **escribir** las fechas y el DOI:
   - La **fecha verificable** de cada pre-registro es la fecha de publicación de su release en GitHub (prereg-v7 y prereg-v8). Es una marca externa e independiente del repositorio. Se escribe en `docs/v7/notas_release.md` y `docs/v8/notas_release.md`.
   - El **DOI** de v8.1 va en esas mismas notas, en `CITATION.cff`, en `README.md` (con su insignia) y en `consulta/version.json` (este último lo regenera `make consulta`).
5. Regenera `consulta/` y `publicacion/` y comprueba que `make evaluate_v8` **acepta ya la fecha**. No evalúa nada: la evaluación real se hace en 2027, cuando se publiquen los datos de 2026T3-2027T2.
6. Ejecuta `make check` y, si todo pasa, hace un commit. Te pregunta antes de **subirlo a `main`**.
7. Por último, lista las ramas de trabajo que ya están contenidas en `main` y te pregunta **una por una** si quieres borrarlas. Si dudas, responde «N»: no pasa nada por dejarlas.

## Si algo sale mal

- **Interrumpir es seguro.** Puedes cortar el guion en cualquier momento (Ctrl+C) y volver a ejecutar la misma fase. Los pasos ya hechos se detectan (etiquetas existentes) o puedes saltarlos respondiendo «N».
- **Una release de prueba con Zenodo activado** genera un DOI que no se puede borrar. Por eso las versiones antiguas se publican en la fase 1, con Zenodo apagado.
- **Datos de terceros.** Los ficheros retirados (docs/v8_1/datos_retirados.md) siguen en el historial de las ramas antiguas. No se reescribe el historial. Si quieres eliminarlos también de ahí, hace falta `git filter-repo` y un force-push: es una decisión aparte y conviene tomarla antes de activar Zenodo.
- **El fichero `data/raw/v4/medidas_programas.csv`** ya no se publica (aplazado a la fase de propuestas). Guarda tu copia local: `make all` la necesita para el módulo v5 A5.
