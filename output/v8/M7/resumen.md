# M7 - multiverso estructurado (capa C4: sensibilidad)

Rejilla 37980 especificaciones (tope 50000); ajustadas 32424; fallidas u omitidas 5556 (todas en registro.csv). Sin truncar.

Regla del multiverso (§9): signo estable en >=80 % y significativo tras BH (q=0,10) en >=50 % de las especificaciones. Cumplen 3 de 74 combinaciones (mercado, periodo, factor).

| mercado | periodo | factor | n | % signo | signo | % sig BH | beta_std mediana [p05, p95] |
|---|---|---|---|---|---|---|---|
| alquiler | P2 | demografia | 288 | 100% | positivo | 78% | 0.52 [0.28, 1.13] |
| alquiler | completo | demografia | 576 | 98% | positivo | 59% | 0.26 [0.02, 0.55] |
| compra | P5 | credito_tipos | 576 | 88% | positivo | 51% | 0.50 [-0.16, 0.94] |

Clave de cruce para M2/M5: `resumen_multiverso.csv`, filas con variable = TODAS, por (mercado, periodo, factor).
Sin lenguaje causal: estas son asociaciones; el multiverso mide la sensibilidad a decisiones del analista, no identifica efectos.
Alquiler sin medida alternativa trimestral nacional; P4 (9 trimestres) casi sin especificaciones viables (GL<5).
