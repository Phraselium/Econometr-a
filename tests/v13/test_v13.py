"""V13: versión y URL únicas (check_v13), metadatos generados, datos_terceros sin cambios en ficheros versionados y paquete
del depósito sin datos no redistribuibles ni muestra sellada."""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src" / "v8_1"))
import datos_terceros as DT  # noqa: E402

from src.v13 import check_v13 as C  # noqa: E402
from src.v13 import metadatos as M  # noqa: E402
from src.v13 import paquete_zenodo as PZ  # noqa: E402


def test_version_y_url_unicas():
    assert C.version_unica() == []
    assert C.url_unica() == []


def test_check_detecta_discrepancias(tmp_path, monkeypatch):
    f = tmp_path / "README.md"
    antigua = "https://github.com/" + "Phraselium/Econometr-a"   # concatenada: el propio check_v13 rechaza la URL literal
    f.write_text(f"Versión pública: **0.9**. Repositorio: {antigua}\n", encoding="utf-8")
    assert [m.group(1) for m in C.DECL.finditer(f.read_text(encoding="utf-8"))] == ["0.9"]
    assert C.URL_REPO.search(f.read_text(encoding="utf-8")).group(0).lower() != C.P["repositorio"].lower()


def test_metadatos_generados_y_coherentes():
    assert C.metadatos_al_dia() == []
    p = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))
    z = json.loads(M.zenodo())
    assert z["version"] == p["version_publica"] and p["repositorio"] in M.citation()


def test_cifras_sin_cambios():
    assert C.cifras_sin_cambios() == []


def test_datos_terceros_no_reescribe_versionados(tmp_path):
    man = tmp_path / "data" / "raw" / "v9" / "x" / "_manifest.csv"
    inv = tmp_path / "docs" / "v5" / "programas" / "inventario.csv"
    for p in (man, inv):
        p.parent.mkdir(parents=True)
        p.write_text("original\n", encoding="utf-8")

    def fetch():
        man.write_text("fecha de descarga nueva\n", encoding="utf-8")
        inv.write_text("filas nuevas\n", encoding="utf-8")

    cambiados = DT.proteger_versionados(tmp_path, fetch)
    assert sorted(cambiados) == ["data/raw/v9/x/_manifest.csv", "docs/v5/programas/inventario.csv"]
    assert man.read_text(encoding="utf-8") == "original\n" and inv.read_text(encoding="utf-8") == "original\n"
    assert (tmp_path / DT.REGISTRO / "data/raw/v9/x/_manifest.csv").read_text(encoding="utf-8") == "fecha de descarga nueva\n"


def test_paquete_sin_no_redistribuibles():
    inc, exc = PZ.seleccionar()
    assert not any(f.startswith("data/sealed") for f in inc)
    excluidos = {f for f, _ in exc}
    for f in ("data/cache/v12/od_seleccion.csv.gz", "data/raw/v11/aeat_irpf_municipios/irpf_municipios_cv.csv.gz",
              "data/processed/nacional_q.csv", "data/base/variables.parquet"):
        assert f in excluidos and f not in inc, f
    assert "data/base/publica/hechos.parquet" in inc and "src/v13/check_v13.py" in inc and not any(f.startswith(".claude/") for f in inc)
    assert PZ.EXCLUIR_PUBLICA.match("aeat_irpf_renta_bruta_media")


def test_inventario_solo_versionados_y_clasificado():
    import pandas as pd
    d = pd.read_csv(RAIZ / "docs" / "v13" / "datos_inventario.csv")
    assert d.versionado.all() and set(d.clase) <= {"a", "b", "c"}
    assert not d.fichero.str.startswith("data/sealed").any()
