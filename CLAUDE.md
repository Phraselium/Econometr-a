# Vivienda España — v3 (V1 y V2 cerradas: no rehacer; v3 en docs/v3, src/v3, output/v3)

- Idioma: español. `make all` reproducible SIN red; SEED=20261010 en todo lo aleatorio.
- Al empezar: leer docs/v3/estado.md, docs/v3/plan.md, docs/v3/hipotesis.md y docs/v2/limitaciones.md.
- Capas v3: C1 HECHOS (≥2 fuentes) · C2 COTAS (Manski, supuestos explícitos) · C3 EFECTOS (pretendencias, placebos, sensibilidad, sellado) · C4 EXPLORATORIO. Nunca promover de capa.
- Neutralidad: veredicto sobre la afirmación, nunca sobre quién la dice; sin lenguaje valorativo ni partidista. `make check` en cada puerta.
- Tras cada tarea: actualizar docs/v3/estado.md (hecho / siguiente / tokens de subagentes).
- Decisiones → docs/v3/decisiones.md; bloqueos reales → docs/v3/bloqueos.md; fuentes inaccesibles → docs/v3/fuentes_fallidas.md.
- Subagentes devuelven: rutas + resumen ≤200 palabras + output/v3/<diseño>/resultado.json. Nunca datos crudos.
- resultado.json: {rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra{modelo, rmse, dm_vs_ar4}, notas}.
- data/raw: solo lectura. data/sealed: SOLO vía src/holdout.py (registra cada acceso; una evaluación por hipótesis confirmatoria).
- Ficheros >50 MB: LFS o .gitignore con checksum en data/CHECKSUMS.sha256.
- Toda especificación probada va al Registry de src/econ_utils.py; control de falsos descubrimientos (Holm o BH).
- Comparar siempre en la MISMA muestra contra AR(4) y ECM v1; validación temporal en bloques con embargo.
- Escala de evidencia: CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Sin lenguaje causal por debajo de CAUSAL.
- Referencias: VERIFICADA (DOI Crossref + cuartil Scimago) o NO VERIFICADA / «cuartil no verificado».
- Ramas: worktree ../wt-<rama> (r3/<rama>, data/ enlazada; máx. 3); src/econ_utils.py y data/ son solo lectura para las ramas.
- Interpolaciones y fuentes no validadas se marcan y solo entran en robustez; si dos métodos discrepan, se reportan ambos.
- Push solo a la rama remota designada (claude/housing-price-spain-econometric-95dhj3).
