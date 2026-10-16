"""V14 · `make arbol_publico DEST=../vivienda-espana-evidencia`: árbol limpio de la versión pública en un repositorio git NUEVO.

Qué entra y por qué está en docs/v14/arbol_1_0.md. En resumen:
- entra todo lo versionado aquí salvo las exclusiones de `excluir()`;
- data/ se reduce a los manifiestos y los checksums (los datos vienen del depósito: `make datos`);
- historico/ se sustituye por un índice que enlaza al repositorio de desarrollo archivado y al commit de origen.
Después crea en DEST un repositorio git nuevo con un único commit «Versión 1.0» y escribe la procedencia en el README.
DEST debe no existir o estar vacío. No lee datos no redistribuibles ni data/sealed. Sin red.
Uso: python3 src/v14/arbol_publico.py --destino ../vivienda-espana-evidencia [--sin-git]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v14 import terceros as T  # noqa: E402

P = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
DATOS_QUE_ENTRAN = re.compile(r"^data/(CHECKSUMS\.sha256|raw/(.+/)?_manifest[^/]*\.csv)$")
PRIVADO = re.compile(r"/tmp/claude|/home/user|/root/|claude\.ai/code/session|session_0[0-9A-Za-z]{10,}|ghp_[A-Za-z0-9]{20,}|"  # arbol_publico: permitido
                     r"github_pat_[A-Za-z0-9_]{20,}|\bsk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{12,}|xox[abp]-[A-Za-z0-9-]{10,}|"  # arbol_publico: permitido
                     r"[A-Za-z0-9._%+-]+@(?!anthropic\.com)[A-Za-z0-9-]+\.[A-Za-z0-9.-]*[a-z]{2,}")  # arbol_publico: permitido
IGNORE_EXTRA = """
# V14 (árbol público): los datos vienen del depósito de Zenodo (`make datos`); solo se versionan manifiestos y checksums
/data/**
!/data/**/
!/data/CHECKSUMS.sha256
!/data/raw/**/_manifest*.csv
/_descarga/
"""


def _git(*a: str, cwd: Path = RAIZ) -> str:
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, check=True).stdout


def excluir(f: str) -> str | None:
    """Motivo de exclusión del fichero versionado f, o None si entra."""
    if f.startswith("data/"):
        return None if DATOS_QUE_ENTRAN.match(f) else "datos: vienen del depósito de Zenodo (`make datos`) o de `make datos_terceros`"
    if f.startswith("historico/"):
        return "histórico de desarrollo: queda en el repositorio archivado (historico/INDICE.md enlaza al commit de origen)"
    if f.startswith(".claude/"):
        return "configuración de los agentes de trabajo de la sesión de desarrollo"
    return None


def seleccionar() -> tuple[list[str], list[tuple[str, str]]]:
    inc, exc = [], []
    for f in sorted(x for x in _git("ls-files", "-z").split("\0") if x and (RAIZ / x).is_file()):
        m = excluir(f)
        (exc.append((f, m)) if m else inc.append(f))
    return inc, exc


def indice_historico(commit: str, fecha: str) -> str:
    dev = P["repositorio_desarrollo"]
    return f"""# Histórico de desarrollo

Este repositorio es el árbol limpio de la versión pública {P['version_publica']}. Los documentos de las versiones internas superadas (v1-V12) y la historia completa de git están en el repositorio de desarrollo, que queda archivado:

- Repositorio de desarrollo: {dev}
- Commit de origen de este árbol: `{commit}` ({fecha})
- Índice del histórico en ese commit: {dev}/blob/{commit}/historico/INDICE.md
- Correspondencia entre versiones internas y versión pública: [CHANGELOG.md](../CHANGELOG.md)

Las etiquetas de pre-registro (`prereg-*`) y de versión interna apuntan a commits de ese repositorio (docs/v14/tareas_autor.md).
"""


def procedencia(commit: str, fecha: str) -> str:
    return (f"\n**Procedencia.** Árbol limpio de la versión pública {P['version_publica']}, generado con `make arbol_publico` desde el repositorio de "
            f"desarrollo {P['repositorio_desarrollo']} (archivado), commit `{commit}` ({fecha}). DOI: {'pendiente' if P['doi'] == 'PENDIENTE' else P['doi']}. "
            "Los datos no se versionan aquí: `make datos` los trae del depósito de Zenodo y verifica sus sha256 (reproducir/instrucciones.md).\n")


def revisar_privacidad(dest: Path) -> list[str]:
    err = []
    for p in sorted(dest.rglob("*")):
        if not p.is_file() or ".git" in p.relative_to(dest).parts:
            continue
        try:
            t = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, ln in enumerate(t.splitlines(), 1):
            if PRIVADO.search(ln) and "arbol_publico: permitido" not in ln:
                err.append(f"{p.relative_to(dest)}:{n}: {PRIVADO.search(ln).group(0)[:60]}")
    return err


def construir(dest: Path, con_git: bool = True) -> dict:
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"arbol_publico: {dest} existe y no está vacío")
    commit = _git("rev-parse", "HEAD").strip()
    fecha = _git("log", "-1", "--format=%cs", commit).strip()
    inc, exc = seleccionar()
    redactadas = []
    for f in inc:
        d = dest / f
        d.parent.mkdir(parents=True, exist_ok=True)
        quitar = T.a_redactar(f, RAIZ / f)
        if quitar:   # tabla propia con columnas de Notariado, Registradores o AEAT: se copia sin ellas (D5, D4)
            T.redactar(RAIZ / f, d, quitar)
            redactadas.append((f, "redactada: sin las columnas " + " ".join(quitar)))
        else:
            shutil.copyfile(RAIZ / f, d)
    (dest / "historico").mkdir(exist_ok=True)
    (dest / "historico" / "INDICE.md").write_text(indice_historico(commit, fecha), encoding="utf-8")
    readme = (dest / "README.md").read_text(encoding="utf-8").split("\n")
    (dest / "README.md").write_text("\n".join(readme[:1] + procedencia(commit, fecha).split("\n") + readme[1:]), encoding="utf-8")
    (dest / ".gitignore").write_text((dest / ".gitignore").read_text(encoding="utf-8").rstrip("\n") + "\n" + IGNORE_EXTRA, encoding="utf-8")
    (dest / "docs" / "v14").mkdir(parents=True, exist_ok=True)
    with (dest / "docs" / "v14" / "excluidos_arbol.csv").open("w", encoding="utf-8") as fh:
        fh.write("fichero,motivo\n" + "".join(f'"{f}","{m}"\n' for f, m in exc + redactadas))
    priv = revisar_privacidad(dest)
    if priv:
        raise SystemExit("arbol_publico: datos personales o rutas locales en el árbol:\n  " + "\n  ".join(priv[:20]))
    if con_git:
        _git("init", "-q", "-b", "main", cwd=dest)
        _git("add", "-A", cwd=dest)
        _git("commit", "-q", "-m", f"Versión {P['version_publica']}\n\nÁrbol limpio generado con `make arbol_publico` desde "
             f"{P['repositorio_desarrollo']} (commit {commit}).", cwd=dest)
    return {"incluidos": len(inc) + 1, "excluidos": len(exc), "redactadas": len(redactadas), "commit_origen": commit}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--destino", required=True)
    ap.add_argument("--sin-git", action="store_true")
    a = ap.parse_args()
    dest = Path(a.destino).resolve()
    r = construir(dest, not a.sin_git)
    print(f"arbol_publico: {dest} · {r['incluidos']} ficheros, {r['excluidos']} versionados excluidos, {r['redactadas']} tablas redactadas, "
          f"origen {r['commit_origen'][:7]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
