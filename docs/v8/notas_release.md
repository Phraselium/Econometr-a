# Notas para la release del pre-registro V8 (tarea del autor)

El pre-registro de V8 (docs/v8/hipotesis.md) solo tiene fecha verificable cuando se publica fuera del entorno de trabajo, porque el remoto rechaza las etiquetas.

1. Comprueba que `git show --no-patch prereg-v8` apunta al commit del pre-registro.
2. Publica la etiqueta y crea una release de GitHub, titulada «Pre-registro V8 (atribución por periodos)». Activa Zenodo para obtener el DOI.
3. Anota aquí la fecha del DOI en `fecha_verificable: AAAA-MM-DD`.
4. Antes de la release, F4 congela las predicciones (`sha256_predicciones_v8`, más abajo). `make evaluate_v8` las evaluará una sola vez con los datos 2026T3-2027T2.

prereg_v8_commit_local: 91e618b (etiqueta local `prereg-v8`)
fecha_verificable: PENDIENTE
sha256_predicciones_v8: 89c5feb6913b52b424688daef7fd3363e11d64654179e8bf63c2de60bc664863
