# Reconciliación original-réplica, lote c (GSADF de V7.2 y R6 de V7.1)

Todo se ejecutó con COPIAS en el directorio temporal de sesión (nada en output/ ni src/; sin data/sealed ni holdout: se leyó data/processed/nacional_q.csv y panel_ccaa_q.csv). Las copias reproducen el original: las 14 series nacionales de v5 (estadístico y p, SEED+500+k, 499 réplicas) son idénticas a output/v5/R1B/tablas/gsadf_corregido.csv, y la copia de R6 reproduce output/v7/R6/impactos.csv con diferencia máxima 0. Los demás números son diagnósticos, no cifras nuevas. C4 en todo.

## 1. Trazado del original (src/v5/r1b_gsadf.py, que importa V7.2)

| Elemento | Original | Réplica (v10_c.py) |
|---|---|---|
| ADF | constante, sin tendencia, 1 retardo fijo (también en la ficha: «ADF con un rezago») | igual (P_ADF = 1) |
| Ventana mínima (r0 = 0,01 + 1,8/√T) | w0 = 16 observaciones de la REGRESIÓN (18 de la serie) | 16 de la SERIE (14 de regresión) |
| Bootstrap | recursivo bajo raíz unitaria, DGP AR(p) de Δy con p por BIC (p ≤ 4), residuos centrados, 499 | DGP AR(1), el mismo p que la ADF |
| Familias de ajuste (BH) | `familia`: «fundamentales» = 4 cocientes + 4 con tipos = 8; «referencia» (niveles) = 2; sensibilidad = 4; CCAA = 34 | cocientes 4; tipos 4; niveles 2; CCAA 34 |
| CCAA | 2 series por CCAA; `dropna` conjunto de ipv, p_tasado e ipc_alquiler y tramo continuo más largo (r1b_gsadf.py:206-207) | v7 panel; Navarra tasado interpolada log-lineal (2015-2018) |

## 2. Primera diferencia y cadena de causas

1. Estadístico: coincide en 13 de 14 series nacionales. Solo difiere valor tasado/renta (0,224 frente a 0,387) por la convención de ventana: con 18 observaciones la réplica da exactamente 0,224.
2. Valores críticos: el DGP del bootstrap (BIC del original frente a AR(1) de la réplica) y la ventana mueven p. Es el factor que más pesa en CCAA.
3. Familia BH: decide ratios-bh.
4. Ruido Monte Carlo: con 499 réplicas, p ≈ 0,05 tiene error típico ≈ 0,01.

Prueba de cierre: original + DGP AR(1) + ventana de la réplica da 23 (frente a 23 de la réplica) en CCAA, y a 3.999 réplicas 2 (cocientes p05), 2 (cocientes BH de 4) y 1 (niveles), como la réplica. La réplica queda explicada por sus elecciones, no por un fallo de cálculo.

## 3. Errores del ORIGINAL (con corrección mínima)

**E1. BIC no comparable entre p (r1b_gsadf.py:75-83, `ar_fit`).** Cada p se ajusta con `yy = dy[p:]`, así que n cambia con p, y el criterio `n·ln(MSE) + (p+1)·ln n` depende de la escala: ln(MSE) ≈ −9 para Δy en logaritmos, y cada retardo pierde una observación (+9 de BIC), lo que sesga hacia p bajo. Prueba: multiplicar Δy por 1, 10, 100, 1000 cambia p (IPV/renta: 0, 0, 4, 4; nivel IPV: 1, 2, 4, 4). Frente a su documentación («AR(p) por BIC, p ≤ 4») el código no es un BIC válido. Corrección: elegir p sobre la muestra común `dy[pmax:]` y estimar después con `dy[p:]`. Con ella, 31 de 48 series cambian de p (por ejemplo, IPV/alquiler pasa de 1 a 4).

**E2. Navarra truncada (r1b_gsadf.py:206).** El `dropna` conjunto de ipv, p_tasado e ipc_alquiler elimina el IPV de Navarra de 2019 en adelante (el tasado falta en 2015-2018). Sus dos series quedan en T = 32 (2007T1-2014T4), mientras que la ficha, la cifra y ficha_burbuja.md declaran «17 CCAA, 2007T1-2026T2, T = 78». Corrección: `dropna` solo de [precio, ipc_alquiler] por serie y limitar a 2007T1-2026T2. El IPV de Navarra pasa a T = 78.

## 4. Veredicto por cifra

Efectos sobre el original con 499 réplicas (semilla original) y, entre paréntesis, con 1.999 réplicas y otras semillas. «Corr.» = E1 + E2.

| Cifra (pub. / réplica) | Veredicto | Evidencia |
|---|---|---|
| ccaa-bh (7 / 23) | **Original con error** (E1, E2); réplica con elecciones abiertas y una infracción de regla | El original da 7 (8, 6, 4 con otras semillas: borde). Solo E2: 10 (9, 10, 8). Con DGP AR(1) y ventana de la réplica: 23. Corr.: 0 de 34 (p<0,05: 5-6). La réplica infringe la regla del proyecto (interpolación solo en robustez): en mi copia, con Navarra truncada o corregida y el resto de elecciones de la réplica, el recuento también es 23, así que la interpolación no explica la discrepancia. |
| niveles-bh (2 / 1) | **Original con error** (E1) + elecciones abiertas | Original 2 (p = 0,036 y 0,012); convergido (1.999-3.999 réplicas, 5 semillas) 1 o 2 (IPV p = 0,041-0,057, borde). Réplica 1 por la ventana (p IPV = 0,05-0,06). Corr.: 0 (p = 0,59 y 0,06). |
| ratios-bh (0 / 2) | **Original con error** (E1 y p publicado inestable); la diferencia directa es una **elección abierta** (familia) | Original a 499: 0 con familia de 8 (p = 0,012; 0,020 → ajustado 0,08). Con 1.999-3.999 réplicas y 5 semillas el MISMO código da 2 con familia de 8 (p = 0,005-0,011), así que el 0 publicado depende del ruido. Con familia de 4 y p del original a 499: 3 (ajustados 0,04-0,048). Réplica (DGP AR(1), ventana 14): familia de 4 → 2; con familia de 8 → 0. Corr.: 0 con familia de 8 o de 14; 1 con familia de 4 (solo IPV/renta, p = 0,012). |
| ratios-p05 (3 / 2) | **Original con error** (E1) + elecciones abiertas | Original 3 (p = 0,012; 0,036; 0,020); IPV/alquiler en el borde (p = 0,034-0,045). Réplica 2: ventana de 14 (IPV/alquiler p = 0,06). Corr.: 1 (IPV/renta; tasado/alquiler p = 0,06). |
| V71-S3-R6-e_ayuda_demanda-compra-precio10a (4,365 [4,141; 8,088]) | **Original correcto** | Reproducido al bit: mediana entre las 17 CCAA de las medianas de Δp a 10 años (Andalucía 4,3654; mín. Asturias 4,1407; máx. Extremadura 8,0876). Aplica la ecuación 2 de metodo.md (Δp = s·ε_d/(ε_s+ε_d)·A(h)) y la senda del apartado 5. No es reproducible desde la ficha por omisiones (sección 6), no por error. |

Observaciones sobre R6. (a) Las ayudas dan el mismo valor en «compra» y «alquiler» por construcción (r6_propuestas.py:184-196 usa un único conjunto de extracciones; la ficha de alquiler repite 4,3654): es una simplificación, no un error, pero debe declararse. (b) La constante `SV = (6.6, 24.8)` (línea 215) es letra muerta: `main` la sobrescribe con la semivida de R4, (6,10; 10,26) trimestres. (c) Sensibilidad (aprox., misma estructura): ε_s = 0,45 en todas las CCAA, 6,0; ε_s = 0, 9,7; sin senda de ajuste, 4,5; semivida 4-40, 3,7. La cifra depende de supuestos que la ficha no lista.

## 5. ¿Cambia alguna cifra publicada, capa o conclusión?

- **Sí, cifras** (si el autor acepta E1 y E2; esta reconciliación no las cambia): V72-GSADF-ccaa-bh 7 → 0; niveles-bh 2 → 0; ratios-p05 3 → 1; ratios-bh 0 → 0 (familia de 8) o 1 (familia de 4); tipos-p05 sigue en 0. V72-GSADF-rev (14 de 14) sigue siendo cierta como «mismo método», pero el método incluye E1. Requeriría entradas en ERRATA.md, porque cambia cifras de cifras_clave.
- **Capa: no.** Todo sigue en C4, EXPLORATORIO.
- **Conclusiones:**
  - El veredicto de V72-BURBUJA («ANALIZADA, NO CONCLUYENTE») no cambia.
  - Pierde apoyo la frase «los niveles nacionales y algunas series regionales son explosivos tras BH».
  - «No hay exuberancia de los cocientes tras el ajuste múltiple» (en que se apoya K15): con E1 corregido se mantiene con familia de 8 o 14 (0), pero no con familia de 4 (1 de 4). El 0 publicado no se sostiene por sí solo: con el código sin corregir converge a 2. K15 no queda contradicho (su Q9-g es otra serie y otro cálculo), pero su apoyo se formula mejor como «depende de la familia de ajuste y del retardo del DGP».
  - Aviso: tras E1, el bootstrap elige p = 2-4 y la ADF queda en 1 retardo; es coherente (se simula el mismo estadístico), pero eleva mucho los valores críticos. Elegir o no ese diseño es una decisión del autor, no de este informe.

## 6. Lo que la ficha debería añadir

1. Retardos: el de la ADF (1, fijo) y la regla del DGP del bootstrap (BIC en muestra común, pmax = 4, o igual al de la ADF).
2. Ventana: r0 = 0,01 + 1,8/√T y si w0 cuenta observaciones de la serie o de la regresión (16 u 18 para T = 78).
3. Constante sin tendencia; derivas del bootstrap (constante estimada, residuos centrados, y inicio con los primeros Δy observados); número de réplicas, semilla por serie (SEED+500+k, orden de S) y que p = (1+#)/(B+1).
4. Series: fórmulas exactas (log de P/denominador, rebase 2015=100 irrelevante, g = 2 %, prima 3 pp, anualidad a 25 años), muestra y regla ante huecos (tramo continuo; sin interpolación; Navarra).
5. Familias de BH con su tamaño m: 8 (cocientes + tipos), 2, 4, 34. Declarar también el resultado con otras familias, y que con 499 réplicas el error típico de p es ≈ 0,01 (recuento de borde).
6. R6: s ~ U(0,05; 0,15); |ε_d| ~ U(0,3; 1,5); ε_s por rejilla A4 (unión de métodos A y B, ponderada por déficit); semivida log-uniforme entre las medianas de R4; A(10) = 1 − 2^(−40/τ); 4.000 extracciones, semilla por CCAA derivada de SEED; el mismo conjunto de extracciones sirve para compra y alquiler; y que el valor es la mediana de las 17 medianas, con mín. y máx. de las medianas.
7. La procedencia de los datos que no están en la ficha: output/v5/A4, T3, R4.

Tokens: unos 150.000.
