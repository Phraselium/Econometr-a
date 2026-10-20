## 2. Datos

**Regla general.** Toda cifra del documento procede de output/v5/cifras_clave.csv con su id (V18-*, V17-* y anteriores), su fuente, su capa y, en las cifras V18, su clasificación. El generador redondea los valores: dos decimales para los menores que la unidad en valor absoluto, un decimal para los intermedios y enteros para los recuentos y las cifras grandes. Los coeficientes pequeños se muestran con tres cifras significativas; los límites de sus intervalos, redondeados como se acaba de decir (los valores completos están en tablas_v18.xlsx, pestaña «estimaciones»).

### 2.1 Fuentes por factor

| Factor | Fuentes principales | Periodo y nivel |
|---|---|---|
| E1 Vivienda turística | Registro de viviendas de uso turístico (HUT) del Ajuntament de Barcelona con coordenadas por licencia; SERPAVI (alquiler mediano por sección); Censo 2021; INE de viviendas turísticas por sección; OpenStreetMap (atractivos); Google Trends; Eurostat (noches por NUTS 3) | Barcelona por sección y barrio, 2011-2024; otras cuatro ciudades por sección, 2021-2024 |
| E2 Topes al alquiler | Incasòl, registro de fianzas (renta media y número de contratos por municipio); paro registrado mensual del SEPE por municipio; padrón; Censo 2021; BOE y DOGC | Municipios de Cataluña, trimestral desde 2019T1 y anual desde 2007 |
| E3 Inmigración | Padrón por nacionalidad (stock a 1 de enero); Censo de 2001 por nacionalidad (Eurostat); entradas por nacionalidad (INE y Eurostat); valor tasado del MIVAU; IPVA; SERPAVI | Provincias, 2002-2022 |
| E4 Ayudas a la demanda | Calendario estatal del Bono Alquiler Joven (RD 42/2022); Encuesta de Condiciones de Vida | Sin microdatos de perceptores |
| E5 Oferta y suelo | Viviendas iniciadas y terminadas (MIVAU); valor tasado; empleo por rama (Eurostat e INE, NUTS 3); deflactor | Provincias, 2002-2023 |
| E6 Obra nueva | Catastro INSPIRE de los municipios de la provincia de València que lo publican; SERPAVI por sección | Secciones de la provincia de València, 2011-2024 |
| E7 Tipos de interés | Tipos hipotecarios y euríbor (Banco de España); sorpresas monetarias de alta frecuencia (Jarociński y Karadi); valor tasado; IPV; IPC de alquiler; compraventas; visados | Nacional, 1999-2026; panel provincial |
| E8 Fiscalidad de la compra | Tipo general del ITP por comunidad (memorias de Hacienda, base de intervenciones de V16); valor tasado provincial; compraventas mensuales | Comunidades de régimen común no selladas, desde 2010 |
| E9 No residentes | Padrón por nacionalidad de 2003; series de riesgo en origen (PIB, precios de la vivienda: Eurostat y OCDE); cuota de compras de no residentes (MIVAU) | Provincias y países de origen |
| E10 Grandes tenedores | Estadística de titularidad del Catastro (tres cortes, 2024-2026); alquiler municipal por m² | Municipios |
| E11 Viviendas vacías | Censos de 2011 y 2021 (este último por consumo eléctrico) | Dos cortes con métodos distintos |
| E12 Vivienda pública | Calificaciones definitivas de vivienda protegida (MIVAU) | Provincias, 2002-2024 |
| F1-F3 Modelos de conjunto | PIB, renta disponible, población, hogares, tipos, parque, iniciadas y valor tasado | Nacional trimestral y panel provincial |

Muestras concretas de las estimaciones principales:

- E1-R3 (Barcelona): {{V18-E1-R3:cobertura}}.
- E2-R1 (Ley 11/2020): {{V18-E2-R1:cobertura}}.
- E3-R1 (inmigración): {{V18-E3-R1-beta:cobertura}}.
- E8-R1 (ITP): {{V18-E8-R1:cobertura}}.
- E10-A1 (grandes tenedores): {{V18-E10-A1:cobertura}}.
- E7-R3 (BVAR de tipos): {{V18-E7-R3:cobertura}}.

### 2.2 Unidades selladas que se excluyen

- **v6.** Se excluyen de toda estimación las comunidades y provincias de la muestra sellada de v6 (Aragón, Asturias, Illes Balears, Canarias, Madrid, Región de Murcia, Navarra y La Rioja, con sus provincias y todos sus municipios, distritos y secciones). Quedan fuera, entre otras, las ciudades de Madrid, Palma, Zaragoza y Murcia.
- **V15 y V16.** Se excluyen los municipios, distritos y secciones de los bloques espaciales sellados de V15 y V16. En Barcelona, València, Sevilla y Málaga eso aparta una parte de los distritos: la muestra de Barcelona pierde Gràcia, Sant Andreu y Nou Barris. El total municipal de una ciudad con distritos sellados es una fuga declarada y no se usa en las principales (adenda 1.5).
- **Sellado temporal.** No se usa ningún periodo posterior al último visto de cada variable en V15 y V16, ni ninguna edición publicada después de la fecha de corte común de ambas (2026-10-17). Los topes por variable están en docs/v18/sellado_v18.json, generado con solo metadatos después de la etiqueta y antes de la primera estimación. Donde dos reglas dan topes distintos se aplica el más restrictivo (por ejemplo, el total de transacciones de extranjeros).
- **Distritos sellados en v3.** No se excluyen: su muestra sellada ya se abrió en v3 con una evaluación por hipótesis (docs/v3/decisiones.md). Se dice por transparencia.
- **Sin acceso a muestras selladas.** No se lee data/sealed ni las filas marcadas como muestra sellada de v6, y no se ejecuta ninguna evaluación sellada. Las fuentes se leen con el filtro de sellado de V18 y con la exclusión de v6.

### 2.3 Datos posteriores a la etiqueta

Las fuentes abiertas que el inventario de la fase 0 marcaba como ausentes y que no requerían al autor se descargaron después de la etiqueta (Censo de 2001 por nacionalidad, OpenStreetMap, Google Trends, Open Data BCN, afiliación por sector, tipos de cambio, entre otras). Llevan la marca `posterior_prereg` y su manifiesto. Su adquisición se limitó a descargar, normalizar y auditar, sin cruzarlas con ningún resultado. Cuando una fuente no pudo descargarse, la especificación que la necesitaba pasó a NO ESTIMABLE y se anotó en docs/v6/fuentes_fallidas.md.

### 2.4 Licencias y terceros

- Incasòl: datos no redistribuibles; solo se publican agregados propios.
- Registradores: el aviso legal prohíbe reproducir; sus agregados se usan solo como contraste interno.
- Inside Airbnb: su política pide no republicar los datos; se publican solo agregados.
- Notariado: el portal no permite extracción automática; las compras por nacionalidad y al contado son tarea del autor.
- Paquetes de replicación de otros autores: se guardan fuera de git, con su licencia y suma de control. Ningún PDF se versiona; las fichas llevan enlace, DOI, licencia y notas, con citas de 15 palabras como máximo.
- Los PDF y paquetes figuran en data/bib (fuera de git, con sha256 en data/bib/CHECKSUMS.sha256).

### 2.5 Interpolaciones y fuentes no validadas

Las series interpoladas (por ejemplo, visados de 1995 a 2007) y las fuentes no validadas entran solo en robustez. Las fechas de entrada en vigor de los cambios del ITP proceden de memorias de Hacienda y no están contrastadas con el BOE: por ello E8 tiene tope SUGESTIVO y esa limitación se repite en la sección 4.8.
