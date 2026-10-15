# V12 · Estado

## Hecho
- F0: guardia de git limpio en `make check`; empalme de titularidad documentado; declarantes aproximados de la AEAT
  (output/v12/f0).
- B1: contabilidad demográfica por municipio (≥ 10.000 hab.), provincia, CCAA y España, 2003-2024, por nacionalidad;
  València por sección, barrio y distrito 2021-2025 (output/v12/b1; decisiones B1).
- B2: flujos OD capital ↔ corona ↔ resto en València (PATEVAL), Madrid, Barcelona, Alicante y Castellón 2003-2024 por
  edad y nacionalidad; destinos 2022-2024; saldos interiores por edad × nacionalidad; asociación (Spearman, Holm)
  con alquiler SERPAVI y valor tasado MIVAU; alquiler en destino de quienes salen de las capitales (output/v12/b2).

## Siguiente (para `claude --continue`)
- B3: corregir `VARANOE` en src/v11/fetch_ine_censo2021.py (tramos 0001-0005 + años 2016-2021) y regenerar el extracto;
  `src/v12/b3_hogares.py`: tasas de jefatura por edad con microdatos del Censo 2011
  (ine.es/ftp/microdatos/censopv/cen11/Microdatos_personas_nacional.zip) y 2021; descomposición del crecimiento de
  hogares (población, estructura de edad, jefatura) por provincia y municipio; índice hogares nuevos / obra nueva;
  hogares por nacionalidad con intervalos (≥ 10 casos, error relativo ≤ 30 %).

## Tokens de subagentes
Ninguno hasta el revisor final.
