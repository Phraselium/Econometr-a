"""V9-DATOS-COMPLETO (bloque 1, punto 1): turismo en Cataluña con fechas.

1. IDESCAT, «Estadística d'establiments turístics» (turall) por municipio y año: habitatges d'ús turístic (HUT, n=16722),
   apartaments turístics (16721), establiments hotelers (6033), càmpings (6034) y turisme rural (6037). Stock a 31 de
   diciembre de cada año desde el primero disponible. El código IDESCAT de 6 dígitos = código INE de municipio (5) + dígito
   de control: el cruce es por código. Licencia: IDESCAT, reutilización con cita (aviso legal) → se versiona.
2. Registre de Turisme de Catalunya (Socrata t2h3-cgys): corte actual, sin fecha de alta y con datos personales de
   titulares. Solo se guarda un agregado por municipio, tipo y modalidad. «See Terms of Use» (como Incasòl) → no se
   versiona (make datos_terceros).
3. Impost sobre les estades en establiments turístics (IEET) por municipio y tipología (Socrata q4sr-68c3), semestral
   2017S1-último: liquidaciones e importe; HT = habitatges d'ús turístic. «See Terms of Use» → no se versiona.
"""
from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import CABECERAS, GZ_PANDAS, RAIZ, RAW9, registrar, sha256  # noqa: E402

FUENTE = "cat_turisme"
DIR = RAW9 / FUENTE
IDESCAT = "https://www.idescat.cat/pub/?id=turall&n={n}&geo=mun&t={t}00&lang=es&f=ssv"
IDESCAT_SERIE = "https://www.idescat.cat/pub/?id=turall&n={n}&geo=mun&lang=es"
TABLAS = {16722: "habitatges_us_turistic", 16721: "apartaments_turistics", 6033: "establiments_hotelers",
          6034: "campings", 6037: "turisme_rural"}
SOCRATA = "https://analisi.transparenciacatalunya.cat/resource/{id}.csv"
LIC_IDESCAT = "IDESCAT: reutilización con cita de la fuente (aviso legal)"
LIC_GENCAT = "Generalitat de Catalunya, dades obertes: «See Terms of Use» (no CC BY explícita; como Incasòl)"


def anios_disponibles(n: int) -> list[int]:
    html = requests.get(IDESCAT_SERIE.format(n=n), headers=CABECERAS, timeout=120).text
    return sorted({int(x[:4]) for x in re.findall(r'value="(\d{4})00" name="t"', html)})


def idescat() -> pd.DataFrame:
    partes = []
    for n, nombre in TABLAS.items():
        for t in anios_disponibles(n):
            txt = requests.get(IDESCAT.format(n=n, t=t), headers=CABECERAS, timeout=120).content.decode("utf-8-sig", "replace")
            lineas = txt.splitlines()
            i = next(k for k, l in enumerate(lineas) if l.startswith("Codi;"))
            d = pd.read_csv(io.StringIO("\n".join(lineas[i:])), sep=";", dtype=str)
            d = d[d.Codi.str.fullmatch(r"\d{6}", na=False)]
            cols = [c for c in d.columns if c not in ("Codi", "Nom")]
            largo = d.melt(id_vars=["Codi", "Nom"], value_vars=cols, var_name="medida", value_name="valor")
            largo["valor"] = pd.to_numeric(largo.valor.str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
                                           errors="coerce")
            largo["anio"], largo["tipo"] = t, nombre
            partes.append(largo)
    d = pd.concat(partes, ignore_index=True)
    d["cod_ine"] = d.Codi.str[:5]
    return d.rename(columns={"Codi": "codi_idescat", "Nom": "nombre"})[
        ["anio", "tipo", "cod_ine", "codi_idescat", "nombre", "medida", "valor"]]


def socrata_todo(ident: str, select: str | None = None, group: str | None = None) -> pd.DataFrame:
    params = {"$limit": 500000}
    if select:
        params["$select"] = select
    if group:
        params["$group"] = group
    r = requests.get(SOCRATA.format(id=ident), params=params, headers=CABECERAS, timeout=600)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text), dtype=str)


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            print("falta _manifest.csv"); return 1
        with open(man, encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                ruta = RAIZ / fila["fichero"]
                if fila["redistribuible"] == "no" and not ruta.exists():
                    continue   # no versionado: lo trae make datos_terceros
                if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK cat_turisme"); return 0
    d = idescat()
    ruta = DIR / "idescat_allotjaments_municipi.csv.gz"
    d.to_csv(ruta, index=False, compression=GZ_PANDAS)
    # cuadre: suma de municipios = total de Cataluña publicado (HUT)
    registrar(FUENTE, ruta, IDESCAT_SERIE.format(n="<n>"), edicion="IDESCAT turall (consulta 2026-10-15)",
              periodo=f"{d.anio.min()}-{d.anio.max()}", nivel_territorial="municipio (código INE desde el código IDESCAT)",
              licencia=LIC_IDESCAT, redistribuible=True,
              notas="; ".join(f"{t}: {g.anio.min()}-{g.anio.max()}" for t, g in d.groupby("tipo")))
    reg = socrata_todo("t2h3-cgys", "codi_municipi_idescat,tipus_establiment,modalitat,count(*) AS n,"
                       "sum(total_places) AS places", "codi_municipi_idescat,tipus_establiment,modalitat")
    reg["cod_ine"] = reg.codi_municipi_idescat.str.zfill(6).str[:5]
    ruta = DIR / "registre_turisme_agregat_municipi.csv.gz"
    reg.to_csv(ruta, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, ruta, SOCRATA.format(id="t2h3-cgys"), edicion="corte actual (sin fechas de alta)",
              periodo="corte 2026-10", nivel_territorial="municipio", licencia=LIC_GENCAT, redistribuible=False,
              notas="agregado por municipio, tipo y modalidad; el fichero completo contiene datos personales (no se guarda)")
    ieet = socrata_todo("q4sr-68c3")
    ruta = DIR / "ieet_municipi.csv.gz"
    ieet.to_csv(ruta, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, ruta, SOCRATA.format(id="q4sr-68c3"), edicion="IEET por municipio y tipología",
              periodo=f"{ieet.iloc[:, 0].min()}-{ieet.iloc[:, 0].max()}", nivel_territorial="municipio (nombre: requiere cruce)",
              licencia=LIC_GENCAT, redistribuible=False,
              notas="SIN código de municipio: solo se usa tras una tabla de correspondencia nombre→INE documentada; HT = HUT")
    print("idescat", len(d), "registre", len(reg), "ieet", len(ieet))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
