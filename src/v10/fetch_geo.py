"""V10-B1: geometrías de partida (solo descarga; se ejecuta con red, una vez). `make base` no usa la red.

- INE, seccionado censal 2025 (shapefile nacional; secciones con CUSEC, CUMUN, CPRO, CCA). >50 MB: no se versiona
  (.gitignore + data/CHECKSUMS.sha256); se reconstruye con este script.
- Ajuntament de València (CC BY 4.0, geoportal): barrios (capa 224), distritos (225) y secciones censales (210).
"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import descargar, sha256  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
DIR = RAIZ / "data" / "raw" / "v10" / "geo"
INE = "https://www.ine.es/prodyser/cartografia/seccionado_2025.zip"
VLC = "https://geoportal.valencia.es/server/rest/services/OPENDATA/UrbanismoEInfraestructuras/MapServer/{capa}/query?where=1=1&outFields=*&f=geojson"
CAPAS_VLC = {"vlc_barrios.geojson": 224, "vlc_distritos.geojson": 225, "vlc_secciones.geojson": 210}


def main() -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    destino = DIR / "seccionado_2025.zip"
    # V14: copia local opcional del zip del INE (variable de entorno), en lugar de una ruta fija de la sesión de trabajo
    cache = Path(os.environ["SECCIONADO_2025_ZIP"]) if os.environ.get("SECCIONADO_2025_ZIP") else None
    if not destino.exists() and cache is not None and cache.exists():
        shutil.copy(cache, destino)
    descargar(INE, destino)
    for nombre, capa in CAPAS_VLC.items():
        descargar(VLC.format(capa=capa), DIR / nombre)
    for f in sorted(DIR.iterdir()):
        print(sha256(f), f.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
