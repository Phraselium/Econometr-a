# Léeme primero

**Vivienda en España: base de evidencia reproducible.** Autor: Borja Romero, economista (firma individual, independiente). Versión pública: **1.0** (16 de octubre de 2026). Reúne las versiones internas de desarrollo v1 a V12; la correspondencia está en [CHANGELOG.md](CHANGELOG.md). Para cada tema vale una versión interna: déficit y necesidad de vivienda, v7.1 con las correcciones de v7.2; por qué ha subido, V8; qué causa qué, V9; atlas descriptivo, base y web, V10; demografía, hogares y titularidad, V12. Repositorio: https://github.com/Phraselium/vivienda-espana-evidencia. Para asistentes y consultas rápidas: [consulta/LEEME_ASISTENTE.md](consulta/LEEME_ASISTENTE.md).

El repositorio tiene cuatro puertas de entrada:
- [publicacion/](publicacion/MANIFIESTO.md): todo lo vigente para leer y difundir. Se genera con `make publicacion` y nunca se edita a mano.
- [metodologia/](metodologia/MANIFIESTO.md): cómo se obtiene cada cifra y con qué garantías.
- [reproducir/](reproducir/MANIFIESTO.md): cómo rehacerlo todo y cómo será la evaluación de 2027.
- [historico/](historico/INDICE.md): versiones superadas.

Toda cifra difundible sale de una única tabla, [publicacion/cifras_clave.csv](publicacion/cifras_clave.csv). Cada resultado lleva una capa de evidencia, de C1 (hecho con dos fuentes) a C4 (exploratorio); las definiciones están en [metodologia/capas.md](metodologia/capas.md). Ningún resultado es causal. Se evalúan afirmaciones e instrumentos, nunca partidos ni personas.

**V9 (qué causa qué).** Diseños de identificación pre-registrados ([informe](publicacion/informe_v9.md), [verificador V9](publicacion/verificador/verificador_v9.md)). Ningún resultado alcanza la capa causal; se publican como diferencias o asociaciones con sus pruebas y sin cotas de contribución.

**V12 (población, hogares, titularidad y oferta; descriptivo).** [Atlas V12](publicacion/atlas_v12.md) y [tablas](publicacion/tablas_v12.xlsx).

**V10 (difusión).**
- [Atlas descriptivo](publicacion/atlas_descriptivo.md): quién soporta el coste de la vivienda (por renta, edad, nacionalidad y tenencia) y dónde (provincias, Comunitat Valenciana, barrios y secciones de València), sin lecturas causales.
- Base de datos única ([diccionario](docs/v10/diccionario_base.md)).
- [Figuras](figuras/README.md).
- [Web pública](web/README.md) con panel, mapas y fichas territoriales.

## Itinerarios de lectura

### Ciudadano (15 minutos)
1. [Una página](publicacion/una_pagina.md): los hechos y lo que no se puede afirmar.
2. [Verificador](publicacion/verificador/verificador.md): afirmaciones del debate público con su veredicto. Las fichas de V8 (por qué ha subido) están en el [verificador V8](publicacion/verificador/verificador_v8.md), vigente; las de V7, en el [verificador v7.1](publicacion/verificador/verificador_v7_1.md).

### Periodista (1 hora)
1. [Lo que sabemos y lo que no](publicacion/lo_que_sabemos.md).
2. [Cifras clave](publicacion/cifras_clave.csv): valor, rango, periodo, fuentes, capa y fecha de cada dato. Cite el rango y la capa.
3. Limitaciones: el recuadro «Lo que NO se puede afirmar» de [una página](publicacion/una_pagina.md), la sección 10 del [informe técnico](publicacion/informe_tecnico.md) y [qué cambió entre versiones y por qué](publicacion/que_cambio.md).

### Gestor público o responsable de decisiones (1-2 horas)
1. [Policy brief](publicacion/policy_brief.md): necesidad, datos e instrumentos con la misma vara.
2. [Atlas regional](publicacion/atlas_regional/atlas_resumen.md) y la ficha de su comunidad en [atlas_regional/](publicacion/atlas_regional/atlas_resumen.md). Lea la sección 6 bis: dosis y coste de cada instrumento, siempre en condicional (C4).
3. Para exponer: [ponencia](publicacion/ponencia/diapositivas.md) con su [guion](publicacion/ponencia/guion.md) y el [artículo del Colegio](publicacion/articulo_colegio.md).

### Revisor (medio día)
1. [Guía del revisor](metodologia/guia_revisor.md).
2. [Anexo metodológico](metodologia/anexo_metodologico.md): una ficha por cifra publicable.
3. [Nota metodológica](publicacion/nota_metodologica.md): estimadores de panel regional con un factor común no estacionario.
4. [Reproducir](reproducir/instrucciones.md): instrucciones, [entorno](reproducir/entorno.md), [tiempos](reproducir/tiempos.md) y [protocolo de la evaluación de 2027](reproducir/evaluacion_2027.md).

### Técnico (un día)
1. [Working paper](publicacion/working_paper.md).
2. Código: src/. Por versión, con `make all`, `make v7`, `make publicacion` y `make check`. El mapa de carpetas está en [docs/MAPA.md](docs/MAPA.md).
3. Tests: tests/, incluidos tests/v7 y tests/v7_1, la doble implementación de tests/doble_impl y los controles de texto y cifras.

## Órdenes

```bash
python3 -m pip install -r requirements.lock
make all           # v1-v6.3 sin red (unas 2 h)
make v7            # atlas regional V7 y consolidación V7.1 (unos 50 min)
make base atlas figuras web   # V10: base única, atlas, figuras y web
make publicacion   # regenera publicacion/, metodologia/ y reproducir/
make check         # ruff, tests y controles de texto, cifras y capas
```
