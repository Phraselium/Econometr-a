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
