# M0 periodos (C4, asociación; completo)

Muestras: compra 112 trimestres, alquiler 94. Efectos que cumplen la regla de §8 (todos C4 exploratorio; ver columna `lectura` de la tabla y el control BH): **2** de 70 evaluados; 40 `no_evaluable` (alquiler: SERPAVI anual; extras sin IPV). Sin lenguaje causal; C4 siempre.

## Detecciones significativas (serie nacional de crédito, tipos o actividad)

| metodo | serie | observable_umbral | n_regimenes | corte_o_regimen | p |
|---|---|---|---|---|---|
| bai_perron | d4_credito_vivienda_real |  | 4.000 | 2003Q4;2007Q4;2011Q4 | 0.013 |
| markov_switching | d4_credito_vivienda_real |  | 3.000 | R0: mu=-4.01, dur=39.8; R1: mu=0.66, dur=12.1; R2: mu=14.92, dur=80.5 | 0.033 |
| markov_switching | tipo_hip_real |  | 3.000 | R0: mu=0.63, dur=13.6; R1: mu=0.85, dur=13.4; R2: mu=2.81, dur=8.1 | 0.033 |
| umbral_hansen | tipo_hip_real | d4_credito_nuevo_real | 2.000 | gamma=1.761 (bajo n=40, alto n=49) | 0.007 |
| umbral_hansen | tipo_hip_real | d4_ocupados_sensibilidad | 2.000 | gamma=3.386 (bajo n=71, alto n=22) | 0.007 |
| markov_switching | d4_pib_vol |  | 3.000 | R0: mu=-1.36, dur=21.2; R1: mu=0.12, dur=10.7; R2: mu=3.25, dur=47.5 | 0.033 |
| umbral_hansen | d4_pib_vol | tasa_paro | 2.000 | gamma=14.711 (bajo n=54, alto n=43) | 0.017 |

## Regla por (mercado, periodo, variable) — ecuación base

| mercado | periodo | variable | signo_principal | n_confirmaciones | p_perm | alt_mismo_signo | cumple | lectura |
|---|---|---|---|---|---|---|---|---|
| compra | P1 | d4_pob_total | -1 | 2 | 0.652 | no_evaluable | no_evaluable |  |
| compra | P1 | d4_pib_vol | -1 | 2 | 0.201 | no_evaluable | no_evaluable |  |
| compra | P1 | tipo_hip_real | -1 | 1 | 0.007 | no_evaluable | no_evaluable |  |
| compra | P1 | d4_credito_vivienda_real | -1 | 1 | 0.111 | no_evaluable | no_evaluable |  |
| compra | P1 | d4_terminadas | -1 | 1 | 0.557 | no_evaluable | no_evaluable |  |
| compra | P2 | d4_pob_total | -1 | 1 | 0.313 | si | no |  |
| compra | P2 | d4_pib_vol | 1 | 3 | 0.040 | si | si | cumple la regla de §8; no sobrevive a BH (C4, exploratorio) |
| compra | P2 | tipo_hip_real | 1 | 3 | 0.167 | no | no |  |
| compra | P2 | d4_credito_vivienda_real | 1 | 3 | 0.868 | si | no |  |
| compra | P2 | d4_terminadas | 1 | 3 | 0.849 | si | no |  |
| compra | P3 | d4_pob_total | 1 | 2 | 0.124 | si | no |  |
| compra | P3 | d4_pib_vol | 1 | 3 | 0.205 | si | no |  |
| compra | P3 | tipo_hip_real | 1 | 2 | 0.896 | no | no |  |
| compra | P3 | d4_credito_vivienda_real | 1 | 2 | 0.546 | si | no |  |
| compra | P3 | d4_terminadas | -1 | 0 | 0.196 | si | no |  |
| compra | P4 | d4_pob_total | 1 | 2 | 0.833 | si | no |  |
| compra | P4 | d4_pib_vol | -1 | 0 | 0.079 | si | no |  |
| compra | P4 | tipo_hip_real | -1 | 0 | 0.305 | si | no |  |
| compra | P4 | d4_credito_vivienda_real | 1 | 2 | 0.580 | si | no |  |
| compra | P4 | d4_terminadas | 1 | 3 | 0.050 | si | si | cumple la regla de §8; no sobrevive a BH (C4, exploratorio) |
| compra | P5 | d4_pob_total | -1 | 0 | 0.098 | si | no |  |
| compra | P5 | d4_pib_vol | -1 | 0 | 0.517 | no | no |  |
| compra | P5 | tipo_hip_real | 1 | 2 | 0.733 | si | no |  |
| compra | P5 | d4_credito_vivienda_real | 1 | 2 | 0.291 | si | no |  |
| compra | P5 | d4_terminadas | -1 | 0 | 0.665 | si | no |  |
| alquiler | P1 | d4_pob_total | -1 | 1 | 0.287 | no_evaluable | no_evaluable |  |
| alquiler | P1 | d4_pib_vol | -1 | 3 | 0.263 | no_evaluable | no_evaluable |  |
| alquiler | P1 | tipo_hip_real | 1 | 3 | 0.337 | no_evaluable | no_evaluable |  |
| alquiler | P1 | d4_credito_vivienda_real | 1 | 3 | 0.520 | no_evaluable | no_evaluable |  |
| alquiler | P1 | d4_terminadas | -1 | 1 | 0.690 | no_evaluable | no_evaluable |  |
| alquiler | P2 | d4_pob_total | -1 | 1 | 0.343 | no_evaluable | no_evaluable |  |
| alquiler | P2 | d4_pib_vol | -1 | 3 | 0.150 | no_evaluable | no_evaluable |  |
| alquiler | P2 | tipo_hip_real | 1 | 3 | 0.270 | no_evaluable | no_evaluable |  |
| alquiler | P2 | d4_credito_vivienda_real | 1 | 3 | 0.264 | no_evaluable | no_evaluable |  |
| alquiler | P2 | d4_terminadas | -1 | 0 | 0.906 | no_evaluable | no_evaluable |  |
| alquiler | P3 | d4_pob_total | 1 | 3 | 0.292 | no_evaluable | no_evaluable |  |
| alquiler | P3 | d4_pib_vol | 1 | 0 | 0.642 | no_evaluable | no_evaluable |  |
| alquiler | P3 | tipo_hip_real | 1 | 3 | 0.484 | no_evaluable | no_evaluable |  |
| alquiler | P3 | d4_credito_vivienda_real | 1 | 3 | 0.673 | no_evaluable | no_evaluable |  |
| alquiler | P3 | d4_terminadas | 1 | 3 | 0.334 | no_evaluable | no_evaluable |  |
| alquiler | P4 | d4_pob_total | 1 | 3 | 0.669 | no_evaluable | no_evaluable |  |
| alquiler | P4 | d4_pib_vol | 1 | 0 | 0.335 | no_evaluable | no_evaluable |  |
| alquiler | P4 | tipo_hip_real | 1 | 3 | 0.194 | no_evaluable | no_evaluable |  |
| alquiler | P4 | d4_credito_vivienda_real | -1 | 0 | 0.473 | no_evaluable | no_evaluable |  |
| alquiler | P4 | d4_terminadas | -1 | 0 | 0.307 | no_evaluable | no_evaluable |  |
| alquiler | P5 | d4_pob_total | 1 | 2 | 0.978 | no_evaluable | no_evaluable |  |
| alquiler | P5 | d4_pib_vol | 1 | 0 | 0.873 | no_evaluable | no_evaluable |  |
| alquiler | P5 | tipo_hip_real | 1 | 3 | 0.454 | no_evaluable | no_evaluable |  |
| alquiler | P5 | d4_credito_vivienda_real | 1 | 3 | 0.444 | no_evaluable | no_evaluable |  |
| alquiler | P5 | d4_terminadas | 1 | 3 | 0.420 | no_evaluable | no_evaluable |  |

## Fuera de muestra (bloques con embargo, RMSE)

```
{
 "compra": {
  "AR4": 1.216435928195345,
  "AR4+X_comun": 1.486484450890057,
  "AR1+X_por_periodo": 1.8024443418980598
 },
 "alquiler": {
  "AR4": 0.8000051159290653,
  "AR4+X_comun": 1.7624595007711685,
  "AR1+X_por_periodo": 1.8146095630086345
 }
}
```

Control informativo de multiplicidad (BH sobre los 70 p de permutación; no forma parte de la regla de §8): de los 2 que cumplen la regla, 0 tienen p_perm BH < 0,10. Límites: BP con potencia 0,32-0,42; permutación de 5 tramos conservadora; P4 tiene 9 trimestres y 3 gl (imprecisa); el signo de una confirmación no exige significación. Desviaciones: docs/v8/desviaciones.md (2026-10-13, M0).