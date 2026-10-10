"""INE · otros indicadores por SECCIÓN censal desde los servicios ArcGIS del INE (servergis/Hosted).

- Atlas de Distribución de Renta de los Hogares (ADRH): renta media por hogar y por persona (2019, 2020, 2022, 2023
  y el servicio sin año, cuyo periodo se lee del campo «periodo» si existe).
- Censo anual (2021-2025): número de personas; 2024-2025: % de extranjeros y % de nacidos en el extranjero.
Solo atributos (sin geometría). Caché por servicio en data/raw/v3_orig/gis/. Salida larga:
data/raw/v3/ine_v3_gis_seccion.csv.gz (servicio, codigo de sección, campo, valor, periodo).
Reutiliza la paginación y la búsqueda de capa de fetch_ine_vut_seccion_v3.py.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_ine_vut_seccion_v3 as fv  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CACHE = RAIZ / "data" / "raw" / "v3_orig" / "gis"
SALIDA = RAIZ / "data" / "raw" / "v3" / "ine_v3_gis_seccion.csv.gz"
SERVICIOS = [
    "Renta_neta_media_por_hogar__2019_", "1_Renta_neta_media_por_persona__2020_", "Renta_media_por_hogar",
    "ADRH_2022_Renta_media_por_hogar", "ADRH_2022_Renta_media_por_persona",
    "ADRH_2023_Renta_media_por_hogar", "ADRH_2023_Renta_media_por_persona", "ADRH_2023_Distribucion_renta_P80P20",
    "Censo_2021___Número_de_personas", "Censo_2022___Número_de_personas", "Censo_2023___Número_de_personas",
    "Censo_2024___Número_de_personas", "Censo_2025___Número_de_personas",
    "Censo_2024___Porcentaje_de_extranjeros", "Censo_2025___Porcentaje_de_extranjeros",
    "Censo_2024___Porcentaje_de_personas_nacidas_en_el_extranjero",
    "Censo_2025___Porcentaje_de_personas_nacidas_en_el_extranjero",
]
NO_DATO = {"objectid", "objectid_1", "objectid_12", "shape_leng", "shape_le_1", "shape__length", "shape__area",
           "cnut0", "cnut1", "cnut2", "cnut3", "cca", "cpro", "cmun", "cdis", "csec"}


def _capa_seccion(serv: str) -> int | None:
    d = fv._get(f"{fv.BASE}/Hosted/{fv.urllib.parse.quote(serv)}/FeatureServer?f=json")
    for lay in d.get("layers", []):
        if "ecci" in lay["name"].lower() and "ontorno" not in lay["name"].lower():
            return int(lay["id"])
    return None


def _descargar(serv: str, capa: int) -> list[dict]:
    url = f"{fv.BASE}/Hosted/{fv.urllib.parse.quote(serv)}/FeatureServer/{capa}/query"
    filas, off = [], 0
    while True:
        q = fv.urllib.parse.urlencode({"where": "1=1", "outFields": "*", "returnGeometry": "false",
                                       "resultOffset": off, "resultRecordCount": 2000, "f": "json"})
        d = fv._get(f"{url}?{q}")
        feats = [f["attributes"] for f in d.get("features", [])]
        filas += feats
        if not d.get("exceededTransferLimit") or not feats:
            return filas
        off += len(feats)


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    force = os.environ.get("FORCE") == "1"
    partes = []
    for serv in SERVICIOS:
        f = CACHE / f"{serv}.json"
        if force or not f.exists():
            capa = _capa_seccion(serv)
            if capa is None:
                print(f"[sin capa de secciones] {serv}", file=sys.stderr)
                continue
            f.write_text(json.dumps(_descargar(serv, capa), ensure_ascii=False))
        df = pd.DataFrame(json.loads(f.read_text()))
        if df.empty:
            print(f"[vacío] {serv}", file=sys.stderr)
            continue
        df.columns = [c.lower() for c in df.columns]
        cod = "cusec" if "cusec" in df else "codigo"
        num = [c for c in df.columns if c not in NO_DATO and c != cod and pd.api.types.is_numeric_dtype(df[c])]
        per = df["periodo"].astype(str) if "periodo" in df else pd.Series("", index=df.index)
        largo = df[[cod]].assign(periodo=per).join(df[num]).melt(id_vars=[cod, "periodo"], var_name="campo",
                                                                  value_name="valor")
        largo = largo.rename(columns={cod: "codigo"}).assign(servicio=serv)
        partes.append(largo)
        print(f"{serv}: {df[cod].nunique()} secciones; campos {num}")
    out = pd.concat(partes, ignore_index=True)
    out["codigo"] = out["codigo"].astype(str)
    out["fuente"] = "INE (servicios ArcGIS: ADRH y Censo anual)"
    out["url"] = fv.BASE + "/Hosted/" + out["servicio"] + "/FeatureServer"
    out.sort_values(["servicio", "codigo", "campo"]).to_csv(SALIDA, index=False)
    print(f"escrito {SALIDA} ({len(out)} filas)")


if __name__ == "__main__":
    main()
