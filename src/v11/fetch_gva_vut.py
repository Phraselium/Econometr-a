"""V11-DATOS (bloque 4, punto 16): Generalitat Valenciana, registro de viviendas de uso turístico, NUEVO corte del
histórico con fechas de alta y baja (recursos del conjunto dades-turisme-habitatges-comunitat-valenciana-2025,
última modificación 2025-11-12; V9 tenía el corte de 2025-01-26 en data/raw/v9/gva_vut/cortes/). Se guarda solo si
el contenido difiere de los cortes de V9 (sha256 o firma: filas, estados, fechas máximas). Resultado 2026-10-15: el
recurso «2025-11-12» es una re-subida del corte de 2025-01-26 (mismo contenido): no hay edición nueva. Licencia CC BY 4.0. Codificación latin-1, separador «;».
Cortes antiguos en web.archive.org: la conexión con archive.org falla en el entorno (fuentes_fallidas.md).
"""
from __future__ import annotations

import gzip
import shutil
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, RAIZ, RAW11, contar_filas, descargar, registrar, sha256, verificar_manifiesto  # noqa: E402

FUENTE = "gva_vut"
DIR = RAW11 / FUENTE
API = "https://dadesobertes.gva.es/api/3/action/package_show?id=dades-turisme-habitatges-comunitat-valenciana-2025"
LIC = "Generalitat Valenciana: CC BY 4.0"


def firma(ruta: Path) -> tuple:
    """Contenido equivalente: nº de filas, estados y fechas máximas de alta y baja (el sha cambia con re-subidas)."""
    import pandas as pd
    d = pd.read_csv(ruta, sep=";", encoding="latin-1", dtype=str)
    return (len(d), tuple(sorted(d["Estado"].value_counts().items())) if "Estado" in d else (),
            str(pd.to_datetime(d["Fecha alta"], format="%d/%m/%Y", errors="coerce").max()) if "Fecha alta" in d else "",
            str(pd.to_datetime(d["Fecha baja"], format="%d/%m/%Y", errors="coerce").max()) if "Fecha baja" in d else "")


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        if not (DIR / "_manifest.csv").exists():   # sin edición nueva: nada propio que verificar (los cortes están en v9)
            print("gva_vut: sin edición nueva respecto a data/raw/v9/gva_vut (nada que verificar)")
            return 0
        return verificar_manifiesto(FUENTE)
    v9 = {sha256(p) for p in (RAIZ / "data/raw/v9/gva_vut/cortes").glob("*.csv.gz")}
    firmas_v9 = {firma(p) for p in (RAIZ / "data/raw/v9/gva_vut/cortes").glob("*.csv.gz")}
    p = requests.get(API, headers=CABECERAS, timeout=120).json()["result"]
    for r in p["resources"]:
        fecha = (r.get("last_modified") or r.get("created") or "")[:10]
        tipo = "historico" if "Hist" in (r.get("name") or "") else "ultimo_periodo"
        bruto = descargar(r["url"], DIR / "original" / f"vut_{tipo}_{fecha}.csv", timeout=900)
        destino = DIR / f"vut_{tipo}_{fecha}.csv.gz"
        with open(bruto, "rb") as fi, gzip.GzipFile(filename="", mode="wb", fileobj=open(destino, "wb"), mtime=0) as fo:
            shutil.copyfileobj(fi, fo)
        if sha256(destino) in v9 or firma(destino) in firmas_v9:
            destino.unlink()
            print("igual que V9:", tipo)
            continue
        registrar(FUENTE, destino, r["url"], edicion=f"{r.get('name')} (modificado {fecha})", periodo=f"corte {fecha}",
                  nivel_territorial="registro individual (municipio INE, CP)", licencia=LIC, redistribuible=True,
                  notas=f"latin-1, separador ';'; campos Estado, Fecha alta, Fecha baja; filas={contar_filas(destino)}")
        print(tipo, fecha, contar_filas(destino))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
