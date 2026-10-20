"""V18 · comparación final de las réplicas ciegas E2-R1 y E8-R1 con las cifras del orquestador (se ejecuta DESPUÉS de las réplicas).

Escribe la comparación en resultado.json (clave 'comparacion') y el informe.md de cada réplica. Lee solo output/v18/replica/*.
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
BASE = RAIZ / "output" / "v18" / "replica"

ORQ = {"e2_r1": {"est": -0.038, "ic": [-0.051, -0.026]}, "e8_r1": {"est": 0.0146, "ic": None}}


def veredicto(mia, orq, se):
    dif = mia - orq
    rel = abs(dif) / abs(orq)
    return dif, rel, (rel < 0.10 and abs(dif) < se)


def main():
    for k, o in ORQ.items():
        p = BASE / k / "resultado.json"
        r = json.loads(p.read_text(encoding="utf-8"))
        se = r["se_cr1_municipio"] if k == "e2_r1" else r["se_cluster_ccaa"]
        dif, rel, ok = veredicto(r["estimacion"], o["est"], se)
        en_ic_orq = (o["ic"][0] <= r["estimacion"] <= o["ic"][1]) if o["ic"] else None
        orq_en_mi_ic = r["ic95"][0] <= o["est"] <= r["ic95"][1]
        r["comparacion"] = {"orquestador": o["est"], "ic95_orquestador": o["ic"], "mia": r["estimacion"], "dif_abs": dif, "dif_rel": rel,
                            "mi_estimacion_en_ic_orquestador": en_ic_orq, "cifra_orquestador_en_mi_ic95": orq_en_mi_ic,
                            "veredicto": "coincide" if ok else "difiere"}
        p.write_text(json.dumps(r, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
        print(k, r["comparacion"])


if __name__ == "__main__":
    main()
