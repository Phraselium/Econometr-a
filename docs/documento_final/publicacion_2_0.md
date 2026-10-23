# Publicación 2.0: preparada, sin publicar (2026-10-23)

Ensayo de la consolidación final. Nada se ha subido a GitHub público, Zenodo ni OSF: lo hace el autor (docs/tareas_autor.md).

## Versión
proyecto.json: `version_publica` 2.0, `fecha_version` 2026-10-23, `estado_publicacion` «preparada y sin publicar». La 1.0 (2026-10-16) no llegó a depositarse. Puertas de entrada, CITATION.cff, .zenodo.json, consulta/ y web regenerados con la 2.0 (`make metadatos publicacion consulta web`); check_v13 comprueba que todas declaran la misma.

## Paquete de Zenodo (`make paquete_zenodo`)
- `_deposito/vivienda-espana-evidencia-2.0/` (ignorado por git): 5.467 ficheros incluidos, 73 versionados excluidos, 7 variables AEAT quitadas de la capa pública, 1.510 MB.
- `sha256sum -c CHECKSUMS.sha256`: correcto en todos los ficheros. sha256 del propio CHECKSUMS.sha256: `0737d4265abdc593c1d9264f6ac6b1d004c765bdb0e048eb475f20b831acdf69` (de este ensayo; el autor regenera el paquete desde el commit final).
- Incluye publicacion/documento_final/ (documento y resumen ejecutivo).
- No se generó el zip (duplicaría el tamaño en un disco con 2,6 GB libres); lo hace el autor con `--zip`.

## Árbol público (`src/v14/arbol_publico.py`)
- 4.455 ficheros, 1.140 versionados excluidos, 31 tablas redactadas, origen c437a8d.
- **Desviación:** se generó con `--sin-git` en el directorio temporal de la sesión, no con `make arbol_publico DEST=…`, porque el árbol con su repositorio git no cabía junto al paquete en el disco de la sesión (y no se pudo borrar el paquete). El contenido es el mismo; el commit único «Versión 2.0» lo crea `make arbol_publico` en la máquina del autor.
- El primer intento se detuvo por dos rutas locales en ficheros versionados (docs/v16/preparacion_2_0.md y el valor por defecto del directorio temporal de src/v18/estimacion/e1_adquisicion.py); se corrigieron y el árbol se generó sin avisos.

## Escaneo de series de terceros (`src/v14/escaneo_terceros.py --valores`), tras K16
Decisión del autor del 2026-10-23 (docs/v18/decisiones.md, K16): `terceros_1_0.aeat` = «redistribuir», con la atribución de LICENSE, punto 5. Paquete y árbol regenerados después: paquete con 5.483 ficheros, 67 versionados excluidos, **0 variables AEAT quitadas**, 1.511 MB, CHECKSUMS.sha256 verificado (sha256 del CHECKSUMS de este ensayo: `d85d813a129d2cee1088457d827fb3ac849c3e2e5e04f0cdc98af78a266958d3`); árbol con 4.461 ficheros, 1.140 versionados excluidos y 26 tablas redactadas (generado con `--sin-git`, por la misma razón de disco). Resultados fichero a fichero: docs/documento_final/escaneo_2_0/escaneo.csv y escaneo_valores.csv.

| Ámbito | Ficheros con hallazgos | Pendientes |
|---|---|---|
| Repositorio | 99 | 0 |
| Árbol 2.0 | 73 | 0 |
| Paquete 2.0 | 76 | 0 |
| Coincidencias por valores (árbol y paquete) | 8 | 0 |

**Decisión aplicada a los 16 ficheros que la 1.0 no había revisado.**

| Fichero | Fuente | Decisión |
|---|---|---|
| output/v12/b5/aeat_cv_2013_2015.csv | AEAT | entra (redistribuir, con atribución) |
| output/v12/b5/aeat_cv_declarantes_inmuebles.csv | AEAT | entra (redistribuir, con atribución) |
| output/v15/auditoria/renta_microdatos/aeat_comprobacion_unidades_2016_2024.csv | AEAT | entra (redistribuir, con atribución) |
| output/v15/auditoria/renta_microdatos/aeat_estructura_por_ejercicio.csv | AEAT | entra (redistribuir, con atribución) |
| output/v15/auditoria/renta_microdatos/aeat_hipotesis_recuentos_2015.csv | AEAT | entra (redistribuir, con atribución) |
| output/v15/auditoria/renta_microdatos/aeat_razones_entre_ejercicios.csv | AEAT | entra (redistribuir, con atribución) |
| output/v15/auditoria/renta_microdatos/resultado.json | AEAT | entra: diagnósticos propios (redistribuir) |
| output/v16/auditoria/tension_social/resultado.json | CGPJ | **excluido (vaciado con nota)**: recuentos de lanzamientos casi sin transformar; la licencia del CGPJ no está verificada (su aviso legal no respondió desde la sesión) |
| docs/v14/escenarios_resultado.json | varias | entra: metadatos de la política, sin series |
| docs/v16/sellado_v16.json | CGPJ (claves) | entra: fechas del sellado, sin valores |
| docs/v18/sellado_v18.json | AEAT (claves) | entra: fechas del sellado, sin valores |
| output/v15/auditoria/precios_compra/resultado.json | Notariado, Registradores | entra: diagnósticos propios de calidad, sin series |
| output/v16/f2_hechos/control.json | varias | entra: grupo de independencia de cada fuente, sin valores |
| output/v16/potencia/resultado.json | Registradores | entra: recuentos de unidades, sin valores |
| output/v16/replica/v10_a/resultado.json | Notariado, Registradores | entra: variaciones calculadas (agregados propios; Notariado con atribución, Registradores con el aviso de la ODbL) |
| revision_externa/2_0/hoja_revision.xlsx | varias | entra: enunciados publicados y cifras propias, sin series |

Además, con «redistribuir» vuelven sin redactar ni vaciar las tablas de la AEAT que la 1.0 vaciaba (output/v12/f0/aeat_*, output/v5/CB/tablas/aeat_*, output/v15/auditoria/renta_microdatos/coherencia_aeat_adrh_*), las 7 variables `aeat_irpf_*` de la capa pública y las series brutas de data/raw (v11/aeat_irpf_municipios y v5/cb_aeat_*.html).

**Falsos positivos por valores (3, en el árbol y en el paquete), documentados en el escáner (FALSOS_POSITIVOS_VALORES):** docs/v18/bib/inmigracion/sa_2015_iza.md (ficha bibliográfica: años y cifras del estudio citado), output/v15/auditoria/alquiler/cobertura_temporal_variables.csv (años y recuentos de periodos) y output/v18/estimacion/e6/informe.md (años, recuentos y coeficientes propios). Las otras coincidencias por valores son tablas de la AEAT, que ahora se redistribuyen.

## Revisión externa 2.0 (`make revision_externa_2_0`)
revision_externa/2_0/: muestra.csv y hoja_revision.xlsx (40 cifras del documento final, estratificadas por capa y clase V18, SEED=20261010: C1 4, C2 4, C3s 1, C4 sin clase V18 4, SUGESTIVO 3, ASOCIACIÓN 4, NO CONCLUYENTE 2, NO ESTIMABLE 4, sin clase propia 14), resumen_ejecutivo.pdf (dos páginas apaisadas en español y una en inglés) y guía de dos páginas (guia.md y guia.pdf).
