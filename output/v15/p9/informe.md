# H5 · Predicción frente al AR(4) y al ECM v1 · informe
**Resultado.** Con 53 errores de entrenamiento (2013Q1–2026Q1, h = 1), la combinación tiene una razón de ECM de 1.51 frente al AR(4); DM-HLN unilateral: DM = -1.12, p = 0.866. Ningún modelo de la lista supera al AR(4); la línea base K1 de menor ECM es AR4. Predicción, sin lectura causal. Evaluación sellada: octubre de 2027.

## Ficha reproducible {#razon}
`python3 src/v15/p9_prediccion.py`. Ventana expansiva; AR(4), ECM v1 reconstruido (DV15-B-2), paseo con deriva, DFM, BVAR, LASSO y ARDL sobre la misma muestra.

| modelo | RMSE | razón ECM / AR(4) |
|---|---|---|
| AR4 | 0.00981 | 1.00 |
| DFM | 0.01090 | 1.24 |
| BVAR | 0.01166 | 1.41 |
| LASSO | 0.01619 | 2.72 |
| ARDL | 0.01104 | 1.27 |
| Combinacion | 0.01207 | 1.51 |
| RWD | 0.01218 | 1.54 |
| ECMv1 | 0.01572 | 2.57 |

## DM-HLN {#dm}
Combinación frente a AR(4): p unilateral 0.866; frente al ECM v1: p 0.088; frente a la base K1: p 0.866. Sin 2020T2-T3: p 0.714.

## MCS y otros contrastes (descriptivos)
MCS 10 %: AR4, DFM, BVAR, LASSO, ARDL, Combinacion. Clark-West y GW: no se calculan (NO APTOS). Multiverso (60): 3.33 % de las especificaciones con ECM menor que el AR(4); razón entre 0.975 y 5.41. Potencia: P ≈ 53 errores (< 73 del preregistro): potencia menor que 0,58 (MC) para una reducción del 20 %.

## Límites
C4 (entrenamiento), `pendiente_sellada`: true. Lenguaje de asociación. Multiplicidad (Holm en H, BH/BY en E) la aplica el orquestador con `p_valores_para_BY` de resultado.json. Desviaciones: docs/v15/desviaciones.md (DV15-B). Semilla 20261010.
