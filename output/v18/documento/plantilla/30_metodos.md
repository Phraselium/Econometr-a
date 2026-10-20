## 3. Métodos

### 3.1 Diseños por factor

| Factor | Diseños (identificadores del plan) | Estimación propia designada para la magnitud preferida |
|---|---|---|
| E1 Vivienda turística | Estudio de eventos de dosis con el registro HUT (R3); diferencias en diferencias radio-anillo en torno a la Sagrada Família (R4); IV de tipo shift-share con atractivos y búsquedas de Google (R2, A1) | E1-A1 (respaldo E1-R2) |
| E2 Topes al alquiler | Diferencias en diferencias con la Ley 11/2020 sobre renta y número de contratos de Incasòl (R1, R1c); zonas tensionadas de 2024 y otras comunidades (A1, A2); desbordamiento y desplazamiento (A3, A4) | E2-R1 (respaldo E2-A1) |
| E3 Inmigración | IV por asentamientos históricos de cada nacionalidad en provincias (R1, R2, A1 a A5) | E3-R2 (respaldo E3-A1) |
| E4 Ayudas a la demanda | Incidencia de las ayudas con microdatos de perceptores (X1) | ninguna (solo literatura) |
| E5 Oferta y suelo | Bartik de empleo por ramas para la elasticidad de la oferta (R1); interacción con el suelo (A1) | E5-R1 |
| E6 Obra nueva | Diferencias en diferencias por distancia a edificios nuevos (R1, A1); IV con lluvia como en Mense (R2) | E6-R2 |
| E7 Tipos de interés | Proyección local con instrumento (R1); SVAR con proxy (R2); BVAR recursivo, réplica de San Juan (R3, A1); panel provincial con exposición hipotecaria (A2) | E7-R1 (respaldo E7-R2) |
| E8 Fiscalidad de la compra | Diferencias en diferencias de dosis continua del tipo general del ITP (R1 precio, R2 volumen, A2 municipal) | E8-R1 (precio), E8-R2 (volumen) |
| E9 No residentes | Shift-share por riesgo en el país de origen (R1, R2, A1, A2) | E9-R2 |
| E10 a E12 | Asociación transversal (E10); calendario de recargos (E11); IV provincial con vivienda protegida (E12) | ninguna |
| F1 a F3 | Corrección del error, DOLS y PMG, CS-ARDL en panel; modelo de alquiler y de oferta | ninguna |

### 3.2 Inferencia

Se publica siempre la inferencia convencional que corresponde a cada diseño. Los errores típicos se agrupan al nivel del tratamiento. Con pocos clusters se usa el wild cluster bootstrap con pesos de Webb. En shift-share se usan los intervalos de Anderson-Rubin y el F efectivo de Montiel Olea y Pflueger, con el número efectivo de choques (inverso del índice de Herfindahl de los pesos, de Borusyak, Hull y Jaravel) calculado antes de estimar. También se usan Conley en datos espaciales, Driscoll-Kraay en paneles con dependencia transversal y Newey-West en series. Cuando el número de clusters es muy pequeño (ocho comunidades), la inferencia por aleatorización del calendario sustituye a Webb.

Cada herramienta se valida antes por Monte Carlo con procesos generadores que reproducen la estructura de los diseños (anexo E). Un resultado «apto» tiene tamaño y cobertura dentro de las bandas de la adenda 1.12. «Con valor crítico corregido» obliga a publicar el p-valor con el valor crítico calibrado en la simulación. «No fiable» se publica con esa etiqueta y la clasificación no puede apoyarse en él. Las herramientas NO APTAS (por ejemplo, la proyección local con Newey-West, el SVAR con proxy, el BVAR y el metaanálisis bayesiano) se publican con esa etiqueta y su resultado se lee como informativo.

### 3.3 Clasificación V18

La clase se asigna con las reglas del plan (B3 y criterios I1 a I8, revisados en la adenda 1.2), sin elegirla por el p-valor:

- **IDENTIFICADO.** Diseño creíble, primera etapa fuerte o intervalo de Anderson-Rubin acotado, pretendencias y placebos superados, robustez, significación tras Holm, réplica ciega coincidente y ningún tope de la especificación. Ninguna estimación de V18 llega a esta clase.
- **SUGESTIVO.** Diseño creíble y réplica ciega coincidente, sin fallo decisivo, con alguna prueba débil o un tope fijado en la adenda. Se dice «la evidencia sugiere», con la limitación concreta.
- **NO CONCLUYENTE (sin potencia).** Diseño válido sin significación y sin equivalencia demostrada por la prueba TOST.
- **ASOCIACIÓN.** Diseño no creíble o fallo decisivo (por ejemplo, un cambio de signo en una prueba B4 o un placebo de fecha significativo del mismo signo).
- **NO ESTIMABLE.** Falta un dato imprescindible o la comprobación previa de variación no alcanza el mínimo.

Tres lecturas decididas antes de difundir resultados (docs/v18/decisiones.md). Un cambio de signo en una prueba de robustez del plan es un fallo decisivo y no se compensa con un tope (K7). Un coeficiente no significativo es NO CONCLUYENTE si supera los criterios de diseño y ASOCIACIÓN si no los supera (K7). Cuando la ficha admite dos lecturas con clases distintas se toma la más prudente (K8 bis). La etiqueta de coherencia con la literatura (I6) se publica, pero no interviene en la clase ni en la entrada en la magnitud preferida. Un resultado sin réplica ciega coincidente no se clasifica.

Capa y lenguaje (K2). Toda cifra V18 es de capa C4, con nivel de evidencia EXPLORATORIO. La clase V18 va en un campo propio al lado de la capa y no la promueve. Cada cifra se lee como asociación condicionada al diseño. La fórmula condicional prevista para la clase IDENTIFICADO solo cabría en la sección 4 y en los anexos, y no se ha necesitado.

### 3.4 Estimabilidad previa por magnitud mínima detectable

Antes de estimar cada especificación principal, y sin mirar su resultado, se calcula por Monte Carlo la magnitud mínima detectable (MDE) con la potencia convencional fijada en la adenda 1.3. El cálculo usa la variación real del tratamiento, de la exposición o del instrumento y la dispersión residual de V15 o V16 (declarada «ya vista») o la del periodo previo. La especificación es estimable si el MDE no supera la magnitud de referencia de la literatura convertida a nuestra unidad. Si no, es NO ESTIMABLE por variación y se publica el MDE, no el coeficiente. Además se exigen mínimos de datos (por ejemplo, un número mínimo de municipios tratados y de control) y, en shift-share, un número efectivo de choques suficiente. Esta comprobación explica la mayoría de los NO ESTIMABLE.

### 3.5 Magnitud preferida (B5, adenda 1.9)

- **Qué entra.** La estimación propia designada de cada factor, si su diseño es válido y es IDENTIFICADO, SUGESTIVO o NO CONCLUYENTE, con independencia de su p-valor. No entran las ASOCIACIÓN ni las NO ESTIMABLE. Los estudios de la literatura entran si están en la misma unidad y tienen error típico.
- **Episodios compartidos.** Si una estimación propia y un estudio miden el mismo episodio con la misma fuente, el episodio cuenta una vez, combinado con una correlación modelada fijada en la adenda.
- **Modelo.** Metaanálisis bayesiano de efectos aleatorios con tres priors sobre el efecto medio. La magnitud preferida se publica solo si la decisión (signo e inclusión del cero) coincide en las tres. Si no, se publica el rango de las tres sin magnitud preferida. Si la heterogeneidad es alta y el intervalo de predicción cambia de signo, tampoco hay magnitud preferida. Con un solo estudio se publica su magnitud; con dos, el efecto fijo ponderado por precisión. Si las unidades no son comparables, no se combinan.
- **Advertencia de la simulación.** El metaanálisis bayesiano resultó NO APTO por conservador: sus intervalos cubren de más y, con dos estudios y heterogeneidad, el efecto fijo no cubre la media verdadera. Los intervalos con más de dos estudios son prudentes y los de dos estudios no deben leerse como IC95 fiables.
- **Referencias.** Toda referencia lleva el estado de su ficha: VERIFICADA (DOI comprobado con Crossref o DataCite; cuartil no verificado), NO VERIFICADA o DISCREPANTE (la ficha describe una versión de trabajo y el DOI corresponde a la versión publicada; se trata como NO VERIFICADA).
- **Confianza de la tabla de magnitudes.** Regla fija: «media» solo con magnitud preferida de tres o más estudios; «muy baja» si la literatura no tiene error típico en la unidad; «baja» en el resto. Nunca «alta», porque toda cifra es C4. La clasificación de cada fila es la de la estimación propia designada del factor; la magnitud preferida puede venir solo de la literatura.

### 3.6 Contabilidad de la subida (adenda 1.10)

La contribución de un factor es su magnitud preferida por su variación observada en el periodo y el territorio, con la incertidumbre propagada por Monte Carlo sobre la magnitud y una fila «no explicado». Es contabilidad con elasticidades estimadas, no una descomposición estructural: no hay interacciones ni efectos de equilibrio general, y los factores no son ortogonales. Reglas:

- Un factor sin magnitud dice «sin magnitud», no cero.
- Cada contribución de un diseño de panel con efectos de periodo se rotula «relativa entre provincias (o unidades), sin el componente común». Solo los tipos (E7, series nacionales) incluyen el componente común.
- Cada fila dice si la variación observada del factor está dentro o fuera del soporte de la muestra de estimación. Fuera del soporte no lleva cifra.
- Inmigración (E3) y no residentes (E9) usan cuotas del padrón por nacionalidad y no se suman: E9 va como alternativa de E3.
- **Lectura restrictiva aplicada.** La adenda admite todo factor con magnitud preferida construida con las reglas de B5. El plan deja las magnitudes «solo literatura» en una tabla secundaria rotulada, y una magnitud sin estimación propia no tiene clase que limite la confianza. Se aplicó la lectura restrictiva (K10): la tabla principal solo admite factores con estimación propia dentro de B5. Ninguno la cumple. Las magnitudes de la literatura van en una tabla aparte, rotulada ilustración. La lectura inclusiva solo cambiaría de tabla a E1, E4 y E6, y no cambiaría ninguna conclusión.
- La variación observada usa el deflactor del PIB del INE, no el IPC general que usó V8. Las variaciones observadas difieren por eso de las de V8.
- Las viviendas liberadas por envejecimiento nunca se restan de la necesidad (la proyección de hogares del INE ya las descuenta).

### 3.7 Modelos de conjunto (F)

El modelo de precio de largo plazo con corrección del error, el de alquiler y el de oferta se contrastan primero para cointegración, con corrección por pruebas múltiples. Si el contraste no rechaza la ausencia de cointegración, no se publican elasticidades de largo plazo ni sobrevaloración (regla AD-F), y solo se publica la dinámica de corto plazo como ASOCIACIÓN.

### 3.8 Evaluación sellada diferida

La vía a la capa C3 es una evaluación sellada diferida (evaluate_v18) con datos posteriores al tope de entrenamiento, una sola evaluación por hipótesis y un criterio de superación fijado en la adenda 1.11. No se ejecuta dentro de V18, requiere orden expresa del autor y no puede abrirse antes de 2027. Los episodios históricos (Ley 11/2020, el auge anterior a 2010, Barcelona 2011-2019, las cohortes de obra de 2015 a 2018 y los cambios del ITP) no pueden llegar a C3 con la definición actual de capas.

### 3.9 Multiplicidad y registro

Toda especificación, incluidas las variantes y las fallidas, se registra antes de leer su resultado. Se controlan los falsos descubrimientos con Holm dentro de la familia de cada factor y con Benjamini-Yekutieli entre las variantes enumeradas de cada identificador. Ningún modelo se elige por su p-valor. SEED 20261010 en todo lo aleatorio.
