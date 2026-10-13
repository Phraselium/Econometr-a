# Decisiones V8.1

## Z0 — Alcance y entorno (2026-10-13)
- V8.1 no estima modelos ni abre muestras selladas: solo redacción, tablas, capa de consulta, retirada de datos de terceros y publicación.
- El encargo dice «en local con `gh` autenticado», pero esta sesión corre en un contenedor en la nube: `gh auth status` informa de que el token GH_TOKEN no es válido, y el remoto rechaza el push de etiquetas. Los bloques A-D se hacen aquí; el bloque E se prepara (comandos exactos en docs/v8_1/publicacion_github.md) y cada acción irreversible se consulta al autor antes de ejecutarla, si el entorno lo permite.

## Z1 — Bloque A: lectura por variables y avisos (2026-10-13)
- La regla del multiverso (§9) se lee por familias (2 de 74 combinaciones, pre-registrada) y, como lectura descriptiva adicional C4, por variables (`cumple_multiverso` de resumen_multiverso.csv, filas con variable distinta de TODAS). La segunda no sustituye a la primera ni cambia ninguna designación de F5.
- Los hechos nuevos se calculan en src/v8/f6_hechos.py desde output/v8/ (M0, M6, M7) y, para la correlación de la población total y la extranjera, desde data/processed/v8/nacional_q_v8.csv (diagnóstico descriptivo, no un modelo).
- `make publicacion` ejecuta antes render v5 y render v8, porque `make v8` no regenera una_pagina ni lo_que_sabemos.

## Z2 — Datos de terceros (2026-10-13)
- Se retiran del índice 75 ficheros sin redistribución claramente permitida o sin licencia que conste (Notariado, Registradores, AEAT, CGPJ, Interior, programas de partidos, Comunidad de Madrid, Registre de Turisme de Catalunya, shocks de Jarociński-Karadi). Siguen en disco, en .gitignore y con su sha256 en data/CHECKSUMS.sha256. `make datos_terceros` los descarga y verifica; en un clon limpio va antes de `make all`.
- `data/raw/v4/medidas_programas.csv` (citas breves transcritas, sin script) sigue versionado a la espera de que el autor confirme si es admisible.
- No se reescribe el historial: los ficheros siguen en las ramas y commits anteriores.

## Z3 — Publicación en GitHub (2026-10-13)
- El bloque E no se puede ejecutar desde este contenedor: `gh` no está autenticado y el remoto rechaza las etiquetas. Queda un guion con confirmación en cada paso (docs/v8_1/publicacion_github.sh) para ejecutarlo en local. Los commits a etiquetar (3fad305, 3d1170c, 7415932, 91e618b y 5c68973) ya están en el remoto.
