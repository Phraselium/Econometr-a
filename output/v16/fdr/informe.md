# V16 · Control de falsos descubrimientos (fase 6)

Generado por `python3 src/v16/f6_fdr.py`. Benjamini-Yekutieli, q = 0.1, denominador fijo por rama (adenda punto 2; K12). Las pruebas sin p-valor (herramienta NO APTA) cuentan en el denominador y no pueden rechazarse. Rechazar en (a) no basta para un hallazgo: faltan (b) magnitud de referencia y (c) muestra sellada.

## Rama diseños (m = 21)

| Prueba | p | q (BY) | Condición (a) |
|---|---|---|---|
| Q9-g | 0.004 | 0.306 | no cumple |

Sin p-valor (NO APTO): 14; no reportadas: 6.

## Rama rejilla (m = 83)

| Prueba | p | q (BY) | Condición (a) |
|---|---|---|---|

Sin p-valor (NO APTO): 83; no reportadas: 0.

<a id="by"></a>Ficha: q_BY = mín. sobre j ≥ rango de p_(j) · m · Σ_{i≤m} 1/i / j, con m fijo por rama; reproducible con `python3 src/v16/f6_fdr.py` desde los p de cada resultado.json.
