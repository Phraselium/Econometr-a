# Por qué se forman más hogares que viviendas (síntesis V9-PREP)

Fecha: 2026-10-14. Síntesis del orquestador a partir de [literatura.csv](literatura.csv) (ids LA/LB), [fuentes_datos.csv](fuentes_datos.csv) (ids F) y de las cifras vigentes del proyecto en `output/v5/cifras_clave.csv` (id entre corchetes, con su capa).

## El hecho de partida

- **Más hogares que viviendas.** Entre 2021 y 2025 el número de hogares aumentó en unos 998.000 [dh_2125, C1]. El déficit contable del mismo periodo está entre 706.000 viviendas sin bajas del parque [L3-DEF-2125, C4] y 735.000 con bajas estimadas [T1-H10, C4].
- **Banco de España.** Su Informe Anual 2025 da un orden de magnitud parecido: un déficit acumulado de unas 750.000 viviendas en 2021-2025, el 3,7 % de los hogares. Solo en 2025 se crearon 240.000 hogares netos y se terminaron 92.000 viviendas (LA18, informe institucional).
- **OCDE.** El Economic Survey 2025 citaría unas 600.000 para 2022-2025 (LA21). Esa cifra viene de un resumen de buscador y no se ha contrastado con el PDF (403).
- **Las cifras no son comparables entre sí.** Los periodos, las fuentes de hogares (ECP o EPA) y el tratamiento de las bajas difieren.
- **Hacia delante.** El INE proyecta 1,72 millones de hogares más en 2026-2035 [B1-H4, C2]. Mantener constante el déficit en 2026-2030 exigiría unas 212.000 terminaciones al año [T4-H6, C4].

El desajuste es, por tanto, un hecho bien documentado en sus órdenes de magnitud. Lo que sigue repasa **por qué** ocurre, ángulo por ángulo.

## 1. Crecimiento de la población e inmigración

- **Qué dice la literatura.**
  - **España, años 2000.** La inmigración elevó la población en edad de trabajar un 1,5 % anual en 2000-2010. Explica alrededor de un cuarto de la subida de precios y la mitad de la construcción de esa década (González y Ortega 2013, LA08, Q1). Estas cifras son del resumen publicado; docs/literatura.md recogía cifras de la versión de trabajo y conviene corregirlas.
  - **Descomposición del efecto.** Sanchis-Guarner (2023, LA07, Q1) separa el efecto directo de la demanda de inmigrantes del efecto inducido por la reubicación de los nativos. Ignorar la reubicación altera sustancialmente el efecto total; la magnitud exacta está pendiente de leer en el texto.
  - **Signos opuestos.** Torres-Téllez y Montero-Soler (2023, LA26) encuentran un efecto positivo en la burbuja, negativo tras la crisis y neto negativo en 2001-2019. En el Reino Unido, Sá (2015, LA34) halla un efecto negativo por la salida de nativos de mayor renta.
  - **Alquiler.** Los informes del Banco de España sitúan el dinamismo demográfico y la concentración urbana como el principal motor del alquiler desde 2015, con la expansión concentrada en jóvenes y en población de origen extranjero (LA20, LA19).
- **Qué dice el proyecto.**
  - En V8, la descomposición del SVAR no identifica el shock demográfico como dominante en ningún periodo [C3s, bandas con el cero].
  - El empuje migratorio como instrumento es débil [V8-H8-7-F, C4].
  - La asociación robusta del multiverso es la de la demografía con el alquiler en la crisis y en la muestra completa [C4].
- **Qué falta.**
  - Flujos por nacionalidad y destino a nivel municipal o de sección: el censo anual del INE por sección (F01), donde la nacionalidad por sección no está confirmada.
  - Una réplica de la descomposición de Sanchis-Guarner con datos 2015-2025 (plan_v9, diseño 1).

## 2. Tamaño del hogar, envejecimiento, hogares unipersonales y separaciones

- **Qué dice la literatura.**
  - El tamaño medio del hogar sigue cayendo. Una parte creciente de los hogares nuevos es de una sola persona, por envejecimiento, viudedad y separaciones.
  - Módenes, Marcos y García-García (2024, LA28, Q3) estiman la «nueva demanda demográfica» en España a partir de la composición por edad. González-Val (2022, LA29) relaciona precios y nupcialidad en España, donde los precios altos retrasan la formación de parejas.
  - No hay en la muestra un estudio revisado que cuantifique la contribución de la fragmentación del hogar al desajuste reciente.
- **Qué dice el proyecto.**
  - Las viviendas que libera el envejecimiento (1,4 millones en diez años [B1-H8, C4]) **no se restan** de la necesidad, porque la proyección de hogares del INE ya las descuenta (regla v5.1).
  - El crecimiento de hogares de la proyección ya incorpora la caída del tamaño del hogar.
- **Qué falta.**
  - Desagregar el crecimiento de hogares de 2021-2025 en efecto población y efecto tamaño (tasas de jefatura por edad). Se puede hacer con la ECP, la EPA y el censo, y es una descomposición contable barata (C1/C4).

## 3. Emancipación y demanda latente

- **Qué dice la literatura.**
  - Soler Montero, Torres-Téllez y García Ayala (2023, LA27, Q2) vinculan la emancipación juvenil al coste de la vivienda en España.
  - La Renta Básica de Emancipación elevó la emancipación de los jóvenes elegibles entre 0,9 y 2,3 puntos (Aparicio-Fenoll y Oppedisano 2015, LB16; mide la emancipación, no los alquileres).
  - No se ha localizado ninguna evaluación empírica del Bono Alquiler Joven (laguna LB23).
- **Qué dice el proyecto.**
  - La emancipación retrasada suma unas 315.000 viviendas al atraso a absorber [E-B1-A2, C4].
  - El 14,7 % de los hogares jóvenes vive en vivienda cedida [CC-C7b-jov-cesion, C4].
  - Es demanda latente: no aparece en la creación de hogares observada, pero sí en la necesidad.
- **Qué falta.**
  - Tasas de emancipación por edad y territorio (EPA y ECV microdatos, F29; EFF, F30).
  - Una evaluación por discontinuidad de edad del Bono Alquiler Joven (plan_v9, diseño 4).

## 4. Caída estructural de la construcción desde 2008

- **Qué dice la literatura.**
  - Tras la crisis, la oferta se recuperó más despacio que la demanda; los precios subieron más donde la escasez relativa es mayor (San Juan 2023, LA16).
  - El Banco de España estima una elasticidad de largo plazo de la oferta de en torno a 0,45 (LA18).
  - En comparación internacional, la elasticidad de la oferta en España es moderada (Caldera y Johansson 2013, LA32, Q2). La regulación y la geografía la reducen (Saiz 2010, LA10; Glaeser y Gyourko 2018, LA11).
- **Qué dice el proyecto.**
  - Producción actual frente a necesidad [T3-H9, C4]: la necesidad decenal equivale a unas 2,7 veces la producción media de 2019-2024.
  - Retardo medio entre iniciadas y terminadas: 3,2 años [B2-H5, C4].
  - El déficit empeora hasta 2030 en 20 provincias [E-B2-empeora, C4].
- **Qué falta.**
  - Licencias y visados municipales (SIU, F24; estadísticas de edificación del Ministerio, F38).
  - Catastro INSPIRE para medir el parque real por edificio (F23).

## 5. Suelo, licencias, costes, mano de obra y crédito a promotores

- **Qué dice la literatura.**
  - La economía política local condiciona la oferta de suelo en España (Solé-Ollé y Viladecans-Marsal 2012, LA31, Q1).
  - Koumpias, Martínez-Vázquez y Sanz-Arcega (2021, LA30) relacionan burbujas y recalificación de suelo.
  - La OCDE (LA21) señala plazos de licencia de hasta dos años (sin verificar en el original).
  - Sobre los costes de construcción, la falta de mano de obra y el crédito a promotores, la muestra solo tiene informes institucionales, sin estudio revisado específico para 2020-2026.
- **Qué dice el proyecto.**
  - V8 incluye el crédito y los costes como controles, pero no identifica su efecto.
  - El crédito a promotores no está en los paneles.
- **Qué falta.**
  - Plazos de licencia municipales (SIU, F24; ayuntamientos).
  - Índice de costes de construcción por provincia (Ministerio).
  - Crédito nuevo a promotores (Banco de España, Boletín Estadístico).

## 6. Vivienda protegida y descalificación

- **Qué dice la literatura.**
  - El parque de alquiler social ronda el 3 % del total en España, frente a medias europeas mucho mayores (OCDE, LA21, cifra pendiente de contraste).
  - En Viena, una mayor cuota de vivienda social se asocia con alquileres privados menores (Banabak 2023, LB27, observacional).
  - En Londres, la regeneración de vivienda pública eleva precios y alquileres cercanos (Blanco y Neri 2025, LB26).
  - No hay estudio español sobre la descalificación de la vivienda protegida, que retira viviendas del parque asequible sin cambiar el total.
- **Qué dice el proyecto.** La vivienda protegida se cuenta dentro de las terminadas [T1-H10]; la descalificación no se mide.
- **Qué falta.** Registros autonómicos de calificación y descalificación (GVA, otras comunidades); no localizados como datos abiertos.

## 7. Conversión a uso turístico o de temporada

- **Qué dice la literatura.**
  - En Barcelona, Airbnb eleva los alquileres un 1,9 % y los precios un 4,6 % en los barrios con más actividad (García-López et al. 2020, LA01, Q1).
  - En Madrid, 100 anuncios más de vivienda entera se asocian con unas 50 entradas residenciales menos al año y precios un 2 % más altos (Chaves-Fonseca 2026, LA02, Q2).
  - En San Sebastián los efectos son mayores (LA03).
  - En la Comunitat Valenciana solo hay un estudio descriptivo (LA05) y cifras de prensa sin verificar (LA35).
  - La regulación de Barcelona redujo a la mitad los anuncios previstos (Gyódi et al. 2025, LB30).
  - El alquiler de temporada y por habitaciones no tiene literatura académica: solo datos de portales y prensa.
- **Qué dice el proyecto.**
  - Las viviendas turísticas desplazan como máximo el 2,75 % del stock de alquiler [B4-v3-vut-cantidad, C2].
  - En España hay 341.001 viviendas turísticas [VER-M4-V3-3, C4].
  - La asociación con el alquiler SERPAVI no se distingue de cero [m1a_*, C4].
  - En V8 el turismo solo aparece en una sensibilidad de aprendizaje automático, sin lectura causal.
- **Qué falta.**
  - Cruzar Inside Airbnb (F14) y el INE VUT por sección (F02) con el censo por sección (F01) y las fianzas de la GVA (F05) en València (plan_v9, diseño 2).
  - Los contratos de temporada no se registran de forma separada en las fianzas: dato que pedir a la GVA.

## 8. Viviendas vacías

- **Qué dice la literatura.** El impuesto francés a la vivienda vacía la redujo un 13 % (Segú 2020, LB28), sin efecto medido sobre precios.
- **Qué dice el proyecto.**
  - Hay 3,8 millones de viviendas vacías por consumo eléctrico en el Censo 2021 [VER-M4-V3-1, C4].
  - Las vacías movilizables en zonas con presión cubrirían entre el 31 % y el 76 % de la necesidad según la clase [E-E1-D2-covvac-*, C4].
- **Qué falta.** La vacía de larga duración por sección: el Censo 2021 (F35) da un corte transversal; hay que actualizarlo con el consumo eléctrico de las distribuidoras, que no es público.

## 9. Geografía del desajuste

- **Qué dice la literatura.**
  - El déficit se concentra en las grandes áreas urbanas: casi un tercio en Madrid y Barcelona (Banco de España, LA19).
  - Los precios de las ciudades españolas convergieron hasta 2009 y divergen después (Ghirelli, Leiva-León y Urtasun 2023, LA22, Q2).
- **Qué dice el proyecto.**
  - Seis provincias suman la mitad del déficit positivo [A4-conc50-2021-2025, C4].
  - El déficit contable 2021-2025 de la provincia de Valencia es de unas 69.000 viviendas y el de València ciudad de unas 13.000 [E-E1-VLC-def2125, E-E1-VLC-defciu, C4].
- **Qué falta.**
  - Afiliación a la Seguridad Social por municipio (F21), para separar el empleo de la población.
  - Movilidad residencial intramunicipal (padrón por sección).

## Conclusión

Los ángulos no se excluyen.

- **Lo más respaldado.** Con la evidencia revisada disponible, la combinación con más respaldo es una demanda demográfica alta, impulsada por la inmigración y la caída del tamaño del hogar, frente a una oferta que no se recuperó tras 2008.
  - La conversión a uso turístico tiene efectos medibles en los barrios centrales de las ciudades con más actividad, pero pequeños sobre el stock total.
  - La vivienda vacía es un stock grande, de movilización incierta.
- **Lo que no tiene evidencia revisada para España en 2020-2026.**
  - El peso relativo de cada ángulo.
  - El efecto de la descalificación, del alquiler de temporada y de los plazos de licencia.

Eso es lo que v9 podría medir con los datos públicos del bloque 1.
