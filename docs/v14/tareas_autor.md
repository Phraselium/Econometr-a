# V14 · Tareas del autor (en orden; revisado en V14.2)

Todo queda **pendiente del autor**: hacen falta permisos en GitHub, Zenodo y OSF y decisiones que no se toman por él. No se anota ninguna fecha de publicación hasta que exista.

Antes de empezar:
- Trabaje en su máquina, con un clon COMPLETO de Econometr-a (`git fetch --unshallow` si hace falta) y `gh` autenticado.
- La integración de Zenodo con GitHub debe estar **DESACTIVADA** para los dos repositorios. El depósito se sube a mano.
- Sustituye a docs/v13/tareas_autor.md, puntos 1-6. El bloque 3.2 de ese fichero sigue siendo el que crea las etiquetas.

```bash
git clone https://github.com/Phraselium/Econometr-a.git econometr-a && cd econometr-a
git checkout claude/housing-price-spain-econometric-95dhj3
```

## A. Calcular la huella de data/sealed
Desde la raíz de Econometr-a, en la máquina donde está data/sealed:
```bash
find data/sealed -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum
```
1. Escriba los 64 caracteres hexadecimales en proyecto.json, en `hash_sellado.valor`, y la fecha en `hash_sellado.fecha`.
2. Mientras siga «PENDIENTE», `make check` avisa en Econometr-a y **falla en el árbol público** (src/v14/check_v14.py).

## B. Leer las licencias y fijar terceros_1_0
1. Lea docs/v14/licencias.md:
   - citas literales de las condiciones de Registradores, Notariado y AEAT;
   - respuestas CLARO / AMBIGUO / NO CONSTA;
   - recomendación, pendiente de su decisión.

   Copias de las páginas: docs/v14/licencias/.
2. Lea también:
   - docs/v14/escenarios.md: qué cambia con cada valor (ids, páginas, tamaño del paquete);
   - docs/v14/cifras_terceros.md: qué cifras dependen de cada fuente.
3. Edite proyecto.json → `terceros_1_0`, con un valor por fuente: `"agregados"`, `"excluir"` o `"redistribuir"`. Hoy vale registradores = agregados, notariado = agregados, aeat = excluir.
4. Si elige «redistribuir» para la AEAT, haga también lo que dice el apartado D4 de «Pendientes», al final.
5. Si decide pedir autorización escrita a CORPME (Anuario ERI) o al CGN, hágalo antes de C. Anote la respuesta en docs/v14/licencias.md.

## C. Regenerar y comprobar
```bash
make metadatos publicacion consulta web
make check                      # único aviso admitido: ninguno si A está hecho
git status --short              # deben aparecer solo proyecto.json y lo regenerado (publicacion/, consulta/, output/v5, output/v10/web_resumen.csv)
git commit -am "1.0: huella de data/sealed y terceros_1_0"
git push origin claude/housing-price-spain-econometric-95dhj3
```
- Si `make check` falla por los tests del árbol (docs/v14/tests_arbol.json) después de cambiar terceros_1_0, regenere el recuento como en docs/v14/arbol_1_0.md («Recuento»):
  ```bash
  python3 src/v14/arbol_publico.py --destino /tmp/arbol-recuento --sin-recuento
  cd /tmp/arbol-recuento && mkdir -p _descarga && cp -r <ruta>/econometr-a/_deposito/vivienda-espana-evidencia-1.0 _descarga/
  make datos && python3 -m pytest tests -q --junitxml=/tmp/junit.xml
  cd <ruta>/econometr-a && python3 src/v14/tests_arbol.py --junit /tmp/junit.xml --commit "$(git rev-parse HEAD)"
  git commit -am "1.0: recuento de tests del árbol"
  ```
  Antes, genere el paquete con el punto 3 (`make paquete_zenodo`).

## 1. Publicar las 18 etiquetas en el remoto de Econometr-a (antes de archivarlo)
Las etiquetas existen solo en el clon de trabajo de la sesión; en el remoto hay 0. En el clon se crean sobre los mismos commits:
```bash
git fetch origin claude/housing-price-spain-econometric-95dhj3
# pegue aquí el bloque 3.2 de docs/v13/tareas_autor.md: la función crear() y sus 18 llamadas (prereg-v2 … prereg-v9-a1b y v5.0 … v8.0),
# con los SHA-1 completos y la comprobación de sha256; omita la línea de v1.0 (va en el repositorio nuevo)
git push origin refs/tags/prereg-v2 refs/tags/prereg-v3 refs/tags/prereg-v5 refs/tags/prereg-v6 refs/tags/prereg-v7 \
  refs/tags/prereg-v8 refs/tags/prereg-v9 refs/tags/prereg-v9-a1 refs/tags/prereg-v9-a1b \
  refs/tags/v5.0 refs/tags/v5.1 refs/tags/v6.0 refs/tags/v6.1 refs/tags/v6.2 refs/tags/v7.0 refs/tags/v7.1 refs/tags/v7.2 refs/tags/v8.0
git ls-remote --tags origin | grep -c -v '\^{}'   # 18
```
Opcional: las etiquetas de las versiones internas que no la tienen (v8.1, v9.0, v10.0, v11.0, v12.0), con los commits de la tabla de docs/v13/tareas_autor.md.

## 2. Crear el repositorio vivienda-espana-evidencia y subir main
El árbol se genera desde el último commit de Econometr-a, el de C. Es un repositorio git nuevo con un único commit, «Versión 1.0».
```bash
cd econometr-a
make paquete_zenodo                                   # paquete del punto 3, para probar el árbol
make arbol_publico DEST=../vivienda-espana-evidencia
cd ../vivienda-espana-evidencia
git log --oneline                                     # un único commit: «Versión 1.0»
mkdir -p _descarga && cp -r ../econometr-a/_deposito/vivienda-espana-evidencia-1.0 _descarga/
make datos && make check && make publicacion && git status --short   # check sin errores (con A hecho) y git status vacío
git commit --amend --reset-author --no-edit           # opcional: el commit con su nombre y correo
gh repo create Phraselium/vivienda-espana-evidencia --public --source . --remote origin --push
```

## 3. Crear el depósito en Zenodo con el paquete (sin la integración automática con GitHub)
```bash
cd econometr-a
make paquete_zenodo && python3 src/v13/paquete_zenodo.py --zip
(cd _deposito/vivienda-espana-evidencia-1.0 && sha256sum -c --quiet CHECKSUMS.sha256)
sha256sum _deposito/vivienda-espana-evidencia-1.0.zip   # anótelo aquí: sha256_zip: PENDIENTE
```
En https://zenodo.org/uploads/new:
1. Suba `_deposito/vivienda-espana-evidencia-1.0.zip`.
2. Copie los metadatos de docs/v14/publicacion_1_0/zenodo_metadatos.md:
   - título, autor y afiliación, versión, idioma y palabras clave;
   - las dos descripciones, en español y en inglés;
   - las licencias por parte;
   - los identificadores relacionados. En «is derived from», el commit de origen que imprimió `make arbol_publico`.
3. **Reserve el DOI**, todavía sin publicar.

## 4. Con el DOI: actualizar proyecto.json, regenerar y subir como 1.0.0 con la etiqueta v1.0.0
1. En proyecto.json de Econometr-a ponga:
   - `doi`: el DOI reservado;
   - `zenodo_url_paquete`: `https://zenodo.org/records/<id>/files/vivienda-espana-evidencia-1.0.zip?download=1`;
   - si quiere el número de tres cifras, `version_publica` = «1.0.0». En ese caso cambie también la versión escrita a mano en README.md, LEEME_PRIMERO.md, CLAUDE.md, README_REPLICACION.md e historico/INDICE.md: check_v13 exige que todas las puertas declaren la misma.
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
   sed "s#{{DOI}}#<DOI>#" ../econometr-a/docs/v14/publicacion_1_0/notas_version_github.md | sed '1,/^---$/d' > /tmp/notas_1_0.md
   gh release create v1.0.0 --repo Phraselium/vivienda-espana-evidencia --verify-tag --title "Versión pública 1.0.0" --notes-file /tmp/notas_1_0.md --latest
   ```
5. Publique el depósito en Zenodo y anote aquí la fecha que muestre Zenodo: `fecha_deposito: PENDIENTE`.

## 5. Registro en OSF de los pre-registros
1. Siga docs/v14/publicacion_1_0/osf_registro.md. Contiene:
   - la tabla de las 9 etiquetas, con commits, fechas y sha256;
   - la declaración de que el sello externo es posterior;
   - el bucle `git show` que extrae y comprueba cada documento.
2. Sustituya `{{DOI}}` por el DOI de Zenodo.
3. Anote aquí el DOI y la fecha del registro: `osf_registro: PENDIENTE`.

## 6. Publicar la web desde el repositorio nuevo (GitHub Pages)
1. Siga docs/v14/publicacion_1_0/github_pages.md: Settings → Pages → Source: «GitHub Actions».
2. El workflow .github/workflows/pages.yml trae los datos del depósito (necesita `zenodo_url_paquete` del punto 4). Lance la primera vez:
   ```bash
   gh workflow run web --repo Phraselium/vivienda-espana-evidencia && gh run watch --repo Phraselium/vivienda-espana-evidencia
   ```
3. Compruebe https://phraselium.github.io/vivienda-espana-evidencia/: el pie debe mostrar «Versión 1.0» (o 1.0.0) y el DOI.

## 7. Archivar Econometr-a cuando todo lo anterior esté hecho
```bash
gh repo archive Phraselium/Econometr-a --yes      # o, si prefiere, pasarlo a privado:
# gh repo edit Phraselium/Econometr-a --visibility private --accept-visibility-change-consequences
```
- Si lo pasa a privado, los enlaces de historico/INDICE.md del repositorio nuevo dejan de resolver para el público.
- Archivar lo mantiene legible y sin cambios. Es lo recomendado.

## 8. Enviar la revisión externa
1. Use el texto de docs/v14/publicacion_1_0/correo_revisor.md. Rellene el nombre, el enlace y el DOI.
2. Adjunte revision_externa/guia.md y revision_externa/hoja_revision.xlsx.
3. La muestra se reproduce con `make muestra_revision` (SEED = 20261010).
4. Los errores que aparezcan van a ERRATA.md y a una versión 1.0.x.

## Pendientes que no bloquean la 1.0
- **D4 · AEAT: activar «redistribuir» o «agregados».**
  - Según docs/v14/licencias.md, las condiciones de reutilización de la AEAT lo autorizan con cita y fecha (CLARO). Antes de cambiar `terceros_1_0.aeat`:
    1. Revise que la publicación de cada ejercicio no lleve indicación en contrario: https://sede.agenciatributaria.gob.es/Sede/estadisticas.html.
    2. Añada la cita a docs/v5/licencias_datos.md: «Agencia Estatal de Administración Tributaria, Estadística de los declarantes del IRPF por municipios, ejercicio N, actualizada el [fecha]».
    3. Con «redistribuir», el paquete lleva data/raw/v11/aeat_irpf_municipios/irpf_municipios_cv.csv.gz y las 7 variables `aeat_irpf_*` de hechos.parquet. Con «agregados», solo se publican las 5 cifras CB-C6.
    4. Siga C y regenere el paquete y el árbol.
  - Si ya se publicó la 1.0, suba `version_publica` a 1.0.1 y publique una versión nueva del mismo concepto en Zenodo, no un DOI independiente.
- **Registradores · Anuario ERI.** Las 5 cifras A23-P5 y CA-CT-ratio-triang-2022 a 2025 salen de un producto con «reproducción no permitida» sin permiso escrito (licencias.md). Pida autorización a CORPME o decida retirarlas. Hoy el campo es por fuente; retirarlas exigiría una regla por id en src/v14/terceros_1_0.py.
- **Notariado.** Condiciones AMBIGUAS. Pida autorización escrita al CGN/CIEN. Si no llega, valore «excluir» (6 cifras, entre ellas A23-P2, C1).
- **Huellas de data/sealed (D3):** guarde el sha256 de data/sealed en un fichero versionado (lo hace A).
- **Tareas abiertas de V12:** puntos 3 y 5 de docs/v12/tareas_autor.md.
