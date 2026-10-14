# Decisiones V9-PREP (investigación documental)

## P0 — Alcance y organización (2026-10-14)
- Solo se crean ficheros nuevos en docs/v9_prep/. No se estima nada, no se tocan datos, salidas ni entregables y no se abren muestras selladas.
- Rama local `v9-prep` (desde r8.1/main); se sube a la rama designada `claude/housing-price-spain-econometric-95dhj3`.
- Cuatro subagentes lit-researcher (sonnet), con un presupuesto de unos 130.000 tokens cada uno (≤0,6 M en total): fuentes de datos (bloque 1), literatura A (turismo, inmigración y demografía, hogares, oferta, crédito, burbujas, factor europeo), literatura B (inversores, extranjeros, regulación, ayudas, vivienda pública, temporada y vacía) y métodos (bloque 3). Las entradas parciales van a docs/v9_prep/_parcial/. Los bloques 4 y 5, el resumen y la consolidación (literatura.csv único, referencias.bib único) los hace el orquestador.
- Verificación: DOI en Crossref u OpenAlex, o enlace oficial. Cuartil de Scimago si responde (desde este entorno suele dar 403); si no, otra fuente declarada, o «cuartil no verificado».

## P1 — Consolidación y presupuesto (2026-10-14)
- **Presupuesto de subagentes:** 681.117 tokens (métodos 78.477; fuentes 208.965; literatura B 211.665; literatura A 182.010). Supera el tope de 0,6 M en unos 81.000 (+13,5 %). El orquestador no podía cortar a los subagentes en curso sin perder su trabajo verificado. Se declara aquí y no se lanzaron más subagentes; la síntesis (bloques 4 y 5, resumen y consolidación) la hizo el orquestador.
- **Deduplicación:** LB31 = LA01, LB04 = LA20 y LB05 = LA19 se fusionan en una fila. LB23 (Bono Alquiler Joven) y LB34 (evaluación BdE/AIReF de la Ley 12/2023) son lagunas, no referencias: van a _parcial/lagunas_literatura.csv.
- **Recuentos finales:**

  | Bloque | Entradas | DOI verificado | Cuartil con fuente |
  |---|---|---|---|
  | Fuentes de datos | 38 | — | — |
  | Literatura | 64 | 59 | 44 |
  | Métodos | 23 | 23 | 19 |

  referencias.bib tiene 88 entradas únicas por DOI.
- **No se modifican** docs/literatura.md, docs/v5/licencias_datos.md ni docs/v3/fuentes_fallidas.md (solo ficheros nuevos). Las correcciones propuestas (González y Ortega 2013; licencia del Incasòl; microdatos de la EFF 2022; licencia del INE) quedan en literatura.md, fuentes_datos.md y resumen.md para que el autor las aplique.
- **Cautelas añadidas por el orquestador** sobre cifras no verificadas en el original: OCDE 2025 (resumen de buscador), magnitud de Sanchis-Guarner, número y fechas de los municipios declarados zona tensionada, y si la Comunitat Valenciana ha declarado zonas.
