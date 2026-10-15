"""V11-DATOS (bloque 2, punto 8): INE, Censo de Población y Viviendas 2021, viviendas y hogares.

1. Tablas predefinidas (tpx 59515-59545, 59546-59551 núcleos): viviendas por tipo (principal, no principal),
   régimen de tenencia, superficie, año de construcción y tamaño del hogar; hogares por tamaño, tipo y estructura;
   a nivel nacional, CCAA, provincia, tamaño de municipio y municipio (capitales y > 50.000 hab.; 59543 hogares
   por tamaño para todos los municipios). Ninguna tabla predefinida cruza con la nacionalidad.
2. Microdatos de PERSONAS (muestra del 10 % de los hogares; ftp INE cen21/CensoPersonas_2021.zip, 1,3 GB, no
   versionado): traen nacionalidad (PNACIO), país de nacimiento, año de llegada a España (VARANOE) y a la vivienda,
   régimen de tenencia, superficie, superficie por ocupante y tamaño y tipo de hogar. Con ellos se construye el cruce
   por nacionalidad que no se publica: hogares de la MUESTRA por municipio × nacionalidad de la primera persona del
   hogar (NORDEN = 01; el censo no identifica «persona de referencia», es una aproximación documentada) × tenencia ×
   superficie × superficie por ocupante × tamaño del hogar × periodo de llegada a España. Son recuentos muestrales sin
   elevar (factor uniforme ≈ 10; no se calcula ningún indicador).
   Municipio: CMUN 991/992/993 = municipios ≤ 2.000, 2.001-5.000 y 5.001-10.000 hab. de la provincia → PP991, PP992,
   PP993 (no son códigos INE de municipio; documentado).
3. Microdatos de VIVIENDAS (muestra; CensoViviendas_2021.zip, 142 MB, no versionado): viviendas de la muestra por
   municipio × tipo (principal, no principal, vacía según el diccionario) × tenencia × superficie × año de construcción.
Nivel sección censal: el INE no publica tablas de tenencia ni de hogares por sección más allá de los indicadores ya
incorporados en v3 (data/raw/v3/ine_v3_censo2021_seccion_indicadores.csv.gz); se documenta en cobertura.md.
Licencia INE: reutilización con cita.
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

FUENTE = "ine_censo2021"
DIR = RAW11 / FUENTE
URL_TPX = "https://www.ine.es/jaxi/files/tpx/es/csv_bdsc/{t}.csv"
URL_MD = "https://www.ine.es/ftp/microdatos/censopv/cen21/{f}"
LIC = "INE: reutilización con cita (Ley 37/2007)"
TPX = list(range(59515, 59552))
# posiciones (1-indexadas) del diseño dr_CensoPersonas_2021.xlsx y dr_CensoViviendas_2021.xlsx
P_PERS = {"CPRO": (1, 2), "CMUN": (3, 3), "NVIV": (6, 7), "NORDEN": (13, 2), "PNACIO": (25, 3), "PNACIM": (28, 3),
          "VARANOE": (53, 4), "TENEN_VIV": (122, 1), "SUP_VIV": (120, 2), "SUP_OCU_VIV": (123, 2), "TAM_HOG": (179, 1),
          "TIPO_HOG": (184, 2)}
P_VIV = {"CPRO": (8, 2), "CMUN": (10, 3), "TIPO_VIV": (13, 1), "TENEN_VIV": (14, 1), "SUPERF": (16, 4), "ANOCO": (25, 4),
         "TAM_HOG_5": (29, 1)}


def leer(zp: Path, pos: dict[str, tuple[int, int]]) -> pd.DataFrame:
    with zipfile.ZipFile(zp) as z:
        nombres = [n for n in z.namelist() if not n.endswith("/")]
        tab = [n for n in nombres if n.lower().endswith((".tab", ".csv"))]
        if tab:
            with z.open(tab[0]) as f:
                return pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"), sep="\t", dtype=str, keep_default_na=False,
                                   usecols=lambda c: c in pos)
        txt = max((n for n in nombres if n.lower().endswith(".txt") and "leeme" not in n.lower()), key=lambda n: z.getinfo(n).file_size)
        with z.open(txt) as f:
            return pd.read_fwf(io.TextIOWrapper(f, encoding="latin-1"), colspecs=[(i - 1, i - 1 + n) for i, n in pos.values()],
                               names=list(pos), dtype=str, header=None, keep_default_na=False)


def cod(d: pd.DataFrame) -> pd.Series:
    return d.CPRO.str.strip().str.zfill(2) + d.CMUN.str.strip().str.zfill(3)


def tablas() -> None:
    for t in TPX:
        try:
            r = descargar(URL_TPX.format(t=t), DIR / f"censo2021_tpx{t}.csv", timeout=300)
        except RuntimeError as e:
            print("FALLO tpx", t, e)
            continue
        cab = r.read_text(encoding="utf-8-sig").splitlines()[0]
        registrar(FUENTE, r, URL_TPX.format(t=t), edicion=f"Censo 2021, tabla tpx {t}", periodo="2021-01-01",
                  nivel_territorial=cab.split(";")[0][:80], licencia=LIC, redistribuible=True, notas=cab[:200])


def personas() -> None:
    zp = descargar(URL_MD.format(f="CensoPersonas_2021.zip"), DIR / "original" / "CensoPersonas_2021.zip", timeout=3600)
    d = leer(zp, P_PERS)
    d = d[(d.NORDEN.str.strip().astype(int) == 1) & (d.TAM_HOG.str.strip() != "9")].copy()
    d["cod_municipio"] = cod(d)
    d["nac_primera_persona"] = np.where(d.PNACIO.str.strip() == "108", "ES", "EXT")
    d["nacido_en_espana"] = np.where(d.PNACIM.str.strip() == "108", "si", "no")
    a = pd.to_numeric(d.VARANOE, errors="coerce")
    d["llegada_espana"] = pd.cut(a, [0, 1999, 2007, 2014, 2021], labels=["<2000", "2000-2007", "2008-2014", "2015-2021"]).astype(str)
    d.loc[d.nacido_en_espana == "si", "llegada_espana"] = "nacido_en_espana"
    g = (d.groupby(["cod_municipio", "nac_primera_persona", "nacido_en_espana", "llegada_espana", "TENEN_VIV", "SUP_VIV",
                    "SUP_OCU_VIV", "TAM_HOG", "TIPO_HOG"]).size().rename("hogares_muestra").reset_index()
         .rename(columns={"TENEN_VIV": "tenencia", "SUP_VIV": "superficie", "SUP_OCU_VIV": "superficie_por_ocupante",
                          "TAM_HOG": "tamano_hogar", "TIPO_HOG": "tipo_hogar"}))
    r = DIR / "hogares_muestra_municipio_nacionalidad.csv.gz"
    g.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, URL_MD.format(f="CensoPersonas_2021.zip"), edicion="Censo 2021, microdatos de personas (muestra 10 % de hogares)",
              periodo="2021-01-01", nivel_territorial="municipio ≥10.000 hab.; PP991/PP992/PP993 = tamaños de municipio menores",
              licencia=LIC, redistribuible=True,
              notas=f"recuentos MUESTRALES sin elevar de hogares en viviendas familiares (NORDEN=01 como persona de referencia "
                    f"aproximada); códigos según dr_CensoPersonas_2021.xlsx; hogares={int(g.hogares_muestra.sum())}")
    print("personas", len(d), len(g))


def viviendas() -> None:
    zp = descargar(URL_MD.format(f="CensoViviendas_2021.zip"), DIR / "original" / "CensoViviendas_2021.zip", timeout=1800)
    d = leer(zp, P_VIV)
    d["cod_municipio"] = cod(d)
    a = pd.to_numeric(d.ANOCO, errors="coerce")
    d["periodo_construccion"] = pd.cut(a, [0, 1940, 1960, 1980, 2000, 2010, 2021],
                                       labels=["<1941", "1941-1960", "1961-1980", "1981-2000", "2001-2010", "2011-2021"]).astype(str)
    s = pd.to_numeric(d.SUPERF, errors="coerce")
    d["superficie_m2"] = pd.cut(s, [0, 45, 60, 75, 90, 120, 180, 1e6], labels=["≤45", "46-60", "61-75", "76-90", "91-120", "121-180", ">180"]).astype(str)
    g = (d.groupby(["cod_municipio", "TIPO_VIV", "TENEN_VIV", "superficie_m2", "periodo_construccion", "TAM_HOG_5"]).size()
         .rename("viviendas_muestra").reset_index().rename(columns={"TIPO_VIV": "tipo_vivienda", "TENEN_VIV": "tenencia", "TAM_HOG_5": "tamano_hogar"}))
    r = DIR / "viviendas_muestra_municipio.csv.gz"
    g.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, URL_MD.format(f="CensoViviendas_2021.zip"), edicion="Censo 2021, microdatos de viviendas (muestra)",
              periodo="2021-01-01", nivel_territorial="municipio ≥10.000 hab.; PP991/PP992/PP993 = tamaños de municipio menores",
              licencia=LIC, redistribuible=True,
              notas=f"recuentos MUESTRALES sin elevar; códigos según dr_CensoViviendas_2021.xlsx; viviendas={int(g.viviendas_muestra.sum())}")
    print("viviendas", len(d), len(g))


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    tablas()
    viviendas()
    personas()
    for f in ("CensoPersonas_2021.zip", "CensoViviendas_2021.zip"):
        p = DIR / "original" / f
        if p.exists():
            registrar(FUENTE, p, URL_MD.format(f=f), edicion="Censo 2021, microdatos", periodo="2021-01-01", nivel_territorial="microdatos",
                      licencia=LIC, redistribuible=True, notas="no versionado (tamaño): se regenera con make datos_v11")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
