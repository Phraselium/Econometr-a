# Estado v6.2

## Hecho
- Preparación: rama r6.2/main y docs/v6_2.
- L3 terminado (55.691 tokens).
  - Déficit 2021-2024 sin bajas: 344.803-710.542 viviendas, C2; con bajas, hasta 924.658.
  - Entregables, D3, verificador (L3-V1), ERRATA, carta de respuesta e historial actualizados.
  - l3_deficit y l3_ficha entran en make.

- L1 terminado (223.573 tokens, por encima del tope de 200.000).
  - Anexo con 17 fichas completas: 12 de las 15 se reconstruyen solo con anexo y data/raw y 3 necesitan tabla intermedia versionada; ninguna queda sin reconstruir. Más las 49 fichas breves.
  - Hallazgo corregido: la grafía «Valéncia» dejaba a Valencia sin cruce. A23-A10 pasa a 28,5 % (26,1-30,8); va a ERRATA.
  - Corregida la referencia de tabla en revision_humana.
- Acumulado: 279.264 tokens (47 %).

- L4 hecho por el orquestador.
  - Asociación total frente a directa en el informe §12, el working paper §6.1, lo que sabemos, el policy brief, la ficha K2-V1 y el historial.
  - Unidad corta «% por pp».
  - Los rangos con mínimo negativo usan « a ».
  - Los rangos del déficit se dan en una sola marca.
- Anexo enlazado desde el README, el informe y el working paper.
- L5 hecho (orquestador): docs/v6_2/cifras_publicables.md generado desde cifras_clave (9 cifras aptas y 13 que no deben citarse fuera de contexto) y tests/test_l5_cifras.py (cifras superadas, ids históricos y publicables al día). l1_verifica y l5_publicables entran en make.
- L2 terminado (129.888 tokens): 15 de 15 cifras reproducidas a ciegas. 11 precisiones incorporadas al anexo. tests/doble_impl entra en `make check` (17 tests, unos 17 s).
- Acumulado: 409.152 tokens (68 %). Revisor tras L3 (53.728 tokens): REHACER, aplicado por el orquestador (E7).
  - Déficit 2021-2024 C2: 389.361-710.542 (sensibilidad 596.371-710.542); con bajas estimadas, 389.361-765.994 (C4).
  - Acumulado de subagentes: 462.880 tokens (77 %).
- L6 hecho (orquestador): docs/v6_2/guia_revisor.md, docs/v6_2/tareas_autor.md (sustituye al de v6.1), versión 6.2 en CITATION, Zenodo y README, CHANGELOG v6.2.

## Siguiente
- L1 (general-purpose) y L3 (econometrician) en curso.

## Tokens de subagentes (presupuesto 0,6 M; corte 0,48 M)

## Cierre v6.2
- `make check`: 89 tests, más check_texto, check_v5 y check_v6, todo con 0 errores.
- `make all` ×2 sin red en un clon limpio de d585b1e: 7.928 s y 8.054 s, con md5 idénticos salvo tiempos.json. Diferencias frente a lo versionado explicadas en E8.
- Tokens de subagentes, total 462.880 de 600.000 (77 %):

  | Módulo | Tokens |
  |---|---|
  | L1 | 223.573 |
  | L2 | 129.888 |
  | L3 | 55.691 |
  | Revisor | 53.728 |

  L4, L5, L6 y la ronda REHACER las hizo el orquestador.
- La etiqueta local v6.2 apunta al commit de cierre. El remoto rechaza las etiquetas (HTTP 403); ver tareas_autor §1.
