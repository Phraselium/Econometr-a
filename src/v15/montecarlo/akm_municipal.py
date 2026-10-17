"""V15 fase 4.1 · H4: shift-share municipal con inferencia AKM y AKM0, F efectivo y choques placebo.

Proceso generador declarado en docs/v15/validacion_montecarlo/akm_municipal.md ANTES de simular (el script lo escribe primero).
Uso: python src/v15/montecarlo/akm_municipal.py [--R 3000] [--jobs 4]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v15.montecarlo import _comun_v15 as C  # noqa: E402

HERR, K = "akm_municipal", 4
T = 11                      # diferencias anuales 2012-2022 (panel 2011-2022)
RHO_G, RHO_U, RHO_E = 0.5, 0.5, 0.3
SIG_Y, SIG_X = 0.05, 1.0
BETA_REF, BETA_MDE = 0.01, 0.008
Z = 1.959964
AGREG = {"Total", "Española", "Extranjera", "De Africa", "De América", "De Asia", "Europa (sin España)", "Oceanía y Apátridas",
         "País de Europa menos UE28", "País de la UE28 sin España"}
RESIDENCIALES = {"Alemania", "Francia", "Italia", "Portugal", "Reino Unido"}   # orígenes residenciales (adenda 1, punto 10: UE-14, RU, Suiza, Noruega) entre los 28
ESC = {  # nombre: (orígenes, fuerza de la primera etapa objetivo)
    "M1_28_origenes_F_alta": ("todos", "alta"),
    "M2_28_origenes_F_baja": ("todos", "baja"),
    "M3_instr_sin_residenciales_F_alta": ("sin_res", "alta"),
}

DGP = """# akm_municipal · H4: shift-share municipal con AKM y AKM0

Herramienta de V15 (preregistro_v15.md H4 y sección 6; adenda 1 puntos 8-10 y 13). Código: `src/v15/montecarlo/akm_municipal.py`; semilla `SeedSequence([20261010, 4, escenario*10+etapa]).spawn(trozos)` (trozos de 25 réplicas).

## Proceso generador (declarado antes de simular)
- **Estructura leída (sin valores de resultado):** municipios con SERPAVI en al menos 12 de los 14 años 2011-2024 y cuotas de nacionalidad del padrón de 2003 (28 nacionalidades individuales, sin agregados), cuotas s_ik = habitantes de la nacionalidad k / población total del municipio. N = el número resultante (≈ 1.452). Provincia = 2 primeros dígitos del código INE. T = 11 diferencias anuales (2012-2022).
- **Ecuación en diferencias anuales (adenda 1, punto 8):** y_it = β x_it + ε_it, con x_it = π z_it + v_it, z_it = c Σ_k s_ik g_kt (instrumento shift-share; c lo deja con desviación típica 1 tras restar la media de provincia × año). Efectos de municipio absorbidos por las diferencias; efectos de provincia × año por el centrado dentro de cada celda.
- **Choques de origen (placebo, independientes del resultado):** g_kt ~ N(0,1) independientes entre orígenes y AR(1) ρ = 0,5 en el tiempo (dependencia temporal arbitraria en la inferencia).
- **Errores con dependencia por cuota (el problema que AKM resuelve):** η_it = √0,4 A_it + √0,2 π_i f_t + √0,4 e_it, donde A_it = c Σ_k s_ik u_kt (choques de origen NO observados, independientes de g_kt, mismas cuotas, AR(1) ρ = 0,5), f_t = factor común AR(1) ρ = 0,7 con cargas π_i ~ N(0,1) (dependencia transversal que provincia × año no absorbe) y e_it AR(1) ρ = 0,3. ε = σ_y η^a (σ_y = 0,05 en puntos logarítmicos); v = σ_x (0,5 η^a + √0,75 η^b) con η^b independiente (endogeneidad de x: correlación 0,5), σ_x = 1.
- **Fuerza de la primera etapa:** π tal que la mediana del F efectivo (Montiel Olea-Pflueger con la varianza AKM de π̂, instrumento único) ≈ 30 en «F alta» y ≈ 4 en «F baja» (V9-D4 tuvo F de 2,8 a 4,6). Se calibra en una pasada previa con 100 réplicas y semilla propia.
- **Escenarios:** M1 (28 orígenes, F alta), M2 (28 orígenes, F baja, informativo), M3 (instrumento principal de la adenda 1 punto 10: sin orígenes residenciales (Alemania, Francia, Italia, Portugal, Reino Unido), 23 orígenes, F alta).
- **Nulo:** β = 0 (tamaño de los contrastes de β = 0). **Alternativa de referencia:** β = 0,01 (≈ 1 % de alquiler por desviación típica de x, orden de Saiz) para cobertura, sesgo, RMSE; potencia además con β = 0,008 (MDE80 del pre-registro).
- **Inferencias:** (a) AKM (Adão-Kolesár-Morales): varianza por origen con series temporales arbitrarias dentro del origen, normal; (b) AKM0: inversión del contraste con residuos bajo el nulo (equivalente en este caso exactamente identificado a Anderson-Rubin con la varianza de shocks); (c) error agrupado por provincia con t(40) solo como referencia del sobre-rechazo (no es candidato).
- **Estimador:** 2SLS exactamente identificado = cociente Σ z̃ỹ / Σ z̃x̃.
- **Criterio:** tamaño en [0,04; 0,06] con R = 3.000 y cobertura del IC95 en [0,92; 0,97] para la inferencia AKM; si no pasa, la alternativa nombrada en la adenda (punto 5) es Anderson-Rubin (AKM0). Un F efectivo ≥ umbral MOP (τ = 10 %, instrumento único) es condición de C3 de H4; aquí se reporta la distribución del F y el tamaño condicional a F ≥ 10 y a F ≥ 23,1 (valor orientativo; NO VERIFICADO).
"""


def estructura():
    d = pd.read_parquet(C.P15 / "p4_inmigracion.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable", "desagregacion", "valor"])
    s = d[(d.variable == "serpavi_alquiler_m2_mediana") & (d.nivel == "municipio") & d.periodo.between("2011", "2024")]
    n = s.groupby("territorio_codigo").periodo.nunique()
    cods = set(n[n >= 12].index.astype(str).str.zfill(5))
    p = d[(d.variable == "padron_municipal_nacionalidad") & (d.periodo == "2003")].copy()
    p["cod"] = p.territorio_codigo.astype(str).str.zfill(5)
    p = p[p.cod.isin(cods)]
    p["nac"] = p.desagregacion.str.replace("nacionalidad=", "", regex=False)
    pv = p.pivot_table(index="cod", columns="nac", values="valor", aggfunc="sum").fillna(0.0)
    tot = pv["Total"]
    orig = [c for c in pv.columns if c not in AGREG]
    ok = tot > 0
    pv, tot = pv[ok], tot[ok]
    S = pv[orig].div(tot, axis=0)
    S = S.sort_index()
    return S, orig


class Dis:
    """Diseño: cuotas, índice de celdas provincia y constante c."""

    def __init__(self, S: pd.DataFrame, orig: list[str], cols: list[str]):
        self.cods = list(S.index)
        self.prov = np.array([c[:2] for c in self.cods])
        self.cols = cols
        self.S = S[cols].to_numpy()
        up, self.starts, self.cnt = np.unique(self.prov, return_index=True, return_counts=True)
        self.n, self.K = self.S.shape
        # centrado dentro de provincia (por año): matriz de cuotas centradas
        Sc = self.dm_prov(self.S[None])[0]
        self.c = 1.0 / np.sqrt((Sc ** 2).sum(1).mean())
        w = self.S.sum(0) / self.S.sum()
        self.n_ef = float(1 / (w ** 2).sum())
        self.G = len(up)

    def dm_prov(self, a):
        """Resta la media de provincia en el eje 1 (unidades) de a: (..., n, ...) con unidades en el eje 1."""
        m = np.add.reduceat(a, self.starts, axis=1) / self.cnt.reshape((1, -1) + (1,) * (a.ndim - 2))
        return a - np.repeat(m, self.cnt, axis=1)


def _eta(g, D, nrep, wA=0.4, wf=0.2, we=0.4):
    n, K = D.S.shape
    u = C.ar1(g, nrep * K, T, RHO_U).reshape(nrep, K, T)
    A = D.c * np.einsum("ik,nkt->nit", D.S, u)
    f = C.ar1(g, nrep, T, 0.7)
    pi = g.standard_normal((nrep, n))
    e = C.ar1(g, nrep * n, T, RHO_E).reshape(nrep, n, T)
    return np.sqrt(wA) * A + np.sqrt(wf) * pi[:, :, None] * f[:, None, :] + np.sqrt(we) * e


def lote(g, nrep, D: Dis, pi_fs: float):
    K = D.K
    gk = C.ar1(g, nrep * K, T, RHO_G).reshape(nrep, K, T)
    z = D.c * np.einsum("ik,nkt->nit", D.S, gk)
    ea, eb = _eta(g, D, nrep), _eta(g, D, nrep)
    eps = SIG_Y * ea
    v = SIG_X * (0.5 * ea + np.sqrt(0.75) * eb)
    x = pi_fs * z + v
    return gk, z, x, eps


def estima(D: Dis, gk, z, x, y):
    zt, xt, yt = D.dm_prov(z), D.dm_prov(x), D.dm_prov(y)
    szx = (zt * xt).sum((1, 2))
    b = (zt * yt).sum((1, 2)) / szx
    # ingredientes AKM: a_kt = sum_i s_ik * resid_it  (resid centrado: sumas por celda nulas)
    Ay = np.einsum("ik,nit->nkt", D.S, yt)
    Ax = np.einsum("ik,nit->nkt", D.S, xt)
    Ak = (gk * D.c * Ay).sum(2)      # (n, K)  S_k(y)
    Bk = (gk * D.c * Ax).sum(2)
    SA, SB = Ak.sum(1), Bk.sum(1)
    se_akm = np.sqrt(((Ak - b[:, None] * Bk) ** 2).sum(1)) / np.abs(szx)
    # EE agrupado por provincia (referencia)
    res = yt - b[:, None, None] * xt
    sc = np.add.reduceat((zt * res).sum(2), D.starts, axis=1)
    se_cl = np.sqrt((sc ** 2).sum(1) * D.G / (D.G - 1)) / np.abs(szx)
    # primera etapa y F efectivo (varianza AKM de pi_hat)
    szz = (zt * zt).sum((1, 2))
    pih = szx / szz
    rx = xt - pih[:, None, None] * zt
    Ax_r = np.einsum("ik,nit->nkt", D.S, rx)
    Fk = (gk * D.c * Ax_r).sum(2)
    se_pi = np.sqrt((Fk ** 2).sum(1)) / szz
    Feff = (pih / se_pi) ** 2
    return b, se_akm, se_cl, SA, SB, Ak, Bk, Feff


def akm0_rechaza(SA, SB, Ak, Bk, b0):
    num = SA - b0 * SB
    return num ** 2 > Z ** 2 * ((Ak - b0 * Bk) ** 2).sum(1)


def akm0_ic(SA, SB, Ak, Bk):
    a2 = SB ** 2 - Z ** 2 * (Bk ** 2).sum(1)
    a1 = -2 * SA * SB + 2 * Z ** 2 * (Ak * Bk).sum(1)
    a0 = SA ** 2 - Z ** 2 * (Ak ** 2).sum(1)
    disc = a1 ** 2 - 4 * a2 * a0
    ok = (a2 > 0) & (disc >= 0)
    r = np.sqrt(np.where(ok, disc, 0.0))
    return np.where(ok, (-a1 - r) / (2 * a2), np.nan), np.where(ok, (-a1 + r) / (2 * a2), np.nan), a2 > 0


def trozo(g, nrep, D, pi_fs):
    gk, z, x, eps = lote(g, nrep, D, pi_fs)
    tc = stats.t.ppf(0.975, D.G - 1)
    out = []
    for beta in (0.0, BETA_REF, BETA_MDE):
        y = beta * x + eps
        b, se_a, se_c, SA, SB, Ak, Bk, F = estima(D, gk, z, x, y)
        rej_a = np.abs(b / se_a) > Z
        rej_c = np.abs(b / se_c) > tc
        rej_0 = akm0_rechaza(SA, SB, Ak, Bk, 0.0)
        cov_a = np.abs(b - beta) <= Z * se_a
        cov_c = np.abs(b - beta) <= tc * se_c
        cov_0 = ~akm0_rechaza(SA, SB, Ak, Bk, beta)
        lo, hi, acot = akm0_ic(SA, SB, Ak, Bk)
        out.append(np.column_stack([b, se_a, rej_a, rej_c, rej_0, cov_a, cov_c, cov_0, hi - lo, acot, F]).astype(float))
    return np.stack(out, 0)   # (3, nrep, 11)


def correr(D, pi_fs, R, etapa, esc_i, jobs, tam=25):
    nch = int(np.ceil(R / tam))
    gens = C.flujos(K, nch, esc_i * 10 + etapa)
    sal = Parallel(n_jobs=jobs)(delayed(trozo)(g, min(tam, R - i * tam), D, pi_fs) for i, g in enumerate(gens))
    return np.concatenate(sal, axis=1)[:, :R]


def calibra(D, F_obj, jobs):
    """π tal que mediana(F_eff) ≈ F_obj (búsqueda por bisección en log π, 100 réplicas, semilla propia)."""
    lo, hi = np.log(1e-4), np.log(100.0)
    for _ in range(14):
        m = (lo + hi) / 2
        g = np.random.default_rng([C.SEED, K, 777])
        F = np.median(trozo(g, 100, D, np.exp(m))[0, :, 10])
        lo, hi = (m, hi) if F < F_obj else (lo, m)
    return float(np.exp((lo + hi) / 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=3000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    C.declarar(HERR, DGP)
    S, orig = estructura()
    filas, info = [], {}
    for i, (esc, (orgs, fza)) in enumerate(ESC.items()):
        cols = [c for c in orig if not (orgs == "sin_res" and c in RESIDENCIALES)]
        D = Dis(S, orig, cols)
        pi_fs = calibra(D, 30.0 if fza == "alta" else 4.0, a.jobs)
        t0 = time.time()
        M = correr(D, pi_fs, a.R, 1, i, a.jobs)
        seg = time.time() - t0
        n0, nr, nm = M[0], M[1], M[2]
        F = n0[:, 10]
        info[esc] = {"N": D.n, "K": D.K, "provincias": D.G, "n_efectivo_choques": D.n_ef, "pi": pi_fs, "F_mediana": float(np.median(F)),
                     "F_p10": float(np.quantile(F, .1)), "F_p90": float(np.quantile(F, .9)), "prop_F_ge_10": float((F >= 10).mean())}
        for nm_, jr, jc in (("AKM", 2, 5), ("AKM0 (AR)", 4, 7), ("agrupado provincia t(40)", 3, 6)):
            tam = float(n0[:, jr].mean())
            cond10 = float(n0[F >= 10, jr].mean()) if (F >= 10).any() else np.nan
            cond23 = float(n0[F >= 23.1, jr].mean()) if (F >= 23.1).any() else np.nan
            e = nr[:, 0] - BETA_REF
            filas.append({"escenario": esc, "inferencia": nm_, "N": D.n, "K": D.K, "n_ef_choques": D.n_ef, "F_mediana": info[esc]["F_mediana"],
                          "R": a.R, "tamano_5pct": tam, "tamano_si_F>=10": cond10, "tamano_si_F>=23.1": cond23,
                          "cobertura_95": float(nr[:, jc].mean()), "potencia_beta_ref": float(nr[:, jr].mean()), "potencia_mde": float(nm[:, jr].mean()),
                          "sesgo": float(e.mean()), "rmse": float(np.sqrt((e ** 2).mean())), "acotado_AKM0": float(nr[:, 9].mean()) if nm_.startswith("AKM0") else np.nan,
                          "segundos": seg})
        print(esc, info[esc], round(seg), flush=True)
    tab = pd.DataFrame(filas)
    ver = {}
    for _, f in tab.iterrows():
        ver.setdefault(f.escenario, {})[f.inferencia] = C.veredicto(float(f.tamano_5pct), float(f.cobertura_95), int(f.R))
    glob = {}
    for esc, v in ver.items():
        if v["AKM"]["apto"]:
            glob[esc] = "APTO (AKM)"
        elif v["AKM0 (AR)"]["apto"]:
            glob[esc] = "alternativa APTA (AKM0/AR)"
        else:
            glob[esc] = "NO APTO → diseño solo descriptivo"
    p = tab[tab.escenario == "M1_28_origenes_F_alta"].set_index("inferencia")
    r = C.base_resultado("H4 (shift-share municipal, AKM / AKM0)", {"municipios": info["M1_28_origenes_F_alta"]["N"], "origenes": 28, "T": T, "provincias": info["M1_28_origenes_F_alta"]["provincias"]}, "2SLS exactamente identificado con inferencia AKM y AKM0")
    r["estimacion"] = {"tamano_AKM": float(p.loc["AKM", "tamano_5pct"]), "cobertura_AKM": float(p.loc["AKM", "cobertura_95"]),
                       "tamano_AKM0": float(p.loc["AKM0 (AR)", "tamano_5pct"]), "cobertura_AKM0": float(p.loc["AKM0 (AR)", "cobertura_95"]),
                       "tamano_agrupado": float(p.loc["agrupado provincia t(40)", "tamano_5pct"]),
                       "potencia_AKM": float(p.loc["AKM", "potencia_beta_ref"]), "potencia_AKM0": float(p.loc["AKM0 (AR)", "potencia_beta_ref"]),
                       "sesgo": float(p.loc["AKM", "sesgo"]), "rmse": float(p.loc["AKM", "rmse"])}
    r["ic95"] = C.ic_binomial(float(p.loc["AKM", "tamano_5pct"]), a.R)
    r["diagnosticos"] = {"veredicto_por_escenario": glob, "por_inferencia": ver, "estructura": info, "R": a.R, "semilla": C.SEED}
    r["notas"] = ["Veredicto global = escenario M1 (28 orígenes, F alta); M2 (F baja) es informativo; M3 es el instrumento principal de la adenda 1 punto 10.",
                  "El umbral MOP 23,1 (τ = 10 %, K = 1) está NO VERIFICADO; el pre-registro fija F ≥ 10 en el texto y τ = 10 % en la adenda."]
    md = (f"## Resultados (R = {a.R} por escenario; semilla {C.SEED}, k = {K})\n\n" + C.md_tabla(tab.drop(columns=["segundos"]), 4)
          + "\n**Estructura y primera etapa**\n\n" + "\n".join(f"- {e}: {i}" for e, i in info.items()) + "\n\n**Veredictos**\n\n"
          + "\n".join(f"- {e}: **{g}**" for e, g in glob.items()) + "\n\n")
    for e, v in ver.items():
        for nm, x in v.items():
            md += f"- {e} / {nm}: {x['veredicto']} {('— ' + '; '.join(x['fallos'])) if x['fallos'] else ''}\n"
    C.cerrar(HERR, r, tab, md)
    print(tab.to_string())
    print(glob)


if __name__ == "__main__":
    main()
