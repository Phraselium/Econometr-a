# Instrucciones comunes para subagentes v7

## Antes de empezar
- Proyecto: /home/user/Econometr-a, en español. Lee CLAUDE.md y docs/v7/decisiones.md y docs/v6/decisiones.md.
- No hagas commit ni push: lo hace el orquestador.
- No leas data/sealed. data/raw y data/processed son de solo lectura, salvo los ficheros NUEVOS que descargues a data/raw/v6/.
- Lee los ficheros grandes solo con head, wc o consultas.

## Código y ficheros
- Escribe únicamente en tus rutas:
  - src/v6/<modulo>_*.py: un `<modulo>_run.py` determinista y sin red, y opcionalmente `<modulo>_fetch.py` con red, que queda fuera de make;
  - output/v6/<MODULO>/;
  - la sección de tu módulo en docs/v6/fuentes_fallidas.md, añadiendo al final y con endpoint, edición y fecha de la prueba.
- `<modulo>_run.py`:
  - solo lee ficheros versionados o generados por `make clean` (data/processed); un fichero >50 MB va comprimido (.csv.gz);
  - SEED=20261010 y un solo hilo;
  - registra TODAS las especificaciones en output/v6/<MODULO>/registro.csv (el Registry de src/econ_utils.py si aplica) y aplica Holm o BH.
- `ruff check src/v6` debe pasar, y `python3 src/v3/check_texto.py` no debe dar errores nuevos.

## Capas, evidencia y redacción
- Capas: C1 hecho con ≥2 fuentes independientes y todos sus componentes en C1; C2 cota con supuestos explícitos; C3 efecto identificado; C4 exploratorio o de fuente única. La capa de un hecho es la menor de sus componentes. Nunca promover de capa. Con C4, veredicto como máximo «ANALIZADA, NO CONCLUYENTE».
- Sin lenguaje causal por debajo de C3. Neutralidad estricta: sin lenguaje valorativo ni partidista.
- Cada cifra lleva su fecha del dato. Las magnitudes van en viviendas, €/mes y %. Los resultados negativos se reportan; si dos métodos discrepan, se dan ambos. Nada inventado.
- Literatura: VERIFICADA (DOI en Crossref y cuartil de Scimago) o NO VERIFICADA / «cuartil no verificado».

## Qué entregar
- output/v6/<MODULO>/resultado.json con {rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra{modelo, rmse, dm_vs_ar4}, notas}. Si un campo no aplica, pon null.
- Además, output/v6/<MODULO>/hechos.json con una lista de cifras para cifras_clave: {id, indicador, valor, min, max, unidad, periodo, cobertura, fuentes, capa, fecha_dato}.
- Si tu módulo aporta una afirmación del debate, añade output/v6/<MODULO>/fichas_verificador.json con el formato de output/v4/M5/fichas_verificador.json.
- Devuelve: rutas, un resumen de ≤200 palabras y los tokens aproximados. Nunca datos crudos.

## Reglas de v6
- **Validación sellada.** Para cualquier panel de modelización, sepáralo con `holdout.sellar_v6(df, nombre, nivel, col_anio, ultimo_anio, col_prov=…, col_mun=…, col_dist=…)` y trabaja SOLO con la parte de entrenamiento que devuelve. La parte sellada solo se abre con `holdout.evaluate_v6(modelo_id, fn, rama, nombres)`, una vez por modelo, y solo en M4 (o en M3 con el modelo final).
- **Predicción no es causalidad.** Las importancias, SHAP, ALE y dependencias parciales son descriptivas (C4). No se escribe lenguaje causal a partir de ellas.
- **Compra.** Cada resultado declara su medida de precio en un campo «medida_precio» de resultado.json: valor tasado del Ministerio, Notariado, Registradores, índice triangulado o IPV del INE (solo CCAA).
- **Alquiler.** Stock (SERPAVI, IPC) y contratos nuevos (fianzas) van SIEMPRE por separado.
- **Magnitudes.** €/mes para el alquiler; €/m² y % para la compra, por unidad interpretable de cada variable.

## Reglas de V7
- Lo nuevo va en:
  - src/v7/<modulo>_*.py;
  - output/v7/<MÓDULO>/;
  - docs/v7/ (solo los ficheros que te asignen).
- No modifiques código de v1-v6 salvo que se te pida expresamente para corregir un error. Si lo haces, documenta el cambio, el antes y el después.
- La sección «Qué entregar» se aplica igual, cambiando output/v6 por output/v7.
- `make check` debe seguir pasando.

## Reglas de V7
- **Tope de tokens.** Cada encargo lleva un tope. Al llegar al 80 % de ese tope, para, guarda lo hecho y devuelve el estado: qué está terminado, qué falta y las rutas.
- **Cruces territoriales.** Siempre por código INE (`codigo_ine_ccaa` o `cod_prov`, dos dígitos, como texto), nunca por nombre.
- **v6.2 queda congelada.** No modifiques output/v5 ni output/v6* ni sus scripts, salvo que el encargo lo diga de forma expresa.
- **Inferencia con 17 CCAA.**
  - Errores: wild cluster bootstrap (Webb), Driscoll-Kraay y CCE.
  - Control de falsos descubrimientos: Holm o BH por familia, con todas las especificaciones registradas en econ_utils.Registry.
  - Los resultados negativos se reportan.
- **Lenguaje.** Las descomposiciones, el SHAP y las importancias son asociación, nunca causalidad.
- **Paneles de CCAA.** No están sellados y v1 ya los usó: todo backtest se etiqueta «informativo, muestra ya vista en v1».
