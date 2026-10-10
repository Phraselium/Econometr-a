# BA - Alquiler: resumen (fase de entrenamiento; muestra sellada NO evaluada)

Nivel de evidencia de H1: **EXPLORATORIO** (no confirmada: falla la conjunción; p_H1 intersección-unión unilateral = 0.850). El componente población 20-34 es un resultado parcial EXPLORATORIO (sobrevive a Holm intra-H1 y a las submuestras, no pre-registrado por separado). Asociación, no causalidad; la evaluación sellada está pendiente y no puede elevar H1 a ROBUSTA.
Contribuciones por periodo (descomposición contable, no atribución causal) y turismo: **EXPLORATORIO**. Muestra: 49 provincias, 2008Q1-2024Q2 (N=3185).
Cifras generadas por src/v2/ba_run.py (output/v2/BA/*.csv); 50 filas en registro.csv.

## H1 (pre-registrada)
Δ4 ln IPC alquiler sobre Δ4 ln pob 20-34, Δ4 ln pob extranjera, Δ4 ln ocupados; FE de provincia y trimestre; EE cluster provincia.

| variable | coef | IC95 % (t, 48 gl) | p cluster | p wild bootstrap (Webb, 9.999) | p Holm intra-H1 (2 contrastes) |
|---|---|---|---|---|---|
| pob 20-34 | 0.149 | [0.046; 0.252] | 0.0056 | 0.0077 | 0.0154 |
| pob extranjera | -0.018 | [-0.054; 0.017] | 0.2979 | 0.3001 | 0.3001 |
| ocupados | -0.0014 | [-0.011; 0.008] | 0.7788 | 0.7778 | - |

Lectura: 1 pp más de crecimiento interanual de la población de 20-34 años se asocia con ~0.15 pp más de crecimiento del
alquiler (diferencial entre provincias, condicionado a efectos de tiempo). **La parte "extranjera" de H1 no se confirma**: coeficiente
-0.018, indistinguible de 0 y de signo opuesto al esperado. Con ocupados tampoco hay asociación. La conjunción
pre-registrada (joven Y extranjera, ambos +) **no queda confirmada** en entrenamiento.

Robustez (h1_robustez.csv): el coeficiente de 20-34 es positivo en todas las submuestras (sin COVID, 2008-2019, desde 2014, sin Madrid/Barcelona,
sin las 5 mayores, solo T1 con población observada, 19 salidas de una CCAA) y en el panel anual (coef 0.149, p bootstrap 0.0042);
el de extranjera es negativo o nulo en todas (anual: -0.015). Sin efectos de tiempo (la variante usa también
la serie temporal común) la extranjera pasa a 0.137 (p <0.001): la
asociación temporal agregada con la población extranjera no se traslada a diferencias entre provincias.
**Aviso de datos**: la población (1 de enero) está interpolada log-linealmente en T2-T4 (marcada); la robustez T1 y anual evita la interpolación y coincide.

## Por periodos (EXPLORATORIO; P1-P4 pre-registrados)
Coeficientes H1 por periodo (EE cluster; q = BH sobre 12 contrastes):

| variable | P1 2008-13 | P2 2014-19 | P3 2020-21 | P4 2022-24Q2 |
|---|---|---|---|---|
| pob 20-34 | 0.171 (0.067; q=0.07) | 0.212 (0.060; q=0.01) | 0.178 (0.073; q=0.07) | 0.081 (0.055; q=0.26) |
| pob extranjera | -0.038 (0.026; q=0.26) | -0.022 (0.027; q=0.46) | -0.039 (0.031; q=0.30) | -0.005 (0.030; q=0.87) |
| ocupados | -0.021 (0.012; q=0.19) | 0.012 (0.007; q=0.19) | 0.010 (0.008; q=0.30) | 0.011 (0.014; q=0.46) |

Igualdad entre periodos (Wald, F): pob 20-34 p=0.064; extranjera p=0.514; ocupados p=0.129.
La asociación con 20-34 es positiva en P1-P3 y se debilita en P4 (q alto), cuando el alquiler crece más en la muestra.

Contribuciones (C1: sin efectos de tiempo, FE provincia + trimestre del año, coeficientes por periodo; contribución = β_P × (media_P(x) − media muestral de x);
IC95 con EE cluster, que NO recogen shocks comunes; tipos, regulación y expectativas quedan en "no explicado"):

| periodo | Δ4 ln alquiler (media periodo − media muestra) | demografía | empleo |
|---|---|---|---|
| P1 2008Q1-2013Q4 | 0.55 pp | -0.05 pp [-0.12 pp; 0.01 pp] | 0.16 pp [0.05 pp; 0.27 pp] |
| P2 2014Q1-2019Q4 | -0.78 pp | -0.39 pp [-0.47 pp; -0.32 pp] | -0.00 pp [-0.04 pp; 0.03 pp] |
| P3 2020Q1-2021Q4 | -0.18 pp | 0.25 pp [0.06 pp; 0.45 pp] | 0.00 pp [-0.00 pp; 0.00 pp] |
| P4 2022Q1-2024Q2 | 0.77 pp | 0.70 pp [0.52 pp; 0.87 pp] | 0.01 pp [-0.05 pp; 0.07 pp] |

Oferta (terminadas/1.000 hab.), coste de uso y PIB pc (anual): contribuciones_por_periodo.csv (C2 trimestral desde 2010Q4; C4 anual). Contribuciones pequeñas
(del orden de décimas de pp) y, para oferta, con signo + en P1 (contrario a la literatura; posible respuesta de la construcción al alquiler). El coste de
uso es una única serie nacional: sus IC están subestimados. Viviendas turísticas (INE, 2021Q3-2024Q1), contribución en P4: 0.02 pp [0.01 pp; 0.04 pp] (N temporal 6).

## Turismo (EXPLORATORIO; causalidad inversa y selección no descartadas)
- Municipal (SERPAVI vc 2020→2023 ~ ΔVUT por 1.000 uu residenciales, FE provincia, N=1981, 43 provincias): coef 0.00035 (EE 0.00030, p 0.25). Sin asociación detectable; placebo (Δ SERPAVI 2017→2020 sobre ΔVUT futura) p=0.81.
- Provincial trimestral: ΔVUT por 1.000 hab. coef 0.0024 (p 0.0007); Δ ln VUT 0.0037 (p 0.40). N temporal = 6 (2021Q3-2024Q1): inferencia frágil; el resultado depende de la métrica.

## Fuera de muestra (h=4, bloques con embargo, primer test 2012Q1; misma muestra)
| modelo | RMSE | RMSE / AR(4) | DM-HLN vs AR(4) (p) | DM-HLN vs ECM v1 (p) |
|---|---|---|---|---|
| A_solo_H1 | 0.01372 | 1.103 | -0.81 (0.42; Holm 1.00) | 0.29 (0.77) |
| B_AR4_mas_H1 | 0.01169 | 0.940 | 0.46 (0.65; Holm 1.00) | 1.43 (0.16) |
| C_AR4_H1_oferta | 0.01160 | 0.933 | 0.55 (0.58; Holm 1.00) | 1.39 (0.17) |
| D_AR4_H1_oferta_cu | 0.01336 | 1.074 | -1.55 (0.13; Holm 0.51) | 0.68 (0.50) |

RMSE de las bases en la muestra común: AR(4) 0.01244, ECM v1 0.01417. Modelo primario fijado ex ante: B_AR4_mas_H1.
**No hay mejora significativa frente al AR(4)** (p 0.65); el modelo de H1 no se presenta como explicación predictiva del alquiler.

## Qué NO se puede afirmar
- Nada causal: sin identificación (población y alquiler se determinan conjuntamente; la población joven se mueve hacia donde hay empleo o sube el alquiler).
- Que la inmigración extranjera eleve el alquiler provincial: H1 no lo encuentra con efectos de tiempo (la identificación causal es de BI).
- Que las viviendas turísticas expliquen el alquiler: sin asociación robusta y con N temporal corto.
- Que el modelo prediga mejor que un AR(4), ni que H1 se confirme en la muestra sellada (no evaluada).
- Efectos de tipos, regulación y expectativas: no medidos aquí (el coste de uso es una sola serie nacional).
