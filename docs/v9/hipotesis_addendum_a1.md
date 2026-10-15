# Addendum A1 al pre-registro V9 (F2) — respuesta a la revisión docs/v9/revision_f2.md

Fecha: 2026-10-15. Escrito **antes de estimar ningún efecto** de D1-D7. Primera iteración de REHACER de la puerta F2 (máximo 2).

Complementa a docs/v9/hipotesis.md (commit 2977349, etiqueta `prereg-v9`) y prevalece sobre él donde difieran. Lleva la etiqueta local `prereg-v9-a1`. Cada cambio figura como desviación fechada en docs/v9/decisiones.md (E3).

Potencia recalculada en src/v9/f2b_potencia_addendum.py → output/v9/potencia/mde_addendum.csv. Tampoco aquí se usa la relación tratamiento-resultado de las unidades tratadas.

## A1.1 · Hipótesis confirmatorias (cambia el conjunto)

| Hipótesis | Antes | Ahora | Motivo |
|---|---|---|---|
| H1a-renta (zonas tensionadas Cataluña) | confirmatoria | **confirmatoria** | La simulación nula por bloques de residuos previos, con n_t = 199 y n_c = 20 reales, da un MDE con Holm (m = 3) de 0,041 ≤ 0,05 (LB01, VERIFICADA, Q1) |
| H1b-renta (Ley 11/2020) | confirmatoria | **confirmatoria** | MDE con Holm de 0,025 ≤ 0,05; 60 tratados y 181 controles. El factor iid se mantiene; con más controles que tratados es conservador |
| H1a-contratos | confirmatoria | exploratoria | La referencia 0,10 no tenía fuente (hallazgo 4) |
| H2-covid-renta, H2-reapertura-renta | confirmatorias | exploratorias | LA01 no se puede convertir a las unidades del MDE (1 DE de plazas HUT por 100 habitantes entre municipios; shock COVID): no hay referencia comparable (hallazgo 4). Con permutación dentro de provincia, el MDE es 0,010 |
| H4-réplica-alquiler | confirmatoria | exploratoria | Con el error AKM (nula impuesta y controles) y la referencia en unidades de forma reducida (0,01 × π̂ = 0,0040), el MDE con Holm es 0,0079 > 0,0040 (hallazgos 4 y 5) |

**Familia de Holm confirmatoria de V9:** {H1a-renta, H1b-renta}, m = 2.
- La potencia se calculó con m = 3, que es conservador.
- Regla de cierre: la m de una familia se fija aquí, con el máximo posible, y no se reduce a posteriori.

**Exploratorias:** todas las demás, en una sola familia de Benjamini-Hochberg (q = 0,10).

## A1.2 · D1a: pruebas e inferencia (hallazgo 2)

- **Prueba 4 (placebo de territorio), redefinida.** Es una prueba de aleatorización de Fisher: se permutan las etiquetas de cohorte (tamaños reales) sobre el conjunto tratados + nunca tratados, con 500 réplicas.
  - **Umbral:** p de permutación < 0,05 del ATT real.
  - Es además la inferencia exigida para C3, porque con 20 conglomerados de control el bootstrap salvaje tiene un tamaño poco fiable.
  - H1a-renta solo puede ser C3 si se cumplen a la vez p de Holm < 0,05 (bootstrap) **y** p de permutación < 0,05.
- **Pretendencias:** e ∈ [−8, −2], p > 0,10.
- **Placebo de fecha:** 4 trimestres antes, p > 0,10.
- **Honest DiD:** con M̄ = 1, el IC debe excluir el 0.
- **D1b:** pretendencias en e ∈ [−7, −2] (hallazgo 10). Las demás pruebas son las de D1a, incluida la permutación de etiquetas con umbral 0,05.

## A1.3 · D2 (hallazgo 7; ahora exploratorio)

- **Umbrales:**
  - permutación de la dosis dentro de provincia (500), p < 0,05;
  - pretendencias p > 0,10;
  - placebo de 2017 p > 0,10.
- **Sensibilidad.** Se añade una tendencia lineal específica por dosis (dosis × año) estimada con todo el periodo, y se informa si el signo y el IC se mantienen.
- **Mecanismo.** «Las HUT pasan al alquiler residencial» es una hipótesis de mecanismo **no contrastada** (hallazgo 11).

## A1.4 · D3 (hallazgo 6; sigue siendo descriptivo)

- **Año final del resultado: 2025**, el último año completo anterior al 2026-07-01.
- **Resultados:**
  - Δ 2024→2025 de la cuota del CP en las fianzas de su provincia (en lugar del Δ log del número);
  - Δ log de la fianza media.
- **Excepción declarada para la exposición.** ΔVUT entre el corte del 2025-01-26 y el del 2026-10-14. La exposición no es un resultado de precio ni de alquiler. Es la única medición disponible de la caída del registro, porque el corte intermedio no existe.
- **Columna `devuelta`.** Se cuentan todas las fianzas constituidas en el año (flujo según `anyo_datos`), estén devueltas o no.

## A1.5 · D4 (hallazgos 7, 9 y 13; ahora exploratorio)

- **Instrumento.** Usa **28** nacionalidades individuales, no 26. Cubren el 87 % de los extranjeros en 2003 y en 2012.
- **Valor tasado de las 7 CCAA uniprovinciales.** Se rellena con el panel anual de CCAA (otra fuente, marcada en `valor_tasado_origen`). Se añade la robustez sin esas 7 provincias.
- **Placebo con resultado anterior a 2003: inviable.** El panel provincial con código empieza en 2002. La única pretendencia es la de 2002→2003 de las cuotas con mayor peso de Rotemberg.
- **Umbral de las pretendencias:** p > 0,10 por país, con ajuste de Holm sobre los 5 países.
- **AKM.** Los shocks se expresan en puntos (Z ≈ cuotas × shocks; correlación de 0,997).

## A1.6 · D1c (hallazgo 8)

- 20 municipios: 11 con zona declarada, de los que **7** tienen al menos un trimestre posterior hasta 2025T4, y 9 sin zona.
- Exploratorio y sin potencia.

## A1.7 · F4: cotas sin promoción de capa (hallazgo 1)

Sustituye la sección «F4 · Cotas de contribución (C2)» de hipotesis.md.

- **Qué se acota.** Solo los efectos **C3/C3s** que hayan superado todas sus pruebas.
- **Cálculo** (C2): Manski con supuestos explícitos.
  - Supuestos:
    1. el efecto en los no observados está entre 0 y el extremo del IC 95 % del ATT del mismo signo;
    2. no hay efectos de desbordamiento.
  - Cota = [mín, máx] de (efecto × exposición), sobre la variación nacional y la de la Comunitat Valenciana.
- **Advertencia única: equilibrio parcial.** No incluye el desplazamiento entre territorios.
- **Si no hay ningún C3/C3s en un factor**, la tabla final dice «no identificado» para ese factor.
  - Los resultados C4 se pueden mostrar solo como «escenario ilustrativo C4, no atribución», sin las palabras «contribución» ni «atribuible».

## A1.8 · Formulación y referencias (hallazgos 11 y 12)

- **D5:** «¿Es mayor la variación de los precios asociada a los shocks del BCE en los países con más hipotecas a tipo variable?» (C4).
- **D4:** la pregunta en términos de cantidad se interpreta solo si se superan los diagnósticos C3. Como es exploratoria, se informa como asociación.
- **D7:** «componente población» y «componente tasa de jefatura» (descomposición contable).
- **Estado de las referencias:**
  - VERIFICADAS (Q1): LB01, LA01, LA07, LA08, LA09 y LA25;
  - VERIFICADAS, cuartil no aplica (informe institucional): LA18 (BdE);
  - NO VERIFICADA en el original (capítulo no leído): LA21 (OCDE);
  - sin DOI, documento no revisado por pares (cuartil no aplica): LB03 (Fedea);
  - NO VERIFICADA: la referencia de orden de magnitud de D5.
