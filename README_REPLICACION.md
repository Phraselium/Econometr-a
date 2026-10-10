# Paquete de replicación: vivienda en España (v1-v5)

**Autor:** Borja Romero, economista (firma individual, independiente). **Versión:** 5.0. **Cita:** CITATION.cff. **DOI:** pendiente (Zenodo; .zenodo.json). **Licencia:** CC BY 4.0 para el código y los textos propios; los datos de terceros conservan su licencia (docs/v5/licencias_datos.md).

Este README sigue el modelo de los editores de datos (AEA Data Editor / Social Science Data Editors). Explica cómo reproducir **todas** las tablas, figuras y documentos del proyecto a partir de los datos incluidos y sin conexión a la red.

## 1. Resumen
| Concepto | Valor |
|---|---|
| Orden principal | `make all` (data → clean → models → report → verificador) |
| Red | No es necesaria. Las descargas están en caché en data/raw; `make data` solo vuelve a descargar con `FORCE=1`. |
| Tiempo | ≈22 minutos por ejecución completa (`make all`), medido dos veces en un clon limpio con un solo hilo: 1.333 s y 1.312 s. |
| Determinismo | Un solo hilo (OMP, OpenBLAS y MKL = 1) y SEED = 20261010. Dos ejecuciones en clon limpio dan md5 idénticos en output/ y data/processed, salvo `output/v2/BM/tiempos.json` (tiempos de reloj). |
| Comprobaciones | `make check`: ruff, pytest, control de texto (neutralidad, capas, verbos de atribución) y `src/v5/check_v5.py`. check_v5 comprueba: toda cifra de los entregables v5 sale de output/v5/cifras_clave.csv; la suma provincial es igual a la nacional; los recuentos usan solo documentos oficiales; ningún script lee ficheros no versionados; ningún tope aparece en C3. `make verificador`: regenera las fichas v3, v4 y v5. |
| Software | Python 3.13. Versiones fijadas en `requirements.lock` (154 paquetes; incluye torch CPU para un módulo de v2). Programa del sistema: `pdftotext` (poppler-utils), que usa `src/v5/a5_run.py` para leer los programas oficiales. |
| Hardware | CPU genérica, ≥8 GB de RAM y ≈2 GB de disco para un clon con datos. |

## 2. Cómo reproducir
```bash
git clone <repositorio> && cd Econometr-a
python3 -m pip install -r requirements.lock
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
make all          # reconstruye paneles, modelos v1-v4, informes y verificador
make check        # ruff + tests + control de texto
```
Si se quiere impedir explícitamente el acceso a la red, puede usarse `HTTPS_PROXY=http://127.0.0.1:9`. Así se verificó la reproducción.

### Orden de los programas (Makefile)
1. `data`: `src/fetch_*.py` y `src/extract_*.py`. Usan la caché y no acceden a la red si existen los ficheros.
2. `clean`: `src/build_dataset.py`, `src/build_dataset_v2.py` y `src/holdout.py build`. Este último separa la muestra sellada de v2.
3. `models`, en este orden:
   - v1: `src/f2_*.py` a `src/f6_*.py`;
   - v2: `src/v2/{ba_run, bv_main, bi_run, bo_run, bp_main, bm_run, bd_run, bs_run}.py`;
   - v3: `src/v3/{pa_run, pb_run, pot_run, gl_run, c1_run, c3_run, holm_v3, pd_run}.py`;
   - v4: `src/v4/{m0_run, m2_run, m1_run, m3_run, m4_run, m7_run, m5_run}.py`;
   - v5 (`V5_ORDEN` del Makefile):
     - `r1t_run, r1c_run, r1a_run, r1b_run`: recuperación de pendientes;
     - `a23_run, a4_run, a5_run, a5_hechos`: cierre de v4;
     - `b1_run, b2_run, b3_run, b4_run`: necesidades y territorio;
     - `ca_run, cb_run, cc_run`: ángulos pendientes;
     - `d1_run, d2_run`: política;
     - `e_hechos, cifras_clave, d3_run, cifras_clave, render`: tabla única de cifras, convergencia y entregables. `render.py` rellena las plantillas `docs/v5/plantillas/*.md` en `output/v5/`.
4. `report`: `src/report.py` y el verificador (`src/v3/verificador.py`, `src/v4/verificador.py`, `src/v5/verificador.py`).

Los scripts de descarga de v3, v4 y v5 (`src/v3/fetch_*`, `src/v4/m*_fetch.py`, `src/v5/*_fetch.py`) **no** forman parte de `make all`. Sus salidas están versionadas en data/raw/v3, data/raw/v4 y data/raw/v5.

### Pre-registro
Las hipótesis confirmatorias de B3 (diferencias entre provincias) están en docs/v5/prereg_B3.md, en un commit anterior a cualquier salida de B3. La etiqueta git `prereg-v5` está en el repositorio local; el remoto de la sesión no acepta etiquetas (docs/v5/bloqueos.md).

### Muestra sellada
- v2 y v3 reservan una muestra sellada para la evaluación confirmatoria. Solo se accede a ella a través de `src/holdout.py`, que registra cada acceso. La copia versionada del registro es docs/v2/holdout_accesos.md.
- Las evaluaciones ya hechas se leen de los ficheros `*_sellado*.json` versionados: `make all` **no** reabre la muestra sellada.

## 3. Datos: fuentes, acceso y licencias
El inventario completo, con fichero, fuente, número de series, fechas y fecha de descarga, está en `data/raw/_manifest.csv` (110 ficheros). Resumen por organismo:

| Organismo | Datos | Acceso | Licencia o condiciones |
|---|---|---|---|
| INE | IPV, IPC de alquiler, EPA, ECP, censos 2011/2021, censo anual por sección, Atlas de renta (ADRH), viviendas turísticas por sección (estadística experimental), ETDP, ECV | API JSON (servicios.ine.es) y servicios ArcGIS (www.ine.es/servergis) | Reutilización libre con cita de la fuente (aviso legal del INE; Ley 37/2007) |
| Ministerio de Vivienda y Agenda Urbana | Viviendas terminadas e iniciadas, valor tasado, precio del suelo urbano, transacciones por residencia, SERPAVI | Boletín Online (apps.fomento.gob.es) y cdn.mivau.gob.es | Reutilización con cita (Ley 37/2007) |
| Dirección General del Catastro | Estadísticas catastrales municipales: unidades urbanas por uso, solares | catastro.hacienda.gob.es | Reutilización con cita |
| Banco de España | Tipos, crédito, precio de la vivienda, EFF (cuadros publicados) | bde.es | Reutilización con cita |
| BCE, BIS, OCDE, Eurostat | Tipos, IAPC, precios de la vivienda, empleo, migración, emancipación | API públicas | Eurostat: CC BY 4.0; los demás, reutilización con cita |
| Consejo General del Notariado y Colegio de Registradores | Compraventas por nacionalidad, precios | Estadísticas publicadas (PDF y datos abiertos) | Condiciones de reutilización no verificadas; se usan agregados publicados con cita |
| Incasòl / Generalitat de Catalunya | Fianzas de alquiler por municipio | analisi.transparenciacatalunya.cat (Socrata) | CC BY 4.0 |
| Generalitat Valenciana, Ayuntamiento de València, Comunidad de Madrid | Viviendas turísticas, padrón municipal, alquiler por código postal | portales de datos abiertos | Reutilización con cita |
| BOE y diarios oficiales | Normas y zonas tensionadas | boe.es | Dominio público |
| Inside Airbnb | Agregados de anuncios (solo robustez) | insideairbnb.com | CC BY 4.0 |
| Programas electorales y proposiciones de ley (M5 y A5) | v4: citas ≤40 palabras (data/raw/v4/medidas_programas.csv). v5: 22 documentos oficiales en PDF con URL y hash (docs/v5/programas/inventario.csv); las copias no oficiales quedan fuera de los recuentos | Webs oficiales de las formaciones y congreso.es | Cita breve con fines de investigación; véase docs/v5/licencias_datos.md |

**Ficheros de más de 50 MB.** No están en el repositorio. Sus checksums están en `data/CHECKSUMS.sha256` y se regeneran con los scripts de descarga. Ninguno es necesario para `make all`.

**Datos no disponibles.** Ver docs/v3/fuentes_fallidas.md y docs/v4/fuentes_fallidas.md. Las solicitudes de transparencia redactadas están en docs/v3/solicitudes_transparencia.md y docs/v4/solicitudes.md.

## 4. Correspondencia entre salidas y programas
| Salida | Programa |
|---|---|
| output/informe.md (v1) | src/report.py, src/f*_*.py |
| output/v2/informe_v2.md | src/v2/bs_run.py |
| output/v3/{lo_que_sabemos, articulo, informe_politica}.md | redactados a partir de output/v3/*/ (PA, PB, C1, C3, GL, PD) |
| output/v4/{working_paper, informe_tecnico, policy_brief, lo_que_sabemos}.md | redactados a partir de output/v4/M0-M7 |
| output/v4/M0 … M7 | src/v4/m0_run.py … m7_run.py (M6 = docs/v4/preguntas_abiertas.md, solicitudes.md) |
| output/v5/cifras_clave.{csv,md} (tabla única de cifras v5) | src/v5/cifras_clave.py |
| output/v5/{R1A,R1B,R1C,R1T,A23,A4,A5,A6,B1,B2,B3,B4,CA,CB,CC,D1,D2,D3} | src/v5/<módulo en minúsculas>_run.py (A6: nota de consolidación) |
| output/v5/{informe_tecnico, working_paper, policy_brief, lo_que_sabemos, una_pagina, articulo_colegio}.md, articulos/, ponencia/, linkedin/ | docs/v5/plantillas/ + src/v5/render.py |
| output/v5/verificador/ | src/v5/verificador.py |
| Las 15 cifras más citables, con script y línea | docs/v5/revision_humana.md |
| Working paper, tabla de hechos (déficit, hogares, terminadas) | m0_run.py (output/v4/M0/), m2_run.py (output/v4/M2/) |
| Working paper e informe, mapas y concentración provincial | m1_run.py (output/v4/M1/figuras, tablas) |
| Clasificación territorial (clases 1-4 y 9) | m3_run.py (output/v4/M3/) |
| Parque y mercado, compradores extranjeros | m4_run.py (output/v4/M4/) |
| Precios triangulados y GSADF | m7_run.py (output/v4/M7/tablas) |
| Matriz de instrumentos | m5_run.py (output/v4/M5/matriz_instrumentos.{csv,md}) |
| output/v3/verificador/, output/v4/verificador/ | src/v3/verificador.py, src/v4/verificador.py |

Los documentos de síntesis (.md) se redactan a partir de las salidas. Las cifras citadas en ellos proceden de los JSON y CSV indicados, y `src/v3/check_texto.py` controla su redacción.

## 5. Independencia, contacto y uso de IA
El trabajo es individual e independiente: no hay financiación externa ni vínculo con partidos. Si algo cambiara, se declararía aquí. Se evalúan afirmaciones e instrumentos, nunca partidos ni personas. Las correcciones se publican en ERRATA.md y los cambios en CHANGELOG.md.

El proyecto se ejecutó con agentes de IA (Claude) bajo supervisión de la persona responsable del repositorio. El uso de IA se declara en output/v3/articulo.md §10, en output/v4/working_paper.md (apéndice C) y en output/v5/working_paper.md (apéndice C). El autor es responsable del contenido. Antes de publicar, el autor replica a mano las 15 cifras de docs/v5/revision_humana.md.
