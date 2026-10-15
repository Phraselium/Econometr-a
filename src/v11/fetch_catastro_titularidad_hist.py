"""V11-DATOS (histórico, A1): Catastro, TITULARES por municipio 2006-2023 (visor JAXI de la sede:
https://www.catastro.hacienda.gob.es/jaxi/tabla.do?path=/est<año>/catastro/titulares/&file=040<PP>.px, un fichero por
provincia; se envía el formulario con todas las opciones y se lee la tabla HTML).
Variable: número de TITULARES (personas o entidades titulares catastrales) por municipio y clase de inmueble (urbano,
rústico, urbano/rústico = titulares distintos en el conjunto). Cambio de definición frente a los CSV de 2024-2026
(fetch_catastro_titularidad.py): aquellos cuentan sujetos pasivos del padrón del IBI e inmuebles por tramo de nº de
inmuebles y tipo de persona; esta serie es un recuento total sin tramos ni tipo de persona. No se encadenan: se
guardan como variables distintas. Régimen común (sin País Vasco ni Navarra). Cruce por el código INE de 5 dígitos de
la etiqueta del municipio. Caché por año y provincia en tmp/ (no versionada).
Licencia Catastro: reutilización libre con reconocimiento.
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "catastro_titularidad"
DIR = RAW11 / FUENTE
B = "https://www.catastro.hacienda.gob.es/jaxi/tabla.do"
LIC = "Catastro (DGC): reutilización libre con reconocimiento de la fuente"
PROV = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "21",
        "22", "23", "24", "25", "26", "27", "28", "29", "30", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41",
        "42", "43", "44", "45", "46", "47", "49", "50", "51", "52"]
ANIOS = range(2006, 2024)


def num(x) -> float:
    x = str(x).strip().replace(".", "").replace(",", ".")
    return pd.to_numeric(x, errors="coerce")


def provincia(s: requests.Session, a: int, p: str) -> pd.DataFrame | None:
    path, fich = f"/est{a}/catastro/titulares/", f"040{p}.px"
    h = s.get(B, params={"path": path, "file": fich, "type": "pcaxis", "L": "0"}, headers=CABECERAS, timeout=120).content.decode("cp1252", "replace")
    m1, m2 = re.search(r'name="cri1".*?</select>', h, re.S), re.search(r'name="cri2".*?</select>', h, re.S)
    if not (m1 and m2):
        return None
    c1 = re.findall(r'<option[^>]*value="?(\d{4})"?', m1.group(0))
    c2 = re.findall(r'<option[^>]*value="?(\d{4})"?', m2.group(0))
    data = ([("cri1", v) for v in c1] + [("cri2", v) for v in c2] +
            [("rows", "municipios"), ("columns", "catastro"), ("numCri", "2"), ("NumCeldas", str(len(c1) * len(c2))),
             ("type", "pcaxis"), ("path", path), ("file", fich), ("divi", ""), ("per", ""), ("idtab", ""), ("accion", "html")])
    t = s.post(B, data=data, headers=CABECERAS, timeout=300).content.decode("cp1252", "replace")
    tab = max(pd.read_html(io.StringIO(t)), key=len)
    cab = [str(x).strip() for x in tab.iloc[0]]
    tab = tab.iloc[1:]
    tab.columns = ["municipio"] + cab[1:]
    tab = tab[tab.municipio.astype(str).str.match(r"^\d{5} ")]
    out = pd.DataFrame({"anio": a, "cod_municipio": tab.municipio.str[:5]})
    for c in cab[1:]:
        out[{"Urbano": "titulares_urbano", "Rústico": "titulares_rustico", "Urbano/Rústico": "titulares_total"}.get(c, c)] = tab[c].map(num).values
    return out


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    cache = DIR / "tmp" / "hist"
    cache.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    partes, faltan = [], []
    for a in ANIOS:
        for p in PROV:
            c = cache / f"{a}_{p}.csv"
            if c.exists():
                partes.append(pd.read_csv(c, dtype={"cod_municipio": str}))
                continue
            d = None
            for _ in range(3):
                try:
                    d = provincia(s, a, p)
                    break
                except Exception:  # noqa: BLE001
                    d = None
            if d is None or d.empty:
                faltan.append(f"{a}-{p}")
                continue
            d.to_csv(c, index=False)
            partes.append(d)
        print(a, sum(len(x) for x in partes), flush=True)
    D = pd.concat(partes, ignore_index=True).sort_values(["anio", "cod_municipio"])
    r = DIR / "titulares_municipio_2006_2023.csv.gz"
    D.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, B + "?path=/est<año>/catastro/titulares/&file=040<PP>.px", edicion="Catastro, JAXI titulares por municipio",
              periodo=f"{D.anio.min()}-{D.anio.max()}", nivel_territorial="municipio (código INE; régimen común)", licencia=LIC,
              redistribuible=True, notas=f"recuento de titulares por clase; distinta definición que los CSV 2024-2026; faltan={faltan[:30]}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
