# V18 · E3 Inmigración: réplica y ampliaciones de González y Ortega (2013)

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.* Generado por `python3 src/v18/estimacion/e3_inmigracion.py` (SEED 20261010, sin red; B = 9999 réplicas de Webb). Clasificaciones **provisionales: pendientes de I8** (réplica ciega, B6). Toda cifra es C4 (nivel_evidencia EXPLORATORIO). Sin lenguaje causal: se habla de asociación condicionada al diseño.

## 1. Resumen
- De las 10 especificaciones principales (R1, R1q, R2, R2b, R2q, A1, A2, A4, A5, A3), la comprobación previa de variación (MDE al 80 %, adenda 1.3) deja **estimables 1** (R1) y **NO ESTIMABLES 9** (por variación: R1q, R2, R2b, R2q, A1, A2, A5, A3; por datos: A4). Además se estiman las coprincipales P (V9-D4, V16-Q3c1 y V16-H4) en la muestra V18.
- **E3-R1** (ventana 2002-2008; sin 2003): 3.555 €/m² por punto; IC95 Webb-AR [-53.49; 63.87]; AR exacto [-39.66; 84.41]; F efectivo 81.07; p (Webb-AR) 0.8781, p (AR) 0.8473, p tras Holm 1. Clase: **NO CONCLUYENTE (sin potencia)**. coherente con González y Ortega (2009, IZA): 44,72 €/m² por punto de población (NO VERIFICADA), razón 0.08.
- Lectura: la estimación no es distinguible de cero ni de la referencia; el diseño no decide.
- B5: E3-R2 (la estimación propia de E3) y su respaldo E3-A1 son NO ESTIMABLES por variación; E3 no aporta magnitud propia a la magnitud preferida (adenda 1.9).

## 2. Diseño y traslado
- **Original.** González y Ortega (2013, J. Regional Science) y su versión IZA de 2009: 50 provincias, primeras diferencias ponderadas, efectos región-año, instrumento de redes étnicas con el Censo de 1991; IZA: 44,72 €/m² por punto de población (EE 18,58); Chicago Fed 2011: elasticidad 0,959 (0,984) solo con redes, 2001-2010.
- **Aquí.** 39 provincias no selladas; x = 100·ΔF/P (F: extranjeros del padrón a 1 de enero; entre t y t+1 entran los del año t); z = 100·Σ_c s_pc·M_ct/P(t), con s_pc la distribución del grupo c entre provincias en el Censo de 2001 y M_ct las entradas nacionales del grupo (Eurostat/INE). Controles: región-año (5 NUTS 1 sin sellar), cuota de empleo en construcción de 2001 × año y costa × año (17 provincias). Pesos: población de 1 de enero de 1998 (R1) o 2000 (R2).
- **Desviaciones** (docs/v18/desviaciones_e3_e5_e9.md): Censo de 2001 vía Eurostat porque el INE no lo sirve (D-E359-1); 8 grupos de origen en lugar de 16 (D-E359-3); 2003 sin detalle por nacionalidad fuera de la principal (D-E359-4); balance a nivel de choque (D-E359-16); etiqueta NO CONCLUYENTE para las estimaciones no significativas con pruebas débiles (D-E359-17).

## 3. Comprobación previa de variación (adenda 1.3)

| id | n | G | F efectivo | σ preperiodo | ρ | MDE80 | |referencia| | estimable | 1/HHI origen |
|---|---|---|---|---|---|---|---|---|---|
| E3-R1 | 234 | 39 | 81.07 | 25.4 | 0.4143 | 36.74 | 44.72 | sí | 7.858 |
| E3-R1q | 234 | 39 | 3.941 | 0.3074 | 0.2751 | — | 0.462 | NO | 7.858 |
| E3-R2 | 312 | 39 | 22.91 | 0.02581 | 0.1341 | 2.331 | 0.959 | NO | 7.857 |
| E3-R2b | 234 | 39 | 24.66 | 0.02581 | 0.1341 | 2.138 | 0.927 | NO | 7.855 |
| E3-R2q | 312 | 39 | 22.91 | 0.2927 | -0.402 | 15.89 | 1.05 | NO | 7.857 |
| E3-A1 | 351 | 39 | 14.85 | 2.895 | -0.02126 | 10.38 | 3.046 | NO | 7.825 |
| E3-A2 | 324 | 36 | 13.85 | 1.655 | 0.8166 | 13.41 | 0.947 | NO | 7.79 |
| E3-A5 | 653 | 39 | 41.57 | 2.581 | 0.1345 | 3.789 | 3.046 | NO | 7.854 |
| E3-A3 | 9798 | 38 | 117.9 | 8.551 | 0 | — | 0.947 | NO | 9.637 |
| E3-P-H4 | 11759 | 38 | 54.34 | 8.551 | 0 | 2.043 | 0.947 | NO | 7.165 |


MDE por Monte Carlo (R = 2000, SEED 20261010) con el contraste de Anderson-Rubin agrupado por provincia y la variación real del regresor y del instrumento; σ y ρ del preperiodo (1996-2001 en R; 2009-2013 en A1 y A5; 2012-2013 en A2 y A3), declaradas como «no vistas» en V15/V16 para estas unidades. Se calculó **antes** de estimar (incidencia D-E359-15: una lectura de desarrollo de R1 antes del MDE, sin efecto en ninguna decisión).

## 4. Resultados

| id | rol | ventana | n | G | beta | se | ic95_webb_ar_lo | ic95_webb_ar_hi | F_eff | p_webb_ar | p_ar | p_holm | q_BY | clase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E3-R1 | principal | 2002-2008 | 234 | 39 | 3.555 | 18.77 | -53.49 | 63.87 | 81.07 | 0.8781 | 0.8473 | 1 | — | NO CONCLUYENTE (sin potencia) |
| E3-R1-v2 | variante | 2002-2008 | 234 | 39 | -1.029 | 24.2 | -147.3 | 65.93 | 20.04 | 0.9757 | 0.9661 | — | 1 |  |
| E3-R1-v4 | variante | 2002-2008 | 234 | 39 | 3.112 | 10.37 | -19.01 | 27.5 | 51.8 | 0.7716 | 0.7614 | — | 1 |  |
| E3-R1-v5 | variante | 2002-2008 | 234 | 39 | 6.562 | 14.47 | -20.83 | 46.6 | 67.02 | 0.6949 | 0.6105 | — | 1 |  |
| E3-R1-v6 | variante | 2002-2008 | 234 | 39 | 5.864 | 17.62 | -62.35 | 48.25 | 215.8 | 0.7865 | 0.7395 | — | 1 |  |
| E3-R1-v7 | variante | 2002-2008 | 234 | 39 | -3.86 | 21.21 | -95.23 | 62.86 | 54.18 | 0.8861 | 0.8572 | — | 1 |  |
| E3-R1-v8 | variante | 2002-2008 | 228 | 38 | 1.008 | 10.77 | -24.61 | 30.07 | 63.75 | 0.9322 | 0.9245 | — | 1 |  |
| E3-R1-v9 | variante | 2002-2008 | 222 | 37 | 4.903 | 12.93 | -39.44 | 47.61 | 81.18 | 0.7391 | 0.6833 | — | 1 |  |
| E3-R1-v11 | variante | 2002-2008 | 273 | 39 | 7.196 | 19.64 | -37.57 | 70.24 | 96.44 | 0.7551 | 0.7045 | — | — |  |
| E3-P-H4 | coprincipal | 2012-2022 | 11759 | 38 | 0.1756 | 0.3294 | -0.65 | 0.9283 | 54.34 | 0.621 | 0.5995 | 1 | — | no se clasifica |
| E3-P-D4 | coprincipal | 2003-2012 | 34 | 34 | 0.005358 | 0.03049 | — | — | 0.3688 | 0.8553 | 0.854 | 1 | — | no se clasifica |
| E3-P-Q3c1 | coprincipal | 2011-2022 | 408 | 34 | 0.008203 | 0.006885 | -0.0117 | 0.02632 | — | 0.3439 | — | 1 | — | no se clasifica |


Unidades: R1 en €/m² por punto de población; A1, A3 y A5 en % por punto; R2 en elasticidad (ln valor tasado frente a ln población de 15 a 64). IC95 Webb-AR: inversión del contraste de Anderson-Rubin con bootstrap de Webb (nulo impuesto, 9999 réplicas); si no está acotado se dice. «p_holm»: Holm dentro de la familia E3 (principales y coprincipales estimables; m = 4). «q_BY»: Benjamini-Yekutieli entre las variantes de su principal.

### NO ESTIMABLES

- **E3-R1-v1**: ventana 1998-2008: sin stock provincial de extranjeros antes de 2002.
- **E3-R1-v3**: Censo de 1991 no está en el repositorio.
- **E3-R1-v10**: choque sin la propia provincia con el padrón por nacionalidad: no reconstruye los 8 grupos.
- **E3-R1q**: NO ESTIMABLE por variación: MDE superior a seis errores típicos de referencia (no se alcanza el 80 % de potencia) frente a |referencia| 0.462 (viviendas por inmigrante).
- **E3-R1q-v2**: ventana 1998-2008: sin stock provincial de extranjeros antes de 2002.
- **E3-R2**: NO ESTIMABLE por variación: MDE 2.33 frente a |referencia| 0.959 (elasticidad).
- **E3-R2-v7**: Censo de 1991 no está en el repositorio.
- **E3-R2b**: NO ESTIMABLE por variación: MDE 2.14 frente a |referencia| 0.927 (elasticidad).
- **E3-R2q**: NO ESTIMABLE por variación: MDE 15.9 frente a |referencia| 1.05 (elasticidad).
- **E3-A1**: NO ESTIMABLE por variación: MDE 10.4 frente a |referencia| 3.05 (% por punto).
- **E3-A1-v4**: IPV por CCAA: nueve clusters, inferencia sin Monte Carlo apto (Webb con 8 clusters: NO APTO).
- **E3-A2**: NO ESTIMABLE por variación: MDE 13.4 frente a |referencia| 0.947 (% por punto).
- **E3-A4**: la tenencia por nacionalidad del Censo de 2011 por provincia no está en el repositorio ni en Eurostat (cens_11htts_r2 es por hogares y NUTS 2, sin nacionalidad).
- **E3-A5**: NO ESTIMABLE por variación: MDE 3.79 frente a |referencia| 3.05 (% por punto).
- **E3-A5-v1**: choque sin la propia provincia con el padrón por nacionalidad: no reconstruye los 8 grupos.
- **E3-A3**: NO ESTIMABLE por variación: MDE superior a seis errores típicos de referencia (no se alcanza el 80 % de potencia) frente a |referencia| 0.947 (% por punto).
- **E3-A3-v1**: valor tasado municipal: el fichero de MIVAU (309 municipios) no trae código INE y la base solo lo tiene para un municipio.
- **E3-R1q-v1**: su principal E3-R1q es NO ESTIMABLE.
- **E3-R2-v1**: su principal E3-R2 es NO ESTIMABLE.
- **E3-R2-v2**: su principal E3-R2 es NO ESTIMABLE.
- **E3-R2-v3**: su principal E3-R2 es NO ESTIMABLE.
- **E3-R2-v4**: su principal E3-R2 es NO ESTIMABLE.
- **E3-R2-v5**: su principal E3-R2 es NO ESTIMABLE.
- **E3-R2-v6**: su principal E3-R2 es NO ESTIMABLE.
- **E3-R2-v8**: su principal E3-R2 es NO ESTIMABLE.
- **E3-R2b-v1**: su principal E3-R2b es NO ESTIMABLE.
- **E3-R2q-v1**: su principal E3-R2q es NO ESTIMABLE.
- **E3-A1-v1**: su principal E3-A1 es NO ESTIMABLE.
- **E3-A1-v2**: su principal E3-A1 es NO ESTIMABLE.
- **E3-A1-v3**: su principal E3-A1 es NO ESTIMABLE.
- **E3-A1-v5**: su principal E3-A1 es NO ESTIMABLE.
- **E3-A1-v6**: su principal E3-A1 es NO ESTIMABLE.
- **E3-A2-v1**: su principal E3-A2 es NO ESTIMABLE.
- **E3-A2-v2**: su principal E3-A2 es NO ESTIMABLE.
- **E3-A2-v3**: su principal E3-A2 es NO ESTIMABLE.
- **E3-A2-v4**: su principal E3-A2 es NO ESTIMABLE.
- **E3-A2-v5**: su principal E3-A2 es NO ESTIMABLE.
- **E3-A2-v6**: su principal E3-A2 es NO ESTIMABLE.
- **E3-A3-v2**: su principal E3-A3 es NO ESTIMABLE.
- **E3-A3-v3**: su principal E3-A3 es NO ESTIMABLE.
- **E3-A3-v4**: su principal E3-A3 es NO ESTIMABLE.
- **E3-A3-v5**: su principal E3-A3 es NO ESTIMABLE.

Qué datos las harían estimables: (i) flujos de entrada por nacionalidad (país) y provincia de destino (EVR 1998-2021 y EMCR 2021-2024 por provincia y país: hoy solo por continente en el repositorio) para el choque sin la propia provincia y con los 16 grupos del original; (ii) el Censo de 2001 por país de nacionalidad y provincia (INE; hoy solo accesible por Eurostat con 8 grupos); (iii) más años de variación del instrumento dentro de región-año (padrón por provincia anterior a 2002) o unidades más finas (municipios con el padrón por nacionalidad anterior a 2003); (iv) las 11 provincias selladas de v6, que no se leen.

## 5. Pruebas B4 de las principales estimables

### E3-R1
- Pretendencia del instrumento (corte transversal, efectos de macrorregión): pendiente 8.922 (EE 6.214), p Webb 0.2555; pendiente detectable al 80 %: 17.41; sesgo implicado en β: 26.64 frente a ½|referencia| = 22.36 → potencia insuficiente (prueba débil).
- Placebo de fecha (instrumento de t+6 en el preperiodo): coef. 10.26, p Webb 0.3006 (N = 195).
- Placebo de resultado (población de 65 años o más, total): coef. 0.008655, p Webb-AR 0.06571, p AR exacto 0.09411.
- Balance a nivel de choque (BHJ; 8 choques; Holm entre características): cuota empleo construcción 2001: pendiente -0.006113, p 0.9069; cuota empleo industria 2001: pendiente 0.02381, p 0.8199; log población 2001: pendiente -0.3576, p 0.7993; cuota de extranjeros 2001: pendiente -0.01047, p 0.7203. p de Holm mínimo 1.
- Información: el balance del instrumento medio frente a las características de 2001 a nivel de provincia da p = 1.8e-12 (esperable: el instrumento es proporcional a la exposición de 2001); no entra en la clasificación (D-E359-16).
- Pesos de Rotemberg: G1_UE15 0.19, G2_AELC 0.01, G3_Europa_resto 0.42, G4_Africa_norte 0.17, G5_Africa_resto 0.07, G6_America_latina_Caribe 0.14, G7_Asia -0.00, G8_resto_mundo 0.00
  Sin los orígenes de más peso (G3_Europa_resto, G1_UE15): β = 37.71 (F efectivo 23.65); mismo signo: True; dentro del IC95 principal: True.
- Jaeger-Ruist-Stuhler (instrumento de t-4 como control): β = 47.19 (EE 25.93); dentro del IC95 principal: True.
- Sin atípicos: β = 16.76 (EE 23.92); mismo signo: True.
- Información (no preinscrita): con el control de la suma de cuotas × año, β = 3.613 (EE 22.82), F efectivo 58.98.
- BHJ a nivel de choque (alternativa, **no fiable (Monte Carlo de V18: BHJ con 10-30 choques NO APTO)**): β = 3.613 (EE 53.66; 48 choques, 8 orígenes).

## 6. Clasificación (I1-I8 revisados; adenda 1.1 y 1.2)

- **E3-R1: NO CONCLUYENTE (sin potencia)** (provisional, pendiente de I8). Razones y pruebas débiles: potencia de las pretendencias (Roth): el sesgo implicado supera la mitad de |referencia|; placebo de resultado p = 0.066; mismo signo en 71% de las variantes enumeradas (< 80 %); tope SUGESTIVO: año base 2001 tras el F de 3,4-4,6 de V9-D4 (adenda 1.6); sin significación (p de Holm ≥ 0,10) y sin equivalencia: se rotula NO CONCLUYENTE con las pruebas débiles listadas (D-E359-17). TOST con δ = 22.4: sin equivalencia. coherente con González y Ortega (2009, IZA): 44,72 €/m² por punto de población (NO VERIFICADA), razón 0.08.

La adenda reserva SUGESTIVO a diseños creíbles con alguna prueba débil; una estimación sin significación (p de Holm ≥ 0,10) y sin equivalencia no tiene un efecto que sugerir, por lo que se rotula NO CONCLUYENTE (sin potencia) con las pruebas débiles listadas (D-E359-17). Tope de la tabla consolidada para E3-R1: SUGESTIVO (año base 2001 tras el F de 3,4-4,6 de V9-D4, adenda 1.6).

## 7. Coprincipales P (adenda 1.6; no se clasifican)

- **E3-P-D4** (V9-D4, 2003-2012, valor tasado, muestra V18): β = 0.005358 (EE 0.03049); IC95 Webb-AR [no acotado; no acotado]; F efectivo 0.3688; p Webb-AR 0.8553, p AR 0.854; n = 34. Publicado en V9: −0,0029 (valor tasado) y 0,0072 (IPC de alquiler), F de 3,4 a 4,6. IPC de alquiler aquí: β = -0.007524.
- **E3-P-Q3c1** (V16, TWFE, ln valor tasado 2011-2022): β = 0.008203 (EE 0.006885); IC95 Webb [-0.0117; 0.02632]; p Webb 0.3439; 34 provincias × 12 años. Publicado en V16: 0,0119 (solo puntual).
- **E3-P-H4** (V16 réplica ciega H4, municipal SERPAVI): β = 0.1756 % por punto (EE 0.3294); IC95 Webb-AR [-0.65; 0.9283]; F efectivo 54.34; N = 11759 (réplica de V16: 2SLS 0,309 con N = 13.395; H4 publicado: 0,29 con N = 13.442; la muestra V18 excluye además los municipios de V16).

## 8. Familia de Holm y multiverso

- Familia E3: m = 4 contrastes (principales estimables y coprincipales P tras las comprobaciones previas); p ajustados: E3-P-Q3c1 1.000, E3-P-H4 1.000, E3-P-D4 1.000, E3-R1 1.000.
- Variantes enumeradas estimadas: 7; las de datos ausentes quedan «no estimable» sin sustituir (D-E359-11). R1-v11 (2003 interpolado) es holgura nº 1: no cuenta en I5 ni en B5.

## 9. Limitaciones

- Ocho grupos de origen en lugar de 16: el número efectivo de choques es bajo y el instrumento es menos fino que el original.
- La σ del preperiodo es la del residuo con los mismos efectos; el Webb-AR de la estimación no tiene Monte Carlo propio (sus piezas, Webb en TWFE y AR de una endógena, son APTAS).
- El F efectivo alto de R1 no garantiza potencia (el Monte Carlo deja NO APTA la regla F ≥ 10).
- Sin las 11 provincias selladas de v6 (entre ellas Madrid, Baleares y Canarias) el panel no cubre las de más inmigración reciente.
- I8 (réplica ciega) y la ronda del abogado del diablo (B6) están pendientes.

