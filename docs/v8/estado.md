# Estado V8

## Hecho
- Rama r8/main desde r7.2/main (e7bf435).
- F0: la mayor parte ya está en v7.2:
  - cifras superadas retiradas;
  - una sola cifra de déficit con bajas;
  - construcción adicional con dosis no nula;
  - ficha de burbuja nacional y regional;
  - test de cifras superadas sobre cifras_clave.
- F0, en esta versión: el marcador «[fecha de publicación: pendiente]» se rotula como pendiente del autor (las etiquetas no se pueden publicar desde el entorno).

## Hecho (continuación)
- **F1.** Paneles en data/processed/v8:
  - nacional_q_v8: 1995T1-2026T2, 251 columnas;
  - panel_ccaa_q_v8;
  - cv_prov_q_v8 y cv_prov_a_v8;
  - valencia_ciudad_v8.
  
  Diccionario en docs/v8/diccionario.md y tests en tests/v8/test_f1_paneles.py. `make v8` arranca con f1_paneles.
- **F2.** Pre-registro docs/v8/hipotesis.md, cerrado con la etiqueta local `prereg-v8` (91e618b). El push de la etiqueta falla (el remoto rechaza etiquetas): queda como tarea del autor (docs/v8/notas_release.md).

## En curso
- F0: clones limpios de v7.2.
- F3: dos subagentes con Monte Carlo (familia VAR y resto).

## Siguiente paso exacto
- Cuando terminen los subagentes de F3:
  1. revisar las aptitudes;
  2. hacer commit;
  3. lanzar el revisor de F3 (opus);
  4. `make check`;
  5. empezar F4 con M0 y M1.

## Tokens por módulo

| Módulo | Subagentes | Orquestador (estimación) |
|---|---|---|
| F0 | 0 | ~40k |
| F1 descarga | 121.258 | ~15k |
| F1 paneles | 214.088 | ~10k |
| F2 | 0 | ~25k |
