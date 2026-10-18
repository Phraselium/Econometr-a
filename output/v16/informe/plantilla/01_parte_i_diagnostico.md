## Parte I · Diagnóstico

Esta parte recoge los hechos de la fase 2 de V16 a todas las escalas: nacional, comunidad autónoma (CCAA), provincia y municipio donde hay dato. No estima efectos. Cada cifra lleva su capa entre corchetes y, cuando hay varias fuentes, su rango.

### I.1 Cómo leer las cifras

- **[C1] Hecho.** Al menos dos fuentes de grupos distintos coinciden dentro de una tolerancia fijada antes de mirar las parejas nuevas. Se escribe «es» y se da el rango entre fuentes.
- **[C2] Cota.** Intervalo con supuestos explícitos.
- **[C4] Descriptivo o exploratorio.** Una sola fuente, o varias que no coinciden, o fuentes que no son independientes. Se escribe «se observa» y no se interpreta.
- **Si dos fuentes discrepan, se dan ambas.** No se elige una.
- **Medida de precio.** Cada cifra de compra dice qué mide. El IPV del INE está ajustado por calidad. Valor tasado (MIVAU), Notariado y Registradores son precios medios por m² sin ese ajuste. Son medidas distintas y pueden dar cuantías distintas.
- **Pre-registro.** Los resultados de V16 citados aquí tienen un pre-registro interno, sin sello de tiempo externo: etiqueta `prereg-v16` en el remoto, commit a8304ec, 2026-10-17. Los de V15, igual: etiqueta `prereg-v15`, commit 542b4fd, 2026-10-17. Los de esta parte son hechos y contabilidad (fase 2), no contrastes de hipótesis. <!-- check:cifra-libre (etiquetas, commit y fecha de pre-registro, años) -->

### I.2 Precio de compra

#### Nacional: nominal y real

**2019-2025.** El cambio acumulado nominal es {{V16-HEC-PRECIO-NOM-2019-2025}} [C1]. El cambio real, con el deflactor del IPC general, es {{V16-HEC-PRECIO-REAL-2019-2025}} [C1]. Las tres medidas por m² (tasación MIVAU, Notariado, Registradores) coinciden dentro de la tolerancia. El IPV del INE, ajustado por calidad, da otra cuantía y queda fuera de ese rango: su cifra figura en la definición de V16-HEC-PRECIO-NOM-2019-2025, sin id propio. <!-- check:cifra-libre (periodo) -->

**Otras ventanas.** Las medidas no coinciden, así que se publica el abanico y no se elige una.

| Ventana | Nominal | Real (IPC general) |
|---|---|---|
| 2007-2025 | {{V16-HEC-PRECIO-NOM-2007-2025:rango}} [C4] | {{V16-HEC-PRECIO-REAL-2007-2025:rango}} [C4] |
| 2013-2025 | {{V16-HEC-PRECIO-NOM-2013-2025:rango}} [C4] | {{V16-HEC-PRECIO-REAL-2013-2025:rango}} [C4] |

<!-- check:cifra-libre (periodos en la tabla) -->

**La 1.0, 2015-2025.** El IPV del INE da {{A23-P1}} [C4]. El núcleo formado por MIVAU, Notariado y Registradores es {{A23-P2}} [C1]. Los dos datos discrepan y se dan ambos. El residuo sin identificar entre ambos es {{A23-P3}} [C4]; no se descompone. <!-- check:cifra-libre (periodo) -->

**Precio por m² en 2025.** Registradores: {{A23-P6}} [C4]. Notariado: {{A23-P7}} [C4]. Son medidas distintas, de composición distinta. <!-- check:cifra-libre (periodo) -->

**Las fuentes se mueven juntas.** El primer componente de las cuatro fuentes recoge {{A23-P10}} [C4] de la varianza de la tasa anual. Es un resumen de comovimiento, no una explicación.

#### Comunidades autónomas

- Por CCAA se publican las tres medidas en `output/v16/f2_hechos/precios_ccaa.csv`. El deflactor es nacional: no hay IPC autonómico en el repositorio.
- Las medidas coinciden en el cambio real 2019-2025 en {{V16-HEC-PRECIO-CCAA-NCOINC-2019-2025}} [C4] comunidades de las 17. En 2007-2025, en {{V16-HEC-PRECIO-CCAA-NCOINC-2007-2025}} [C4]. En 2013-2025, en {{V16-HEC-PRECIO-CCAA-NCOINC-2013-2025}} [C4]. Fuera de esas comunidades, la medida elegida cambia la cuantía. <!-- check:cifra-libre (17 comunidades, periodos) -->
- Las ocho CCAA de la decisión K8 aparecen solo a escala de CCAA y nación. Nunca por provincia ni por debajo. <!-- check:cifra-libre (ocho CCAA del diseño) -->

#### Provincia: parte común y parte local

Se descompone la tasa anual de ln precio (valor tasado MIVAU, nominal, provincias no selladas) en un factor común y un residuo local. Es contabilidad, no causalidad.

| Periodo | Cuota del factor común (IC 95 % bootstrap) | R² mediano por provincia (mín.-máx.) |
|---|---|---|
| 2007-2013 | {{V16-CON-PRECIO-CUOTA-PC1-2007-2013}} [C4] | {{V16-CON-PRECIO-R2-PROV-2007-2013}} [C4] |
| 2014-2019 | {{V16-CON-PRECIO-CUOTA-PC1-2014-2019}} [C4] | {{V16-CON-PRECIO-R2-PROV-2014-2019}} [C4] |
| 2020-2026 | {{V16-CON-PRECIO-CUOTA-PC1-2020-2026}} [C4] | {{V16-CON-PRECIO-R2-PROV-2020-2026}} [C4] |

<!-- check:cifra-libre (periodos y nivel de confianza en la tabla) -->

- **Sesgo de la cuota.** Con pocas series y pocos periodos, la cuota queda sesgada al alza incluso sin factor. Por eso se compara con el azar en el informe de la fase.
- **Contraste con V8.** V8 estimó el factor común sobre CCAA. Con provincias, la cuota difiere de V8 en {{V16-CON-PRECIO-V8-DIF-PP}} [C4]. Discrepan y se informan ambas. Una explicación posible, no contrastada, es que las CCAA agregan provincias y promedian parte del residuo local.
- **Factor dinámico.** Un factor dinámico de una sola componente da R² medio con el factor de {{V16-CON-PRECIO-DFM-R2}} [C4].
- **Residuo local.** Tras quitar el factor, las correlaciones entre provincias de la misma CCAA son {{V16-CON-PRECIO-LOCAL-CCAA}} [C4]. Son pequeñas: el residuo es sobre todo específico de cada provincia.
- **Dispersión provincial.** El cociente P90/P10 del valor tasado por m² entre provincias no selladas es {{V16-ATL-DISP-PRECIO-PROV:num}} [C4] en 2026T2. <!-- check:cifra-libre (periodo, P90/P10 en el texto) -->

#### Municipio

A escala municipal solo València tiene valor tasado: el MIVAU publica los municipios con nombre, no con código INE. Para el resto de municipios no hay medida de precio de compra comparable en el repositorio. El atlas (Parte IV) usa el alquiler y la renta.

### I.3 Alquiler: contratos vigentes frente a contratos nuevos

**Qué mide cada serie.** El IPC de alquiler y SERPAVI miden el conjunto de contratos vigentes (stock). El IPVA separa contratos nuevos y existentes. Las fianzas (Incasòl, GVA) recogen contratos nuevos. IPVA y SERPAVI comparten fuente primaria (AEAT-IRPF): cuentan como un solo grupo.

**Nacional, contratos vigentes.**
- IPC de alquiler 2019-2025: cambio nominal {{V16-HEC-ALQ-IPC-NOMINAL-2019-2025}} [C4] y real {{V16-HEC-ALQ-IPC-REAL-2019-2025}} [C4].
- 2013-2025: nominal {{V16-HEC-ALQ-IPC-NOMINAL-2013-2025}} [C4], real {{V16-HEC-ALQ-IPC-REAL-2013-2025}} [C4].
- 2007-2025: nominal {{V16-HEC-ALQ-IPC-NOMINAL-2007-2025}} [C4], real {{V16-HEC-ALQ-IPC-REAL-2007-2025}} [C4].
- Con tres fuentes (IPC, IPVA, SERPAVI), el cambio nominal de los contratos vigentes 2019-2024 va de {{V16-HEC-ALQ-STOCK-NOMINAL-2019-2024:rango}} [C4]; el real, de {{V16-HEC-ALQ-STOCK-REAL-2019-2024:rango}} [C4].
- La 1.0 da, para 2015-2024, un núcleo IPC-IPVA de {{A23-A2}} [C1]. SERPAVI, con renta declarada y composición constante, da {{A23-A2b}} [C4] y discrepa del núcleo. Se dan ambos.
- En 2025 solo hay una fuente (el IPC); IPVA y SERPAVI acaban en 2024.

<!-- check:cifra-libre (periodos, tres fuentes) -->

**Contratos nuevos frente a vigentes.**
- Brecha de crecimiento 2021-2024 en Cataluña: es {{V16-HEC-ALQ-BRECHA-2124-CAT}} [C1], con dos estimaciones independientes (IPVA frente a fianzas menos IPC).
- En la Comunitat Valenciana, las dos estimaciones dan {{V16-HEC-ALQ-BRECHA-2124-CV:rango}} [C4]. No coinciden dentro de la tolerancia y no llegan a C1.
- Brecha de nivel en 2024 (IPVA): Cataluña {{V16-HEC-ALQ-NIVEL-2024-CAT}} [C4]; Comunitat Valenciana {{V16-HEC-ALQ-NIVEL-2024-CV}} [C4]. Nacional, brecha nuevo menos existente: {{A23-A6}} [C4].
- Contratos nuevos 2021-2024 (1.0): en Cataluña, IPVA nuevo e Incasòl dan {{A23-A9}} [C1]; en la Comunitat Valenciana, IPVA nuevo y fianzas GVA dan {{A23-A10}} [C1].
- Con fianzas hasta 2025: Cataluña {{V16-HEC-ALQ-BRECHA-2125-CAT}} [C4]; Comunitat Valenciana {{V16-HEC-ALQ-BRECHA-2125-CV}} [C4]. En 2025 no hay segunda fuente.
- Rotación: las fianzas equivalen a {{A23-A11}} [C4] de los contratos vigentes en Cataluña y a {{A23-A12}} [C4] en la Comunitat Valenciana.
- Cuota implícita de contratos nuevos en el IPVA: {{A23-A7}} [C4].

<!-- check:cifra-libre (periodos) -->

**Cómo leer una cifra de alquiler.** Un dato de contratos vigentes no describe lo que paga quien firma hoy. Un dato de fianzas o de contratos nuevos no describe lo que paga el conjunto de inquilinos. Hay que decir cuál de los dos se usa.

**Escala territorial.** SERPAVI da alquiler mediano por m² en {{V16-ATL-COB-ALQ-MUN}} [C4] municipios publicables (n y CV por celda; Parte IV). Inside Airbnb queda fuera de la serie de alquiler: es turístico y es un rastreo no validado.

### I.4 Esfuerzo de acceso: compra y alquiler

Fuente: ECV 2004-2025 (microdatos) con intervalos bootstrap aproximados. Todo es [C4]: fuente única. ECV y Eurostat son la misma encuesta; la coincidencia con Eurostat valida la implementación, no forma un C1. Entre 2013 y 2025 coincide con Eurostat; entre 2004 y 2012 no coincide en casi todos los años y esos años se tratan como no validados. <!-- check:cifra-libre (periodos de validación) -->

**España.** La sobrecarga del coste de la vivienda (gasto neto superior al 40 % de la renta neta) es {{V16-ESF-ESP-S40-2025}} [C4] de la población en 2025. Con el umbral del 30 %: {{V16-ESF-ESP-S30-2025}} [C4]. Cambio 2019-2025: {{V16-ESF-ESP-S40-2019_2025}} [C4]; 2015-2025: {{V16-ESF-ESP-S40-2015_2025}} [C4]; 2008-2025: {{V16-ESF-ESP-S40-2008_2025}} [C4]. Personas que quedan por debajo del umbral de pobreza tras pagar la vivienda: {{V16-ESF-ESP-RES-2025}} [C4]. <!-- check:cifra-libre (umbrales del 40 % y del 30 % del diseño, periodos) -->

**Esfuerzo de compra.** Se mide en propietarios con hipoteca. Sobrecarga 2025: {{V16-ESF-TEN-prop_con_hipoteca-S40-2025}} [C4]. Cambio 2019-2025: {{V16-ESF-TEN-prop_con_hipoteca-S40-2019_2025}} [C4]. Propietarios sin hipoteca: {{V16-ESF-TEN-prop_sin_hipoteca-S40-2025}} [C4]. El gasto recoge intereses, no amortización, en esta variable; no es el precio de compra. Ratio precio/renta disponible del índice OCDE, cambio 2019-2025: España {{V16-HEC-INTL-HPI_YDH-ES-2019-2025}} [C4], mediana UE {{V16-HEC-INTL-HPI_YDH-MED-2019-2025}} [C4]. no hay en el repositorio una cifra de años de renta por vivienda tipo; la más cercana es el cambio del cociente precio/renta de la OCDE, {{V16-HEC-INTL-HPI_YDH-ES-2019-2025}} en 2019-2025 [C4] <!-- check:cifra-libre (periodos) -->

**Esfuerzo de alquiler.** Alquiler a precio de mercado, sobrecarga 2025: {{V16-ESF-TEN-alquiler_mercado-S40-2025}} [C4]. Cambio 2019-2025: {{V16-ESF-TEN-alquiler_mercado-S40-2019_2025}} [C4]; 2015-2025: {{V16-ESF-TEN-alquiler_mercado-S40-2015_2025}} [C4]. Alquiler reducido o cesión: {{V16-ESF-TEN-alquiler_reducido_cesion-S40-2025}} [C4]. La 1.0, en la misma medida para alquiler de mercado, da {{V10-ATL-A1}} [C4]. Son la misma encuesta con implementaciones distintas. <!-- check:cifra-libre (periodos) -->

**Por grupo (sobrecarga del 40 %, 2025).**
- Quintil de renta: Q1 {{V16-ESF-QUI-Q1-S40-2025}} [C4]; Q2 {{V16-ESF-QUI-Q2-S40-2025}} [C4]; Q3 {{V16-ESF-QUI-Q3-S40-2025}} [C4]; Q4 {{V16-ESF-QUI-Q4-S40-2025}} [C4]. El quintil 5 queda suprimido por muestra insuficiente.
- Edad del sustentador: 16-34 años {{V16-ESF-EDA-16-34-S40-2025}} [C4]; 35-49 {{V16-ESF-EDA-35-49-S40-2025}} [C4]; 50-64 {{V16-ESF-EDA-50-64-S40-2025}} [C4]; 65 o más {{V16-ESF-EDA-65+-S40-2025}} [C4].
- Nacionalidad del sustentador: española {{V16-ESF-NAC-Espana-S40-2025}} [C4]; otra de la UE {{V16-ESF-NAC-UE-S40-2025}} [C4]; de fuera de la UE {{V16-ESF-NAC-Resto-S40-2025}} [C4].
- Región (NUTS2): la ECV no tiene provincia. Los valores por región, con intervalos, están en `output/v16/f2_esfuerzo/esfuerzo_por_anio.csv`. El cociente P90/P10 entre CCAA es {{V16-ATL-DISP-ECV40-CCAA:num}} [C4] en 2025; el atlas (Parte IV) lo muestra por territorio.

<!-- check:cifra-libre (umbral del 40 %, quintiles, tramos de edad, P90/P10 en el texto) -->

**Descomposición contable 2019-2025.** El cambio observado del esfuerzo medio en alquiler de mercado es {{V16-ESF-DES-alquiler_mercado-observado-total-2019_2025}} [C4]; la parte atribuida a la composición por reponderación (DFL) es {{V16-ESF-DES-alquiler_mercado-DFL-composicion-2019_2025}} [C4]. En propietarios con hipoteca, el cambio observado es {{V16-ESF-DES-prop_con_hipoteca-observado-total-2019_2025}} [C4] y la composición, {{V16-ESF-DES-prop_con_hipoteca-DFL-composicion-2019_2025}} [C4]. Es una suma contable: la renta entra a la vez en la ratio y como covariable. No se lee como mecanismo. Los métodos discrepan en la mitad de las comparaciones y se publican todos (`comparacion_metodos.csv`). <!-- check:cifra-libre (periodos, mitad de las comparaciones) -->

**Esfuerzo de alquiler por territorio fino.** La ratio descriptiva «alquiler anual de 80 m² sobre renta neta del hogar» (SERPAVI y ADRH) no es la tasa de sobrecarga de la ECV y no debe compararse con ella. Está en {{V16-ATL-COB-ESF-SECCION}} [C4] secciones censales publicables en 2023. Detalle en la Parte IV. <!-- check:cifra-libre (80 m², año) -->

### I.5 Hogares, viviendas terminadas y déficit

#### Hogares

**Aumento 2021-2025 (1.0).** El aumento del número de hogares es {{dh_2125}} [C1]. Los dos extremos son ECP y EPA, sin corrección, con ventanas distintas (stock a 1 de enero frente a media anual). La ECP sola da {{V16-HEC-HOGARES-ECP-2125}} [C4]; la EPA da un cambio mayor en {{V16-CON-HOG-ECP-EPA-DISCREPANCIA}} [C4]. Se dan ambas.

**Contabilidad del cambio de hogares 2021-2025 (ECP).** Cambio observado: {{V16-CON-HOG-CAMBIO}} [C4] (valor ECP, rango ECP y EPA). Se reparte así:
- población: {{V16-CON-HOG-POBLACION}} [C4];
- composición por nacionalidad: {{V16-CON-HOG-COMPOSICION-NACIONALIDAD}} [C4];
- estructura por edad: {{V16-CON-HOG-ESTRUCTURA-EDAD}} [C4];
- residuo de jefatura: {{V16-CON-HOG-JEFATURA}} [C4].

La composición resta porque las tasas de jefatura por edad del Censo 2021 son menores en la población extranjera. Mezcla migración y cambios de nacionalidad. El residuo de jefatura es una tasa agregada a población constante, no una tasa por edad: no hay tasas por edad después de 2021.

**Por CCAA (11 CCAA sin provincias selladas).** El residuo de jefatura, en porcentaje de los hogares iniciales, tiene mediana y rango {{V16-CON-HOG-CCAA-JEFATURA-PCT}} [C4]. La parte de población en el cambio: {{V16-CON-HOG-CCAA-POBLACION-PCT}} [C4]. Las provincias están en `output/v16/f2_contabilidad/hogares_ecp_2021_2025.csv`. Las ocho CCAA de K8 no se calculan. <!-- check:cifra-libre (11 CCAA, ocho CCAA del diseño) -->

**Serie larga 2002-2021 (EPA, nacional).** Cambio {{V16-CON-HOG-EPA-2002-2021-CAMBIO}} [C4]: población {{V16-CON-HOG-EPA-2002-2021-POBLACION}} [C4]; composición {{V16-CON-HOG-EPA-2002-2021-COMPOSICION-NACIONALIDAD}} [C4]; estructura por edad {{V16-CON-HOG-EPA-2002-2021-ESTRUCTURA-EDAD}} [C4]; jefatura {{V16-CON-HOG-EPA-2002-2021-JEFATURA-RESIDUO}} [C4]. El reparto depende de la tasa de referencia: con las tasas del Censo 2011 la jefatura sería otra. En 2014-2021 el residuo de jefatura es {{V16-CON-HOG-EPA-2014-2021-JEFATURA}} [C4], compatible con la ruptura de la EPA en 2021T1. No se interpreta. <!-- check:cifra-libre (periodos, trimestre de la ruptura) -->

**Antecedente V12, 2011-2021.** Crecimiento de hogares {{V12-B3-hogares-crec}} [C4], con componentes de población {{V12-B3-hogares-poblacion}} [C4], estructura por edad {{V12-B3-hogares-estructura}} [C4] y jefatura {{V12-B3-hogares-jefatura}} [C4]. Hogares con persona de referencia extranjera en 2021: {{V12-B3-hogares-ext}} [C4]. No se repiten en V16.

#### Viviendas terminadas

- **Territorio común, 2019-2024 (1.0).** Las viviendas terminadas al año son {{terminadas_1924}} [C1] (Ministerio y Catastro, dentro de ±15 %; sin País Vasco ni Navarra).
- **Ampliación a 2025 (MIVAU, solo libres).** En 2025: {{V16-HEC-OBRA-TERMINADAS-2025}} [C4]. Acumulado 2021-2025: {{V16-HEC-OBRA-TERMINADAS-2125}} [C4]. Por hogar nuevo (ECP): {{V16-HEC-OBRA-SOBRE-HOGARES-2125}} [C4]. Esta ampliación no sustituye a `terminadas_1924` ni a `dh_2125`; las terminadas de la 1.0 incluyen protegidas.

<!-- check:cifra-libre (periodos, tolerancia del diseño, identificadores) -->

#### Déficit acumulado

El déficit es hogares nuevos menos viviendas terminadas. Las viviendas liberadas por envejecimiento nunca se restan de la necesidad: la proyección de hogares del INE ya las descuenta.
- 2021-2024, sin bajas del parque, todas las variantes de corrección de la EPA y de terminadas: {{L3-DEF-2124-SINBAJAS}} [C2].
- Misma cota sin las dos variantes que conservan el salto de la EPA: {{L3-DEF-2124-SENS}} [C2].
- Con las bajas estimadas en la versión 5.1: {{L3-DEF-2124-BAJAST1}} [C4].
- 2021-2025, sin bajas: {{L3-DEF-2125}} [C4]; el dato de terminadas de 2025 es frágil.

Los rangos recogen el desacuerdo entre fuentes y correcciones, no una incertidumbre estadística. <!-- check:cifra-libre (periodos, versión 5.1) -->

### I.6 Demografía

- **Población y migración.** Saldo migratorio exterior (EMCR) 2021-2024: {{V16-CON-MIG-EMCR-SALDO}} [C4]. La población extranjera de la ECP crece en un importe que incluye cambios de nacionalidad; no se concilian las dos cifras. EMCR solo se usa desde 2021 por la ruptura de nivel anterior.
- **Dónde se concentra.** Entre municipios no sellados, el cociente P90/P10 de la población de nacionalidad extranjera es {{V16-ATL-DISP-EXTRANJERA:num}} [C4] (censo anual 2025). El de la renta es {{V16-ATL-DISP-RENTA-HOGAR:num}} [C4] (2023).
- **Jóvenes en el hogar de origen.** Personas de 30 a 34 años que viven con al menos uno de sus padres: {{V10-ATL-A10}} [C4] en 2018 y {{V10-ATL-A11}} [C4] en 2025 (EPA).
- **Titularidad y acceso.** Entre adultos de renta y edad iguales, la brecha de alquiler a precio de mercado entre nacionalidad extranjera y española es {{V12-B6-brecha-tenencia_3}} [C4] (V12).

<!-- check:cifra-libre (años, edades 30 a 34, P90/P10 en el texto) -->

### I.7 Parque, viviendas vacías y lanzamientos

**Parque (Censo 2021).** Viviendas familiares: {{V16-HEC-PARQUE-TOTAL-2021}} [C4]; principales {{V16-HEC-PARQUE-PRINCIPALES-2021}} [C4]; no principales {{V16-HEC-PARQUE-NOPRINCIPALES-2021}} [C4]. El Catastro y el Censo difieren en {{V16-HEC-PARQUE-CATASTRO-CENSO-2021}} [C4] en el territorio común. Se mantiene C4 porque no está demostrada la independencia entre ambos.

**Vacías y esporádicas.** Vacías por consumo eléctrico: {{V16-HEC-VACIAS-CONSUMO-2021}} [C4], {{V16-HEC-VACIAS-PCT-2021}} [C4] de las viviendas familiares. Uso esporádico: {{V16-HEC-ESPORADICO-2021}} [C4]. Las «vacías del Censo» y las «vacías por consumo» son la misma cifra: la tabla 59531 es del propio Censo, con el mismo universo. No son dos fuentes. Por municipio, el cociente P90/P10 de las vacías es {{V16-ATL-DISP-VACIAS:num}} [C4]. <!-- check:cifra-libre (tabla 59531, P90/P10 en el texto) -->

**Lanzamientos (CGPJ, fuente única).** 2013: {{V16-HEC-LANZ-2013}} [C4]. Máximo, en 2014: {{V16-HEC-LANZ-PICO}} [C4]. 2025: {{V16-HEC-LANZ-2025}} [C4]. Últimos cuatro trimestres: {{V16-HEC-LANZ-UM4T}} [C4]. Por tipo en 2025: hipotecaria {{V16-HEC-LANZ-TIPO-HIPOTECARIA-2025}} [C4]; arrendamientos (LAU) {{V16-HEC-LANZ-TIPO-LAU-2025}} [C4]; otros {{V16-HEC-LANZ-TIPO-OTROS-2025}} [C4]. El total nacional es el de los tribunales superiores, no la suma de provincias. <!-- check:cifra-libre (periodos) -->

**Comparación internacional (OCDE y Eurostat).** España no tiene segunda fuente independiente: todo es [C4].
- Precio real 2019-2025: España {{V16-HEC-INTL-RHP-ES-2019-2025}}; mediana UE {{V16-HEC-INTL-RHP-MED-2019-2025}}.
- Precio real 2007-2025: España {{V16-HEC-INTL-RHP-ES-2007-2025}}; mediana UE {{V16-HEC-INTL-RHP-MED-2007-2025}}.
- Precio/alquiler 2019-2025: España {{V16-HEC-INTL-HPI_RPI-ES-2019-2025}}; mediana UE {{V16-HEC-INTL-HPI_RPI-MED-2019-2025}}.
- Sobrecarga del coste de la vivienda 2025 (España y UE): {{V16-HEC-INTL-SOBRECARGA-ES-2025}}.

Vivienda pública por habitante frente a la UE: sin dato (la descarga de la OCDE, tabla PH4.2, está pendiente en docs/v16/tareas_autor.md). No se estima con otra fuente. <!-- check:cifra-libre (periodos, código de tabla) -->

### I.8 Qué deja esta parte sin resolver

- La medida de precio cambia la cuantía en varias ventanas. Ninguna cifra única resume «lo que ha subido el precio».
- En alquiler, solo Cataluña supera la vara de C1 en la brecha entre contratos nuevos y vigentes.
- El esfuerzo de acceso viene de una encuesta con intervalos aproximados; no hay dato por provincia.
- El déficit es una cota entre fuentes, no una estimación puntual.
- Nada de lo anterior contrasta una política ni un mecanismo. Los mecanismos están en la Parte II.
