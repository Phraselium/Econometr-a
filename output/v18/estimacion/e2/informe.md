# V18 · E2 · Topes al alquiler (Ley 11/2020 de Cataluña, Incasòl)

**Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO. La clasificación V18 va en el campo `clasificacion_v18` y no cambia la capa.
Clasificaciones provisionales: falta I8 (réplica ciega, B6). Código: `src/v18/estimacion/e2_topes.py` (+ `e2_datos.py`, `e2_diseno.py`, `e2_estim.py`, `e2_salidas.py`, `_e2e8_comun.py`); SEED 20261010; sin red; 156 s.

## 1. Resumen
- **E2-R1 (principal)**: coeficiente de Reg × Post sobre el log de la renta media de contratos nuevos = **-0.0382** (IC95 de Webb -0.0507; -0.0257; p tras Holm 0.00057). Clase V18: **SUGESTIVO**. Razón con la referencia (−0,045 de Jofre-Monseny et al., 2023): 0.85, etiqueta «coherente» (razón en [1/3; 3]; no interviene en la clase).
- **E2-R1c (contratos por 1.000 habitantes)**: 0.0173 (IC95 -0.0249; 0.0595), sin significación (p Holm 1.000). Clase V18: **ASOCIACIÓN**; el TOST con δ = 0,05 no se cumple (IC90 -0.0182; 0.0529).
- **Reversión** tras la STC 37/2022 (2022T2-2023T4): coeficiente -0.0016 (p 0.840): el nivel vuelve al previo; no se aplica el tope de la adenda.
- **No estimables por variación o por datos**: E2-A1 (MDE 0.0408 > 0,0298), E2-A2 (6 municipios tratados con EMAL no sellados), E2-A3 (2 controles), E2-A4 (MDE 0.0444 > 0,027), E2-R2, E2-R2s, E2-R2-X1 y E2-A5 (datos). La ampliación A1 («provisional, sin difundir») no se estima: no hay cifra que difundir.
- Ninguna estimación IDENTIFICADO: no hay contradicción con una conclusión publicada (parada G no activada).

## 2. Qué se ha leído y qué queda fuera (sellado)
- Toda serie pasa por `sellado.filtrar` (tope temporal de docs/v18/sellado_v18.json y exclusión de unidades de v6, V15 y V16) y por `holdout.excluir_sellados_v6`. No se lee `data/sealed` ni se ejecuta ningún `evaluate_*`.
- Cataluña no tiene provincia sellada en v6. Los bloques de V15 y V16 dejan fuera 176 municipios catalanes (Barcelona 83, Lleida 86, Tarragona 7, Girona 0; adenda 1.5): de los 61 de la Ley 11/2020 quedan 51 con Incasòl trimestral.
- Barcelona ciudad (08019), que tiene distritos sellados, queda fuera de la principal (criterio de JMS) y entra en la variante v2: el total municipal de esa ciudad es una fuga declarada (adenda 1.5).
- Incasòl público: trimestral solo desde 2019T1 (anual desde 2007); la ventana de JMS (2016T1-2022T1) no existe en nuestros datos y la principal es 2019T1-2022T1 (adenda R-1).

## 3. Estimabilidad (adenda 1.3), calculada antes de mirar los coeficientes
MDE80: R = 2.000 reasignaciones placebo del tratamiento con el número y el calendario reales (σ y dependencia «ya vistas», tomadas del propio panel de entrenamiento; V15 y V16 publican la sd placebo del ATT y no la σ residual de este resultado). El MDE es optimista: no incluye los choques de comarca.

| id | n_tratados | n_controles | minimo_datos | mde80 | umbral | estimable |
|---|---|---|---|---|---|---|
| E2-R1 | 49 | 94 | 49 tratados y 94 controles (mínimo 30 y 30) | 0.0214 | 0.0450 | True |
| E2-R1c | 49 | 156 | 49 tratados y 156 controles (mínimo 30 y 30) | 0.0809 | 0.1000 | True |
| E2-A1 | 169 | 20 | 169 tratados y 20 nunca tratados (CS exige controles propios) | 0.0408 | 0.0298 | False |
| E2-A2 | 6 | 4 | 6 municipios tratados con EMAL no sellados (mínimo 10) y trimestres posteriores por cohorte … (mínimo 3) | — | 0.0298 | False |
| E2-A3 | 44 | 2 | 44 tratados y 2 controles en la serie municipal de MIVAU | — | 0.1000 | False |
| E2-A4 | 84 | 12 | 84 cerca (< 10 km) y 12 lejos (> 25 km) | 0.0444 | 0.0270 | False |

## 4. Resultados de las especificaciones estimadas
| id | n_tratados | n_controles | coef | ic95_lo | ic95_hi | p_webb | p_i7 | p_holm | clase |
|---|---|---|---|---|---|---|---|---|---|
| E2-R1 | 49 | 94 | -0.0382 | -0.0507 | -0.0257 | 0.0001 | 0.0001 | 0.0006 | SUGESTIVO |
| E2-R1c | 49 | 156 | 0.0173 | -0.0249 | 0.0595 | 0.4029 | 0.5721 | 1.0000 | ASOCIACIÓN |
| E2-P-D1b | 50 | 146 | -0.0582 | -0.0761 | -0.0402 | 0.0001 | 0.0001 | 0.0006 | no se clasifica |
| E2-P-D1b-c | 50 | 298 | -0.0067 | -0.0709 | 0.0545 | 0.8346 | 1.0000 | 1.0000 | no se clasifica |

p_i7 = p de Webb con el valor crítico corregido por el tamaño de Monte Carlo (cs_webb, cat_trim_M: 0,071, banda «con valor crítico corregido»). Holm sobre la familia E2 (m = 4 tras las comprobaciones previas: E2-R1, E2-R1c, E2-P-D1b, E2-P-D1b-c). Las coprincipales P no se clasifican; la cifra publicada de V9-D1b (−0,0585 en renta y −0,0132 en contratos, con 60 y 181 unidades) va al lado y se reproduce en la muestra V18 con CS.

Inferencias alternativas de E2-R1: Webb por conglomerado espacial de 42 grupos (sustituto de las comarcas, que no están en el repositorio) p = 0.0005; aleatorización entre municipios p = 0.0001 y dentro del conglomerado p = 0.0001; EE de Conley a 10 km = 0.00666 (CR1 0.00649); Driscoll-Kraay p = 0.00016 (rótulo «no fiable»: NO APTO en su Monte Carlo).

## 5. Pruebas B4 de E2-R1
**Estudio de eventos** (coeficientes Reg × 1[t = k], base 2019T4; k = 0..12 es 2019T1..2022T1; k = 6 es 2020T3, la anticipación):

| periodo | coef | se |
|---|---|---|
| 2019T1 | 0.0010 | 0.0133 |
| 2019T2 | 0.0056 | 0.0130 |
| 2019T3 | 0.0068 | 0.0126 |
| 2020T1 | 0.0195 | 0.0130 |
| 2020T2 | -0.0111 | 0.0152 |
| 2020T3 | 0.0166 | 0.0132 |
| 2020T4 | -0.0204 | 0.0134 |
| 2021T1 | -0.0578 | 0.0128 |
| 2021T2 | -0.0492 | 0.0155 |
| 2021T3 | -0.0389 | 0.0143 |
| 2021T4 | -0.0264 | 0.0149 |
| 2022T1 | -0.0147 | 0.0139 |

- Pretendencias (cinco adelantos, contraste conjunto con covarianza agrupada): p = 0.440.
- Potencia de Roth: pendiente lineal previa detectable al 80 % = 0.0093 por trimestre; el sesgo que implicaría en la ventana posterior (0.0606) supera la mitad de |referencia| (0,0225): prueba débil (tope SUGESTIVO).
- Placebo de fecha (anual 2014-2019, adopción falsa en 2017): coeficiente 0.0146, p = 0.056, de signo contrario al principal.
- Placebo de resultado (población de 65 años o más por municipio y año; contratos de locales): sin dato en el repositorio. El sustituto de la renta IRPF solo cubre la C. Valenciana: no realizable. Prueba débil.
- Honest DiD (muestra comprimida sin 2020T1-2020T3; previos 2019T1-T3; referencia 2019T4). Según el Monte Carlo de V18 solo M̄ = 0 es apto; con M̄ = 0,5 y 1 es válido pero conservador (tamaño ≈ 0): se publica y no decide (adenda 1.12; desviación D2):

| M̄ | IC95 | excluye 0 | lectura |
|---|---|---|---|
| 0.0 | (-0.0549; -0.0141) | True | apto (Monte Carlo) |
| 0.5 | (-0.0870; 0.0251) | False | válido pero conservador: informativo, no criterio |
| 1.0 | (-0.1340; 0.0717) | False | válido pero conservador: informativo, no criterio |

- I de Moran de los residuos medios por municipio (5 vecinos más próximos): I = 0.037 (E[I] = -0.007), p unilateral = 0.176: no hay autocorrelación espacial positiva significativa de los residuos medios. Se publican igualmente Webb por conglomerado espacial, aleatorización dentro del conglomerado y Conley, porque el Monte Carlo de V18 mide un sobrerrechazo de la agrupación por municipio con choques de comarca (tamaño 0,071).
- Honest DiD en la variante anual (E2-R1-v8; previos 2014-2018, referencia 2019, posterior 2021): M̄ = 0: (-0.0461; -0.0124); M̄ = 0.5: (-0.0593; 0.0014); M̄ = 1: (-0.0776; 0.0200).
- Reversión tras la STC 37/2022: coeficiente en 2022T2-2023T4 = -0.0016 (p 0.840); coeficiente de la vigencia en ese panel -0.0366.
- Robustez: el signo coincide con el de la principal en 10 de 10 variantes estimadas; el IC95 (CR1) no solapa con el de la principal en: E2-R1-v9.

## 6. Variantes enumeradas (anexo A) y holgura
Ajuste de Benjamini-Yekutieli al 10 % dentro de cada identificador (q_by). Webb con 1.999 réplicas.

| id | nota | estado | n_tratados | n_controles | coef | ic95_lo | ic95_hi | p_webb | q_by |
|---|---|---|---|---|---|---|---|---|---|
| E2-R1-v1 | [V] sin 2020T1-2020T3 | estimada | 49 | 94 | -0.0379 | -0.0517 | -0.0240 | 0.0005 | 0.0021 |
| E2-R1-v2 | [U] con Barcelona ciudad | estimada | 50 | 94 | -0.0390 | -0.0519 | -0.0261 | 0.0005 | 0.0021 |
| E2-R1-v3 | [C] controles por covariables (vecino más cercano) | estimada | 49 | 10 | -0.0260 | -0.0388 | -0.0133 | 0.0005 | 0.0021 |
| E2-R1-v4 | [C] controles a más de 10 km | estimada | 49 | 62 | -0.0560 | -0.0706 | -0.0413 | 0.0005 | 0.0021 |
| E2-R1-v5 | [C] sin covariables: la principal ya va sin covariables (el paro registrado de 2020 no est | coincide con la principal | — | — | -0.0382 | -0.0507 | -0.0257 | 0.0001 | — |
| E2-R1-v6 | [C] densidad HUT 2019 × posterior | estimada | 49 | 94 | -0.0376 | -0.0503 | -0.0248 | 0.0005 | 0.0021 |
| E2-R1-v7 | [E] anticipación desde 2019T2 | estimada | 49 | 94 | -0.0355 | -0.0575 | -0.0135 | 0.0015 | 0.0049 |
| E2-R1-v8 | [V] anual 2014-2021 con Honest DiD | estimada | 50 | 167 | -0.0268 | -0.0438 | -0.0097 | 0.0015 | 0.0049 |
| E2-R1-v9 | [M] SERPAVI municipal anual 2016-2021 | estimada | 50 | 152 | -0.0052 | -0.0174 | 0.0069 | 0.3605 | 1.0000 |
| E2-R1-v10 | [P] ponderada por contratos de 2019 | estimada | 49 | 94 | -0.0350 | -0.0468 | -0.0232 | 0.0005 | 0.0021 |
| E2-R1-v11 | [U] sin el 1 % de municipios con más contratos | estimada | 47 | 94 | -0.0376 | -0.0505 | -0.0246 | 0.0005 | 0.0021 |
| E2-R1-h1 | paro registrado con 2020 interpolado linealmente (el de 2020 no está en la base): solo rob | estimada | 49 | 94 | -0.0378 | -0.0508 | -0.0248 | 0.0005 | — |
| E2-R1c-v1 | [M] contratos por hogar inquilino: la variable (hogares en alquiler del Censo 2021 por mun | estimada a posteriori (B6) | — | — | — | — | — | — | — |
| E2-R1c-v2 | [E] PPML | estimada | 49 | 156 | 0.0225 | -0.0234 | 0.0683 | — | — |
| E2-R1c-v3 | [V] sin 2020T1-2020T3 | estimada | 49 | 156 | -0.0085 | -0.0563 | 0.0393 | 0.7140 | 1.0000 |
| E2-R1c-v4 | [U] con Barcelona | estimada | 50 | 156 | 0.0202 | -0.0223 | 0.0627 | 0.3405 | 1.0000 |

## 7. Clasificación (I1-I8 revisados)
- **E2-R1: SUGESTIVO.** Razones: potencia de Roth: el sesgo implicado por la pendiente detectable supera la mitad de |referencia|; placebo de fecha p = 0.056; placebo de resultado sin dato en el repositorio; IC95 de alguna robustez no solapa con el principal; tope SUGESTIVO por corrección de un fallo conocido de V9-D1b: grupo de control y ventana (adenda 1.6; Honest M̄ de ruptura 0,5).
- **E2-R1c: ASOCIACIÓN.** Razones: potencia de Roth: el sesgo implicado por la pendiente detectable supera la mitad de |referencia|; placebo de fecha p = 0.001; placebo de resultado sin dato en el repositorio; mismo signo en 67% de las variantes enumeradas (< 80 %); la diferencia persiste tras la STC 37/2022 (coeficiente +0.0736, p = 0.002): tope de la adenda, AD-E2-R1 (línea 581); el placebo de fecha (adopción falsa en 2017) es significativo (coeficiente -0.0793, p = 0.0005): el diseño no es creíble para este resultado (K7). Lectura: coeficiente no significativo; no hay clase SUGESTIVO sin significación (K7): al no superar I1-I5 (placebo de fecha, persistencia tras la STC) la clase es ASOCIACIÓN, no NO CONCLUYENTE.
- I6 se publica como etiqueta (razón con la referencia); no interviene en la clase ni en B5.
- I8 pendiente para ambas (replicador-ciego). El lenguaje de ambas cifras es el de una asociación estimada.

## 8. Desviaciones y lecturas de las reglas (se recogen en docs/v18/desviaciones.md)
- **D1. Paro registrado de 2020 ausente.** La base no tiene el paro municipal del SEPE de 2013 ni de 2020. La principal va sin covariables; E2-R1-v5 («sin covariables») coincide con ella; el paro con 2020 interpolado entra como holgura E2-R1-h1 (adenda 1.8). Los ERTE por municipio no están en el repositorio.
- **D2. Honest DiD.** Se aplica la lectura de la adenda 1.12 y del Monte Carlo de V18: solo M̄ = 0 es apto; el criterio de I3 «IC con M̄ = 1 excluye el cero» no es evaluable (tamaño 0 con M̄ ≥ 0,5). I3 se juzga con las pretendencias y la potencia de Roth.
- **D3. Comarcas.** No están en el repositorio: 42 conglomerados de k-medias sobre los centroides de los 947 municipios (SEED 20261010) sustituyen a las comarcas en la inferencia alternativa.
- **D4. Entradas y salidas del régimen.** La lista de la Ley 11/2020 del repositorio no identifica municipios que entraron o salieron; no se pudo reconstruir con el DOGC (sin red). Se dice.
- **D5. Hogares en alquiler del Censo 2021** (E2-R1c-v1): la variable no tenía entrada en docs/v18/sellado_v18.json cuando se estimó la principal; se añadió DESPUÉS de la etiqueta (desviación B6-1) y la variante se estima a posteriori en `e2_robustez.py` (sección «Robustez B6» de este informe).
- **D6. Población** para contratos por 1.000 habitantes: padrón municipal (tope 2022 de la regla de sellado); en la reversión de 2023 se mantiene la de 2022.
- **D7. Códigos INE de MIVAU.** Los ficheros municipales de MIVAU solo traen nombres; el código se asigna por nombre dentro de su comunidad con el diccionario oficial del INE (3 de 205 sin resolver). Solo afecta a E2-A3 (no estimable).
- **D8. Lectura de la regla de clasificación (revisada en B6, K7).** Antes se aplicaba SUGESTIVO a un coeficiente sin significación con alguna prueba débil; tras la ronda 1 el autor decidió (K7) que no existe «SUGESTIVO sin significación»: un no significativo es NO CONCLUYENTE si supera I1-I5 y ASOCIACIÓN si no (opción `nulo_sin_sugestivo` de `clasificar`). Cambia E2-R1c: SUGESTIVO → ASOCIACIÓN.
- **D9. Coprincipales sin estimar.** E2-P-H1, E2-P-H2, E2-P-D1c y E2-P-Q1c heredan la no estimabilidad de la principal que acompañan (misma variación).

## 9. Limitaciones
- Incasòl público solo da la renta media por municipio y trimestre, sin renta anterior, superficie ni tipo de contrato: no se separa composición de precio y no se contrasta el desvío a la temporada.
- La COVID coincide con el posterior; el control de JMS se define por el crecimiento de la renta de 2014-2019 (criterio legal de mercado tensionado), lo que condiciona la comparación (la coprincipal V9-D1b, sin ese criterio, da un coeficiente mayor).
- Las 4 provincias catalanas no bastan como clusters; la unidad de agrupación es el municipio.

## 10. Datos que los desbloquearían
Microdatos de contratos del registro de fianzas con renta, renta anterior, superficie y tipo de contrato (tareas_autor, punto 4); compraventas municipales de todos los municipios; EMAL y zonas tensionadas con más trimestres posteriores; evaluación diferida de H1 y H2 de V15 para A1.

## Robustez B6 (a posteriori)

Pruebas pedidas por la ronda 1 del abogado del diablo (hallazgos 1, 2, 4, 5 y 6; docs/v18/revision_estimaciones/ronda1_e2_e8.md). **Se declaran a posteriori**: se añadieron después de ver los
resultados de E2, no cambian la especificación principal ni su clase por sí solas y entran como robustez (desviación B6-2 de docs/v18/desviaciones_e2_e8.md). Código: `src/v18/estimacion/e2_robustez.py`;
SEED 20261010; 42 s; inferencia de Webb con 4.999 réplicas por municipio en las variantes (9.999 en E2-R1c-v1) y 999 placebos de Conley-Taber en el SDID. q_bh: Benjamini-Hochberg al 10 % sobre las variantes de la renta de esta sección (B6b, B6c-1 a B6c-3, B6d; exploratorias);
los diagnósticos, los placebos y E2-R1c-v1 (una sola variante) llevan su p propio, sin ajuste. Análisis V18; capa C4; nivel de evidencia EXPLORATORIO.

### Lectura
- (a) Tendencia: el coeficiente por trimestre sube +0.0109 por trimestre en 2021T1-2022T1 (IC95 0.0050; 0.0167; p = 0.000): ya durante la vigencia pierde magnitud trimestre a trimestre (ajustado: -0.0588 en 2021T1); con la ventana 2020T4-2022T1 la pendiente es +0.0043 (p = 0.073). El coeficiente medio de la principal (-0.0382) no describe un nivel estable. Salto en 2022T2 sobre la extrapolación de la recta: -0.0217 (IC95 -0.0468; 0.0034; p = 0.090): observado -0.0262 frente a -0.0045 extrapolado; media 2022T2-2022T4: -0.0141 (p = 0.271). El observado es MÁS negativo que la extrapolación (no hay una desaparición abrupta del coeficiente en 2022T2): no se detecta un salto en la fecha de la STC a este nivel de potencia, y el coeficiente se aproxima a cero de forma gradual.
- (b) Covariables por trimestre: B6b-1 -0.0376 (IC95 -0.0504; -0.0249; p Webb 0.0002); B6b-2 -0.0228 (IC95 -0.0451; -0.0005; p Webb 0.0412); B6b-3 -0.0237 (IC95 -0.0461; -0.0014; p Webb 0.0356); B6b-4 -0.0236 (IC95 -0.0462; -0.0010; p Webb 0.0366); principal -0.0382. HUT × trimestre deja el coeficiente en -0.0376 (por debajo de −0,03); ln(población) × trimestre lo reduce a -0.0228 (no queda por debajo de −0,03, criterio de la ronda), con IC95 que casi llega a cero.
- (c) Controles emparejados: B6c-1 -0.0543 (p Webb 0.0004; pretendencias p = 0.64); B6c-2 -0.0381 (p Webb 0.0028; pretendencias p = 0.35); B6c-3 -0.0422 (p Webb 0.0002; pretendencias p = 0.56). Placebo de 2017: sin tendencia +0.0146 (p = 0.056); con tendencia propia de los regulados +0.0299 (p = 0.012, de signo contrario al de la principal); con tendencia y controles emparejados +0.0021 (p = 0.848). El placebo de signo contrario indica que los regulados subían más que los controles en 2017-2019 (lo que, si se revierte, sesgaría hacia un coeficiente más negativo); el emparejamiento por ese crecimiento no reduce el coeficiente.
- (d) SDID: B6d-1 τ = -0.0416 (Conley-Taber p = 0.001, mínimo posible 0,001; razón de variabilidad previa 0.45, conservadora (tratados menos variables que los controles); donantes efectivos 93 de 94; DiD simple -0.0382); B6d-2 τ = -0.0440 (Conley-Taber p = 0.001, mínimo posible 0,001; razón de variabilidad previa 0.46, conservadora (tratados menos variables que los controles); donantes efectivos 144 de 146; DiD simple -0.0443). Los pesos de unidad quedan casi uniformes (la regularización de ζ es fuerte con 49 tratados): SDID reproduce al DiD y no cambia la lectura; la dependencia del control (hallazgo 5) se aborda mejor con B6c.
- (e) E2-R1c-v1: -0.0314 (IC95 -0.0846; 0.0218; p Webb 0.2255); en la misma muestra con la población como denominador -0.0270 (p Webb 0.3078); la R1c principal, con 156 controles, da +0,0173. Criterio de AD-E2 (caída ≥ 5 % con p < 0,05): no se cumple, pero el IC95 incluye caídas mayores que 5 % (hasta -0.085): no se descarta el desvío a la temporada o a no depositar la fianza. mínimo 30/30: True; MDE80 0.0670 (umbral 0.10, 2δ).

### Tabla
| id | rol | n_tratados | n_controles | coef | se | p_cr1 | p_webb | ic95_lo | ic95_hi | q_bh |
|---|---|---|---|---|---|---|---|---|---|---|
| E2-R1-B6a-14T-2021T1-2022T1-pendiente | diagnóstico | 49 | 94 | 0.0109 | 0.0030 | 0.0004 | — | 0.0050 | 0.0167 | — |
| E2-R1-B6a-14T-2021T1-2022T1-salto-2022T2 | diagnóstico | 49 | 94 | -0.0217 | 0.0127 | 0.0900 | — | -0.0468 | 0.0034 | — |
| E2-R1-B6a-14T-2020T4-2022T1-pendiente | diagnóstico | 49 | 94 | 0.0043 | 0.0024 | 0.0732 | — | -0.0004 | 0.0091 | — |
| E2-R1-B6a-14T-2020T4-2022T1-salto-2022T2 | diagnóstico | 49 | 94 | -0.0107 | 0.0124 | 0.3935 | — | -0.0353 | 0.0139 | — |
| E2-R1-B6a-20T-2021T1-2022T1-pendiente | diagnóstico | 49 | 91 | 0.0104 | 0.0030 | 0.0006 | — | 0.0045 | 0.0163 | — |
| E2-R1-B6a-20T-2021T1-2022T1-salto-2022T2 | diagnóstico | 49 | 91 | -0.0231 | 0.0126 | 0.0698 | — | -0.0481 | 0.0019 | — |
| E2-R1-B6a-20T-2021T1-2022T1-salto-2022T2-2022T4 | diagnóstico | 49 | 91 | -0.0141 | 0.0128 | 0.2710 | — | -0.0394 | 0.0112 | — |
| E2-R1-B6a-20T-2020T4-2022T1-pendiente | diagnóstico | 49 | 91 | 0.0039 | 0.0024 | 0.1078 | — | -0.0009 | 0.0086 | — |
| E2-R1-B6a-20T-2020T4-2022T1-salto-2022T2 | diagnóstico | 49 | 91 | -0.0122 | 0.0124 | 0.3264 | — | -0.0367 | 0.0123 | — |
| E2-R1-B6a-20T-2020T4-2022T1-salto-2022T2-2022T4 | diagnóstico | 49 | 91 | 0.0033 | 0.0119 | 0.7822 | — | -0.0203 | 0.0269 | — |
| E2-R1-B6b-1 | variante | 49 | 94 | -0.0376 | 0.0065 | 0.0000 | 0.0002 | -0.0504 | -0.0249 | 0.0009 |
| E2-R1-B6b-2 | variante | 49 | 94 | -0.0228 | 0.0113 | 0.0450 | 0.0412 | -0.0451 | -0.0005 | 0.0412 |
| E2-R1-B6b-3 | variante | 49 | 94 | -0.0237 | 0.0113 | 0.0378 | 0.0356 | -0.0461 | -0.0014 | 0.0412 |
| E2-R1-B6b-4 | variante | 49 | 94 | -0.0236 | 0.0114 | 0.0410 | 0.0366 | -0.0462 | -0.0010 | 0.0412 |
| E2-R1-B6c-1 | variante | 49 | 31 | -0.0543 | 0.0134 | 0.0001 | 0.0004 | -0.0809 | -0.0277 | 0.0012 |
| E2-R1-B6c-2 | variante | 49 | 34 | -0.0381 | 0.0111 | 0.0009 | 0.0028 | -0.0601 | -0.0161 | 0.0042 |
| E2-R1-B6c-3 | variante | 49 | 76 | -0.0422 | 0.0069 | 0.0000 | 0.0002 | -0.0559 | -0.0285 | 0.0009 |
| E2-R1-B6c-4 | placebo | 50 | 170 | 0.0146 | 0.0076 | 0.0560 | — | -0.0004 | 0.0296 | — |
| E2-R1-B6c-5 | placebo | 50 | 170 | 0.0299 | 0.0118 | 0.0121 | — | 0.0066 | 0.0532 | — |
| E2-R1-B6c-6 | placebo | 50 | 31 | 0.0021 | 0.0108 | 0.8479 | — | -0.0193 | 0.0235 | — |
| E2-R1-B6d-1 | variante | 49 | 94 | -0.0416 | 0.0099 | — | 0.0010 | -0.0608 | -0.0224 | 0.0018 |
| E2-R1-B6d-2 | variante | 49 | 146 | -0.0440 | 0.0092 | — | 0.0010 | -0.0624 | -0.0256 | 0.0018 |
| E2-R1c-v1 | variante | 49 | 38 | -0.0314 | 0.0268 | 0.2442 | 0.2255 | -0.0846 | 0.0218 | — |
| E2-R1c-v1-ref | referencia | 49 | 38 | -0.0270 | 0.0268 | 0.3176 | 0.3078 | -0.0804 | 0.0264 | — |

### Notas por fila
| id | nota |
|---|---|
| E2-R1-B6a-14T-2021T1-2022T1-pendiente | coeficiente ajustado al inicio de la ventana -0.0588 |
| E2-R1-B6a-14T-2021T1-2022T1-salto-2022T2 | observado -0.0262; extrapolado -0.0045 |
| E2-R1-B6a-14T-2020T4-2022T1-pendiente | coeficiente ajustado al inicio de la ventana -0.0416 |
| E2-R1-B6a-14T-2020T4-2022T1-salto-2022T2 | observado -0.0262; extrapolado -0.0155 |
| E2-R1-B6a-20T-2021T1-2022T1-pendiente | coeficiente ajustado al inicio de la ventana -0.0565 |
| E2-R1-B6a-20T-2021T1-2022T1-salto-2022T2 | observado -0.0275; extrapolado -0.0044 |
| E2-R1-B6a-20T-2021T1-2022T1-salto-2022T2-2022T4 | observado -0.0081; extrapolado +0.0060 |
| E2-R1-B6a-20T-2020T4-2022T1-pendiente | coeficiente ajustado al inicio de la ventana -0.0387 |
| E2-R1-B6a-20T-2020T4-2022T1-salto-2022T2 | observado -0.0275; extrapolado -0.0153 |
| E2-R1-B6a-20T-2020T4-2022T1-salto-2022T2-2022T4 | observado -0.0081; extrapolado -0.0114 |
| E2-R1-B6b-1 | principal -0.0382; criterio de la ronda: por debajo de −0,03: sí |
| E2-R1-B6b-2 | principal -0.0382; criterio de la ronda: por debajo de −0,03: no |
| E2-R1-B6b-3 | principal -0.0382; criterio de la ronda: por debajo de −0,03: no |
| E2-R1-B6b-4 | principal -0.0382; criterio de la ronda: por debajo de −0,03: no |
| E2-R1-B6c-1 | pretendencias (contraste conjunto) p = 0.636; principal -0.0382 |
| E2-R1-B6c-2 | pretendencias (contraste conjunto) p = 0.347; principal -0.0382 |
| E2-R1-B6c-3 | pretendencias (contraste conjunto) p = 0.557; principal -0.0382 |
| E2-R1-B6c-4 | adopción falsa en 2017; el coeficiente principal del placebo sin tendencia fue +0,0146 (p = 0,056), de signo contrario al de la principal |
| E2-R1-B6c-5 | adopción falsa en 2017; el coeficiente principal del placebo sin tendencia fue +0,0146 (p = 0,056), de signo contrario al de la principal |
| E2-R1-B6c-6 | adopción falsa en 2017; el coeficiente principal del placebo sin tendencia fue +0,0146 (p = 0,056), de signo contrario al de la principal |
| E2-R1-B6d-1 | τ(SDID) -0.0416; DiD simple en los mismos periodos -0.0382; razón de variabilidad previa tratados/controles 0.45 (conservadora (tratados menos variables que los controles)); donantes efectivos 93.3; 45 donantes en cada placebo (Mo |
| E2-R1-B6d-2 | τ(SDID) -0.0440; DiD simple en los mismos periodos -0.0443; razón de variabilidad previa tratados/controles 0.46 (conservadora (tratados menos variables que los controles)); donantes efectivos 144.1; 97 donantes en cada placebo (M |
| E2-R1c-v1 | pretendencias p = 0.426; MDE80 0.0670; criterio AD-E2 (cae ≥ 5 % con p < 0,05): no |
| E2-R1c-v1-ref | pretendencias p = 0.409; MDE80 0.0670; criterio AD-E2 (cae ≥ 5 % con p < 0,05): no |

### Cómo se hizo
- **(a)** Estudio de eventos (base 2019T4) en los paneles equilibrados 2019T1-2022T2 (14 trimestres) y 2019T1-2023T4 (20): la recta se ajusta por mínima distancia (GLS con la covarianza agrupada por municipio) a los coeficientes de 2021T1-2022T1 (y, como variante, de 2020T4-2022T1); el salto es el coeficiente de 2022T2 menos el valor de la recta extrapolada, con su error típico conjunto (t de G−1 gl). La muestra de estos paneles es menor que la de la principal porque exige contratos en más trimestres.
- **(b)** Covariables por trimestre: x_i × 1[t = k] para cada trimestre; la densidad HUT usa IDESCAT 2019 (sin dato = 0) entre los habitantes del padrón de 2019; la población municipal del padrón está en el repositorio. B6b-4 añade el paro registrado de 2019 (el de 2020 no está en la base; los ERTE por municipio tampoco).
- **(c)** Emparejamiento con reposición por el crecimiento anual de la renta 2017-2019 (y 2014-2017 en B6c-2) con el conjunto de no regulados sin el criterio de crecimiento de JMS; el peso del control es el número de veces elegido. El placebo de 2017 usa Incasòl anual 2014-2019, adopción falsa en 2017, con y sin una tendencia lineal propia de los regulados.
- **(d)** SDID con los pesos de unidad ω (símplex, con regularización) y de tiempo λ de `sdid.py`; pre = 2019T1-2020T2, post = 2020T4-2022T1 (como la principal; 2020T3 queda fuera). La inferencia por placebos de Conley-Taber solo es válida si los tratados son intercambiables con los controles (Monte Carlo de V18): se rotula la razón de variabilidad temporal previa entre tratados y controles. Con JMS hay pocos donantes por placebo.
- **(e)** E2-R1c-v1: estimabilidad (mínimo de 30/30 y MDE80 frente al umbral 2δ = 0,10) calculada antes del coeficiente. Como el denominador (hogares inquilinos) es fijo en el tiempo, lo absorbe el efecto fijo de municipio: la variante equivale al log de contratos en la muestra de municipios con Censo 2021 (de 10.000 habitantes o más), y su contribución es el cambio de muestra y de unidades.

### Qué dicen estas pruebas sobre la clase de E2-R1
- Prueba 1 de la ronda (tendencia y salto): pendiente significativa; salto en 2022T2 sobre la extrapolación no distinguible.
- Prueba 2 (COVID y turismo por trimestre): HUT × trimestre -0.0376 (por debajo de −0,03); ln(población) × trimestre -0.0228 (no por debajo de −0,03).
- Placebo de 2017 con tendencia propia: +0.0299 (p = 0.012), de signo contrario al de la principal: no activa el fallo decisivo del plan (que exige el mismo signo); con controles emparejados el coeficiente de la principal sigue entre -0.0543 y -0.0381.
- Reglas escritas del plan (líneas 118-130): ninguna de estas pruebas es un fallo decisivo ni un tope pre-registrado; ninguna variante cambia de signo; las pretendencias de las muestras emparejadas son compatibles con cero. Por las reglas escritas, la clase provisional de E2-R1 sigue siendo SUGESTIVO. Las pruebas 1 y 2 limitan la lectura: el coeficiente no es un nivel estable (pierde magnitud durante la vigencia) y con ln(población) × trimestre baja a -0.0228. La propuesta del abogado («ASOCIACIÓN si fallan las pruebas 1-2») usa un criterio (por debajo de −0,03) que no estaba en el pre-registro: aplicado literalmente, la prueba 2 falla con ln(población) × trimestre y no con HUT × trimestre; la decisión corresponde al orquestador y al árbitro, que deben decidir antes de la ronda 2.
