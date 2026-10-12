# Tareas del autor para la publicación (definitivas, v6.1)

> **Sustituido por docs/v6_2/tareas_autor.md (v6.2).**

Este fichero sustituye a docs/v6/tareas_autor.md y a docs/v5/tareas_autor.md. Recoge solo lo que no pueden hacer los agentes. Marca cada casilla al terminar.

## 1. Etiquetas, releases y fechas reales

Las etiquetas solo existen en local. El remoto de la sesión rechaza su envío (HTTP 403), y `git ls-remote --tags origin` no devuelve ninguna. Una etiqueta local **no es verificable por terceros**: puede crearse o moverse en cualquier momento, y la fecha del commit la declara quien lo hace.

| Etiqueta | Commit | Fecha del commit | Qué marca |
|---|---|---|---|
| prereg-v2 | 910c42a | 2026-10-10 07:13 UTC | Pre-registro v2 |
| prereg-v3 | 204c073 | 2026-10-10 13:33 UTC | Pre-registro v3 |
| prereg-v5 | 8803f04 | 2026-10-10 19:11 UTC | Pre-registro v5 |
| v5.0 | cc69e02 | 2026-10-10 21:04 UTC | Cierre de v5 |
| v5.1 | bac2fda | 2026-10-11 07:47 UTC | Cierre de v5.1 |
| prereg-v6 | a33c167 | 2026-10-11 08:47 UTC | Pre-registro v6 |
| v6.0 | 08d7629 | 2026-10-11 17:28 UTC | Cierre de v6 |
| v6.1 | (commit de cierre de v6.1) | — | Cierre de v6.1 |

Sobre el pre-registro:
- Todos estos commits se subieron a la rama remota `claude/housing-price-spain-econometric-95dhj3` en la sesión en que se crearon.
- La prueba externa más fuerte disponible es la presencia del commit en el remoto. Lo que fija una fecha verificable por terceros es la fecha de publicación: release o DOI.
- Los entregables deben declarar el pre-registro **con su fecha real de publicación**, no con la fecha del commit.

Tareas:
- [ ] Desde una copia con permisos de escritura, comprobar `git show --no-patch <tag>` contra la tabla.
- [ ] Publicar las etiquetas: `git push origin prereg-v2 prereg-v3 prereg-v5 v5.0 v5.1 prereg-v6 v6.0 v6.1`.
- [ ] Crear releases de GitHub sobre `v5.0` (cc69e02), `v5.1` (bac2fda), `v6.0` (08d7629) y `v6.1`. Las notas salen de la sección correspondiente de CHANGELOG.md.
- [ ] Sustituir «[fecha de publicación: pendiente]» en docs/v5/plantillas por la fecha real de publicación remota de cada etiqueta o release. Después regenerar con `python3 src/v5/render.py`; nunca se edita output/v5 a mano.

## 2. DOI
- [ ] Activar Zenodo en el repositorio (lee .zenodo.json y CITATION.cff, versión 6.1). La release `v6.1` generará el DOI.
- [ ] Añadir el DOI a README.md, README_REPLICACION.md, CITATION.cff (`doi`) y .zenodo.json. Opcional: ORCID.

## 3. Revisión humana externa
- [ ] Revisión por dos economistas externos, con los perfiles de docs/v6/tareas_autor.md §3.
  - Hay que enviarles el informe técnico y estos documentos:
    - docs/v6_1/auditoria.md
    - docs/v6_1/doble_implementacion.md
    - docs/v6_1/informe_arbitro_academico.md
    - docs/v6_1/informe_arbitro_politica.md
    - docs/v6_1/carta_respuesta.md
  - Las objeciones de los árbitros simulados no sustituyen a una revisión humana.
- [ ] **Replicación de las 15 cifras** de docs/v5/revision_humana.md, firmando la tabla.
  - La doble implementación de K4b, hecha por un agente, reprodujo 5 exactas y 5 parciales.
  - Las otras 5 no se pueden reconstruir solo con el texto publicado (backlog K4b-NR). Para esas, revisar el código citado.

## 4. Licencias y declaración
- [ ] Confirmar las condiciones de reutilización de Notariado, Registradores, CGPJ y AEAT, y la copia versionada de PDF (docs/v5/licencias_datos.md).
- [ ] Revisar y firmar DECLARACION_IA.md y la declaración de independencia del working paper (apéndice C).

## 5. Colegio y difusión
- [ ] Colegiación en el Colegio de Economistas de València, si procede, con el número para la firma.
- [ ] Ampliar el artículo del Colegio y los tres artículos (BK-E3). Enviar el correo al Colegio (output/v5/correo_coev.md).
- [ ] Programar LinkedIn según docs/v5/calendario_publicacion.md. Revisar antes cada post frente a cifras_clave: el verificador de cifras está en make (k4c).
- [ ] Coautor o socio institucional sin vínculo partidista, si se desea. Si la publicación se vincula al despacho, consultar su política; si no, declararla a título individual.

## 6. Solicitudes de datos
- [ ] Presentar las solicitudes S1-S10 de docs/v5/solicitudes.md (exigen identificación electrónica) y anotar fecha y registro. Reclamar ante el Consejo de Transparencia si no hay respuesta.

## 7. Repositorio
- [ ] Pasar un escáner de secretos (p. ej., `gitleaks detect`) antes de hacer público el repositorio. Decidir sobre la autoría de los commits (noreply).
- [ ] Scripts de datos fuera de `make data` (docs/v6/auditoria.md): renombrar con prefijo `fetch_` o documentarlos.

## 8. Referencias
- [ ] Verificar en Scimago el cuartil de las 50 referencias marcadas «cuartil no verificado» y de las 76 NO VERIFICADA con DOI (output/v6_1/K4D/referencias.csv). Desde la sesión, Scimago devuelve 403.
