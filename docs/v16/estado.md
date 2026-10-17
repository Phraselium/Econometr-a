# V16 · Estado

Plan: docs/v16/plan.md (íntegro). Pre-registros internos sin sello de tiempo externo. La versión 1.0 no cambia de valor. V16 añade cifras V16-* y se publicará como 2.0.

## Hecho
- **Plan.** Guardado íntegro (7615269) y aviso en CLAUDE.md.
- **B1 · Guardas** (decisiones K1).
  - La guarda (d) exige prereg-v15 en el remoto en 542b4fd.
  - La guarda nueva (f) exige prereg-v16 en el remoto para las fases 5 a 7 y el objetivo v16.
  - check_v16 controla que las estimaciones no sean anteriores a su etiqueta.
  - Tests: tests/v16/test_guardas.py (26).
  - Pruebas en vivo: el hook bloqueó las fases 6 y completa de V16 y la fase 4 de V15; los lanzadores de fase llamados sin make terminan con código 1.
- **B2 · Subagentes nuevos.** adquisidor-datos, ingeniero-datos, replicador-ciego, abogado-del-diablo, redactor y verificador-cifras (K2).
- **B3 · Comandos y make.**
  - Comandos /v16-fase0 … /v16-fase7 y /v16-estado.
  - Objetivos make v16_f0 … v16_f7, v16 y check_v16, este último dentro de make check.
  - src/v16/fase.py y src/v16/registro_subagentes.py (tokens por fase y aviso de 6 millones).
- **Bloqueo B-1.** El remoto rechaza las etiquetas (HTTP 403). Los comandos para publicarlas están en tareas_autor.

## Siguiente
- Fase 0: proyecto.json (preregistro_tipo), comprobación de las correcciones previas, plantilla de una página y lo_ya_visto.md.
