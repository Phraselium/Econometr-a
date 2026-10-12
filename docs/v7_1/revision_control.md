# Revisión de control de V7.1 (revisor independiente, revisión única)

Fecha: 2026-10-12. Alcance: cuatro ejes (cifras y capas, neutralidad, lenguaje causal, enlaces y estructura), revisados por muestreo. No se ha leído data/sealed ni se han ejecutado `make all` ni `make v7`. Lo que sí se ha ejecutado:

- `python3 -m pytest -q tests/v7_1`: 10 tests superados.
- `python3 src/v3/check_texto.py`: 0 errores.

## Comprobaciones superadas (muestreo)

**Cifras.** Se contrastaron 24 cifras con publicacion/cifras_clave.csv (V71-*, V7-*) y todas coinciden en valor y capa (C4):

- R² del componente común: 93,6 % y 86,1 %, con sus rangos 81,0-97,8 y 64,9-97,4.
- Hipótesis de largo plazo confirmadas: 0 de 7. Coeficientes H7-A1, A2, C1 y C4 del atlas_resumen.
- Comunidades con mejor modelo que la base más exigente: 6 de 17 y 5 de 17.
- Comunidades donde no se descarta I(2): 8 de 17 y 9 de 17.
- Variación del precio de mercado: 4,4 % (ayudas a la demanda) y 1,1 % (rebaja de ITP/IVA). Variación del esfuerzo con ayudas: -5,3 %.
- Coste anual: 378,2 y 93,3 M€/año. Coste por punto: 76,4 y 82,4 M€/año.
- Efecto por 10.000 viviendas en alquiler: -1,7 (vacías) y -3,2 (vivienda pública).
- Robustez de vacías: 17 de 17. Robustez de ayudas a la demanda: 0.
- Monte Carlo: sesgos de 53,9 / 43,8 / 20,3 / 15,8 / 10,9 / 16,8 %, coberturas de 0,37 / 0,12 / 0,89 / 0,92 / 0,88 / 0,86, y valor crítico de -8,83.

**Dosis y coste.** Las medianas nacionales se recalcularon desde output/v7_1/S1/dosis_coste.csv y coinciden con S1/resumen.md y con atlas_resumen.md. publicacion/dosis_coste.csv es idéntico al de output. Todas las filas de vacías, vivienda pública, turísticos, construcción y ayudas en alquiler llevan «no estimable». resultado.json: capa C4, EXPLORATORIO.

**Neutralidad.** No se nombra ningún partido ni ninguna persona evaluada. No hay adjetivos valorativos. El texto dice explícitamente «no se recomienda ningún instrumento».

**Lenguaje causal.** No hay verbos causales fuera de negaciones. Las ayudas y la rebaja de ITP/IVA aparecen como «escenario condicional», con la nota de que el signo lo fija la fórmula de incidencia (salvo en H3). El componente común se presenta como «descripción, no un modelo».

**Estructura.** Ninguno de los ficheros revisados dice que la v6.2 sea la referencia: v6.2 figura como histórica en MAPA.md, historico/INDICE.md y CLAUDE.md. No hay enlaces rotos en LEEME_PRIMERO.md, README.md, docs/MAPA.md, historico/INDICE.md ni en los cinco entregables principales.

## Hallazgos

| id | eje | fichero:línea | hallazgo | severidad | corrección propuesta |
|---|---|---|---|---|---|
| H1 | 1 | publicacion/que_cambio.md:53 | Dice que el efecto por 10.000 viviendas en compra es «-0,61 puntos % (mediana; igual en los cuatro instrumentos por construcción de la fórmula)». Según cifras_clave y S1/resumen.md solo es igual en tres (vacías, vivienda pública, turísticos). En construcción es -0,78 (V71-S1-a_construccion-compra-efecto_10k = -0,785). La marca `check:cifra-libre` dejó la cifra fuera del control. | media | Escribir «igual en vacías, vivienda pública y turísticos (-0,61); -0,78 en construcción adicional». Quitar `cifra-libre` y enlazar la cifra a su id. Corregir en la fuente output/v5/que_cambio.md y regenerar. |
| H2 | 1 | publicacion/una_pagina.md:19 | Dice que en los instrumentos «de oferta» el coste no es estimable. Pero la rebaja de impuestos y costes de construcción (f2), que es de oferta, sí tiene coste estimado: 14,6 M€/año (V71-S1-f2_...-coste_anual_meur). Además, «su coste y su dosis están declarados» no vale para las ayudas en alquiler, cuyo coste no es estimable. | media | Sustituir «oferta» por «cantidad (construcción, vacías, vivienda pública, turísticos)». Añadir «en compra» tras «su coste». |
| H3 | 3 | publicacion/una_pagina.md:19 | La frase sobre las ayudas a la demanda va en indicativo y no lleva la nota «el signo lo fija en gran parte la fórmula de incidencia». Esa nota sí aparece en lo_que_sabemos, policy_brief y que_cambio. | media | Añadir «(escenario condicional; el signo lo fija la fórmula de incidencia; C4)». |
| H4 | 1 | publicacion/policy_brief.md:46 | Dice que la cobertura del 29,7 % usa la «versión v5 de la necesidad, no la recalculada en v5.1». Esto contradice informe_tecnico.md:440 («desde v6.3, D2 usa la misma necesidad provincial que el titular, v5.1 T3») y las fuentes de D2-H11 en cifras_clave (output/v5_1/T3). Además, el 29,7 % es el central de un rango (11,9-47,5 %) que no se cita. | media | Alinear el texto con v6.3/T3, citar el rango 11,9-47,5 % y comprobar que la cifra es la vigente. Si la cifra cambia, va a ERRATA.md. |
| H5 | 1 | publicacion/que_cambio.md:59 (sección v7.1) y lo_que_sabemos.md:77-80 | La lista de costes omite el tercer instrumento con coste estimado, f2 (14,6 M€/año; coste por punto 15,3), y su advertencia de que el efecto por 100 M€ está sobrestimado por construcción. El lector deduce que solo hay dos instrumentos con coste. | baja | Añadir f2 con la advertencia de S1/resumen.md («no debe leerse como el más eficiente por euro»). |
| H6 | 4 | LEEME_PRIMERO.md:13-35 | Los itinerarios (ciudadano, periodista, revisor, técnico) no enlazan el policy brief, el atlas regional (atlas_regional/), la ponencia ni el artículo. Falta un perfil de responsable de decisiones o gestor público. | media | Añadir un itinerario «Gestor público» (policy_brief y atlas_regional/atlas_resumen con la ficha de su comunidad) y enlazar la ponencia y el artículo. |
| H7 | 1 | publicacion/que_cambio.md:32 y :33 | Unidades duplicadas o mal formadas: «0,66 correlacion» y «18,9-20,3 años de alquiler años». | baja | Corregir la plantilla de unidades: «0,66», «18,9-20,3 años de alquiler». |
| H8 | 1 | publicacion/nota_metodologica.md:149 y :200 | En la línea 149, «-8,83 estadístico t» lleva la unidad pegada. En la 200, «t de MG = -6.56» y «-3.12» usan punto decimal y faltan tildes («critico», «valido»). | baja | Formato español y tildes en la plantilla de R4. |
| H9 | 1 | publicacion/informe_tecnico.md:440 | Unidad duplicada: «210.424 viviendas/año viviendas/año». | baja | Corregir la plantilla. |
| H10 | 1 | publicacion/atlas_regional/01_Andalucia.md:139-148 (y el resto de fichas de CCAA) | La tabla de R6 rotula el mercado como «precio» y la tabla S1 de la misma ficha como «compra». La etiqueta interna `precio` llega al lector. | baja | Mapear `precio` a «compra» en la tabla de R6 del atlas. |
| H11 | 3 | publicacion/lo_que_sabemos.md:81 y policy_brief.md:63 | «La movilización de vacías es robusta en 17 de 17» puede leerse como robustez estadística. Es una propiedad de la rejilla (el esfuerzo baja en todas las extracciones). | baja | Escribir «robusta en la rejilla simulada (C4) en 17 de 17». |
| H12 | 4 | publicacion/verificador/verificador.md:3 y verificador_v7_1.md:5 | El título dice «(v5)» y el complemento lo llama «verificador de v6.2». No afirma que v6.2 sea la referencia, pero la etiqueta es inconsistente dentro de publicacion/. | baja | Titular «Verificador (fichas v5-v6.3, vigentes en v7.1)» en ambos. |
| H13 | 3 | publicacion/policy_brief.md:38 y lo_que_sabemos.md:87 | «Las ayudas a la demanda mejoran al beneficiario como grupo» va como [C2] (rejilla v5). En la sección v7.1 la misma lectura es C4. No hay promoción de capa, porque son resultados distintos, pero sin aclararlo el lector ve una afirmación con dos capas. | baja | Añadir «(signo en la rejilla v5, C2; magnitudes v7.1, C4)». |

## Veredicto

**APROBAR CON CORRECCIONES.** No hay hallazgos de severidad alta:

- ninguna cifra contradice cifras_clave en su capa;
- no hay problemas de neutralidad;
- no hay lenguaje causal por debajo de C3;
- ningún fichero presenta v6.2 como referencia.

Correcciones antes de difundir, por prioridad:

1. **H1 y H2.** Son afirmaciones numéricas inexactas en entregables de difusión. Hay que corregirlas en la fuente y regenerar con `make publicacion`.
2. **H4.** Contradicción entre el policy brief y el informe técnico sobre qué necesidad usa D2.
3. **H3 y H6.**
4. **H5 y H7-H13.** Formato y precisión.

Recomendación adicional: restringir `check:cifra-libre` a unidades de normalización sin valor numérico de resultado. H1 se coló por esa exención.
