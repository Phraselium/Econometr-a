# Instrucciones comunes para subagentes v5

## Antes de empezar
- Proyecto: /home/user/Econometr-a, en español. Lee CLAUDE.md y docs/v5/decisiones.md.
- No hagas commit ni push: lo hace el orquestador.
- No leas data/sealed. data/raw y data/processed son de solo lectura, salvo los ficheros NUEVOS que descargues a data/raw/v5/.
- Lee los ficheros grandes solo con head, wc o consultas.

## Código y ficheros
- Escribe únicamente en tus rutas:
  - src/v5/<modulo>_*.py: un `<modulo>_run.py` determinista y sin red, y opcionalmente `<modulo>_fetch.py` con red, que queda fuera de make;
  - output/v5/<MODULO>/;
  - la sección de tu módulo en docs/v5/fuentes_fallidas.md, añadiendo al final y con endpoint, edición y fecha de la prueba.
- `<modulo>_run.py`:
  - solo lee ficheros versionados o generados por `make clean` (data/processed); un fichero >50 MB va comprimido (.csv.gz);
  - SEED=20261010 y un solo hilo;
  - registra TODAS las especificaciones en output/v5/<MODULO>/registro.csv (el Registry de src/econ_utils.py si aplica) y aplica Holm o BH.
- `ruff check src/v5` debe pasar, y `python3 src/v3/check_texto.py` no debe dar errores nuevos.

## Capas, evidencia y redacción
- Capas: C1 hecho con ≥2 fuentes independientes y todos sus componentes en C1; C2 cota con supuestos explícitos; C3 efecto identificado; C4 exploratorio o de fuente única. La capa de un hecho es la menor de sus componentes. Nunca promover de capa. Con C4, veredicto como máximo «ANALIZADA, NO CONCLUYENTE».
- Sin lenguaje causal por debajo de C3. Neutralidad estricta: sin lenguaje valorativo ni partidista.
- Cada cifra lleva su fecha del dato. Las magnitudes van en viviendas, €/mes y %. Los resultados negativos se reportan; si dos métodos discrepan, se dan ambos. Nada inventado.
- Literatura: VERIFICADA (DOI en Crossref y cuartil de Scimago) o NO VERIFICADA / «cuartil no verificado».

## Qué entregar
- output/v5/<MODULO>/resultado.json con {rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia, diagnosticos, fuera_muestra{modelo, rmse, dm_vs_ar4}, notas}. Si un campo no aplica, pon null.
- Además, output/v5/<MODULO>/hechos.json con una lista de cifras para cifras_clave: {id, indicador, valor, min, max, unidad, periodo, cobertura, fuentes, capa, fecha_dato}.
- Si tu módulo aporta una afirmación del debate, añade output/v5/<MODULO>/fichas_verificador.json con el formato de output/v4/M5/fichas_verificador.json.
- Devuelve: rutas, un resumen de ≤200 palabras y los tokens aproximados. Nunca datos crudos.
