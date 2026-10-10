"""C3 / P-C3: topes de la Ley 11/2020 (H3-3a renta, H3-3b contratos) con fianzas Incasòl y validación sellada por fuente
(SERPAVI municipal). Determinista y sin red. Uso: python src/v3/c3_run.py [--smoke]
Si existen output/v3/C3/sellado_H3-3a.json y sellado_H3-3b.json se leen y NO se reevalúa (una apertura por hipótesis).
--smoke: submuestra, pocas réplicas, test en seco de fn y NINGUNA apertura sellada."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c3_data as dat  # noqa: E402
import c3_est as E  # noqa: E402

import holdout  # noqa: E402
from econ_utils import Registry  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUT = dat.RAIZ / "output/v3/C3" / ("smoke" if SMOKE else "")
OUT_REAL = dat.RAIZ / "output/v3/C3"
OUT.mkdir(parents=True, exist_ok=True)
REPS = 99 if SMOKE else 999
REPS_EMD = 100 if SMOKE else 500
EER = {"alq": 0.03, "n": 0.10}
Y_ = {"alq": "lnalq", "n": "lnn"}
HIP = {"alq": "H3-3a", "n": "H3-3b"}
TARGET = {"alq": -0.045, "n": -0.003}
reg = Registry(OUT / "registro.csv")
rng_s = np.random.default_rng(E.SEED)
T0, BASE, END_MAIN, END_ALT, TMAX = 8, 7, 13, 11, 20     # t=1 es 2019Q1; 2020Q4=8; 2022Q1=13; 2021Q3=11; 2023Q4=20
ANIOS_PRE, ANIOS_POST = (2018, 2019), (2021, 2022)


def qlab(t):
    return f"{2019 + (t - 1) // 4}Q{(t - 1) % 4 + 1}"


def pct(b):
    return 100 * (np.exp(b) - 1)


def log_reg(modelo, formula, n, b, p, notas, ini="2019Q1", fin="2023Q4"):
    reg.log("C3", modelo, formula, ini, fin, int(n), np.nan, np.nan, np.nan, coef_interes=float(b), p_interes=float(p), notas=notas)


# ------------------------------------------------------------------ contexto de datos (entrenamiento)
def contexto():
    tr = dat.construir_y_sellar()          # pasos 1-2: fianzas -> sellar_v3; SERPAVI -> sellar_fuente_v3 (sin mirar)
    c = pd.read_csv(dat.D / "cataluna_contencion_rentas_v3.csv", dtype=str)
    l11 = set(c[c.regimen == "ley11_2020"].cod_ine.str.zfill(5))
    pop = dat.poblacion_censo2021()
    tr = tr.copy()
    tr["lnalq"], tr["lnn"] = np.log(tr.alq), np.log(tr.n)
    q = tr[tr.freq == "Q"].copy()
    q["t"] = (q.anio - 2019) * 4 + q.q
    a = tr[tr.freq == "A"].copy()
    muni = sorted(tr.cod_ine.unique())
    if SMOKE:
        sel = set(rng_s.choice(muni, size=len(muni) // 3, replace=False)) | (l11 & set(muni))
        q, a = q[q.cod_ine.isin(sel)], a[a.cod_ine.isin(sel)]
    # mercado tenso: crecimiento anual compuesto de la renta de fianzas 2014-2019 >= 4,15 % (proxy; JMS usan el suyo)
    r = a.pivot(index="cod_ine", columns="anio", values="alq")
    g = (r[2019] / r[2014]) ** (1 / 5) - 1
    gr = pd.DataFrame({"sujeto": [m in l11 for m in muni]}, index=muni)
    gr["pop"] = pop.reindex(gr.index)
    gr["tenso"] = (g.reindex(gr.index) >= 0.0415)
    return tr, q, a, gr, l11


def bal_q(q, tmax):
    k = q[q.t <= tmax].groupby("cod_ine").t.nunique()
    return k[k == tmax].index


def wide_q(q, var, units, tmax):
    w = q[q.cod_ine.isin(units)].pivot(index="cod_ine", columns="t", values=var)
    return w.reindex(index=units, columns=range(1, tmax + 1))


def seleccion(gr, units, ctrl, excl_bcn=True, extra_excl=()):
    """Devuelve (índice ordenado, vector tratado). Tratados = sujetos de la lista oficial."""
    g = gr.reindex(units)
    tr = g.sujeto.values
    nc = ~tr
    if ctrl == "pop20k":
        nc = nc & (g["pop"].values >= 20000)
    elif ctrl == "tenso20k":
        nc = nc & (g["pop"].values < 20000) & g.tenso.values
    keep = tr | nc
    if excl_bcn:
        keep &= (np.asarray(units) != "08019")
    if len(extra_excl):
        keep &= ~np.isin(np.asarray(units), list(extra_excl))
    idx = pd.Index(np.asarray(units)[keep])
    return idx, g.sujeto.values[keep]


# ------------------------------------------------------------------ SERPAVI anual: mismo diseño
def did_anual(df, col, treated, controls, anios_pre=ANIOS_PRE, anios_post=ANIOS_POST):
    """DiD anual: Δ_i = media(y en post) - media(y en pre); tratados frente a controles; Welch + t(n-2). y en logs.
    Solo municipios con todos los años y valores > 0."""
    d = df[df.cod_ine.isin(set(treated) | set(controls)) & df.anio.isin(anios_pre + anios_post)]
    w = d.pivot(index="cod_ine", columns="anio", values=col)
    w = w.reindex(columns=list(anios_pre + anios_post)).dropna()
    w = w[(w > 0).all(axis=1)]
    y = np.log(w)
    delta = (y[list(anios_post)].mean(axis=1) - y[list(anios_pre)].mean(axis=1)).values
    tr = np.isin(w.index, list(treated))
    if tr.sum() < 3 or (~tr).sum() < 3:
        return dict(b=np.nan, se=np.nan, p=np.nan, ic=(np.nan, np.nan), nT=int(tr.sum()), nC=int((~tr).sum()))
    th, se = E.welch_t(delta, tr)
    n = len(delta)
    h = stats.t.ppf(.975, n - 2) * se
    return dict(b=float(th), se=float(se), p=float(2 * stats.t.sf(abs(th / se), n - 2)), ic=(float(th - h), float(th + h)),
                nT=int(tr.sum()), nC=int((~tr).sum()), idx=list(w.index), delta=delta, tr=tr)


def make_fn(clave, treated, controls, rent_ref):
    """fn para evaluate_v3: la MISMA especificación anual (pre 2018-2019, post 2021-2022, 2020 excluido) en SERPAVI.
    clave: 'alq' (H3-3a) o 'n' (H3-3b)."""
    col = {"alq": "alq", "n": "n_viv"}[clave]

    def fn(sellado):
        s = sellado["c3_serpavi"].copy()
        s["cod_ine"] = s.cod_ine.astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(5)
        s["anio"] = pd.to_numeric(s.anio).astype(int)
        s[col] = pd.to_numeric(s[col], errors="coerce")
        r = did_anual(s, col, treated, controls)
        b, se = r["b"], r["se"]
        res = dict(hipotesis=HIP[clave], resultado=col, diseno="DiD anual; Δ = media(2021-2022) - media(2018-2019); 2020 excluido",
                   beta=b, se=se, ic95=list(r["ic"]), p_dos_colas=r["p"],
                   p_una_cola_neg=float(stats.t.cdf(b / se, r["nT"] + r["nC"] - 2)) if se > 0 else None,
                   pct=float(pct(b)), pct_ic95=[float(pct(r["ic"][0])), float(pct(r["ic"][1]))],
                   nT=r["nT"], nC=r["nC"])
        if clave == "alq":
            res["eur_mes"] = float(pct(b) / 100 * rent_ref)
            res["eur_mes_ic95"] = [float(pct(r["ic"][0]) / 100 * rent_ref), float(pct(r["ic"][1]) / 100 * rent_ref)]
        return res
    return fn


def estructura_serpavi(col, treated, controls):
    """SOLO la estructura (qué municipios tienen los 4 años con dato), sin valores: se usa para N y potencia."""
    s = dat.serpavi_cat()
    s = s[s.cod_ine.isin(set(treated) | set(controls)) & s.anio.isin(ANIOS_PRE + ANIOS_POST)]
    ok = s.assign(v=s[col].notna() & (s[col] > 0)).groupby("cod_ine").v.sum()
    return set(ok[ok == 4].index)


class shim_pandas3:
    """evaluate_v3 usa DataFrame.apply(pd.to_numeric, errors='ignore'), que pandas 3 ya no admite (ValueError
    'invalid error value specified' DESPUÉS de registrar la apertura). Se sustituye SOLO durante la llamada, en memoria;
    src/holdout.py no se modifica."""

    def __enter__(self):
        self.orig = pd.DataFrame.apply
        orig = self.orig

        def ap(df, func, *a, **k):
            if func is pd.to_numeric and k.get("errors") == "ignore":
                out = df.copy()
                for c in out.columns:
                    try:
                        out[c] = pd.to_numeric(out[c])
                    except (ValueError, TypeError):
                        pass
                return out
            return orig(df, func, *a, **k)
        pd.DataFrame.apply = ap
        return self

    def __exit__(self, *x):
        pd.DataFrame.apply = self.orig


def dry_run(fn, muni_train, tag):
    """Test en seco de fn con un panel sintético de la misma forma, a través de evaluate_v3 con rutas de ensayo
    (el registro real de accesos no se toca)."""
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="c3_dry_"))
    rr = np.random.default_rng(E.SEED)
    filas = [(m, y, float(np.exp(rr.normal(2.2, .3))), float(np.exp(rr.normal(5, 1)))) for m in muni_train for y in range(2018, 2024)]
    syn = pd.DataFrame(filas, columns=["cod_ine", "anio", "alq", "n_viv"])
    syn.loc[rr.choice(len(syn), 20, replace=False), "alq"] = np.nan
    old = (holdout.SEALED, holdout.LOG, holdout.LOG_MD)
    try:
        holdout.SEALED, holdout.LOG, holdout.LOG_MD = tmp, tmp / "_accesos.log", tmp / "accesos.md"
        holdout.sellar_fuente_v3(syn, "c3_serpavi")
        with shim_pandas3():
            r = holdout.evaluate_v3(f"DRY-{tag}", fn, "C3-dry", ["c3_serpavi"])
    finally:
        holdout.SEALED, holdout.LOG, holdout.LOG_MD = old
    json.dumps(r)
    return r


# ------------------------------------------------------------------ principal
def main():
    tr_all, q, a, gr, l11 = contexto()
    desv = []
    units_all = bal_q(q, TMAX)
    W = {k: wide_q(q, Y_[k], units_all, TMAX) for k in Y_}
    Wlev = wide_q(q, "alq", units_all, TMAX)
    Wn = wide_q(q, "n", units_all, TMAX)
    res = {"meta": dict(muni_entrenamiento=int(tr_all.cod_ine.nunique()), balanceadas_2019Q1_2023Q4=int(len(units_all)),
                        sujetos_en_entrenamiento=int(sum(m in l11 for m in tr_all.cod_ine.unique())))}

    def sub(k, ctrl="todos", excl=True, tmax=TMAX, extra=()):
        idx, tr = seleccion(gr, units_all, ctrl, excl, extra)
        Y = W[k].loc[idx].values[:, :tmax]
        return idx, tr, Y

    # ---------- referencia de magnitudes: renta y contratos medios de los tratados en el periodo previo
    idx0, tr0, _ = sub("alq")
    rent_ref = float(Wlev.loc[idx0[tr0]].iloc[:, :BASE].values.mean())
    n_ref = float(Wn.loc[idx0[tr0]].iloc[:, :BASE].values.mean())
    res["meta"].update(rent_ref_eur_mes=rent_ref, contratos_trim_por_muni_ref=n_ref, nT=int(tr0.sum()), nC=int((~tr0).sum()))

    # ---------- 3. POTENCIA (P2): antes de estimar
    treated_tr = set(idx0[tr0])
    controls_tr = set(idx0[~tr0])
    pot = []
    for k in Y_:
        idx, tr, Y = sub(k)
        d = E.delta_cs(Y, BASE - 1, list(range(T0 - 1, END_MAIN)))
        e = E.emd_cs(d, tr, REPS_EMD)
        pot.append(dict(hipotesis=HIP[k], especificacion="CS trimestral 2019Q1-2022Q1 (pre 7, post 6)", N=int(len(d)),
                        clusters=e["G"], ee=e["ee"], emd_t=e["emd_t"], emd_wcb=e["emd_wcb"], emd=e["emd"], eer=EER[k],
                        veredicto="estimable" if e["emd"] <= EER[k] else "no detectable"))
        # validación SERPAVI: estructura (N) de SERPAVI, varianza = la de las fianzas anuales (aproximación declarada)
        col = {"alq": "alq", "n": "n_viv"}[k]
        ok = estructura_serpavi(col, treated_tr, controls_tr)
        fa = a.copy()
        r = did_anual(fa[fa.cod_ine.isin(ok)], {"alq": "alq", "n": "n"}[k], treated_tr & ok, controls_tr & ok)
        if np.isfinite(r["b"]):
            e2 = E.emd_cs(r["delta"], r["tr"], REPS_EMD)
            pot.append(dict(hipotesis=HIP[k], especificacion="Validación SERPAVI anual (estructura SERPAVI, varianza de fianzas anuales)",
                            N=int(len(r["delta"])), clusters=e2["G"], ee=e2["ee"], emd_t=e2["emd_t"], emd_wcb=e2["emd_wcb"],
                            emd=e2["emd"], eer=EER[k], veredicto="estimable" if e2["emd"] <= EER[k] else "no concluyente (EMD > EER)"))
        else:
            pot.append(dict(hipotesis=HIP[k], especificacion="Validación SERPAVI anual", N=0, clusters=0, ee=np.nan, emd_t=np.inf,
                            emd_wcb=np.inf, emd=np.inf, eer=EER[k], veredicto="no concluyente (sin estructura)"))
    pot = pd.DataFrame(pot)
    pot.to_csv(OUT / "potencia_c3.csv", index=False)
    for r_ in pot.itertuples():
        reg.log("C3", f"POT:{r_.hipotesis}:{r_.especificacion[:30]}", "EMD=max(t(G-1), WCB)", "2019", "2023", r_.N, np.nan, np.nan,
                np.nan, coef_interes=r_.emd, notas=f"EMD (no coeficiente) vs EER={r_.eer}: {r_.veredicto}")
    res["potencia"] = pot.to_dict("records")
    pot_ok = {k: bool(pot[(pot.hipotesis == HIP[k])].iloc[0].emd <= EER[k]) for k in Y_}
    val_ok = {k: bool(pot[(pot.hipotesis == HIP[k])].iloc[-1].emd <= EER[k]) for k in Y_}
    if SMOKE:   # la submuestra no tiene potencia: se fuerza solo para recorrer el código
        pot_ok, val_ok = {k: True for k in Y_}, {k: True for k in Y_}
    res["potencia_ok"], res["potencia_validacion_ok"] = pot_ok, val_ok
    print(pot.round(4).to_string())

    # ---------- 4. RÉPLICA JMS 2023
    rep = []

    def clasifica(ic, T, n_t, n_c):
        if n_t < 10 or n_c < 10:
            return "NO REPLICABLE", "muestra insuficiente"
        lo, hi = ic
        contiene_T, contiene_0 = lo <= T <= hi, lo <= 0 <= hi
        if contiene_T and not contiene_0:
            return "REPLICADO", "IC95 contiene T y excluye 0"
        if contiene_T and contiene_0:
            return "PARCIAL", "IC95 contiene T y 0"
        if not contiene_0 and np.sign(lo + hi) == np.sign(T):
            return "PARCIAL", "excluye 0 con el signo de T, sin contener T"
        return "NO REPLICADO", "IC95 excluye T" + ("" if contiene_0 else " y 0 con signo contrario")

    for k in Y_:
        for nombre, ctrl, tmax, est, nivel in (
                ("R1 JMS: trimestral 2019Q1-2022Q4, TWFE, control tenso<20k, sin Barcelona", "tenso20k", 16, "TWFE", "Q"),
                ("R2 JMS: trimestral 2019Q1-2022Q4, CS, control tenso<20k, sin Barcelona", "tenso20k", 16, "CS", "Q"),
                ("R3 JMS: anual 2017-2022, TWFE con fracción del año, control tenso<20k", "tenso20k", 6, "TWFE-A", "A"),
                ("EXT1: trimestral 2019Q1-2023Q4, TWFE, todos los no sujetos", "todos", 20, "TWFE", "Q"),
                ("EXT2: anual 2017-2023, TWFE con fracción del año, todos los no sujetos", "todos", 7, "TWFE-A", "A")):
            if nivel == "Q":
                idx, trv, Y = sub(k, ctrl, True, tmax)
                r = E.twfe(Y, trv, T0 - 1) if est == "TWFE" else E.cs(Y, trv, BASE - 1, list(range(T0 - 1, tmax)))
            else:
                yrs = list(range(2017, 2017 + tmax))
                aa = a[a.anio.isin(yrs)]
                okk = aa.groupby("cod_ine").anio.nunique()
                okk = okk[okk == tmax].index
                idx, trv = seleccion(gr, okk, ctrl, True)
                Y = aa[aa.cod_ine.isin(idx)].pivot(index="cod_ine", columns="anio", values=Y_[k]).reindex(index=idx, columns=yrs).values
                frac = [0.0 if y < 2020 else (0.25 if y == 2020 else 1.0) for y in yrs]
                r = E.twfe_frac(Y, trv, frac)
            cl, crit = clasifica(r["ic"], TARGET[k], r["nT"], r["nC"])
            rep.append(dict(hipotesis=HIP[k], resultado="log alquiler" if k == "alq" else "log contratos", especificacion=nombre,
                            N_municipios=r["nT"] + r["nC"], tratados=r["nT"], controles=r["nC"], coef=r["b"], ee=r["se"],
                            ic95_lo=r["ic"][0], ic95_hi=r["ic"][1], p=r["p"], objetivo_T=TARGET[k], clasificacion=cl, criterio=crit))
            log_reg(f"REPL:{k}:{nombre[:2]}", nombre, len(idx), r["b"], r["p"], f"{cl}; objetivo {TARGET[k]}")
    rep = pd.DataFrame(rep)
    rep.to_csv(OUT / "tabla_replicacion_jms.csv", index=False)
    print(rep[["hipotesis", "especificacion", "tratados", "controles", "coef", "ee", "clasificacion"]].round(4).to_string())
    res["replicacion_jms"] = rep.to_dict("records")
    res["replicacion_jms_clasificacion"] = {HIP[k]: rep[(rep.hipotesis == HIP[k])].iloc[0].clasificacion for k in Y_}

    # ---------- 5. H3-3a y H3-3b
    est_out, ev_out, mv_all, pl_all, crit_out = {}, {}, [], [], {}
    for k in Y_:
        if not pot_ok[k]:
            est_out[k] = dict(estimado=False, motivo="EMD > EER: no detectable")
            continue
        idx, trv, Y = sub(k)
        post = list(range(T0 - 1, END_MAIN))
        cs_ = E.cs(Y, trv, BASE - 1, post)
        d = E.delta_cs(Y, BASE - 1, post)
        cs_["p_wcb"] = E.wcb_webb(d, trv, REPS)
        cs_["p_ri"] = E.ri_perm(d, trv, REPS)
        tw = E.twfe(Y[:, :END_MAIN], trv, T0 - 1)
        dm = E.cs(Y, trv, BASE - 1, [T0 - 1])
        for nm, r in (("CS", cs_), ("TWFE", tw), ("DID_M", dm)):
            r["pct"], r["pct_ic95"] = pct(r["b"]), [pct(r["ic"][0]), pct(r["ic"][1])]
            if k == "alq":
                r["eur_mes"] = r["pct"] / 100 * rent_ref
                r["eur_mes_ic95"] = [x / 100 * rent_ref for x in r["pct_ic95"]]
            else:
                r["contratos_trim_muni"] = r["pct"] / 100 * n_ref
            log_reg(f"MAIN:{k}:{nm}", f"{Y_[k]} ~ trat x post(2020Q4..2022Q1), FE muni+trim, cluster muni", len(idx), r["b"], r["p"], nm)
        # event study + pretendencias + RR
        es, ses, V = E.event_study(Y, trv, BASE - 1)
        pre_cols = list(range(0, BASE - 1))
        wp = E.wald_pre(es, V, pre_cols)
        rr = E.rr_bounds(Y, trv, BASE - 1, pre_cols, [c for c in post], REPS)
        pd.DataFrame(dict(t=[qlab(t) for t in range(1, TMAX + 1)], coef=es, ee=ses, lo=es - 1.96 * ses, hi=es + 1.96 * ses)
                     ).to_csv(OUT / f"event_study_{k}.csv", index=False)
        ev_out[k] = dict(es=es, ses=ses)
        # sensibilidad (Oster, Cinelli-Hazlett) con covariables observadas
        Yl = Y
        t_ax = np.arange(1, BASE + 1)
        pretrend = np.array([np.polyfit(t_ax, row[:BASE], 1)[0] for row in Yl])
        cov = {"ln_poblacion": np.log(gr["pop"].reindex(idx).values), "nivel_previo": Yl[:, :BASE].mean(1), "pendiente_previa": pretrend}
        sens = E.sensibilidad(d, trv, cov)
        # ---------- multiverso
        mv = []
        for ctrl in ("todos", "pop20k", "tenso20k"):
            for end in (END_MAIN, END_ALT):
                for exc in (True, False):
                    for est in ("CS", "DID_M", "TWFE"):
                        i2, t2, Y2 = sub(k, ctrl, exc)
                        if t2.sum() < 5 or (~t2).sum() < 5:
                            continue
                        if est == "CS":
                            r = E.cs(Y2, t2, BASE - 1, list(range(T0 - 1, end)))
                        elif est == "DID_M":
                            r = E.cs(Y2, t2, BASE - 1, [T0 - 1])
                        else:
                            r = E.twfe(Y2[:, :end], t2, T0 - 1)
                        mv.append(dict(resultado=k, control=ctrl, fin=qlab(end), sin_barcelona=exc, estimador=est, b=r["b"], se=r["se"],
                                       p=r["p"], lo=r["ic"][0], hi=r["ic"][1], nT=r["nT"], nC=r["nC"]))
                        log_reg(f"MV:{k}:{ctrl}:{qlab(end)}:{int(exc)}:{est}", "multiverso", len(i2), r["b"], r["p"], "curva de especificaciones")
        mv = pd.DataFrame(mv)
        mv.to_csv(OUT / f"multiverso_{k}.csv", index=False)
        mv_all.append(mv)
        # ---------- placebos P3
        pls = []
        # (i) fecha falsa trimestral 2019Q4 (post falso 2019Q4-2020Q2, base 2019Q3), mismos tratados
        Yp = Y[:, :BASE - 1]
        rp = E.cs(Yp, trv, 2, [3, 4, 5])
        dp = E.delta_cs(Yp, 2, [3, 4, 5])
        pls.append(dict(resultado=k, placebo="fecha falsa 2019Q4 (trimestral)", b=rp["b"], se=rp["se"], p=rp["p"], p_ri=E.ri_perm(dp, trv, REPS),
                        nT=rp["nT"], nC=rp["nC"]))
        # (ii) fecha falsa anual 2018 -> 2019 (equivalente a 2018Q4 en datos anuales 2016-2019)
        yrs = [2016, 2017, 2018, 2019]
        aa = a[a.anio.isin(yrs)]
        okk = aa.groupby("cod_ine").anio.nunique()
        okk = okk[okk == 4].index
        ia, ta = seleccion(gr, okk, "todos", True)
        Ya = aa[aa.cod_ine.isin(ia)].pivot(index="cod_ine", columns="anio", values=Y_[k]).reindex(index=ia, columns=yrs).values
        ra = E.cs(Ya, ta, 2, [3])
        da = E.delta_cs(Ya, 2, [3])
        pls.append(dict(resultado=k, placebo="fecha falsa 2018Q4 (anual: 2019 frente a 2018)", b=ra["b"], se=ra["se"], p=ra["p"],
                        p_ri=E.ri_perm(da, ta, REPS), nT=ra["nT"], nC=ra["nC"]))
        # (iii) unidades falsas: no sujetos de 10.000-20.000 hab. con tratamiento ficticio en 2020Q4
        g_ = gr.reindex(units_all)
        fal = (~g_.sujeto.values) & (g_["pop"].values >= 10000) & (g_["pop"].values < 20000)
        ctr = (~g_.sujeto.values) & ~fal
        keep = (fal | ctr) & (np.asarray(units_all) != "08019")
        Yu = W[k].loc[np.asarray(units_all)[keep]].values[:, :END_MAIN]
        tu = fal[keep]
        if tu.sum() >= 3:
            ru = E.cs(Yu, tu, BASE - 1, post)
            du = E.delta_cs(Yu, BASE - 1, post)
            pls.append(dict(resultado=k, placebo="unidades falsas 10.000-20.000 hab. (2020Q4)", b=ru["b"], se=ru["se"], p=ru["p"],
                            p_ri=E.ri_perm(du, tu, REPS), p_wcb=E.wcb_webb(du, tu, REPS) if tu.sum() < 50 else np.nan,
                            nT=ru["nT"], nC=ru["nC"]))
        for p_ in pls:
            log_reg(f"PLAC:{k}:{p_['placebo'][:20]}", p_["placebo"], p_["nT"] + p_["nC"], p_["b"], p_["p"], "placebo P3")
        pl_all.append(pd.DataFrame(pls))
        # ---------- criterios a-c
        a_ok = bool(wp["p"] > 0.10 and (rr["ic_RM"][0] > 0 or rr["ic_RM"][1] < 0))
        b_ok = bool(all(min(p_["p"], p_["p_ri"]) >= 0.05 for p_ in pls))
        c_ok = bool(sens["RV_q1"] > sens["r2_parcial_max"] and sens["oster_abs"] > 1)
        est_out[k] = dict(estimado=True, N=int(len(idx)), nT=cs_["nT"], nC=cs_["nC"], CS=cs_, TWFE=tw, DID_M=dm,
                          pretrend_wald=wp, rambachan_roth=rr, sensibilidad=sens, placebos=pls)
        crit_out[k] = dict(a=a_ok, b=b_ok, c=c_ok)
        print(k, "CS", round(cs_["b"], 4), round(cs_["se"], 4), "p", round(cs_["p"], 4), "| TWFE", round(tw["b"], 4), "| pre p", round(wp["p"], 3),
              "RR", [round(x, 4) for x in rr["ic_RM"]], "| crit", crit_out[k], "| mv med", round(mv.b.median(), 4))
    pd.concat(pl_all).to_csv(OUT / "placebos.csv", index=False)
    pd.concat(mv_all).to_csv(OUT / "multiverso.csv", index=False)
    res["estimacion"], res["criterios_abc"] = est_out, crit_out
    mvres = {}
    for m in mv_all:
        kk = m.resultado.iloc[0]
        mvres[HIP[kk]] = dict(n_specs=int(len(m)), mediana_b=float(m.b.median()), mediana_pct=float(pct(m.b.median())),
                              prop_mismo_signo=float((m.b < 0).mean()), prop_signif_5pct=float(((m.p < 0.05) & (m.b < 0)).mean()))
    res["multiverso"] = mvres

    # ---------- 6. EVALUACIÓN SELLADA (una vez por hipótesis)
    ctrl_set = controls_tr
    sell = {}
    for k in Y_:
        fn = make_fn(k, treated_tr, ctrl_set, rent_ref)
        dr = dry_run(fn, sorted(treated_tr | ctrl_set), HIP[k])      # test en seco (rutas de ensayo); si falla, se detiene
        res.setdefault("dry_run", {})[HIP[k]] = dr
        f = OUT_REAL / f"sellado_{HIP[k]}.json"
        if f.exists():
            sell[k] = json.loads(f.read_text())
        elif SMOKE:
            sell[k] = dict(omitido="smoke: sin apertura sellada")
        elif not (pot_ok[k] and val_ok[k]):
            sell[k] = dict(omitido="sin potencia en la especificación o en la validación (P2)")
        else:
            try:
                with shim_pandas3():
                    r = holdout.evaluate_v3(HIP[k], fn, "C3", ["c3_serpavi"])
                f.write_text(json.dumps(r, indent=1, ensure_ascii=False, default=str))
                sell[k] = r
            except Exception as ex:   # noqa: BLE001  el acceso queda consumido: se registra y NO se repite
                sell[k] = dict(error=repr(ex), nota="acceso consumido; no repetir")
                f.write_text(json.dumps(sell[k], indent=1, ensure_ascii=False))
    res["sellado"] = sell

    # ---------- 7. CAPA
    capa = {}
    for k in Y_:
        s = sell.get(k, {})
        if not est_out[k].get("estimado"):
            capa[HIP[k]] = dict(capa="C4", fallo="no detectable (P2)", criterios={})
            continue
        b_tr = est_out[k]["CS"]["b"]
        if "beta" in s:
            d_ok = bool(np.sign(s["beta"]) == np.sign(b_tr) and (s["ic95"][1] < 0 or s["ic95"][0] > 0) and (s["beta"] < 0))
        else:
            d_ok = None
        cr = dict(crit_out[k], d=d_ok, e="pendiente: Holm m=4 lo aplica el orquestador")
        fallos = [x for x in "abcd" if cr[x] is False]
        if d_ok is None:
            capa[HIP[k]] = dict(capa="C4", fallo="validación sellada no evaluada", criterios=cr)
        elif fallos:
            capa[HIP[k]] = dict(capa="C4", fallo="falla: " + ", ".join(fallos), criterios=cr)
        else:
            capa[HIP[k]] = dict(capa="C3 (condicionada a Holm, criterio e)", fallo=None, criterios=cr)
    res["capa"] = capa
    (OUT / "_interno.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    reg.flush()
    figuras(ev_out, mv_all)
    escribir_salidas(res, est_out, sell, capa, rep, pot)
    return res


def figuras(ev_out, mv_all):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4), sharex=True)
    for a_, k, tit in zip(ax, ("alq", "n"), ("ln renta (H3-3a)", "ln contratos (H3-3b)")):
        if k not in ev_out:
            continue
        e, s = ev_out[k]["es"], ev_out[k]["ses"]
        x = np.arange(1, TMAX + 1)
        a_.errorbar(x, e, yerr=1.96 * s, fmt="o", ms=3, capsize=2)
        a_.axhline(0, color="k", lw=.6)
        a_.axvline(T0 - .5, color="r", ls="--", lw=.8)
        a_.axvline(END_MAIN + .5, color="gray", ls=":", lw=.8)
        a_.set_title(tit)
        a_.set_xticks(x[::2])
        a_.set_xticklabels([qlab(t) for t in x[::2]], rotation=60, fontsize=7)
    fig.suptitle("Event study CS (base 2020Q3; línea roja: 2020Q4; punteada: fin de ventana 2022Q1)")
    fig.tight_layout()
    fig.savefig(OUT / "fig_event_study.png", dpi=130)
    plt.close(fig)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for a_, m in zip(ax, mv_all):
        m = m.sort_values("b").reset_index(drop=True)
        col = np.where((m.p < .05) & (m.b < 0), "tab:red", "tab:gray")
        a_.vlines(m.index, m.lo, m.hi, color=col, lw=1)
        a_.plot(m.index, m.b, "k.", ms=4)
        a_.axhline(0, color="k", lw=.6)
        a_.set_title("Curva de especificaciones: " + ("renta" if m.resultado.iloc[0] == "alq" else "contratos"))
        a_.set_xlabel("especificación (ordenada por coeficiente)")
        a_.set_ylabel("log-puntos")
    fig.tight_layout()
    fig.savefig(OUT / "fig_curva_especificaciones.png", dpi=130)
    plt.close(fig)


def escribir_salidas(res, est_out, sell, capa, rep, pot):
    tab = []
    for k in Y_:
        e = est_out[k]
        if not e.get("estimado"):
            continue
        for nm in ("CS", "TWFE", "DID_M"):
            r = e[nm]
            tab.append(dict(hipotesis=HIP[k], estimador=nm, N=e["N"], tratados=e["nT"], controles=e["nC"], b_logpuntos=r["b"], ee=r["se"],
                            ic95_lo=r["ic"][0], ic95_hi=r["ic"][1], p=r["p"], pct=r["pct"], pct_lo=r["pct_ic95"][0], pct_hi=r["pct_ic95"][1],
                            eur_mes=r.get("eur_mes"), contratos_trim_muni=r.get("contratos_trim_muni"),
                            p_wcb=r.get("p_wcb"), p_ri=r.get("p_ri")))
        s = sell.get(k, {})
        if "beta" in s:
            tab.append(dict(hipotesis=HIP[k], estimador="SERPAVI sellado (DiD anual)", N=s["nT"] + s["nC"], tratados=s["nT"], controles=s["nC"],
                            b_logpuntos=s["beta"], ee=s["se"], ic95_lo=s["ic95"][0], ic95_hi=s["ic95"][1], p=s["p_dos_colas"], pct=s["pct"],
                            pct_lo=s["pct_ic95"][0], pct_hi=s["pct_ic95"][1], eur_mes=s.get("eur_mes")))
    pd.DataFrame(tab).to_csv(OUT / "tabla_resultados.csv", index=False)
    top = {}
    for k in Y_:
        e = est_out[k]
        s = sell.get(k, {})
        top[HIP[k]] = dict(CS=dict(b=e["CS"]["b"], ic95=e["CS"]["ic"], pct=e["CS"]["pct"], pct_ic95=e["CS"]["pct_ic95"],
                                   eur_mes=e["CS"].get("eur_mes"), eur_mes_ic95=e["CS"].get("eur_mes_ic95"),
                                   contratos_trim_muni=e["CS"].get("contratos_trim_muni"), p=e["CS"]["p"], p_ri=e["CS"]["p_ri"]) if e.get("estimado") else None,
                           sellado=s)
    p_val = {HIP[k]: sell.get(k, {}).get("p_dos_colas") for k in Y_}
    out = dict(rama="C3", pregunta="¿Redujeron los topes de la Ley 11/2020 la renta (H3-3a) y el nº de contratos nuevos (H3-3b) en los 61 municipios sujetos?",
               datos="Incasòl fianzas municipales trimestrales 2019Q1-2023Q4 (entrenamiento, vía sellar_v3), lista Ley 11/2020, Censo 2021 (población), "
                     "SERPAVI municipal 2018-2023 (sellado por fuente)",
               N=res["meta"]["balanceadas_2019Q1_2023Q4"], metodo="DiD Callaway-Sant'Anna con un solo momento (2020Q4), TWFE y DID_M como contraste; cluster municipio; "
               "event study, cotas Rambachan-Roth (sin paquete), placebos P3, Oster, Cinelli-Hazlett, multiverso",
               estimacion=top, ic95={h: (top[h]["CS"]["pct_ic95"] if top[h]["CS"] else None) for h in top},
               p_ajustado=None, nivel_evidencia=None, p_validacion_sellada=p_val,
               capa=capa, criterios={h: capa[h]["criterios"] for h in capa},
               diagnosticos=dict(potencia=res["potencia"], pretendencias={HIP[k]: dict(wald=est_out[k]["pretrend_wald"], rr=est_out[k]["rambachan_roth"]) for k in Y_ if est_out[k].get("estimado")},
                                 sensibilidad={HIP[k]: est_out[k]["sensibilidad"] for k in Y_ if est_out[k].get("estimado")},
                                 placebos={HIP[k]: est_out[k]["placebos"] for k in Y_ if est_out[k].get("estimado")},
                                 multiverso=res["multiverso"], replicacion_jms=res["replicacion_jms_clasificacion"]),
               fuera_muestra=dict(modelo="validación sellada por fuente (SERPAVI anual)", rmse=None, dm_vs_ar4=None,
                                  nota="No aplica AR(4)/ECM v1: es un efecto de política, no un pronóstico; la validación fuera de muestra es la sellada por fuente."),
               notas="p_ajustado: Holm m=4 lo aplica el orquestador con p_validacion_sellada. Magnitudes en % y €/mes (renta media previa de los tratados en fianzas). "
                     "Ver desviaciones.md.")
    lv = [capa[h]["capa"] for h in capa]
    out["nivel_evidencia"] = ("CAUSAL (condicionado a Holm)" if all(x.startswith("C3") for x in lv) else
                              "ASOCIACIÓN ROBUSTA" if any(x.startswith("C3") for x in lv) else "EXPLORATORIO")
    (OUT / "resultado.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    (OUT / "desviaciones.md").write_text(DESV)


DESV = """# Desviaciones del pre-registro (C3)

1. Las fianzas trimestrales de Incasòl solo existen desde 2019Q1 (2017-2018 solo anual). La ventana previa es 2019Q1-2020Q3 (7 trimestres), el periodo de análisis 2019Q1-2023Q4 y la ventana de tratamiento 2020Q4-2022Q1 (o 2021Q3).
2. Placebo de fecha falsa 2018Q4: no es trimestral (no hay trimestres de 2018). Se hacen dos versiones: fecha falsa 2019Q4 con post 2019Q4-2020Q2 (se excluye 2020Q3 por la anticipación que documentan JMS) y versión anual (2019 frente a 2018, panel anual 2016-2019).
3. Rambachan-Roth: no hay paquete instalado. Se usan la cota de magnitudes relativas con M̄=1 y la de tendencia lineal (suavidad con M=0) con IC por bootstrap de unidades (999). No es el IC condicional/híbrido de Rambachan-Roth.
4. Control del multiverso: hipotesis.md dice «no sujetos con más de 20.000 habitantes como en JMS 2023». La ficha de literatura (A3) describe sus controles como mercado tenso por debajo del umbral. Se corren los dos más «todos los no sujetos» (principal). «Mercado tenso» se aproxima con el crecimiento anual de la renta de fianzas 2014-2019 ≥ 4,15 %.
5. Población: Censo 2021 (suma de grandes grupos de edad por municipio), fija en el tiempo. No hay padrón anual en los datos.
6. Barcelona se excluye en la especificación principal (como JMS y la potencia); su inclusión es una decisión del multiverso.
7. dCDH: no hay paquete. Se usa DID_M (efecto en el momento del cambio, 2020Q4 frente a 2020Q3), que con un único momento de tratamiento coincide con ATT(g,g) de CS.
8. Contratos: ln del nº de fianzas (sin denominador de población; la población fija se absorbe en los efectos fijos de municipio). Sin controles (paro, ERTO) que sí usan JMS.
9. El resultado de renta es la media de las medias de banda ponderada por nº de contratos; las bandas cambian entre años.
10. Potencia de la validación SERPAVI: la estructura (municipios con los 4 años) viene de SERPAVI y la varianza es la de las fianzas anuales (aproximación; SERPAVI es un stock IRPF y su varianza real no se miró).
11. holdout.evaluate_v3 usa DataFrame.apply(pd.to_numeric, errors='ignore'), no válido en pandas 3. Se aplica un parche en memoria solo durante la llamada (clase shim_pandas3); src/holdout.py no se modifica. El test en seco se hizo a través de evaluate_v3 con rutas de ensayo, sin tocar el registro real de accesos.
12. Muestra: panel equilibrado 2019Q1-2023Q4 (misma muestra para event study, pretendencias, estimación principal y sensibilidad). Las réplicas JMS usan paneles equilibrados de su propio periodo.
13. fuera_muestra: no se compara con AR(4)/ECM v1 (es un efecto de política); la validación fuera de muestra es la sellada por fuente.
"""

if __name__ == "__main__":
    main()
