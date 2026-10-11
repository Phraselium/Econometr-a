# Decisiones v6

## Setup y validación sellada
- Rama r6/main desde r5.1/main (bac2fda, v5.1).
- **Validación sellada nueva (holdout.py: `provincias_selladas_v6`, `sellar_v6`, `evaluate_v6`).**
  - Temporal: el último año disponible de cada panel.
  - Transversal: el 20 % de las provincias por bloques completos de CCAA, en orden aleatorio con SEED+6, sin las CCAA que contienen las provincias selladas en v2 (11, 16 y 45). Resultado: 07, 22, 26, 28, 30, 31, 33, 35, 38, 44 y 50 (Baleares, Aragón, La Rioja, Madrid, Murcia, Navarra, Asturias y Canarias; 11 de 52, 21 %).
  - Los municipios y distritos de esas provincias quedan sellados: una sola partición espacial (≈20 % en cada nivel), sin fuga entre niveles en los modelos jerárquicos.
  - Los distritos sellados en v3 se excluyen de todo uso en v6.
- **Limitación declarada: contaminación descriptiva.** El último año y todas las provincias se usaron de forma DESCRIPTIVA en v4-v5 (tasas, mapas, B3). La validación v6 es nueva para la estimación y la selección de modelos, pero no es una muestra que nadie haya visto nunca. Así se dirá en todos los resultados.
- `evaluate_v6` abre la muestra sellada UNA vez por modelo o hipótesis, y queda registrado en docs/v2/holdout_accesos.md.

## G (subagente)
- Pasan a archive/ (con git mv) los entregables de v3 y v4 que ningún script ni plantilla cita. informe_tecnico y lo_que_sabemos de v4 se quedan, porque las plantillas v5 los citan.
- Makefile: se añaden `a5_validacion` y `b3_potencia`, que producen ficheros versionados que leen otros scripts. Reproducen sus salidas byte a byte.
- Quedan pendientes para el autor (docs/v6/tareas_autor.md):
  - tres scripts de datos auxiliares fuera de `make data`;
  - las etiquetas;
  - la release y el DOI;
  - la autoría de los commits.

## Revisión de M0: REHACER (B1-B5)
- **B5, declaración** (orquestador). El corte temporal de v6 (el último año: 2025 en compra y 2024 en alquiler) cae dentro de la ventana sellada de v2 (2024Q3-2026Q2). Esa ventana se abrió 8 veces para las hipótesis confirmatorias de v2, y siempre para las 3 provincias selladas de v2 (11, 16 y 45).
  - Consecuencias:
    - el año de validación v6 NO es nuevo en el tiempo;
    - lo nuevo es la combinación de año y provincias: las 11 provincias v6 no se usaron nunca como validación;
    - las variables y especificaciones de v6 no se eligieron mirando su error en esa muestra.
  - Se declara en hipotesis.md y en todo resultado de M3/M4 como «validación espacial nueva; temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5».
- **B1-B4 y determinismo.** Los corrige el agente de M0:
  - un mismo corte temporal por mercado en todos los niveles;
  - las CCAA uniprovinciales se asignan a su provincia;
  - el pre-registro se cierra sin grados de libertad;
  - gzip con mtime=0.
- **Correcciones de M0 aplicadas** por el agente: B1-B4, determinismo y los no bloqueantes locales.
  - Cortes temporales por mercado: compra en 2025 y alquiler en 2024, iguales en todos los niveles.
  - Las 11 provincias selladas tienen precio.
  - hipotesis.md cerrado: regresores en t−1, efectos fijos de unidad y año, DM-HLN, Holm/BH, embargo de 1 año y criterio operativo de «relevante con seguridad».
  - md5 idénticos.
- **No hay segunda revisión de M0.** Las correcciones son exactamente las que pidió el revisor y no se ha estimado nada. El revisor final comprobará el pre-registro.
- **m0_run.py entra en `make all` (V6_ORDEN).** En un clon limpio regenera el sellado (data/sealed no está versionado) y check_v6 verifica que su sha256 coincide con output/v6/M0/sellado_info.json.
- **Pre-registro.** La etiqueta `prereg-v6` se pone en este commit, antes de cualquier estimación. Es local; el remoto rechaza etiquetas (tarea del autor).

## M1, M2 y M3 (subagentes)
- **Ningún resultado pasa de C4.**
  - Ninguna hipótesis confirmatoria sobrevive a Holm en la especificación pre-registrada: N pequeño (41 provincias de entrenamiento) y regresores en t−1.
  - La identificación (shift-share de un solo choque F=6; topes con pretendencias rechazadas) no alcanza C3.
- **Sustitutos declarados:** BART por un bosque con bootstrap bayesiano, y PyMC por MixedLM (no instalados).
- **Deep learning:** resultado negativo en el alquiler (distrito) y en la compra (municipio). Ninguna red bate a gradient boosting.
- **Compra trimestral:** la persistencia (1,91 %) iguala o mejora a ML y econometría. Es un resultado negativo para el valor añadido de los modelos frente a la inercia.
- **Determinismo:** los .csv.gz se escriben con mtime=0 en M2, M3a y M3b.

## M4 (subagente)
- **Evaluación sellada.** src/v6/m4_sellado.py la ejecuta una sola vez, fuera de make: 53 aperturas, una por modelo, con fn probada antes sobre un sellado falso. Los resultados se versionan en output/v6/M4/sellado_*.json. m4_run.py (en make) solo lee esos JSON, así que `make all` no reabre el sellado.
- **«Mejor modelo».** Se elige por el RMSE espacial en la sellada y por la estabilidad.
  - Los árboles (GB y RF) ganan en alquiler y en el precio provincial.
  - El ECM v1 gana en el precio municipal y en Registradores, con empate técnico.
  - En el volumen trimestral del último año, la persistencia no se bate.
- **Ninguna variable cumple el criterio pre-registrado de «relevante con seguridad».** La familia econométrica nunca pasa Holm. Todo queda en C4.
- **Limitación de la comparación espacial.** En provincias nuevas, AR, ECM y M1 caen a persistencia, porque no tienen efecto fijo. La red de M3a no admitía provincias nuevas y M4 usa la media de los embeddings (declarado).
- Se elimina de output/v6/M1A/diagnosticos.json el campo «seg» (tiempo de ejecución), que impedía que dos ejecuciones dieran md5 idénticos.

## Revisión final de v6: APROBAR (16 no bloqueantes) → correcciones prioritarias aplicadas por el orquestador
- N1: m3b_run entra en `make all` una vez comprobado su determinismo.
- N2-N3: M2 fija un solo hilo; M1A ya no guarda tiempos; `.tmp_todo.pkl` deja de versionarse (.gitignore).
- N4: la desviación de las variables nacionales en el ML trimestral de compra queda declarada en M3B/desviaciones.md.
- N5-N6 y N8: las notas de M4/resultado.json recogen los embeddings medios, los sustitutos de BART y PyMC, el sesgo de selección del ganador mirado en el sellado y la divergencia del AR municipal.
- N13-N15: M1A deja de decir «ASOCIACIÓN ROBUSTA»; M1B dice «variación asociada»; la elasticidad precio-alquiler se da como rango de 0,4 a 2,1 según la especificación; la fecha del dato es la de los datos.
- El resto de no bloqueantes queda en docs/v6/revision_final.md, sin impacto en las conclusiones.
