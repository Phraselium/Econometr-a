# V15 · Bibliografía crítica (fase 2)

> Ampliada en V16 por instrumento de política: docs/v16/literatura.md (fichas en docs/v16/literatura/).

Fichas completas por pregunta en docs/v15/literatura/. Cada ficha recoge el diseño, los datos, la magnitud tal como la da el autor, la validez externa para España y las discrepancias.

Las fichas las escribieron seis lectores (subagente lector-literatura, uno por pregunta). Los DOI se comprueban con `src/v15/verificar_referencias.py`, contra Crossref con caché versionada, y con DataCite o doi.org si el DOI no es de Crossref. Las fichas sin DOI se buscaron en Crossref con `src/v15/buscar_doi.py`, que exige título, primer autor y año coincidentes.

Estado a 2026-10-17:
- **100 fichas:** 88 VERIFICADA (DOI y metadatos coinciden) y 12 NO VERIFICADA (sin DOI localizado, o DOI de otra agencia sin metadatos comparables). Ninguna DISCREPANTE.
- **Cuartiles:** todos «cuartil no verificado». Scimago bloquea la descarga automática (docs/v6/fuentes_fallidas.md) y la descarga manual queda como tarea del autor.
- **Grado de lectura:** casi todo se ha leído en resumen o en un documento de trabajo, no en la versión publicada. Cada ficha dice qué se leyó. Las magnitudes de los resúmenes no sustituyen a las tablas de los artículos.

Preguntas sin revisión propia:
- P1 (oferta con restricciones físicas): descartada en la fase 1 por falta de datos.
- P7 (demografía frente a obra nueva) y P10 (espacial): quedan como exploratorias.
- P8 (distribución): sin potencia para cambios. Se apoya en la literatura de V12-B6.

## Síntesis por pregunta

### P2 · Fundamentales (docs/v15/literatura/P2_fundamentales.md, 18 fichas)
- **Evidencia.** Con dependencia transversal, la relación de largo plazo precio-renta en EE. UU. por estados es unitaria solo tras corregir los factores comunes (Holly, Pesaran y Yamagata: MG ingenuo 0,30; CCE ≈ 1). El ajuste es lento: −0,17 a −0,18 anual, con semivida de 3,5 a 6,3 años. Varios trabajos no encuentran cointegración precio-renta o precio-alquiler sin esa corrección (Gallin; Mikhed y Zemčík).
- **España.** Banco de España: brecha del 24-32 % en 2004 (Ayuso y Restoy) y precios provinciales cerca del equilibrio en 2018 (Álvarez Román y García-Posada). No se localizó ningún estudio español con CIPS y CS-ARDL en panel provincial trimestral.
- **Implicación.** El rango previo del repositorio (0,43-2,1 según el estimador) es coherente con una relación que depende de cómo se tratan los factores comunes. P2 es informativa si se fija el estimador (CS-ARDL/CCE) antes de estimar y se reportan todos.

### P3 · Tipos de interés (P3_tipos_interes.md, 15 fichas)
- **Magnitudes.** Las magnitudes de alta frecuencia por desviación típica de sorpresa son ≈ 0,006 en logaritmo (panel de 9 países con España) y ≈ 0,010 en la ratio precio/alquiler de España. Ambas están por debajo del MDE del repositorio: 0,012 a 4 trimestres y 0,025 a 8.
- **Depuración.** Hay que depurar el efecto información (Jarociński y Karadi). La serie mensual de sorpresas está en el repositorio, con licencia contradictoria (auditoría de financiación).
- **Exposición.** La hipoteca variable es muy alta en todo el país: poca variación territorial.
- **Implicación.** Sin potencia frente a las magnitudes plausibles. Un efecto significativo sería más probablemente una sobreestimación que un hallazgo.

### P4 · Inmigración (P4_inmigracion.md, 16 fichas)
- **Magnitudes.** Saiz: una entrada igual al 1 % de la población se asocia con +1 % en alquiler y valor. Sanchis-Guarner: ≈ 1 % de alquiler por punto de tasa. González y Ortega (España 1998-2008): +52 % acumulado en precios.
- **Escala.** Dentro de la ciudad el efecto es menor o de otro signo (Saiz y Wachter; Accetturo et al.; meta-análisis de Larkin et al.).
- **Instrumento.** El de redes o cuotas mezcla ajuste de corto y largo plazo (Jaeger, Ruist y Stuhler). La inferencia del shift-share necesita AKM (Adão, Kolesár y Morales) o el marco de Borusyak, Hull y Jaravel.
- **Implicación.** Con el padrón municipal por nacionalidad 2003-2022 (auditoría de demografía) hay potencia para efectos del orden de 1 % por desviación típica. El riesgo principal es la identificación: persistencia de las cuotas y desbordamiento entre municipios.

### P5 · Pisos turísticos (P5_pisos_turisticos.md, 17 fichas)
- **Magnitudes.** Las elasticidades del alquiler a la densidad de anuncios con diseño creíble van de 0,018 a 0,06 (García-López et al. en Barcelona, Barron et al., Koster et al., MESVAL en València). En los barrios más expuestos de Barcelona el efecto es del 1,9-7 %. Sobre el precio de compra el efecto es mayor.
- **Regulación.** Las evaluaciones de regulación dan efectos pequeños sobre el alquiler residencial: −2 % con −50 % de anuncios en Los Ángeles.
- **Corrección del orquestador.** El lector leyó el MDE como 0,7 en logaritmo; es 0,007. Corregido en la ficha: los efectos de la literatura, del orden de 0,02-0,06 por desviación típica, quedan por encima del MDE.
- **Implicación.** Hay potencia. Los riesgos son la selección espacial, los desbordamientos a barrios vecinos y la medida del resultado (SERPAVI mide el stock de contratos; la literatura usa alquiler de oferta). La COVID no sirve como experimento limpio.

### P6 · Topes y zonas tensionadas (P6_topes_alquiler.md, 18 fichas)
- **Ley 11/2020.** Los trabajos sobre Cataluña coinciden en ≈ −5 % en la renta de los contratos nuevos (Monràs y Montalvo; Jofre-Monseny et al.; Abel et al.), en línea con V9-D1b (−5,9 %). Ninguno lo somete a Honest DiD.
- **Oferta y desplazamiento.** En el número de contratos o la oferta, los resultados van de nulo a −30 %. Desplazamiento a la venta: +13-18 % (Abel et al.).
- **Zonas tensionadas 2024.** Un preprint (Pérez García, 2026) halla que el efecto en renta no resiste el emparejamiento ni el DiD sintético, con pretendencias rechazadas. La caída del número de contratos (≈ −13 %) sí resiste.
- **Desbordamientos.** Hay evidencia de desbordamientos a municipios no regulados (Berlín; Cataluña).
- **Implicación.** Con Incasòl trimestral (contratos nuevos, MDE ≈ 2,2 %) la pregunta tiene potencia para efectos del orden de la literatura. Lo informativo es si el efecto en renta pasa Honest DiD y si el número de contratos responde. Los donantes deben ser lejanos.

### P9 · Predicción (P9_prediccion.md, 16 fichas)
- **Literatura.** Las ganancias publicadas suelen medirse frente al paseo aleatorio, un listón más bajo que el AR(4) (Kishor y Marfatia). Los predictores individuales son inestables y las combinaciones simples a veces ganan (Stock y Watson; Timmermann). El nowcasting con precios de oferta reduce el RMSE un 5-23 % (Trojanek et al., pendiente de comprobar en el PDF).
- **Implicación.** Con 73 errores, el DM solo detecta reducciones del 18-30 % del ECM. El resultado esperado es «no distinguible del AR(4)», que hay que declarar con el MCS y el intervalo del ECM relativo.

## Qué sería sorprendente replicar o no replicar (resumen; detalle al final de cada fichero)
- **P2.** Sería sorprendente una elasticidad precio-alquiler unitaria y estable entre estimadores, o un ajuste rápido (más del 20 % anual). No lo sería no hallar cointegración sin corrección de factores comunes.
- **P3.** Sería sorprendente cualquier efecto significativo de una sorpresa de 1 desviación típica, o una interacción territorial significativa. Un nulo es lo esperable y no prueba ausencia de efecto.
- **P4.** Sería sorprendente replicar +3,06 %/pp o el 52 % de González y Ortega, o una primera etapa municipal fuerte con cuotas persistentes. Por barrio no lo sería un efecto nulo o menor que el municipal.
- **P5.** Sería sorprendente un efecto ≥ 0,10 por desviación típica, que señalaría selección o tendencias, o un nulo preciso en los barrios más expuestos de Barcelona. No lo sería un efecto pequeño de la regulación sobre el alquiler residencial.
- **P6.** Sería sorprendente que el −5 % en contratos nuevos pasara Honest DiD con M̄ = 1 sin más datos, o un efecto limpio y constante en 2024-2026. No lo sería un nulo en renta con una caída del número de contratos.
- **P9.** Sería sorprendente una reducción del ECM ≥ 18 % frente al AR(4) con un solo modelo. Una media simple de modelos que gane sería coherente con la literatura, pero debe persistir en el bloque sellado.

## Multiplicidad entre versiones (para el pre-registro)
La inmigración (P4) y los topes (P6) se han contrastado en cinco versiones o más, y la predicción (P9) en todas desde v1. El pre-registro de V15 declara este historial y limita las hipótesis confirmatorias a un número pequeño con Holm.
