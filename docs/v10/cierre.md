# Cierre de V10-DIFUSIÓN (2026-10-14)

**Clon limpio** (`git clone` de la rama en un directorio temporal) a partir del commit 126356b:
- se copia el seccionado del INE (60 MB, no versionado; `src/v10/fetch_geo.py` lo descarga);
- se copian los 77 ficheros de terceros retirados. Equivale a `make datos_terceros`, que en el clon no detectó red y solo verificó.

| Orden | Resultado |
|---|---|
| `make base` | 10,1 M filas públicas; capa pública idéntica en contenido a la de la copia de trabajo; escritura determinista (mismo sha256 en dos ejecuciones) |
| `make figuras` | 14 figuras |
| `make web` | 320 páginas, 311 fichas territoriales, 27 indicadores, 4 mapas (49 MB) |
| `make check` | 352 tests aprobados; check_texto, check_v5, check_v6 y check_v8 con 0 errores; rc = 0 |

**Diferencias tras el cierre.** Solo cambió consulta/version.json, con el commit del último cambio de output/. Se regeneró con `make consulta` en el commit final.

**Revisión independiente.** Revisor opus, unos 90.600 tokens (tope de 100.000). Veredicto REHACER: 2 bloqueantes y 4 importantes, todos corregidos (D10).
- En el cierre aparecieron además un fallo de determinismo (claves EMAL) y la escritura no determinista de la base; ambos se corrigieron (D11).
