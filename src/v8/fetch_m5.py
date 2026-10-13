#!/usr/bin/env python3
"""V8-F4 M5: descarga UNICA de datos de Eurostat para IV2 (flujos por ciudadania a la UE) e IV3 (empleo sectorial NUTS2).

Red solo aqui (el script de modelo m5_lpiv.py NO usa red). Con cache: si el JSON ya existe en data/raw/v8/eurostat_migr/_cache/ no se vuelve a pedir.
Salidas (data/raw/v8/eurostat_migr/):
  migr_imm1ctz_ue.csv      geo (destino), citizen (origen), anio, valor   [Eurostat migr_imm1ctz, agedef=REACH, age=TOTAL, sex=T, unit=NR]
  lfst_r_lfe2en2_sector.csv geo (NUTS2 y ES), nace_r2, anio, valor (miles) [Eurostat lfst_r_lfe2en2, sex=T, age=Y15-64, unit=THS_PER]
  _manifest.csv            url, fecha_descarga, n, estado, sha256
Uso: python3 src/v8/fetch_m5.py
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DEST = RAIZ / "data" / "raw" / "v8" / "eurostat_migr"
CACHE = DEST / "_cache"
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
UE27 = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
        "PL", "PT", "RO", "SK", "SI", "SE", "ES"]
NUTS2 = ["ES11", "ES12", "ES13", "ES21", "ES22", "ES23", "ES24", "ES30", "ES41", "ES42", "ES43", "ES51", "ES52", "ES53", "ES61",
         "ES62", "ES63", "ES64", "ES70", "ES"]


def _pide(url: str, nombre: str) -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{nombre}.json"
    if f.exists():
        return json.loads(f.read_text())
    for intento in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                txt = r.read().decode("utf-8")
            f.write_text(txt)
            return json.loads(txt)
        except Exception:
            time.sleep(3 * (intento + 1))
    raise RuntimeError(f"fallo la descarga: {url}")


def _jsonstat_a_df(d: dict) -> pd.DataFrame:
    ids, size = d["id"], d["size"]
    dims = {k: list(d["dimension"][k]["category"]["index"]) for k in ids}
    import itertools
    idx = list(itertools.product(*[range(s) for s in size]))
    vals = d["value"]
    rows = []
    for pos, ix in enumerate(idx):
        v = vals.get(str(pos)) if isinstance(vals, dict) else vals[pos]
        if v is None:
            continue
        rows.append({k: dims[k][i] for k, i in zip(ids, ix)} | {"valor": float(v)})
    return pd.DataFrame(rows)


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    man = []
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # --- migr_imm1ctz: una peticion por pais de destino
    partes = []
    for g in UE27:
        url = f"{BASE}/migr_imm1ctz?geo={g}&sex=T&age=TOTAL&agedef=REACH&unit=NR&sinceTimePeriod=2002&lang=EN"
        df = _jsonstat_a_df(_pide(url, f"migr_imm1ctz_{g}"))
        df = df.rename(columns={"time": "anio"})[["geo", "citizen", "anio", "valor"]]
        partes.append(df)
        man.append({"dataset": "migr_imm1ctz", "geo": g, "url": url, "fecha_descarga": ahora, "n": len(df),
                    "estado": "ok" if len(df) else "vacio"})
    a = pd.concat(partes, ignore_index=True)
    a["anio"] = a["anio"].astype(int)
    a.to_csv(DEST / "migr_imm1ctz_ue.csv", index=False)
    # --- lfst_r_lfe2en2 con todos los sectores
    geos = "&".join(f"geo={g}" for g in NUTS2)
    url = f"{BASE}/lfst_r_lfe2en2?{geos}&sex=T&age=Y15-64&unit=THS_PER&sinceTimePeriod=2008&lang=EN"
    b = _jsonstat_a_df(_pide(url, "lfst_r_lfe2en2_sector")).rename(columns={"time": "anio"})[["geo", "nace_r2", "anio", "valor"]]
    b["anio"] = b["anio"].astype(int)
    b.to_csv(DEST / "lfst_r_lfe2en2_sector.csv", index=False)
    man.append({"dataset": "lfst_r_lfe2en2", "geo": "NUTS2+ES", "url": url, "fecha_descarga": ahora, "n": len(b),
                "estado": "ok" if len(b) else "vacio"})
    m = pd.DataFrame(man)
    m["sha256"] = ""
    for k, f in (("migr_imm1ctz", "migr_imm1ctz_ue.csv"), ("lfst_r_lfe2en2", "lfst_r_lfe2en2_sector.csv")):
        m.loc[m.dataset == k, "sha256"] = hashlib.sha256((DEST / f).read_bytes()).hexdigest()
    m.to_csv(DEST / "_manifest.csv", index=False)
    print(m.groupby("dataset").n.sum())


if __name__ == "__main__":
    main()
