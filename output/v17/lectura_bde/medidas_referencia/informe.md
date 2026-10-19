# V17 · B5 · Medidas de referencia del Banco de España

Análisis a posteriori (V17). Generado por src/v17/f2_medidas_referencia.py. Las cifras son estadísticas oficiales de fuente única (lectura «OF»); en la capa del proyecto son C4. No cambian ninguna cifra publicada.

## Indicadores del Banco de España

La lectura del Banco de España compara el último dato con su media histórica y con el máximo del ciclo anterior (2007). Una desviación positiva del precio/renta o del esfuerzo indica menor accesibilidad; una rentabilidad por alquiler menor que su media indica precios altos frente al alquiler.

| Indicador | Último | Fecha | 2007 | 2019 | Media histórica (años) | Desviación frente a la media | Uso |
|---|---|---|---|---|---|---|---|
| Precio de la vivienda / renta bruta por hogar (años) | 8,36 | 2026-06 | 9,36 | 6,87 | 6,04 (1987-2025) | 38,4 % | sobrevaloración y acceso |
| Esfuerzo teórico anual sin deducciones (% de la renta) | 38,01 | 2026-06 | 53,16 | 30,25 | 39,74 (1987-2025) | -4,4 % | acceso |
| Rentabilidad bruta por alquiler, doce meses (%) | 2,84 | 2026-09 | 2,94 | 3,83 | 4,69 (1987-2025) | -39,4 % | sobrevaloración (inversa del precio/alquiler) |
| Relación préstamo-valor (RPV o LTV) de transacción (%) | 63,70 | 2026-06 | 63,50 | 64,45 | 62,23 (2004-2025) | 2,4 % | crédito |
| Préstamos con RPV mayor que 80 % (% del total) | 9,60 | 2026-06 | 14,30 | 12,12 | 12,49 (2004-2025) | -23,2 % | crédito |
| Saldo del crédito a hogares para vivienda (% del PIB) | 30,24 | 2026-06 | 59,00 | 42,11 | 42,40 (1995-2025) | -28,7 % | crédito |
| Crédito a hogares para adquisición de vivienda, tasa interanual (%) | 3,72 | 2026-08 | 17,00 | -1,17 | 7,68 (1995-2025) | -51,6 % | crédito |
| Ratio de dudosidad del crédito a hogares para vivienda (%) | 1,45 | 2026-06 | 0,59 | 3,77 | 2,66 (1988-2025) | -45,4 % | crédito |

## Compras sin hipoteca (aproximación)

Proporción de compraventas de viviendas que no tienen una hipoteca sobre vivienda constituida el mismo año. Es una COTA INFERIOR: la estadística de hipotecas incluye préstamos no ligados a una compra (refinanciaciones, autopromoción), así que 1 - hipotecas/compraventas subestima las compras al contado. La serie del Notariado, que las mide directamente, queda como tarea del autor (docs/v18/tareas_autor.md). Hasta 2011 se constituían más hipotecas sobre viviendas que compraventas (refinanciaciones, autopromoción y el desfase entre escritura e inscripción), así que en esos años la aproximación no es informativa y no se usa.

| Año | Hipotecas sobre viviendas | Compraventas de viviendas | Sin hipoteca (cota inferior) |
|---|---|---|---|
| 2007 | 1.238.890 | 775.300 | no informativa |
| 2008 | 836.419 | 552.080 | no informativa |
| 2009 | 650.889 | 413.393 | no informativa |
| 2010 | 607.535 | 439.591 | no informativa |
| 2011 | 408.461 | 359.824 | no informativa |
| 2012 | 273.873 | 318.534 | 14,0 % |
| 2013 | 199.703 | 312.593 | 36,1 % |
| 2014 | 204.302 | 318.830 | 35,9 % |
| 2015 | 246.767 | 355.556 | 30,6 % |
| 2016 | 282.707 | 405.385 | 30,3 % |
| 2017 | 312.843 | 467.644 | 33,1 % |
| 2018 | 348.326 | 517.984 | 32,8 % |
| 2019 | 361.291 | 505.467 | 28,5 % |
| 2020 | 337.752 | 420.238 | 19,6 % |
| 2021 | 418.058 | 566.485 | 26,2 % |
| 2022 | 464.107 | 650.265 | 28,6 % |
| 2023 | 380.966 | 583.651 | 34,7 % |
| 2024 | 425.522 | 640.401 | 33,6 % |
| 2025 | 498.429 | 711.543 | 30,0 % |

## Otras medidas de B5 ya publicadas en el repositorio

- **Precio ajustado por calidad (IPV del INE) como medida principal.** La variación real 2019-2025 es la cifra V16-HEC-INTL-RHP-ES-2019-2025, y la del precio medio por m² tasado está en el informe integral (Parte I). El sesgo de composición de los precios medios se analiza en la fase 3 (fila «Precio»).
- **Precio deflactado por renta.** Precio/renta disponible de Eurostat: V16-HEC-INTL-HPI_YDH-ES-2019-2025 y 2007-2025.
- **Sobrevaloración.** GSADF corregido (V7.2, B-4: R1B-G-*) y factor común de V16 (Q9-g, pista no confirmada). El Banco de España estima la sobrevaloración con sus propios modelos (docs/v17/referencias/bde_bce_documentos.md).
