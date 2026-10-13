"""V7.1-S5: publicacion/, metodologia/ y reproducir/ son exactamente lo que genera `make publicacion` (nunca se editan a mano)."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v7_1"))
import publicacion as P  # noqa: E402


def _ficheros(base: Path) -> dict[str, bytes]:
    return {p.relative_to(base).as_posix(): p.read_bytes() for c in P.CARPETAS for p in (base / c).rglob("*") if p.is_file()}


def test_regeneracion_identica(tmp_path):
    P.construir(tmp_path)
    esperado, actual = _ficheros(tmp_path), _ficheros(RAIZ)
    sobran = sorted(set(actual) - set(esperado))
    faltan = sorted(set(esperado) - set(actual))
    distintos = sorted(k for k in set(esperado) & set(actual) if esperado[k] != actual[k])
    assert not (sobran or faltan or distintos), f"ejecutar `make publicacion`; sobran {sobran[:5]}, faltan {faltan[:5]}, distintos {distintos[:5]}"


def test_contenido_minimo():
    pub = RAIZ / "publicacion"
    for f in ("una_pagina.md", "lo_que_sabemos.md", "policy_brief.md", "informe_tecnico.md", "working_paper.md", "nota_metodologica.md",
              "articulo_colegio.md", "cifras_clave.csv", "ponencia/diapositivas.md", "atlas_regional/atlas_resumen.md",
              "atlas_regional/tablas_regionales.xlsx", "verificador/verificador.md"):
        assert (pub / f).exists(), f
    assert len(list((pub / "atlas_regional").glob("[0-9][0-9]_*.md"))) == 17


def test_contenido_v8():
    """V8 (F6): verificador y metodología de V8 publicados; los entregables pendientes del orquestador están comentados en FUENTES."""
    for d in ("publicacion/verificador/verificador_v8.md", "publicacion/verificador/fichas_v8.json", "metodologia/preregistro_v8.md",
              "metodologia/desviaciones_v8.md", "metodologia/revision_v8_F4.md"):
        assert d in P.FUENTES and (RAIZ / d).exists(), d
    for d, src in P.FUENTES.items():
        assert (RAIZ / src).exists(), f"{d}: falta la fuente {src}"
