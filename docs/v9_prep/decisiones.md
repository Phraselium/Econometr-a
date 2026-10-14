# Decisiones V9-PREP (investigación documental)

## P0 — Alcance y organización (2026-10-14)
- Solo se crean ficheros nuevos en docs/v9_prep/. No se estima nada, no se tocan datos, salidas ni entregables y no se abren muestras selladas.
- Rama local `v9-prep` (desde r8.1/main); se sube a la rama designada `claude/housing-price-spain-econometric-95dhj3`.
- Cuatro subagentes lit-researcher (sonnet), con un presupuesto de unos 130.000 tokens cada uno (≤0,6 M en total): fuentes de datos (bloque 1), literatura A (turismo, inmigración y demografía, hogares, oferta, crédito, burbujas, factor europeo), literatura B (inversores, extranjeros, regulación, ayudas, vivienda pública, temporada y vacía) y métodos (bloque 3). Las entradas parciales van a docs/v9_prep/_parcial/. Los bloques 4 y 5, el resumen y la consolidación (literatura.csv único, referencias.bib único) los hace el orquestador.
- Verificación: DOI en Crossref u OpenAlex, o enlace oficial. Cuartil de Scimago si responde (desde este entorno suele dar 403); si no, otra fuente declarada, o «cuartil no verificado».
