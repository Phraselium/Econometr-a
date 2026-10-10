# Vivienda España — v4 (V1-V3 cerradas: no rehacer; v4 en docs/v4, src/v4, output/v4)

- Idioma: español. `make all` reproducible SIN red; SEED=20261010 en todo lo aleatorio.
- Al empezar: leer docs/v4/estado.md, docs/v4/plan.md, docs/v3/limitaciones.md y docs/v4/decisiones.md.
- Capas v3: C1 HECHOS (≥2 fuentes) · C2 COTAS (Manski, supuestos explícitos) · C3 EFECTOS (pretendencias, placebos, sensibilidad, sellado) · C4 EXPLORATORIO. Nunca promover de capa.
- Neutralidad: veredicto sobre la afirmación, nunca sobre quién la dice; se evalúan instrumentos, no partidos; sin lenguaje valorativo ni partidista. `make check` en cada puerta.
- Tras cada tarea: actualizar docs/v4/estado.md (hecho / siguiente / tokens de subagentes).
- Decisiones → docs/v4/decisiones.md; bloqueos reales → docs/v4/bloqueos.md; fuentes inaccesibles → docs/v4/fuentes_fallidas.md.
- Subagentes devuelven: rutas + resumen ≤200 palabras + output/v4/<módulo>/resultado.json. Nunca datos crudos.
- resultado.json: {rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra{modelo, rmse, dm_vs_ar4}, notas}.
- data/raw: solo lectura. data/sealed: SOLO vía src/holdout.py (registra cada acceso; una evaluación por hipótesis confirmatoria).
- Ficheros >50 MB: LFS o .gitignore con checksum en data/CHECKSUMS.sha256.
- Toda especificación probada va al Registry de src/econ_utils.py; control de falsos descubrimientos (Holm o BH).
- Comparar siempre en la MISMA muestra contra AR(4) y ECM v1; validación temporal en bloques con embargo.
- Escala de evidencia: CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Sin lenguaje causal por debajo de CAUSAL.
- Referencias: VERIFICADA (DOI Crossref + cuartil Scimago) o NO VERIFICADA / «cuartil no verificado».
- Ramas: worktree ../wt-<rama> (r4/<rama>, data/ enlazada; máx. 3); src/econ_utils.py y data/ son solo lectura para las ramas.
- Interpolaciones y fuentes no validadas se marcan y solo entran en robustez; si dos métodos discrepan, se reportan ambos.
- Push solo a la rama remota designada (claude/housing-price-spain-econometric-95dhj3).
