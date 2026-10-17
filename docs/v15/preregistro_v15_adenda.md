# V15 · Adenda al pre-registro (respuesta al revisor; vinculante)

Fecha: 2026-10-17, antes del depósito y antes de cualquier estimación. Esta adenda **prevalece sobre docs/v15/preregistro_v15.md** donde difieran. Responde, punto por punto, a la revisión independiente (revisor-preregistro, veredicto «APTO CON CAMBIOS»; 18 hallazgos). Cada punto se incorpora (I) o se rebate (R), con motivo.

## Recuento previo de tratados y donantes (P6; no es un resultado)
Recuento con data/processed/v15/p6_zonas_tensionadas.parquet (entrenamiento, tras el sellado), sin mirar la renta.
- **Adopción en Cataluña:**
  - 2024T1: 128 municipios (primera cohorte);
  - 2024T4: 113 (segunda cohorte);
  - no hay cohortes de 2025 en el entrenamiento.
- **Preperiodo limpio** 2022T2-2023T4. Filtro: 7 trimestres con dato, media ≥ 5 contratos y ningún trimestre sin contratos. Quedan:
  - 234 tratados;
  - 74 nunca tratados;
  - 13 nunca tratados a 10 km o más de un tratado, y 1 a 25 km o más.
- **Umbral de 10 contratos:** 199 tratados, 23 nunca tratados y 4 a 10 km o más.
- **Umbral de 30 contratos:** 119 tratados y 7 nunca tratados.

## Respuestas

1. **(I) Contaminación del preperiodo por la Ley 11/2020 y su anulación.**
   - El preperiodo principal de H1 y H2 pasa a **2022T2-2023T4**: después de la anulación por la STC 37/2022 (8-4-2022) y después del cambio de tramos de Incasòl de 2021.
   - 2019T1-2020T2 solo como robustez.
   - El placebo temporal pasa a **2023T2**, una fecha sin intervención en el preperiodo limpio.
   - Se añade una prueba de ruptura en 2022T2 sobre el preperiodo largo (descriptiva).
   - Se declara que V9-D1a usó un preperiodo con los topes: su rechazo de pretendencias puede venir de ahí.
2. **(I) Donantes.** Recuento arriba. La definición de tratamiento queda fijada en **dos cohortes: 2024T1 y 2024T4**.
   - **Diseño principal (doble, ambos necesarios):**
     - (a) Callaway-Sant'Anna con la cohorte 2024T4 como control **aún no tratado** de la cohorte 2024T1 durante 2024T1-2024T3;
     - (b) SDID por cohortes con los 74 nunca tratados como donantes.
   - **Exclusión por distancia:** queda como robustez (13 donantes) y como diagnóstico de desbordamiento.
   - **Solapamiento:** se diagnostica con la renta media del preperiodo. Con menos de 30 donantes dentro del soporte común de los tratados, **H1 y H2 no pueden alcanzar C3** y se reportan como C4.
   - **Potencia:** se recalcula al inicio de la fase 4, antes de estimar, con asignación aleatoria de 234 de 308 unidades y SDID con pesos (agente montecarlo). Si el MDE80 supera el 5 % en renta o el 13 % en contratos, la hipótesis pasa a exploratoria.
3. **(I) Evaluación sellada como condición de C3.**
   - **Condición.** C3 exige además superar la **evaluación sellada temporal**. El estadístico es el ATT de los trimestres u años nuevos, con la especificación congelada al final de la fase 4. La regla: mismo signo que en entrenamiento e IC95 que excluye 0. Para un nulo, IC95 dentro del margen TOST (punto 12).
   - **Plazo.** Si a 31-12-2027 no se alcanza el mínimo, el resultado es «**no evaluable, no C3**».
   - **Bloque espacial.** Pasa a **informativo** para H1-H3: comparte periodos ya vistos en V3, V6 y V9. Solo se reporta.
   - **Claves de evaluate_v15**, una apertura cada una: `H1-temporal`, `H2-temporal`, `H4-temporal`, `H5-temporal`, `H1-espacial`, `H2-espacial`, `H3-espacial` y `H4-espacial`.
4. **(I) Calendario de H4.**
   - **Panel de evaluación temporal:** diferencia larga 2022→2025.
   - **Resultado:** SERPAVI 2025 (sellado) frente a 2022.
   - **Exposición:** crecimiento de la población extranjera 2022→2025 del censo anual por nacionalidad, con las 22 categorías comunes al padrón y al censo anual. El mapeo se versiona antes de estimar en docs/v15/mapeo_nacionalidades.csv.
   - **Instrumento:** cuotas de 2003 agrupadas en esas 22 categorías y choques nacionales 2022→2025, sin el propio municipio.
   - Si el censo anual de 2026 o SERPAVI 2025 no se publican antes del 31-12-2027: «no evaluable, no C3».
5. **(I) Familias.**
   - **Familia causal confirmatoria:** {H1, H2, H4}, Holm con m = 3.
   - **Qué p entra:**
     - H1 y H2: el mayor de los p de CS (wild cluster bootstrap de Webb por municipio) y de SDID (placebo);
     - H4: el p de Anderson-Rubin si el F efectivo no supera el umbral MOP, y el de AKM en otro caso.
   - **H3** pasa a «asociación pre-registrada»: familia propia, α = 0,05, sin corrección adicional, capa máxima C4.
   - **H5** es un contraste predictivo aparte, con la regla K1 (punto 16). No entra en Holm con las causales.
6. **(I) SDID y resultados mixtos.**
   - Los pesos de SDID se ajustan en 2022T2-2023T2; 2023T3-2023T4 quedan reservados como **preperiodo de contraste** (sin efecto esperado).
   - CS se contrasta en todo el preperiodo limpio.
   - Para C3 deben pasar **los dos**. Si uno pasa y el otro no: C4 «resultado mixto».
   - **Se declara** que el diseño de V15 se eligió conociendo el fallo de pretendencias de V9-D1a; por eso el estándar es más exigente que el de V9.
7. **(I) Holgura del multiverso.**
   - Se limita al **20 %** de lo declarado: 68 especificaciones. El total máximo baja de 4.104 a **408**.
   - Ninguna desviación puede ser la especificación principal ni sostener C3.
   - Cada desviación va a metodologia/desviaciones_v15.md **antes** de ver su resultado y entra en BH dentro de su familia.
8. **(I) Grados de libertad cerrados.**
   - **H1 y H2:**
     - umbral de contratos: media ≥ 5 en el preperiodo limpio, ningún trimestre con 0, y 7 de 7 trimestres con dato;
     - la muestra de H2 es la misma que la de H1;
     - en H2, principal PPML sobre el recuento, con efectos de municipio y trimestre; log(1+n) solo como robustez (Chen-Roth).
   - **H3:**
     - solo secciones con el mismo código en 2021-2024 (sin cambios de seccionado);
     - SERPAVI tal como se publica (supresión del INE/MIVAU);
     - «salto de factor > 10»: |Δlog| > ln 10 entre ediciones consecutivas del INE.
   - **H4:**
     - ecuación en diferencias anuales: Δlog alquiler(t) frente a ΔPobExt(t)/Pob(t−1);
     - instrumento: Σk s(i,k,2003) · g(k,t), donde g es el crecimiento nacional de la nacionalidad k sin el municipio i;
     - efectos de provincia × año;
     - se reportan los pesos de Rotemberg y el número efectivo de choques (1/HHI);
     - el contraste de desbordamiento (vi) entra en «C3 si».
   - **H5** (ventana expansiva común desde 2003T1 para todos los modelos y para la línea base):
     - BVAR con 6 variables: Δlog valor tasado, Δlog compraventas, Δlog hipotecas (número), tipo hipotecario, Δlog ocupados e inflación del IPC. Hiperparámetro de Minnesota por verosimilitud marginal (Giannone-Lenza-Primiceri) solo con datos de entrenamiento;
     - DFM con 2 factores y los mensuales agregados al trimestre;
     - LASSO con λ por validación temporal con embargo de 4 trimestres;
     - ARDL con rezagos elegidos por BIC, como máximo 4.
   - **Exclusiones por código INE:**
     - municipio 08019 (Barcelona) y municipio 46250 (València);
     - provincias 28, 07, 35 y 38, que ya están fuera porque se sellaron en v6;
     - para H1 y H2, además, la provincia 08 sin la capital como segunda robustez;
     - la regla del 1 % superior de exposición solo para exposiciones continuas (H3, H4 y E4).
9. **(I, en parte) Potencias.**
   - **Recálculo en la fase 4, antes de estimar.** Se rehacen con exposiciones reales permutadas por bloques: entre secciones del mismo municipio en H3; las cuotas de 2003 reales con choques permutados entre orígenes en H4. Si el MDE80 supera el umbral de cada hipótesis (H3: 1 % por desviación típica intra-sección; H4: 1 % por punto), pasa a exploratoria.
   - **H4.** Su rechazo placebo es 0,116 con las provincias de entrenamiento, así que la inferencia principal es AKM (ya lo era).
   - **H3.** Se traduce la literatura a desviaciones típicas intra-sección antes de estimar y se declara la cifra.
   - **(R parcial)** No se recalcula ahora: hacerlo bien exige construir el instrumento de H4, que es trabajo de la fase 4. La regla de paso a exploratoria lo cubre sin mirar resultados.
10. **(I) Identificación de H4.**
    - **Instrumento principal** sin orígenes residenciales: UE-14, Reino Unido, Suiza y Noruega. El instrumento con todos los orígenes queda como robustez.
    - **Controles** de provincia costera × año (provincias con costa, lista fijada por código INE en docs/v15/provincias_costeras.csv antes de estimar) y de cuota de vivienda secundaria del Censo 2021 × año.
    - **Primera etapa:** umbral MOP con τ = 10 % (valor crítico del procedimiento, no F ≥ 10). Intervalos AR siempre.
    - **Pretendencias:** SERPAVI 2011-2013 frente a choques 2014-2022.
11. **(I) Estimando y selección en H1.**
    - El estimando es el **paquete** de la declaración (zona tensionada con sus medidas asociadas), no el tope aislado.
    - Se añaden **cotas de Lee** para H1, condicionadas a la variación de contratos de H2.
    - **Omisión explicada:** el desplazamiento a temporada no tiene dato municipal. El desplazamiento a compra solo tiene compraventas provinciales, inútiles con 4 provincias. Ambos quedan fuera de V15.
12. **(I) Nulos.**
    - Se separa la validez del diseño (las pruebas) de la significación.
    - Un diseño válido con equivalencia TOST da «**nulo C3 acotado**». Márgenes:
      - H1: ±5 %;
      - H2: ±10 %;
      - H4: ±0,5 % de alquiler por punto de población extranjera.
    - Rige para los resultados de entrenamiento y para la evaluación sellada.
13. **(I) Herramientas de las que depende C3** (SDID, CS con bootstrap de Webb, Honest DiD, AKM y AR):
    - tamaño empírico en [0,04; 0,06] con 2.000 réplicas o más;
    - doble implementación (tests/doble_impl).
    - **Honest DiD:** la implementación propia de V9 (tamaño 7,3 %) no se usa sin revalidación. Si no hay una segunda implementación independiente, el criterio M̄ no puede sostener C3.
14. **(I, en parte) Selección.**
    - **H3** pasa a asociación pre-registrada (punto 5), sin papel confirmatorio.
    - **E4:** se declara su historial. V9 estimó una dosis-respuesta en Cataluña con pretendencias rechazadas.
    - **(R) P1** sigue descartada en V15: no hay restricciones físicas en el repositorio y conseguirlas es trabajo de datos (MDT, SIOSE, Natura 2000). Se anota como tarea del autor para una versión posterior, sin intentarlo aquí.
15. **(I) Fugas.**
    - **Protocolo de ingreso.** Todo dato posterior al corte entra solo por `src/v15/f3_sellado.py` y holdout.sellar_v15. Los módulos de la fase 4 leen solo data/processed/v15; check_v15 lo comprueba.
    - **(R) Choques de H4.** Ya están libres de unidades selladas: el padrón entró por sellar_v15 y el fichero de entrenamiento excluye los municipios sellados. Se declara que los choques nacionales sin el propio municipio se calculan sobre el entrenamiento.
    - **Redacción corregida:** las filas sub-provinciales de las provincias de v6 están en la base, pero fuera del entrenamiento (G6).
    - **Filas selladas en la base pública.** Siguen en data/base y en la base pública (1.0), que ya existían. La protección efectiva es el fichero de entrenamiento más check_v15. Se declara como limitación.
16. **(I) Línea base de H5.** La de K1: la de menor ECM en entrenamiento entre el AR(4), el ECM v1 y el paseo aleatorio con deriva, en la misma muestra. Además, la combinación debe estar en el MCS al 10 %.
17. **(I) Neutralidad.**
    - Se eliminan «sería la primera cifra causal de regulación del repositorio» y «confirma lo que ya sabíamos».
    - En H3, la comprobación de la medida se aplica a cualquier resultado, no solo a un nulo.
18. **(I) Detalles.**
    - **E3:** periodos 2011-2019 y 2015-2024.
    - **E2:** 24 especificaciones = 2 niveles (provincia, municipio) × 3 medidas de oferta (obra neta del Catastro, terminadas MIVAU, iniciadas MIVAU) × 2 medidas de demanda (hogares, población) × 2 resultados (SERPAVI, IPC de alquiler).
    - **BH** se aplica por familia.
    - **Regla del 1 % superior** de exposición: solo exposiciones continuas.

## Recuento del multiverso tras la adenda
H1 36 · H2 36 · H3 48 · H4 64 · H5 60 · E1 36 · E2 24 · E3 12 · E4 24 = 340 declaradas, más una holgura máxima de 68. **Total: 408.**

## Capas máximas tras la adenda

| Id | Capa máxima | Condiciones adicionales |
|---|---|---|
| H1, H2 | C3 | CS y SDID pasan; ≥ 30 donantes en soporte común; Honest DiD con implementación doble; evaluación sellada temporal superada |
| H4 | C3 | Umbral MOP o AR; AKM; pretendencias 2011-2013; desbordamientos; evaluación sellada temporal 2022→2025 |
| H3 | C4 | Asociación pre-registrada |
| H5 | — | Predictiva (K1 y MCS) |
| E1-E4 | C4 | Exploratorias, BH por familia |
