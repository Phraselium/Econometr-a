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

## K14. Lectura de los resultados de V15 en entrenamiento (2026-10-17)
- **H3.**
  - El IC de Conley a 2 km (p = 0,95) se publica marcado como «condicionado».
  - Conley solo está validado en corte transversal (V16, Q3-b), no en un panel con T = 4.
  - No cuenta para ningún hallazgo ni para Holm.
  - A efectos de la regla de hallazgo, H3 es descriptiva.
- **H2.** El SDID (−14,2 %) queda fuera del IC de V9-D1b, pero sin inferencia válida y frente a una conclusión «sin diferencia detectable». Precisar un «no concluyente» no es contradecirlo (adenda V16, punto 10), así que no hay parada.
- **H1.** El ATT de CS (−7,2 %) cae dentro del IC de V9-D1a (−8,5 a −3,2). No es nuevo: se presenta como réplica en entrenamiento de lo ya visto.
- **H5.** El BVAR se corrigió de escala después de ver su primera ejecución; está registrado en DV15-B-3. Ningún modelo bate al AR(4) ni antes ni después de la corrección.
- **H4.** Solo es puntual. Al quitar los 5 orígenes de mayor peso Rotemberg cambia de signo; se declara como fragilidad.

## K15. Q9-g: pista no confirmada; se levanta la parada D (2026-10-18, decisión del autor)
- **Cifras.** El GSADF del factor común de ln(valor tasado / IPC de alquiler) da 5,92, frente a un valor crítico bootstrap del 95 % de 3,34, con p = 0,004 sin ajuste. Con Benjamini-Yekutieli en la rama de diseños (m = 21) el q es 0,153 (output/v16/fdr/).
- **Por qué no es hallazgo.** El umbral pre-registrado es q ≤ 0,10 (adenda V16, punto 9a) y Q9 no tiene magnitud de referencia (punto 3: «no aplica»), así que la condición (b) no se cumple.
- **Lectura.** Pista no confirmada (C4), coherente con la conclusión de V7.2 y de la 1.0 («no hay exuberancia de los cocientes tras el ajuste múltiple»). No contradice ninguna conclusión publicada y no se aplica la parada D (B-2 queda resuelto).
- **En el informe:**
  - Va solo a la Parte VII («lo que no se puede afirmar»), con los dos números (p = 0,004 y q = 0,153). Tras K16 el q vigente es 0,306, y ese es el que se cita.
  - Lleva tres advertencias:
    - corrección múltiple;
    - el valor tasado está suavizado y retrasado;
    - una exuberancia estadística no identifica una burbuja.
  - Va también a la ficha del verificador sobre «hay / no hay burbuja».
  - No va al resumen ejecutivo.
- **Revisión.** abogado-del-diablo lo revisa como las demás pistas citadas.
- **Cifras citables.** V16-Q9-g, V16-Q9-gp y V16-FDR-Q9-g-q, todas C4.

## K16. Réplica ciega: dos errores de implementación corregidos y una imputación retirada (2026-10-18)
Regla del plan (fase 6.3): si la réplica discrepa, no se publica hasta resolverlo. Correcciones solo de errores frente a la ficha; ninguna se elige por su resultado.

**Conley (Q3-b de V16 y H3 de V15)**
- **Error.** `sparse_distance_matrix` de scipy ya guarda la diagonal (distancia 0) y el código la añadía otra vez, así que cada observación contaba dos veces en la varianza y el EE salía inflado. Afectaba a tres sitios:
  - src/v16/montecarlo/conley_seccion.py;
  - src/v16/q3_seccion.py;
  - src/v15/pa_panel.py.
- **Cómo se detectó.** La réplica de Q3-b daba un EE un 21 % menor. Con el núcleo corregido el EE de producción es idéntico al de la réplica (0,00124).
- **Monte Carlo repetido** con el núcleo correcto, R = 4.000, sin cambiar el proceso generador: tamaño 0,096 y cobertura 0,904. Conley a 2 km pasa a **NO APTO**; su APTO anterior venía del error.
- **Consecuencias:**
  - Q3-b y H3 quedan solo con estimación puntual; los EE se dan como referencia, sin IC ni p.
  - La tabla K12 se actualiza.
  - En la rama de diseños queda un solo p válido (Q9-g). Su q de Benjamini-Yekutieli pasa de 0,153 a **0,306** (m = 21; K15 sigue valiendo, con el nuevo q).

**H5 (V15): errores frente a DV15-B-1 y fugas**
- **Causa.** La réplica daba una razón de 1,15 frente a 1,70. La reconciliación (output/v16/replica/h5/reconciliacion.md) encontró en producción:
  - el primer origen estaba desplazado: ok + 24 + h en lugar de ok + 24 − 1;
  - el AR(4) incluía en su estimación la fila del propio objetivo (i + h ≤ len en lugar de i + h ≤ t) y empezaba en 1995 en vez de en 2003T1;
  - compraventas y ocupados estaban desestacionalizados con STL sobre toda la muestra, usando datos posteriores al origen.
- **Correcciones.** Primer origen según DV15-B-1, AR(4) sin fuga y desde 2003T1, y STL reestimada en cada origen. Ninguna dato posterior al origen se usa; es una regla del proyecto, no una elección por resultado.
- **Resultado corregido.** P = 53; razón ECM combinación / AR(4) = **1,51**; DM-HLN unilateral p = 0,866.
- **Discrepancia restante.** La réplica da 1,15. Se debe a elecciones que la ficha deja abiertas (sobre todo LASSO y BVAR) y se reportan ambas cifras (regla de CLAUDE.md). La conclusión es la misma en las dos: la combinación no supera al AR(4).
- **Error de la réplica.** El encadenado del IPC solo afecta a su ECM v1.

**H4 (V15): imputación no declarada**
- **Qué pasaba.** Los municipios sin población en el año base (2003) recibían instrumento 0 sin declararlo. La ficha define la cuota en el año base, así que esos municipios quedan fuera.
- **Resultado.** N pasa de 13.442 a 13.417 y el coeficiente puntual de 0,29 a **0,305** % por punto. La réplica da 0,309 con N = 13.395; la diferencia restante de muestra es del 0,16 %, dentro de la tolerancia del coeficiente.

**Réplicas que coinciden sin cambios:** Q9-g (5,919 frente a 5,92), E3 (ρ 0,392 frente a 0,39) y H1 (−7,18 % frente a −7,2 %).

**Ninguna cifra de la 1.0 cambia.** Son resultados de V15 y V16 todavía no publicados en cifras_clave, así que no hay entrada en ERRATA.

## K17. Revisión adversarial: dos correcciones y la lista de pistas citables (2026-10-18)
Tres revisiones de abogado-del-diablo; respuesta punto por punto en output/v16/critica/respuestas.md.

**Correcciones (errores frente a la ficha, no elecciones por resultado)**
- **Q2c.** La principal no era la de la adenda, punto 3. La adenda fija Δlog del IPVA municipal sobre la exposición INE-VUT estandarizada en nivel, con efectos fijos de municipio y año. Se había usado el log del nivel y el log de la exposición.
  - La principal pasa a ser la de la adenda: −0,0054 por DT, puntual. La anterior (−0,0095) queda como variante.
  - El placebo, los controles y la exclusión de grandes ciudades se rehacen con la principal.
- **Q6.** El resumen del multiverso incluía las dCDH con la fecha adelantada un año, que equivalen al placebo. Se quitan del resumen pero siguen en el registro.

**Texto**
- **H3.** Se quita «preciso». H3 es «no concluyente», no «nula», y se cita la mediana del multiverso.
- **Q5.** Se da el número real de especificaciones (15).

**Contrastadas con datos**
- **BY frente a BH.** Lo obliga la adenda (punto 2), porque el BH jerárquico falló en el Monte Carlo.
- **AR(4) de H5.** No hay fuga. La diferencia con la reconciliación es una convención de ventana.

**Qué se cita y cómo** (solo C4, sin lenguaje causal; siempre con mediana y rango del multiverso cuando la principal está en un extremo)
- **Pistas citables:**
  - H1, solo en el signo, con el rango CS-SDID;
  - H5, «la combinación no supera al AR(4)», con la razón entre 1,15 y 1,51 según la implementación;
  - E3, como correlación espacial descriptiva, con el rango del multiverso;
  - Q6-p, puntual.
- **Correlaciones frágiles:** Q3-b y H4.
- **No se citan como pista:**
  - H2, Q1c, Q6-v, Q5 y Q10-3;
  - Q2c, que tiene el signo inestable;
  - H3 y Q2a, que son «no concluyentes».
- **Q9-g:** solo en la Parte VII (K15). La revisión lo lee como artefacto probable: GSADF sobre una tasación suavizada sin rezagos y fechas en tramos bajistas.

**Pendiente de la fase 7:** la coherencia de lo_ya_visto entre «ningún modelo predice mejor» y K1-N-MEJOR (6 de 9), sin cambiar ninguna cifra 1.0.

## K18. Aclaraciones antes de la fase 7 (2026-10-18, encargo del autor)

**Por qué el q de Q9-g pasó de 0,153 a 0,306**
- **La familia no cambió.** Es la rama de diseños, con m = 21 fijo (18 pruebas principales + 3 BLP) y Benjamini-Yekutieli con q = 0,10. El p de Q9-g tampoco cambió (0,004; réplica ciega: COINCIDE).
- **Fórmula.** q_(k) = p_(k) · m · c(m) / k, donde c(21) = Σ 1/i = 3,6454 y k es la posición de la prueba ordenando los p de menor a mayor.
- **Antes de K16** había dos p válidos: Q3-b (7,6e-9, posición 1) y Q9-g (posición 2). Por eso q = 0,004 · 21 · 3,6454 / 2 = 0,153.
- **Tras K16**, la corrección del núcleo de Conley dejó Conley a 2 km como NO APTO. Q3-b perdió su p: sigue contando en m = 21, pero no puede rechazarse. Q9-g pasó a la posición 1, así que q = 0,004 · 21 · 3,6454 / 1 = 0,306.
- **Lectura.** La conclusión no cambia: q > 0,10 tanto antes como después.
- **Valor que cita el informe.** La Parte VII y la ficha del verificador citan la cifra V16-FDR-Q9-g-q, que hoy vale 0,306.
  - La genera src/v16/f6_fdr.py a partir de los p vigentes.
  - El test tests/v16/test_fdr.py::test_q_de_q9g_citable_es_el_vigente comprueba que coincide con el control BY recalculado y que ningún hechos.json conserva 0,153.
  - verificador-cifras comprobará en la fase 7 que el informe usa ese id.

**H5: por qué la razón frente al AR(4) va de 1,15 a 1,51**
- La ficha (preregistro_v15, H5; DV15-B-1 a B-4) no fija la penalización del LASSO, la prior exacta del BVAR ni el número de factores del DFM.
- **1,51** es la implementación de producción corregida (K16): primer origen 2013T1, AR(4) desde 2003T1 sin fuga, y STL reestimada en cada origen.
- **1,49** es la misma con la desestacionalización hecha sobre toda la muestra (con datos posteriores al origen).
- **1,21** es la misma con las series sin desestacionalizar.
- **1,15** es la réplica ciega, con sus propias elecciones dentro de lo que la ficha deja abierto.
- **Cifra pre-registrada:** la combinación de la ficha (DFM, BVAR, LASSO y ARDL frente al AR(4), h = 1, valor tasado, ventana expansiva) en la implementación de producción, es decir, **1,51**.
- **Cómo se cita.** Siempre con el rango [1,15; 1,51] y la lectura común: la combinación no supera al AR(4).

**Réplicas ciegas añadidas antes de la fase 7** (todo lo que se cita con cifra; se añaden a K16)
- **Q2a: COINCIDE.** 0,013162 frente a 0,0132, con el mismo N.
- **H3: COINCIDE.** 0,002989 % por DT, con el mismo N. Advertencia: el replicador fijó la regla de los singletons de municipio × año después de comparar el N. Su primera pasada, sin esa regla, daba 0,00303 %, también dentro de la tolerancia. La regla no cambia el coeficiente.
- **Q6-p: DISCREPABA. Error en producción, corregido.**
  - En src/v16/q6_itp.py, las diferencias por provincia (ΔY y Δtipo) saltaban los años sin dato. Cuenca no tiene valor tasado de 2012, así que aparecía en 2013 un «cambio de tipo» falso de +1 punto con un ΔY de dos años.
  - Ahora solo se usan diferencias entre años consecutivos.
  - Q6-p pasa de −0,0157 a **−0,0020** log por punto (N = 480), igual que la réplica (−0,0020).
  - Q6-v no cambia (0,0251), porque sus series no tienen huecos.
  - Con −0,0020 frente a una referencia de −0,01, sin inferencia válida, Q6-p deja de ser pista y pasa a **«no concluyente»**.

**Lista de citables que sustituye la de K17**
- **Pistas:** H1 (solo el signo), H5 y E3.
- **Correlaciones frágiles:** Q3-b y H4.
- **«No concluyente»:** H3, Q2a y Q6-p.
- **Parte VII:** Q9-g.

Todas las cifras que se citen tienen réplica ciega coincidente o resuelta:

| Resultado | Réplica |
|---|---|
| Q9-g | coincide |
| E3 | coincide |
| H1 | coincide |
| Q2a | coincide |
| H3 | coincide |
| Q3-b | resuelta (K16) |
| H4 | resuelta (K16) |
| H5 | resuelta (K16) |
| Q6-p | resuelta (K18) |

Lo que no se cita como pista (H2, Q1c, Q6-v, Q5, Q10, Q2c) se nombra en el informe sin cifra, solo con el motivo.

## K19. Réplica ciega de las cifras de una_pagina y de las C1 de la 1.0 (2026-10-18, encargo del autor)
31 cifras en cuatro lotes (output/v16/replica/v10_{a,b,b2,c,d}/), con reconciliación de las que discrepaban.

**Cegado parcial.** En varios lotes el replicador vio los valores publicados antes de estimar, por fallos al leer cifras_clave o porque la documentación los cita. Consta en cada resultado.json.

**Lote a: coinciden las 9**, entre ellas las 7 C1 (A23-A10, A23-A2, A23-A9, A23-P2, R1C-001, dh_2125 y terminadas_1924) y E-T7-*. Hubo que deducir dos detalles comparando con lo publicado:
- el filtro de celdas sin renta de A23-A9;
- el parque de E-T7-demol-2024.

**Lote b: coinciden 7.**
- L3-DEF-2124-SENS, L3-DEF-2124-SINBAJAS, E-B1-F y V10-ATL-A1 coinciden.
- T3-H5b y T4-H3 coinciden en la segunda pasada.
- T4-H2 coincide en la central y el máximo. El mínimo se explica por una convención del original no escrita, que se ha documentado en el anexo: en cuanto y − L > 2025, la cartera toma el relleno sin interpolar. La cifra no cambia.

**Lote c (GSADF de V7.2 y V7.1).**
- Coinciden V72-GSADF-ccaa-v6, V72-GSADF-tipos-p05, V71-S3-comun-r2-compra y V71-S3-largo-confirmadas (esta solo en el recuento).
- V71-S3-R6 es correcta, reproducida al bit, pero su ficha omite supuestos.
- **Los recuentos GSADF tienen dos errores de código del original** (E1 y E2; B-4 y ERRATA): ccaa-bh, niveles-bh y ratios-p05 cambiarían.

**Lote d (V8).**
- Coinciden OBS-a y OBS-c.
- H8-9 y VOTOS: el error era de la réplica; el original es correcto.
- M1 (mínimo) y QNA: elecciones que la ficha deja abiertas.
- Quedan correcciones de texto (ERRATA, B-4).

**Lectura.** Las cifras C1 y las de déficit y necesidad se sostienen. Las cifras de exuberancia (GSADF) de una_pagina tienen errores que cambian recuentos publicados, aunque no la capa ni el veredicto «no concluyente». Varias fichas del anexo no bastaban para reproducir la cifra: se han completado las de T4 y quedan por completar las de GSADF y R6 (lista en las reconciliaciones).

