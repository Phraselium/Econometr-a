"""V16 · Registro de pre-registros (src/v16/preregistros.py): hashes iguales a git, fechas de git y pre-registros vigentes intactos."""
import csv
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def _m():
    spec = importlib.util.spec_from_file_location("v16_preregistros", RAIZ / "src" / "v16" / "preregistros.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_registro_actual_sin_errores():
    assert _m().check() == []


def test_hash_alterado_falla(tmp_path, monkeypatch):
    m = _m()
    filas = list(csv.DictReader(m.CSV.open(encoding="utf-8")))
    filas[0]["sha256_en_commit"] = "0" * 64
    f = tmp_path / "f.csv"
    with f.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=m.COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    monkeypatch.setattr(m, "CSV", f)
    assert any("sha256 registrado distinto" in e for e in m.check())


def test_preregistro_vigente_cambiado_falla(monkeypatch):
    m = _m()
    reales = m.filas()
    monkeypatch.setattr(m, "filas", lambda: [dict(r, igual_hoy="no") if r["etiqueta"] == "prereg-v16" else r for r in reales])
    assert any("prereg-v16" in e and "ha cambiado" in e for e in m.check())


def test_fecha_distinta_de_git_falla(tmp_path, monkeypatch):
    m = _m()
    filas = list(csv.DictReader(m.ETIQUETAS.open(encoding="utf-8")))
    filas[0]["fecha_commit_utc"] = "2000-01-01T00:00:00Z"
    f = tmp_path / "e.csv"
    with f.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    monkeypatch.setattr(m, "ETIQUETAS", f)
    assert any("distinta de git" in e for e in m.check())
