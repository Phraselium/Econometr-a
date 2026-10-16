<!-- Generado por `make publicacion` desde output/v5/una_pagina.md. No editar a mano: se regenera y un test lo comprueba. -->

# Vivienda en España en una página (versión pública 1.0)

**Borja Romero, economista.** Solo hechos con al menos dos fuentes [C1] o cotas con supuestos explícitos [C2]. Cada cifra lleva periodo, fuente, fecha del dato y capa.

1. [C1] **Hay más hogares.** El número de hogares aumentó en 997.586 hogares (981.823-1.013.350 hogares) (2021-2025; INE ECP y EPA (sin corrección: los dos extremos son posteriores a la ruptura de 2021; ventanas distintas: stock a 1 de enero en la ECP y media anual en la EPA, v7.1 K4b-dh); dato de 2025T1; C1).
2. [C2] **Se terminan menos viviendas de las que se forman hogares.** Balance acumulado 2021-2024 sin bajas del parque: en el rango 389.361-710.542 viviendas (sin las dos correcciones que conservan el salto de la EPA, 596.371-710.542 viviendas) (2021-2024; hogares: EPA (varias correcciones) y ECP; terminadas: MIVAU y Catastro; dato de 2024T4; C2: el rango depende de cómo se corrija el salto de la EPA en 2021, y es una cota, no una estimación puntual).
3. [C2] **Hasta 2030 el balance empeora en todos los escenarios.** Con los ritmos de construcción considerados, incluido uno optimista, el déficit nacional 2025-2030 crece en toda la rejilla de escenarios, definida por el autor (2025-2030; Ministerio e INE; C2). Cuánto crece no es un hecho (ver el recuadro).
4. [C1] **Viviendas terminadas.** Viviendas terminadas al año: 72.264-94.426 viviendas/año (2019-2024; Ministerio (fin de obra) y Catastro (altas), dentro de ±15 %; dato de 2024; C1).
5. [C1] **El precio de compra sube.** Variación acumulada según el núcleo de tres fuentes: 47,2 % (44,2-56,1 %) (2015-2025 (media anual); MIVAU valor tasado; Notariado CGN; Registradores opendata; dato de 2025 (anual); C1).
6. [C1] **El alquiler de los contratos vigentes sube menos que el de los nuevos.** Contratos vigentes: 10,9-22,9 % (2015-2024; INE IPC (encuesta); INE IPVA (datos tributarios AEAT); dato de 2024; C1). Contratos nuevos en la Comunitat Valenciana: 28,5 % (26,1-30,8 %) (2021-2024; INE IPVA (AEAT); GVA fianzas; dato de 2024; C1).
7. [C2] **La próxima década.** Crecimiento de hogares proyectado por el INE: 1.720.537 hogares (1.308.531-1.772.410 hogares) (2026-2035; INE Proyección de Hogares (tabla 54562); dato de 2026; C2).
8. [C1] **La mayoría de los hogares es propietaria.** Hogares con vivienda principal en propiedad: 74,5 % de hogares (72,1-75,9 % de hogares) (2021-2022; BdE EFF; INE ECV; INE Censo 2021; dato de 2021-11 (Censo) / 2022 (EFF, ECV); C1).

**Qué añade la versión interna v7.2 [C4].** Los cambios entre versiones, y por qué, están en una sección única: [Qué cambió entre versiones y por qué](que_cambio.md).
- Los precios de las comunidades se mueven sobre todo juntos: la variación de cada una acompaña en gran medida a la media de las 17 (R² mediano de 93,6 % en compra).
- No se confirma ninguna relación regional de largo plazo con el empleo, la población, las hipotecas o el paro (0 de siete hipótesis).
- En una simulación condicional, las ayudas a la demanda reducen el precio neto de quien las recibe, pero el precio de mercado sube (4,4 % a diez años; el signo lo fija en gran parte la fórmula de incidencia). Su dosis y su coste en compra están declarados. En los instrumentos de cantidad (construcción, vacías, vivienda pública, turísticos) el coste no es estimable.

**Qué añade la versión interna V8: por qué ha subido [C4].** Detalle en [¿Por qué ha subido el precio de la vivienda?](por_que_ha_subido.md); afirmaciones evaluadas: [verificador V8](verificador/verificador_v8.md).
- Ningún factor puede designarse como el más relevante en ninguno de los diez casos (mercado por periodo): el máximo de métodos coincidentes es 2,0 de cuatro y la regla exige tres.
- El precio real de compra ha subido 18,4 pp desde mediados de 2022; 9,5 pp de los 18,4 pp quedan sin atribuir a los shocks identificados (banda del 68 %: -14,6 a 24,1 pp) [C3s, condicionado a las restricciones de signo y de cero]. <!-- check:cifra-libre (umbral pre-registrado) -->
- El alquiler real (-1,8 pp) mide el parque de contratos vivos; los contratos nuevos [C1] suben más: Cataluña 16,9 % (16,6-17,2 %) (2021-2024; INE IPVA (AEAT); Incasòl; dato de 2024; C1); Comunitat Valenciana 28,5 % (26,1-30,8 %) (2021-2024; INE IPVA (AEAT); GVA fianzas; dato de 2024; C1).
- La subida reciente es muy común a las diecisiete comunidades (92,8 % (86,7-94,9 %) de la varianza) y acompaña a la de la zona euro (correlación 0,60 (0,14-0,86)); es una asociación.
- Ningún modelo predice mejor fuera de muestra que un AR(4) sencillo.

> **Lo que NO se puede afirmar con estos datos**
>
> - Que un único factor (turísticos, inmigración, falta de oferta, tipos, compradores extranjeros o empresas) sea la causa principal de la subida.
> - Qué parte de las viviendas o del alquiler está en manos de empresas o grandes tenedores: no hay datos de titularidad.
> - Que los topes al alquiler reduzcan los precios o la oferta.
> - Que haya una burbuja, ni que no la haya [C4]. En el ámbito nacional, los cocientes precio/renta y precio/alquiler son exuberantes sin ajuste en 3 de cuatro, pero en 0 tras el ajuste por comparaciones múltiples, y en 0 frente a referencias con tipos de interés; los niveles de precio sí son explosivos (2 de dos). Por comunidades, 7 de 34 series tras el ajuste (y 0 de 11 en otra muestra). Una exuberancia estadística no identifica una burbuja, y su ausencia tampoco la descarta. <!-- check:cifra-libre (número de series del diseño) -->
> - Qué variable mueve el alquiler o el precio de compra: en v6 ninguna es «relevante con seguridad» y ninguna hipótesis confirmatoria pasa Holm; que un modelo prediga bien no identifica por qué sube el precio [C4].
> - La necesidad total de vivienda para 2026-2035 como hecho: depende de supuestos sobre el parque y queda como exploratoria (210.424 viviendas/año (99.388-292.083 viviendas/año) (2026-2035; B1; T1; dato de 2025 (ECP y MIVAU); proyección INE 54562 de 2026-06-17; C4)). Las viviendas liberadas no se restan de la necesidad: la proyección de hogares del INE ya descuenta las disoluciones de hogares.
> - Cuánto empeora el déficit a 2030 (87.246-946.852 viviendas, [C4]) y si empeora a 2035 (indeterminado, [C4]).
> - Cuántas viviendas salen del parque cada año: las identidades de stock no miden bajas, y las demoliciones con licencia son 0,02-0,04 % del parque en 2024 [C4].

**Cómo citar estas cifras (revisión por pares simulada).**

- Dé el rango antes que el valor central. Los rangos [C1] son el mínimo y el máximo entre combinaciones de fuentes, no intervalos de confianza.
- El precio de compra se cita con las dos medidas juntas: el núcleo de registros y el índice oficial.
- Las cotas y las direcciones [C2] valen dentro de la rejilla de escenarios definida por el autor. Cite la rejilla junto con la conclusión.
- Solo es citable la versión vigente. Las cifras de versiones anteriores se sustituyeron por nuevas fuentes, muestras o correcciones, y el motivo de cada cambio consta en el historial de conclusiones y en la fe de erratas.
- [C4] no indica baja calidad: incluye estadísticas oficiales de fuente única y resultados exploratorios.

**Pre-registro y versiones.** Las etiquetas git `prereg-v5` (pre-registro de las diferencias entre provincias, `docs/v5/prereg_B3.md`) y `v5.0` se crearon en el repositorio local el 10 de octubre de 2026 y se publicaron en el repositorio remoto el [fecha de publicación: pendiente del autor; las etiquetas aún no se han podido publicar desde el entorno de trabajo, véase la primera tarea de `docs/v7_1/tareas_autor.md`]. El commit del pre-registro es anterior a cualquier resultado de ese análisis, pero una etiqueta local no es un sello de tiempo externo. Por eso, en versiones futuras el pre-registro se depositará además con sello de tiempo externo (OSF o Zenodo) antes de estimar.
