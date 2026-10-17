"""V16 fase 2 · carga de microdatos ECV transversales 2004-2025 (INE), sin red.

Devuelve una tabla por hogar con las variables necesarias para el esfuerzo de acceso.
Solo lectura de data/raw. No toca data/sealed (la ECV no tiene provincia: solo DB040, NUTS2).
Caché opcional en parquet (ECON_V16_CACHE; por defecto el directorio temporal del sistema).
"""
from __future__ import annotations

import io
import os
import re
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
ANIOS = list(range(2004, 2026))


def ruta_zip(y: int) -> Path:
    cands = [RAW / "v16/renta_parque/ecv/transversal_2004_2012" / f"ecvb04_{y}.zip",
             RAW / "v16/renta_parque/ecv" / f"datos_{y}.zip",
             RAW / "v9/ine_microdatos/ecv" / f"datos_{y}.zip"]
    for c in cands:
        if c.exists():
            return c
    raise FileNotFoundError(f"ECV {y}")


def _recoge(z: zipfile.ZipFile, out: dict) -> None:
    for n in z.namelist():
        b = n.split("/")[-1]
        if b.lower().endswith(".zip") and not b.lower().startswith("disreg"):
            _recoge(zipfile.ZipFile(io.BytesIO(z.read(n))), out)
        elif re.fullmatch(r"esudb\d\d([dhpr])(_arope)?\.csv", b.lower()):
            k = re.fullmatch(r"esudb\d\d([dhpr])(_arope)?\.csv", b.lower()).group(1)
            out.setdefault(k, (z, n))


def _lee(y: int, fich: str, cols: list[str]) -> pd.DataFrame:
    z = zipfile.ZipFile(ruta_zip(y))
    d: dict = {}
    _recoge(z, d)
    zz, nn = d[fich]
    head = pd.read_csv(zz.open(nn), nrows=0).columns
    usar = [c for c in cols if c in head]
    return pd.read_csv(zz.open(nn), usecols=usar, low_memory=False)


def cargar_anio(y: int) -> pd.DataFrame:
    D = _lee(y, "d", ["DB030", "DB040", "DB090"])
    H = _lee(y, "h", ["HB030", "HY020", "HY070G", "HY070N", "HH070", "HH020", "HH021", "HX040", "HX240", "HX060",
                                  "cuotahip", "HH060"])
    R = _lee(y, "r", ["RB010", "RB030", "RB050", "RB080", "RB090", "RB290"])
    pcols = ["PB030", "PB040", "PB220A"] + [f"PY{k}N" for k in
                                         ("010", "020", "021", "035", "050", "080", "090", "100", "110", "120", "130", "140")]
    P = _lee(y, "p", pcols)
    R["hid"] = R.RB030 // 100
    P["hid"] = P.PB030 // 100
    R["edad"] = R.RB010 - R.RB080
    ycols = [c for c in P.columns if c.startswith("PY")]
    P["renta_pers"] = P[ycols].fillna(0).sum(axis=1)
    nat = "PB220A" if "PB220A" in P.columns else None
    P = P.merge(R[["RB030", "edad"] + (["RB290"] if "RB290" in R.columns else [])],
                left_on="PB030", right_on="RB030", how="left")
    if nat:
        P["nac_raw"] = P[nat].astype(str).str.strip()
    else:
        P["nac_raw"] = P["RB290"].astype(str).str.strip()
    # sustentador principal: mayor renta personal neta; empate: mayor edad; luego menor PB030
    P = P.sort_values(["hid", "renta_pers", "edad", "PB030"], ascending=[True, False, False, True])
    S = P.drop_duplicates("hid")[["hid", "edad", "nac_raw", "renta_pers"]].rename(
        columns={"edad": "edad_sust", "renta_pers": "renta_sust"})
    # población del hogar (pesos RB050) y suma de pesos personales
    Rh = R.groupby("hid").agg(pop_w=("RB050", "sum"), n_pers=("RB050", "size")).reset_index()
    H = H.rename(columns={"HB030": "hid"})
    D = D.rename(columns={"DB030": "hid"})
    df = D.merge(H, on="hid", how="inner").merge(S, on="hid", how="left").merge(Rh, on="hid", how="left")
    df["anio"] = y
    for c in df.columns:
        if c not in ("nac_raw", "DB040"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["nac_raw"] = df["nac_raw"].astype(str).str.strip()
    df["DB040"] = df["DB040"].astype(str).str.strip()
    return df


def cargar(cache: bool = True, anios=None) -> pd.DataFrame:
    anios = list(anios or ANIOS)
    cdir = Path(os.environ.get("ECON_V16_CACHE", tempfile.gettempdir())) / "v16_f2_cache_v3"
    out = []
    for y in anios:
        f = cdir / f"hogares_{y}.parquet"
        if cache and f.exists():
            out.append(pd.read_parquet(f))
            continue
        df = cargar_anio(y)
        if cache:
            cdir.mkdir(parents=True, exist_ok=True)
            df.to_parquet(f)
        out.append(df)
    return pd.concat(out, ignore_index=True, sort=False)


if __name__ == "__main__":
    d = cargar()
    print(d.groupby("anio").size())
    print(d.columns.tolist())
