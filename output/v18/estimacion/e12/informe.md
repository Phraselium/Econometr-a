# E12 · Vivienda protegida y obra libre (estilo Chapelle)

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.*

## Lectura

- **E12-A1** (38 provincias × 23 años): 2SLS 6.507 viviendas libres iniciadas por vivienda protegida calificada; F efectivo 7.90; AR 95 % [-1.19; 170.04]; p Webb del AR en 0 = 0.113; MDE(β) 11.72 frente a |Chapelle| = 1.604. Clase provisional **NO ESTIMABLE** (estimación informativa, fuera de clasificación y de la familia de Holm: el MDE supera el umbral de la adenda 1.3).
- **E12-A2** (valor tasado real): 2SLS 22.084 % por 100 protegidas por 100 del parque; F efectivo 4.35; AR toda la recta salvo (-67.94; 9.05): no acotado; p Webb 0.000. Clase provisional **ASOCIACIÓN**.
- Mide la vivienda **protegida** (calificaciones definitivas), no la pública (E12-X1 NO ESTIMABLE por falta de promociones públicas por municipio y año: tarea del autor, punto 11).
- Tope SUGESTIVO. Las variantes heredan la clase de su principal; E12-A1-v3 (libres terminadas) no se estima por falta de la clave de sellado.

## Tabla de especificaciones

| id | estado | muestra | N | G | beta_2sls | se_cr1 | F_efectivo | ar_tipo | ar_lo | ar_hi | p_webb | p_holm | q_BY_variantes | mde_beta | umbral_mde | estimable | clasificacion_v18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E12-X1 | NO ESTIMABLE | — | — | — | — | — | — | — | — | — | — | — | — | — | — | False | NO ESTIMABLE |
| E12-A1-v3 | variante | — | — | — | — | — | — | — | — | — | — | — | — | — | — | False | no se clasifica |
| E12-A1 | principal | 2002-2024 | 874 | 38 | 6.5067 | 5.6995 | 7.8993 | intervalo | -1.1918 | 170.0367 | 0.1125 | — | — | 11.724 | 1.604 | False | NO ESTIMABLE |
| E12-A1-v1 | variante | 2002-2024 | 874 | 38 | 4.4909 | 5.359 | 6.3639 | complemento | -92.7725 | -2.6542 | 0.321 | — | 0.5886 | 11.386 | 1.604 | False | NO ESTIMABLE |
| E12-A1-v2 | variante | 2002-2024 | 851 | 37 | 6.7716 | 6.3767 | 6.5222 | complemento | -507.2472 | -1.594 | 0.1511 | — | 0.4156 | 12.828 | 1.604 | False | NO ESTIMABLE |
| E12-A1-v4 | variante | 2002-2013 | 456 | 38 | 94.0749 | 351.7178 | 0.0888 | complemento | -15.4988 | -2.8648 | 0.0399 | — | 0.2195 | 153.811 | 1.604 | False | NO ESTIMABLE |
| E12-A1-sin-atipicos | diagnóstico | 2002-2024 | 828 | 36 | 12.4061 | 11.1537 | 3.2549 | complemento | -102.9811 | -0.4451 | 0.026 | — | — | 18.863 | 1.604 | False | no se clasifica |
| E12-A2 | principal | 2003-2024 | 726 | 33 | 22.084 | 12.4289 | 4.3494 | complemento | -67.9357 | 9.047 | 0.0003 | 0.0003 | — | 19.226 | — | True | ASOCIACIÓN |
| E12-A2-v1 | variante | 2003-2024 | 704 | 32 | 21.9526 | 14.3607 | 3.2335 | complemento | -42.5377 | 8.0786 | 0.0001 | — | 0.0003 | 19.203 | — | True | ASOCIACIÓN |
| E12-A2-v2 | variante | 2003-2013 | 363 | 33 | 147.2348 | 419.4471 | 0.1416 | recta | — | — | 0.0782 | — | 0.1173 | 231.032 | — | True | ASOCIACIÓN |


## Diagnósticos del pre-registro

```json
{
 "pretendencias_y_exclusion": {
  "pretendencia_instrumento_2002_2007_sobre_variacion_libre_1996_2001": {
   "coef": -0.4327,
   "se_hc1": 0.7278,
   "p": 0.5559,
   "N": 38,
   "unidad": "variación de la obra libre iniciada 1996-2001 frente a 1991-95 por 100 viviendas del parque de 2001, por unidad del instrumento medio"
  },
  "exclusion_cuota_sobre_pib_1995_2001": {
   "p": null,
   "nota": "NO VERIFICABLE: el PIB provincial (data/raw/ine_v2_cre.csv) empieza en 2000; solo habría el crecimiento 2000-2001. Tope SUGESTIVO (ya es el tope de la especificación)."
  }
 },
 "I5_signo": {
  "A1": 1.0,
  "A1_sin_atipicos_mismo_signo": true,
  "A2": 1.0
 },
 "atipicos_excluidos": "A1 sin atípicos (02, 29)",
 "holm": {
  "m": 1,
  "valores": {
   "E12-A2": 0.00030003000300030005
  }
 },
 "BY_variantes": {
  "E12-A1-v1": 0.5886,
  "E12-A1-v2": 0.4156,
  "E12-A1-v4": 0.2195,
  "E12-A2-v1": 0.0003,
  "E12-A2-v2": 0.1173
 },
 "cd_pesaran_A1": {
  "CD": 1.8673,
  "p": 0.0619,
  "rho_medio": 0.0147
 },
 "mde": {
  "E12-A1": {
   "mde_beta": 11.724,
   "umbral": 1.604,
   "estimable": false,
   "R": 2000
  },
  "E12-A1-v1": {
   "mde_beta": 11.386,
   "umbral": 1.604,
   "estimable": false,
   "R": 2000
  },
  "E12-A1-v2": {
   "mde_beta": 12.828,
   "umbral": 1.604,
   "estimable": false,
   "R": 2000
  },
  "E12-A1-v4": {
   "mde_beta": 153.811,
   "umbral": 1.604,
   "estimable": false,
   "R": 2000
  },
  "E12-A1-sin-atipicos": {
   "mde_beta": 18.863,
   "umbral": 1.604,
   "estimable": false,
   "R": 2000
  },
  "E12-A2": {
   "mde_beta": 19.226,
   "umbral": null,
   "estimable": true,
   "R": 2000
  },
  "E12-A2-v1": {
   "mde_beta": 19.203,
   "umbral": null,
   "estimable": true,
   "R": 2000
  },
  "E12-A2-v2": {
   "mde_beta": 231.032,
   "umbral": null,
   "estimable": true,
   "R": 2000
  }
 },
 "driscoll_kraay": "NO APTO con T <= 30 (V18 montecarlo/driscoll_kraay): solo etiqueta",
 "instrumento": "cuota de protegida 1991-95 × calificaciones de las demás provincias no selladas; 1/HHI no aplica (un solo choque nacional)"
}
```
