# V16 · F2.2 Contabilidad, no causalidad (C4)

Capa C4, descriptiva: son identidades contables y resúmenes de comovimiento, sin interpretación causal. Generado por `src/v16/f2_contabilidad.py` (SEED 20261010). La descomposición del esfuerzo es de otro módulo (`f2_esfuerzo`).

## 1. Hogares: demografía, jefatura y nacionalidad

**Qué amplía.** V12-B3 ya descompuso 2011-2021 con los dos censos (lo ya visto: V12-B3-hogares-*; no se repite). Aquí se añade 2021-2026 con ECP y EPA, la separación extranjera/española (V12 solo separaba edad) y 2002-2021 con EPA.

**Método.** H = k·Σ N·m·s·h (tamaño N, cuota de nacionalidad m, estructura por edad s dentro de cada nacionalidad, tasa de jefatura h por nacionalidad y quinquenio de edad del Censo 2021). Los tres factores demográficos se reparten por Shapley (rango = 6 órdenes); la jefatura es el residuo exacto H1 − k·V(1,1,1). No hay tasas de jefatura por edad después de 2021, así que la jefatura es una tasa agregada a población constante, no una tasa por edad. La suma reproduce el cambio observado (error máximo 5.8e-11 hogares; test).

**España, 1-1-2021 a 1-1-2025 (ECP).** <a id="v16-con-hog-cambio"></a>Cambio observado 981 823 hogares (EPA: 1 062 300; difiere 8.2 %). <a id="v16-con-hog-poblacion"></a>Población 670 187 (662 247 a 678 200); <a id="v16-con-hog-composicion-nacionalidad"></a>composición por nacionalidad -80 764; <a id="v16-con-hog-estructura-edad"></a>estructura por edad 371 922; <a id="v16-con-hog-jefatura"></a>residuo de jefatura 20 478 (0.11 % de los hogares a población constante). La población extranjera cambia 1 482 129 personas y la española 206 256; su cuota pasa de 11.3 % a 14.0 %. A tasas de jefatura iniciales, la variación de población extranjera suma 540 052 hogares y la española 421 293 (vista aditiva exacta). La composición resta porque las tasas de jefatura por edad del Censo 2021 son menores en la población extranjera; "composición" mezcla migración y cambios de nacionalidad.

**ECP frente a EPA.** <a id="v16-con-hog-ecp-epa-discrepancia"></a>Los dos discrepan en el nivel (18,54 M frente a 18.61 M hogares en 2021T1) y 8.2 % en el cambio; se reportan por separado (`hogares_ecp_*`, `hogares_epa_*`). Con EPA el residuo de jefatura es 97 285 (ECP: 20 478). Hasta 1-1-2026 (ECP): cambio 1 222 836, población 852 671, composición -98 230, estructura 474 450, jefatura -6 055.

**CCAA (11 sin provincias selladas v6; las 8 restantes se excluyen por K8).** <a id="v16-con-hog-ccaa-jefatura-pct"></a><a id="v16-con-hog-ccaa-poblacion-pct"></a>El residuo de jefatura va de -0.21 % a 1.36 % de los hogares iniciales; la parte de población en el cambio, de -31 % a 92 %. Provincias (41): `hogares_ecp_2021_2025.csv`. EPA no publica hogares por CCAA en la base.

**2002-2021 (EPA, nacional).** <a id="v16-con-hog-epa-2002-2021-cambio"></a>Cambio 4 276 400 hogares: <a id="v16-con-hog-epa-2002-2021-poblacion"></a>población 2 353 708, <a id="v16-con-hog-epa-2002-2021-composicion-nacionalidad"></a>composición -202 133, <a id="v16-con-hog-epa-2002-2021-estructura-edad"></a>estructura 2 012 790, <a id="v16-con-hog-epa-2002-2021-jefatura-residuo"></a>jefatura 112 035 (padrón en 4 grupos de edad). Con las tasas del Censo 2011 la jefatura sería 399 827: el reparto depende de la tasa de referencia. <a id="v16-con-hog-epa-2014-2021-jefatura"></a>En 2014-2021 el residuo es -677 776, compatible con la ruptura de la EPA en 2021T1 (recalibración al Censo 2021); no se interpreta. 
<a id="v16-con-mig-emcr-saldo"></a>**Migración (EMCR).** Saldo exterior 2021-2024: 2 186 663 personas; la población extranjera ECP crece 1 482 129 (incluye cambios de nacionalidad); no se concilian. Solo se usa EMCR desde 2021 (ruptura de nivel antes: K6).

## 2. Precio: parte común y parte local

**Muestra.** Valor tasado MIVAU, trimestral, 33 provincias con serie completa de las 38 no selladas (las 11 de v6 se excluyen, K8; Cantabria no figura en la serie; 5 provincias con huecos en 2012 solo entran interpoladas, MARCADO, en robustez). Nominal salvo la variante real (deflactor nacional).

**Ya visto.** V8-M1 estimó el factor común de 17 CCAA (precio real, periodos P1-P5). Aquí: provincias, tres periodos nuevos, DynamicFactor y residuo local.

| Periodo | Cuota PC1 (IC95 bootstrap) | Azar (media) | p BH | Factores Bai-Ng | R² mediano prov. (mín.-máx.) | Trimestral | Real | Interpolada (38) |
|---|---|---|---|---|---|---|---|---|
| 2007-2013 | <a id="v16-con-precio-cuota-pc1-2007-2013"></a>71.4 % (40.0-82.9) | 11.6 % | 0.001 | 4 | <a id="v16-con-precio-r2-prov-2007-2013"></a>76 % (16-94) | 36.0 % | 61.2 % | 70.2 % |
| 2014-2019 | <a id="v16-con-precio-cuota-pc1-2014-2019"></a>52.9 % (24.8-63.1) | 12.5 % | 0.001 | 4 | <a id="v16-con-precio-r2-prov-2014-2019"></a>53 % (1-88) | 19.3 % | 45.0 % | 48.0 % |
| 2020-2026 | <a id="v16-con-precio-cuota-pc1-2020-2026"></a>80.9 % (40.2-86.1) | 12.1 % | 0.001 | 3 | <a id="v16-con-precio-r2-prov-2020-2026"></a>83 % (51-96) | 45.4 % | 81.6 % | 79.9 % |

Cuota = parte de la varianza de la tasa interanual de ln precio que recoge el PC1 (series tipificadas). Con N = 33 y T = 24-28 la cuota está sesgada al alza incluso sin factor (columna azar). Bai-Ng alcanza el máximo permitido (4) en la tasa interanual, que es muy persistente: ese número no es fiable. La cuota depende de la tasa: con la variación trimestral baja a 19-45 % (ruido de medida trimestral).

**DynamicFactor (statsmodels, 1 factor AR(2), 2007T1-2026T2, tasa trimestral; convergió: True).** Correlación absoluta del factor con el PC1: 0.995. <a id="v16-con-precio-dfm-r2"></a>R² medio con el factor: 2007-2013 36 % (PC1 global 36 %); 2014-2019 18 % (PC1 global 18 %); 2020-2026 45 % (PC1 global 45 %). Se estima una sola vez en toda la muestra (N > T por periodo); las cuotas por periodo salen de ese factor.

**Residuo local.** Es lo que queda tras quitar el factor. <a id="v16-con-precio-local-ccaa"></a>Sus correlaciones entre provincias de la misma CCAA son 0.11, 0.02 y 0.10 (por periodo), frente a -0.05, -0.04 y -0.05 entre CCAA distintas: las del mismo territorio autonómico son algo mayores, pero pequeñas: el residuo es en su mayor parte específico de cada provincia. En 2020-2026 las provincias con mayor cuota local son 49, 06, 25, 01 (49 %, 46 %, 36 %, 33 %). Contabilidad exacta del cambio acumulado de ln precio (tasa trimestral, factor sin centrar; `precio_contabilidad_nivel_provincia.csv`): en 2020-2026 la parte del factor es 31 puntos de ln x100 en la mediana provincial (local -1; local mín.-máx. -11 a 14).

**Contraste con V8 (17 CCAA, precio real, interanual, `precio_puente_v8.csv`).** P2: V8 45 % (banda 68 % 42-54); 9 CCAA sin provincias selladas 53 %; 33 provincias 40 %; P3: V8 60 % (banda 68 % 48-67); 9 CCAA sin provincias selladas 55 %; 33 provincias 45 %; P5: V8 93 % (banda 68 % 87-95); 9 CCAA sin provincias selladas 95 %; 33 provincias 89 %. 
<a id="v16-con-precio-v8-dif-pp"></a>Con 33 provincias la cuota difiere de V8 entre -15 y -4 pp; 2 de 3 caen fuera de la banda del 68 % de V8. Discrepan: se informan ambas. Con 9 CCAA agregadas la cuota es parecida a la de V8; con 33 provincias es menor. Una explicación posible, no contrastada, es que las CCAA agregan provincias y promedian parte del residuo local.

## Límites
- Contabilidad, no causalidad: ni la composición por nacionalidad ni el factor común admiten lectura causal. - Jefatura: residuo agregado; la tasa de referencia es la del Censo 2021 (2011 como sensibilidad). - Las 8 CCAA con provincias selladas (K8) no se calculan en hogares; el panel de precios no incluye las 11 provincias v6. - Valor tasado nominal; la variante real usa el deflactor nacional. - Registro de especificaciones: `registro.csv`; p frente a azar por BH.
