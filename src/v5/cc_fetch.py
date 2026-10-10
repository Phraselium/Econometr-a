"""CC · Descargas (con red, fuera de make) a data/raw/v5/cc_*.

Eurostat: ilc_lvho07b (sobrecarga por quintil), ilc_lvho07c (por tenencia), ilc_lvho28, ilc_lvho02 ya en CA.
INE ECV: tabla 59953 (personas por decil y tenencia).
BOE: texto de los RD de los planes estatales de vivienda (régimen de protección).
"""
from __future__ import annotations

import itertools
import json
import subprocess
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DEST = RAIZ / "data" / "raw" / "v5"
ES = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
BOE = {
    "1992": ("BOE-A-1992-604", "RD 1932/1991"), "1996": ("BOE-A-1995-27970", "RD 2190/1995"),
    "1998": ("BOE-A-1998-15136", "RD 1186/1998"), "2002": ("BOE-A-2002-689", "RD 1/2002"),
    "2005": ("BOE-A-2005-12049", "RD 801/2005"), "2009": ("BOE-A-2008-20751", "RD 2066/2008"),
    "2013": ("BOE-A-2013-3780", "RD 233/2013"), "2018": ("BOE-A-2018-3358", "RD 106/2018"),
    "2022": ("BOE-A-2022-802", "RD 42/2022"), "2026": ("BOE-A-2026-8872", "RD 326/2026"),
}


def curl(url: str) -> bytes:
    return subprocess.run(["curl", "-sSL", "-m", "120", url], capture_output=True).stdout


def jsonstat(url: str) -> pd.DataFrame:
    j = json.loads(curl(url))
    ids, size = j["id"], j["size"]
    idx = {d: list(j["dimension"][d]["category"]["index"].keys()) for d in ids}
    rows = []
    for k, combo in enumerate(itertools.product(*[range(s) for s in size])):
        v = j["value"].get(str(k)) if isinstance(j["value"], dict) else j["value"][k]
        if v is not None:
            rows.append({**{d: idx[d][i] for d, i in zip(ids, combo)}, "valor": v})
    df = pd.DataFrame(rows)
    df["actualizado"] = j.get("updated")
    return df


def main() -> None:
    for ds in ("ilc_lvho07b", "ilc_lvho07c", "ilc_lvho28"):
        df = jsonstat(f"{ES}/{ds}?format=JSON&lang=EN&geo=ES&geo=EU27_2020&unit=PC")
        df.to_csv(DEST / f"cc_eurostat_{ds}.csv", index=False)
        print(ds, len(df))
    (DEST / "cc_ine_t59953.json").write_bytes(curl("https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/59953?nult=12"))
    for plan, (bid, _) in BOE.items():
        (DEST / f"cc_boe_{plan}.html").write_bytes(curl(f"https://www.boe.es/buscar/doc.php?id={bid}"))


if __name__ == "__main__":
    main()
