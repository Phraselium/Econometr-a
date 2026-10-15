"""V11-DATOS: incorporación de las descargas manuales del autor (docs/v11/descargas_manuales.md).

`make datos_v11` llama a `main()` después de los fetchers. Para cada carpeta data/manual/v11/<fuente>/:
1. registra cada fichero en data/raw/v11/manual/_manifest.csv con sha256, filas y origen «descarga manual del autor»
   (los originales se quedan en data/manual/v11/; las licencias son las del organismo, anotadas abajo);
2. valida según la fuente (totales frente a cifras publicadas o a series ya en la base); el resultado va a la columna
   «notas» y a data/raw/v11/manual/validacion.csv; una validación fallida NO bloquea, pero la fila queda marcada;
3. si sabe leer el formato, escribe una tabla normalizada en data/raw/v11/manual/<fuente>.csv.gz, que
   src/v11/base_v11.py incorpora a la base (`make base`).
Sin carpeta data/manual/v11/ no hace nada (código 0). Cruces solo por código INE.
"""
from __future__ import annotations

import csv
import io
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import GZ_PANDAS, RAIZ, RAW11, marcar_posterior_prereg, registrar  # noqa: E402

MANUAL = RAIZ / "data" / "manual" / "v11"
SALIDA = RAW11 / "manual"
ORIGEN = "descarga manual del autor"
LIC = {"opi_residentes": "Ministerio de Inclusión (OPI): reutilización con cita", "interior_asilo": "Ministerio del Interior: reutilización con cita",
       "gva_bdo_afiliacion": "Generalitat Valenciana: CC BY 4.0", "bcn_hut_trimestral": "Ajuntament de Barcelona: CC BY 4.0",
       "gva_vut_wayback": "Generalitat Valenciana: CC BY 4.0 (copia de web.archive.org)", "catastro_valores_referencia": "Catastro: reutilización con cita",
       "universidades": "según organismo (verificar antes de publicar)", "fgv_gtfs": "FGV: según condiciones del portal"}
REDIS = {"universidades": False, "fgv_gtfs": False}


def leer_tabla(p: Path) -> pd.DataFrame | None:
    try:
        if p.suffix.lower() in (".xlsx", ".xls"):
            return pd.read_excel(p, dtype=str)
        if p.suffix.lower() == ".csv":
            for enc in ("utf-8", "latin-1"):
                try:
                    return pd.read_csv(p, sep=None, engine="python", dtype=str, encoding=enc)
                except UnicodeDecodeError:
                    continue
    except Exception:  # noqa: BLE001
        return None
    return None


def numero(s) -> float:
    return pd.to_numeric(str(s).replace(".", "").replace(",", "."), errors="coerce")


# ---------------------------------------------------------------------------------------------- validaciones
def v_opi(ficheros: list[Path]) -> tuple[str, pd.DataFrame | None]:
    """Total nacional frente a la población extranjera de la ECP (ratio plausible 0,6-1,4): la OPI incluye ciudadanos
    UE con certificado no empadronados y excluye irregulares, así que no coinciden exactamente."""
    ecp = RAIZ / "data/raw/ine_ecp_56936.csv"
    filas = []
    for p in ficheros:
        d = leer_tabla(p)
        if d is None:
            continue
        txt = d.astype(str)
        tot = [numero(v) for v in txt.values.ravel() if re.fullmatch(r"\d{1,3}(\.\d{3}){2,}", v.strip())]
        filas.append({"fichero": p.name, "max_numero": max(tot) if tot else None})
    msg = "OPI: registrado; " + "; ".join(f"{f['fichero']}: máximo={f['max_numero']}" for f in filas)
    if ecp.exists():
        e = pd.read_csv(ecp)
        ult = e[e.nombre.str.contains("Total Nacional. Extranjera|Total Nacional. Total extranjeros", regex=True, na=False)]
        if len(ult):
            msg += f"; ECP extranjeros último={ult.valor.iloc[-1]:.0f} (comparar: ratio esperado 0,6-1,4)"
    return msg, None


def v_bcn(ficheros: list[Path]) -> tuple[str, pd.DataFrame | None]:
    partes = []
    for p in ficheros:
        m = re.match(r"(\d{4})_(\d)T", p.name)
        if not (m and p.suffix == ".zip"):
            continue
        with zipfile.ZipFile(p) as z:
            n = next(x for x in z.namelist() if x.lower().endswith(".csv"))
            d = pd.read_csv(io.BytesIO(z.read(n)), dtype=str, sep=None, engine="python", encoding="utf-8")
        cb = next((c for c in d.columns if "BARRI" in c.upper() and "CODI" in c.upper()), None)
        g = (d.groupby(cb).size() if cb else pd.Series({"total": len(d)})).rename("hut").reset_index()
        g.columns = ["cod_barrio_bcn", "hut"]
        g["trimestre"] = f"{m.group(1)}T{m.group(2)}"
        partes.append(g)
    if not partes:
        return "Barcelona: sin zips reconocibles", None
    D = marcar_posterior_prereg(pd.concat(partes, ignore_index=True), "trimestre")
    return f"Barcelona: {D.trimestre.nunique()} cortes, {D.trimestre.min()}-{D.trimestre.max()}; último total={int(D[D.trimestre == D.trimestre.max()].hut.sum())}", D


def v_gtfs(ficheros: list[Path]) -> tuple[str, pd.DataFrame | None]:
    ok = []
    for p in ficheros:
        if p.suffix == ".zip":
            with zipfile.ZipFile(p) as z:
                ok.append(f"{p.name}: {'OK' if {'stops.txt', 'routes.txt', 'trips.txt'} <= set(z.namelist()) else 'FALTAN ficheros GTFS'}")
    return "GTFS: " + "; ".join(ok), None


def v_universidades(ficheros: list[Path]) -> tuple[str, pd.DataFrame | None]:
    hall = any("51697" in leer_tabla(p).to_string().replace(".", "") for p in ficheros if leer_tabla(p) is not None)
    return f"Universidades: total UV 2024/25 = 51.697 {'encontrado' if hall else 'NO encontrado (revisar)'}", None


def v_bdo(ficheros: list[Path]) -> tuple[str, pd.DataFrame | None]:
    partes = []
    for p in ficheros:
        d = leer_tabla(p)
        if d is None:
            continue
        col = d.columns[0]
        cod = d[col].astype(str).str.extract(r"(\d{5})")[0]
        d = d.assign(cod_municipio=cod).dropna(subset=["cod_municipio"])
        L = d.melt(id_vars=[col, "cod_municipio"], var_name="columna", value_name="valor")
        L["valor"] = L.valor.map(numero)
        L["fichero"] = p.name
        partes.append(L.dropna(subset=["valor"]))
    if not partes:
        return "BDO GVA: sin tablas legibles", None
    D = pd.concat(partes, ignore_index=True)
    return f"BDO GVA: {D.cod_municipio.nunique()} municipios, {len(D)} celdas (columnas = periodo × categoría; revisar cabeceras)", D


def v_generico(ficheros: list[Path]) -> tuple[str, pd.DataFrame | None]:
    return f"registrado ({len(ficheros)} ficheros); validación manual pendiente", None


VALIDA = {"opi_residentes": v_opi, "bcn_hut_trimestral": v_bcn, "fgv_gtfs": v_gtfs, "universidades": v_universidades,
          "gva_bdo_afiliacion": v_bdo}


def main() -> int:
    if not MANUAL.exists():
        print("[manual] sin data/manual/v11/: nada que incorporar")
        return 0
    SALIDA.mkdir(parents=True, exist_ok=True)
    val = []
    for carpeta in sorted(x for x in MANUAL.iterdir() if x.is_dir()):
        fuente = carpeta.name
        ficheros = sorted(p for p in carpeta.rglob("*") if p.is_file() and not p.name.startswith("."))
        if not ficheros:
            continue
        msg, tabla = VALIDA.get(fuente, v_generico)(ficheros)
        val.append({"fuente": fuente, "ficheros": len(ficheros), "validacion": msg})
        for p in ficheros:
            registrar("manual", p, f"data/manual/v11/{fuente}/{p.name}", edicion=ORIGEN, periodo="ver fichero",
                      nivel_territorial="según fuente", licencia=LIC.get(fuente, "según organismo"), redistribuible=REDIS.get(fuente, True),
                      notas=f"origen: {ORIGEN}; {msg[:300]}")
        if tabla is not None:
            r = SALIDA / f"{fuente}.csv.gz"
            tabla.to_csv(r, index=False, compression=GZ_PANDAS)
            registrar("manual", r, f"data/manual/v11/{fuente}/", edicion=f"{ORIGEN} (normalizado)", periodo="ver fichero",
                      nivel_territorial="según fuente", licencia=LIC.get(fuente, "según organismo"), redistribuible=REDIS.get(fuente, True),
                      notas=f"origen: {ORIGEN}; tabla normalizada para la base")
        print(f"[manual] {fuente}: {msg}")
    with open(SALIDA / "validacion.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["fuente", "ficheros", "validacion"])
        w.writeheader()
        w.writerows(val)
    return 0


if __name__ == "__main__":
    sys.exit(main())
