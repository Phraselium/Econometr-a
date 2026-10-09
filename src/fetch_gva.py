"""Series de vivienda del Portal de datos abiertos de la Generalitat (CKAN, dadesobertes.gva.es).

1) Viviendas de uso turistico (Registre de Turisme de la CV). Salida: data/raw/gva_vut_municipio.csv
   - vut_stock_*: viviendas activas a fin de mes, 2010-01..2024-12, reconstruido del historico
     (activa en t si alta <= t y (estado ALTA o baja > t)). Las 9 filas BAJA sin fecha de baja se excluyen.
   - vut_altas_*: altas registradas en el mes (flujo), por fecha de alta.
   - vut_foto_*: recuento de la lista vigente (recurso tur-gestur-vt). Fecha = fecha de modificacion del recurso.
2) Padron municipal continuo: explotacion estadistica por distritos y secciones (IVE). Un ZIP por año
   (castellano). Salida: data/raw/gva_padron_extranjeros_municipio.csv
   Se agrega a municipio sumando las filas de total de distrito (seccion en blanco).
   Series: padron_pob_total_*, padron_pob_extranjera_* (todos los años) y padron_extr_<grupo>_* solo en los
   años cuyos nombres de grupos de procedencia coinciden con los de 2022 (leidos de disenyo.txt del ZIP).
   fecha = YYYY-01-01 (referencia anual; supuesto: el padron se refiere a 1 de enero, sin verificar en las
   notas metodologicas del IVE desde este entorno).

Codigo municipal = INE de 5 digitos (provincia + municipio). Valencia ciudad = 46250.
Originales sin editar en data/raw/gva_orig/. Idempotente: download() no vuelve a bajar salvo FORCE=1 y
un CSV de salida existente no se reconstruye salvo FORCE=1.
"""
from __future__ import annotations

import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import RAW, cached, download, get, save  # noqa: E402

CKAN = "https://dadesobertes.gva.es/api/3/action/package_show"
ORIG = RAW / "gva_orig"
PROVINCIAS = {"03": "Alacant/Alicante", "12": "Castello/Castellon", "46": "Valencia/Valencia"}
VLC = "46250"

FUENTE_VUT = "Generalitat Valenciana - Registre de Turisme CV (datos abiertos CKAN)"
FUENTE_PADRON = ("IVE - Padron municipal continuo: explotacion estadistica por distritos "
                 "y secciones (datos abiertos CKAN)")

STOCK_FIN_MES = pd.date_range("2010-01-01", "2024-12-01", freq="MS")
ALTAS_MESES = pd.date_range("2010-01-01", "2025-01-01", freq="MS")
ANIOS_PADRON = range(2005, 2023)
COLS_SALIDA = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "ambito", "codigo",
               "nombre", "dataset_ckan", "ckan_modificado"]


# ---------------------------------------------------------------- CKAN

def ckan_pkg(nombres: list[str]) -> dict:
    """Devuelve el paquete CKAN (package_show) probando los nombres en orden."""
    ultimo = None
    for n in nombres:
        try:
            r = get(CKAN, params={"id": n})
        except RuntimeError as e:
            ultimo = e
            continue
        if r.get("success"):
            return r["result"]
    raise RuntimeError(f"CKAN sin paquete para {nombres}: {ultimo}")


def ckan_recurso(pkg: dict, pred) -> dict:
    for r in pkg["resources"]:
        if pred(r):
            return r
    raise RuntimeError(f"CKAN {pkg['name']}: ningun recurso cumple la condicion")


def fecha_mod(obj: dict) -> str:
    return (obj.get("last_modified") or obj.get("metadata_modified") or "")[:10]


# ---------------------------------------------------------------- VUT

def _cargar_historico(path: Path) -> pd.DataFrame:
    h = pd.read_csv(path, sep=";", encoding="latin-1", dtype=str)
    h["prov"] = h["Cod. Provincia"].str.zfill(2)
    h["cod"] = h["prov"] + h["Cod. Municipio"].str.zfill(3)
    h["alta"] = pd.to_datetime(h["Fecha alta"], format="%d/%m/%Y", errors="coerce")
    h["baja"] = pd.to_datetime(h["Fecha baja"], format="%d/%m/%Y", errors="coerce")
    h["nombre"] = h["Municipio"]
    if h["alta"].isna().any():
        raise ValueError("historico VUT: fecha de alta no parseable")
    return h


def _activas(h: pd.DataFrame, t: pd.Timestamp) -> pd.Series:
    return (h["alta"] <= t) & (h["Estado"].eq("ALTA") | (h["baja"] > t))


def _filas_recuento(total: int, prov: pd.Series, mun: pd.Series, fecha: str, periodo: str,
                    tipo: str, unidad: str, url: str, dataset: str, mod: str,
                    nombres: dict) -> list[dict]:
    """Convierte recuentos (CV, provincias, municipios) en filas de formato largo."""
    base = dict(fecha=fecha, periodo=periodo, unidad=unidad, fuente=FUENTE_VUT, url=url,
                dataset_ckan=dataset, ckan_modificado=mod)
    filas = [dict(base, serie=f"vut_{tipo}_cv", valor=int(total), ambito="cv", codigo="CV",
                  nombre="Comunitat Valenciana")]
    for p, v in prov.items():
        filas.append(dict(base, serie=f"vut_{tipo}_prov_{p}", valor=int(v), ambito="provincia",
                          codigo=p, nombre=PROVINCIAS.get(p, p)))
    for c, v in mun.items():
        filas.append(dict(base, serie=f"vut_{tipo}_mun_{c}", valor=int(v), ambito="municipio",
                          codigo=c, nombre=nombres.get(c, c)))
    return filas


def build_vut() -> None:
    nombre = "gva_vut_municipio.csv"
    if cached(nombre):
        return
    pkg_h = ckan_pkg(["dades-turisme-habitatges-comunitat-valenciana-2025"])
    r_h = ckan_recurso(pkg_h, lambda r: "hist" in r["name"].lower() and r["format"].upper() == "CSV")
    pkg_l = ckan_pkg(["tur-gestur-vt"])
    r_l = ckan_recurso(pkg_l, lambda r: r["format"].upper() == "CSV")

    p_h = download(r_h["url"], ORIG / "vut_historico_2025.csv")
    p_l = download(r_l["url"], ORIG / "vut_lista_actual.csv")

    h = _cargar_historico(p_h)
    codigos = sorted(h["cod"].unique())
    provs = sorted(PROVINCIAS)
    nombres = h.drop_duplicates("cod").set_index("cod")["nombre"].to_dict()
    print(f"[vut] historico: {len(h)} filas, {len(codigos)} municipios, "
          f"alta {h['alta'].min().date()}..{h['alta'].max().date()}")

    filas: list[dict] = []
    url_h, ds_h, mod_h = r_h["url"], pkg_h["name"], fecha_mod(r_h)

    # Stock a fin de mes (fecha = primer dia del mes; corte al ultimo dia)
    for m in STOCK_FIN_MES:
        t = m + pd.offsets.MonthEnd(0)
        act = h.loc[_activas(h, t)]
        prov = act["prov"].value_counts().reindex(provs, fill_value=0)
        mun = act["cod"].value_counts().reindex(codigos, fill_value=0)
        filas += _filas_recuento(len(act), prov, mun, m.strftime("%Y-%m-%d"), m.strftime("%Y-%m"),
                                 "stock", "viviendas (stock a fin de mes)", url_h, ds_h, mod_h, nombres)

    # Altas mensuales (flujo)
    for m in ALTAS_MESES:
        sel = h.loc[(h["alta"] >= m) & (h["alta"] < m + pd.offsets.MonthBegin(1))]
        prov = sel["prov"].value_counts().reindex(provs, fill_value=0)
        mun = sel["cod"].value_counts().reindex(codigos, fill_value=0)
        filas += _filas_recuento(len(sel), prov, mun, m.strftime("%Y-%m-%d"), m.strftime("%Y-%m"),
                                 "altas", "viviendas (altas en el mes)", url_h, ds_h, mod_h, nombres)

    # Foto de la lista vigente (tur-gestur-vt)
    lista = pd.read_csv(p_l, sep=";", dtype=str, encoding="utf-8")
    lista["prov"] = lista["cod_provincia"].str.zfill(2)
    lista["cod"] = lista["prov"] + lista["cod_municipio"].str.zfill(3)
    fecha_foto = fecha_mod(r_l)
    prov = lista["prov"].value_counts().reindex(provs, fill_value=0)
    mun = lista["cod"].value_counts()
    nombres_l = lista.drop_duplicates("cod").set_index("cod")["municipio"].to_dict()
    mun = mun.reindex(sorted(set(codigos) | set(mun.index)), fill_value=0)
    filas += _filas_recuento(len(lista), prov, mun, fecha_foto, fecha_foto[:7],
                             "foto", "viviendas (registros vigentes en la lista)", r_l["url"],
                             pkg_l["name"], fecha_mod(r_l), {**nombres, **nombres_l})

    df = pd.DataFrame(filas)
    print(f"[vut] foto {fecha_foto}: {len(lista)} registros; Valencia ciudad {int(mun.get(VLC, 0))}")
    save(df, nombre, FUENTE_VUT)


# ---------------------------------------------------------------- PADRON

def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _leer_prn(zf: zipfile.ZipFile, miembro: str) -> pd.DataFrame:
    """Lee un .prn de ancho fijo: clave de 12 caracteres (prov 2, comarca 2, municipio 3, distrito 2,
    seccion 3) y N campos de 8 caracteres. N se infiere de la longitud de linea (varia por año).
    Seccion en blanco = total de distrito."""
    with zf.open(miembro) as fh:
        lineas = [raw.decode("latin-1").rstrip("\r\n") for raw in fh]
    lineas = [ln for ln in lineas if ln.strip()]
    ancho = max(len(ln) for ln in lineas)
    n = (ancho - 12 + 7) // 8
    filas = []
    for ln in lineas:
        vals = []
        for j in range(n):
            s = ln[12 + 8 * j:20 + 8 * j].strip()
            vals.append(float(s) if s else np.nan)
        filas.append((ln[0:2], ln[4:7], ln[7:9], ln[9:12].strip(), *vals))
    cols = ["prov", "mun", "distrito", "seccion"] + [f"v{j}" for j in range(n)]
    return pd.DataFrame(filas, columns=cols)


def _agregar_municipio(zf: zipfile.ZipFile, miembros: dict, ficheros: tuple[str, str]) -> pd.DataFrame:
    """Suma hombres y mujeres y agrega a municipio usando los totales de distrito (seccion en blanco).
    Si un distrito no trae fila de total, se suman sus secciones."""
    d = pd.concat([_leer_prn(zf, miembros[f]) for f in ficheros], ignore_index=True)
    vcols = [c for c in d.columns if c.startswith("v")]
    clave = ["prov", "mun", "distrito"]
    tot = d[d["seccion"] == ""].groupby(clave)[vcols].sum(min_count=1)
    sec = d[d["seccion"] != ""].groupby(clave)[vcols].sum(min_count=1)
    faltan = sec.index.difference(tot.index)
    if len(faltan):
        print(f"[padron] {len(faltan)} distritos sin fila de total: se usan secciones")
        tot = pd.concat([tot, sec.loc[faltan]])
    return tot.groupby(level=["prov", "mun"]).sum(min_count=1)


def _nombres_ta6(zf: zipfile.ZipFile, miembros: dict) -> list[str]:
    """Nombres de los grupos de procedencia de ta6_1 leidos de disenyo.txt del ZIP ([] si no se leen)."""
    if "disenyo.txt" not in miembros:
        return []
    txt = zf.read(miembros["disenyo.txt"]).decode("latin-1")
    i = txt.find("ta6_1.prn y ta6_6.prn")
    if i < 0:
        return []
    nombres: list[str] = []
    for linea in txt[i:].splitlines()[1:]:
        s = linea.strip()
        if not s:
            if nombres:
                break
            continue
        if s.startswith("---") or s.startswith("Variable"):
            continue
        m = re.match(r"^(.*?)\s+(\d+)\s*$", s)
        if not m:
            break
        nombre = m.group(1).strip()
        if nombre.lower().startswith(("código", "codigo")):
            continue
        nombres.append(nombre)
    return nombres


def build_padron() -> None:
    nombre = "gva_padron_extranjeros_municipio.csv"
    if cached(nombre):
        return
    anios = []
    for y in ANIOS_PADRON:
        try:
            pkg = ckan_pkg([f"padro-municipal-continu-explotacio-estadistica-per-districtes-i-seccions-{y}",
                            f"padro-municipal-continu-explotacio-estadistica-per-districtes-i-seccions-{y}-v3"])
            r = ckan_recurso(pkg, lambda r: "castellan" in r["name"].lower() and r["format"].upper() == "ZIP")
        except RuntimeError as e:
            print(f"[padron] {y}: sin recurso en CKAN ({e})")
            continue
        zp = download(r["url"], ORIG / f"padron_dist_{y}_cas.zip")
        try:
            with zipfile.ZipFile(zp) as zf:
                miembros = {Path(m).name.lower(): m for m in zf.namelist()}
                pob = _agregar_municipio(zf, miembros, ("ta1_1.prn", "ta1_6.prn"))
                ext = _agregar_municipio(zf, miembros, ("ta6_1.prn", "ta6_6.prn"))
                nombres_grp = _nombres_ta6(zf, miembros)
        except (ValueError, KeyError, zipfile.BadZipFile) as e:
            print(f"[padron] {y}: formato no reconocido, se omite ({e})")
            continue
        anios.append(dict(y=y, url=r["url"], dataset=pkg["name"], mod=fecha_mod(r),
                          pob=pob, ext=ext, nombres=nombres_grp))

    if not anios:
        raise RuntimeError("padron: ningun año descargado")
    # Diseño de referencia: grupos de procedencia del año mas reciente que los lea
    canon = next((a["nombres"] for a in reversed(anios)
                  if a["nombres"] and len(a["nombres"]) == a["ext"].shape[1]), [])
    print(f"[padron] grupos de procedencia de referencia: {len(canon)}")

    partes = []
    for a in anios:
        y = a["y"]
        idx = a["pob"].index.union(a["ext"].index)
        pob = a["pob"].reindex(idx)
        ext = a["ext"].reindex(idx)
        w = pd.DataFrame(index=idx)
        w["padron_pob_total"] = pob.sum(axis=1, min_count=1)
        w["padron_pob_extranjera"] = ext.sum(axis=1, min_count=1)
        if canon and a["nombres"] == canon and ext.shape[1] == len(canon):
            for j, g in enumerate(canon):
                w[f"padron_extr_{_slug(g)}"] = ext.iloc[:, j]
        else:
            print(f"[padron] {y}: grupos de procedencia no comparables con la referencia; solo totales")
        w = w.reset_index()
        w["codigo"] = w["prov"] + w["mun"]
        cv = w.drop(columns=["prov", "mun", "codigo"]).sum(min_count=1)

        largo = w.drop(columns=["prov", "mun"]).melt(id_vars=["codigo"], var_name="var", value_name="valor")
        resumen = pd.DataFrame([{"codigo": "CV", "var": k, "valor": v} for k, v in cv.items()])
        largo = pd.concat([largo, resumen], ignore_index=True)
        es_cv = largo["codigo"].eq("CV")
        largo["ambito"] = np.where(es_cv, "cv", "municipio")
        largo["nombre"] = np.where(es_cv, "Comunitat Valenciana", "")
        largo["serie"] = np.where(es_cv, largo["var"] + "_cv", largo["var"] + "_mun_" + largo["codigo"])
        largo["periodo"] = str(y)
        largo["fecha"] = f"{y}-01-01"
        largo["unidad"] = "personas"
        largo["fuente"] = FUENTE_PADRON
        largo["url"] = a["url"]
        largo["dataset_ckan"] = a["dataset"]
        largo["ckan_modificado"] = a["mod"]
        partes.append(largo)

        val = w.loc[w["codigo"].eq(VLC)].iloc[0]
        print(f"[padron] {y}: {len(w)} municipios; Valencia ciudad pob={val['padron_pob_total']:.0f} "
              f"extranjera={val['padron_pob_extranjera']:.0f}")

    df = pd.concat(partes, ignore_index=True)[COLS_SALIDA]
    save(df, nombre, FUENTE_PADRON)


def main() -> None:
    build_vut()
    build_padron()


if __name__ == "__main__":
    main()
