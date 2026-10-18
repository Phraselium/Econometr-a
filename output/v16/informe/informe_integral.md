# Vivienda en España: informe integral (V16)

Informe integral de la versión V16 del proyecto (docs/v16/plan.md, fase 7). Toda cifra procede de output/v5/cifras_clave.csv, con su
capa (C1 hechos con al menos dos fuentes; C2 cotas; C3 y C3s efectos; C4 exploratorio). Los resultados de V15 y V16 tienen
pre-registro interno, sin sello de tiempo externo (etiquetas prereg-v15 y prereg-v16 en el remoto). Generado por src/v16/f7_informe.py;
no se edita a mano.


## Resumen ejecutivo

**Alcance.** Entran solo los resultados que superan todas sus pruebas: hechos [C1], con dos fuentes independientes, y cotas [C2], con supuestos explícitos. Todo lo de V15 y V16 es [C4] (exploratorio o descriptivo). Ningún resultado alcanza C3. Los rangos [C1] son mínimo y máximo entre fuentes, no intervalos de confianza. <!-- check:cifra-libre (nombres de capa y de versión) -->

**Límites de las herramientas.** Casi ninguna herramienta de inferencia pasó la validación por Monte Carlo; los resultados con herramienta no apta se dan como estimación puntual, sin p ni intervalo. El cegado de las réplicas fue parcial (decisión K19): en varios lotes el replicador vio los valores publicados antes de estimar. <!-- check:cifra-libre (decisión K19) -->

**Evaluación sellada.** evaluate_v16 no aplica: ninguna pregunta de V16 cumple las condiciones del hallazgo, así que V16 no tiene evaluación sellada pendiente. Las hipótesis de V15 sí la tienen, con su calendario (al final de este resumen). <!-- check:cifra-libre (nombres de versión y de función) -->

**Pre-registros.** Los de V15 y V16 son pre-registros internos sin sello de tiempo externo. V15: etiqueta prereg-v15 en el remoto, commit 542b4fd, 2026-10-17. V16: etiqueta prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiquetas, hashes y fechas del registro de pre-registros) -->

### Hechos vigentes [C1]

- **Hogares.** Entre 2021 y 2025 el número de hogares aumentó 997.586 hogares (981.823-1.013.350 hogares) [C1]. Es la cifra de la 1.0: combina la ECP (stock a 1 de enero) y la EPA (media anual), sin corrección, y las ventanas son distintas (v7.1, K4b-dh). La cifra de V16 981.823 hogares (981.823-1.062.300 hogares) [C4] alinea las dos fuentes al 1 de enero de 2021 y de 2025 (valor: ECP; máximo: EPA); por eso su extremo EPA es mayor y queda fuera del rango [C1]. La cifra C1 de la 1.0 no cambia. <!-- check:cifra-libre (periodo y fechas de las ventanas) -->
- **Obra terminada.** En el territorio común, las viviendas terminadas al año son 72.264-94.426 viviendas/año [C1]. Coinciden el Ministerio (fin de obra) y el Catastro (altas). <!-- check:cifra-libre (periodo) -->
- **Precio de compra, 2015-2025.** El núcleo de registros da 47,2 % (44,2-56,1 %) [C1]. <!-- check:cifra-libre (periodo) -->
- **Precio de compra, 2019-2025.** Dos medidas, que discrepan; se dan ambas. Precio medio por m², sin ajuste de calidad. Nominal: 30,4 % (29,6-31,7 %) [C1]. Real, con el deflactor del IPC general: 7,1 % (6,5-8,2 %) [C1]. IPV del INE, ajustado por calidad (una sola fuente): nominal 44,4 % / real 18,7 % [C4]. Se citan siempre las dos medidas y la versión real junto a la nominal. <!-- check:cifra-libre (periodo) -->
- **Alquiler de contratos vigentes, 2015-2024.** IPC de alquiler e IPVA: 10,9-22,9 % [C1]. <!-- check:cifra-libre (periodo) -->
- **Alquiler de contratos nuevos, 2021-2024.** Cataluña: 16,9 % (16,6-17,2 %) [C1]. Comunitat Valenciana: 28,5 % (26,1-30,8 %) [C1]. <!-- check:cifra-libre (periodo) -->
- **Contratos nuevos frente a vigentes, Cataluña, 2021-2024.** La brecha de crecimiento es 10,8 p.p. (9,7-11,9 p.p.) [C1]. <!-- check:cifra-libre (periodo) -->
- **Tenencia.** Hogares con la vivienda principal en propiedad: 74,5 % de hogares (72,1-75,9 % de hogares) [C1].

### Cotas vigentes [C2]

Valen dentro de la rejilla de escenarios del autor. Se cita la rejilla junto con la cota.

- **Déficit 2021-2024.** Sin bajas del parque: 549.952 viviendas (389.361-710.542 viviendas) [C2]. Sin las dos variantes que conservan el salto de la EPA: 653.456 viviendas (596.371-710.542 viviendas) [C2]. <!-- check:cifra-libre (periodo) -->
- **Hogares proyectados por el INE.** 2026-2035: 1.720.537 hogares (1.308.531-1.772.410 hogares) [C2]. 2026-2030: 1.024.156 hogares (819.421-1.060.364 hogares) [C2]. <!-- check:cifra-libre (periodos) -->
- **Déficit hasta 2030.** Empeora en todos los escenarios de la rejilla a escala nacional [C2]. Por provincias, en 15 provincias empeora, en 0 provincias mejora y en 37 provincias queda indeterminado [C2]. <!-- check:cifra-libre (año) -->
- **Demanda latente de jóvenes**, por convivencia con los padres, frente a 2008: 188.000-506.000 hogares [C2]. <!-- check:cifra-libre (año) -->
- **Vivienda turística.** El aumento 2020-2024 equivale como máximo a 2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler) [C2]. Es una cota de cantidad (sustitución uno a uno): 81.771 viviendas (81.771-81.771 viviendas) [C2]. <!-- check:cifra-libre (periodo) -->

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

**Facts [C1].** Households rose by 997.586 in 2021-2025 (annual-average window; the 1 January window is reported separately as [C4]). Annual completions in the common territory are 72.264-94.426 viviendas/año dwellings per year. Purchase prices rose 47,2 % over 2015-2025 (core of registers). In 2019-2025 two measures differ and both are given. Average price per m² without quality adjustment: nominal 30,4 %, real 7,1 %. Quality-adjusted INE index (single source) [C4]: nominal 44,4 %, real 18,7 %. Rents of existing contracts, 2015-2024: 10,9-22,9 % %. New contracts, 2021-2024: Catalonia 16,9 %, Comunitat Valenciana 28,5 %. The growth gap between new and existing contracts in Catalonia is 10,8 percentage points. Home ownership: 74,5 % of households. <!-- check:cifra-libre (periodos) -->

**Bounds [C2]**, valid within the scenario grid. Deficit 2021-2024 without dwelling losses: 549.952 dwellings. Projected household growth, 2026-2035: 1.720.537 households. Deficit worsens to 2030 in every scenario. Tourist dwellings: at most 2,7 % of the rental stock. <!-- check:cifra-libre (periodos) -->

**No robust finding.** For H1 only the sign (negative) is citable; the magnitude is not cited. H5: the combination does not beat the AR(4), in every implementation. E3 is a descriptive spatial correlation, not contagion. H4 and Q3-b are fragile correlations. H3, Q2a and Q6-p are inconclusive. All other questions are descriptive, lack valid inference, or fail pre-trends and placebos. Q9 (bubble) is an unconfirmed lead, discussed in Part VII. <!-- check:cifra-libre (ids de hipótesis y pregunta, AR(4), número de parte) -->

**Pending.** The V15 hypotheses await the sealed evaluation: H1 and H2 from about March 2027, H5 about October 2027, H4 and H3 in the last quarter of 2027. Deadline: 31-12-2027. <!-- check:cifra-libre (fechas del calendario) -->

---

*Atribución (Open Database License).* Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. Las cifras construidas con esos datos se publican bajo la misma licencia.


## Parte I · Diagnóstico

Esta parte recoge los hechos de la fase 2 de V16 a todas las escalas: nacional, comunidad autónoma (CCAA), provincia y municipio donde hay dato. No estima efectos. Cada cifra lleva su capa entre corchetes y, cuando hay varias fuentes, su rango. <!-- check:cifra-libre (fase 2 y versión V16) -->

### I.1 Cómo leer las cifras

- **[C1] Hecho.** Al menos dos fuentes de grupos distintos coinciden dentro de una tolerancia fijada antes de mirar las parejas nuevas. Se escribe «es» y se da el rango entre fuentes.
- **[C2] Cota.** Intervalo con supuestos explícitos.
- **[C4] Descriptivo o exploratorio.** Una sola fuente, o varias que no coinciden, o fuentes que no son independientes. Se escribe «se observa» y no se interpreta.
- **Si dos fuentes discrepan, se dan ambas.** No se elige una.
- **Medida de precio.** Cada cifra de compra dice qué mide. El IPV del INE está ajustado por calidad. Valor tasado (MIVAU), Notariado y Registradores son precios medios por m² sin ese ajuste. Son medidas distintas y pueden dar cuantías distintas.
- **Pre-registro.** Los resultados de V16 citados aquí tienen un pre-registro interno, sin sello de tiempo externo: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. Los de V15, igual: etiqueta `prereg-v15`, commit 542b4fd, 2026-10-17. Los de esta parte son hechos y contabilidad (fase 2), no contrastes de hipótesis. <!-- check:cifra-libre (etiquetas, commit y fecha de pre-registro, años) -->

### I.2 Precio de compra

#### Nacional: nominal y real

**2019-2025.** El cambio acumulado nominal es 30,4 % (29,6-31,7 %) [C1]. El cambio real, con el deflactor del IPC general, es 7,1 % (6,5-8,2 %) [C1]. Las tres medidas por m² (tasación MIVAU, Notariado, Registradores) coinciden dentro de la tolerancia. El IPV del INE, ajustado por calidad, es otra medida y da otra cuantía: nominal 44,4 % y real 18,7 % [C4], de fuente única. Queda fuera del rango de las otras tres. Se dan ambas medidas y no se elige una. <!-- check:cifra-libre (periodo) -->

**Otras ventanas.** Las medidas no coinciden, así que se publica el abanico y no se elige una.

| Ventana | Nominal | Real (IPC general) |
|---|---|---|
| 2007-2025 | -1,9 a 20,3 % [C4] | -31,3 a -15,7 % [C4] |
| 2013-2025 | 42,3-86,9 % [C4] | 13,0-48,4 % [C4] |

<!-- check:cifra-libre (periodos en la tabla) -->

**La 1.0, 2015-2025.** El IPV del INE da 79,9 % [C4]. El núcleo formado por MIVAU, Notariado y Registradores es 47,2 % (44,2-56,1 %) [C1]. Los dos datos discrepan y se dan ambos. El residuo sin identificar entre ambos es -30,9 pp [C4]; no se descompone. <!-- check:cifra-libre (versión 1.0, periodo) -->

**Precio por m² en 2025.** Registradores: 2.284 EUR/m2 [C4]. Notariado: 1.949 EUR/m2 [C4]. Son medidas distintas, de composición distinta. <!-- check:cifra-libre (periodo) -->

**Las fuentes se mueven juntas.** El primer componente de las cuatro fuentes recoge 89,2 % [C4] de la varianza de la tasa anual. Es un resumen de comovimiento, no una explicación. <!-- check:cifra-libre (cuatro fuentes, diseño) -->

#### Comunidades autónomas

- Por CCAA se publican las tres medidas en `output/v16/f2_hechos/precios_ccaa.csv`. El deflactor es nacional: no hay IPC autonómico en el repositorio.
- Las medidas coinciden en el cambio real 2019-2025 en 10 CCAA de las 17 [C4]. En 2007-2025, en 10 [C4]. En 2013-2025, en 1 [C4]. Fuera de esas comunidades, la medida elegida cambia la cuantía. <!-- check:cifra-libre (17 comunidades, periodos) -->
- Las ocho CCAA de la decisión K8 aparecen solo a escala de CCAA y nación. Nunca por provincia ni por debajo. <!-- check:cifra-libre (ocho CCAA del diseño) -->

#### Provincia: parte común y parte local

Se descompone la tasa anual de ln precio (valor tasado MIVAU, nominal, provincias no selladas) en un factor común y un residuo local. Es contabilidad, no causalidad.

| Periodo | Cuota del factor común (IC 95 % bootstrap) | R² mediano por provincia (mín.-máx.) |
|---|---|---|
| 2007-2013 | 71,4 % (40,0-82,9 %) [C4] | 76,0 % (16,3-93,5 %) [C4] |
| 2014-2019 | 52,9 % (24,8-63,1 %) [C4] | 53,2 % (1,1-88,0 %) [C4] |
| 2020-2026 | 80,9 % (40,2-86,1 %) [C4] | 83,1 % (51,0-95,6 %) [C4] |

<!-- check:cifra-libre (periodos y nivel de confianza en la tabla) -->

- **Sesgo de la cuota.** Con pocas series y pocos periodos, la cuota queda sesgada al alza incluso sin factor. Por eso se lee como cota superior de la parte común y no como su valor. Este informe no cuantifica ese sesgo.
- **Contraste con V8.** V8 estimó el factor común sobre CCAA. Con provincias, la cuota difiere de V8 en -7,7 pp (-14,5 a -3,7 pp) [C4]. Discrepan y se informan ambas. Una explicación posible, no contrastada, es que las CCAA agregan provincias y promedian parte del residuo local. <!-- check:cifra-libre (versión V8) -->
- **Factor dinámico.** Un factor dinámico de una sola componente da R² medio con el factor de 45,0 % (17,6-45,0 %) [C4].
- **Residuo local.** Tras quitar el factor, las correlaciones entre provincias de la misma CCAA son 0,02 correlación (0,02-0,11 correlación) [C4]. Son pequeñas: el residuo es sobre todo específico de cada provincia.
- **Dispersión provincial.** El cociente P90/P10 del valor tasado por m² entre provincias no selladas es 2,7 [C4] en 2026T2. <!-- check:cifra-libre (periodo, P90/P10 en el texto) -->

#### Municipio

A escala municipal solo València tiene valor tasado: el MIVAU publica los municipios con nombre, no con código INE. Para el resto de municipios no hay medida de precio de compra comparable en el repositorio. El atlas (Parte IV) usa el alquiler y la renta.

### I.3 Alquiler: contratos vigentes frente a contratos nuevos

**Qué mide cada serie.** El IPC de alquiler y SERPAVI miden el conjunto de contratos vigentes (stock). El IPVA separa contratos nuevos y existentes. Las fianzas (Incasòl, GVA) recogen contratos nuevos. IPVA y SERPAVI comparten fuente primaria (AEAT-IRPF): cuentan como un solo grupo.

**Nacional, contratos vigentes.**
- IPC de alquiler 2019-2025: cambio nominal 10,1 % [C4] y real -9,5 % [C4].
- 2013-2025: nominal 12,3 % [C4], real -10,8 % [C4].
- 2007-2025: nominal 23,7 % [C4], real -13,3 % [C4].
- Con tres fuentes (IPC, IPVA, SERPAVI), el cambio nominal de los contratos vigentes 2019-2024 va de 7,5-21,2 % [C4]; el real, de -9,3 a 2,3 % [C4].
- La 1.0 da, para 2015-2024, un núcleo IPC-IPVA de 10,9-22,9 % [C1]. SERPAVI, con renta declarada y composición constante, da 43,0 % [C4] y discrepa del núcleo. Se dan ambos.
- En 2025 solo hay una fuente (el IPC); IPVA y SERPAVI acaban en 2024.

<!-- check:cifra-libre (periodos, tres fuentes, versión 1.0) -->

**Contratos nuevos frente a vigentes.**
- Brecha de crecimiento 2021-2024 en Cataluña: es 10,8 p.p. (9,7-11,9 p.p.) [C1], con dos estimaciones independientes (IPVA frente a fianzas menos IPC).
- En la Comunitat Valenciana, las dos estimaciones dan 16,0-23,6 p.p. [C4]. No coinciden dentro de la tolerancia y no llegan a C1.
- Brecha de nivel en 2024 (IPVA): Cataluña 10,8 % [C4]; Comunitat Valenciana 19,2 % [C4]. Nacional, brecha nuevo menos existente: 13,6 % [C4].
- Contratos nuevos 2021-2024 (1.0): en Cataluña, IPVA nuevo e Incasòl dan 16,9 % (16,6-17,2 %) [C1]; en la Comunitat Valenciana, IPVA nuevo y fianzas GVA dan 28,5 % (26,1-30,8 %) [C1].
- Con fianzas hasta 2025: Cataluña 12,6 p.p. [C4]; Comunitat Valenciana 36,2 p.p. [C4]. En 2025 no hay segunda fuente.
- Rotación: las fianzas equivalen a 25,0 % (25,0-43,2 %) [C4] de los contratos vigentes en Cataluña y a 13,5 % (13,5-15,8 %) [C4] en la Comunitat Valenciana.
- Cuota implícita de contratos nuevos en el IPVA: 16,0 % (13,9-17,6 %) [C4].

<!-- check:cifra-libre (periodos, versión 1.0) -->

**Cómo leer una cifra de alquiler.** Un dato de contratos vigentes no describe lo que paga quien firma hoy. Un dato de fianzas o de contratos nuevos no describe lo que paga el conjunto de inquilinos. Hay que decir cuál de los dos se usa.

**Escala territorial.** SERPAVI da alquiler mediano por m² en 1.390 municipios publicables [C4] (n y CV por celda; Parte IV). Inside Airbnb queda fuera de la serie de alquiler: es turístico y es un rastreo no validado. <!-- check:cifra-libre (n y CV, umbrales de publicación del diseño) -->

### I.4 Esfuerzo de acceso: compra y alquiler

Fuente: ECV 2004-2025 (microdatos) con intervalos bootstrap aproximados. Todo es [C4]: fuente única. ECV y Eurostat son la misma encuesta; la coincidencia con Eurostat valida la implementación, no forma un C1. Entre 2013 y 2025 coincide con Eurostat; entre 2004 y 2012 no coincide en casi todos los años y esos años se tratan como no validados. <!-- check:cifra-libre (periodos de validación) -->

**España.** La sobrecarga del coste de la vivienda (gasto neto superior al 40 % de la renta neta) es 7,2 % de la población (6,8-7,7 % de la población) [C4] de la población en 2025. Con el umbral del 30 %: 12,0 % de la población (11,4-12,7 % de la población) [C4]. Cambio 2019-2025: -1,4 puntos porcentuales (-2,2 a -0,43 puntos porcentuales) [C4]; 2015-2025: -3,2 puntos porcentuales (-4,2 a -2,2 puntos porcentuales) [C4]; 2008-2025: -2,9 puntos porcentuales (-3,8 a -2,0 puntos porcentuales) [C4]. Personas que quedan por debajo del umbral de pobreza tras pagar la vivienda: 9,3 % de la población (8,7-9,9 % de la población) [C4]. <!-- check:cifra-libre (umbrales del 40 % y del 30 % del diseño, periodos) -->

**Esfuerzo de compra.** Se mide en propietarios con hipoteca. Sobrecarga 2025: 3,4 % de la población (2,8-4,2 % de la población) [C4]. Cambio 2019-2025: -0,24 puntos porcentuales (-1,5 a 0,95 puntos porcentuales) [C4]. Propietarios sin hipoteca: 1,9 % de la población (1,6-2,1 % de la población) [C4]. El gasto recoge intereses, no amortización, en esta variable; no es el precio de compra. No hay en el repositorio una cifra de años de renta por vivienda tipo. La más cercana es el cambio del cociente precio/renta disponible del índice OCDE en 2019-2025: España 13,7 % [C4], mediana UE 3,2 % [C4]. <!-- check:cifra-libre (periodos) -->

**Esfuerzo de alquiler.** Alquiler a precio de mercado, sobrecarga 2025: 26,8 % de la población (24,6-29,3 % de la población) [C4]. Cambio 2019-2025: -10,6 puntos porcentuales (-14,7 a -6,0 puntos porcentuales) [C4]; 2015-2025: -16,5 puntos porcentuales (-21,0 a -11,5 puntos porcentuales) [C4]. Alquiler reducido o cesión: 8,4 % de la población (6,8-10,1 % de la población) [C4]. La 1.0, en la misma medida para alquiler de mercado, da 26,8 % (24,4-29,2 %) [C4]. Son la misma encuesta con implementaciones distintas. <!-- check:cifra-libre (periodos, versión 1.0) -->

**Por grupo (sobrecarga del 40 %, 2025).**
- Quintil de renta: Q1 27,7 % de la población (25,7-29,9 % de la población) [C4]; Q2 5,2 % de la población (4,5-6,0 % de la población) [C4]; Q3 1,9 % de la población (1,5-2,3 % de la población) [C4]; Q4 0,89 % de la población (0,60-1,2 % de la población) [C4]. El quintil 5 queda suprimido por muestra insuficiente.
- Edad del sustentador: 16-34 años 12,8 % de la población (10,8-15,2 % de la población) [C4]; 35-49 8,6 % de la población (7,7-9,5 % de la población) [C4]; 50-64 5,9 % de la población (5,1-6,9 % de la población) [C4]; 65 o más 4,6 % de la población (4,1-5,1 % de la población) [C4].
- Nacionalidad del sustentador: española 4,6 % de la población (4,3-5,0 % de la población) [C4]; otra de la UE 18,5 % de la población (15,5-22,2 % de la población) [C4]; de fuera de la UE 25,4 % de la población (22,1-29,4 % de la población) [C4].
- Región (NUTS2): la ECV no tiene provincia. Los valores por región, con intervalos, están en `output/v16/f2_esfuerzo/esfuerzo_por_anio.csv`. El cociente P90/P10 entre CCAA es 2,0 [C4] en 2025; el atlas (Parte IV) lo muestra por territorio.

<!-- check:cifra-libre (umbral del 40 %, quintiles, tramos de edad, P90/P10 en el texto) -->

**Descomposición contable 2019-2025.** El cambio observado del esfuerzo medio en alquiler de mercado es -6,2 puntos porcentuales de la renta neta (-8,4 a -4,3 puntos porcentuales de la renta neta) [C4]; la parte atribuida a la composición por reponderación (DFL) es -10,0 puntos porcentuales de la renta neta (-12,0 a -7,9 puntos porcentuales de la renta neta) [C4]. En propietarios con hipoteca, el cambio observado es 0,81 puntos porcentuales de la renta neta (-0,10 a 1,6 puntos porcentuales de la renta neta) [C4] y la composición, -3,6 puntos porcentuales de la renta neta (-4,3 a -3,0 puntos porcentuales de la renta neta) [C4]. Es una suma contable: la renta entra a la vez en la ratio y como covariable. No se lee como mecanismo. Los métodos discrepan en la mitad de las comparaciones y se publican todos (`comparacion_metodos.csv`). <!-- check:cifra-libre (periodos, mitad de las comparaciones) -->

**Esfuerzo de alquiler por territorio fino.** La ratio descriptiva «alquiler anual de 80 m² sobre renta neta del hogar» (SERPAVI y ADRH) no es la tasa de sobrecarga de la ECV y no debe compararse con ella. Está disponible en 10.773 secciones censales publicables en 2023 [C4]. Detalle en la Parte IV. <!-- check:cifra-libre (80 m², año) -->

### I.5 Hogares, viviendas terminadas y déficit

#### Hogares

**Aumento 2021-2025 (1.0).** El aumento del número de hogares es 997.586 hogares (981.823-1.013.350 hogares) [C1]. Los dos extremos son ECP y EPA, sin corrección. La ECP sola da 981.823 hogares [C4]; la EPA da un cambio mayor en 8,2 % [C4]. Se dan ambas. <!-- check:cifra-libre (versión 1.0) -->

**Dos cifras de hogares, dos ventanas.** `dh_2125` compara la ECP, que es un stock a 1 de enero, con la EPA, que es una media anual. Sus dos extremos son posteriores a la ruptura de la EPA de 2021. `V16-CON-HOG-CAMBIO` mide el cambio del 1 de enero de 2021 al 1 de enero de 2025 en ambas fuentes, con otra ventana para la EPA. El C1 usa la primera porque cumple la regla de la 1.0: extremos posteriores a la ruptura y dos fuentes dentro de la tolerancia. La segunda queda en C4. Por eso el máximo de 1.062.300 hogares no se contradice con el rango de `dh_2125`: son ventanas distintas. <!-- check:cifra-libre (identificadores, 1 de enero, versión 1.0) -->

**Contabilidad del cambio de hogares 2021-2025 (ECP).** Cambio observado: 981.823 hogares [C4] en la ECP; con la EPA llega a 1.062.300 hogares [C4]. Se reparte así:
- población: 670.187 hogares (662.247-680.789 hogares) [C4];
- composición por nacionalidad: -80.764 hogares (-84.075 a -77.809 hogares) [C4];
- estructura por edad: 371.922 hogares (363.855-381.513 hogares) [C4];
- residuo de jefatura: 20.478 hogares (20.478-97.285 hogares) [C4].

La composición resta porque las tasas de jefatura por edad del Censo 2021 son menores en la población extranjera. Mezcla migración y cambios de nacionalidad. El residuo de jefatura es una tasa agregada a población constante, no una tasa por edad: no hay tasas por edad después de 2021.

**Por CCAA (11 CCAA sin provincias selladas).** El residuo de jefatura, en porcentaje de los hogares iniciales, tiene mediana y rango 0,22 % (-0,21 a 1,4 %) [C4]. La parte de población en el cambio: 37,3 % del cambio (-31,4 a 91,7 % del cambio) [C4]. Las provincias están en `output/v16/f2_contabilidad/hogares_ecp_2021_2025.csv`. Las ocho CCAA de K8 no se calculan. <!-- check:cifra-libre (11 CCAA, ocho CCAA del diseño) -->

**Serie larga 2002-2021 (EPA, nacional).** Cambio 4.276.400 hogares [C4]: población 2.353.708 hogares (2.194.101-2.512.956 hogares) [C4]; composición -202.133 hogares (-218.730 a -139.312 hogares) [C4]; estructura por edad 2.012.790 hogares (1.570.414-2.159.620 hogares) [C4]; jefatura 112.035 hogares (112.035-399.827 hogares) [C4]. El reparto depende de la tasa de referencia: con las tasas del Censo 2011 la jefatura sería otra. En 2014-2021 el residuo de jefatura es -677.776 hogares [C4], compatible con la ruptura de la EPA en 2021T1. No se interpreta. <!-- check:cifra-libre (periodos, trimestre de la ruptura) -->

**Antecedente V12, 2011-2021.** Crecimiento de hogares 455.531 hogares [C4], con componentes de población 196.494 hogares (195.104-197.884 hogares) [C4], estructura por edad 1.071.741 hogares (966.831-1.176.650 hogares) [C4] y jefatura -812.704 hogares (-919.003 a -706.404 hogares) [C4]. Hogares con persona de referencia extranjera en 2021: 9,7 % (9,7-9,8 %) [C4]. No se repiten en V16. <!-- check:cifra-libre (versiones V12 y V16, periodo) -->

**Hogares proyectados por el INE [C2].** Crecimiento de hogares 2026-2035: 1.720.537 hogares (1.308.531-1.772.410 hogares) [C2]. En 2026-2030: 1.024.156 hogares (819.421-1.060.364 hogares) [C2]. Son proyecciones, no observaciones. <!-- check:cifra-libre (periodos) -->

#### Viviendas terminadas

- **Territorio común, 2019-2024 (1.0).** Las viviendas terminadas al año son 72.264-94.426 viviendas/año [C1] (Ministerio y Catastro, dentro de ±15 %; sin País Vasco ni Navarra).
- **Ampliación a 2025 (MIVAU, solo libres).** En 2025: 80.792 viviendas [C4]. Acumulado 2021-2025: 411.900 viviendas [C4]. Por hogar nuevo (ECP): 0,42 viviendas por hogar [C4]. Esta ampliación no sustituye a `terminadas_1924` ni a `dh_2125`; las terminadas de la 1.0 incluyen protegidas.

<!-- check:cifra-libre (periodos, tolerancia del diseño, identificadores, versión 1.0) -->

#### Déficit acumulado

El déficit es hogares nuevos menos viviendas terminadas. Las viviendas liberadas por envejecimiento nunca se restan de la necesidad: la proyección de hogares del INE ya las descuenta.
- 2021-2024, sin bajas del parque, todas las variantes de corrección de la EPA y de terminadas: 549.952 viviendas (389.361-710.542 viviendas) [C2].
- Misma cota sin las dos variantes que conservan el salto de la EPA: 653.456 viviendas (596.371-710.542 viviendas) [C2].
- Con las bajas estimadas en la versión 5.1: 654.646 viviendas (389.361-765.994 viviendas) [C4].
- 2021-2025, sin bajas: 705.778 viviendas (523.606-887.950 viviendas) [C4]; el dato de terminadas de 2025 es frágil.

Los rangos recogen el desacuerdo entre fuentes y correcciones, no una incertidumbre estadística. <!-- check:cifra-libre (periodos, versión 5.1) -->

### I.6 Demografía

- **Población y migración.** Saldo migratorio exterior (EMCR) 2021-2024: 2.186.663 personas (1.482.129-2.186.663 personas) [C4]. La población extranjera de la ECP crece en un importe que incluye cambios de nacionalidad; no se concilian las dos cifras. EMCR solo se usa desde 2021 por la ruptura de nivel anterior.
- **Dónde se concentra.** Entre municipios no sellados, el cociente P90/P10 de la población de nacionalidad extranjera es 17,8 [C4] (censo anual 2025). El de la renta es 1,8 [C4] (2023).
- **Jóvenes en el hogar de origen.** Personas de 30 a 34 años que viven con al menos uno de sus padres: 27,1 % (26,5-27,7 %) [C4] en 2018 y 31,7 % (30,8-32,5 %) [C4] en 2025 (EPA).
- **Demanda latente de jóvenes [C2].** Por convivencia con los padres, frente a 2008: 188.000-506.000 hogares [C2]. Es una cota con supuestos explícitos, no una proyección.
- **Titularidad y acceso.** Entre adultos de renta y edad iguales, la brecha de alquiler a precio de mercado entre nacionalidad extranjera y española es 41,8 puntos (40,0-43,8 puntos) [C4] (V12).

<!-- check:cifra-libre (años, edades 30 a 34, P90/P10 en el texto, versión V12) -->

### I.7 Parque, viviendas vacías y lanzamientos

**Parque (Censo 2021).** Viviendas familiares: 26.623.708 viviendas [C4]; principales 18.536.616 viviendas [C4]; no principales 8.087.092 viviendas [C4]. El Catastro y el Censo difieren en -5,2 % de diferencia [C4] en el territorio común. Se mantiene C4 porque no está demostrada la independencia entre ambos.

**Vacías y esporádicas.** Vacías por consumo eléctrico: 3.828.307 viviendas [C4], 14,4 % [C4] de las viviendas familiares. Uso esporádico: 2.517.628 viviendas [C4]. Las «vacías del Censo» y las «vacías por consumo» son la misma cifra: la tabla 59531 es del propio Censo, con el mismo universo. No son dos fuentes. Por municipio, el cociente P90/P10 de las vacías es 4,8 [C4]. <!-- check:cifra-libre (tabla 59531, P90/P10 en el texto) -->

**Viviendas turísticas [C2].** El aumento 2020-2024 equivale como máximo a 2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler) [C2], con el supuesto de sustitución uno a uno; en viviendas, 81.771 viviendas (81.771-81.771 viviendas) [C2]. Es una cota de cantidad, no de precio. <!-- check:cifra-libre (periodo, supuesto de sustitución uno a uno) -->

**Lanzamientos (CGPJ, fuente única).** 2013: 67.189 lanzamientos [C4]. Máximo, en 2014: 68.091 lanzamientos [C4]. 2025: 24.540 lanzamientos [C4]. Últimos cuatro trimestres: 18.731 lanzamientos [C4]. Por tipo en 2025: hipotecaria 17,7 % [C4]; arrendamientos (LAU) 74,6 % [C4]; otros 7,6 % [C4]. El total nacional es el de los tribunales superiores, no la suma de provincias. <!-- check:cifra-libre (periodos, cuatro trimestres) -->

**Comparación internacional (OCDE y Eurostat).** España no tiene segunda fuente independiente: todo es [C4]. La medida es la de los índices de la OCDE (precio real, precio/alquiler y precio/renta disponible), con su propio deflactor. No es el precio por m² de I.2 ni el IPV del INE, y no se asume que el deflactor sea el IPC general de I.2. Por eso la cifra de España puede diferir de las de I.2. Para 2019-2025, el precio real de la OCDE es 19,6 % y el IPV real del INE, 18,7 %. Se dan ambas.
- Precio real 2019-2025: España 19,6 %; mediana UE 15,6 %.
- Precio real 2007-2025: España -12,8 %; mediana UE 9,1 %.
- Precio/alquiler 2019-2025: España 31,5 %; mediana UE 16,2 %.
- Sobrecarga del coste de la vivienda 2025 (Eurostat, ECV): España 7,2 % de la población; UE 7,7 % de la población.

Vivienda pública por habitante frente a la UE: sin dato (la descarga de la OCDE, tabla PH4.2, está pendiente en docs/v16/tareas_autor.md). No se estima con otra fuente. <!-- check:cifra-libre (periodos, código de tabla) -->

### I.8 Qué deja esta parte sin resolver

- La medida de precio cambia la cuantía en varias ventanas. Ninguna cifra única resume «lo que ha subido el precio».
- En alquiler, solo Cataluña supera la vara de C1 en la brecha entre contratos nuevos y vigentes.
- El esfuerzo de acceso viene de una encuesta con intervalos aproximados; no hay dato por provincia.
- El déficit es una cota entre fuentes, no una estimación puntual.
- Nada de lo anterior contrasta una política ni un mecanismo. Los mecanismos están en la Parte II.

---

*Atribución (Open Database License).* Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. Las cifras construidas con esos datos se publican bajo la misma licencia.


## Parte II · Mecanismos

Esta parte responde a una pregunta: qué se asocia con el precio de compra y con el alquiler, qué sabemos de ello y qué no. Usa un marco teórico (cuatro cuadrantes), la descomposición «por qué ha subido» de la versión 8, la triangulación de V16 y las pistas de V15 y V16 que superan la revisión adversarial. No hay en ella ninguna conclusión sobre una medida concreta: eso va en la Parte III.

### II.1 Cómo leer esta parte

- **Capas.** Todo lo de V15 y V16 es [C4] (exploratorio o descriptivo). Lo de V8 es [C3s] cuando se dice, y está condicionado a las restricciones de signo que se declaran. Una coincidencia con la literatura no sube la capa.
- **Lenguaje.** Se escribe «se asocia», «coincide con» y «en la simulación». Nada de lo que sigue identifica un efecto.
- **Pre-registro.** Los resultados de V15 y V16 citados aquí tienen un pre-registro interno, sin sello de tiempo externo. V15: etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17. V16: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. No es un pre-registro depositado. <!-- check:cifra-libre (etiquetas, commit y fecha de pre-registro) -->
- **Evaluación sellada de V15.** Las hipótesis H1 a H5 de V15 tienen la evaluación sellada pendiente. El calendario está en `docs/v15/preregistro_v15_adenda.md`, sección C, con fecha límite 31-12-2027. Aquí son pistas pendientes, nunca confirmaciones. <!-- check:cifra-libre (números de hipótesis, sección y fecha límite del calendario) -->
- **Literatura.** Cada referencia lleva la etiqueta de su ficha: «DOI verificado; cuartil no verificado» (existe en Crossref o DataCite) o NO VERIFICADA (sin DOI localizado o de otra agencia). Casi todo se leyó en resumen o en versión de trabajo. Las magnitudes de la literatura no están en `cifras_clave`: por eso aquí se da el signo y se remite a la ficha. Las cifras que faltan se listan en III.11. <!-- check:cifra-libre (apartado III.11) -->

### II.2 El marco: cuatro cuadrantes (DiPasquale y Wheaton)

#### Qué es y qué no es

El modelo de stock y flujo de cuatro cuadrantes conecta cuatro relaciones:

1. el mercado del uso: la demanda de servicios de vivienda fija el alquiler para un stock dado;
2. el mercado de activos: el alquiler y la rentabilidad exigida fijan el precio;
3. la construcción: el precio frente al coste fija la obra nueva;
4. el stock: la obra nueva, menos las bajas, cambia el parque.

En V16 se calibra para España con rangos declarados y se simula cada shock con Monte Carlo sobre esos rangos (`output/v16/f3/cuatro_cuadrantes.md`, generado por `src/v16/f3_cuatro_cuadrantes.py`). Es un marco teórico calibrado, no una estimación. Dice qué respuesta cabe esperar si el mercado funcionara como el modelo. Capa [C4]. <!-- check:cifra-libre (cuatro cuadrantes: nombre del marco) -->

#### Parámetros: de dónde salen

| Parámetro | Origen | Estado |
|---|---|---|
| Elasticidad de la oferta nueva al precio | Literatura: una estimación por CCAA (Taltavull de la Paz, 2014, DOI verificado, leída en resumen) | Rango de la ficha L3 | <!-- check:cifra-libre (ficha L3) -->
| Elasticidad-precio de la demanda | Supuesto del autor; no hay estimación española leída | Rango amplio a propósito |
| Elasticidad-renta de la demanda | Supuesto del autor; hay una referencia española (Fernández-Kranz y Hon, 2006, DOI verificado) que no se usó para fijar el rango | Rango amplio a propósito |
| Rentabilidad inicial (inversa del cociente precio/alquiler) | `cifras_clave` | Ratio precio/alquiler 2023: 17,1-17,7 años de alquiler [C4] |
| Obra nueva sobre el parque cada año | Supuesto del autor; orden de magnitud de las terminadas | Terminadas por año 2019-2024, 52 provincias con País Vasco y Navarra, libres y protegidas (ámbito de E-T7-prod): 78.810-100.980 viviendas/año [C4]. En territorio común, sin País Vasco ni Navarra: 72.264-94.426 viviendas/año [C1] | <!-- check:cifra-libre (52 provincias: ámbito de E-T7-prod) -->
| Retardo entre inicio y fin de obra | `cifras_clave` | 3,0-3,2 años [C4]. Solo informativo: el estado estacionario no depende de él |

Tres de los cinco parámetros que mueven los multiplicadores son supuestos del autor. Los rangos son amplios a propósito. Un lector que cambie un supuesto cambia el multiplicador. Las dos series de terminadas tienen ámbitos distintos (con y sin País Vasco y Navarra, y con o sin protegidas): no se comparan entre sí ni se restan. <!-- check:cifra-libre (cinco parámetros y tres supuestos: diseño del marco) -->

#### Qué respuesta cabe esperar de cada shock

Los multiplicadores numéricos (mediana y banda entre los percentiles 5 y 95) están en `output/v16/f3/cuatro_cuadrantes.md` y no están en `cifras_clave`: se consultan allí; el informe no los cita porque no tienen id. Sin cifras, el patrón de signos es este: <!-- check:cifra-libre (percentiles 5 y 95: banda del Monte Carlo) -->

| Shock | A corto plazo (stock fijo) | A largo plazo (stock se ajusta) |
|---|---|---|
| Más demanda (renta u hogares) | Sube el alquiler y sube la obra nueva. El precio sube con el alquiler | Alquiler y precio suben menos; el stock crece |
| Más rentabilidad exigida al comprador (coste de uso: tipo, fiscalidad, revalorización esperada) | Baja el precio y baja la obra nueva. El alquiler no cambia | El precio baja menos; el stock es menor y el alquiler sube |
| Más coste de construcción | Sin efecto inmediato | Suben precio y alquiler; el stock es menor |
| Oferta menos elástica y más demanda | — | El precio sube más y el stock crece menos |

Tres lecturas, todas dentro del marco:

- **El stock tarda décadas en ajustarse.** La semivida del ajuste del stock sale de varias décadas con los rangos declarados, porque la obra nueva anual es una fracción pequeña del parque. A corto plazo el ajuste recae en el precio y el alquiler. El valor de la semivida está en output/v16/f3/cuatro_cuadrantes.md y no se cita aquí, porque no tiene id en cifras_clave.
- **Los shocks de tipos y de demanda tienen firmas distintas.** Un shock solo de tipos baja precio y obra nueva y deja el alquiler. Un shock solo de demanda sube alquiler, obra nueva y precio.
- **El «tipo exigido» no es el tipo hipotecario.** Es la rentabilidad que pide el comprador. Una subida del hipotecario no se traslada uno a uno.

#### ¿Lo muestran los datos? Episodio de subida de tipos

Comparación descriptiva de las medias de 2024 frente a las de 2022. Es una lectura de signos, no un contraste.

| Serie | Signo observado | Signo si solo cambiaran los tipos |
|---|---|---|
| Tipo hipotecario | + | + |
| Precio de compra (IPV) | + | − |
| Alquiler (IPC) | + | 0 o + |
| Compraventas | − | − |
| Visados de obra nueva | + | − |
| Renta real de los hogares | + | 0 |
| Hogares (EPA) | + | 0 |

Los valores de la variación de cada serie están en `output/v16/f3/cuatro_cuadrantes.md`: se consultan allí; no tienen id en cifras_clave. <!-- check:cifra-libre (años de la comparación) -->

El patrón de un shock solo de tipos no aparece: precio, alquiler y obra nueva suben. El marco es compatible con un shock de demanda simultáneo (hogares, renta) que compense la subida de tipos. Con estos datos no se pueden separar los dos shocks. El intento de separarlos (Q5, sorpresas de política monetaria) no dio señal estable: la primera etapa tiene el signo contrario al esperado y el placebo es comparable a la respuesta. Q5 queda «no concluyente» y no se cita con cifras. <!-- check:cifra-libre (identificador de pregunta) -->

#### Dónde falla el marco

- No hay elasticidad municipal de la oferta identificada para España. Q4 (restricción física, Red Natura) no produjo ningún hallazgo: la inferencia con agrupación provincial no es apta y el placebo de choque adelantado es del mismo signo y de mayor tamaño que la estimación. Queda «sin hallazgo». <!-- check:cifra-libre (identificador de pregunta) -->
- Los parámetros españoles de la demanda quedan como supuestos.
- El marco es de equilibrio y de un solo mercado. No modela la segmentación entre contratos nuevos y vigentes, ni el alquiler de temporada, ni los cambios de uso.

### II.3 La descomposición «por qué ha subido» de V8

#### Qué hizo V8

V8 descompuso la variación del precio real de compra y del alquiler real en cinco periodos, con un SVAR con restricciones de signo y de cero (M2), y contrastó cada factor con una regla fijada de antemano (la regla del apartado 9: coincidencia entre métodos, bandas y falsación). Los factores son demografía, empleo y renta, crédito y tipos, oferta, demanda externa y turismo. Todo se condiciona a esas restricciones. <!-- check:cifra-libre (cinco periodos P1 a P5 y apartado 9: diseño de V8) -->

#### Resultado: ningún factor designado

- **Ningún factor queda designado.** La regla del apartado 9 no designa a ningún factor en ninguno de los periodos, ni en compra ni en alquiler. En el último periodo (P5, desde 2022T3) la regla da 0,00 en compra y 0,00 en alquiler (1 = designado, 0 = no designado) [C4]. <!-- check:cifra-libre (P5 es el nombre del periodo; codificación 1 y 0) -->
- **La contribución de cada factor tiene una banda que contiene el cero.** Ejemplos del último periodo, con el intervalo del 95 %: <!-- check:cifra-libre (nivel del intervalo) -->
  - demografía y alquiler real: 0,07 pp, intervalo -4,5 a 4,7 pp [C3s]; p ajustado por Holm 0,99 [C3s]. No respaldada;
  - crédito y tipos y precio real de compra: -0,47 pp, intervalo -15,4 a 27,4 pp [C3s]; p ajustado por Holm 0,99 [C3s]. No respaldada.

#### La parte no atribuida

La «cuota no atribuida» es la parte de la variación observada que el SVAR no asigna a ningún factor identificado: su componente determinista y lo no identificado. Para el precio real de compra en el último periodo:

- media posterior: 9,5 pp [C3s];
- mediana posterior: 3,4 pp [C3s];
- banda del 68 % exacta, calculada con los cuantiles de la suma: -7,8 a 16,4 pp [C3s]; <!-- check:cifra-libre (nivel de la banda) -->
- sensibilidad, con el tipo hipotecario del Banco de España en lugar del del BCE: media 20,7 pp [C3s].

La media está muy por encima de la mediana porque la cola derecha es pesada. Por eso se dan las dos y la banda. La sensibilidad al tipo hipotecario elegido es grande en la media y pequeña en la mediana: se reportan ambas. Esta cifra se corrigió en V16 (errata de la banda exacta, aplicada en ERRATA.md).

Como proporción de la variación observada, la parte no atribuida del precio de compra en el último periodo es 0,52 (-0,79 a 1,3) [C3s]. Para el alquiler real, en puntos, es -2,0 pp con banda -7,9 a 3,6 pp [C3s].

**Lectura.** La descomposición no permite decir qué factor ha pesado más en la subida. Una parte grande y de signo incierto queda sin atribuir, y ninguna contribución se separa de cero tras el control de múltiples contrastes. Esto no dice que los factores no importen: dice que esta descomposición, con estos datos, no los separa.

#### Lo que V16 añade: comovimiento y contabilidad (descriptivo)

V16 no repite la descomposición. Añade tres descripciones que ayudan a leerla [C4]:

- **Una parte grande del crecimiento del valor tasado es común a las provincias.** La cuota del primer factor común en la varianza del crecimiento interanual de 33 provincias es 71,4 % en 2007-2013, 52,9 % en 2014-2019 y 80,9 % en 2020-2026 [C4]. La correlación media de los residuos locales entre provincias de la misma comunidad es baja: 0,02 correlación [C4]. Con provincias en lugar de comunidades, la cuota común es menor que la de V8: diferencia media -7,7 pp [C4]. Esto describe el comovimiento. No dice qué lo mueve. <!-- check:cifra-libre (33 provincias, periodos) -->
- **Contabilidad del número de hogares, 2021-2025.** El cambio observado es 981.823 hogares [C4], con rango entre ECP y EPA 981.823-1.062.300 hogares [C4]. Según la descomposición de Shapley, el tamaño de la población aporta 670.187 hogares [C4], la estructura por edad 371.922 hogares [C4], el residuo de jefatura 20.478 hogares [C4] y la composición por nacionalidad -80.764 hogares [C4]. Es contabilidad, no una estimación de efectos. La diferencia entre ECP y EPA en el cambio de hogares es 8,2 % [C4]: se dan las dos fuentes. <!-- check:cifra-libre (periodo) -->
- **Obra frente a hogares.** Las viviendas libres terminadas en 2021-2025 por hogar nuevo son 0,42 viviendas por hogar [C4], con 411.900 viviendas terminadas en el periodo [C4]. Es un cociente de flujos. No dice cuánta vivienda falta: la necesidad de vivienda se trata en la Parte V. <!-- check:cifra-libre (periodo) -->

### II.4 Triangulación de V16

La fase 6 compara cada resultado con la literatura y con otros diseños del mismo proyecto (`output/v16/triangulacion/informe.md`). Reglas: se compara el signo y, solo si la unidad coincide, el orden de magnitud. No hay metaanálisis, porque ningún grupo de resultados reúne estudios suficientes con error estándar y la misma unidad (decisión K7). Los 88 grupos de la literatura se quedan en rangos sin agregar. Ningún resultado sube de capa por coincidir con la literatura. <!-- check:cifra-libre (88 grupos y decisión K7: diseño del metaanálisis) -->

#### Entre diseños del propio proyecto

| Pareja | Mismo signo |
|---|---|
| H1: Callaway-Sant'Anna y SDID (zonas tensionadas y renta de contratos nuevos, Cataluña) | Sí |
| H3 y Q2a (vivienda turística y alquiler, sección y provincia) | Sí |
| H3 y Q2c (vivienda turística y alquiler, sección y municipio) | No |
| H4 y Q3-c1 (inmigración y alquiler municipal; inmigración y valor tasado provincial) | Sí |
| H4 y Q3-b (inmigración y alquiler municipal; inmigración y alquiler por sección) | Sí |

Que dos diseños coincidan en el signo no los convierte en independientes: comparten datos, periodo y, a veces, el mismo shock de origen.

#### Frente a la literatura

| Resultado | Estado | Lectura frente a la literatura |
|---|---|---|
| H1 (zonas tensionadas, renta de contratos nuevos) | Pista, solo el signo [C4] | Mismo signo. Las unidades no son comparables: solo se compara el signo |
| H2 y Q1c (zonas tensionadas, contratos y compraventas) | Ruido previo; no se citan | Sin señal estable |
| H3 y Q2a (vivienda turística) | No concluyente [C4] | Mismo signo; unidades no comparables |
| Q2c (vivienda turística, IPVA municipal) | No se cita | Signo opuesto al de la literatura, sin inferencia válida; se lee como robustez nula de H3 |
| H4 y Q3-b (inmigración) | Correlaciones frágiles [C4] | Sin comparación numérica con la literatura leída |
| Q6-v (ITP y compraventas) | Descriptivo | Se aparta de la literatura: el placebo con el resultado retardado es de signo contrario y mayor que la estimación, y los cambios de tipo se concentran en la crisis. El diseño no separa el ITP del ciclo |
| Q6-p (ITP y valor tasado) | No concluyente [C4] | Mismo signo; unidades no comparables |
| Q5-p (sorpresas monetarias y valor tasado) | No se cita | Sin comparación |

#### Qué se cita y con qué límites

**H1 de V15: solo el signo.** La asociación de la zona tensionada con la renta media de los contratos nuevos en Cataluña es negativa en los dos diseños (Callaway-Sant'Anna y SDID). No se cita ninguna magnitud: el placebo temporal y las pretendencias fallan, y las cotas no la permiten. Además hay anticipación y reversión por la sentencia del Tribunal Constitucional, selección de municipios y paso de contratos a temporada. La evaluación sellada está pendiente. [C4]

**H5 de V15: la combinación no supera al AR(4).** La razón del error cuadrático medio de la combinación frente al AR(4), en el valor tasado a un trimestre, es 1,5 en la implementación pre-registrada [C4]. En la réplica ciega es 1,2. El rango entre implementaciones es 1,2-1,5 razón [C4]: en ambas la razón queda por encima de uno. El multiverso de 60 especificaciones, que mezcla medidas y horizontes, va de 0,97 razón a 5,4 razón [C4]; no es un rango entre implementaciones. Se dice «la combinación no supera al AR(4)». No se dice «el AR(4) es mejor». El contraste de Diebold-Mariano no se cita como prueba. La evaluación sellada está pendiente. <!-- check:cifra-libre (AR(4): nombre del modelo; 60 especificaciones: tamaño del multiverso) -->

**E3 de V15: correlación espacial descriptiva, no contagio.** El parámetro autorregresivo espacial ρ (contigüidad, variación de la renta de alquiler de 1.124 municipios en 2015-2024) es 0,39, con rango del multiverso de 0,24 ρ a 0,64 ρ [C4]. Puede reflejar una tendencia regional común. El intervalo no recoge la incertidumbre de especificación: se cita el rango del multiverso. <!-- check:cifra-libre (1.124 municipios y periodo: diseño de E3) -->

**H4 de V15 y Q3-b de V16: correlaciones frágiles.** Ambas son asociaciones entre la presencia de población extranjera y el alquiler. No se leen como el efecto de la inmigración.
- **H4.** La asociación (2SLS) entre población extranjera predicha y alquiler municipal es 0,30 % por p.p., con rango del multiverso -0,14 a 0,39 % por p.p. [C4]. El rango contiene el cero y el signo cambia al quitar los orígenes principales. Hay pocos orígenes efectivos: 5,5 choques efectivos [C4]. El 2SLS es varias veces el MCO. La mediana del multiverso es 0,08 % por p.p. [C4]. <!-- check:cifra-libre (2SLS: nombre del estimador) -->
- **Q3-b.** La asociación transversal del alquiler por sección con la cuota de extranjeros es 0,01 log por desviación típica, con rango del multiverso de 0,00 log por desviación típica a 0,01 log por desviación típica [C4]. El coeficiente de pretendencia (variación previa) es 0,01 [C4], más de la mitad del coeficiente principal. Puede haber reversión a la media o convergencia, y la exposición de 2022 cae dentro de la ventana del resultado. La mediana del multiverso es 0,01 [C4].
- **Literatura.** La literatura con DOI verificado sobre inmigración y vivienda no tiene un signo único. Mussa, Nwaogu y Pozo (2017) asocian más entradas con alquileres y precios más altos. El metaanálisis de Larkin et al. (2019) halla que la inmigración sube los precios en conjunto, más a escala provincial. Sá (2015) y Saiz y Wachter (2011) hallan, en cambio, precios más bajos o una apreciación más lenta. Para España, Torres-Téllez y Montero-Soler (2023) asocian la llegada de inmigrantes con alquileres más altos. Las cinco referencias tienen DOI verificado y cuartil no verificado (ficha P4 de V15). Miden en unidades distintas y con otras muestras: no se compara la magnitud. <!-- check:cifra-libre (ficha P4) -->

**H3, Q2a y Q6-p: no concluyentes.** No concluyente no es «nulo». H3 (vivienda turística y alquiler por sección) tiene un coeficiente principal que es el mínimo de su multiverso y no tiene error estándar válido. Q2a (provincial) depende de los controles. Q6-p (ITP y valor tasado) fue pista hasta su réplica ciega, que corrigió un error de diferencias entre años no consecutivos.

**Exuberancia de precios.** Se trata en la Parte VII, con sus advertencias.

### II.5 Qué se asocia con qué: síntesis por canal

Cada canal se juzga con lo que la evidencia permite. «Literatura» es la ficha con DOI verificado de V15 o V16; «nuestro dato» es lo de V15, V16 o la 1.0.

| Canal | Mecanismo | Literatura | Nuestro dato | Estado |
|---|---|---|---|---|
| Demanda: hogares y renta | Más hogares o más renta suben alquiler y precio a corto plazo | Marco de cuatro cuadrantes; Fernández-Kranz y Hon (2006, DOI verificado) sobre la elasticidad-renta | Contabilidad de hogares; V8 no designa ningún factor | Compatible, no separado |
| Demanda: inmigración | Más hogares en alquiler y compra | Signo no unívoco (Mussa et al., 2017; Larkin et al., 2019; Sá, 2015; Torres-Téllez y Montero-Soler, 2023, todas con DOI verificado) | H4 y Q3-b, correlaciones frágiles | Correlación frágil [C4] |
| Tipos de interés | Más tipo exigido, menos precio y menos obra | Marco de cuatro cuadrantes | V8 no designa crédito y tipos; Q5 no concluyente | No separado de la demanda |
| Oferta y suelo | Oferta rígida, más precio ante un shock de demanda | Saiz (2010); Hilber y Vermeulen (2016); Caldera Sánchez y Johansson (2013), todas con DOI verificado | Q4 sin hallazgo; elasticidad municipal sin identificar | No evaluable con los datos |
| Vivienda turística | Cambio de uso: menos oferta residencial, más alquiler | García-López et al. (2020, Barcelona); Barron et al. (2021), ambas con DOI verificado | H3 y Q2a no concluyentes; Q2c no se cita | No concluyente [C4] |
| Regulación del alquiler | Tope en el contrato regulado, posibles desbordamientos | Ver Parte III | H1: signo | Pista, solo el signo [C4] |
| Fiscalidad de la compra | Un impuesto sobre la transmisión cambia volumen y, en parte, precio | Best y Kleven (2018); Besley et al. (2014), ambas con DOI verificado | Q6-v descriptivo; Q6-p no concluyente | No evaluable |
| Compradores no residentes | Más demanda de compra | Badarinza y Ramadorai (2018); Cvijanović y Spaenjers (2021), ambas con DOI verificado | Q8 descriptivo | No evaluable |
| Fundamentales y burbuja | Precio frente a alquiler y renta | — | La exuberancia se trata en la Parte VII | Ver Parte VII |

### II.6 Qué no sabemos

- **Qué factor pesa más en la subida reciente.** V8 no designa ningún factor y deja una parte sin atribuir. V16 no mejora esa descomposición.
- **El tamaño de ningún efecto de una medida en España.** Todo lo de V15 y V16 es [C4]. Las pistas son signos.
- **Si el patrón de 2022-2024 viene de la demanda, de los tipos o de ambos.** Q5 no los separa.
- **La elasticidad de la oferta municipal.** No hay estimación identificada.
- **Cuánto del comovimiento de precios entre provincias es un factor común y cuánto es una tendencia compartida.** El análisis de factores describe, no identifica.
- **Qué parte del cambio de hogares es formación y qué parte es cambio de jefatura.** La contabilidad da un residuo con rango.

Todo esto se actualiza cuando llegue la evaluación sellada de V15 (calendario en `docs/v15/preregistro_v15_adenda.md`, sección C). Hasta entonces, las hipótesis de V15 están pendientes. <!-- check:cifra-libre (sección C del calendario) -->

---

*Atribución (Open Database License).* Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. Las cifras construidas con esos datos se publican bajo la misma licencia.


## Parte III · Catálogo de medidas

Esta parte evalúa afirmaciones sobre ocho instrumentos de política de vivienda. No evalúa a quien los propone ni a quien los aplica. Cada ficha tiene siete apartados: mecanismo, evidencia internacional, evidencia española, nuestra estimación, coste, efectos secundarios y veredicto. <!-- check:cifra-libre (ocho instrumentos y siete apartados: estructura del catálogo) -->

### III.1 Cómo leer el catálogo

- **Qué se evalúa.** Una afirmación del tipo «el instrumento X baja el alquiler (o el precio)». Cada afirmación se formula según el **objetivo declarado** del instrumento, que se nombra en cada ficha. Una ayuda a la demanda, por ejemplo, tiene como objetivo la asequibilidad del beneficiario; su traslación al precio o a la renta se evalúa por separado.
- **Regla de umbral (la misma para todas las fichas).** El veredicto depende de tres cosas: cuántos estudios con diseño hay para ese resultado y ese objetivo, si coinciden en el signo y si se leyeron completos. Los estudios con diseño son los que usan un grupo de control, una discontinuidad, un instrumento u otro diseño que se declare. Los descriptivos no cuentan.
- **Escala de veredicto.**
  - **Eficacia probada.** Al menos dos estudios con diseño, leídos completos, con referencia de DOI verificado, que coinciden en el signo para el mismo resultado. Se dice siempre para qué resultado y en qué país.
  - **Prometedora.** Hay al menos un estudio con diseño en el sentido del objetivo, pero se leyó en resumen, o son pocos, o son de otro contexto, o discrepan en parte. Si hay dos estudios con diseño que coinciden pero no se leyeron completos, es «prometedora», no «eficacia probada».
  - **Sin evidencia.** No hay estudio con diseño que permita decir que funciona, o los estudios con diseño discrepan en el signo.
  - **Evidencia en contra.** Al menos dos estudios con diseño, leídos completos, en sentido contrario al objetivo declarado.
  - **No evaluable con los datos disponibles.** Ni la literatura ni nuestros datos permiten juzgar el instrumento en España.
- **Resultado de aplicar la regla.** Casi toda la literatura de `docs/v16/literatura/` se leyó en resumen o en versión de trabajo. Por eso ninguna ficha llega a «eficacia probada» ni a «evidencia en contra». Cuando los estudios con diseño coinciden, el veredicto es «prometedora» y la ficha lo dice.
- **Regla de capa.** Todas nuestras estimaciones (V15, V16 y los escenarios de la 1.0) son [C4]. Ningún veredicto de este catálogo se apoya en una estimación propia de capa superior a [C4]. Los veredictos que no son «no evaluable» vienen de la literatura con DOI verificado, de otros países o periodos, y no de una estimación nuestra sobre España.
- **Literatura.** Solo entran las referencias de `docs/v16/literatura/` y `docs/v15/literatura/`, con la etiqueta de su ficha: «DOI verificado; cuartil no verificado» (existe en Crossref o DataCite) o NO VERIFICADA (sin DOI localizado). Las magnitudes de los autores no están en `cifras_clave`, así que aquí se da el signo y la ficha donde está la cifra.
- **Pre-registro.** Los resultados de V15 y V16 que se citan tienen un pre-registro interno, sin sello de tiempo externo. V15: etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17. V16: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. No son pre-registros depositados. <!-- check:cifra-libre (etiquetas, commit y fecha de pre-registro) -->
- **Evaluación sellada.** Las hipótesis de V15 (H1 a H5) tienen la evaluación sellada pendiente (calendario en `docs/v15/preregistro_v15_adenda.md`, sección C; fecha límite 31-12-2027). `evaluate_v16` no aplica: ninguna pregunta de V16 cumple las condiciones para una evaluación sellada confirmatoria, así que V16 no tiene evaluación sellada pendiente. <!-- check:cifra-libre (números de hipótesis, sección y fecha) -->
- **Qué se cita de V15 y V16.** Solo lo que superó la revisión adversarial. H1: solo el signo. H2, Q1c, Q1b, Q6-v y Q2c no se citan con cifras. H3, Q2a y Q6-p son «no concluyentes». <!-- check:cifra-libre (identificadores de hipótesis) -->
- **Costes.** Cuando existe, el coste sale de los escenarios de la versión 7.1 (`V71-S1-*`): una simulación sobre un panel de 17 comunidades a diez años, con rangos entre comunidades. Es [C4]. No es un presupuesto. <!-- check:cifra-libre (versión 7.1, 17 comunidades y diez años: diseño de V71-S1) -->

### III.2 Zonas tensionadas y topes al alquiler

**Objetivo declarado:** contener la subida de la renta de los inquilinos en zonas con tensión de precios.

#### Mecanismo

- **Teoría.** Un precio máximo por debajo del de equilibrio crea exceso de demanda. La oferta de alquiler puede retirarse (venta, otros usos), bajar la calidad y reducir la movilidad. Con un segmento regulado y otro libre, la renta libre puede subir (desbordamiento). Fuente: ficha L1, apartado 1. <!-- check:cifra-libre (ficha L1 y apartado 1) -->
- **Generaciones.** La congelación de rentas es la primera generación. Los topes que limitan la subida entre contratos y dentro de ellos, con exenciones para obra nueva, son la segunda. La Ley 12/2023 combina un tope de actualización con zonas declaradas tensionadas y con exención de obra nueva durante un periodo. <!-- check:cifra-libre (Ley 12/2023) -->
- **Vías de salida.** La ficha L1 y el Banco de España (Documento Ocasional 2432, DOI verificado) describen el paso a alquiler de temporada y de habitaciones, con marco regulatorio más laxo. <!-- check:cifra-libre (Documento Ocasional 2432) -->

#### Evidencia internacional

- **Renta del contrato regulado.** Los estudios de segunda generación con grupo de control hallan rentas más bajas en los contratos regulados. Entre ellos: Breidenbach, Eilers y Fries (2022, Alemania, DOI verificado), con un efecto que se atenúa al cabo de un tiempo; Breuillé et al. (2025, París, NO VERIFICADA), con un efecto creciente. En la congelación de Berlín, Hahn, Kholodilin, Waltl y Fongoni (2024, DOI verificado), la caída es mayor.
- **Desbordamiento a la renta libre.** Mense, Michelsen y Kholodilin (2023, DOI verificado) hallan rentas libres al alza en Alemania. Jofre-Monseny et al. (2023, DOI verificado) hallan en Cataluña, en cambio, una caída menor en municipios vecinos no regulados. Los estudios con diseño discrepan en el signo del desbordamiento: se estima, no se supone.
- **Tercera generación, San Francisco.** Diamond, McQuade y Qian (2019, DOI verificado): baja la oferta de alquiler de los propietarios afectados y sube la renta de la ciudad.
- **Valor del inmueble.** Autor, Palmer y Pathak (2014, DOI verificado): el fin de un control estricto sube el valor, también el de viviendas nunca controladas. Ahern y Giacoletti (2022, DOI verificado, documento NBER): el tope baja el valor de venta.
- **Construcción.** Kholodilin y Voigtländer (2026, NO VERIFICADA, documento de trabajo): menos terminaciones tras el freno alemán, con pretendencias significativas en uno de los estimadores. Mense et al. (2019, DOI verificado) hallan, en cambio, más valor del suelo edificable exento. Los resultados sobre obra nueva no coinciden.
- **Revisión.** Kholodilin (2024, DOI verificado) cuenta el signo de los estudios publicados. La mayoría halla rentas controladas más bajas. La mayoría halla también peor calidad, menos movilidad y rentas no controladas más altas. Es un recuento de signos, no de tamaños, y mezcla generaciones y calidad de diseño.

#### Evidencia española

- **Ley 11/2020 de Cataluña (2020-2022).** Monràs y García-Montalvo (2023, DOI verificado) y Jofre-Monseny et al. (2023, DOI verificado), ambos con microdatos de contratos, coinciden en una renta más baja en los contratos regulados. Discrepan en la cantidad de contratos. Kholodilin, López, Rey Blanco y González Arbués (2022, DOI verificado) estudian la norma anulada. Abel, Carrer y Luque (2024, NO VERIFICADA) la estudian con anuncios. <!-- check:cifra-libre (Ley 11/2020) -->
- **Zonas de la Ley 12/2023.** Hay trabajos sobre 2024 (Pérez García, 2026, DOI verificado en DataCite, preprint; Pinto, 2026, NO VERIFICADA). Sus resultados constan en la ficha P6 de V15 y no se resumen aquí. <!-- check:cifra-libre (Ley 12/2023, ficha P6) -->
- **Banco de España.** El Documento Ocasional 2432 (DOI verificado) es descriptivo, sin identificación: documenta el paso a temporada y a habitaciones y no estima el efecto de la regulación. <!-- check:cifra-libre (Documento Ocasional 2432) -->
- **Lagunas.** No hay evaluación con identificación de la Ley 12/2023 ni medida del desplazamiento a temporada con contratos. <!-- check:cifra-libre (Ley 12/2023) -->

#### Nuestra estimación

- **H1 (V15): solo el signo.** La asociación de la zona tensionada con la renta media de los contratos nuevos, en municipios de Cataluña, es negativa con Callaway-Sant'Anna y con SDID [C4]. No se cita ninguna magnitud: el placebo temporal y las pretendencias fallan, y las cotas no la permiten. Hay anticipación por la Ley 12/2023, reversión tras la sentencia del Tribunal Constitucional sobre la norma catalana, selección de municipios y paso a contratos de temporada. La evaluación sellada está pendiente. <!-- check:cifra-libre (Ley 12/2023) -->
- **H2 (V15) y Q1c (V16).** El número de contratos y las compraventas provinciales no tienen señal que se distinga del ruido previo. No se citan con cifras.
- **Q1a y Q1b (V16): descriptivo, sin cifras.** La declaración de zona no es determinista con el criterio de precio del artículo 18, lo que limita una discontinuidad nítida en el umbral. Q1a no tiene resultado en el entrenamiento. Fuera de Cataluña, el primer inicio de zona vigente es posterior al último año de datos de alquiler del entrenamiento, y Q1b queda sin periodo posterior. Por eso Q1a y Q1b no se citan con cifras. V16 no tiene evaluación sellada para Q1b (véase III.1). <!-- check:cifra-libre (artículo 18, apartado III.1) -->
- **Ley 11/2020 en V9 (C4).** La diferencia (ATT, Callaway-Sant'Anna) en la renta media de los contratos nuevos en Cataluña es -5,9 %, con intervalo -7,3 a -4,4 % [C4]. No supera la robustez, así que no sostiene ningún veredicto de este catálogo. <!-- check:cifra-libre (Ley 11/2020) -->
- **Triangulación.** El signo de H1 coincide con el de la literatura leída. Las unidades no son comparables. Ningún resultado sube de capa por eso.

#### Coste

No hay cifra de coste fiscal en `V71-S1-*` para este instrumento. Sin dato de coste en el repositorio.

#### Efectos secundarios

- Posible paso a alquiler de temporada o de habitaciones, y a venta. La literatura lo documenta con anuncios; ningún estudio leído lo mide con contratos.
- Posible reducción de la cantidad de contratos o de anuncios. Los estudios con microdatos del mismo territorio discrepan.
- Calidad, movilidad y construcción: signos en su mayoría negativos en la literatura, con las salvedades de arriba.
- Desbordamiento a la renta libre y a municipios vecinos, de signo incierto.

#### Veredicto

| Afirmación | Veredicto | Base |
|---|---|---|
| Un tope de segunda generación baja la renta del contrato regulado | **Prometedora** (solo literatura con DOI verificado; Cataluña 2020-2022, Alemania; no es una estimación nuestra) | Varios estudios con grupo de control y microdatos coinciden en el signo, pero se leyeron en resumen |
| Un tope baja la renta del conjunto del mercado | **Sin evidencia** | Los estudios con diseño discrepan en el signo del desbordamiento a la renta libre |
| Un tope mantiene la cantidad de contratos y la oferta | **Sin evidencia** | Los estudios con microdatos del mismo territorio discrepan |
| Las zonas de la Ley 12/2023 bajan el alquiler en España | **No evaluable con los datos disponibles** | Sin periodo posterior en el entrenamiento fuera de Cataluña; H1 solo en el signo, con pruebas fallidas, en [C4] | <!-- check:cifra-libre (Ley 12/2023) -->

### III.3 Bono Alquiler Joven

**Objetivo declarado:** reducir el coste del alquiler del joven que recibe la ayuda.

#### Mecanismo

Una ayuda directa al pago del alquiler reduce el coste neto del inquilino que la recibe. Si la oferta de alquiler es rígida, parte de la ayuda puede trasladarse a la renta. El tamaño depende de la elasticidad de la oferta y de que la ayuda alcance a una parte pequeña o grande del mercado.

#### Evidencia internacional

La traslación de las ayudas al alquiler en las fichas con DOI verificado de L5 (Susin, 2002; Collinson y Ganong, 2018; Eriksen y Ross, 2015; Viren, 2013; Hyslop y Rea, 2019; Eerola et al., 2026) va de parcial a muy alta según el diseño y el mercado. La dispersión es grande. La ficha L5 da las cifras de los autores. No hay un resultado único que sirva para predecir España.

#### Evidencia española

No hay evaluación del Bono Alquiler Joven ni de sus convocatorias autonómicas (ficha L5). La base de intervenciones recoge solo la norma estatal; faltan las convocatorias autonómicas y la vigencia posterior a 2025 (`docs/v16/fuentes/intervenciones.md`).

#### Nuestra estimación

- **Q7a (V16): descriptivo, sin separación entre señal y ruido.** Se compara el alquiler de los inquilinos de mercado a uno y otro lado del corte de edad del bono, antes y después de su entrada en vigor, con la ECV. La diferencia en discontinuidades del logaritmo del alquiler es -0,12 Δlog [C4]. Los umbrales placebo de edad dan diferencias del mismo orden: -0,14 a -0,05 Δlog [C4]. No se muestra ningún intervalo.
- **Lo que mide.** El Plan Estatal 2018-2021 ya tenía un programa para menores de 35 años. La diferencia mide un cambio de generosidad entre ese plan y el bono, no un programa nuevo. El corte legal difiere en un año del de la ECV. La potencia está en el límite. <!-- check:cifra-libre (edad de corte, plan 2018-2021) -->
- **Conclusión.** No se cita ninguna magnitud como efecto del bono. V16 no tiene evaluación sellada para Q7a (véase III.1). <!-- check:cifra-libre (apartado III.1) -->

#### Coste

Sin dato de coste en el repositorio. En `V71-S1-e` se simula el coste de una ayuda a la demanda en compra, no en alquiler (véase III.8). <!-- check:cifra-libre (apartado III.8) -->

#### Efectos secundarios

Traslación a la renta en mercados de oferta rígida (literatura). Efectos de umbral: una edad de corte puede crear incentivos a posponer o adelantar la solicitud. Ningún estudio español los mide.

#### Veredicto

**No evaluable con los datos disponibles.** La literatura internacional apunta a una traslación al alquiler de tamaño muy variable. En España no hay evaluación, y nuestro diseño descriptivo no distingue señal de ruido.

### III.4 Impuesto de transmisiones patrimoniales (ITP)

**Objetivo declarado:** abaratar el acceso a la compra (menor coste de transacción).

#### Mecanismo

Un impuesto sobre la transmisión es un coste de transacción. Si baja, se espera más compraventa y menos inmovilidad de los hogares. La incidencia entre comprador y vendedor depende de las elasticidades de oferta y demanda. En mercados con oferta rígida, parte de la bajada puede capitalizarse en el precio.

#### Evidencia internacional

Las fichas con DOI verificado de L4 coinciden en que el volumen de transacciones responde al impuesto: baja tras las subidas permanentes, se adelanta antes de las subidas y sube con las rebajas temporales (Besley, Meads y Surico, 2014, Reino Unido; Best y Kleven, 2018; Dachis, Duranton y Turner, 2012, Toronto; Fritzsche y Vandrei, 2019, Alemania; Dolls et al., 2025). La incidencia en el precio recae sobre todo en el vendedor en varios de ellos. Hilber y Lyytikäinen (2017, DOI verificado) estudian la movilidad de los hogares. Las cifras están en la ficha L4.

#### Evidencia española

No hay estudio con identificación del ITP, de las rebajas autonómicas, del adelanto de 2012 ni del IVA superreducido (ficha L4). Mora-Sanguinetti y Rubio (2014, DOI verificado) evalúan reformas con un modelo DSGE; Montalvo, Piolatto y Raya (2020, DOI verificado) tratan la evasión en transacciones. Ninguno estima el efecto de un cambio autonómico del tipo.

#### Nuestra estimación

- **Q6 (V16).** El calendario de entrenamiento tiene 14,0 cambios del tipo general del ITP, que se concentran en 2012-2013, en plena crisis. El diseño no separa el ITP del ciclo. <!-- check:cifra-libre (años 2012-2013) -->
- **Q6-v (compraventas): descriptivo.** El placebo con el resultado retardado un año es de signo contrario y mayor que la estimación. No se cita ninguna cifra.
- **Q6-p (valor tasado): no concluyente.** Fue pista hasta su réplica ciega, que corrigió un error de diferencias entre años no consecutivos.
- **Escenarios de la 1.0.** Véase «Coste»: en la simulación, la rebaja del ITP y del IVA de vivienda nueva da el mismo valor de efecto sobre el precio de mercado que las ayudas a la demanda (III.8). <!-- check:cifra-libre (apartado III.8) -->

#### Coste

Coste fiscal anual aproximado de una rebaja de ITP e IVA en vivienda nueva, en la simulación: 93,3 M€/año, con rango entre comunidades 17,2-717,7 M€/año [C4]. Coste anual por punto de reducción del precio neto pagado: 82,4 M€/año por punto, rango 12,9-549,5 M€/año por punto [C4]. En la misma simulación, el precio de mercado sube en 1,4 puntos % por cada 100 M€ anuales, rango 0,16-7,6 puntos % [C4]. Es una simulación, no una estimación del ITP. <!-- check:cifra-libre (100 M€: unidad de la cifra de cifras_clave) -->

#### Efectos secundarios

Menos recaudación autonómica. Competencia fiscal entre comunidades. Mayor movilidad de los hogares si el impuesto baja. Transmisiones en fraude (ficha L4).

#### Veredicto

**No evaluable con los datos disponibles** para España. La literatura con DOI verificado, leída en resumen, indica que el volumen responde al impuesto; no establece para España que una rebaja mejore la asequibilidad, y la incidencia en el precio queda abierta. Nuestro diseño no separa el ITP del ciclo.

### III.5 Regulación de la vivienda turística

**Objetivo declarado:** devolver vivienda al mercado residencial y contener el alquiler residencial.

#### Mecanismo

Una vivienda dedicada a estancias cortas sale del mercado residencial o no entra en él. Con demanda residencial dada, menos oferta residencial tiende a subir el alquiler. Una norma que limite la vivienda turística puede devolver vivienda al mercado residencial, o no, si la vivienda pasa a otro uso (temporada, venta, vacía) o si el cumplimiento es bajo.

#### Evidencia internacional

Las fichas con DOI verificado de L2 y P5 (entre ellas Barron, Kung y Proserpio, 2021; Robertson, Dejean y Suire, 2023, Burdeos; Chaves Fonseca, 2024, Santa Mónica; Wachsmuth y St-Hilaire, 2026) coinciden en el signo: el aumento de oferta de alquiler de corta duración se asocia con rentas residenciales más altas, y las normas reducen sobre todo los anuncios. El efecto sobre el alquiler residencial es pequeño según los autores, con algún caso nulo. En precios de compra, el signo es negativo en las normas estudiadas. Las cifras están en las fichas L2 y P5. La elasticidad del alquiler a la densidad turística, en las fichas, es de un orden de magnitud pequeño. <!-- check:cifra-libre (fichas L2 y P5) -->

#### Evidencia española

- García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020, Barcelona, DOI verificado): la actividad de Airbnb se asocia con rentas y precios de venta más altos en los barrios más expuestos.
- Benítez-Aurioles (2023) y Mozo Carollo et al. (2023) tienen DOI verificado. Casanova Ferrando (2019) y Pastor et al. (2022) son NO VERIFICADAS. Chaves Fonseca (2026, Madrid, SERIEs) tiene DOI verificado.
- Reina (2026, DOI verificado) estudia el PEUAT de Barcelona; su diseño y resultado constan en la ficha P5. <!-- check:cifra-libre (ficha P5) -->
- No hay evaluación con identificación localizada del Plan Especial de Hospedaje de Madrid, de Palma, de Baleares, de Canarias ni de la moratoria de València (ficha L2). <!-- check:cifra-libre (ficha L2) -->

#### Nuestra estimación

- **H3 (V15), Q2a (V16): no concluyentes.** La asociación entre la densidad de vivienda turística y el alquiler tiene signo positivo en los dos diseños (sección censal y provincia) [C4]. El coeficiente principal de H3 es el mínimo de su multiverso y no tiene error estándar válido. El efecto mínimo detectable de H3, 0,10 % por desviación típica [C4], es mayor que el coeficiente principal, 0,00 % por desviación típica [C4]. No concluyente no significa nulo: el diseño no distingue entre efecto pequeño y ausencia de efecto. Q2a depende de los controles y de la fecha de la exposición. Las escalas «por desviación típica» no son comparables entre diseños.
- **Q2c (V16).** No se cita: tiene signo inestable.
- **Atlas.** La vivienda turística (INE, medición experimental) se concentra: el cociente entre el percentil 90 y el 10 de su peso municipal es 23,6 cociente P90/P10 (min y max en la unidad del indicador: % de las viviendas) [C4], con dato en una parte de los municipios (el resto, suprimidos). La media nacional esconde la concentración. <!-- check:cifra-libre (percentiles 90 y 10: definición del cociente) -->
- **Triangulación.** H3 y Q2a coinciden en el signo; H3 y Q2c no. Con la literatura: mismo signo, unidades no comparables. H3 (V15) está pendiente de su evaluación sellada; Q2a (V16) no tiene evaluación sellada.

#### Coste

En los escenarios de la 1.0, una regulación local de pisos turísticos se simula como un cambio de oferta residencial. No hay coste fiscal. Sin dato de coste de inspección en el repositorio.

#### Efectos secundarios

Paso a otros usos (temporada, venta, vacía). Pérdida de ingresos de propietarios y de actividad turística local. Caída del valor de los inmuebles con licencia (la literatura internacional lo recoge). Cumplimiento: las normas necesitan registro y control.

#### Veredicto

**Prometedora** en la literatura internacional: las normas reducen los anuncios y el alquiler residencial baja algo (estudios con diseño leídos en resumen). **No evaluable con los datos disponibles** en España: nuestros resultados son no concluyentes y sin identificación, y no hay evaluación con identificación de las normas españolas. Nada permite hoy decir cuánto alquiler se evita.

### III.6 Movilización de vivienda vacía

**Objetivo declarado:** que la vivienda vacía pase a alquiler o venta y aumente la oferta efectiva.

#### Mecanismo

Un impuesto o recargo sobre la vivienda vacía eleva el coste de mantenerla sin uso. Si la vivienda vacía pasa a alquiler o venta, la oferta efectiva aumenta. Hay vacancia friccional (cambio de inquilino, obra, herencia) que ningún impuesto elimina, y la vivienda vacía puede estar donde no hay demanda.

#### Evidencia internacional

Segú (2020, Francia, DOI verificado): la vacancia baja con el impuesto, también en relativo. Caracciolo y Miglino (2024), Han, Stacey y Chen (2023) y el informe de BCREA (2020) estudian el impuesto de Columbia Británica; las tres fichas son NO VERIFICADAS, y la última procede de una asociación del sector. La cifra de Segú está en la ficha L7. <!-- check:cifra-libre (ficha L7) -->

#### Evidencia española

No hay estudio con diseño sobre el recargo del IBI a la vivienda vacía (ficha L7). La base de intervenciones recoge solo el marco estatal (Ley 12/2023); no hay ordenanzas municipales verificadas (`docs/v16/fuentes/intervenciones.md`). <!-- check:cifra-libre (ficha L7, Ley 12/2023) -->

#### Nuestra estimación

- **Hecho de partida [C4].** El Censo 2021 cuenta 8.087.092 viviendas no principales (secundarias y vacías) [C4]. Por consumo eléctrico, hay 3.828.307 viviendas vacías, un 14,4 % de las viviendas familiares [C4]. Son medidas con definiciones distintas; no se suman ni se identifican con vivienda disponible.
- **Dispersión.** El cociente entre percentil 90 y percentil 10 del porcentaje municipal de viviendas vacías por consumo eléctrico es 4,8 cociente P90/P10 (min y max en la unidad del indicador: % de las viviendas) [C4]. La media nacional esconde que la vacancia se concentra en unos municipios. <!-- check:cifra-libre (percentiles 90 y 10: definición del cociente) -->
- **Escenario de la 1.0.** En la simulación de la versión 7.1, movilizar vivienda vacía se asocia con una variación del precio del alquiler de -1,7 puntos % por cada 10.000 viviendas en 10 años (mediana entre comunidades), con rango -6,8 a -0,31 puntos % [C4]. Es un escenario condicional sobre coeficientes de panel de la versión 7, no un resultado de V15 ni de V16. En compra, las cuatro actuaciones de oferta de la simulación (construcción, vacías, vivienda pública y turísticas) tienen el mismo valor: -0,61 puntos %, rango -2,4 a -0,11 puntos % [C4]. En la simulación, el precio de compra no distingue entre ellas. <!-- check:cifra-libre (versiones 7 y 7.1, 10.000 viviendas y 10 años: unidad y horizonte de la cifra de cifras_clave; cuatro actuaciones: diseño) -->
- Ninguna estimación de V15 ni de V16 cubre este instrumento.

#### Coste

Sin dato de coste en el repositorio.

#### Efectos secundarios

Recaudación adicional si el recargo se aplica. Traslado del uso de la vivienda a segunda residencia declarada o a alquiler de temporada. Costes de verificar la vacancia (el consumo eléctrico es una aproximación). Efecto desigual: la vacancia se concentra en pocos municipios.

#### Veredicto

**Prometedora** para reducir la vacancia (Segú, 2020, DOI verificado: un solo estudio con diseño, en un país). **Sin evidencia** de que reduzca el alquiler o el precio: no hay estudio con diseño sobre ese resultado, y el escenario de la 1.0 es una simulación de capa [C4]. En España, no evaluable con los datos disponibles.

### III.7 Oferta pública y suelo

La ficha agrupa dos instrumentos con mecanismos distintos: más oferta libre (suelo, urbanismo, obra nueva) y vivienda pública o asequible.

**Objetivo declarado:** aumentar la oferta para contener precios y rentas.

#### Mecanismo

- **Más oferta libre.** Con demanda dada, más vivienda reduce el precio y el alquiler relativos. El tamaño depende de la elasticidad de la oferta, que depende del suelo, el planeamiento y los costes. Las cadenas de mudanzas trasladan parte del efecto a hogares de renta baja.
- **Vivienda pública.** Añade viviendas a precio regulado. Una parte puede sustituir a vivienda privada que no se construye (desplazamiento), y el efecto en el vecindario puede cambiar de signo según su renta.

#### Evidencia internacional

- **Oferta libre.** Saiz (2010), Hilber y Vermeulen (2016) y Caldera Sánchez y Johansson (2013) tienen DOI verificado y asocian la restricción de oferta con precios más altos. Asquith, Mast y Reed (2023), Mast (2023) y Bratu, Harjunen y Saarimaa (2023) tienen DOI verificado y asocian la obra nueva con rentas cercanas más bajas y con cadenas de mudanzas que llegan a hogares de renta baja. Greenaway-McGrevy y Phillips (2023), Pennington (2021) y Li (2022) son NO VERIFICADAS. Las cifras de los autores están en la ficha L3. <!-- check:cifra-libre (ficha L3) -->
- **Vivienda pública.** Sinai y Waldfogel (2005), Eriksen y Rosenthal (2010), Baum-Snow y Marion (2009), Diamond y McQuade (2019) y Koster y van Ommeren (2019) tienen DOI verificado. Los estudios de EE. UU. sobre desplazamiento hallan que parte de la vivienda subsidiada sustituye a vivienda privada. El efecto en el precio del vecindario cambia de signo según la renta del barrio (ficha L7). <!-- check:cifra-libre (ficha L7) -->

#### Evidencia española

- La única elasticidad de la oferta nueva leída es por comunidad autónoma (Taltavull de la Paz, 2014, DOI verificado, leída en resumen). No hay elasticidad municipal identificada ni evaluación de la Ley del Suelo (ficha L3). Taltavull de la Paz (2015, DOI verificado) trata los factores institucionales; Arrazola et al. (2014) es NO VERIFICADA. <!-- check:cifra-libre (ficha L3) -->
- No hay estudio con diseño sobre la vivienda protegida. El parque social español es una fracción pequeña del total y su tamaño depende de la fuente (ficha L7). Rodríguez-Fernández (2026, Funcas) es NO VERIFICADA. <!-- check:cifra-libre (ficha L7) -->

#### Nuestra estimación

- **Q4 (V16): sin hallazgo.** La asociación de la obra nueva neta con el porcentaje de Red Natura municipal es -0,13 log por desviación típica [C4], pero la inferencia con agrupación provincial no es apta, los residuos tienen dependencia espacial y la Red Natura no es exógena (restricción de uso correlacionada con el medio rural). La interacción con el choque de demanda, Q4b, es -0,00 log por punto de choque y DT de RN [C4] y su placebo de choque adelantado tiene el mismo signo y mayor tamaño. No se concluye nada sobre la elasticidad municipal.
- **Producción de vivienda.** En 2025 se terminaron 80.792 viviendas libres [C4]. Entre 2021 y 2025 se terminaron 0,42 viviendas por hogar libres por hogar nuevo [C4]. Son flujos, no una medida de necesidad. <!-- check:cifra-libre (años) -->
- **Escenarios de la 1.0 (V7.1).** En la simulación, por cada 10.000 viviendas adicionales en 10 años: <!-- check:cifra-libre (versión 7.1, 10.000 viviendas y 10 años: unidad y horizonte de las cifras de cifras_clave) -->
  - construcción adicional: alquiler -0,70 puntos %, rango -2,7 a -0,12 puntos % [C4];
  - vivienda pública o asequible: alquiler -3,2 puntos %, rango -12,2 a -0,56 puntos % [C4];
  - en compra, el mismo valor para todas las actuaciones de oferta: -0,61 puntos %, rango -2,4 a -0,11 puntos % [C4].

  Los valores son variaciones del precio en puntos porcentuales, mediana entre comunidades. Es una simulación condicional sobre coeficientes de panel, no una estimación de V15 ni de V16. No se ha comprobado que la simulación recoja el desplazamiento de vivienda privada que documenta la literatura de EE. UU.

#### Coste

El escenario de la 1.0 no estima el coste de construir o de adquirir suelo. Sin dato de coste por vivienda en el repositorio.

#### Efectos secundarios

Desplazamiento de vivienda privada por la pública. Plazos largos (el retardo medio entre inicio y fin de obra es de 3,2 años [C4]). Presión sobre el medio natural y los servicios. Cambios de valor en el vecindario de una promoción.

#### Veredicto

- **Oferta libre (más suelo, más obra nueva):** **prometedora**. Las referencias con DOI verificado, leídas en resumen, asocian más oferta con rentas cercanas más bajas, y las restricciones de oferta con precios más altos. En España no hay estimación identificada de la elasticidad municipal, y Q4 queda sin hallazgo.
- **Vivienda pública o asequible:** **sin evidencia** en España; **no evaluable con los datos disponibles**. La literatura de EE. UU. documenta desplazamiento parcial, y el efecto en el precio depende de la renta del barrio.

### III.8 Ayudas a la demanda (compra y alquiler en general)

Incluye las ayudas a la compra (avales ICO, deducciones, planes estatales) y las ayudas al alquiler distintas del Bono Alquiler Joven, que tiene su ficha.

**Objetivo declarado:** la asequibilidad del beneficiario (poder pagar la compra o el alquiler). La traslación de la ayuda al precio o a la renta de mercado es un resultado distinto y se evalúa por separado.

#### Mecanismo

Una ayuda a la demanda aumenta la capacidad de pago. Si la oferta es rígida, el aumento de demanda sube el precio y la ayuda se capitaliza en parte en el precio o en la renta. Si la oferta responde, se construye más.

#### Evidencia internacional

Las fichas con DOI verificado de L5 (Carozzi, Hilber y Yu, 2024, Help to Buy; Berger, Turner y Zwick, 2020; Susin, 2002; Collinson y Ganong, 2018; Eriksen y Ross, 2015) apuntan a que la ayuda se capitaliza en el precio donde la oferta es rígida y, en alquiler, se traslada en parte a la renta. Krolage (2020, NO VERIFICADA) estudia la ayuda a la compra en Baviera. Las cifras están en la ficha L5. <!-- check:cifra-libre (ficha L5) -->

#### Evidencia española

No hay evaluación de los avales ICO ni de las ayudas del plan estatal (ficha L5). La base de intervenciones recoge solo el convenio de avales de 2024; las modificaciones posteriores no están comprobadas. <!-- check:cifra-libre (ficha L5) -->

#### Nuestra estimación

Ninguna estimación de V15 ni de V16 cubre este instrumento. Escenario de la 1.0, en la simulación:
- coste fiscal anual aproximado de una ayuda a la demanda en compra: 378,2 M€/año, rango entre comunidades 68,0-2.915 M€/año [C4];
- coste anual por punto de reducción del precio neto pagado por el comprador: 76,4 M€/año por punto, rango 12,2-515,9 M€/año por punto [C4];
- variación del precio de mercado por cada 100 M€ anuales: 1,4 puntos %, rango 0,16-7,6 puntos % [C4].

Es una simulación condicional sobre coeficientes de panel de la versión 7. <!-- check:cifra-libre (100 M€: unidad de la cifra de cifras_clave; versión 7) -->

#### Coste

Los tres valores anteriores. Son el coste de la simulación, no un presupuesto.

#### Efectos secundarios

Capitalización en el precio, con beneficio parcial para el vendedor. Mayor endeudamiento de los hogares beneficiarios. En el alquiler, traslado parcial a la renta. Una parte del beneficio llega a quien ya habría comprado o alquilado.

#### Veredicto

- **Asequibilidad del beneficiario (objetivo declarado):** **no evaluable con los datos disponibles** en España. No hay evaluación local, y nuestro escenario es una simulación [C4].
- **Traslación al precio o a la renta de mercado (resultado distinto):** las referencias con DOI verificado, leídas en resumen, describen capitalización parcial donde la oferta es rígida. Es una advertencia sobre el precio de mercado, no un veredicto sobre el instrumento. Con la regla de umbral no alcanza «evidencia en contra» (estudios no leídos completos). Eso no afirma que el comprador no se beneficie: afirma que parte de la ayuda llega al precio, según esos estudios y, en la simulación, según los coeficientes de panel.

### III.9 Compradores no residentes

**Objetivo declarado:** reducir la presión de la demanda de compra de no residentes sobre el precio local.

#### Mecanismo

Más demanda de compra de quien no vive en el mercado local sube el precio si la oferta es rígida. Un recargo o un límite a esa compra reduce la demanda de ese grupo. El efecto sobre el alquiler es indirecto: compra para alquilar, uso turístico o vivienda vacía.

#### Evidencia internacional

Badarinza y Ramadorai (2018, Londres), Cvijanović y Spaenjers (2021, París) y Gorback y Keys (2020, NBER) tienen DOI verificado y asocian más demanda extranjera con precios más altos. Pavlov, Somerville y Wetzel (2024) y Howell, Mughan y Singla (2024) tienen DOI verificado y estudian recargos a compradores extranjeros, con caídas de precio a corto plazo. Khan y Verstraete (2019, Banco de Canadá) tiene DOI verificado en DataCite. Sá (2016) y Pereira dos Santos y Strohmaier (2024, visados de oro) son NO VERIFICADAS. Las cifras están en la ficha L6. <!-- check:cifra-libre (ficha L6) -->

#### Evidencia española

Álvarez, Blanco y García-Posada (2020, Banco de España) es NO VERIFICADA. Lajer Baron et al. (2024, Documento Ocasional 2433) tiene DOI verificado. La ficha L6 recoge un estudio provincial sin resultado significativo y no localiza evaluación de la Ley 14/2013 ni de su supresión. <!-- check:cifra-libre (Documento Ocasional 2433, ficha L6, Ley 14/2013) -->

#### Nuestra estimación

- **Q8 (V16): descriptivo, sin estimador de efecto.** En el agregado de entrenamiento, la cuota de compras de no residentes sobre el total de transacciones es 7,4 % de las transacciones en 2025T2-2026T1 y 8,7 % de las transacciones en 2024T2-2025T1 [C4]. La variación entre ventanas es -1,3 puntos porcentuales (este año -1,3 puntos porcentuales; la misma comparación un año antes, -0,68 puntos porcentuales, del mismo signo) [C4]. La cuota ya bajaba antes de abril de 2025. En 2025 hubo 41.239 transacciones de no residentes, una cuota anual de 7,6 % de las transacciones [C4]. <!-- check:cifra-libre (periodos) -->
- **Qué no permite.** La fuente no distingue comunitarios de extracomunitarios y no trae las autorizaciones de residencia por inversión. La cuota total de no residentes no identifica los visados de oro. No hay lectura sobre el fin de ese régimen. V16 no tiene evaluación sellada para Q8 (véase III.1). <!-- check:cifra-libre (apartado III.1) -->

#### Coste

El instrumento no tiene coste fiscal directo; sí una posible variación de recaudación por transmisiones. Sin dato de recaudación en el repositorio.

#### Efectos secundarios

Menor entrada de capital. Efectos sobre el mercado turístico y de segunda residencia. Dificultad de aplicación por la libre circulación de capitales dentro de la Unión Europea.

#### Veredicto

**No evaluable con los datos disponibles.** En la literatura internacional, los recargos a compradores extranjeros se asocian con caídas de precio a corto plazo; para España no hay evaluación, y nuestros datos no distinguen el grupo afectado.

### III.10 Resumen del catálogo

| Instrumento | Veredicto | Nota |
|---|---|---|
| Zonas tensionadas y topes | Prometedora para la renta del contrato regulado (solo literatura); sin evidencia para la renta del conjunto del mercado y para la cantidad de contratos; no evaluable para la Ley 12/2023 | H1: solo el signo en [C4]; ATT de V9 sobre la Ley 11/2020 en [C4], no supera la robustez | <!-- check:cifra-libre (Ley 12/2023 y Ley 11/2020) -->
| Bono Alquiler Joven | No evaluable con los datos disponibles | Q7a descriptivo |
| ITP | No evaluable con los datos disponibles | Q6-v descriptivo; Q6-p no concluyente |
| Vivienda turística | Prometedora (literatura internacional); no evaluable en España | H3 y Q2a no concluyentes |
| Movilización de vacías | Prometedora para la vacancia; sin evidencia para alquiler y precio | Un solo estudio verificado |
| Oferta libre y suelo | Prometedora | Q4 sin hallazgo |
| Vivienda pública | Sin evidencia; no evaluable con los datos disponibles | Desplazamiento parcial en la literatura de EE. UU. |
| Ayudas a la demanda | Asequibilidad del beneficiario: no evaluable en España. Traslación al precio: capitalización parcial en la literatura (resumen) | Escenario de la 1.0 |
| Compradores no residentes | No evaluable con los datos disponibles | Q8 descriptivo |

#### Qué dice la regla de capa sobre esta tabla

- Con todas nuestras estimaciones en [C4], ninguna fila se apoya en un resultado propio de capa superior. Con la regla de umbral de III.1, ninguna fila alcanza «eficacia probada» ni «evidencia en contra». Las filas «prometedora» vienen de la literatura con DOI verificado, de otros países o periodos, y solo para el resultado que se indica. <!-- check:cifra-libre (apartado III.1) -->
- Para ningún instrumento hay una evaluación española con identificación y diseño creíble, salvo los topes de la Ley 11/2020 de Cataluña. La validez externa de la literatura depende de la elasticidad de la oferta y de la tenencia, que en España son distintas: mucha propiedad, poco parque social y una hipoteca mayoritariamente variable hasta 2022. <!-- check:cifra-libre (Ley 11/2020) -->
- La evaluación sellada de V15 puede cambiar las filas de la tabla. V16 no tiene evaluación sellada pendiente. Hasta entonces, las hipótesis de V15 están pendientes.

### III.11 Cifras pendientes

- Magnitudes de la literatura (rangos de renta, oferta, precio y traslación): no están en `cifras_clave`. Se remite a las fichas `docs/v16/literatura/L1` a `L7` y a `docs/v15/literatura/`. Las magnitudes se dan en esas fichas, no en este informe. <!-- check:cifra-libre (fichas L1 a L7) -->
- Costes de zonas tensionadas, Bono Alquiler Joven, vivienda vacía, oferta pública y no residentes: marcados en cada ficha.

### III.12 Instrumentos del plan no cubiertos y por qué

Estos instrumentos figuran en el plan de V16 (`docs/v16/plan.md`) y no tienen ficha propia. No se evalúan: el motivo se da en cada fila.

| Instrumento | Dónde queda | Por qué no tiene ficha |
|---|---|---|
| Tope del 2 % y del 3 % a la actualización de rentas vigentes | Se trata dentro de III.2 como parte de los topes | Ninguna pregunta de V15 o V16 lo toma como tratamiento; la ficha L1 recoge topes de actualización de otros países y no localiza una evaluación española del tope aplicado a contratos vigentes | <!-- check:cifra-libre (2 % y 3 %: topes del plan; apartado III.2; ficha L1) -->
| Suspensión de desahucios y lanzamientos | Sin ficha | La ficha L7 recoge moratorias de desahucios de otro país, con amenazas a la identificación declaradas por los autores; ninguna pregunta de V16 las toma como tratamiento | <!-- check:cifra-libre (ficha L7) -->
| Incentivos fiscales al alquiler | Sin ficha | No hay ficha de literatura ni pregunta de V15 o V16 sobre ellos |
| Planes estatales como tales | Sus programas entran en III.3 (Bono Alquiler Joven) y III.8 (ayudas a la demanda) | No hay evaluación del plan en conjunto; se evalúa cada programa por separado | <!-- check:cifra-libre (apartados III.3 y III.8) -->
| Avales ICO | III.8 (ayudas a la demanda) | Sin evaluación española localizada | <!-- check:cifra-libre (apartado III.8) -->
| Fin de la golden visa | III.9 (compradores no residentes) | La fuente de Q8 no trae las autorizaciones por inversión; no hay lectura sobre el fin del régimen | <!-- check:cifra-libre (apartado III.9) -->


## Parte IV · Territorios

Esta parte presenta el atlas multiescala y lo que sobrevive a escala local. Todo es [C4]: descriptivo o exploratorio. Las frases describen coincidencias territoriales y no atribuyen causas. Las tablas largas no se copian aquí: están en las fichas territoriales de la web y en las descargas del atlas (`territorios.csv` y `territorios.parquet`).

### IV.1 Qué es el atlas y qué cubre

**Escalas.** España, CCAA, provincia, partido judicial, municipio, distrito y sección censal. No hay área urbana funcional: no existe correspondencia en la base geográfica del repositorio.

**Tamaño.** El atlas tiene 1.586.227 filas en formato largo [C4]. Hay al menos un indicador publicado en 4.904 municipios y en 17.763 secciones censales [C4]. Hay alquiler SERPAVI publicable en 1.390 municipios [C4] (al menos 10 contratos y CV de 30 % o menos). <!-- check:cifra-libre (umbrales de supresión del diseño) -->

**Qué amplía.** El atlas de V10 (coste por grupo social, València, Comunitat Valenciana y provincias) sigue vigente y no se repite. V16 añade renta ADRH 2015-2023 completa, turismo, parque, lanzamientos e intervenciones. <!-- check:cifra-libre (periodo; versiones V10 y V16) -->

**Unidades en blanco por validación sellada.** Las unidades de la muestra sellada (v6, V15 y V16) están en blanco por validación, no por falta de dato. No figuran con valor en el fichero ni en los mapas. Las ocho CCAA de la decisión K8 (Aragón, Asturias, Baleares, Canarias, Madrid, Murcia, Navarra y La Rioja) aparecen solo a escala de CCAA y nación. Nunca como provincia ni por debajo. Por eso un indicador provincial o municipal es, en este atlas, el de las unidades no selladas. <!-- check:cifra-libre (ocho CCAA del diseño; versiones) -->

**Supresión.** Se deja en blanco toda celda con menos de 10 unidades de base o con CV superior a 30 %. Afecta al 4,5 % [C4] de las filas. Los valores sustitutos de provincia o comarca de la ADRH no se muestran como municipales. <!-- check:cifra-libre (umbrales de supresión) -->

**Incertidumbre.** Hay intervalo al 95 % solo donde hay error de estimación: alquiler SERPAVI municipal y provincial, esfuerzo que propaga ese intervalo, y sobreesfuerzo de la ECV por CCAA. Los registros administrativos (ADRH, padrón, Censo 2021, CGPJ) no llevan intervalo y sí una marca de calidad. <!-- check:cifra-libre (nivel de confianza; Censo 2021) -->

### IV.2 Heterogeneidad entre territorios

Una media nacional esconde la dispersión. La tabla da el cociente entre el percentil 90 y el percentil 10 (P90/P10) de cada magnitud entre las unidades no selladas. Un cociente de 1 significa que no hay dispersión; cuanto mayor, más dispersión. <!-- check:cifra-libre (percentiles 90 y 10 y cociente de referencia 1, definición) -->

| Magnitud | Escala | Periodo | Cociente P90/P10 |
|---|---|---|---|
| Renta neta media del hogar (ADRH) | municipio | 2023 | 1,8 |
| Renta mediana por unidad de consumo (ADRH) | sección | 2023 | 1,8 |
| Alquiler mediano €/m² y mes (SERPAVI) | municipio | 2024 | 2,5 |
| Ratio alquiler anual de 80 m² sobre renta del hogar | municipio | 2023 | 1,9 |
| Misma ratio | sección | 2023 | 2,5 |
| Valor tasado €/m² | provincia | 2026T2 | 2,7 |
| Sobreesfuerzo del 40 % (ECV) | CCAA | 2025 | 2,0 |
| Viviendas no principales, % (Censo 2021) | municipio | 2021 | 3,0 |
| Viviendas vacías por consumo eléctrico, % (Censo 2021) | municipio | 2021 | 4,8 |
| Viviendas turísticas, % de las viviendas (INE VTE) | municipio | 2026-05 | 23,6 |
| Población de nacionalidad extranjera, % (censo anual) | municipio | 2025 | 17,8 |
| Lanzamientos por 10.000 viviendas, suma 2013-2024 | partido judicial | 2013-2024 | 8,5 |

<!-- check:cifra-libre (80 m², 40 %, 10.000 viviendas, periodos y escalas en la tabla) -->

**Lectura.**
- La renta tiene un cociente menor que las magnitudes de turismo, de población extranjera y de lanzamientos.
- Las viviendas turísticas se miden solo en los municipios con dato del INE; la cifra no es comparable con las de cobertura completa.
- El cociente de la ratio de esfuerzo en secciones (2,5) supera al de municipios (1,9): dentro de un mismo municipio hay secciones más distintas entre sí que los municipios entre sí.
- Los mínimos y máximos de cada magnitud están en `output/v16/f2_atlas/hechos.json`.

### IV.3 Esfuerzo de alquiler por territorio

**Construcción.** La ratio es el alquiler anual de una vivienda tipo de 80 m² (mediana SERPAVI en €/m² y mes, tipología colectiva) sobre la renta neta media del hogar (ADRH), en el mismo año. Los 80 m² son un supuesto, no la superficie observada. SERPAVI mide contratos vigentes, no nuevos. La renta es la de todos los hogares de la unidad, no solo la de los inquilinos. **No es la tasa de sobreesfuerzo de la ECV** y no debe compararse con ella. <!-- check:cifra-libre (80 m²) -->

**Cobertura.** Hay ratio publicable en 10.773 secciones censales en 2023 [C4].

**Provincias (1.0, V10).** El alquiler anual de 80 m² sobre la renta neta por persona tiene mediana y rango provincial 42,3 % (28,6-66,9 %) [C4]. Es otra definición de renta (por persona, no por hogar): no se mezcla con la ratio de arriba. <!-- check:cifra-libre (80 m², versiones) -->

**Municipios de la Comunitat Valenciana con 20.000 habitantes o más (V10).** La variación del alquiler mediano 2019-2024 tiene mediana y rango 31,9 % (19,1-48,5 %) [C4]. <!-- check:cifra-libre (umbral de población del diseño, periodo, versión V10) -->

**Ciudades comparables (V10), variación del alquiler mediano 2019-2024.**
- València: 39,8 % [C4].
- Alicante/Alacant: 31,3 % [C4].
- Málaga: 31,4 % [C4].
- Palma: 24,6 % [C4].
- Sevilla: 21,4 % [C4].
- Zaragoza: 21,3 % [C4].

Son contratos vigentes (SERPAVI). <!-- check:cifra-libre (periodo, versión V10) -->

### IV.4 Presión residencial y composición: ejemplos locales

- **València.** Población de nacionalidad extranjera: 19,4 % [C4] en 2025 y 13,3 % [C4] en 2021. Viviendas turísticas (INE, medición experimental): 5.393 viviendas [C4] en 2026-05. El índice descriptivo de presión residencial (puntuación z media 2019-2026) varía por barrio: por ejemplo, La Seu 1,4 puntuación z media [C4] y El Mercat 2,2 puntuación z media [C4]. Es un índice descriptivo, no una medida con intervalo. <!-- check:cifra-libre (años) -->
- **Mapas.** `output/v16/f2_atlas/mapas/` contiene, para Barcelona, València y Sevilla, un mapa de los municipios de la provincia y uno de las secciones del municipio. Cada uno tiene seis paneles: renta, alquiler, esfuerzo, viviendas turísticas, población extranjera y viviendas no principales. El gris claro indica sin dato o suprimido. El gris hachurado indica validación sellada. <!-- check:cifra-libre (seis paneles, tres ciudades) -->
- **Viviendas turísticas.** La medición del INE es experimental. Inside Airbnb es un rastreo de plataforma no validado y no exhaustivo: solo se usa de forma descriptiva. Los registros autonómicos de Madrid, Canarias y Baleares no se usan.
- **Intervenciones.** El atlas incluye dos indicadores de normativa vigente (zona tensionada y regulación municipal de viviendas de uso turístico), con fecha del dato. La ausencia de fila no equivale a ausencia de regulación. <!-- check:cifra-libre (dos indicadores, diseño) -->

### IV.5 Hallazgos locales que sobreviven

Sobreviven, como hechos descriptivos [C4], los de las secciones IV.2 a IV.4: la dispersión entre territorios, el esfuerzo de alquiler por unidad y las diferencias entre ciudades. Ninguno es un efecto. A escala local no hay ningún resultado con diseño causal que haya superado todas sus pruebas.

De los contrastes exploratorios de V15 y V16, ninguno sube de C4. Se presentan a continuación como pistas, con sus limitaciones. <!-- check:cifra-libre (numeración de secciones, versiones V15 y V16) -->

### IV.6 Pistas, marcadas como tales

Todas son [C4]. Su pre-registro es interno, sin sello de tiempo externo: V16, etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17; V15, etiqueta `prereg-v15`, commit 542b4fd, 2026-10-17. Las hipótesis de V15 tienen la evaluación sellada pendiente (`evaluate_v15`, fecha límite 31-12-2027): son pendientes, no confirmadas. <!-- check:cifra-libre (etiquetas, commit y fechas de pre-registro y calendario) -->

#### Q3-b (V16): población extranjera y alquiler por sección. Correlación frágil

- **Qué es.** Asociación transversal entre la variación del alquiler mediano SERPAVI 2021-2024 (contratos vigentes) y la cuota de población extranjera de 2022, por desviación típica, con efectos fijos de municipio.
- **Resultado.** Las seis variantes pre-registradas dan el mismo signo. La principal es 0,01 y es la mayor de las variantes, no la mediana. Las variantes van de 0,00 log por desviación típica a 0,01 log por desviación típica, y su mediana es 0,01 [C4] (unidad: log por desviación típica).
- **Limitaciones.**
  - La pretendencia (el mismo ajuste con la variación 2018-2021) da 0,01 [C4]. Es más de la mitad del coeficiente principal. Una asociación previa a la exposición no se distingue de una tendencia anterior.
  - Puede haber reversión a la media o convergencia, y desbalance de renta.
  - La exposición de 2022 cae dentro de la ventana del resultado.
  - Hay un posible confusor turístico.
  - Sin intervalo: solo estimaciones puntuales.
  - Las unidades selladas están fuera de la muestra.
- **Lectura.** Correlación frágil. No se interpreta como efecto.

<!-- check:cifra-libre (seis variantes del diseño, años de ventana, «más de la mitad») -->

#### H4 (V15): población extranjera predicha y alquiler municipal. Correlación frágil

- **Qué es.** Asociación entre la variación de la población extranjera, predicha con un instrumento de tipo shift-share, y el alquiler municipal SERPAVI. Se lee como asociación descriptiva.
- **Resultado.** La estimación principal es 0,30 % por p.p. [C4]. El multiverso de 64 especificaciones va de -0,14 % por p.p. a 0,39 % por p.p., e incluye el cero. Su mediana es 0,08 % por p.p. [C4].
- **Limitaciones.**
  - La principal está en la cola alta del multiverso.
  - El signo cambia al quitar los cinco orígenes principales.
  - El número efectivo de choques es 5,5 [C4]: pocos orígenes pesan en el resultado.
  - El F robusto de primera etapa (70,2 F [C4]) es descriptivo.
  - El padrón por nacionalidad no recoge las nacionalizaciones.
  - La estimación 2SLS es varias veces la de mínimos cuadrados.
- **Estado.** Evaluación sellada pendiente.
- **Lectura.** Correlación frágil. Los dos diseños (Q3-b y H4) coinciden en el signo; eso no los convierte en un efecto.

<!-- check:cifra-libre (64 especificaciones del multiverso, cinco orígenes del diseño, 2SLS) -->

#### E3 (V15): correlación espacial del alquiler entre municipios vecinos

- **Qué es.** Un modelo autorregresivo espacial (SAR, contigüidad) sobre la variación del alquiler SERPAVI (tipología colectiva) 2015-2024 entre municipios.
- **Resultado.** El parámetro espacial ρ es 0,39 [C4]. Va de 0,24 ρ a 0,64 ρ entre las especificaciones del multiverso.
- **Lectura.** Es una correlación espacial descriptiva. Los municipios vecinos tienden a moverse en el mismo sentido. No es contagio.
- **Limitaciones.** ρ puede reflejar una tendencia regional común. El intervalo subestima la incertidumbre de especificación. La muestra depende de los vecinos disponibles.
- **Estado.** Evaluación sellada pendiente.

<!-- check:cifra-libre (periodo) -->

#### H3 (V15): viviendas turísticas y alquiler por sección. No concluyente

- **Qué es.** Asociación entre la variación del alquiler SERPAVI (contratos vigentes) y la exposición turística intra-sección 2021-2024 (INE, medición experimental), con efectos de municipio por año.
- **Resultado.** No concluyente. La mediana del multiverso es 0,07 % por DT y el rango entre especificaciones, 0,00-0,22 % por DT [C4] (el rango no es un intervalo de confianza). Efecto mínimo detectable de referencia: 0,10 % por DT [C4]. Panel principal: 12.976 secciones [C4].
- **Por qué no concluye.** La estimación principal es el mínimo del multiverso. No hay error estándar válido. La medida (stock de contratos, poca variación, topes) sesga hacia cero. Los efectos de municipio por año absorben parte de la variación y dejan fuera los mercados más turísticos. El diseño de Q2a, con el IPC de alquiler provincial, depende de los controles y de la fecha de la exposición, y tampoco concluye.
- **Estado.** Evaluación sellada pendiente.
- **Lectura.** Ni apoya ni descarta una asociación. «No concluyente» no equivale a «nula».

<!-- check:cifra-libre (periodo) -->

#### Otros contrastes territoriales

- **Q2a** (turismo e IPC de alquiler provincial) y **Q6-p** (tipo del impuesto de transmisiones y valor tasado provincial) son no concluyentes.
- **Q1c** no se cita: las pretendencias muestran rupturas previas al primer tratamiento y el resultado no se distingue del ruido previo. **Q1b** no es estimable: fuera de Cataluña, la primera zona vigente empieza en 2025, después del último año de SERPAVI del entrenamiento.
- **H2 y Q2c** no dan señal utilizable. **Q6-v** queda descriptivo: el placebo es mayor que el efecto y de signo contrario. Se nombran, sin cifras. <!-- check:cifra-libre (nombres de hipótesis, años) -->

### IV.7 Dónde ver el detalle

- **Fichas territoriales de la web.** Una ficha por territorio, con el indicador, su periodo, su fuente, su capa y su marca de calidad. Se accede desde la página de fichas de la web del proyecto.
- **Descargas.** `territorios.csv` y `territorios.parquet`, más los ficheros `atlas_*.csv` de V10.
- **Fichas del anexo.** Cada cifra `V16-ATL-*` tiene ficha en `output/v16/f2_atlas/` y en el anexo metodológico.
- **Atlas de la 1.0.** `publicacion/atlas_descriptivo.md`, `publicacion/atlas_v12.md` y `publicacion/atlas_regional/atlas_resumen.md`.

<!-- check:cifra-libre (versiones V10, V12, V16 y 1.0) -->


## Parte V · Escenarios y predicción

Esta parte reúne tres cosas distintas. Primero, cuántas viviendas hacen falta según la contabilidad de la 1.0. Segundo, qué resulta de simular medidas bajo supuestos. Tercero, qué se puede predecir y con qué límites. Ninguna de las tres se lee como un efecto identificado. Un escenario responde a «qué pasa si se cumplen estos supuestos». Una predicción responde a «qué valor es probable». Ninguna responde a «qué produce qué». <!-- check:cifra-libre (versión 1.0 del estudio) -->

### V.1 Necesidad de vivienda y déficit (cifras de la 1.0)

#### Qué se mide

La necesidad anual suma el crecimiento de hogares, la reposición y el atraso a absorber. Resta las viviendas en construcción. No resta las viviendas que deja el envejecimiento. La proyección de hogares del INE ya las descuenta. Restarlas de nuevo las contaría dos veces. `make check` comprueba esta regla.

Los rangos de abajo son rangos entre supuestos, no intervalos de confianza. Las cifras de necesidad son [C4]: dependen de hogares de fuente única y de supuestos que ningún dato contrasta.

#### Necesidad anual

- La necesidad anual 2026-2035, en la base sin la sensibilidad X, es 210.424 viviendas/año (99.388-292.083 viviendas/año) [C4]. <!-- check:cifra-libre (periodo 2026-2035) -->
- El rango pone todos los componentes en su extremo bajo o alto a la vez: 99.388-292.083 viviendas/año [C4].
- Es una cifra de orden de magnitud. Una cifra puntual no es defendible con estos datos.

Afirmación evaluada: «Hacen falta X viviendas al año». Veredicto de la 1.0: ANALIZADA, NO CONCLUYENTE [C4]. El valor depende del atraso y de las viviendas vacías movilizables, que son los componentes más inciertos. <!-- check:cifra-libre (versión 1.0) -->

#### Cambio del déficit entre 2025 y 2030

La dirección y la magnitud se separan, porque tienen capas distintas.

- **Dirección [C2].** En el recuento de provincias, 15 provincias empeoran, 0 provincias mejoran y 37 provincias quedan indeterminadas [C2]. A escala nacional el déficit empeora en todos los escenarios de la rejilla. <!-- check:cifra-libre (rejilla de 180 escenarios, número de diseño; periodo 2025-2030) -->
- **Magnitud [C4].** El cambio central es 585.609 viviendas [C4]. El rango de la rejilla es 87.246-946.852 viviendas [C4].
- **Terminadas.** Para no empeorar harían falta 211.772 viviendas/año (163.884-245.193 viviendas/año) [C4] en 2026-2030. El escenario optimista llega a 94.650-146.435 viviendas/año [C4]. El extremo bajo es el ritmo reciente y el alto, el máximo plausible. <!-- check:cifra-libre (periodo 2026-2030) -->

#### Dos mínimos de T4-H2

El extremo inferior del rango depende de una convención de cálculo. Hay dos versiones y se dan las dos.

| Versión | Convención | Mínimo del cambio del déficit | Capa |
|---|---|---|---|
| Publicada | Tras 2025 la cartera toma el valor de relleno del escenario, sin interpolar | 87.246 viviendas | [C4] |
| Alternativa | Interpolación lineal entre 2025 y el valor de relleno | 103.788 viviendas | [C4] |

<!-- check:cifra-libre (años de la tabla) -->

La convención publicada hace más favorable el escenario optimista. Adelanta las terminadas del relleno a los años de 2026 a 2030 y baja el extremo inferior del déficit. La interpolación lineal sube ese extremo y hace el escenario optimista menos favorable. El valor central y la dirección no dependen de la convención. Por eso la afirmación «el déficit empeora en toda la rejilla» no cambia. La ficha T4-H2 del anexo metodológico (output/v6_2/anexo_metodologico.md) describe las dos versiones. Una réplica ciega de V16 reprodujo el valor central y el máximo, y explicó el mínimo por esta convención. <!-- check:cifra-libre (años 2025 y 2026-2030; referencia a la ficha del anexo) -->

Afirmación evaluada: «Al ritmo actual el déficit se cerrará en pocos años». Veredicto de la 1.0: NO RESPALDADA [C2]. Lo que la sostiene es la dirección, no la magnitud. Una producción sostenida muy por encima del escenario optimista, o unos hogares claramente por debajo de la proyección baja del INE, podrían cambiar la dirección. <!-- check:cifra-libre (versión 1.0) -->

#### Déficit acumulado hasta 2024

Aquí se cuenta el aumento de hogares menos las viviendas terminadas. La cuantía es una cota, porque la EPA cambió de método en 2021 y hay siete correcciones posibles del salto. <!-- check:cifra-libre (año 2021 y número de correcciones, diseño) -->

- Sin bajas del parque, 2021-2024: 389.361-710.542 viviendas [C2]. <!-- check:cifra-libre (periodo 2021-2024) -->
- Sin las dos variantes que conservan el salto de la EPA: 596.371-710.542 viviendas [C2].
- Con las bajas estimadas en v5.1: 389.361-765.994 viviendas [C4]. Es la única cifra con bajas desde v7.2. <!-- check:cifra-libre (versiones v5.1 y v7.2) -->
- Hasta 2025, sin bajas: 523.606-887.950 viviendas [C4]. Las terminadas de 2025 son frágiles. <!-- check:cifra-libre (año 2025) -->

El signo lo confirman dos fuentes de hogares y dos de terminadas en todas las variantes. La cuantía es una cota. Afirmación evaluada: «Faltan cientos de miles de viviendas». Veredicto de la 1.0: PARCIALMENTE [C2]. «Cientos de miles» se cumple en todas las variantes. Una cifra puntual no es defendible. <!-- check:cifra-libre (versión 1.0; dos fuentes de hogares y dos de terminadas, diseño) -->

#### Hogares proyectados [C2]

La proyección de hogares del INE da un crecimiento 2026-2035 de 1.720.537 hogares (1.308.531-1.772.410 hogares) [C2] y 2026-2030 de 1.024.156 hogares (819.421-1.060.364 hogares) [C2]. Son proyecciones oficiales, no observaciones. <!-- check:cifra-libre (periodos) -->

#### Viviendas liberadas por el envejecimiento

Las viviendas que quedan libres por fallecimiento o traslado a residencia son una cifra de orden de magnitud [C4]. No se restan de la necesidad. No suman a la oferta adicional, porque la proyección de hogares ya las incluye. Se informa de ellas aparte. Su destino (venta, alquiler, herencia o uso esporádico) no tiene dato.

### V.2 Simulaciones condicionales

Una simulación aplica una medida a un modelo con supuestos y devuelve una variación. Todas las de esta sección son [C4]. En la simulación, cada medida se asocia con un cambio de precio o de esfuerzo. La simulación no mide lo que ocurriría en la realidad. Los resultados dependen de elasticidades de oferta que no se han estimado con datos de España.

Cada resultado declara su medida de precio: precio de compra o de alquiler de mercado, y esfuerzo del hogar. El horizonte es de 10 años. El ámbito son 17 comunidades autónomas. Las cifras son la mediana entre comunidades, con el rango entre comunidades. <!-- check:cifra-libre (horizonte de 10 años y 17 comunidades, números de diseño) -->

#### V71-S1 y V71-S3: rejilla de medidas

- **Vivienda pública o asequible, por cada 10.000 viviendas.** En la simulación, el alquiler de mercado varía -3,2 puntos % (-12,2 a -0,56 puntos %) [C4]. La compra varía -0,61 puntos % (-2,4 a -0,11 puntos %) [C4]. <!-- check:cifra-libre (dosis de 10.000 viviendas, diseño) -->
- **Variación acumulada a 10 años con esa medida.** En la simulación, alquiler: -3,0 % (-5,3 a -0,64 %) [C4]. Compra: -0,57 % (-1,0 a -0,13 %) [C4]. <!-- check:cifra-libre (horizonte de 10 años) -->
- **Robustez.** El esfuerzo baja en todas las extracciones y el precio de mercado no sube en 17 CCAA de 17 en alquiler y en 12 CCAA de 17 en compra. <!-- check:cifra-libre (17 CCAA, diseño) -->
- **Regulación local de turísticos.** En la simulación, alquiler a 10 años: -0,50 % (-3,0 a -0,18 %) [C4]. Compra: -0,09 % (-0,53 a -0,03 %) [C4]. Es robusta en 8 CCAA de 17 en alquiler y en 1 CCAA de 17 en compra. <!-- check:cifra-libre (horizonte de 10 años, 17 CCAA) -->
- **Ayudas a la demanda (compra).** Coste fiscal anual aproximado: 378,2 M€/año (68,0-2.915 M€/año) [C4]. En la simulación, cada 100 M€ anuales se asocian con una variación del precio de mercado de 1,4 puntos % (0,16-7,6 puntos %) [C4]. El signo es al alza. <!-- check:cifra-libre (unidad de 100 M€, diseño) -->

Lectura. Con dosis de 10.000 a 25.000 viviendas al año, la vivienda pública queda lejos de la brecha de la sección V.1. Que «resuelva» el problema depende del volumen y del desplazamiento de la construcción privada. En la simulación, la ayuda a la demanda baja el precio neto para quien la recibe y sube el de mercado. En la simulación, quien no la recibe paga más. Ese reparto por grupos es el único resultado de signo que la ficha del verificador de la 1.0 sitúa en [C2]. Las cifras de esta sección son [C4]; el C2 no se apoya en ellas. <!-- check:cifra-libre (dosis de 10.000 y 25.000 viviendas al año de la ficha V11 del verificador; versión 1.0) -->

#### Límites de la rejilla

- La ficha del anexo de V71-S3-R6 estaba incompleta: omitía supuestos de la rejilla. Tras completarlos, la réplica ciega de V16 reprodujo V71-S3-R6 al bit (decisión K19). Esa reproducción confirma el cálculo, no los supuestos. Las cifras de V71-S3-R6 son [C4] y no sostienen ningún veredicto [C2]. <!-- check:cifra-libre (identificadores V71-S3-R6 y K19) -->
- La variación de precio depende de elasticidades de oferta y de un coste unitario que son parámetros, no estimaciones.
- La rebaja de ITP o IVA de la vivienda nueva tiene su fila en la rejilla (V71-S1-f1). La afirmación sobre su incidencia en el precio que paga el comprador está NO ANALIZADA por falta de datos. <!-- check:cifra-libre (identificador V71-S1-f1) -->
- En el análisis regional de largo plazo de V7.1, las hipótesis confirmadas son 0 de 7 pre-registradas [C4]. <!-- check:cifra-libre (versión V7.1; 7 hipótesis del diseño) -->

#### Q5 de V16

Q5 estimó la respuesta del alquiler y del valor tasado a sorpresas de política monetaria. No se cita ninguna cifra. Motivo: la primera etapa tiene el signo contrario al esperado, el placebo es comparable al resultado y la respuesta cambia de signo. Es un resultado sin señal utilizable. <!-- check:cifra-libre (identificador de hipótesis Q5) -->

### V.3 Predicción y sus límites

#### Qué se evalúa

Una predicción se compara siempre con el modelo sencillo más exigente (un autorregresivo de orden 4, AR(4)) y con el ECM v1, en la misma muestra de objetivos. Un modelo solo «predice mejor» si lo supera. Predecir bien no dice nada sobre qué mueve el precio. Ningún coeficiente, ninguna importancia ni ningún valor SHAP se lee como efecto. <!-- check:cifra-libre (nombres de modelos: AR(4), ECM v1) -->

**Estado del contraste DM-HLN.** El contraste de Diebold-Mariano con corrección de Harvey, Leybourne y Newbold (DM-HLN) es apto bajo el proceso generador de datos de V15 y no apto bajo el de V16. No se usa como prueba en este informe. <!-- check:cifra-libre (versiones V15 y V16; nombre del contraste) -->

#### Pre-registros de V15 y V16

Los resultados de V15 y V16 son un pre-registro interno sin sello de tiempo externo.

- V15: etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (commit y fecha del pre-registro de V15) -->
- V16: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (commit y fecha del pre-registro de V16) -->

Las hipótesis de V15 tienen la evaluación sellada pendiente (`evaluate_v15`, fecha límite 31-12-2027). Se presentan como pendientes, nunca como confirmadas. Todo lo de esta sección es [C4]: nivel de evidencia descriptivo o exploratorio. <!-- check:cifra-libre (fecha límite de la evaluación sellada; V15) -->

#### H5 de V15: la combinación no supera al AR(4)

H5 combinaba varios modelos para predecir el valor tasado un trimestre adelante. El diseño contrastaba si la combinación supera al AR(4). No lo supera. <!-- check:cifra-libre (identificadores H5, AR(4); horizonte de un trimestre) -->

- La razón del error cuadrático medio de la combinación frente al AR(4), pre-registrada, es 1,5 razón [C4]. Una razón mayor que uno quiere decir que la combinación se equivoca más.
- Según la implementación, la razón va de 1,2-1,5 razón (de la réplica ciega a la producción pre-registrada). Se cita el rango entre implementaciones, no solo la cifra pre-registrada. En las dos la razón es mayor que uno.
- No se cita un valor p: el DM-HLN no se usa como prueba (véase arriba su estado). La conclusión descansa en la razón de error.
- La STL por origen se eligió por la regla «sin datos posteriores al origen», no por su valor. Se decidió después de ver la reconciliación entre implementaciones, y así consta. <!-- check:cifra-libre (identificador STL; «mayor que uno» como umbral de la razón) -->

La evaluación sellada de V15 sigue pendiente.

#### Q10 de V16: tres series nacionales, horizonte de un trimestre

Q10 prueba un modelo más elaborado contra el AR(4) en tres series nacionales: el índice de precios, el IPC de alquiler y las compraventas. Los resultados son descriptivos. El DM-HLN no se usa como prueba (véase arriba) y el contraste de Clark-West no superó la calibración. No hay valor p. Solo se informa de la reducción puntual del error. Se usan los datos en su última edición, no en tiempo real. <!-- check:cifra-libre (identificadores Q10 y AR(4); horizonte de un trimestre) -->

| Serie | Modelo | Frente al AR(4) | Frente al ECM v1 reducido |
|---|---|---|---|
| Q10-1, precio (IPV) | MIDAS | empeora | el ECM v1 reducido también empeora frente al AR(4); MIDAS comete menos error que el ECM v1 reducido |
| Q10-2, IPC de alquiler | Nowcast | empeora | no existe ECM v1 para esta serie |
| Q10-3, compraventas | MIDAS | sin mejora fuera de 2020 | no existe ECM v1 para esta serie |

<!-- check:cifra-libre (identificadores Q10-1 a Q10-3, AR(4), ECM v1 y año 2020) -->

- **Q10-1 y Q10-2 empeoran frente al AR(4).** El modelo elaborado comete más error que el AR(4) en las dos series. Esto se mantiene al excluir 2020.
- **Q10-3 sin mejora fuera de 2020.** La mejora aparente en compraventas procede de 2020 y 2021, el periodo de caída y rebote. Al excluir 2020 desaparece. No se cita como pista.
- **ECM v1 reducido.** El ECM v1 de Q10 es una versión reducida, reproducida en el conjunto de entrenamiento sin la variable de costes. No equivale al modelo completo de la 1.0. Solo existe para el precio.
- **Cobertura.** Los intervalos conformes del 90 % quedan en torno o por debajo del nivel nominal en las tres series, tanto con el modelo elaborado como con el AR(4).

<!-- check:cifra-libre (años 2020 y 2021; ECM v1; versión 1.0; nivel nominal del 90 %) -->

Las cifras de Q10 no se citan. El motivo es que la comparación se apoya en un único criterio (el error puntual), sin contraste válido y con datos revisados. La evaluación sellada de Q10 no aplica: ninguna pregunta de V16 cumple las condiciones de `evaluate_v16`. <!-- check:cifra-libre (identificador Q10; evaluate_v16) -->

#### Qué se puede decir de la predicción

1. Un modelo más complejo no supera al AR(4) en las series nacionales probadas, salvo en una comparación que depende de un año atípico. El alcance es el agregado nacional trimestral.
2. La capacidad de predecir un trimestre adelante es limitada en precio y en alquiler.
3. Estos resultados no dicen nada sobre qué medidas bajan o suben los precios. Esa pregunta es de la sección V.2, con sus supuestos.
4. Cuando la 1.0 afirma que un modelo «predice mejor», la afirmación se limita a las tareas en que supera a la línea base más exigente. Está en el verificador (K1-V1) y tiene otro alcance: la validación sellada de v6, sobre provincias y municipios. <!-- check:cifra-libre (numeración de la lista, AR(4), versiones 1.0 y v6, ficha K1-V1) -->


## Parte VI · Manual de verificación

Este manual enseña a reconocer un argumento engañoso sobre la vivienda. No sirve para decidir quién tiene razón. Sirve para comprobar si una afirmación concreta se sostiene con los datos. Las afirmaciones se formulan en abstracto: se evalúa lo que se dice, nunca quién lo dice. Las mismas reglas valen para todas.

Cada apartado tiene tres partes: cómo es el truco, cómo se comprueba y un ejemplo real evaluado por el estudio. Los ejemplos salen del verificador de la 1.0 y de los hechos de V16. Las capas son: C1 hechos con al menos dos fuentes, C2 cotas con supuestos explícitos, C3 efectos identificados y C4 exploratorio. <!-- check:cifra-libre (versión 1.0; nombres de capa) -->

### Cinco preguntas antes de creer una cifra

1. ¿Qué periodo cubre y por qué ese?
2. ¿Es un valor nominal o real?
3. ¿Mide contratos vigentes o contratos nuevos?
4. ¿Es una media, un índice o un caso concreto?
5. ¿Compara dos cosas que ocurren a la vez o muestra un efecto?

<!-- check:cifra-libre (numeración de la lista) -->

### VI.1 Periodos elegidos a conveniencia

**El truco.** Una misma serie da un crecimiento muy distinto según el año de inicio y el de fin. Quien elige el periodo elige el resultado.

**Cómo se comprueba.** Pide la serie entera y prueba otras ventanas. Si la conclusión cambia con el periodo, la cifra no resume la serie.

**Ejemplo.** Para los contratos nuevos de Cataluña hay dos cifras. En 2015-2025 la renta media de las fianzas sube 54,5 % [C4]. En 2021-2024, con el índice del INE y esa misma fuente, sube 16,9 % [C1], con rango 16,6-17,2 %. Las dos son ciertas. Responden a preguntas distintas. Ninguna puede usarse sola para hablar de «lo que ha subido el alquiler». <!-- check:cifra-libre (periodos 2015-2025 y 2021-2024) -->

### VI.2 Nominal frente a real

**El truco.** Un valor nominal incluye la inflación. Un valor real la descuenta. Mezclarlos hace parecer que algo sube o baja más de lo que lo hace.

**Cómo se comprueba.** Mira si la cifra está deflactada y con qué índice. Compara siempre con la misma base y con la misma medida.

**Ejemplo.** Se usa una sola medida: el IPC de alquiler, que mide contratos vigentes. En 2019-2025 su cambio acumulado es 10,1 % en términos nominales [C4] y -9,5 % en términos reales, con el deflactor del IPC general [C4]. Es la misma serie y el mismo periodo. Solo cambia el deflactor. Lo mismo vale para el precio de compra. Con las tres medidas por m² (MIVAU, Notariado y Registradores), el cambio 2019-2025 es 30,4 % (29,6-31,7 %) nominal [C1] y 7,1 % (6,5-8,2 %) real [C1]. Con otra medida, el IPV del INE ajustado por calidad, es 44,4 % nominal y 18,7 % real [C4]. Una cifra nominal de una medida no se compara con una cifra real de otra. <!-- check:cifra-libre (periodo 2019-2025) -->

### VI.3 Contratos vigentes frente a contratos nuevos

**El truco.** El alquiler de quien firma hoy no es el alquiler de quien firmó hace años. Los contratos vigentes se actualizan con topes y cambian poco. Los nuevos reflejan el mercado actual.

**Cómo se comprueba.** Pregunta si la cifra mide el stock de contratos o el flujo de los firmados ahora.

**Ejemplo.** La afirmación «el alquiler se ha duplicado» tiene dos versiones. Con el stock, el veredicto de la 1.0 es CONTRADICHA [C1]: ninguna fuente llega a +100 % y el rango es 10,9-22,9 %. Con los contratos nuevos, la subida del índice del INE es 37,0 % [C4]. Los contratos nuevos pesan 16,0 % [C4] en el índice de contratos vigentes, y por eso el stock sube más despacio. Tampoco los contratos nuevos alcanzan +100 % en el periodo, pero su cuantía nacional es de fuente única y el veredicto es ANALIZADA, NO CONCLUYENTE. <!-- check:cifra-libre (umbral de +100 %, periodo 2015-2024 y versión 1.0) -->

### VI.4 Medias frente a índices

**El truco.** Una media nacional oculta casos concretos, y una media de precios cambia cuando cambia la mezcla de viviendas, no solo el precio. Un índice de composición constante sigue las mismas viviendas.

**Cómo se comprueba.** Pregunta si es una media o un índice, y si se refiere a todos los casos o a una parte.

**Ejemplo.** Que la media no llegue a +100 % no excluye que algún municipio sí lo alcance. En Cataluña, 1 de 261 municipios con al menos 30 fianzas tiene una renta media de fianzas doble o más entre 2015 y 2025 [C4]. En la Comunitat Valenciana son 2 de 103 municipios, entre 2020 y 2025 [C4]. Un caso así no demuestra que la media sea otra. La media tampoco descarta el caso. <!-- check:cifra-libre (tamaños de muestra 261 y 103, número mínimo de fianzas y periodos) -->

### VI.5 Correlación presentada como si fuera un efecto

**El truco.** Dos cosas suben a la vez y se afirma que una produce la otra. Puede ser que ambas crezcan con la urbanización, con la costa o con el tiempo. Es una correlación presentada como si fuera un efecto.

**Cómo se comprueba.** Busca si la asociación ya existía antes de que ocurriera lo que se invoca (pretendencia). Mira si desaparece con controles. Mira si el rango de las especificaciones incluye el cero.

**Ejemplo, Q3-b de V16.** Entre las secciones censales, la subida del alquiler 2021-2024 se asocia con la cuota de extranjeros: 0,01 (log por desviación típica) [C4]. Pero el mismo cálculo sobre 2018-2021, antes del periodo, da 0,01 [C4]. La asociación ya estaba. Es una pista descriptiva y frágil, no un efecto. Pre-registro interno sin sello de tiempo externo (etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17).

**Ejemplo, H4 de V15.** La asociación entre la población extranjera predicha y el alquiler municipal es 0,30 % por p.p. en la estimación principal [C4]. El rango del multiverso de especificaciones va de -0,14 % por p.p. a 0,39 % por p.p. e incluye el cero. No se puede leer como un efecto. Pre-registro interno sin sello de tiempo externo (etiqueta `prereg-v15` en el remoto, commit 542b4fd, 2026-10-17); evaluación sellada pendiente. <!-- check:cifra-libre (periodos 2018-2021 y 2021-2024; commits y fechas de los pre-registros) -->

Que un cálculo salga con el signo esperado no lo vuelve un efecto. Solo lo vuelve un diseño que supere pretendencias, placebos y sensibilidad. La 1.0 sitúa todas sus estimaciones de este tipo en C4. <!-- check:cifra-libre (versión 1.0) -->

### VI.6 Efecto base

**El truco.** Un porcentaje grande puede venir de partir de un valor muy bajo, o de comparar con un año atípico. Un rebote parece una tendencia.

**Cómo se comprueba.** Mira el nivel de partida y quita el año atípico. Si la conclusión desaparece, dependía de la base.

**Ejemplo 1, compraventas (Q10-3 de V16).** Un modelo de predicción parece mejorar al modelo sencillo en las compraventas. La mejora procede de los años 2020 y 2021, de caída y rebote. Al excluir 2020 desaparece. Por eso Q10-3 se describe como «sin mejora fuera de 2020» y no se cita como pista. <!-- check:cifra-libre (años 2020 y 2021; identificador Q10-3) -->

**Ejemplo 2, déficit acumulado.** El déficit 2021-2024 depende de cómo se trate el salto de la encuesta de hogares de 2021. Con todas las variantes, el rango sin bajas es 389.361-710.542 viviendas [C2]. Sin las dos variantes que conservan el salto, es 596.371-710.542 viviendas [C2]. La base de la comparación cambia el resultado, y por eso la 1.0 da una cota y no una cifra puntual. <!-- check:cifra-libre (periodo 2021-2024 y año 2021; versión 1.0) -->

### VI.7 Escala que esconde la heterogeneidad

**El truco.** Una cifra nacional puede ser cierta y no describir ningún sitio concreto. Lo que pasa en el conjunto no pasa en cada provincia o ciudad.

**Cómo se comprueba.** Pide el desglose por territorio. Mira cuántas unidades empeoran, cuántas mejoran y cuántas no se pueden decir.

**Ejemplo, déficit por provincias.** A escala nacional, el déficit 2025-2030 empeora en todos los escenarios de la rejilla [C2]. Por provincias, 15 empeoran, 0 provincias mejoran y 37 provincias quedan indeterminadas [C2]. La dirección nacional es robusta. La provincial queda sin determinar en la mayoría de las provincias. <!-- check:cifra-libre (periodo 2025-2030 y rejilla de escenarios) -->

**Ejemplo, viviendas turísticas.** La cota nacional del alquiler que las viviendas turísticas podrían desplazar es de 2,4-2,7 % del stock de alquiler [C2], entre 2020 y 2024. En una ciudad concreta la cota es mayor: el repositorio no tiene una cota por ciudad, así que el ejemplo se queda en la escala nacional. Una cifra nacional baja no excluye una concentración local alta. Una cifra local alta tampoco se extiende al país. <!-- check:cifra-libre (periodo 2020-2024 y supuesto de sustitución 1:1) -->

### VI.8 Anuncios frente a entregas

**El truco.** Un objetivo de viviendas anunciadas no equivale a viviendas terminadas y habitables. Entre el anuncio y la entrega hay iniciadas, retrasos, calificaciones y bajas.

**Cómo se comprueba.** Compara el objetivo con las terminadas y con la necesidad en el mismo periodo. Mira qué parte son viviendas nuevas netas y qué parte sustituye a las que salen del parque protegido.

**Ejemplo, ritmo de terminadas.** Para no empeorar el déficit 2026-2030 harían falta 211.772 viviendas/año (163.884-245.193 viviendas/año) [C4]. El escenario optimista llega a 94.650-146.435 viviendas/año [C4]. El extremo bajo es el ritmo reciente y el alto, el máximo plausible. Un anuncio solo es comparable con estas cifras si está medido en viviendas terminadas por año. <!-- check:cifra-libre (periodo 2026-2030) -->

**Ejemplo, vivienda protegida.** En los escenarios ilustrativos, las viviendas que saldrían del régimen de protección en 2026-2035 son 594.890 viviendas [C4]. Las calificaciones definitivas nuevas son 11.265 viviendas/año [C4] de media anual en 2021-2025. Un anuncio de viviendas protegidas tiene que restar las salidas por fin de plazo para dar el saldo. Las salidas son escenarios con supuestos, no descalificaciones observadas. <!-- check:cifra-libre (periodos 2026-2035 y 2021-2025) -->

### Verificador ampliado

Esta tabla recoge afirmaciones que el estudio permite evaluar. Usa la escala del verificador de la 1.0: RESPALDADA, PARCIALMENTE, NO RESPALDADA, CONTRADICHA, ANALIZADA, NO CONCLUYENTE y NO ANALIZADA: FALTAN DATOS. Con una capa C4, el veredicto máximo es ANALIZADA, NO CONCLUYENTE. Las afirmaciones se evalúan; las personas y los partidos no. «NO ANALIZADA: FALTAN DATOS» quiere decir que no hay datos para analizar la afirmación, no que sea falsa. Los resultados de V15 y V16 son un pre-registro interno sin sello de tiempo externo, con la evaluación sellada de V15 pendiente. <!-- check:cifra-libre (versión 1.0; identificadores V15 y V16) -->

| Afirmación | Veredicto | Capa | Cifra | Por qué |
|---|---|---|---|---|
| El alquiler se ha duplicado (contratos vigentes) | CONTRADICHA | C1 | 10,9-22,9 % [C1] | Ninguna fuente llega a +100 %. Las dos fuentes del núcleo coinciden. |
| El alquiler se ha duplicado (contratos nuevos) | ANALIZADA, NO CONCLUYENTE | C4 | 37,0 % [C4] | La cuantía nacional de contratos nuevos es de fuente única. |
| Al ritmo actual el déficit se cerrará en pocos años | NO RESPALDADA | C2 | 15 provincias empeoran, 0 provincias mejoran y 37 provincias indeterminadas [C2] | La dirección empeora en toda la rejilla. La magnitud, 87.246-946.852 viviendas [C4], es solo C4. |
| Faltan cientos de miles de viviendas | PARCIALMENTE | C2 | 389.361-710.542 viviendas [C2] | Dos fuentes confirman el signo. La cuantía es una cota por la corrección de la encuesta de hogares. |
| Hacen falta X viviendas al año | ANALIZADA, NO CONCLUYENTE | C4 | 210.424 viviendas/año (99.388-292.083 viviendas/año) [C4] | Rango entre supuestos, no intervalo. Las liberadas por envejecimiento no se restan. |
| La vivienda que dejan los mayores resolverá el problema | ANALIZADA, NO CONCLUYENTE | C4 | Sin cifra citable aquí | Ya están descontadas en la proyección de hogares. Su destino no tiene dato. |
| Hay una burbuja en el precio de la vivienda | ANALIZADA, NO CONCLUYENTE | C4 | 0 series con exuberancia tras ajuste múltiple; 1 sin ajuste [C4] | Una exuberancia estadística no identifica una burbuja. El contraste no distingue renta, tipos ni oferta. |
| La subida de alquileres es atribuible a las viviendas turísticas | ANALIZADA, NO CONCLUYENTE | C4 | 2,4-2,7 % del stock de alquiler [C2] (cota de cantidad) | La cota de cantidad limita el desplazamiento nacional. El paso a precio depende de una elasticidad no verificada. |
| Los compradores no residentes encarecen la vivienda | ANALIZADA, NO CONCLUYENTE | C4 | Peso de no residentes en las compraventas de 2025 (R1A-H1): 6,8 % [C4] | Hay un peso descriptivo. Asociación bivariada con el precio 2015-2025 (R1A-H4): 0,96 % de precio por punto de peso inicial, rango 0,46-1,5 % de precio por punto de peso inicial [C4]. Con controles (R1A-H5): 0,02 % de precio por punto de peso inicial, rango -0,55 a 0,59 % de precio por punto de peso inicial, que incluye cero [C4]. |
| La población extranjera se asocia con subidas del alquiler municipal | ANALIZADA, NO CONCLUYENTE | C4 | 0,30 % por p.p. en la estimación principal [C4] | Correlación frágil: el rango del multiverso, de -0,14 % por p.p. a 0,39 % por p.p., incluye cero. Evaluación sellada de V15 pendiente. |
| La vivienda pública resolvería el problema | ANALIZADA, NO CONCLUYENTE | C4 | En la simulación, precio de compra a 10 años: -0,57 % (-1,0 a -0,13 %) [C4] | Las cifras de la simulación son C4. «Resolver» depende del volumen y del desplazamiento. La ficha V11 del verificador de la 1.0 la sitúa en PARCIALMENTE (C2) para el esfuerzo de acceso, no para el precio de compra. |
| Las ayudas a la demanda abaratan el acceso | PARCIALMENTE | C2 | En la simulación, 1,4 puntos % (0,16-7,6 puntos %) por 100 M€ en el precio de mercado [C4] | El beneficiario paga igual o menos (C2, ficha del verificador de la 1.0). En la simulación, parte de la ayuda llega al precio. |
| La rebaja del ITP o del IVA abarata la compra | NO ANALIZADA: FALTAN DATOS | C4 | — | Falta una serie armonizada de tipos. La incidencia depende de la elasticidad de oferta. |
| Las empresas y fondos dominan el alquiler | ANALIZADA, NO CONCLUYENTE | C4 | 16,9-38,1 % del stock [C4] del stock (residuo de personas jurídicas, sector público y no declarado) | Los dos métodos discrepan. Ninguno llega al 50 %, pero no miden el peso por zonas. |
| Los modelos más complejos predicen mejor que uno sencillo | ANALIZADA, NO CONCLUYENTE | C4 | 1,5 razón [C4] pre-registrada, razón de error frente al AR(4); entre implementaciones, 1,2-1,5 razón | Alcance: agregado nacional trimestral. Una razón mayor que uno es peor. La combinación no supera al AR(4). Q10-1 y Q10-2 empeoran y Q10-3 no mejora fuera de 2020. La validación sellada de v6 (6 de 9 tareas) tenía otro alcance (provincias y municipios) y no se traslada aquí. El DM-HLN es apto bajo el proceso generador de V15 y no apto bajo el de V16: no se usa como prueba. |

<!-- check:cifra-libre (identificadores de hipótesis R1A, V11 y Q10; umbrales de +100 % y 50 %; 2020; 2025; AR(4); 9 tareas del diseño; v6; DM-HLN) -->

#### Cómo se lee la tabla

- Un veredicto ANALIZADA, NO CONCLUYENTE no quiere decir que la afirmación sea falsa. Quiere decir que los datos disponibles no bastan para sostenerla ni para negarla.
- En la 1.0, los veredictos CONTRADICHA y NO RESPALDADA descansan en capas C1 y C2. Con una capa C4 no se llega a ninguno de los dos.
- Una cifra en C4 informa del orden de magnitud. No es una medición de un efecto.
- Las simulaciones muestran qué se asocia con qué bajo los supuestos del modelo. No dicen qué ocurriría.
- Compradores: «no residentes» no equivale a «extranjeros» (nacionalidad). La cifra de R1A-H1 es de no residentes, de la tabla 1.6 del Boletín del MIVAU, para España en el año 2025. La cuota anual de no residentes de Q8, 7,6 % de las transacciones [C4], viene de otra tabla del mismo Boletín, de un agregado de entrenamiento (9 CCAA más Ceuta y Melilla). Las dos fuentes, el ámbito y la ventana difieren, y por eso las cuantías difieren. Se dan ambas. <!-- check:cifra-libre (tabla 1.6; 9 CCAA del agregado de entrenamiento; identificadores R1A-H1 y Q8) -->
- Cuando el estudio no tiene datos, lo declara. No rellena el hueco.

<!-- check:cifra-libre (referencias a capas y veredictos; versión 1.0) -->


## Parte VII · Lo que no se puede afirmar y por qué

Esta parte evalúa afirmaciones frecuentes en el debate. No evalúa a quien las dice. Para cada una indica qué no se puede afirmar con los datos y los diseños disponibles, y por qué: datos, diseño, potencia o pruebas fallidas.

Tres reglas de lectura:
- La ausencia de hallazgo no demuestra la ausencia del fenómeno. Muchos diseños tienen poca potencia o no tienen inferencia válida.
- Todo lo de V15 y V16 es [C4]. Ningún resultado alcanza C3. Las estimaciones se leen como asociaciones. <!-- check:cifra-libre (nombres de versión y de capa) -->
- Los pre-registros de V15 y V16 son internos, sin sello de tiempo externo (anexo C). <!-- check:cifra-libre (nombres de versión) -->

### VII.1 «Hay una burbuja» y «no hay burbuja»

**Qué no se puede afirmar.** Ni que haya una burbuja ni que no la haya [C4].

**La pista de V16 (Q9-g), no confirmada [C4].**
- Q9-g mide la exuberancia estadística (GSADF) del factor común del cociente entre el valor tasado y el IPC de alquiler. El estadístico es 5,9; el valor crítico bootstrap del 95 % es 3,3 estadístico. <!-- check:cifra-libre (id de pregunta y nivel del 95 % del diseño) -->
- El p sin ajuste es 0,00. <!-- check:cifra-libre (id de pregunta) -->
- Con el control de falsos descubrimientos de Benjamini-Yekutieli sobre la rama de diseños (m = 21), el q es 0,31. El umbral pre-registrado es q ≤ 0,10 y no se alcanza. Por eso es una pista y no un hallazgo. <!-- check:cifra-libre (m = 21 y umbral q ≤ 0,10 del diseño) -->
- Q9 no tiene magnitud de referencia pre-registrada, así que tampoco se cumple la condición de tamaño. <!-- check:cifra-libre (id de pregunta) -->

**Tres advertencias.**
1. **Corrección múltiple.** El p sin ajuste no es el que cuenta. Tras el ajuste, el q queda por encima del umbral. Las pruebas sin p válido, por herramienta no apta, cuentan en el denominador y no pueden rechazarse.
2. **Valor tasado suavizado y con retraso.** La tasación se suaviza y llega tarde. Eso puede generar un patrón explosivo aparente. La revisión adversarial lo lee como artefacto probable: la mayoría de las fechas marcadas caen en tramos en que el cociente baja o está plano. Además, la prueba de calibración no cubre este proceso generador, porque la variación del factor es persistente y heterocedástica.
3. **Una exuberancia estadística no identifica una burbuja.** Un resultado explosivo es compatible con cambios en los fundamentales, en los tipos de interés o en la composición de lo que se mide. Con tipos de interés, V7.2 no rechaza. La alternativa con SERPAVI anual no rechaza, pero tiene muy pocos periodos y no tiene potencia. <!-- check:cifra-libre (nombre de versión) -->

**El GSADF de V7.2, corregido (K20) [C4].**
- Cocientes nacionales (precio/renta y precio/alquiler) con exuberancia tras el ajuste múltiple, en la familia publicada de 8 contrastes: 0. <!-- check:cifra-libre (tamaño de la familia de contrastes y nombre de versión) -->
- Solo como sensibilidad, con el ajuste limitado a la familia de 4 cocientes: 1. <!-- check:cifra-libre (tamaño de la familia de contrastes) -->
- Sin ajuste múltiple: 1.
- Niveles de precio nacionales (IPV y valor tasado) con exuberancia tras el ajuste: 0.
- Series de comunidades autónomas (17 comunidades) con exuberancia tras el ajuste: 0. <!-- check:cifra-libre (número de comunidades del diseño) -->
- Muestra de entrenamiento de v6 (11 comunidades): 0. <!-- check:cifra-libre (número de comunidades del diseño y nombre de versión) -->

La familia principal es la de 8 contrastes. La de 4 es una sensibilidad: se muestra para que el lector vea que el recuento cambia con el tamaño de la familia. Nada de esto identifica una burbuja ni la descarta. <!-- check:cifra-libre (tamaño de las familias de contrastes) -->

**Explicación en lenguaje llano.** Es un cambio de cifras de la 1.0 y se cuenta aquí.
- **Qué decía la 1.0.** Que los niveles de precio nacionales y varias series autonómicas eran «explosivos» tras el ajuste. En la 1.0 eran 2 de 2 series de niveles y 7 de 34 series autonómicas (valores de antes de la errata, en ERRATA.md). <!-- check:cifra-libre (versión) -->
- **Por qué era incorrecto.** Por dos errores de código.
  - **E1.** El contraste compara cada serie con miles de series simuladas sin burbuja. La regla que elige cuántos retardos simula el bootstrap comparaba modelos estimados con distinto número de datos. Eso la sesgaba. <!-- check:cifra-libre (id de error) -->
  - **E2.** La serie del IPV de Navarra se cortaba en 2014 porque faltaba otra serie de Navarra en 2015-2018. <!-- check:cifra-libre (id de error y años) -->
- **Cómo se vio.** La réplica ciega de V16 rehízo las cifras sin leer el código original. No coincidían, y la reconciliación encontró E1 y E2. <!-- check:cifra-libre (versión e ids de error) -->
- **Qué da el cálculo corregido.** 0 series de niveles y 0 series autonómicas con exuberancia tras el ajuste. También se pasó de 499 a 4.999 simulaciones, porque con 499 los recuentos cambiaban con la semilla. <!-- check:cifra-libre (número de simulaciones del diseño) -->
- **Qué no cambia.** La conclusión de fondo: no se puede afirmar que haya una burbuja ni que no la haya. Que no salga exuberancia no demuestra alineación con los fundamentales, porque el contraste tiene poca potencia con 78 trimestres. Que saliera tampoco identificaría una burbuja. <!-- check:cifra-libre (número de trimestres de la muestra) -->

El detalle, con los valores de antes y de después, está en el anexo de erratas y en ERRATA.md.

**Otras pruebas.** El largo plazo entre valor tasado y alquiler no se contrasta: Westerlund, CIPS y CS-ARDL no pasaron el Monte Carlo (E1 de V15 y Q9-c de V16). Las elasticidades de largo plazo se dan solo como estimaciones puntuales, con un rango entre estimadores que incluye ambos signos (Q9-c: estimación 0,84, rango -1,4 a 0,95 elasticidad). En el panel regional de V7.1, las hipótesis de largo plazo confirmadas son 0 hipótesis. <!-- check:cifra-libre (ids de análisis y de versión) -->

### VII.2 «Un solo factor es el responsable de la subida»

**Qué no se puede afirmar.** Que turismo, inmigración, falta de oferta, tipos de interés, compradores extranjeros o empresas sean el factor principal.

**Por qué.**
- **Datos.** Los factores se mueven juntos. El componente común a las comunidades y a la zona euro es grande: la correlación del factor común español con el de la zona euro es 0,60 (intervalo del 95 %: 0,14-0,86) [C4]. Eso describe comovimiento, no atribución. <!-- check:cifra-libre (nivel del intervalo) -->
- **Diseño.** En V8, la regla de designación de un factor como el más relevante dio «no designado» en los diez casos (dos mercados por cinco periodos). Los métodos discrepan entre sí. <!-- check:cifra-libre (versión y diseño de V8: diez casos = dos mercados por cinco periodos) -->
- **Instrumentos.** Los instrumentos externos de V8 que cumplen las condiciones de C3: 0 instrumentos. El F efectivo de la primera etapa para el empuje migratorio es 0,05. <!-- check:cifra-libre (versión y nombre de capa) -->
- **Pruebas fallidas.** Ninguna hipótesis de V8 pasa Holm con un instrumento que supere C3. V9, V15 y V16 no alcanzan C3 en ninguna pregunta. <!-- check:cifra-libre (versiones y nombre de capa) -->
- **Atribuciones.** Siempre se dan con bandas. Una atribución sin banda no es citable.

**Qué sí hay.** Hechos [C1] sobre cuánto han subido el precio y el alquiler, y sobre cuánto han crecido los hogares frente a las viviendas terminadas (resumen ejecutivo). Describen qué ha pasado, no qué lo ha movido.

### VII.3 «Los pisos turísticos suben (o no suben) el alquiler»

**Qué no se puede afirmar.** Ni la dirección ni la magnitud de la asociación entre vivienda turística y alquiler en España.

**Por qué.**
- **Datos.** El INE publica la vivienda turística como estadística experimental, con pocas ediciones. El SERPAVI mide el stock de contratos declarados, no los contratos nuevos. Las exposiciones de los registros autonómicos se reconstruyen con supuestos de fecha.
- **Potencia.** En H3 (V15), el coeficiente principal (0,00 % por DT) está por debajo del efecto mínimo detectable (0,10 % por DT). La mediana de su multiverso es 0,07 % por DT (0,00-0,22 % por DT). H3 es no concluyente, no nula. <!-- check:cifra-libre (ids de hipótesis y versión) -->
- **Diseño.** Q2a (provincias) es no concluyente. Q2c (IPVA municipal) cambia de signo según la especificación, falla la prueba de Oster y tiene heterocedasticidad. En E4 (Cataluña y Comunitat Valenciana), la regla puntual de pretendencias la cumplen 6 de 16 especificaciones. El BLP/GATES no pasó el Monte Carlo. <!-- check:cifra-libre (ids de pregunta) -->
- **Triangulación.** H3 y Q2a tienen el mismo signo; Q2c, el contrario. Las escalas «por desviación típica» no son comparables entre diseños, así que no se comparan magnitudes. <!-- check:cifra-libre (ids de pregunta) -->

**Qué sí hay.** Una cota [C2]: el aumento de viviendas turísticas entre 2020 y 2024 equivale como máximo a 2,7 % del stock de alquiler (2,4-2,7 % del stock de alquiler). En viviendas, con sustitución uno a uno, 81.771 viviendas (81.771-81.771 viviendas) [C2]. Es una cota de cantidad, no de precio. <!-- check:cifra-libre (años) -->

### VII.4 «La inmigración sube (o no sube) los precios y el alquiler»

**Qué no se puede afirmar.** Que la inmigración suba o baje el precio o el alquiler.

**Por qué.**
- **Instrumentos débiles.** En V9, el F efectivo del instrumento por cuotas de origen es 2,8 (alquiler) y 3,4 (valor tasado). Está muy por debajo del umbral de 10 que fija el diseño de V8 para C3. En V8, el del empuje migratorio es 0,05. <!-- check:cifra-libre (versiones y umbral F ≥ 10 del diseño) -->
- **Pocos orígenes efectivos.** En H4, el número efectivo de choques es 5,5. En Q3-c, el origen de mayor peso aporta una fracción 0,48 del estimador. <!-- check:cifra-libre (ids de hipótesis y pregunta) -->
- **Fragilidad de H4.** Estimación principal: 0,30 % por punto porcentual de población extranjera predicha [C4]. Cambia de signo al quitar los cinco orígenes de mayor peso, y la AKM no pasó el Monte Carlo. Mediana del multiverso: 0,08 % por punto porcentual [C4]. <!-- check:cifra-libre (id de hipótesis y número de orígenes del diseño) -->
- **Pretendencia de Q3-b.** Estimación principal: 0,01 (log por desviación típica) [C4]. El placebo con el periodo anterior da 0,01, del mismo orden. La inferencia de Conley no pasó el Monte Carlo. Mediana del multiverso: 0,01 [C4]. <!-- check:cifra-libre (id de pregunta) -->
- **Signos que dependen de la medida.** En el valor tasado provincial, la asociación es 0,01 log por punto de población (0,01-0,05 log por punto de población); en las compraventas, -0,03 log por punto de población (-0,08 a -0,02 log por punto de población). Ninguna tiene inferencia válida.
- **Controles.** El signo cambia con el control de población, la medida de precio, el método y la escala. Controlar por población es un mal control, porque la población crece por la propia inmigración.
- **Datos.** El padrón por nacionalidad no recoge las nacionalizaciones y termina en 2022. <!-- check:cifra-libre (año) -->

**Qué sí hay.** La contabilidad [C4]: de dónde viene el aumento de hogares y de población (Parte I). Es descriptiva.

### VII.5 «Los topes al alquiler y las zonas tensionadas bajan (o no bajan) el alquiler»

**Qué no se puede afirmar.** Que bajen el alquiler, que reduzcan la oferta o que no hagan ninguna de las dos cosas.

**Por qué.**
- **Datos.** Solo hay trimestres posteriores a la declaración para Cataluña. Fuera de Cataluña, la primera zona vigente empieza en 2025, después del último año de SERPAVI del entrenamiento: Q1b no es estimable. El SERPAVI es stock de contratos; un tope sobre contratos vigentes no se lee con los contratos nuevos. En Cataluña, la brecha de crecimiento entre nuevos y vigentes es 10,8 p.p. (9,7-11,9 p.p.) [C1]. <!-- check:cifra-libre (ids de pregunta y años) -->
- **Diseño de H1.** En V15, la estimación de entrenamiento tiene signo negativo. Falla las pretendencias y el placebo temporal. El control sintético de los grandes municipios da signo contrario. Solo se cita el signo: la magnitud no se cita, porque el placebo, las pretendencias y las cotas no lo permiten. H2 no tiene señal estable. <!-- check:cifra-libre (ids de hipótesis y versión) -->
- **Pretendencias de Q1c.** El estudio de eventos muestra rupturas en la brecha entre provincias tratadas y no tratadas antes del primer tratamiento. Q1c no se cita con cifras. <!-- check:cifra-libre (id de pregunta) -->
- **V9.** La Ley 11/2020 se asocia con -5,9 % (-7,3 a -4,4 %) en la renta de los contratos nuevos frente a municipios comparables [C4]. Es compatible con la literatura y no supera la robustez a desviaciones de tendencia. <!-- check:cifra-libre (versión y número de ley) -->
- **Selección.** Los municipios tratados no se eligen al azar: la declaración depende de criterios de precio (art. 18 de la Ley 12/2023). La tasa de declaración entre los municipios que superan el criterio no se cita con cifra. <!-- check:cifra-libre (artículo y número de ley) -->
- **Desplazamientos.** El paso a contratos de temporada y a venta no se puede medir con los datos de entrenamiento.
- **Potencia.** Las herramientas de inferencia (Honest DiD, Webb, control sintético) no pasaron el Monte Carlo.

**Pendiente.** H1 y H2 se evaluarán con la muestra sellada, a partir de marzo de 2027. <!-- check:cifra-libre (ids de hipótesis y fecha del calendario) -->

### VII.6 «Los compradores extranjeros o no residentes suben (o no suben) el precio»

**Qué no se puede afirmar.** Que limitar o liberar las compras de no residentes cambie el precio. Ni que el fin de la golden visa tenga algún efecto en la cuota de compradores.

**Por qué.**
- **Datos.** La fuente (MIVAU) da el total de no residentes, sin separar UE de extra-UE. La cuota total no identifica los visados de oro. No hay autorizaciones por programa.
- **Dos categorías distintas.** «Extranjero (residente o no)» y «no residente» no son lo mismo. La cifra de compraventas con comprador extranjero, residente o no, viene de Ministerio y Notariado: 16,9 % (16,9-18,8 %) [C4]. La cifra de no residentes, de MIVAU (tabla 1.6, España, 2025): 6,8 % [C4]. Son categorías distintas, no dos medidas de la misma.
- **Dos cuotas de no residentes.** La de R1A-H1 es nacional, de la tabla 1.6 del Boletín del MIVAU. La de Q8 para 2025 es 7,6 % de las transacciones [C4]. Q8 usa otra tabla (Boletín en línea, tabla 340101d0) y otro ámbito: el agregado de entrenamiento (nueve comunidades más Ceuta y Melilla). Por eso difieren; son fuentes y ventanas distintas. <!-- check:cifra-libre (tabla de la fuente y número de comunidades del diseño) -->
- **Diseño de Q8.** Es descriptiva: sin estimador, sin placebo, sin diferencias en diferencias. La cuota de no residentes en el agregado de entrenamiento pasa de 8,7 % de las transacciones (2024T2-2025T1) a 7,4 % de las transacciones (2025T2-2026T1), una variación de -1,3 puntos porcentuales [C4]. El año anterior ya había bajado: su variación fue -0,68 puntos porcentuales puntos porcentuales. <!-- check:cifra-libre (id de pregunta y ventanas de trimestres) -->
- **Hecho de la 1.0.** Compraventas con comprador extranjero (residente o no): 16,9 % (16,9-18,8 %) [C4]. Compraventas con comprador no residente: 6,8 % [C4]. Ministerio y Notariado no son independientes, así que no llega a C1. <!-- check:cifra-libre (nombres de capa y versión) -->
- **Asociación bivariada.** La asociación bivariada del precio 2015-2025 con el peso inicial de no residentes (0,96 % de precio por punto de peso inicial (0,46-1,5 % de precio por punto de peso inicial)) es una correlación entre provincias, no una identificación. Con controles de renta, población, costa e islas (R1A-H5), la asociación es 0,02 % de precio por punto de peso inicial (-0,55 a 0,59 % de precio por punto de peso inicial): no se distingue de cero. <!-- check:cifra-libre (id de resultado, periodo) -->

### VII.7 «Los grandes tenedores controlan el alquiler»

**Qué no se puede afirmar.** Cuántas viviendas en alquiler, o con qué precio, están en manos de grandes tenedores.

**Por qué.**
- **Datos.** El Catastro da la titularidad por tramos de inmuebles (V12), pero cuenta viviendas, no contratos de alquiler. En España sin País Vasco ni Navarra, en 2026, las viviendas de titulares con más de diez viviendas son 4,2 % y las de titulares con más de cien son 2,1 % [C4]. No dicen cuántas están alquiladas, vacías o en venta. <!-- check:cifra-libre (versión, tramos de titularidad del Catastro y año) -->
- **Compraventas.** Las compraventas con comprador persona jurídica son 11,3 % de compraventas (11,3-11,3 % de compraventas) [C4]. La persona jurídica no equivale a gran tenedor.
- **Diseño.** Ningún diseño de V15-V16 contrasta conductas de precio por tipo de titular. Las solicitudes de datos de titularidad del alquiler figuran como pendientes en la 1.0 (S1, S3 y S4). <!-- check:cifra-libre (versiones e ids de solicitud) -->

### VII.8 «Bajar el ITP abarata (o no abarata) la compra»

**Qué no se puede afirmar.** Que bajar o subir el tipo general del ITP cambie el precio o las compraventas.

**Por qué.**
- **Datos.** Las compraventas provinciales de entrenamiento son el total de vivienda, sin separar usada y nueva. Hay 14,0 cambios de tipo en pocas comunidades, concentrados en 2012-2013, en plena crisis. El diseño no separa el ITP del ciclo. <!-- check:cifra-libre (años del calendario) -->
- **Q6-p (valor tasado).** -0,00 log por punto de tipo (-0,02 a 0,01 log por punto de tipo) [C4]. No concluyente: sin inferencia válida y por debajo de la referencia de diseño. <!-- check:cifra-libre (id de pregunta) -->
- **Q6-v (compraventas).** El placebo es mayor que la estimación y de signo contrario. No se cita con cifra. <!-- check:cifra-libre (id de pregunta) -->
- **Herramientas.** dCDH, Honest DiD y la inferencia por aleatorización no pasaron el Monte Carlo.
- **Exclusiones.** País Vasco, Ceuta y Melilla quedan fuera por falta de tipo general comparable.

### VII.9 «Falta oferta» y «el suelo es el cuello de botella»

**Qué no se puede afirmar.** Que construir más baje (o suba) el alquiler o el precio, ni cuánto pesa el suelo.

**Por qué.**
- **Datos.** La pendiente, la costa, el agua y el planeamiento no están en disco y figuran como tareas del autor. El coste de construcción no tiene fuente verificable.
- **Diseño de Q4.** Usa el porcentaje de Red Natura como restricción física. La Red Natura no es exógena: se asocia con lo rural y la despoblación. Los residuos tienen dependencia espacial fuerte, y el placebo de choque adelantado tiene el mismo signo y mayor tamaño que el resultado. <!-- check:cifra-libre (id de pregunta) -->
- **Identificación.** No hay una elasticidad de oferta instrumentada con inferencia válida, así que no se separan oferta y demanda.
- **E2 (V15).** La presión demográfica no cubierta por la obra se asocia de forma positiva con el crecimiento del alquiler en las especificaciones con dato. No hay intervalo y las provincias son pocas. Que las viviendas iniciadas se asocien con el alquiler no indica que construir lo suba. <!-- check:cifra-libre (ids de análisis y versión) -->

**Qué sí hay.** Los hogares crecen más que las viviendas terminadas (997.586 hogares (981.823-1.013.350 hogares) y 72.264-94.426 viviendas/año) [C1]. El balance 2021-2024 es positivo, con cota 549.952 viviendas (389.361-710.542 viviendas) [C2]. Las viviendas liberadas por envejecimiento no se restan de la necesidad. <!-- check:cifra-libre (periodo) -->

### VII.10 «Este modelo predice el precio» y «lo que predice es lo que lo mueve»

**Qué no se puede afirmar.** Que algún modelo del proyecto prediga el precio nacional mejor que un AR(4) sencillo, ni que las variables que ayudan a predecir sean las que lo mueven. <!-- check:cifra-libre (AR(4): nombre del modelo) -->

**Por qué.**
- **H5 (V15).** La combinación de DFM, BVAR, LASSO y ARDL no supera al AR(4). La razón del ECM frente al AR(4) es mayor que uno en todas las implementaciones. Rango entre implementaciones (réplica ciega y producción pre-registrada): 1,2-1,5 razón [C4]. La pre-registrada es 1,5 [C4]. La conclusión es la misma en todas. El DM-HLN dio 0,87 p. Estado del DM-HLN: apto bajo el proceso generador de V15 y no apto bajo el de V16; no se usa como prueba. <!-- check:cifra-libre (ids de hipótesis, versiones y AR(4)) -->
- **Q10 (V16).** MIDAS y el nowcasting no mejoran al AR(4) en el IPV ni en el IPC de alquiler. En las compraventas, la mejora aparente desaparece al excluir 2020. En el IPV, los intervalos conformes de MIDAS y del AR(4) cubren menos que su nivel nominal. Las cifras de Q10 no se citan. <!-- check:cifra-libre (id de pregunta, versión, AR(4) y año) -->
- **Datos.** Las series son revisadas, no en tiempo real.
- **Alcance de estos resultados.** H5, Q10 y las pruebas de V8 se refieren al agregado nacional trimestral. <!-- check:cifra-libre (nombres de versión) -->
- **Coherencia con la 1.0.** En la validación sellada de v6 (provincias que los modelos no vieron), el mejor modelo supera a la línea base más exigente en 6 de las 9 tareas. Tenía otro alcance: otro objetivo, otra escala y otra muestra que el agregado nacional trimestral de H5 y de V8. No contradice esa conclusión: en el agregado nacional ningún modelo gana al AR(4). <!-- check:cifra-libre (versiones, id de hipótesis y nueve tareas de la validación de v6) -->
- **Predicción no es identificación.** Las importancias de los modelos de predicción dicen qué variables ayudan a predecir, no qué pasaría si una variable cambiara.


## Anexos

Este bloque reúne los métodos, las pruebas superadas y fallidas por resultado, los pre-registros, las desviaciones y las licencias. Los anexos de erratas y de reproducibilidad van aparte.

### A. Métodos

Aquí se resume lo esencial. El detalle está en metodologia/ y en la ficha de cada cifra (metodologia/anexo_metodologico.md).

**Capas y escala de evidencia.** Cada cifra lleva una capa: [C1] hecho con al menos dos fuentes independientes; [C2] cota con supuestos explícitos; [C3] y [C3s] resultado con identificación; [C4] exploratorio o descriptivo. Una capa nunca sube. La escala de evidencia va de mayor a menor: identificación (C3 y C3s), asociación robusta, exploratorio, descriptivo. Todo V15 y V16 es [C4]. Definiciones en metodologia/capas.md. <!-- check:cifra-libre (nombres de capa y de versión) -->

**Pre-especificación.** Las especificaciones principales, el multiverso y las pruebas se fijan antes de estimar, en un pre-registro interno (apartado C). Ningún modelo se elige por su p-valor. Toda especificación probada va al registro del proyecto. Las desviaciones se anotan antes de ver el resultado afectado.

**Validación de herramientas por Monte Carlo.** Una herramienta de inferencia solo se usa si pasa la validación con el proceso generador del proyecto: pocos clusters, dependencia transversal, T corto, adopción escalonada y correlación espacial. Casi ninguna herramienta de inferencia la pasó. Los resultados están en metodologia/validacion_montecarlo_v16.md y metodologia/validacion_montecarlo_v15.md. <!-- check:cifra-libre (nombres de versión) -->

- **Utilizables en V16:** SDID con Conley-Taber en el escenario A (en el límite superior del tamaño); GSADF sobre el factor con bootstrap salvaje; Benjamini-Yekutieli en lugar del BH jerárquico; TOST solo cuando Δ/EE ≥ 2. <!-- check:cifra-libre (versión y umbral Δ/EE ≥ 2 del diseño) -->
- **Utilizables en V15:** SAR, SDM y SEM con Wald de ρ. <!-- check:cifra-libre (versión) -->
- **DM-HLN (estado único).** Apto bajo el proceso generador de V15 y no apto bajo el de V16. No se usa como prueba en ningún resultado. <!-- check:cifra-libre (nombres de versión) -->
- **No aptas, solo descriptivas:** CS con Webb, dCDH, rejilla TWFE, shift-share con AKM, DiD de intensidad, proyección local con Newey-West de ancho fijo, BLP/GATES, CIPS, CS-ARDL, bayesiano jerárquico, Honest DiD, control sintético, Westerlund y Clark-West.
- **Conley a dos kilómetros** pasó a no apto tras corregir un error en el núcleo (réplica ciega). Q3-b y H3 quedan solo con estimación puntual. <!-- check:cifra-libre (ids de resultado) -->
- Con una herramienta no apta, el resultado se da como estimación puntual, sin p ni intervalo.

**Control de falsos descubrimientos.** Benjamini-Yekutieli con q = 0,10 y denominador fijo por rama: 21 pruebas en la rama de diseños y 83 celdas en la rejilla. Las pruebas sin p válido cuentan en el denominador y no pueden rechazarse. Para las hipótesis de V15, Holm sobre la familia confirmatoria. Solo un p con q ≤ 0,10 abre la puerta a un hallazgo; además se exigen una magnitud plausible y la réplica en la muestra sellada. <!-- check:cifra-libre (q = 0,10, 21 y 83: números del diseño; versión) -->

**Comprobaciones de que el resultado es correcto.**
- Réplica ciega: otro analista reimplementa desde la ficha, sin leer el código. Si discrepa, no se publica hasta resolver. El cegado fue parcial (decisión K19): en varios lotes el replicador vio los valores publicados antes de estimar, y consta en cada resultado.json. <!-- check:cifra-libre (decisión K19) -->
- Abogado del diablo: tres revisiones de solo lectura intentan romper cada resultado citable. Cada objeción se corrige, se contrasta con datos o se declara como limitación (output/v16/critica/respuestas.md). <!-- check:cifra-libre (tres revisiones del diseño) -->
- Triangulación: comparación de signo con otros diseños y con la literatura. Ningún grupo de la literatura reúne estudios comparables para un metaanálisis. Las fichas llevan la etiqueta «DOI verificado; cuartil no verificado» y casi todas se leyeron en resumen.
- Detalle y resultados en el anexo de reproducibilidad.

**Muestras selladas.** Ninguna se ha abierto. Las evaluaciones de V15 se harán según su calendario, una vez por hipótesis y solo a través de src/holdout.py. evaluate_v16 no aplica: ninguna pregunta de V16 cumple las condiciones del hallazgo, así que V16 no tiene evaluación sellada pendiente. <!-- check:cifra-libre (nombre de versión y de fichero) -->

**Neutralidad.** Se evalúan afirmaciones e instrumentos con la misma vara. No se evalúan partidos ni personas.

### B. Pruebas superadas y fallidas por resultado

Todos los resultados de esta sección son [C4]. «Superada» y «fallida» se refieren a pruebas puntuales, porque casi ninguna herramienta de inferencia pasó el Monte Carlo. Una prueba «no evaluable» no cuenta como superada. El pre-registro de cada resultado es interno, sin sello de tiempo externo.

#### B.1 Resultados de V15 <!-- check:cifra-libre (nombre de versión) -->

##### H1 · Zonas tensionadas y renta de contratos nuevos <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la declaración de zona tensionada (Cataluña, Ley 12/2023) con la renta media de los contratos nuevos? <!-- check:cifra-libre (número de ley) --> |
| Diseño | Callaway-Sant'Anna y SDID por cohortes, estimación puntual. Incasòl trimestral, municipios, entrenamiento. |
| Capa | [C4], descriptivo. Pista solo en el signo, sin magnitud. |
| Superadas | El signo se mantiene al excluir Barcelona y el decil superior, y al excluir la capital de la provincia de Barcelona (CS y SDID). Soporte común de donantes suficiente. La réplica ciega coincide. |
| Fallidas o no evaluables | Pretendencias de CS. Contraste SDID de los dos últimos trimestres previos. Placebo temporal (CS y SDID). Control sintético de los diez mayores municipios, con mediana de signo contrario. Las cotas de Lee no permiten citar magnitud. Honest DiD, potencia de Roth, Webb y placebo SDID: no evaluables, por herramienta no apta. <!-- check:cifra-libre (diez municipios del diseño) --> |
| Pre-registro | Interno, sin sello de tiempo externo: etiqueta prereg-v15 en el remoto, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### H2 · Zonas tensionadas y número de contratos <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la declaración de zona tensionada con el número de contratos nuevos? |
| Diseño | PPML con efectos de municipio y trimestre, más CS y SDID sobre log(1+n) como robustez. Puntual. <!-- check:cifra-libre (log(1+n): fórmula de la transformación) --> |
| Capa | [C4], descriptivo. No se cita como pista. |
| Superadas | Contraste SDID de los dos últimos trimestres previos y placebo temporal de SDID, compatibles. Placebo espacial de CS, dentro de la escala permutada. |
| Fallidas o no evaluables | Pretendencias de CS y placebo temporal de CS. El rango del multiverso de CS incluye ambos signos. Ceros imputados. Sin inferencia válida. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### H3 · Vivienda turística y alquiler por sección <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | Dentro de cada sección, ¿se asocia el porcentaje de viviendas turísticas con el alquiler declarado (SERPAVI, stock de contratos)? |
| Diseño | MCO con efectos fijos de sección y de municipio × año. Exposición estandarizada por la desviación típica intra-sección. Puntual. |
| Capa | [C4], descriptivo. No concluyente, no nula. |
| Superadas | El signo se mantiene al excluir las grandes ciudades y el uno por ciento superior de exposición. La réplica ciega coincide. |
| Fallidas o no evaluables | Coeficiente principal (0,00 % por DT) por debajo del efecto mínimo detectable (0,10 % por DT). Mediana del multiverso: 0,07 % por DT (0,00-0,22 % por DT). Conley a dos kilómetros: no apto. Error agrupado por municipio en panel corto: sin validar. Placebo de adelanto sin inferencia válida. Muchas secciones sin variación intra-sección. Valor de Cinelli-Hazlett prácticamente nulo. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. Réplica, no confirmatoria. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### H4 · Inmigración y alquiler municipal <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la población extranjera predicha por cuotas de origen con el alquiler municipal? |
| Diseño | 2SLS shift-share (cuotas de 2003 × crecimiento nacional sin la provincia), efectos de provincia × año. Puntual. <!-- check:cifra-libre (año base del diseño) --> |
| Capa | [C4]. Correlación frágil: 0,30 % por punto porcentual. |
| Superadas | Primera etapa fuerte en términos descriptivos (F robusto 70,2). Balance de 2003 cercano a cero. El signo se mantiene al excluir Barcelona y València y el uno por ciento superior de exposición. La réplica ciega, tras corregir la muestra, coincide. <!-- check:cifra-libre (año) --> |
| Fallidas o no evaluables | Cambia de signo al quitar los cinco orígenes de mayor peso. Número efectivo de choques bajo (5,5). AKM, AKM0 y agrupación por provincia: no aptos. Con el control del instrumento retardado, la estimación cae a casi cero. Con 28 orígenes, el signo es contrario. Sin p ni intervalo. Mediana del multiverso: 0,08 % por punto porcentual [C4]. <!-- check:cifra-libre (número de orígenes del diseño) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### H5 · Predicción del valor tasado nacional <!-- check:cifra-libre (id de hipótesis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Predice la combinación el Δlog trimestral del valor tasado nacional mejor que el AR(4) y el ECM v1, en la misma muestra? <!-- check:cifra-libre (nombres de modelo) --> |
| Diseño | Ventana expansiva, h = 1. Combinación de DFM, BVAR, LASSO y ARDL. DM-HLN unilateral. <!-- check:cifra-libre (horizonte h = 1 del diseño) --> |
| Capa | [C4], predictivo. Pista: la combinación no supera al AR(4). <!-- check:cifra-libre (nombre de modelo) --> |
| Superadas | La réplica ciega, tras corregir tres errores, coincide en la conclusión. Ninguna fila posterior al origen entra en la estimación. En error cuadrático, la combinación queda por delante del ECM v1. <!-- check:cifra-libre (nombre de modelo y número de errores corregidos) --> |
| Fallidas o no evaluables | Razón del ECM frente al AR(4): mayor que uno en todas las implementaciones. Rango entre implementaciones (réplica ciega y producción pre-registrada): 1,2-1,5 razón [C4]. La pre-registrada: 1,5 [C4]. DM-HLN: 0,87 p; sin valor probatorio (estado en el apartado A). Clark-West y Giacomini-White: no aptos. MCS: descriptivo. Potencia inferior a la pre-registrada (menos errores). <!-- check:cifra-libre (nombres de modelo) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. Evaluación sellada hacia octubre de 2027. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### E1 · Largo plazo entre valor tasado y alquiler (panel provincial) <!-- check:cifra-libre (id de análisis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Hay una relación de largo plazo entre el valor tasado y el alquiler en las provincias de entrenamiento? |
| Diseño | ECM por unidad: CS-ARDL, MG y PMG. Todo puntual. |
| Capa | [C4], descriptivo. |
| Superadas | Ninguna prueba de inferencia aplicable. |
| Fallidas o no evaluables | Westerlund, CIPS y CS-ARDL: no aptos. PMG con coste de uso: no identificado. Elasticidad 0,64, con un rango del multiverso (-3,4 a 10,2 elasticidad) que cambia de signo. Semivida del desajuste: 4,0 años (3,5-4,2 años). La cointegración no se contrasta. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### E2 · Presión demográfica no cubierta por la obra y alquiler <!-- check:cifra-libre (id de análisis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia el exceso de hogares sobre la obra con el crecimiento del alquiler? |
| Diseño | Correlaciones de Pearson y Spearman, 24 especificaciones, provincias. <!-- check:cifra-libre (número de especificaciones del diseño) --> |
| Capa | [C4], descriptivo. |
| Superadas | El signo es positivo en todas las especificaciones con dato. |
| Fallidas o no evaluables | Sin intervalo ni herramienta de inferencia. Pocas provincias. Catastro municipal parcial. Regularización catastral previa a 2018. Demografía y población coinciden salvo por la escala. <!-- check:cifra-libre (año) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### E3 · Dependencia espacial del alquiler municipal <!-- check:cifra-libre (id de análisis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Hay dependencia espacial en el crecimiento del alquiler municipal (SERPAVI)? |
| Diseño | SAR, SEM y SDM por máxima verosimilitud, con W de contigüidad y de distancia inversa. |
| Capa | [C4], asociación espacial exploratoria. |
| Superadas | Wald de ρ: herramienta apta. Moran positivo en dos ventanas y con dos matrices W. El resultado se mantiene al excluir Barcelona y València. La réplica ciega coincide. ρ = 0,39, con rango de multiverso 0,24-0,64 ρ. |
| Fallidas o no evaluables | ρ puede recoger una tendencia regional común, no contagio. El intervalo subestima la incertidumbre de especificación; se cita el rango del multiverso. Selección de la muestra por vecinos. Los efectos indirectos del SDM dependen de W. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### E4 · Turismo con periodo previo y alquiler (Cataluña y Comunitat Valenciana) <!-- check:cifra-libre (id de análisis) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la exposición turística, con periodo previo, con el alquiler en un estudio de eventos de dosis continua? |
| Diseño | Efectos fijos de municipio y año, referencia 2017. Coeficientes puntuales. <!-- check:cifra-libre (año de referencia) --> |
| Capa | [C4], exploratorio. |
| Superadas | Regla puntual de pretendencias: la cumplen 6 de 16 especificaciones. |
| Fallidas o no evaluables | La incumplen las demás especificaciones. Honest DiD y potencia de Roth: no evaluables. La exposición del registro valenciano está reconstruida: solo robustez. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v15, commit 542b4fd, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

#### B.2 Resultados de V16 <!-- check:cifra-libre (nombre de versión) -->

V16 no añade hipótesis confirmatorias (desviación D1) y todo es [C4]. Pre-registro interno de V16, sin sello de tiempo externo: etiqueta prereg-v16 en el remoto, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (versión, desviación, etiqueta, hash y fecha) -->

##### Q1 · Zonas tensionadas (Q1a, Q1b, Q1c) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué diferencia hay, en el entrenamiento, entre mercados con y sin zona tensionada declarada? |
| Diseño | Q1a: recuento de elegibilidad (art. 18). Q1b: SDID con Conley-Taber. Q1c: Callaway-Sant'Anna sin regresores sobre compraventas provinciales. <!-- check:cifra-libre (ids de pregunta y artículo) --> |
| Capa | [C4], descriptivo. Sin hallazgo ni pista. Q1c no se cita con cifras. <!-- check:cifra-libre (id de pregunta) --> |
| Superadas | Q1c: el signo se mantiene al excluir las grandes ciudades. Valor de Cinelli-Hazlett por encima del umbral de fragilidad. Moran y Breusch-Pagan sin señal. <!-- check:cifra-libre (id de pregunta) --> |
| Fallidas o no evaluables | Q1b: sin periodo posterior al tratamiento (2025 es el primer inicio fuera de Cataluña) y sin potencia. Q1c: Oster indica fragilidad; el balance entre tratadas y no tratadas es muy desigual; Bai-Perron encuentra rupturas antes del primer tratamiento. CS con Webb y BLP/GATES: no aptos. Honest DiD y controles negativos: no evaluables. <!-- check:cifra-libre (ids de pregunta y año) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q2 · Vivienda turística (Q2a, Q2b, Q2c) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué asociación hay entre la exposición a vivienda turística y la evolución del alquiler? |
| Diseño | Q2a: DiD de intensidad provincial en forma reducida. Q2b: Andalucía, solo robustez. Q2c: IPVA municipal con efectos fijos de municipio y año (especificación de la adenda tras la corrección K17). <!-- check:cifra-libre (ids de pregunta y decisión) --> |
| Capa | [C4], descriptivo. Q2a, no concluyente. Q2c, de signo inestable y sin cita. <!-- check:cifra-libre (ids de pregunta) --> |
| Superadas | Q2a: Oster y Cinelli-Hazlett pasan; el signo se mantiene al excluir las grandes ciudades; Moran y Breusch-Pagan sin señal. Q2c: Cinelli-Hazlett pasa. <!-- check:cifra-libre (ids de pregunta) --> |
| Fallidas o no evaluables | Q2a: DiD de intensidad con Webb, no apto; Honest DiD, no evaluable; ruptura de Bai-Perron en la brecha entre terciles; shift-share retirado por falta de pernoctaciones por país. Q2c: Oster falla; heterocedasticidad; signo opuesto al de la literatura. BLP/GATES: no apto. <!-- check:cifra-libre (ids de pregunta) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q3 · Inmigración, más allá de H4 (Q3-c1, Q3-c2, Q3-b, BLP/GATES) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia la población extranjera con el valor tasado, las compraventas y el alquiler por sección? |
| Diseño | Shift-share de forma reducida en provincias (Q3-c) y correlación transversal por sección con efectos de municipio (Q3-b). Puntual. <!-- check:cifra-libre (ids de pregunta) --> |
| Capa | [C4]. Q3-b, correlación frágil: 0,01 (log por desviación típica). <!-- check:cifra-libre (id de pregunta) --> |
| Superadas | Q3-b: Oster y Cinelli-Hazlett no indican fragilidad; el signo se mantiene al excluir las grandes ciudades; la réplica ciega queda resuelta tras corregir Conley. Q3-c: mismo signo en todo el multiverso. <!-- check:cifra-libre (ids de pregunta) --> |
| Fallidas o no evaluables | Q3-b: pretendencia del mismo orden (0,01); Conley, no apto; Moran de residuos con señal; desequilibrio de renta. Q3-c: AKM y AKM0, no aptos; el origen de mayor peso aporta una fracción 0,48 del estimador; los signos de Q3-c1 y Q3-c2 son opuestos. BLP/GATES: no apto (0,00). Mediana del multiverso de Q3-b: 0,01 [C4]. <!-- check:cifra-libre (ids de pregunta) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q4 · Oferta y restricción física (Q4a, Q4b) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocia el porcentaje de Red Natura con la obra nueva neta, y con la respuesta del alquiler al choque de demanda de Q3? <!-- check:cifra-libre (id de pregunta) --> |
| Diseño | Q4a: MCO con efectos de provincia y año. Q4b: primeras diferencias con interacción choque × Red Natura. Puntual. <!-- check:cifra-libre (ids de pregunta) --> |
| Capa | [C4], descriptivo. Sin hallazgo. |
| Superadas | Q4a y Q4b: el signo se mantiene al excluir las grandes ciudades. Q4a: el signo se mantiene en el periodo de regularización catastral. <!-- check:cifra-libre (ids de pregunta) --> |
| Fallidas o no evaluables | Q4a: dependencia espacial fuerte en los residuos. Q4b: placebo de choque adelantado con el mismo signo y mayor tamaño. La Red Natura no es exógena. Agrupación provincial, no apta. Costa, pendiente, agua y planeamiento: sin datos. <!-- check:cifra-libre (ids de pregunta) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q5 · Sorpresas monetarias <!-- check:cifra-libre (id de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocian las sorpresas monetarias (Jarociński-Karadi) con el valor tasado y el IPC de alquiler a cuatro trimestres? |
| Diseño | Proyección local con cuatro rezagos. Puntual. |
| Capa | [C4], descriptivo. No se cita como pista. |
| Superadas | Ninguna prueba de inferencia aplicable. |
| Fallidas o no evaluables | Proyección local con Newey-West de ancho fijo, no apta. Autocorrelación de residuos. Primera etapa de signo equivocado. El multiverso no apoya el signo. El placebo es comparable y la respuesta cambia de signo. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q6 · Fiscalidad de la compra (Q6-v, Q6-p) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Se asocian los cambios del tipo general del ITP con las compraventas y el valor tasado? |
| Diseño | Wald-DID de de Chaisemartin-D'Haultfœuille con dosis continua, panel provincial anual. Solo puntual. Diferencias entre años consecutivos (corregido en la réplica ciega). |
| Capa | [C4]. Q6-p, no concluyente: -0,00 log por punto de tipo (-0,02 a 0,01 log por punto de tipo). Q6-v, descriptivo, sin cifra. <!-- check:cifra-libre (ids de pregunta) --> |
| Superadas | Q6-p: placebo de ΔY retardado pequeño y signo estable sin las grandes ciudades. Control negativo con la población, cercano a cero. <!-- check:cifra-libre (id de pregunta) --> |
| Fallidas o no evaluables | Q6-v: placebo mayor y de signo contrario; signo opuesto a la referencia. Los 14,0 cambios se concentran en 2012-2013. Inferencia por aleatorización, Honest DiD, Cinelli-Hazlett y TOST: no evaluables. Compraventas = total de vivienda. <!-- check:cifra-libre (id de pregunta y años) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q7 · Ayudas al alquiler joven <!-- check:cifra-libre (id de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Cambió en el corte de edad del bono la diferencia de alquiler pagado entre inquilinos de mercado, entre dos periodos? |
| Diseño | Diferencia en discontinuidades lineal local con pesos de la encuesta, anchos de tres, cinco y siete años. Sin intervalo. |
| Capa | [C4], descriptivo: -0,12 Δlog (-0,15 a -0,12 Δlog). Sin hallazgo ni pista. |
| Superadas | Los anchos de tres, cinco y siete años dan el mismo signo. |
| Fallidas o no evaluables | Los umbrales placebo dan resultados del mismo orden (-0,05 Δlog (-0,14 a -0,05 Δlog)), así que el resultado no se lee como específico del corte. Potencia en el límite. Sin intervalo (Kolesár-Rothe no mostrado). Edad discreta: sin rdrobust. El Plan Estatal 2018-2021 ya tenía un programa para menores de 35 años: se mide un cambio de generosidad, no un programa nuevo. Oster, Cinelli-Hazlett y exclusión de grandes ciudades: no aplican o no son evaluables. <!-- check:cifra-libre (periodo del plan y umbral de edad) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q8 · Compras de no residentes <!-- check:cifra-libre (id de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Cómo ha evolucionado la cuota de compras de no residentes antes y después de abril de 2025? |
| Diseño | Descriptivo: cuotas y niveles por trimestre y comparación de ventanas de cuatro trimestres. |
| Capa | [C4], descriptivo. Variación de la cuota: -1,3 puntos porcentuales. |
| Superadas | No hay contraste de hipótesis. La comparación con el año anterior se declara. |
| Fallidas o no evaluables | La fuente no separa UE de extra-UE. No identifica los visados de oro. Sin autorizaciones por programa. Sin placebo ni diferencias en diferencias. La cuota de Q8 (Boletín en línea, agregado de entrenamiento) difiere de la de R1A-H1 (tabla 1.6, España) por fuente y ventana. <!-- check:cifra-libre (id de resultado y tabla 1.6) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q9 · Fundamentales y burbuja (Q9-g, Q9-c) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Hay exuberancia en el factor común del cociente valor tasado / IPC de alquiler, y qué elasticidad de largo plazo hay entre ambos? |
| Diseño | Q9-g: GSADF con bootstrap salvaje. Q9-c: CS-ARDL, MG, PMG y CIPS, puntuales. <!-- check:cifra-libre (ids de pregunta) --> |
| Capa | [C4], pista no confirmada. Solo en la Parte VII. <!-- check:cifra-libre (número de parte) --> |
| Superadas | Calibración del GSADF del factor con bootstrap salvaje (tamaño aceptable). Réplica ciega: coincide. |
| Fallidas o no evaluables | Q9-g: estadístico 5,9; valor crítico del 95 % 3,3 estadístico. q de Benjamini-Yekutieli: 0,31, por encima del umbral. Heterocedasticidad de la variación del factor. Potencia limitada. Fechas marcadas en tramos en que el cociente baja o está plano. La alternativa con SERPAVI anual no rechaza y no tiene potencia. Q9-c: CS-ARDL no apto; el rango del multiverso incluye ambos signos (estimación 0,84, rango -1,4 a 0,95 elasticidad). CIPS: descriptivo, sin valor crítico. <!-- check:cifra-libre (ids de pregunta y nivel del 95 %) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Q10 · Predicción nacional (Q10-1, Q10-2, Q10-3) <!-- check:cifra-libre (ids de pregunta) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Mejoran MIDAS y el nowcasting al AR(4) y al ECM v1 en la predicción a un trimestre del IPV, del IPC de alquiler y de las compraventas? Alcance: agregado nacional trimestral. <!-- check:cifra-libre (nombres de modelo) --> |
| Diseño | Ventana expansiva. Razones de ECM. Intervalos conformes. |
| Capa | [C4], descriptivo. Las cifras de Q10 no se citan. <!-- check:cifra-libre (id de pregunta) --> |
| Superadas | Frente al ECM v1 reducido, el AR(4) es mejor en el IPV. Cobertura empírica de los intervalos conformes cercana a la nominal en el nowcasting del alquiler. <!-- check:cifra-libre (nombres de modelo) --> |
| Fallidas o no evaluables | Q10-1: MIDAS no mejora al AR(4). Q10-2: el nowcasting tampoco. Q10-3: la mejora aparente sale de 2020 y desaparece al excluirlo. DM-HLN: sin valor probatorio (estado en el apartado A). Clark-West: no apto. Datos revisados, no en tiempo real. <!-- check:cifra-libre (ids de pregunta, modelo y año) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Rejilla fija multiescala

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué asociación puntual hay en cada celda de la rejilla de escalas × resultados para Q1, Q2, Q3, Q4 y Q6? <!-- check:cifra-libre (ids de pregunta) --> |
| Diseño | 83 celdas, TWFE con efectos de unidad y periodo, cinco variantes por celda. Estimación puntual. <!-- check:cifra-libre (celdas del diseño) --> |
| Capa | [C4], descriptivo. Sin hallazgo local. |
| Superadas | Cada celda se estimó. El signo mediano se mantiene entre variantes. |
| Fallidas o no evaluables | TWFE, no apto (tamaño y cobertura fuera de rango): ninguna celda tiene p válido. Los diagnósticos de diseño no se ejecutan por celda. Cuentan en el denominador de Benjamini-Yekutieli y no pueden rechazarse. |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Control de falsos descubrimientos, triangulación y potencia (V16) <!-- check:cifra-libre (nombre de versión) -->

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué pruebas sobreviven al control, coinciden entre diseños y con la literatura, y con qué potencia se diseñaron? |
| Diseño | Benjamini-Yekutieli por rama. Comparación de signo entre diseños y con la literatura. Potencia por aleatorización placebo. |
| Capa | [C4], descriptivo. |
| Superadas | Solo una prueba de la rama de diseños tiene p válido (Q9-g). H1-CS y H1-SDID coinciden en signo, y H3 con Q2a. <!-- check:cifra-libre (ids de análisis) --> |
| Fallidas o no evaluables | Q9-g no pasa el control (0,31). Q2c y Q6-v se apartan de la literatura y quedan descriptivos. H4, Q3-c1 y Q3-b no tienen grupo comparable en la literatura. Ningún grupo permite metaanálisis. Ningún resultado sube de capa por coincidir con la literatura. <!-- check:cifra-libre (ids de análisis) --> |
| Pre-registro | Interno, sin sello de tiempo externo: prereg-v16, commit a8304ec, 2026-10-17. <!-- check:cifra-libre (etiqueta, hash y fecha) --> |

##### Fase de hechos y contabilidad (hechos, esfuerzo, contabilidad, atlas)

| Campo | Contenido |
|---|---|
| Pregunta | ¿Qué hechos se sostienen con dos fuentes independientes, y cómo se reparte contablemente el cambio de hogares, precio y esfuerzo? |
| Diseño | Cambios acumulados con media anual, coincidencia dentro de una tolerancia de tres puntos o del quince por ciento. Descomposiciones de Shapley, factores dinámicos, Oaxaca-Blinder, DFL y RIF. Atlas descriptivo con supresión de celdas pequeñas. |
| Capa | [C1] solo para tres cifras nuevas (precios 2019-2025 y brecha de alquiler en Cataluña); el resto, [C4]. Descriptivo. El IPV del INE (ajustado por calidad, una sola fuente) se da como [C4] junto a las medidas por m². <!-- check:cifra-libre (periodo y nombres de capa) --> |
| Superadas | Reproducen los controles de la 1.0. Identidad contable de hogares sin error. Esfuerzo de la ECV, compatible con el de Eurostat en los años recientes. |
| Fallidas o no evaluables | ECV y Eurostat son la misma encuesta: no hay [C1] en esfuerzo. Los años antiguos no coinciden con Eurostat. Intervalos aproximados. Vivienda pública por habitante frente a la UE: sin dato descargado. No hay contrastes de hipótesis: no aplica el control de falsos descubrimientos. <!-- check:cifra-libre (nombre de capa) --> |
| Pre-registro | No requiere pre-registro (hechos y contabilidad, sin estimar efectos). Para el resto de V16: interno, sin sello de tiempo externo (prereg-v16, commit a8304ec, 2026-10-17). <!-- check:cifra-libre (versión, etiqueta, hash y fecha) --> |

### C. Pre-registros de V15 y V16

Los dos son internos y no tienen sello de tiempo externo. Una etiqueta git publicada en el remoto no es un sello de tiempo externo. El plan inicial de depositar el pre-registro fuera se sustituyó por esta declaración: el proyecto registra `preregistro_tipo` como «interno, sin sello externo». <!-- check:cifra-libre (versión) -->

| Versión | Etiqueta en el remoto | Commit | Fecha del commit | Etiqueta publicada | Sello externo |
|---|---|---|---|---|---|
| V15 | prereg-v15 | 542b4fd | 2026-10-17 | 2026-10-17 | No | <!-- check:cifra-libre (etiquetas, hashes y fechas del registro de etiquetas) -->
| V16 | prereg-v16 | a8304ec | 2026-10-17 | 2026-10-17 | No | <!-- check:cifra-libre (etiquetas, hashes y fechas del registro de etiquetas) -->

Registro completo, con fechas en UTC y la huella de cada fichero: docs/preregistros.md y docs/preregistros_ficheros.csv. Las etiquetas de las versiones anteriores están en el mismo registro.

**Qué cubre cada uno.**
- **V15.** Cinco hipótesis (H1 a H5) y cuatro análisis exploratorios (E1 a E4). H1, H2 y H4 forman la familia Holm; H3 es una réplica; H5 es predictiva. Las hipótesis no se modifican ni se reformulan. Sus evaluaciones selladas están pendientes (calendario: docs/v15/preregistro_v15_adenda.md, sección C; fecha límite 31-12-2027). <!-- check:cifra-libre (ids de hipótesis y análisis, fecha límite) -->
- **V16.** Diez preguntas (Q1 a Q10) y una rejilla fija de 83 celdas. No añade hipótesis confirmatorias. Todo es [C4] como máximo. La adenda es vinculante. No tiene evaluación sellada pendiente: evaluate_v16 no aplica. <!-- check:cifra-libre (ids de pregunta, celdas y nombre de función) -->

**Desviaciones.** Se anotan antes de ver el resultado afectado. Se citan por su número, tal como figuran en el fichero de desviaciones.
- **V16** (metodologia/desviaciones_v16.md, D1 a D9): D1, sin preguntas confirmatorias nuevas; D2, operacionalización forzada por los datos en Q3, Q4 y Q6; D3, precisiones en Q1, Q2, Q7 y Q8; D4, Q5, Q9, Q10 y rejilla; D5, correcciones tras la réplica ciega; D6, correcciones tras la revisión adversarial; D7, Q6 con años consecutivos; D8, GSADF de V7.2 corregido y 4.999 simulaciones; D9, omisiones frente al plan: metaanálisis con Egger y PET-PEESE, modelo bayesiano jerárquico con priors de metaanálisis, GRF y DML, BH jerárquico sustituido por BY, y condición (b) de Gelman-Carlin. <!-- check:cifra-libre (ids de desviación D1 a D9, de pregunta y simulaciones) -->
- **V15** (docs/v15/desviaciones.md): DV15-A (H1, H2, H3, E4), DV15-B (H4, H5, E1, E2, E3) y DV15-K16 (correcciones tras la réplica ciega). <!-- check:cifra-libre (ids de desviación e hipótesis) -->
- **Versiones cerradas anteriores.** Cambios posteriores a algunos commits de pre-registro: metodologia/desviaciones_preregistros.md. Ninguno cambia una hipótesis ni una cifra de la 1.0. <!-- check:cifra-libre (versión) -->

### D. Licencias

No se inventa ninguna licencia: cada una se toma del registro de la fuente.

- **Qué se publica.** La carpeta publicacion/ la genera `make publicacion`; su inventario y las huellas de cada fichero están en publicacion/MANIFIESTO.md. Las series no redistribuibles no salen del repositorio de desarrollo. La capa pública de la base solo lleva datos redistribuibles.
- **Cifras de terceros de la 1.0.** publicacion/cifras_no_publicadas_1_0.csv recoge las cifras que no se publican, según proyecto.json (campo `terceros_1_0`). <!-- check:cifra-libre (versión) -->
- **Condiciones de uso de Registradores, Notariado y AEAT.** docs/v14/licencias.md, con las cláusulas literales y la clave CLARO, AMBIGUO o NO CONSTA. Es un informe, no una decisión. Atribución exigida para el conjunto abierto de Registradores (compraventas de uso residencial por provincia): Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. <!-- check:cifra-libre (versión de la licencia ODbL y de documento) -->
- **Fuentes nuevas de V16.** docs/v16/inventario_fuentes.csv recoge, por fichero, la edición, la licencia declarada por el proveedor, si es redistribuible (sí, no o dudoso), la huella sha256 y si está versionado. Lo marcado «dudoso» o «no» no se redistribuye. <!-- check:cifra-libre (versión) -->
- **Incasòl (fianzas).** Marcada como no redistribuible en las fuentes de las cifras de V9; solo se publican agregados propios. <!-- check:cifra-libre (versión) -->
- **Huellas de los datos de origen.** data/CHECKSUMS.sha256.
- **Literatura.** Las fichas de docs/v16/literatura.md llevan la etiqueta «DOI verificado; cuartil no verificado» (existe en Crossref o DataCite) o «NO VERIFICADA» (sin DOI localizado). Casi todas se leyeron en resumen o en versión de trabajo y son orientativas. <!-- check:cifra-libre (versión) -->


# Anexo · Erratas de la 1.0 corregidas en V16 <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

Fuente única: ERRATA.md, con los valores de antes y de después y la huella de cada fila cambiada de cifras_clave. Ninguna corrección sube una capa ni cambia la conclusión de fondo de la 1.0. Sí cambia una afirmación: la de que los niveles de precio y algunas series autonómicas eran «explosivos». <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

## La «exuberancia» del precio (GSADF), explicada sin tecnicismos

**Qué decía la 1.0.** <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
- Tras el ajuste por comparaciones múltiples, los niveles de precio nacionales (2 de 2 series) y 7 de las 34 series autonómicas eran «explosivos». <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
- Los cocientes entre el precio y sus fundamentales (renta, alquiler, tipos de interés) no lo eran.

**Por qué era incorrecto.** El programa tenía dos errores.
- **E1.** El contraste compara cada serie con miles de series simuladas sin burbuja. Para simularlas hay que elegir cuántos trimestres pasados se tienen en cuenta. La regla que lo elegía comparaba modelos estimados con distinto número de datos, y eso la sesgaba.
- **E2.** La serie del IPV de Navarra se cortaba en 2014, porque al programa le faltaba otra serie de Navarra en 2015-2018.

**Cómo se detectó.** En V16 se rehicieron las cifras de la 1.0 sin mirar el código original (réplica ciega). Al comparar, estas no coincidían, y la reconciliación encontró los dos errores. <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

**Qué da el cálculo corregido:**
- 0 series de niveles explosivas tras el ajuste;
- 0 series autonómicas;
- 0 cocientes nacionales.

También se aumentaron las simulaciones de 499 a 4.999, porque con 499 los recuentos cambiaban con la semilla. <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

**La conclusión de fondo no cambia.** Con estos contrastes no se puede afirmar que haya una burbuja ni que no la haya.
- Que no haya exuberancia estadística no demuestra que el precio esté alineado con sus fundamentales: el contraste tiene poca potencia con 78 trimestres. <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
- Que la hubiera tampoco identificaría una burbuja.

**El mismo error en v6.** Estaba también en una copia del código de v6. Corregido, el recuento de v6 sigue en 0 CCAA de 11 comunidades; solo cambian cuatro valores críticos. <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

## Resto de erratas aplicadas en V16

| Cifra o resultado | Qué estaba mal | Qué cambia |
|---|---|---|
| V8-M5, instrumento Bartik (8 filas de tablas_v8.xlsx) | Navarra y La Rioja entraban con cuota 0 por falta de datos de 2008 | Se excluyen; cambian solo esas 8 filas, ninguna cifra de cifras_clave | <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
| V8-H8-9 | Periodo mal rotulado | 2006T1-2026T2; el valor no cambia |
| V8-QNA-pp-c-P5 | Banda aproximada y media sin la mediana al lado | Banda exacta, mediana y sensibilidad al tipo del Banco de España |
| V8-VOTOS-c-P5 | Regla Y10 sin publicar | Publicada; el valor no cambia | <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
| V8-M1-cuota-c-P5 | Longitud del bloque no fijada en la ficha | Nota con el resultado alternativo; el valor no cambia |
| T4-H2 (mínimo) | Convención no escrita | Se documenta y se dan los dos mínimos; el valor no cambia |


# Anexo · Reproducibilidad: réplica ciega de la 1.0 y de los resultados de V15-V16 <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

## Réplica ciega de las cifras de la 1.0 (K19) <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

**Qué se hizo.** Se rehicieron las 31 cifras de la página resumen (una_pagina), entre ellas las 7 C1 vigentes. <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
- Cada una se reimplementó desde data/raw y su ficha metodológica, sin leer el código que la produjo (output/v16/replica/v10_*). <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
- El cegado fue parcial: en algunos lotes el replicador vio el valor publicado antes de estimar. Consta en cada resultado.json.

| Resultado | Cifras | Cuáles |
|---|---|---|
| Coinciden a la primera | 19 | Las 7 C1, E-T7 (2), L3 (2), E-B1-F, V10-ATL-A1, V72-GSADF-ccaa-v6, V72-GSADF-tipos-p05, V71-S3 (2), V8-OBS (2) | <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
| Coinciden tras completar la ficha (el original era correcto; faltaba un detalle por escribir) | 8 | T3-H5b, T4-H2, T4-H3, V71-S3-R6, V8-H8-9, V8-M1-cuota-c-P5, V8-QNA-pp-c-P5, V8-VOTOS-c-P5 | <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
| Discrepan por un error de código del original | 4 | V72-GSADF-ccaa-bh, -niveles-bh, -ratios-bh y -ratios-p05 | <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

**Errores encontrados y corregidos.** Valores de antes y de después en ERRATA.md y en el anexo de erratas.
- **GSADF de V7.2** (E1 y E2). El mismo E1 estaba en la copia de v6. Corregidos: los recuentos tras el ajuste de niveles y comunidades pasan a 0, y los de v6 no cambian. <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
- **V8-M5** (auditoría del alcance de los errores de V16). Navarra y La Rioja tenían cuota 0 en el instrumento Bartik y ahora quedan fuera. <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->

## Réplica ciega de los resultados citables de V15 y V16 (K16 y K18)

| Resultado | Hallazgo | Corrección |
|---|---|---|
| Q3-b | El núcleo de Conley contaba dos veces la diagonal | Corregido; Conley queda NO APTO en el Monte Carlo y Q3-b se cita solo como estimación puntual |
| H4 | Municipios sin población en el año base con instrumento 0, sin declararlo | Fuera de la muestra (N 13.442 → 13.417) | <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
| H5 | Primer origen desplazado, el AR(4) usaba el propio objetivo y la desestacionalización usaba datos posteriores al origen | Corregidos; la combinación sigue sin superar al AR(4) | <!-- check:cifra-libre (recuentos del proceso de réplica y de errata, no cifras de resultados) -->
| Q6-p | Diferencias entre años no consecutivos | Corregido; deja de ser pista y queda «no concluyente» |
| Q9-g, E3, H1, Q2a, H3 | Coinciden | — |

Ninguna corrección se eligió por su resultado: todas son errores frente a la ficha o frente a las reglas del proyecto.
