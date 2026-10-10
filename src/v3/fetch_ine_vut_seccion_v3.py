"""INE · Medición del número de viviendas turísticas (estadística experimental) por SECCIÓN y DISTRITO censal.

Las tablas JAXI del INE (39363-39366) llegan solo a municipio. El nivel de sección y distrito se publica en
los servicios ArcGIS del INE (www.ine.es/servergis/rest/services/Hosted/Viviendas_turísticas_<oleada>/FeatureServer,
capa 2 = distritos, capa 3 = secciones). Se consultan solo atributos (sin geometría), paginando.
Si existe una versión «_V1» de la oleada (revisada), se usa esa. Caché por oleada en data/raw/v3_orig/vut_seccion/.
Salida: data/raw/v3/ine_v3_vut_seccion.csv.gz (formato largo).
"""
from __future__ import annotations

import json
import os
import sys
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
CACHE = RAIZ / "data" / "raw" / "v3_orig" / "vut_seccion"
SALIDA = RAIZ / "data" / "raw" / "v3" / "ine_v3_vut_seccion.csv.gz"
BASE = "https://www.ine.es/servergis/rest/services"
NIVELES = {"distrito": "Distritos", "seccion": "Secciones"}   # la capa se localiza por nombre (los id cambian)


def _get(url: str) -> dict:
    for intento in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:  # noqa: BLE001
            if intento == 3:
                raise
            time.sleep(2 ** (intento + 1))
    return {}


def servicios(prefijo: str = "viviendas_tur") -> dict[str, str]:
    """oleada -> nombre de servicio (prefiere la versión _V1). Los servicios «Porcentaje_...» traen las
    mismas variables y sirven de respaldo cuando el de «Viviendas_...» está vacío (2022M08)."""
    d = _get(f"{BASE}/Hosted?f=json")
    out: dict[str, str] = {}
    for s in d.get("services", []):
        n = s["name"].split("/", 1)[1]
        if s["type"] != "FeatureServer" or not n.lower().startswith(prefijo):
            continue
        ole = "".join(ch for ch in n if ch.isalnum())
        ole = ole[ole.find("20"):ole.find("20") + 7]          # p. ej. 2024M08
        if len(ole) != 7 or "M" not in ole:
            continue
        if ole not in out or n.upper().endswith("_V1"):
            out[ole] = n
    return dict(sorted(out.items()))


def capa_de(servicio: str, nivel: str) -> int | None:
    d = _get(f"{BASE}/Hosted/{urllib.parse.quote(servicio)}/FeatureServer?f=json")
    for lay in d.get("layers", []):
        if NIVELES[nivel][:6] in lay["name"] and "ontorno" not in lay["name"]:
            return int(lay["id"])
    return None


def _normaliza(a: dict, nivel: str) -> dict:
    """Los nombres de campo cambian entre oleadas (codigo/código, vivienda_turistica/viviendas_turísticas...)."""
    k = {re.sub(r"[^a-z0-9_]", "", unicodedata.normalize("NFKD", c).encode("ascii", "ignore").decode().lower()): v
         for c, v in a.items()}
    cod = k.get("cusec") if nivel == "seccion" else k.get("cudis")
    if not cod:
        cod = k.get("codigo")

    def primero(patron):
        for c, v in k.items():
            if re.fullmatch(patron, c):
                return v
        return None
    out = {"codigo": cod, "vivienda_turistica": primero(r"viviendas?_turisticas?"),
           "plazas": primero(r"plazas(_en_viviendas?_turisticas?)?"),
           "porcentaje_vivienda_turistica": primero(r"porcentaje_viviendas?_turisticas?"),
           "nota1": k.get("nota1", k.get("nota"))}
    # oleada 2021M02: campos genéricos dato1..dato4 con su unidad en unidad1..unidad4
    if out["vivienda_turistica"] is None and "dato1" in k:
        etiquetas = {str(k.get(f"unidad{i}", "")).lower(): k.get(f"dato{i}") for i in range(1, 5)}
        out["vivienda_turistica"] = etiquetas.get("viviendas")
        out["plazas"] = k.get("dato2") if str(k.get("unidad2", "")).lower() == "plazas" else None
        out["porcentaje_vivienda_turistica"] = etiquetas.get("porcentaje")
    return out


def descargar_capa(servicio: str, capa: int, nivel: str) -> list[dict]:
    url = f"{BASE}/Hosted/{urllib.parse.quote(servicio)}/FeatureServer/{capa}/query"
    filas, off = [], 0
    while True:
        q = urllib.parse.urlencode({"where": "1=1", "outFields": "*", "returnGeometry": "false",
                                    "resultOffset": off, "resultRecordCount": 2000, "f": "json"})
        d = _get(f"{url}?{q}")
        feats = [_normaliza(f["attributes"], nivel) for f in d.get("features", [])]
        filas += feats
        if not d.get("exceededTransferLimit") or not feats:
            return filas
        off += len(feats)


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    force = os.environ.get("FORCE") == "1"
    partes = []
    respaldo = servicios("porcentaje_")
    for ole, serv0 in servicios().items():
        for nivel in NIVELES:
            f = CACHE / f"{ole}_{nivel}.json"
            serv = serv0
            if force or not f.exists():
                try:
                    filas = []
                    for serv in [serv0] + ([respaldo[ole]] if ole in respaldo else []):
                        capa = capa_de(serv, nivel)
                        filas = descargar_capa(serv, capa, nivel) if capa is not None else []
                        if filas:
                            break
                    if not filas:
                        print(f"[vacío] {ole} {nivel}", file=sys.stderr)
                        continue
                    f.write_text(json.dumps({"servicio": serv, "filas": filas}, ensure_ascii=False))
                except Exception as e:  # noqa: BLE001
                    print(f"[fallo] {ole} {nivel}: {e}", file=sys.stderr)
                    continue
            js = json.loads(f.read_text())
            if isinstance(js, dict):
                serv, js = js["servicio"], js["filas"]
            df = pd.DataFrame(js)
            if df.empty:
                continue
            df["oleada"], df["nivel_geo"], df["servicio"] = ole, nivel, serv
            partes.append(df)
            print(f"{ole} {nivel}: {len(df)} unidades ({serv})")
    df = pd.concat(partes, ignore_index=True)
    df["codigo"] = df["codigo"].astype(str)
    largo = df.melt(id_vars=["oleada", "nivel_geo", "codigo", "servicio", "nota1"],
                    value_vars=[c for c in ("vivienda_turistica", "plazas", "porcentaje_vivienda_turistica") if c in df],
                    var_name="medida", value_name="valor")
    largo["fecha"] = pd.to_datetime(largo["oleada"].str.replace("M", "-") + "-01").dt.strftime("%Y-%m-%d")
    largo["periodo"] = largo["oleada"]
    largo["serie"] = "VUT_" + largo["nivel_geo"] + "_" + largo["codigo"] + "_" + largo["medida"]
    largo["unidad"] = largo["medida"].map({"vivienda_turistica": "viviendas", "plazas": "plazas",
                                           "porcentaje_vivienda_turistica": "% del total de viviendas"})
    largo["fuente"] = "INE (estadística experimental, servicio ArcGIS)"
    largo["url"] = BASE + "/Hosted/" + largo["servicio"] + "/FeatureServer"
    largo["territorio"], largo["nivel"] = largo["codigo"], largo["nivel_geo"]
    cols = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "territorio", "nivel", "codigo",
            "medida", "nota1"]
    largo[cols].sort_values(["nivel", "codigo", "medida", "periodo"]).to_csv(SALIDA, index=False)
    print(f"escrito {SALIDA} ({len(largo)} filas)")


if __name__ == "__main__":
    main()
