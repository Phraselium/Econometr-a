"""V9-DATOS-COMPLETO, bloque 0 (inventario y actualización) y bloque 6 (VPO y suelo): ediciones vigentes de series que el
proyecto ya tenía. No se toca ningún fichero existente de data/raw: las ediciones nuevas se escriben en
data/raw/v9/actualizaciones/ y comparacion_ediciones.csv dice, por serie, el último periodo del proyecto y el actual.

- MIVAU, Boletín Online (sedal): suelo urbano (36400500, 36403000), vivienda protegida (calificaciones provisionales ≈
  iniciadas y definitivas ≈ terminadas; anual 1991- y mensual 2008-) y viviendas libres iniciadas y terminadas.
  Se reutiliza el parser verificado de src/fetch_mivau_v2.py (comprueba el título de cada tabla).
- Banco de España: crédito a hogares para vivienda (be1911, be1916), otra financiación (be0819) y crédito a
  actividades productivas, incluidas construcción y promoción inmobiliaria (be0418). CSV originales.
- Shocks monetarios del BCE (Jarociński y Karadi, actualización pública): solo comparación (v8 ya los tiene; sin
  licencia explícita, no se redistribuyen).
- Eurostat, costes de construcción (sts_copi_q): solo comparación con data/raw/eurostat_costes.csv.
"""
from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.v9.comun import CABECERAS, GZ_PANDAS, RAIZ, RAW9, descargar, registrar, sha256  # noqa: E402

FUENTE = "actualizaciones"
DIR = RAW9 / FUENTE
ORIG = DIR / "original"
LIC_MIVAU = "Ministerio de Vivienda (Boletín Online): reutilización con cita (aviso legal; Ley 37/2007)"
LIC_BDE = "Banco de España: reutilización con cita de la fuente"
BDE = "https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/{t}.csv"
JK = "https://raw.githubusercontent.com/marekjarocinski/jkshocks_update_ecb/main/shocks_ecb_mpd_me_m.csv"
EUROSTAT_COSTES = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_copi_q?geo=ES&indic_bt=COST"
                   "&cpa2_1=CPA_F41001_X_410014&unit=I21&s_adj=NSA&format=JSON")
COMPARACION = DIR / "comparacion_ediciones.csv"


def _ultimo_proyecto(rel: str, col: str = "periodo", filtro: str | None = None) -> str:
    d = pd.read_csv(RAIZ / rel, dtype=str, encoding_errors="replace")
    if filtro:
        d = d[d.url.str.contains(filtro, regex=False)]
    if "valor" in d:
        d = d[pd.to_numeric(d.valor, errors="coerce").notna()]
    return d[col].max()


def mivau(comp: list[dict]) -> None:
    import fetch_mivau_v2 as mv
    from utils_fetch import read_excel_any
    grupos = {"mivau_suelo_v9.csv.gz": ("data/raw/mivau_v2_suelo.csv", mv.TABLAS_SUELO),
              "mivau_protegida_v9.csv.gz": ("data/raw/mivau_v2_protegida.csv", mv.TABLAS_PROTEGIDA),
              "mivau_iniciadas_terminadas_v9.csv.gz": ("data/raw/mivau_v2_iniciadas_terminadas_prov.csv", mv.TABLAS_INICIADAS)}
    for salida, (previo, tablas) in grupos.items():
        partes = []
        for code, prefijo, tipo, unidad, esperado in tablas:
            url = f"{mv.BASE}/{code}.XLS"
            hojas = read_excel_any(descargar(url, ORIG / "mivau" / f"{code}.XLS"))
            hoja = next(iter(hojas.values()))
            d = mv.parse_tabla(hoja, code, tipo, prefijo, unidad, esperado)
            partes.append(d)
            comp.append({"fuente": "MIVAU", "tabla": code, "fichero_proyecto": previo,
                         "ultimo_periodo_proyecto": _ultimo_proyecto(previo, filtro=f"/{code}.XLS"),
                         "ultimo_periodo_actual": d.loc[d.valor.notna(), "periodo"].max(),
                         "primer_periodo_actual": d.periodo.min(), "fichero_v9": f"data/raw/v9/{FUENTE}/{salida}"})
        nuevos = [c for c in comp[-len(tablas):] if c["ultimo_periodo_actual"] != c["ultimo_periodo_proyecto"]]
        if not nuevos:   # misma edición que el proyecto: no se duplica
            for c in comp[-len(tablas):]:
                c["fichero_v9"] = "(sin copia: misma última observación que el proyecto)"
            continue
        df = pd.concat(partes, ignore_index=True)
        ruta = DIR / salida
        df.to_csv(ruta, index=False, compression=GZ_PANDAS)
        registrar(FUENTE, ruta, f"{mv.BASE}/<tabla>.XLS", edicion="Boletín Online MIVAU, edición vigente a 2026-10-14",
                  periodo=f"{df.periodo.min()}–{df.loc[df.valor.notna(), 'periodo'].max()}",
                  nivel_territorial="nacional, CCAA y provincia (nombre MIVAU; código INE en la correspondencia de v2)",
                  licencia=LIC_MIVAU, redistribuible=True, notas=f"tablas={','.join(t[0] for t in tablas)}; filas={len(df)}")


def _bde_ultimo(texto: str) -> tuple[str, str]:
    filas = [ln.split(",")[0].strip('"') for ln in texto.splitlines()]
    fechas = [f for f in filas if re.fullmatch(r"[A-Z]{3} \d{4}|\d{4}", f)]
    meses = {m: i + 1 for i, m in enumerate("ENE FEB MAR ABR MAY JUN JUL AGO SEP OCT NOV DIC".split())}

    def iso(f: str) -> str:
        return f"{f[4:]}-{meses[f[:3]]:02d}" if " " in f else f
    return (iso(fechas[0]), iso(fechas[-1])) if fechas else ("", "")


def bde(comp: list[dict]) -> None:
    previos = {"be0819": ("data/raw/bde_credito_finalidad.csv", "/be0819.csv"),
               "be1911": ("data/raw/bde_credito_finalidad.csv", "/be1911.csv"),
               "be1916": ("data/raw/bde_credito_finalidad.csv", "/be1916.csv"),
               "be0418": ("data/raw/v5/ca_bde_be0418_credito_actividad.csv", None)}
    for t, (previo, filtro) in previos.items():
        r = requests.get(BDE.format(t=t), headers=CABECERAS, timeout=120)
        r.raise_for_status()
        ruta = DIR / f"bde_{t}.csv"
        ruta.write_bytes(r.content)
        primero, ultimo = _bde_ultimo(r.content.decode("latin-1"))
        if filtro:
            up = _ultimo_proyecto(previo, filtro=filtro)
        else:
            up = pd.read_csv(RAIZ / previo, dtype=str).fecha.max()[:7]
        comp.append({"fuente": "Banco de España", "tabla": t, "fichero_proyecto": previo, "ultimo_periodo_proyecto": up,
                     "ultimo_periodo_actual": ultimo, "primer_periodo_actual": primero,
                     "fichero_v9": str(ruta.relative_to(RAIZ))})
        registrar(FUENTE, ruta, BDE.format(t=t), edicion="BdE, Boletín Estadístico, edición vigente a 2026-10-14",
                  periodo=f"{primero}–{ultimo}", nivel_territorial="nacional", licencia=LIC_BDE, redistribuible=True,
                  notas="CSV original del BdE (latin-1; fechas «MMM AAAA»)")


def comparaciones_externas(comp: list[dict]) -> None:
    r = requests.get(JK, headers=CABECERAS, timeout=120)
    r.raise_for_status()
    jk = pd.read_csv(io.StringIO(r.text))
    ult = f"{int(jk.iloc[-1, 0])}-{int(jk.iloc[-1, 1]):02d}"
    comp.append({"fuente": "Shocks BCE (Jarociński-Karadi, actualización)", "tabla": "shocks_ecb_mpd_me_m",
                 "fichero_proyecto": "data/raw/v8/jk_shocks_ecb_mensual.csv",
                 "ultimo_periodo_proyecto": _ultimo_proyecto("data/raw/v8/jk_shocks_ecb_mensual.csv"),
                 "ultimo_periodo_actual": ult, "primer_periodo_actual": f"{int(jk.iloc[0, 0])}-{int(jk.iloc[0, 1]):02d}",
                 "fichero_v9": "(sin copia: sin licencia explícita; v8 ya está al día)"})
    r = requests.get(EUROSTAT_COSTES, headers=CABECERAS, timeout=120)
    r.raise_for_status()
    per = sorted(r.json()["dimension"]["time"]["category"]["index"], key=lambda p: r.json()["dimension"]["time"]["category"]["index"][p])
    vals = r.json()["value"]
    idx = r.json()["dimension"]["time"]["category"]["index"]
    con = [p for p in per if str(idx[p]) in vals]
    comp.append({"fuente": "Eurostat (sts_copi_q, coste de construcción residencial)", "tabla": "sts_copi_q",
                 "fichero_proyecto": "data/raw/eurostat_costes.csv",
                 "ultimo_periodo_proyecto": _ultimo_proyecto("data/raw/eurostat_costes.csv"),
                 "ultimo_periodo_actual": con[-1], "primer_periodo_actual": con[0],
                 "fichero_v9": "(sin copia: ninguna novedad)" })


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            print("falta _manifest.csv"); return 1
        with open(man, encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                ruta = RAIZ / fila["fichero"]
                if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK actualizaciones"); return 0
    comp: list[dict] = []
    mivau(comp)
    bde(comp)
    comparaciones_externas(comp)
    for c in comp:
        c["novedad"] = "sí" if str(c["ultimo_periodo_actual"]) != str(c["ultimo_periodo_proyecto"]) else "no"
    pd.DataFrame(comp).to_csv(COMPARACION, index=False)
    registrar(FUENTE, COMPARACION, "(varias)", edicion="2026-10-14", periodo="", nivel_territorial="—",
              licencia="elaboración propia sobre fuentes públicas", redistribuible=True,
              notas="último periodo del proyecto frente a la edición vigente")
    print(pd.DataFrame(comp)[["tabla", "ultimo_periodo_proyecto", "ultimo_periodo_actual", "novedad"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
