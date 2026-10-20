"""V18 · Monte Carlo del F efectivo de Montiel Olea-Pflueger e intervalos Anderson-Rubin (una y dos endógenas). Simulación; sin datos reales.

Ejecución: python src/v18/montecarlo/iv_debil.py [--R 2000]   (SEED 20261010)

Proceso generador (declarado antes de simular)
- Panel de G = 39 clusters (provincias no selladas) x T = 14 años (n = 546), cluster por provincia. Constante parcializada.
- Instrumentos z_gtj = sqrt(0,5) zeta_gj + sqrt(0,5) xi_gtj (mitad de la varianza a nivel de cluster: exposición provincial).
- Perturbaciones (u, v1, v2): e_gt = sigma_g (sqrt(0,5) eta_g + sqrt(0,5) eps_gt), con eta y eps ~ N(0, S), S con correlaciones
  corr(u,v1) = 0,6; corr(u,v2) = 0,4; corr(v1,v2) = 0,3 (endogeneidad); sigma_g = exp(0,5 N(0,1)) normalizada a media 1 (heterogeneidad); la
  dependencia dentro del cluster es la mitad de la varianza (componente común). Dependencia transversal entre provincias: no hay
  (el cluster por provincia la ignora por diseño; la que existe es shift-share, ver bhj).
- Una endógena (p = 1, k = 1): x = pi z + v, pi en {0,03; 0,06; 0,1; 0,2; 0,5} (F efectivo medio de unos 2 a 150; se informa).
- Dos endógenas (p = 2, k = 2; E3-A4): x_j = s_j (z_j + 0,3 z_otro) + v_j, (s1, s2) en {(1; 1) fuertes, (1; 0,05) una débil, (0,06; 0,06) débiles}.
- y = beta x + u. Efecto nulo beta = 0; no nulo: delta = 0,5 por regresor. 2SLS y AR son equivariantes a la traslación de beta: la potencia
  es la tasa de rechazo de H0: beta = -delta con los datos de beta = 0; la cobertura del IC AR es 1 menos el tamaño.
- Inferencia: 2SLS con varianza por cluster G/(G-1), normal y t(G-1); AR con varianza por cluster (chi2; con p = 1 IC exacto, con p = 2 AR
  conjunto y AR de subvector por proyección en rejilla). Regla F efectivo >= 10: tamaño del 2SLS condicionado a esa regla.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[3]


def _H():
    """Carga la herramienta por ruta (mismo nombre de fichero que este script: no se puede importar por nombre)."""
    m = sys.modules.get("herr_iv_debil")
    if m is None:
        spec = importlib.util.spec_from_file_location("herr_iv_debil", RAIZ / "src" / "v18" / "herr18" / "iv_debil.py")
        m = importlib.util.module_from_spec(spec)
        sys.modules["herr_iv_debil"] = m
        spec.loader.exec_module(m)
    return m


SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "iv_debil"
ROTULO = "simulación; sin datos reales"
G, T = 39, 14
DELTA = 0.5
Z95 = 1.959964
TC = stats.t.ppf(0.975, G - 1)
SALIDA = RAIZ / "output" / "v18" / "montecarlo" / HERR
SIGMA = np.array([[1, .6, .4], [.6, 1, .3], [.4, .3, 1]])
CHOL = np.linalg.cholesky(SIGMA)


def veredicto(tam, cob, R, Rmin=1000):
    fallos = []
    if R < Rmin:
        fallos.append(f"R={R} < {Rmin}")
    if not (0.03 <= tam <= 0.08):
        fallos.append(f"tamaño {tam:.4f} fuera de [0,03; 0,08]")
    if not (0.92 <= cob <= 0.97):
        fallos.append(f"cobertura {cob:.4f} fuera de [0,92; 0,97]")
    return ("APTO" if not fallos else "NO APTO"), fallos


def banda_adenda(tam, cob):
    if tam > 0.15 or tam < 0.02:
        return "no fiable"
    if 0.04 <= tam <= 0.06 and 0.93 <= cob <= 0.97:
        return "apta"
    return "con valor crítico corregido"


def ic_bin(p, n):
    e = 1.96 * math.sqrt(max(p * (1 - p), 1e-12) / n)
    return [round(max(p - e, 0.0), 4), round(min(p + e, 1.0), 4)]


def dgp(rng, p, pi):
    k = p
    cl = np.repeat(np.arange(G), T)
    n = G * T
    sig = np.exp(0.5 * rng.standard_normal(G))
    sig /= sig.mean()
    zeta = rng.standard_normal((G, k))
    Z = math.sqrt(0.5) * zeta[cl] + math.sqrt(0.5) * rng.standard_normal((n, k))
    eta = rng.standard_normal((G, 3)) @ CHOL.T
    eps = rng.standard_normal((n, 3)) @ CHOL.T
    e = sig[cl][:, None] * (math.sqrt(0.5) * eta[cl] + math.sqrt(0.5) * eps)
    u, v = e[:, 0], e[:, 1:1 + p]
    if p == 1:
        X = pi[0] * Z[:, :1] + v
    else:
        X = np.column_stack([pi[0] * (Z[:, 0] + 0.3 * Z[:, 1]) + v[:, 0], pi[1] * (Z[:, 1] + 0.3 * Z[:, 0]) + v[:, 1]])
    y = u.copy()            # beta = 0
    return y, X, Z, cl


def rep_p1(rng, pi):
    H = _H()
    y, X, Z, cl = dgp(rng, 1, pi)
    y, X, Z, cl, g = H.preparar(y, X, Z, cl)
    F = H.f_efectivo(X, Z, cl, g)[0]
    b, V = H.dos_sls(y, X, Z, cl, g)
    se = float(np.sqrt(V[0, 0]))
    A, C = H.sumas_ar(y, X, Z, cl, g)
    ic = H.ar_ic_1(A, C, g)
    ac = not (ic[0] == "intervalo")
    largo = (ic[2] - ic[1]) if ic[0] == "intervalo" else np.nan
    rz0, rt0 = abs(b[0]) / se > Z95, abs(b[0]) / se > TC
    rzA, rtA = abs(b[0] + DELTA) / se > Z95, abs(b[0] + DELTA) / se > TC
    ra0 = not H.ar_en_ic_1(ic, 0.0)
    raA = not H.ar_en_ic_1(ic, -DELTA)
    return [b[0], se, F, rz0, rt0, ra0, rzA, rtA, raA, float(ac), largo]


def rep_p2(rng, pi):
    H = _H()
    y, X, Z, cl = dgp(rng, 2, pi)
    y, X, Z, cl, g = H.preparar(y, X, Z, cl)
    F = H.f_efectivo(X, Z, cl, g)
    b, V = H.dos_sls(y, X, Z, cl, g)
    se = float(np.sqrt(V[0, 0]))
    A, C = H.sumas_ar(y, X, Z, cl, g)
    p_conj0 = H.ar_p(A, C, np.zeros(2), g)
    p_conjA = H.ar_p(A, C, np.array([-DELTA, -DELTA]), g)
    p_sub0 = H.ar_subvector_p(A, C, g, 0.0)
    p_subA = H.ar_subvector_p(A, C, g, -DELTA)
    return [b[0], se, F.min(), abs(b[0]) / se > Z95, abs(b[0]) / se > TC, p_conj0 < 0.05, p_sub0 < 0.05,
            abs(b[0] + DELTA) / se > Z95, abs(b[0] + DELTA) / se > TC, p_conjA < 0.05, p_subA < 0.05]


def f_rep(rng, n, p, pi):
    fn = rep_p1 if p == 1 else rep_p2
    return np.array([fn(rng, pi) for _ in range(n)], dtype=float)


def paralelo(k, R, **kw):
    from joblib import Parallel, delayed
    base, extra = divmod(R, 40)
    tr = [base + (1 if i < extra else 0) for i in range(40)]
    res = Parallel(n_jobs=int(os.environ.get("V18_MC_JOBS", "4")))(delayed(f_rep)(np.random.default_rng([SEED, k, i]), n, **kw) for i, n in enumerate(tr) if n > 0)
    return np.vstack(res)


def _fila(esc, inf, rech0, rechA, R, extra=None, Rmin=1000):
    tam, pot = float(np.mean(rech0)), float(np.mean(rechA))
    d = {"escenario": esc["nombre"], "p": esc["p"], "inferencia": inf, "R": R, "tamano_5pct": tam, "tamano_ic95": str(ic_bin(tam, R)),
         "cobertura_95": 1.0 - tam, "potencia": pot, "principal": esc.get("principal", True)}
    d.update(extra or {})
    d["veredicto"] = veredicto(tam, 1.0 - tam, R, Rmin)[0]
    d["banda_adenda_1_12"] = banda_adenda(tam, 1.0 - tam)
    return d


def resumir(M, esc):
    R = len(M)
    F = M[:, 2]
    ex = {"F_eff_medio": float(F.mean()), "F_eff_mediana": float(np.median(F)), "prop_F_eff_ge_10": float((F >= 10).mean()),
          "sesgo_2sls_mediana": float(np.median(M[:, 0])), "rmse_2sls": float(np.sqrt(np.mean(M[:, 0] ** 2)))}
    filas = []
    if esc["p"] == 1:
        filas.append(_fila(esc, "2SLS (normal)", M[:, 3], M[:, 6], R, ex))
        filas.append(_fila(esc, "2SLS (t de Student, G-1)", M[:, 4], M[:, 7], R, ex))
        filas.append(_fila(esc, "AR (IC exacto por cluster)", M[:, 5], M[:, 8], R,
                           {**ex, "ic_ar_no_acotado": float(M[:, 9].mean()), "longitud_ar_mediana_acotados": float(np.nanmedian(M[:, 10])) if np.isfinite(M[:, 10]).any() else np.nan}))
        m = F >= 10
        if m.sum() >= 200:
            filas.append(_fila(esc, "2SLS (normal) | regla F efectivo >= 10", M[m, 3], M[m, 6], int(m.sum()), ex, Rmin=200))
        else:
            filas.append({"escenario": esc["nombre"], "p": 1, "inferencia": "2SLS (normal) | regla F efectivo >= 10", "R": int(m.sum()),
                          "veredicto": "n insuficiente (< 200 réplicas con F efectivo >= 10)", "principal": esc.get("principal", True), **ex})
    else:
        filas.append(_fila(esc, "2SLS beta_1 (normal)", M[:, 3], M[:, 7], R, ex))
        filas.append(_fila(esc, "2SLS beta_1 (t de Student, G-1)", M[:, 4], M[:, 8], R, ex))
        filas.append(_fila(esc, "AR conjunto (chi2, 2 gl)", M[:, 5], M[:, 9], R, ex))
        filas.append(_fila(esc, "AR de subvector beta_1 (proyección)", M[:, 6], M[:, 10], R, ex))
        m = F >= 10
        if m.sum() >= 200:
            filas.append(_fila(esc, "2SLS beta_1 (normal) | regla min F efectivo >= 10", M[m, 3], M[m, 7], int(m.sum()), ex, Rmin=200))
        else:
            filas.append({"escenario": esc["nombre"], "p": 2, "inferencia": "2SLS beta_1 (normal) | regla min F efectivo >= 10", "R": int(m.sum()),
                          "veredicto": "n insuficiente (< 200 réplicas con F efectivo >= 10)", "principal": esc.get("principal", True), **ex})
    return filas


ESCENARIOS = ([{"nombre": f"p=1, pi={pi}", "p": 1, "pi": (pi,)} for pi in (0.03, 0.06, 0.1, 0.2, 0.5)]
              + [{"nombre": "p=2, ambas fuertes (1; 1)", "p": 2, "pi": (1.0, 1.0)},
                 {"nombre": "p=2, una débil (1; 0,05)", "p": 2, "pi": (1.0, 0.05)},
                 {"nombre": "p=2, ambas débiles (0,06; 0,06)", "p": 2, "pi": (0.06, 0.06)}])


def main(R=2000, salida=SALIDA, esc=None):
    esc = esc or ESCENARIOS
    filas, brutos = [], {}
    for k, e in enumerate(esc):
        M = paralelo(k, R, p=e["p"], pi=e["pi"])
        filas += resumir(M, e)
        brutos[e["nombre"]] = M[:, [2, 3]].copy() if e["p"] == 1 else None
        print(e["nombre"], flush=True)
    tab = pd.DataFrame(filas)
    # tamaño del 2SLS (normal, p = 1) por tramo de F efectivo, réplicas agrupadas de los escenarios p = 1
    F = np.concatenate([v[:, 0] for v in brutos.values() if v is not None])
    rz = np.concatenate([v[:, 1] for v in brutos.values() if v is not None])
    tr = []
    for lo, hi in ((0, 5), (5, 10), (10, 23.1), (23.1, np.inf)):
        m = (F >= lo) & (F < hi)
        hi_s = "inf" if np.isinf(hi) else str(hi)
        tr.append({"escenario": f"tramo F efectivo [{lo}; {hi_s}) (p = 1, escenarios agrupados)", "p": 1, "inferencia": "2SLS (normal)", "R": int(m.sum()),
                   "tamano_5pct": float(rz[m].mean()) if m.sum() else np.nan, "principal": False,
                   "veredicto": "descriptivo (mezcla de escenarios)"})
    tab = pd.concat([tab, pd.DataFrame(tr)], ignore_index=True)
    escribir(tab, salida)
    return tab


def escribir(tab, salida):
    salida.mkdir(parents=True, exist_ok=True)
    tab.to_csv(salida / "tabla.csv", index=False)
    pr = tab[tab.principal & tab.tamano_5pct.notna() & ~tab.inferencia.str.contains(r"\|")]
    vg = {}
    for (p, inf), g in pr.groupby(["p", "inferencia"]):
        ok = g[g.veredicto == "APTO"]
        vg[f"p={p} · {inf}"] = {"veredicto": "APTO" if len(ok) == len(g) else ("NO APTO" if len(ok) == 0 else "APTO CONDICIONADO"),
                                "aptos": list(ok.escenario), "fallan": [f"{r.escenario} (tamaño {r.tamano_5pct:.4f})" for r in g[g.veredicto != "APTO"].itertuples()]}
    cond = tab[tab.inferencia.str.contains(r"\|") & ~tab.escenario.str.startswith("tramo")]
    vg["regla F efectivo >= 10 (2SLS condicionado)"] = {
        "veredicto": "APTO" if (cond.veredicto == "APTO").all() else "NO APTO",
        "detalle": {r.escenario: (None if pd.isna(getattr(r, "tamano_5pct", np.nan)) else round(float(r.tamano_5pct), 4)) for r in cond.itertuples()}}
    res = {"rama": "v18/montecarlo", "pregunta": "validación del F efectivo de MOP y de los IC de Anderson-Rubin (toda IV; E3-A4 con dos endógenas)",
           "capa": "validación de herramienta (sin capa de evidencia)", "datos": ROTULO, "N": f"{G} clusters x {T} años; p = 1 y p = 2",
           "metodo": "2SLS por cluster, F efectivo (MOP), AR exacto (p = 1) y AR conjunto/subvector (p = 2)",
           "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "no aplica (validación Monte Carlo)",
           "diagnosticos": {"veredicto_por_inferencia": vg, "R": int(tab[tab.principal].R.min()), "semilla": SEED,
                            "criterio": "tamaño [0,03; 0,08], cobertura [0,92; 0,97], R >= 2.000 (n >= 200 en filas condicionadas)",
                            "bandas_adenda_1_12": {f"{r.escenario} · {r.inferencia}": r.banda_adenda_1_12 for r in tab.itertuples()
                                                   if isinstance(getattr(r, "banda_adenda_1_12", None), str)},
                            "alcance_territorial": ALCANCE_TERRITORIAL},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": [ROTULO, "Cobertura = 1 - tamaño por equivariancia a la traslación de beta; potencia frente a delta = 0,5."]}
    (salida / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    cols = ["escenario", "inferencia", "R", "tamano_5pct", "cobertura_95", "potencia", "F_eff_medio", "prop_F_eff_ge_10", "veredicto", "banda_adenda_1_12"]
    md = ["# F efectivo (MOP) y Anderson-Rubin · Monte Carlo V18", "", f"**{ROTULO}.** SEED {SEED}.", "",
          "Proceso generador: ver el docstring de src/v18/montecarlo/iv_debil.py.", "", "## Resultados", "",
          tab[[c for c in cols if c in tab.columns]].round(4).to_markdown(index=False), "", "## Veredicto", ""]
    for k, v in vg.items():
        md.append(f"- **{k}: {v['veredicto']}.** " + (f"Aptos: {', '.join(v['aptos']) or 'ninguno'}. Fallan: {'; '.join(v['fallan']) or 'ninguno'}." if "aptos" in v else f"Tamaños: {v['detalle']}."))
    (salida / "informe.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    main(ap.parse_args().R)
