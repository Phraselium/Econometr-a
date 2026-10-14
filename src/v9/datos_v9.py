"""V9-DATOS · `make datos_v9`: descarga o verifica todas las fuentes de data/raw/v9 y consolida el manifiesto global.

Para cada src/v9/fetch_<fuente>.py:
  1. main(verificar=True): sin red, comprueba que los ficheros de data/raw/v9/<fuente>/_manifest.csv existen y que su
     sha256 coincide;
  2. si falla y hay red (y no se pasa --solo-verificar), main(verificar=False) descarga lo que falta y vuelve a registrar.
Después escribe data/raw/v9/_manifest.csv con todas las filas. Código de salida 1 si alguna fuente queda sin verificar.
Uso: python3 src/v9/datos_v9.py [--solo-verificar]
"""
from __future__ import annotations

import csv
import importlib
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v9"))
import comun  # noqa: E402

RAW9 = comun.RAW9


def hay_red() -> bool:
    try:
        urllib.request.urlopen("https://servicios.ine.es/", timeout=6)
        return True
    except Exception:  # noqa: BLE001
        return False


def consolidar() -> int:
    filas = []
    for m in sorted(RAW9.glob("*/_manifest.csv")):
        with open(m, encoding="utf-8") as f:
            filas += list(csv.DictReader(f))
    with open(RAW9 / "_manifest.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=comun.COLS_MANIFIESTO, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(filas, key=lambda r: (r["fuente"], r["fichero"])))
    return len(filas)


def main(solo_verificar: bool = False) -> int:
    red = None
    malos = []
    for s in sorted((RAIZ / "src" / "v9").glob("fetch_*.py")):
        mod = importlib.import_module(s.stem)
        ok = mod.main(verificar=True) == 0
        if not ok and not solo_verificar:
            red = hay_red() if red is None else red
            if red:
                print(f"[datos_v9] {s.stem}: descargando")
                ok = mod.main(verificar=False) == 0 and mod.main(verificar=True) == 0
        print(f"[datos_v9] {s.stem}: {'OK' if ok else 'SIN VERIFICAR'}")
        if not ok:
            malos.append(s.stem)
    n = consolidar()
    print(f"[datos_v9] manifiesto global: {n} ficheros; sin verificar: {malos or 'ninguno'}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main("--solo-verificar" in sys.argv))
