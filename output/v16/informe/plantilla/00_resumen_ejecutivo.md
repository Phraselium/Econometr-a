## Resumen ejecutivo

**Alcance.** Entran solo los resultados que superan todas sus pruebas: hechos [C1], con dos fuentes independientes, y cotas [C2], con supuestos explícitos. Todo lo de V15 y V16 es [C4] (exploratorio o descriptivo). Ningún resultado alcanza C3. Los rangos [C1] son mínimo y máximo entre fuentes, no intervalos de confianza. <!-- check:cifra-libre (nombres de capa y de versión) -->

**Límites de las herramientas.** Casi ninguna herramienta de inferencia pasó la validación por Monte Carlo; los resultados con herramienta no apta se dan como estimación puntual, sin p ni intervalo. El cegado de las réplicas fue parcial (decisión K19): en varios lotes el replicador vio los valores publicados antes de estimar. <!-- check:cifra-libre (decisión K19) -->

**Evaluación sellada.** evaluate_v16 no aplica: ninguna pregunta de V16 cumple las condiciones del hallazgo, así que V16 no tiene evaluación sellada pendiente. Las hipótesis de V15 sí la tienen, con su calendario (al final de este resumen). <!-- check:cifra-libre (nombres de versión y de función) -->

**Pre-registros.** Los de V15 y V16 son pre-registros internos sin sello de tiempo externo. V15: etiqueta prereg-v15 en el remoto, commit 542b4fd, 2026-10-17. V16: etiqueta prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiquetas, hashes y fechas del registro de pre-registros) -->

### Hechos vigentes [C1]

- **Hogares.** Entre 2021 y 2025 el número de hogares aumentó {{dh_2125}} [C1]. Es la cifra de la 1.0: combina la ECP (stock a 1 de enero) y la EPA (media anual), sin corrección, y las ventanas son distintas (v7.1, K4b-dh). La cifra de V16 {{V16-CON-HOG-CAMBIO}} [C4] alinea las dos fuentes al 1 de enero de 2021 y de 2025 (valor: ECP; máximo: EPA); por eso su extremo EPA es mayor y queda fuera del rango [C1]. La cifra C1 de la 1.0 no cambia. <!-- check:cifra-libre (periodo y fechas de las ventanas) -->
- **Obra terminada.** En el territorio común, las viviendas terminadas al año son {{terminadas_1924}} [C1]. Coinciden el Ministerio (fin de obra) y el Catastro (altas). <!-- check:cifra-libre (periodo) -->
- **Precio de compra, 2015-2025.** El núcleo de registros da {{A23-P2}} [C1]. <!-- check:cifra-libre (periodo) -->
- **Precio de compra, 2019-2025.** Dos medidas, que discrepan; se dan ambas. Precio medio por m², sin ajuste de calidad. Nominal: {{V16-HEC-PRECIO-NOM-2019-2025}} [C1]. Real, con el deflactor del IPC general: {{V16-HEC-PRECIO-REAL-2019-2025}} [C1]. IPV del INE, ajustado por calidad (una sola fuente): nominal {{V16-HEC-IPV-NOM-2019-2025:valor}} / real {{V16-HEC-IPV-REAL-2019-2025:valor}} [C4]. Se citan siempre las dos medidas y la versión real junto a la nominal. <!-- check:cifra-libre (periodo) -->
- **Alquiler de contratos vigentes, 2015-2024.** IPC de alquiler e IPVA: {{A23-A2}} [C1]. <!-- check:cifra-libre (periodo) -->
- **Alquiler de contratos nuevos, 2021-2024.** Cataluña: {{A23-A9}} [C1]. Comunitat Valenciana: {{A23-A10}} [C1]. <!-- check:cifra-libre (periodo) -->
- **Contratos nuevos frente a vigentes, Cataluña, 2021-2024.** La brecha de crecimiento es {{V16-HEC-ALQ-BRECHA-2124-CAT}} [C1]. <!-- check:cifra-libre (periodo) -->
- **Tenencia.** Hogares con la vivienda principal en propiedad: {{R1C-001}} [C1].

### Cotas vigentes [C2]

Valen dentro de la rejilla de escenarios del autor. Se cita la rejilla junto con la cota.

- **Déficit 2021-2024.** Sin bajas del parque: {{L3-DEF-2124-SINBAJAS}} [C2]. Sin las dos variantes que conservan el salto de la EPA: {{L3-DEF-2124-SENS}} [C2]. <!-- check:cifra-libre (periodo) -->
- **Hogares proyectados por el INE.** 2026-2035: {{B1-H4}} [C2]. 2026-2030: {{B2-H3}} [C2]. <!-- check:cifra-libre (periodos) -->
- **Déficit hasta 2030.** Empeora en todos los escenarios de la rejilla a escala nacional [C2]. Por provincias, en {{T4-H3:num}} provincias empeora, en {{T4-H3:min}} mejora y en {{T4-H3:max}} queda indeterminado [C2]. <!-- check:cifra-libre (año) -->
- **Demanda latente de jóvenes**, por convivencia con los padres, frente a 2008: {{latente_convivencia}} [C2]. <!-- check:cifra-libre (año) -->
- **Vivienda turística.** El aumento 2020-2024 equivale como máximo a {{B4-v3-vut-cantidad}} [C2]. Es una cota de cantidad (sustitución uno a uno): {{VER-B4-V2-1}} [C2]. <!-- check:cifra-libre (periodo) -->

### Sin hallazgo robusto en V15 y V16

Una línea por resultado, con su capa y la razón. Sin cifras: las magnitudes están en las Partes II, IV, V y VII.

- **H1** (zonas tensionadas, renta de contratos nuevos, Cataluña). Pista [C4] solo en el signo, negativo. La magnitud no se cita: fallan pretendencias y placebo temporal, y las cotas no lo permiten. <!-- check:cifra-libre (id de hipótesis) -->
- **H2** (número de contratos). [C4]. Sin señal estable. No se cita. <!-- check:cifra-libre (id de hipótesis) -->
- **H3** (vivienda turística, alquiler por sección). [C4]. No concluyente, no nula: la medida varía poco y el coeficiente queda por debajo del efecto mínimo detectable. <!-- check:cifra-libre (id de hipótesis) -->
- **H4** (inmigración, alquiler municipal). Correlación frágil [C4]. Cambia de signo al quitar los cinco orígenes de mayor peso, y la mediana del multiverso es menor que la estimación principal. <!-- check:cifra-libre (id de hipótesis y recuento de orígenes del diseño) -->
- **H5** (predicción del valor tasado). Pista [C4]: la combinación no supera al AR(4). La razón del error es mayor que uno en todas las implementaciones, incluida la réplica ciega. <!-- check:cifra-libre (id de hipótesis y AR(4)) -->
- **E1, E2, E4.** [C4]. Descriptivas: herramientas sin validar, sin intervalos o pretendencias incumplidas. <!-- check:cifra-libre (ids de análisis exploratorio) -->
- **E3** (dependencia espacial del alquiler municipal). Correlación espacial descriptiva [C4]. No es contagio: puede recoger una tendencia regional común. <!-- check:cifra-libre (id de análisis exploratorio) -->
- **Q1** (zonas tensionadas). [C4]. Q1b no es estimable: no hay periodo posterior al tratamiento. Q1c tiene pocas provincias tratadas y rupturas previas; no se cita. <!-- check:cifra-libre (ids de pregunta) -->
- **Q2** (turismo). [C4]. Q2a, no concluyente. Q2c, de signo inestable. Q2b, solo robustez. <!-- check:cifra-libre (ids de pregunta) -->
- **Q3** (inmigración, escalas provincial y de sección). Q3-b, correlación frágil [C4]: tiene una pretendencia del mismo orden y la mediana del multiverso es menor que la estimación principal. <!-- check:cifra-libre (ids de pregunta) -->
- **Q4** (oferta). [C4]. La Red Natura no es exógena y los residuos tienen dependencia espacial. <!-- check:cifra-libre (id de pregunta) -->
- **Q5** (tipos de interés). [C4]. El multiverso no apoya el signo. <!-- check:cifra-libre (id de pregunta) -->
- **Q6** (ITP). [C4]. Q6-p, no concluyente. Q6-v, con placebo mayor y de signo contrario. <!-- check:cifra-libre (ids de pregunta) -->
- **Q7** (ayudas al alquiler joven). [C4]. Descriptiva, sin intervalo, con potencia en el límite. <!-- check:cifra-libre (id de pregunta) -->
- **Q8** (compras de no residentes). [C4]. Descriptiva: la fuente no separa UE de extra-UE. <!-- check:cifra-libre (id de pregunta) -->
- **Q9** (burbuja). Pista no confirmada [C4]: la exuberancia se trata en la Parte VII. <!-- check:cifra-libre (id de pregunta y de parte) -->
- **Q10** (predicción). [C4]. Sin mejora sobre el AR(4) fuera de 2020. <!-- check:cifra-libre (id de pregunta, AR(4) y año) -->
- **Rejilla multiescala.** [C4]. Ninguna de las 83 celdas tiene un p válido. <!-- check:cifra-libre (número de celdas del diseño) -->

### Pendientes de la evaluación sellada (V15)

Las cinco hipótesis de V15 no están confirmadas: están pendientes. Fecha límite: 31-12-2027. Lo que no se evalúe entonces queda «no evaluable» y no alcanza C3. <!-- check:cifra-libre (fecha límite del calendario y nombre de capa) -->

- **H1 y H2:** primera fecha posible, hacia marzo de 2027. <!-- check:cifra-libre (ids de hipótesis y fecha del calendario) -->
- **H5:** hacia octubre de 2027. <!-- check:cifra-libre (id de hipótesis y fecha del calendario) -->
- **H4:** último trimestre de 2027, con riesgo de no llegar a la fecha límite. <!-- check:cifra-libre (id de hipótesis y fecha del calendario) -->
- **H3** (réplica, no confirmatoria): último trimestre de 2027. <!-- check:cifra-libre (id de hipótesis y fecha del calendario) -->

### Summary

**Scope.** Only results that pass all their tests are reported: facts [C1] backed by two independent sources, and bounds [C2] with explicit assumptions. Everything from V15 and V16 is [C4] (exploratory or descriptive); nothing reaches C3. Almost no inference tool passed the Monte Carlo validation, and the blinding of the replications was partial (decision K19). evaluate_v16 does not apply, so V16 has no sealed evaluation pending; the V15 ones are pending. The V15 and V16 pre-registrations are internal, with no external timestamp: prereg-v15 (commit 542b4fd) and prereg-v16 (commit a8304ec), both dated 2026-10-17. <!-- check:cifra-libre (etiquetas, hashes, fechas y decisión K19) -->

**Facts [C1].** Households rose by {{dh_2125:num}} in 2021-2025 (annual-average window; the 1 January window is reported separately as [C4]). Annual completions in the common territory are {{terminadas_1924:rango}} dwellings per year. Purchase prices rose {{A23-P2:num}} % over 2015-2025 (core of registers). In 2019-2025 two measures differ and both are given. Average price per m² without quality adjustment: nominal {{V16-HEC-PRECIO-NOM-2019-2025:num}} %, real {{V16-HEC-PRECIO-REAL-2019-2025:num}} %. Quality-adjusted INE index (single source) [C4]: nominal {{V16-HEC-IPV-NOM-2019-2025:num}} %, real {{V16-HEC-IPV-REAL-2019-2025:num}} %. Rents of existing contracts, 2015-2024: {{A23-A2:rango}} %. New contracts, 2021-2024: Catalonia {{A23-A9:num}} %, Comunitat Valenciana {{A23-A10:num}} %. The growth gap between new and existing contracts in Catalonia is {{V16-HEC-ALQ-BRECHA-2124-CAT:num}} percentage points. Home ownership: {{R1C-001:num}} % of households. <!-- check:cifra-libre (periodos) -->

**Bounds [C2]**, valid within the scenario grid. Deficit 2021-2024 without dwelling losses: {{L3-DEF-2124-SINBAJAS:num}} dwellings. Projected household growth, 2026-2035: {{B1-H4:num}} households. Deficit worsens to 2030 in every scenario. Tourist dwellings: at most {{B4-v3-vut-cantidad:num}} % of the rental stock. <!-- check:cifra-libre (periodos) -->

**No robust finding.** For H1 only the sign (negative) is citable; the magnitude is not cited. H5: the combination does not beat the AR(4), in every implementation. E3 is a descriptive spatial correlation, not contagion. H4 and Q3-b are fragile correlations. H3, Q2a and Q6-p are inconclusive. All other questions are descriptive, lack valid inference, or fail pre-trends and placebos. Q9 (bubble) is an unconfirmed lead, discussed in Part VII. <!-- check:cifra-libre (ids de hipótesis y pregunta, AR(4), número de parte) -->

**Pending.** The V15 hypotheses await the sealed evaluation: H1 and H2 from about March 2027, H5 about October 2027, H4 and H3 in the last quarter of 2027. Deadline: 31-12-2027. <!-- check:cifra-libre (fechas del calendario) -->
