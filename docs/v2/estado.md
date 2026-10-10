# Estado v2

| Tarea / rama | Estado | Veredicto | Evidencia principal | Tokens subagentes |
|---|---|---|---|---|
| Paso 0 setup | hecho | — | — | 0 |
| Paso A literatura | hecho | — | 51 verificadas (46 Q1/Q2) | 167.921 |
| Paso A B0 datos (descargas) | hecho | — | INE prov., MIVAU/Catastro, UE/BdE, eventos | 797.979 |
| Paso A B0 paneles (limpiador) | hecho | — | 7 paneles; sellado 686 filas prov-trim | 265.765 |
| G0 viabilidad + prereg | hecho | — | H1-H7; BT recortada; ancla SHA 910c42a | 0 |
| Infra v2_common (bloques, AR4, ECM v1, DM-HLN) | hecho | — | 16 tests (4 de no-fuga) | 76.956 |
| BA alquiler | APROBADA y fusionada; H1 sellada evaluada | APROBAR (it.2) | H1 conjunta EXPLORATORIO (p_IUT 0,85); mejora predictiva sellada vs AR(4) p=0,005 | 173.983 + rev. 141.720 |
| BV compra | APROBADA y fusionada; H2 sellada evaluada | APROBAR (it.2) | H2 NO confirmada en sellado (p=0,19); signos dentro de muestra EXPLORATORIO | 133.326 + rev. 139.310 |
| BI inmigración | APROBADA y fusionada | APROBAR (it.2) | H3 EXPLORATORIO; β_alq>0 EXPLORATORIO (GPSS, placebos) | 194.488 + rev. 132.141 |
| BO oferta y suelo | APROBADA y fusionada | APROBAR (it.2) | H4 EXPLORATORIO (2005-2023; inestable, placebo futuro) | 148.153 + rev. 140.152 |
| Datos: iniciadas/terminadas anuales | hecho | — | 2005-2023 sin huecos | 70.985 |
| BM modelos | revisión (wt-BM) | — | Ningún modelo supera AR(4)/ECM v1 en entrenamiento | 250.476 |
| BP política | re-revisión (it.2) | REHACER it.1 | H5 EXPLORATORIO (placebo y pretendencia fallan) | 158.552 + rev. 142.790 |
| Literatura anexo v2-C | hecho | — | Roodman 2019 verificada; JRS 2018 WP | 19.903 |
| Literatura métodos (anexo v2-B) | hecho | — | 5 nuevas; 2 NO VERIFICADAS (actas NeurIPS) | 55.684 |

**Hecho:** rama r2/main; requirements.lock; data/sealed ignorado; CLAUDE.md v2; .claude/settings.json (permisos + hook ruff); subagentes v2 (data-fetcher haiku, econometrician/ml-engineer/lit-researcher sonnet, reviewer opus); comandos /rama y /estado; checksums de ficheros >50 MB.
**Siguiente:** puertas de BI, BO, BP → BM → BD → BS. Evaluaciones selladas hechas: H1 (confirma mejora predictiva), H2 (no confirma).
**Tokens de subagentes v2 acumulados:** 3.381.596.
