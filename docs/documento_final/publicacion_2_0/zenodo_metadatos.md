# Metadatos del depósito en Zenodo (versión 2.0, preparada)

Se copian a mano en https://zenodo.org/uploads/new (docs/tareas_autor.md, punto 6).
- Coinciden con .zenodo.json y CITATION.cff, que genera `make metadatos` desde proyecto.json.
- tests/v14/test_publicacion_1_0.py comprueba (desde la 2.0, sobre este fichero) que el título, la versión, el autor, la fecha, las palabras clave y el repositorio de este fichero son los de .zenodo.json.
- Si se cambia proyecto.json, se regenera con `make metadatos` y se corrige aquí.

| Campo de Zenodo | Valor |
|---|---|
| Tipo de recurso | Software (`upload_type`: software) |
| Título | Vivienda en España: base de evidencia reproducible (2.0) |
| Autor | Romero, Borja · afiliación: Economista independiente |
| Versión | 2.0 |
| Fecha de publicación | 2026-10-23 |
| Idioma | spa (español) |
| Palabras clave | vivienda; España; precios de la vivienda; alquiler; déficit de vivienda; econometría; reproducibilidad |
| DOI | lo reserva Zenodo («Reserve DOI») y se escribe en proyecto.json, `doi` (docs/tareas_autor.md, punto 7) |

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
- **Documento final.** publicacion/documento_final/: qué permiten decir V15-V18 (réplicas, auditoría, mejor estimación por factor rotulada como juicio experto).
- **Versiones.** La versión pública 2.0 reúne las versiones internas v1-V18 (CHANGELOG.md).

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
  - demographic, household, ownership and supply accounts (V12);
  - a final document (V15-V18): replications, an audit of public claims and policies, and a best estimate per factor labelled as expert judgement.
- **Evidence layers.** Every result carries an evidence layer: C1 (fact, two or more sources), C2 (bounds under explicit assumptions), C3/C3s (causal; C3s only under declared sign restrictions) or C4 (exploratory). No result in this version reaches C3.
- **Third-party data.** Data without clear redistribution terms are not included: `make datos_terceros` downloads and verifies them. After that, `make all` reproduces everything offline.

## Licencias por parte
| Parte | Licencia | Dónde se declara |
|---|---|---|
| Código (src/, tests/, Makefile) | MIT | LICENSE; campo `license` de .zenodo.json |
| Textos, tablas y figuras propios (publicacion/, metodologia/, output/, figuras/, web/, paper/, docs/) | CC BY 4.0 | LICENSE; campo `notes` de .zenodo.json |
| Tablas, bases y cifras construidas con los datos abiertos de Registradores (la parte construida con ellos; 65 ficheros de docs/v14/licencias_tablas.csv) | ODbL 1.0, con el aviso de atribución | LICENSE, punto 4; `notes` de .zenodo.json; CITATION.cff (`ODbL-1.0`) |
| Datos de terceros incluidos (data/raw de clase a, capa pública de la base) | la de su fuente | docs/v5/licencias_datos.md; docs/v13/datos_inventario.csv |
| Datos de la AEAT (series de data/raw, variables `aeat_irpf_*` de la capa pública y tablas derivadas) | se incluyen: reutilización autorizada por la AEAT citando la fuente y la fecha (K16; `terceros_1_0.aeat` = redistribuir) | LICENSE, punto 5; `notes` de .zenodo.json; `references` de CITATION.cff |
| Series de Notariado y del Anuario ERI de Registradores | no se incluyen (solo agregados propios con atribución) | docs/v14/licencias.md; docs/v14/registradores_origen.md |
| Series del CGPJ | no se incluyen (licencia no verificada: solo agregados propios) | docs/v5/licencias_datos.md |

En el formulario de Zenodo: licencia principal «MIT License»; añada «Open Data Commons Open Database License v1.0» como licencia adicional si el formulario lo permite. En «Additional notes», el texto de `notes` de .zenodo.json:
> Código bajo MIT; textos, tablas y figuras propios bajo CC BY 4.0 (fichero LICENSE). Los datos de terceros conservan sus licencias: véase docs/v5/licencias_datos.md y docs/v13/datos_deposito.md. Las tablas, bases y cifras construidas con los datos abiertos del Colegio de Registradores se publican bajo la Open Database License (ODbL) 1.0 (https://opendatacommons.org/licenses/odbl/1-0/; lista de ficheros en docs/v14/licencias_tablas.csv). Contiene información de «Compraventas de inmuebles, uso residencial, por provincia» (Colegio de Registradores, https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia), disponible bajo la Open Database License (ODbL) 1.0, https://opendatacommons.org/licenses/odbl/1-0/. Fuente: Agencia Estatal de Administración Tributaria (AEAT), Estadística de los declarantes del IRPF por municipios, ejercicios 2013-2024, consultado el 15 de octubre de 2026; y Estadística de los declarantes del IRPF (bienes inmobiliarios, ejercicios 2019-2024; vivienda, ejercicio 2024), consultado el 13 de octubre de 2026. Reutilización autorizada citando la fuente (https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica/aviso-legal/utilizacion-informacion-contenida-web-aeat.html); la AEAT no participa ni patrocina este trabajo.

## Identificadores relacionados
| Relación en Zenodo | Identificador | Nota |
|---|---|---|
| is supplement to | https://github.com/Phraselium/vivienda-espana-evidencia | repositorio nuevo (también en .zenodo.json) |
| is derived from | https://github.com/Phraselium/Econometr-a/tree/{{COMMIT_ORIGEN}} | repositorio de desarrollo archivado, en el commit de origen del árbol. El valor exacto está en el README del árbol («Procedencia») |
| is documented by | https://phraselium.github.io/vivienda-espana-evidencia/ | web |

El fichero que se sube es `_deposito/vivienda-espana-evidencia-2.0.zip` (`make paquete_zenodo && python3 src/v13/paquete_zenodo.py --zip`), y su sha256 se anota en docs/tareas_autor.md al subirlo.
