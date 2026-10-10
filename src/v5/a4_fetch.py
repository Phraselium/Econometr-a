"""A4 descargas (con red, fuera de make): python3 src/v5/a4_fetch.py
Guarda en data/raw/v5/ los valores oficiales de coste de construccion con URL y fecha de consulta:
  a4_mbc_rd1020_1993.csv   Real Decreto 1020/1993 (BOE-A-1993-19265), disposicion final primera: MBC1..MBC7 (pesetas/m2, 1993),
                           Norma 16 (coeficientes maximos de incremento por acuerdo de la Comision Superior, texto consolidado
                           tras RD 1464/2007) y expresion Vv = 1,40 [VR + VC] FL.
  a4_boe_plan_*.html no se guardan; la comprobacion de BOE-A-2022-802 y BOE-A-2026-8872 (sin modulo de coste) queda en
  docs/v5/fuentes_fallidas.md.
La serie de indice de costes (Eurostat sts_copi_q) ya esta en data/raw/eurostat_costes.csv (fetch de v1).
"""
import csv
import datetime
import re
import urllib.request
from pathlib import Path

DEST = Path(__file__).resolve().parents[2] / "data" / "raw" / "v5"
ID = "BOE-A-1993-19265"
URL = f"https://www.boe.es/buscar/act.php?id={ID}"


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(URL, timeout=120) as r:
        t = r.read().decode("utf8", "ignore")
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))
    hoy = datetime.date.today().isoformat()
    filas = []
    for k, v in re.findall(r"(MBC\d) = ([\d.]+) pesetas", t):
        filas.append(["MBC", k, "valor_pesetas_m2_1993", int(v.replace(".", "")), URL, hoy])
    for k, lo, hi in re.findall(r"(MBC\d) (1,\d\d)-(1,\d\d)", t):
        filas.append(["MBC", k, "coef_max_incremento", float(hi.replace(",", ".")), URL, hoy])
    m = re.search(r"V v =(1,\d+)", t)
    filas.append(["MODULACION", "Vv=1,40[VR+VC]FL", "factor", float(m.group(1).replace(",", ".")) if m else "", URL, hoy])
    with open(DEST / "a4_mbc_rd1020_1993.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bloque", "clave", "concepto", "valor", "url", "fecha_consulta"])
        w.writerows(filas)
    print(len(filas), "filas")


if __name__ == "__main__":
    main()
