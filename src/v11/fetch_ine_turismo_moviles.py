"""V11-DATOS (bloque 4, punto 17): INE, medición del turismo a partir de la posición de los teléfonos móviles
(estadística experimental), por MUNICIPIO de destino y mes, desde 2019:
- 52048 (TMOV_R, receptor): turistas residentes en el extranjero por municipio de destino y país de residencia;
- 53464 (TMOV_I, interno): turistas residentes en España por municipio de destino y CCAA de origen.
Las descargas completas (jaxiT3, px, xlsx) dan error 500 y la API tempus limita el volumen («No puede mostrarse por
restricciones de volumen»), incluso con «Total» de país. Se pide municipio a municipio (tv=19:<id>) con metadatos
(tip=AM), lo que da el código INE de cada serie. Ámbito por coste (≈1 s por petición): municipios de la Comunitat
Valenciana (provincias 03, 12, 46) y capitales de provincia; el resto, documentado en cobertura.md.
Filas desde 2026-07: posterior_prereg = True. Licencia INE: reutilización con cita.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, marcar_posterior_prereg, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "ine_turismo_moviles"
DIR = RAW11 / FUENTE
API = "https://servicios.ine.es/wstempus/js/ES/"
LIC = "INE: reutilización con cita (Ley 37/2007); estadística experimental"
TABLAS = {52048: ("receptor", "País de residencia"), 53464: ("interno", "Comunidad autónoma de origen")}
CAPITALES = {"01059", "02003", "03014", "04013", "05019", "06015", "07040", "08019", "09059", "10037", "11012", "12040",
             "13034", "14021", "15030", "16078", "17079", "18087", "19130", "20069", "21041", "22125", "23050", "24089",
             "25120", "26089", "27028", "28079", "29067", "30030", "31201", "32054", "33044", "34120", "35016", "36038",
             "37274", "38038", "39075", "40194", "41091", "42173", "43148", "44216", "45168", "46250", "47186", "48020",
             "49275", "50297", "51001", "52001"}


def get(url: str):
    for i in range(3):
        try:
            r = requests.get(url, headers=CABECERAS, timeout=300)
            if r.status_code == 200:
                return json.loads(r.content.decode("utf-8", "replace"))
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2 ** (i + 1))
    return None


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    for t, (nombre, dim) in TABLAS.items():
        grupos = get(f"{API}GRUPOS_TABLA/{t}")
        gm = next(g["Id"] for g in grupos if "unicipio" in g["Nombre"] and "destino" in g["Nombre"].lower())
        muns = [m for m in get(f"{API}VALORES_GRUPOSTABLA/{t}/{gm}") if m.get("Codigo")]
        sel = [m for m in muns if m["Codigo"][:2] in ("03", "12", "46") or m["Codigo"] in CAPITALES]
        filas, fallos = [], []
        for m in sel:
            d = get(f"{API}DATOS_TABLA/{t}?tv={m['FK_Variable']}:{m['Id']}&nult=200&tip=AM")
            if not isinstance(d, list):
                fallos.append(m["Codigo"])
                continue
            for s in d:
                meta = {x.get("T3_Variable", ""): x.get("Nombre", "") for x in s.get("MetaData", [])}
                origen = next((v for k, v in meta.items() if k not in ("Municipios", "Tipo de dato", "Concepto turístico")), "")
                concepto = meta.get("Concepto turístico", "")
                tipo = meta.get("Tipo de dato", "")
                for x in s.get("Data", []):
                    per = str(x.get("T3_Periodo", ""))
                    mes = f"{x['Anyo']}-{per[1:].zfill(2)}" if per.startswith("M") else f"{x['Anyo']}-{per}"
                    filas.append((m["Codigo"], origen, concepto, tipo, mes, x.get("Valor"), x.get("Secreto", False)))
        D = pd.DataFrame(filas, columns=["cod_municipio", "origen", "concepto", "tipo_dato", "mes", "valor", "secreto"])
        D = marcar_posterior_prereg(D.dropna(subset=["valor"]).sort_values(["cod_municipio", "origen", "mes"]), "mes")
        r = DIR / f"turismo_moviles_{nombre}_municipio.csv.gz"
        D.to_csv(r, index=False, compression=GZ_PANDAS)
        registrar(FUENTE, r, f"{API}DATOS_TABLA/{t}?tv=19:<id>&nult=200&tip=AM", edicion=f"INE {t} ({nombre}), API tempus",
                  periodo=f"{D.mes.min()}–{D.mes.max()}", nivel_territorial="municipio de destino (Comunitat Valenciana y capitales)",
                  licencia=LIC, redistribuible=True, notas=f"origen = {dim}; municipios={D.cod_municipio.nunique()}; fallos={fallos[:20]}; "
                                                          f"posterior_prereg={int(D.posterior_prereg.sum())}")
        print(t, len(D), D.cod_municipio.nunique(), len(fallos))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
