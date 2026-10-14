"""V10-B4/B5: la web se construye sin red, solo con datos redistribuibles, con capa, fuente y fecha visibles, texto
alternativo en las imágenes y sin datos posteriores al pre-registro en el panel ni en los mapas."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v10"))


@pytest.fixture(scope="module")
def sitio():
    if not (RAIZ / "data/base/publica/hechos.parquet").exists():
        pytest.skip("falta la capa pública de la base")
    import web
    web.construir()
    return web.SITE


def test_paginas_accesibles(sitio):
    paginas = list(sitio.rglob("*.html"))
    assert len(paginas) > 300
    for p in paginas:
        h = p.read_text(encoding="utf-8")
        assert re.search(r'<html lang="es"', h) and "<title>" in h and 'href="#contenido"' in h, p.name
        for img in re.findall(r"<img [^>]*>", h):
            assert re.search(r'alt="[^"]{10,}"', img), (p.name, img[:80])
    for nav in ("Inicio", "Inici", "Mapes", "Metodologia i dades"):
        assert nav in (sitio / "index.html").read_text(encoding="utf-8")
    assert 'lang="en"' in (sitio / "metodologia.html").read_text(encoding="utf-8")


def test_capa_fuente_fecha_en_datos(sitio):
    cat = json.loads((sitio / "datos/indicadores/catalogo.json").read_text(encoding="utf-8"))
    for m in cat:
        assert m["capa"] and m["fuente"] and m["fecha_dato"] < "2026-07-01", m["id"]
    mapas = json.loads((sitio / "datos/mapas/catalogo.json").read_text(encoding="utf-8"))
    for m in mapas.values():
        assert m["fuente"] and m["fecha"] and all(c["capa"] for c in m["cols"])


def test_sin_posteriores_en_panel(sitio):
    for f in (sitio / "datos/indicadores").glob("*__*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        for _, _, periodo, _ in d["filas"]:
            assert not re.match(r"^2026(T[34]|-0[7-9]|-1[0-2])", periodo) and not periodo.startswith("2027"), (f.name, periodo)


def test_solo_redistribuible(sitio):
    import pandas as pd
    h = pd.read_parquet(sitio / "descargas/hechos.parquet", columns=["variable", "redistribuible", "fuente"])
    assert h.redistribuible.all() and not h.fuente.str.contains("Registradores|Notariado|Incasòl|Jaroci", case=False).any()
    nombres = {p.name for p in (sitio / "descargas").iterdir()}
    assert not any(n.startswith(("incasol", "jk_", "notariado", "registr")) for n in nombres)


def test_sin_recursos_externos(sitio):
    for p in sitio.rglob("*.html"):
        h = p.read_text(encoding="utf-8")
        externos = [u for u in re.findall(r'(?:src|href)="(https?://[^"]+)"', h) if "github.com" not in u and "doi.org" not in u]
        scripts = [u for u in re.findall(r'<script src="([^"]+)"', h) if u.startswith("http")]
        assert not scripts, (p.name, scripts)
        assert all(not u.endswith((".js", ".css")) for u in externos), (p.name, externos)
