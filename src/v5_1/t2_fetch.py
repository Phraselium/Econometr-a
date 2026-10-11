"""T2 fetch (con red; fuera de make). Descarga a data/raw/v5_1/ tablas INE: 6154 (viviendas transmitidas por titulo)."""
import json
import urllib.request
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parents[2] / "data" / "raw" / "v5_1"
OUT.mkdir(parents=True, exist_ok=True)
for tabla, nult in ((6154, 12),):
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{tabla}?nult={nult}"
    d = json.load(urllib.request.urlopen(url, timeout=90))
    filas = [(tabla, x["Nombre"], z["Anyo"], z["FK_Periodo"], z["Valor"], url) for x in d for z in x["Data"]]
    pd.DataFrame(filas, columns=["tabla", "nombre", "anyo", "periodo", "valor", "url"]).to_csv(
        OUT / f"ine_t2_t{tabla}.csv", index=False)
    print(tabla, len(filas))
