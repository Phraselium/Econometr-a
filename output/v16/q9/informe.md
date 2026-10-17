# Q9 · Fundamentales y burbuja (C4, pendiente de evaluación sellada)

**Capa.** C4 exploratorio. Sin lenguaje causal. Solo Q9-g tiene inferencia APTA (GSADF con bootstrap salvaje). Q9-c, CIPS y el GSADF por provincia son **descriptivos** (sin p-valor ni IC).

## Q9-g · GSADF del factor común (APTO)
<a id="q9g"></a>Ratio: ln(valor tasado provincial) − ln(IPC de alquiler provincial), 33 provincias, 2002T1-2026T2 (T = 98); factor = 1ª componente principal (87,4 % de la varianza).
GSADF = 5,919; valor crítico bootstrap (95 %, B = 499) = 3,340; p bootstrap = 0,004. Lectura: **explosivo**.
Fechas con BSADF sobre su valor crítico puntual: 2010Q1, 2010Q2, 2010Q3, 2010Q4, 2011Q1, 2011Q2, 2011Q3, 2011Q4, 2012Q1, 2012Q2, 2012Q3, 2012Q4, 2013Q1, 2013Q2, 2013Q3, 2013Q4, 2014Q1, 2014Q2, 2014Q3, 2014Q4, 2015Q1, 2015Q2, 2015Q3, 2015Q4, 2016Q1, 2016Q2, 2016Q3, 2016Q4, 2017Q1, 2017Q2, 2017Q3, 2017Q4, 2018Q1, 2018Q2, 2018Q3, 2019Q1, 2019Q2, 2019Q3, 2019Q4, 2020Q1, 2025Q1, 2025Q2, 2025Q3, 2025Q4, 2026Q1, 2026Q2.
Heterocedasticidad (ARCH-LM): LM 33,74, p 0,000: heterocedástico (ARCH-LM p < 0,05).
Robustez: media de los ln-cocientes, GSADF 6,200 (vc 3,170, p 0,002). Alternativa SERPAVI anual (T = 14, sin potencia): GSADF 0,878 (vc 1,147, p 0,092).
Cautela de lectura: el factor tiene una tendencia marcada y el GSADF (con constante, sin tendencia) puede rechazar con tramos de ascenso sostenido sin que sean explosivos en sentido estricto; el bootstrap salvaje impone raíz unitaria sin deriva. Provincias con ambas series completas: 33 de las 38 de entrenamiento (D4 las daba por 38; el resto carece de valor tasado trimestral).
«No explosivo» significa «no detectado con esta potencia», nunca «no hay burbuja»; «explosivo» exigiría BH/BY y réplica sellada. Ya visto: GSADF por CCAA de V7.2.

## GSADF por provincia (descriptivo)
<a id="q9p"></a>Sin p-valor (herramienta no validada por provincia; potencia casi nula con corrección múltiple). Por encima del valor crítico bootstrap individual, **sin ajuste múltiple**:
valor_tasado/IPC_alquiler (trimestral): 18 de 33; valor_tasado/SERPAVI (anual, T=14): 1 de 30. Detalle en q9_gsadf_provincias.csv.

## Q9-c · elasticidad de largo plazo (NO APTO: puntual)
<a id="q9c"></a>CS-ARDL (p = 2, medias transversales de y y x): θ = 0,838 (media entre 33 provincias); mediana entre provincias 0,557.
Multiverso (14 restantes de las 15 ejecutadas): mediana -0,544, rango [-1,436; 0,950], mismo signo 0,14.
Por estimador (mediana): CS-ARDL 0,838; MG -0,686; PMG -0,550. Se ejecutan 15 de las 36 pre-registradas (D4).
CIPS descriptivo (sin vc): ratio -2,18; ln valor tasado -1,61; ln IPC alquiler -2,17.
Correlación transversal media de Δln valor tasado: 0,49 (dependencia fuerte: motivo del uso de medias transversales).

## Regla de hallazgo
Q9-g: (a) p bootstrap sin ajuste = 0,004, q pendiente del BY del orquestador; (b) no aplica (prueba de explosividad: sin magnitud); (c) sellada: pendiente. Q9-c: sin p-valor ni IC; (b) no aplica. Resultado: C4 descriptivo.
