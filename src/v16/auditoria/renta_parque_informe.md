# Auditoría de datos V16 · renta_parque (capa C4, descriptivo)

Script: `src/v16/auditoria/renta_parque.py` (SEED=20261010). Filtro: `muestra_sellada_v6 == False` y exclusión de unidades con `holdout.unidad_sellada_v16` verdadero (1.297.894 de 2.433.670 filas del versionado). Sin estimación de efectos.

## 1. ADRH de la API frente a la base (sección, 2019-2023)
- La base no trae 2021 (2019, 2020, 2022, 2023); la API sí (17.463 secciones con renta por persona): el parquet nuevo cubre ese hueco.
- En el solape (68.484 pares sección-año de renta por persona; igual en hogar; 65.948 en Gini) los valores coinciden salvo redondeo: la base está redondeada a euros enteros (diferencia máxima 0,5; 99,5 % coincide al redondear la API a 0 decimales) y el Gini de la base a un decimal (diferencia máxima 0,05; 10,4 % idéntico a 2 decimales). La diferencia media con signo es 0,005 euros: sin sesgo y sin revisiones del INE apreciables. No hay segundo vintage.
- Cobertura distinta: 14 pares solo en la base y 213 solo en la API en 2019-2020 (renta por persona).
- Marcado: la base declara `observado` el 100 % de sus filas, pero en el solape la API marca 2.762 pares de renta por persona (4,0 %) como cota por secreto o valor sustituto (2.513 sustitutos de menos de 100 habitantes y 249 cotas); en hogar 2.783 y en Gini 286 cotas. Las filas equivalentes de la base no llevan esa marca.

## 2. Coherencia jerárquica y saltos
- Municipio frente a media ponderada por población de secciones: en municipios con 2 o más secciones (5.081 pares, solo 2015-2018 en datos no sellados) la mediana de |dif. relativa| es 0,014 %; p95 3,4 %; p99 8,2 %. Las 140 diferencias >5 % se dan solo donde las secciones con renta no suman la población municipal (cobertura p1 = 0,50); con cobertura entre 0,98 y 1,02 (4.528 pares) el p99 es 0,28 % y no hay ninguna >5 %. Distritos: igual patrón (297 pares >5 %, 0 con cobertura completa).
- Saltos anuales, |z robusto| > 5: transversal por transición, 1,6 % de las tasas municipales (53-84 por año), 1,1 % en secciones (157-204 por año). Por unidad (series con ≥6 tasas): 293 saltos en 237 municipios (p. ej. 05254: -68,6 % en 2016 y +49,4 % en 2017; 17216: +86,2 % en 2017). 29 tasas municipales superan ±50 %. En secciones solo hay 4 años (2015-2018) no sellados: no se puede hacer el contraste por unidad.
- Cambio de seccionado y cobertura: el número de secciones por municipio cambia en 35 (2015-16), 40 (2016-17) y 76 (2017-18) municipios; 264 de 16.588 secciones tienen huecos internos. Las secciones no se empalman.
- Ruptura de cobertura municipal: con datos municipales pasan de 3.987 (2019) a 4.864 (2020). De los 877 que entran en 2020, 847 llevan `valor_sustituto_media_provincia_pob_menor_100`: es un cambio de definición de lo publicado, no de nivel de renta.

## 3. Valores que no son del propio municipio (municipios no sellados)
- ADRH municipal: 218.092 observados; 3.434 sustitutos de media provincial y 3.296 de media comarcal agraria (menos de 100 habitantes); 1.302 cotas inferiores y 143 superiores. 1.221 municipios distintos, 33 provincias; concentración en 19, 42, 05, 09, 37, 34, 40, 16. De 2020 en adelante hay ~1.700 filas por año frente a ~250 antes.
- Marcado correcto en el versionado: ningún municipio con población <100 queda como `observado`; ningún grupo de ≥4 municipios de la misma provincia y año comparte valor con marca `observado`; el 99,3 % de los no observados tiene población <100. Claves duplicadas: 0.
- Subáreas de Navarra: 422 filas (211 municipios, solo 2020, renta por persona y por hogar), marcadas; todas quedan en la muestra sellada, 0 en la no sellada. En sección y distrito hay 3.312 y 8.238 filas no observadas. Estas filas deben excluirse del análisis principal.

## 4. Alias manuales (11)
Los 11 códigos existen en `territorios.parquet`, son de la provincia indicada, vigentes en 2025 y coinciden con `renta_parque_correspondencia.csv`. Dos nombres de la base difieren en grafía pero coinciden en código (Castelló de la Plana/Castellón de la Plana 12040; Castillonuevo/Gazteluberri 31071). El alias de Noáin (Valle de Elorz) apunta a 31088, cuyo nombre en territorios es «Valle de Elorz/Elortzibar»: el nombre no contiene Noáin; el código es el único candidato del nombre ADRH en Navarra y es plausible, pero conviene que el autor lo confirme. Dos grafías distintas de un mismo municipio (Sant Vicent, Ribarredonda, Erriberabeitia) se resuelven al mismo código sin duplicar claves. De los 18 nombres sin coincidencia, 8 son islas (sin nivel INE); el resto son municipios históricos o fusionados (Cesuras y Oza dos Ríos con 15902; Cerdedo y Cotobade con 36902; Darrical, Candín, Alfarp y Goñi sin código vigente claro). Hay 8 municipios vigentes sin ninguna renta municipal (Benitagla, Carrascalejo (El), Villar del Pozo, Cumbres de Enmedio, Pesquera, Tresviso, Puebla de San Miguel, Sempere).

## 5. Catastro URBANA2026
- SUPERF_URB está en m²: frente a la superficie municipal INE (ha; el área del polígono en EPSG:3035 da cociente mediano 1,00 con la cifra INE), la fracción de suelo urbano es 0,7 % (mediana), 38 % (p99) y 68,6 % (máx., Eliana (l')) con m²; con ha sería 70 veces la superficie del municipio en la mediana y >1 en los 4.807 casos. Mediana 315 m² de suelo por unidad urbana. Sin valores <=0; valor suelo + construcción = total (error relativo <1e-7).
- Cobertura: 7.610 municipios; ninguna fila en las provincias 01, 20, 31 y 48 (524 municipios), más Oza-Cesuras (15902) y Cerdedo-Cotobade (36902). Tras el filtro de sellado quedan 4.811 municipios.

## 6. Inventario ECV y EPF (sin auditoría de fondo)
- ECV transversal 2004-2025 completo (2004-2012, 2013-2017, 2018-2025): pesos DB090, RB050 y PB040 presentes en todas las olas. Longitudinal: 17 periodos, pesos DB090 o DB095 y RB060; el periodo 2008-2011 de la base 2013 es un `.7z` con un `.doc` y no se pudo inspeccionar. Faltan los longitudinales 2017-2020 a 2022-2025.
- EPF: solo 2006 (miembros, gastos, hogar; texto de ancho fijo) y módulo de bienestar 2010. El diseño de registro que acompaña a EPF 2006 se llama `dr_EPF*_2016.xlsx` (el nombre indica 2016): conviene verificar que corresponde a los datos 2006. Factor poblacional (`FACTOR`) declarado en los tres diseños.

## Notas para quien use los datos
Excluir de cualquier análisis principal todo `metodo_dato != observado`. Fijar la ventana municipal de 2020 en adelante solo con la marca. La sección 2019-2023 de la base y de la API son equivalentes salvo redondeo; la base no marca sustitutos.
