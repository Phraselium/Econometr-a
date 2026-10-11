# Backlog v6.1 (K6)

Fuentes:
- hallazgos medios y bajos de K4a, K4c/K4d y la revisión tras K2;
- cifras no reconstruibles en K4b;
- lo abierto de docs/v5/backlog.md.

Coste: S < 20k tokens o 1 h de autor · M 20-80k · L > 80k o datos nuevos.

## Cerrados en v6.1

| id | Qué | Cómo |
|---|---|---|
| K4a-01, K4a-02 | Redondeo de recuentos en cifras_clave; fianzas de Incasòl | Corregidos, con entrada en ERRATA |
| K4a-03 | Dos versiones de la necesidad (B1 y T3) en el informe | Rótulo de definición en el informe técnico y el policy brief. El recálculo queda abajo |
| K4a-07 | Pliegues omitidos en la validación fuera de muestra de CA, sin contar | Ahora se cuentan y se informan en output/v5/CA/resultado.json: 0 de 30 |
| K4a-11 | Faltaban tests de v5, v5.1 y v6 | 31 tests K4a y 1 K4c |
| R-08 | A23-A10: la provincia de Valencia quedaba sin peso | Corregido, con entrada en ERRATA |
| R-09 | Origen de la serie de Notariado en A23-P2 | Está versionada: data/raw/pdf/notariado_cgn_extranjeros_semestral.csv |
| R-10 | Descripción de las fuentes del déficit; constante de la EPA | Texto corregido, con entrada en ERRATA |
| K4d | Enlaces rotos, versiones, declaración de IA, marcas de referencias | Hecho (docs/v6_1/auditoria_K4cd.md) |
| BK-044, BK-045, BK-046, BK-047 | — | Ya cerrados en v5 |

## Abiertos

| id | Qué | Por qué sigue abierto | Coste |
|---|---|---|---|
| K4a-03b | Recalcular D2 sobre la necesidad T3 de v5.1 | Cambia el reparto por clase; requiere nueva revisión de D2 | M |
| K4a-04 | 48 filas de cifras_clave usan min/max con otro sentido (crítico, RIC, extremos) | Hay que separar en columnas ref_min/ref_max y adaptar render y las plantillas. Un test vigila que no aparezcan filas nuevas | M |
| K4a-05 | Fianza media de la GVA: media bruta en m0_run frente a truncada en a23 | Cambiaría paneles sellados de v6 (contratos nuevos, no evaluados) y su hash. Diferencia de +0,1 a +0,5 % | S |
| K4a-06 | SEED de econ_utils (20261009) | Afecta solo a v1, que es solo lectura. Anotado | — |
| K4a-08 | El adaptador «188-506 mil» de cifras_clave se extrae de un texto | Leer un campo numérico de v4 M2 | S |
| K4a-10 | Comprobaciones tautológicas en control_sumas | Hay que rediseñar las comprobaciones de v5.1 | M |
| K4b-NR | 5 cifras no reconstruibles solo con el texto publicado: D1-H11/H12, B1-H1, latente_convivencia y B4-vut | Escribir un anexo metodológico con fórmulas y parámetros (clases A4, rejilla εd, componentes por provincia, fuente del latente, conversión de VUT) | M |
| K4b-dh | dh_2125 mezcla el stock a 1 de enero (ECP) con la media anual (EPA) | Declararlo en la ficha o armonizar la ventana | S |
| K4c-26 | 26 cifras del verificador no están en cifras_clave | Llevarlas a hechos.json del verificador | S |
| K4d-ref | 50 referencias con «cuartil no verificado» y 76 NO VERIFICADA | Scimago devuelve 403 desde la sesión: lo verifica el autor (tareas_autor §8) | S (autor) |
| R-05 | El factor común de m4_lineas_base se calcula antes de filtrar por año (sin efecto hoy) | El script no se puede volver a ejecutar (aperturas únicas). Anotado | — |
| K2-49 | Reestimar la inmigración con la muestra de 49 provincias de v2 | Exige mirar provincias selladas en v6; solo es posible con una muestra nueva | L |
| BK-E3 | Ampliar los artículos | Presupuesto del redactor | M |
| BK-050, BK-051, BK-042, BK-038 | Heredados de v5 | Sin cambio | S-M |
| BK-014, BK-017 | Temporada y habitaciones; MESVAL | Sin datos oficiales / datos privados | L |
