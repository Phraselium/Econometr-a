"""K4d · Documentación y publicación: enlaces relativos de los .md, versión y marcas de referencias. Determinista, sin red.

Salida: output/v6_1/K4D/enlaces_rotos.csv, versiones.csv, referencias.csv y resumen.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "v6_1" / "K4D"
EXCL = ("data/", ".git/", "node_modules/", "output/v6_1/K4D/")
ENLACE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMG = re.compile(r"\!\[[^\]]*\]\(([^)\s]+)\)")


def mds() -> list[Path]:
    # v6.2: se excluyen las cachés no versionadas (.pytest_cache, .ruff_cache), para que el recuento no dependa del entorno
    fs = [p for p in ROOT.rglob("*.md") if not any(p.relative_to(ROOT).as_posix().startswith(e) for e in EXCL)
          and not any(part in (".pytest_cache", ".ruff_cache") for part in p.relative_to(ROOT).parts)]
    return sorted(fs)


def enlaces_rotos() -> pd.DataFrame:
    filas = []
    for f in mds():
        txt = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), f.read_text(encoding="utf-8", errors="replace"), flags=re.S)
        for n, ln in enumerate(txt.split("\n"), 1):
            ln = re.sub(r"`[^`]*`", " ", ln)
            for m in list(ENLACE.finditer(ln)) + list(IMG.finditer(ln)):
                d = m.group(1).split("#")[0]
                if not d or re.match(r"[a-z]+:", d):
                    continue
                base = f.parent
                rel = f.relative_to(ROOT).as_posix()
                if rel.startswith("docs/v5/plantillas/"):  # las plantillas se renderizan a output/v5/: allí se resuelven sus enlaces
                    base = ROOT / "output" / "v5" / f.parent.relative_to(ROOT / "docs" / "v5" / "plantillas")
                dest = (ROOT / d.lstrip("/")) if d.startswith("/") else (base / unquote(d))
                if not dest.exists():
                    filas.append({"fichero": f.relative_to(ROOT).as_posix(), "linea": n, "destino": d})
    return pd.DataFrame(filas, columns=["fichero", "linea", "destino"])


def versiones() -> pd.DataFrame:
    def g(p, pat):
        t = (ROOT / p).read_text(encoding="utf-8")
        m = re.search(pat, t, re.M)
        return m.group(1) if m else ""
    filas = [
        ("CITATION.cff", g("CITATION.cff", r'^version:\s*"?([\d.]+)')),
        (".zenodo.json", g(".zenodo.json", r'"version":\s*"([\d.]+)"')),
        ("README.md", g("README.md", r"Versi[óo]n:\*\*\s*v?([\d.]+)")),
        ("README_REPLICACION.md", g("README_REPLICACION.md", r"Versi[óo]n:\*\*\s*([\d.]+)")),
        ("CHANGELOG.md (primera sección)", g("CHANGELOG.md", r"^## v([\d.]+)")),
    ]
    return pd.DataFrame(filas, columns=["fichero", "version"])


def referencias() -> pd.DataFrame:
    """Referencias con DOI o en formato autor-año de docs/literatura.md, docs/v5/literatura_instrumentos.md y entregables."""
    fs = [ROOT / "docs" / "literatura.md", ROOT / "docs" / "v5" / "literatura_instrumentos.md"] + sorted((ROOT / "output" / "v5").glob("*.md"))
    filas = []
    for f in fs:
        if not f.exists():
            continue
        en_refs = f.name == "literatura_instrumentos.md" or f.name == "literatura.md"
        for n, ln in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            if ln.startswith("#"):
                en_refs = en_refs or bool(re.search(r"Referencias|referencias", ln))
            es_ref = bool(re.search(r"10\.\d{4,}/\S+", ln)) and (re.match(r"\s*(- |\|)", ln) is not None)
            if not es_ref:
                continue
            nover = bool(re.search(r"NO VERIFICADA|no verificad", ln, re.I))
            ver = bool(re.search(r"(?<!NO )VERIFICADA|DOI verificado", ln)) and not nover
            q = bool(re.search(r"\bQ[1-4]\b", ln))
            qnv = bool(re.search(r"cuartil no verificado|cuartil: no verificado|sin cuartil|\(libro\)", ln, re.I))
            if nover:
                est = "NO_VERIFICADA_MARCADA"
            elif ver and q:
                est = "VERIFICADA_COMPLETA"
            elif ver and qnv:
                est = "VERIFICADA_CUARTIL_NO_VERIFICADO"
            elif ver:
                est = "VERIFICADA_SIN_CUARTIL"
            else:
                est = "SIN_MARCA"
            filas.append({"fichero": f.relative_to(ROOT).as_posix(), "linea": n, "estado": est, "texto": re.sub(r"\s+", " ", ln)[:110]})
    return pd.DataFrame(filas, columns=["fichero", "linea", "estado", "texto"])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    e, v, r = enlaces_rotos(), versiones(), referencias()
    e.to_csv(OUT / "enlaces_rotos.csv", index=False)
    v.to_csv(OUT / "versiones.csv", index=False)
    r.to_csv(OUT / "referencias.csv", index=False)
    res = {"md_revisados": len(mds()), "enlaces_rotos": len(e), "versiones": dict(zip(v.fichero, v.version)),
           "referencias_por_estado": r.estado.value_counts().to_dict()}
    (OUT / "resumen.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
