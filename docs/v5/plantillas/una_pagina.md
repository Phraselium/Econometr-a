# Vivienda en España en una página (versión pública {{proyecto.version_publica}})

**Borja Romero, economista.** Esta página resume lo que se sabe con más seguridad. Cada cifra va redondeada y con su rango al lado. Las notas técnicas están en la ficha enlazada.

**Cómo leer las etiquetas.** La página separa las cifras por cómo se sabe lo que dicen. <!-- check:cifra-libre (etiquetas de capa) -->
- [C1] es un hecho: al menos dos fuentes **independientes** coinciden dentro de una tolerancia declarada. <!-- check:cifra-libre (etiquetas de capa) -->
- [C2] es una cota: vale si se aceptan unos supuestos declarados. <!-- check:cifra-libre (etiquetas de capa) -->
- [C3s] depende de las restricciones de un modelo. <!-- check:cifra-libre (etiquetas de capa) -->
- [C4] incluye las estadísticas oficiales de **una sola fuente** y los resultados exploratorios. No permite hablar de causas. <!-- check:cifra-libre (etiquetas de capa) -->

Dos fuentes no son independientes si una se construye a partir de la otra o salen de la misma encuesta. Por eso en la versión 1.0 once cifras pasaron de C1 a C4 sin cambiar su valor (ver la fe de erratas). <!-- check:cifra-libre (recuento de la fe de erratas) -->

## Hechos: dos fuentes independientes coinciden [C1]

1. **Hay más hogares.** Entre 2021 y 2025 el número de hogares creció en unos {{dh_2125:breve}} [C1]. [Ficha A1](../v6_2/anexo_metodologico.md#a1-dh_2125-aumento-del-número-de-hogares-2021-2025)
2. **Se terminan {{terminadas_1924:rango_breve}}.** Son datos de 2019 a 2024 [C1]: Ministerio (fin de obra) y Catastro (altas). [Ficha A2](../v6_2/anexo_metodologico.md#a2-terminadas_1924-viviendas-terminadas-al-año-en-territorio-común-2019-2024)
3. **El precio de compra ha subido.** Entre 2015 y 2025 subió un {{A23-P2:breve}} [C1]. [Ficha A8](../v6_2/anexo_metodologico.md#a8-a23-p2-precio-de-compra-variación-2015-2025-núcleo-mivau-notariado-y-registradores)
4. **El alquiler sube más en los contratos nuevos.** En los contratos ya firmados subió un {{A23-A2:rango_breve}} entre 2015 y 2024 [C1]. En los contratos nuevos de la Comunitat Valenciana subió un {{A23-A10:breve}} entre 2021 y 2024 [C1]. [Fichas A7](../v6_2/anexo_metodologico.md#a7-a23-a2-alquiler-de-stock-variación-2015-2024-núcleo) y [A9](../v6_2/anexo_metodologico.md#a9-a23-a10-contratos-nuevos-en-la-comunitat-valenciana-2021-2024)
5. **La mayoría de los hogares es propietaria.** Son propietarios de su vivienda: {{R1C-001:breve}} [C1]. [Ficha A10](../v6_2/anexo_metodologico.md#a10-r1c-001-hogares-con-vivienda-principal-en-propiedad)

## Estadísticas oficiales de una sola fuente [C4]

Son datos oficiales y fiables en su definición, pero no hay una segunda fuente independiente con la que contrastarlos.

6. **Viviendas terminadas al año en toda España**, con País Vasco y Navarra: {{E-T7-prod:rango_breve}} según el año (Ministerio, una sola estadística) [C4].
7. **Sobrecarga del gasto en vivienda.** Destina más del 40 % de su renta a la vivienda un {{V10-ATL-A1:breve}} de quienes alquilan a precio de mercado (Encuesta de Condiciones de Vida, 2025) [C4]. El dato de Eurostat sale de la misma encuesta: no es una segunda fuente. <!-- check:cifra-libre (umbral de sobrecarga) -->

## Cotas y proyecciones: valen bajo supuestos declarados [C2]

8. **Se terminan menos viviendas de las que se forman hogares.** Entre 2021 y 2024 faltaron {{L3-DEF-2124-SINBAJAS:rango_breve}} [C2]. Es una cota, no una cifra exacta. Si se descartan dos de las correcciones de la EPA, faltaron {{L3-DEF-2124-SENS:rango_breve}}. [Ficha A5](../v6_2/anexo_metodologico.md#a5-l3-def-2124-sinbajas-déficit-2021-2024-sin-bajas-todas-las-variantes-v62)
9. **Hasta 2030 el saldo empeora en todos los escenarios.** Ocurre en todos los escenarios definidos por el autor, también en el más optimista [{{T4-H3:capa}}]. Cuánto empeora no se sabe: ver el recuadro. [Ficha B10](../v6_2/anexo_metodologico.md#b10-módulos-v51-t2-t3-y-t4-srcv5_1t2_runpy-t3_runpy-t4_runpy)
10. **Habrá más hogares.** El INE proyecta {{E-B1-F:breve}} más entre 2026 y 2035 [C2]. [Ficha A14](../v6_2/anexo_metodologico.md#a13-a14-b1-h4-y-e-b1-f-crecimiento-de-hogares-proyectado-2026-2035)

## Lo que añade el atlas regional (versión interna v7.2) [C4]

- Los precios de las comunidades se mueven casi siempre juntos. La media de las 17 recoge en compra un {{V71-S3-comun-r2-compra:breve}} de lo que varía cada una.
- No se confirma ninguna relación regional de largo plazo con el empleo, la población, las hipotecas o el paro: {{V71-S3-largo-confirmadas:num}} de siete hipótesis.
- En una simulación, las ayudas a la compra abaratan la vivienda a quien las recibe. Pero el precio de mercado sube un {{V71-S3-R6-e_ayuda_demanda-compra-precio10a:breve}} a diez años. Ese signo depende sobre todo de la fórmula de la simulación.
- El coste de construir más, movilizar vacías o limitar los pisos turísticos no se puede estimar con estos datos.
- Notas técnicas: [atlas regional](../v7_1/atlas/atlas_resumen.md) y [dosis y coste](../v7_1/S1/resumen.md). Los cambios entre versiones están en [qué cambió y por qué](que_cambio.md).

## Por qué ha subido (versión interna V8) [C4]

- Ningún factor destaca como el principal en ninguno de los diez casos estudiados. Como mucho coinciden {{V8-VOTOS-c-P5:num}} métodos de cuatro, y la regla exige tres.
- Desde mediados de 2022 el precio real de compra subió {{V8-OBS-c-P5:breve}}. De esa subida, {{V8-QNA-pp-c-P5:breve}} no se atribuye a ningún factor identificado [C3s: vale solo bajo las restricciones del modelo]. <!-- check:cifra-libre (umbral pre-registrado) -->
- El alquiler real del conjunto de contratos varió {{V8-OBS-a-P5:breve}}. Los contratos nuevos subieron más: Cataluña {{A23-A9:breve}} y Comunitat Valenciana {{A23-A10:breve}} [C1].
- La subida reciente es común a casi todas las comunidades: un {{V8-M1-cuota-c-P5:breve}} de lo que varían. Acompaña a la de la zona euro, con correlación {{V8-H8-9-est:breve}}. Es una asociación.
- Ningún modelo predice mejor que una regla sencilla basada en los últimos trimestres.
- Notas técnicas: [por qué ha subido](../v8/por_que_ha_subido.md), [informe econométrico](../v8/informe_econometrico.md) y [verificador V8](../v8/verificador_v8.md).

> **Lo que NO se puede afirmar con estos datos**
>
> - Que un solo factor sea la causa principal de la subida. Ni los pisos turísticos, ni la inmigración, ni la falta de oferta, ni los tipos de interés, ni los compradores extranjeros, ni las empresas.
> - Qué parte de las viviendas tienen empresas o grandes propietarios: no hay datos de titularidad suficientes.
> - Que los topes al alquiler bajen los precios o reduzcan la oferta.
> - Que haya una burbuja, ni que no la haya [C4]. Con ajuste por comparaciones múltiples, {{V72-GSADF-ratios-bh:num}} de cuatro cocientes nacionales son exuberantes. Sin ajuste son {{V72-GSADF-ratios-p05:num}}, y frente a los tipos de interés, {{V72-GSADF-tipos-p05:num}}.
> - Los niveles de precio sí son explosivos en {{V72-GSADF-niveles-bh:num}} de dos series. Por comunidades lo son {{V72-GSADF-ccaa-bh:num}} de 34 series, y {{V72-GSADF-ccaa-v6:num}} de 11 en otra muestra. [Ficha de la burbuja](../v7_2/gsadf/ficha_burbuja.md) <!-- check:cifra-libre (número de series del diseño) -->
> - Qué variable mueve el alquiler o el precio: ninguna supera las pruebas exigidas. Que un modelo prediga bien no dice por qué sube el precio [C4].
> - Cuántas viviendas harán falta entre 2026 y 2035: depende de supuestos y es exploratorio. La estimación central es de {{T3-H5b:breve}} [C4].
> - Las viviendas que quedan libres no se restan de esa necesidad: la proyección de hogares del INE ya las tiene en cuenta.
> - Cuánto empeora el saldo hasta 2030: {{T4-H2:rango_breve}} [C4]. Si empeora hasta 2035 tampoco se sabe [C4].
> - Cuántas viviendas desaparecen cada año. Las demoliciones con licencia fueron un {{E-T7-demol-2024:rango_breve}} en 2024 [C4]. [Ficha B7](../v6_2/anexo_metodologico.md#b7-módulo-e-hechos-derivados-srcv5e_hechos_e1py-e_hechos_t7py-e_hechos_v6py)

## Cómo citar estas cifras

- Cite el rango además de la cifra. En [C1], el rango va de la fuente más baja a la más alta.
- Las cotas [C2] valen solo dentro de los escenarios definidos por el autor. Cítelos con la conclusión.
- Cite solo la versión pública vigente. Los cambios de cifras y sus motivos están en el historial de conclusiones y en la fe de erratas.
- [C4] no significa mala calidad. Incluye estadísticas oficiales de una sola fuente y resultados exploratorios.
- Las cifras completas, sin redondear, están en [cifras_clave.csv](cifras_clave.csv), con su id.

**Pre-registro.** Los análisis se registraron en git antes de estimarlos. Es un pre-registro **interno, sin sello de tiempo externo**: lo fijan etiquetas git (prereg-*) en el repositorio de desarrollo, cuya lista y commits están en `docs/v16/etiquetas_prereg.csv`.
