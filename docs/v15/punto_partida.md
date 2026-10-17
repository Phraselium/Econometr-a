# V15 · Punto de partida (fase 0)

Lectura crítica de V5-V14: qué sigue sin respuesta y por qué, qué resultados son frágiles y qué debilidades veo. Nada de esto corrige lo publicado. Lo que pudiera cambiar una cifra de la 1.0 queda para revisión (plan, D: ERRATA en una versión posterior, nunca reescribiendo). Fuentes: metodologia/historial_conclusiones.md, docs/limitaciones.md, docs/v9/cierre.md y revision_final.md, ERRATA.md, output/v5/cifras_clave.csv y output/v7/cuenta_especificaciones.md.

## 1. Preguntas sin respuesta y su causa

| Pregunta | Lo que hay | Causa principal | ¿Lo puede cambiar V15? |
|---|---|---|---|
| Efecto de la inmigración en precio y alquiler | v1-V9: C4, «no concluyente». Signo dependiente del control por población (L4). Instrumento de redes de origen débil a escala provincial (F efectiva 4,6 en V9-D4; F 3,5 en las provincias de entrenamiento de v6) | **Identificación** (instrumento débil, exposición posiblemente endógena) y **potencia** (17 CCAA, 50 provincias) | Solo si el shift-share municipal o por barrio (padrón de V11, BDO) da una primera etapa fuerte y pretendencias limpias. Si no, el nulo debe quedarse como nulo |
| Pisos turísticos | v3, v6, V8 y V9: C4. Pretendencias rechazadas en D2; D3 sin potencia y con placebo del mismo signo | **Datos**: falta exposición fechada y un resultado por barrio o código postal con frecuencia | Barcelona por barrio (HUT 2018-2026) y la reconstrucción del registro GVA de V12 dan exposición fechada. El cuello de botella es el resultado (precio o renta por barrio y periodo) |
| Topes de renta y zonas tensionadas | V9-D1b: −5,9 % en contratos nuevos. Supera pretendencias, placebo, permutación y Holm, pero no Honest DiD (M̄ de ruptura 0,5). V9-D1a: pretendencias rechazadas | **Identificación** (tendencias diferenciales) y pocos controles completos (20 municipios en D1a) | Con 2024-2026 y SDID o control sintético por municipio, hay más periodos posteriores y otra forma de construir el contrafactual. Riesgo: la Ley 12/2023 coincide con otros cambios |
| Tipos de interés | V7, V8 y V9: precio no distinguible de 0; alquiler, asociación negativa sin potencia | **Potencia** (18 países, o 17 CCAA con exposición poco variable) y medida de la sorpresa | Solo con exposición municipal o provincial a hipoteca variable que varíe de verdad. Si no hay datos, se descarta |
| Elasticidad de la oferta | v1 y v2: DOLS descriptivos; elasticidad de iniciadas ~0,8-1,4 sin instrumento | **Identificación**: no hay desplazador de demanda excluido ni restricciones físicas construidas | P1 con pendiente, agua y suelo protegido (MDT e INSPIRE) a escala municipal. Exige datos que hoy no están en el repositorio (ver fase 1) |
| Burbuja o exuberancia | v4, V7.2: GSADF en niveles explosivos, sin exuberancia con ajuste múltiple | **Concepto**: un test de exuberancia no identifica una burbuja | Poco: se puede mejorar la inferencia (bandas y fecha), no la interpretación |
| Predicción | Ningún modelo bate al AR(4) en la misma muestra (v1, K1 y V8) | **Variación y T**: series cortas y dominadas por la persistencia | P9 puede cerrar la pregunta con MCS y nowcasting, pero el resultado esperado es un nulo |
| Bono Alquiler Joven | No estimable (V9-D6) | **Datos** (edad exacta y receptores) | No, sin las solicitudes de docs/v9/solicitudes_transparencia.md |

## 2. Resultados previos frágiles

1. **v2/BI, alquiler +3,06 %/pp (inmigración, 2SLS).** Se citó durante varias versiones. Su F era 14,4 en la muestra de 49 provincias y 3,5 en las de entrenamiento de v6. K2 muestra que el orden alquiler > compra depende del 2SLS. Ya está en C4, pero conviene que ningún texto lo use como magnitud de referencia.
2. **V9-D1b, −5,9 % por los topes catalanes.** Es el resultado más cercano a C3. Su fragilidad está declarada: falla Honest DiD con M̄ = 1 (ruptura en 0,5). Además, el intervalo de Rambachan y Roth es una implementación propia con tamaño del 7,3 % en 400 réplicas, por encima del nominal. Una réplica con más periodos o con otra implementación puede moverlo en cualquier dirección.
3. **121 cifras C3s del SVAR de V8.** Valen solo bajo las restricciones de signo y de cero. Las bandas de casi todas las contribuciones incluyen el 0. La C3s es correcta como etiqueta, pero el lector puede sobrevalorarla.
4. **Elasticidades precio-alquiler (v6/M1b)**: 0,43-1,33 en FE y 1,6-2,1 en DOLS. Dependen de la especificación.
5. **Cambios de signo según el método**: empleo (EF − / PDS +), iniciadas (− 2021-23 / + 2016-23) y renta (PIP sin signo estable). Son señales de que no hay efecto estable, no resultados.
6. **Déficit 2021-2024 (C2: 389-711 mil).** Depende de siete correcciones del salto de la EPA. La amplitud es la conclusión honesta.
7. **Comparaciones múltiples entre versiones.** Desde v1 se han registrado al menos 43.510 especificaciones hasta V7.2, más las de V8 (multiverso ≤ 50.000) y V9. La corrección (Holm/BH) se aplica dentro de cada versión, nunca entre versiones. La inmigración y los topes se han contrastado en cinco versiones o más. Un «sí» aislado tras varios «no» debe leerse con esa historia.

## 3. Errores o debilidades que no están en ERRATA (para revisión; no se corrigen aquí)

1. **Cifras C1 que no cumplen la definición de C1** (capas.md: dos fuentes independientes como mínimo; una estadística oficial de fuente única es C4):
   - E-T7-prod: una sola fuente (MIVAU, terminadas libres y protegidas);
   - V8-M8-cv-p03/p12-P5-acum-alt y -acum-mivau: cada una describe una sola serie (Registradores o MIVAU);
   - VER-A23-V2-1 y VER-A23-V2-2: recuentos internos de municipios, no hechos con dos fuentes;
   - V10-ATL-A1 a A3: el «contraste» con Eurostat ilc_lvho07 procede de la misma encuesta (EU-SILC/ECV), así que no es una fuente independiente;
   - V9-D7-c1-dif: la ECP a 1-1-2022 se apoya en el censo 2021; la independencia es dudosa.

   **Efecto:** no cambian valores, sí capas. Cambiar la capa de una cifra de la 1.0 es una corrección de la 1.0 y debe ir a ERRATA en una versión posterior. Queda **pendiente del autor**: tareas_autor.md, condición de parada «error de versiones anteriores».
2. **p_bde = p_tasado** (limitaciones.md): la serie larga del BdE es el valor tasado del MIVAU. Toda comprobación que las trate como dos fuentes estaría duplicando una. No he encontrado ninguna C1 que lo haga; queda para la auditoría de la fase 1.
3. **Medidas de alquiler mezcladas entre versiones.** El IPC de alquiler y SERPAVI miden el stock de contratos vigentes. Las fianzas (Incasòl, GVA) y el IPVA «nuevo» miden contratos nuevos. Varias filas del historial comparan signos entre medidas distintas. Lo señala K2, pero no todos los textos lo dicen.
4. **Valor tasado como precio principal** en paneles provinciales (v6, K2 y V8-M8): mide tasaciones, no transacciones. El sesgo de composición y el suavizado de las tasaciones no se han cuantificado (fase 1).
5. **Validación sellada.**
   - La de v2 se reconstruyó en el incidente D3 de V13; sus evaluaciones previas siguen registradas.
   - Las muestras de v6 (último año y 11 provincias) ya se evaluaron.
   - Para V15 no queda ninguna muestra limpia hasta que se publiquen datos posteriores al depósito del pre-registro (fase 3.3).
6. **Reparto espacial de V12-B1.** El reparto de la contabilidad demográfica a escala fina usa un único criterio. El plan pide un reparto alternativo por viviendas del Catastro (fase 1.2).
7. **AEAT 2013-2015.** Las unidades de los ficheros municipales de esos años son dudosas (V12-F0). Solo afecta a análisis de titularidad (C4).

## 4. Qué implica para V15

- Priorizar preguntas donde **un dato nuevo cambia la identificación** frente a V9: exposición fechada por barrio, más periodos posteriores a la regulación y exposición municipal a tipos. No repetir con otro estimador las preguntas ya cerradas por falta de identificación.
- Tomar el **nulo bien identificado como resultado válido**: inmigración, tipos y predicción tienen alta probabilidad de quedarse en nulo.
- **Controlar la multiplicidad entre versiones**: el pre-registro de V15 debe declarar cuántas veces se ha contrastado antes cada hipótesis y fijar las confirmatorias con Holm sobre un número pequeño.
