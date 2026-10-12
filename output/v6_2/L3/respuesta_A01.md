**A-01 (capa C1 del déficit 2021-2024).** Objeción: el extremo alto usa una corrección de la EPA fijada en el código (242.400 hogares), y las terminadas proceden de un solo organismo, de modo que no hay dos fuentes independientes en sentido fuerte.

Qué se hizo (v6.2, L3; src/v6_2/l3_deficit.py):
- Se recalculó el déficit con siete tratamientos alternativos del salto de la EPA en 2021T1, más la constante de v1: sin corrección; variación de ese trimestre igual a la media de los trimestres vecinos, con dos y con cuatro; igual a cero; enlace por cociente con la ECP; ECP retropolada; ECP publicada.
- Se cruzaron con tres fuentes de terminadas: Ministerio con y sin protegida, y Catastro completado con el Ministerio en País Vasco y Navarra.
- Se aplicaron bajas de 0 %, 0,1 % y 0,2 % anual, además de las estimadas en v5.1.
- Tras la revisión de v6.2, la ventana de la ECP va de 1-ene-2021 a 1-ene-2025.

Resultado:
- Sin bajas, el déficit 2021-2024 queda entre 389.361 y 710.542 viviendas. La amplitud es del 29,2 % del punto medio, frente a una tolerancia del 15 %, aunque la EPA corregida y la ECP coinciden dentro del 10,5 %, y el Catastro y el Ministerio dentro del 3,1 %.
- El mínimo lo fijan las variantes que conservan el quiebre de la EPA. Sin ellas, el rango sería 596.371-710.542, pero excluirlas es un supuesto sobre el salto.

Capa final: el déficit 2021-2024 sin bajas pasa de C1 a C2, una cota con supuestos explícitos sobre el tratamiento del salto y la fuente de terminadas.
- Con bajas estimadas: 389.361-765.994 (C4).
- Con bajas supuestas: hasta 924.658 (C2).
- La regla de capa se escribió en el mismo commit que los resultados, así que su anterioridad no consta en git.
