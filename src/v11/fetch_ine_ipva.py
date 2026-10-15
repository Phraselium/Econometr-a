"""V11-DATOS (histórico, A4): INE, Índice de Precios de Vivienda en Alquiler (IPVA), API tempus con metadatos (tip=AM),
que da el CÓDIGO INE de cada serie (municipio de 5 dígitos; distrito de 7 = municipio + distrito):
- 59060: índices por municipio (municipios de más de 10.000 hab.), anual 2011-último, por tamaño de la vivienda;
- 59061: índices por distritos de los municipios capitales de provincia, anual 2011-último, por tamaño de la vivienda.
Tipo de dato: índice (2015 = 100) y variación anual. La desagregación por antigüedad del contrato (nuevos/existentes)
solo existe por CCAA y provincia (59004, 59005; ya en data/raw/v9/ine_ipva): a escala municipal y de distrito NO se
publica. Nada se cruza por nombre. Licencia INE: reutilización con cita.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, marcar_posterior_prereg, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "ine_ipva"
DIR = RAW11 / FUENTE
URL = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{t}?nult=40&tip=AM"
LIC = "INE: reutilización con cita (Ley 37/2007)"
TABLAS = {59060: ("municipio", "Municipios"), 59061: ("distrito", "Distritos")}


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    for t, (nivel, var) in TABLAS.items():
        d = json.loads(requests.get(URL.format(t=t), headers=CABECERAS, timeout=600).content.decode("utf-8", "replace"))
        filas = []
        for s in d:
            meta = {m.get("T3_Variable"): m for m in s["MetaData"]}
            terr = meta.get(var) or meta.get("Total Nacional")
            cod = terr.get("Codigo", "") if terr else ""
            for x in s["Data"]:
                filas.append({"codigo": cod, "nivel": nivel if var in meta else "nacional", "territorio": terr.get("Nombre") if terr else "",
                              "tipo_dato": meta.get("Tipo de dato", {}).get("Nombre", ""),
                              "tamano_vivienda": meta.get("Tamaño de la vivienda", {}).get("Nombre", ""),
                              "anio": x["Anyo"], "valor": x.get("Valor")})
        D = marcar_posterior_prereg(pd.DataFrame(filas).dropna(subset=["valor"]).sort_values(["codigo", "tipo_dato", "tamano_vivienda", "anio"]).assign(
            anio=lambda z: z.anio.astype(str)), "anio")
        r = DIR / f"ipva_{nivel}_tamano.csv.gz"
        D.to_csv(r, index=False, compression=GZ_PANDAS)
        registrar(FUENTE, r, URL.format(t=t), edicion=f"INE IPVA, tabla {t} (API tempus, tip=AM)", periodo=f"{D.anio.min()}-{D.anio.max()}",
                  nivel_territorial=f"{nivel} (código INE de los metadatos)", licencia=LIC, redistribuible=True,
                  notas=f"índice y variación anual por tamaño de la vivienda; territorios={D.codigo.nunique()}; sin códigos={int((D.codigo == '').sum())}")
        print(t, len(D), D.codigo.nunique(), D.anio.min(), D.anio.max(), (D.codigo == "").sum())
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
