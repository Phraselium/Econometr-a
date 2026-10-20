# V18 · E5 Oferta y suelo: elasticidad de la oferta con un Bartik de empleo

*análisis V18; capa C4; pre-registro interno plan-replicacion-v18.* Generado por `python3 src/v18/estimacion/e5_oferta.py` (SEED 20261010, sin red; B = 9999). Clasificaciones provisionales: pendientes de I8. Toda cifra es C4 (EXPLORATORIO). Sin lenguaje causal.

## 1. Resumen
- **E5-R1: NO ESTIMABLE.** La comprobación previa de variación (adenda 1.3) da un MDE al 80 % superior a 230.8 (seis errores típicos de referencia) frente a la referencia única de 0.87 (Taltavull, NO VERIFICADA); el F efectivo de la primera etapa es 0.03195 y el número efectivo de choques es 3.326 (4 ramas). **No se publica ningún coeficiente de E5-R1** ni de sus variantes (auge, caída, terminadas, pesos, exclusiones).
- F efectivo por ventana (solo primera etapa, sin usar el resultado): 2002-2007: 6.58, 2008-2013: 0.001793, 2014-2023: 0.1817, 2002-2023: 0.03195.
- **E5-A1** (ASOCIACIÓN como máximo; fuera de Holm): ψ = 0.002439 (EE 0.003886); IC95 Webb [-0.007625; 0.0105]; p Webb 0.5557; N = 324.
- **E5-R2, E5-A2, E5-A3 y la coprincipal P-Q4a: NO ESTIMABLES por datos.**
- B5: E5-R1 es la estimación propia de E5 y no tiene respaldo; E5 no aporta magnitud propia (entra solo la literatura).

## 2. Diseño y traslado
- **Original.** Saiz (2010, QJE): elasticidades de oferta por área metropolitana con restricciones geográficas (solo resumen en la ficha). Baum-Snow y Han (2024): choques de demanda laboral (Bartik). Taltavull (2006): CCAA 1990-2004, elasticidad de los inicios de 0,46 a 0,87.
- **Aquí.** Δ ln iniciadas libres = ε·Δ ln valor tasado real + efectos de provincia y año, con el Bartik B = Σ_k s_pk(2001)·g_kt(sin la provincia) de cuatro ramas (A, B-E, G-J, O-U) de Eurostat/INE, sin construcción, finanzas, inmobiliarias ni servicios profesionales. 39 provincias de entrenamiento, 2002-2023, sin pesos. Inferencia: Webb-AR y AR exacto por provincia (D-E359-7).
- **Desviaciones:** la afiliación provincial por CNAE de 2001 no está publicada; Eurostat solo da seis ramas a escala NUTS 3 (D-E359-2, D-E5-1). Con cuatro ramas se excluye 1 sector en Rotemberg (D-E5-2).

## 3. Comprobación previa de variación (adenda 1.3)

| id | n | G | F efectivo | σ preperiodo | ρ | MDE80 | referencia | estimable | 1/HHI |
|---|---|---|---|---|---|---|---|---|---|
| E5-R1 | 848 | 39 | 0.03195 | 0.3224 | -0.4864 | no acotado | 0.87 | NO | 3.326 |
| E5-A1 | 324 | 36 | — | 0.02833 | -0.2619 | 0.01339 | 0.1 | sí | — |

MDE por Monte Carlo (R = 2000, SEED 20261010) con el contraste de Anderson-Rubin agrupado por provincia y la variación real de x y z; σ y ρ del preperiodo 1996-2001 (E5-R1) o 2009-2013 (E5-A1) tras los efectos de provincia y año; «no vistas» en V15/V16 para esta unidad. Se calculó antes de estimar.

## 4. NO ESTIMABLES

- **E5-R1**: NO ESTIMABLE por variación: MDE superior a seis errores típicos de referencia (no se alcanza el 80 % de potencia) frente a |referencia| 0.87.
- **E5-R1-v4**: los diez sectores A*10: a escala NUTS 3 Eurostat solo da seis ramas.
- **E5-R1-v10**: exposición a cajas de 2007 × año: no está en el repositorio.
- **E5-R2**: restricciones físicas (MDT05, agua, costa) y de planeamiento (SIU) no están en el repositorio.
- **E5-A2**: Atlas de áreas urbanas del MIVAU (`posterior_prereg`) no descargado; la unidad exige el valor tasado y la obra nueva por área.
- **E5-A3**: afiliación municipal por sección de la CNAE anterior a 2011-12 no agregada en el repositorio (solo tres ramas); el Bartik municipal no se puede construir.
- **E5-P-Q4a**: la Red Natura municipal de V16 solo existe como panel de entrenamiento de V16 (data/processed/v16) y su variable no figura en docs/v18/sellado_v18.json: no se puede leer con sellado.filtrar.
- **E5-R1-v1**: su principal E5-R1 es NO ESTIMABLE.
- **E5-R1-v2**: su principal E5-R1 es NO ESTIMABLE.
- **E5-R1-v3**: su principal E5-R1 es NO ESTIMABLE.
- **E5-R1-v5**: su principal E5-R1 es NO ESTIMABLE.
- **E5-R1-v6**: su principal E5-R1 es NO ESTIMABLE.
- **E5-R1-v7**: su principal E5-R1 es NO ESTIMABLE.
- **E5-R1-v8**: su principal E5-R1 es NO ESTIMABLE.
- **E5-R1-v9**: su principal E5-R1 es NO ESTIMABLE.
- **E5-R1-v11**: su principal E5-R1 es NO ESTIMABLE.

Qué datos las harían estimables: (i) afiliación a la Seguridad Social por provincia y sección o división de la CNAE-93 de 2001 (o la primera disponible) y su serie de los años siguientes, para un Bartik con más ramas que las cuatro de Eurostat y con variación suficiente entre provincias (el F efectivo del Bartik de cuatro ramas es ≈ 0); (ii) restricciones físicas (pendiente del MDT05, agua, costa) y de planeamiento (SIU) por provincia o área urbana para E5-R2; (iii) el Atlas de áreas urbanas del MIVAU con valor tasado y obra nueva por área para E5-A2; (iv) afiliación municipal por sección de la CNAE de 2011-12 en adelante (ficheros STAT/MUNCNAE de la Seguridad Social) para E5-A3; (v) la Red Natura municipal bajo el sellado de V18 para la coprincipal Q4a; (vi) las 11 provincias selladas, que no se leen.

## 5. Lectura y limitaciones

- Con un Bartik de cuatro ramas y efectos de provincia y año, la variación del instrumento entre provincias es la de la composición sectorial de 2001 frente a los crecimientos sectoriales nacionales; no predice el precio real (F efectivo ≈ 0). La respuesta de la oferta no se identifica con estos datos; no se debe leer ninguna elasticidad de este módulo.
- La referencia de Taltavull (CCAA, 1990-2004) y la cota de 0,45 del Banco de España siguen siendo la única información sobre la elasticidad de la oferta española en V18.
- I8 (réplica ciega) y la ronda del abogado del diablo (B6) están pendientes.

