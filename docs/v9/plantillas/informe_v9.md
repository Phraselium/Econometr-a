# Qué causa qué: diseños de identificación de V9

Borja Romero, economista (firma individual, independiente). Generado por `make v9` desde `docs/v9/plantillas/informe_v9.md`. Cada cifra sale de `output/v5/cifras_clave.csv` (identificadores `V9-…`) y se puede rastrear hasta su script en `src/v9/`.

## Resumen

V9 intenta pasar de asociaciones a efectos con diseños de identificación sobre datos locales:

- topes de renta y zonas tensionadas (Cataluña y Euskadi);
- pisos turísticos ante el shock del COVID (Cataluña);
- caída del registro de viviendas turísticas (Comunitat Valenciana);
- inmigración predicha por redes de origen (provincias);
- shocks del BCE según la exposición a hipotecas a tipo variable (zona euro);
- contabilidad de hogares y viviendas.

Las reglas se fijaron antes de estimar: pre-registro `docs/v9/hipotesis.md` y addendum `docs/v9/hipotesis_addendum_a1.md`, revisados por un revisor independiente.

**Ningún resultado alcanza C3 o C3s** ({{V9-NC3}} en C3/C3s). Por tanto, V9 no atribuye a ningún factor una parte de la subida y la tabla de cotas queda vacía (`publicacion/cotas_v9.md`). Lo que sí se observa:

- [C4] **Ley catalana 11/2020.** En los municipios con topes, la renta de los contratos nuevos fue {{V9-D1b-renta-att}} respecto a los comparables (p de Holm {{V9-D1b-renta-pholm:num}}).
  - La comparación supera la prueba de tendencias previas (p {{V9-D1b-renta-pretend-p:num}}), el placebo de fecha y la permutación.
  - No supera la robustez a desviaciones de tendencia exigida en el pre-registro (M̄ de ruptura {{V9-D1b-renta-ruptura:num}} frente a 1).
  - La magnitud coincide con la literatura (LB01: −4 % a −6 %), pero no se lee como efecto.
- [C4] **Zonas tensionadas en Cataluña.** La diferencia es {{V9-D1a-renta-att}}, pero los municipios declarados ya evolucionaban de forma distinta antes de 2024 (pretendencias p {{V9-D1a-renta-pretend-p:num}}; placebo de fecha p {{V9-D1a-renta-placebo-p:num}}). No se puede separar de esas tendencias.
- [C4] **Número de contratos.** No se detecta una caída del número de contratos ni con la Ley 11/2020 ({{V9-D1b-contratos-att}}) ni con las zonas tensionadas ({{V9-D1a-contratos-att}}).
- [C4] **Pisos turísticos (Cataluña).** Los municipios con más plazas turísticas en 2019 muestran una renta de contratos nuevos algo mayor tras la reapertura, {{V9-D2-renta-reap}} por desviación típica de dosis. Las tendencias previas se rechazan (p {{V9-D2-renta-pretend-p:num}}).
- [C4] **Inmigración (provincias).** El instrumento de redes de origen es débil (F efectiva {{V9-D4-ipc-replica-F:num}}). Los coeficientes no son concluyentes: IPC de alquiler {{V9-D4-ipc-replica}} por punto de población extranjera en 2003-2012.
- [C4] **Tipos de interés (zona euro).** Con más hipotecas a tipo variable, la asociación con el precio a cuatro trimestres es {{V9-D5-precio-h4}} y no se distingue de cero. La del alquiler es negativa a cuatro trimestres ({{V9-D5-alq-h4}}).
- [C4, contable] **Hogares.** Entre el 1 de enero de 2022 y el de 2025, el componente población supone {{V9-D7-ES-2225-cuota-pob}} del aumento de hogares en España y {{V9-D7-CV-2225-cuota-pob}} en la Comunitat Valenciana. Más del 100 % significa que la tasa de jefatura (hogares por persona) bajó. En 2011-2021 pesó más la tasa de jefatura (componente población {{V9-D7-ES-1121-cuota-pob}}).
- **Bono Alquiler Joven.** No se puede evaluar con datos públicos: falta la edad exacta y no se identifica a los receptores.

## Abstract (English)

V9 tries to move from associations to effects with local identification designs:

- rent caps and stressed-market zones (Catalonia, Basque Country);
- short-term rentals under the COVID shock (Catalonia);
- the drop in the tourist-dwelling register (Valencia region);
- immigration predicted by origin networks (provinces);
- ECB shocks by exposure to variable-rate mortgages (euro area);
- household-dwelling accounting.

Rules were pre-registered and amended once after independent review, before any estimation. **No result reaches the causal layers (C3/C3s)**, so no share of the price rise is attributed to any factor.

- Rents of new contracts in municipalities under the 2020 Catalan rent cap were about 6 % lower than in comparable municipalities. The comparison passes pre-trend, date-placebo and permutation tests but fails the pre-registered robustness-to-trend-deviation test, so it is reported as an association consistent with earlier studies.
- Stressed-market zones show diverging pre-trends.
- No fall in the number of contracts is detected.
- The short-term rental, immigration and monetary-policy designs are either underpowered or weakly identified.
- Population growth accounts for most of the 2022-2025 rise in households.

## 1. Qué se ha medido y con qué reglas

Los efectos y asociaciones se expresan en puntos logarítmicos ×100, que equivalen aproximadamente a porcentajes (%). En D5 son puntos por unidad de shock del BCE y desviación típica de exposición.

- **Capas.** C3 exige que la hipótesis sea confirmatoria (con potencia suficiente, calculada antes de estimar), que supere Holm y que pase todas sus pruebas: tendencias previas, placebo de fecha, robustez a desviaciones de tendencia (Honest DiD, M̄ = 1) y permutación de etiquetas. C4 es todo lo demás. Nada sube de capa por robustez.
- **Familia confirmatoria:** {H1a-renta, H1b-renta}. El resto es exploratorio, con una única familia de Benjamini-Hochberg.
- **Tabla completa** (β, error, IC, p, p ajustado, N, diagnósticos y capa): `publicacion/tabla_v9.md`.
- **Comparación con la literatura:** `output/v9/f3/comparacion_literatura.csv`.

## 2. Resultados por diseño

**D1. Topes y zonas tensionadas.**
- **Datos.** Fianzas de Incasòl por municipio y trimestre (no redistribuibles: solo se publican agregados).
- **Método.** Callaway y Sant'Anna con nunca tratados; como alternativas, BJS y dCDH.
- **Ley 11/2020** (60 municipios con datos completos frente a 181). Renta {{V9-D1b-renta-att:cita}}; contratos {{V9-D1b-contratos-att}}.
- **Zonas tensionadas** (dos cohortes en 2024). Renta {{V9-D1a-renta-att}}; contratos {{V9-D1a-contratos-att}}.
  - Las pretendencias y el placebo de fecha se rechazan (p {{V9-D1a-renta-pretend-p:num}} y {{V9-D1a-renta-placebo-p:num}}).
  - Con solo 20 municipios de control con datos completos, la comparación es frágil.
- **Euskadi** (EMAL, pocos trimestres posteriores; exploratorio): {{V9-D1c-renta-att}}.

**D2. Pisos turísticos × COVID (Cataluña).**
- **Dosis.** Plazas en viviendas de uso turístico por cada 100 habitantes en 2019 (IDESCAT).
- **COVID** (2020-2021): {{V9-D2-renta-covid}}.
- **Reapertura** (2022-2025): {{V9-D2-renta-reap}}.
- **Pretendencias:** p {{V9-D2-renta-pretend-p:num}}. Con una tendencia lineal por dosis, la asociación de la reapertura deja de distinguirse de cero (`output/v9/d2/tabla_d2.csv`).

**D3. Comunitat Valenciana (descriptivo).**
- **Unidad y periodo.** Códigos postales; variación 2024→2025 frente a la caída del registro de viviendas turísticas.
- **Fianza media:** {{V9-D3-media}} por cada variación de +1 vivienda turística registrada por 100 viviendas.
- **Placebo.** El de 2021→2023 muestra una asociación del mismo signo, así que no se separa de diferencias previas entre códigos postales.

**D4. Inmigración.**
- **Método.** 2SLS con un instrumento de redes de origen: 28 nacionalidades, crecimiento nacional sin la propia provincia, 50 provincias.
- **Réplica 2003-2012:**
  - IPC de alquiler {{V9-D4-ipc-replica}};
  - valor tasado {{V9-D4-tasado-replica}};
  - F efectiva {{V9-D4-ipc-replica-F:num}}, por debajo del umbral de 23,1.
- **Ampliación 2015-2022:** valor tasado {{V9-D4-tasado-ampliacion}}, con instrumento también débil.
- **Lectura.** Con instrumentos débiles solo se interpreta el IC de Anderson-Rubin (`output/v9/d4/tabla_d4.csv`).

**D5. Tipos de interés.**
- **Método.** Proyecciones locales en 18 países con un shock del BCE (Jarociński-Karadi) interactuado con la cuota de hipotecas a tipo variable en 2003-2007.
- **Precio:** {{V9-D5-precio-h4}} a 4 trimestres y {{V9-D5-precio-h8}} a 8.
- **Alquiler:** {{V9-D5-alq-h4}} a 4 trimestres.

**D7. Hogares y viviendas (contable).**
- **Aumento de hogares 2022-2025:** {{V9-D7-ES-2225-dH}} en España.
- **Componente población:** {{V9-D7-ES-2225-cuota-pob}} en España y {{V9-D7-CV-2225-cuota-pob}} en la Comunitat Valenciana.
- **Contraste entre fuentes.** Censo 2021 y ECP difieren en {{V9-D7-c1-dif}} [C4: la ECP se apoya en el censo, así que no son fuentes independientes; corregido en V15, ERRATA].
- **Reconciliación del déficit** (proyecto, Banco de España y OCDE): `output/v9/d7/reconciliacion_deficit.csv`. Las viviendas liberadas por envejecimiento no se restan (regla v5.1).

## 3. Qué no se ha podido identificar y qué datos lo resolverían

- **Bono Alquiler Joven:** edad exacta y receptores.
- **Pisos turísticos en València:** fianzas por barrio y mes, y altas y bajas fechadas del registro.
- **Concentración de la propiedad:** titularidad agregada del Catastro.

Las solicitudes están redactadas en `docs/v9/solicitudes_transparencia.md`. El cierre (`docs/v9/cierre.md`) explica por qué el siguiente paso es la revisión humana y la publicación, no otra versión de modelización.
