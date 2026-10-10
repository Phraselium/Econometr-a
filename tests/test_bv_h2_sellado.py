"""Ensayo en seco de bv_h2_sellado._evaluar con un pseudo-sellado construido SOLO con datos de entrenamiento.
Pseudo-ventana sellada: 2022Q3-2024Q2 (8 trimestres atrás); 3 pseudo-provincias selladas (elegidas con SEED).
No toca data/sealed ni holdout.evaluate. Ejecutar: python tests/test_bv_h2_sellado.py"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "v2"))
import bv_h2_sellado as bh  # noqa: E402
import bv_lib as bl  # noqa: E402
import v2_common as vc  # noqa: E402


def pseudo():
    pan, nac = vc.load("panel_prov_q"), vc.load("nacional_q_v2")
    nac = nac[nac["trimestre"].astype(str) <= "2024Q2"]
    rng = np.random.default_rng(vc.SEED)
    ps = sorted(rng.choice(sorted(pan["cod_prov"].unique()), 3, replace=False).tolist())
    L = "2022Q2"
    t = pan["trimestre"].astype(str)
    es_ps = pan["cod_prov"].isin(ps)
    train_p = pan[~es_ps & (t <= L)]
    sell_p = pan[es_ps | (t > L)]
    return ({"panel_prov_q": sell_p, "nacional_q_v2": nac[nac["trimestre"].astype(str) > L]},
            {"panel_prov_q": train_p, "nacional_q_v2": nac[nac["trimestre"].astype(str) <= L]}, ps)


def test_dry_run():
    s, t, ps = pseudo()
    r = bh._evaluar(s, t, "2022Q2", "2024Q2", "2021Q3", "2023Q2")
    assert r["provincias_selladas"] == ps and len(r["provincias_selladas"]) == 3
    assert r["PRINCIPAL_todas"]["n_periodos"] >= 8 and np.isfinite(r["PRINCIPAL_todas"]["p_vs_AR4"])
    assert r["PRINCIPAL_todas"]["n"] > r["sec_a_entrenamiento"]["n"]
    return r


def test_aborta_con_pocos_periodos():
    s, t, _ = pseudo()
    try:
        bh._evaluar(s, t, "2022Q2", "2024Q2", "2022Q3", "2023Q2")   # solo 4 orígenes con objetivo
    except RuntimeError as e:
        assert "abortado" in str(e)
        return
    raise AssertionError("debía abortar")


if __name__ == "__main__":
    test_aborta_con_pocos_periodos()
    r = test_dry_run()
    (ROOT / "output" / "v2" / "BV" / "dryrun_h2_sellado.json").write_text(json.dumps(r, indent=1, ensure_ascii=False, default=str))
    print(json.dumps(r, indent=1, ensure_ascii=False, default=str)[:3500])
