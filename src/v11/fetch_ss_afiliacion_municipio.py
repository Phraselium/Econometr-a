"""V11-DATOS (bloque 4, punto 15): Seguridad Social, afiliados (último día del mes) por MUNICIPIO, régimen, CNAE 2D y
sexo: https://www.seg-social.es/descargas/STAT/MUNCNAE<MMAA>.xlsx (página «Información desagregada a nivel
Municipal», que carga los enlaces con JavaScript; la URL de los ficheros es estable). El código de municipio del
fichero es INE (provincia × 1000 + municipio → 5 dígitos). Celdas con menos de 5 afiliados: «<5» (secreto
estadístico); aquí se suman solo los valores numéricos y se cuenta el número de celdas suprimidas (el total
publicado no se puede reconstruir exactamente: cota inferior = suma; cota superior = suma + 4 × celdas «<5»).

Se prueba cada mes desde 2009-01 con las variantes de nombre (.xlsx/.xls, sufijo R o _R de revisado); los meses
sin fichero quedan en el manifiesto. Algunos meses vienen repartidos en varias hojas o sin la columna CNAE (las columnas CNAE quedan vacías ese mes);
las columnas se detectan por nombre; en 2025-05 el último dígito del código de municipio
aparece desplazado al inicio del nombre y se reconstruye. Cada mes agregado se guarda en tmp/meses/ (caché local) para poder reanudar.
Por espacio en disco, cada xlsx (~25 MB) se descarga, se agrega y se borra; su
sha256 queda en el manifiesto y `make datos_v11` lo regenera.
Salida: afiliacion_municipio_mensual.csv.gz (mes, cod_municipio, grupo de régimen [general, autonomos, otros],
afiliados_suma_numerica, celdas_menor5, construccion [CNAE 41-43], hosteleria [55-56], inmobiliarias [68]).
Meses de 2026-07 en adelante: posterior_prereg = True (no se usan en cálculos).
Licencia: Seguridad Social, reutilización con cita (Ley 37/2007).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, marcar_posterior_prereg, registrar, sha256, verificar_manifiesto  # noqa: E402

FUENTE = "ss_afiliacion_municipio"
DIR = RAW11 / FUENTE
BASE = "https://www.seg-social.es/descargas/STAT/"
LIC = "Seguridad Social: reutilización con cita (Ley 37/2007)"
FIN = pd.Timestamp("2026-09-01")


def grupo(cod: pd.Series) -> np.ndarray:
    c = pd.to_numeric(cod, errors="coerce")
    return np.where(c == 111, "general", np.where(c.isin([521, 522, 523, 524]), "autonomos", "otros"))


def bajar(m: pd.Timestamp) -> tuple[Path, str] | None:
    mmyy = f"{m.month:02d}{m.year % 100:02d}"
    for nombre in (f"MUNCNAE{mmyy}.xlsx", f"MUNCNAE{mmyy}R.xlsx", f"MUNCNAE{mmyy}_R.xlsx", f"MUNCNAE{mmyy}.xls"):
        try:
            r = requests.get(BASE + nombre, headers=CABECERAS, timeout=300)
        except Exception:  # noqa: BLE001
            continue
        if r.status_code == 200 and len(r.content) > 100_000:
            p = DIR / "tmp" / nombre
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(r.content)
            return p, BASE + nombre
    return None


def _col(cols, *claves, excluir=()):
    for c in cols:
        if all(k in c for k in claves) and not any(e in c for e in excluir):
            return c
    return None


def agregar(p: Path, m: pd.Timestamp) -> pd.DataFrame:
    hojas = pd.read_excel(p, dtype=str, sheet_name=None)   # algunos meses vienen repartidos en varias hojas
    partes = []
    for h in hojas.values():
        h.columns = [str(c).strip().upper() for c in h.columns]
        if _col(h.columns, "MUNICIPIO") and _col(h.columns, "AFILIADOS"):
            partes.append(h)
    d = pd.concat(partes, ignore_index=True)
    cm = _col(d.columns, "COD", "MUNICIPIO")
    cr = _col(d.columns, "COD", "REGIMEN") or _col(d.columns, "COD", "RÉGIMEN")
    cc = _col(d.columns, "COD", "CNAE")
    cod = pd.to_numeric(d[cm], errors="coerce").astype("Int64").astype(str)
    nombre = d[_col(d.columns, "MUNICIPIO", excluir=("COD",))].astype(str)
    desplazado = nombre.str.match(r"^\d")   # p. ej. 2025-05: último dígito del código pegado al inicio del nombre
    cod = np.where(desplazado, cod + nombre.str[0], cod)
    d["cod_municipio"] = pd.Series(cod, index=d.index).str.zfill(5)
    v = pd.to_numeric(d[_col(d.columns, "AFILIADOS")], errors="coerce")
    d["num"], d["sup"] = v.fillna(0), v.isna().astype(int)
    d["regimen"] = grupo(d[cr])
    cnae = pd.to_numeric(d[cc], errors="coerce") if cc else pd.Series(np.nan, index=d.index)
    for col, rango in (("construccion", (41, 43)), ("hosteleria", (55, 56)), ("inmobiliarias", (68, 68))):
        d[col] = np.where(cnae.between(*rango), d.num, np.nan if cc is None else 0)
    g = d.groupby(["cod_municipio", "regimen"]).agg(afiliados_suma_numerica=("num", "sum"), celdas_menor5=("sup", "sum"),
                                                     construccion=("construccion", "sum"), hosteleria=("hosteleria", "sum"),
                                                     inmobiliarias=("inmobiliarias", "sum")).reset_index()
    if cc is None:
        g[["construccion", "hosteleria", "inmobiliarias"]] = np.nan
    g.insert(0, "mes", m.strftime("%Y-%m"))
    return g


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    partes, faltan = [], []
    for m in pd.date_range("2009-01-01", FIN, freq="MS"):
        cache = DIR / "tmp" / "meses" / f"{m:%Y-%m}.csv.gz"
        if cache.exists():   # agregado ya hecho en una ejecución anterior (caché local, no versionada)
            partes.append(pd.read_csv(cache, dtype={"cod_municipio": str, "mes": str}))
            continue
        b = bajar(m)
        if b is None:
            faltan.append(m.strftime("%Y-%m"))
            continue
        p, url = b
        g = agregar(p, m)
        cache.parent.mkdir(parents=True, exist_ok=True)
        g.to_csv(cache, index=False, compression=GZ_PANDAS)
        partes.append(g)
        registrar(FUENTE, p, url, edicion=f"Afiliados por municipio {m:%Y-%m}", periodo=m.strftime("%Y-%m"), nivel_territorial="microdatos agregados (municipio × régimen × CNAE 2D × sexo)",
                  licencia=LIC, redistribuible=True, notas=f"no versionado y borrado tras agregar (espacio); sha256 en manifiesto; filas={len(g)}")
        p.unlink()
        print(m.strftime("%Y-%m"), len(g), int(g.afiliados_suma_numerica.sum()))
    A = pd.concat(partes, ignore_index=True).sort_values(["mes", "cod_municipio", "regimen"])
    A = marcar_posterior_prereg(A, "mes")
    r = DIR / "afiliacion_municipio_mensual.csv.gz"
    A.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, BASE + "MUNCNAE<MMAA>.xlsx", edicion="Seguridad Social, afiliados último día del mes por municipio",
              periodo=f"{A.mes.min()}–{A.mes.max()}", nivel_territorial="municipio (código INE)", licencia=LIC, redistribuible=True,
              notas=f"suma de celdas numéricas + nº de celdas <5 por municipio × régimen; meses sin fichero: {faltan}; "
                    f"filas posterior_prereg={int(A.posterior_prereg.sum())}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
