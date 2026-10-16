# V14 · Tareas del autor (en orden)

Todo queda **pendiente del autor**: hacen falta permisos en GitHub, Zenodo y OSF. No se anota ninguna fecha de publicación hasta que exista.

Antes de empezar:
- Trabaje en su máquina, con un clon COMPLETO de Econometr-a (`git fetch --unshallow` si hace falta) y `gh` autenticado.
- La integración de Zenodo con GitHub debe estar **DESACTIVADA** para los dos repositorios. El depósito se sube a mano.
- Sustituye a docs/v13/tareas_autor.md, puntos 1-6. Los comandos de etiquetas y el texto de OSF siguen allí.

## 0. Revisar docs/v14/cifras_terceros.md y las condiciones de uso
- Lea docs/v14/cifras_terceros.md (y el .csv): las cifras publicadas que dependen de Notariado, Registradores o AEAT, con su capa, su ficha y dónde aparecen.
- Lea las condiciones de uso enlazadas al final. No están interpretadas.
- Decida, por fuente, si los agregados publicados pueden seguir en publicacion/, consulta/ y la web.
- Si alguna cifra debe retirarse, se hace en una versión posterior, con entrada en ERRATA.md y en cifras_superadas.csv. Nunca se toca a mano.

## 0 bis. Calcular la huella de data/sealed si sigue pendiente
En su máquina, desde la raíz de Econometr-a (donde está data/sealed):
```bash
find data/sealed -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum
```
- Escriba los 64 caracteres hexadecimales en proyecto.json, en `hash_sellado.valor`, y la fecha en `hash_sellado.fecha`.
- Ejecute `make publicacion && make check` y haga commit.
- Mientras siga «PENDIENTE», `make check` avisa en Econometr-a y **falla en el árbol público** (src/v14/check_v14.py). Por eso este paso va antes de generar y subir el repositorio nuevo (punto 2).

## 1. Publicar las 18 etiquetas en el remoto de Econometr-a (antes de archivarlo)
Las etiquetas existen solo en el clon de trabajo de la sesión; en el remoto hay 0. En un clon nuevo se crean sobre los mismos commits.
```bash
git clone https://github.com/Phraselium/Econometr-a.git econometr-a && cd econometr-a
git fetch origin claude/housing-price-spain-econometric-95dhj3
# bloque 3.2 de docs/v13/tareas_autor.md: función crear() y las 18 llamadas
# (prereg-v2 … prereg-v9-a1b y v5.0 … v8.0), con los SHA-1 completos y la comprobación de sha256
git push origin refs/tags/prereg-v2 refs/tags/prereg-v3 refs/tags/prereg-v5 refs/tags/prereg-v6 refs/tags/prereg-v7 \
  refs/tags/prereg-v8 refs/tags/prereg-v9 refs/tags/prereg-v9-a1 refs/tags/prereg-v9-a1b \
  refs/tags/v5.0 refs/tags/v5.1 refs/tags/v6.0 refs/tags/v6.1 refs/tags/v6.2 refs/tags/v7.0 refs/tags/v7.1 refs/tags/v7.2 refs/tags/v8.0
git ls-remote --tags origin | wc -l   # 18 (más las ^{} de las anotadas)
```
Opcional: las etiquetas de las versiones internas que no la tienen (v8.1, v9.0, v10.0, v11.0, v12.0), con los commits de la tabla de docs/v13/tareas_autor.md.

## 2. Crear el repositorio vivienda-espana-evidencia y subir main
El árbol se genera desde el último commit de Econometr-a. Es un repositorio git nuevo con un único commit, «Versión 1.0».
```bash
cd econometr-a
git checkout claude/housing-price-spain-econometric-95dhj3
make arbol_publico DEST=../vivienda-espana-evidencia
cd ../vivienda-espana-evidencia
git log --oneline                         # un único commit: «Versión 1.0»
git commit --amend --reset-author --no-edit   # opcional: el commit con su nombre y correo
gh repo create Phraselium/vivienda-espana-evidencia --public --source . --remote origin --push
```
Antes de subir, compruébelo:
```bash
mkdir -p _descarga && cp -r <ruta>/_deposito/vivienda-espana-evidencia-1.0 _descarga/   # paquete del punto 3
make datos && make check && make publicacion && git status --short   # git status debe salir vacío
```

## 3. Crear el depósito en Zenodo con el paquete (sin la integración automática con GitHub)
```bash
cd econometr-a
make paquete_zenodo && python3 src/v13/paquete_zenodo.py --zip
(cd _deposito/vivienda-espana-evidencia-1.0 && sha256sum -c --quiet CHECKSUMS.sha256)
```
En https://zenodo.org/uploads/new:
1. Suba `_deposito/vivienda-espana-evidencia-1.0.zip`.
2. Copie los metadatos de `.zenodo.json`: título, autor y afiliación, versión 1.0, idioma, palabras clave, licencias (MIT y CC BY 4.0) y descripción. Como identificador relacionado ponga la URL del repositorio nuevo («is supplement to»).
3. **Reserve el DOI**, todavía sin publicar.

## 4. Con el DOI: actualizar proyecto.json, regenerar y subir como 1.0.0 con la etiqueta v1.0.0
1. En proyecto.json de Econometr-a, ponga:
   - `doi`: el DOI reservado;
   - `zenodo_url_paquete`: `https://zenodo.org/records/<id>/files/vivienda-espana-evidencia-1.0.zip?download=1`;
   - si quiere el número de tres cifras, `version_publica`: «1.0.0». Cambie también la versión escrita a mano en README.md, LEEME_PRIMERO.md, CLAUDE.md, README_REPLICACION.md y historico/INDICE.md: check_v13 exige que todas las puertas declaren la misma.
2. Regenere y compruebe:
   ```bash
   make metadatos publicacion consulta && make check
   git commit -am "1.0.0: DOI de Zenodo" && git push origin claude/housing-price-spain-econometric-95dhj3
   ```
3. Si cambió `version_publica`, vuelva a generar el paquete (punto 3) y sustituya el fichero en el borrador de Zenodo antes de publicar.
4. Regenere el árbol, copie su contenido sobre el repositorio nuevo (sin su .git) y suba:
   ```bash
   make arbol_publico DEST=/tmp/arbol-1.0.0
   rsync -a --delete --exclude .git --exclude _descarga --exclude data /tmp/arbol-1.0.0/ ../vivienda-espana-evidencia/
   cd ../vivienda-espana-evidencia && git add -A && git commit -m "Versión 1.0.0: DOI" && git push origin main
   git tag -a v1.0.0 -m "Versión pública 1.0.0" && git push origin refs/tags/v1.0.0
   gh release create v1.0.0 --repo Phraselium/vivienda-espana-evidencia --verify-tag --title "Versión pública 1.0.0" --notes-file CHANGELOG.md --latest
   ```
5. Publique el depósito en Zenodo y anote aquí la fecha que muestre Zenodo: `fecha_deposito: PENDIENTE`.

## 5. Registro en OSF de los pre-registros
- Use el texto propuesto en docs/v13/tareas_autor.md, punto 5. Recoge las 9 etiquetas `prereg-*` con su SHA-1 y el sha256 de cada documento.
- Añada esta frase:
  > «El sello externo de este registro es posterior a los commits que fija: la anterioridad respecto a los resultados descansa en el commit, su fecha y su huella, y este registro es la primera constancia independiente.»
- Adjunte cada documento tal como está en su commit (`git show <etiqueta>:<ruta>`).
- Anote aquí el DOI y la fecha del registro: `osf_registro: PENDIENTE`.

## 6. Publicar la web desde el repositorio nuevo (GitHub Pages)
1. En el repositorio nuevo, vaya a Settings → Pages y elija como origen «GitHub Actions». El workflow .github/workflows/pages.yml publica en cada push a main.
2. Compruebe la web en https://phraselium.github.io/vivienda-espana-evidencia/. El pie debe mostrar «Versión 1.0» (o 1.0.0) y el DOI.

## 7. Archivar Econometr-a cuando todo lo anterior esté hecho
```bash
gh repo archive Phraselium/Econometr-a --yes      # o, si prefiere, pasarlo a privado:
# gh repo edit Phraselium/Econometr-a --visibility private --accept-visibility-change-consequences
```
- Si lo pasa a privado, los enlaces de historico/INDICE.md del repositorio nuevo dejan de resolver para el público.
- Archivar lo mantiene legible y sin cambios. Es lo recomendado.

## 8. Enviar la revisión externa
- Envíe al revisor revision_externa/: `guia.md` y `hoja_revision.xlsx`, junto con el enlace al repositorio nuevo y el DOI.
- La muestra se reproduce con `make muestra_revision` (SEED = 20261010).
- Los errores que aparezcan van a ERRATA.md y a una versión 1.0.x.

## Pendientes que no bloquean la 1.0
- **D4 · AEAT. Cómo reincorporar las 7 variables `aeat_irpf_*` en una 1.0.1:**
  1. Revise el aviso legal: https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica/aviso-legal/propiedad-intelectual.html. A 2026-10-16 reserva los derechos y no concede una licencia abierta.
  2. Revise también la ficha del conjunto en datos.gob.es, si lo hay, y la página de estadísticas: https://sede.agenciatributaria.gob.es/Sede/estadisticas.html.
  3. Si hay una licencia que permita redistribuir, o una autorización escrita:
     - vacíe `EXCLUIR_PUBLICA` en src/v13/paquete_zenodo.py y quite la regla AEAT de src/v13/inventario_datos.py;
     - quite «aeat» de `PALABRA` en src/v14/terceros.py;
     - actualice docs/v5/licencias_datos.md;
     - suba `version_publica` a 1.0.1 y regenere con `make metadatos publicacion consulta paquete_zenodo arbol_publico`;
     - publique una versión nueva del depósito en Zenodo (nueva versión del mismo concepto, no un DOI nuevo independiente).
- **Huellas de data/sealed (D3):** en su máquina, guarde el sha256 de data/sealed en un fichero versionado. Así podrá comparar el estado del sellado en el futuro.
- **Tareas abiertas de V12:** puntos 3 y 5 de docs/v12/tareas_autor.md.
