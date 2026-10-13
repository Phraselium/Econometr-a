# Plan V8: por qué ha subido (factores, periodos y factor común)

Rama r8/main, creada desde r7.2/main. La v7.1 es la versión de referencia; las correcciones de la v7.2 van con ERRATA. V8 es la última versión de modelización.

## Orden y puertas

| Fase | Contenido | Puerta |
|---|---|---|
| F0 | Correcciones pendientes (casi todas hechas en v7.2; aquí el marcador de fecha y el cierre de los clones de v7.2) | `make check` |
| F1 | Datos: nacional trimestral 1995T1-2026T2, panel de 17 CCAA ampliado, Comunitat Valenciana por provincias y València ciudad; diccionario | `make check` |
| F2 | Pre-registro: docs/v8/hipotesis.md, etiqueta `prereg-v8`, notas de la release, `make evaluate_v8` | commit antes de cualquier estimación real |
| F3 | Herramientas validadas por Monte Carlo: BVAR-GLP, signos y ceros (ARW), TVP-VAR-SV o regímenes, MS, umbral, DFM, LP y LP-IV, dominancia, permutación de fechas, SHAP agrupado | revisor (opus) + `make check` |
| F4 | Modelos M0-M9 | revisor (opus) + `make check` |
| F5 | Atribución y factor más relevante | `make check` |
| F6 | Entregables, verificador, cifras_clave, cierre_proyecto, `make v8` en clon limpio | revisor final (opus) + `make check` |

## Topes de trabajo

- Multiverso: como máximo 50.000 especificaciones.
- SVAR: como máximo 3 variantes de identificación además de la principal.
- Como máximo 2 REHACER por puerta.
- Ningún módulo fuera del encargo; las ideas nuevas van a docs/v8/ideas_futuras.md.

## Subagentes

- Haiku: tareas mecánicas.
- Sonnet: código (datos, herramientas, módulos).
- Síntesis, decisiones y coherencia: el orquestador.
- Cada subagente devuelve rutas, un resumen de 200 palabras como máximo y resultado.json.
