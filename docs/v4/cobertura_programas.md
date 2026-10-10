# Cobertura de la recogida de medidas (M5a, 2026-10-10)

Documentos anonimizados D1-D9, en el orden en que aparecen en `data/raw/v4/medidas_programas.csv` (la correspondencia solo se obtiene del CSV). Páginas leídas: aproximadas, contadas como páginas visualizadas (índice incluido). Totales: del propio documento, de su índice o de prensa, cuando se conocen.

| Doc | Tipo de fuente | Páginas leídas / totales | Cómo se localizó la parte leída | Medidas en el CSV |
|---|---|---|---|---|
| D1 | copia no oficial alojada por un medio | ≈14 / ≈272 (según prensa) | apartado «Vivienda» del bloque social (pp. 207-220 impresas) | 15 |
| D2 | copia no oficial alojada por un medio | ≈13 / ≈105 (índice) | índice, objetivo de infraestructuras y vivienda, objetivo de propiedad y fiscalidad (pp. 3-5, 21-22, 31-33, 78-79) | 8 |
| D3 | copia no oficial alojada por un medio | ≈13 / ≈180 (según prensa) | índice y apartado «Derecho a la vivienda» (pp. 72-76 impresas); sondeos pp. 61, 68, 95 | 22 |
| D4 | web del grupo | ≈6 / ≈132 | índice y apartado «Habitatge» (pp. 113-114) | 9 |
| D5 | web del grupo | 5 / 16 | pp. 2-6 (preámbulo y apartado «Justicia social: vivienda») | 3 |
| D6 | web del grupo | ≈5 / ≥50 (índice llega a p. 50) | índice y apartado de políticas sociales (pp. 45-47) | 2 |
| D7 | web del grupo | ≈7 / ≈67 | índice y apartado «Vivenda» (pp. 14-16) | 9 |
| D8 | web del grupo | 6 / 6 | documento completo | 2 |
| D9 | copia no oficial alojada por un medio | ≈37 / no registrado | pp. 40-76 (segunda pasada, texto extraído) | 18 |

Documentos no accesibles: 2 programas de grupos con representación (no localizados) y las proposiciones de ley de la XV legislatura (no consultadas). Ver `docs/v4/fuentes_fallidas.md`.

## Términos de búsqueda y protocolo
- Protocolo pedido: búsqueda por palabras clave sobre el TEXTO COMPLETO de cada documento (vivienda, alquiler, suelo, hipoteca, ocupación, desahucio, turístic, joven, construcción).
- **No se pudo aplicar.** Las herramientas disponibles solo muestran los PDF como imágenes por página (la descarga es binaria y no hay extractor de texto). Una búsqueda por palabras clave exige texto extraído. El único documento con texto extraído fue D9 (segunda pasada).
- Lo que se hizo en D1-D8: localizar el apartado de vivienda por el índice y leerlo entero, más las páginas con medidas conexas que señala el índice (suelo, ocupación, fiscalidad). Es una lectura por índice, no una búsqueda exhaustiva.
- Consecuencia: los recuentos de documentos por instrumento son **cotas inferiores** y dependen de la cobertura. Una medida de vivienda fuera de las páginas leídas no está recogida. Para cerrar el hueco hace falta un extractor de texto (por ejemplo `pdftotext`) en una pasada posterior; no se intentó sortear la herramienta.
- Medidas por documento: de 2 a 22. La diferencia refleja en parte la extensión del apartado de vivienda de cada programa y en parte la cobertura de la lectura.
