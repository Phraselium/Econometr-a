# Informe econométrico V8: factores, periodos y factor común de los precios de la vivienda en España

Borja Romero, economista (firma individual, independiente). Generado por `make v8` desde `docs/v8/plantillas/informe_econometrico.md`; cada cifra procede de `output/v5/cifras_clave.csv` (ids `V8-…`). Lectura no técnica: `output/v8/por_que_ha_subido.md`. Tablas en formato de revista: `output/v8/tablas_modelos_destacados.md` y `output/v8/tablas_v8.xlsx`.

## Abstract (English)

We decompose real house-price and rent growth in Spain (1995-2026) into seven pre-registered factor families across five pre-registered periods, using four attribution methods: a Bayesian SVAR identified with sign and zero restrictions (historical decomposition), LMG dominance analysis, local projections with external instruments (ECB high-frequency shocks, an EU-migration shift-share push and a sectoral Bartik), and household-dwelling accounting. A designation rule fixed before estimation requires agreement of three of four methods, sign stability in at least 80 % of a structured multiverse and a 68 % structural band excluding zero. No factor is designated in any of the ten market-period cells. The pre-registered SVAR identification is rejected by the data (no accepted rotations) and the impact-only variant is used; all three instruments are weak (effective F well below ten). The activity-and-income shock in 1995-2007 is the only structural contribution whose band excludes zero. Regional co-movement is highest in 2022-2026, and the Spanish common factor is associated with euro-area house prices (Holm-adjusted p below the five per cent level). No model beats an AR(4) out of sample. An independent review found and corrected a mis-specified 2021 labour-survey dummy; both versions are published.

## 1. Diseño

- **Pre-registro.** `docs/v8/hipotesis.md` (etiqueta local `prereg-v8`), escrito antes de cualquier estimación con datos reales. Desviaciones con fecha y motivo en `docs/v8/desviaciones.md`; decisiones en `docs/v8/decisiones.md` (Y0-Y11).
- **Herramientas.** Validadas por Monte Carlo antes de usarse (F3; `output/v8/F3/*/validacion.md`): BVAR normal-Wishart con hiperparámetros por verosimilitud marginal, restricciones de signo y de cero, Bai-Perron y umbral con bootstrap sieve-AR, Markov switching, DFM/PCA, LP y LP-IV con intervalos de Anderson-Rubin, dominancia LMG, permutación de fechas, SHAP agrupado y multiverso con registro.
- **Control del azar.** Holm dentro de las tres familias confirmatorias ({H8-1…H8-4}, {H8-5…H8-7}, {H8-8, H8-9}); BH (q = 0,10) en todo lo exploratorio. Toda especificación probada está en el Registry (`output/v8/*/registro.csv`).
- **Capas.** C3s para la descomposición histórica del SVAR (condicionada a las restricciones); C4 para todo lo demás. Ningún resultado alcanza C3.
- **Revisión independiente.** Tras las herramientas (`docs/v8/revision_F3.md`) y tras los modelos (`docs/v8/revision_F4.md`: aprobar con correcciones; SVAR rehecho una vez).

## 2. Hipótesis confirmatorias

| id | Hipótesis | Estimación (intervalo al 95 %) | p ajustado (Holm) | Capa |
|---|---|---|---|---|
| H8-1 | Demografía empuja el alquiler real en P5 (SVAR) | {{V8-H8-1-est}} | {{V8-H8-1-pholm:num}} | {{V8-H8-1-est:capa}} |
| H8-2 | Crédito y tipos restan al precio real en P5 (SVAR) | {{V8-H8-2-est}} | {{V8-H8-2-pholm:num}} | {{V8-H8-2-est:capa}} |
| H8-3 | Actividad y renta suman al precio real en P3 (SVAR) | {{V8-H8-3-est}} | {{V8-H8-3-pholm:num}} | {{V8-H8-3-est:capa}} |
| H8-4 | Crédito más actividad restan al precio real en P2 (SVAR) | {{V8-H8-4-est}} | {{V8-H8-4-pholm:num}} | {{V8-H8-4-est:capa}} |
| H8-5 | Shock contractivo del BCE reduce el precio real (LP-IV) | F efectivo {{V8-H8-5-F:num}}; t de la forma reducida {{V8-H8-5-tFR:num}} | {{V8-H8-5-pholm:num}} | {{V8-H8-5-F:capa}} |
| H8-6 | Shock contractivo del BCE reduce el alquiler real (LP-IV) | F efectivo {{V8-H8-6-F:num}}; t {{V8-H8-6-tFR:num}} | {{V8-H8-6-pholm:num}} | {{V8-H8-6-F:capa}} |
| H8-7 | Empuje migratorio aumenta el alquiler real (LP-IV) | F efectivo {{V8-H8-7-F:num}}; t {{V8-H8-7-tFR:num}} | {{V8-H8-7-pholm:num}} | {{V8-H8-7-F:capa}} |
| H8-8 | Componente común > 50 % de la varianza en cada periodo | cuota mínima {{V8-H8-8-est}} | {{V8-H8-8-pholm:num}} | {{V8-H8-8-est:capa}} |
| H8-9 | Factor común español y zona euro covarían positivamente | {{V8-H8-9-est}} | {{V8-H8-9-pholm:num}} | {{V8-H8-9-est:capa}} |

Solo H8-9 se sostiene tras Holm, y es una asociación. En H8-5 a H8-7 los p unilaterales de Anderson-Rubin usan el signo **a priori** de la primera etapa; la primera etapa estimada de los shocks del BCE tiene el signo contrario (corrección J3 de la revisión). Las estimaciones de H8-1 a H8-4 con la especificación errónea de la ficticia EPA (escalón) quedan publicadas como retiradas en `output/v8/M2/hipotesis_m2_retirada.csv`; ninguna decisión de Holm cambia con la corrección.

## 3. SVAR bayesiano con restricciones de signo y de cero (M2)

**Especificación.** Siete variables nacionales trimestrales (precio real de compra, alquiler real, compraventas, crédito nuevo real, tipo hipotecario, ocupados EPA y población), en tasas log ×100 salvo el tipo, 2004T2-2026T1, dos retardos, ficticias COVID (2020T2-2020T4) e impulso EPA en 2021T1 como exógenas. Para P1, versión larga de cuatro variables desde 1995 (precio, tipo, PIB en volumen y población).

**Identificación.** La tabla pre-registrada (signos en el impacto y el trimestre siguiente más cuatro ceros en la población) no aceptó ninguna rotación entre varios millones de candidatas: los datos rechazan esa tabla conjunta. Se usa la variante pre-registrada V3 (solo impacto, sin la restricción de compraventas), con un tamaño muestral efectivo de los pesos de importancia por encima del objetivo. Variantes: V1 (Euríbor más diferencial, solo impacto) y V2 (factor europeo exógeno). Robustez: uno y cuatro retardos, prior fijo, sin COVID y deflactor alternativo.

**Descomposición histórica: precio real de compra** (media posterior acumulada en el periodo, banda del 68 %; C3s):

| Shock | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| Actividad y renta | {{V8-SVAR-c-P1-empleo_renta-media}} | {{V8-SVAR-c-P2-empleo_renta-media}} | {{V8-SVAR-c-P3-empleo_renta-media}} | {{V8-SVAR-c-P4-empleo_renta-media}} | {{V8-SVAR-c-P5-empleo_renta-media}} |
| Demográfico | {{V8-SVAR-c-P1-demografia-media}} | {{V8-SVAR-c-P2-demografia-media}} | {{V8-SVAR-c-P3-demografia-media}} | {{V8-SVAR-c-P4-demografia-media}} | {{V8-SVAR-c-P5-demografia-media}} |
| Crédito y tipos | {{V8-SVAR-c-P1-credito_tipos-media}} | {{V8-SVAR-c-P2-credito_tipos-media}} | {{V8-SVAR-c-P3-credito_tipos-media}} | {{V8-SVAR-c-P4-credito_tipos-media}} | {{V8-SVAR-c-P5-credito_tipos-media}} |
| Demanda de vivienda | — | {{V8-SVAR-c-P2-demanda_vivienda-media}} | {{V8-SVAR-c-P3-demanda_vivienda-media}} | {{V8-SVAR-c-P4-demanda_vivienda-media}} | {{V8-SVAR-c-P5-demanda_vivienda-media}} |
| Oferta | — | {{V8-SVAR-c-P2-oferta-media}} | {{V8-SVAR-c-P3-oferta-media}} | {{V8-SVAR-c-P4-oferta-media}} | {{V8-SVAR-c-P5-oferta-media}} |
| No atribuido | {{V8-QNA-pp-c-P1}} | {{V8-QNA-pp-c-P2}} | {{V8-QNA-pp-c-P3}} | {{V8-QNA-pp-c-P4}} | {{V8-QNA-pp-c-P5}} |
| Observado | {{V8-OBS-c-P1}} | {{V8-OBS-c-P2}} | {{V8-OBS-c-P3}} | {{V8-OBS-c-P4}} | {{V8-OBS-c-P5}} |

**Alquiler real:**

| Shock | P2 | P3 | P4 | P5 |
|---|---|---|---|---|
| Actividad y renta | {{V8-SVAR-a-P2-empleo_renta-media}} | {{V8-SVAR-a-P3-empleo_renta-media}} | {{V8-SVAR-a-P4-empleo_renta-media}} | {{V8-SVAR-a-P5-empleo_renta-media}} |
| Demográfico | {{V8-SVAR-a-P2-demografia-media}} | {{V8-SVAR-a-P3-demografia-media}} | {{V8-SVAR-a-P4-demografia-media}} | {{V8-SVAR-a-P5-demografia-media}} |
| Crédito y tipos | {{V8-SVAR-a-P2-credito_tipos-media}} | {{V8-SVAR-a-P3-credito_tipos-media}} | {{V8-SVAR-a-P4-credito_tipos-media}} | {{V8-SVAR-a-P5-credito_tipos-media}} |
| Demanda de vivienda | {{V8-SVAR-a-P2-demanda_vivienda-media}} | {{V8-SVAR-a-P3-demanda_vivienda-media}} | {{V8-SVAR-a-P4-demanda_vivienda-media}} | {{V8-SVAR-a-P5-demanda_vivienda-media}} |
| Oferta | {{V8-SVAR-a-P2-oferta-media}} | {{V8-SVAR-a-P3-oferta-media}} | {{V8-SVAR-a-P4-oferta-media}} | {{V8-SVAR-a-P5-oferta-media}} |
| No atribuido | {{V8-QNA-pp-a-P2}} | {{V8-QNA-pp-a-P3}} | {{V8-QNA-pp-a-P4}} | {{V8-QNA-pp-a-P5}} |
| Observado | {{V8-OBS-a-P2}} | {{V8-OBS-a-P3}} | {{V8-OBS-a-P4}} | {{V8-OBS-a-P5}} |

La media es la única medida aditiva (las contribuciones más la parte no atribuida suman lo observado en cada extracción). La posterior tiene colas largas: en la compra de P5, la mediana de crédito y tipos es {{V8-SVAR-c-P5-credito_tipos-mediana:valor}} y la de actividad y renta {{V8-SVAR-c-P5-empleo_renta-mediana:valor}}. Por eso el voto del SVAR en la regla se basa en la probabilidad, extracción a extracción, de que cada shock sea el mayor (decisión Y10). Magnitudes posiblemente atenuadas por el prior (sesgo documentado en F3).

## 4. Instrumentos externos (M5)

Los tres instrumentos son débiles; ninguno alcanza C3 ({{V8-M5-c3:num}} de tres):

- **Shocks monetarios del BCE** (Jarociński-Karadi, componente de política monetaria pura): F efectivo {{V8-H8-5-F:num}} para el precio y {{V8-H8-6-F:num}} para el alquiler; primera etapa con signo contrario al esperado; intervalos de Anderson-Rubin no acotados al 95 %. Las pretendencias pasan, por falta de potencia.
- **Empuje migratorio** (llegadas predichas por la emigración de cada país de origen al resto de la UE, cuotas de 2002): F efectivo {{V8-H8-7-F:num}}.
- **Bartik sectorial** (cuotas de empleo de 2008 por comunidad): efecto relativo entre comunidades, no comparable con una contribución nacional; F efectivo por debajo de diez.

Con F por debajo de diez y Anderson-Rubin no acotado, el método LP-IV se abstiene en la regla del factor más relevante (regla R2). Detalle: `output/v8/M5/resumen.md`.

## 5. Periodos (M0), coeficientes por periodo (M3) y largo plazo (M4)

- **M0.** Los periodos pre-registrados se contrastan con Bai-Perron, Markov switching (número de regímenes por BIC) y umbral de Hansen (tipo real, crédito y paro), detectando solo con series de crédito, tipos y actividad. {{V8-M0-cumplen:num}} de {{V8-M0-coef:num}} coeficientes cumplen la regla del efecto por periodo; tras BH sobre los p de permutación, ninguno. El alquiler no tiene medida alternativa trimestral y su regla queda «no evaluable».
- **M3.** Proyecciones locales con interacción por periodo (principal) y VAR por regímenes (contraste, no apto según F3). Diferencias significativas tras BH en una minoría de los contrastes; P4 impreciso. C4.
- **M4.** DOLS, FMOLS y ARDL-bounds con rupturas. El ARDL rechaza la ausencia de cointegración, exigiendo también el contraste t, en {{V8-M4-ardl-rechaza:num}} de {{V8-M4-ardl-total:num}} especificaciones; Engle-Granger y Gregory-Hansen en ninguna. Las contribuciones de largo plazo se etiquetan «sin cointegración demostrada» y no votan. La contabilidad hogares-viviendas (brecha entre hogares nuevos y viviendas terminadas, en unidades físicas) vota por demografía en {{V8-M4-voto-demografia:num}} casos (compra de P3 y P5).

## 6. Colinealidad, dominancia y multiverso (M6 y M7)

- **M6.** VIF y diagnóstico de Belsley por periodo; dominancia LMG con bandas bootstrap por bloques centradas; ortogonalización en todos los órdenes; índice compuesto; Granger y LP (predictivos, no causales); BMA y ridge o red elástica con validación temporal con embargo. La dominancia reparte el R² (no la variación) y vota por el factor de mayor cuota cuya contribución parcial tiene el signo de la variación observada.
- **M7.** Rejilla de {{V8-M7-rejilla:num}} especificaciones ({{V8-M7-ajustadas:num}} estimadas; las fallidas, registradas). Con signos orientados (un tipo más bajo cuenta como presión al alza), {{V8-M7-cumplen:num}} de {{V8-M7-combinaciones:num}} combinaciones de mercado, periodo y factor cumplen la regla del multiverso (signo estable en al menos el 80 % y significativo tras BH en al menos el 50 %): demografía en el alquiler, en P2 y en la muestra completa, con signo positivo.

## 7. Factor común (M1) y análisis regional (M8)

Cuota de la varianza del crecimiento interanual común a las diecisiete comunidades (primer componente; bandas bootstrap por bloques):

| Periodo | Compra (M1) | Alquiler (M1) | Mediana entre CCAA, compra (M8) | Mediana entre CCAA, alquiler (M8) |
|---|---|---|---|---|
| P1 | {{V8-M1-cuota-c-P1}} | — | {{V8-M8-comun-c-P1}} | — |
| P2 | {{V8-M1-cuota-c-P2}} | {{V8-M1-cuota-a-P2}} | {{V8-M8-comun-c-P2}} | {{V8-M8-comun-a-P2}} |
| P3 | {{V8-M1-cuota-c-P3}} | {{V8-M1-cuota-a-P3}} | {{V8-M8-comun-c-P3}} | {{V8-M8-comun-a-P3}} |
| P4 | {{V8-M1-cuota-c-P4}} | {{V8-M1-cuota-a-P4}} | {{V8-M8-comun-c-P4}} | {{V8-M8-comun-a-P4}} |
| P5 | {{V8-M1-cuota-c-P5}} | {{V8-M1-cuota-a-P5}} | {{V8-M8-comun-c-P5}} | {{V8-M8-comun-a-P5}} |

Con pocos trimestres por periodo, la cuota del primer componente está sesgada al alza; como H8-8 no se rechaza, la conclusión es prudente. Parte del crecimiento nacional asociada a la zona euro: {{V8-M1-eur-c-P1}} en P1, {{V8-M1-eur-c-P2}} en P2, {{V8-M1-eur-c-P3}} en P3, {{V8-M1-eur-c-P4}} en P4 y {{V8-M1-eur-c-P5}} en P5 (C4). En el panel regional, la pendiente del factor común es mecánicamente próxima a uno y no compite en la regla.

## 8. Aprendizaje automático interpretable (M9, solo contraste)

Gradient boosting con restricciones de monotonía, GAM, DML con cross-fitting por bloques, SHAP agrupado, permutación agrupada, ALE/PDP, interacciones SHAP, modelo sustituto y estabilidad del ranking. Ningún modelo supera a la base más exigente: en el panel de compra, {{V8-M9-oos-c-panel-ml}} frente a {{V8-M9-oos-c-panel-base}}. SHAP asigna al factor europeo {{V8-M9-shap-c-P5-factor_europeo}} y al turismo {{V8-M9-shap-c-P5-turismo}} en la compra de P5; el segundo queda fuera de su banda bootstrap y solo hay datos de turismo para {{V8-M9-turismo-ccaa:num}} comunidades. El ranking completo se reproduce en una minoría de réplicas bootstrap. Nada causal se deduce de SHAP ni de las importancias.

## 9. Atribución y regla del factor más relevante (F5)

Regla operativa fijada antes de calcular (R0-R8, `docs/v8/desviaciones.md`): unidad común (pp acumulados en la ventana del periodo); «mayor contribución» = la que más empuja en la dirección de lo observado; la parte no atribuida no compite; votos del SVAR (probabilidad de ser el mayor), de la dominancia (cuota de R² con signo), de LP-IV (solo con instrumento fuerte o Anderson-Rubin al 68 % acotado) y de la contabilidad (solo demografía); abstención = no apoya; P4 y el alquiler de P1, imprecisos.

Resultado: **ningún factor designado** en los diez casos; el máximo de votos coincidentes es dos. Probabilidad de que el primer factor del SVAR sea el mayor: compra {{V8-PFSTAR-c-P1}} (P1), {{V8-PFSTAR-c-P2}} (P2), {{V8-PFSTAR-c-P3}} (P3), {{V8-PFSTAR-c-P4}} (P4) y {{V8-PFSTAR-c-P5}} (P5); alquiler {{V8-PFSTAR-a-P2}} (P2), {{V8-PFSTAR-a-P3}} (P3), {{V8-PFSTAR-a-P4}} (P4) y {{V8-PFSTAR-a-P5}} (P5). Fichas: `output/v8/F5/fichas.md`.

## 10. Predicción fuera de muestra

Muestra de prueba común (cinco bloques de ocho trimestres con embargo de cuatro, 2016T2-2026T1); DM-HLN y Holm frente a AR(4):

| Modelo | RMSE compra | p Holm frente a AR(4) | RMSE alquiler | p Holm frente a AR(4) |
|---|---|---|---|---|
| AR(4) | {{V8-OOS-c-ar4-rmse}} | — | {{V8-OOS-a-ar4-rmse}} | — |
| AR + factor común | {{V8-OOS-c-ar_fc-rmse}} | {{V8-OOS-c-ar_fc-pholm:num}} | {{V8-OOS-a-ar_fc-rmse}} | {{V8-OOS-a-ar_fc-pholm:num}} |
| BVAR (forma reducida de M2) | {{V8-OOS-c-bvar_m2-rmse}} | {{V8-OOS-c-bvar_m2-pholm:num}} | {{V8-OOS-a-bvar_m2-rmse}} | {{V8-OOS-a-bvar_m2-pholm:num}} |
| ECM v1 (especificación A de v7) | {{V8-OOS-c-ecm_v1-rmse}} | {{V8-OOS-c-ecm_v1-pholm:num}} | {{V8-OOS-a-ecm_v1-rmse}} | {{V8-OOS-a-ecm_v1-pholm:num}} |

AR(4) es la base más exigente en ambos mercados. Predicciones de 2026T3-2027T2 congeladas (`output/v8/congelacion/`, sha256 en `docs/v8/notas_release.md`); `make evaluate_v8` las evaluará una sola vez.

## 11. Reproducibilidad

`make v8` reconstruye datos, modelos, atribución, tablas, hechos y este informe sin red, con SEED = 20261010 y un hilo. Dos ejecuciones dan ficheros idénticos salvo los tiempos (`tiempos.json`). Revisión de F4: hallazgos J1-J23 y su corrección en `docs/v8/revision_F4.md` y `docs/v8/decisiones.md` (Y9-Y11).
