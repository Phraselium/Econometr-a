"""V18 · El wild cluster bootstrap-t de Callaway-Sant'Anna en forma cerrada coincide con una implementación ingenua (remuestreo explícito de las diferencias por celda)."""
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v18.herramientas.did import CallawaySantAnna, pesos_webb  # noqa: E402


def _ingenuo(Y, coh, cl, T, theta0, V, nulo_impuesto=True):
    gs = sorted(set(coh[coh >= 0].tolist()))
    celdas = [(g, t) for g in gs for t in range(g, T)]
    n_g = {g: (coh == g).sum() for g in gs}
    tot = sum(n_g[g] for g, _ in celdas)
    w = np.array([n_g[g] / tot for g, _ in celdas])
    clusters = np.unique(cl)
    nunca = coh < 0

    def estima(d_cells):                      # d_cells: lista de vectores (n,) por celda
        att_c, psi = [], np.zeros(len(clusters))
        for k, (g, t) in enumerate(celdas):
            d = d_cells[k]
            G = coh == g
            mG, mC = d[G].mean(), d[nunca].mean()
            att_c.append(mG - mC)
            u = np.zeros(len(coh))
            u[G] = (d[G] - mG) / G.sum()
            u[nunca] = -(d[nunca] - mC) / nunca.sum()
            psi += w[k] * np.array([u[cl == c].sum() for c in clusters])
        att = float(w @ np.array(att_c))
        return att, np.sqrt((psi ** 2).sum()), np.array(att_c)

    d0 = [Y[:, t] - Y[:, g - 1] for g, t in celdas]
    att, se, att_c = estima(d0)
    despl = (att - theta0) if nulo_impuesto else 0.0
    t_b = []
    for b in range(V.shape[1]):
        db = []
        for k, (g, t) in enumerate(celdas):
            d = d0[k]
            G = coh == g
            mG, mC = d[G].mean(), d[nunca].mean()
            ajuste = np.zeros(len(coh))
            res = np.zeros(len(coh))
            res[G] = d[G] - mG + despl
            ajuste[G] = mC + att_c[k] + (theta0 - att if nulo_impuesto else 0.0)
            res[nunca] = d[nunca] - mC
            ajuste[nunca] = mC
            vv = np.array([V[list(clusters).index(c), b] for c in cl])
            db.append(ajuste + vv * res)
        a_b, se_b, _ = estima(db)
        t_b.append((a_b - (theta0 if nulo_impuesto else att)) / se_b)     # sin nulo impuesto el bootstrap se centra en la estimación
    return (att - theta0) / se, np.array(t_b)


def test_forma_cerrada_igual_al_remuestreo_ingenuo_una_y_dos_cohortes():
    rng = np.random.default_rng(1)
    for coh in (np.array([3] * 6 + [-1] * 9), np.array([2] * 4 + [4] * 4 + [-1] * 7)):
        n, T = len(coh), 6
        cl = np.arange(n) // 3
        Y = rng.normal(0, 1, (n, T)) + rng.normal(0, 1, (n, 1)) + np.repeat(rng.normal(0, 0.5, (n // 3 + 1, T)), 3, axis=0)[:n]
        est = CallawaySantAnna(coh, cl, T)
        V = pesos_webb(rng, len(np.unique(cl)), 40)
        for th0, imp in ((0.0, True), (0.3, True), (0.0, False)):
            t_obs, t_b, att, se = est.estadisticos(Y, th0, V, imp)
            t_obs_i, t_b_i = _ingenuo(Y, coh, cl, T, th0, V, imp)
            assert abs(t_obs - t_obs_i) < 1e-9
            assert np.allclose(t_b, t_b_i, atol=1e-9)
