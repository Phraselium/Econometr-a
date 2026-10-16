# Versión pública 1.0

Texto para la publicación de GitHub del repositorio vivienda-espana-evidencia (`gh release create v1.0.0 … --notes-file`). Va sin cifras: todas están en [publicacion/una_pagina.md](../../../publicacion/una_pagina.md) y [publicacion/cifras_clave.csv](../../../publicacion/cifras_clave.csv), cada una con su capa, su fecha y su ficha.

---

## Qué es
- **Una base de evidencia independiente y reproducible sobre la vivienda en España.** Abarca:
  - el déficit y la necesidad de vivienda 2026-2035;
  - los precios de compra y el alquiler, triangulados;
  - las diferencias entre provincias y comunidades, con un módulo para València;
  - una atribución por factores y periodos de la subida del precio (V8);
  - diseños pre-registrados de qué causa qué (V9);
  - una base de datos única con atlas y web (V10-V12).
- **Cada resultado lleva una capa de evidencia:**
  - C1: hecho con al menos dos fuentes;
  - C2: cota con supuestos explícitos;
  - C3s: vale solo bajo restricciones de signo declaradas;
  - C4: exploratorio.

  Ningún resultado de esta versión está en C3 (causal con un instrumento o un diseño que supera las pruebas).
- **La versión 1.0 reúne las versiones internas v1-V12** del repositorio de desarrollo Phraselium/Econometr-a. Ese repositorio queda archivado; la correspondencia está en CHANGELOG.md.
- **Por dónde empezar:**
  - [publicacion/una_pagina.md](../../../publicacion/una_pagina.md): una página para lectores no técnicos;
  - [LEEME_PRIMERO.md](../../../LEEME_PRIMERO.md): mapa del repositorio;
  - [consulta/](../../../consulta/): registro de hallazgos y preguntas frecuentes.

## Cómo citar
> Romero, B. (2026). *Vivienda en España: base de evidencia reproducible* (versión 1.0) [software y datos]. Zenodo. https://doi.org/{{DOI}}

CITATION.cff y .zenodo.json llevan los mismos datos (`make metadatos`, desde proyecto.json). Cite siempre la cifra por su id de cifras_clave, con su capa y la fecha del dato.

## Qué no se puede afirmar con estos datos
- **Que un solo factor sea la causa principal de la subida del precio.** Ni los pisos turísticos, ni la inmigración, ni la falta de oferta, ni los tipos de interés, ni los compradores extranjeros, ni las empresas.
- **Que los topes al alquiler bajen los precios o reduzcan la oferta.**
- **Que haya una burbuja, ni que no la haya.**
- **Qué parte de las viviendas tienen empresas o grandes propietarios.**
- **Cuántas viviendas harán falta exactamente entre 2026 y 2035.** La estimación es exploratoria y depende de supuestos.
- **Nada causal a partir de un modelo que predice bien:** predecir no es explicar.
- **Que una asociación (C4) o un resultado condicionado a restricciones (C3s) pruebe una causa.**

La lista completa, con cifras y fichas, está en el recuadro de [una_pagina.md](../../../publicacion/una_pagina.md).

## Limitación de reproducibilidad
- **Sin red,** con el paquete del depósito (`make datos`), se reproducen:
  - las tablas, las figuras, la publicación y la web;
  - los tests que necesitan datos de terceros no redistribuibles (Notariado, Registradores, CGPJ, AEAT y otros) se omiten, con su motivo. El recuento exacto de una ejecución real está en el README y en docs/v14/tests_arbol.json.
- **Para reconstruir todo,** hay que descargar antes esos datos con `make datos_terceros` (con red; docs/v11/descargas_manuales.md para las descargas manuales). Después:
  - `make all`;
  - el depósito tiene las tablas de output/ que contienen esas series redactadas (sin sus columnas) o vaciadas. Ningún enlace se rompe.
- **Algunas cifras no se publican en la 1.0** por la licencia de su fuente: publicacion/cifras_no_publicadas_1_0.csv. Siguen en el registro cifras_clave.
- **Evaluaciones selladas ya hechas:** sus resultados van en output/. La muestra sellada no se publica ni se reabre. Su huella (sha256) está en proyecto.json, `hash_sellado`.
- **Evaluaciones diferidas de V7 y V8:** se harán una sola vez con datos posteriores (`make evaluate_v7`, `make evaluate_v8`).

## Licencias
- **Código:** MIT.
- **Textos, tablas y figuras propios:** CC BY 4.0.
- **Datos de terceros:** la licencia de su fuente (docs/v5/licencias_datos.md, docs/v14/licencias.md).
