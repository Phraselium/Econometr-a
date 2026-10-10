# Rama BV (compra) — resumen

Datos: `panel_prov_q` y `nacional_q_v2` vía `v2_common.load` (49 provincias de entrenamiento, 2004Q1-2024Q2; sin muestra sellada). Precio real = Δ4 ln `p_tasado` − Δ4 ln `deflactor` nacional (de `nacional_q_v2`). Dos ejecuciones con md5 idénticos (`bv_main.py`; smoke con 10 provincias y 2010-2019 en `smoke/`).

## H2 (confirmatoria; especificación del pre-registro)
Δ4 ln p real ~ Δ4 ln hipotecas_importe + coste_uso×exposición 2005-07 (z-score; importe hipotecario por habitante) + Δ4 ln ocupados; FE provincia y trimestre; N=3.981, 49 clusters. IC95 y p con EE cluster; p también con wild cluster bootstrap (Webb, 9.999, WCR).

| Coef. | Estimación | IC95 | p (WCB) | Holm (m=2) |
|---|---|---|---|---|
| Δ4 ln crédito hipotecario | +0,0087 | [0,0033; 0,0141] | 0,0018 | 0,0018 |
| coste de uso × exposición (por DE y pp) | −0,0044 | [−0,0058; −0,0030] | <0,0001 | <0,0001 |
| Δ4 ln ocupados | +0,044 | [0,005; 0,083] | 0,032 | n/a (no es parte de H2) |

Signos como los esperados. Magnitud: +10 % de crédito anual se asocia con +0,09 pp de precio real; +1 pp de coste de uso resta 0,44 pp al crecimiento anual en una provincia con exposición +1 DE respecto a la media (solo se identifica el diferencial por exposición; el nivel nacional lo absorbe el FE de trimestre). Con Bonferroni conservador ×7 (familia de 7 confirmatorias) el crédito queda en 0,013.

**Simultaneidad.** Con el crédito retardado 4 trimestres su coeficiente es +0,0019 (p=0,48): la asociación del crédito es contemporánea (comovimiento, como en v1), no predictiva. La interacción del coste de uso no cambia (−0,0042). Con crédito en t y t−4: +0,0106 y +0,0056 (p=0,10).
Submuestras: crédito 2004-13 +0,0086 (p=0,04) y 2014-24 +0,0046 (p=0,20, no significativo); coste de uso significativo en ambas (−0,0050; −0,0019); también sin COVID y sin Madrid/Barcelona.

**Nivel de evidencia: EXPLORATORIO.** Dentro de muestra pasa signos, Holm y submuestras, pero el criterio fijado de antemano para ASOCIACIÓN ROBUSTA exigía además mejorar fuera de muestra al AR(4): no lo hace (ver abajo). Máximo posible sin sellado: ASOCIACIÓN ROBUSTA. La confirmación queda a `bv_h2_sellado.evaluar_H2` (NO ejecutada; modelo fijado: C1).

## Fuera de muestra (h=4, bloques, primer test 2012Q1, embargo 4; misma muestra, n=2.209 provincia-trimestre)
Panel (6 configuraciones declaradas, registradas): RMSE AR(4)=0,0418; ECM v1 de panel=0,0809. Mejor: C1 (AR4+Δ4 crédito) 0,0413, DM-HLN +0,28 (p=0,78); C2 0,0420; C3-C6 (con coste de uso, ocupados) 0,059-0,063, peores (DM −1,5, no significativo). Ninguna mejora significativa al AR(4) (Holm/BH); todas son mejores que el ECM v1 (RMSE) pero no significativamente tras ajuste. **El modelo de H2 no mejora al AR(4) fuera de muestra: no se presenta como explicación predictiva.**
Nacional (4 configuraciones): AR(4)=0,0274; ECM v1=0,0693; N1-N4 = 0,035-0,041, peores que el AR(4) (N3, crédito por finalidad, significativamente peor, Holm 0,03). En muestra (HAC 4, exploratorio): crédito, hipotecas y coste de uso Δ4 positivos y significativos, pero no predicen.

## Por periodos (EXPLORATORIO; `periodos_*.csv`)
Coeficientes por periodo (spec H2): el crédito no es significativo en ningún periodo individual (0,007 en P1-P3; −0,004 en P4); la interacción del coste de uso es negativa y fuerte en P1 (−0,0075) y P3 (−0,013; Holm 0,0005), débil en P2 (−0,0028, Holm 0,15) y nula en P4 (−0,0001). Contribuciones (pp de Δ4 precio real respecto a la media de la muestra; modelo B con FE de provincia e intercepto de periodo, IC95 cluster): P1 ajuste: crédito −0,65 [−1,04;−0,27], coste de uso −1,31, empleo −1,07, demografía −0,48 (explica −3,6 de −3,3 observados). P2: crédito +0,36, demografía −0,44; lo explicado ≈ 0 de +1,85 observado (resto +1,95: no explicado). P3: crédito +0,44, coste de uso +1,02. P4: demografía −1,35, coste de uso −1,09, y 3,6 pp sin explicar; el aumento de tipos de 2022 no se recoge con el coste de uso×exposición (coef. P4 ≈ 0). Oferta ≈ 0 siempre. Renta provincial no existe en el panel (empleo = ocupados); el nivel nacional de tipos/coste de uso queda en el intercepto de periodo.

## Arbitraje alquiler-compra (EXPLORATORIO; `arbitraje_lp.csv`)
Proyecciones locales h=1..8 con FE provincia y trimestre. Un ratio precio/alquiler 1 unidad de log por encima de la media provincial predice menor crecimiento posterior del precio (h=1: −0,036; h=4: −0,12; h=8: −0,25; todas p<0,001, Holm m=16) y mayor del alquiler (h=1: +0,005; h=4: +0,021; h=8: +0,037; Holm 0,02-0,03). Con media expansiva (sin mirar al futuro) los signos se mantienen y son menores (h=4: −0,065 / +0,021). Cautela: la desviación respecto de la media de toda la muestra incorpora reversión mecánica (y error de medida del índice de alquiler), y el ratio es un índice, no un nivel; el ajuste es sobre todo vía precio.

## Qué NO se puede afirmar
- Causalidad: ni del crédito (simultaneidad, sin instrumento) ni del coste de uso (aproximación sin impuestos ni prima de riesgo, mismo valor en todas las provincias; identificación solo por interacción con una exposición provincial no aleatoria).
- Que el modelo explique o prediga mejor que un AR(4) (no lo hace fuera de muestra).
- Nada sobre no residentes: el panel no tiene datos provinciales (limitación; no se leyó data/raw).
- Nada sobre 2024Q3-2026Q2 ni sobre Cádiz, Cuenca y Toledo (sellados).
- Los resultados por periodo y el arbitraje son exploratorios; P3 tiene solo 8 trimestres.
