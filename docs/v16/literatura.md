# V16 · Literatura por instrumento (fase 3, ampliación de docs/v15/literatura.md)

## Qué hay y cómo se ha comprobado
- **Fichas.** Están en docs/v16/literatura/L*.md, una por instrumento. Siguen la estructura del encargo: mecanismo, evidencia internacional con diseño creíble, evidencia española, efectos secundarios y fichas.
- **Lectores.** Las escribieron siete lectores (lector-literatura), uno por instrumento. No repiten las de V15: tipos de interés, inmigración, fundamentales, predicción y la primera tanda de topes y pisos turísticos siguen en docs/v15/literatura/.
- **Referencias.** Las comprueba `python3 src/v16/f3_verificar_referencias.py`, el mismo verificador de V15 con caché propia.
  - Resultado a 2026-10-17: 72 VERIFICADA, 43 NO VERIFICADA (sin DOI localizado o DOI de otra agencia) y ninguna DISCREPANTE.
  - Hubo dos correcciones del orquestador. A una ficha con el DOI del documento de trabajo se le puso el de la revista. A otra se le retiró un DOI que el lector había deducido del patrón de numeración y que no coincidía con el título.
- **Cuartiles.** Todos «cuartil no verificado»: la descarga de Scimago sigue pendiente del autor (tareas_autor de V15).
- **Grado de lectura.** Casi todo se leyó en resumen o en una versión de trabajo. Las magnitudes de los resúmenes no sustituyen a las tablas.
- **Metaanálisis.** Está en output/v16/f3/metaanalisis.md y sigue la regla fijada de antemano (decisiones K7). Ningún grupo de resultado llega a cinco estudios con error estándar y la misma unidad, así que no hay agregado: se dan rangos sin agregar. La fase 6 usará distribuciones a priori poco informativas, con la escala del rango de la literatura de diseño creíble.

## Síntesis por instrumento
Cada línea resume lo que dicen los estudios leídos, con su signo y orden de magnitud; no es un veredicto del proyecto. Las magnitudes son las de los autores, en su unidad.

### L1 · Control de alquileres y zonas tensionadas (14 fichas nuevas; P6 de V15)
- **Renta:** los topes de segunda generación se asocian a rentas un 3-7 % más bajas en los contratos regulados. Cataluña, con la Ley 11/2020, da en torno a −5 % en dos estudios; la congelación de Berlín, −7 % a −11 %.
- **Oferta:** va de nula a −10 % en contratos del mismo territorio, y llega a −30 % en anuncios.
- **Precio de compra:** negativo o nulo.
- **Evidencia española causal:** solo los estudios sobre Cataluña. No hay evaluación de las zonas de la Ley 12/2023 ni del desplazamiento al alquiler de temporada medido con contratos.

### L2 · Regulación de la vivienda turística (14 fichas nuevas; P5 de V15)
- **Anuncios:** bajan entre un 9 % y un 60 % con la norma.
- **Alquiler residencial:** −2 % a −5 %, con un caso nulo.
- **Precio de compra:** −3 % a −10 %.
- **Densidad de viviendas turísticas:** elasticidad del alquiler en torno a 0,02-0,06 (P5).
- **España:** no hay evaluación causal del PEUAT, del Plan Especial de Hospedaje de Madrid, de Palma, de Baleares, de Canarias ni de la moratoria de València.

### L3 · Oferta y elasticidad (19 fichas)
- **Obra nueva y alquiler cercano:** la obra nueva se asocia a alquileres cercanos un 1-6 % más bajos (Asquith, Mast y Reed; Pennington; Li).
- **Cadenas de mudanzas:** llegan a hogares de renta baja (Mast; Bratu et al.).
- **Upzoning:** aumenta la construcción (Auckland, São Paulo).
- **España:** la única elasticidad leída es 0,8-1,3 por CCAA (Taltavull, resumen). No hay elasticidad municipal identificada ni evaluación de la Ley del Suelo. Faltan los parámetros españoles de calibración del modelo de cuatro cuadrantes, que quedan como supuestos declarados.

### L4 · Fiscalidad de la compra (19 fichas)
- **Volumen:** cae tras subidas permanentes del impuesto (−7 % por p.p. en Alemania; −14 % en Toronto). Antes de las subidas hay adelantos (+26 % a +41 %), y las rebajas temporales lo elevan.
- **Precio:** el impuesto lo soporta sobre todo el vendedor.
- **España:** no hay estudio causal del ITP, de las rebajas autonómicas, del adelanto de 2012 ni del IVA superreducido.

### L5 · Ayudas a la demanda (14 fichas)
- **Traslación al alquiler:** entre 0,04 y más de 1 euro de alquiler por euro de ayuda (Francia, Finlandia, EE. UU., Nueva Zelanda). La dispersión es muy grande según diseño y mercado.
- **Ayudas a la compra:** se capitalizan en el precio donde la oferta es rígida (Baviera; Help to Buy en Londres).
- **España:** no hay evaluación del Bono Alquiler Joven ni de los avales ICO.

### L6 · Compradores extranjeros y visados por inversión (14 fichas)
- **Demanda extranjera:** se asocia a +1 a +2 % de precio por punto de cuota extranjera.
- **Recargos a compradores extranjeros:** −4 a −6 % de precio a corto plazo (Vancouver).
- **España:** el único estudio provincial (MCO) no es significativo. No hay evaluación de la Ley 14/2013 ni de su supresión (Ley Orgánica 1/2025).

### L7 · Vivienda pública, impuestos a vacías y moratorias (20 fichas)
- **Vivienda pública:** desplaza entre 0,5 y 1 vivienda privada por cada una construida (EE. UU.). El efecto en el precio del vecindario cambia de signo según la renta del barrio.
- **Impuestos a vacías:** la vacancia baja con el impuesto (Francia −13 % relativo).
- **Moratorias de desahucios:** −2 a −4 % en la renta de oferta, con amenazas a la identificación declaradas.
- **España:** no hay estudio con diseño sobre VPO, el recargo del IBI ni el RDL 11/2020. El parque social español se sitúa entre el 1 % y el 2,5 % según la fuente.

## Marco de cuatro cuadrantes
- **Dónde:** output/v16/f3/cuatro_cuadrantes.md, generado por src/v16/f3_cuatro_cuadrantes.py.
- **Qué dice:** con los rangos declarados, a corto plazo los shocks de demanda van sobre todo al alquiler y al precio, y los de tipos al precio y a la obra nueva. El stock tarda décadas en ajustarse.
- **Datos de 2022 a 2024:** el patrón de un shock solo de tipos no se ve, porque precio, alquiler y obra nueva suben. El marco es compatible con un shock de demanda simultáneo, que la fase 6 (Q5) intentará separar.

## Lo que la literatura deja abierto para España
Ninguno de los siete instrumentos tiene una evaluación causal española con diseño creíble, salvo los topes de Cataluña. Para el resto, la evidencia es internacional. Su validez externa depende de la elasticidad de la oferta y de la tenencia, que en España son distintas: hay mucha propiedad, poco parque social y una hipoteca mayoritariamente variable hasta 2022.
