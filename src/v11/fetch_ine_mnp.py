"""V11-DATOS (bloque 1, punto 3): INE, Movimiento Natural de la Población (MNP), nacimientos y defunciones por
municipio de RESIDENCIA y año (saldo vegetativo municipal), desde los microdatos anonimizados (ftp INE).

Las tablas de INEbase (operaciones MNPN y MNPD) solo llegan a provincia; el nivel municipal sale de los microdatos,
cuyo diseño de registro cambia por periodos (ficheros de diseño en la misma carpeta del ftp):
- nacimientos 1980-1995 («disreg nac 80-95»): residencia de la madre en posiciones 23-27; sin nacionalidad;
- nacimientos 1996-2006 («disreg nac 96»): municipio 27-29 y provincia 30-31 de residencia de la madre;
  nacionalidad de la madre 80-82;
- nacimientos 2007- («disreg_nacimientos», dr_MNPnacim_Desde2016.xlsx): PROREM 45-46, MUNREM 47-49, PAISNACM 33-35;
- defunciones 1980-1998 («Disreg80-98»): MUNIRES 15-17, PROVRES 18-19; sin nacionalidad;
- defunciones 1999-2008 («Rdefa994»): MUNIRES 21-23, PROVRES 24-25, NACION 16-18;
- defunciones 2009- («disreg_defun15», dr_MNPdefun_Desde2016.xlsx): CPRORE 33-34, CMUNRE 35-37, PAISNAC 20-22.
1975-1979 no se incorpora (otro diseño, sin cambio sustantivo para el periodo de análisis; documentado).
El municipio se blanquea si tiene < 10.000 hab. → PP999. Residencia en el extranjero o provincia en blanco → «EXTR».
El año es el del fichero (año de inscripción estadística del suceso). Nacionalidad: ES (108), EXT (otra), NC (sin dato o
periodo sin la variable). En nacimientos se cuenta cada registro (nacido) y, por separado, los nacidos vivos cuando el
fichero trae el indicador.

Salidas (data/raw/v11/ine_mnp/): original/ (zips, no versionados) y mnp_municipio.csv.gz
(anio, cod_municipio, nac, nacimientos, nacidos_vivos, defunciones, saldo_vegetativo). Licencia INE: reutilización con cita.
"""
from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import GZ_PANDAS, RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "ine_mnp"
DIR = RAW11 / FUENTE
BASE = "https://www.ine.es/ftp/microdatos/"
LIC = "INE: reutilización con cita (Ley 37/2007); microdatos públicos"
ANIOS = range(1980, 2025)


def url_nac(a: int) -> str:
    yy = f"{a % 100:02d}"
    if a <= 2006:
        return BASE + f"mnp_nacim/datos%20nacimientos%20{yy}.zip"
    if a <= 2010:
        return BASE + f"mnp_nacim/datos%20nacimientos{yy}.zip"
    return BASE + f"mnp_nacim/datos_nacimientos{yy}.zip"


def url_def(a: int) -> str:
    if a <= 2008:
        return BASE + f"mnp_defun/datos%20defuncio{a % 100:02d}.zip"
    if a <= 2015:
        return BASE + f"mnp_defun/sin/datos_{a}.zip"
    return BASE + f"mnp_defun/datos_{a}.zip"


# posiciones 1-indexadas inclusivas del diseño → [inicio-1, fin)
def _p(i: int, n: int) -> tuple[int, int]:
    return (i - 1, i - 1 + n)


def diseno(tipo: str, a: int) -> dict[str, tuple[int, int]]:
    if tipo == "nac":
        if a <= 1995:
            return {"MUN": _p(23, 3), "PROV": _p(26, 2), "VIVO": _p(46, 1)}
        if a <= 2006:
            return {"MUN": _p(27, 3), "PROV": _p(30, 2), "PAIS": _p(80, 3), "VIVO": _p(70, 1)}
        return {"PROV": _p(45, 2), "MUN": _p(47, 3), "PAIS": _p(33, 3), "VIVO": _p(173, 1)}
    if a <= 1998:
        return {"MUN": _p(15, 3), "PROV": _p(18, 2)}
    if a <= 2008:
        return {"PAIS": _p(16, 3), "MUN": _p(21, 3), "PROV": _p(24, 2)}
    return {"PAIS": _p(20, 3), "PROV": _p(33, 2), "MUN": _p(35, 3)}


def leer(zp: Path, tipo: str, a: int) -> pd.DataFrame:
    dz = diseno(tipo, a)
    with zipfile.ZipFile(zp) as z:
        nombres = [n for n in z.namelist() if not n.endswith("/") and not n.lower().endswith((".xls", ".xlsx", ".doc", ".pdf", ".txt.bak"))
                   and "leeme" not in n.lower() and "readme" not in n.lower()]
        csvs = [n for n in nombres if n.lower().endswith((".csv", ".tab"))]
        if csvs:  # desde 2016: CSV/<…>.tab con tabulador y cabecera; se toman las variables por nombre
            nom = {"nac": {"PROV": "PROREM", "MUN": "MUNREM", "PAIS": "PAISNACM", "VIVO": "NACVN"},
                   "def": {"PROV": "CPRORE", "MUN": "CMUNRE", "PAIS": "PAISNAC"}}[tipo]
            with z.open(csvs[0]) as f:
                d = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"), sep="\t", dtype=str, keep_default_na=False,
                                usecols=list(nom.values()))
            d = d.rename(columns={v: k for k, v in nom.items()})
        else:
            nombre = max(nombres, key=lambda n: z.getinfo(n).file_size)
            with z.open(nombre) as f:
                d = pd.read_fwf(io.TextIOWrapper(f, encoding="latin-1"), colspecs=list(dz.values()), names=list(dz),
                                dtype=str, header=None, keep_default_na=False)
    p = d.PROV.astype(str).str.strip()
    m = d.MUN.astype(str).str.strip()
    valida = p.str.fullmatch(r"\d{1,2}") & (pd.to_numeric(p, errors="coerce").between(1, 52))
    p2 = p.str.zfill(2)
    d["cod_municipio"] = np.where(~valida, "EXTR", np.where((m == "") | (m == "000") | (m == "999"), p2 + "999", p2 + m.str.zfill(3)))
    if "PAIS" in d:
        pais = d.PAIS.astype(str).str.strip()
        d["nac"] = np.where(pais == "108", "ES", np.where((pais == "") | (pais == "999") | (pais == "000"), "NC", "EXT"))
    else:
        d["nac"] = "NC"
    d["vivo"] = d.VIVO.astype(str).str.strip() == "1" if "VIVO" in d else False
    return d[["cod_municipio", "nac", "vivo"]]


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    partes, fallos = [], []
    for a in ANIOS:
        for tipo, url in (("nac", url_nac(a)), ("def", url_def(a))):
            try:
                zp = descargar(url, DIR / "original" / f"{tipo}_{a}.zip", timeout=900)
                d = leer(zp, tipo, a)
            except Exception as e:  # noqa: BLE001
                print("FALLO", tipo, a, e)
                fallos.append((tipo, a))
                continue
            g = d.groupby(["cod_municipio", "nac"]).agg(n=("vivo", "size"), vivos=("vivo", "sum")).reset_index()
            g["anio"], g["tipo"] = a, tipo
            partes.append(g)
            print(tipo, a, len(d), "vivos" if tipo == "nac" else "", int(d.vivo.sum()) if tipo == "nac" else "")
    D = pd.concat(partes, ignore_index=True)
    nac = D[D.tipo == "nac"].rename(columns={"n": "nacimientos", "vivos": "nacidos_vivos"}).drop(columns="tipo")
    de = D[D.tipo == "def"].rename(columns={"n": "defunciones"}).drop(columns=["tipo", "vivos"])
    M = nac.merge(de, on=["anio", "cod_municipio", "nac"], how="outer").fillna(0)
    for c in ("nacimientos", "nacidos_vivos", "defunciones"):
        M[c] = M[c].astype(int)
    # periodos sin indicador de vivo (no hay periodo así hoy, pero se protege): nacidos_vivos = NA
    M["saldo_vegetativo"] = M.nacimientos - M.defunciones
    M = M[["anio", "cod_municipio", "nac", "nacimientos", "nacidos_vivos", "defunciones", "saldo_vegetativo"]]
    M = M.sort_values(["anio", "cod_municipio", "nac"])
    r = DIR / "mnp_municipio.csv.gz"
    M.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, BASE + "mnp_nacim/ y mnp_defun/", edicion="MNP microdatos anonimizados (ftp INE), nacimientos y defunciones",
              periodo=f"{M.anio.min()}-{M.anio.max()}", nivel_territorial="municipio de residencia ≥10.000 hab. (PP999 = resto; EXTR = residencia fuera de España)",
              licencia=LIC, redistribuible=True,
              notas="nac: ES/EXT/NC (nacimientos: nacionalidad de la madre desde 1996; defunciones: del fallecido desde 1999); "
                    f"saldo_vegetativo = nacimientos - defunciones; fallos={fallos}")
    for a in ANIOS:
        for tipo in ("nac", "def"):
            p = DIR / "original" / f"{tipo}_{a}.zip"
            if p.exists():
                registrar(FUENTE, p, url_nac(a) if tipo == "nac" else url_def(a), edicion=f"MNP {tipo} {a}", periodo=str(a),
                          nivel_territorial="microdatos", licencia=LIC, redistribuible=True,
                          notas="no versionado (tamaño): se regenera con make datos_v11")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
