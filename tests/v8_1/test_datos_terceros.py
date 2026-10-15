"""V8.1 C: los ficheros de terceros retirados del índice no rompen check_v5 y se verifican por checksum."""
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "v5"))
sys.path.insert(0, str(ROOT / "src" / "v8_1"))

import check_v5  # noqa: E402
import datos_terceros  # noqa: E402


def _retirados():
    with (ROOT / "docs/v8_1/inventario_licencias.csv").open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["estado"].startswith("no claramente")]


def test_retirados_no_versionados_y_ignorados():
    tracked = set(subprocess.run(["git", "ls-files", "data/raw"], cwd=ROOT, capture_output=True, text=True).stdout.split())
    for r in _retirados():
        assert r["fichero"] not in tracked, r["fichero"]
        ign = subprocess.run(["git", "check-ignore", "-q", r["fichero"]], cwd=ROOT).returncode
        assert ign == 0, f"{r['fichero']} no está en .gitignore"


def test_retirados_con_checksum():
    ck = {l.split("  ", 1)[1].strip(): l.split("  ", 1)[0] for l in
          (ROOT / "data/CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines() if "  " in l}
    for r in _retirados():
        assert ck.get(r["fichero"]) == r["sha256"], r["fichero"]


def test_regla_lecturas_acepta_retirados_con_script():
    nombres = check_v5.retirados_con_descarga()
    assert "registradores_opendata_anual.csv" in nombres and "jk_shocks_ecb_mensual.csv" in nombres
    # un renders manual (sin script) no se acepta como lectura
    assert not any(n.endswith("_zoomA.png") for n in nombres)
    assert check_v5.lecturas_no_versionadas() == []


def test_regla_sigue_detectando_ficheros_no_listados(tmp_path, monkeypatch):
    # un fichero retirado SIN script de descarga no queda exento: se simula quitando el script del inventario
    fake = tmp_path / "inv.csv"
    fake.write_text("fichero,organismo,estado,motivo,script_descarga,sha256\n"
                    "data/raw/pdf/registradores_opendata_anual.csv,x,no claramente permitida / no consta,m,,h\n", encoding="utf-8")
    ck = tmp_path / "ck"
    ck.write_text("h  data/raw/pdf/registradores_opendata_anual.csv\n", encoding="utf-8")
    (tmp_path / "docs/v8_1").mkdir(parents=True)
    (tmp_path / "data").mkdir()
    (tmp_path / "docs/v8_1/inventario_licencias.csv").write_text(fake.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "data/CHECKSUMS.sha256").write_text(ck.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(check_v5, "RAIZ", tmp_path)
    assert check_v5.retirados_con_descarga() == set()


def test_datos_terceros_verifica_sin_red():
    items = datos_terceros.cargar(ROOT)
    assert len(items) == len(_retirados())
    for f, h, _ in items:
        assert h, f
        p = ROOT / f
        if p.exists():
            # V9: un .gz regenerado con otra cabecera y el mismo contenido es «OK (contenido; cabecera gzip distinta)»
            assert datos_terceros.estado(ROOT, f, h).startswith("OK") or datos_terceros.estado(ROOT, f, h) == "DISTINTO"
