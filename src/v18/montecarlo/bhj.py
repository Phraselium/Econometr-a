"""V18 · Monte Carlo de BHJ a nivel de choque (bhj_lib.iv_cluster y ar_ic_nulo_impuesto). Simulación; sin datos reales.

Ejecución: python src/v18/montecarlo/bhj.py [--R 2000]   (SEED 20261010)

Proceso generador (declarado antes de simular)
- Unidades: 39 provincias no selladas (corte transversal, un periodo; diferencia larga como E3-R1/E9-R1), K choques
  (sectores) con K en {10, 20, 30}; HHI de los pesos de los choques en {0,1; 0,2; 0,3} (1/HHI = 10, 5, 3,3 efectivos;
  con K = 10 y HHI = 0,1 los pesos son iguales). Pesos geométricos con el HHI objetivo.
- Cuotas: s_lk = c_l q_lk, c_l ~ U(0,5; 0,95) (cuotas incompletas, sector «faltante» con choque 0, control: suma de cuotas),
  q_l ~ Dirichlet(10 omega). Pesos de provincia (aw) lognormales (sigma 0,7).
- Choques: g_k ~ N(0,1) i.i.d. (la aleatoriedad de BHJ). Instrumento z_l = sum_k s_lk g_k / sqrt(sum_k s_lk^2).
- x_l = pi z_l + v_l. Resultado: y_l = beta x_l + u_l, con u_l = 0,8 v_l + a-bar_l + e_l: a-bar_l = sum_k s_lk a_k / sqrt(sum s^2) con
  a_k ~ N(0,1) (confusores a nivel de sector, independientes de g), e_l = sqrt(0,5) eps_l + sqrt(0,5) phi_{r(l)} (4 regiones: dependencia
  transversal entre provincias). Endógeno: OLS sesgado, el IV es válido.
- Heterogeneidad: pesos de provincia lognormales; cuotas aleatorias. Pocos clusters: K clusters (sectores) de 10 a 30.
- Efecto nulo beta = 0; no nulo beta = 0,5. El IV y el IC de Anderson-Rubin con H0 impuesta son equivariantes a la
  traslación de beta: la potencia y la cobertura del caso no nulo se calculan con los mismos datos desplazando beta (se
  verifica en el test). pi = 1 (F de primera etapa a nivel de choque de unos 15-20) en el principal; pi = 0,25 (débil) y K = 200
  choques (referencia de calibración: con muchos choques el AR debe dar tamaño cercano a 0,05) como sensibilidades.
- Inferencia: IC normal con iv_cluster (ajuste G/(G-1)), t(G-1) y AR (ar_ic_nulo_impuesto, rango [-10, 10]; un IC no acotado
  en el rango cuenta como no rechazo y se informa).
"""
from __future__ import annotations

import argparse
import json
import os
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src" / "v18" / "herramientas"))
import bhj_inferencia as B  # noqa: E402

SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "bhj"
ROTULO = "simulación; sin datos reales"
L_PROV = 39
BETA_ALT = 0.5
Z = 1.959964
SALIDA = RAIZ / "output" / "v18" / "montecarlo" / HERR


def veredicto(tam, cob, R):
    """Criterio del encargo: tamaño en [0,03; 0,08], cobertura en [0,92; 0,97], R >= 2.000 (R >= 1.000 se declara)."""
    fallos = []
    if R < 1000:
        fallos.append(f"R={R} < 1.000")
    if not (0.03 <= tam <= 0.08):
        fallos.append(f"tamaño {tam:.4f} fuera de [0,03; 0,08]")
    if not (0.92 <= cob <= 0.97):
        fallos.append(f"cobertura {cob:.4f} fuera de [0,92; 0,97]")
    return ("APTO" if not fallos else "NO APTO"), fallos


def banda_adenda(tam, cob):
    """Bandas de 1.12 de la adenda."""
    if tam > 0.15 or tam < 0.02:
        return "no fiable"
    if 0.04 <= tam <= 0.06 and 0.93 <= cob <= 0.97:
        return "apta"
    return "con valor crítico corregido"


def ic_bin(p, n):
    e = 1.96 * math.sqrt(max(p * (1 - p), 1e-12) / n)
    return [round(max(p - e, 0.0), 4), round(min(p + e, 1.0), 4)]


def dgp_datos(rng, K, h, pi):
    omega = B.pesos_con_hhi(K, h)
    q = rng.dirichlet(10 * omega + 1e-9, size=L_PROV)
    c = rng.uniform(0.5, 0.95, L_PROV)
    s = q * c[:, None]
    w = np.exp(0.7 * rng.standard_normal(L_PROV))
    w = w / w.mean()
    g = rng.standard_normal(K)
    a = rng.standard_normal(K)
    nrm = np.sqrt((s ** 2).sum(1))
    z = (s @ g) / nrm
    abar = (s @ a) / nrm
    v = rng.standard_normal(L_PROV)
    reg = rng.integers(0, 4, L_PROV)
    phi = rng.standard_normal(4)[reg]
    e = math.sqrt(0.5) * rng.standard_normal(L_PROV) + math.sqrt(0.5) * phi
    x = pi * z + v
    u = 0.8 * v + abar + e
    return x, u, w, s, g


def una_rep(rng, K, h, pi):
    x, u, w, s, g = dgp_datos(rng, K, h, pi)
    r = B.bhj_choque(u, x, w, s, g, ar=True, rango=(-10.0, 10.0))   # y = 0*x + u (beta = 0)
    izq, der = r["ic_ar"] if r["ic_ar"] is not None else (np.nan, np.nan)
    return [r["beta"], r["se"], r["F1"], r["inv_hhi"], izq, der, float(r["inf_ar"])]


def f_rep(rng, n, K, h, pi):
    return np.array([una_rep(rng, K, h, pi) for _ in range(n)])


def paralelo(k, R, **kw):
    from joblib import Parallel, delayed
    base, extra = divmod(R, 40)
    tr = [base + (1 if i < extra else 0) for i in range(40)]
    res = Parallel(n_jobs=int(os.environ.get("V18_MC_JOBS", "4")))(delayed(f_rep)(np.random.default_rng([SEED, k, i]), n, **kw) for i, n in enumerate(tr) if n > 0)
    return np.vstack(res)


def resumir(M, K, h, pi, R):
    b, se, F1, ih, l, r, inf = (M[:, j] for j in range(7))
    G = K + 0   # clusters = sectores con cuota (el sector faltante forma un cluster más)
    tcrit = stats.t.ppf(0.975, G)   # G+1 clusters en iv_cluster (sector faltante incluido): gl = G
    filas = []

    def fila(nombre, rech_nulo, cubre_nulo, rech_alt, cubre_alt, extra=None):
        d = {"inferencia": nombre, "K": K, "HHI": h, "pi": pi, "R": R,
             "tamano_5pct": float(rech_nulo.mean()), "tamano_ic95": str(ic_bin(float(rech_nulo.mean()), R)),
             "cobertura_95": float(cubre_nulo.mean()), "potencia": float(rech_alt.mean()),
             "cobertura_alt": float(cubre_alt.mean()), "sesgo": float(np.mean(b)), "rmse": float(np.sqrt(np.mean(b ** 2))),
             "F1_medio": float(np.mean(F1)), "inv_hhi_realizado": float(np.mean(ih))}
        d.update(extra or {})
        tam, cob = d["tamano_5pct"], d["cobertura_95"]
        d["veredicto"] = veredicto(tam, cob, R)[0]
        d["banda_adenda_1_12"] = banda_adenda(tam, cob)
        filas.append(d)

    for nom, crit in (("iv_cluster (normal)", Z), ("iv_cluster (t de Student)", tcrit)):
        rn = np.abs(b) / se > crit
        cn = np.abs(b - 0.0) <= crit * se
        ra = np.abs(b + BETA_ALT) / se > crit
        ca = np.abs(b + BETA_ALT - BETA_ALT) <= crit * se
        fila(nom, rn, cn, ra, ca)
    nofin = np.isnan(l)
    cubre = nofin | ((l <= 0) & (0 <= r))
    rech = ~cubre
    pot = ~(nofin | ((l + BETA_ALT <= 0) & (0 <= r + BETA_ALT)))
    fila("AR (ar_ic_nulo_impuesto)", rech, cubre, pot, cubre, {"ic_ar_no_acotado": float(inf.mean()),
                                                                 "longitud_ar_mediana": float(np.nanmedian(r - l))})
    return filas


ESCENARIOS = ([{"K": K, "h": h, "pi": 1.0, "principal": True} for K in (10, 20, 30) for h in (0.1, 0.2, 0.3)]
              + [{"K": 20, "h": 0.2, "pi": 0.25, "principal": False},
                 {"K": 200, "h": 0.006, "pi": 1.0, "principal": False}])   # referencia de calibración (muchos choques)


def main(R=2000, escenarios=None, salida=SALIDA):
    esc = escenarios or ESCENARIOS
    filas = []
    for k, e in enumerate(esc):
        M = paralelo(k, R, K=e["K"], h=e["h"], pi=e["pi"])
        for f in resumir(M, e["K"], e["h"], e["pi"], len(M)):
            f["principal"] = e["principal"]
            filas.append(f)
        print(e, flush=True)
    tab = pd.DataFrame(filas)
    escribir(tab, R, salida)
    return tab


def _veredicto_global(tab):
    out = {}
    for inf, g in tab[tab.principal].groupby("inferencia"):
        ok = g[g.veredicto == "APTO"]
        out[inf] = {"veredicto": "APTO" if len(ok) == len(g) else ("NO APTO" if len(ok) == 0 else "APTO CONDICIONADO"),
                    "escenarios_aptos": [f"K={r.K}, HHI={r.HHI}" for r in ok.itertuples()],
                    "escenarios_no_aptos": [f"K={r.K}, HHI={r.HHI} (tamaño {r.tamano_5pct:.4f}, cobertura {r.cobertura_95:.4f})"
                                            for r in g[g.veredicto != "APTO"].itertuples()]}
    return out


def escribir(tab, R, salida):
    salida.mkdir(parents=True, exist_ok=True)
    tab.to_csv(salida / "tabla.csv", index=False)
    vg = _veredicto_global(tab)
    res = {"rama": "v18/montecarlo", "pregunta": "validación de BHJ a nivel de choque (E3, E5, E9)",
           "capa": "validación de herramienta (sin capa de evidencia)", "datos": ROTULO,
           "N": f"{L_PROV} provincias; K = 10, 20, 30 choques; HHI 0,1-0,3",
           "metodo": "ssaggregate + iv_cluster + ar_ic_nulo_impuesto (src/v18/reproduccion/bhj_lib.py)",
           "estimacion": None, "ic95": None, "p_ajustado": None,
           "nivel_evidencia": "no aplica (validación Monte Carlo)",
           "diagnosticos": {"veredicto_por_inferencia": vg, "R": int(tab.R.min()), "semilla": SEED,
                            "criterio": "tamaño [0,03; 0,08], cobertura [0,92; 0,97], R >= 2.000",
                            "bandas_adenda_1_12": {f"{r.inferencia} K={r.K} HHI={r.HHI} pi={r.pi}": r.banda_adenda_1_12
                                                   for r in tab.itertuples()},
                            "alcance_territorial": ALCANCE_TERRITORIAL},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": [ROTULO, "Cobertura y potencia del caso no nulo por equivariancia a la traslación de beta."]}
    (salida / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    cols = ["inferencia", "K", "HHI", "pi", "R", "tamano_5pct", "cobertura_95", "potencia", "F1_medio", "inv_hhi_realizado",
            "veredicto", "banda_adenda_1_12"]
    md = ["# BHJ a nivel de choque · Monte Carlo V18", "", f"**{ROTULO}.** SEED {SEED}, R = {int(tab.R.min())} por escenario.", "",
          "Proceso generador: ver el docstring de src/v18/montecarlo/bhj.py (39 provincias, K choques, HHI, cuotas incompletas, "
          "confusores sectoriales, dependencia entre provincias por 4 regiones).", "",
          "## Resultados", "", tab[cols].round(4).to_markdown(index=False), "", "## Veredicto", ""]
    for k, v in vg.items():
        md.append(f"- **{k}: {v['veredicto']}.** Aptos: {', '.join(v['escenarios_aptos']) or 'ninguno'}. "
                  f"Fallan: {'; '.join(v['escenarios_no_aptos']) or 'ninguno'}.")
    (salida / "informe.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    main(ap.parse_args().R)
