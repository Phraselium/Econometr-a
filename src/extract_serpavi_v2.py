"""SERPAVI v2 (MIVAU, Sistema Estatal de Referencia del Precio del Alquiler) -> TODOS los municipios y provincias.

Entrada: data/raw/pdf/originales/serpavi_bd_2011-2024.xlsx (BD oficial, 71 MB, excluida de git).
         Si no existe y no hay salida en cache, se descarga con la URL verificada en extract_serpavi.py.
Salida:  data/raw/pdf/serpavi_v2_municipios.csv  (formato largo; hojas 'Municipios' y 'Provincias')

Variables (solo las pedidas; nombres de serie IGUALES a v1 para poder contrastar):
  alquiler_m2 mediana / p25 / p75  (EUR/m2/mes, vivienda habitual en alquiler, tipologia VC y VU)
  n_contratos                      (recuento; el Metadatos lo define como BIENES INMUEBLES con
                                    ingresos por arrendamiento de vivienda habitual, no contratos)
  VC = vivienda colectiva, VU = vivienda unifamiliar o rural (tipologia de mayor superficie).

Anyos 2011-2024. Huecos (celdas vacias: muestra insuficiente / secreto estadistico) se omiten, no se rellenan.
Caché: si la salida existe y no hay FORCE=1, no hace falta el XLSX.
El CSV supera 50 MB: no se versiona (gitignore) y su checksum va a data/CHECKSUMS.sha256.
Registro en data/raw/_manifest.csv con el mismo formato que utils_fetch.save().
"""
from __future__ import annotations

import datetime as dt
import fcntl
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import FORCE, MANIFEST, RAW, download  # noqa: E402
from extract_serpavi import PAGE_URL, XLSX, XLSX_URL  # noqa: E402  (reutiliza ruta y URL de v1; v1 no se modifica)

OUT = RAW / "pdf" / "serpavi_v2_municipios.csv"
FUENTE = "MIVAU-SERPAVI (AEAT IRPF)"
COL_RE = re.compile(r"^(BI_ALVHEPCO|ALQM2(?:mes)?_LV)_(M|25|75|TVC|TVU)(?:_(VC|VU))?_(\d{2})$")
STAT = {"M": "mediana", "25": "p25", "75": "p75"}
COLS = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "nivel", "codigo", "nombre",
        "provincia_codigo", "provincia_nombre", "tipologia", "variable", "estadistico"]


def parse_cols(header) -> dict:
    """Mapa indice de columna -> (anyo, tipologia, variable, unidad, estadistico), solo variables pedidas."""
    cols = {}
    for i, h in enumerate(header):
        m = COL_RE.match(str(h).strip()) if h is not None else None
        if not m:
            continue
        v, s, t, yy = m.groups()
        if v == "BI_ALVHEPCO":
            tip, est = {"TVC": "VC", "TVU": "VU"}[s], "recuento"
            var, uni = "n_contratos", "bienes_inmuebles"
        else:
            tip, est = t, STAT[s]
            var, uni = "alquiler_m2", "EUR/m2/mes"
        cols[i] = (2000 + int(yy), tip, var, uni, est)
    return cols


def leer_hoja(wb, nombre: str, nivel: str, cod_idx: int, nom_idx: int, prov_idx: int | None,
              prov_nom_idx: int | None) -> pd.DataFrame:
    ws = wb[nombre].iter_rows(values_only=True)
    header = next(ws)
    cols = parse_cols(header)
    recs = []
    for row in ws:
        if row[cod_idx] is None:
            continue
        cod = str(row[cod_idx]).strip()
        cod = cod.zfill(2) if nivel == "PROV" else cod.zfill(5)
        nom = str(row[nom_idx]).strip() if nom_idx is not None else ""
        if prov_idx is not None:
            pcod = str(row[prov_idx]).strip().zfill(2)
            pnom = str(row[prov_nom_idx]).strip()
        else:
            pcod, pnom = cod.zfill(2), nom
        for i, (y, tip, var, uni, est) in cols.items():
            v = row[i]
            if v is None or v == "":
                continue
            try:
                v = float(v)
            except (TypeError, ValueError):
                continue
            recs.append((f"{y}-01-01", str(y), f"SERPAVI_{nivel}_{cod}_{tip}_{var}_{est}", v, uni, FUENTE,
                         XLSX_URL, nivel, cod, nom, pcod, pnom, tip, var, est))
    return pd.DataFrame(recs, columns=COLS)


def registrar(df: pd.DataFrame) -> None:
    """Fila en _manifest.csv (mismo formato que utils_fetch.save; archivo relativo a data/raw)."""
    row = pd.DataFrame([{
        "archivo": f"pdf/{OUT.name}", "fuente": FUENTE, "n_series": df["serie"].nunique(),
        "primera_fecha": str(df["fecha"].min()), "ultima_fecha": str(df["fecha"].max()),
        "n_obs": len(df), "n_nan": int(df["valor"].isna().sum()),
        "descargado_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }])
    with open(RAW / ".manifest.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if MANIFEST.exists():
            man = pd.read_csv(MANIFEST)
            man = pd.concat([man[man["archivo"] != row.archivo[0]], row], ignore_index=True)
        else:
            man = row
        man.sort_values("archivo").to_csv(MANIFEST, index=False)


def validar(df: pd.DataFrame) -> None:
    """Contraste con la salida v1 (provincias y municipios de la provincia 46) en las series comunes."""
    v1 = []
    for f in ("serpavi_provincias.csv", "serpavi_municipios_46.csv"):
        p = RAW / "pdf" / f
        if p.exists():
            v1.append(pd.read_csv(p, dtype={"codigo": str}, usecols=["serie", "valor"]))
    if not v1:
        return
    ref = pd.concat(v1, ignore_index=True).drop_duplicates("serie").set_index("serie")["valor"]
    nue = df.drop_duplicates("serie").set_index("serie")["valor"]
    comunes = nue.index.intersection(ref.index)
    if len(comunes) == 0:
        print("  [control] sin series comunes con v1")
        return
    # Mismo valor de origen: la diferencia debe ser nula (salvo redondeo de la exportacion)
    dif = (nue.loc[comunes] - ref.loc[comunes]).abs()
    print(f"  [control] v1 vs v2 en {len(comunes)} series comunes: dif. máx {dif.max():.6g}, "
          f"series distintas {(dif > 1e-9).sum()}")


def main() -> None:
    if OUT.exists() and not FORCE:
        print(f"[cache] {OUT.relative_to(RAW.parent)}")
        return
    import openpyxl
    if not XLSX.exists() or FORCE:
        download(XLSX_URL, XLSX, timeout=900)
    wb = openpyxl.load_workbook(XLSX, read_only=True)
    prov = leer_hoja(wb, "Provincias", "PROV", cod_idx=0, nom_idx=1, prov_idx=None, prov_nom_idx=None)
    mun = leer_hoja(wb, "Municipios", "MUN", cod_idx=2, nom_idx=3, prov_idx=0, prov_nom_idx=1)
    wb.close()
    df = pd.concat([prov, mun], ignore_index=True).sort_values(["serie", "fecha"]).reset_index(drop=True)
    n_prov = df.loc[df.nivel == "PROV", "codigo"].nunique()
    n_mun = df.loc[df.nivel == "MUN", "codigo"].nunique()
    validar(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    registrar(df)
    print(f"[ok] {OUT.name}: {len(df)} obs, {df.serie.nunique()} series, {n_prov} provincias, "
          f"{n_mun} municipios, {df.fecha.min()} -> {df.fecha.max()}, NaN={int(df.valor.isna().sum())}")


if __name__ == "__main__":
    main()
