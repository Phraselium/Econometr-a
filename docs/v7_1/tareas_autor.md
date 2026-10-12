# Tareas del autor tras V7.1 (por urgencia)

Sustituye a docs/v7/tareas_autor.md y a historico/docs/v6_1/tareas_autor.md. docs/v6_2/tareas_autor.md queda como histórico. Nada de esta lista lo puede hacer el agente: requiere credenciales, firma o juicio del autor.

## 1. Releases y Zenodo, ANTES del 4 de diciembre de 2026 (publicación del IPV 2026T3)

Es lo más urgente. Hasta que exista una fecha verificable externa, el pre-registro de V7 solo tiene la de una etiqueta local. Si el IPV 2026T3 se publica antes de la release, ese trimestre deja de ser limpio para la compra. Para el alquiler ya hay una sensibilidad declarada sin 2026T3 (docs/v7/desviaciones.md).

1. Desde una copia con permisos de escritura, publica las etiquetas locales, en este orden: `prereg-v7` (3fad305), `v7.0` (3d1170c) y `v7.1` (commit de cierre de V7.1). Opcionalmente, también las anteriores: prereg-v2, prereg-v3, prereg-v5, prereg-v6, v5.0, v5.1, v6.0, v6.1 y v6.2. El remoto de esta sesión rechaza las etiquetas.
2. Crea una release de GitHub por etiqueta, con el texto de docs/v7_1/release_notes.md.
3. Activa la integración con Zenodo y obtén el DOI de `prereg-v7` y el de `v7.1`. Anota la fecha del DOI de `prereg-v7` en docs/v7/notas_release.md (`fecha_verificable:`) y los DOI en CITATION.cff, .zenodo.json y README.md.

## 2. Revisión externa con la guía actualizada

- Envía metodologia/guia_revisor.md a, como mínimo, un econometrista de panel (nota metodológica, regla de triangulación, Monte Carlo) y un economista de vivienda (déficit, necesidad, dosis y coste).
- Pide comentarios con referencia a fichero y línea. Las respuestas van a una carta pública y, si cambian cifras, a ERRATA.md.

## 3. Replicación humana de las cifras difundibles

- Reproduce a mano, con metodologia/anexo_metodologico.md y data/raw, al menos tres cifras de publicacion/cifras_clave.csv de capa C1 o C2.
- Comprueba una fila de dosis y coste (publicacion/dosis_coste.csv) con output/v7_1/S1/resumen.md.
- Ejecuta `make all`, `make v7`, `make publicacion` y `make check` en una máquina propia, y anota tiempos y diferencias.

## 4. Licencias y declaración de IA

- Revisa LICENSE (MIT para el código y CC BY 4.0 para los textos) y docs/v5/licencias_datos.md, que recoge la licencia de cada fuente de data/raw.
- Revisa y firma DECLARACION_IA.md. Confirma que el apéndice C del working paper y la nota metodológica la recogen.
- Verifica en Scimago los cuartiles de las referencias marcadas «cuartil no verificado» y de las tres revistas propuestas (docs/v7_1/literatura_nota.md, con sus ISSN). Desde esta sesión Scimago devuelve 403. Si alguna referencia no se confirma, márcala o retírala antes de enviar la nota.

## 5. Artículo del Colegio

- Amplía la prosa de docs/v5/plantillas/articulo_colegio.md con los puntos de V7. Están en el comentario «NOTA PARA EL AUTOR» y en publicacion/que_cambio.md.
- Usa solo marcadores {{id}} de cifras_clave para las cifras. Después ejecuta `make v7_1`, `make publicacion` y `make check`.

## 6. Peticiones de datos

Están en docs/v5/solicitudes.md, sin respuesta registrada. Para completar la dosis y el coste y una futura V8 hacen falta:
- un coste unitario verificable de la vivienda pública y de la movilización de vacías (Ministerio, comunidades autónomas);
- los tipos vigentes de ITP e IVA por CCAA y fecha;
- la renta media del alquiler en euros y los hogares beneficiarios de ayudas al alquiler por CCAA;
- la renta disponible por CCAA;
- una serie de vacías por CCAA;
- la titularidad del parque (Catastro).

## 7. Fecha de ejecución de `make evaluate_v7`

- **Fecha recomendada:** segunda quincena de septiembre de 2027, después de la publicación del IPV 2027T2. El INE aún no ha publicado su calendario de 2027: confírmalo cuando lo haga.
- **Antes:** comprueba que `fecha_verificable` ya no es PENDIENTE y ejecuta el ensayo (`python3 src/v7_1/s4_ensayo.py`).
- **Después:** sigue reproducir/evaluacion_2027.md paso a paso y publica el resultado, sea cual sea, una sola vez.
