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
- F0: `make all` de v7.2 en su clon (`make v7` ya cerrado: coincide salvo el recuento de especificaciones, copiado).
- F3: revisión hecha, APROBAR CON CORRECCIONES (docs/v8/revision_F3.md); desviaciones y aclaraciones en docs/v8/desviaciones.md. Dos subagentes corrigen el código: familia VAR (H1, H2, H4, H9, H10, H12) y resto (H5-H8, H13-H15, H17, H18).

## Siguiente paso exacto
- Al terminar las correcciones de F3:
  1. comprobar las cifras;
  2. decidir entre la principal y V3 si la aceptación de 7 variables es inviable;
  3. hacer commit;
  4. `make check`.
- Después, empezar F4. Primera tanda: M2 y M3 (SVAR y regímenes), M0 y M4 (periodos y largo plazo), M6 y M7 (colinealidad y multiverso). Segunda tanda: M1 y M8 (factor común y regional), M5 (LP-IV) y M9 (ML). Siguiendo docs/v8/contrato_salidas.md.

## Tokens por módulo

| Módulo | Subagentes | Orquestador (estimación) |
|---|---|---|
| F0 | 0 | ~40k |
| F1 descarga | 121.258 | ~15k |
| F1 paneles | 214.088 | ~10k |
| F2 | 0 | ~25k |
| F3 herramientas | 384.763 | ~20k |
| F3 revisor | 163.223 | ~10k |
