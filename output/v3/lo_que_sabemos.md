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
- [C2] Tipos de interés. La bajada del coste de uso en 2014-2021 es compatible con toda la subida del precio de compra de ese periodo. En 2021-2025 el coste de uso subió y no puede contribuir a la subida de precios de ese periodo, porque su signo es el contrario.

**Soluciones (simulación con rangos de parámetros)**
- [C2] Para estabilizar el esfuerzo de acceso en 2026-2035 se necesitan **104.000-413.000 viviendas al año**, frente a 89.000-101.000 terminadas. La brecha es positiva en todo el rango de supuestos.
- [C2] Las opciones que añaden viviendas reducen el esfuerzo de acceso en todo el rango simulado sin reducir la oferta: construir 25.000-100.000 viviendas más al año, o movilizar el 10-30 % de las vacías situadas donde hay presión de precios. Esas vacías cubrirían entre el **4,6 % y el 51 %** de la brecha.

## Probable pero no demostrado

- [C4] Topes de la Ley 11/2020 en Cataluña. La renta de los contratos nuevos fue **un 5,4 % menor** en los municipios sujetos (IC95 −7,1 % a −3,7 %; −37 €/mes). La validación por otra fuente (SERPAVI) tiene el mismo signo y menor tamaño (−0,8 %). La réplica de Jofre-Monseny et al. (2023) reproduce su resultado en la especificación más cercana. No llega a C3: el test de pretendencias de Rambachan-Roth y el de sensibilidad no lo permiten.
- [C4] En el número de contratos nuevos bajo los topes, el signo es negativo en la mayoría de especificaciones (−4,9 %), pero el contraste principal no es significativo y fallan las pretendencias y el placebo de fecha.
- [C4] Asociación entre viviendas turísticas y alquiler por sección censal (2021-2024): pequeña. Con un aumento típico de 1,4 puntos de viviendas turísticas sobre el parque, el alquiler sube **menos de un 0,5 %**. En los distritos sellados el IC95 incluye 0. La réplica de García-López et al. (2020) no se reproduce con datos actuales (otro periodo y otra medida de alquiler).

## No se puede afirmar con estos datos

- Que las viviendas turísticas sean la causa principal de la subida del alquiler en España (sin evidencia C3; las cotas no lo descartan solo con supuestos débiles).
- Que los topes reduzcan la oferta de alquiler, ni que no la reduzcan.
- La contribución de los grandes tenedores: los datos están pedidos al Catastro (docs/v3/solicitudes_transparencia.md).
- Que exista una burbuja: no hay test de exuberancia, y las dos medidas de la razón precio/alquiler discrepan en signo.
- El efecto sobre el precio de los compradores extranjeros, de la ocupación ilegal o de bajar el ITP/IVA: no hay diseño ni datos.
- Una cifra de efecto de la regulación de viviendas turísticas sobre el alquiler local: depende de una elasticidad sin estimación española verificada.

## Problema y soluciones robustas

- [C1] El desfase entre hogares y viviendas nuevas desde 2021 y la caída de la propiedad entre los jóvenes son hechos confirmados por varias fuentes.
- [C2] Aumentar la oferta mejora el esfuerzo de acceso en todo el rango de supuestos simulado. Es la única familia de medidas para la que el signo no depende de supuestos inciertos.
- [C4] El saldo neto de los topes para los inquilinos (beneficio menos posible reducción de contratos) cambia de signo según la respuesta de la oferta: −4.600 a +1.600 € al año por inquilino cubierto. Depende de supuestos.
- [C4] Retirar viviendas turísticas devuelve como máximo unas 31.000 viviendas al alquiler en las seis grandes ciudades, retirándolas todas en las secciones de mayor peso. Su efecto sobre el alquiler local depende de una elasticidad no estimada.
