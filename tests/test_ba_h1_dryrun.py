"""Ensayo en seco de evaluar_H1 con un PSEUDO-sellado construido solo con datos de ENTRENAMIENTO.
No llama a holdout.evaluate ni lee data/sealed. Pseudo-sellado: trimestres > 2022Q2 y provincias 02, 33, 50 (toda su
historia); entrenamiento: el resto hasta 2022Q2."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "v2"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import ba_h1_sellado as hs  # noqa: E402
import v2_common as vc  # noqa: E402

PSEUDO = ["02", "33", "50"]
QF = "2022Q2"


def _datos(perturbar=False):
    pan = vc.load("panel_prov_q")
    pan["cod_prov"] = pan["cod_prov"].astype(str)
    pan["trimestre"] = pan["trimestre"].astype(str)
    nac = vc.load("nacional_q_v2")
    nac["trimestre"] = nac["trimestre"].astype(str)
    es_ps = pan["cod_prov"].isin(PSEUDO)
    tr = {"panel_prov_q": pan[~es_ps & (pan["trimestre"] <= QF)], "nacional_q_v2": nac[nac["trimestre"] <= QF]}
    se_p = pan[es_ps | (pan["trimestre"] > QF)].copy()
    if perturbar:   # cambia la historia de las pseudo-selladas: las pendientes de train_provs no deben moverse
        m = se_p["cod_prov"].isin(PSEUDO)
        se_p.loc[m, "ln_ocupados"] = se_p.loc[m, "ln_ocupados"] + 0.5
    se = {"panel_prov_q": se_p, "nacional_q_v2": nac[nac["trimestre"] > QF]}
    return se, tr


def test_dryrun():
    se, tr = _datos()
    r = hs.evaluar_H1(se, tr, q_fin_train=QF)
    assert r["selladas"] == PSEUDO
    assert r["todas"]["n_periodos"] >= 8
    assert np.isfinite(r["todas"]["rmse"]) and np.isfinite(r["todas"]["dm_vs_AR4"])
    assert r["selladas_ventana"].get("n_periodos", 0) >= 8
    assert "rmse" in r["selladas_toda_historia"] and "rmse" in r["train_provs"]
    se2, tr2 = _datos(perturbar=True)
    r2 = hs.evaluar_H1(se2, tr2, q_fin_train=QF)
    # las pendientes vienen solo de entrenamiento: las 49 provincias de entrenamiento no cambian
    assert abs(r["train_provs"]["rmse"] - r2["train_provs"]["rmse"]) < 1e-12
    assert abs(r["train_provs"]["rmse_AR4"] - r2["train_provs"]["rmse_AR4"]) < 1e-12


if __name__ == "__main__":
    test_dryrun()
    print("OK")
