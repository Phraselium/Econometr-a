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

## K4. Subagentes de la fase 1 (17-10-2026)
- **Problema.** Las definiciones nuevas de .claude/agents (adquisidor-datos y las demás de B2) no se cargan en esta sesión: se crearon después de que empezara.
- **Qué se hace.** Se usa el tipo más cercano, data-fetcher (mismas herramientas), con la instrucción expresa de seguir .claude/agents/adquisidor-datos.md. Los roles de solo lectura que falten se cubren igual, con general-purpose o Explore y la definición del rol en el encargo. Las definiciones de B2 se cargaron durante la fase 1: desde la base de intervenciones se usan los tipos propios (adquisidor-datos y los demás).
- **Dónde escriben.** Los adquisidores escriben en el árbol principal, cada uno en carpetas disjuntas (data/raw/v16/<familia>/ y docs/v16/fuentes/<familia>.md), y no en worktrees. Motivo: los originales de más de 50 MB y las series de terceros no se versionan (.gitignore: _grandes/ y _terceros/) y se perderían al borrar un worktree. Sigue habiendo como máximo tres subagentes que escriben a la vez, y ningún make check corre mientras tanto.

## K5. Registro de licencias de V16
- **Registro.** Es el manifiesto de cada familia: data/raw/v16/<familia>/_manifest.csv, con el mismo esquema que data/raw/v11/_manifest.csv. Sus columnas licencia y redistribuible son las que leen src/v13/inventario_datos.py y la base.
- **Ficheros de terceros.** Los que tienen redistribuible «no» o «dudoso» van a _terceros/ y no se versionan (regla terceros_1_0).
- **Control.** src/v16/f1_inventario.py valida los manifiestos (columnas, sha256, licencia no vacía, ningún fichero versionado de terceros) y escribe docs/v16/inventario_fuentes.csv.

## K6. Lecciones de la auditoría de la fase 1 para la vara de C1 (fase 2)
- **No son fuentes independientes:**
  - OCDE y Eurostat para el precio de la vivienda en España: correlación 0,9999, ambas salen del IPV del INE;
  - los choques mensuales y diarios de Jarociński-Karadi.
  - Con estas parejas no se forma un C1, igual que con ECV y Eurostat.
- **EMCR y EVR** tienen una ruptura de nivel en 2021 (inmigración exterior ×1,31, emigración ×1,56): no se empalman.
- **Partidos judiciales del CGPJ en 2025:** excluidos (fuentes/tension_social.md).
- **Intervenciones:** 78 de 105 fechas fiscales son aproximadas (1 de enero). Se usan solo con resolución anual, y en Q6 la fecha exacta de la ley autonómica entra como robustez.

## K7. Regla del metaanálisis (fase 3), fijada antes de ejecutarlo
- **Unidad de análisis:** un estudio aporta una estimación, la primera que anotó el lector, y nunca se elige la más favorable. El error estándar es el del autor o el derivado de su IC 95 %; nunca se imputa.
- **Cuándo hay metaanálisis:** solo con al menos 5 estudios con error estándar y la misma unidad.
- **Métodos:** efectos aleatorios DL y REML; Egger, PET y PEESE, con aviso si k < 10.
- **Resultado:** con la literatura leída (6 instrumentos, 69 grupos), ningún grupo llega al mínimo. La fase 6 usará distribuciones a priori poco informativas, centradas en cero, con la escala que sugiere el rango de la literatura de diseño creíble. Esta conclusión se declara en el pre-registro de V16 y no se rebaja el umbral para obtener un agregado.
- **Corrección de entrada:** en L3_oferta_elasticidad_efectos.csv, dos filas tenían una coma sin comillas («Asquith, Mast y Reed»). Se repararon uniendo los dos campos, y el script ahora para si un CSV tiene filas de distinta longitud.
