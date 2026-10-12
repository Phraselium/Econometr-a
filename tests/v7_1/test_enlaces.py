"""V7.1-S5: ningún enlace relativo roto en las puertas de entrada del lector (LEEME_PRIMERO, README, MAPA, publicacion/,
metodologia/, reproducir/ e historico/INDICE.md)."""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENLACE = re.compile(r"\]\(([^)\s]+)\)")


def _ficheros():
    fs = [RAIZ / "LEEME_PRIMERO.md", RAIZ / "README.md", RAIZ / "docs" / "MAPA.md", RAIZ / "historico" / "INDICE.md"]
    for c in ("publicacion", "metodologia", "reproducir"):
        fs += sorted((RAIZ / c).rglob("*.md"))
    return fs


def test_sin_enlaces_rotos():
    rotos = []
    for f in _ficheros():
        txt = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        for m in ENLACE.finditer(txt):
            t = m.group(1)
            if re.match(r"^(?:[a-z]+:|#|mailto)", t):
                continue
            ruta = t.split("#", 1)[0]
            if ruta and not (f.parent / ruta).exists():
                rotos.append(f"{f.relative_to(RAIZ)} -> {t}")
    assert not rotos, f"{len(rotos)} enlaces rotos: {rotos[:15]}"
