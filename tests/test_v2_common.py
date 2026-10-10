"""Tests de src/v2_common.py (embargo, DM-HLN, ausencia de fugas, esquema resultado.json)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import v2_common as v2  # noqa: E402

PER = [f"{y}Q{q}" for y in range(1995, 2025) for q in range(1, 5)]


# ---------------------------------------------------------------- (a) splits
@pytest.mark.parametrize("h,embargo", [(1, 4), (4, 4), (8, 4), (1, 6)])
def test_block_splits_embargo(h, embargo):
    sp = v2.block_splits(PER, h, block_len=4, embargo=embargo, min_train=40)
    emb = max(embargo, h)
    assert len(sp) > 5
    prev_ini = None
    for itr, ite in sp:
        assert len(ite) == 4 and len(itr) >= 40
        assert itr[0] == 0 and (np.diff(itr) == 1).all()           # expansiva
        assert ite[0] - itr[-1] - 1 == emb                           # periodos intermedios
        assert itr.max() + h < ite.min()                             # objetivo del train fuera del test
        assert not set(itr) & set(ite)
        if prev_ini is not None:
            assert ite[0] - prev_ini == 4
        prev_ini = ite[0]
    assert sp[-1][1][-1] == len(PER) - 1 or len(PER) - sp[-1][1][-1] <= 4


def test_block_splits_first_test_y_min_train():
    sp = v2.block_splits(PER, 4, first_test="2012Q1", min_train=8)
    assert PER[sp[0][1][0]] == "2012Q1" and PER[sp[0][0][-1]] == "2010Q4"
    with pytest.raises(ValueError):
        v2.block_splits(PER, 4, first_test="1996Q1", min_train=40)


# ---------------------------------------------------------------- (b) DM-HLN
def test_dm_signo_y_magnitud():
    rng = np.random.default_rng(v2.SEED)
    n = 120
    e2 = rng.normal(0, 1.0, n)
    e1 = rng.normal(0, 1.5, n)                  # modelo 1 peor
    r = v2.dm_hln(e1, e2, h=1)
    assert r["DM"] > 2 and r["p"] < 0.05          # positivo: gana el modelo 2
    r_inv = v2.dm_hln(e2, e1, h=1)
    assert r_inv["DM"] < -2 and np.isclose(r_inv["DM"], -r["DM"])
    # magnitud: ~ dbar/se con dbar ~ 1.25
    assert 0.5 < r["mean_d"] < 2.0
    assert v2.dm_hln(e1, e2, h=4, loss="mae")["DM"] > 0


def test_dm_p_uniforme_bajo_h0():
    rng = np.random.default_rng(v2.SEED)
    for h in (1, 4):
        p = np.array([v2.dm_hln(rng.normal(size=60), rng.normal(size=60), h)["p"] for _ in range(600)])
        assert np.isfinite(p).all()
        assert stats.kstest(p, "uniform").pvalue > 0.01
        assert 0.02 < (p < 0.05).mean() < 0.11


def test_dm_panel_agrega_por_periodo():
    rng = np.random.default_rng(v2.SEED)
    per = np.repeat(np.arange(40), 10)
    e1, e2 = rng.normal(0, 1.4, 400), rng.normal(0, 1, 400)
    r = v2.dm_panel(e1, e2, per, h=1)
    assert r["n"] == 40 and r["DM"] > 0


# ---------------------------------------------------------------- (c) no fuga
@pytest.fixture(scope="module")
def datos():
    nac = v2.load("nacional_q_v2")
    pan = v2.load("panel_prov_q")
    pan = pan[pan.cod_prov.isin(sorted(pan.cod_prov.unique())[:8])].copy()
    return nac, pan


def _perturba(df, desde, seed=1, extra_skip=("trimestre", "anio", "cod_prov", "provincia", "cod_ccaa",
                                              "fecha", "q1", "q2", "q3", "q4")):
    """Multiplica por ruido todas las columnas numéricas con trimestre > desde."""
    d = df.copy()
    rng = np.random.default_rng(seed)
    m = d["trimestre"].astype(str) > desde
    for c in d.select_dtypes("number").columns:
        if c in extra_skip:
            continue
        d[c] = d[c].astype(float)
        d.loc[m, c] = d.loc[m, c] * (1 + rng.normal(0, 0.5, int(m.sum()))) + rng.normal(0, 1, int(m.sum()))
    return d


def _llamadas(nac, pan, h=4):
    kw = dict(desde="2013Q1", min_train=8)
    return {
        "ar4_nacional": lambda n, p: v2.ar4_nacional(n, "ln_ipc_alquiler", h, **kw),
        "ecm_v1_nacional": lambda n, p: v2.ecm_v1_nacional(n, h, var="p_tasado", **kw),
        "panel_ar4": lambda n, p: v2.panel_ar4(p, "p_tasado", "cod_prov", h, real=True, nac=n, **kw),
        "panel_ecm_v1": lambda n, p: v2.panel_ecm_v1(p, "p_tasado", "cod_prov", h, nac=n, **kw),
    }


@pytest.mark.parametrize("modelo", ["ar4_nacional", "ecm_v1_nacional", "panel_ar4", "panel_ecm_v1"])
def test_no_fuga(datos, modelo):
    nac, pan = datos
    f = _llamadas(nac, pan)[modelo]
    base = f(nac, pan)
    assert len(base) > 0 and base["y_pred"].notna().all()
    sp = base.attrs["splits"]
    lab = _rejilla(nac, pan, modelo)
    # 1) datos posteriores al ULTIMO ORIGEN de test no cambian las predicciones del split
    for sid in (0, 3):
        itr, ite = sp[sid]
        corte = lab[ite[-1]]
        n2, p2 = _perturba(nac, corte), _perturba(pan, corte)
        out = f(n2, p2)
        a = base[base.split == sid].set_index(["unidad", "periodo"]).sort_index()
        b = out[out.split == sid].set_index(["unidad", "periodo"]).sort_index()
        pd.testing.assert_series_equal(a["y_pred"], b["y_pred"], check_exact=False, rtol=1e-9, atol=1e-12)
        # 2) COEFICIENTES (estimación) no cambian al perturbar todo lo posterior al fin del entrenamiento
        corte_tr = lab[itr[-1]]
        out2 = f(_perturba(nac, corte_tr), _perturba(pan, corte_tr))
        ca, cb = base.attrs["coef"][sid], out2.attrs["coef"][sid]
        assert ca.keys() == cb.keys()
        np.testing.assert_allclose([ca[k] for k in ca], [cb[k] for k in ca], rtol=1e-9, atol=1e-12)
        # 3) la predicción del PRIMER origen de test no usa nada posterior a ese origen
        t0 = lab[ite[0]]
        out3 = f(_perturba(nac, t0), _perturba(pan, t0))
        a0 = base[(base.split == sid) & (base.periodo == t0)].set_index("unidad")["y_pred"].sort_index()
        b0 = out3[(out3.split == sid) & (out3.periodo == t0)].set_index("unidad")["y_pred"].sort_index()
        pd.testing.assert_series_equal(a0, b0, check_exact=False, rtol=1e-9, atol=1e-12)


def _rejilla(nac, pan, modelo):
    """Etiquetas de periodo de la rejilla que usa cada predictor (desde el primer nivel disponible)."""
    if modelo == "ar4_nacional":
        d = nac.assign(l=np.log(nac["ipc_alquiler"]))
    elif modelo == "ecm_v1_nacional":
        d = nac.assign(l=np.log(nac["p_tasado"]) - nac["ln_deflactor"])
    else:
        defl = nac.set_index("trimestre")["ln_deflactor"]
        d = pan.assign(l=np.log(pan["p_tasado"]) - pan["trimestre"].map(defl))
    d = d[d["trimestre"].astype(str) <= v2.Q_TRAIN_FIN]
    first = d.loc[d["l"].notna(), "trimestre"].min()
    return sorted(d.loc[d["trimestre"] >= first, "trimestre"].astype(str).unique())


def test_ecm_usa_solo_entrenamiento_en_el_ect(datos):
    nac, _ = datos
    a = v2.ecm_v1_nacional(nac, 4, var="p_tasado", desde="2013Q1", min_train=8)
    assert a.attrs["k_dols"] and not a.attrs["omitidos"]
    assert (a["periodo_obj"].dropna() > a["periodo"].iloc[0]).all()


# ---------------------------------------------------------------- evaluar
def test_evaluar_misma_muestra(datos):
    nac, _ = datos
    kw = dict(desde="2013Q1", min_train=8)
    a = v2.ar4_nacional(nac, "ln_ipc_alquiler", 4, **kw)
    e = v2.ecm_v1_nacional(nac, 4, var="ln_ipc_alquiler", real=False, **kw)
    m = a.assign(modelo="X", y_pred=a["y_pred"] * 0.9)
    e2 = e.iloc[3:]                                  # muestras distintas -> intersección
    r = v2.evaluar(m, {"AR4": a, "ECM_v1": e2}, 4)
    ok = lambda x: set(zip(*x.dropna(subset=["y_real", "y_pred"])[["unidad", "periodo"]].T.values))
    assert r["n"][0] == len(ok(a) & ok(e2))
    assert {"rmse", "mae", "dm_vs_AR4", "dm_vs_ECM_v1"} <= set(r.columns)


# ---------------------------------------------------------------- (d) resultado.json
def _campos(**o):
    c = dict(rama="BM", pregunta="P1", datos="nacional_q_v2", N=10, metodo="m", estimacion={}, ic95=[0, 1],
             p_ajustado=0.1, nivel_evidencia="EXPLORATORIO", diagnosticos={},
             fuera_muestra={"modelo": "x", "rmse": 0.1, "dm_vs_ar4": 1.0}, notas="")
    c.update(o)
    return c


def test_resultado_json(tmp_path):
    ruta = tmp_path / "r" / "resultado.json"
    v2.resultado_json(ruta, **_campos())
    assert ruta.exists()
    for malo in ("causal", "ROBUSTO", "", None):
        with pytest.raises(ValueError):
            v2.resultado_json(ruta, **_campos(nivel_evidencia=malo))
    with pytest.raises(ValueError):
        v2.resultado_json(ruta, **_campos(fuera_muestra={"modelo": "x"}))
    c = _campos()
    del c["notas"]
    with pytest.raises(ValueError):
        v2.resultado_json(ruta, **c)
    for ok in v2.NIVELES_EVIDENCIA:
        v2.resultado_json(ruta, **_campos(nivel_evidencia=ok))


def test_registro_y_presupuesto(tmp_path):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from econ_utils import Registry
    reg = Registry(tmp_path / "reg.csv")
    pr = v2.Presupuesto(reg, "BM", 2, "prueba")
    pr.usar("m1", {"lr": 0.1})
    pr.usar("m2", {"lr": 0.2})
    with pytest.raises(RuntimeError):
        pr.usar("m3", {"lr": 0.3})
    assert len(reg.frame()) == 3 and "lr" in reg.frame()["notas"].iloc[1]
