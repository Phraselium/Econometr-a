"""V9 F2 · potencia y efecto mínimo detectable (MDE) de los diseños D1-D5, ANTES de estimar ningún efecto.

Regla: ningún cálculo usa la relación entre tratamiento y resultado de las unidades tratadas.
- DiD (D1): placebos aleatorios SOLO entre unidades nunca tratadas en la ventana real (pseudo-tratados con la misma
  estructura de cohortes); el error estándar del diseño real se escala por sqrt((1/n_t + 1/n_c)/(1/k + 1/(m-k))).
- Dosis-respuesta (D2), diferencias largas (D3), shift-share (D4) y proyecciones locales (D5): inferencia por
  aleatorización, permutando la exposición (D2-D4) o el calendario de shocks por bloques (D5): la distribución
  resultante es la del estimador bajo la nula, no la estimación.
MDE (80 % de potencia, bilateral) = (z_{1-a/2} + z_{0,80}) × SE, con a = 0,05 y con a de Holm en el peor caso (a/m,
m = tamaño de la familia confirmatoria del diseño). Un diseño es confirmatorio solo si su MDE de Holm es menor o igual
que la magnitud de referencia de la literatura (docs/v9_prep/literatura.csv); si no, se estima como exploratorio (C4).
Salida: output/v9/potencia/mde.csv y resultado.json. SEED = 20261010.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paneles as P  # noqa: E402

OUT = P.RAIZ / "output" / "v9" / "potencia"
B = 300
RNG = np.random.default_rng(P.SEED)
Z80 = stats.norm.ppf(0.80)


def mde(se: float, m: int) -> tuple[float, float]:
    return (stats.norm.ppf(1 - 0.025) + Z80) * se, (stats.norm.ppf(1 - 0.05 / (2 * m)) + Z80) * se


def twfe_beta(y: np.ndarray, d: np.ndarray) -> float:
    """β de y_it = a_i + g_t + β d_it en panel balanceado (matrices unidades × periodos)."""
    def dm(x):
        return x - x.mean(1, keepdims=True) - x.mean(0, keepdims=True) + x.mean()
    dd = dm(d)
    return float((dd * dm(y)).sum() / (dd ** 2).sum())


def balanceado(df: pd.DataFrame, col: str, tcol: str, t_ini: int, t_fin: int) -> pd.DataFrame:
    d = df[(df[tcol] >= t_ini) & (df[tcol] <= t_fin) & df[col].notna() & (df[col] > 0)]
    w = d.pivot_table(index="cod", columns=tcol, values=col)
    return w.dropna()


def placebo_did(w: pd.DataFrame, pool: list[str], cohortes: list[tuple[int, int]], n_t: int, n_c: int) -> dict:
    """cohortes: [(tamaño real, posición del primer periodo tratado en la ventana)]."""
    pool = [c for c in pool if c in w.index]
    m = len(pool)
    tot = sum(s for s, _ in cohortes)
    k = min(tot, m // 2)
    tam = [max(1, round(s * k / tot)) for s, _ in cohortes]
    y = np.log(w.loc[pool].values)
    betas = []
    for _ in range(B):
        perm = RNG.permutation(m)
        d = np.zeros_like(y)
        ini = 0
        for (s, pos), n in zip(cohortes, tam):
            d[perm[ini:ini + n], pos:] = 1
            ini += n
        betas.append(twfe_beta(y, d))
    sd = float(np.std(betas, ddof=1))
    k = sum(tam)
    escala = np.sqrt((1 / n_t + 1 / n_c) / (1 / k + 1 / (m - k)))
    return {"se_placebo": sd, "se_escalado": sd * escala, "k_pseudo": k, "pool": m, "n_t": n_t, "n_c": n_c}


def ols_beta_se(y: np.ndarray, X: np.ndarray) -> np.ndarray:
    return np.linalg.lstsq(X, y, rcond=None)[0]


# ----------------------------------------------------------------------------------------------- D1
def d1() -> list[dict]:
    filas = []
    q = P.incasol("T")
    tr = P.tratamientos_cat()
    ley = set(tr[tr.ley11].cod)
    zt = tr.dropna(subset=["zt_t0"]).set_index("cod").zt_t0
    for var, nombre in (("renta_media", "log renta media de contratos nuevos"), ("contratos", "log contratos nuevos")):
        # D1a: zonas tensionadas de Cataluña, ventana 2022T2-2026T1 (16 trimestres)
        t_ini, t_fin = 2022 * 4 + 1, 2026 * 4 + 0
        w = balanceado(q, var, "t", t_ini, t_fin)
        trat = [c for c in w.index if c in zt.index]
        nunca = [c for c in w.index if c not in zt.index and c not in ley]
        coh = [(int((zt.loc[trat] == t0).sum()), int(t0 - t_ini)) for t0 in sorted(zt.loc[trat].unique())]
        r = placebo_did(w, nunca, coh, len(trat), len(nunca))
        a, h = mde(r["se_escalado"], 4)
        filas.append({"diseno": "D1a zonas tensionadas Cataluña (CS/BJS)", "resultado": nombre, "N_unidades": len(w),
                      "tratadas": len(trat), "controles": len(nunca), "periodos": w.shape[1], "se": r["se_escalado"],
                      "mde_005": a, "mde_holm": h, "m_familia": 4, "referencia": 0.05 if var == "renta_media" else 0.10,
                      "fuente_referencia": "LB01 (−4 % a −6 %, Ley 11/2020); LB03 Fedea (descriptivo)", **{k: r[k] for k in ("k_pseudo", "pool")}})
        # D1b: Ley 11/2020, ventana 2019T1-2022T1 (13 trimestres; primer trimestre tratado 2020T4)
        t_ini, t_fin = 2019 * 4 + 0, 2022 * 4 + 0
        w = balanceado(q, var, "t", t_ini, t_fin)
        trat = [c for c in w.index if c in ley]
        nunca = [c for c in w.index if c not in ley]
        r = placebo_did(w, nunca, [(len(trat), (2020 * 4 + 3) - t_ini)], len(trat), len(nunca))
        a, h = mde(r["se_escalado"], 4)
        filas.append({"diseno": "D1b Ley 11/2020 Cataluña (DiD, cohorte única)", "resultado": nombre, "N_unidades": len(w),
                      "tratadas": len(trat), "controles": len(nunca), "periodos": w.shape[1], "se": r["se_escalado"],
                      "mde_005": a, "mde_holm": h, "m_familia": 4, "referencia": 0.05 if var == "renta_media" else 0.10,
                      "fuente_referencia": "LB01 Jofre-Monseny, Martínez-Mazza y Segú (2023): −4 % a −6 %", **{k: r[k] for k in ("k_pseudo", "pool")}})
    # D1c: Euskadi (EMAL): recuento de unidades y trimestres posteriores; sin placebo (≤ 7 controles)
    e = P.emal()
    pv = P.tratamientos_pv().set_index("cod").zt_t0
    tmax = e.t.max()
    trat = sorted(set(e.cod) & set(pv.index))
    post = {c: int(max(0, tmax - pv[c] + 1)) for c in trat}
    filas.append({"diseno": "D1c zonas tensionadas Euskadi (EMAL)", "resultado": "log renta media / log contratos",
                  "N_unidades": e.cod.nunique(), "tratadas": len(trat), "controles": e.cod.nunique() - len(trat),
                  "periodos": int(e.t.nunique()), "se": np.nan, "mde_005": np.nan, "mde_holm": np.nan, "m_familia": 4,
                  "referencia": 0.05, "fuente_referencia": "LB01",
                  "nota": f"trimestres posteriores por municipio tratado: {post}; controles nunca tratados ≤ 7: sin potencia"})
    return filas


# ----------------------------------------------------------------------------------------------- D2
def d2() -> list[dict]:
    filas = []
    a = P.incasol("A")
    h = P.hut_cat()
    dosis = h[h.anio == 2019].assign(dosis=lambda x: 100 * x.hut_plazas / x.poblacion).set_index("cod").dosis
    for var, nombre in (("renta_media", "log renta media de contratos nuevos"), ("contratos", "log contratos nuevos")):
        w = balanceado(a.rename(columns={"anio": "anio_"}), var, "anio_", 2014, 2025)
        w = w[w.index.isin(dosis.index)]
        y = np.log(w.values)
        anios = np.array(w.columns)
        x = dosis.loc[w.index].values
        x = (x - x.mean()) / x.std()
        covid = ((anios >= 2020) & (anios <= 2021)).astype(float)
        reap = (anios >= 2022).astype(float)
        betas = []
        for _ in range(B):
            xp = RNG.permutation(x)
            b1 = twfe_beta(y, np.outer(xp, covid))
            b2 = twfe_beta(y, np.outer(xp, reap))
            betas.append((b1, b2))
        sd = np.std(np.array(betas), axis=0, ddof=1)
        for j, per in enumerate(("2020-2021 (COVID)", "2022-2025 (reapertura)")):
            a5, ho = mde(float(sd[j]), 4)
            filas.append({"diseno": f"D2 HUT × COVID Cataluña, {per}", "resultado": nombre + " por 1 DE de dosis",
                          "N_unidades": len(w), "tratadas": len(w), "controles": 0, "periodos": w.shape[1], "se": float(sd[j]),
                          "mde_005": a5, "mde_holm": ho, "m_familia": 4, "referencia": 0.019,
                          "fuente_referencia": "LA01 Garcia-López et al. (2020): +1,9 % barrio medio (Barcelona)"})
    return filas


# ----------------------------------------------------------------------------------------------- D3
def d3() -> list[dict]:
    f = P.fianzas_gva_cp()
    v = P.vut_gva_cp()
    viv = P.viviendas_cp()[["cp", "viviendas"]]
    w = f.pivot_table(index="cp", columns="anio", values=["fianzas", "fianza_media"])
    base = pd.DataFrame({"n24": w[("fianzas", 2024)], "n26": w[("fianzas", 2026)],
                         "m24": w[("fianza_media", 2024)], "m26": w[("fianza_media", 2026)]}).dropna()
    base = base[(base.n24 >= 20) & (base.n26 >= 20)].reset_index().merge(v, on="cp").merge(viv, on="cp")
    base = base[base.viviendas > 0]
    x = 100 * (base.vut_2026 - base.vut_2025) / base.viviendas
    x = ((x - x.mean()) / x.std()).values
    filas = []
    for col, nombre in (("m", "Δ log fianza media 2024→2026"), ("n", "Δ log número de fianzas 2024→2026")):
        y = np.log(base[f"{col}26"] / base[f"{col}24"]).values
        X1 = np.column_stack([np.ones(len(y)), x])
        bs = [ols_beta_se(y, np.column_stack([np.ones(len(y)), RNG.permutation(x)]))[1] for _ in range(B)]
        del X1
        sd = float(np.std(bs, ddof=1))
        a5, ho = mde(sd, 2)
        filas.append({"diseno": "D3 caída del registro VUT por CP (Comunitat Valenciana)", "resultado": nombre + " por 1 DE de ΔVUT/viviendas",
                      "N_unidades": len(y), "tratadas": len(y), "controles": 0, "periodos": 2, "se": sd, "mde_005": a5,
                      "mde_holm": ho, "m_familia": 2, "referencia": 0.019, "fuente_referencia": "LA01 (efecto medio de barrio, signo opuesto esperado)"})
    return filas


# ----------------------------------------------------------------------------------------------- D4
def instrumento(pn: pd.DataFrame, t0: int, t1: int) -> pd.DataFrame:
    """Shift-share de Card con crecimiento nacional leave-one-out por nacionalidad (sin Total, Española, Extranjera ni
    agregados continentales). Z_p = Σ_c (F_pc,t0 / F_c,t0) × ΔF_c,-p / Pop_p,t0 × 100 (puntos de población)."""
    excl = {"Total", "Española", "Extranjera"}
    pn = pn[~pn.nacionalidad.isin(excl) & ~pn.nacionalidad.str.startswith(("De ", "Europa", "País", "Oceanía"))]
    a = pn[pn.anio == t0].set_index(["cod_provincia", "nacionalidad"]).poblacion
    b = pn[pn.anio == t1].set_index(["cod_provincia", "nacionalidad"]).poblacion
    d = pd.DataFrame({"f0": a, "f1": b}).fillna(0).reset_index()
    nac = d.groupby("nacionalidad")[["f0", "f1"]].transform("sum")
    d["dF_loo"] = (nac.f1 - d.f1) - (nac.f0 - d.f0)
    d["F_loo0"] = nac.f0 - d.f0
    d["s"] = d.f0 / nac.f0
    return d


def d4() -> list[dict]:
    pp = P.padron_nac("provincia")
    tot = pp[pp.nacionalidad == "Total"].set_index(["anio", "cod_provincia"]).poblacion
    pv = P.panel_prov()
    vta = pv.set_index(["cod_prov", "anio"]).valor_tasado
    ipca = pv.set_index(["cod_prov", "anio"]).ipc_alquiler_indice
    filas = []
    for (t0, t1, etiqueta) in ((2003, 2012, "réplica 2003-2012"), (2015, 2022, "ampliación 2015-2022")):
        d = instrumento(pp, t0, t1)
        # Z_p: ΔF_{c,-p} × cuota s_pc, en puntos sobre la población de t0
        z = d.assign(zz=d.s * d.dF_loo).groupby("cod_provincia").zz.sum() / tot.loc[t0] * 100
        z = z[~z.index.isin(["51", "52"])]
        for serie, nombre in ((vta, "Δ log valor tasado"), (ipca, "Δ log IPC alquiler")):
            y = np.log(serie.xs(t1, level="anio") / serie.xs(t0, level="anio")).reindex(z.index).dropna()
            zz = z.loc[y.index].values
            bs = [ols_beta_se(y.values, np.column_stack([np.ones(len(y)), RNG.permutation(zz)]))[1] for _ in range(B)]
            sd = float(np.std(bs, ddof=1))
            a5, ho = mde(sd, 4)
            filas.append({"diseno": f"D4 shift-share inmigración ({etiqueta}), forma reducida", "resultado": nombre + " por 1 punto de Z",
                          "N_unidades": len(y), "tratadas": len(y), "controles": 0, "periodos": 2, "se": sd, "mde_005": a5,
                          "mde_holm": ho, "m_familia": 4, "referencia": 0.01, "fuente_referencia": "LA09 Saiz (2007): 1 % por 1 % de población; LA08 González y Ortega (2013)",
                          "nota": f"Z medio = {zz.mean():.2f} puntos, DE = {zz.std():.2f}"})
    return filas


# ----------------------------------------------------------------------------------------------- D5
def d5() -> list[dict]:
    eu = P.europa()
    jk = eu["jk"].copy()
    jk["q"] = pd.PeriodIndex(jk.periodo, freq="M").asfreq("Q").astype(str)
    shock_q = jk.groupby("q").MP_median.sum()
    rai = eu["rai"]
    expo = rai[(rai.periodo >= "2003-01") & (rai.periodo <= "2007-12")].groupby("pais").valor.mean()
    w = eu["bis"].pivot_table(index="territorio", columns="q", values="valor")
    paises = [p for p in P.ZONA_EURO if p in w.index and p in expo.index]
    w = w.loc[paises]
    cols = [c for c in w.columns if "2008Q1" <= c <= "2025Q3"]
    y = np.log(w[cols])
    e = ((expo.loc[paises] - expo.loc[paises].mean()) / expo.loc[paises].std()).values
    s = shock_q.reindex(cols).fillna(0).values
    filas = []
    for h in (4, 8):
        dy = (y.shift(-h, axis=1) - y.shift(1, axis=1)).iloc[:, 1:-h]
        ss = s[1:-h]
        def beta(sh):
            d = np.outer(e, sh)
            m = ~np.isnan(dy.values)
            yy = np.where(m, dy.values, np.nanmean(dy.values))
            return twfe_beta(yy, d)
        bs = []
        nb = 8
        for _ in range(B):
            bloques = [ss[i:i + nb] for i in range(0, len(ss), nb)]
            orden = RNG.permutation(len(bloques))
            bs.append(beta(np.concatenate([bloques[i] for i in orden])[:len(ss)]))
        sd = float(np.std(bs, ddof=1))
        a5, ho = mde(sd, 2)
        filas.append({"diseno": f"D5 proyección local precios (BIS), h = {h} trimestres", "resultado": "Δ log HPI por shock JK × 1 DE de exposición",
                      "N_unidades": len(paises), "tratadas": len(paises), "controles": 0, "periodos": len(ss), "se": sd,
                      "mde_005": a5, "mde_holm": ho, "m_familia": 2, "referencia": 0.05,
                      "fuente_referencia": "LA25 Koeniger et al. (2022), cualitativo; referencia de orden de magnitud NO VERIFICADA: 5 % de precio por 1 pp de shock y 1 DE de exposición (la mitad de una respuesta media de −10 %/pp)",
                      "nota": f"DE del shock trimestral = {s.std():.3f}; MDE en unidades de shock (1 = 1 unidad JK)"})
    return filas


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    filas = d1() + d2() + d3() + d4() + d5()
    t = pd.DataFrame(filas)
    t["confirmatorio"] = np.where(t.referencia.notna() & t.mde_holm.notna(), t.mde_holm <= t.referencia, False)
    t.to_csv(OUT / "mde.csv", index=False, float_format="%.5f")
    res = {"rama": "v9/f2_potencia", "pregunta": "¿Qué diseños tienen potencia para un contraste confirmatorio?",
           "capa": "—", "datos": "Incasòl, EMAL, IDESCAT, GVA, padrón, MIVAU, INE, BCE, Eurostat", "N": int(t.N_unidades.sum()),
           "metodo": "placebos entre nunca tratados y permutaciones de la exposición (B = 300, SEED = 20261010)",
           "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "—",
           "diagnosticos": t[["diseno", "resultado", "mde_holm", "referencia", "confirmatorio"]].to_dict("records"),
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "No usa la relación tratamiento-resultado de las unidades tratadas."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    with pd.option_context("display.width", 250, "display.max_columns", 20):
        print(t[["diseno", "resultado", "N_unidades", "tratadas", "se", "mde_005", "mde_holm", "referencia", "confirmatorio"]])
    return 0


if __name__ == "__main__":
    sys.exit(main())
