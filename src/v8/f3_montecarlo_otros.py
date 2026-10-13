"""V8-F3 grupo B: validacion por Monte Carlo (SOLO datos simulados) de src/v8/herramientas/{regimenes,dfm,lp,dominancia,
permutacion,shap_grupos,multiverso}. SEED=20261010, un hilo, determinista. Version corregida tras docs/v8/revision_F3.md
(H5-H8, H13-H15, H17, H18): celdas con T ~ 90-126 (uso previsto), persistencia alta, configuraciones alternativas de
bootstrap/EE y etiquetas derivadas por reglas explicitas (REGLAS), no literales.

Uso:  python3 src/v8/f3_montecarlo_otros.py --bloque <nombre>   (escribe $F3_OUT/_parcial_<nombre>.csv)
      python3 src/v8/f3_montecarlo_otros.py --merge             (une parciales; escribe montecarlo.csv, validacion.md y resultado.json)
      python3 src/v8/f3_montecarlo_otros.py --rapido            (humo: R minimos, salida en $F3_OUT; no sustituye a la validacion)
Salida: variable de entorno F3_OUT (por defecto output/v8/F3/otros).
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
import time
import warnings
from pathlib import Path

for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np
import pandas as pd
from scipy.signal import lfilter

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
from src.v8.herramientas import dfm, dominancia, lp, permutacion, regimenes, shap_grupos  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
OUT = Path(os.environ.get("F3_OUT", ROOT / "output" / "v8" / "F3" / "otros"))
FILAS: list = []
RAPIDO = False

# ----------------------------------------------------------------------------- reglas de etiquetado (H15)
# Definidas por el ejecutor en la primera pasada de F3 tras ver las cifras (no pre-registradas): se documentan en
# validacion.md. apta = cumple todas las filas principales; con reservas = todas dentro de la banda laxa; no apta = alguna fuera.
REGLAS = {
    "tamano": ("[0,02; 0,10]", "<= 0,15"),
    "cobertura": ("[0,90; 0,98]", "[0,80; 0,99]"),
    "cobertura_inf": ("[0,90; 1] (solo cota inferior: conjuntos AR conservadores por construcción con instrumento débil)", "[0,80; 1]"),
    "potencia": (">= 0,80", ">= 0,50"),
    "acierto": (">= umbral de la fila", ">= 0,50"),
    "error": ("< umbral de la fila", "< 1,5 x umbral de la fila"),
}
TIPOS_VALIDEZ = ("tamano", "cobertura", "cobertura_inf", "acierto", "error")


def evaluar(tipo, v, umbral):
    """(objetivo, cumple, laxo) de una cifra segun REGLAS."""
    if tipo == "tamano":
        return REGLAS[tipo][0], bool(0.02 <= v <= 0.10), bool(v <= 0.15)
    if tipo == "cobertura":
        return REGLAS[tipo][0], bool(0.90 <= v <= 0.98), bool(0.80 <= v <= 0.99)
    if tipo == "cobertura_inf":
        return REGLAS[tipo][0], bool(v >= 0.90), bool(v >= 0.80)
    if tipo == "potencia":
        return REGLAS[tipo][0], bool(v >= 0.80), bool(v >= 0.50)
    if tipo == "acierto":
        return f">= {umbral}", bool(v >= umbral), bool(v >= 0.50)
    if tipo == "error":
        return f"< {umbral}", bool(abs(v) < umbral), bool(abs(v) < 1.5 * umbral)
    return "informativo", None, None


def reg(herr, config, esc, metrica, valor, tipo, reps, B="", n="", nota="", umbral=None, rol="principal"):
    obj, ok, laxo = evaluar(tipo, float(valor), umbral)
    FILAS.append({"herramienta": herr, "config": config, "escenario": esc, "metrica": metrica, "tipo": tipo, "rol": rol,
                  "valor": float(valor), "objetivo": obj, "cumple": ok, "laxo": laxo, "reps": reps, "B": B, "n": n, "nota": nota})


def rng_(*k):
    return np.random.default_rng([SEED, *k])


def nR(R, minimo=3):
    return max(minimo, R // 25) if RAPIDO else R


def ar1(g, n, rho, size=None, burn=100):
    """AR(1) de varianza marginal 1 (n x size)."""
    shape = (n + burn,) if size is None else (n + burn, size)
    x = lfilter([1.0], [1.0, -rho], g.normal(size=shape), axis=0) * np.sqrt(1 - rho ** 2)
    return x[burn:]


# ----------------------------------------------------------------------------- umbral (H6)
def mc_umbral(R=300, B=299, n=120):
    R, B = nR(R), (29 if RAPIDO else B)
    # (a) dominio de 'wild': errores sin autocorrelacion, n = 120 (cifras historicas)
    for esc in ("H0_iid", "H0_heterocedastico", "H1_salto_pendiente"):
        rej, cov, gam = [], [], []
        for r in range(R):
            g = rng_(1, r)
            x, q = g.normal(size=n), g.normal(size=n)
            e = g.normal(size=n) * (np.sqrt(0.4 + x ** 2) if esc == "H0_heterocedastico" else 1.0)
            b = np.where(q > 0.0, 1.2, 0.4) if esc.startswith("H1") else 0.4
            y = 1 + b * x + e
            res = regimenes.umbral_hansen(y, np.column_stack([np.ones(n), x]), q, B=B, seed=SEED + r)
            rej.append(res["p_linealidad"] < 0.05)
            if esc.startswith("H1"):
                cov.append(res["ic_gamma"][0] <= 0.0 <= res["ic_gamma"][1])
                gam.append(res["gamma"])
        if esc.startswith("H0"):
            reg("umbral_hansen", "wild", f"{esc} (errores sin autocorrelación)", "tamaño (rechazo al 5%)", np.mean(rej), "tamano", R, B, n)
        else:
            reg("umbral_hansen", "wild", f"{esc} (errores sin autocorrelación)", "potencia (rechazo al 5%)", np.mean(rej), "potencia", R, B, n)
            reg("umbral_hansen", "IC_LR", f"{esc} (errores sin autocorrelación)", "cobertura IC95 del umbral por inversión de LR", np.mean(cov), "cobertura", R, B, n,
                nota="gamma verdadero = 0")
            reg("umbral_hansen", "IC_LR", f"{esc} (errores sin autocorrelación)", "sesgo mediano del umbral", np.median(gam), "error", R, B, n, umbral=0.15)

    # (b) errores autocorrelacionados y variable umbral persistente (AR 0,9): H0 y H1 con tres bootstraps
    def celda(n_, rho_e, boot, salto, rol, R_=R):
        rej, cov = [], []
        for r in range(R_):
            g = rng_(21, r, n_, int(rho_e * 100))
            x, q, e = g.normal(size=n_), ar1(g, n_, 0.9), ar1(g, n_, rho_e)
            y = 1 + np.where(q > 0, 0.4 + salto, 0.4) * x + e
            o = regimenes.umbral_hansen(y, np.column_stack([np.ones(n_), x]), q, B=B, seed=SEED + r, boot=boot)
            rej.append(o["p_linealidad"] < 0.05)
            cov.append(o["ic_gamma"][0] <= 0.0 <= o["ic_gamma"][1])
        cfg = {"wild": "wild", "bloque": "bloque_pw", "sieve": "sieve"}[boot]
        esc = f"{'H1 salto ' + str(salto) if salto else 'H0'} | errores AR({rho_e}), q AR(0,9)"
        if salto:
            reg("umbral_hansen", cfg, esc, "potencia (rechazo al 5%)", np.mean(rej), "potencia", R_, B, n_, rol=rol)
            reg("umbral_hansen", "IC_LR", esc + f" | boot={boot}", "cobertura IC95 del umbral por inversión de LR", np.mean(cov), "cobertura", R_, B, n_,
                rol="referencia" if boot != "sieve" else "principal", nota="IC por inversión de LR homocedástico (no depende del bootstrap)")
        else:
            reg("umbral_hansen", cfg, esc, "tamaño (rechazo al 5%)", np.mean(rej), "tamano", R_, B, n_, rol=rol)

    for n_ in (100, 126):
        celda(n_, 0.5, "wild", 0.0, "referencia")
        celda(n_, 0.5, "bloque", 0.0, "principal")
        celda(n_, 0.5, "sieve", 0.0, "principal")
    celda(110, 0.85, "wild", 0.0, "referencia")
    celda(110, 0.85, "bloque", 0.0, "principal")
    celda(110, 0.85, "sieve", 0.0, "principal")
    for n_ in (100, 126):
        celda(n_, 0.5, "bloque", 0.8, "principal")
        celda(n_, 0.5, "sieve", 0.8, "principal")


# ----------------------------------------------------------------------------- Bai-Perron (H5)
def _serie_bp(g, n, rho, het, shift):
    e = ar1(g, n, rho) if rho else g.normal(size=n)
    if het:
        e = e * np.r_[np.ones(n // 2) * .6, np.ones(n - n // 2) * 1.4]
    return e + shift * (np.arange(n) >= n // 2)


BOOT_BP = {"wild": ("wild", "auto"), "bloque_pw": ("bloque", "auto"), "bloque_8": ("bloque", 8), "sieve": ("sieve", "auto")}


def _celda_bp(n, rho, het, shift, cfg, R, B, tag, rol):
    boot, bl = BOOT_BP[cfg]
    rej, rej1, fecha, bls = [], [], [], []
    for r in range(R):
        g = rng_(2, r, tag)
        y = _serie_bp(g, n, rho, het, shift)
        res = regimenes.bai_perron(y, max_cortes=3, B=B, seed=SEED + r, boot=boot, bloque=bl)
        rej.append(res["p_UDmax"] < .05)
        rej1.append(res["p_supF"][0] < .05)
        if shift:
            fecha.append(abs(res["cortes"][1][0] - n // 2) if res["cortes"][1] else np.nan)
        if res["bloque_usado"]:
            bls.append(res["bloque_usado"])
    nota = f"bloque mediano {np.median(bls):.0f}" if bls else ""
    return np.mean(rej), np.mean(rej1), (np.nanmedian(fecha) if shift else np.nan), nota


def mc_bp_size(R=250, B=199):
    R, B = nR(R), (29 if RAPIDO else B)
    # cifras historicas (n=120): wild iid y heterocedastico; wild con AR(0,5) como demostracion del fallo
    for esc, rho, het in (("H0_iid", 0, 0), ("H0_heterocedastico", 0, 1)):
        u, s1, _, _ = _celda_bp(120, rho, het, 0, "wild", R, B, 0, "principal")
        reg("bai_perron", "wild", f"{esc} n=120 (errores sin autocorrelación)", "tamaño UDmax (5%)", u, "tamano", R, B, 120)
        reg("bai_perron", "wild", f"{esc} n=120 (errores sin autocorrelación)", "tamaño supF(1) (5%)", s1, "tamano", R, B, 120)
    # H5: tamaño con rho en {0, 0.5, 0.85}, n = 100 y 126, cuatro remuestreos
    for n in (100, 126):
        for rho in (0, 0.5, 0.85):
            for cfg in ("wild", "bloque_pw", "bloque_8", "sieve"):
                if n == 126 and cfg in ("wild", "bloque_pw"):
                    continue
                u, s1, _, nota = _celda_bp(n, rho, 0, 0, cfg, R, B, 10 + n, "")
                rol = "referencia" if (cfg == "wild" and rho > 0) else "principal"
                esc = f"H0 n={n} | errores AR({rho})"
                reg("bai_perron", cfg, esc, "tamaño UDmax (5%)", u, "tamano", R, B, n, nota=nota, rol=rol)
                reg("bai_perron", cfg, esc, "tamaño supF(1) (5%)", s1, "tamano", R, B, n, nota=nota, rol="referencia")


def mc_bp_pot(R=250, B=199):
    R, B = nR(R), (29 if RAPIDO else B)
    for n in (100, 126):
        for rho in (0, 0.5, 0.85):
            for cfg in ("bloque_8", "sieve"):
                for shift in (1.0, 2.0):
                    pot, _, fe, nota = _celda_bp(n, rho, 0, shift, cfg, R, B, 20 + n, "")
                    esc = f"H1 salto {shift}σ (σ marginal) n={n} | errores AR({rho})"
                    reg("bai_perron", cfg, esc, "potencia UDmax (5%)", pot, "potencia", R, B, n, nota=nota,
                        rol="principal" if shift == 2.0 else "referencia")
                    reg("bai_perron", cfg, esc, "error absoluto mediano de la fecha (obs.)", fe, "info", R, B, n)


# ----------------------------------------------------------------------------- Markov switching (H14)
def sim_ms(n, mu, s2, P, g):
    k = len(mu)
    s = np.zeros(n, int)
    for t in range(1, n):
        s[t] = g.choice(k, p=P[:, s[t - 1]])
    return np.asarray(mu)[s] + np.sqrt(np.asarray(s2)[s]) * g.normal(size=n)


DGP_MS = {
    "1reg": dict(mu=[0.], s2=[1.], P=np.ones((1, 1))),
    "2reg": dict(mu=[0., 1.5], s2=[1., 2.5], P=np.array([[.95, .05], [.05, .95]])),
    "3reg": dict(mu=[-2., 0., 2.], s2=[1., 1., 1.], P=np.array([[.92, .04, .04], [.04, .92, .04], [.04, .04, .92]])),
}


def mc_ms_bic(R=30, n=250):
    R = nR(R, 2)
    rol = "principal" if n <= 130 else "referencia"
    for nm, d in DGP_MS.items():
        ks = []
        for r in range(R):
            y = sim_ms(n, d["mu"], d["s2"], d["P"], rng_(3, r, n))
            bic = {1: -2 * n * (-0.5 * np.log(2 * np.pi * y.var()) - 0.5) + 2 * np.log(n)}
            for k in (2, 3):
                try:
                    bic[k] = regimenes.ms_fit(y, k, search_reps=3, seed=SEED + r)["bic"]
                except Exception:
                    bic[k] = np.inf
            ks.append(min(bic, key=bic.get))
        v = np.mean(np.array(ks) == len(d["mu"]))
        reg("markov_switching", "BIC", f"verdadero_{nm} (T={n})", "% BIC elige k verdadero", v, "acierto", R, "", n, umbral=0.70, rol=rol)


def mc_ms12(R=20, B=39, n=200):
    R, B = nR(R, 2), (9 if RAPIDO else B)
    rol = "principal" if n <= 130 else "referencia"
    for nm in ("1reg", "2reg"):
        d = DGP_MS[nm]
        rej = []
        for r in range(R):
            y = sim_ms(n, d["mu"], d["s2"], d["P"], rng_(4, r, n))
            rej.append(regimenes.ms_contraste_regimenes(y, 1, 2, B=B, search_reps=3, seed=SEED + r)["p"] < .05)
        v = np.mean(rej)
        if nm == "1reg":
            reg("markov_switching", "bootstrap_LR_1v2", f"H0_1reg (T={n})", "tamaño del bootstrap LR 1 vs 2 (5%)", v, "tamano", R, B, n, rol=rol,
                nota=f"R pequeño: IC binomial 95% ~ ±{1.96 * np.sqrt(.05 * .95 / R):.2f}")
        else:
            reg("markov_switching", "bootstrap_LR_1v2", f"H1_2reg (T={n})", "potencia del bootstrap LR 1 vs 2 (5%)", v, "potencia", R, B, n, rol=rol)


def mc_ms12_t110():
    mc_ms12(R=20, B=39, n=110)


def mc_msbic_t110():
    mc_ms_bic(R=30, n=110)


def mc_ms23(R=6, B=19, n=250):
    R, B = nR(R, 2), (9 if RAPIDO else B)
    # con B=19 el p minimo es 0,05: el criterio p<0,05 no puede rechazar -> NO CONCLUYENTE (tipo info)
    for nm in ("2reg", "3reg"):
        d = DGP_MS[nm]
        ps = []
        for r in range(R):
            y = sim_ms(n, d["mu"], d["s2"], d["P"], rng_(5, r))
            ps.append(regimenes.ms_contraste_regimenes(y, 2, 3, B=B, search_reps=2, seed=SEED + r)["p"])
        reg("markov_switching", "bootstrap_LR_2v3", f"{nm}_test_2v3 (T={n})", "rechazo bootstrap LR 2 vs 3 (5%)", np.mean(np.array(ps) < .05), "info", R, B, n,
            nota="NO CONCLUYENTE: B=19 => p mínimo 0,05 y el criterio p<0,05 no puede rechazar; R muy pequeño", rol="referencia")


# ----------------------------------------------------------------------------- LP y LP-IV (H7, H8)
VAR_LP = {"NW_h+1": dict(hac="h+1"), "NW_2h+2": dict(hac="2h+2"), "EWC": dict(ewc=True)}


def mc_lp(R=400, hs=(0, 4, 8, 12)):
    R = nR(R)
    for n in (90, 110):
        for rho in (0.6, 0.9):
            cob = {(c, h): [] for c in VAR_LP for h in list(hs) + [-4, -2, "4-8"]}
            ver_agr = np.mean([rho ** h for h in range(4, 9)])
            for r in range(R):
                g = rng_(6, r, n, int(rho * 100))
                x, e = g.normal(size=n + 50), g.normal(size=n + 50)
                y = lfilter([1.0], [1.0, -rho], x + e)
                y, x = y[50:], x[50:]
                for c, kw in VAR_LP.items():
                    res = lp.lp(y, x, H=max(hs), H_min=-4, rezagos=2, **kw).set_index("h")
                    for h in list(hs) + [-4, -2]:
                        tr = rho ** h if h >= 0 else 0.0
                        cob[(c, h)].append(res.lo[h] <= tr <= res.hi[h])
                    ag = lp.lp_agregado(y, x, hs=(4, 8), rezagos=2, **kw).iloc[0]
                    cob[(c, "4-8")].append(ag.lo <= ver_agr <= ag.hi)
            for (c, h), v in cob.items():
                reg("lp_ols", c, f"ρ={rho}, n={n}, h={h}" + (" (pretendencia: efecto verdadero 0)" if isinstance(h, int) and h < 0 else ""),
                    "cobertura IC95", np.mean(v), "cobertura", R, "", n)


def _dgp_iv(g, n, pi, beta, rho, contaminada=False):
    N = n + 50
    z, v, w = g.normal(size=N), g.normal(size=N), g.normal(size=N)
    u = .7 * v + np.sqrt(1 - .49) * w
    if contaminada:  # instrumento invalido: correlacionado con el error del periodo anterior
        z = z + 0.6 * np.r_[0.0, u[:-1]]
    x = pi * z + v
    y = lfilter([1.0], [1.0, -rho], beta * x + u)
    return y[50:], x[50:], z[50:]


def mc_lpiv(R=300, hs=(0, 4, 8, 12)):
    R = nR(R)
    esc_iv = (("instrumento_fuerte", 1.0, 0.5), ("instrumento_debil", 0.12, 0.5), ("instrumento_debil_rho0.8", 0.12, 0.8))
    for n in (90, 110):
        for nm, pi, rho in esc_iv:
            cn = {h: [] for h in list(hs) + ["4-8"]}
            ca = {h: [] for h in list(hs) + ["4-8"]}
            Fm, acot = [], []
            ver_agr = np.mean([rho ** h for h in range(4, 9)])
            for r in range(R):
                y, x, z = _dgp_iv(rng_(7, r, n, int(pi * 100), int(rho * 100)), n, pi, 1.0, rho)
                for h in hs:
                    row = lp.lp_iv(y, x, z, H=h, H_min=h, rezagos=2, grid_n=601).iloc[0]
                    tr = rho ** h
                    cn[h].append(row.lo <= tr <= row.hi)
                    ca[h].append(row.ar_lo <= tr <= row.ar_hi)
                    acot.append(row.ar_acotado)
                    if h == 0:
                        Fm.append(row.F_robusto)
                row = lp.lp_iv_agregado(y, x, z, hs=(4, 8), rezagos=2, grid_n=601).iloc[0]
                cn["4-8"].append(row.lo <= ver_agr <= row.hi)
                ca["4-8"].append(row.ar_lo <= ver_agr <= row.ar_hi)
            nota = f"F robusto mediano {np.median(Fm):.1f}; % AR no acotado {100 * (1 - np.mean(acot)):.0f}"
            for h in cn:
                reg("lp_iv", "AR", f"{nm}, n={n}, h={h}", "cobertura IC Anderson-Rubin", np.mean(ca[h]), "cobertura_inf", R, "", n, nota=nota)
                reg("lp_iv", "IC_normal", f"{nm}, n={n}, h={h}", "cobertura IC normal 2SLS", np.mean(cn[h]), "cobertura", R, "", n, nota=nota,
                    rol="principal" if nm == "instrumento_fuerte" else "referencia")


def mc_lpiv_inf(R=300):
    """p-valor AR unilateral (H8-5/H8-6), pretendencias y placebo de permutacion del instrumento (H7)."""
    R = nR(R)
    n, rho = 110, 0.9  # persistencia alta: el efecto verdadero a h=4-8 (beta*rho^h) no es despreciable
    # (1) tamaño y potencia de la AR unilateral a h=4 y agregado 4-8; efecto verdadero -1 (potencia) o 0 (tamaño); IV fuerte
    for beta, etq in ((0.0, "efecto nulo"), (-1.0, "efecto -1")):
        rej_h4, rej_agr, rej_dos = [], [], []
        for r in range(R):
            y, x, z = _dgp_iv(rng_(30, r, int(beta * 10) + 10), n, 1.0, beta, rho)
            a = lp.lp_iv(y, x, z, H=4, H_min=4, grid_n=201).iloc[0]
            b = lp.lp_iv_agregado(y, x, z, hs=(4, 8), grid_n=201).iloc[0]
            rej_h4.append(a.ar_p_menor < .05)
            rej_dos.append(a.ar_p_dos < .05)
            rej_agr.append(b.ar_p_menor < .05)
        t = "tamano" if beta == 0 else "potencia"
        nm = "tamaño" if beta == 0 else "potencia"
        reg("lp_iv", "AR_unilateral", f"{etq}, IV fuerte, n={n}, h=4", f"{nm} AR unilateral (H1: β<0) al 5%", np.mean(rej_h4), t, R, "", n)
        reg("lp_iv", "AR_unilateral", f"{etq}, IV fuerte, n={n}, agregado 4-8", f"{nm} AR unilateral (H1: β<0) al 5%", np.mean(rej_agr), t, R, "", n)
        reg("lp_iv", "AR_unilateral", f"{etq}, IV fuerte, n={n}, h=4", f"{nm} AR bilateral al 5%", np.mean(rej_dos), t, R, "", n, rol="referencia")
    # (2) pretendencias: IV valido (tamaño) frente a instrumento contaminado (deteccion)
    for cont, etq in ((False, "IV válido"), (True, "IV contaminado")):
        rej1, rej_any = [], []
        for r in range(R):
            y, x, z = _dgp_iv(rng_(31, r, int(cont)), n, 1.0, 1.0, rho, contaminada=cont)
            res = lp.lp_iv(y, x, z, H=-1, H_min=-4, grid_n=201)
            rej1.append(res.ar_p_dos.iloc[-1] < .05)
            rej_any.append((res.ar_p_dos < .05).any())
        t = "potencia" if cont else "tamano"
        nm = "detección" if cont else "tamaño"
        reg("lp_iv", "pretendencias", f"{etq}, n={n}, h=-1", f"{nm} (p AR bilateral < 0,05)", np.mean(rej1), t, R, "", n)
        reg("lp_iv", "pretendencias", f"{etq}, n={n}, algún h en -4..-1", f"{nm} (p AR bilateral < 0,05 en algún h)", np.mean(rej_any), t if cont else "info", R, "", n,
            nota="4 contrastes sin ajuste: el tamaño 'algún h' puede llegar a ~0,19" if not cont else "", rol="referencia")
    # (3) placebo por permutacion del instrumento: rechazo de p_perm<0,05 con efecto verdadero (potencia) y nulo (tamaño)
    npm = 99 if RAPIDO else 199
    for beta, etq in ((0.0, "efecto nulo"), (1.0, "efecto 1")):
        rej, rej_a = [], []
        for r in range(R):
            y, x, z = _dgp_iv(rng_(32, r, int(beta * 10)), n, 1.0, beta, rho)
            rej.append(lp.placebo_permutacion_iv(y, x, z, h=4, n_perm=npm, seed=SEED + r)["p_perm"] < .05)
            rej_a.append(lp.placebo_permutacion_iv(y, x, z, agregado=(4, 8), n_perm=npm, seed=SEED + r, modo="desplazamiento")["p_perm"] < .05)
        t = "tamano" if beta == 0 else "potencia"
        nm = "tamaño" if beta == 0 else "potencia"
        reg("lp_iv", "placebo_permutacion", f"{etq}, IV fuerte, n={n}, h=4 (permutación libre)", f"{nm} (p_perm < 0,05)", np.mean(rej), t, R, npm, n)
        reg("lp_iv", "placebo_permutacion", f"{etq}, IV fuerte, n={n}, agregado 4-8 (desplazamiento circular)", f"{nm} (p_perm < 0,05)", np.mean(rej_a), t, R, npm, n)


# ----------------------------------------------------------------------------- dominancia (H14)
def mc_dominancia(R=60, B=100):
    R, B = nR(R), (20 if RAPIDO else B)
    p = 5
    S = np.eye(p)
    S[0, 1] = S[1, 0] = .8
    S[2, 3] = S[3, 2] = .6
    S[1, 2] = S[2, 1] = .3
    beta = np.array([1., .5, .8, 0., .3])
    c = S @ beta
    vy = beta @ S @ beta + 1.0
    cache = {frozenset(): 0.0}
    for r in range(1, p + 1):
        for T in itertools.combinations(range(p), r):
            cs = c[list(T)]
            cache[frozenset(T)] = float(cs @ np.linalg.solve(S[np.ix_(T, T)], cs)) / vy
    phi0 = dominancia._shapley_from_cache(cache, p)
    vif0 = np.diag(np.linalg.inv(S))
    L = np.linalg.cholesky(S)
    celdas = [  # n, rho_x, rho_e, bloque, config, rol
        (300, 0.0, 0.0, 1, "filas", "referencia"),
        (100, 0.0, 0.0, 1, "filas", "principal"),
        (100, 0.8, 0.5, 1, "filas", "referencia"),
        (100, 0.8, 0.5, 8, "bloque_8", "principal"),
        (126, 0.8, 0.5, 8, "bloque_8", "principal"),
    ]
    for n, rx, re_, bl, cfg, rol in celdas:
        err, cov, top, vif_err = [], [], [], []
        for r in range(R):
            g = rng_(8, r, n, int(rx * 10))
            X = (ar1(g, n, rx, size=p) if rx else g.normal(size=(n, p))) @ L.T
            e = ar1(g, n, re_) if re_ else g.normal(size=n)
            y = X @ beta + e
            o = dominancia.shapley_r2(X, y, B=B, bloque=bl, seed=SEED + r)
            err.append(np.abs(o.phi.values - phi0))
            cov.append((o.lo.values <= phi0) & (phi0 <= o.hi.values))
            top.append(np.argsort(-o.phi.values)[:2].tolist() == np.argsort(-phi0)[:2].tolist())
            vif_err.append(np.max(np.abs(dominancia.colinealidad(X)["vif"].values / vif0 - 1)))
            if r == 0 and n == 300:
                jr = dominancia.johnson_rw(X, y)
                d_ = np.max(np.abs(jr.peso.values - o.phi.values))
                reg("dominancia", "filas", "p=5 colineal, n=300", "|Johnson - LMG| máx (en R2)", d_, "error", 1, "", n, umbral=0.05, rol="referencia")
        esc = f"p=5 colineal, n={n}, regresores AR({rx}), errores AR({re_})"
        nota = f"phi verdadero={np.round(phi0, 3).tolist()}"
        reg("dominancia", cfg, esc, "error absoluto medio de phi (R2)", np.mean(err), "error", R, B, n, umbral=0.03, nota=nota, rol=rol)
        reg("dominancia", cfg, esc, "cobertura IC95 bootstrap de phi", np.mean(cov), "cobertura", R, B, n, rol=rol)
        reg("dominancia", cfg, esc, "% acierto en las 2 variables dominantes (orden)", np.mean(top), "acierto", R, B, n, umbral=0.80, rol=rol)
        reg("dominancia", cfg, esc, "error relativo máx del VIF", np.mean(vif_err), "error", R, "", n, umbral=0.20, rol=rol)


# ----------------------------------------------------------------------------- permutacion de fechas (H13)
def mc_perm(R=250, n=100, n_perm=2000, min_len=15, shift_h1=.8, etq="", escs=(("H0_iid", 0, 0.0), ("H0_AR0.5", .5, 0.0), ("H1_ruptura_pendiente", 0, None))):
    R, n_perm = nR(R), (199 if RAPIDO else n_perm)
    for esc, rho, shift in escs:
        shift = shift_h1 if shift is None else shift
        rej = {"t_studentizado": [], "dif_sin_studentizar": []}
        for r in range(R):
            g = rng_(9, r, n)
            x = g.normal(size=n)
            e = ar1(g, n, rho) if rho else g.normal(size=n)
            y = 1 + np.where(np.arange(n) >= n // 2, .5 + shift, .5) * x + e
            X = np.column_stack([np.ones(n), x])
            for cfg, fabrica in (("dif_sin_studentizar", permutacion.stat_dif_coef), ("t_studentizado", permutacion.stat_t_dif_coef)):
                rej[cfg].append(permutacion.permutacion_cortes(fabrica(y, X, 1), n, (n // 2,), min_len, n_perm=n_perm, seed=SEED + r)["p"] < .05)
        for cfg, lst in rej.items():
            v = np.mean(lst)
            if esc.startswith("H0"):
                reg("permutacion_fechas", cfg + "_2tramos", f"{esc}{etq} (n={n})", "tamaño (5%)", v, "tamano", R, n_perm, n,
                    rol="principal" if n <= 130 else "referencia")
            else:
                reg("permutacion_fechas", cfg + "_2tramos", f"{esc}{etq} (n={n})", "potencia (5%)", v, "potencia", R, n_perm, n,
                    rol="principal" if n <= 130 else "referencia")


def mc_perm_n200():
    mc_perm(R=250, n=200, min_len=20, shift_h1=1.0, etq=" salto 1,0", escs=(("H0_iid", 0, 0.0), ("H1_ruptura_pendiente", 0, None)))


TRAMOS_5 = ((0, 28), (32, 58), (58, 80), (80, 106), (108, 126))  # n=126, huecos de 4 y 2 observaciones, longitudes 18-28


def mc_perm_multi(R=200, n_perm=499, min_len=8):
    R, n_perm = nR(R), (99 if RAPIDO else n_perm)
    n = 126
    fabricas = {"Q_homo": lambda y, X: permutacion.stat_Q_tramos(y, X, 1, se="homo"),
                "maxt_homo": lambda y, X: permutacion.stat_maxt_tramos(y, X, 1, se="homo"),
                "Q_hac": lambda y, X: permutacion.stat_Q_tramos(y, X, 1, se="hac", L=4)}
    for rho in (0.0, 0.8):
        for h1 in (False, True):
            bet = np.array([.3, .3, 1.2, 1.2, .3]) if h1 else np.full(5, .5)
            rej = {k: [] for k in fabricas}
            for r in range(R):
                g = rng_(40, r, int(rho * 10), int(h1))
                x = g.normal(size=n)
                e = ar1(g, n, rho) if rho else g.normal(size=n)
                b = np.full(n, .5)
                for (a_, c_), bb in zip(TRAMOS_5, bet):
                    b[a_:c_] = bb
                y = 1 + b * x + e
                X = np.column_stack([np.ones(n), x])
                for k, f in fabricas.items():
                    rej[k].append(permutacion.permutacion_tramos(f(y, X), n, TRAMOS_5, min_len, n_perm=n_perm, seed=SEED + r)["p"] < .05)
            for k, lst in rej.items():
                v = np.mean(lst)
                esc = f"{'H1 pendientes (0,3; 0,3; 1,2; 1,2; 0,3)' if h1 else 'H0 pendiente constante'}, 5 tramos no contiguos, n={n}, min {min_len}, AR({rho})"
                reg("permutacion_fechas", k + "_5tramos", esc, "potencia (5%)" if h1 else "tamaño (5%)", v, "potencia" if h1 else "tamano", R, n_perm, n)


# ----------------------------------------------------------------------------- SHAP agrupado, DFM
GR = {"F1": ["a", "b"], "F2": ["c"], "F3": ["d", "e"], "F4": ["f"]}


def dgp_shap(g, n, duro=False):
    X = pd.DataFrame(g.normal(size=(n, 6)), columns=list("abcdef"))
    if duro:  # F1 y F2 casi iguales en importancia
        y = 1.0 * X.a + 0.2 * X.b + 0.95 * X.c + 0.3 * X.d * X.e + g.normal(size=n) * .5
    else:
        y = 2 * X.a + 1.5 * X.b + np.sin(2 * X.c) + 0.7 * X.d * X.e + g.normal(size=n) * .5
    return X, y


def mc_shap(R=30, n=400, Rest=10, B=20):
    R, Rest, B = nR(R, 2), nR(Rest, 2), (4 if RAPIDO else B)
    ok = []
    for r in range(R):
        X, y = dgp_shap(rng_(10, r), n)
        m = shap_grupos.modelo_lgbm(seed=SEED + r).fit(X.values, y)
        ok.append(list(shap_grupos.shap_grupos(m, X, GR)[0].index) == ["F1", "F2", "F3", "F4"])
    reg("shap_grupos", "ranking_familias", "DGP aditivo+interacción (orden verdadero F1>F2>F3>F4)", "% ranking correcto de familias", np.mean(ok), "acierto", R, "", n, umbral=0.90, rol="referencia")
    for duro in (False, True):
        pc, pt, pb = [], [], []
        for r in range(Rest):
            X, y = dgp_shap(rng_(11, r), n, duro)
            e = shap_grupos.estabilidad_ranking(X, y, GR, B=B, seed=SEED + r)
            pb.append(e["pct_ranking_completo_bootstrap"])
            pt.append(e["pct_ranking_completo_pliegues"])
            pc.append(e["pct_misma_pos_bootstrap"].min())
        esc = "DGP duro (F1≈F2)" if duro else "DGP claro"
        reg("shap_grupos", "estabilidad_bootstrap", esc, "% réplicas bootstrap con ranking completo igual (media)", np.mean(pb), "info" if duro else "acierto", Rest, B, n,
            umbral=0.80, rol="referencia")
        reg("shap_grupos", "estabilidad_pliegues", esc, "% pliegues temporales con ranking completo igual (media)", np.mean(pt), "info", Rest, 4, n, rol="referencia")
    X, y = dgp_shap(rng_(12, 0), n)
    m = shap_grupos.modelo_lgbm().fit(X.values, y)
    reg("shap_grupos", "sustituto", "arbol sustituto prof.3", "fidelidad R2", shap_grupos.sustituto(m, X)["fidelidad_r2"], "info", 1, "", n)
    ale = shap_grupos.ale_1d(m.predict, X, "c")
    reg("shap_grupos", "ALE", "ALE de c vs sin(2c) centrado", "correlación", np.corrcoef(ale.ale, np.sin(2 * ale.x))[0, 1], "acierto", 1, "", n, umbral=0.90, rol="referencia")


def mc_dfm(R=200):
    R = nR(R, 5)
    # Bai-Ng: referencia (N grande y N pequeno) y uso previsto (N=17, T=110/126)
    for T, N, r_t, rol in ((120, 40, 2, "referencia"), (120, 10, 2, "referencia"), (110, 17, 1, "principal"), (126, 17, 1, "principal"),
                           (110, 17, 2, "principal")):
        ok = []
        for r in range(R):
            g = rng_(13, r, T, N, r_t)
            F = g.normal(size=(T, r_t))
            X = F @ g.normal(size=(r_t, N)) + g.normal(size=(T, N))
            ok.append(dfm.bai_ng(X, 8)["k_ic2"] == r_t)
        reg("dfm_baing", "IC_p2", f"T={T},N={N},r={r_t}", "% IC_p2 elige r verdadero", np.mean(ok), "acierto", R, "", T, umbral=0.90, rol=rol,
            nota="con N pequeño el criterio tiende a elegir kmax" if N <= 17 else "")
    # varianza explicada por el primer componente (H8-8): sesgo respecto a la parte comun verdadera, T=110,N=17, factor AR(0,7)
    err, est, ver = [], [], []
    for r in range(R):
        g = rng_(15, r)
        T, N = 110, 17
        f = lfilter([1.0], [1.0, -.7], g.normal(size=T + 100))[100:]
        lam = g.uniform(.4, 1.2, N)
        X = np.outer(f, lam) + g.normal(size=(T, N))
        vf = 1 / (1 - .49)
        tv = np.sum(lam ** 2 * vf) / np.sum(lam ** 2 * vf + 1)
        e_ = dfm.pca_factores(X, 1)["var_explicada_total"]
        err.append(e_ - tv)
        est.append(e_)
        ver.append(tv)
    reg("dfm_pca", "PCA_r1", "T=110,N=17,r=1 (factor AR(0,7))", "sesgo medio de la varianza explicada por el 1.er factor (estimada - verdadera)", np.mean(err), "error", R, "", 110,
        umbral=0.05, nota=f"verdadera media {np.mean(ver):.3f}; estimada media {np.mean(est):.3f}; error absoluto medio {np.mean(np.abs(err)):.3f}")
    # DFM-ML: R2 de la parte comun recuperado (AR(1) factor)
    Rm = nR(15, 2)
    for T, N, rol in ((100, 8, "referencia"), (110, 17, "principal")):
        e2 = []
        for r in range(Rm):
            g = rng_(14, r, T, N)
            f = lfilter([1.0], [1.0, -.7], g.normal(size=T))
            lam = g.uniform(.5, 1.5, N)
            X = np.outer(f, lam) + g.normal(size=(T, N))
            r2_true = lam ** 2 * f.var() / (lam ** 2 * f.var() + 1)
            o = dfm.dfm_ml(X, 1)
            e2.append(np.mean(np.abs(o["r2"].values[:, 0] - r2_true)))
        reg("dfm_ml", "ML_r1", f"T={T},N={N},r=1", "error absoluto medio del R2 por variable", np.mean(e2), "error", Rm, "", T, umbral=0.10, rol=rol)


# ----------------------------------------------------------------------------- bloques, fusion y etiquetas
BLOQUES = {"ms12": [mc_ms12, mc_ms12_t110], "ms23": [mc_ms23], "msbic": [mc_ms_bic, mc_msbic_t110],
           "umbral": [mc_umbral], "bp_size": [mc_bp_size], "bp_pot": [mc_bp_pot], "lp": [mc_lp], "lpiv": [mc_lpiv], "lpiv_inf": [mc_lpiv_inf],
           "dom": [mc_dominancia], "perm": [mc_perm, mc_perm_n200], "perm_multi": [mc_perm_multi], "shap": [mc_shap], "dfm": [mc_dfm]}

HERRAMIENTAS_SIN_MC = {"multiverso": "sin Monte Carlo: verificación determinista por tests unitarios (tests/v8/test_herramientas_otros.py); registra todas las "
                       "especificaciones, también las fallidas, con tope por defecto de 50.000"}


def _fmt(v):
    return f"{v:.3f}".replace(".", ",")


def etiqueta_dim(sub):
    """('apta'|'con reservas'|'no apta'|'sin datos', filas que no cumplen) sobre las filas principales `sub`."""
    sub = sub[sub.cumple.notna()]
    if sub.empty:
        return "sin datos", sub
    ok = sub.cumple.map(lambda x: str(x) == "True")
    laxo = sub.laxo.map(lambda x: str(x) == "True")
    if ok.all():
        return "apta", sub[~ok]
    return ("con reservas" if laxo.all() else "no apta"), sub[~ok]


def etiquetas(df):
    """Etiqueta por (herramienta, configuracion) derivada de REGLAS sobre las filas principales: validez (tamaño, cobertura,
    acierto, error) y potencia por separado. Devuelve lista de dicts con las cifras que determinan la etiqueta."""
    out = []
    pr = df[(df.rol == "principal") & (df.tipo != "info")]
    for (h, c), g in pr.groupby(["herramienta", "config"], sort=False):
        ev, mal_v = etiqueta_dim(g[g.tipo.isin(TIPOS_VALIDEZ)])
        ep, mal_p = etiqueta_dim(g[g.tipo == "potencia"])
        peor = pd.concat([mal_v, mal_p])
        cif = "; ".join(f"{r.escenario}: {r.metrica} = {_fmt(r.valor)}" for r in peor.head(5).itertuples())
        if len(peor) > 5:
            cif += f"; (+{len(peor) - 5} filas más, ver montecarlo.csv; {len(peor)} de {len(g)} filas principales no cumplen)"
        out.append({"herramienta": h, "config": c, "validez": ev, "potencia": ep, "n_filas": len(g),
                    "incumple": cif or "todas las filas principales cumplen",
                    "rango_tamano": (f"{_fmt(g[g.tipo == 'tamano'].valor.min())}-{_fmt(g[g.tipo == 'tamano'].valor.max())}" if (g.tipo == "tamano").any() else ""),
                    "rango_potencia": (f"{_fmt(g[g.tipo == 'potencia'].valor.min())}-{_fmt(g[g.tipo == 'potencia'].valor.max())}" if (g.tipo == "potencia").any() else ""),
                    "rango_cobertura": (f"{_fmt(g[g.tipo == 'cobertura'].valor.min())}-{_fmt(g[g.tipo == 'cobertura'].valor.max())}" if (g.tipo == "cobertura").any() else "")})
    return pd.DataFrame(out)


def merge():
    parc = sorted(OUT.glob("_parcial_*.csv"))
    df = pd.concat([pd.read_csv(p) for p in parc], ignore_index=True)
    df.to_csv(OUT / "montecarlo.csv", index=False)
    seg = {p.stem.replace("_parcial_", ""): json.loads((OUT / f"_tiempo_{p.stem.replace('_parcial_', '')}.json").read_text())["segundos"] for p in parc}
    E = etiquetas(df)
    E.to_csv(OUT / "etiquetas.csv", index=False)
    L = ["# Validación Monte Carlo — herramientas V8-F3 grupo B (no VAR), versión corregida tras la revisión F3", "",
         "Solo datos simulados; SEED=20261010; un hilo por proceso; determinista. Bloques en procesos paralelos (4 núcleos): "
         + ", ".join(f"{k} {v:.0f} s" for k, v in seg.items()) + ". Detalle por fila en `montecarlo.csv`; etiquetas en `etiquetas.csv`.", "",
         "## Reglas de etiquetado (derivadas en el código, `REGLAS`)", "",
         "Las reglas de «con reservas» las fijó el ejecutor tras ver las cifras de la primera pasada de F3 (no están pre-registradas). "
         "Una configuración (herramienta + remuestreo/EE) recibe dos etiquetas sobre sus filas PRINCIPALES (uso previsto: T ≈ 90-126; las filas de "
         "referencia, con n=200-300 o fuera del dominio de la configuración, se muestran pero no etiquetan):", "",
         "| Tipo de cifra | apta | con reservas |", "|---|---|---|"]
    for k, (a, b) in REGLAS.items():
        L.append(f"| {k} | {a} | {b} |")
    L += ["", "Validez = tamaño, cobertura, acierto y error; potencia aparte. «apta» si todas las filas cumplen; «con reservas» si todas están en la banda laxa; "
          "«no apta» en otro caso.", "", "## Etiquetas por configuración", "",
          "| Herramienta | Configuración | Validez | Potencia | Rango tamaño | Rango cobertura | Rango potencia | Filas que no cumplen (cifras) |", "|---|---|---|---|---|---|---|---|"]
    for r in E.itertuples():
        L.append(f"| {r.herramienta} | {r.config} | **{r.validez}** | **{r.potencia}** | {r.rango_tamano} | {r.rango_cobertura} | {r.rango_potencia} | {str(r.incumple).replace('|', '/')} |")
    for k, v in HERRAMIENTAS_SIN_MC.items():
        L.append(f"| {k} | - | no evaluada por MC | - | | | | {v} |")
    def _v(h, c, esc, met):
        m = df[(df.herramienta == h) & (df.config == c) & df.escenario.str.contains(esc, regex=False) & df.metrica.str.contains(met, regex=False)]
        return "n/d" if m.empty else _fmt(float(m.valor.iloc[0]))
    L += ["", "## Restricciones de uso (cifras generadas desde montecarlo.csv)", "",
          f"- **Bai-Perron (H5).** Tamaño de UDmax con errores AR(0,85): wild {_v('bai_perron', 'wild', 'H0 n=100 | errores AR(0.85)', 'tamaño UDmax')}, bloque Politis-White "
          f"{_v('bai_perron', 'bloque_pw', 'H0 n=100 | errores AR(0.85)', 'tamaño UDmax')}, bloque fijo 8 {_v('bai_perron', 'bloque_8', 'H0 n=100 | errores AR(0.85)', 'tamaño UDmax')}, "
          f"sieve {_v('bai_perron', 'sieve', 'H0 n=100 | errores AR(0.85)', 'tamaño UDmax')} (n=100) y {_v('bai_perron', 'sieve', 'H0 n=126 | errores AR(0.85)', 'tamaño UDmax')} (n=126). "
          f"Con AR(0,5): sieve {_v('bai_perron', 'sieve', 'H0 n=100 | errores AR(0.5)', 'tamaño UDmax')}. Uso: solo `boot='sieve'` con series persistentes; "
          f"su potencia con salto de 2σ y AR(0,85) es {_v('bai_perron', 'sieve', 'salto 2.0σ (σ marginal) n=100 | errores AR(0.85)', 'potencia')} (n=100) y "
          f"{_v('bai_perron', 'sieve', 'salto 2.0σ (σ marginal) n=126 | errores AR(0.85)', 'potencia')} (n=126): un no rechazo con series muy persistentes NO es evidencia de ausencia de ruptura.",
          f"- **Umbral de Hansen (H6).** Con errores AR(0,5) y q AR(0,9), n=100: tamaño wild {_v('umbral_hansen', 'wild', 'H0 | errores AR(0.5)', 'tamaño')}, bloque {_v('umbral_hansen', 'bloque_pw', 'H0 | errores AR(0.5)', 'tamaño')}, "
          f"sieve {_v('umbral_hansen', 'sieve', 'H0 | errores AR(0.5)', 'tamaño')}; con AR(0,85): wild {_v('umbral_hansen', 'wild', 'H0 | errores AR(0.85)', 'tamaño')}, bloque {_v('umbral_hansen', 'bloque_pw', 'H0 | errores AR(0.85)', 'tamaño')}, "
          f"sieve {_v('umbral_hansen', 'sieve', 'H0 | errores AR(0.85)', 'tamaño')}. Uso: `boot='wild'` solo con errores sin autocorrelación; con errores autocorrelacionados, `boot='sieve'`.",
          "- **LP-OLS (H8).** Ver filas `lp_ols`: la cobertura NW(h+1) cae por debajo de 0,90 en varios horizontes con n=90-110 y ρ=0,9 (mínimo "
          f"{_fmt(df[df.herramienta == 'lp_ols'][df.config == 'NW_h+1'].valor.min())}); EWC ({_fmt(df[df.herramienta == 'lp_ols'][df.config == 'EWC'].valor.min())} mínimo) es la menos mala; "
          f"el ancho de banda mayor NW(2h+2) empeora ({_fmt(df[df.herramienta == 'lp_ols'][df.config == 'NW_2h+2'].valor.min())}). LP-OLS no se usa como evidencia de C3.",
          "- **LP-IV.** El IC Anderson-Rubin cubre entre "
          f"{_fmt(df[(df.herramienta == 'lp_iv') & (df.config == 'AR')].valor.min())} y {_fmt(df[(df.herramienta == 'lp_iv') & (df.config == 'AR')].valor.max())}; "
          "el p unilateral, las pretendencias y el placebo de permutación se resumen en las filas de `lp_iv` (potencia del placebo baja).", "",
          "## Resultados por prueba", "", "| Herramienta | Config. | Escenario | Métrica | Valor | Objetivo | Cumple | Rol | Réplicas | B | n |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in df.itertuples():
        c = "" if pd.isna(r.cumple) else ("sí" if str(r.cumple) == "True" else "NO")
        esc_, met_, obj_ = (str(x).replace("|", "/") for x in (r.escenario, r.metrica, r.objetivo))
        L.append(f"| {r.herramienta} | {r.config} | {esc_} | {met_} | {_fmt(r.valor)} | {obj_} | {c} | {r.rol} | {r.reps} | {'' if pd.isna(r.B) else r.B} | {'' if pd.isna(r.n) else r.n} |")
    L += ["", "## Notas y límites", "",
          "- Con R réplicas el error de Monte Carlo del tamaño nominal 5 % es ±1,96·sqrt(0,05·0,95/R): ±0,027 con R=250, ±0,031 con R=200, ±0,043 con R=100; con R<=30 las cifras de MS son orientativas.",
          "- Bai-Perron: el bootstrap `wild` no corrige autocorrelación (sobre-rechaza); `bloque_pw` (Politis-White) elige bloques cortos y deja tamaño inflado; "
          "`sieve` (AR por BIC sobre los residuos de la nula) es la configuración con tamaño más cercano al nominal y sacrifica potencia con persistencia alta. "
          "Una variante que estima el AR sobre los residuos del mejor modelo con un corte se probó en un piloto (tamaño 0,13-0,21 con R=300) y se descartó.",
          "- Umbral de Hansen: el IC del umbral por inversión de la LR es homocedástico y no se corrige por autocorrelación; su cobertura se informa aparte (config. IC_LR).",
          "- Permutación de fechas: validez aproximada (no exacta); con 5 tramos no contiguos el contraste resulta conservador y de potencia baja (ver filas).",
          "- Markov switching: el bootstrap paramétrico es costoso (cada réplica reajusta k0 y k1); el contraste 2 vs 3 solo se probó con R muy pequeño y es NO concluyente. "
          "Y3/desviaciones: k por BIC.",
          "- LP-IV: el p-valor AR unilateral usa el signo de la primera etapa estimada (válido si el signo se da por conocido).",
          "- Ninguna herramienta se ha estimado con datos reales. Predicción != causalidad (SHAP, ALE, dominancia son descriptivos)."]
    (OUT / "validacion.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    est = {f"{r.herramienta}[{r.config}]": {"validez": r.validez, "potencia": r.potencia} for r in E.itertuples()}
    est.update({k: {"validez": "no evaluada por MC", "potencia": "-"} for k in HERRAMIENTAS_SIN_MC})
    diag = {f"{r.herramienta}[{r.config}]": r.incumple for r in E.itertuples()}
    res = {"rama": "v8/F3/otros", "pregunta": "¿Las herramientas no-VAR (regímenes, DFM, LP/LP-IV, dominancia, permutación de fechas, SHAP agrupado, multiverso) tienen tamaño, potencia y cobertura aceptables en DGP conocidos, con T≈90-126 y persistencia alta?",
           "capa": "C4 (validación metodológica con datos simulados; sin resultados sobre vivienda)", "datos": "SIMULADOS (SEED=20261010)",
           "N": int(df.reps.max()), "metodo": "Monte Carlo por herramienta y configuración (ver montecarlo.csv); etiquetas derivadas de REGLAS (etiquetas.csv)",
           "estimacion": est, "ic95": None, "p_ajustado": None,
           "nivel_evidencia": "DESCRIPTIVO (validación de herramientas; no es evidencia sobre el mercado de vivienda)",
           "diagnosticos": diag, "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Reglas de «con reservas» definidas tras ver las cifras de la primera pasada. Réplicas en montecarlo.csv. Tiempos de bloque (s): " + json.dumps(seg)}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(E[["herramienta", "config", "validez", "potencia"]].to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bloque", choices=list(BLOQUES))
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--rapido", action="store_true")
    a = ap.parse_args()
    RAPIDO = a.rapido
    OUT.mkdir(parents=True, exist_ok=True)
    if a.merge:
        merge()
    elif a.rapido and not a.bloque:
        t0 = time.time()
        for nm, fs in BLOQUES.items():
            for f in fs:
                f()
            print(nm, round(time.time() - t0, 1), "s", flush=True)
        pd.DataFrame(FILAS).to_csv(OUT / "_parcial_rapido.csv", index=False)
        (OUT / "_tiempo_rapido.json").write_text(json.dumps({"segundos": round(time.time() - t0, 1)}))
        merge()
    else:
        t0 = time.time()
        for f in BLOQUES[a.bloque]:
            f()
        pd.DataFrame(FILAS).to_csv(OUT / f"_parcial_{a.bloque}.csv", index=False)
        (OUT / f"_tiempo_{a.bloque}.json").write_text(json.dumps({"segundos": round(time.time() - t0, 1)}))
        print(a.bloque, "ok", round(time.time() - t0, 1), "s")
