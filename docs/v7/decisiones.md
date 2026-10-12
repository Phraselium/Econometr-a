# Decisiones V7

- **V0 · Rutas.** Lo nuevo va en src/v7, output/v7, docs/v7 y tests/v7. v6.2 queda congelada, y cualquier corrección de una cifra publicable se publica como v6.3 y se anota en ERRATA.md.
- **V1 · Librerías.** pip pudo instalar pymc 6.3.2, arviz 1.3.0, pytensor 3.3.3, arch 8.0.0, libpysal 4.15.0 y spreg 1.9.1 (2026-10-12), y quedan fijadas en requirements.lock. El modelo jerárquico se estima en pymc, con MixedLM como contraste.
- **V2 · R0, incidencias del inventario.**
  1. **DM del ECM de v1 (0,29 frente a 0,51).** No es un error: son dos modelos.
     - p = 0,509 corresponde al **precio real** (output/f2/real_oos_dm.md, RMSE 0,0244 frente a 0,0165 del AR(4));
     - p = 0,290 corresponde al **precio nominal** (output/f2/oos_dm.md).
     - El informe de v1 (output/informe.md:140) ya daba los dos.
     - En adelante se citan siempre con su medida. Se añade una nota al historial.
  2. **v3 C3 H3-3b (IC con el 0 y p ajustado 0,0002).** Fallo de rotulado en output/v3/C3/resultado.json, sin efecto en ninguna cifra publicable.
     - El campo `ic95` de primer nivel es el IC de la estimación Callaway-Sant'Anna en entrenamiento: −9,9 % a 0,5 %, p 0,073.
     - El `p_ajustado`, 0,0002, es el de la evaluación **sellada**: β −4,4 %, IC −6,4 % a −2,3 %, p 5,5e-5, Holm.
     - Se anota en ERRATA como incoherencia de campos. v3 está cerrada y el JSON no se reescribe.
     - H3-3b sigue en C4: las pretendencias fallan.
  3. **min/max con otro sentido (K4a-04).** cifras_clave.csv tiene una nueva columna `sentido_min_max`: «rango» en 548 filas y una descripción en las otras 70 (9 prefijos). Los tests de rango ya no usan una lista de excepciones en el código, sino esta columna. Ningún valor cambia.
  4. **Cruces por código INE.** El test tests/test_v7_cruces.py prohíbe los cruces por nombre en el código nuevo (src/v7, src/v6_3), tanto los merge/join como la traducción de nombres con `.map` o `.replace`.
     - En el código heredado congela el recuento actual: un solo caso, R1C, en src/v5/r1c_run.py:220, C4 descriptivo, que declara las filas no cruzadas.
     - Los diccionarios de nombres heredados, como SERP2IPVA, no los detecta el patrón; se revisaron en K4a y L1.
  5. **D2 con T3 y las 26 cifras del verificador.** Las hace un subagente R0 y se publican como v6.3.
