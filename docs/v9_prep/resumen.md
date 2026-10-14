# Resumen V9-PREP: base documental para un v9 con datos nuevos

2026-10-14. 38 fuentes, 64 referencias y 23 métodos (125 entradas); sin estimaciones nuevas. Ids de literatura.csv, fuentes_datos.csv y metodos.csv.

## Hallazgos clave de la literatura, por factor

- **Pisos turísticos.**
  - Efectos locales medibles en barrios muy turísticos:
    - Barcelona: +1,9 % en alquileres y +4,6 % en precios (García-López et al. 2020, LA01, Q1).
    - Madrid: +2 % en precios por cada 100 anuncios, y unas 50 entradas residenciales menos al año (Chaves-Fonseca 2026, LA02, Q2).
  - Comunitat Valenciana: solo un estudio descriptivo. El proyecto acota el desplazamiento agregado en un 2,75 % del stock de alquiler como máximo (C2): diferencia de escala, no de signo.
- **Inmigración y demografía.**
  - En España, en 2000-2010, la inmigración explica alrededor de un cuarto de la subida de precios y la mitad de la construcción (González y Ortega 2013, LA08, Q1; cifras del resumen publicado, distintas de las de docs/literatura.md).
  - El signo cambia con el periodo y la escala: es neto negativo en 2001-2019 según LA26 y negativo en el Reino Unido (LA34), por la reubicación de nativos que Sanchis-Guarner (2023, LA07) separa.
- **Hogares y emancipación.**
  - El Banco de España sitúa el déficit en unas 750.000 viviendas en 2021-2025. En 2025 se crearon 240.000 hogares netos y se terminaron 92.000 viviendas (LA18).
  - La Renta Básica de Emancipación elevó la emancipación de los jóvenes elegibles entre 0,9 y 2,3 puntos (LB16).
  - No hay evaluación del Bono Alquiler Joven.
- **Oferta y suelo.**
  - Elasticidad de largo plazo de en torno a 0,45 (BdE, LA18). La oferta es moderadamente elástica en comparación internacional (LA32).
- **Crédito, tipos y expectativas.** Los modelos estadounidenses priorizan las creencias (LA12); los estudios del boom español, el crédito (LA15, LA33).
- **Inversores institucionales.** El signo sobre los alquileres se contradice: baja con REIT multifamiliares (LB06) y sube con compradores unifamiliares en EE. UU. (LB07, LB09). En España el peso institucional es bajo (BdE).
- **Compradores extranjeros.** Los precios suben en el Reino Unido (LB11) y el efecto es pequeño en París (LB13).
- **Regulación del alquiler.**
  - Cataluña 2020: alquiler −4 % a −6 % sin caída de los contratos (LB01, Q1).
  - San Francisco: oferta −15 % (LB02, Q1).
  - Fedea 2026, descriptivo: anuncios −20,5 % en Cataluña (LB03).
  - Discrepan medida de oferta, horizonte y ley; no hay evaluación del BdE ni de la AIReF.
- **Ayudas a la demanda.** La capitalización va de 60-78 céntimos por euro (Francia, LB17; Finlandia, LB19) a prácticamente cero en los escalones finlandeses (LB20, LB21); difieren el diseño de la reforma y la elasticidad de la oferta.
- **Vivienda pública.** Solo hay evidencia extranjera (LB25-LB27), sin estudio español.
- **Vivienda vacía.** El impuesto francés redujo la vacante un 13 % (LB28), sin efecto medido sobre precios. No hay evaluación del recargo español del IBI.
- **Factor común europeo.** Las ciudades españolas convergen hasta 2009 y divergen después (LA22). No se ha verificado ningún estudio de un factor común europeo en 2018-2026. El proyecto halla una asociación con la zona euro (C4).

## Qué es replicable con datos públicos (plan_v9.md)

1. **Zonas tensionadas.** DiD escalonado con Honest DiD sobre las fianzas del Incasòl, SERPAVI y el IPVA. Es el diseño de mayor valor: resuelve la principal contradicción.
2. **Pisos turísticos en València por sección.** INE VUT, censo anual, registro de la GVA e Inside Airbnb (este último solo como robustez).
3. **Réplica de Sanchis-Guarner con 2015-2025** por municipio, con diagnósticos de shift-share.
4. **Bono Alquiler Joven** por discontinuidad de edad en la ECV (muestra pequeña).
5. **Reconciliación del déficit y descomposición del crecimiento de hogares**: barata y contable.

## Qué no es replicable hoy

Diseños con microdatos privados o restringidos (contratos individuales, propiedad registral, grandes tenedores), alquiler de temporada y por habitaciones, expectativas de precios y capitalización individual de ayudas.

## Fuentes de datos

- Prioridad alta: censo anual por sección (F01), INE VUT (F02), IPVA (F03), SERPAVI (F04), fianzas de la GVA (F05), Eurostat plataformas NUTS3 (F12), Ajuntament de València (F18-F19), registro turístico de la GVA (F20) y proyección de hogares, padrón y renta (F31-F33).
- Solo Cataluña, la Comunitat Valenciana y Euskadi publican fianzas.
- Discrepancias con docs del proyecto (sin modificarlos): licencia del Incasòl («términos de uso»), microdatos de la EFF 2022 ya disponibles y licencia del INE (CC BY-SA en el pie, CC BY en el icono).

## Límites de esta revisión

- Scimago devolvió 403: los cuartiles vienen de agregadores o de docs/literatura.md, con su fuente; 24 entradas no tienen cuartil (sobre todo informes y documentos de trabajo).
- Varias magnitudes están pendientes de leer en el texto completo: Sanchis-Guarner, OCDE 2025 y algunas del Banco de España.
- docs/literatura.md no se modifica; las correcciones propuestas están en literatura.md.
