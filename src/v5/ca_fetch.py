"""CA · Descargas (con red, fuera de make) a data/raw/v5/.

Eurostat: ilc_lvho07a, ilc_lvho05a, yth_demo_030, ilc_lvho02, demo_gind.
BdE: boletín estadístico be0418 (crédito por actividad productiva, saldos, mensual).
BCE: encuesta de préstamos bancarios (BLS) de España (EPB), series seleccionadas.
Salidas: data/raw/v5/ca_*.csv (formato largo). Los fallos van a docs/v5/fuentes_fallidas.md (sección CA).
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import itertools
import json
import subprocess
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DEST = RAIZ / "data" / "raw" / "v5"
DEST.mkdir(parents=True, exist_ok=True)
ES = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
GEOS = ("EU27_2020,AT,BE,BG,HR,CY,CZ,DK,EE,FI,FR,DE,EL,HU,IE,IT,LV,LT,LU,MT,NL,PL,PT,RO,SK,SI,ES,SE,"
        "NO,IS,CH,UK").split(",")


def curl(url: str) -> bytes:
    return subprocess.run(["curl", "-sS", "-L", "-m", "120", url], capture_output=True).stdout


def jsonstat(url: str) -> pd.DataFrame:
    j = json.loads(curl(url))
    ids, size = j["id"], j["size"]
    idx = {d: list(j["dimension"][d]["category"]["index"].keys()) for d in ids}
    val = j["value"]
    rows = []
    for k, combo in enumerate(itertools.product(*[range(s) for s in size])):
        v = val.get(str(k)) if isinstance(val, dict) else val[k]
        if v is None:
            continue
        r = {d: idx[d][i] for d, i in zip(ids, combo)}
        r["valor"] = v
        rows.append(r)
    df = pd.DataFrame(rows)
    df["actualizado"] = j.get("updated")
    return df


def eurostat() -> None:
    g = "&".join(f"geo={x}" for x in GEOS)
    pet = {
        "ilc_lvho07a": "unit=PC&age=TOTAL&sex=T&rskpovth=TOTAL",
        "ilc_lvho05a": "unit=PC&age=TOTAL&sex=T&rskpovth=TOTAL",
        "yth_demo_030": "",
        "ilc_lvho02": "unit=PC&hhcomp=TOTAL&rskpovth=TOTAL&tenure=OWN&tenure=RENT&tenure=RENT_MKT&tenure=RENT_FR&tenure=OWN_L&tenure=OWN_NL",
        "demo_gind": "indic_de=GROWRT&indic_de=CNMIGRATRT&indic_de=NATGROWRT",
    }
    for ds, filt in pet.items():
        url = f"{ES}/{ds}?format=JSON&lang=EN&{g}" + (f"&{filt}" if filt else "")
        try:
            df = jsonstat(url)
            if df.empty:
                raise ValueError("vacío")
        except Exception as e:  # noqa: BLE001
            print(ds, "ERROR", e)
            continue
        df.insert(0, "dataset", ds)
        df["url"] = url
        df["descargado"] = dt.date.today().isoformat()
        df.to_csv(DEST / f"ca_eurostat_{ds}.csv", index=False)
        print(ds, df.shape, list(df.columns))


def bde() -> None:
    url = "https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/be0418.csv"
    raw = curl(url).decode("latin1")
    rows = list(csv.reader(io.StringIO(raw)))
    cod, desc = rows[0], [r for r in rows if r[0].startswith("DESCRIPCI")][0]
    out = []
    mes = {m: i + 1 for i, m in enumerate("ENE FEB MAR ABR MAY JUN JUL AGO SEP OCT NOV DIC".split())}
    for r in rows:
        p = r[0].split()
        if len(p) == 2 and p[0] in mes and p[1].isdigit():
            for i in range(1, len(r)):
                if cod[i] in ("D_MEE61000", "D_MEE61010", "D_MEE61013", "D_MEADU103", "D_MEADU109") \
                        and r[i] not in ("_", ""):
                    out.append({"fecha": f"{p[1]}-{mes[p[0]]:02d}-01", "serie": cod[i], "valor": float(r[i]),
                                "unidad": "Miles de euros", "titulo": desc[i], "fuente": "BdE be0418", "url": url,
                                "descargado": dt.date.today().isoformat()})
    pd.DataFrame(out).to_csv(DEST / "ca_bde_be0418_credito_actividad.csv", index=False)
    print("bde", len(out))


def bls() -> None:
    ks = ["CP.H.H.B3.ST.S.FNET", "CP.H.H.B3.TC.S.FNET", "CP.E.Z.B3.ST.S.FNET", "CP.E.Z.B3.TC.S.FNET",
          "DR.H.H.B3.ZZ.D.FNET", "DR.E.Z.B3.ZZ.D.FNET"]
    parts = []
    for k in ks:
        u = f"https://data-api.ecb.europa.eu/service/data/BLS/Q.ES.ALL.{k}?format=csvdata"
        b = curl(u).decode("utf8", "ignore")
        if b.startswith("KEY"):
            parts.append(pd.read_csv(io.StringIO(b))[["KEY", "TIME_PERIOD", "OBS_VALUE"]])
        else:
            print("BLS fallo", k)
    if parts:
        d = pd.concat(parts)
        d["fuente"] = "BCE BLS (EPB) España"
        d["descargado"] = dt.date.today().isoformat()
        d.to_csv(DEST / "ca_ecb_bls_es.csv", index=False)
        print("bls", d.shape)


if __name__ == "__main__":
    eurostat()
    bde()
    bls()
