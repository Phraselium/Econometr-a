# Vivienda en España: lo que sabemos y lo que no (v3)

Resumen en dos páginas del proyecto v3: datos públicos, `make all` reproducible sin red y revisión independiente por oleadas. Cada afirmación lleva su capa de evidencia:
- **C1**, hecho confirmado por ≥2 fuentes, con su rango;
- **C2**, cota válida bajo supuestos débiles y explícitos;
- **C3**, efecto con identificación que supera pretendencias, placebos, sensibilidad y validación sellada;
- **C4**, exploratorio.

Ningún resultado de este proyecto alcanzó C3. Detalle y fuentes: output/v3/articulo.md; afirmaciones del debate: output/v3/verificador/verificador.md.

## Afirmable con seguridad

**El problema**
- [C1] Entre 2021 y 2025 los hogares crecieron más que las viviendas nuevas. El balance contable es de **+701.000 viviendas** (rango entre combinaciones de fuentes: 560.000 a 969.000). La cifra del Banco de España (≈750.000) cae dentro del rango. Con 2012 como año de partida, el signo del balance no está determinado.
- [C1] Las viviendas terminadas fueron **89.000-101.000 al año** en 2021-2025 (MIVAU).
- [C1] Viven con sus padres el **40-50 %** de las personas de 25 a 34 años (Eurostat/ECV y EPA).
- [C1] La propiedad entre los hogares jóvenes (menos de 35 años) cayó al **30,7-31,8 %** en 2022, **24 a 34 puntos menos** que en 2008 (EFF y ECV). En los hogares de 65 años o más es del 83-89 %.
- [C1] El precio de una vivienda de 80 m² equivale a **3,0-4,1 veces** la renta anual media de un hogar en 2023 (Atlas de renta del INE, con valor tasado y precio registral).
- [C1] El Censo 2021 cuenta **3,8 millones de viviendas vacías**. Solo el **27-36 %** está en los municipios con más presión de precios (tercil alto).
- [C1] Las personas de nacionalidad extranjera hicieron entre el **9,6 % y el 15,0 %** de las compraventas de vivienda de 2023-2025 (MIVAU y Registradores).

**Cotas: cuánto puede pesar cada factor como máximo**
- [C2] Viviendas turísticas. Su aumento de 2020 a 2024 equivale, como máximo, al **2,4-2,7 % del stock de viviendas en alquiler**, suponiendo que cada vivienda turística nueva es una de alquiler menos. Una **cuarta parte** de la subida municipal del alquiler ocurrió en municipios donde las viviendas turísticas apenas crecieron. Desde 2024 su número baja: la cota superior de ese periodo es 0.
- [C2] Inmigración. En 2014-2019 los hogares extranjeros suponen **como máximo el 45 %** de la creación neta de hogares. Para 2020-2025 la cota no es informativa: el supuesto extremo la lleva al 100 %.

**Soluciones (simulación con rangos de parámetros)**
- [C2] Para estabilizar el esfuerzo de acceso en 2026-2035 se necesitan **104.000-413.000 viviendas al año**, frente a 89.000-101.000 terminadas. La brecha es positiva en todo el rango de supuestos.
- [C2] Tienen signo estable en toda la rejilla simulada (reducen el esfuerzo de acceso sin reducir la oferta): construir 25.000-100.000 viviendas más al año, o movilizar el 10-30 % de las vacías situadas donde hay presión de precios. Esas vacías cubrirían entre el **4,6 % y el 51 %** de la brecha. La simulación no modela costes, así que esta ordenación no compara costes y beneficios.

## Probable pero no demostrado (exploratorio, C4)

Asociaciones que no alcanzan la capa C3. Se informan sin lenguaje causal y no deciden ningún veredicto.


- [C4] Topes de la Ley 11/2020 en Cataluña. La renta de los contratos nuevos de los municipios sujetos se asocia a una diferencia de **−5,4 %** (IC95 −7,1 % a −3,7 %; −37 €/mes). La validación por otra fuente (SERPAVI) tiene el mismo signo y menor tamaño (−0,8 %). La réplica de Jofre-Monseny et al. (2023) reproduce su resultado en la especificación más cercana. No llega a C3: el test de pretendencias de Rambachan-Roth y el de sensibilidad no lo permiten.
- [C4] Número de contratos nuevos bajo los topes: asociación de −4,9 % (IC95 −9,9 % a +0,5 %), no significativa. La validación por fuente (stock SERPAVI) da −4,4 % y excluye 0. Hay estimadores alternativos de signo opuesto, y fallan las pretendencias y el placebo de fecha.
- [C4] Tipos de interés, con el supuesto estructural P/R = 1/coste de uso: la bajada del coste de uso en 2014-2021 es compatible con toda la subida del precio de compra de ese periodo. En 2021-2025 el coste de uso subió, con signo contrario a la subida de precios.
- [C4] Asociación entre viviendas turísticas y alquiler por sección censal (2021-2024): pequeña. Con un aumento típico de 1,4 puntos de viviendas turísticas sobre el parque, se asocia a un alquiler mayor en **menos de un 0,5 %**. En los distritos sellados el IC95 incluye 0. La réplica de García-López et al. (2020) no se reproduce con datos actuales (otro periodo y otra medida de alquiler).

## No se puede afirmar con estos datos

- Que las viviendas turísticas sean la causa principal de la subida del alquiler en España (sin evidencia C3; las cotas no lo descartan solo con supuestos débiles).
- Que los topes reduzcan el alquiler o la oferta de alquiler, ni que no lo hagan: ningún diseño alcanzó C3.
- La contribución de los grandes tenedores: los datos están pedidos al Catastro (docs/v3/solicitudes_transparencia.md).
- Que exista una burbuja: no hay test de exuberancia, y las dos medidas de la razón precio/alquiler discrepan en signo.
- El efecto sobre el precio de los compradores extranjeros, de la ocupación ilegal o de bajar el ITP/IVA: no hay diseño ni datos.
- Una cifra de efecto de la regulación de viviendas turísticas sobre el alquiler local: depende de una elasticidad sin estimación española verificada.

## Problema y opciones con signo estable en la rejilla

- [C1] El desfase entre hogares y viviendas nuevas desde 2021 y la caída de la propiedad entre los jóvenes son hechos confirmados por varias fuentes.
- [C2] Signo estable en toda la rejilla simulada:
  - en sentido estricto, más construcción y movilización de vacías donde hay presión;
  - solo débilmente (efecto ≤ 0, nulo si desplaza a la construcción privada), la vivienda pública.
  
  La retirada de viviendas turísticas no tiene signo estable al incluir la estimación sellada H3-1. Los topes dependen de la respuesta de la oferta. Ninguna opción incluye sus costes.
- [C4] Topes: la reducción de renta por inquilino cubierto es de 148-598 €/año. El efecto sobre el esfuerzo medio de los inquilinos va de −2,9 % a +7,3 % según la respuesta de la oferta.
- [C2] Retirar todas las viviendas turísticas de las secciones de mayor peso de las seis grandes ciudades devolvería como máximo unas 31.000 viviendas al alquiler. [C4] Su efecto sobre el alquiler local va de −2,0 % a +0,5 % con la estimación sellada H3-1, y es mayor con calibraciones de la literatura no replicadas.
