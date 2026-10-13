# Léeme primero

**Vivienda en España: base de evidencia reproducible.** Autor: Borja Romero, economista (firma individual, independiente). Versión de referencia: **v7.2** (13 de octubre de 2026; v7.1 con correcciones previas a la release).

El repositorio tiene cuatro puertas de entrada:
- [publicacion/](publicacion/MANIFIESTO.md): todo lo vigente para leer y difundir. Se genera con `make publicacion` y nunca se edita a mano.
- [metodologia/](metodologia/MANIFIESTO.md): cómo se obtiene cada cifra y con qué garantías.
- [reproducir/](reproducir/MANIFIESTO.md): cómo rehacerlo todo y cómo será la evaluación de 2027.
- [historico/](historico/INDICE.md): versiones superadas.

Toda cifra difundible sale de una única tabla, [publicacion/cifras_clave.csv](publicacion/cifras_clave.csv). Cada resultado lleva una capa de evidencia, de C1 (hecho con dos fuentes) a C4 (exploratorio); las definiciones están en [metodologia/capas.md](metodologia/capas.md). Ningún resultado es causal. Se evalúan afirmaciones e instrumentos, nunca partidos ni personas.

## Itinerarios de lectura

### Ciudadano (15 minutos)
1. [Una página](publicacion/una_pagina.md): los hechos y lo que no se puede afirmar.
2. [Verificador](publicacion/verificador/verificador.md): afirmaciones del debate público con su veredicto. Las fichas de V7 están en el [verificador v7.1](publicacion/verificador/verificador_v7_1.md).

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
make publicacion   # regenera publicacion/, metodologia/ y reproducir/
make check         # ruff, tests y controles de texto, cifras y capas
```
