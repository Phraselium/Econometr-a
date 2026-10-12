# Vivienda en España: lo que sabemos y lo que no (v5)

Actualización de output/v4/lo_que_sabemos.md con las salidas de v5. Cada afirmación lleva su capa:
- **C1**: hecho con al menos dos fuentes independientes, con todos sus componentes en C1.
- **C2**: cota con supuestos explícitos.
- **C4**: exploratorio o de fuente única.

**Cómo citar estas cifras (revisión por pares simulada).**

- Dé el rango antes que el valor central. Los rangos [C1] son el mínimo y el máximo entre combinaciones de fuentes, no intervalos de confianza.
- El precio de compra se cita con las dos medidas juntas: el núcleo de registros y el índice oficial.
- Las cotas y las direcciones [C2] valen dentro de la rejilla de escenarios definida por el autor. Cite la rejilla junto con la conclusión.
- Solo es citable la versión vigente. Las cifras de versiones anteriores se sustituyeron por nuevas fuentes, muestras o correcciones, y el motivo de cada cambio consta en el historial de conclusiones y en la fe de erratas.
- [C4] no indica baja calidad: incluye estadísticas oficiales de fuente única y resultados exploratorios.

La capa de un hecho es la menor de las de sus componentes. Ningún resultado alcanza la capa de identificación causal.

## Afirmable con seguridad

**Hogares y viviendas**
- [C1] Entre 2021 y 2025 los hogares aumentaron en {{dh_2125:cita}}.
- [C2] En 2021-2024 los hogares crecieron más que las viviendas terminadas: balance entre {{L3-DEF-2124-SINBAJAS:min}} y {{L3-DEF-2124-SINBAJAS:max}} ({{L3-DEF-2124-SINBAJAS:periodo}}; {{L3-DEF-2124-SINBAJAS:fuentes}}; dato de {{L3-DEF-2124-SINBAJAS:fecha_dato}}; {{L3-DEF-2124-SINBAJAS:capa}}). Que es positivo lo confirman dos fuentes; la cuantía es una cota porque depende de la corrección del salto de la EPA en 2021.
- [C1] Viviendas terminadas al año en el territorio común: {{terminadas_1924:rango}} ({{terminadas_1924:periodo}}; {{terminadas_1924:fuentes}}; dato de {{terminadas_1924:fecha_dato}}; {{terminadas_1924:capa}}).
- [C2] Demanda latente de los jóvenes por convivencia con los padres, frente a 2008: {{latente_convivencia:rango}} ({{latente_convivencia:periodo}}; {{latente_convivencia:fuentes}}; dato de {{latente_convivencia:fecha_dato}}; {{latente_convivencia:capa}}).
- [C2] Hasta 2030 el déficit nacional empeora en todos los escenarios de la rejilla, incluido uno de construcción optimista ({{T4-H3:periodo}}; {{T4-H3:capa}}). Por provincias: {{T4-H3:valor}} empeoran, {{T4-H3:min}} mejoran y {{T4-H3:max}} quedan indeterminadas.
- [C2] Crecimiento de hogares proyectado por el INE para 2026-2035: {{E-B1-F:cita}}; para 2026-2030: {{B2-H3}} ({{B2-H3:periodo}}; INE; dato de {{B2-H3:fecha_dato}}; {{B2-H3:capa}}).

**Precios y alquileres**
- [C1] Precio de compra, núcleo Ministerio-Notariado-Registradores: {{A23-P2:cita}}.
- [C1] Alquiler de los contratos vigentes (IPC de alquiler e IPVA): {{A23-A2:rango}} ({{A23-A2:periodo}}; {{A23-A2:fuentes}}; dato de {{A23-A2:fecha_dato}}; {{A23-A2:capa}}).
- [C1] Alquiler de los contratos nuevos, con dos fuentes por comunidad: Cataluña {{A23-A9:cita}}; Comunitat Valenciana {{A23-A10:cita}}.

**Tenencia**
- [C1] Hogares con vivienda principal en propiedad: {{R1C-001:cita}}.

**Cotas que se mantienen**
- [C2] El aumento de viviendas turísticas entre 2020 y 2024 equivale como máximo a {{B4-v3-vut-cantidad:cita}}.

## Probable pero no demostrado (C4)

- [C4] Con las bajas del parque estimadas, el balance 2021-2024 llega como máximo a {{T3-H2:max}} ({{T3-H2:periodo}}). Sustituye a la cota anterior, que suponía unas bajas que nada observado respalda.
- [C4] Necesidad de vivienda 2026-2035, suma de provincias (base): {{T3-H5b}}. Si una parte de las viviendas liberadas no llega al mercado, la necesidad efectiva sube a {{T3-H5}}. El supuesto que más pesa en el rango es la fracción de vacías movilizables ({{E-T7-peso-M}} de la amplitud). Equivale a {{T3-H9:min}}, {{T3-H9:valor}} y {{T3-H9:max}} la producción actual ({{E-T7-prod:rango}} terminadas en {{E-T7-prod:periodo}}, con la misma cobertura).
- [C4] Viviendas liberadas por envejecimiento en 2026-2035: {{T2-H1}}; llegan al mercado {{T2-H6:num}} viviendas al año. Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares.
- [C4] Cuánto empeora el déficit de 2025 a 2030: {{T4-H2}}. A 2035 la dirección es indeterminada: el envejecimiento libera más viviendas en 2031-2035 ({{T4-H8:valor}}) que en 2026-2030 ({{T4-H8:min}}).
- [C4] Bajas del parque: las identidades de stock no las miden (dan bajas negativas), y las demoliciones con licencia son {{E-T7-demol-2024:rango}} en 2024.
- [C4] Déficit nacional a fin de 2030: {{T4-H1}} según la rejilla de escenarios (mínimo, ritmo actual y máximo).
- [C4] Contratos nuevos frente a vigentes: la brecha en el IPVA es de {{A23-A6}} en 2024, con fuente única.
- [C4] Las cuatro fuentes de precio comparten un factor común que recoge {{A23-P10:valor}} de la varianza; el IPV del INE acumula {{A23-P1}} en 2015-2025.
- [C4] Compraventas con comprador extranjero en 2025: {{compradores_extranjeros}}; no residentes: {{compradores_no_residentes}}.
- [C4] Compraventas con comprador persona jurídica en 2024: {{R1C-004:valor}}.
- [C4] La parte de una ayuda general que se traslada al precio, por clase territorial (A4, método A, rejilla de elasticidades de demanda): clase `1`, falta y es rentable, {{D1-H11:rango}}; clase `2`, la oferta no responde, {{D1-H12:rango}}; clase `3`, no rentable, {{D1-H13:rango}} [C4]. El extremo bajo se apoya en la literatura con oferta elástica (Eriksen y Ross, 2015) y el alto en la de oferta rígida (Gibbons y Manning, 2006; Hilber y Turner, 2014).
- [C4] En Europa (Eurostat): tenencia en propiedad en España de {{CA-EU-propiedad-nivel:num}} % de la población en 2025, dentro del rango intercuartílico de la Unión Europea; precio real de la vivienda {{CA-EU-hpi_real-crecimiento:valor}}.
- [C4] Crédito a construcción y actividades inmobiliarias: {{CA-CR-saldo-caida}} desde su máximo de 2008.
- [C4] (v6) En provincias que los modelos no vieron, los árboles predicen el alquiler de stock con menos error que la persistencia: {{V6-M4-RMSE-alq_provincia:num}} % frente a {{V6-M4-PERS-alq_provincia:num}} % en la provincia (SERPAVI, último año disponible). En el precio de compra (valor tasado) provincial: {{V6-M4-RMSE-PROV_PRECIO_ANUAL:num}} % frente a {{V6-M4-PERS-PROV_PRECIO_ANUAL:num}} %. Frente a la línea base más exigente (un AR con factor común), la ventaja se mantiene en el alquiler, pero en el precio provincial anual es frágil. Predecir mejor no dice por qué sube el precio.
- [C4] (v6) La población se asocia con el alquiler y con la compra; el PIB por habitante, con la compra y no con el alquiler (probabilidad de inclusión {{m2_pip_cp_ln_pib_pc:num}} frente a {{m2_pip_alq_ln_pib_pc:num}}). En la población extranjera y en las viviendas iniciadas los métodos discrepan; la asociación de las iniciadas con el alquiler no indica que construir suba el alquiler (el orden temporal con el crecimiento del alquiler no se distingue de cero, C4).
- [C4] (v6) Precio y alquiler se mueven juntos: elasticidad de {{m1b_elasticidad_anual_FE_unidad_tendencia:num}} a {{m1b_elasticidad_trimestral_DOLS_FE_unidad_tendencia:num}} según la especificación (asociación). La ratio precio/alquiler mediana bajó de {{m1b_ratio_precio_alquiler_mediana_2015:num}} a {{m1b_ratio_precio_alquiler_mediana:num}} años de alquiler entre {{m1b_ratio_precio_alquiler_mediana_2015:periodo}} y {{m1b_ratio_precio_alquiler_mediana:periodo}}, y el GSADF no detecta exuberancia en ninguna de las {{E-V6-M1B-GSADF-TOT:num}} CCAA contrastadas.

## No se puede afirmar con estos datos

- Qué parte del stock y del alquiler está en manos de empresas o grandes tenedores: no hay datos de titularidad (solicitudes S1, S3 y S4).
- El coste de construcción en nivel: no hay fuente verificable (S5). La clasificación territorial queda en C4.
- Que alguno de estos factores sea la causa principal de la subida: turísticos, inmigración, falta de oferta, tipos, compradores extranjeros o empresas.
- Que los topes al alquiler reduzcan los precios o la oferta: su resultado queda en C4.
- Que haya una burbuja: la exuberancia estadística no la identifica.
- Que la inmigración suba o baje los precios o el alquiler. Hay especificaciones con intervalos que excluyen el cero y otras que no. El signo cambia con el control de población, la medida de precio, el método y el nivel territorial, y ninguna especificación aislada es la de referencia. Todo queda en C4, sin lectura causal.
- (v6) Que alguna variable sea «relevante con seguridad» para el alquiler o la compra: ninguna cumple los criterios pre-registrados y ninguna hipótesis confirmatoria pasa Holm. Las importancias de los modelos de predicción describen qué variables ayudan a predecir, no qué pasaría si una variable cambiara.
- (v6) Que los modelos de aprendizaje profundo predigan mejor que el gradient boosting, o que algún modelo bata a la inercia en el volumen trimestral de compraventas del último año: no lo hacen.
- El resultado de bajar impuestos a la compra o a la construcción, de la seguridad jurídica frente a la ocupación ilegal o de limitar compras de no residentes: no hay diseño ni datos.

## Qué cambió entre versiones y por qué (v6.1)

- [C4] **Inmigración.** v2 la asociaba más con el alquiler y v6 con la compra. El orden depende del método, de la medida de alquiler y de los controles, no de un resultado estable que se haya invertido.
  - Con valor tasado, la asociación de la cuota de extranjeros es {{K2-CUOTA-COMPRA-SINPOB-SIN:valor}} sin población ni controles de demanda externa.
  - Baja a {{K2-CUOTA-COMPRA-SINPOB-EXT:valor}} con controles de costa y demanda externa.
  - Pasa a {{K2-CUOTA-COMPRA-SIN:valor}} controlando por población, que puede ser mediadora.
  - «ANALIZADA, NO CONCLUYENTE»: no se puede afirmar un efecto.
- [C4] **Modelos.** Frente a la línea base más exigente, la ventaja predictiva se mantiene en {{K1-N-MEJOR:num}} de las {{K1-N-TAREAS:valor}}: alquiler de stock y precio de tasación, frágil en el anual. Desaparece en el precio municipal, con Registradores y en el volumen anual.
- [C4] **Iniciadas y alquiler.** La asociación es del mismo año. No hay orden temporal detectable, y no indica que construir suba el alquiler.
- **Correcciones** (ERRATA.md): los contratos nuevos de la Comunitat Valenciana pasan a {{A23-A10:valor}} ({{A23-A10:rango}}) por un error de ponderación; otros redondeos son menores. Ninguna conclusión cambia.

## Problema y opciones con signo estable

- [C1] Desde 2021 los hogares crecen más que las viviendas terminadas, y el precio de compra y el alquiler suben con varias fuentes.
- [C2] Signo estable en toda la rejilla simulada: movilización de vacías y más construcción donde hay presión. La vivienda pública lo tiene de forma débil (signo no positivo o nulo si desplaza a la promoción privada). Las ayudas a la demanda mejoran al beneficiario como grupo.
- [C4] Signo no estable: topes, regulación de turísticos y traslado al precio de las ayudas a la demanda. La matriz completa está en output/v5/D1/matriz_instrumentos.md y la política por territorio, condicional, en output/v5/D2/politica_territorio.md.

**Pre-registro y versiones.** Las etiquetas git `prereg-v5` (pre-registro de las diferencias entre provincias, `docs/v5/prereg_B3.md`) y `v5.0` se crearon en el repositorio local el 10 de octubre de 2026 y se publicaron en el repositorio remoto el [fecha de publicación: pendiente]. El commit del pre-registro es anterior a cualquier resultado de ese análisis, pero una etiqueta local no es un sello de tiempo externo. Por eso, en versiones futuras el pre-registro se depositará además con sello de tiempo externo (OSF o Zenodo) antes de estimar.
