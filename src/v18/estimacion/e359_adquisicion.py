"""V18 · fase 4 · adquisición de las fuentes `posterior_prereg` de E3, E5 y E9 (descarga única, después de la etiqueta plan-replicacion-v18).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Único módulo de E3/E5/E9 que usa red; las estimaciones (e3_inmigracion.py,
e5_oferta.py, e9_no_residentes.py) leen solo los ficheros locales. Se descarga, se normaliza y se audita la calidad; no se cruza con ningún
resultado. Salidas en data/raw/v18/eurostat_e359/ y data/raw/v18/_manifest_e359.csv (fuente, url, fecha, sha256, licencia).

Fuentes (Eurostat, API de difusión 1.0, reutilización con cita; datos originales del INE):
- cens_01rsctz: Censo de 2001, población por sexo, nacionalidad y NUTS 3 (cuotas de asentamiento de E3; INE no deja consultar su Censo de 2001:
  docs/v6/fuentes_fallidas.md).
- nama_10r_3empers: empleo por NUTS 3 y rama A*10 (cuotas sectoriales de 2001 del Bartik de E5 y control de construcción de E3). Sustituye a la
  afiliación provincial por CNAE de 2001, que no está publicada (docs/v18/desviaciones.md, D-E359-2).
- demo_r_pjangrp3 (2014-2025) y demo_r_pjanaggr3 (desde 1990): población a 1 de enero por NUTS 3 y edad (población de 15 a 64 años, ponderación de 1998/2000
  y placebo de 65 o más).
Uso: python3 src/v18/estimacion/e359_adquisicion.py   (SEED sin efecto: no hay aleatoriedad).
"""
from __future__ import annotations

import gzip
import hashlib
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd

ALCANCE_TERRITORIAL = "sin lectura de datos"     # solo descarga y escribe ficheros nuevos; no lee datos del proyecto
RAIZ = Path(__file__).resolve().parents[3]
DEST = RAIZ / "data" / "raw" / "v18" / "eurostat_e359"
MANIFIESTO = RAIZ / "data" / "raw" / "v18" / "_manifest_e359.csv"
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
SEMILLA = 20261010


def pedir(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))


def jsonstat_a_df(js: dict) -> pd.DataFrame:
    ids, size = js["id"], js["size"]
    cats = []
    for d in ids:
        idx = js["dimension"][d]["category"]["index"]
        orden = sorted(idx.items(), key=lambda kv: kv[1])
        cats.append([k for k, _ in orden])
    filas = []
    val = js["value"]
    status = js.get("status", {})
    import itertools
    prod = itertools.product(*[range(n) for n in size])
    for flat, ix in enumerate(prod):
        v = val.get(str(flat))
        if v is None:
            continue
        filas.append([cats[j][i] for j, i in enumerate(ix)] + [v, status.get(str(flat), "")])
    return pd.DataFrame(filas, columns=list(ids) + ["valor", "estado"])


def guardar(df: pd.DataFrame, nombre: str, url: str, edicion: str, notas: str) -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    f = DEST / nombre
    with gzip.GzipFile(f, "wb", mtime=0) as g:      # mtime = 0: salida determinista
        g.write(df.to_csv(index=False).encode("utf-8"))
    sha = hashlib.sha256(f.read_bytes()).hexdigest()
    fila = {"fuente": "Eurostat (datos del INE)", "fichero": str(f.relative_to(RAIZ)), "url": url, "fecha_descarga": date.today().isoformat(),
            "edicion": edicion, "periodo": f"{df['time'].min()}-{df['time'].max()}" if "time" in df else "2001", "nivel_territorial": "NUTS 3 (provincia)",
            "n_filas": len(df), "sha256": sha, "licencia": "Eurostat: reutilización con cita (Decisión 2011/833/UE)", "redistribuible": "sí",
            "posterior_prereg": "sí", "notas": notas}
    antes = pd.read_csv(MANIFIESTO) if MANIFIESTO.exists() else pd.DataFrame()
    antes = antes[antes["fichero"] != fila["fichero"]] if len(antes) else antes
    pd.concat([antes, pd.DataFrame([fila])], ignore_index=True).to_csv(MANIFIESTO, index=False)
    print(nombre, len(df), sha[:12])


def main() -> int:
    # 1. Censo de 2001 por nacionalidad y NUTS 3 (todas las NUTS 3 de Europa; se filtra a ES)
    u = API + "cens_01rsctz?format=JSON&lang=EN&sex=T"
    js = pedir(u)
    df = jsonstat_a_df(js)
    df = df[df["geo"].str.startswith("ES")]
    guardar(df, "cens_01rsctz_ES_nuts3.csv.gz", u, js.get("updated", ""), "Censo de 2001 (1-11-2001), población total por nacionalidad y NUTS 3 de España; sexo = total")
    geos = sorted(df["geo"].unique())
    # 2. empleo por NUTS 3 y rama
    lote = []
    for i in range(0, len(geos), 25):
        g = "&".join(f"geo={x}" for x in geos[i:i + 25])
        js = pedir(API + f"nama_10r_3empers?format=JSON&lang=EN&wstatus=EMP&unit=THS&{g}")
        lote.append(jsonstat_a_df(js))
    emp = pd.concat(lote, ignore_index=True)
    guardar(emp, "nama_10r_3empers_ES_nuts3.csv.gz", API + "nama_10r_3empers?wstatus=EMP&unit=THS&geo=<NUTS 3 de ES>", js.get("updated", ""),
            "empleo (miles de personas, concepto nacional) por NUTS 3 y rama NACE Rev. 2 (A*10 y subramas)")
    # 3. población a 1 de enero por NUTS 3, edad y sexo total
    lote = []
    for i in range(0, len(geos), 25):
        g = "&".join(f"geo={x}" for x in geos[i:i + 25])
        js = pedir(API + f"demo_r_pjangrp3?format=JSON&lang=EN&sex=T&unit=NR&{g}")
        lote.append(jsonstat_a_df(js))
    pob = pd.concat(lote, ignore_index=True)
    guardar(pob, "demo_r_pjangrp3_ES_nuts3.csv.gz", API + "demo_r_pjangrp3?sex=T&unit=NR&geo=<NUTS 3 de ES>", js.get("updated", ""),
            "población a 1 de enero por NUTS 3 y grupo de edad quinquenal; sexo total")
    # 4. población a 1 de enero por NUTS 3 y grandes grupos de edad (serie larga desde 1990)
    lote = []
    for i in range(0, len(geos), 25):
        g = "&".join(f"geo={x}" for x in geos[i:i + 25])
        js = pedir(API + f"demo_r_pjanaggr3?format=JSON&lang=EN&sex=T&{g}")
        lote.append(jsonstat_a_df(js))
    pob2 = pd.concat(lote, ignore_index=True)
    guardar(pob2, "demo_r_pjanaggr3_ES_nuts3.csv.gz", API + "demo_r_pjanaggr3?sex=T&geo=<NUTS 3 de ES>", js.get("updated", ""),
            "población a 1 de enero por NUTS 3 y grandes grupos de edad (menos de 15, 15-64, 65 o más); sexo total; desde 1990")
    return 0


if __name__ == "__main__":
    sys.exit(main())
