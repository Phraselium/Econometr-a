# Fichas F5: factor mas relevante por mercado y periodo (ambito nacional)

svar_hd: C3s, condicionado a los supuestos de signo y de cero de M2 (V3: solo impacto; magnitudes posiblemente atenuadas, Y6). El resto de metodos son C4 (asociacion): sin lectura causal.

Regla fijada ANTES de calcular (docs/v8/desviaciones.md, R0-R8): 3 de 4 votos + multiverso orientado >= 80 % (familia y variable principal) + banda 68 % de svar_hd sin el 0; P4 y alquiler P1 no se designan. Una abstencion cuenta como «no apoya».

## Compra P1

- dY observada (R0): 75.4 pp (ventana de cada metodo (P1: desde su 1.er trimestre)).
- Votos: svar_hd = empleo_renta (P(f*) = 0.72); dominancia = abstiene; lpiv = abstiene; contabilidad = abstiene.
- Recuento: empleo_renta:1. Factor evaluado: empleo_renta (1 de 4).
- Multiverso orientado (pib_vol): familia 88 % (35 % con fallidas); variable principal 88 % (58 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [9.0; 54.6] pp.
- Cuota no atribuida (determinista + no identificados): 31.6 pp = 42 % de dY (banda 68 % aproximada -8 % a 98 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 1 de 4 votos (empleo_renta); lpiv abstiene (c·sign(dY) de lpiv (26.7 pp) no supera la mayor de svar_hd (31.8 pp): se abstiene).
- Conclusion: no se designa un factor mas relevante en compra P1; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Compra P2

- dY observada (R0): -44.0 pp (ventana de cada metodo (P1: desde su 1.er trimestre)).
- Votos: svar_hd = empleo_renta (P(f*) = 0.32); dominancia = factor_europeo; lpiv = abstiene; contabilidad = abstiene.
- Recuento: empleo_renta:1; factor_europeo:1. Factor evaluado: empleo_renta (1 de 4).
- Aviso svar_hd: ranking incierto (P(f*) < 0,5).
- Multiverso orientado (pib_vol): familia 75 % (75 % con fallidas); variable principal 75 % (75 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [-23.5; 0.7] pp.
- Cuota no atribuida (determinista + no identificados): -9.6 pp = 22 % de dY (banda 68 % aproximada -35 % a 80 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 1 de 4 votos (empleo_renta); lpiv abstiene (c·sign(dY) de lpiv (-42.4 pp) no supera la mayor de svar_hd (10.6 pp): se abstiene); condicion 2 no se cumple (multiverso orientado: familia 75 %, variable principal 75 %; umbral 80 %); condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0.
- Conclusion: no se designa un factor mas relevante en compra P2; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Compra P3

- dY observada (R0): 8.2 pp (ventana de cada metodo (P1: desde su 1.er trimestre)).
- Votos: svar_hd = empleo_renta (P(f*) = 0.41); dominancia = empleo_renta; lpiv = abstiene; contabilidad = demografia.
- Recuento: empleo_renta:2; demografia:1. Factor evaluado: empleo_renta (2 de 4).
- Aviso svar_hd: ranking incierto (P(f*) < 0,5).
- Multiverso orientado (pib_vol): familia 85 % (85 % con fallidas); variable principal 95 % (95 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [-3.5; 18.2] pp.
- Cuota no atribuida (determinista + no identificados): 1.9 pp = 24 % de dY (banda 68 % aproximada -307 % a 336 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 2 de 4 votos (empleo_renta); lpiv abstiene (c·sign(dY) de lpiv (7.4 pp) no supera la mayor de svar_hd (7.7 pp): se abstiene); condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0.
- Conclusion: no se designa un factor mas relevante en compra P3; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Compra P4

- dY observada (R0): -5.5 pp (ventana de cada metodo (P1: desde su 1.er trimestre)).
- Votos: svar_hd = empleo_renta (P(f*) = 0.26); dominancia = credito_tipos; lpiv = credito_tipos; contabilidad = abstiene.
- Recuento: credito_tipos:2; empleo_renta:1. Factor evaluado: credito_tipos (2 de 4).
- Aviso svar_hd: ranking incierto (media y P(f*) discrepan); ranking incierto (P(f*) < 0,5).
- Multiverso orientado (tipo_hip_real): familia 54 % (34 % con fallidas); variable principal 52 % (33 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [-4.7; 4.4] pp.
- Cuota no atribuida (determinista + no identificados): -0.8 pp = 14 % de dY (banda 68 % aproximada -220 % a 295 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 2 de 4 votos (credito_tipos); lpiv vota (ok); condicion 2 no se cumple (multiverso orientado: familia 54 %, variable principal 52 %; umbral 80 %); condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0; R7: periodo impreciso (P4 de 9 trimestres / alquiler P1 sin svar_hd).
- Conclusion: no se designa un factor mas relevante en compra P4; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Compra P5

- dY observada (R0): 18.4 pp (2022T3-2026T1).
- Votos: svar_hd = credito_tipos (P(f*) = 0.30); dominancia = credito_tipos; lpiv = abstiene; contabilidad = demografia.
- Recuento: credito_tipos:2; demografia:1. Factor evaluado: credito_tipos (2 de 4).
- Aviso svar_hd: ranking incierto (media y P(f*) discrepan); ranking incierto (P(f*) < 0,5).
- Multiverso orientado (tipo_hip_real): familia 63 % (63 % con fallidas); variable principal 88 % (88 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [-2.8; 12.8] pp.
- Cuota no atribuida (determinista + no identificados): 9.5 pp = 52 % de dY (banda 68 % aproximada -79 % a 131 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 2 de 4 votos (credito_tipos); lpiv abstiene (c·sign(dY) de lpiv (-11.3 pp) no supera la mayor de svar_hd (7.2 pp): se abstiene); condicion 2 no se cumple (multiverso orientado: familia 63 %, variable principal 88 %; umbral 80 %); condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0.
- Conclusion: no se designa un factor mas relevante en compra P5; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Alquiler P1

- dY observada (R0): 4.9 pp (ventana de cada metodo (P1: desde su 1.er trimestre)).
- Votos: svar_hd = abstiene; dominancia = factor_europeo; lpiv = abstiene; contabilidad = abstiene.
- Recuento: factor_europeo:1. Factor evaluado: factor_europeo (1 de 4).
- Aviso svar_hd: sin svar_hd (M2 no cubre esta celda).
- Multiverso orientado (bis_hpi_xm_real): familia 51 % (51 % con fallidas); variable principal 50 % (50 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [n.d.; n.d.] pp.
- Resultado: **no designado**. condicion 1 no se cumple: maximo 1 de 4 votos (factor_europeo); lpiv abstiene (F < 10 y AR 68 % no acotado: se abstiene); condicion 2 no se cumple (multiverso orientado: familia 51 %, variable principal 50 %; umbral 80 %); condicion 3 no evaluable: no hay svar_hd en esta celda; R7: periodo impreciso (P4 de 9 trimestres / alquiler P1 sin svar_hd).
- Conclusion: no se designa un factor mas relevante en alquiler P1; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Alquiler P2

- dY observada (R0): -2.7 pp (ventana de cada metodo (P1: desde su 1.er trimestre)).
- Votos: svar_hd = empleo_renta (P(f*) = 0.39); dominancia = empleo_renta; lpiv = abstiene; contabilidad = abstiene.
- Recuento: empleo_renta:2. Factor evaluado: empleo_renta (2 de 4).
- Aviso svar_hd: ranking incierto (P(f*) < 0,5).
- Multiverso orientado (pib_vol): familia 51 % (51 % con fallidas); variable principal 56 % (56 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [-4.3; 0.8] pp.
- Cuota no atribuida (determinista + no identificados): -1.2 pp = 46 % de dY (banda 68 % aproximada -191 % a 278 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 2 de 4 votos (empleo_renta); lpiv abstiene (F < 10 y AR 68 % no acotado: se abstiene); condicion 2 no se cumple (multiverso orientado: familia 51 %, variable principal 56 %; umbral 80 %); condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0.
- Conclusion: no se designa un factor mas relevante en alquiler P2; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Alquiler P3

- dY observada (R0): -1.1 pp (ventana de cada metodo (P1: desde su 1.er trimestre)).
- Votos: svar_hd = demografia (P(f*) = 0.33); dominancia = demanda_externa; lpiv = abstiene; contabilidad = abstiene.
- Recuento: demografia:1; demanda_externa:1. Factor evaluado: demografia (1 de 4).
- Aviso svar_hd: ranking incierto (P(f*) < 0,5).
- Multiverso orientado (pob_total): familia 79 % (79 % con fallidas); variable principal 90 % (90 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [-2.9; 2.7] pp.
- Cuota no atribuida (determinista + no identificados): -4.6 pp = 431 % de dY (banda 68 % aproximada -269 % a 1092 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 1 de 4 votos (demografia); lpiv abstiene (F < 10 y AR 68 % no acotado: se abstiene); condicion 2 no se cumple (multiverso orientado: familia 79 %, variable principal 90 %; umbral 80 %); condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0.
- Conclusion: no se designa un factor mas relevante en alquiler P3; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Alquiler P4

- dY observada (R0): -9.3 pp (ventana de cada metodo (P1: desde su 1.er trimestre)).
- Votos: svar_hd = demanda_vivienda (P(f*) = 0.24); dominancia = credito_tipos; lpiv = abstiene; contabilidad = abstiene.
- Recuento: demanda_vivienda:1; credito_tipos:1. Factor evaluado: demanda_vivienda (1 de 4).
- Aviso svar_hd: ranking incierto (media y P(f*) discrepan); ranking incierto (P(f*) < 0,5).
- Multiverso orientado (-): familia n.d. % (n.d. % con fallidas); variable principal n.d. % (n.d. % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [-3.2; 0.1] pp.
- Cuota no atribuida (determinista + no identificados): -3.2 pp = 34 % de dY (banda 68 % aproximada -15 % a 87 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 1 de 4 votos (demanda_vivienda); lpiv abstiene (F < 10 y AR 68 % no acotado: se abstiene); condicion 2 no se cumple (multiverso orientado: familia n.d. %, variable principal n.d. %; umbral 80 %); condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0; R7: periodo impreciso (P4 de 9 trimestres / alquiler P1 sin svar_hd).
- Conclusion: no se designa un factor mas relevante en alquiler P4; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).

## Alquiler P5

- dY observada (R0): -1.8 pp (2022T3-2026T1).
- Votos: svar_hd = credito_tipos (P(f*) = 0.26); dominancia = credito_tipos; lpiv = abstiene; contabilidad = abstiene.
- Recuento: credito_tipos:2. Factor evaluado: credito_tipos (2 de 4).
- Aviso svar_hd: ranking incierto (P(f*) < 0,5).
- Multiverso orientado (tipo_hip_real): familia 52 % (52 % con fallidas); variable principal 85 % (85 % con fallidas).
- Banda 68 % de svar_hd del factor evaluado: [-2.6; 2.3] pp.
- Cuota no atribuida (determinista + no identificados): -2.0 pp = 106 % de dY (banda 68 % aproximada -194 % a 429 %).
- Resultado: **no designado**. condicion 1 no se cumple: maximo 2 de 4 votos (credito_tipos); lpiv abstiene (F < 10 y AR 68 % no acotado: se abstiene); condicion 2 no se cumple (multiverso orientado: familia 52 %, variable principal 85 %; umbral 80 %); condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0.
- Conclusion: no se designa un factor mas relevante en alquiler P5; se publica el ranking con incertidumbre (ranking.csv), sin lectura causal salvo la condicionada de svar_hd (C3s).
