# V18 · B6 · Abogado del diablo, ronda 1: E2-R1, E2-R1c y E8-R1 (2026-10-20)

Solo lectura sobre output/v18/estimacion/{e2,e8}/, el plan y la adenda. Veredicto: **E2-R1 resiste con limitaciones (SUGESTIVO se sostiene); E2-R1c y E8-R1 no resisten como SUGESTIVO.**

## E2-R1 (renta, −0,038)
1. **Alta. Efecto que se apaga dentro de la vigencia.** −0,058 (2021T1) → −0,015 (2022T1, no significativo) antes de la STC; la «reversión» (−0,0016) continúa esa caída; el pico coincide con la tercera ola y la vuelta de pisos turísticos al alquiler. Prueba: tendencia del efecto en 2021T1-2022T1 y salto en 2022T2 sobre su extrapolación.
2. **Alta. Control de COVID y turismo rígido** (HUT 2019 × un solo «post»; sin ERTE). Prueba: HUT 2019 × efectos de trimestre y ln(población) × trimestre; el efecto debería seguir por debajo de −0,03.
3. **Alta. Sensibilidad a tendencias.** Con M̄ = 0,5 el IC de Honest DiD incluye el cero; el plan (línea 122) hace de un M̄ de ruptura < 0,5 un fallo decisivo; la desviación C2 lo declaró «no evaluable» por el veredicto del Monte Carlo (con M̄ > 0, tamaño 0 y potencia ≈ 0). Prueba: Honest DiD con restricción de suavidad en la serie anual y Monte Carlo de Honest con M̄ = 0,5 informativo.
4. **Media. Reversión a la media.** Placebo de 2017: +0,0146 (p = 0,056), 38 % del efecto y de signo contrario; potencia de Roth insuficiente (sesgo indetectable 0,061). Prueba: controles emparejados por crecimiento 2017-2019 y tendencia propia de los regulados.
5. **Media. Dependencia del control y de la medida:** −0,026 (vecino más cercano) a −0,056 (más de 10 km); con SERPAVI −0,005 (p = 0,36). Prueba: control sintético o SDID.
6. **Media. Desvío a temporada sin potencia** (MDE de R1c 8,1 % frente a la regla del 5 %; R1c-v1 sin registrar en sellado_v18.json). Prueba: hogares en alquiler del Censo 2021 en f3_sellado.py y estimar R1c-v1.
7. **Baja.** La razón 0,85 con JMS compara el mismo registro y episodio: no es validación externa.
8. **Baja.** El MDE usa el σ del panel entero, no solo del periodo previo (declarado); no cambia la estimabilidad.

## E2-R1c (contratos, +0,017, no significativo)
9. **Alta.** Placebo de fecha −0,079 (p = 0,0005) y diferencia persistente tras la STC (+0,074, p = 0,002): activa el tope de la adenda (línea 581), no recogido entre las razones; signo en el 67 % de las variantes.
10. **Media.** La regla literal deja «SUGESTIVO sin I7»; pide al árbitro que esa clase no exista.

## E8-R1 (ITP, +0,0146 por punto)
11. **Alta.** Fechas sin contraste con el BOE (10 de 16 el 1 de enero aproximado); con todas en el 1 de enero 0,0011 (p = 0,92); ±3 meses 0,0088 / 0,0131.
12. **Alta.** El cambio de signo sin 2012-2013 es una prueba B4 del plan (línea 737) y un cambio de signo en B4 es fallo decisivo (línea 124): ASOCIACIÓN; la adenda R-18 pone un techo, no anula la regla.
13. **Alta.** Confusores de 2012-2013 (fin de la deducción, IVA de obra nueva, cajas). Prueba: excluir 2012T3-2013T2 y controlar obra nueva × trimestre.
14. **Media.** Composición del valor tasado; con el IPV, 0,0073 (p = 0,38).
15. **Media.** Dejar fuera una comunidad cada vez; pesos iguales por comunidad.
16. **Baja.** MDE 0,0244 frente a 0,03 con un σ optimista.

## Clasificación propuesta
| Estimación | Propuesta | Condición |
|---|---|---|
| E2-R1 | SUGESTIVO | ASOCIACIÓN si se aplica el M̄ de ruptura < 0,5 o fallan las pruebas 1-2 |
| E2-R1c | ASOCIACIÓN | diseño no creíble para este resultado |
| E8-R1 | ASOCIACIÓN | cambio de signo en B4 y fechas no verificadas |
