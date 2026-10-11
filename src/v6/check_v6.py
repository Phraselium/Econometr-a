"""Comprobaciones de puerta v6 (entran en `make check`). Sin red.

1. La validación v6 es nueva: no comparte provincias con la de v2 y solo los módulos M3/M4 llaman a evaluate_v6.
2. Ninguna afirmación causal a partir de SHAP, importancias, ALE o dependencias parciales (output/v6, plantillas).
3. Cada resultado de compra declara su medida de precio (campo «medida_precio» en output/v6/*/resultado.json).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

OUT = RAIZ / "output" / "v6"
CAUSAL = re.compile(r"\b(caus[aó]\w*|provoc\w*|efecto causal|impacto causal|se debe a|debido a|gracias a|hace que|explica[nr]? (la|el|que))\b", re.I)
INTERP = re.compile(r"\b(SHAP|importancia|ALE|dependencia parcial|partial dependence|feature importance)\b", re.I)
NEG = re.compile(r"\b(no|nunca|ni)\b[^.]{0,40}\b(causal|caus\w*)", re.I)


def validacion_nueva() -> list[str]:
    err = []
    comun = set(holdout.provincias_selladas_v6()) & set(holdout.provincias_selladas())
    if comun:
        err.append(f"v6 comparte provincias selladas con v2: {sorted(comun)}")
    for p in sorted((RAIZ / "src").rglob("*.py")):
        if p.name in ("holdout.py", "check_v6.py"):
            continue
        if "evaluate_v6(" in p.read_text() and not re.match(r"m[34]_", p.name):
            err.append(f"{p.relative_to(RAIZ)}: llama a evaluate_v6 fuera de M3/M4")
    return err


def sin_causalidad_ml() -> list[str]:
    err = []
    ficheros = list(OUT.rglob("*.md")) + list(OUT.rglob("*.json")) + list((RAIZ / "docs" / "v5" / "plantillas").rglob("*.md"))
    for p in ficheros:
        for i, l in enumerate(p.read_text(errors="ignore").splitlines(), 1):
            for frase in re.split(r"(?<=[.;])\s+", l):
                if INTERP.search(frase) and CAUSAL.search(frase) and not NEG.search(frase):
                    err.append(f"{p.relative_to(RAIZ)}:{i}: lenguaje causal junto a una interpretación de ML: «{frase.strip()[:90]}»")
    return err


def medida_precio() -> list[str]:
    err = []
    for p in sorted(OUT.glob("*/resultado.json")):
        try:
            r = json.loads(p.read_text())
        except ValueError:
            continue
        txt = json.dumps(r, ensure_ascii=False).lower()
        if re.search(r"compra|precio de (la )?vivienda|valor tasado", txt) and "medida_precio" not in r:
            err.append(f"{p.relative_to(RAIZ)}: resultado de compra sin «medida_precio»")
    return err


def sellado_integro() -> list[str]:
    """El sellado v6 regenerado (data/sealed/v6_*.csv) coincide con el sha256 versionado en output/v6/M0/sellado_info.json."""
    import hashlib
    info = OUT / "M0" / "sellado_info.json"
    if not info.exists():
        return []
    err = []
    for p in json.loads(info.read_text()):
        f = holdout.SEALED / f"v6_{p['panel']}.csv"
        if f.exists() and hashlib.sha256(f.read_bytes()).hexdigest() != p["sha256_sealed"]:
            err.append(f"sellado v6 {p['panel']}: sha256 distinto del versionado (el sellado cambió)")
    return err


def main() -> int:
    err = validacion_nueva() + sin_causalidad_ml() + medida_precio() + sellado_integro()
    for e in err:
        print(e)
    print(f"check_v6: {len(err)} errores")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
