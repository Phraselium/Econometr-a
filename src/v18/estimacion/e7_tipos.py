"""V18 · fase 4 · E7 Tipos de interés: proyección local con instrumento (LP-IV), SVAR con instrumento externo y panel provincial con exposición.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md 1.7 y adenda: R-9, AD-E7-R1/R2, 1.3, 1.9, 1.10, 1.12).
Determinista (SEED = 20261010), sin red. Los datos pasan por src/v18/sellado.filtrar (holdout.excluir_sellados_v6() y bloques de V15 y V16). Nunca data/sealed ni evaluate_*.

Instrumento: sorpresas de política monetaria de Jarociński y Karadi (2020, AEJ: Macroeconomics 12(2); DOI 10.1257/mac.20180090), actualizadas con la EA-MPD
(Altavilla et al., 2019, JME 108; DOI 10.1016/j.jmoneco.2019.08.016): data/bib/replicacion/jarocinski_karadi2020/shocks_ecb_mpd_me_m.csv, repositorio
github.com/marekjarocinski/jkshocks_update_ecb (descargado el 2026-10-20; sin licencia declarada: solo local, no se redistribuye; idéntico byte a byte a
data/raw/v16/demanda_internacional/bce_sorpresas/jk_shocks_ecb_mpd_me_m.csv, la ruta del manifiesto de sellado). Se usa como dato; no se usa EA-MPD (E7-A3).

Herramientas: LP-IV y SVAR con proxy son NO APTOS en el Monte Carlo de V18 (output/v18/montecarlo/lp_iv y svar_proxy): se publica la estimación con su etiqueta de
distorsión y, con F < 10, el conjunto de Anderson-Rubin con errores EHW tras aumentar con rezagos. Webb (CR1 t con efectos de año) APTO para el panel (G = 30-39).

Uso: python3 src/v18/estimacion/e7_tipos.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_conjunto as F  # noqa: E402
import f_datos as D  # noqa: E402
import f_nucleo as N  # noqa: E402

RAIZ = N.RAIZ
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry, holm  # noqa: E402
from src.v18.herramientas import lp_iv as L  # noqa: E402
from src.v18.herramientas import svar_proxy as SP  # noqa: E402
from src.v18.herramientas import webb_twfe as WB  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
OUT = RAIZ / "output" / "v18" / "estimacion" / "e7"
ROTULO = F.ROTULO
JK = RAIZ / "data" / "bib" / "replicacion" / "jarocinski_karadi2020" / "shocks_ecb_mpd_me_m.csv"
JK_RAW = RAIZ / "data" / "raw" / "v16" / "demanda_internacional" / "bce_sorpresas" / "jk_shocks_ecb_mpd_me_m.csv"
REFERENCIA = {"precio": -2.0, "cv": -3.0}        # San Juan (2023): −2 % precio y −3 % compraventas a 8 trimestres por +100 pb
SIGMA4_V16 = 1.47 / 2.8 * np.sqrt(101)            # σ del LP a h = 4 del valor tasado, derivada del MDE declarado en V16 Q5 (1,47 % por DT; n = 101): ya visto
H_MAX = 12
HS = list(range(0, H_MAX + 1))
OMIT_1013 = ("2010Q1", "2013Q4")
FUENTES = ["data/bib/replicacion/jarocinski_karadi2020/shocks_ecb_mpd_me_m.csv (Jarociński y Karadi 2020, actualizado con EA-MPD de Altavilla et al. 2019)",
           "base:p_tasado (MIVAU) y base:deflactor hasta 2026T2", "base:tipo_hip_bde y base:euribor_1y hasta 2026T2", "base:pib_vol_idx y base:inflacion_ipc_yoy hasta 2026T2"]

FILAS: list[dict] = []
HECHOS: list[dict] = []
REG: Registry | None = None


def num(x, d=4):
    return F.num(x, d)


def mdev(m: dict):
    """MDE como número, o texto si el contraste no alcanza el 80 % de potencia en toda la rejilla (primera etapa débil)."""
    return num(m["mde"]) if np.isfinite(m["mde"]) else "no detectable (potencia < 80 % en toda la rejilla)"


def mdet(m: dict) -> str:
    return f"{m['mde']:.2f}" if np.isfinite(m["mde"]) else "no detectable (potencia < 80 % en toda la rejilla)"


# ---------------------------------------------------------------------------------------------- datos
def choques_trimestrales() -> pd.DataFrame:
    """Sorpresas mensuales → suma por trimestre (solo trimestres completos hasta 2025T3, tope de sellado_v18.json)."""
    assert hashlib.sha256(JK.read_bytes()).hexdigest() == hashlib.sha256(JK_RAW.read_bytes()).hexdigest(), "los dos ficheros de sorpresas deben coincidir"
    j = pd.read_csv(JK)
    j["periodo"] = j.year.astype(str) + "-" + j.month.astype(str).str.zfill(2)
    out = {}
    for nombre, col in (("z_med", "MP_median"), ("z_pm", "MP_pm"), ("z_tot", "pc1_hf")):
        d = pd.DataFrame({"territorio_codigo": "EZ", "nivel": "zona_euro", "periodo": j.periodo, "valor": j[col]})
        # el choque total (pc1 = MP + CBI) vive en el mismo fichero y con el mismo corte; hereda la clave del choque monetario (desviaciones, punto 3)
        d = D.sellado.filtrar(d, "territorio_codigo", "zona_euro", "periodo", "bce_jk_mp_median_m", "M")
        d["q"] = pd.PeriodIndex(d.periodo, freq="M").asfreq("Q")
        g = d.groupby("q").valor.agg(["sum", "size"])
        out[nombre] = g[g["size"] == 3]["sum"]
    return pd.DataFrame(out)


def macro_trimestral() -> pd.DataFrame:
    d = D.trim_idx(D.base("deflactor", "nacional", "T"))
    s = lambda v: D.trim_idx(D.base(v, "nacional", "T"))      # noqa: E731
    real = lambda v: 100 * np.log(s(v) / d * 100)             # noqa: E731
    M = pd.DataFrame({"y_p": real("p_tasado"), "y_ipv": real("ipv"), "y_cv": 100 * np.log(s("compraventas")), "y_alq": real("ipc_alquiler"),
                      "y_pob": 100 * np.log(s("pob_total")), "hip": s("tipo_hip_bde"), "eur": s("euribor_1y"), "pib": 100 * np.log(s("pib_vol_idx")),
                      "infl": s("inflacion_ipc_yoy")})
    M["dx_hip"] = M.hip.diff()
    M["dx_eur"] = M.eur.diff()
    M["dpib"] = M.pib.diff()
    ch = choques_trimestrales()
    M = M.join(ch)
    M["covid"] = ((M.index >= pd.Period("2020Q2", "Q")) & (M.index <= pd.Period("2020Q3", "Q"))).astype(float)
    return M


# ---------------------------------------------------------------------------------------------- LP-IV con controles
def _res(v, W):
    return v - W @ np.linalg.lstsq(W, v, rcond=None)[0]


def lp_iv_ctrl(y, x, z, ctrl: list[np.ndarray], h, p: int = 4, L_hac: int = 0, omit: np.ndarray | None = None, lags_ctrl: int = 4,
               lags_y: int | None = None, extra: list[np.ndarray] | None = None) -> dict:
    """y_{t+h} − y_{t−1} (o la media de varios horizontes si h es lista) sobre Δi_t instrumentado por z_t, con constante, p rezagos de y (niveles) y de x, y
    `lags_ctrl` rezagos de cada control. Frisch-Waugh como en src/v18/herramientas/lp_iv.py; devuelve el mismo objeto r (a, b, Om, n, beta) más residuos."""
    T = len(y)
    hs = [h] if np.isscalar(h) else list(h)
    hm = max(hs)
    ly = p if lags_y is None else lags_y
    t = np.arange(max(p, lags_ctrl, ly), T - hm)
    cols = [np.ones(len(t))] + [y[t - l] for l in range(1, ly + 1)] + [x[t - l] for l in range(1, p + 1)]
    for c in ctrl:
        cols += [c[t - l] for l in range(1, lags_ctrl + 1)]
    for e in (extra or []):
        cols.append(e[t])
    W = np.column_stack(cols)
    dep = np.mean([y[t + k] - y[t - 1] for k in hs], axis=0)
    ok = np.isfinite(W).all(1) & np.isfinite(dep) & np.isfinite(x[t]) & np.isfinite(z[t])
    if omit is not None:
        ok &= ~omit[t]
    W, dep, xx, zz = W[ok], dep[ok], x[t][ok], z[t][ok]
    n, k = W.shape
    yt, xt, zt = _res(dep, W), _res(xx, W), _res(zz, W)
    a, b = float(zt @ yt), float(zt @ xt)
    s = zt[:, None] * np.column_stack([yt, xt])
    fac = n / max(n - k - 1, 1)
    Om = L.lrv(s, L_hac) * fac
    return {"a": a, "b": b, "Om": Om, "n": n, "beta": a / b if abs(b) > 1e-300 else np.nan, "zt": zt, "xt": xt, "yt": yt, "k": k, "t_idx": t[ok]}


def resumen_lp(y, x, z, ctrl, h, omit=None, p=4, **kw) -> dict:
    """2SLS con Newey-West (h + 1), 2SLS con EHW (aumentada), F robusto, conjunto de Anderson-Rubin (EHW) y p de AR en 0, a un horizonte h."""
    hh = max(h) if not np.isscalar(h) else h
    r_nw = lp_iv_ctrl(y, x, z, ctrl, h, p, L_hac=hh + 1, omit=omit, **kw)
    r_eh = lp_iv_ctrl(y, x, z, ctrl, h, p, L_hac=0, omit=omit, **kw)
    cj = L.conjunto_ar(r_eh)
    se_nw = float(np.sqrt(max(L.var_g(r_nw, r_nw["beta"]), 1e-300) * r_nw["n"] / r_nw["b"] ** 2)) if np.isfinite(r_nw["beta"]) else np.nan
    se_eh = float(np.sqrt(max(L.var_g(r_eh, r_eh["beta"]), 1e-300) * r_eh["n"] / r_eh["b"] ** 2)) if np.isfinite(r_eh["beta"]) else np.nan
    pi = r_eh["b"] / (r_eh["zt"] @ r_eh["zt"])
    return {"beta": r_eh["beta"], "se_nw": se_nw, "se_ehw": se_eh, "p_t_nw": L.p_t(r_nw, 0.0), "p_t_ehw": L.p_t(r_eh, 0.0), "F": L.f_robusto(r_eh), "F_nw": L.f_robusto(r_nw),
            "ar": cj, "p_ar0": L.p_ar(r_eh, 0.0), "pi": float(pi), "n": r_eh["n"], "r_eh": r_eh, "sig_v": float(np.std(r_eh["xt"] - pi * r_eh["zt"]))}


def ar_texto(cj) -> str:
    if cj[0] == "acotado":
        return f"[{cj[1]:.2f}; {cj[2]:.2f}]"
    if cj[0] == "no_acotado":
        return f"toda la recta salvo ({cj[1]:.2f}; {cj[2]:.2f}): no acotado"
    return {"recta": "toda la recta (no acotado)", "vacio": "vacío"}[cj[0]]


# ---------------------------------------------------------------------------------------------- MDE por Monte Carlo
GRID = np.array([0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128])


def mde_lp(zt: np.ndarray, pi: float, sig_v: float, sig_u: float, h: int, R: int, seed: int = SEED) -> dict:
    """MDE al 80 % (AR de EHW al 5 %, bilateral) con la variación real del instrumento (z̃ de la muestra), la primera etapa estimada (π, σ_v) y un error de
    la LP MA(h−1) de desviación típica σ_u (V16 Q5, ya visto). El contraste es el AR en β0 = 0: no depende de la fuerza de la primera etapa para su tamaño."""
    rng = np.random.default_rng(seed)
    n = len(zt)
    v = rng.normal(size=(R, n)) * sig_v
    eps = rng.normal(size=(R, n + h - 1)) if h > 1 else rng.normal(size=(R, n))
    cs = np.cumsum(np.concatenate([np.zeros((R, 1)), eps], axis=1), axis=1)
    u = (cs[:, h:h + n] - cs[:, 0:n]) * (sig_u / np.sqrt(h)) if h > 1 else eps * sig_u
    x = pi * zt[None, :] + v
    pot = []
    for beta in GRID:
        y = beta * x + u
        zy = zt[None, :] * y
        a = zy.sum(1)
        om = ((zy - zy.mean(1, keepdims=True)) ** 2).sum(1)
        ar = a ** 2 / np.maximum(om, 1e-300)
        pot.append(float(np.mean(stats.chi2.sf(ar, 1) < 0.05)))
    pot = np.array(pot)
    k = np.where(pot >= 0.8)[0]
    if len(k) == 0:
        return {"mde": float("inf"), "potencia_en_rejilla_max": float(pot[-1]), "R": R, "rejilla_max": float(GRID[-1])}
    j = k[0]
    mde = float(GRID[j]) if j == 0 else float(np.interp(0.8, pot[j - 1:j + 1], GRID[j - 1:j + 1]))
    return {"mde": mde, "potencia_en_rejilla": {f"{g}": round(float(p_), 3) for g, p_ in zip(GRID, pot)}, "R": R, "seed": seed}


def sigma_propia(y, x, z, ctrl, h, omit=None, **kw) -> float:
    """σ del error de la LP del propio resultado (residuo de y_{t+h} − y_{t−1} sobre los controles), declarada ya vista, cuando V15/V16 no tienen el σ."""
    r = lp_iv_ctrl(y, x, z, ctrl, h, L_hac=0, omit=omit, **kw)
    return float(np.std(r["yt"]))


# ---------------------------------------------------------------------------------------------- especificaciones LP
def ctrl_std(M):
    return [M["dpib"].to_numpy(), M["infl"].to_numpy()]


def omit_mask(M, rango):
    if rango is None:
        return None
    return ((M.index >= pd.Period(rango[0], "Q")) & (M.index <= pd.Period(rango[1], "Q")))


def spec_lp(M: pd.DataFrame, id_: str, estado: str, repite: str, desc: str, y: str, x: str, z: str, h: int, reps: dict, omit=None, ref: float | None = -2.0,
            umbral: float | None = 2.0, sigma: float | None = None, kw: dict | None = None, full_irf: bool = False) -> dict:
    kw = kw or {}
    yv, xv, zv, ctrl = M[y].to_numpy(), M[x].to_numpy(), M[z].to_numpy(), ctrl_std(M)
    om = omit_mask(M, omit)
    # comprobación previa por MDE: antes de mirar el coeficiente (solo primera etapa y variación del instrumento)
    pre = resumen_lp(yv, xv, zv, ctrl, h, om, **kw)
    sig = sigma if sigma is not None else sigma_propia(yv, xv, zv, ctrl, h, om, **kw)
    hmax = h if np.isscalar(h) else max(h)
    h_txt = str(h) if np.isscalar(h) else f"{min(h)}-{max(h)} (media)"
    mde = mde_lp(pre["r_eh"]["zt"], pre["pi"], pre["sig_v"], sig, hmax, reps["mde"])
    estimable = bool(mde["mde"] <= umbral) if umbral is not None else True
    REG.log("E7-prereg", id_, f"y={y}; x={x}; z={z}; h={h}; omit={omit}", str(M.index[0]), str(M.index[-1]), 0, np.nan, np.nan, np.nan,
            notas=f"{estado}; repite_visto={repite}; MDE={mde['mde']:.2f} frente a {umbral}; σ = {sig:.2f} ({'V16 Q5, ya visto' if sigma is not None else 'residuo propio, ya visto'}); estimable={estimable}")
    res = resumen_lp(yv, xv, zv, ctrl, h, om, **kw)
    irf = None
    if full_irf:
        irf = []
        for hh in HS:
            rr = resumen_lp(yv, xv, zv, ctrl, hh, om, **kw)
            irf.append({"h": hh, "beta": num(rr["beta"]), "se_nw": num(rr["se_nw"]), "ar": rr["ar"][0], "ar_lo": num(rr["ar"][1]), "ar_hi": num(rr["ar"][2]),
                        "F": num(rr["F"]), "n": rr["n"]})
    REG.log("E7", id_, f"LP-IV h={h_txt}", str(M.index[0]), str(M.index[-1]), res["n"], np.nan, np.nan, np.nan, coef_interes=res["beta"], p_interes=res["p_ar0"],
            notas=f"F={res['F']:.2f}; AR={ar_texto(res['ar'])}; NO APTO: etiqueta de distorsión")
    return {"id": id_, "estado": estado, "repite_visto": repite, "desc": desc, "y": y, "x": x, "z": z, "h": h_txt, "res": res, "mde": mde, "sigma": sig,
            "estimable": estimable, "umbral": umbral, "ref": ref, "irf": irf, "omit": omit, "muestra": f"{M.index[res['r_eh']['t_idx'][0]]}-{M.index[res['r_eh']['t_idx'][-1]]}"}


def placebo_lp(M: pd.DataFrame, y: str, x: str, z: str, h: int, tipo: str, omit=None) -> dict:
    yv, xv, zv, ctrl = M[y].to_numpy(), M[x].to_numpy(), M[z].to_numpy(), ctrl_std(M)
    if tipo == "adelantado":
        zv = np.concatenate([zv[8:], np.full(8, np.nan)])           # instrumento adelantado ocho trimestres
    elif tipo == "poblacion":
        yv = M["y_pob"].to_numpy()
    r = resumen_lp(yv, xv, zv, ctrl, h, omit_mask(M, omit))
    return {"tipo": tipo, "beta": num(r["beta"]), "p_ar0": num(r["p_ar0"]), "F": num(r["F"]), "n": r["n"], "ar": ar_texto(r["ar"])}


def sup_f_primera_etapa(M: pd.DataFrame, x: str, z: str, h: int = 8) -> dict:
    r = lp_iv_ctrl(M["y_p"].to_numpy(), M[x].to_numpy(), M[z].to_numpy(), ctrl_std(M), h, 4, 0)
    zt, xt, idx = r["zt"], r["xt"], r["t_idx"]
    per = M.index[idx]
    out = {}
    for f in ("2008Q1", "2015Q1"):
        m = per >= pd.Period(f, "Q")
        if m.sum() < 10 or (~m).sum() < 10:
            continue
        b0 = (zt @ xt) / (zt @ zt)
        rss_r = float(((xt - b0 * zt) ** 2).sum())
        rss_u = 0.0
        for mm in (m, ~m):
            bb = (zt[mm] @ xt[mm]) / (zt[mm] @ zt[mm])
            rss_u += float(((xt[mm] - bb * zt[mm]) ** 2).sum())
        out[f] = num(((rss_r - rss_u) / 1) / (rss_u / (len(zt) - 2)))
    return out


def sostenido_h12(M: pd.DataFrame, z: str = "z_med") -> dict:
    """Contribución por cambio sostenido (adenda 1.10): respuesta del precio a h = 12 dividida por la respuesta acumulada del propio tipo a h = 12 con la misma
    proyección local e instrumento (razón de formas reducidas: no depende de la primera etapa). Banda por el método delta con EHW."""
    ctrl = ctrl_std(M)
    zv, xv = M[z].to_numpy(), M["dx_hip"].to_numpy()
    rp = lp_iv_ctrl(M["y_p"].to_numpy(), xv, zv, ctrl, 12, 4, 0)
    lvl = M["hip"].to_numpy()
    rx = lp_iv_ctrl(lvl, xv, zv, ctrl, 12, 4, 0)
    n = rp["n"]
    zt = rp["zt"]
    S = np.column_stack([zt * rp["yt"], zt * rx["yt"]])
    Om = L.lrv(S, 0)
    ap, ax = rp["a"] / n, rx["a"] / n
    r = ap / ax
    var = (Om[0, 0] - 2 * r * Om[0, 1] + r ** 2 * Om[1, 1]) / n / ax ** 2
    se = float(np.sqrt(max(var, 0)))
    return {"razon": num(r), "se_delta": num(se), "ic95": [num(r - 1.96 * se), num(r + 1.96 * se)], "n": n, "respuesta_propia_tipo_h12_por_pp_sorpresa": num(ax / (zt @ zt / n)),
            "nota": "razón de formas reducidas a h = 12; sin cambio sostenido más allá del horizonte estimado: «fuera del horizonte estimado», sin cifra"}


# ---------------------------------------------------------------------------------------------- SVAR con proxy
def _prep_svar(M: pd.DataFrame, cols: list[str], z: str, omit=None, ini="2007Q1"):
    d = M[cols + [z]].loc[ini:].dropna()
    Y = d[cols].to_numpy()
    zz = d[z].to_numpy().copy()
    if omit is not None:
        m = ((d.index >= pd.Period(omit[0], "Q")) & (d.index <= pd.Period(omit[1], "Q")))
        zz[m] = zz[~m].mean()
    return Y, zz, d.index


def spec_svar(M: pd.DataFrame, id_: str, estado: str, repite: str, desc: str, cols: list[str], z: str, reps: dict, omit=None, p: int = 2, h: int = 8,
              ref: float | None = -2.0, umbral: float | None = 2.0, full_irf: bool = False) -> dict:
    Y, zz, idx = _prep_svar(M, cols, z, omit)
    j = cols.index("y_p")
    r = SP.proxy_svar(Y, zz, p, h, j, 0, 4)
    cj = L.conjunto_ar(r)
    Fr = L.f_robusto(r)
    # MDE: primera etapa y variación del proxy reales; σ del error de la IRF de h = 8 derivada de V16 Q5 (ya visto) con escala √(h/4); AR delta en β0 = 0 por simulación
    # paramétrica del mismo VAR (impacto del choque en el precio fijado para que la respuesta a h sea 0 y desplazado en rejilla)
    mde = mde_svar(Y, zz, p, h, j, reps["mde_svar"])
    estimable = bool(mde["mde"] <= umbral) if umbral is not None else True
    REG.log("E7-prereg", id_, f"SVAR proxy {cols}; p={p}; h={h}; omit={omit}", str(idx[0]), str(idx[-1]), 0, np.nan, np.nan, np.nan,
            notas=f"{estado}; repite_visto={repite}; MDE={mde['mde']:.2f} frente a {umbral}; estimable={estimable}")
    irf = None
    if full_irf:
        irf = []
        for hh in HS:
            rr = SP.proxy_svar(Y, zz, p, hh, j, 0, 4)
            c2 = L.conjunto_ar(rr)
            irf.append({"h": hh, "beta": num(rr["beta"]), "ar": c2[0], "ar_lo": num(c2[1]), "ar_hi": num(c2[2]), "F": num(L.f_robusto(rr))})
    Als = r["Als"]
    comp = np.zeros((Y.shape[1] * p, Y.shape[1] * p))
    comp[:Y.shape[1], :] = np.hstack(list(Als))
    comp[Y.shape[1]:, :-Y.shape[1]] = np.eye(Y.shape[1] * (p - 1))
    rho = float(np.max(np.abs(np.linalg.eigvals(comp))))
    se = float(np.sqrt(max(L.var_g(r, r["beta"]), 1e-300) * r["n"] / r["b"] ** 2)) if np.isfinite(r["beta"]) else np.nan
    REG.log("E7", id_, f"SVAR proxy h={h}", str(idx[0]), str(idx[-1]), r["n"], np.nan, np.nan, np.nan, coef_interes=r["beta"], p_interes=L.p_ar(r, 0.0),
            notas=f"F={Fr:.2f}; AR={ar_texto(cj)}; NO APTO: etiqueta de distorsión")
    return {"id": id_, "estado": estado, "repite_visto": repite, "desc": desc, "cols": cols, "z": z, "h": h, "p": p, "res": {"beta": r["beta"], "se_delta": se, "F": Fr, "ar": cj,
            "p_ar0": L.p_ar(r, 0.0), "p_t": L.p_t(r, 0.0), "n": r["n"], "pi": None}, "mde": mde, "estimable": estimable, "umbral": umbral, "ref": ref, "irf": irf,
            "raiz_maxima_VAR": rho, "omit": omit, "muestra": f"{idx[0]}-{idx[-1]}"}


def mde_svar(Y, z, p, h, j, R, seed=SEED) -> dict:
    """MDE del SVAR con proxy por Monte Carlo paramétrico: proceso generador = VAR(p) estimado + choque estructural s_t con vector de impacto b (b[0] = 1) y proxy
    z = λ s + ruido (λ y la varianza del ruido calibradas con la covarianza proxy-residuos de los datos); la respuesta del precio a h se fija en 0 (nula) o
    en θ (rejilla) moviendo b[j]. Potencia del AR delta frente a θ = 0 al 5 %."""
    B, U, X = SP.var_ols(Y, p)
    n = Y.shape[1]
    Als = SP._lags(B, p)
    zz = z[p:] - z[p:].mean()
    m = (zz[:, None] * U).mean(0)
    b = m / m[0]
    Su = np.cov(U.T)
    lam = 1.0
    sig_s2 = max(abs(float(m[0])), 1e-6)       # fuerza observada del proxy (el signo no cambia la potencia del AR)
    Se = Su - sig_s2 * np.outer(b, b)
    w, V = np.linalg.eigh((Se + Se.T) / 2)
    Se = V @ np.diag(np.maximum(w, 1e-8)) @ V.T
    Ch = np.linalg.cholesky(Se)
    var_z = max(float(zz.var()) - lam ** 2 * sig_s2, 1e-8)
    Psi_h = SP.psi(Als, h)
    # impacto del precio tal que Ψ_h[j,:] b = 0
    otros = Psi_h[j, :] @ b - Psi_h[j, j] * b[j]
    b0 = b.copy()
    b0[j] = -otros / Psi_h[j, j] if abs(Psi_h[j, j]) > 1e-8 else b[j]
    grid = [0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32]
    T = len(Y)
    rng = np.random.default_rng(seed)
    pot = np.zeros(len(grid))
    c = B[:, 0]
    for r in range(R):
        s = rng.normal(size=T + 50) * np.sqrt(sig_s2)
        e = rng.normal(size=(T + 50, n)) @ Ch.T
        zs = lam * s + rng.normal(size=T + 50) * np.sqrt(var_z)
        for gi, th in enumerate(grid):
            bb = b0.copy()
            bb[j] = b0[j] + th / Psi_h[j, j]
            Ys = np.zeros((T + 50, n))
            for t_ in range(p, T + 50):
                lag = sum(Als[l] @ Ys[t_ - 1 - l] for l in range(p))
                Ys[t_] = c + lag + bb * s[t_] + e[t_]
            rr = SP.proxy_svar(Ys[50:], zs[50:], p, h, j, 0, 4)
            if np.isfinite(rr["b"]) and abs(rr["b"]) > 1e-12:
                pot[gi] += float(L.p_ar(rr, 0.0) < 0.05)
        if r == 0 and R > 400:
            pass
    pot /= R
    k = np.where(pot >= 0.8)[0]
    if len(k) == 0:
        return {"mde": float("inf"), "potencia_en_rejilla": {str(g): round(float(p_), 3) for g, p_ in zip(grid, pot)}, "R": R}
    jj = k[0]
    mde = float(grid[jj]) if jj == 0 else float(np.interp(0.8, pot[jj - 1:jj + 1], grid[jj - 1:jj + 1]))
    return {"mde": mde, "potencia_en_rejilla": {str(g): round(float(p_), 3) for g, p_ in zip(grid, pot)}, "R": R, "seed": seed,
            "nota": "VAR estimado como proceso generador, ruido normal; el σ de la respuesta sale del propio VAR (sin σ de V15/V16 para el SVAR)"}


# ---------------------------------------------------------------------------------------------- panel provincial con exposición (E7-A2)
def exposicion_hipoteca(ini: int = 2007, fin: int = 2019) -> pd.Series:
    """E_p = Σ hipotecas sobre vivienda (número) / Σ compraventas de vivienda (total), 2007-2019, por provincia (INE; sellado hip_n|provincia|M y compraventas|provincia|M)."""
    def leer(f, filtro, clave):
        d = pd.read_csv(D.RAW / f)
        d = d[filtro(d)].copy()
        d["territorio_codigo"] = d["codigo"].astype(str).str.zfill(2)
        d["periodo"] = d["periodo"].str.replace("M", "-", regex=False)
        d["nivel"] = "provincia"
        return D.sellado.filtrar(d[["territorio_codigo", "nivel", "periodo", "valor"]], "territorio_codigo", "provincia", "periodo", clave, "M")
    h = leer("ine_v2_hipotecas_prov.csv", lambda d: (d.medida == "hipotecas_viviendas_numero") & (d.nivel == "provincia"), "hip_n")
    c = leer("ine_v2_etdp_prov.csv", lambda d: (d.medida == "compraventas_viviendas") & (d.desglose == "total") & (d.nivel == "provincia"), "compraventas")
    for d in (h, c):
        d["anio"] = d.periodo.str[:4].astype(int)
    h = h[(h.anio >= ini) & (h.anio <= fin)].groupby("territorio_codigo").valor.sum()
    c = c[(c.anio >= ini) & (c.anio <= fin)].groupby("territorio_codigo").valor.sum()
    return (h / c).dropna()


def panel_valor_tasado_trimestral() -> pd.DataFrame:
    v = D.base("valor_tasado", "provincia", "T")
    W = v.pivot(index="periodo", columns="territorio_codigo", values="valor")
    W.index = pd.PeriodIndex([s.replace("T", "Q") for s in W.index], freq="Q")
    return np.log(W).sort_index()


def a2_arrays(lnp: pd.DataFrame, M: pd.DataFrame, E: pd.Series, z: str, h: int, ini: str = "2002Q2", excluir: list[str] | None = None, lag_z: int = 0):
    """y (N, T): 100 [ln p_{t+h} − ln p_{t−1}]; D (N, T): choque_t × E_p. Panel balanceado de provincias con todos los periodos."""
    excl = set(excluir or [])
    cols = [c for c in lnp.columns if c in E.index and c not in excl]
    zq = M[z].dropna()
    ult = min(zq.index[-1], lnp.index[-1] - h)
    orig = pd.period_range(ini, ult, freq="Q")
    ok = [c for c in cols if lnp.loc[orig[0] - 1:orig[-1] + h, c].notna().all()]
    Y = np.stack([100 * (lnp.loc[orig + h, c].to_numpy() - lnp.loc[orig - 1, c].to_numpy()) for c in ok])
    Dm = np.stack([zq.reindex(orig - lag_z).to_numpy() * E[c] for c in ok])
    return Y, Dm, ok, orig


def spec_a2(lnp, M, E, id_, estado, repite, desc, reps, h=8, excluir=None, E_alt=None, B=None, z="z_med") -> dict:
    Ee = E if E_alt is None else E_alt
    Y, Dm, ok, orig = a2_arrays(lnp, M, Ee, z, h, excluir=excluir)
    n, T = Y.shape
    # MDE: ruido = residuos de dos vías de y (sin el regresor) remuestreados por bloques de h periodos (conserva la dependencia transversal y la MA(h − 1))
    e0 = WB.desmedia2(Y)
    Dt = WB.desmedia2(Dm)
    sdd = float((Dt ** 2).sum())
    rngm = np.random.default_rng(SEED)

    def sim(rng):
        idx = N._bloques(T, max(h, 2), rng)
        ys = WB.desmedia2(e0[:, idx])
        b = float((Dt * ys).sum() / sdd)
        es = ys - b * Dt
        sc = (Dt * es).sum(1)
        c = n / (n - 1) * (n * T - 1) / (n * T - T)
        return b, float(np.sqrt(c * (sc ** 2).sum()) / sdd)
    mde = N.mde_mc(sim, reps["mde_a2"], SEED)
    REG.log("E7-prereg", id_, f"panel: Δ_{h} ln p ~ choque × E_p; FE de provincia y de periodo", str(orig[0]), str(orig[-1]), 0, np.nan, np.nan, np.nan,
            notas=f"{estado}; repite_visto={repite}; MDE={mde['mde']:.3f} (sin referencia: 2δ = 2,0 en pp); σ de los residuos de dos vías (ya visto)")
    rng = np.random.default_rng(SEED + h)
    B_ = B or reps["webb"]
    p_w, tt, b_, se_ = WB.wcr_webb(Y, Dm, 0.0, B_, rng)
    gl = n - 1
    lo, hi = b_ - stats.t.ppf(0.975, gl) * se_, b_ + stats.t.ppf(0.975, gl) * se_
    resid = WB.desmedia2(Y) - b_ * Dt
    cd = F.cd_pesaran(resid)
    REG.log("E7", id_, f"panel h={h}", str(orig[0]), str(orig[-1]), n * T, np.nan, np.nan, np.nan, coef_interes=b_, p_interes=p_w, notas=f"G={n}; Webb B={B_}")
    return {"id": id_, "estado": estado, "repite_visto": repite, "desc": desc, "h": h, "beta": b_, "se_cr1": se_, "p_webb": p_w, "ic95_t": [lo, hi], "G": n, "T": T, "mde": mde,
            "cd": cd, "muestra": f"{orig[0]}-{orig[-1]}", "excluidas": excluir or []}


# ---------------------------------------------------------------------------------------------- clasificación y publicación
def banda_lp(F_: float, ar) -> str:
    if F_ > 10:
        return "F efectivo > 10"
    return "F efectivo < 10" if F_ >= 5 else "F efectivo < 5"


def clasificar_lp(sp: dict, placebos: dict | None, p_holm: float | None, signo_igual: float | None) -> tuple[str, list[str]]:
    """Reglas de la adenda 1.2 con el gate de la 1.3. Clase provisional (falta I8)."""
    if not sp["estimable"]:
        return "NO ESTIMABLE", [f"NO ESTIMABLE por variación: MDE {mdet(sp['mde'])} > {sp['umbral']}"]
    r = sp["res"]
    motivos = []
    F_ = r["F"]
    ar_acot = r["ar"][0] == "acotado"
    decisivo = (F_ < 5 and not ar_acot)
    if decisivo:
        motivos.append("F efectivo < 5 con AR no acotado: fallo decisivo (I2)")
    elif F_ < 10:
        motivos.append("F efectivo < 10: tope SUGESTIVO (R-9)")
    if placebos:
        for k, v in placebos.items():
            if v["p_ar0"] is not None and v["p_ar0"] < 0.05:
                motivos.append(f"placebo {k} significativo al 5 %")
                decisivo = True
    if signo_igual is not None and signo_igual < 0.8:
        motivos.append("menos del 80 % de las variantes con el mismo signo (I5)")
    if decisivo:
        return "ASOCIACIÓN", motivos
    i7 = p_holm is not None and p_holm < 0.05
    debil = F_ < 10 or (signo_igual is not None and signo_igual < 0.8)
    if i7 and not debil:
        return "IDENTIFICADO", motivos
    return ("SUGESTIVO" if (i7 or debil) else "NO CONCLUYENTE"), motivos


def criterios_i(sp: dict, plac: dict | None, signo: float | None, p_holm: float | None) -> dict:
    """Criterios I1-I8 de la adenda 1.2 para una especificación de E7 (resumen legible; I8 la hace el orquestador, B6)."""
    r = sp["res"]
    F_ = r["F"]
    ar_acot = r["ar"][0] == "acotado"
    out = {"I1_diseno": "LP-IV con sorpresas de alta frecuencia del BCE como instrumento externo (supuestos: relevancia, exclusión y monotonía de la sorpresa monetaria pura); cumple como diseño",
           "gate_MDE_1.3": f"{'supera' if sp['estimable'] else 'NO supera'} (MDE {mdet(sp['mde'])} frente a {sp['umbral']})",
           "I2_primera_etapa": f"F efectivo {F_:.2f}; AR {'acotado' if ar_acot else 'no acotado'}: " + ("supera" if (F_ > 10 or ar_acot) else "no supera") + (" (fallo decisivo: F < 5 y AR no acotado)" if F_ < 5 and not ar_acot else ""),
           "I3_pretendencias": "no aplica a una serie temporal con instrumento; se sustituye por los placebos de I4 y por el sup-F de la primera etapa (diagnósticos)"}
    if plac:
        out["I4_placebos"] = {k: f"p AR {v['p_ar0']} ({'supera' if v['p_ar0'] is not None and v['p_ar0'] > 0.10 else 'no supera'})" for k, v in plac.items()}
    out["I5_robustez"] = f"{signo:.2f} de las variantes con el mismo signo (se exige 0,80): " + ("supera" if signo is not None and signo >= 0.8 else "no supera") if signo is not None else "sin variantes comparables"
    out["I6_etiqueta"] = etiqueta_i6(r["beta"], sp["ref"])
    out["I7_significacion"] = (f"p Holm {p_holm:.3f}" if p_holm is not None else "fuera de la familia de Holm (no estimable)") + f"; p AR en 0 = {r['p_ar0']:.3f}"
    out["I8_replica_ciega"] = "pendiente (B6)"
    return out


def etiqueta_i6(beta: float, ref: float | None) -> str:
    if ref is None or not np.isfinite(beta):
        return "sin referencia comparable"
    razon = beta / ref
    return f"{'coherente' if 1 / 3 <= razon <= 3 else 'no coherente'} con San Juan (2023) ({ref:+.1f}), razón {razon:.2f}"


def hecho(id_, indicador, valor, lo, hi, unidad, periodo, cobertura, clase, nota):
    HECHOS.append({"id": id_, "indicador": indicador, "valor": num(valor), "min": num(lo), "max": num(hi), "unidad": unidad, "periodo": periodo, "cobertura": cobertura,
                   "fuentes": FUENTES, "capa": "C4", "clasificacion_v18": clase, "nota": f"{nota} [{ROTULO}]"})


NOTA_NO_APTO = ("LP-IV con Newey-West (h + 1): NO APTO en el Monte Carlo de V16 y de V18 (tamaño 0,07-0,115 con instrumento fuerte); AR aumentado con EHW, el único cercano al "
                "nominal bajo el nulo (0,049-0,069), con cobertura bajo la alternativa de 0,77-0,96 por la atenuación con T = 108 (10 %, 22 % y 38 % a h = 4, 8 y 12). "
                "Se publica con esa etiqueta y la clasificación no se apoya en ella.")


def publicar_lp(sp: dict, clase: str, motivos: list[str], p_holm: float | None, extra_nota: str = "") -> None:
    r = sp["res"]
    cj = r["ar"]
    unidad = "% del precio por +100 pb del tipo (acumulado a h trimestres; LP-IV)" if sp["y"] != "y_cv" else "% de las compraventas por +100 pb del tipo (LP-IV)"
    if sp["y"] == "y_alq":
        unidad = "% del IPC de alquiler real por +100 pb del tipo (LP-IV)"
    lo, hi = (cj[1], cj[2]) if cj[0] == "acotado" else (None, None)
    nota = (f"{ROTULO.split(';')[0]}. {sp['desc']}. 2SLS {r['beta']:.2f} (error típico NW h+1 {r['se_nw']:.2f}; EHW {r['se_ehw']:.2f}); F efectivo (EHW) {r['F']:.2f}; primera etapa π = {r['pi']:.3f} "
            f"({'signo contrario al esperado (cae el tipo ante una sorpresa restrictiva)' if r['pi'] < 0 else 'signo esperado'}); conjunto AR 95 % (EHW) {ar_texto(cj)}; p AR en 0 = {r['p_ar0']:.3f}. "
            f"MDE {mdet(sp['mde'])} frente al umbral {sp['umbral']} (σ {sp['sigma']:.2f}). {NOTA_NO_APTO} "
            f"I6 (etiqueta, no decide): {etiqueta_i6(r['beta'], sp['ref'])}. {'; '.join(motivos)}. {extra_nota}")
    nom_y = {"y_p": "del precio real (valor tasado)", "y_ipv": "del IPV real", "y_cv": "de las compraventas", "y_alq": "del IPC de alquiler real"}.get(sp["y"], sp["y"])
    hecho(f"V18-{sp['id']}", f"Respuesta {nom_y} a un aumento de 100 pb del tipo hipotecario a {sp['h']} trimestres ({sp['id']})",
          r["beta"], lo, hi, unidad, sp["muestra"], "nacional", clase, nota)
    FILAS.append({"id": sp["id"], "familia": "E7", "estado": sp["estado"], "repite_visto": sp["repite_visto"], "muestra": sp["muestra"], "N": r["n"], "h": sp["h"],
                  "beta_2sls": num(r["beta"]), "se_nw": num(r["se_nw"]), "se_ehw": num(r["se_ehw"]), "F_efectivo": num(r["F"]), "pi_primera_etapa": num(r["pi"]),
                  "ar_tipo": cj[0], "ar_lo": num(cj[1]), "ar_hi": num(cj[2]), "p_ar0": num(r["p_ar0"], 4), "p_holm": num(p_holm, 4), "mde": mdev(sp["mde"]),
                  "umbral_mde": sp["umbral"], "estimable": sp["estimable"], "I6": etiqueta_i6(r["beta"], sp["ref"]), "clasificacion_v18": clase, "nota": nota})


# ---------------------------------------------------------------------------------------------- principal
REPS_FULL = {"mde": 2000, "mde_svar": 2000, "mde_a2": 2000, "webb": 9999}
REPS_RAPIDO = {"mde": 100, "mde_svar": 12, "mde_a2": 100, "webb": 499}


def main(rapido: bool = False, salida: Path | None = None) -> dict:
    global REG, OUT
    reps = REPS_RAPIDO if rapido else REPS_FULL
    if salida:
        OUT = salida
    OUT.mkdir(parents=True, exist_ok=True)
    FILAS.clear()
    HECHOS.clear()
    REG = Registry(OUT / "registro.csv")
    M = macro_trimestral()
    sig4 = SIGMA4_V16
    sg = lambda h: sig4 * np.sqrt(h / 4)       # noqa: E731
    S: dict[str, dict] = {}
    # R1 principal (precio) y sus variantes
    S["E7-R1"] = spec_lp(M, "E7-R1", "principal", "sí (Q5; V8 H8-5 a H8-7)", "LP-IV, valor tasado real, h = 8, sorpresa monetaria pura (mediana)", "y_p", "dx_hip", "z_med", 8, reps,
                         sigma=sg(8), full_irf=True)
    v = {"E7-R1-v1": dict(desc="sin 2010-2013 (origen)", omit=OMIT_1013), "E7-R1-v3": dict(desc="sorpresa «poor man's»", z="z_pm"),
         "E7-R1-v5": dict(desc="choque total (pc1)", z="z_tot"), "E7-R1-v7": dict(desc="euríbor a 1 año como endógena", x="dx_eur"),
         "E7-R1-v8": dict(desc="h = 4", h=4), "E7-R1-v9": dict(desc="h = 12", h=12)}
    for k, o in v.items():
        h_ = o.get("h", 8)
        S[k] = spec_lp(M, k, "variante", "sí", f"E7-R1: {o['desc']}", "y_p", o.get("x", "dx_hip"), o.get("z", "z_med"), h_, reps, omit=o.get("omit"), sigma=sg(h_))
    S["E7-R1-v6"] = spec_lp(M, "E7-R1-v6", "variante", "sí", "E7-R1 con 2SLS aumentado y errores EHW (la inferencia principal es la misma; se muestra el 2SLS-EHW)", "y_p", "dx_hip", "z_med", 8, reps, sigma=sg(8))
    # R1 en otras medidas
    S["E7-R1-ipv"] = spec_lp(M, "E7-R1-ipv", "principal", "sí", "LP-IV, IPV real (desde 2007), h = 8", "y_ipv", "dx_hip", "z_med", 8, reps, sigma=None)
    S["E7-R1-cv"] = spec_lp(M, "E7-R1-cv", "principal", "sí", "LP-IV, compraventas (desde 2007), h = 8", "y_cv", "dx_hip", "z_med", 8, reps, ref=-3.0, umbral=3.0, sigma=None)
    S["E7-R1-alq"] = spec_lp(M, "E7-R1-alq", "principal", "sí", "LP-IV, IPC de alquiler real (desde 2002), h = 8", "y_alq", "dx_hip", "z_med", 8, reps, ref=None, umbral=2.0, sigma=None)
    # coprincipales: P-Q5 (forma reducida de V16 Q5) y P-H8-5 / P-H8-6 (euríbor, h = 4-8 agregado, 2 retardos y COVID)
    S["E7-P-Q5"] = spec_lp(M, "E7-P-Q5", "coprincipal", "sí (V16 Q5)", "forma reducida de Q5: LP a h = 4 de la sorpresa (MCO), 4 rezagos", "y_p", "z_med", "z_med", 4, reps, sigma=sg(4),
                           ref=-0.6, umbral=None)
    S["E7-P-H8-5"] = spec_lp(M, "E7-P-H8-5", "coprincipal", "sí (V8 H8-5)", "V8 IV1: LP-IV valor tasado real, euríbor, h = 4-8 agregado, 2 retardos y COVID", "y_p", "dx_eur", "z_med", list(range(4, 9)),
                             reps, sigma=sg(6), ref=-2.0, umbral=None, kw={"lags_ctrl": 2, "p": 2, "extra": [M["covid"].to_numpy()], "lags_y": 2})
    S["E7-P-H8-6"] = spec_lp(M, "E7-P-H8-6", "coprincipal", "sí (V8 H8-6)", "V8 IV1: LP-IV IPC de alquiler real, euríbor, h = 4-8 agregado, 2 retardos y COVID", "y_alq", "dx_eur", "z_med",
                             list(range(4, 9)), reps, sigma=None, ref=None, umbral=None, kw={"lags_ctrl": 2, "p": 2, "extra": [M["covid"].to_numpy()], "lags_y": 2})
    # diagnósticos de R1
    diag = {"series": {c: F.adf_kpss(M[c].dropna()) for c in ("y_p", "hip", "eur", "pib", "infl")},
            "placebos_R1": {"choque_adelantado_8": placebo_lp(M, "y_p", "dx_hip", "z_med", 8, "adelantado"),
                            "poblacion_total": placebo_lp(M, "y_p", "dx_hip", "z_med", 8, "poblacion")},
            "estabilidad_primera_etapa": sup_f_primera_etapa(M, "dx_hip", "z_med"),
            "sensibilidad_a_la_identificacion": {k: {"beta_2sls": num(S[k]["res"]["beta"]), "F": num(S[k]["res"]["F"]), "ar": ar_texto(S[k]["res"]["ar"])}
                                                 for k in ("E7-R1", "E7-R1-v3", "E7-R1-v5", "E7-R1-v7")},
            "sostenido_h12": sostenido_h12(M),
            "primera_etapa_signo": "V8 y Q5 ya dieron signo contrario o F de 2,1 a 2,9: aquí se publica la π estimada de cada especificación",
            "diferencial_soberano": "NO ESTIMABLE: no hay serie trimestral del diferencial soberano a 10 años en el repositorio (solo anual, irt_lt_mcby_a, sin clave en sellado_v18.json); se necesita la serie mensual del BCE"}
    # SVAR
    base_cols = ["hip", "y_p", "y_cv", "pib", "infl", "eur"]
    S["E7-R2"] = spec_svar(M, "E7-R2", "principal", "sí (V8 H8-5 a H8-7)", "SVAR con proxy: [tipo hipotecario, ln precio real, ln compraventas, ln PIB, inflación, euríbor], p = 2, h = 8",
                           base_cols, "z_med", reps, full_irf=True)
    S["E7-R2-v1"] = spec_svar(M, "E7-R2-v1", "variante", "sí", "E7-R2 sin 2010-2013 en el momento del proxy", base_cols, "z_med", reps, omit=OMIT_1013)
    S["E7-R2-v3"] = spec_svar(M, "E7-R2-v3", "variante", "sí", "E7-R2 con VAR de 4 variables [tipo, precio, PIB, inflación]", ["hip", "y_p", "pib", "infl"], "z_med", reps)
    S["E7-R2-v4"] = spec_svar(M, "E7-R2-v4", "variante", "sí", "E7-R2 con la sorpresa «poor man's»", base_cols, "z_pm", reps)
    # panel provincial con exposición
    lnp = panel_valor_tasado_trimestral()
    E = exposicion_hipoteca(2007, 2019)
    E13 = exposicion_hipoteca(2007, 2013)
    A2 = {}
    for h_ in (4, 8, 12):
        A2[f"E7-A2-h{h_}"] = spec_a2(lnp, M, E, f"E7-A2" if h_ == 8 else f"E7-A2-h{h_}", "principal" if h_ == 8 else "variante", "sí (V9-D5)",
                                     f"panel provincial, choque × exposición hipotecaria 2007-2019, h = {h_}", reps, h=h_, B=reps["webb"] if h_ == 8 else min(999, reps["webb"]))
    A2["E7-A2-v2"] = spec_a2(lnp, M, E, "E7-A2-v2", "variante", "sí", "sin Barcelona", reps, h=8, excluir=["08"], B=min(999, reps["webb"]))
    A2["E7-A2-v3"] = spec_a2(lnp, M, E, "E7-A2-v3", "variante", "sí", "exposición 2007-2013", reps, h=8, E_alt=E13, B=min(999, reps["webb"]))
    return {"reps": reps, "S": S, "diag": diag, "A2": A2, "M": M, "E": E}


# ---------------------------------------------------------------------------------------------- publicación
def no_estimable(id_: str, estado: str, desc: str, motivo: str, repite: str = "—") -> None:
    REG.log("E7-prereg", id_, desc, "", "", 0, np.nan, np.nan, np.nan, notas=f"NO ESTIMABLE: {motivo}")
    FILAS.append({"id": id_, "familia": "E7", "estado": estado, "repite_visto": repite, "estimable": False, "clasificacion_v18": "NO ESTIMABLE" if estado != "coprincipal" else "no se clasifica",
                  "nota": motivo})
    if estado != "coprincipal":
        hecho(f"V18-{id_}", f"{desc}: no estimable", None, None, None, "—", "", "nacional", "NO ESTIMABLE", motivo)


def finalizar(res: dict) -> dict:
    S, A2, diag = res["S"], res["A2"], res["diag"]
    M = res["M"]
    # I5: proporción de variantes enumeradas con el mismo signo que la principal (precio a 8 trimestres)
    b0 = S["E7-R1"]["res"]["beta"]
    var_ids = ["E7-R1-v1", "E7-R1-v3", "E7-R1-v5", "E7-R1-v7", "E7-R1-v8", "E7-R1-v9", "E7-R1-v6"]
    signo = float(np.mean([np.sign(S[k]["res"]["beta"]) == np.sign(b0) for k in var_ids]))
    diag["I5_proporcion_mismo_signo_R1"] = {"proporcion": num(signo), "variantes": var_ids,
                                            "nota": "v2 (diferencial soberano) es NO ESTIMABLE y v4 (mediana) coincide con la principal"}
    # familia de Holm: contrastes de las estimables (principales y coprincipales), p de AR (EHW), de AR delta (SVAR) o de Webb (panel)
    fam: dict[str, float] = {}
    for k in ("E7-R1", "E7-R1-ipv", "E7-R1-cv", "E7-R1-alq", "E7-P-Q5", "E7-P-H8-5", "E7-P-H8-6"):
        if S[k]["estimable"]:
            fam[k] = S[k]["res"]["p_ar0"]
    if S["E7-R2"]["estimable"]:
        fam["E7-R2"] = S["E7-R2"]["res"]["p_ar0"]
    if A2["E7-A2-h8"]["mde"]["mde"] <= 2.0:
        fam["E7-A2"] = A2["E7-A2-h8"]["p_webb"]
    hp = holm(fam) if fam else {}
    # clasificación y publicación de LP-IV
    plac = diag["placebos_R1"]
    clases: dict[str, str] = {}
    for k, sp in S.items():
        if k.startswith("E7-R2"):
            continue
        es_var = sp["estado"] == "variante"
        if sp["estado"] == "coprincipal":
            clases[k] = "no se clasifica"
            FILAS.append({"id": k, "familia": "E7", "estado": "coprincipal", "repite_visto": sp["repite_visto"], "muestra": sp["muestra"], "N": sp["res"]["n"], "h": sp["h"],
                          "beta_2sls": num(sp["res"]["beta"]), "se_nw": num(sp["res"]["se_nw"]), "se_ehw": num(sp["res"]["se_ehw"]), "F_efectivo": num(sp["res"]["F"]),
                          "pi_primera_etapa": num(sp["res"]["pi"]), "ar_tipo": sp["res"]["ar"][0], "ar_lo": num(sp["res"]["ar"][1]), "ar_hi": num(sp["res"]["ar"][2]),
                          "p_ar0": num(sp["res"]["p_ar0"], 4), "p_holm": num(hp.get(k), 4), "mde": mdev(sp["mde"]), "clasificacion_v18": "no se clasifica",
                          "nota": f"{sp['desc']}; entra en la familia de Holm (adenda 1.7); {NOTA_NO_APTO}" + (
                              f" Unidad de Q5: % por desviación típica de la sorpresa (aquí por unidad de sorpresa trimestral; sd = {M['z_med'].std():.3f})." if k == "E7-P-Q5" else "")})
            continue
        if es_var:
            base_id = "E7-R1"
            clase = clases.get(base_id) or "NO ESTIMABLE"
            motivos = ["variante: entra en I5 y en BY; sin clase propia, hereda la de la principal"]
            publicar_lp(sp, clase, motivos, None)
            continue
        placebos = plac if k == "E7-R1" else None
        clase, motivos = clasificar_lp(sp, placebos, hp.get(k), signo if k == "E7-R1" else None)
        clases[k] = clase
        publicar_lp(sp, clase, motivos, hp.get(k),
                    extra_nota=("Placebos: " + json.dumps(plac, ensure_ascii=False) if k == "E7-R1" else ""))
    # SVAR
    for k in ("E7-R2", "E7-R2-v1", "E7-R2-v3", "E7-R2-v4"):
        sp = S[k]
        r = sp["res"]
        cj = r["ar"]
        es_var = sp["estado"] == "variante"
        if not es_var:
            clase, motivos = clasificar_lp({"estimable": sp["estimable"], "mde": sp["mde"], "umbral": sp["umbral"], "res": {"F": r["F"], "ar": cj}}, None, hp.get(k), None)
            clases[k] = clase
        else:
            clase, motivos = clases["E7-R2"], ["variante: entra en I5 y en BY; hereda la clase de la principal"]
        lo, hi = (cj[1], cj[2]) if cj[0] == "acotado" else (None, None)
        nota = (f"SVAR con instrumento externo (proxy), p = {sp['p']}, muestra {sp['muestra']}; respuesta del precio real a h = {sp['h']} normalizada a +100 pb de impacto en el tipo hipotecario; "
                f"F robusto del proxy {r['F']:.2f}; AR 95 % {ar_texto(cj)}; p AR en 0 = {r['p_ar0']:.3f}; raíz máxima del VAR {sp['raiz_maxima_VAR']:.3f} (estable si < 1). "
                f"MDE {mdet(sp['mde'])} frente al umbral {sp['umbral']}. SVAR con proxy: NO APTO en el Monte Carlo de V18 (tamaño 0,057-0,072 con F ≈ 27 y cobertura bajo la alternativa "
                f"0,87-0,90; conservador con F ≈ 4): se publica con esa etiqueta. I6 (etiqueta): {etiqueta_i6(r['beta'], sp['ref'])}. {'; '.join(motivos)}")
        hecho(f"V18-{k}", f"Respuesta del precio real a +100 pb del tipo hipotecario a {sp['h']} trimestres (SVAR con proxy, {k})", r["beta"], lo, hi,
              "% del precio por +100 pb del tipo (impacto normalizado; SVAR con proxy)", sp["muestra"], "nacional", clase, nota)
        FILAS.append({"id": k, "familia": "E7", "estado": sp["estado"], "repite_visto": sp["repite_visto"], "muestra": sp["muestra"], "N": r["n"], "h": sp["h"], "beta_2sls": num(r["beta"]),
                      "F_efectivo": num(r["F"]), "ar_tipo": cj[0], "ar_lo": num(cj[1]), "ar_hi": num(cj[2]), "p_ar0": num(r["p_ar0"], 4), "p_holm": num(hp.get(k), 4),
                      "mde": mdev(sp["mde"]), "umbral_mde": sp["umbral"], "estimable": sp["estimable"], "I6": etiqueta_i6(r["beta"], sp["ref"]), "clasificacion_v18": clase, "nota": nota})
    # panel provincial
    for k, a in A2.items():
        es_var = a["estado"] == "variante"
        est = a["mde"]["mde"] <= 2.0
        if k == "E7-A2-h8":
            if not est:
                clase = "NO ESTIMABLE"
            else:
                i7 = hp.get("E7-A2", 1.0) < 0.05
                clase = "SUGESTIVO" if i7 else "NO CONCLUYENTE"
            clases["E7-A2"] = clase
        else:
            clase = clases.get("E7-A2", "NO ESTIMABLE")
        nota = (f"Panel provincial: Δ_h ln p_pt sobre (sorpresa_t × exposición hipotecaria E_p, 2007-2019) con efectos fijos de provincia y de periodo; G = {a['G']} provincias no selladas con serie "
                f"completa, T = {a['T']} trimestres ({a['muestra']}); h = {a['h']}. Error típico agrupado por provincia {a['se_cr1']:.3f}; p de Webb (WCR) = {a['p_webb']:.3f}; "
                f"IC95 t({a['G'] - 1}); Webb y CR1 t con efectos de año: APTOS con G = 30-39 (V18 montecarlo/webb_twfe). Tope SUGESTIVO: la exposición es endógena al mercado local. "
                f"Respuesta relativa entre provincias, sin el componente común (los efectos de periodo lo absorben). MDE {mdet(a['mde'])} frente a 2δ = 2,0 (la sorpresa tiene una desviación típica de {M['z_med'].std():.3f} pp: +100 pb queda muy fuera del soporte observado). CD de Pesaran {a['cd']['CD']} (p = {a['cd']['p']}). "
                f"Falta el peso provincial de la hipoteca variable (E7-A2-X1) y las compras al contado: la exposición es una aproximación. {'Variante: clase heredada.' if es_var else ''}")
        FILAS.append({"id": a["id"], "familia": "E7", "estado": a["estado"], "repite_visto": a["repite_visto"], "muestra": a["muestra"], "N": a["G"] * a["T"], "h": a["h"],
                      "beta_2sls": num(a["beta"]), "ic95_lo": num(a["ic95_t"][0]), "ic95_hi": num(a["ic95_t"][1]), "p_ar0": num(a["p_webb"], 4), "p_holm": num(hp.get("E7-A2") if k == "E7-A2-h8" else None, 4),
                      "mde": mdev(a["mde"]), "umbral_mde": 2.0, "estimable": est, "clasificacion_v18": clase, "nota": nota})
        hecho(f"V18-{a['id']}", f"Respuesta relativa entre provincias del precio a la sorpresa × exposición hipotecaria a {a['h']} trimestres", a["beta"], a["ic95_t"][0], a["ic95_t"][1],
              "% del precio por pp de sorpresa y por unidad de exposición (relativo entre provincias, sin el componente común)", a["muestra"], f"{a['G']} provincias", clase, nota)
    no_estimable("E7-A2-v1", "variante", "E7-A2 con la cuota de compradores extranjeros × choque",
                 "variante no estimada: la cuota provincial de compradores extranjeros (data/raw/mivau_transacciones_residencia.csv) no figura entre las variables del manifiesto de E7-A2 y su carga pertenece a E9; "
                 "queda como tarea de integración (no es una desviación elegida por su resultado)", "sí (V9-D5)")
    no_estimable("E7-R1-v2", "variante", "E7-R1 con el diferencial soberano a 10 años como control",
                 "falta el dato: no hay serie trimestral del diferencial soberano a 10 años (solo la anual irt_lt_mcby_a, sin clave en sellado_v18.json); descarga mensual del BCE (`posterior_prereg`) pendiente")
    no_estimable("E7-R2-v2", "variante", "E7-R2 con el diferencial soberano a 10 años", "falta el dato (ver E7-R1-v2)")
    no_estimable("E7-P-H8-7", "coprincipal", "V8 H8-7 (empuje migratorio, IV2)", "no es una especificación de tipos de interés (IV2 es el empuje migratorio anual por cuotas de nacionalidad: pertenece a E3); "
                 "se deja a la fase de E3", "sí (V8 H8-7)")
    no_estimable("E7-P-D5", "coprincipal", "V9-D5 (panel de 18 países, tipo variable × choques)", "no reproducible: el panel de países de V9-D5 usa el BIS y la exposición de cada país a la hipoteca variable, "
                 "que no están en sellado_v18.json; el contraste provincial es E7-A2", "sí (V9-D5)")
    no_estimable("E7-A3", "principal", "E7-R1 y R2 con EA-MPD como choque alternativo", "no se estima hasta que el autor decida la licencia de EA-MPD (tareas_autor, punto 14)")
    no_estimable("E7-A2-X1", "principal", "E7-A2 con el peso provincial de la hipoteca variable", "falta el dato: Registradores con autorización (tareas_autor, punto 8) o la EFF (punto 6)")
    res["hp"] = hp
    res["clases"] = clases
    res["signo"] = signo
    res["criterios"] = {"E7-R1": criterios_i(S["E7-R1"], plac, signo, hp.get("E7-R1")), "E7-R1-ipv": criterios_i(S["E7-R1-ipv"], None, None, hp.get("E7-R1-ipv")),
                        "E7-R1-cv": criterios_i(S["E7-R1-cv"], None, None, hp.get("E7-R1-cv")), "E7-R1-alq": criterios_i(S["E7-R1-alq"], None, None, hp.get("E7-R1-alq")),
                        "E7-R2": criterios_i({**S["E7-R2"], "res": {**S["E7-R2"]["res"], "pi": None}}, None, None, hp.get("E7-R2"))}
    return res


# ---------------------------------------------------------------------------------------------- salidas
def escribir(res: dict, salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    S, A2, diag, hp, clases = res["S"], res["A2"], res["diag"], res["hp"], res["clases"]
    t = pd.DataFrame(FILAS)
    t.to_csv(salida / "tabla.csv", index=False)
    (salida / "hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1), encoding="utf-8")
    pd.DataFrame(S["E7-R1"]["irf"]).to_csv(salida / "irf_R1_precio.csv", index=False)
    pd.DataFrame(S["E7-R2"]["irf"]).to_csv(salida / "irf_R2_precio.csv", index=False)
    r1 = S["E7-R1"]
    estim = {}
    for r in t.itertuples():
        if r.estado in ("principal", "variante", "coprincipal"):
            estim[r.id] = {"beta": getattr(r, "beta_2sls", None), "ar95": [getattr(r, "ar_lo", None), getattr(r, "ar_hi", None)], "F": getattr(r, "F_efectivo", None),
                           "p_ar0": getattr(r, "p_ar0", None), "p_holm": getattr(r, "p_holm", None), "mde": getattr(r, "mde", None), "clasificacion_v18": r.clasificacion_v18}
    resultado = {
        "rama": "v18/estimacion/e7",
        "pregunta": "¿Cuánto cambia el precio real de la vivienda (y las compraventas y el alquiler) ante un aumento de 100 pb del tipo hipotecario, identificado con las sorpresas de política "
                    "monetaria del BCE (Jarociński-Karadi)? Proyección local con instrumento, SVAR con proxy y panel provincial con exposición (E7 del plan de replicación V18)",
        "capa": "C4",
        "datos": "base (hechos.parquet) vía src/v18/sellado.filtrar; sorpresas de data/bib/replicacion/jarocinski_karadi2020 (mensuales, 1999-2025-10; trimestrales hasta 2025T3); "
                 "hipotecas y compraventas provinciales de data/raw (INE) para la exposición",
        "N": {"LP-IV_h8": r1["res"]["n"], "SVAR": S["E7-R2"]["res"]["n"], "panel": {k: [a["G"], a["T"]] for k, a in A2.items()}},
        "metodo": "LP-IV con 4 rezagos de y y de Δi y de los controles (PIB, inflación): 2SLS con Newey-West h+1 y con EHW aumentado, F efectivo, conjunto de Anderson-Rubin; "
                  "SVAR con proxy (p = 2) con AR por método delta; panel provincial con WCR de Webb (B = 9.999); MDE por Monte Carlo; Holm sobre la familia E7",
        "estimacion": estim,
        "ic95": {k: v["ar95"] for k, v in estim.items()},
        "p_ajustado": {"metodo": "Holm sobre las estimables de E7 (p de AR con EHW, AR delta o Webb); m = tamaño de la familia tras las comprobaciones de MDE", "m": len(hp), "valores": hp},
        "nivel_evidencia": "EXPLORATORIO",
        "clasificacion_v18": clases.get("E7-R1", "NO ESTIMABLE"),
        "clasificacion_v18_por_especificacion": {r.id: r.clasificacion_v18 for r in t.itertuples()},
        "diagnosticos": {**diag, "mde_R1": r1["mde"], "mde_R2": S["E7-R2"]["mde"], "irf_R1": r1["irf"], "irf_R2": S["E7-R2"]["irf"], "herramientas": NOTA_NO_APTO,
                         "tamano_familia_holm": len(hp), "raiz_maxima_VAR_R2": S["E7-R2"]["raiz_maxima_VAR"], "criterios_I1_I8": res["criterios"]},
        "fuera_muestra": None,
        "notas": [ROTULO, "Clase provisional hasta I8 (réplica ciega, B6).",
                  "fuera_muestra: no aplica a E7 (modelos de identificación; la predicción frente a AR(4) y ECM v1 se hace en F1).",
                  "Referencia única: San Juan (2023), −2 % por +100 pb a 8 trimestres (intervalos al 68 %: sin vía de solapamiento); la del BCE (−5 %) va al lado sin función en I6.",
                  "Fuente de las sorpresas: Jarociński y Karadi (2020), DOI 10.1257/mac.20180090, actualización con EA-MPD (Altavilla et al., 2019, DOI 10.1016/j.jmoneco.2019.08.016); sin licencia declarada: solo local.",
                  "Desviaciones y motivos: docs/v18/desviaciones_f_e7.md. E7-R3 y E7-A1 (BVAR de San Juan) no se encargaron a este módulo."],
    }
    (salida / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    informe(res, t, salida)


def informe(res: dict, t: pd.DataFrame, salida: Path) -> None:
    S, A2, diag, hp, clases = res["S"], res["A2"], res["diag"], res["hp"], res["clases"]
    r1, r2 = S["E7-R1"], S["E7-R2"]
    L_ = [f"# E7 · Tipos de interés: proyección local con instrumento, SVAR con proxy y panel provincial\n\n*{ROTULO}.*\n"]
    L_.append("## Lectura\n")
    L_.append(f"- **Primera etapa.** Sorpresa monetaria (mediana de Jarociński-Karadi, suma trimestral) sobre la variación trimestral del tipo hipotecario: π = {r1['res']['pi']:.3f} "
              f"({'signo contrario al esperado' if r1['res']['pi'] < 0 else 'signo esperado'}), F efectivo {r1['res']['F']:.2f} (EHW tras aumentar con rezagos). "
              f"Q5 (V16) dio F de 2,1 a 2,9 y V8, primera etapa de signo contrario: {'se repite la debilidad' if r1['res']['F'] < 10 else 'el instrumento es más fuerte que en V8/V16'}.\n")
    L_.append(f"- **Comprobación previa por MDE (adenda 1.3).** E7-R1: MDE {mdet(r1['mde'])} frente al umbral 2,0 (San Juan: −2 % por +100 pb) → "
              f"{'estimable' if r1['estimable'] else 'NO ESTIMABLE por variación'}. E7-R2: MDE {mdet(r2['mde'])} → {'estimable' if r2['estimable'] else 'NO ESTIMABLE por variación'}. "
              f"E7-A2: MDE {mdet(A2['E7-A2-h8']['mde'])} frente a 2δ = 2,0. Se calculó y registró antes de estimar; las especificaciones no estimables salen de la familia de Holm y se "
              "publican como estimación informativa, fuera de clasificación.\n")
    L_.append(f"- **Estimación a 8 trimestres (E7-R1).** 2SLS {r1['res']['beta']:.2f} % por +100 pb; conjunto AR 95 % (EHW) {ar_texto(r1['res']['ar'])}; p de AR en 0 = {r1['res']['p_ar0']:.3f}. "
              f"Clase provisional: **{clases.get('E7-R1')}**. Referencia: San Juan (2023), −2 %; {etiqueta_i6(r1['res']['beta'], -2.0)} (etiqueta, no decide). El −5 % del BCE va al lado sin función en I6.\n")
    L_.append(f"- **SVAR con proxy (E7-R2).** Respuesta del precio a h = 8: {r2['res']['beta']:.2f}; F robusto {r2['res']['F']:.2f}; AR 95 % {ar_texto(r2['res']['ar'])}; clase provisional **{clases.get('E7-R2')}**.\n")
    a8 = A2["E7-A2-h8"]
    L_.append(f"- **Panel provincial (E7-A2).** β = {a8['beta']:.2f} (IC95 t[{a8['G'] - 1}] {a8['ic95_t'][0]:.2f} a {a8['ic95_t'][1]:.2f}; p de Webb {a8['p_webb']:.3f}); G = {a8['G']}; clase **{clases.get('E7-A2')}**; "
              "respuesta relativa entre provincias, sin el componente común.\n")
    L_.append("## Herramientas (etiqueta de distorsión)\n")
    L_.append(NOTA_NO_APTO + "\n")
    L_.append("SVAR con proxy: NO APTO (AR por método delta: tamaño 0,057-0,072 con F ≈ 27, cobertura 0,87-0,90 bajo la alternativa; conservador con F ≈ 4). Panel: Webb y CR1 t con efectos de año, APTOS con 30-39 clusters.\n")
    L_.append("## Tabla de especificaciones\n")
    cols = ["id", "estado", "muestra", "N", "h", "beta_2sls", "se_nw", "F_efectivo", "ar_tipo", "ar_lo", "ar_hi", "p_ar0", "p_holm", "mde", "estimable", "clasificacion_v18"]
    L_.append(F.md_tabla(t, cols))
    L_.append("\n## Diagnósticos del pre-registro\n")
    L_.append("```json\n" + json.dumps(diag, ensure_ascii=False, indent=1, default=str) + "\n```\n")
    L_.append("## IRF a 12 trimestres (E7-R1, precio, % por +100 pb)\n")
    L_.append(F.md_tabla(pd.DataFrame(r1["irf"]), ["h", "beta", "se_nw", "ar", "ar_lo", "ar_hi", "F", "n"]))
    L_.append("\n## Notas\n- Clase provisional hasta I8 (réplica ciega, B6).\n- Sorpresas: Jarociński y Karadi (2020), actualización con EA-MPD (Altavilla et al., 2019); sin licencia declarada: solo local.\n"
              "- «Controlando el diferencial soberano» (v2): NO ESTIMABLE por falta de la serie trimestral; ver docs/v18/desviaciones_f_e7.md.\n"
              "- Controles de la principal: PIB y inflación; el crédito nuevo empieza en 2003T1 y recortaría la muestra (desviación declarada).\n")
    (salida / "informe.md").write_text("\n".join(L_), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()
    out = Path(args.salida) if args.salida else OUT
    r = finalizar(main(rapido=args.rapido, salida=out))
    escribir(r, out)
    REG.flush()
    print(f"e7_tipos: {len(FILAS)} filas, {len(HECHOS)} cifras -> {out}")
