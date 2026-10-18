# Q6 · Fiscalidad de la compra: tipo general del ITP (V16, fase 6)

**Capa C4, descriptiva. Asociación C4; pendiente de evaluación sellada. Sin lenguaje causal.** Datos de entrenamiento; desviaciones D2. Registro: output/v16/q6/registro.csv.

## Resultado (dCDH, dosis continua, por punto de tipo; sin p-valor ni IC: aleatorización NO APTA)
| Resultado | Estimación | Referencia de la adenda | Rango del multiverso (8) | Con el mismo signo |
|---|---|---|---|---|
| Q6-v log compraventas (N = 504) | 0,0251 | -0,07 | 0,0025 a 0,0251 | 100 % |
| Q6-p log valor tasado (N = 480) | -0,0020 | -0,01 | -0,0155 a 0,0064 | 83 % |

TWFE de referencia: Q6-v 0,0157; Q6-p -0,0047. Subidas/bajadas por separado: Q6-v 0,0055 / -0,0279; Q6-p -0,0030 / -0,0043.

## Pruebas
- Superadas: Q6-p: placebo con ΔY retardado pequeño (-0,0079); Q6-p: sin grandes ciudades, mismo signo (-0,0017); Q6-v y Q6-p: control negativo (log población) cercano a 0 (-0,0041).
- Fallidas: Q6-v: placebo con ΔY retardado de signo opuesto y mayor tamaño que el efecto (-0,0484 frente a 0,0251); Q6-v: la estimación principal tiene signo opuesto a la referencia (-0,07 por punto); las bajadas (-0,0279) tienen el signo de la referencia y las subidas son casi nulas (0,0055): lectura no unívoca; Q6-v/Q6-p: el diseño tiene 14 cambios en 8 CCAA, concentrados en 2012-2013: en 2012 no hay estables que cumplan la exclusión de anticipación.
- No evaluables: inferencia por aleatorización del calendario (dCDH NO APTO): sin p-valor ni IC; Honest DiD (no validado); Cinelli-Hazlett (requiere t válido); Oster (no aplica al Wald-DID); TOST (sin SE).
- E-value del punto: Q6-v 1,69; Q6-p 1,30. Moran de residuos TWFE: 0,108 / -0,017.

## Regla de hallazgo
(a) sin p-valor propio; (b) magnitud numérica disponible, pero sin SE válido los errores S y M no son evaluables; (c) pendiente. **Sin hallazgo.** Q6-v: signo opuesto a la referencia, con un placebo mayor que el efecto: no se interpreta. Q6-p: signo y orden de magnitud cercanos a la referencia (razón 0,20), solo puntual. No hay conclusión publicada de la 1.0 sobre el ITP: sin contradicción.

## Fichas reproducibles
Comando: `python src/v16/q6_itp.py && python src/v16/qb_informe.py`.
- <a id="q6-v"></a>**q6-v.** Wald-DID = Σ_t Σ_{switchers}(Δlog compraventas_ut − media de estables) / Σ Δtipo; switchers = provincias de CCAA con cambio del tipo general en el año de efecto; estables = sin cambio en t ni t+1; CCAA 01, 06, 07, 08, 09, 10, 11, 12; 2012-2024 en diferencias.
- <a id="q6-p"></a>**q6-p.** Igual con log valor tasado provincial (38 provincias, sin Cantabria).
- <a id="q6-calendario"></a>**q6-calendario.** 14 cambios del tipo general (mínimo de la escala cuando hay escala) 2011-2024 en output/v16/f1/intervenciones.csv; fechas en su mayoría aproximadas al 1 de enero; año de efecto.
