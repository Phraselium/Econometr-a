# M7 - multiverso estructurado (capa C4: sensibilidad)

Rejilla 37980 especificaciones (tope 50000); ajustadas 32424; fallidas u omitidas 5556 (todas en registro.csv). Sin truncar.

Regla del multiverso (§9, R3): signo ORIENTADO (tipos x-1) estable en >=80 % y significativo tras BH (q=0,10) en >=50 % de las especificaciones, en la familia y en su variable principal. Las fallidas cuentan como «no cumple» en las columnas *_rejilla; P4 y compra P1: multiverso truncado. Cumplen 2 de 74 combinaciones (mercado, periodo, factor).

| mercado | periodo | factor | n | % signo | signo | % sig BH | beta_std mediana [p05, p95] |
|---|---|---|---|---|---|---|---|
| alquiler | P2 | demografia | 288 | 100% | positivo | 78% | 0.52 [0.28, 1.13] |
| alquiler | completo | demografia | 576 | 98% | positivo | 60% | 0.26 [0.03, 0.55] |

Clave de cruce para M2/M5: `resumen_multiverso.csv`, filas con variable = TODAS, por (mercado, periodo, factor).
Sin lenguaje causal: estas son asociaciones; el multiverso mide la sensibilidad a decisiones del analista, no identifica efectos.
Alquiler sin medida alternativa trimestral nacional; P4 (9 trimestres) casi sin especificaciones viables (GL<5).
