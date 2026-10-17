"""V16 · Controles de `make check` (docs/v16/plan.md). Sin red; no escribe nada en el repositorio.

1. guardas: las guardas (d) y (f) del hook bloquean sin la etiqueta en el remoto y no bloquean con ella (se simula el remoto
   con ECONOMETRA_ETIQUETAS_REMOTAS); el hook sigue registrado.
2. preregistro: proyecto.json declara preregistro_tipo = «interno, sin sello externo» y no conserva campos de OSF.
3. estimaciones posteriores a su etiqueta: todo commit que toque estimaciones de V15 (src/v15/pN*.py, output/v15/pN*/) o de
   V16 (src/v16/qN*.py, output/v16/qN*/) desciende de la etiqueta local prereg-v15 o prereg-v16. Sin la etiqueta, no
   puede haber ningún commit de estimación.
4. cifras V16: toda cifra V16-* de output/v5/cifras_clave.csv tiene capa y ficha (cuando existan).
5. lenguaje causal en output/v16/**/*.md fuera de C3/C3s (mismo criterio que check_v15).
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
TIPO = "interno, sin sello externo"
ESTIMACION = {"prereg-v15": re.compile(r"^(src/v15/p\d[^/]*\.py|output/v15/p\d[^/]*/)"),
              "prereg-v16": re.compile(r"^(src/v16/q\d[^/]*\.py|output/v16/q\d[^/]*/)")}


def _hook():
    spec = importlib.util.spec_from_file_location("guardas_bash", RAIZ / ".claude" / "hooks" / "guardas_bash.py")
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    return g


def guardas() -> list[str]:
    err = []
    s = json.loads((RAIZ / ".claude" / "settings.json").read_text(encoding="utf-8"))
    if "guardas_bash.py" not in json.dumps(s.get("hooks", {}).get("PreToolUse", [])):
        err.append("settings.json: falta el hook PreToolUse .claude/hooks/guardas_bash.py")
    g = _hook()
    v15, v16 = "make " + "v15_f4", "make " + "v16_f5"
    antes = os.environ.get("ECONOMETRA_ETIQUETAS_REMOTAS")
    with tempfile.TemporaryDirectory() as d:
        vacio, lleno = Path(d) / "vacio.json", Path(d) / "lleno.json"
        vacio.write_text("{}", encoding="utf-8")
        lleno.write_text(json.dumps({"prereg-v15": "542b4fdf398970c817af7abfcd20c92dda299c69", "prereg-v16": "abc1234"}), encoding="utf-8")
        try:
            os.environ["ECONOMETRA_ETIQUETAS_REMOTAS"] = str(vacio)
            if not (g.evaluar(v15, RAIZ) or "").startswith("(d)"):
                err.append("guarda (d) no bloquea sin prereg-v15 en el remoto")
            if not (g.evaluar(v16, RAIZ) or "").startswith("(f)"):
                err.append("guarda (f) no bloquea sin prereg-v16 en el remoto")
            os.environ["ECONOMETRA_ETIQUETAS_REMOTAS"] = str(lleno)
            if g.evaluar(v15, RAIZ) or g.evaluar(v16, RAIZ):
                err.append("las guardas (d) o (f) bloquean con las etiquetas publicadas")
        finally:
            if antes is None:
                os.environ.pop("ECONOMETRA_ETIQUETAS_REMOTAS", None)
            else:
                os.environ["ECONOMETRA_ETIQUETAS_REMOTAS"] = antes
    return err


def preregistro() -> list[str]:
    p = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
    err = []
    if p.get("preregistro_tipo") != TIPO:
        err.append(f"proyecto.json: preregistro_tipo debe ser «{TIPO}»")
    err += [f"proyecto.json: campo de OSF que ya no se usa: {k}" for k in p if k.startswith("osf_prereg")]
    return err


def _git(*a: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *a], cwd=RAIZ, capture_output=True, text=True)


def estimaciones_tras_etiqueta() -> list[str]:
    err = []
    for etiqueta, patron in ESTIMACION.items():
        commits = []
        for linea in _git("log", "--format=@%H", "--name-only", "--", "src/v15", "output/v15", "src/v16", "output/v16").stdout.splitlines():
            if linea.startswith("@"):
                actual = linea[1:]
            elif linea and patron.match(linea) and (not commits or commits[-1] != actual):
                commits.append(actual)
        if not commits:
            continue
        t = _git("rev-parse", "-q", "--verify", f"{etiqueta}^{{commit}}")
        if t.returncode != 0:
            err.append(f"{len(commits)} commits con estimaciones sin la etiqueta {etiqueta}")
            continue
        for c in commits:
            if _git("merge-base", "--is-ancestor", t.stdout.strip(), c).returncode != 0:
                err.append(f"commit {c[:7]} con estimaciones anterior a {etiqueta}")
    return err


def cifras_v16() -> list[str]:
    import pandas as pd
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv", dtype=str).fillna("")
    v = ck[ck.id.str.startswith("V16-")]
    err = [f"{r.id}: sin capa" for r in v.itertuples() if r.capa not in ("C1", "C2", "C3", "C3s", "C4")]
    err += [f"{r.id}: sin ficha" for r in v.itertuples() if r.ficha in ("", "—")]
    return err


def causal() -> list[str]:
    sys.path.insert(0, str(RAIZ / "src" / "v15"))
    import check_v15 as C15
    err = []
    for p in sorted((RAIZ / "output" / "v16").rglob("*.md")):
        for n, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if C15.CAUSAL.search(ln) and not re.search(r"\[C3s?\b|C3s?:|check:causal-permitido", ln):
                err.append(f"{p.relative_to(RAIZ)}:{n}: vocabulario causal fuera de C3/C3s: {C15.CAUSAL.search(ln).group(0)!r}")
    return err


def main() -> int:
    total = 0
    for nombre, f in (("guardas", guardas), ("pre-registro interno", preregistro),
                      ("estimaciones posteriores a su etiqueta", estimaciones_tras_etiqueta), ("cifras V16", cifras_v16),
                      ("lenguaje causal", causal)):
        e = f()
        print(f"check_v16 · {nombre}: {len(e)} errores")
        for x in e[:30]:
            print("  -", x)
        total += len(e)
    print(f"check_v16: {total} errores")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
