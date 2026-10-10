"""B3 · geometría provincial simplificada (script *_fetch, fuera de make: lee data/raw/v3/cartografia/Cartografia_secc.zip, ignorado por git).
Rasteriza las secciones censales 2021 (INE) a 2 km, extrae el contorno de cada provincia y lo guarda en
data/raw/v5/prov_geom_simplificada.json (versionado, pequeño). Canarias se traslada +750 km en y (recuadro). Sin pyshp/geopandas:
lectura propia del .shp/.dbf. Determinista."""
import io
import json
import struct
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from scipy import ndimage  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
ZIP = RAIZ / "data/raw/v3/cartografia/Cartografia_secc.zip"
OUTJ = RAIZ / "data/raw/v5/prov_geom_simplificada.json"
RES = 2000.0


def lee_dbf(b, campo="CPRO"):
    nrec, hlen, rlen = struct.unpack("<IHH", b[4:12])
    campos, off, pos = [], 1, 32
    while b[pos] != 0x0D:
        nm = b[pos:pos + 11].split(b"\0")[0].decode()
        ln = b[pos + 16]
        campos.append((nm, off, ln))
        off += ln
        pos += 32
    d = {n: (o, ln) for n, o, ln in campos}
    o, ln = d[campo]
    return [b[hlen + i * rlen + o: hlen + i * rlen + o + ln].decode("latin1").strip() for i in range(nrec)]


def lee_shp(b):
    pos, polys = 100, []
    while pos < len(b):
        clen = struct.unpack(">i", b[pos + 4:pos + 8])[0] * 2
        c = b[pos + 8: pos + 8 + clen]
        pos += 8 + clen
        t = struct.unpack("<i", c[:4])[0]
        if t == 0:
            polys.append([])
            continue
        npart, npt = struct.unpack("<ii", c[36:44])
        parts = np.frombuffer(c, "<i4", npart, 44)
        pts = np.frombuffer(c, "<f8", npt * 2, 44 + 4 * npart).reshape(-1, 2)
        ends = list(parts[1:]) + [npt]
        polys.append([pts[s:e] for s, e in zip(parts, ends)])
    return polys


def main():
    z = zipfile.ZipFile(ZIP)
    base = "Seccionado_2021/SECC_CE_20210101"
    cpro = lee_dbf(z.read(base + ".dbf"))
    polys = lee_shp(z.read(base + ".shp"))
    assert len(cpro) == len(polys), (len(cpro), len(polys))
    prov = np.array([int(c) if c.isdigit() else -1 for c in cpro])
    canarias = np.isin(prov, [35, 38])
    xmin, xmax, ymin, ymax = -1000e3, 1300e3, 3050e3, 4900e3
    nx, ny = int((xmax - xmin) / RES), int((ymax - ymin) / RES)
    lab = np.zeros((ny, nx), np.int16)
    for pid, (rings, p, ca) in enumerate(zip(polys, prov, canarias)):
        if p < 1 or p > 50:
            continue
        for r in rings:
            if len(r) < 4:
                continue
            xs = r[:, 0]
            ys = r[:, 1] + (750e3 if ca else 0.0)
            a2 = (xs[:-1] * ys[1:] - xs[1:] * ys[:-1]).sum()
            if a2 > 0:                       # anillo antihorario = hueco en shapefile
                continue
            i0, i1 = int((xs.min() - xmin) // RES), int((xs.max() - xmin) // RES) + 1
            j0, j1 = int((ys.min() - ymin) // RES), int((ys.max() - ymin) // RES) + 1
            i0, j0 = max(i0, 0), max(j0, 0)
            i1, j1 = min(i1, nx), min(j1, ny)
            if i1 <= i0 or j1 <= j0:
                continue
            gx, gy = np.meshgrid(xmin + (np.arange(i0, i1) + 0.5) * RES, ymin + (np.arange(j0, j1) + 0.5) * RES)
            inside = MPath(np.column_stack([xs, ys])).contains_points(np.column_stack([gx.ravel(), gy.ravel()])).reshape(gx.shape)
            sub = lab[j0:j1, i0:i1]
            sub[inside] = p
    out = {}
    for p in range(1, 51):
        m = ndimage.binary_fill_holes(ndimage.binary_closing(lab == p, iterations=1))
        if not m.any():
            continue
        fig = plt.figure()
        cs = plt.contour(np.pad(m.astype(float), 1), [0.5])
        rings = []
        for seg in cs.allsegs[0]:
            if len(seg) < 4:
                continue
            xy = np.column_stack([xmin + (seg[:, 0] - 1 + 0.5) * RES, ymin + (seg[:, 1] - 1 + 0.5) * RES]) / 1000.0
            rings.append(np.round(xy[:: max(1, len(xy) // 150)], 1).tolist())
        plt.close(fig)
        out[f"{p:02d}"] = rings
    json.dump(out, open(OUTJ, "w"))
    print(len(out), OUTJ.stat().st_size)


if __name__ == "__main__":
    main()
