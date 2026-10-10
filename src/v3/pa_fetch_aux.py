"""P-A: descarga (con red) de las tablas del INE que se guardan en data/raw/v3/pa_aux/.

NO forma parte de `pa_run.py` (que no usa red). Tablas JAXI del INE (API wstempus, DATOS_TABLA):
  59531  Censo 2021: viviendas vacías y de uso esporádico (consumo eléctrico), por municipio
  59533  Censo 2021: hogares
  3456   Censo 2011: viviendas por tipo, municipios de más de 2.000 habitantes (solo nombre)
  3457   Censo 2011: viviendas por tipo, provincias
  65944  EPA: población por relación de parentesco con la persona de referencia, sexo y edad
Uso: python3 src/v3/pa_fetch_aux.py   (sobrescribe la caché)
"""
from __future__ import annotations

from pathlib import Path

import requests

AUX = Path(__file__).resolve().parents[2] / "data" / "raw" / "v3" / "pa_aux"
TABLAS = {59531: "?nult=1", 59533: "?nult=1", 3456: "?nult=1", 3457: "?nult=1", 65944: "?nult=200"}


def main() -> None:
    AUX.mkdir(parents=True, exist_ok=True)
    for t, q in TABLAS.items():
        r = requests.get(f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{t}{q}", timeout=600)
        r.raise_for_status()
        (AUX / f"ine_t{t}.json").write_bytes(r.content)
        print(t, len(r.content))


if __name__ == "__main__":
    main()
