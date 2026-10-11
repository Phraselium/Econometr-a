# archive/: salidas superadas

Contiene salidas de versiones anteriores que ya no son vigentes y que **ningún script, regla del Makefile, test ni plantilla de v5 lee ni escribe**. Se movieron con `git mv`, así que `git log --follow <fichero>` muestra su historia completa. No se han modificado: lo publicado no se reescribe (las correcciones van en ERRATA.md).

Criterio de traslado: grep de la ruta y del nombre del fichero en src/, tests/, Makefile y docs/v5/plantillas sin ninguna coincidencia. Los enlaces internos de estos documentos apuntan a sus rutas originales; la ruta nueva es la misma con el prefijo `archive/`.

| Fecha | Ruta original | Ruta nueva | Superado por | Motivo |
|---|---|---|---|---|
| 2026-10-11 | output/v3/articulo.md | archive/output/v3/articulo.md | output/v5/working_paper.md | Síntesis de v3 redactada a mano; sin lectores en el código |
| 2026-10-11 | output/v3/informe_politica.md | archive/output/v3/informe_politica.md | output/v5/policy_brief.md | Síntesis de v3 redactada a mano; sin lectores en el código |
| 2026-10-11 | output/v3/lo_que_sabemos.md | archive/output/v3/lo_que_sabemos.md | output/v5/lo_que_sabemos.md | Síntesis de v3 redactada a mano; sin lectores en el código |
| 2026-10-11 | output/v4/policy_brief.md | archive/output/v4/policy_brief.md | output/v5/policy_brief.md | Síntesis de v4 redactada a mano; sin lectores en el código |
| 2026-10-11 | output/v4/working_paper.md | archive/output/v4/working_paper.md | output/v5/working_paper.md | Síntesis de v4 redactada a mano; sin lectores en el código |

**No trasladados** (se citan por ruta en docs/v5/plantillas): output/v4/informe_tecnico.md y output/v4/lo_que_sabemos.md.

Efecto en `make check`: `src/v3/check_texto.py` recorre output/v3 y output/v4 con rglob; los ficheros trasladados quedan fuera de ese control. En la ubicación original queda un README.md con enlaces a la nueva ruta.
