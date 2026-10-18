"""V16-F6 · Control de falsos descubrimientos de V16 (adenda del pre-registro, punto 2; decisión K12).

Dos ramas con denominador FIJO:
- diseños: 18 pruebas principales + 3 BLP/GATES = 21;
- rejilla: 83 celdas de rejilla_fija.csv.
Método: Benjamini-Yekutieli (alternativa nombrada en la adenda; el BH jerárquico no superó el Monte Carlo, K12), q = 0,10.
Las pruebas sin p-valor (herramienta NO APTA) cuentan en el denominador y no pueden rechazarse.
Lee `p_valores_para_BY` de output/v16/q*/resultado.json y output/v16/rejilla/resultado.json; escribe output/v16/fdr/resultado.json
y output/v16/fdr/informe.md. Sin red; determinista.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v16" / "fdr"
Q = 0.10
M = {"diseños": 21, "rejilla": 83}


def by(pvalores: dict[str, float], m: int, q: float = Q) -> dict[str, dict]:
    """q-valores de Benjamini-Yekutieli con denominador fijo m (las pruebas sin p cuentan en m)."""
    c = sum(1 / i for i in range(1, m + 1))
    orden = sorted(pvalores.items(), key=lambda kv: kv[1])
    ajust, previo = {}, 1.0
    for rango in range(len(orden), 0, -1):  # paso descendente: mínimo acumulado desde el final
        k, p = orden[rango - 1]
        previo = min(previo, p * m * c / rango)
        ajust[k] = min(previo, 1.0)
    return {k: {"p": p, "q_BY": ajust[k], "rechaza": ajust[k] <= q} for k, p in pvalores.items()}


def recoger() -> dict[str, dict]:
    ramas = {"diseños": {}, "rejilla": {}}
    sin_p = {"diseños": [], "rejilla": []}
    for r in sorted((RAIZ / "output" / "v16").glob("*/resultado.json")):
        if not (r.parent.name.startswith("q") or r.parent.name == "rejilla"):
            continue
        lista = json.loads(r.read_text(encoding="utf-8")).get("p_valores_para_BY") or []
        rama = "rejilla" if r.parent.name == "rejilla" else "diseños"
        for x in lista:
            (ramas[rama].__setitem__(x["id"], float(x["p"])) if x.get("p") is not None else sin_p[rama].append(x["id"]))
    return {"con_p": ramas, "sin_p": sin_p}


def main() -> int:
    d = recoger()
    res = {}
    for rama, m in M.items():
        n = len(d["con_p"][rama]) + len(d["sin_p"][rama])
        if n > m:
            print(f"f6_fdr: la rama {rama} tiene {n} pruebas y el denominador fijado es {m}")
            return 1
        res[rama] = {"m": m, "pruebas_con_p": by(d["con_p"][rama], m) if d["con_p"][rama] else {},
                     "pruebas_sin_p_NO_APTO": d["sin_p"][rama], "pruebas_no_reportadas": m - n}
    OUT.mkdir(parents=True, exist_ok=True)
    salida = {"rama": "v16-fdr", "pregunta": "control de falsos descubrimientos de V16", "capa": "C4",
              "metodo": f"Benjamini-Yekutieli, q = {Q}, denominador fijo por rama (adenda punto 2; K12)", "ramas": res,
              "notas": "Las pruebas sin p-valor (herramienta NO APTA) cuentan en el denominador y no pueden rechazarse. "
                       "Rechazar en (a) no basta para un hallazgo: faltan (b) magnitud de referencia y (c) muestra sellada."}
    (OUT / "resultado.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    L = ["# V16 · Control de falsos descubrimientos (fase 6)", "",
         f"Generado por `python3 src/v16/f6_fdr.py`. {salida['metodo']}. {salida['notas']}", ""]
    for rama, r in res.items():
        L += [f"## Rama {rama} (m = {r['m']})", "", "| Prueba | p | q (BY) | Condición (a) |", "|---|---|---|---|"]
        for k, v in sorted(r["pruebas_con_p"].items(), key=lambda kv: kv[1]["p"]):
            L.append(f"| {k.replace('|', ' · ')} | {v['p']:.3g} | {v['q_BY']:.3g} | {'cumple' if v['rechaza'] else 'no cumple'} |")
        L += ["", f"Sin p-valor (NO APTO): {len(r['pruebas_sin_p_NO_APTO'])}; no reportadas: {r['pruebas_no_reportadas']}.", ""]
    L += ["<a id=\"by\"></a>Ficha: q_BY = mín. sobre j ≥ rango de p_(j) · m · Σ_{i≤m} 1/i / j, con m fijo por rama; reproducible con "
          "`python3 src/v16/f6_fdr.py` desde los p de cada resultado.json.", ""]
    (OUT / "informe.md").write_text("\n".join(L), encoding="utf-8")
    hechos = [{"id": f"V16-FDR-{k.split('|')[0]}-q", "indicador": f"{k.split('|')[0]}: q-valor de Benjamini-Yekutieli en la rama {rama} (m = {M[rama]})",
               "valor": v["q_BY"], "min": v["q_BY"], "max": v["q_BY"], "unidad": "q-valor", "periodo": "fase 6 de V16",
               "cobertura": f"rama {rama}", "fuentes": "cálculo propio sobre output/v16/*/resultado.json", "capa": "C4",
               "fecha_dato": "2026-10-17", "ficha": "output/v16/fdr/informe.md#by"}
              for rama, r in res.items() for k, v in sorted(r["pruebas_con_p"].items())]
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("f6_fdr:", {k: {kk: round(vv["q_BY"], 4) for kk, vv in v["pruebas_con_p"].items()} for k, v in res.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
