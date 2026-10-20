# V18 · Adenda al plan de replicación (pre-registro interno)

Documento de la fase 3 de V18. Redactado el 2026-10-20 para el autor (Borja Romero). Responde, uno por uno, a los 28 hallazgos de docs/v18/revision_plan/revisor_preregistro.md («R-n») y a los del abogado del diablo, docs/v18/revision_plan/abogado_del_diablo.md («AD-x»), sobre docs/v18/plan_replicacion.md (commit d4e9869), y aplica la decisión K2 del autor (docs/v18/decisiones.md). Los identificadores de especificación son los del plan (V18-E3-R1…); se abrevian sin el prefijo «V18-» cuando no hay ambigüedad.

---

## 0. Naturaleza y alcance

- **Prevalencia.** Esta adenda prevalece sobre el plan donde difiera (plan, 0.1). El plan y la adenda forman juntos el **pre-registro interno** de V18. La etiqueta git local `plan-replicacion-v18` fija el commit que contiene ambos, y la puerta de la fase 4 exige además que ese commit esté en la rama remota (K1). No es un pre-registro depositado en un registro externo y no se describe como tal.
- **Declaración.** Esta adenda se escribe **sin haber mirado ningún resultado de V18**. No existe todavía ninguna estimación de V18 con nuestros datos. Para escribirla solo se han leído metadatos:
  - los manifiestos docs/v15/sellado_v15.json y docs/v16/sellado_v16.json (claves «variable|nivel|frecuencia», fechas de corte y listas de variables de los conjuntos) y los `_manifest.csv` de data/raw;
  - las funciones de src/holdout.py que devuelven listas de unidades selladas, ejecutadas sin abrir datos: `provincias_selladas_v6()`, `ccaa_selladas_v6()`, `municipios_sellados_v15()`, `municipios_sellados_v16()`, `distritos_sellados_v15()` y `distritos_sellados_v16()` (estas dos leen solo los códigos de distrito y municipio de data/base/geo/secciones.parquet);
  - las cadenas de documentación de src/v9/paneles.py y docs/v3/decisiones.md sobre la frecuencia de Incasòl;
  - los PDF de data/bib/pdf de Jofre-Monseny, Martínez-Mazza y Segú (2023), García-López et al. (2020) y González y Ortega (2009).
- **Corrección del inventario (R-2).** src/v18/f0_inventario.py se ha corregido y output/v18/f0/ se ha regenerado con `python3 src/v18/f0_inventario.py`: Incasòl es anual desde 2007 y trimestral solo desde 2019T1, y los contratos por tramo de renta pasan de «parcial» a «falta» (el tramo clasifica al municipio, no reparte contratos). E2 queda con 5 variables disponibles, 1 parcial y 3 que faltan.
- **Pendiente de orden del autor.** Lo que esta adenda prevé en src/holdout.py (funciones `sellar_v18` y `evaluate_v18`, sección 1.11) y en check_v18 (campo clasificacion_v18, sección 1.1) no se escribe aquí: src/holdout.py es compartido y se modifica solo con orden expresa del autor.

---

## 1. Reglas transversales nuevas

Las respuestas de las secciones 2 y 3 remiten a estas reglas. Cada una sustituye al apartado del plan que se indica.

### 1.1 Capas y clasificación (K2 aplicado; sustituye a la última nota de 0.5 y a 0.6, «nivel_evidencia»)
- **Capa.** Toda cifra de V18 es **C4**, con `nivel_evidencia = "EXPLORATORIO"` en resultado.json. Ninguna clasificación V18 cambia la capa (CLAUDE.md, «nunca promover de capa»).
- **Campo nuevo.** La clasificación V18 va en el campo `clasificacion_v18` de resultado.json, al lado de `capa` y `nivel_evidencia`. Valores posibles: `IDENTIFICADO`, `IDENTIFICADO (efecto nulo acotado)`, `SUGESTIVO`, `SUGESTIVO (efecto nulo acotado)`, `NO CONCLUYENTE (sin potencia)`, `ASOCIACIÓN` y `NO ESTIMABLE`. Las especificaciones coprincipales «P» (sección 1.6) llevan `no se clasifica`.
- **Clase nueva: NO CONCLUYENTE (sin potencia).** Diseño válido (I1 a I5 e I8 superados), sin significación (p ajustado por Holm ≥ 0,10) y sin equivalencia demostrada por TOST con el δ de su especificación (Anexo B). No es una asociación: el diseño es válido y la estimación no decide.
- **Nulo acotado.** Sustituye a la regla «nulo identificado» de 0.5. Con el diseño válido, la equivalencia se contrasta por TOST al 5 % (intervalo al 90 % dentro de ±δ, con el δ de su especificación del Anexo B). Si se cumple, la clase es «IDENTIFICADO (efecto nulo acotado)», o «SUGESTIVO (efecto nulo acotado)» si la especificación tiene ese tope.
- **Lenguaje.**
  - En IDENTIFICADO solo cabe la fórmula condicional «con los supuestos [lista], el diseño identifica…», y solo en las secciones técnicas del Documento de Trabajo (resultados por factor y anexos).
  - Nunca va en cifras_clave, en la web, en la consulta, en el resumen ejecutivo ni en el resumen no técnico.
  - check_v18 rechaza el lenguaje causal en todas las cifras V18, también en IDENTIFICADO (K2).
  - Se suprime la frase del plan (0.5) según la cual check_v18 lo rechazaba «en toda cifra que no sea IDENTIFICADO».
- **Vía a C3.** Solo la evaluación sellada diferida evaluate_v18 de la sección 1.11.

### 1.2 Criterios I1-I8 revisados (sustituye a los de 0.5)
- **I1** sin cambios.
- **I2 · Fuerza de la primera etapa.** Se supera con F efectivo de Montiel Olea-Pflueger > 10, o con el conjunto de Anderson-Rubin al 95 % acotado (finito). No se exige que el AR excluya el cero: la significación es cosa de I7.
  - Con F efectivo < 10, el tope es SUGESTIVO aunque el AR esté acotado.
  - Con F efectivo < 5 y AR no acotado, el fallo es decisivo: ASOCIACIÓN.
- **I3 · Pretendencias.** Se mantiene el texto de 0.5 y se añade una condición de potencia (AD-T4).
  - En cada estudio de eventos y en cada shift-share se publica la pendiente lineal previa detectable al 80 % (Roth, 2022) con la covarianza de los adelantos estimados.
  - El sesgo que esa pendiente implicaría en la ventana posterior debe ser menor que la mitad de |referencia| (Anexo B). Si no, tope SUGESTIVO.
- **I4** sin cambios, salvo donde la sección 2 declara un placebo «no aplicable».
- **I5 · Robustez.** El 80 % del multiverso con el mismo signo se cuenta solo sobre las variantes enumeradas del Anexo A, nunca sobre la holgura.
- **I6 · Coherencia con la literatura: etiqueta, no criterio** (AD-T1 y R-13).
  - Se calcula con una referencia única por especificación (Anexo B).
  - Es «coherente» si la razón entre nuestra estimación y la referencia está en [1/3; 3].
  - La vía del solapamiento de los IC95 solo vale si el error típico de la referencia es menor que la mitad de su coeficiente y el IC95 propio no es más de 3 veces más ancho que el de la referencia.
  - Se publica siempre como etiqueta («coherente / no coherente con [referencia], razón r»).
  - No interviene en la clasificación ni en la entrada en B5.
- **I7 · Significación.** p < 0,05 tras Holm dentro de la familia (sección 1.7), con el valor crítico corregido por tamaño cuando el tamaño del Monte Carlo cae fuera de [0,04; 0,06] (sección 1.12).
- **I8** sin cambios.
- **Reglas de clasificación (sustituyen a las de 0.5):**
  - **IDENTIFICADO:** I1-I5, I7 e I8, sin ningún tope de la especificación que lo impida.
  - **SUGESTIVO:** I1 e I8, sin fallo decisivo, con al menos una prueba débil de la lista de 0.5, o con un tope de los fijados en esta adenda.
  - **NO CONCLUYENTE (sin potencia):** el de la sección 1.1.
  - **ASOCIACIÓN:** diseño no creíble o fallo decisivo (lista de 0.5, con I2 como arriba).
  - **NO ESTIMABLE:** falta un dato imprescindible o la especificación no supera la regla de estimabilidad de la sección 1.3.

### 1.3 Regla común de estimabilidad por MDE (R-10 y R-28; sustituye a todas las «comprobaciones previas» numéricas del plan)
- **Cuándo.** Antes de estimar cada especificación principal, sin mirar su resultado.
- **Qué se calcula.** El efecto mínimo detectable (MDE) al 80 % de potencia, contraste bilateral al 5 % y con la inferencia principal de la especificación, por Monte Carlo:
  - R = 2.000 réplicas, SEED = 20261010;
  - variación real del tratamiento, de la exposición o del instrumento, que se lee después de la etiqueta y nunca junto al resultado;
  - σ residual del resultado tomada de V15 o V16 para el mismo resultado y la misma unidad, **declarada como «ya vista»** en el registro;
  - si V15 y V16 no tienen ese σ, se usa el σ del resultado tras los efectos fijos de unidad y de periodo **solo en el periodo previo al tratamiento**, y también se declara.
- **Umbral.**
  - La especificación es estimable si MDE ≤ |referencia única| del Anexo B, convertida a nuestra unidad.
  - Sin referencia, si MDE ≤ 2δ (Anexo B).
  - Si no, «NO ESTIMABLE por variación», con el MDE publicado. La especificación sale de su familia de Holm.
- **Mínimos de datos** (además del MDE; si no se alcanzan, NO ESTIMABLE):

| Id | Mínimo |
|---|---|
| E1-R1 | ≥ 20 barrios cuyo stock HUT cambia al menos un 10 % entre el primer y el último valor anual, con el stock del primer valor anual como denominador |
| E2-R1, R1c | ≥ 30 municipios tratados y ≥ 30 de control tras el sellado y las exclusiones, con al menos un contrato en cada trimestre (panel equilibrado, como JMS, p. 8) |
| E2-A2 | ≥ 3 trimestres posteriores por cohorte y ≥ 10 municipios tratados no sellados |
| E6-R1 | ≥ 30 secciones tratadas y ≥ 30 de control |
| E8 | ≥ 8 cambios efectivos del tipo general en ≥ 4 CCAA |
| E9-R1, R2 | 1/HHI de los choques ≥ 10 (sección 1.13) |

- **Definiciones que resuelven las ambigüedades señaladas en R-10:**
  - El valor anual del registro HUT es el corte más cercano al 31 de diciembre. Con dos cortes equidistantes, el anterior. Un año sin corte a menos de 3 meses queda vacío, sin interpolar.
  - El denominador del HUT por 100 viviendas son las viviendas del Censo 2021 por sección, fijas en el tiempo.
  - Se suprimen el umbral de 0,25 licencias por 100 viviendas y el de «10 % entre cortes» del plan.

### 1.4 Sellado temporal: regla de frecuencia (R-3; completa 0.3)
- **(a)** Para la variable v, el nivel n y la frecuencia f usada, el tope es la clave «v|n|f» de sellado_v16.json. Si existe también en sellado_v15.json, manda la menor de las dos (como en src/holdout.py, sellar_v16).
- **(b)** Una media anual construida desde datos trimestrales o mensuales solo incluye años que cumplen dos condiciones:
  - no son posteriores a la clave anual «v|n|A», si existe;
  - están completos bajo la clave de la frecuencia de origen.

  Ejemplo: el valor tasado provincial tiene la clave T en 2026T2 y la clave A en 2024, así que las medias anuales llegan a 2024.
- **(c)** Si la frecuencia usada no tiene clave, pero la variable sí la tiene en otra frecuencia del mismo nivel, el tope es el final del periodo más antiguo entre esas claves. Ejemplo: las compraventas provinciales mensuales llegan a 2024-12.
- **(d)** Si la variable figura en un conjunto de V15 o V16 y la combinación «v|n» existe en la base sin ninguna clave, esa combinación está sellada entera (src/holdout.py:711, `tope.isna()`): no se usa.
- **(e)** Si la variable no figura en ningún conjunto ni pregunta de V15 o V16, no pertenece a ninguna muestra sellada anterior. Su tope para V18 es el último periodo presente en el repositorio en el commit de la etiqueta, y se registra en docs/v18/sellado_v18.json. Así ocurre con base:bcn_hut_registro, base:eurostat_plataformas_noches, base:sepe_paro_registrado_media_anual, base:deflactor, base:pib_vol_idx, base:costes_constr, base:credito_promotor, base:tx_extranj_ccaa y base:aeat_irpf_renta_disponible_media.
- **(f) Sustitutos.** Una serie que mide la misma magnitud al mismo nivel que una variable con clave hereda su tope, aunque tenga otro nombre o venga de data/raw. Así, base:ecp_pob_nacionalidad hereda 2022 de padron_pob_nacionalidad, y las entradas por nacionalidad de data/raw/ine_migraciones_nacionalidad.csv heredan 2024 de ine_emcr_inmigraciones_exterior_personas.
- **(g) Ediciones.** No se usan las publicadas después de 2026-10-17 (fecha de corte común de V15 y V16) en las variables con clave, ni las posteriores a la etiqueta en las de (e).
- **docs/v18/sellado_v18.json** se genera después de la etiqueta y antes de la primera estimación, con estas reglas. Sus valores quedan determinados por la regla, sin elección. Lo usan sellar_v18 y evaluate_v18 (sección 1.11). Los cortes que resultan para cada especificación están en el Anexo C.

### 1.5 Sellado espacial: distritos sellados y totales municipales (R-20)
- **Distritos sellados de las grandes ciudades** (cálculo con `distritos_sellados_v15()` y `distritos_sellados_v16()`, sin abrir datos; códigos INE de distrito censal):

| Municipio | Distritos censales | Sellados V15 | Sellados V16 | Secciones selladas / total |
|---|---|---|---|---|
| Barcelona (08019) | 10 | 0801906 (Gràcia), 0801909 (Sant Andreu) | 0801908 (Nou Barris) | 299 / 1.068 |
| València (46250) | 19 | 4625004, 4625010, 4625016 | 4625009, 4625019 | 166 / 588 |
| Sevilla (41091) | 11 | 4109102, 4109111 | 4109110 | 106 / 522 |
| Málaga (29067) | 11 | 2906701, 2906708 | 2906705 | 79 / 435 |
| Alicante (03014) | 8 | 0301402 | 0301405 | 50 / 246 |
| Bilbao (48020) | 8 | 4802007 | 4802008 | 59 / 271 |

  - En Barcelona, los 10 distritos censales coinciden con los 10 distritos municipales. Por eso los nombres de la tabla son los de la ciudad.
  - En las demás ciudades, la correspondencia de cada distrito censal con los distritos y barrios municipales, en particular con los centros históricos, se comprueba con la correspondencia oficial antes de estimar. Esa comprobación no abre datos de resultado.
- **Efecto en Barcelona (E1).**
  - Salen los 25 barrios de Gràcia (5), Nou Barris (13) y Sant Andreu (7). Quedan 48 de 73.
  - El plan decía «unos 60 clusters tras el sellado» y se corrige a 48 como máximo. Son más de 40: el cluster por barrio es válido, y el bootstrap de Webb va siempre al lado.
  - **E1-R1** no pierde Ciutat Vella ni l'Eixample, los distritos de más densidad de viviendas turísticas. Sí pierde los barrios de Gràcia, entre ellos la Vila de Gràcia y el Camp d'en Grassot i Gràcia Nova, de densidad alta. La pérdida exacta de exposición se mide con el registro HUT tras la etiqueta, sin el resultado, y se publica.
  - **E1-R4** conserva el templo y sus secciones tratadas: el barrio de la Sagrada Família está en l'Eixample (0801902, no sellado). Del anillo de 500-1.000 m se excluyen las secciones que caigan en Gràcia (0801906). Si la exclusión deja el radio de 500 m o el anillo con menos del 75 % de sus secciones, R4 es NO ESTIMABLE. El recuento se hace con la geometría antes de estimar.
- **Totales municipales: se mantiene la convención de V15 y V16** (docs/v15/preregistro_v15.md, sección 2).
  - Los municipios con 5 distritos o más nunca se sellan enteros, y su agregado municipal está en entrenamiento aunque contiene distritos sellados: es una fuga declarada.
  - V18 la declara en cada diseño municipal (E2-R1, E2-A1, E2-A3, E2-A4, E3-A3, E5-A3, E8-A2 y E10-A1).
  - En cada uno añade la variante «sin los municipios con distritos sellados» (Anexo A).
  - No combina en un mismo modelo los datos por sección y los municipales de esas ciudades.
- **Municipios sellados por provincia** (V15 + V16), que reducen los diseños municipales:

| Provincia | Municipios sellados |
|---|---|
| Barcelona | 83 |
| Lleida | 86 |
| Tarragona | 7 |
| Girona | 0 |
| València | 101 |
| Alicante | 38 |
| Castellón | 35 |
| Málaga | 41 |
| Sevilla | 37 |
| Bizkaia | 107 |
| Gipuzkoa | 79 |
| Araba | 6 |

### 1.6 repite_visto y coprincipales «P» (R-8; AD, «especificaciones elegidas conociendo un resultado previo»)
- **Cuándo se marca.** Se marca `repite_visto` toda especificación que coincide con una ya estimada en el proyecto en resultado, exposición o tratamiento, unidad y periodo, aunque sea en parte. La lista mínima está en la tabla consolidada. Antes de estimar se repasa además metodologia/historial_conclusiones.md, y toda coincidencia nueva se marca y se anota en desviaciones.md.
- **Coprincipal «P».** Por cada coincidencia se estima al lado la especificación anterior exacta como coprincipal, con el identificador V18-<factor>-P-<origen>:
  - código, variables, periodo y estimador de la versión etiquetada de origen;
  - en la muestra V18, con las exclusiones de v6, V15 y V16, porque reejecutarla en su muestra original leería unidades que V16 selló después.
- **Holm y clasificación.** La P entra en la misma familia de Holm que su especificación V18. No se clasifica: no cambia la clase de lo publicado y su cifra publicada se muestra al lado.
- **Tope por corrección de un fallo conocido.** Si la clase V18 es mejor que la que daría la P solo por un cambio que corrige un fallo ya conocido de la P, la especificación V18 tiene tope SUGESTIVO. Lista fijada ahora:

| Especificación | Cambio que corrige un fallo conocido |
|---|---|
| E1-A1 | Instrumento nuevo tras el nulo de H3 |
| E2-R1 | Grupo de control y ventana tras la pretendencia de V9-D1b |
| E3-R1, R2 | Año base 2001 tras el F de 3,4-4,6 de V9-D4 |
| E5-R1 | Bartik en lugar de la Red Natura tras Q4 |
| E7-R1, R2 | Ninguno: el instrumento es el mismo que en Q5 y V8, y se dice |
| E8-R1, R2 | Fechas corregidas tras Q6 |

### 1.7 Multiplicidad (R-24; sustituye a 0.6 y a las familias de la sección 6)
- **Composición de las familias.**
  - Cada familia la forman las especificaciones principales que pueden llegar a SUGESTIVO o IDENTIFICADO, más sus coprincipales P.
  - Las de tope ASOCIACIÓN quedan fuera: E1-A3, E5-A1, E7-R3, E7-A1, E10-A1 y toda F.
  - Las P entran aunque su diseño fuera de asociación, porque representan la elección ya hecha.
- **Momento.** El número m de cada familia se fija **después** de las comprobaciones previas (sección 1.3): las NO ESTIMABLES salen antes de ajustar.
- **Familias máximas antes de esas comprobaciones** (lista en la tabla consolidada):

| Familia | Contrastes (máximo) |
|---|---|
| E1 | 9 |
| E2 | 12 |
| E3 | 14 |
| E5 | 4 |
| E6 | 4 |
| E7 | 11 |
| E8 | 6 |
| E9 | 4 |
| E12 | 2 |
| F | Solo contrastes de cointegración |

- **Variantes.** Las variantes de cada identificador se ajustan con Benjamini-Yekutieli al 10 % (sin cambios).

### 1.8 Multiverso enumerado (R-5; sustituye a «Multiverso acotado» de 0.6 y a la columna de variantes de la sección 6)
- **Variantes enumeradas.** El Anexo A enumera cada variante de cada especificación principal, con su dimensión: control [C], ventana [V], medida [M], peso [P], estimador [E] o unidad y muestra [U].
  - Son **245 variantes**.
  - Con las **86 especificaciones principales y coprincipales** de la tabla consolidada, el multiverso declarado es de 331 especificaciones.
  - Una variante cuyo dato no exista (por ejemplo, el Censo de 1991 o la exposición a cajas) se registra como «no estimable» y no se sustituye por otra.
- **Holgura máxima: 200 especificaciones.**
  - Cada una exige una entrada en desviaciones.md, con motivo, antes de ver su resultado.
  - La holgura no cuenta en I5, no apoya ninguna clasificación IDENTIFICADO y no entra en B5 ni en la contabilidad.
  - El tope total de V18 baja de 1.500 a **531**.
- **Diagnósticos.** Placebos, pretendencias, Rotemberg, primeras etapas y MDE se registran en el Registry como diagnósticos, con su identificador, y no cuentan en el multiverso.

### 1.9 B5 revisado (R-6, R-7, R-25, R-26; AD-T1; sustituye a «Qué entra» y a «Modelo» de la sección 3)
- **Sin filtro por significación.**
  - Entra la estimación propia designada de cada factor si su diseño es válido (I1-I5 e I8 superados), sea cual sea su p.
  - Su clase puede ser IDENTIFICADO, SUGESTIVO o NO CONCLUYENTE, con o sin nulo acotado.
  - No entran las ASOCIACIÓN ni las NO ESTIMABLE.
  - El revisor pedía «I1-I6 e I8». I6 se excluye como filtro por AD-T1, para no sesgar la magnitud preferida hacia la literatura, y se publica como etiqueta.
- **Una estimación propia por factor, fijada ahora:**

| Factor | Estimación propia | Respaldo |
|---|---|---|
| E1 | E1-A1 | E1-R2 |
| E2 | E2-R1 | E2-A1 |
| E3 | E3-R2 | E3-A1 |
| E5 | E5-R1 | — |
| E6 | E6-R2 | — (E6-R1 está en otra unidad: se muestra al lado sin combinarse) |
| E7 | E7-R1 (h = 8, valor tasado) | E7-R2 |
| E8, precio | E8-R1 | — |
| E8, volumen | E8-R2 | — |
| E9 | E9-R2 | — |

  - El respaldo se usa solo si la propia es NO ESTIMABLE por la sección 1.3, es decir, antes de cualquier resultado. Nunca porque la propia salga ASOCIACIÓN o NO CONCLUYENTE.
- **Episodios compartidos con el original.**
  - Si nuestra estimación y un estudio de la literatura miden el mismo episodio con la misma fuente, el episodio entra una sola vez. Su valor es la combinación por inversa de la varianza de las dos estimaciones, con una correlación modelada ρ = 0,8, fijada ahora. Sensibilidad: ρ = 0,5 y ρ = 1 (equivale a quedarse con la más precisa).
  - Episodios compartidos fijados ahora:

| Factor | Nuestra estimación | Estudios del mismo episodio |
|---|---|---|
| E2 | E2-R1 | Jofre-Monseny et al. (2023) y Monràs y García-Montalvo (2023), entre sí también con ρ = 0,8 |
| E3 | E3-R2 | González y Ortega (2011/2013) |
| E7 | E7-R1 | San Juan (2023), por la misma serie nacional |

  - Si se usa el respaldo de E2, E2-A1 comparte episodio con Pérez García (2026).
- **Priors.**
  - Tres variantes de la prior de μ: N(0, s_f²), N(0, (2·s_f)²) y N(0, (s_f/2)²), con los s_f de la sección 3.
  - La magnitud preferida se publica solo si la decisión coincide en las tres: el signo de la mediana de μ y si el intervalo de credibilidad al 95 % excluye el cero. Si no coinciden, se publica el rango de las tres sin magnitud preferida, y se dice.
  - τ semi-Cauchy sigue como sensibilidad adicional.
- **Con y sin I6.** B5 se publica también sin las estimaciones, propias o de la literatura, que no sean coherentes por I6 (AD-T1).
- **Referencias.** Toda referencia de B5 y de I6 lleva el estado de su ficha (VERIFICADA, NO VERIFICADA o DISCREPANTE, Anexo B) en la tabla publicada (R-26).

### 1.10 Contabilidad de la subida (R-21; AD-T2, AD-T5; completa la sección 4)
- **Entrada de los factores.**
  - La contabilidad principal usa todo factor con magnitud preferida de B5, construida con las reglas de la sección 1.9.
  - Cada fila lleva la clase de su estimación propia, y la confianza no supera la de esa clase.
  - Un factor sin magnitud dice «sin magnitud», no cero.
  - Se suprime el filtro «al menos una V18 IDENTIFICADO o SUGESTIVO», que reintroducía la significación.
- **Respuesta acumulada a un cambio sostenido.**
  - **Tipos (E7).** La contribución usa la respuesta del precio a h = 12, dividida por la respuesta acumulada del propio tipo a h = 12 en la misma proyección local con instrumento. Así se normaliza por un cambio sostenido de 100 pb.
    - En cada fecha, solo cuenta la variación del tipo de los 12 trimestres anteriores.
    - Lo anterior se rotula «fuera del horizonte estimado», sin cifra.
  - **Paneles en primeras diferencias (E3, E5, E9, E12).** El coeficiente es ya una respuesta de nivel permanente y se multiplica por la variación acumulada del factor en el periodo.
- **Rótulo obligatorio.** Toda contribución de un diseño de panel con efectos de periodo (E1, E2, E3, E5, E6-R2, E8, E9, E12) se rotula **«relativa entre provincias (o unidades), sin el componente común»**.
  - El agregado se contrasta con F1 y con la descomposición SVAR de V8, sin sumarlos.
  - Solo E7 (series nacionales) incluye el componente común.
- **Validez externa en cada fila.** Una columna dice «dentro del soporte» si la variación observada del factor en ese territorio y periodo está entre los percentiles 5 y 95 de la variación de la muestra de estimación. Si no, «fuera del soporte» y la fila no lleva cifra. Se aplica en particular a la fila nacional, que incluye las 11 provincias selladas.
- **Sin doble cómputo E3/E9 (AD-T5).** E3 (inmigración) y E9 (no residentes) usan cuotas del padrón por nacionalidad y no se suman.
  - La principal usa E3. E9 va como fila alternativa en la sensibilidad.
  - Se publica la correlación entre los dos instrumentos en la muestra común.
  - Siguen sin sumarse, como en el plan, E3 con la población de F1 y E7 con el crédito.

### 1.11 evaluate_v18: evaluación sellada diferida, pre-registrada (R-4; K2)
- **Qué se evalúa.** Una hipótesis confirmatoria por identificador. Solo se evalúan las que en entrenamiento queden IDENTIFICADO, con o sin nulo acotado:
  - E1-A1;
  - E2-A1;
  - E3-A1, E3-A2 y E3-A3;
  - E5-R1;
  - E6-R2.

  Son 7 hipótesis. Las demás no se evalúan ni consumen nada.
- **Con qué datos.** Observaciones cuyo resultado corresponde a un periodo estrictamente posterior al tope de entrenamiento de V18 (sellado_v18.json) y a las claves de V15 y V16 de esa variable. Además:
  - solo ediciones publicadas después de la fecha de la etiqueta;
  - las mismas unidades no selladas del entrenamiento: nunca unidades de v6, V15 o V16 ni datos de sus muestras selladas;
  - los regresores pueden pertenecer a periodos ya vistos.

  Datos mínimos por hipótesis:

| Hipótesis | Datos posteriores mínimos |
|---|---|
| E1-A1 | SERPAVI por sección 2025 y 2026 (ediciones posteriores a la etiqueta; si la de 2025 ya está publicada y en la muestra sellada de V16, se empieza en 2026 y se exige 2027) |
| E2-A1 | Incasòl trimestral de 2026T2 a 2027T1 como mínimo (cuatro trimestres) |
| E3-A1 | Valor tasado provincial anual 2027 y 2028 (primeros años con sus cuatro trimestres posteriores a 2026T2) y padrón por nacionalidad a 1-1-2026, 2027 y 2028 |
| E3-A2, E3-A3 | SERPAVI provincial o municipal 2027 y 2028, con el padrón de esos años |
| E5-R1 | Iniciadas y valor tasado anuales 2027 y 2028, con la afiliación por sector de esos años |
| E6-R2 | IPVA de dos años de edición posterior a la etiqueta, con las terminadas trimestrales y la lluvia de AEMET correspondientes |

  - En E3, las primeras diferencias del padrón empiezan en 2027 (2027 menos 2026), porque las de 2023-2025 forman parte de la muestra sellada temporal de V16 y no se usan, ni siquiera después de que V16 las evalúe.
  - En E1-A1, el índice de Google Trends no interviene. En E1-R2, que no se evalúa, no se reutilizaría sin empalme: Google reescala cada descarga.
- **Cuándo.** La evaluación de cada hipótesis se abre en la primera fecha en que se cumplan tres condiciones:
  - (i) existen sus datos mínimos;
  - (ii) ya están hechas las evaluaciones selladas de V15 y V16 que comparten variables con ella (como `hipotesis_v15_pendientes`): H3 para E1-A1, H1 y H2 para E2-A1, H4 y la pregunta Q3 de V16 para E3, Q4 de V16 para E5 y las preguntas de V16 sobre alquiler y oferta para E6;
  - (iii) el MDE con el diseño posterior (solo la variación del tratamiento en los periodos nuevos y el σ de entrenamiento) es ≤ |b_entrenamiento|. Si (iii) no se cumple, se aplaza sin abrir nada.

  Si el 2031-12-31 no se ha abierto, la hipótesis se cierra «sin evaluación» y queda en C4. evaluate_v18 no se ejecuta dentro de V18 (docs/v18/plan.md, línea 17): requiere orden expresa del autor en una versión posterior.
- **Cómo: una sola evaluación por hipótesis, vía src/holdout.py.** Funciones nuevas, que el autor tiene que autorizar:
  - **`sellar_v18`:** los datos posteriores se descargan directamente a data/sealed/v18_<conjunto>.parquet sin devolverse, como sellar_v16, y cada sellado queda registrado.
  - **`evaluate_v18`:** puerta = la etiqueta plan-replicacion-v18 con su commit en el remoto; registro de la apertura antes de leer; una apertura por clave «v18:<id>»; se niega si alguna evaluación de V15 o V16 que comparte variables sigue pendiente.
  - **Código congelado.** Se ejecuta el código del commit que produjo el resultado.json de entrenamiento de ese identificador, con su hash registrado. Solo cambia la muestra.
- **Criterio de superación, fijado ahora.** b_ev es la estimación con los datos posteriores; b_tr, la de entrenamiento. La evaluación se supera si se cumplen las tres condiciones:
  - (1) signo(b_ev) = signo(b_tr);
  - (2) p de b_ev < 0,05 tras Holm sobre la familia de evaluación, con m = 7 fijo, se abran o no todas;
  - (3) b_tr está dentro del IC95 de b_ev, o la razón b_ev/b_tr está en [1/3; 3].

  Si la clase de entrenamiento es un nulo acotado, se supera si el TOST con su δ se cumple en los datos posteriores.
- **Consecuencia.**
  - **Supera, con clase IDENTIFICADO en entrenamiento:** se propone al autor la capa C3 para esa cifra. Es una parada de tipo G1: si altera una cifra publicada va a ERRATA.md.
  - **No supera:** queda en C4, se documenta y no hay segunda evaluación.
- **Episodios históricos: no pueden llegar a C3.** No hay periodo posterior del mismo episodio que sellar, y capas.md exige evaluación en muestra sellada. Quedan en C4 sea cual sea su clasificación V18, y se dice:
  - Ley 11/2020: E2-R1, E2-R1c, E2-A3 y E2-A4;
  - auge de 1998-2010: E3-R1, R1q, R2, R2b, R2q y E3-A5;
  - Barcelona 2011-2019: E1-R3 y E1-R4;
  - cohortes de obra de 2015-2018: E6-R1;
  - cambios del ITP 2007-2024: E8.

### 1.12 Monte Carlo: bandas (R-19; sustituye a las bandas de 0.4)
- **Apta.** Tamaño al 5 % en [0,04; 0,06] y cobertura al 95 % en [0,93; 0,97], con R ≥ 2.000.
- **Con valor crítico corregido.** Tamaño en [0,02; 0,04) o en (0,06; 0,15]. Se publica el p con el valor crítico corregido por tamaño del Monte Carlo, y es el que usa I7.
- **No fiable.** Tamaño superior a 0,15 o inferior a 0,02. Se publica con esa etiqueta, y la clasificación no puede apoyarse en ella.
- **E8.** Tope SUGESTIVO salvo que la inferencia usada tenga tamaño en [0,04; 0,06] (R-18).

### 1.13 Pocos choques efectivos (R-11; AD-E3 inferencia)
- **Qué se publica.** En todo shift-share o Bartik (E3, E5, E9, E12) se publica 1/HHI de los pesos de los choques (BHJ), calculado antes de estimar con las cuotas y los choques, sin el resultado.
- **Inferencia según 1/HHI.**
  - Si 1/HHI < 20, la inferencia principal es el cluster por provincia con wild bootstrap de Webb (9.999 réplicas), más el intervalo AR. BHJ pasa a alternativa.
  - En E9, 1/HHI < 10 implica NO ESTIMABLE.
  - En E5 el Bartik tiene 7 sectores (sección 2, R-17), así que 1/HHI < 20 por construcción y la regla se aplica de entrada.

### 1.14 G3 simétrica (R-22; sustituye a G3 y a sus ejemplos de la sección 5)
- **Cuándo se activa.** Con cualquier estimación IDENTIFICADO, nulo acotado incluido, cuyo IC95 sea incompatible con una conclusión publicada vigente, en cualquier signo.
- **Conclusiones «no concluyente».** Una conclusión publicada de ese tipo (por ejemplo, «turísticos: no concluyente») queda contradicha tanto por un efecto positivo IDENTIFICADO como por uno negativo, y también por un nulo acotado.
- **Procedimiento:** el de la sección 5 del plan, sin cambios.

---

## 2. Respuesta a los hallazgos del revisor del pre-registro

### Alta

**R-1 / AD-E2-R1 · aceptado.**
- **Ventana real de JMS, leída en el PDF** (data/bib/pdf/jofremonseny2023.pdf, versión de trabajo de febrero de 2023; la ficha cita la publicada en RSUE 101):
  - los microdatos de Incasòl «are available between 2016 and 2022» y se agregan por municipio y trimestre (p. 7);
  - las figuras van de 2016q1 a 2022q1 (fig. 2, p. 11);
  - la tabla 2 tiene 3.698 observaciones y 148 municipios (p. 12), es decir, 25 trimestres (148 × 25 = 3.700, menos 2);
  - el primer trimestre tratado es 2020T4 y la anticipación es 2020T3 (pp. 9-10);
  - la normalización es 2019T4 (p. 10). La ecuación (2) escribe «t ≠ 2019q3»: discrepancia del propio texto, se declara y se sigue el texto, 2019T4;
  - la extensión con el fin de la norma va hasta 2022T2 (sección 6.3, pp. 21-22).

  La ventana de JMS es, por tanto, **2016T1-2022T1, con microdatos**. Nuestro Incasòl público es trimestral solo desde 2019T1 (docs/v3/decisiones.md; docstring de `incasol` en src/v9/paneles.py).
- **Cambio a E2-R1:**
  - Principal **trimestral 2019T1-2022T1**, marcada `repite_visto` (es la ventana de V9-D1b): posterior 2020T4-2022T1, anticipación 2020T3, base 2019T4.
  - Covariables: paro registrado trimestral (media trimestral del paro municipal del SEPE si es mensual; si es anual, el anual, declarado) y expedientes de regulación temporal de empleo por municipio si están en el repositorio. Si no están, se omiten y se dice.
  - Variante E2-R1-v1: sin 2020T1-2020T3 en el periodo previo.
  - Robustez **anual 2014-2021** (E2-R1-v8) con Honest DiD.
  - Placebo de fecha en la serie anual: adopción falsa en 2017. El placebo trimestral de 2018T4 del plan no es aplicable y se suprime.
  - Variante E2-R1-v7 con anticipación desde 2019T2: RDL 7/2019 (BOE de 5-3-2019) y Decreto-ley catalán 9/2019. La fecha de este último se verifica en el DOGC antes de estimar. Si no se verifica, el término se mantiene en 2019T2 por el RDL 7/2019, y se dice.
- **Por qué.** Una ventana que no existe en nuestros datos no puede ser principal. La anual es la única con preperiodo largo y queda como robustez.

**R-2 · aceptado.**
- **Cambio:**
  - E2-R2, E2-R2s y E2-R2-X1 pasan a **NO ESTIMABLES (X)** y salen de la familia de Holm de E2. El campo de tramo de Incasòl clasifica al municipio y no reparte sus contratos (src/v9/paneles.py, docstring de `incasol`; docs/v9/revision_f2.md).
  - Sus 7 variantes se suprimen.
  - Inventario corregido y regenerado (sección 0).
  - Para hacerlas estimables: microdatos de contratos del registro de fianzas con renta, renta anterior y superficie (tareas_autor, punto 4).
- **Por qué.** El estimando de Monràs y García-Montalvo exige la distribución de los contratos por tramo, que no existe en los datos públicos.

**R-3 · aceptado.**
- **Cambio:**
  - Regla de frecuencia de la sección 1.4.
  - E3-A1, A2, A3 y A4 terminan en **2022**: las claves de padron_pob_nacionalidad|provincia|A, padron_municipal_nacionalidad|municipio|A y pob_extranjera|municipio|A son 2022 (docs/v16/sellado_v16.json).
  - La serie de la ECP por nacionalidad hereda 2022 (regla 1.4 f).
  - Las variables sin clave en conjuntos de V15 o V16 están selladas enteras (1.4 d). Las que no estuvieron nunca en un conjunto siguen la regla 1.4 e.
  - Cortes por especificación: Anexo C.
- **Por qué.** El sellado temporal de V16 protege su evaluación de Q3 y H4, y una media anual o un sustituto no pueden saltárselo.

**R-4 / AD-T3 · aceptado (decisión K2 del autor).**
- **Cambio:** sección 1.1 (C4, `nivel_evidencia = "EXPLORATORIO"`, campo clasificacion_v18, clase NO CONCLUYENTE, fórmula condicional solo en las secciones técnicas, check_v18 sin lenguaje causal en ninguna cifra V18) y sección 1.11 (evaluate_v18 pre-registrado; los episodios históricos no llegan a C3).
- **Por qué.** CLAUDE.md y metodologia/capas.md reservan la causalidad a C3/C3s, y C3 exige evaluación en muestra sellada. El autor eligió la opción restrictiva.

**R-5 · aceptado.**
- **Cambio:** sección 1.8 y Anexo A: 245 variantes enumeradas, holgura máxima de 200 que no apoya IDENTIFICADO ni entra en B5, y tope de V18 de 531.
- **Por qué.** Un multiverso sin enumerar deja elegir variantes a la vista.

**R-6 · aceptado.**
- **Cambio:** sección 1.9. Entran todas las estimaciones con diseño válido, sea cual sea su p, con la clase NO CONCLUYENTE (sin potencia), y el nulo se acota por TOST con el δ de cada especificación (Anexo B).
- **Por qué.** Seleccionar por significación sesga la magnitud preferida hacia arriba (maldición del ganador).

**R-7 · aceptado.**
- **Cambio:** sección 1.9 (una propia por factor, con respaldo solo por NO ESTIMABLE, y episodios compartidos con ρ = 0,8 y sensibilidades 0,5 y 1).
- **Por qué.** Contar dos veces el mismo episodio con la misma fuente infla la precisión de la magnitud preferida.

**R-8 / AD (elegidas conociendo un resultado previo) · aceptado.**
- **Cambio:** sección 1.6. La columna repite_visto de la tabla consolidada recoge, como mínimo:
  - E1-R1 y R3 (V9-D2), E1-A1 (H3) y E1-A2 (Q2b);
  - E2-R1 y R1c (V9-D1b), E2-A1 (H1 y H2), E2-A2 (V9-D1c) y E2-A3 (Q1c);
  - E3-R1, R1q, R2, R2b, R2q y A5 (V9-D4), E3-A1 (Q3-c1), E3-A2 (H4 y Q3) y E3-A3 (H4);
  - E5-R1 (elección del instrumento tras Q4);
  - E7-R1 y R2 (Q5 y V8 H8-5 a H8-7) y E7-A2 (V9-D5);
  - E8-R1 (Q6-p) y E8-R2 (Q6-v);
  - F1-R1 y A2 (V7.2 y V8-M4), F1-R2 (V7.2), F1-A1 (V15 E1-P2 y Q9-c) y F2-A2 (V15 E1).

  Cada una tiene su coprincipal P en la misma familia, y rige el tope SUGESTIVO por corrección de un fallo conocido.
- **Por qué.** Sin la especificación anterior en la familia, la mejora de V18 no se distingue de una búsqueda.

**R-9 · aceptado.**
- **Cambio:** I2 de la sección 1.2. E7-R1 y E7-R2 dejan de poder llegar a IDENTIFICADO por la vía «AR informativo»: con F < 10, el tope es SUGESTIVO.
- **Por qué.** Un AR acotado mide que la inferencia es informativa, no que el instrumento sea fuerte. La significación se juzga en I7.

### Media

**R-10 · aceptado.**
- **Cambio:**
  - Sección 1.3: MDE por Monte Carlo con la variación real y el σ de V15/V16 declarado como ya visto, más los mínimos de datos y las definiciones.
  - E2-A2 deja de ser «solo descriptiva» y queda NO ESTIMABLE si no alcanza su mínimo. Se puede mostrar una figura descriptiva fuera de la clasificación.
  - En E1-R1 se suprime el corte de 2024T1: el valor anual es el corte más cercano al 31 de diciembre.
- **Por qué.** Umbrales arbitrarios y distintos por estudio son grados de libertad. Una sola regla de potencia, fijada sin resultados, los elimina.

**R-11 · aceptado.**
- **Cambio:** sección 1.13 (1/HHI publicado; con menos de 20, cluster por provincia con Webb y AR como principal), aplicada a E3, E5, E9 y E12.
- **Por qué.** BHJ necesita muchos choques efectivos; en E3, Rumanía pesa 0,475 en Q3-c.

**R-12 / AD-E3-R1 · aceptado.** Cambios en E3 y por qué:
- **Ventanas.** Principal **2002-2008** con cuotas del Censo de 2001; 1998-2008 como variante E3-R1-v1. E3-R2 pasa a **2002-2010** (2000-2010, la del original, en la variante E3-R2-v1), y E3-R2b a 2002-2008 (2001-2008 en su variante). Por qué: con la base en 2001, la ventana tiene que empezar después.
- **Censo de 1991.** No está en el repositorio: ningún `_manifest.csv` de data/raw lo registra (solo los Censos de 2011 y 2021). Se intentará descargar como variante (E3-R1-v3 y E3-R2-v7), nunca como principal.
- **Choque.** El de la principal es el flujo nacional por origen **sin quitar la propia provincia, como en el original** (IZA, p. 9: flujos nacionales del Registro). La versión sin la propia provincia, que solo es posible desde 2004 con la variación del stock del padrón por nacionalidad, va como variante (E3-R1-v10, 2004-2008).
- **Unidad de R1.** R1 se compara con la cifra del IZA en su propia unidad (44,72 €/m² por punto; Anexo B) y **no entra en B5**, así que no hay precio de conversión que fijar. B5 usa E3-R2, que es una elasticidad.
- **Referencias.** La de R2 queda fijada en **0,959 (0,984)**, solo redes, 2001-2010, Chicago Fed 2011 (NO VERIFICADA), y la de R2b en 0,927 (0,596). En unidades distintas no se combinan.

**R-13 / AD-T1 · aceptado en parte.**
- **Se acepta:**
  - la referencia única por especificación (Anexo B);
  - la razón en [1/3; 3];
  - la vía del solapamiento solo si el error de la referencia es menor que la mitad de su coeficiente, y además con el límite de anchura de AD-T1.
- **No se acepta:** que I6 siga decidiendo la clasificación.
- **Cambio:** I6 pasa a etiqueta (sección 1.2).
- **Por qué.** El revisor propone endurecerlo y el abogado del diablo, sacarlo de las decisiones. Se adoptan ambas cosas: la definición más estricta, para la etiqueta, y su salida de las decisiones, porque usar I6 como filtro sesga hacia la literatura.

**R-14 / AD-E1-R2 · aceptado.** Cambios en E1-R2 y E1-A1:
- **Endógena.** Variante E1-R2-v5 con el % de viviendas turísticas de INE-VUT como endógena (desde 2020, sin 2020-2021, es decir, 2022-2024).
- **Sin 2020-2021.** Variantes E1-R2-v2 y E1-A1-v1.
- **Primera etapa por subperiodo** (2018-2019, 2020-2021 y 2022-2024), publicada. Si el signo cambia entre subperiodos o más de la mitad del F efectivo procede de 2020-2021, tope SUGESTIVO.
- **Pretendencias.** La pretendencia limpia de E1-R2 exigiría SERPAVI de 2007-2011, que no existe (empieza en 2011). Barcelona ya tenía expansión de Airbnb desde 2013 (García-López et al., 2020, PDF p. 9). Por eso **E1-R2 tiene tope SUGESTIVO**.
- **E1-A1 sin Barcelona.** La principal de E1-A1 pasa a **València, Sevilla, Málaga y Alicante**, con la pretendencia del instrumento sobre Δln SERPAVI 2011-2013, antes de su expansión. Barcelona va en la variante E1-A1-v2, porque su preperiodo está contaminado.
- **Consulta de Trends fijada:** término «airbnb» (término, no tema), región ES-CT, enero de 2010 a diciembre de 2024, mensual, media anual y una sola descarga con su fecha registrada.
- **Control** distancia al centro × año en la principal de R2 y de A1. El centro es la sección que contiene la sede del ayuntamiento (OpenStreetMap, amenity=townhall).
- **Por qué.** Sin preperiodo anterior a la expansión de las plataformas, la exclusión no se contrasta.

**R-15 · aceptado.** Cambios por especificación:
- **Placebo de resultado (65 años o más por sección):** solo existe desde 2021. En E1-R3 y E1-R4 (2011-2019) se declara **no aplicable**. En E1-R1 y E1-A1 se mantiene con los años 2021-2024.
- **E1-R4, fecha fijada:** tratamiento desde **2014**, el primer año completo tras la expansión de 2013 (García-López et al., 2020, sección 4.4, PDF p. 8, y sección 5.1, PDF p. 9). Posterior 2014-2019, base 2013, preperiodo 2011-2012, placebo de fecha con adopción falsa en 2012 en la ventana 2011-2013.
- **E1-R3:** se publican la potencia del preperiodo (I3) y la tendencia por distancia al centro de 2011-2013, como diagnóstico. Si esa tendencia es significativa al 10 %, la variante con distancia × año (E1-R3-v3) pasa a coprincipal en la familia de E1.
- **E1-A2:** estimador de de Chaisemartin-D'Haultfœuille con dosis continua escalonada como principal, y Callaway, Goodman-Bacon y Sant'Anna (dosis continua) en la variante E1-A2-v1. Los dos requieren Monte Carlo (sección 1.13 del plan).
- **Por qué.** Un placebo sin datos o sin fecha no es una prueba.

**R-16 / AD-E2-R1 · aceptado en parte.**
- **Cambio:**
  - **Se suprime** la variante de controles por tercil de renta media y de su crecimiento en 2016-2019, que emparejaba por el resultado.
  - **Principal:** el grupo de control de JMS (p. 8): municipios catalanes no regulados con un crecimiento anual de la renta de 2014-2019 superior al 4,15 %, al menos un contrato en cada trimestre, sin los municipios que entraron o salieron del régimen y sin Barcelona ciudad. Si la lista del repositorio no identifica las entradas y salidas, se reconstruyen con el DOGC antes de estimar, y si no es posible se dice.
  - **Variantes:** controles por covariables (E2-R1-v3: vecino más cercano por población de 2019, distancia a Barcelona y paro de 2019); controles a más de 10 km, los del plan, que se eligieron tras el fallo de V9-D1b (E2-R1-v4); y V9-D1b exacta como coprincipal (E2-P-D1b).
  - **Mínimo:** 30 municipios de control (sección 1.3).
- **No se acepta:** quitar también el criterio de JMS.
- **Por qué.** Es el criterio legal de mercado tensionado y el del original. La réplica lo conserva, y la versión por covariables aísla el riesgo que señala el revisor.

**R-17 / AD-E5-R1 · aceptado.** Cambios en E5-R1:
- **Bartik de la principal** con la agregación A*10 de la CNAE, **sin construcción (F), sin finanzas (K) y sin inmobiliarias (L)**: 7 sectores.
- **Correspondencia CNAE-93 a CNAE-2009, fijada en A*10:**

| Sector A*10 | CNAE-93 |
|---|---|
| A | A, B |
| B-E | C, D, E |
| F | F (división 45) |
| G-I | G, H, I (salvo 64) |
| J | 64 y 72, más las divisiones 221-223 y 921-922, que se asignan a J |
| K | J (divisiones 65-67) |
| L | 70 |
| M-N | 71 y 73-74 |
| O-Q | L, M, N |
| R-U | O, P, Q (salvo 921-922) |

  Si la afiliación de 2001 no tiene el detalle de división, las celdas ambiguas (64, 72, 221-223, 921-922) se asignan al sector de su sección de la CNAE-93, y se declara.
- **Variante con los diez sectores** (E5-R1-v4), la del plan.
- **Auge y caída por separado:** 2002-2007, 2008-2013 y 2014-2024 (v1 a v3). Si el signo difiere entre el auge y la caída, la principal agrupada tiene tope SUGESTIVO.
- **Exposición a cajas de 2007 × año** (v10), si el dato está en el repositorio. Si no, se omite y se dice.
- **Ventana:** termina en 2024 por la regla 1.4 b.
- **Por qué.** Con la construcción dentro, el instrumento contiene la propia oferta.

**R-18 / AD-E8 · aceptado.** Cambios en E8:
- **Recuento corregido.** Las 8 CCAA suman **36 provincias**, no 30: Andalucía 8, Cantabria 1, Castilla y León 9, Castilla-La Mancha 5, Cataluña 4, Comunitat Valenciana 3, Extremadura 2 y Galicia 4. Con las 3 del País Vasco son las 39 no selladas.
- **Inferencia.** Aleatorización del calendario: 9.999 permutaciones de las fechas y dosis de los cambios entre CCAA y años, manteniendo la distribución de las dosis. Wild cluster bootstrap restringido de Webb con 8 clusters.
- **Tope:** SUGESTIVO salvo tamaño de Monte Carlo en [0,04; 0,06].
- **Reglas de codificación de fechas, fijadas ahora:**
  - la fecha es la de entrada en vigor publicada en el BOE o en el diario oficial autonómico, no la de aprobación ni la de publicación;
  - en datos mensuales cuenta el mes de entrada en vigor si es día 15 o anterior, y si no el siguiente; en trimestrales, el trimestre de ese mes;
  - la dosis es la variación del tipo general en puntos;
  - dos cambios de una CCAA a menos de 12 meses se tratan como un solo evento, con la dosis acumulada en la primera fecha.
- **Control de recaudación previa.** Crecimiento de la recaudación del ITP en t−1 y t−2 y déficit autonómico, de Hacienda (`posterior_prereg`). Si no se puede descargar, la principal va sin ese control y con tope SUGESTIVO.
- **Robustez:** signo sin 2012-2013 como condición (si cambia, tope SUGESTIVO) y fechas desplazadas ±3 meses (variantes v2 y v3).
- **Por qué.** Los cambios del ITP pueden responder a la recaudación, y con 8 clusters la inferencia convencional no es fiable.

**R-19 · aceptado.**
- **Cambio:** sección 1.12.
- **Por qué.** Con un tamaño del 8 % el p nominal sobrestima la significación.

**R-20 · aceptado.**
- **Cambio:** sección 1.5 (lista de distritos sellados de Barcelona y de las demás ciudades, efecto en E1-R1 y E1-R4, convención de V15/V16 declarada y variante sin esos municipios).
- **Por qué.** El agregado municipal de una gran ciudad contiene distritos sellados.

**R-21 / AD-T2 · aceptado.**
- **Cambio:** sección 1.10 (respuesta acumulada a un cambio sostenido, rótulo «relativa entre provincias, sin el componente común» y validez externa por fila).
- **Por qué.** Multiplicar efectos relativos de horizontes distintos por variaciones nacionales mezcla unidades y soporte.

**R-22 · aceptado.**
- **Cambio:** sección 1.14.
- **Por qué.** Una parada que solo mira un signo favorece una dirección.

**R-23 / AD-E2-A1A2 · aceptado.**
- **Cambio:**
  - E2-A1 **no se difunde** antes de la evaluación sellada de H1 y H2 de V15. En el Documento de Trabajo va rotulada «provisional: H1/H2 pendientes de su evaluación sellada».
  - E2-A2 declara el fallo previo de V9-D1c (pretendencia con p = 0,000) y el sellado de 107 municipios de Bizkaia y 79 de Gipuzkoa (sección 1.5), que probablemente la dejan bajo el mínimo de la sección 1.3. Tope SUGESTIVO.
- **Por qué.** E2-A1 repite en entrenamiento una hipótesis cuya evaluación sellada está pendiente.

### Baja

**R-24 · aceptado.**
- **Cambio:** sección 1.7.
- **Por qué.** Contar en m las especificaciones que no pueden llegar a SUGESTIVO o IDENTIFICADO, o las NO ESTIMABLES, resta potencia sin proteger nada.

**R-25 · aceptado.**
- **Cambio:** sección 1.9 (tres priors; se combina solo si la decisión coincide).
- **Por qué.** La magnitud preferida no debe depender de la escala de la prior.

**R-26 · aceptado.**
- **Cambio:** Anexo B con el estado de cada ficha, rotulado en toda tabla. Las referencias NO VERIFICADAS o DISCREPANTES se verifican en la fase 5 si la red lo permite. Si no, se dejan rotuladas.
- **Por qué.** Es la regla de referencias de CLAUDE.md.

**R-27 · aceptado.** Cambios por especificación:
- **E7-R3:** la variable de crédito es el **saldo** de préstamos para vivienda, como en San Juan (BdE, `posterior_prereg`). Si no se puede descargar, se usa base:credito_nuevo y se rotula «flujo, no saldo».
- **Sorpresa monetaria:** la clave bce_jk_mp_pm_m|zona_euro|M es 2025-10, así que la suma trimestral llega a **2025T3** (el último trimestre completo), no a 2025T4. Con h = 8 y el resultado hasta 2026T2, el último origen utilizable es 2024T2.
- **E1-R1:** principal **sin controles variables en el tiempo**, porque la renta ADRH (2019-2023) y la población (2021-2025) no cubren 2018-2024. La renta ADRH entra solo en la variante E1-R1-v10, en 2019-2023.
- **E6-R1:** k = 0 es el primer año natural completo tras la terminación (T+1), porque SERPAVI mide los contratos vigentes declarados en el año.
- **Por qué.** Eran ambigüedades que dejaban decisiones para después de ver los datos.

**R-28 · aceptado.**
- **Cambio:** sección 1.3 (MDE previo por especificación principal, publicado).
- **Por qué.** Lo mismo que en R-10.

---

## 3. Respuesta al abogado del diablo

### Transversales

**AD-T1 · aceptado.** Cambio: I6 como etiqueta, B5 con y sin las estimaciones no coherentes y límite de anchura en la vía del solapamiento (secciones 1.2 y 1.9). Por qué: I6 como filtro sesga la magnitud preferida hacia la literatura.

**AD-T2 · aceptado.** Cambio: sección 1.10 (rótulo, contraste con F1 y con el SVAR de V8 sin sumar y sin extrapolar fuera del soporte). Por qué: las magnitudes salen de 39 provincias sin las de más inmigración, turismo y compra extranjera.

**AD-T3 · aceptado** (K2). Cambio y motivo: como en R-4.

**AD-T4 · aceptado.** Cambio: I3 con la pendiente previa detectable al 80 % y el sesgo implicado menor que la mitad de la referencia; si no, tope SUGESTIVO (sección 1.2). Por qué: un p > 0,10 con poca potencia no es evidencia de tendencias paralelas.

**AD-T5 · aceptado.** Cambio:
- E3 y E9 en la regla de no doble cómputo (sección 1.10), con la correlación entre instrumentos publicada.
- Variante de E3 **sin UE-15, Noruega, Suiza e Islandia**, es decir, sin los grupos 1 y 2 de la lista fija (E3-R1-v5, E3-R2-v3, E3-A1-v1, E3-A2-v3 y E3-A3-v5).

Por qué: los dos factores comparten cuotas, y el Reino Unido pesa 0,157 en Q3-c.

### Por estudio

**AD-E1-A1 · aceptado.** Cambio:
- Distancia al centro × año en la principal (v11 la quita).
- Placebos del instrumento con proximidad a hospitales (amenity=hospital) y a universidades (amenity=university) × noches. Si la forma reducida del placebo es significativa al 5 %, con el mismo signo y al menos la mitad del efecto, ASOCIACIÓN; si su p está entre 0,05 y 0,10, tope SUGESTIVO.
- Sin 2021 (v1).
- **H3 coprincipal** (E1-P-H3) en la familia E1.
- Tope por corrección de un fallo conocido (sección 1.6).

Por qué: el diseño se eligió tras H3 (p = 0,931) y Q2, y la proximidad × noches puede recoger la recuperación del centro tras la COVID.

**AD-E1-R2 · aceptado.** Cambio: como en R-14 (primera etapa por subperiodo, tope SUGESTIVO si se concentra en 2020-2021, distancia al centro × año y tope SUGESTIVO por la pretendencia contaminada). Por qué: con la moratoria, el «cuándo» mueve los anuncios, no las licencias.

**AD-E1-R3 · aceptado.** Cambio y motivo: como en R-15 (tendencia por distancia al centro de 2011-2013 y potencia del preperiodo publicadas).

**AD-E1 (medida) · aceptado en parte.**
- **Cambio:**
  - El número de contratos de SERPAVI por sección no tiene clave a escala de sección en los manifiestos (serpavi_n_contratos_recuento solo tiene clave municipal y provincial). Por eso la prueba de composición pedida es **NO ESTIMABLE** a escala de sección, y se declara como limitación.
  - En su lugar, diagnóstico de composición por tamaño: la mediana en €/m² frente a la mediana en €/mes de la sección (serpavi_alquiler_mes_mediana, con clave por sección hasta 2024), con el mismo signo exigido.
- **Por qué.** No se usa un dato sin clave en su nivel (regla 1.4 d).

**AD-E2-R1 · aceptado.**
- **Cambio:**
  - **Reversión tras la STC 37/2022**, como prueba: el coeficiente de los municipios regulados en 2022T2-2023T4. Se esperaba la vuelta a los niveles previos (JMS, p. 21). Si la diferencia persiste (mismo signo, significativa al 5 % y al menos la mitad del efecto de la vigencia), tope SUGESTIVO.
  - **Densidad HUT de 2019 × posterior** (variante v6, con idescat_hut_n municipal).
  - Controles por covariables (v3) y **V9-D1b como coprincipal** (E2-P-D1b).
  - Errores por comarca con Webb (42 comarcas) y Conley como inferencia alternativa.
- **Por qué.** La COVID coincide con el periodo posterior, y el grupo de control se definió tras el fallo de V9-D1b.

**AD-E2 (medida) · aceptado en parte.**
- **Cambio:**
  - Contratos registrados por hogar inquilino (hogares en alquiler del Censo 2021, fijos) como resultado en E2-R1c-v1.
  - Si caen al menos un 5 % con significación al 5 %, no se puede descartar el desvío a la temporada o a no depositar la fianza, y E2-R1 y E2-A1 tienen tope SUGESTIVO.
- **No se acepta:** que A5 cierre siempre el paso a IDENTIFICADO.
- **Por qué.** El desvío es contrastable en parte con los contratos. Cerrar el paso sin contraste haría la clasificación independiente de los datos.

**AD-E2-A1/A2 · aceptado.** Cambio y motivo: como en R-23.

**AD-E3-R1 · aceptado.** Cambio:
- Principal 2002-2008 (R-12). Censo de 1991 solo como variante, porque no está en el repositorio.
- **Lista fija de 16 grupos de origen** (el original usa 16 regiones del Censo de 1991, IZA, p. 9, nota 16, sin enumerarlas):
  1. UE-15 sin España;
  2. Noruega, Suiza, Islandia y Liechtenstein;
  3. Rumanía;
  4. Bulgaria;
  5. resto de Europa;
  6. Marruecos;
  7. Argelia y resto del norte de África;
  8. África subsahariana;
  9. Ecuador;
  10. Colombia;
  11. Bolivia;
  12. Perú;
  13. Argentina;
  14. resto de América Central y del Sur y Caribe;
  15. China;
  16. resto del mundo (resto de Asia, América del Norte, Oceanía y apátridas).
- Si un grupo no puede construirse igual en el Censo de 2001, en los flujos y en el padrón, se une con este orden fijo: 4 → 5, 11 → 14 y 7 → 8.

Por qué: la elección de la lista después de ver las fuentes sería un grado de libertad.

**AD-E3 (exclusión) · aceptado en parte.**
- **Cambio:**
  - En la principal de E3-R1, R2 y A1-A5:
    - cuota del empleo en la construcción de 2001 × año (afiliación de 2001, `posterior_prereg`);
    - costa × año, con 17 provincias costeras no selladas fijadas ahora: 03, 04, 08, 11, 12, 15, 17, 18, 20, 21, 27, 29, 36, 39, 43, 46 y 48.
  - Variante sin los grupos 1 y 2.
  - Variante con las ficticias de 2005 (regularización) y de 2006 (bajas por caducidad), cada una interactuada con la cuota no comunitaria de 2001 (E3-R1-v7).
- **No se acepta:** el saldo migratorio interior de nativos como resultado. Las migraciones interiores de la base (ine_emcr) no distinguen la nacionalidad. Queda NO ESTIMABLE y se declara.
- **Por qué.** Los asentamientos previos pueden reflejar una demanda local persistente.

**AD-E3 (inferencia) · aceptado.** Cambio y motivo: como en R-11 (sección 1.13).

**AD-E5-R1 · aceptado.** Cambio y motivo: como en R-17.

**AD-E6-R1 · aceptado.** Cambio:
- **Solo secciones contiguas.** El resultado se mide en las secciones contiguas a la del edificio, sin la propia, porque su mediana incluye la vivienda nueva. La versión del plan, con la propia, va en la variante v4.
- **Fecha de inicio de obra.** El Catastro da el año de construcción. La fecha de inicio se aproxima por la terminación menos 2 años en la variante v2.
- **Controles sin obra en el periodo posterior:** edificios terminados en T+6 o después, y en 2024 como máximo.
- Con el preperiodo de k = −4 a −1, desde 2011, las cohortes tratadas son **2015-2018**.

Por qué: con la propia sección se mide en parte la composición, y con controles en obra el contraste se contamina.

**AD-E6-R2 · aceptado.** Cambio:
- Placebo de la lluvia de julio a septiembre de t−1 sobre las pernoctaciones de t. Si p < 0,10, la exclusión es dudosa y tope SUGESTIVO.
- Variante sin 2019 ni 2024 en la provincia de València (DANA; v1).
- IPC de alquiler trimestral (v2).

Por qué: la lluvia de verano puede afectar al turismo, y las DANA de otoño a la obra.

**AD-E7-R1/R2 · aceptado.** Cambio:
- Diferencial soberano a 10 años como control en las variantes v2 (BCE, `posterior_prereg`, si no está en la base).
- Sin 2010-2013 (v1).
- **Una sola referencia:** San Juan (2023), −2 % por +100 pb a 8 trimestres. La del BCE (−5 %) se muestra al lado, sin función en I6.
- En E7-A2, la cuota de compradores extranjeros × choque (v1).

Por qué: la prima soberana de 2010-2013 mueve el tipo hipotecario sin política monetaria, y dos referencias permiten elegir.

**AD-E8 · aceptado.** Cambio y motivo: como en R-18 (fechas, recaudación previa, signo sin 2012-2013, banda de ±3 meses y Monte Carlo con 8 clusters).

**AD-E9 · aceptado.** Cambio:
- **Recuento de choques efectivos (1/HHI) antes de estimar.** Con menos de 10, E9-R1 y R2 son NO ESTIMABLES; entre 10 y 20, cluster con Webb y AR (sección 1.13).
- **Signo esperado fijado ahora:** positivo (refugio de la inversión ante un choque en origen: Badarinza y Ramadorai; Sá). Un resultado significativo de signo contrario se clasifica como mucho SUGESTIVO y se documenta.
- Las pruebas son bilaterales.
- Control de pernoctaciones por país de origen × exposición (v6 en R1 y v3 en R2), si hay pernoctaciones por país. Si no, se omite y se dice.

Por qué: los choques casi comunes los absorben los efectos de año, y el signo es ambiguo.

**AD-F (F1, F2, F4) · aceptado.**
- **Cambio:**
  - Si el contraste de límites del ARDL (F1-R1, F1-A2) o el de Westerlund con bootstrap (F1-R2, F1-A1, F2-R1, F2-A1, F3-A2) no rechaza la ausencia de cointegración al 5 %, con valores críticos validados por Monte Carlo:
    - no se publican elasticidades de largo plazo de ese modelo;
    - no se publica la sobrevaloración (F1-A3);
    - no se hacen las comparaciones de F4 que las usan (F4-1, F4-3 y F4-5 con F1; F4-2 con F2; F4-4 con F3-A2).
  - Solo se publica la dinámica de corto plazo, como ASOCIACIÓN.
  - Coprincipales P en F: F1-P-V72, F1-P-M4 y F1-P-E1P2.
- **Por qué.** V7.2 y V8-M4 no hallaron cointegración. Un largo plazo sin cointegración es espurio.

**AD-E12-A1 · aceptado.** Cambio: la obra libre iniciada de 1991-1995 × año, como control de persistencia regional, en la principal (v1 lo quita). Por qué: la cuota de protegida de 1991-1995 puede reflejar la actividad constructora de la provincia.

---

## Anexo A. Multiverso enumerado

Cada fila enumera las variantes de una especificación principal. Dimensiones: [C] control, [V] ventana, [M] medida, [P] peso, [E] estimador, [U] unidad o muestra. Los identificadores son <id>-v<n>. Las inferencias alternativas (Webb, Conley, Driscoll-Kraay y otras) no cambian la estimación puntual y no cuentan como variante.

**E1 (40 variantes)**

| Id | Principal | Variantes |
|---|---|---|
| E1-R1 | Sección; HUT por 100 viviendas del Censo 2021; tendencias lineales por barrio; 2018-2024; sin pesos ni controles variables | v1 [E] sin tendencias; v2 [E] tendencias cuadráticas; v3 [V] sin 2020-2021; v4 [M] fianzas de Open Data BCN por barrio; v5 [M] HUT reconstruida por año de expediente; v6 [U] sin el 1 % superior de exposición; v7 [P] ponderada por viviendas; v8 [C] distancia al centro × año; v9 [U] barrio como unidad; v10 [C] ADRH en 2019-2023 (10) |
| E1-R2 | Proximidad a 3 atractivos OSM × Trends; distancia al centro × año; 2018-2024 | v1 [M] noches de Eurostat en lugar de Trends; v2 [V] sin 2020-2021; v3 [U] sin Sagrada Família, Park Güell y Casa Batlló; v4 [E] 5 atractivos; v5 [M] endógena INE-VUT, 2022-2024; v6 [C] sin distancia × año; v7 [M] fianzas como resultado; v8 [P] ponderada (8) |
| E1-R3 | Dosis continua 2018T2; 2011-2019; base 2013 | v1 [V] base 2012; v2 [E] dosis binaria del decil superior; v3 [C] distancia × año; v4 [U] barrio; v5 [U] sin el 1 % superior (5) |
| E1-R4 | < 500 m frente a 500-1.000 m; tratamiento desde 2014 | v1 [C] resto de Barcelona como control; v2 [E] radios de 300 m y 300-800 m (2) |
| E1-A1 | València, Sevilla, Málaga y Alicante; % de viviendas VUT en media anual; distancia × año; 2021-2024 | v1 [V] 2022-2024; v2 [U] con Barcelona; v3 [M] IPVA por distrito; v4 [P] ponderada por viviendas; v5 [M] % de plazas VUT; v6-v9 [U] cada ciudad por separado; v10 [U] sin el 1 % superior; v11 [C] sin distancia × año (11) |
| E1-A2 | de Chaisemartin-D'Haultfœuille con dosis continua; Málaga y Sevilla; 2015-2024 | v1 [E] Callaway, Goodman-Bacon y Sant'Anna; v2 [U] solo Málaga; v3 [U] solo Sevilla; v4 [E] Callaway-Sant'Anna con dosis binaria (4) |

**E2 (27 variantes)**

| Id | Principal | Variantes |
|---|---|---|
| E2-R1 | Trimestral 2019T1-2022T1; controles de JMS; sin Barcelona; paro registrado; anticipación 2020T3; base 2019T4 | v1 [V] sin 2020T1-2020T3 en el preperiodo; v2 [U] con Barcelona; v3 [C] controles por covariables; v4 [C] controles a más de 10 km; v5 [C] sin covariables; v6 [C] HUT 2019 × posterior; v7 [E] anticipación desde 2019T2; v8 [V] anual 2014-2021 con Honest DiD; v9 [M] SERPAVI municipal anual 2016-2021; v10 [P] ponderada por contratos de 2019; v11 [U] sin el 1 % de municipios con más contratos (11) |
| E2-R1c | Log de contratos por 1.000 habitantes | v1 [M] contratos por hogar inquilino; v2 [E] PPML; v3 [V] sin 2020T1-2020T3; v4 [U] con Barcelona (4) |
| E2-A1 | Callaway-Sant'Anna, cohortes de 2024T2 y 2024T4; 2022T1-2026T1 | v1 [E] efectos fijos de dos vías; v2 [E] emparejamiento por puntuación de propensión (como Pérez García); v3 [E] SDID, si su Monte Carlo es apto; v4 [U] sin Barcelona; v5 [V] 2023T1-2026T1 (5) |
| E2-A2 | EMAL, renta mensual | v1 [M] €/m²; v2 [U] sin Bilbao (2) |
| E2-A3 | Compraventas por 1.000 habitantes, anual 2016-2022 | v1 [M] valor tasado; v2 [U] sin Barcelona; v3 [V] trimestral 2019-2022 (3) |
| E2-A4 | < 10 km frente a > 25 km | v1 [C] vecinos directos (frontera común, JMS p. 18); v2 [C] 10-25 km frente a > 25 km (2) |

**E3 (42 variantes)**

| Id | Principal | Variantes |
|---|---|---|
| E3-R1 | 2002-2008; cuotas del Censo 2001 con los 16 grupos; choque nacional; construcción × año y costa × año; región × año; peso: población de 1998 | v1 [V] 1998-2008; v2 [M] cuotas del padrón de 2003; v3 [M] Censo de 1991; v4 [P] sin ponderar; v5 [U] sin los grupos 1 y 2; v6 [C] sin construcción ni costa × año; v7 [C] ficticias de 2005 y 2006 × cuota no comunitaria; v8 [U] sin Barcelona; v9 [U] sin Alicante ni Málaga; v10 [E] choque sin la propia provincia, 2004-2008 (10) |
| E3-R1q | Iniciadas por inmigrante | v1 [M] terminadas; v2 [V] 1998-2008 (2) |
| E3-R2 | 2002-2010; elasticidad respecto a la población en edad de trabajar; solo redes | v1 [V] 2000-2010; v2 [M] población total; v3 [U] sin los grupos 1 y 2; v4 [C] sin construcción ni costa; v5 [P] sin ponderar; v6 [M] cuotas de 2003; v7 [M] Censo de 1991; v8 [U] sin Barcelona (8) |
| E3-R2b | 2002-2008 | v1 [V] 2001-2008 (1) |
| E3-R2q | Cantidad (iniciadas) | v1 [M] terminadas (1) |
| E3-A1 | Valor tasado, 2014-2022 | v1 [U] sin los grupos 1 y 2; v2 [M] cuotas de 2003; v3 [P] sin ponderar; v4 [M] IPV por CCAA (9 CCAA); v5 [U] sin Barcelona; v6 [C] sin construcción ni costa (6) |
| E3-A2 | SERPAVI provincial, 2014-2022 | v1 [M] IPVA; v2 [M] IPC de alquiler; v3 [U] sin los grupos 1 y 2; v4 [P] sin ponderar; v5 [M] cuotas de 2003; v6 [U] sin Barcelona (6) |
| E3-A3 | SERPAVI municipal, 2014-2022; cuotas municipales del padrón de 2003 | v1 [M] valor tasado municipal; v2 [U] sin municipios con distritos sellados; v3 [P] sin ponderar; v4 [U] municipios de más de 20.000 habitantes; v5 [U] sin los grupos 1 y 2 (5) |
| E3-A4 | Tenencia del Censo 2011, umbral en la mediana | v1 [M] umbral en el tercil; v2 [P] sin ponderar (2) |
| E3-A5 | Forma de A1, 2002-2019, partición 2002-2010 / 2011-2019 | v1 [V] 2004-2019 con el choque sin la propia provincia (1) |

**E5 (17 variantes)**

| Id | Principal | Variantes |
|---|---|---|
| E5-R1 | Bartik A*10 sin F, K y L; cuotas de afiliación de 2001; crecimiento nacional sin la provincia; 2002-2024; sin pesos | v1 [V] 2002-2007; v2 [V] 2008-2013; v3 [V] 2014-2024; v4 [M] los diez sectores; v5 [E] B_{p,t−1}; v6 [M] terminadas; v7 [U] sin Barcelona; v8 [U] sin Alicante, Málaga y Girona; v9 [P] ponderada por población de 2001; v10 [C] cajas de 2007 × año; v11 [M] secciones CNAE-2009 sin F, K y L, 2009-2024 (11) |
| E5-A1 | — | v1 [U] sin Barcelona (1) |
| E5-A2 | Áreas urbanas | v1 [M] terminadas; v2 [V] 2002-2007 (2) |
| E5-A3 | Municipios | v1 [U] sin municipios con distritos sellados; v2 [U] municipios de más de 10.000 habitantes; v3 [V] 2012-2019 (3) |

**E6 (14 variantes)**

| Id | Principal | Variantes |
|---|---|---|
| E6-R1 | Contiguas sin la propia; Sun-Abraham; cohortes 2015-2018; controles terminados en T+6 o después | v1 [M] SERPAVI de vivienda unifamiliar; v2 [E] fecha de evento = terminación − 2; v3 [U] sin València ciudad; v4 [U] con la sección propia; v5 [C] cerca frente a lejos (contiguas de segundo orden); v6 [U] umbral de 10 viviendas (6) |
| E6-R2 | IPVA provincial; lluvia de julio a septiembre | v1 [U] sin 2019 ni 2024 en València; v2 [M] IPC de alquiler trimestral; v3 [U] sin Barcelona; v4 [M] lluvia de agosto-septiembre (4) |
| E6-A1 | — | v1 [U] umbral de 100 viviendas; v2 [U] anillo de 500 m (2) |
| E6-A3 | — | v1 [V] 2002-2010; v2 [U] sin Barcelona (2) |

**E7 (25 variantes)**

| Id | Principal | Variantes |
|---|---|---|
| E7-R1 | h = 8; valor tasado real; LP-IV; sorpresa monetaria pura | v1 [V] sin 2010-2013; v2 [C] diferencial soberano a 10 años; v3 [M] sorpresa «poor man's»; v4 [M] sorpresa mediana; v5 [M] choque total; v6 [E] LP aumentada con errores EHW; v7 [M] euríbor a 1 año; v8 [E] h = 4; v9 [E] h = 12 (9) |
| R1-ipv, R1-cv, R1-alq | — | Cada una: v1 [V] sin 2010-2013; v2 [C] diferencial soberano (6) |
| E7-R2 | SVAR con proxy | v1 sin 2010-2013; v2 diferencial soberano; v3 VAR de 4 variables; v4 «poor man's» (4) |
| E7-R3 | BVAR recursivo | v1 prior más laxa; v2 2004-2019 (2) |
| E7-A1 | — | v1 sin 2010-2013 (1) |
| E7-A2 | Panel provincial con exposición | v1 [C] cuota de compradores extranjeros × choque; v2 [U] sin Barcelona; v3 [M] exposición 2007-2013 (3) |

**E8 (21 variantes)**

| Id | Principal | Variantes |
|---|---|---|
| E8-R1 | dCDH con dosis continua; fechas de entrada en vigor; recaudación previa; 2007T1-2026T2 | v1 [M] fechas del 1 de enero; v2 y v3 [M] fechas −3 y +3 meses; v4 [V] sin 2012-2013; v5 y v6 [E] subidas y bajadas por separado (Sun-Abraham); v7 [M] IPV por CCAA; v8 [U] sin Barcelona; v9 [C] sin recaudación previa (9) |
| E8-R2 | Compraventas mensuales, 2007-01 a 2024-12 | v1-v6 como en R1; v7 [U] sin Barcelona; v8 [C] sin recaudación previa (8) |
| E8-A1 | Recaudación | v1 sin 2012-2013; v2 fechas del 1 de enero (2) |
| E8-A2 | Municipios grandes | v1 sin 2012-2013; v2 sin Barcelona (2) |

**E9 (15 variantes)**

| Id | Principal | Variantes |
|---|---|---|
| E9-R1 | Riesgo = caída del PIB en el quintil superior; efecto a 4 trimestres | v1 [M] caída del empleo; v2 [M] precio de la vivienda en origen; v3 [U] sin Reino Unido; v4 [U] sin Alicante; v5 [U] sin Málaga; v6 [C] pernoctaciones por origen × exposición; v7 [E] horizonte de 8 trimestres (7) |
| E9-R2 | IV de la cuota de no residentes | v1 instrumento con el empleo; v2 sin Reino Unido; v3 pernoctaciones; v4 sin Alicante ni Málaga (4) |
| E9-A1 | — | v1 sin Reino Unido; v2 sin Alicante (2) |
| E9-A2 | — | v1 sin Cataluña; v2 sin ponderar (2) |

**E10 y E12 (10 variantes)**

| Id | Variantes |
|---|---|
| E10-A1 | v1 [M] % de personas jurídicas; v2 [U] sin Barcelona; v3 [C] sin controles; v4 [U] municipios de más de 10.000 habitantes (4) |
| E12-A1 (principal con obra libre 1991-1995 × año) | v1 [C] sin ese control; v2 [U] sin Barcelona; v3 [M] terminadas; v4 [V] 2002-2013 (4) |
| E12-A2 | v1 sin Barcelona; v2 2002-2013 (2) |

**F (34 variantes)**

| Id | Variantes |
|---|---|
| F1-R1 | v1 población total; v2 sin 2008-2013; v3 IPV desde 2007; v4 tipo nominal (4) |
| F1-R2, R2-alt y R2-pmg | Cada una: v1 PIB per cápita como sustituto; v2 2000-2008 (6) |
| F1-A1 | v1 sin 2008-2013; v2 PIB per cápita; v3 CCE-MG (3) |
| F1-A2 | v1 sin parque; v2 sin 2008-2013 (2) |
| F1-A3 | Una por modelo: R1, A2 y R2 (3) |
| F2-R1 | v1 SERPAVI; v2 sin hogares; v3 sin 2008-2013 (3) |
| F2-A1 | v1 SERPAVI; v2 sin 2008-2013 (2) |
| F2-A2 | v1 amortización del 3 %; v2 ganancia esperada nula (2) |
| F3-R1 | v1 sin costes; v2 precio sin retardo (2) |
| F3-A1 | v1 sin costes; v2 sin 2008-2013 (2) |
| F3-A2 | v1 sin suelo; v2 sin crédito; v3 sin 2008-2013 (3) |
| F3-A3 | v1 B_{t−1}; v2 los diez sectores (2) |

**Total:** 40 + 27 + 42 + 17 + 14 + 25 + 21 + 15 + 10 + 34 = **245 variantes**.

## Anexo B. Referencia única por especificación (I6) y δ del TOST

δ = ½·|referencia|. Sin referencia en la misma unidad, I6 «no aplicable» y δ = 0,05 en log (en la unidad de la especificación). El estado es el de la ficha de docs/v18/bib.

| Id | Referencia única | Valor (error) | Estado de la ficha | δ |
|---|---|---|---|---|
| E1-R1, R2, R3, A1, A2 | Segú (2018), IV lineal, por pp de densidad | 0,038 (0,012) | NO VERIFICADA | 0,019 |
| E1-R4 | — (no aplica) | — | — | 0,05 |
| E2-R1 | Jofre-Monseny et al. (2023), tabla 2, col. 3, p. 12 | −0,045 (0,006) | VERIFICADA (cuartil no verificado) | 0,022 |
| E2-R1c | — (la referencia, −0,003, es ≈ 0 y la razón no está definida) | — | — | 0,05 |
| E2-A1, A2 | Pérez García (2026) | −0,0298 (0,0113) | VERIFICADA (DataCite; preprint) | 0,015 |
| E2-A3 | — | — | — | 0,05 |
| E2-A4 | Jofre-Monseny et al. (2023), vecinos directos, p. 18 | −0,027 (sin error leído: sin vía de solapamiento) | VERIFICADA | 0,0135 |
| E3-R1 | González y Ortega (2009, IZA), €/m² por punto | 44,72 (18,58) | NO VERIFICADA | 22,4 |
| E3-R1q | Ídem, viviendas por inmigrante | 0,462 (0,033) | NO VERIFICADA | 0,231 |
| E3-R2 | González y Ortega (2011), solo redes, 2001-2010 | 0,959 (0,984) | NO VERIFICADA | 0,48 |
| E3-R2b | Ídem, 2001-2008 | 0,927 (0,596) | NO VERIFICADA | 0,46 |
| E3-R2q | Ídem, cantidad | 1,05 (0,578) | NO VERIFICADA | 0,525 |
| E3-A1, A5 | Sanchis-Guarner, precios, semielasticidad | 3,046 (1,214) | DISCREPANTE (año) | 1,52 |
| E3-A2, A3 | Sanchis-Guarner, alquileres | 0,947 (0,470) | DISCREPANTE (año) | 0,47 |
| E3-A4 | — (dos endógenas) | — | — | 0,47 |
| E5-R1, A2, A3 | Taltavull (2006), panel de CCAA 1990-2004 | 0,87 (0,125, desde t = 6,96) | NO VERIFICADA | 0,435 |
| E6-R1, A1 | Asquith et al., «cerca frente a cerca» | −0,062 (0,037) | DISCREPANTE (año) | 0,031 |
| E6-R2, A3 | Mense (2025) | −0,192 (0,065) | VERIFICADA | 0,096 |
| E7-R1, R1-ipv, R2, R3, A1 | San Juan (2023), precio a 8 trimestres por +100 pb | −2 % (intervalos al 68 %: sin vía de solapamiento) | VERIFICADA | 1,0 pp |
| E7-R1-cv | San Juan (2023), compraventas | −3 % | VERIFICADA | 1,5 pp |
| E7-R1-alq, A2 | — | — | — | 1,0 pp |
| E8-R1 | Dolls et al. (versión publicada) | −3 % por pp | VERIFICADA | 1,5 pp |
| E8-R2, A2 | Fritzsche y Vandrei | −6 % por pp | VERIFICADA | 3 pp |
| E8-A1 | — | — | — | 0,05 |
| E9-R2, A2 | Sá (2016), IV en volumen | +2 % por pp | VERIFICADA | 1,0 pp |
| E9-R1, A1 | — (forma reducida) | — | — | 0,05 |
| E12-A1 | Chapelle (2015), sin combinar | −1,604 (0,219) | NO VERIFICADA | 0,80 |
| E12-A2, E10-A1, F | — | — | — | — |

δ por factor para el B5 (el de su estimación propia): E1 0,019; E2 0,022; E3 0,48; E5 0,435; E6 0,096; E7 1,0 pp; E8 1,5 pp (precio) y 3 pp (volumen); E9 1,0 pp.

## Anexo C. Cortes temporales por especificación (regla 1.4)

| Especificación | Variables y cortes |
|---|---|
| E1-R1 a R4 | SERPAVI hasta 2024. HUT de Barcelona y noches de Eurostat por la regla (e), dentro de la ventana hasta 2024. ADRH por sección hasta 2023. Población del censo anual hasta 2025 |
| E1-A1 | INE-VUT: clave mensual 2026-05, medias anuales hasta 2025. Ventana limitada por SERPAVI: 2021-2024 |
| E1-A2, A3 | Registro de Andalucía por la regla (e). Registro reconstruido de la GVA hasta 2025-01 |
| E2-R1, R1c | Incasòl trimestral hasta 2026T1 (prueba de reversión hasta 2023T4) y anual hasta 2025 (robustez 2014-2021). Paro del SEPE por la regla (e). HUT de IDESCAT hasta 2025 |
| E2-A1 | Incasòl hasta 2026T1. Zonas tensionadas vigentes hasta 2026T3 |
| E2-A2 | EMAL hasta 2025T4 |
| E2-A3 | Valor tasado municipal (p_tasado) trimestral hasta 2026T2. Compraventas municipales por la regla (f): hasta 2024-12. Ventana 2016-2022 |
| E3-R1 a R2q | Ventanas dentro de 1998-2010. Valor tasado provincial anual hasta 2024. Población provincial hasta 2024 |
| E3-A1 a A4 | Padrón por nacionalidad provincial y municipal hasta **2022**. ECP por nacionalidad, por sustitución, hasta 2022. Ventanas 2014-2022 |
| E3-A5 | 2002-2019 |
| E5-R1, A1, A2 | Iniciadas y terminadas anuales hasta 2024. Valor tasado anual hasta 2024. Ventana 2002-2024 |
| E5-A3 | Obra nueva del Catastro hasta 2025. Valor tasado municipal: años completos hasta 2025 |
| E6-R1 | SERPAVI hasta 2024. Catastro INSPIRE hasta 2026-08-21 |
| E6-R2 | IPVA hasta 2024. Terminadas trimestrales hasta 2026T2. IPC de alquiler provincial (ipc_alquiler_indice) hasta 2024 (A) y 2026T2 (T) |
| E7 | Sorpresa monetaria hasta 2025-10 (trimestral hasta 2025T3). Tipo hipotecario, euríbor, renta, crédito e inflación hasta 2026T2. Último origen con h = 8: 2024T2 |
| E8-R1 | Valor tasado trimestral hasta 2026T2 |
| E8-R2 | Compraventas mensuales hasta 2024-12 |
| E9 | Valor tasado hasta 2026T2. Cuota de no residentes del MIVAU por la regla (e) |
| E10-A1 | SERPAVI hasta 2024. Titularidad hasta 2026 |
| E12 | Obra libre anual hasta 2024. Protegida del MIVAU por la regla (e) |
| F1 a F3 | Variables nacionales hasta 2026T2 (medias anuales hasta 2025). Provinciales: anuales hasta 2024 |

---

## Tabla consolidada

«Estado»: principal, coprincipal (P), variante o NO ESTIMABLE, tras la adenda y antes de las comprobaciones de la sección 1.3, que pueden pasar más especificaciones a NO ESTIMABLE. «Familia Holm»: la del factor, o «fuera» si su tope es ASOCIACIÓN o no se estima. «Clasificación máxima»: valor máximo del campo clasificacion_v18. La capa es siempre C4 y nivel_evidencia, EXPLORATORIO. «Evaluable»: hipótesis de evaluate_v18 (sección 1.11).

| id | estado tras la adenda | familia Holm | repite_visto | clasificación máxima posible | evaluable en evaluate_v18 |
|---|---|---|---|---|---|
| E1-R1 | principal | E1 | sí (V9-D2) | SUGESTIVO | no |
| E1-R2 | principal | E1 | no | SUGESTIVO | no |
| E1-R3 | principal | E1 | sí (V9-D2) | SUGESTIVO | no |
| E1-R4 | principal | E1 | no | SUGESTIVO | no |
| E1-A1 | principal | E1 | sí (H3) | IDENTIFICADO | sí |
| E1-A2 | principal | E1 | sí (Q2b) | SUGESTIVO | no |
| E1-A3 | variante (robustez de A1) | fuera | sí (como A1) | ASOCIACIÓN | no |
| E1-A4, E1-A5, E1-X1 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E1-P-H3, E1-P-D2, E1-P-Q2b | coprincipal | E1 | sí | no se clasifica | no |
| E2-R1 | principal | E2 | sí (V9-D1b) | IDENTIFICADO | no (episodio histórico) |
| E2-R1c | principal | E2 | sí (V9-D1b) | IDENTIFICADO (efecto nulo acotado) | no |
| E2-R2, E2-R2s, E2-R2-X1 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E2-A1 | principal (provisional) | E2 | sí (H1, H2) | IDENTIFICADO | sí |
| E2-A2 | principal | E2 | sí (V9-D1c) | SUGESTIVO | no |
| E2-A3 | principal | E2 | sí (Q1c) | IDENTIFICADO | no |
| E2-A4 | principal | E2 | no | IDENTIFICADO | no |
| E2-A5 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E2-P-D1b, E2-P-D1b-c, E2-P-H1, E2-P-H2, E2-P-D1c, E2-P-Q1c | coprincipal | E2 | sí | no se clasifica | no |
| E3-R1 | principal | E3 | sí (V9-D4) | IDENTIFICADO | no (episodio histórico) |
| E3-R1q | principal | E3 | sí (V9-D4) | IDENTIFICADO | no |
| E3-R2 | principal | E3 | sí (V9-D4) | IDENTIFICADO | no |
| E3-R2b | principal | E3 | sí (V9-D4) | IDENTIFICADO | no |
| E3-R2q | principal | E3 | sí (V9-D4) | IDENTIFICADO | no |
| E3-A1 | principal | E3 | sí (Q3-c1) | IDENTIFICADO | sí |
| E3-A2 | principal | E3 | sí (H4, Q3) | IDENTIFICADO | sí |
| E3-A3 | principal | E3 | sí (H4) | IDENTIFICADO | sí |
| E3-A4 (dos contrastes) | principal | E3 | no | SUGESTIVO | no |
| E3-A5 | principal | E3 | sí (V9-D4) | IDENTIFICADO | no |
| E3-P-D4, E3-P-Q3c1, E3-P-H4 | coprincipal | E3 | sí | no se clasifica | no |
| E4-X1 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E4-X2 | no se estima (Q7a) | fuera | sí (Q7a) | — | no |
| E4-L1 | solo literatura | fuera | — | — | no |
| E5-R1 | principal | E5 | sí (Q4, elección del instrumento) | IDENTIFICADO | sí |
| E5-R2 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E5-A1 | principal | fuera | no | ASOCIACIÓN | no |
| E5-A2 | principal | E5 | no | IDENTIFICADO | no |
| E5-A3 | principal | E5 | no | SUGESTIVO | no |
| E5-P-Q4a | coprincipal | E5 | sí | no se clasifica | no |
| E6-R1 | principal | E6 | no | IDENTIFICADO | no (episodio histórico) |
| E6-R2 | principal | E6 | no | IDENTIFICADO | sí |
| E6-A1 | principal | E6 | no | IDENTIFICADO | no |
| E6-A2 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E6-A3 | principal | E6 | no | IDENTIFICADO | no |
| E7-R1 (precio), R1-ipv, R1-cv, R1-alq | principal (4 contrastes) | E7 | sí (Q5; V8 H8-5 a H8-7) | IDENTIFICADO (SUGESTIVO con F < 10) | no |
| E7-R2 | principal | E7 | sí (V8 H8-5 a H8-7) | IDENTIFICADO (SUGESTIVO con F < 10) | no |
| E7-R3 | principal | fuera | no | ASOCIACIÓN | no |
| E7-A1 | principal | fuera | no | ASOCIACIÓN | no |
| E7-A2 | principal | E7 | sí (V9-D5) | SUGESTIVO | no |
| E7-A3, E7-A2-X1 | NO ESTIMABLE (A3, hasta la licencia) | fuera | — | NO ESTIMABLE | no |
| E7-P-Q5, E7-P-H8-5, E7-P-H8-6, E7-P-H8-7, E7-P-D5 | coprincipal | E7 | sí | no se clasifica | no |
| E8-R1 | principal | E8 | sí (Q6-p) | IDENTIFICADO (solo con fechas exactas y tamaño en [0,04; 0,06]; si no, SUGESTIVO) | no (episodio histórico) |
| E8-R2 | principal | E8 | sí (Q6-v) | ídem | no |
| E8-A1 | principal | E8 | no | ídem | no |
| E8-A2 | principal | E8 | no | ídem | no |
| E8-X1, E8-X2 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E8-P-Q6p, E8-P-Q6v | coprincipal | E8 | sí | no se clasifica | no |
| E9-R1 | principal | E9 | no | SUGESTIVO | no |
| E9-R2 | principal | E9 | no | IDENTIFICADO (NO ESTIMABLE con 1/HHI < 10) | no |
| E9-A1 | principal | E9 | no | SUGESTIVO | no |
| E9-A2 | principal | E9 | no | IDENTIFICADO | no |
| E9-X1, E9-X2 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E10-X1 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E10-A1 | principal | fuera | no | ASOCIACIÓN | no |
| E11-X1, E11-X2 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E12-X1 | NO ESTIMABLE | fuera | — | NO ESTIMABLE | no |
| E12-A1 | principal | E12 | no | SUGESTIVO | no |
| E12-A2 | principal | E12 | no | SUGESTIVO | no |
| F1-R1 | principal | F (cointegración) | sí (V7.2, V8-M4) | ASOCIACIÓN | no |
| F1-R2, F1-R2-alt, F1-R2-pmg | principal | F (cointegración) | sí (V7.2) | ASOCIACIÓN | no |
| F1-A1 | principal | F (cointegración) | sí (V15 E1-P2, Q9-c) | ASOCIACIÓN | no |
| F1-A2 | principal | F (cointegración) | sí (V7.2, V8-M4) | ASOCIACIÓN | no |
| F1-A3 | principal (no se publica sin cointegración) | fuera | sí (como R1) | ASOCIACIÓN | no |
| F1-P-V72, F1-P-M4, F1-P-E1P2 | coprincipal | F (cointegración) | sí | no se clasifica | no |
| F2-R1, F2-A1 | principal | F (cointegración) | no | ASOCIACIÓN | no |
| F2-A2 | principal | fuera | sí (V15 E1) | ASOCIACIÓN | no |
| F3-R1, F3-A1, F3-A2 | principal | F (cointegración en A2) | no | ASOCIACIÓN | no |
| F3-A3 | principal | fuera | no | la de E5-R1, sin pasar de SUGESTIVO por la exclusión de F3 | no |
| F4-1 a F4-5 | comparación (condicionada a la cointegración) | fuera | — | no aplica | no |
| B5-E1 … B5-E9, B5-F | derivadas (sección 1.9) | fuera | — | no aplica | no |
| C5-* | derivadas (sección 1.10) | fuera | — | no aplica | no |

*Fin de la adenda. Con el plan, forma el pre-registro interno que fija la etiqueta local `plan-replicacion-v18`, que se pone antes de la primera estimación.*
