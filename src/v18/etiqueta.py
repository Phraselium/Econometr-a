"""V18 · Puerta del plan de replicación (plan V18, B1 y fase 3). Pre-registro interno, sin sello de tiempo externo.

La puerta está abierta si la etiqueta LOCAL plan-replicacion-v18 existe y su commit está en la rama remota de desarrollo
(referencia de seguimiento local `origin/claude/housing-price-spain-econometric-95dhj3`). Así funciona aunque el proxy no deje
subir la etiqueta: basta con que el commit etiquetado se haya subido con la rama (plan, fase 3).

Para tests, ECONOMETRA_ETIQUETA_V18 puede apuntar a un JSON {"commit": "<sha>" | null, "en_remoto": true|false}.
Uso: python3 src/v18/etiqueta.py  (código 0 si la puerta está abierta, 1 si no)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ETIQUETA = "plan-replicacion-v18"
RAMA_REMOTA = "origin/claude/housing-price-spain-econometric-95dhj3"


def _git(*args: str, raiz: Path = RAIZ) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=raiz, capture_output=True, text=True, timeout=30)


def commit_etiqueta(raiz: Path = RAIZ) -> str | None:
    f = os.environ.get("ECONOMETRA_ETIQUETA_V18")
    if f:
        return json.loads(Path(f).read_text(encoding="utf-8")).get("commit")
    r = _git("rev-parse", "--verify", "--quiet", f"refs/tags/{ETIQUETA}^{{commit}}", raiz=raiz)
    return r.stdout.strip() or None


def en_rama_remota(commit: str, raiz: Path = RAIZ) -> bool:
    f = os.environ.get("ECONOMETRA_ETIQUETA_V18")
    if f:
        return bool(json.loads(Path(f).read_text(encoding="utf-8")).get("en_remoto"))
    return _git("merge-base", "--is-ancestor", commit, RAMA_REMOTA, raiz=raiz).returncode == 0


def puerta(raiz: Path = RAIZ) -> tuple[bool, str]:
    c = commit_etiqueta(raiz)
    if not c:
        return False, f"no existe la etiqueta local {ETIQUETA}"
    if not en_rama_remota(c, raiz):
        return False, f"el commit de {ETIQUETA} ({c[:7]}) no está en {RAMA_REMOTA}"
    return True, f"{ETIQUETA} → {c[:7]}, en la rama remota"


def es_posterior(commit: str, raiz: Path = RAIZ) -> bool:
    """True si `commit` desciende del commit etiquetado (o es él)."""
    c = commit_etiqueta(raiz)
    return bool(c) and _git("merge-base", "--is-ancestor", c, commit, raiz=raiz).returncode == 0


if __name__ == "__main__":
    ok, motivo = puerta()
    print(f"puerta V18: {'abierta' if ok else 'cerrada'} ({motivo})")
    sys.exit(0 if ok else 1)
