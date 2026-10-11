# Vivienda en España: lo que sabemos y lo que no (v5)

Actualización de output/v4/lo_que_sabemos.md con las salidas de v5. Cada afirmación lleva su capa:
- **C1**: hecho con al menos dos fuentes independientes, con todos sus componentes en C1.
- **C2**: cota con supuestos explícitos.
- **C4**: exploratorio o de fuente única.

La capa de un hecho es la menor de las de sus componentes. Ningún resultado alcanza la capa de identificación causal.

## Afirmable con seguridad

**Hogares y viviendas**
- [C1] Entre 2021 y 2025 los hogares aumentaron en {{dh_2125:cita}}.
- [C1] En 2021-2024 los hogares crecieron más que las viviendas terminadas: balance de {{deficit_2124_c1:rango}} ({{deficit_2124_c1:periodo}}; {{deficit_2124_c1:fuentes}}; dato de {{deficit_2124_c1:fecha_dato}}; {{deficit_2124_c1:capa}}).
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

## No se puede afirmar con estos datos

- Qué parte del stock y del alquiler está en manos de empresas o grandes tenedores: no hay datos de titularidad (solicitudes S1, S3 y S4).
- El coste de construcción en nivel: no hay fuente verificable (S5). La clasificación territorial queda en C4.
- Que alguno de estos factores sea la causa principal de la subida: turísticos, inmigración, falta de oferta, tipos, compradores extranjeros o empresas.
- Que los topes al alquiler reduzcan los precios o la oferta: su resultado queda en C4.
- Que haya una burbuja: la exuberancia estadística no la identifica.
- El resultado de bajar impuestos a la compra o a la construcción, de la seguridad jurídica frente a la ocupación ilegal o de limitar compras de no residentes: no hay diseño ni datos.

## Problema y opciones con signo estable

- [C1] Desde 2021 los hogares crecen más que las viviendas terminadas, y el precio de compra y el alquiler suben con varias fuentes.
- [C2] Signo estable en toda la rejilla simulada: movilización de vacías y más construcción donde hay presión. La vivienda pública lo tiene de forma débil (signo no positivo o nulo si desplaza a la promoción privada). Las ayudas a la demanda mejoran al beneficiario como grupo.
- [C4] Signo no estable: topes, regulación de turísticos y traslado al precio de las ayudas a la demanda. La matriz completa está en output/v5/D1/matriz_instrumentos.md y la política por territorio, condicional, en output/v5/D2/politica_territorio.md.

**Pre-registro y versiones.** Las etiquetas git `prereg-v5` (pre-registro de las diferencias entre provincias, `docs/v5/prereg_B3.md`) y `v5.0` se crearon en el repositorio local el 10 de octubre de 2026 y se publicaron en el repositorio remoto el [fecha de publicación: pendiente]. El commit del pre-registro es anterior a cualquier resultado de ese análisis, pero una etiqueta local no es un sello de tiempo externo. Por eso, en versiones futuras el pre-registro se depositará además con sello de tiempo externo (OSF o Zenodo) antes de estimar.
