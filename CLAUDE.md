# Vivienda España — V8.1 coherencia, consulta y publicación de V8 (por qué ha subido). V1-V8 cerradas; v8 referencia (v7.2 anterior); trabajo en docs/v8_1, src/v8, output/v8

- Idioma: español. `make all` reproducible SIN red; SEED=20261010 en todo lo aleatorio.
- Al empezar: leer docs/v8/estado.md, docs/v8/plan.md, docs/v8/decisiones.md, docs/v7_1/decisiones.md y docs/estado_proyecto/informe_estado.md (inventario v1-v6.2).
- Capas v3: C1 HECHOS (≥2 fuentes) · C2 COTAS (Manski, supuestos explícitos) · C3 EFECTOS (pretendencias, placebos, sensibilidad, sellado) · C4 EXPLORATORIO. Nunca promover de capa.
- Neutralidad: veredicto sobre la afirmación, nunca sobre quién la dice; se evalúan afirmaciones e instrumentos, nunca partidos ni personas; sin lenguaje valorativo ni partidista. `make check` en cada puerta.
- Tras cada tarea: actualizar docs/v8/estado.md (hecho / siguiente / tokens de subagentes).
- Decisiones → docs/v8/decisiones.md; bloqueos reales → docs/v8/bloqueos.md; fuentes inaccesibles → docs/v6/fuentes_fallidas.md (endpoint, edición y fecha verificados).
- Subagentes devuelven: rutas + resumen ≤200 palabras + output/v6/<módulo>/resultado.json. Nunca datos crudos.
- resultado.json: {rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra{modelo, rmse, dm_vs_ar4}, notas}.
- data/raw: solo lectura. data/sealed: SOLO vía src/holdout.py (registra cada acceso; una evaluación por hipótesis confirmatoria).
- Ficheros >50 MB: LFS o .gitignore con checksum en data/CHECKSUMS.sha256.
- Toda especificación probada va al Registry de src/econ_utils.py; control de falsos descubrimientos (Holm o BH).
- Comparar siempre en la MISMA muestra contra AR(4) y ECM v1; validación temporal en bloques con embargo.
- Escala de evidencia: CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Sin lenguaje causal por debajo de CAUSAL.
- Referencias: VERIFICADA (DOI Crossref + cuartil Scimago) o NO VERIFICADA / «cuartil no verificado».
- Ramas: worktree ../wt-<rama> (r6/<rama>, data/ enlazada; máx. 3); src/econ_utils.py y data/ son solo lectura para las ramas.
- Interpolaciones y fuentes no validadas se marcan y solo entran en robustez; si dos métodos discrepan, se reportan ambos.
- Push solo a la rama remota designada (claude/housing-price-spain-econometric-95dhj3).
- v5: toda cifra de entregables sale de output/v5/cifras_clave.csv (con fecha del dato); ningún script lee ficheros no versionados; nada no oficial en recuentos; suma provincial = nacional.
- Autor: Borja Romero, economista (firma individual, independiente). Resúmenes también en inglés en working paper y artículos.
- v5.1: las viviendas liberadas por envejecimiento NUNCA se restan de la necesidad (la proyección de hogares del INE ya las descuenta); `make check` lo comprueba.
- v6: validación sellada NUEVA (src/holdout.py: sellar_v6, evaluate_v6; último año + 11 provincias por bloques de CCAA); predicción ≠ causalidad: nada causal desde SHAP o importancias; cada resultado de compra declara su medida de precio.
- v6.1: un modelo solo «predice mejor» si supera a la línea base más exigente (K1); todo error que cambie una cifra publicada va a ERRATA.md.
- v6.2: cada cifra publicable tiene ficha en output/v6_2/anexo_metodologico.md, reconstruible solo con el anexo y data/raw (test en tests/doble_impl).
- V7: cruces territoriales SOLO por código INE; herramientas de panel (MG/PMG/DFE/CS-ARDL/Westerlund/Pedroni/CIPS) validadas por Monte Carlo antes de usarse; paneles de CCAA ya vistos en v1 (backtests «informativos»); validación limpia solo diferida (`make evaluate_v7`).
- V7.1: sin análisis nuevo; publicacion/ solo se genera con `make publicacion` (nunca a mano); toda cifra difundible sale de cifras_clave y de una versión vigente.

- V8: capas C1, C2, C3 (instrumento externo o diseño que supera pruebas), C3s (restricciones de signo explícitas), C4; causalidad solo en C3/C3s; ningún modelo elegido por p-valor; atribuciones siempre con bandas; multiverso ≤50.000; fuera de alcance: programas electorales y divulgación.