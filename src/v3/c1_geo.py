"""Centroides de sección censal (INE, seccionado 2021) para el EE de Conley. Lee el shapefile SIN geopandas.
Descomprime solo .shp/.dbf en un directorio temporal y lo borra. Caché: output/v3/C1/centroides.csv."""
import shutil
import struct
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ZIP = RAIZ / "data/raw/v3/cartografia/Cartografia_secc.zip"
CACHE = RAIZ / "output/v3/C1/centroides.csv"
BASE = "Seccionado_2021/SECC_CE_20210101"


def _dbf_cusec(b):
    n, hl, rl = struct.unpack("<xxxxIHH", b[:12])
    pos, off, ln = 32, 1, None
    while b[pos] != 0x0D:
        nombre = b[pos:pos + 11].split(b"\0")[0].decode()
        long_ = b[pos + 16]
        if nombre == "CUSEC":
            ln = (off, long_)
        off += long_
        pos += 32
    o, long_ = ln
    return [b[hl + i * rl + o: hl + i * rl + o + long_].decode().strip() for i in range(n)]


def _shp_centroides(b):
    """(x, y, área) del centroide de cada registro (anillos con signo: los huecos restan)."""
    pos, out = 100, []
    while pos < len(b):
        ln = struct.unpack(">i", b[pos + 4:pos + 8])[0] * 2
        c = b[pos + 8:pos + 8 + ln]
        pos += 8 + ln
        if struct.unpack("<i", c[:4])[0] != 5:
            out.append((np.nan, np.nan, 0.0))
            continue
        npart, npt = struct.unpack("<ii", c[36:44])
        parts = np.frombuffer(c, "<i4", npart, 44).tolist() + [npt]
        pts = np.frombuffer(c, "<f8", npt * 2, 44 + 4 * npart).reshape(-1, 2)
        A = cx = cy = 0.0
        for a, z in zip(parts[:-1], parts[1:]):
            p = pts[a:z]
            x0, y0 = p[:-1, 0], p[:-1, 1]
            x1, y1 = p[1:, 0], p[1:, 1]
            cr = x0 * y1 - x1 * y0
            a2 = cr.sum() / 2
            A += a2
            cx += ((x0 + x1) * cr).sum() / 6
            cy += ((y0 + y1) * cr).sum() / 6
        out.append((cx / A, cy / A, A) if A != 0 else (p[:, 0].mean(), p[:, 1].mean(), 0.0))
    return out


def centroides():
    """DataFrame codigo (10 díg.), x, y (m, ETRS89 UTM 30N). Usa la caché si existe."""
    if CACHE.exists():
        return pd.read_csv(CACHE, dtype={"codigo": str})
    tmp = Path(tempfile.mkdtemp(prefix="c1_shp_"))
    try:
        with zipfile.ZipFile(ZIP) as z:
            for e in (".shp", ".dbf"):
                z.extract(BASE + e, tmp)
        cu = _dbf_cusec((tmp / (BASE + ".dbf")).read_bytes())
        ce = _shp_centroides((tmp / (BASE + ".shp")).read_bytes())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    d = pd.DataFrame({"codigo": cu, "x": [c[0] for c in ce], "y": [c[1] for c in ce], "a": [abs(c[2]) for c in ce]})
    d["a"] = d.a.where(d.a > 0, 1.0)
    d["xa"], d["ya"] = d.x * d.a, d.y * d.a
    g = d.groupby("codigo")[["xa", "ya", "a"]].sum()
    out = pd.DataFrame({"codigo": g.index, "x": (g.xa / g.a).values, "y": (g.ya / g.a).values})
    out.round(1).to_csv(CACHE, index=False)
    return out
