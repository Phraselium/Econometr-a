# Determinantes del precio de la vivienda en España: informe v2 (síntesis BS)

Documento generado por `src/v2/bs_run.py` a partir de las salidas versionadas de las ramas BA, BV, BI, BO, BP, BM y BD (`output/v2/`). Ninguna cifra está escrita a mano: cada bloque cita su fichero de origen. Escala de evidencia: CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO; **ninguna conclusión de este informe supera EXPLORATORIO** y se evita el lenguaje causal. Inferencia: EE cluster por provincia con wild cluster bootstrap (Webb) o HAC(4); comparación de modelos en la misma muestra frente a AR(4) y ECM v1 (Diebold-Mariano con corrección Harvey-Leybourne-Newbold).

## 1. Resumen ejecutivo

**Alcance.** 34 especificaciones registradas en v2 (`output/v2/tablas/registro_v2.csv`; v1: 3.812), sobre paneles provinciales (49 provincias de entrenamiento, 2002Q1-2024Q2) con la muestra 2024Q3-2026Q2 y las provincias 11, 16 y 45 selladas. Lenguaje de **asociación**: ninguna pregunta alcanza el nivel CAUSAL y ninguna confirmatoria alcanza ASOCIACIÓN ROBUSTA.

- **Hipótesis confirmatorias.** Ninguna de las 7 supera Holm sobre la familia de 7 (p ajustado por hipótesis: H6 0,098; H3 0,176; H4 0,232; H2 0,779; H1 1,000; H5 1,000; H7 1,000; el menor es H6). Por el criterio uniforme todas quedan **EXPLORATORIO** (etiquetas fijadas en `docs/v2/decisiones.md`).
- **Hecho predictivo de v2.** En la muestra sellada, el modelo demográfico de alquiler (H1) mejora al AR(4) de panel (RMSE 0,0108 frente a 0,0122; DM-HLN 3,98; p = 0,005; p×7 = 0,037) y al ECM v1 (p = 0,031). Es un hecho fuera de muestra; **no** convierte la hipótesis conjunta de H1 (que exigía también signo + de la población extranjera, no cumplido: p_IUT 0,850) en una asociación robusta de cada coeficiente. En las 3 provincias selladas solas (n = 24) no hay diferencia significativa.
- **Ningún otro modelo supera al AR(4).** De 85 configuraciones evaluadas en validación por bloques con embargo, 0 mejoran al AR(4) tras BH (2 con p<0,05 sin corregir); de los 5 contrastes sellados principales, solo cumple (BA: B_AR4_mas_H1).
- **Alquiler frente a compra.** Alquiler: la población de 20-34 años es la asociación más estable entre provincias (+, en todas las submuestras), pero no se traduce en explicar la subida agregada. Compra: el crédito hipotecario nuevo (+) y el coste de uso × exposición hipotecaria (−) se asocian con el precio real dentro de muestra, sin valor predictivo (H2 no se confirma en el sellado). Lo que más pesa en ambos mercados es el componente común no explicado: desde 2020 el alquiler acumula 5,66 pp y el componente común es 5,79 pp (102 % del observado, M1); desde 2014, 7,25 pp con 10,14 pp en el común. El precio real de compra varía −4,50 pp desde 2020.
- **Política.** Tope catalán de 2020 (H5): signo contrario y fallan pretendencias. Zonas tensionadas (H6): τ = −0,0117 en ln del IPC de alquiler, p nominal 0,014, pero Holm-7 0,098; el DiD simple discrepa y hay heterogeneidad entre provincias: EXPLORATORIO.
- **Contribuciones por periodo (BD).** 19 de los componentes familia × periodo × mercado son «no robustos» (el IC95 excluye 0 solo en uno de los dos modelos o con signos opuestos): no son hallazgos.
- **Qué no se puede afirmar** (sección 11): causalidad de la inmigración, del crédito o del tope catalán; efecto causal de las zonas tensionadas; que un modelo prediga mejor que un AR(4) salvo el hecho sellado de H1; magnitudes de elasticidades.

*Fuente: `output/v2/BS/holm7.csv`; `output/v2/BA/h1_sellado.json`; `output/v2/BP/h6_sellado.json`; `output/v2/BD/tabla_resumen.csv`; `output/v2/tablas/modelos_fuera_muestra.csv`; `output/v2/tablas/registro_v2.csv`; `output/registro_busqueda.csv`.*

## 2. Datos y muestra

**Paneles (entrenamiento).** Provincial trimestral (`panel_prov_q`: 49 provincias de entrenamiento, 2002Q1-2024Q2), provincial anual, municipal anual y UE anual, más la serie nacional (`nacional_q_v2`), siempre vía `holdout.load_train`. N por rama, tal como figura en `resultado.json`:

- **BA**: N = H1_prov_trim = 3.185; provincias = 49; OOS_obs_comunes = 1.974; municipal = 1.981. Datos: panel_prov_q 2008Q1-2024Q2, 49 provincias de entrenamiento (via v2_common.load); panel_prov_a; panel_muni_a. Población interpolada intra-anual en T2-T4 (marcada); robustez con T1 observado y panel anual.
- **BV**: N = H2_principal = 3.981; provincias = 49. Datos: panel_prov_q y nacional_q_v2 (holdout.load_train), 49 provincias, 2004Q1-2024Q2; precio real = Δ4 ln p_tasado − Δ4 ln deflactor nacional (nacional_q_v2); sin muestra sellada
- **BI**: N = 621. Datos: panel_prov_a (v2_common.load), 49 provincias de entrenamiento, 2009-2021; flujos INE EM; stock por nacionalidad ECP; IPC alquiler (media anual); valor tasado real.
- **BO**: N = 879. Datos: panel_prov_a 2005-2023 (47 provincias de entrenamiento con iniciadas y suelo; iniciadas libres anuales MIVAU 32200500); panel_prov_q, nacional_q_v2 (hasta 2024Q2), panel_ue_a/q; sin muestra sellada
- **BP**: N = tratadas = 4; donantes = 45; trimestres = 32. Datos: panel_prov_q (entrenamiento), ipc_alquiler provincial (agregado_media, sin interpolación); 4 tratadas (08,17,25,43) y 45 donantes no catalanas no selladas; 2016Q1-2023Q4
- **BM**: N = A = 38; B = 2.254; C = 2.209; configuraciones = 63. Datos: nacional_q_v2 y panel_prov_q (holdout.load_train vía v2_common.load); 49 provincias de entrenamiento; orígenes 2012Q1-2023Q2; sin muestra sellada
- **BD**: N = alquiler = 3.185; compra = 3.156; provincias = 49; nacional_LP = 68; nacional_CP = 65. Datos: panel_prov_q y nacional_q_v2 vía v2_common.load; 49 provincias; 2008Q1-2024Q1 (2024Q2 sin población por fuga del sellado); sin muestra sellada

*Fuente: `output/v2/BA/resultado.json`; `output/v2/BV/resultado.json`; `output/v2/BI/resultado.json`; `output/v2/BO/resultado.json`; `output/v2/BP/resultado.json`; `output/v2/BM/resultado.json`; `output/v2/BD/resultado.json`; `docs/v2/viabilidad_g0.md`.*

**Muestra sellada.** Trimestres 2024Q3-2026Q2 (todas las provincias) y las provincias 11 (Cádiz), 16 (Cuenca) y 45 (Toledo) en todos los periodos; en paneles anuales 2025+ sellado y 2024 en embargo (`docs/v2/hipotesis.md`). Cada hipótesis con evaluación sellada (H1, H2, H6, H7) se evaluó UNA vez (registro de aperturas en `docs/v2/holdout_accesos.md`):

| Hipótesis | Rama | UTC de la evaluación | Paneles |
|---|---|---|---|
| H1 | BA | 2026-10-10T07:46:11Z | panel_prov_q, nacional_q_v2 |
| H2 | BV | 2026-10-10T07:53:11Z | panel_prov_q, nacional_q_v2 |
| H6 | BP | 2026-10-10T09:24:16Z | panel_prov_q |
| H7 | BM | 2026-10-10T09:56:19Z | panel_prov_q, nacional_q_v2 |

El sellado es **procedimental** (permisos, carga obligatoria vía `holdout.load_train`, auditoría del revisor), no un secreto físico: `data/raw` está versionado con todos los periodos. Además, los últimos 8 trimestres nacionales ya se usaron en v1, así que a escala nacional el sellado no es «virgen»; las hipótesis confirmatorias se evalúan preferentemente en las provincias selladas.

*Fuente: `docs/v2/hipotesis.md`; `docs/v2/holdout_accesos.md`; `docs/v2/decisiones.md`; `output/v2/BA/h1_sellado.json`; `output/v2/BV/h2_sellado.json`; `output/v2/BP/h6_sellado.json`; `output/v2/BM/h7_sellado.json`.*

**Periodos fijados ex ante.**

| Periodo | Trimestres | Justificación previa |
|---|---|---|
| P0 boom final | 2002Q1-2007Q4 | expansión crediticia; solo donde hay datos |
| P1 ajuste | 2008Q1-2013Q4 | crisis financiera y caída de precios |
| P2 recuperación | 2014Q1-2019Q4 | quiebre de 2014 detectado en v1 (Chow); recuperación del empleo y del crédito |
| P3 COVID | 2020Q1-2021Q4 | pandemia, moratorias, tope de rentas en Cataluña (2020Q4-2022Q1) |
| P4 subida de tipos | 2022Q1-2024Q2 | BCE sube tipos desde julio de 2022; inflación; Ley 12/2023 |
| P5 sellado | 2024Q3-2026Q2 | zonas tensionadas en Cataluña (2024), bajada de tipos; solo evaluación |

*Fuente: `docs/v2/hipotesis.md`.*

**Interpolaciones y datos no validados (solo robustez, nunca en un modelo principal sin marca).**
- Población (1 de enero) interpolada log-linealmente en T2-T4 en el panel trimestral: marcada; la robustez con T1 observado y con el panel anual coincide (`BA/resumen.md`). El padrón se publica con retraso, de modo que en tiempo real el dato no estaría disponible (`docs/v2/limitaciones.md`, C7 de BA).
- Viviendas turísticas (INE) solo desde 2020Q3 (N temporal 6 en el módulo provincial); SERPAVI municipal (extraído de visor/PDF) se usa únicamente en el módulo exploratorio de turismo de BA, no en los modelos principales.
- Vivienda protegida en el déficit: 34.704 viviendas observadas (2021Q1-2024Q2) más 14.873 viviendas **supuestas** (ritmo constante, 2024Q3-2025Q4) en la ilustración de BO; el supuesto no se usa como dato.
- Coste de uso aproximado (sin impuestos ni prima de riesgo; misma serie para todas las provincias). No hay datos provinciales de no residentes ni de inversores (`docs/v2/fuentes_fallidas.md`; licencias, titularidad catastral y AEAT: descargas fallidas).

*Fuente: `output/v2/BA/resumen.md`; `output/v2/BO/resumen.md`; `docs/v2/fuentes_fallidas.md`; `docs/v2/viabilidad_g0.md`.*

**Fugas detectadas y corregidas** (`docs/v2/decisiones.md`):
1. **Población de 2024Q2** (`pob_total`, `pob_extranj`, `pob_20_34`): se interpolaba con el dato del 1 de enero de 2025, que está sellado. Ahora es NaN en entrenamiento (método `anulado_fuga_sellado`); por eso P4 de BD termina en 2024Q1.
2. **Nivel de los índices con base 2025** (IPC alquiler, IPV, IPV nueva y usada): el INE publica en base 2025=100, de modo que los niveles de entrenamiento incorporaban información de 2025. `holdout.build` rebasa a media de 2015 = 100 por unidad antes de separar entrenamiento y sellado; las diferencias logarítmicas no cambian. Reejecutadas BA, BV, BI y BO: diferencias máximas ~1e-13 (ruido de coma flotante). H1 y H2 se evaluaron antes del rebase, con entrenamiento y sellado ambos en base 2025 (consistentes).

**Lectura indebida menor declarada por el orquestador.** Para comprobar la continuidad del rebase, el orquestador leyó en memoria el panel completo fuera de `holdout.evaluate` y mostró dos estadísticos: la media de 2015 por provincia (= 100 en las 52) y el máximo |Δln| del IPC de alquiler entre 2024Q2 y 2024Q3 entre provincias (0,0129). No se miró ningún efecto ni diferencia entre tratadas y donantes. Es un acceso indebido menor, registrado en `docs/v2/decisiones.md`; el umbral de continuidad de H7 (0,05) se fijó después de esa comprobación (limitación de BM).

*Fuente: `docs/v2/decisiones.md`; `docs/v2/limitaciones.md`.*

**Métodos y referencias metodológicas** (estado de verificación entre corchetes; detalle en la sección 12):
- Comparación fuera de muestra: Diebold-Mariano Diebold y Mariano (1995) [verificada] con la corrección de muestra finita Harvey, Leybourne y Newbold (1997) [verificada].
- Inferencia con pocos clusters: wild cluster bootstrap restringido, Roodman, Nielsen, MacKinnon y Webb (2019) [cuartil no verificado] y pesos de Webb (2023) [verificada].
- Control sintético y SDiD (H5, H6): Abadie, Diamond y Hainmueller (2010) [verificada] y Arkhangelsky et al. (2021) [verificada].
- Shift-share (H3): Goldsmith-Pinkham et al. (2020) [verificada], Borusyak, Hull y Jaravel (2022) [verificada], Adão, Kolesár y Morales (2019) [verificada]; crítica de exogeneidad y de dinámica: Jaeger, Ruist y Stuhler (2018) [verificada]; F de primera etapa: Montiel Olea y Pflueger (2013) [verificada].
- Heterogeneidad y aprendizaje automático (BI, BM): Chernozhukov et al. (2018) [verificada] y Athey, Tibshirani y Wager (2019) [verificada]; elastic net Zou y Hastie (2005) [verificada]; post-double-selection Belloni, Chernozhukov y Hansen (2014) [verificada]; ALE Apley y Zhu (2020) [verificada]; LSTM Hochreiter y Schmidhuber (1997) [verificada]; SHAP Lundberg y Lee (2017) [NO VERIFICADA] y LightGBM Ke et al. (2017) [NO VERIFICADA].
- Parámetros cambiantes y proyecciones locales (BM, BV, BO): BVAR Giannone, Lenza y Primiceri (2015) [verificada]; TVP-VAR Primiceri (2005) [verificada] con la corrección de Del Negro y Primiceri (2015) [verificada]; proyecciones locales Jordà (2005) [verificada].
- Coste de uso de la vivienda: Poterba (1984) [verificada].
- Contexto y signos esperados: demografía y alquiler Khametshin, López Rodríguez y Pérez García (2024) [verificada]; inmigración y precios Saiz (2007) [verificada]; turismo Garcia-López et al. (2020) [verificada]; tope de rentas (contratos nuevos) Jofre-Monseny, Martínez-Mazza y Segú (2023) [NO VERIFICADA]; elasticidad de la oferta citada por el Banco de España Caldera y Johansson (2013) [verificada] y Cavalleri, Cournède y Özsöğüt (2019) [verificada]; déficit de 750.000 viviendas Banco de España (2026) [verificada].

*Fuente: `docs/literatura.md`; `output/v2/tablas/referencias_v2.csv`.*

## 3. Alquiler frente a compra: qué se asocia con cada uno y por periodo

Todo en este apartado es **asociación** (EXPLORATORIO o DESCRIPTIVO). Crecimiento acumulado observado por periodo en pp de ln (alquiler nominal; valor tasado real) y coeficientes por periodo de las ecuaciones de BA y BV:

| Periodo | Alquiler observado (pp) | Compra real observada (pp) | Alquiler: coef. 20-34 [q BH] | Compra: coef. crédito [p Holm] | Compra: coef. coste de uso × exposición [p Holm] |
|---|---|---|---|---|---|
| P1 | 9,17 | −34,87 | 0,171 [0,07] | 0,0068 [1,000] | −0,0075 [<0,001] |
| P2 | 1,58 | 3,39 | 0,212 [0,01] | 0,0065 [1,000] | −0,0028 [0,151] |
| P3 | 1,74 | −2,61 | 0,178 [0,07] | 0,0065 [1,000] | −0,0129 [<0,001] |
| P4 | 3,93 | −1,88 | 0,081 [0,26] | −0,0039 [1,000] | −0,0001 [1,000] |

*Fuente: `output/v2/BD/tabla_resumen.csv`; `output/v2/BA/periodos_coef.csv`; `output/v2/BV/periodos_coeficientes_H2_FEtrim.csv`.*

**Alquiler.**
- La población de 20-34 años es la variable más estable entre provincias: positiva en P1-P3 y más débil en P4 (tabla). La población extranjera sale con signo no positivo (−0,018, IC95 [−0,054; 0,017]) cuando se condiciona a efectos de tiempo; sin ellos la asociación temporal agregada con la población extranjera sí aparece (`BA/resumen.md`), pero no se traslada a diferencias entre provincias.
- La inmigración instrumentada con shift-share (BI, 2009-2021) da un coeficiente positivo (β = 3,06) que **no resiste** los controles GPSS, los placebos de alquiler pasado ni la submuestra 2015-2021: solo el signo es estable; la magnitud no está identificada.
- Viviendas turísticas, oferta (terminadas), empleo y coste de uso: sin asociación robusta (ranking, sección 5).
- Política: zonas tensionadas de Cataluña (H6) y tope de 2020 (H5) en la sección 7.

**Compra.**
- El crédito hipotecario nuevo (+) y el coste de uso × exposición hipotecaria (−) se asocian con el crecimiento del precio real en la muestra completa, con los signos esperados, pero el crédito no es significativo en 2014-2024 ni con el crédito retardado 4 trimestres (simultaneidad), y el modelo con ambas variables no predice mejor que un AR(4) (sección 6).
- La asociación del coste de uso es fuerte en P1 y P3 y nula en P4: el alza de tipos de 2022 no se recoge con esta variable.
- Arbitraje alquiler-compra (ratio precio/alquiler 1 unidad de log por encima de su media, h = 4): precio −0,119 (Holm m=16 <0,001) y alquiler 0,021 (Holm 0,024); el ajuste es sobre todo vía precio; la desviación respecto de la media de toda la muestra incorpora reversión mecánica.
- Demografía, empleo y oferta: sin atribución estable en BD entre M1 y M2.

**Común a ambos.** Lo que más pesa es lo no explicado por las familias medidas (efectos comunes de tiempo: tipos, expectativas, inflación, regulación nacional); ver sección 4.3.

*Fuente: `output/v2/BA/resumen.md`; `output/v2/BV/resumen.md`; `output/v2/BI/resumen.md`; `output/v2/BV/arbitraje_lp.csv`; `output/v2/BA/h1_principal.csv`; `output/v2/BI/h3_principal.csv`.*

## 4. Ecuaciones principales y contribuciones por periodo

### 4.1 Alquiler (BA, H1): Δ4 ln IPC de alquiler provincial

MCO con efectos fijos de provincia y de trimestre, EE cluster por provincia (49 clusters, t con 48 gl), wild cluster bootstrap restringido (Webb, 9.999). N = 3.185, 49 provincias, 2008Q1-2024Q1 con población disponible, R² within = 0,035. Nivel: **EXPLORATORIO**.

| Variable | Coef. | EE cluster | IC95 % | p cluster | p wild bootstrap | p Holm intra-H1 (m=2) |
|---|---|---|---|---|---|---|
| Δ4 ln población 20-34 | 0,1488 | 0,0512 | [0,0458; 0,2518] | 0,006 | 0,008 | 0,015 |
| Δ4 ln población extranjera | −0,0184 | 0,0175 | [−0,0537; 0,0168] | 0,298 | 0,300 | 0,300 |
| Δ4 ln ocupados | −0,0014 | 0,0048 | [−0,0111; 0,0083] | 0,779 | 0,778 | n/d |

*Fuente: `output/v2/BA/h1_principal.csv`.*

Lectura: 1 pp más de crecimiento interanual de la población de 20-34 años se asocia con 0,15 pp más de crecimiento del alquiler (diferencial entre provincias). La parte «extranjera» de H1 no se confirma (signo opuesto, indistinguible de 0) y los ocupados no se asocian. Población interpolada en T2-T4 (marcada).

### 4.2 Compra (BV, H2): Δ4 ln valor tasado real provincial

MCO con FE de provincia y trimestre, EE cluster, bootstrap Webb 9.999. N = 3.981, 49 provincias, 2004Q1-2024Q2. Nivel: **EXPLORATORIO** (H2 no se confirma en el sellado). Magnitud: 1 unidad de coste de uso × exposición (por DE y pp) se asocia con −0,0044 pp; solo se identifica el diferencial por exposición (el nivel nacional lo absorbe el FE de trimestre).

| Variable | Coef. | EE cluster | IC95 % | p cluster | p wild bootstrap |
|---|---|---|---|---|---|
| Δ4 ln importe hipotecario | 0,0087 | 0,0027 | [0,0033; 0,0141] | 0,002 | 0,002 |
| coste de uso × exposición hip. 2005-07 (z) | −0,0044 | 0,0007 | [−0,0058; −0,0030] | <0,001 | <0,001 |
| Δ4 ln ocupados | 0,0439 | 0,0192 | [0,0053; 0,0826] | 0,027 | 0,032 |

*Fuente: `output/v2/BV/h2_resultados.csv`.*

Simultaneidad: con el crédito retardado 4 trimestres su coeficiente es 0,0019 (p wild 0,481): la asociación del crédito es contemporánea, no predictiva.

### 4.3 Contribuciones por periodo y familia (BD)

**Nivel de evidencia global: EXPLORATORIO.** Descomposición contable de asociaciones condicionales; no hay identificación causal.

Contribución = coeficiente por periodo × variación media de la familia (media ponderada por población), en pp de ln acumulados; identidad contable observado = familias + común + residuo. **M1**: efectos fijos de provincia y de trimestre (el «común» recoge lo que se mueve igual en todas las provincias). **M2**: sin efectos de tiempo, con Δ4 del coste de uso nacional. IC95 % = envolvente de bootstrap por provincias y por bloques de tiempo. P4 termina en 2024Q1 (fuga de la población de 2024Q2 corregida).

**Respuesta breve de BD** (asociaciones condicionales, EXPLORATORIO):

- **Alquiler desde 2014:** +7,25 [3,45; 11,26] pp; las familias medidas no lo explican (suma M1 −2,70 [−5,73; −0,17] pp) y el componente común/no explicado es 10,14 [5,57; 13,25] pp.
- **Alquiler desde 2020:** +5,66 [4,81; 6,58] pp; ninguna familia se distingue de 0 en M1 y M2 a la vez; ~95-100 % queda en el componente común.
- **Compra (real) desde 2014:** −1,11 [−10,23; 5,70] pp (≈0); **desde 2020:** −4,50 [−10,37; −2,56] pp (caída real). Sin atribución estable entre M1 y M2.
- Contrafactuales: efectos pequeños y con IC que incluyen 0 salvo los listados como no robustos abajo.

La demografía contribuye de forma negativa en 2014-2019 por composición, no por una asociación nueva:

> La demografía contribuye NEGATIVAMENTE en 2014-2019 (P2: población de 20-34 años en descenso, coeficiente positivo): −3,02 [−4,78; −1,31] pp en M1.
>
> — `output/v2/BD/resumen.md`


![Contribuciones por periodo](BS/contribuciones_periodo.png)

*Figura: `output/v2/BS/contribuciones_periodo.png` (datos: `output/v2/BD/tabla_resumen.csv`).*

**Alquiler, por periodo (M1).**

| Periodo | Observado | Demografía | Empleo | Crédito/CU | Oferta | Común |
|---|---|---|---|---|---|---|
| P1 | 9,17 [2,87; 16,21] | −3,24 [−6,01; −0,75] | 0,38 [−0,07; 0,83] | 0,33 [−0,23; 0,95] | −0,23 [−0,53; −0,02] | 11,73 [3,45; 18,52] |
| P2 | 1,58 [−2,15; 5,34] | −3,03 [−4,88; −1,30] | 0,17 [−0,07; 0,35] | 0,15 [−0,02; 0,35] | 0,02 [−0,01; 0,06] | 4,35 [0,71; 6,92] |
| P3 | 1,74 [1,27; 2,20] | −0,30 [−0,98; 0,23] | 0,00 [−0,15; 0,07] | −0,03 [−0,08; 0,04] | 0,01 [−0,01; 0,03] | 2,05 [1,36; 2,82] |
| P4 | 3,93 [3,23; 4,63] | 0,25 [−1,09; 1,33] | 0,08 [−0,13; 0,30] | −0,00 [−0,10; 0,08] | 0,00 [−0,01; 0,02] | 3,74 [2,52; 5,25] |

**Alquiler, ventanas acumuladas desde 2014 y desde 2020.**

| Ventana | Componente | M1 pp [IC95 %] | M2 pp [IC95 %] | Robustez M1/M2 | Nivel |
|---|---|---|---|---|---|
| P2-P4 (desde 2014) | Demografía: 20-34 | −2,67 [−4,40; −1,05] | −3,61 [−5,83; −1,15] | replica en M1 y M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Demografía: extranjera | −0,41 [−2,17; 1,03] | 0,29 [−1,49; 1,50] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Empleo (ocupados) | 0,25 [−0,05; 0,54] | 0,08 [−0,27; 0,41] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Crédito / coste de uso | 0,12 [−0,05; 0,34] | −0,24 [−1,50; 0,92] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Oferta (terminadas) | 0,03 [−0,01; 0,08] | 0,03 [−0,02; 0,08] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Política (tope CAT) | −0,01 [−0,18; 0,10] | −0,06 [−0,25; 0,08] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Suma de familias | −2,70 [−5,73; −0,17] | −3,51 [−6,75; 0,54] | contable | DESCRIPTIVO |
| P2-P4 (desde 2014) | Común (efectos de tiempo) | 10,14 [5,57; 13,25] | 11,69 [8,34; 14,11] | contable | DESCRIPTIVO |
| P2-P4 (desde 2014) | Residuo | −0,19 [−0,61; 0,28] | −0,93 [−1,55; 0,04] | contable | DESCRIPTIVO |
| P2-P4 (desde 2014) | Observado | 7,25 [3,45; 11,26] | 7,25 [3,50; 11,24] | contable | DESCRIPTIVO |
| P3-P4 (desde 2020) | Demografía: 20-34 | 0,34 [−0,11; 0,85] | 0,57 [0,09; 1,04] | NO ROBUSTO: IC95 excluye 0 solo en M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Demografía: extranjera | −0,39 [−2,15; 0,82] | 0,26 [−1,26; 1,16] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Empleo (ocupados) | 0,08 [−0,12; 0,30] | −0,00 [−0,20; 0,22] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Crédito / coste de uso | −0,03 [−0,11; 0,07] | −0,11 [−0,74; 0,52] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Oferta (terminadas) | 0,01 [−0,01; 0,05] | 0,01 [−0,01; 0,04] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Política (tope CAT) | −0,01 [−0,18; 0,10] | −0,06 [−0,25; 0,08] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Suma de familias | −0,00 [−1,93; 1,28] | 0,66 [−0,78; 1,89] | contable | DESCRIPTIVO |
| P3-P4 (desde 2020) | Común (efectos de tiempo) | 5,79 [4,16; 7,76] | 5,36 [3,92; 7,19] | contable | DESCRIPTIVO |
| P3-P4 (desde 2020) | Residuo | −0,12 [−0,54; 0,29] | −0,36 [−0,74; 0,17] | contable | DESCRIPTIVO |
| P3-P4 (desde 2020) | Observado | 5,66 [4,81; 6,58] | 5,66 [4,95; 6,55] | contable | DESCRIPTIVO |

**Compra (valor tasado real), por periodo (M1).**

| Periodo | Observado | Demografía | Empleo | Crédito/CU | Oferta | Común |
|---|---|---|---|---|---|---|
| P1 | −34,87 [−47,93; −28,08] | −7,83 [−14,69; −2,16] | −0,71 [−2,68; 1,13] | −4,18 [−7,83; −0,88] | −1,10 [−2,69; 0,55] | −18,42 [−30,03; −11,73] |
| P2 | 3,39 [−4,23; 9,40] | −7,69 [−14,47; −3,31] | 0,05 [−0,80; 1,02] | 0,34 [−0,44; 1,18] | 0,11 [−0,05; 0,55] | 7,19 [−0,52; 16,77] |
| P3 | −2,61 [−5,31; −0,82] | 0,44 [−1,92; 1,95] | 0,00 [−0,26; 0,04] | 1,44 [−0,01; 2,45] | −0,01 [−0,09; 0,05] | −4,00 [−5,38; −2,42] |
| P4 | −1,88 [−6,41; −0,43] | 0,74 [−2,10; 2,86] | 0,45 [−0,02; 1,01] | 0,50 [−0,87; 1,84] | −0,01 [−0,06; 0,03] | −3,34 [−8,96; −0,74] |

**Compra, ventanas acumuladas.**

| Ventana | Componente | M1 pp [IC95 %] | M2 pp [IC95 %] | Robustez M1/M2 | Nivel |
|---|---|---|---|---|---|
| P2-P4 (desde 2014) | Demografía: 20-34 | −7,46 [−14,84; −3,17] | −3,46 [−12,19; 1,34] | NO ROBUSTO: IC95 excluye 0 solo en M1 | EXPLORATORIO |
| P2-P4 (desde 2014) | Demografía: extranjera | 0,96 [−3,20; 5,19] | −4,08 [−10,46; −0,84] | NO ROBUSTO: IC95 excluye 0 solo en M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Empleo (ocupados) | 0,50 [−0,43; 1,61] | 1,67 [0,48; 2,96] | NO ROBUSTO: IC95 excluye 0 solo en M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Crédito / coste de uso | 2,27 [0,39; 4,81] | 0,03 [−3,26; 4,45] | NO ROBUSTO: IC95 excluye 0 solo en M1 | EXPLORATORIO |
| P2-P4 (desde 2014) | Oferta (terminadas) | 0,09 [−0,07; 0,55] | 0,10 [−0,08; 0,59] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P2-P4 (desde 2014) | Suma de familias | −3,64 [−12,14; 2,54] | −5,74 [−19,83; 2,12] | contable | DESCRIPTIVO |
| P2-P4 (desde 2014) | Común (efectos de tiempo) | −0,15 [−11,42; 9,45] | 1,95 [−10,34; 16,59] | contable | DESCRIPTIVO |
| P2-P4 (desde 2014) | Residuo | 2,68 [0,70; 4,45] | 2,68 [0,41; 4,92] | contable | DESCRIPTIVO |
| P2-P4 (desde 2014) | Observado | −1,11 [−10,23; 5,70] | −1,11 [−10,48; 6,04] | contable | DESCRIPTIVO |
| P3-P4 (desde 2020) | Demografía: 20-34 | 0,16 [−1,86; 1,41] | −1,08 [−3,34; 0,70] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Demografía: extranjera | 1,03 [−2,46; 4,04] | −4,19 [−7,40; −0,57] | NO ROBUSTO: IC95 excluye 0 solo en M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Empleo (ocupados) | 0,45 [−0,02; 0,99] | 0,77 [0,13; 1,44] | NO ROBUSTO: IC95 excluye 0 solo en M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Crédito / coste de uso | 1,93 [0,12; 3,96] | −0,00 [−1,89; 2,66] | NO ROBUSTO: IC95 excluye 0 solo en M1 | EXPLORATORIO |
| P3-P4 (desde 2020) | Oferta (terminadas) | −0,02 [−0,11; 0,05] | −0,01 [−0,11; 0,06] | sin señal: IC95 incluye 0 en M1 y M2 | EXPLORATORIO |
| P3-P4 (desde 2020) | Suma de familias | 3,55 [−0,23; 6,28] | −4,52 [−8,51; 2,04] | contable | DESCRIPTIVO |
| P3-P4 (desde 2020) | Común (efectos de tiempo) | −7,34 [−13,48; −4,27] | 0,33 [−9,74; 4,05] | contable | DESCRIPTIVO |
| P3-P4 (desde 2020) | Residuo | −0,71 [−2,00; 0,56] | −0,32 [−1,75; 1,01] | contable | DESCRIPTIVO |
| P3-P4 (desde 2020) | Observado | −4,50 [−10,37; −2,56] | −4,50 [−10,30; −2,33] | contable | DESCRIPTIVO |

*Fuente: `output/v2/tablas/contribuciones_periodo.csv`; `output/v2/BD/tabla_resumen.csv`.*

**Componentes no robustos** (IC95 que excluye 0 solo en un modelo o con signos opuestos; no son hallazgos; sin corrección por multiplicidad sobre ~14 componentes × 2 modelos):

| Mercado | Ventana | Componente | M1 [IC95 %] | M2 [IC95 %] | Motivo |
|---|---|---|---|---|---|
| alquiler | P1 | demografia | −3,24 [−6,01; −0,75] | −3,90 [−7,24; 0,18] | NO ROBUSTO: IC95 excluye 0 solo en M1 |
| alquiler | P1 | oferta | −0,23 [−0,53; −0,02] | −0,16 [−0,48; 0,10] | NO ROBUSTO: IC95 excluye 0 solo en M1 |
| alquiler | P4 | demografia_20_34 | 0,31 [−0,15; 0,73] | 0,53 [0,12; 0,95] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| alquiler | P3-P4 (desde 2020) | demografia_20_34 | 0,34 [−0,11; 0,85] | 0,57 [0,09; 1,04] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P1 | empleo_renta | −0,71 [−2,68; 1,13] | −4,19 [−6,93; −1,66] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P2 | demografia | −7,69 [−14,47; −3,31] | −2,27 [−12,43; 1,88] | NO ROBUSTO: IC95 excluye 0 solo en M1 |
| compra | P2 | demografia_20_34 | −7,62 [−15,45; −3,31] | −2,38 [−11,25; 1,66] | NO ROBUSTO: IC95 excluye 0 solo en M1 |
| compra | P3 | credito_tipos_cu | 1,44 [−0,01; 2,45] | 1,03 [0,00; 2,07] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P4 | demografia | 0,74 [−2,10; 2,86] | −4,72 [−7,32; −0,63] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P4 | empleo_renta | 0,45 [−0,02; 1,01] | 0,76 [0,11; 1,42] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P4 | demografia_extranj | 0,59 [−1,59; 2,73] | −3,67 [−7,06; −0,42] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P2-P4 (desde 2014) | empleo_renta | 0,50 [−0,43; 1,61] | 1,67 [0,48; 2,96] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P2-P4 (desde 2014) | credito_tipos_cu | 2,27 [0,39; 4,81] | 0,03 [−3,26; 4,45] | NO ROBUSTO: IC95 excluye 0 solo en M1 |
| compra | P2-P4 (desde 2014) | demografia_20_34 | −7,46 [−14,84; −3,17] | −3,46 [−12,19; 1,34] | NO ROBUSTO: IC95 excluye 0 solo en M1 |
| compra | P2-P4 (desde 2014) | demografia_extranj | 0,96 [−3,20; 5,19] | −4,08 [−10,46; −0,84] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P3-P4 (desde 2020) | demografia | 1,19 [−2,28; 4,13] | −5,27 [−8,49; −0,87] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P3-P4 (desde 2020) | empleo_renta | 0,45 [−0,02; 0,99] | 0,77 [0,13; 1,44] | NO ROBUSTO: IC95 excluye 0 solo en M2 |
| compra | P3-P4 (desde 2020) | credito_tipos_cu | 1,93 [0,12; 3,96] | −0,00 [−1,89; 2,66] | NO ROBUSTO: IC95 excluye 0 solo en M1 |
| compra | P3-P4 (desde 2020) | demografia_extranj | 1,03 [−2,46; 4,04] | −4,19 [−7,40; −0,57] | NO ROBUSTO: IC95 excluye 0 solo en M2 |

*Fuente: `output/v2/tablas/contribuciones_periodo.csv`.*

**Limitaciones de BD** (de `docs/v2/limitaciones.md`):

- Efecto de borde: Σ Δ4/4 no equivale al cambio en niveles (alquiler P2 1,58 frente a 2,30; compra P2 3,39 frente a 4,76; `observado_niveles_referencia.csv`).
- IC temporal con 2 bloques en P3 (8 trimestres) y P4 (9): poco fiable. Sin corrección por multiplicidad en ningún IC.
- Estimación MCO sin ponderar y agregación ponderada por población; población intra-anual interpolada (heredada de BA).
- Compra M2: coeficiente de Δ4 coste de uso nacional positivo (signo contrario al esperado).
- Contribuciones de M1 = b·media nacional; el «común» recoge el resto. Los canales por exposición en M1 existen solo por la ponderación. 20-34 EXPLORATORIO (Holm-7 ya ejecutado).
- ECM nacional: IC de CP por bootstrap de residuos con regresores fijos (subestima); IC de LP por simulación con covarianza HAC(4).
- BD (corrección C1): la contribución de `cu_x_expo` se mide como (coste de uso − media muestral del coste de uso) × exposición; la estimación usa la variable sin centrar (centrar por periodo no es neutro). Cambian solo las cifras de compra (M1 P2-P4 crédito/coste de uso: +2,27 pp, antes +0,13).

*Fuente: `docs/v2/limitaciones.md`.*

## 5. Ranking de factores y nivel de evidencia

Criterios (A-E) por familia y mercado: **A** p ajustado por multiplicidad < 0,05 (Holm/BH intra-rama o Holm-7); **B** signo estable en submuestras o periodos; **C** mejora predictiva significativa frente al AR(4) en validación de entrenamiento; **D** mejora significativa frente al AR(4) en la muestra sellada; **E** contribución de BD replicada en M1 y M2 desde 2020 (IC95 excluye 0, mismo signo). «n/a» = no evaluable. La puntuación (nº de criterios cumplidos) ordena la tabla; es un resumen descriptivo, no un contraste. **Ninguna familia supera el nivel EXPLORATORIO** (tope fijado por el orquestador: ninguna confirmatoria sobrevive a Holm-7); lo no explicado y el déficit son DESCRIPTIVO.

| rango | familia | mercado | nivel | A | B | C | D | E | cumple | evaluables |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Coste de uso × exposición hipotecaria | compra | EXPLORATORIO | sí | sí | no | no | no | 2 | 5 |
| 2 | Demografía: modelo conjunto de H1 (valor predictivo) | alquiler | EXPLORATORIO | n/a | n/a | no | sí | n/a | 1 | 2 |
| 3 | Precio/alquiler (arbitraje, ratio vs media) | alquiler | EXPLORATORIO | sí | sí | n/a | n/a | n/a | 1 | 2 |
| 4 | Precio/alquiler (arbitraje, ratio vs media) | compra | EXPLORATORIO | sí | sí | n/a | n/a | n/a | 1 | 2 |
| 5 | Política: zonas tensionadas de Cataluña (H6) | alquiler | EXPLORATORIO | no | no | n/a | sí | n/a | 1 | 3 |
| 6 | Demografía: población 20-34 (BA) | alquiler | EXPLORATORIO | sí | sí | no | n/a | no | 1 | 4 |
| 7 | Crédito hipotecario nuevo | compra | EXPLORATORIO | sí | no | no | no | no | 1 | 5 |
| 8 | Viviendas turísticas (VUT) | alquiler | EXPLORATORIO | no | n/a | n/a | n/a | n/a | 0 | 1 |
| 9 | Crédito, tipos y coste de uso | alquiler | EXPLORATORIO | n/a | n/a | no | n/a | no | 0 | 2 |
| 10 | Oferta (terminadas) | alquiler | EXPLORATORIO | n/a | n/a | no | n/a | no | 0 | 2 |
| 11 | Demografía (20-34 y extranjera) | compra | EXPLORATORIO | n/a | no | n/a | n/a | no | 0 | 2 |
| 12 | Inmigración instrumentada (BI) | compra | EXPLORATORIO | no | no | n/a | n/a | n/a | 0 | 2 |
| 13 | Oferta (terminadas / iniciadas) | compra | EXPLORATORIO | n/a | n/a | no | n/a | no | 0 | 2 |
| 14 | Suelo (precio del suelo) | compra | EXPLORATORIO | no | n/a | no | n/a | n/a | 0 | 2 |
| 15 | Población extranjera (BA, MCO con FE) | alquiler | EXPLORATORIO | no | no | n/a | n/a | no | 0 | 3 |
| 16 | Inmigración instrumentada, shift-share 2002 (BI) | alquiler | EXPLORATORIO | sí | no | no | n/a | n/a | 0 | 3 |
| 17 | Empleo (ocupados) | alquiler | EXPLORATORIO | no | no | n/a | n/a | no | 0 | 3 |
| 18 | Política: tope de rentas de Cataluña (H5) | alquiler | EXPLORATORIO | no | no | n/a | n/a | no | 0 | 3 |
| 19 | Empleo (ocupados) | compra | EXPLORATORIO | no | n/a | no | n/a | no | 0 | 3 |
| 20 | No explicado: efectos comunes de tiempo (tipos, expectativas, inflación…) | alquiler | DESCRIPTIVO | n/a | n/a | n/a | n/a | n/a | 0 | 0 |
| 21 | No explicado: efectos comunes de tiempo (tipos, expectativas, inflación…) | compra | DESCRIPTIVO | n/a | n/a | n/a | n/a | n/a | 0 | 0 |
| 22 | Déficit acumulado de vivienda (oferta − hogares) | ambos | DESCRIPTIVO | n/a | n/a | n/a | n/a | n/a | 0 | 0 |

*Fuente: `output/v2/tablas/ranking_factores.csv`.*

**Por qué (con la cifra de origen):**

- **1. Coste de uso × exposición hipotecaria (compra)**: Coef. −0,0044 (Holm m=2 <0,001), significativo en ambas submuestras; el modelo C3 es peor que el AR(4) en entrenamiento (p 0,117) y no mejora en el sellado; solo se identifica el diferencial por exposición (no aleatoria); en BD M2 el coste de uso nacional sale con signo contrario.
- **2. Demografía: modelo conjunto de H1 (valor predictivo) (alquiler)**: Hecho fuera de muestra: en la muestra sellada mejora al AR(4) (RMSE 0,0108 vs 0,0122; p 0,005); ×7 = 0,037; en entrenamiento no mejoraba (p 0,645). No se atribuye a un coeficiente concreto; H1 conjunta EXPLORATORIO.
- **3. Precio/alquiler (arbitraje, ratio vs media) (alquiler)**: Ratio por encima de la media predice más alquiler (h=4: 0,021, Holm 0,024); con media expansiva Holm 0,115; reversión mecánica posible.
- **4. Precio/alquiler (arbitraje, ratio vs media) (compra)**: Ratio por encima de la media predice menos crecimiento del precio (h=4: −0,119, Holm <0,001); con media expansiva −0,065 (Holm 0,213); reversión mecánica posible.
- **5. Política: zonas tensionadas de Cataluña (H6) (alquiler)**: τ SDiD −0,0117, p nominal 0,014 (cumple la regla), Holm-7 0,098; DiD simple de signo contrario y Tarragona positiva.
- **6. Demografía: población 20-34 (BA) (alquiler)**: Coef. 0,149 (Holm intra-H1 0,0154), + en todas las submuestras; el modelo no mejora al AR(4) en entrenamiento (p 0,645); en BD desde 2020 no replica entre M1 y M2; H1 (conjunta) no supera Holm-7 (1,000): tope EXPLORATORIO.
- **7. Crédito hipotecario nuevo (compra)**: Coef. 0,0087 (Holm m=2 0,0018); no significativo en 2014-2024 (p 0,198) ni con crédito retardado; H2 no se confirma en el sellado (p 0,195); simultaneidad.
- **8. Viviendas turísticas (VUT) (alquiler)**: Depende de la métrica: municipal p 0,252, provincial Δ ln VUT p 0,396, provincial Δ por 1.000 hab. p 0,0007 (N temporal 6); causalidad inversa no descartada.
- **9. Crédito, tipos y coste de uso (alquiler)**: Coste de uso = una serie nacional única (IC subestimados, sin ajuste); el modelo D no mejora al AR(4) (p 0,129); BD sin señal.
- **10. Oferta (terminadas) (alquiler)**: Contribuciones del orden de décimas de pp; signo + en P1 (contrario al esperado); el modelo C no mejora al AR(4) (p 0,585).
- **11. Demografía (20-34 y extranjera) (compra)**: En BD desde 2020 la contribución cambia de signo entre M1 (1,19 pp) y M2 (−5,27 pp): sin atribución estable.
- **12. Inmigración instrumentada (BI) (compra)**: β compra −1,04 (p WCB 1 cola 0,661), IC95 muy ancho; el signo cambia entre variantes.
- **13. Oferta (terminadas / iniciadas) (compra)**: Contribución ≈ 0 en BD; ningún modelo de precio con oferta mejora al AR(4) (P4 p 0,208).
- **14. Suelo (precio del suelo) (compra)**: Serie cruda sin señal (mín. Holm 1,00); solo la variante «media4T», añadida a posteriori, da Holm 0,021 en P4 (h=6); P2 no mejora al AR(4) (p 0,609).
- **15. Población extranjera (BA, MCO con FE) (alquiler)**: Coef. −0,018 (p Holm 0,300): signo opuesto al esperado; IC95 incluye 0; no replica en BD.
- **16. Inmigración instrumentada, shift-share 2002 (BI) (alquiler)**: β alquiler 3,06 (p WCB 1 cola 0,001) pero con GPSS de extranjeros 2002 (p 0,078) y 2015-2021 (p 0,059) pierde significación; placebos de alquiler pasado rechazan; magnitud no identificada; H3 no supera Holm-7 (0,176).
- **17. Empleo (ocupados) (alquiler)**: Coef. −0,0014 (p bootstrap 0,778); el signo cambia entre periodos.
- **18. Política: tope de rentas de Cataluña (H5) (alquiler)**: Signo contrario al esperado (p una cola − = 0,968); fallan pretendencias y placebo en el tiempo (p 0,009).
- **19. Empleo (ocupados) (compra)**: Coef. 0,044; p bootstrap 0,032 sin ajuste (no forma parte de Holm de H2); el modelo con ocupados no mejora al AR(4).
- **20. No explicado: efectos comunes de tiempo (tipos, expectativas, inflación…) (alquiler)**: Desde 2020 el componente común es 5,79 pp de 5,66 pp observados en M1 (102 %): las familias medidas no explican la subida.
- **21. No explicado: efectos comunes de tiempo (tipos, expectativas, inflación…) (compra)**: Desde 2020 el real cae −4,50 pp; el común es −7,34 pp en M1 y 0,33 pp en M2: sin atribución estable.
- **22. Déficit acumulado de vivienda (oferta − hogares) (ambos)**: EPA corregida 2021Q1-2024Q2: 632.861 sin protegida; no comparable con el periodo 2021-2025 del BdE; la protegida incluye supuestos en la ilustración.

*Fuente: `output/v2/tablas/ranking_factores.csv (columna fuentes de cada fila)`.*

## 6. Modelos fuera de muestra frente a AR(4) y ECM v1

Todo en la misma muestra por contraste, h = 4 trimestres (anual en BI), DM con corrección Harvey-Leybourne-Newbold (DM > 0 = el modelo es mejor que la base). Detalle de los 109 modelos y evaluaciones: `output/v2/tablas/modelos_fuera_muestra.csv`.

### 6.1 Validación en bloques con embargo (entrenamiento ≤ 2024Q2; informativa)

| Rama | Objetivo | Config. | Mejor RMSE (modelo) | N | RMSE | RMSE AR(4) | RMSE ECM v1 | DM vs AR(4) | p | p BH | Mejoran al AR(4) con BH |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BA | Δ4 ln IPC alquiler (panel provincial, 49 prov.) | 4 | C_AR4_H1_oferta | 1.974 | 0,0116 | 0,0124 | 0,0142 | 0,55 | 0,585 | 0,645 | 0 |
| BV | Δ4 ln valor tasado real (panel provincial, 49 prov.) | 6 | BV_C1 | 2.209 | 0,0413 | 0,0418 | 0,0809 | 0,28 | 0,779 | 0,850 | 0 |
| BV | Δ4 ln valor tasado real (nacional) | 4 | BV_N2 | 46 | 0,0349 | 0,0274 | 0,0693 | −2,00 | 0,052 | 0,139 | 0 |
| BO | precio real | 4 | P2_suelo | 1.211 | 0,0404 | 0,0394 | 0,0647 | −0,52 | 0,609 | 0,609 | 0 |
| BO | iniciadas (4T) | 2 | I2_precio_suelo | 1.025 | 0,5064 | 0,5262 | n/d | 2,39 | 0,026 | 0,097 | 0 |
| BI | Δ ln IPC alquiler (panel provincial anual) | 2 | AR4+flujo_t+1 (contemporáneo, NO pronóstico) | 392 | 0,0080 | 0,0107 | n/d | 2,28 | 0,056 | 0,113 | 0 |
| BM | ln IPV real (nacional) | 21 | TVPVAR_k0.95 | 38 | 0,0726 | 0,0699 | 0,1094 | −0,31 | 0,760 | 0,760 | 0 |
| BM | Δ4 ln IPC alquiler (panel provincial) | 19 | LGBM_nl4_n400 | 2.254 | 0,0124 | 0,0154 | 0,0168 | 0,94 | 0,353 | 0,989 | 0 |
| BM | Δ4 ln valor tasado real (panel provincial) | 19 | EN_l10.7_a0.4 | 2.209 | 0,0528 | 0,0418 | 0,0809 | −1,32 | 0,194 | 0,194 | 0 |

*Fuente: `output/v2/tablas/modelos_fuera_muestra.csv`.*

De 85 filas de modelos con variables (incluidas 4 configuraciones de LSTM), **0 mejoran al AR(4) con BH** (2 con p < 0,05 sin corregir: BO I1_precio (p 0,032, p BH 0,097); BO I2_precio_suelo (p 0,026, p BH 0,097), que tampoco sobreviven a BH). El ECM v1 es peor que el AR(4) en los tres objetivos de BM: mejorarlo es un listón bajo. El LSTM no supera al gradient boosting (RMSE 0,0141 frente a 0,0124; DM −0,84; p = 0,404): resultado negativo.

### 6.2 Muestra sellada (una evaluación por hipótesis; principal = 52 provincias, 2024Q3-2026Q2)

| Rama | Modelo | Objetivo | N | RMSE | RMSE AR(4) | DM vs AR(4) | p | p BH (5 sellados) | RMSE ECM v1 | DM vs ECM v1 | p ECM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BA | B_AR4_mas_H1 | Δ4 ln IPC alquiler (panel provincial) | 416 | 0,0108 | 0,0122 | 3,98 | 0,005 | 0,026 | 0,0123 | 2,70 | 0,031 |
| BV | BV_C3 | Δ4 ln valor tasado real (panel provincial) | 416 | 0,0546 | 0,0619 | 1,43 | 0,195 | 0,487 | n/d | n/d | n/d |
| BM | TVPVAR_k0.95 | ln IPV real (nacional) | 8 | 0,0722 | 0,0508 | −1,12 | 0,300 | 0,500 | 0,0128 | −6,74 | <0,001 |
| BM | LGBM_nl4_n400 | Δ4 ln IPC alquiler (panel provincial) | 416 | 0,0111 | 0,0122 | 0,71 | 0,499 | 0,624 | 0,0123 | 1,37 | 0,212 |
| BM | EN_l10.7_a0.4 | Δ4 ln valor tasado real (panel provincial) | 416 | 0,0655 | 0,0619 | −0,28 | 0,786 | 0,786 | 0,0528 | −0,73 | 0,491 |

*Fuente: `output/v2/BA/h1_sellado.json`; `output/v2/BV/h2_sellado.json`; `output/v2/BM/h7_sellado.json`; `output/v2/tablas/modelos_fuera_muestra.csv`.*

**Lectura.** Ningún modelo supera al AR(4) salvo la mejora sellada del modelo demográfico de alquiler (BA: B_AR4_mas_H1). En las 3 provincias selladas solas (n = 24) esa mejora no es significativa (p = 0,589): la potencia es baja y el resultado descansa en las 49 provincias de entrenamiento evaluadas en 2024Q3-2026Q2. En entrenamiento el mismo modelo no mejoraba (p = 0,645). H2 (C3) y H7 (A, B, C) no cumplen la regla.

**Observación NO pre-registrada (no se usa como evidencia).** En la ventana sellada nacional (n = 8) el ECM v1 tuvo RMSE 0,0128 frente a 0,0508 del AR(4) y 0,0722 del TVP-VAR elegido para H7. Con n = 8 y sin que se hubiera fijado de antemano, no se interpreta; en entrenamiento el ECM v1 era peor que el AR(4) en los tres objetivos.

*Fuente: `output/v2/BM/h7_sellado.json`; `output/v2/BM/resumen.md`.*

## 7. Hipótesis confirmatorias y Holm-7

Familia de 7 hipótesis pre-registradas (`docs/v2/hipotesis.md`, tag `prereg-v2`). p de cada hipótesis = la decisión pre-registrada: las conjunciones se contrastan por intersección-unión (máximo de los p componentes) y, con evaluación sellada, el p conjunto es el máximo entre dentro de muestra y sellado. Holm sobre las 7. **Ninguna supera Holm al 5 %.** Todas EXPLORATORIO.

| Id | Signo esperado | Estimación | IC95 % | p dentro de muestra | p sellado | p hipótesis (IUT/máx.) | p Holm-7 | Nivel |
|---|---|---|---|---|---|---|---|---|
| H1 | + | pob 20-34 0,149; pob extranjera −0,018; ocupados −0,001 | 20-34 [0,046; 0,252]; extranjera [−0,054; 0,017] | 0,8499 | 0,0053 | 0,8499 | 1,0000 | EXPLORATORIO |
| H2 | + crédito / − coste de uso | crédito hipotecario 0,0087; coste de uso × exposición −0,0044; ocupados 0,044 | crédito [0,0033; 0,0141]; coste de uso [−0,0058; −0,0030] | 0,0018 | 0,1947 | 0,1947 | 0,7787 | EXPLORATORIO |
| H3 | β_alquiler > 0 y β_alquiler > β_compra | β alquiler 3,06; β compra −1,04; alquiler − compra 4,10 | alquiler [1,14; 4,98]; contraste [−0,33; 8,52] | 0,0294 | n/d | 0,0294 | 0,1764 | EXPLORATORIO |
| H4 | + ; interacción − con ln p_suelo | β precio 0,794; β precio × ln suelo −0,616 | precio [0,110; 1,479]; interacción [−1,292; 0,059] | 0,0463 | n/d | 0,0463 | 0,2315 | EXPLORATORIO |
| H5 | − | τ SDiD 2020Q4-2022Q1 (ln IPC alquiler) +0,0037 | [−0,0002; 0,0076] | 0,9680 | n/d | 0,9680 | 1,0000 | EXPLORATORIO |
| H6 | − | τ SDiD 2024Q3-2026Q2 (ln IPC alquiler) −0,0117 | [−0,0210; −0,0023] | n/d | 0,0140 | 0,0140 | 0,0979 | EXPLORATORIO |
| H7 | mejora del RMSE | A: RMSE 0,0722 vs AR(4) 0,0508; B: RMSE 0,0111 vs AR(4) 0,0122; C: RMSE 0,0655 vs AR(4) 0,0619 | n/a (contraste de predicción) | n/d | 1,0000 | 1,0000 | 1,0000 | EXPLORATORIO |

*Fuente: `output/v2/tablas/hipotesis_confirmatorias.csv`; `output/v2/BS/holm7.csv`.*

- **H1 (BA)**: NO confirmada como conjunción de signos (extranjera con signo opuesto; p_IUT 0,850). Hecho fuera de muestra: el modelo con las variables de H1 mejora al AR(4) en la muestra sellada (RMSE 0,0108 vs 0,0122; DM-HLN 3,98; p 0,005) y al ECM v1 (p 0,031); p conjunto (máximo) 0,850; no supera Holm-7. El p sellado ×7 = 0,037 no convierte la mejora predictiva en asociación robusta de cada coeficiente.
- **H2 (BV)**: NO confirmada en la muestra sellada: C3 RMSE 0,0546 vs AR(4) 0,0619; DM-HLN 1,43; p 0,195 (regla: mejora significativa). Signos dentro de muestra como los esperados (p_IUT 0,002). Simultaneidad: con el crédito retardado 4 trimestres el coeficiente no es significativo (BV/h2_resultados.csv).
- **H3 (BI)**: p_IUT nominal 0,0294 < 0,05 pero no supera Holm-7 (0,176); el IC95 del contraste incluye 0; GPSS, placebos, timing y submuestras lo debilitan; magnitud no identificada. Sin evaluación sellada posible (flujos hasta 2021-2022). Identificación NO superada: CAUSAL descartado.
- **H4 (BO)**: p_IUT nominal 0,0463 < 0,05 pero no supera Holm-7 (0,232); falla submuestras 2005-2013 y 2014-2023; el IV no la respalda (J rechaza); placebo de precio futuro significativo. Sin evaluación sellada. Asociación exploratoria; elasticidad no estructural.
- **H5 (BP)**: NO confirmada: signo contrario al esperado (p una cola del signo − = 0,968; bilateral 0,065); fallan pretendencias y placebo en el tiempo. Un nulo no prueba ausencia de efecto: el IPC provincial diluye el tratamiento (BP/resultado.json, notas).
- **H6 (BP)**: Cumple la regla pre-registrada nominalmente (τ<0, p de permutación bilateral 0,014) pero NO supera Holm-7 (0,098). Discrepancias: control sintético −0,0121 (p 0,044) coincide; DiD simple +0,0238 (signo contrario); heterogeneidad por provincia; sin 2023Q3-Q4 en el pre p 0,067. Efecto estimado por debajo del MDE declarado (≈1,7 %); paquete regulatorio catalán coetáneo: mide «Cataluña 2024-2026», no la zona tensionada aislada.
- **H7 (BM)**: NO confirmada: ningún objetivo cumple la regla (p_IUT Holm m=3 = 1,000; 1,000; 1,000). Observación NO pre-registrada, no usada como evidencia: en la ventana sellada nacional (n=8) el ECM v1 tuvo RMSE 0,0128 frente a 0,0508 del AR(4).

*Fuente: `output/v2/tablas/hipotesis_confirmatorias.csv`.*

**Verificación de los p transcritos.** La versión previa de `src/v2/holm7.py` traía transcritos los p dentro de muestra de H1-H5; ahora se leen de los ficheros de cada rama y se contrastan:

| Id | p transcrito en la versión previa | p leído del fichero | Diferencia |
|---|---|---|---|
| H1 | 0,8500 | 0,8499 | −0,0001 |
| H2 | 0,0018 | 0,0018 | +0,0000 |
| H3 | 0,0290 | 0,0294 | +0,0004 |
| H4 | 0,0460 | 0,0463 | +0,0003 |
| H5 | 0,9700 | 0,9680 | −0,0020 |

Todos coinciden salvo redondeo; se usa el valor del fichero. El único efecto visible es H3: el fichero da 0,0294 (la versión previa 0,029), de modo que su p Holm-7 es 0,1764 y no 0,174 (en `docs/v2/decisiones.md` figura «0,17»); la conclusión no cambia. Del mismo modo, el p sellado de H1 ×7 es 0,037 con el p exacto del fichero (en `docs/v2/decisiones.md` figura 0,035, con el p redondeado a 0,005).

*Fuente: `output/v2/BS/holm7_verificacion.csv`; `output/v2/BS/holm7.csv`.*

**Etiquetas finales (fijadas por el orquestador).** Ninguna hipótesis confirmatoria alcanza ASOCIACIÓN ROBUSTA ni CAUSAL. H1 (conjunta) EXPLORATORIO; se reporta como HECHO fuera de muestra que el modelo demográfico de alquiler mejora al AR(4) y al ECM v1 en la muestra sellada, sin convertirlo en asociación robusta de cada coeficiente. H6 EXPLORATORIO (SDiD y control sintético coinciden; el DiD simple discrepa; heterogeneidad por provincia). H2, H3, H4, H5 y H7 EXPLORATORIO o no confirmadas. Todo lo demás EXPLORATORIO o DESCRIPTIVO (`docs/v2/decisiones.md`).

*Fuente: `docs/v2/decisiones.md`.*

## 8. Qué cambió respecto de v1 y por qué

| Aspecto | v1 | v2 | Por qué cambia / lectura |
|---|---|---|---|
| Unidad de análisis y N | Serie nacional trimestral: LP N=72, CP N=73; panel de 17 CCAA anual | Paneles provinciales: alquiler N=3.185 y compra N=3.981 (49 provincias, trimestral); BI N=621; BO N=879 | Más N y heterogeneidad; riesgo de interpolación de población en T2-T4 |
| Escala de evidencia | «asociación» (ninguna pregunta alcanzó el nivel causal) | CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO; 7 confirmatorias pre-registradas con Holm-7 | Pre-registro (tag `prereg-v2`) y muestra sellada: separa confirmación de exploración |
| Especificaciones probadas | 3.812 | 34 | Corrección por búsqueda: Holm/BH por familia y Holm-7 |
| Inmigración y alquiler | OLS IPC alquiler 0,534 (p WCB 0,004); panel de 17 CCAA, 2003-2025; 2SLS 0,437 (p WCB 0,119) | 2SLS β alquiler 3,06 (p WCB 0,001); con GPSS de extranjeros 2002 1,95 (p cluster 0,115); placebo de alquiler pasado rechaza | Con paneles provinciales, GPSS y placebos la inmigración **ya no es una asociación robusta con el alquiler**: solo el signo + es estable; magnitud no identificada; CAUSAL descartado |
| Déficit de vivienda | 866.100 (2021T1-2025T4, EPA corregida, sin protegida); 810.936 (ECP) | 632.861 sin protegida y 598.157 con protegida (2021Q1-2024Q2, observadas) | No comparable (periodo más corto por el sellado); con/sin protegida se separan observadas y supuestas; DESCRIPTIVO |
| Predicción | El modelo preferido no mejora al AR(4) (DM p = 0,509) | Ninguna configuración mejora al AR(4) en validación (BH); solo H1 mejora en el sellado | Validación en bloques con embargo y evaluación sellada única |
| Caldera y Johansson (2013) | NO VERIFICADA | VERIFICADA | DOI comprobado en Crossref en v2; el informe v1 no se modifica |
| Quiebres | Chow 2014Q1; modelo no estable | Periodos P0-P5 fijados ex ante; coeficientes por periodo y contribuciones con IC | Se pregunta por los periodos en vez de detectarlos |

*Fuente: `output/informe.md`; `output/tablas/ecuacion_final_lp.csv`; `output/tablas/ecuacion_final_cp.csv`; `output/tablas/inmigracion_iv.csv`; `output/tablas/deficit.csv`; `output/tablas/referencias.csv`; `output/registro_busqueda.csv`; `output/v2/BI/h3_principal.csv`; `output/v2/BI/h3_identificacion.csv`; `output/v2/BO/deficit_nacional.csv`; `docs/literatura.md`.*

Cavalleri, Cournède y Özsöğüt (2019) sigue como parcialmente verificada (DOI existe; autores y número no confirmados). El estudio de València de v1 no se repite en v2 (los paneles son provinciales): sus conclusiones siguen siendo las de v1.

## 9. Resultados negativos (se reportan igual que los positivos)

- **H2 no se confirma en el sellado.** C3 RMSE 0,0546 frente a 0,0619 del AR(4), DM-HLN 1,43, p = 0,195. En entrenamiento C3 ya era peor que el AR(4) (`BV/oos_panel.csv`). Los signos dentro de muestra (crédito +, coste de uso × exposición −) quedan EXPLORATORIO. *(`BV/h2_sellado.json`)*
- **H5 (tope catalán de 2020).** Efecto SDiD +0,0037 (signo contrario; p de permutación una cola del signo − = 0,968); placebo en el tiempo (2018Q4) p = 0,009 y pendiente de pretendencia p = 0,040: las tratadas ya divergían antes. El IPC provincial diluye el tratamiento: un nulo no prueba ausencia de efecto. *(`BP/resultado.json`)*
- **H7.** Ningún objetivo cumple la regla: A (nacional, TVP-VAR) 0,0722 frente a 0,0508; B (alquiler, LightGBM) 0,0111 frente a 0,0122 (p = 0,499); C (compra, elastic net) 0,0655 frente a 0,0619. *(`BM/h7_sellado.json`)*
- **LSTM.** RMSE 0,0141 frente a 0,0124 del gradient boosting; DM −0,84 (p = 0,404); la selección del mejor LSTM entre 4 configuraciones es además optimista. *(`BM/lstm_resultado.json`)*
- **H4 (oferta).** Falla submuestras: sin signos esperados en precio_lag2 (p_IUT 0,615), 2005-2013 (p_IUT 0,884), 2014-2023 (p_IUT 0,631); el IV no la respalda (J de Hansen rechaza) y el placebo de precio futuro es significativo. *(`BO/h4_robustez_submuestras.csv`, `BO/resumen.md`)*
- **H3 con pocos grupos.** BHJ a nivel de shock (8 grupos × 13 años, t(7)): alquiler 3.99 (p=0.000); precio 2.90 (p=0.55). Con 8 shocks la potencia y la inferencia son pobres: no aporta evidencia de exogeneidad de los shocks. *(`BI/resumen.md`)*
- **Suelo.** La serie cruda no da señal (mínimo p Holm sobre 160 contrastes = 1,00); la variante «media4T», añadida a posteriori, da p Holm = 0,021 solo en P4 (h = 6, n pequeña): no es una señal anticipatoria robusta. *(`BO/suelo_proyecciones_locales.csv`)*
- **Turismo (VUT).** Municipal: coef. 0,00035 (p = 0,252), placebo de pretendencia p = 0,814; provincial: Δ ln VUT p = 0,396 frente a Δ por 1.000 hab. p = 0,0007 con N temporal 6: depende de la métrica. *(`BA/turismo.csv`)*
- **Panel UE.** Elasticidad de los permisos al precio real (t−1), anual: España 1,91 (EE HAC 1,23) frente a 0,99 de media UE (26 países, EE 0,21); España es la 5.ª más alta de 27. Panel con FE país y año: 1,69 (España) frente a 0,62 (resto); no se dan p ni EE de la diferencia (España es un único clúster: inferencia cluster no válida). Trimestral: 1,27 frente a 0,57 (HICP general trimestral «anual_asignado»). Alquiler: España −6,0 frente a +2,7 de media UE, la más baja; el valor lo generan dos episodios en que el alquiler real y los permisos se mueven en sentido contrario (2008-2010 y 2021-2023, con la inflación general alta); no interpretar. Series de 11-18 años: elasticidades por país imprecisas. *(`BO/resumen.md`, sección 4)*
- **Importancias SHAP / permutación / ALE (BM).** Provienen de modelos que no mejoran al AR(4): no son explicación y la colinealidad reparte las importancias de forma arbitraria. *(`BM/resumen.md`)*

*Fuente: `output/v2/BV/h2_sellado.json`; `output/v2/BP/resultado.json`; `output/v2/BM/h7_sellado.json`; `output/v2/BM/lstm_resultado.json`; `output/v2/BO/resumen.md`; `output/v2/BI/resumen.md`; `output/v2/BA/turismo.csv`.*

## 10. Limitaciones (priorizadas)

La prioridad es un ordenamiento de BS según su efecto sobre la inferencia; el texto procede de `docs/v2/limitaciones.md` (limitaciones de v1 en `docs/limitaciones.md` siguen vigentes para las series nacionales).

**Prioridad 1 · identificación e inferencia (invalidan lecturas causales o la confirmación)**

*BI (inmigración) — aprobada en re-revisión*

- La identificación descansa en las cuotas 2002 de Sudamérica (68 % del peso de Rotemberg), correlacionadas con el tamaño, el precio y el enclave extranjero de 2002: la exogeneidad de las cuotas no es creíble; con los controles GPSS (extranjeros 2002 × año) β_alquiler deja de ser significativo y con todos los controles F = 4,3.
- Los placebos (alquiler y precio pasados sobre el flujo instrumentado de t) rechazan con fuerza: el diseño no separa el efecto del flujo de t de ajustes acumulados o tendencias provinciales (problema de Jaeger, Ruist y Stuhler 2018).
- Las pretendencias 2003-2007 no son pre-tratamiento (boom de llegadas a los mismos enclaves) y no informan.
- 8 agrupaciones de países: BHJ/AKM con poca potencia; Sargan rechaza en la ecuación de precio.
- Submuestra 2009-2014 sin primera etapa (F 0,7); 2015-2021, p=0,073. β_alquiler>0 y H3 quedan EXPLORATORIO; la magnitud (0,8-5) no está identificada.
- Flujos de inmigración provinciales solo hasta 2021-2022: sin evaluación sellada posible.

*BV (compra) — aprobada en re-revisión*

- El secundario (b′) de evaluar_H2 llega a orígenes 2023Q4 y solapa dos trimestres con la ventana sellada.
- Potencia baja en la evaluación sellada; en entrenamiento el modelo pre-registrado C3 es peor que el AR(4) de panel (RMSE 0,0605 vs 0,0418).
- Simultaneidad del crédito con el precio (con el crédito retardado 4 trimestres el coeficiente no es significativo); coste de uso aproximado (sin impuestos ni depreciación).
- No residentes: sin datos provinciales.

**Prioridad 2 · datos y medición (condicionan magnitudes)**

*BA (alquiler) — aprobada en re-revisión*

- C6: el criterio de signos y la elección del modelo primario fuera de muestra no son auditables como fijados de antemano (no estaban en el pre-registro con ese detalle).
- C7: la población del modelo principal está interpolada intra-anual (T2-T4) y el padrón se publica con retraso: en tiempo real el dato no estaría disponible.
- C8: módulo de turismo con solo 6 periodos y corrección BH parcial; la población extranjera sale con signo negativo en 2008-2019.

*BO (oferta y suelo) — aprobada en re-revisión*

- H4 inestable y endógena: falla en 2005-2013 y 2014-2023; el IV con desplazadores de demanda no la respalda (J rechaza); el placebo de precio futuro es significativo (ciclo común). EXPLORATORIO.
- Oferta medida con viviendas LIBRES iniciadas/terminadas (no totales); sin licencias municipales.
- Déficit 2021Q1-2024Q2: incluye 14.873 viviendas protegidas SUPUESTAS (ritmo constante) además de las 34.704 observadas; no comparable con el periodo 2021-2025 del BdE.
- Suelo: serie ruidosa; sin señal anticipatoria robusta tras BH/Holm sobre 160 contrastes.
- Panel UE: sin inferencia válida para la comparación de España (un único clúster); el resultado de alquiler (−6) lo producen 2008-2010 y 2021-2023.
- Fuera de muestra: ningún modelo de precio con variables de oferta mejora al AR(4); el de iniciadas mejora (p 0,03) pero no sobrevive a BH.

*BD (descomposición por periodos) — iteración 2*

- Efecto de borde: Σ Δ4/4 no equivale al cambio en niveles (alquiler P2 1,58 frente a 2,30; compra P2 3,39 frente a 4,76; `observado_niveles_referencia.csv`).
- IC temporal con 2 bloques en P3 (8 trimestres) y P4 (9): poco fiable. Sin corrección por multiplicidad en ningún IC.
- Estimación MCO sin ponderar y agregación ponderada por población; población intra-anual interpolada (heredada de BA).
- Compra M2: coeficiente de Δ4 coste de uso nacional positivo (signo contrario al esperado).
- Contribuciones de M1 = b·media nacional; el «común» recoge el resto. Los canales por exposición en M1 existen solo por la ponderación. 20-34 EXPLORATORIO (Holm-7 ya ejecutado).
- ECM nacional: IC de CP por bootstrap de residuos con regresores fijos (subestima); IC de LP por simulación con covarianza HAC(4).
- BD (corrección C1): la contribución de `cu_x_expo` se mide como (coste de uso − media muestral del coste de uso) × exposición; la estimación usa la variable sin centrar (centrar por periodo no es neutro). Cambian solo las cifras de compra (M1 P2-P4 crédito/coste de uso: +2,27 pp, antes +0,13).

**Prioridad 3 · potencia y modelos predictivos**

*BM (modelos) — aprobada en re-revisión*

- Ningún modelo con variables (59 configuraciones + 4 LSTM) supera al AR(4) ni al ECM v1 en la validación por bloques de entrenamiento tras BH; el ECM v1 es peor que el AR(4) en los tres objetivos. Importancias (SHAP, permutación, ALE) solo EXPLORATORIO.
- H7: potencia baja (8 orígenes; objetivo nacional con n=8); el modelo elegido para compra provincial ya era peor que el AR(4) en entrenamiento; el contraste principal usa las 52 provincias, no solo las selladas; un aborto con <8 periodos consumiría el acceso.
- El código del BVAR no sigue exactamente lo declarado (verosimilitud marginal) sin efecto en la elección; algunas constantes fijas no declaradas.
- Bloque 5 (factor dinámico, spillovers espaciales) no ejecutado: sin coordenadas en los paneles. Deep learning solo probado en el panel de alquiler (LSTM; resultado negativo frente a LightGBM).
- El umbral de continuidad (0,05) se fijó después del acceso de comprobación declarado por el orquestador (docs/v2/decisiones.md).

*BP (política)* — declaración ex ante antes de abrir H6:

* Riesgos: (a) anticipación (Resolución TER/2940/2023, agosto de 2023; λ probablemente concentrado en 2023Q4: sesgo hacia 0); (b) paquete catalán coetáneo (DL 3/2023 de viviendas de uso turístico, 2.ª ronda de zonas desde 2024-10-10): H6 mide "Cataluña 2024-2026", no la zona tensionada aislada; (c) contratos del tope aún en el parque en el pre 2022Q2-2023Q4; (d) choques nacionales (tope del 3 % en 2024, IRAV desde 2025); (e) la inferencia placebo supone unidades intercambiables (probablemente conservadora, pues Barcelona reduce el ruido del agregado) y el jackknife es poco fiable con 4 tratadas; (f) los pesos de zona_tensionada_share pueden venir de un año de stock sellado (solo secundario). Secundario informativo añadido: SDiD sin 2023Q3-Q4 en el pre.

*Infraestructura y sellado* (`docs/v2/decisiones.md`):

- 2026-10-10 · holdout · Limitación conocida: los últimos 8 trimestres nacionales ya se usaron en v1 (informe v1). El sellado es estricto para v2, pero no «virgen» a nivel nacional; las hipótesis confirmatorias se evalúan preferentemente en las provincias selladas.
- El sellado es procedimental; hubo una lectura indebida menor del orquestador (sección 2).

*Fuente: `docs/v2/limitaciones.md`; `docs/limitaciones.md`; `output/v2/BP/resumen.md`; `docs/v2/decisiones.md`.*

## 11. Qué NO se puede afirmar

- **Causalidad de la inmigración** (BI): el placebo de alquiler pasado rechaza, las cuotas 2002 no están balanceadas (Sudamérica pesa en Rotemberg), con GPSS el F cae y el coeficiente deja de ser significativo; las pretendencias 2003-2007 no son pre-tratamiento (diagnóstico de Jaeger, Ruist y Stuhler 2018). H3: p_IUT 0,0294, Holm-7 0,176.
- **Causalidad del crédito** (BV): simultaneidad sin instrumento; con el crédito retardado 4 trimestres no es significativo.
- **Causalidad del tope catalán** (H5): fallan pretendencias y placebo; el signo es contrario al esperado.
- **Efecto de las zonas tensionadas como causal** (H6): τ = −0,0117 no supera Holm-7 (0,098); el DiD simple discrepa; mide «Cataluña 2024-2026» con un paquete regulatorio coetáneo, no la zona tensionada aislada; está por debajo del MDE declarado. EXPLORATORIO.
- **Que algún modelo prediga mejor que un AR(4)**, salvo el hecho sellado de H1 (y ni siquiera en las 3 provincias selladas solas: n = 24, p = 0,589). La observación del ECM v1 en la ventana nacional sellada no es evidencia.
- **Que H1 «se confirma»**: la conjunción de signos falla (población extranjera) y H1 no supera Holm-7; tampoco que el signo + de la población de 20-34 años sea una asociación robusta de ese coeficiente.
- **Magnitudes de elasticidades**: inmigración-alquiler (rango 0,8-5; IC95 [1,1; 5,0]), oferta-precio (0,79, inestable entre submuestras), crédito y coste de uso (simultaneidad y aproximación del coste), efecto de zonas tensionadas. No se comparan cuantitativamente con Saiz (2007) ni con el 0,45 del Banco de España.
- **Que H3 (alquiler > compra) ni H4 (suelo barato eleva la elasticidad) sean robustas**: nominalmente p < 0,05, pero no sobreviven a Holm-7 ni a las submuestras.
- **Que las familias medidas expliquen la subida del alquiler o del precio** desde 2014 o desde 2020: la mayor parte queda en el componente común; los contrafactuales de BD son aritmética de coeficientes de asociación, sin equilibrio general.
- **Importancias SHAP/ALE/permutación como explicación**, ni efectos de política con series nacionales que solo varían en el tiempo.
- **Cifras de déficit comparables con el BdE** (2021-2025 frente a 2021Q1-2024Q2 = 632.861 sin protegida; parte de la protegida es supuesto), ni déficit provincial (solo un proxy).
- **Nada sobre no residentes, inversores, licencias o titularidad** (sin datos), sobre viviendas turísticas como causa, ni sobre diferencias significativas de España frente a la UE (un único clúster).
- **Nada sobre 2024Q3-2026Q2 ni sobre Cádiz, Cuenca y Toledo** más allá de las cuatro evaluaciones selladas (H1, H2, H6, H7), y nada específico de la Comunitat Valenciana / València en v2.

*Fuente: `output/v2/BI/resumen.md`; `output/v2/BI/h3_principal.csv`; `output/v2/BP/h6_sellado.json`; `output/v2/BA/h1_sellado.json`; `output/v2/BO/resumen.md`; `output/v2/BD/resumen.md`; `output/v2/BS/holm7.csv`.*

## 12. Referencias (marca de verificación)

Estado según `docs/literatura.md` (DOI comprobado en Crossref; cuartil leído de resultados de búsqueda de Scimago o de agregadores, en la mayoría de la edición 2025, no del año de publicación: «año publ. no comprobado»). No se inventa ninguna referencia: las **NO VERIFICADAS** son 3 y las de **cuartil no verificado**, 2.

| Referencia | DOI | Revista | Cuartil | Estado |
|---|---|---|---|---|
| Harvey, Leybourne y Newbold (1997), 13(2), 281-291 | 10.1016/S0169-2070(96)00719-4 | Int. J. Forecasting | Q1 (SJR 2025; año publ. no comprobado) | VERIFICADA |
| Diebold y Mariano (1995), 13(3), 253-263 | 10.1080/07350015.1995.10524599 | J. Business & Economic Statistics | Q1 (agregador de Scimago; año publ. no comprobado) | VERIFICADA |
| Arkhangelsky et al. (2021), 111(12), 4088-4118 | 10.1257/aer.20190159 | AER | Q1 (1999-2025) | VERIFICADA |
| Abadie, Diamond y Hainmueller (2010), 105(490), 493-505 | 10.1198/jasa.2009.ap08746 | JASA | Q1 (1999-2022) | VERIFICADA |
| Goldsmith-Pinkham et al. (2020), 110(8) [v1] | 10.1257/aer.20181047 | AER | Q1 (1999-2025) | VERIFICADA |
| Borusyak, Hull y Jaravel (2022), 89(1) [v1] | 10.1093/restud/rdab030 | REStud | Q1 (1999-2025) | VERIFICADA |
| Adão, Kolesár y Morales (2019), 134(4), 1949-2010 | 10.1093/qje/qjz025 | Quarterly Journal of Economics | Q1 (agregador de Scimago; año publ. no comprobado) | VERIFICADA |
| Jaeger, Ruist y Stuhler (2018), NBER WP 24285 | 10.3386/w24285 | NBER Working Paper | sin cuartil (WP) | VERIFICADA (WP; revista NO VERIFICADA) |
| Roodman, Nielsen, MacKinnon y Webb (2019), 19(1), 4-60 | 10.1177/1536867X19830877 | The Stata Journal | cuartil no verificado | VERIFICADA |
| Webb (2023), 56(3), 839-858 | 10.1111/caje.12661 | Canadian Journal of Economics | Q2 (agregador de Scimago, datos hasta 2022-2023; año publ. no comprobado) | VERIFICADA |
| Montiel Olea y Pflueger (2013), 31(3), 358-369 | 10.1080/00401706.2013.806694 | J. Business & Economic Statistics | Q1 (agregador de Scimago; año publ. no comprobado) | VERIFICADA |
| Chernozhukov et al. (2018), 21(1), C1-C68 | 10.1111/ectj.12097 | Econometrics Journal | Q1 (2010-2025) | VERIFICADA |
| Athey, Tibshirani y Wager (2019), 47(2), 1148-1178 | 10.1214/18-aos1709 | Annals of Statistics | Q1 (1999-2025) | VERIFICADA |
| Giannone, Lenza y Primiceri (2015), 97(2), 436-451 | 10.1162/REST_a_00483 | Rev. Economics and Statistics | Q1 (1999-2025) | VERIFICADA |
| Primiceri (2005), 72(3), 821-852 | 10.1111/j.1467-937X.2005.00353.x | REStud | Q1 (1999-2025) | VERIFICADA |
| Del Negro y Primiceri (2015), 82(4), 1342-1345 | 10.1093/restud/rdv024 | REStud | Q1 (1999-2025) | VERIFICADA |
| Jordà (2005), 95(1), 161-182 | 10.1257/0002828053828518 | American Economic Review | Q1 (1999-2025, ver Diamond et al. 2019 en la tabla v2) | VERIFICADA |
| Belloni, Chernozhukov y Hansen (2014), 81(2), 608-650 | 10.1093/restud/rdt044 | Review of Economic Studies | Q1 (1999-2025, ver tabla v2) | VERIFICADA |
| Zou y Hastie (2005), 67(2), 301-320 | 10.1111/j.1467-9868.2005.00503.x | JRSS Series B | Q1 (agregador de Scimago; año publ. no comprobado) | VERIFICADA |
| Apley y Zhu (2020), 82(4), 1059-1086 | 10.1111/rssb.12377 | JRSS Series B | Q1 (agregador de Scimago; año publ. no comprobado) | VERIFICADA |
| Hochreiter y Schmidhuber (1997), 9(8), 1735-1780 | 10.1162/neco.1997.9.8.1735 | Neural Computation | Q1 (agregador de Scimago, categoría Cognitive Neuroscience; año publ. no comprobado) | VERIFICADA |
| Lundberg y Lee (2017), NeurIPS 30 (SHAP), «A Unified Approach to Interpreting Model Predictions» | sin DOI Crossref (la consulta bibliográfica no lo devolvió) | Advances in Neural Information Processing Systems 30 (actas) | sin cuartil de revista (actas) | NO VERIFICADA |
| Ke et al. (2017), NeurIPS 30 (LightGBM), «LightGBM: A Highly Efficient Gradient Boosting Decision Tree» | sin DOI Crossref localizado (consulta devolvió HTTP 429, no repetida) | Advances in Neural Information Processing Systems 30 (actas) | sin cuartil de revista (actas) | NO VERIFICADA |
| Poterba (1984), 99(4), 729-752 | 10.2307/1883123 | Quarterly Journal of Economics | Q1 (agregador de Scimago; año publ. no comprobado) | VERIFICADA |
| Khametshin, López Rodríguez y Pérez García (2024), BdE DO 2432 | 10.53479/37872 | BdE Documentos Ocasionales | sin cuartil | VERIFICADA |
| Saiz (2007), 61(2) [v1] | 10.1016/j.jue.2006.07.004 | J. Urban Economics | Q1 (SJR 2025; año publ. no comprobado) | VERIFICADA |
| Caldera y Johansson (2013), 22(3), 231-249 | 10.1016/j.jhe.2013.05.002 | J. Housing Economics | Q2 (SJR 2025; año publ. no comprobado) | VERIFICADA |
| Cavalleri, Cournède y Özsöğüt (2019), OECD ECO WP | 10.1787/4777e29a-en | OECD Economics Dept. WP | sin cuartil (WP) | VERIFICADA (parcial: DOI sí; autores y nº no confirmados) |
| Garcia-López et al. (2020), 119, 103278 | 10.1016/j.jue.2020.103278 | J. Urban Economics | Q1 (SJR 2025; año publ. no comprobado) | VERIFICADA |
| Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE 101, 103916 (citada por BP/resultado.json) | no consta en docs/literatura.md | Regional Science and Urban Economics | cuartil no verificado | NO VERIFICADA |
| Banco de España (2026), Informe Anual 2025 | 10.53479/43565 | Banco de España (informe institucional) | n/a (informe) | VERIFICADA |

NO VERIFICADAS: Lundberg y Lee (2017), NeurIPS 30 (SHAP), «A Unified Approach to Interpreting Model Predictions»; Ke et al. (2017), NeurIPS 30 (LightGBM), «LightGBM: A Highly Efficient Gradient Boosting Decision Tree»; Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE 101, 103916 (citada por BP/resultado.json). Cuartil no verificado: Roodman, Nielsen, MacKinnon y Webb (2019), 19(1), 4-60; Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE 101, 103916 (citada por BP/resultado.json).

*Fuente: `output/v2/tablas/referencias_v2.csv`; `docs/literatura.md`.*

## Anexo. Especificaciones registradas y reproducibilidad

| Rama | Especificaciones |
|---|---|
| BA | 5 |
| BV | 5 |
| BI | 5 |
| BO | 5 |
| BP | 5 |
| BM | 4 |
| BD | 5 |

Total v2: 34 (excluye 1 filas de presupuesto declarado de configuraciones). Cada rama registra sus especificaciones en `output/v2/<rama>/registro.csv` (Registry de `econ_utils`); la concatenación con columna `rama` es `output/v2/tablas/registro_v2.csv`.

Reproducibilidad: `python3 src/v2/bs_run.py` (1 hilo, SEED = 20261010, sin red) regenera `output/v2/BS/*`, `output/v2/tablas/*.csv` y este informe; dos ejecuciones dan md5 idénticos. Todas las cifras se leen de los ficheros citados.

*Fuente: `output/v2/tablas/registro_v2.csv`.*
