# Vivienda en España: lo que sabemos y lo que no (v3)

Resumen en dos páginas del proyecto v3: datos públicos, `make all` reproducible sin red y revisión independiente por oleadas. Cada afirmación lleva su capa de evidencia:
- **C1**: hecho confirmado por ≥2 fuentes, con su rango.
- **C2**: cota válida bajo supuestos débiles y explícitos.
- **C3**: efecto con identificación que supera pretendencias, placebos, sensibilidad y validación sellada.
- **C4**: exploratorio o de fuente única.

Ningún resultado de este proyecto alcanzó C3. El detalle y las fuentes están en output/v3/articulo.md; las afirmaciones del debate, en output/v3/verificador/verificador.md.

## Afirmable con seguridad

**El problema**
- [C1] Entre 2021 y 2025 los hogares crecieron más que las viviendas nuevas: el balance contable es de **+701.000 viviendas**, con un rango entre combinaciones de fuentes de 560.000 a 969.000. La cifra del Banco de España (≈750.000, DOI no comprobado) cae dentro del rango. Si se toma 2012 como año de partida, el signo del balance no está determinado. Las ventanas con dos fuentes de hogares se eligieron tras ver la disponibilidad de fuentes (docs/v3/limitaciones.md).
- [C1] Viven con sus padres el **40,3-50,2 %** de las personas de 25 a 34 años (Eurostat/ECV y EPA).
- [C1] La propiedad de la vivienda entre los hogares de menos de 35 años era del **30,7-31,8 %** en 2022, **24,2 a 34,0 puntos menos** que en 2008 (EFF y ECV). En los hogares de 65 años o más es del 83,0-89,4 %.
- [C1] El precio de una vivienda de 80 m² equivale a **3,0-4,1 veces** la renta anual media de un hogar en 2023 (Atlas de renta del INE, con valor tasado y precio registral).
- [C1] Sobre los 277 municipios con dato, entre el **27,5 % y el 40,3 %** de las viviendas vacías están en los municipios del tercil alto de presión de precios. En el tercil bajo está entre el 20,7 % y el 28,3 %. El rango recoge las dos medidas de vacías y las definiciones de presión.
- [C1] Las personas de nacionalidad extranjera hicieron entre el **9,6 % y el 15,0 %** de las compraventas de vivienda en 2023-2025 (MIVAU y Registradores; output/v3/verificador/fichas/V14.json).

**Cotas: cuánto puede pesar cada factor como máximo**
- [C2] Viviendas turísticas. Su aumento de 2020 a 2024 equivale, como máximo, al **2,4-2,7 % del stock de viviendas en alquiler**, suponiendo que cada vivienda turística nueva es una de alquiler menos. Una **cuarta parte (25 %)** de la subida municipal del alquiler ocurrió en municipios donde las viviendas turísticas crecieron menos de 0,1 puntos.
- [C2] Inmigración. En 2014-2019 los hogares extranjeros suponen **como máximo el 45 %** de la creación neta de hogares. Para 2020-2025 la cota no es informativa, porque el supuesto extremo la lleva al 100 %.

**Soluciones (simulación con rangos de parámetros)**
- [C2] Para estabilizar el esfuerzo de acceso en 2026-2035 se necesitan **104.000-413.000 viviendas al año**. La brecha frente al ritmo reciente de terminadas es positiva en todo el rango de supuestos.
- [C2] Dos opciones tienen signo estable en toda la rejilla simulada (reducen el esfuerzo de acceso sin reducir la oferta):
  - construir 25.000-100.000 viviendas más al año;
  - movilizar el 10-30 % de las vacías situadas donde hay presión de precios, que cubriría entre el **4,6 % y el 51 %** de la brecha.

  La simulación no modela costes, así que esta ordenación no compara costes y beneficios.

## Probable pero no demostrado (exploratorio, C4)

Asociaciones y datos de fuente única que no alcanzan C1, C2 ni C3. Se informan sin lenguaje causal y no deciden ningún veredicto.

- [C4] Topes de la Ley 11/2020 en Cataluña.
  - La renta de los contratos nuevos de los municipios sujetos se asocia a una diferencia de **−5,4 %** (IC95 −7,1 % a −3,7 %; −37 €/mes).
  - La validación con otra fuente (SERPAVI) tiene el mismo signo y es menor (−0,8 %).
  - La réplica de Jofre-Monseny et al. (2023) reproduce su resultado en la especificación más cercana.
  - No llega a C3 porque fallan el test de pretendencias de Rambachan-Roth y el de sensibilidad.
- [C4] Número de contratos nuevos bajo los topes.
  - Asociación de −4,9 % (IC95 −9,9 % a +0,5 %), no significativa.
  - La validación por fuente (stock de SERPAVI) da −4,4 % y excluye 0.
  - Hay estimadores alternativos de signo opuesto, y fallan las pretendencias y el placebo de fecha.
- [C4] Tipos de interés, con el supuesto estructural P/R = 1/coste de uso. La bajada del coste de uso en 2014-2021 es compatible con toda la subida del precio de compra de ese periodo. En 2021-2025 el coste de uso subió, con signo contrario a la subida de precios.
- [C4] Viviendas turísticas y alquiler por sección censal (2021-2024).
  - Coeficiente nacional de entrenamiento: +0,00026 log-puntos por punto de VUT (IC95 −0,0007 a +0,0013).
  - Coeficiente en los distritos sellados: +0,0010 (IC95 −0,0007 a +0,0028). Ambos IC95 incluyen 0.
  - Con un aumento típico de 1,4 puntos, la variación asociada es inferior al 0,5 %.
  - La réplica de García-López et al. (2020) no se reproduce con datos actuales (otro periodo y otra medida de alquiler).
- [C4] Fuente única: el Censo 2021 estima **3,8 millones de viviendas vacías** (por consumo eléctrico). Las viviendas terminadas fueron **89.000-101.000 al año** en 2021-2025 (certificados de fin de obra del MIVAU). Desde 2024 el número de viviendas turísticas baja.

## No se puede afirmar con estos datos

- Que sea la causa principal de la subida (≥50 %) ninguno de estos factores: viviendas turísticas, inmigración, falta de oferta y suelo, tipos de interés. No hay evidencia C3, y las cotas de cantidad no atribuyen precio. En los tipos, la traducción a precio depende de un supuesto estructural (C4).
- Que los topes reduzcan el alquiler o la oferta de alquiler, ni que no lo hagan: ningún diseño alcanzó C3.
- La contribución de los grandes tenedores: la solicitud de datos al Catastro está redactada y pendiente de presentar (docs/v3/solicitudes_transparencia.md).
- Que exista una burbuja: no hay test de exuberancia, y las dos medidas de la razón precio/alquiler discrepan en signo.
- La relación con el precio de los compradores extranjeros, de la ocupación ilegal o de bajar el ITP/IVA: no hay diseño ni datos.
- La variación del alquiler local asociada a regular las viviendas turísticas: depende de una elasticidad sin estimación española verificada.

## Problema y opciones con signo estable en la rejilla

- [C1] El desfase entre hogares y viviendas nuevas desde 2021 y la caída de la propiedad entre los jóvenes son hechos confirmados por varias fuentes.
- [C2] Signo estable en toda la rejilla simulada:
  - en sentido estricto: más construcción y movilización de vacías donde hay presión;
  - solo débilmente (≤ 0, nulo si desplaza a la construcción privada): la vivienda pública.

  La retirada de viviendas turísticas no tiene signo estable al incluir la estimación sellada H3-1. Los topes dependen de la respuesta de la oferta. Ninguna opción incluye sus costes.
- [C4] Topes: la reducción de renta por inquilino cubierto es de 148-598 €/año. La variación asociada del esfuerzo medio de los inquilinos va de −2,9 % a +7,3 % según la respuesta de la oferta.
- [C2] Retirar todas las viviendas turísticas de las secciones de mayor peso de las seis grandes ciudades devolvería como máximo unas 31.000 viviendas al alquiler. [C4] La variación asociada del alquiler local va de −2,0 % a +0,5 % con la estimación sellada H3-1, y es mayor con calibraciones de la literatura no replicadas.
