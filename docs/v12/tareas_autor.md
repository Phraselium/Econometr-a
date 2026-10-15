# V12 · Tareas del autor

1. **Padrón por barrio con nacionalidad (Ajuntament de València):** no está en data/raw; B1 usa el censo anual por
   sección. Si se descarga a mano (data/manual/v11/), la variación 2021-2025 por barrio sería comparable en los 87
   barrios (hoy solo en 37, por los cambios de seccionado).
2. **`make datos_terceros` reescribe tres ficheros versionados** (data/raw/_manifest.csv, data/raw/v9/incasol/_manifest.csv
   y docs/v5/programas/inventario.csv: fechas de descarga y filas de v4). Es previo a V12; decidir si esos ficheros deben
   versionarse o regenerarse sin fecha.
3. **Revisar el umbral de C1 de la oferta provincial** (10 %: 10 provincias) y, si se prefiere, fijarlo en el
   pre-registro de la siguiente versión.
4. **Publicar la web** (web/_site, GitHub Pages) con las tres páginas nuevas y la ficha V12-V02 del verificador.
5. **Valores de referencia del Catastro y AEAT 2013-2015:** unidades de los rendimientos del capital inmobiliario por
   verificar antes de usarlos como cifra.
