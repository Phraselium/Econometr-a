# Decisiones v5.1

## Setup
- Rama r5.1/main desde r5/main (cc69e02, v5.0). Las salidas nuevas van en output/v5_1; los entregables se regeneran en output/v5 a partir de las mismas plantillas, para conservar las rutas publicadas.

## T1 y T2 (subagentes)
- **T1, bajas del parque.**
  - Las identidades de stock (Censos 2011-2021 y Catastro) dan bajas NEGATIVAS (−0,33 % y −0,18 % al año). Lo que miden son altas netas no certificadas o afloramientos, no bajas, así que no sirven como estimación de bajas.
  - Las licencias de demolición del Ministerio, solo nacionales y por CCAA, dan un 0,02-0,04 % del parque en 2024. No cubren ruina, cambios de uso ni agregaciones.
  - Los métodos no coinciden: la tasa queda en C4 (0 / 0,026 % / 0,052 %), salvo la cota física 0, que es C2. Sustituye al supuesto del 0,1-0,2 % de v4, que queda por encima de todo lo observado.
  - **Hallazgo:** el Censo 2021 se refiere a 1-ene-2021, no a 1-nov-2021 como anota el manifiesto, que recoge la fecha de descarga. B1 (v5) sumó un año de terminadas de más en su método de identidad; con la ventana correcta el resultado sigue siendo negativo. Se anota en ERRATA.
- **T2, liberadas.**
  - 1,86 M en 2026-2035, por fallecimiento y por traslado a residencias (C4). Llegan al mercado unas 150.000 al año.
  - Los parámetros de residencias no tienen dato verificado.
  - NO se restan de la necesidad.
- **Para T3.** El déficit 2021-2024 debe combinar las 12 combinaciones de fuentes de M0 (C1 sin bajas: 562.692-688.692) con la tasa de bajas de T1. T1 dio 562.692-618.144 con una combinación, y no debe estrechar el rango C1 de fuentes.

## T5 (orquestador)
- **Ayudas a la demanda.** El traslado al precio aparece SIEMPRE desglosado por clase territorial (clases 1, 2 y 3; A4, método A) en el informe técnico, el WP, el brief, lo que sabemos, el artículo del Colegio, la ponencia y LinkedIn, con la literatura que fija cada extremo:
  - extremo bajo, oferta elástica: Eriksen y Ross (2015);
  - extremo alto, oferta rígida: Gibbons y Manning (2006) y Hilber y Turner (2014).
  Ya no aparecen rangos que mezclen clases.
- **Pre-registro y versiones.** Diez entregables llevan una nota en la metodología:
  - `prereg-v5` y `v5.0` se crearon en local el 10 de octubre de 2026;
  - la fecha de publicación remota queda «pendiente» (campo que completa el autor);
  - una etiqueta local no es un sello de tiempo externo, así que en el futuro se depositará en OSF o Zenodo antes de estimar.

## T3 y T4 (subagente)
- **Déficit 2021-2024.** Combina las 12 combinaciones de fuentes de M0 con las bajas de T1.
  - Sin bajas: 562.692-688.692 (C1).
  - Con bajas estimadas: hasta 744.144 (C4), frente al antiguo máximo C2 de 902.808, que se basaba en un supuesto de bajas del 0,1-0,2 % que nada observado respalda.
  - 2021-2025: 700.934-826.703 (C4).
- **Necesidad 2026-2035.** Se presentan dos cifras, ambas C4:
  - base (A + R + V + F − M − K, con R de T1): 99.000 / 210.000 / 292.000 al año (mínimo / central / máximo);
  - con la sensibilidad de T2 (liberadas que no llegan al mercado, que SUMAN): 124.000 / 246.000 / 339.000.
  - Los titulares usan la cifra con sensibilidad e indican la base.
  - Las liberadas nunca se restan; check_v5 lo controla con control_liberadas.json.
- **Descomposición de la amplitud.** Movilizables 34 %, flujo futuro 22 %, atraso 21 %, liberadas que no llegan 10 %, reposición 6,5 %, vacancia 5,5 % y cartera 1 %. El supuesto que más pesa es la fracción de vacías movilizables.
- **Frente a las terminadas actuales** (72.000-94.000 al año en el territorio común): la necesidad equivale a 1,5 / 3,0 / 4,1 veces la producción media.
- **T4, dirección y magnitud.** Rejilla de 180 escenarios: los de B2, uno optimista (146.435 terminadas al año, suma de máximos provinciales, por encima de cualquier año nacional desde 2008, aunque muy por debajo de 2006-2007), bajas 0, hogares bajos y liberadas.
  - Dirección nacional 2026-2030: EMPEORA en los 180 escenarios, así que pasa a **C2**. La magnitud (cambio de +87.000 a +947.000) es C4.
  - Provincias: 15 empeoran, 0 mejoran y 37 son indeterminadas (en v5: 20 / 5 / 27).
  - A 2035, la dirección nacional es indeterminada (C4).
  - El envejecimiento libera 870.000 viviendas en 2026-2030 y 987.000 en 2031-2035 (centrales, C4).
- **Verificador.** La ficha T4-V1 sustituye a B2-V1. verificador.py admite ya sustituciones de fichas v5 por fichas v5.1.

## Revisión de v5.1 (T1-T5): REHACER acotado (B1-B2) → corregido por el orquestador
- **B1.** La frase frente a las terminadas usa ahora la misma cobertura que la necesidad: terminadas nacionales con País Vasco y Navarra, 78.810-100.980 al año en 2019-2024. Resultado: 1,4 / 2,7 / 3,8 veces (antes 1,5 / 3,0 / 4,1 con el territorio común) y decimales con coma.
- **B2.** T4-V1 pasa a NO RESPALDADA (C2): la afirmación «se cerrará en pocos años» falla en todos los escenarios. La regla dice qué podría romper la dirección C2; los umbrales están en docs/v5_1/revision.md.
- **No bloqueantes.**
  - Los titulares de los entregables usan la necesidad BASE (sin X: 99.000 / 210.000 / 292.000) y dan X como sensibilidad que SUMA (124.000 / 246.000 / 339.000). X es un flujo bruto hacia la vacancia y sesga al alza.
  - El 0,052 % se rotula «máximo de las demoliciones con licencia», no «máximo de las bajas».
  - T2 fecha el Censo 2021 en el 1-ene-2021.
  - Pendientes, por impacto bajo: la cuota de referencia del desajuste territorial, que L en T3 venga de B1 y el carácter casi tautológico del control de liberadas.
- Son las correcciones que propuso el revisor y no cambian estimaciones: v5.1 (T1-T5) queda APROBADA.
