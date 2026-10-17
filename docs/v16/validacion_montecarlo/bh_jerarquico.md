# Validación Monte Carlo V16 · bh_jerarquico (control de falsos descubrimientos en dos niveles)

Código: `src/v16/montecarlo/bh_jerarquico.py` · semilla `default_rng([20261010, 5, k])`.

## Proceso generador (declarado antes de simular)
- **Estructura real:** rejilla fija (83 celdas, familias Q1 18, Q2 24, Q3 21, Q4 7, Q6 13; resultado y escala leídos de `output/v16/potencia/rejilla_fija.csv`) y rama de diseños (18 pruebas en la tabla del punto 3, familia = pregunta; el encargo hablaba de 21: se simulan 18 y 21 con 3 pruebas hipotéticas añadidas a Q1, Q2 y Q3).
- **Estadísticos:** z normales con correlación por factores latentes: factor de **resultado** (celdas que comparten resultado, aunque sean de distinta familia) y factor de **escala** (misma pregunta y escala). Correlación débil (0,2; 0,1), moderada (0,4; 0,2) o fuerte (0,7; 0,2). **Signos** positivos o mixtos (cargas ±).
- **Nulos mixtos:** global (todas nulas); 20 % de celdas no nulas al azar; 40 % de las familias activas con 50 % de celdas no nulas. Efecto no nulo: desplazamiento de 3 en z. p-valores bilaterales (y un contraste unilateral con signos mixtos).
- **Procedimiento:** p de familia por Simes, BH entre familias a q = 0,10, y BH dentro de cada familia rechazada a q = 0,10. Alternativa nombrada: Benjamini-Yekutieli (Simes con factor armónico y BY en ambos pasos).
- **Medidas:** FDR = E[V/max(R,1)] y FWER = P(V ≥ 1) a nivel de celda, potencia por celda; PRDS empírico: en pares nulos que comparten factor se comprueba que P(p_j ≤ 0,10 | p_i ≤ s) crece al bajar s. R = 2.000 por escenario.
- **Criterio:** FDR realizada ≤ q = 0,10 en todos los escenarios bilaterales (el tamaño al 5 % no aplica a un procedimiento múltiple; adaptación declarada). La cota 2q = 0,20 de la adenda se informa.

<!-- RESULTADOS -->
## Resultados (R=2000 réplicas por escenario)

| estructura            | correlacion   | signos    | nulos     | metodo   |    FDR |   FWER |   potencia_celda |
|:----------------------|:--------------|:----------|:----------|:---------|-------:|-------:|-----------------:|
| rejilla_83            | debil         | positivos | global    | bh       | 0.102  | 0.102  |         nan      |
| rejilla_83            | debil         | positivos | global    | by       | 0.014  | 0.014  |         nan      |
| rejilla_83            | debil         | positivos | celdas_20 | bh       | 0.1033 | 0.7375 |           0.7351 |
| rejilla_83            | debil         | positivos | celdas_20 | by       | 0.0309 | 0.25   |           0.4901 |
| rejilla_83            | debil         | positivos | familias  | bh       | 0.0708 | 0.558  |           0.8287 |
| rejilla_83            | debil         | positivos | familias  | by       | 0.0162 | 0.17   |           0.6195 |
| rejilla_83            | debil         | mixtos    | global    | bh       | 0.0925 | 0.0925 |         nan      |
| rejilla_83            | debil         | mixtos    | global    | by       | 0.014  | 0.014  |         nan      |
| rejilla_83            | debil         | mixtos    | celdas_20 | bh       | 0.0991 | 0.716  |           0.7425 |
| rejilla_83            | debil         | mixtos    | celdas_20 | by       | 0.0274 | 0.225  |           0.4959 |
| rejilla_83            | debil         | mixtos    | familias  | bh       | 0.0705 | 0.5725 |           0.8307 |
| rejilla_83            | debil         | mixtos    | familias  | by       | 0.0174 | 0.1755 |           0.6303 |
| rejilla_83            | moderada      | positivos | global    | bh       | 0.099  | 0.099  |         nan      |
| rejilla_83            | moderada      | positivos | global    | by       | 0.013  | 0.013  |         nan      |
| rejilla_83            | moderada      | positivos | celdas_20 | bh       | 0.1032 | 0.6905 |           0.7313 |
| rejilla_83            | moderada      | positivos | celdas_20 | by       | 0.0274 | 0.215  |           0.4861 |
| rejilla_83            | moderada      | positivos | familias  | bh       | 0.0678 | 0.535  |           0.8257 |
| rejilla_83            | moderada      | positivos | familias  | by       | 0.0165 | 0.1635 |           0.6184 |
| rejilla_83            | moderada      | mixtos    | global    | bh       | 0.1055 | 0.1055 |         nan      |
| rejilla_83            | moderada      | mixtos    | global    | by       | 0.0135 | 0.0135 |         nan      |
| rejilla_83            | moderada      | mixtos    | celdas_20 | bh       | 0.1003 | 0.685  |           0.7387 |
| rejilla_83            | moderada      | mixtos    | celdas_20 | by       | 0.0284 | 0.2195 |           0.4954 |
| rejilla_83            | moderada      | mixtos    | familias  | bh       | 0.0726 | 0.5445 |           0.8301 |
| rejilla_83            | moderada      | mixtos    | familias  | by       | 0.0178 | 0.176  |           0.6259 |
| rejilla_83            | fuerte        | positivos | global    | bh       | 0.0965 | 0.0965 |         nan      |
| rejilla_83            | fuerte        | positivos | global    | by       | 0.0115 | 0.0115 |         nan      |
| rejilla_83            | fuerte        | positivos | celdas_20 | bh       | 0.1041 | 0.618  |           0.7363 |
| rejilla_83            | fuerte        | positivos | celdas_20 | by       | 0.0289 | 0.198  |           0.49   |
| rejilla_83            | fuerte        | positivos | familias  | bh       | 0.0671 | 0.487  |           0.8102 |
| rejilla_83            | fuerte        | positivos | familias  | by       | 0.0151 | 0.143  |           0.5974 |
| rejilla_83            | fuerte        | mixtos    | global    | bh       | 0.082  | 0.082  |         nan      |
| rejilla_83            | fuerte        | mixtos    | global    | by       | 0.0125 | 0.0125 |         nan      |
| rejilla_83            | fuerte        | mixtos    | celdas_20 | bh       | 0.1028 | 0.621  |           0.737  |
| rejilla_83            | fuerte        | mixtos    | celdas_20 | by       | 0.0307 | 0.2165 |           0.4923 |
| rejilla_83            | fuerte        | mixtos    | familias  | bh       | 0.0691 | 0.487  |           0.8246 |
| rejilla_83            | fuerte        | mixtos    | familias  | by       | 0.0175 | 0.1515 |           0.6286 |
| disenos_18            | debil         | positivos | global    | bh       | 0.1    | 0.1    |         nan      |
| disenos_18            | debil         | positivos | global    | by       | 0.0185 | 0.0185 |         nan      |
| disenos_18            | debil         | positivos | celdas_20 | bh       | 0.1164 | 0.3585 |           0.7326 |
| disenos_18            | debil         | positivos | celdas_20 | by       | 0.0451 | 0.1435 |           0.5259 |
| disenos_18            | debil         | positivos | familias  | bh       | 0.0972 | 0.294  |           0.7611 |
| disenos_18            | debil         | positivos | familias  | by       | 0.033  | 0.095  |           0.5732 |
| disenos_18            | debil         | mixtos    | global    | bh       | 0.1095 | 0.1095 |         nan      |
| disenos_18            | debil         | mixtos    | global    | by       | 0.024  | 0.024  |         nan      |
| disenos_18            | debil         | mixtos    | celdas_20 | bh       | 0.1216 | 0.3655 |           0.7389 |
| disenos_18            | debil         | mixtos    | celdas_20 | by       | 0.0451 | 0.143  |           0.5376 |
| disenos_18            | debil         | mixtos    | familias  | bh       | 0.0899 | 0.2765 |           0.7723 |
| disenos_18            | debil         | mixtos    | familias  | by       | 0.0292 | 0.0935 |           0.5941 |
| disenos_18            | moderada      | positivos | global    | bh       | 0.107  | 0.107  |         nan      |
| disenos_18            | moderada      | positivos | global    | by       | 0.0255 | 0.0255 |         nan      |
| disenos_18            | moderada      | positivos | celdas_20 | bh       | 0.1164 | 0.3475 |           0.7319 |
| disenos_18            | moderada      | positivos | celdas_20 | by       | 0.043  | 0.133  |           0.5218 |
| disenos_18            | moderada      | positivos | familias  | bh       | 0.0875 | 0.2575 |           0.7661 |
| disenos_18            | moderada      | positivos | familias  | by       | 0.03   | 0.086  |           0.5718 |
| disenos_18            | moderada      | mixtos    | global    | bh       | 0.09   | 0.09   |         nan      |
| disenos_18            | moderada      | mixtos    | global    | by       | 0.0185 | 0.0185 |         nan      |
| disenos_18            | moderada      | mixtos    | celdas_20 | bh       | 0.1158 | 0.344  |           0.7208 |
| disenos_18            | moderada      | mixtos    | celdas_20 | by       | 0.0438 | 0.128  |           0.5126 |
| disenos_18            | moderada      | mixtos    | familias  | bh       | 0.0917 | 0.271  |           0.7719 |
| disenos_18            | moderada      | mixtos    | familias  | by       | 0.0329 | 0.1015 |           0.5808 |
| disenos_18            | fuerte        | positivos | global    | bh       | 0.0865 | 0.0865 |         nan      |
| disenos_18            | fuerte        | positivos | global    | by       | 0.023  | 0.023  |         nan      |
| disenos_18            | fuerte        | positivos | celdas_20 | bh       | 0.1106 | 0.3035 |           0.7322 |
| disenos_18            | fuerte        | positivos | celdas_20 | by       | 0.042  | 0.122  |           0.5248 |
| disenos_18            | fuerte        | positivos | familias  | bh       | 0.0903 | 0.2395 |           0.7482 |
| disenos_18            | fuerte        | positivos | familias  | by       | 0.0311 | 0.0885 |           0.5542 |
| disenos_18            | fuerte        | mixtos    | global    | bh       | 0.082  | 0.082  |         nan      |
| disenos_18            | fuerte        | mixtos    | global    | by       | 0.0205 | 0.0205 |         nan      |
| disenos_18            | fuerte        | mixtos    | celdas_20 | bh       | 0.1001 | 0.286  |           0.7389 |
| disenos_18            | fuerte        | mixtos    | celdas_20 | by       | 0.0375 | 0.1115 |           0.5369 |
| disenos_18            | fuerte        | mixtos    | familias  | bh       | 0.0874 | 0.247  |           0.77   |
| disenos_18            | fuerte        | mixtos    | familias  | by       | 0.0356 | 0.105  |           0.5909 |
| disenos_21            | debil         | positivos | global    | bh       | 0.1005 | 0.1005 |         nan      |
| disenos_21            | debil         | positivos | global    | by       | 0.0205 | 0.0205 |         nan      |
| disenos_21            | debil         | positivos | celdas_20 | bh       | 0.1118 | 0.376  |           0.7379 |
| disenos_21            | debil         | positivos | celdas_20 | by       | 0.0441 | 0.1495 |           0.5251 |
| disenos_21            | debil         | positivos | familias  | bh       | 0.0898 | 0.3045 |           0.7708 |
| disenos_21            | debil         | positivos | familias  | by       | 0.0292 | 0.101  |           0.5755 |
| disenos_21            | debil         | mixtos    | global    | bh       | 0.099  | 0.099  |         nan      |
| disenos_21            | debil         | mixtos    | global    | by       | 0.02   | 0.02   |         nan      |
| disenos_21            | debil         | mixtos    | celdas_20 | bh       | 0.1157 | 0.3865 |           0.7329 |
| disenos_21            | debil         | mixtos    | celdas_20 | by       | 0.044  | 0.1465 |           0.5161 |
| disenos_21            | debil         | mixtos    | familias  | bh       | 0.0965 | 0.315  |           0.7831 |
| disenos_21            | debil         | mixtos    | familias  | by       | 0.0341 | 0.1115 |           0.5894 |
| disenos_21            | moderada      | positivos | global    | bh       | 0.0815 | 0.0815 |         nan      |
| disenos_21            | moderada      | positivos | global    | by       | 0.0155 | 0.0155 |         nan      |
| disenos_21            | moderada      | positivos | celdas_20 | bh       | 0.1187 | 0.3805 |           0.7371 |
| disenos_21            | moderada      | positivos | celdas_20 | by       | 0.0453 | 0.1485 |           0.5246 |
| disenos_21            | moderada      | positivos | familias  | bh       | 0.0906 | 0.2885 |           0.7563 |
| disenos_21            | moderada      | positivos | familias  | by       | 0.0305 | 0.0955 |           0.5624 |
| disenos_21            | moderada      | mixtos    | global    | bh       | 0.095  | 0.095  |         nan      |
| disenos_21            | moderada      | mixtos    | global    | by       | 0.021  | 0.021  |         nan      |
| disenos_21            | moderada      | mixtos    | celdas_20 | bh       | 0.1196 | 0.3755 |           0.7439 |
| disenos_21            | moderada      | mixtos    | celdas_20 | by       | 0.0473 | 0.152  |           0.5341 |
| disenos_21            | moderada      | mixtos    | familias  | bh       | 0.0914 | 0.3035 |           0.7891 |
| disenos_21            | moderada      | mixtos    | familias  | by       | 0.0304 | 0.1005 |           0.5863 |
| disenos_21            | fuerte        | positivos | global    | bh       | 0.087  | 0.087  |         nan      |
| disenos_21            | fuerte        | positivos | global    | by       | 0.025  | 0.025  |         nan      |
| disenos_21            | fuerte        | positivos | celdas_20 | bh       | 0.1075 | 0.3005 |           0.7288 |
| disenos_21            | fuerte        | positivos | celdas_20 | by       | 0.0356 | 0.1095 |           0.5261 |
| disenos_21            | fuerte        | positivos | familias  | bh       | 0.0886 | 0.25   |           0.7488 |
| disenos_21            | fuerte        | positivos | familias  | by       | 0.0289 | 0.0845 |           0.5492 |
| disenos_21            | fuerte        | mixtos    | global    | bh       | 0.08   | 0.08   |         nan      |
| disenos_21            | fuerte        | mixtos    | global    | by       | 0.016  | 0.016  |         nan      |
| disenos_21            | fuerte        | mixtos    | celdas_20 | bh       | 0.115  | 0.343  |           0.741  |
| disenos_21            | fuerte        | mixtos    | celdas_20 | by       | 0.042  | 0.1305 |           0.5213 |
| disenos_21            | fuerte        | mixtos    | familias  | bh       | 0.0961 | 0.273  |           0.773  |
| disenos_21            | fuerte        | mixtos    | familias  | by       | 0.0313 | 0.0985 |           0.5798 |
| rejilla_83_unilateral | moderada      | mixtos    | global    | bh       | 0.0885 | 0.0885 |         nan      |
| rejilla_83_unilateral | moderada      | mixtos    | global    | by       | 0.013  | 0.013  |         nan      |
| rejilla_83_unilateral | moderada      | mixtos    | celdas_20 | bh       | 0.0985 | 0.748  |           0.8332 |
| rejilla_83_unilateral | moderada      | mixtos    | celdas_20 | by       | 0.0292 | 0.2595 |           0.6148 |
| rejilla_83_unilateral | moderada      | mixtos    | familias  | bh       | 0.067  | 0.5585 |           0.9047 |
| rejilla_83_unilateral | moderada      | mixtos    | familias  | by       | 0.0143 | 0.158  |           0.7391 |

Violaciones PRDS empíricas (proporción de pares): {'rejilla_83|positivos|bilateral': 0.0, 'rejilla_83|mixtos|bilateral': 0.0, 'rejilla_83|mixtos|unilateral': 0.0, 'disenos_18|mixtos|bilateral': 0.0}

**Veredicto: NO APTO BH jerárquico; alternativa Benjamini-Yekutieli APTA** FDR máx. 0.1216 > 0.1
