# V7-R6 · Método de traslado (incidencia) y escenarios. Capa C4 (los parámetros son supuestos)

Todo el texto es condicional: «si se hiciera X, con estos supuestos…». No se afirma causalidad (C4). Se evalúan instrumentos, no actores.

## Ecuaciones (equilibrio parcial, mercado local)

Demanda con elasticidad $\varepsilon_d<0$ y oferta con elasticidad $\varepsilon_s\ge 0$ (respecto del precio).

1. Incidencia de una ayuda a la demanda sobre el precio (parte que capta el vendedor):
$$\iota=\frac{|\varepsilon_d|}{\varepsilon_s+|\varepsilon_d|}\in(0,1]$$
2. Variación del precio ante una ayuda de demanda de intensidad $s$ (fracción del precio pagado), con ajuste completo:
$$\frac{\Delta p}{p}=s\,\iota=s\,\frac{|\varepsilon_d|}{\varepsilon_s+|\varepsilon_d|}$$
   Precio neto pagado por el comprador: $\frac{\Delta p^{n}}{p}\approx -s\,(1-\iota)=-s\,\frac{\varepsilon_s}{\varepsilon_s+|\varepsilon_d|}$. Con $\varepsilon_s=0$ el precio absorbe toda la ayuda y el esfuerzo no varía.
3. Variación del precio ante un aumento de oferta $\Delta Q/Q$:
$$\frac{\Delta p}{p}=-\frac{\Delta Q/Q}{\varepsilon_s+|\varepsilon_d|}$$
4. Rebaja de un impuesto al coste de construcción $c$ (cuota $\kappa$ del coste en el precio), desplazamiento de la oferta:
$$\frac{\Delta p}{p}=-c\,\kappa\,\frac{\varepsilon_s}{\varepsilon_s+|\varepsilon_d|}$$
5. Senda de ajuste a horizonte $h$ años, con semivida $\tau$ (trimestres): $A(h)=1-2^{-4h/\tau}$, de modo que el efecto es el de las ecuaciones 2-4 multiplicado por $A(h)$.
6. Esfuerzo (compra) = precio neto pagado / renta, con la renta constante: su variación porcentual es la del precio neto. Para el alquiler, la variación de la renta.
7. Coste por euro: $\text{coste}/(\text{reducción del precio neto}\times\text{valor anual de compras})$, que en demanda es $1/(1-\iota)$ en el límite.

## Supuestos y capa

| Supuesto | Valor | Capa |
|---|---|---|
| Equilibrio parcial, un solo mercado local por CCAA, sin cambios de composición | — | C4 |
| $\lvert\varepsilon_d\rvert$ | rejilla uniforme 0,3-1,5 (P-D v3 / v5). Literatura sin valor verificado en docs/literatura.md: NO VERIFICADA | C4 |
| $\varepsilon_s$ rejilla | por clase A4 (método A de v5: percentiles 25-75 de la respuesta de oferta; método B: 1,75 / 0 / 0,45), media ponderada por déficit de las provincias de cada CCAA, cruce por código INE. Referencias: Saiz (2010, DOI verificado, cuartil no verificado); BdE IA 2025 (≈0,45) | C4 |
| $\varepsilon_s$ regional | DOLS ±2 de ln(visados) sobre ln(IPV/IPCA), 2008-2025, por CCAA; MG solo como insumo. Se usa si IC95 en [0; 5] y diagnósticos (cointegración Engle-Granger p<0,10; Ljung-Box(4) p>0,05) | C4 |
| Senda de ajuste | semivida entre las medianas regionales de R4 (spec A y B). Supuesto de senda: la inferencia de R4 no es válida (sin largo plazo identificado) | C4 |
| Ofertas: llegada | 1 año de trámite y obra antes de completarse; el acumulado es lineal | C4 |
| (a) construcción adicional | min(necesidad anual central T3, máximo anual de visados 2016-2025 menos visados 2025) × U(0,5; 1) | C4 |
| (b) vacías | triangular(M_min, M_central, M_max) de T3 / 10 años (v5 B1/T3) | C4 |
| (c) vivienda pública | 20 % de la necesidad anual central × U(0,5; 1,5), con desplazamiento de la promoción privada U(0; 0,5) | C4 |
| (d) turísticos | 5-30 % del stock de VUT regional vuelve al uso residencial; la cota nacional B4-v3-vut-cantidad (2,746 % del stock de alquiler, C2) no se reparte por CCAA | C4 |
| (e) ayuda a la demanda | 5-15 % del precio o la renta | C4 |
| (f1) rebaja ITP / IVA vivienda nueva | 1-4 puntos del precio; sin tipos vigentes por CCAA en data/raw: escenario genérico | C4 |
| (f2) impuestos a la construcción | rebaja del coste 2-6 %, cuota del coste en el precio 40-70 % | C4 |
| Reparto a alquiler | parque en alquiler 15-20 %; fracción de ΔQ al alquiler: (a) 10-30 %, (b) 30-70 %, (c) 80-100 %, (d) 100 % | C4 |
| Coste fiscal | s × compraventas 2025 × 90 m² × precio tasado (€/m²), sin efectos inducidos. Alquiler y oferta: sin base | C4 |

## Regla de «recomendación robusta» (adaptación declarada)

El encargo de V7 pedía robustez por PMG y jerárquico. R4 no identificó un largo plazo estable, así que se adapta: una combinación CCAA × instrumento es robusta solo si (i) la variación del esfuerzo es negativa en TODAS las extracciones de Monte Carlo y en los tres horizontes, y menor que -0,1 % a 10 años (materialidad), con la rejilla de $\varepsilon_s$, y (ii) lo mismo con la elasticidad regional cuando es utilizable. Si la regional no es utilizable, la robustez es «solo con rejilla» y se declara.
