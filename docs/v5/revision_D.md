# Revisión del módulo D (v5, política): D1 matriz, D2 territorio, D3 convergencia

Revisor independiente. Fecha: 2026-10-10. No se ha reejecutado `make all` ni se ha leído data/sealed.

## Comprobaciones hechas

- `src/v5/d1_run.py`, `d2_run.py` y `d3_run.py`, sin red (`HTTPS_PROXY=http://127.0.0.1:9`):
  - salida 0 en los tres;
  - md5 de los .csv/.md de output/v5/D1-D3 idéntico antes y después (`db60b856…`); `git status` limpio.
- `python3 src/v3/check_texto.py`: 0 errores. `python3 src/v5/check_v5.py`: 0 errores. `ruff check`: sin avisos.
- Neutralidad:
  - Búsqueda de nombres de partidos, cargos y personas en todos los entregables D: 0 apariciones.
  - Búsqueda de términos valorativos y prescriptivos: solo aparece «No recomendados» en D2 (véase B1).
- Literatura. Se han comprobado en api.crossref.org 7 DOI (título, revista, autores y año): Oates-Schwab 1997, Krimmel-Wang 2026, Maltman-Greenaway-McGrevy 2025, Ball 2011, Mora-Sanguinetti 2012, Eriksen-Ross 2015 y Kangasharju 2010.
  - Los 7 resuelven y coinciden con la cita.
  - En Eriksen-Ross 2015, Hilber-Turner 2014, Diamond et al. 2019 (−15 % de oferta) y Segú 2020 (−13 % de vacancia), la descripción concuerda con el estudio publicado.
- Signo de I16 frente a I02: se ha revisado output/v3/PD/tablas/resultados_tabla.csv.
  - En I16 la cota superior es +0,0075 %, por lo que «no» (signo no estable) es correcto.
  - En I02 la cota superior es exactamente 0, por lo que «≤ 0» es correcto.
  - La asimetría solo es aparente y se debe al redondeo (véase N1).
- Capas:
  - Ayudas: signo por grupo en C2 con la regla común de M5-V1; traslado por clase en C4 con los métodos A y B reportados.
  - D2: C4 en resultado.json y en el texto. La cobertura «igual por construcción» está declarada como supuesto (politica_territorio.md, lectura transversal).
  - D3: no promueve capas.

## Hallazgos

| # | Tipo | Fichero:línea | Hallazgo | Corrección |
|---|---|---|---|---|
| B1 | **Bloqueante** (lenguaje, neutralidad) | src/v5/d2_run.py:21-23, 54, 61, 117 → output/v5/D2/politica_territorio.md:22, 30, 38, 46; politica_territorio.csv (columna `instrumentos_no_recomendados_por_evidencia`) | 1) «No recomendados por la evidencia» es una prescripción fuera del condicional, en un módulo C4. 2) En la clase 2, I29 y N4 entran en esa lista por literatura NO VERIFICADA, que solo puede usarse en robustez. 3) En la clase 3, «N2 No evaluable» aparece dentro de «No recomendados»: se mezcla «no evaluable» con un juicio. 4) La lista de ayudas omite el signo C2 por grupo (el beneficiario paga igual o menos), así que solo se presenta la parte desfavorable. 5) «C2 débil» (línea 23) no es una categoría de la escala. | 1) Renombrar la columna y la viñeta a algo descriptivo y condicional, por ejemplo «Con la evidencia disponible, instrumentos con mayor traslado esperado a precios en esta clase (C4)». 2) Sacar I29 y N4 a una línea «solo robustez (NO VERIFICADA)». 3) Poner «No evaluable» en su propio campo. 4) Añadir el signo por grupo de las ayudas. 5) Sustituir «C2 débil» por «C2 (≤ 0, posiblemente nulo)». |
| B2 | **Bloqueante** (D3: comparabilidad e independencia) | src/v5/d3_run.py:76-87 (`clasificar`), 146, 160 → output/v5/D3/convergencia.md:9 y filas R05, R06, R10, R15, R16, R19, R20, R21 | 1) `comparable == "parcial"` se trata igual que «si». Por eso R05/R06 (2022-2025 frente a 2021-2025), R10 (media 2019-2024 en territorio común frente a 2025 en España) y R21 (personas en 2025 frente a hogares en 2021-2022) figuran como «coincide», aunque el periodo, la cobertura o el concepto difieren. Con la misma condición «parcial», R01/R02 figuran como «difiere»: la regla es asimétrica. 2) El resumen «coinciden 10» incluye 4 controles de transcripción de la misma fuente (R15, R16, R19, R20) y cuenta dos veces la cifra de 600.000 del BdE (R05 y R06, la OCDE citando al BdE). Las notas lo advierten, pero el titular lo presenta como 10 coincidencias. | 1) Añadir el veredicto «comparable con salvedades (no cuenta)» para «parcial», o bien recalcular la cifra del proyecto en el mismo periodo (p. ej., déficit 2022-2024 y 2022-2025). R10 y R21 deben pasar a «no comparable». 2) Separar en el resumen: coincidencias independientes / controles de transcripción (misma fuente) / duplicados (R06 = R05). |
| B3 | **Bloqueante** (neutralidad, misma rúbrica) | src/v5/d1_run.py:131, 137-139 → output/v5/D1/matriz_instrumentos.csv (columna `clase_A4_donde_funciona`) | La columna de clase no sigue una regla común: 1) Los instrumentos de oferta o públicos con signo «No evaluable» (I03, I04, I05, I12, I13, I20, I26, I29, N1, N3, N4, N5, N6) reciben un texto de «dónde funciona» (p. ej., «1 (oferta responde) y 2…»). 2) Instrumentos regulatorios con evidencia comparable o mejor (I16, I18, I21, I22) reciben «No evaluable: sin evaluación por clase». 3) I01 recibe «la literatura sugiere más riesgo de capitalización en 2-3», sin referencia que lo respalde: la capitalización es el mecanismo de las ayudas, no el de un tope de renta. | Aplicar una sola regla: o bien a) «No evaluable: sin evaluación por clase» para todo instrumento sin signo evaluable, o bien b) una inferencia de mecanismo C4 para todos, también I01, I16, I18 e I21, redactada con la misma plantilla. Quitar o referenciar la frase de I01. |
| N1 | No bloqueante | src/v4/m5_run.py:61 (formato heredado) → output/v5/D1/matriz_instrumentos.md:38 (I16) | El rango «-1,7 a 0,0 %» oculta la cota superior +0,0075 %. Junto a I02 («-13,1 a 0,0 %», signo ≤ 0, C2) parece un trato distinto con datos iguales. | En D1, mostrar 2 decimales o «-1,70 a +0,01 %», y añadir «(cota superior > 0)». |
| N2 | No bloqueante | src/v5/d1_run.py:165, 235; output/v5/D1/fichas_verificador.json (campo `literatura`) | Gibbons-Manning 2006 figura como «VERIFICADA» en la matriz y como «VERIFICADA, cuartil no verificado» en la ficha. docs/literatura.md:467 la registra con «cuartil no verificado», lo que contradice la regla. | Usar «DOI verificado; cuartil no verificado», o registrar el cuartil de J. Public Economics (Q1, ya anotado para otras referencias) y marcarla VERIFICADA · Q1. |
| N3 | No bloqueante | src/v5/d1_run.py:165 | Hilber-Turner 2014 aparece como «VERIFICADA» sin cuartil. | Añadir «Q1». |
| N4 | No bloqueante | output/v5/D1/matriz_instrumentos.md:23 (I01, riesgos) | «contratos −4,9 % [−9,9; +0,5]» se presenta como riesgo sin advertir que el IC95 incluye 0. | Añadir «IC95 incluye 0». |
| N5 | No bloqueante | output/v5/D1/literatura_instrumentos.csv (I14, I04/I20); docs/literatura.md:498 | 1) El DOI de Mora-Sanguinetti (10.1007/s13209-011-0063-6) resuelve hoy en Crossref (SERIEs, 2011 en línea). 2) Ali-Raviola tiene DOI 10.1111/1540-6229.12525 (REE, 2025). 3) La descripción de I14 («efecto positivo menor sobre la propiedad frente al alquiler») es confusa: el título indica que la ineficiencia judicial aumenta el peso de la propiedad. | Pasar ambas a «DOI verificado; cuartil no verificado» y reescribir la descripción de I14. |
| N6 | No bloqueante | data/raw/v5/d3_referencias.csv (R04, R09, R10) | R04 no tiene URL. R09 y R10 no son citas literales, sino paráfrasis tomadas de docs/literatura.md. | Añadir la URL de R04 o marcarla como «sin URL». Marcar R09/R10 como «paráfrasis» o sustituirlas por la cita literal. |
| N7 | No bloqueante | output/v5/D3/convergencia.md, filas R01-R05 | 1) La coincidencia de B2-H2 con el BdE (R03, R04) usa los mismos insumos primarios (ECP del INE y terminadas del MIVAU): es concordancia aritmética, no confirmación independiente. 2) R01/R02 comparan la cifra C1 de 2021-2024 (ECP+EPA), mientras que R03-R05 usan B2-H2 (solo ECP), y no se declara que son dos construcciones distintas. Además, 562.692 + (240.000 − 92.000) en 2025 ≈ 710.000 > 700.934: hay una tensión interna que conviene explicar. | 1) Añadir en la explicación «mismos insumos primarios». 2) Declarar la diferencia entre las dos construcciones y explicar la tensión. |
| N8 | No bloqueante | src/v5/d2_run.py:22 → politica_territorio.md:28 | «N2 edificabilidad y N1/I13 licencias actúan sobre ese cuello de botella» es una afirmación de mecanismo en indicativo. | «se dirigen a ese cuello de botella (inferencia de mecanismo, C4)». |
| N9 | No bloqueante | output/v5/D2/politica_territorio.md (por clase) | I01, I16 y el resto de instrumentos con signo no estable o no evaluable no aparecen en D2. Con la misma rúbrica, cada clase debería listar todos los instrumentos en tres grupos: estable, no estable y no evaluable. I02/N8 aparece en la lista negativa en la clase 1 y como «signo estable» en la clase 3. | Añadir la fila «signo no estable / no evaluable» por clase y unificar el trato de I02/N8. |

## Veredicto

**REHACER**, con tres bloqueantes concretos y de corrección acotada:

1. **B1** (lenguaje prescriptivo y uso de literatura NO VERIFICADA en D2).
2. **B2** (comparabilidad «parcial» y recuento de coincidencias en D3).
3. **B3** (regla de la columna de clase en D1).

Lo demás cumple:
- reproducibilidad;
- ausencia de nombres de partidos;
- verificación de la literatura comprobada;
- capas C2 y C4 de las ayudas con los métodos A y B;
- supuesto de cobertura declarado;
- checks a cero.

Los hallazgos N1-N9 pueden corregirse en la misma pasada.
