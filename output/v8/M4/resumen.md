# M4 largo plazo (C4, asociación; completo)

## Cointegración por especificación

| mercado | spec | EG_p_mackinnon | GH_p_sim | GH_fecha | ARDL_F_sin_rupturas | ARDL_p_sup_sin |
|---|---|---|---|---|---|---|
| compra | C1 | 0.625 | 0.938 | 2019Q2 | 1.994 | 0.100 |
| compra | C2 | 0.969 | 0.956 | 2010Q3 | 8.461 | 0.001 |
| compra | C3 | 0.962 | 0.840 | 2009Q4 | 12.428 | 0.001 |
| compra | C4 | 0.814 | 0.882 | 2009Q4 | 12.689 | 0.001 |
| alquiler | A1 | 0.440 | 0.447 | 2020Q2 | 17.432 | 0.001 |
| alquiler | A2 | 0.635 | 0.719 | 2020Q1 | 22.222 | 0.001 |
| alquiler | A2b | 0.817 | 0.866 | 2020Q1 | 24.710 | 0.001 |
| alquiler | A3 | 0.371 | 0.409 | 2017Q1 | 12.063 | 0.001 |
| alquiler | A4 | 0.428 | 0.573 | 2017Q1 | 9.994 | 0.001 |

## Coeficientes de largo plazo de la especificación de cabecera (sin rupturas)

| mercado | metodo_lp | variable | beta | ic95_lo | ic95_hi | p_ajustado | vel_ajuste | semivida |
|---|---|---|---|---|---|---|---|---|
| compra | dols | renta | 0.058 | -0.269 | 0.385 | 0.841 | -0.015 | 46.806 |
| compra | dols | tipo | -0.004 | -0.010 | 0.002 | 0.299 | -0.015 | 46.806 |
| compra | dols | pob | 1.598 | 0.892 | 2.303 | 0.000 | -0.015 | 46.806 |
| compra | dols | credito | 0.520 | 0.444 | 0.596 | 0.000 | -0.015 | 46.806 |
| compra | dols | oferta | -0.043 | -0.155 | 0.069 | 0.648 | -0.015 | 46.806 |
| compra | fmols | renta | 1.026 | 0.537 | 1.516 | 0.000 | -0.015 | 44.844 |
| compra | fmols | tipo | 0.000 | -0.013 | 0.013 | 0.985 | -0.015 | 44.844 |
| compra | fmols | pob | -0.417 | -1.870 | 1.035 | 0.741 | -0.015 | 44.844 |
| compra | fmols | credito | 0.619 | 0.479 | 0.759 | 0.000 | -0.015 | 44.844 |
| compra | fmols | oferta | -0.311 | -0.497 | -0.124 | 0.004 | -0.015 | 44.844 |
| compra | ardl | renta | -0.045 | -1.126 | 1.035 | 0.964 | -0.083 | 7.978 |
| compra | ardl | tipo | 0.019 | -0.005 | 0.042 | 0.240 | -0.083 | 7.978 |
| compra | ardl | pob | 0.268 | -2.623 | 3.158 | 0.914 | -0.083 | 7.978 |
| compra | ardl | credito | -0.145 | -0.677 | 0.386 | 0.741 | -0.083 | 7.978 |
| compra | ardl | oferta | 0.656 | 0.054 | 1.257 | 0.087 | -0.083 | 7.978 |
| alquiler | dols | renta | 0.034 | -0.123 | 0.191 | 0.807 | -0.213 | 2.898 |
| alquiler | dols | tipo | 0.002 | -0.001 | 0.005 | 0.357 | -0.213 | 2.898 |
| alquiler | dols | hogares | -2.014 | -2.834 | -1.193 | 0.000 | -0.213 | 2.898 |
| alquiler | dols | credito | -0.000 | -0.080 | 0.079 | 0.992 | -0.213 | 2.898 |
| alquiler | dols | oferta | 0.397 | 0.168 | 0.625 | 0.003 | -0.213 | 2.898 |
| alquiler | fmols | renta | -0.097 | -0.175 | -0.020 | 0.042 | -0.227 | 2.691 |
| alquiler | fmols | tipo | 0.004 | 0.001 | 0.006 | 0.005 | -0.227 | 2.691 |
| alquiler | fmols | hogares | -1.879 | -2.609 | -1.150 | 0.000 | -0.227 | 2.691 |
| alquiler | fmols | credito | -0.040 | -0.111 | 0.031 | 0.471 | -0.227 | 2.691 |
| alquiler | fmols | oferta | 0.494 | 0.285 | 0.704 | 0.000 | -0.227 | 2.691 |
| alquiler | ardl | renta | -3.032 | -30.575 | 24.510 | 0.905 | 0.012 |  |
| alquiler | ardl | tipo | -0.248 | -2.563 | 2.067 | 0.905 | 0.012 |  |
| alquiler | ardl | hogares | 5.502 | -65.328 | 76.333 | 0.924 | 0.012 |  |
| alquiler | ardl | credito | 1.367 | -11.535 | 14.269 | 0.905 | 0.012 |  |
| alquiler | ardl | oferta | -1.959 | -24.677 | 20.759 | 0.919 | 0.012 |  |

Discrepancias DOLS/FMOLS (signo o |z|>1,96): 18 de 62; se reportan ambos (discrepancias_dols_fmols.csv).

## Fuera de muestra (RMSE de dy x100; bloques con embargo; misma muestra)

```
{
 "compra": {
  "AR4": 1.2826573442853957,
  "SR": 1.5272327033640105,
  "ECM": 2.652436757382752
 },
 "alquiler": {
  "AR4": 0.7255234886744043,
  "SR": 0.7253216296594136,
  "ECM": 2.796476880419172
 }
}
```

Decisión ARDL (J10): rechaza solo con F > cota I(1) y t < cota I(1); `contabilidad_lp` = sin cointegración demostrada (vota_s9 = no). Voto de la contabilidad por el signo de la brecha física: `voto_contabilidad.csv`.

Límites: asociación de largo plazo (no causal); potencia baja de los contrastes de cointegración; FMOLS con bandas normales; oferta y población son proxies marcadas; ECM v1 no replicable en la misma muestra.