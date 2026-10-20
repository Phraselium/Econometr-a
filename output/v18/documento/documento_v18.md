# Factores de la subida del precio de la vivienda en España: reproducción, réplica y magnitudes (Documento de Trabajo V18)

Borja Romero, economista (firma individual, independiente). Documento de Trabajo de la versión V18 del proyecto (docs/v18/plan.md,
fase 6). Toda cifra procede de output/v5/cifras_clave.csv con su id. Toda cifra V18 es de capa C4 (nivel de evidencia EXPLORATORIO)
y lleva al lado su clasificación V18 (IDENTIFICADO, SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE o NO ESTIMABLE; docs/v18/decisiones.md,
K2). Pre-registro interno sin sello de tiempo externo (etiqueta plan-replicacion-v18). Generado por src/v18/f6_documento.py; no se
edita a mano.


## Resumen ejecutivo

Este documento reproduce, replica y amplía los estudios publicados sobre nueve factores del precio de la vivienda en España y fija,
para cada uno, una magnitud preferida con su intervalo y su clasificación V18. Toda cifra es de capa C4 (exploratoria).

| Factor | Magnitud preferida | Intervalo | Clasificación | Confianza | Limitación principal |
|---|---|---|---|---|---|
| Vivienda turística (E1) | 0,038 | [0,0145; 0,0615] (IC95) | NO ESTIMABLE | baja | un solo estudio en la unidad; estimación propia: no entra (NO ESTIMABLE) |
| Topes al alquiler (E2) | sin magnitud preferida | [−0,122; 0,0029] (rango) | SUGESTIVO | baja | la decisión cambia con la prior: rango sin magnitud preferida; estimación propia: SUGESTIVO |
| Inmigración (E3) | sin magnitud preferida | [−0,49; 3,51] (rango) | NO ESTIMABLE | baja | heterogeneidad alta entre estudios: rango sin magnitud preferida; estimación propia: no entra (NO ESTIMABLE) |
| Ayudas a la demanda (E4) | 0,0408 | [−0,0138; 0,0953] (IC95) | NO ESTIMABLE | baja | pocos estudios con error típico; heterogeneidad declarada; estimación propia: no entra (NO ESTIMABLE) |
| Oferta y suelo (E5) | sin magnitud preferida | [−0,202; 1,48] (rango) | NO ESTIMABLE | baja | heterogeneidad alta entre estudios: rango sin magnitud preferida; estimación propia: no entra (NO ESTIMABLE) |
| Obra nueva (E6) | −0,192 | [−0,319; −0,0646] (IC95) | NO ESTIMABLE | baja | un solo estudio en la unidad; estimación propia: no entra (NO ESTIMABLE) |
| Tipos de interés (E7) | sin magnitud preferida | [−5; −2] (rango) | NO ESTIMABLE | muy baja | sin error típico en la literatura: rango sin intervalo estadístico; estimación propia: no entra (NO ESTIMABLE) |
| Fiscalidad de la compra (ITP) (E8) | sin magnitud preferida | [−3,5; −3] (rango) | NO ESTIMABLE | muy baja | sin error típico en la literatura: rango sin intervalo estadístico; estimación propia: no entra (ASOCIACIÓN) |
| Compradores no residentes (E9) | sin magnitud preferida | [1,4; 2,1] (rango) | NO ESTIMABLE | muy baja | sin error típico en la literatura: rango sin intervalo estadístico; estimación propia: no entra (NO ESTIMABLE) |

Unidades: E1: Δln del alquiler por +1 pp de viviendas turísticas sobre el parque; E2: ATT en ln de la renta de los contratos regulados; E3: % de precio por +1 % de población por entrada de inmigrantes; E4: θ: euros de alquiler por euro de ayuda; E5: elasticidad precio de la oferta de unidades; E6: elasticidad del alquiler respecto a la oferta nueva (% por 1 %); E7: % del precio por +100 pb del tipo hipotecario, a 8 trimestres; E8: % de precio por +1 pp del ITP, a 12 meses; E9: % de precio por +1 pp de cuota de compras de no residentes. Cifras: ids V18-B5-E1 a V18-B5-E9 de cifras_clave (capa C4). La clasificación es la de la estimación propia designada del factor; la magnitud preferida puede venir solo de la literatura (sección 4). Confianza: media solo con magnitud preferida de tres o más estudios; muy baja sin error típico en la literatura; baja en el resto.

En la contabilidad principal, la variación del precio real de compra en 1995-2007 que queda sin explicar es de
69,0 pp (100·Δln) (NO ESTIMABLE): ningún factor tiene una
magnitud preferida construida con una estimación propia válida.


## Resumen no técnico

Para los topes al alquiler de Cataluña, el conjunto de estudios da un rango de -0,12 a 0,00 ATT en ln de la renta de los contratos regulados, sin una cifra única
preferida.


## Abstract

For each of nine factors, the paper reproduces and replicates published estimates for Spain and reports a preferred magnitude, an
interval and a V18 classification. All V18 figures are exploratory (layer C4). For rent caps in Catalonia, the range across studies
is -0,12 a 0,00 ATT en ln de la renta de los contratos regulados.


## 1. Introducción

Entre 1995 y 2007, la contabilidad principal deja sin explicar 69,0 pp (100·Δln) de la variación del
precio real de compra en el conjunto de España (toda la variación observada).


## 2. Datos

La réplica de vivienda turística en Barcelona usa 769 de las 1.068 secciones de Barcelona (sin Gràcia, Sant Andreu y Nou Barris, sellados en V15 y V16), en 48 barrios; 769 con SERPAVI; viviendas del Censo 2021 como denominador.


## 3. Métodos

La magnitud preferida de topes al alquiler combina los estudios con un metaanálisis con tres priors; su cobertura es
estudios de España, Francia, Alemania (5 estudios con error típico en la unidad (metaanálisis bayesiano de efectos aleatorios (3 priors)); estado B5: rango sin magnitud preferida (la decisión no coincide en las tres priors)).


## 4. Resultados por factor

### 4.2 Topes al alquiler (E2)

Réplica de la Ley 11/2020 en Cataluña: -0,04 log (diferencia entre regulados y controles, posterior frente a previo) (-0,05 a -0,03 log (diferencia entre regulados y controles, posterior frente a previo)), clasificación SUGESTIVO, capa C4.


## 5. Contabilidad de la subida por periodo y territorio

### 5.1 Por periodo

Variación sin explicar del alquiler real en 1995-2007: 1,8 pp (100·Δln).


### 5.2 ¿Problema general o local? (V17)

El componente común entre comunidades reúne 81,1 % (IC95 bootstrap por provincias) de la varianza de la variación anual del IPV.


### 5.3 Demografía (V17)

El número de hogares aumentó en 1.222.836 hogares entre 2021 y 2026.


## 6. Implicaciones para las políticas

La magnitud preferida de las ayudas al alquiler (E4) es 0,04 θ: euros de alquiler por euro de ayuda, con clasificación NO ESTIMABLE.


### 6.1 Factibilidad de construir (V17)

Se terminaron 83.700 viviendas/año de media en 2024-2025, frente a 568.684 viviendas/año en 2005-2007.


### 6.2 Medidas auditadas en V17: qué cambia

Traslación mediana de las ayudas al alquiler a la renta en los estudios con diseño: 46,0 % de la ayuda.


### 6.3 Discurso público auditado en V17: qué cambia

Renta media de los contratos nuevos en Cataluña (Incasòl, 2019-2025, ponderada): 20,0 %.


## 7. Limitaciones y qué datos las resolverían

Para los tipos de interés (E7) no hay estudios con error típico en la unidad: la literatura da un rango de -5,0 a -2,0 % del precio por +100 pb del tipo hipotecario, a 8 trimestres.


## Anexo A. Fichas bibliográficas

Estudios con error típico en la unidad para inmigración (E3): estudios de España, EE. UU., Reino Unido, Alemania (5 estudios con error típico en la unidad (metaanálisis bayesiano de efectos aleatorios (3 priors)); estado B5: rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo)).

## Anexo B. Reproducciones

## Anexo C. Planes de replicación

## Anexo D. Pruebas por estimación

Ejemplo: 0,13 elasticidad de impacto en variaciones (corto plazo; MCO clásico) (-0,02 a 0,27 elasticidad de impacto en variaciones (corto plazo; MCO clásico)) (ASOCIACIÓN).

## Anexo E. Monte Carlo de las herramientas

## Anexo F. Pre-registro interno y análisis a posteriori
