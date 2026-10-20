# V18 · E6 · Obra nueva y alquileres cercanos (piloto de la provincia de València)

**Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO. La clasificación V18 va en el campo `clasificacion_v18` y no cambia la capa. Sin estimación del resultado: no hay clasificación que contrastar con I8.
Código: `src/v18/estimacion/e6_obra_nueva.py` (+ `e6_datos.py`, `e6_diseno.py`, `e6_estim.py`, `e6_salidas.py`, `e1_nucleo.py`, `e1_datos.py`, `_e2e8_comun.py`); SEED 20261010; sin red; 12 s.

## 1. Resumen
- **Ninguna especificación de E6 supera la estimabilidad previa (adenda 1.3)**; no se estima ningún coeficiente y no hay cifra de efecto que difundir. Se publican los recuentos, el MDE y lo que falta.
- **E6-R1** (cohortes 2015-2018, secciones contiguas sin la propia, edificios de 20 viviendas o más): 33 secciones tratadas y 74 de control (mínimo 30 y 30: se cumple), pero **MDE80 = 0.0623** frente al umbral 0,062 (|−0,062| de Asquith, Mast y Reed, «cerca frente a cerca», año de la ficha DISCREPANTE). Supera el umbral por 0.0003 (una diferencia de unas dos milésimas del umbral) y se mantiene con R = 10.000 (MDE80 0.0622); con el valor crítico nominal en lugar del corregido por tamaño sería 0.0550. La regla de la adenda es «MDE ≤ referencia» con R = 2.000 y el valor crítico corregido por tamaño cuando el tamaño se aparta del 5 %: aquí el tamaño nominal del CR1 es 0.098. Se aplica la regla, no el matiz: NO ESTIMABLE por variación.
- **E6-A1** (50 viviendas, anillo de 250 m): 0 secciones tratadas (mínimo 30): NO ESTIMABLE por datos.
- **E6-R2 y E6-A3** (instrumento de lluvia de Mense): NO ESTIMABLES (X1) sin la lluvia de AEMET; E6-A2 sin la descarga masiva del Catastro.
- Consecuencia para B5: la estimación propia de E6 es E6-R2 (sin respaldo: E6-R1 está en otra unidad y no se combina). **E6 no tiene estimación propia**: la magnitud de E6 sale solo de la literatura en B5.
- Sin estimación del resultado no hay clase que pueda ser IDENTIFICADO ni contradicción con lo publicado (parada G no activada).

## 2. Datos y sellado
- **Secciones.** 1830 secciones INE de la provincia de València; quedan 992 tras excluir los bloques sellados de V15 y V16 (166 de las 588 secciones de València ciudad y los 101 municipios sellados de la provincia). La provincia 46 no está sellada en v6.
- **Edificios.** Microdatos del Catastro (INSPIRE, 92 municipios de la provincia, descarga de 2026-08-21; microdatos no versionados, agregados en data/raw/v11/catastro_inspire): 5913 edificios residenciales con año de construcción en 2011-2024 y en secciones no selladas. Cada edificio se asigna a la sección INE 2025 que contiene su centro; el año es el fin de obra del Catastro y mide solo edificios que siguen en pie.
- **Sellado y exposición.** La exposición a edificios de secciones selladas no es observable: se excluyen las unidades con alguna sección contigua sellada (201 de 992). Las pilas usan solo edificios de secciones no selladas.
- **SERPAVI** (VC, €/m²): 855 secciones de la provincia no selladas con algún año; todas las lecturas con `sellado.filtrar` (tope 2024).

## 3. Diseño (sin resultados)
Definiciones operativas fijadas antes de estimar (docs/v18/desviaciones_e1_e6.md, D-E6-1 a D-E6-4 y D-E6-8): edificio cualificado, unidad, «contigua», pila por cohorte, tratadas y controles, k = año − (T + 1), ventana T−4..T+4 (k = −5..3) y referencia k = −5. Controles: unidades cuyo primer edificio expuesto es de T+6 a 2024; ni unas ni otras tienen edificio propio cualificado en la ventana, y las tratadas no tienen otro edificio expuesto en la ventana.

| cohorte | tratadas | controles | municipios tratadas | municipios controles | València ciudad (tratadas) |
|---|---|---|---|---|---|
| 2015 | 14 | 73 | 3 | 3 | 1 |
| 2016 | 13 | 44 | 1 | 3 | 13 |
| 2017 | 3 | 22 | 1 | 1 | 3 |
| 2018 | 3 | 7 | 1 | 1 | 3 |

## 4. Estimabilidad (adenda 1.3), calculada antes de mirar ningún coeficiente
MDE80 de la media de k = 0..3, con CR1 t(G−1) por sección del edificio. El ruido se remuestrea por cluster de los residuos de 2011-2014 (ln SERPAVI tras efectos de sección y de municipio × año; «σ ya vista»: V15 y V16 no publican la σ residual de este resultado) con la variación real de las pilas; la ventana temporal se recicla de forma circular (4 años previos para 9 de ventana). Valor crítico: el mayor entre el nominal t(G−1) y el empírico del propio Monte Carlo (tamaño nominal del CR1: 0.098).

| id | tratadas | controles | clusters | MDE80 (R = 2.000) | nominal | corregido por tamaño | R = 10.000 | umbral | decisión |
|---|---|---|---|---|---|---|---|---|---|
| E6-R1 | 33 | 74 | 37 | 0.0623 | 0.0550 | 0.0623 | 0.0622 | 0.062 | NO ESTIMABLE |

Recuentos de las variantes y de E6-A1 (diseño, sin resultado):

| id | tratadas | controles | por pila (tratadas/controles) |
|---|---|---|---|
| E6-R1 | 33 | 146 | 2015: 14/73; 2016: 13/44; 2017: 3/22; 2018: 3/7 |
| E6-R1-v1 | 3 | 4 | 2015: 3/2; 2016: 0/2; 2017: 0/0; 2018: 0/0 |
| E6-R1-v2 | 34 | 29 | 2015: 3/22; 2016: 3/7; 2017: 9/0; 2018: 19/0 |
| E6-R1-v3 | 13 | 4 | 2015: 13/2; 2016: 0/2; 2017: 0/0; 2018: 0/0 |
| E6-R1-v4 | 38 | 153 | 2015: 15/79; 2016: 15/43; 2017: 5/24; 2018: 3/7 |
| E6-R1-v5 | 33 | 50 | 2015: 14/16; 2016: 13/20; 2017: 3/3; 2018: 3/11 |
| E6-R1-v6 | 7 | 99 | 2015: 3/49; 2016: 2/32; 2017: 1/15; 2018: 1/3 |
| E6-A1 | 0 | 40 | 2015: 0/19; 2016: 0/11; 2017: 0/9; 2018: 0/1 |

- Las variantes de E6-R1 no se estiman (principal NO ESTIMABLE). Los recuentos muestran además que la regla de «un solo evento en la ventana» deja pocas tratadas al bajar el umbral a 10 viviendas (más edificios por sección contigua) y que sin València ciudad no quedan controles suficientes.

## 5. E6-R2 (Mense, 2025): NO ESTIMABLE
- la API de AEMET OpenData exige una clave personal (alta con correo electrónico del autor); la consulta sin clave, hecha el 2026-10-20 desde esta sesión, devuelve una respuesta vacía. Sin la lluvia de AEMET, E6-R2 es NO ESTIMABLE (plan 1.6, X1); no se sustituye por otra fuente (ERA5, Open-Meteo) sin orden expresa del autor.
- Disponible: terminadas trimestrales por provincia (MIVAU, 2008T1-2026T2), IPVA provincial (2011-2024) e IPC de alquiler provincial. Con 39 provincias no selladas (las 11 de v6 fuera) el diseño tendría cluster por provincia con Webb (G < 40), según el plan.
- Los placebos de la adenda (lluvia de enero a marzo sobre T^Q4; lluvia sobre la renta ADRH y el empleo; lluvia de julio a septiembre de t−1 sobre las pernoctaciones de t) y la primera etapa no se pueden calcular sin la lluvia.

## 6. Desviaciones (detalle y fechas en docs/v18/desviaciones_e1_e6.md)
D-E6-1 definición operativa de edificio, unidad y exposición; D-E6-2 unidades con vecina sellada excluidas; D-E6-3 pilas con controles aún no expuestos y referencia k = −5 en lugar de Sun-Abraham con nunca tratadas; D-E6-4 regla de evento único en la ventana; D-E6-5 caché de edificios fuera del repositorio; D-E6-6 E6-R2 NO ESTIMABLE sin AEMET (tarea del autor); D-E6-7 E6-R1 NO ESTIMABLE por 0,0003 sobre el umbral; D-E6-8 ventana temporal circular del ruido.

## 7. Limitaciones y datos que lo resolverían
- Con 33 tratadas en 12 clusters de edificio, casi todas en València ciudad y municipios metropolitanos, el diseño tiene poca variación: el MDE80 queda en el límite de la referencia.
- SERPAVI mide contratos vigentes declarados (stock): diluye el efecto de una obra nueva sobre los alquileres de las secciones contiguas.
- El Catastro solo recoge edificios que siguen en pie: la obra nueva de 2015-2018 está subestimada si hubo demoliciones, y la fecha de inicio de obra no existe (v2 aproxima la terminación − 2).
- Datos: SERPAVI de 2025-2027 (más cohortes y periodo posterior), descarga masiva del Catastro (otras provincias; tareas_autor, punto 1), alquiler por anuncio georreferenciado (puntos 2 y 4) y la clave de AEMET OpenData o la autorización de una fuente alternativa de lluvia (tarea del autor).
