"""BD - descomposición por periodos (alquiler y compra), IC por bootstrap y contrafactuales. EXPLORATORIO."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bd_lib as L  # noqa: E402  (fija 1 hilo)

import warnings  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

warnings.filterwarnings('ignore')
PN = L.PNAMES
ETIQ_FAM = {"demografia": "demografía (pob 20-34 y extranjera)", "empleo_renta": "empleo (ocupados)",
            "credito_tipos_cu": "crédito/coste de uso", "oferta": "oferta (terminadas)",
            "politica": "política (tope de rentas CAT)", "comun_efectos_tiempo": "común / efectos de tiempo + FE",
            "residuo": "residuo"}


def decompone(d, mercado, modelo, B, seed, reg, smoke=False, provs=None, con_cf=True):
    s = L.muestra(d, mercado)
    if provs is not None:
        s = s[s["cod_prov"].isin(provs)]
    cfd = L.contrafactual_vars(d) if con_cf else {}
    if provs is not None:
        cfd = {k: v[v["cod_prov"].isin(provs)] for k, v in cfd.items()}
    P = L.Panel(s, mercado, modelo, cfd)
    beta, pt = P.corre()
    bc, betac = L.bootstrap(P, "cluster", B, seed)
    bt, betat = L.bootstrap(P, "tiempo", B, seed + 1)
    formula = (f"{L.YVAR[mercado]} ~ " + " + ".join(P.meta["col"]) +
               (" | FE prov + trim" if modelo == "M1" else " | FE prov + trim-del-año + interc. periodo"))
    reg.log("BD", f"{mercado}_{modelo}_descomposicion", formula, s["trimestre"].min(), s["trimestre"].max(), len(s),
            np.nan, np.nan, np.nan, np.nan, np.nan,
            f"EXPLORATORIO; ponderación por población; bootstrap cluster-provincia y bloques de tiempo (4) B={B} "
            f"seed={seed}; 2024Q2 excluido (población anulada por fuga)")
    # ---- coeficientes
    cf = P.meta.copy()
    cf["coef"] = beta
    cf["se_boot_cluster"] = betac.std(0, ddof=1)
    cf["ic95_cluster_inf"], cf["ic95_cluster_sup"] = L.ic(betac)
    cf["ic95_tiempo_inf"], cf["ic95_tiempo_sup"] = L.ic(betat)
    cf.insert(0, "mercado", mercado)
    cf.insert(1, "modelo", modelo)
    # ---- contribuciones
    comps = [k for k in pt if not k.startswith("cf__")]
    rows = []
    obs_pt = pt["observado"]
    VENT = {**{p: [i] for i, p in enumerate(PN)}, "P2-P4 (desde 2014)": [1, 2, 3], "P3-P4 (desde 2020)": [2, 3]}
    for k in comps:
        for p, ii in VENT.items():
            fs = lambda v: np.nansum(v[..., ii], -1)
            pe, ob = float(fs(pt[k])), float(fs(obs_pt))
            lo_c, hi_c = L.ic(fs(bc[k]))
            lo_t, hi_t = L.ic(fs(bt[k]))
            rows.append(dict(mercado=mercado, modelo=modelo, periodo=p, componente=k, contrib_pp=pe,
                             ic95_cluster_inf=lo_c, ic95_cluster_sup=hi_c, ic95_tiempo_inf=lo_t,
                             ic95_tiempo_sup=hi_t, ic95_inf=min(lo_c, lo_t), ic95_sup=max(hi_c, hi_t),
                             pct_observado=(100 * pe / ob if ob else np.nan) if k != "observado" else 100.0, observado_pp=ob))
    contrib = pd.DataFrame(rows)
    # ---- contrafactuales: efecto (pp acumulados, signo = cf - observado) por periodo y total
    rows = []
    for k in [k for k in pt if k.startswith("cf__")]:
        nm = k[4:]
        for ip, p in enumerate(PN + ["P2-P4 acumulado"]):
            def f(v):
                if ip < 4:
                    return v[..., ip]
                return v[..., 1:4].sum(-1)
            pe = f(pt[k])
            lo_c, hi_c = L.ic(f(bc[k]))
            lo_t, hi_t = L.ic(f(bt[k]))
            ob = f(obs_pt)
            rows.append(dict(mercado=mercado, modelo=modelo, escenario=nm, periodo=p, efecto_pp=pe,
                             ic95_cluster_inf=lo_c, ic95_cluster_sup=hi_c, ic95_tiempo_inf=lo_t,
                             ic95_tiempo_sup=hi_t, ic95_inf=min(lo_c, lo_t), ic95_sup=max(hi_c, hi_t),
                             observado_pp=ob, pct_observado=100 * pe / ob if ob else np.nan))
    cfdf = pd.DataFrame(rows)
    for nm in (sorted(cfdf["escenario"].unique()) if len(cfdf) else []):
        x = cfdf[(cfdf.escenario == nm) & (cfdf.periodo == "P2-P4 acumulado")].iloc[0]
        reg.log("BD", f"{mercado}_{modelo}_cf_{nm}", f"contrafactual parcial ceteris paribus sobre {mercado}_{modelo}",
                s["trimestre"].min(), s["trimestre"].max(), len(s), np.nan, np.nan, np.nan, np.nan, x["efecto_pp"], np.nan,
                f"EXPLORATORIO; efecto P2-P4 acumulado (pp) IC95 [{x['ic95_inf']:.3f}; {x['ic95_sup']:.3f}]; sin equilibrio general ni causalidad")
    # crecimiento observado en niveles (referencia, misma muestra): Σ_w[ln y(fin) - ln y(inicio-1)]
    return dict(contrib=contrib, coef=cf, cf=cfdf, n=len(s), G=P.G, T=P.T, panel=P)


def niveles_observados(d, mercado, provs=None):
    """Referencia: variación acumulada del ln nivel (media ponderada por población al inicio) en cada periodo."""
    lv = L.NIVEL_LEVEL[mercado]
    p = d.pivot(index="trimestre", columns="cod_prov", values=lv)
    w = d.pivot(index="trimestre", columns="cod_prov", values="pob_w")
    if provs is not None:
        p, w = p[provs], w[provs]
    out = {}
    for k, (a, b) in L.PERIODOS.items():
        b = min(b, L.Q_FIN_MUESTRA)
        ia = p.index.get_loc(a) - 1
        dl = p.loc[b] - p.iloc[ia]
        ww = w.iloc[ia]
        m = dl.notna() & ww.notna()
        out[k] = 100 * float((dl[m] * ww[m]).sum() / ww[m].sum())
    return out
