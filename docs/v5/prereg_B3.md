# Pre-registro v5 · B3 Diferencias entre provincias (etiqueta `prereg-v5`)

Fecha: 2026-10-10. Lo escribe el orquestador ANTES de que se estime nada de B3. Cualquier desviación se declara en decisiones.md como exploratoria.

## Unidades y periodos
- Las 50 provincias, más Ceuta y Melilla si hay datos; si faltan, se excluyen y se declara.
- Variables dependientes (Δlog):
  - Y1: precio de compra (valor tasado del Ministerio; robustez con Registradores provincial);
  - Y2: alquiler (SERPAVI provincial; robustez con IPVA provincial si existe);
  - Y3: esfuerzo (precio/renta).
- Periodos: P1 = 2015-2025 y P2 = 2021-2025. El principal es P1.

## Familias de regresores (valores iniciales de 2015 o variaciones en el periodo)
- F1 empleo tipo Bartik: pesos sectoriales de 2015 por provincia × crecimiento nacional del sector.
- F2 llegada de población: Δ población por migración, total y extranjera.
- F3 intensidad turística: VUT por 1.000 viviendas, INE 2021 (no hay dato anterior: es valor inicial C4).
- F4 suelo y rigidez: clase y brecha de A4, y respuesta de las terminadas.
- F5 renta: renta por hogar inicial (ADRH) y su crecimiento.
- F6 convergencia: log del precio inicial de 2015.
- F7 crédito hipotecario: nuevas operaciones por hogar (si hay dato provincial; si no, por CCAA, y se declara).
- F8 costa e islas: indicador.

## Hipótesis confirmatorias (dos colas, α = 0,05, Holm sobre las 8 familias × Y1 en P1)
- H-B3-1: F1 (Bartik) se asocia positivamente con Y1.
- H-B3-2: F2 (población) se asocia positivamente con Y1.
- H-B3-6: F6 (convergencia): coeficiente negativo.
- El resto de combinaciones de familia, variable dependiente y periodo son EXPLORATORIAS (BH).

## Especificación principal
- MCO con todas las familias a la vez y regresores estandarizados.
- Errores robustos HC3 y errores de Conley con corte de 100 km y de 200 km. Se informa del mayor.
- Inferencia por aleatorización (5.000 permutaciones, SEED=20261010) como contraste con N≈50.

## Descomposición
- Shapley de R² por familia. Capa C4 (exploratoria) salvo que dos fuentes de Y1 den el mismo orden de familias: entonces el ORDEN es C1 y las magnitudes siguen en C4.

## Potencia previa
- Con N=50, 8 familias y α Holm, se calcula el efecto mínimo detectable (en desviaciones típicas) antes de estimar y se declara.
- Si el efecto mínimo detectable supera 0,5 DT, B3 se presenta como «descriptivo honesto».

## Multiverso
- Periodos, fuente de Y, Bartik con pesos de 2011 o 2015, con o sin Madrid, Barcelona, Baleares y Canarias, y errores HC3 o Conley.
- Se informa del porcentaje de especificaciones con el mismo signo.

## Sensibilidad
- Oster (δ con Rmax = 1,3·R²) y Cinelli-Hazlett (RV, RV_α) para H-B3-1 y H-B3-2.

## Lenguaje
Asociación, nunca efecto. Capa máxima: C4 o «asociación robusta», sin pasar a C3.
