# V16 · Decisiones

## K1. Pre-registro interno sin sello externo: la puerta es la etiqueta en el remoto (B1)
- **Guarda (d).** Ni el hook ni src/v15/puerta.py miran ya osf_prereg_v15: exigen que prereg-v15 exista en el remoto y apunte a 542b4fd.
- **Guarda (f), nueva.** Exige prereg-v16 en el remoto para las fases 5 a 7 de V16 y para el objetivo v16. src/v16/fase.py repite la comprobación, así que llamar al lanzador sin make tampoco la salta (probado).
- **Consulta del remoto.** Se hace con `git ls-remote --tags origin` (src/v16/etiquetas.py). Sin red o sin respuesta, la puerta queda cerrada. Los tests simulan el remoto con ECONOMETRA_ETIQUETAS_REMOTAS.
- **Controles sin red.**
  - check_v15 («puerta») comprueba la etiqueta local.
  - check_v16 («estimaciones posteriores a su etiqueta») falla si un commit que toca estimaciones de V15 (src/v15/pN*.py, output/v15/pN*/) o de V16 (src/v16/qN*.py, output/v16/qN*/) no desciende de su etiqueta, o si hay estimaciones sin etiqueta.
- **Pruebas en vivo.**
  - El hook bloqueó las fases 6 y completa de V16 (guarda (f)) y la fase 4 de V15 (guarda (d)). La (d) también rechazó comandos míos que solo contenían ese texto.
  - Los lanzadores de fase llamados directamente terminan con código 1.

## K2. Subagentes nuevos (B2)
adquisidor-datos, ingeniero-datos, replicador-ciego y redactor (sonnet), abogado-del-diablo (opus) y verificador-cifras (haiku). Todos los alias del plan están disponibles: no hay sustituciones.

## K3. El remoto rechaza las etiquetas (bloqueo B-1)
- **Respuesta.** El remoto devuelve 403 al publicar etiquetas.
- **Qué se hace.**
  - Se versiona docs/v16/etiquetas_prereg.csv con cada etiqueta y su commit.
  - Los comandos para publicarlas pasan a tareas_autor.
- **Cómo afecta a las fases.**
  - Las fases 0 a 4 continúan: no necesitan las etiquetas.
  - Las fases 5 a 7 esperarán a prereg-v16 en el remoto. Es la guarda funcionando, no una parada de la sección D.
