# V13 · Tareas del autor (en orden)

Esto solo puede hacerlo el autor, con permisos en GitHub, Zenodo y OSF. **Nada de esto está hecho: todo queda «pendiente del autor».** No se anota ninguna fecha de publicación hasta que exista.

Antes de empezar:
- Trabajar en un clon local **completo**, no superficial. Si hace falta, ejecutar `git fetch --unshallow`.
- Tener `gh` autenticado.
- **Zenodo DESACTIVADO** para el repositorio (https://zenodo.org/account/settings/github/). Si está activo, cada etiqueta publicada generaría un DOI.
- Este guion sustituye a docs/v8_1/publicacion_github.sh, que preparaba una release v8.1. No hay que ejecutarlo.

## 1. Renombrar el repositorio en GitHub
Pendiente del autor.
```bash
gh repo rename vivienda-espana-evidencia --repo Phraselium/Econometr-a --yes
git remote set-url origin https://github.com/Phraselium/vivienda-espana-evidencia.git
git fetch origin --prune
```
- GitHub redirige el nombre antiguo.
- La URL nueva ya está en proyecto.json y en todas las puertas de entrada; `make check` comprueba que no aparece otra.

## 2. Crear la rama main y fusionar
Pendiente del autor.
```bash
git fetch origin claude/housing-price-spain-econometric-95dhj3
# si main no existe en el remoto:
git checkout -B main origin/claude/housing-price-spain-econometric-95dhj3
git push origin main
# si main ya existe: fusionar sin reescribir la historia
# git checkout main && git merge --no-ff origin/claude/housing-price-spain-econometric-95dhj3 && git push origin main
gh repo edit Phraselium/vivienda-espana-evidencia --default-branch main
```
Después, en el clon de main, comprobar el estado:
```bash
make datos_terceros   # con red, una vez
make check            # debe terminar sin errores y sin cambios en git
```

## 3. Publicar las etiquetas de pre-registro y de versión
Pendiente del autor.

### 3.1 Qué etiquetas hay

Las etiquetas existen solo en el clon de trabajo de la sesión. Comprobación del 2026-10-16:
- `git ls-remote --tags origin` devuelve 0 etiquetas: **ninguna existe en el remoto**;
- **todos los commits sí están en el remoto**: `git branch -r --contains` los encuentra en origin/claude/housing-price-spain-econometric-95dhj3.

En un clon nuevo hay que crearlas otra vez sobre los mismos commits.

| Etiqueta | Tipo | Commit (SHA-1) | Fecha del commit | Documento | sha256 del documento en ese commit | En el remoto |
|---|---|---|---|---|---|---|
| prereg-v2 | anotada | 910c42aef06348b884ea70e7b6cdc510d58e48c1 | 2026-10-10T07:13:42Z | docs/v2/hipotesis.md | 3fa640930bd0f645077808b8553a08e85be98196bd723d93c0fb3f40025040cb | no |
| prereg-v3 | ligera | 204c073e9e2c9e0edd6ac23dad7edf3049ba4428 | 2026-10-10T13:33:09Z | docs/v3/hipotesis.md | ee40f73e5e68482ecff3f4b194cd127dd0e6a35c691ac5a79a7b9a500d8e86b5 | no |
| prereg-v5 | anotada | 8803f049c0f46ae4db8a79221470594295931d86 | 2026-10-10T19:11:04Z | docs/v5/prereg_B3.md | 0b5d09d9f0ca778d47329b291884fdd1672d2ecc8046c6ea4369badc7d8030d1 | no |
| prereg-v6 | anotada | a33c167080fbd4b86a9239dcb3744d070e501429 | 2026-10-11T08:47:34Z | docs/v6/hipotesis.md | 9c5d9333e70fcbb9abc12252ad91a6218db92c84cccea020f64be7b53fb5a82d | no |
| prereg-v7 | ligera | 3fad305fc51bbcec67ec9ae298a31c58b8bd0fd0 | 2026-10-12T12:04:36Z | docs/v7/hipotesis.md | e82d61184dcb3d9ddfdda093bbc7e8f35d10d93c5b6a9b449b6d6b59bbde4c86 | no |
| prereg-v8 | ligera | 91e618be1a2d17879808982a1fe87729d7f5afaf | 2026-10-13T08:00:40Z | docs/v8/hipotesis.md | 9e7d28dcb2c2176358c6350547c1e150bcca53a1d2bac3c43362018cdc1cd0d2 | no |
| prereg-v9 | ligera | 2977349e3ed3092a51c8a3ad309140cf0b83dca8 | 2026-10-15T08:22:29Z | docs/v9/hipotesis.md | 845269079a46a6d84f08397fb02c4591aaf387e4a828f250f964f0e0df9872bb | no |
| prereg-v9-a1 | ligera | 9cb2200e7cb487fcd22d9da1e8b40ba68a3303d7 | 2026-10-15T08:32:35Z | docs/v9/hipotesis_addendum_a1.md | 22d9eadab98fe39ab4274cdaf79d3e9a1330b7fa8267a12dc9ed2b7e7e3c083e | no |
| prereg-v9-a1b | ligera | 4639772d1dbac4e01af0e24bc0a8501117fe1324 | 2026-10-15T08:35:36Z | docs/v9/hipotesis_addendum_a1.md | 58a2cb8fd4aabfba49be91c3b800bb892a6d8932f011bf99fcf8f4babb87c540 | no |
| v5.0 | anotada | cc69e026aef8f5ee11288ffa18dae7bcd2937ca1 | 2026-10-10T21:04:57Z | — | — | no |
| v5.1 | anotada | bac2fda92fda1c15e9ec3bfec1c6c7fb21a72771 | 2026-10-11T07:47:55Z | — | — | no |
| v6.0 | anotada | 08d7629c41aa3e4b87c5b10c2d3b5026a2e69003 | 2026-10-11T17:28:41Z | — | — | no |
| v6.1 | ligera | 7a63f9f112d5f8c3179f5dfaed281733bdc6ba2d | 2026-10-11T23:44:51Z | — | — | no |
| v6.2 | ligera | 462ebf1858af597fe1e7e0ade9c0283e09e90efd | 2026-10-12T10:31:02Z | — | — | no |
| v7.0 | ligera | 3d1170cd0a43b4aa215e5371475e653a1a2054f8 | 2026-10-12T16:54:24Z | — | — | no |
| v7.1 | ligera | 7415932b2a3e547bdac7fba5c297d60da6e232f7 | 2026-10-12T21:10:24Z | — | — | no |
| v7.2 | ligera | e7bf435277e630a8109c7c98a7549b186ec466d9 | 2026-10-13T07:13:17Z | — | — | no |
| v8.0 | ligera | 5c689730a53e6ef29fccae483d19ea0ca6f289d6 | 2026-10-13T12:06:50Z | — | — | no |

**Versiones sin etiqueta.** Se proponen estos commits de cierre, todos en el remoto; el autor decide si los etiqueta:

| Etiqueta | Commit de cierre | Mensaje del commit |
|---|---|---|
| v8.1 | fa560be | «V8.1: consulta/version.json con el último commit de output» |
| v10.0 | c0902d7 | «V10: cierre en clon limpio» |
| v9.0 | 880fda6 | «V9: cierre (E7, estado final)» |
| v11.0 | 11c94c6 | «V11-DATOS cierre del histórico» |
| v12.0 | 8645b9b | «V12: cierre en clon limpio verificado» |

Además:
- **v1.0** va en el commit de main que resulte del punto 2.
- Las fechas de las etiquetas no son la prueba de anterioridad. La prueba es el commit (su SHA-1 y su fecha) más el registro externo (OSF y Zenodo, puntos 4 y 5).

### 3.2 Comandos exactos
Desde la raíz del clon, ya en main:
```bash
set -e
crear() { git rev-parse -q --verify "refs/tags/$1" >/dev/null || git tag -a "$1" "$2" -m "$3"; \
          [ "$(git rev-parse "$1^{commit}")" = "$(git rev-parse "$2^{commit}")" ] || { echo "ERROR: $1 no apunta a $2"; exit 1; }; }
crear prereg-v2     910c42aef06348b884ea70e7b6cdc510d58e48c1 "Pre-registro v2 (docs/v2/hipotesis.md)"
crear prereg-v3     204c073e9e2c9e0edd6ac23dad7edf3049ba4428 "Pre-registro v3 (docs/v3/hipotesis.md)"
crear prereg-v5     8803f049c0f46ae4db8a79221470594295931d86 "Pre-registro v5, B3 (docs/v5/prereg_B3.md)"
crear prereg-v6     a33c167080fbd4b86a9239dcb3744d070e501429 "Pre-registro v6 (docs/v6/hipotesis.md)"
crear prereg-v7     3fad305fc51bbcec67ec9ae298a31c58b8bd0fd0 "Pre-registro V7 (docs/v7/hipotesis.md)"
crear prereg-v8     91e618be1a2d17879808982a1fe87729d7f5afaf "Pre-registro V8 (docs/v8/hipotesis.md)"
crear prereg-v9     2977349e3ed3092a51c8a3ad309140cf0b83dca8 "Pre-registro V9 (docs/v9/hipotesis.md)"
crear prereg-v9-a1  9cb2200e7cb487fcd22d9da1e8b40ba68a3303d7 "Addendum A1 al pre-registro V9"
crear prereg-v9-a1b 4639772d1dbac4e01af0e24bc0a8501117fe1324 "Addendum A1, re-revisión aprobada"
crear v5.0 cc69e026aef8f5ee11288ffa18dae7bcd2937ca1 "v5.0 (interna)"
crear v5.1 bac2fda92fda1c15e9ec3bfec1c6c7fb21a72771 "v5.1 (interna)"
crear v6.0 08d7629c41aa3e4b87c5b10c2d3b5026a2e69003 "v6.0 (interna)"
crear v6.1 7a63f9f112d5f8c3179f5dfaed281733bdc6ba2d "v6.1 (interna)"
crear v6.2 462ebf1858af597fe1e7e0ade9c0283e09e90efd "v6.2 (interna)"
crear v7.0 3d1170cd0a43b4aa215e5371475e653a1a2054f8 "v7.0 (interna)"
crear v7.1 7415932b2a3e547bdac7fba5c297d60da6e232f7 "v7.1 (interna)"
crear v7.2 e7bf435277e630a8109c7c98a7549b186ec466d9 "v7.2 (interna)"
crear v8.0 5c689730a53e6ef29fccae483d19ea0ca6f289d6 "v8.0 (interna)"
# opcionales (versiones internas sin etiqueta; ver la tabla anterior)
# crear v8.1 fa560be "v8.1 (interna)";  crear v9.0 880fda6 "V9 (interna)";  crear v10.0 c0902d7 "V10 (interna)"
# crear v11.0 11c94c6 "V11 (interna)";  crear v12.0 8645b9b "V12 (interna)"
crear v1.0 "$(git rev-parse origin/main)" "Versión pública 1.0"
# comprobar el documento del pre-registro de cada etiqueta (debe coincidir con la tabla)
for p in prereg-v2:docs/v2/hipotesis.md prereg-v3:docs/v3/hipotesis.md prereg-v5:docs/v5/prereg_B3.md prereg-v6:docs/v6/hipotesis.md \
         prereg-v7:docs/v7/hipotesis.md prereg-v8:docs/v8/hipotesis.md prereg-v9:docs/v9/hipotesis.md \
         prereg-v9-a1:docs/v9/hipotesis_addendum_a1.md prereg-v9-a1b:docs/v9/hipotesis_addendum_a1.md; do
  printf '%s  %s\n' "$(git show "$p" | sha256sum | cut -c1-64)" "$p"; done
# publicar (Zenodo sigue DESACTIVADO)
git push origin refs/tags/prereg-v2 refs/tags/prereg-v3 refs/tags/prereg-v5 refs/tags/prereg-v6 refs/tags/prereg-v7 \
  refs/tags/prereg-v8 refs/tags/prereg-v9 refs/tags/prereg-v9-a1 refs/tags/prereg-v9-a1b \
  refs/tags/v5.0 refs/tags/v5.1 refs/tags/v6.0 refs/tags/v6.1 refs/tags/v6.2 refs/tags/v7.0 refs/tags/v7.1 refs/tags/v7.2 refs/tags/v8.0
git ls-remote --tags origin   # deben aparecer todas
```
v1.0 se publica en el punto 4, junto con la release.

## 4. Crear el depósito en Zenodo
Pendiente del autor.

**Recomendación: subir a mano el paquete de `make paquete_zenodo`.** No conviene archivar con la integración de GitHub, porque archiva el repositorio entero y este incluye:
- derivados con series de Notariado y Registradores (D5);
- variables de la AEAT con la licencia por confirmar (D4).

El paquete los excluye (docs/v13/datos_deposito.md).

1. Resolver D4 y D5 (docs/v13/decisiones.md). Si cambian las exclusiones, ajustar src/v13/paquete_zenodo.py.
2. Generar el paquete en el clon de main:
   ```bash
   make paquete_zenodo && python3 src/v13/paquete_zenodo.py --zip
   cd _deposito/vivienda-espana-evidencia-1.0 && sha256sum -c --quiet CHECKSUMS.sha256 && cd -
   ```
3. En https://zenodo.org/uploads/new:
   - subir `_deposito/vivienda-espana-evidencia-1.0.zip`;
   - copiar los metadatos de .zenodo.json: título, autor, versión 1.0, licencia MIT + CC BY 4.0, idioma y palabras clave;
   - poner como identificador relacionado la URL del repositorio («is supplement to»);
   - **reservar el DOI** antes de publicar.
4. Escribir el DOI reservado en proyecto.json (campo `doi`) y regenerar:
   ```bash
   make metadatos publicacion consulta && make check
   git commit -am "1.0: DOI de Zenodo" && git push origin main
   git tag -a v1.0 "$(git rev-parse HEAD)" -m "Versión pública 1.0" -f   # solo si v1.0 aún no se ha publicado
   git push origin refs/tags/v1.0
   gh release create v1.0 --repo Phraselium/vivienda-espana-evidencia --verify-tag --title "Versión pública 1.0" \
     --notes-file CHANGELOG.md --latest
   ```
5. Publicar el depósito en Zenodo y anotar aquí la fecha de publicación que muestre Zenodo: `fecha_deposito: PENDIENTE`.
6. Opcional, después: la propuesta D2, sacar data/raw del árbol de trabajo para que `make all` lo recupere del DOI.

## 5. Registro en OSF
Pendiente del autor.
1. Crear un proyecto en https://osf.io: «Vivienda en España: base de evidencia reproducible».
2. Crear un registro de tipo «Open-Ended Registration» con el texto siguiente.
3. Adjuntar los ficheros del pre-registro tal como están en sus commits:
   ```bash
   git show prereg-v9:docs/v9/hipotesis.md > hipotesis_v9.md
   ```
   y lo mismo para cada fila de la tabla 3.1.
4. Anotar aquí la fecha y el DOI del registro de OSF: `osf_registro: PENDIENTE`.

Texto propuesto para el registro (sin fechas de publicación: las pone OSF):

> **Título:** Pre-registros del proyecto «Vivienda en España: base de evidencia reproducible» (v2-V9)
>
> **Autor:** Borja Romero, economista (firma individual, independiente).
>
> **Descripción:**
> - Este registro deja constancia externa de los pre-registros de análisis del proyecto. Cada uno se fijó en un commit de git antes de estimar los modelos a los que se refiere.
> - El registro no añade hipótesis nuevas. Solo fecha y fija, con su huella criptográfica, documentos que ya existen en el repositorio público https://github.com/Phraselium/vivienda-espana-evidencia.
> - La anterioridad respecto a los resultados se prueba con tres elementos:
>   - el commit (SHA-1) y su fecha;
>   - el sha256 del documento en ese commit;
>   - la etiqueta `prereg-*` publicada en el repositorio.
>
> **Documentos registrados** (etiqueta · commit · documento · sha256):
> - prereg-v2 · 910c42aef06348b884ea70e7b6cdc510d58e48c1 · docs/v2/hipotesis.md · 3fa640930bd0f645077808b8553a08e85be98196bd723d93c0fb3f40025040cb
> - prereg-v3 · 204c073e9e2c9e0edd6ac23dad7edf3049ba4428 · docs/v3/hipotesis.md · ee40f73e5e68482ecff3f4b194cd127dd0e6a35c691ac5a79a7b9a500d8e86b5
> - prereg-v5 · 8803f049c0f46ae4db8a79221470594295931d86 · docs/v5/prereg_B3.md · 0b5d09d9f0ca778d47329b291884fdd1672d2ecc8046c6ea4369badc7d8030d1
> - prereg-v6 · a33c167080fbd4b86a9239dcb3744d070e501429 · docs/v6/hipotesis.md · 9c5d9333e70fcbb9abc12252ad91a6218db92c84cccea020f64be7b53fb5a82d
> - prereg-v7 · 3fad305fc51bbcec67ec9ae298a31c58b8bd0fd0 · docs/v7/hipotesis.md · e82d61184dcb3d9ddfdda093bbc7e8f35d10d93c5b6a9b449b6d6b59bbde4c86
> - prereg-v8 · 91e618be1a2d17879808982a1fe87729d7f5afaf · docs/v8/hipotesis.md · 9e7d28dcb2c2176358c6350547c1e150bcca53a1d2bac3c43362018cdc1cd0d2
> - prereg-v9 · 2977349e3ed3092a51c8a3ad309140cf0b83dca8 · docs/v9/hipotesis.md · 845269079a46a6d84f08397fb02c4591aaf387e4a828f250f964f0e0df9872bb
> - prereg-v9-a1 · 9cb2200e7cb487fcd22d9da1e8b40ba68a3303d7 · docs/v9/hipotesis_addendum_a1.md · 22d9eadab98fe39ab4274cdaf79d3e9a1330b7fa8267a12dc9ed2b7e7e3c083e
> - prereg-v9-a1b · 4639772d1dbac4e01af0e24bc0a8501117fe1324 · docs/v9/hipotesis_addendum_a1.md · 58a2cb8fd4aabfba49be91c3b800bb892a6d8932f011bf99fcf8f4babb87c540
>
> **Evaluaciones diferidas** (todavía no realizadas):
> - V7 y V8 tienen predicciones congeladas que se evaluarán una sola vez con datos posteriores (`make evaluate_v7` y `make evaluate_v8`).
> - La huella de las predicciones de V8 (sha256_predicciones_v8) está en docs/v8/notas_release.md.
>
> **Limitación declarada:**
> - Los commits se hicieron en un repositorio privado de trabajo antes de ser públicos.
> - La fecha del commit la fija quien lo crea. Este registro externo es la primera constancia independiente de esos documentos.
> - Ningún resultado del proyecto alcanza la capa causal (C3/C3s).

## 6. Publicar la web
Pendiente del autor.
1. En GitHub → Settings → Pages: origen «GitHub Actions». El workflow .github/workflows/pages.yml publica en cada push a main.
2. Comprobar que la web responde en https://phraselium.github.io/vivienda-espana-evidencia/ (proyecto.json, campo `web`). El pie de cada página debe mostrar «Versión 1.0» y el DOI del punto 4.
3. Activar el monitor mensual (V10), que abre un pull request y no publica sin revisión.

## Otras decisiones pendientes del autor
- D2: sacar data/raw del árbol tras el depósito (propuesta en docs/v13/decisiones.md).
- D4: licencia de la AEAT.
- D5: derivados con series de Notariado y Registradores.
- Siguen abiertas las tareas 1, 3 y 5 de docs/v12/tareas_autor.md. La 4 se cubre con el punto 6 de esta lista y la 2 está resuelta en V13.
