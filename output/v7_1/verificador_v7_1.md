# Verificador V7.1 (fichas de V7, con dosis y coste en V7-V2; ficha de burbuja de v7.2)

Fichas añadidas en V7, actualizadas en v7.1. Complementan el verificador principal (fichas v5-v6.3, vigentes en v7.1; output/v5/verificador), cuyos recuentos no cambian.

## V7-V1 · Determinantes regionales de largo plazo

**Afirmación evaluada:** En cada comunidad autónoma, el precio y el alquiler dependen a largo plazo sobre todo del empleo y de la población.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C4)

**Magnitud:** Paneles de 17 CCAA, 2007T1-2026T2 (MG con demeaning, PMG y CS-DL). Ninguna de las 7 hipótesis de largo plazo se confirma tras Holm y triangulación. Rango del coeficiente del empleo en alquiler: 0,003 a 0,088; en compra: -0,46 a -0,06. La velocidad de ajuste no es significativa frente al valor crítico simulado.

**Intervalo:** rango entre estimadores (output/v7/R4/*/hipotesis.csv)

**Límites:** Con un factor común I(1) de cargas heterogéneas ningún estimador es apto en el Monte Carlo (R2); I(2) no descartado en 8 de 17 CCAA.

**Regla:** Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE. Muestra regional ya vista en v1; la validación limpia es diferida (make evaluate_v7).

**Evidencia:** output/v7/R4/alquiler/resumen.md; output/v7/R4/compra/resumen.md; docs/v7/validacion_herramientas.md

## V7-V2 · Ayudas a la compra

**Afirmación evaluada:** Las ayudas directas a la compra abaratan la vivienda.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C4)

**Magnitud:** Simulación de traslado (rejilla de elasticidades de v5, C4), a 10 años, mediana entre CCAA: el esfuerzo neto del beneficiario varía -5,3 %, pero el precio de mercado sube 4,4 % (afecta a quien no recibe la ayuda). Dosis: todas las compraventas de 2025 (mediana 26.678 por CCAA) con una ayuda del 5-15 % del precio; coste fiscal anual aproximado 378 M€ por CCAA (mediana; rango entre CCAA 68-2.915); por cada 100 M€ anuales el precio de mercado sube 1,36 puntos (mediana). El signo lo fija la fórmula de incidencia (C4).

**Intervalo:** p5-p95 del esfuerzo: -9,4 a -2,5 %

**Límites:** Elasticidad de oferta regional no utilizable (DOLS fuera de [0; 5]); parámetros supuestos.

**Regla:** Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE. Muestra regional ya vista en v1; la validación limpia es diferida (make evaluate_v7).

**Evidencia:** output/v7/R6/impactos.csv; output/v7/R6/metodo.md; output/v7_1/S1/dosis_coste.csv; output/v7_1/S1/resumen.md

## V7-V3 · Tipos de interés y regiones

**Afirmación evaluada:** Las subidas de los tipos de interés abaratan la vivienda más en las regiones con más hipotecas.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C4)

**Magnitud:** Proyecciones locales de panel (17 CCAA) con exposición hipotecaria 2015-2019: en compra, 2 horizontes con q de BH < 0,10 que no resisten a Driscoll-Kraay; en alquiler, ninguno. El signo depende de cómo se construye el shock.

**Intervalo:** output/v7/R4b/lp_*.csv

**Límites:** Shock = residuo AR(2) del tipo nacional (desviación declarada); 17 unidades.

**Regla:** Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE. Muestra regional ya vista en v1; la validación limpia es diferida (make evaluate_v7).

**Evidencia:** output/v7/R4b/lp_compra.csv; output/v7/R4b/resumen.md

## V72-BURBUJA · Burbuja de precios: nacional y regional juntos

**Afirmación evaluada:** Hay una burbuja en el precio de la vivienda en España.

**Veredicto:** ANALIZADA, NO CONCLUYENTE (C4)

**Magnitud:** NACIONAL (2007T1-2026T2; reverificado: 14 de 14 series idénticas a v5). Los cocientes precio/renta y precio/alquiler muestran exuberancia sin ajuste en 1 de 4 (y 1 más con p en el borde de 0,05, a menos de dos errores típicos de Monte Carlo), y en 0 tras BH en la familia de 8 (sensibilidad con la familia de 4 cocientes: 1). Frente a valores de referencia con tipos de interés (descuento del alquiler, cuota sobre renta): 0 de 4. Los niveles de precio, sin fundamentales, son explosivos tras BH en 0 de 2. REGIONAL: 0 de 34 series de CCAA con exuberancia tras BH (6 sin ajuste; panel 2007-2026); en v6, con otra muestra (provincias de entrenamiento, 2015-2024, T=40), 0 de 11 CCAA.

**Intervalo:** —

**Límites:** T=78 (T=40 en v6); ADF con un rezago; sin renta por CCAA; los resultados regionales de v5 y v6 usan muestras distintas y no son comparables entre sí. 4.999 réplicas (con 499, hasta la 1.0, los recuentos cambiaban con la semilla: output/v16/b4_gsadf/); un p en el borde de 0,05 no se estabiliza con ningún número finito de réplicas. El valor tasado de Navarra falta en 2015-2018: su serie usa el tramo continuo más largo (2007T1-2014T4, T=32); el IPV de Navarra usa 2007T1-2026T2 desde la errata de V16.

**Regla:** No se puede afirmar que haya una burbuja: la exuberancia de los cocientes nacionales no sobrevive al ajuste múltiple, frente a los valores con tipos no la hay, y un test de exuberancia no identifica sobrevaloración ni su causa. Tampoco se puede afirmar que NO la haya: que el contraste no rechace tras el ajuste no demuestra que el precio esté alineado con sus fundamentales (la potencia es baja con T=78 y hay series exuberantes sin ajuste), el valor fundamental usado es una referencia simple con supuestos propios y la muestra es corta para el ciclo.

**Evidencia:** output/v7_2/gsadf/reverificacion.csv; output/v5/R1B/tablas/gsadf_corregido.csv; output/v5/E/hechos.json (E-V6-M1B-GSADF-*)
