# Decisiones V7.1 (W = decisión de V7.1)

- **W0.** La v7.1 es la versión de referencia; la v6.2 pasa a histórica. La única fuente de cifras sigue siendo output/v5/cifras_clave.csv, que ahora también incorpora los hechos.json de output/v7 y output/v7_1. No se cambia ninguna cifra publicada de v6.2 o v6.3: solo se añaden filas.
- **W1.** Las tareas de texto, consolidación y estructura las hace el orquestador. Motivo: los subagentes de entregables, revisión e inventario superaron sus topes en V7 (regla de disciplina).
- **W2.** cifras_clave también lee output/v7/*/hechos.json (R4, R4b, R5, R6) y output/v7_1/*/hechos.json, nunca los `_smoke`. Solo se añaden 46 filas; ninguna cifra existente cambia (diff con solo inserciones). Las variaciones % de los escenarios R6 pueden ser negativas, así que el test test_k4a_cifras admite el prefijo V7-R6-.
- **W3.** S1 no publica un «umbral de equivalencia» frente a f2 (rebaja de impuestos y costes de construcción). Motivo: R6 traslada la rebaja al precio de todo el mercado, mientras que el coste fiscal solo cubre la obra nueva. La eficiencia por euro de f2 queda sobrestimada por construcción, y compararse con ella sesgaría la lectura. Se declara en el resumen, las fichas y el atlas.
- **W4.** Normalización de S1:
  - **Efecto por 10.000 viviendas:** solo en los instrumentos de cantidad (a-d), sobre la dosis acumulada a 10 años.
  - **Efecto por 100 M€:** sobre el coste fiscal ANUAL, porque una ayuda permanente es un flujo y el efecto en el precio es un nivel. Solo se calcula donde hay coste estimable (e, f1 y f2 en compra).
  - **Ayudas a la demanda y rebaja de ITP/IVA:** como el precio de mercado sube, el «coste por punto» se refiere al precio neto que paga el beneficiario.
  - **Dosis de f1:** todas las compraventas, igual que en R6. Es una cota superior, porque el escenario es de vivienda nueva.
- **W5.** Los costes de los instrumentos de cantidad (construcción, vacías, vivienda pública, turísticos) y el de las ayudas al alquiler quedan como «coste no estimable», con su motivo. Se da una regla de lectura: efecto por 100 M€ = efecto por 10.000 viviendas × 10.000 / u, para un coste por vivienda u. No se publica ningún u.
- **W6.** Literatura de la nota (S2): Scimago devolvió 403. Ninguna referencia queda «VERIFICADA» completa; todas figuran como «DOI verificado, cuartil no verificado» (docs/v7_1/literatura_nota.md). Las 3 revistas propuestas también quedan con «cuartil no verificado» y pasan a las tareas del autor.
