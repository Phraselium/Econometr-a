# Documento final · Revisión, ronda 1 (2026-10-23)

## Árbitro (revisor del Banco de España): REVISAR

Resumen del veredicto: documento bien organizado y prudente; cumple las reglas de capa y reproduce completa la frase de limitación de E2-R1. Antes de difundirlo hay que corregir: (a) la cuenta de juicio experto resta de la variación nacional magnitudes que el propio documento dice que no se restan, y su lectura no se sostiene con sus intervalos; (b) grados de confianza más altos de lo que permite la evidencia; (c) la celda de tipos de interés no es coherente con su propia literatura ni con V17; (d) el resumen inglés incumple K9/K14. Todo se arregla con texto, rótulos o selección de cifras existentes.

| # | Gravedad | Hallazgo | Respuesta |
|---|---|---|---|
| 1 | Mayor | A.6 e IX.1 dicen que las filas relativas no se restan de la variación nacional; la versión 2 lo hace | A.6 e IX.1 reescritas: solo en la versión 2, como supuesto de juicio experto; V.4 cita K14-N4 y K15; referencia «parte V d» corregida |
| 2 | Mayor | «El no explicado es la mayor parte en todos los periodos» solo vale con el valor central | Reformulado: en el valor central; en 2014-2019 y 2022-2026 el rango no lo garantiza; en 2020-2022 el no explicado supera a lo observado |
| 3 | Mayor | El «intervalo del 90 %» no es estadístico (propagación de un rango uniforme de estudios) | Rotulado «rango del 90 % de la propagación de un rango de estudios, sin error típico»; regla de la magnitud descrita |
| 4 | Mayor | El resumen omite el supuesto de la cuenta | Añadido en el resumen; 1995-2007 se mantiene con su supuesto y su ventana |
| 5 | Mayor | E3: el 25 % de un estudio y los 6,9 de 69,0 pp de la cuenta no casan en el resumen; «extremo alto» mal dicho | Fila E3 explica las dos cifras; «por encima de la magnitud central» |
| 6 | Mayor | Confianza de E3 demasiado alta | Partida: sugiere (asociación regional 2000-2010); no permite concluir (magnitud en el ciclo actual) |
| 7 | Mayor | Celda de tipos incoherente (valor central en un extremo; contrafactual) | Rango de V17 sin valor central, redactado como «aplicar las semielasticidades… equivale a»; la fila E7 de la cuenta en 2022-2026 recoge la bajada |
| 8 | Mayor | Topes: mismos datos, no independientes; falta −0,023; extremo de Monràs sin efectos fijos | Reescrito: «en torno a −0,04», con las cuatro cifras y la advertencia de que no son evidencia independiente |
| 9 | Mayor | Resumen inglés da −0.038 sin frase K9 | Quitadas las cifras de la viñeta |
| 10 | Mayor | Lenguaje con contrafactual («cerrar el déficit se asociaría», «acaba en la renta», «es un freno») | Reformulado en el resumen y en V.2; en la parte IV, «equivale a 0,39 de la necesidad» |
| 11 | Mayor | Confianza asimétrica E8/E9; turismo y oferta | E9: indica (peso), no permite concluir (precio); turismo y oferta: sugiere (signo/local), es compatible con (magnitud nacional de un estudio) |
| 12 | Mayor | Ayudas: «menos con la combinación formal» oculta una discrepancia de un orden de magnitud | Las dos cifras lado a lado con la causa (composición) |
| 13 | Menor | E2-R1c «sin diferencia detectable» | «el diseño no es creíble para la cantidad (placebo de fecha)» |
| 14 | Menor | Parte I (V8, IPC) y parte V (deflactor del PIB) dan variaciones distintas desde 2022 | Frase que lo explica en la parte V |
| 15 | Menor | Componente común seleccionado al alza | Rango de las series en compra y alquiler |
| 16 | Menor | «Moderada» atribuido al Banco de España sin cifra; «no encuentran cointegración» | Quitado «moderada»; «no rechazan su ausencia (potencia baja)» |
| 17 | Menor | El resumen no cabe en dos páginas; jerga | E10-E12 en una fila; calibraciones a la columna de juicio; NO APTA y pp definidos. PDF apaisado de dos páginas |
| 18 | Menor | «Ninguna cifra cambia» omite las 9 altas | Dicho |
| 19 | Menor | «El saldo exterior aportó» incluye ajustes estadísticos | Corregido |
| 20 | Menor | Hogares 998 mil (2021-2025) frente a 1.222.836 (2021-2026) | Aclarado en la parte II |
| 21 | Editorial | Duplicados, «2,0 métodos», «la anexo», generador citado, párrafo fuera de lista, ruta de tareas | Corregidos |

## Verificador de cifras: 7 discrepancias, ninguna de valor

839 marcadores (349 ids, todos en cifras_clave); los 836 valores renderizados coinciden; tablas de impactos, erratas y pre-registros completas; las 9 filas V18-AUX-JE-* coinciden con contabilidad_ilustracion.csv y cuadran (observado − E3 − E7 = no explicado, diferencias ≤ 0,010 pp).

| # | Discrepancia | Respuesta |
|---|---|---|
| 1 | Resumen inglés da la cifra de E2-R1 sin frase K9 | Corregido (árbitro 9) |
| 2 | Anexo B remite a «4.2», que no existe | Remite a B.2 y al resumen ejecutivo |
| 3 | «Durante la vigencia (2020T4-2022T1)» con ids de periodo 2020T1-2022T2 | El id es del periodo de la cuenta; el texto dice ya que la cifra se refiere a la vigencia dentro de ese periodo |
| 4 | «capa C3s» junto a recuentos C4 de la comparación con V8 | Precisado: C3s es la descomposición de V8; los recuentos son C4 |
| 5 | «8, 30 y 39 clusters» sin id | Dato del diseño (número de comunidades y provincias de la muestra), declarado como tal |
| 6 | «cuatro cocientes», «dos series» sin id | Denominadores del diseño de la ficha GSADF (output/v7_2/gsadf/ficha_burbuja.md), citada |
| 7 | «publicación 2.0» tecleado | Marcador {{proyecto.version_publica}} |

# Ronda 2 (2026-10-23)

**Árbitro: REVISAR (revisión menor); «cuando el PDF esté regenerado y se apliquen los puntos 2 a 8, que son solo de texto, el documento puede aceptarse sin otra ronda».** De los 21 hallazgos de la ronda 1, 16 resueltos y 5 en parte o no verificables (2, 7, 17, 19, 21), cubiertos por los nuevos:

| # | Gravedad | Hallazgo nuevo | Respuesta |
|---|---|---|---|
| 1 | Mayor | El PDF del resumen era el de la ronda 1 | Regenerado (`make revision_externa_2_0`): el resumen en español ocupa dos páginas A4 apaisadas y la versión inglesa la tercera. check_final comprueba ahora que el PDF lleva las cifras del resumen vigente |
| 2 | Mayor | La celda de tipos mezcla escalas | Se separan: rango de la literatura por +100 pb y, aparte, la calibración de V17 con semielasticidades del BCE, de −5,9 % (solo compras con hipoteca) a −22,6 %; mismo texto en V.2 |
| 3 | Menor | V.4: «la mayor parte queda sin asociar» | «en el valor central» |
| 4 | Menor | Descripción de la extracción de la magnitud | Uniforme entre los extremos de los estudios que admite la regla de la cuenta (columna magnitud_centro); no es el rango de las priors |
| 5 | Menor | Razón sobrante en la comparación con González y Ortega | Sustituida por el desfase de ventanas |
| 6 | Menor | Grado de confianza aplicado a un cociente de una sola fuente (suelo) | Quitado |
| 7 | Menor | Inglés: «effect», saldo migratorio sin ajustes | Corregido |
| 8 | Editorial | C3 en las siglas, antecedente de «lo», paréntesis de E2-R1 | Corregidos |
| — | Ronda 1, 21 | «75 % de hogares … de los hogares» | Corregido |

**Verificador: 6 de 7 discrepancias resueltas; 1 abierta y 1 nueva**, ambas corregidas: el periodo de la fila de Cataluña (la cifra es de la fila 2020T1-2022T2 y se refiere a los trimestres de vigencia dentro de él) y el denominador «34 series» (17 comunidades, dos series cada una). 832 marcadores de cifra, todos con id; publicacion/documento_final y consulta/resumen_final.md idénticos al resumen generado; la frase K9 idéntica en el resumen y en B.2; el inglés sin cifras de E2-R1.

Con esto se cierra la revisión (máximo de dos rondas).
