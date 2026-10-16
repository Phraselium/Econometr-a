# V14.2 · Escaneo de series de Notariado, Registradores y AEAT (y CGPJ) en todos los formatos

Generado con `python3 src/v14/escaneo_terceros.py --arbol <árbol> --paquete _deposito/vivienda-espana-evidencia-1.0 [--valores]` el 2026-10-16.
- Árbol de prueba: `make arbol_publico` desde d1c2162.
- Paquete: `make paquete_zenodo` desde d1c2162.
- Resultado, fichero a fichero: [escaneo_terceros.csv](escaneo_terceros.csv) y [escaneo_terceros_valores.csv](escaneo_terceros_valores.csv).
- Política aplicada: la de proyecto.json, `terceros_1_0` = registradores «agregados», notariado «agregados», aeat «excluir» (escenarios.md).

## Qué se mira
1. **Columnas, claves y hojas** (src/v14/terceros.py, `escanear`), por formato:
   - .csv, .csv.gz y otros .gz: cabecera;
   - .parquet: esquema, más los valores de las columnas `variable`, `serie` e `indicador`;
   - .xlsx: título de cada hoja y sus 6 primeras filas;
   - .zip: cada fichero interno, recursivamente;
   - .json: claves a cualquier profundidad;
   - .duckdb: columnas de todas las tablas.

   El nombre de la fuente cuenta solo como palabra: notariado, cgn, registradores, registr, aeat, cgpj. Así no cuentan «preregistrada» ni «registradas».
2. **Nombre del fichero** en output/. Es nuevo en V14.2: varias tablas son la serie aunque ninguna columna nombre la fuente, por ejemplo `notariado_provincia_trimestral.csv` o `aeat_declarantes_inmuebles_aprox.csv`.
3. **Valores** (`--valores`), en todos los ficheros de texto, .gz y .parquet del árbol y del paquete:
   - Para cada fuente se toman los valores distintivos de sus ficheros brutos (|v| ≥ 100, sin años ni múltiplos de 100):
     - Notariado: 7.488 valores;
     - Registradores: 31.306;
     - AEAT: 76.014.
   - Se mide qué fracción de los valores de cada fichero coincide con ellos, frente a un control con los mismos valores + 1.
   - Se señala el fichero si coinciden al menos 10 valores y la fracción supera al control en 25 puntos.

## Hallazgos y correcciones
**Repositorio: 82 ficheros con hallazgos.**
- 7 no entran ni en el árbol ni en el paquete: paneles de data/processed y copias completas de la base.
- 17 tablas se redactan: sin las columnas de la serie.
- 13 ficheros se vacían: queda la cabecera, o una nota en los .md.
- data/base/publica/hechos.parquet se filtra: sin las 7 variables `aeat_irpf_*`.
- 44 se revisaron a mano. Nombran la fuente, pero son resultados propios o metadatos (motivo en el .csv). Por ejemplo:
  - métricas, SHAP, ALE y PDP de los modelos con el precio de Registradores;
  - cifras nacionales citadas;
  - el catálogo de variables.

**Nuevo respecto a V14.1** (lo que el escaneo solo por cabeceras no veía):
| Fichero | Qué era | Corrección |
|---|---|---|
| output/f6/notariado_provincia_trimestral.csv y .md | serie trimestral del Notariado, provincia de València (por valores: 122 de 122 coinciden) | vaciado |
| output/f6/notariado_municipio_vs_provincia.csv y .md | serie del Notariado, València | vaciado |
| output/v4/M4/tablas/extranjeros_notariado_cv_provincias.csv | compraventas del Notariado por provincia | vaciado |
| output/v12/f0/aeat_declarantes_inmuebles_aprox.csv | serie municipal de la AEAT (2.882 filas) | vaciado |
| output/v12/f0/aeat_inmuebles_2013_2015.csv | serie municipal de la AEAT | vaciado |
| output/v5/CB/tablas/aeat_irpf_capital_inmobiliario_2019_2024.csv, aeat_viviendas_arrendadas_ccaa_declarante_2024.csv | tablas publicadas por la AEAT | vaciado |
| output/v5/CB/tablas/cgpj_lanzamientos_ccaa.csv, cgpj_verbales_posesorios_ocupacion.csv | series del CGPJ (no redistribuible; sin escenario) | vaciado |
| output/v12/b5/aeat_cv_declarantes_inmuebles.csv, aeat_cv_2013_2015.csv | agregados propios de la serie de la AEAT (sumas de la Comunitat Valenciana) | vaciados con aeat = «excluir»; se publican con «agregados» |
| output/v5/A23/tablas/tamano_implicito_registradores.csv | `pm2` e `importe_medio_vivienda` son la serie de Registradores (por valores: 22 de 22) | redactado: sin esas dos columnas |
| output/v5/CA/tablas/contado_ratio_hipotecas_compraventas.csv | `reg_compraventas_viv` y `reg_hipotecas_viv` son la serie de Registradores (por valores: 19 de 59 frente a 0 del control) | redactado: sin esas dos columnas |

**Árbol y paquete regenerados:**
- Árbol: 57 ficheros con hallazgos, 0 pendientes.
- Paquete: 59 ficheros con hallazgos, 0 pendientes.
- Todos están vaciados, redactados (comprobado que ya no tienen esas columnas) o revisados a mano.
- **Por valores: 0 ficheros por encima del control** en el árbol y en el paquete.
- El paquete no contiene ningún fichero bruto de Notariado, Registradores ni AEAT. De la AEAT solo va el manifiesto: data/raw/v11/aeat_irpf_municipios/_manifest.csv (metadatos, sin valores).
- hechos.parquet del paquete no tiene ninguna variable `aeat_*`.

## Límites
- La búsqueda por valores no ve los valores de menos de 100: porcentajes y precios en logaritmos. Para esos, la garantía es el escaneo por nombre de columna y de fichero.
- Las figuras (.png, .svg) no se escanean por contenido. output/f6/fig_notariado_provincia.png dibuja la serie trimestral del Notariado. Se mantiene como figura citando la fuente: está en output/, no en publicacion/. Queda anotada para la decisión del autor (licencias.md).
- Los ficheros brutos de la AEAT en HTML (data/raw/v5/cb_aeat_*.html) no entran en la búsqueda por valores. Las tablas que salen de ellos (output/v5/CB/tablas/aeat_*) se vacían por nombre.
