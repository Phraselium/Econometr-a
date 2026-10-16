# Vivienda en España: base de evidencia reproducible

**Autor:** Borja Romero, economista (firma individual, independiente). **Versión pública:** 1.0 (16 de octubre de 2026). Las versiones v1 a V12 son versiones internas de desarrollo; su correspondencia con la 1.0 está en [CHANGELOG.md](CHANGELOG.md). La 1.0 no añade análisis: ordena, aligera y prepara el depósito.

**Repositorio:** https://github.com/Phraselium/vivienda-espana-evidencia (la URL se configura en un único sitio, [proyecto.json](proyecto.json)). **DOI:** pendiente (Zenodo).

## Versión interna vigente por tema

| Tema | Versión interna vigente | Dónde leerlo |
|---|---|---|
| Déficit y necesidad de vivienda 2026-2035, simulaciones de instrumentos y atlas regional | v7.1 con las correcciones de v7.2 | [lo que sabemos](publicacion/lo_que_sabemos.md), [policy brief](publicacion/policy_brief.md), [atlas regional](publicacion/atlas_regional/atlas_resumen.md) |
| Por qué ha subido el precio de compra y el alquiler | V8 (redacción y tablas de v8.1) | [por qué ha subido](publicacion/por_que_ha_subido.md), [informe econométrico](publicacion/informe_econometrico_v8.md), [verificador V8](publicacion/verificador/verificador_v8.md) |
| Qué causa qué | V9 | [informe V9](publicacion/informe_v9.md), [verificador V9](publicacion/verificador/verificador_v9.md) |
| Atlas descriptivo, base de datos única, figuras y web | V10 (base ampliada en V11 y V12) | [atlas descriptivo](publicacion/atlas_descriptivo.md), [diccionario de la base](docs/v10/diccionario_base.md) |
| Demografía, hogares, titularidad, oferta, condiciones por origen y turismo | V12 (datos de V11) | [atlas V12](publicacion/atlas_v12.md) |

**Nuevo en V9 (qué causa qué, 15 de octubre de 2026):** diseños de identificación pre-registrados sobre topes y zonas tensionadas, pisos turísticos, inmigración, tipos de interés y hogares. **Ninguno alcanza la capa causal (C3/C3s)**. Se publican como diferencias o asociaciones con todas sus pruebas: [informe](publicacion/informe_v9.md), [tabla](publicacion/tabla_v9.md), [verificador V9](publicacion/verificador/verificador_v9.md), [pre-registro](metodologia/preregistro_v9.md) y página «Qué causa qué» de la web.

**Nuevo en V10 (difusión, sin modelos nuevos):**
- una base de datos única: [diccionario](docs/v10/diccionario_base.md) y datos redistribuibles en `data/base/publica`;
- un [atlas descriptivo](publicacion/atlas_descriptivo.md) de quién soporta el coste de la vivienda y dónde, con sus [tablas en Excel](publicacion/tablas_atlas.xlsx);
- [figuras y mapas](figuras/README.md);
- una [web pública](web/README.md) (prevista en https://phraselium.github.io/vivienda-espana-evidencia/) con panel, mapas, fichas territoriales, verificador y monitor de datos nuevos;
- un [manuscrito en preparación](paper/README.md).

**Empiece por [LEEME_PRIMERO.md](LEEME_PRIMERO.md)**, que propone itinerarios de lectura para ciudadanos, periodistas, revisores y técnicos.

## Qué es
Una base de evidencia sobre la vivienda en España, por provincias, por comunidades autónomas y con un módulo para València. Incluye:
- precios y alquileres triangulados;
- déficit y necesidad de vivienda 2026-2035;
- un atlas econométrico regional;
- simulaciones condicionales de instrumentos, con su dosis y su coste;
- una nota metodológica sobre paneles regionales;
- un verificador de afirmaciones del debate público;
- una atribución por factores y periodos del precio real de compra y del alquiler real (V8), con su informe econométrico y su verificador.

Todo se reproduce sin red tras descargar una vez los datos de terceros que no se redistribuyen (`make datos_terceros`; [docs/v8_1/datos_retirados.md](docs/v8_1/datos_retirados.md)).

## Por qué ha subido (versión interna V8)

- **Lectura no técnica:** [¿Por qué ha subido el precio de la vivienda?](publicacion/por_que_ha_subido.md). **Informe econométrico:** [informe_econometrico_v8.md](publicacion/informe_econometrico_v8.md). **Verificador vigente:** [verificador V8](publicacion/verificador/verificador_v8.md) (las fichas de v5-v7.1 siguen en el [verificador anterior](publicacion/verificador/verificador.md)).
- **Resultado principal:** con las reglas fijadas antes de estimar, ningún factor puede designarse como el más relevante en ninguno de los diez casos (mercado por periodo). Ningún resultado de V8 alcanza C3; la descomposición del SVAR es C3s (condicionada a sus restricciones) y el resto, C4.
- Una página y «lo que sabemos» incluyen un apartado V8, regenerados con `make publicacion`.

Cada resultado se clasifica en una capa de evidencia ([metodologia/capas.md](metodologia/capas.md)):
- **C1 hechos:** al menos dos fuentes;
- **C2 cotas:** supuestos explícitos;
- **C3 efectos:** identificados; ninguno alcanzado;
- **C4 exploratorio.**

Se evalúan afirmaciones e instrumentos, nunca partidos ni personas.

## Estructura

| Carpeta | Qué contiene | Cómo se mantiene |
|---|---|---|
| [publicacion/](publicacion/MANIFIESTO.md) | Lo vigente: una página, lo que sabemos, policy brief, informe técnico, working paper, nota metodológica, artículo del Colegio, ponencia, atlas regional, por qué ha subido (V8), informe econométrico V8, verificadores y cifras_clave.csv | `make publicacion`; nunca a mano (lo comprueba un test) |
| [metodologia/](metodologia/MANIFIESTO.md) | Anexo metodológico, guía del revisor, capas, historial de conclusiones, validación Monte Carlo, pre-registro V7, dosis y coste | `make publicacion` |
| [reproducir/](reproducir/MANIFIESTO.md) | Instrucciones, entorno y versiones, tiempos, ensayo y protocolo de `make evaluate_v7` | `make publicacion` |
| [historico/](historico/INDICE.md) | Documentos de versiones superadas e índice por versión | `git mv`, sin modificar |
| data/base/ | Base única (V10): tabla larga, territorios, variables, geometrías; capa pública en data/base/publica | `make base` |
| output/v10/, figuras/, web/, paper/ | Atlas, figuras con ficha, web estática y manuscrito (V10; §6 con V9) | `make atlas`, `make figuras`, `make web` |
| output/v9/, docs/v9/ | Qué causa qué (V9): diseños D1-D7, pruebas, capas, cotas, verificador; pre-registro y revisiones | `make v9` |
| src/, tests/, output/, docs/, data/ | Código, pruebas, salidas de cada versión, documentación de trabajo y datos | `make all`, `make v7`, `make check` |

El mapa detallado está en [docs/MAPA.md](docs/MAPA.md).

## Cómo reproducir
```bash
python3 -m pip install -r requirements.lock
make all           # v1-v6.3 sin red (unas 2 h)
make v7            # atlas regional y V7.1 (unos 50 min)
make v8            # por qué ha subido (V8): paneles, modelos, atribución, tablas y entregables (unos 20 min)
make base          # V10: base única (DuckDB y Parquet) y geometrías (unos 5 min)
make atlas         # V10: atlas descriptivo (los microdatos se recalculan si están en disco)
make figuras       # V10: figuras y mapas
make web           # V10: web estática en web/_site
make datos_v9      # V9: descarga o verificación de data/raw/v9 (sin red solo verifica)
make v9            # V9: diseños D1-D7, cotas, cifras V9, verificador, textos y Excel (unos 30 min; Honest DiD es lento)
make v12          # V12: demografía, hogares, titularidad y oferta (descriptivo)
make publicacion   # publicacion/, metodologia/ y reproducir/ (y CITATION.cff, .zenodo.json)
make paquete_zenodo  # V13: paquete del depósito en _deposito/ (no versionado)
make check         # ruff, tests, controles de texto, cifras y capas
```
Detalle: [reproducir/instrucciones.md](reproducir/instrucciones.md). La validación limpia de V7 es diferida (2027): [reproducir/evaluacion_2027.md](reproducir/evaluacion_2027.md).

## Cómo citar
Metadatos en [CITATION.cff](CITATION.cff) y .zenodo.json, generados desde proyecto.json con `make metadatos`. DOI: pendiente (depósito en Zenodo).

> Romero, B. (2026). *Vivienda en España: base de evidencia reproducible* (versión 1.0) [software y datos].

## Licencias
- Código (src/, tests/, Makefile): MIT.
- Textos, tablas y figuras propios (docs/, output/, publicacion/, metodologia/, reproducir/, historico/): CC BY 4.0.
- Datos de terceros (data/raw/): conservan la licencia de su fuente; véase [docs/v5/licencias_datos.md](docs/v5/licencias_datos.md).

Texto completo en [LICENSE](LICENSE).

## Uso de IA
El código y los borradores se elaboraron con agentes de IA (Claude) bajo la supervisión del autor, que revisa y responde del contenido. La declaración completa está en [DECLARACION_IA.md](DECLARACION_IA.md) (también en el apéndice C del [working paper](publicacion/working_paper.md) y en README_REPLICACION.md §5).

## Erratas y cambios
- Correcciones de resultados publicados: [ERRATA.md](ERRATA.md).
- Cambios por versión: [CHANGELOG.md](CHANGELOG.md).
- Versiones superadas: [historico/INDICE.md](historico/INDICE.md).
