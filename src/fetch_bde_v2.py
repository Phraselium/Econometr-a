"""Banco de España (v2): crédito a hogares por finalidad y tipos de nuevas hipotecas.

Reutiliza el parser de tablas anchas de src/fetch_bde.py (_parse_wide) y el formato
CSV largo de utils_fetch.save(). Cada tabla del BdE se descarga una vez (caché por
archivo de salida; FORCE=1 para rebajar).

Tablas (boletín estadístico, compartido/datos/csv/beNNNN.csv):
- be0819  OIFM, balance UEM. Préstamos y créditos a hogares por finalidad (SALDOS, mensual).
          Columnas usadas: total hogares, crédito vivienda (DF_MESNAA22A1), consumo (DF_MESNAA21A1),
          consumo y resto (DF_MESNAA25A1), resto excepto actividades productivas (DF_MESNAA26A1),
          adquisición de vivienda por funciones de gasto (D_MEE62100), rehabilitación (D_MEE62600),
          consumo duradero (D_MEE62200).
- be1911  Nuevas operaciones, importes totales estimados, hogares (vivienda, consumo, otros fines).
- be1916  Saldos vivos, importes totales estimados, hogares (vivienda, consumo y otros).
- be1903  TEDR (tipo de interés efectivo) de nuevas operaciones, hogares (vivienda, consumo, otros).
- be1906  TAE de nuevas operaciones, hogares (vivienda, consumo, otros fines).

Ejecutar desde la raíz del repo:  python3 src/fetch_bde_v2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_bde import BASE, _parse_wide  # noqa: E402
from utils_fetch import HEADERS, ROOT, cached, get, save  # noqa: E402

FUENTE = "BdE"
FALLIDAS = ROOT / "docs" / "v2" / "fallidas" / "ue_bde.md"

CREDITO = "bde_credito_finalidad.csv"
TIPOS = "bde_tipos_hipotecas_nuevas.csv"

# (archivo de salida, [(tabla, [(código de serie, descripción corta)])])
SOURCES = [
    (CREDITO, [
        ("be0819.csv", [
            ("DF_MESNAA20A1U62251Z01E", "Saldo préstamos y créditos a hogares (total)"),
            ("DF_MESNAA22A1U62251Z01E", "Saldo crédito vivienda a hogares"),
            ("DF_MESNAA21A1U62251Z01E", "Saldo crédito al consumo a hogares"),
            ("DF_MESNAA25A1U62251Z01E", "Saldo crédito al consumo y resto a hogares"),
            ("DF_MESNAA26A1U62251Z01E", "Saldo resto de crédito a hogares excepto actividades productivas"),
            ("D_MEE62100", "Saldo otra financiación hogares, adquisición vivienda (total)"),
            ("D_MEE62600", "Saldo otra financiación hogares, rehabilitación vivienda"),
            ("D_MEE62200", "Saldo otra financiación hogares, consumo duradero"),
        ]),
        ("be1911.csv", [
            ("DN_1TI2TIE96", "Nuevas operaciones (importe) crédito a la vivienda, hogares"),
            ("DN_1TI2TIE98", "Nuevas operaciones (importe) crédito vivienda excl. renegociaciones"),
            ("DN_1TI2TIE99", "Nuevas operaciones (importe) crédito al consumo, hogares"),
            ("DN_1TI2TIE102", "Nuevas operaciones (importe) crédito a otros fines, hogares"),
        ]),
        ("be1916.csv", [
            ("DF_MESN7A22A1U22250EURE", "Saldo vivo (importe) crédito a la vivienda, hogares"),
            ("DF_MESN7A24A1U22250EURE", "Saldo vivo (importe) crédito al consumo y otros, hogares"),
        ]),
    ]),
    (TIPOS, [
        ("be1903.csv", [
            ("DN_1TI2T0135", "TEDR nuevas operaciones crédito a la vivienda, hogares (%)"),
            ("DN_1TI2T0138", "TEDR nuevas operaciones crédito al consumo, hogares (%)"),
            ("DN_1TI2T1141", "TEDR nuevas operaciones crédito a otros fines, hogares (%)"),
        ]),
        ("be1906.csv", [
            ("DN_1TI2T0082", "TAE nuevas operaciones crédito a la vivienda, hogares (%)"),
            ("DN_1TI2T0087", "TAE nuevas operaciones crédito al consumo, hogares (%)"),
            ("DN_1TI2T0091", "TAE nuevas operaciones crédito para otros fines, hogares (%)"),
        ]),
    ]),
]


def _probe(url: str) -> str:
    """Petición pequeña (Range 0-1999): comprueba que el endpoint responde y el formato es el esperado."""
    r = requests.get(url, headers={**HEADERS, "Range": "bytes=0-1999"}, timeout=60)
    r.raise_for_status()
    head = r.content.decode("latin-1", errors="replace")
    if "CÓDIGO DE LA SERIE" not in head and "CODIGO DE LA SERIE" not in head:
        raise RuntimeError(f"{url}: formato inesperado en la cabecera")
    return "OK"


def _fetch_tabla(tabla: str, wanted: list[tuple[str, str]]) -> pd.DataFrame:
    url = f"{BASE}/{tabla}"
    _probe(url)
    text = get(url, as_json=False)
    if "CÓDIGO DE LA SERIE" not in text and "CODIGO DE LA SERIE" not in text:
        raise RuntimeError(f"{url}: formato inesperado (no contiene 'CÓDIGO DE LA SERIE')")
    df = _parse_wide(text, url, wanted)
    df["territorio"] = "España"
    df["dataset"] = tabla.replace(".csv", "")
    return df


def _registrar_fallo(nombre: str, errores: list[tuple[str, str]]) -> None:
    FALLIDAS.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not FALLIDAS.exists()
    with FALLIDAS.open("a", encoding="utf-8") as f:
        if nuevo:
            f.write("# Fallos de descarga v2: UE (Eurostat, OCDE, BIS, BCE) y Banco de España\n\n")
        f.write(f"## {nombre}\n")
        for url, err in errores:
            f.write(f"- URL probada: {url}\n  - Error: {err}\n")
        f.write("\n")


def procesar(nombre: str, tablas) -> bool:
    if cached(nombre):
        return True
    partes, errores = [], []
    for tabla, wanted in tablas:
        try:
            partes.append(_fetch_tabla(tabla, wanted))
            print(f"[ok] {nombre} <- {tabla}: {len(wanted)} series")
        except Exception as e:  # noqa: BLE001
            errores.append((f"{BASE}/{tabla}", str(e)))
            print(f"[fallo] {nombre} <- {tabla}: {e}")
    if not partes:
        _registrar_fallo(nombre, errores)
        return False
    df = pd.concat(partes, ignore_index=True)
    df["fuente"] = FUENTE
    save(df, nombre, FUENTE)
    if errores:
        _registrar_fallo(nombre + " (parcial)", errores)
    return True


if __name__ == "__main__":
    resultados = {n: procesar(n, t) for n, t in SOURCES}
    print("[resumen]", {k: ("OK" if v else "FALLO") for k, v in resultados.items()})
