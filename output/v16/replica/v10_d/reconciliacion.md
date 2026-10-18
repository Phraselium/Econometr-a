# Reconciliación original (V8) frente a réplica ciega (lote d): cuatro cifras

Fecha: 2026-10-18. Alcance: solo lectura de src/v8, docs/v8, output/v8 y data/processed/v8. Las copias y las ejecuciones están en
/tmp/claude-0/-home-user-Econometr-a/468da938-3e2d-5fba-ac52-e16a4175b9ac/scratchpad (orig_qna.py, orig_bde.py, var_qna.py, var_pf.py, var_dom.py, var_m1.py, var_m1b.py; M1 completo en m1out/). No se tocó data/sealed ni se escribió en output/ salvo este fichero.
Comprobación de partida: la ejecución de una copia de m1_factor_comun.py (--salida en /tmp) reproduce al decimal V8-H8-9-est y V8-M1-cuota-c-P5; la copia de M2 (V3, clave 10) reproduce 9,516 (media ponderada de determinista + no_identificados). El original es determinista.

## Resumen de veredictos

| Cifra | Veredicto | Primera diferencia |
|---|---|---|
| V8-H8-9-est | **Réplica con error**; original correcto (etiqueta de periodo errónea en F6) | La réplica usa `p_tasado` (empieza en 2007T1, hueco de Navarra 2015T1-2018T4) en lugar de `valor_tasado_ccaa` |
| V8-M1-cuota-c-P5 | **Elecciones abiertas** (original correcto) | Longitud del bloque: original L=4; réplica L=8 |
| V8-QNA-pp-c-P5 | **Elecciones abiertas + réplica fuera de la ficha**; original conforme a la ficha, pero frágil | Estadístico (media frente a mediana), banda (suma de límites frente a cuantiles de la suma), pesos ARW y serie del tipo |
| V8-VOTOS-c-P5 | **Réplica con error** (en dominancia); el 2 del original depende de una decisión (Y10) que no está en desviaciones.md | Transformación de la variable de crédito y tipos y signo de su contribución parcial |

## 1. V8-H8-9-est (0,5976 [0,135; 0,858] frente a 0,534 [0,089; 0,822])

**Original** (m1_factor_comun.py:169, 251-264, 62-64): Xc = interanual log×100 de `valor_tasado_ccaa`/IPC general, 17 CCAA completas desde 1996T1 (`dropna` no quita nada). `comun` = Xc ∩ g_EA19 = 2006T1-2026T2, N = 82. PC1 sobre Z=Xc[comun], re-estimado en cada réplica; bloques circulares L=8, B=999, rng SEED+2; IC95 = percentiles 2,5/97,5.
**Réplica** (v10_d.py:29-37, 62-68): usa `p_tasado`. Esa columna coincide con `valor_tasado_ccaa` donde existe (cociente 1,0), pero empieza en 2007T1 y Navarra no tiene 2015T1-2018T4. La réplica interpola Navarra y trunca la muestra a T=74 (2008T1-2026T2), con B=2000 y semilla SEED.
**Ficha**: desviaciones.md l.23 fija «valor tasado real por CCAA (cubre desde 1996T1)» y l.24 fija «2006T1-2026T2», con L=8. Con `p_tasado` esa ventana es imposible (el interanual empieza en 2008T1): la réplica incumple la ficha, no la deja abierta.
**Cuantificación**: la copia de la réplica con solo `valor_tasado_ccaa` da 0,5976 [0,1456; 0,8542] con su B/semilla y 0,5976 [0,1350; 0,8578] con B=999 y semilla SEED+2, es decir, el original exacto. Nada de lo demás (L, bootstrap, estandarización) importa.
**Error en el original (etiqueta, no cifra)**: src/v8/f6_hechos.py:169-170 rotula el periodo como «1999-último dato»; el real es 2006T1-2026T2 (N=82; el propio resumen de M1 dice «2006T1+»). Corrección mínima: sustituir por «2006T1-2026T2» en ambas líneas (también afecta a V8-H8-9-pholm).

## 2. V8-M1-cuota-c-P5 (92,79 [86,65; 94,92] frente a 92,79 [85,71; 94,93])

**Original** (m1_factor_comun.py:197, 203-207, 179): PCA estandarizado dentro de P5 (T=16, N=17); bloque `L = max(2, min(4, T//3))` = 4; B=999; rng único SEED+1 compartido por todas las series y periodos; banda 68 % = percentiles 16/84.
**Réplica** (v10_d.py:83-91): mismo estimador puntual (92,793), pero L=8 (copiado de H8-9), B=2000, rng propio.
**Ficha**: l.23 dice «bootstrap por bloques circulares de filas» sin longitud ni B ni generador. L=8 es de H8-9 (l.24), no de H8-8.
**Cuantificación** (copia de la réplica, 8 semillas, B=999): con L=4 el mínimo cae en 86,16-87,29 (media 86,75; el original, 86,65, está dentro); con L=8, 85,71-85,93 (media 85,75). El máximo no depende de L (94,7-95,1). La discrepancia de 1,1 % del mínimo es efecto de la longitud del bloque, no ruido de semilla. Ninguna de las dos es un error.

## 3. V8-QNA-pp-c-P5 (9,52 [−14,56; 24,14] frente a 4,32 [−6,61; 15,96])

**Original**: M2 V3 (m2_svar.py:94-96, construir, procesar; signos.py:104-186). Pesos ARW por sorteo (`peso`; ESS 657 de 708 aceptadas), `i` = `tipo_hip_bce` (con respaldo en `tipo_hip_bde`), λ por GLP (0,374). F5 (f5_atribucion.py:168-184): punto = suma de las medias posteriores de `determinista` (5,356) y `no_identificados` (4,160) = 9,516; banda = suma de los límites de las dos bandas del 68 % (−8,82 − 5,74; 11,81 + 12,33).
**Réplica** (v10_d.py:242-281): BVAR propio, rotación sin pesos, `i` = `tipo_hip_bde`, mediana de la suma de sorteos y cuantiles de la suma (4,32 [−6,61; 15,96]).
**Ficha**: desviaciones.md l.42(3) fija «cuota no atribuida = (determinista + no_identificados)/ΔY» y que la banda se aproxima «por la suma de los límites de las dos bandas». Decisiones Y10 (l.56): la contribución puntual es la media posterior. Por tanto, el original sigue la ficha en estadístico y banda; la réplica no (lo reconoce en su diagnóstico). La ficha no fija: serie del tipo, pesos ARW (F3 muestra que sin pesos E[Q²] falla en 0,21), GLP, número de sorteos.
**Primeras diferencias y efecto** (ΔY = 18,42 pp en ambos):
1. Estadístico: sobre el mismo posterior del original, media ponderada de la suma = 9,52, mediana ponderada = 3,42 (cola derecha pesada: determinista, media 5,36, mediana 0,93). Mediana del original (3,42) y de la réplica (4,32) concuerdan dentro de la banda; las medias no.
2. Banda: cuantiles exactos de la suma en el original = [−7,76; 16,44] (ponderados), frente al publicado [−14,56; 24,14] por suma de límites (el doble de ancho; conservador como declara l.42(3)). Aplicada la regla de la ficha a la réplica: [−13,33; 22,79].
3. Serie del tipo: en la réplica, `tipo_hip_bce` en vez de `bde` sube la media de 4,30 a 6,13. En el original, `bde` en vez de `bce` sube la media de 9,52 a 20,67 (mediana sin ponderar estable, 3,5). No hay ninguna cifra publicada de sensibilidad a esta elección.
4. Pesos ARW: en el original, quitarlos cambia la media de 9,52 a 11,93. La réplica no los usa y por tanto no muestrea el objetivo validado en F3.
Queda una brecha de media (6,1 réplica con `bce` frente a 9,5) que no se atribuye a un solo paso (prior/GLP, pesos, sorteos); las bandas por componente sí concuerdan (determinista réplica [−7,9; 11,8] frente a original [−8,8; 11,8]).
**Veredicto**: sin error de código en el original. Hay que declarar mejor: (a) la cifra publicada es una media sobre colas pesadas, con mediana 3,4; (b) la banda es aproximada por suma de límites (el rótulo «aproximada» está solo en la nota de F5, no en f6_hechos.py:109-113); (c) depende de la serie del tipo.

## 4. V8-VOTOS-c-P5 (2 frente a 1)

**Original** (f5_atribucion.py:91-103, 106-111, 114-128, 131-136, 187-215): svar_hd vota por el mayor P(f*) (crédito y tipos, 0,297; por media sería empleo_renta, 7,16); dominancia (M6) vota crédito y tipos; lpiv se abstiene (−11,3 pp no supera 7,2); contabilidad vota demografía. Recuento: crédito y tipos 2, demografía 1. Máximo 2 de 4: no designado (capa C4).
**Réplica** (v10_d.py:284-335, hard-code `"valor": 1`): su dominancia vota demografía porque transforma el crédito y tipos como −Δ4(tipo real) y toma el producto β·media(Δx), con signo negativo.
**Ficha**: desviaciones.md l.30 fija como principal de la familia el «tipo hipotecario real» (en nivel) y l.39 fija la contribución parcial de las variables en nivel como β·(media del periodo − media histórica). La réplica incumple ambas.
**Cuantificación** (copia de v10_d.py con esas dos reglas): R²=0,988 (original 0,988), cuota LMG de crédito y tipos 0,111 (0,113), mismo ranking (europeo > turismo > empleo > crédito y tipos); contribución parcial de crédito y tipos +1,11; vota crédito y tipos. Con svar_hd (P(f*) de la réplica: crédito y tipos 0,288; original 0,297) suman 2, igual que el original. La réplica no cubre lpiv ni contabilidad.
**Elección abierta con efecto**: el voto de svar_hd sigue Y10 (decisiones.md l.57: P(f*), fijada antes de F5), que modifica R2 (revision_F4.md l.423: argmax de la media) y no está en desviaciones.md. Con la lectura literal de R2 (media) el original daría empleo_renta, y el recuento sería 1 (no 2). Ni en uno ni en otro caso hay designación.

## 5. ¿Cambia alguna cifra o capa publicada?

No. Ningún valor de cifras_clave debe cambiar ni ninguna capa (H8-9 y M1 siguen en C4; QNA en C3s; VOTOS en C4; la regla de §9 sigue en «no designado»). Cambios de texto recomendados (decide el autor si van a ERRATA.md): periodo de H8-9 y H8-9-pholm en f6_hechos.py:169-170; rótulo «banda aproximada (suma de límites)» y «media posterior (mediana 3,4)» en QNA-pp (f6_hechos.py:109-113); nota de que el 2 de VOTOS depende de Y10.

## 6. Lo que la ficha debería añadir para ser reproducible

- Columna exacta de precio por CCAA (`valor_tasado_ccaa`) y su ventana; tratamiento de huecos (ninguno en esa columna).
- Longitud de bloque de las cuotas de H8-8 (regla `max(2, min(4, T//3))`), B, y generador/orden de uso del rng.
- Serie `i` de M2 (`tipo_hip_bce` con respaldo `bde`), muestra 2004T2-2026T1, λ por GLP con α, ψ y rejilla, D, M, objetivo ESS, y el uso de pesos ARW.
- Estadístico de la cuota no atribuida (media), regla de banda (suma de límites) y rótulo «aproximada»; la mediana como cifra acompañante.
- Voto de svar_hd (Y10: P(f*)) dentro de desviaciones.md; variable de crédito y tipos en nivel y fórmula de contribución parcial; orden de las series, B y bloque del LMG; reglas de lpiv (horizontes, controles, instrumento) y de contabilidad.
