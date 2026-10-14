# Resumen V9-PREP: base documental para un v9 con datos nuevos

Fecha: 2026-10-14. Base: 38 fuentes de datos, 64 referencias y 23 métodos (125 entradas). Ninguna estimación nueva. Ids de [literatura.csv](literatura.csv), [fuentes_datos.csv](fuentes_datos.csv) y [metodos.csv](metodos.csv).

## Hallazgos clave de la literatura, por factor

- **Pisos turísticos.**
  - Efectos locales medibles en barrios muy turísticos:
    - Barcelona: +1,9 % en alquileres y +4,6 % en precios (García-López et al. 2020, LA01, Q1).
    - Madrid: +2 % en precios por cada 100 anuncios, y unas 50 entradas residenciales menos al año (Chaves-Fonseca 2026, LA02, Q2).
  - En la Comunitat Valenciana solo hay un estudio descriptivo y cifras de prensa sin verificar.
  - El proyecto acota el desplazamiento agregado en un máximo del 2,75 % del stock de alquiler (C2). La diferencia es de escala, no de signo.
- **Inmigración y demografía.**
  - En España, en 2000-2010, la inmigración explica alrededor de un cuarto de la subida de precios y la mitad de la construcción (González y Ortega 2013, LA08, Q1; cifras del resumen publicado, distintas de las de docs/literatura.md).
  - El signo cambia con el periodo y la escala: es neto negativo en 2001-2019 según LA26 y negativo en el Reino Unido (LA34), por la reubicación de nativos que Sanchis-Guarner (2023, LA07) separa.
- **Hogares y emancipación.**
  - El Banco de España sitúa el déficit en unas 750.000 viviendas en 2021-2025. En 2025 se crearon 240.000 hogares netos y se terminaron 92.000 viviendas (LA18).
  - La Renta Básica de Emancipación elevó la emancipación de los jóvenes elegibles entre 0,9 y 2,3 puntos (LB16).
  - No hay evaluación del Bono Alquiler Joven.
- **Oferta y suelo.**
  - Elasticidad de largo plazo de en torno a 0,45 (BdE, LA18). La oferta es moderadamente elástica en comparación internacional (LA32).
  - La economía política local frena el suelo (LA31).
- **Crédito, tipos y expectativas.** Los modelos estadounidenses priorizan las creencias (LA12); los estudios del boom español, el crédito (LA15, LA33).
- **Burbujas.** Los contrastes de exuberancia (LA13, LA14) ya están replicados en el proyecto (v5 y v7.2).
- **Inversores institucionales.** El signo sobre los alquileres se contradice: baja con REIT multifamiliares (LB06) y sube con compradores unifamiliares en EE. UU. (LB07, LB09). En España el peso institucional es bajo (BdE).
- **Compradores extranjeros.** Los precios suben en el Reino Unido (LB11) y el efecto es pequeño en París (LB13). Hay una prima de unos 38.000 euros en el umbral del golden visa portugués (LB15, documento de trabajo).
- **Regulación del alquiler.**
  - Cataluña 2020: alquiler −4 % a −6 % sin caída de los contratos (LB01, Q1).
  - San Francisco: oferta −15 % (LB02, Q1).
  - Fedea 2026, descriptivo: anuncios −20,5 % en Cataluña (LB03).
  - Discrepan las medidas de oferta, el horizonte y la ley evaluada.
  - No hay evaluación del Banco de España ni de la AIReF de la Ley 12/2023.
- **Ayudas a la demanda.** La capitalización va de 60-78 céntimos por euro (Francia, Finlandia en 2010) a prácticamente cero en los escalones finlandeses (LB20, LB21). El diseño de la reforma y la elasticidad de la oferta explican la diferencia.
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

- Diseños con microdatos administrativos privados o restringidos: contratos individuales, propiedad registral, grandes tenedores.
- Alquiler de temporada y por habitaciones: no hay datos oficiales.
- Expectativas de precios: no hay serie pública larga.
- Capitalización de las ayudas con alquiler pagado individual.

## Fuentes de datos

- **Prioridad alta.**
  - Censo anual por sección (F01).
  - INE VUT por sección (F02).
  - IPVA (F03).
  - SERPAVI (F04).
  - Fianzas de la GVA (F05).
  - Eurostat plataformas por NUTS3 (F12).
  - Datos abiertos del Ajuntament de València (F18-F19).
  - Registro de turismo de la GVA (F20).
  - Proyección de hogares, padrón y renta (F31-F33).
- **Fianzas por comunidad.** Solo Cataluña, la Comunitat Valenciana y Euskadi publican datos; Galicia, Andalucía, Baleares y Madrid, no.
- **Tres discrepancias con la documentación del proyecto.**
  - La licencia del Incasòl son «términos de uso», no CC BY 4.0.
  - La EFF 2022 ya ofrece microdatos científicos.
  - El INE muestra CC BY-SA 4.0 en el pie frente a CC BY 4.0 en el icono.
  - Quedan anotadas para que el autor revise docs/v5/licencias_datos.md y docs/v3/fuentes_fallidas.md (no modificados aquí).
- **Cifra en litigio.** Los 750.000 del Banco de España frente a unos 600.000 de la OCDE: periodos y supuestos distintos (contradicciones.md, punto 6).

## Límites de esta revisión

- Scimago devolvió 403. Los cuartiles proceden de agregadores o de docs/literatura.md, con la fuente indicada en cada fila; 24 entradas quedan sin cuartil o no aplica (20 de literatura y 4 de métodos) (informes, documentos de trabajo).
- Varias magnitudes están pendientes de leer en el texto completo: Sanchis-Guarner, OCDE 2025 y algunas del Banco de España.
- docs/literatura.md no se ha modificado (solo se permiten ficheros nuevos). Las correcciones propuestas están en literatura.md, sección «Actualiza docs/literatura.md».
