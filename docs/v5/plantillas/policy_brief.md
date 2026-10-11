# Vivienda en España: necesidad, datos y opciones con la misma vara (policy brief v5)

**Borja Romero, economista** (firma individual, independiente). Octubre de 2026. Cada afirmación lleva su capa: [C1] hecho con al menos dos fuentes independientes; [C2] cota con supuestos explícitos; [C4] exploratorio o de fuente única. Ningún resultado alcanza la capa de identificación causal, de modo que el texto describe asociaciones y cotas, no relaciones de causa.

## Mensajes principales

1. [C1] Entre 2021 y 2025 el número de hogares aumentó en {{dh_2125}}, con dos fuentes de hogares (ECP y EPA corregida) que coinciden en orden de magnitud.
2. [C1] En 2021-2024 los hogares crecieron más que las viviendas terminadas: el balance acumulado es de {{deficit_2124_c1:rango}} sin contar bajas del parque. [C4] Con las bajas del parque estimadas, llegaría como máximo a {{T3-H2:max}}.
3. [C1] Las viviendas terminadas fueron de {{terminadas_1924:rango}} en 2019-2024 (territorio común), con el Ministerio y el Catastro de acuerdo.
4. [C1] El precio de compra subió {{A23-P2}} en 2015-2025 según el núcleo Ministerio-Notariado-Registradores. [C1] El alquiler de los contratos vigentes subió {{A23-A2:rango}} en 2015-2024; el de los contratos nuevos crece más deprisa, pero esa brecha es [C4].
5. [C2] La proyección del INE añade {{B1-H4}} en 2026-2035: es la parte de la necesidad que no depende de supuestos propios sobre el parque.
6. [C2] Hasta 2030 el déficit nacional empeora en todos los escenarios de la rejilla (definida por el autor), incluido uno de construcción optimista; cuánto empeora es [C4].
7. [C2] La demanda latente de los jóvenes, medida por la convivencia con los padres frente a 2008, queda en {{latente_convivencia:rango}}.

## Necesidad y proyección

La necesidad de vivienda para 2026-2035 se construye por componentes. El crecimiento de hogares proyectado es [C2]. El resto (atraso, reposición, vacancia friccional, vacías movilizables, cartera en construcción) depende de supuestos y queda en [C4]:

- [C4] Necesidad total por año, suma de provincias (base): {{T3-H5b}}. Si una parte de las viviendas liberadas no llega al mercado, la necesidad efectiva sube a {{T3-H5}}. Equivale a {{T3-H9:min}}, {{T3-H9:valor}} y {{T3-H9:max}} la producción actual ({{E-T7-prod:rango}} terminadas en {{E-T7-prod:periodo}}, España con País Vasco y Navarra). El supuesto que más pesa es la fracción de vacías movilizables.
- [C4] Viviendas liberadas por envejecimiento en 2026-2035: {{T2-H1}}, de las que llegan al mercado {{T2-H6:num}} viviendas al año, sobre todo fuera de las capitales ({{E-T7-lib-resto:valor}} en el resto de municipios frente a {{E-T7-lib-capital:valor}} en las capitales). Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares.
- [C4] Bajas del parque: las identidades de stock no las miden, y las demoliciones con licencia son {{E-T7-demol-2024:rango}} en 2024.
- [C4] Atraso a absorber: déficit 2021-2025 de {{E-B1-A1:valor}} y emancipación retrasada de {{E-B1-A2:valor}}.
- [C4] Vacías movilizables en zonas con presión: {{B1-H6}}; reposición del parque: {{B1-H3}}.
- [C2] Proyección a 2030: el déficit empeora en todos los escenarios. [C4] La magnitud del aumento es {{T4-H2}}. Provincias: {{T4-H3:valor}} empeoran, {{T4-H3:min}} mejoran y {{T4-H3:max}} quedan indeterminadas. A 2035 la dirección es indeterminada [C4]: el envejecimiento libera más viviendas después de 2030.

![](B1/figuras/B1_mapa_necesidad.png)

## Instrumentos con la misma vara

La matriz D1 aplica la misma rúbrica (evidencia, signo, plazo, coste, riesgos, distribución) a cada instrumento. La política por territorio (D2) es condicional: solo indica qué tipo de instrumento es compatible con cada clase de provincia, dado el diagnóstico de esa clase.

| Instrumento (D1) | Signo sobre el acceso (condicional a la rejilla de supuestos; no es un efecto estimado en España) | Capa del signo | Dónde sería compatible (D2, condicional) |
|---|---|---|---|
| Movilización de vivienda vacía (I10, I27) | mejora, estable en la rejilla | [C2] | provincias con presión y vacías movilizables |
| Parque público o social a gran escala (I02) | mejora débil o nula si desplaza promoción privada | [C2] | provincias con presión, condicionado al desplazamiento |
| Ayudas a la demanda (I06, I07, I08) | el beneficiario mejora; según la rejilla, parte se trasladaría al precio | [C2] por grupo; traslado [C4] | donde la oferta responde; con oferta rígida el traslado es mayor |
| Regulación de precios del alquiler (I01) | no estable: depende de la respuesta de la oferta | [C4] | no determinado con estos datos |
| Alquiler turístico y de temporada (I16) | no estable en precio | [C4] | zonas con alta densidad de viviendas turísticas |
| Reducción de tributos a la promoción (I29) | parcial, literatura no verificada | [C4] | no determinado |
| Agilización urbanística y de licencias (I13, N1) | no evaluable sin identificación | [C4] | provincias donde falta vivienda y construir es rentable |

[C4] Según D1, la parte de una ayuda general que se traslada al precio, por clase territorial (A4, método A, rejilla de elasticidades de demanda): clase `1`, falta y es rentable, {{D1-H11:rango}}; clase `2`, la oferta no responde, {{D1-H12:rango}}; clase `3`, no rentable, {{D1-H13:rango}} [C4]. El extremo bajo se apoya en la literatura con oferta elástica (Eriksen y Ross, 2015) y el alto en la de oferta rígida (Gibbons y Manning, 2006; Hilber y Turner, 2014).

[C4] Según D2, la construcción adicional planificada cubriría {{D2-H11:valor}} de la necesidad de las provincias donde falta vivienda y construir es rentable, y las vacías movilizables {{E-E1-D2-covvac-1:valor}}; ambas cifras son condicionales a los supuestos de B1 (versión v5 de la necesidad, no la recalculada en v5.1; ver informe técnico, D2). <!-- check:cifra-libre (etiquetas de versión) -->

[C2] El aumento de viviendas turísticas de 2020 a 2024 equivale como máximo a {{B4-v3-vut-cantidad}}.

## Alquiler y compraventa: qué predice y qué no (v6)

[C4] Con datos públicos por provincia, municipio y distrito, los modelos de árboles predicen el alquiler de stock (SERPAVI) y el precio de compra (valor tasado) en provincias que no vieron mejor que la simple inercia: en el alquiler provincial, {{V6-M4-RMSE-alq_provincia:num}} % de error frente a {{V6-M4-PERS-alq_provincia:num}} %. Pero predecir no es explicar: ninguna variable es «relevante con seguridad», ninguna hipótesis confirmatoria pasa la corrección de Holm y, en el volumen trimestral de compraventas del último año, nada bate a la inercia. La población se asocia con los dos mercados y el PIB por habitante solo con la compra. Precio y alquiler se mueven juntos sin señales de exuberancia en ninguna de las {{E-V6-M1B-GSADF-TOT:num}} CCAA contrastadas. Para decidir, estos resultados orientan dónde mirar, no qué instrumento funciona.

## Qué falta para decidir mejor

Las solicitudes de docs/v5/solicitudes.md, por orden de prioridad:

- **S4.** Registros autonómicos de fianzas: contratos nuevos y vigentes por municipio, para separar el alquiler de stock del de contratos nuevos.
- **S1.** Catastro: inmuebles residenciales por naturaleza del titular, para saber quién posee las viviendas.
- **S2.** Sistema de Información Urbana: serie de suelo urbanizable por municipio.
- **S3.** Agencia Tributaria: rendimientos del capital inmobiliario por tramos de inmuebles arrendados.
- **S5.** Licencias de obra: presupuesto por metro cuadrado, para medir el coste de construcción en nivel.
- **S7.** INE: tabulación a medida de los Censos (hogares con varios núcleos, hacinamiento, vacías).
- **S8.** Ayuntamientos: plazo medio de concesión de licencias de obra mayor.
- **S10.** CGPJ e Interior: duración de los procedimientos de desahucio y de ocupación.
- **S6.** Registro único de arrendamientos: contratos de corta duración y de temporada.
- **S9.** Portales e Inside Airbnb: series de oferta para replicar estudios previos.

**Cómo citar estas cifras (revisión por pares simulada).**

- Dé el rango antes que el valor central. Los rangos [C1] son el mínimo y el máximo entre combinaciones de fuentes, no intervalos de confianza.
- El precio de compra se cita con las dos medidas juntas: el núcleo de registros y el índice oficial.
- Las cotas y las direcciones [C2] valen dentro de la rejilla de escenarios definida por el autor. Cite la rejilla junto con la conclusión.
- Solo es citable la versión vigente. Las cifras de versiones anteriores se sustituyeron por nuevas fuentes, muestras o correcciones, y el motivo de cada cambio consta en el historial de conclusiones y en la fe de erratas.
- [C4] no indica baja calidad: incluye estadísticas oficiales de fuente única y resultados exploratorios.

## Lo que este brief no afirma

- No atribuye la subida de precios a un factor principal: turísticos, inmigración, oferta, tipos, compradores extranjeros o empresas.
- No afirma que los topes al alquiler reduzcan precios u oferta: su resultado queda en [C4].
- No afirma que haya una burbuja.
- No afirma que la inmigración suba o baje los precios: el signo de la asociación cambia con el control de población, la medida de precio y el nivel territorial [C4].
- No afirma que ninguna variable determine el alquiler o el precio de compra: las importancias de los modelos de predicción de v6 son descriptivas.

## Neutralidad

Se evalúan afirmaciones e instrumentos, nunca a quienes los proponen. Todos los instrumentos se miden con la misma rúbrica y las cifras proceden de output/v5/cifras_clave.csv, con su periodo, fuente y capa. Cuando dos métodos discrepan se dan los dos.

**Pre-registro y versiones.** Las etiquetas git `prereg-v5` (pre-registro de las diferencias entre provincias, `docs/v5/prereg_B3.md`) y `v5.0` se crearon en el repositorio local el 10 de octubre de 2026 y se publicaron en el repositorio remoto el [fecha de publicación: pendiente]. El commit del pre-registro es anterior a cualquier resultado de ese análisis, pero una etiqueta local no es un sello de tiempo externo. Por eso, en versiones futuras el pre-registro se depositará además con sello de tiempo externo (OSF o Zenodo) antes de estimar.
