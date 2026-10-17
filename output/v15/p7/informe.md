# E2 · Presión demográfica frente a obra nueva · informe
**Resultado (descriptivo, sin p ni IC).** Correlación entre el exceso de presión ((hogares nuevos − obra)/población inicial) y el Δlog del alquiler: Pearson entre 0.254 y 0.77 en 16 de 24 especificaciones; positivas en el 100 %. Caso de referencia (provincial, terminadas, hogares, SERPAVI, 2018-2024): r = 0.743. Es una asociación entre territorios dominada por el término de demanda; no es un efecto.

## Ficha reproducible {#pearson}
`python3 src/v15/p7_demografia.py`. Obra neta del Catastro con el desfase de un año (obra de t = Δ unidades en t+1); hogar medio 2,5 (DV15-B-8). 8 especificaciones municipales con MIVAU no disponibles. En el nivel provincial, hogares y población coinciden salvo escala.

## Limitaciones
N provincial ≈ 38 (correlación con ruido grande, sin IC); provincial: demanda hogares y población coinciden salvo escala (DV15-B-8); Catastro municipal solo de municipios de entrenamiento: la suma provincial es parcial; contaminación por regularización catastral 2011-2021 (por eso solo 2018+).

## Límites
C4 (entrenamiento), `pendiente_sellada`: true. Lenguaje de asociación. Multiplicidad (Holm en H, BH/BY en E) la aplica el orquestador con `p_valores_para_BY` de resultado.json. Desviaciones: docs/v15/desviaciones.md (DV15-B). Semilla 20261010.
