# Informe econométrico V8: factores, periodos y factor común de los precios de la vivienda en España

Borja Romero, economista (firma individual, independiente). Generado por `make v8` desde `docs/v8/plantillas/informe_econometrico.md`; cada cifra procede de `output/v5/cifras_clave.csv` (ids `V8-…`). Lectura no técnica: `output/v8/por_que_ha_subido.md`. Tablas en formato de revista: `output/v8/tablas_modelos_destacados.md` y `output/v8/tablas_v8.xlsx`.

## Abstract (English)

We decompose real house-price and rent growth in Spain (1995-2026) into seven pre-registered factor families across five pre-registered periods, using four attribution methods: a Bayesian SVAR identified with sign and zero restrictions (historical decomposition), LMG dominance analysis, local projections with external instruments (ECB high-frequency shocks, an EU-migration shift-share push and a sectoral Bartik), and household-dwelling accounting. A designation rule fixed before estimation requires agreement of three of four methods, sign stability in at least 80 % of a structured multiverse and a 68 % structural band excluding zero. No factor is designated in any of the ten market-period cells. The pre-registered SVAR identification is rejected by the data (no accepted rotations) and the impact-only variant is used; all three instruments are weak (effective F well below ten). The activity-and-income shock in 1995-2007 is the only structural contribution whose band excludes zero. Regional co-movement is highest in 2022-2026, and the Spanish common factor is associated with euro-area house prices (Holm-adjusted p below the five per cent level). No model beats an AR(4) out of sample. An independent review found and corrected a mis-specified 2021 labour-survey dummy; both versions are published.

## 1. Diseño

- **Pre-registro.** `docs/v8/hipotesis.md` (etiqueta local `prereg-v8`), escrito antes de cualquier estimación con datos reales. Desviaciones con fecha y motivo en `docs/v8/desviaciones.md`; decisiones en `docs/v8/decisiones.md` (Y0-Y12).
- **Herramientas.** Validadas por Monte Carlo antes de usarse (F3; `output/v8/F3/*/validacion.md`): BVAR normal-Wishart con hiperparámetros por verosimilitud marginal, restricciones de signo y de cero, Bai-Perron y umbral con bootstrap sieve-AR, Markov switching, DFM/PCA, LP y LP-IV con intervalos de Anderson-Rubin, dominancia LMG, permutación de fechas, SHAP agrupado y multiverso con registro.
- **Control del azar.** Holm dentro de las tres familias confirmatorias ({H8-1…H8-4}, {H8-5…H8-7}, {H8-8, H8-9}); BH (q = 0,10) en todo lo exploratorio. Toda especificación probada está en el Registry (`output/v8/*/registro.csv`).
- **Capas.** C3s para la descomposición histórica del SVAR (condicionada a las restricciones); C4 para todo lo demás. Ningún resultado alcanza C3.
- **Revisión independiente.** Tras las herramientas (`docs/v8/revision_F3.md`) y tras los modelos (`docs/v8/revision_F4.md`: aprobar con correcciones; SVAR rehecho una vez).

## 2. Hipótesis confirmatorias

| id | Hipótesis | Estimación (intervalo al 95 %) | p ajustado (Holm) | Capa |
|---|---|---|---|---|
| H8-1 | Demografía empuja el alquiler real en P5 (SVAR) | 0,07 pp (-4,5 a 4,7 pp) | 0,987 | C3s |
| H8-2 | Crédito y tipos restan al precio real en P5 (SVAR) | -0,47 pp (-15,4 a 27,4 pp) | 0,987 | C3s |
| H8-3 | Actividad y renta suman al precio real en P3 (SVAR) | 7,7 pp (-22,8 a 40,0 pp) | 0,838 | C3s |
| H8-4 | Crédito más actividad restan al precio real en P2 (SVAR) | -19,2 pp (-57,3 a 9,9 pp) | 0,343 | C3s |
| H8-5 | Shock contractivo del BCE reduce el precio real (LP-IV) | F efectivo 1,83; t de la forma reducida 0,60 | 1,000 | C4 |
| H8-6 | Shock contractivo del BCE reduce el alquiler real (LP-IV) | F efectivo 0,77; t 0,34 | 1,000 | C4 |
| H8-7 | Empuje migratorio aumenta el alquiler real (LP-IV) | F efectivo 0,05; t -0,09 | 1,000 | C4 |
| H8-8 | Componente común > 50 % de la varianza en cada periodo | cuota mínima 45,3 % | 0,669 | C4 |
| H8-9 | Factor común español y zona euro covarían positivamente | 0,60 (0,14-0,86) | 0,020 | C4 |

Solo H8-9 se sostiene tras Holm, y es una asociación. En H8-5 a H8-7 los p unilaterales de Anderson-Rubin usan el signo **a priori** de la primera etapa; la primera etapa estimada de los shocks del BCE tiene el signo contrario (corrección J3 de la revisión). Las estimaciones de H8-1 a H8-4 con la especificación errónea de la ficticia EPA (escalón) quedan publicadas como retiradas en `output/v8/M2/hipotesis_m2_retirada.csv`; ninguna decisión de Holm cambia con la corrección.

## 3. SVAR bayesiano con restricciones de signo y de cero (M2)

**Especificación.** Siete variables nacionales trimestrales (precio real de compra, alquiler real, compraventas, crédito nuevo real, tipo hipotecario, ocupados EPA y población), en tasas log ×100 salvo el tipo, 2004T2-2026T1, dos retardos, ficticias COVID (2020T2-2020T4) e impulso EPA en 2021T1 como exógenas. Para P1, versión larga de cuatro variables desde 1995 (precio, tipo, PIB en volumen y población), con tres shocks identificados (actividad y renta, demográfico, crédito y tipos).

**Identificación.** La tabla pre-registrada (signos en el impacto y el trimestre siguiente más cuatro ceros en la población) no aceptó ninguna rotación entre varios millones de candidatas: los datos rechazan esa tabla conjunta. Se usa la variante pre-registrada V3 (solo impacto, sin la restricción de compraventas), con un tamaño muestral efectivo de los pesos de importancia por encima del objetivo. Variantes: V1 (Euríbor más diferencial, solo impacto) y V2 (factor europeo exógeno). Robustez: uno y cuatro retardos, prior fijo, sin COVID y deflactor alternativo.

**Descomposición histórica: precio real de compra** (media posterior acumulada en el periodo, banda del 68 %; C3s):

| Shock | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| Actividad y renta | 31,8 pp (9,0-54,6 pp) | -10,6 pp (-23,5 a 0,66 pp) | 7,7 pp (-3,5 a 18,2 pp) | 0,27 pp (-7,1 a 4,7 pp) | 7,2 pp (-4,7 a 11,2 pp) |
| Demográfico | 8,9 pp (-5,0 a 24,8 pp) | -2,9 pp (-10,7 a 4,0 pp) | 0,14 pp (-6,6 a 6,8 pp) | -0,27 pp (-4,0 a 3,4 pp) | 0,65 pp (-4,1 a 5,8 pp) |
| Crédito y tipos | 3,0 pp (-7,2 a 14,0 pp) | -8,6 pp (-18,9 a 0,54 pp) | -1,6 pp (-9,8 a 7,1 pp) | -1,3 pp (-4,7 a 4,4 pp) | -0,47 pp (-2,8 a 12,8 pp) |
| Demanda de vivienda | — | -7,4 pp (-17,9 a 2,0 pp) | -0,41 pp (-7,2 a 9,0 pp) | -2,6 pp (-6,0 a 2,4 pp) | -0,30 pp (-2,9 a 11,0 pp) |
| Oferta | — | -4,8 pp (-13,3 a 2,5 pp) | 0,38 pp (-7,3 a 8,0 pp) | -0,80 pp (-4,8 a 3,3 pp) | 1,9 pp (-3,3 a 9,0 pp) |
| No atribuido (banda aproximada; en P5, exacta desde la errata de V16) | 31,6 pp (-6,0 a 74,1 pp) | -9,6 pp (-35,2 a 15,5 pp) | 1,9 pp (-25,2 a 27,6 pp) | -0,75 pp (-16,1 a 12,0 pp) | 9,5 pp (-7,8 a 16,4 pp) |
| Observado | 75,4 pp | -44,0 pp | 8,2 pp | -5,5 pp | 18,4 pp |

**Alquiler real:**

| Shock | P2 | P3 | P4 | P5 |
|---|---|---|---|---|
| Actividad y renta | -1,7 pp (-4,3 a 0,83 pp) | 1,7 pp (-1,1 a 4,8 pp) | -0,81 pp (-2,8 a 0,64 pp) | 0,47 pp (-1,9 a 2,1 pp) |
| Demográfico | 0,33 pp (-1,9 a 2,7 pp) | 0,00 pp (-2,9 a 2,7 pp) | -0,74 pp (-2,3 a 0,65 pp) | 0,07 pp (-1,9 a 2,1 pp) |
| Crédito y tipos | 0,26 pp (-1,5 a 2,1 pp) | 0,24 pp (-1,7 a 2,7 pp) | -1,5 pp (-3,2 a 0,30 pp) | -0,50 pp (-2,6 a 2,3 pp) |
| Demanda de vivienda | -0,32 pp (-2,3 a 1,8 pp) | 0,66 pp (-1,4 a 2,9 pp) | -1,6 pp (-3,2 a 0,12 pp) | -0,30 pp (-2,0 a 2,0 pp) |
| Oferta | -0,06 pp (-2,0 a 1,9 pp) | 0,87 pp (-1,1 a 3,2 pp) | -1,6 pp (-3,6 a 0,10 pp) | 0,37 pp (-1,8 a 2,6 pp) |
| No atribuido (banda aproximada) | -1,2 pp (-7,5 a 5,2 pp) | -4,6 pp (-11,6 a 2,9 pp) | -3,2 pp (-8,1 a 1,4 pp) | -2,0 pp (-7,9 a 3,6 pp) |
| Observado | -2,7 pp | -1,1 pp | -9,3 pp | -1,8 pp |

En síntesis, en la compra de 2022-2026 9,5 pp de los 18,4 pp observados quedan sin atribuir a los shocks identificados de media (banda del 68 % exacta: -7,8 a 16,4 pp, que incluye el cero; mediana 3,4; con el tipo hipotecario del Banco de España, media 20,7) [C3s, condicionado a las restricciones de signo y de cero]. La media es la única medida aditiva (las contribuciones más la parte no atribuida suman lo observado en cada extracción). La posterior tiene colas largas: en la compra de P5, la mediana de crédito y tipos es 3,4 pp y la de actividad y renta 1,1 pp. Por eso el voto del SVAR en la regla se basa en la probabilidad, extracción a extracción, de que cada shock sea el mayor (decisión Y10). Magnitudes posiblemente atenuadas por el prior (sesgo documentado en F3).

## 4. Instrumentos externos (M5)

Los tres instrumentos son débiles; ninguno alcanza C3 (0 de tres):

- **Shocks monetarios del BCE** (Jarociński-Karadi, componente de política monetaria pura): F efectivo 1,83 para el precio y 0,77 para el alquiler; primera etapa con signo contrario al esperado; intervalos de Anderson-Rubin no acotados al 95 %. Las pretendencias pasan, por falta de potencia.
- **Empuje migratorio** (llegadas predichas por la emigración de cada país de origen al resto de la UE, cuotas de 2002): F efectivo 0,05.
- **Bartik sectorial** (cuotas de empleo de 2008 por comunidad): efecto relativo entre comunidades, no comparable con una contribución nacional; F efectivo por debajo de diez. Navarra y La Rioja quedan fuera del instrumento porque Eurostat no publica su empleo del sector inmobiliario en 2008 (dato confidencial): sin cuota del año base, el instrumento no está definido, y no se les asigna cuota cero (errata aplicada en V16; ERRATA.md).

En el alquiler, LP-IV se abstiene en la regla del factor más relevante (F por debajo de diez y Anderson-Rubin al 68 % no acotado). En la compra, el Anderson-Rubin al 68 % está acotado y LP-IV vota cuando supera a todos los factores del SVAR: solo en P4, con una primera etapa de signo contrario al esperado (regla R2). Detalle: `output/v8/M5/resumen.md`.

## 5. Periodos (M0), coeficientes por periodo (M3) y largo plazo (M4)

- **M0.** Los periodos pre-registrados se contrastan con Bai-Perron, Markov switching (número de regímenes por BIC) y umbral de Hansen (tipo real, crédito y paro), detectando solo con series de crédito, tipos y actividad. 2 de 70 coeficientes cumplen la regla del efecto por periodo, y solo 30 son evaluables; tras BH sobre los p de permutación, ninguno. El alquiler no tiene medida alternativa trimestral y su regla queda «no evaluable» (35 coeficientes del alquiler dentro de los 40 no evaluables): es una regla que no se puede aplicar, no una regla incumplida.
- **M3.** Proyecciones locales con interacción por periodo (principal) y VAR por regímenes (contraste, no apto según F3). Diferencias significativas tras BH en una minoría de los contrastes; P4 impreciso. C4.
- **M4.** DOLS, FMOLS y ARDL-bounds con rupturas. El ARDL rechaza la ausencia de cointegración, exigiendo también el contraste t, en 2 de 9 especificaciones; Engle-Granger y Gregory-Hansen en ninguna. Las contribuciones de largo plazo se etiquetan «sin cointegración demostrada» y no votan. La contabilidad hogares-viviendas (brecha entre hogares nuevos y viviendas terminadas, en unidades físicas) vota por demografía en 2 casos (compra de P3 y P5).

## 6. Colinealidad, dominancia y multiverso (M6 y M7)

- **M6.** VIF y diagnóstico de Belsley por periodo; dominancia LMG con bandas bootstrap por bloques «básicas» (algunos puntos quedan fuera de su banda del 68 % por el sesgo del R² remuestreado); ortogonalización en todos los órdenes; índice compuesto; Granger y LP (predictivos, no causales); BMA y ridge o red elástica con validación temporal con embargo. La dominancia reparte el R² (no la variación) y vota por el factor de mayor cuota cuya contribución parcial tiene el signo de la variación observada.
- **Aviso de colinealidad (M6).** La población total y la población extranjera (INE) comparten gran parte de su variación: correlación de sus crecimientos interanuales 0,91 en la muestra completa, 0,98 en P2 (VIF del par 24,89) y 0,78 en P5. M6 usa una variable por familia (VIF máximo 18,38; población total, hasta 7,44), de modo que el diagnóstico de Belsley no recoge el par; las filas de ambas variables en M7 no son pruebas independientes.
- **M7.** Rejilla de 37.980 especificaciones (32.424 estimadas; las fallidas, registradas). Con signos orientados (un tipo más bajo cuenta como presión al alza), 2 de 74 combinaciones de mercado, periodo y factor cumplen la regla del multiverso (signo estable en al menos el 80 % y significativo tras BH en al menos el 50 %): demografía en el alquiler, en P2 y en la muestra completa, con signo positivo (lectura por **familias**). Por **variables**, la misma regla la cumplen 18 de 200 combinaciones de mercado, periodo y variable (15 si las especificaciones fallidas cuentan como «no cumple»); la lista completa, con el porcentaje de mismo signo y de significativas tras BH, está en `output/v8/por_que_ha_subido.md` (apartado «Lectura por variables del multiverso»). Son asociaciones [C4].
- **Signo del tipo real.** El tipo real hipotecario tiene un signo positivo con el crecimiento del precio de compra en P5 y con el del alquiler (P4 y muestra completa). No se interpreta como efecto del tipo: la inflación resta al tipo real y deflacta el precio real, lo que induce un comovimiento positivo por construcción, y tampoco se descarta el sentido inverso (el ciclo del precio acompañando al del tipo).

## 7. Factor común (M1) y análisis regional (M8)

Cuota de la varianza del crecimiento interanual común a las diecisiete comunidades (primer componente; bandas bootstrap por bloques):

| Periodo | Compra (M1) | Alquiler (M1) | Mediana entre CCAA, compra (M8) | Mediana entre CCAA, alquiler (M8) |
|---|---|---|---|---|
| P1 | 64,7 % (56,4-71,2 %) | — | 68,5 % | — |
| P2 | 45,3 % (42,0-54,2 %) | 96,2 % (92,6-97,7 %) | 46,2 % | 96,1 % |
| P3 | 59,6 % (47,8-66,8 %) | 79,6 % (71,5-86,0 %) | 61,9 % | 85,8 % |
| P4 | 45,5 % (42,7-53,1 %) | 99,5 % (99,3-99,7 %) | 46,5 % | 99,8 % |
| P5 | 92,8 % (86,7-94,9 %) | 97,5 % (86,1-98,7 %) | 93,6 % | 98,2 % |

Con pocos trimestres por periodo, la cuota del primer componente está sesgada al alza; como H8-8 no se rechaza, la conclusión es prudente. Parte del crecimiento nacional asociada a la zona euro: 7,4 pp (4,7-8,7 pp) en el tramo final de P1 (la serie de la zona euro empieza en 2006), -15,3 pp (-21,7 a -7,6 pp) en P2, 0,81 pp (-4,4 a 4,0 pp) en P3, 1,4 pp (-1,8 a 3,4 pp) en P4 y -3,3 pp (-7,0 a 1,8 pp) en P5 (C4). En el panel regional, la pendiente del factor común es mecánicamente próxima a uno y no compite en la regla.

**Medida del alquiler y contratos nuevos.** El alquiler real (-1,8 pp en P5) es el IPC de alquiler, que sigue el parque de contratos vivos. Los contratos nuevos suben más, según cifras C1 con dos fuentes por comunidad en 2021-2024 (medida y periodo distintos, no comparables cifra a cifra): Cataluña 16,9 % (16,6-17,2 %) (2021-2024; INE IPVA (AEAT); Incasòl; dato de 2024; C1); Comunitat Valenciana 28,5 % (26,1-30,8 %) (2021-2024; INE IPVA (AEAT); GVA fianzas; dato de 2024; C1).

**València.** En la provincia de Valencia el valor tasado (29,4 pp) y Registradores (17,4 pp) discrepan en P5 y se publican ambos; la ciudad solo tiene valor tasado (43,5 pp), sin contraste con una segunda fuente [C4].

## 8. Aprendizaje automático interpretable (M9, solo contraste)

Gradient boosting con restricciones de monotonía, GAM, DML con cross-fitting por bloques, SHAP agrupado, permutación agrupada, ALE/PDP, interacciones SHAP, modelo sustituto y estabilidad del ranking. Ningún modelo supera a la base más exigente: en el panel de compra, 2,5 pp frente a 2,1 pp. SHAP asigna al factor europeo 2,1 pp (-0,36 a 7,2 pp) en la compra de P5. El turismo solo entra en una sensibilidad no principal limitada a las 6 comunidades con datos, no comparable con la variación nacional. El ranking completo se reproduce en una minoría de réplicas bootstrap. Nada causal se deduce de SHAP ni de las importancias.

## 9. Atribución y regla del factor más relevante (F5)

Regla operativa fijada antes de calcular (R0-R8, `docs/v8/desviaciones.md`): unidad común (pp acumulados en la ventana del periodo); «mayor contribución» = la de mayor contribución en la dirección de lo observado; la parte no atribuida no compite; votos del SVAR (probabilidad de ser el mayor), de la dominancia (cuota de R² con signo), de LP-IV (solo con instrumento fuerte o Anderson-Rubin al 68 % acotado) y de la contabilidad (solo demografía); abstención = no apoya; P4 y el alquiler de P1, imprecisos.

Resultado: **ningún factor designado** en los diez casos; el máximo de votos coincidentes es dos. Probabilidad de que el primer factor del SVAR sea el mayor: compra 71,7 % (P1), 31,8 % (P2), 40,8 % (P3), 25,9 % (P4) y 29,7 % (P5); alquiler 38,8 % (P2), 32,6 % (P3), 24,5 % (P4) y 25,7 % (P5). Fichas: `output/v8/F5/fichas.md`.

## 10. Predicción fuera de muestra

Muestra de prueba común (cinco bloques de ocho trimestres con embargo de cuatro, 2016T2-2026T1); DM-HLN y Holm frente a AR(4):

| Modelo | RMSE compra | p Holm frente a AR(4) | RMSE alquiler | p Holm frente a AR(4) |
|---|---|---|---|---|
| AR(4) | 1,2 pp | — | 0,80 pp | — |
| AR + factor común | 1,3 pp | 0,132 | 0,83 pp | 0,596 |
| BVAR (forma reducida de M2) | 1,4 pp | 0,132 | 0,98 pp | 0,127 |
| ECM v1 (especificación A de v7) | 2,6 pp | 0,012 | 1,7 pp | < 0,001 |

AR(4) es la base más exigente en ambos mercados. Predicciones de 2026T3-2027T2 congeladas (`output/v8/congelacion/`, sha256 en `docs/v8/notas_release.md`); `make evaluate_v8` las evaluará una sola vez.

## 11. Reproducibilidad

`make v8` reconstruye datos, modelos, atribución, tablas, hechos y este informe sin red, con SEED = 20261010 y un hilo. Dos ejecuciones dan ficheros idénticos salvo los tiempos (`tiempos.json`). Revisión de F4: hallazgos J1-J23 y su corrección en `docs/v8/revision_F4.md` y `docs/v8/decisiones.md` (Y9-Y11).

---

*Atribución (Open Database License).* Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. Las cifras construidas con esos datos se publican bajo la misma licencia.
