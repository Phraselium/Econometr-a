# Paquete de replicación: vivienda en España (v1-v4)

Este README sigue el modelo de los editores de datos (AEA Data Editor / Social Science Data Editors). Explica cómo reproducir **todas** las tablas, figuras y documentos del proyecto a partir de los datos incluidos y sin conexión a la red.

## 1. Resumen
| Concepto | Valor |
|---|---|
| Orden principal | `make all` (data → clean → models → report → verificador) |
| Red | No es necesaria. Las descargas están en caché en data/raw; `make data` solo vuelve a descargar con `FORCE=1`. |
| Tiempo | ≈20-21 minutos por ejecución completa (`make all`), medido dos veces en un clon limpio con un solo hilo: 1.218 s y 1.222 s. |
| Determinismo | Un solo hilo (OMP, OpenBLAS y MKL = 1) y SEED = 20261010. Dos ejecuciones en clon limpio dan md5 idénticos en output/ y data/processed, salvo `output/v2/BM/tiempos.json` (tiempos de reloj). |
| Comprobaciones | `make check`: ruff, pytest y el control de texto de neutralidad y de capas. `make verificador`: regenera las fichas de afirmaciones v3 y v4. |
| Software | Python 3.13. Versiones fijadas en `requirements.lock` (154 paquetes; incluye torch CPU para un módulo de v2). |
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
   - v4: `src/v4/{m0_run, m2_run, m1_run, m3_run, m4_run, m7_run, m5_run}.py`.
4. `report`: `src/report.py` y el verificador (`src/v3/verificador.py`, `src/v4/verificador.py`).

Los scripts de descarga de v3 y v4 (`src/v3/fetch_*`, `src/v4/m*_fetch.py`) **no** forman parte de `make all`. Sus salidas están versionadas en data/raw/v3 y data/raw/v4.

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
| Programas electorales (M5) | Citas literales ≤40 palabras con procedencia (data/raw/v4/medidas_programas.csv) | Webs de los partidos (5 documentos) y copias no oficiales alojadas por medios (4 documentos; docs/v4/cobertura_programas.md) | Cita breve con fines de investigación |

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
| Working paper, tabla de hechos (déficit, hogares, terminadas) | m0_run.py (output/v4/M0/), m2_run.py (output/v4/M2/) |
| Working paper e informe, mapas y concentración provincial | m1_run.py (output/v4/M1/figuras, tablas) |
| Clasificación territorial (clases 1-4 y 9) | m3_run.py (output/v4/M3/) |
| Parque y mercado, compradores extranjeros | m4_run.py (output/v4/M4/) |
| Precios triangulados y GSADF | m7_run.py (output/v4/M7/tablas) |
| Matriz de instrumentos | m5_run.py (output/v4/M5/matriz_instrumentos.{csv,md}) |
| output/v3/verificador/, output/v4/verificador/ | src/v3/verificador.py, src/v4/verificador.py |

Los documentos de síntesis (.md) se redactan a partir de las salidas. Las cifras citadas en ellos proceden de los JSON y CSV indicados, y `src/v3/check_texto.py` controla su redacción.

## 5. Contacto y uso de IA
El proyecto se ejecutó con agentes de IA (Claude) bajo supervisión de la persona responsable del repositorio. El uso de IA se declara en output/v3/articulo.md §10 y en output/v4/working_paper.md, apéndice C.
