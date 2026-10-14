#!/usr/bin/env bash
# V8.1 · Bloque E: publicación en GitHub en DOS FASES. Ejecutar EN LOCAL, con `gh` autenticado y permisos de escritura,
# desde la raíz de un clon COMPLETO (no superficial) del repositorio. Instrucciones: docs/v8_1/INSTRUCCIONES_PUBLICACION.md
#
#   bash docs/v8_1/publicacion_github.sh fase1   # Zenodo DESACTIVADO: renombrar, main, rama por defecto, etiquetas y
#                                                 # releases de las versiones antiguas. Termina en PAUSA.
#   bash docs/v8_1/publicacion_github.sh fase2   # Zenodo ACTIVADO: release v8.1, DOI y fechas verificables.
#
# Cada acción irreversible pide confirmación [s/N]. No reescribe el historial ni hace force-push.
set -euo pipefail

PROPIETARIO="Phraselium"
NOMBRE_ANTIGUO="Econometr-a"
NOMBRE_NUEVO="vivienda-espana-evidencia"
RAMA_TRABAJO="claude/housing-price-spain-econometric-95dhj3"
# etiqueta -> commit (v8.1 = main final, se resuelve en la fase 1)
ETIQUETAS=(prereg-v7 v7.0 v7.1 prereg-v8 v8.0)
declare -A COMMIT=( [prereg-v7]=3fad305 [v7.0]=3d1170c [v7.1]=7415932 [prereg-v8]=91e618b [v8.0]=5c68973 )
RELEASES_ANTIGUAS=(prereg-v7 v7.0 prereg-v8 v8.0)

confirmar() { local r; read -r -p "$1 [s/N] " r; [[ "$r" =~ ^[sS]$ ]]; }
paso() { printf '\n=== %s ===\n' "$1"; }

repo_actual() {   # el que exista en GitHub: el nombre nuevo si ya se renombró
  if gh repo view "$PROPIETARIO/$NOMBRE_NUEVO" >/dev/null 2>&1; then echo "$PROPIETARIO/$NOMBRE_NUEVO"
  else echo "$PROPIETARIO/$NOMBRE_ANTIGUO"; fi
}

comprobaciones() {
  paso "Comprobaciones iniciales"
  command -v gh >/dev/null && command -v git >/dev/null && command -v python3 >/dev/null || { echo "Faltan gh, git o python3"; exit 1; }
  gh auth status
  [ "$(git rev-parse --is-shallow-repository)" = "false" ] || { echo "El clon es superficial: ejecuta 'git fetch --unshallow' y repite."; exit 1; }
  git fetch origin --prune
  for t in "${ETIQUETAS[@]}"; do
    c=${COMMIT[$t]}
    git cat-file -e "$c^{commit}" 2>/dev/null || { echo "No existe el commit $c ($t) en este clon"; exit 1; }
    git branch -r --contains "$c" | grep -q . || { echo "El commit $c ($t) no está en ninguna rama remota"; exit 1; }
  done
  echo "Clon completo; los commits ${COMMIT[*]} existen y están en el remoto."
}

fase1() {
  comprobaciones
  REPO=$(repo_actual)
  echo "Repositorio: $REPO. ANTES DE SEGUIR: la integración con Zenodo debe estar DESACTIVADA para este repositorio."
  confirmar "¿Zenodo está desactivado para el repositorio?" || { echo "Desactívalo en https://zenodo.org/account/settings/github/ y vuelve a ejecutar."; exit 1; }

  paso "1. Renombrar el repositorio"
  if [ "$REPO" = "$PROPIETARIO/$NOMBRE_ANTIGUO" ] && confirmar "¿Renombrar $REPO a $PROPIETARIO/$NOMBRE_NUEVO? (GitHub redirige el nombre antiguo)"; then
    gh repo rename "$NOMBRE_NUEVO" --repo "$REPO" --yes
    REPO="$PROPIETARIO/$NOMBRE_NUEVO"
  fi
  git remote set-url origin "https://github.com/$REPO.git"
  git fetch origin --prune

  paso "2. Rama main con el estado final y rama por defecto"
  echo "main apuntará a origin/$RAMA_TRABAJO = $(git rev-parse --short "origin/$RAMA_TRABAJO")"
  if confirmar "¿Crear o actualizar main en el remoto (sin force-push)?"; then
    git branch -f main "origin/$RAMA_TRABAJO"
    git push origin main
  fi
  if confirmar "¿Poner main como rama por defecto de $REPO?"; then
    gh repo edit "$REPO" --default-branch main
  fi
  git fetch origin main
  COMMIT[v8.1]=$(git rev-parse --short origin/main)

  paso "3. Etiquetas"
  for t in "${ETIQUETAS[@]}" v8.1; do
    c=${COMMIT[$t]}
    if git rev-parse -q --verify "refs/tags/$t" >/dev/null; then
      [ "$(git rev-parse "$t^{commit}")" = "$(git rev-parse "$c^{commit}")" ] || { echo "La etiqueta local $t no apunta a $c: corrígela a mano"; exit 1; }
    else
      git tag -a "$t" "$c" -m "$t"
    fi
    echo "  $t -> $c"
  done
  if confirmar "¿Publicar estas seis etiquetas en el remoto?"; then
    for t in "${ETIQUETAS[@]}" v8.1; do git push origin "refs/tags/$t"; done
  fi

  paso "4. Releases de las versiones antiguas (Zenodo desactivado: no generan DOI)"
  notas_v8=$(mktemp); { cat docs/v8/cierre_proyecto.md; echo; echo "Notas de la release del pre-registro: docs/v8/notas_release.md"; } > "$notas_v8"
  if confirmar "¿Crear las releases prereg-v7, v7.0, prereg-v8 y v8.0 (ninguna marcada como latest)?"; then
    gh release create prereg-v7 --repo "$REPO" --verify-tag --title "Pre-registro V7" --notes-file docs/v7/notas_release.md --latest=false
    gh release create v7.0 --repo "$REPO" --verify-tag --title "V7.0" --notes-file docs/v7_1/release_notes.md --latest=false
    gh release create prereg-v8 --repo "$REPO" --verify-tag --title "Pre-registro V8 (atribución por periodos)" --notes-file docs/v8/notas_release.md --latest=false
    gh release create v8.0 --repo "$REPO" --verify-tag --title "V8.0: por qué ha subido (factores, periodos y factor común)" --notes-file "$notas_v8" --latest=false
  fi
  for t in "${RELEASES_ANTIGUAS[@]}"; do
    printf "  %-10s published_at=%s\n" "$t" "$(gh release view "$t" --repo "$REPO" --json publishedAt -q .publishedAt 2>/dev/null || echo '(sin release)')"
  done

  paso "PAUSA"
  echo "Fase 1 terminada. Ahora ACTIVA Zenodo para $REPO en https://zenodo.org/account/settings/github/"
  echo "(interruptor del repositorio en ON). Después ejecuta:  bash docs/v8_1/publicacion_github.sh fase2"
}

escribir_campo() {   # escribir_campo fichero clave valor : sustituye «clave: ...» en ficheros de notas
  python3 - "$1" "$2" "$3" <<'PY'
import re, sys
p, k, v = sys.argv[1:]
s = open(p, encoding="utf-8").read()
s2, n = re.subn(rf"^{re.escape(k)}:.*$", f"{k}: {v}", s, flags=re.M)
if n == 0:
    s2 = s.rstrip("\n") + f"\n{k}: {v}\n"
open(p, "w", encoding="utf-8").write(s2)
PY
}

fase2() {
  comprobaciones
  REPO=$(repo_actual)
  confirmar "¿Zenodo está ACTIVADO para $REPO?" || { echo "Actívalo primero (fase 1, PAUSA)."; exit 1; }
  git rev-parse -q --verify refs/tags/v8.1 >/dev/null || { echo "Falta la etiqueta v8.1: ejecuta antes la fase 1."; exit 1; }
  git checkout main && git merge --ff-only origin/main
  [ -z "$(git status --porcelain)" ] || { echo "Hay cambios sin confirmar en el árbol de trabajo: resuélvelos antes."; exit 1; }
  make datos_terceros   # los datos de terceros no versionados hacen falta para `make check`

  paso "5. Release v8.1 (latest)"
  if confirmar "¿Crear la release v8.1, marcada como latest? Zenodo la archivará y le dará un DOI."; then
    gh release create v8.1 --repo "$REPO" --verify-tag --title "V8.1: coherencia, capa de consulta y datos de terceros" \
      --notes-file docs/v8_1/notas_release_v81.md --latest
  fi

  paso "6. DOI en Zenodo"
  DOI=""; FECHA_DOI=""
  for i in $(seq 1 20); do
    resp=$(curl -s "https://zenodo.org/api/records?q=%22${NOMBRE_NUEVO}%22&sort=mostrecent&size=20" || true)
    read -r DOI FECHA_DOI < <(printf '%s' "$resp" | python3 -c '
import json, sys
try:
    hits = json.load(sys.stdin).get("hits", {}).get("hits", [])
except Exception:
    hits = []
for h in hits:
    md = h.get("metadata", {})
    if str(md.get("version", "")).lstrip("v") == "8.1":
        print(h.get("doi", ""), md.get("publication_date", "")); break
else:
    print("", "")') || true
    [ -n "$DOI" ] && break
    echo "  DOI aún no visible (intento $i/20); espero 30 s..."; sleep 30
  done
  FV7=$(gh release view prereg-v7 --repo "$REPO" --json publishedAt -q .publishedAt | cut -c1-10)
  FV8=$(gh release view prereg-v8 --repo "$REPO" --json publishedAt -q .publishedAt | cut -c1-10)
  F81=$(gh release view v8.1 --repo "$REPO" --json publishedAt -q .publishedAt | cut -c1-10)
  echo "  DOI v8.1: ${DOI:-PENDIENTE} (${FECHA_DOI:-sin fecha})"
  echo "  fecha_verificable: prereg-v7 $FV7 · prereg-v8 $FV8 (published_at de la release en GitHub)"
  confirmar "¿Escribir estas fechas y el DOI en notas de release, CITATION.cff, README y consulta/version.json?" || exit 0

  escribir_campo docs/v7/notas_release.md fecha_verificable "$FV7"
  escribir_campo docs/v8/notas_release.md fecha_verificable "$FV8"
  escribir_campo docs/v7/notas_release.md doi "${DOI:-PENDIENTE}"
  escribir_campo docs/v8/notas_release.md doi "${DOI:-PENDIENTE}"
  python3 - "${DOI:-}" "$F81" <<'PY'
import re, sys
doi, fecha = sys.argv[1:]
c = open("CITATION.cff", encoding="utf-8").read()
c = re.sub(r'^date-released:.*$', f'date-released: "{fecha}"', c, flags=re.M)
if doi and "\ndoi:" not in c:
    c = c.replace('\nversion: ', f'\ndoi: "{doi}"\nversion: ', 1)
open("CITATION.cff", "w", encoding="utf-8").write(c)
r = open("README.md", encoding="utf-8").read()
if doi:
    badge = f"[![DOI](https://zenodo.org/badge/DOI/{doi}.svg)](https://doi.org/{doi})"
    r = r.replace("**DOI:** pendiente (Zenodo).", f"**DOI:** [{doi}](https://doi.org/{doi}) {badge}")
open("README.md", "w", encoding="utf-8").write(r)
PY
  make consulta
  make publicacion
  python3 -c "import sys; sys.path.insert(0,'src/v8'); import evaluate_v8 as e; f=e.fecha_verificable(); ok=bool(f) and f.upper()!='PENDIENTE'; r=e.congelacion_anterior(f) if ok else (False,'PENDIENTE'); print('evaluate_v8 acepta la fecha:', f, '|', r[1]); sys.exit(0 if ok and r[0] else 1)"
  make check
  git add docs/v7/notas_release.md docs/v8/notas_release.md CITATION.cff README.md consulta llms.txt publicacion metodologia reproducir
  git commit -m "V8.1: fechas verificables y DOI tras la publicación"
  if confirmar "¿Subir este commit a main?"; then git push origin HEAD:main; fi

  paso "7. Ramas de trabajo ya fusionadas en main"
  git fetch origin --prune
  mapfile -t RAMAS < <(git branch -r --merged origin/main | sed 's#^ *origin/##' | grep -v -e '^main$' -e '^HEAD')
  printf '  %s\n' "${RAMAS[@]:-}"
  echo "No se borra nada sin un «s» explícito para cada rama."
  for b in "${RAMAS[@]:-}"; do
    [ -n "$b" ] && confirmar "  ¿Borrar origin/$b?" && git push origin --delete "$b"
  done
}

case "${1:-}" in
  fase1) fase1 ;;
  fase2) fase2 ;;
  *) echo "Uso: bash docs/v8_1/publicacion_github.sh fase1|fase2  (ver docs/v8_1/INSTRUCCIONES_PUBLICACION.md)"; exit 2 ;;
esac
