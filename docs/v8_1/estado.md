# Estado V8.1 (coherencia de V8, capa de consulta, datos de terceros y publicación en GitHub)

Rama de trabajo: r8.1/main (desde 5c68973, cierre de V8). Sin estimaciones nuevas ni muestras selladas.

## Hecho
- A (coherencia): lectura del multiverso por variables (18 de 200 combinaciones, frente a 2 de 74 por familias); la regla M0 del alquiler queda como «no evaluable»; avisos de colinealidad de la población y del signo del tipo real; remisión a contratos nuevos (C1); discrepancia de fuentes en València; frase de la parte no atribuida. V8 pasa a versión de referencia (README, CLAUDE.md, LEEME_PRIMERO, una_pagina, lo_que_sabemos y que_cambio). Ninguna cifra publicada cambia: sin ERRATA; CHANGELOG lo dice. Test de cifras superadas en tests/v8_1/test_v81.py.
- B (consulta): `make consulta` genera consulta/ (LEEME_ASISTENTE con 1.382 palabras, hallazgos.json con 1.192 registros, preguntas_frecuentes con 72 preguntas, glosario, indice_ficheros y version.json) y llms.txt. Tests en tests/consulta.
- C (datos de terceros): 75 ficheros salen del índice (docs/v8_1/datos_retirados.md); `make datos_terceros`. Descargas idénticas hoy.
- E (preparación): docs/v8_1/publicacion_github.sh. No se ha ejecutado nada en GitHub: en este entorno `gh` no está autenticado y el remoto rechaza las etiquetas.

## Siguiente paso exacto
- D: en curso. Clon limpio sin red con los datos retirados copiados: `make v8`, `make publicacion`, `make consulta` y `make check`. Después, comparar con lo versionado.
- E: el autor ejecuta docs/v8_1/publicacion_github.sh en local, confirmando cada paso.

## Tokens por bloque

| Bloque | Subagentes | Orquestador (estimación) |
|---|---|---|
| A coherencia | 243.316 | ~10k |
| B consulta | 219.968 | ~5k |
| C datos de terceros | 162.656 | ~8k |
| D y E | 0 | ~10k |
