# Vivienda España — v2 (F1-F7 aprobadas; v1 en output/informe.md)

- Idioma: español. `make all` reproducible SIN red; SEED=20261010 en todo lo aleatorio.
- Al empezar: leer docs/v2/estado.md, docs/v2/plan.md y docs/limitaciones.md (+ docs/v2/limitaciones.md).
- Tras cada tarea: actualizar docs/v2/estado.md (hecho / siguiente / tokens de subagentes).
- Decisiones → docs/v2/decisiones.md; bloqueos reales → docs/v2/bloqueos.md; fuentes inaccesibles → docs/v2/fuentes_fallidas.md.
- Subagentes devuelven: rutas + resumen ≤200 palabras + output/v2/<rama>/resultado.json. Nunca datos crudos.
- resultado.json: {rama, pregunta, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra{modelo, rmse, dm_vs_ar4}, notas}.
- data/raw: solo lectura. data/sealed: SOLO vía src/holdout.py (registra cada acceso; una evaluación por hipótesis confirmatoria).
- Ficheros >50 MB: LFS o .gitignore con checksum en data/CHECKSUMS.sha256.
- Toda especificación probada va al Registry de src/econ_utils.py; control de falsos descubrimientos (Holm o BH).
- Comparar siempre en la MISMA muestra contra AR(4) y ECM v1; validación temporal en bloques con embargo.
- Escala de evidencia: CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Sin lenguaje causal por debajo de CAUSAL.
- Referencias: VERIFICADA (DOI Crossref + cuartil Scimago) o NO VERIFICADA / «cuartil no verificado».
- Ramas: worktree ../wt-<rama> (r2/<rama>); src/econ_utils.py y data/ son solo lectura para las ramas.
- Interpolaciones y fuentes no validadas se marcan y solo entran en robustez; si dos métodos discrepan, se reportan ambos.
- Push solo a la rama remota designada (claude/housing-price-spain-econometric-95dhj3).
