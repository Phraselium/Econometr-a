## 7. Limitaciones y qué datos las resolverían

### 7.1 Limitaciones generales

- **Capa y evaluación.** Toda cifra V18 es de capa C4 y ninguna ha pasado una evaluación en muestra sellada. La vía a una capa superior es la evaluación sellada diferida (evaluate_v18), que se abriría con datos posteriores al tope de entrenamiento y no antes de 2027. Las hipótesis fijadas para esa evaluación (E1-A1, E2-A1, E3-A1, E3-A2, E3-A3, E5-R1 y E6-R2) solo se evalúan si en entrenamiento quedan IDENTIFICADO. Hoy ninguna lo es, de modo que ninguna se evaluaría. Los episodios históricos (Ley 11/2020, el auge anterior a 2010, Barcelona 2011-2019, las cohortes de obra de 2015-2018 y los cambios del ITP) no pueden llegar a C3 con la definición actual de capas.
- **Pre-registro interno.** El plan y la adenda no tienen sello de tiempo externo, y casi todos los factores se habían estimado antes con estos datos: las réplicas no son primeras miradas. Parte de la evidencia de V18 es a posteriori (anexo F).
- **Potencia.** La mayoría de las ampliaciones son NO ESTIMABLES porque la magnitud mínima detectable supera la magnitud de la literatura o el número efectivo de choques es insuficiente. Un resultado NO ESTIMABLE no es un resultado nulo.
- **Literatura.** Muchas fichas son «solo resumen», NO VERIFICADAS o DISCREPANTES (la ficha describe una versión de trabajo y el DOI corresponde a la publicada), y el cuartil de las revistas no está verificado. La búsqueda sistemática adicional con OpenAlex quedó incompleta por agotarse la cuota, y está pendiente. Las magnitudes de otros países se aplican a España con unidades que no siempre coinciden. Para los tipos de interés (E7) no hay estudios con error típico en la unidad: la literatura da un rango de {{V18-B5-E7:rango}}.
- **Herramientas.** El BVAR, la proyección local con Newey-West, el SVAR con proxy y el metaanálisis bayesiano son NO APTOS en el Monte Carlo, y la herramienta de Honest DiD es apta solo sin desviación de tendencias paralelas. Sus resultados se publican con esa etiqueta.
- **Sellado y muestra.** Las comunidades y provincias selladas de v6 (entre ellas Madrid, Baleares y Canarias) y los bloques de V15 y V16 quedan fuera. Las ciudades con más presión turística y de alquiler no están en la muestra, salvo Barcelona con tres distritos menos.
- **Medidas.** El precio se mide con el valor tasado, el IPV por comunidad o el IPVA; el alquiler, con SERPAVI, el IPC de alquiler o los contratos nuevos del Incasòl (solo Cataluña). No son equivalentes.
- **Contabilidad.** Es contabilidad con elasticidades estimadas, sin interacciones ni efectos de equilibrio general. La variación observada no tiene error. Las contribuciones de los paneles son relativas entre territorios.
- **Fechas del ITP.** Proceden de memorias de Hacienda y no están contrastadas con el BOE.

### 7.2 Qué falta por factor y qué dato lo resolvería

La tercera columna cita, cuando existe, la tarea correspondiente de docs/v18/tareas_autor.md.

| Factor | Qué falta | Dato que lo resolvería |
|---|---|---|
| E1 Turismo | Más barrios con cambio de stock; primera etapa del IV; zonas y fechas de la regulación local | Microdatos de portales; geometría del PEUAT y fechas de moratorias; Inside Airbnb anterior a 2025-12 |
| E2 Topes | Renta anterior, superficie y tipo de contrato; tramo de renta; más trimestres posteriores en las zonas de 2024; desvío a temporada | Microdatos de fianzas con renta anterior y registros de otras comunidades; Registro Único de Arrendamientos |
| E3 Inmigración | Variación suficiente para detectar la magnitud de la literatura; Censo de 1991 y más grupos de origen | Series de nacionalidad más finas por provincia; ventanas más largas con datos posteriores |
| E4 Ayudas | Cualquier estimación propia | Microdatos de beneficiarios del Bono Alquiler Joven y de las ayudas autonómicas |
| E5 Oferta y suelo | Restricciones físicas y de planeamiento; primera etapa del Bartik | Sistema de Información Urbana, modelo digital del terreno, costa y agua; descarga masiva del Catastro |
| E6 Obra nueva | Edificios nuevos fuera de la provincia de València; lluvia de AEMET | Descarga masiva del Catastro; lluvia de AEMET |
| E7 Tipos | Primera etapa fuerte; exposición hipotecaria; saldo de préstamos | Licencia de EA-MPD; Encuesta Financiera de las Familias; saldo de préstamos del Banco de España; compraventas anteriores a 2007 |
| E8 Fiscalidad | Fechas verificadas; recaudación; compraventas por tramo | BOE y diarios autonómicos; compras por tramo de precio (Notariado) |
| E9 No residentes | Series de riesgo de más países de origen; compras por nacionalidad y provincia | Notariado y Registradores por nacionalidad y provincia; autorizaciones de golden visa |
| E10 Grandes tenedores | Serie homogénea de titularidad y entrada por zona | Serie del Catastro por tramo de titular, municipio y año; Panel de Hogares AEAT-IEF |
| E11 Vacías | Calendario del recargo del IBI y del impuesto catalán | Ordenanzas fiscales por municipio; calendario de la Ley catalana de vacías; serie anual de vacancia |
| E12 Vivienda pública | Promociones públicas por municipio y año | MIVAU, CASA 47 y empresas públicas autonómicas, por transparencia |
| F1 a F3 | Cointegración detectable con series más largas | Más años de datos y la Encuesta Financiera de las Familias |

### 7.3 Tareas pendientes del autor que no bloquean el documento

- Subir la etiqueta plan-replicacion-v18 al remoto desde su ordenador (el commit ya está en la rama remota).
- Descargar la tabla de Scimago para verificar los cuartiles.
- Repetir la búsqueda sistemática con OpenAlex cuando se restablezca la cuota.
- Autorizar `sellar_v18` y `evaluate_v18` en una versión posterior, cuando existan los datos mínimos.

### 7.4 Qué no cambia

Ninguna cifra publicada cambia de valor ni de capa por V18. No hay parada por contradicción con una conclusión publicada, porque ninguna estimación propia es IDENTIFICADO.
