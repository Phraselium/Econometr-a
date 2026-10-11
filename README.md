# Vivienda en España: base de evidencia reproducible

**Autor:** Borja Romero, economista (firma individual, independiente). **Versión:** v6.1 (borrador, pendiente de cierre; 11 de octubre de 2026). Última versión cerrada: v6.0 (alquiler y compraventa; docs/v6/plan.md). Plan de v6.1: docs/v6_1/plan.md.

## Qué es
Una base de evidencia sobre la vivienda en España, por provincias y con un módulo para València: precios y alquileres triangulados, déficit y necesidad de vivienda 2026-2035, diferencias territoriales, comparación europea, una matriz de instrumentos de política y un verificador de afirmaciones del debate público. Todo se reproduce con los datos incluidos en el repositorio y sin conexión a la red.

Cada resultado se clasifica en una de cuatro capas de evidencia:
- **C1 hechos:** al menos dos fuentes;
- **C2 cotas:** intervalos con supuestos explícitos (Manski);
- **C3 efectos:** identificados, con pretendencias, placebos, sensibilidad y muestra sellada;
- **C4 exploratorio.**

Ningún resultado se presenta en una capa superior a la que alcanza. Se evalúan afirmaciones e instrumentos, nunca partidos ni personas.

## Qué se puede afirmar
- Resumen por capas: [output/v5/lo_que_sabemos.md](output/v5/lo_que_sabemos.md).
- Una página: [output/v5/una_pagina.md](output/v5/una_pagina.md).
- Informe técnico, working paper y policy brief: output/v5/. Todas las cifras de estos documentos salen de [output/v5/cifras_clave.csv](output/v5/cifras_clave.csv), con la fecha de cada dato.
- Verificador de afirmaciones: output/v5/verificador/.

El mapa de carpetas, con lo vigente y lo histórico, está en [docs/MAPA.md](docs/MAPA.md).

## Cómo reproducir
```bash
python3 -m pip install -r requirements.lock
make all     # datos en caché → paneles → modelos v1-v5.1 → entregables → verificador
make check   # ruff, tests y controles de texto, cifras y capas
```
Detalle (software, tiempos, orden de los programas, correspondencia entre salidas y scripts, fuentes): [README_REPLICACION.md](README_REPLICACION.md).

## Cómo citar
Metadatos en [CITATION.cff](CITATION.cff) y .zenodo.json. DOI: pendiente (depósito en Zenodo).

> Romero, B. (2026). *Vivienda en España: base de evidencia reproducible* (versión 6.1, borrador) [software y datos].

## Licencias
- Código (src/, tests/, Makefile): MIT.
- Textos, tablas y figuras propios (docs/, output/): CC BY 4.0.
- Datos de terceros (data/raw/): conservan la licencia de su fuente; véase [docs/v5/licencias_datos.md](docs/v5/licencias_datos.md).

Texto completo en [LICENSE](LICENSE).

## Uso de IA
El código y los borradores se elaboraron con agentes de IA (Claude) bajo la supervisión del autor, que revisa y responde del contenido. La declaración completa está en [DECLARACION_IA.md](DECLARACION_IA.md) (también en el apéndice C de output/v5/working_paper.md y en README_REPLICACION.md §5).

## Erratas y cambios
- Correcciones de resultados publicados: [ERRATA.md](ERRATA.md).
- Cambios por versión: [CHANGELOG.md](CHANGELOG.md).
- Salidas superadas de v3 y v4: [archive/](archive/README.md).
