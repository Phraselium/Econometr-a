# V17 · Bloqueos y paradas

## P1. Parada E (2026-10-19): veredicto de las ayudas a la demanda
- **Qué conclusión.** Medida 5 de D1, «sin evidencia de mejorar la asequibilidad». También publicacion/informe_integral/informe_integral.md, III.8: «Asequibilidad del beneficiario: sin evidencia».
- **Qué muestra la auditoría.**
  - Ficha: output/v17/auditoria/filas/ayudas_demanda.md, sección 7.
  - El coste neto del beneficiario es la renta menos la ayuda, así que una traslación θ < 1 deja al beneficiario una mejora de (1 − θ) de la ayuda.
  - Siete estudios con diseño dan θ < 1, con una mediana de 0,46. Fack (2006), verificado en Crossref, da 0,78.
  - Con la regla de umbral de III.1, el veredicto sobre la asequibilidad del beneficiario de las ayudas al ALQUILER sería «prometedora».
  - Para los avales ICO, «sin evidencia» sigue siendo defendible.
- **Antecedente.**
  - En la tercera ronda del arbitraje de V16 (N5), III.8 pasó de «prometedora» a «sin evidencia».
  - El motivo fue que las referencias de L5 estudian la traslación al precio, no la asequibilidad del beneficiario, y que una simulación no es un estudio con diseño.
  - La auditoría sostiene que la traslación medida implica directamente la asequibilidad del beneficiario (es una identidad contable). Por eso esos estudios sí son evidencia con diseño sobre el objetivo declarado.
- **Qué no se ha hecho.** No se ha cambiado ningún fichero publicado. Decide el autor:
  - (a) corregir III.8 y la medida 5, con una entrada en ERRATA.md porque cambia un veredicto publicado;
  - (b) mantenerlo, explicando por qué;
  - (c) otra opción.

## P2. Parada E (2026-10-19): «no hay datos de titularidad»
- **Qué conclusión.** publicacion/lo_que_sabemos.md, sección «No se puede afirmar con estos datos», dice sobre qué parte del stock y del alquiler está en manos de empresas o grandes tenedores: «no hay datos de titularidad (solicitudes S1, S3 y S4)». Lo mismo dice la ficha V02 del verificador («Sin datos de titularidad por tamaño de tenedor») y la fila de discurso de D1 («no hay datos de titularidad para afirmarlo ni negarlo»).
- **Qué muestra la auditoría** (output/v17/auditoria/filas/grandes_tenedores.md, sección 7):
  - Para la parte del STOCK sí hay datos públicos: el Catastro, con la titularidad por tramos y por tipo de titular.
  - La propia 1.0 publica el 4,2 % en manos de titulares con más de diez viviendas, en publicacion/atlas_v12.md y en el informe integral, VII.7 (4,2 % y 2,1 % [C4]). El script de la auditoría lo reproduce: 4,16 % en 2026 y 4,30 % en 2025.
  - Es una contradicción interna de la 1.0: una página dice que no hay datos y otra publica la cifra.
  - Para la parte del ALQUILER no hay un dato nacional directo. Hay datos parciales: un 2,4 % del alquiler habitual en personas físicas con once o más viviendas (Banco de España); un 36 % del alquiler habitual de Barcelona ciudad (O-HB); y entre un 2 % y un 12 % con supuestos explícitos.
  - publicacion/una_pagina.md («no hay datos de titularidad suficientes») es matizable, no falsa.
- **Veredicto de la fila de discurso.** «Incorrecta»: los datos bastan para negar el «control» a escala nacional; Barcelona ciudad pesa mucho más; el efecto en los precios no está medido en España.
- **Qué no se ha hecho.** No se ha cambiado ningún fichero publicado. Decide el autor: (a) corregir lo_que_sabemos.md y la ficha V02 (la frase, no una cifra), separando stock y alquiler; (b) mantenerlo; (c) otra opción.
