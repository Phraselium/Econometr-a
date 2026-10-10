# Tareas del autor (solo Borja Romero)

Lista de comprobación de lo que no pueden hacer los agentes. Se marca cada casilla al terminar.

## Antes de publicar
- [ ] **Revisión por dos economistas externos.**
  - Perfil 1: economista urbano o de vivienda con experiencia en datos españoles (universidad o servicio de estudios). Revisa B1 (método de necesidad), B2, A4 (clases territoriales) y D1 (matriz).
  - Perfil 2: econometrista aplicado. Revisa B3 (pre-registro, inferencia con N≈50, Conley, permutación), R1B (GSADF, sensibilidad) y A2 (puente de precios).
  - Se les envía: el informe técnico, docs/v5/revision_humana.md (las 15 cifras) y el repositorio. Plazo propuesto: 3 semanas.
- [ ] **Replicación humana de las 15 cifras** de docs/v5/revision_humana.md: ejecutar cada script, comprobar la línea indicada y firmar la tabla.
- [ ] **Licencias.** Confirmar las condiciones de reutilización del Notariado, Registradores, CGPJ y AEAT, y si es admisible la copia de los programas en PDF (docs/v5/licencias_datos.md).
- [ ] **Etiquetas git.** Publicar `prereg-v5` y `v5.0` desde una copia con permisos (`git push origin prereg-v5 v5.0`). El remoto de esta sesión las rechaza (docs/v5/bloqueos.md).
- [ ] **Depósito con DOI.** Conectar el repositorio con Zenodo (usa .zenodo.json y CITATION.cff) y crear la versión 5.0. Añadir después el DOI a README_REPLICACION.md y a CITATION.cff.

## Independencia y colaboración
- [ ] **Coautor o socio institucional.** Buscarlo en una universidad, un servicio de estudios o una fundación sin vínculo partidista. Ventajas: revisión, visibilidad y acceso a datos (fianzas, Catastro). Hay que fijar por escrito la autoría y la independencia del contenido.
- [ ] **Colegiación** en el Colegio de Economistas de València (si no se tiene), con el número para la firma.
- [ ] **Despacho.** Si la publicación se vincula al despacho profesional, consultar antes su política de publicaciones y conflictos de interés; si no se vincula, decir en la declaración que es a título individual.
- [ ] **Declaración de independencia y uso de IA**: revisarla y firmarla (output/v5/working_paper.md, apéndice C, y README_REPLICACION.md).

## Difusión
- [ ] Enviar el correo al Colegio de Economistas de València (output/v5/correo_coev.md), proponiendo el artículo (output/v5/articulo_colegio.md) y la ponencia (output/v5/ponencia/).
- [ ] Revisar y programar la serie de LinkedIn (output/v5/linkedin/), siguiendo el calendario de docs/v5/calendario_publicacion.md.
- [ ] Elegir revista para cada artículo (output/v5/articulos/: cada uno trae 3-4 revistas con cuartil) y adaptar el formato.

## Datos
- [ ] Presentar las solicitudes S1-S10 en el orden de docs/v5/solicitudes.md (sede electrónica de cada organismo) y anotar fecha y registro en la tabla de seguimiento.
- [ ] Reclamar ante el Consejo de Transparencia si no hay respuesta en plazo.
