"""D2 v3: emancipación y tenencia desde Eurostat (API JSON-stat 1.0), anual, España y UE-27.

- ilc_lvps08: personas que viven con sus padres (o aportan/reciben renta del hogar), 16-34 años, por grupo de edad y sexo.
- ilc_lvho02: distribución de la población por régimen de tenencia (propiedad, hipoteca, alquiler a precio de mercado)
  y tipo de hogar (hhcomp). Es la tabla de tenencia por tipo de hogar (la edad del cabeza no está en ilc_lvho01/02).
Salida: data/raw/v3/eurostat_emancipacion_tenencia_v3.csv (formato largo). Originales JSON en data/raw/v3_orig/ (caché).
Los valores faltantes de Eurostat (':') quedan como NaN; no se imputan.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import utils_fetch as uf  # noqa: E402

API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{ds}?format=JSON&lang=EN&geo=ES&geo=EU27_2020&unit=PC"
DATASETS = {"ilc_lvps08": None, "ilc_lvho02": ["TOTAL", "OWN", "OWN_L", "OWN_NL", "RENT", "RENT_MKT"]}
DEST = uf.RAW / "v3" / "eurostat_emancipacion_tenencia_v3.csv"


def parsear(js: dict, ds: str, url: str, filtro: dict | None) -> list[dict]:
    ids = js["id"]
    sizes = js["size"]
    cats = {k: list(js["dimension"][k]["category"]["index"].keys()) for k in ids}
    vals = js["value"]
    out = []
    # strides para pasar de índice plano a posiciones por dimensión
    strides = {}
    acc = 1
    for k, s in zip(reversed(ids), reversed(sizes)):
        strides[k] = acc
        acc *= s
    for flat, v in ((int(i), x) for i, x in vals.items()):
        rec = {}
        for k in ids:
            pos = (flat // strides[k]) % js["dimension"][k]["category"]["index"].__len__()
            rec[k] = cats[k][pos]
        out.append(rec | {"valor": v})
    df = pd.DataFrame(out)
    if filtro:
        for k, allowed in filtro.items():
            if allowed is not None:
                df = df[df[k].isin(allowed)]
    df["ds"] = ds
    df["url"] = url
    return df


def main() -> None:
    if DEST.exists() and not uf.FORCE:
        print(f"[cache] {DEST.relative_to(uf.ROOT)}")
        return
    frames = []
    for ds, tenencias in DATASETS.items():
        url = API.format(ds=ds)
        orig = uf.RAW / "v3_orig" / f"eurostat_{ds}.json"
        uf.download(url, orig)
        import json
        js = json.loads(orig.read_text(encoding="utf-8"))
        filtro = {"tenure": tenencias, "rskpovth": ["TOTAL"]} if tenencias else None
        d = parsear(js, ds, url, filtro)
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    df["fecha"] = df["time"].astype(str) + "-01-01"
    df["periodo"] = df["time"].astype(str)
    df["fuente"] = "Eurostat (" + df["ds"] + ")"
    df["nivel"] = "PAIS"
    df["territorio"] = df["geo"].map({"ES": "España", "EU27_2020": "UE-27"})
    df["codigo"] = df["geo"]
    def serie(r):
        if r["ds"] == "ilc_lvps08":
            return f"EUROSTAT_ilc_lvps08_{r['geo']}_{r['age']}_{r['sex']}_con_padres"
        return f"EUROSTAT_ilc_lvho02_{r['geo']}_{r['hhcomp']}_{r['tenure']}"
    df["serie"] = df.apply(serie, axis=1)
    df["unidad"] = "porcentaje"
    dup = df.duplicated(["serie", "fecha"]).sum()
    if dup:
        raise ValueError(f"series duplicadas: {dup}")
    out = df[["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "territorio", "nivel", "codigo"]]
    out = out.sort_values(["serie", "fecha"])
    DEST.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(DEST, index=False)
    print(f"[ok] {DEST.relative_to(uf.ROOT)}: {len(out)} obs, {out['serie'].nunique()} series, "
          f"{out['fecha'].min()} -> {out['fecha'].max()}, NaN={int(out['valor'].isna().sum())}")


if __name__ == "__main__":
    main()
