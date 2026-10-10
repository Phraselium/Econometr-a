# BD - Descomposición por periodos con contrafactuales e intervalos (alquiler y compra)

**Nivel de evidencia global: EXPLORATORIO.** Descomposición contable de asociaciones condicionales; no hay identificación causal.
Cada fila lleva el nivel de la rama de origen (columna «Evidencia heredada»): H1 (alquiler) tuvo mejora predictiva confirmada en la
muestra sellada, pero Holm-7 ya se ejecutó (output/v2/BS/holm7.csv, docs/v2/decisiones.md) y ninguna confirmatoria sobrevive; el componente 20-34 queda
a decisión de BS y aquí es EXPLORATORIO (además la contribución reestimada aquí es otra especificación). H2 (compra) NO se confirmó en el sellado.
La descomposición NO usa el periodo sellado (termina en 2024Q1 por la razón indicada abajo).
Cifras generadas por `src/v2/bd_run.py` (B=49, semilla 20261010); dos ejecuciones con md5 idénticos.

## Respuesta breve (EXPLORATORIO; asociaciones condicionales)
- **Alquiler desde 2014:** +7,69 [3,86; 10,80] pp; las familias medidas no lo explican (suma M1 −4,20 [−10,92; 0,51] pp) y el componente común/no explicado es 11,70 [5,32; 19,43] pp.
- **Alquiler desde 2020:** +6,38 [4,70; 7,20] pp; ninguna familia se distingue de 0 en M1 y M2 a la vez; ~95-100 % queda en el componente común.
- **Compra (real) desde 2014:** −9,53 [−22,26; −3,33] pp (≈0); **desde 2020:** −5,03 [−11,87; −2,31] pp (caída real). Sin atribución estable entre M1 y M2.
- Contrafactuales: efectos pequeños y con IC que incluyen 0 salvo los listados como no robustos abajo.

## Método (qué se calcula exactamente)
- Datos: `panel_prov_q` y `nacional_q_v2` vía `v2_common.load` (49 provincias de entrenamiento). Alquiler: Δ4 ln IPC de alquiler (nominal, como BA);
  compra: Δ4 ln valor tasado REAL (deflactor nacional, como BV). Muestra 2008Q1-2024Q1 (N alquiler = 780, compra = 780).
  **P4 llega solo a 2024Q1**: la población de 2024Q2 está anulada (fuga del sellado corregida en holdout.build) y las familias demografía la necesitan.
- Modelos (EXPLORATORIOS), coeficientes POR PERIODO (como estimaron BA y BV; el tope catalán y el Δ4 del coste de uso nacional, globales):
  **M1** = FE de provincia y de trimestre (los efectos de tiempo recogen lo común que las familias, con b·x̄ aplicado a la media nacional, no explican:
  tipos, regulación nacional, expectativas, inflación...); **M2** = FE de provincia + dummies de trimestre del año + intercepto por periodo + Δ4 del coste de uso nacional
  (identificación solo temporal con una serie única: sin variación transversal, los EE cluster no valen; se usa el bootstrap por bloques de tiempo).
  Los coeficientes de M1/M2 son nuevos (no son los de BA/BV: otra especificación conjunta, oferta contemporánea Δ4 ln terminadas con relleno 0 y dummy
  de dato ausente —Ceuta, Melilla y 2008Q1-Q3—, y crédito provincial y tope catalán en alquiler); se informan en `coeficientes_por_periodo.csv`.
- Contribución de la familia f en el periodo P = coeficiente_{f,P} × (variación media de la familia en P), con media nacional PONDERADA POR POBLACIÓN
  de las 49 provincias, expresada como crecimiento acumulado ≈ (n_trim/4) × media del Δ4 (pp de ln; efecto de borde: ver `observado_niveles_referencia.csv`).
  Identidad: observado = Σ familias + común (efectos de tiempo + FE de provincia + dummies) + residuo.
  **Cautela de lectura de M1**: el coeficiente se identifica con diferencias entre provincias y se aplica a la media nacional de la variable; el «común» es el resto
  (en alquiler supera el 100 % desde 2014 porque la demografía aporta en negativo).
- Estimación MCO SIN ponderar; solo la agregación (medias por trimestre y contribuciones) pondera por población total (con ffill).
- `cu_x_expo` (coste de uso × exposición) es una variable en NIVEL: su contribución se mide como (coste de uso − media muestral del coste de uso) × exposición, no respecto al origen del coste de uso.
  Los canales por exposición en M1 dependen de la media ponderada de la exposición (estandarizada sin ponderar): existen solo por la ponderación por población.
- Efecto de borde: Σ Δ4/4 no es el cambio en niveles y difieren de forma apreciable (alquiler P2: 1,94 en niveles frente a 1,32 aquí;
  compra P2: −2,95 frente a −4,49; `observado_niveles_referencia.csv`).
- Los IC temporales de P3 (8 trimestres, 2 bloques) y P4 (9) son poco fiables. No hay corrección por multiplicidad en ningún IC.
- IC95 %: percentiles de 49 réplicas de (i) bootstrap por bloques de provincias (cluster, remuestreo de provincias con reposición, modelo reestimado) y (ii) bootstrap
  por bloques de tiempo (bloques móviles de 4 trimestres dentro de cada periodo). La tabla da la ENVOLVENTE de ambos (`contribuciones_todas.csv` tiene cada uno por separado).
  El «observado» también tiene IC porque la media ponderada depende de las provincias/trimestres remuestreados.
- Ventanas acumuladas: «desde 2014» = P2+P3+P4 (2014Q1-2024Q1) y «desde 2020» = P3+P4 (2020Q1-2024Q1).

## Alquiler (IPC de alquiler nominal) - subida desde 2014 (P2+P3+P4)
| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |
|---|---|---|---|---|---|
| **Observado** (crecimiento acumulado, pp de ln) | 7,69 [3,86; 10,80] | 100 % | 7,69 [5,53; 12,03] | 100 % | DESCRIPTIVO |
| Suma de familias | −4,20 [−10,92; 0,51] | −55 % | −3,70 [−12,18; 3,09] | −48 % | DESCRIPTIVO |
| Demografía (20-34 + extranjera) | −4,51 [−11,02; 0,44] | −59 % | −3,71 [−11,15; 2,05] | −48 % | EXPLORATORIO |
|   · pob 20-34 | −4,07 [−8,38; −0,53] | −53 % | −5,39 [−11,31; −0,61] | −70 % | EXPLORATORIO (coeficiente análogo al componente 20-34 de H1; Holm-7 ejecutado: ninguna confirmatoria sobrevive; nivel según BS) |
|   · pob extranjera | −0,44 [−4,14; 3,66] | −6 % | 1,68 [−0,80; 4,57] | 22 % | EXPLORATORIO |
| Empleo (ocupados) | 0,49 [−0,10; 1,36] | 6 % | 0,25 [−0,66; 1,14] | 3 % | EXPLORATORIO |
| Crédito / coste de uso | −0,15 [−0,49; 0,18] | −2 % | −0,21 [−1,65; 0,58] | −3 % | EXPLORATORIO |
| Oferta (terminadas) | −0,03 [−0,15; 0,09] | −0 % | −0,02 [−0,09; 0,11] | −0 % | EXPLORATORIO |
| Política (tope de rentas CAT) | 0,00 [0,00; 0,00] | 0 % | 0,00 [0,00; 0,00] | 0 % | EXPLORATORIO (H5/tope: falló placebos y pretendencias en BP) |
| Común: efectos de tiempo + FE | 11,70 [5,32; 19,43] | 152 % | 11,70 [5,72; 17,63] | 152 % | DESCRIPTIVO |
| Residuo | 0,19 [−0,33; 0,48] | 2 % | −0,31 [−1,12; 0,39] | −4 % | DESCRIPTIVO |

## Alquiler - subida desde 2020 (P3+P4)
| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |
|---|---|---|---|---|---|
| **Observado** (crecimiento acumulado, pp de ln) | 6,38 [4,70; 7,20] | 100 % | 6,38 [5,11; 7,50] | 100 % | DESCRIPTIVO |
| Suma de familias | −0,10 [−4,00; 3,57] | −2 % | 2,14 [−0,34; 5,15] | 34 % | DESCRIPTIVO |
| Demografía (20-34 + extranjera) | −0,69 [−4,19; 2,75] | −11 % | 1,77 [−0,69; 4,29] | 28 % | EXPLORATORIO |
|   · pob 20-34 | −0,20 [−0,67; 1,14] | −3 % | −0,11 [−0,68; 0,85] | −2 % | EXPLORATORIO (coeficiente análogo al componente 20-34 de H1; Holm-7 ejecutado: ninguna confirmatoria sobrevive; nivel según BS) |
|   · pob extranjera | −0,49 [−4,05; 3,23] | −8 % | 1,88 [−0,71; 4,74] | 29 % | EXPLORATORIO |
| Empleo (ocupados) | 0,70 [0,10; 1,37] | 11 % | 0,43 [−0,11; 1,16] | 7 % | EXPLORATORIO |
| Crédito / coste de uso | −0,09 [−0,36; 0,03] | −1 % | −0,04 [−0,82; 0,46] | −1 % | EXPLORATORIO |
| Oferta (terminadas) | −0,03 [−0,08; 0,09] | −0 % | −0,02 [−0,08; 0,11] | −0 % | EXPLORATORIO |
| Política (tope de rentas CAT) | 0,00 [0,00; 0,00] | 0 % | 0,00 [0,00; 0,00] | 0 % | EXPLORATORIO (H5/tope: falló placebos y pretendencias en BP) |
| Común: efectos de tiempo + FE | 6,25 [2,80; 9,86] | 98 % | 4,10 [0,80; 7,10] | 64 % | DESCRIPTIVO |
| Residuo | 0,23 [−0,28; 0,46] | 4 % | 0,14 [−0,24; 0,44] | 2 % | DESCRIPTIVO |

**Lectura (asociación, no causalidad).**
- Desde 2014 el IPC de alquiler acumula 7,69 [3,86; 10,80] pp. Con efectos de tiempo (M1) las familias medidas suman
  −4,20 [−10,92; 0,51] pp: casi todo el aumento queda en el componente común (11,70 [5,32; 19,43] pp), es decir,
  en lo que se mueve igual en todas las provincias y no se explica con las variables disponibles (tipos, regulación nacional, expectativas, inflación...).
- La demografía contribuye NEGATIVAMENTE en 2014-2019 (P2: población de 20-34 años en descenso, coeficiente positivo): −3,87 [−8,27; −0,93] pp en M1.
  No explica la subida; el signo es el de la composición, no el de una asociación nueva.
- Desde 2020 ninguna familia se distingue de 0 en M1 y M2 a la vez (población 20-34: M1 −0,20 [−0,67; 1,14], M2 −0,11 [−0,68; 0,85]; ver «No robustos»).
- Lo no explicado domina: en M1 el componente común es 98 % del crecimiento desde 2020; en M2 64 %.

## Compra (valor tasado REAL) - subida desde 2014 (P2+P3+P4)
| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |
|---|---|---|---|---|---|
| **Observado** (crecimiento acumulado, pp de ln) | −9,53 [−22,26; −3,33] | 100 % | −9,53 [−18,41; −3,29] | 100 % | DESCRIPTIVO |
| Suma de familias | −19,21 [−39,83; 4,08] | 202 % | −14,35 [−47,99; 2,14] | 151 % | DESCRIPTIVO |
| Demografía (20-34 + extranjera) | −17,98 [−30,20; 4,49] | 189 % | −15,45 [−44,10; −2,74] | 162 % | EXPLORATORIO (H2 no confirmada en el sellado) |
|   · pob 20-34 | −17,54 [−34,96; −3,94] | 184 % | −3,81 [−30,30; 9,08] | 40 % | EXPLORATORIO (H2 no confirmada en el sellado) |
|   · pob extranjera | −0,43 [−7,38; 13,29] | 5 % | −11,64 [−18,99; −5,26] | 122 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Empleo (ocupados) | 0,23 [−1,60; 2,44] | −2 % | 1,12 [−0,01; 3,29] | −12 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Crédito / coste de uso | −1,52 [−15,45; 5,13] | 16 % | −0,04 [−6,16; 6,24] | 0 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Oferta (terminadas) | 0,06 [−0,69; 0,41] | −1 % | 0,02 [−0,54; 0,44] | −0 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Común: efectos de tiempo + FE | 10,08 [−22,17; 32,53] | −106 % | 5,43 [−18,89; 36,21] | −57 % | DESCRIPTIVO |
| Residuo | −0,40 [−1,17; 1,31] | 4 % | −0,60 [−1,75; 1,40] | 6 % | DESCRIPTIVO |

## Compra - desde 2020 (P3+P4)
| Componente | M1 pp [IC95 %] | % obs. M1 | M2 pp [IC95 %] | % obs. M2 | Evidencia heredada |
|---|---|---|---|---|---|
| **Observado** (crecimiento acumulado, pp de ln) | −5,03 [−11,87; −2,31] | 100 % | −5,03 [−9,76; −2,27] | 100 % | DESCRIPTIVO |
| Suma de familias | −3,14 [−10,57; 8,08] | 62 % | −10,09 [−17,39; −0,33] | 200 % | DESCRIPTIVO |
| Demografía (20-34 + extranjera) | −1,98 [−8,47; 11,72] | 39 % | −9,56 [−14,59; −3,64] | 190 % | EXPLORATORIO (H2 no confirmada en el sellado) |
|   · pob 20-34 | −1,10 [−3,83; 1,55] | 22 % | 1,76 [−1,16; 4,67] | −35 % | EXPLORATORIO (H2 no confirmada en el sellado) |
|   · pob extranjera | −0,88 [−8,07; 13,36] | 18 % | −11,31 [−16,96; −4,59] | 225 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Empleo (ocupados) | 0,85 [−0,24; 2,57] | −17 % | 0,48 [−0,20; 2,18] | −10 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Crédito / coste de uso | −2,03 [−15,24; 3,66] | 40 % | −1,02 [−4,83; 4,71] | 20 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Oferta (terminadas) | 0,03 [−0,16; 0,26] | −0 % | 0,01 [−0,18; 0,25] | −0 % | EXPLORATORIO (H2 no confirmada en el sellado) |
| Común: efectos de tiempo + FE | −1,33 [−17,68; 6,21] | 26 % | 5,09 [−5,91; 14,23] | −101 % | DESCRIPTIVO |
| Residuo | −0,57 [−1,07; 0,32] | 11 % | −0,04 [−1,14; 0,74] | 1 % | DESCRIPTIVO |

**Lectura (asociación, no causalidad).**
- En términos REALES el valor tasado no «sube» en el conjunto 2014-2024Q1: observado −9,53 [−22,26; −3,33] pp (recuperación en P2, caída real en P3-P4: −5,03 [−11,87; −2,31] pp desde 2020 por la inflación del deflactor).
  Por eso la pregunta «qué explica la subida» se refiere al nominal solo de forma indirecta; aquí se descompone el real.
- Ninguna familia explica de forma robusta la evolución desde 2020: en M1 las familias suman −3,14 [−10,57; 8,08] pp y el común −1,33 [−17,68; 6,21] pp.
  En M2 la demografía (sobre todo extranjera: −11,31 [−16,96; −4,59] pp) sale con signo negativo en P3-P4 porque los coeficientes por periodo de la población cambian de signo
  (`coeficientes_por_periodo.csv`); no se interpreta, la inestabilidad entre M1 y M2 indica que no hay una atribución estable.
- Crédito/coste de uso en P1 (con (coste de uso − media muestral) × exposición; la estimación no se centra): −4,33 [−9,99; 13,83] pp en M1; desde 2014 −1,52 [−15,45; 5,13] pp.
- En compra M2 el coeficiente de Δ4 coste de uso nacional es 0,0058 (signo contrario al esperado si es positivo; IC por bloques de tiempo en `coeficientes_por_periodo.csv`).

## Contrafactuales (EXPLORATORIOS y PARCIALES)
**Advertencia:** son ejercicios ceteris paribus sobre las variables del modelo: se modifican solo esas variables con los coeficientes estimados; no hay equilibrio general
(oferta, expectativas, migración y precios se retroalimentan), la identificación no es causal y M1 solo recoge el canal diferencial entre provincias (coste de uso
únicamente vía exposición hipotecaria; en alquiler M1 el canal de coste de uso es 0 por construcción). M2 añade el canal temporal nacional, pero con una serie única (IC por bloques de tiempo).
Efecto = valor contrafactual − observado (pp acumulados de ln). Si «sin variación» elimina una caída observada, el efecto es positivo.
| Mercado | Modelo | Escenario | Efecto P2-P4 acumulado (pp) | Efecto P4 (pp) | Observado P4 (pp) |
|---|---|---|---|---|---|
| alquiler | M1 | (a) 20-34 y extranjera sin variación desde 2014Q1 | 4,51 [−0,44; 11,02] | 0,24 [−1,84; 2,94] | 4,46 |
| alquiler | M1 | (a1) solo 20-34 sin variación | 4,07 [0,53; 8,38] | 0,11 [−0,52; 0,52] | 4,46 |
| alquiler | M1 | (a2) solo extranjera sin variación | 0,44 [−3,66; 4,14] | 0,13 [−2,16; 3,18] | 4,46 |
| alquiler | M1 | (a3) ambas: se elimina solo el crecimiento positivo | 0,73 [−2,10; 3,85] | 0,28 [−1,79; 3,05] | 4,46 |
| alquiler | M1 | (b) crédito y coste de uso congelados en 2013Q4 | 0,17 [−0,18; 0,54] | 0,00 [−0,13; 0,17] | 4,46 |
| alquiler | M1 | (c) coste de uso de 2021Q4 durante P4 | (solo P4) | no aplica (0 por construcción) | 4,46 |
| alquiler | M2 | (a) 20-34 y extranjera sin variación desde 2014Q1 | 3,71 [−2,05; 11,15] | −1,53 [−3,94; 0,78] | 4,46 |
| alquiler | M2 | (a1) solo 20-34 sin variación | 5,39 [0,61; 11,31] | 0,06 [−0,59; 0,57] | 4,46 |
| alquiler | M2 | (a2) solo extranjera sin variación | −1,68 [−4,57; 0,80] | −1,59 [−4,08; 0,70] | 4,46 |
| alquiler | M2 | (a3) ambas: se elimina solo el crecimiento positivo | −2,53 [−5,12; 0,14] | −1,51 [−3,52; 0,80] | 4,46 |
| alquiler | M2 | (b) crédito y coste de uso congelados en 2013Q4 | 0,24 [−0,51; 1,65] | −0,08 [−0,54; 0,57] | 4,46 |
| alquiler | M2 | (c) coste de uso de 2021Q4 durante P4 | (solo P4) | 0,01 [−0,24; 0,33] | 4,46 |
| compra | M1 | (a) 20-34 y extranjera sin variación desde 2014Q1 | 17,98 [−4,49; 30,20] | 2,59 [−10,62; 8,02] | −2,48 |
| compra | M1 | (a1) solo 20-34 sin variación | 17,54 [3,94; 34,96] | 0,59 [−0,82; 2,78] | −2,48 |
| compra | M1 | (a2) solo extranjera sin variación | 0,43 [−13,29; 7,38] | 2,00 [−10,98; 7,46] | −2,48 |
| compra | M1 | (a3) ambas: se elimina solo el crecimiento positivo | 2,76 [−13,01; 9,47] | 2,80 [−9,72; 8,24] | −2,48 |
| compra | M1 | (b) crédito y coste de uso congelados en 2013Q4 | 3,11 [−4,35; 27,11] | 1,99 [−4,74; 14,42] | −2,48 |
| compra | M1 | (c) coste de uso de 2021Q4 durante P4 | (solo P4) | 0,41 [−1,03; 3,05] | −2,48 |
| compra | M2 | (a) 20-34 y extranjera sin variación desde 2014Q1 | 15,45 [2,74; 44,10] | 9,59 [5,83; 13,45] | −2,48 |
| compra | M2 | (a1) solo 20-34 sin variación | 3,81 [−9,08; 30,30] | −1,99 [−4,62; 0,58] | −2,48 |
| compra | M2 | (a2) solo extranjera sin variación | 11,64 [5,26; 18,99] | 11,58 [6,14; 16,24] | −2,48 |
| compra | M2 | (a3) ambas: se elimina solo el crecimiento positivo | 7,40 [2,22; 16,83] | 8,93 [5,23; 12,54] | −2,48 |
| compra | M2 | (b) crédito y coste de uso congelados en 2013Q4 | −0,06 [−8,70; 7,32] | 0,68 [−7,87; 4,49] | −2,48 |
| compra | M2 | (c) coste de uso de 2021Q4 durante P4 | (solo P4) | 0,44 [−1,56; 2,21] | −2,48 |

- (a) La población de 20-34 años cayó en P2, así que fijarla (Δ=0) SUBE el alquiler contrafactual (a1, P2-P4, M1: 4,07 [0,53; 8,38] pp; M2: 5,39 [0,61; 11,31]); eliminar solo el crecimiento positivo (a3, M1) da 0,73 [−2,10; 3,85] pp.
- (b) y (c) en alquiler: (b) M1 0,17 [−0,18; 0,54] pp, M2 0,24 [−0,51; 1,65]; (c) M2 0,01 [−0,24; 0,33] (M1: no aplica). Compra: (b) M1 3,11 [−4,35; 27,11], M2 −0,06 [−8,70; 7,32]; (c) M1 0,41 [−1,03; 3,05], M2 0,44 [−1,56; 2,21]. Ausencia de señal no es evidencia de efecto nulo.
- Compra, (a), P4: M1 2,59 [−10,62; 8,02] frente a M2 9,59 [5,83; 13,45]: no hay contrafactual demográfico estable.
- En M1 el canal de coste de uso de (b)/(c) por exposición existe solo por la media ponderada de la exposición.
## Nacional: precio real con el ECM v1 real (EXPLORATORIO)
ECM v1 real (v1: `output/f2/ecuacion_real.csv`) reestimado con datos de entrenamiento (DOLS LP 2007Q1-2023Q4, N=68; CP 2008Q2-2024Q2, N=65).
IC95: CP = bootstrap de residuos por bloques (4), regresores fijos, B=49 (ECT puntual, no reestimado; subestima la incertidumbre del DOLS); LP = simulación normal (B=49) con covarianza HAC(4) del DOLS, coherente con v1. La tabla LP incluye la fila estacional y cuadra con el observado. Identidad de largo plazo (Δy = b·Δx + estacional + Δ desequilibrio):
| Periodo | Componente | pp [IC95 %] | % obs. |
|---|---|---|---|
| P1 | empleo (ocupados) | −31,0 [−52,2; −16,0] | 66 % |
| P1 | tipo hipotecario real | 0,3 [−0,3; 0,9] | −1 % |
| P1 | permisos (t-4) | −11,9 [−24,4; 2,8] | 25 % |
| P1 | costes de construcción reales | −5,5 [−8,1; −2,2] | 12 % |
| P1 | estacional (dummies) | 0,0 [0,0; 0,0] | −0 % |
| P1 | desequilibrio (Δ ect) | 1,2 [−5,1; 10,2] | −3 % |
| P1 | observado | −47,0 [−47,0; −47,0] | 100 % |
| P2 | empleo (ocupados) | 25,0 [12,9; 42,1] | 116 % |
| P2 | tipo hipotecario real | −1,8 [−6,5; 2,0] | −8 % |
| P2 | permisos (t-4) | 2,1 [−0,5; 4,4] | 10 % |
| P2 | costes de construcción reales | 2,0 [0,8; 3,0] | 9 % |
| P2 | estacional (dummies) | 0,0 [0,0; 0,0] | 0 % |
| P2 | desequilibrio (Δ ect) | −5,8 [−16,1; 1,1] | −27 % |
| P2 | observado | 21,6 [21,6; 21,6] | 100 % |
| P3 | empleo (ocupados) | 2,5 [1,3; 4,2] | 103 % |
| P3 | tipo hipotecario real | −2,8 [−10,3; 3,2] | −114 % |
| P3 | permisos (t-4) | −2,7 [−5,5; 0,6] | −110 % |
| P3 | costes de construcción reales | −4,7 [−7,0; −1,9] | −195 % |
| P3 | estacional (dummies) | 0,0 [0,0; 0,0] | 0 % |
| P3 | desequilibrio (Δ ect) | 10,1 [6,4; 14,0] | 417 % |
| P3 | observado | 2,4 [2,4; 2,4] | 100 % |
| P4 | empleo (ocupados) | 11,0 [5,7; 18,5] | 231 % |
| P4 | tipo hipotecario real | 2,7 [−3,1; 10,2] | 58 % |
| P4 | permisos (t-4) | 5,0 [−1,2; 10,2] | 105 % |
| P4 | costes de construcción reales | −0,2 [−0,3; −0,1] | −4 % |
| P4 | estacional (dummies) | −3,0 [−5,6; −1,3] | −63 % |
| P4 | desequilibrio (Δ ect) | −10,7 [−19,5; −5,4] | −226 % |
| P4 | observado | 4,8 [4,8; 4,8] | 100 % |

Corto plazo (suma de Δy_t = Σ coef·x; exacta):
| Periodo | Componente | pp [IC95 %] | % obs. |
|---|---|---|---|
| P1 | desequilibrio (ect t-1) | −10,6 [−19,9; −3,3] | 23 % |
| P1 | constante + estacionales | −5,0 [−12,6; 2,2] | 11 % |
| P1 | empleo (Δ ocupados t-1) | −10,1 [−13,5; −5,9] | 22 % |
| P1 | tipos (Δ tipo hip. t-1) | 2,6 [0,4; 4,9] | −6 % |
| P1 | renta real (Δ) | −0,9 [−1,8; 0,0] | 2 % |
| P1 | inercia (Δy t-4) | −9,4 [−14,6; −4,3] | 21 % |
| P1 | crédito nuevo (Δ) | −6,2 [−9,4; −4,0] | 13 % |
| P1 | residuo | −6,3 [−14,3; 3,4] | 14 % |
| P1 | observado | −45,9 [−45,9; −45,9] | 100 % |
| P2 | desequilibrio (ect t-1) | 5,9 [1,8; 11,1] | 27 % |
| P2 | constante + estacionales | −4,9 [−13,3; 2,7] | −23 % |
| P2 | empleo (Δ ocupados t-1) | 7,8 [4,6; 10,5] | 36 % |
| P2 | tipos (Δ tipo hip. t-1) | 1,1 [0,1; 2,0] | 5 % |
| P2 | renta real (Δ) | 2,2 [−0,0; 4,3] | 10 % |
| P2 | inercia (Δy t-4) | 2,7 [1,2; 4,2] | 12 % |
| P2 | crédito nuevo (Δ) | 3,0 [2,0; 4,7] | 14 % |
| P2 | residuo | 3,7 [−7,1; 15,0] | 17 % |
| P2 | observado | 21,6 [21,6; 21,6] | 100 % |
| P3 | desequilibrio (ect t-1) | −0,5 [−0,9; −0,1] | −19 % |
| P3 | constante + estacionales | −1,6 [−4,4; 0,9] | −67 % |
| P3 | empleo (Δ ocupados t-1) | 0,6 [0,4; 0,8] | 26 % |
| P3 | tipos (Δ tipo hip. t-1) | 0,5 [0,1; 1,0] | 21 % |
| P3 | renta real (Δ) | −0,0 [−0,0; 0,0] | −1 % |
| P3 | inercia (Δy t-4) | 0,6 [0,3; 0,9] | 24 % |
| P3 | crédito nuevo (Δ) | 1,0 [0,6; 1,5] | 41 % |
| P3 | residuo | 1,8 [−0,9; 5,1] | 75 % |
| P3 | observado | 2,4 [2,4; 2,4] | 100 % |
| P4 | desequilibrio (ect t-1) | 1,8 [0,6; 3,4] | 38 % |
| P4 | constante + estacionales | −0,7 [−4,8; 2,8] | −15 % |
| P4 | empleo (Δ ocupados t-1) | 3,0 [1,8; 4,1] | 64 % |
| P4 | tipos (Δ tipo hip. t-1) | −2,3 [−4,3; −0,3] | −48 % |
| P4 | renta real (Δ) | 1,0 [−0,0; 1,9] | 20 % |
| P4 | inercia (Δy t-4) | 0,7 [0,3; 1,0] | 14 % |
| P4 | crédito nuevo (Δ) | 0,5 [0,3; 0,8] | 11 % |
| P4 | residuo | 0,8 [−3,8; 5,7] | 16 % |
| P4 | observado | 4,8 [4,8; 4,8] | 100 % |

Lectura: en 2014-2019 (P2) el empleo (7,8 [4,6; 10,5] pp en CP) y el desequilibrio (5,9 [1,8; 11,1] pp) concentran buena parte del aumento real;
en P4 (2022Q1-2024Q2) los tipos restan (−2,3 [−4,3; −0,3] pp, IC en el límite del 0) y el desequilibrio de largo plazo se cierra (−10,7 [−19,5; −5,4] pp),
mientras el empleo aporta 11,0 [5,7; 18,5] pp. Los IC de LP vienen del HAC (en v1 solo empleo y costes eran significativos).
El DOLS usa pocos datos, la estacionalidad del LP depende de los trimestres de inicio y fin, y el «residuo» de CP no es independiente de la elección de variables de v1 (elegidas por R² ajustado en la misma muestra).

## Turismo (VUT; solo ventana 2021Q3-2024Q1; N temporal = 6)
Contribución en P4 (6 trimestres): −0,19 pp [−0,40; 0,48] sobre un crecimiento observado en la ventana de 2,40 pp. No se distingue de 0; no comparable con el resto (otra ventana y coeficiente global). `turismo_*.csv`.

## No robustos / no replicados entre M1 y M2 (no son hallazgos; sin corrección por multiplicidad sobre ~14 componentes × 2 modelos)
- Población 20-34 en alquiler desde 2020: M1 −0,20 [−0,67; 1,14] (IC incluye 0) frente a M2 −0,11 [−0,68; 0,85] (IC excluye 0): solo aparece en un modelo.
- (a1) alquiler en P4: M1 0,11 [−0,52; 0,52] frente a M2 0,06 [−0,59; 0,57]: solo M2 excluye 0.
- (b) compra P2-P4: M1 3,11 [−4,35; 27,11] (excluye 0) frente a M2 −0,06 [−8,70; 7,32].

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
