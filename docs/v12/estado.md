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

## Siguiente (para `claude --continue`)
- B5: `src/v12/b5_propiedad.py`: cuotas de viviendas de titulares con > 5 y > 10 inmuebles y de personas jurídicas
  (2024-2026, municipio = cota inferior; ficheros nacional/CCAA/provincia), ranking, relación descriptiva (C4) con
  alquiler, precio, VUT, llegada de población y renta; 2012-2023 titulares frente a viviendas; AEAT; ficha del
  verificador sobre fondos y grandes tenedores → «analizada».

## Tokens de subagentes
Ninguno hasta el revisor final.
