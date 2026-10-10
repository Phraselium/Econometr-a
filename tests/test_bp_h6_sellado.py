"""Ensayo en seco de bp_h6_sellado._evaluar con un pseudo-sellado construido SOLO con datos de entrenamiento.
Pseudo-diseño (análogo al real): pseudo-entrenamiento <= 2022Q2, pseudo-sellado = 2022Q3-2024Q2 (8 trimestres) +
3 pseudo-provincias selladas (SEED); tratamiento FALSO desde 2021Q3 (4 pseudo-tratadas no catalanas); 2021Q3-2022Q2
excluidos del ajuste (análogo a 2024Q1-Q2). No toca data/sealed ni holdout.evaluate.
Ejecutar: python tests/test_bp_h6_sellado.py"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "v2"))
sys.path.insert(0, str(ROOT / "src"))
import bp_h6_sellado as bh  # noqa: E402
import v2_common as vc  # noqa: E402

CAT = ["08", "17", "25", "43"]
L = "2022Q2"


def pseudo(efecto=0.0, quitar_trimestre=None):
    pan = vc.load("panel_prov_q")
    pan["trimestre"] = pan["trimestre"].astype(str)
    pan["cod_prov"] = pan["cod_prov"].astype(str)
    rng = np.random.default_rng(vc.SEED)
    cand = sorted(set(pan["cod_prov"]) - set(CAT) - set(bh.CFG_REAL["no_donantes"]))
    sel = rng.choice(cand, 7, replace=False).tolist()
    ps, tr = sorted(sel[:3]), sorted(sel[3:])
    t = pan["trimestre"]
    train = pan[~pan.cod_prov.isin(ps) & (t <= L)].copy()
    sell = pan[pan.cod_prov.isin(ps) | (t > L)].copy()
    if efecto:
        m = sell.cod_prov.isin(tr) & (sell.trimestre > L)
        sell.loc[m, "ipc_alquiler"] = sell.loc[m, "ipc_alquiler"] * np.exp(efecto)
    if quitar_trimestre:
        sell = sell[~(sell.cod_prov.isin(tr) & (sell.trimestre == quitar_trimestre))]
    cfg = dict(bh.CFG_REAL, tratadas=tr, no_donantes=CAT + bh.CFG_REAL["no_donantes"],
               pre_nivel=bh.qrange("2016Q1", "2021Q2"), pre_d4=bh.qrange("2016Q1", "2021Q2"),
               post=bh.qrange("2022Q3", "2024Q2"), B=200)
    return {"panel_prov_q": sell}, {"panel_prov_q": train}, cfg, ps, tr


def test_sin_efecto():
    s, t, cfg, ps, tr = pseudo()
    assert not set(ps) & set(t["panel_prov_q"].cod_prov) and set(ps) <= set(s["panel_prov_q"].cod_prov)
    r = bh._evaluar(s, t, cfg)
    d = r["DECISION"]
    assert r["n_donantes"] >= 30 and not set(ps) & set(r["donantes"]) and not set(CAT) & set(r["donantes"])
    assert np.isfinite(d["tau"]) and 0 < d["p_perm_bilateral"] <= 1
    assert r["PRINCIPAL_ln_ipc_alquiler"]["sdid"]["B"] == 200
    return r


def test_efecto_inyectado():
    s, t, cfg, ps, tr = pseudo(efecto=-0.03)
    r = bh._evaluar(s, t, cfg)
    d = r["DECISION"]
    assert d["cumple_regla"] and abs(d["tau"] + 0.03) < 0.012, d
    return r


def test_aborta_con_dato_ausente():
    s, t, cfg, ps, tr = pseudo(quitar_trimestre="2023Q1")
    try:
        bh._evaluar(s, t, cfg)
    except RuntimeError as e:
        assert "abortado" in str(e)
        return
    raise AssertionError("debía abortar")


def pseudo_real(efecto=0.0):
    """Sellado falso para CFG_REAL EXACTO: entrenamiento real; sellado = 2022Q3-2024Q2 re-etiquetado como 2024Q3-2026Q2
    (encadenado en nivel) + 3 provincias selladas falsas (11, 16, 45) copiadas de otras tres, todos los periodos."""
    import pandas as pd
    pan = vc.load("panel_prov_q")
    pan["trimestre"] = pan["trimestre"].astype(str)
    pan["cod_prov"] = pan["cod_prov"].astype(str)
    old, new = bh.qrange("2022Q3", "2024Q2"), bh.qrange("2024Q3", "2026Q2")
    base = pan[pan.trimestre == "2022Q2"].set_index("cod_prov")["ipc_alquiler"]
    fin = pan[pan.trimestre == "2024Q2"].set_index("cod_prov")["ipc_alquiler"]
    f = pan[pan.trimestre.isin(old)].copy()
    f["ipc_alquiler"] = f["ipc_alquiler"] * f["cod_prov"].map(fin / base)
    f["trimestre"] = f["trimestre"].map(dict(zip(old, new)))
    f.loc[f.cod_prov.isin(CAT), "ipc_alquiler"] *= np.exp(efecto)
    falsas = []
    for nuevo, orig in zip(["11", "16", "45"], ["02", "05", "07"]):
        g = pan[pan.cod_prov == orig].copy()
        g["cod_prov"] = nuevo
        falsas.append(g)
    return {"panel_prov_q": pd.concat([f] + falsas)}, {"panel_prov_q": pan}


def test_cfg_real_exacta():
    import time
    out = {}
    for efecto in (0.0, -0.03):
        s, t = pseudo_real(efecto)
        cfg = dict(bh.CFG_REAL, B=100)
        t0 = time.time()
        r = bh._evaluar(s, t, cfg)
        out[efecto] = r
        assert r["n_donantes"] == 40 and not {"11", "16", "45"} & set(r["donantes"])
        assert r["pre_nivel"][2] == 26 and r["post"][2] == 8
        assert "sec_sin_2023Q3_Q4_en_pre" in r and r["DECISION"]["tau"] == r["PRINCIPAL_ln_ipc_alquiler"]["sdid"]["tau"]
        print("CFG_REAL exacto, efecto", efecto, r["DECISION"], "t=%.1fs (B=100)" % (time.time() - t0))
    assert out[-0.03]["DECISION"]["cumple_regla"]
    return out


def test_secundario_falla_no_aborta():
    """Si un secundario lanza error, la decisión principal se devuelve igualmente."""
    s, t, cfg, ps, tr = pseudo()
    orig = bh.bl.run_design
    n = {"k": 0}

    def roto(*a, **k):
        n["k"] += 1
        if n["k"] > 1:          # la primera llamada es la PRINCIPAL
            raise ValueError("fallo simulado")
        return orig(*a, **k)
    bh.bl.run_design = roto
    try:
        r = bh._evaluar(s, t, dict(cfg, B=50))
    finally:
        bh.bl.run_design = orig
    assert "DECISION" in r and str(r["sec_delta4"]).startswith("error")


def test_no_abre_muestra_sellada():
    import ast
    for f in ("bp_h6_sellado.py", "bp_lib.py", "bp_main.py"):
        tree = ast.parse((ROOT / "src" / "v2" / f).read_text())
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                assert all(a.name != "holdout" for a in n.names), f
            if isinstance(n, ast.ImportFrom):
                assert n.module != "holdout", f
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                assert n.func.attr not in ("evaluate", "load_sealed"), f


if __name__ == "__main__":
    test_no_abre_muestra_sellada()
    test_aborta_con_dato_ausente()
    test_secundario_falla_no_aborta()
    rr = test_cfg_real_exacta()
    r0, r1 = test_sin_efecto(), test_efecto_inyectado()
    out = ROOT / "output" / "v2" / "BP" / "dryrun_h6_sellado.json"
    out.write_text(json.dumps({"sin_efecto_(tratamiento_falso)": r0, "con_efecto_inyectado_-0,03": r1,
                               "CFG_REAL_exacto_sin_efecto_B100": rr[0.0], "CFG_REAL_exacto_efecto_-0,03_B100": rr[-0.03]},
                              indent=1, ensure_ascii=False, default=str))
    for k, r in (("sin efecto", r0), ("efecto -0,03", r1)):
        print(k, json.dumps(r["DECISION"]), r["sec_tratadas_solas"])
