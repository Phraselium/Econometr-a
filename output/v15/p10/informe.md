# E3 · Dependencia espacial del alquiler municipal · informe
**Resultado (SAR/SEM/SDM APTO).** Hay autocorrelación espacial positiva y fuerte en el Δlog SERPAVI VC: ρ (SAR, contigüidad, 2015-2024) = 0.393 (IC95 Wald 0.34–0.446), N = 1124. Los 12 contrastes de Wald rechazan ρ = 0 antes de ajustar (el ajuste BY lo aplica el orquestador). Asociación espacial, no mecanismo.

## Ficha reproducible {#rho}
`python3 src/v15/p10_espacial.py`. Regresores: constante, log alquiler inicial, log contratos iniciales.

| especificación | ρ/λ | EE | p Wald | N |
|---|---|---|---|---|
| E3-SAR-contigüidad-2015_2024 | 0.393 | 0.027 | 2.5e-47 | 1124 |
| E3-SEM-contigüidad-2015_2024 | 0.475 | 0.029 | 1.87e-59 | 1124 |
| E3-SDM-contigüidad-2015_2024 | 0.436 | 0.026 | 4.25e-63 | 1124 |
| E3-SAR-dist_inversa_25km-2015_2024 | 0.532 | 0.029 | 6.04e-73 | 1124 |
| E3-SEM-dist_inversa_25km-2015_2024 | 0.639 | 0.028 | 1.15e-115 | 1124 |
| E3-SDM-dist_inversa_25km-2015_2024 | 0.557 | 0.028 | 3.13e-87 | 1124 |
| E3-SAR-contigüidad-2011_2019 | 0.244 | 0.030 | 1.11e-15 | 1015 |
| E3-SEM-contigüidad-2011_2019 | 0.411 | 0.035 | 2.14e-31 | 1015 |
| E3-SDM-contigüidad-2011_2019 | 0.376 | 0.028 | 2.64e-40 | 1015 |
| E3-SAR-dist_inversa_25km-2011_2019 | 0.344 | 0.037 | 1.92e-20 | 1015 |
| E3-SEM-dist_inversa_25km-2011_2019 | 0.624 | 0.034 | 1.77e-77 | 1015 |
| E3-SDM-dist_inversa_25km-2011_2019 | 0.471 | 0.034 | 1.86e-44 | 1015 |

Efectos directo e indirecto (simulación LeSage-Pace, 1.000 réplicas): en resultado.json (`detalle`). Moran de los residuos MCO y exclusión de Barcelona/València: en `diagnosticos`. Sin errores de Conley (no figura en las tablas).

## Límites
C4 (entrenamiento), `pendiente_sellada`: true. Lenguaje de asociación. Multiplicidad (Holm en H, BH/BY en E) la aplica el orquestador con `p_valores_para_BY` de resultado.json. Desviaciones: docs/v15/desviaciones.md (DV15-B). Semilla 20261010.
