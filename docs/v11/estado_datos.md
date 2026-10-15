# V11-DATOS · Estado

## Hecho
- Inventario (docs/v11/inventario.md); infraestructura src/v11 (comun.py, datos_v11.py; `make datos_v11`).
- Bloque 1:
  - EMCR 2021-2024 completa y validada (microdatos y 8 tablas municipales).
  - ECP trimestral provincial por nacionalidad (4 tablas).
  - Eurostat asilo y protección temporal (nacional).
  - Eventos normativos del BOE (85 normas y 171 modificaciones).
  - EVR 1988-2021 y MNP 1980-2024 completos y validados.
  - OPI e Interior fallidos (fuentes_fallidas.md).

## Siguiente (para `claude --continue`)
1. Bloque 1 cerrado salvo OPI e Interior (segunda pasada).
2. Bloque 2:
   - Censo 2021: las tablas tpx y el agregado de viviendas ya están hechos; el de personas está en curso
     (`python3 src/v11/fetch_ine_censo2021.py`, con caché).
   - Auditoría ECV/EPA y ECEPOV: hechas.
3. Bloque 3:
   - Catastro INSPIRE en curso (`python3 src/v11/fetch_catastro_inspire.py`).
   - Siguiente: valores de referencia, MIVAU y Ajuntament.

## Tokens de subagentes
Ninguno (la tarea prohíbe subagentes).
