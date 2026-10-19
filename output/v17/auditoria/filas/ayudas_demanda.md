Análisis a posteriori (V17). Ficha de auditoría de la fila «ayudas_demanda» (D1, medida 5). Grupo regulacion_ayudas. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia. Versión tras la ronda 1 del abogado del diablo (secciones 8 y 9).

# Medida 5 · Ayudas a la demanda (bono joven, avales)

## 1. Texto auditado

> «Ayudas a la demanda (bono joven, avales): sin evidencia de mejorar la asequibilidad. La literatura internacional muestra que parte de la ayuda acaba en el precio donde la oferta es rígida.»

**Estado tras la parada P1.** El autor decidió el 2026-10-19 (ERRATA.md) que III.8 diga:
- (i) para la asequibilidad del beneficiario de las ayudas al alquiler, «prometedora», con una traslación mediana del 46 % (rango del 3,6 % al 78 %);
- (ii) para la asequibilidad general del alquiler, «evidencia en contra».

Esta ficha no toca nada publicado. La sección 9 da la recomendación razonada sobre esa redacción.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor de la frase original.**
- **No hay evaluación española.** No se ha evaluado el Bono Alquiler Joven (RD 42/2022) ni los avales ICO-MIVAU (búsqueda del 2026-10-19).
- **Q7a (V16) no distingue señal de ruido.** Da −0,12 Δlog (IC −0,26 a 0,02; p = 0,074; distorsión sin medir), con placebos del mismo orden (V17-AUD-RA-AYU-Q7).
- **Compra donde la oferta es rígida: hay indicios en contra.**
  - Carozzi, Hilber y Yu (2024; resumen): en Londres, el Help to Buy subió los precios sin efecto en la obra y no ayudó a los compradores en las zonas inasequibles.
  - Krolage (2020, NO VERIFICADA): capitalización casi completa en casas de Baviera.
- **Bono joven: la duración puede anular la ganancia.** El bono dura como máximo 24 meses (RD 42/2022, art. 12) y el contrato, al menos 5 años (LAU, art. 9). Si el arrendador incorpora la traslación θ·250 € a la renta inicial y la mantiene todo el contrato, el perceptor pierde en el conjunto del contrato cuando θ > 24/60 = 0,40. Con la θ mediana de 0,46, la pérdida sería de unos −900 € por contrato. El rango va de −5.700 € con θ = 0,78 a +5.460 € con θ = 0,036 (V17-AUD-RA-AYU-BONO-DURACION). Es un escenario, no una estimación.

**En contra de la frase original (ayudas al alquiler).**
- **La identidad del coste neto.** El coste neto del perceptor es la renta menos la ayuda. Con una traslación θ < 1, mientras dure la ayuda y a calidad constante, el perceptor gana (1 − θ) por euro.
- **Lo que dice la tabla completa** (sección 3):
  - de ocho estudios con diseño, siete tienen una θ central menor que 1;
  - el octavo, Grislain-Letrémy y Trevien, tiene una θ implícita de 0,96 y no se puede distinguir de 1;
  - tres estimaciones contrastan θ < 1 con p < 0,05: Eerola et al. y dos de Fack (2005) con controles.
- **Lo que no recoge la frase original: el resto de inquilinos.**
  - Susin (2002, versión de trabajo leída completa): +16 % en el alquiler de los no perceptores de renta baja.
  - Grislain-Letrémy y Trevien (2022, leído completo): +5,5 % (0,055; e.e. 0,025) en los no perceptores.
  - Gibbons y Manning (versión de 2003, leída completa): sin efecto detectable, con poca potencia.
  - Fuente: docs/v17/referencias/no_beneficiarios.md.

## 3. Tabla completa de θ (traslación al alquiler de los perceptores)

θ son los euros de alquiler por euro de ayuda, o la fracción de la incidencia que cae sobre el arrendador. Se incluyen todas las filas de L5_ayudas_demanda_efectos.csv con traslación a perceptores, más tres añadidas: Fack (2006) y Gibbons y Manning (2006), por su resumen publicado, y la θ implícita de Grislain-Letrémy y Trevien (2022), calculada por el auditor. Se excluyen Kangasharju en el sector municipal (renta regulada, θ = 0) y las filas de precio de compra. Script: tabla_theta().

| Estudio (fuente) | θ | e.e. o rango | Variación | Horizonte | Calidad | ¿Contrasta θ < 1? | Principal |
|---|---|---|---|---|---|---|---|
| Fack (2005), tabla 3, DD sin controles | 0,76 | 0,26 | aumento (extensión de los 90) | medio | no ajustada | no | — |
| Fack (2005), tabla 3, DD con controles | 0,39 | 0,24 | ídem | medio | no ajustada | sí (p < 0,05) | — |
| Fack (2005), tabla 3, DDD sin controles | **1,42** | 0,63 | ídem | largo (1984-2002) | no ajustada | no | — |
| Fack (2005), tabla 3, DDD con controles | **1,02** | 0,52 | ídem | largo | no ajustada | no | — |
| Fack (2005), tabla 7, DD sin controles | 0,62 | 0,33 | ídem | medio | a calidad constante | no | — |
| Fack (2005), tabla 7, DD con controles | 0,20 | 0,33 | ídem | medio | a calidad constante | sí (p < 0,05) | — |
| Fack (2005), tabla 7, DDD sin controles | **1,45** | 0,76 | ídem | largo | a calidad constante | no | — |
| Fack (2005), tabla 7, DDD con controles | 0,92 | 0,64 | ídem | largo | a calidad constante | no | — |
| Fack (2006), resumen | 0,78 | — | ídem (nuevos perceptores) | medio | no ajustada | sin e.e. | **sí** |
| Gibbons y Manning (2006), resumen | 0,63 | 0,60-0,67 | **recorte** a nuevos solicitantes | corto | no ajustada | sin e.e. (en la versión de 2003 la caída desaparece con tendencias por antigüedad) | **sí** |
| Collinson y Ganong (2018), revisión de 2005 | 0,46 | — | **techo de cupón** | medio (6 años) | incluye calidad (+0,05 hedónica) | sin e.e. | **sí** |
| Collinson y Ganong (2018), cambio de 2001 | 0,47 | — | techo de cupón | medio | ídem | sin e.e. | — |
| Kangasharju (2010), sector privado | 0,65 | 0,60-0,70 | aumento (reforma de 2002) | medio | no ajustada | sin e.e. | **sí** |
| Viren (2013) | 0,33 | hasta 0,50 | variación general | largo | no ajustada | sin e.e. | **sí** |
| Hyslop y Rea (2019) | 0,36 | — | aumento zonal (frontera) | corto (segundo año) | no ajustada | sin e.e. | **sí** |
| Eerola et al. (2026) | 0,036 | 0,028 | aumento (reforma de 2015) | medio (5 años) | no ajustada | sí (p < 0,05) | **sí** |
| Grislain-Letrémy y Trevien (2022), θ implícita | 0,96 | 0,33 (de 0,018 log); rango 0,59-1,57 por el diferencial de 15-40 € | **diferencial de cuantía** por zona | largo (2000-2016) | sin efecto en calidad (autores) | no | **sí** |

**Cómo se calcula la θ implícita de Grislain-Letrémy y Trevien.** El alquiler de los perceptores sube 0,052 log sobre una renta media de 454 €, unos 23,6 €. Se divide por el diferencial de ayuda de su ejemplo (22-27 €; rango 15-40 €).

**Medianas, un valor por estudio** (V17-AUD-RA-AYU-TRASLACION-MEDIANA y -SENS):

| Composición | θ mediana | Parte que retiene el perceptor |
|---|---|---|
| Siete estudios (los de ERRATA P1) | **46 %** (3,6-78 %) | 54 % |
| Ocho estudios, con Grislain-Letrémy y Trevien | 54,7 % | 45 % |
| Siete, sin Collinson y Ganong | 49,7 % | 50 % |
| Ocho, sin Collinson y Ganong | 63,3 % | 37 % |
| Siete, sin Gibbons y Manning | 41,0 % | 59 % |
| Solo aumentos de ayuda (Fack, Kangasharju, Hyslop y Rea, Eerola, Grislain-Letrémy y Trevien) | 65,0 % | 35 % |
| Corto plazo (Gibbons y Manning, Hyslop y Rea) | 49,7 % | 50 % |
| Medio y largo plazo | 55,5 % | 45 % |
| A calidad constante (solo Fack 2005, tabla 7, cuatro columnas) | 0,77 | 23 % |

**Lectura.** El signo de la ganancia del perceptor (θ < 1) aparece en 7 de 8 estudios por su valor central. La magnitud es muy dispersa: la mediana va del 41 % al 65 % según la composición. El rango completo va de casi nada (Eerola) a casi todo (Grislain-Letrémy y Trevien; Fack DDD). Solo cinco estimaciones tienen error estándar, y solo tres rechazan θ = 1.

**¿La ganancia es menor donde la oferta es más rígida?** Es compatible con la evidencia:
- **Entre estudios.** Las tres θ más altas (Grislain-Letrémy y Trevien 0,96, Fack 0,78, Gibbons y Manning 0,63) son de estudios cuyos autores describen una oferta privada poco elástica. La más baja (Eerola et al.) la atribuyen sus autores a que los perceptores no cambiaron de vivienda, no a una oferta elástica.
- **Dentro de un mismo estudio.** Eriksen y Ross (2015) hallan las mayores subidas en ciudades con oferta poco sensible. Grislain-Letrémy y Trevien ven que el efecto deja de ser significativo en las viviendas de 1-2 habitaciones, donde la oferta respondió.
- **Lo que no se sostiene.** «La ganancia es menor donde más se usa la ayuda» no tiene base: ningún estudio relaciona θ con la intensidad de uso. Susin relaciona la intensidad de uso con la subida para los NO perceptores, que es el resultado (ii).

## 4. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_regulacion_ayudas.py (tabla_theta, ayudas).
1. **Traslación medida e implicación para el perceptor:** tabla y medianas de la sección 3.
2. **Implicación para el resto de inquilinos:** Susin (+16 %, tercil bajo; sección cruzada no significativa al 5 %, primeras diferencias sí) y Grislain-Letrémy y Trevien (+5,5 %) frente a Gibbons y Manning (nulo, con poca potencia). Ninguno es español.
3. **Bono y avales en España:**
   - **Condiciones del bono** (RD 42/2022, comprobadas en el BOE el 2026-10-19): 250 €/mes (art. 11); 24 meses como máximo (art. 12); alquiler ≤ 600 €, ampliable a 900 € (art. 8); edad ≤ 35 años y renta ≤ 3 IPREM (art. 6). La duración condiciona la identidad (sección 2).
   - **Avales ICO:** sin evaluación.

## 5. Literatura

| Referencia | Estado | Lectura |
|---|---|---|
| Fack (2006), Labour Economics 13(6), 10.1016/j.labeco.2006.01.001 | VERIFICADA (Crossref) | resumen |
| Fack (2005), Économie et Statistique 381-382 | NO VERIFICADA | texto parcial, tablas 3-7 (L5) |
| Gibbons y Manning (2006), JPubE 90(4-5), 10.1016/j.jpubeco.2005.01.002 | VERIFICADA (Crossref) | resumen publicado; versión de trabajo de 2003 leída completa (no_beneficiarios.md) |
| Grislain-Letrémy y Trevien (2022), Banque de France WP 886 | NO VERIFICADA (sin DOI) | texto completo (no_beneficiarios.md) |
| Susin (2002), JPubE 83(1), 10.1016/S0047-2727(01)00081-0 | VERIFICADA | versión de trabajo de 1999 leída completa; la publicada no se ha leído |
| Collinson y Ganong (2018); Viren (2013); Hyslop y Rea (2019); Eerola et al. (2026); Eriksen y Ross (2015) | VERIFICADAS (L5) | resumen o texto parcial |
| Kangasharju (2010); Krolage (2020) | NO VERIFICADAS | resumen o introducción |
| Carozzi, Hilber y Yu (2024), JUE 139, 10.1016/j.jue.2023.103611 | VERIFICADA | resumen |
| RD 42/2022 (BOE-A-2022-802); Ley 29/1994 (LAU), art. 9 | normas | consulta del 2026-10-19 |

## 6. Veredicto

**Incorrecta** en la primera frase, para las ayudas al alquiler, con dos condiciones de la identidad que hay que declarar:
- la calidad constante;
- que la subida de renta no dure más que la ayuda (en el bono joven, 24 meses frente a contratos de 5 años).

Para los avales y la compra en mercados rígidos, «sin evidencia» es defendible. La segunda frase se sostiene, pero omite a los no perceptores.

## 7. Texto corregido y confianza

> «Ayudas a la demanda. Ayudas al alquiler: en otros países el perceptor paga menos de lo que recibe de ayuda, porque solo una parte de la ayuda acaba en la renta (en mediana, en torno a la mitad, con estudios entre casi nada y casi toda), y menos donde la oferta es rígida; pero la ayuda puede subir el alquiler de quien no la recibe. En el bono joven, que dura dos años, la ganancia depende de que la subida de renta no se quede en el contrato cuando la ayuda acaba. Ayudas a la compra y avales: donde la oferta es rígida la ayuda se capitaliza en el precio y puede no mejorar el acceso. En España no hay evaluación del bono ni de los avales.»

**Confianza:**
- ganancia parcial del perceptor de ayudas al alquiler: **la evidencia sugiere**;
- subida para no perceptores: **la evidencia sugiere** (dos estudios leídos completos de tres);
- bono joven en todo el contrato, y avales: **la evidencia no permite concluir**.

## 8. Respuesta a la ronda 1

| Punto del abogado del diablo | Respuesta |
|---|---|
| «Solo una especificación DDD de Fack (2005) supera 1» | **Corregido.** Son tres: 1,42 y 1,02 (tabla 3) y 1,45 (tabla 7). |
| Tabla completa de θ | **Aplicado** (sección 3), con error estándar o rango, tipo de estimando, calidad, contraste de θ < 1 y la θ implícita de Grislain-Letrémy y Trevien. |
| Medianas con y sin Collinson y Ganong y por estimando | **Aplicado.** |
| Apoyo circular de la rejilla C2 | **Retirado.** El signo C2 de la 1.0 sale de la misma literatura y no es un apoyo independiente; ya no se usa como argumento. |
| Tratar igual a Gibbons y Manning en (i) y (ii) | **Aplicado.** En la versión de 2003 su caída en perceptores desaparece con tendencias por antigüedad, y su nulo en no perceptores tiene poca potencia. Si cuenta en (i), cuenta en (ii) como nulo. Si se descarta, se descarta en ambos: la θ mediana pasa al 41 % y (ii) queda con 2 de 2 estudios. Ninguna de las dos opciones cambia las etiquetas (sección 9). |
| Condicionar la identidad | **Aplicado.** La identidad exige calidad constante (Collinson y Ganong incluyen calidad; Fack a calidad constante da 0,77 de mediana) y que la traslación no dure más que la ayuda: RD 42/2022, 24 meses, frente a la LAU, 5 años; umbral θ > 0,40. |
| «La ganancia es menor donde más se usa» | **Evaluado.** «Donde la oferta es más rígida» es compatible con la evidencia (entre estudios y dentro de dos estudios). «Donde más se usa» no tiene base y debe borrarse o sustituirse. |

## 9. Para el autor: III.8

Esta sección es una recomendación. No se ha aplicado ningún cambio.

**Regla de III.1, literal:**
- **«Eficacia probada»:** al menos dos estudios con diseño, leídos completos, con DOI verificado, que coinciden en el signo.
- **«Prometedora»:** al menos un estudio con diseño en el sentido del objetivo, aunque se haya leído en resumen o discrepe en parte.
- **«Sin evidencia»:** no hay estudio con diseño, o los que hay discrepan en el signo.
- **«Evidencia en contra»:** al menos dos estudios con diseño, leídos completos, en sentido contrario al objetivo declarado.

### (i) Asequibilidad del perceptor de ayudas al alquiler

**Etiqueta: «prometedora»**, que es la decidida.
- **No llega a «eficacia probada».** De los estudios leídos completos, Gibbons y Manning (2003) tiene DOI verificado solo para la versión publicada, que no se ha leído, y su efecto en perceptores no es robusto. Grislain-Letrémy y Trevien no tiene DOI y su θ (0,96) no se distingue de 1.
- **Sí llega a «prometedora».** Siete de ocho estudios con diseño dan θ < 1, y Eerola et al. y Fack (2005, con controles) lo contrastan.

**Cifra principal recomendada.** «Traslación mediana en torno a la mitad (46 % con siete estudios; entre el 41 % y el 65 % según qué estudios se incluyan), con estudios que van de casi nada al 100 %». El rango «3,6-78 %» publicado omite:
- la θ implícita de Grislain-Letrémy y Trevien (≈ 0,96), leída completa;
- las tres especificaciones DDD de Fack por encima de 1.

**Frases que habría que cambiar:**
1. «Así que la ganancia es menor donde más se usa la ayuda» → «la ganancia es menor donde la oferta es más rígida (Fack, 2006; Grislain-Letrémy y Trevien, 2022; Eriksen y Ross, 2015)».
2. Añadir las dos condiciones de la identidad: calidad constante y duración. Para el Bono Alquiler Joven, dos años de ayuda frente a contratos de cinco: si la subida se queda en la renta, el perceptor pierde con traslaciones superiores al 40 %.
3. «Rango del 3,6 % al 78 %» → «del 3,6 % a cerca del 100 %».

### (ii) Asequibilidad general del alquiler

**Etiqueta: «evidencia en contra» es una aplicación literal defendible**, con tres condiciones que habría que escribir:
- (a) **No es el objetivo declarado.** III.8 declara como objetivo la asequibilidad del perceptor. La etiqueta se refiere a un resultado distinto, la renta de los no perceptores y del conjunto de inquilinos de renta baja, y el texto debe nombrarlo así para no confundir.
- (b) **Los dos estudios cumplen la regla, con límites.** Susin y Grislain-Letrémy y Trevien están leídos completos en su versión de trabajo o abierta: Susin con DOI verificado de la versión publicada no leída; Grislain-Letrémy y Trevien sin DOI. La regla de «evidencia en contra» no exige DOI de forma literal, a diferencia de «eficacia probada»; por coherencia convendría decirlo.
- (c) **Hay un tercer estudio leído completo que no halla efecto.** Gibbons y Manning da un nulo con poca potencia. No es un signo contrario, así que no activa «sin evidencia», pero debe citarse.

**La magnitud apoya la etiqueta.** En los dos estudios, la subida para el conjunto de inquilinos de renta baja supera la ayuda:
- Susin: 8.200 millones de dólares de más alquiler para no perceptores frente a 5.800 millones de ayuda;
- Grislain-Letrémy y Trevien: +23,6 € para todos los inquilinos de la zona frente a 22-27 € de ayuda para quien la cobra (hasta el 44 % de los inquilinos privados, según los autores).

**Cifra principal recomendada.** «+16 % en EE. UU. (tercil bajo, 1974-1993) y +5,5 % en Francia (2000-2016) en el alquiler de no perceptores; sin efecto detectable en el Reino Unido (poca potencia)».

**Frase que habría que cambiar.** «La parte trasladada sube el alquiler de los no beneficiarios» → «la ayuda se asocia con alquileres más altos también para quienes no la reciben (EE. UU. y Francia; en el Reino Unido no se detecta)». En Grislain-Letrémy y Trevien la subida es la misma para perceptores y no perceptores: no es «la parte trasladada».

## 10. Parada

La parada P1 (D1, medida 5, e informe integral, III.8) la resolvió el autor el 2026-10-19 (ERRATA.md). No hay parada nueva. Las recomendaciones de la sección 9 son de redacción y de rango; ninguna convierte en falsa la decisión tomada.
