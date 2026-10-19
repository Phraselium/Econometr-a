Análisis a posteriori (V17). Ficha de auditoría de la fila «ayudas_demanda» (D1, medida 5). Grupo regulacion_ayudas. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia.

# Medida 5 · Ayudas a la demanda (bono joven, avales)

## 1. Texto auditado

> «Ayudas a la demanda (bono joven, avales): sin evidencia de mejorar la asequibilidad. La literatura internacional muestra que parte de la ayuda acaba en el precio donde la oferta es rígida.»

La misma tesis está en el informe integral, III.8: el veredicto sobre la asequibilidad del beneficiario es «sin evidencia», porque las referencias de L5 «estudian la traslación al precio... no la asequibilidad del beneficiario».

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- **No hay evaluación en España.** No hay evaluación del Bono Alquiler Joven (RD 42/2022) ni de los avales ICO-MIVAU (2024). Búsqueda en V17 del 2026-10-19: AIReF, Banco de España, Ministerio y universidades, sin resultados. Nuestro Q7a (V16), con inferencia convencional, da −0,12 Δlog (IC −0,26 a 0,02; p = 0,074; distorsión sin medir), y los placebos de edad son del mismo orden (V16-Q7-4: −0,14 a −0,05). No distingue señal de ruido (V17-AUD-RA-AYU-Q7).
- **Ayudas a la compra donde la oferta es rígida: pueden no mejorar el acceso.** Carozzi, Hilber y Yu (2024, JUE 139, DOI 10.1016/j.jue.2023.103611; resumen) hallan que en Londres el Help to Buy subió los precios sin efecto en la obra. Según su resumen, no ayudó a los compradores en las zonas ya inasequibles. Krolage (2020, NO VERIFICADA) halla una capitalización casi completa en casas unifamiliares de Baviera. Para los avales, que facilitan la entrada con más deuda, esto apoya la prudencia.
- **La segunda frase se sostiene.** Hay traslación al precio o a la renta donde la oferta es rígida: Fack 2006, Gibbons y Manning 2006, Grislain-Letrémy y Trevien 2022, Carozzi et al. 2024.

**En contra (decisivo para las ayudas al alquiler).**
- **El argumento de III.8 es un error lógico.** El coste neto del beneficiario es la renta menos la ayuda. Si una ayuda de 1 € sube su renta θ €, su coste neto baja (1 − θ) €. Un estudio de incidencia que mide θ < 1 con diseño mide, por tanto, la mejora de asequibilidad del beneficiario. Traslación y asequibilidad del beneficiario son las dos caras de una misma identidad, no resultados distintos.
- **Estudios con diseño y θ < 1** (L5 y lecturas de V17):
  - Fack (2006, Labour Economics 13(6), DOI 10.1016/j.labeco.2006.01.001, resumen leído en V17): 78 céntimos de renta por euro de ayuda, de modo que al beneficiario le quedan 22 céntimos.
  - Gibbons y Manning (2006, JPubE 90(4-5), DOI 10.1016/j.jpubeco.2005.01.002, resumen leído en V17): entre el 60 % y dos tercios de la incidencia recae en el arrendador.
  - Collinson y Ganong (2018): 0,46-0,47.
  - Kangasharju (2010): 0,6-0,7.
  - Viren (2013): un tercio.
  - Hyslop y Rea (2019): 0,36.
  - Eerola et al. (2026, JPubE): 0,036 (e.e. 0,028).
- **Lo que retiene el beneficiario.** La mediana de los siete estudios es el 54 % de la ayuda, con un rango del 22 % (Fack) al 96 % (Eerola et al.) (V17-AUD-RA-AYU-RETIENE-MEDIANA). Aplicado mecánicamente al bono de 250 €/mes son unos 135 €/mes, entre 55 y 241 (V17-AUD-RA-AYU-BONO-RETIENE). Es un juicio experto, no una estimación sobre España.
- **Con la propia regla de III.1, el veredicto sería «prometedora».** «Prometedora» exige al menos un estudio con diseño en el sentido del objetivo, aunque se haya leído solo en resumen. Hay siete, y todos coinciden en el signo de la asequibilidad del beneficiario (θ < 1). Solo una especificación DDD de Fack (2005) supera 1, con error grande.
- **El propio proyecto lo publica.** La 1.0 da el signo [C2] «el beneficiario paga igual o menos como grupo» (D1-V1). publicacion/lo_que_sabemos.md añade que la ayuda reduce el precio neto que paga el beneficiario: su esfuerzo varía un −5,3 % [C4]. La frase de D1 contradice ambas cosas sin decirlo.
- **Lo que sí empeora: el resto de inquilinos.** Esto falta en la frase de D1.
  - Susin (2002): el alquiler de los no perceptores de bajos ingresos sube un 16 %.
  - Grislain-Letrémy y Trevien (2022, Banque de France WP 886, resumen leído en V17): las ayudas elevan a largo plazo la renta también de quien no las recibe, con más viviendas en alquiler.
  - Gibbons y Manning: sin efecto en no perceptores.

## 3. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_regulacion_ayudas.py.
1. **Traslación medida y su implicación para el beneficiario.** Tabla de θ por estudio, un valor central cada uno:

| Estudio | θ | 1 − θ (beneficiario) |
|---|---|---|
| Fack (2006) | 0,78 | 0,22 |
| Kangasharju (2010) | 0,65 | 0,35 |
| Gibbons y Manning (2006) | 0,63 | 0,37 |
| Collinson y Ganong (2018) | 0,46 | 0,54 |
| Hyslop y Rea (2019) | 0,36 | 0,64 |
| Viren (2013) | 0,33 | 0,67 |
| Eerola et al. (2026) | 0,036 | 0,96 |

2. **Implicación para el resto de inquilinos:** signo al alza en EE. UU. y Francia, nulo en el Reino Unido; sin magnitud comparable en lo leído.
3. **Bono y avales en España:** sin evaluación. Q7a no permite concluir.
4. **Q7 de V16:** véase el apartado 2. No se usa para el veredicto.

## 4. Literatura

| Referencia | Estado | Lectura |
|---|---|---|
| Fack (2006), Labour Economics 13(6), 747-771, 10.1016/j.labeco.2006.01.001 | VERIFICADA (Crossref, V17; cuartil no verificado) | resumen (IDEAS) |
| Fack (2005), Économie et Statistique 381-382 | NO VERIFICADA (sin DOI) | texto parcial, tablas 3-7 (L5) |
| Gibbons y Manning (2006), JPubE 90(4-5), 799-822, 10.1016/j.jpubeco.2005.01.002 | VERIFICADA (Crossref, V17; en L5 figuraba sin DOI) | resumen y texto parcial del documento de trabajo (L5) |
| Grislain-Letrémy y Trevien (2022), Banque de France WP 886 | NO VERIFICADA (sin DOI localizado) | resumen (página del Banque de France, consulta del 2026-10-19) |
| Carozzi, Hilber y Yu (2024), JUE 139, 103611, 10.1016/j.jue.2023.103611 | VERIFICADA | resumen (LSE Research Online) |
| Susin (2002); Collinson y Ganong (2018); Viren (2013); Hyslop y Rea (2019); Eerola et al. (2026) | VERIFICADAS (L5) | resumen o texto parcial (L5) |
| Kangasharju (2010); Krolage (2020) | NO VERIFICADAS (sin DOI) | resumen o introducción (L5) |

## 5. Veredicto

**Incorrecta** en su primera frase, en lo que toca a las ayudas al alquiler, como el bono joven: hay evidencia con diseño, en otros países, de que el beneficiario mejora su asequibilidad en una fracción de la ayuda. Para los avales y las ayudas a la compra en mercados rígidos, «sin evidencia» es defendible y hay incluso indicios en contra (Carozzi et al.). La segunda frase se sostiene, pero omite que la traslación puede encarecer el alquiler de los no beneficiarios.

## 6. Texto corregido y confianza

> «Ayudas a la demanda. Ayudas al alquiler (como el bono joven): en otros países, el beneficiario retiene una parte de la ayuda, entre una quinta parte y casi toda según el estudio, y el resto se traslada a la renta, sobre todo donde la oferta es rígida; la traslación puede subir también el alquiler de quien no recibe la ayuda. Ayudas a la compra y avales: donde la oferta es rígida, la ayuda se capitaliza en el precio y puede no mejorar el acceso. En España no hay evaluación del bono ni de los avales.»

Confianza:
- mejora parcial de la asequibilidad del beneficiario del alquiler: **la evidencia sugiere** (signo coincidente en siete estudios con diseño, magnitud muy dispersa y ninguno en España);
- efecto sobre los no beneficiarios: **la evidencia es compatible con** una subida;
- avales y ayudas a la compra en España: **la evidencia no permite concluir**.

## 7. PARADA

La auditoría muestra que **«sin evidencia de mejorar la asequibilidad» es falsa para las ayudas al alquiler**, y no solo matizable. Lo es en D1 (medida 5) y en el veredicto de publicacion/informe_integral/informe_integral.md, III.8 («Asequibilidad del beneficiario ... sin evidencia»).

**Prueba:**
1. La identidad del coste neto, coste neto = renta − ayuda, convierte toda estimación de traslación θ < 1 en una mejora de (1 − θ) para el beneficiario.
2. Siete estudios con diseño dan θ < 1, con una mediana de 0,46, y Fack (2006), verificado en Crossref, da 0,78. El beneficiario retiene, por tanto, el 22 %.
3. Con la regla de umbral de III.1, el veredicto sobre la asequibilidad del beneficiario de las ayudas al alquiler sería «prometedora», no «sin evidencia».
4. La propia 1.0 publica el signo [C2] de que el beneficiario paga igual o menos.

Para los avales ICO, la afirmación no es falsa.

No se corrige ningún fichero publicado: decide el autor.
