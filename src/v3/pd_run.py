"""P-D (capas C2/C4): simulaciones contrafactuales de cuatro políticas con RANGOS de parámetros.

Políticas: (1) viviendas por año para estabilizar el esfuerzo de acceso, (2) retirada de viviendas turísticas,
(3) topes de alquiler (coste-beneficio), (4) vivienda pública y movilización de vacías.
Criterio: dominancia en el rango y mínimo arrepentimiento máximo (regret) sobre la rejilla completa.
Determinista (SEED=20261010), sin red. Sin contrastes de hipótesis: no hay p-valores y no se aplica Holm/BH.

Uso:
    python3 src/v3/pd_run.py             # run completo -> output/v3/PD/
    python3 src/v3/pd_run.py --smoke     # rejilla de extremos -> carpeta temporal
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v3"))
import econ_utils  # noqa: E402
import pa_data as pdat  # noqa: E402

SEED = 20261010
HORIZ = 10  # 2026-2035
PA = RAIZ / "output" / "v3" / "PA"
PB = RAIZ / "output" / "v3" / "PB"

# Rangos de la literatura (docs/v3/literatura_v3.md, parte B). Cada uno con su fuente.
EPS = [0.3, 0.5, 0.75, 1.0, 1.5]            # |ε_d|: rango del encargo; sin estimación verificada para España (laguna 2)
ETA = [0.0, 0.45, 1.75]                      # elasticidad de oferta: 0 = fórmula del encargo; 0,45 BdE IA 2025; 1,75 Saiz (2010)
T_GL = (0.0122, 0.117)                       # objetivo T de la réplica GL (output/v3/GL/resultado.json), log-p por pp
BARRON = 0.018                               # elasticidad alquiler/anuncios (Barron et al. 2021)
JMS_CUT, JMS_CUT_EE = -0.045, 0.006          # Jofre-Monseny et al. 2023: renta
JMS_L, JMS_L_EE = -0.003, 0.021              # contratos (EE interpretado en puntos log; supuesto)
DIAMOND_L = -0.15                            # Diamond et al. 2019: oferta de alquiler en inmuebles afectados
Z = 1.96


def cargar() -> dict:
    d: dict = {}
    # --- A1: ritmo de hogares y terminadas
    comb = pd.read_csv(PA / "tablas" / "A1_nacional_combinaciones.csv")
    gh = []
    for per in ("2021-2025", "2022-2025"):
        c = comb[(comb.periodo == per) & (comb.protegida == "con") & (comb.bajas_pct == 0)]
        ny = int(c.t1.iloc[0] - c.t0.iloc[0] + 1)
        gh += list((c.delta_hogares / ny).values)
    d["gh_lo"], d["gh_hi"] = float(min(gh)), float(max(gh))
    d["dh_ecp_2225"] = float(comb[(comb.periodo == "2022-2025") & (comb.hogares_fuente == "Censo+ECP")].delta_hogares.iloc[0])
    m = pdat.mivau_nacional_anual()
    term = (m.libres + m.protegida.fillna(0)).loc[2021:2025]
    d["term_serie"] = {int(k): float(v) for k, v in term.items()}
    d["c0"] = [float(term.min()), float(term.mean()), float(term.max())]
    d["parque"] = float(m.parque.loc[2025])
    d["H0"] = float(pdat.censo2021_hogares_nacional()) + d["dh_ecp_2225"]
    # --- A2 y A3
    hechos = {h["id"]: h for h in json.load(open(PA / "hechos.json"))}
    d["A2"] = hechos["A2_hogares_implicitos"]["intervalo"]
    t3 = pd.read_csv(PA / "tablas" / "A3_vacias_por_tercil.csv")
    v = t3[(t3.tercil == "alto") & (t3.muestra == "todos con dato") & (t3.medida_vacia == "Censo 2021: vacías")]
    d["V_alto"] = [float(v.vacias.min()), float(v.vacias.max())]
    d["V_alto_tabla"] = v[["presion", "vacias"]].to_dict("records")
    # hogares del tercil alto (misma definición que pa_a23) para la lectura local
    base = pd.read_csv(PA / "tablas" / "A3_municipios_base.csv", dtype={"codigo": str})
    hh = {}
    for pc in ("ln_tasado_15_21", "ln_alq_15_21"):
        b = base[base[pc].notna() & base.vacias.notna()].copy()
        b["t"] = pd.qcut(b[pc].rank(method="first"), 3, labels=["bajo", "medio", "alto"])
        g = b[b.t == "alto"]
        hh[pc] = {"vacias": float(g.vacias.sum()), "hogares": float(g.hogares.sum())}
    d["H_alto"] = hh
    # --- B1: stock de alquiler, VUT y secciones
    sens = pd.read_csv(PB / "tablas" / "b1_nacional_sensibilidad.csv")
    s = sens[(sens.periodo == "2020M08-2024M08") & (sens.eps == 1)]
    d["R"] = [float(x) for x in sorted(s.stock_alquiler.unique())]
    d["VUT_fin"] = float(s.VUT_fin.iloc[0])
    d["dVUT"] = float(s.dVUT.iloc[0])
    d["cota_B1_pct"] = float(s.cota_cantidad_pct.max())
    sec = pd.read_csv(PB / "tablas" / "b1_secciones_ciudades.csv").dropna(subset=["peso_parque_pct", "viv_alquiler", "vut_2024M08", "viv_total"])
    umbral = sec.peso_parque_pct.quantile(0.9)
    top = sec[sec.peso_parque_pct >= umbral]
    d["sec"] = {"n_secciones": int(len(sec)), "n_top": int(len(top)), "umbral_pp": float(umbral), "V_top": float(top.vut_2024M08.sum()),
                "R_top": float(top.viv_alquiler.sum()), "w_top_pp": float(100 * top.vut_2024M08.sum() / top.viv_total.sum()),
                "V_ciudades": float(sec.vut_2024M08.sum()), "R_ciudades": float(sec.viv_alquiler.sum()),
                "por_ciudad": top.groupby("ciudad").agg(n=("codigo", "size"), vut=("vut_2024M08", "sum"), alq=("viv_alquiler", "sum")).reset_index().to_dict("records")}
    # --- renta de alquiler anual (SERPAVI 2023, mediana provincial) en €/año
    prov = pd.read_csv(PA / "tablas" / "A4_provincias.csv")
    ra = prov[prov.anio == 2023].alquiler_mes_serpavi.dropna() * 12
    d["Ra"] = [float(ra.quantile(0.1)), float(ra.median()), float(ra.quantile(0.9))]
    # --- C1 (H3-1) y C3 (H3-3a/b): se leen en tiempo de ejecución
    for k, ruta in (("C1", RAIZ / "output" / "v3" / "C1" / "resultado.json"), ("C3", RAIZ / "output" / "v3" / "C3" / "resultado.json")):
        d[k] = json.load(open(ruta)) if ruta.exists() else None
    return d


def rejilla(dims: dict) -> dict:
    """Producto cartesiano de las dimensiones, como vectores planos."""
    mesh = np.meshgrid(*[np.asarray(v, dtype=float) for v in dims.values()], indexing="ij")
    return {k: m.ravel() for k, m in zip(dims.keys(), mesh)}


def ext(v, smoke):
    return [v[0], v[-1]] if smoke else list(v)


def gap_acum(r, d):
    """Demanda acumulada menos oferta acumulada 2026-2035 con las terminadas actuales (viviendas)."""
    baj = r.b * d["parque"]
    return HORIZ * (r.gh + r.a * r.A2 / HORIZ + baj - r.c0) + r.arr * 2 * (max(r.gh, d["gh_lo"]) - r.c0 + baj)


# ------------------------------------------------------------------ política 1
def politica1(d, smoke, reg, tablas):
    A2lo, A2hi = d["A2"]
    g = rejilla({
        "gh": ext([0.5 * d["gh_lo"], d["gh_lo"], d["gh_hi"]], smoke),
        "a": ext([0, 0.5, 1], smoke), "A2": [A2lo, A2hi], "b": ext([0, 0.001, 0.002], smoke),
        "c0": ext(d["c0"], smoke), "arr": [0, 1], "mov": ext([0, 0.15, 0.30], smoke), "V": d["V_alto"]})
    bajas = g["b"] * d["parque"]
    gh_obs = np.maximum(g["gh"], d["gh_lo"])
    arr = g["arr"] * 2 * (gh_obs - g["c0"] + bajas) / HORIZ     # arrastre 2024-2025 repartido en el horizonte
    nec = g["gh"] + g["a"] * g["A2"] / HORIZ + bajas + arr - g["mov"] * g["V"] / HORIZ
    df = pd.DataFrame({**g, "necesarias": nec, "brecha": nec - g["c0"]})
    chk = df[(df.a == 0) & (df.b == 0) & (df.arr == 0) & (df.mov == 0)]
    assert np.allclose(chk.necesarias, chk.gh)    # sanidad: sin latentes, bajas, arrastre ni movilización
    tablas["t1_necesarias_rejilla.csv"] = df
    res = []
    for etiqueta, f in (("sin movilización", df.mov == 0), ("movilización 15 % del tercil alto", df.mov == 0.15), ("movilización 30 % del tercil alto", df.mov == 0.30)):
        s = df[f] if f.any() else df
        res.append({"movilizacion": etiqueta, "necesarias_min": s.necesarias.min(), "necesarias_p25": s.necesarias.quantile(.25),
                    "necesarias_mediana": s.necesarias.median(), "necesarias_p75": s.necesarias.quantile(.75), "necesarias_max": s.necesarias.max(),
                    "brecha_min": s.brecha.min(), "brecha_max": s.brecha.max(), "n_escenarios": len(s)})
    tablas["t1_necesarias_resumen.csv"] = pd.DataFrame(res)
    sin = df[df.mov == 0]
    tablas["t1_necesarias_por_hogares_latentes.csv"] = sin.groupby(["gh", "a"]).agg(necesarias_min=("necesarias", "min"), necesarias_max=("necesarias", "max")).reset_index()
    e = rejilla({"eps": ext(EPS, smoke), "eta": ext(ETA, smoke)})
    gs = sin.assign(gap_acum=[gap_acum(r, d) for r in sin.itertuples()])
    sq = pd.concat([pd.DataFrame({"eps": ee, "eta": hh, "pct": 100 * (np.exp(gs.gap_acum.values / d["H0"] / (ee + hh)) - 1)}) for ee, hh in zip(e["eps"], e["eta"])])
    tablas["t1_esfuerzo_2035_statu_quo.csv"] = sq.groupby(["eps", "eta"]).pct.agg(["min", "median", "max"]).reset_index()
    fil = []
    for K in (0, 25e3, 50e3, 100e3, 150e3, 200e3, 300e3):
        ok = tot = 0
        for ee, hh in zip(e["eps"], e["eta"]):
            p = (gs.gap_acum.values - HORIZ * K) / d["H0"] / (ee + hh)
            ok += int((p <= 1e-12).sum())
            tot += len(p)
        fil.append({"K_adicional_por_anio": K, "fraccion_rejilla_estabiliza": ok / tot, "n": tot})
    tablas["t1_estabiliza.csv"] = pd.DataFrame(fil)
    reg.log("P1", "P1_necesarias", "c* = Δh + a·A2/10 + bajas + arrastre − mov·V/10", 2026, 2035, len(df), np.nan, np.nan, np.nan,
            coef_interes=float(df.necesarias.median()), notas=f"rango {df.necesarias.min():.0f}-{df.necesarias.max():.0f}; terminadas 2021-25 {d['c0'][0]:.0f}-{d['c0'][2]:.0f}")
    reg.log("P1", "P1_statu_quo_2035", "p = (Σ demanda − Σ oferta)/H0/(ε+η)", 2026, 2035, len(sq), np.nan, np.nan, np.nan,
            coef_interes=float(sq.pct.median()), notas=f"% 2035 vs 2025: {sq.pct.min():.1f} a {sq.pct.max():.1f}")
    return df, gs, sq


# ------------------------------------------------------------------ opciones de política y arrepentimiento
def opciones(d, smoke, reg, tablas):
    s = d["sec"]
    mO2 = ["cantidad_eps", "T_GL_bajo", "T_GL_alto", "Barron"]
    beta_c1 = None
    if d["C1"] and isinstance(d["C1"].get("estimacion"), (int, float)):
        beta_c1 = float(d["C1"]["estimacion"])
        mO2.append("beta_H3-1")
    Ldim = [JMS_L + Z * JMS_L_EE, JMS_L, JMS_L - Z * JMS_L_EE, DIAMOND_L]
    cuts = [JMS_CUT - Z * JMS_CUT_EE, JMS_CUT, JMS_CUT + Z * JMS_CUT_EE]
    g = rejilla({
        "eps": ext(EPS, smoke), "eta": ext(ETA, smoke), "R": d["R"], "phimode": [0, 1], "s": ext([0, 0.5, 1], smoke),
        "m": ext(list(range(len(mO2))), smoke), "L": ext(Ldim, smoke), "cut": ext(cuts, smoke),
        "rho": ext([0, 0.5, 1], smoke), "V": d["V_alto"]})
    N = len(g["eps"])
    ed = g["eps"] + g["eta"]
    phi = np.where(g["phimode"] == 0, g["R"] / d["H0"], 0.5)
    opts: dict = {}
    sup: dict = {}
    meta: dict = {}

    def agrega(nombre, pol, dosis, dp, so):
        opts[nombre], sup[nombre], meta[nombre] = dp, so, (pol, dosis)

    agrega("O0_sin_politica", "Sin política", "0", np.zeros(N), np.zeros(N))
    for K in (25e3, 50e3, 100e3):
        U = HORIZ * K
        agrega(f"P1_construccion_{int(K / 1e3)}k_anio", "P1 construcción adicional", f"{int(K / 1e3)} mil/año", -phi * U / g["R"] / ed, np.full(N, U))
    for X in (0.25, 0.5, 1.0):
        ret = g["s"] * X * s["V_top"]
        loc = np.select([g["m"] == 0, g["m"] == 1, g["m"] == 2, g["m"] == 3],
                        [-ret / s["R_top"] / ed, -T_GL[0] * X * s["w_top_pp"], -T_GL[1] * X * s["w_top_pp"], -BARRON * X], default=np.nan)
        if beta_c1 is not None:
            loc = np.where(g["m"] == 4, -abs(beta_c1) * X * s["w_top_pp"], loc)   # unidad supuesta: log-p por pp (se declara en notas)
        agrega(f"P2_retirar_VUT_{int(X * 100)}pct", "P2 retirar VUT", f"{int(X * 100)} % en el decil superior de peso", loc * s["R_top"] / g["R"], ret)
    for kap in (0.05, 0.15, 0.30):
        agrega(f"P3_tope_cobertura_{int(kap * 100)}pct", "P3 topes de alquiler", f"cobertura {int(kap * 100)} % del stock de alquiler",
               kap * g["cut"] - g["L"] * kap / ed, g["L"] * kap * g["R"])
    for m in (0.10, 0.30):
        U = m * g["V"]
        agrega(f"P4_movilizar_{int(m * 100)}pct_vacias_alto", "P4 movilización de vacías", f"{int(m * 100)} % de las vacías del tercil alto", -phi * U / g["R"] / ed, U)
    for G in (10e3, 25e3):
        U = (1 - g["rho"]) * HORIZ * G
        agrega(f"P4_publica_{int(G / 1e3)}k_anio", "P4 vivienda pública", f"{int(G / 1e3)} mil/año (coste unitario = parámetro)", -phi * U / g["R"] / ed, U)
    names = list(opts)
    E = np.vstack([opts[k] for k in names])
    S = np.vstack([sup[k] for k in names])
    RG = E - E.min(axis=0)
    central = {"O0_sin_politica", "P1_construccion_50k_anio", "P2_retirar_VUT_50pct", "P3_tope_cobertura_15pct", "P4_movilizar_30pct_vacias_alto", "P4_publica_25k_anio"}
    idx_c = [i for i, k in enumerate(names) if k in central]
    Ec = E[idx_c]
    RGc = Ec - Ec.min(axis=0)
    filas = []
    tol = 1e-12
    for i, k in enumerate(names):
        e = E[i]
        pol, dosis = meta[k]
        filas.append({"opcion": k, "politica": pol, "dosis": dosis, "esfuerzo_min_pct": 100 * (np.exp(e.min()) - 1), "esfuerzo_mediana_pct": 100 * (np.exp(np.median(e)) - 1),
                      "esfuerzo_max_pct": 100 * (np.exp(e.max()) - 1), "oferta_min": S[i].min(), "oferta_max": S[i].max(),
                      "frac_mejora": float((e < -tol).mean()), "frac_empeora": float((e > tol).mean()),
                      "domina_debil": bool((e.max() <= tol) and (S[i].min() >= -tol)),
                      "domina_estricto": bool((e.max() < -tol) and (S[i].min() >= -tol)),
                      "regret_max_pp": 100 * RG[i].max(), "regret_medio_pp": 100 * RG[i].mean(),
                      "regret_max_dosis_central_pp": 100 * RGc[idx_c.index(i)].max() if i in idx_c else np.nan,
                      "frac_mejor": float((RG[i] <= tol).mean())})
        reg.log("P-D", k, "variación simulada del esfuerzo de acceso (log) en 2035 frente a sin política", 2026, 2035, N, np.nan, np.nan, np.nan,
                coef_interes=float(np.median(e)), notas=f"rango {e.min():.4f} a {e.max():.4f}; oferta {S[i].min():.0f} a {S[i].max():.0f}")
    tab = pd.DataFrame(filas)
    tablas["t5_regret_opciones.csv"] = tab
    mats = []
    for col, pref in (("eps", "eps"), ("L", "L"), ("eta", "eta")):
        for v in sorted(set(g[col])):
            f = g[col] == v
            mats.append(pd.Series(100 * RG[:, f].mean(axis=1), index=names, name=f"{pref}={v:+.3f}" if col == "L" else f"{pref}={v}"))
    mapa = pd.concat(mats, axis=1)
    tablas["t5_regret_mapa.csv"] = mapa.reset_index().rename(columns={"index": "opcion"})
    return dict(names=names, E=E, S=S, RG=RG, g=g, tab=tab, mapa=mapa, meta=meta, mO2=mO2, Ldim=Ldim, cuts=cuts)


# ------------------------------------------------------------------ política 3: coste-beneficio
def politica3(d, smoke, reg, tablas, O):
    g = rejilla({"eps": ext(EPS, smoke), "eta": ext(ETA, smoke), "R": d["R"], "Ra": d["Ra"], "L": ext(O["Ldim"], smoke),
                 "cut": ext(O["cuts"], smoke), "ell": ext([0.1, 0.25, 0.5], smoke)})
    ed = g["eps"] + g["eta"]
    por_inq = g["Ra"] * (-g["cut"]) * (1 + g["L"]) - np.maximum(-g["L"], 0) * g["ell"] * g["Ra"] - (-g["L"]) * g["Ra"] / ed
    ben_inq = g["Ra"] * (-g["cut"])
    filas = []
    for kap in (0.05, 0.15, 0.30):
        ncov = kap * g["R"]
        benef = ncov * (1 + g["L"]) * g["Ra"] * (-g["cut"])
        desv = np.maximum(-g["L"], 0) * ncov
        c_desv = desv * g["ell"] * g["Ra"]
        c_tras = -g["L"] * kap * g["R"] * g["Ra"] / ed
        neto = benef - c_desv - c_tras
        for nombre, v, u in (("beneficio_agregado", benef, "M€/año"), ("coste_desvio", c_desv, "M€/año"), ("coste_traspaso_no_cubiertos", c_tras, "M€/año"),
                             ("neto_agregado", neto, "M€/año"), ("contratos_cubiertos", ncov, "contratos"), ("contratos_desviados", desv, "contratos")):
            f = v / 1e6 if u == "M€/año" else v
            filas.append({"cobertura": kap, "magnitud": nombre, "unidad": u, "min": f.min(), "mediana": np.median(f), "max": f.max(),
                          "frac_neto_positivo": float((neto > 0).mean()) if nombre == "neto_agregado" else np.nan})
    tablas["t3_topes_coste_beneficio.csv"] = pd.DataFrame(filas)
    rows = []
    for Lv in sorted(set(g["L"])):
        f = g["L"] == Lv
        rows.append({"L_contratos": Lv, "neto_por_inquilino_min": por_inq[f].min(), "neto_por_inquilino_mediana": np.median(por_inq[f]),
                     "neto_por_inquilino_max": por_inq[f].max(), "frac_neto_positivo": float((por_inq[f] > 0).mean())})
    tablas["t3_neto_por_inquilino_rama.csv"] = pd.DataFrame(rows)
    rows = []
    for ev in sorted(set(np.round(ed, 4))):
        f = np.isclose(ed, ev)
        fd = f & (g["L"] == DIAMOND_L)
        rows.append({"eps_mas_eta": ev, "frac_neto_positivo": float((por_inq[f] > 0).mean()),
                     "frac_neto_positivo_solo_Diamond": float((por_inq[fd] > 0).mean()) if fd.any() else np.nan})
    tablas["t3_signo_por_eps_eta.csv"] = pd.DataFrame(rows)
    reg.log("P3", "P3_neto_por_inquilino", "Ra·|cut|·(1+L) − max(−L,0)·ℓ·Ra − (−L)·Ra/(ε+η)", 2026, 2035, len(ed), np.nan, np.nan, np.nan,
            coef_interes=float(np.median(por_inq)), notas=f"€/año por inquilino cubierto: {por_inq.min():.0f} a {por_inq.max():.0f}")
    return dict(por_inq=por_inq, ben_inq=ben_inq, g=g)


# ------------------------------------------------------------------ figuras
def figuras(d, gs, O, P3, fig_dir, smoke, df1):
    fig_dir.mkdir(parents=True, exist_ok=True)
    t = np.arange(0, HORIZ + 1)
    fig, ax = plt.subplots(figsize=(8, 5))
    base = gs.gap_acum.values
    for K, col in ((0, "#c0392b"), (50e3, "#2874a6"), (100e3, "#1e8449")):
        v = np.concatenate([100 * (np.exp((base - HORIZ * K) / d["H0"] / (ee + hh)) - 1) for ee in ext(EPS, smoke) for hh in ext(ETA, smoke)])
        q = np.percentile(v, [0, 10, 50, 90, 100])
        ax.fill_between(2025 + t, q[0] * t / HORIZ, q[4] * t / HORIZ, color=col, alpha=0.12)
        ax.fill_between(2025 + t, q[1] * t / HORIZ, q[3] * t / HORIZ, color=col, alpha=0.25)
        ax.plot(2025 + t, q[2] * t / HORIZ, color=col, label="terminadas actuales" if K == 0 else f"+{int(K / 1e3)} mil/año adicionales")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("variación simulada del esfuerzo frente a 2025 (%)")
    ax.set_title("Abanico de escenarios (mín-máx, p10-p90 y mediana)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / "fig1_abanico_esfuerzo.png", dpi=130)
    plt.close(fig)
    mapa = O["mapa"]
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(mapa.values, aspect="auto", cmap="viridis_r")
    ax.set_xticks(range(mapa.shape[1]))
    ax.set_xticklabels(mapa.columns, rotation=60, ha="right", fontsize=8)
    ax.set_yticks(range(mapa.shape[0]))
    ax.set_yticklabels(mapa.index, fontsize=8)
    ax.set_title("Mapa de arrepentimiento medio (puntos log x100) por escenario")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(fig_dir / "fig2_mapa_arrepentimiento.png", dpi=130)
    plt.close(fig)
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    ax = axs[0]
    for lab, f, col in (("sin movilización", df1.mov == 0, "#c0392b"), ("movilización 30 %", df1.mov == 0.30, "#2874a6")):
        s = df1[f] if f.any() else df1
        ax.hist(s.necesarias / 1e3, bins=30, alpha=0.5, color=col, label=lab)
    ax.axvspan(d["c0"][0] / 1e3, d["c0"][2] / 1e3, color="gray", alpha=0.3, label="terminadas MIVAU 2021-25")
    ax.set_xlabel("viviendas necesarias por año (miles)")
    ax.set_title("Políticas 1 y 4: necesarias frente a terminadas")
    ax.legend(fontsize=8)
    ax = axs[1]
    g = P3["g"]
    for Lv in sorted(set(g["L"])):
        f = g["L"] == Lv
        ax.vlines(Lv * 100, P3["por_inq"][f].min(), P3["por_inq"][f].max(), lw=8, color="#7d3c98", alpha=0.6)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("variación de contratos cubiertos, L (%)")
    ax.set_ylabel("neto por inquilino cubierto (€/año)")
    ax.set_title("Política 3: rango del neto por rama de contratos")
    fig.tight_layout()
    fig.savefig(fig_dir / "fig3_necesarias_y_topes.png", dpi=130)
    plt.close(fig)


# ------------------------------------------------------------------ principal
def main(smoke: bool = False):
    np.random.seed(SEED)
    out = Path(tempfile.mkdtemp(prefix="pd_smoke_")) if smoke else RAIZ / "output" / "v3" / "PD"
    (out / "tablas").mkdir(parents=True, exist_ok=True)
    reg = econ_utils.Registry(out / "registro.csv")
    d = cargar()
    tablas: dict = {}
    df1, gs, sq = politica1(d, smoke, reg, tablas)
    O = opciones(d, smoke, reg, tablas)
    P3 = politica3(d, smoke, reg, tablas, O)
    tab = O["tab"].set_index("opcion")
    g = O["g"]
    s = d["sec"]

    # ---------- política 2
    p2 = []
    for X in (0.25, 0.5, 1.0):
        for sv in (0, 0.5, 1):
            ret = sv * X * s["V_top"]
            p2.append({"X": X, "s": sv, "viviendas_devueltas": ret, "pct_stock_alquiler_secciones_top": 100 * ret / s["R_top"],
                       "pct_stock_alquiler_nacional_min": 100 * ret / max(d["R"]), "pct_stock_alquiler_nacional_max": 100 * ret / min(d["R"]),
                       "local_cantidad_eps_max_pct": -100 * ret / s["R_top"] / 0.3, "local_cantidad_eps_min_pct": -100 * ret / s["R_top"] / (1.5 + 1.75),
                       "local_T_bajo_pct": -100 * T_GL[0] * X * s["w_top_pp"], "local_T_alto_pct": -100 * T_GL[1] * X * s["w_top_pp"],
                       "local_Barron_pct": -100 * BARRON * X})
    p2 = pd.DataFrame(p2)
    tablas["t2_vut_efecto_local.csv"] = p2
    tablas["t2_vut_secciones_top.csv"] = pd.DataFrame(s["por_ciudad"]).assign(umbral_pp=s["umbral_pp"])
    tablas["t2_vut_contexto_B1.csv"] = pd.DataFrame([{"X": X, "viviendas_max_nacional": X * d["VUT_fin"], "pct_stock_alquiler_max": 100 * X * d["VUT_fin"] / max(d["R"]),
                                                      "cota_B1_nuevas_2020_24_pct": d["cota_B1_pct"]} for X in (0.1, 0.25, 0.5, 1.0)])

    # ---------- política 4
    sinm = df1[df1.mov == 0]
    brecha_lo, brecha_hi = float(sinm.brecha.min()), float(sinm.brecha.max())
    p4 = []
    for V, nom in zip(d["V_alto"], ("presión mínima", "presión máxima")):
        for m in (0, 0.1, 0.2, 0.3):
            u = m * V
            p4.append({"V_alto": V, "medida": nom, "movilizable_pct": 100 * m, "viviendas": u, "por_anio_10a": u / HORIZ,
                       "pct_brecha_acum_min": 100 * u / (HORIZ * brecha_hi), "pct_brecha_acum_max": 100 * u / (HORIZ * brecha_lo) if brecha_lo > 0 else np.nan})
    tablas["t4_movilizacion.csv"] = pd.DataFrame(p4)
    tablas["t4_vacias_tercil_alto_local.csv"] = pd.DataFrame([{"presion": k, **v, "movilizar_30pct_por_100_hogares": 100 * 0.3 * v["vacias"] / v["hogares"]} for k, v in d["H_alto"].items()])
    tablas["t4_coste_publico_parametro.csv"] = pd.DataFrame([{"parametro": "coste_unitario_publico_eur_por_vivienda", "valor": None,
                                                              "nota": "sin dato en data/ (solo hay un índice de costes, no €/vivienda); coste total = unidades × parámetro"}])

    par = [
        ("eps_d", f"{EPS}", "rango del encargo; sin estimación verificada para España (literatura_v3 B, laguna 2)"),
        ("eta_oferta", f"{ETA}", "0 = fórmula del encargo; 0,45 BdE IA 2025; 1,75 Saiz (2010)"),
        ("ritmo_hogares_anual", f"{0.5 * d['gh_lo']:.0f} / {d['gh_lo']:.0f} / {d['gh_hi']:.0f}", "A1 2021-25 y 2022-25 (EPA y Censo+ECP); el primer valor es el supuesto de desaceleración al 50 %"),
        ("latentes_A2", f"{d['A2']}", "A2 (C2), absorción 0, 50, 100 %"),
        ("bajas_anuales", "0, 0,1, 0,2 % del parque 2025", f"parque {d['parque']:.0f} (MIVAU); supuesto de A1"),
        ("terminadas_2021_25", f"{d['c0']}", f"MIVAU libres+protegida {d['term_serie']}"),
        ("H0_hogares", f"{d['H0']:.0f}", "Censo 2021 + ΔECP 2022-25"),
        ("stock_alquiler", f"{d['R']}", "PB: Censo 2021 y ECV2021×ECP"),
        ("V_alto_vacias", f"{d['V_alto']}", f"A3 Censo vacías tercil alto: {d['V_alto_tabla']}"),
        ("VUT_top", f"V={s['V_top']:.0f}, R={s['R_top']:.0f}, peso={s['w_top_pp']:.2f} pp", f"decil superior de peso VUT/parque en 6 ciudades (umbral {s['umbral_pp']:.2f} pp), PB b1_secciones_ciudades"),
        ("T_GL", f"{T_GL}", "output/v3/GL/resultado.json (T_pp_rango); extremo alto sin verificar"),
        ("Barron", f"{BARRON}", "Barron, Kung y Proserpio (2021), elasticidad alquiler/anuncios"),
        ("JMS", f"renta {JMS_CUT}±{Z * JMS_CUT_EE:.3f}; contratos {JMS_L}±{Z * JMS_L_EE:.3f}", "Jofre-Monseny et al. 2023; EE tomado en puntos log (supuesto)"),
        ("Diamond", f"{DIAMOND_L}", "Diamond, McQuade y Qian (2019), oferta en inmuebles afectados, San Francisco 1994"),
        ("perdida_desvio_ell", "0,1, 0,25, 0,5 de la renta anual", "SUPUESTO sin dato"),
        ("cobertura_topes", "5, 15, 30 % del stock de alquiler", "SUPUESTO; 15 % ≈ hogares en municipios con marca de zona tensionada en A3 (lectura de la marca por verificar)"),
        ("renta_anual_alquiler", f"{d['Ra']}", "SERPAVI 2023, p10/mediana/p90 provincial x12"),
        ("crowding_out_publica_rho", "0, 0,5, 1", "SUPUESTO sin dato"),
        ("fraccion_a_alquiler_phi", "R/H0 (proporcional) y 0,5", "SUPUESTO"),
        ("sustitucion_s", "0, 0,5, 1", "B1: 1:1 es el máximo (C2); límite inferior 0"),
        ("C1_H3-1", "presente" if d["C1"] else "ausente", "output/v3/C1/resultado.json; si ausente, solo literatura (marcado)"),
        ("C3_H3-3", "presente" if d["C3"] else "ausente", "output/v3/C3/resultado.json; si ausente, solo JMS y Diamond (marcado)"),
    ]
    tablas["parametros.csv"] = pd.DataFrame(par, columns=["parametro", "valor", "fuente_o_supuesto"])

    # ---------- resultados.json
    R: list = []

    def add(politica, metrica, lo, hi, unidad, robusta, depende, capa, limites, debil=None):
        R.append({"politica": politica, "metrica": metrica, "rango_min": None if lo is None else float(lo), "rango_max": None if hi is None else float(hi),
                  "unidad": unidad, "robusta_en_todo_el_rango": robusta, "domina_debilmente": debil, "depende_de": depende, "capa": capa, "limites": limites})

    yn = lambda b: "sí" if b else "no"  # noqa: E731
    marca_c13 = "" if (d["C1"] or d["C3"]) else " Resultados C1/C3 de la oleada 2 ausentes: solo rangos de literatura (marcado)."
    lim1 = ("Modelo log-lineal de stock-flujo con ε y η constantes; las terminadas MIVAU incluyen toda vivienda (no solo residencia habitual); "
            "las bajas son un supuesto; el balance contable no equivale a demanda insatisfecha a cualquier precio.")
    c0lo, c0hi = d["c0"][0], d["c0"][2]
    add("P1 estabilizar el esfuerzo", "viviendas necesarias por año 2026-2035 (sin movilización)", sinm.necesarias.min(), sinm.necesarias.max(), "viviendas/año", "sí",
        "ritmo de hogares, absorción de latentes (A2), bajas y arrastre 2024-25; no depende de ε ni de η (estabilizar exige oferta = demanda)", "C2", lim1)
    add("P1 estabilizar el esfuerzo", f"brecha frente a las terminadas 2021-25 ({c0lo / 1e3:.0f}-{c0hi / 1e3:.0f} mil/año)", sinm.brecha.min(), sinm.brecha.max(), "viviendas/año",
        yn(sinm.brecha.min() > 0), "el signo depende del ritmo de hogares (supuesto de desaceleración al 50 %) y de las bajas", "C2", lim1)
    add("P1 estabilizar el esfuerzo", "variación simulada del esfuerzo 2035 vs 2025 con el ritmo actual de terminadas", sq.pct.min(), sq.pct.max(), "%", yn(sq.pct.min() > 0),
        "depende de |ε_d|, η y del ritmo de hogares", "C4", "Condicional a ε (sin estimación verificada para España)." + marca_c13)
    m30 = df1[df1.mov == 0.30]
    add("P1 estabilizar el esfuerzo", "viviendas necesarias por año con movilización del 30 % del tercil alto", m30.necesarias.min(), m30.necesarias.max(), "viviendas/año", "sí",
        "supuesto de movilización (0-30 %)", "C2", lim1)
    for K in (25, 50, 100):
        o = tab.loc[f"P1_construccion_{K}k_anio"]
        add("P1 estabilizar el esfuerzo", f"variación del esfuerzo medio con +{K} mil/año adicionales", o.esfuerzo_min_pct, o.esfuerzo_max_pct, "%", yn(o.domina_estricto),
            "la magnitud depende de ε, η y de la fracción que llega al alquiler; signo < 0 en toda la rejilla", "C2", "Sin coste fiscal ni efecto sobre el suelo y la construcción.", yn(o.domina_debil))
    # P2
    for X in (0.25, 0.5, 1.0):
        add("P2 retirar turísticos", f"viviendas devueltas al alquiler (X = {int(X * 100)} % en secciones de mayor peso, 6 ciudades)", 0, X * s["V_top"], "viviendas", "no",
            "depende de la sustitución s (cota B1: máximo 1:1, mínimo 0)", "C2", "Cota superior de sustitución 1:1 (PB B1); no estima cuántas vuelven.")
        r = p2[p2.X == X]
        add("P2 retirar turísticos", f"variación local del alquiler (X = {int(X * 100)} %), método T de GL y Barron", r.local_T_alto_pct.min(), r.local_Barron_pct.max(), "% del alquiler de las secciones",
            "no", "depende del método (T de GL o Barron) y de X; H3-1 ausente, solo literatura", "C4",
            "Rango de literatura no verificado en España; la réplica propia de GL es NO REPLICADO; T alto sin verificar." + marca_c13)
        add("P2 retirar turísticos", f"variación local del alquiler (X = {int(X * 100)} %), vía cantidad B1 con ε", r.local_cantidad_eps_max_pct.min(), 0, "% del alquiler de las secciones", "no",
            "depende de ε, η y de s (nula si s = 0)", "C4", "Condicional a ε y s.")
    n2 = tab.loc["P2_retirar_VUT_50pct"]
    add("P2 retirar turísticos", "variación del esfuerzo medio nacional con X = 50 %", n2.esfuerzo_min_pct, n2.esfuerzo_max_pct, "%", yn(n2.domina_estricto),
        "efecto ≤ 0 en toda la rejilla y nulo si s = 0 en la vía de cantidad (domina débilmente); magnitud depende de s, ε, η y del método", "C2",
        "Solo seis ciudades; ponderación nacional por el stock de alquiler; sin costes ni variación del sector turístico.", yn(n2.domina_debil))
    # P3
    pi, bi = P3["por_inq"], P3["ben_inq"]
    add("P3 topes de alquiler", "reducción de renta por inquilino cubierto", bi.min(), bi.max(), "€/año", "sí", "reducción JMS (IC) y renta anual de alquiler", "C4",
        "Efecto de Jofre-Monseny et al. (Cataluña 2016-22) extrapolado; H3-3 ausente." if d["C3"] is None else "H3-3 presente (ver notas).")
    add("P3 topes de alquiler", "neto por inquilino cubierto (beneficio menos desvío y traspaso)", pi.min(), pi.max(), "€/año", yn(pi.min() > 0),
        "depende de la variación de contratos L (de +3,8 % a -15 %), de ε+η y de la pérdida por desvío ℓ", "C4", "ℓ es un supuesto sin dato; Diamond es San Francisco 1994, JMS es Cataluña.")
    ft = tablas["t3_topes_coste_beneficio.csv"]
    for kap in (0.05, 0.15, 0.30):
        f = ft[(ft.cobertura == kap) & (ft.magnitud == "neto_agregado")].iloc[0]
        add("P3 topes de alquiler", f"neto agregado con cobertura {int(kap * 100)} %", f["min"], f["max"], "M€/año", yn(f["min"] > 0), "depende de L, ε+η, ℓ y de la cobertura (supuesto)", "C4",
            "Valoración monetaria simplificada; sin costes administrativos ni efectos en calidad.")
    p3 = tab.loc["P3_tope_cobertura_15pct"]
    add("P3 topes de alquiler", "variación del esfuerzo medio de los inquilinos (cobertura 15 %)", p3.esfuerzo_min_pct, p3.esfuerzo_max_pct, "%", yn(p3.domina_estricto),
        f"el signo depende de L y de ε+η: baja en el {100 * p3.frac_mejora:.0f} % de la rejilla y sube en el {100 * p3.frac_empeora:.0f} %", "C4",
        "Incluye el traspaso de la oferta perdida a los inquilinos no cubiertos; la oferta baja en parte de la rejilla.", yn(p3.domina_debil))
    # P4
    for m in (0.1, 0.3):
        o = tab.loc[f"P4_movilizar_{int(m * 100)}pct_vacias_alto"]
        add("P4 movilización de vacías", f"viviendas aportadas ({int(m * 100)} % de las vacías del tercil alto)", m * d["V_alto"][0], m * d["V_alto"][1], "viviendas", "no",
            "depende del % movilizable (supuesto 0-30 %) y de la medida de presión", "C2", "Supuesto de movilización sin dato; las vacías incluyen segundas residencias y viviendas no aptas.")
        add("P4 movilización de vacías", f"variación del esfuerzo medio nacional ({int(m * 100)} %)", o.esfuerzo_min_pct, o.esfuerzo_max_pct, "%", yn(o.domina_estricto),
            "la magnitud depende de ε, η y de la fracción que llega al alquiler; signo < 0", "C2", "Movilización y localización supuestas; el efecto local en el tercil alto es mayor que el nacional.", yn(o.domina_debil))
    add("P4 movilización de vacías", "aporte máximo (30 %) como % de la brecha acumulada de P1", 100 * 0.3 * d["V_alto"][0] / (HORIZ * brecha_hi),
        100 * 0.3 * d["V_alto"][1] / (HORIZ * brecha_lo) if brecha_lo > 0 else None, "%", "no", "depende de la brecha de P1 y del % movilizable", "C2", "Brecha de P1 sin movilización.")
    for G in (10, 25):
        o = tab.loc[f"P4_publica_{G}k_anio"]
        add("P4 vivienda pública", f"variación del esfuerzo medio nacional ({G} mil/año; coste unitario = parámetro)", o.esfuerzo_min_pct, o.esfuerzo_max_pct, "%", yn(o.domina_estricto),
            "depende del desplazamiento de la construcción privada ρ (nulo si ρ = 1), ε y η", "C2", "Sin coste unitario en data/; coste total = unidades x parámetro (sin cifra inventada).", yn(o.domina_debil))
    # criterio
    mm = tab.regret_max_pp.idxmin()
    mmc = tab.regret_max_dosis_central_pp.idxmin()
    dom = [k for k in tab.index if tab.loc[k, "domina_estricto"]]
    domd = [k for k in tab.index if tab.loc[k, "domina_debil"] and k != "O0_sin_politica"]
    add("Criterio", "opciones que mejoran el esfuerzo en toda la rejilla sin reducir la oferta (estricto)", len(dom), len(tab) - 1, "n.º de opciones (de las evaluadas)", yn(dom),
        "; ".join(dom), "C2", "Dominancia frente a sin política, sin coste fiscal.")
    add("Criterio", "opciones que dominan débilmente (efecto ≤ 0 y oferta ≥ 0)", len(domd), len(tab) - 1, "n.º de opciones (de las evaluadas)", yn(domd), "; ".join(domd), "C2", "Incluye efectos nulos.")
    add("Criterio", f"mínimo arrepentimiento máximo, todas las dosis: {mm}", tab.loc[mm, "regret_max_pp"], tab.loc[mm, "regret_max_pp"], "puntos log x100", "no",
        "depende de las dosis consideradas (supuestos): la dosis mayor minimiza el arrepentimiento", "C4", "Arrepentimiento medido en esfuerzo medio nacional; sin costes.")
    add("Criterio", f"mínimo arrepentimiento máximo, dosis central: {mmc}", tab.loc[mmc, "regret_max_dosis_central_pp"], tab.loc[mmc, "regret_max_dosis_central_pp"], "puntos log x100", "no",
        "depende de la dosis central elegida", "C4", "Dosis centrales: P1 50 mil/año, P2 50 %, P3 15 %, P4 30 % y 25 mil/año.")

    tablas["resultados_tabla.csv"] = pd.DataFrame(R)
    for nom, df in tablas.items():
        df.to_csv(out / "tablas" / nom, index=False)
    json.dump(R, open(out / "resultados.json", "w"), ensure_ascii=False, indent=1)
    figuras(d, gs, O, P3, out / "figuras", smoke, df1)

    res = {
        "rama": "PD", "capa": "C2/C4 por resultado (ver resultados.json)",
        "pregunta": "Qué variación simulada del esfuerzo de acceso y de la oferta producen cuatro políticas en rangos de parámetros, y cuál domina o minimiza el arrepentimiento máximo",
        "datos": "output/v3/PA (A1-A4), output/v3/PB (B1), MIVAU terminadas 2021-25, literatura_v3 parte B; C1/C3 de oleada 2: " + ("presentes" if d["C1"] or d["C3"] else "ausentes (solo literatura, marcado)"),
        "N": {"escenarios_rejilla_politicas": int(len(g["eps"])), "escenarios_P1": int(len(df1)), "opciones": int(len(tab))},
        "metodo": "Simulación contrafactual stock-flujo log-lineal sobre rejilla completa de parámetros; dominancia y regret minimax; sin contrastes de hipótesis",
        "estimacion": {"P1_necesarias_mediana": float(sinm.necesarias.median()), "P1_necesarias_rango": [float(sinm.necesarias.min()), float(sinm.necesarias.max())],
                       "terminadas_2021_25_rango": [c0lo, c0hi], "minimax_regret_todas_dosis": mm, "minimax_regret_dosis_central": mmc,
                       "domina_estricto": dom, "domina_debil": domd},
        "ic95": None, "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO",
        "diagnosticos": {"sanidad_necesarias_igual_ritmo_hogares": "verificada (assert)", "FDR": "no aplica: sin p-valores",
                         "C1_resultado_json": "presente" if d["C1"] else "ausente", "C3_resultado_json": "presente" if d["C3"] else "ausente"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "no aplica: simulación con rangos, sin predicción fuera de muestra"},
        "notas": "Capa C2 solo para cantidades contables y signo bajo supuestos débiles; magnitudes de precio condicionales a ε (C4). Sin lenguaje causal. "
                 "Topes: JMS y Diamond son literatura externa; ℓ, cobertura, ρ, φ y las dosis son supuestos. Coste público = parámetro sin cifra.",
    }
    json.dump(res, open(out / "resultado.json", "w"), ensure_ascii=False, indent=1)
    reg.flush()
    print("salida:", out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    main(ap.parse_args().smoke)
