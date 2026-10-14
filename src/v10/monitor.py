"""V10-B5 · monitor: descarga las series abiertas que cambian con frecuencia y resume su último dato y su variación.

Uso:
  python3 src/v10/monitor.py            descarga (con red) y escribe data/raw/v10/monitor/*.csv y el resumen
  python3 src/v10/monitor.py --sin-red  rehace solo el resumen desde data/raw/v10/monitor (lo usa `make web`)
Salidas: data/raw/v10/monitor/<id>.csv (serie larga: periodo, valor) y output/v10/monitor/monitor.json.

Reglas: solo descriptivo; la variación es interanual (mismo periodo del año anterior). Las filas desde 2026T3 llevan
`posterior_prereg` = True: se muestran como dato y no se comparan con ninguna predicción congelada (evaluate_v7 y
evaluate_v8 son los únicos que pueden hacerlo, en su fecha). El flujo mensual (.github/workflows/actualizar.yml)
ejecuta este script, reconstruye base, atlas, figuras y web, pasa `make check` y abre un pull request; nunca publica
sin revisión.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import sys
from pathlib import Path

import pandas as pd
import requests

RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw" / "v10" / "monitor"
OUT = RAIZ / "output" / "v10" / "monitor"
CAB = {"User-Agent": "vivienda-espana-evidencia/10 (monitor; investigacion independiente)"}
INE = "https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{cod}?nult=36"
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{q}"
BCE = "https://data-api.ecb.europa.eu/service/data/MIR/{clave}?format=csvdata&startPeriod=2022-01"
GVA = "https://dadesobertes.gva.es/api/3/action/package_show?id=viv-reg-fia-{anio}"

# id -> (etiqueta, origen, código, unidad, capa, fuente)
SERIES = {
    "ipv_general": ("Índice de precios de vivienda (IPV), general", "ine", "IPV1209", "índice", "C1",
                    "INE, IPV (serie IPV1209)"),
    "ipc_alquiler": ("IPC de alquiler de vivienda, índice", "ine", "IPC290887", "índice", "C4", "INE, IPC (IPC290887)"),
    "compraventas_libre": ("Compraventas de vivienda libre", "ine", "ETDP1823", "operaciones", "C4", "INE, ETDP (ETDP1823)"),
    "compraventas_protegida": ("Compraventas de vivienda protegida", "ine", "ETDP1822", "operaciones", "C4", "INE, ETDP (ETDP1822)"),
    "hipotecas_viviendas": ("Hipotecas sobre viviendas, número", "ine", "HPT34618", "hipotecas", "C4", "INE, hipotecas (HPT34618)"),
    "vut_viviendas": ("Viviendas turísticas (medición experimental)", "ine", "VTE71", "viviendas", "C4", "INE, VUT (VTE71)"),
    "poblacion": ("Población residente", "ine", "ECP320", "personas", "C4", "INE, ECP (ECP320)"),
    "hpi_eurostat": ("Índice de precios de vivienda (Eurostat), España", "eurostat",
                     "prc_hpi_q?geo=ES&purchase=TOTAL&unit=I15_Q", "índice 2015=100", "C1", "Eurostat, prc_hpi_q"),
    "plataformas_noches": ("Noches en alojamientos reservados por plataformas, España", "eurostat",
                           "tour_ce_omr?geo=ES&c_resid=TOTAL&unit=NR", "noches", "C4", "Eurostat, tour_ce_omr"),
    "tipo_hip_variable": ("Tipo de nuevas hipotecas, variable o fijado ≤1 año", "bce", "M.ES.B.A2C.F.R.A.2250.EUR.N",
                          "% anual", "C4", "BCE, MIR"),
    "tipo_hip_tae": ("Coste total de las nuevas hipotecas (TAE)", "bce", "M.ES.B.A2C.AM.R.A.2250.EUR.N", "% anual",
                     "C4", "BCE, MIR"),
    "fianzas_gva": ("Fianzas de alquiler depositadas en la GVA", "gva", "", "fianzas", "C4",
                    "Generalitat Valenciana, datos abiertos (CC BY 4.0)"),
}
MESES_INE = {1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 7: "07", 8: "08", 9: "09", 10: "10", 11: "11", 12: "12"}


def ine(cod: str) -> pd.DataFrame:
    d = requests.get(INE.format(cod=cod), headers=CAB, timeout=120).json()
    filas = []
    for x in d.get("Data", []):
        f = dt.datetime.fromtimestamp(x["Fecha"] / 1000, dt.timezone.utc) + dt.timedelta(hours=12)
        per = x.get("FK_Periodo")
        if per in (19, 20, 21, 22):          # trimestres
            p = f"{x['Anyo']}T{per - 18}"
        elif per in MESES_INE:
            p = f"{x['Anyo']}-{MESES_INE[per]}"
        elif per == 28:
            p = str(x["Anyo"])
        else:
            p = f.strftime("%Y-%m")
        if x.get("Valor") is not None:
            filas.append({"periodo": p, "valor": float(x["Valor"])})
    return pd.DataFrame(filas)


def eurostat(q: str) -> pd.DataFrame:
    sep = "&" if "?" in q else "?"
    d = requests.get(EUROSTAT.format(q=q) + sep + "format=JSON&lang=EN", headers=CAB, timeout=120).json()
    idx = d["dimension"]["time"]["category"]["index"]
    inv = {v: k for k, v in idx.items()}
    filas = [{"periodo": inv[int(k)].replace("-Q", "T"), "valor": float(v)} for k, v in d["value"].items() if int(k) in inv]
    return pd.DataFrame(filas).sort_values("periodo")


def bce(clave: str) -> pd.DataFrame:
    r = requests.get(BCE.format(clave=clave), headers=CAB, timeout=120)
    r.raise_for_status()
    d = pd.read_csv(io.StringIO(r.text))
    return pd.DataFrame({"periodo": d.TIME_PERIOD, "valor": pd.to_numeric(d.OBS_VALUE, errors="coerce")}).dropna()


def gva() -> pd.DataFrame:
    filas = []
    for anio in range(dt.date.today().year - 1, dt.date.today().year + 1):
        p = requests.get(GVA.format(anio=anio), headers=CAB, timeout=120).json()
        if not p.get("success"):
            continue
        rec = next((r for r in p["result"]["resources"] if r.get("format", "").upper() == "CSV"), None)
        if rec is None:
            continue
        r = requests.get(rec["url"], headers=CAB, timeout=300)
        d = pd.read_csv(io.BytesIO(r.content), sep=None, engine="python", dtype=str)
        col_mes = next((c for c in d.columns if "mes" in c.lower()), None)
        if col_mes is None:
            filas.append({"periodo": str(anio), "valor": float(len(d))})
        else:
            for mes, n in d.groupby(col_mes).size().items():
                filas.append({"periodo": f"{anio}-{int(float(mes)):02d}", "valor": float(n)})
    return pd.DataFrame(filas)


def descargar() -> list[str]:
    import time
    RAW.mkdir(parents=True, exist_ok=True)
    fallos = []
    for ident, (_, origen, cod, *_rest) in SERIES.items():
        for intento in range(3):
            try:
                d = {"ine": ine, "eurostat": eurostat, "bce": bce}.get(origen, lambda c: gva())(cod)
                if d.empty:
                    raise RuntimeError("sin datos")
                d.to_csv(RAW / f"{ident}.csv", index=False)
                break
            except Exception as e:  # noqa: BLE001
                if intento == 2:
                    fallos.append(f"{ident}: {e}")
                time.sleep(4 * (intento + 1))
    return fallos


def fin_periodo(p: str) -> str:
    """Último mes del periodo (AAAA-MM): un periodo es posterior al pre-registro si incluye algún mes desde 2026-07."""
    if "T" in p:
        a, t = p.split("T")
        return f"{a}-{int(t) * 3:02d}"
    return p[:7] if len(p) >= 7 else f"{p}-12"


def anterior(p: str) -> str:
    if "T" in p:
        a, t = p.split("T")
        return f"{int(a) - 1}T{t}"
    if len(p) == 7:
        return f"{int(p[:4]) - 1}{p[4:]}"
    return str(int(p) - 1)


def resumen(fallos: list[str] | None = None) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    filas = []
    for ident, (etq, _, _, unidad, capa, fuente) in SERIES.items():
        ruta = RAW / f"{ident}.csv"
        if not ruta.exists():
            continue
        d = pd.read_csv(ruta, dtype={"periodo": str}).dropna().sort_values("periodo")
        if d.empty:
            continue
        ult = d.iloc[-1]
        prev = d[d.periodo == anterior(ult.periodo)]
        en_puntos = unidad.startswith("%")
        parcial = len(ult.periodo) == 4 and int(ult.periodo) >= dt.date.today().year   # año en curso: acumulado parcial
        if parcial or prev.empty or (not en_puntos and prev.valor.iloc[0] == 0):
            var = None
        else:
            var = ult.valor - prev.valor.iloc[0] if en_puntos else 100 * (ult.valor / prev.valor.iloc[0] - 1)
        filas.append({"id": ident, "etiqueta": etq, "territorio": "España" if ident != "fianzas_gva" else "Comunitat Valenciana",
                      "periodo": ult.periodo + (" (acumulado parcial del año)" if parcial else ""), "valor": f"{ult.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                      "variacion": "—" if var is None else (f"{var:+.2f} puntos interanual" if en_puntos
                                                             else f"{var:+.1f} % interanual").replace(".", ","),
                      "unidad": unidad, "capa": capa, "fuente": fuente,
                      "posterior_prereg": fin_periodo(ult.periodo) >= "2026-07"})
    previo = json.loads((OUT / "monitor.json").read_text(encoding="utf-8")) if (OUT / "monitor.json").exists() else {}
    fecha = dt.date.today().isoformat() if fallos is not None else previo.get("fecha", "")   # sin red: se conserva
    res = {"fecha": fecha, "n": len(filas), "filas": filas, "fallos": fallos or []}
    (OUT / "monitor.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(OUT / "monitor.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()) if filas else ["id"])
        w.writeheader()
        w.writerows(filas)
    return res


def main(sin_red: bool = False) -> int:
    fallos = None if sin_red else descargar()
    r = resumen(fallos)
    print(json.dumps({"series": r["n"], "fallos": r["fallos"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main("--sin-red" in sys.argv))
