"""M4 descargas (unico script con red). Ejecutar a mano: python3 src/v4/m4_fetch.py
Descarga tablas INE (API Tempus) a data/raw/v4/ y anade entradas a data/raw/_manifest.csv.
  59523 Censo 2021: viviendas principales por regimen de tenencia (nacional, CCAA, provincias)
  59529 Censo 2021: viviendas principales por regimen de tenencia (municipios grandes)
  50256 ETDP: % compraventas de viviendas segun transmitente y titular (persona fisica/juridica)
  50272 ETDP: idem (otra base)
"""
import csv
import datetime as dt
import json
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DEST = RAIZ / "data" / "raw" / "v4"
TABLAS = {59523: 1, 59529: 1, 50256: 400, 50272: 400}
API = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{t}?nult={n}"


def descarga(t, n):
    url = API.format(t=t, n=n)
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return url, json.load(r)
        except Exception:
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"fallo {url}")


def fe_url(u):
    return u


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    man = RAIZ / "data" / "raw" / "_manifest.csv"
    filas = []
    for t, n in TABLAS.items():
        url, d = descarga(t, n)
        out = DEST / f"ine_v4_t{t}.csv"
        cnt = 0
        fmin = fmax = None
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["tabla", "serie_nombre", "fecha", "valor", "url"])
            for s in d:
                for p in s.get("Data", []):
                    v = p.get("Valor")
                    if v is None:
                        continue
                    fe = dt.datetime.fromtimestamp(p["Fecha"] / 1000, dt.timezone.utc).strftime("%Y-%m-%d") if p.get("Fecha") else ""
                    w.writerow([t, s["Nombre"], fe, v, fe_url(url)])
                    cnt += 1
                    a = fe[:4]
                    if a:
                        fmin = a if fmin is None or a < fmin else fmin
                    fmax = a if fmax is None or a > fmax else fmax
        filas.append([f"v4/{out.name}", f"INE tabla {t} (API Tempus)", len(d), fmin, fmax, cnt, 0,
                      dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")])
        print(out.name, cnt)
    with open(man, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(filas)


if __name__ == "__main__":
    main()
