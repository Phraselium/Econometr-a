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

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import GZ_PANDAS, RAIZ, RAW11, marcar_posterior_prereg, registrar  # noqa: E402

MANUAL = RAIZ / "data" / "manual" / "v11"
SALIDA = RAW11 / "manual"
ORIGEN = "descarga manual del autor"
LIC = {"icane_extranjeros_tarjeta": "ICANE (Gobierno de Cantabria): reutilización con cita", "opi_residentes": "Ministerio de Inclusión (OPI): reutilización con cita", "interior_asilo": "Ministerio del Interior: reutilización con cita",
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
    """Cortes trimestrales del registro HUT del Ajuntament de Barcelona (AAAA_nT_hut_comunicacio*.csv.zip). Hasta 2023T1
    los ficheros no traen código de barrio (solo nombre): de esos cortes se usa solo el total de la ciudad (los barrios
    no se cruzan por nombre). Desde que traen CODI_BARRI, también por barrio. Ficheros sin fecha en el nombre: solo se
    registran."""
    partes = []
    for p in ficheros:
        m = re.match(r"(\d{4})_(\d)T", p.name)
        if not (m and p.suffix == ".zip"):
            continue
        with zipfile.ZipFile(p) as z:
            n = next(x for x in z.namelist() if x.lower().endswith(".csv"))
            raw = z.read(n)
        try:
            txt = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            txt = raw.decode("latin-1")
        # csv.reader y no pandas: algunos cortes traen filas con una coma de más sin entrecomillar en la dirección;
        # cada fila es un registro y las columnas que se usan (código de barrio, plazas) se leen por su posición
        filas_csv = [r for r in csv.reader(io.StringIO(txt)) if r]
        cab, todas = [c.strip().upper() for c in filas_csv[0]], filas_csv[1:]
        # una vivienda por expediente: algunos cortes (2023T4) repiten filas del mismo expediente
        vistos, datos = set(), []
        for r in todas:
            if r[0] not in vistos:
                vistos.add(r[0])
                datos.append(r)
        trim = f"{m.group(1)}T{m.group(2)}"
        ipl = next((i for i, c in enumerate(cab) if "PLACES" in c), None)
        icb = cab.index("CODI_BARRI") if "CODI_BARRI" in cab else None
        largo = len(cab)
        malas = sum(len(r) != largo for r in datos)
        usar_pl = ipl is not None and malas <= 0.05 * len(datos)   # plazas solo si ≥ 95 % de filas bien formadas
        places = [numero(r[ipl]) if usar_pl and len(r) == largo else np.nan for r in datos]
        filas = [{"cod_barrio_bcn": "Total", "hut": len(datos), "places": np.nansum(places) if usar_pl else np.nan,
                  "filas_fichero": len(todas), "filas_mal_formadas": malas}]
        if icb is not None:
            g = pd.DataFrame({"b": [r[icb].strip().zfill(2) for r in datos], "pl": places}).groupby("b")
            filas += [{"cod_barrio_bcn": k, "hut": int(len(x)), "places": x.pl.sum(min_count=1)} for k, x in g]
        partes.append(pd.DataFrame(filas).assign(trimestre=trim, fichero=p.name))
    if not partes:
        return "Barcelona: sin zips reconocibles", None
    D = pd.concat(partes, ignore_index=True)
    dup = D[D.cod_barrio_bcn == "Total"].groupby("hut").trimestre.apply(list)
    rep = [v for v in dup if len(v) > 1]
    D = marcar_posterior_prereg(D, "trimestre")
    tot = D[D.cod_barrio_bcn == "Total"].set_index("trimestre").hut
    msg = (f"Barcelona: {tot.size} cortes {tot.index.min()}-{tot.index.max()}; total último={int(tot.iloc[-1])}; "
           f"con código de barrio desde {D[D.cod_barrio_bcn != 'Total'].trimestre.min()}; cortes con el mismo recuento: {rep}")
    return msg, D


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
    """Banco de Datos Municipal de la GVA (consulta V0201_C2D0244): afiliados a la Seguridad Social por municipio,
    trimestre, sexo y nacionalidad (españoles, UE, otros extranjeros). Código INE del prefijo «03001 - nombre». «-» en
    origen = dato no disponible o secreto: NaN. Validación: provincia de Valencia frente a la afiliación municipal de la
    Seguridad Social (data/raw/v11/ss_afiliacion_municipio) del mismo trimestre (definiciones de municipio distintas:
    se informa del ratio)."""
    partes = []
    for p in ficheros:
        if p.suffix.lower() != ".csv":
            continue
        d = pd.read_csv(p, dtype=str, encoding="latin-1")
        if not {"Trimestre", "Municipios", "Sexo", "Nacionalidad", "Valor"} <= set(d.columns):
            continue
        t = d.Trimestre.str.extract(r"(\d{4})\D+(\d)")
        d["trimestre"] = t[0] + "T" + t[1]
        d["cod_municipio"] = d.Municipios.str.extract(r"^(\d{5})")[0]
        d["valor"] = pd.to_numeric(d.Valor.str.replace(".", "", regex=False), errors="coerce")
        d["sexo"] = d.Sexo.str.strip()
        d["nacionalidad"] = d.Nacionalidad.str.strip().map({"Españoles": "ES", "Extranjeros de la Unión Europea": "EXT_UE",
                                                           "Otros extranjeros": "EXT_no_UE", "Total": "Total"})
        partes.append(d.dropna(subset=["cod_municipio"])[["trimestre", "cod_municipio", "sexo", "nacionalidad", "valor"]].assign(fichero=p.name))
    if not partes:
        return "BDO GVA: sin tablas legibles", None
    D = marcar_posterior_prereg(pd.concat(partes, ignore_index=True), "trimestre")
    u = D.trimestre.max()
    v = D[(D.trimestre == u) & (D.sexo == "Ambos sexos")].pivot_table(index="cod_municipio", columns="nacionalidad", values="valor", aggfunc="sum")
    ext = 100 * (v.EXT_UE + v.EXT_no_UE).sum() / v.Total.sum()
    msg = (f"BDO GVA: {D.cod_municipio.nunique()} municipios, {D.trimestre.min()}-{u}; {u}: total {v.Total.sum():.0f}, "
           f"extranjeros {ext:.1f} %; València {v.Total.get('46250', np.nan):.0f}")
    f = RAW11 / "ss_afiliacion_municipio/afiliacion_municipio_mensual.csv.gz"
    if f.exists():
        a = pd.read_csv(f, dtype={"cod_municipio": str, "mes": str})
        meses = {"T1": ("01", "02", "03"), "T2": ("04", "05", "06"), "T3": ("07", "08", "09"), "T4": ("10", "11", "12")}[u[4:]]
        a = a[a.mes.isin([f"{u[:4]}-{m}" for m in meses]) & (a.cod_municipio.str[:2] == "46")]
        if len(a):
            ss = a.groupby("mes").afiliados_suma_numerica.sum().mean()
            bdo = D[(D.trimestre == u) & (D.sexo == "Ambos sexos") & (D.nacionalidad == "Total") & (D.cod_municipio.str[:2] == "46")].valor.sum()
            msg += f"; provincia 46: BDO {bdo:.0f} frente a SS {ss:.0f} (ratio {bdo / ss:.3f}; la SS suma celdas < 5 como 0)"
    return msg, D


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
