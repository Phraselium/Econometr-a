# V16 · Q2 · Vivienda turística (grupo A, entrenamiento)

**Capa C4, pendiente de evaluación sellada.** Asociaciones en forma reducida, sin lenguaje causal. Fecha de corte 2026-10-17. Herramientas: NO APTO (Q2a: tamaño 0,142; Q2c: 0,0975) → solo descriptivo; BLP/GATES NO APTO (tamaño 0,005; cobertura 0,9885) → solo descriptivo. **Sin p-valor ni IC.**

<a id="v16-q2-1"></a>
## Q2a · DiD de intensidad (principal)
log IPC de alquiler provincial (media anual) ~ exposición × posterior + efectos fijos de provincia y año. Exposición: log del % de viviendas turísticas INE de 2020-08, estandarizado (DT del log = 0,947). Pre 2017-2019, post 2022-2025, sin 2020-2021; N = 287.
- Coeficiente: **0,0132 por DT** (elasticidad 0,0139). Referencia pre-registrada: 0,0379 por DT (0,04 × DT del log). La estimación puntual es 0,35 veces la referencia.
- Sin grandes ciudades: 0,0118. Con controles (renta, población, extranjeros × posterior): 0,0071; misma muestra sin controles: 0,0133.
- Estudio de eventos (base 2019): 2012: -0,0053, 2013: -0,0064, 2014: -0,0072, 2015: -0,0078, 2016: -0,0061, 2017: -0,0059, 2018: -0,0044, 2022: 0,0052, 2023: 0,0075, 2024: 0,0112, 2025: 0,0150.

<a id="v16-q2-2"></a>
**Placebo de fecha** (post falso 2016-2019): 0,0026 por DT.

<a id="v16-q2-3"></a>
## Q2c · exposición INE-VUT municipal frente al IPVA-TAM
log IPVA-TAM ~ z(log % VUT) + efectos fijos de municipio y año, 2021-2024; 388 municipios, N = 1524 (municipio-años con 0 % fuera).
- Coeficiente: **-0,0095 por DT** (referencia 0,0633). Variantes (nivel, Δlog, sin grandes ciudades, controles): 0,0078; -0,0005; -0,0054; -0,0095; -0,0091.
- Multiverso (6 especificaciones): mediana -0,0072, rango [-0,0095; 0,0078], mismo signo que la principal en 83 %. Se lee como robustez de H3.

<a id="v16-q2-4"></a>
## Q2b · solo robustez (Andalucía)
Dosis = altas acumuladas de viviendas completas (OpenRTA, reconstruida con sesgo de supervivencia). 8 especificaciones: mediana 0,00020; mismo signo que la primera en 62 %. Sin inferencia.

<a id="v16-q2-5"></a>
## BLP/GATES (descriptivo, NO APTO)
- Q2a (n = 37): pendiente media 0,0113; GATES por cuartil [0.0116, 0.0139, 0.0097, 0.0044].
- Q2c (n = 374): pendiente media -0,0098; GATES por cuartil [-0.005, -0.0132, -0.0135, 0.0054].
- Moderadores: renta ADRH, población, cuota de extranjeros, obra nueva per cápita (y % VUT 2021 en Q2c; en Q2a coincide con la exposición). Subgrupos descriptivos C4.

## Diagnósticos (superados y fallidos)
| Prueba | Estado | Detalle |
|---|---|---|
| Q2a · pretendencias (estudio de eventos, base 2019) | informativa (sin umbral pre-registrado) | coeficientes 2012-2018: 2012 -0,0053, 2013 -0,0064, 2014 -0,0072, 2015 -0,0078, 2016 -0,0061, 2017 -0,0059, 2018 -0,0044; pendiente lineal previa 0,00018/año |
| Q2a · Honest DiD | no evaluable | no validado en la fase 5 |
| Q2a · placebo de fecha (post falso 2016-2019 frente a 2012-2015) | informativa | 0,0026 por DT frente a 0,0132 del principal |
| Q2a · exclusión de grandes ciudades | informativa | 0,0118 (mismo signo) |
| Q2a · Oster | superada | δ = 1,84 |
| Q2a · Cinelli-Hazlett | superada | RV_q=1 = 0,197 |
| Q2a · E-value (puntual) | informativa | 2,98 |
| Q2a · Moran de residuos | informativa | I = -0,058, p diagnóstico = 0,921 |
| Q2a · Breusch-Pagan | informativa | p = 0,878 |
| Q2a · ruptura (Bai-Perron) brecha tercil alto − bajo | informativa | 2 rupturas: ['2019Q2', '2023Q1'] |
| Q2a · balance (terciles de exposición) | informativa | ln_renta 0,14; ln_pob 1,85; cuota_extranj 1,00; obra_pc 0,01 |
| Q2a · F efectivo de Montiel Olea-Pflueger / AKM / Rotemberg | no aplica | shift-share retirado (no hay pernoctaciones por país en disco): forma reducida |
| Q2c · Oster | superada | δ = 8,82 |
| Q2c · Cinelli-Hazlett | superada | RV_q=1 = 0,125 |
| Q2c · exposición adelantada (placebo temporal) | informativa | -0,0048 por DT |
| Q2c · Moran (por provincia, aproximado) | informativa | I = 0,001, p diagnóstico = 0,061 |
| Q2c · Breusch-Pagan | fallida (heterocedasticidad) | p = 4.9e-09 |
| Q2c · exclusión de grandes ciudades | informativa | -0,0095 |
| Controles negativos (población 65+, IPC general provincial) | no evaluable | no están en el entrenamiento |
| Raíces unitarias / cointegración con dependencia transversal | no aplica | diferencias sobre ventanas cortas |
| BLP/GATES (adenda, punto 13) | no evaluable como prueba | herramienta NO APTA: solo puntuales, descriptivos (ver detalle) |

## Límites
Todo es asociación en forma reducida (C4). Solapes declarados: V9-D2 y H3. La conclusión publicada sobre vivienda turística es «no concluyente»: este resultado no la cambia. Q2c se lee como robustez de H3. Q2b es solo robustez, con dosis reconstruida (sesgo de supervivencia). El multiverso de 32 especificaciones de Q2a era del shift-share retirado y no se ejecuta (D3). Sin errores típicos no se calculan tipo S ni M: la condición (b) no es evaluable. Pernoctaciones por país y municipio: tarea del autor.
Lista de p-valores para el control BY: vacía. Ficha reproducible: `python3 src/v16/q2_turismo.py` (SEED=20261010); entradas en data/processed/v16/entrenamiento; salidas en output/v16/q2/ (q2_detalle.json, registro.csv).
