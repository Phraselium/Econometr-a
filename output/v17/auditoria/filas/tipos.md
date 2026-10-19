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

**3.1 Calibración (juicio experto, calibración).** Cada semielasticidad se aplica al tipo con el que se estimó y se compara con su medida de precio. No es una estimación para España ni un contrafactual identificado.

| Fuente | Tipo | Medida de precio | %/pp | Subida aplicada | Efecto calibrado a ≈ 2 años |
|---|---|---|---|---|---|
| BCE, BE 6/2022, lineal (1995-2019) | hipotecario | no consta en lo leído | −5 | 2,27-2,51 pp (TAE nuevas) | −11,4 a −12,6 % |
| BCE, BE 6/2022, no lineal con tipos bajos | hipotecario | no consta | −9 | 2,27-2,51 pp | −20,5 a −22,6 % |
| Calza, Monacelli y Stracca (2013), reescalado por Williams (2015) | interbancario a 3 meses | real | −2,3 | 4,5 pp (facilidad de depósito, 2021T4-2023T4) | −10,4 % |
| Williams (2015), con Jordà, Schularick y Taylor (2015) | corto | real | −6,3 | 4,5 pp | −28,4 % |

- **Tipo hipotecario.** El efecto calibrado va de −11,4 % a −22,6 % (V17-AUD-DP-TIP-CALIBRACION-EFECTO-HIPOTECARIO). Descontado ese efecto, la variación nominal del IPV de 2021T4-2024T4 queda entre +38,0 % y +58,0 %, frente al +22,3 % observado (V17-AUD-DP-TIP-CALIBRACION-DESCONTADO).
- **Tipo de política.** El efecto calibrado sobre el precio real va de −10,4 % a −28,4 % (V17-AUD-DP-TIP-CALIBRACION-EFECTO-POLITICA). Descontado, el IPV real queda entre +21,1 % y +51,5 %, frente al +8,5 % observado. Es una extrapolación lineal de 1 a 4,5 puntos, fuera del rango en que se estimaron estas elasticidades.
- **Transmisión solo al 52 % de compras con hipoteca.** Efecto de −5,9 % a −11,7 % (V17-AUD-DP-TIP-CALIBRACION-SOLO-HIPOTECA). Es una cota inferior en valor absoluto, porque el comprador al contado también descuenta con el tipo.

Supuestos y límites:
- **Elasticidad.** La de la zona euro se aplica a España, con más hipoteca variable (Pica, 2023: ≈ 90 % en 2014) y menos compras con hipoteca.
- **Calendario.** Se ignoran el desfase de dos años y la bajada de 2024-2025: la TAE estaba en el 2,68 % en 2025T4.
- **Otros choques.** No se modelan.

Lectura: con cualquiera de esas elasticidades, el aumento observado es compatible con un efecto negativo de los tipos de varios puntos, compensado por otros factores. La calibración no dice cuáles.

**3.1 bis Cálculo de la 1.0 con el coste de uso** (publicacion/verificador/verificador.md, ficha B4-V4):
- 2014-2021: la caída del coste de uso es compatible como máximo con +23,5 % a +78,0 % de precio (Δln 1/uc), frente al +12,7 % del valor tasado.
- 2021-2025: «los tipos suben y el precio también (+25,0 %): signo contrario».
- La 1.0 lo rotula C4, como cota condicional a supuestos del coste de uso.

**3.1 ter Comparación con la zona euro.** Con la misma subida de tipos de política, los precios de la zona euro cayeron en torno a un 3 % en año y medio (BCE, Boletín Económico 2/2025; extraído por conversor). En España, el IPV subió un 22,3 % nominal entre 2021T4 y 2024T4. Ante el mismo choque monetario, la diferencia apunta a factores propios de España (hogares, renta, oferta y una menor dependencia del crédito), sin identificarlos.

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

**Se sostiene con matices** (lectura literal). El hecho es cierto y rebate la predicción literal de que el precio baje en nivel. El matiz: no muestra que los tipos no afecten al precio. Sin contrafactual, un efecto negativo de varios puntos es compatible con que el precio suba. En España, en 2023, cayeron el crédito y las compraventas. Si la frase se usa como «los tipos no importan», es engañosa.

## 6. Texto corregido y confianza

> «Con los tipos altos bajarán los precios»: en 2022-2024 subieron los tipos y también los precios, así que no bajaron. Eso no significa que los tipos no influyan. Con las elasticidades de la zona euro, la subida de unos 2,5 puntos del tipo hipotecario equivale a restar al precio entre un 11 % y un 23 % a unos dos años; es una calibración, no una estimación para España. En 2023 cayeron el crédito y las compraventas. A la vez crecían los hogares y la renta, y se terminaban unas 90.000 viviendas al año, frente a más de 200.000 hogares nuevos. Cerca de la mitad de las compras no usa hipoteca. En la zona euro, con la misma subida, los precios cayeron en torno a un 3 %.

Confianza:
- signo negativo del efecto de los tipos sobre el precio: **la evidencia indica** (zona euro);
- magnitud en España en 2022-2024: **la evidencia es compatible con** el rango calibrado (no medido en España);
- qué compensó la subida (demanda, renta, oferta): **la evidencia no permite concluir** (V8: patrón de cuatro cuadrantes; Q5 no separa los choques).

## 7. Parada

No hay parada. La 1.0 no afirma que los tipos no afecten al precio. Dice que el patrón es compatible con un choque de demanda simultáneo y que Q5 no separa los dos choques. Su ficha B4-V4 da el «signo contrario» de 2021-2025 como descripción, no como efecto.

## 8. Respuesta a la ronda 1

- **Unidades coherentes: aplicado.** Cada elasticidad va con su tipo (hipotecario o de política) y su medida de precio (real o nominal), y se añade el −9 %/pp no lineal del BCE con tipos bajos (3.1).
- **Id: aplicado.** TIP-CONTRAFACTUAL pasa a TIP-CALIBRACION-DESCONTADO (con su variante real). La lectura ya no usa «sería».
- **Lectura de los hechos: aplicado.** Todos los hechos de calibración llevan «juicio experto (calibración)», con rango completo, elasticidades y fuente.
- **Texto corregido: aplicado.** Sin el «porque» causal; «apenas se construía» pasa a ≈ 90.000 terminadas al año.
- **Comparaciones nuevas: aplicado.** Se añaden el cálculo de la 1.0 con el coste de uso (3.1 bis) y la zona euro, con una caída de ≈ 3 % (3.1 ter).
- **Veredicto: aplicado.** Pasa a «se sostiene con matices», porque la lectura auditada es la literal; se mantiene la advertencia de uso engañoso.
