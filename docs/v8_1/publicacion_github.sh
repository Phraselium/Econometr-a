#!/usr/bin/env bash
# V8.1 · Bloque E: publicación en GitHub. Para ejecutar EN LOCAL, con `gh` autenticado y permisos de escritura.
# Cada acción irreversible pide confirmación. Uso:  bash docs/v8_1/publicacion_github.sh
# No reescribe el historial ni hace force-push. Requiere: git, gh, curl, python3.
set -euo pipefail

REPO_ACTUAL="Phraselium/Econometr-a"
NOMBRE_PROPUESTO="vivienda-espana-evidencia"
RAMA_TRABAJO="claude/housing-price-spain-econometric-95dhj3"

confirmar() { read -r -p "$1 [s/N] " r; [[ "$r" =~ ^[sS]$ ]]; }

gh auth status
git fetch origin "$RAMA_TRABAJO"

# 1. Rama main con el estado final y rama por defecto
if confirmar "1. ¿Crear/actualizar la rama main en origin con origin/$RAMA_TRABAJO y subirla?"; then
  git branch -f main "origin/$RAMA_TRABAJO"
  git push origin main
fi
if confirmar "1b. ¿Cambiar la rama por defecto del repositorio a main?"; then
  gh repo edit "$REPO_ACTUAL" --default-branch main
fi

# 2. Renombrar el repositorio (opcional)
if confirmar "2. ¿Renombrar $REPO_ACTUAL a $NOMBRE_PROPUESTO?"; then
  gh repo rename "$NOMBRE_PROPUESTO" --repo "$REPO_ACTUAL" --yes
  REPO_ACTUAL="Phraselium/$NOMBRE_PROPUESTO"
  git remote set-url origin "https://github.com/$REPO_ACTUAL"
  echo "Después: actualiza README.md, CITATION.cff (repository-code) y enlaces internos al nuevo nombre (grep -rn Econometr-a)."
fi

# 3. Etiquetas (comprueba que cada commit está en el remoto)
declare -A ETQ=( [prereg-v7]=3fad305 [v7.0]=3d1170c [v7.1]=7415932 [prereg-v8]=91e618b [v8.0]=5c68973 )
ETQ[v8.1]=$(git rev-parse --short origin/main)
for t in prereg-v7 v7.0 v7.1 prereg-v8 v8.0 v8.1; do
  c=${ETQ[$t]}
  git branch -r --contains "$c" | grep -q . || { echo "El commit $c de $t no está en el remoto"; exit 1; }
  git rev-parse -q --verify "refs/tags/$t" >/dev/null || git tag "$t" "$c"
  [ "$(git rev-parse --short "$t^{commit}")" = "$(git rev-parse --short "$c")" ] || { echo "La etiqueta local $t no apunta a $c"; exit 1; }
done
if confirmar "3. ¿Publicar las etiquetas (git push origin --tags)?"; then
  git push origin --tags
fi

# 4. Releases (la última, latest)
if confirmar "4. ¿Crear las releases prereg-v7, v7.0, prereg-v8, v8.0 y v8.1?"; then
  gh release create prereg-v7 --repo "$REPO_ACTUAL" --title "Pre-registro V7" --notes-file docs/v7/notas_release.md --latest=false
  gh release create v7.0 --repo "$REPO_ACTUAL" --title "V7.0" --notes-file docs/v7_1/release_notes.md --latest=false
  gh release create prereg-v8 --repo "$REPO_ACTUAL" --title "Pre-registro V8 (atribución por periodos)" --notes-file docs/v8/notas_release.md --latest=false
  gh release create v8.0 --repo "$REPO_ACTUAL" --title "V8.0: por qué ha subido (factores, periodos y factor común)" --notes-file docs/v8/cierre_proyecto.md --latest=false
  gh release create v8.1 --repo "$REPO_ACTUAL" --title "V8.1: coherencia, capa de consulta y datos de terceros" --notes-file docs/v8_1/notas_release_v81.md --latest
fi

# 5. Fechas verificables y DOI (Zenodo tarda unos minutos tras cada release)
echo "Esperando 5 minutos a Zenodo..."; sleep 300
for t in prereg-v7 v7.0 prereg-v8 v8.0 v8.1; do
  printf "%s published_at=%s\n" "$t" "$(gh release view "$t" --repo "$REPO_ACTUAL" --json publishedAt -q .publishedAt)"
done
curl -s "https://zenodo.org/api/records?q=$(basename "$REPO_ACTUAL")&sort=mostrecent&size=20" \
  | python3 -c 'import json,sys; [print(h["metadata"].get("version"), h.get("doi"), h["metadata"].get("publication_date")) for h in json.load(sys.stdin).get("hits",{}).get("hits",[])]'
echo "6. Escribe fecha_verificable (DOI o published_at) y DOI en docs/v7/notas_release.md, docs/v8/notas_release.md,"
echo "   CITATION.cff y README; ejecuta \`make consulta\` (consulta/version.json) y \`make check\`; comprueba que"
echo "   \`python3 src/v8/evaluate_v8.py\` ya no rechaza la fecha (sale por «aún no hay datos», sin abrir). Commit y push a main."

# 7. Ramas de trabajo fusionadas (no se borra nada sin confirmación explícita, una a una)
echo "Ramas remotas ya contenidas en main:"
git branch -r --merged origin/main | grep -v -e "origin/main$" -e HEAD || true
if confirmar "7. ¿Revisar el borrado, una a una, de esas ramas remotas?"; then
  for b in $(git branch -r --merged origin/main | grep -v -e "origin/main$" -e HEAD | sed 's#origin/##'); do
    confirmar "   ¿Borrar origin/$b?" && git push origin --delete "$b"
  done
fi
