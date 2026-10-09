"""Descarga series del INE (API JSON wstempus) a data/raw en formato largo.

Idempotente: si el CSV de destino ya existe no se vuelve a bajar (salvo FORCE=1).
Periodos: FK_Periodo 1-12 = mes, 19-22 = T1-T4, 28 = anual (verificado contra el
epoch de Fecha en Europe/Madrid). Fecha = primer día del periodo.
Serie = COD del INE; nombre = Nombre del INE; unidad = último segmento del Nombre
(texto), fk_unidad = código numérico original del INE.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import ROOT, cached, get, save  # noqa: E402

BASE = "https://servicios.ine.es/wstempus/js/ES"
NULT = 300
MAD = ZoneInfo("Europe/Madrid")
FALLIDAS = ROOT / "docs" / "fuentes_fallidas.md"

# FK_Periodo -> (mes de inicio, etiqueta de periodo)
QUARTER = {19: 1, 20: 4, 21: 7, 22: 10}


def period(fk: int, anyo: int) -> tuple[dt.date, str]:
    if 1 <= fk <= 12:
        return dt.date(anyo, fk, 1), f"{anyo}M{fk:02d}"
    if fk in QUARTER:
        q = {1: 1, 4: 2, 7: 3, 10: 4}[QUARTER[fk]]
        return dt.date(anyo, QUARTER[fk], 1), f"{anyo}T{q}"
    if fk == 28:
        return dt.date(anyo, 1, 1), f"{anyo}"
    raise ValueError(f"FK_Periodo no reconocido: {fk}")


def unidad_texto(nombre: str) -> str:
    partes = [p.strip() for p in nombre.strip().rstrip(".").split(".") if p.strip()]
    return partes[-1] if partes else ""


def series_to_rows(serie: dict, url: str, tabla: str | None) -> tuple[list[dict], int]:
    """Convierte una serie INE a filas largas. Devuelve (filas, n_desajustes_fecha)."""
    rows, mismatch = [], 0
    unidad = unidad_texto(serie["Nombre"])
    for x in serie.get("Data") or []:
        d, lab = period(int(x["FK_Periodo"]), int(x["Anyo"]))
        loc = dt.datetime.fromtimestamp(x["Fecha"] / 1000, tz=MAD)
        if (loc.year, loc.month) != (d.year, d.month):
            mismatch += 1
        valor = None if x.get("Secreto") else x.get("Valor")
        rows.append({
            "fecha": d.isoformat(), "periodo": lab, "serie": serie["COD"],
            "valor": valor, "unidad": unidad, "fuente": "INE", "url": url,
            "nombre": serie["Nombre"].strip(), "fk_unidad": serie.get("FK_Unidad"),
            "tabla": tabla,
        })
    return rows, mismatch


def probe(url: str) -> str:
    """Petición pequeña (nult=3) para verificar el endpoint y la última fecha."""
    d = get(url, params={"nult": 3}, timeout=120)
    ser = d if isinstance(d, list) else [d]
    last = [x for s in ser for x in (s.get("Data") or [])]
    if not last:
        return "sin datos"
    x = max(last, key=lambda z: (int(z["Anyo"]), int(z["FK_Periodo"])))
    return f"{x['Anyo']} FK_Periodo={x['FK_Periodo']}"


def fetch_group(name: str, fuente_txt: str, specs: list[tuple[str, str, str | None]]) -> None:
    """specs: lista de (kind, id, filtro_regex_o_None). kind = 'tabla' | 'serie'."""
    if cached(name):
        return
    print(f"[get] {name}")
    all_rows, mism = [], 0
    for kind, ident, pat in specs:
        if kind == "tabla":
            url = f"{BASE}/DATOS_TABLA/{ident}"
            print(f"  verificando DATOS_TABLA/{ident}: {probe(url)}")
            payload = get(url, params={"nult": NULT}, timeout=600)
            series = payload if isinstance(payload, list) else [payload]
            tabla = ident
        else:
            url = f"{BASE}/DATOS_SERIE/{ident}"
            print(f"  verificando DATOS_SERIE/{ident}: {probe(url)}")
            series = [get(url, params={"nult": NULT}, timeout=600)]
            tabla = None
        n_sel = 0
        for s in series:
            if pat and not re.search(pat, s["Nombre"], re.I):
                continue
            n_sel += 1
            rows, m = series_to_rows(s, f"{url}?nult={NULT}", tabla)
            all_rows.extend(rows)
            mism += m
        print(f"  {kind} {ident}: {n_sel} series seleccionadas")
    if not all_rows:
        raise RuntimeError(f"{name}: ninguna serie seleccionada")
    if mism:
        print(f"  [aviso] {mism} observaciones con Fecha epoch distinta al periodo (ver fetch_ine.py)")
    df = pd.DataFrame(all_rows)
    save(df, name, fuente_txt)


def registrar_fallo(nombre: str, url: str, error: str) -> None:
    FALLIDAS.parent.mkdir(parents=True, exist_ok=True)
    nueva = not FALLIDAS.exists()
    with FALLIDAS.open("a", encoding="utf-8") as f:
        if nueva:
            f.write("# Fuentes fallidas\n\n| fecha UTC | archivo | URL probada | error | alternativa |\n|---|---|---|---|---|\n")
        ahora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        f.write(f"| {ahora} | {nombre} | {url} | {error[:200]} | pendiente de revisión |\n")


# (archivo, [(tipo, id, filtro)])
JOBS = [
    ("ine_ipv_25171.csv", [("tabla", "25171", None)]),
    ("ine_epa_ocupados.csv", [("serie", "EPA387796", None)]),
    ("ine_epa_ocupados_ccaa.csv", [("tabla", "65302", None)]),
    ("ine_ecp_nacional.csv", [("serie", "ECP320", None), ("serie", "ECP701", None)]),
    ("ine_ecp_56936.csv", [("tabla", "56936", None)]),
    ("ine_ecp_59585.csv", [("tabla", "59585", None)]),
    ("ine_hogares_60131.csv", [("tabla", "60131", None)]),
    ("ine_migraciones_nacionalidad.csv", [("tabla", "59011", None)]),
    ("ine_migraciones_ccaa_nacionalidad.csv", [("tabla", "59013", None)]),
    ("ine_migraciones_total_anual.csv", [("tabla", "69687", None)]),
    ("ine_etdp_compraventas.csv", [("tabla", "6150", None)]),
    ("ine_ipva_nacional_ccaa.csv", [("tabla", "59056", None)]),
    ("ine_ipva_municipal.csv", [("tabla", "59060", None)]),
    ("ine_ipc_alquiler.csv", [("serie", "IPC292307", None), ("tabla", "76137", r"Alquiler de vivienda")]),
    ("ine_cnt_pib_oferta_corrientes.csv", [("tabla", "67821", None)]),
    ("ine_cnt_pib_oferta_volumen.csv", [("tabla", "67822", None)]),
    ("ine_cnt_demanda_corrientes.csv", [("tabla", "67823", None)]),
    ("ine_cnt_demanda_volumen.csv", [("tabla", "67824", None)]),
    ("ine_cnt_renta_disponible.csv", [("tabla", "80333", None)]),
]


def main() -> int:
    errores = 0
    for nombre, specs in JOBS:
        try:
            fetch_group(nombre, "INE", specs)
        except Exception as e:  # noqa: BLE001
            errores += 1
            url = f"{BASE}/DATOS_TABLA/" + ",".join(i for _, i, _ in specs)
            print(f"[fallo] {nombre}: {e}")
            registrar_fallo(nombre, url, str(e))
    print(f"terminado: {len(JOBS) - errores} OK, {errores} fallidos")
    return 0 if errores == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
