"""V9-DATOS-COMPLETO (bloque 3, punto 15): Padrón continuo del INE por nacionalidad y por país de nacimiento,
provincia y municipio, 2003-2022 (una tabla jaxiT3 por provincia; «principales nacionalidades» y «país de nacimiento»).

Las tablas se localizaron escaneando los identificadores jaxiT3 33400-34150 (cabeceras con «Nacionalidad (principales
nacionalidades)» o «País de nacimiento»; docs/v9/decisiones_datos.md, D8). Se leen en streaming y solo se guarda
sexo = Total; los códigos territoriales salen de las etiquetas («46 Valencia/València», «46250 València»): nunca por
nombre. Para 2021-2025 el proyecto ya tiene el censo anual (22 grupos de nacionalidad) y para 1998-2002 solo hay
continentes; el inicio real de la serie por país es 2003 (1 de enero).

Salidas (data/raw/v9/ine_padron_nacionalidad/):
  padron_nacionalidad_2003_2022.csv.gz   anio, cod_provincia, cod_municipio ('' = total provincial), nacionalidad, poblacion
  padron_pais_nacimiento_2003_2022.csv.gz  ídem con pais_nacimiento
"""
from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import CABECERAS, RAIZ, RAW9, abrir_gz_texto, registrar, sha256  # noqa: E402

FUENTE = "ine_padron_nacionalidad"
DIR = RAW9 / FUENTE
URL = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{t}.csv?nocab=1"
RANGO = range(33400, 34151)
LICENCIA = "INE: reutilización con cita (Ley 37/2007)"
TIPOS = {"nacionalidad": "Nacionalidad (principales nacionalidades)", "pais_nacimiento": "País de nacimiento"}


def localizar() -> dict[str, list[int]]:
    """Identificadores de tabla por tipo (cabecera exacta). Caché en DIR/tablas.csv."""
    cache = DIR / "tablas.csv"
    if cache.exists():
        out: dict[str, list[int]] = {k: [] for k in TIPOS}
        with open(cache, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out[r["tipo"]].append(int(r["tabla"]))
        return out
    import concurrent.futures as cf

    def cab(t):
        try:
            r = requests.get(URL.format(t=t), headers=CABECERAS, timeout=60, stream=True)
            linea = next(r.iter_lines(decode_unicode=False), b"").decode("utf-8-sig", "replace")
            r.close()
            return t, linea
        except Exception:  # noqa: BLE001
            return t, ""
    with cf.ThreadPoolExecutor(12) as ex:
        res = list(ex.map(cab, RANGO))
    out = {k: [t for t, c in res if c.split(";")[-3:-2] == [v] or f";{v};Periodo" in c] for k, v in TIPOS.items()}
    DIR.mkdir(parents=True, exist_ok=True)
    with open(cache, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tipo", "tabla"])
        for k, ts in out.items():
            w.writerows([k, t] for t in ts)
    return out


def num(s: str) -> str:
    s = s.strip().replace(".", "").replace(",", ".")
    return s if re.fullmatch(r"-?\d+(\.\d+)?", s) else ""


def descargar_tipo(tipo: str, tablas: list[int]) -> tuple[Path, int, set]:
    salida = DIR / f"padron_{tipo}_2003_2022.csv.gz"
    claves = set()
    n = 0
    with abrir_gz_texto(salida) as g:
        w = csv.writer(g)
        w.writerow(["anio", "cod_provincia", "cod_municipio", tipo, "poblacion", "tabla"])
        for t in sorted(tablas):
            for intento in range(3):
                try:
                    r = requests.get(URL.format(t=t), headers=CABECERAS, timeout=300)
                    r.raise_for_status()
                    break
                except Exception:  # noqa: BLE001
                    if intento == 2:
                        raise
            texto = r.content.decode("utf-8-sig", "replace")
            lector = csv.reader(io.StringIO(texto), delimiter=";")
            cab = next(lector)
            i_sexo, i_per, i_val = cab.index("Sexo"), cab.index("Periodo"), len(cab) - 1
            i_mun = cab.index("Municipios")
            i_prov = cab.index("Provincias") if "Provincias" in cab else None
            i_cat = cab.index(TIPOS[tipo])
            for fila in lector:
                if len(fila) < len(cab) or fila[i_sexo] != "Total":
                    continue
                mun = re.match(r"^(\d{5}) ", fila[i_mun] or "")
                prov = re.match(r"^(\d{2}) ", fila[i_prov]) if i_prov is not None else None
                cod_mun = mun.group(1) if mun else ""
                cod_prov = prov.group(1) if prov else (cod_mun[:2] if cod_mun else "")
                if not cod_prov:
                    continue   # filas de isla u otros agregados sin código de provincia
                anio = re.search(r"(\d{4})", fila[i_per])
                v = num(fila[i_val])
                if not anio or v == "":
                    continue
                clave = (anio.group(1), cod_prov, cod_mun, fila[i_cat])
                if clave in claves:
                    continue
                claves.add(clave)
                w.writerow([*clave, v, t])
                n += 1
    return salida, n, {c[1] for c in claves}


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            print("falta _manifest.csv"); return 1
        with open(man, encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                ruta = RAIZ / fila["fichero"]
                if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK ine_padron_nacionalidad"); return 0
    tablas = localizar()
    for tipo, ts in tablas.items():
        ruta, n, provs = descargar_tipo(tipo, ts)
        registrar(FUENTE, ruta, URL.format(t="<tabla>"), edicion="Padrón continuo, tablas jaxiT3 por provincia (2003-2022)",
                  periodo="2003-2022 (1 de enero)", nivel_territorial="provincia y municipio (código INE)", licencia=LICENCIA,
                  redistribuible=True, notas=f"tablas={len(ts)}; filas={n}; provincias={len(provs)}; sexo=Total")
        print(tipo, len(ts), n, len(provs))
    registrar(FUENTE, DIR / "tablas.csv", URL.format(t="<escaneo 33400-34150>"), edicion="escaneo de cabeceras",
              periodo="", nivel_territorial="—", licencia=LICENCIA, redistribuible=True, notas="identificadores de tabla por tipo")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
