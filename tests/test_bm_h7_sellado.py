"""Ensayo en seco de bm_h7_sellado._evaluar con un pseudo-sellado construido SOLO con datos de entrenamiento.
Pseudo-ventana sellada: 2022Q3-2024Q2; 3 pseudo-provincias selladas (elegidas con SEED). No toca data/sealed ni
holdout.evaluate. Ejecutar: python tests/test_bm_h7_sellado.py  (o pytest)"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "v2"))
import bm_h7_sellado as bh  # noqa: E402
import bm_lib as bl  # noqa: E402
import v2_common as vc  # noqa: E402

L, FIN, O_INI, O_FIN = "2022Q2", "2024Q2", "2021Q3", "2023Q2"


def pseudo(perturbar=False):
    pan, nac = vc.load("panel_prov_q"), vc.load("nacional_q_v2")
    nac = nac[nac["trimestre"].astype(str) <= "2024Q2"]
    rng = np.random.default_rng(vc.SEED)
    ps = sorted(rng.choice(sorted(pan["cod_prov"].unique()), 3, replace=False).tolist())
    t = pan["trimestre"].astype(str)
    es_ps = pan["cod_prov"].isin(ps)
    train_p = pan[~es_ps & (t <= L)]
    sell_p = pan[es_ps | (t > L)].copy()
    if perturbar:    # perturba la historia (<= L) de las pseudo-selladas: no debe mover a las 49 de entrenamiento
        m = sell_p["cod_prov"].isin(ps) & (sell_p["trimestre"].astype(str) <= L)
        sell_p.loc[m, "ipc_alquiler"] = sell_p.loc[m, "ipc_alquiler"] * 1.15
        sell_p.loc[m, "p_tasado"] = sell_p.loc[m, "p_tasado"] * 0.85
        for c in [c for c in sell_p.columns if "ipc_alquiler" in c or "p_tasado" in c]:
            if c.startswith("ln_"):
                sell_p.loc[m, c] = np.log(sell_p.loc[m, c.replace("ln_", "", 1)]) if c in ("ln_ipc_alquiler", "ln_p_tasado") else sell_p.loc[m, c]
    return ({"panel_prov_q": sell_p, "nacional_q_v2": nac[nac["trimestre"].astype(str) > L]},
            {"panel_prov_q": train_p, "nacional_q_v2": nac[nac["trimestre"].astype(str) <= L]}, ps)


def _sel(clases):
    """Selección de prueba por objetivo a partir de la real y de overrides de clase para cubrir todas las rutas."""
    return clases


def test_dry_run_seleccion_real():
    s, t, ps = pseudo()
    r = bh._evaluar(s, t, L, FIN, O_INI, O_FIN)
    assert r["selladas"] == ps and len(ps) == 3
    for o in "ABC":
        assert r[o]["PRINCIPAL"]["n_periodos"] >= 8 and np.isfinite(r[o]["PRINCIPAL"]["p_vs_AR4"])
        assert 0 <= r[o]["p_IUT_Holm"] <= 1
    assert r["B"]["PRINCIPAL"]["n"] > r["B"]["sec_a_entrenamiento_49"]["n"]
    assert "sec_b2_selladas_historia" in r["C"]
    return r


def test_todas_las_clases():
    s, t, _ = pseudo()
    sel = json.loads(bh.SEL_FILE.read_text())
    casos = {"A": [("PostLasso", "postlasso", {}), ("ARDL", "ardl", {}), ("TAR_ECM_asim", "tar_ecm", {"umbral": "asim"}),
                   ("BVAR_lam0.2", "bvar", {"lambda": 0.2}), ("TVPVAR_k0.99", "tvpvar", {"kappa": 0.99})],
             "B": [("RF_d4_l40", "rf", {}), ("LGBM_nl4_n150", "lgbm", {}), ("EN_l10.3_a0.05", "enet", {})]}
    for o, lst in casos.items():
        for nombre, clase, cfg in lst:
            s2 = {k: dict(v) for k, v in sel.items()}
            for oo in "ABC":
                if oo != o:
                    continue
            s2[o] = dict(s2[o], modelo=nombre, clase=clase, config=cfg)
            r = bh._evaluar(s, t, L, FIN, O_INI, O_FIN, seleccion=s2, objetivos=o)
            assert r[o]["PRINCIPAL"]["n_periodos"] >= 8, (o, nombre)
            assert np.isfinite(r[o]["PRINCIPAL"]["rmse"]), (o, nombre)


def test_aborta_con_pocos_periodos():
    s, t, _ = pseudo()
    try:
        bh._evaluar(s, t, L, FIN, "2022Q3", "2023Q2")      # solo 4 orígenes con objetivo
    except RuntimeError as e:
        assert "abortado" in str(e)
        return
    raise AssertionError("debía abortar")


def test_historia_de_selladas_no_mueve_las_pendientes():
    s, t, ps = pseudo()
    s2, t2, _ = pseudo(perturbar=True)
    r1 = bh._evaluar(s, t, L, FIN, O_INI, O_FIN)
    r2 = bh._evaluar(s2, t2, L, FIN, O_INI, O_FIN)
    for o in "BC":
        a = r1[o]["sec_a_entrenamiento_49"]["rmse"]
        b = r2[o]["sec_a_entrenamiento_49"]["rmse"]
        assert abs(a - b) < 1e-12, (o, a, b)
    # y las selladas SÍ cambian (su efecto fijo propio usa su historia)
    assert r1["B"]["PRINCIPAL"]["rmse"] != r2["B"]["PRINCIPAL"]["rmse"]


def _cambio_base(s, kipv=0.62, kalq=0.87):
    s = {k: v.copy() for k, v in s.items()}
    n, p = s["nacional_q_v2"], s["panel_prov_q"]
    n["ipv"] *= kipv
    n["ln_ipv"] += np.log(kipv)
    p["ipc_alquiler"] *= kalq
    p["ln_ipc_alquiler"] += np.log(kalq)
    return s


def test_cambio_de_base_en_el_sellado_da_el_mismo_resultado():
    s, t, _ = pseudo()
    r0 = bh._evaluar(s, t, L, FIN, O_INI, O_FIN)
    r1 = bh._evaluar(_cambio_base(s), t, L, FIN, O_INI, O_FIN)      # se reencadena desde el nivel de L
    for o in "ABC":
        assert abs(r0[o]["PRINCIPAL"]["rmse"] - r1[o]["PRINCIPAL"]["rmse"]) < 1e-9, o
        assert abs(r0[o]["PRINCIPAL"]["rmse_AR4"] - r1[o]["PRINCIPAL"]["rmse_AR4"]) < 1e-9, o


def test_guarda_aborta_con_discontinuidad():
    s, t, _ = pseudo()
    s2 = _cambio_base(s)
    nac = bh._concat(t["nacional_q_v2"], s2["nacional_q_v2"], ["trimestre"])      # concatenación ingenua (sin reencadenar)
    pan = bh._concat(t["panel_prov_q"], s2["panel_prov_q"], ["cod_prov", "trimestre"])
    for d_ in (nac, pan):
        d_["trimestre"] = d_["trimestre"].astype(str)
    try:
        bh._guarda_continuidad(nac, pan, L)
    except RuntimeError as e:
        assert "discontinuidad" in str(e)
        return
    raise AssertionError("debía abortar")


def test_secundario_que_falla_no_aborta():
    s, t, _ = pseudo()
    orig = bh._historia
    bh._historia = lambda *a, **k: (_ for _ in ()).throw(ValueError("fallo simulado"))
    try:
        r = bh._evaluar(s, t, L, FIN, O_INI, O_FIN, objetivos="BC")
    finally:
        bh._historia = orig
    assert "error" in r["B"]["sec_b2_selladas_historia"] and r["secundarios_errores"]
    assert np.isfinite(r["B"]["PRINCIPAL"]["rmse"]) and "H7_cumple" in r


if __name__ == "__main__":
    test_cambio_de_base_en_el_sellado_da_el_mismo_resultado()
    test_guarda_aborta_con_discontinuidad()
    test_secundario_que_falla_no_aborta()
    test_aborta_con_pocos_periodos()
    test_historia_de_selladas_no_mueve_las_pendientes()
    test_todas_las_clases()
    r = test_dry_run_seleccion_real()
    (ROOT / "output" / "v2" / "BM" / "dryrun_h7_sellado.json").write_text(json.dumps(r, indent=1, ensure_ascii=False, default=str))
    print(json.dumps(r, indent=1, ensure_ascii=False, default=str)[:3000])
