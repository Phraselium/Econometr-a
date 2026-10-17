# sdid_conley_taber · Q1b · SDID con Conley-Taber (principal) y wild bootstrap de Webb (alternativa)

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/sdid_conley_taber.py)
```
Monte Carlo V16 (fase 5) · SDID con inferencia de Conley-Taber (principal) y wild cluster bootstrap de Webb (alternativa), Q1b.

Proceso generador (declarado en docs/v16/validacion_montecarlo/sdid_conley_taber.md ANTES de simular):
  ESTRUCTURA (leída de entrenamiento y de intervenciones.csv, sin valores del resultado): municipios de entrenamiento con SERPAVI completo
  en 2019-2022 y 2024; tratados = municipios con zona tensionada declarada fuera de Cataluña; donantes = municipios de CCAA sin zonas;
  clusters = provincia; años 2019..2024 con 2023 fuera del estimador (pre 2019-2022, post 2024).
  RESULTADO SIMULADO (log SERPAVI €/m²): y_it = mu_i + d_i*t + sum_k g_ik f_kt + eta_{p(i),t} + s_it + e_it
    f_1, f_2 factores comunes AR(1) rho 0,6, sd 0,03; g_i1 ~ N(1; 0,5), g_i2 = campo espacial (alcance 150 km) N(0,1)
    eta: choque provincia-año AR(1) rho 0,5, sd 0,02;  s_it: campo gaussiano espacial exp(-d/100 km), AR(1) rho 0,5, sd 0,02
    e_it: AR(1) rho 0,5, sd marginal 0,05 * exp(0,4 z_i - 0,08) (heterocedasticidad entre municipios)
    d_i ~ N(0; 0,005) tendencia propia. Valores declarados, no estimados con datos reales.
  EFECTO (solo en el año post): nulo = 0; alternativa = -0,0075 (magnitud de referencia de la adenda) con heterogeneidad
  tau_i = tau (1 + 0,5 z_i); la verdad de la cobertura es el ATT muestral (media de tau_i en tratados).
Escenarios: A (estructura real: 2 tratados, 1 provincia) y B (diseño ampliado: patrón de las 8 zonas declaradas 15:2, 20:2, 48:3, 01:1).
```

<!-- RESULTADOS -->
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
| escenario | inferencia | efecto | n_tratados | n_donantes | R | sesgo | rmse | cobertura | rechazo | ancho_medio_ic |
|---|---|---|---|---|---|---|---|---|---|---|
| A | ct | nulo | 2 | 930 | 2000 | -0.0016 | 0.0588 | 0.9425 | 0.0575 | 0.2297 |
| A | webb | nulo | 2 | 930 | 2000 | -0.0016 | 0.0588 | 0.2205 | 0.7795 | 0.0263 |
| A | ct | ref | 2 | 930 | 1000 | -0.0011 | 0.0591 | 0.9430 | 0.0620 | 0.2280 |
| A | webb | ref | 2 | 930 | 1000 | -0.0011 | 0.0591 | 0.2070 | 0.8180 | 0.0266 |
| A | ct | mde | 2 | 930 | 300 | -0.0045 | 0.0580 | 0.9567 | 0.3233 | 0.2277 |
| A | webb | mde | 2 | 930 | 300 | -0.0045 | 0.0580 | 0.1567 | 0.9000 | 0.0220 |
| B | ct | nulo | 2 | 930 | 2000 | -0.0017 | 0.0605 | 0.9350 | 0.0650 | 0.2294 |
| B | webb | nulo | 2 | 930 | 2000 | -0.0017 | 0.0605 | 0.2080 | 0.7920 | 0.0264 |
| B | ct | ref | 2 | 930 | 1000 | -0.0010 | 0.0608 | 0.9290 | 0.0760 | 0.2274 |
| B | webb | ref | 2 | 930 | 1000 | -0.0010 | 0.0608 | 0.1970 | 0.7990 | 0.0270 |
| B | ct | mde | 2 | 930 | 300 | -0.0050 | 0.0577 | 0.9600 | 0.3167 | 0.2275 |
| B | webb | mde | 2 | 930 | 300 | -0.0050 | 0.0577 | 0.1433 | 0.9033 | 0.0228 |

## Veredicto
**APTO (Conley-Taber, escenario A; en el límite superior del tamaño, ver notas)**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{
 "A_ct": {
  "apto": true,
  "tamano_ok": true,
  "cobertura_ok": true,
  "fallos": [],
  "tamano": 0.0575,
  "R_nulo": 2000,
  "cobertura_alt": 0.943,
  "R_alt": 1000,
  "cobertura_nulo": 0.9425,
  "sesgo_nulo": -0.0016154805824415,
  "rmse_nulo": 0.0587989633217807,
  "se_mc_tamano": 0.005205465877325487,
  "se_mc_cobertura": 0.007331507348424336
 },
 "A_webb": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.7795 fuera de [0,04; 0,06]",
   "cobertura 0.2070 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.7795,
  "R_nulo": 2000,
  "cobertura_alt": 0.207,
  "R_alt": 1000,
  "cobertura_nulo": 0.2205,
  "sesgo_nulo": -0.0016154805824415,
  "rmse_nulo": 0.0587989633217807,
  "se_mc_tamano": 0.009270376205958419,
  "se_mc_cobertura": 0.012812142677944232
 },
 "B_ct": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": true,
  "fallos": [
   "tamaño 0.0650 fuera de [0,04; 0,06]"
  ],
  "tamano": 0.065,
  "R_nulo": 2000,
  "cobertura_alt": 0.929,
  "R_alt": 1000,
  "cobertura_nulo": 0.935,
  "sesgo_nulo": -0.0016752745748473,
  "rmse_nulo": 0.0605052989557364,
  "se_mc_tamano": 0.005512485827646181,
  "se_mc_cobertura": 0.008121514637061239
 },
 "B_webb": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.7920 fuera de [0,04; 0,06]",
   "cobertura 0.1970 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.792,
  "R_nulo": 2000,
  "cobertura_alt": 0.197,
  "R_alt": 1000,
  "cobertura_nulo": 0.208,
  "sesgo_nulo": -0.0016752745748473,
  "rmse_nulo": 0.0605052989557364,
  "se_mc_tamano": 0.009075681792570737,
  "se_mc_cobertura": 0.012577400367325514
 }
}
```

## Notas y límites
Hallazgo de estructura: con los datos de entrenamiento, el diseño literal de la adenda (tratados = municipios con zona vigente fuera de Cataluña, con SERPAVI completo 2019-2022 y 2024) tiene 2 municipios en 1 provincia (['15']) y 930 donantes en 30 provincias; las zonas de esos dos municipios entran en vigor en 2025-2026, es decir, DESPUÉS del año post (2024): en entrenamiento hay 0 municipios con zona vigente en 2024 fuera de Cataluña. El resto de zonas fuera de Cataluña (Álava, Gipuzkoa, Bizkaia) está en territorios forales sin SERPAVI, por lo que el escenario B del docstring (reparto 15:2, 20:2, 48:3, 01:1) no pudo construirse y resultó ser el mismo conjunto de 2 tratados con otra realización de la geometría simulada (B = réplica independiente de A, no un diseño distinto). Veredicto sobre A (proceso del repositorio, declarado antes de simular). Resultados A: Conley-Taber tamaño 0.0575 (error MC 0.0052), cobertura bajo tau=-0,0075 0.9430, bajo el nulo 0.9425. La réplica B queda fuera del intervalo (tamaño 0.0650, cobertura 0.9290); agrupando A y B (4.000 réplicas nulas) el tamaño es 0.0612 (error MC 0.0038): la calibración es CASI en el límite del criterio, no holgada. Alternativa Webb (solo se informa): tamaño 0.7795 y cobertura 0.2070; con un único cluster tratado el bootstrap degenera (no se debe usar). Potencia de Conley-Taber a -7,1 % (MDE de la adenda): 0.323; a -0,75 % es prácticamente el tamaño. El IC medio mide 0.230 de ancho (en log): con 2 municipios tratados el diseño no distingue efectos de la magnitud de la literatura y su lectura es la de un nulo no concluyente. Los pesos SDID se estiman por FISTA (40 iteraciones) con regularización a la Arkhangelsky et al.; en la alternativa Webb los pesos se mantienen fijos.

## Reproducción
`python3 src/v16/montecarlo/sdid_conley_taber.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/sdid_conley_taber/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.
