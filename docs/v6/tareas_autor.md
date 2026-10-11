# Tareas del autor para la publicación (v6)

> **Sustituido por docs/v6_1/tareas_autor.md (v6.1).**

Lo que no pueden hacer los agentes. Sustituye a docs/v5/tareas_autor.md como lista de trabajo; las casillas pendientes de v5 se copian aquí. Se marca cada casilla al terminar.

## 1. Etiquetas git
El remoto de la sesión rechaza las etiquetas; a 11 de octubre de 2026, `git ls-remote --tags origin` no devuelve ninguna. Las siguientes existen solo en local: `prereg-v2`, `prereg-v3`, `prereg-v5`, `v5.0` y `v5.1`.
- [ ] Desde una copia con permisos de escritura, comprobar con `git show --no-patch <tag>` que cada etiqueta apunta al commit esperado (pre-registros: commit anterior a cualquier salida de la hipótesis).
- [ ] Publicarlas: `git push origin prereg-v2 prereg-v3 prereg-v5 v5.0 v5.1`.
- [ ] Cuando exista (módulo M0 de v6), publicar `prereg-v6` con `git push origin prereg-v6` **antes** de que haya ninguna estimación de v6, y anotar la fecha.
- [ ] Completar en los entregables la fecha de publicación remota de las etiquetas: sustituir «[fecha de publicación: pendiente]» en docs/v5/plantillas (articulo_colegio, articulos/a_necesidades, b_replicacion, c_territorio, informe_tecnico, lo_que_sabemos, policy_brief, ponencia/guion, una_pagina, working_paper) y regenerar output/v5 con `make all` (o `python3 src/v5/render.py`). No editar output/v5 a mano.

## 2. Release y DOI
- [ ] Crear la release de GitHub sobre la etiqueta `v5.1` (notas: entrada v5.1 de CHANGELOG.md).
- [ ] Conectar el repositorio con Zenodo (lee .zenodo.json y CITATION.cff) y obtener el DOI.
- [ ] Añadir el DOI a README.md, README_REPLICACION.md, CITATION.cff (campo `doi`) y .zenodo.json.
- [ ] Opcional: añadir el ORCID del autor a CITATION.cff y .zenodo.json.
- [ ] Decidir si el correo de contacto aparece en CITATION.cff o README.md (hoy no aparece en ningún fichero versionado).

## 3. Revisión antes de publicar (pendiente de v5)
- [ ] **Revisión por dos economistas externos.**
  - Perfil 1: economista urbano o de vivienda con experiencia en datos españoles. Revisa B1 (método de necesidad, con T1-T3 de v5.1), B2 y T4, A4 (clases territoriales) y D1 (matriz).
  - Perfil 2: econometrista aplicado. Revisa B3 (pre-registro, inferencia con N≈50, Conley, permutación), R1B (GSADF, sensibilidad) y A2 (puente de precios).
  - Se les envía el informe técnico, docs/v5/revision_humana.md (las 15 cifras) y el repositorio. Plazo propuesto: 3 semanas.
- [ ] **Replicación humana de las 15 cifras** de docs/v5/revision_humana.md: ejecutar cada script, comprobar la línea indicada y firmar la tabla.
- [ ] **Licencias de datos.** Confirmar las condiciones de reutilización del Notariado, Registradores, CGPJ y AEAT, y si es admisible la copia versionada de los programas en PDF (docs/v5/licencias_datos.md). Si no lo es, sustituirla por URL + hash.
- [ ] **Declaración de independencia y uso de IA**: revisarla y firmarla (output/v5/working_paper.md, apéndice C; README.md; README_REPLICACION.md §5).

## 4. Independencia y colaboración (pendiente de v5)
- [ ] Coautor o socio institucional sin vínculo partidista (universidad, servicio de estudios o fundación), con acuerdo escrito sobre autoría e independencia.
- [ ] Colegiación en el Colegio de Economistas de València, si procede, con el número para la firma.
- [ ] Despacho: si la publicación se vincula al despacho, consultar su política de publicaciones y conflictos de interés; si no, declarar que es a título individual.

## 5. Difusión (pendiente de v5)
- [ ] Ampliar el artículo del Colegio (unas 1.740 palabras de prosa) y los tres artículos antes de enviarlos (backlog BK-E3).
- [ ] Enviar el correo al Colegio de Economistas de València (output/v5/correo_coev.md) con el artículo y la ponencia.
- [ ] Revisar y programar la serie de LinkedIn (output/v5/linkedin/) según docs/v5/calendario_publicacion.md.
- [ ] Elegir revista para cada artículo (output/v5/articulos/) y adaptar el formato.

## 6. Datos (pendiente de v5)
- [ ] Presentar las solicitudes S1-S10 de docs/v5/solicitudes.md y anotar fecha y registro.
- [ ] Reclamar ante el Consejo de Transparencia si no hay respuesta en plazo.

## 7. Decisiones abiertas de la auditoría (docs/v6/auditoria.md)
- [ ] Scripts de datos fuera de `make data`: `src/build_eventos.py`, `src/v3/build_zonas_eventos_v3.py` y `src/v3/pa_fetch_aux.py`. Propuesta: renombrarlos con el prefijo `fetch_` o documentarlos en README_REPLICACION.md §2 junto a los demás scripts de descarga que no entran en `make all`.
- [ ] Historial git: la auditoría buscó en todo el historial los patrones habituales (ghp_, github_pat_, sk-, AKIA, xox, claves privadas) sin coincidencias; antes de hacer público el repositorio, conviene pasar además un escáner dedicado (p. ej., `gitleaks detect`). Los 332 commits figuran con el correo noreply@anthropic.com como autor: decidir si se reescribe la autoría o se deja (la firma del trabajo está en CITATION.cff).

- [ ] Publicar la etiqueta `v6.0`, creada en local; el remoto de la sesión la rechaza.
