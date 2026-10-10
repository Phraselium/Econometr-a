"""B2 · Proyección del déficit provincial 2026-2030. Determinista, sin red (SEED=20261010, un hilo).

D2030 = D2025 + F(2026->2031) - T(2026-2030) + B(2026-2030), por provincia, en viviendas.
  D2025: déficit A4 2021-2025 con bajas 0 (reconciliado con el nacional); F: hogares proyectados INE (C2 como en B1);
  T: terminadas libres + protegidas definitivas (MIVAU); B: bajas = R de B1 / 10 por año (R acotado >= 0 como en B1).
Escenarios de T: (a) media 2023-25; (b) cartera con retardo iniciadas->terminadas; (c) tendencia 2021-25 (sensibilidad).
Uso: python3 src/v5/b2_run.py [--smoke]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
for p in ("src", "src/v3", "src/v4", "src/v5"):
    sys.path.insert(0, str(RAIZ / p))
import b1_run as b1  # noqa: E402
import econ_utils  # noqa: E402
import m1_run as m1  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v5" / "B2"
SMOKE = "--smoke" in sys.argv
Y0, Y1 = 2026, 2031          # stock a 1-ene; flujo 2026-2030 (5 años)
H = 5
FECHA = ("INE Proyección de Hogares 54562 (mod. 2026-06-17, base 1-ene-2026); INE Proyecciones de Población 36726; "
         "MIVAU Boletín Online (hasta 2025); A4 déficit 2021-2025 (ECP INE + MIVAU); B1 (R). Ejecución 2026-10-10")


def estima_retardo(I: pd.Series, T: pd.Series, t0: int, t1: int) -> float:
    """Retardo medio (años) entre iniciadas y terminadas: para cada año t, x tal que acumI(x) = acumT(t); L = media de t-x."""
    ci = I.cumsum()
    ct = T.cumsum()
    xs = np.arange(I.index.min() - 1, I.index.max() + 1)
    civ = np.concatenate([[0.0], ci.values])      # acumulado a fin de año (índice año-1 -> 0)
    ls = []
    for t in range(t0, t1 + 1):
        x = np.interp(ct[t], civ, xs)              # x: año (fin) en que iniciadas acumuladas igualan terminadas acumuladas de t
        ls.append(t - x)
    return float(np.mean(ls))


def interp_ini(serie: pd.Series, x: float, relleno: float) -> float:
    """Iniciadas en el instante x (años, interpolación lineal entre años); tras 2025 = relleno (supuesto)."""
    if x > 2025:
        return relleno
    ys = np.array(sorted(serie.index))
    return float(np.interp(x, ys, serie.reindex(ys).values))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tablas").mkdir(exist_ok=True)
    (OUT / "figuras").mkdir(exist_ok=True)
    reg = econ_utils.Registry(OUT / "registro.csv")
    b = pd.read_csv(RAIZ / "output/v5/B1/tablas/B1_provincias.csv", dtype={"cod_prov": str}).set_index("cod_prov")
    cods = list(b.index)
    if SMOKE:
        cods = ["46", "28", "52"]
    nombres = {c: b.loc[c, "provincia"] for c in cods}
    kcod = {c: b1.kn(nombres[c]) for c in cods}

    # ---- F: hogares INE 2026 -> 2031 (+ método alternativo de B1: jefatura constante con población proyectada)
    hp, hnac = b1.lee_proy_hogares()
    pp, _ = b1.lee_proy_pob()
    pob = pp[pp.e == -1].pivot(index="k", columns="anyo", values="valor")
    base = pd.DataFrame(index=cods)
    base["provincia"] = [nombres[c] for c in cods]
    base["hogares_2026"] = [hp.loc[kcod[c], Y0] for c in cods]
    base["hogares_2031"] = [hp.loc[kcod[c], Y1] for c in cods]
    base["F_ine"] = base.hogares_2031 - base.hogares_2026
    base["F_alt"] = [base.loc[c, "hogares_2026"] * (pob.loc[kcod[c], Y1] / pob.loc[kcod[c], Y0] - 1) for c in cods]
    base["F_min"] = base[["F_ine", "F_alt"]].min(axis=1)
    base["F_max"] = base[["F_ine", "F_alt"]].max(axis=1)
    base["F_central"] = base.F_ine

    # ---- D2025 (A4, bajas 0, reconciliado) y bajas B (R de B1, >= 0, 10 años -> anual)
    a4 = pd.read_csv(RAIZ / "output/v5/A4/tablas/A4_deficit_provincial_ECP_MIVAU.csv", dtype={"cod_prov": str})
    a4 = a4[a4.periodo == "2021-2025"].set_index("cod_prov")
    base["D2025"] = a4.deficit_bajas0.reindex(cods)
    for s in ("min", "central", "max"):
        base[f"B_{s}"] = b.loc[cods, f"R_{s}"].clip(lower=0) / 10 * H

    # ---- T: series anuales (libres terminadas + protegidas definitivas) e I (libres iniciadas + protegidas provisionales)
    mi = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    mp = pd.read_csv(RAW / "mivau_v2_protegida.csv")
    ex_l = {c: m1.UNIPROV.get(c) for c in cods}
    ex_p = {c: m1.UNIPROV_PROT.get(c) for c in cods}
    lt = b1.serie_prov(mi, "viv_libres_terminadas_anual", nombres, ex_l)
    pt = b1.serie_prov(mp, "prot_definitiva_anual", nombres, ex_p)
    li = b1.serie_prov(mi, "viv_libres_iniciadas_anual", nombres, ex_l)
    pi_ = b1.serie_prov(mp, "prot_provisional_anual", nombres, ex_p)

    def suma(a, c):
        return a.loc[c] if c in a.index else 0.0
    yrs = list(range(1991, 2026))
    Tp = {c: (suma(lt, c).reindex(yrs).fillna(0) + (suma(pt, c).reindex(yrs).fillna(0) if c in pt.index else 0)) for c in cods}
    Ip = {c: (suma(li, c).reindex(yrs).fillna(0) + (suma(pi_, c).reindex(yrs).fillna(0) if c in pi_.index else 0)) for c in cods}
    sin_prot = [c for c in cods if c not in pt.index]

    def nac(df, pat):
        s = df[(df.nivel == "nacional") & df.serie.str.contains(pat)].set_index("periodo").valor
        s.index = s.index.astype(int)
        return s.reindex(yrs).astype(float)
    Tn = nac(mi, "viv_libres_terminadas_anual") + nac(mp, "prot_definitiva_anual")
    In = nac(mi, "viv_libres_iniciadas_anual") + nac(mp, "prot_provisional_anual")

    # ---- retardo medio (nacional; rango por ventana de estimación)
    ventanas = {"2012-2025": (2012, 2025), "2016-2025": (2016, 2025), "2019-2025": (2019, 2025), "2022-2025": (2022, 2025),
                "2008-2025": (2008, 2025)}
    lags = {k: estima_retardo(In, Tn, *v) for k, v in ventanas.items()}
    Lc = float(np.median(list(lags.values())))
    Lmin, Lmax = min(lags.values()), max(lags.values())

    # ---- escenarios de T (suma 2026-2030 por provincia)
    rows = {}
    for c in cods:
        t, i = Tp[c], Ip[c]
        a_c = 5 * t.loc[2023:2025].mean()
        a_lo, a_hi = 5 * t.loc[2023:2025].min(), 5 * t.loc[2023:2025].max()
        relleno = float(i.loc[2023:2025].mean())

        def cart(L, i=i, relleno=relleno):
            return sum(interp_ini(i, y - L, relleno) for y in range(2026, 2031))
        bs = [cart(L) for L in (Lmin, Lc, Lmax)]
        b_c, b_lo, b_hi = cart(Lc), min(bs), max(bs)
        x = np.arange(2021, 2026)
        y = t.loc[2021:2025].values
        sl, ic = np.polyfit(x, y, 1)
        res = y - (sl * x + ic)
        se = np.sqrt((res ** 2).sum() / 3 / ((x - x.mean()) ** 2).sum())
        def tr(s, sl=sl, ic=ic):
            return sum(max(0.0, ic + s * yy) for yy in range(2026, 2031))
        # recta con pendiente alternativa que pasa por la media de 2021-25
        def tr2(s, y=y, x=x):
            return sum(max(0.0, y.mean() + s * (yy - x.mean())) for yy in range(2026, 2031))
        c_c, c_lo, c_hi = tr(sl), tr2(sl - se), tr2(sl + se)
        rows[c] = dict(Ta_central=a_c, Ta_min=a_lo, Ta_max=a_hi, Tb_central=b_c, Tb_min=b_lo, Tb_max=b_hi,
                       Tc_central=c_c, Tc_min=min(c_lo, c_hi), Tc_max=max(c_lo, c_hi))
    base = base.join(pd.DataFrame(rows).T)
    # relleno 2026+: iniciadas = media 2023-25 (supuesto). Envolvente (a)+(b) = rango principal; central = (a)
    base["T_central"] = base.Ta_central
    base["T_min"] = base[["Ta_min", "Tb_min"]].min(axis=1)
    base["T_max"] = base[["Ta_max", "Tb_max"]].max(axis=1)

    def d2030(F, T, B):
        return base.D2025 + F - T + B
    base["D2030_min"] = d2030(base.F_min, base.T_max, base.B_min)
    base["D2030_central"] = d2030(base.F_central, base.T_central, base.B_central)
    base["D2030_max"] = d2030(base.F_max, base.T_min, base.B_max)
    for s in ("min", "central", "max"):
        base[f"dD_{s}"] = base[f"D2030_{s}"] - base.D2025

    def signo(r):
        if r.dD_min > 0:
            return "empeora"
        if r.dD_max < 0:
            return "mejora"
        return "indeterminado"
    base["signo"] = base.apply(signo, axis=1)
    sg = {}
    for e in ("a", "b", "c"):
        dd = base.F_central - base[f"T{e}_central"] + base.B_central
        sg[e] = np.where(dd > 0, "empeora", "mejora")
        base[f"signo_central_{e}"] = sg[e]
    base["signo_estable_3esc"] = (base.signo_central_a == base.signo_central_b) & (base.signo_central_b == base.signo_central_c)
    # cota de la variante sin bajas (B=0) y cierre del déficit (años hasta D=0 al ritmo (a), si mejora)
    base["dD_anual_central"] = base.dD_central / H
    base["anios_cierre_central"] = np.where(base.dD_anual_central < 0, base.D2025.clip(lower=0) / -base.dD_anual_central, np.nan)
    base["capa"] = "C4"

    # ---- registro (todas las especificaciones)
    for c in base.index:
        r = base.loc[c]
        for e in ("a", "b", "c"):
            reg.log("B2", f"B2_T{e}_{c}", f"terminadas 2026-2030 escenario ({e}) central", 2026, 2030, H, np.nan, np.nan, np.nan,
                    np.nan, float(r[f"T{e}_central"]), np.nan, f"{r.provincia}; (c) solo sensibilidad; C4")
        reg.log("B2", f"B2_D2030_{c}", "D2030 = D2025 + F - T(a) + B", 2026, 2030, H, np.nan, np.nan, np.nan, np.nan,
                float(r.D2030_central), np.nan, f"{r.provincia}; signo {r.signo}; p ajustado no aplica (proyección, sin contraste)")
    for k, v in lags.items():
        reg.log("B2", f"B2_lag_{k}", "retardo medio iniciadas->terminadas (nacional, años)", k.split("-")[0], 2025, 1, np.nan,
                np.nan, np.nan, np.nan, v, np.nan, "ventana de estimación")
    if SMOKE:
        print(base[["provincia", "D2025", "F_central", "T_central", "B_central", "D2030_central", "signo"]].round(0))
        print(lags)
        return
    base.to_csv(OUT / "tablas" / "B2_provincias_completo.csv", float_format="%.2f", index_label="cod_prov")
    cols = ["provincia", "D2025", "D2030_min", "D2030_central", "D2030_max", "dD_min", "dD_central", "dD_max", "signo",
            "signo_central_a", "signo_central_b", "signo_central_c", "signo_estable_3esc", "anios_cierre_central"]
    base[cols].round(0).to_csv(OUT / "tablas" / "B2_deficit_2030_provincial.csv", index_label="cod_prov")
    pd.DataFrame([{"ventana": k, "retardo_anios": v} for k, v in lags.items()]
                 + [{"ventana": "central (mediana)", "retardo_anios": Lc}]).to_csv(OUT / "tablas" / "B2_retardo.csv", index=False,
                                                                                    float_format="%.3f")

    # ---- nacional y control de sumas (nacional calculado con series nacionales independientes)
    F_nac = float(hnac[Y1] - hnac[Y0])
    Ta_nac = 5 * float(Tn.loc[2023:2025].mean())
    a4n = pd.read_csv(RAIZ / "output/v5/A4/tablas/A4_reconciliacion_prov_nacional.csv")
    D0_nac = float(a4n[a4n.periodo == "2021-2025"].deficit_nac.iloc[0])
    tot = {k: float(base[k].sum()) for k in ("D2025", "F_central", "F_min", "F_max", "T_central", "T_min", "T_max", "B_min",
                                             "B_central", "B_max", "D2030_min", "D2030_central", "D2030_max", "Ta_central",
                                             "Tb_central", "Tc_central", "Tb_min", "Tb_max", "Tc_min", "Tc_max")}
    D2030_nac = D0_nac + F_nac - Ta_nac + tot["B_central"]
    control = [
        {"tabla": "hogares_proyectados_2031", "suma_provincial": float(base.hogares_2031.sum()), "nacional": float(hnac[Y1]),
         "tolerancia_rel": 0.001},
        {"tabla": "F_2026_2031", "suma_provincial": tot["F_central"], "nacional": F_nac, "tolerancia_rel": 0.01},
        {"tabla": "deficit_2025_A4", "suma_provincial": tot["D2025"], "nacional": D0_nac, "tolerancia_rel": 1e-6},
        {"tabla": "terminadas_2026_2030_esc_a", "suma_provincial": tot["Ta_central"], "nacional": Ta_nac, "tolerancia_rel": 0.01,
         "nota": "nacional = 5 x media 2023-25 de la serie nacional publicada (libres terminadas + protegidas definitivas)"},
        {"tabla": "deficit_2030_central", "suma_provincial": tot["D2030_central"], "nacional": D2030_nac, "tolerancia_rel": 0.01,
         "nota": "nacional con series nacionales de F y T y D2025 nacional; bajas = suma provincial (sin serie nacional independiente)"},
    ]
    for t in control:
        t["ok"] = abs(t["suma_provincial"] - t["nacional"]) <= t["tolerancia_rel"] * abs(t["nacional"]) + 1e-9
    (OUT / "control_sumas.json").write_text(json.dumps(control, ensure_ascii=False, indent=1))
    fallos = [t["tabla"] for t in control if not t["ok"]]
    print("control_sumas fallos:", fallos, [(t["tabla"], round(t["suma_provincial"]), round(t["nacional"])) for t in control])
    escenarios = pd.DataFrame([{"escenario": e, "T_central": tot[f"T{e}_central"], "F_central": tot["F_central"],
                                "D2030_central": tot["D2025"] + tot["F_central"] - tot[f"T{e}_central"] + tot["B_central"],
                                "n_prov_empeora": int((base[f"signo_central_{e}"] == "empeora").sum()),
                                "n_prov_mejora": int((base[f"signo_central_{e}"] == "mejora").sum())} for e in ("a", "b", "c")])
    escenarios.to_csv(OUT / "tablas" / "B2_escenarios_nacional.csv", index=False, float_format="%.0f")
    figura(base)
    escribe(base, tot, lags, Lc, control, fallos, escenarios, sin_prot, D0_nac, F_nac, Ta_nac)


def figura(f: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cen = pd.read_csv(RAW / "v5" / "municipio_centroides_utm30.csv", dtype={"codigo": str})
    cen["cod_prov"] = cen.codigo.str[:2]
    cen = cen[~cen.cod_prov.isin(["35", "38", "51", "52"])]
    xy = cen.groupby("cod_prov")[["x_m", "y_m"]].median()
    g = f.join(xy, how="inner")
    colores = {"empeora": "#b2182b", "mejora": "#2166ac", "indeterminado": "#999999"}
    fig, ax = plt.subplots(1, 2, figsize=(13, 7), gridspec_kw={"width_ratios": [1.1, 1]})
    ax[0].scatter(g.x_m / 1e3, g.y_m / 1e3, s=(g.dD_central.abs() / g.dD_central.abs().max() * 1500 + 30),
                  c=[colores[s] for s in g.signo], alpha=0.65, edgecolor="k", linewidth=0.4)
    for c, r in g.iterrows():
        ax[0].annotate(c, (r.x_m / 1e3, r.y_m / 1e3), fontsize=6, ha="center", va="center")
    ax[0].set_aspect("equal")
    ax[0].set_title("Cambio del déficit 2025 a 2030, ritmo actual (esc. a)\nrojo empeora · azul mejora · gris indeterminado "
                    "(rango cruza 0); tamaño ∝ |cambio central|; C4", fontsize=8)
    top = f.reindex(f.dD_central.abs().sort_values(ascending=False).index).head(20)
    yy = list(range(len(top)))[::-1]
    ax[1].barh(yy, top.dD_central, color=[colores[s] for s in top.signo])
    ax[1].errorbar(top.dD_central, yy, xerr=[top.dD_central - top.dD_min, top.dD_max - top.dD_central], fmt="none", ecolor="k", lw=0.7)
    ax[1].axvline(0, color="k", lw=0.6)
    ax[1].set_yticks(yy)
    ax[1].set_yticklabels(top.provincia, fontsize=7)
    ax[1].set_title("20 mayores cambios: central y rango mín-máx (viviendas, 2026-2030)", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "figuras" / "B2_mapa_signo.png", dpi=110, metadata={"Software": None})
    plt.close(fig)


def escribe(f, tot, lags, Lc, control, fallos, esc, sin_prot, D0_nac, F_nac, Ta_nac) -> None:
    n = f.signo.value_counts().to_dict()
    nest = int(f.signo_estable_3esc.sum())
    dn = {s: tot[f"D2030_{s}"] for s in ("min", "central", "max")}
    d25 = tot["D2025"]
    cambio = {s: dn[s] - d25 for s in dn}
    cierre = None
    if cambio["central"] < 0:
        cierre = d25 / (-cambio["central"] / H)
    nac_signo = "empeora" if cambio["min"] > 0 else ("mejora" if cambio["max"] < 0 else "indeterminado")
    sg_e = {r.escenario: ("mejora" if r.D2030_central < d25 else "empeora") for r in esc.itertuples()}
    fd = FECHA
    hechos = [
        {"id": "B2-H1", "indicador": "Déficit acumulado nacional a fin de 2030 (suma de 52 provincias, escenario a)", "valor": round(dn["central"]),
         "min": round(dn["min"]), "max": round(dn["max"]), "unidad": "viviendas", "periodo": "1-ene-2026 a 31-dic-2030",
         "cobertura": "España (52 provincias)", "fuentes": ["A4", "INE 54562", "MIVAU", "B1"], "capa": "C4", "fecha_dato": fd},
        {"id": "B2-H2", "indicador": "Déficit 2021-2025 de partida (bajas 0)", "valor": round(d25), "min": round(d25), "max": round(d25),
         "unidad": "viviendas", "periodo": "2021-2025", "cobertura": "España (52 provincias)", "fuentes": ["ECP INE", "MIVAU"],
         "capa": "C4", "fecha_dato": "ECP 2021-2025; MIVAU hasta 2025"},
        {"id": "B2-H3", "indicador": "Crecimiento de hogares proyectado INE 2026-2030", "valor": round(F_nac),
         "min": round(tot["F_min"]), "max": round(tot["F_max"]), "unidad": "hogares", "periodo": "1-ene-2026 a 1-ene-2031",
         "cobertura": "España", "fuentes": ["INE 54562", "INE 36726"], "capa": "C2", "fecha_dato": "INE 2026-06-17"},
        {"id": "B2-H4", "indicador": "Terminadas 2026-2030, ritmo actual (5 x media 2023-25)", "valor": round(Ta_nac),
         "min": round(tot["T_min"]), "max": round(tot["T_max"]), "unidad": "viviendas", "periodo": "2026-2030",
         "cobertura": "España", "fuentes": ["MIVAU"], "capa": "C4", "fecha_dato": "MIVAU hasta 2025"},
        {"id": "B2-H5", "indicador": "Retardo medio iniciadas-terminadas (nacional)", "valor": round(Lc, 2),
         "min": round(min(lags.values()), 2), "max": round(max(lags.values()), 2), "unidad": "años", "periodo": "ventanas 2008-2025 a 2022-2025",
         "cobertura": "España", "fuentes": ["MIVAU"], "capa": "C4", "fecha_dato": "MIVAU hasta 2025"},
        {"id": "B2-H6", "indicador": "Provincias que empeoran / mejoran / indeterminadas (rango completo)",
         "valor": n.get("empeora", 0), "min": n.get("mejora", 0), "max": n.get("indeterminado", 0), "unidad": "provincias",
         "periodo": "2025 a 2030", "cobertura": "52 provincias (valor=empeora, min=mejora, max=indeterminado)",
         "fuentes": ["B2"], "capa": "C4", "fecha_dato": fd},
    ]
    esc_txt = {r.escenario: round(r.D2030_central) for r in esc.itertuples()}
    res = {
        "rama": "B2",
        "pregunta": "¿Mejora o empeora el déficit 2026-2030 por provincia al ritmo actual?",
        "capa": "C4",
        "datos": ["INE Proyección de Hogares 54562", "INE Proyecciones de Población 36726", "MIVAU iniciadas/terminadas libres",
                  "MIVAU protegida (definitivas y provisionales)", "A4 déficit 2021-2025", "B1 R (bajas)"],
        "N": int(len(f)),
        "metodo": "D2030 = D2025 + F - T + B por provincia; T con 3 escenarios (a media 2023-25; b cartera con retardo; c tendencia, "
                  "sensibilidad); rango = F_min/F_max, envolvente de T(a,b), B_min/B_max; signo por rango completo",
        "estimacion": {"deficit_2030_nacional": dn, "deficit_2025_nacional": d25, "cambio_2025_2030_nacional": cambio,
                       "signo_nacional_rango": nac_signo, "signo_nacional_por_escenario_central": sg_e,
                       "deficit_2030_central_por_escenario": esc_txt, "n_provincias_por_signo": n,
                       "n_prov_signo_estable_3_escenarios": nest, "retardo_anios": {"central": Lc, **lags},
                       "anios_cierre_nacional_si_mejora_ritmo_actual": cierre},
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "EXPLORATORIO (C4: proyección con supuestos; solo F es C2)",
        "diagnosticos": {"control_sumas_fallos": fallos, "provincias_sin_serie_protegida": sin_prot},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": [
            "Proyección bajo supuestos, no pronóstico; AR(4) y ECM v1 no aplican (fuera_muestra null); Holm/BH no aplica (sin contrastes).",
            "Supuestos: (1) D2025 = A4 con bajas 0; (2) bajas = R de B1 (acotado >= 0) / 10 por año, R es límite inferior no informativo; "
            "(3) terminadas = libres terminadas + protegidas definitivas (calificaciones definitivas como proxy); "
            "(4) en (b) las iniciadas posteriores a 2025 = media 2023-25 y el retardo nacional se aplica a todas las provincias; "
            "(5) hogares INE = escenario del INE, sin reacción a la oferta; no hay ajuste de A2, V, M ni L.",
            "Rango: mínimo = F_min, T máximo (envolvente a-b), B_min; máximo al revés; son cotas, no IC.",
            "Escenario (c) es solo sensibilidad y no entra en el rango principal.",
            "Sin lenguaje causal: se describen magnitudes proyectadas, no efectos.",
        ],
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1, default=float))
    ficha = [{
        "id": "B2-V1", "tema": "Cierre del déficit",
        "enunciado": "Al ritmo actual el déficit se cerrará en pocos años.",
        "capa": "C4",
        "magnitud": ("Déficit acumulado nacional 2021-2025: %.0f viviendas. Proyección a fin de 2030 al ritmo 2023-2025 (suma de provincias): "
                     "%.0f central (rango %.0f a %.0f). Cambio frente a 2025: %.0f (rango %.0f a %.0f); signo nacional: %s. "
                     "Provincias con rango completo: %d empeoran, %d mejoran, %d indeterminadas. Escenarios centrales a fin de 2030: "
                     "a %.0f, b %.0f, c %.0f." % (d25, dn["central"], dn["min"], dn["max"], cambio["central"], cambio["min"], cambio["max"],
                                                  nac_signo, n.get("empeora", 0), n.get("mejora", 0), n.get("indeterminado", 0),
                                                  esc_txt["a"], esc_txt["b"], esc_txt["c"])),
        "intervalo": "%.0f a %.0f viviendas de déficit a fin de 2030 (C4)" % (dn["min"], dn["max"]),
        "cota": "—", "literatura": "—",
        "veredicto": "ANALIZADA, NO CONCLUYENTE",
        "regla": "Proyección C4 (supuestos de bajas, retardo y ritmo constante); solo F (INE) es C2. Con C4 el máximo es ANALIZADA, NO CONCLUYENTE. "
                 "Se informa el signo solo donde el rango completo no cruza cero.",
        "limites": "Sin ajuste por atraso latente, vacías ni vivienda liberada; protegida medida con calificaciones definitivas; "
                   "rangos no son IC; el retardo es nacional.",
        "evidencia": ["output/v5/B2/tablas/B2_deficit_2030_provincial.csv", "output/v5/B2/resultado.json"],
    }]
    (OUT / "fichas_verificador.json").write_text(json.dumps(ficha, ensure_ascii=False, indent=1, default=float))
    (OUT / "metodo.md").write_text(
        "# B2 · método\n\nD2030 = D2025 + F(2026-31) - T(2026-30) + B(2026-30), en viviendas por provincia. "
        "Cambio = D2030 - D2025; empeora si el mínimo > 0, mejora si el máximo < 0, indeterminado si el rango cruza 0.\n"
        "Escenarios T: (a) media 2023-25; (b) cartera, T(y) = iniciadas(y - L) con L estimado por igualdad de acumulados, "
        "iniciadas tras 2025 = media 2023-25; (c) tendencia lineal 2021-25 (sensibilidad).\n"
        "Fechas de datos: " + FECHA + ".\n")


if __name__ == "__main__":
    main()
