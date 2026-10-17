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
- **Resultado:** con la literatura leída (7 instrumentos, 88 grupos de resultado), ningún grupo llega al mínimo. La fase 6 usará distribuciones a priori poco informativas, centradas en cero, con la escala que sugiere el rango de la literatura de diseño creíble. Esta conclusión se declara en el pre-registro de V16 y no se rebaja el umbral para obtener un agregado.
- **Corrección de entrada:** en L3_oferta_elasticidad_efectos.csv, dos filas tenían una coma sin comillas («Asquith, Mast y Reed»). Se repararon uniendo los dos campos, y el script ahora para si un CSV tiene filas de distinta longitud. En L2 se quitaron dos filas de cabecera de bloque («BLOQUE …»).

## K8. La muestra sellada v6 cubre CCAA enteras: consecuencias para V16 (17-10-2026)
- **Qué hay.** Las 11 provincias selladas de v6 forman bloques de CCAA completos: 07, 22, 26, 28, 30, 31, 33, 35, 38, 44 y 50. Son Aragón, Asturias, Baleares, Canarias, Madrid, Murcia, Navarra y La Rioja.
- **Qué está sellado.** La marca muestra_sellada_v6 se aplica por regla a provincia, municipio, distrito y sección. Las filas de nivel ccaa de esas comunidades no se marcan: los paneles de CCAA ya se vieron en v1 (CLAUDE.md, V7) y la auditoría de contaminación de V15 mantuvo esa definición. No es un acceso a la muestra sellada ni una parada D.
- **Consecuencias para V16:**
  - Los datos municipales y provinciales nuevos de esas ocho comunidades solo se usan a través de src/holdout.py. Por ejemplo: el registro de viviendas turísticas de Madrid, Canarias y Baleares, Inside Airbnb de Madrid y Mallorca, y el padrón por sección de Madrid.
  - Las preguntas de V16 se diseñan con el resto de provincias. Los totales de CCAA de esas comunidades no se usan como sustituto de sus provincias en una validación provincial: duplican la información sellada.
  - sellar_v16 (fase 4) no vuelve a sellar esas provincias: elige su bloque espacial nuevo entre las 39 restantes.
- **Origen.** La auditoría de alquiler_turismo (output/v16/auditoria/alquiler_turismo) lo detectó al no encontrar filas no selladas de Madrid, Canarias ni Baleares.

## K9. Pre-registro V16: nada confirmatorio y todo C4 como máximo (17-10-2026)
- **Origen.** La potencia con placebos (output/v16/potencia) y dos revisiones independientes (revisor-preregistro: «aprobar con cambios»; abogado-del-diablo: «no resiste» en la primera redacción).
- **Decisión.** El documento final es docs/v16/preregistro_v16.md más su adenda vinculante.
  - V16 no añade hipótesis confirmatorias y todo V16 es C4 como máximo: en entrenamiento no se pasa de C4 y la lista de parejas de triangulación válidas está vacía.
  - Hay dos ramas de control de falsos descubrimientos: 21 pruebas de diseños y 83 celdas de una rejilla fija.
  - Las especificaciones principales y las magnitudes de referencia son numéricas y quedan fijadas, con una holgura del 20 %.
  - El código de holdout impide abrir datos de V15 antes de su evaluación.
- **Desviación del plan.** Está en docs/v16/desviaciones.md (D1).

## K10. Etiquetas publicadas y puertas de V15 y V16 (2026-10-17)
- **Comprobado.** Las 11 etiquetas prereg-* están en el remoto, son anotadas y apuntan a su commit (tareas_autor §1).
- **Puertas.** src/v16/etiquetas.py, guardas (d) y (f) del hook, src/v15/puerta.py, fase.py y evaluate_v16 exigen dos cosas a la vez:
  - (1) la etiqueta publicada y apuntando a su commit: prereg-v15 → 542b4fd y prereg-v16 → a8304ec, este último ya fijo;
  - (2) el criterio provisional: el commit está en la rama remota y los ficheros del pre-registro (texto, adenda y sellado) no han cambiado desde él.
- **Pruebas de las puertas.**
  - Tests (tests/v16/test_guardas.py): bloquean sin etiqueta, con la etiqueta en otro commit y cuando falla el criterio provisional, y dejan pasar con las dos condiciones.
  - Autocomprobación de check_v16 con los mismos casos.
  - En vivo, en esta sesión, las dos puertas están abiertas y las órdenes prohibidas (e) siguen bloqueadas.
- **Registro.** docs/preregistros.md y docs/preregistros_ficheros.csv, generados por src/v16/preregistros.py:
  - fecha del commit en UTC, sacada de git;
  - fecha de publicación de la etiqueta, la del etiquetador de la etiqueta anotada;
  - sha256 de cada fichero en su commit.
  - check_v16 comprueba que los hashes coinciden con git, que las fechas son las de git y que V15 y V16 siguen intactos.
- **Ficheros cambiados después de su commit.** Hay cuatro, todos de versiones cerradas, y se declaran en el registro:
  - v2: recuento del sellado;
  - v6: huella del sellado rehecha;
  - v9: se añadió el hash del propio commit;
  - v9-a1: sustituido por v9-a1b.
  - Ninguno cambia una hipótesis ni una cifra de la 1.0.
- **Hashes corregidos en CHANGELOG.md.** Citaba prereg-v2, prereg-v5 y prereg-v6 con el hash de los antiguos objetos de etiqueta locales (f59574a, 1e057cd, 278cc9e) en lugar del commit. Ahora cita 910c42a, 8803f04 y a33c167. Las fechas de docs/v6_2, docs/v13 y docs/v14 ya coincidían con git.
- **Redacción en los textos.** «Pre-registro interno, fijado en el commit X y publicado como etiqueta el <fecha>, sin sello de tiempo externo».

## K11. Cambios posteriores a los commits de pre-registro (2026-10-17, encargo del autor)
- **v2: sellado anterior a todas las evaluaciones.**
  - El cambio es fd2559a, a las 07:20Z, y la primera evaluación es de las 07:45Z.
  - Lleva el código a lo que decía el pre-registro: entrenamiento hasta 2024Q2.
  - La fila 2026Q3 que se retiró tiene vacías las variables de resultado (IPV, IPC de alquiler, valor tasado; comprobado en git) y está fuera de la ventana evaluada.
- **v6: huella cambiada después de todas las evaluaciones.**
  - El cambio es 42cf68b, a las 17:48Z, y la última evaluación es de las 17:45Z.
  - Solo afecta a dos paneles de contratos nuevos (corrección K4a-02, ya en ERRATA) que ninguna evaluación abrió: ninguna de las 160 entradas v6 del registro los nombra.
- **v9 y v9-a1.** v9 solo añade el hash. v9-a1 lo sustituye v9-a1b.
- **Resultado.** Ningún resultado publicado depende de muestras modificadas y no procede entrada en ERRATA. Está documentado en docs/preregistros_desviaciones.md (publicado como metodologia/desviaciones_preregistros.md) y en docs/preregistros.md.
- **Sin cálculos nuevos.** No se reejecutó ninguna evaluación sellada ni se estimó nada.
- **Publicación.** metodologia/desviaciones_v16.md se publica también desde docs/v16/desviaciones.md.

## K12. Consecuencias del Monte Carlo para la fase 6 (2026-10-17)
- **Tabla.** docs/v16/validacion_montecarlo.md y output/v16/montecarlo/veredictos.csv, generadas por src/v16/f5_validacion.py; se publica como metodologia/validacion_montecarlo_v16.md.
- **Inferencia utilizable (solo estas):**
  - SDID con Conley-Taber, escenario A, con el tamaño en el límite superior (0,0575). Q1b no tiene periodos posteriores al tratamiento en el entrenamiento, así que queda pendiente.
  - Conley a 2 km por sección (Q3-b), solo con el escenario principal; se declara que no es robusto al rango espacial.
  - GSADF sobre el factor con bootstrap salvaje (Q9-g).
  - Benjamini-Yekutieli en lugar del BH jerárquico, en las dos ramas de control.
  - TOST solo cuando Δ/EE ≥ 2; en otro caso, «no concluyente».
- **Todo lo demás es NO APTO y queda solo descriptivo**, con estimación puntual sin p-valor ni IC: CS-Webb, dCDH, rejilla TWFE, shift-share AKM, DiD de intensidad, LP Newey-West b, BLP/GATES, CIPS, CS-ARDL, DM-HLN y bayesiano jerárquico.
- **Sin cambio de especificaciones.** No se cambia ninguna especificación para «hacerla apta». El cambio de BH a BY es la alternativa nombrada en la adenda (punto 11), no una elección por resultados.

## K13. Herramientas de V15 validadas en la fase 5 (2026-10-17)
- **Tabla.** docs/v15/validacion_montecarlo.md y output/v15/montecarlo/veredictos.csv, generadas con `python3 src/v16/f5_validacion.py v15`. Se publica como metodologia/validacion_montecarlo_v15.md. El criterio es el de V16.
- **Utilizables:**
  - SAR/SDM/SEM, con Wald de ρ y efectos indirectos;
  - DM-HLN en E1-E4.
- **Clark-West y MCS al 10 %:** NO APTOS; el MCS queda descriptivo.
- **NO APTOS, solo descriptivos:**
  - SDID de H1/H2. El placebo literal no es computable con 74 o 14 donantes frente a 124 tratados, y Webb da un tamaño de 0,09-0,23.
  - Honest DiD: con M̄ = 1 el IC nunca excluye 0, así que el criterio «M̄ ≥ 1» de H1 no se alcanza en el entrenamiento.
  - Control sintético.
  - AKM y AKM0 de H4.
  - Westerlund y CS-ARDL de E1.
  - Wild bootstrap de Webb.
- **Sin elección por resultados.** La variante «placebo sin escalar» sale APTA solo en S1, pero no es la inferencia pre-registrada ni la alternativa nombrada: no se usa.
- **Efecto en las capas.** Ninguno de estos veredictos cambia la capa máxima de V15 (C4 en entrenamiento; C3 solo tras la evaluación sellada). La evaluación sellada de H1/H2 heredará estas limitaciones de inferencia; se dirá al evaluarla.

