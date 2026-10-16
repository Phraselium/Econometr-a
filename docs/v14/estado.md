# V14 · Estado (publicación de la versión 1.0)

Sin análisis nuevo. Ningún modelo estimado, ninguna muestra sellada abierta ni regenerada y ninguna cifra de cifras_clave cambiada (check_v13).

## Hecho
- **Bloque 0 · Verificación del incidente D3.**
  - Los registros de acceso no cambian desde a58b426: no hay entradas nuevas.
  - La partición versionada es idéntica.
  - No se pudo comparar el sha256 de data/sealed: el entorno deniega su lectura y no hay huellas previas.
  - Queda documentado en ERRATA.md, en metodologia (desviaciones) y en D3.
  - Nueva regla en CLAUDE.md y control src/v14/check_v14.py en `make check` (heredocs sin comillas).
- **Bloque 1 · Árbol público 1.0** (docs/v14/arbol_1_0.md).
  - `make arbol_publico` crea un repositorio nuevo con un único commit, «Versión 1.0».
  - Tamaño: 46,1 MiB de pack git; 125 MB de árbol sin datos, en 3.000 ficheros.
  - `make datos` trae data/ del depósito (o de `_descarga/`) y verifica los sha256.
  - Prueba sin red, con el paquete copiado a mano:
    - `make datos`: 705 ficheros y 0 problemas;
    - `make check`: 316 tests superados y 59 omitidos por faltar datos de terceros; todos los controles sin errores y git sin cambios;
    - `make publicacion`: sin cambios.
  - Rutas y datos personales: se eliminó la ruta local de src/v10/fetch_geo.py; el árbol sale limpio.
- **Bloque 2 · Decisiones.**
  - D2: resuelta por el árbol nuevo.
  - D4 (AEAT): sigue excluida; el aviso legal reserva los derechos. Procedimiento para una 1.0.1 en tareas_autor.md.
  - D5: 15 tablas redactadas. La búsqueda por cabeceras y por valores de muestra no encuentra ninguna serie de terceros.
- **Bloque 3 · Revisión externa.** `make muestra_revision`: 40 cifras (C1 10, C2 9, C3s 10, C4 11), determinista. Hoja xlsx y guía.
- **Bloque 4 · Pasos del autor.** docs/v14/tareas_autor.md, del 1 al 8.

## Siguiente
- V14 cerrada en este repositorio. Lo que queda es del autor: docs/v14/tareas_autor.md, puntos 1 a 8.
- El árbol se probó generado desde cb19106. Los commits posteriores solo cambian docs/v13, docs/v14 y consulta/. El autor lo
  regenera desde el commit final con `make arbol_publico` (punto 2).

## Tokens de subagentes
Ninguno.

## V14.1 · Ajustes de cierre (2026-10-16)
- **Bloque 1 · Integridad de la muestra sellada.**
  - proyecto.json `hash_sellado`: valor PENDIENTE (lo calcula el autor), fecha 2026-10-16 y comando.
  - Sección «Integridad de la muestra sellada» en docs/v7_1/evaluacion_2027.md, con marcadores `{{proyecto.hash_sellado.*}}` que rellena `make publicacion`.
  - check_v14 da un aviso en este repositorio y un error en el árbol público mientras el valor siga pendiente.
- **Bloque 3 · Cifras que dependen de terceros.** docs/v14/cifras_terceros.{md,csv} (src/v14/cifras_terceros.py): 254 cifras distintas, 409 filas fuente × cifra.
  - Notariado: 6 directas y 151 técnicas.
  - Registradores: 56 directas, 35 indirectas (el modelo usa la serie) y 151 técnicas.
  - AEAT: 5 directas y 5 indirectas vía estadística oficial (IPVA, SERPAVI).
  - Al final, las URL de las condiciones de uso, sin interpretar.
- **Hallazgo y corrección:** la redacción de tablas no miraba los .csv.gz. output/v6/M0/paneles/prov_compra_anual_train.csv.gz llevaba 2 columnas de Registradores. Ahora src/v14/terceros.py revisa también los .gz y reconoce «registr» como palabra: 16 tablas redactadas.

