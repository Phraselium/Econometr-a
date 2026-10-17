# V15-A · H3: vivienda turística (INE) y alquiler por sección (SERPAVI), 2021-2024

Capa C4 (asociación pre-registrada, entrenamiento). Sin lenguaje causal. `pendiente_sellada: true`: las réplicas con SERPAVI 2025 y el bloque espacial no se han hecho.

## Datos y diseño
- Resultado: log de la mediana SERPAVI de alquiler en €/m² de vivienda colectiva (**stock de contratos declarados en el IRPF, no contratos nuevos**). Exposición: media anual de las ediciones INE del porcentaje de viviendas turísticas, estandarizada por la DT intra-sección (0,61 puntos porcentuales). Efectos fijos de sección y de municipio × año.
- Muestra: 50846 observaciones, 12976 secciones en 1523 municipios (sección con el mismo código en las ediciones INE de 2021 y 2024; 20759 secciones cumplen el criterio, 15680 tienen alquiler y exposición). Madrid, Illes Balears y Canarias están fuera (sellado v6).
- Inferencia: el error agrupado por municipio (principal pre-registrado) no tiene validación en un panel de T = 4: es descriptivo. Conley a 2 km es APTO en V16 solo en su escenario principal de corte transversal; aquí se aplica al panel con la marca «APTO condicionado». No es Holm: H3 es una asociación con su propia familia.

## Resultado principal
- Coeficiente: **0,0030 % por DT intra-sección** (EE de Conley 0,0473; EE agrupado por municipio 0,0410). IC95 de Conley (condicionado): [-0,0897; 0,0957] % por DT. p de Conley 0,950; p agrupado (descriptivo) 0,942.
- Potencia: MDE80 = 0,132 % por DT (Conley), por debajo de los 0,5 % del pre-registro y de los 2-6 % que el pre-registro atribuye a la literatura (cifra del pre-registro, no verificada aquí). El umbral de paso a exploratoria (1 % por DT) no se supera.
- Multiverso de 48 (24 especificaciones × 2 agrupaciones): coeficientes entre 0,003 % y 0,220 % por DT, mediana 0,071; 100 % positivos; con p de Conley < 0,05: 1 de 24 (BH por familia lo aplica el orquestador; los p están en registro.csv).

## Pruebas
- **Placebo de adelanto** (exposición en t+1 con la de t controlada): -0,0057 % por DT, p de Conley 0,765: superado.
- **Sin Barcelona ni València** (las grandes ciudades en entrenamiento): 0,0110 % por DT (EE de Conley 0,0507): mismo signo. Sin el 1 % superior de exposición: 0,0158 %.
- **IPVA por distrito** (resultado alternativo; EE agrupado por municipio, descriptivo): 0,211 % por DT con efecto de año y 0,129 % con municipio × año (242 distritos).
- **Moran de residuos** (distancia inversa, 2 km; solo estadístico): I medio anual -0,074. **Cinelli-Hazlett** RV = 0,00035; **Oster** δ = 0,019 (con efecto casi nulo no informativo).
- **Comprobación de la medida** (pre-registro: se aplica a cualquier resultado): 25,7 % de las observaciones tiene exposición 0; 13,1 % de las secciones no varía; en las 2963 secciones con media ≥ 1 % el coeficiente es 0,0358 % por DT (EE de Conley 0,1009). Las exposiciones por número y por plazas correlacionan con el porcentaje en 0,66 y 0,63. La exposición «viviendas por 100 hogares» no se pudo construir (DV15-A, A5).
- Raíces unitarias, cointegración y rupturas: no aplican (T = 4).

## Lectura frente a lo ya publicado
- La 1.0 dice «turísticos: no concluyente» (v3, v6, V8, V9). Un coeficiente pequeño y preciso por sección no contradice esa conclusión; V9-D2 usa otra exposición (viviendas de uso turístico en 2019 × periodos) y otra unidad (municipio, renta de contratos nuevos): no es comparable cifra a cifra.
- Todo es asociación C4: el alquiler SERPAVI es un stock y se mueve despacio (DT residual del log: 0,030), de modo que un efecto sobre contratos nuevos no se descarta con este resultado.

## Fichas reproducibles
Todas: `python3 src/v15/p5_turismo.py && python3 src/v15/p5_informe.py` (SEED 20261010); cifras en output/v15/p5/estimacion_bruta.json y registro.csv.
- <a id="ficha-h3-principal"></a>**ficha-h3-principal:** `principal.pct_por_DT` = 100 × β de log(SERPAVI VC) sobre z = pct/DT intra-sección, con FE de sección y de municipio × año (src/v15/pa_panel.py:ols_fe); EE de Conley con núcleo de Bartlett a 2 km y puntuaciones sumadas por sección.
- <a id="ficha-h3-rango"></a>**ficha-h3-rango:** `resumen_multiverso.rango_pct_por_DT` (24 especificaciones × 2 agrupaciones).
- <a id="ficha-h3-placebo"></a>**ficha-h3-placebo:** `placebo_adelanto.beta_lead` (modelo con z_t y z_{t+1}, años 2021-2023).
- <a id="ficha-h3-mde"></a>**ficha-h3-mde:** `principal.MDE80_conley_pct_por_DT` = 2,8 × EE de Conley × 100.
- <a id="ficha-h3-ipva"></a>**ficha-h3-ipva:** `ipva_distrito.mun_anio`.
- <a id="ficha-h3-n"></a>**ficha-h3-n:** `principal.n_secciones`.
