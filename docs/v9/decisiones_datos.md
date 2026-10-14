# Decisiones V9-DATOS (solo descarga y validación)

## D0 — Alcance y organización (2026-10-14)
- **Alcance.** Solo descarga, validación y documentación. No se estima nada, no se modifican salidas ni entregables y no se abren muestras selladas. Rama `v9-datos` (desde v9-prep), subida a la rama designada.
- **Infraestructura común** (orquestador):
  - src/v9/comun.py: descarga con caché, manifiesto por fuente y columna `posterior_prereg`;
  - src/v9/datos_v9.py: `make datos_v9`, que verifica sin red y descarga si falta, y consolida data/raw/v9/_manifest.csv.
- **Subagentes.** Cinco subagentes haiku en paralelo, con un tope explícito de 60.000 tokens cada uno y parada al 80 % (≤0,3 M en total, dentro del presupuesto de 0,4 M):
  - EMAL y afiliación;
  - INE (censo anual, IPVA, VUT y microdatos);
  - València (padrón, registro de viviendas turísticas de la GVA y fianzas de la GVA);
  - Inside Airbnb;
  - Eurostat, BCE, Aena e Incasòl.
- **Orquestador.** Hace la validación (tests), la cobertura, el diccionario, las licencias y .gitignore, y la integración con `make datos_terceros` y `make check`.
- **Periodos posteriores al pre-registro.** Las series de precios y alquileres con fecha llevan la columna `posterior_prereg` (True desde 2026T3, la fecha de inicio de evaluate_v7 y evaluate_v8). Esas filas no se usan en ningún cálculo y no se miran sus valores.
