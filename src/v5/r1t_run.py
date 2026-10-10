"""R1 técnico (v5): pendientes menores del backlog. Determinista y sin red.

- BK-046: nombres oficiales de los 19 distritos SERPAVI de València (cruce con la capa de distritos del Ajuntament).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "v5" / "R1T"


def distritos_valencia() -> pd.DataFrame:
    nom = pd.read_csv(ROOT / "data/raw/v5/valencia_distritos_nombres.csv", dtype={"codigo_serpavi": str})
    rk = pd.read_csv(ROOT / "output/f6/serpavi_distritos_ranking.csv", dtype={"distrito_cod": str})
    m = rk.merge(nom[["codigo_serpavi", "nombre"]], left_on="distrito_cod", right_on="codigo_serpavi", how="left")
    assert m.nombre.notna().all() and len(m) == 19, "cruce de distritos incompleto"
    m = m.drop(columns="codigo_serpavi").rename(columns={"nombre": "distrito"})
    return m[["distrito_cod", "distrito"] + [c for c in m.columns if c not in ("distrito_cod", "distrito")]]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    d = distritos_valencia()
    d.to_csv(OUT / "serpavi_distritos_valencia_nombres.csv", index=False, float_format="%.2f")
    res = dict(rama="R1T", pregunta="Pendientes técnicos del backlog (BK-046)", capa="C4",
               datos=["serpavi_valencia_distritos", "valencia_distritos_nombres (Ajuntament, 2026-10-10)"], N=len(d),
               metodo="cruce código SERPAVI 46250dd = distrito municipal dd (19 = 19)", estimacion=None, ic95=None,
               p_ajustado=None, nivel_evidencia="DESCRIPTIVO", diagnosticos={"distritos_cruzados": len(d)},
               fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
               notas="Supuesto declarado: los distritos censales de SERPAVI coinciden con los 19 distritos municipales.")
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
