# Instrucciones comunes para la redacción de entregables v5 (módulo E)

Autor: **Borja Romero, economista** (firma individual, independiente). Idioma: español. El working paper y los artículos llevan además el resumen en inglés.

## Regla de oro: ninguna cifra tecleada
- Los entregables se escriben como PLANTILLAS en `docs/v5/plantillas/<ruta>.md`. `python3 src/v5/render.py` las rellena en `output/v5/<ruta>.md`.
- Toda cifra va como marcador de output/v5/cifras_clave.csv (tabla legible en output/v5/cifras_clave.md):
  - `{{id}}`: valor + unidad + rango;
  - `{{id:valor}}`, `{{id:rango}}`, `{{id:min}}`, `{{id:max}}`, `{{id:num}}`: partes sueltas;
  - `{{id:periodo}}`, `{{id:fuentes}}`, `{{id:capa}}`, `{{id:fecha_dato}}`, `{{id:cobertura}}`;
  - `{{id:cita}}`: «valor (periodo; fuentes; dato de fecha; capa)».
- `python3 src/v5/check_v5.py` rechaza cualquier dígito de una plantilla que no esté en un marcador. Están permitidos los años, los identificadores como C1, BK-002, H-B3-6 o Ley 12/2023, la numeración de listas, las rutas entre `backticks` y los enlaces.
- Si una línea necesita de verdad un número libre que no es una cifra del análisis, por ejemplo «20 minutos» en el guion o el número de una diapositiva, se marca con el comentario `<!-- check:cifra-libre -->` en esa línea. Úsalo lo menos posible.
- Si falta una cifra en cifras_clave, NO la teclees. Añádela a `src/v5/e_hechos.py`, que lee el valor de un JSON o CSV de output/v5 o output/v4 y escribe `output/v5/E/hechos.json` con el formato estándar ({id, indicador, valor, min, max, unidad, periodo, cobertura, fuentes, capa, fecha_dato}). Después ejecuta `python3 src/v5/cifras_clave.py`. Cada id nuevo empieza por `E-`. Coordina con los otros redactores: cada uno añade sus funciones a e_hechos.py sin borrar las de los demás.

## Capas y lenguaje
- Cada afirmación lleva su capa entre corchetes: [C1], [C2] o [C4]. No hay ninguna C3.
- En titulares de E4 (artículo del Colegio), E6 (una página) y E8 (LinkedIn) solo van C1 y C2. Lo C4 va en «probable pero no demostrado» o en el recuadro de lo que no se puede afirmar.
- Nada de lenguaje causal por debajo de C3: ni «se debe a», «causa», «provoca», «explica» (como atribución), «gracias a» ni «efecto». Se usa «se asocia», «coincide», «como máximo», «es compatible con».
- Neutralidad estricta: se evalúan afirmaciones e instrumentos, nunca partidos ni personas. Sin nombres de partidos ni de políticos y sin adjetivos de juicio. `python3 src/v3/check_texto.py` debe dar 0 errores.
- Si dos métodos discrepan, se dan los dos. Los negativos se reportan. Cada cifra lleva su periodo y, en los textos divulgativos, la fuente y la fecha (usa `:cita`).

## Fuentes de contenido (no reestimes nada)
- Resultados de los módulos: output/v5/<MÓDULO>/resultado.json, tablas y figuras; docs/v5/decisiones.md; docs/v5/backlog.md; las revisiones docs/v5/revision_*.md.
- La matriz de instrumentos (output/v5/D1/matriz_instrumentos.md), la política por territorio (output/v5/D2/politica_territorio.md) y la convergencia (output/v5/D3/convergencia.md).
- El verificador: output/v5/verificador/verificador.md.
- Lo heredado de v4: output/v4/*.md. Reutiliza la estructura, sin copiar las cifras: van en marcadores.
- La literatura: docs/literatura.md (con el anexo v5) y docs/v5/literatura_instrumentos.md. Solo VERIFICADA con DOI y cuartil; el resto se marca NO VERIFICADA.
- Las figuras se enlazan con rutas relativas a output/v5 (por ejemplo `![](B1/figuras/B1_mapa_necesidad.png)`).

## Al terminar
- `python3 src/v5/render.py`: 0 marcadores sin resolver.
- `python3 src/v5/check_v5.py` y `python3 src/v3/check_texto.py`: 0 errores.
- No hagas commit. Devuelve las rutas, un resumen de ≤200 palabras y los tokens.
