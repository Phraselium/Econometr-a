# Desviaciones del pre-registro V7 (prereg-v7)

## R4a (2026-10-12)
1. **Dummies de quiebre.** Las herramientas validadas de panel_tools no admiten regresores exogenos. Los quiebres (COVID 2020T2-T4; escalon EPA 2021T1 en ocupados y paro) se aplican como pulsos en las DIFERENCIAS de cada serie y region, reacumuladas antes de estimar (no como dummies dentro del ECM). Motivo: usar solo funciones validadas. La poblacion no se ajusta. Efecto: se descarta la informacion de esos trimestres.
2. **Controles de corto plazo** (Δ ln hipotecas en alquiler; Δ ln compraventas en compra): solo en el ECM propio de cada region (diagnosticos y F-H), no en MG/PMG/CS-DL/DFE comunes. zt_declarada y tope_rentas_ccaa (F-R) quedan para otro encargo.
3. **Muestra spec A.** La poblacion total no existe desde 2025T2 (NaN), por lo que la spec A usa 2007T1-2025T1 (T=73); la spec B, 2007T1-2026T2 (T=78). Cada spec usa su muestra comun.
4. **Cotas de ARDL bounds.** Valores criticos del F de PSS simulados (caso III, 5 %, 500 reps) para (k, T), no tabulados de PSS 2001 (no verificados).
5. **Familia F-E.** Holm sobre los 4 p del tipo Westerlund y 2 de Pedroni (spec A) por mercado; E1 se declararia con Holm < 0,05 en alguno. E2 se resuelve por el valor critico -8,83 (sin p).
6. **Holm** de F-A y F-C: sobre p unilaterales de H1 de cada estimador por separado (3 y 4 hipotesis), con t de Student (N-1) para MG_dm y CS-DL, y EE bootstrap con t(N-1) para PMG_dm.
7. **PMG_dm bootstrap** B=199 con EE inflados por replicas extremas; solo se usa su signo en la triangulacion.

## R4b (anotadas por el orquestador a partir del informe del subagente)
- **F-L.** El shock es el residuo AR(2) estandarizado de la variación del tipo hipotecario nacional y del crédito nuevo; el pre-registro solo decía «shock del tipo». Hay riesgo de que el signo dependa de esa construcción, y se declara.
- **F-H (jerárquico).**
  - Priors informativos y variables X estandarizadas; demeaning transversal y por CCAA.
  - Muestra común 2007T3-2025T1, porque ln_pob_total no tiene datos al final.
  - Los modelos de alquiler A y compra A no convergen (R-hat ≈ 1,5) y no se interpretan.
- **F-P.** No es viable el CCE con flujos de ETDP e iniciadas: 13 años por provincia para 12 parámetros.
