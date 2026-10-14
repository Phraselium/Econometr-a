"""V9-DATOS: Censo Anual de Población (INE, operación 463) por municipio, sexo y nacionalidad (España/extranjera).

Fuente API: servicios.ine.es/wstempus/js/ES/DATOS_TABLA/<tabla>?nult=5
  - 69343: Población por sexo y nacionalidad (española/extranjera), por municipio (ediciones 2021-último).
  - 68065: Población según municipio y sexo (control: total nacional y total municipal).
Códigos de municipio: diccionario INE de municipios a 1-1-2026 (data/raw/ine_diccionario_municipios_2026.xlsx).
Sección censal: la API de tablas no ofrece sección con nacionalidad; no se descarga aquí (ver notas de la fila de manifiesto).
"""
from __future__ import annotations

import csv
import gzip
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from src.v9.comun import RAW9, descargar, registrar, sha256  # noqa: E402

FUENTE = "ine_censo_anual"
DIR = RAW9 / FUENTE
DIC = RAIZ / "data" / "raw" / "ine_diccionario_municipios_2026.xlsx"
TABLAS = {"69343": "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/69343?nult=5",
          "68065": "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/68065?nult=5"}
LICENCIA = "Aviso legal INE: reutilización con cita (Ley 37/2007)"
EDICIONES = range(2021, 2026)
CAB = ["edicion", "cod_municipio", "municipio_nombre_ine", "sexo", "nacionalidad", "poblacion", "tabla", "id_serie"]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def variantes(nombre: str) -> set[str]:
    """Claves de emparejamiento: nombre tal cual, con artículo final invertido (', El' -> 'El ') y partes separadas por '/'."""
    out = {norm(nombre)}
    m = re.match(r"^(.*), (el|la|los|las|l'|els|les|lo)$", nombre.strip(), re.I)
    if m:
        out.add(norm(f"{m.group(2)} {m.group(1)}"))
    for p in nombre.split("/"):
        out.add(norm(p))
    return out


def cargar_diccionario() -> dict[str, set[str]]:
    import pandas as pd
    df = pd.read_excel(DIC, sheet_name="dic25", header=None, dtype=str, skiprows=2)
    df.columns = ["codauto", "cpro", "cmun", "dc", "nombre"]
    idx: dict[str, set[str]] = {}
    for _, r in df.dropna(subset=["cpro", "cmun", "nombre"]).iterrows():
        cod = f"{r.cpro.zfill(2)}{r.cmun.zfill(3)}"
        for k in variantes(r.nombre):
            idx.setdefault(k, set()).add(cod)
    return idx


def parsear_serie(nombre: str):
    n = re.sub(r"\.\s*Todas las edades\.\s*Dato base\.\s*$", "", nombre.strip())
    partes = n.rsplit(". ", 2)
    if len(partes) != 3:
        return None
    return partes  # municipio, sexo, nacionalidad


def main(verificar: bool = False) -> int:
    man = DIR / "_manifest.csv"
    if verificar:
        if not man.exists():
            print("sin manifiesto")
            return 1
        ok = True
        with open(man, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                p = RAIZ / r["fichero"]
                if not p.exists() or sha256(p) != r["sha256"]:
                    print("FALLO", r["fichero"])
                    ok = False
        return 0 if ok else 1

    DIR.mkdir(parents=True, exist_ok=True)
    orig = DIR / "original"
    series = {}
    for tabla, url in TABLAS.items():
        bruto = descargar(url, orig / f"ine_t{tabla}_nult5.json")
        gz = orig / f"ine_t{tabla}_nult5.json.gz"
        with open(bruto, "rb") as fi, gzip.open(gz, "wb") as fo:
            fo.write(fi.read())
        bruto.unlink()
        registrar(FUENTE, gz, url, "2021-2025", "1 de enero", "municipio", LICENCIA, True,
                  f"Tabla INE {tabla} tal cual (JSON gzip)")
        series[tabla] = json.loads(gzip.open(gz, "rt", encoding="utf-8").read())

    dic = cargar_diccionario()
    filas, sin_match, ambiguos, nombres = [], set(), set(), {}
    for s in series["69343"]:
        p = parsear_serie(s["Nombre"])
        if p is None:
            continue
        mun, sexo, nac = p
        if mun not in nombres:
            cods = set()
            for k in variantes(mun):
                cods |= dic.get(k, set())
            if len(cods) == 1:
                nombres[mun] = (cods.pop(), "ok")
            elif len(cods) > 1:
                nombres[mun] = ("", "ambiguo")
            else:
                nombres[mun] = ("", "no_encontrado")
        cod, estado = nombres[mun]
        if estado == "no_encontrado":
            sin_match.add(mun)
        if estado == "ambiguo":
            ambiguos.add(mun)
        if not cod:
            continue
        for v in s["Data"]:
            if v["Anyo"] in EDICIONES and not v.get("Secreto") and v["Valor"] is not None:
                filas.append([v["Anyo"], cod, mun, sexo, nac, int(round(v["Valor"])), "69343", s["COD"]])

    salida = DIR / "ine_censo_anual_municipio_sexo_nacionalidad.csv.gz"
    with gzip.open(salida, "wt", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CAB)
        w.writerows(filas)
    registrar(FUENTE, salida, TABLAS["69343"], "2021-2025", "1 de enero", "municipio", LICENCIA, True,
              "Derivado de tabla 69343 (sexo x nacionalidad española/extranjera). Sin sección ni países.")

    corr = DIR / "correspondencia_municipio_nombre_codigo.csv"
    with open(corr, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["municipio_nombre_ine", "cod_municipio", "estado", "origen"])
        for mun, (cod, est) in sorted(nombres.items()):
            w.writerow([mun, cod, est, "data/raw/ine_diccionario_municipios_2026.xlsx (dic25, 1-1-2026); emparejamiento por nombre"])
    registrar(FUENTE, corr, "https://www.ine.es/daco/daco42/codmun/codmun.htm", "1-1-2026", "1 de enero", "municipio",
              "INE (diccionario de códigos)", True, "Correspondencia nombre->código por emparejamiento de texto")

    # Control: total municipal (68065) frente a total nacional publicado por la misma tabla.
    tot_mun = {}
    nacional = {}
    for s in series["68065"]:
        if s["Nombre"].startswith("Total Nacional. Total. Total"):
            nacional = {v["Anyo"]: v["Valor"] for v in s["Data"]}
        elif s["Nombre"].endswith(". Total. Total. Todas las edades. Dato base.") or \
                re.search(r"\. Total\. Total\. Todas las edades\. Dato base\.\s*$", s["Nombre"]):
            for v in s["Data"]:
                tot_mun[v["Anyo"]] = tot_mun.get(v["Anyo"], 0) + (v["Valor"] or 0)
    print(f"filas={len(filas)} municipios_mapeados={len(nombres) - len(sin_match) - len(ambiguos)} "
          f"no_encontrados={len(sin_match)} ambiguos={len(ambiguos)}")
    for a in sorted(EDICIONES):
        print(f"control {a}: total nacional INE (68065, Total Nacional)={nacional.get(a)} "
              f"suma municipios={tot_mun.get(a)}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
