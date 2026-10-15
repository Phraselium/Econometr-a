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
- B7: vivienda turística CV y València (INE frente a registro GVA, móviles, asociaciones), Cataluña y Barcelona
  (output/v12/b7).

## Siguiente (para `claude --continue`)
- B8: incorporar V12 a la base (`make base`), figuras (`make figuras`), tres páginas web nuevas («De dónde viene la
  población», «Quién es propietario», «Dónde se construye»), fichas ampliadas, verificador con V12-V02 (sustituye a
  V02), `make web`; publicacion/atlas_v12.md, actualizar por_que_ha_subido, lo_que_sabemos e historial_conclusiones;
  publicacion/tablas_v12.xlsx; revisor final (opus, tope 100k); cierre en clon limpio.

## Tokens de subagentes
Ninguno hasta el revisor final.
