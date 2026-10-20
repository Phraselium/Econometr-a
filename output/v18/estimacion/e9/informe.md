# V18 · E9 Compradores no residentes: recuento de choques efectivos

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.* Generado por `python3 src/v18/estimacion/e9_no_residentes.py` (SEED 20261010, sin red). Clasificaciones provisionales: pendientes de I8. Toda cifra es C4 (EXPLORATORIO). Sin lenguaje causal.

## 1. Resumen
- **E9-R1, E9-R2, E9-A1 y E9-A2: NO ESTIMABLES por choques efectivos.** Con la exposición del padrón de 2003 (residentes por nacionalidad, aproximación a la exposición por compradores) y los 8 orígenes con serie de riesgo (Alemania, Francia, Italia, Portugal, Reino Unido, Rumanía, Bulgaria, Polonia), 1/HHI = 6.30 sin pesos y 5.88 con pesos de población, por debajo del umbral de 10 de la adenda (1.3 y 1.13). Si los 28 países individuales del padrón tuvieran serie de riesgo, 1/HHI sería 11.54: el límite son las series de riesgo de los países latinoamericanos, africanos y asiáticos, que no están en el repositorio.
- **E9-X1 y E9-X2: NO ESTIMABLES por datos.**
- No se estima ningún coeficiente. B5: E9-R2 (la estimación propia) no tiene respaldo; E9 no aporta magnitud propia (entra solo la literatura). Doble cómputo E3/E9: sin instrumento de E9 no hay correlación que publicar (adenda 1.10).

## 2. Diseño que se habría estimado
- Original: Badarinza y Ramadorai (2018; Londres 1995-2013; +1,62 pp de precio en barrios de más cuota del país en riesgo, transitorio), Sá (2016; +2 % de precio por +1 pp de cuota de compras de no residentes, IV), Cvijanović y Spaenjers (2021; París, efecto pequeño y no significativo), Álvarez, Blanco y García-Posada (2020; MCO transversal, no significativo).
- Traslado: 39 provincias de entrenamiento, exposición s_pc = residentes de la nacionalidad c entre la población de 2003 (padrón provincial), riesgo en origen = caída del PIB en el quintil superior de la historia del país (a 4 trimestres); R2 instrumenta la cuota de no residentes (MIVAU) con el índice de R1. Signo esperado fijado en la adenda: positivo.

## 3. Recuento de choques efectivos

| conjunto de orígenes | pesos | nº de orígenes | 1/HHI |
|---|---|---|---|
| origenes_con_serie_de_riesgo | sin pesos | 8 | 6.30 |
| origenes_con_serie_de_riesgo | pesos de población 2003 | 8 | 5.88 |
| todos_los_paises_del_padron_(informacion) | sin pesos | 28 | 11.54 |
| todos_los_paises_del_padron_(informacion) | pesos de población 2003 | 28 | 11.88 |

Pesos de los orígenes con serie de riesgo (sin pesos): Alemania 11.8%, Francia 8.9%, Italia 6.1%, Portugal 14.3%, Reino Unido 19.0%, Rumanía 24.4%, Bulgaria 12.8%, Polonia 2.8%.

Por origen × trimestre (76 trimestres de riesgo) el recuento sería 479 solo si los choques de un origen fueran independientes entre trimestres; no lo son (el PIB y el empleo en origen son persistentes), de modo que la regla de la adenda cuenta orígenes («unos 10 a 15 orígenes»).

## 4. Tabla de especificaciones

| id | descripción | tope de la tabla consolidada | estado | motivo |
|---|---|---|---|---|
| E9-R1 | Badarinza-Ramadorai, forma reducida: Δ ln precio sobre exposición a nacionalidades × riesgo en origen (caída del PIB en el quintil superior de su historia, a 4 trimestres) | SUGESTIVO | NO ESTIMABLE | NO ESTIMABLE por choques efectivos: 1/HHI = 6.30 sin pesos y 5.88 con pesos de población (< 10; adenda 1.3 y 1.13) con 8 orígenes que tienen serie de riesgo |
| E9-R2 | Sá, IV: Δ ln precio sobre Δ cuota de no residentes en las compras, instrumentada por el índice de R1 | IDENTIFICADO | NO ESTIMABLE | NO ESTIMABLE por choques efectivos: 1/HHI = 6.30 sin pesos y 5.88 con pesos de población (< 10; adenda 1.3 y 1.13) con 8 orígenes que tienen serie de riesgo |
| E9-A1 | R1 con el tipo de cambio como choque (libra en 2016 y otras monedas fuera del euro) | SUGESTIVO | NO ESTIMABLE | NO ESTIMABLE por choques efectivos: 1/HHI = 6.30 sin pesos y 5.88 con pesos de población (< 10; adenda 1.3 y 1.13) con 8 orígenes que tienen serie de riesgo |
| E9-A2 | R2 con compras de extranjeros residentes (CCAA, 9 no selladas) como primera etapa alternativa | IDENTIFICADO | NO ESTIMABLE | NO ESTIMABLE por choques efectivos: 1/HHI = 6.30 sin pesos y 5.88 con pesos de población (< 10; adenda 1.3 y 1.13) con 8 orígenes que tienen serie de riesgo |
| E9-X1 | fin de la golden visa (LO 1/2025) como diferencias en diferencias, UE frente a fuera de la UE | NO ESTIMABLE | NO ESTIMABLE | no hay compras separadas entre la UE y fuera de la UE por provincia ni autorizaciones de la OPI (tareas_autor, puntos 7 y 14) |
| E9-X2 | introducción de 2013 (Martínez-Toledano et al.) | NO ESTIMABLE | NO ESTIMABLE | requiere el universo de transacciones (Registradores o Notariado) |

Qué datos las harían estimables: (i) compras de no residentes por nacionalidad del comprador y provincia (Notariado, Registradores o la estadística del Ministerio con detalle de nacionalidad), para una exposición por compradores y no por residentes, con al menos 10 choques efectivos; (ii) series de riesgo en origen para los países latinoamericanos, africanos y asiáticos (PIB, tipo de cambio) y no solo para 31 países europeos; (iii) autorizaciones de residencia por inversión de la OPI y compras por nacionalidad UE/fuera de la UE y provincia para X1 (tareas_autor, puntos 7 y 14); (iv) el universo de transacciones para X2; (v) las 4 provincias selladas de más cuota de no residentes (Baleares, Las Palmas, Santa Cruz de Tenerife y Murcia), que no se leen.

## 5. Limitaciones
- La exposición es por residentes, no por compradores (aproximación declarada en el plan).
- Los países no europeos (Ecuador, Colombia, Marruecos, China, etc.) no tienen serie de riesgo en el repositorio.
- Las cuatro provincias selladas de más cuota de no residentes (Baleares, Las Palmas, Santa Cruz de Tenerife y Murcia) no entran; quedan Alicante, Málaga y Girona.
- I8 (réplica ciega) y la ronda del abogado del diablo (B6) están pendientes.

