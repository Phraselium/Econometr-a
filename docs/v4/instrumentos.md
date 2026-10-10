# Taxonomía de instrumentos de vivienda (M5a, recalculada desde el CSV, 2026-10-10)

Se evalúan instrumentos, no actores. La procedencia (quién, página, cita) está solo en `data/raw/v4/medidas_programas.csv`. Aquí solo hay recuentos de documentos y de medidas.

## Alcance, reglas y límites
- 9 programas de las elecciones generales de 2023 de grupos con representación en la XV legislatura, codificados en 88 medidas (recuento del CSV). Cobertura por documento: `docs/v4/cobertura_programas.md`.
- Procedencia: 4 de los 9 documentos se leyeron en «copia no oficial alojada por un medio»; los otros 5, en la web del propio grupo. No se comprobó que las 4 copias coincidan con la versión oficial.
- NO recogidos (`docs/v4/fuentes_fallidas.md`): 2 programas de grupos con representación (no localizados) y las proposiciones de ley de la XV legislatura (congreso.es).
- Regla de codificación única. Cada medida tiene un instrumento principal. La columna `direccion` vale «a favor/ampliar» si la medida crea, mantiene, amplía o refuerza el instrumento tal como está definido en su rótulo, y «derogar/reducir» si propone derogarlo o suprimirlo. Toda propuesta de derogar el control de rentas o la Ley 12/2023 es I01 con «derogar/reducir» en todos los documentos.
- Los recuentos por instrumento separan documentos a favor y en contra: un documento con posiciones opuestas contaría en ambas columnas. Nadie «propone» un instrumento por figurar en la columna en contra.
- Normas «en vigor»: solo se afirma lo documentado en `docs/` o en la cita literal; el resto va «sin verificar en BOE».

## A. Instrumentos que aparecen en el CSV
| Id | Instrumento | Mecanismo (1-2 frases) | Medidas | Docs a favor | Docs en contra | En vigor en España |
|---|---|---|---|---|---|---|
| I01 | Regulación de precios del alquiler (zonas tensionadas, índice de referencia, topes) | Limita el crecimiento o el nivel de la renta en zonas declaradas tensionadas. | 7 | 3 | 4 medidas en 3 docs | Sí: Ley 12/2023, de 24 de mayo (docs v2). Efectiva solo en Cataluña desde 16/03/2024 según Fedea 2026/15 (NO VERIFICADA). |
| I02 | Parque público o social de alquiler a gran escala | El sector público construye, compra o rehabilita vivienda para alquiler por debajo de mercado. | 9 | 7 | 0 | Parcial: Plan Estatal 2022-2025 (sin verificar en BOE). |
| I03 | Reservas de suelo para vivienda protegida | Obliga a destinar un porcentaje de nuevos desarrollos a VPO. | 3 | 3 | 0 | Sí, 30 % en suelo urbanizable (RDL 7/2015; sin verificar). |
| I04 | Movilización de suelo y patrimonio públicos (incl. cartera de la sociedad de activos) | Cede o promueve en suelo público, o transfiere activos, para vivienda asequible. | 11 | 7 | 0 | Parcial (SEPES, Sareb; sin verificar). |
| I05 | Captura de plusvalías del suelo | La administración recupera parte del aumento de valor por recalificación. | 1 | 1 | 0 | Parcial: cesión de aprovechamiento (TRLSRU art. 18; sin verificar). |
| I06 | Avales públicos a hipotecas | El Estado garantiza parte del préstamo a compradores jóvenes. Con oferta rígida puede capitalizarse en precio. | 2 | 2 | 0 | Sí: línea ICO-MIVAU 2024 (cifras de prensa especializada; sin verificar en BOE). |
| I07 | Fiscalidad y ahorro para vivienda en propiedad (IVA, deducciones, cuenta ahorro) | Reduce el coste de uso o de compra del propietario. | 6 | 4 | 0 | Parcial: deducción por vivienda habitual suprimida desde 2013 (sin verificar). |
| I08 | Ayudas directas al alquiler (demanda) | Subvención al inquilino; con oferta inelástica parte se traslada a la renta. | 4 | 4 | 0 | Sí: Bono Alquiler Joven (RD 42/2022; sin verificar). |
| I09 | Ayudas a hogares hipotecados | Transfiere o aplaza carga financiera a deudores. | 5 | 3 | 0 | Parcial: Código de Buenas Prácticas, RDL 19/2022 y 8/2023 (sin verificar). |
| I10 | Movilización de vivienda vacía (registro, convenios, recuperación de posesión) | Pone en uso vivienda desocupada. | 4 | 4 | 0 | Parcial (registros autonómicos; sin verificar). |
| I11 | Rehabilitación del parque | Ayudas a rehabilitación y eficiencia energética. | 1 | 1 | 0 | Sí, fondos europeos (sin verificar). |
| I12 | Industrialización de la construcción | Prefabricación para bajar plazos y costes por vivienda. | 1 | 1 | 0 | No como política específica (sin verificar). |
| I13 | Agilización y seguridad jurídica urbanística (incl. liberalizar suelo no protegido) | Menos plazo e incertidumbre en planeamiento. | 2 | 2 | 0 | No como medida específica (sin verificar). |
| I14 | Seguridad jurídica y procedimientos de desalojo | Acorta desalojos y refuerza la posesión; efecto esperado sobre la oferta de alquiler por menor riesgo percibido. | 5 | 3 | 0 | Parcial: reforma de 2018 (sin verificar). |
| I15 | Fiscalidad de arrendadores e inversores inmobiliarios | Incentivos o recargos fiscales condicionados al precio o al uso. | 4 | 2 | 0 | Parcial: reducción en el IRPF del arrendador en zona tensionada (Ley 12/2023; cuantía sin verificar). |
| I16 | Alquiler turístico y de temporada | Regula esos usos para que no eludan el control de rentas ni retiren oferta residencial. | 4 | 3 | 0 | Parcial: Ley 12/2023 y registro de corta duración (sin verificar). |
| I18 | Duración y prórroga de contratos de alquiler | Alarga la estabilidad del contrato. | 3 | 3 | 0 | Sí: LAU (sin verificar). |
| I19 | Sinhogarismo y vivienda de emergencia | Provisión directa (Housing First). | 2 | 2 | 0 | Parcial (sin verificar). |
| I20 | Colaboración público-privada y nuevas modalidades | El sector público aporta suelo o garantías y el privado promueve y gestiona. | 3 | 3 | 0 | Parcial (sin verificar). |
| I21 | Limitación de compras con fin de inversión o de no residentes | Condiciona la compra con fin de inversión. | 2 | 2 | 0 | Parcial: visado por inversión (Ley 14/2013, citada en un programa). |
| I22 | Obligaciones a grandes tenedores | Impone cuota de alquiler social a propietarios grandes. | 1 | 1 | 0 | Parcial: Ley 12/2023 (sin verificar). |
| I24 | Derecho subjetivo a la vivienda | Convierte el acceso en derecho exigible; requiere oferta pública o ayudas. | 2 | 2 | 0 | No como derecho exigible. |
| I25 | Coordinación multinivel (pacto de Estado) | Acuerdo entre Estado, comunidades y entes locales. | 1 | 1 | 0 | No. |
| I26 | Gravamen sobre suelo urbanizable ocioso | Grava el suelo sin edificar para incentivar su puesta en uso. | 1 | 1 | 0 | No a nivel estatal. |
| I27 | Recargo o impuesto a la vivienda vacía | Encarece mantener vivienda desocupada. | 1 | 1 | 0 | Parcial: recargo de IBI (TRLRHL art. 72.4; sin verificar). |
| I28 | Inembargabilidad de la vivienda habitual | Impide el embargo de la vivienda familiar por deudas personales. | 1 | 1 | 0 | Sin verificar. |
| I29 | Reducción de tributos sobre la promoción y construcción de vivienda | Baja la carga fiscal del proceso edificatorio. | 1 | 1 | 0 | Parcial (sin verificar). |
| N1 | Agilización de licencias (medios técnicos municipales para informes) | Reduce el plazo y la incertidumbre del permiso. | 1 | 1 | 0 | Sin verificar; silencio positivo general, no como medida de vivienda. |

Total de medidas: 88. Docs a favor: documentos con al menos una medida «a favor/ampliar» del instrumento. En I01, los 4 «en contra» son medidas de 3 documentos.

## B. Instrumentos sin ninguna medida en el CSV (añadidos por el equipo)
| Id | Instrumento | Mecanismo | Docs |
|---|---|---|---|
| N2 | Mayor edificabilidad o densidad (zonificación permisiva) | Eleva el techo de oferta en suelo ya urbano (Saiz 2010). | 0 |
| N3 | Impuesto sobre el valor del suelo (en lugar del impuesto sobre la construcción) | Grava el suelo sin edificar, no la edificación. Es el más cercano a I26. | 0 |
| N4 | Incentivo fiscal a la promoción privada de alquiler asequible (crédito fiscal a la oferta) | Subvenciona al promotor a cambio de rentas limitadas. | 0 |

Agrupación analítica: las ayudas a la demanda con oferta rígida son la familia I06+I07+I08+I09 (no un instrumento aparte). Su riesgo común es la capitalización en precio.

## Estado
Sección «Pendiente» cerrada: recuentos recalculados desde el CSV (88 medidas, 9 documentos). Rúbrica común por instrumento en M5; la simulación P-D usa solo rangos de la literatura (`docs/v4/literatura_v4.md`).
