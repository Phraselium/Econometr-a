"""V18 · E8 (ITP) · estimación y pruebas B4: dCDH con dosis continua (ℓ trimestres), aleatorización de calendarios entre comunidades, adelantos del estudio de
eventos (diferencias del resultado retardado), TWFE con Driscoll-Kraay como alternativa («no fiable»), Sun-Abraham para las bajadas y la coprincipal de V16 (Q6).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Con 7 u 8 comunidades: el Monte Carlo de V18 (dcdh_aleatorizacion) da APTO a la aleatorización
estudentizada de los calendarios (tamaño 0,0455) y NO APTO al bootstrap de Webb (0,12-0,15); el t con G − 1 gl da 0,0655 («con valor crítico corregido»).
Honest DiD con 8 clusters: covarianza de rango ≤ 7, tamaño 0,17 con M̄ = 0: no se usa.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
from herr18 import dcdh as DC  # noqa: E402
from herr18.did import SunAbraham  # noqa: E402
from herr18.driscoll_kraay import fe_dk  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
SEED = K.SEMILLA
TAM_ALEAT = 0.0455      # dcdh_aleatorizacion · itp_desigual_ell4 · aleatorizacion_estudentizada (banda apta)
TAM_T7 = 0.0655         # dcdh_aleatorizacion · itp_desigual_ell4 · t_cluster_7gl (con valor crítico corregido)


def estimar_m(Y: np.ndarray, D: np.ndarray, ell: int, mask: np.ndarray | None = None, beta0=None) -> dict:
    """DID_ℓ de dCDH (la misma fórmula que herramientas.dcdh.estimar) con una máscara opcional sobre el periodo del cambio: los cambiantes solo son
    los de periodos con mask True; los controles siguen siendo las unidades estables. mask=None reproduce el estimador de la herramienta."""
    dD, chg, ctrl = DC._celdas(D, ell)
    T = Y.shape[-1]
    if mask is not None:
        chg = chg & np.asarray(mask)[: chg.shape[-1]]
    dY = Y[..., 1 + ell:] - Y[..., : T - 1 - ell]
    n0 = ctrl.sum(-2)
    valido = n0 > 0
    m = np.where(valido, (dY * ctrl).sum(-2) / np.maximum(n0, 1), 0.0)
    chg = chg & valido[..., None, :]
    s, a = np.sign(dD), np.abs(dD)
    num = (chg * s * (dY - m[..., None, :])).sum((-2, -1))
    den = (chg * a).sum((-2, -1))
    beta = np.where(den > 0, num / np.maximum(den, 1e-300), np.nan)
    b0 = beta if beta0 is None else np.broadcast_to(np.asarray(beta0, float), np.shape(beta))
    St = (chg * s).sum(-2)
    res = dY - m[..., None, :]
    tc = (chg * (s * res - np.asarray(b0)[..., None, None] * a)).sum(-1)
    tk = (ctrl * valido[..., None, :] * (St / np.maximum(n0, 1))[..., None, :] * res).sum(-1)
    IF = (tc - tk) / np.maximum(den, 1e-300)[..., None]
    return {"beta": beta, "IF": IF, "den": den, "chg": chg}


def p_aleat(Y, Dc, cl, theta0: float, ell: int, perms: np.ndarray, mask=None, estud: bool = True) -> float:
    """Aleatorización de Fisher del calendario de dosis entre comunidades (efecto constante θ0), estadístico |β̂/EE| (estudentizado) o |β̂|."""
    M = DC.onehot(cl)
    Dobs = Dc[cl]
    Yt = Y - theta0 * Dobs
    r0 = estimar_m(Yt, Dobs, ell, mask)
    if not np.isfinite(r0["beta"]):
        return float("nan")
    t0 = abs(r0["beta"] / max(float(DC.ee_cluster(r0["IF"], M)), 1e-300)) if estud else abs(r0["beta"])
    st = []
    for b0 in range(0, len(perms), 400):
        pp = perms[b0:b0 + 400]
        Dp = Dc[pp][:, cl, :]
        rp = estimar_m(Yt[None], Dp, ell, mask)
        s = np.abs(rp["beta"]) / np.maximum(DC.ee_cluster(rp["IF"], M), 1e-300) if estud else np.abs(rp["beta"])
        st.append(np.where(np.isfinite(s), s, 0.0))
    st = np.concatenate(st)
    return float((1 + np.sum(st >= t0 - 1e-12)) / (len(st) + 1))


def principal(Y, Dc, cl, ell: int, B: int, B_ic: int, mask=None, semilla: int = SEED, ic: bool = True) -> dict:
    """β̂ de dCDH (ℓ), EE de agrupación por comunidad (t con G − 1 gl), p de aleatorización estudentizada y su IC95 por inversión."""
    G = len(set(cl.tolist())) if not isinstance(cl, int) else cl
    M = DC.onehot(cl)
    D = Dc[cl]
    r = estimar_m(Y, D, ell, mask)
    beta, se = float(r["beta"]), float(DC.ee_cluster(r["IF"], M))
    p_t = float(2 * stats.t.sf(abs(beta / se), G - 1)) if se > 0 else float("nan")
    rng = np.random.default_rng(semilla)
    perms = DC.permutaciones(rng, M.shape[1], B)
    p_a = p_aleat(Y, Dc, cl, 0.0, ell, perms, mask)
    out = {"coef": beta, "se": se, "p_t": p_t, "p_aleat": p_a, "p_aleat_i7": K.p_corr(p_a, TAM_ALEAT), "G": G, "n_obs": int(Y.size),
           "ic_t": (beta - stats.t.ppf(0.975, G - 1) * se, beta + stats.t.ppf(0.975, G - 1) * se)}
    out["p_t_i7"] = K.p_corr(p_t, TAM_T7)
    if ic:
        perms_ic = DC.permutaciones(np.random.default_rng(semilla), M.shape[1], B_ic)
        out["ic_aleat"] = K.ic_por_p(lambda th: p_aleat(Y, Dc, cl, th, ell, perms_ic, mask), beta, max(se, 1e-4))
    else:
        out["ic_aleat"] = (np.nan, np.nan)
    out["tost"] = None
    return out


def webb_no_fiable(Y, Dc, cl, ell: int, B: int, semilla: int = SEED) -> float:
    """p del bootstrap de Webb con 7-8 comunidades: NO APTO en su Monte Carlo (tamaño 0,12-0,15). Solo se rotula."""
    M = DC.onehot(cl)
    return float(DC.p_webb(Y, Dc[cl], 0.0, ell, M, np.random.default_rng(semilla), B))


# --------------------------------------------------------------------------------------------- adelantos (resultado retardado)
def lead_gap(Y: np.ndarray, D: np.ndarray, k: int) -> np.ndarray:
    """β placebo del adelanto k: Σ s·(Y_{t−1} − Y_{t−1−k} − m_t) / Σ|ΔD|, con cambiantes en t sin otro cambio en [t−k, t−1] y controles sin cambio en [t−k, t].
    Admite lote (..., n, T). Un adelanto distinto de cero indica tendencias previas distintas entre unidades que cambian y estables."""
    T = D.shape[-1]
    c = np.concatenate([np.zeros(D.shape[:-1] + (1,), bool), (D[..., 1:] != D[..., :-1])], axis=-1)       # c[..., t]: cambio en t
    cum = np.cumsum(c, axis=-1)
    tt = np.arange(k + 1, T)
    dD = (D[..., 1:] - D[..., :-1])
    dDt = np.concatenate([np.zeros(D.shape[:-1] + (1,)), dD], axis=-1)[..., tt]
    w_chg = cum[..., tt - 1] - cum[..., tt - k - 1]
    w_ctl = cum[..., tt] - cum[..., tt - k - 1]
    chg = c[..., tt] & (w_chg == 0)
    ctl = w_ctl == 0
    dY = Y[..., tt - 1] - Y[..., tt - 1 - k]
    n0 = ctl.sum(-2)
    valido = n0 > 0
    m = np.where(valido, (dY * ctl).sum(-2) / np.maximum(n0, 1), 0.0)
    chg = chg & valido[..., None, :]
    num = (chg * np.sign(dDt) * (dY - m[..., None, :])).sum((-2, -1))
    den = (chg * np.abs(dDt)).sum((-2, -1))
    return np.where(den > 0, num / np.maximum(den, 1e-300), np.nan)


def adelantos(Y, Dc, cl, ks: list[int], B: int, semilla: int = SEED) -> dict:
    """Adelantos k ∈ ks y contraste conjunto por aleatorización de calendarios: estadístico = media de |g_k|."""
    M = DC.onehot(cl)
    D = Dc[cl]
    g = np.array([float(lead_gap(Y, D, k)) for k in ks])
    perms = DC.permutaciones(np.random.default_rng(semilla), M.shape[1], B)
    stat0 = float(np.nanmean(np.abs(g)))
    gk_perm = []
    for b0 in range(0, B, 250):
        pp = perms[b0:b0 + 250]
        Dp = Dc[pp][:, cl, :]
        gk_perm.append(np.stack([lead_gap(Y[None], Dp, k) for k in ks], axis=-1))
    gk_perm = np.concatenate(gk_perm)
    st = np.nanmean(np.abs(gk_perm), axis=-1)
    p_joint = float((1 + np.sum(st >= stat0 - 1e-12)) / (len(st) + 1))
    p_k = {k: float((1 + np.sum(np.abs(gk_perm[:, i]) >= abs(g[i]) - 1e-12)) / (len(gk_perm) + 1)) for i, k in enumerate(ks)}
    return {"ks": ks, "g": g.tolist(), "p_conjunto": p_joint, "p_k": p_k, "perm": gk_perm}


def pendiente_detectable(gk_perm: np.ndarray, ks: list[int], k_ref: int, ell: int) -> dict:
    """Pendiente lineal previa detectable al 80 % (aproximación de Roth por aleatorización): MDE del adelanto de k_ref trimestres dividido entre k_ref, y el
    sesgo que implicaría entre t − 1 y t + ℓ (ℓ + 1 trimestres)."""
    i = ks.index(k_ref)
    mde = K.mde_desde_placebos(gk_perm[:, i])
    pend = mde["mde80"] / k_ref
    return {"mde_adelanto": mde["mde80"], "pendiente_por_trimestre": pend, "sesgo_post": pend * (ell + 1)}


# --------------------------------------------------------------------------------------------- otras estimaciones
def twfe_dk(Y: np.ndarray, Dc: np.ndarray, cl: np.ndarray) -> dict:
    """TWFE de nivel de la dosis acumulada con EE de Driscoll-Kraay (alternativa; «no fiable» en su Monte Carlo)."""
    D = Dc[cl]
    r = fe_dk(Y, D[:, :, None], tiempo=True)
    se = float(np.sqrt(r["V_dk"][0, 0]))
    t = float(r["beta"][0] / se)
    return {"coef": float(r["beta"][0]), "se": se, "p": float(2 * stats.t.sf(abs(t), Y.shape[1] - 1))}


def sun_abraham_bajadas(Y: np.ndarray, Dc: np.ndarray, cl: np.ndarray, B: int, semilla: int = SEED) -> dict:
    """E8-R1-v6: Sun-Abraham para las bajadas (cohorte = primer periodo con ΔD < 0; nunca tratadas = comunidades sin bajadas). Con pocas comunidades tratadas:
    estimación puntual y p de Webb rotulados sin banda de Monte Carlo propia."""
    dD = np.diff(Dc, axis=1)
    primero = np.array([int(np.argmax(r < 0)) + 1 if (r < 0).any() else -1 for r in dD])
    # solo bajadas: se excluyen del contraste las comunidades con subidas posteriores a la bajada no se corrigen (aproximación declarada)
    g = primero[cl]
    n_tr = len(set(cl[g >= 0].tolist()))
    n_co = len(set(cl[g < 0].tolist()))
    if n_tr == 0 or n_co == 0:
        return {"estimable": False, "n_tr": n_tr, "n_co": n_co}
    T = Y.shape[1]
    sa = SunAbraham(g, cl, T)
    p, att, se = sa.p_valor(Y, 0.0, np.random.default_rng(semilla), B)
    return {"estimable": True, "coef": float(att), "se": float(se), "p_webb": float(p), "n_tr": n_tr, "n_co": n_co}


def anual_desde_trimestral(Dc_t: np.ndarray, periodos_t: list[str], anios: list[str]) -> np.ndarray:
    """Dosis anual = nivel en el tercer trimestre de cada año (mitad del año): placebo de resultado con población anual."""
    idx = [periodos_t.index(f"{a}T3") for a in anios]
    return Dc_t[:, idx]
