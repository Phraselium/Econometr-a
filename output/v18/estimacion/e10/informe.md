# E10 · Grandes tenedores y alquiler municipal (asociación transversal)

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.*

## Lectura

- **E10-X1** NO ESTIMABLE (tres cortes de titularidad; tarea del autor: puntos 9, 10, 7 y 6).
- **E10-A1** (1365 municipios no sellados, 38 provincias): coeficiente 1.068 % del alquiler por m² por punto de viviendas de grandes tenedores (IC95 t [-0.068; 2.205]; p Webb 0.065; Conley 10 km 0.321).
- **E10-A1-d** (variación 2019-2024, 1219 municipios): 0.105 (IC95 t [-0.437; 0.647]; p Webb 0.714).
- **ASOCIACIÓN** (tope): sin variación exógena y con el orden temporal invertido. El % de grandes tenedores es una cota inferior (tramo contado dentro del municipio). V17: titulares de más de 10 viviendas con el 4,2 % del parque (Catastro 2026; V17-AUD-OT-CAT-GT-PARQUE-2026) y entre el 2 y el 12 % del alquiler habitual con supuestos; no se duplica.

## Tabla de especificaciones

| id | estado | N | G | resultado | regresor | coef | se_cr1 | ic95_lo | ic95_hi | p_webb | se_conley_10km | moran_I | moran_p | q_BY | mde | clasificacion_v18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E10-X1 | NO ESTIMABLE | — | — | — | — | — | — | — | — | — | — | — | — | — | — | NO ESTIMABLE |
| E10-A1 | principal | 1365 | 38 | ln_alq_2024 | pct10 | 0.0107 | 0.0056 | -0.0007 | 0.022 | 0.0648 | 0.0032 | 0.2794 | 0.001 | 0.185 | 0.017 | ASOCIACIÓN |
| E10-A1-d | principal | 1219 | 38 | d_ln_alq | pct10 | 0.001 | 0.0027 | -0.0044 | 0.0065 | 0.714 | 0.0018 | 0.0023 | 0.853 | 1 | 0.0077 | ASOCIACIÓN |
| E10-A1-v1 | variante | 1365 | 38 | ln_alq_2024 | pctpj | 0.0271 | 0.0058 | 0.0154 | 0.0387 | 0 | 0.0028 | 0.2577 | 0.001 | 0 | 0.0206 | no se clasifica |
| E10-A1-v2 | variante | 1364 | 38 | ln_alq_2024 | pct10 | 0.0107 | 0.0056 | -0.0006 | 0.0221 | 0.063 | 0.0032 | 0.2803 | 0.001 | 0.185 | 0.0171 | no se clasifica |
| E10-A1-v3 | variante | 1365 | 38 | ln_alq_2024 | pct10 | 0.0239 | 0.0058 | 0.0122 | 0.0356 | 0 | 0.0038 | 0.3536 | 0.001 | 0 | 0.0234 | no se clasifica |
| E10-A1-v4 | variante | 395 | 37 | ln_alq_2024 | pct10 | -0.0014 | 0.0082 | -0.018 | 0.0153 | 0.8726 | 0.0056 | 0.2095 | 0.001 | 1 | 0.023 | no se clasifica |
| E10-A1-vF | holgura | 1246 | 36 | ln_alq_2024 | pct10 | 0.0125 | 0.0059 | 0.0006 | 0.0243 | 0.0472 | 0.0033 | 0.2579 | 0.001 | — | 0.0186 | no se clasifica |
| E10-A1-d-v1 | variante | 1219 | 38 | d_ln_alq | pctpj | 0.0043 | 0.0016 | 0.001 | 0.0076 | 0.0244 | 0.0013 | 0.0002 | 0.979 | 0.2786 | 0.0059 | no se clasifica |
| E10-A1-d-v2 | variante | 1218 | 38 | d_ln_alq | pct10 | 0.0011 | 0.0027 | -0.0044 | 0.0065 | 0.7121 | 0.0018 | 0.0021 | 0.876 | 1 | 0.0078 | no se clasifica |
| E10-A1-d-v3 | variante | 1219 | 38 | d_ln_alq | pct10 | 0 | 0.0023 | -0.0047 | 0.0046 | 0.9894 | 0.0016 | 0.0013 | 0.925 | 1 | 0.0065 | no se clasifica |
| E10-A1-d-v4 | variante | 394 | 37 | d_ln_alq | pct10 | -0.0002 | 0.0019 | -0.0041 | 0.0037 | 0.925 | 0.0017 | 0.0236 | 0.328 | 1 | 0.0054 | no se clasifica |
| E10-A1-d-vF | holgura | 1100 | 36 | d_ln_alq | pct10 | 0.001 | 0.0029 | -0.0048 | 0.0069 | 0.7371 | 0.0019 | 0.0008 | 0.964 | — | 0.0084 | no se clasifica |


## Diagnósticos del pre-registro

```json
{
 "I5_mismo_signo_variantes": {
  "": 0.75,
  "-d": 0.5
 },
 "mde": {
  "E10-A1": {
   "mde": 0.017,
   "sd_regresor": 2.2056
  },
  "E10-A1-d": {
   "mde": 0.0077,
   "sd_regresor": 2.2118
  },
  "E10-A1-v1": {
   "mde": 0.0206,
   "sd_regresor": 2.802
  },
  "E10-A1-v2": {
   "mde": 0.0171,
   "sd_regresor": 2.2027
  },
  "E10-A1-v3": {
   "mde": 0.0234,
   "sd_regresor": 2.2056
  },
  "E10-A1-v4": {
   "mde": 0.023,
   "sd_regresor": 2.2481
  },
  "E10-A1-vF": {
   "mde": 0.0186,
   "sd_regresor": 2.1002
  },
  "E10-A1-d-v1": {
   "mde": 0.0059,
   "sd_regresor": 2.8081
  },
  "E10-A1-d-v2": {
   "mde": 0.0078,
   "sd_regresor": 2.2087
  },
  "E10-A1-d-v3": {
   "mde": 0.0065,
   "sd_regresor": 2.2118
  },
  "E10-A1-d-v4": {
   "mde": 0.0054,
   "sd_regresor": 2.2201
  },
  "E10-A1-d-vF": {
   "mde": 0.0084,
   "sd_regresor": 2.102
  }
 },
 "moran": {
  "E10-A1": {
   "I": 0.2794,
   "p_permutacion": 0.001,
   "k_vecinos": 8,
   "esperado_bajo_nulo": -0.0007
  },
  "E10-A1-d": {
   "I": 0.0023,
   "p_permutacion": 0.853,
   "k_vecinos": 8,
   "esperado_bajo_nulo": -0.0008
  }
 },
 "conley_10km": {
  "E10-A1": {
   "se_conley": 0.0032085071218415553,
   "t": 3.3294592090116013,
   "vecinos_medios_en_el_corte": 4.01025641025641,
   "var_positiva": true
  },
  "E10-A1-d": {
   "se_conley": 0.001781231233147999,
   "t": 0.5883555016682924,
   "vecinos_medios_en_el_corte": 3.970467596390484,
   "var_positiva": true
  }
 },
 "dato_titularidad": "cota inferior: el tramo se cuenta dentro del municipio (la mediana municipal es 0)",
 "datos_parciales_v17": "V17: titulares de más de 10 viviendas con el 4,2 % del parque (Catastro 2026; V17-AUD-OT-CAT-GT-PARQUE-2026) y entre el 2 y el 12 % del alquiler habitual con supuestos; no se duplica"
}
```
