# Decisiones V9 COMPLETO (datos, modelización local e integración en la web)

Rama local `r9/main`, subida a la rama remota designada (`claude/housing-price-spain-econometric-95dhj3`), la única a la que se puede subir (CLAUDE.md). Las decisiones de la descarga de datos de V9 siguen en docs/v9/decisiones_datos.md (D0-D7). Referencias: v8.1 para resultados y V10 para base y web.

## E0 — Correcciones de la web de V10 (F0)
- **Sobrecarga en alquiler** (V10-ATL-A1 y A3; 38,1 % → 26,8 %, 2018-2025). El atlas y la página «Quién soporta el coste» explican tres cosas para que no se lea como «el problema mejora»:
  - la ECV mide a todos los inquilinos, sobre todo con contratos antiguos;
  - la renta es la del año anterior;
  - el periodo coincide con subidas salariales.
  - Al lado se ponen las cifras C1 de contratos nuevos: A23-A10, Comunitat Valenciana 28,5 % (2021-2024); A23-A9, Cataluña 16,9 %.
- **Brecha del IPVA** (V10-ATL-B1). Se presenta como «diferencia de puntos de índice (base 2015)» y se aclara explícitamente que no es un porcentaje de encarecimiento.
- **València +39,8 % (2019-2024)**: «C4, fuente única (SERPAVI)» en el atlas, la figura F10, las fichas municipales (nueva fila de variación del alquiler) y los mapas.
- **Cifras.** Ninguna cambia: solo cambia el texto. `make web` y `make check` (rc = 0).
