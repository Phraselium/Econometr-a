"""V15 · Comprobaciones de `make check` (docs/v15/plan.md). Sin red; no escribe nada.

1. guardas: .claude/settings.json niega leer y escribir la muestra sellada y los comandos prohibidos, registra el hook
   PreToolUse de Bash, y el hook bloquea un caso de cada regla (autocomprobación rápida);
2. puerta: ningún resultado de estimación de V15 (output/v15/p*/resultado.json con `estimacion`) existe sin osf_prereg_v15;
3. cifras V15 (output/v15/cifras_v15.csv, si existe): id V15-*, capa válida, ficha no vacía y ningún id de la 1.0;
4. lenguaje causal: en output/v15/**/*.md ninguna línea con vocabulario causal sin etiqueta [C3] o [C3s];
5. literatura: cada ficha de docs/v15/literatura/*.md declara su estado (VERIFICADA, NO VERIFICADA o DISCREPANTE).
Que ninguna cifra de la 1.0 cambie de valor lo comprueba check_v13 (huellas de docs/v13/cifras_base_v12.csv).
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CAPAS = {"C1", "C2", "C3", "C3s", "C4"}
CAUSAL = re.compile(r"\b(causa(?:n|do|da)?|provoc\w*|efecto causal|debido a|gracias a|impulsad[oa]s? por|explica(?:n)? (?:la|el) subida)\b", re.I)
DENY_MINIMO = ("Read(data/sealed/**)", "Write(data/sealed/**)", "Edit(data/sealed/**)", "Bash(make clean:*)", "Bash(make all:*)",
               "Bash(make evaluate_v7:*)", "Bash(git push --force:*)", "Bash(git filter-repo:*)", "Bash(rm -rf data:*)", "Bash(rm -rf output:*)")


def guardas() -> list[str]:
    err = []
    s = json.loads((RAIZ / ".claude" / "settings.json").read_text(encoding="utf-8"))
    deny = set(s.get("permissions", {}).get("deny", []))
    err += [f"settings.json: falta en permissions.deny «{d}»" for d in DENY_MINIMO if d not in deny]
    hooks = json.dumps(s.get("hooks", {}).get("PreToolUse", []))
    if "guardas_bash.py" not in hooks:
        err.append("settings.json: falta el hook PreToolUse .claude/hooks/guardas_bash.py")
    ruta = RAIZ / ".claude" / "hooks" / "guardas_bash.py"
    if not ruta.exists():
        return err + ["falta .claude/hooks/guardas_bash.py"]
    spec = importlib.util.spec_from_file_location("guardas_bash", ruta)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    delim, sel = "E" + "OF", "data/" + "sealed"
    casos = {f"cat > x <<{delim}\nx\n{delim}": "(a)", f"ls {sel}": "(b)", "make clean": "(e)", "git push --force origin x": "(e)"}
    for cmd, regla in casos.items():
        m = g.evaluar(cmd, RAIZ)
        if not m or not m.startswith(regla):
            err.append(f"guarda {regla} no bloquea: {cmd!r}")
    if g.evaluar(f"cat > x <<'{delim}'\nx\n{delim}", RAIZ) or g.evaluar("python3 src/holdout.py estado", RAIZ):
        err.append("las guardas bloquean un comando permitido (heredoc entrecomillado o src/holdout.py)")
    return err


def puerta() -> list[str]:
    sys.path.insert(0, str(RAIZ / "src" / "v15"))
    import puerta as P
    ok, _ = P.abierta()
    if ok:
        return []
    err = []
    for r in sorted((RAIZ / "output" / "v15").glob("p*/resultado.json")):
        d = json.loads(r.read_text(encoding="utf-8"))
        if d.get("estimacion") not in (None, "", {}, []):
            err.append(f"{r.relative_to(RAIZ)}: estimación de V15 antes de la puerta (falta osf_prereg_v15)")
    return err


def cifras() -> list[str]:
    f = RAIZ / "output" / "v15" / "cifras_v15.csv"
    if not f.exists():
        return []
    ids_10 = {r["id"] for r in csv.DictReader((RAIZ / "output" / "v5" / "cifras_clave.csv").open(encoding="utf-8"))}
    err = []
    for r in csv.DictReader(f.open(encoding="utf-8")):
        if not r["id"].startswith("V15-"):
            err.append(f"cifras_v15: id sin prefijo V15-: {r['id']}")
        if r.get("capa") not in CAPAS:
            err.append(f"cifras_v15: capa no válida en {r['id']}: {r.get('capa')}")
        if not (r.get("ficha") or "").strip() or r.get("ficha") == "—":
            err.append(f"cifras_v15: {r['id']} sin ficha")
        if r["id"] in ids_10:
            err.append(f"cifras_v15: {r['id']} ya existe en la 1.0")
    return err


def causal() -> list[str]:
    err = []
    for p in sorted((RAIZ / "output" / "v15").rglob("*.md")):
        for n, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if CAUSAL.search(ln) and not re.search(r"\[C3s?\b|C3s?:|check:causal-permitido", ln):
                err.append(f"{p.relative_to(RAIZ)}:{n}: vocabulario causal fuera de C3/C3s: {CAUSAL.search(ln).group(0)!r}")
    return err


def literatura() -> list[str]:
    err = []
    for p in sorted((RAIZ / "docs" / "v15" / "literatura").glob("*.md")):
        t = p.read_text(encoding="utf-8")
        for bloque in re.split(r"\n(?=### )", t)[1:]:
            if not re.search(r"Estado:\s*(VERIFICADA|NO VERIFICADA|DISCREPANTE)", bloque):
                err.append(f"{p.relative_to(RAIZ)}: ficha sin estado de verificación: {bloque.splitlines()[0][:80]}")
    return err


def main() -> int:
    total = 0
    for nombre, f in (("guardas", guardas), ("puerta", puerta), ("cifras", cifras), ("lenguaje causal", causal), ("literatura", literatura)):
        e = f()
        print(f"check_v15 · {nombre}: {len(e)} errores")
        for x in e[:30]:
            print("  -", x)
        total += len(e)
    print(f"check_v15: {total} errores")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
