# E4 · Ayudas a la demanda

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.*

## Lectura

- No hay microdatos de perceptores del Bono Alquiler Joven ni de las ayudas autonómicas, ni convocatorias autonómicas con fecha: **NO ESTIMABLE**.
- Q7a (V16) ya estimó la discontinuidad por la edad (−0,120) y no se repite: su estimando es un cambio de generosidad, no la incidencia.
- Datos comprobados: {"ficheros_con_nombre_de_perceptores_o_bono": [], "n_filas_bono_alquiler_joven_en_intervenciones": 5, "ambitos_bono": ["estatal"], "convocatorias_autonomicas_con_fecha": 0, "ecv_disponible_q7a": true, "nota": "La ECV no asigna el bono por la edad (Q7a, V16): su estimando es un cambio de generosidad, no la incidencia."}
- Tarea del autor que lo resolvería: tareas_autor.md, punto 3: microdatos de beneficiarios del Bono Alquiler Joven y de las ayudas autonómicas (edad, tramo de renta, municipio, fecha de solicitud y concesión, importe, alquiler declarado), por el Portal de Transparencia o convenio con anonimización.
- La magnitud preferida saldrá solo de la literatura, rotulada «solo literatura, sin estimación propia» (E4-L1).

## Literatura (sin combinar: unidades distintas)

| estudio | diseno | resultado | unidad |
|---|---|---|---|
| Fack (2005, CEPREMAP) | diferencias y triples diferencias con la extensión de las ayudas de los noventa (Francia) | θ = 0,76 (0,26) y 0,39 (0,24) en doble diferencia; 1,42 (0,63) y 1,02 (0,52) en triple | traslación de la ayuda al alquiler (θ) |
| Gibbons y Manning (2006) | recorte del Housing Benefit por fecha de mudanza (Reino Unido) | −10,3 % y −16,2 %; con tendencias por antigüedad −3,5 % y −6,8 % | % del alquiler |
| Grislain-Letrémy y Trevien (2022, Banque de France WP 886) | discontinuidad geográfica difusa, 60 aglomeraciones (Francia) | +0,052 (0,019) en el log del alquiler por m² por un diferencial de 15-40 €/mes | log del alquiler |


## Especificaciones

| id | estado | clasificacion_v18 | motivo |
|---|---|---|---|
| E4-X1 | NO ESTIMABLE | NO ESTIMABLE | falta el dato imprescindible: no hay microdatos de perceptores ni convocatorias autonómicas con fecha (solo el calendario estatal del bono). Sin tratamiento medido no hay variación que comprobar por MDE. |
| E4-X2 | no se estima (Q7a) | no se clasifica | no se repite: Q7a (V16) ya la estimó (−0,120 en el log del alquiler, con placebos del mismo orden) y su estimando es un cambio de generosidad, no la incidencia |
| E4-L1 | solo literatura | no se clasifica | la magnitud preferida saldrá solo de la literatura, rotulada «solo literatura, sin estimación propia»; en la fase 5 se combinará en la unidad de la ficha si es comparable |
