# Anexo · Reproducibilidad: réplica ciega de la 1.0 y de los resultados de V15-V16

## Réplica ciega de las cifras de la 1.0 (K19)

**Qué se hizo.** Se rehicieron las 31 cifras de la página resumen (una_pagina), entre ellas las 7 C1 vigentes.
- Cada una se reimplementó desde data/raw y su ficha metodológica, sin leer el código que la produjo (output/v16/replica/v10_*).
- El cegado fue parcial: en algunos lotes el replicador vio el valor publicado antes de estimar. Consta en cada resultado.json.

| Resultado | Cifras | Cuáles |
|---|---|---|
| Coinciden a la primera | 19 | Las 7 C1, E-T7 (2), L3 (2), E-B1-F, V10-ATL-A1, V72-GSADF-ccaa-v6, V72-GSADF-tipos-p05, V71-S3 (2), V8-OBS (2) |
| Coinciden tras completar la ficha (el original era correcto; faltaba un detalle por escribir) | 8 | T3-H5b, T4-H2, T4-H3, V71-S3-R6, V8-H8-9, V8-M1-cuota-c-P5, V8-QNA-pp-c-P5, V8-VOTOS-c-P5 |
| Discrepan por un error de código del original | 4 | V72-GSADF-ccaa-bh, -niveles-bh, -ratios-bh y -ratios-p05 |

**Errores encontrados y corregidos.** Valores de antes y de después en ERRATA.md y en el anexo de erratas.
- **GSADF de V7.2** (E1 y E2). El mismo E1 estaba en la copia de v6. Corregidos: los recuentos tras el ajuste de niveles y comunidades pasan a 0, y los de v6 no cambian.
- **V8-M5** (auditoría del alcance de los errores de V16). Navarra y La Rioja tenían cuota 0 en el instrumento Bartik y ahora quedan fuera.

## Réplica ciega de los resultados citables de V15 y V16 (K16 y K18)

| Resultado | Hallazgo | Corrección |
|---|---|---|
| Q3-b | El núcleo de Conley contaba dos veces la diagonal | Corregido; Conley queda NO APTO en el Monte Carlo y Q3-b se cita solo como estimación puntual |
| H4 | Municipios sin población en el año base con instrumento 0, sin declararlo | Fuera de la muestra (N 13.442 → 13.417) |
| H5 | Primer origen desplazado, el AR(4) usaba el propio objetivo y la desestacionalización usaba datos posteriores al origen | Corregidos; la combinación sigue sin superar al AR(4) |
| Q6-p | Diferencias entre años no consecutivos | Corregido; deja de ser pista y queda «no concluyente» |
| Q9-g, E3, H1, Q2a, H3 | Coinciden | — |

Ninguna corrección se eligió por su resultado: todas son errores frente a la ficha o frente a las reglas del proyecto.
