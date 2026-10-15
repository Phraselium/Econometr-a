# V11-DATOS · Estado

## Hecho
- Inventario (docs/v11/inventario.md); infraestructura src/v11 (comun.py, datos_v11.py; `make datos_v11`).
- Bloque 1:
  - EMCR 2021-2024 completa y validada (microdatos y 8 tablas municipales).
  - ECP trimestral provincial por nacionalidad (4 tablas).
  - Eurostat asilo y protección temporal (nacional).
  - Eventos normativos del BOE (85 normas y 171 modificaciones).
  - EVR 1988-2021 y MNP 1980-2024 corriendo en segundo plano (logs evr.log y mnp.log en el scratchpad).
  - OPI e Interior fallidos (fuentes_fallidas.md).

## Siguiente (para `claude --continue`)
1. Cuando terminen EVR y MNP: validar, registrar y hacer commit. Si se cortan, relanzar `python3 src/v11/fetch_ine_evr.py` y
   `python3 src/v11/fetch_ine_mnp.py` (con caché de originales).
2. Bloque 2: Censo 2021 (tablas de hogares y viviendas por sección o municipio y nacionalidad), auditoría de
   variables ECV/EPA y ECEPOV.

## Tokens de subagentes
Ninguno (la tarea prohíbe subagentes).
