"""V9-DATOS: registro de viviendas de uso turístico (GVA, dadesobertes.gva.es, CC BY 4.0).

Descarga los cortes disponibles (histórico y último periodo 2025 del conjunto dades-turisme-habitatges-comunitat-valenciana-2025,
y el conjunto diario tur-gestur-vt), los guarda comprimidos y construye el panel de stock por municipio (INE 5 dígitos) y CP.
Sin estimaciones: solo conteos.
"""
from __future__ import annotations

import csv
import gzip
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAW9, RAIZ, descargar, registrar, sha256  # noqa: E402

FUENTE = "gva_vut"
DIR = RAW9 / FUENTE
CORTES = DIR / "cortes"
LICENCIA = "CC BY 4.0 (catálogo CKAN: cc-by)"
# (nombre local, URL, corte, descripción)
FICHEROS = [
    ("vut_historico_2025-01-26.csv", "https://dadesobertes.gva.es/dataset/8a1c4fa3-4696-4b3b-8a1a-6bff038abf0c/resource/9f3d18dc-3150-4075-8dd4-4f96d5dd1868/download/listaviviendas_19600101.csv",
     "2025-01-26", "histórico con altas y bajas (recurso 'listaviviendas_19600101', corte según el conjunto)"),
    ("vut_ultimo_periodo_2025-01-26.csv", "https://dadesobertes.gva.es/dataset/8a1c4fa3-4696-4b3b-8a1a-6bff038abf0c/resource/2c1e8aa4-5238-47c4-9404-f574ee1269a4/download/listaviviendas_20250126.csv",
     "2025-01-26", "último periodo, solo ALTA en el corte"),
    ("vut_actual_2026-10-14.csv", "https://dadesobertes.gva.es/dataset/758f8f8e-c5af-4622-b268-a6c591710a51/resource/b1bdc28e-9813-422a-ab7a-63c21290493d/download/lista-de-viviendas-turisticas.csv",
     "2026-10-14", "conjunto diario tur-gestur-vt (formato reducido: sin estado ni baja)"),
]


def _leer(ruta: Path) -> pd.DataFrame:
    df = pd.read_csv(ruta, sep=";", encoding="latin-1", dtype=str, keep_default_na=False)
    df.columns = [c.strip() for c in df.columns]
    if "Cod. Municipio" in df.columns:   # formato rico (histórico y último periodo)
        df = pd.DataFrame({"ine5": df["Cod. Provincia"].str.zfill(2) + df["Cod. Municipio"].str.zfill(3),
                           "municipio": df["Municipio"], "cp": df["C.P."].str.zfill(5), "direccion": df["Dirección"],
                           "signatura": df["Signatura"], "estado": df["Estado"],
                           "alta": pd.to_datetime(df["Fecha alta"], format="%d/%m/%Y", errors="coerce"),
                           "baja": pd.to_datetime(df["Fecha baja"], format="%d/%m/%Y", errors="coerce")})
    else:                                  # formato reducido (conjunto diario)
        df = pd.DataFrame({"ine5": df["cod_provincia"].str.zfill(2) + df["cod_municipio"].str.zfill(3),
                           "municipio": df["municipio"], "cp": df["cp"].str.zfill(5), "direccion": df["direccion"],
                           "signatura": df["signatura"], "estado": "ALTA",
                           "alta": pd.to_datetime(df["fecha_alta"], format="%d/%m/%Y", errors="coerce"), "baja": pd.NaT})
    return df


def _panel(df: pd.DataFrame, corte: str, clave: str) -> pd.DataFrame:
    vivas = df[df["estado"].str.upper().eq("ALTA")]
    return vivas.groupby(clave).size().rename("stock").reset_index().assign(tipo="corte", fecha=corte)


def _mensual(df: pd.DataFrame, clave: str, inicio="2015-01", fin="2025-01") -> pd.DataFrame:
    """Stock mensual reconstruido: vivas en fin de mes con alta <= fin de mes y (sin baja o baja > fin de mes)."""
    filas = []
    for m in pd.period_range(inicio, fin, freq="M"):
        fm = m.to_timestamp(how="end").normalize()
        act = df["alta"].le(fm) & (df["baja"].isna() | df["baja"].gt(fm))
        s = df.loc[act].groupby(clave).size().rename("stock").reset_index()
        s["tipo"], s["fecha"] = "mensual_reconstruido", str(m)
        filas.append(s)
    return pd.concat(filas, ignore_index=True)


def main(verificar: bool = False) -> int:
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            print("falta _manifest.csv"); return 1
        for r in csv.DictReader(open(man, encoding="utf-8")):
            p = RAIZ / r["fichero"]
            if not p.exists() or sha256(p) != r["sha256"]:
                print("fallo de verificación:", r["fichero"]); return 1
        print("verificación OK"); return 0

    tmp = DIR / "_tmp"
    CORTES.mkdir(parents=True, exist_ok=True)
    tmp.mkdir(parents=True, exist_ok=True)
    frames = {}
    for nombre, url, corte, desc in FICHEROS:
        bruto = descargar(url, tmp / nombre)
        gz = CORTES / (nombre + ".gz")
        with open(bruto, "rb") as f, gzip.open(gz, "wb") as g:
            shutil.copyfileobj(f, g)
        registrar(FUENTE, gz, url, edicion=corte, periodo=corte, nivel_territorial="registro individual",
                  licencia=LICENCIA, redistribuible=True, notas=desc)
        frames[nombre] = _leer(bruto)
    shutil.rmtree(tmp, ignore_errors=True)

    # Panel de cortes (municipio y CP) + mensual reconstruido desde el histórico con fechas de alta/baja.
    dh = frames["vut_historico_2025-01-26.csv"]
    partes_m = [_panel(frames["vut_historico_2025-01-26.csv"], "2025-01-26", "ine5"),
                _panel(frames["vut_actual_2026-10-14.csv"], "2026-10-14", "ine5")]
    partes_c = [_panel(frames["vut_historico_2025-01-26.csv"], "2025-01-26", "cp"),
                _panel(frames["vut_actual_2026-10-14.csv"], "2026-10-14", "cp")]
    mens_m = _mensual(dh, "ine5")
    mens_c = _mensual(dh, "cp")
    pm = pd.concat(partes_m + [mens_m], ignore_index=True)[["ine5", "tipo", "fecha", "stock"]]
    pc = pd.concat(partes_c + [mens_c], ignore_index=True)[["cp", "tipo", "fecha", "stock"]]
    pm.sort_values(["ine5", "fecha", "tipo"]).to_csv(DIR / "gva_vut_panel_municipio.csv", index=False)
    pc.sort_values(["cp", "fecha", "tipo"]).to_csv(DIR / "gva_vut_panel_cp.csv", index=False)
    for nombre in ["gva_vut_panel_municipio.csv", "gva_vut_panel_cp.csv"]:
        registrar(FUENTE, DIR / nombre, "derivado de cortes de cortes/", edicion="v9", periodo="2015-01/2026-10",
                  nivel_territorial="municipio (INE 5)" if "municipio" in nombre else "código postal",
                  licencia=LICENCIA, redistribuible=True, notas="derivado; ver LEEME.md")
    for nombre, df in frames.items():
        print(nombre, "filas", len(df), "ALTA", int(df["estado"].str.upper().eq("ALTA").sum()), "municipios", df["ine5"].nunique())
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
