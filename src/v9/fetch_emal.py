"""V9-DATOS · fuente `emal`: Estadística del Mercado de Alquiler de Euskadi (EMAL, Gobierno Vasco, operación 122417).

Descarga los dos libros de tablas del catálogo de datos abiertos de Euskadi (edición 2016-2025, datos a 31-12-2025
y contratos por trimestre/año de inicio) y los convierte a CSV largo:
  periodo, nivel, codigo_ine, nombre, grupo, tipo_contrato, variable, valor, hoja, posterior_prereg

Nada de estimación: solo lectura de hojas, normalización y validación aritmética básica.
Licencia: CC BY 4.0 (dct:license del DCAT oficial de las tablas, comprobado 2026-10-14) -> redistribuible.
"""
from __future__ import annotations

import gzip
import re
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAW9, descargar, marcar_posterior_prereg, registrar, sha256  # noqa: E402

FUENTE = "emal"
DIR = RAW9 / FUENTE
BASE = "https://www.euskadi.eus/contenidos/estadistica/122417_emal_tablas_estad/opendata/"
FICHEROS = {
    "EMAL-2016-2025_es.xlsx": "territorio histórico, tamaño municipal, comarcas y áreas funcionales (libre, vivienda habitual y temporada)",
    "EMAL.-Barrios-Municipios.-2016-2025_es.xlsx": "municipios >5.000 hab., zonificación OFIN, distritos y barrios de capitales",
}
EDICION = "2016-2025 (datos a 31-12-2025; DCAT 2016-2025T4)"
LICENCIA = "CC BY 4.0 (dct:license, DCAT oficial de las tablas EMAL)"
ANIOS = {str(a) for a in range(2016, 2030)}
TRIM = {"I": 1, "II": 2, "III": 3, "IV": 4}
SALIDA = DIR / "emal_largo.csv"


def _txt(c) -> str:
    return "" if c is None else re.sub(r"\s+", " ", str(c).replace("\xa0", " ")).strip()


def _tipo(titulo: str) -> str:
    t = titulo.lower()
    if "vigentes" in t:
        return "vigente"
    if "inicio del contrato" in t or "alta" in t:
        return "nuevo"
    return "sin_clasificar"


def _variable(titulo: str) -> str:
    t = titulo.lower()
    if "metro cuadrado" in t or "m2" in t:
        return "renta_eur_m2_util" if ("útil" in t or "util" in t) else "renta_eur_m2_construido"
    if "renta mensual" in t:
        return "renta_mensual_eur"
    if "fianzas" in t:
        return "n_fianzas"
    return "sin_clasificar"


def _nivel(codigo: str, nombre: str, hoja_titulo: str) -> str:
    if re.fullmatch(r"\d{5}", codigo):
        return "municipio"
    t = hoja_titulo.lower()
    if "barrio" in t or "distrito" in t or "zonificación" in t or "zonificacion" in t:
        return "zona"
    if "comarca" in t or "área funcional" in t or "area funcional" in t:
        return "territorio"
    if nombre in {"Euskadi", "Álava", "Gipuzkoa", "Bizkaia"}:
        return "territorio"
    return "agrupacion"


def _mapa_columnas(ws_rows: list[tuple]) -> dict[int, str]:
    """Columna -> periodo ('2016T1' o '2016'), usando la fila de años (propagada) y la de trimestres si existe."""
    fila_anio = None
    fila_trim = None
    for r in ws_rows[:6]:
        vals = [_txt(c) for c in r]
        if fila_anio is None and sum(v in ANIOS for v in vals) >= 1:
            fila_anio = vals
        elif fila_anio is not None and fila_trim is None and sum(v in TRIM for v in vals) >= 2:
            fila_trim = vals
    if fila_anio is None:
        return {}
    mapa, anio = {}, None
    fila_fecha = None   # bloque «vigentes a fecha» (fechas dd/mm/aaaa en la fila siguiente a la de años)
    fila_estad = None   # estadísticos del bloque vigente (Media, Mediana, Percentil 25, Percentil 75)
    for r in ws_rows[:7]:
        vals = [_txt(c) for c in r]
        if fila_fecha is None and sum(bool(re.fullmatch(r"\d{2}/\d{2}/\d{4}", v)) for v in vals) >= 1:
            fila_fecha = vals
        if "Mediana" in vals:
            fila_estad = vals
    ultima_fecha = None
    for j, v in enumerate(fila_anio):
        if j < 2:
            continue
        f = fila_fecha[j] if fila_fecha is not None and j < len(fila_fecha) else ""
        e = fila_estad[j] if fila_estad is not None and j < len(fila_estad) else ""
        e = "" if e.lower().startswith(("euros", "€", "m2", "m²")) else e
        if re.fullmatch(r"\d{2}/\d{2}/\d{4}", f):
            d, m, a = f.split("/")
            ultima_fecha = f"{a}-{m}-{d}"
            mapa[j] = f"vigente_{ultima_fecha}" + (f"_{e.lower().replace(' ', '')}" if e else "")
            anio = None
            continue
        if ultima_fecha and e:
            mapa[j] = f"vigente_{ultima_fecha}_{e.lower().replace(' ', '')}"
            continue
        if not v and not f and not e:
            ultima_fecha = None
        if v in ANIOS:
            anio = v
        if fila_trim is not None:
            q = fila_trim[j] if j < len(fila_trim) else ""
            if anio is not None and q in TRIM:
                mapa[j] = f"{anio}T{TRIM[q]}"
            elif not q:
                anio = None   # columna vacía: termina el bloque de años
        elif v in ANIOS:
            mapa[j] = anio
    return mapa


def _filas_hoja(ws, hoja: str, titulo: str, nombre_fichero: str) -> list[dict]:
    rows = [r for r in ws.iter_rows(values_only=True)]
    mapa = _mapa_columnas(rows)
    if not mapa:
        return []
    variable, tipo = _variable(titulo), _tipo(titulo)
    if variable == "sin_clasificar":
        return []
    salida, grupo = [], ""
    inicio_datos = max(i for i, r in enumerate(rows[:6]) if any(_txt(c) in ANIOS for c in r)) + 1
    for r in rows[inicio_datos:]:
        c0, c1 = _txt(r[0]), _txt(r[1]) if len(r) > 1 else ""
        if not c0 and not c1:
            continue
        if c0 and not c1 and not re.fullmatch(r"\d{5}", c0):
            grupo = c0 if c0 not in {"Euskadi"} else ""
            nombre, codigo = c0, ""
        elif re.fullmatch(r"\d{5}", c0):
            codigo, nombre = c0, c1
        else:
            codigo, nombre = "", c1
        if not nombre or nombre.lower().startswith(("fuente", "datos", "(*)", "nota", "renta", "número")):
            continue
        nivel = _nivel(codigo, nombre, titulo)
        for j, periodo in mapa.items():
            if j >= len(r) or not isinstance(r[j], (int, float)):
                continue
            tipo_j = "vigente" if periodo.startswith("vigente_") else tipo
            salida.append({"periodo": periodo, "nivel": nivel, "codigo_ine": codigo, "nombre": nombre,
                           "grupo": grupo, "tipo_contrato": tipo_j, "variable": variable,
                           "valor": r[j], "hoja": hoja, "libro": nombre_fichero})
    return salida


def _convertir() -> list[dict]:
    filas = []
    for nombre in FICHEROS:
        wb = openpyxl.load_workbook(DIR / nombre, read_only=True, data_only=True)
        for ws in wb.worksheets:
            if ws.title.lower().startswith(("índice", "indice", "composición")):
                continue
            primera = next(ws.iter_rows(values_only=True), ())
            titulo = next((_txt(c) for c in primera if _txt(c)), "")
            filas.extend(_filas_hoja(ws, ws.title, titulo, nombre))
    return filas


def _correspondencia(nombre: str) -> Path:
    """Extrae la hoja «Composición de zonas y distrito» (tabla de correspondencia nombre->código del propio libro)."""
    wb = openpyxl.load_workbook(DIR / nombre, read_only=True, data_only=True)
    ws = wb["Composición de zonas y distrito"]
    destino = DIR / "correspondencia_zonas_distrito.csv"
    import csv
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for r in ws.iter_rows(values_only=True):
            vals = [_txt(c) for c in r]
            if any(vals):
                w.writerow(vals)
    return destino


def _validar(filas: list[dict]) -> dict:
    """Controles: claves únicas y suma aritmética (Euskadi = Álava + Gipuzkoa + Bizkaia) en nº de fianzas por trimestre."""
    import collections
    claves = collections.Counter((f["periodo"], f["nivel"], f["codigo_ine"], f["nombre"], f["tipo_contrato"],
                                  f["variable"], f["hoja"]) for f in filas)
    duplicados = sum(v - 1 for v in claves.values() if v > 1)
    res = {"filas": len(filas), "claves_duplicadas": duplicados}
    for hoja in ("T1.1",):
        tot = collections.defaultdict(float)
        for f in filas:
            if f["hoja"] == hoja and f["variable"] == "n_fianzas" and f["nombre"] in {"Álava", "Gipuzkoa", "Bizkaia"}:
                tot[(f["periodo"], f["nombre"])] += f["valor"]
        eus = {f["periodo"]: f["valor"] for f in filas if f["hoja"] == hoja and f["nombre"] == "Euskadi"
               and f["variable"] == "n_fianzas"}
        suma = collections.defaultdict(float)
        for (p, n), v in tot.items():
            suma[p] += v
        difs = {p: (eus[p], suma[p]) for p in eus if p in suma and abs(eus[p] - suma[p]) > 0.5}
        res[f"cuadre_{hoja}_periodos_comparados"] = sum(1 for p in eus if p in suma)
        res[f"cuadre_{hoja}_discrepancias"] = len(difs)
    return res


def main(verificar: bool = False) -> int:
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            print("FALTA _manifest.csv")
            return 1
        import csv
        with open(man, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                ruta = Path(r["fichero"]).resolve() if Path(r["fichero"]).is_absolute() else \
                    (Path(__file__).resolve().parents[2] / r["fichero"])
                if not ruta.exists() or sha256(ruta) != r["sha256"]:
                    print(f"ERROR {r['fichero']}")
                    return 1
        print("OK emal: ficheros y sha256 coinciden con el manifiesto")
        return 0

    DIR.mkdir(parents=True, exist_ok=True)
    origen = {}
    for nombre in FICHEROS:
        origen[nombre] = descargar(BASE + nombre, DIR / nombre)
    filas = _convertir()
    import pandas as pd
    df = pd.DataFrame(filas)
    df = marcar_posterior_prereg(df, "periodo")
    df.to_csv(SALIDA, index=False, encoding="utf-8")
    ruta_csv = SALIDA
    if SALIDA.stat().st_size > 5 * 1024 * 1024:
        ruta_csv = SALIDA.with_suffix(".csv.gz")
        with open(SALIDA, "rb") as fi, gzip.open(ruta_csv, "wb") as fo:
            fo.write(fi.read())
        SALIDA.unlink()
    val = _validar(filas)
    print(val)
    for nombre, ruta in origen.items():
        registrar(FUENTE, ruta, BASE + nombre, EDICION, "2016-2025T4", "territorio/municipio/zona", LICENCIA, True,
                  notas=f"libro original: {FICHEROS[nombre]}")
    corr = _correspondencia("EMAL.-Barrios-Municipios.-2016-2025_es.xlsx")
    registrar(FUENTE, corr, BASE + "EMAL.-Barrios-Municipios.-2016-2025_es.xlsx", EDICION, "2016-2025T4",
              "zona", LICENCIA, True, notas="extracto de la hoja «Composición de zonas y distrito» del libro original")
    registrar(FUENTE, ruta_csv, BASE, EDICION, "2016-2025T4", "territorio/municipio/zona", LICENCIA, True,
              notas=f"CSV largo generado por src/v9/fetch_emal.py; validación: {val}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
