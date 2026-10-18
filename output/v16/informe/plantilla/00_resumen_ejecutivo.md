## Resumen ejecutivo

**Alcance.** Entran solo los resultados que superan todas sus pruebas: hechos [C1], con dos fuentes independientes, y cotas [C2], con supuestos explícitos. Todo lo de V15 y V16 es [C4] (exploratorio o descriptivo). Ningún resultado alcanza C3. Los rangos [C1] son mínimo y máximo entre fuentes, no intervalos de confianza. <!-- check:cifra-libre (nombres de capa y de versión) -->

**Pre-registros.** Los de V15 y V16 son pre-registros internos sin sello de tiempo externo. V15: etiqueta prereg-v15 en el remoto, commit 542b4fd, 2026-10-17. V16: etiqueta prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiquetas, hashes y fechas del registro de pre-registros) -->

### Hechos vigentes [C1]

- **Hogares.** Entre 2021 y 2025 el número de hogares aumentó {{dh_2125}} [C1]. Los extremos son la ECP y la EPA, sin corrección. <!-- check:cifra-libre (periodo) -->
- **Obra terminada.** En el territorio común, las viviendas terminadas al año son {{terminadas_1924}} [C1]. Coinciden el Ministerio (fin de obra) y el Catastro (altas). <!-- check:cifra-libre (periodo) -->
- **Precio de compra, 2015-2025.** El núcleo de registros da {{A23-P2}} [C1]. <!-- check:cifra-libre (periodo) -->
- **Precio de compra, 2019-2025.** Medida: precio medio por m², sin ajuste de calidad. Nominal: {{V16-HEC-PRECIO-NOM-2019-2025}} [C1]. Real, con el deflactor del IPC general: {{V16-HEC-PRECIO-REAL-2019-2025}} [C1]. El IPV del INE, ajustado por calidad, da una variación mayor: la cifra figura en la definición de V16-HEC-PRECIO-NOM-2019-2025 y no tiene id propio, así que no se cita aquí. Se citan siempre las dos medidas y la versión real junto a la nominal. <!-- check:cifra-libre (periodo) -->
- **Alquiler de contratos vigentes, 2015-2024.** IPC de alquiler e IPVA: {{A23-A2}} [C1]. <!-- check:cifra-libre (periodo) -->
- **Alquiler de contratos nuevos, 2021-2024.** Cataluña: {{A23-A9}} [C1]. Comunitat Valenciana: {{A23-A10}} [C1]. <!-- check:cifra-libre (periodo) -->
- **Contratos nuevos frente a vigentes, Cataluña, 2021-2024.** La brecha de crecimiento es {{V16-HEC-ALQ-BRECHA-2124-CAT}} [C1]. <!-- check:cifra-libre (periodo) -->
- **Tenencia.** Hogares con la vivienda principal en propiedad: {{R1C-001}} [C1].

### Cotas vigentes [C2]

Valen dentro de la rejilla de escenarios del autor. Se cita la rejilla junto con la cota.

- **Déficit 2021-2024.** Sin bajas del parque: {{L3-DEF-2124-SINBAJAS}} [C2]. Sin las dos variantes que conservan el salto de la EPA: {{L3-DEF-2124-SENS}} [C2]. <!-- check:cifra-libre (periodo) -->
- **Hogares proyectados por el INE.** 2026-2035: {{B1-H4}} [C2]. 2026-2030: {{B2-H3}} [C2]. <!-- check:cifra-libre (periodos) -->
- **Déficit hasta 2030.** Empeora en todos los escenarios de la rejilla y no mejora en ninguna provincia [C2]. <!-- check:cifra-libre (año) -->
- **Demanda latente de jóvenes**, por convivencia con los padres, frente a 2008: {{latente_convivencia}} [C2]. <!-- check:cifra-libre (año) -->
- **Vivienda turística.** El aumento 2020-2024 equivale como máximo a {{B4-v3-vut-cantidad}} [C2]. Es una cota de cantidad (sustitución uno a uno): {{VER-B4-V2-1}} [C2]. <!-- check:cifra-libre (periodo) -->

### Sin hallazgo robusto en V15 y V16

Cada línea da la razón. Sin cifras salvo en las pistas citables.

- **H1** (zonas tensionadas, renta de contratos nuevos, Cataluña). Pista [C4] solo en el signo, negativo. Sin magnitud: falla pretendencias y placebo temporal, y no hay inferencia válida. <!-- check:cifra-libre (id de hipótesis) -->
- **H2** (número de contratos). Sin señal estable. No se cita. <!-- check:cifra-libre (id de hipótesis) -->
- **H3** (vivienda turística, alquiler por sección). No concluyente, no nula: la medida varía poco y el coeficiente queda por debajo del efecto mínimo detectable. <!-- check:cifra-libre (id de hipótesis) -->
- **H4** (inmigración, alquiler municipal). Correlación frágil [C4]: {{V15-H4-beta}}. Cambia de signo al quitar los cinco orígenes de mayor peso. Mediana del multiverso: {{V15-H4-mediana:valor}} [C4] <!-- check:cifra-libre (id de hipótesis) -->
- **H5** (predicción del valor tasado). Pista [C4]: la combinación no supera al AR(4). Razón del ECM {{V15-H5-razon-ecm:valor}} en la implementación pre-registrada; la réplica ciega da una razón menor ({{V15-H5-razon-replica:valor}} [C4]). La conclusión es la misma en todas las implementaciones. <!-- check:cifra-libre (id de hipótesis y del AR(4)) -->
- **E1, E2, E4.** Descriptivas: herramientas sin validar, sin intervalos o pretendencias incumplidas. <!-- check:cifra-libre (ids de análisis exploratorio) -->
- **E3** (dependencia espacial del alquiler municipal). Correlación espacial descriptiva [C4]: ρ = {{V15-E3-rho:num}}, con rango de multiverso {{V15-E3-rho:rango}}. No es contagio: puede recoger una tendencia regional común. <!-- check:cifra-libre (id de análisis exploratorio) -->
- **Q1** (zonas tensionadas). Q1b no es estimable: no hay periodo posterior al tratamiento. Q1c tiene pocas provincias tratadas y rupturas previas. <!-- check:cifra-libre (ids de pregunta) -->
- **Q2** (turismo). Q2a, no concluyente. Q2c, de signo inestable. Q2b, solo robustez. <!-- check:cifra-libre (ids de pregunta) -->
- **Q3** (inmigración, escalas provincial y de sección). Q3-b, correlación frágil [C4]: {{V16-Q3-b-beta}}, con una pretendencia del mismo orden ({{V16-Q3-b-pretendencia}}). Mediana del multiverso: {{V16-Q3-b-mediana:valor}} [C4] <!-- check:cifra-libre (ids de pregunta) -->
- **Q4** (oferta). La Red Natura no es exógena y los residuos tienen dependencia espacial. <!-- check:cifra-libre (id de pregunta) -->
- **Q5** (tipos de interés). El multiverso no apoya el signo. <!-- check:cifra-libre (id de pregunta) -->
- **Q6** (ITP). Q6-p, no concluyente. Q6-v, con placebo mayor y de signo contrario. <!-- check:cifra-libre (ids de pregunta) -->
- **Q7** (ayudas al alquiler joven). Descriptiva, sin intervalo, con potencia en el límite. <!-- check:cifra-libre (id de pregunta) -->
- **Q8** (compras de no residentes). Descriptiva: la fuente no separa UE de extra-UE. <!-- check:cifra-libre (id de pregunta) -->
- **Q9** (burbuja). Pista no confirmada: va a la Parte VII. <!-- check:cifra-libre (id de pregunta y de parte) -->
- **Q10** (predicción). Sin mejora sobre el AR(4) fuera de 2020. <!-- check:cifra-libre (id de pregunta, AR(4) y año) -->
- **Rejilla multiescala.** Ninguna de las 83 celdas tiene un p válido. <!-- check:cifra-libre (número de celdas del diseño) -->

### Pendientes de la evaluación sellada (V15)

Las cinco hipótesis de V15 no están confirmadas: están pendientes. Fecha límite: 31-12-2027. Lo que no se evalúe entonces queda «no evaluable» y no alcanza C3. <!-- check:cifra-libre (fecha límite del calendario y nombre de capa) -->

- **H1 y H2:** primera fecha posible, hacia marzo de 2027. <!-- check:cifra-libre (ids de hipótesis y fecha del calendario) -->
- **H5:** hacia octubre de 2027. <!-- check:cifra-libre (id de hipótesis y fecha del calendario) -->
- **H4:** último trimestre de 2027, con riesgo de no llegar a la fecha límite. <!-- check:cifra-libre (id de hipótesis y fecha del calendario) -->
- **H3** (réplica, no confirmatoria): último trimestre de 2027. <!-- check:cifra-libre (id de hipótesis y fecha del calendario) -->

### Summary

**Scope.** Only results that pass all their tests are reported: facts [C1] backed by two independent sources, and bounds [C2] with explicit assumptions. Everything from V15 and V16 is [C4] (exploratory or descriptive); nothing reaches C3. The V15 and V16 pre-registrations are internal, with no external timestamp: prereg-v15 (commit 542b4fd) and prereg-v16 (commit a8304ec), both dated 2026-10-17. <!-- check:cifra-libre (etiquetas, hashes y fechas) -->

**Facts [C1].** Households rose by {{dh_2125}} in 2021-2025. Annual completions in the common territory are {{terminadas_1924}}. Purchase prices rose {{A23-P2}} over 2015-2025 (core of registers). In 2019-2025, on average price per m² without quality adjustment: nominal {{V16-HEC-PRECIO-NOM-2019-2025}}, real {{V16-HEC-PRECIO-REAL-2019-2025}}. The quality-adjusted INE index gives a larger change: la cifra figura en la definición de V16-HEC-PRECIO-NOM-2019-2025 y no tiene id propio, así que no se cita aquí. Rents of existing contracts, 2015-2024: {{A23-A2}}. New contracts, 2021-2024: Catalonia {{A23-A9}}, Comunitat Valenciana {{A23-A10}}. The growth gap between new and existing contracts in Catalonia is {{V16-HEC-ALQ-BRECHA-2124-CAT}}. Home ownership: {{R1C-001}}. <!-- check:cifra-libre (periodos) -->

**Bounds [C2]**, valid within the scenario grid. Deficit 2021-2024 without dwelling losses: {{L3-DEF-2124-SINBAJAS}}. Projected household growth, 2026-2035: {{B1-H4}}. Deficit worsens to 2030 in every scenario. Tourist dwellings: at most {{B4-v3-vut-cantidad}} of the rental stock. <!-- check:cifra-libre (periodos) -->

**No robust finding.** For H1 only the sign (negative) is citable. H5: the combination does not beat the AR(4); ECM ratio {{V15-H5-razon-ecm:valor}} in the pre-registered implementation, lower in the blind replication. E3 is a descriptive spatial correlation, not contagion. H4 and Q3-b are fragile correlations. H3, Q2a and Q6-p are inconclusive. All other questions are descriptive, lack valid inference, or fail pre-trends and placebos. Q9 (bubble) is an unconfirmed lead, discussed in Part VII. <!-- check:cifra-libre (ids de hipótesis y pregunta, AR(4), número de parte) -->

**Pending.** The V15 hypotheses await the sealed evaluation: H1 and H2 from about March 2027, H5 about October 2027, H4 and H3 in the last quarter of 2027. Deadline: 31-12-2027. <!-- check:cifra-libre (fechas del calendario) -->
