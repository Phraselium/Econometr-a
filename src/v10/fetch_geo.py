"""V10-B1: geometrías de partida (solo descarga; se ejecuta con red, una vez). `make base` no usa la red.

- INE, seccionado censal 2025 (shapefile nacional; secciones con CUSEC, CUMUN, CPRO, CCA). >50 MB: no se versiona
  (.gitignore + data/CHECKSUMS.sha256); se reconstruye con este script.
- Ajuntament de València (CC BY 4.0, geoportal): barrios (capa 224), distritos (225) y secciones censales (210).
"""
from __future__ import annotations

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
    cache = Path("/tmp/claude-0/-home-user-Econometr-a/468da938-3e2d-5fba-ac52-e16a4175b9ac/scratchpad/iab/seccionado_2025.zip")
    if not destino.exists() and cache.exists():
        shutil.copy(cache, destino)
    descargar(INE, destino)
    for nombre, capa in CAPAS_VLC.items():
        descargar(VLC.format(capa=capa), DIR / nombre)
    for f in sorted(DIR.iterdir()):
        print(sha256(f), f.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
