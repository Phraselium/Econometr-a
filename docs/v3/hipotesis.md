# Hipótesis v3 (pre-registro)

Redactado por el orquestador antes de estimar ningún diseño confirmatorio de la oleada 2. Se congela con el tag `prereg-v3`. Si el push del tag se rechaza, el ancla es el SHA del commit en la rama remota, anotado en docs/v3/decisiones.md. Toda desviación posterior se anota en decisiones.md con su motivo.

## Información ya conocida al pre-registrar (O1 de la revisión de la oleada 1)
- **P-C1, efectos fijos de sección y de año, muestra NO sellada.** Estimaciones conocidas por la réplica GL y la potencia: nacional +0,0011 por pp de VUT, IC95 [−0,0003; 0,0025]; Barcelona −0,0042; Sevilla −0,0027; València +0,0050; Madrid +0,0032; Málaga +0,0017. Por eso en P-C1 **solo la evaluación sellada es confirmatoria**: los distritos sellados y la última oleada. La estimación no sellada se informa como descriptiva.
- **P-C3.** Se conocen los coeficientes de los topes y de las zonas en fianzas municipales con todos los municipios: topes −0,022 / +0,002; zonas −0,047 / −0,203. La validación sellada de P-C3 es **por fuente**: alquiler SERPAVI municipal, que nunca se ha estimado para P-C3.
- Se hizo un `describe()` global del tratamiento VUT (todas las unidades) antes de fijar el sellado. Son estadísticos marginales, sin el resultado.

## Reglas comunes
- **Capas.** Un efecto llega a C3 solo si supera todo lo siguiente:
  - (a) pretendencias: event study con test conjunto p > 0,10 y Rambachan-Roth con M̄ = 1, cuyo IC robusto excluye 0;
  - (b) placebos de tratamiento (fechas o unidades falsas) y de resultado (una variable que no debería moverse), ninguno significativo al 5 %;
  - (c) sensibilidad: valor de robustez de Cinelli-Hazlett (RV_q=1) mayor que el R² parcial del mejor covariable observada; δ de Oster > 1;
  - (d) validación sellada con el mismo signo y su IC95 que excluye 0;
  - (e) Holm sobre la familia confirmatoria.

  Si falla alguno, queda en C4 y se dice cuál falló. «Robusto» exige además ≥2 diseños con supuestos distintos que coincidan en el signo (triangulación).
- **Multiverso:** curva de especificaciones sobre las decisiones razonables listadas en cada hipótesis. Se informa la mediana, la proporción con el mismo signo y la proporción significativa.
- **Inferencia:**
  - EE por clúster: distrito en P-C1; municipio en P-C3.
  - Wild cluster bootstrap (Webb, 999 réplicas) con G < 50.
  - Conley (1 km entre centroides de sección) como robustez si existe cartografía.
  - Inferencia por aleatorización: 999 permutaciones a nivel de clúster.
- **Magnitudes:** % de alquiler, €/mes (con el alquiler medio de la unidad) y viviendas.
- **Familia Holm v3 (m = 4):** H3-1, H3-2, H3-3a y H3-3b.

## Hipótesis confirmatorias
| Id | Diseño | Hipótesis | Signo | Especificación principal | Validación sellada |
|---|---|---|---|---|---|
| H3-1 | P-C1, efectos fijos | Más VUT por cada 100 viviendas en una sección se asocia a más alquiler | + | ln alquiler SERPAVI (€/m², vivienda colectiva) de la sección, 2021-2024, sobre VUT/viviendas×100 (oleada de agosto de cada año); efectos fijos de sección y de año × municipio; cluster por distrito; muestra nacional y 6 ciudades conjuntas | Misma especificación en los distritos sellados (2021-2024); se cumple si β_sellado > 0 y su IC95 excluye 0 |
| H3-2 | P-C1, shift-share leave-one-out (ciudades: Barcelona, Madrid, València, Sevilla, Málaga; Palma no estimable, P5) | Ídem, con la variación de VUT instrumentada | + | ΔVUT de la sección instrumentada con cuota inicial de VUT en 2021M08 × crecimiento de VUT del resto de la ciudad sin la propia sección (leave-one-out); diagnósticos GPSS (pesos de Rotemberg) y BHJ; F de primera etapa > 10 | Distritos sellados de las 6 ciudades |
| H3-3a | P-C3, topes de la Ley 11/2020 | La contención de rentas redujo la renta de los contratos nuevos en los 61 municipios sujetos | − | Panel municipal trimestral de fianzas Incasòl, 2017Q1-2023Q4; tratados = 61 municipios oficiales; controles = municipios catalanes no sujetos y no sellados; Callaway-Sant'Anna con un solo momento de tratamiento (2020Q4) más TWFE como contraste; ventana 2020Q4-2022Q1 | Por fuente: alquiler SERPAVI municipal 2018-2023 con el mismo diseño (anual) |
| H3-3b | P-C3, topes, cantidad | La contención redujo el número de contratos nuevos (desvío a otros usos o salida del mercado) | − | Ídem, con ln número de fianzas como resultado | Por fuente: nº de viviendas en alquiler SERPAVI (IRPF), con el mismo diseño |

## Precisiones de la revisión de la oleada 1, iteración 2 (P1-P6), fijadas antes de estimar
- **P1. Pretendencias de H3-1 y H3-2.** No hay periodo sin tratamiento porque las VUT por sección empiezan en 2021. El criterio de pretendencias es un **test de adelanto**: Δ ln alquiler SERPAVI 2016-2020 de la sección sobre ΔVUT 2021-2024 (y sobre el nivel de VUT de 2021M08), con efectos fijos de municipio y cluster por distrito. Se exige p > 0,10 y que el coeficiente sea menor que la mitad del efecto principal, en valor absoluto. Rambachan-Roth solo se aplica a H3-3 (event study con periodo previo). Si el test de adelanto falla, la capa máxima de H3-1 y H3-2 es C4.
- **P2. Potencia de lo registrado.** Antes de estimar, cada diseño recalcula el EMD de la especificación exactamente registrada y de su validación sellada:
  - H3-1: efectos fijos año × municipio;
  - H3-3: Callaway-Sant'Anna trimestral;
  - validaciones selladas: los distritos sellados en P-C1 y SERPAVI municipal en P-C3.

  Si el EMD de la especificación principal es mayor que el EER, la hipótesis no se estima y se informa como «no detectable». Si lo que no tiene potencia es la validación sellada, su fallo se informa como «no concluyente», y el resultado no puede pasar a C3.
- **P3. Placebos con nombre.**
  - H3-1 y H3-2:
    - placebo de tratamiento: VUT de otra sección del mismo municipio asignada al azar (999 permutaciones a nivel de sección dentro del municipio);
    - placebo de resultado: renta media por hogar del ADRH (2021-2023). Limitación: puede responder a la gentrificación, así que un resultado significativo se informa sin invalidar automáticamente.
  - H3-3:
    - placebo de tratamiento: fecha falsa 2018Q4 en los mismos tratados;
    - placebo de unidad: municipios no sujetos de 10.000 a 20.000 habitantes con tratamiento ficticio;
    - placebo de resultado: no hay un resultado de vivienda no afectado en las fianzas; se declara.
- **P4. Holm.** La familia (m = 4) se aplica a los p de las evaluaciones confirmatorias: selladas en H3-1 y H3-2, y la validación por fuente en H3-3a y H3-3b. El multiverso no entra en Holm.
- **P5. Palma.** No es estimable en la muestra no sellada: H3-2 se estima con las 5 ciudades restantes y Palma solo entra si aparece en la parte sellada (se informa aparte).
- **P6. H3-3b.** La validación por fuente mide un stock (viviendas en alquiler declaradas en el IRPF), no el flujo de contratos nuevos. Su signo esperado es el mismo, pero atenuado. Se declara.

## Decisiones del multiverso
- **H3-1:** resultado (mediana, o media si existe); tipo de vivienda (colectiva o unifamiliar); efectos fijos de año (año o año × municipio); tratamiento (nivel, Δ o log(1+VUT)); muestra (todas las secciones o las de ≥100 viviendas); peso (ninguno o viviendas).
- **H3-2:** periodo base de la cuota (2021M02 o 2021M08); agregado leave-one-out (ciudad o provincia).
- **H3-3:** grupo de control (todos los no sujetos, o los no sujetos con más de 20.000 habitantes como en Jofre-Monseny et al. 2023); fin de la ventana (2022Q1 o 2021Q3); estimador (CS, dCDH o TWFE); excluir o no Barcelona.

## Exploratorio (C4)
- **Zonas tensionadas de Cataluña 2024**, alquiler y cantidad: sus coeficientes ya se vieron (O1).
- **Caída de anuncios 2025-2026**, descriptiva: no hay resultado de alquiler con potencia (decisión de la puerta).
- **Desvío a temporada**, solo si hay datos.
- **P-E**, solo si sobra presupuesto.
