<!-- Generado por `make v12` (src/v12/atlas_v12.py) desde docs/v12/plantillas/atlas_v12.md y output/v5/cifras_clave.csv. No editar a mano. -->

# Atlas V12: población, propiedad y oferta

Borja Romero, economista (firma individual, independiente). Análisis descriptivo y contable: ninguna cifra de este atlas es causal. Capas: C4 salvo indicación; cada cifra lleva periodo, fuente, fecha y capa.

**Abstract (English).** V12 describes, without models, where Spain's population growth comes from, who moves within metropolitan areas, how households form relative to new construction, who owns housing, and the housing conditions of households by origin. Recent growth comes from net international migration while natural change is negative; capital cities lose residents to their metropolitan rings; household growth exceeds new supply in most provinces; large owners and legal persons hold a small share of the stock nationally, with higher shares in tourist and high-rent municipalities; at equal age and income, adults of foreign nationality face higher housing-cost overburden, associated with renting at market prices rather than with higher rent effort among tenants. All results are descriptive associations.

## 1. De dónde viene la población

| Periodo | Crecimiento | Saldo vegetativo | Saldo con el extranjero | Residuo |
|---|---|---|---|---|
| 2003-2007 | {{V12-B1-2003-2007-crecimiento:valor}} | {{V12-B1-2003-2007-vegetativo:valor}} | {{V12-B1-2003-2007-saldo_exterior:valor}} | {{V12-B1-2003-2007-residuo:valor}} |
| 2008-2013 | {{V12-B1-2008-2013-crecimiento:valor}} | {{V12-B1-2008-2013-vegetativo:valor}} | {{V12-B1-2008-2013-saldo_exterior:valor}} | {{V12-B1-2008-2013-residuo:valor}} |
| 2014-2019 | {{V12-B1-2014-2019-crecimiento:valor}} | {{V12-B1-2014-2019-vegetativo:valor}} | {{V12-B1-2014-2019-saldo_exterior:valor}} | {{V12-B1-2014-2019-residuo:valor}} |
| 2020-2021 | {{V12-B1-2020-2021-crecimiento:valor}} | {{V12-B1-2020-2021-vegetativo:valor}} | {{V12-B1-2020-2021-saldo_exterior:valor}} | {{V12-B1-2020-2021-residuo:valor}} |
| 2022-2024 | {{V12-B1-2022-2024-crecimiento:valor}} | {{V12-B1-2022-2024-vegetativo:valor}} | {{V12-B1-2022-2024-saldo_exterior:valor}} | {{V12-B1-2022-2024-residuo:valor}} |

Personas; España; {{V12-B1-2022-2024-crecimiento:fuentes}}; capa {{V12-B1-2022-2024-crecimiento:capa}}. El residuo es grande con la EVR (hasta 2020) y casi nulo con la EMCR: recoge revisiones del padrón y bajas no registradas como flujo. El saldo interior suma cero en España. Por provincia, CCAA y municipio: `output/v12/b1`. <!-- check:cifra-libre (años de los periodos) -->

València, 2021-2025 (censo anual por sección): población {{V12-B1-VLC-var_total}}; nacionalidad española {{V12-B1-VLC-var_espanola}}; extranjera {{V12-B1-VLC-var_extranjera}}. La población española también cambia por adquisiciones de nacionalidad. Barrios y distritos: `output/v12/b1/valencia_*`. <!-- check:cifra-libre (años del periodo) -->

## 2. A dónde va y quién se desplaza

Saldo de cada capital con su corona metropolitana en 2022-2024 (negativo: salen más de la capital a la corona que al revés): València {{V12-B2-valencia-saldo-corona}}, Madrid {{V12-B2-madrid-saldo-corona}}, Barcelona {{V12-B2-barcelona-saldo-corona}}, Alicante {{V12-B2-alicante-saldo-corona}}, Castelló {{V12-B2-castellon-saldo-corona}}. Corona de composición fija (cota inferior). En València, Madrid, Barcelona y Alicante, quienes salen de la capital van, en promedio, a municipios con alquiler más bajo (en Castelló, similar); la asociación entre saldos y precios entre municipios es descriptiva (`output/v12/b2`). <!-- check:cifra-libre (años del periodo) -->

## 3. Hogares y presión

Entre los censos de 2011 y 2021 los hogares aumentaron {{V12-B3-hogares-crec}}: población {{V12-B3-hogares-poblacion}}, estructura por edad {{V12-B3-hogares-estructura}} y tasa de jefatura {{V12-B3-hogares-jefatura}} (media y rango de los dos órdenes de la descomposición). La jefatura baja sobre todo entre los adultos jóvenes. <!-- check:cifra-libre (años de los censos) -->

Desde 2021, con la ECP: hogares {{V12-B3-reciente-crecimiento_observado}}; población {{V12-B3-reciente-componente_poblacion}}; estructura por edad {{V12-B3-reciente-componente_estructura_edad}}; cambio implícito de jefatura {{V12-B3-reciente-cambio_jefatura_implicito}}.

Hogares con persona de referencia de nacionalidad extranjera (Censo 2021, muestra): {{V12-B3-hogares-ext}}. <!-- check:cifra-libre (año del censo) -->

## 4. Dónde se construye

Del 1 de enero de 2021 al de 2025 (obra: años 2021-2024), en las 46 provincias con Catastro estatal y serie del MIVAU (sin País Vasco, Navarra, Ceuta ni Melilla): hogares nuevos {{V12-B4-hogares-nuevos}}; obra nueva neta {{V12-B4-obra-catastro}} (Catastro); terminadas {{V12-B4-terminadas-mivau}} (MIVAU, libres y protegidas). En 2013-2017, en esas mismas provincias, el Catastro supera al MIVAU en {{V12-B4-regularizacion}} por la regularización catastral: esos años no se leen como construcción. Ratio obra/hogares por municipio y mapa: `output/v12/b4`, figura F19. Es una relación contable, no una medida de necesidad. <!-- check:cifra-libre (años del periodo) -->

## 5. Quién es propietario

Viviendas de titulares con más de diez viviendas: {{V12-B5-pct_mas10}}; con más de cien: {{V12-B5-pct_mas100}}; personas jurídicas privadas: {{V12-B5-pct_PJ}}; entidades públicas: {{V12-B5-pct_PE}}; personas físicas: {{V12-B5-pct_PF}}. Los tramos se cuentan dentro de cada ámbito: la cuota municipal es una cota inferior. La cuota de personas jurídicas es mayor en municipios con alquiler y precio altos, más vivienda turística y mayor saldo exterior: asociación entre municipios, sin dirección causal. Verificador: V12-V02 (antes V02, «no analizada»). <!-- check:cifra-libre (identificadores de ficha) -->

## 6. Condiciones de vivienda por origen

A igual edad y renta (ECV), diferencia entre personas adultas de nacionalidad extranjera y española (en sus hogares): alquiler a precio de mercado {{V12-B6-brecha-tenencia_3}}; sobrecarga de más del 40 % {{V12-B6-brecha-sobrecarga_40}}; hacinamiento {{V12-B6-brecha-hacinamiento}}; inquilinos de mercado con alquiler de más del 30 % de la renta {{V12-B6-brecha-esfuerzo_alquiler_30}}. La diferencia en sobrecarga acompaña a la tenencia; no se atribuye a la nacionalidad. Por llegada, edad y tipo de hogar (Censo 2021): `output/v12/b6`. <!-- check:cifra-libre (umbrales de los indicadores y año del censo) -->

## 7. Turismo y presión residencial

Comunitat Valenciana: {{V12-B7-CV-vut-ine}} anunciadas (INE) y {{V12-B7-CV-vut-registro}} inscritas (registro GVA); València: {{V12-B7-VLC-vut-ine}} y {{V12-B7-VLC-vut-registro}}. Miden cosas distintas y se reportan ambas. Por municipio, distrito y barrio: `output/v12/b7`.

## Límites

Todo es descriptivo o contable (C4); en la tabla provincial de oferta, la obra nueva es C1 solo donde Catastro y MIVAU difieren menos de un 10 %. Celdas con menos de diez casos o error relativo superior al 30 % suprimidas. Decisiones: `docs/v12/decisiones.md`. <!-- check:cifra-libre (umbrales de supresión) -->
