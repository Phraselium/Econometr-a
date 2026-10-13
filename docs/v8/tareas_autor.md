# Tareas del autor tras V8 (por urgencia)

Sustituye a docs/v7_1/tareas_autor.md, que queda como histórico para lo que no se repite aquí. Nada de esta lista lo puede hacer el agente: requiere credenciales, firma o juicio del autor.

## 1. Etiquetas, releases y Zenodo (urgente: antes de que se publique 2026T3)

El remoto de esta sesión rechaza las etiquetas (el push termina con «remote end hung up»). Quedan solo en local: prereg-v2, prereg-v3, prereg-v5, prereg-v6, prereg-v7, prereg-v8, v5.0, v5.1, v6.0, v6.1, v6.2, v7.0, v7.1 y v7.2.

1. Desde una copia con permisos, publica en este orden `prereg-v8` (91e618b), `v7.2` y la etiqueta de cierre de V8 (créala sobre el commit de cierre: `git tag v8.0 <commit>`). También las pendientes de V7 (docs/v7_1/tareas_autor.md).
2. Crea la release del pre-registro V8 y la de V8 y activa Zenodo. Anota la fecha del DOI en docs/v8/notas_release.md (`fecha_verificable:`). Sin esa fecha, `make evaluate_v8` no tiene una congelación verificable.
3. Comprueba que `sha256_predicciones_v8` de docs/v8/notas_release.md coincide con output/v8/congelacion/congelacion.json.

## 2. Revisión humana antes de difundir (docs/v8/cierre_proyecto.md, punto 4)

- Lee output/v8/por_que_ha_subido.md y output/v8/informe_econometrico.md contra output/v8/F5/fichas.md.
- Revisa la regla operativa del factor más relevante (docs/v8/desviaciones.md, R0-R8) y la corrección de la ficticia EPA (revisión F4, J1).
- Verifica en Crossref y Scimago las referencias metodológicas marcadas NO VERIFICADA en las fichas del verificador V8.

## 3. Evaluación diferida en 2027

- `make evaluate_v7` y `make evaluate_v8`, una sola vez cada uno, cuando se publiquen los datos de 2026T3-2027T2 (evaluate_v8 solo abre si están los cuatro trimestres de las tres series).

## 4. Fase de propuestas y publicaciones

Fuera de V8 (no empezada): análisis de propuestas de programas electorales y divulgación. Lo que necesita de V8 está en docs/v8/cierre_proyecto.md, punto 5.
