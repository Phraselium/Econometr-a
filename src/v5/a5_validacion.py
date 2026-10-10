"""A5: validacion de precision del diccionario sobre una muestra aleatoria (SEED 20261011) de 40 filas de documentos no normativos.

Etiquetas (lectura manual del analista sobre la cita; no corrigen ningun dato):
M = medida o propuesta pertinente al instrumento; X = mencion, diagnostico o contexto del instrumento; R = ruido (el termino no corresponde al instrumento).
Las etiquetas valen para el CSV de medidas de la fecha de etiquetado; si cambia el diccionario o el CSV, la clave de control no coincide
y el script no escribe la validacion (hay que re-etiquetar).
"""
import csv
import hashlib
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/v5/A5"
ETQ = "MXMXRMRMMMRMXXRMXRMMMMRRMXRMXXMRMXMXMMXM"
CLAVE = "50096da2dd0f"


def main():
    m = [x for x in csv.DictReader((OUT / "medidas_programas_v5.csv").open(encoding="utf-8")) if x["doc_id"] not in ("A5-D11", "A5-D12")]
    random.seed(20261011)
    idx = sorted(random.sample(range(len(m)), 40))
    clave = hashlib.sha256("|".join(f"{m[i]['doc_id']}{m[i]['instrumento']}{m[i]['pagina']}" for i in idx).encode()).hexdigest()[:12]
    if CLAVE and clave != CLAVE:
        raise SystemExit("La muestra ha cambiado: re-etiquetar antes de escribir la validacion")
    rows = [[m[i]["doc_id"], m[i]["instrumento"], m[i]["pagina"], m[i]["direccion"], ETQ[k]] for k, i in enumerate(idx)]
    with (OUT / "validacion_precision.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["doc_id", "instrumento", "pagina", "direccion_automatica", "etiqueta_manual"])
        w.writerows(rows)
    c = Counter(r[4] for r in rows)
    res = {"clave_muestra": clave, "n": 40, "M": c["M"], "X": c["X"], "R": c["R"],
           "precision_estricta_M": c["M"] / 40, "precision_M_o_X": (c["M"] + c["X"]) / 40}
    (OUT / "validacion_precision.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(res)


if __name__ == "__main__":
    main()
