Análisis a posteriori (V17). Ficha de auditoría de la fila «inmigracion» (D1, discurso político). Grupo demanda_precios. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia. Ids nuevos: V17-AUD-DP-INM-* (output/v17/auditoria/demanda_precios_hechos.json); se usan además los V17-D3-* de output/v17/d3/hechos.json.

# «La culpa es de la inmigración»

## 1. Texto auditado

> «La culpa es de la inmigración»: correlación frágil; la literatura no tiene un signo único. La población crece y eso empuja la demanda, pero atribuirlo a un grupo concreto no tiene base.

La frase mezcla dos afirmaciones que hay que separar:
- **Contable:** «la demanda nueva procede mayoritariamente de la inmigración». Es una pregunta de cuentas: de dónde salen los hogares nuevos.
- **Causal:** «la inmigración sube el precio o el alquiler, o lo sube más que otra demanda equivalente». Es una pregunta de efectos y necesita un diseño.

La palabra «culpa» no se evalúa: es un juicio moral, no una afirmación empírica. Se evalúa el papel de la inmigración en la demanda y en los precios.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor (de la frase auditada).**
- **Nuestras estimaciones son frágiles.**
  - H4 (V15, shift-share): 0,31 % de alquiler por punto de población extranjera; en la lectura convencional, p = 0,26 e IC 95 % de −1,04 a 0,60 (tamaño real 0,5 %).
  - Q3-b (V16): 0,0091 log por DT con p = 2,6e-13 (tamaño real 9,6 %), pero el placebo del periodo anterior da 0,0051, del mismo orden. Es una pretendencia, no un efecto.
  - El F efectivo del instrumento por orígenes es de 2,8-3,4 (V9).
  - (output/v17/lectura_bde/tabla_comparativa.md; informe integral, VII.4.)
- **Hay signos negativos en la literatura.**
  - Sá (2015, Reino Unido) halla un efecto negativo en precio a escala de área local (autoridades locales), por la salida de nativos de renta alta, concentrado donde los inmigrantes tienen menos estudios.
  - Torres-Téllez y Montero-Soler (2023, 50 provincias, 2001-2019): durante la burbuja la inmigración elevó el precio hasta un 2,5 %, y el retorno posterior lo redujo un 1,12 %, con un saldo neto negativo en el periodo. La llegada de 2010-2019 explica un +5,9 % en el alquiler. Es España y escala provincial, con signo que cambia según la fase (docs/v15/literatura/P4_inmigracion.md; DOI 10.37230/CyTET.2023.215.3, visto en la revista).
  - Saiz y Wachter (2011) y Accetturo et al. (2014) hallan una revalorización más lenta en los barrios que reciben inmigrantes.

**En contra.**
- **La contabilidad no es frágil.**
  - De 2015 a 2025 la población creció en 3.170.654 personas con un saldo vegetativo de −896.778. El residuo migratorio es el 128 % del crecimiento (V17-D3-RESIDUO-PESO).
  - Los nacidos en el extranjero aumentaron en 4.120.690 y los nacidos en España disminuyeron en 975.687 (V17-D3-NACIDOS-*).
  - El aumento de hogares de 2021-2026 fue de 1.222.836. De él, 858.274 vienen del tamaño de la población, y entre 724.785 y 858.274 corresponden a nacidos en el extranjero, si forman hogares como el resto (V17-D3-HOGARES-*).
- **La demanda nueva de alquiler es aún más concentrada.** En el Censo 2021:
  - alquila el 38,3 % de los hogares cuya persona de mayor edad nació fuera, frente al 12,2 % de los nacidos en España; y el 45,5 % de los llegados en 2016-2021;
  - los nacidos fuera son el 15,0 % de los hogares y el 35,6 % de los hogares en alquiler (V17-AUD-DP-INM-CUOTA-ALQUILER-EXTR);
  - aplicando esas tasas, el aumento de hogares de 2021-2026 atribuido a nacidos fuera supone entre 277.730 y 390.506 hogares de alquiler (V17-AUD-DP-INM-ALQUILER-NUEVO-CONTABLE; contabilidad, no efecto).
- **La literatura con diseño creíble a escala regional sí tiene un signo dominante, y es positivo.**
  - Larkin et al. (2019; metaanálisis de 474 estimaciones de 14 países): la inmigración eleva los precios, y más a escala provincial o estatal que de ciudad.
  - Saiz (2007): +1 % de población por inmigración → alquiler y valor ≈ +1 %.
  - En España, González y Ortega (2013): 2000-2010, provincias, IV por enclaves y accesibilidad.
    - La inmigración elevó la población en edad de trabajar ≈ 1,5 % al año, el precio entre un 1,5 % y un 2,3 % al año y las viviendas un 1,2-1,5 % al año.
    - Salvedad (docs/v17/referencias/d2_versiones.md): la versión de Wiley no se leyó; las cifras proceden de resúmenes. La versión IZA de 2009 (1998-2008) atribuye un tercio; la publicada (2000-2010), un cuarto.
    - Explica en torno a una cuarta parte de la subida de precios y la mitad de la construcción del periodo.
    - La elasticidad implícita es de ≈ 1,0-1,5 (V17-AUD-DP-INM-GO-ELASTICIDAD).
  - Sanchis-Guarner (2023, provincias 2001-2012): +3,3 % de precio por punto de tasa de inmigración.
  - Los signos negativos aparecen DENTRO de las ciudades (redistribución entre barrios), no en el agregado.

## 3. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_demanda_precios.py (sin red, SEED 20261010, sin muestra sellada). Datos: output/v17/d3/.

**3.1 Proporción del crecimiento que viene de la migración neta.**
- **Población.** 128 % del crecimiento de 2015-2025 en el residuo migratorio. Saldo exterior oficial: 3.757.591 (EVR y EMCR 2015-2024).
- **Hogares.** La parte del componente población de 2021-2026 que corresponde a nacidos fuera es del 84-100 %. Por el lado del parque, el envejecimiento suma 473.045 hogares, y el componente edad no depende del origen.
- **Lectura.** Sin la migración neta, la población habría bajado. Los hogares habrían crecido solo por envejecimiento y por el tamaño medio. Es contabilidad: no dice qué habría pasado con los precios.

**3.2 Tenencia por origen** (Censo 2021, muestra del 10 %, persona de mayor edad):

| Origen | Propiedad | Alquiler |
|---|---|---|
| Nacido en España | 80,0 % | 12,2 % |
| Nacido en el extranjero | 49,7 % | 38,3 % |
| Llegada 2016-2021 | 40,8 % | 45,5 % |

**3.3 González y Ortega (2013) frente a H4 y Q3** (lectura convencional, output/v17/lectura_bde/v15_v16_micro/inferencia.csv):

| Estimación | Medida | Punto | Inferencia convencional | Tamaño real |
|---|---|---|---|---|
| González y Ortega (2013) | precio, % por 1 % de población | ≈ 1,0-1,5 (cociente del resumen) | IV, significativa según los autores | — |
| Q3-c1-AKM0 (V16) | log del valor tasado por punto de población extranjera | 0,012 (≈ 1,2 %) | p = 0,33 | 1,1 % |
| H4-AKM0 (V15) | % de alquiler por punto de población extranjera | 0,31 | p = 0,26; IC −1,04 a 0,60 | 0,5 % |
| Q3-c2-AKM0 (V16) | log de compraventas por punto | −0,028 | p = 0,077 | 1,1 % |
| Q3-b (V16) | Δlog SERPAVI por DT de la cuota | 0,0091 | p = 2,6e-13, con pretendencia del mismo orden | 9,6 % |

**Lectura.**
- **El precio.** El punto de Q3-c1 coincide en magnitud con González y Ortega, pero es impreciso. Nuestros datos son compatibles con su elasticidad y no la contradicen.
- **El alquiler (H4).** El IC excluye un efecto de +1 % por punto, como el de Saiz (2007), en el IPC de alquiler de contratos vigentes. La medida y el periodo son distintos, y el instrumento es débil.
- **Medidas distintas.** Las unidades no son idénticas: punto de cuota frente a un 1 % de población. La comparación es de orden de magnitud.

**3.4 Banco de España.**
- DO 2432 da la contabilidad de 2014-2022: nacidos en España −1,4 %, extranjeros +4,5 %, total +3,1 %.
- DO 2433, nota 7: la población nacida en España disminuye en unos 700.000 desde 2016.
- No hay estimación causal del Banco de España sobre inmigración y precios (docs/v17/referencias/bde_bce_documentos.md, «lo que no se encontró»).
- El Boletín 2025/T2 (artículo 8, solo resumen) atribuye los flujos a factores de atracción del país receptor: empleo, salarios y políticas de residencia.

## 4. Literatura

| Referencia | Estado | Lectura |
|---|---|---|
| González y Ortega (2013), J. Regional Science 53(1), 37-59, DOI 10.1111/jors.12010 | VERIFICADA (DOI y metadatos comprobados en api.crossref.org el 2026-10-19: título, autores, revista, volumen 53(1), pp. 37-59; también en docs/v15/literatura/crossref_cache.json vía P4; cuartil no verificado). Contenido: solo resúmenes secundarios (la versión de Wiley no se leyó) | resumen (Crossref). Corrige D2: la versión publicada cubre 2000-2010 y dice «una cuarta parte» del precio; «un tercio» es de la versión IZA 2009 |
| Saiz (2007), JUE 61(2), DOI 10.1016/j.jue.2006.07.004 | VERIFICADA | resumen |
| Larkin et al. (2019), J. Housing Economics 46, DOI 10.1016/j.jhe.2019.04.002 | VERIFICADA | resumen |
| Sá (2015), Economic Journal 125(587), DOI 10.1111/ecoj.12158 | VERIFICADA | resumen |
| Torres-Téllez y Montero-Soler (2023), CyTET 55(215), 47-60, DOI 10.37230/CyTET.2023.215.3 | VERIFICADA (Crossref, 2026-10-19) | resumen (P4) |
| Sanchis-Guarner (2023), RSUE 100, DOI 10.1016/j.regsciurbeco.2023.103893 | VERIFICADA (V15) | resumen y extracto (docs/v15/literatura/P4_inmigracion.md) |
| Accetturo et al. (2014), RSUE 45, DOI 10.1016/j.regsciurbeco.2014.01.001; Saiz y Wachter (2011), AEJ: Policy 3(2), DOI 10.1257/pol.3.2.169 | VERIFICADA (V15) | resumen |
| BdE DO 2432 (DOI 10.53479/37872) y DO 2433 (DOI 10.53479/37873) | VERIFICADA (Crossref) | parcial (páginas en docs/v17/referencias/) |

## 5. Veredicto

**Engañosa.** «Lo» se lee como la culpa, es decir, el efecto. Con esa lectura, la frase mezcla una parte defendible (no hay base para un efecto distinto por origen) con dos omisiones: la contabilidad y el signo dominante de la literatura a escala regional.
- «Correlación frágil» se sostiene para nuestras estimaciones.
- «La literatura no tiene un signo único» es engañosa. A la escala que importa para el agregado (provincias, ciudades, países), la literatura con diseño, incluida la española, halla un efecto positivo en precio. Los signos negativos son de redistribución dentro de la ciudad.
- «Atribuirlo a un grupo concreto no tiene base» sería falsa si se refiriera a la contabilidad. Más del 100 % del crecimiento de la población de 2015-2025 procede de la migración neta. La mayor parte del aumento de hogares de 2021-2026 corresponde a nacidos en el extranjero, que además alquilan en una proporción tres veces mayor (38,3 % frente a 12,2 %). Lo que no tiene base es otra afirmación, que la frase no separa: que un hogar inmigrante presione más que un hogar equivalente de otro origen.

## 6. Texto corregido y confianza

> «La culpa es de la inmigración»: hay que separar dos preguntas. Contabilidad: la población crece por la inmigración, porque el saldo vegetativo es negativo desde 2017. De 2021 a 2026, la mayor parte de los hogares nuevos parece corresponder a nacidos en el extranjero, que alquilan en una proporción tres veces mayor que los nacidos en España. Efecto: para el auge de 2000-2010, un estudio con diseño causal estima que la inmigración explica en torno a una cuarta parte de la subida de precios en España. Para 2015-2025 nuestras estimaciones son frágiles y no permiten cifrarlo. Un aumento de población presiona la demanda sea cual sea su origen. No hay evidencia de que un hogar inmigrante presione más que otro hogar equivalente. «Culpa» es un juicio, no un dato.

Confianza:
- contabilidad de la población: **la evidencia indica** (identidad con estadísticas oficiales);
- reparto por origen de los hogares nuevos: **la evidencia es compatible con** (supuesto de igual formación de hogares; cuota acotada al 100 %; resultado del Shapley que depende del orden; composición por nacionalidad ≈ −97.000 hogares);
- efecto positivo del aumento de población en el precio, a escala provincial: **la evidencia sugiere** (literatura con diseño; nuestro punto es compatible);
- magnitud en 2015-2025: **la evidencia no permite concluir**;
- efecto distinto por origen a igual número de hogares: **la evidencia no permite concluir**.

## 7. Parada

No hay parada. La frase de D1 no figura en publicacion/. La 1.0 (informe integral, VII.4) dice «Qué no se puede afirmar. Que la inmigración suba o baje el precio o el alquiler». Esa frase se apoya en las capas del proyecto (sus instrumentos débiles), no en la literatura. Con su regla de capas no es falsa. Sin embargo, omite que un diseño causal publicado para España (González y Ortega, 2013) halla un efecto positivo en 2000-2010. Se señala al autor como matiz, y como error de la referencia de partida D2 la cifra de «un tercio».

## 8. Respuesta a la ronda 1

- **Veredicto: aplicado.** Pasa a «engañosa», leyendo «lo» como la culpa (el efecto). Se mantiene que sería falsa si se refiriera a la contabilidad.
- **Literatura: aplicado.** Se añaden Torres-Téllez y Montero-Soler (2023), con signo cambiante según la fase, y la escala de Sá (2015), de área local.
- **González y Ortega: aplicado.** Van con la salvedad de d2_versiones.md: rango del 1,5-2,3 % anual y elasticidad de 1,0-1,5.
- **Confianza contable: aplicado.** El reparto por origen pasa a «es compatible con» (tope al 100 %, orden del Shapley, composición ≈ −97.000).
- **«Sobre todo de alquiler»: aplicado.** Se sustituye por la proporción con su denominador: 38,3 % de los hogares de nacidos fuera frente a 12,2 % de los nacidos en España.
- **Matiz que no se retira.** Torres-Téllez y Montero-Soler refuerzan que el signo depende de la fase, pero no de la escala. A escala provincial, el efecto del aumento de población en la fase de entrada es positivo en todos los trabajos españoles leídos.

## 9. Respuesta a la ronda 2

- **Estado de González y Ortega (2013): unificado.** Es VERIFICADA en cuanto a la referencia: el DOI 10.1111/jors.12010 se comprobó en Crossref el 2026-10-19 (título, autores, revista y páginas coinciden). La diferencia con d2_versiones.md, donde figura como NO VERIFICADA, es de criterio: allí se rotula el contenido, que solo se conoce por resúmenes porque la versión de Wiley no se leyó.
- **Respaldo de la frase: aplicado.** La afirmación cuantitativa («en torno a una cuarta parte») se apoya también en el documento de trabajo de 2011, leído en su texto: 25 % del aumento de precios en 2000-2010, conclusiones (d2_versiones.md).
- **Torres-Téllez y Montero-Soler (2023): aplicado.** Pasan a ser evidencia de simetría: la inmigración eleva el precio en la fase de entrada y su retorno lo reduce en la de salida, con el mismo mecanismo de población. No son un signo contrario. El texto de la sección 2 se mantiene, con esta lectura.
