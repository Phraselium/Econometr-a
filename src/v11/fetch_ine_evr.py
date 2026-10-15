"""V11-DATOS (bloque 1, punto 1): INE, Estadística de Variaciones Residenciales (EVR), microdatos anuales 1988-2021.

Fichero por año: https://www.ine.es/ftp/microdatos/varires/datos_<año>.zip (CSV separado por tabulador; diseño de
registro en disreg_vr.xlsx). Cada registro es una variación residencial con municipio de baja (origen) y de alta
(destino), mes y año de variación, sexo, edad, país de nacionalidad (CNAC) y provincia/municipio o país de nacimiento.
El INE blanquea el código de los municipios de menos de 10.000 habitantes: aquí se codifican como PP999 («resto de la
provincia PP»). Provincia 66 = extranjero (el código de municipio es entonces el país).

Salidas (data/raw/v11/ine_evr/):
- original/datos_<año>.zip                microdatos (no se versionan: `make datos_v11`)
- od_municipios_<año>.parquet             flujos origen-destino internos (baja → alta), por nacionalidad (ES/EXT),
                                          sexo y grupo de edad (0-15, 16-34, 35-64, 65+); no se versionan (tamaño)
- saldos_internos_municipio.csv.gz        altas, bajas y saldo interno (solo movimientos entre municipios de España)
                                          por municipio × año × nacionalidad (ES/EXT) × grupo de edad; se versiona
- flujos_exterior_municipio.csv.gz        altas desde el extranjero y bajas al extranjero por municipio × año × país de
                                          nacionalidad (CNAC); se versiona
Nacionalidad: CNAC = 108 es España (Anexo «Lista países» del diseño de registro). Licencia INE: reutilización con cita.
Los años anteriores a 2002 se descargan igual (inicio real de la serie: 1988).
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

FUENTE = "ine_evr"
DIR = RAW11 / FUENTE
URL = "https://www.ine.es/ftp/microdatos/varires/datos_{a}.zip"
ANIOS = range(1988, 2022)
LIC = "INE: reutilización con cita (Ley 37/2007); microdatos públicos"
ESPANA = "108"
EDAD = [-1, 15, 34, 64, 200]
EDAD_LAB = ["0-15", "16-34", "35-64", "65+"]


def cod(prov: pd.Series, mun: pd.Series) -> pd.Series:
    p = prov.astype(str).str.strip().str.zfill(2)
    m = mun.astype(str).str.strip()
    return np.where(p == "66", "66" + m.str.zfill(3), np.where(m == "", p + "999", p + m.str.zfill(3)))


# ancho fijo (diseño de registro disreg_vr.xlsx, igual en todos los años): posiciones 0-indexadas [inicio, fin)
ANCHO = {"SEXO": (0, 1), "EDAD": (6, 9), "CNAC": (15, 18), "PROVALTA": (18, 20), "MUNIALTA": (20, 23),
         "ANOVAR": (25, 29), "PROVBAJA": (29, 31), "MUNIBAJA": (31, 34)}


def leer(zp: Path) -> pd.DataFrame:
    """CSV con tabulador (años recientes) o fichero de ancho fijo de 37 posiciones (años antiguos, sin CSV)."""
    with zipfile.ZipFile(zp) as z:
        csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if csvs:
            with z.open(csvs[0]) as f:
                d = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"), sep="\t", dtype=str, keep_default_na=False,
                                usecols=["SEXO", "EDAD", "CNAC", "PROVALTA", "MUNIALTA", "ANOVAR", "PROVBAJA", "MUNIBAJA"])
        else:
            nombre = next(n for n in z.namelist() if not n.endswith("/") and "leeme" not in n.lower() and not n.lower().endswith((".xlsx", ".xls", ".doc", ".pdf")))
            with z.open(nombre) as f:
                d = pd.read_fwf(io.TextIOWrapper(f, encoding="latin-1"), colspecs=list(ANCHO.values()), names=list(ANCHO),
                                dtype=str, header=None, keep_default_na=False)
    d["origen"] = cod(d.PROVBAJA, d.MUNIBAJA)
    d["destino"] = cod(d.PROVALTA, d.MUNIALTA)
    d["nac"] = np.where(d.CNAC.str.strip() == ESPANA, "ES", "EXT")
    d["edad_g"] = pd.cut(pd.to_numeric(d.EDAD, errors="coerce"), EDAD, labels=EDAD_LAB).astype(str)
    d["anio"] = pd.to_numeric(d.ANOVAR, errors="coerce").astype("Int64")
    d["sexo"] = d.SEXO.map({"1": "H", "6": "M"}).fillna("?")
    return d


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    saldos, exter = [], []
    for a in ANIOS:
        try:
            zp = descargar(URL.format(a=a), DIR / "original" / f"datos_{a}.zip", timeout=900)
        except RuntimeError as e:
            print("FALLO", a, e)
            continue
        d = leer(zp)
        interno = d[~d.origen.str.startswith("66") & ~d.destino.str.startswith("66")]
        od = interno.groupby(["origen", "destino", "nac", "sexo", "edad_g"]).size().rename("n").reset_index()
        od.insert(0, "anio_fichero", a)
        od.to_parquet(DIR / f"od_municipios_{a}.parquet", index=False, compression="zstd")
        alt = interno.groupby(["destino", "nac", "edad_g"]).size().rename("altas")
        baj = interno.groupby(["origen", "nac", "edad_g"]).size().rename("bajas")
        alt.index.names = baj.index.names = ["cod_municipio", "nac", "edad_g"]
        s = pd.concat([alt, baj], axis=1).fillna(0).astype(int).reset_index()
        s["saldo"] = s.altas - s.bajas
        s.insert(0, "anio", a)
        saldos.append(s)
        ex_in = d[d.origen.str.startswith("66") & ~d.destino.str.startswith("66")].groupby(["destino", "CNAC"]).size().rename("altas_desde_extranjero")
        ex_out = d[d.destino.str.startswith("66") & ~d.origen.str.startswith("66")].groupby(["origen", "CNAC"]).size().rename("bajas_al_extranjero")
        ex_in.index.names = ex_out.index.names = ["cod_municipio", "cnac"]
        e = pd.concat([ex_in, ex_out], axis=1).fillna(0).astype(int).reset_index()
        e.insert(0, "anio", a)
        exter.append(e)
        print(a, len(d), "OD", len(od))
    S = pd.concat(saldos, ignore_index=True).sort_values(["anio", "cod_municipio", "nac", "edad_g"])
    E = pd.concat(exter, ignore_index=True).sort_values(["anio", "cod_municipio", "cnac"])
    r1 = DIR / "saldos_internos_municipio.csv.gz"
    r2 = DIR / "flujos_exterior_municipio.csv.gz"
    S.to_csv(r1, index=False, compression=GZ_PANDAS)
    E.to_csv(r2, index=False, compression=GZ_PANDAS)
    per = f"{S.anio.min()}-{S.anio.max()}"
    registrar(FUENTE, r1, URL.format(a="<año>"), edicion="EVR microdatos 1988-2021 (ftp INE)", periodo=per,
              nivel_territorial="municipio ≥10.000 hab. (PP999 = resto de provincia)", licencia=LIC, redistribuible=True,
              notas="altas, bajas y saldo de movimientos entre municipios de España; nac ES/EXT; edad en 4 grupos")
    registrar(FUENTE, r2, URL.format(a="<año>"), edicion="EVR microdatos 1988-2021", periodo=per,
              nivel_territorial="municipio ≥10.000 hab. (PP999 = resto de provincia)", licencia=LIC, redistribuible=True,
              notas="altas desde el extranjero y bajas al extranjero por país de nacionalidad (CNAC; 108 = España)")
    for a in ANIOS:
        p = DIR / f"od_municipios_{a}.parquet"
        if p.exists():
            registrar(FUENTE, p, URL.format(a=a), edicion=f"EVR {a} (agregado propio)", periodo=str(a),
                      nivel_territorial="municipio × municipio", licencia=LIC, redistribuible=True,
                      notas="no versionado (tamaño): se regenera con make datos_v11")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
