# INE v2 por provincia: fallos y limitaciones

Generado por `src/fetch_ine_v2.py` (2026-10-10T06:53Z). Los datos no disponibles no se han inventado.

## Fallos de descarga en la última ejecución

Ninguno.

## Limitaciones verificadas (sin dato a nivel provincial)

| dato pedido | estado | tablas/endpoints probados | alternativa propuesta |
|---|---|---|---|
| Renta disponible de los hogares por provincia | No existe en la CRE. Solo PIB, PIB per cápita y empleo por CCAA/provincia. | op. CRE (257): 17 tablas, ninguna de renta disponible | INE Atlas de Distribución de Renta de los Hogares (ADRH), a nivel municipal/distrito, no verificado en esta sesión; `ine_cnt_renta_disponible.csv` (nacional/CCAA) |
| Hogares por provincia antes de 2021 | No encontrado | op. ECP tablas 60131–60136 (desde 2021); op. CENSOPV (8) solo viviendas 2011 (3457, 3456) | Censo 2011 de hogares por provincia (no localizado en la API); ECP 2021+ |
| Proyección de hogares | Descartada: es proyección, no dato observado | op. PROH (70), tabla 54562 | No usada |
| Hipotecas (base antigua) | Series 1994–2003; solo nacional y provincia con 'Total fincas' | tablas 3232, 3233, 3241 | No usadas: la base nueva (76317) cubre 2003–2026 solo para viviendas |
| Hipotecas: unidad del importe | Confirmar en metadatos INE | tabla 76317 | Unidad inferida por magnitud (miles de euros); FK_Unidad=7 |
| Código INE de municipio | La API no lo incluye en el nombre de serie | tablas 59060, 59061, 39363 | Unir por nombre con el catálogo de municipios (no descargado) |
| IPVA: Álava, Gipuzkoa, Bizkaia y Navarra | La tabla provincial no publica estas provincias (49 nombres = nacional + 48 provincias) | tablas 59058, 59005, 59059 | Sin alternativa en la API; no imputar |
| Inmigración desde el extranjero después de 2022S1 | La serie semestral (24420/24421) termina en 2022S1 | tablas 24420, 24421 | Continuación trimestral desde 2023 en tablas 59011/59020 (3 principales países, flujos); no descargada |
| Viviendas turísticas: plazas | No descargadas (fuera de la petición: solo viviendas) | tablas 39364, 39363 | Descargar si se necesitan (8.186 series municipales) |
| IPVA en euros | No existe: solo índices y variación anual | tablas de ponderaciones 50015, 50016, 50083, 59062–59067 (solo pesos) | Ninguna |
| Población por país de nacionalidad concreto y provincia (stock) | Solo agrupaciones de países en 77023 | 77023; 77099 (lugar de nacimiento) | Flujos por 3 países principales desde 2023 (59020); país de nacimiento (79278) |
| ECP por provincia en tabla completa (56947) | 'No puede mostrarse por restricciones de volumen' | 56947 con nult=4 y 40 | Descarga serie a serie con DATOS_SERIE (77023) |
| PIB provincial, unidad | Etiqueta de FK_Unidad=7 no verificada | 80109 | Unidad inferida (miles de euros) |
| PIB: Madrid, Murcia y Navarra | En 80109 solo aparecen con nombre de CCAA (uniprovinciales); se asignan a su única provincia | 80109 | Ninguna necesaria |
| Duplicados INE | Balears, Illes aparece dos veces con valores idénticos (ETDP3633/ETDP4170; 6150) | 6150 | Se conserva una serie |
| Municipios homónimos de provincia (VUT) | En 39363 un nombre puede ser provincia o municipio | 39363 vs 39364 | Se descarta la serie si su último valor coincide con la provincia de 39364 |
| Serie IPC alquiler con ECOICOP v1 | Cambio de clasificación | 76137 (v1) vs 76142 (ECOICOP v2) | Empalme no hecho; usar con cuidado |
