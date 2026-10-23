# Tareas del autor · publicación 2.0 (en orden; 2026-10-23)

Lista única desde la consolidación final. Sustituye, para la publicación, a docs/v14/tareas_autor.md (pasos de la 1.0, que no llegó a publicarse) y recoge lo que sigue abierto de docs/v18/tareas_autor.md. Todo queda **pendiente del autor**: hacen falta permisos en GitHub, Zenodo y OSF y decisiones que no se toman por él. No se anota ninguna fecha de publicación hasta que exista. Las secciones «## » de este fichero son la lista de pendientes de consulta/version.json.

Antes de empezar: trabaje en su máquina, con un clon completo de Econometr-a (`git fetch --unshallow` si hace falta), `gh` autenticado y la integración de Zenodo con GitHub **desactivada** (el depósito se sube a mano).

```bash
git clone https://github.com/Phraselium/Econometr-a.git econometr-a && cd econometr-a
git checkout claude/housing-price-spain-econometric-95dhj3
```

## 1. Calcular la huella de data/sealed
En la máquina donde está data/sealed, desde la raíz: `find data/sealed -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum`. Escriba los 64 caracteres en proyecto.json (`hash_sellado.valor` y `hash_sellado.fecha`). Mientras sea «PENDIENTE», `make check` avisa aquí y falla en el árbol público.

## 2. Confirmar dos decisiones abiertas
- Las dos filas añadidas a docs/v16/escrituras_autorizadas.csv para cifras_clave (V18, fase 6).
- Los 16 hallazgos del escaneo de terceros que la 1.0 no había revisado (docs/documento_final/publicacion_2_0.md), sobre todo seis tablas derivadas de la AEAT que con `terceros_1_0.aeat = agregados` entran en el árbol y el paquete: confirmar que son agregados propios o excluirlas.
- La versión pública: proyecto.json dice 2.0, fecha 2026-10-23, preparada y sin publicar. Si prefiere el número de tres cifras (2.0.0) o otra fecha, cámbielo allí y en las puertas escritas a mano (README.md, LEEME_PRIMERO.md, CLAUDE.md, README_REPLICACION.md e historico/INDICE.md; check_v13 exige que coincidan) y regenere con `make metadatos publicacion consulta web`.

## 3. Publicar las etiquetas en el remoto de Econometr-a
Las etiquetas de pre-registro y de versión solo existen en el clon de trabajo; el proxy de la sesión no deja subirlas. Cree en su clon las que falten sobre los mismos commits (tabla de docs/preregistros.md y bloque 3.2 de docs/v13/tareas_autor.md) y súbalas, incluida `plan-replicacion-v18` (commit ad4385c):
```bash
git push origin refs/tags/prereg-v2 … refs/tags/prereg-v16 refs/tags/plan-replicacion-v18
```

## 4. Enviar la revisión externa 2.0
Carpeta revision_externa/2_0/: guía de dos páginas (guia.md y guia.pdf), resumen ejecutivo en PDF, hoja_revision.xlsx y muestra.csv (40 cifras del documento final por capa y clase, SEED=20261010; `make revision_externa_2_0` la reproduce). Adapte el texto de docs/v14/publicacion_1_0/correo_revisor.md. Los errores que aparezcan van a ERRATA.md y a una versión 2.0.x. La carpeta revision_externa/ de la 1.0 queda como histórico.

## 5. Crear el repositorio vivienda-espana-evidencia y subir el árbol 2.0
El árbol se genera desde el último commit de Econometr-a, con un único commit «Versión 2.0». Ensayo de la consolidación: docs/documento_final/publicacion_2_0.md.
```bash
make paquete_zenodo
make arbol_publico DEST=../vivienda-espana-evidencia
python3 src/v14/escaneo_terceros.py --arbol ../vivienda-espana-evidencia --paquete _deposito/vivienda-espana-evidencia-2.0
cd ../vivienda-espana-evidencia && mkdir -p _descarga && cp -r ../econometr-a/_deposito/vivienda-espana-evidencia-2.0 _descarga/
make datos && make check && make publicacion && git status --short
gh repo create Phraselium/vivienda-espana-evidencia --public --source . --remote origin --push
```
Si `make check` del árbol falla por el recuento de tests (docs/v14/tests_arbol.json), regenérelo como dice docs/v14/arbol_1_0.md («Recuento»).

## 6. Depósito en Zenodo con el paquete 2.0
```bash
make paquete_zenodo && python3 src/v13/paquete_zenodo.py --zip
(cd _deposito/vivienda-espana-evidencia-2.0 && sha256sum -c --quiet CHECKSUMS.sha256)
sha256sum _deposito/vivienda-espana-evidencia-2.0.zip
```
En https://zenodo.org/uploads/new suba el zip, copie los metadatos de docs/documento_final/publicacion_2_0/zenodo_metadatos.md (versión 2.0, con el documento final en la descripción), y **reserve el DOI** sin publicar.

## 7. Con el DOI: actualizar proyecto.json, regenerar y publicar
Ponga `doi` y `zenodo_url_paquete` (`https://zenodo.org/records/<id>/files/vivienda-espana-evidencia-2.0.zip?download=1`) en proyecto.json; `make metadatos publicacion consulta web && make check`; commit y push. Vuelva a generar el árbol y el paquete, súbalos, cree la etiqueta `v2.0` y la release en GitHub y publique el depósito. Anote aquí la fecha que muestre Zenodo: `fecha_deposito: PENDIENTE`.

## 8. Registro en OSF de los pre-registros
Siga docs/v14/publicacion_1_0/osf_registro.md con la tabla actual de docs/preregistros.md y la etiqueta plan-replicacion-v18. El sello externo es posterior a cada pre-registro y así se declara. `osf_registro: PENDIENTE`.

## 9. Publicar la web (GitHub Pages)
docs/v14/publicacion_1_0/github_pages.md. La portada lleva el resumen ejecutivo del documento final y la página «Documento final». Compruebe que el pie muestra «Versión 2.0» y el DOI.

## 10. Archivar Econometr-a
Cuando todo lo anterior esté hecho: `gh repo archive Phraselium/Econometr-a --yes` (recomendado frente a pasarlo a privado, que rompe los enlaces de historico/INDICE.md).

## Pendientes que no bloquean la 2.0
- **Datos que harían estimable lo que hoy no lo es** (docs/v18/tareas_autor.md y parte IX del documento final): descarga masiva del Catastro, clave de AEMET, histórico de InsideAirbnb, fianzas por barrio y por tramo con la renta anterior, perceptores de ayudas, anuncios de portales, SIU, compras por nacionalidad y provincia, ordenanzas fiscales de vacías y promociones públicas por municipio.
- **Bibliografía:** tabla de cuartiles de Scimago y repetición de la búsqueda sistemática con OpenAlex.
- **Evaluaciones selladas diferidas:** `evaluate_v7`, `evaluate_v8` y, si alguna estimación llega a IDENTIFICADO, `evaluate_v18`; no antes de 2027 y solo con su orden.
- **Licencias de terceros:** Anuario ERI de Registradores y Notariado (docs/v14/tareas_autor.md, «Pendientes que no bloquean la 1.0»), siguen igual.
- **vivienda.duckdb:** está en disco tras la consolidación (docs/documento_final/base_restaurada.md); no se versiona.
