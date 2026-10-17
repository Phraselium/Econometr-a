# Metadatos del depósito en Zenodo (versión 1.0)

Se copian a mano en https://zenodo.org/uploads/new (docs/v14/tareas_autor.md, punto 3).
- Coinciden con .zenodo.json y CITATION.cff, que genera `make metadatos` desde proyecto.json.
- tests/v14/test_publicacion_1_0.py comprueba que el título, la versión, el autor, la fecha, las palabras clave y el repositorio de este fichero son los de .zenodo.json.
- Si se cambia proyecto.json, se regenera con `make metadatos` y se corrige aquí.

| Campo de Zenodo | Valor |
|---|---|
| Tipo de recurso | Software (`upload_type`: software) |
| Título | Vivienda en España: base de evidencia reproducible (1.0) |
| Autor | Romero, Borja · afiliación: Economista independiente |
| Versión | 1.0 |
| Fecha de publicación | 2026-10-16 |
| Idioma | spa (español) |
| Palabras clave | vivienda; España; precios de la vivienda; alquiler; déficit de vivienda; econometría; reproducibilidad |
| DOI | lo reserva Zenodo («Reserve DOI») y se escribe en proyecto.json, `doi` (tareas_autor.md, punto 4) |

## Descripción (español; es la de .zenodo.json)
Base de evidencia independiente y reproducible sobre la vivienda en España por provincias, con un módulo para València.
- **Qué cubre:**
  - el déficit y la necesidad de vivienda 2026-2035;
  - las diferencias territoriales;
  - los precios y el alquiler triangulados;
  - la comparación europea;
  - una matriz de instrumentos de política;
  - un verificador de afirmaciones.
- **Qué incluye además:**
  - una atribución por factores y periodos de la subida del precio de compra y del alquiler (V8);
  - diseños de identificación pre-registrados (V9);
  - una base de datos única con atlas descriptivo y web (V10);
  - una contabilidad demográfica, de hogares, titularidad y oferta (V12).
- **Capas de evidencia.** Cada resultado se clasifica en una capa: C1, C2, C3, C3s o C4.
- **Datos de terceros.** Los que no tienen redistribución clara no se incluyen: `make datos_terceros` los descarga y verifica (docs/v8_1/datos_retirados.md; docs/v13/datos_deposito.md). Después, `make all` reproduce sin red.
- **Versiones.** La versión pública 1.0 reúne las versiones internas v1-V12 (CHANGELOG.md).

## Description (English, to add as an additional description)
Independent, reproducible evidence base on housing in Spain by province, with a module for València.
- **What it covers:**
  - housing shortfall and need, 2026-2035;
  - territorial differences;
  - triangulated purchase prices and rents;
  - a European comparison;
  - a matrix of policy instruments;
  - a claim checker.
- **What else it includes:**
  - an attribution of the rise in purchase prices and rents by factor and period (V8);
  - pre-registered identification designs (V9);
  - a single database with a descriptive atlas and website (V10);
  - demographic, household, ownership and supply accounts (V12).
- **Evidence layers.** Every result carries an evidence layer: C1 (fact, two or more sources), C2 (bounds under explicit assumptions), C3/C3s (causal; C3s only under declared sign restrictions) or C4 (exploratory). No result in this version reaches C3.
- **Third-party data.** Data without clear redistribution terms are not included: `make datos_terceros` downloads and verifies them. After that, `make all` reproduces everything offline.

## Licencias por parte
| Parte | Licencia | Dónde se declara |
|---|---|---|
| Código (src/, tests/, Makefile) | MIT | LICENSE; campo `license` de .zenodo.json |
| Textos, tablas y figuras propios (publicacion/, metodologia/, output/, figuras/, web/, paper/, docs/) | CC BY 4.0 | LICENSE; campo `notes` de .zenodo.json |
| Tablas, bases y cifras construidas con los datos abiertos de Registradores (la parte construida con ellos; 65 ficheros de docs/v14/licencias_tablas.csv) | ODbL 1.0, con el aviso de atribución | LICENSE, punto 4; `notes` de .zenodo.json; CITATION.cff (`ODbL-1.0`) |
| Datos de terceros incluidos (data/raw de clase a, capa pública de la base) | la de su fuente | docs/v5/licencias_datos.md; docs/v13/datos_inventario.csv |
| Series de Notariado, Registradores (datos abiertos y Anuario ERI) y AEAT | no se incluyen (proyecto.json, `terceros_1_0`) | docs/v14/licencias.md; docs/v14/registradores_origen.md |

En el formulario de Zenodo: licencia principal «MIT License»; añada «Open Data Commons Open Database License v1.0» como licencia adicional si el formulario lo permite. En «Additional notes», el texto de `notes` de .zenodo.json:
> Código bajo MIT; textos, tablas y figuras propios bajo CC BY 4.0 (fichero LICENSE). Los datos de terceros conservan sus licencias: véase docs/v5/licencias_datos.md y docs/v13/datos_deposito.md. Las tablas, bases y cifras construidas con los datos abiertos del Colegio de Registradores se publican bajo la Open Database License (ODbL) 1.0 (https://opendatacommons.org/licenses/odbl/1-0/; lista de ficheros en docs/v14/licencias_tablas.csv). Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/.

## Identificadores relacionados
| Relación en Zenodo | Identificador | Nota |
|---|---|---|
| is supplement to | https://github.com/Phraselium/vivienda-espana-evidencia | repositorio nuevo (también en .zenodo.json) |
| is derived from | https://github.com/Phraselium/Econometr-a/tree/{{COMMIT_ORIGEN}} | repositorio de desarrollo archivado, en el commit de origen del árbol. El valor exacto está en docs/v14/arbol_1_0.md y en el README del árbol («Procedencia») |
| is documented by | https://phraselium.github.io/vivienda-espana-evidencia/ | web |

El fichero que se sube es `_deposito/vivienda-espana-evidencia-1.0.zip` (`make paquete_zenodo && python3 src/v13/paquete_zenodo.py --zip`), y su sha256 se anota en tareas_autor.md al subirlo.
