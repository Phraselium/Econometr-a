# V12 · Estado

## Hecho
- F0: guardia de git limpio en `make check`; empalme de titularidad documentado; declarantes aproximados de la AEAT
  (output/v12/f0).
- B1: contabilidad demográfica por municipio (≥ 10.000 hab.), provincia, CCAA y España, 2003-2024, por nacionalidad;
  València por sección, barrio y distrito 2021-2025 (output/v12/b1; decisiones B1).
- B2: flujos OD capital ↔ corona ↔ resto en València (PATEVAL), Madrid, Barcelona, Alicante y Castellón 2003-2024 por
  edad y nacionalidad; destinos 2022-2024; saldos interiores por edad × nacionalidad; asociación (Spearman, Holm)
  con alquiler SERPAVI y valor tasado MIVAU; alquiler en destino de quienes salen de las capitales (output/v12/b2).
- B3: jefatura por edad (Censos 2011 y 2021, microdatos), descomposición 2011-2021 en dos órdenes, 2021-2026 con ECP,
  hogares por nacionalidad con IC95 y supresión de celdas (output/v12/b3). Corregido VARANOE del extracto V11.
- B4: obra nueva neta del Catastro, contraste con MIVAU (libre + protegida), INSPIRE, presión obra/hogares por
  municipio (2011-2021 y 2021-2025) y provincia (output/v12/b4).
- B5: cuotas de titularidad 2024-2026 en cuatro ámbitos, tipo fino, ranking, asociaciones (Holm), titulares
  2012-2023, AEAT CV y ficha V12-V02 que sustituye a V02 (output/v12/b5).
- B6: condiciones por origen con ECV 2018-2025 (anual, cruces, brecha a igual edad y renta) y Censo 2021 (llegada,
  edad, tipo de hogar), con IC y supresión de celdas (output/v12/b6).
- B8 (parcial): base con variables v12_*, figuras F15-F23, 54 cifras V12 en cifras_clave, atlas_v12.md, tablas_v12.xlsx,
  lo_que_sabemos / por_que_ha_subido / historial_conclusiones actualizados, tres páginas web y verificador (V12-V02).
- B7: vivienda turística CV y València (INE frente a registro GVA, móviles, asociaciones), Cataluña y Barcelona
  (output/v12/b7).

- Revisor final (opus, ~82.000 tokens, dentro del tope): REHACER con 12 hallazgos; todos corregidos (decisiones,
  «Revisión final»).

## Siguiente (para `claude --continue`)
- Cierre en clon limpio: `make datos_terceros`, `make v12`, `make base`, `make figuras`, `make web`, `make check` (sin
  cambios en git); commit y push.

## Tokens de subagentes
Revisor final V12: ~82.000 tokens (tope 100.000).
