# Plan v4: dónde falta vivienda, por qué, si se puede construir allí, mercado frente a parque e instrumentos

V1, V2 y V3 están cerradas. La v4 mantiene la escala de capas de v3 (C1 hechos, C2 cotas, C3 efectos, C4 exploratorio) y la neutralidad del verificador. Reutiliza datos, `src/econ_utils.py`, `src/holdout.py`, `make check` y `make verificador`.

## Módulos y orden
| Orden | Módulo | Contenido | Capa | Presupuesto de subagentes |
|---|---|---|---|---|
| 1 | M0 Cierre de v3 | Conciliación del déficit (v1, v3, BdE); triangulación de terminadas; verificador con «ANALIZADA, NO CONCLUYENTE» y «NO ANALIZADA: FALTAN DATOS»; cotas con las dos convenciones; contaminación de los topes; por qué no se replica García-López | C1/C2 | ≤0,2 M |
| 2 | M2 ¿Por qué tantos hogares? | Descomposición de la creación de hogares: población (nativos, extranjeros, migración), estructura por edad y tasa de jefatura; demanda latente juvenil | C1 | ≤0,4 M |
| 2 | M1 Geografía del déficit | Provincias y municipios de más de 10.000 habitantes, 2012-2025 y 2021-2025; concentración; excedentes; latente | C1/C2 | ≤0,4 M |
| 3 | M4 Parque frente a mercado | Stock por uso y titular; flujos por tipo de comprador y arrendador; oferta anunciada (solo como robustez) | C1 | ≤0,4 M |
| 4 | M3 ¿Se puede construir? | Suelo y solares; brecha precio-coste (Glaeser-Gyourko); capacidad del sector; clasificación municipal | C1/C2 | ≤0,4 M |
| 5 | M5 Instrumentos | Medidas de los programas oficiales agrupadas por instrumento, más instrumentos no propuestos; rúbrica idéntica; simulación P-D | C2/C4 | ≤0,4 M |
| 6 | M6 Preguntas abiertas | Lista priorizada; solicitudes de transparencia o de convenio | — | mínimo |

Puertas del reviewer: oleada A (M0-M2), oleada B (M3-M4) y oleada C (M5-M6, entregables). `make check` en cada puerta. Presupuesto total: 2,5 M tokens de subagentes; al 80 % de cualquier límite, se cierra y se anota.

## Entregables
- output/v4/working_paper.md
- output/v4/informe_tecnico.md (con módulo València)
- output/v4/policy_brief.md
- output/v4/lo_que_sabemos.md
- verificador v4 (`make verificador`)
- README_REPLICACION.md
