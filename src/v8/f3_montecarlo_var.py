"""V8-F3 (grupo A, familia VAR): validacion por Monte Carlo de BVAR-GLP, signos/ceros (RWZ/ARW) y TVP-VAR-SV. SOLO datos simulados.
Salidas: output/v8/F3/var/montecarlo.csv, validacion.md, resultado.json. Uso: python3 src/v8/f3_montecarlo_var.py [--rapido]
Replicas: las que caben en ~20 min de computo total (se declaran en el csv y en validacion.md). SEED = 20261010, un hilo, determinista."""
from __future__ import annotations

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import integrate, stats  # noqa: E402
from scipy.special import gammaln  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "v8"))
from herramientas import bvar, signos, tvp  # noqa: E402

SEED = 20261010
OUT = Path(os.environ.get("F3_OUT", ROOT / "output" / "v8" / "F3" / "var"))
RAPIDO = "--rapido" in sys.argv
ROWS = []
TIEMPOS = {}
T0 = time.time()


def add(herr, esc, T, R, metrica, valor, criterio="", cumple=None):
    ROWS.append(dict(herramienta=herr, escenario=esc, T=T, replicas=R, metrica=metrica, valor=float(valor), criterio=criterio,
                     cumple=("" if cumple is None else bool(cumple))))


def rng_for(*tag):
    return np.random.default_rng([SEED, *tag])


def sim_var(A_list, imp, T, rng, burn=100):
    n = imp.shape[0]
    p = len(A_list)
    Y = np.zeros((T + burn, n))
    for t in range(p, T + burn):
        Y[t] = sum(A_list[l] @ Y[t - 1 - l] for l in range(p)) + imp @ rng.standard_normal(n)
    return Y[burn:]


def B_from(A_list):
    n = A_list[0].shape[0]
    p = len(A_list)
    B = np.zeros((1, n * p + 1, n))
    for l, A in enumerate(A_list):
        B[0, l * n:(l + 1) * n, :] = A.T
    return B


def radio(A_list):
    n, p = A_list[0].shape[0], len(A_list)
    top = np.hstack(A_list)
    comp = np.vstack([top, np.hstack([np.eye(n * (p - 1)), np.zeros((n * (p - 1), n))])])
    return np.max(np.abs(np.linalg.eigvals(comp)))


# ======================================================================== 1. BVAR
def dgp_bvar(nombre):
    n = 4
    if nombre == "denso":
        A1 = np.array([[0.55, 0.10, 0.00, 0.05], [0.10, 0.45, 0.10, 0.00], [0.00, 0.10, 0.60, 0.10], [0.10, 0.00, 0.10, 0.35]])
        A2 = np.array([[-0.10, 0, 0.05, 0], [0, -0.05, 0, 0.05], [0.05, 0, -0.10, 0], [0, 0.05, 0, -0.05]])
    elif nombre == "tasas":  # tres tasas de variacion poco persistentes + una variable en nivel muy persistente (como el tipo)
        A1 = np.array([[0.30, 0.05, 0.00, 0.02], [0.05, 0.25, 0.05, 0.00], [0.00, 0.05, 0.35, 0.03], [0.00, 0.00, 0.05, 0.95]])
        A2 = np.array([[-0.05, 0, 0, 0], [0, -0.05, 0, 0], [0, 0, -0.05, 0], [0, 0, 0, 0.0]])
    else:  # casi paseo aleatorio por variable: coherente con el prior Minnesota
        A1 = 0.9 * np.eye(n)
        A2 = np.zeros((n, n))
    L = np.array([[1.0, 0, 0, 0], [0.4, 0.9, 0, 0], [0.2, 0.3, 0.8, 0], [0.1, 0.2, 0.3, 0.7]])
    return [A1, A2], L


BVAR_MODOS = {"GLP": {}, "GLP_delta1": dict(delta=1.0), "plano_lam100": dict(lam=100.0)}
BVAR_ESC = ("denso", "casi_RW", "tasas")


def mc_bvar(R):
    H = 12
    for esc in BVAR_ESC:
        A, L = dgp_bvar(esc)
        assert radio(A) < 0.97
        Phi_t = bvar.ma_coefs(B_from(A), 4, 2, H)[0]
        Itrue = Phi_t @ L  # (H+1, i, j)
        struct0 = np.zeros((H + 1, 4, 4), bool)
        struct0[0] = np.triu(np.ones((4, 4)), 1).astype(bool)
        modos = dict(BVAR_MODOS)
        if esc == "tasas":
            modos["GLP_delta_mixto"] = dict(delta=np.array([0.0, 0.0, 0.0, 1.0]))  # 0 en tasas, 1 en el nivel (desviaciones.md)
        for T in (120, 60):
            for modo, kw in modos.items():
                cov68, cov90, med, lams, lb = [], [], [], [], []
                t0 = time.time()
                for r in range(R):
                    rg = rng_for(1, T, r)
                    Y = sim_var(A, L, T, rg)
                    post = bvar.estimar(Y, 2, **kw)
                    I, b = bvar.irf(post, H, 300, rg)
                    ok = ~struct0
                    cov68.append(((b["lo68"] <= Itrue) & (Itrue <= b["hi68"]))[ok])
                    cov90.append(((b["lo90"] <= Itrue) & (Itrue <= b["hi90"]))[ok])
                    med.append(b["med"])
                    lams.append(post["lam"])
                    lb.append(post["logml"])
                cov68, cov90 = np.array(cov68), np.array(cov90)
                bias = np.mean(med, 0) - Itrue
                m = np.ones((H + 1, 4, 4), bool)
                m[0] = False
                sesgo_rel = np.abs(bias[m]).sum() / np.abs(Itrue[m]).sum()
                sesgo_h = {h: np.abs(bias[h]).sum() / np.abs(Itrue[h]).sum() for h in (1, 4, 8, 12)}
                # H12: sesgo FIRMADO relativo (atenuacion): positivo = la IRF media esta mas cerca de 0 que la verdad
                sg = np.sign(Itrue)
                aten = -(sg * bias)[m].sum() / np.abs(Itrue[m]).sum()
                aten_h = {h: -(sg[h] * bias[h]).sum() / np.abs(Itrue[h]).sum() for h in (1, 4, 8, 12)}
                mm = m & (np.abs(Itrue) >= 0.05)
                frac_at = float(((sg * bias) < 0)[mm].mean())
                c68, c90 = float(cov68.mean()), float(cov90.mean())
                tag = f"{esc}|{modo}"
                add("BVAR", tag, T, R, "cobertura_68", c68)
                add("BVAR", tag, T, R, "cobertura_90", c90, "[0.85, 0.98]", 0.85 <= c90 <= 0.98)
                add("BVAR", tag, T, R, "sesgo_rel_IRF_h1-12", sesgo_rel, "<= 0.10", sesgo_rel <= 0.10)
                add("BVAR", tag, T, R, "atenuacion_firmada_rel_h1-12", aten)
                add("BVAR", tag, T, R, "frac_celdas_atenuadas_(|IRF|>=0.05)", frac_at)
                for h, v in sesgo_h.items():
                    add("BVAR", tag, T, R, f"sesgo_rel_h{h}", v)
                for h, v in aten_h.items():
                    add("BVAR", tag, T, R, f"atenuacion_firmada_rel_h{h}", v)
                if modo.startswith("GLP"):
                    for q, v in zip(("media", "p05", "mediana", "p95"), (np.mean(lams), *np.quantile(lams, [0.05, 0.5, 0.95]))):
                        add("BVAR", tag, T, R, f"lambda_{q}", v)
                print(f"[BVAR {tag} T={T}] cov68={c68:.3f} cov90={c90:.3f} sesgo={sesgo_rel:.3f} aten={aten:.3f} frac_at={frac_at:.2f} lam~{np.median(lams):.2f} ({time.time() - t0:.0f}s)", flush=True)


def ml_fuerza_bruta():
    """(i) n=1,p=1 sin constante: cuadratura 2-D de p(Y|b,s2) p(b|s2) p(s2). (ii) cadena predictiva t-multivariante (n=3,p=2, con dummies)."""
    out = {}
    rng = rng_for(2, 0)
    y = np.zeros(11)
    for t in range(1, 11):
        y[t] = 0.7 * y[t - 1] + rng.standard_normal()
    Y = y[:, None]
    lam = 0.5
    psi = np.array([1.3])
    pr = bvar.prior_minnesota(1, 1, lam, psi, const=False)
    yy, X = bvar.retardos(Y, 1, const=False)
    om = 1.0 / pr["Oinv"][0, 0]
    nu0, s0 = pr["nu0"], pr["S0"][0, 0]

    def integrando(b, s2):
        lik = np.prod(stats.norm.pdf(yy[:, 0], X[:, 0] * b, np.sqrt(s2)))
        pb = stats.norm.pdf(b, 0.0 + pr["B0"][0, 0], np.sqrt(s2 * om))
        ps = np.exp((nu0 / 2) * np.log(s0 / 2) - gammaln(nu0 / 2) - (nu0 / 2 + 1) * np.log(s2) - s0 / (2 * s2))
        return lik * pb * ps
    val, err = integrate.dblquad(lambda b, s2: integrando(b, s2), 1e-4, 40, lambda s2: -6, lambda s2: 6, epsabs=1e-12, epsrel=1e-8)
    exacto = bvar.logml(Y, 1, lam, const=False, psi=psi)
    out["cuadratura_n1"] = abs(np.log(val) - exacto)
    # (ii) cadena predictiva con prior (Minnesota + dummies SOC e IO)
    n, p, T = 3, 2, 40
    A = [0.5 * np.eye(3), -0.1 * np.eye(3)]
    Y3 = sim_var(A, np.eye(3), T, rng_for(2, 1))
    psi3 = bvar._psi_ar(Y3, p)
    pr3 = bvar._prior_completo(Y3, p, 0.3, 0.8, 1.5, 1.0, 2.0, True, psi3)
    yy3, X3 = bvar.retardos(Y3, p)
    cur, tot = pr3, 0.0
    for t in range(len(yy3)):
        x = X3[t:t + 1]
        post = bvar._actualizar(cur, yy3[t:t + 1], x)
        Om = np.linalg.inv(cur["Oinv"])
        dfp = cur["nu0"] - n + 1
        mean = (x @ cur["B0"])[0]
        scale = cur["S0"] / dfp * (1 + (x @ Om @ x.T)[0, 0])
        tot += stats.multivariate_t.logpdf(yy3[t], mean, scale, df=dfp)
        cur = dict(B0=post["B0"], Oinv=post["Oinv"], S0=post["S0"], nu0=post["nu0"])
    ex3 = bvar.logml_prior(pr3, yy3, X3)
    out["cadena_predictiva_n3_dummies"] = abs(tot - ex3)
    for k, v in out.items():
        add("BVAR", f"logml_vs_{k}", "", 1, "error_abs_logml", v, "<= 1e-6", v <= 1e-6)
    print("ML fuerza bruta:", out, flush=True)


# ======================================================================== 2. Signos
VARS = ["y", "pi", "cred", "tipo"]
SHOCKS = ["oferta", "demanda", "credito", "monetario"]


def impacto(zeros=False):
    A0 = np.array([[1.0, 0.8, 0.5, -0.6],
                   [-0.5, 0.6, 0.3, -0.4],
                   [0.2, 0.4, 1.0, -0.5],
                   [0.1, 0.5, 0.2, 0.8]])
    if zeros:
        A0[0, 3] = 0.0   # monetario: efecto nulo sobre y en el impacto
        A0[3, 0] = 0.0   # oferta: efecto nulo sobre el tipo en el impacto
    return A0


def restr_signos(zeros=False):
    r = signos.Restricciones(VARS, SHOCKS)
    r.signo("y", "oferta", 1).signo("pi", "oferta", -1)
    r.signo("y", "demanda", 1).signo("pi", "demanda", 1).signo("tipo", "demanda", 1)
    r.signo("cred", "credito", 1).signo("y", "credito", 1).signo("pi", "credito", 1)
    r.signo("tipo", "monetario", 1).signo("pi", "monetario", -1).signo("cred", "monetario", -1)
    if zeros:
        r.cero("y", "monetario", 0).cero("tipo", "oferta", 0)
    else:
        r.signo("y", "monetario", -1)
    return r


def mc_signos(R_by):
    H = 12
    A1 = 0.6 * np.eye(4) + np.array([[0, .05, 0, 0], [0, 0, .05, 0], [0, 0, 0, .05], [.05, 0, 0, 0]])
    A = [A1, -0.1 * np.eye(4)]
    hs = (0, 1, 4, 8)
    for esc, zeros, T in (("signos", False, 120), ("signos", False, 60), ("signos+ceros", True, 120)):
        R = R_by[(esc, T)]
        A0 = impacto(zeros)
        Itrue = bvar.ma_coefs(B_from(A), 4, 2, H)[0] @ A0
        r = restr_signos(zeros)
        restringida = np.zeros((H + 1, 4, 4), bool)
        for (i, j, sg, h) in r.signos:
            restringida[h, i, j] = True
        zero_c = np.zeros((H + 1, 4, 4), bool)
        for (i, j, h) in r.ceros:
            zero_c[h, i, j] = True
        c68 = {"restr": [], "libre": []}
        c90 = {"restr": [], "libre": []}
        signo_ok, banda_signo, med_bias, ess, acept, zmax, hd_err, nacc, fth = [], [], [], [], [], [], [], [], []
        t0 = time.time()
        for rep in range(R):
            rg = rng_for(3, int(zeros), T, rep)
            Y = sim_var(A, A0, T, rg)
            post = bvar.estimar(Y, 2)
            B, Sig = bvar.muestrear(post, 400, rg)
            res = signos.identificar(B, Sig, 4, 2, r, H=H, n_objetivo=150, rotaciones=800, rng=rg)
            if len(res["Q"]) < 20:
                continue
            nacc.append(len(res["Q"]))
            fth.append(res["frac_theta_acept"])
            ess.append(res["ess"])
            acept.append(res["acept"])
            mz, fs = signos.comprobar(res, r)
            zmax.append(mz)
            bb = bvar.bandas(res["irf"], 0, res["peso"])
            for nm, (lo, hi) in (("68", (bb["lo68"], bb["hi68"])), ("90", (bb["lo90"], bb["hi90"]))):
                cv = (lo <= Itrue) & (Itrue <= hi)
                dst = c68 if nm == "68" else c90
                sel_h = np.zeros_like(restringida)
                sel_h[list(hs)] = True
                dst["restr"].append(cv[restringida & sel_h].mean())
                dst["libre"].append(cv[(~restringida) & (~zero_c) & sel_h].mean())
            # signo del impacto en elementos no restringidos con |verdad| >= 0.2
            lib0 = (~restringida[0]) & (~zero_c[0]) & (np.abs(Itrue[0]) >= 0.2)
            signo_ok.append((np.sign(bb["med"][0]) == np.sign(Itrue[0]))[lib0].mean())
            banda_signo.append(((np.sign(bb["lo90"][0]) == np.sign(Itrue[0])) & (np.sign(bb["hi90"][0]) == np.sign(Itrue[0])))[lib0].mean())
            nl = (~restringida) & (~zero_c)
            nl[:, :, :] &= (np.abs(Itrue) >= 0.2)
            med_bias.append(((bb["med"] - Itrue)[nl]).mean())
            if rep < 6:
                hd = signos.descomposicion_historica({k: (v[:20] if isinstance(v, np.ndarray) and v.shape[:1] == res["Q"].shape[:1] else v)
                                                      for k, v in res.items()}, Y)
                hd_err.append(hd["error"])
            fv = signos.fevd(res["irf"])
            assert np.allclose(fv.sum(-1), 1.0)
        tag = f"{esc}|T{T}"
        Rv = len(nacc)
        add("signos", tag, T, Rv, "aceptacion_por_rotacion", np.mean(acept))
        add("signos", tag, T, Rv, "frac_theta_con_aceptada_(800_rotaciones)", np.mean(fth))
        add("signos", tag, T, Rv, "aceptadas_medias_(tope_150_al_cerrar_theta)", np.mean(nacc))
        add("signos", tag, T, Rv, "ESS_medio_de_150", np.mean(ess))
        add("signos", tag, T, Rv, "restricciones_cumplidas_max_abs_cero", max(zmax) if zeros else 0.0, "< 1e-10", (max(zmax) < 1e-10) if zeros else True)
        add("signos", tag, T, Rv, "cobertura_68_IRF_restringidas", np.mean(c68["restr"]))
        add("signos", tag, T, Rv, "cobertura_68_IRF_no_restringidas", np.mean(c68["libre"]))
        add("signos", tag, T, Rv, "cobertura_90_IRF_restringidas", np.mean(c90["restr"]), "[0.85, 0.98]", 0.85 <= np.mean(c90["restr"]) <= 0.98)
        add("signos", tag, T, Rv, "cobertura_90_IRF_no_restringidas", np.mean(c90["libre"]), "[0.85, 0.98]", 0.85 <= np.mean(c90["libre"]) <= 0.98)
        add("signos", tag, T, Rv, "signo_impacto_recuperado_no_restringidas", np.mean(signo_ok), ">= 0.90", np.mean(signo_ok) >= 0.90)
        add("signos", tag, T, Rv, "banda90_excluye_cero_con_signo_correcto", np.mean(banda_signo))
        add("signos", tag, T, Rv, "sesgo_medio_mediana_no_restringidas", np.mean(med_bias))
        add("signos", tag, T, Rv, "descomposicion_historica_error_max", max(hd_err), "< 1e-8", max(hd_err) < 1e-8)
        print(f"[SIGNOS {tag}] R={Rv} acept={np.mean(acept):.4f} ESS={np.mean(ess):.0f} cov90 restr={np.mean(c90['restr']):.3f} libre={np.mean(c90['libre']):.3f} "
              f"cov68 libre={np.mean(c68['libre']):.3f} signo={np.mean(signo_ok):.3f} hd={max(hd_err):.1e} ({time.time() - t0:.0f}s)", flush=True)


def invariancia_orden(N):
    """Los pesos de importancia deben hacer la distribucion de Q invariante al orden de los shocks (diagnostico de los pesos)."""
    rg = rng_for(4, 0)
    n = 4
    B = np.zeros((1, 9, 4))
    B[0, :4, :4] = 0.5 * np.eye(4) + 0.1 * rg.standard_normal((4, 4))
    M = rg.standard_normal((4, 4))
    Sig = (M @ M.T + np.eye(4))[None]
    r = signos.Restricciones(VARS, SHOCKS)
    r.cero(0, 0, 0).cero(1, 1, 0).cero(2, 1, 0)
    stats_ = {}
    for nombre, orden, sd in (("A", [1, 0, 2, 3], 1), ("A_otra_semilla", [1, 0, 2, 3], 2), ("B", [1, 2, 0, 3], 3)):
        res = signos.identificar(B, Sig, n, 2, r, H=2, rotaciones=N, rng=rng_for(4, sd), orden=orden)
        w = res["peso"]
        stats_[nombre] = (np.einsum("n,nij->ij", w, res["Q"] ** 2), (res["Q"] ** 2).mean(0), res["ess"])
    ruido = np.abs(stats_["A"][0] - stats_["A_otra_semilla"][0]).max()
    cruz_p = max(np.abs(stats_["B"][0] - stats_[k][0]).max() for k in ("A", "A_otra_semilla"))
    cruz_s = max(np.abs(stats_["B"][1] - stats_[k][1]).max() for k in ("A", "A_otra_semilla"))
    ok = cruz_p <= max(0.04, 1.5 * ruido) and cruz_p < cruz_s / 4
    add("signos", "ARW_invariancia_al_orden", "", N, "ESS_medio", np.mean([v[2] for v in stats_.values()]))
    add("signos", "ARW_invariancia_al_orden", "", N, "suelo_de_ruido_(mismo_orden_otra_semilla)", ruido)
    add("signos", "ARW_invariancia_al_orden", "", N, "max_dif_E[Q^2]_entre_ordenes_con_pesos", cruz_p, "<= max(0.04, 1.5*ruido) y < sin_pesos/4", ok)
    add("signos", "ARW_invariancia_al_orden", "", N, "max_dif_E[Q^2]_entre_ordenes_sin_pesos", cruz_s)
    print(f"[ARW invariancia] ruido={ruido:.4f} entre ordenes con pesos={cruz_p:.4f} sin pesos={cruz_s:.4f} ESS={[round(v[2]) for v in stats_.values()]}", flush=True)


# ======================================================================== 2b. Configuracion PRE-REGISTRADA (M2): 7 variables, T=88, p=2
PV = ["p", "r", "q", "c", "i", "e", "n"]
PS = ["actividad", "demografico", "demanda", "oferta", "credito", "libre1", "libre2"]
T_PRE, P_PRE = 88, 2
# tramos de la descomposicion historica sobre las observaciones efectivas (Te = 86; indices base 0, inclusivos). Los periodos de
# hipotesis.md §3 recortados a 2004T3-2026T2: P0 = 2004T3-2007T4 (14), huecos 2008T1-T2, P2 = 2008T3-2013T4 (22), P3 = 2014T1-2019T4 (24),
# hueco 2020T1, P4 = 2020T2-2022T2 (9), P5 = 2022T3-fin (14 en la muestra simulada de 88 trimestres).
TRAMOS_PRE = [(0, 13), (16, 37), (38, 61), (63, 71), (72, 85)]
TRAMOS_NOM = ["P0 (14)", "P2 (22)", "P3 (24)", "P4 (9)", "P5 (14)"]
IDX_COVID = [66, 67, 68]   # 2020T2-T4 si el indice 0 es 2004T1
IDX_EPA = [69]             # 2021T1


def restr_prereg(solo_impacto=False):
    """Tabla de hipotesis.md §5. solo_impacto = variante V3: signos solo en h=0 y sin la restriccion de q en demanda y oferta."""
    r = signos.Restricciones(PV, PS)
    hs = [0] if solo_impacto else [0, 1]
    r.signo("p", "actividad", 1, hs).signo("r", "actividad", 1, hs).signo("c", "actividad", 1, hs).signo("e", "actividad", 1, hs)
    r.signo("r", "demografico", 1, hs).signo("n", "demografico", 1, hs)
    r.signo("p", "demanda", 1, hs).signo("c", "demanda", 1, hs)
    r.signo("p", "oferta", -1, hs)
    r.signo("p", "credito", 1, hs).signo("c", "credito", 1, hs).signo("i", "credito", -1, hs)
    if not solo_impacto:
        r.signo("q", "demanda", 1, hs).signo("q", "oferta", 1, hs)
    for sh in ("actividad", "demanda", "oferta", "credito"):   # 4 ceros (desviaciones.md, H16)
        r.cero("n", sh, 0)
    return r


def dgp_prereg():
    """DGP fijo de 7 variables que cumple la tabla (signos en h=0 y h=1, 4 ceros). Devuelve dict(A, A0, Bx)."""
    for intento in range(200):
        rg = rng_for(7, 0, intento)
        A1 = 0.5 * np.eye(7) + 0.04 * rg.standard_normal((7, 7))
        A1[4, 4] = 0.9
        A2 = -0.1 * np.eye(7)
        A2[4, 4] = 0.0
        if radio([A1, A2]) >= 0.97:
            continue
        A0 = 0.4 * rg.standard_normal((7, 7))
        r = restr_prereg()
        for (i, j, sg, h) in r.signos:
            A0[i, j] = sg * rg.uniform(0.3, 1.0)
        for (i, j, h) in r.ceros:
            A0[i, j] = 0.0
        A0[:, 5:] = 0.5 * rg.standard_normal((7, 2))
        Phi = bvar.ma_coefs(B_from([A1, A2]), 7, 2, 2)[0]
        ok = all(sg * (Phi[h] @ A0)[i, j] > 0 for (i, j, sg, h) in r.signos)
        if ok:
            Bx = np.zeros((2, 7))        # filas: COVID, EPA 2021T1
            Bx[0, 5], Bx[0, 2], Bx[0, 0] = -2.0, -1.5, -0.5
            Bx[1, 5], Bx[1, 2] = 1.5, 0.5
            return dict(A=[A1, A2], A0=A0, Bx=Bx, intento=intento)
    raise RuntimeError("no se encontro un DGP compatible con la tabla")


def sim_prereg(dg, rg, T=T_PRE, burn=100):
    A1, A2 = dg["A"]
    X = np.zeros((T, 2))
    X[IDX_COVID, 0] = 1.0
    X[IDX_EPA, 1] = 1.0
    eps = rg.standard_normal((T + burn, 7))
    Y = np.zeros((T + burn, 7))
    for t in range(2, T + burn):
        ex = X[t - burn] @ dg["Bx"] if t >= burn else 0.0
        Y[t] = A1 @ Y[t - 1] + A2 @ Y[t - 2] + ex + dg["A0"] @ eps[t]
    return Y[burn:], X, eps[burn:]


def contrib_verdad(dg, eps):
    """Contribucion verdadera del shock j a la variable i en t (efectiva, t >= p): suma_s Phi_{t-s} A0[:, j] eps_s[j]."""
    Te = eps.shape[0] - P_PRE
    Phi = bvar.ma_coefs(B_from(dg["A"]), 7, 2, Te - 1)[0]
    G = Phi @ dg["A0"]
    e = eps[P_PRE:]
    out = np.zeros((Te, 7, 7))
    for t in range(Te):
        for s in range(t + 1):
            out[t] += G[t - s] * e[s][None, :]
    return out


def mc_prereg(R, D, M, solo_impacto, n_obj=300):
    """Valida la configuracion pre-registrada. Devuelve el diccionario de tiempos (no se escribe en el csv: no es determinista)."""
    dg = dgp_prereg()
    r = restr_prereg(solo_impacto)
    tag = "V3_solo_impacto" if solo_impacto else "principal"
    A0t = dg["A0"]
    restringida = np.zeros((7, 7), bool)
    for (i, j, sg, h) in r.signos:
        restringida[i, j] = True
    zero_c = np.zeros((7, 7), bool)
    for (i, j, h) in r.ceros:
        zero_c[i, j] = True
    ident = np.zeros((7, 7), bool)
    ident[:, :5] = True
    Phi_t = bvar.ma_coefs(B_from(dg["A"]), 7, 2, 12)[0] @ A0t
    tr_ok = np.zeros((7, 7), bool)
    tr_ok[:, :5] = True
    libre0 = ident & ~restringida & ~zero_c & (np.abs(A0t) >= 0.2)
    delta = np.array([0, 0, 0, 0, 1, 0, 0.0])
    ac, fth, ess, nacc, rpa, zmax, hderr, utiles, sig_ok, sig_band, bad_band = [], [], [], [], [], [], [], [], [], [], []
    cov68t, cov90t, sgn_t, excl_t, wrong_t = [], [], [], [], []
    c90_irf = {"restr": [], "libre": []}
    exo_est = []
    tiempo = 0.0
    nrep_hd = 0
    for rep in range(R):
        rg = rng_for(8, int(solo_impacto), rep)
        Y, X, eps = sim_prereg(dg, rg)
        post = bvar.estimar(Y, P_PRE, delta=delta, exog=X)
        B, Sig = bvar.muestrear(post, D, rg)
        t0 = time.time()
        res = signos.identificar(B, Sig, 7, P_PRE, r, H=12, n_objetivo=n_obj, rotaciones=M, rng=rg)
        tiempo += time.time() - t0
        N = len(res["Q"])
        ac.append(res["acept"])
        fth.append(res["frac_theta_acept"])
        rpa.append(res["rot_total"] / max(N, 1))
        if N < 20:
            utiles.append(0)
            continue
        utiles.append(1)
        nacc.append(N)
        ess.append(res["ess"])
        mz, fs = signos.comprobar(res, r)
        zmax.append(mz)
        exo_est.append(post["B"][14:16, :])
        w = res["peso"]
        bb = bvar.bandas(res["irf"], 0, w)
        for hh in (0, 1, 4, 8):
            cv = (bb["lo90"][hh] <= Phi_t[hh]) & (Phi_t[hh] <= bb["hi90"][hh])
            c90_irf["restr"].append(cv[restringida & ident].mean())
            c90_irf["libre"].append(cv[~restringida & ~zero_c & ident].mean())
        s0 = np.sign(bb["med"][0]) == np.sign(A0t)
        sig_ok.append(s0[libre0].mean())
        sig_band.append(((np.sign(bb["lo90"][0]) == np.sign(A0t)) & (np.sign(bb["hi90"][0]) == np.sign(A0t)))[libre0].mean())
        hd = signos.descomposicion_historica(res, Y, exog=X)
        hderr.append(hd["error"])
        fechas = np.arange(hd["contrib"].shape[1])
        trs = signos.sumar_tramos(hd["contrib"], fechas, TRAMOS_PRE)[..., :5]       # (N, tramo, var, shock identificado)
        cv_true = contrib_verdad(dg, eps)
        tv = np.stack([cv_true[a:b + 1].sum(0) for a, b in TRAMOS_PRE])[..., :5]
        bt = bvar.bandas(trs, 0, w)
        c68 = (bt["lo68"] <= tv) & (tv <= bt["hi68"])
        c90 = (bt["lo90"] <= tv) & (tv <= bt["hi90"])
        cov68t.append(c68.mean((1, 2)))
        cov90t.append(c90.mean((1, 2)))
        grande = np.abs(tv) >= 0.5
        sgn_t.append(((np.sign(bt["med"]) == np.sign(tv)) & grande).sum() / max(grande.sum(), 1))
        ex_ok = ((bt["lo90"] > 0) | (bt["hi90"] < 0))
        right = (np.sign(bt["med"]) == np.sign(tv))
        excl_t.append((ex_ok & right & grande).sum() / max(grande.sum(), 1))
        wrong_t.append((ex_ok & ~right & grande).sum() / max(grande.sum(), 1))
        nrep_hd += 1
        if rep < 3:
            print(f"   [{tag}] rep {rep}: N={N} acept={res['acept']:.2e} fth={res['frac_theta_acept']:.2f} ESS={res['ess']:.1f} cov90_DH={c90.mean():.3f}", flush=True)
    Rv = int(sum(utiles))
    add("prereg", tag, T_PRE, R, "replicas_con_>=20_aceptadas", Rv)
    add("prereg", tag, T_PRE, R, "aceptacion_por_rotacion", np.mean(ac))
    add("prereg", tag, T_PRE, R, "frac_theta_con_aceptada", np.mean(fth), ">= 0.01 (viabilidad)", np.mean(fth) >= 0.01)
    add("prereg", tag, T_PRE, R, "frac_theta_con_aceptada_minimo_replicas", np.min(fth))
    add("prereg", tag, T_PRE, R, "rotaciones_por_aceptada", np.mean(rpa))
    if Rv:
        add("prereg", tag, T_PRE, Rv, "aceptadas_medias", np.mean(nacc))
        add("prereg", tag, T_PRE, Rv, "ESS_medio", np.mean(ess))
        add("prereg", tag, T_PRE, Rv, "ESS_minimo", np.min(ess))
        add("prereg", tag, T_PRE, Rv, "restricciones_cumplidas_max_abs_cero", max(zmax), "< 1e-10", max(zmax) < 1e-10)
        add("prereg", tag, T_PRE, Rv, "descomposicion_historica_error_max_con_exogenas", max(hderr), "< 1e-8", max(hderr) < 1e-8)
        add("prereg", tag, T_PRE, Rv, "cobertura_90_IRF_restringidas", np.mean(c90_irf["restr"]))
        add("prereg", tag, T_PRE, Rv, "cobertura_90_IRF_no_restringidas", np.mean(c90_irf["libre"]))
        add("prereg", tag, T_PRE, Rv, "signo_impacto_recuperado_no_restringidas", np.mean(sig_ok), ">= 0.90", np.mean(sig_ok) >= 0.90)
        add("prereg", tag, T_PRE, Rv, "banda90_excluye_cero_con_signo_correcto_impacto", np.mean(sig_band))
        c68a, c90a = np.mean(cov68t, 0), np.mean(cov90t, 0)
        for k, nom in enumerate(TRAMOS_NOM):
            add("prereg", tag, T_PRE, Rv, f"DH_cobertura_68_{nom}", c68a[k])
            add("prereg", tag, T_PRE, Rv, f"DH_cobertura_90_{nom}", c90a[k], "[0.85, 0.98]", 0.85 <= c90a[k] <= 0.98)
        add("prereg", tag, T_PRE, Rv, "DH_cobertura_90_total", float(np.mean(cov90t)), "[0.85, 0.98]", 0.85 <= np.mean(cov90t) <= 0.98)
        add("prereg", tag, T_PRE, Rv, "DH_cobertura_68_total", float(np.mean(cov68t)))
        add("prereg", tag, T_PRE, Rv, "DH_signo_tramo_correcto_(|contrib|>=0.5)", np.mean(sgn_t))
        add("prereg", tag, T_PRE, Rv, "DH_banda90_excluye_0_con_signo_correcto_(|contrib|>=0.5)", np.mean(excl_t))
        add("prereg", tag, T_PRE, Rv, "DH_banda90_excluye_0_con_signo_ERRONEO_(|contrib|>=0.5)", np.mean(wrong_t))
        ex = np.mean(exo_est, 0)
        add("prereg", tag, T_PRE, Rv, "coef_COVID_sobre_e_estimado_(verdad_-2.0)", ex[0, 5])
        add("prereg", tag, T_PRE, Rv, "coef_EPA_sobre_e_estimado_(verdad_1.5)", ex[1, 5])
    print(f"[PREREG {tag}] R={R} utiles={Rv} acept={np.mean(ac):.2e} fth={np.mean(fth):.3f} rot/acept={np.mean(rpa):.0f} "
          f"ESS={np.mean(ess) if ess else 0:.1f} N={np.mean(nacc) if nacc else 0:.0f} DH cov90={np.mean(cov90t) if cov90t else float('nan'):.3f} "
          f"signo={np.mean(sig_ok) if sig_ok else float('nan'):.3f} ({tiempo:.0f}s identificacion)", flush=True)
    TIEMPOS[f"prereg|{tag}"] = (tiempo, R)


def cuadricula_M(R, D, Ms):
    """Coste frente a M (rotaciones por theta) en la configuracion principal: fraccion de theta con aceptada, aceptadas y ESS."""
    dg = dgp_prereg()
    r = restr_prereg(False)
    delta = np.array([0, 0, 0, 0, 1, 0, 0.0])
    for M in Ms:
        fth, nacc, ess, ac = [], [], [], []
        t0 = time.time()
        for rep in range(R):
            rg = rng_for(9, rep)
            Y, X, eps = sim_prereg(dg, rg)
            post = bvar.estimar(Y, P_PRE, delta=delta, exog=X)
            B, Sig = bvar.muestrear(post, D, rg)
            res = signos.identificar(B, Sig, 7, P_PRE, r, H=2, rotaciones=M, rng=rg)
            fth.append(res["frac_theta_acept"])
            nacc.append(len(res["Q"]))
            ess.append(res["ess"])
            ac.append(res["acept"])
        t = time.time() - t0
        tag = f"M{M}"
        add("prereg_M", tag, T_PRE, R, "frac_theta_con_aceptada", np.mean(fth))
        add("prereg_M", tag, T_PRE, R, "aceptadas_medias_de_D", np.mean(nacc))
        add("prereg_M", tag, T_PRE, R, "ESS_medio", np.mean(ess))
        add("prereg_M", tag, T_PRE, R, "aceptacion_por_rotacion", np.mean(ac))
        TIEMPOS[f"M|{M}"] = (t, R)
        print(f"[M={M}] D={D} fth={np.mean(fth):.3f} N={np.mean(nacc):.0f} ESS={np.mean(ess):.1f} ({t:.0f}s)", flush=True)


# ======================================================================== 3b. VAR por regimenes con los 5 tramos reales
LONG_REG = (16, 22, 24, 9, 15)
HUECOS_REG = (2, 0, 1, 0)   # observaciones de transicion tras cada tramo (2008T1-T2 tras el 1.o; 2020T1 tras el 3.o)
COEF_REG = {"cambios": (0.2, 0.6, 0.3, 0.7, 0.4), "sin_cambio": (0.4, 0.4, 0.4, 0.4, 0.4)}
NOM_REG = ["T1 (16)", "T2 (22)", "T3 (24)", "T4 (9)", "T5 (15)"]


def segs_reg5(p=2):
    segs, pos = [], 0
    for k, Lk in enumerate(LONG_REG):
        segs.append((pos, pos + Lk))
        pos += Lk + (HUECOS_REG[k] if k < len(HUECOS_REG) else 0)
    return segs, pos


def dgp_reg5(rg, coefs, p=2, burn=60):
    segs, Te = segs_reg5(p)
    n, T = 4, Te + p
    A2 = -0.1 * np.eye(n)
    Y = np.zeros((T + burn, n))
    reg = np.full(Te, -1)
    for k, (a, b) in enumerate(segs):
        reg[a:b] = k
    for t in range(2, T + burn):
        te = t - burn - p
        k = reg[te] if te >= 0 and reg[te] >= 0 else (0 if te < 0 else int(np.max(reg[:te + 1])))   # los huecos usan el regimen previo
        A1 = 0.3 * np.eye(n)
        A1[0, 0] = coefs[k]
        A1[1, 0], A1[2, 1] = 0.15, 0.15
        Y[t] = A1 @ Y[t - 1] + A2 @ Y[t - 2] + 0.5 * rg.standard_normal(n)
    return Y[burn:], segs


REG_MODOS = {"GLP": {}, "lam1": dict(lam=1.0), "plano_lam5": dict(lam=5.0)}


def mc_regimenes5(R):
    p = 2
    for (esc0, coefs), (modo, kw) in [(e, mo) for e in COEF_REG.items() for mo in REG_MODOS.items()]:
        esc = f"{esc0}|{modo}"
        K = len(LONG_REG)
        cov68 = [[] for _ in range(K)]
        cov90 = [[] for _ in range(K)]
        err, wpost, wprior, lams = [[] for _ in range(K)], [[] for _ in range(K)], [[] for _ in range(K)], []
        det = [[] for _ in range(K - 1)]
        t0 = time.time()
        for rep in range(R):
            rg = rng_for(10, int(esc0 == "cambios"), rep)
            Y, segs = dgp_reg5(rg, coefs)
            res = tvp.var_regimenes(Y, p, tramos=segs, **kw)
            lams.append(res["lam"])
            Bp, _ = bvar.muestrear(res["prior"], 400, rg)
            wp = np.subtract(*np.quantile(Bp[:, 0, 0], [0.95, 0.05]))
            draws = []
            for k in range(K):
                B, _ = bvar.muestrear(res["regimenes"][k], 400, rg)
                x = B[:, 0, 0]
                draws.append(x)
                for lv, qs, dst in (("68", (0.16, 0.84), cov68), ("90", (0.05, 0.95), cov90)):
                    lo, hi = np.quantile(x, qs)
                    dst[k].append(lo <= coefs[k] <= hi)
                err[k].append(x.mean() - coefs[k])
                wpost[k].append(np.subtract(*np.quantile(x, [0.95, 0.05])))
                wprior[k].append(wp)
            for k in range(K - 1):
                d = draws[k + 1] - draws[k]
                lo, hi = np.quantile(d, [0.05, 0.95])
                truth = coefs[k + 1] - coefs[k]
                det[k].append((lo > 0 or hi < 0) if abs(truth) < 1e-12 else ((lo > 0) if truth > 0 else (hi < 0)))
        for k in range(K):
            c90 = float(np.mean(cov90[k]))
            nm = NOM_REG[k]
            add("regimenes5", esc, 88, R, f"cobertura_68_{nm}", np.mean(cov68[k]))
            add("regimenes5", esc, 88, R, f"cobertura_90_{nm}", c90, "[0.85, 0.98]", 0.85 <= c90 <= 0.98)
            add("regimenes5", esc, 88, R, f"sesgo_{nm}", np.mean(err[k]))
            add("regimenes5", esc, 88, R, f"RMSE_media_posterior_{nm}", np.sqrt(np.mean(np.square(err[k]))))
            add("regimenes5", esc, 88, R, f"ancho90_posterior_{nm}", np.mean(wpost[k]))
            add("regimenes5", esc, 88, R, f"ratio_ancho90_posterior_sobre_prior_{nm}", np.mean(wpost[k]) / np.mean(wprior[k]), "< 0.75 (informativo)", np.mean(wpost[k]) / np.mean(wprior[k]) < 0.75)
        for k in range(K - 1):
            nm = f"{NOM_REG[k][:2]}->{NOM_REG[k + 1][:2]}"
            if esc0 == "cambios":
                add("regimenes5", esc, 88, R, f"deteccion_{nm}_(cambio_{coefs[k + 1] - coefs[k]:+.1f})", np.mean(det[k]), ">= 0.80", np.mean(det[k]) >= 0.80)
            else:
                add("regimenes5", esc, 88, R, f"falsos_positivos_{nm}_(bilateral)", np.mean(det[k]), "<= 0.15", np.mean(det[k]) <= 0.15)
        add("regimenes5", esc, 88, R, "lambda_mediana", np.median(lams))
        print(f"[REG5 {esc}] R={R} cov90={[round(float(np.mean(c)), 2) for c in cov90]} ratio={[round(float(np.mean(a) / np.mean(b)), 2) for a, b in zip(wpost, wprior)]} "
              f"det={[round(float(np.mean(d)), 2) for d in det]} lam~{np.median(lams):.2f} ({time.time() - t0:.0f}s)", flush=True)


def dgp_tvp(rg, ruptura, T=120, burn=50, k_break=None):
    n = 3
    A1 = 0.4 * np.eye(n)
    A1[0, 1], A1[1, 2] = 0.1, 0.1
    A2 = -0.1 * np.eye(n)
    Y = np.zeros((T + burn, n))
    for t in range(2, T + burn):
        A = A1.copy()
        if ruptura and t - burn >= k_break:
            A[0, 0] = 0.8
        Y[t] = A @ Y[t - 1] + A2 @ Y[t - 2] + 0.5 * rg.standard_normal(n)
    return Y[burn:]


def mc_tvp(R_by, n_iter, burn_it):
    tau, p = 30, 2
    Te = 120 - p - tau
    mid = Te // 2
    k_break = mid + tau + p  # indice en Y a partir del cual cambia
    for esc, ruptura, kQ in (("ruptura_kQ0.10", True, 0.10), ("sin_ruptura_kQ0.10", False, 0.10), ("ruptura_kQ0.30", True, 0.30),
                             ("sin_ruptura_kQ0.30", False, 0.30), ("ruptura_kQ0.01", True, 0.01)):
        R = R_by[esc]
        cov = {c: {"68": [], "90": []} for c in ("rupt", "ctrl")}
        det, dif, rmse, sg = [], [], [], []
        t0 = time.time()
        for rep in range(R):
            rg = rng_for(5, int(ruptura), int(round(kQ * 100)), rep)
            Y = dgp_tvp(rg, ruptura, k_break=k_break)
            res = tvp.estimar(Y, p, tau=tau, n_iter=n_iter, burn=burn_it, thin=4, rng=rg, kQ=kQ)
            true_r = np.where(np.arange(Te) < mid, 0.4, 0.8) if ruptura else np.full(Te, 0.4)
            for nm, tr, tp in (("rupt", tvp.trayectoria(res, 0, 0, 1), true_r), ("ctrl", tvp.trayectoria(res, 2, 2, 1), np.full(Te, 0.4))):
                for lv, qs in (("68", (0.16, 0.84)), ("90", (0.05, 0.95))):
                    lo, hi = np.quantile(tr, qs, axis=0)
                    cov[nm][lv].append(((lo <= tp) & (tp <= hi)).mean())
            tr = tvp.trayectoria(res, 0, 0, 1)
            q = Te // 4
            d = tr[:, -q:].mean(1) - tr[:, :q].mean(1)
            lo, hi = np.quantile(d, [0.05, 0.95])
            det.append(lo > 0)
            dif.append(d.mean())
            rmse.append(np.sqrt(np.mean((tr.mean(0) - true_r) ** 2)))
            sg.append(tvp.volatilidad(res).mean() / 0.5)
        tag = esc
        for nm in ("rupt", "ctrl"):
            c90 = float(np.mean(cov[nm]["90"]))
            add("TVP", tag, 120, R, f"cobertura_68_{'coef_con_ruptura' if nm == 'rupt' else 'coef_control_constante'}", np.mean(cov[nm]["68"]))
            add("TVP", tag, 120, R, f"cobertura_90_{'coef_con_ruptura' if nm == 'rupt' else 'coef_control_constante'}", c90, "[0.85, 0.98]", 0.85 <= c90 <= 0.98)
        if ruptura:
            add("TVP", tag, 120, R, "deteccion_cambio_(banda90_late-early>0)", np.mean(det), ">= 0.80", np.mean(det) >= 0.80)
            add("TVP", tag, 120, R, "cambio_estimado_medio_(verdad_0.4_en_cuartiles_extremos)", np.mean(dif), "sesgo rel. <= 0.10", abs(np.mean(dif) - 0.4) / 0.4 <= 0.10)
        else:
            add("TVP", tag, 120, R, "falsos_positivos_(banda90_late-early>0)", np.mean(det), "<= 0.15", np.mean(det) <= 0.15)
        add("TVP", tag, 120, R, "RMSE_senda_coef_rupt", np.mean(rmse))
        add("TVP", tag, 120, R, "sigma_estimado_sobre_verdad_(0.5)", np.mean(sg), "[0.9, 1.1]", 0.9 <= np.mean(sg) <= 1.1)
        print(f"[TVP {tag}] R={R} cov90 rupt={np.mean(cov['rupt']['90']):.3f} ctrl={np.mean(cov['ctrl']['90']):.3f} det/FP={np.mean(det):.2f} dif={np.mean(dif):.2f} ({time.time() - t0:.0f}s)", flush=True)


def mc_regimenes(R):
    """Alternativa: VAR por regimenes con prior comun y ruptura CONOCIDA a mitad de la muestra efectiva."""
    p = 2
    Te = 120 - p
    mid = Te // 2
    for esc, ruptura in (("ruptura", True), ("sin_ruptura", False)):
        cov = {"68": [], "90": []}
        det, dif, lams = [], [], []
        for rep in range(R):
            rg = rng_for(6, int(ruptura), rep)
            Y = dgp_tvp(rg, ruptura, k_break=mid + p)
            res = tvp.var_regimenes(Y, p, [mid])
            lams.append(res["lam"])
            for r_, tv in ((0, 0.4), (1, 0.8 if ruptura else 0.4)):
                B, _ = bvar.muestrear(res["regimenes"][r_], 400, rg)
                x = B[:, 0, 0]
                for lv, qs in (("68", (0.16, 0.84)), ("90", (0.05, 0.95))):
                    lo, hi = np.quantile(x, qs)
                    cov[lv].append(lo <= tv <= hi)
            d = tvp.diferencia_regimenes(res, 0, 1, 0, 0, 1, 400, rg)
            det.append(np.quantile(d, 0.05) > 0)
            dif.append(d.mean())
        c90 = float(np.mean(cov["90"]))
        add("regimenes", esc, 120, R, "cobertura_68_coef", np.mean(cov["68"]))
        add("regimenes", esc, 120, R, "cobertura_90_coef", c90, "[0.85, 0.98]", 0.85 <= c90 <= 0.98)
        if ruptura:
            add("regimenes", esc, 120, R, "deteccion_cambio_(banda90_dif>0)", np.mean(det), ">= 0.80", np.mean(det) >= 0.80)
            add("regimenes", esc, 120, R, "cambio_estimado_medio_(verdad_0.4)", np.mean(dif), "sesgo rel. <= 0.10", abs(np.mean(dif) - 0.4) / 0.4 <= 0.10)
        else:
            add("regimenes", esc, 120, R, "falsos_positivos_(banda90_dif>0)", np.mean(det), "<= 0.15", np.mean(det) <= 0.15)
        add("regimenes", esc, 120, R, "lambda_mediana", np.median(lams))
        print(f"[REGIMENES {esc}] R={R} cov90={c90:.3f} det/FP={np.mean(det):.2f} dif={np.mean(dif):.2f} lam~{np.median(lams):.2f}", flush=True)


def _todo(serie):
    """True si todos los valores no vacios de `cumple` son verdaderos (acepta bool o texto del csv)."""
    v = [x for x in serie if x is True or x is False or str(x) in ("True", "False")]
    return len(v) > 0 and all(x is True or str(x) == "True" for x in v)


def V(df, herr, esc, T, met):
    m = df[(df.herramienta == herr) & (df.escenario == esc) & (df["metrica"] == met)]
    if T != "":
        m = m[m["T"].astype(str) == str(T)]
    return float(m["valor"].iloc[0])


def hay(df, herr, esc, met):
    return bool(((df.herramienta == herr) & (df.escenario == esc) & (df["metrica"] == met)).any())


S4 = (("signos", 120), ("signos", 60), ("signos+ceros", 120))
UMBRALES = ("Reglas (definidas por el ejecutor, algunas DESPUES de ver las cifras de F3; ver docs/v8/decisiones.md): "
            "cobertura 90 % en [0,85; 0,98] = nominal; [0,80; 0,99] = con reservas (BVAR) o >= 0,85 (signos); sesgo relativo IRF <= 10 % apta, <= 30 % con reservas; "
            "recuperacion del signo del impacto >= 90 %; deteccion >= 80 % y falsos positivos <= 15 %; viabilidad del muestreo: fraccion de theta con alguna rotacion aceptada >= 1 % y ESS >= 30.")


def etiq_prereg(df, tag):
    """Tres etiquetas por configuracion pre-registrada, con reglas explicitas: (viabilidad y mecanica, signo del impacto no restringido, DH por tramos)."""
    fth = V(df, "prereg", tag, T_PRE, "frac_theta_con_aceptada")
    if fth < 0.01 or not hay(df, "prereg", tag, "ESS_medio"):
        return "inviable (fraccion de theta con aceptada < 1 %)", "n/d", "n/d"
    ess = V(df, "prereg", tag, T_PRE, "ESS_medio")
    essmin = V(df, "prereg", tag, T_PRE, "ESS_minimo")
    z = V(df, "prereg", tag, T_PRE, "restricciones_cumplidas_max_abs_cero")
    hd = V(df, "prereg", tag, T_PRE, "descomposicion_historica_error_max_con_exogenas")
    sg = V(df, "prereg", tag, T_PRE, "signo_impacto_recuperado_no_restringidas")
    c90 = V(df, "prereg", tag, T_PRE, "DH_cobertura_90_total")
    if not (z < 1e-10 and hd < 1e-8):
        mec = "no apta (ceros o identidad de la descomposicion historica)"
    elif ess < 30:
        mec = f"con reservas (ESS medio {ess:.0f} < 30)"
    elif essmin < 30:
        mec = f"apta (viable: theta con aceptada {fth:.2f}, ESS medio {ess:.0f}; con reservas por replicas con ESS minimo {essmin:.0f} < 30)"
    else:
        mec = f"apta (viable: theta con aceptada {fth:.2f}, ESS medio {ess:.0f})"
    sig = "apta" if sg >= 0.90 else f"no apta (signo del impacto no restringido recuperado en {sg:.2f} < 0,90)"
    if 0.85 <= c90 <= 0.98:
        dh = f"apta en cobertura (90 % = {c90:.2f}), pero ver poder de la banda (excluye 0 en pocas celdas)"
    elif c90 > 0.98:
        dh = f"con reservas (bandas conservadoras: cobertura 90 % = {c90:.2f} > 0,98)"
    elif c90 >= 0.80:
        dh = f"con reservas (cobertura 90 % = {c90:.2f} < 0,85)"
    else:
        dh = f"no apta (cobertura 90 % = {c90:.2f} < 0,80)"
    return mec, sig, dh


def etiq_reg5(df):
    esc = "cambios|GLP"
    cov = [V(df, "regimenes5", esc, 88, f"cobertura_90_{n}") for n in NOM_REG]
    det = [V(df, "regimenes5", esc, 88, d) for d in df[(df.herramienta == "regimenes5") & (df.escenario == esc) & df.metrica.str.startswith("deteccion_")]["metrica"]]
    fp = [float(x) for x in df[(df.herramienta == "regimenes5") & (df.escenario == "sin_cambio|GLP") & df.metrica.str.startswith("falsos_positivos")]["valor"]]
    if all(0.85 <= c <= 0.98 for c in cov) and min(det) >= 0.8 and max(fp) <= 0.15:
        return "apta"
    if min(cov) >= 0.80 and max(fp) <= 0.15:
        return "con reservas"
    return "no apta"


def etiquetas(df):
    """Etiquetas apta / con reservas / no apta con reglas declaradas (ver validacion.md)."""
    E = {}
    # BVAR-GLP. Celdas segun el tipo de variable: tasas (delta 0 o mixto) y nivel casi paseo aleatorio (delta 1)
    ml_ok = _todo(df[(df.escenario.str.startswith("logml_vs_"))]["cumple"])

    def etq_bvar(cel):
        cov = [V(df, "BVAR", f"{e}|{m}", T, "cobertura_90") for e, T, m in cel]
        ses = [V(df, "BVAR", f"{e}|{m}", T, "sesgo_rel_IRF_h1-12") for e, T, m in cel]
        if ml_ok and all(0.85 <= c <= 0.98 for c in cov) and all(s_ <= 0.10 for s_ in ses):
            return "apta"
        if ml_ok and all(0.80 <= c <= 0.99 for c in cov) and all(s_ <= 0.30 for s_ in ses):
            return "con reservas"
        return f"no apta (cobertura 90 % {min(cov):.2f}-{max(cov):.2f}; sesgo absoluto relativo hasta {max(ses):.2f})"
    cel_tasas = [(e, T, m) for (e, m) in (("denso", "GLP"), ("tasas", "GLP"), ("tasas", "GLP_delta_mixto")) for T in (120, 60)]
    cel_nivel = [("casi_RW", T, "GLP_delta1") for T in (120, 60)]
    E["BVAR-GLP en tasas (delta 0 o mixto; DGP denso y tasas; T = 60 y 120)"] = etq_bvar(cel_tasas)
    E["BVAR-GLP en nivel casi paseo aleatorio (delta 1; T = 60 y 120)"] = etq_bvar(cel_nivel)
    E["BVAR-GLP casi paseo aleatorio con delta 0 (uso NO previsto; sensibilidad)"] = etq_bvar([("casi_RW", T, "GLP") for T in (120, 60)])
    atn = [V(df, "BVAR", f"{e}|{m}", T, "atenuacion_firmada_rel_h1-12") for (e, T, m) in cel_tasas + cel_nivel]
    E["BVAR-GLP (direccion del sesgo de las IRF)"] = ("atenuadas hacia cero (atenuacion firmada > 0 en todas las celdas de uso previsto)" if all(a_ > 0 for a_ in atn)
                                                      else "direccion no uniforme")
    # signos 4 variables: mecanica
    hd = max(V(df, "signos", f"{e}|T{T}", T, "descomposicion_historica_error_max") for e, T in S4)
    z = V(df, "signos", "signos+ceros|T120", 120, "restricciones_cumplidas_max_abs_cero")
    inv = _todo(df[df.escenario == "ARW_invariancia_al_orden"]["cumple"])
    E["signos/ceros (mecanica: restricciones, FEVD, descomposicion historica)"] = "apta" if (hd < 1e-8 and z < 1e-10) else "no apta"
    E["pesos de importancia propios (Haar condicionado a los ceros; no se afirman iguales a ARW)"] = "apta (invariancia al orden)" if inv else "con reservas"
    sg = [V(df, "signos", f"{e}|T{T}", T, "signo_impacto_recuperado_no_restringidas") for e, T in S4]
    c90r = [V(df, "signos", f"{e}|T{T}", T, "cobertura_90_IRF_restringidas") for e, T in S4]
    c90l = [V(df, "signos", f"{e}|T{T}", T, "cobertura_90_IRF_no_restringidas") for e, T in S4]
    todas = c90r + c90l
    k4 = "signos/ceros, 4 variables solo impacto (inferencia: bandas y signo del impacto)"
    if all(x >= 0.90 for x in sg) and all(0.85 <= c <= 0.98 for c in todas):
        E[k4] = "apta"
    elif all(x >= 0.90 for x in sg) and all(0.85 <= c for c in todas):
        E[k4] = "con reservas (bandas conservadoras: cobertura 90 % por encima de 0,98; conjunto identificado)"
    else:
        E[k4] = "no apta (signo del impacto < 90 % o cobertura < 0,85)"
    # configuracion pre-registrada
    for tag, nom in (("principal", "principal (7 var, T=88, h=0-1, 4 ceros)"), ("V3_solo_impacto", "variante V3 (solo impacto, sin q)")):
        mec, sig, dh = etiq_prereg(df, tag)
        E[f"signos PRE-REGISTRADO {nom}: viabilidad y mecanica"] = mec
        E[f"signos PRE-REGISTRADO {nom}: signo del impacto no restringido"] = sig
        E[f"signos PRE-REGISTRADO {nom}: descomposicion historica por tramos"] = dh
    # TVP
    def tv(e, m):
        return V(df, "TVP", e, 120, m)
    best = None
    for kq in ("0.10", "0.30"):
        c90 = tv(f"ruptura_kQ{kq}", "cobertura_90_coef_con_ruptura")
        d = tv(f"ruptura_kQ{kq}", "deteccion_cambio_(banda90_late-early>0)")
        fp = tv(f"sin_ruptura_kQ{kq}", "falsos_positivos_(banda90_late-early>0)")
        if 0.85 <= c90 <= 0.98 and d >= 0.80 and fp <= 0.15:
            best = ("apta", kq)
            break
        if best is None and c90 >= 0.75 and d >= 0.50 and fp <= 0.15:
            best = ("con reservas", kq)
    sig_ok = _todo(df[(df.herramienta == "TVP") & (df.metrica == "sigma_estimado_sobre_verdad_(0.5)")]["cumple"])
    E["TVP-VAR-SV (convergencia y volatilidad)"] = "apta" if sig_ok else "con reservas"
    E["TVP-VAR-SV (deteccion de un cambio de coeficiente con T efectivo = 88)"] = (f"{best[0]} (kQ={best[1]})" if best else "no apta (potencia y cobertura insuficientes con T efectivo = 88; ver kQ=0,10 y 0,30)")
    # regimenes
    c = V(df, "regimenes", "ruptura", 120, "cobertura_90_coef")
    d = V(df, "regimenes", "ruptura", 120, "deteccion_cambio_(banda90_dif>0)")
    fp = V(df, "regimenes", "sin_ruptura", 120, "falsos_positivos_(banda90_dif>0)")
    E["VAR por regimenes, 2 regimenes de 59 obs. (ruptura CONOCIDA)"] = "apta" if (0.85 <= c <= 0.98 and d >= 0.8 and fp <= 0.15) else ("con reservas" if (c >= 0.80 and d >= 0.5 and fp <= 0.15) else "no apta")
    E["VAR por regimenes, 5 tramos reales (16, 22, 24, 9, 15; n=4, p=2; con huecos)"] = etiq_reg5(df)
    return E


def tabla(cab, filas):
    return ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)] + ["| " + " | ".join(str(x) for x in f) + " |" for f in filas]


def rango(xs, f="{:.2f}"):
    xs = list(xs)
    return f.format(min(xs)) + " a " + f.format(max(xs)) if min(xs) != max(xs) else f.format(min(xs))


def informe(df, seg, tiempos):
    E = etiquetas(df)
    g = lambda h, e, T, m: V(df, h, e, T, m)  # noqa: E731
    md = []
    md.append("# V8-F3 grupo A (familia VAR): validacion por Monte Carlo (version corregida tras la revision F3)\n")
    md.append("Capa C4 (metodologico). Solo datos simulados; ningun dato real ni sellado. SEED = 20261010, un hilo, determinista (montecarlo.csv reproducible; "
              "los tiempos de computo van aparte en tiempos.json porque dependen de la maquina). "
              f"Computo total de la ejecucion: {seg:.0f} s ({seg / 60:.1f} min). Reproducir: `python3 src/v8/f3_montecarlo_var.py`. "
              "Resultados completos: `montecarlo.csv`. Referencias de metodo NO VERIFICADAS (sin acceso a Crossref). "
              "Las etiquetas se derivan de las cifras con reglas explicitas en `etiquetas()` (f3_montecarlo_var.py).\n")
    md.append("## Veredicto por herramienta\n")
    md += tabla(["Herramienta / componente", "Etiqueta"], [(k, f"**{v}**") for k, v in E.items()])
    md.append("\n" + UMBRALES + "\n")
    md.append("## Cambios respecto a la primera version (revision F3: H1, H2, H4, H9, H10, H12)\n")
    md.append("- H4: `exog` (ficticias deterministas) en `retardos`, `estimar`, `logml`, `prediccion` y `descomposicion_historica`; varianza a priori laxa (1e6), igual que la constante; "
              "la parte determinista de la DH incluye las exogenas (`det_exog` las aísla). Test de identidad con exogenas; la configuracion pre-registrada se valida con ficticias de COVID y EPA 2021T1.\n"
              "- H10: `delta` por variable (vector), por defecto 0 (antes 1). Las dummies de suma de coeficientes y de observacion inicial usan la media de las p primeras observaciones sin escalar por delta. "
              "Celdas con delta = 0 (por defecto), delta = 1 (sensibilidad) y mixto (0 en tasas, 1 en el nivel) en un DGP de tasas.\n"
              "- H2: para cada theta se prueba un numero FIJO `rotaciones` de rotaciones y se conservan TODAS las aceptadas (nunca se reintenta hasta aceptar); asi la distribucion de theta entre las aceptadas es proporcional a p(theta) P(S|theta).\n"
              "- H1/H16: validacion de la configuracion pre-registrada (7 variables, T = 88, p = 2, signos en h = 0-1, 4 ceros en la fila de poblacion, 2 shocks sin identificar) y de la variante V3 (solo impacto).\n"
              "- H9: `var_regimenes` admite tramos no contiguos (`tramos=[(ini, fin), ...]`) y se valida con 5 tramos de 16, 22, 24, 9 y 15 trimestres y huecos de transicion.\n"
              "- H12: sesgo firmado relativo (atenuacion) de las IRF del BVAR por celda.\n")
    md.append("## Replicas\n")
    reps = df.groupby(["herramienta", "escenario", "T"])["replicas"].first().reset_index()
    md += tabla(["Herramienta", "Escenario", "T", "Replicas"], [(r.herramienta, str(r.escenario).replace("|", " / "), r["T"], int(r.replicas)) for _, r in reps.iterrows()])
    # ------------------------------------------------------------------ BVAR
    md.append("\n## 1. BVAR normal-Wishart inversa (GLP)\n")
    md.append("DGP: VAR(2) de 4 variables. «denso»: radio espectral %.2f; «casi_RW»: 0,9 por variable; «tasas»: tres tasas poco persistentes (0,25-0,35) y una variable en nivel muy persistente (0,95), como el tipo. "
              "IRF de Cholesky; 300 sorteos de la posterior por replica; cobertura medida sobre las celdas no triviales (se excluyen los ceros estructurales del impacto). "
              "Modos: `GLP` = delta 0 (por defecto); `GLP_delta1` = delta 1 en todas (sensibilidad); `GLP_delta_mixto` = delta (0, 0, 0, 1) (solo «tasas»; configuracion de desviaciones.md); "
              "`plano_lam100` = referencia sin contraccion. Atenuacion firmada = -sum(signo(verdad)·(media de la mediana - verdad)) / sum|verdad| sobre h = 1-12 (positiva = IRF media mas cerca de 0 que la verdad).\n" % radio(dgp_bvar("denso")[0]))
    filas = []
    for e in BVAR_ESC:
        for T in (120, 60):
            for modo in ("GLP", "GLP_delta1", "GLP_delta_mixto", "plano_lam100"):
                tag = f"{e}|{modo}"
                if not hay(df, "BVAR", tag, "cobertura_90"):
                    continue
                lam = f"{g('BVAR', tag, T, 'lambda_mediana'):.2f}" if modo.startswith("GLP") else "100 (fijo)"
                filas.append((tag.replace("|", " / "), T, f"{g('BVAR', tag, T, 'cobertura_68'):.3f}", f"{g('BVAR', tag, T, 'cobertura_90'):.3f}",
                              f"{g('BVAR', tag, T, 'sesgo_rel_IRF_h1-12'):.3f}", f"{g('BVAR', tag, T, 'atenuacion_firmada_rel_h1-12'):+.3f}",
                              f"{g('BVAR', tag, T, 'frac_celdas_atenuadas_(|IRF|>=0.05)'):.2f}", lam))
    md += tabla(["Escenario / modo", "T", "cob. 68 %", "cob. 90 %", "sesgo abs. rel. h=1-12", "atenuacion firmada h=1-12", "frac. celdas atenuadas", "lambda mediana"], filas)
    md.append("\nAtenuacion firmada por horizonte (modo GLP):\n")
    md += tabla(["Escenario", "T", "h=1", "h=4", "h=8", "h=12"],
                [(e, T, *[f"{g('BVAR', f'{e}|GLP', T, f'atenuacion_firmada_rel_h{h}'):+.3f}" for h in (1, 4, 8, 12)]) for e in BVAR_ESC for T in (120, 60)])
    md.append("\nVerosimilitud marginal frente a fuerza bruta: error absoluto en log = "
              f"{g('BVAR', 'logml_vs_cuadratura_n1', '', 'error_abs_logml'):.1e} (cuadratura 2-D, n=1, p=1) y "
              f"{g('BVAR', 'logml_vs_cadena_predictiva_n3_dummies', '', 'error_abs_logml'):.1e} (cadena predictiva t multivariante, n=3, p=2, con dummies de suma de coeficientes y de observacion inicial).\n")
    glp = [(e, T) for e in BVAR_ESC for T in (120, 60)]
    uso = [(e, T, m) for (e, m) in (("denso", "GLP"), ("tasas", "GLP"), ("tasas", "GLP_delta_mixto"), ("casi_RW", "GLP_delta1")) for T in (120, 60)]
    c90 = [g("BVAR", f"{e}|{m}", T, "cobertura_90") for e, T, m in uso]
    c68 = [g("BVAR", f"{e}|{m}", T, "cobertura_68") for e, T, m in uso]
    sb = [g("BVAR", f"{e}|{m}", T, "sesgo_rel_IRF_h1-12") for e, T, m in uso]
    at = [g("BVAR", f"{e}|{m}", T, "atenuacion_firmada_rel_h1-12") for e, T, m in uso]
    fr = [g("BVAR", f"{e}|{m}", T, "frac_celdas_atenuadas_(|IRF|>=0.05)") for e, T, m in uso]
    mejor_g = sum(g("BVAR", f"{e}|GLP", T, "sesgo_rel_IRF_h1-12") < g("BVAR", f"{e}|plano_lam100", T, "sesgo_rel_IRF_h1-12") for e, T in glp)
    mejor_d1 = sum(g("BVAR", f"{e}|GLP_delta1", T, "sesgo_rel_IRF_h1-12") < g("BVAR", f"{e}|plano_lam100", T, "sesgo_rel_IRF_h1-12") for e, T in glp)
    cr0, cr1 = g("BVAR", "casi_RW|GLP", 120, "cobertura_90"), g("BVAR", "casi_RW|GLP_delta1", 120, "cobertura_90")
    md.append(f"Lectura (cifras del csv; celdas de uso previsto: denso, tasas con delta 0 y mixto, y casi_RW con delta 1; T = 60 y 120): cobertura del 90 % entre {rango(c90, '{:.3f}')} y del 68 % entre {rango(c68, '{:.3f}')}; "
              f"sesgo absoluto relativo entre {rango(sb, '{:.3f}')}; atenuacion firmada entre {rango(at, '{:+.3f}')} (fraccion de celdas atenuadas: {rango(fr)}). "
              f"El sesgo absoluto es menor que el del prior casi plano en {mejor_g} de 6 celdas con GLP delta 0 y en {mejor_d1} de 6 con GLP delta 1. "
              f"En el DGP casi_RW, delta 0 da cobertura del 90 % de {cr0:.2f} (T = 120) frente a {cr1:.2f} con delta 1: delta 0 no es adecuado para variables en nivel casi integradas. "
              "La atenuacion firmada separa el sesgo sistematico (hacia cero) del error de Monte Carlo por celda, que promediado en valor absoluto lo infla; crece con el horizonte en los DGP persistentes.\n")
    # ------------------------------------------------------------------ Signos 4 var
    md.append("## 2. Signos y ceros (RWZ / ARW): DGP de 4 variables, solo impacto\n")
    md.append("DGP estructural de 4 shocks (oferta, demanda, credito, monetario) sobre 4 variables (y, pi, cred, tipo). Restricciones de signo en el impacto: "
              "oferta (y+, pi-); demanda (y+, pi+, tipo+); credito (cred+, y+, pi+); monetario (tipo+, pi-, cred-, y-). Variante con ceros: el shock monetario no mueve y en el impacto y "
              "el de oferta no mueve el tipo (sustituyen a la restriccion y- del monetario). 400 sorteos de la posterior, 800 rotaciones por theta (todas las aceptadas se conservan; se para al llegar a 150 aceptadas). "
              "Cobertura medida en h = 0, 1, 4, 8. «Restringidas» = celdas con restriccion de signo; «no restringidas» = el resto (con verdad no nula).\n")
    filas = []
    for e, T in S4:
        t = f"{e}|T{T}"
        filas.append((e, T, int(df[(df.escenario == t)]["replicas"].iloc[0]), f"{g('signos', t, T, 'aceptacion_por_rotacion'):.4f}", f"{g('signos', t, T, 'frac_theta_con_aceptada_(800_rotaciones)'):.2f}",
                      f"{g('signos', t, T, 'ESS_medio_de_150'):.0f}", f"{g('signos', t, T, 'cobertura_68_IRF_restringidas'):.3f}", f"{g('signos', t, T, 'cobertura_68_IRF_no_restringidas'):.3f}",
                      f"{g('signos', t, T, 'cobertura_90_IRF_restringidas'):.3f}", f"{g('signos', t, T, 'cobertura_90_IRF_no_restringidas'):.3f}",
                      f"{g('signos', t, T, 'signo_impacto_recuperado_no_restringidas'):.3f}", f"{g('signos', t, T, 'banda90_excluye_cero_con_signo_correcto'):.3f}",
                      f"{g('signos', t, T, 'descomposicion_historica_error_max'):.1e}"))
    md += tabla(["Escenario", "T", "replicas", "aceptacion/rotacion", "frac. theta con aceptada", "ESS", "cob. 68 % restr.", "cob. 68 % no restr.", "cob. 90 % restr.", "cob. 90 % no restr.",
                 "signo impacto (no restr.)", "banda 90 % excluye 0 con signo correcto", "HD error max"], filas)
    md.append(f"\nCeros: maximo |IRF| en las restricciones de cero = {g('signos', 'signos+ceros|T120', 120, 'restricciones_cumplidas_max_abs_cero'):.1e}. "
              "Descomposicion historica: error maximo < 1e-8 en las replicas comprobadas (6 por escenario, 20 sorteos cada una). Las filas de la FEVD (h = 4, 8, 12, 20) suman 1.\n")
    n_inv = int(df[df.escenario == 'ARW_invariancia_al_orden']['replicas'].iloc[0])
    md.append("Pesos de importancia PROPIOS (no se afirma que coincidan con los de ARW; revision F3 H3): derivacion por coarea en el espacio (forma reducida, Q), objetivo p(theta)·Haar(Q) condicionado a los ceros. "
              f"Diagnostico: la distribucion ponderada de Q debe ser invariante al orden de los shocks. Con {n_inv} rotaciones en un theta, la diferencia maxima en E[Q^2] entre ordenes es "
              f"{g('signos', 'ARW_invariancia_al_orden', '', 'max_dif_E[Q^2]_entre_ordenes_con_pesos'):.3f} con pesos frente a {g('signos', 'ARW_invariancia_al_orden', '', 'max_dif_E[Q^2]_entre_ordenes_sin_pesos'):.3f} sin pesos; "
              f"suelo de ruido {g('signos', 'ARW_invariancia_al_orden', '', 'suelo_de_ruido_(mismo_orden_otra_semilla)'):.3f}; ESS medio {g('signos', 'ARW_invariancia_al_orden', '', 'ESS_medio'):.0f}.\n")
    cl = [g("signos", f"{e}|T{T}", T, "cobertura_90_IRF_no_restringidas") for e, T in S4]
    sgl = [g("signos", f"{e}|T{T}", T, "signo_impacto_recuperado_no_restringidas") for e, T in S4]
    bn = [g("signos", f"{e}|T{T}", T, "banda90_excluye_cero_con_signo_correcto") for e, T in S4]
    md.append(f"Lectura: la cobertura del 90 % de las celdas no restringidas esta en {rango(cl, '{:.3f}')} y el signo del impacto de los elementos no restringidos se recupera (por la mediana) en {rango(sgl, '{:.3f}')} de las replicas; "
              f"la banda del 90 % de esos elementos excluye el cero con el signo correcto en {rango(bn, '{:.3f}')} de las celdas. Con un conjunto identificado la banda mezcla incertidumbre de parametros e identificacion; "
              "la «cobertura» no tiene el significado frecuentista habitual.\n")
    # ------------------------------------------------------------------ Prereg
    md.append("## 2b. Configuracion PRE-REGISTRADA (hipotesis.md §5): 7 variables, T = 88, p = 2, h = 0-1, 4 ceros\n")
    md.append("DGP fijo (VAR(2) de 7 variables p, r, q, c, i, e, n) cuya matriz de impacto cumple exactamente la tabla (signos en h = 0 y h = 1; cero en el impacto de la poblacion ante los shocks de actividad, demanda, oferta y credito; "
              "dos shocks sin identificar). Incluye las ficticias exogenas de COVID (3 trimestres) y de EPA 2021T1 (efectos verdaderos sobre e: -2,0 y +1,5), estimadas con varianza a priori laxa. "
              "BVAR-GLP con delta = 1 en el tipo y 0 en el resto (desviaciones.md). Principal = signos en h = 0-1 con q en demanda y oferta; V3 = solo h = 0 y sin la restriccion de q (hipotesis.md V3). "
              "Por theta se prueban M rotaciones y se conservan todas las aceptadas. La DH se evalua por tramos (suma de contribuciones en los trimestres del tramo) contra la contribucion verdadera, "
              "solo para los 5 shocks identificados (los 2 libres son intercambiables). «Cobertura DH» = fraccion de celdas (tramo x variable x shock) cuya contribucion verdadera cae en la banda ponderada.\n")
    cols = ["principal", "V3_solo_impacto"]
    def fila(nm, m, f="{:.3g}"):
        return (nm, *[f.format(g("prereg", c, T_PRE, m)) if hay(df, "prereg", c, m) else "n/d" for c in cols])
    filas = [fila("replicas (de las simuladas) con >= 20 aceptadas", "replicas_con_>=20_aceptadas", "{:.0f}"),
             fila("aceptacion por rotacion", "aceptacion_por_rotacion", "{:.2e}"),
             fila("fraccion de theta con alguna rotacion aceptada (media)", "frac_theta_con_aceptada", "{:.3f}"),
             fila("fraccion de theta con aceptada (minimo entre replicas)", "frac_theta_con_aceptada_minimo_replicas", "{:.3f}"),
             fila("rotaciones probadas por aceptada", "rotaciones_por_aceptada", "{:.0f}"),
             fila("aceptadas por replica", "aceptadas_medias", "{:.0f}"),
             fila("ESS medio de los pesos", "ESS_medio", "{:.1f}"),
             fila("ESS minimo", "ESS_minimo", "{:.1f}"),
             fila("max |IRF| en los ceros", "restricciones_cumplidas_max_abs_cero", "{:.1e}"),
             fila("error maximo de la DH con exogenas", "descomposicion_historica_error_max_con_exogenas", "{:.1e}"),
             fila("signo del impacto recuperado (no restr.)", "signo_impacto_recuperado_no_restringidas", "{:.3f}"),
             fila("banda 90 % del impacto excluye 0 con signo correcto", "banda90_excluye_cero_con_signo_correcto_impacto", "{:.3f}"),
             fila("cobertura 90 % IRF restringidas", "cobertura_90_IRF_restringidas", "{:.3f}"),
             fila("cobertura 90 % IRF no restringidas", "cobertura_90_IRF_no_restringidas", "{:.3f}"),
             fila("cobertura DH 68 % (total)", "DH_cobertura_68_total", "{:.3f}"),
             fila("cobertura DH 90 % (total)", "DH_cobertura_90_total", "{:.3f}"),
             fila("DH: signo del tramo correcto (|contrib| >= 0,5)", "DH_signo_tramo_correcto_(|contrib|>=0.5)", "{:.3f}"),
             fila("DH: banda 90 % excluye 0 con signo correcto", "DH_banda90_excluye_0_con_signo_correcto_(|contrib|>=0.5)", "{:.3f}"),
             fila("DH: banda 90 % excluye 0 con signo ERRONEO", "DH_banda90_excluye_0_con_signo_ERRONEO_(|contrib|>=0.5)", "{:.3f}"),
             fila("coef. COVID sobre e estimado (verdad -2,0)", "coef_COVID_sobre_e_estimado_(verdad_-2.0)", "{:+.2f}"),
             fila("coef. EPA sobre e estimado (verdad +1,5)", "coef_EPA_sobre_e_estimado_(verdad_1.5)", "{:+.2f}")]
    md += tabla(["Metrica", "Principal (h = 0-1, con q)", "V3 (solo impacto, sin q)"], filas)
    md.append("\nCobertura de la descomposicion historica por tramos (solo shocks identificados):\n")
    filas = []
    for nom in TRAMOS_NOM:
        filas.append((nom, *[f"{g('prereg', c, T_PRE, f'DH_cobertura_68_{nom}'):.3f} / {g('prereg', c, T_PRE, f'DH_cobertura_90_{nom}'):.3f}" if hay(df, "prereg", c, f"DH_cobertura_90_{nom}") else "n/d" for c in cols]))
    md += tabla(["Tramo (trimestres)", "Principal: cob. 68 % / 90 %", "V3: cob. 68 % / 90 %"], filas)
    tp, rp = tiempos.get("prereg|principal", (float("nan"), 1))
    t3, r3 = tiempos.get("prereg|V3_solo_impacto", (float("nan"), 1))
    md.append(f"\nCoste (tiempo de pared de la identificacion por replica, un hilo; depende de la maquina): principal {tp / rp:.1f} s, V3 {t3 / r3:.1f} s.\n")
    md.append("Rotaciones por theta (M) frente a coste y rendimiento, configuracion principal (pocas replicas, sorteos de theta fijos):\n")
    filas = []
    for k, v in tiempos.items():
        if k.startswith("M|"):
            M = int(k.split("|")[1])
            t = f"M{M}"
            filas.append((M, f"{g('prereg_M', t, T_PRE, 'frac_theta_con_aceptada'):.3f}", f"{g('prereg_M', t, T_PRE, 'aceptadas_medias_de_D'):.0f}",
                          f"{g('prereg_M', t, T_PRE, 'ESS_medio'):.1f}", f"{g('prereg_M', t, T_PRE, 'aceptacion_por_rotacion'):.2e}", f"{v[0] / v[1]:.1f}"))
    md += tabla(["M", "frac. theta con aceptada", "aceptadas por replica", "ESS medio", "aceptacion por rotacion", "s por replica"], filas)
    fth = g("prereg", "principal", T_PRE, "frac_theta_con_aceptada")
    md.append(f"\nViabilidad de la principal: con M = {M_PRE} la fraccion de theta con alguna rotacion aceptada es {fth:.3f} "
              f"({'>=' if fth >= 0.01 else '<'} 1 %, regla de viabilidad) y el ESS medio {g('prereg', 'principal', T_PRE, 'ESS_medio') if hay(df, 'prereg', 'principal', 'ESS_medio') else float('nan'):.1f}. "
              "Se reportan ambas configuraciones (principal y V3) con cifras; la eleccion entre ellas y la fijacion de M y del numero de sorteos de theta corresponden al orquestador.\n")
    if hay(df, "prereg", "principal", "ESS_medio"):
        sgp, sg3 = g("prereg", "principal", T_PRE, "signo_impacto_recuperado_no_restringidas"), g("prereg", "V3_solo_impacto", T_PRE, "signo_impacto_recuperado_no_restringidas")
        dhp, dh3 = g("prereg", "principal", T_PRE, "DH_cobertura_90_total"), g("prereg", "V3_solo_impacto", T_PRE, "DH_cobertura_90_total")
        exp_, ex3 = (g("prereg", c, T_PRE, "DH_banda90_excluye_0_con_signo_correcto_(|contrib|>=0.5)") for c in cols)
        md.append(f"Lectura (cifras del csv): la principal tiene aceptacion {g('prereg', 'principal', T_PRE, 'aceptacion_por_rotacion'):.1e} por rotacion y, con M = {M_PRE}, el {100 * fth:.0f} % de los theta aporta alguna rotacion aceptada "
                  f"(minimo entre replicas {100 * g('prereg', 'principal', T_PRE, 'frac_theta_con_aceptada_minimo_replicas'):.0f} %); V3, {g('prereg', 'V3_solo_impacto', T_PRE, 'aceptacion_por_rotacion'):.1e} y "
                  f"{100 * g('prereg', 'V3_solo_impacto', T_PRE, 'frac_theta_con_aceptada'):.0f} %. La cobertura de la DH por tramos es {dhp:.2f} (principal) y {dh3:.2f} (V3) al 90 %, pero la banda del 90 % solo excluye el cero en "
                  f"{100 * exp_:.1f} % y {100 * ex3:.1f} % de las celdas con contribucion verdadera grande: las bandas cubren porque son anchas (conjunto identificado), no porque la DH discrimine el signo de la contribucion por tramos. "
                  f"El signo del impacto de los elementos no restringidos se recupera por la mediana en {sgp:.2f} (principal) y {sg3:.2f} (V3) de las replicas; con 7 variables y 86 observaciones no alcanza el 0,90 de las reglas. "
                  f"Fraccion de celdas con banda que excluye el cero con signo erroneo: {g('prereg', 'principal', T_PRE, 'DH_banda90_excluye_0_con_signo_ERRONEO_(|contrib|>=0.5)'):.3f} (principal), "
                  f"{g('prereg', 'V3_solo_impacto', T_PRE, 'DH_banda90_excluye_0_con_signo_ERRONEO_(|contrib|>=0.5)'):.3f} (V3). Ficticias exogenas estimadas (principal): COVID sobre e "
                  f"{g('prereg', 'principal', T_PRE, 'coef_COVID_sobre_e_estimado_(verdad_-2.0)'):+.2f} (verdad -2,0) y EPA {g('prereg', 'principal', T_PRE, 'coef_EPA_sobre_e_estimado_(verdad_1.5)'):+.2f} (verdad +1,5).\n")
    # ------------------------------------------------------------------ TVP
    md.append("## 3. TVP-VAR con volatilidad estocastica\n")
    md.append("DGP: VAR(2) de 3 variables, un coeficiente (primer retardo propio de la ecuacion 1) pasa de 0,4 a 0,8 a mitad de la muestra efectiva; volatilidad 0,5 constante. "
              "T = 120 con 30 observaciones de entrenamiento del prior (T efectivo = 88). Gibbs de 1200 iteraciones, 400 de calentamiento, adelgazado 4 (200 sorteos). "
              "kQ es la escala del prior de Q (Primiceri usa 0,01). Control = coeficiente constante de otra ecuacion. «Deteccion» = la banda del 90 % de (media del ultimo cuarto - media del primer cuarto) excluye 0 por arriba.\n")
    filas = []
    for e in ("ruptura_kQ0.10", "sin_ruptura_kQ0.10", "ruptura_kQ0.30", "sin_ruptura_kQ0.30", "ruptura_kQ0.01"):
        r_ = int(df[(df.herramienta == "TVP") & (df.escenario == e)]["replicas"].iloc[0])
        det = g("TVP", e, 120, "deteccion_cambio_(banda90_late-early>0)") if e.startswith("ruptura") else g("TVP", e, 120, "falsos_positivos_(banda90_late-early>0)")
        dif = f"{g('TVP', e, 120, 'cambio_estimado_medio_(verdad_0.4_en_cuartiles_extremos)'):.2f}" if e.startswith("ruptura") else "-"
        filas.append((e, r_, f"{g('TVP', e, 120, 'cobertura_68_coef_con_ruptura'):.3f}", f"{g('TVP', e, 120, 'cobertura_90_coef_con_ruptura'):.3f}", f"{g('TVP', e, 120, 'cobertura_90_coef_control_constante'):.3f}",
                      f"{det:.2f}", dif, f"{g('TVP', e, 120, 'RMSE_senda_coef_rupt'):.3f}", f"{g('TVP', e, 120, 'sigma_estimado_sobre_verdad_(0.5)'):.2f}"))
    md += tabla(["Escenario", "replicas", "cob. 68 % coef.", "cob. 90 % coef.", "cob. 90 % control", "deteccion / falsos positivos", "cambio estimado (verdad 0,4)", "RMSE senda", "sigma est./verdad"], filas)
    md.append(f"\nLectura (cifras del csv): deteccion con kQ = 0,01 / 0,10 / 0,30: {g('TVP', 'ruptura_kQ0.01', 120, 'deteccion_cambio_(banda90_late-early>0)'):.2f} / "
              f"{g('TVP', 'ruptura_kQ0.10', 120, 'deteccion_cambio_(banda90_late-early>0)'):.2f} / {g('TVP', 'ruptura_kQ0.30', 120, 'deteccion_cambio_(banda90_late-early>0)'):.2f}; "
              f"cobertura del 90 % del coeficiente con ruptura: {g('TVP', 'ruptura_kQ0.01', 120, 'cobertura_90_coef_con_ruptura'):.2f} / {g('TVP', 'ruptura_kQ0.10', 120, 'cobertura_90_coef_con_ruptura'):.2f} / "
              f"{g('TVP', 'ruptura_kQ0.30', 120, 'cobertura_90_coef_con_ruptura'):.2f}; falsos positivos sin ruptura (kQ 0,10 / 0,30): {g('TVP', 'sin_ruptura_kQ0.10', 120, 'falsos_positivos_(banda90_late-early>0)'):.2f} / "
              f"{g('TVP', 'sin_ruptura_kQ0.30', 120, 'falsos_positivos_(banda90_late-early>0)'):.2f}. No se recomienda para fechar o atribuir cambios de coeficientes con muestras de este tamano; "
              "como descripcion exploratoria de la volatilidad, la sigma estimada sobre la verdadera esta en la tabla.\n")
    md.append("### Alternativa: VAR por regimenes (prior comun, ruptura conocida), 2 regimenes\n")
    md.append("Misma DGP; coeficientes distintos por tramo con el mismo prior Minnesota (delta = 0; lambda comun por verosimilitud marginal). La fecha de ruptura se SUPONE conocida.\n")
    filas = []
    for e in ("ruptura", "sin_ruptura"):
        r_ = int(df[(df.herramienta == "regimenes") & (df.escenario == e)]["replicas"].iloc[0])
        det = g("regimenes", e, 120, "deteccion_cambio_(banda90_dif>0)") if e == "ruptura" else g("regimenes", e, 120, "falsos_positivos_(banda90_dif>0)")
        dif = f"{g('regimenes', e, 120, 'cambio_estimado_medio_(verdad_0.4)'):.2f}" if e == "ruptura" else "-"
        filas.append((e, r_, f"{g('regimenes', e, 120, 'cobertura_68_coef'):.3f}", f"{g('regimenes', e, 120, 'cobertura_90_coef'):.3f}", f"{det:.2f}", dif))
    md += tabla(["Escenario", "replicas", "cob. 68 %", "cob. 90 %", "deteccion / falsos positivos", "cambio estimado"], filas)
    # ------------------------------------------------------------------ regimenes 5
    md.append("\n### Alternativa: VAR por regimenes con los 5 tramos reales (H9)\n")
    md.append(f"DGP: VAR(2) de n = 4 variables, 5 tramos de {', '.join(str(x) for x in LONG_REG)} trimestres con huecos de transicion de {HUECOS_REG[0]} (tras el 1.o) y {HUECOS_REG[2]} (tras el 3.o) trimestres, "
              "que no entran como variable dependiente (`tramos` no contiguos). Parametro: primer retardo propio de la ecuacion 1: "
              f"{', '.join(str(x) for x in COEF_REG['cambios'])} en los tramos («cambios») o 0,4 constante («sin_cambio»). Ancho prior = ancho de la banda 90 % del coeficiente bajo el prior. "
              "Modos: `GLP` (lambda por verosimilitud marginal), `lam1` (lambda = 1), `plano_lam5` (lambda = 5, casi plano).\n")
    for esc0 in COEF_REG:
        for modo in REG_MODOS:
            esc = f"{esc0}|{modo}"
            filas = []
            for nm in NOM_REG:
                filas.append((nm, f"{g('regimenes5', esc, 88, f'cobertura_68_{nm}'):.2f}", f"{g('regimenes5', esc, 88, f'cobertura_90_{nm}'):.2f}", f"{g('regimenes5', esc, 88, f'sesgo_{nm}'):+.3f}",
                              f"{g('regimenes5', esc, 88, f'RMSE_media_posterior_{nm}'):.3f}", f"{g('regimenes5', esc, 88, f'ancho90_posterior_{nm}'):.3f}",
                              f"{g('regimenes5', esc, 88, f'ratio_ancho90_posterior_sobre_prior_{nm}'):.2f}"))
            md.append(f"**{esc.replace('|', ' / ')}** (lambda mediana {g('regimenes5', esc, 88, 'lambda_mediana'):.2f}; replicas {int(df[(df.herramienta == 'regimenes5') & (df.escenario == esc)]['replicas'].iloc[0])}):\n")
            md += tabla(["Tramo", "cob. 68 %", "cob. 90 %", "sesgo", "RMSE", "ancho 90 % posterior", "ancho posterior / prior"], filas)
            ms = df[(df.herramienta == "regimenes5") & (df.escenario == esc) & (df.metrica.str.startswith("deteccion_") | df.metrica.str.startswith("falsos_positivos"))]
            md.append("\n" + "; ".join(f"{r.metrica.replace('_', ' ')} = {r.valor:.2f}" for r in ms.itertuples()) + "\n")
    c4 = g("regimenes5", "cambios|GLP", 88, "cobertura_90_T4 (9)")
    r4 = g("regimenes5", "cambios|GLP", 88, "ratio_ancho90_posterior_sobre_prior_T4 (9)")
    md.append(f"Lectura: en el tramo de 9 trimestres la cobertura del 90 % es {c4:.2f} y el ancho de la posterior es {r4:.2f} veces el del prior (modo GLP, «cambios»); "
              f"regla de imprecision: ancho posterior/prior >= 0,75 -> tramo {'impreciso (posterior cercana al prior)' if r4 >= 0.75 else 'informado por los datos'}. "
              "Los demas tramos figuran en la tabla; la etiqueta global se deriva de las cobertura, la deteccion entre tramos contiguos y los falsos positivos.\n")
    md.append("\n## Limitaciones\n")
    md.append("- Un solo conjunto de DGP por herramienta; los resultados no se extrapolan a otras dinamicas.\n"
              "- BVAR: psi de la muestra completa (no pre-muestra); no se imponen hiperpriors (maximo de la densidad marginal pura).\n"
              "- Signos: cobertura de un conjunto identificado no es una propiedad frecuentista; pesos propios (ver arriba). El DGP pre-registrado es uno solo y cumple la tabla por construccion; "
              "la aceptacion real depende de la posterior de los datos reales.\n"
              "- La DH por tramos usa tramos del calendario simulado (14, 22, 24, 9, 14 trimestres); P1 (1995-2007) no existe con 7 variables.\n"
              "- TVP: sin truncamiento de estabilidad; prior de entrenamiento con 30 observaciones; ruptura unica; ESS de Gibbs no reportado.\n"
              "- Replicas pocas en TVP (8-30) y en la configuracion pre-registrada (30) y la cuadricula de M (5): los porcentajes tienen error de muestreo de varios puntos.\n")
    (OUT / "validacion.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    sig4 = {f"{e}|T{T}": g("signos", f"{e}|T{T}", T, "signo_impacto_recuperado_no_restringidas") for e, T in S4}
    pre = {c: {m: (g("prereg", c, T_PRE, m) if hay(df, "prereg", c, m) else None) for m in
               ("aceptacion_por_rotacion", "frac_theta_con_aceptada", "rotaciones_por_aceptada", "ESS_medio", "signo_impacto_recuperado_no_restringidas", "DH_cobertura_68_total",
                "DH_cobertura_90_total", "DH_banda90_excluye_0_con_signo_ERRONEO_(|contrib|>=0.5)", "descomposicion_historica_error_max_con_exogenas")} for c in cols}
    for c in cols:
        pre[c]["DH_cobertura_90_por_tramo"] = {nom: (g("prereg", c, T_PRE, f"DH_cobertura_90_{nom}") if hay(df, "prereg", c, f"DH_cobertura_90_{nom}") else None) for nom in TRAMOS_NOM}
    res = dict(
        rama="r8/F3/var", pregunta="¿Son aptas, con datos simulados, las herramientas BVAR-GLP (con exogenas y delta), signos/ceros (RWZ, configuracion pre-registrada), TVP-VAR-SV y VAR por regimenes (5 tramos)?",
        capa="C4", datos="Simulados (DGP del Monte Carlo; sin datos reales ni sellados)",
        N={"BVAR": int(df[(df.herramienta == 'BVAR') & (df.metrica == 'cobertura_90')]['replicas'].iloc[0]), "signos_4var": "100 (T=120), 80 (T=60), 80 (ceros)",
           "prereg": {c: int(df[(df.herramienta == 'prereg') & (df.escenario == c) & (df.metrica == 'aceptacion_por_rotacion')]['replicas'].iloc[0]) for c in cols},
           "TVP": "30/12/12/10/8 segun escenario", "regimenes": 300, "regimenes5": int(df[df.herramienta == 'regimenes5']['replicas'].iloc[0])},
        metodo="Monte Carlo (SEED 20261010): cobertura de bandas 68/90 de IRF, sesgo absoluto y firmado relativo, recuperacion del signo, ceros exactos, identidad de la descomposicion historica con exogenas, "
               "cobertura de la DH por tramos, viabilidad del muestreo (fraccion de theta con aceptada, ESS), deteccion de cambio de coeficiente",
        estimacion={"etiquetas": E,
                    "reglas": UMBRALES,
                    "BVAR_cobertura90": {f"{e}|{m}|T{T}": g("BVAR", f"{e}|{m}", T, "cobertura_90") for e in BVAR_ESC for m in ("GLP", "GLP_delta1", "plano_lam100") for T in (120, 60)},
                    "BVAR_sesgo_rel": {f"{e}|{m}|T{T}": g("BVAR", f"{e}|{m}", T, "sesgo_rel_IRF_h1-12") for e in BVAR_ESC for m in ("GLP", "GLP_delta1", "plano_lam100") for T in (120, 60)},
                    "BVAR_atenuacion_firmada_rel": {f"{e}|{m}|T{T}": g("BVAR", f"{e}|{m}", T, "atenuacion_firmada_rel_h1-12") for e in BVAR_ESC for m in ("GLP", "GLP_delta1", "plano_lam100") for T in (120, 60)},
                    "BVAR_tasas_delta_mixto_cobertura90": {f"T{T}": g("BVAR", "tasas|GLP_delta_mixto", T, "cobertura_90") for T in (120, 60)},
                    "signos_4var_signo_impacto": sig4,
                    "signos_prereg": pre,
                    "signos_prereg_M": M_PRE,
                    "TVP_deteccion": {e: g("TVP", e, 120, "deteccion_cambio_(banda90_late-early>0)") for e in ("ruptura_kQ0.10", "ruptura_kQ0.30", "ruptura_kQ0.01")},
                    "regimenes_deteccion_2reg": g("regimenes", "ruptura", 120, "deteccion_cambio_(banda90_dif>0)"),
                    "regimenes5_GLP_cambios": {nm: dict(cob90=g("regimenes5", "cambios|GLP", 88, f"cobertura_90_{nm}"), ratio_ancho=g("regimenes5", "cambios|GLP", 88, f"ratio_ancho90_posterior_sobre_prior_{nm}"),
                                                        rmse=g("regimenes5", "cambios|GLP", 88, f"RMSE_media_posterior_{nm}")) for nm in NOM_REG}},
        ic95=None, p_ajustado=None, nivel_evidencia="DESCRIPTIVO (validacion metodologica sobre datos simulados; sin lenguaje causal)",
        diagnosticos={"logml_vs_fuerza_bruta_error_abs": {k: g("BVAR", k, "", "error_abs_logml") for k in ("logml_vs_cuadratura_n1", "logml_vs_cadena_predictiva_n3_dummies")},
                      "ceros_max_abs": g("signos", "signos+ceros|T120", 120, "restricciones_cumplidas_max_abs_cero"),
                      "descomposicion_historica_error_max": max(g("signos", f"{e}|T{T}", T, "descomposicion_historica_error_max") for e, T in S4),
                      "tiempo_computo_s": round(seg), "replicas_por_escenario": {f"{r.herramienta}|{r.escenario}|{r['T']}": int(r.replicas) for _, r in reps.iterrows()}},
        fuera_muestra={"modelo": None, "rmse": None, "dm_vs_ar4": None},
        notas="Herramientas en src/v8/herramientas/{bvar,signos,tvp}.py. Referencias de metodo NO VERIFICADAS (sin Crossref). Pesos de importancia propios (no se afirma igualdad con ARW). "
              "Correcciones de la revision F3: H4 (exog), H10 (delta), H2 (muestreo con rotaciones fijas), H1/H16 (configuracion pre-registrada y V3), H9 (5 tramos), H12 (atenuacion firmada). "
              "La eleccion entre la configuracion principal y V3, M y el numero de sorteos de theta queda al orquestador.")
    (OUT / "resultado.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=float) + "\n", encoding="utf-8")


M_PRE = 3000


def main():
    if RAPIDO:
        R_reg, R_reg5 = 6, 6
        R_bvar, R_sg, R_tvp, it, bu, Nin = 6, {("signos", 120): 3, ("signos", 60): 3, ("signos+ceros", 120): 3}, {"ruptura_kQ0.10": 2, "sin_ruptura_kQ0.10": 1, "ruptura_kQ0.30": 1, "sin_ruptura_kQ0.30": 1, "ruptura_kQ0.01": 1}, 300, 100, 3000
        R_pre, D_pre, R_M, D_M, Ms = 1, 200, 1, 100, (500, 3000)
    else:
        R_reg, R_reg5 = 300, 300
        R_bvar = 500
        R_sg = {("signos", 120): 100, ("signos", 60): 80, ("signos+ceros", 120): 80}
        R_tvp = {"ruptura_kQ0.10": 30, "sin_ruptura_kQ0.10": 12, "ruptura_kQ0.30": 12, "sin_ruptura_kQ0.30": 10, "ruptura_kQ0.01": 8}
        it, bu, Nin = 1200, 400, 100000
        R_pre, D_pre, R_M, D_M, Ms = 30, 600, 5, 200, (500, 1500, 3000, 10000)
    if "--solo-informe" in sys.argv:
        tj = json.loads((OUT / "tiempos.json").read_text()) if (OUT / "tiempos.json").exists() else {}
        informe(pd.read_csv(OUT / "montecarlo.csv", keep_default_na=False, na_values=[]), float(sys.argv[sys.argv.index("--solo-informe") + 1]), {k: tuple(v) for k, v in tj.items()})
        return None
    ml_fuerza_bruta()
    mc_bvar(R_bvar)
    mc_signos(R_sg)
    invariancia_orden(Nin)
    mc_prereg(R_pre, D_pre, M_PRE, False)
    mc_prereg(R_pre, D_pre, M_PRE, True)
    cuadricula_M(R_M, D_M, Ms)
    mc_tvp(R_tvp, it, bu)
    mc_regimenes(R_reg)
    mc_regimenes5(R_reg5)
    df = pd.DataFrame(ROWS)
    OUT.mkdir(parents=True, exist_ok=True)
    seg = time.time() - T0
    df.to_csv(OUT / "montecarlo.csv", index=False, float_format="%.6g")
    (OUT / "tiempos.json").write_text(json.dumps({k: list(v) for k, v in TIEMPOS.items()}, indent=1) + "\n", encoding="utf-8")
    informe(df, seg, TIEMPOS)
    print(f"tiempo total {seg:.0f} s", flush=True)
    return df


if __name__ == "__main__":
    main()
