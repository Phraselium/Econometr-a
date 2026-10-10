"""R1b (fetch, fuera de make): centroides municipales a partir del seccionado INE 2021.

Lee data/raw/v3/cartografia/Cartografia_secc.zip (110 MB, no versionado) y escribe
data/raw/v5/municipio_centroides_utm30.csv (pequeño, versionable). Sin red; solo analiza el zip local.
Centro del municipio = media de los centros de caja de sus secciones (ETRS89 UTM 30N, metros).
"""
import struct
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ZIP = RAIZ / "data/raw/v3/cartografia/Cartografia_secc.zip"
SALIDA = RAIZ / "data/raw/v5/municipio_centroides_utm30.csv"


def leer_dbf_campo(buf: bytes, campo: str) -> list[str]:
    n, hl, rl = struct.unpack("<IHH", buf[4:12])
    pos, off, cols = 32, 1, {}
    while buf[pos] != 0x0D:
        nombre = buf[pos:pos + 11].split(b"\0")[0].decode()
        cols[nombre] = (off, buf[pos + 16])
        off += buf[pos + 16]
        pos += 32
    o, ln = cols[campo]
    return [buf[hl + i * rl + o: hl + i * rl + o + ln].decode("latin-1").strip() for i in range(n)]


def main():
    z = zipfile.ZipFile(ZIP)
    pre = "Seccionado_2021/SECC_CE_20210101"
    cusec = leer_dbf_campo(z.read(pre + ".dbf"), "CUSEC")
    shp = z.read(pre + ".shp")
    pos, cx, cy = 100, [], []
    while pos < len(shp):
        _, ln = struct.unpack(">ii", shp[pos:pos + 8])
        tipo = struct.unpack("<i", shp[pos + 8:pos + 12])[0]
        if tipo == 0:
            cx.append(np.nan); cy.append(np.nan)
        else:
            x0, y0, x1, y1 = struct.unpack("<4d", shp[pos + 12:pos + 44])
            cx.append((x0 + x1) / 2); cy.append((y0 + y1) / 2)
        pos += 8 + ln * 2
    assert len(cx) == len(cusec), (len(cx), len(cusec))
    d = pd.DataFrame({"codigo": [c[:5] for c in cusec], "x": cx, "y": cy}).dropna()
    g = d.groupby("codigo").agg(x_m=("x", "mean"), y_m=("y", "mean"), n_secciones=("x", "size")).reset_index()
    g.round(1).to_csv(SALIDA, index=False)
    print(len(g), "municipios ->", SALIDA)


if __name__ == "__main__":
    main()
