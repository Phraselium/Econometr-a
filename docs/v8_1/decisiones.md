# Decisiones V8.1

## Z0 — Alcance y entorno (2026-10-13)
- V8.1 no estima modelos ni abre muestras selladas: solo redacción, tablas, capa de consulta, retirada de datos de terceros y publicación.
- El encargo dice «en local con `gh` autenticado», pero esta sesión corre en un contenedor en la nube: `gh auth status` informa de que el token GH_TOKEN no es válido, y el remoto rechaza el push de etiquetas. Los bloques A-D se hacen aquí; el bloque E se prepara (comandos exactos en docs/v8_1/publicacion_github.md) y cada acción irreversible se consulta al autor antes de ejecutarla, si el entorno lo permite.

## Z1 — Bloque A: lectura por variables y avisos (2026-10-13)
- La regla del multiverso (§9) se lee por familias (2 de 74 combinaciones, pre-registrada) y, como lectura descriptiva adicional C4, por variables (`cumple_multiverso` de resumen_multiverso.csv, filas con variable distinta de TODAS). La segunda no sustituye a la primera ni cambia ninguna designación de F5.
- Los hechos nuevos se calculan en src/v8/f6_hechos.py desde output/v8/ (M0, M6, M7) y, para la correlación de la población total y la extranjera, desde data/processed/v8/nacional_q_v8.csv (diagnóstico descriptivo, no un modelo).
- `make publicacion` ejecuta antes render v5 y render v8, porque `make v8` no regenera una_pagina ni lo_que_sabemos.

## Z2 — Datos de terceros (2026-10-13)
- Se retiran del índice 75 ficheros (76 con medidas_programas.csv, segunda ronda) sin redistribución claramente permitida o sin licencia que conste (Notariado, Registradores, AEAT, CGPJ, Interior, programas de partidos, Comunidad de Madrid, Registre de Turisme de Catalunya, shocks de Jarociński-Karadi). Siguen en disco, en .gitignore y con su sha256 en data/CHECKSUMS.sha256. `make datos_terceros` los descarga y verifica; en un clon limpio va antes de `make all`.
- `data/raw/v4/medidas_programas.csv` (citas breves transcritas, sin script) también se retira, por decisión del autor: «aplazado a la fase de propuestas; incluye copias no oficiales». Total: 76 ficheros.
- No se reescribe el historial: los ficheros siguen en las ramas y commits anteriores.

## Z3 — Publicación en GitHub (2026-10-13)
- El bloque E no se puede ejecutar desde este contenedor: `gh` no está autenticado y el remoto rechaza las etiquetas. Queda un guion con confirmación en cada paso (docs/v8_1/publicacion_github.sh) para ejecutarlo en local. Los commits a etiquetar (3fad305, 3d1170c, 7415932, 91e618b y 5c68973) ya están en el remoto.

## Z4 — Incidente (2026-10-14)
- Al redactar la retirada de medidas_programas.csv, un heredoc sin comillas ejecutó los comandos entre acentos graves del texto, entre ellos `make all`. Se detuvo en el primer módulo (src/f2_nacional.py) a los pocos segundos. Las descargas pasaron por la caché y data/raw quedó idéntico (todas las entradas de data/CHECKSUMS.sha256 coinciden). output/ no cambió, y el único fichero versionado modificado (docs/v2/fallidas/ine.md, una marca de tiempo) se restauró. Sin efecto en ninguna cifra.

## Z5 — Respuestas del autor (2026-10-14)
- **medidas_programas.csv:** se retira (Z2); total de ficheros retirados, 76.
- **Nombre del repositorio:** `vivienda-espana-evidencia`. Desde aquí no se puede renombrar. README, LEEME_PRIMERO, CITATION.cff, .zenodo.json, README_REPLICACION, los enlaces de las plantillas v5, consulta/ y llms.txt ya usan el nombre nuevo (GitHub redirige el antiguo).
- **Guion en dos fases** (docs/v8_1/publicacion_github.sh; guía en docs/v8_1/INSTRUCCIONES_PUBLICACION.md):
  - Fase 1, con Zenodo desactivado: renombrar, crear main y ponerla por defecto, publicar las etiquetas y crear las releases antiguas (prereg-v7, v7.0, prereg-v8 y v8.0).
  - Pausa para activar Zenodo.
  - Fase 2: release v8.1 (latest), búsqueda del DOI y escritura de fechas y DOI.
  - Al inicio comprueba que el clon no es superficial y que los commits existen y están en el remoto. Pide confirmación [s/N] en cada paso irreversible.
- **fecha_verificable de cada pre-registro:** el published_at de su release en GitHub (prereg-v7, prereg-v8), que es una marca externa anterior a cualquier dato evaluable. El DOI de v8.1 se anota aparte. consulta/version.json lee ambos de docs/v8/notas_release.md (`fecha_verificable:` y `doi:`).
