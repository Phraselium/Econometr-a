"""V9 F2 · addendum A1 al pre-registro: potencia recalculada tras la revisión (docs/v9/revision_f2.md), ANTES de
estimar ningún efecto. No usa la relación tratamiento-resultado de las unidades tratadas.

- D1a (hallazgo 2): simulación nula con los tamaños reales n_t/n_c. Residuos de un modelo de efectos fijos de unidad y
  trimestre ajustado SOLO con el periodo previo a las zonas tensionadas (2019T1-2023T4) para todas las unidades de la
  muestra; cada réplica toma, para cada unidad, un bloque contiguo de 16 trimestres de sus propios residuos; se estima
  CS con las cohortes reales. SE = DE de los ATT nulos (heterocedasticidad por unidad preservada).
- Familias de Holm con su m real (hallazgo 3): D1 m = 3, D2 m = 2, D4 m = 1.
- D2 (hallazgo 5): permutación de la dosis restringida dentro de cada provincia.
- D4 (hallazgos 4 y 5): error AKM con la nula impuesta (residuos de y sobre los controles, sin Z), controles
  pre-registrados incluidos; referencia de forma reducida = 0,01 × primera etapa estimada (la primera etapa no usa el
  resultado).
Salida: output/v9/potencia/mde_addendum.csv. SEED = 20261010.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import herramientas as H  # noqa: E402
import paneles as P  # noqa: E402

OUT = P.RAIZ / "output" / "v9" / "potencia"
B = 300
RNG = np.random.default_rng(P.SEED)
Z80 = stats.norm.ppf(0.80)


def mde(se, m):
    return (stats.norm.ppf(0.975) + Z80) * se, (stats.norm.ppf(1 - 0.05 / (2 * m)) + Z80) * se


def d1a() -> list[dict]:
    q = P.incasol("T")
    tr = P.tratamientos_cat()
    ley = set(tr[tr.ley11].cod)
    zt = tr.dropna(subset=["zt_t0"]).set_index("cod").zt_t0
    filas = []
    for var, nombre in (("renta_media", "log renta media"), ("contratos", "log contratos")):
        t_ini, t_fin = 2022 * 4 + 1, 2026 * 4
        W = q[(q.t >= t_ini) & (q.t <= t_fin)].pivot_table(index="cod", columns="t", values=var)
        W = W[(W > 0).all(1)].dropna()
        W = W[~(W.index.isin(ley) & ~W.index.isin(zt.index))]
        # 2019T1-2023T4: previo a la primera cohorte (re-revisión A1-a)
        pre = q[(q.t >= 2019 * 4) & (q.t <= 2023 * 4 + 3)].pivot_table(index="cod", columns="t", values=var)
        pre = np.log(pre[(pre > 0).all(1)].dropna())
        units = [c for c in W.index if c in pre.index]
        R = H.dm2(pre.loc[units].values)                        # residuos del modelo bidireccional (solo pre)
        g = np.array([zt[c] - t_ini if c in zt.index else np.inf for c in units], float)
        L = W.shape[1]
        maxs = R.shape[1] - L
        ats = []
        for _ in range(B):
            s = RNG.integers(0, maxs + 1, len(units))
            Y = np.stack([R[i, s[i]:s[i] + L] for i in range(len(units))])
            ats.append(H.cs(Y, g, B=2)["att"])
        se = float(np.std(ats, ddof=1))
        a, h = mde(se, 3)
        ref = 0.05 if var == "renta_media" else np.nan
        filas.append({"diseno": "D1a zonas tensionadas Cataluña", "resultado": nombre, "metodo": "simulación nula por bloques de residuos previos (n_t, n_c reales)",
                      "tratadas": int(np.isfinite(g).sum()), "controles": int((~np.isfinite(g)).sum()), "se": se, "mde_005": a,
                      "mde_holm": h, "m": 3, "referencia": ref,
                      "fuente_referencia": "LB01 (VERIFICADA, Q1): −4 % a −6 % (Ley 11/2020); contratos: sin fuente → exploratoria",
                      "confirmatorio": bool(var == "renta_media" and h <= ref)})
    return filas


def d2() -> list[dict]:
    a = P.incasol("A")
    h = P.hut_cat()
    h19 = h[h.anio == 2019].set_index("cod")
    dosis = 100 * h19.hut_plazas / h19.poblacion
    filas = []
    for var, nombre in (("renta_media", "log renta media"), ("contratos", "log contratos")):
        w = a[(a.anio >= 2014) & (a.anio <= 2025)].pivot_table(index="cod", columns="anio", values=var)
        w = np.log(w[(w > 0).all(1)].dropna())
        w = w[w.index.isin(dosis.dropna().index)]
        anios = np.array(w.columns)
        x = dosis.loc[w.index].values
        x = (x - x.mean()) / x.std()
        prov = np.array([c[:2] for c in w.index])
        y = H.dm2(w.values)
        res = []
        for _ in range(B):
            xp = x.copy()
            for p in np.unique(prov):
                m = prov == p
                xp[m] = RNG.permutation(x[m])
            X = np.column_stack([H.dm2(np.outer(xp, ((anios >= 2020) & (anios <= 2021)).astype(float))).ravel(),
                                 H.dm2(np.outer(xp, (anios >= 2022).astype(float))).ravel()])
            res.append(np.linalg.lstsq(X, y.ravel(), rcond=None)[0])
        sd = np.std(np.array(res), axis=0, ddof=1)
        for j, per in enumerate(("2020-2021", "2022-2025")):
            a5, ho = mde(float(sd[j]), 2)
            filas.append({"diseno": f"D2 HUT × COVID, {per}", "resultado": nombre + " por 1 DE de dosis",
                          "metodo": "permutación de la dosis dentro de provincia", "tratadas": len(w), "controles": 0,
                          "se": float(sd[j]), "mde_005": a5, "mde_holm": ho, "m": 2, "referencia": np.nan,
                          "fuente_referencia": "LA01 (VERIFICADA, Q1) no es convertible a estas unidades → exploratoria",
                          "confirmatorio": False})
    return filas


def d4() -> list[dict]:
    pp = P.padron_nac("provincia")
    pv = P.panel_prov()
    filas = []
    for (t0, t1, et) in ((2003, 2012, "réplica 2003-2012"), (2015, 2022, "ampliación 2015-2022")):
        s = P.construir(pp, t0, t1)
        d = s["d"]
        for col, nombre in (("ipc_alquiler_indice", "Δ log IPC de alquiler"), ("valor_tasado", "Δ log valor tasado")):
            serie = pv.pivot_table(index="cod_prov", columns="anio", values=col)
            y = np.log(serie[t1] / serie[t0]).reindex(d.index)
            m = y.notna() & d.notna().all(1)
            dd = d[m]
            Wm = np.column_stack([np.ones(m.sum()), dd[["lpop0", "suma_cuotas"]].values])
            def res(v):
                return v - Wm @ np.linalg.lstsq(Wm, v, rcond=None)[0]
            zt, xt, e0 = res(dd.Z.values), res(dd.x.values), res(y[m].values)   # e0: residuo con la nula impuesta
            pi = float(zt @ xt / (zt @ zt))
            sh = s["w"].loc[dd.index].values
            st = sh - Wm @ np.linalg.lstsq(Wm, sh, rcond=None)[0]
            Rc = (st * e0[:, None]).sum(0)
            se_akm0 = float(np.sqrt(np.sum(s["g"].values ** 2 * Rc ** 2)) / (zt @ zt))
            a5, ho = mde(se_akm0, 1)
            ref = 0.01 * pi
            conf = bool(et.startswith("réplica") and nombre.startswith("Δ log IPC") and ho <= ref)
            filas.append({"diseno": f"D4 shift-share ({et}), forma reducida", "resultado": nombre + " por punto de Z",
                          "metodo": "AKM con nula impuesta y controles", "tratadas": int(m.sum()), "controles": 0, "se": se_akm0,
                          "mde_005": a5, "mde_holm": ho, "m": 1, "referencia": ref,
                          "fuente_referencia": f"LA09 Saiz 2007 (VERIFICADA, Q1): 1 % por 1 % de población × primera etapa π = {pi:.3f}",
                          "confirmatorio": conf})
    return filas


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    t = pd.DataFrame(d1a() + d2() + d4())
    t.to_csv(OUT / "mde_addendum.csv", index=False, float_format="%.5f")
    with pd.option_context("display.width", 250, "display.max_columns", 12, "display.max_colwidth", 60):
        print(t[["diseno", "resultado", "tratadas", "controles", "se", "mde_holm", "referencia", "confirmatorio"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
