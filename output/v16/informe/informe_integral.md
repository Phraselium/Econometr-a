# Vivienda en España: informe integral (V16)

Informe integral de la versión V16 del proyecto (docs/v16/plan.md, fase 7). Toda cifra procede de output/v5/cifras_clave.csv, con su
capa (C1 hechos con al menos dos fuentes; C2 cotas; C3 y C3s efectos; C4 exploratorio). Los resultados de V15 y V16 tienen
pre-registro interno, sin sello de tiempo externo (etiquetas prereg-v15 y prereg-v16 en el remoto). Generado por src/v16/f7_informe.py;
no se edita a mano.


# Anexo · Erratas de la 1.0 corregidas en V16

Fuente única: ERRATA.md, con los valores de antes y de después y la huella de cada fila cambiada de cifras_clave. Ninguna corrección sube una capa ni cambia una conclusión de la 1.0.

## La «exuberancia» del precio (GSADF), explicada sin tecnicismos

**Qué decía la 1.0.**
- Tras el ajuste por comparaciones múltiples, los niveles de precio nacionales (2 de 2 series) y 7 de las 34 series autonómicas eran «explosivos».
- Los cocientes entre el precio y sus fundamentales (renta, alquiler, tipos de interés) no lo eran.

**Por qué era incorrecto.** El programa tenía dos errores.
- **E1.** El contraste compara cada serie con miles de series simuladas sin burbuja. Para simularlas hay que elegir cuántos trimestres pasados se tienen en cuenta. La regla que lo elegía comparaba modelos estimados con distinto número de datos, y eso la sesgaba.
- **E2.** La serie del IPV de Navarra se cortaba en 2014, porque al programa le faltaba otra serie de Navarra en 2015-2018.

**Cómo se detectó.** En V16 se rehicieron las cifras de la 1.0 sin mirar el código original (réplica ciega). Al comparar, estas no coincidían, y la reconciliación encontró los dos errores.

**Qué da el cálculo corregido:**
- 0 series series de niveles explosivas tras el ajuste;
- 0 series series autonómicas;
- 0 series cocientes nacionales.

También se aumentaron las simulaciones de 499 a 4.999, porque con 499 los recuentos cambiaban con la semilla.

**La conclusión de fondo no cambia.** Con estos contrastes no se puede afirmar que haya una burbuja ni que no la haya.
- Que no haya exuberancia estadística no demuestra que el precio esté alineado con sus fundamentales: el contraste tiene poca potencia con 78 trimestres.
- Que la hubiera tampoco identificaría una burbuja.

**El mismo error en v6.** Estaba también en una copia del código de v6. Corregido, el recuento de v6 sigue en 0 CCAA de 11 comunidades; solo cambian cuatro valores críticos.

## Resto de erratas aplicadas en V16

| Cifra o resultado | Qué estaba mal | Qué cambia |
|---|---|---|
| V8-M5, instrumento Bartik (8 filas de tablas_v8.xlsx) | Navarra y La Rioja entraban con cuota 0 por falta de datos de 2008 | Se excluyen; cambian solo esas 8 filas, ninguna cifra de cifras_clave |
| V8-H8-9 | Periodo mal rotulado | 2006T1-2026T2; el valor no cambia |
| V8-QNA-pp-c-P5 | Banda aproximada y media sin la mediana al lado | Banda exacta, mediana y sensibilidad al tipo del Banco de España |
| V8-VOTOS-c-P5 | Regla Y10 sin publicar | Publicada; el valor no cambia |
| V8-M1-cuota-c-P5 | Longitud del bloque no fijada en la ficha | Nota con el resultado alternativo; el valor no cambia |
| T4-H2 (mínimo) | Convención no escrita | Se documenta y se dan los dos mínimos; el valor no cambia |


# Anexo · Reproducibilidad: réplica ciega de la 1.0 y de los resultados de V15-V16

## Réplica ciega de las cifras de la 1.0 (K19)

**Qué se hizo.** Se rehicieron las 31 cifras de la página resumen (una_pagina), entre ellas las 7 C1 vigentes.
- Cada una se reimplementó desde data/raw y su ficha metodológica, sin leer el código que la produjo (output/v16/replica/v10_*).
- El cegado fue parcial: en algunos lotes el replicador vio el valor publicado antes de estimar. Consta en cada resultado.json.

| Resultado | Cifras | Cuáles |
|---|---|---|
| Coinciden a la primera | 19 | Las 7 C1, E-T7 (2), L3 (2), E-B1-F, V10-ATL-A1, V72-GSADF-ccaa-v6, V72-GSADF-tipos-p05, V71-S3 (2), V8-OBS (2) |
| Coinciden tras completar la ficha (el original era correcto; faltaba un detalle por escribir) | 8 | T3-H5b, T4-H2, T4-H3, V71-S3-R6, V8-H8-9, V8-M1-cuota-c-P5, V8-QNA-pp-c-P5, V8-VOTOS-c-P5 |
| Discrepan por un error de código del original | 4 | V72-GSADF-ccaa-bh, -niveles-bh, -ratios-bh y -ratios-p05 |

**Errores encontrados y corregidos.** Valores de antes y de después en ERRATA.md y en el anexo de erratas.
- **GSADF de V7.2** (E1 y E2). El mismo E1 estaba en la copia de v6. Corregidos: los recuentos tras el ajuste de niveles y comunidades pasan a 0, y los de v6 no cambian.
- **V8-M5** (auditoría del alcance de los errores de V16). Navarra y La Rioja tenían cuota 0 en el instrumento Bartik y ahora quedan fuera.

## Réplica ciega de los resultados citables de V15 y V16 (K16 y K18)

| Resultado | Hallazgo | Corrección |
|---|---|---|
| Q3-b | El núcleo de Conley contaba dos veces la diagonal | Corregido; Conley queda NO APTO en el Monte Carlo y Q3-b se cita solo como estimación puntual |
| H4 | Municipios sin población en el año base con instrumento 0, sin declararlo | Fuera de la muestra (N 13.442 → 13.417) |
| H5 | Primer origen desplazado, el AR(4) usaba el propio objetivo y la desestacionalización usaba datos posteriores al origen | Corregidos; la combinación sigue sin superar al AR(4) |
| Q6-p | Diferencias entre años no consecutivos | Corregido; deja de ser pista y queda «no concluyente» |
| Q9-g, E3, H1, Q2a, H3 | Coinciden | — |

Ninguna corrección se eligió por su resultado: todas son errores frente a la ficha o frente a las reglas del proyecto.
