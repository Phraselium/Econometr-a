# Respuesta al arbitraje del informe integral (V16, fase 7)

Árbitro independiente (arbitro-final), primera ronda, 2026-10-18. Veredicto: **REVISAR**, con 23 hallazgos. Se añaden los del verificador de cifras (verificador-cifras): 22 discrepancias claras y 3 casos límite.

Cada hallazgo se corrige o se rebate. Ninguna corrección cambia una cifra de la 1.0 ni sube una capa. Las cifras nuevas son lecturas de resultados ya versionados (src/v16/f7_hechos.py):
- V16-HEC-IPV-NOM/REAL-2019-2025;
- V16-T4-H2-min-interp;
- V15-H5-razon-replica;
- V15-H4-mediana;
- V16-Q3-b-mediana.

## Árbitro

| # | Gravedad | Hallazgo | Respuesta |
|---|---|---|---|
| 1 | alta | El resumen ejecutivo daba cifras de resultados que no superan sus pruebas | **Corregido.** «Sin hallazgo robusto» va sin cifras: una línea por resultado con capa y razón. Las magnitudes quedan en las Partes II, IV, V y VII. |
| 2 | alta | «Evidencia en contra» para un tope que baja la renta del conjunto del mercado | **Corregido.** Pasa a «Sin evidencia»: los estudios con diseño discrepan en el signo del desbordamiento. |
| 3 | alta | La etiqueta VERIFICADA no seguía la definición del repositorio, y «Eficacia probada» era demasiado fuerte | **Corregido.** La etiqueta pasa a «DOI verificado; cuartil no verificado», también en los Anexos A y D. «Eficacia probada» exige al menos dos estudios con diseño leídos completos; el tope del contrato regulado queda en «Prometedora». |
| 4 | alta | Varas distintas entre instrumentos | **Corregido.** La regla de umbral está al inicio de la Parte III y se aplica a todas las fichas. Cada afirmación sigue el objetivo declarado del instrumento: las ayudas a la demanda se separan en asequibilidad del beneficiario y traslación al precio. |
| 5 | alta | Faltaban instrumentos del plan | **Corregido.** Nueva tabla III.12 con los no cubiertos y su razón: tope del 2 % y del 3 % a rentas vigentes, desahucios, incentivos fiscales y planes estatales. Indica también dónde van los avales ICO y la golden visa. |
| 6 | alta | Formato «valor (mín.-máx.)» en cifras que no son rangos | **Corregido.** T4-H3 se da como «empeoran / mejoran / indeterminadas». Q9-g como «estadístico; valor crítico». H5 separa el rango entre implementaciones (réplica y producción) del multiverso de 60 especificaciones. |
| 7 | media | Medidas de precio discrepantes sin cifrar | **Corregido.** El IPV del INE de 2019-2025, nominal y real [C4], va junto al precio por m² [C1] en el resumen y en la Parte I. I.7 declara la medida y el deflactor. El ejemplo de VI.2 usa una sola medida. |
| 8 | media | Dos cambios de hogares sin conciliar | **Corregido.** dh_2125 (C1 de la 1.0) combina la ECP a 1 de enero y la EPA en media anual (K4b-dh). La cifra de V16 alinea ambas al 1 de enero, y por eso su extremo EPA es mayor. La cifra C1 no cambia. |
| 9 | media | Estado de V71-S3-R6 contradictorio | **Corregido.** Su ficha estaba incompleta y la réplica la reprodujo al bit tras completar los supuestos (K19). Sus cifras son C4 y no sostienen veredictos C2. |
| 10 | media | «La vivienda pública resolvería el problema» con C2 en compra | **Corregido.** Pasa a ANALIZADA, NO CONCLUYENTE [C4]. El PARCIALMENTE (C2) de la ficha V11 de la 1.0 se refiere al esfuerzo de acceso, no al precio de compra. |
| 11 | media | Afirmaciones de efecto sin «en la simulación» | **Corregido** en V.2 y en las filas del verificador. |
| 12 | media | Estado del DM-HLN, cifras de Q10 y alcance de la fila de modelos | **Corregido.** DM-HLN tiene una sola frase de estado (apto bajo V15, no apto bajo V16, no se usa como prueba), y el p ya no se cita. Q10 va sin cifras en todo el informe. La fila de modelos lleva el alcance «agregado nacional trimestral» y la nota sobre los 6 de 9 de v6. |
| 13 | media | Faltaban limitaciones transversales en el resumen | **Corregido.** El resumen dice: Monte Carlo casi todo no apto; cegado parcial de las réplicas (K19); evaluate_v16 no aplica y V16 no tiene evaluación sellada pendiente; las de V15 tienen calendario. III.1 se corrige igual. |
| 14 | media | Omisiones del plan fuera de las desviaciones | **Corregido.** Nueva D9 en metodologia/desviaciones_v16.md: metaanálisis, bayesiano jerárquico, GRF/DML (BLP/GATES), BY en lugar del BH jerárquico y condición (b). El Anexo C remite a D1-D9. |
| 15 | media | `cifra-libre` para cifras sustantivas | **Corregido** para el mínimo alternativo de T4-H2, que pasa a V16-T4-H2-min-interp [C4]. **Rebatido** para «N 13.442 → 13.417» del anexo de reproducibilidad: es un recuento del proceso de réplica (K16), no una cifra de resultado, y se rotula así. |
| 16 | media | Compradores extranjeros frente a no residentes | **Corregido.** Se rotulan por separado. R1A-H1 es no residentes. Se concilia con Q8 (otra tabla, otro ámbito, otra ventana). La asociación bivariada (R1A-H4) y la de «con controles» (R1A-H5) se citan con su id. |
| 17 | media | «Ninguna corrección cambia una conclusión de la 1.0» es demasiado fuerte | **Corregido** en el anexo de erratas: no cambia la conclusión de fondo, pero sí la afirmación sobre los niveles y las series autonómicas. |
| 18 | baja | Errores de sustitución (unidades duplicadas, años con separador, Summary con español) | **Corregido.** Se usan :num, :valor, :min y :max con texto propio; los años van literales; el Summary va sin frases en español. Comprobado en la versión ensamblada: no quedan palabras duplicadas. |
| 19 | baja | Precisión insuficiente en Q3-b | **Corregido.** Q3-b y su pretendencia van con :num (todas las cifras significativas). |
| 20 | baja | Referencias colgantes y C2 solo en el resumen | **Corregido.** Se quitaron las referencias colgantes. B1-H4, B2-H3, la demanda latente y las viviendas turísticas [C2] aparecen en el cuerpo (I.5, I.6, I.7 y V.1). |
| 21 | baja | Dos rangos de terminadas | **Corregido.** II.2 declara el ámbito de E-T7-prod (52 provincias, libres y protegidas) frente a terminadas_1924 (territorio común). |
| 22 | baja | Falta V9 sobre la Ley 11/2020 en III.2 | **Corregido.** V9-D1b-renta-att [C4], que no supera la robustez, va en «Nuestra estimación». |
| 23 | baja | Neutralidad | Sin cambios: el árbitro no encuentra problemas de partidos ni personas. La asimetría de vara se resuelve con el hallazgo 4. |

## Verificador de cifras

| Punto | Respuesta |
|---|---|
| 1-3 (marcadores, capas, periodos) | Sin discrepancias. Los dos matices de periodo («fase 6 de V16» en el q de Q9-g; «1-1-2021 a 1-1-2025» frente a «2021-2025») son de notación y no cambian la cifra. |
| 4 (números libres sin comentario) | **Corregido.** Las líneas con umbrales, categorías de diseño, leyes, versiones y niveles de intervalo llevan `check:cifra-libre`. |
| 5 (lista citable) | **Corregido.** Ningún V16-Q1-* va con cifra, y Q9-g no se nombra fuera de la Parte VII y los anexos. T4-H2 y T4-H3 son cifras de la 1.0, no de la lista restringida (que cubre H2 de V15), y se mantienen. El limítrofe V16-Q6-cambios cuenta los cambios del ITP del calendario, no un resultado de Q6-v, y se mantiene. |
| 6 (H1 solo el signo) | **Corregido.** Se quitan V15-H1-lee y las frases sobre la cota de Lee; solo queda el signo. |

## Estado
Tras las correcciones, `make v16_f7` ensambla el informe sin marcadores sin cifra ni «[FALTA CIFRA]», y check_v16 no da errores (lenguaje causal incluido). La segunda ronda de verificación se anota en docs/v16/decisiones.md (K23).

## Segunda ronda (2026-10-18)
El árbitro dio **REVISAR (menor)**: 14 hallazgos resueltos, 5 en parte y 2 sin resolver, más 4 problemas nuevos (N1-N4). El verificador encontró 12 discrepancias menores y ninguna en ids, capas ni lista citable. Respuesta:

| Punto | Respuesta |
|---|---|
| 12 (p del DM-HLN) | **Corregido.** Se quita de VII.10 y del anexo B; solo queda la frase de estado. |
| 19 (redondeo) | **Corregido.** Nuevo formato `{{id:sig}}` (3 cifras significativas) en src/v5/render.py, aplicado a Q3-b, H3, Q6-p y al p y la q de Q9-g. |
| 8 / N4 (hogares) | **Corregido.** El 8,2 % se atribuye a la ventana alineada al 1 de enero (V16-CON-HOG-CAMBIO). dh_2125 se describe en el cuerpo y en el Summary como combinación de la ECP a 1 de enero y la EPA en media anual. |
| N1 (Parte III frente a las cotas C2 de la 1.0) | **Corregido.** III.1, III.6, III.7, III.8, III.10, V.2 y el verificador de la VI recogen los signos [C2] vigentes de la 1.0 en la rejilla simulada: vacías y construcción con signo estable; vivienda pública con signo débil (V11 PARCIALMENTE para el esfuerzo, sin signo C2 en el precio de compra); y ayudas a la demanda con mejora del beneficiario como grupo (D1-V1). III.8 pasa a «Prometedora». Ninguna capa sube ni baja. |
| 14 (D9) | **Corregido.** D9 se declara anotada después de ver los resultados e incluye la calibración de los cuatro cuadrantes por área urbana, que no se hizo. `make publicacion` la lleva a metodologia/desviaciones_v16.md. |
| 6 y 18 (formatos y restos) | **Corregido.** Rangos degenerados con `:valor`, Q7 con valor y rango por separado, duplicaciones eliminadas («del del», «de de»), Summary sin unidades en español, id R1A-H4 añadido y «9 tareas» de v6 tomado de cifras_clave (K1-N-MEJOR). **Rebatido en parte:** el formato por defecto «valor (min-max unidad)» repite la unidad dentro del paréntesis. Es el formato de todos los entregables de la 1.0 (src/v5/render.py) y se mantiene por coherencia. |
| N2 (VI.7) | **Corregido.** Se quita la frase sin dato. |
| Menores | **Corregido.** El alcance del resumen admite las cifras [C4] necesarias para dar ambas medidas. La sobrecarga de la UE se rotula como extremo del rango del indicador, porque no tiene id propio. Las líneas con números del diseño llevan `check:cifra-libre`. |
| Verificador, periodo de B2-H3 | Notación distinta de la misma ventana («1-ene-2026 a 1-ene-2031» frente a «2026-2030»). No cambia la cifra y se mantiene. |
| Verificador, etiquetas «H2»/«R1A-H1» | Son T4-H2 (déficit) y R1A-H1 (no residentes) de la 1.0, no H2 y H1 de V15. Aparecen siempre con su prefijo completo. |
