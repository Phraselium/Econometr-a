# Auditoría crítica v6.1 (K4), consolidada

Fecha: 2026-10-11. Fuentes:
- docs/v6_1/auditoria_K4a.md: código y estadística, subagente independiente;
- docs/v6_1/doble_implementacion.md: K4b, sin ver el código original;
- docs/v6_1/auditoria_K4cd.md: coherencia de cifras, documentación y publicación;
- docs/v6_1/revision_K2.md: revisor independiente;
- docs/v6_1/informe_arbitro_*.md: K5.

El efecto en las cifras publicadas se refiere a output/v5/cifras_clave.csv y a los entregables.

## Recuento por severidad (hallazgos verificados)

| Severidad | Nº | Corregidos | Cambian cifra publicada |
|---|---|---|---|
| Crítica | 0 | — | — |
| Alta | 5 | 5 | 2 (K4a-01, R-08) |
| Media | 13 | 9 | 0 (R-10 corrige una descripción, no una cifra) |
| Baja | 12 | 6 | 0 |

## Altas

| id | Ubicación | Hallazgo | Efecto en conclusiones | Corrección |
|---|---|---|---|---|
| K4a-01 | src/v5/cifras_clave.py | `%.6g` redondeaba los recuentos de 1.000.000 o más | 33 campos cambian, hasta 5 unidades; ninguna conclusión | `%.10g`; entrada en ERRATA |
| K4a-02 | src/v6/m0_run.py (`incasol`) | Las fianzas de Incasòl se sumaban por triplicado y la cuota «>600 €» mezclaba unidades | Solo el descriptivo de M1A; ningún modelo sellado | Filtro de año completo y de unidad; ERRATA; D4 (sha256 de dos paneles no evaluados) |
| K4a-03 | Informe técnico §7, policy brief | Dos versiones de la necesidad (B1 y T3) en el mismo informe | Ninguna; ambigüedad de lectura | Rótulo de definición; el recálculo queda en el backlog (K4a-03b) |
| R-08 | src/v5/a23_run.py | `fillna(1.0)` dejaba a Valencia sin peso en el IPVA de contratos nuevos | A23-A10 pasa de 26,6 % (22,4-30,8) a 27,7 % (24,6-30,8). La conclusión no cambia: los nuevos suben más que los vigentes | Relleno con la media de la CCAA; ERRATA. Confirmado por K4b (24,7) |
| K4d-06 | docs/literatura.md | 60 referencias con DOI sin marca de cuartil | Ninguna | Marcadas: 10 VERIFICADA y 50 «cuartil no verificado» |

## Medias y bajas

Detalle, ubicación y coste en los informes parciales.

- **Medias corregidas:**
  - R-10, descripción de las fuentes del déficit y constante de la EPA (ERRATA);
  - K4c-01 y K4c-02;
  - K4d-01, K4d-03, K4d-04 y K4d-08 (enlaces, versiones y `make check` en un clon limpio);
  - R-01 y R-02 (inferencia de K1: permutación exacta, DM por periodo, PROV_PRECIO_ANUAL «frágil»).
- **Medias abiertas** (en docs/v6_1/backlog.md):
  - K4a-04, min/max con otro sentido;
  - K4a-05, fianza GVA bruta o truncada;
  - K4c-03, 26 cifras del verificador;
  - K4d-07, cuartiles: tarea del autor.
- **Bajas corregidas:** K4a-07 (0 de 30 pliegues omitidos), K4a-09, K4a-11 (tests), R-03, K4c-05 y K4c-06.
- **Bajas anotadas:** K4a-06 (semilla de v1), K4a-08, K4a-10, R-04, R-05, R-06 (sensibilidad hecha), K4c-04 y K4c-07.

## Doble implementación (K4b)

| Resultado | Nº | Cifras |
|---|---|---|
| Coinciden | 6 | A23-A2, terminadas_1924, E-B1-F, B1-H4, R1C-001 y, tras la corrección R-08, A23-A10 |
| Parciales, con explicación | 4 | deficit_2124_c1/c2 (definición del rango), dh_2125 (stock frente a media anual), A23-P2 (central: falta Notariado en la réplica) |
| No reconstruibles solo con el texto | 5 | D1-H11, D1-H12, B1-H1, latente_convivencia, B4-vut: falta un anexo metodológico (backlog K4b-NR) |

## Tests añadidos

- tests/test_k4a_cifras.py y tests/test_k4a_paneles.py: 31 pruebas.
  - Unicidad de ids y de claves de los paneles.
  - Rangos (0-100 %, precios positivos, min ≤ valor ≤ max salvo una lista cerrada).
  - Reconciliaciones hechos.json → cifras_clave → entregables renderizados.
  - Control de sumas.
  - Incasòl solo con el año completo.
  - Paneles provinciales sin huecos.
- tests/test_k4c_cifras.py: ninguna cifra huérfana nueva en los entregables principales.
- Scripts en make: k4c_cifras.py (cifras de los entregables frente a cifras_clave) y k4d_docs.py (enlaces, versiones y referencias).
