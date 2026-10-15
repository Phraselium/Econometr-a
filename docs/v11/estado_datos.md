# V11-DATOS · Estado

## Hecho
- Inventario (docs/v11/inventario.md); infraestructura src/v11 (comun.py, datos_v11.py; `make datos_v11`).
- Bloque 1 en curso: EVR 1988-2021 (fetch_ine_evr.py) y EMCR 2021-2024 (fetch_ine_emcr.py; tablas jaxiT3 descargadas).

## Siguiente (para `claude --continue`)
1. Terminar EVR/EMCR (logs en el scratchpad) y validar totales.
2. MNP municipal (microdatos nacimientos/defunciones) → src/v11/fetch_ine_mnp.py.
3. ECP por nacionalidad, OPI, protección temporal/internacional, eventos BOE.

## Tokens de subagentes
Ninguno (la tarea prohíbe subagentes).
