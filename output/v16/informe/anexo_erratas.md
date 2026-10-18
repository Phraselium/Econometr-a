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
- {{V72-GSADF-niveles-bh}} series de niveles explosivas tras el ajuste;
- {{V72-GSADF-ccaa-bh}} series autonómicas;
- {{V72-GSADF-ratios-bh}} cocientes nacionales.

También se aumentaron las simulaciones de 499 a 4.999, porque con 499 los recuentos cambiaban con la semilla.

**La conclusión de fondo no cambia.** Con estos contrastes no se puede afirmar que haya una burbuja ni que no la haya.
- Que no haya exuberancia estadística no demuestra que el precio esté alineado con sus fundamentales: el contraste tiene poca potencia con 78 trimestres.
- Que la hubiera tampoco identificaría una burbuja.

**El mismo error en v6.** Estaba también en una copia del código de v6. Corregido, el recuento de v6 sigue en {{V72-GSADF-ccaa-v6}} de 11 comunidades; solo cambian cuatro valores críticos.

## Resto de erratas aplicadas en V16

| Cifra o resultado | Qué estaba mal | Qué cambia |
|---|---|---|
| V8-M5, instrumento Bartik (8 filas de tablas_v8.xlsx) | Navarra y La Rioja entraban con cuota 0 por falta de datos de 2008 | Se excluyen; cambian solo esas 8 filas, ninguna cifra de cifras_clave |
| V8-H8-9 | Periodo mal rotulado | 2006T1-2026T2; el valor no cambia |
| V8-QNA-pp-c-P5 | Banda aproximada y media sin la mediana al lado | Banda exacta, mediana y sensibilidad al tipo del Banco de España |
| V8-VOTOS-c-P5 | Regla Y10 sin publicar | Publicada; el valor no cambia |
| V8-M1-cuota-c-P5 | Longitud del bloque no fijada en la ficha | Nota con el resultado alternativo; el valor no cambia |
| T4-H2 (mínimo) | Convención no escrita | Se documenta y se dan los dos mínimos; el valor no cambia |
