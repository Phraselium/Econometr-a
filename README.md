# Vivienda en España: base de evidencia reproducible

**Autor:** Borja Romero, economista (firma individual, independiente). **Versión:** v8.1 (14 de octubre de 2026): v8 es la versión de referencia de modelización (por qué ha subido el precio de la vivienda), con coherencia de redacción y tablas, capa de consulta ([consulta/](consulta/LEEME_ASISTENTE.md)) y retirada de datos de terceros, sin análisis nuevo. Versiones cerradas: v1-v8.0. La v7.2 queda como referencia anterior y la v6.2 es histórica ([historico/INDICE.md](historico/INDICE.md)).

**Repositorio:** https://github.com/Phraselium/vivienda-espana-evidencia (antes Phraselium/Econometr-a; GitHub redirige el nombre antiguo). **DOI:** pendiente (Zenodo).

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

## Versión vigente: v8 (por qué ha subido)

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
| src/, tests/, output/, docs/, data/ | Código, pruebas, salidas de cada versión, documentación de trabajo y datos | `make all`, `make v7`, `make check` |

El mapa detallado está en [docs/MAPA.md](docs/MAPA.md).

## Cómo reproducir
```bash
python3 -m pip install -r requirements.lock
make all           # v1-v6.3 sin red (unas 2 h)
make v7            # atlas regional y V7.1 (unos 50 min)
make v8            # por qué ha subido (V8): paneles, modelos, atribución, tablas y entregables (unos 20 min)
make publicacion   # publicacion/, metodologia/ y reproducir/
make check         # ruff, tests, controles de texto, cifras y capas
```
Detalle: [reproducir/instrucciones.md](reproducir/instrucciones.md). La validación limpia de V7 es diferida (2027): [reproducir/evaluacion_2027.md](reproducir/evaluacion_2027.md).

## Cómo citar
Metadatos en [CITATION.cff](CITATION.cff) y .zenodo.json. DOI: pendiente (depósito en Zenodo).

> Romero, B. (2026). *Vivienda en España: base de evidencia reproducible* (versión 7.2) [software y datos].

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
