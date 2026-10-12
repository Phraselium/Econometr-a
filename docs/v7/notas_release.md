# Notas para la release del pre-registro V7 (tarea del autor)

El pre-registro de V7 (docs/v7/hipotesis.md) y la congelación de los modelos de predicción (output/v7/R5/modelos_congelados.json) solo tienen fecha **verificable por terceros** cuando se publican fuera de esta sesión. La etiqueta local `prereg-v7` no basta, porque el remoto rechaza las etiquetas.

## Pasos
1. Desde una copia con permisos de escritura en GitHub, comprueba que `git show --no-patch prereg-v7` apunta al commit del pre-registro.
2. Publica la etiqueta (`git push origin prereg-v7`) y crea una **release de GitHub** sobre ella, titulada «Pre-registro V7 (validación diferida)».
3. Activa Zenodo para obtener un DOI de esa release. La fecha del DOI es la fecha verificable del pre-registro.
4. Anota esa fecha aquí: `fecha_verificable: AAAA-MM-DD`.
5. A partir de esa fecha, los datos publicados después (IPV y EPA de 2026T3 en adelante, IPC alquiler, hipotecas y compraventas por CCAA; anuales de 2026) son la muestra limpia.
6. Cuando estén publicados al menos 2026T3-2027T2 (hacia el verano de 2027), ejecuta **una sola vez**, con red: `make evaluate_v7`.
   - El objetivo comprueba que el sha256 de la congelación coincide con el anotado abajo y registra la apertura en docs/v7/evaluate_v7_accesos.md antes de evaluar.
   - Si ya hay una apertura, se niega a repetir.
7. Publica el resultado (output/v7/evaluate/resultado.json), sea favorable o no.

## Datos de la congelación (los rellena el cierre de R5)
sha256_modelos_congelados: PENDIENTE
fecha_verificable: PENDIENTE
