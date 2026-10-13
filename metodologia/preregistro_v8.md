<!-- Generado por `make publicacion` desde docs/v8/hipotesis.md. No editar a mano: se regenera y un test lo comprueba. -->

# Pre-registro V8: por qué ha subido el precio de la vivienda y el alquiler (factores, periodos y factor común)

Fecha de redacción: 2026-10-13. Se escribe ANTES de cualquier estimación con datos reales de V8. Solo se han visto datos para describir su cobertura en F1.

- **Versión vinculante.** La del commit con la etiqueta local `prereg-v8`. Su fecha verificable será la de la release o el DOI que cree el autor (docs/v8/notas_release.md).
- **Desviaciones.** Se anotan en docs/v8/desviaciones.md, con su motivo y la fecha, antes de ver el resultado afectado.

## 1. Preguntas y orden de prioridad

1. **Peso de cada factor** en la subida del alquiler y del precio de compra por periodo, y cuál es el más relevante con un criterio explícito, o por qué no se puede designar. Factores:
   - demanda demográfica;
   - empleo y renta;
   - crédito y tipos;
   - oferta;
   - demanda externa y extranjera;
   - turismo;
   - factor europeo.
2. **Ecuaciones significativas y robustas por periodo**, sin hallazgos por azar.
3. **El componente común** que domina la subida (España frente a la zona euro).

**Ámbitos:** nacional, 17 CCAA, provincias de la Comunitat Valenciana (03, 12, 46) y València ciudad. Todos los cruces se hacen por código INE.

## 2. Capas

| Capa | Exige |
|---|---|
| C1 | dos o más fuentes |
| C2 | cota con supuestos |
| C3 | instrumento externo, o diseño que supera sus pruebas (primera etapa F efectivo ≥ 10 o intervalo AR informativo; pretendencias; placebos) |
| C3s | identificación por restricciones de signo o de cero explícitas: el efecto vale solo bajo esos supuestos |
| C4 | exploratorio o asociación |

Hay lenguaje causal solo en C3 y C3s; en C3s, condicionado a los supuestos. Ningún resultado se oculta por no ser significativo.

## 3. Periodos pre-registrados

| Código | Periodo | Descripción |
|---|---|---|
| P1 | 1995T1-2007T4 | expansión y crédito |
| P2 | 2008T3-2013T4 | crisis financiera y ajuste |
| P3 | 2014T1-2019T4 | recuperación |
| P4 | 2020T2-2022T2 | pandemia y reapertura |
| P5 | 2022T3-último (2026T2) | subida de tipos y presión demográfica |

- **Rupturas fijas.** EPA 2021T1 (variable ficticia de nivel en las variables EPA) y COVID 2020T2-2020T4.
- **Huecos.** 2008T1-2008T2 y 2020T1 no pertenecen a ningún periodo (transición). Se reportan, pero no entran en la atribución por periodo.

## 4. Datos y medidas

- **Precio de compra.**
  - Medida principal: valor tasado del Ministerio (desde 1995T1).
  - Alternativas: IPV del INE (desde 2007); Registradores (media móvil de 4 trimestres) y Notariado (semestral), donde existan.
  - El precio de vivienda libre del BdE coincide con el valor tasado (republicación): no cuenta como segunda fuente.
- **Alquiler.**
  - Medida principal: IPC de alquiler (desde 2002).
  - Alternativas: SERPAVI anual, contratos nuevos (fianzas de Cataluña y de la Comunitat Valenciana).
- **En términos reales.** Deflactor principal: IPC general. Alternativo: deflactor del PIB.
- **Variables de cada familia de factores:**

| Familia | Variables |
|---|---|
| Demografía | población, población extranjera, llegadas, hogares, jóvenes que viven con sus padres |
| Empleo y renta | ocupados EPA, renta y PIB, salarios |
| Crédito y tipos | tipo hipotecario, Euríbor, tipo del BCE, crédito nuevo y stock, crédito a promotores, encuesta de préstamos bancarios (BLS) |
| Oferta | visados, iniciadas, terminadas, costes de construcción |
| Demanda externa | compras de extranjeros y no residentes |
| Turismo | turistas internacionales, viviendas de uso turístico (VUT, desde 2020) |
| Factor europeo | precio de la vivienda en la zona euro, shocks monetarios de alta frecuencia del BCE (Jarociński-Karadi) |

## 5. Identificación principal: SVAR bayesiano con restricciones de signo y de cero (M2)

**Variables.** Nacionales, trimestrales, 2004T1-2026T2, por la disponibilidad conjunta de compraventas, crédito nuevo y alquiler. Todas en tasas trimestrales log ×100 salvo el tipo:
1. p: precio real de compra;
2. r: alquiler real;
3. q: compraventas;
4. c: crédito nuevo para vivienda real;
5. i: tipo hipotecario, en nivel;
6. e: ocupados EPA;
7. n: población.

**Especificación.**
- BVAR con prior normal-Wishart y hiperparámetros por verosimilitud marginal (GLP).
- Retardos: p = 2 (sensibilidad con 1 y 4).
- Variables ficticias fijas de COVID y EPA 2021T1 como exógenas.

**Shocks.** Las restricciones son de impacto y del trimestre siguiente (h = 0-1); «0» es una restricción de cero en el impacto:

| Shock | p | r | q | c | i | e | n |
|---|---|---|---|---|---|---|---|
| Actividad y renta | + | + | · | + | · | + | 0 |
| Demográfico | · | + | · | · | · | · | + |
| Demanda de vivienda | + | · | + | + | · | · | 0 |
| Oferta de vivienda | − | · | + | · | · | · | 0 |
| Crédito y tipos (incluye la transmisión monetaria) | + | · | · | + | − | · | 0 |

- **Ceros en población.** La población no responde en el impacto a ningún shock salvo al demográfico: es un stock que se mueve despacio. Defendible y declarado.
- **Por qué se distinguen el demográfico y el de actividad.** Por el cero en la población, que el shock demográfico no tiene.
- **Crédito frente a política monetaria.** No se distinguen en la principal. La política monetaria se identifica aparte con un instrumento externo (§6) y en la variante V1.

**Variantes de identificación** (como máximo tres):
- **V1.** Política monetaria frente a crédito: i se sustituye por el Euríbor a 1 año más el diferencial hipotecario. Monetario: Euríbor +, c −. Crédito: diferencial −, c +, Euríbor = 0 en el impacto.
- **V2.** Factor europeo exógeno: el crecimiento del precio de la vivienda de la zona euro sin España, como bloque exógeno.
- **V3.** Solo restricciones de impacto (h = 0), sin la restricción de q en demanda y oferta.

**Robustez, que no cuenta como variante:** retardos 1 y 4, prior fijo frente a GLP, submuestras sin COVID y deflactor alternativo.

**Muestra larga.** Para P1, la descomposición histórica no está disponible con 7 variables. Se usa una versión con 4 variables desde 1995T2 (p, i, y = PIB en volumen, n; la EPA del panel empieza en 2002) con los shocks de actividad, demográfico, crédito y tipos y un residual, como contraste (C3s). En P1 la atribución principal combina esa versión, el largo plazo (M4) y la contabilidad hogares-viviendas.

## 6. Instrumentos externos (M5, candidatos a C3)

- **IV1.** Shocks monetarios de alta frecuencia del BCE (Jarociński-Karadi, componente de política monetaria pura), agregados por trimestre (1999T1-2025T3). Instrumentan el Euríbor y el tipo hipotecario en LP-IV sobre el precio y el alquiler, a horizontes 0-12.
- **IV2.** Empuje migratorio: llegadas a España por país de origen predichas con la variación de la emigración del país de origen al resto de la UE (excluida España) por la cuota inicial (2002) de cada origen. Instrumentan las llegadas y, a través de ellas, el alquiler y el precio. Panel provincial cuando haya cuotas por provincia; si no, nacional. Los flujos por ciudadanía hacia otros países de la UE se descargan en F4 (Eurostat migr_pop1ctz y migr_imm1ctz). Si no están disponibles, IV2 se marca como fallido.
- **IV3.** Bartik sectorial: cuotas sectoriales de empleo de 2008 por provincia por el crecimiento nacional sectorial (excluida la propia provincia). Instrumenta el empleo provincial. Si no hay empleo sectorial provincial, se usa el panel de CCAA (NUTS2, Eurostat).
- **Requisitos de C3:**
  - F efectivo de primera etapa ≥ 10;
  - intervalo Anderson-Rubin que excluye el cero;
  - pretendencias (horizontes negativos) no significativas;
  - placebo con un instrumento permutado.
  
  Si no se cumplen, C4. Si el instrumento no está disponible o falla, se marca con su motivo.

## 7. Hipótesis confirmatorias (Holm, α = 0,05)

La prueba unilateral se basa en la probabilidad posterior P(contribución ≤ 0) o P(≥ 0) para el SVAR, y en el p del intervalo AR para LP-IV.

| id | Hipótesis | Método |
|---|---|---|
| H8-1 | En P5, la contribución del shock demográfico a la subida del alquiler real es positiva | SVAR, descomposición histórica |
| H8-2 | En P5, la contribución de crédito y tipos al precio real de compra es negativa | SVAR, descomposición histórica |
| H8-3 | En P3, la contribución de actividad y renta al precio real de compra es positiva | SVAR, descomposición histórica |
| H8-4 | En P2, la contribución conjunta de crédito y tipos y de actividad y renta al precio real de compra es negativa | SVAR, descomposición histórica |
| H8-5 | Un shock monetario contractivo del BCE reduce el precio real de compra a h = 4-8 | LP-IV con IV1 |
| H8-6 | Un shock monetario contractivo del BCE reduce el alquiler real a h = 4-8 | LP-IV con IV1 |
| H8-7 | El empuje migratorio aumenta el alquiler real | LP-IV con IV2 |
| H8-8 | El componente común de las 17 CCAA explica más del 50 % de la varianza del crecimiento interanual del precio de compra en cada periodo | DFM y PCA |
| H8-9 | El factor común español covaría positivamente con el crecimiento del precio de la vivienda de la zona euro | correlación con bootstrap por bloques |

**Familias:** {H8-1…H8-4} (SVAR), {H8-5…H8-7} (instrumentos) y {H8-8, H8-9} (factor común); Holm dentro de cada familia. Todo lo demás es exploratorio, con BH (q = 0,10).

## 8. Periodos (M0): regla de «efecto por periodo»

- **Análisis principal.** Periodos pre-registrados, con inferencia por tramo y sin búsqueda.
- **Confirmaciones:**
  - Bai-Perron con valores críticos que corrigen la búsqueda (bootstrap);
  - Markov switching con 2-3 regímenes y su número contrastado por bootstrap;
  - umbral con variables observables pre-registradas: tipo real hipotecario, crecimiento interanual del crédito nuevo y tasa de paro.
- **Detección separada de la estimación.** Los regímenes se detectan solo con las series nacionales de crédito, tipos y actividad. Los efectos se estiman con precio y alquiler. Segunda partición: detectar en 1995-2013 y comprobar en 2014-último.
- **Control del azar.** Permutación con 2.000 conjuntos de fechas aleatorias, con el mismo número de tramos y una longitud mínima de 8 trimestres.
- **Regla.** Un «efecto por periodo» exige:
  - que coincida el signo en el análisis principal y en al menos una confirmación;
  - p de permutación < 0,05;
  - el mismo signo con la medida alternativa (IPV o SERPAVI).
  
  Si no, es C4 y se reporta igual.

## 9. Criterios de decisión

**Factor más relevante**, por mercado, periodo y ámbito. Solo se designa si se cumplen las tres condiciones:
1. tiene la mayor contribución en al menos 3 de 4 métodos: descomposición histórica del SVAR, dominancia (M6), LP-IV (M5) y contabilidad hogares-viviendas;
2. su signo es estable en al menos el 80 % del multiverso;
3. su banda del 68 % en la descomposición histórica no incluye el cero.

Si no, se da un ranking con incertidumbre y se explica por qué no se designa. El ranking SHAP agrupado (M9) se muestra solo como contraste.

**Modelo destacado:**
- modelos que cumplen la regla de §8 y la del multiverso (signo estable en al menos el 80 % y significativo tras BH en al menos el 50 % de las especificaciones de esa variable);
- además, el mejor de cada familia por mercado y periodo según el error fuera de muestra en bloques con embargo, nunca por su p, marcado «no cumple la regla» si es el caso.

**Multiverso (M7).** Como máximo 50.000 especificaciones, todas registradas en el Registry. Ninguna se elige por su p.

## 10. Evaluación diferida (`make evaluate_v8`)

- **Qué se congela.** Antes de la release se congelan con su sha256 las predicciones del BVAR principal (forma reducida) y del mejor modelo de cada familia para el precio real de compra y el alquiler real, nacional, a h = 1-4 desde 2026T2.
- **Con qué se evalúa.** Una sola vez, con los datos 2026T3-2027T2 publicados después de la fecha verificable, frente al AR(4) y la base fuerte (AR con factor común). DM-HLN y Holm.
- **Registro.** La apertura se registra en docs/v8/evaluate_v8_accesos.md antes de evaluar. Se publica el resultado, sea cual sea.

## 11. Qué no se afirmará en ningún caso

- Causalidad desde asociaciones, SHAP, importancias o dominancia.
- Un «factor más relevante» que no cumpla la regla de §9.
- Efectos por periodo que no cumplan la regla de §8 (se reportan como C4).
