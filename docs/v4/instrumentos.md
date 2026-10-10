# Taxonomía de instrumentos de vivienda (M5a, 2026-10-10)

Se evalúan instrumentos, no actores. La procedencia (quién, página, cita) está solo en `data/raw/v4/medidas_programas.csv`. Aquí solo hay recuentos de documentos.

## Alcance y límites de la recogida
- Documentos leídos y codificados: 8 programas de las elecciones generales de 2023 de grupos con representación en la XV legislatura. 71 medidas en el CSV.
- NO recogidos (ver `docs/v4/fuentes_fallidas.md`): 3 programas de grupos con representación (PDF demasiado grande para la herramienta, o no localizado) y las proposiciones de ley sobre vivienda de la XV legislatura (congreso.es), no consultadas por límite de presupuesto. Los recuentos «n de 8» son por tanto cotas inferiores sobre el conjunto de grupos.
- Alcance de lectura por documento: solo el apartado de vivienda y, donde se localizó, medidas de vivienda en otros apartados (suelo, ocupación, fiscalidad). Un documento puede tener medidas en páginas no leídas.
- Una medida que aparece en varios documentos cuenta como un instrumento. Cada medida del CSV tiene un único instrumento principal (los programas mezclan varios en una frase).
- Normas «en vigor»: solo se afirma lo que consta en `docs/` (verificado en v2/v3) o en la cita literal del programa. Las demás van marcadas «sin verificar en BOE» y deben comprobarse antes de citarse.

## A. Instrumentos propuestos en al menos un documento
| Id | Instrumento | Mecanismo (1-2 frases) | Docs (de 8) | En vigor en España |
|---|---|---|---|---|
| I01 | Regulación de precios del alquiler (zonas tensionadas, índice de referencia, topes) | Limita el crecimiento o el nivel de la renta en zonas declaradas tensionadas. Hay propuestas de ampliarlo (3 docs) y de derogar el marco vigente (2 docs). | 5 | Sí: Ley 12/2023, de 24 de mayo, por el derecho a la vivienda (cita en los programas y en docs v2). Aplicación efectiva solo en Cataluña desde 16/03/2024 según el Apunte Fedea 2026/15 (NO VERIFICADA). |
| I02 | Parque público o social de alquiler a gran escala | El sector público construye, compra o rehabilita vivienda para alquiler por debajo de mercado. Aumenta oferta y desplaza demanda del mercado privado. | 6 | Parcial: Plan Estatal de Vivienda 2022-2025 (sin verificar en BOE). El peso del parque social ronda el 2,5 % de principales según una cifra de un programa (no verificada). |
| I03 | Reservas de suelo para vivienda protegida | Obliga a destinar un porcentaje de nuevos desarrollos a VPO. Reduce el suelo libre y condiciona la oferta de mercado. | 3 | Sí, reserva del 30 % en suelo urbanizable (texto refundido de la Ley de Suelo, RDL 7/2015; sin verificar en BOE). |
| I04 | Movilización de suelo y patrimonio públicos (incluida la cartera de la sociedad de gestión de activos) | Cede o promueve en suelo público, o transfiere activos, para vivienda asequible. Baja el coste del suelo en esas promociones. | 6 | Parcial: SEPES y Sareb existen; transferencias por convenio (sin verificar en BOE). |
| I05 | Captura de plusvalías del suelo | La administración recupera parte del aumento de valor por recalificación y lo destina a política de vivienda. | 1 | Sí, parcial: cesión de aprovechamiento a la administración (TRLSRU art. 18; sin verificar). |
| I06 | Avales públicos a hipotecas | El Estado garantiza parte del préstamo (20 %, hasta 95 % del precio financiado) para compradores jóvenes. Relaja la restricción de entrada; con oferta rígida puede capitalizarse en precio. | 2 | Sí: línea ICO-MIVAU de avales, 2024; cifras de diseño de prensa especializada no oficial (sin verificar en BOE). |
| I07 | Fiscalidad y ahorro para vivienda en propiedad (IVA, ITP, cuenta ahorro, deducciones) | Reduce el coste de uso del propietario o el coste de compra. Ayuda a la demanda. | 3 | Sí, parcial: deducción por vivienda habitual suprimida para adquisiciones desde 2013 (sin verificar en BOE); ITP autonómico. |
| I08 | Ayudas directas al alquiler (demanda) | Subvención al inquilino. Con oferta inelástica, parte se traslada a la renta. | 3 | Sí: Bono Alquiler Joven y ayudas de los planes estatales (RD 42/2022, sin verificar en BOE). |
| I09 | Ayudas a hogares hipotecados (bono, congelación o limitación de cuotas, código de buenas prácticas, dación en pago) | Transfiere o aplaza carga financiera a deudores. Efecto en precios indirecto. | 3 | Sí, parcial: Código de Buenas Prácticas y medidas anticrisis (RDL 19/2022, RDL 8/2023; sin verificar en BOE). |
| I10 | Movilización de vivienda vacía (registro, convenios, recuperación de posesión) | Pone en uso vivienda desocupada con registro, incentivos u otros medios. El efecto depende de cuánta vacía esté realmente disponible. | 4 | Parcial: registros autonómicos; sin verificar. |
| I11 | Rehabilitación del parque | Ayudas a la rehabilitación y a la eficiencia energética. Amplía oferta utilizable sin suelo nuevo. | 1 | Sí: ayudas con fondos europeos (sin verificar en BOE). |
| I12 | Industrialización de la construcción | Prefabricación y construcción industrializada para bajar plazos y costes por vivienda. | 1 | No como política específica (clúster citado solo como propuesta). Sin verificar. |
| I13 | Agilización y seguridad jurídica urbanística | Menos plazo e incertidumbre en planeamiento y licencias, para acelerar la oferta. | 1 | No como medida de licencias; sin verificar. |
| I14 | Seguridad jurídica del propietario y antiocupación | Acorta desalojos y refuerza la posesión. Efecto esperado sobre la oferta de alquiler por menor riesgo percibido. | 2 | Sí, parcial: reforma de 2018 de desalojo en ocupación; sin verificar. |
| I15 | Fiscalidad de arrendadores e inversores inmobiliarios | Incentivos o recargos fiscales condicionados al precio o al uso. | 2 | Sí, parcial: reducción del 50-90 % en el IRPF del arrendador condicionada a zona tensionada (Ley 12/2023; sin verificar la cuantía). |
| I16 | Alquiler turístico y de temporada | Regula esos usos para que no eludan el control de rentas ni retiren oferta residencial. | 2 | Sí, parcial: Ley 12/2023 y registro de alquileres de corta duración (sin verificar en BOE). |
| I18 | Duración y prórroga de contratos de alquiler | Alarga la estabilidad del contrato. Efecto contractual, con posible efecto sobre la oferta. | 3 | Sí: LAU (prórroga de 5 años, 7 si arrendador es persona jurídica; sin verificar en BOE). |
| I19 | Sinhogarismo y vivienda de emergencia | Provisión directa a personas sin hogar (Housing First). | 2 | Parcial: estrategia nacional vigente; sin verificar. |
| I20 | Colaboración público-privada y nuevas modalidades (derecho de superficie, cooperativas de cesión de uso, asociaciones sin ánimo de lucro) | El sector público aporta suelo o garantías y el privado promueve y gestiona. | 2 | Parcial; sin verificar. |
| I21 | Limitación de compras especulativas o de no residentes | Condiciona o restringe la compra con fin de inversión. Modifica la demanda de inversión. | 2 | Sí, parcial: visado de residencia por inversión inmobiliaria (Ley 14/2013), citado en un programa como vigente. |
| I22 | Obligaciones a grandes tenedores (alquiler social obligatorio) | Impone cuota de alquiler social a propietarios grandes. | 1 | Sí, parcial: definición de gran tenedor y obligaciones en la Ley 12/2023 (sin verificar). |
| I24 | Derecho subjetivo a la vivienda | Convierte el acceso en un derecho exigible. Requiere oferta pública o ayudas para ser efectivo. | 2 | No como derecho subjetivo exigible. |
| I25 | Coordinación multinivel (pacto de Estado) | Acuerdo estable entre Estado, comunidades y entes locales sobre competencias y financiación. | 1 | No. |
| I26 | Gravamen sobre suelo urbanizable ocioso | Grava el suelo urbanizable sin desarrollar para incentivar su puesta en uso. | 1 | No a nivel estatal. |
| I27 | Recargo o impuesto a la vivienda vacía | Encarece mantener vivienda desocupada mediante un recargo en un impuesto local o estatal. | 1 | Sí, parcial: recargo del IBI a vivienda desocupada (TRLRHL art. 72.4; sin verificar). |

## B. Instrumentos no propuestos (o propuestos por 0-1 documentos) añadidos por el equipo
| Id | Instrumento | Mecanismo | Docs (de 8) | En vigor |
|---|---|---|---|---|
| N1 | Agilización de licencias (plazos, silencio positivo, ventanilla única) | Reduce el tiempo y la incertidumbre del permiso. En la literatura el retraso regulatorio eleva precios (Hilber y Vermeulen 2016). | 0 | Sin verificar; el silencio positivo existe de forma general, pero no como medida de vivienda. |
| N2 | Aumento de edificabilidad o densidad (zonificación permisiva) | Eleva el techo de oferta en suelo ya urbano. Elasticidad de oferta baja es el supuesto clave (Saiz 2010). | 0 | No como medida estatal. |
| N3 | Impuesto sobre el valor del suelo (en lugar del impuesto sobre la construcción) | Grava el suelo, no la edificación. Reduce la retención especulativa. | 0 (I26 es el más cercano) | No. |
| N4 | Incentivo fiscal a la promoción de alquiler asequible privado (tipo crédito fiscal a la oferta) | Subvenciona al promotor privado a cambio de rentas limitadas. | 0 | Parcial; sin verificar. |
| N5 | Industrialización de la construcción | Ya figura como I12 (1 documento); se evalúa también por estimaciones de coste. | 1 | Ver I12. |
| N6 | Captura de plusvalías del suelo | Ya figura como I05 (1 documento). | 1 | Ver I05. |
| N7 | Impuesto o recargo a la vivienda vacía | Ya figura como I27 (1 documento). | 1 | Ver I27. |
| N8 | Alquiler social a gran escala | Ya figura como I02 (6 documentos). | 6 | Ver I02. |
| N9 | Ayudas a la demanda con oferta rígida | No es un instrumento aparte: agrupa I06, I07, I08 e I09. Se analiza como familia por su riesgo de capitalización en precios. | I06+I07+I08+I09 | Ver cada uno. |

## Cómo se usa en M5
Rúbrica común por instrumento: efecto esperado en precio, en cantidad, requisito de oferta y evidencia (ver `docs/v4/literatura_v4.md`). La simulación P-D usa solo el rango de la literatura y las elasticidades de oferta ya registradas. Ningún instrumento se puntúa por quién lo propone.
