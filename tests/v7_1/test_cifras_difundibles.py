"""V7.1-S3: ninguna cifra difundible fuera de cifras_clave ni de una versión superada.

1. Las plantillas de los entregables no tienen cifras fuera de marcadores {{id}} (check_v5) y todos los marcadores existen.
2. publicacion/cifras_clave.csv es la tabla única vigente (copia exacta) y no contiene filas de ejecuciones de prueba (_smoke).
3. Ningún fichero de publicacion/, metodologia/ o reproducir/ cita un valor superado (ERRATA), salvo en líneas marcadas como históricas.
4. Ningún entregable difundible presenta como vigente una versión superada.
"""
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v5"))
sys.path.insert(0, str(RAIZ / "tests"))
import check_v5  # noqa: E402
from test_l5_cifras import PERMITIDO, SUPERADOS  # noqa: E402

MARC = re.compile(r"\{\{([A-Za-z0-9_.\-]+)(?::[a-z_]+)?\}\}")


def test_plantillas_solo_marcadores():
    assert check_v5.plantillas() == []
    ids = set(pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").id)
    usados = {m for p in (RAIZ / "docs" / "v5" / "plantillas").rglob("*.md") for m in MARC.findall(p.read_text(encoding="utf-8"))}
    assert usados <= ids, sorted(usados - ids)[:10]


def test_tabla_unica_vigente():
    pub = RAIZ / "publicacion" / "cifras_clave.csv"
    assert pub.read_bytes() == (RAIZ / "output" / "v5" / "cifras_clave.csv").read_bytes()
    ck = pd.read_csv(pub)
    assert not ck.origen.astype(str).str.contains("_smoke").any()
    assert ck.id.is_unique


def test_sin_valores_superados():
    malas = []
    for c in ("publicacion", "metodologia", "reproducir"):
        for f in (RAIZ / c).rglob("*"):
            if f.suffix not in (".md", ".csv", ".json"):
                continue
            for n, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                for v in SUPERADOS:
                    if v in ln and not PERMITIDO.search(ln):
                        malas.append(f"{f.relative_to(RAIZ)}:{n}: {v}")
    assert not malas, malas[:10]


def test_version_vigente():
    vieja = re.compile(r"versi[óo]n de referencia (?:congelada )?\(?v?6|v6\.2 es la versi[óo]n de referencia", re.I)
    for f in ("una_pagina.md", "lo_que_sabemos.md", "policy_brief.md", "informe_tecnico.md", "working_paper.md", "que_cambio.md"):
        t = (RAIZ / "publicacion" / f).read_text(encoding="utf-8")
        assert "v7.1" in t or "`7.1`" in t, f
        assert not vieja.search(t), f
    for f in ("README.md", "LEEME_PRIMERO.md"):
        assert not vieja.search((RAIZ / f).read_text(encoding="utf-8")), f
