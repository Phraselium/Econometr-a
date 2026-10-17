# Auditoría V16 fase 1: tension_social (C4, descriptivo)

Script: `src/v16/auditoria/tension_social.py` (SEED=20261010). Excluye provincias de la muestra sellada (`muestra_sellada_v6`); las cifras de CGPJ son solo agregados propios. Detalle numérico en `resultado.json`.

## 1. Discrepancia 2025 de lanzamientos por partido judicial frente a provincia (prioridad)

**Qué se observa (39 provincias fuera de la muestra sellada con ambas series).** Para 2013-2024 la suma de partidos coincide con la serie provincial (desviación mediana 0,0 %; solo 2 provincias con desvío sistemático por partidos descartados, ver 1.4). En 2025 la desviación mediana es 9 % y 19 provincias superan el 10 % (24 en total con las selladas, según la ficha).

**Causa, en dos partes. Ninguna es un fallo del cruce de nombres ni del script.**

1. **Celda anómala en el xlsx de origen (RIBADAVIA, 2025).** El fichero `cgpj_lanzamientos_partidos_judiciales_2013_2025.xlsx` trae en la fila RIBADAVIA, bloque 2025, total 2.944 = hipotecaria 749 + LAU 1.783 + otros 412 (2024: 4). La fila se asigna bien a PJ-32-2 (Ribadavia, Ourense) y las columnas no están desplazadas: la fila es coherente internamente y las cuatro columnas del bloque 2025 son las mismas que en los otros años. Sin ese partido, Ourense suma 147 frente a 152 de la serie provincial (-3 %). Es un valor de la fuente, no del parseo.
2. **El bloque 2025 completo de ese fichero no reproduce la distribución territorial oficial.** El total nacional sí encaja (partidos cruzados sin PJ-32-2: 24.481; total TSJ anual 2025: 24.540; el déficit de 59 corresponde a los 4 partidos no cruzados). Pero por comunidad la suma de partidos se aparta del total TSJ, que coincide exactamente con la serie provincial 2T-2026 y con la edición anual 2025: Castilla-La Mancha +57,6 %, Extremadura +41,8 %, Castilla y León +22,9 %, Comunitat Valenciana -13,5 %, Cantabria -13,1 %, País Vasco -4,0 %; Andalucía -0,4 %, Cataluña -1,5 % y Galicia +0,5 % encajan. Con las filas en el mismo orden que en 2024 (correlación 2024-2025 de 0,95 sin PJ-32-2; con desfases de 1 a 3 filas, 0,1-0,3), no hay desplazamiento de filas. La dispersión del crecimiento 2025/2024 entre partidos (sd log 0,47) es mayor que entre provincias (0,36), mientras que en 2019-2024 es igual. Dos partidos más con salto atípico (|z|>5): PJ-13-10 y PJ-49-1. Hipótesis no verificable con los ficheros: reasignación de lanzamientos entre sedes en 2025 al implantarse los tribunales de instancia; hace falta confirmación del CGPJ.
3. Descartadas: unidades (los totales son lanzamientos practicados; total = hipotecaria + LAU + otros en las 4.290 celdas partido-año) y cruce por nombre (el cruce reproduce 2013-2024 al decimal).

**Corrección propuesta (sin tocar el script ahora).** (a) Anular (NA) la serie de partidos de 2025 o marcarla `invalida_2025`, y usar la serie provincial/TSJ para 2025; (b) añadir al script un control que compare, por provincia y año, suma de partidos frente a provincia con umbral 3 % y falle en 2013-2024; (c) añadir alias para los 4 partidos sin cruce (Cangas de Narcea, Maó, Villarcayo, Villarrobledo) y recuperar 37 municipios; (d) dejar el filtro del bloque 2025 en la ficha.

## 2. Otras comprobaciones del CGPJ
Provincias con desvío antes de 2025: Albacete (02; 0,77-0,81 en 2013-2015 y 0,88 en 2023, por el partido Villarrobledo sin cruce) y Burgos (09); Cádiz y Málaga (11, 29) quedan en 0,93-0,98 porque Ceuta y Melilla están en la serie provincial pero son partidos con código propio (51, 52) fuera de la suma de 11 y 29. Araba/Álava 2022: partidos 18 % por encima de la serie provincial (sin explicar).

## 3. Padrón municipal 1996-2025 (cifras oficiales, 6.502 municipios no sellados)
Falta 1997 (no publicado). Total = hombres + mujeres en todas las celdas; sin ceros ni negativos; 4 municipios sin dato en 2025 (códigos con `vigente_2025 = False`); sin huecos intermedios. La suma provincial coincide al 0,00 % con `padron_pob_nacionalidad` Total de data/base (41 provincias, 2003-2022; mismo origen INE, no es validación independiente). Atípicos de crecimiento (|z| robusto >5): 42 casos en municipios de ≥5.000 hab. (11 en 2014; top: 08068 en 1999, 10180 en 1999, 11021 y 14060 en 2019, 03118/03012/03047 en 2014), compatibles con revisiones de padrón y ajustes por bajas de oficio; a verificar si se usan como regresor.

## 4. EMCR frente a EVR (solape 2021)
La EMCR 2021 de la familia coincide al 100 % con `emcr_md_inmigracion_exterior` de la base (microdatos). Frente a EVR, en los 562 municipios con EVR: inmigración exterior EMCR/EVR = 1,31 (corr. 0,999; mediana de desviación +34 %); emigración exterior = 1,56 (corr. 0,99; mediana +74 %). Hay por tanto una ruptura de nivel (otra metodología, ya señalada en la ficha) pero no de rango: el orden entre municipios se conserva. La EVR cubre solo municipios >=10.000 hab. No se deben enlazar niveles; sí variaciones dentro de cada serie. Suma municipal EMCR de inmigración exterior: 572.832 (2021), 806.363 (2022), 797.573 (2023), 830.365 (2024).

Nivel de evidencia: DESCRIPTIVO. No se estima ningún efecto.
