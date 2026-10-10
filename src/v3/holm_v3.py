"""Holm (m=4) sobre los p de las evaluaciones confirmatorias v3 (docs/v3/hipotesis.md, P4).

Familia: H3-1 y H3-2 (p de la evaluación sellada en distritos) y H3-3a y H3-3b (p de la validación sellada
por fuente). Si una hipótesis no se evaluó (no estimable o sin acceso), entra con p = 1 (conservador).
Salida: output/v3/holm_v3.json y output/v3/holm_v3.csv.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v3"
FAMILIA = ["H3-1", "H3-2", "H3-3a", "H3-3b"]


def _p_c1(h: str) -> float | None:
    f = OUT / "C1" / f"sellado_{h}.json"
    if not f.exists():
        return None
    d = json.loads(f.read_text())
    for k in ("p", "p_dos_colas", "p_valor", "pvalue"):
        if k in d and d[k] is not None:
            return float(d[k])
    return None


def _p_c3(h: str) -> float | None:
    f = OUT / "C3" / "resultado.json"
    if not f.exists():
        return None
    return json.loads(f.read_text()).get("p_validacion_sellada", {}).get(h)


def holm(p: dict[str, float]) -> dict[str, float]:
    orden = sorted(p, key=p.get)
    m, ajust, maximo = len(orden), {}, 0.0
    for i, h in enumerate(orden):
        maximo = max(maximo, min(1.0, (m - i) * p[h]))
        ajust[h] = maximo
    return ajust


def main() -> dict:
    crudo = {h: (_p_c1(h) if h.startswith("H3-1") or h == "H3-2" else _p_c3(h)) for h in FAMILIA}
    p = {h: (1.0 if v is None else float(v)) for h, v in crudo.items()}
    aj = holm(p)
    filas = [{"hipotesis": h, "p_sellado": crudo[h], "p_usado": p[h], "p_holm": aj[h],
              "nota": "no evaluada: p=1" if crudo[h] is None else ""} for h in FAMILIA]
    pd.DataFrame(filas).to_csv(OUT / "holm_v3.csv", index=False)
    res = {"m": len(FAMILIA), "filas": filas}
    (OUT / "holm_v3.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


if __name__ == "__main__":
    for f in main()["filas"]:
        print(f)
