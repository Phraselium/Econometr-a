# rejilla_twfe · especificación principal de la rejilla fija (TWFE, exposición continua)

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/rejilla_twfe.py)
```
Monte Carlo V16 (fase 5) · TWFE de la rejilla fija (output/v16/potencia/rejilla_fija.csv), dos escalas representativas.

Proceso generador (declarado en docs/v16/validacion_montecarlo/rejilla_twfe.md ANTES de simular):
  ESTRUCTURA (leída; sin valores del resultado): MUNICIPIO = unidades de entrenamiento con SERPAVI (2.014; clusters = su provincia);
  PROVINCIA = las 41 provincias de entrenamiento (cada una es su cluster). Ventana 2019-2025 (7 años => 6 diferencias).
  Especificación principal (rejilla): Dlog resultado_it = a_i + l_t + b x_it + u_it, con x_it = z_i * 1[t >= 2023] (exposición continua
  estandarizada, DiD de intensidad), efectos fijos de unidad y de periodo.
  EXPOSICIÓN z_i: campo gaussiano espacial estandarizado (alcance 150 km municipal; 300 km provincial) => correlación espacial.
  RESULTADO SIMULADO (log, en niveles; se toman diferencias): y_it = mu_i + d_i t + g_i1 f_1t + g_i2 f_2t + eta_p(i),t + s_it + e_it
    municipio: f AR(1) rho 0,6 sd 0,03; g_i1 ~ N(1; 0,5); g_i2 campo (150 km) N(0,1); eta provincia-año AR(1) rho 0,5 sd 0,02;
      s_it campo exp(-d/100 km) AR(1) rho 0,5 sd 0,02; e_it AR(1) rho 0,5 sd 0,05 exp(0,4 z_h - 0,08); d_i ~ N(0; 0,005)
    provincia: f AR(1) rho 0,6 sd 0,05; g_i1 ~ N(1; 0,4); g_i2 campo (300 km) N(0; 0,5); s_it campo (150 km) AR(1) 0,5 sd 0,03;
      e_it AR(1) rho 0,5 sd 0,05 exp(0,3 z_h - 0,045); d_i ~ N(0; 0,003)
  EFECTO sobre el crecimiento: nulo b = 0; alternativas b = 0,04 (magnitud de referencia Q2: 0,04 por DT de exposición; cobertura) y
  b = 0,01 (potencia); heterogeneidad b_i = b (1 + 0,5 z_h); verdad = media de b_i ponderada por x_it^2 (la que estima TWFE sin sesgo si
  b_i es independiente de x).
Inferencia: municipio = errores agrupados por provincia (CR1, t con G-1 gl); provincia = wild cluster bootstrap-t de Webb con el nulo
  impuesto (B = 999), cluster = provincia. Informativo (no cambia el veredicto): wild de Webb en la escala municipal no se calcula.
```

<!-- RESULTADOS -->
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
| escala | escenario | b | n_unidades | n_clusters | R | sesgo | rmse | cobertura | rechazo | ancho_medio_ic |
|---|---|---|---|---|---|---|---|---|---|---|
| municipio | nulo | 0.0000 | 2014 | 41 | 2000 | 0.0001 | 0.0052 | 0.7970 | 0.2030 | 0.0126 |
| municipio | alt_ref_0.04 | 0.0400 | 2014 | 41 | 2000 | 0.0001 | 0.0056 | 0.8055 | 0.9995 | 0.0132 |
| municipio | alt_pot_0.01 | 0.0100 | 2014 | 41 | 1000 | -0.0001 | 0.0056 | 0.7970 | 0.7800 | 0.0129 |
| municipio | control_iid_nulo | 0.0000 | 2014 | 41 | 1000 | -0.0000 | 0.0009 | 0.9490 | 0.0510 | 0.0036 |
| provincia | nulo | 0.0000 | 41 | 41 | 2000 | 0.0001 | 0.0092 | 0.8890 | 0.1105 | 0.0308 |
| provincia | alt_ref_0.04 | 0.0400 | 41 | 41 | 2000 | 0.0000 | 0.0092 | 0.9545 | 0.9600 | 0.0398 |
| provincia | alt_pot_0.01 | 0.0100 | 41 | 41 | 1000 | -0.0002 | 0.0092 | 0.9130 | 0.2780 | 0.0319 |
| provincia | control_iid_nulo | 0.0000 | 41 | 41 | 1000 | -0.0001 | 0.0066 | 0.9540 | 0.0440 | 0.0278 |

## Veredicto
**municipio: NO APTO → diseño solo descriptivo; provincia: NO APTO → diseño solo descriptivo**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{
 "municipio": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": false,
  "fallos": [
   "tamaño 0.2030 fuera de [0,04; 0,06]",
   "cobertura 0.8055 fuera de [0,92; 0,97]"
  ],
  "tamano": 0.203,
  "R_nulo": 2000,
  "cobertura_alt": 0.8055,
  "R_alt": 2000,
  "cobertura_nulo": 0.797,
  "sesgo_nulo": 8.460748974844136e-05,
  "rmse_nulo": 0.005193202568052,
  "se_mc_tamano": 0.00899419257076476,
  "se_mc_cobertura": 0.00885069912492793
 },
 "provincia": {
  "apto": false,
  "tamano_ok": false,
  "cobertura_ok": true,
  "fallos": [
   "tamaño 0.1105 fuera de [0,04; 0,06]"
  ],
  "tamano": 0.1105,
  "R_nulo": 2000,
  "cobertura_alt": 0.9545,
  "R_alt": 2000,
  "cobertura_nulo": 0.889,
  "sesgo_nulo": 9.559865025309044e-05,
  "rmse_nulo": 0.0091650654084672,
  "se_mc_tamano": 0.0070103405766053905,
  "se_mc_cobertura": 0.004659922209651143
 }
}
```

## Notas y límites
Escalas representativas de la especificación principal de la rejilla: municipio (2014 unidades, 41 provincias, CR1 con t(G-1)) y provincia (41, wild bootstrap-t de Webb con nulo impuesto). La adenda no nombra alternativa para la rejilla: si la principal falla, la escala es solo descriptiva. Tamaño municipal 0.2030, provincial 0.1105; cobertura bajo b=0,04: 0.8055 y 0.9545. Control iid (exposición y ruido independientes): tamaño 0.051 (municipio) y 0.044 (provincia), de modo que el procedimiento está bien implementado y el exceso de rechazo procede de la correlación espacial de la exposición con cargas de factores y choques espaciales que cruzan fronteras de provincia (el agrupamiento por provincia no los absorbe). Potencia: municipio {'b=0.04': 0.9995, 'b=0.01': 0.78}, provincia {'b=0.04': 0.96, 'b=0.01': 0.278}. Consecuencia: las 83 celdas de la rejilla con TWFE y exposición espacial no deben llevar p-valor calibrado; se leen como descriptivas, o con una inferencia espacial (Conley) validada aparte.

## Reproducción
`python3 src/v16/montecarlo/rejilla_twfe.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/rejilla_twfe/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.
