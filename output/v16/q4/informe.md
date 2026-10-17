# Q4 · Oferta municipal y restricción física (V16, fase 6)

**Capa C4, descriptiva. Asociación C4; pendiente de evaluación sellada. Sin lenguaje causal.** Datos de entrenamiento; desviaciones D2 en docs/v16/desviaciones.md. Registro: output/v16/q4/registro.csv.

## Resultado
| Diseño | Estimación puntual | Inferencia |
|---|---|---|
| Q4a: log obra neta (obra > 0), 2018-2025, 4374 municipios, N = 18184 | -0,1297 por DT de Red Natura (31,8 pp), con FE de provincia y año | ninguna (agrupación provincial NO APTA) |
| Q4b: Δlog SERPAVI (VC), 2018-2022, 1293 municipios, N = 6105 | interacción -0,0014 (choque principal 0,0076) | ninguna |

Multiverso (sin IC): Q4a 8 especificaciones, mediana -0,0397, 100 % con el mismo signo (las variantes asinh tienen otra escala); Q4b 8, mediana -0,0018, 100 %.

## Pruebas
- Superadas: Q4a: sin grandes ciudades, mismo resultado (-0,1294); Q4a: periodo 2012-2016 de signo igual (-0,1109; no es placebo); Q4b: sin grandes ciudades, mismo signo (-0,0014).
- Fallidas: Q4a: dependencia espacial de residuos (Moran I = 0,346, p de permutación 0,001); Q4b: placebo de choque adelantado de igual signo y mayor tamaño que el efecto (-0,0021 frente a -0,0014); Q4a y Q4b: la Red Natura no es exógena (restricción de uso del suelo correlacionada con rural y despoblación).
- No evaluables: inferencia con agrupación provincial (rejilla TWFE provincia NO APTA): sin p-valor ni IC; Cinelli-Hazlett (requiere t válido); costa, pendiente, agua y planeamiento: no están en disco (tareas del autor).
- Sensibilidad Q4a: Oster δ = 11,2 (no frágil por la regla δ < 1); E-value del punto 1,39. Q4b: E-value del punto 1,10.
- Heterocedasticidad Q4a (BP LM) 62,3; autocorrelación (Wooldridge) -0,41 frente a -0,5.

## Regla de hallazgo
Sin p-valor propio (NO APTO) y sin magnitud de referencia: (a) pendiente, (b) no se cumple, (c) pendiente. **Sin hallazgo.** No hay conclusión publicada sobre elasticidad municipal: sin contradicción.

## Fichas reproducibles
Comando: `python src/v16/q4_oferta.py && python src/v16/qb_informe.py`.
- <a id="q4a"></a>**q4a.** log(obra neta > 0) del Catastro ~ % Red Natura estandarizado + FE provincia + FE año, 2018-2025. Rango = 8 variantes (log/asinh, control log unidades 2017, 2018-2025/2018-2021).
- <a id="q4b"></a>**q4b.** Δlog mediana €/m² SERPAVI municipal (VC) ~ (Δx_mt × RN_std) + Δx_mt + FE año; Δx = cambio anual del shift-share municipal (cuotas del padrón de 2003, 28 orígenes, sin la provincia). Rango = 8 variantes (VC/VU, 2018-2022/2018-2020, FE año/provincia×año).
