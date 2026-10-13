"""K4b paso 2: compara output/v6_1/K4B/calculos.json con output/v5/cifras_clave.csv (solo tras calcular)."""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "v6_1" / "K4B"
calc = json.load(open(OUT / "calculos.json"))
ck = pd.concat([pd.read_csv(ROOT / "output" / "v5" / "cifras_clave.csv"),   # v7.2: las retiradas siguen comparándose
                pd.read_csv(ROOT / "output" / "v5" / "cifras_superadas.csv")]).set_index("id")
ORDEN = ["A23-A2", "terminadas_1924", "deficit_2124_c1", "deficit_2124_c2", "dh_2125", "D1-H11", "A23-P2",
         "B4-v3-vut-cantidad", "D1-H12", "A23-A10", "E-B1-F", "latente_convivencia", "B1-H1", "B1-H4", "R1C-001"]


def rel(a, b):
    if a is None or b is None or pd.isna(a) or pd.isna(b):
        return None
    return abs(a - b) / abs(b) if b else abs(a - b)


rows = []
for k in ORDEN:
    c, p = calc[k], ck.loc[k]
    pv, pm, px = (None if pd.isna(x) else float(x) for x in (p.valor, p["min"], p["max"]))
    d = [rel(c["valor"], pv), rel(c["min"], pm), rel(c["max"], px)]
    dd = [x for x in d if x is not None]
    pct = "%" in str(p.unidad)
    # redondeo: cifras en % publicadas con 1 decimal -> tolerancia absoluta 0,05 pp
    def ok(a, b):
        if a is None or b is None or pd.isna(a) or pd.isna(b):
            return None
        return abs(a - b) / abs(b) <= 0.01 or (pct and abs(a - b) <= 0.0501)
    oks = [ok(c["valor"], pv), ok(c["min"], pm), ok(c["max"], px)]
    oks = [x for x in oks if x is not None]
    coincide = "no_reconstruible" if not oks else ("si" if all(oks) else ("parcial" if any(oks) else "no"))
    rows.append({"id": k, "valor_publicado": pv, "min_pub": pm, "max_pub": px, "valor_k4b": c["valor"], "min_k4b": c["min"],
                 "max_k4b": c["max"], "dif_relativa": round(max(dd), 4) if dd else None, "coincide": coincide,
                 "explicacion": c["nota"]})
df = pd.DataFrame(rows)
df.to_csv(OUT / "comparacion.csv", index=False)
n = int((df.coincide == "si").sum())
res = {"rama": "v6_1/K4B", "pregunta": "Reproducen 15 cifras de cifras_clave.csv desde data/raw con codigo independiente?", "capa": "C4",
       "datos": "data/raw (+ v3/v5 raw)", "N": 15, "metodo": "doble implementacion independiente (src/v6_1/k4b_run.py)",
       "estimacion": {"coinciden": n, "parciales": int((df.coincide == "parcial").sum()),
                      "no_reconstruibles": int((df.coincide == "no_reconstruible").sum()), "no_coinciden": int((df.coincide == "no").sum())},
       "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO", "diagnosticos": df.set_index("id").coincide.to_dict(),
       "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "Ver docs/v6_1/doble_implementacion.md"}
json.dump(res, open(OUT / "resultado.json", "w"), indent=1, ensure_ascii=False)
print(df[["id", "valor_k4b", "min_k4b", "max_k4b", "valor_publicado", "min_pub", "max_pub", "dif_relativa", "coincide"]].to_string())
