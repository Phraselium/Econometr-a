# Verificador V7.1 (fichas de V7, con dosis y coste en V7-V2)

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
