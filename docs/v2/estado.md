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
| BM modelos | APROBADA y fusionada; H7 sellada evaluada | APROBAR (it.2) | H7 NO confirmada; LSTM negativo | 274.876 + rev. 148.438 |
| BD descomposición | APROBADA y fusionada | APROBAR (it.2 + C1) | EXPLORATORIO; atribuciones de compra no robustas | 240.745 + rev. 171.515 |
| BS síntesis | fusionada; revisión final en curso | — | informe_v2.md; ninguna confirmatoria sobrevive Holm-7 | 312.146 |
| Holm-7 (orquestador) | hecho | — | ninguna confirmatoria sobrevive | 0 |
| BP política | APROBADA y fusionada; H6 sellada evaluada | APROBAR (verif. final) | H5 EXPLORATORIO; H6 SDiD −0,0117 (p 0,014) cumple regla, con discrepancias | 162.854 + rev. 175.026 |
| Literatura anexo v2-C | hecho | — | Roodman 2019 verificada; JRS 2018 WP | 19.903 |
| Literatura métodos (anexo v2-B) | hecho | — | 5 nuevas; 2 NO VERIFICADAS (actas NeurIPS) | 55.684 |

**Hecho:** rama r2/main; requirements.lock; data/sealed ignorado; CLAUDE.md v2; .claude/settings.json (permisos + hook ruff); subagentes v2 (data-fetcher haiku, econometrician/ml-engineer/lit-researcher sonnet, reviewer opus); comandos /rama y /estado; checksums de ficheros >50 MB.
**Siguiente:** revisión final + make all ×2 sin red en clon limpio (en curso) → cierre. Selladas: H1 mejora predictiva sí (conjunta no), H2 no, H6 cumple regla nominal, H7 no. Holm-7: ninguna.
**Tokens de subagentes v2 acumulados:** 4.744.791.
