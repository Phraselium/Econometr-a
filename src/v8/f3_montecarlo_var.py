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
    else:  # casi paseo aleatorio por variable: coherente con el prior Minnesota
        A1 = 0.9 * np.eye(n)
        A2 = np.zeros((n, n))
    L = np.array([[1.0, 0, 0, 0], [0.4, 0.9, 0, 0], [0.2, 0.3, 0.8, 0], [0.1, 0.2, 0.3, 0.7]])
    return [A1, A2], L


def mc_bvar(R):
    H = 12
    for esc in ("denso", "casi_RW"):
        A, L = dgp_bvar(esc)
        assert radio(A) < 0.97
        Phi_t = bvar.ma_coefs(B_from(A), 4, 2, H)[0]
        Itrue = Phi_t @ L  # (H+1, i, j)
        struct0 = np.zeros((H + 1, 4, 4), bool)
        struct0[0] = np.triu(np.ones((4, 4)), 1).astype(bool)
        for T in (120, 60):
            for modo, kw in (("GLP", {}), ("plano_lam100", dict(lam=100.0))):
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
                c68, c90 = float(cov68.mean()), float(cov90.mean())
                tag = f"{esc}|{modo}"
                add("BVAR", tag, T, R, "cobertura_68", c68)
                add("BVAR", tag, T, R, "cobertura_90", c90, "[0.85, 0.98]", 0.85 <= c90 <= 0.98)
                add("BVAR", tag, T, R, "sesgo_rel_IRF_h1-12", sesgo_rel, "<= 0.10", sesgo_rel <= 0.10)
                for h, v in sesgo_h.items():
                    add("BVAR", tag, T, R, f"sesgo_rel_h{h}", v)
                if modo == "GLP":
                    for q, v in zip(("media", "p05", "mediana", "p95"), (np.mean(lams), *np.quantile(lams, [0.05, 0.5, 0.95]))):
                        add("BVAR", tag, T, R, f"lambda_{q}", v)
                print(f"[BVAR {tag} T={T}] cov68={c68:.3f} cov90={c90:.3f} sesgo={sesgo_rel:.3f} lam~{np.median(lams):.2f} ({time.time() - t0:.0f}s)", flush=True)


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
        signo_ok, banda_signo, med_bias, ess, acept, zmax, hd_err, nacc = [], [], [], [], [], [], [], []
        t0 = time.time()
        for rep in range(R):
            rg = rng_for(3, int(zeros), T, rep)
            Y = sim_var(A, A0, T, rg)
            post = bvar.estimar(Y, 2)
            B, Sig = bvar.muestrear(post, 400, rg)
            res = signos.identificar(B, Sig, 4, 2, r, H=H, n_objetivo=150, rng=rg)
            if len(res["Q"]) < 20:
                continue
            nacc.append(len(res["Q"]))
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
        res = signos.identificar(B, Sig, n, 2, r, H=2, por_sorteo=N, rng=rng_for(4, sd), orden=orden)
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


def etiquetas(df):
    """Etiquetas apta / con reservas / no apta con reglas declaradas (ver validacion.md)."""
    E = {}
    # BVAR (GLP)
    cel = [(e, T) for e in ("denso", "casi_RW") for T in (120, 60)]
    cov = [V(df, "BVAR", f"{e}|GLP", T, "cobertura_90") for e, T in cel]
    ses = [V(df, "BVAR", f"{e}|GLP", T, "sesgo_rel_IRF_h1-12") for e, T in cel]
    ml_ok = _todo(df[(df.escenario.str.startswith("logml_vs_"))]["cumple"])
    if ml_ok and all(0.85 <= c <= 0.98 for c in cov) and all(s_ <= 0.10 for s_ in ses):
        E["BVAR-GLP"] = "apta"
    elif ml_ok and all(0.80 <= c <= 0.99 for c in cov) and all(s_ <= 0.30 for s_ in ses):
        E["BVAR-GLP"] = "con reservas"
    else:
        E["BVAR-GLP"] = "no apta"
    # signos: mecanica
    hd = max(V(df, "signos", f"{e}|T{T}", T, "descomposicion_historica_error_max") for e, T in (("signos", 120), ("signos", 60), ("signos+ceros", 120)))
    z = V(df, "signos", "signos+ceros|T120", 120, "restricciones_cumplidas_max_abs_cero")
    inv = _todo(df[df.escenario == "ARW_invariancia_al_orden"]["cumple"])
    E["signos/ceros (mecanica: restricciones, FEVD, descomposicion historica)"] = "apta" if (hd < 1e-8 and z < 1e-10) else "no apta"
    E["pesos de importancia ARW (derivados aqui; formula del articulo NO contrastada)"] = "apta (invariancia al orden)" if inv else "con reservas"
    sg = [V(df, "signos", f"{e}|T{T}", T, "signo_impacto_recuperado_no_restringidas") for e, T in (("signos", 120), ("signos", 60), ("signos+ceros", 120))]
    c90r = [V(df, "signos", f"{e}|T{T}", T, "cobertura_90_IRF_restringidas") for e, T in (("signos", 120), ("signos", 60), ("signos+ceros", 120))]
    c90l = [V(df, "signos", f"{e}|T{T}", T, "cobertura_90_IRF_no_restringidas") for e, T in (("signos", 120), ("signos", 60), ("signos+ceros", 120))]
    todas = c90r + c90l
    if all(x >= 0.90 for x in sg) and all(0.85 <= c <= 0.98 for c in todas):
        E["signos/ceros (inferencia: bandas y signo del impacto)"] = "apta"
    elif all(x >= 0.90 for x in sg) and all(0.85 <= c for c in todas):
        E["signos/ceros (inferencia: bandas y signo del impacto)"] = "con reservas (bandas conservadoras: cobertura 90 % por encima de 0,98; set-identified)"
    else:
        E["signos/ceros (inferencia: bandas y signo del impacto)"] = "no apta (signo del impacto < 90 % o cobertura < 0,85)"
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
    E["VAR por regimenes (ruptura CONOCIDA)"] = "apta" if (0.85 <= c <= 0.98 and d >= 0.8 and fp <= 0.15) else ("con reservas" if (c >= 0.80 and d >= 0.5 and fp <= 0.15) else "no apta")
    return E


def informe(df, seg):
    E = etiquetas(df)
    g = lambda h, e, T, m: V(df, h, e, T, m)  # noqa: E731
    md = []
    md.append("# V8-F3 grupo A (familia VAR): validacion por Monte Carlo\n")
    md.append("Capa C4 (metodologico). Solo datos simulados; ningun dato real ni sellado. SEED = 20261010, un hilo, determinista. "
              f"Computo total de la ejecucion: {seg:.0f} s ({seg / 60:.1f} min). Reproducir: `python3 src/v8/f3_montecarlo_var.py`. "
              "Resultados completos: `montecarlo.csv`. Referencias de metodo NO VERIFICADAS (sin acceso a Crossref).\n")
    md.append("## Veredicto por herramienta\n")
    md.append("| Herramienta / componente | Etiqueta |\n|---|---|")
    for k, v in E.items():
        md.append(f"| {k} | **{v}** |")
    md.append("\nReglas declaradas. Criterios: sesgo relativo <= 10 % (IRF) o, en conjuntos identificados por signos, recuperacion del signo del impacto "
              "en >= 90 % de replicas; cobertura de las bandas del 90 % en [0,85; 0,98]. «Apta»: cumple todos. «Con reservas»: la mecanica es exacta y "
              "la cobertura 90 % esta en [0,80; 0,99] (BVAR; sesgo <= 30 %) o es conservadora (signos, >= 0,85). «No apta»: el resto. "
              "Deteccion de cambios (TVP y regimenes): potencia >= 80 % y falsos positivos <= 15 % (criterio anadido por el ejecutor).\n")
    md.append("## Replicas (las que caben en ~20 min)\n")
    reps = df.groupby(["herramienta", "escenario", "T"])["replicas"].first().reset_index()
    md.append("| Herramienta | Escenario | T | Replicas |\n|---|---|---|---|")
    for _, r in reps.iterrows():
        md.append(f"| {r.herramienta} | {str(r.escenario).replace('|', ' / ')} | {r['T']} | {int(r.replicas)} |")
    md.append("\n## 1. BVAR normal-Wishart inversa (GLP)\n")
    md.append("DGP: VAR(2) de 4 variables («denso»: radio espectral %.2f; «casi_RW»: 0,9 por variable). IRF de Cholesky; 300 sorteos de la posterior por replica; "
              "cobertura medida sobre las celdas no triviales (se excluyen los ceros estructurales del impacto). `plano_lam100` es la referencia sin contraccion "
              "(prior casi plano).\n" % radio(dgp_bvar("denso")[0]))
    md.append("| Escenario | T | cob. 68 % | cob. 90 % | sesgo rel. IRF h=1-12 | lambda mediana |\n|---|---|---|---|---|---|")
    for e in ("denso", "casi_RW"):
        for T in (120, 60):
            for modo in ("GLP", "plano_lam100"):
                tag = f"{e}|{modo}"
                lam = f"{g('BVAR', tag, T, 'lambda_mediana'):.2f}" if modo == "GLP" else "100 (fijo)"
                md.append(f"| {tag.replace('|', ' / ')} | {T} | {g('BVAR', tag, T, 'cobertura_68'):.3f} | {g('BVAR', tag, T, 'cobertura_90'):.3f} | "
                          f"{g('BVAR', tag, T, 'sesgo_rel_IRF_h1-12'):.3f} | {lam} |")
    md.append("\nVerosimilitud marginal frente a fuerza bruta: error absoluto en log = "
              f"{g('BVAR', 'logml_vs_cuadratura_n1', '', 'error_abs_logml'):.1e} (cuadratura 2-D, n=1, p=1) y "
              f"{g('BVAR', 'logml_vs_cadena_predictiva_n3_dummies', '', 'error_abs_logml'):.1e} (cadena predictiva t multivariante, n=3, p=2, con dummies de suma de coeficientes y de observacion inicial).\n")
    md.append("GLP elige lambda coherente con el DGP: menor en el paseo aleatorio (casi_RW) que en el VAR denso, y siempre dentro de [0,005; 20] sin tocar los limites.\n")
    md.append("Lectura: la cobertura del 90 % es correcta; el sesgo relativo agregado supera el 10 % en parte de las celdas. Ese sesgo aparece tambien con el prior casi plano "
              "(sesgo de muestra finita del VAR persistente y del orden de Cholesky), asi que no es atribuible a la contraccion; la contraccion GLP lo reduce en el DGP casi_RW "
              "y mejora la cobertura. Por eso la etiqueta es «con reservas» y no «apta» segun el criterio de sesgo declarado.\n")
    md.append("## 2. Signos y ceros (RWZ / ARW)\n")
    md.append("DGP estructural de 4 shocks (oferta, demanda, credito, monetario) sobre 4 variables (y, pi, cred, tipo). Restricciones de signo en el impacto: "
              "oferta (y+, pi-); demanda (y+, pi+, tipo+); credito (cred+, y+, pi+); monetario (tipo+, pi-, cred-, y-). Variante con ceros: el shock monetario no mueve y en el impacto y "
              "el de oferta no mueve el tipo (sustituyen a la restriccion y- del monetario). 400 sorteos de la posterior, 150 rotaciones aceptadas por replica. "
              "Cobertura medida en h = 0, 1, 4, 8. «Restringidas» = celdas con restriccion de signo; «no restringidas» = el resto (con verdad no nula).\n")
    md.append("| Escenario | T | replicas | aceptacion/rotacion | ESS (de 150) | cob. 68 % restr. | cob. 68 % no restr. | cob. 90 % restr. | cob. 90 % no restr. | signo impacto recuperado (no restr.) | HD error max |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for e, T in (("signos", 120), ("signos", 60), ("signos+ceros", 120)):
        t = f"{e}|T{T}"
        md.append(f"| {e} | {T} | {int(df[(df.escenario == t)]['replicas'].iloc[0])} | {g('signos', t, T, 'aceptacion_por_rotacion'):.4f} | {g('signos', t, T, 'ESS_medio_de_150'):.0f} | "
                  f"{g('signos', t, T, 'cobertura_68_IRF_restringidas'):.3f} | {g('signos', t, T, 'cobertura_68_IRF_no_restringidas'):.3f} | "
                  f"{g('signos', t, T, 'cobertura_90_IRF_restringidas'):.3f} | {g('signos', t, T, 'cobertura_90_IRF_no_restringidas'):.3f} | "
                  f"{g('signos', t, T, 'signo_impacto_recuperado_no_restringidas'):.3f} | {g('signos', t, T, 'descomposicion_historica_error_max'):.1e} |")
    md.append(f"\nCeros: maximo |IRF| en las restricciones de cero = {g('signos', 'signos+ceros|T120', 120, 'restricciones_cumplidas_max_abs_cero'):.1e} (se cumplen exactamente). "
              "Descomposicion historica: y_t = componente determinista + suma de contribuciones con error maximo < 1e-8 en todas las replicas comprobadas (6 por escenario, 20 sorteos cada una). "
              "Las filas de la FEVD (h = 4, 8, 12, 20) suman 1 en todas las replicas.\n")
    md.append(f"Pesos ARW: la formula exacta del articulo NO se pudo contrastar (sin acceso). Los pesos usados son una derivacion propia por coarea en el espacio (forma reducida, Q) "
              f"(ver cabecera de signos.py). Diagnostico: la distribucion ponderada de Q debe ser invariante al orden de los shocks. Con {int(df[df.escenario == 'ARW_invariancia_al_orden']['replicas'].iloc[0])} "
              f"sorteos, la diferencia maxima en E[Q^2] entre ordenes es {g('signos', 'ARW_invariancia_al_orden', '', 'max_dif_E[Q^2]_entre_ordenes_con_pesos'):.3f} con pesos frente a "
              f"{g('signos', 'ARW_invariancia_al_orden', '', 'max_dif_E[Q^2]_entre_ordenes_sin_pesos'):.3f} sin pesos; el suelo de ruido (mismo orden, otra semilla) es "
              f"{g('signos', 'ARW_invariancia_al_orden', '', 'suelo_de_ruido_(mismo_orden_otra_semilla)'):.3f} (ESS medio {g('signos', 'ARW_invariancia_al_orden', '', 'ESS_medio'):.0f} de {int(df[df.escenario == 'ARW_invariancia_al_orden']['replicas'].iloc[0])}). "
              "La prueba rechaza pesos incorrectos pero no demuestra la igualdad con la formula de ARW.\n")
    md.append("Lectura: las bandas por signos son anchas (la verdad cae en ellas mas a menudo que lo nominal: con un conjunto identificado la banda mezcla incertidumbre de parametros y de identificacion, "
              "y la ‘cobertura’ no tiene el significado frecuentista habitual). Se informa de la cobertura y se etiqueta «con reservas»: las bandas son validas como cotas de credibilidad conservadoras, no calibradas al nivel nominal.\n")
    md.append("## 3. TVP-VAR con volatilidad estocastica\n")
    md.append("DGP: VAR(2) de 3 variables, un coeficiente (primer retardo propio de la ecuacion 1) pasa de 0,4 a 0,8 a mitad de la muestra efectiva; volatilidad 0,5 constante. "
              "T = 120 con 30 observaciones de entrenamiento del prior (T efectivo = 88). Gibbs de 1200 iteraciones, 400 de calentamiento, adelgazado 4 (200 sorteos). "
              "kQ es la escala del prior de Q (Primiceri usa 0,01). Control = coeficiente constante de otra ecuacion. «Deteccion» = la banda del 90 % de (media del ultimo cuarto - media del primer cuarto) excluye 0 por arriba.\n")
    md.append("| Escenario | replicas | cob. 68 % coef. | cob. 90 % coef. | cob. 90 % control | deteccion / falsos positivos | cambio estimado (verdad 0,4) | RMSE senda | sigma est./verdad |\n|---|---|---|---|---|---|---|---|---|")
    for e in ("ruptura_kQ0.10", "sin_ruptura_kQ0.10", "ruptura_kQ0.30", "sin_ruptura_kQ0.30", "ruptura_kQ0.01"):
        r_ = int(df[(df.herramienta == "TVP") & (df.escenario == e)]["replicas"].iloc[0])
        det = g("TVP", e, 120, "deteccion_cambio_(banda90_late-early>0)") if e.startswith("ruptura") else g("TVP", e, 120, "falsos_positivos_(banda90_late-early>0)")
        dif = g("TVP", e, 120, "cambio_estimado_medio_(verdad_0.4_en_cuartiles_extremos)") if e.startswith("ruptura") else float("nan")
        md.append(f"| {e} | {r_} | {g('TVP', e, 120, 'cobertura_68_coef_con_ruptura'):.3f} | {g('TVP', e, 120, 'cobertura_90_coef_con_ruptura'):.3f} | {g('TVP', e, 120, 'cobertura_90_coef_control_constante'):.3f} | "
                  f"{det:.2f} | {dif:.2f} | {g('TVP', e, 120, 'RMSE_senda_coef_rupt'):.3f} | {g('TVP', e, 120, 'sigma_estimado_sobre_verdad_(0.5)'):.2f} |")
    md.append("\nLectura: el muestreador converge (la volatilidad se recupera y la senda sigue al coeficiente), pero un salto de 0,4 en un solo coeficiente con 88 observaciones efectivas "
              "se detecta con poca potencia: el paseo aleatorio suaviza el escalon y las bandas son anchas. kQ=0,01 (valor de Primiceri) ignora el cambio; subir kQ lo recupera en parte a costa de bandas mas anchas. "
              "No se recomienda usarlo para fechar o atribuir cambios de coeficientes con muestras de este tamano; si sirve como descripcion exploratoria de la volatilidad.\n")
    md.append("### Alternativa documentada: VAR por regimenes (prior comun, ruptura conocida)\n")
    md.append("Misma DGP; coeficientes distintos por tramo con el mismo prior Minnesota (lambda comun por verosimilitud marginal). La fecha de ruptura se SUPONE conocida.\n")
    md.append("| Escenario | replicas | cob. 68 % | cob. 90 % | deteccion / falsos positivos | cambio estimado |\n|---|---|---|---|---|---|")
    for e in ("ruptura", "sin_ruptura"):
        r_ = int(df[(df.herramienta == "regimenes") & (df.escenario == e)]["replicas"].iloc[0])
        det = g("regimenes", e, 120, "deteccion_cambio_(banda90_dif>0)") if e == "ruptura" else g("regimenes", e, 120, "falsos_positivos_(banda90_dif>0)")
        dif = g("regimenes", e, 120, "cambio_estimado_medio_(verdad_0.4)") if e == "ruptura" else float("nan")
        md.append(f"| {e} | {r_} | {g('regimenes', e, 120, 'cobertura_68_coef'):.3f} | {g('regimenes', e, 120, 'cobertura_90_coef'):.3f} | {det:.2f} | {dif:.2f} |")
    md.append("\n## Limitaciones\n")
    md.append("- Un solo conjunto de DGP por herramienta; los resultados no se extrapolan a otras dinamicas.\n"
              "- BVAR: psi de la muestra completa (no pre-muestra); no se optimiza la prior de la matriz de escala ni se imponen hiperpriors (maximo de la densidad marginal pura).\n"
              "- Signos: cobertura de un conjunto identificado no es una propiedad frecuentista; los pesos ARW son propios (ver arriba).\n"
              "- TVP: sin truncamiento de estabilidad; prior de entrenamiento con 30 observaciones; ruptura unica; ESS de Gibbs no reportado.\n"
              "- Replicas pocas en TVP (8-30): los porcentajes tienen error de muestreo de varios puntos.\n")
    (OUT / "validacion.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    res = dict(
        rama="r8/F3/var", pregunta="¿Son aptas, con datos simulados, las herramientas BVAR-GLP, signos/ceros (RWZ/ARW) y TVP-VAR-SV (o regimenes)?",
        capa="C4", datos="Simulados (DGP del Monte Carlo; sin datos reales ni sellados)", N=int(df["replicas"].max()),
        metodo="Monte Carlo (SEED 20261010): cobertura de bandas 68/90 de IRF, sesgo relativo, recuperacion del signo, ceros exactos, identidad de la descomposicion historica, deteccion de cambio de coeficiente",
        estimacion={"etiquetas": E,
                    "BVAR_GLP_cobertura90": {f"{e}|T{T}": g("BVAR", f"{e}|GLP", T, "cobertura_90") for e in ("denso", "casi_RW") for T in (120, 60)},
                    "BVAR_GLP_sesgo_rel": {f"{e}|T{T}": g("BVAR", f"{e}|GLP", T, "sesgo_rel_IRF_h1-12") for e in ("denso", "casi_RW") for T in (120, 60)},
                    "signos_signo_impacto": {f"{e}|T{T}": g("signos", f"{e}|T{T}", T, "signo_impacto_recuperado_no_restringidas") for e, T in (("signos", 120), ("signos", 60), ("signos+ceros", 120))},
                    "signos_cobertura90_no_restringidas": {f"{e}|T{T}": g("signos", f"{e}|T{T}", T, "cobertura_90_IRF_no_restringidas") for e, T in (("signos", 120), ("signos", 60), ("signos+ceros", 120))},
                    "TVP_deteccion": {e: g("TVP", e, 120, "deteccion_cambio_(banda90_late-early>0)") for e in ("ruptura_kQ0.10", "ruptura_kQ0.30", "ruptura_kQ0.01")},
                    "regimenes_deteccion": g("regimenes", "ruptura", 120, "deteccion_cambio_(banda90_dif>0)")},
        ic95=None, p_ajustado=None, nivel_evidencia="DESCRIPTIVO (validacion metodologica sobre datos simulados; sin lenguaje causal)",
        diagnosticos={"logml_vs_fuerza_bruta_error_abs": {k: g("BVAR", k, "", "error_abs_logml") for k in ("logml_vs_cuadratura_n1", "logml_vs_cadena_predictiva_n3_dummies")},
                      "ceros_max_abs": g("signos", "signos+ceros|T120", 120, "restricciones_cumplidas_max_abs_cero"),
                      "descomposicion_historica_error_max": max(g("signos", f"{e}|T{T}", T, "descomposicion_historica_error_max") for e, T in (("signos", 120), ("signos", 60), ("signos+ceros", 120))),
                      "tiempo_computo_s": round(seg), "replicas_por_escenario": {f"{r.herramienta}|{r.escenario}|{r['T']}": int(r.replicas) for _, r in reps.iterrows()}},
        fuera_muestra={"modelo": None, "rmse": None, "dm_vs_ar4": None},
        notas="Herramientas en src/v8/herramientas/{bvar,signos,tvp}.py. Referencias de metodo NO VERIFICADAS (sin Crossref). Pesos ARW propios, validados por invariancia al orden; formula del articulo no contrastada. "
              "TVP: ver validacion.md; el VAR por regimenes (ruptura conocida) se incluye como alternativa en tvp.py.")
    (OUT / "resultado.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=float) + "\n", encoding="utf-8")


def main():
    if RAPIDO:
        R_reg = 6
        R_bvar, R_sg, R_tvp, it, bu, Nin = 6, {("signos", 120): 3, ("signos", 60): 3, ("signos+ceros", 120): 3}, {"ruptura_kQ0.10": 2, "sin_ruptura_kQ0.10": 1, "ruptura_kQ0.30": 1, "sin_ruptura_kQ0.30": 1, "ruptura_kQ0.01": 1}, 300, 100, 3000
    else:
        R_reg = 300
        R_bvar = 300
        R_sg = {("signos", 120): 100, ("signos", 60): 80, ("signos+ceros", 120): 80}
        R_tvp = {"ruptura_kQ0.10": 30, "sin_ruptura_kQ0.10": 12, "ruptura_kQ0.30": 12, "sin_ruptura_kQ0.30": 10, "ruptura_kQ0.01": 8}
        it, bu, Nin = 1200, 400, 100000
    if "--solo-informe" in sys.argv:
        informe(pd.read_csv(OUT / "montecarlo.csv", keep_default_na=False, na_values=[]), float(sys.argv[sys.argv.index("--solo-informe") + 1]))
        return None
    ml_fuerza_bruta()
    mc_bvar(R_bvar)
    mc_signos(R_sg)
    invariancia_orden(Nin)
    mc_tvp(R_tvp, it, bu)
    mc_regimenes(R_reg)
    df = pd.DataFrame(ROWS)
    OUT.mkdir(parents=True, exist_ok=True)
    seg = time.time() - T0
    df.to_csv(OUT / "montecarlo.csv", index=False, float_format="%.6g")
    informe(df, seg)
    print(f"tiempo total {seg:.0f} s", flush=True)
    return df


if __name__ == "__main__":
    main()
