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

## Siguiente paso exacto
- Revisor de F2 (opus, tope 100k) → F3, D1a y D1b (src/v9/d1_zonas.py) según hipotesis.md.

## Subagentes
- Ninguno.
