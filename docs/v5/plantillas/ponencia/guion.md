# Ponencia: qué sabemos y qué no sobre la vivienda en España y València (guion)

**Borja Romero, economista.** Duración total: 20 minutos. <!-- check:cifra-libre -->
Regla del ponente: cada cifra se dice con su periodo y su capa; los veredictos son sobre afirmaciones, nunca sobre quién las dice; lo que funciona y lo que no, siempre en condicional.

## Bloque 0 · Apertura (0:00-1:30; diapositivas 1-2) <!-- check:cifra-libre -->
- Presentar las cuatro capas: hechos [C1], cotas [C2], efectos (ninguno en esta charla) y exploratorio [C4].
- Mensaje: «Hoy no diré qué causa la subida; diré qué se puede medir y hasta dónde».

## Bloque 1 · Hechos (1:30-6:00; diapositivas 3-5) <!-- check:cifra-libre -->
- Hogares frente a terminadas: {{dh_2125:valor}} más en {{dh_2125:periodo}} [C1]; terminadas entre {{terminadas_1924:rango}} [C1].
- Alquiler: el stock creció entre {{A23-A2:min}} y {{A23-A2:max}} en {{A23-A2:periodo}} [C1]; los contratos nuevos, más.
- Precio de compra: núcleo de fuentes {{A23-P2:valor}} en {{A23-P2:periodo}} [C1]; el INE da más y la diferencia no está descompuesta.

## Bloque 2 · Mitos del verificador (6:00-11:00; diapositivas 6-9) <!-- check:cifra-libre -->
- Recordar: se evalúa la afirmación; las mismas reglas para todas.
- «El alquiler se ha duplicado»: CONTRADICHA para el stock [C1].
- «Faltan cientos de miles de viviendas»: PARCIALMENTE [C1]; depende del periodo y de las bajas, que nadie mide bien: las demoliciones con licencia son {{E-T7-demol-2024:rango}} [C4].
- «El envejecimiento resolverá el problema» (ficha `T2-V1`): ANALIZADA, NO CONCLUYENTE [C4]; {{T2-H1:valor}} liberadas en 2026-2035, la mayoría fuera de las capitales. Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares.
- «Los topes bajan los alquileres» y «los topes reducen la oferta»: ANALIZADA, NO CONCLUYENTE [C4]; la validación quedó contaminada.

## Bloque 3 · Necesidades por territorio (11:00-15:30; diapositivas 10-12) <!-- check:cifra-libre -->
- Crecimiento de hogares {{B1-H4:valor}} en {{B1-H4:periodo}} [C2].
- Necesidad anual base {{T3-H5b:valor}} [C4], con rango; si parte de las liberadas no llega al mercado, {{T3-H5:valor}}. Entre {{T3-H9:min}} y {{T3-H9:max}} la producción actual. Lo que más pesa: cuántas vacías se pueden movilizar.
- València: {{E-B1-anual-Valencia:valor}} al año en la provincia [C4]; a 2030 el déficit nacional empeora en todos los escenarios [C2] (ficha `T4-V1`); por provincias empeora en {{T4-H3:valor}}, mejora en {{T4-H3:min}} y en {{T4-H3:max}} es indeterminado [C4]. A 2035, indeterminado [C4].

## Bloque 4 · Qué funcionaría y qué no (15:30-19:00; diapositivas 13-14) <!-- check:cifra-libre -->
- Matriz de instrumentos (D1): muchos instrumentos no son evaluables en el signo con los datos disponibles ({{D1-H02}} de {{D1-H01}}) [C4].
- Las ayudas generales a la demanda podrían trasladarse al precio en una parte que depende de la elasticidad de la oferta : clase `1`: {{D1-H11:rango}}; clase `2`: {{D1-H12:rango}}; clase `3`: {{D1-H13:rango}} [C4]; el extremo bajo corresponde a la literatura con oferta elástica y el alto a la de oferta rígida.
- La política por territorio (D2): la construcción adicional planificada cubriría en torno a {{D2-H11:valor}} de la necesidad [C4]; donde construir no es rentable, el instrumento sería distinto del que serviría donde hay freno de suelo.

- Versión de referencia v7.1 (atlas regional) [C4]: los precios de las comunidades se mueven sobre todo juntos y no se confirma ningún largo plazo regional ({{V71-S3-largo-confirmadas:num}} de siete hipótesis). En la simulación, las ayudas a la demanda bajan el precio neto del beneficiario y suben el de mercado ({{V71-S3-R6-e_ayuda_demanda-compra-precio10a:valor}}); el signo lo da la fórmula, lo informativo es la magnitud relativa. Los cambios entre versiones están en una sección única ([que_cambio](../que_cambio.md)).

## Bloque 5 · Cierre (19:00-20:00; diapositiva 15) <!-- check:cifra-libre -->
- Lo que no se puede afirmar. Dónde están los datos y el código. Preguntas.

**Pre-registro y versiones.** Las etiquetas git `prereg-v5` (pre-registro de las diferencias entre provincias, `docs/v5/prereg_B3.md`) y `v5.0` se crearon en el repositorio local el 10 de octubre de 2026 y se publicaron en el repositorio remoto el [fecha de publicación: pendiente]. El commit del pre-registro es anterior a cualquier resultado de ese análisis, pero una etiqueta local no es un sello de tiempo externo. Por eso, en versiones futuras el pre-registro se depositará además con sello de tiempo externo (OSF o Zenodo) antes de estimar.
