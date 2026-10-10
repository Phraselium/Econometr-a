# Revisión independiente v3 — oleada 3 (puerta final)

Revisor independiente. Alcance: identificación, capas, neutralidad y conclusiones de los entregables de la oleada 3. No he reproducido el pipeline ni he reabierto los resultados de las oleadas 1 y 2, salvo donde un entregable los contradice. HEAD revisado: `a2a5549` (rama r3/main).

Entregables revisados:
- output/v3/lo_que_sabemos.md
- output/v3/articulo.md
- output/v3/informe_politica.md (con el módulo València)
- output/v3/verificador/verificador.md, las fichas V01-V14 y el docstring de src/v3/verificador.py
- docs/v3/solicitudes_transparencia.md
- docs/v3/limitaciones.md

## Veredicto: **REHACER**

Las cifras principales coinciden con sus fuentes y ningún resultado se presenta como C3. Hay cuatro tipos de problema que impiden aprobar:
1. **Módulo València.** Tiene dos errores numéricos, mezcla oleadas y medidas sin advertirlo y omite la cifra provincial que apunta en sentido contrario.
2. **«Afirmable con seguridad».** Incluye cifras con una capa superior a la de su fuente o sin fuente en output/v3.
3. **Verificador.** Aplica la regla de periodos de forma asimétrica (V05 frente a V04, V08 y V12).
4. **Lenguaje.** Quedan restos de lenguaje causal en cifras C4 y adjetivos valorativos.

Todos los cambios son de texto o de trazabilidad: ninguno exige volver a estimar.

## Muestreo de cifras (27 comprobadas)

| # | Cifra en el entregable | Fuente | Valor en la fuente | Capa (entregable / fuente) | Estado |
|---|---|---|---|---|---|
| 1 | +701.000 (560.000-969.000), 2021-2025 | PA A1_nacional_2021-2025 | 701.187 [559.752; 969.059] | C1 / C1 | OK |
| 2 | Desde 2012, signo no determinado (−436.000 a +1.501.000) | PA A1_nacional_2012-2025 | [−436.271; 1.500.620] | C1 / C1 | OK |
| 3 | 40-50 % viven con sus padres | PA A2_tasa_convivencia | [40,3; 50,2] | C1 / C1 | OK |
| 4 | 30,7-31,8 %; −24 a −34 pp | PA A5 | [30,7; 31,8]; [−34,0; −24,2] | C1 / C1 | OK |
| 5 | 83-89 % (65 años o más) | PA A5_propiedad_65_mas | [83,0; 89,4] | C1 / C1 | OK |
| 6 | 3,0-4,1 veces la renta | PA A4_precio_renta_nacional | [2,99; 4,11] | C1 / C1 | OK |
| 7 | 27-36 % de las vacías en el tercil alto | PA A3_vacias_tercil_alto_vs_bajo | 27,5-36,0 % (rango de medida, 277 municipios); el rango de definición es 30,4-40,3 % | C1 / C1 | **Incompleto**: falta el rango de definición y la base no es «3,8 millones» (Z3) |
| 8 | 3,8 millones de vacías | Solo en la ficha V08 («estimación por consumo eléctrico»); no aparece en PA | — | C1 / sin fuente C1 | **FALLA** (Z3) |
| 9 | Terminadas: 89.000-101.000 al año | PD resultado.json, `terminadas_2021_25_rango` [89.320; 100.980] | MIVAU, fuente única | C1 / sin hecho C1 | **FALLA**: capa superior (Z4) |
| 10 | Compraventas de extranjeros: 9,6-15,0 % | Ficha V14 (data/processed v2); no aparece en PA | MIVAU 9,6-11,0; Registradores 13,8-15,0 | C1 / fuera de las fuentes v3 | Trazabilidad débil (Z4) |
| 11 | VUT ≤2,4-2,7 % del stock | PB B1-nac-cantidad | 2,42-2,75 | C2 / C2 | OK |
| 12 | «Una cuarta parte» de la subida, donde las VUT apenas crecieron | PB `no_explica` 25,03 | 25,0 % | C2 / C2 | OK (sin intervalo) |
| 13 | «Desde 2024 … la cota superior es 0» | PB B1-nac-precio-eps_min-2024M08-2026M05 | 0 / −6,34 | C2 / **C4** | **FALLA**: capa superior (Z4) |
| 14 | Inmigración ≤45 % (2014-2019) | PB B2-nac-cuota-2014-2019 | 45,2 (sensibilidad 15,1-45,2) | C2 / C2 | OK |
| 15 | 104.000-413.000 viviendas/año | PD P1 | 103.560-413.004 | C2 / C2 | OK |
| 16 | Vacías movilizadas: 4,6-51 % de la brecha | PD P4 | 4,65-51,18 | C2 / C2 | OK |
| 17 | Topes: −5,4 % [−7,1; −3,7]; −37 €/mes | C3 H3-3a CS | −5,41 [−7,09; −3,70]; −36,95 | C4 / C4 | OK |
| 18 | SERPAVI −0,8 %; Holm 0,048 | C3 sellado; holm_v3.csv | −0,77 %; 0,0485 | C4 / C4 | OK |
| 19 | Contratos −4,9 % [−9,9; +0,5]; SERPAVI −4,4 % | C3 H3-3b | −4,87 [−9,93; 0,47]; −4,36 | C4 / C4 | OK |
| 20 | H3-1: entrenamiento 0,00026 [−0,0007; 0,0013]; sellado 0,00105 (p 0,23); Holm 0,47 y 0,50 | C1 resultado y sellado | idéntico | C4 / C4 | OK |
| 21 | H3-1 sellado en 6 ciudades: −0,0013 [−0,0034; 0,0008], p 0,20 | C1 sellado_H3-1.json | −0,00130 [−0,00336; 0,00076], p 0,203 | C4 / C4 | OK |
| 22 | H3-2: F = 60; multiverso 75 % / 10 %; H3-3a 100 % / 89 % | sellado_H3-2.json (F sellado 60,5; F de entrenamiento 21,9); multiverso_*.csv | idéntico | C4 | OK |
| 23 | Topes: 148-598 €/año; esfuerzo de −2,9 % a +7,3 % | PD P3 | 147,8-598,2; −2,93 a +7,25 | C4 / C4 | OK |
| 24 | Retirada de VUT: ≤31.000 viviendas; −2,0 % a +0,5 % | PD P2, X = 100 % | 30.595; −1,995 a +0,487 | C2 / C2 y C4 / C4 | OK (pero «efecto», Z5) |
| 25 | València: ≤1,9 %; ≤5,8 % (≈29 €); provincia ≤9,6 %; 28 % (575 secciones); +28,7 % | PB B1-ciudad-46250, B1-prov-46, registro B1-seccion-València, b1_ciudades.csv | 1,93; 5,84; 28,69 €; 9,6; 28,3 %; 28,72 % | C2 / C2 y C4 / C4 | OK |
| 26 | València: «≥80 %» no cubierto; «como máximo una quinta parte» | PB `no_explica_agregado_pct` 79,66 | 79,7 % no cubierto, es decir, 20,3 % cubierto | C4 | **FALLA**: 79,7 < 80 y 20,3 % > 1/5 (Z1) |
| 27 | València: VUT 5.973 (feb. 2021) → 7.976 (ago. 2024) → 5.393 (may. 2026); balance 52.000-69.000; precio/renta 3,8/3,0; alquiler/renta 18,1/16,3; cuota 18,8/15,0; réplica GL +0,005 [0,0001; 0,010] | b1_ciudades.csv (2020: 6.899; 2024: 7.976); A1_provincial_resumen; A4_*; GL | 7.976 y el resto OK. **5.973 y 5.393 no aparecen en ninguna salida**; la cota usa la base de agosto de 2020 (6.899), no la de febrero de 2021 | C4 | **FALLA** de trazabilidad y de oleadas (Z1) |

## «Afirmable con seguridad» (lo_que_sabemos.md)

La sección mezcla C1 y C2, lo que está permitido. Hay cuatro elementos que no cumplen la regla:
- **Capa superior a la de la fuente o sin fuente C1:**
  - las terminadas (fuente única, sin hecho C1 en PA);
  - los 3,8 millones de vacías (fuente única, por consumo eléctrico, sin hecho en PA);
  - la cota 0 desde 2024 (la fila de origen es C4).
- **«Solo el 27-36 % está…».** El porcentaje se calcula sobre los municipios con dato (277), no sobre los 3,8 millones. Además omite el rango de definición (30,4-40,3 %) y el dato de contraste del tercil bajo (20,7-28,3 %). Con ese contraste, el tercil alto concentra más vacías que el bajo. «Solo» es un adverbio valorativo.
- **«Una cuarta parte».** Le falta el intervalo de sensibilidad o la indicación expresa de que es un valor puntual.
- **«Los datos están pedidos al Catastro».** Es falso: según docs/v3/solicitudes_transparencia.md, las solicitudes están «redactadas, no presentadas». Lo mismo ocurre en el artículo («se han pedido»).

## Módulo València

- **Periodos.** La tabla mezcla, una fila junto a otra, tres cosas distintas, y no lo advierte:
  - la ciudad en el ámbito municipal, 2020-2024 (cota de 1,9 % y subida SERPAVI de +28,7 %);
  - las secciones, 2021M08-2024M08 (28 %);
  - una serie de VUT con oleadas de febrero, agosto y mayo (5.973 → 7.976 → 5.393).

  Las dos primeras están rotuladas con su periodo, pero falta una nota que diga que no son comparables. La serie de VUT es más grave:
  - compara oleadas de meses distintos, con estacionalidad;
  - no coincide con la base de la cota (agosto de 2020: 6.899);
  - sus valores de 2021 y 2026 no salen de ninguna salida de output/v3;
  - «bajó por debajo del nivel de 2021» compara mayo de 2026 con febrero de 2021.
- **Medidas distintas.** La cota de la ciudad usa SERPAVI y la de la provincia usa el IPC de alquiler provincial. La fila «Cota de precio» las pone juntas sin decirlo.
- **Asimetría.** Para la ciudad el módulo informa de que la cota cubre «como máximo una quinta parte» (y lo que no cubre como «≥80 %»). No informa de que, en la provincia, `no_explica` = 0 %: allí la cota con |ε| = 0,33 cubre toda la subida (PB B1-prov-46). Las dos lecturas proceden del mismo método con medidas distintas. Por la regla «si dos métodos discrepan, se reportan ambos», hay que dar las dos.
- **Errores numéricos.** «≥80 %» debe decir 79,7 %. «Como máximo una quinta parte» debe decir 20,3 %.
- **Réplica de García-López en València.** La etiqueta PARCIAL es correcta, pero faltan dos datos: p_Holm = 0,37 (familia de 15) y 15 clústeres. Sin ellos, la fila parece más sólida que el resto de la réplica (NO REPLICADO en Barcelona, Sevilla, Madrid, Málaga y España).
- **«Su aumento … es pequeño (≤1,9 %)».** El adjetivo sobra: basta la cifra.

## Neutralidad

1. **V05 frente a V04, V08 y V12 (asimetría de regla).** V05 («faltan cientos de miles de viviendas») queda RESPALDADA con una sola ventana (2021-2025). Sin embargo:
   - la propia ficha admite que con 2012 como base el signo no está determinado;
   - la limitación 7 reconoce que las ventanas C1 se añadieron después de ver las fuentes;
   - la regla general del docstring dice «PARCIALMENTE: respaldada en parte (zonas, periodos…)», y esa regla se aplica a V08 y V11.

   Con la regla tal como está escrita, V05 debe ser PARCIALMENTE. La alternativa es justificar en el docstring por qué el periodo reciente basta. En ese caso hay que aplicar el mismo criterio de «periodo reciente» a todas las fichas.
2. **«No se puede afirmar con estos datos».** Solo lista la atribución principal a las viviendas turísticas. El verificador trata igual cuatro atribuciones (V01 turísticas, V03 inmigración, V04 oferta y suelo, V12 tipos), todas SIN EVIDENCIA SUFICIENTE. La sección debe listar las cuatro o ninguna.
3. **Vacías.** «Solo» aparece en lo_que_sabemos.md, en el resumen del artículo («Solo un tercio») y en V08 («Solo … la mayor parte no está donde sube el precio»). La palabra es valorativa y omite el rango de definición y el contraste con el tercil bajo.
4. **Adjetivos en C4.** «Asociación … pequeña» (lo_que_sabemos), «es pequeño» (informe) y «desplazamiento pequeño» (V01). Hay que sustituirlos por la cifra.
5. **Solicitudes de transparencia.** Son neutrales:
   - cubren dos temas asociados a posiciones distintas (grandes tenedores y suelo);
   - piden datos agregados;
   - la finalidad está redactada sin juicio.

   No requieren cambios, salvo la coherencia de «pedidos» señalada arriba.
6. **Informe de política.** No recomienda opciones. Trata con simetría los casos de signo no estable (turísticos y topes: «pueden mejorar o empeorar»). La tabla de palancas es correcta.

## Lenguaje causal por debajo de C3

- lo_que_sabemos.md: «[C4] **Su efecto** sobre el alquiler local va de −2,0 % a +0,5 %».
- informe_politica.md: «**efecto** local en alquiler de −2,0 % a +0,5 % con H3-1 sellado».

Las dos frases son C4. PD declara: «asociación, no efecto causal». Hay que escribir «variación asociada (C4)» o «variación simulada».

lo_que_sabemos.md, en la viñeta C4 sobre VUT: «se asocia a un alquiler mayor en menos de un 0,5 %. En los distritos sellados el IC95 incluye 0». La frase sugiere que en el entrenamiento hay una asociación positiva distinta de cero. No la hay: el IC95 es [−0,0007; 0,0013] y p = 0,61. Hay que decir que el IC95 incluye 0 en el entrenamiento y en el sellado, y dar la cifra (+0,04 % por 1,37 pp en entrenamiento y +0,14 % en el sellado).

## Artículo

| Requisito | Estado |
|---|---|
| Replicación | Sí (GL, MESVAL, JMS) |
| Extensión | Sí |
| Capas | Sí |
| Multiverso | Sí (H3-1, H3-3a) |
| Sensibilidad | Sí (RV, Oster, Rambachan-Roth) |
| Limitaciones | Sí |
| Reproducibilidad | Sí |
| Declaración de uso de IA | Sí |
| **Lista de referencias con DOI, VERIFICADA / NO VERIFICADA y cuartil** | **No.** La §10 afirma que «las referencias se verificaron con DOI», pero el artículo no tiene lista de referencias. Los datos existen en docs/v3/literatura_v3.md (GL: Q1 VERIFICADA; JMS: Q1 VERIFICADA; MESVAL: NO VERIFICADA) |
| **«Qué cambia cada mejora»** | **Parcial**, por tres motivos: |

1. **García-López.** Solo cuantifica el cambio del objetivo (de 0,039 a 0,012). No cuantifica cuánto se mueve la estimación propia con cada decisión: sección frente a distrito (−0,0042 frente a −0,0054), exclusión de los distritos sellados, vut100 frente a vut_cien, y el rango de T de 0,012 a 0,117.
2. **JMS.** «Ampliar el control a todos los no sujetos la atenúa a −0,033» usa EXT1, que también amplía el periodo a 2023. Son dos cambios a la vez: hay que separarlos o decirlo.
3. **Contratos.** La tabla solo da TWFE (R1: +0,030). Debe dar también CS (R2: −0,020 [−0,083; 0,042]), como hace V07.

## Limitaciones: lo que falta en docs/v3/limitaciones.md

- **Vacías.** Proceden de una estimación por consumo eléctrico de una sola fuente (Censo 2021). El reparto por tercil se calcula sobre 277 municipios y depende de la definición de presión (27,5-40,3 %).
- **VUT del INE.** Son una estadística experimental:
  - cubren ≈90 % del total publicado;
  - las oleadas son de meses distintos, con estacionalidad;
  - las comparaciones entre oleadas solo son válidas dentro del mismo mes.
- **Terminadas del MIVAU.** Son de fuente única y cubren menos que la variación del parque (esto ya figura en PA, pero no en las limitaciones del entregable).
- **Módulo València.** Usa medidas de alquiler distintas para la ciudad (SERPAVI) y la provincia (IPC), y periodos distintos para ciudad y secciones.
- **Dependencia de V05 de la ventana A1 elegida a posteriori.** Hay que enlazar la limitación 7 con el veredicto.
- **Réplicas de García-López con 8-16 clústeres.** Las p sin ajustar son engañosas; las p de Holm están todas por encima de 0,04.

## Cambios obligatorios (por prioridad)

- **Z1. Módulo València (cifras, periodos y simetría).**
  - Corregir «≥80 %» a 79,7 % y «como máximo una quinta parte» a 20,3 %.
  - Añadir la fila provincial de la parte no cubierta (0 %: la cota cubre toda la subida con el IPC provincial) y advertir que la ciudad (SERPAVI) y la provincia (IPC) usan medidas distintas.
  - Sustituir la serie de VUT por la misma oleada que la cota (agosto: 6.899 en 2020 y 7.976 en 2024), o citar el fichero de origen de 5.973 y 5.393 y advertir que son oleadas de meses distintos. Reformular «bajó por debajo del nivel de 2021».
  - Añadir una nota de que la fila de secciones (2021M08-2024M08) y las filas de la ciudad (2020-2024) no son comparables.
  - Añadir p_Holm = 0,37 y G = 15 en la réplica de García-López para València.
  - Quitar «pequeño».
- **Z2. Simetría del verificador y de «No se puede afirmar».**
  - Pasar V05 a PARCIALMENTE (respaldada en 2021-2025 y no determinada desde 2012), o justificar en la regla común un criterio de periodo que se aplique a todas las fichas.
  - Propagar el cambio a lo_que_sabemos.md, al artículo (§7, recuento 1/2/11) y al informe.
  - En «No se puede afirmar», listar las cuatro atribuciones de «causa principal» (V01, V03, V04, V12), o ninguna.
- **Z3. Vacías.**
  - Quitar «27-36 % de 3,8 millones»: el porcentaje se calcula sobre los municipios con dato.
  - Dar el rango completo (27,5-40,3 %) y el del tercil bajo (20,7-28,3 %).
  - Eliminar «Solo» en lo_que_sabemos.md, el resumen del artículo y V08.
  - Para los 3,8 millones, añadir un hecho en PA con dos fuentes (C1) o rebajarlos a C4 de fuente única y sacarlos de «Afirmable».
- **Z4. Capas superiores a la de la fuente en «Afirmable» y en la tabla del §3 del artículo.**
  - Terminadas 89.000-101.000: crear el hecho en PA con dos fuentes (fin de obra y calificaciones) o etiquetarlas como C4 de fuente única.
  - «Desde 2024 la cota superior es 0»: crear una fila C2 de cantidad en PB o rebajarla a C4.
  - Compraventas de extranjeros 9,6-15,0 %: dar como origen una salida de output/v3 (PA), no data/processed v2.
- **Z5. Lenguaje causal y adjetivos en C4.**
  - Cambiar «Su efecto sobre el alquiler local» (lo_que_sabemos.md) y «efecto local en alquiler» (informe) por «variación asociada (C4)».
  - Corregir la viñeta C4 de VUT para decir que el IC95 incluye 0 también en el entrenamiento, con cifras.
  - Sustituir «pequeña», «pequeño» y «desplazamiento pequeño» por las cifras.
- **Z6. Coherencia con las solicitudes de transparencia.** Cambiar «los datos están pedidos al Catastro» y «se han pedido por transparencia» por «solicitud redactada, pendiente de presentar».
- **Z7. Artículo.**
  - Añadir una lista de referencias con DOI, VERIFICADA / NO VERIFICADA y cuartil Scimago.
  - Completar «qué cambia cada mejora» con las cifras del efecto en cada paso de García-López.
  - Separar en JMS el cambio de grupo de control del de periodo.
  - Informar CS y TWFE en la fila de contratos.
- **Z8. Limitaciones.** Añadir las seis que faltan (sección anterior).

Tras aplicar Z1-Z8, una comprobación de texto basta para aprobar (`make check` y una relectura de las cifras tocadas). No hace falta volver a estimar ni abrir la muestra sellada.
