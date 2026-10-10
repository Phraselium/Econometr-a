"""M3: extracción y sondeos de red (la red solo se usa aquí; m3_run.py no la usa).

Uso:
  python src/v4/m3_fetch.py extract   # xls catastrales -> data/raw/v4/catastro_solares_municipios.csv.gz (sin red)
  python src/v4/m3_fetch.py red       # un único intento al SIU y sondeo del coste (PEM/m2) en el Boletín Online

Resultado de los sondeos (2026-10-10), ver docs/v4/fuentes_fallidas.md:
  - SIU: el proxy rechaza el host (connect_rejected), igual que en v3.
  - Boletín Online MIVAU (BoletinOnline2 y BoletinOnline): ninguna tabla de presupuesto de ejecución material
    ni de superficie de visados con presupuesto; la sección «Construcción de edificios (licencias municipales de
    obra)» (orden 10000000) trae número de licencias, superficie y viviendas, sin presupuesto.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
import warnings
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
XLS = RAW / "v2_orig" / "catastro"
OUT = RAW / "v4" / "catastro_solares_municipios.csv.gz"
VARS = ["UU_SOLAR", "V_CAT_SOLAR", "SUPERF_URB", "PARCELAS_URB", "UU_RES", "V_SUELO", "V_CONSTRUCCION"]
CODIGO = ("C_INE", "COD_INE_MUNI")


def extract() -> pd.DataFrame:
    warnings.filterwarnings("ignore")
    partes = []
    for y in range(2012, 2027):
        f = XLS / f"URBANA{y}.xls"
        if not f.exists():
            print("[falta]", f.name)
            continue
        d = pd.read_excel(f, dtype={c: str for c in CODIGO})
        d.columns = [str(c).strip().upper() for c in d.columns]
        cod = next(c for c in CODIGO if c in d.columns)
        o = pd.DataFrame({"cod_mun": d[cod].astype(str).str.zfill(5), "anio": y})
        for v in VARS:
            o[v.lower()] = pd.to_numeric(d[v], errors="coerce") if v in d.columns else float("nan")
        partes.append(o)
        print(f"[ok] {f.name}: {len(o)} municipios")
    df = pd.concat(partes, ignore_index=True).sort_values(["cod_mun", "anio"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False, compression="gzip")
    _manifest(df)
    return df


def _manifest(df: pd.DataFrame) -> None:
    man_p = RAW / "_manifest.csv"
    name = "v4/catastro_solares_municipios.csv.gz"
    row = pd.DataFrame([{
        "archivo": name, "fuente": "Catastro - Estadisticas catastrales municipales (URBANA2012-2026.xls); extracto",
        "n_series": df["cod_mun"].nunique(), "primera_fecha": f"{df.anio.min()}-01-01",
        "ultima_fecha": f"{df.anio.max()}-01-01", "n_obs": len(df), "n_nan": int(df[[v.lower() for v in VARS]].isna().sum().sum()),
        "descargado_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }])
    man = pd.read_csv(man_p)
    man = pd.concat([man[man["archivo"] != name], row], ignore_index=True)
    man.sort_values("archivo").to_csv(man_p, index=False)


def red() -> None:
    import requests
    for url in ("https://siu.mivau.gob.es/", "https://sig.mivau.gob.es/siu/"):
        try:
            r = requests.get(url, timeout=30)
            print("SIU", url, r.status_code, len(r.content))
        except Exception as e:  # noqa: BLE001
            print("SIU FALLO", url, type(e).__name__, str(e)[:120])
    base = "https://apps.fomento.gob.es/BoletinOnline/?nivel=2&orden=10000000"
    t = re.sub(r"\s+", " ", requests.get(base, timeout=60).text)
    tit = re.findall(r'href="(sedal/[^"]+)"[^>]*>([^<]+)</a>', t)
    hit = [x for x in tit if re.search(r"presupuesto|ejecuci", x[1], re.I)]
    print("licencias: tablas", len(tit), "con presupuesto:", hit)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "extract"
    if modo == "extract":
        extract()
    else:
        red()
