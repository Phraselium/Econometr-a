# Estado V9 COMPLETO (para retomar con `claude --continue`)

Rama local `r9/main` → remota `claude/housing-price-spain-econometric-95dhj3`.

## Hecho
- **F0:** correcciones de la web (E0).
- **F1:** datos completos (bloques 1-9; decisiones_datos.md D8).
  - 10 scripts nuevos en src/v9;
  - auditoria_exhaustividad.md, fuentes_fallidas.md, solicitudes_transparencia.md, tareas_autor.md y cobertura.md (estado por diseño);
  - `make datos_v9` verifica 123 ficheros;
  - `make base`: 10,67 millones de filas, 13 variables nuevas.

- **F2:** pre-registro en docs/v9/hipotesis.md, con potencia en output/v9/potencia (src/v9/f2_potencia.py). Commit con etiqueta local `prereg-v9`.

- **Revisor F2:** REHACER (1 de 2), respondido con hipotesis_addendum_a1.md (etiqueta `prereg-v9-a1`).
- **Herramientas** (src/v9/herramientas.py): validadas por Monte Carlo (tests/v9/test_herramientas.py, 8 pruebas).
- **Scripts de D1, D2 y D4:** escritos y sin ejecutar.

## Siguiente paso exacto
- Revisión breve del addendum.
- Ejecutar src/v9/d1_zonas.py adaptado al addendum (permutación de etiquetas), y después D2, D4, D3, D5 y D7.

## Subagentes
- Revisor F2: unos 55.000 tokens según su propia estimación; la notificación del sistema contabiliza 69.477 (tope 100.000).
