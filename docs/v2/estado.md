# Estado v2

| Tarea / rama | Estado | Veredicto | Evidencia principal | Tokens subagentes |
|---|---|---|---|---|
| Paso 0 setup | hecho | — | — | 0 |
| Paso A literatura | hecho | — | 51 verificadas (46 Q1/Q2) | 167.921 |
| Paso A B0 datos (descargas) | hecho | — | INE prov., MIVAU/Catastro, UE/BdE, eventos | 797.979 |
| Paso A B0 paneles (limpiador) | hecho | — | 7 paneles; sellado 686 filas prov-trim | 265.765 |
| G0 viabilidad + prereg | hecho | — | H1-H7; BT recortada; ancla SHA 910c42a | 0 |
| Infra v2_common (bloques, AR4, ECM v1, DM-HLN) | hecho | — | 16 tests (4 de no-fuga) | 76.956 |
| BA alquiler | revisión (wt-BA) | — | H1 parcial: + pob 20-34; extranjera n.s. | 150.917 |
| BV compra | REHACER it.1 (evaluar_H2) | REHACER | H2 dentro de muestra: signos esperados; sin mejora OOS | 99.084 + rev. 108.603 |
| BI inmigración | revisión (wt-BI) | — | β_alquiler 3,06 (2SLS); compra n.s. | 144.852 |
| Literatura métodos (anexo v2-B) | hecho | — | 5 nuevas; 2 NO VERIFICADAS (actas NeurIPS) | 55.684 |

**Hecho:** rama r2/main; requirements.lock; data/sealed ignorado; CLAUDE.md v2; .claude/settings.json (permisos + hook ruff); subagentes v2 (data-fetcher haiku, econometrician/ml-engineer/lit-researcher sonnet, reviewer opus); comandos /rama y /estado; checksums de ficheros >50 MB.
**Siguiente:** puertas de BA, BV, BI → evaluación sellada H1/H2 tras APROBAR → ola 2 (BO, BP, BM).
**Tokens de subagentes v2 acumulados:** 1.867.761.
