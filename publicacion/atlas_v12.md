<!-- Generado por `make publicacion` desde output/v12/atlas_v12.md. No editar a mano: se regenera y un test lo comprueba. -->

<!-- Generado por `make v12` (src/v12/atlas_v12.py) desde docs/v12/plantillas/atlas_v12.md y output/v5/cifras_clave.csv. No editar a mano. -->

# Atlas V12: población, propiedad y oferta

Borja Romero, economista (firma individual, independiente). Análisis descriptivo y contable: ninguna cifra de este atlas es causal. Capas: C4 salvo indicación; cada cifra lleva periodo, fuente, fecha y capa.

**Abstract (English).** V12 describes, without models, where Spain's population growth comes from, who moves within metropolitan areas, how households form relative to new construction, who owns housing, and the housing conditions of households by origin. Recent growth comes from net international migration while natural change is negative; capital cities lose residents to their metropolitan rings; household growth exceeds new supply in most provinces; large owners and legal persons hold a small share of the stock nationally, with higher shares in tourist and high-rent municipalities; at equal age and income, adults of foreign nationality face higher housing-cost overburden, associated with renting at market prices rather than with higher rent effort among tenants. All results are descriptive associations.

## 1. De dónde viene la población

| Periodo | Crecimiento | Saldo vegetativo | Saldo con el extranjero | Residuo |
|---|---|---|---|---|
| 2003-2007 | 3.440.758 personas | 441.232 personas | 3.154.542 personas | -155.016 personas |
| 2008-2013 | 613.519 personas | 522.433 personas | 691.833 personas | -600.747 personas |
| 2014-2019 | 679.454 personas | -111.584 personas | 1.272.915 personas | -481.877 personas |
| 2020-2021 | 24.625 personas | -264.138 personas | 443.487 personas | -154.724 personas |
| 2022-2024 | 1.641.570 personas | -362.896 personas | 1.995.569 personas | 8.897 personas |

Personas; España; INE: padrón y censo anual, MNP, EVR (hasta 2020) y EMCR (desde 2021); cálculo V12-B1; capa C4. El residuo es grande con la EVR (hasta 2020) y casi nulo con la EMCR: recoge revisiones del padrón y bajas no registradas como flujo. El saldo interior suma cero en España. Por provincia, CCAA y municipio: `output/v12/b1`. <!-- check:cifra-libre (años de los periodos) -->

València, 2021-2025 (censo anual por sección): población 52.716 personas; nacionalidad española -5.670 personas; extranjera 58.386 personas. La población española también cambia por adquisiciones de nacionalidad. Barrios y distritos: `output/v12/b1/valencia_*`. <!-- check:cifra-libre (años del periodo) -->

## 2. A dónde va y quién se desplaza

Saldo de cada capital con su corona metropolitana en 2022-2024 (negativo: salen más de la capital a la corona que al revés): València -12.225 personas, Madrid -29.196 personas, Barcelona -22.541 personas, Alicante -3.590 personas, Castelló -650 personas. Corona de composición fija (cota inferior). En València, Madrid, Barcelona y Alicante, quienes salen de la capital van, en promedio, a municipios con alquiler más bajo (en Castelló, similar); la asociación entre saldos y precios entre municipios es descriptiva (`output/v12/b2`). <!-- check:cifra-libre (años del periodo) -->

## 3. Hogares y presión

Entre los censos de 2011 y 2021 los hogares aumentaron 455.531 hogares: población 196.494 hogares (195.104-197.884 hogares), estructura por edad 1.071.741 hogares (966.831-1.176.650 hogares) y tasa de jefatura -812.704 hogares (-919.003 a -706.404 hogares) (media y rango de los dos órdenes de la descomposición). La jefatura baja sobre todo entre los adultos jóvenes. <!-- check:cifra-libre (años de los censos) -->

Desde 2021, con la ECP: hogares 1.222.836 hogares; población 835.141 hogares; estructura por edad 375.142 hogares; cambio implícito de jefatura 12.553 hogares.

Hogares con persona de referencia de nacionalidad extranjera (Censo 2021, muestra): 9,7 % (9,7-9,8 %). <!-- check:cifra-libre (año del censo) -->

## 4. Dónde se construye

Del 1 de enero de 2021 al de 2025 (obra: años 2021-2024), en las 46 provincias con Catastro estatal y serie del MIVAU (sin País Vasco, Navarra, Ceuta ni Melilla): hogares nuevos 934.562 hogares; obra nueva neta 355.508 viviendas (Catastro); terminadas 346.403 viviendas (MIVAU, libres y protegidas). En 2013-2017, en esas mismas provincias, el Catastro supera al MIVAU en 348.840 viviendas por la regularización catastral: esos años no se leen como construcción. Ratio obra/hogares por municipio y mapa: `output/v12/b4`, figura F19. Es una relación contable, no una medida de necesidad. <!-- check:cifra-libre (años del periodo) -->

## 5. Quién es propietario

Viviendas de titulares con más de diez viviendas: 4,2 %; con más de cien: 2,1 %; personas jurídicas privadas: 4,6 %; entidades públicas: 1,1 %; personas físicas: 93,4 %. Los tramos se cuentan dentro de cada ámbito: la cuota municipal es una cota inferior. La cuota de personas jurídicas es mayor en municipios con alquiler y precio altos, más vivienda turística y mayor saldo exterior: asociación entre municipios, sin dirección causal. Verificador: V12-V02 (antes V02, «no analizada»). <!-- check:cifra-libre (identificadores de ficha) -->

## 6. Condiciones de vivienda por origen

A igual edad y renta (ECV), diferencia entre personas adultas de nacionalidad extranjera y española (en sus hogares): alquiler a precio de mercado 41,8 puntos (40,0-43,8 puntos); sobrecarga de más del 40 % 14,7 puntos (13,3-16,3 puntos); hacinamiento 8,2 puntos (6,4-9,9 puntos); inquilinos de mercado con alquiler de más del 30 % de la renta -0,85 puntos (-3,2 a 1,8 puntos). La diferencia en sobrecarga acompaña a la tenencia; no se atribuye a la nacionalidad. Por llegada, edad y tipo de hogar (Censo 2021): `output/v12/b6`. <!-- check:cifra-libre (umbrales de los indicadores y año del censo) -->

## 7. Turismo y presión residencial

Comunitat Valenciana: 51.268 viviendas anunciadas (INE) y 90.124 viviendas inscritas (registro GVA); València: 5.393 viviendas y 5.766 viviendas. Miden cosas distintas y se reportan ambas. Por municipio, distrito y barrio: `output/v12/b7`.

## Límites

Todo es descriptivo o contable (C4); en la tabla provincial de oferta, la obra nueva es C1 solo donde Catastro y MIVAU difieren menos de un 10 %. Celdas con menos de diez casos o error relativo superior al 30 % suprimidas. Decisiones: `docs/v12/decisiones.md`. <!-- check:cifra-libre (umbrales de supresión) -->
