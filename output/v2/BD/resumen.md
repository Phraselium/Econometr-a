# BD - Descomposición por periodos con contrafactuales e intervalos (alquiler y compra)

**Nivel de evidencia global: EXPLORATORIO.** Descomposición contable de asociaciones condicionales; no hay identificación causal.
Cada fila hereda el nivel de la rama de origen (columna «Evidencia heredada»): H1 (alquiler) tuvo mejora predictiva confirmada en la
muestra sellada (BA/BV/BP aprobadas; H1 conjunta de signos EXPLORATORIA; el componente 20-34 es candidato a ASOCIACIÓN ROBUSTA sujeto a Holm-7 en BS);
H2 (compra) NO se confirmó en el sellado. La descomposición NO usa el periodo sellado (termina en 2024Q1 por la razón indicada abajo).
Cifras generadas por `src/v2/bd_run.py` (B=999, semilla 20261010); dos ejecuciones con md5 idénticos.

## Respuesta breve (EXPLORATORIO; asociaciones condicionales)
- **Alquiler desde 2014:** +7,25 [3,45; 11,26] pp; las familias medidas no lo explican (suma M1 −2,70 [−5,73; −0,17] pp) y el componente común/no explicado es 10,14 [5,57; 13,25] pp.
- **Alquiler desde 2020:** +5,66 [4,81; 6,58] pp; solo la población de 20-34 años aparece con IC>0 en M2 (0,57 [0,09; 1,04] pp, ~10 %); ~95-100 % queda en el componente común.
- **Compra (real) desde 2014:** −1,11 [−10,23; 5,70] pp (≈0); **desde 2020:** −4,50 [−10,37; −2,56] pp (caída real). Sin atribución estable entre M1 y M2.
- Contrafactuales (b) y (c) (crédito/coste de uso): efectos pequeños en alquiler; en compra solo (b) en M1 tiene IC que excluye 0 (−4,48 pp) y no se replica en M2.

## Método (qué se calcula exactamente)
- Datos: `panel_prov_q` y `nacional_q_v2` vía `v2_common.load` (49 provincias de entrenamiento). Alquiler: Δ4 ln IPC de alquiler (nominal, como BA);
  compra: Δ4 ln valor tasado REAL (deflactor nacional, como BV). Muestra 2008Q1-2024Q1 (N alquiler = 3185, compra = 3156).
  **P4 llega solo a 2024Q1**: la población de 2024Q2 está anulada (fuga del sellado corregida en holdout.build) y las familias demografía la necesitan.
- Modelos (EXPLORATORIOS), coeficientes POR PERIODO (como estimaron BA y BV; el tope catalán y el Δ4 del coste de uso nacional, globales):
  **M1** = FE de provincia y de trimestre (los efectos de tiempo recogen todo lo común: tipos, regulación nacional, expectativas y el movimiento
  común de las propias familias); **M2** = FE de provincia + dummies de trimestre del año + intercepto por periodo + Δ4 del coste de uso nacional
  (identificación solo temporal con una serie única: sin variación transversal, los EE cluster no valen; se usa el bootstrap por bloques de tiempo).
  Los coeficientes de M1/M2 son nuevos (no son los de BA/BV: otra especificación conjunta, oferta contemporánea Δ4 ln terminadas con relleno 0 y dummy
  de dato ausente —Ceuta, Melilla y 2008Q1-Q3—, y crédito provincial y tope catalán en alquiler); se informan en `coeficientes_por_periodo.csv`.
- Contribución de la familia f en el periodo P = coeficiente_{f,P} × (variación media de la familia en P), con media nacional PONDERADA POR POBLACIÓN
  de las 49 provincias, expresada como crecimiento acumulado ≈ (n_trim/4) × media del Δ4 (pp de ln; efecto de borde: ver `observado_niveles_referencia.csv`).
  Identidad: observado = Σ familias + común (efectos de tiempo + FE de provincia + dummies) + residuo.
  **Cautela de lectura de M1**: el coeficiente se identifica con diferencias entre provincias y se aplica a la media nacional de la variable; lo que en M1 no
  atribuye a las familias queda en «común», que por construcción es grande.
- IC95 %: percentiles de 999 réplicas de (i) bootstrap por bloques de provincias (cluster, remuestreo de provincias con reposición, modelo reestimado) y (ii) bootstrap
  por bloques de tiempo (bloques móviles de 4 trimestres dentro de cada periodo). La tabla da la ENVOLVENTE de ambos (`contribuciones_todas.csv` tiene cada uno por separado).
  El «observado» también tiene IC porque la media ponderada depende de las provincias/trimestres remuestreados.
- Ventanas acumuladas: «desde 2014» = P2+P3+P4 (2014Q1-2024Q1) y «desde 2020» = P3+P4 (2020Q1-2024Q1).

## Alquiler (IPC de alquiler nominal) - subida desde 2014 (P2+P3+P4)
| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |
|---|---|---|---|---|---|
| **Observado** (crecimiento acumulado, pp de ln) | 7,25 [3,45; 11,26] | 100 % | 7,25 [3,50; 11,24] | 100 % | DESCRIPTIVO |
| Suma de familias | −2,70 [−5,73; −0,17] | −37 % | −3,51 [−6,75; 0,54] | −48 % | DESCRIPTIVO |
| Demografía (20-34 + extranjera) | −3,09 [−5,96; −0,74] | −43 % | −3,32 [−6,57; −0,03] | −46 % | mixto: 20-34 candidato a ASOCIACIÓN ROBUSTA; extranjera EXPLORATORIO |
|   · pob 20-34 | −2,67 [−4,40; −1,05] | −37 % | −3,61 [−5,83; −1,15] | −50 % | ASOCIACIÓN ROBUSTA (candidato: coef. 20-34 de H1; mejora predictiva confirmada en sellado; Holm-7 pendiente en BS) |
|   · pob extranjera | −0,41 [−2,17; 1,03] | −6 % | 0,29 [−1,49; 1,50] | 4 % | EXPLORATORIO |
| Empleo (ocupados) | 0,25 [−0,05; 0,54] | 3 % | 0,08 [−0,27; 0,41] | 1 % | EXPLORATORIO |
| Crédito / coste de uso | 0,12 [−0,05; 0,34] | 2 % | −0,24 [−1,50; 0,92] | −3 % | EXPLORATORIO |
| Oferta (terminadas) | 0,03 [−0,01; 0,08] | 0 % | 0,03 [−0,02; 0,08] | 0 % | EXPLORATORIO |
| Política (tope de rentas CAT) | −0,01 [−0,18; 0,10] | −0 % | −0,06 [−0,25; 0,08] | −1 % | EXPLORATORIO (H5/tope: falló placebos y pretendencias en BP) |
| Común: efectos de tiempo + FE | 10,14 [5,57; 13,25] | 140 % | 11,69 [8,34; 14,11] | 161 % | DESCRIPTIVO |
| Residuo | −0,19 [−0,61; 0,28] | −3 % | −0,93 [−1,55; 0,04] | −13 % | DESCRIPTIVO |

## Alquiler - subida desde 2020 (P3+P4)
| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |
|---|---|---|---|---|---|
| **Observado** (crecimiento acumulado, pp de ln) | 5,66 [4,81; 6,58] | 100 % | 5,66 [4,95; 6,55] | 100 % | DESCRIPTIVO |
| Suma de familias | −0,00 [−1,93; 1,28] | −0 % | 0,66 [−0,78; 1,89] | 12 % | DESCRIPTIVO |
| Demografía (20-34 + extranjera) | −0,05 [−1,93; 1,21] | −1 % | 0,83 [−0,81; 1,63] | 15 % | mixto: 20-34 candidato a ASOCIACIÓN ROBUSTA; extranjera EXPLORATORIO |
|   · pob 20-34 | 0,34 [−0,11; 0,85] | 6 % | 0,57 [0,09; 1,04] | 10 % | ASOCIACIÓN ROBUSTA (candidato: coef. 20-34 de H1; mejora predictiva confirmada en sellado; Holm-7 pendiente en BS) |
|   · pob extranjera | −0,39 [−2,15; 0,82] | −7 % | 0,26 [−1,26; 1,16] | 5 % | EXPLORATORIO |
| Empleo (ocupados) | 0,08 [−0,12; 0,30] | 1 % | −0,00 [−0,20; 0,22] | −0 % | EXPLORATORIO |
| Crédito / coste de uso | −0,03 [−0,11; 0,07] | −0 % | −0,11 [−0,74; 0,52] | −2 % | EXPLORATORIO |
| Oferta (terminadas) | 0,01 [−0,01; 0,05] | 0 % | 0,01 [−0,01; 0,04] | 0 % | EXPLORATORIO |
| Política (tope de rentas CAT) | −0,01 [−0,18; 0,10] | −0 % | −0,06 [−0,25; 0,08] | −1 % | EXPLORATORIO (H5/tope: falló placebos y pretendencias en BP) |
| Común: efectos de tiempo + FE | 5,79 [4,16; 7,76] | 102 % | 5,36 [3,92; 7,19] | 95 % | DESCRIPTIVO |
| Residuo | −0,12 [−0,54; 0,29] | −2 % | −0,36 [−0,74; 0,17] | −6 % | DESCRIPTIVO |

**Lectura (asociación, no causalidad).**
- Desde 2014 el IPC de alquiler acumula 7,25 [3,45; 11,26] pp. Con efectos de tiempo (M1) las familias medidas suman
  −2,70 [−5,73; −0,17] pp: casi todo el aumento queda en el componente común (10,14 [5,57; 13,25] pp), es decir,
  en lo que se mueve igual en todas las provincias y no se explica con las variables disponibles (tipos, regulación nacional, expectativas, inflación...).
- La demografía contribuye NEGATIVAMENTE en 2014-2019 (P2: población de 20-34 años en descenso, coeficiente positivo): −3,02 [−4,78; −1,31] pp en M1.
  No explica la subida; el signo es el de la composición, no el de una asociación nueva.
- Desde 2020 el único componente con IC que excluye el 0 y signo positivo es la población de 20-34 en M2: 0,57 [0,09; 1,04] pp
  (10 % del observado 5,66 [4,95; 6,55]); en M1 el efecto es
  0,34 [−0,11; 0,85] (IC incluye 0). La población extranjera, el empleo, la oferta, el crédito y el tope catalán no se distinguen de 0 (IC incluyen el 0).
- Lo no explicado domina: en M1 el componente común es 102 % del crecimiento desde 2020; en M2 95 %.

## Compra (valor tasado REAL) - subida desde 2014 (P2+P3+P4)
| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |
|---|---|---|---|---|---|
| **Observado** (crecimiento acumulado, pp de ln) | −1,11 [−10,23; 5,70] | 100 % | −1,11 [−10,48; 6,04] | 100 % | DESCRIPTIVO |
| Suma de familias | −5,85 [−13,80; 0,39] | 529 % | −8,29 [−21,69; −0,25] | 749 % | DESCRIPTIVO |
| Demografía (20-34 + extranjera) | −6,50 [−15,48; −0,16] | 588 % | −7,53 [−19,75; −2,62] | 681 % | EXPLORATORIO (H2 no confirmada en el sellado) |
|   · pob 20-34 | −7,46 [−14,84; −3,17] | 675 % | −3,46 [−12,19; 1,34] | 313 % | EXPLORATORIO (H2 no confirmada en el sellado) |
|   · pob extranjera | 0,96 [−3,20; 5,19] | −87 % | −4,08 [−10,46; −0,84] | 368 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Empleo (ocupados) | 0,50 [−0,43; 1,61] | −46 % | 1,67 [0,48; 2,96] | −151 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Crédito / coste de uso | 0,06 [−2,04; 1,97] | −5 % | −2,52 [−5,71; 2,26] | 228 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Oferta (terminadas) | 0,09 [−0,07; 0,55] | −8 % | 0,10 [−0,08; 0,59] | −9 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Común: efectos de tiempo + FE | 2,06 [−9,59; 12,27] | −187 % | 4,50 [−8,14; 19,14] | −407 % | DESCRIPTIVO |
| Residuo | 2,68 [0,70; 4,45] | −242 % | 2,68 [0,41; 4,92] | −242 % | DESCRIPTIVO |

## Compra - desde 2020 (P3+P4)
| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |
|---|---|---|---|---|---|
| **Observado** (crecimiento acumulado, pp de ln) | −4,50 [−10,37; −2,56] | 100 % | −4,50 [−10,30; −2,33] | 100 % | DESCRIPTIVO |
| Suma de familias | 1,94 [−1,54; 4,73] | −43 % | −5,84 [−10,21; 0,75] | 130 % | DESCRIPTIVO |
| Demografía (20-34 + extranjera) | 1,19 [−2,28; 4,13] | −26 % | −5,27 [−8,49; −0,87] | 117 % | EXPLORATORIO (H2 no confirmada en el sellado) |
|   · pob 20-34 | 0,16 [−1,86; 1,41] | −4 % | −1,08 [−3,34; 0,70] | 24 % | EXPLORATORIO (H2 no confirmada en el sellado) |
|   · pob extranjera | 1,03 [−2,46; 4,04] | −23 % | −4,19 [−7,40; −0,57] | 93 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Empleo (ocupados) | 0,45 [−0,02; 0,99] | −10 % | 0,77 [0,13; 1,44] | −17 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Crédito / coste de uso | 0,33 [−0,99; 1,17] | −7 % | −1,32 [−2,86; 1,27] | 29 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Oferta (terminadas) | −0,02 [−0,11; 0,05] | 0 % | −0,01 [−0,11; 0,06] | 0 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Común: efectos de tiempo + FE | −5,73 [−12,08; −1,95] | 127 % | 1,66 [−8,43; 5,44] | −37 % | DESCRIPTIVO |
| Residuo | −0,71 [−2,00; 0,56] | 16 % | −0,32 [−1,75; 1,01] | 7 % | DESCRIPTIVO |

**Lectura (asociación, no causalidad).**
- En términos REALES el valor tasado no «sube» en el conjunto 2014-2024Q1: observado −1,11 [−10,23; 5,70] pp (recuperación en P2, caída real en P3-P4: −4,50 [−10,37; −2,56] pp desde 2020 por la inflación del deflactor).
  Por eso la pregunta «qué explica la subida» se refiere al nominal solo de forma indirecta; aquí se descompone el real.
- Ninguna familia explica de forma robusta la evolución desde 2020: en M1 las familias suman 1,94 [−1,54; 4,73] pp y el común −5,73 [−12,08; −1,95] pp.
  En M2 la demografía (sobre todo extranjera: −4,19 [−7,40; −0,57] pp) sale con signo negativo en P3-P4 porque los coeficientes por periodo de la población cambian de signo
  (`coeficientes_por_periodo.csv`); no se interpreta, la inestabilidad entre M1 y M2 indica que no hay una atribución estable.
- El crédito/coste de uso pesa en P1 (−6,26 [−10,31; −2,34] pp en M1) y es indistinguible de 0 desde 2014 en M1.

## Contrafactuales (EXPLORATORIOS y PARCIALES)
**Advertencia:** son ejercicios ceteris paribus sobre las variables del modelo: se modifican solo esas variables con los coeficientes estimados; no hay equilibrio general
(oferta, expectativas, migración y precios se retroalimentan), la identificación no es causal y M1 solo recoge el canal diferencial entre provincias (coste de uso
únicamente vía exposición hipotecaria; en alquiler M1 el canal de coste de uso es 0 por construcción). M2 añade el canal temporal nacional, pero con una serie única (IC por bloques de tiempo).
Efecto = valor contrafactual − observado (pp acumulados de ln). Si «sin variación» elimina una caída observada, el efecto es positivo.
| Mercado | Modelo | Escenario | Efecto P2-P4 acumulado (pp) | Efecto P4 (pp) | Observado P4 (pp) |
|---|---|---|---|---|---|
| alquiler | M1 | (a) 20-34 y extranjera sin variación desde 2014Q1 | 3,09 [0,74; 5,96] | −0,25 [−1,33; 1,09] | 3,93 |
| alquiler | M1 | (a1) solo 20-34 sin variación | 2,67 [1,05; 4,40] | −0,31 [−0,73; 0,15] | 3,93 |
| alquiler | M1 | (a2) solo extranjera sin variación | 0,41 [−1,03; 2,17] | 0,06 [−0,93; 1,34] | 3,93 |
| alquiler | M1 | (a3) ambas: se elimina solo el crecimiento positivo | −0,03 [−1,55; 2,21] | −0,28 [−1,39; 1,07] | 3,93 |
| alquiler | M1 | (b) crédito y coste de uso congelados en 2013Q4 | −0,15 [−0,35; 0,06] | 0,00 [−0,08; 0,10] | 3,93 |
| alquiler | M1 | (c) coste de uso de 2021Q4 durante P4 | (solo P4) | 0,00 [0,00; 0,00] | 3,93 |
| alquiler | M2 | (a) 20-34 y extranjera sin variación desde 2014Q1 | 3,32 [0,03; 6,57] | −0,86 [−1,46; 0,54] | 3,93 |
| alquiler | M2 | (a1) solo 20-34 sin variación | 3,61 [1,15; 5,83] | −0,53 [−0,95; −0,12] | 3,93 |
| alquiler | M2 | (a2) solo extranjera sin variación | −0,29 [−1,50; 1,49] | −0,33 [−0,96; 0,97] | 3,93 |
| alquiler | M2 | (a3) ambas: se elimina solo el crecimiento positivo | −1,92 [−3,14; 0,06] | −0,92 [−1,53; 0,53] | 3,93 |
| alquiler | M2 | (b) crédito y coste de uso congelados en 2013Q4 | 0,24 [−0,88; 1,47] | 0,03 [−0,43; 0,57] | 3,93 |
| alquiler | M2 | (c) coste de uso de 2021Q4 durante P4 | (solo P4) | 0,04 [−0,26; 0,37] | 3,93 |
| compra | M1 | (a) 20-34 y extranjera sin variación desde 2014Q1 | 6,50 [0,16; 15,48] | −0,74 [−2,86; 2,10] | −1,88 |
| compra | M1 | (a1) solo 20-34 sin variación | 7,46 [3,17; 14,84] | −0,15 [−1,44; 1,76] | −1,88 |
| compra | M1 | (a2) solo extranjera sin variación | −0,96 [−5,19; 3,20] | −0,59 [−2,73; 1,59] | −1,88 |
| compra | M1 | (a3) ambas: se elimina solo el crecimiento positivo | −0,75 [−5,22; 3,36] | −0,76 [−2,96; 2,14] | −1,88 |
| compra | M1 | (b) crédito y coste de uso congelados en 2013Q4 | −4,48 [−8,28; −0,91] | −0,68 [−2,56; 1,19] | −1,88 |
| compra | M1 | (c) coste de uso de 2021Q4 durante P4 | (solo P4) | −0,14 [−0,55; 0,27] | −1,88 |
| compra | M2 | (a) 20-34 y extranjera sin variación desde 2014Q1 | 7,53 [2,62; 19,75] | 4,72 [0,63; 7,32] | −1,88 |
| compra | M2 | (a1) solo 20-34 sin variación | 3,46 [−1,34; 12,19] | 1,05 [−0,67; 3,20] | −1,88 |
| compra | M2 | (a2) solo extranjera sin variación | 4,08 [0,84; 10,46] | 3,67 [0,42; 7,06] | −1,88 |
| compra | M2 | (a3) ambas: se elimina solo el crecimiento positivo | 3,42 [−0,72; 11,34] | 4,83 [0,59; 7,46] | −1,88 |
| compra | M2 | (b) crédito y coste de uso congelados en 2013Q4 | −2,96 [−7,02; 1,53] | 0,96 [−1,17; 3,30] | −1,88 |
| compra | M2 | (c) coste de uso de 2021Q4 durante P4 | (solo P4) | 0,59 [−0,45; 1,53] | −1,88 |

- (a) «Sin crecimiento» de 20-34 y extranjera desde 2014: la población de 20-34 años CAYÓ en P2, así que fijarla (Δ=0) sube el alquiler contrafactual
  (M1: 2,67 pp); eliminar solo el crecimiento positivo (a3) apenas cambia nada.
  En P4 (donde la población joven crece) quitar su variación resta −0,53 pp en M2 y −0,31 pp en M1 sobre un observado de 3,93 pp.
- (b) y (c), alquiler: efectos pequeños (décimas de pp) y con IC que incluyen 0; en compra, congelar crédito y coste de uso en 2013Q4 reduce el real acumulado en M1 pero el IC en M2 incluye 0.
  (c): con el coste de uso de 2021Q4 durante P4 el efecto es de décimas de pp con IC que incluye 0 en M2 (en M1 es 0 por construcción en alquiler y −0,14 [−0,55; 0,27] en compra):
  la subida de tipos de 2022 no deja una señal detectable en estos modelos (ausencia de señal, no evidencia de efecto nulo).
- Compra, (a): M1 y M2 discrepan (P4: M1 −0,74 pp, M2 4,72 pp): no hay contrafactual demográfico estable para la compra.

## Nacional: precio real con el ECM v1 real (EXPLORATORIO)
ECM v1 real (v1: `output/f2/ecuacion_real.csv`) reestimado con datos de entrenamiento (2008Q2-2024Q2; LP N=68, CP N=65; el P1 de CP empieza en 2008Q2).
IC95: bootstrap de residuos por bloques (4), regresores fijos, B=999 (el desequilibrio de CP usa el ECT puntual, no reestimado). Identidad de largo plazo (Δy = b·Δx + estacional + Δ desequilibrio):
| Periodo | Componente | pp [IC95 %] | % obs. |
|---|---|---|---|
| P1 | empleo (ocupados) | −31,0 [−44,8; −15,1] | 66 % |
| P1 | tipo hipotecario real | 0,3 [−0,5; 0,9] | −1 % |
| P1 | permisos (t-4) | −11,9 [−24,7; −1,0] | 25 % |
| P1 | costes de construcción reales | −5,5 [−11,2; 0,1] | 12 % |
| P1 | desequilibrio (Δ ect) | 1,2 [−6,3; 8,7] | −3 % |
| P1 | observado | −47,0 [−47,0; −47,0] | 100 % |
| P2 | empleo (ocupados) | 25,0 [12,1; 36,0] | 116 % |
| P2 | tipo hipotecario real | −1,8 [−6,4; 3,3] | −8 % |
| P2 | permisos (t-4) | 2,1 [0,2; 4,4] | 10 % |
| P2 | costes de construcción reales | 2,0 [−0,0; 4,1] | 9 % |
| P2 | desequilibrio (Δ ect) | −5,8 [−12,3; 1,7] | −27 % |
| P2 | observado | 21,6 [21,6; 21,6] | 100 % |
| P3 | empleo (ocupados) | 2,5 [1,2; 3,6] | 103 % |
| P3 | tipo hipotecario real | −2,8 [−10,1; 5,2] | −114 % |
| P3 | permisos (t-4) | −2,7 [−5,5; −0,2] | −110 % |
| P3 | costes de construcción reales | −4,7 [−9,6; 0,1] | −195 % |
| P3 | desequilibrio (Δ ect) | 10,1 [5,1; 14,2] | 417 % |
| P3 | observado | 2,4 [2,4; 2,4] | 100 % |
| P4 | empleo (ocupados) | 11,0 [5,3; 15,8] | 231 % |
| P4 | tipo hipotecario real | 2,7 [−5,2; 10,0] | 58 % |
| P4 | permisos (t-4) | 5,0 [0,4; 10,3] | 105 % |
| P4 | costes de construcción reales | −0,2 [−0,4; 0,0] | −4 % |
| P4 | desequilibrio (Δ ect) | −10,7 [−20,1; −0,3] | −226 % |
| P4 | observado | 4,8 [4,8; 4,8] | 100 % |

Corto plazo (suma de Δy_t = Σ coef·x; exacta):
| Periodo | Componente | pp [IC95 %] | % obs. |
|---|---|---|---|
| P1 | desequilibrio (ect t-1) | −10,6 [−17,8; −3,3] | 23 % |
| P1 | constante + estacionales | −5,0 [−12,1; 3,0] | 11 % |
| P1 | empleo (Δ ocupados t-1) | −10,1 [−14,9; −4,9] | 22 % |
| P1 | tipos (Δ tipo hip. t-1) | 2,6 [−0,0; 5,0] | −6 % |
| P1 | renta real (Δ) | −0,9 [−1,8; 0,1] | 2 % |
| P1 | inercia (Δy t-4) | −9,4 [−16,7; −3,0] | 21 % |
| P1 | crédito nuevo (Δ) | −6,2 [−8,8; −3,5] | 13 % |
| P1 | residuo | −6,3 [−16,3; 3,3] | 14 % |
| P1 | observado | −45,9 [−45,9; −45,9] | 100 % |
| P2 | desequilibrio (ect t-1) | 5,9 [1,9; 9,9] | 27 % |
| P2 | constante + estacionales | −4,9 [−12,4; 3,4] | −23 % |
| P2 | empleo (Δ ocupados t-1) | 7,8 [3,8; 11,5] | 36 % |
| P2 | tipos (Δ tipo hip. t-1) | 1,1 [−0,0; 2,1] | 5 % |
| P2 | renta real (Δ) | 2,2 [−0,2; 4,3] | 10 % |
| P2 | inercia (Δy t-4) | 2,7 [0,8; 4,8] | 12 % |
| P2 | crédito nuevo (Δ) | 3,0 [1,7; 4,3] | 14 % |
| P2 | residuo | 3,7 [−5,5; 13,3] | 17 % |
| P2 | observado | 21,6 [21,6; 21,6] | 100 % |
| P3 | desequilibrio (ect t-1) | −0,5 [−0,8; −0,1] | −19 % |
| P3 | constante + estacionales | −1,6 [−4,1; 1,1] | −67 % |
| P3 | empleo (Δ ocupados t-1) | 0,6 [0,3; 0,9] | 26 % |
| P3 | tipos (Δ tipo hip. t-1) | 0,5 [−0,0; 1,0] | 21 % |
| P3 | renta real (Δ) | −0,0 [−0,0; 0,0] | −1 % |
| P3 | inercia (Δy t-4) | 0,6 [0,2; 1,0] | 24 % |
| P3 | crédito nuevo (Δ) | 1,0 [0,6; 1,4] | 41 % |
| P3 | residuo | 1,8 [−1,0; 4,5] | 75 % |
| P3 | observado | 2,4 [2,4; 2,4] | 100 % |
| P4 | desequilibrio (ect t-1) | 1,8 [0,6; 3,0] | 38 % |
| P4 | constante + estacionales | −0,7 [−4,1; 2,8] | −15 % |
| P4 | empleo (Δ ocupados t-1) | 3,0 [1,5; 4,5] | 64 % |
| P4 | tipos (Δ tipo hip. t-1) | −2,3 [−4,4; 0,0] | −48 % |
| P4 | renta real (Δ) | 1,0 [−0,1; 1,9] | 20 % |
| P4 | inercia (Δy t-4) | 0,7 [0,2; 1,2] | 14 % |
| P4 | crédito nuevo (Δ) | 0,5 [0,3; 0,7] | 11 % |
| P4 | residuo | 0,8 [−3,8; 5,5] | 16 % |
| P4 | observado | 4,8 [4,8; 4,8] | 100 % |

Lectura: en 2014-2019 (P2) el empleo (7,8 [3,8; 11,5] pp en CP) y el desequilibrio (5,9 [1,9; 9,9] pp) concentran buena parte del aumento real;
en P4 (2022Q1-2024Q2) los tipos restan (−2,3 [−4,4; 0,0] pp, IC en el límite del 0) y el desequilibrio de largo plazo se cierra (−10,7 [−20,1; −0,3] pp),
mientras el empleo aporta 11,0 [5,3; 15,8] pp. El IC del tipo real de LP incluye 0 en todos los periodos (en v1 también era no significativo, igual que permisos; solo empleo y costes lo eran).
El DOLS usa pocos datos, la estacionalidad del LP depende de los trimestres de inicio y fin, y el «residuo» de CP no es independiente de la elección de variables de v1 (elegidas por R² ajustado en la misma muestra).

## Turismo (VUT; solo ventana 2021Q3-2024Q1; N temporal = 6)
Contribución en P4 (6 trimestres): 0,02 pp [−0,06; 0,11] sobre un crecimiento observado en la ventana de 2,12 pp. No se distingue de 0; no comparable con el resto (otra ventana y coeficiente global). `turismo_*.csv`.

## Qué NO se puede afirmar
- Nada causal: ni «la demografía/el crédito/los tipos causaron» ni que los contrafactuales sean lo que habría ocurrido. Son aritmética de coeficientes de asociación.
- Que las familias medidas expliquen la subida desde 2014 o desde 2020: la mayor parte queda en el componente común/no explicado.
- Que la subida de tipos de 2022 no importara: con una serie nacional única y 9-10 trimestres en P4, M1/M2 no tienen potencia para detectarla (no es evidencia de efecto nulo).
- Efectos de política (tope catalán de 2020-22, Ley 12/2023, zonas tensionadas 2024: sellada), inversores y no residentes (sin datos provinciales).
- Nada sobre 2024Q2 en adelante (2024Q2 queda fuera por la población anulada; el sellado no se usa).
- Estabilidad: M1 y M2 difieren en tamaño y a veces en signo (p. ej. compra, demografía); los coeficientes por periodo con 8-24 trimestres son imprecisos. Poblaciones intra-anuales interpoladas (T2-T4) y coste de uso aproximado (sin impuestos ni prima de riesgo).
- Las medidas de «% del observado» son inestables cuando el observado es pequeño (alquiler P2, compra P2-P4).

## Archivos
`tabla_resumen.csv` (periodo × familia × mercado, con M1 y M2), `contribuciones_todas.csv`, `coeficientes_por_periodo.csv`, `contrafactuales.csv`, `nacional_*.csv`, `turismo_*.csv`,
`observado_niveles_referencia.csv`, `registro.csv`, `resultado.json`, `figuras/`.
