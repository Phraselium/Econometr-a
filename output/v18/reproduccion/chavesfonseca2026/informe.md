# Reproduccion de Chaves-Fonseca (2026), tabla 2 (precios)

**Rotulo: reproduccion del estudio original con sus datos; no usa datos del proyecto.**

- Estudio: Chaves-Fonseca (2026), SERIEs, DOI 10.1007/s13209-026-00335-2. Paquete CC BY 4.0, figshare 10.6084/m9.figshare.26263979.v2 (version 2 del 7-4-2026).
- Codigo original: Stata (`code/01_analysis_main.do`, lineas 371-519; reghdfe/ivreghdfe). Sin Stata: traducido a Python (pandas, statsmodels, linearmodels 7.0; efectos fijos por variables ficticias; `pandas.read_stata`, sin pyreadstat).
- Semilla 20261010 (la estimacion es determinista, no hay aleatoriedad).
- Aviso territorial: Madrid es provincia sellada en la validacion v6 del proyecto. Reproducir el estudio con los datos de su autor no la toca, pero la replica con datos del proyecto en Madrid no se hara.
- Decisiones de traduccion: `egen group(year)` -> rango denso del ano; tendencia `c.dist_sol#c.time` y `#c.time^2` con distancia en km; IV con una sola excluida `ln(share_iv_top3) x search_interest`; error tipico agrupado por barrio. OLS: correccion reghdfe (G/(G-1)*(N-1)/(N-K), con efectos de barrio anidados excluidos de K). IV: sin correccion de gl (ivreghdfe sin `small`). F de primera etapa: t^2 agrupado sin ajuste de muestra finita (aproximacion al rk Wald F de Kleibergen-Paap; difiere ~2 % de la publicada por el ajuste de grados de libertad de ivreg2, no replicado).

## Comparacion con tab_2.tex (variable dependiente: log precio; coeficiente por 100 anuncios)

| Col | Tipo | Repro | EE repro | Publicado | EE publ. | Dif abs | Dif rel | F repro | F publ. | N | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MCO | 0.0609 | 0.0170 | 0.061 | 0.017 | -0.0001 | -0.2% |  |  | 1029 | coincide |
| 2 | MCO | 0.0238 | 0.0071 | 0.024 | 0.007 | -0.0002 | -0.7% |  |  | 1029 | coincide |
| 3 | MCO | 0.0247 | 0.0045 | 0.025 | 0.005 | -0.0003 | -1.2% |  |  | 1029 | coincide |
| 4 | MCO | 0.0146 | 0.0027 | 0.015 | 0.003 | -0.0004 | -2.9% |  |  | 1029 | coincide |
| 5 | MCO | 0.0142 | 0.0028 | 0.014 | 0.003 | 0.0002 | 1.6% |  |  | 1029 | coincide |
| 6 | IV | 0.0197 | 0.0044 | 0.020 | 0.004 | -0.0003 | -1.8% | 21.131 | 20.691 | 1029 | coincide |
| 7 | IV | 0.0215 | 0.0047 | 0.022 | 0.005 | -0.0004 | -2.1% | 16.327 | 15.955 | 1029 | coincide |

N publicado: 1029. Veredicto global: **coincide**.

## Alcance y limites

- Reproducido: tabla 2 (cols. 1-7). No reproducidos: tabla 4 (movilidad: requiere ivreghdfe con tendencias por valor base, no hecho por tiempo), tabla 5 (mediacion `ivmediate`) y alquileres (revision); no se contrastan con el texto del articulo (solo resumen y tablas del paquete).
- No se redistribuyen datos del paquete: aqui solo hay coeficientes y estadisticos agregados.
- Dependencia anotada: `pip install linearmodels` (ya instalado, version 7.0).
