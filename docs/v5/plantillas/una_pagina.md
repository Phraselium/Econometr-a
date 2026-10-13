# Vivienda en España en una página (versión de referencia v7.2)

**Borja Romero, economista.** Solo hechos con al menos dos fuentes [C1] o cotas con supuestos explícitos [C2]. Cada cifra lleva periodo, fuente, fecha del dato y capa.

1. [C1] **Hay más hogares.** El número de hogares aumentó en {{dh_2125:cita}}.
2. [C2] **Se terminan menos viviendas de las que se forman hogares.** Balance acumulado 2021-2024 sin bajas del parque: en el rango {{L3-DEF-2124-SINBAJAS:rango}} (sin las dos correcciones que conservan el salto de la EPA, {{L3-DEF-2124-SENS:rango}}) ({{L3-DEF-2124-SINBAJAS:periodo}}; {{L3-DEF-2124-SINBAJAS:fuentes}}; dato de {{L3-DEF-2124-SINBAJAS:fecha_dato}}; {{L3-DEF-2124-SINBAJAS:capa}}: el rango depende de cómo se corrija el salto de la EPA en 2021, y es una cota, no una estimación puntual).
3. [C2] **Hasta 2030 el balance empeora en todos los escenarios.** Con los ritmos de construcción considerados, incluido uno optimista, el déficit nacional 2025-2030 crece en toda la rejilla de escenarios, definida por el autor ({{T4-H3:periodo}}; Ministerio e INE; {{T4-H3:capa}}). Cuánto crece no es un hecho (ver el recuadro).
4. [C1] **Viviendas terminadas.** Viviendas terminadas al año: {{terminadas_1924:rango}} ({{terminadas_1924:periodo}}; {{terminadas_1924:fuentes}}; dato de {{terminadas_1924:fecha_dato}}; {{terminadas_1924:capa}}).
5. [C1] **El precio de compra sube.** Variación acumulada según el núcleo de tres fuentes: {{A23-P2:cita}}.
6. [C1] **El alquiler de los contratos vigentes sube menos que el de los nuevos.** Contratos vigentes: {{A23-A2:rango}} ({{A23-A2:periodo}}; {{A23-A2:fuentes}}; dato de {{A23-A2:fecha_dato}}; {{A23-A2:capa}}). Contratos nuevos en la Comunitat Valenciana: {{A23-A10:cita}}.
7. [C2] **La próxima década.** Crecimiento de hogares proyectado por el INE: {{E-B1-F:cita}}.
8. [C1] **La mayoría de los hogares es propietaria.** Hogares con vivienda principal en propiedad: {{R1C-001:cita}}.

**Qué añade la versión de referencia v7.2 [C4].** Los cambios entre versiones, y por qué, están en una sección única: [Qué cambió entre versiones y por qué](que_cambio.md).
- Los precios de las comunidades se mueven sobre todo juntos: la variación de cada una acompaña en gran medida a la media de las 17 (R² mediano de {{V71-S3-comun-r2-compra:valor}} en compra).
- No se confirma ninguna relación regional de largo plazo con el empleo, la población, las hipotecas o el paro ({{V71-S3-largo-confirmadas:num}} de siete hipótesis).
- En una simulación condicional, las ayudas a la demanda reducen el precio neto de quien las recibe, pero el precio de mercado sube ({{V71-S3-R6-e_ayuda_demanda-compra-precio10a:valor}} a diez años; el signo lo fija en gran parte la fórmula de incidencia). Su dosis y su coste en compra están declarados. En los instrumentos de cantidad (construcción, vacías, vivienda pública, turísticos) el coste no es estimable.

> **Lo que NO se puede afirmar con estos datos**
>
> - Que un único factor (turísticos, inmigración, falta de oferta, tipos, compradores extranjeros o empresas) sea la causa principal de la subida.
> - Qué parte de las viviendas o del alquiler está en manos de empresas o grandes tenedores: no hay datos de titularidad.
> - Que los topes al alquiler reduzcan los precios o la oferta.
> - Que haya una burbuja, ni que no la haya [C4]. En el ámbito nacional, los cocientes precio/renta y precio/alquiler son exuberantes sin ajuste en {{V72-GSADF-ratios-p05:num}} de cuatro, pero en {{V72-GSADF-ratios-bh:num}} tras el ajuste por comparaciones múltiples, y en {{V72-GSADF-tipos-p05:num}} frente a referencias con tipos de interés; los niveles de precio sí son explosivos ({{V72-GSADF-niveles-bh:num}} de dos). Por comunidades, {{V72-GSADF-ccaa-bh:num}} de 34 series tras el ajuste (y {{V72-GSADF-ccaa-v6:num}} de 11 en otra muestra). Una exuberancia estadística no identifica una burbuja, y su ausencia tampoco la descarta. <!-- check:cifra-libre (número de series del diseño) -->
> - Qué variable mueve el alquiler o el precio de compra: en v6 ninguna es «relevante con seguridad» y ninguna hipótesis confirmatoria pasa Holm; que un modelo prediga bien no identifica por qué sube el precio [C4].
> - La necesidad total de vivienda para 2026-2035 como hecho: depende de supuestos sobre el parque y queda como exploratoria ({{T3-H5b:cita}}). Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares.
> - Cuánto empeora el déficit a 2030 ({{T4-H2:rango}}, [C4]) y si empeora a 2035 (indeterminado, [C4]).
> - Cuántas viviendas salen del parque cada año: las identidades de stock no miden bajas, y las demoliciones con licencia son {{E-T7-demol-2024:rango}} en 2024 [C4].

**Cómo citar estas cifras (revisión por pares simulada).**

- Dé el rango antes que el valor central. Los rangos [C1] son el mínimo y el máximo entre combinaciones de fuentes, no intervalos de confianza.
- El precio de compra se cita con las dos medidas juntas: el núcleo de registros y el índice oficial.
- Las cotas y las direcciones [C2] valen dentro de la rejilla de escenarios definida por el autor. Cite la rejilla junto con la conclusión.
- Solo es citable la versión vigente. Las cifras de versiones anteriores se sustituyeron por nuevas fuentes, muestras o correcciones, y el motivo de cada cambio consta en el historial de conclusiones y en la fe de erratas.
- [C4] no indica baja calidad: incluye estadísticas oficiales de fuente única y resultados exploratorios.

**Pre-registro y versiones.** Las etiquetas git `prereg-v5` (pre-registro de las diferencias entre provincias, `docs/v5/prereg_B3.md`) y `v5.0` se crearon en el repositorio local el 10 de octubre de 2026 y se publicaron en el repositorio remoto el [fecha de publicación: pendiente]. El commit del pre-registro es anterior a cualquier resultado de ese análisis, pero una etiqueta local no es un sello de tiempo externo. Por eso, en versiones futuras el pre-registro se depositará además con sello de tiempo externo (OSF o Zenodo) antes de estimar.
