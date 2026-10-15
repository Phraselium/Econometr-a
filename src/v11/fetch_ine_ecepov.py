"""V11-DATOS (bloque 2, punto 10): INE, Encuesta de Características Esenciales de la Población y las Viviendas
(ECEPOV) 2021, microdatos (ftp INE /ftp/microdatos/ecepov/datos_2021.zip, 197 MB; ficheros de adultos, hogar y
vivienda). Los microdatos no se versionan (tamaño; `make datos_v11`); se versiona el inventario de variables
(nombre, descripción, posición, fichero) leído de los diseños de registro oficiales, para documentar qué cruces por
origen permite (nacionalidad, país de nacimiento, año de llegada, tenencia, superficie, gasto en vivienda).
Licencia INE: reutilización con cita.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "ine_ecepov"
DIR = RAW11 / FUENTE
URL = "https://www.ine.es/ftp/microdatos/ecepov/{f}"
LIC = "INE: reutilización con cita (Ley 37/2007); microdatos públicos"


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    zd = descargar(URL.format(f="disreg_ecepov21.zip"), DIR / "original" / "disreg_ecepov21.zip", timeout=300)
    zp = descargar(URL.format(f="datos_2021.zip"), DIR / "original" / "datos_2021.zip", timeout=3600)
    filas = []
    with zipfile.ZipFile(zd) as z:
        for n in sorted(x for x in z.namelist() if x.endswith(".xlsx")):
            with z.open(n) as f:
                v = pd.read_excel(f, sheet_name=0, header=1, dtype=str)
            v = v[v.iloc[:, 0].notna() & ~v.iloc[:, 0].str.startswith("*")]
            for _, r in v.iterrows():
                filas.append({"fichero": n.replace("dr_ECEPOV", "").replace("_2021.xlsx", ""), "variable": r.iloc[0],
                              "posicion": r.get("Posición", ""), "longitud": r.get("Longitud", ""),
                              "descripcion": str(r.get("Descripción ", r.get("Descripción", ""))).replace("\n", " ")[:200]})
    inv = pd.DataFrame(filas)
    r = DIR / "variables_ecepov2021.csv"
    inv.to_csv(r, index=False)
    registrar(FUENTE, r, URL.format(f="disreg_ecepov21.zip"), edicion="ECEPOV 2021, diseños de registro", periodo="2021",
              nivel_territorial="(inventario de variables)", licencia=LIC, redistribuible=True, notas=f"{len(inv)} variables")
    with zipfile.ZipFile(zp) as z:
        cont = ", ".join(n for n in z.namelist() if not n.endswith("/"))[:300]
    for p, nota in ((zp, f"microdatos; contenido: {cont}"), (zd, "diseños de registro")):
        registrar(FUENTE, p, URL.format(f=p.name), edicion="ECEPOV 2021 (ftp INE)", periodo="2021", nivel_territorial="microdatos",
                  licencia=LIC, redistribuible=True, notas=f"no versionado (tamaño): se regenera con make datos_v11; {nota}")
    print(len(inv), cont[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
