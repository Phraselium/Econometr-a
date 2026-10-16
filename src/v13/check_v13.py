"""Comprobaciones de puerta V13 (entran en `make check`). Sin red; no escribe nada.

1. Versión vigente única: ninguna puerta de entrada declara una «versión pública / de referencia / vigente / de consulta» ni un
   «**Versión:**» distinto de proyecto.json; las puertas principales declaran la versión pública; los campos «version» de
   CITATION.cff, .zenodo.json y consulta/*.json coinciden.
2. URL única: toda URL github.com/Phraselium/... o phraselium.github.io/... de los ficheros versionados es la configurada en
   proyecto.json (repositorio y web; desde V14 también el repositorio de desarrollo archivado, `repositorio_desarrollo`).
3. Metadatos generados: CITATION.cff y .zenodo.json son los que genera src/v13/metadatos.py.
4. Cifras: ninguna cifra de output/v5/cifras_clave.csv cambia, desaparece ni se añade respecto a las huellas de
   docs/v13/cifras_base_v12.csv sin entrada en ERRATA.md (mismo criterio que check_v9).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ))
import check_v8 as C8  # noqa: E402

from src.v13 import metadatos  # noqa: E402

P = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
VP = P["version_publica"]

# puertas de entrada (rutas o carpetas, relativas a la raíz); las PRINCIPALES deben declarar la versión pública
PUERTAS = ["README.md", "LEEME_PRIMERO.md", "CLAUDE.md", "llms.txt", "README_REPLICACION.md", "CITATION.cff", ".zenodo.json",
           "consulta", "publicacion", "metodologia", "reproducir", "web/README.md", "web/plantillas", "historico/INDICE.md"]
PRINCIPALES = ["README.md", "LEEME_PRIMERO.md", "CLAUDE.md", "llms.txt", "README_REPLICACION.md", "consulta/LEEME_ASISTENTE.md",
               "historico/INDICE.md", "publicacion/una_pagina.md"]
DECL = re.compile(r"versi[oó]n (?:p[uú]blica|de referencia|vigente|de consulta)[:*`\s]*\(?v?(\d+(?:\.\d+)*)"
                  r"|\*\*versi[oó]n:\*\*\s*`?v?(\d+(?:\.\d+)*)", re.I)
URL_REPO = re.compile(r"https?://(?:www\.)?github\.com/phraselium/[A-Za-z0-9_.-]+", re.I)
URL_WEB = re.compile(r"https?://phraselium\.github\.io/[A-Za-z0-9_./-]*", re.I)
EXT_TEXTO = (".md", ".txt", ".cff", ".json", ".html", ".py", ".yml", ".yaml", ".csv", ".sh", ".qmd", ".bib", ".toml", ".cfg", "")


def _versionados(*rutas: str) -> list[str]:
    r = subprocess.run(["git", "ls-files", "-z", "--", *rutas], cwd=RAIZ, capture_output=True, text=True, check=True)
    return [f for f in r.stdout.split("\0") if f and (RAIZ / f).is_file()]


def version_unica() -> list[str]:
    err = []
    for f in _versionados(*PUERTAS):
        if not f.endswith((".md", ".txt", ".html")):
            continue
        for n, ln in enumerate((RAIZ / f).read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for m in DECL.finditer(ln):
                v = next(g for g in m.groups() if g)
                if v != VP:
                    err.append(f"{f}:{n}: declara la versión {v} (vigente: {VP})")
    for f in PRINCIPALES:
        t = (RAIZ / f).read_text(encoding="utf-8")
        if not any(next(g for g in m.groups() if g) == VP for m in DECL.finditer(t)):
            err.append(f"{f}: no declara la versión pública {VP}")
    campos = {"CITATION.cff": re.search(r'^version:\s*"([^"]+)"', (RAIZ / "CITATION.cff").read_text(encoding="utf-8"), re.M).group(1),
              ".zenodo.json": json.loads((RAIZ / ".zenodo.json").read_text(encoding="utf-8"))["version"]}
    for f in ("consulta/version.json", "consulta/hallazgos.json"):
        campos[f] = json.loads((RAIZ / f).read_text(encoding="utf-8"))["version"]
    err += [f"{f}: version = {v} (vigente: {VP})" for f, v in campos.items() if v != VP]
    return err


def url_unica() -> list[str]:
    repo, web = P["repositorio"].lower(), P["web"].lower()
    admitidas = {repo, P.get("repositorio_desarrollo", repo).lower()}   # V14: el de desarrollo, archivado, también se cita
    err = []
    for f in _versionados("."):
        if not f.endswith(EXT_TEXTO) or f == "proyecto.json":
            continue
        t = (RAIZ / f).read_text(encoding="utf-8", errors="ignore")
        for m in URL_REPO.finditer(t):
            u = m.group(0).rstrip(".").lower()
            u = u[:-4] if u.endswith(".git") else u
            if u not in admitidas:
                err.append(f"{f}: URL de repositorio distinta de la configurada: {m.group(0)}")
        for m in URL_WEB.finditer(t):
            if not m.group(0).lower().startswith(web.rstrip("/")):
                err.append(f"{f}: URL de la web distinta de la configurada: {m.group(0)}")
    return err


def metadatos_al_dia() -> list[str]:
    return [f"{rel} desactualizado: ejecutar `make metadatos`" for rel, txt in metadatos.generar().items()
            if (RAIZ / rel).read_text(encoding="utf-8") != txt]


def cifras_sin_cambios() -> list[str]:
    base = pd.read_csv(RAIZ / "docs/v13/cifras_base_v12.csv", comment="#", dtype=str).set_index("id")["sha256"]
    ck = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv", dtype=str).fillna("").set_index("id")
    errata = (RAIZ / "ERRATA.md").read_text(encoding="utf-8")
    err = []
    for i, h in base.items():
        if i not in ck.index:
            if not C8._en_errata(errata, i, None):
                err.append(f"cifra desaparecida sin ERRATA: {i}")
            continue
        h2 = C8._huella(ck, i)
        if h2 != h and not C8._en_errata(errata, i, h2):
            err.append(f"cifra cambiada sin ERRATA: {i}")
    err += [f"cifra nueva en V13 (sin análisis nuevo): {i}" for i in ck.index if i not in base.index]
    return err


def main() -> int:
    total = 0
    for nombre, fn in (("versión vigente", version_unica), ("URL del repositorio", url_unica), ("metadatos", metadatos_al_dia),
                       ("cifras", cifras_sin_cambios)):
        e = fn()
        total += len(e)
        print(f"check_v13 · {nombre}: {len(e)} errores")
        for x in e[:20]:
            print("  -", x)
    print(f"check_v13: {total} errores")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
