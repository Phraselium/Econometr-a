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
- F3 cerrada: correcciones aplicadas (Y6, Y7 en decisiones.md); puerta `make check` rc=0 (168 passed; check_texto, check_v5 y check_v6 con 0 errores).
- F4: M2 (SVAR con restricciones de signo) en curso con un subagente.

## Siguiente paso exacto
- Lanzar F4, primera tanda junto a M2: M3 (LP dependiente del periodo, Y6), M0 y M4 (periodos y largo plazo), M6 y M7 (colinealidad y multiverso).
- Segunda tanda: M1 y M8 (factor común y regional), M5 (LP-IV) y M9 (ML). Siguiendo docs/v8/contrato_salidas.md.

## Tokens por módulo

| Módulo | Subagentes | Orquestador (estimación) |
|---|---|---|
| F0 | 0 | ~40k |
| F1 descarga | 121.258 | ~15k |
| F1 paneles | 214.088 | ~10k |
| F2 | 0 | ~25k |
| F3 herramientas | 384.763 | ~20k |
| F3 revisor | 163.223 | ~10k |
| F3 correcciones (VAR) | 226.757 | ~5k |
| F3 correcciones (resto) | 254.317 | ~5k |
