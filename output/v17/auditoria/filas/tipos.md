Análisis a posteriori (V17). Ficha de auditoría de la fila «tipos» (D1, discurso político). Grupo demanda_precios. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia. Ids nuevos: V17-AUD-DP-TIP-*.

# «Con los tipos altos bajarán los precios»

## 1. Texto auditado

> «Con los tipos altos bajarán los precios»: en 2022-2024 subieron los tipos y también los precios.

La respuesta usa un hecho (tipos y precios suben a la vez) para rebatir una afirmación causal (los tipos altos bajan los precios). Lo que hay que auditar es si el hecho rebate la afirmación.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- **El hecho es cierto.**
  - El tipo de las nuevas hipotecas (TAE, Banco de España) pasó del 1,54 % en 2021T4 al 4,06 % en 2023T3, +2,5 pp (V17-AUD-DP-TIP-DELTA-TAE).
  - El IPV subió un 22,3 % nominal y un 8,5 % real entre 2021T4 y 2024T4 (V17-AUD-DP-TIP-IPV-2022-2024).
- **Rebate la versión fuerte.** Quien dijera «los tipos harán bajar el precio en nivel» se equivocó en 2022-2024.
- **Nuestra estimación no da señal estable.** Q5 (V16), con proyecciones locales y sorpresas monetarias, Newey-West y tamaño real del 8,4-11,6 % (publicable):

| Horizonte | Efecto por DT de sorpresa | p | Holm |
|---|---|---|---|
| 1 trimestre | −0,45 % | 0,036 | 0,29 |
| 4 trimestres | −0,51 % | 0,32 | — |
| 8 trimestres | +0,23 % | 0,81 | — |
| 12 trimestres | +2,3 % | 0,15 | — |

La 1.0 no la cita, por la primera etapa con signo contrario y el placebo (informe integral, Q5).

**En contra.**
- **Falta el contrafactual.** Que dos cosas suban a la vez no dice qué habría pasado sin la subida de tipos. La literatura con identificación da un efecto negativo:
  - BCE (Boletín Económico 6/2022, proyecciones locales, zona euro 1995-2019): +1 pp de tipo hipotecario ≈ −5 % de precio a unos dos años;
  - Williams (2015), con Jordà, Schularick y Taylor (2015): −6,3 %;
  - Calza, Monacelli y Stracca (2013): −2,3 %.
- **La demanda se movió en sentido contrario al mismo tiempo.**
  - La renta disponible bruta de los hogares subió un 28,4 % nominal de 2021 a 2024 y los hogares (EPA) en unos 791.000 (V17-AUD-DP-TIP-RDB-2021-2024).
  - La oferta nueva siguió en unas 90.000 viviendas al año (BdE IA2023).
- **Los tipos sí movieron lo que deben mover primero: crédito y compraventas.**
  - En 2023 las hipotecas sobre viviendas cayeron de 464.107 a 380.966 (−18 %) y las compraventas de 650.265 a 583.651 (−10 %) (output/v17/lectura_bde/medidas_referencia/).
  - El flujo de crédito hipotecario cayó un 10,5 % interanual en 2023T4 (BdE IEF primavera 2024).
  - Las compras con hipoteca pasaron de más del 50 % en 2021 a menos del 45 % en 2023 (BdE DO 2433).
- **Una parte de la demanda no depende del crédito.**
  - Con hipoteca, solo el 52 % de las compras de 2025 (BdE IA2025, p. 124). Nuestra cota inferior de compras sin hipoteca es del 30 % (V17-B5).
  - No residentes, el 7,4 % de las compras de 2021-2025 (IA2025, p. 149), y personas jurídicas, el 10 % (IA2025, p. 123).
  - La transmisión por el canal del crédito es menor que en la zona euro media de la muestra del BCE.

## 3. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_demanda_precios.py. Serie: data/processed/v8/nacional_q_v8.csv, versionada.

**3.1 Contrafactual aproximado.** Es juicio experto: ilustración con parámetros de la zona euro, no un contrafactual identificado.

| Supuesto | Efecto en el precio a ≈ 2 años | IPV 2021T4-2024T4 sin la subida |
|---|---|---|
| −5 %/pp (BCE) × 2,27 pp (subida de la media anual 2021→2023) | −11,4 % | +38,0 % |
| Rango: −2,3 a −6,3 %/pp × 2,27-2,51 pp | −5,2 a −15,8 % | +29,0 a +45,3 % |
| Transmisión solo al 52 % de compras con hipoteca | −2,7 a −8,2 % (central −5,9 %) | — |
| Observado | — | +22,3 % |

Supuestos y límites:
- **Elasticidad.** La de la zona euro se aplica a España, que tiene más hipoteca variable (Pica, 2023: ≈ 90 % en 2014) y menos compras con hipoteca.
- **Calendario.** Se ignoran el desfase de dos años y la bajada de tipos de 2024-2025: la TAE estaba en el 2,68 % en 2025T4.
- **Otros choques.** No se modelan los demás choques.
- **Escalado al 52 %.** Es una cota inferior en valor absoluto, porque el comprador al contado también descuenta con el tipo (coste de oportunidad).

Lectura: con cualquiera de esos parámetros, sin la subida de tipos el precio habría subido más (entre 7 y 23 puntos más en tres años). El hecho «subieron los dos» es compatible con un efecto negativo de los tipos de esa magnitud.

**3.2 Banco de España y BCE.**
- No se encontró ningún documento del Banco de España con un efecto por cada 100 pb sobre el precio o las compraventas en España (docs/v17/referencias/bde_bce_documentos.md).
- El Banco de España describe contención del crédito y de la actividad, y que la menor financiación se compensa «en parte» con recursos propios (DO 2433, p. 26).
- El BCE (WP 2752, regiones 1999-2018) halla que el choque monetario convencional explica una parte muy pequeña de la varianza del precio de la vivienda. Es otro choque y otro régimen.

## 4. Literatura

| Referencia | Estado | Lectura |
|---|---|---|
| Battistini, Gareis y Roma (2022), «The impact of rising mortgage rates on the euro area housing market», ECB Economic Bulletin 6/2022 | NO VERIFICADA (sin DOI) | texto de la página por conversor (docs/v17/referencias) |
| Williams (2015), FRBSF Economic Letter 2015-28 | NO VERIFICADA (sin DOI) | texto (docs/v15/literatura/P3_tipos_interes.md) |
| Calza, Monacelli y Stracca (2013), JEEA 11(S1), DOI 10.1111/j.1542-4774.2012.01095.x | VERIFICADA (Crossref, 2026-10-19) | resumen y cifra reescalada por Williams |
| Jordà, Schularick y Taylor (2015), J. International Economics 96(S1), DOI 10.1016/j.jinteco.2014.12.011 | VERIFICADA (Crossref) | resumen |
| Battistini, Falagiarda, Hackmann y Roma (2022), ECB WP 2752 | NO VERIFICADA (DOI del documento no localizado) | parcial (pp. 1-8, 19-26) |
| Dieckelmann et al. (2023), ECB WP 2789 | NO VERIFICADA | parcial (pp. 1-3) |
| Pica (2023), Banco de Italia, documento de trabajo | NO VERIFICADA (sin DOI) | texto parcial (P3) |
| BdE DO 2433 (DOI 10.53479/37873) e IA2025 | VERIFICADA (DO 2433, Crossref); NO VERIFICADA (IA2025, sin DOI) | parcial |

## 5. Veredicto

**Engañosa.** El hecho es cierto y rebate la versión literal, que el precio baje en nivel. Pero se presenta como si mostrara que los tipos no afectan al precio. Eso es confundir correlación con efecto, sin contrafactual. La evidencia con diseño de la zona euro da un efecto negativo de varios puntos a dos años. En España los tipos sí frenaron el crédito y las compraventas en 2023. El precio siguió subiendo porque la demanda (hogares y renta) y la oferta rígida empujaban más.

## 6. Texto corregido y confianza

> «Con los tipos altos bajarán los precios»: no necesariamente. Los tipos altos frenan el precio respecto a lo que habría subido, pero no tienen por qué bajarlo. En 2022-2023 el tipo de las nuevas hipotecas subió unos 2,5 puntos. Con las estimaciones del BCE para la zona euro, eso resta al precio del orden de un 5 % a un 16 % a dos años. En España el crédito y las compraventas cayeron en 2023. El precio siguió subiendo porque los hogares y la renta crecían y apenas se construía. Además, cerca de la mitad de las compras no usa hipoteca, y eso debilita el efecto.

Confianza:
- signo negativo del efecto de los tipos sobre el precio: **la evidencia indica** (zona euro);
- magnitud en España en 2022-2024: **la evidencia es compatible con** el rango de 5-16 %, que no se ha medido en España;
- que el precio subiera a pesar de la subida porque dominó la demanda: **la evidencia sugiere** (V8: patrón de cuatro cuadrantes; no separado).

## 7. Parada

No hay parada. La 1.0 no afirma que los tipos no afecten al precio. Dice que el patrón es compatible con un choque de demanda simultáneo y que Q5 no separa los dos choques (informe integral, II y Q5). La paráfrasis D1 es más débil que la 1.0 en este punto, pero no la contradice.
