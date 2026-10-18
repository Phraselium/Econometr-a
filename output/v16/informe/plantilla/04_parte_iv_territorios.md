## Parte IV · Territorios

Esta parte presenta el atlas multiescala y lo que sobrevive a escala local. Todo es [C4]: descriptivo o exploratorio. Las frases describen coincidencias territoriales y no atribuyen causas. Las tablas largas no se copian aquí: están en las fichas territoriales de la web y en las descargas del atlas (`territorios.csv` y `territorios.parquet`).

### IV.1 Qué es el atlas y qué cubre

**Escalas.** España, CCAA, provincia, partido judicial, municipio, distrito y sección censal. No hay área urbana funcional: no existe correspondencia en la base geográfica del repositorio.

**Tamaño.** El atlas tiene {{V16-ATL-COB-FILAS:num}} filas en formato largo [C4]. Hay al menos un indicador publicado en {{V16-ATL-COB-MUNICIPIO:num}} municipios y en {{V16-ATL-COB-SECCION:num}} secciones censales [C4]. Hay alquiler SERPAVI publicable en {{V16-ATL-COB-ALQ-MUN:num}} municipios [C4] (al menos 10 contratos y CV de 30 % o menos). <!-- check:cifra-libre (umbrales de supresión del diseño) -->

**Qué amplía.** El atlas de V10 (coste por grupo social, València, Comunitat Valenciana y provincias) sigue vigente y no se repite. V16 añade renta ADRH 2015-2023 completa, turismo, parque, lanzamientos e intervenciones. <!-- check:cifra-libre (periodo; versiones V10 y V16) -->

**Unidades en blanco por validación sellada.** Las unidades de la muestra sellada (v6, V15 y V16) están en blanco por validación, no por falta de dato. No figuran con valor en el fichero ni en los mapas. Las ocho CCAA de la decisión K8 (Aragón, Asturias, Baleares, Canarias, Madrid, Murcia, Navarra y La Rioja) aparecen solo a escala de CCAA y nación. Nunca como provincia ni por debajo. Por eso un indicador provincial o municipal es, en este atlas, el de las unidades no selladas. <!-- check:cifra-libre (ocho CCAA del diseño; versiones) -->

**Supresión.** Se deja en blanco toda celda con menos de 10 unidades de base o con CV superior a 30 %. Afecta al {{V16-ATL-COB-SUPRIMIDAS}} [C4] de las filas. Los valores sustitutos de provincia o comarca de la ADRH no se muestran como municipales. <!-- check:cifra-libre (umbrales de supresión) -->

**Incertidumbre.** Hay intervalo al 95 % solo donde hay error de estimación: alquiler SERPAVI municipal y provincial, esfuerzo que propaga ese intervalo, y sobreesfuerzo de la ECV por CCAA. Los registros administrativos (ADRH, padrón, Censo 2021, CGPJ) no llevan intervalo y sí una marca de calidad. <!-- check:cifra-libre (nivel de confianza; Censo 2021) -->

### IV.2 Heterogeneidad entre territorios

Una media nacional esconde la dispersión. La tabla da el cociente entre el percentil 90 y el percentil 10 (P90/P10) de cada magnitud entre las unidades no selladas. Un cociente de 1 significa que no hay dispersión; cuanto mayor, más dispersión. <!-- check:cifra-libre (percentiles 90 y 10 y cociente de referencia 1, definición) -->

| Magnitud | Escala | Periodo | Cociente P90/P10 |
|---|---|---|---|
| Renta neta media del hogar (ADRH) | municipio | 2023 | {{V16-ATL-DISP-RENTA-HOGAR:num}} |
| Renta mediana por unidad de consumo (ADRH) | sección | 2023 | {{V16-ATL-DISP-RENTA-UC-SECCION:num}} |
| Alquiler mediano €/m² y mes (SERPAVI) | municipio | 2024 | {{V16-ATL-DISP-ALQUILER-M2:num}} |
| Ratio alquiler anual de 80 m² sobre renta del hogar | municipio | 2023 | {{V16-ATL-DISP-ESFUERZO:num}} |
| Misma ratio | sección | 2023 | {{V16-ATL-DISP-ESFUERZO-SECCION:num}} |
| Valor tasado €/m² | provincia | 2026T2 | {{V16-ATL-DISP-PRECIO-PROV:num}} |
| Sobreesfuerzo del 40 % (ECV) | CCAA | 2025 | {{V16-ATL-DISP-ECV40-CCAA:num}} |
| Viviendas no principales, % (Censo 2021) | municipio | 2021 | {{V16-ATL-DISP-NO-PRINCIPALES:num}} |
| Viviendas vacías por consumo eléctrico, % (Censo 2021) | municipio | 2021 | {{V16-ATL-DISP-VACIAS:num}} |
| Viviendas turísticas, % de las viviendas (INE VTE) | municipio | 2026-05 | {{V16-ATL-DISP-VT-PCT:num}} |
| Población de nacionalidad extranjera, % (censo anual) | municipio | 2025 | {{V16-ATL-DISP-EXTRANJERA:num}} |
| Lanzamientos por 10.000 viviendas, suma 2013-2024 | partido judicial | 2013-2024 | {{V16-ATL-DISP-LANZ-PJ:num}} |

<!-- check:cifra-libre (80 m², 40 %, 10.000 viviendas, periodos y escalas en la tabla) -->

**Lectura.**
- La renta tiene un cociente menor que las magnitudes de turismo, de población extranjera y de lanzamientos.
- Las viviendas turísticas se miden solo en los municipios con dato del INE; la cifra no es comparable con las de cobertura completa.
- El cociente de la ratio de esfuerzo en secciones ({{V16-ATL-DISP-ESFUERZO-SECCION:num}}) supera al de municipios ({{V16-ATL-DISP-ESFUERZO:num}}): dentro de un mismo municipio hay secciones más distintas entre sí que los municipios entre sí.
- Los mínimos y máximos de cada magnitud están en `output/v16/f2_atlas/hechos.json`.

### IV.3 Esfuerzo de alquiler por territorio

**Construcción.** La ratio es el alquiler anual de una vivienda tipo de 80 m² (mediana SERPAVI en €/m² y mes, tipología colectiva) sobre la renta neta media del hogar (ADRH), en el mismo año. Los 80 m² son un supuesto, no la superficie observada. SERPAVI mide contratos vigentes, no nuevos. La renta es la de todos los hogares de la unidad, no solo la de los inquilinos. **No es la tasa de sobreesfuerzo de la ECV** y no debe compararse con ella. <!-- check:cifra-libre (80 m²) -->

**Cobertura.** Hay ratio publicable en {{V16-ATL-COB-ESF-SECCION:num}} secciones censales en 2023 [C4].

**Provincias (1.0, V10).** El alquiler anual de 80 m² sobre la renta neta por persona tiene mediana y rango provincial {{V10-ATL-D1}} [C4]. Es otra definición de renta (por persona, no por hogar): no se mezcla con la ratio de arriba. <!-- check:cifra-libre (80 m², versiones) -->

**Municipios de la Comunitat Valenciana con 20.000 habitantes o más (V10).** La variación del alquiler mediano 2019-2024 tiene mediana y rango {{V10-ATL-D2}} [C4]. <!-- check:cifra-libre (umbral de población del diseño, periodo, versión V10) -->

**Ciudades comparables (V10), variación del alquiler mediano 2019-2024.**
- València: {{V10-ATL-E-46250}} [C4].
- Alicante/Alacant: {{V10-ATL-E-03014}} [C4].
- Málaga: {{V10-ATL-E-29067}} [C4].
- Palma: {{V10-ATL-E-07040}} [C4].
- Sevilla: {{V10-ATL-E-41091}} [C4].
- Zaragoza: {{V10-ATL-E-50297}} [C4].

Son contratos vigentes (SERPAVI). <!-- check:cifra-libre (periodo, versión V10) -->

### IV.4 Presión residencial y composición: ejemplos locales

- **València.** Población de nacionalidad extranjera: {{V10-ATL-C1}} [C4] en 2025 y {{V10-ATL-C2}} [C4] en 2021. Viviendas turísticas (INE, medición experimental): {{V10-ATL-C3}} [C4] en 2026-05. El índice descriptivo de presión residencial (puntuación z media 2019-2026) varía por barrio: por ejemplo, La Seu {{V10-ATL-C4-462500101}} [C4] y El Mercat {{V10-ATL-C4-462500105}} [C4]. Es un índice descriptivo, no una medida con intervalo. <!-- check:cifra-libre (años) -->
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
- **Resultado.** Las seis variantes pre-registradas dan el mismo signo. La principal es {{V16-Q3-b-beta:num}} y es la mayor de las variantes, no la mediana. Las variantes van de {{V16-Q3-b-beta:min}} a {{V16-Q3-b-beta:max}}, y su mediana es {{V16-Q3-b-mediana:num}} [C4] (unidad: log por desviación típica).
- **Limitaciones.**
  - La pretendencia (el mismo ajuste con la variación 2018-2021) da {{V16-Q3-b-pretendencia:num}} [C4]. Es más de la mitad del coeficiente principal. Una asociación previa a la exposición no se distingue de una tendencia anterior.
  - Puede haber reversión a la media o convergencia, y desbalance de renta.
  - La exposición de 2022 cae dentro de la ventana del resultado.
  - Hay un posible confusor turístico.
  - Sin intervalo: solo estimaciones puntuales.
  - Las unidades selladas están fuera de la muestra.
- **Lectura.** Correlación frágil. No se interpreta como efecto.

<!-- check:cifra-libre (seis variantes del diseño, años de ventana, «más de la mitad») -->

#### H4 (V15): población extranjera predicha y alquiler municipal. Correlación frágil

- **Qué es.** Asociación entre la variación de la población extranjera, predicha con un instrumento de tipo shift-share, y el alquiler municipal SERPAVI. Se lee como asociación descriptiva.
- **Resultado.** La estimación principal es {{V15-H4-beta:valor}} [C4]. El multiverso de 64 especificaciones va de {{V15-H4-beta:min}} a {{V15-H4-beta:max}}, e incluye el cero. Su mediana es {{V15-H4-mediana:valor}} [C4].
- **Limitaciones.**
  - La principal está en la cola alta del multiverso.
  - El signo cambia al quitar los cinco orígenes principales.
  - El número efectivo de choques es {{V15-H4-neff:num}} [C4]: pocos orígenes pesan en el resultado.
  - El F robusto de primera etapa ({{V15-H4-F:valor}} [C4]) es descriptivo.
  - El padrón por nacionalidad no recoge las nacionalizaciones.
  - La estimación 2SLS es varias veces la de mínimos cuadrados.
- **Estado.** Evaluación sellada pendiente.
- **Lectura.** Correlación frágil. Los dos diseños (Q3-b y H4) coinciden en el signo; eso no los convierte en un efecto.

<!-- check:cifra-libre (64 especificaciones del multiverso, cinco orígenes del diseño, 2SLS) -->

#### E3 (V15): correlación espacial del alquiler entre municipios vecinos

- **Qué es.** Un modelo autorregresivo espacial (SAR, contigüidad) sobre la variación del alquiler SERPAVI (tipología colectiva) 2015-2024 entre municipios.
- **Resultado.** El parámetro espacial ρ es {{V15-E3-rho:num}} [C4]. Va de {{V15-E3-rho:min}} a {{V15-E3-rho:max}} entre las especificaciones del multiverso.
- **Lectura.** Es una correlación espacial descriptiva. Los municipios vecinos tienden a moverse en el mismo sentido. No es contagio.
- **Limitaciones.** ρ puede reflejar una tendencia regional común. El intervalo subestima la incertidumbre de especificación. La muestra depende de los vecinos disponibles.
- **Estado.** Evaluación sellada pendiente.

<!-- check:cifra-libre (periodo) -->

#### H3 (V15): viviendas turísticas y alquiler por sección. No concluyente

- **Qué es.** Asociación entre la variación del alquiler SERPAVI (contratos vigentes) y la exposición turística intra-sección 2021-2024 (INE, medición experimental), con efectos de municipio por año.
- **Resultado.** No concluyente. La mediana del multiverso es {{V15-H3-rango:valor}} y el rango entre especificaciones, {{V15-H3-rango:rango}} [C4] (el rango no es un intervalo de confianza). Efecto mínimo detectable de referencia: {{V15-H3-mde:valor}} [C4]. Panel principal: {{V15-H3-n:num}} secciones [C4].
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
