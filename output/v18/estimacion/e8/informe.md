# V18 · E8 · Fiscalidad de la compra: ITP por comunidades

**Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO. La clasificación V18 va en `clasificacion_v18` y no cambia la capa. I8 cumplido: la réplica ciega de E8-R1 coincide (output/v18/replica/e8_r1); clase final tras la ronda 1 del abogado del diablo (K7). Las demás especificaciones de E8 son NO ESTIMABLES y no necesitan réplica.
Código: `src/v18/estimacion/e8_itp.py` (+ `e8_datos.py`, `e8_diseno.py`, `e8_estim.py`, `e8_salidas.py`, `_e2e8_comun.py`); SEED 20261010; sin red; 28 s.
Rótulo del plan (1.8): no se conoce una evaluación española del ITP con diseño (ficha L4); esta sería la primera, con las reservas de la clasificación.

## 1. Resumen
- **E8-R1 (principal)**: Wald-DID de dosis continua sobre el log del valor tasado provincial a 4 trimestres = **0.0146 por punto** del tipo general (IC95 por inversión de la aleatorización 0.0009; 0.0309); p de aleatorización 0.0437; p tras Holm (familia E8, m = 2) 0.0874. Clase V18: **ASOCIACIÓN**.
- El signo es **contrario** al de la referencia (Dolls et al.: −0,03 por pp; razón -0.49, etiqueta «no coherente»). Sin 2012-2013 el signo cambia (-0.0079, p de aleatorización 0.176): el calendario de cambios se concentra en la crisis y el diseño no separa el tipo del ciclo.
- **Coprincipal V16-Q6-p** reproducida en la muestra V18: -0.002037 por punto (cifra publicada −0,0020); p de aleatorización 0.880.
- **No estimables**: E8-R2 (compraventas: MDE 0.0894 > 0,06 por punto), E8-A2 (municipal: MDE 0.2157 > 0,06), E8-A1 (recaudación sin datos), E8-X1 y E8-X2 (sin compraventas por tramo ni calendario de tipos reducidos). E8-P-Q6v hereda la no estimabilidad de E8-R2.
- Ninguna estimación IDENTIFICADO: no hay contradicción con una conclusión publicada (parada G no activada). Lo publicado (Q6-p «no concluyente», Q6-v «descriptivo», ITP «no evaluable con los datos disponibles») no cambia.

## 2. Qué se ha leído y qué queda fuera (sellado)
- Toda serie pasa por `sellado.filtrar` y `holdout.excluir_sellados_v6`. No se lee `data/sealed` ni se ejecuta ningún `evaluate_*`.
- Las 8 comunidades de régimen común no selladas en v6 (Andalucía, Cantabria, Castilla y León, Castilla-La Mancha, Cataluña, Comunitat Valenciana, Extremadura y Galicia) suman 36 provincias (la adenda corrige las 30 del plan). El valor tasado provincial completo 2007T1-2026T2 existe para 30 de ellas (7 comunidades: falta Cantabria y seis provincias con huecos). Las compraventas mensuales (INE) cubren las 36.
- Los territorios forales y Ceuta y Melilla no entran. Los bloques de V15 y V16 no contienen provincias, solo municipios y distritos: no afectan al diseño provincial.

## 3. Calendario de cambios del tipo general y reglas de codificación (adenda R-18)
Reglas: fecha de entrada en vigor; mes de entrada si es día 15 o anterior y, si no, el siguiente (trimestral: el trimestre de ese mes); dosis = variación del tipo general en puntos (en las escalas, el tipo mínimo, que es el «tipo general» de la base); dos cambios de una comunidad a menos de 12 meses se fusionan con la dosis acumulada en la primera fecha. Antes de 2010 no hay datos de tipos: se supone sin cambios en 2007-2009.

**Calidad de las fechas.** La base de intervenciones recoge las memorias de Hacienda (fuente secundaria): las fechas de 1 de enero son aproximadas y las demás constan en la memoria, pero ninguna está contrastada con el BOE ni con el diario autonómico (la fuente `itp_fechas_entrada_en_vigor` es posterior a la etiqueta y no está descargada). Por eso: tope SUGESTIVO (plan 1.8 f), y la variante de fechas del 1 de enero y las de ±3 meses se publican.

| cod_ine | fecha_original | dosis | fecha_codificada_mes | fecha_codificada_trimestre | calidad_fecha |
|---|---|---|---|---|---|
| 01 | 2012-01-01 | +1 | 2012-01 | 2012T1 | aproximada (1 de enero) |
| 01 | 2021-04-28 | -1 | 2021-05 | 2021T2 | de la memoria de Hacienda, sin contraste con el BOE |
| 06 | 2013-01-01 | +1 | 2013-01 | 2013T1 | aproximada (1 de enero) |
| 06 | 2019-01-01 | +2 | 2019-01 | 2019T1 | aproximada (1 de enero) |
| 06 | 2024-01-01 | -1 | 2024-01 | 2024T1 | aproximada (1 de enero) |
| 07 | 2013-01-01 | +1 | 2013-01 | 2013T1 | aproximada (1 de enero) |
| 08 | 2012-01-01 | +1 | 2012-01 | 2012T1 | aproximada (1 de enero) |
| 08 | 2016-06-01 | +1 | 2016-06 | 2016T2 | de la memoria de Hacienda, sin contraste con el BOE |
| 09 | 2010-07-01 | +1 | 2010-07 | 2010T3 | de la memoria de Hacienda, sin contraste con el BOE |
| 09 | 2013-08-01 | +2 | 2013-08 | 2013T3 | de la memoria de Hacienda, sin contraste con el BOE |
| 10 | 2013-01-01 | +3 | 2013-01 | 2013T1 | aproximada (1 de enero) |
| 10 | 2026-06-01 | -1 | 2026-06 | 2026T2 | de la memoria de Hacienda, sin contraste con el BOE |
| 11 | 2012-01-01 | +1 | 2012-01 | 2012T1 | aproximada (1 de enero) |
| 12 | 2013-03-01 | +3 | 2013-03 | 2013T1 | de la memoria de Hacienda, sin contraste con el BOE |
| 12 | 2022-01-01 | -1 | 2022-01 | 2022T1 | aproximada (1 de enero) |
| 12 | 2024-01-01 | -1 | 2024-01 | 2024T1 | aproximada (1 de enero) |

## 4. Estimabilidad (adenda 1.3), calculada antes de mirar los coeficientes
Mínimo de datos: al menos 8 cambios efectivos en 4 comunidades (E8-R1: 12 cambios efectivos del tipo general en 7 comunidades (mínimo 8 en 4); 30 provincias con valor tasado). MDE80 por Monte Carlo (R = 2.000 reasignaciones de los calendarios entre comunidades, con el estimador principal; valor crítico = cuantil 95 % de |β̂| entre las reasignaciones; σ «ya vista»).

| id | n_unidades | n_comunidades | mde80 | umbral | estimable |
|---|---|---|---|---|---|
| E8-R1 | 30 | 7 | 0.0244 | 0.0300 | True |
| E8-R2 | 36 | 8 | 0.0894 | 0.0600 | False |
| E8-A1 | 0 | 0 | — | 0.1000 | False |
| E8-A2 | 164 | 8 | 0.2157 | 0.0600 | False |

## 5. Resultado de E8-R1 y pruebas B4
- Inferencia principal: aleatorización estudentizada de los calendarios entre 7 comunidades (Monte Carlo de V18: tamaño 0,0455, APTO); p = 0.0437. Alternativas: t con G − 1 = 6 gl, p = 0.0208 (tamaño 0,0655: con valor crítico corregido, p corregido 0.0273); Webb p = 0.0002 (rótulo «no fiable»: tamaño 0,12-0,15 con 8 clusters); TWFE de nivel con Driscoll-Kraay -0.0004 (p 0.8947; «no fiable»).
- Honest DiD: no se usa (con 7-8 clusters la covarianza tiene rango ≤ 7 y el tamaño con M̄ = 0 es 0,17 en el Monte Carlo de V18).
- TOST con δ = 0,015 por pp: intervalo al 90 % (0.0055; 0.0237), no dentro de ±δ.

**Adelantos** (diferencia del resultado retardado entre unidades que cambian y estables, normalizada por la dosis; contraste conjunto por aleatorización de calendarios, p = 0.994):

| adelanto (trimestres antes) | gap | p (aleatorización) |
|---|---|---|
| −2 | -0.0060 | 0.196 |
| −3 | -0.0011 | 0.850 |
| −4 | 0.0013 | 0.880 |
| −5 | -0.0001 | 0.995 |
| −6 | 0.0006 | 0.956 |
| −7 | 0.0010 | 0.945 |
| −8 | 0.0005 | 0.966 |

- Potencia previa (aproximación de Roth por aleatorización): pendiente detectable al 80 % = 0.0035 por trimestre; sesgo implicado en la ventana posterior = 0.0176, mayor que la mitad de |referencia| (0,015): prueba débil.
- I de Moran de los residuos medios por provincia del TWFE de la dosis (5 vecinos): I = 0.018 (E[I] = -0.034), p unilateral = 0.297.
- Placebo de fecha (resultado de 8 trimestres antes): 0.0005, p = 0.966.
- Placebo de resultado (log de la población provincial, anual): -0.0023, p = 0.475.
- No hay estimación sin 2012-2013 con el mismo signo: v4 = -0.0079.

## 6. Variantes enumeradas (anexo A)
Aleatorización con 4.999 permutaciones; q_by = Benjamini-Yekutieli al 10 % dentro de E8-R1.

| id | nota | estado | coef | se | p_t | p_aleat | q_by |
|---|---|---|---|---|---|---|---|
| E8-R1-v1 | [M] fechas del 1 de enero | estimada | 0.0011 | 0.0091 | 0.906 | 0.925 | 1.000 |
| E8-R1-v2 | [M] fechas −3 meses | estimada | 0.0088 | 0.0052 | 0.142 | 0.271 | 0.994 |
| E8-R1-v3 | [M] fechas +3 meses | estimada | 0.0131 | 0.0059 | 0.069 | 0.104 | 0.766 |
| E8-R1-v4 | [V] sin 2012-2013 (cambiantes fuera de esos años) | estimada | -0.0079 | 0.0039 | 0.087 | 0.176 | 0.862 |
| E8-R1-v5 | [E] subidas por separado (Sun-Abraham): todas las comunidades del panel suben el tipo en algún momen | NO ESTIMABLE | — | — | — | — | — |
| E8-R1-v6 | [E] bajadas por separado (Sun-Abraham): 3 comunidades con bajadas y 4 sin ellas; p de Webb sin banda | estimada | 0.0368 | 0.0130 | 0.243 | — | — |
| E8-R1-v7 | [M] IPV por comunidad | estimada | 0.0073 | 0.0070 | 0.333 | 0.381 | 1.000 |
| E8-R1-v8 | [U] sin Barcelona | estimada | 0.0172 | 0.0057 | 0.023 | 0.049 | 0.726 |
| E8-R1-v9 | [C] sin recaudación previa: la principal ya va sin control de recaudación (la fuente no está descarg | coincide con la principal | 0.0146 | 0.0047 | 0.021 | 0.044 | — |

## 7. Coprincipal V16-Q6-p
Wald-DID anual 2011-2024 de V16 (año de efecto, ΔY de años consecutivos, año previo al cambio fuera por anticipación) sobre las provincias de las 8 comunidades con valor tasado anual: **-0.002037** por punto (V16: −0,002037; coincide). V16 no daba inferencia (dCDH con aleatorización NO APTO); aquí se añade la aleatorización de calendarios con el coeficiente como estadístico (p = 0.880, 35 provincias). No se clasifica; entra en la familia de Holm.

## 8. Clasificación (I1-I8 revisados)
- **E8-R1: ASOCIACIÓN.** Razones: el signo cambia sin 2012-2013 (prueba B4 del plan, línea 737): cambio de signo en B4 = fallo decisivo (plan, línea 124; K7).
- I6: razón con la referencia -0.49 (signo contrario): etiqueta «no coherente»; no interviene en la clase ni en B5.
- Clase ASOCIACIÓN por fallo decisivo: el signo cambia sin 2012-2013 (prueba B4 del plan, línea 737; un cambio de signo en B4 es fallo decisivo, línea 124; el tope SUGESTIVO de la adenda R-18 es un techo y no anula esa regla; K7). Topes que se mantendrían de todos modos: fechas sin contraste con el BOE, ausencia del control de recaudación previa y corrección de un fallo conocido de Q6.
- Lectura: asociación estimada con diseño de dosis continua; no se interpreta como respuesta del mercado al impuesto.

## 9. Desviaciones y lecturas de las reglas (se recogen en docs/v18/desviaciones.md)
- **D1. Fechas.** La fuente de fechas exactas (`itp_fechas_entrada_en_vigor`) no está descargada (sin red): se usan las de la base de intervenciones (Hacienda, fuente secundaria) con las reglas de codificación de la adenda; toda la especificación principal es «con fechas no contrastadas» (tope SUGESTIVO).
- **D2. Recaudación previa.** `itp_recaudacion_ccaa` no está descargada: la principal va sin ese control (tope SUGESTIVO) y E8-A1 es NO ESTIMABLE; E8-R1-v9 coincide con la principal.
- **D3. Valor tasado.** El panel completo 2007T1-2026T2 solo existe para 30 provincias de 7 comunidades (el plan decía 30; la adenda, 36 por recuento de provincias): se declara y se calcula el mínimo de datos con las comunidades presentes.
- **D4. Compraventas.** E8-R2 usa vivienda usada (el ITP grava la usada, plan 1.8 b); la coprincipal V16-Q6-v usaba el total.
- **D5. Códigos INE de MIVAU.** E8-A2: código por nombre dentro de su comunidad con el diccionario oficial del INE (3 de 205 sin resolver).
- **D6. Sun-Abraham.** E8-R1-v5 (subidas) no tiene comunidades nunca tratadas: NO ESTIMABLE. E8-R1-v6 (bajadas) tiene pocas comunidades tratadas (3, una de ellas con la bajada en 2026T2, sin periodo posterior): estimación puntual con p de Webb sin banda de Monte Carlo propia.
- **D7. Adelantos y Roth.** Los adelantos y la pendiente detectable se obtienen por aleatorización de calendarios (sin covarianza analítica de los adelantos): son diagnósticos sin Monte Carlo propio.
- **D8. Lectura de la regla de clasificación.** Aplicada literalmente (véase E2, D8); el p tras Holm entre 0,05 y 0,10 es una prueba débil.
- **D9. Coprincipal E8-P-Q6v** no se estima (hereda E8-R2).

## 10. Limitaciones y datos que las resolverían
- Calendario concentrado en 2012-2013 (crisis): el diseño no separa el tipo del ciclo; sin ese tramo el signo cambia.
- 7 comunidades como unidad de tratamiento: la inferencia de aleatorización tiene 5.040 calendarios posibles.
- Fechas exactas de entrada en vigor (BOE y diarios autonómicos), recaudación del ITP por comunidad, compraventas por tramo de precio (Notariado o AEAT, modelo 600) y tipos reducidos (tareas_autor, punto 7).
