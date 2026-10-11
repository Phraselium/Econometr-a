"""T4 · Dirección frente a magnitud en la proyección del déficit 2026-2030 (extensión a 2035). Determinista, sin red.

dD = F - T + B + X por provincia, con una rejilla de escenarios de terminadas (T), hogares (F), bajas (B, T1) y liberadas que no
llegan al mercado (X, T2). La DIRECCIÓN sube a C2 solo si el signo es el mismo en TODA la rejilla plausible; la MAGNITUD es C4.
Uso: python3 src/v5_1/t4_run.py [--smoke]
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v5_1"))
import t3_run as t3  # noqa: E402  (importa b1_run, m1_run y econ_utils)

b1, m1, econ_utils = t3.b1, t3.m1, t3.econ_utils
np.random.seed(t3.SEED)
RAW = t3.RAW
OUT = RAIZ / "output" / "v5_1" / "T4"
SMOKE = "--smoke" in sys.argv
S3 = t3.S3
TS = ("a", "b", "c", "lo", "opt")        # terminadas: ritmo actual, cartera, tendencia, mínimo, optimista
FS = ("min", "central", "max")           # hogares
BS = ("min", "central", "max")           # bajas T1 (tasa 0 / central / máx.)
XS = ("0", "min", "central", "max")      # liberadas que no llegan al mercado (0 = sin variante)
FECHA = "2025 (ECP y MIVAU); proyecciones INE 54562 y 36726 de 2026-06-17"


def series_t(cods, nombres):
    mi = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    mp = pd.read_csv(RAW / "mivau_v2_protegida.csv")
    ex_l = {c: m1.UNIPROV.get(c) for c in cods}
    ex_p = {c: m1.UNIPROV_PROT.get(c) for c in cods}
    lt = b1.serie_prov(mi, "viv_libres_terminadas_anual", nombres, ex_l)
    pt = b1.serie_prov(mp, "prot_definitiva_anual", nombres, ex_p)
    li = b1.serie_prov(mi, "viv_libres_iniciadas_anual", nombres, ex_l)
    pi_ = b1.serie_prov(mp, "prot_provisional_anual", nombres, ex_p)
    yrs = list(range(1991, 2026))

    def suma(a, b_, c):
        x = a.loc[c].reindex(yrs).fillna(0) if c in a.index else pd.Series(0.0, index=yrs)
        y = b_.loc[c].reindex(yrs).fillna(0) if c in b_.index else pd.Series(0.0, index=yrs)
        return x + y
    Tp = {c: suma(lt, pt, c) for c in cods}
    Ip = {c: suma(li, pi_, c) for c in cods}

    def nac(df, pat):
        s = df[(df.nivel == "nacional") & df.serie.str.contains(pat)].set_index("periodo").valor
        s.index = s.index.astype(int)
        return s.reindex(yrs).astype(float)
    Tn = nac(mi, "viv_libres_terminadas_anual") + nac(mp, "prot_definitiva_anual")
    In = nac(mi, "viv_libres_iniciadas_anual") + nac(mp, "prot_provisional_anual")
    return Tp, Ip, Tn, In


def retardos(In, Tn):
    import b2_run as b2
    vent = {"2012-2025": (2012, 2025), "2016-2025": (2016, 2025), "2019-2025": (2019, 2025), "2022-2025": (2022, 2025),
            "2008-2025": (2008, 2025)}
    lags = {k: b2.estima_retardo(In, Tn, *v) for k, v in vent.items()}
    return lags, float(np.median(list(lags.values()))), min(lags.values()), max(lags.values()), b2.interp_ini


def terminadas_escenarios(t, i, H, Lc, Lmin, Lmax, interp_ini):
    """Terminadas acumuladas en H años (2026..2025+H) por escenario, para una provincia."""
    y0 = 2026
    anios = range(y0, y0 + H)
    rell = float(i.loc[2023:2025].mean())
    rell_max = float(i.loc[2021:2025].max())

    def cart(L, relleno):
        return sum(interp_ini(i, y - L, relleno) for y in anios)
    a = H * float(t.loc[2023:2025].mean())
    b_c, b_lo, b_hi = cart(Lc, rell), cart(Lmax, rell), cart(Lmin, rell)
    x = np.arange(2021, 2026)
    yv = t.loc[2021:2025].values
    sl, ic = np.polyfit(x, yv, 1)
    c_ = sum(max(0.0, ic + sl * yy) for yy in anios)
    lo = min(H * float(t.loc[2023:2025].min()), b_lo)
    # optimista: el mayor de (máximo anual de terminadas 2019-2025 sostenido) y (cartera con el retardo más corto
    # y las iniciadas posteriores a 2025 en el máximo de 2021-2025)
    opt = max(H * float(t.loc[2019:2025].max()), cart(Lmin, rell_max))
    return dict(a=a, b=b_c, c=c_, lo=lo, opt=opt, b_lo=b_lo, b_hi=b_hi)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    (OUT / "figuras").mkdir(exist_ok=True)
    reg = econ_utils.Registry(OUT / "registro.csv")
    _, nombres = m1.provincias_ecp()
    cods = sorted(nombres)
    if SMOKE:
        cods = ["46", "28", "31", "08"]
    nombres = {c: nombres[c] for c in cods}
    ins = t3.insumos(cods, nombres)
    kcod = ins["kcod"]
    park, bj = ins["park"], ins["bj"]
    parque_ult = park[park.columns.max()].reindex(cods)
    rate = {s: bj[f"tasa_{s}"].astype(float) for s in S3}
    Tp, Ip, Tn, In = series_t(cods, nombres)
    lags, Lc, Lmin, Lmax, interp_ini = retardos(In, Tn)

    # ---- F por horizonte
    hp, hnac = b1.lee_proy_hogares()
    pp, _ = b1.lee_proy_pob()
    pob = pp[pp.e == -1].pivot(index="k", columns="anyo", values="valor")

    def F_h(c, y1):
        k = kcod[c]
        ine = hp.loc[k, y1] - hp.loc[k, 2026]
        alt = hp.loc[k, 2026] * (pob.loc[k, y1] / pob.loc[k, 2026] - 1)
        return dict(min=min(ine, alt), central=ine, max=max(ine, alt))
    # ---- X por horizonte: reparto del acumulado 2026-2035 de T2 según la trayectoria de defunciones 75+
    mu = ins["muertes"].reindex(cods)
    sh5 = mu.loc[:, 2026:2030].sum(axis=1) / mu.loc[:, 2026:2035].sum(axis=1)
    lib = ins["lib"]

    def X_h(c, H):
        out = {"0": 0.0}
        for s in S3:
            tot = float(lib.loc[c, f"no_llega_{s}"])
            out[s] = tot * (float(sh5[c]) if H == 5 else 1.0)
        return out

    res_h = {}
    for H in (5, 10):
        y1 = 2026 + H
        prov = {}
        for c in cods:
            T = terminadas_escenarios(Tp[c], Ip[c], H, Lc, Lmin, Lmax, interp_ini)
            F = F_h(c, y1)
            X = X_h(c, H)
            Bf = {s: float(rate[s][c]) * float(parque_ult[c]) * H for s in S3}
            prov[c] = dict(T=T, F=F, X=X, B=Bf)
        res_h[H] = prov

    # ---- rejilla: dD por provincia y escenario
    def rejilla(H, ts=TS, fs=FS, bs=BS, xs=XS):
        filas = []
        for c in cods:
            p = res_h[H][c]
            for t, f_, b_, x_ in itertools.product(ts, fs, bs, xs):
                filas.append((c, t, f_, b_, x_, p["F"][f_] - p["T"][t] + p["B"][b_] + p["X"][x_]))
        return pd.DataFrame(filas, columns=["cod_prov", "T", "F", "B", "X", "dD"])

    def signos(g):
        mn, mx = g.dD.min(), g.dD.max()
        return "empeora" if mn > 0 else ("mejora" if mx < 0 else "indeterminado")

    cuentas, stage_rows = {}, []
    etapas = [
        ("E0 como B2 (T a,b; F mín-máx; bajas central y máx.; sin X)", dict(ts=("a", "b"), bs=("central", "max"), xs=("0",))),
        ("E1 + bajas mínimas (tasa 0)", dict(ts=("a", "b"), bs=BS, xs=("0",))),
        ("E2 + terminadas mínimas y tendencia", dict(ts=("a", "b", "c", "lo"), bs=BS, xs=("0",))),
        ("E3 + terminadas optimistas", dict(ts=TS, bs=BS, xs=("0",))),
        ("E4 + liberadas que no llegan (completa)", dict(ts=TS, bs=BS, xs=XS)),
    ]
    for H in (5, 10):
        for nm, kw in etapas:
            g = rejilla(H, **kw)
            sg = g.groupby("cod_prov").apply(signos, include_groups=False)
            nacd = g.groupby(["T", "F", "B", "X"]).dD.sum()
            nsg = "empeora" if nacd.min() > 0 else ("mejora" if nacd.max() < 0 else "indeterminado")
            n = sg.value_counts()
            stage_rows.append(dict(horizonte=2025 + H, etapa=nm, n_escenarios=int(len(nacd)), nacional=nsg,
                                   nacional_dD_min=float(nacd.min()), nacional_dD_max=float(nacd.max()),
                                   n_empeoran=int(n.get("empeora", 0)), n_mejoran=int(n.get("mejora", 0)),
                                   n_indeterminadas=int(n.get("indeterminado", 0))))
    etapas_df = pd.DataFrame(stage_rows)
    etapas_df.to_csv(OUT / "tablas" / "recuento_por_etapas.csv", index=False, float_format="%.0f")

    # ---- rejilla completa y resultado provincial
    out = {}
    for H in (5, 10):
        g = rejilla(H)
        sg = g.groupby("cod_prov").apply(signos, include_groups=False)
        gm = g.groupby("cod_prov").dD.agg(["min", "max"])
        cen = g[(g["T"] == "a") & (g.F == "central") & (g.B == "central") & (g.X == "0")].set_index("cod_prov").dD
        cen_x = g[(g["T"] == "a") & (g.F == "central") & (g.B == "central") & (g.X == "central")].set_index("cod_prov").dD
        nacd = g.groupby(["T", "F", "B", "X"]).dD.sum().reset_index()
        out[H] = dict(g=g, sg=sg, gm=gm, cen=cen, cen_x=cen_x, nacd=nacd)
        tab = pd.DataFrame({"provincia": [nombres[c] for c in cods], "dD_min": gm["min"].reindex(cods).values,
                            "dD_central_a": cen.reindex(cods).values, "dD_central_a_con_X": cen_x.reindex(cods).values,
                            "dD_max": gm["max"].reindex(cods).values, "direccion": sg.reindex(cods).values}, index=cods)
        tab["capa_direccion"] = np.where(tab.direccion == "indeterminado", "C4", "C2")
        tab["capa_magnitud"] = "C4"
        tab.round(0).to_csv(OUT / "tablas" / f"direccion_provincial_{2025 + H}.csv", index_label="cod_prov")
        out[H]["tab"] = tab
        nacd.to_csv(OUT / "tablas" / f"escenarios_nacional_{2025 + H}.csv", index=False, float_format="%.0f")
        for r in nacd.itertuples():
            reg.log("T4", f"T4_nac_{2025 + H}_T{r.T}_F{r.F}_B{r.B}_X{r.X}", "dD = F - T + B + X (suma de provincias)", 2026, 2025 + H,
                    len(cods), np.nan, np.nan, np.nan, coef_interes=float(r.dD), notas="escenario; capa C4 (magnitud)")
        for c in cods:
            reg.log("T4", f"T4_prov_{2025 + H}_{c}", "signo de dD en toda la rejilla", 2026, 2025 + H, 1, np.nan, np.nan, np.nan,
                    coef_interes=float(gm.loc[c, "min"]), notas=f"{nombres[c]}; dD max {gm.loc[c, 'max']:.0f}; {sg[c]}")

    # ---- estrés 2006-2007 (fuera de la rejilla plausible) y ritmo de equilibrio
    t0607 = float(Tn.loc[2006:2007].mean())
    t_max_rec = float(Tn.loc[2019:2025].max())
    T_nac = {H: {k: sum(res_h[H][c]["T"][k] for c in cods) for k in ("a", "b", "c", "lo", "opt")} for H in (5, 10)}
    F_nac = {H: {s: sum(res_h[H][c]["F"][s] for c in cods) for s in FS} for H in (5, 10)}
    B_nac = {H: {s: sum(res_h[H][c]["B"][s] for c in cods) for s in S3} for H in (5, 10)}
    X_nac = {H: {s: sum(res_h[H][c]["X"][s] for c in cods) for s in XS} for H in (5, 10)}
    equil = {H: {"central": (F_nac[H]["central"] + B_nac[H]["central"]) / H, "con_X": (F_nac[H]["central"] + B_nac[H]["central"] + X_nac[H]["central"]) / H,
                 "hogares_bajos_bajas_0": F_nac[H]["min"] / H} for H in (5, 10)}
    stress = {H: dict(T=H * t0607, dD_central=F_nac[H]["central"] - H * t0607 + B_nac[H]["central"]) for H in (5, 10)}

    # ---- niveles (C4): D2025 por fuente y bajas del pasado
    base_con, base_sin = float(ins["d_con"].sum()), float(ins["d_sin"].sum())
    baj25 = {s: float(t3.bajas_pasadas(rate[s], park, range(2021, 2026)).sum()) for s in S3}
    D0 = {"min": base_con + baj25["min"], "central": (base_con + base_sin) / 2 + baj25["central"], "max": base_sin + baj25["max"]}
    niveles = {}
    for H in (5, 10):
        nd = out[H]["nacd"]
        cen = nd[(nd["T"] == "a") & (nd.F == "central") & (nd.B == "central") & (nd.X == "0")].dD.iloc[0]
        cen_x = nd[(nd["T"] == "a") & (nd.F == "central") & (nd.B == "central") & (nd.X == "central")].dD.iloc[0]
        niveles[H] = dict(D_min=base_con + nd.dD.min(), D_central=D0["central"] + cen, D_central_con_X=D0["central"] + cen_x,
                          D_max=base_sin + baj25["max"] + nd.dD.max(), dD_min=nd.dD.min(), dD_central=cen, dD_central_con_X=cen_x,
                          dD_max=nd.dD.max())
    pd.DataFrame([{"horizonte": 2025 + H, **v} for H, v in niveles.items()]).to_csv(OUT / "tablas" / "niveles_nacional.csv", index=False,
                                                                                    float_format="%.0f")

    # ---- envejecimiento 2031-2035 frente a 2026-2030 (T2 repartido por defunciones de 75+)
    lc = lib.liberadas_central
    l5a = float((lc * sh5).sum())
    l5b = float(lc.sum() - l5a)
    d5a, d5b = float(mu.loc[:, 2026:2030].sum().sum()), float(mu.loc[:, 2031:2035].sum().sum())
    x5a, x5b = X_nac[5]["central"], X_nac[10]["central"] - X_nac[5]["central"]
    f5a = F_nac[5]["central"]
    hn36 = float(sum(hp.loc[kcod[c], 2036] - hp.loc[kcod[c], 2031] for c in cods))
    t2n = json.loads((RAIZ / "output/v5_1/T2/tablas/agregados.json").read_text())["resumen"]
    env = pd.DataFrame([
        dict(periodo="2026-2030", liberadas_central=l5a, liberadas_central_anual=l5a / 5, defunciones_75mas=d5a, no_llega_central=x5a,
             hogares_F_ine=f5a, F_anual=f5a / 5),
        dict(periodo="2031-2035", liberadas_central=l5b, liberadas_central_anual=l5b / 5, defunciones_75mas=d5b, no_llega_central=x5b,
             hogares_F_ine=hn36, F_anual=hn36 / 5),
        dict(periodo="2036-2040 (T2, escenario)", liberadas_central=t2n["2036-2040"]["liberadas_central"],
             liberadas_central_anual=t2n["2036-2040"]["liberadas_central"] / 5, defunciones_75mas=np.nan,
             no_llega_central=t2n["2036-2040"]["no_llega_central"], hogares_F_ine=np.nan, F_anual=np.nan),
    ])
    env.to_csv(OUT / "tablas" / "envejecimiento_2031_2035.csv", index=False, float_format="%.0f")
    mu_y = mu.sum()
    mu_y.loc[2026:2040].to_csv(OUT / "tablas" / "defunciones_75mas_anual.csv", header=["defunciones"], float_format="%.0f")

    # ---- control de sumas
    Ta_nac = {H: H * float(Tn.loc[2023:2025].mean()) for H in (5, 10)}
    a4n = pd.read_csv(RAIZ / "output/v5/A4/tablas/A4_reconciliacion_prov_nacional.csv")
    t2a = t2n["2026-2035"]
    cs = []

    def chk(nm, parts, tot, tol=1e-6):
        cs.append(dict(tabla=nm, suma_provincial=float(parts), nacional=float(tot), tolerancia_rel=tol))
    if not SMOKE:
        chk("deficit_2025_fuente_ECP_con_A4", base_con, a4n[a4n.periodo == "2021-2025"].deficit_nac.iloc[0])
        for H in (5, 10):
            chk(f"F_2026_{2026 + H}_hogares_INE", F_nac[H]["central"], float(hnac[2026 + H] - hnac[2026]), 1e-2)
            chk(f"terminadas_esc_a_{H}a", T_nac[H]["a"], Ta_nac[H], 1e-2)
        chk("X_central_2026_2035_T2", X_nac[10]["central"], t2a["no_llega_central"], 1e-6)
        chk("X_min_2026_2035_T2", X_nac[10]["min"], t2a["no_llega_min"], 1e-6)
        chk("X_max_2026_2035_T2", X_nac[10]["max"], t2a["no_llega_max"], 1e-6)
        chk("liberadas_2026_2030_mas_2031_2035_T2", l5a + l5b, t2a["liberadas_central"], 1e-9)
        chk("dD_central_2030_a", out[5]["cen"].sum(), F_nac[5]["central"] - T_nac[5]["a"] + B_nac[5]["central"], 1e-9)
        nd5 = out[5]["nacd"]
        chk("dD_nacional_2030_suma_provincias", nd5[(nd5["T"] == "a") & (nd5.F == "central") & (nd5.B == "central") & (nd5.X == "0")].dD.iloc[0],
            Ta_nac[5] * -1 + float(hnac[2031] - hnac[2026]) + B_nac[5]["central"], 1e-2)
    for c in cs:
        c["ok"] = abs(c["suma_provincial"] - c["nacional"]) <= c["tolerancia_rel"] * max(1.0, abs(c["nacional"]))
    (OUT / "control_sumas.json").write_text(json.dumps(cs, ensure_ascii=False, indent=1))
    fallos = [c["tabla"] for c in cs if not c["ok"]]
    print("control_sumas fallos:", fallos)
    print(etapas_df.round(0).to_string())
    print({H: {k: round(v) for k, v in niveles[H].items()} for H in niveles})
    print("estrés 2006-07:", {H: {k: round(v) for k, v in s.items()} for H, s in stress.items()}, "equilibrio:", {H: {k: round(v) for k, v in e.items()} for H, e in equil.items()})
    print(env.round(0).to_string())
    if SMOKE:
        return

    # ---- recuentos y fichas
    n5 = out[5]["sg"].value_counts()
    n10 = out[10]["sg"].value_counts()
    old = pd.read_csv(RAIZ / "output/v5/B2/tablas/B2_deficit_2030_provincial.csv", dtype={"cod_prov": str}).signo.value_counts()
    dir_nac = {H: etapas_df[(etapas_df.horizonte == 2025 + H) & etapas_df.etapa.str.startswith("E4")].nacional.iloc[0] for H in (5, 10)}
    figura(out, niveles, T_nac, F_nac)
    escribe(out, niveles, etapas_df, n5, n10, old, dir_nac, T_nac, F_nac, B_nac, X_nac, equil, stress, t0607, t_max_rec, env, lags, Lc,
            fallos, base_con, base_sin, baj25, l5a, l5b, d5a, d5b, nombres)
    reg.flush()


def figura(out, niveles, T_nac, F_nac) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    for k, H in enumerate((5, 10)):
        nd = out[H]["nacd"]
        ax[k].hist(nd.dD / 1e6, bins=30, color="#4575b4")
        ax[k].axvline(0, color="k", lw=0.8)
        ax[k].set_title(f"Cambio nacional del déficit 2025 a {2025 + H}: {len(nd)} escenarios\n"
                        f"mín. {nd.dD.min() / 1e6:.2f} M, máx. {nd.dD.max() / 1e6:.2f} M (magnitud C4)", fontsize=9)
        ax[k].set_xlabel("millones de viviendas")
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "T4_escenarios_nacional.png", dpi=110, metadata={"Software": None})
    plt.close(fig)


def esc(x) -> str:
    return f"{x:,.0f}".replace(",", ".")


def escribe(out, niveles, etapas_df, n5, n10, old, dir_nac, T_nac, F_nac, B_nac, X_nac, equil, stress, t0607, t_max_rec, env, lags, Lc,
            fallos, base_con, base_sin, baj25, l5a, l5b, d5a, d5b, nombres) -> None:
    fd = FECHA
    e5 = int(n5.get("empeora", 0)), int(n5.get("mejora", 0)), int(n5.get("indeterminado", 0))
    e10 = int(n10.get("empeora", 0)), int(n10.get("mejora", 0)), int(n10.get("indeterminado", 0))
    o = int(old.get("empeora", 0)), int(old.get("mejora", 0)), int(old.get("indeterminado", 0))
    capa_dir = {H: ("C2" if dir_nac[H] != "indeterminado" else "C4") for H in (5, 10)}
    N5, N10 = niveles[5], niveles[10]

    def H(i, ind, v, lo, hi, ud, per, cob, fu, capa, fecha=fd):
        return dict(id=i, indicador=ind, valor=None if v is None else round(float(v), 1), min=None if lo is None else round(float(lo), 1),
                    max=None if hi is None else round(float(hi), 1), unidad=ud, periodo=per, cobertura=cob, fuentes=fu, capa=capa, fecha_dato=fecha)
    src = ["B2", "T1", "T2", "INE 54562", "MIVAU"]
    hechos = [
        H("T4-H1", "Déficit acumulado nacional a fin de 2030 (magnitud; mín., central ritmo actual y máx. de la rejilla)", N5["D_central"],
          N5["D_min"], N5["D_max"], "viviendas", "2021-2030", "España (52 provincias)", src, "C4"),
        H("T4-H2", "Cambio del déficit 2025 a 2030 (nacional; mín. y máx. de la rejilla)", N5["dD_central"], N5["dD_min"], N5["dD_max"],
          "viviendas", "2026-2030", "España", src, "C4"),
        H("T4-H3", f"Dirección nacional del déficit 2025-2030 en toda la rejilla ({dir_nac[5]}); provincias que empeoran / mejoran / indeterminadas",
          e5[0], e5[1], e5[2], "provincias", "2025-2030", "52 provincias (valor=empeoran, min=mejoran, max=indeterminadas)", src, capa_dir[5]),
        H("T4-H4", "Provincias que empeoran / mejoran / indeterminadas en B2 (rango sin las variantes nuevas)", o[0], o[1], o[2], "provincias",
          "2025-2030", "52 provincias (valor=empeoran, min=mejoran, max=indeterminadas)", ["B2"], "C4"),
        H("T4-H5", "Déficit acumulado nacional a fin de 2035 (escenario; mín., central y máx.)", N10["D_central"], N10["D_min"], N10["D_max"],
          "viviendas", "2021-2035", "España", src, "C4"),
        H("T4-H6", "Terminadas por año necesarias para mantener constante el déficit 2026-2030 (hogares INE central + bajas T1 central)",
          equil[5]["central"], equil[5]["hogares_bajos_bajas_0"], equil[5]["con_X"], "viviendas/año", "2026-2030", "España", src, "C4"),
        H("T4-H7", "Terminadas por año del escenario optimista (máximo plausible; media de provincias sumadas)", T_nac[5]["opt"] / 5,
          T_nac[5]["a"] / 5, T_nac[5]["opt"] / 5, "viviendas/año", "2026-2030", "España", ["MIVAU"], "C4", "MIVAU hasta 2025"),
        H("T4-H8", "Viviendas liberadas por envejecimiento, 2031-2035 frente a 2026-2030 (central, T2 repartido por defunciones de 75+)", l5b,
          l5a, l5b, "viviendas (5 años)", "2031-2035 (valor y max) / 2026-2030 (min)", "España", ["T2", "INE 36726", "INE 67235"], "C4"),
    ]
    res = {
        "rama": "v5_1/T4",
        "pregunta": "¿Se mantiene la dirección (empeora o mejora) del déficit 2026-2030 en todos los escenarios plausibles, y qué magnitud tiene?",
        "capa": f"Dirección nacional {capa_dir[5]} (criterio de unanimidad en la rejilla); magnitud C4",
        "datos": ["output/v5/B2", "output/v5/B1", "output/v5_1/T1", "output/v5_1/T2", "output/v5/A4", "MIVAU iniciadas/terminadas", "INE 54562"],
        "N": {"provincias": int(len(nombres)), "escenarios_por_horizonte": 180, "horizontes": [2030, 2035]},
        "metodo": "dD = F - T + B + X por provincia sobre una rejilla de 5 (terminadas) x 3 (hogares) x 3 (bajas T1) x 4 (liberadas que no llegan) = 180 "
                  "escenarios; dirección = signo común en toda la rejilla (C2) o indeterminada (C4); magnitud siempre C4.",
        "estimacion": {
            "deficit_2030_nacional": {k: N5[k] for k in ("D_min", "D_central", "D_central_con_X", "D_max")},
            "cambio_2025_2030_nacional": {k: N5[k] for k in ("dD_min", "dD_central", "dD_central_con_X", "dD_max")},
            "direccion_nacional_2030": dir_nac[5],
            "recuento_provincias_2030": {"empeoran": e5[0], "mejoran": e5[1], "indeterminadas": e5[2], "B2_anterior": list(o)},
            "deficit_2035_nacional": {k: N10[k] for k in ("D_min", "D_central", "D_central_con_X", "D_max")},
            "direccion_nacional_2035": dir_nac[10],
            "recuento_provincias_2035": {"empeoran": e10[0], "mejoran": e10[1], "indeterminadas": e10[2]},
            "terminadas_equilibrio_anual_2026_2030": equil[5],
            "estres_ritmo_2006_2007": {"terminadas_anual_nacional": t0607, "dD_central_2030": stress[5]["dD_central"]},
            "envejecimiento": env.to_dict("records"),
        },
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "EXPLORATORIO (C4 en magnitud); la dirección nacional sube a C2 solo con signo único en toda la rejilla",
        "diagnosticos": {"control_sumas_fallos": fallos, "recuento_por_etapas": etapas_df.to_dict("records")},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": [
            "Proyección bajo supuestos, no pronóstico; AR(4) y ECM v1 no aplican (fuera_muestra null); Holm/BH no aplica (sin contrastes).",
            "Rejilla: terminadas = a (media 2023-25), b (cartera con retardo), c (tendencia 2021-25), lo (mínimo de a y b con el retardo más largo), "
            "opt (el mayor de: máximo anual 2019-2025 sostenido; cartera con el retardo más corto e iniciadas posteriores a 2025 en el máximo de 2021-25).",
            "Hogares: INE (central), mínimo y máximo entre INE y jefatura constante con población proyectada (B1); la tabla 54562 solo trae un escenario del INE.",
            "Bajas: tasa 0 (cota física, C2), central y máxima de T1 (C4) sobre el parque de 2024. Liberadas que no llegan al mercado (T2, C4): ninguna, mín., central, máx., que SUMAN a la necesidad efectiva; las liberadas no se restan.",
            "Estrés 2006-2007: no entra en la rejilla plausible; se informa como ritmo de equilibrio (terminadas necesarias para no empeorar) frente a la media nacional de 2006-2007.",
            "Dirección por provincia con las mismas reglas; D2025 de partida depende de la fuente (con/sin protegida) y de las bajas, y no altera el signo del cambio.",
            "El reparto 2026-2030 / 2031-2035 de las liberadas y de X es proporcional a las defunciones de 75+ (proyección INE x riesgo de muerte 2024 constante).",
            "Sin lenguaje causal.",
        ],
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1, default=float))

    txt_dir = {"empeora": "empeora", "mejora": "mejora", "indeterminado": "no tiene un signo único"}[dir_nac[5]]
    if dir_nac[5] == "empeora":
        ver_txt = ("El déficit nacional 2025-2030 empeora en todos los escenarios de la rejilla (dirección C2); por tanto la afirmación «se cerrará en pocos años» "
                   "no se sostiene en ninguno de ellos. La dirección C2 depende de que el rango plausible esté en la rejilla: unas terminadas sostenidas muy por encima del optimista o unos hogares claramente por debajo de la proyección baja del INE podrían cambiarla (umbrales en docs/v5_1/revision.md). La magnitud del aumento es C4.")
        veredicto, capa = "NO RESPALDADA", "C2"   # revisión v5.1 (B2): la afirmación falla en todos los escenarios de la rejilla
    else:
        ver_txt = ("El signo nacional del cambio del déficit no es único en la rejilla (dirección C4): la dirección y la magnitud quedan en C4.")
        veredicto, capa = "ANALIZADA, NO CONCLUYENTE", "C4"
    ficha = [{
        "id": "T4-V1", "actualiza": "B2-V1", "tema": "Cierre del déficit",
        "enunciado": "Al ritmo actual el déficit se cerrará en pocos años.",
        "capa": capa,
        "magnitud": (f"Dirección nacional 2025-2030 ({capa}): {txt_dir} en {len(out[5]['nacd'])} escenarios (terminadas: ritmo actual, cartera, tendencia, mínimo y optimista; "
                     f"hogares bajos, central y altos; bajas 0, central y máxima de T1; liberadas que no llegan al mercado: ninguna, mín., central y máx.). "
                     f"Magnitud (C4): el déficit pasa de {esc(N5['D_central'] - N5['dD_central'])} (2025, central: media de las fuentes con y sin protegida más bajas centrales de T1; {esc(base_con)} sin bajas y con protegida) a {esc(N5['D_central'])} a fin de 2030 al ritmo 2023-2025 "
                     f"(rango de la rejilla {esc(N5['D_min'])} a {esc(N5['D_max'])}); cambio {esc(N5['dD_central'])} (rango {esc(N5['dD_min'])} a {esc(N5['dD_max'])}). "
                     f"Para no empeorar harían falta unas {esc(equil[5]['central'])} terminadas al año frente a {esc(T_nac[5]['a'] / 5)} del ritmo actual y {esc(T_nac[5]['opt'] / 5)} del escenario optimista. "
                     f"Provincias: {e5[0]} empeoran, {e5[1]} mejoran y {e5[2]} indeterminadas (B2: {o[0]} / {o[1]} / {o[2]}). {ver_txt}"),
        "intervalo": f"cambio del déficit 2025-2030: {esc(N5['dD_min'])} a {esc(N5['dD_max'])} viviendas (C4); dirección nacional {capa}",
        "cota": "Dirección C2 solo si el signo es único en toda la rejilla; magnitud siempre C4" if capa == "C2" else "—",
        "literatura": "—",
        "veredicto": veredicto,
        "regla": "Criterio T4: la dirección sube a C2 solo si el signo se mantiene en TODOS los escenarios que cubren el rango plausible de terminadas, hogares, bajas y liberadas; "
                 "si no, C4. La magnitud es siempre C4 (con C4 el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE»). Actualiza B2-V1: misma afirmación.",
        "limites": "Terminadas aproximadas con libres terminadas más calificaciones definitivas de protegida; el retardo de la cartera es nacional; el escenario de 2006-2007 queda fuera "
                   "del rango plausible y se informa aparte; las bajas y las liberadas son C4 de fuente única; los rangos no son intervalos de confianza.",
        "evidencia": ["output/v5_1/T4/tablas/recuento_por_etapas.csv", "output/v5_1/T4/tablas/direccion_provincial_2030.csv",
                      "output/v5_1/T4/resultado.json"],
    }]
    (OUT / "fichas_verificador.json").write_text(json.dumps(ficha, ensure_ascii=False, indent=1, default=float))
    et = "\n".join(f"| {r.horizonte} | {r.etapa} | {r.n_escenarios} | {r.nacional} | {r.n_empeoran} / {r.n_mejoran} / {r.n_indeterminadas} |"
                   for r in etapas_df.itertuples())
    (OUT / "metodo.md").write_text(
        "# T4 · método\n\n"
        "dD = F − T + B + X por provincia (viviendas). Rejilla de 180 escenarios: terminadas (a, b, c, mínimo, optimista) × hogares (mínimo, central, máximo) × "
        "bajas de T1 (0, central, máxima) × liberadas que no llegan al mercado (ninguna, mínimo, central, máximo; suman a la necesidad efectiva).\n\n"
        "Criterio: la dirección (empeora o mejora) es C2 solo si el signo es el mismo en toda la rejilla; en otro caso C4. La magnitud es siempre C4.\n\n"
        "| horizonte | etapa | escenarios | nacional | empeoran / mejoran / indeterminadas |\n|---|---|---|---|---|\n" + et + "\n\n"
        f"Envejecimiento: liberadas centrales {esc(l5a)} en 2026-2030 y {esc(l5b)} en 2031-2035 (T2 repartido por defunciones de 75+: {esc(d5a)} y {esc(d5b)}). "
        "Fechas de datos: " + FECHA + ".\n")


if __name__ == "__main__":
    main()
