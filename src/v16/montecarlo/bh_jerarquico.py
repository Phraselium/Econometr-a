"""Control de falsos descubrimientos jerárquico (Simes por familia, q=0,10; BH dentro de las familias rechazadas).

Estructura: rejilla fija de V16 (83 celdas, 5 familias; output/v16/potencia/rejilla_fija.csv) y rama de diseños
(adenda punto 3: 18 pruebas en la tabla; se repite con 21 para cubrir el recuento del encargo). Solo se lee la
ESTRUCTURA (pregunta, resultado, escala); los estadísticos se simulan. Alternativa nombrada: Benjamini-Yekutieli.
Uso: python bh_jerarquico.py [R]
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.montecarlo import _comun_series as C  # noqa: E402

Q = 0.10

# Rama de diseños: (id, familia = pregunta, grupo de resultado, escala-pregunta)
DISENOS = [("Q1b", "Q1", "serpavi"), ("Q1c", "Q1", "compraventas"), ("Q2a", "Q2", "ipc_alq"), ("Q2c", "Q2", "ipva"),
           ("Q3-c1", "Q3", "valor_tasado"), ("Q3-c2", "Q3", "compraventas"), ("Q3-b", "Q3", "serpavi"),
           ("Q4a", "Q4", "obra_nueva"), ("Q4b", "Q4", "serpavi"), ("Q5-p", "Q5", "valor_tasado"), ("Q5-a", "Q5", "ipc_alq"),
           ("Q6-v", "Q6", "compraventas"), ("Q6-p", "Q6", "valor_tasado"), ("Q9-g", "Q9", "valor_tasado"),
           ("Q9-c", "Q9", "valor_tasado"), ("Q10-1", "Q10", "ipv"), ("Q10-2", "Q10", "ipc_alq"), ("Q10-3", "Q10", "compraventas")]
EXTRA21 = [("Qx1", "Q1", "serpavi"), ("Qx2", "Q2", "ipva"), ("Qx3", "Q3", "serpavi")]


def estructura_rejilla():
    d = pd.read_csv(C.RAIZ / "output" / "v16" / "potencia" / "rejilla_fija.csv")
    d = d[d.en_rejilla]
    return d.pregunta.values, d.resultado.values, (d.pregunta + "|" + d.escala).values


def estructura_disenos(n):
    lst = DISENOS + (EXTRA21 if n == 21 else [])
    return (np.array([x[1] for x in lst]), np.array([x[2] for x in lst]), np.array([x[1] for x in lst]))


def bh(p, q):
    m = len(p)
    o = np.argsort(p)
    ok = p[o] <= q * (np.arange(1, m + 1) / m)
    rej = np.zeros(m, bool)
    if ok.any():
        rej[o[: np.nonzero(ok)[0].max() + 1]] = True
    return rej


def by(p, q):
    m = len(p)
    return bh(p, q / np.sum(1.0 / np.arange(1, m + 1)))


def simes(p, factor=1.0):
    m = len(p)
    return min(1.0, factor * np.min(np.sort(p) * m / np.arange(1, m + 1)))


def jerarquico(p, fam, metodo):
    """Paso 1: p de familia (Simes) y selección de familias a q; paso 2: dentro de cada familia seleccionada, a q."""
    rej = np.zeros(len(p), bool)
    fams = np.unique(fam)
    f = len(fams)
    if metodo == "bh":
        pf = np.array([simes(p[fam == g]) for g in fams]); sel = bh(pf, Q); dentro = bh
    else:
        # BY: Simes con factor armónico por familia (válido bajo dependencia arbitraria) y BY en ambos pasos
        pf = np.array([simes(p[fam == g], np.sum(1.0 / np.arange(1, (fam == g).sum() + 1))) for g in fams]); sel = by(pf, Q); dentro = by
    for g, s in zip(fams, sel):
        if s:
            idx = np.nonzero(fam == g)[0]
            rej[idx] = dentro(p[idx], Q)
    return rej


def simular_z(rng, R, fam, res, esc, rho_r, rho_e, signos, nulos, mu):
    m = len(fam)
    ur, ue = np.unique(res), np.unique(esc)
    ir = np.searchsorted(ur, res); ie = np.searchsorted(ue, esc)
    a = rng.standard_normal((R, len(ur))); b = rng.standard_normal((R, len(ue)))
    s1 = rng.choice([-1.0, 1.0], m) if signos == "mixtos" else np.ones(m)
    s2 = rng.choice([-1.0, 1.0], m) if signos == "mixtos" else np.ones(m)
    z = np.sqrt(rho_r) * s1 * a[:, ir] + np.sqrt(rho_e) * s2 * b[:, ie] + np.sqrt(1 - rho_r - rho_e) * rng.standard_normal((R, m))
    nonnull = np.zeros((R, m), bool)
    if nulos == "global":
        pass
    elif nulos == "celdas_20":
        nonnull = rng.random((R, m)) < 0.20
    elif nulos == "familias":  # 40 % de las familias con 50 % de celdas no nulas, el resto nulas
        fu = np.unique(fam)
        activa = rng.random((R, len(fu))) < 0.4
        nonnull = activa[:, np.searchsorted(fu, fam)] & (rng.random((R, m)) < 0.5)
    z = z + mu * nonnull
    return z, nonnull


def evaluar(estructura, rho_r, rho_e, signos, nulos, R, k, bilateral=True, mu=3.0):
    fam, res, esc = estructura
    rng = C.rng(5, k)
    z, nn = simular_z(rng, R, fam, res, esc, rho_r, rho_e, signos, nulos, mu)
    p = 2 * stats.norm.sf(np.abs(z)) if bilateral else stats.norm.sf(z)
    out = {}
    for met in ("bh", "by"):
        fdp = np.empty(R); v1 = np.empty(R, bool); pw = np.full(R, np.nan)
        for r in range(R):
            rej = jerarquico(p[r], fam, met)
            V = (rej & ~nn[r]).sum(); Rr = rej.sum()
            fdp[r] = V / max(Rr, 1); v1[r] = V >= 1
            if nn[r].any():
                pw[r] = (rej & nn[r]).sum() / nn[r].sum()
        out[met] = (fdp.mean(), v1.mean(), np.nanmean(pw) if np.isfinite(pw).any() else np.nan)
    return out


def prds_empirico(estructura, rho_r, rho_e, signos, R, k, bilateral=True):
    """Compara P(p_j<=0,10 | p_i<=s) en pares nulos que comparten factor; debe crecer al bajar s (PRDS)."""
    fam, res, esc = estructura
    rng = C.rng(6, k)
    z, _ = simular_z(rng, R, fam, res, esc, rho_r, rho_e, signos, "global", 0.0)
    p = 2 * stats.norm.sf(np.abs(z)) if bilateral else stats.norm.sf(z)
    pares = [(i, j) for i in range(len(res)) for j in range(i + 1, len(res)) if res[i] == res[j] or esc[i] == esc[j]]
    sel = rng.choice(len(pares), size=min(150, len(pares)), replace=False)
    grilla = [0.5, 0.2, 0.1, 0.05, 0.02]
    viol = 0
    for t in sel:
        i, j = pares[t]
        cond = [(p[p[:, i] <= s, j] <= 0.10).mean() if (p[:, i] <= s).sum() > 30 else np.nan for s in grilla]
        cond = np.array(cond)
        # PRDS: la probabilidad debe ser no decreciente al bajar s; se tolera 0,03 por error de simulación
        if np.nanmin(np.diff(cond)) < -0.03:
            viol += 1
    return viol / len(sel)


def main(R=2000):
    est = {"rejilla_83": estructura_rejilla(), "disenos_18": estructura_disenos(18), "disenos_21": estructura_disenos(21)}
    corr = {"debil": (0.2, 0.1), "moderada": (0.4, 0.2), "fuerte": (0.7, 0.2)}
    filas = []
    k = 0
    for ne, es in est.items():
        for nc, (rr, re_) in corr.items():
            for sg in ("positivos", "mixtos"):
                for nu in ("global", "celdas_20", "familias"):
                    k += 1
                    o = evaluar(es, rr, re_, sg, nu, R, k)
                    for met in ("bh", "by"):
                        filas.append({"estructura": ne, "correlacion": nc, "signos": sg, "nulos": nu, "metodo": met,
                                      "FDR": o[met][0], "FWER": o[met][1], "potencia_celda": o[met][2]})
    # contraste: p-valores UNILATERALES con signos mixtos (dependencia negativa real): PRDS deja de valer
    for ne in ("rejilla_83",):
        for nu in ("global", "celdas_20", "familias"):
            k += 1
            o = evaluar(est[ne], 0.4, 0.2, "mixtos", nu, R, k, bilateral=False)
            for met in ("bh", "by"):
                filas.append({"estructura": ne + "_unilateral", "correlacion": "moderada", "signos": "mixtos", "nulos": nu, "metodo": met,
                              "FDR": o[met][0], "FWER": o[met][1], "potencia_celda": o[met][2]})
    t = pd.DataFrame(filas)
    prds = {f"{ne}|{sg}|{bil}": prds_empirico(est[ne], 0.4, 0.2, sg, 20000, 900 + i, bil == "bilateral")
            for i, (ne, sg, bil) in enumerate([("rejilla_83", "positivos", "bilateral"), ("rejilla_83", "mixtos", "bilateral"),
                                                ("rejilla_83", "mixtos", "unilateral"), ("disenos_18", "mixtos", "bilateral")])}
    bil = t[~t.estructura.str.contains("unilateral")]
    bh_ = bil[bil.metodo == "bh"]; by_ = bil[bil.metodo == "by"]
    max_bh, max_by = float(bh_.FDR.max()), float(by_.FDR.max())
    fwer_bh = float(bh_.FWER.max())
    if max_bh <= Q:
        glob = {"veredicto": "APTO (BH jerárquico)", "fallos": []}
    elif max_by <= Q:
        glob = {"veredicto": "NO APTO BH jerárquico; alternativa Benjamini-Yekutieli APTA", "fallos": [f"FDR máx. {max_bh:.4f} > {Q}"]}
    else:
        glob = {"veredicto": "NO APTO → diseño solo descriptivo", "fallos": [f"FDR máx. BH {max_bh:.4f}, BY {max_by:.4f} > {Q}"]}
    peor = bh_.loc[bh_.FDR.idxmax()].to_dict()
    r = C.resultado_base("bh_jerarquico", "Control de falsos descubrimientos (adenda punto 2)", {"celdas_rejilla": 83, "pruebas_disenos": [18, 21]},
                         "Simes por familia (q=0,10) + BH dentro; alternativa BY")
    r["estimacion"] = {"FDR_max_BH": max_bh, "FDR_max_BY": max_by, "FWER_max_BH": fwer_bh,
                       "FDR_media_BH": float(bh_.FDR.mean()), "FDR_max_BH_unilateral_signos_mixtos": float(t[t.estructura.str.contains("unilateral") & (t.metodo == "bh")].FDR.max()),
                       "potencia_media_BH": float(bh_.potencia_celda.mean()), "potencia_media_BY": float(by_.potencia_celda.mean())}
    r["diagnosticos"] = {"R": R, "q": Q, "cota_2q": 2 * Q, "escenario_peor_BH": peor, "violaciones_PRDS_empirico": prds, "veredicto": glob,
                         "criterio": "Para el control de FDR el criterio es FDR realizada <= q = 0,10 en todos los escenarios bilaterales declarados (el tamaño al 5 % no aplica)."}
    r["notas"] = ["La adenda lista 18 pruebas de diseños en el punto 3; el encargo decía 21: se simulan ambas (las 3 adicionales son hipotéticas).",
                  "Un tamaño/FDR de 0,0 no es relevante aquí: se informa también la potencia."]
    md = (f"## Resultados (R={R} réplicas por escenario)\n\n" + t.round(4).to_markdown(index=False)
          + f"\n\nViolaciones PRDS empíricas (proporción de pares): {prds}\n\n**Veredicto: {glob['veredicto']}** {'; '.join(glob['fallos'])}\n")
    C.escribir_salidas("bh_jerarquico", r, t, md)
    print(r["estimacion"], prds, glob)


if __name__ == "__main__":
    main(*[int(x) for x in sys.argv[1:]])
