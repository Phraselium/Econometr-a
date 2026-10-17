# V16 · Fase 2 · Esfuerzo de acceso a la vivienda (ECV 2004-2025)

Capa **C4 · DESCRIPTIVO**. Contabilidad y descripción: no se contrasta ninguna política. ECV y Eurostat son la misma encuesta (K6): la coincidencia con Eurostat valida la implementación, no forma un C1. Año = año de la encuesta (la renta es del año anterior). 

## Definiciones y método

- **Gasto neto** G = 12·HH070 − HY070N (HH070 mensual; HY070N, ayudas a la vivienda, anual). **Renta neta** Y = HY020 − HY070N (definición Eurostat de la sobrecarga de coste de vivienda). Se cuenta como sobrecarga G > 40 % o 30 % de Y; con Y ≤ 0 y G > 0 también.
- **Renta residual:** renta equivalente (HY020/HX240) antes y después de 12·HH070; umbral = 60 % de la mediana ponderada por personas del mismo año de la renta antes del gasto. Indicador: antes ≥ umbral y después < umbral.
- **Esfuerzo** r = min(G/Y, 1) (r = 1 si Y ≤ 0 y G > 0). Tasas: ponderadas por personas (suma de RB050 del hogar); esfuerzo medio: pesos de hogar DB090.
- **Grupos:** quintil de renta equivalente antes del gasto (personas); edad y nacionalidad del sustentador (miembro con mayor renta personal neta; nacionalidad: PB220A hasta 2020, RB290 desde 2021; 2004-2009 el código 4 se agrupa con 3: supuesto); tenencia: HH021 desde 2011; hasta 2010 (HH020) la hipoteca se identifica por cuotahip > 0 (ruptura de definición); región NUTS2 (DB040; la ECV no tiene provincia).
- **Incertidumbre:** bootstrap de hogares con reposición, B = 500, SEED = 20261010, IC 95 % percentil; el umbral de pobreza se recalcula en cada réplica; los quintiles se fijan con la muestra completa. El diseño real tiene estratos y conglomerados no publicados: el IC es **aproximado** (algo estrecho). **Supresión:** celdas con menos de 50 hogares muestrales o CV > 30 % se marcan «suprimida».

## Validación frente a Eurostat ilc_lvho07a

- 2013-2025: diferencia absoluta máxima 0,05 pp; dentro de ±0,5 pp en 13 de 13 años (2015-2024: 10 de 10).
- 2004-2012: **no coincide** en 8 de 9 años (diferencia máxima 4,1 pp, mi tasa por encima). Origen no resuelto (posible cambio de definición de HH070 en la serie anterior a 2013). Esos años se tratan como no validados; el nivel de 2008 solo se usa con esta advertencia.

(Años seleccionados; serie completa en comparacion_eurostat.csv.)

| Año | ECV (%) | Eurostat (%) | Dif. (pp) |
|---|---|---|---|
| 2008 | 10,1 | 9,4 | 0,7 |
| 2012 | 14,3 | 10,7 | 3,6 |
| 2013 | 10,3 | 10,3 | 0,0 |
| 2015 | 10,3 | 10,3 | 0,0 |
| 2019 | 8,5 | 8,5 | 0,0 |
| 2022 | 9,2 | 9,2 | 0,0 |
| 2025 | 7,2 | 7,2 | -0,0 |

## Esfuerzo de acceso

<a id="esf-espana"></a>
### España (% de la población; IC 95 %)

| Indicador | 2008 | 2015 | 2019 | 2025 |
|---|---|---|---|---|
| sobre40 | 10,1 [9,2; 11,0] | 10,3 [9,6; 11,2] | 8,5 [7,8; 9,4] | 7,2 [6,8; 7,7] |
| sobre30 | 16,3 [15,3; 17,4] | 16,9 [16,0; 17,9] | 14,0 [13,0; 14,9] | 12,0 [11,4; 12,7] |
| cae_bajo_umbral | 9,9 [9,1; 10,6] | 9,8 [9,1; 10,5] | 9,7 [9,0; 10,4] | 9,3 [8,7; 9,9] |
| pobreza_antes | 20,7 [19,7; 21,6] | 22,1 [21,4; 23,0] | 20,6 [19,8; 21,7] | 19,5 [18,7; 20,2] |
| pobreza_despues | 30,6 [29,7; 31,4] | 31,9 [31,1; 32,9] | 30,3 [29,5; 31,3] | 28,7 [27,9; 29,4] |

<a id="esf-tenencia"></a>
### Por tenencia (sobre40, %)

| Grupo | 2008 | 2015 | 2019 | 2025 |
|---|---|---|---|---|
| propiedad sin hipoteca | 2,7 [2,3; 3,2] | 2,7 [2,3; 3,1] | 1,8 [1,5; 2,2] | 1,9 [1,6; 2,1] |
| propiedad con hipoteca | 11,7 [10,1; 13,3] | 8,7 [7,5; 10,1] | 3,7 [2,7; 4,7] | 3,4 [2,8; 4,2] |
| alquiler a precio de mercado | 38,8 [34,0; 44,0] | 43,3 [39,1; 47,4] | 37,4 [33,8; 41,3] | 26,8 [24,6; 29,3] |
| alquiler reducido o cesión | 7,1 [4,9; 9,7] | 9,9 [7,7; 12,5] | 9,3 [6,7; 12,0] | 8,4 [6,8; 10,1] |

<a id="esf-quintil"></a>
### Por quintil de renta (sobre40, %)

| Grupo | 2008 | 2015 | 2019 | 2025 |
|---|---|---|---|---|
| Q1 | 31,9 [29,1; 35,1] | 40,8 [37,7; 43,9] | 32,5 [29,4; 35,3] | 27,7 [25,7; 29,9] |
| Q2 | 10,2 [8,4; 12,5] | 7,6 [6,2; 9,1] | 6,4 [5,1; 7,7] | 5,2 [4,5; 6,0] |
| Q3 | 5,0 [3,8; 6,3] | 1,9 [1,3; 2,6] | 2,5 [1,8; 3,4] | 1,9 [1,5; 2,3] |
| Q4 | 2,3 [1,6; 3,0] | 1,1 [0,7; 1,6] | 1,2 [0,7; 1,7] | 0,9 [0,6; 1,2] |
| Q5 | 1,0 [0,6; 1,5] | suprimida | suprimida | suprimida |

<a id="esf-edad"></a>
### Por edad del sustentador (sobre40, %)

| Grupo | 2008 | 2015 | 2019 | 2025 |
|---|---|---|---|---|
| 16-34 | 13,9 [11,7; 16,2] | 19,1 [15,4; 22,6] | 16,4 [13,6; 19,4] | 12,8 [10,8; 15,2] |
| 35-49 | 12,5 [10,9; 14,3] | 13,8 [12,1; 15,5] | 11,3 [9,7; 13,2] | 8,6 [7,7; 9,5] |
| 50-64 | 6,2 [4,8; 7,9] | 7,1 [6,0; 8,4] | 5,9 [4,9; 6,9] | 5,9 [5,1; 6,9] |
| 65+ | 5,8 [4,3; 7,6] | 3,6 [3,0; 4,5] | 3,8 [3,1; 4,7] | 4,6 [4,1; 5,1] |

<a id="esf-nacionalidad"></a>
### Por nacionalidad del sustentador (sobre40, %)

| Grupo | 2008 | 2015 | 2019 | 2025 |
|---|---|---|---|---|
| nacionalidad española | 6,7 [6,1; 7,4] | 7,5 [6,9; 8,2] | 6,0 [5,4; 6,6] | 4,6 [4,3; 5,0] |
| nacionalidad de otro país de la UE | 30,4 [19,6; 42,8] | 33,1 [24,0; 43,1] | 32,7 [22,3; 45,2] | 18,5 [15,5; 22,2] |
| nacionalidad de fuera de la UE | 37,5 [31,3; 43,7] | 49,1 [40,0; 58,1] | 34,2 [28,8; 40,7] | 25,4 [22,1; 29,4] |

<a id="esf-ccaa"></a>
### Por región (sobre40, último año; todas las regiones y años en esfuerzo_por_anio.csv)

Andalucía 7,0 [5,8; 8,5]; Aragón 4,4 [2,8; 6,3]; Asturias 5,4 [3,8; 7,1]; Canarias 5,0 [3,6; 6,5]; Cantabria 6,7 [4,7; 9,3]; Castilla y León 7,6 [5,5; 9,9]; Castilla-La Mancha 6,7 [4,7; 8,9]; Cataluña 7,8 [6,8; 8,9]; Ceuta 7,3 [3,6; 12,2]; Comunitat Valenciana 8,5 [7,1; 9,9]; Extremadura 4,2 [3,1; 5,4]; Galicia 4,7 [3,5; 6,0]; Illes Balears 6,4 [4,2; 9,5]; La Rioja 6,8 [3,6; 10,6]; Madrid 9,9 [8,1; 11,9]; Melilla 13,8 [7,1; 21,8]; Murcia 6,8 [4,7; 9,1]; Navarra 3,5 [2,3; 4,9]; País Vasco 4,9 [3,6; 6,4].

<a id="esf-descomposicion"></a>
## Descomposiciones contables del esfuerzo medio (puntos porcentuales; IC 95 %)

Variable: r = min(G/Y, 1). Covariables: ln renta, edad del sustentador (y cuadrado), tamaño del hogar, nacionalidad, región. «Atribuido a características» es una suma contable: la renta entra a la vez en la ratio y como covariable, así que no se lee como mecanismo. OB2 = Oaxaca-Blinder de dos pliegues (referencia agrupada); DFL = reponderación; directa = identidad exacta de la razón de medias.

| Tenencia | Periodo | Cambio observado | OB2 características | OB2 no atribuido | OB3 dotaciones / coef. / interacción | DFL composición / estructura | Directa: gasto / renta / interacción | Métodos |
|---|---|---|---|---|---|---|---|---|
| alquiler a precio de mercado | 2008-2015 | 5,58 [1,79; 8,96] | 4,90 [1,56; 7,75] | 0,68 [-1,06; 2,43] | 4,54 / 0,23 / 0,81 | 5,54 / 0,04 | -0,4 / 2,6 / -0,0 | coinciden |
| alquiler a precio de mercado | 2015-2025 | -9,73 [-12,47; -7,11] | -16,15 [-18,54; -13,81] | 6,42 [5,09; 7,74] | -16,68 / 5,85 / 1,11 | -14,29 / 4,56 | 12,4 / -14,4 / -4,8 | coinciden |
| alquiler a precio de mercado | 2008-2025 | -4,15 [-6,60; -1,78] | -11,06 [-13,13; -9,05] | 6,91 [5,50; 8,24] | -11,99 / 6,35 / 1,48 | -9,20 / 5,05 | 11,1 / -12,0 / -3,8 | discrepan |
| alquiler a precio de mercado | 2019-2025 | -6,23 [-8,45; -4,28] | -10,57 [-12,45; -8,80] | 4,35 [3,23; 5,57] | -10,63 / 4,22 / 0,19 | -9,97 / 3,74 | 7,7 / -9,7 / -2,2 | coinciden |
| propiedad con hipoteca | 2008-2015 | -1,73 [-2,89; -0,47] | 0,57 [-0,45; 1,62] | -2,30 [-3,08; -1,54] | 0,35 / -2,85 / 0,77 | 0,83 / -2,57 | -3,3 / 0,5 / -0,1 | coinciden |
| propiedad con hipoteca | 2015-2025 | -5,21 [-6,25; -4,27] | -8,96 [-9,97; -7,99] | 3,75 [3,29; 4,29] | -9,60 / 2,72 / 1,67 | -6,95 / 1,74 | 3,1 / -5,2 / -1,1 | discrepan |
| propiedad con hipoteca | 2008-2025 | -6,94 [-7,85; -6,05] | -8,19 [-9,04; -7,30] | 1,25 [0,61; 1,88] | -9,31 / -0,32 / 2,69 | -6,60 / -0,34 | -0,3 / -5,9 / 0,1 | coinciden |
| propiedad con hipoteca | 2019-2025 | 0,81 [-0,10; 1,62] | -4,94 [-5,68; -4,22] | 5,75 [5,30; 6,23] | -5,00 / 5,66 / 0,15 | -3,60 / 4,42 | 4,9 / -2,6 / -1,2 | discrepan |

Cuantiles, solo 2019-2025 (resto en comparacion_metodos.csv; RIF, Firpo-Fortin-Lemieux, atribuido a características frente a composición DFL; pp):

| Tenencia | Periodo | Estadístico | Cambio | RIF características | DFL composición | Métodos |
|---|---|---|---|---|---|---|
| alquiler a precio de mercado | 2019-2025 | p10 | -1,62 | -2,84 | -3,36 | discrepan |
| alquiler a precio de mercado | 2019-2025 | p50 | -5,12 | -7,44 | -6,70 | coinciden |
| alquiler a precio de mercado | 2019-2025 | p90 | -25,00 | -18,27 | -36,01 | discrepan |
| propiedad con hipoteca | 2019-2025 | p10 | 0,40 | -0,88 | -0,72 | discrepan |
| propiedad con hipoteca | 2019-2025 | p50 | 1,13 | -2,09 | -1,83 | coinciden |
| propiedad con hipoteca | 2019-2025 | p90 | 0,89 | -10,27 | -7,58 | discrepan |

Regla de discrepancia (fijada aquí): signo distinto o diferencia > 25 % del cambio total. Discrepan 16 de 32 comparaciones; se reportan ambos métodos siempre (comparacion_metodos.csv).

## Límites

- C4 (fuente única); sin interpretación de mecanismos. HH070 en propiedad con hipoteca recoge intereses, no amortización (la cuota completa está en la variante de descomposicion_directa.csv). El gasto no es el precio de compra ni la renta contractual nueva. Ruptura de marco y tamaño muestral en 2021 (ver auditoría V15). La edad y la nacionalidad son las del sustentador (criterio de mayor renta personal). Los IC no incluyen estratos ni conglomerados. Celdas suprimidas entre las cifras candidatas: 1. Contrastes de la parte atribuida: BH sobre 64 (descomposiciones.csv).
