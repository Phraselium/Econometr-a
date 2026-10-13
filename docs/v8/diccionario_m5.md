<!-- Sección añadida por M5 (F4). src/v8/f1_paneles.py la incorpora al final de docs/v8/diccionario.md. -->
## M5: datos de Eurostat descargados en F4 (data/raw/v8/eurostat_migr/)

Descarga única con `src/v8/fetch_m5.py` (API de difusión de Eurostat 1.0, JSON-stat; caché en `_cache/`; manifiesto con URL, fecha 2026-10-13, n y sha256 en `_manifest.csv`). El script de modelo `src/v8/m5_lpiv.py` no usa red.

| Fichero | Variables | Fuente | Cobertura | Uso |
|---|---|---|---|---|
| `migr_imm1ctz_ue.csv` | `geo` (destino), `citizen` (ciudadanía de origen), `anio`, `valor` (personas) | Eurostat migr_imm1ctz (age=TOTAL, sex=T, agedef=REACH, unit=NR) para 27 destinos UE (incl. ES) | 2002-2024; huecos por destino (FR desde 2006, BG desde 2007, RO desde 2008, PT hasta 2022; CY, EL, MT y PL con pocos orígenes) | IV2: emigración de cada origen hacia la UE sin España (destinos con total completo 2002-2024: 19) |
| `lfst_r_lfe2en2_sector.csv` | `geo` (NUTS2 y ES), `nace_r2` (10 sectores + TOTAL), `anio`, `valor` (miles de personas) | Eurostat lfst_r_lfe2en2 (sex=T, age=Y15-64, unit=THS_PER) | 2008-2025 | IV3: cuotas sectoriales de 2008 y crecimiento sectorial leave-one-out; empleo total regional. Celdas confidenciales (p. ej. sector L) = 0 |

Cuotas iniciales de IV2: población extranjera residente por ciudadanía a 1-1-2002 (`data/raw/v8/eurostat_migr_pop1ctz_es.csv`, Eurostat migr_pop1ctz, ES). Llegadas a España: Eurostat migr_imm1ctz, ES, total (la serie `inmig_anual` del panel). Las llegadas por ciudadanía a España del INE (EVR) solo existen desde 2008 en data/raw (semestrales), por lo que no se usan para la cuota de 2002.
