## Qué se reproduce y qué no

- **Con `make datos`** (depósito de Zenodo): se recalculan las cifras que no usan datos de terceros, la base pública, las figuras, la web y los entregables (`make publicacion`). Pasan {{pasados}} tests.
- **Con `make datos_terceros`** (Notariado, Registradores): se recalculan las series y los modelos que los usan. Sin esos datos se omiten {{omitidos}} tests, cada uno con su motivo.
- **No se puede reproducir públicamente:** la muestra sellada, cuyas evaluaciones ya hechas están en output/, ni las series que proyecto.json (`terceros_1_0`) no redistribuye.
- Cifras que dependen de terceros y no publicadas: docs/v14/cifras_terceros.md y publicacion/cifras_no_publicadas_1_0.csv.
- Explicación: [reproducir/instrucciones.md](reproducir/instrucciones.md#árbol-público-de-la-versión-10-repositorio-vivienda-espana-evidencia).
