"""V11-DATOS (histórico, A2): Catastro, «Otras estadísticas» municipales (sede → Estadísticas → Otras estadísticas):
ficheros xlsx por provincia con detalle municipal, solo publicados para 2019 (y 2020 en superficie/uso); desde 2022 esa
sección solo trae piscinas. URL: https://www.catastro.hacienda.gob.es/documentos/estadisticas/extenionocupacion/<año>/<tabla>_m<PP>.xlsx
- aant: viviendas por año de CONSTRUCCIÓN (tramos) y tipo (colectiva o unifamiliar);
- aref: viviendas por año de REFORMA (tramos) y tipo;
- sunau: superficie y uso (inmuebles por uso).
Formato largo: anio_fichero, tabla, cod_municipio (código INE de la primera columna), grupo (cabecera de la fila 0),
categoria (fila 1), valor. Régimen común. Licencia Catastro: reutilización libre con reconocimiento.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "catastro_otras"
DIR = RAW11 / FUENTE
URL = "https://www.catastro.hacienda.gob.es/documentos/estadisticas/extenionocupacion/{a}/{t}_m{p}.xlsx"
LIC = "Catastro (DGC): reutilización libre con reconocimiento de la fuente"
PROV = ["02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "21",
        "22", "23", "24", "25", "26", "27", "28", "29", "30", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41",
        "42", "43", "44", "45", "46", "47", "49", "50", "51", "52"]
COMBOS = [(2019, "aant"), (2019, "aref"), (2019, "sunau"), (2020, "sunau"), (2020, "aant"), (2020, "aref")]


def largo(ruta: Path, a: int, t: str) -> pd.DataFrame:
    filas = []
    for hoja, x in pd.read_excel(ruta, sheet_name=None, header=None, dtype=str).items():
        g = x.iloc[0].ffill()
        c = x.iloc[1].fillna(x.iloc[0])
        datos = x[x[0].fillna("").str.fullmatch(r"\d{5}")]
        for j in range(2, x.shape[1]):
            v = pd.to_numeric(datos[j], errors="coerce")
            filas.append(pd.DataFrame({"anio_fichero": a, "tabla": t, "hoja": hoja, "cod_municipio": datos[0].values,
                                       "grupo": str(g[j]).strip(), "categoria": str(c[j]).strip(), "valor": v.values}))
    return pd.concat(filas, ignore_index=True).dropna(subset=["valor"])


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    partes, faltan = [], []
    for a, t in COMBOS:
        for p in PROV:
            dest = DIR / "original" / f"{t}_{a}_m{p}.xlsx"
            if not dest.exists():
                r = requests.get(URL.format(a=a, t=t, p=p), headers=CABECERAS, timeout=120)
                if r.status_code != 200 or not r.content.startswith(b"PK"):
                    faltan.append(f"{a}-{t}-{p}")
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(r.content)
            partes.append(largo(dest, a, t))
        print(a, t, sum(len(x) for x in partes), flush=True)
    D = pd.concat(partes, ignore_index=True)
    r = DIR / "catastro_otras_municipio.csv.gz"
    D.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, URL.format(a="<año>", t="<tabla>", p="<PP>"), edicion="Catastro, otras estadísticas (extensión ocupación)",
              periodo=f"{D.anio_fichero.min()}-{D.anio_fichero.max()}", nivel_territorial="municipio (código INE; régimen común)",
              licencia=LIC, redistribuible=True, notas=f"tablas {sorted(D.tabla.unique())}; combinaciones sin fichero: {len(faltan)} ({faltan[:12]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
