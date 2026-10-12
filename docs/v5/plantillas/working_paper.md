# Necesidad de vivienda, territorio y precios en España: hechos, cotas y exploración con datos públicos y una escala de evidencia

*Borja Romero, economista (independiente). Documento de trabajo, versión de referencia `7.1`, 12 de octubre de 2026. DOI: pendiente.*

*Proyecto reproducible: `make all` sin red; todas las cifras proceden de `output/v5/cifras_clave.csv`.*

## Resumen

Este trabajo mide la necesidad de vivienda en España y su distribución territorial con registros públicos y clasifica cada resultado en una escala de evidencia: hechos con dos fuentes independientes, cotas con supuestos explícitos y resultados exploratorios. Entre 2021 y 2024 los hogares crecieron más que las viviendas terminadas, en el rango {{L3-DEF-2124-SINBAJAS:rango}} (sin las dos correcciones que conservan el salto de la EPA, {{L3-DEF-2124-SENS:rango}}) según la corrección del salto de la EPA [C2]. El precio de compra subió {{A23-P2:valor}} en 2015-2025 según tres registros, frente a {{A23-P1:valor}} del índice oficial; un puente contable reconcilia ambas medidas salvo un residuo de método. Una contabilidad stock-flujo provincial da una necesidad base de {{T3-H5b:valor}} al año en 2026-2035 ({{T3-H5b:rango}}), entre {{T3-H9:min}} y {{T3-H9:max}} la producción actual [C4]; el supuesto que más pesa es la fracción de vacías movilizables. Las viviendas liberadas por el envejecimiento no se restan, porque la proyección de hogares del INE ya descuenta las disoluciones. De 2025 a 2030 el déficit empeora en todos los escenarios considerados [C2], aunque la magnitud es exploratoria [C4]; a 2035 la dirección es indeterminada. El déficit se concentra en pocas provincias, y una clasificación con un coste de construcción oficial separa dónde falta vivienda y es rentable construir de dónde la oferta no responde. Un análisis pre-registrado de las diferencias provinciales de precios resulta descriptivo por falta de potencia, y las contribuciones contables de los factores a la subida no son estables entre métodos ni periodos. Ningún resultado nuevo alcanza la capa de efectos identificados. La versión de referencia v7.1 añade un atlas regional [C4]: los precios de las comunidades se mueven sobre todo con su media común (R² mediano de {{V71-S3-comun-r2-compra:valor}} en compra), no se confirma ninguna relación regional de largo plazo y, en una simulación de traslado con dosis y coste declarados, las ayudas a la demanda reducen el precio neto del beneficiario pero suben el precio de mercado.

## Abstract

This paper measures housing need in Spain and its territorial distribution using public records, and classifies every result on an evidence scale: facts confirmed by two independent sources, bounds under explicit assumptions, and exploratory results. Between 2021 and 2024 households grew by between {{L3-DEF-2124-SINBAJAS:min}} and {{L3-DEF-2124-SINBAJAS:max}} more than completed dwellings, depending on how the 2021 Labour Force Survey break is corrected [C2]. Purchase prices rose by {{A23-P2:valor}} over 2015-2025 according to three administrative registers, against {{A23-P1:valor}} in the official index; an accounting bridge reconciles both measures up to a methodological residual. A provincial stock-flow accounting yields a baseline need of {{T3-H5b:valor}} per year in 2026-2035 ({{T3-H5b:rango}}), between {{T3-H9:min}} and {{T3-H9:max}} current output [C4]; the assumption that weighs most is the share of vacant dwellings that can be mobilised. Dwellings released by population ageing are not subtracted, because the INE household projection already nets out household dissolutions. Between 2025 and 2030 the shortfall widens in every scenario considered [C2], although its size is exploratory [C4]; by 2035 the direction is undetermined. The shortfall is concentrated in a few provinces, and a classification based on an official construction cost separates places where housing is lacking and building is profitable from places where supply does not respond. A pre-registered analysis of provincial price differences turns out to be descriptive for lack of power, and the accounting contributions of the factors behind the price increase are not stable across methods or periods. No new result reaches the layer of identified effects. Reference version v7.1 adds a regional atlas [C4]: regional prices move mostly with their common mean (median R² of {{V71-S3-comun-r2-compra:valor}} for purchase prices), no regional long-run relationship is confirmed, and in a pass-through simulation with stated dose and cost, demand subsidies lower the beneficiary's net price but raise the market price.

**Palabras clave:** vivienda; déficit de vivienda; necesidad de vivienda; precios de la vivienda; alquiler; identificación parcial; pre-registro; España.

**Keywords:** housing; housing shortage; housing need; house prices; rents; partial identification; pre-registration; Spain.

**JEL:** R21, R31, R38, C21, C81.

---

*Note on figures:* numbers are rendered from the Spanish key-figures file, so they use the Spanish decimal comma and Spanish units (viviendas = dwellings; viviendas/año = dwellings per year; veces = times).

---

## 1. Introducción

**Pregunta.** ¿Qué se puede afirmar, y con qué grado de seguridad, sobre cuántas viviendas faltan en España, dónde faltan, cuánto han subido los precios y alquileres, qué factores se asocian con la subida y qué instrumentos tienen evidencia a favor en cada territorio?

**Motivación.** El debate público sobre la vivienda en España mezcla cifras de déficit que difieren por definición, índices de precios que miden cosas distintas y afirmaciones causales sin diseño que las sostenga. Una misma pregunta («¿cuánto ha subido la vivienda?») tiene respuestas que van de la mitad a cuatro quintas partes según el índice, y una misma cifra de déficit cambia según la ventana y la fuente de hogares. Este trabajo no añade una estimación más: ordena lo que los datos públicos permiten afirmar y con qué capa de evidencia.

**Contribución.**
1. **Una escala de evidencia aplicada de forma uniforme.** Cuatro capas: C1 hechos (al menos dos fuentes independientes, con todos los componentes en C1), C2 cotas de identificación parcial con supuestos explícitos (Manski, 2003), C3 efectos (pretendencias, placebos, sensibilidad y muestra sellada) y C4 exploratorio. La capa de una cifra es la menor de sus componentes. En esta versión ningún resultado nuevo alcanza C3.
2. **Una contabilidad de necesidad a diez años por provincia y una proyección del déficit a 2030**, con rango por componente y capa por componente, que hace explícito de qué supuesto depende cada cifra.
3. **Un puente contable entre el índice de precios oficial y el núcleo de tres registros**, y la separación del alquiler de stock y de contratos nuevos con dos fuentes por territorio.
4. **Una clasificación territorial con un coste de construcción oficial**, que sustituye al coste supuesto de versiones anteriores, y un análisis pre-registrado de las diferencias provinciales cuya potencia se declara antes de estimar.
5. **Una matriz de instrumentos con rúbrica común y una comparación sistemática con las cifras de los organismos públicos.**

**Frente a la literatura.**
- La literatura sobre la respuesta de la oferta y la regulación del suelo (Saiz, 2010; Glaeser y Gyourko, 2018; Hilber y Vermeulen, 2016) relaciona la elasticidad de la oferta con la transmisión de la demanda al precio. Este trabajo usa esa intuición para clasificar provincias, pero no estima elasticidades causales: la clasificación es exploratoria.
- Sobre la regulación del alquiler, Diamond, McQuade y Qian (2019) documentan una reducción de la oferta de alquiler en San Francisco, y Jofre-Monseny, Martínez-Mazza y Segú (2023) una reducción de rentas en Cataluña. Con los datos abiertos del proyecto no se replica García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020) sobre viviendas turísticas, y se documenta por qué (stock frente a flujo).
- Sobre la incidencia de las ayudas a la demanda, Gibbons y Manning (2006), Eriksen y Ross (2015), Hilber y Turner (2014) y Carozzi, Hilber y Yu (2024) muestran que el traslado al precio depende de la rigidez de la oferta. La matriz de instrumentos traduce esa condición a las clases territoriales.
- Sobre edificabilidad y licencias, Büchler y Lutz (2024) y Greenaway-McGrevy y Phillips (2023) evalúan cambios de zonificación con diseños de diferencias; Ball (2011) documenta retrasos de tramitación. No hay evaluación comparable en España.
- Metodológicamente, el trabajo combina identificación parcial (Manski, 2003), sensibilidad a variables omitidas (Oster, 2019; Cinelli y Hazlett, 2020), pretendencias robustas (Rambachan y Roth, 2023) y pre-registro con corrección por comparaciones múltiples.

**Estructura.** La sección de datos describe las fuentes y la regla de dos fuentes. La de métodos presenta las capas y los procedimientos de cada una. Los resultados se ordenan en necesidad, territorio, precios y contribuciones. Siguen la robustez, la discusión y las conclusiones.

---

## 2. Datos

**Fuentes.** Todas son públicas y se descargan con scripts separados de la reconstrucción (`make all` funciona sin red):
- **Hogares:** INE, Encuesta Continua de Población (ECP) y EPA (con la ruptura metodológica de 2021 tratada según la ventana: ver anexo metodológico); proyecciones de hogares del INE para 2026-2035.
- **Producción de vivienda:** Ministerio de Vivienda (certificados de fin de obra, iniciadas, calificaciones de vivienda protegida) y Catastro (altas de inmuebles).
- **Precio de compra:** INE (IPV), Ministerio (valor tasado), Notariado (Consejo General) y Registradores (datos abiertos).
- **Alquiler:** INE (IPC de alquiler e IPVA de la AEAT), SERPAVI del Ministerio, Incasòl (Cataluña) y registro de fianzas de la GVA (Comunitat Valenciana).
- **Coste de construcción:** módulo básico de construcción (BOE) actualizado con el índice de costes de Eurostat.
- **Parque y propiedad:** Censo 2021, ECV, EFF del Banco de España y estadísticas del IRPF de la AEAT.
- **Europa:** Eurostat (índice de precios, IPCA, SILC, permisos, demografía).
- **Organismos (para la convergencia):** Banco de España, Ministerio, INE, OCDE y Eurostat.

**Regla de dos fuentes.** Una cifra es C1 si dos fuentes independientes coinciden dentro de una tolerancia declarada. Eurostat toma el dato de España del INE y la ECV es la fuente de Eurostat-SILC: en esos casos no hay independencia y la cifra queda en C4.

**Unidad territorial.** {{E-E1-nprov:valor}} (cincuenta provincias y dos ciudades autónomas) en la contabilidad de necesidad; {{E-E1-B3-N:valor}} en el análisis transversal de precios (sin Ceuta ni Melilla). La suma provincial coincide con el total nacional en todas las tablas (comprobación automática).

**Muestra sellada.** Una parte de las series de v2 y v3 está sellada para evaluación confirmatoria y solo se accede a ella mediante un registro de accesos (`src/holdout.py`); cada hipótesis confirmatoria se evalúa una vez.

---

## 3. Métodos por capas

### 3.1 C1: hechos

Para cada cifra C1 se calculan los dos valores y se publica el rango. El déficit 2021-2024 es el aumento de hogares (ECP y EPA corregida) menos las terminadas (Ministerio y Catastro). El núcleo de precio es la banda entre Ministerio, Notariado y Registradores con pesos comunes. El alquiler de stock es la banda entre el IPC y el IPVA de contratos existentes.

### 3.2 C2: cotas

Se usan cotas de identificación parcial cuando un supuesto no se puede contrastar: bajas del parque en un rango, demanda latente frente a una tasa de convivencia de referencia, crecimiento de hogares del INE como escenario, desplazamiento máximo del stock de alquiler por viviendas turísticas. La cota se escribe con su supuesto.

### 3.3 C4: contabilidades, proyecciones y asociaciones

- **Necesidad (B1).** `N = A + R + V + F − M − K` por provincia: atraso, reposición, vacancia friccional, crecimiento de hogares, vacías movilizables y cartera en construcción. Cada componente tiene un rango; el total toma la menor capa.
- **Proyección (B2).** `D2030 = D2025 + F − T + B`, con tres escenarios de terminadas. El signo provincial se asigna solo si todo el rango coincide.
- **Clasificación (A4).** Falta o no falta (déficit 2021-2025) y rentabilidad con el coste oficial; estabilidad en una rejilla de costes, márgenes, tipos y holguras.
- **Diferencias provinciales (B3).** Mínimos cuadrados con las ocho familias de factores a la vez, errores `HC3` y Conley, inferencia por aleatorización de Freedman-Lane y Holm sobre las familias. Pre-registro con análisis de potencia previo.
- **Contribuciones (B4).** Triangulación de salidas de v2 (series temporales nacionales), B3 (reparto de Shapley entre provincias) y v3 (cotas). Estabilidad con la tau de Kendall.
- **Puente de precios (A23).** Variación acumulada en logaritmos con pesos comunes, sensibilidad a pesos y desfases, factor común de las fuentes.

### 3.4 Control de falsos descubrimientos y validación

Toda especificación probada se registra (`registro.csv` de cada módulo). Las familias de contrastes se corrigen con Holm (confirmatorias) o Benjamini-Hochberg (exploratorias). Los modelos de series se comparan en la misma muestra con un AR(4) y con el ECM de v1, con validación temporal en bloques con embargo; en el corte transversal se usa validación dejando una provincia fuera frente al modelo de solo media.

---

## 4. Resultados

### 4.1 Necesidad

**Déficit pasado.** El déficit 2021-2024 está en el rango {{L3-DEF-2124-SINBAJAS:rango}} [C2: cota según la corrección del salto de la EPA en 2021]; con las bajas del parque estimadas, {{L3-DEF-2124-BAJAST1}} [C4]; con bajas supuestas, sin respaldo observado, el máximo llegaría a {{L3-DEF-2124-CONBAJAS:max}} [C2]. El de 2021-2025, con bajas nulas, es {{B2-H2:valor}} [C4]. Los hogares crecieron {{dh_2125:valor}} en 2021-2025 [C1] y se terminaron {{terminadas_1924:rango}} en 2019-2024 [C1]. La demanda latente por convivencia con los padres está entre {{latente_convivencia:rango}} [C2].

**Bajas del parque (`T1`) [C4].** Las identidades de stock no miden bajas: Censos 2011-2021 y Catastro dan tasas negativas ({{T1-H2:valor}} y {{T1-H4:valor}}), que reflejan altas no certificadas o afloramientos. Las demoliciones con licencia son {{E-T7-demol-2024:rango}} en 2024 y no cubren ruina, cambios de uso ni agregaciones. La tasa usada es C4 (mínimo, central y máximo de las demoliciones con licencia: {{T1-H8:min}}, {{T1-H8:valor}} y {{T1-H8:max}}), salvo la cota física cero, que es C2. Sustituye al supuesto de bajas de v4, que queda por encima de todo lo observado.

**Necesidad (`v5.1`) [C4].** Con la reposición basada en las bajas estimadas (`T1`) en lugar del supuesto de v4, la necesidad base (A + R + V + F − M − K) es de {{T3-H5b}} de media anual en 2026-2035 [C4]. Si una parte de las viviendas liberadas no llega al mercado y queda vacía o como secundaria (componente X, que suma), la necesidad efectiva sube a {{T3-H5}} [C4]. X es un flujo bruto hacia la vacancia y sesga al alza; por eso la cifra de referencia es la base. Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares. Frente a la producción con la misma cobertura (terminadas en España con País Vasco y Navarra, {{E-T7-prod:rango}} en {{E-T7-prod:periodo}}), la necesidad con X equivale a {{T3-H9:min}}, {{T3-H9:valor}} y {{T3-H9:max}} la producción media (mínimo, central y máximo) [C4].

**Descomposición del rango [C4].** La amplitud de la necesidad anual (máximo menos mínimo) es de {{T3-H8:valor}}. Se reparte así entre los supuestos: vacías movilizables {{E-T7-peso-M}}, flujo futuro de hogares {{E-T7-peso-F}}, atraso {{E-T7-peso-A}}, liberadas que no llegan al mercado {{E-T7-peso-X}}, reposición {{E-T7-peso-R}}, vacancia friccional {{E-T7-peso-V}} y cartera {{E-T7-peso-K}}. El supuesto que más pesa es la fracción de vacías movilizables.

**Viviendas liberadas por envejecimiento (`T2`) [C4].** En 2026-2035 se liberarían {{T2-H1}} por fallecimiento del último miembro del hogar o por traslado a una residencia; llegan al mercado (venta o alquiler) {{T2-H6:num}} viviendas al año. Por tipo de municipio (central): {{E-T7-lib-capital}} en las capitales de provincia, {{E-T7-lib-entorno}} en el entorno de las grandes ciudades y {{E-T7-lib-resto}} en el resto de municipios. Hay desajuste territorial: {{T2-H12:valor}} de las liberadas está en municipios sin clase A4 (sin precio de referencia); entre los clasificados, {{T2-H11:valor}} cae en municipios de clase `1` o `2`. Los parámetros de traslado a residencias no tienen dato verificado. Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares.

**Componentes de B1 (`v5`).** Componentes a diez años del cálculo de `v5`, con la reposición anterior a `T1`:

| Componente | Central (rango) | Capa |
|---|---|---|
| Atraso | {{B1-H2}} | C4 |
| Reposición | {{B1-H3}} | C4 |
| Vacancia friccional | {{B1-H5}} | C4 |
| Hogares (INE) | {{B1-H4}} | C2 |
| Vacías movilizables (resta) | {{B1-H6}} | C4 |
| Cartera en construcción (resta) | {{B1-H7}} | C4 |

**Déficit a 2030.** **Proyección 2026-2030 (`T4`).** En una rejilla de escenarios que incluye los de B2, uno de construcción optimista ({{T4-H7:num}} terminadas al año, por encima de cualquier año nacional desde 2008), bajas nulas, hogares bajos y las liberadas, el déficit nacional empeora de 2025 a 2030 en todos los escenarios: la dirección es [C2]. La magnitud es [C4]: el aumento está en el intervalo {{T4-H2:rango}} y el déficit a fin de 2030 queda en {{T4-H1}}. Por provincias, {{T4-H3:valor}} empeoran, {{T4-H3:min}} mejoran y {{T4-H3:max}} quedan indeterminadas (en `v5`: {{T4-H4:valor}}, {{T4-H4:min}} y {{T4-H4:max}}). A 2035 la dirección nacional es indeterminada [C4], con un déficit a fin de 2035 entre {{T4-H5:min}} y {{T4-H5:max}}: el envejecimiento libera {{T4-H8:min}} en 2026-2030 y {{T4-H8:valor}} en 2031-2035, de modo que pesa más después de 2030. Mantener constante el déficit en 2026-2030 exigiría {{T4-H6:num}} terminadas al año [C4].

![Necesidad anual por provincia](B1/figuras/B1_mapa_necesidad.png)

### 4.2 Territorio

**Concentración.** {{A4-conc50-2021-2025:valor}} suman la mitad del déficit positivo de 2021-2025 y {{A4-conc80-2021-2025:valor}} cuatro quintas partes [C4].

**Clases.** Con el coste oficial ({{A4-001}}), en 2021-2025 hay {{A4-prov-2021-2025-c1:valor}} en la clase `1` (falta y es rentable), {{A4-prov-2021-2025-c2:valor}} en la clase `2` (falta y la oferta no responde pese a que el precio supera coste y suelo), {{A4-prov-2021-2025-c3:valor}} en la clase `3` (falta y no es rentable) y {{A4-prov-2021-2025-c4:valor}} en la clase `4` (no falta) [C4]. En 2012-2025 la clase `4` reúne {{A4-prov-2012-2025-c4:valor}} [C4]. Todas las clases son C4.

**Diferencias provinciales (B3).** El modelo de ocho familias alcanza un R² de {{B3-R2:valor}} [C4]. La única asociación que sobrevive a Holm es la del precio inicial (`H-B3-6`): {{B3-H-B3-6-b}}, p ajustado {{B3-H-B3-6-p:valor}}; con el precio inicial de otra fuente, {{B3-H-B3-6-b-control:valor}} y p {{B3-H-B3-6-p-control:valor}} [C4]. La demanda sectorial (`H-B3-1`, {{B3-H-B3-1-b:valor}}, p ajustado {{B3-H-B3-1-p:valor}}) y el crecimiento de la población (`H-B3-2`, {{B3-H-B3-2-b:valor}}, p ajustado {{B3-H-B3-2-p:valor}}) no se distinguen de cero [C4].

![Variación del precio por provincia](B3/figuras/mapa_P1.png)

### 4.3 Precios

**Compra.** Núcleo de tres registros: {{A23-P2}} en 2015-2025 [C1]. IPV del INE: {{A23-P1:valor}} [C4]. Las cuatro fuentes comparten un factor común que recoge {{A23-P10:valor}} de la varianza de las variaciones anuales [C4]. La reponderación geográfica no reduce la diferencia: con pesos provinciales, Registradores sube {{A23-P8:valor}} [C4]. Queda un residuo no identificado de {{A23-P3:valor}} [C4].

**Alquiler.** Stock de contratos: {{A23-A2:rango}} en 2015-2024 [C1]. Contratos nuevos con dos fuentes: Cataluña {{A23-A9}} y Comunitat Valenciana {{A23-A10}} en 2021-2024 [C1]. En 2024 los contratos nuevos están {{A23-A6:valor}} por encima de los existentes [C4].

**Europa.** El precio real de la vivienda en España creció {{CA-EU-hpi_real-crecimiento:valor}} y el alquiler real del IPCA {{CA-EU-alq_real-crecimiento:valor}} [C4]; la tasa de sobrecarga de coste varió {{CA-EU-sobrecarga-cambio_desde_2015:num}} puntos desde 2015 [C4].

![Puente de precio](A23/fig1_puente_precio.png)

### 4.4 Contribuciones

Las contribuciones contables al precio de compra en 2015-2025 (v2) son: demografía {{B4-v2-compra-2015-2025-demografica:valor}}, renta y empleo {{B4-v2-compra-2015-2025-renta_empleo:valor}}, financiación {{B4-v2-compra-2015-2025-financiacion_tipos:valor}}, oferta {{B4-v2-compra-2015-2025-oferta_suelo:valor}} y residuo {{B4-v2-compra-2015-2025-residuo:valor}} [C4]. Entre provincias (B3), el reparto del R² da oferta y suelo {{B4-b3-shapley-oferta_suelo:valor}}, demografía {{B4-b3-shapley-demografica:valor}}, turismo y no residentes {{B4-b3-shapley-turismo_no_residentes:valor}}, financiación {{B4-b3-shapley-financiacion_tipos:valor}} y renta {{B4-b3-shapley-renta_empleo:valor}} [C4]. La tau de Kendall mínima del orden de las familias es {{B4-estabilidad-tau-min:valor}} [C4]: las contribuciones no son estables. Las viviendas turísticas desplazaron como máximo {{B4-v3-vut-cantidad:valor}} [C2].

### 4.5 Alquiler y compraventa: qué se asocia y qué predice (v6)

Medidas: alquiler de stock (SERPAVI, €/m²/mes) por provincia, municipio y distrito; los contratos nuevos van aparte y solo de forma descriptiva, por falta de cobertura provincial. Compraventa: precio medido con el valor tasado del MIVAU (Registradores como robustez) y volumen con la ETDP del INE. En la validación sellada espacial ({{E-V6-NPROV-SELL:num}} provincias nunca usadas como validación), los árboles predicen mejor que la persistencia el alquiler provincial ({{V6-M4-RMSE-alq_provincia:num}} % de error frente a {{V6-M4-PERS-alq_provincia:num}} %), municipal y por distrito, y el precio provincial ({{V6-M4-RMSE-PROV_PRECIO_ANUAL:num}} % frente a {{V6-M4-PERS-PROV_PRECIO_ANUAL:num}} %); en el precio municipal y con Registradores el mejor es el ECM v1 heredado [C4]. Frente a la línea base más exigente (AR con factor común, crecimiento nacional o efectos fijos), la ventaja se mantiene en el alquiler de stock y en el precio trimestral, es frágil en el precio provincial anual y desaparece en el precio municipal, con Registradores y en el volumen anual [C4]. Ninguna variable es «relevante con seguridad» ({{V6-M4-N-REL:num}}). La población se asocia con los dos mercados (aparece en más modelos; PIP {{m2_pip_alq_ln_pob:num}} en alquiler y {{m2_pip_cp_ln_pob:num}} en compra) y el PIB por habitante en la compra y no en el alquiler ({{m2_pip_cp_ln_pib_pc:num}} frente a {{m2_pip_alq_ln_pib_pc:num}}); en la población extranjera y en las viviendas iniciadas los métodos discrepan y se dan las dos lecturas; la asociación de las iniciadas con el alquiler no indica que construir suba el alquiler: retardos y adelantos de las iniciadas no se distinguen de cero respecto al crecimiento del alquiler (K3) [C4]. La elasticidad precio-alquiler va de {{m1b_elasticidad_anual_FE_unidad_tendencia:num}} a {{m1b_elasticidad_trimestral_DOLS_FE_unidad_tendencia:num}} según la especificación (asociación); la ratio precio/alquiler mediana baja de {{m1b_ratio_precio_alquiler_mediana_2015:num}} a {{m1b_ratio_precio_alquiler_mediana:num}} años ({{m1b_ratio_precio_alquiler_mediana_2015:periodo}}-{{m1b_ratio_precio_alquiler_mediana:periodo}}) y el GSADF no detecta exuberancia en ninguna de las {{E-V6-M1B-GSADF-TOT:num}} CCAA [C4]. Detalle en la sección sobre alquiler y compraventa del informe técnico. <!-- check:cifra-libre (etiqueta de módulo) -->

---

## 5. Robustez

### 5.1 Multiverso

- **B3.** {{E-E1-B3-nesp:valor}} por hipótesis confirmatoria. El signo de la principal se mantiene en {{B3-mv-H-B3-6:valor}} de las especificaciones para `H-B3-6`, en {{B3-mv-H-B3-2:valor}} para `H-B3-2` y en {{B3-mv-H-B3-1:valor}} para `H-B3-1` [C4]. La proporción de especificaciones con p nominal por debajo del umbral convencional es {{E-E1-B3-mvp-H-B3-6:valor}}, {{E-E1-B3-mvp-H-B3-2:valor}} y {{E-E1-B3-mvp-H-B3-1:valor}}, respectivamente.
- **Diseños de v2 (`R1B`).** En la forma reducida del alquiler sobre el instrumento (BI), la proporción de especificaciones con el mismo signo que la base es {{R1B-S-BI-mv:valor}} [C4]. En el diseño de control sintético (BP H5), {{R1B-S-BP-mv:valor}} [C4].
- **Efecto donut (`R1B`).** El cambio de pendiente del gradiente de crecimiento con la distancia al centro, antes y después de 2019, es {{R1B-D-serpavi_VC:valor}} en el alquiler y {{R1B-D-tasado:valor}} en el valor tasado; ninguna especificación es significativa tras Holm ({{R1B-D-serpavi_VC-holm:valor}} y {{R1B-D-tasado-holm:valor}}) [C4].

### 5.2 Oster y Cinelli-Hazlett

| Diseño | Oster δ | RV de Cinelli-Hazlett | Capa |
|---|---|---|---|
| B3, `H-B3-1` (Bartik) | {{E-E1-B3-oster-H-B3-1:num}} | {{E-E1-B3-RV-H-B3-1:num}} (RV con α: {{E-E1-B3-RV-H-B3-1:min}}) | C4 |
| B3, `H-B3-2` (población) | {{E-E1-B3-oster-H-B3-2:num}} | {{E-E1-B3-RV-H-B3-2:num}} (RV con α: {{E-E1-B3-RV-H-B3-2:min}}) | C4 |
| v2, BI (alquiler e instrumento) | {{R1B-S-BI-delta:num}} | {{R1B-S-BI-RV:num}} | C4 |
| v2, BP H6 (muestra sellada) | — | {{R1B-S-BP-H6-RV:num}} (aproximado) | C4 |

Un δ de Oster mayor que uno indica que las variables omitidas tendrían que estar más relacionadas con el resultado que las observadas para anular el coeficiente. En B3, el parámetro de Oster se acotó a uno porque la regla del pre-registro daba un valor mayor (desviación declarada). El RV con α, que exige que el intervalo deje de excluir el cero, es pequeño en las dos hipótesis de B3: una confusión modesta bastaría para que dejaran de ser significativas, en línea con su falta de significación tras Holm.

### 5.3 GSADF con tamaño corregido

La prueba GSADF de exuberancia con valores críticos para errores independientes tiene un tamaño empírico de {{R1B-G-tam:num}} (fracción de rechazos con un nivel nominal convencional) cuando la variación sigue un AR(1) [C4]; con valores críticos por bootstrap de un AR(p) estimado, el tamaño baja a {{R1B-G-tam-corr:num}} [C4]. Con los valores corregidos:

| Razón | Estadístico (valor crítico, p y p ajustado BH) | Capa |
|---|---|---|
| Precio/renta (IPV) | {{R1B-G-0:valor}} | C4 |
| Precio/alquiler (IPV) | {{R1B-G-1:valor}} | C4 |
| Precio frente al valor de descuento del alquiler (IPV) | {{R1B-G-2:valor}} | C4 |
| Precio frente a la cuota hipotecaria (IPV) | {{R1B-G-3:valor}} | C4 |
| Precio/renta (valor tasado) | {{R1B-G-5:valor}} | C4 |
| Precio/alquiler (valor tasado) | {{R1B-G-6:valor}} | C4 |
| Precio frente al valor de descuento del alquiler (valor tasado) | {{R1B-G-7:valor}} | C4 |
| Precio frente a la cuota hipotecaria (valor tasado) | {{R1B-G-8:valor}} | C4 |

Ninguna razón supera el ajuste por comparaciones múltiples en la familia nacional; por comunidades autónomas, {{R1B-G-ccaa:valor}} de las combinaciones muestran exuberancia tras BH [C4]. Las razones que comparan el precio con fundamentales (valor de descuento del alquiler, cuota hipotecaria) no muestran exuberancia. Una exuberancia estadística no es una burbuja.

### 5.4 Pre-registro `prereg-v5` y desviaciones

El pre-registro (`docs/v5/prereg_B3.md`, etiqueta git `prereg-v5`) fijó antes de estimar: hipótesis, variables, ventanas, familias, errores estándar, inferencia por aleatorización y corrección de Holm. El análisis de potencia dio un efecto mínimo detectable de {{E-B3-EMD}} [C4], y B3 se declaró descriptivo de antemano. Desviaciones, todas exploratorias (`output/v5/B3/desviaciones.md`):
1. Renta: PIB per cápita provincial en lugar de la renta por hogar, por la falta de serie provincial de 2015.
2. Ventanas más cortas en alquiler (SERPAVI) y en renta.
3. Crecimiento de la población con el padrón; los flujos migratorios terminan antes.
4. Hipotecas por habitante en lugar de por hogar.
5. La respuesta de la oferta se mide en la ventana del resultado: su asociación puede ser en parte mecánica.
6. Holm aplicado como dice el texto del pre-registro y, además, sobre las tres confirmatorias.
7. Validación dejando una provincia fuera en lugar de AR(4) y ECM, que no aplican a un corte transversal.
8. Control añadido del error de medida del precio inicial con otra fuente.
9. Parámetro de Oster acotado a uno.

### 5.5 Validación sellada v6 y resultados negativos

La validación v6 es **espacial nueva** y **temporal ya vista**: el último año cae en la ventana sellada de v2 (otras provincias) y todas las provincias se usaron de forma descriptiva en v4-v5. Cada modelo se evaluó una vez, sin reajuste, y en provincias nuevas el AR, el ECM y la econometría de M1 quedan reducidos a la persistencia. Resultados negativos [C4]: ninguna hipótesis confirmatoria pasa Holm ({{E-V6-M1A-HOLM:num}} de {{E-V6-M1A-NCONF:num}} en alquiler; {{E-V6-M1B-HOLM:num}} en compra); el deep learning no bate al gradient boosting (MLP {{E-V6-M3A-DL-mlp:num}} % frente a {{E-V6-M3A-GB-dis:num}} % en distritos, p {{E-V6-M3A-DLp-mlp:num}}); y la persistencia no se bate en el volumen trimestral (parte temporal sellada: {{E-V6-M4-TEMP-PROV_VOL_TRIM:num}} % del bosque frente a {{E-V6-M4-TEMPPERS-PROV_VOL_TRIM:num}} %). Las importancias y los SHAP son descriptivos: no dicen qué pasaría si una variable cambiara. La comparación posterior con líneas base más exigentes es una segunda mirada a la misma muestra sellada y no es confirmatoria. Con once provincias selladas y errores correlacionados en el espacio, los p del DM-HLN calculados por provincia sobrestiman la precisión. El criterio prudente es el DM por periodo, y con él la ventaja en el precio provincial anual no es significativa.

---

## 5 bis. Qué añade la versión de referencia v7.1 (atlas regional) [C4]

- **Domina el componente común.** La variación interanual del precio de cada comunidad acompaña en gran medida a la media de las 17: el R² mediano es {{V71-S3-comun-r2-compra:valor}} en compra y {{V71-S3-comun-r2-alquiler:valor}} en alquiler. Es una descripción, no un modelo.
- **No hay un largo plazo regional confirmado.** Se confirman {{V71-S3-largo-confirmadas:num}} de las siete hipótesis pre-registradas (empleo, población, hipotecas y paro). En compra no se descarta que la serie sea I(2) en {{V71-S3-i2-compra:num}} de 17 comunidades. En la simulación, con un componente común así, ningún estimador de panel es fiable (nota metodológica).
- **Traslado al precio de las ayudas a la demanda y de la rebaja de ITP/IVA** (escenario condicional). Reducen el precio neto que paga el beneficiario: su esfuerzo varía un {{V7-R6-e_ayuda_demanda-esfuerzo10a:valor}} con la ayuda. Pero el precio de mercado sube un {{V71-S3-R6-e_ayuda_demanda-compra-precio10a:valor}} con la ayuda y un {{V71-S3-R6-f1_rebaja_ITP_IVA_vivienda_nueva-compra-precio10a:valor}} con la rebaja, a diez años (mediana entre comunidades). *Nota:* el signo lo fija en gran parte la fórmula de incidencia; lo informativo son las magnitudes relativas.
- **Dosis y coste.**
  - Coste fiscal anual mediano por comunidad: ayudas a la demanda, {{V71-S1-e_ayuda_demanda-compra-coste_anual_meur:valor}}; rebaja de ITP/IVA, {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_anual_meur:valor}}; rebaja de impuestos y costes de construcción, {{V71-S1-f2_impuestos_construccion-compra-coste_anual_meur:valor}} (su efecto por euro está sobrestimado por construcción del escenario; no es «el más eficiente»).
  - Coste anual por punto de reducción del precio neto: {{V71-S1-e_ayuda_demanda-compra-coste_por_punto_meur:valor}} y {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_por_punto_meur:valor}}.
  - Construcción, vacías, vivienda pública y turísticos no tienen coste estimable, porque no hay coste unitario verificado. Se comparan por su efecto por cada diez mil viviendas: en alquiler, {{V71-S1-b_vacias-alquiler-efecto_10k:valor}} con vacías y {{V71-S1-c_vivienda_publica-alquiler-efecto_10k:valor}} con vivienda pública (mediana). <!-- check:cifra-libre (unidad de normalización «diez mil viviendas», no son cifras de resultado) -->
  - Robustez en la rejilla simulada (C4; no es robustez estadística): la movilización de vacías es robusta en {{V71-S3-R6-b_vacias-alquiler-robustas:num}} de 17 comunidades en alquiler; las ayudas a la demanda, en {{V71-S3-R6-e_ayuda_demanda-compra-robustas:num}}.
- Detalle por comunidad: atlas regional (atlas_regional/). Método: [nota metodológica](nota_metodologica.md). Afirmaciones evaluadas: verificador V7.

## 6. Discusión

**Necesidad.** La cifra de necesidad es grande y su rango es amplio. El rango no es un defecto: muestra que la necesidad depende sobre todo de dos supuestos (el crecimiento de hogares y la parte movilizable de las vacías). Una política que fije un objetivo de producción debería declarar qué supuesto adopta.

**Territorio.** El déficit está concentrado y la clasificación separa dos situaciones con implicaciones distintas: donde construir es rentable y la oferta responde, y donde el precio supera holgadamente coste y suelo pero la oferta no responde. En el segundo caso, la literatura verificada de otros países apunta al suelo y a la tramitación; en España no hay evaluación comparable. La clasificación es exploratoria y depende del coste oficial.

**Alcance de la aportación.** La aportación es de medición y de método. Reconcilia medidas de precio y contabilidades del déficit con una escala de evidencia explícita y valida predicciones en una muestra sellada. No aporta ninguna estimación identificada. Los estudios citados de otros países fijan los extremos de las rejillas, y sus resultados no se trasladan a España como evidencia propia.

**Precios.** La discrepancia entre índices no indica que ninguna de las dos fuentes esté mal medida: el índice oficial y los registros miden cosas distintas (método hedónico frente a medias, calidad, tamaño, cobertura). Citar una sola cifra sin su definición produce desacuerdos aparentes. El alquiler de stock y el de contratos nuevos también miden cosas distintas.

**Contribuciones.** La falta de estabilidad de las contribuciones es un resultado, no una carencia del análisis. Con las series y los cortes disponibles, la pregunta «qué factor explica la subida» no tiene una respuesta robusta. Un diseño de identificación requeriría variación exógena que los datos públicos no ofrecen en el periodo estudiado.

**Instrumentos.** La condición que más pesa en la evaluación de instrumentos es la respuesta de la oferta, que entra como parámetro supuesto y no como efecto estimado en España: la fracción de las ayudas a la demanda que se trasladaría al precio según la rejilla, por clase territorial (A4, método A, rejilla de elasticidades de demanda): clase `1`, falta y es rentable, {{D1-H11:rango}}; clase `2`, la oferta no responde, {{D1-H12:rango}}; clase `3`, no rentable, {{D1-H13:rango}} [C4]. El extremo bajo se apoya en la literatura con oferta elástica (Eriksen y Ross, 2015) y el alto en la de oferta rígida (Gibbons y Manning, 2006; Hilber y Turner, 2014). Con el método B, la clase `1` baja a {{E-E1-D1-incB-1:valor}}. Los instrumentos con signo estable en la rejilla de v3 son la construcción adicional donde falta y la movilización de vacías [C2 en el signo]. Las evaluaciones son condicionales y no sustituyen a evaluaciones con diseño de identificación en España.

**Convergencia.** Las cifras del proyecto coinciden con las de los organismos cuando concepto y periodo son comparables, y las diferencias se explican por definiciones. Las coincidencias con fuentes que comparten insumos primarios no elevan la capa.

---

### 6.1 Qué cambió entre versiones y por qué

Sección única del proyecto: [Qué cambió entre versiones y por qué](que_cambio.md) (versión de referencia v7.1).

## 7. Conclusiones

1. Entre 2021 y 2024 el aumento de hogares superó al de viviendas terminadas en una cantidad en el rango {{L3-DEF-2124-SINBAJAS:rango}} [C2]. Que el balance es positivo lo confirman dos fuentes de hogares y dos de terminadas; la cuantía es una cota porque depende de cómo se corrija el salto metodológico de la EPA en 2021 (siete alternativas más la constante de v1).
2. La necesidad 2026-2035 y el déficit a 2030 son contabilidades con supuestos [C4]; su rango es amplio y depende de hogares y vacías.
3. El déficit se concentra en pocas provincias, y la clase territorial condiciona qué instrumentos tienen signo estable [C4].
4. El precio de compra subió {{A23-P2:valor}} según los registros [C1] y {{A23-P1:valor}} según el índice oficial [C4]; las dos cifras deben darse juntas.
5. No se puede atribuir la subida a una familia de factores: las contribuciones contables no son estables.
6. El pre-registro declaró la falta de potencia antes de ver los resultados, y las conclusiones de ese análisis se limitan a lo descriptivo.

---

## Limitaciones (revisión por pares simulada v6.1) <!-- check:cifra-libre (etiqueta de versión pedida en el título) -->

Objeciones de la revisión por pares simulada (informes del árbitro académico y del revisor de política pública) que no se pueden resolver sin nuevas estimaciones. Cada punto indica el motivo y el coste.

- **Capa del déficit acumulado.** El extremo superior depende de una corrección constante de la EPA, y las terminadas son dos variantes del Ministerio. Para mantener la etiqueta [C1] con fuentes independientes en sentido fuerte habría que recalcular el rango con las altas del Catastro como segunda fuente de terminadas, o rebajar la capa en cifras_clave. Exige recalcular el módulo y regenerar las cifras.
- **Validación sellada.** La comparación con líneas base nuevas fue una segunda mirada a la muestra sellada, y la parte temporal ya se había visto. Una validación confirmatoria limpia exige una muestra nueva (el año siguiente), que todavía no existe.
- **Inferencia con once provincias selladas.** Dar como criterio principal el DM por periodo o agrupado por comunidad, y el efecto mínimo detectable, exige reejecutar las comparaciones.
- **Multiplicidad entre versiones.** La relación entre inmigración y precios se ha reestimado en varias versiones con correcciones dentro de cada módulo, no conjuntas. Un recuento conjunto con su p ajustado exige reconstruir los registros de todas las versiones. Hasta entonces, ningún p de una versión aislada debe leerse como confirmatorio.
- **Pocos conglomerados.** Generalizar el wild cluster bootstrap a todas las tablas con pocos grupos, y retirar los paneles municipales con regresor provincial, exige reestimar los módulos afectados.
- **Instrumento débil.** Los intervalos de Anderson-Rubin y la inferencia específica de diseños shift-share exigen reestimar. Las cifras de dos etapas quedan solo como historial.
- **Reproducibilidad del método de traslado y de la necesidad.** Varias cifras de modelo no se reconstruyen solo con el texto. Publicar las ecuaciones y parámetros de la rejilla exige extraerlos del código y verificarlos.
- **Utilidad para la decisión.** La tabla de instrumentos no da costes ni magnitudes por euro, y el reparto territorial usa una definición de necesidad distinta de la del titular. Las dos cosas exigen nuevos datos o recalcular el módulo de política por territorio.
- **Fecha de publicación** de las etiquetas del pre-registro: queda pendiente hasta su publicación en el repositorio remoto.

---

## Referencias

Solo se citan como base referencias verificadas por DOI en Crossref, con cuartil Scimago cuando consta; el resto se marca.

- Ball, M. (2011). Planning delay and the responsiveness of English housing supply. *Urban Studies*. DOI: https://doi.org/10.1177/0042098010363499. VERIFICADA, Q1 (solo asociación).
- Büchler, S. y Lutz, E. (2024). Making housing affordable? The local effects of relaxing land-use regulation. *Journal of Urban Economics*. DOI: https://doi.org/10.1016/j.jue.2024.103689. VERIFICADA, Q1.
- Carozzi, F., Hilber, C. A. L. y Yu, X. (2024). On the economic impacts of mortgage credit expansion policies: evidence from Help to Buy. *Journal of Urban Economics*. DOI: https://doi.org/10.1016/j.jue.2023.103611. VERIFICADA, Q1.
- Cinelli, C. y Hazlett, C. (2020). Making sense of sensitivity: extending omitted variable bias. *Journal of the Royal Statistical Society, Series B*. DOI: https://doi.org/10.1111/rssb.12348. VERIFICADA, Q1.
- Diamond, R., McQuade, T. y Qian, F. (2019). The effects of rent control expansion on tenants, landlords, and inequality: evidence from San Francisco. *American Economic Review*. DOI: https://doi.org/10.1257/aer.20181289. VERIFICADA, Q1.
- Eriksen, M. D. y Ross, A. (2015). Housing vouchers and the price of rental housing. *American Economic Journal: Economic Policy*. DOI: https://doi.org/10.1257/pol.20130064. VERIFICADA, Q1.
- García-López, M. À., Jofre-Monseny, J., Martínez-Mazza, R. y Segú, M. (2020). Do short-term rental platforms affect housing markets? Evidence from Airbnb in Barcelona. *Journal of Urban Economics*. DOI: https://doi.org/10.1016/j.jue.2020.103278. VERIFICADA, Q1.
- Gibbons, S. y Manning, A. (2006). The incidence of UK housing benefit: evidence from the 1990s reforms. *Journal of Public Economics*. DOI: https://doi.org/10.1016/j.jpubeco.2005.01.002. DOI verificado; cuartil no verificado. <!-- check:cifra-libre (título de la obra) -->
- Glaeser, E. y Gyourko, J. (2018). The economic implications of housing supply. *Journal of Economic Perspectives*. DOI: https://doi.org/10.1257/jep.32.1.3. DOI verificado; cuartil no verificado.
- Greenaway-McGrevy, R. y Phillips, P. C. B. (2023). The impact of upzoning on housing construction in Auckland. *Journal of Urban Economics*. DOI: https://doi.org/10.1016/j.jue.2023.103555. VERIFICADA, Q1.
- Hilber, C. A. L. y Turner, T. M. (2014). The mortgage interest deduction and its impact on homeownership decisions. *Review of Economics and Statistics*. DOI: https://doi.org/10.1162/rest_a_00427. VERIFICADA, Q1.
- Hilber, C. A. L. y Vermeulen, W. (2016). The impact of supply constraints on house prices in England. *Economic Journal*. DOI: https://doi.org/10.1111/ecoj.12213. VERIFICADA, Q1.
- Jofre-Monseny, J., Martínez-Mazza, R. y Segú, M. (2023). Effectiveness and supply effects of high-coverage rent control policies. *Regional Science and Urban Economics*. DOI: https://doi.org/10.1016/j.regsciurbeco.2023.103916. VERIFICADA, Q1.
- Manski, C. F. (2003). *Partial Identification of Probability Distributions*. Springer. DOI: https://doi.org/10.1007/b97478. VERIFICADA (libro).
- Oster, E. (2019). Unobservable selection and coefficient stability: theory and evidence. *Journal of Business & Economic Statistics*. DOI: https://doi.org/10.1080/07350015.2016.1227711. VERIFICADA, Q1.
- Phillips, P. C. B., Shi, S. y Yu, J. (2015). Testing for multiple bubbles. *International Economic Review*. NO VERIFICADA en este proyecto (DOI no comprobado).
- Rambachan, A. y Roth, J. (2023). A more credible approach to parallel trends. *Review of Economic Studies*. DOI: https://doi.org/10.1093/restud/rdad018. VERIFICADA, Q1.
- Saiz, A. (2010). The geographic determinants of housing supply. *Quarterly Journal of Economics*. DOI: https://doi.org/10.1162/qjec.2010.125.3.1253. DOI verificado; cuartil no verificado.

Lista completa y estado de verificación: `docs/literatura.md` y `docs/v5/literatura_instrumentos.md`.

---

## Apéndices

### Apéndice A. Datos

- Fuentes, licencias y fechas de descarga: `README_REPLICACION.md`, `docs/v5/licencias_datos.md` y el manifiesto de `data/raw`.
- Fuentes que no se pudieron obtener: `docs/v5/fuentes_fallidas.md`.
- Cada cifra del texto, con indicador, periodo, cobertura, fuentes, capa y fecha del dato: `output/v5/cifras_clave.md`.
- Tablas por módulo: `output/v5/<módulo>/tablas` y `resultado.json`.

### Apéndice B. Replicación

- **Anexo metodológico** ([output/v6_2/anexo_metodologico.md](../v6_2/anexo_metodologico.md)): una ficha por cifra publicable, con definición, fuente y fichero de data/raw, filtros, fórmula paso a paso, supuestos, capa y script. Permite reconstruir cada cifra sin leer el código; una segunda implementación independiente, escrita solo con el anexo, se comprueba en `make check` (tests/doble_impl). <!-- check:cifra-libre (ruta de versión) -->
- `make all` reconstruye todos los resultados sin red; `make check` ejecuta las comprobaciones de puerta (cifras fuera de marcador, sumas provinciales, capas, léxico y lenguaje causal).
- Semilla `SEED=20261010` en todo lo aleatorio.
- Registro de especificaciones: `output/v5/*/registro.csv`; muestra sellada solo vía `src/holdout.py`.
- Este documento se genera con `python3 src/v5/render.py` desde `docs/v5/plantillas/working_paper.md`.

### Apéndice C. Uso de IA y declaración de independencia

- **Uso de IA.** El proyecto se ha ejecutado con agentes de IA (Claude, de Anthropic) bajo la supervisión del autor: un orquestador y subagentes de datos, econometría, literatura, redacción y revisión independiente por oleadas. Todas las cifras proceden del código del repositorio y de fuentes públicas; ninguna se ha tecleado en el texto. Las referencias se verifican por DOI o se marcan como no verificadas.
- **Responsabilidad.** El autor es responsable del contenido, incluidos los errores.
- **Independencia.** El trabajo no ha recibido financiación y no tiene vínculo con ningún partido ni organización política. Si hubiera algo que declarar, el autor lo completará en esta sección antes de la publicación.

**Pre-registro y versiones.** Las etiquetas git `prereg-v5` (pre-registro de las diferencias entre provincias, `docs/v5/prereg_B3.md`) y `v5.0` se crearon en el repositorio local el 10 de octubre de 2026 y se publicaron en el repositorio remoto el [fecha de publicación: pendiente]. El commit del pre-registro es anterior a cualquier resultado de ese análisis, pero una etiqueta local no es un sello de tiempo externo. Por eso, en versiones futuras el pre-registro se depositará además con sello de tiempo externo (OSF o Zenodo) antes de estimar.
