# V18 · Fase 3 · Abogado del diablo sobre el plan de replicación (2026-10-20)

Revisión de solo lectura de docs/v18/plan_replicacion.md (versión del commit d4e9869). No había estimaciones: se atacan los diseños. «plan:N» es la línea del plan revisado. Veredicto: **resiste con limitaciones**; E1-A1, E3-R1, E5-R1 y E2-R1 no resisten en su forma actual y necesitan las pruebas siguientes en la adenda antes de la etiqueta; T1-T3 antes de la fase 5.

## Transversales
- **T1 (alta).** El criterio I6 (coherencia con la literatura, con la vía del solapamiento de IC95) decide la entrada en B5 y en la contabilidad: sesga la magnitud preferida hacia la literatura. Prueba: I6 solo etiqueta; B5 con y sin las estimaciones que fallan I6; sin vía de solapamiento si el IC propio es más de 3 veces más ancho.
- **T2 (alta).** La contabilidad multiplica efectos relativos entre provincias (con efectos de año) por variaciones nacionales; además las magnitudes salen de 39 provincias sin las de más inmigración, turismo y compra extranjera. Prueba: rotular «relativa entre provincias, sin el componente común»; contrastar el agregado con F1 y el SVAR de V8 sin sumar; no extrapolar fuera del soporte.
- **T3 (alta).** El plan permite lenguaje causal en cifras de capa C4, contra la regla del proyecto (causalidad solo en C3/C3s). Prueba: decisión expresa del autor antes de la etiqueta; hasta entonces check_v18 rechaza «causa» y «efecto causal» también en IDENTIFICADO.
- **T4 (media).** Pretendencias con p > 0,10 y poca potencia (Roth). Prueba: pendiente previa detectable al 80 % en todos los diseños de evento o shift-share; el sesgo implicado debe ser menor que la mitad del efecto de referencia.
- **T5 (media).** Doble cómputo E3/E9 (mismas cuotas del padrón; Reino Unido pesa 0,157 en Rotemberg en Q3-c). Prueba: añadir E3/E9 a la regla de no doble cómputo; E3 sin UE-15, Noruega y Suiza; correlación entre instrumentos.

## Por estudio
- **E1-A1 (alta).** Proximidad a atractivos × noches, con efectos municipio × año, puede medir la recuperación post-COVID del centro; elegido tras H3 (p = 0,931) y Q2 nulos. Pruebas: distancia al centro × año; placebo con hospitales o universidades × noches; sin 2021; H3 coprincipal en la misma familia de Holm.
- **E1-R2 (alta).** Las licencias HUT están congeladas (moratoria, PEUAT): el «cuándo» mueve anuncios, no licencias. Pruebas: signo y F de primera etapa por subperiodo; si se concentra en 2020-2021, como mucho SUGESTIVO; distancia al centro × año.
- **E1-R3 (media).** Dosis de 2018 posterior a la ventana y preperiodo de dos años. Prueba: tendencia por distancia al centro de 2011-2013 y potencia del preperiodo.
- **E1, medida (media).** Composición de SERPAVI. Prueba: número de viviendas en SERPAVI como resultado.
- **E2-R1 (alta).** COVID en el periodo posterior; controles a más de 10 km definidos tras el fallo de V9-D1b (pretendencia p = 0,000). Pruebas: reversión tras la STC 37/2022 (2022T2-2023T4); densidad HUT 2019 × post; controles emparejados por tamaño y tensión; control de V9-D1b coprincipal; errores por comarca o Conley.
- **E2, medida (media).** Desvío a temporada o a no depositar la fianza. Prueba: contratos registrados por hogar inquilino como resultado; A5 (temporada) como limitación que cierra el paso a IDENTIFICADO.
- **E2-A1/A2 (media).** A1 repite H1/H2 (evaluación sellada pendiente); en el País Vasco D1c ya dio pretendencia p = 0,000. Prueba: A1 no se publica antes de la evaluación sellada de H1/H2; A2 declara el fallo previo.
- **E3-R1 (alta).** Cuotas del Censo 2001 dentro de la ventana 1998-2008, elegidas tras el F de 3,4-4,6 de V9-D4; lista de orígenes no fijada. Pruebas: Censo 1991 como principal o R1 en 2002-2008; lista fija de 16 orígenes.
- **E3, exclusión (alta).** Los asentamientos reflejan demanda (construcción, agricultura, segunda residencia). Pruebas: cuota de construcción 2001 × año y costa × año; sin UE-15; saldo migratorio interior de nativos como resultado; ficticias de la regularización de 2005 y de las bajas por caducidad de 2006.
- **E3, inferencia (media).** Pocos choques efectivos (Rumanía pesa 0,475). Prueba: regla de menos de 20 choques efectivos (1/HHI) también en E3.
- **E5-R1 (alta).** El Bartik principal incluye la construcción (exclusión violada mecánicamente); 2002-2025 mezcla auge y caída. Pruebas: excluir construcción, inmobiliarias y finanzas en la principal; elasticidad por auge y caída; exposición a cajas de 2007 × año.
- **E6-R1 (alta).** La mediana SERPAVI de la sección incluye el edificio nuevo; los controles están en obra. Pruebas: solo secciones contiguas; fecha de inicio de obra.
- **E6-R2 (media).** Poca lluvia en verano; DANA de otoño. Pruebas: placebo de lluvia sobre pernoctaciones; sin 2019 y 2024 en València; medida trimestral.
- **E7-R1/R2 (media).** Prima soberana en 2010-2013; dos referencias (−2 % y −5 %). Pruebas: diferencial a 10 años y sin 2010-2013; una sola referencia; en A2, cuota de compradores extranjeros × choque.
- **E8 (alta).** Cambios del ITP endógenos a la caída de recaudación y simultáneos al IVA de la obra nueva y al fin de la deducción; fechas corregidas tras Q6. Pruebas: reglas de codificación de fechas fijadas ahora; recaudación previa y déficit autonómico; signo sin 2012-2013 como condición; banda de ±3 meses; Monte Carlo con 8 clusters.
- **E9 (alta).** Choques casi comunes absorbidos por los efectos de año; signo ambiguo; canal turístico. Pruebas: contar choques efectivos antes (menos de 10: NO ESTIMABLE); pernoctaciones por origen × exposición; signo esperado fijado ahora.
- **F1, F2, F4 (alta).** V7.2 y V8-M4 no hallaron cointegración. Prueba: si el contraste de límites no rechaza, no se publican elasticidades de largo plazo ni sobrevaloración y no se hace F4.
- **E12-A1 (baja).** Persistencia regional de la protegida 1991-1995. Prueba: añadir la obra libre de 1991-1995.

## Especificaciones elegidas conociendo un resultado previo
E1-A1 (tras H3 y Q2), E2-R1 (tras V9-D1b), E3-R1/R2 (tras V9-D4), E8 (tras Q6), E5 sin Red Natura (tras Q4, declarado), E7 (debilidad conocida). La especificación anterior debe ir como coprincipal en la misma familia de Holm.
