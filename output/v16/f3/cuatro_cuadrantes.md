# V16 · Marco de cuatro cuadrantes (DiPasquale y Wheaton) calibrado para España

Generado por `python3 src/v16/f3_cuatro_cuadrantes.py`. Es un marco teórico calibrado, no una estimación: dice qué respuesta cabe esperar de cada shock si el mercado funcionara como el modelo, con los parámetros y rangos declarados. Capa C4.

## Parámetros

| Parámetro | Mínimo | Máximo | Tipo | Fuente |
|---|---|---|---|---|
| es | 0.8 | 1.3 | literatura | elasticidad de la nueva oferta a precio, 17 CCAA 1990-2012: Taltavull (2014), docs/v16/literatura/L3_oferta_elasticidad.md (leída en resumen) |
| ed | 0.3 | 1 | supuesto del autor | elasticidad-precio de la demanda de servicios de vivienda: sin estimación española leída en V16 (L3, «Parámetros de calibración»); rango amplio |
| ey | 0.5 | 1.5 | supuesto del autor | elasticidad-renta de la demanda de vivienda: sin estimación española leída en V16; rango amplio |
| i | 0.0564 | 0.05841 | cifra_clave | inversa del ratio precio/alquiler 2023 (K3-RATIO-2023, mínimo y máximo de las medidas) |
| phi | 0.002 | 0.006 | supuesto del autor | obra nueva sobre el parque al año (crecimiento del parque + bajas); orden de magnitud de E-T7-prod sobre el parque censal; las bajas por licencia (T1-H8) son < 0,06 % |
| retardo | 2.97 | 3.21 | cifra_clave | retardo medio iniciadas-terminadas en años (B2-H5); solo informativo: el estado estacionario no depende de él |

Tres de los cinco parámetros que mueven los multiplicadores son supuestos del autor: no hay estimación española leída de las elasticidades de la demanda ni de la tasa de obra nueva sobre el parque. Los rangos son amplios a propósito.

## Respuestas esperadas (Monte Carlo sobre los rangos): % de variación por shock de +1 % o de +1 p.p.; la semivida en años

| Shock | Variable | Plazo | Mediana | P5 | P95 |
|---|---|---|---|---|---|
| demanda +1 % (renta u hogares) | alquiler | largo | 0,60 | 0,31 | 0,95 |
| demanda +1 % (renta u hogares) | precio | largo | 0,60 | 0,31 | 0,95 |
| demanda +1 % (renta u hogares) | stock | largo | 0,62 | 0,33 | 0,97 |
| demanda +1 % (renta u hogares) | alquiler | corto (stock fijo) | 1,55 | 0,73 | 3,38 |
| demanda +1 % (renta u hogares) | obra nueva | corto (stock fijo) | 1,62 | 0,74 | 3,60 |
| tipo exigido +1 p.p. | precio | corto (stock fijo) | -17,42 | -17,70 | -17,15 |
| tipo exigido +1 p.p. | obra nueva | corto (stock fijo) | -18,27 | -22,18 | -14,36 |
| tipo exigido +1 p.p. | alquiler | corto (stock fijo) | 0,00 | 0,00 | 0,00 |
| tipo exigido +1 p.p. | precio | largo | -6,66 | -8,78 | -4,15 |
| tipo exigido +1 p.p. | alquiler | largo | 10,76 | 8,64 | 13,28 |
| tipo exigido +1 p.p. | stock | largo | -6,91 | -9,01 | -4,39 |
| coste de construcción +1 % | precio | largo | 0,62 | 0,50 | 0,76 |
| coste de construcción +1 % | alquiler | largo | 0,62 | 0,50 | 0,76 |
| coste de construcción +1 % | stock | largo | -0,40 | -0,52 | -0,25 |
| oferta menos elástica (es/2), demanda +1 % | precio | largo | 0,86 | 0,44 | 1,46 |
| oferta menos elástica (es/2), demanda +1 % | stock | largo | 0,45 | 0,23 | 0,75 |
| ajuste del stock | semivida (años) | — | 65,11 | 35,31 | 127,65 |

El «tipo exigido» es la rentabilidad que pide el comprador (coste de uso: tipo, depreciación, fiscalidad y revalorización esperada), no el tipo hipotecario: una subida de 1 p.p. del hipotecario no se traslada por fuerza uno a uno.

Lectura: con una obra nueva del orden del 0,2-0,6 % del parque al año, el stock tarda décadas en ajustarse; a corto plazo los shocks de demanda van sobre todo al alquiler y al precio, y los de tipos al precio y a la obra nueva.

## ¿Lo muestran los datos? Episodio de subida de tipos: medias de 2024 frente a 2022 (descriptivo)

| Serie | Variación | Signo |
|---|---|---|
| tipo hipotecario (p.p.) | 1,43 | + |
| precio de compra, IPV (%) | 12,70 | + |
| alquiler, IPC (%) | 4,29 | + |
| compraventas (%) | -1,52 | − |
| visados de obra nueva (%) | 15,70 | + |
| renta real de los hogares (%) | 8,20 | + |
| hogares, EPA (%) | 2,40 | + |

Signos que predice el marco si solo cambiaran los tipos: precio −, obra nueva −, alquiler 0 o +. Con los datos observados, ese patrón no se cumple. Si no se cumple, el marco es compatible con un shock de demanda simultáneo (hogares, renta) que compensa la subida de tipos; con estos datos no se puede separar un shock del otro: es una pregunta de la fase 6 (Q5), no una conclusión de este marco.
