<!-- Generado por `make publicacion` desde output/documento_final/documento_final.md. No editar a mano: se regenera y un test lo comprueba. -->

# La subida del precio de la vivienda en España: qué sabemos, con qué confianza y qué falta (documento final)

Borja Romero, economista (firma individual, independiente). Documento final del proyecto, preparado para la publicación 2.0: reúne
lo que permiten decir las versiones internas V15 a V18 sobre lo publicado en las anteriores, sin análisis nuevo. Toda cifra procede
de output/v5/cifras_clave.csv con su id, su capa y, en las cifras V18, su clasificación. Lo que es juicio experto va rotulado como tal.
Generado por src/documento_final/documento_final.py (`make documento_final`); no se edita a mano.


## Resumen ejecutivo

**Pregunta.** ¿Qué factores se asocian con la subida del precio de compra y del alquiler en España, con qué magnitud y con qué confianza? El proyecto ha medido los hechos, ha estimado modelos y diseños (V8, V9, V15, V16), ha auditado la divulgación y las medidas (V17) y ha reproducido y replicado la literatura (V18). Ninguna estimación propia alcanza la clase IDENTIFICADO ni la capa C3, de modo que todo lo que sigue se lee como asociación, no como efecto. La columna «mejor estimación» es juicio experto que combina la literatura con nuestras réplicas, y se rotula así; las calibraciones con parámetros de otros países también lo son. Siglas: C1 a C4, capas del proyecto (C1 hecho, C2 cota, C4 exploratorio); NO APTA, herramienta que no supera el Monte Carlo; pp, cien veces la variación del logaritmo.

| Factor | Qué sabemos | Mejor estimación (juicio experto: literatura y réplicas propias) | Confianza (escala del Banco de España) | Qué falta |
|---|---|---|---|---|
| Población y hogares | La población creció en 3.170.654 personas entre 2015 y 2026; el saldo migratorio exterior, con ajustes estadísticos, fue mayor que todo ese aumento (saldo vegetativo negativo). En 2021-2025 se formaron 998 mil hogares (982-1.013 mil) más [C1] | Se terminan menos viviendas de las que se forman hogares: déficit 2021-2024 de 389-711 mil viviendas [C2]. Es el factor de cantidades mejor medido; su relación con el precio no tiene magnitud propia | la evidencia indica (déficit); no permite concluir (magnitud en el precio) | Tasas de jefatura por edad posteriores a 2021 |
| Inmigración (E3) | La réplica propia de González y Ortega es NO CONCLUYENTE (IC95 de −53,5 a 63,9 €/m² por punto de población). Entre países, los estudios van de −0,49 a 3,51 % de precio por 1 % de población y no se combinan | Asociación positiva a escala regional en la literatura española de 2000-2010: un solo estudio la cifra en torno a un 25,0 % del aumento de precios de aquel ciclo; con la magnitud central de varios estudios, la cuenta de la parte V asocia 6,9 de 69,0 pp en 1995-2007. Sin base para asignar a un origen más presión que a otro hogar equivalente | sugiere (asociación regional, 2000-2010); no permite concluir (magnitud en el ciclo actual) | Más variación, más grupos de origen y ventanas más largas |
| Tipos de interés (E7) | Entre 2021T4 y 2024T4 el IPV subió un 22,3 % con los tipos al alza. La réplica del BVAR de San Juan da −1,6 % a ocho trimestres por +100 pb (ASOCIACIÓN; herramienta NO APTA) | Literatura: de −5,0 a −2,0 % del precio por +100 pb a ocho trimestres. Aplicar las semielasticidades de la zona euro a la subida del tipo hipotecario de 2022-2023 equivale a un nivel de precios entre un −22,6 y un −5,9 % distinto (calibración, no estimación para España) | es compatible con | Primera etapa fuerte; Encuesta Financiera de las Familias |
| Renta, crédito y nivel de precios | Precio sobre renta bruta por hogar: 8,4 años; crédito para vivienda: 30,2 % del PIB, frente a 59,0 en 2007. Los modelos de largo plazo no rechazan la ausencia de cointegración (potencia baja) | No hay un auge del crédito como el de 2005-2007. El proyecto no replica las medidas de sobrevaloración del Banco de España (parte VI) | la evidencia indica (crédito); no permite concluir (sobrevaloración propia) | Series más largas |
| Oferta, suelo y obra nueva (E5, E6) | Se terminan 83.700 viviendas al año (2024-2025); cerrar el déficit en diez años y absorber los hogares nuevos exigiría de 204.828 a 241.262 al año. Las réplicas propias son NO ESTIMABLES | Más vivienda donde hay presión se asocia con alquileres algo menores, con una diferencia pequeña por vivienda: aplicar la elasticidad de Mense (−0,192) al cierre del déficit equivale a −0,50 % del alquiler medio (orden de magnitud). La elasticidad de la oferta no tiene magnitud preferida (de −0,202 a 1,48) | sugiere (signo); es compatible con (magnitud, un estudio de Alemania) | Catastro completo, suelo (SIU) y lluvia de AEMET |
| Vivienda turística (E1) | Garcia-López et al. (2020) lo miden con diseño en Barcelona. Réplica propia en Barcelona: ASOCIACIÓN (pretendencias rechazadas) | Peso pequeño en el agregado y de varios puntos en las secciones más expuestas: con los coeficientes de Garcia-López et al. y la densidad observada, 1,6 % del alquiler a escala nacional (de 1,0 a 2,1) y 10,6 % en la sección del percentil 99 | sugiere (local); es compatible con (magnitud nacional) | Zonas y fechas de la regulación local; anuncios de portales |
| Topes al alquiler (E2) | Tres estimaciones con el mismo registro (Incasòl) y el mismo episodio (Ley 11/2020), en log de la renta de los contratos nuevos: la nuestra, E2-R1, −0,038 (SUGESTIVO; −0,023 con trayectorias por tamaño); Jofre-Monseny et al. (2023), −0,044; Monràs y García-Montalvo (2023), −0,058, sin efectos fijos de unidad. Usan los mismos datos: no son evidencia independiente | Durante la vigencia, la renta de los contratos nuevos regulados en Cataluña fue menor que en los municipios de control, del orden de −0,044 en logaritmos (la nuestra equivale a un 3,8 % menos), con una diferencia que se reduce durante la vigencia (nota bajo la tabla). No se traslada a otros regímenes. Cantidad de contratos (E2-R1c, ASOCIACIÓN): el diseño no es creíble para ella (placebo de fecha) | la evidencia sugiere (renta); no permite concluir (cantidad) | Renta anterior, tipo de contrato y tramo (microdatos de fianzas) |
| Ayudas a la demanda (E4) | Ningún estudio español. Mediana de la traslación al alquiler en siete estudios: 46,0 % de la ayuda (de 3,6 a 78,0); la combinación formal, con los dos estudios que tienen error típico, da θ = 0,0408 euros por euro | La literatura estima que una parte de la ayuda al alquiler se traslada a la renta; cuánta depende de los estudios que se combinen: la mediana de V17 y la combinación formal difieren en un orden de magnitud por su composición (anexo B.4) | es compatible con | Microdatos de perceptores |
| Fiscalidad de la compra (ITP, E8) | No hay evaluación española con diseño. La propia (E8-R1) es ASOCIACIÓN, con signo contrario al de la literatura y dependiente de 2012-2013 | Sin magnitud para España; la literatura alemana da de −3,5 a −3,0 % del precio por +1 pp del impuesto (un solo estudio) | no permite concluir | Fechas contrastadas con el BOE; compras por tramo de precio |
| Compradores no residentes (E9) | Hicieron el 7,6 % de las compras en 2025. La réplica propia es NO ESTIMABLE (pocos choques efectivos) | Peso medido; su asociación con el precio local no está medida en España. La literatura (un estudio, Inglaterra y Gales) da de 1,4 a 2,1 % del precio por +1 pp de cuota | indica (peso); no permite concluir (precio) | Compras por nacionalidad y provincia |
| Grandes tenedores, vacías y vivienda pública (E10 a E12) | Los titulares de más de diez viviendas tienen el 4,2 % del parque (sin País Vasco ni Navarra) y, con supuestos, entre el 2,2 y el 12,2 % del alquiler habitual (E10-A1: ASOCIACIÓN). No hay calendario de recargos a las vacías ni promociones públicas por municipio | Su asociación con los precios no está medida con un diseño | no permite concluir | Catastro por tramo de titular; ordenanzas fiscales; promociones públicas |

Nota sobre los topes (frase de limitación obligatoria de E2-R1, K9):

> Entre 2020T4 y 2022T1, la renta media de los contratos nuevos registrados en el Incasòl en los 49 municipios sujetos a la Ley 11/2020 (sin Barcelona ciudad) se situó, respecto a 2019, un 3,8 % por debajo (log −0,038; IC95 −0,051 a −0,026) de la de municipios catalanes no regulados con mercado tensionado. La diferencia no es estable: es máxima en 2021T1 (−0,058), se reduce de forma gradual hasta no distinguirse de cero en 2022T1, antes de la STC 37/2022, sin cambio posterior, y baja a −0,023 (IC95 −0,045 a −0,001) cuando se permiten trayectorias trimestrales distintas según el tamaño del municipio. Con estos datos no se separa la parte asociada a la norma de un choque transitorio de la COVID-19 en los municipios grandes ni de un cambio en la composición de los contratos registrados, y la sensibilidad a tendencias diferenciales (Honest DiD con M̄ ≥ 0,5) no es evaluable con la potencia disponible. La magnitud coincide con la de Jofre-Monseny et al. (2023), que usan el mismo registro y el mismo episodio. Clase V18: SUGESTIVO; capa del proyecto C4.

**La cuenta de la subida (parte V).**

- *Con solo magnitudes propias* (la regla fijada antes de estimar), toda la variación queda sin explicar: el precio real de compra varió 69,0 pp en 1995-2007 y 14,9 pp en 2022T3-2026T2, y ningún factor tiene una estimación propia válida que restar.
- *Con magnitudes de la literatura* (juicio experto con magnitudes de la literatura, no estimación propia; supone que las magnitudes relativas entre provincias de la inmigración valen para el agregado nacional), en el valor central la fila «no explicado» es la mayor en los cinco periodos: 62,1 pp de 69,0 en 1995-2007 y 10,2 pp de 14,9 en 2022T3-2026T2. Sus rangos, de la propagación de rangos de estudios sin error típico (5,6 a 15,0 en el último periodo), no lo garantizan en 2014-2019 ni en 2022-2026. La fila de tipos de 2022T3-2026T2 recoge la bajada posterior, no la subida de 2022-2023.
- Ningún factor puede designarse como el principal, igual que en V8. Una parte grande de la variación anual es común a todo el territorio: del 60,7 al 81,1 % de la varianza en compra y del 64,2 al 70,8 % en alquiler, según la serie, en 2015-2024 o 2015-2025 (parte III).

**Qué cambia respecto a lo publicado.** Ninguna cifra publicada cambia de valor ni de capa y ningún veredicto de la auditoría de medidas y de discurso público cambia (partes VII y VIII). Se añaden nueve cifras copiadas sin recalcular de la ilustración V18 (la fila «no explicado» de la cuenta con magnitudes de la literatura; ERRATA del 2026-10-23). Lo nuevo es la combinación, rotulada como juicio experto, de la literatura con nuestras réplicas.

**Qué falta** (parte IX y docs/tareas_autor.md): microdatos de contratos de alquiler con la renta anterior y de perceptores de ayudas, el Catastro completo, compras por nacionalidad y provincia y calendarios fiscales locales; y, para una capa superior, la evaluación sellada diferida, no antes de 2027.


## Executive summary (English)

Which factors are associated with the rise in Spanish house prices and rents, by how much, and with what confidence? The project has measured the facts, estimated models and pre-registered designs, audited public claims and policies, and reproduced and replicated the published literature. No own estimate reaches the IDENTIFIED class or project layer C3, so everything below reads as association, not as an effect, and the "best estimate" column of the table above is expert judgement that combines the literature with our replications, and is labelled as such.

- Demography: net migration exceeded the whole population increase (the natural balance was negative), and fewer dwellings were completed than households formed in 2021-2024 (a bound under explicit assumptions). The price effect has no own magnitude.
- Rent caps (Catalonia, Law 11/2020): three estimates with the same register agree that regulated new-contract rents were lower than in control municipalities while the law was in force; the three use the same data and are not independent evidence. Ours is SUGGESTIVE; the gap shrinks over time and cannot be separated from a COVID-19 shock or a change in contract composition (figures, with the mandatory limitation sentence, in the Spanish summary and Annex B.2).
- Interest rates, tourism, supply, demand subsidies, transfer tax, non-resident buyers, large landlords, vacant and public housing: magnitudes come only from the literature, or there is none for Spain.
- Accounting for the rise: with own magnitudes only, the whole change stays unexplained; with literature magnitudes (expert judgement, not an own estimate; it assumes that cross-provincial magnitudes hold for the national aggregate), the unexplained part is the largest in every period at the central value, though its ranges do not guarantee it in 2014-2019 and 2022-2026. No single factor can be designated as the main one.

Nothing published changes its value or layer. JEL codes: R21, R31, R38. Keywords: house prices, rents, Spain, replication, expert judgement.


## Cómo leer este documento

**Tres etiquetas por cifra.** Cada cifra lleva su capa del proyecto; las de V18 llevan además su clase; y los juicios del autor llevan su grado de confianza.

| Etiqueta | Valores | Qué dice |
|---|---|---|
| Capa del proyecto | C1 hecho (dos fuentes independientes coinciden); C2 cota con supuestos explícitos; C3 efecto con un diseño que supera las pruebas; C3s descomposición con restricciones de signo; C4 exploratorio | Cómo se sabe. Ningún resultado del proyecto alcanza C3. La capa nunca se promueve |
| Clase V18 | IDENTIFICADO, SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE, NO ESTIMABLE (y, sin clase propia, literatura, diagnóstico o variante, robustez a posteriori) | Qué permite el diseño de una estimación propia. Ninguna es IDENTIFICADO; toda cifra V18 es de capa C4 |
| Confianza (escala del Banco de España) | la evidencia indica; la evidencia sugiere; es compatible con; no permite concluir | Juicio experto del autor sobre el conjunto de la evidencia (literatura y datos propios), como en V17 |

**Juicio experto.** Lo es la columna «mejor estimación» del resumen ejecutivo, la confianza de cada factor y la contabilidad con magnitudes de la literatura de la parte V. Se rotula así cada vez y no es una estimación propia. La regla del proyecto no cambia: sin un diseño que supere las pruebas no hay lenguaje causal, también en el juicio experto.

**Cifras.** Toda cifra sale de output/v5/cifras_clave.csv con su id (en publicacion/cifras_clave.csv, con fuente, periodo, fecha del dato y capa). El generador redondea al presentar; los valores completos están en la tabla. Los puntos porcentuales de la contabilidad (pp) son cien veces la variación del logaritmo del precio o del alquiler real.

**Lo que no hace.** No estima nada nuevo: integra lo publicado en las versiones internas vigentes (déficit y necesidad: v7.1 con v7.2; por qué ha subido: V8; qué causa qué: V9; base y atlas: V10; demografía y titularidad: V12) con lo que añaden V15 a V18. No evalúa partidos ni personas: evalúa afirmaciones e instrumentos.


## Parte I. Diagnóstico: qué ha pasado

**Precios y alquileres.**

- El precio de compra subió un 47 % (44-56) entre 2015 y 2025 [C1: Ministerio, Notariado y Registradores coinciden en la tolerancia declarada].
- El alquiler de los contratos ya firmados subió un 11-23 % entre 2015 y 2024 [C1]. Los contratos nuevos subieron más: en la Comunitat Valenciana, un 29 % (26-31) entre 2021 y 2024 [C1]; en Cataluña, 16,9 % (16,6-17,2) [C1].
- Desde mediados de 2022 el precio real de compra varió 18 pp, y el alquiler real del conjunto de contratos, −1,8 pp [C4]. La subida reciente es común a casi todas las comunidades: la media de las comunidades recoge un 93 % (87-95) de lo que varían [C4].
- Quienes alquilan a precio de mercado destinan más del 40 % de su renta a la vivienda en un 27 % (24-29) de los casos (Encuesta de Condiciones de Vida, 2025) [C4]; el 40 % es el umbral de sobrecarga.

**Hogares y viviendas.**

- Entre 2021 y 2025 se formaron unos 998 mil hogares (982-1.013 mil) más [C1], y se terminaron 72,3-94,4 mil viviendas/año [C1, territorio común, 2019-2024]. Con País Vasco y Navarra, 78,8-101 mil viviendas/año según el año [C4, una sola estadística].
- Se terminan menos viviendas de las que se forman hogares: entre 2021 y 2024 faltaron 389-711 mil viviendas [C2]. Es una cota con supuestos explícitos; si se descartan dos de las correcciones de la EPA, 596-711 mil viviendas.
- El INE proyecta 1,72 millones de hogares (1,31-1,77 millones) más entre 2026 y 2035 [C2]. La necesidad anual de vivienda en 2026-2035 es de 210 mil viviendas/año (99,4-292 mil) [C4], sin restar las viviendas que quedan libres por envejecimiento, que la proyección del INE ya descuenta.
- Hasta 2030 el saldo entre hogares y viviendas empeora en todos los escenarios definidos [C2]; cuánto, no se sabe: 87,2-947 mil viviendas [C4].
- Son propietarios de su vivienda principal 75 % de hogares (72-76) de los hogares [C1].

**Lo que el diagnóstico no dice.** Que un solo factor sea el principal de la subida: en V8 ningún factor destaca como el principal en ninguno de los diez casos estudiados (como mucho coinciden 2 métodos de cuatro, y la regla exige tres), y de la subida de la compra desde 2022, 9,5 pp (−7,8 a 16) de media no se asocia con ningún factor del modelo [C3s: vale solo bajo las restricciones del modelo]. Tampoco que haya o no haya una burbuja (parte VI).

---

*Atribución (Open Database License).* Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. Las cifras construidas con esos datos se publican bajo la misma licencia.


## Parte II. Demografía

Análisis a posteriori de V17, capa C4, contable y descriptivo. Los datos locales no contienen los motivos de llegada ni permiten construir un contrafactual, de modo que esta sección no estima efectos.

**Población.** Entre el 1 de enero de 2015 y el 1 de enero de 2026, la población residente creció en 3.170.654 personas. El saldo vegetativo acumulado fue de −896.778 personas (negativo desde 2017; el dato de 2025 es provisional). El resto, 4.067.432 personas, es saldo migratorio exterior neto más ajustes estadísticos, y equivale al 128,3 % del crecimiento. El residuo mezcla el saldo exterior oficial con ajustes (rebase censal de 2021, revisiones, bajas por caducidad). En 2015-2024, el saldo exterior oficial suma 3.757.591 personas, y el residuo menos ese saldo es de −284.056 personas.

**Por lugar de nacimiento.** La población nacida en el extranjero varió en 4.120.690 personas y la nacida en España, en −975.687. Los nacidos en el extranjero equivalen al 130,0 % del crecimiento, más que la totalidad porque la población nacida en España disminuye. El saldo vegetativo de nacionalidad española acumula −1.389.513 personas y el de nacionalidad extranjera, 604.316 (por nacionalidad de la madre y del fallecido, que aproxima el lugar de nacimiento).

**Hogares.** Entre 2021 y 2026 el número de hogares aumentó en 1.222.836 según la Encuesta Continua de Población (la cifra de la parte I, de 2021-2025, combina dos fuentes y es de capa C1). Descomposición contable del cambio (Shapley anual, V16): 858.274 hogares corresponden al tamaño de la población, 473.045 a la estructura por edad (envejecimiento) y −11.510 a la jefatura (residuo; tamaño medio del hogar). Si los nacidos en el extranjero forman hogares como el resto, entre 724.785 y 858.274 hogares del componente de población corresponden a su crecimiento (valor central 791.530). Es una cota de contabilidad, no un efecto.

**Tenencia (Censo 2021, muestra del hogar con persona de mayor edad de referencia).** Viven en alquiler el 36,8 % de los hogares cuya persona de mayor edad nació en el extranjero y el 11,5 % de los de persona nacida en España. En propiedad viven el 50,6 % y el 80,5 %, respectivamente.

**Relación con E3 y E9.** La contabilidad de población no es una estimación del efecto de la inmigración sobre los precios, que es la pregunta de E3. Un aumento de población se asocia con más hogares sea cual sea su origen, y no hay evidencia de que un hogar inmigrante presione más que otro equivalente. E3-R1 es NO CONCLUYENTE y la magnitud preferida de E3 no existe (anexo B.3). Por eso V17 mantuvo la calificación «engañosa» para la afirmación que atribuye la subida a la inmigración: ni la contabilidad ni la literatura permiten fijar una magnitud.

**Límites.** La población del Padrón continuo es provisional y se revisa cada trimestre; el dato de 2025 mezcla ediciones. El saldo vegetativo aproxima el lugar de nacimiento por la nacionalidad. No hay tasa de jefatura por edad posterior a 2021. Las cifras de V5 sobre el conjunto de provincias se citan solo como publicadas.


## Parte III. ¿Problema general o local?

Análisis a posteriori de V17, capa C4, contable y descriptivo. La pregunta es qué parte de la varianza de la variación anual de los precios y los alquileres corresponde a un componente común a todos los territorios (el efecto año) y qué parte es local (provincia por año). Las cuotas llevan intervalo de confianza al 95 % por bootstrap de provincias y se comparan con una referencia de azar (permutación temporal dentro de cada provincia).

| Serie | Periodo | Cuota del componente común (%) | IC95 (%) |
|---|---|---|---|
| Índice de precios de vivienda (IPV) por comunidad, comunidades no selladas | 2015-2025 | 81,1 | 70,3 a 93,9 |
| Valor tasado del MIVAU por provincia | 2015-2025 | 60,7 | 55,2 a 67,5 |
| Índice de precios de vivienda del INE por provincia (IPVA) | 2015-2024 | 76,9 | 70,4 a 84,6 |
| IPC de alquiler del INE por provincia | 2015-2025 | 64,2 | 59,3 a 71,4 |
| Alquiler mediano en €/m² de SERPAVI por provincia | 2015-2024 | 70,8 | 64,8 a 79,1 |

**Lectura.**

- En compra, el componente común es mayoritario en el conjunto de 2015-2025 en las tres series. Por subperiodos, en el valor tasado y en el IPV por comunidad el componente local pesa más antes de 2020 y el común domina desde 2020; no ocurre así con el IPVA. Cuota común (%, IC95 bootstrap): valor tasado 3,8 (1,5 a 12,4) en 2015-2019 y 66,2 (60,5 a 73,0) en 2020-2025; IPV por comunidad 19,3 (7,5 a 65,1) y 91,8 (89,4 a 96,5); IPVA 74,0 (68,3 a 81,5) en 2015-2019 y 67,8 (58,4 a 80,1) en 2020-2024 (output/v17/d3/varianza_comun_local.csv).
- En alquiler, el resultado es mixto y menos seguro: las cuotas del componente común son menores y los intervalos más anchos, y en SERPAVI el componente común baja desde 2020 (de 75,7 % en 2015-2019 a 44,9 % en 2020-2024).
- En todas las series queda una parte local (provincia por año), de modo que la respuesta no es una u otra. Depende de la serie y del método.
- El déficit está concentrado (41 provincias no selladas). Provincias que suman la mitad del déficit positivo 2021-2025 (sin sellada v6): 5. Provincias que suman el 80 % del déficit positivo 2021-2025 (sin sellada v6): 14.
- Movimientos dentro de la provincia: el saldo acumulado de 2015 a 2024 de las capitales con el resto de su provincia es de −199.029 personas (8 capitales de provincias no selladas); negativo significa que la capital cede residentes a su corona. Solo cubre movimientos entre municipios de una misma provincia y no mide el padrón de la corona.

**Relación con V18.** Los diseños de panel con efectos de periodo (E1, E2, E3, E5, E8, E9, E12) solo recogen la parte local, la que varía entre territorios en el mismo periodo. Por eso las diferencias asociadas a cada factor en la contabilidad se rotulan «relativas entre provincias, sin el componente común», y la variación común queda fuera de lo que esos diseños pueden asociar a un factor. Es una de las razones de que la fila «no explicado» sea grande.

**Límites.** No hay esfuerzo provincial propio en los datos locales. La cuota depende de la serie, del número de periodos y de los territorios no sellados. Nada de esta sección es una estimación de un efecto.


## Parte IV. Factibilidad de construir

Análisis a posteriori de V17, capa C4, contable y con supuestos explícitos; no es una predicción.

**Producción.** Se terminaron 83.700 viviendas al año de media en 2024-2025, frente a 568.684 en 2005-2007. Para cerrar el déficit inicial y absorber los hogares nuevos y la reposición hacen falta 293.623 viviendas al año en cinco años (rango por déficit inicial: 257.188 a 330.057) o 223.045 en diez años (204.828 a 241.262). Supuestos: producción necesaria igual al déficit entre los años más los hogares nuevos de la proyección del INE y la reposición, sin restar las viviendas liberadas por envejecimiento. El déficit de 2021-2025 equivale al 2,7 % del parque de viviendas familiares.

**Cuántas veces la producción actual.** El cociente entre la producción necesaria y la actual no es una cifra única: depende de los supuestos. Con el déficit central, V17 lo calcula con varias combinaciones de supuestos (reposición fija o proporcional al parque, absorción de una parte del déficit por viviendas vacías y secundarias, y dos cifras de producción actual) y obtiene de 2,8 a 4,4 veces a cinco años y de 2,2 a 3,5 veces a diez años (output/v17/auditoria/filas/mas_oferta.md). Ese rango no se obtiene dividiendo las cifras del párrafo anterior, que usan un solo juego de supuestos. La cifra publicada en la versión pública (T3-H9) es otra: 2,7 veces (de 1,4 a 3,8), porque usa otra producción (media de 2019-2024, con País Vasco y Navarra) y la necesidad anual con la sensibilidad X. Las tres cifras dicen lo mismo en orden de magnitud: la necesidad es varias veces la producción actual. Ninguna sustituye a las otras.

**Capacidad.** Los ocupados en construcción eran 1.498 miles en 2025, frente a 2.703 miles en 2007. Las viviendas terminadas por ocupado fueron 0,05 en 2025 y 0,21 en 2007. El índice real del coste de la mano de obra en construcción en 2025 es de 1,0 respecto a 2007. Con supuestos de productividad (juicio experto), pasar a la producción necesaria a cinco años exigiría entre 208,0 y 1.615 miles de ocupados adicionales (central 648,6), y a diez años, entre 142,1 y 1.033 miles.

**Suelo.** No hay Sistema de Información Urbana por provincia en los datos locales. El potencial que cita el Banco de España para las seis grandes áreas urbanas es de 1.100.000 viviendas (cifra de documento). En el área de Barcelona, el potencial equivale a 0,39 de la necesidad provincial a diez años (rango 0,29 a 0,51): el suelo previsto equivale a menos de la necesidad, y ahí la evidencia indica una restricción de suelo. En el resto de las grandes ciudades no se puede saber con los datos disponibles. Los plazos de licencias y de transporte a coronas no tienen datos oficiales locales.

**Qué aporta V18.** Los factores de oferta no tienen estimación propia: E5 (elasticidad de la oferta con Bartik) y E6 (obra nueva y alquileres cercanos) son NO ESTIMABLES (anexo B). La única magnitud de V18 que enlaza con esta sección es la de E6, que procede de un estudio de la literatura (Mense 2025, VERIFICADA): −0,192 de elasticidad del alquiler respecto a la oferta nueva. Con ella, la ilustración de V17 al cerrar el déficit da −0,50 % del alquiler medio (rango −0,63 a −0,37), que es un orden de magnitud y no una estimación para España. El veredicto de V17 sobre más oferta no cambia.


## Parte V. Determinantes: qué se asocia con la subida y cuánto

### V.1 Tabla de impactos (V18)

Para cada factor, la magnitud preferida que fijan las reglas de V18 (metaanálisis con las estimaciones en una misma unidad, fijado antes de combinar), su intervalo y la clase de la estimación propia designada. No es juicio experto: es la aplicación de la regla. Toda cifra es de capa C4.

| Factor | Magnitud preferida | Intervalo | Clasificación | Confianza | Limitación principal |
|---|---|---|---|---|---|
| Vivienda turística (E1) | 0,038 | [0,0145; 0,0615] (IC95 del único estudio) | NO ESTIMABLE | baja | un solo estudio en la unidad; estimación propia: no entra (NO ESTIMABLE) |
| Topes al alquiler (E2) | sin magnitud preferida | [−0,122; 0,0029] (rango) | SUGESTIVO | baja | la decisión cambia con la prior: rango sin magnitud preferida; estimación propia: SUGESTIVO |
| Inmigración (E3) | sin magnitud preferida | [−0,49; 3,51] (rango) | NO ESTIMABLE | baja | heterogeneidad alta entre estudios: rango sin magnitud preferida; estimación propia: no entra (NO ESTIMABLE) |
| Ayudas a la demanda (E4) | 0,0408 | [−0,0138; 0,0953] (intervalo del efecto fijo con dos estudios; no es un IC95 fiable) | NO ESTIMABLE | baja | pocos estudios con error típico; heterogeneidad declarada; estimación propia: no entra (NO ESTIMABLE) |
| Oferta y suelo (E5) | sin magnitud preferida | [−0,202; 1,48] (rango) | NO ESTIMABLE | baja | heterogeneidad alta entre estudios: rango sin magnitud preferida; estimación propia: no entra (NO ESTIMABLE) |
| Obra nueva (E6) | −0,192 | [−0,319; −0,0646] (IC95 del único estudio) | NO ESTIMABLE | baja | un solo estudio en la unidad; estimación propia: no entra (NO ESTIMABLE) |
| Tipos de interés (E7) | sin magnitud preferida | [−5; −2] (rango) | NO ESTIMABLE | muy baja | sin error típico en la literatura: rango de 2 estudios, sin intervalo estadístico; estimación propia: no entra (NO ESTIMABLE) |
| Fiscalidad de la compra (ITP) (E8) | sin magnitud preferida | [−3,5; −3] (rango) | ASOCIACIÓN | muy baja | sin error típico en la literatura: rango de un solo estudio, sin intervalo estadístico; estimación propia: no entra (ASOCIACIÓN) |
| Compradores no residentes (E9) | sin magnitud preferida | [1,4; 2,1] (rango) | NO ESTIMABLE | muy baja | sin error típico en la literatura: rango de un solo estudio, sin intervalo estadístico; estimación propia: no entra (NO ESTIMABLE) |

Unidades: E1: Δln del alquiler por +1 pp de viviendas turísticas sobre el parque; E2: diferencia en ln de la renta de los contratos regulados; E3: % de precio por +1 % de población por entrada de inmigrantes; E4: θ: euros de alquiler por euro de ayuda; E5: elasticidad precio de la oferta de unidades; E6: elasticidad del alquiler respecto a la oferta nueva (% por 1 %); E7: % del precio por +100 pb del tipo hipotecario, a 8 trimestres; E8: % de precio por +1 pp del ITP, a 12 meses; E9: % de precio por +1 pp de cuota de compras de no residentes. Cifras: ids V18-B5-E1 a V18-B5-E9 de cifras_clave (capa C4). La clasificación es la de la estimación propia designada del factor; la magnitud preferida puede venir solo de la literatura (sección 4). Confianza: media solo con magnitud preferida de tres o más estudios; muy baja sin error típico en la literatura; baja en el resto.

### V.2 De la regla al juicio experto, factor por factor

La tabla anterior aplica una regla estricta: solo combina estudios con error típico en la misma unidad y solo admite estimaciones propias con diseño válido. El resumen ejecutivo da, además, una mejor estimación por factor que es juicio experto: pondera la literatura por su diseño y su cercanía a España y la contrasta con nuestras réplicas. La diferencia entre las dos se explica aquí. El detalle de cada réplica (original, reproducción, réplica, ampliación y pruebas) está en el anexo B.

- **Vivienda turística (E1).** La réplica propia en Barcelona (E1-R3) da 0,00443 en log del alquiler por punto de densidad, ASOCIACIÓN: el contraste de pretendencias rechaza. El caso de la Sagrada Família (E1-R4) es NO CONCLUYENTE. La magnitud preferida procede de un solo estudio con ficha NO VERIFICADA. Juicio experto: el peso a escala nacional es pequeño y el local puede ser de varios puntos en las secciones más expuestas, como miden Garcia-López et al. (2020) con diseño en Barcelona; la evidencia sugiere lo local y es compatible con la magnitud nacional, que es una calibración.
- **Topes al alquiler (E2).** La regla no da magnitud preferida: con estudios de Francia y Alemania la heterogeneidad es alta y la decisión cambia con la prior (rango de −0,122 a 0,0029; con la otra estrategia de extracción de Hahn et al., −0,0487, como sensibilidad). El juicio experto se limita al episodio catalán, donde hay tres estimaciones con el mismo registro de contratos del Incasòl: E2-R1 (−0,038, SUGESTIVO), Jofre-Monseny et al. (2023, −0,044) y Monràs y García-Montalvo (2023, −0,058, sin efectos fijos de unidad). Las tres tienen el mismo signo y una magnitud parecida; la nuestra es la menor en valor absoluto, con otro grupo de control y sin Barcelona ciudad. Las tres usan los mismos datos y no son evidencia independiente; con trayectorias por tamaño del municipio, la nuestra baja a −0,023. Mejor estimación (juicio experto): durante la vigencia, la renta de los contratos nuevos regulados se situó del orden de −0,044 en logaritmos por debajo de la de los municipios de control, con una diferencia que se reduce durante la vigencia y que no se separa de la COVID-19 ni de la composición (frase de limitación en el resumen ejecutivo). Sobre la cantidad de contratos, E2-R1c es ASOCIACIÓN: el placebo de fecha indica que el diseño no es creíble para ese resultado, y la literatura está dividida. La evidencia sugiere; no se traslada a las zonas tensionadas de 2024, que son otro régimen.
- **Inmigración (E3).** La réplica de González y Ortega (E3-R1) es NO CONCLUYENTE: su intervalo incluye el cero y también la magnitud del original. Entre países los estudios van de −0,49 a 3,51 % de precio por 1 % de población y no se combinan. Juicio experto: los estudios españoles con diseño (2000-2010) son positivos; uno de ellos cifra la asociación en torno a un 25,0 % del aumento de precios de aquel ciclo. No hay base para trasladar esa fracción a 2014-2026 ni para asignar a un origen más presión que a otro hogar equivalente. La evidencia sugiere una asociación positiva a escala regional y no permite concluir sobre su magnitud en el ciclo actual.
- **Ayudas a la demanda (E4).** No hay estimación propia (no hay microdatos de perceptores). La regla da θ = 0,0408 con dos estudios, dominada por el finlandés; V17 daba una mediana de 46,0 % con un valor por estudio. Las dos cifras difieren en un orden de magnitud por la composición de los estudios (anexo B.4). Juicio experto: la literatura estima que una parte de la ayuda se traslada a la renta, sin una fracción preferida; es compatible con, y la literatura no es española.
- **Oferta, suelo y obra nueva (E5, E6).** Las réplicas propias son NO ESTIMABLES (primera etapa débil en E5; potencia insuficiente en E6). La elasticidad de la oferta no tiene magnitud preferida; la de la obra nueva procede de un estudio de Alemania (−0,192). Juicio experto: más vivienda donde hay presión se asocia con alquileres algo menores, con una diferencia pequeña por vivienda; la evidencia sugiere el signo y es compatible con la magnitud de un estudio de Alemania.
- **Tipos de interés (E7).** La proyección local con instrumento y el SVAR con proxy son NO ESTIMABLES (primera etapa débil); el BVAR recursivo da −1,6 % a ocho trimestres por +100 pb (ASOCIACIÓN, herramienta NO APTA). La literatura da de −5,0 a −2,0 % sin error típico. Juicio experto: aplicar las magnitudes de la literatura a la subida de 2022-2023 equivale a un nivel de precios algo menor, mientras el precio siguió subiendo; es compatible con.
- **Fiscalidad de la compra (E8).** E8-R1 da 0,0146 en log del valor tasado por punto del tipo, ASOCIACIÓN: signo contrario al de la literatura y dependiente de 2012-2013. Sin magnitud para España; no permite concluir.
- **Compradores no residentes (E9).** NO ESTIMABLE por pocos choques efectivos. La literatura es de un solo estudio de otro país. La evidencia indica su peso en las compras y no permite concluir sobre su asociación con el precio en España.
- **Grandes tenedores, vacías y vivienda pública (E10 a E12).** E10-A1 es una asociación transversal (ASOCIACIÓN), que cambia con la definición del regresor; E11 es NO ESTIMABLE; E12-A2 (ASOCIACIÓN) mide vivienda protegida, no pública. No permite concluir.
- **Renta y modelos de conjunto (F1 a F4).** Ningún contraste de cointegración rechaza su ausencia tras Holm; la respuesta de corto plazo del precio a la renta real (F1-R1) es 0,126, ASOCIACIÓN; y F1 no predice mejor que el AR(4) fuera de muestra. No se publican elasticidades de largo plazo.

### V.3 Comparación con V8 y con el Banco de España

- **V8** (descomposición histórica del SVAR, de capa C3s, con bandas del 68 %) no designó ningún factor como el más relevante en ninguno de los diez casos. Comparación con V18 (recuentos de capa C4): con cifra en V8 y en V18 (E3, E7 y E9) hay 12 comparaciones; el signo coincide en 7 y las bandas se solapan en 10. Como las bandas de V8 incluyen el cero casi siempre, el solape es una prueba débil.
- **Banco de España.** La sobrevaloración del precio es un indicador de nivel frente a fundamentales que la contabilidad con elasticidades no replica (parte VI). San Juan (2023) es uno de los dos estudios del rango de E7, de modo que su cifra está en el rango por construcción. El diferencial entre hogares y viviendas que estima el Banco de España es contabilidad de cantidades, como el déficit de la parte I.


### V.4 La cuenta de la subida: dos versiones, lado a lado

La cuenta multiplica la magnitud de cada factor por la variación observada del factor en el periodo y deja una fila «no explicado». Es contabilidad con elasticidades, no una descomposición estructural ni una atribución: no incluye interacciones ni efectos de equilibrio general, los factores no son independientes entre sí y la variación observada se toma sin error. Las cifras están en puntos porcentuales (pp: cien veces la variación del logaritmo del precio real de compra, deflactado con el deflactor del PIB) y son de capa C4.

**Versión 1. Solo magnitudes propias (regla fijada antes de estimar).** Solo entra un factor con una estimación propia válida dentro de su magnitud preferida. Ninguno la cumple: E2, el único con una estimación SUGESTIVO, no tiene magnitud preferida, y las demás designadas son NO ESTIMABLES o ASOCIACIÓN. Por construcción, toda la variación observada queda sin explicar. No significa que los factores no importen: significa que con datos españoles y un diseño que supere las pruebas no se ha podido medir cuánto.

**Versión 2. Juicio experto con magnitudes de la literatura, no estimación propia.** Usa la magnitud de la literatura de cada factor que tiene una variación nacional medible: E3 (inmigración), E7 (tipos de interés) y E9 (compradores no residentes) como alternativa de E3, porque los dos se construyen con las mismas cuotas por origen y no se suman. Como E3, E7 y E9 no tienen magnitud preferida en B5, la magnitud de cada uno se extrae de manera uniforme del rango de los estudios (la columna «magnitud_centro» de contabilidad_ilustracion.csv da su centro). Supone que la magnitud de E3 y E9, estimada en la literatura entre provincias, vale también para el agregado nacional, lo que esos diseños no estiman; la regla de V18 no lo admite (A.6) y el árbitro de V18 retiró por eso estas filas de cifras_clave (K14, N4); el documento final las recupera rotuladas como juicio experto (K15). El rango que se da es el del 90 % de esa propagación: no es un intervalo estadístico, porque los estudios no tienen error típico en la unidad, y puede ser artificialmente estrecho.

| Periodo | Variación observada (versión 1: todo sin explicar) | E3 inmigración | E7 tipos de interés | Versión 2: no explicado (rango del 90 %) | Con E9 en lugar de E3: E9 | Con E9: no explicado (rango del 90 %) |
|---|---|---|---|---|---|---|
| 1995T1-2007T4 | 69,0 | 6,9 | fuera del horizonte | 62,1 (44,7 a 80,3) | — | — |
| 2008T1-2013T4 | −36,6 | −0,75 | 1,1 | −37,0 (−39,1 a −35,1) | 11,2 | −49,0 (−51,1 a −46,9) |
| 2014T1-2019T4 | 6,3 | 1,0 | 0,35 | 5,0 (2,4 a 7,7) | −4,2 | 10,2 (9,5 a 11,0) |
| 2020T1-2022T2 | −1,0 | 0,48 | 0,33 | −1,9 (−3,1 a −0,59) | fuera del soporte | −1,4 (−1,5 a −1,2) |
| 2022T3-2026T2 | 14,9 | 1,8 | 2,9 | 10,2 (5,6 a 15,0) | −3,3 | 15,3 (14,0 a 16,7) |

Clasificación de todas las filas: NO ESTIMABLE (magnitudes de la literatura, sin estimación propia válida). Filas sin cifra: E7 en 1995T1-2007T4 (la subida del tipo queda fuera del horizonte de ocho trimestres que estima la literatura) y E9 en 2020T1-2022T2 (fuera del soporte de la variación de la muestra de estimación). E1, E4, E5 y E6 no tienen fila nacional: sus unidades no son comparables con la variación disponible o no hay variación medida. El detalle por comunidad y provincia, en las dos versiones, está en output/v18/f5/contabilidad.csv y contabilidad_ilustracion.csv (y en tablas_v18.xlsx).

**Lectura.**

- En el valor central, la fila «no explicado» de la versión 2 es la mayor en los cinco periodos; en 2014T1-2019T4 y 2022T3-2026T2 su rango no lo garantiza, y en 2020T1-2022T2 supera en valor absoluto a la propia variación observada. En 1995T1-2007T4, la parte asociada a la inmigración es de 6,9 pp de 69,0, con un rango amplio. Es una fracción menor que la que el estudio de González y Ortega asocia con la inmigración en 2000-2010 (en torno a un 25,0 %), porque su elasticidad implícita (1,3) está por encima de la magnitud central del rango de estudios, y porque la cuenta aplica al agregado una magnitud estimada entre provincias.
- Con E9 en lugar de E3, el «no explicado» es mayor en valor absoluto que la propia variación observada en los cuatro periodos con cifra: en los tres en que E9 tiene fila, su signo es opuesto al de la variación observada, y la magnitud procede de un solo estudio de otro país. Es una señal de que la versión 2 depende de magnitudes poco seguras, no una medida de lo que pesan los compradores no residentes.
- En 2022T3-2026T2 la fila de E7 es positiva: la literatura asocia la bajada de tipos de los últimos ocho trimestres con precios mayores; la subida de 2022-2023 queda fuera del horizonte de ocho trimestres de ese periodo.
- Las dos versiones dicen lo mismo en lo esencial: ningún factor puede designarse como el principal, en ningún periodo, con la evidencia disponible; la versión 2 añade que, aun aceptando magnitudes de otros países, la mayor parte de la variación queda sin asociar a un factor medido. La parte común a todas las provincias (parte III), que los diseños de panel no separan de los efectos de periodo, es una de las razones.

**Cataluña y Barcelona (ilustración local, no atribución).** E2 no tiene magnitud preferida, de modo que no hay fila de E2 en la cuenta; con la estimación propia E2-R1 sola, durante la vigencia (2020T4-2022T1) la diferencia asociada en el nivel medio de la renta de los contratos nuevos en Cataluña (sin Barcelona ciudad), ponderada por la cuota de contratos regulados, es de −2,7 pp (intervalo del 90 % de −3,5 a −2,0; clase NO ESTIMABLE: la de E2-R1 no se traslada), frente a una variación observada de esos contratos de −2,8 pp; las dos cifras no se restan, y la primera requiere la frase de limitación de E2-R1. En Barcelona ciudad, con la magnitud de E1 (definida por anuncios de Airbnb) y el registro de viviendas turísticas: −0,08 pp en 2020T1-2022T2 y 0,50 pp en 2022T3-2026T2, frente a una variación observada del alquiler de los contratos nuevos de −6,1 y −2,1 pp.

**Por qué difiere de la parte I.** Desde 2022T3, la parte I da la variación del precio real de V8, deflactado con el IPC; la cuenta usa el deflactor del PIB (A.6), y por eso sus variaciones observadas no coinciden.

**Limitaciones de la cuenta.** Magnitudes de la literatura, muchas con ficha NO VERIFICADA o leídas solo por el resumen, aplicadas a España; E7 y E9 sin error típico, y E9 con el rango de un solo estudio; magnitudes relativas entre provincias (E3, E9) aplicadas a variaciones nacionales; efectos de nivel permanentes para E3 y E9, que en la literatura son promedios del periodo o a doce meses; variación observada sin error; deflactor del PIB en lugar del IPC. Las provincias selladas de v6 y los municipios de V15 y V16 se excluyen de las series provinciales; la cifra nacional es la del conjunto de España.


## Parte VI. Sobrevaloración: ¿está el precio por encima de sus fundamentales?

**Qué miden los indicadores convencionales** (Banco de España; último dato frente a su media histórica y a su máximo anual; capa C4, a posteriori de V17).

| Indicador | Último dato | Media histórica | Máximo anual |
|---|---|---|---|
| Precio de la vivienda sobre renta bruta por hogar (años) | 8,4 | 6,0 | 9,4 |
| Esfuerzo teórico anual sin deducciones (% de la renta) | 38,0 | 39,7 | 71,4 |
| Rentabilidad bruta del alquiler (%) | 2,8 | 4,7 | 8,0 |
| Crédito a hogares para vivienda (% del PIB) | 30,2 | 42,4 | 63,2 |
| Crédito para vivienda, tasa interanual (%) | 3,7 | 7,7 | 24,2 |
| Préstamos con relación préstamo-valor mayor que 80 % (% del total) | 9,6 | 12,5 | 17,0 |
| Dudosidad del crédito para vivienda (%) | 1,4 | 2,7 | 6,1 |

**Lectura.** El nivel del precio frente a la renta está por encima de su media histórica y por debajo del máximo de 2007 (−10,7 % frente a 2007), y la rentabilidad del alquiler está por debajo de su media; el esfuerzo teórico, que incorpora los tipos, está algo por debajo de la suya. En cambio, el crédito no muestra un auge como el de 2005-2007: su saldo sobre el PIB está −28,8 puntos por debajo del de 2007, su tasa de crecimiento y los préstamos con relación préstamo-valor alta están por debajo de su media, y la dudosidad es baja. Una parte grande de las compras no usa hipoteca (al menos un 29,9 % en 2025). El Banco de España presenta un rango de indicadores de desequilibrio del precio con métodos distintos y una incertidumbre alta entre ellos; el proyecto no replica esas medidas de nivel y no las sustituye.

**Qué añade el proyecto.**

- *Exuberancia estadística* (v7.2, contraste GSADF). Con ajuste por comparaciones múltiples, 0 de cuatro cocientes nacionales son exuberantes (los denominadores son los del diseño de output/v7_2/gsadf/ficha_burbuja.md); los niveles de precio lo son en 0 de dos series y las comunidades en 0 de 34. La potencia del contraste frente a una alternativa explosiva simulada es baja (0,06 de rechazos), de modo que su ausencia no descarta una burbuja, igual que una exuberancia estadística no la demostraría.
- *Relación de largo plazo* (V7.2, V8-M4 y V18, familia F). Ningún contraste de cointegración entre precio, alquiler, renta, crédito y oferta rechaza su ausencia tras la corrección de Holm. Por la regla del proyecto no se publican elasticidades de largo plazo ni una sobrevaloración propia (F1-A3). F1 no predice mejor que el AR(4) fuera de muestra.

**Conclusión.** La afirmación «hay burbuja» y la afirmación «no hay burbuja» no se pueden sostener con estos datos (veredicto de V17 sobre las dos: engañosa). Los indicadores de nivel son altos frente a su media y los de crédito, contenidos; la evidencia indica que no hay un auge del crédito como el de 2005-2007 y no permite concluir sobre una sobrevaloración medida por el proyecto.


## Parte VII. Medidas: tabla auditada

Esta parte y la siguiente dicen qué se puede y qué no se puede afirmar de cada instrumento y de cada afirmación del debate con la evidencia disponible, y qué dato permitiría afirmar más. Se evalúan instrumentos y afirmaciones, nunca a quien los propone, y no se hacen recomendaciones.

**Resultado: no cambia ningún veredicto de la auditoría de V17.** Ninguna estimación propia es IDENTIFICADO y ninguna cifra V18 pasa de la capa C4; la única estimación designada de clase SUGESTIVO, la de los topes en Cataluña (E2-R1), es compatible con lo que V17 decía sobre la renta de los contratos regulados y añade que la diferencia se reduce durante la vigencia; las demás son ASOCIACIÓN, NO CONCLUYENTE o NO ESTIMABLE y no tienen potencia o diseño para sostener ni para refutar una afirmación; y las magnitudes de V18 son de la literatura que V17 ya había usado. Donde V17 dice «en España no se ha medido» (ITP, ayudas, vivienda pública), el enunciado exacto es «no se ha medido con un diseño que supere las pruebas; hay una estimación exploratoria de clase ASOCIACIÓN o NO ESTIMABLE». No es un cambio de veredicto ni de cifra.

Son las filas de los grupos «Regulación y ayudas» y «Oferta y titularidad» de la tabla final de V17 (output/v17/auditoria/tabla_final.md). La segunda columna da el enunciado auditado (columna «Antes» de esa tabla, abreviado y sin sus cifras). El veredicto de V17 es sobre ese enunciado. La última columna dice si V18 cambia el veredicto.

| Medida | Enunciado auditado (V17, «antes») | Veredicto de V17 | Aporte de V18 (clase, capa C4) | ¿Cambia? |
|---|---|---|---|---|
| Ayudas a la demanda (bono joven, avales) | «Ayudas a la demanda (bono joven, avales): sin evidencia de mejorar la asequibilidad» | incorrecta | E4 sin estimación propia (NO ESTIMABLE). Magnitud solo de la literatura, θ = 0,0408, con dos estudios | No |
| Regulación de la renta de los contratos nuevos (topes) | «Regular la renta de los contratos nuevos: prometedora para el inquilino con contrato regulado», con efectos secundarios documentados y en Cataluña «solo una pista de signo» | engañosa | E2-R1 (SUGESTIVO): renta de los contratos nuevos menor en los municipios regulados, con una diferencia que se reduce durante la vigencia (cifra solo con su frase de limitación, anexo B.2). E2-R1c, contratos (ASOCIACIÓN): sin diferencia detectable | No |
| Regulación de la vivienda turística | «Regular la vivienda turística: prometedora en la literatura internacional, no evaluable en España»; efecto agregado acotado y local sin medir | se sostiene con matices | E1-R3 (ASOCIACIÓN) y E1-R4 (NO CONCLUYENTE); sin evaluación de ninguna norma local sobre el alquiler | No |
| Grandes tenedores | «Los grandes tenedores controlan el mercado»: no hay datos de titularidad para afirmarlo ni negarlo | incorrecta | E10-A1 (ASOCIACIÓN): asociación municipal sin variación exógena; la asociación con los precios sigue sin medirse con diseño | No |
| Rebajar el ITP (medida y discurso) | «Bajar el ITP abarata la vivienda»: no evaluable en España; «Vivienda pública e ITP: sin evidencia en España» | se sostiene con matices | E8-R1 (ASOCIACIÓN): signo contrario a la literatura y dependiente de 2012-2013; E8-R2 (NO ESTIMABLE) | No |
| Más oferta donde hay presión | «Más oferta donde hay presión: prometedora», coherente con el déficit medido y con la literatura internacional, pero tarda años | se sostiene con matices | E5-R1 (NO ESTIMABLE) y E6-R1 (NO ESTIMABLE); magnitud de E6 solo de la literatura (−0,192, un estudio) | No |
| Movilizar vivienda vacía | «Movilizar vivienda vacía: prometedora para reducir la vacancia»; sin evidencia de que baje precios | se sostiene con matices | E11-X1, NO ESTIMABLE: sin calendario de recargos no hay estimación | No |
| Vivienda pública o social | «Vivienda pública e ITP: sin evidencia en España» (parte de vivienda pública) | se sostiene con matices | E12-A1 (NO ESTIMABLE) y E12-A2 (ASOCIACIÓN) miden vivienda protegida, no pública | No |

**Notas por fila.**

- *Ayudas.* La traslación mediana de las ayudas al alquiler a la renta en los estudios con diseño es de 46,0 % de la ayuda (rango 3,6 a 78,0 entre estudios); con sensibilidad de composición, 54,7 % (de 41,0 a 65,0). La magnitud de B5 es distinta porque solo incluye dos estudios con error típico en la misma unidad; no sustituye a la cifra de V17 y la discrepancia se declara (anexo B.4). Ningún estudio es español, y el bono dura menos que el contrato: el umbral de traslación a partir del cual el perceptor pierde en el contrato es de 40,0 %.
- *Topes.* La renta de los contratos regulados es menor en E2-R1 que en los controles, con una diferencia menor que la mediana de la réplica de V17 (−5,8 %); el anexo B.2 explica la diferencia. Que la cantidad de contratos baje sigue en disputa en la literatura, y E2-R1c no la resuelve. La magnitud depende del grupo de control y de la medida de la renta (anexo B.2 y anexo B.14).
- *ITP.* El enunciado exacto pasa a «no se ha medido con un diseño que supere las pruebas». La estimación de V18 es una asociación con signo contrario al de la literatura internacional y no sostiene ni refuta el veredicto. Las fechas de los cambios no están contrastadas con el BOE.
- *Grandes tenedores.* V17 situó a los titulares de más de diez viviendas en el 4,2 % del parque y, con supuestos, entre el 2,2 y el 12,2 % del alquiler habitual; en Barcelona ciudad, el 36,1 % del alquiler habitual en 2021. V18 no añade cifras de peso. Sobre la asociación con el alquiler, E10-A1 no es concluyente y depende de la definición del regresor.
- *Más oferta, vacías y vivienda pública.* V17 cifró el tamaño de la tarea (parte IV) y V18 no la modifica.

**Qué puede decirse hoy de cada medida.** Para las ayudas, los topes, el ITP, la oferta, las vacías y la vivienda pública, la evidencia con diseño de España es escasa o nula y la de otros países es heterogénea. Esta es una afirmación sobre la evidencia y no sobre la conveniencia de la medida.


## Parte VIII. Discurso público: tabla auditada

Son las afirmaciones del grupo «Demanda y precios» de la tabla final de V17. La segunda columna da el enunciado auditado (columna «Antes» de output/v17/auditoria/tabla_final.md, abreviado y sin sus cifras). El veredicto se emite sobre la afirmación, nunca sobre quien la formula. La última columna dice si V18 lo cambia.

| Afirmación | Enunciado auditado (V17, «antes») | Veredicto de V17 | Cifras de V17 y aporte de V18 (clase, capa C4) | ¿Cambia? |
|---|---|---|---|---|
| «Hay burbuja» o «no hay burbuja» | Ninguna de las dos se puede afirmar; no hay exuberancia estadística | engañosa | Variación del precio sobre la renta bruta por hogar frente a 2007: −10,7 %; variación del saldo de crédito sobre el PIB frente a 2007: −28,8 puntos. V18: los modelos F1 a F3 no rechazan la ausencia de cointegración y no publican sobrevaloración; la dinámica de corto plazo es ASOCIACIÓN (F1-R1: ASOCIACIÓN) y F1 no predice mejor que el AR(4) (anexo B.11) | No |
| La inmigración como explicación de la subida | «La culpa es de la inmigración»: correlación frágil y sin signo único en la literatura; la población crece y eso empuja la demanda, pero atribuirlo a un grupo concreto no tiene base | engañosa | La población crece por el saldo migratorio (el residuo es el 128,3 % del crecimiento) y los hogares en alquiler cuya persona de mayor edad nació en el extranjero son el 33,2 % del total. V18: E3-R1 (NO CONCLUYENTE) y E3 sin magnitud preferida | No |
| Los pisos turísticos como explicación de la subida | «La culpa es de los pisos turísticos»: a escala nacional no puede ser lo principal; en barrios concretos es posible, pero no está demostrado en España | engañosa | El aumento de 2020-2024 equivale al 2,7 % del parque de alquiler y el stock de mayo de 2026, al 11,5 %; en el percentil 90 de las secciones, el 33,9 %. V18: E1-R3 (ASOCIACIÓN) y E1-R4 (NO CONCLUYENTE) | No |
| «El alquiler ha subido un X %» | Hay que preguntar si son contratos vigentes o nuevos, y si la cifra es nominal o real | se sostiene con matices | La renta media de los contratos nuevos en Cataluña, ponderada por contratos (Incasòl, 2019-2025), varió 20,0 %; el IPC de alquiler deflactado por la renta por hogar, −13,9 %. V18 no añade estimaciones sobre esta pregunta | No |
| «El precio ha subido un X %» | Según la medida (nominal o real, por m² o con índice), la cifra cambia: quien elige la cifra elige el mensaje | se sostiene con matices | El IPV deflactado por la renta por hogar varió 12,9 % en 2019-2025. V18 no añade estimaciones | No |
| «Con los tipos altos bajarán los precios» | En 2022-2024 subieron los tipos y también los precios | se sostiene con matices | El IPV subió 22,3 % entre 2021T4 y 2024T4. V18: E7-R1 (NO ESTIMABLE) y E7-R3 (ASOCIACIÓN); el rango de la literatura es de −5,0 a −2,0 % por +100 pb | No |

**Por qué no cambian.**

- *Burbuja.* V17 concluía que ninguna de las dos afirmaciones se puede sostener. V18 no aporta un indicador de nivel nuevo, y los modelos de largo plazo no se publican por falta de cointegración. La sobrevaloración que cita V17 es la del Banco de España.
- *Inmigración.* V17 separaba la contabilidad de la población (que V18 no toca) de la asociación con el precio (que V18 tampoco logra medir: E3-R1 es NO CONCLUYENTE y las demás especificaciones, NO ESTIMABLES). La afirmación sigue sin base para atribuir la subida a un grupo concreto, y también sin base para negar que un aumento de población se asocie con más demanda.
- *Turísticos.* Los datos permiten una asociación débil en Barcelona y nada concluyente fuera de ella. V17 situaba la asociación local en los barrios muy expuestos, y V18 no la desmiente ni la confirma.
- *Alquiler y precio.* Son preguntas de definición y medida (contratos vigentes o nuevos, nominal o real, territorio). V18 no estima nada sobre ellas.
- *Tipos.* El hecho de que los precios subieran con los tipos (2022-2024) es descriptivo y V18 no puede contrastarlo: la proyección local con instrumento es NO ESTIMABLE por primera etapa débil, y el BVAR es informativo, con herramienta NO APTA.

**Lo que dicen las preguntas D3 de V17 con V18.** Población: crece por la migración neta (parte II). ¿General o local?: común en compra, mixto en alquiler (parte III). ¿Factible construir?: la necesidad supera varias veces la producción actual (parte IV). Qué no sabemos: el efecto en España de casi todas las medidas, que es también el resultado de V18.


## Parte IX. Qué no sabemos

### IX.1 Limitaciones generales

- **Capa y evaluación.** Toda cifra V18 es de capa C4 y ninguna ha pasado una evaluación en muestra sellada. La vía a una capa superior es la evaluación sellada diferida (evaluate_v18), que se abriría con datos posteriores al tope de entrenamiento y no antes de 2027. Las hipótesis fijadas para esa evaluación (E1-A1, E2-A1, E3-A1, E3-A2, E3-A3, E5-R1 y E6-R2) solo se evalúan si en entrenamiento quedan IDENTIFICADO. Hoy ninguna lo es, de modo que ninguna se evaluaría. Los episodios históricos (Ley 11/2020, el auge anterior a 2010, Barcelona 2011-2019, las cohortes de obra de 2015-2018 y los cambios del ITP) no pueden llegar a C3 con la definición actual de capas.
- **Pre-registro interno.** El plan y la adenda no tienen sello de tiempo externo, y casi todos los factores se habían estimado antes con estos datos: las réplicas no son primeras miradas. Parte de la evidencia de V18 es a posteriori (anexo E).
- **Potencia.** La mayoría de las ampliaciones son NO ESTIMABLES porque la magnitud mínima detectable supera la magnitud de la literatura o el número efectivo de choques es insuficiente. Un resultado NO ESTIMABLE no es un resultado nulo.
- **Literatura.** Muchas fichas son «solo resumen», NO VERIFICADAS o DISCREPANTES (la ficha describe una versión de trabajo y el DOI corresponde a la publicada), y el cuartil de las revistas no está verificado. La búsqueda sistemática adicional con OpenAlex quedó incompleta por agotarse la cuota, y está pendiente. Las magnitudes de otros países se aplican a España con unidades que no siempre coinciden. Para los tipos de interés (E7) no hay estudios con error típico en la unidad: la literatura da un rango de −5,0 a −2,0 % del precio por +100 pb del tipo hipotecario, a 8 trimestres.
- **Herramientas.** El BVAR, la proyección local con Newey-West, el SVAR con proxy y el metaanálisis bayesiano son NO APTOS en el Monte Carlo, y la herramienta de Honest DiD es apta solo sin desviación de tendencias paralelas. Sus resultados se publican con esa etiqueta.
- **Sellado y muestra.** Las comunidades y provincias selladas de v6 (entre ellas Madrid, Baleares y Canarias) y los bloques de V15 y V16 quedan fuera. Las ciudades con más presión turística y de alquiler no están en la muestra, salvo Barcelona con tres distritos menos.
- **Medidas.** El precio se mide con el valor tasado, el IPV por comunidad o el IPVA; el alquiler, con SERPAVI, el IPC de alquiler o los contratos nuevos del Incasòl (solo Cataluña). No son equivalentes.
- **Contabilidad.** Es contabilidad con elasticidades estimadas, sin interacciones ni efectos de equilibrio general, y no una atribución. La variación observada no tiene error. Las diferencias asociadas que proceden de paneles son relativas entre territorios; la versión 1 de la cuenta no las resta de la variación nacional, y la versión 2 (juicio experto) lo hace solo como supuesto escrito, con rangos que proceden de rangos de estudios sin error típico.
- **Réplica ciega.** Solo E2-R1, E8-R1 y E1-R4 tienen réplica ciega; las clases de las demás estimaciones con cifra son provisionales (anexo A.3).
- **Modelos de conjunto.** F1 no predice mejor que el AR(4) fuera de muestra, y los coeficientes de corto plazo de los paneles con PMG no se publican porque suponen una cointegración que no se encuentra (anexo B.11).
- **Fechas del ITP.** Proceden de memorias de Hacienda y no están contrastadas con el BOE.

### IX.2 Qué falta por factor y qué dato lo resolvería

La tercera columna cita, cuando existe, la tarea correspondiente de docs/v18/tareas_autor.md (resumidas en docs/tareas_autor.md).

| Factor | Qué falta | Dato que lo resolvería |
|---|---|---|
| E1 Turismo | Más barrios con cambio de stock; primera etapa del IV; zonas y fechas de la regulación local | Microdatos de portales; geometría del PEUAT y fechas de moratorias; Inside Airbnb anterior a 2025-12 |
| E2 Topes | Renta anterior, superficie y tipo de contrato; tramo de renta; más trimestres posteriores en las zonas de 2024; desvío a temporada | Microdatos de fianzas con renta anterior y registros de otras comunidades; Registro Único de Arrendamientos |
| E3 Inmigración | Variación suficiente para detectar la magnitud de la literatura; Censo de 1991 y más grupos de origen | Series de nacionalidad más finas por provincia; ventanas más largas con datos posteriores |
| E4 Ayudas | Cualquier estimación propia | Microdatos de beneficiarios del Bono Alquiler Joven y de las ayudas autonómicas |
| E5 Oferta y suelo | Restricciones físicas y de planeamiento; primera etapa del Bartik | Sistema de Información Urbana, modelo digital del terreno, costa y agua; descarga masiva del Catastro |
| E6 Obra nueva | Edificios nuevos fuera de la provincia de València; lluvia de AEMET | Descarga masiva del Catastro; lluvia de AEMET |
| E7 Tipos | Primera etapa fuerte; exposición hipotecaria; saldo de préstamos | Licencia de EA-MPD; Encuesta Financiera de las Familias; saldo de préstamos del Banco de España; compraventas anteriores a 2007 |
| E8 Fiscalidad | Fechas verificadas; recaudación; compraventas por tramo | BOE y diarios autonómicos; compras por tramo de precio (Notariado) |
| E9 No residentes | Series de riesgo de más países de origen; compras por nacionalidad y provincia | Notariado y Registradores por nacionalidad y provincia; autorizaciones de golden visa |
| E10 Grandes tenedores | Serie homogénea de titularidad y entrada por zona | Serie del Catastro por tramo de titular, municipio y año; Panel de Hogares AEAT-IEF |
| E11 Vacías | Calendario del recargo del IBI y del impuesto catalán | Ordenanzas fiscales por municipio; calendario de la Ley catalana de vacías; serie anual de vacancia |
| E12 Vivienda pública | Promociones públicas por municipio y año | MIVAU, CASA 47 y empresas públicas autonómicas, por transparencia |
| F1 a F3 | Cointegración detectable con series más largas | Más años de datos y la Encuesta Financiera de las Familias |

### IX.3 Tareas pendientes del autor

Están en docs/tareas_autor.md: datos que harían estimable lo que hoy no lo es, la verificación de cuartiles y de la búsqueda sistemática, la evaluación sellada diferida (no antes de 2027) y los pasos de la publicación 2.0. Ninguna bloquea este documento.

### IX.4 Qué no cambia

Ninguna cifra publicada cambia de valor ni de capa. No hay parada por contradicción con una conclusión publicada, porque ninguna estimación propia es IDENTIFICADO.


## Anexo A. Métodos

### A.1 Diseños por factor

| Factor | Diseños (identificadores del plan) | Estimación propia designada para la magnitud preferida |
|---|---|---|
| E1 Vivienda turística | Estudio de eventos de dosis con el registro HUT (R3); diferencias en diferencias radio-anillo en torno a la Sagrada Família (R4); IV de tipo shift-share con atractivos y búsquedas de Google (R2, A1) | E1-A1 (respaldo E1-R2) |
| E2 Topes al alquiler | Diferencias en diferencias con la Ley 11/2020 sobre renta y número de contratos de Incasòl (R1, R1c); zonas tensionadas de 2024 y otras comunidades (A1, A2); desbordamiento y desplazamiento (A3, A4) | E2-R1 (respaldo E2-A1) |
| E3 Inmigración | IV por asentamientos históricos de cada nacionalidad en provincias (R1, R2, A1 a A5) | E3-R2 (respaldo E3-A1) |
| E4 Ayudas a la demanda | Incidencia de las ayudas con microdatos de perceptores (X1) | ninguna (solo literatura) |
| E5 Oferta y suelo | Bartik de empleo por ramas para la elasticidad de la oferta (R1); interacción con el suelo (A1) | E5-R1 |
| E6 Obra nueva | Diferencias en diferencias por distancia a edificios nuevos (R1, A1); IV con lluvia como en Mense (R2) | E6-R2 |
| E7 Tipos de interés | Proyección local con instrumento (R1); SVAR con proxy (R2); BVAR recursivo, réplica de San Juan (R3, A1); panel provincial con exposición hipotecaria (A2) | E7-R1 (respaldo E7-R2) |
| E8 Fiscalidad de la compra | Diferencias en diferencias de dosis continua del tipo general del ITP (R1 precio, R2 volumen, A2 municipal) | E8-R1 (precio), E8-R2 (volumen) |
| E9 No residentes | Shift-share por riesgo en el país de origen (R1, R2, A1, A2) | E9-R2 |
| E10 a E12 | Asociación transversal (E10); calendario de recargos (E11); IV provincial con vivienda protegida (E12) | ninguna |
| F1 a F3 | Corrección del error, DOLS y PMG, CS-ARDL en panel; modelo de alquiler y de oferta | ninguna |

### A.2 Inferencia

Se publica siempre la inferencia convencional que corresponde a cada diseño. Los errores típicos se agrupan al nivel del tratamiento. Con pocos clusters se usa el wild cluster bootstrap con pesos de Webb. En shift-share se usan los intervalos de Anderson-Rubin y el F efectivo de Montiel Olea y Pflueger, con el número efectivo de choques (inverso del índice de Herfindahl de los pesos, de Borusyak, Hull y Jaravel) calculado antes de estimar. También se usan Conley en datos espaciales, Driscoll-Kraay en paneles con dependencia transversal y Newey-West en series. Cuando el número de clusters es muy pequeño (las comunidades autónomas de E8), la inferencia por aleatorización del calendario sustituye a Webb.

Cada herramienta se valida antes por Monte Carlo con procesos generadores que reproducen la estructura de los diseños (anexo A.15). Un resultado «apto» tiene tamaño y cobertura dentro de las bandas de la adenda 1.12; el anexo A.15 da también el criterio, más amplio, del encargo del Monte Carlo y dice cuál decide. «Con valor crítico corregido» obliga a publicar el p-valor con el valor crítico calibrado en la simulación. «No fiable» se publica con esa etiqueta y la clasificación no puede apoyarse en él. Las herramientas NO APTAS (por ejemplo, la proyección local con Newey-West, el SVAR con proxy, el BVAR y el metaanálisis bayesiano) se publican con esa etiqueta y su resultado se lee como informativo.

### A.3 Clasificación V18

La clase se asigna con las reglas del plan (B3 y criterios I1 a I8, revisados en la adenda 1.2), sin elegirla por el p-valor:

- **IDENTIFICADO.** Diseño creíble, primera etapa fuerte o intervalo de Anderson-Rubin acotado, pretendencias y placebos superados, robustez, significación tras Holm, réplica ciega coincidente y ningún tope de la especificación. Ninguna estimación de V18 llega a esta clase.
- **SUGESTIVO.** Diseño creíble y réplica ciega coincidente, sin fallo decisivo, con alguna prueba débil o un tope fijado en la adenda. Se dice «la evidencia sugiere», con la limitación concreta.
- **NO CONCLUYENTE (sin potencia).** Diseño válido sin significación y sin equivalencia demostrada por la prueba TOST.
- **ASOCIACIÓN.** Diseño no creíble o fallo decisivo de la lista del plan: F efectivo menor que 5 con Anderson-Rubin no informativo; pretendencias con p < 0,01 o M̄ de ruptura < 0,5; placebo de fecha significativo al 5 %, del mismo signo y de al menos la mitad del efecto; cambio de signo en una prueba B4; inferencia «no fiable» sin alternativa apta. Además (K7), un coeficiente no significativo que no supera los criterios de diseño (I1 a I5) es ASOCIACIÓN: por ejemplo, con un placebo de fecha significativo de cualquier signo, que indica que el diseño no es creíble para ese resultado (es el caso de E2-R1c).
- **NO ESTIMABLE.** Falta un dato imprescindible o la comprobación previa de variación no alcanza el mínimo. Esta comprobación se aplica antes que la clasificación.

Tres lecturas decididas antes de difundir resultados (docs/v18/decisiones.md). Un cambio de signo en una prueba de robustez del plan es un fallo decisivo y no se compensa con un tope (K7). Un coeficiente no significativo es NO CONCLUYENTE si supera los criterios de diseño y ASOCIACIÓN si no los supera (K7). Cuando la ficha admite dos lecturas con clases distintas se toma la más prudente (K8 bis). La etiqueta de coherencia con la literatura (I6) se publica, pero no interviene en la clase ni en la entrada en la magnitud preferida.

Réplica ciega (I8). El plan no clasifica un resultado sin réplica ciega coincidente. Se hizo para E2-R1, E8-R1 y E1-R4 (orden de la fase 4). Las clases de las demás estimaciones con cifra (entre ellas E1-R3, E3-R1, las de E7, E10, E12 y la familia F) son provisionales hasta I8, como dicen sus resultado.json; la réplica solo podría bajarlas o dejarlas sin clase.

Cifras sin clase propia (K12 y K14). Cada cifra lleva la clase de su propia especificación, no la del estudio. Cuatro valores marcan las cifras que no tienen clase propia: «sin clasificar (coprincipal informativa)» para la coprincipal que el plan no clasifica (E1-P-H3); «robustez a posteriori» para las pruebas añadidas tras ver el resultado (B6); «diagnóstico o variante (sin clase propia)» para los diagnósticos, las variantes enumeradas y las pruebas de una estimación, incluidas las cifras auxiliares que el documento cita de su salida de origen; y «literatura (sin clase propia)» para los valores publicados por la literatura y sus reproducciones (ids V18-AUX-LIT-* y V18-AUX-REP-*), porque la clase V18 es de un factor o de una estimación propia, no de un valor publicado. Las filas de magnitud preferida (V18-B5) llevan la clase de la estimación propia designada del factor, no la de la magnitud ni la del rango.

Capa y lenguaje (K2). Toda cifra V18 es de capa C4, con nivel de evidencia EXPLORATORIO. La clase V18 va en un campo propio al lado de la capa y no la promueve. Cada cifra se lee como asociación condicionada al diseño. La fórmula condicional prevista para la clase IDENTIFICADO solo cabría en los anexos técnicos, y no se ha necesitado.

### A.4 Estimabilidad previa por magnitud mínima detectable

Antes de estimar cada especificación principal, y sin mirar su resultado, se calcula por Monte Carlo la magnitud mínima detectable (MDE) con la potencia convencional fijada en la adenda 1.3. El cálculo usa la variación real del tratamiento, de la exposición o del instrumento y la dispersión residual de V15 o V16 (declarada «ya vista») o la del periodo previo. La especificación es estimable si el MDE no supera la magnitud de referencia de la literatura convertida a nuestra unidad. Si no, es NO ESTIMABLE por variación y se publica el MDE, no el coeficiente. Además se exigen mínimos de datos (por ejemplo, un número mínimo de municipios tratados y de control) y, en shift-share, un número efectivo de choques suficiente. Esta comprobación explica la mayoría de los NO ESTIMABLE.

### A.5 Magnitud preferida (B5, adenda 1.9)

- **Qué entra.** La estimación propia designada de cada factor, si su diseño es válido y es IDENTIFICADO, SUGESTIVO o NO CONCLUYENTE, con independencia de su p-valor. No entran las ASOCIACIÓN ni las NO ESTIMABLE. Los estudios de la literatura entran si están en la misma unidad y tienen error típico.
- **Episodios compartidos.** Si una estimación propia y un estudio miden el mismo episodio con la misma fuente, el episodio cuenta una vez, combinado con una correlación modelada fijada en la adenda.
- **Modelo.** Metaanálisis bayesiano de efectos aleatorios con tres priors sobre el efecto medio. La magnitud preferida se publica solo si la decisión (signo e inclusión del cero) coincide en las tres. Si no, se publica el rango de las tres sin magnitud preferida. Si la heterogeneidad es alta y el intervalo de predicción cambia de signo, tampoco hay magnitud preferida. Con un solo estudio se publica su magnitud; con dos, el efecto fijo ponderado por precisión. Si las unidades no son comparables, no se combinan.
- **Advertencia de la simulación.** El metaanálisis bayesiano resultó NO APTO por conservador: sus intervalos cubren de más y, con dos estudios y heterogeneidad, el efecto fijo no cubre la media verdadera. Los intervalos con más de dos estudios son prudentes y los de dos estudios no deben leerse como IC95 fiables.
- **Referencias.** Toda referencia lleva el estado de su ficha: VERIFICADA (DOI comprobado con Crossref o DataCite; cuartil no verificado), NO VERIFICADA o DISCREPANTE (la ficha describe una versión de trabajo y el DOI corresponde a la versión publicada; se trata como NO VERIFICADA).
- **Confianza de la tabla de magnitudes.** Regla fija: «media» solo con magnitud preferida de tres o más estudios; «muy baja» si la literatura no tiene error típico en la unidad; «baja» en el resto. Nunca «alta», porque toda cifra es C4. La clasificación de cada fila es la de la estimación propia designada del factor; la magnitud preferida puede venir solo de la literatura. Con un estudio, el intervalo es el IC95 de ese estudio; con dos, el del efecto fijo, que no es un IC95 fiable.

### A.6 Contabilidad de la subida (adenda 1.10)

La diferencia asociada a un factor en la contabilidad es su magnitud preferida por su variación observada en el periodo y el territorio, con la incertidumbre propagada por Monte Carlo sobre la magnitud y una fila «no explicado». Es contabilidad con elasticidades estimadas, no una descomposición estructural ni una atribución: no hay interacciones ni efectos de equilibrio general, y los factores no son ortogonales. Reglas:

- Un factor sin magnitud dice «sin magnitud», no cero.
- Cada diferencia asociada que procede de un diseño de panel con efectos de periodo se rotula «relativa entre provincias (o unidades), sin el componente común». Solo los tipos (E7, series nacionales) incluyen el componente común. Por eso, en la regla del Documento de Trabajo V18, las filas relativas no se restan de la variación nacional. El documento final solo lo hace en la versión 2 de la cuenta (parte V.4), como supuesto de juicio experto escrito, con la fila «no explicado» que K14 (N4) había retirado y K15 recupera rotulada.
- Cada fila dice si la variación observada del factor está dentro o fuera del soporte de la muestra de estimación. Fuera del soporte no lleva cifra.
- Inmigración (E3) y no residentes (E9) usan cuotas del padrón por nacionalidad y no se suman: E9 va como alternativa de E3.
- **Lectura restrictiva aplicada.** La adenda admite todo factor con magnitud preferida construida con las reglas de B5. El plan deja las magnitudes «solo literatura» en una tabla secundaria rotulada, y una magnitud sin estimación propia no tiene clase que limite la confianza. Se aplicó la lectura restrictiva (K10): la tabla principal solo admite factores con estimación propia dentro de B5. Ninguno la cumple. Las magnitudes de la literatura van en una tabla aparte, rotulada ilustración en V18 y «juicio experto con magnitudes de la literatura, no estimación propia» en el documento final (parte V.4, versión 2). La lectura inclusiva solo cambiaría de tabla a E1, E4 y E6, y no cambiaría ninguna conclusión.
- La variación observada usa el deflactor del PIB del INE, no el IPC general que usó V8. Las variaciones observadas difieren por eso de las de V8.
- Las viviendas liberadas por envejecimiento nunca se restan de la necesidad (la proyección de hogares del INE ya las descuenta).

### A.7 Modelos de conjunto (F)

El modelo de precio de largo plazo con corrección del error, el de alquiler y el de oferta se contrastan primero para cointegración, con corrección por pruebas múltiples. Si el contraste no rechaza la ausencia de cointegración, no se publican elasticidades de largo plazo ni sobrevaloración (regla AD-F), y solo se publica la dinámica de corto plazo como ASOCIACIÓN, cuando su estimador no supone la cointegración (por eso no se publican los coeficientes de corto plazo del PMG; anexo B.11). El modelo de precio se evalúa además fuera de muestra en la misma muestra que el AR(4) y el ECM v1, en bloques con embargo; solo «predice mejor» si supera a la línea base más exigente (K1 de v6.1).

### A.8 Evaluación sellada diferida

La vía a la capa C3 es una evaluación sellada diferida (evaluate_v18) con datos posteriores al tope de entrenamiento, una sola evaluación por hipótesis y un criterio de superación fijado en la adenda 1.11. No se ejecuta dentro de V18, requiere orden expresa del autor y no puede abrirse antes de 2027. Los episodios históricos (Ley 11/2020, el auge anterior a 2010, Barcelona 2011-2019, las cohortes de obra de 2015 a 2018 y los cambios del ITP) no pueden llegar a C3 con la definición actual de capas.

### A.9 Multiplicidad y registro

Toda especificación, incluidas las variantes y las fallidas, se registra antes de leer su resultado. Se controlan los falsos descubrimientos con Holm dentro de la familia de cada factor y con Benjamini-Yekutieli entre las variantes enumeradas de cada identificador. Ningún modelo se elige por su p-valor. SEED 20261010 en todo lo aleatorio.

**Regla general.** Toda cifra del documento procede de output/v5/cifras_clave.csv con su id (V18-*, V17-* y anteriores), su fuente, su capa y, en las cifras V18, su clasificación. El generador redondea los valores: dos decimales para los menores que la unidad en valor absoluto, un decimal para los intermedios y enteros para los recuentos y las cifras grandes. Los coeficientes pequeños se muestran con tres cifras significativas; los límites de sus intervalos, redondeados como se acaba de decir (los valores completos están en tablas_v18.xlsx, pestaña «estimaciones»).

### A.10 Fuentes por factor

| Factor | Fuentes principales | Periodo y nivel |
|---|---|---|
| E1 Vivienda turística | Registro de viviendas de uso turístico (HUT) del Ajuntament de Barcelona con coordenadas por licencia; SERPAVI (alquiler mediano por sección); Censo 2021; INE de viviendas turísticas por sección; OpenStreetMap (atractivos); Google Trends; Eurostat (noches por NUTS 3) | Barcelona por sección y barrio, 2011-2024; otras cuatro ciudades por sección, 2021-2024 |
| E2 Topes al alquiler | Incasòl, registro de fianzas (renta media y número de contratos por municipio); paro registrado mensual del SEPE por municipio; padrón; Censo 2021; BOE y DOGC | Municipios de Cataluña, trimestral desde 2019T1 y anual desde 2007 |
| E3 Inmigración | Padrón por nacionalidad (stock a 1 de enero); Censo de 2001 por nacionalidad (Eurostat); entradas por nacionalidad (INE y Eurostat); valor tasado del MIVAU; IPVA; SERPAVI | Provincias, 2002-2022 |
| E4 Ayudas a la demanda | Calendario estatal del Bono Alquiler Joven (RD 42/2022); Encuesta de Condiciones de Vida | Sin microdatos de perceptores |
| E5 Oferta y suelo | Viviendas iniciadas y terminadas (MIVAU); valor tasado; empleo por rama (Eurostat e INE, NUTS 3); deflactor | Provincias, 2002-2023 |
| E6 Obra nueva | Catastro INSPIRE de los municipios de la provincia de València que lo publican; SERPAVI por sección | Secciones de la provincia de València, 2011-2024 |
| E7 Tipos de interés | Tipos hipotecarios y euríbor (Banco de España); sorpresas monetarias de alta frecuencia (Jarociński y Karadi); valor tasado; IPV; IPC de alquiler; compraventas; visados | Nacional, 1999-2026; panel provincial |
| E8 Fiscalidad de la compra | Tipo general del ITP por comunidad (memorias de Hacienda, base de intervenciones de V16); valor tasado provincial; compraventas mensuales | Comunidades de régimen común no selladas, desde 2010 |
| E9 No residentes | Padrón por nacionalidad de 2003; series de riesgo en origen (PIB, precios de la vivienda: Eurostat y OCDE); cuota de compras de no residentes (MIVAU) | Provincias y países de origen |
| E10 Grandes tenedores | Estadística de titularidad del Catastro (tres cortes, 2024-2026); alquiler municipal por m² | Municipios |
| E11 Viviendas vacías | Censos de 2011 y 2021 (este último por consumo eléctrico) | Dos cortes con métodos distintos |
| E12 Vivienda pública | Calificaciones definitivas de vivienda protegida (MIVAU) | Provincias, 2002-2024 |
| F1-F3 Modelos de conjunto | PIB, renta disponible, población, hogares, tipos, parque, iniciadas y valor tasado | Nacional trimestral y panel provincial |

Muestras concretas de las estimaciones principales:

- E1-R3 (Barcelona): 769 de las 1.068 secciones de Barcelona (sin Gràcia, Sant Andreu y Nou Barris, sellados en V15 y V16), en 48 barrios; 769 con SERPAVI; viviendas del Censo 2021 como denominador.
- E2-R1 (Ley 11/2020): 49 municipios regulados por la Ley 11/2020 y 94 controles de Cataluña, panel trimestral equilibrado 2019T1-2022T1 sin Barcelona ciudad; sin los municipios sellados en v6, V15 y V16.
- E3-R1 (inmigración): 39 provincias de entrenamiento; N = 234; sin las 11 provincias de v6.
- E8-R1 (ITP): 30 provincias con valor tasado trimestral de 7 comunidades de régimen común no selladas (sin Cantabria: no hay serie provincial completa), 2007T1-2026T2.
- E10-A1 (grandes tenedores): 1365 municipios.
- E7-R3 (BVAR de tipos): nacional.

### A.11 Unidades selladas que se excluyen

- **v6.** Se excluyen de toda estimación las comunidades y provincias de la muestra sellada de v6 (Aragón, Asturias, Illes Balears, Canarias, Madrid, Región de Murcia, Navarra y La Rioja, con sus provincias y todos sus municipios, distritos y secciones). Quedan fuera, entre otras, las ciudades de Madrid, Palma, Zaragoza y Murcia.
- **V15 y V16.** Se excluyen los municipios, distritos y secciones de los bloques espaciales sellados de V15 y V16. En Barcelona, València, Sevilla y Málaga eso aparta una parte de los distritos: la muestra de Barcelona pierde Gràcia, Sant Andreu y Nou Barris. El total municipal de una ciudad con distritos sellados es una fuga declarada y no se usa en las principales (adenda 1.5).
- **Sellado temporal.** No se usa ningún periodo posterior al último visto de cada variable en V15 y V16, ni ninguna edición publicada después de la fecha de corte común de ambas (2026-10-17). Los topes por variable están en docs/v18/sellado_v18.json, generado con solo metadatos después de la etiqueta y antes de la primera estimación. Donde dos reglas dan topes distintos se aplica el más restrictivo (por ejemplo, el total de transacciones de extranjeros).
- **Distritos sellados en v3.** No se excluyen: su muestra sellada ya se abrió en v3 con una evaluación por hipótesis (docs/v3/decisiones.md). Se dice por transparencia.
- **Sin acceso a muestras selladas.** No se lee data/sealed ni las filas marcadas como muestra sellada de v6, y no se ejecuta ninguna evaluación sellada. Las fuentes se leen con el filtro de sellado de V18 y con la exclusión de v6.

### A.12 Datos posteriores a la etiqueta

Las fuentes abiertas que el inventario de la fase 0 marcaba como ausentes y que no requerían al autor se descargaron después de la etiqueta (Censo de 2001 por nacionalidad, OpenStreetMap, Google Trends, Open Data BCN, afiliación por sector, tipos de cambio, entre otras). Llevan la marca `posterior_prereg` y su manifiesto. Su adquisición se limitó a descargar, normalizar y auditar, sin cruzarlas con ningún resultado. Cuando una fuente no pudo descargarse, la especificación que la necesitaba pasó a NO ESTIMABLE y se anotó en docs/v6/fuentes_fallidas.md.

### A.13 Licencias y terceros

- Incasòl: datos no redistribuibles; solo se publican agregados propios.
- Registradores: el aviso legal prohíbe reproducir; sus agregados se usan solo como contraste interno.
- Inside Airbnb: su política pide no republicar los datos; se publican solo agregados.
- Notariado: el portal no permite extracción automática; las compras por nacionalidad y al contado son tarea del autor.
- Paquetes de replicación de otros autores: se guardan fuera de git, con su licencia y suma de control. Ningún PDF se versiona; las fichas llevan enlace, DOI, licencia y notas, con citas de 15 palabras como máximo.
- Los PDF y paquetes figuran en data/bib (fuera de git, con sha256 en data/bib/CHECKSUMS.sha256).

### A.14 Interpolaciones y fuentes no validadas

Las series interpoladas (por ejemplo, visados de 1995 a 2007) y las fuentes no validadas entran solo en robustez. Las fechas de entrada en vigor de los cambios del ITP proceden de memorias de Hacienda y no están contrastadas con el BOE: por ello E8 tiene tope SUGESTIVO y esa limitación se repite en el anexo B.8.

### A.15 Monte Carlo de las herramientas

Cada herramienta nueva se validó antes de usarse con procesos generadores que reproducen la estructura de los diseños de V18 (output/v18/montecarlo/<herramienta>/). Se simula bajo el nulo y bajo la alternativa, con semilla fija y sin ningún dato real de resultado ni muestra sellada.

Hay dos criterios de «apto», y los dos se publican. El del encargo del Monte Carlo, más amplio, pide un tamaño al 5 % entre 0,03 y 0,08 y una cobertura al 95 % entre 0,92 y 0,97, bajo el nulo y bajo la alternativa; con él se escribió el veredicto de cada herramienta (columna «Veredicto» de la segunda tabla). Las bandas de la adenda 1.12, más estrictas, piden un tamaño entre 0,04 y 0,06 y una cobertura entre 0,93 y 0,97; son las que deciden en la inferencia de cada estimación (por ejemplo, el valor crítico corregido cuando el tamaño cae fuera de su banda) y están en la columna banda_112 de cada tabla.csv. Cuando los dos criterios difieren, la inferencia sigue el de la adenda, que es el del pre-registro (adenda 1.12 e I7); el criterio del encargo solo rotula la herramienta. La tabla da, por herramienta, el mínimo y el máximo entre las filas que deciden su veredicto (columna «principal», «entra_en_veredicto» o «decisivo» de su tabla.csv; si no la hay, la variante principal, con h = 8 en las proyecciones locales y el proxy-SVAR). Los escenarios de diagnóstico (rotulados así en su tabla.csv, como los de pocos controles o de variabilidad distinta) no deciden el veredicto y no entran en el mínimo ni en el máximo; en webb_twfe solo entran las filas del bootstrap de Webb, porque las de CR1 son otra inferencia (su veredicto está en la segunda tabla). El valor de cada condición está en output/v18/montecarlo/<herramienta>/tabla.csv y el veredicto en su resultado.json. En meta_bayes la cobertura es la de μ.

| Herramienta | Tamaño al 5 %: mínimo a máximo | Cobertura al 95 %: mínimo a máximo |
|---|---|---|
| aleatorizacion | 0,053 a 0,0635 | 0,936 a 0,947 |
| bhj | 0,0015 a 0,262 | 0,739 a 0,999 |
| conley | 0,052 a 0,261 | 0,739 a 0,948 |
| cs_webb | 0,0565 a 0,178 | 0,822 a 0,944 |
| dcdh_aleatorizacion | 0,0455 a 0,0535 | 0,947 a 0,955 |
| driscoll_kraay | 0,16 a 0,566 | 0,434 a 0,84 |
| honest_did | 0 a 0,0845 | 0,915 a 1 |
| iv_debil | 0 a 0,193 | 0,807 a 1 |
| lp_iv | 0,0104 a 0,118 | 0,882 a 0,99 |
| meta_bayes | 0,00967 a 0,5 | 0,5 a 0,99 |
| sa_webb | 0,0575 a 0,071 | 0,929 a 0,943 |
| sdid_conley_taber | 0,0445 a 0,056 | 0,944 a 0,956 |
| svar_proxy | 0,0127 a 0,0873 | 0,913 a 0,987 |
| webb_twfe | 0,0465 a 0,0595 | 0,941 a 0,954 |

El BVAR se valida con sus bandas del 68 % y del 90 %, que son aptas si cubren entre 0,63 y 0,73 y entre 0,87 y 0,93, respectivamente; en sus filas decisivas la cobertura al 68 % va de 0,0055 a 0,988 y la del 90 % de 0,117 a 1.

| Herramienta | Veredicto | Condición |
|---|---|---|
| Callaway-Sant'Anna con Webb | APTO CONDICIONADO | Diseños municipales con muchos tratados y controles; NO APTO con ocho clusters |
| Sun-Abraham con Webb | APTO | Frágil si las comunidades de control son pocas |
| de Chaisemartin-D'Haultfœuille con aleatorización del calendario | APTO | Aleatorización entre ocho comunidades. El t de Student con siete grados de libertad es apto con valor crítico corregido (banda de la adenda 1.12); solo el bootstrap de Webb con ocho clusters es NO APTO |
| Aleatorización | APTO | Entre municipios y entre comunidades |
| Honest DiD | APTO CONDICIONADO | Solo sin desviación de tendencias paralelas; con desviaciones mayores es válido pero conservador y sin potencia |
| DiD sintético con Conley-Taber | APTO | Si los tratados son intercambiables con los controles; no si son más variables |
| Webb en TWFE | APTO | Con 8, 30 y 39 clusters (tamaños del diseño de la simulación: comunidades, provincias con valor tasado y provincias de entrenamiento). En la misma tabla, CR1 con la normal es APTO CONDICIONADO (NO APTO con ocho clusters) y CR1 con t de Student de G − 1 grados de libertad es APTO; los diseños con muy pocos tratados son NO APTOS |
| Conley | Mixto | Apto si el alcance de la dependencia no supera el corte; NO APTO si lo duplica |
| IV débil | Mixto | APTO con instrumento fuerte; APTO CONDICIONADO o NO APTO en los diseños más débiles |
| BHJ con pocos choques | NO APTO | Con pocos choques efectivos; por eso, con menos de 20, la inferencia principal de E3, E5, E9 y E12 es Webb por provincia con Anderson-Rubin y BHJ queda como alternativa (adenda 1.13) |
| Driscoll-Kraay con T corto | NO APTO | Con series temporales cortas |
| Proyección local con instrumento | NO APTO | Newey-West subestima la incertidumbre; el AR aumentado con EHW es el más cercano al nominal bajo el nulo; con T corto la respuesta a horizontes largos queda atenuada |
| SVAR con proxy | NO APTO | AR por método delta apto solo con F cercano a diez |
| BVAR recursivo | NO APTO | Bandas conservadoras o con cobertura distinta de la nominal |
| Metaanálisis bayesiano | NO APTO por conservador | Intervalos que cubren de más; con dos estudios y heterogeneidad el efecto fijo no cubre la media verdadera |

En la simulación, con ocho comunidades, la aleatorización del calendario es apta; el t de Student con siete grados de libertad lo es con valor crítico corregido, y el bootstrap de Webb es NO APTO. La muestra de E8-R1 tiene 7 comunidades. Las herramientas NO APTAS se publican con esa etiqueta y la clasificación no se apoya en ellas.


## Anexo B. Réplicas por factor

Cada subsección sigue el mismo orden: estudio original, reproducción, réplica, ampliación y magnitud preferida. Las estimaciones propias se rotulan «estimación propia V18» y llevan su clase V18 y su capa. Las magnitudes de la literatura se rotulan «literatura» y llevan el estado de su ficha (VERIFICADA, NO VERIFICADA o DISCREPANTE; la verificación es la del DOI, y el cuartil de la revista no está verificado). Todas las cifras V18 son de capa C4 y se leen como asociaciones condicionadas al diseño.

Los valores publicados por estudio de la literatura, con su error típico cuando el autor lo da o se deduce de lo publicado, están en la Tabla B.0 (output/v18/f5/magnitudes_estudios.csv; ids V18-AUX-LIT-*). Cada valor está en la unidad de su autor y no es comparable entre estudios sin conversión. Esta sección describe cada estudio por su diseño, su signo y el estado de su ficha, y da las magnitudes agregadas con los ids de la magnitud preferida (V18-B5-E1 a V18-B5-E9).

Tabla B.0. Valores publicados por estudio (literatura; capa C4)

| Factor | Estudio (estado de la ficha) | Valor publicado | Error típico | Unidad del autor |
|---|---|---|---|---|
| E1 | Segú (2018), Barcelona, 2009-2016 (NO VERIFICADA) | 0,038 | 0,012 | Δln alquiler por punto de densidad de Airbnb |
| E1 | Garcia-López et al. (2020), Barcelona, 2007-2017 (VERIFICADA) | 0,022 | 0,011 | ln por cada 100 anuncios en la BSA (IV, alquileres) |
| E1 | Chaves-Fonseca (2026), Madrid, 2010-2018 (VERIFICADA) | 0,02 | 0,004 | ln del precio por 100 anuncios en el barrio |
| E2 | Jofre-Monseny et al. (2023), Cataluña, 2020-2022 (VERIFICADA) | −0,044 | 0,006 | ln de la renta media, tabla 2 |
| E2 | Monràs y García-Montalvo (2023), Cataluña, 2016-2021 (VERIFICADA) | −0,058 | 0,014 | ln del precio del contrato (sin efectos fijos de unidad) |
| E2 | Breuille et al. (2025), París y cinco ciudades, 2018-2024 (NO VERIFICADA) | −0,051 | 0,007 | ln de la renta por m² |
| E2 | Hahn et al. (2021), Berlín, 2019-2020 (VERIFICADA) | −0,113 | 0,019 | ln de la renta anunciada (estrategia A; B: −0,075) |
| E2 | Pérez García (2026), zonas tensionadas 2024 (VERIFICADA) | −0,0298 | 0,0113 | puntos de crecimiento de la renta |
| E3 | González y Ortega (2009, IZA), provincias, 1998-2008 (NO VERIFICADA) | 3,2 | 1,33 | % de precio por 1 % de población (euros/m²: 44,72 con error 18,58) |
| E3 | González y Ortega (2011, Chicago Fed), provincias, 2001-2010 (NO VERIFICADA) | 0,866 | 0,803 | elasticidad respecto a la población en edad de trabajar |
| E3 | Sanchis-Guarner (2017), provincias, 2001-2012 (DISCREPANTE) | 3,05 | 1,21 | puntos de crecimiento del precio por punto de tasa de inmigración (semielasticidad ≈ % por 1 %) |
| E3 | Saiz (2007), áreas metropolitanas de EE. UU., 1983-1998 (VERIFICADA) | 1,61 | 0,326 | Δln precio por 1 % de población en inmigrantes |
| E3 | Sá (2015), autoridades locales de Inglaterra y Gales, 2004-2010 (VERIFICADA) | −1,63 | 0,366 | % de precio por 1 % de población |
| E3 | Unal (2022), distritos de Alemania, 2004-2020 (NO VERIFICADA) | 2,69 | 0,648 | % por 1 % de población inicial (pisos) |
| E3 | Accetturo et al. (2012), distritos de 20 ciudades de Italia (DISCREPANTE) | 0,16 | 0,053 | elasticidad log-log (ciudad) |
| E3 | Torres y Montero (2023), provincias, 2001-2019 (VERIFICADA) | −0,95 | — | % de precio por 1 % de población (texto) |
| E4 | Fack (2005), Francia, 1984-2002 (VERIFICADA) | 0,39 | 0,24 | θ (DD con controles; sin controles 0,76 con error 0,26) |
| E4 | Eerola et al. (2026), Finlandia, reforma de 2015 (VERIFICADA) | 0,036 | 0,028 | θ |
| E4 | Kangasharju (2008), Finlandia (VERIFICADA) | 0,57 | — | θ (IV) |
| E4 | Hyslop y Rea (2018), Nueva Zelanda (VERIFICADA) | 0,36 | — | θ |
| E5 | Taltavull (2006), panel de CCAA, 1990-2004 (NO VERIFICADA) | 0,87 | 0,125 | elasticidad precio de los inicios de obra (error desde t = 6,96) |
| E5 | Baum-Snow y Han (2020, versión de trabajo), tractos de EE. UU., 2000-2010 (DISCREPANTE) | 0,26 | 0,11 | elasticidad precio de la oferta de unidades |
| E5 | Paciorek (2012), EE. UU. (VERIFICADA) | 0,84 | 0,1 | elasticidad de permisos al precio (IV) |
| E6 | Mense (2025), regiones de planificación de Alemania, 2010-2017 (VERIFICADA) | −0,192 | 0,065 | elasticidad del alquiler respecto a la oferta nueva |
| E6 | Asquith, Mast y Reed (2020, versión de trabajo), EE. UU. (DISCREPANTE) | −0,062 | 0,037 | Δln cerca de un edificio nuevo |
| E7 | San Juan (2023, Banco de España), BVAR, 2004-2022 (VERIFICADA) | −2 | — | % del precio por +100 pb a 8 trimestres |
| E7 | Battistini et al. (2022, BCE), proyecciones locales, área del euro (NO VERIFICADA) | −5 | — | % del precio por +1 pp del tipo hipotecario a ~2 años |
| E8 | Dolls et al. (2020), Länder de Alemania, 2005-2018 (VERIFICADA) | −3 | — | % de precio por +1 pp del tipo, a 12 meses (publicada −3; WP −3,5) |
| E9 | Sá (2016), Inglaterra y Gales, 1999-2014 (VERIFICADA) | 2 | — | % de precio por +1 pp de cuota (IV en volumen: 2,0; valor: 1,4; principal 2,1) |
| E9 | Álvarez et al. (2020, Banco de España), provincias, 2013T4-2019 (NO VERIFICADA) | 2,55 | 2,26 | % de crecimiento acumulado por +1 pp de compras netas sobre el parque |

Duso et al. (2024) y Abel et al. (2024) no tienen valor en magnitudes_estudios.csv y no figuran en la tabla. Los rangos de la literatura de E8 y E9 proceden de un solo estudio cada uno (Dolls et al. 2020 y Sá 2016, con los valores de sus versiones o especificaciones), y el de E7, de dos (San Juan 2023 y el BCE). Los intervalos de la magnitud preferida están en la tabla del resumen ejecutivo. El estado de las fichas que no se citan con estado en el texto está en output/v18/f1/catalogo.csv y en el anexo C.2.

### B.1 Vivienda turística (E1)

**Original (literatura).** Garcia-López, Jofre-Monseny, Martínez-Mazza y Segú (2020), Journal of Urban Economics 119, 103278 (ficha VERIFICADA). Barcelona, datos de 2007-2017, alquiler anunciado. Diseños: efectos fijos con tendencias heterogéneas por barrio; shift-share con atractivos turísticos (dónde) y búsquedas de Google (cuándo); estudio de eventos; caso de la Sagrada Família. Resultado publicado (resumen de los autores, evaluado al nivel de actividad de 2016): alquiler +1,9 % en el barrio medio y +7 % en el decil de mayor actividad de Airbnb. Su unidad es el logaritmo del alquiler por cada 100 anuncios en el área estadística básica, y no es convertible a puntos de densidad de viviendas porque la ficha no da las viviendas por área. Con sus coeficientes y la densidad turística observada, V17 calculó una ilustración, que no es una estimación: 1,6 por ciento del alquiler a escala nacional (rango 1,0 a 2,1).

**Reproducción.** El paquete de Garcia-López et al. no es público, y no se reproduce. Sí se reproduce, con el paquete de su autor, Chaves-Fonseca (2026) (VERIFICADA): un instrumento del mismo tipo (proximidad a atractivos por búsquedas de Google) sobre precios de compra en Madrid. Coincide con lo publicado (anexo C.1). Valida la herramienta, no el resultado de Barcelona.

**Réplica (estimaciones propias V18, Barcelona).**

- E1-R3, estudio de eventos de dosis (densidad HUT de 2018T2 por periodo posterior, sobre el logaritmo del alquiler mediano de SERPAVI por sección): coeficiente 0,00443 por punto de densidad, con IC95 que excluye el cero. Clase ASOCIACIÓN, capa C4. El contraste conjunto de los adelantos de 2011 y 2012 rechaza las tendencias paralelas previas (p = 0,00838): con p < 0,01 es un fallo decisivo de la regla del plan, y por eso la clase es ASOCIACIÓN. El coeficiente es unas 0,117 veces el de la referencia de Segú (2018), es decir, mucho menor. La diferencia no se explica con estos datos; tres rasgos de la medida van en esa dirección: SERPAVI mide la renta del conjunto de contratos declarados (stock) y no la de los anuncios; la dosis es el registro HUT, no la actividad de Airbnb; y el periodo es otro. Muestra: 769 de las 1.068 secciones de Barcelona (sin Gràcia, Sant Andreu y Nou Barris, sellados en V15 y V16), en 48 barrios; 769 con SERPAVI; viviendas del Censo 2021 como denominador; la estimación usa las 766 secciones con SERPAVI en todo el periodo.
- E1-R4, Sagrada Família (secciones del radio frente al anillo exterior): coeficiente 0,00166, con IC95 de Webb que incluye el cero. Clase NO CONCLUYENTE: el diseño es válido, la estimación no es significativa y la equivalencia con el nulo no queda acotada. La réplica ciega y el modelizador partieron de lecturas distintas de la ficha (con y sin los adelantos de 2011-2012 como regresores); se resolvió a favor de la más prudente (K8 bis). La variante con adelantos se publica al lado: coeficiente 0,00259, IC90 de Webb −0,0257 a 0,0394, que acota el nulo. Su resultado.json la rotula «nulo acotado», pero no tiene réplica ciega coincidente y, por K8 bis, la clase de E1-R4 es la de la principal: la variante va como diagnóstico o variante (sin clase propia).
- E1-R1 (stock HUT por barrio) es NO ESTIMABLE: solo 18 barrios cumplen el cambio mínimo de stock exigido por el plan. E1-R2 (IV con atractivos y búsquedas) es NO ESTIMABLE: F efectivo de la primera etapa 0,0233.
- Coprincipal H3 de V15 en la muestra V18: −0,000065 (logaritmo del alquiler por desviación típica intra-sección). El plan no clasifica las coprincipales que repiten una pregunta ya vista: clase sin clasificar (coprincipal informativa) (la misma en el anexo B.14 y en cifras_clave). Como en V15, no se distingue de cero. Q2a de V16 dio 0,0132 en el logaritmo del IPC de alquiler por desviación típica de la exposición, con una herramienta NO APTA, solo puntual.

**Ampliación.** E1-A1 (viviendas turísticas por sección, instrumentadas con proximidad a atractivos por noches de la NUTS 3, en València, Sevilla, Málaga y Alicante, 2021-2024) es NO ESTIMABLE: la magnitud mínima detectable es 0,166, frente a 0,038 de la referencia. La regulación local (PEUAT y moratorias) como diferencias en diferencias no se estima: faltan la geometría de las zonas y las fechas (tarea 13 del autor).

**Magnitud preferida (literatura).** 0,038 en Δln del alquiler por +1 pp de viviendas turísticas sobre el parque, clase de la estimación propia designada NO ESTIMABLE, capa C4. Procede de un solo estudio, Segú (2018), un documento de trabajo cuya ficha es NO VERIFICADA: la magnitud preferida de E1 descansa en una referencia no verificada. Estudios de España: 1 estudio con error típico en la unidad; estado B5: magnitud de un solo estudio. Los tres estudios con ficha VERIFICADA (Garcia-López et al., Chaves-Fonseca y Duso et al.) no entran por unidad no convertible. La estimación propia E1-R3 no es coherente con la referencia (etiqueta I6). Confianza baja.

**Lectura.** Los datos disponibles no permiten contrastar la magnitud local de la literatura ni en otras ciudades ni después de las regulaciones. No contradice lo publicado: v3, v6 y V8 calificaban de no concluyente el resultado nacional, y V17 circunscribía la asociación local a Barcelona en 2012-2016.

### B.2 Topes al alquiler (E2)

**Original (literatura).** Jofre-Monseny, Martínez-Mazza y Segú (2023), Regional Science and Urban Economics 101, 103916 (VERIFICADA): diferencias en diferencias y estudio de eventos con el registro de contratos; renta menor en los contratos regulados y sin caída detectable de la oferta. Monràs y García-Montalvo (2023), documento de trabajo de la Reserva Federal de San Francisco (VERIFICADA): contratos del Incasòl, no anuncios (así lo recoge la ficha de la fase 1, que corrige la lectura del plan); efectos distintos por tramo de precio. Con el mismo registro, la réplica de V17 sobre la renta de los contratos nuevos da una mediana de −5,8 por ciento (rango de especificaciones −6,8 a −5,1; no es un intervalo de confianza).

**Reproducción.** Ninguno de los dos estudios tiene paquete público (microdatos no públicos del Incasòl). No se reproducen.

**Réplica (estimación propia V18).**

- E2-R1, renta media de los contratos nuevos, 2019T1-2022T1. Coeficiente −0,038 en logaritmos (IC95 de Webb −0,051 a −0,026). Clase SUGESTIVO, capa C4. La réplica ciega coincide con el coeficiente del modelizador, y las dos rondas del abogado del diablo no activan ningún fallo decisivo. La clase queda en SUGESTIVO por la potencia insuficiente de la prueba de pretendencias, el placebo de fecha en el límite y la corrección de un fallo conocido de V9-D1b (grupo de control y ventana).

La cifra no se difunde sin la frase de limitación siguiente, que se reproduce tal cual (K9; docs/v18/revision_estimaciones/ronda2_e2r1.md):

> Entre 2020T4 y 2022T1, la renta media de los contratos nuevos registrados en el Incasòl en los 49 municipios sujetos a la Ley 11/2020 (sin Barcelona ciudad) se situó, respecto a 2019, un 3,8 % por debajo (log −0,038; IC95 −0,051 a −0,026) de la de municipios catalanes no regulados con mercado tensionado. La diferencia no es estable: es máxima en 2021T1 (−0,058), se reduce de forma gradual hasta no distinguirse de cero en 2022T1, antes de la STC 37/2022, sin cambio posterior, y baja a −0,023 (IC95 −0,045 a −0,001) cuando se permiten trayectorias trimestrales distintas según el tamaño del municipio. Con estos datos no se separa la parte asociada a la norma de un choque transitorio de la COVID-19 en los municipios grandes ni de un cambio en la composición de los contratos registrados, y la sensibilidad a tendencias diferenciales (Honest DiD con M̄ ≥ 0,5) no es evaluable con la potencia disponible. La magnitud coincide con la de Jofre-Monseny et al. (2023), que usan el mismo registro y el mismo episodio. Clase V18: SUGESTIVO; capa del proyecto C4.

Muestra de la estimación: 49 municipios regulados por la Ley 11/2020 y 94 controles de Cataluña, panel trimestral equilibrado 2019T1-2022T1 sin Barcelona ciudad; sin los municipios sellados en v6, V15 y V16. El porcentaje es la transformación 100·(exp(b)−1) del coeficiente (−3,77 %). El valor M̄ ≥ 0,5 es el de la adenda 1.12: con M̄ = 0,5 el intervalo de Honest DiD va de −0,087 a 0,025 e incluye el cero, pero con esa M̄ la herramienta tiene tamaño nulo y potencia casi nula en el Monte Carlo, de modo que el intervalo no informa sobre el efecto (anexo A.15).

**E2-R1 frente a V17 y a otras medidas.** La réplica de V17 con el mismo registro da una mediana de −5,8 % (rango de sus especificaciones −6,8 a −5,1 %, que no es un intervalo de confianza), una diferencia mayor que la de E2-R1 (−3,77 %). Las especificaciones no son las mismas: E2-R1 sigue el plan de V18, con el paro registrado trimestral como control, sin Barcelona ciudad y sin los municipios sellados en V15 y V16, mientras que las de V17 combinan otras ventanas y grupos de control. Con trayectorias por tamaño del municipio (robustez a posteriori) la diferencia baja a −0,023 en logaritmos. En el multiverso enumerado de la adenda el coeficiente va de −0,056 a −0,005, siempre negativo. El extremo menos negativo es el de la variante con SERPAVI, que mide la renta del conjunto de contratos vigentes y no la de los nuevos: −0,005 (IC95 −0,017 a 0,007). La prueba de pretendencias no rechaza, pero el sesgo que no podría detectar (potencia de Roth) es de 0,061 en logaritmos, mayor que el propio coeficiente.

- Pruebas. La prueba de pretendencias no rechaza, pero su potencia es insuficiente para descartar una pendiente previa relevante (párrafo anterior). El placebo de fecha (adopción falsa en 2017) tiene signo contrario al principal. Honest DiD solo es apto con M̄ igual a cero; con valores mayores es válido pero conservador y no decide (anexo A.15). El placebo de resultado no tiene dato en el repositorio. El signo es negativo en todas las variantes estimadas.
- Robustez a posteriori (B6; no decide la clase; clase de estas cifras: robustez a posteriori). El coeficiente medio no describe un nivel estable: la diferencia se reduce durante la vigencia. Con HUT y ln(población) por trimestre: −0,0242. Con controles emparejados por el crecimiento previo de la renta: −0,0546. Con diferencias en diferencias sintéticas: −0,044. Los intervalos de estas tres variantes excluyen el cero. Salto en 2022T2 sobre la extrapolación de la recta: −0,0217, con IC95 que incluye el cero.
- Reversión tras la STC 37/2022 (2022T2-2023T4): −0,00157, con IC95 que incluye el cero (diagnóstico o variante (sin clase propia): es una prueba de E2-R1). El nivel vuelve al previo y no se detecta un rebote.
- E2-R1c, número de contratos nuevos por 1.000 habitantes: coeficiente 0,0173, con IC95 que incluye el cero. Clase ASOCIACIÓN. El placebo de fecha es significativo pero de signo contrario al principal, de modo que no es por sí solo el fallo decisivo de la lista del plan (que exige el mismo signo); la clase sale de la regla K7: un coeficiente no significativo es NO CONCLUYENTE solo si supera los criterios de diseño (I1 a I5), y este no los supera, porque el placebo de fecha significativo indica que el diseño no es creíble para este resultado y la diferencia persiste tras la STC (tope de la adenda). Con el denominador de hogares inquilinos del Censo 2021, la variante a posteriori da −0,0314, también con IC95 que incluye el cero y que no excluye caídas relevantes. No se descarta el desvío a contratos de temporada ni la falta de depósito de fianza.

**Ampliación.** Las cuatro ampliaciones son NO ESTIMABLES. Zonas tensionadas de 2024 en Cataluña (E2-A1): MDE 0,0408, superior al umbral. Otras comunidades (E2-A2): 6 municipios tratados con datos y periodo posterior, frente a un mínimo mayor del plan. Desplazamiento a la venta (E2-A3): 2 municipios de control en la serie municipal del MIVAU. Desbordamiento a municipios vecinos (E2-A4): MDE 0,0444, superior al umbral. El análisis por tramo de renta y el desvío a temporada necesitan los microdatos de fianzas (tarea 4 del autor).

**Comparación con lo publicado.** El informe integral (III.2) calificaba los topes de «prometedora» y recogía una renta regulada menor. E2-R1 es compatible con esa lectura y añade que la diferencia se reduce durante la vigencia. Sobre el número de contratos, V17 concluía que la evidencia no permite concluir; E2-R1c no lo cambia. V17 recoge para los contratos una mediana de 3,6 por ciento (rango −1,3 a 7,6). E2-A1 repite H1 y H2 de V15 en entrenamiento y no sustituye su evaluación sellada.

**Magnitud preferida.** No hay. Estudios de España, Francia, Alemania: 5 estudios con error típico en la unidad; método: metaanálisis bayesiano de efectos aleatorios (3 priors); estado B5: rango sin magnitud preferida (la decisión no coincide en las tres priors). La decisión no coincide en las tres priors (con una de ellas el intervalo incluye el cero), la heterogeneidad es alta y el intervalo de predicción cambia de signo. Se publica el rango de las tres priors: −0,122 a 0,0029 en logaritmos de la renta de los contratos regulados (clase de la estimación propia designada: SUGESTIVO). Estudios que entran (literatura): Jofre-Monseny et al. 2023 (VERIFICADA), Monràs y García-Montalvo 2023 (VERIFICADA), Breuille et al. 2025 (NO VERIFICADA), Hahn et al. 2021 (VERIFICADA) y la estimación propia E2-R1, contando una vez el episodio catalán. La ficha de Hahn et al. admite dos estrategias para extraer su magnitud. La elección de la estrategia A (la primera de la ficha) se tomó en la fase 5, antes de combinar pero después de la etiqueta y de ver E2-R1: es una decisión a posteriori (anexo E). Con la estrategia B sí habría magnitud preferida; se publica como sensibilidad y no cambia la tabla (con la estrategia B: −0,0487 en logaritmos, intervalo −0,0835 a −0,0179; output/v18/f5/sensibilidad_b5.csv). La herramienta es NO APTA por conservadora.

### B.3 Inmigración (E3)

**Original (literatura).** González y Ortega (2013), Journal of Regional Science 53(1), 37-59: instrumento por asentamientos históricos de cada nacionalidad en provincias españolas, años 2000-2010 según la ficha de la fase 1. Se leen además dos versiones previas del mismo trabajo, con ventanas distintas: IZA 2009 (NO VERIFICADA) y Chicago Fed 2011 (NO VERIFICADA). La fase 1 señala que lo que cada versión cuantifica no es lo mismo: en torno al 25 % del aumento de precios en la versión Chicago Fed de 2011 y «un cuarto» (25 %) en la edición de 2013, según sus resúmenes; la versión IZA de 2009 no da una fracción, sino un aumento acumulado del precio de en torno al 52 % para la entrada media de extranjeros (extrapolación lineal de los autores). V17 dedujo del resumen de la versión de 2013 una elasticidad implícita de 1,3 por ciento de precio por 1 % de población (rango 1,0 a 1,5); es una derivación a partir del resumen, no un coeficiente publicado. Saiz (2007) y Borusyak, Hull y Jaravel (2022) son referencias metodológicas.

**Reproducción.** González y Ortega no tiene paquete público. Se reproduce, con el paquete de sus autores, Borusyak, Hull y Jaravel (2022), aplicación de Autor, Dorn y Hanson con datos: coincide con lo publicado en todos los coeficientes comparados, y la herramienta de shift-share queda validada (anexo C.1).

**Réplica (estimación propia V18).** E3-R1 (provincias no selladas, 2002-2008, sin 2003; instrumento por la distribución del grupo de origen en el Censo de 2001 y las entradas nacionales del grupo; ocho grupos de origen en lugar de dieciséis, desviación declarada): asociación entre la entrada de extranjeros y la variación anual del valor tasado de 3,55 €/m² por punto de población, con IC95 de Webb-Anderson-Rubin de −53,5 a 63,9. F efectivo de la primera etapa 81,1; magnitud mínima detectable 36,7 €/m² por punto; número efectivo de choques 7,9. El umbral de choques efectivos de la adenda (1.13) tiene dos usos: por debajo de 20, la inferencia principal de cualquier shift-share pasa a Webb por provincia con el intervalo de Anderson-Rubin, y BHJ queda como alternativa; solo en E9, por debajo de 10, la especificación es NO ESTIMABLE. Por eso E3-R1 se estima y E9 no. La clase de E3-R1 se apoya en Webb con Anderson-Rubin, no en BHJ, que es NO APTA con pocos choques en el Monte Carlo (anexo A.15). Aun así, con tan pocos choques efectivos (Rumanía pesa mucho en las cuotas) la inferencia por provincia también puede quedar corta, y es una limitación de esta estimación. Clase NO CONCLUYENTE, capa C4. El intervalo incluye el cero y también la magnitud de la versión IZA de 2009 (44,7 €/m² por punto de población, error típico 18,6). Muestra: 39 provincias de entrenamiento; N = 234; sin las 11 provincias de v6.

**Ampliación.** Las demás especificaciones son NO ESTIMABLES por variación (la magnitud mínima detectable supera la de referencia): la elasticidad de 2002-2010 (E3-R2, MDE 2,33), su variante hasta 2008 (E3-R2b, 2,14), la ampliación de 2014 a 2022 en precio (E3-A1, 10,4 % por punto), en alquiler municipal (E3-A2, 13,4 % por punto) y la ventana de 2002 a 2019 (E3-A5, 3,8 % por punto). La separación entre demanda de compra y de alquiler por tenencia del Censo de 2011 no tiene datos (E3-A4). Coincide con V9-D4 (F efectivo bajo) y con H4 de V15 y Q3 de V16 (no concluyentes).

**Magnitud preferida.** No hay. Estudios de España, EE. UU., Reino Unido, Alemania: 5 estudios con error típico en la unidad; método: metaanálisis bayesiano de efectos aleatorios (3 priors); estado B5: rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo). Rango de las tres priors: −0,49 a 3,5 en % de precio por +1 % de población (literatura). Entran González y Ortega 2009 (NO VERIFICADA), Sanchis-Guarner 2017 (DISCREPANTE), Saiz 2007 (VERIFICADA), Sá 2015 (VERIFICADA) y Ünal 2022 (NO VERIFICADA). Quedan fuera por versión duplicada, unidad o falta de error típico: González y Ortega 2011 (NO VERIFICADA), Accetturo 2012 (DISCREPANTE) y Torres y Montero 2023 (VERIFICADA). La heterogeneidad es alta y el intervalo de predicción cambia de signo. La estimación propia designada es NO ESTIMABLE, y E3-R1 (NO CONCLUYENTE) está en otra unidad: se muestra al lado y no se combina. La elasticidad implícita de V17 cae dentro del rango.

### B.4 Ayudas a la demanda (E4)

**Original (literatura).** Fack (2005, CEPREMAP; VERIFICADA) y Fack (2006): diferencias y triples diferencias con la extensión de las ayudas al alquiler de los años noventa en Francia. Gibbons y Manning (2006): recorte del Housing Benefit en el Reino Unido. Grislain-Letrémy y Trevien (2022, Banque de France, documento de trabajo 886): discontinuidad geográfica en aglomeraciones francesas. Eerola et al. (2026; VERIFICADA): Finlandia. Todos miden la parte de la ayuda que acaba en el alquiler (traslación θ) o su relación con el alquiler en otra unidad. Ningún estudio es español.

**Reproducción y réplica.** Ninguno tiene paquete público. E4 es NO ESTIMABLE (E4-X1): no hay microdatos de perceptores del Bono Alquiler Joven ni convocatorias autonómicas con fecha, solo el calendario estatal. La discontinuidad por edad de Q7a (V16) da −0,12 en el logaritmo del alquiler (IC95 −0,26 a 0,02); mide un cambio de generosidad, no la incidencia, y no se repite.

**Magnitud preferida (solo literatura, sin estimación propia).** θ = 0,0408 euros de alquiler por euro de ayuda, clase NO ESTIMABLE, capa C4. Estudios de Francia, Finlandia: 2 estudios con error típico en la unidad; método: media ponderada por la inversa de la varianza (efecto fijo); estado B5: magnitud preferida. Entran Fack 2005 (VERIFICADA) y Eerola et al. 2026 (VERIFICADA), por efecto fijo ponderado por precisión; Kangasharju 2008 (VERIFICADA) y Hyslop y Rea 2018 (VERIFICADA) quedan fuera por falta de error típico en la ficha. Con dos estudios y heterogeneidad, el efecto fijo no cubre la media verdadera en la simulación, de modo que su intervalo (−0,0138 a 0,0953) no es un IC95 fiable y no se presenta como tal. Esta magnitud está dominada por el estudio más preciso (Eerola et al.) y no sustituye a la lectura de V17, que usó la mediana de la traslación de siete u ocho estudios con una cifra por estudio: 46,0 % (rango 3,6 a 78,0) con siete estudios y 54,7 % con ocho. En la misma escala, θ = 0,0408 euros por euro es una traslación muy inferior a esa mediana. La diferencia procede de la composición: B5 solo admite estudios con error típico en la unidad (dos), pondera por precisión y queda cerca del estudio finlandés, mientras que V17 da el mismo peso a cada estudio. Ninguna de las dos cifras es española, y la discrepancia se declara sin elegir entre ellas.

### B.5 Oferta y suelo (E5)

**Original (literatura).** Saiz (2010, Quarterly Journal of Economics): elasticidades de oferta por área metropolitana con restricciones geográficas (solo resumen en la ficha; sin paquete). Baum-Snow y Han (2020; DISCREPANTE: se lee la versión de trabajo, publicada en 2024): elasticidades por choques de demanda laboral; solo código. Taltavull (2006; NO VERIFICADA): comunidades autónomas españolas, 1990-2004. Paciorek (2012; VERIFICADA).

**Reproducción.** Ninguna: el paquete de Baum-Snow y Han no cabe en el disco y el resto no tiene paquete.

**Réplica (estimación propia V18).** E5-R1, elasticidad de las viviendas libres iniciadas respecto al valor tasado real, con un Bartik de empleo de cuatro ramas en provincias, 2002-2023: NO ESTIMABLE, y no se publica ningún coeficiente. El F efectivo de la primera etapa es 0,032 en toda la ventana (6,6 en 2002-2007, 0,00179 en 2008-2013 y 0,182 en 2014-2023), y el número efectivo de choques es 3,3. La interacción del instrumento de inmigración con los solares por vivienda (E5-A1) da 0,00244, con IC95 que incluye el cero y una magnitud mínima detectable de 0,0134. Clase ASOCIACIÓN. No se usa la Red Natura como instrumento, porque ya falló en Q4.

**Ampliación.** Las restricciones físicas (pendiente, costa, agua) y de planeamiento (SIU) no están en el repositorio (tarea 5 del autor); la elasticidad tipo Saiz no se estima. La elasticidad de la oferta de F3 se resume en 4.11.

**Magnitud preferida.** No hay. Estudios de España, EE. UU.: 3 estudios con error típico en la unidad; método: metaanálisis bayesiano de efectos aleatorios (3 priors); estado B5: rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo). Rango de las tres priors: −0,20 a 1,5 (elasticidad precio de la oferta, literatura). Entran Taltavull 2006 (NO VERIFICADA), Baum-Snow y Han 2020 (DISCREPANTE) y Paciorek 2012 (VERIFICADA). La heterogeneidad es alta y el intervalo de predicción cambia de signo. El Informe Anual 2025 del Banco de España usa una elasticidad de oferta como cota superior, que es de otro orden de incertidumbre y no se usa en la contabilidad.

### B.6 Obra nueva y alquileres cercanos (E6)

**Original (literatura).** Mense (2025), Journal of Political Economy Macroeconomics (VERIFICADA): elasticidad del alquiler respecto a la oferta nueva, con un instrumento de lluvia, en Alemania. Asquith, Mast y Reed (2020; DISCREPANTE: se lee la versión de trabajo, publicada en 2023): alquileres cerca de edificios nuevos, en Estados Unidos.

**Reproducción.** Con el paquete de Mense (CC0, con datos): coincide con lo publicado (anexo C.1). Asquith, Mast y Reed solo tiene código.

**Réplica (estimación propia V18).** E6-R1 (cohortes de edificios terminados en 2015-2018 en la provincia de València; secciones contiguas; antigüedad del Catastro INSPIRE y SERPAVI): NO ESTIMABLE por variación; la magnitud mínima detectable es 0,0623, un poco por encima del umbral de la adenda. Se aplica la regla y no el matiz. E6-A1 (edificios mayores, anillo menor): 0 secciones tratadas, frente al mínimo del plan, NO ESTIMABLE por datos. La réplica de Mense (E6-R2) necesita la lluvia de AEMET, que no está en el repositorio. Fuera de la provincia de València, la descarga masiva del Catastro no está disponible (tarea 1 del autor).

**Magnitud preferida (literatura, un solo estudio).** −0,192 en elasticidad del alquiler respecto a la oferta nueva (% por 1 %), clase de la estimación propia designada NO ESTIMABLE. Estudios de Alemania: 1 estudio con error típico en la unidad; estado B5: magnitud de un solo estudio. Procede de Mense 2025 (VERIFICADA). Asquith, Mast y Reed quedan fuera por otra unidad y no se combinan. La ilustración de V17 con esta elasticidad da −0,50 % del alquiler medio al cerrar el déficit (rango −0,63 a −0,37); es un orden de magnitud, no una estimación.

### B.7 Tipos de interés (E7)

**Original (literatura).** San Juan (2023), Banco de España (VERIFICADA): BVAR con identificación recursiva; intervalos al 68 % solo en un gráfico, sin error típico numérico. BCE, Boletín Económico 6/2022 (NO VERIFICADA): proyecciones locales. Jarociński y Karadi (2020) y Altavilla et al. (2019) aportan las sorpresas monetarias, que se usan como dato.

**Reproducción.** No hay paquete con las series del Banco de España; las sorpresas se usan como dato y no se reproducen.

**Réplica (estimaciones propias V18, nacionales).**

- E7-R1, proyección local con instrumento, ocho trimestres, valor tasado, 1999T1-2024T2: 2SLS de 1,28 % del precio por +100 pb. El conjunto de Anderson-Rubin es toda la recta, la primera etapa tiene signo contrario al esperado y el F efectivo es bajo. Clase NO ESTIMABLE. Repite la debilidad ya vista en V8 y V16. La proyección local con Newey-West es NO APTA en el Monte Carlo y se publica con esa etiqueta.
- E7-R2, SVAR con proxy: −10,5 (% del precio por +100 pb del tipo (impacto normalizado; SVAR con proxy)). Clase NO ESTIMABLE (primera etapa débil; Anderson-Rubin no acotado; herramienta NO APTA).
- E7-R3, BVAR recursivo (réplica de San Juan, 2008T1-2022T4): a ocho trimestres de +100 pb del euríbor, el precio responde −1,55 %, con banda del 68 % de −2,3 a −0,87. Clase ASOCIACIÓN. Se publica solo como informativa, porque el Monte Carlo del BVAR es NO APTO (bandas conservadoras o con cobertura distinta de la nominal). La ampliación a 2026T2 (E7-A1) da −0,321 %, con banda del 68 % de −1,9 a 1,2, que incluye el cero. Una parte de las extracciones del posterior es explosiva (raíz máxima mayor que uno): el 15 % en E7-R3 y el 74,6 % en E7-A1. Las bandas incluyen esas extracciones, de modo que la de E7-A1 describe sobre todo trayectorias no estacionarias y no debe leerse como incertidumbre de una respuesta estable.
- Panel provincial (E7-A2), respuesta relativa entre provincias a la sorpresa por la exposición hipotecaria: −19,7 (% del precio por pp de sorpresa y por unidad de exposición (relativo entre provincias, sin el componente común)). Clase NO ESTIMABLE.
- Regla de clase cuando el intervalo de Anderson-Rubin no está acotado. E7-R1 y E7-R2 son NO ESTIMABLES porque no superan la comprobación previa de la adenda 1.3 (la magnitud mínima detectable no se alcanza con ninguna potencia de la rejilla) y la regla de NO ESTIMABLE se aplica antes que la clasificación. E12-A2 (anexo B.10) no tiene magnitud de referencia en su unidad, de modo que esa comprobación no se puede hacer; pasa a la clasificación, y allí un F efectivo menor que 5 con Anderson-Rubin no acotado es un fallo decisivo: ASOCIACIÓN.

**Comparación.** San Juan estima una caída del precio a ocho trimestres menor que la del BCE, en el extremo menos negativo del rango de la literatura, con otra unidad (el choque al tipo hipotecario, no al euríbor). E7-R3 coincide en el signo; la etiqueta I6 de E7-R1 es «no coherente». V17 calibró con las elasticidades de la zona euro un efecto de −11,4 % del precio (rango −22,6 a −11,4) para una subida de 2,5 puntos del tipo de las hipotecas nuevas entre 2021T4 y 2023T3. Es una calibración, no una estimación para España, y V18 no la sustituye.

**Magnitud preferida.** No hay. Literatura sin estudios con error típico en la unidad; estado B5: rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico). Rango de la literatura sin error típico, de −5,0 a −2,0 % del precio por +100 pb del tipo hipotecario a ocho trimestres. San Juan 2023 (VERIFICADA) y el BCE (NO VERIFICADA) no entran en el metaanálisis por falta de error típico.

### B.8 Fiscalidad de la compra (E8)

**Original (literatura).** Best y Kleven (2018) y Besley, Meads y Surico (2014): impuestos de transmisión en el Reino Unido, con datos fiscales administrativos; sin paquete. Dolls et al. (2020; VERIFICADA): precio de la vivienda frente al tipo del impuesto de transmisión. La búsqueda de la fase 1 no encontró una evaluación española del ITP con diseño cuasi experimental; la búsqueda sistemática quedó incompleta (parte IX), de modo que no se afirma que no exista.

**Reproducción.** Ninguna.

**Réplica (estimación propia V18).** E8-R1, diferencias en diferencias de dosis continua con el tipo general del ITP por comunidad sobre el logaritmo del valor tasado provincial, respuesta acumulada a cuatro trimestres: 0,0146 por punto del tipo general, con IC95 por inversión de la aleatorización de los calendarios que excluye el cero; tras la corrección de Holm con la coprincipal, p = 0,0874, que no es significativo al 5 %. Clase ASOCIACIÓN, capa C4. Muestra: 30 provincias con valor tasado trimestral de 7 comunidades de régimen común no selladas (sin Cantabria: no hay serie provincial completa), 2007T1-2026T2. La réplica ciega coincide. Tiene signo contrario al de la referencia (etiqueta I6: no coherente) y, sin los años 2012-2013, el signo cambia: el calendario de cambios se concentra en la crisis y el diseño no separa el tipo del ciclo. Un cambio de signo en una prueba del plan es un fallo decisivo (K7). Las fechas de entrada en vigor proceden de memorias de Hacienda y no están contrastadas con el BOE. La coprincipal Q6-p de V16, reproducida en la muestra V18, se mantiene sin clasificar. El volumen de compraventas (E8-R2, MDE 0,0894 por punto) y la ampliación municipal (E8-A2, MDE 0,216 por punto) son NO ESTIMABLES por variación. El análisis de recaudación y de agrupamiento en umbrales no tiene datos.

**Inferencia.** La muestra de E8-R1 tiene 7 comunidades. Con tan pocas, en el Monte Carlo (simulado con ocho comunidades) la aleatorización del calendario es apta, el t de Student con siete grados de libertad lo es con valor crítico corregido y solo el bootstrap de Webb es NO APTO. La inferencia de E8-R1 es la de la aleatorización.

**Magnitud preferida.** No hay. Literatura sin estudios con error típico en la unidad; estado B5: rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico). Rango de la literatura sin error típico, de −3,5 a −3,0 % de precio por +1 pp del ITP a doce meses. El rango procede de un solo estudio, Dolls et al. (2020, VERIFICADA): sus extremos son las cifras de su versión publicada y de su versión de trabajo, no la dispersión entre estudios. Clase de la estimación propia designada (E8-R1): ASOCIACIÓN.

### B.9 Compradores no residentes (E9)

**Original (literatura).** Badarinza y Ramadorai (2018): choques en los países de origen y precios por barrios de Londres. Cvijanović y Spaenjers (2021): París, magnitud pequeña y no significativa. Sá (2016; VERIFICADA): documento del Centre for Macroeconomics de la London School of Economics, con instrumento. Álvarez, Blanco y García-Posada (2020; NO VERIFICADA): regresión de corte transversal para España, sin instrumento. Ninguno tiene paquete.

**Réplica (estimación propia V18).** E9 es NO ESTIMABLE por choques efectivos. Con la exposición del padrón de 2003 y los ocho orígenes con serie de riesgo, el inverso del índice de Herfindahl es 6,3 sin pesos y 5,9 con pesos de población, por debajo del mínimo de 10 choques efectivos que la adenda (1.13) fija solo para E9 (en E3, con menos de 20, cambia la inferencia, no la estimabilidad; anexo B.3). Si todos los países del padrón tuvieran serie de riesgo, sería 11,5: el límite son las series de riesgo de los países latinoamericanos, africanos y asiáticos, que no están en el repositorio. El índice de exposición de E9 y el instrumento de E3 se construyen con las mismas cuotas del padrón y están muy correlacionados: no se suman, y E9 va como alternativa de E3 en la contabilidad. El fin de la golden visa como diferencias en diferencias no se estima (sin datos que separen UE de fuera de la UE).

**Contexto descriptivo.** La cuota de compras de no residentes fue 7,4 % de las transacciones entre 2025T2 y 2026T1 (V16). Es un dato descriptivo.

**Magnitud preferida.** No hay. Literatura sin estudios con error típico en la unidad; estado B5: rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico). Rango de la literatura sin error típico, de 1,4 a 2,1 % de precio por +1 pp de cuota de compras de no residentes. Procede de un solo estudio, Sá (2016, VERIFICADA): sus extremos son especificaciones del mismo trabajo, no la dispersión entre estudios. Álvarez, Blanco y García-Posada no entra por ser una asociación transversal sin instrumento.

### B.10 Grandes tenedores, viviendas vacías y vivienda pública (E10 a E12)

- **E10, grandes tenedores.** La fase 1 no encontró estudios con datos españoles. La replicación exigiría la entrada de grandes tenedores por zona y la renta de contratos; solo hay tres cortes de titularidad. E10-X1 es NO ESTIMABLE. E10-A1 es una asociación transversal entre el alquiler municipal por m² y el porcentaje de viviendas de grandes tenedores: 1,07 % del alquiler por punto, con IC95 que incluye el cero (muestra: 1365 municipios). En la variación de 2019 a 2024 (E10-A1-d), 0,105. La definición del regresor cambia el resultado: con personas jurídicas (E10-A1-v1), 2,71, con IC95 que excluye el cero. Clase ASOCIACIÓN: sin variación exógena y con el tramo contado dentro del municipio, que da una cota inferior. V17 midió que los titulares de más de diez viviendas tienen el 4,2 % del parque (Catastro, 2026) y entre el 2,2 y el 12,2 % del alquiler habitual con supuestos explícitos. V18 no duplica esas cifras.
- **E11, viviendas vacías.** NO ESTIMABLE (E11-X1): no hay calendario de adopción del recargo del IBI por municipio ni del impuesto catalán, y la vacancia solo tiene dos cortes con métodos distintos, de modo que una diferencia entre cortes confundiría el método con la diferencia buscada. Tarea 12 del autor.
- **E12, vivienda pública.** Solo hay calificaciones de vivienda protegida por provincia, no promociones públicas por municipio y año (tarea 11 del autor). E12-A1, respuesta de las viviendas libres iniciadas a la vivienda protegida calificada con un instrumento provincial: 6,5 viviendas libres por vivienda protegida (ambas por 100 del parque), con conjunto de Anderson-Rubin de −1,2 a 170,0, que incluye el cero. Clase NO ESTIMABLE (magnitud mínima detectable superior a la de referencia). E12-A2, valor tasado real: 22,1 (% del valor tasado real (variación anual) por cada 100 viviendas protegidas calificadas por 100 del parque), con un conjunto de Anderson-Rubin no acotado. Clase ASOCIACIÓN: sin magnitud de referencia en su unidad no hay comprobación previa de estimabilidad, y el F efectivo menor que 5 con Anderson-Rubin no acotado es un fallo decisivo (la diferencia de regla con E7-R1 se explica en el anexo B.7). Ninguna de las dos mide la vivienda pública.

### B.11 Modelos de conjunto (F1 a F4)

En ninguno de los contrastes de cointegración de la familia F, con corrección de Holm, se rechaza la ausencia de cointegración. Por la regla AD-F no se publican elasticidades de largo plazo de precio, alquiler u oferta, ni la sobrevaloración (F1-A3), y no se hacen las comparaciones de F4. El resultado coincide con V7.2 y V8-M4 y no cambia ninguna cifra ni conclusión publicada.

- F1, precio frente a renta real de los hogares, trimestral nacional, 1999T1-2026T2: elasticidad de impacto en variaciones de 0,126, con IC95 que incluye el cero (clase ASOCIACIÓN).
- Paneles provinciales (F1-R2, F2-R1, F3-A2). Sus coeficientes de corto plazo se estimaron con PMG, que supone una relación de largo plazo común; como los contrastes no encuentran cointegración, esos coeficientes no se interpretan y no se publican aquí, y no hay en la tabla de F una especificación de panel en diferencias que los sustituya (no se estima ninguna nueva). En F2-R1 el coeficiente de corto plazo del alquiler respecto a la renta tenía además signo negativo, contrario al esperado, y cambia de signo con SERPAVI en lugar del IPC de alquiler (F2-R1-v1): es otra señal de que la especificación no es fiable. En F3-A2 hay una señal cercana a la cointegración, que se declara sin publicarse como largo plazo.
- El nivel de precio frente a renta que usan los indicadores del Banco de España (V17) es de 8,4 años de renta bruta por hogar en el último dato; V18 no lo replica con elasticidades.

**Evaluación fuera de muestra de F1 (K1 de v6.1).** El modelo de corrección del error de F1 (F1-ECM: AR(4) más los niveles y las variaciones retardadas de los fundamentales) se compara en la misma muestra con el AR(4) y con el ECM v1 del proyecto, a un paso, en 105 trimestres de prueba repartidos en bloques con embargo.

| Modelo | RMSE fuera de muestra (variación trimestral del precio real, %) |
|---|---|
| F1-ECM | 1,36 |
| AR(4) | 1,28 |
| ECM v1 (aproximado) | 2,05 |

Diebold-Mariano (corrección HLN) de F1-ECM frente a AR(4): p = 0,187. Giacomini-White frente a AR(4): p = 0,378. Clark-West, con el AR(4) anidado en F1-ECM: p unilateral = 0,0729; este contraste corrige el ruido que añade estimar los parámetros de más del modelo grande, de modo que puede acercarse a la significación aunque el RMSE de F1-ECM sea mayor, y no rechaza al 5 %. El conjunto de confianza de modelos al 90 % contiene a F1-ECM (p = 0,234) y al AR(4), y excluye al ECM v1. F1-ECM no predice mejor que el AR(4): su error es mayor y ninguna de las tres pruebas rechaza la igualdad al 5 %. Solo supera al ECM v1, que no es la línea base más exigente. El ECM v1 es aproximado en el mismo sentido que en v6: no se reestima el ECM original de v1 con sus variables y su especificación, sino una sola ecuación por MCO de la variación del precio sobre el nivel retardado del precio y de los fundamentales de F1, sin retardos de la variación.

### B.12 Lectura conjunta

- La única estimación designada de clase SUGESTIVO es E2-R1. Sus robusteces a posteriori, sus diagnósticos (reversión, estudio de eventos) y la fila de la ilustración no heredan su clase: cada cifra lleva la de su propia especificación (K12). Las clases de las estimaciones sin réplica ciega son provisionales (anexo A.3).
- Las etiquetas de coherencia con la literatura (I6) son informativas: E2-R1 es coherente con Jofre-Monseny et al.; E1-R3, E7-R1 y E8-R1 no lo son. No intervienen en la clase.
- Las estimaciones propias con cifra que no son la designada de su factor (por ejemplo, E1-R3, E1-R4 y E3-R1) no entran en la magnitud preferida: son ASOCIACIÓN o NO CONCLUYENTE, o están en otra unidad.
- La coherencia de F4 entre los modelos de conjunto y los factores no puede evaluarse: F no publica elasticidades de largo plazo.

### B.13 Planes de replicación

El pre-registro interno lo forman el plan de replicación (docs/v18/plan_replicacion.md, commit d4e9869) y su adenda (docs/v18/plan_replicacion_adenda.md), que prevalece donde difiera. La etiqueta git local plan-replicacion-v18 señala el commit de la adenda (ad4385c), que está en la rama remota claude/housing-price-spain-econometric-95dhj3. La puerta de la fase 4 exige la etiqueta y que su commit esté en la rama remota; la subida de la etiqueta al remoto queda como tarea del autor.

- **Contenido.** Para cada estudio y ampliación: la especificación del original, su traslado a los datos del proyecto, las ampliaciones previstas y las pruebas. Incluye las reglas de inferencia, la clasificación V18, el multiverso enumerado, la estimabilidad por MDE, el sellado temporal y espacial, la magnitud preferida y la contabilidad.
- **Revisión.** Revisor del pre-registro (apto con cambios) y abogado del diablo (resiste con limitaciones). La adenda responde a todos los hallazgos de ambos sin haber mirado ningún resultado de V18; el autor decidió la regla de capas y lenguaje (K2).
- **Sellado de entrenamiento.** docs/v18/sellado_v18.json, generado con solo metadatos después de la etiqueta y antes de la primera estimación.
- **Desviaciones.** Toda desviación respecto al plan está en docs/v18/desviaciones*.md con fecha y motivo.

### B.14 Pruebas por estimación

Las pruebas son las de B4 de cada diseño (pretendencias y potencia de Roth, placebos de fecha y de resultado, Honest DiD, primera etapa y F efectivo, número efectivo de choques, robustez a la exclusión de unidades atípicas y a la medida de precio o alquiler). Madrid, Baleares y Canarias ya están fuera por el sellado de v6, de modo que «sin Madrid» y «sin islas» no cambian la muestra provincial. Los valores completos y los intervalos están en tablas_v18.xlsx (pestañas «estimaciones» y «magnitudes»).

**D.1 Estimaciones con cifra.** «IC incluye el cero» describe el intervalo de la ficha (IC95, salvo indicación). Todas son de capa C4.

| Id | Magnitud y unidad | Estimación | ¿IC incluye el cero? | Clase V18 |
|---|---|---|---|---|
| E1-R3 | Log del alquiler por punto de densidad HUT (estudio de eventos) | 0,00443 | No | ASOCIACIÓN |
| E1-R4 | Log, secciones del radio frente al anillo (Sagrada Família) | 0,00166 | Sí | NO CONCLUYENTE |
| E1-P-H3 | Log del alquiler por desviación típica intra-sección (coprincipal) | −0,000065 | Sí | sin clasificar (coprincipal informativa) |
| E2-R1 | Log de la renta media de contratos nuevos (cifra solo con la frase de limitación de B.2 y del resumen ejecutivo) | −0,038 | No | SUGESTIVO |
| E2-R1c | Log de contratos por 1.000 habitantes | 0,0173 | Sí | ASOCIACIÓN |
| E2-R1-REV | Reversión tras la STC 37/2022 (log de la renta) | −0,00157 | Sí | diagnóstico o variante (sin clase propia) |
| E3-R1 | €/m² por punto de población (IV, Webb-AR) | 3,55 | Sí | NO CONCLUYENTE |
| E5-A1 | Interacción del instrumento de inmigración con solares (Δ ln P) | 0,00244 | Sí | ASOCIACIÓN |
| E7-R1 | % del precio por +100 pb a ocho trimestres (LP-IV); AR no acotado | 1,28 | No aplicable | NO ESTIMABLE |
| E7-R3 | % del precio por +100 pb del euríbor a ocho trimestres (BVAR; banda del 68 %, con un 15 % de extracciones explosivas) | −1,55 | No (banda del 68 %) | ASOCIACIÓN |
| E7-A2 | % del precio por pp de sorpresa y por unidad de exposición (relativo entre provincias, sin el componente común) | −19,7 | No | NO ESTIMABLE |
| E8-R1 | Log del valor tasado a cuatro trimestres por punto del tipo general del ITP | 0,0146 | No (aleatorización) | ASOCIACIÓN |
| E10-A1 | % del alquiler por m² por punto de viviendas de grandes tenedores | 1,07 | Sí | ASOCIACIÓN |
| E12-A1 | Viviendas libres iniciadas por vivienda protegida calificada (IV) | 6,5 | Sí (conjunto AR) | NO ESTIMABLE |
| E12-A2 | % del valor tasado real (variación anual) por cada 100 viviendas protegidas calificadas por 100 del parque (IV) | 22,1 | AR no acotado | ASOCIACIÓN |
| F1-R1 | Elasticidad de impacto, precio frente a renta de los hogares (nacional) | 0,126 | Sí | ASOCIACIÓN |

Los coeficientes de corto plazo de los paneles con PMG (F1-R2-pmg, F2-R1, F3-A2) no se publican: el PMG supone una cointegración que los contrastes no encuentran (anexo B.11).

**D.2 Estimaciones NO ESTIMABLES: la comprobación previa.** Se publica la magnitud mínima detectable (MDE), el F efectivo o el recuento de datos, no el coeficiente.

| Id | Comprobación | Cifra | Clase V18 |
|---|---|---|---|
| E1-R1 | Barrios con el cambio mínimo de stock | 18 | NO ESTIMABLE |
| E1-R2 | F efectivo de la primera etapa | 0,0233 | NO ESTIMABLE |
| E1-A1 | MDE | 0,166 | NO ESTIMABLE |
| E2-A1 | MDE | 0,0408 | NO ESTIMABLE |
| E2-A4 | MDE | 0,0444 | NO ESTIMABLE |
| E3-R2 | MDE (elasticidad) | 2,33 | NO ESTIMABLE |
| E3-A1 | MDE (% por punto) | 10,4 | NO ESTIMABLE |
| E5-R1 | F efectivo de la primera etapa | 0,032 | NO ESTIMABLE |
| E6-R1 | MDE (log) | 0,0623 | NO ESTIMABLE |
| E8-R2 | MDE (log por punto) | 0,0894 | NO ESTIMABLE |
| E9 | Número efectivo de choques (sin pesos) | 6,3 | NO ESTIMABLE |

**D.3 E2-R1: robustez a posteriori (B6).** Los resultados de esta tabla se añadieron después de ver los de E2-R1 y no deciden su clase; su clase propia es «robustez a posteriori».

| Id | Prueba | Estimación | ¿IC incluye el cero? |
|---|---|---|---|
| E2-B6-A | Salto en 2022T2 sobre la extrapolación de la recta de la vigencia | −0,0217 | Sí |
| E2-B6-B | HUT 2019 y ln(población) 2019 por trimestre | −0,0242 | No |
| E2-B6-C | Controles emparejados por el crecimiento previo de la renta | −0,0546 | No |
| E2-B6-D | Diferencias en diferencias sintéticas con controles ponderados | −0,044 | No |
| E2-R1c-v1 | Contratos por hogar inquilino del Censo 2021 | −0,0314 | Sí |


## Anexo C. Reproducciones y fichas bibliográficas

### C.1 Reproducciones

La fase 2 reproduce con el paquete de su autor, y sin datos del proyecto, los estudios que lo tienen abierto. El veredicto es «coincide» (la misma cifra al redondeo publicado, o una diferencia menor que la fijada en el plan y dentro del error), «difiere con explicación» o «difiere sin explicación» (parada). Ninguna reproducción difiere sin explicación. Las tres coinciden:

| Estudio (especificación) | Publicado | Reproducido |
|---|---|---|
| Borusyak, Hull y Jaravel (2022), columna 5 de la tabla 4 del artículo; IC95 con el nulo impuesto | −0,31 (IC95 −0,705 a −0,002) | −0,31 (IC95 −0,706 a −0,0022) |
| Chaves-Fonseca (2026), columna 6 (IV), Madrid | 0,02 (error típico 0,004) | 0,0197 (IC95 0,011 a 0,0283) |
| Mense (2025), columna 3 (IV), Alemania | −0,192 (error típico 0,065) | −0,192 (IC95 −0,318 a −0,0658) |

Los artículos de Chaves-Fonseca y de Mense publican el error típico y no el intervalo; el detalle por columna está en output/v18/reproduccion/*/tabla.csv.

| Estudio | Método reproducido | Veredicto |
|---|---|---|
| Chaves-Fonseca (2026), tabla 2 | IV shift-share (proximidad a atractivos por búsquedas de Google), efectos fijos de barrio y año, errores agrupados por barrio; Madrid, precios | coincide |
| Mense (2025), tabla 3A | IV-2SLS en panel con efectos fijos de región y año, instrumento de lluvia; alquiler | coincide |
| Borusyak, Hull y Jaravel (2022), tabla 4 | IV shift-share a nivel de sector, aplicación de Autor, Dorn y Hanson | coincide; la herramienta (src/v18/reproduccion/bhj_lib.py) queda validada |

Sin reproducción por falta de paquete con datos: Garcia-López et al. (2020), Jofre-Monseny et al. (2023), Monràs y García-Montalvo (2023), González y Ortega (2013), Fack, Gibbons y Manning y Grislain-Letrémy y Trevien (E4), Saiz (2010), Best y Kleven (2018) y Besley et al. (2014), Badarinza y Ramadorai (2018) y Cvijanović y Spaenjers (2021), la literatura de grandes tenedores, Segú (2020; impuesto sobre la vivienda vacía en Francia, otro trabajo que Segú 2018) y Koster y van Ommeren (2019). Baum-Snow y Han (2020) solo tiene código y su paquete completo no cabe en el disco; Asquith, Mast y Reed (2020) solo tiene código, sin datos. Jarociński y Karadi (2020) y Altavilla et al. (2019) aportan series de choques, que se usan como dato.

### C.2 Fichas bibliográficas

La fase 1 fijó los criterios antes de buscar (docs/v18/bib/criterios.md): diseño cuasi experimental o estructural, datos de España o de mercados europeos comparables, y publicación en revista con revisión, documento de banco central o serie reconocida de documentos de trabajo. Se hizo una ficha por estudio, agrupadas por factor (docs/v18/bib/<factor>/), con una tabla de efectos y su unidad. El catálogo está en output/v18/f1/catalogo.csv: 181 fichas, 52 leídas en texto completo, 104 solo por el resumen y 25 sin indicar el grado de lectura; 11 con paquete de replicación. Por el estado de la referencia: 125 VERIFICADA, 45 NO VERIFICADA y 11 DISCREPANTE (detalle por factor en output/v18/f1/informe.md).

Los PDF y los paquetes de replicación están solo en disco, con sha256 en data/bib/CHECKSUMS.sha256, y no se versionan. Al repositorio van la ficha, el enlace, el DOI, la licencia y las notas, con citas breves. Estado: VERIFICADA es DOI comprobado con Crossref o DataCite; el cuartil de Scimago no está verificado (tarea del autor). DISCREPANTE es una ficha de versión de trabajo cuyo DOI corresponde a la versión publicada (otro año o título), y se trata como NO VERIFICADA. No se cita ninguna cifra de la versión publicada sin leerla.

Inmigración (E3). Estudios de España, EE. UU., Reino Unido, Alemania: 5 estudios con error típico en la unidad; método: metaanálisis bayesiano de efectos aleatorios (3 priors); estado B5: rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo).

**Referencias de la magnitud preferida y de la etiqueta I6.**

| Factor | Estudio | Estado de la ficha | ¿Entra en la magnitud preferida? Motivo |
|---|---|---|---|
| E1 | Segú (2018) | NO VERIFICADA | Sí (único estudio) |
| E1 | Garcia-López et al. (2020) | VERIFICADA | No: unidad no convertible (por 100 anuncios en el área estadística básica) |
| E1 | Chaves-Fonseca (2026) | VERIFICADA | No: unidad no convertible (por 100 anuncios, sobre el precio de compra) |
| E1 | Duso et al. (2024) | VERIFICADA | No: unidad no convertible (€/m² por anuncio en un radio) |
| E2 | Jofre-Monseny et al. (2023) | VERIFICADA | Sí |
| E2 | Monràs y García-Montalvo (2023) | VERIFICADA | Sí (peso nulo al contar una vez el episodio compartido) |
| E2 | Breuille et al. (2025) | NO VERIFICADA | Sí |
| E2 | Hahn et al. (2021) | VERIFICADA | Sí |
| E2 | Pérez García (2026) | VERIFICADA | No: otro régimen (zonas de 2024), otra unidad y sin pretendencias paralelas |
| E2 | Abel (2024) | NO VERIFICADA | No: mide la oferta |
| E3 | González y Ortega (IZA, 2009) | NO VERIFICADA | Sí (versión que da la unidad) |
| E3 | González y Ortega (Chicago Fed, 2011) | NO VERIFICADA | No: misma obra; entra en la sensibilidad |
| E3 | Sanchis-Guarner (2017) | DISCREPANTE | Sí |
| E3 | Saiz (2007) | VERIFICADA | Sí |
| E3 | Sá (2015) | VERIFICADA | Sí |
| E3 | Ünal (2022) | NO VERIFICADA | Sí |
| E3 | Accetturo (2012) | DISCREPANTE | No: elasticidad respecto a la población extranjera, no a la total |
| E3 | Torres y Montero (2023) | VERIFICADA | No: sin error típico |
| E4 | Fack (2005) | VERIFICADA | Sí |
| E4 | Eerola et al. (2026) | VERIFICADA | Sí |
| E4 | Kangasharju (2008) | VERIFICADA | No: sin error típico |
| E4 | Hyslop y Rea (2018) | VERIFICADA | No: sin error típico |
| E5 | Taltavull (2006) | NO VERIFICADA | Sí |
| E5 | Baum-Snow y Han (2020, versión de trabajo; publicado en 2024) | DISCREPANTE | Sí |
| E5 | Paciorek (2012) | VERIFICADA | Sí |
| E6 | Mense (2025) | VERIFICADA | Sí (único estudio) |
| E6 | Asquith, Mast y Reed (2020, versión de trabajo; publicado en 2023) | DISCREPANTE | No: otra unidad |
| E7 | San Juan (2023) | VERIFICADA | No: intervalos solo en un gráfico |
| E7 | BCE, Boletín Económico 6/2022 | NO VERIFICADA | No: sin error típico |
| E8 | Dolls et al. (2020) | VERIFICADA | No: sin error típico recuperado |
| E9 | Sá (2016) | VERIFICADA | No: sin error típico extraído |
| E9 | Álvarez, Blanco y García-Posada (2020) | NO VERIFICADA | No: regresión transversal sin instrumento |

Los valores por estudio están en output/v18/f5/magnitudes_estudios.csv y también en cifras_clave, con ids V18-AUX-LIT-* (tabla B.0 del anexo B).


## Anexo D. Fe de erratas

Lo publicado no se reescribe: cada error que cambia una cifra, una capa o un texto difundido se corrige en una versión posterior y se anota en ERRATA.md, con la versión, el fichero, el error, la corrección y la fecha. La tabla siguiente es el índice de esas entradas (fecha, versión y fichero), generado desde ERRATA.md; el texto completo de cada una, con sus cifras, está en ERRATA.md. Los cambios de capa de cifras (siempre bajadas) y las huellas de las cifras cambiadas están al final de ese fichero.

| Fecha | Versión | Fichero |
|---|---|---|
| 2026-10-10 | v2 | output/v2/BA/resultado.json, BV/resultado.json, BM/resultado.json («notas») |
| 2026-10-10 | v1 | src/extract_notariado.py |
| 2026-10-10 | v4 | `data/raw/gva_vut_municipio.csv` |
| 2026-10-11 | v5 | src/v5/b1_run.py (método de identidad de stock de R) |
| 2026-10-11 | v5-v6 | src/v5/cifras_clave.py (`float_format="%.6g"`) |
| 2026-10-11 | v6 | src/v6/m0_run.py (`incasol`) |
| 2026-10-11 | v5 | src/v5/a23_run.py (contratos nuevos de Cataluña y la Comunitat Valenciana, IPVA) |
| 2026-10-11 | v5 | output/v5/informe_tecnico.md (§ déficit 2021-2024) |
| 2026-10-12 | v4-v6.1 | output/v5/cifras_clave.csv (deficit_2124_c1, deficit_2124_c2) y entregables |
| 2026-10-12 | v5-v6.1 | src/v5/a23_run.py (`SERP2IPVA`) |
| 2026-10-12 | v5 | docs/v5/revision_humana.md (cifra 8) |
| 2026-10-12 | v5-v6.2 | src/v5/d2_run.py; output/v5/D2 (D2-H01 a D2-H13) |
| 2026-10-12 | v3 (detectado en V7, R0) | output/v3/C3/resultado.json (H3-3b) |
| 2026-10-12 | v6.3 (propagación detectada en el `make all` de cierre de V7) | output/v5/E/hechos.json y entregables (informe técnico, policy brief) |
| 2026-10-13 | v4-v7.1 | output/v5/cifras_clave.csv (deficit_2124_c1, T3-H1, deficit_2124_c2, T3-H2, T3-H3, T3-H4, L3-DEF-2124-CONBAJAS) |
| 2026-10-13 | v5-v7.1 | output/v5/cifras_clave.csv (B1-H1); output/v5/D3 |
| 2026-10-13 | v7-v7.1 | output/v7/R6 (a_construccion), output/v7_1/S1 y entregables |
| 2026-10-13 | v7-v7.1 | output/v7_1/S1, entregables (f2_impuestos_construccion) |
| 2026-10-16 | V13 (incidencia D3, constatada en V14) | data/sealed (muestra sellada v2, no versionada) |
| 2026-10-17 | 1.0 (antes del depósito; detectado en V15, fase 0) | output/v5/cifras_clave.csv: E-T7-prod, V8-M8-cv-p03-P5-acum-alt, V8-M8-cv-p03-P5-acum-mivau, V8-M8-cv-p12-P5-acum-alt, V8-M8-cv-p12-P5-acum-mivau, VER-A23-V2-1, VER-A23-V2-2, V10-ATL-A1, V10-ATL-A2, V10-ATL-A3, V9-D7-c1-dif |
| 2026-10-17 | V11-1.0 (antes del depósito; detectado en V15, fase 1) | data/base (hechos y variables, `obra_nueva_neta_catastro`); src/v11/base_v11.py |
| 2026-10-17 | V10-1.0 (antes del depósito; detectado en V15, fase 1) | data/base (hechos y variables, `ipc_alquiler_indice`); src/v10/base.py |
| 2026-10-17 | V10-1.0 (antes del depósito; detectado en V15, fase 1) | data/base (hechos y variables, `permisos`); src/v10/base.py |
| 2026-10-18 | V8-1.0 (detectado en V16, alcance de los errores K16: docs/v16/alcance_errores_k16.md, E4) | src/v8/m5_lpiv.py:214-217 (IV3 Bartik); output/v8/M5/atribucion.csv → output/v8/F5/atribucion_combinada.csv → publicacion/tablas_v8.xlsx, hoja «Atribucion», 8 filas IV3_bartik_h1-2 |
| 2026-10-18 | V7.2-1.0 (detectado en V16 por la réplica ciega de las cifras de una_pagina; output/v16/replica/v10_c/reconciliacion.md) | src/v5/r1b_gsadf.py (ar_fit y construir_series; NBOOT); output/v5/R1B (tablas, hechos R1B-G-*), output/v7_2/gsadf (V72-GSADF-*); output/v5/cifras_clave.csv; publicacion/una_pagina.md, lo_que_sabemos.md, policy_brief, que_cambio, working_paper; consulta |
| 2026-10-18 | v6-1.0 (detectado en V16 al delimitar E1; docs/v16/errata_v72_gsadf.md) | src/v6/m1b_lib.py (`ar_fit`, copia con el error E1); output/v6/M1B (hechos, tablas GSADF, registro, multiplicidad, resultado); output/v5/cifras_clave.csv: m1b_gsadf_ccaa_11, _16, _18 y _19 (campo max = valor crítico del 95 %) |
| 2026-10-18 | V8-1.0 (detectado en V16 por la réplica ciega; output/v16/replica/v10_d/reconciliacion.md) | src/v8/f6_hechos.py (H8-9 y QNA-pp de compra P5); output/v5/cifras_clave.csv: V8-H8-9-est y V8-H8-9-pholm (periodo), V8-QNA-pp-c-P5 (rótulo y banda), V8-QNA-pp-c-P5-med y V8-QNA-pp-c-P5-bde (nuevas); docs/v8/desviaciones.md (Y10 y M1) |
| 2026-10-19 | V16-2.0 (informe integral; detectado en la auditoría de V17, parada P1: docs/v17/bloqueos.md) | output/v16/informe/plantilla/03_parte_iii_medidas.md (III.1, III.3, III.8 y III.10) → publicacion/informe_integral/informe_integral.md |
| 2026-10-19 | 1.0 (lo_que_sabemos y verificador; detectado en la auditoría de V17, parada P2: docs/v17/bloqueos.md) | docs/v5/plantillas/lo_que_sabemos.md → publicacion/lo_que_sabemos.md; docs/v5/plantillas/informe_tecnico.md → publicacion/informe_tecnico.md (dos pasajes; el de la AEAT era correcto y no cambia); src/v3/verificador.py y src/v4/verificador.py (ficha V02) → publicacion/verificador/verificador.md |
| 2026-10-19 | V17 (cifras V17 publicadas el mismo día en cifras_clave; detectado en la ronda 1 del abogado del diablo de la auditoría de V17) | output/v17/auditoria/*_hechos.json → output/v17/f5/hechos.json → output/v5/cifras_clave.csv y publicacion/cifras_clave.csv |
| 2026-10-20 | V16-2.0 (informe integral; segunda decisión del autor sobre III.8 tras la tabla completa de traslaciones de la auditoría de V17) | output/v16/informe/plantilla/03_parte_iii_medidas.md (III.8 y III.10) → publicacion/informe_integral/informe_integral.md |
| 2026-10-20 | V17 (cifras V17 de cifras_clave; detectado en la ronda 2 del abogado del diablo de la auditoría de V17 y al aplicar la guarda de fuga v6, decisión del autor del 2026-10-20) | src/v17/d3_cuantitativo.py, src/v17/f3_*.py → output/v17/d3/hechos.json y output/v17/auditoria/*_hechos.json → output/v17/f5/hechos.json → output/v5/cifras_clave.csv |
| 2026-10-20 | V16-2.0 (informe integral; ronda 2 del abogado del diablo de la auditoría de V17, decisión del autor: docs/v17/decisiones.md, K6) | output/v16/informe/plantilla/03_parte_iii_medidas.md (III.1, III.8 y III.10) → publicacion/informe_integral/informe_integral.md, web y consulta |
| 2026-10-20 | V17 (commits 8aa173d a a4a65e2 de la rama de trabajo; detectado al regenerar la publicación tras la ronda 2) | src/v5/render.py, src/v5/cifras_clave.py y src/v10/web.py → docs/v8/plantillas/README.md, output/v8/*.md, output/v5/cifras_clave.md, publicacion/ y web |
| 2026-10-21 | V18 (cifras V18 de cifras_clave, incorporadas el 2026-10-21; detectado por el árbitro y el verificador del Documento de Trabajo, ronda 1; docs/v18/decisiones.md K12) | src/v18/f6_hechos.py, src/v18/f5_contabilidad.py, src/v18/f5_magnitudes.py → output/v18/f6/hechos.json → output/v5/cifras_clave.csv |
| 2026-10-21 | V18 (cifras V18 de cifras_clave; árbitro del Documento de Trabajo, ronda 2; docs/v18/decisiones.md K14) | src/v18/f5_contabilidad.py, src/v18/f6_hechos.py → output/v18/f6/hechos.json → output/v5/cifras_clave.csv |
| 2026-10-23 | V18 (consolidación final, publicación 2.0 preparada; orden del autor; docs/v18/decisiones.md K15) | src/v18/f6_hechos.py → output/v18/f6/hechos.json → output/v5/cifras_clave.csv |


## Anexo E. Pre-registros internos

### E.1 Pre-registro interno y análisis a posteriori

**Qué es pre-registro interno sin sello de tiempo externo.**

- El plan de replicación (commit d4e9869) y su adenda, con la etiqueta git local plan-replicacion-v18 sobre el commit ad4385c, fechada el 2026-10-20. El commit está en la rama remota claude/housing-price-spain-econometric-95dhj3; la etiqueta aún no está en el remoto (tarea del autor).
- No es un pre-registro depositado en un registro externo y no debe describirse como tal. Lo fija solo el historial de git del proyecto.
- Las especificaciones, las variantes enumeradas, las reglas de estimabilidad por MDE, de clasificación y de magnitud preferida, la designación de la estimación propia de cada factor y las hipótesis de la evaluación diferida se fijaron en ese plan y su adenda, antes de la primera estimación de V18 y sin haber mirado ningún resultado.
- Los resultados de V18 se describen siempre como resultados de un pre-registro interno sin sello de tiempo externo, con su etiqueta, su commit y su fecha.

**Qué es a posteriori.**

- *Todo V17.* La auditoría de afirmaciones y medidas, la demografía, el análisis general o local, la factibilidad y las cifras V17-* se hicieron sin pre-registro y se integran aquí como análisis a posteriori de capa C4.
- *La robustez B6 de E2-R1 y E2-R1c.* Se añadió después de ver los resultados, por petición del abogado del diablo (anexo B.14.3). No cambia la especificación principal ni su clase por sí sola.
- *Las desviaciones.* Toda desviación respecto al plan (docs/v18/desviaciones*.md) se declaró con fecha y motivo. Entre ellas: el paro registrado de E2 (una versión anterior de la desviación era errónea y se corrigió); la geometría y la lectura de la ficha de E1-R4 (K8 bis); la lectura restrictiva de la contabilidad (K10); el deflactor del PIB en lugar del IPC; los ocho grupos de origen en E3.
- *Decisiones tomadas tras ver resultados de otras especificaciones.* K7 (clasificación de E8-R1 y E2-R1c tras la ronda 1 del abogado del diablo), K8 y K8 bis (E1-R4), K9 (E2-R1 tras la ronda 2, con su frase de limitación) y K12 (clase propia por especificación y correcciones de esta revisión, sin estimar de nuevo).
- *La estrategia A para extraer la magnitud de Hahn et al. (E2).* Se fijó en la fase 5 (K10), antes de combinar pero después de la etiqueta y de ver E2-R1, por ser la primera de la ficha. Es una decisión a posteriori: con la estrategia B, E2 tendría magnitud preferida (sensibilidad de B5, anexo B.2).
- *Datos descargados después de la etiqueta.* Marcados `posterior_prereg`.
- *La ilustración de la contabilidad* con magnitudes de la literatura.
- *El juicio experto del documento final.* La mejor estimación por factor, su grado de confianza y la contabilidad con magnitudes de la literatura (parte V) se escribieron en la consolidación final, después de conocer todos los resultados. Son juicio experto a posteriori y se rotulan así; no cambian ninguna cifra ni clase.
- *Réplicas del plan sobre preguntas ya vistas.* Las especificaciones que repiten una pregunta cuyo resultado ya se conocía llevan la marca `repite_visto` (plan, 0.2).

**Capa y lenguaje.** Toda cifra V18 es de capa C4 con nivel de evidencia EXPLORATORIO. Ninguna estimación es IDENTIFICADO, de modo que no se usa en ningún lugar la fórmula condicional prevista. El documento no formula ninguna cifra V18 como causa: cada una es una asociación condicionada al diseño. El generador de este documento (src/documento_final/documento_final.py, con el motor de src/v18/f6_documento.py) toma todas las cifras de output/v5/cifras_clave.csv y falla si un marcador no existe.

### E.2 Etiquetas de pre-registro del proyecto

Cada pre-registro es interno: lo fija un commit de la rama de desarrollo y una etiqueta git anotada, sin sello de tiempo externo. La tabla procede de docs/preregistros.md (generado desde git por src/v16/preregistros.py), con la columna que dice si el fichero es igual hoy que en el commit. El plan de replicación de V18 se fijó con la etiqueta local plan-replicacion-v18 (commit ad4385c); su publicación en el remoto es una tarea del autor.

| Etiqueta | Commit | Fecha del commit (UTC) | Publicada como etiqueta (UTC) | Ficheros (sha256 en el commit) | ¿Igual hoy? |
|---|---|---|---|---|---|
| prereg-v2 | 910c42a | 2026-10-10T07:13:42Z | 2026-10-17T17:42:07Z | `docs/v2/hipotesis.md` `3fa640930bd0f645…`<br>`data/processed/v2/train/_sellado.json` `a9a291f9fbef90c9…` | sí<br>no |
| prereg-v3 | 204c073 | 2026-10-10T13:33:09Z | 2026-10-17T17:42:07Z | `docs/v3/hipotesis.md` `ee40f73e5e68482e…` | sí |
| prereg-v5 | 8803f04 | 2026-10-10T19:11:04Z | 2026-10-17T17:42:07Z | `docs/v5/prereg_B3.md` `0b5d09d9f0ca778d…` | sí |
| prereg-v6 | a33c167 | 2026-10-11T08:47:34Z | 2026-10-17T17:42:08Z | `docs/v6/hipotesis.md` `9c5d9333e70fcbb9…`<br>`output/v6/M0/sellado_info.json` `006ff58397b77003…` | sí<br>no |
| prereg-v7 | 3fad305 | 2026-10-12T12:04:36Z | 2026-10-17T17:42:08Z | `docs/v7/hipotesis.md` `e82d61184dcb3d9d…` | sí |
| prereg-v8 | 91e618b | 2026-10-13T08:00:40Z | 2026-10-17T17:42:09Z | `docs/v8/hipotesis.md` `9e7d28dcb2c21763…` | sí |
| prereg-v9 | 2977349 | 2026-10-15T08:22:29Z | 2026-10-17T17:42:09Z | `docs/v9/hipotesis.md` `845269079a46a6d8…` | no |
| prereg-v9-a1 | 9cb2200 | 2026-10-15T08:32:35Z | 2026-10-17T17:42:09Z | `docs/v9/hipotesis_addendum_a1.md` `22d9eadab98fe39a…` | no |
| prereg-v9-a1b | 4639772 | 2026-10-15T08:35:36Z | 2026-10-17T17:42:09Z | `docs/v9/hipotesis_addendum_a1.md` `58a2cb8fd4aabfba…` | sí |
| prereg-v15 | 542b4fd | 2026-10-17T09:24:18Z | 2026-10-17T17:42:07Z | `docs/v15/preregistro_v15.md` `936868be91c66738…`<br>`docs/v15/preregistro_v15_adenda.md` `2df7459c3e99b793…`<br>`docs/v15/sellado_v15.json` `89f5b3da2d77fbed…` | sí<br>sí<br>sí |
| prereg-v16 | a8304ec | 2026-10-17T16:08:21Z | 2026-10-17T17:42:09Z | `docs/v16/preregistro_v16.md` `2bb1e11b5de7fc60…`<br>`docs/v16/preregistro_v16_adenda.md` `b92dd7d2373f9bbb…`<br>`docs/v16/sellado_v16.json` `127785d007898d16…` | sí<br>sí<br>sí |
