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

- Bloque 2 completo: Censo 2021 (37 tablas tpx, agregados muestrales de viviendas y hogares por nacionalidad), ECEPOV
  (microdatos e inventario), auditoría ECV/EPA.
- Bloque 3: Catastro INSPIRE (51 municipios, sección y barrio); Catastro estadísticas y MIVAU sin edición nueva;
  València datos abiertos (CKAN: 9 conjuntos, GTFS EMT incluido).
- Bloque 4:
  - Afiliación municipal de la Seguridad Social (en curso).
  - REATE Euskadi.
  - GVA VUT: sin edición nueva.
  - Turismo con móviles (en curso).
  - CGPJ y BdE: sin edición nueva.
- Bloque 5: docs/v11/solicitudes.md (7 solicitudes).
- Bloque 6: src/v11/base_v11.py enlazado en src/v10/base.py (≈600.000 filas nuevas).

## Siguiente (para `claude --continue`)
1. Esperar a que terminen `src/v11/fetch_ss_afiliacion_municipio.py` y `src/v11/fetch_ine_turismo_moviles.py`
   (logs afi.log y moviles.log en el scratchpad). Si se cortan, relanzarlos (sin caché: rehacen las descargas).
2. `make datos_v11`, `make base` y `make check`.
3. Segunda pasada de fuentes fallidas (OPI, Interior, Barcelona HUT, universidades, valores de referencia).
4. docs/v11/cobertura.md y auditoria_exhaustividad.md; commit y push.

## Tokens de subagentes
Ninguno (la tarea prohíbe subagentes).
