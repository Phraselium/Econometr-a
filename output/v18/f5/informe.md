# V18 · Fase 5 · Magnitudes preferidas y contabilidad de la subida

**análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO; toda cifra es C4 y la clasificación V18 va al lado. Código: `src/v18/f5_magnitudes.py` y `src/v18/f5_contabilidad.py`; SEED 20261010, 10.000 extracciones; sin red.

## 1. Resumen

- **B5 (magnitud preferida).** La adenda 1.9 fija una estimación propia por factor. Solo **E2-R1** (Ley 11/2020, SUGESTIVO) tiene diseño válido y no es NO ESTIMABLE; E1, E3, E4, E5, E6, E7 y E9 salen NO ESTIMABLE y E8-R1 es ASOCIACIÓN (K7): no entran. E1-R4 y E3-R1 (NO CONCLUYENTE) no son las estimaciones designadas de su factor y están en otra unidad: se muestran al lado, sin combinar.
- **E2 no tiene magnitud preferida:** con el episodio catalán (E2-R1, Jofre-Monseny et al. y Monràs y García-Montalvo, ρ = 0,8, contado una vez), Breuille et al. y Hahn et al. la decisión no coincide en las tres priors (el intervalo de credibilidad al 95 % con la prior s/2 incluye el cero) y I² = 0,95 con un intervalo de predicción que cambia de signo (regla del plan). Se publica el rango de las tres priors: -0,122 a 0,003. La única magnitud con diseño propio es −0,038 (IC95 −0,051 a −0,026) en Cataluña, con la frase de limitación de la sección 2.
- **Magnitud preferida solo con literatura:** E1 (un estudio, Segú 2018), E4 (θ, dos estudios con error, efecto fijo con heterogeneidad) y E6 (un estudio, Mense 2025). E3 y E5 tienen 5 y 3 estudios en la unidad, pero I² > 75 % e intervalo de predicción que cambia de signo: rango sin magnitud preferida. E7, E8 y E9 no tienen ningún estudio con error típico en la unidad: rango de la literatura sin intervalo estadístico.
- **Contabilidad principal (adenda 1.10):** ningún factor tiene magnitud preferida construida con una estimación propia IDENTIFICADO o SUGESTIVO. Cada factor dice «sin magnitud» (no cero) y toda la variación observada queda en «no explicado» (100 %).
- **Ilustración con magnitudes de la literatura** (tabla aparte, rotulada así): no es una atribución. Sus resultados, con cualquier magnitud, dejan sin explicar la mayor parte de la variación en casi todos los periodos y territorios (secciones 4 y 5).

**Es contabilidad con elasticidades estimadas, no una descomposición estructural:** contribución = magnitud × variación observada del factor; sin interacciones ni efectos de equilibrio general, y los factores no son ortogonales.

## 2. Magnitud preferida por factor (B5)

| factor | magnitud preferida | intervalo | heterogeneidad | n estudios | origen (propia/literatura) | limitación |
|---|---|---|---|---|---|---|
| E1 | 0,038 | [0,015; 0,061] (IC95) | no estimable | 1 | magnitud solo de la literatura | magnitud de un solo estudio. un solo estudio en la unidad: sin heterogeneidad estimable |
| E2 | sin magnitud preferida | rango [-0,122; 0,003] | τ = 0,036; I² = 0,95 | 5 | propia + literatura | rango sin magnitud preferida (la decisión no coincide en las tres priors). herramienta meta_bayes NO APTO por conservadora (intervalos que cubren de más; el prior s/2 queda corto en calibración); episodio compartido con el original: cuenta una vez (rho = 0,8) |
| E3 | sin magnitud preferida | rango [-0,490; 3,515] | τ = 1,799; I² = 0,91 | 5 | magnitud solo de la literatura | rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo). herramienta meta_bayes NO APTO por conservadora (intervalos que cubren de más; el prior s/2 queda corto en calibración) |
| E4 | 0,041 | [-0,014; 0,095] (IC95) | I² = 0,53 (Q, K = 2) | 2 | magnitud solo de la literatura | magnitud preferida. con K = 2 el efecto fijo no cubre mu si hay heterogeneidad (cobertura 0,50-0,56 en el Monte Carlo) |
| E5 | sin magnitud preferida | rango [-0,202; 1,485] | τ = 0,461; I² = 0,95 | 3 | magnitud solo de la literatura | rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo). herramienta meta_bayes NO APTO por conservadora (intervalos que cubren de más; el prior s/2 queda corto en calibración) |
| E6 | -0,192 | [-0,319; -0,065] (IC95) | no estimable | 1 | magnitud solo de la literatura | magnitud de un solo estudio. un solo estudio en la unidad: sin heterogeneidad estimable |
| E7 | sin magnitud preferida | rango [-5,000; -2,000] | no estimable | 0 | sin magnitud (ni propia ni literatura comparable) | rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico). |
| E8 | sin magnitud preferida | rango [-3,500; -3,000] | no estimable | 0 | sin magnitud (ni propia ni literatura comparable) | rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico). |
| E9 | sin magnitud preferida | rango [1,400; 2,100] | no estimable | 0 | sin magnitud (ni propia ni literatura comparable) | rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico). |

Unidades: E1: Δln del alquiler por +1 pp de viviendas turísticas sobre el parque; E2: ATT en ln de la renta de los contratos regulados; E3: % de precio por +1 % de población por entrada de inmigrantes; E4: θ: euros de alquiler por euro de ayuda; E5: elasticidad precio de la oferta de unidades; E6: elasticidad del alquiler respecto a la oferta nueva (% por 1 %); E7: % del precio por +100 pb del tipo hipotecario, a 8 trimestres; E8: % de precio por +1 pp del ITP, a 12 meses; E9: % de precio por +1 pp de cuota de compras de no residentes.

**Advertencia del Monte Carlo (K5).** El metaanálisis bayesiano (herr18/meta_bayes) es NO APTO por conservador: con verdades fijas la cobertura de μ es 0,96-0,99 (intervalos que cubren de más), el prior s/2 queda corto en calibración (0,85-0,92) y, con K = 2, el efecto fijo cubre μ solo 0,50-0,56 si hay heterogeneidad. Los intervalos de las filas con K ≥ 3 son por tanto prudentes y los de las filas con K = 2 no deben leerse como IC95 fiables. La regla «la decisión debe coincidir en las tres priors» parte de intervalos conservadores.

### Estudios y estado de la ficha

| factor | estudio | estado de la ficha | valor | error típico | entra | etiqueta I6 | motivo si no entra |
|---|---|---|---|---|---|---|---|
| E1 | segu2018 | NO VERIFICADA | 0,038 | 0,012 | sí | referencia de I6 |  |
| E1 | garcialopez2020 | VERIFICADA | 0,022 | 0,011 | no | coherente con segu2018, razón 0.58 | unidad no convertible: por 100 anuncios en una BSA; la conversión a pp de viviendas exige las viviendas por BSA, que la ficha no da (plan, sección 3) |
| E1 | chavesfonseca2026 | VERIFICADA | 0,020 | 0,004 | no | coherente con segu2018, razón 0.53 | unidad no convertible (por 100 anuncios y sobre el precio de compra, no el alquiler) |
| E1 | duso2024 | VERIFICADA | — | — | no | no aplicable | unidad no convertible (€/m² por anuncio a 250 m) |
| E2 | jofremonseny2023 | VERIFICADA | -0,044 | 0,006 | sí | referencia de I6 |  |
| E2 | monras2023 | VERIFICADA | -0,058 | 0,014 | sí | coherente con jofremonseny2023, razón 1.29 |  |
| E2 | breuille2025 | NO VERIFICADA | -0,051 | 0,007 | sí | coherente con jofremonseny2023, razón 1.13 |  |
| E2 | hahn2021 | VERIFICADA | -0,113 | 0,019 | sí | coherente con jofremonseny2023, razón 2.51 |  |
| E2 | perezgarcia2026 | VERIFICADA | -0,030 | 0,011 | no | coherente con jofremonseny2023, razón 0.66 | otro régimen (zonas tensionadas de 2024) y otra unidad (puntos de crecimiento); sin pretendencias paralelas |
| E2 | abel2024 | NO VERIFICADA | — | — | no | no aplicable | otra variable (oferta) |
| E3 | gonzalez_ortega_2009_iza | NO VERIFICADA | 3,200 | 1,329 | sí | no coherente con gonzalez_ortega_2011_chicagofed, razón 3.34 |  |
| E3 | gonzalez_ortega_2011_chicagofed | NO VERIFICADA | 0,866 | 0,803 | no | referencia de I6 | versión del mismo trabajo que la de 2009 (mismo episodio y fuente): no cuenta dos veces; entra en la sensibilidad |
| E3 | sanchis_guarner_2017_lse | DISCREPANTE | 3,046 | 1,214 | sí | no coherente con gonzalez_ortega_2011_chicagofed, razón 3.18 |  |
| E3 | saiz_2007_philly | VERIFICADA | 1,607 | 0,326 | sí | coherente con gonzalez_ortega_2011_chicagofed, razón 1.68 |  |
| E3 | sa_2015_iza | VERIFICADA | -1,627 | 0,366 | sí | no coherente con gonzalez_ortega_2011_chicagofed, razón -1.70 |  |
| E3 | unal_2022_marburg | NO VERIFICADA | 2,689 | 0,648 | sí | coherente con gonzalez_ortega_2011_chicagofed, razón 2.80 |  |
| E3 | accetturo_2012_bdi | DISCREPANTE | 0,160 | 0,053 | no | no coherente con gonzalez_ortega_2011_chicagofed, razón 0.17 | elasticidad log-log respecto a la población extranjera dentro de la ciudad, no a la población total: unidad no convertible |
| E3 | torres_montero_2023_cytet | VERIFICADA | -0,950 | — | no | no coherente con gonzalez_ortega_2011_chicagofed, razón -0.99 | sin error típico en la ficha |
| E4 | fack_2005_cepremap | VERIFICADA | 0,390 | 0,240 | sí | no aplicable |  |
| E4 | eerola_etal_2026_jpube | VERIFICADA | 0,036 | 0,028 | sí | no aplicable |  |
| E4 | kangasharju_2008_vatt458 | VERIFICADA | 0,570 | — | no | no aplicable | sin error típico en la ficha |
| E4 | hyslop_rea_2018_motu | VERIFICADA | 0,360 | — | no | no aplicable | sin error típico en la ficha |
| E5 | taltavull_2006_funcas | NO VERIFICADA | 0,870 | 0,125 | sí | referencia de I6 |  |
| E5 | baum_snow_han_2020_nberconf | DISCREPANTE | 0,260 | 0,110 | sí | no coherente con taltavull_2006_funcas, razón 0.30 |  |
| E5 | paciorek_2012_feds | VERIFICADA | 0,840 | 0,100 | sí | coherente con taltavull_2006_funcas, razón 0.97 |  |
| E6 | mense_2025_jpemacro | VERIFICADA | -0,192 | 0,065 | sí | referencia de I6 |  |
| E6 | asquith_mast_reed_2020_philly | DISCREPANTE | -0,062 | 0,037 | no | no coherente con mense_2025_jpemacro, razón 0.32 | otra unidad (Δln del alquiler cerca de un edificio, no elasticidad respecto a la oferta): no se combina con Mense (plan, sección 3) |
| E7 | sanjuan_2023_bde_be2302art09 | VERIFICADA | -2,000 | — | no | referencia de I6 | intervalos al 68 % solo en un gráfico: sin error típico numérico |
| E7 | bce_eb_2022_6_battistini_gareis_roma | NO VERIFICADA | -5,000 | — | no | coherente con sanjuan_2023_bde_be2302art09, razón 2.50 | sin error típico (el plan lo deja fuera del metaanálisis y al lado) |
| E8 | dolls_etal_2020_vfs | VERIFICADA | -3,000 | — | no | referencia de I6 | sin error típico recuperado |
| E9 | sa_2016_lse_cfm2016_39 | VERIFICADA | 2,000 | — | no | referencia de I6 | sin error típico extraído |
| E9 | alvarez_blanco_garciaposada_2020_bde_be2002art14 | NO VERIFICADA | 2,550 | 2,260 | no | coherente con sa_2016_lse_cfm2016_39, razón 1.27 | MCO transversal sin instrumento: asociación (el plan no admite asociaciones); se muestra al lado |
| E2 | E2-R1 | estimación propia V18 (SUGESTIVO) | -0,038 | 0,006 | sí | coherente con jofremonseny2023, razón 0.85 |  |

El estado es el de `docs/v18/bib` según el verificador de DOI (VERIFICADA, NO VERIFICADA, DISCREPANTE por versión de trabajo frente a publicada); el cuartil Scimago no está verificado. Todas las referencias de B5 y de I6 llevan su estado (adenda 1.9, R-26). Las cifras con «solo resumen» no se han leído en texto completo.

### Episodios compartidos y sensibilidad

- **E2:** la estimación propia, Jofre-Monseny et al. (2023) y Monràs y García-Montalvo (2023) usan el mismo registro (Incasòl) y el mismo episodio: entran como un solo episodio, combinados con ρ = 0,8 por mínima varianza con pesos no negativos. Con ρ = 0,8 los pesos son 0,325 (E2-R1), 0,675 (Jofre-Monseny) y 0 (Monràs); con ρ = 1 se queda con la más precisa.
- **E3:** González y Ortega (2009, IZA; 2011, Chicago Fed; 2013, J. Regional Science) son versiones del mismo trabajo: cuentan una vez (versión de 2009, que es la que da «% por 1 %»; su error se reconstruye por proporcionalidad con el de €/m²).
- **E9 frente a E3 (sin doble cómputo):** ambos usan cuotas del padrón por nacionalidad; la correlación entre el índice de exposición de E9 (cuotas de 2003 de los orígenes con riesgo) y el instrumento medio de E3-R1 es 0,85 (output/v18/estimacion/e9/informe.md). No se suman: la principal usa E3 y E9 va como alternativa.

| factor | variante | K | estado | μ o media | lo | hi | I² | notas |
|---|---|---|---|---|---|---|---|---|
| E1 | sin_I6 | 1 | magnitud preferida | 0,038 | 0,015 | 0,061 |  |  |
| E2 | rho_0.5 | 3 | rango sin magnitud preferida (la decisión no coincide en las tres priors) | -0,060 | -0,113 | -0,005 | 0.95 |  |
| E2 | rho_1 | 3 | rango sin magnitud preferida (la decisión no coincide en las tres priors) | -0,061 | -0,113 | -0,007 | 0.95 |  |
| E2 | sin_I6 | 3 | rango sin magnitud preferida (la decisión no coincide en las tres priors) | -0,060 | -0,113 | -0,005 | 0.95 |  |
| E2 | hahn_estrategia_B | 3 | magnitud preferida | -0,049 | -0,084 | -0,018 | 0.7 |  |
| E2 | sin_estimacion_propia | 3 | rango sin magnitud preferida (la decisión no coincide en las tres priors) | -0,061 | -0,113 | -0,007 | 0.95 |  |
| E2 | solo_europeos | 3 | rango sin magnitud preferida (la decisión no coincide en las tres priors) | -0,060 | -0,113 | -0,005 | 0.95 |  |
| E3 | sin_I6 | 2 | magnitud preferida | 1,825 | 1,255 | 2,396 | 0.55 | gonzalez_ortega_2009_iza fuera de I6 (razón 3.34); sanchis_guarner_2017_lse fuera de I6 (razón 3.18); sa_2015_iza fuera de I6 (razón -1.70) |
| E3 | version_2011_en_lugar_de_2009 | 5 | rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo) | 1,076 | -0,628 | 2,793 | 0.91 |  |
| E3 | solo_europeos | 4 | rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo) | 1,364 | -0,791 | 3,535 | 0.88 |  |
| E3 | solo_espana | 2 | magnitud preferida | 3,116 | 1,359 | 4,873 | 0.0 |  |
| E4 | sin_I6 | 2 | magnitud preferida | 0,041 | -0,014 | 0,095 | 0.53 |  |
| E5 | sin_I6 | 2 | magnitud preferida | 0,852 | 0,699 | 1,005 | 0.0 | baum_snow_han_2020_nberconf fuera de I6 (razón 0.30) |
| E6 | sin_I6 | 1 | magnitud preferida | -0,192 | -0,319 | -0,065 |  |  |
| E7 | sin_I6 | 0 | sin estudios | — | — | — |  |  |
| E8 | sin_I6 | 0 | sin estudios | — | — | — |  |  |
| E9 | sin_I6 | 0 | sin estudios | — | — | — |  |  |

**La estimación propia de E2 (K9), con su frase de limitación obligatoria al difundir la cifra:** «Entre 2020T4 y 2022T1, la renta media de los contratos nuevos registrados en el Incasòl en los 49 municipios sujetos a la Ley 11/2020 (sin Barcelona ciudad) se situó, respecto a 2019, un 3,8 % por debajo (log −0,038; IC95 −0,051 a −0,026) de la de municipios catalanes no regulados con mercado tensionado. La diferencia no es estable: es máxima en 2021T1 (−0,058), se reduce de forma gradual hasta no distinguirse de cero en 2022T1, antes de la STC 37/2022, sin cambio posterior, y baja a −0,023 (IC95 −0,045 a −0,001) cuando se permiten trayectorias trimestrales distintas según el tamaño del municipio. Con estos datos no se separa la parte asociada a la norma de un choque transitorio de la COVID-19 en los municipios grandes ni de un cambio en la composición de los contratos registrados, y la sensibilidad a tendencias diferenciales (Honest DiD con M̄ ≥ 0,5) no es evaluable con la potencia disponible. La magnitud coincide con la de Jofre-Monseny et al. (2023), que usan el mismo registro y el mismo episodio. Clase V18: SUGESTIVO; capa del proyecto C4.»

## 3. Contabilidad principal (adenda 1.10)

La adenda 1.10 deroga el filtro «al menos una estimación IDENTIFICADO o SUGESTIVO» y manda usar «todo factor con magnitud preferida de B5, construida con las reglas de 1.9», con la clase de su estimación propia como techo de la confianza y «sin magnitud» (no cero) para el resto. Lectura aplicada: el plan (sección 4) deja las magnitudes «solo literatura» en una tabla secundaria rotulada; la adenda no lo revoca, y una magnitud sin estimación propia no tiene clase que ponga techo a la confianza. Por eso la tabla principal solo admitiría factores con estimación propia dentro de B5, y ninguno lo cumple: **la contabilidad principal no tiene filas con cifra.** Se dice así y todo se deja en «no explicado»; la ilustración va aparte (sección 4).

| periodo | Δ precio real (pp) | Δ alquiler real (pp) | no explicado |
|---|---|---|---|
| 1995T1-2007T4 | 69,0 | 1,8 | 100 % (sin magnitud en ningún factor) |
| 2008T1-2013T4 | -36,6 | 6,6 | 100 % (sin magnitud en ningún factor) |
| 2014T1-2019T4 | 6,3 | -2,9 | 100 % (sin magnitud en ningún factor) |
| 2020T1-2022T2 | -1,0 | -3,8 | 100 % (sin magnitud en ningún factor) |
| 2022T3-2026T2 | 14,9 | -6,4 | 100 % (sin magnitud en ningún factor) |

Δ observada = 100·Δln del valor tasado (MIVAU) o del IPC de alquiler, menos el deflactor del PIB del INE (base:deflactor): difiere del IPC general que usó V8, por lo que las cifras de variación observada no coinciden con las de V8 (P4 y P5 sobre todo). El alquiler de 1995-2007 solo existe desde 2002T1. Las tablas provinciales y de CCAA (en `contabilidad.csv`) son **relativas a la media de las provincias no selladas** y no suman el total nacional. Cantabria no tiene serie provincial de valor tasado en la base (38 provincias con dato, no 39) y su CCAA queda fuera. 11 provincias selladas (v6) y los municipios de V15 y V16 se excluyen.

## 4. Ilustración con magnitudes de la literatura (no es una atribución)

Magnitud: rango uniforme entre los estudios (E3, E7, E8, E9; sin intervalo estadístico), efecto fijo o estudio único (E1) y, para Cataluña, E2-R1 propia sola. Variación observada del factor sin error (una sola fuente). Los factores de unidad no comparable con la contabilidad (E5: elasticidad de la oferta al precio; E6: oferta nueva local de Mense; E4: sin variación medida) no tienen fila. Tipos (E7): solo cuenta el cambio de los últimos 8 trimestres del periodo; lo anterior es «fuera del horizonte estimado», sin cifra. Todas las filas de panel (E1, E2, E3, E8, E9) llevan el rótulo «relativa entre provincias (o unidades), sin el componente común»; solo E7 incluye el componente común. La fila nacional de esos factores usa la variación absoluta e incluye las 11 provincias selladas; se contrasta con el soporte (percentiles 5-95 de la variación provincial) y, si queda fuera, no lleva cifra.

### Nacional, precio real de compra (periodos del plan)

| periodo | factor | variación del factor | mediana (pp) | p16 | p84 | % de la Δ obs. | Δ obs. (pp) | soporte |
|---|---|---|---|---|---|---|---|---|
| 1995T1-2007T4 | E3 | 8,2 | 6,9 | -6,7 | 20,0 | 9,9 | 69,0 | dentro del soporte |
| 1995T1-2007T4 | E7 | 2,3 | — | — | — | — | 69,0 | fuera del soporte |
| 1995T1-2007T4 | NOEXPL | — | 62,1 | 49,0 | 75,7 | 90,1 | 69,0 |  |
| 2008T1-2013T4 | E3 | -0,9 | -0,8 | -2,2 | 0,7 | 2,1 | -36,6 | dentro del soporte |
| 2008T1-2013T4 | E9 | 6,4 | 11,2 | 9,7 | 12,7 | -30,5 | -36,6 | dentro del soporte |
| 2008T1-2013T4 | E7 | -0,3 | 1,1 | 0,8 | 1,5 | -3,1 | -36,6 | dentro del soporte |
| 2008T1-2013T4 | NOEXPL | — | -37,0 | -38,5 | -35,6 | 101,1 | -36,6 |  |
| 2008T1-2013T4 | NOEXPL_alt_E9 | — | -49,0 | -50,5 | -47,5 | 133,6 | -36,6 |  |
| 2014T1-2019T4 | E3 | 1,2 | 1,0 | -1,0 | 3,0 | 16,1 | 6,3 | dentro del soporte |
| 2014T1-2019T4 | E9 | -2,4 | -4,2 | -4,8 | -3,7 | -66,7 | 6,3 | dentro del soporte |
| 2014T1-2019T4 | E7 | -0,1 | 0,4 | 0,2 | 0,5 | 5,5 | 6,3 | dentro del soporte |
| 2014T1-2019T4 | NOEXPL | — | 5,0 | 3,0 | 7,0 | 78,4 | 6,3 |  |
| 2014T1-2019T4 | NOEXPL_alt_E9 | — | 10,2 | 9,7 | 10,8 | 161,2 | 6,3 |  |
| 2020T1-2022T2 | E3 | 0,6 | 0,5 | -0,5 | 1,4 | -45,4 | -1,0 | dentro del soporte |
| 2020T1-2022T2 | E9 | 1,1 | — | — | — | — | -1,0 | fuera del soporte |
| 2020T1-2022T2 | E7 | -0,1 | 0,3 | 0,2 | 0,4 | -31,2 | -1,0 | dentro del soporte |
| 2020T1-2022T2 | NOEXPL | — | -1,9 | -2,8 | -0,9 | 176,7 | -1,0 |  |
| 2020T1-2022T2 | NOEXPL_alt_E9 | — | -1,4 | -1,5 | -1,3 | 131,2 | -1,0 |  |
| 2022T3-2026T2 | E3 | 2,1 | 1,8 | -1,7 | 5,1 | 11,8 | 14,9 | dentro del soporte |
| 2022T3-2026T2 | E9 | -1,9 | -3,3 | -3,8 | -2,9 | -22,3 | 14,9 | dentro del soporte |
| 2022T3-2026T2 | E7 | -0,8 | 2,9 | 2,0 | 3,7 | 19,5 | 14,9 | dentro del soporte |
| 2022T3-2026T2 | NOEXPL | — | 10,2 | 6,9 | 13,8 | 68,7 | 14,9 |  |
| 2022T3-2026T2 | NOEXPL_alt_E9 | — | 15,3 | 14,4 | 16,2 | 102,9 | 14,9 |  |

E9 es la alternativa de E3 (no se suman): la fila `NOEXPL_alt_E9` de `contabilidad_ilustracion.csv` da el no explicado cuando E9 sustituye a E3. Intervalos al 68 % (p16-p84); al 90 % están en el CSV (p05, p95).

### Cataluña (E2-R1 propia sola) y Barcelona (E1)

| periodo | territorio | factor | fila | variación | mediana (pp) | p16 | p84 | Δ obs. (pp) |
|---|---|---|---|---|---|---|---|---|
| 2020T1-2022T2 | Cataluña (sin Barcelona ciudad) | E2 | factor_extremos | 0,00 | 0,00 | 0,00 | 0,00 | -2,81 |
| 2020T1-2022T2 | Cataluña (sin Barcelona ciudad) | NOEXPL | no_explicado | — | -2,81 | -2,81 | -2,81 | -2,81 |
| 2020T1-2022T2 | Cataluña (sin Barcelona ciudad) | E2 | factor_vigencia | 0,71 | -2,71 | -3,17 | -2,26 | -2,81 |
| 2020T1-2022T2 | provincia 08 (sin Barcelona ciudad) | E2 | factor_extremos | 0,00 | 0,00 | 0,00 | 0,00 | -4,04 |
| 2020T1-2022T2 | provincia 08 (sin Barcelona ciudad) | NOEXPL | no_explicado | — | -4,04 | -4,04 | -4,04 | -4,04 |
| 2020T1-2022T2 | provincia 08 (sin Barcelona ciudad) | E2 | factor_vigencia | 0,78 | -2,98 | -3,48 | -2,48 | -4,04 |
| 2020T1-2022T2 | provincia 17 (sin Barcelona ciudad) | E2 | factor_extremos | 0,00 | 0,00 | 0,00 | 0,00 | 0,45 |
| 2020T1-2022T2 | provincia 17 (sin Barcelona ciudad) | NOEXPL | no_explicado | — | 0,45 | 0,45 | 0,45 | 0,45 |
| 2020T1-2022T2 | provincia 17 (sin Barcelona ciudad) | E2 | factor_vigencia | 0,53 | -2,04 | -2,38 | -1,70 | 0,45 |
| 2020T1-2022T2 | provincia 25 (sin Barcelona ciudad) | E2 | factor_extremos | 0,00 | 0,00 | 0,00 | 0,00 | -2,41 |
| 2020T1-2022T2 | provincia 25 (sin Barcelona ciudad) | NOEXPL | no_explicado | — | -2,41 | -2,41 | -2,41 | -2,41 |
| 2020T1-2022T2 | provincia 25 (sin Barcelona ciudad) | E2 | factor_vigencia | 0,65 | -2,48 | -2,91 | -2,07 | -2,41 |
| 2020T1-2022T2 | provincia 43 (sin Barcelona ciudad) | E2 | factor_extremos | 0,00 | 0,00 | 0,00 | 0,00 | 0,89 |
| 2020T1-2022T2 | provincia 43 (sin Barcelona ciudad) | NOEXPL | no_explicado | — | 0,89 | 0,89 | 0,89 | 0,89 |
| 2020T1-2022T2 | provincia 43 (sin Barcelona ciudad) | E2 | factor_vigencia | 0,61 | -2,35 | -2,75 | -1,96 | 0,89 |
| 2022T3-2026T2 | Cataluña (sin Barcelona ciudad) | E2 | factor_sin_magnitud | — | — | — | — | -1,81 |
| 2022T3-2026T2 | provincia 08 (sin Barcelona ciudad) | E2 | factor_sin_magnitud | — | — | — | — | 0,82 |
| 2022T3-2026T2 | provincia 17 (sin Barcelona ciudad) | E2 | factor_sin_magnitud | — | — | — | — | -1,56 |
| 2022T3-2026T2 | provincia 25 (sin Barcelona ciudad) | E2 | factor_sin_magnitud | — | — | — | — | -0,48 |
| 2022T3-2026T2 | provincia 43 (sin Barcelona ciudad) | E2 | factor_sin_magnitud | — | — | — | — | -4,14 |
| 2020T1-2022T2 | Barcelona | E1 | factor | -0,02 | -0,08 | -0,11 | -0,06 | -6,13 |
| 2020T1-2022T2 | Barcelona | NOEXPL | no_explicado | — | -6,05 | -6,07 | -6,02 | -6,13 |
| 2022T3-2026T2 | Barcelona | E1 | factor | 0,13 | 0,50 | 0,34 | 0,65 | -2,09 |
| 2022T3-2026T2 | Barcelona | NOEXPL | no_explicado | — | -2,58 | -2,74 | -2,43 | -2,09 |

En 2020T1-2022T2 el régimen de la Ley 11/2020 no estaba vigente al final (STC 37/2022; reversión estimada −0,0016): la variación entre extremos del factor es 0 y su contribución a la variación del periodo es 0; durante la vigencia (2020T4-2022T1) el nivel medio de la renta de los contratos nuevos fue −2,7 pp menor en Cataluña por la cuota de contratos regulados (mediana; la cifra requiere la frase de limitación de la sección 2). La renta observada es la de contratos nuevos del Incasòl (sin Barcelona ciudad), no el IPC. Barcelona ciudad no estaba en la muestra de E2-R1 (criterio de Jofre-Monseny et al.) y no lleva cifra de E2; su cifra de E1 mide viviendas HUT por 100 viviendas con una magnitud definida por anuncios de Airbnb. En 2022T3-2026T2 la zona tensionada de 2024 es otro régimen: sin magnitud.

## 5. Respuesta por periodo y territorio

Descripción sin interpretación de efectos: lo que sigue indica cuánta de la variación observada se asocia en la ilustración con cada factor y cuánta queda sin explicar. La confianza usa la escala del Banco de España (V17) y no supera la clase del factor de menor nivel que la sostiene: sin estimación propia estimable, «la evidencia no permite concluir»; E2 en Cataluña, «la evidencia sugiere» (SUGESTIVO).

| periodo | Δ obs. (pp) | factor con mayor contribución | mediana (pp) | % de la Δ | no explicado (principal, %) | no explicado (ilustración, %) | no explicado (E9 en lugar de E3, %) | confianza |
|---|---|---|---|---|---|---|---|---|
| 1995T1-2007T4 | 69,0 | E3 | 6,9 | 9,9 | 100,0 | 90,1 | — | la evidencia no permite concluir (sin estimación propia estimable; magnitud solo de la literatura) |
| 2008T1-2013T4 | -36,6 | E7 | 1,1 | -3,1 | 100,0 | 101,1 | 133,6 | la evidencia no permite concluir (sin estimación propia estimable; magnitud solo de la literatura) |
| 2014T1-2019T4 | 6,3 | E3 | 1,0 | 16,1 | 100,0 | 78,4 | 161,2 | la evidencia no permite concluir (sin estimación propia estimable; magnitud solo de la literatura) |
| 2020T1-2022T2 | -1,0 | E3 | 0,5 | -45,4 | 100,0 | 176,7 | 131,2 | la evidencia no permite concluir (sin estimación propia estimable; magnitud solo de la literatura) |
| 2022T3-2026T2 | 14,9 | E7 | 2,9 | 19,5 | 100,0 | 68,7 | 102,9 | la evidencia no permite concluir (sin estimación propia estimable; magnitud solo de la literatura) |

Por CCAA (8 con dato; tabla completa en `respuesta.csv`): en la ilustración la mediana del porcentaje que queda sin explicar es 84 % (valor absoluto, relativo al componente común); el factor con mayor contribución es E8 en 28 de 40 combinaciones de CCAA y periodo.
**Respuesta corta.** Con los criterios de la adenda no hay ningún factor que explique la mayor parte de la variación en ningún periodo ni territorio con respaldo propio: la contabilidad principal deja el 100 % sin explicar. Con magnitudes de la literatura, las contribuciones nacionales con cifra que superan el 50 % de la variación observada (en valor absoluto) son: E9 en 2014T1-2019T4 (-67 %, mediana -4,2 pp frente a una variación de 6,3 pp). La de E9 tiene signo opuesto al de la variación observada, procede de un rango de otro país sin error típico y no se suma a E3. Qué queda sin explicar: la parte común a todas las provincias (el componente común, no identificable con diseños de panel con efectos de periodo) y la variación de los fundamentales no medidos aquí (renta y crédito: F1 es ASOCIACIÓN y no entra).

**Sensibilidad de E2.** Con la estrategia B de Hahn et al. (−0,075 en lugar de −0,113; la A se fijó antes de combinar, por ser la primera de la ficha) el metaanálisis sí daría magnitud preferida: -0,049 [-0.0835; -0.0179], I² = 0.7. Se publica como sensibilidad; no cambia la tabla principal, porque la regla se fijó antes. Si se adoptara, E2 entraría en la contabilidad con clase SUGESTIVO como techo, pero su variación entre extremos del periodo 2020-2022 sería 0 (la norma no estaba vigente al final del periodo).

## 6. Comparación con V8 y con el Banco de España (sin sumar)

**V8 (descomposición histórica del SVAR, C3s, bandas del 68 %).** V8 no designó ningún factor como el más relevante en ninguno de los diez casos. Correspondencias: demográfico ↔ inmigración (E3, E9); crédito y tipos ↔ tipos (E7); oferta ↔ E5/E6 (sin fila en V18); actividad y renta ↔ F1 (ASOCIACIÓN, no entra). Se comparan el signo y el solape de las bandas del 68 %; los periodos de V8 son los suyos (2008T3-2013T4, 2020T2-2022T2) y la Δ observada de V18 usa otro deflactor.

| periodo V8 | factor V8 | factor V18 | V8 mediana | V8 p16 | V8 p84 | V18 mediana | V18 p16 | V18 p84 | mismo signo | bandas se solapan |
|---|---|---|---|---|---|---|---|---|---|---|
| P2 | empleo_renta | F1 (sensibilidad) | -7,6 | -23,5 | 0,7 | — | — | — |  |  |
| P2 | demografia | E3 | -1,6 | -10,7 | 4,0 | -0,8 | -2,2 | 0,7 | True | True |
| P2 | demografia | E9 | -1,6 | -10,7 | 4,0 | 11,3 | 9,8 | 12,9 | False | False |
| P2 | oferta | E5 | -2,1 | -13,3 | 2,5 | — | — | — |  |  |
| P2 | oferta | E6 | -2,1 | -13,3 | 2,5 | — | — | — |  |  |
| P2 | credito_tipos | E7 | -5,9 | -18,9 | 0,5 | 1,1 | 0,8 | 1,5 | False | False |
| P3 | empleo_renta | F1 (sensibilidad) | 5,2 | -3,5 | 18,2 | — | — | — |  |  |
| P3 | demografia | E3 | -0,2 | -6,6 | 6,8 | 1,0 | -1,0 | 3,0 | False | True |
| P3 | demografia | E9 | -0,2 | -6,6 | 6,8 | -4,2 | -4,8 | -3,7 | True | True |
| P3 | oferta | E5 | 0,2 | -7,3 | 8,0 | — | — | — |  |  |
| P3 | oferta | E6 | 0,2 | -7,3 | 8,0 | — | — | — |  |  |
| P3 | credito_tipos | E7 | -0,7 | -9,8 | 7,1 | 0,4 | 0,2 | 0,5 | False | True |
| P4 | empleo_renta | F1 (sensibilidad) | -0,5 | -7,1 | 4,7 | — | — | — |  |  |
| P4 | demografia | E3 | 0,1 | -4,0 | 3,4 | 0,5 | -0,5 | 1,4 | True | True |
| P4 | demografia | E9 | 0,1 | -4,0 | 3,4 | — | — | — |  |  |
| P4 | oferta | E5 | -0,3 | -4,8 | 3,3 | — | — | — |  |  |
| P4 | oferta | E6 | -0,3 | -4,8 | 3,3 | — | — | — |  |  |
| P4 | credito_tipos | E7 | 0,1 | -4,7 | 4,4 | 0,3 | 0,2 | 0,4 | True | True |
| P5 | empleo_renta | F1 (sensibilidad) | 1,1 | -4,7 | 11,2 | — | — | — |  |  |
| P5 | demografia | E3 | 0,6 | -4,1 | 5,8 | 1,8 | -1,7 | 5,1 | True | True |
| P5 | demografia | E9 | 0,6 | -4,1 | 5,8 | -3,3 | -3,8 | -2,9 | False | True |
| P5 | oferta | E5 | 1,8 | -3,3 | 9,0 | — | — | — |  |  |
| P5 | oferta | E6 | 1,8 | -3,3 | 9,0 | — | — | — |  |  |
| P5 | credito_tipos | E7 | 3,4 | -2,8 | 12,8 | 2,9 | 2,0 | 3,7 | True | True |
| P1 | empleo_renta | F1 (sensibilidad) | 29,5 | 9,0 | 54,6 | — | — | — |  |  |
| P1 | demografia | E3 | 4,8 | -5,0 | 24,8 | 6,9 | -6,7 | 20,0 | True | True |
| P1 | demografia | E9 | 4,8 | -5,0 | 24,8 | — | — | — |  |  |
| P1 | credito_tipos | E7 | 0,1 | -7,2 | 14,0 | — | — | — |  |  |
\nCon cifra en ambos lados (E3 y E7, la contabilidad principal de la ilustración): 9 comparaciones; mismo signo en 6 y bandas del 68 % que se solapan en 8. Las bandas de V8 incluyen el cero casi siempre, por lo que el solape es una prueba débil; no se suman ni se promedian.

**Banco de España (referencias de V17 y fichas de `docs/v18/bib/modelos_conjunto` y `no_residentes`; no se suman).** (i) Sobrevaloración del precio: 10-15 % en diciembre de 2025 (IEF de primavera de 2026, rango entre métodos), un indicador de nivel frente a fundamentales que la contabilidad con elasticidades no replica. (ii) Tipos: San Juan (2023) estima ≈ −2 % del precio a 8 trimestres por +100 pb (BVAR, intervalos al 68 % solo en gráfico); el rango usado aquí (−5 a −2) lo incluye. (iii) Lajer Baron et al. (2024): un diferencial de unos 365.000 entre hogares y viviendas en 2022-2023 y unas 120.000 viviendas más de déficit por los no residentes; son contabilidad de cantidades, no de precios. (iv) Informe Anual 2025: no residentes 7,4 % de las compras (Alicante 33,3 %, Málaga 27,9 %, Baleares 23,0 %) y elasticidad de oferta 0,45 como cota superior (V16; cifra que el Documento Ocasional 2433 no recoge); frente a ello, el rango de E5 (0,26-0,87 entre tres estudios) es de otro orden de incertidumbre y no se usa en la contabilidad.

## 7. Contradicciones con lo publicado

Ninguna estimación propia de V18 es IDENTIFICADO, así que no hay parada G. Compatibilidad con conclusiones publicadas: (a) V8 («ningún factor puede designarse»): coherente; V18 tampoco designa ninguno. (b) Informe integral III.2 y V17: los topes de Cataluña («prometedora», −4 a −6 % en la renta regulada): E2-R1 (−3,8 %) es compatible y añade que la diferencia se apaga dentro de la vigencia. (c) V17, inmigración (≈ 1,3 % de precio por 1 % de población): cae dentro del rango de la literatura de E3 (−1,6 a 3,2); la ilustración asocia a la inmigración en torno al 10 % de la subida de 1995-2007 con la mediana de ese rango, bastante por debajo del «un cuarto» de González y Ortega (2013) para 2000-2010, que corresponde al extremo alto del rango; se documenta, no contradice (la cifra de V17 es una ilustración). (d) V17, tipos («frenó el precio» en 2022-2023): el horizonte de 8 trimestres de la contabilidad deja fuera del horizonte ese aumento del tipo, y en 2022T3-2026T2 solo cuenta la bajada posterior (de signo contrario): la contabilidad no contradice la afirmación, no la contrasta.

## 8. Limitaciones y desviaciones

- Magnitudes de la literatura (muchas «solo resumen» o NO VERIFICADAS) aplicadas a España; E7, E8 y E9 sin error típico; E1 con un solo estudio y unidades que no coinciden con la variación disponible (anuncios de Airbnb frente a registro HUT).
- Factores sin variación comparable medida (E4, E5, E6) y turismo antes de 2018 (no medido, no cero).
- Variación observada sin error; independencia entre factores (no hay dos magnitudes del mismo modelo, así que la sensibilidad a ρ = ±0,5 entre magnitudes no aplica).
- Conversión de % a log (≈ igual) y efectos de nivel permanentes para E3, E8 y E9, que en la literatura son a 12 meses o promedios del periodo.
- Ventanas de factor anuales (stock a 1 de enero) recortadas a los topes de sellado (2024 en el padrón y la población extranjera); los ITP usan fechas sin contraste con el BOE y solo desde 2010.
- Desviaciones de la contabilidad respecto al plan: deflactor del PIB en lugar del IPC de V8; rangos de la literatura en lugar de posterior de B5 cuando B5 no da magnitud; Cantabria sin serie provincial; E1 y E2 solo en Barcelona y Cataluña (grandes ciudades solo València y Barcelona con dato no sellado); lectura de la adenda 1.10 explicada en la sección 3.
