"""C1 (P-C1): turísticos -> alquiler por sección. H3-1 (efectos fijos) y H3-2 (shift-share leave-one-out).
Determinista y sin red. Orden: panel -> sellado inmediato -> P2 -> adelanto (P1) -> H3-1 -> H3-2 -> evaluación
sellada (una vez por hipótesis; si existe output/v3/C1/sellado_H3-*.json se lee, NO se vuelve a llamar) -> capa.
Uso: python src/v3/c1_run.py [--smoke]   (smoke: Barcelona, 99 réplicas, sin evaluación sellada)."""
import io
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c1_data as cd  # noqa: E402
import c1_est as ce  # noqa: E402
import c1_geo  # noqa: E402

from econ_utils import Registry  # noqa: E402

SMOKE = "--smoke" in sys.argv
OUT = cd.OUT / ("smoke" if SMOKE else "")
OUT.mkdir(parents=True, exist_ok=True)
REPS = 99 if SMOKE else 999
EER = 0.01
CIU6, CIU5 = list(cd.CIUDADES), cd.CIUDADES5
CTRL = list(cd.CTRL.values())
reg = Registry(OUT / "registro.csv")
R = {}          # resultados acumulados


def rlog(fase, mid, formula, r, notas=""):
    reg.log(fase, mid, formula, 2021, 2024, r.get("n", np.nan), r.get("r2w", np.nan), np.nan, np.nan,
            coef_interes=r.get("b", np.nan), p_interes=r.get("p", np.nan), notas=notas)


def f(x):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else float(x)


def resumen(r, extra=None):
    o = {k: f(r[k]) for k in ("b", "se", "lo", "hi", "p", "F", "sd_x") if k in r}
    o.update(n=int(r["n"]), G=int(r["G"]))
    o.update(extra or {})
    return o


# ------------------------------------------------------------------ normalización para fn (sellado y entrenamiento)
def norm(df):
    """Los códigos se regeneran desde 'codigo' (texto)."""
    d = df.copy()
    d["codigo"] = d.codigo.astype(str).str.zfill(10)
    d["muni"], d["distrito"], d["prov"] = d.codigo.str[:5], d.codigo.str[:7], d.codigo.str[:2]
    return d


def _est_h31(sub, reps):
    if sub.distrito.nunique() < 3 or sub.codigo.nunique() < 5:
        return {"error": "muestra insuficiente", "n": int(len(sub)), "G": int(sub.distrito.nunique())}
    r = ce.fit(sub, "vut100", keep=True)
    o = resumen(r)
    if r["G"] < 50:
        w = ce.wcb(r["yt"], r["xt"], r["xh"], r["cl"], reps=reps)
        o.update(wcb_p=w["p"], wcb_crit=w["crit"])
    return o


def _est_h32(pan, ciudades, reps, base="2108", nivel="muni", rel=True):
    sub = pan[pan.muni.isin(ciudades)]
    s = ce.shift(sub if nivel == "muni" else pan, base, nivel, rel)
    s = s[s.muni.isin(ciudades)]
    if s.distrito.nunique() < 3 or s.codigo.nunique() < 5:
        return {"error": "muestra insuficiente", "n": int(len(s)), "G": int(s.distrito.nunique())}
    r = ce.fit(s, "vut100", z=["z"], keep=True)
    o = resumen(r)
    if r["G"] < 50:
        w = ce.wcb(r["yt"], r["xt"], r["xh"], r["cl"], reps=reps)
        o.update(wcb_p=w["p"], wcb_crit=w["crit"])
    return o


def fn_h31(sel):
    """Especificación FIJADA de H3-1: ln alq SERPAVI (VC, mediana) ~ VUT/viviendas×100; FE sección + año×municipio;
    cluster distrito. Principal sellada = nacional; secundaria = 6 ciudades conjuntas."""
    pan, _ = cd.prep(norm(sel["c1_panel"]))
    out = {}
    for nom, sub in (("nacional", pan), ("6_ciudades", pan[pan.muni.isin(CIU6)])):
        try:
            out[nom] = _est_h31(sub, 999)
        except Exception as ex:  # noqa: BLE001  (el acceso sellado no se puede repetir)
            out[nom] = {"error": repr(ex)}
    return out


def fn_h32(sel):
    """Especificación FIJADA de H3-2: 2SLS de vut100 con z = cuota inicial (2021M08) × crecimiento LOO del municipio;
    FE sección + año×municipio; cluster distrito. Sellada principal = 6 ciudades; 5 ciudades y Palma aparte (P5)."""
    pan, _ = cd.prep(norm(sel["c1_panel"]))
    out = {}
    for nom, ciu in (("6_ciudades", CIU6), ("5_ciudades", CIU5), ("Palma", ["07040"])):
        try:
            out[nom] = _est_h32(pan, ciu, 999)
        except Exception as ex:  # noqa: BLE001
            out[nom] = {"error": repr(ex)}
    return out


def dry_run(fn, train):
    """Test en seco de fn con el mismo recorrido de (de)serialización que evaluate_v3 (CSV -> str -> numérico)."""
    buf = io.StringIO()
    train.to_csv(buf, index=False)
    buf.seek(0)
    d = pd.read_csv(buf, dtype={c: str for c in ("codigo", "distrito")})
    return fn({"c1_panel": d})


def evalua_sellado(hip, fn, train):
    """Una sola evaluación por hipótesis: si existe sellado_<hip>.json se lee; si no, se llama a evaluate_v3."""
    ruta = OUT / f"sellado_{hip}.json"
    if ruta.exists():
        return json.loads(ruta.read_text())
    if SMOKE:
        return {"smoke": "sin evaluación sellada", "dry_run": dry_run(fn, train)}
    dry_run(fn, train)                                  # si falla aquí, NO se abre el sellado
    from holdout import evaluate_v3
    try:
        res = evaluate_v3(hip, fn, "C1", ["c1_panel"])
        res = json.loads(json.dumps(res, default=str))
    except PermissionError as ex:                       # ya consumida: no hay JSON guardado
        res = {"error": "acceso ya consumido y sin resultado guardado", "detalle": str(ex)}
    except Exception as ex:  # noqa: BLE001
        res = {"error": "fallo dentro de evaluate_v3; NO se reintenta (acceso consumido)", "detalle": repr(ex)}
    ruta.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


# ------------------------------------------------------------------ utilidades de contraste
def emd(r, G_s, reps):
    """EMD = max(analítico t(G-1), calibrado por WCB) con potencia 0,80; la validación sellada se aproxima con el
    EE de entrenamiento reescalado por sqrt(G_ent/G_sellado) (aproximación declarada)."""
    G = r["G"]
    t80 = stats.t.ppf(0.80, G - 1)
    w = ce.wcb(r["yt"], r["xt"], r["xh"], r["cl"], reps=reps)
    emd_t = (stats.t.ppf(0.975, G - 1) + t80) * r["se"]
    emd_w = (w["crit"] + t80) * r["se"]
    se_s = r["se"] * np.sqrt(G / G_s)
    emd_s = (stats.t.ppf(0.975, G_s - 1) + stats.t.ppf(0.80, G_s - 1)) * se_s
    return {"se": r["se"], "G": G, "emd_t": emd_t, "emd_wcb": emd_w, "emd": max(emd_t, emd_w),
            "G_sellado": G_s, "se_sellado_aprox": se_s, "emd_sellado_aprox": emd_s,
            "estimable": bool(max(emd_t, emd_w) <= EER),
            "validacion_sellada": "potente" if emd_s <= EER else "no concluyente (EMD sellado > EER)"}


def lead_reg(lead, xcol):
    """Δ ln alquiler 2016-2020 sobre xcol con FE de municipio; cluster distrito; t(G-1)."""
    d = lead.dropna(subset=["dln_prev", xcol]).reset_index(drop=True)
    M = ce.absorb(d[["dln_prev", xcol]].values, [ce._codes(d.muni)])
    y, x = M[:, 0], M[:, 1]
    b = float(x @ y / (x @ x))
    e = y - b * x
    cl = ce._codes(d.distrito)
    G = cl.max() + 1
    S = np.bincount(cl, x * e, G)
    se = float(np.sqrt((S ** 2).sum() / (x @ x) ** 2 * G / (G - 1)))
    return {"b": b, "se": se, "p": float(2 * stats.t.sf(abs(b / se), G - 1)), "n": int(len(d)), "G": int(G)}


def efecto(b, lo, hi, dv, rent):
    """Magnitud: % del alquiler y €/mes para un aumento dv (pp de VUT/100 viviendas), con el alquiler medio."""
    pc = lambda v: 100 * (np.exp(v * dv) - 1)  # noqa: E731
    return {"dVUT_pp": float(dv), "alquiler_medio_eur_mes": float(rent), "pct": pc(b), "pct_ic95": [pc(lo), pc(hi)],
            "eur_mes": rent * pc(b) / 100, "eur_mes_ic95": [rent * pc(lo) / 100, rent * pc(hi) / 100]}


def adrh_panel(sub):
    a = sub[sub.anio.isin([2022, 2023]) & (sub.adrh > 0)].copy()
    ok = a.groupby("codigo").anio.nunique()
    a = a[a.codigo.isin(ok[ok == 2].index)].copy()
    a["lnadrh"] = np.log(a.adrh)
    return a


def bonferroni_bh(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    n = len(p)
    q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / (np.arange(n) + 1))[::-1])[::-1]
    return np.minimum(q, 1)


# ------------------------------------------------------------------ multiverso
def multiverso_h31(preps, cities, nombre):
    """Curva de especificaciones H3-1: resultado × tipo × FE de año × tratamiento × muestra × peso."""
    filas = []
    for res_, tipo, fe, trat, mues, peso in itertools.product(["mediana", "eur"], ["VC", "VU"], ["ym", "y"],
                                                              ["nivel", "delta", "log"], ["todas", "viv100"],
                                                              ["no", "viv"]):
        pan = preps[(tipo, res_, 100 if mues == "viv100" else 0)]
        if cities is not None:
            pan = pan[pan.muni.isin(cities)]
        if pan.distrito.nunique() < 3 or pan.codigo.nunique() < 5:
            continue
        x = {"nivel": "vut100", "delta": "vut100", "log": "lvut"}[trat]
        w = pan.drop_duplicates("codigo").set_index("codigo").viv if peso == "viv" else None
        wv = None if w is None else pan.codigo.map(w).values
        if trat == "delta" and wv is not None:        # el peso se asigna a las filas diferenciadas
            pan = pan.assign(_w=wv)
            dd = ce.diferencias(pan, ["lnalq", "vut100"])
            r = ce.fit(pan, x, fe=fe, fd=True, w=dd["_w"].values)
        else:
            r = ce.fit(pan, x, fe=fe, fd=(trat == "delta"), w=wv)
        filas.append(dict(resultado=res_, tipo=tipo, fe=fe, tratamiento=trat, muestra=mues, peso=peso,
                          b=r["b"], se=r["se"], p=r["p"], n=r["n"], G=r["G"], sd_x=r["sd_x"],
                          efecto_sd=r["b"] * r["sd_x"], lo_sd=r["lo"] * r["sd_x"], hi_sd=r["hi"] * r["sd_x"]))
        rlog("multiverso_H3-1", f"{nombre}|{res_}|{tipo}|{fe}|{trat}|{mues}|{peso}", "lnalq~VUT FE", filas[-1],
             "exploratorio; multiverso fuera de Holm")
    m = pd.DataFrame(filas)
    m["p_bh"] = bonferroni_bh(m.p.values)
    return m


def curva(m, nombre, ref_sign, ruta):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    m = m.sort_values("efecto_sd").reset_index(drop=True)
    fig, ax = plt.subplots(2, 1, figsize=(11, 7), gridspec_kw={"height_ratios": [2, 1.4]}, sharex=True)
    ax[0].errorbar(m.index, m.efecto_sd, yerr=[m.efecto_sd - m.lo_sd, m.hi_sd - m.efecto_sd], fmt="none",
                   ecolor="0.75", lw=0.8)
    ax[0].scatter(m.index, m.efecto_sd, c=np.where(m.p < 0.05, "tab:red", "tab:blue"), s=12, zorder=3)
    ax[0].axhline(0, c="k", lw=0.6)
    ax[0].axhline(m.efecto_sd.median(), c="tab:green", ls="--", lw=1)
    ax[0].set_ylabel("log-puntos de alquiler por 1 DT\nde variación intra-FE del tratamiento")
    ax[0].set_title(f"H3-1 curva de especificaciones ({nombre}); mediana {m.efecto_sd.median():.4f}; "
                    f"mismo signo {100 * (np.sign(m.efecto_sd) == ref_sign).mean():.0f} %; "
                    f"p<0,05 {100 * (m.p < 0.05).mean():.0f} %", fontsize=9)
    cats = [("resultado", ["mediana", "eur"]), ("tipo", ["VC", "VU"]), ("fe", ["ym", "y"]),
            ("tratamiento", ["nivel", "delta", "log"]), ("muestra", ["todas", "viv100"]), ("peso", ["no", "viv"])]
    yy = 0
    for c, vals in cats:
        for v in vals:
            sel = m[c] == v
            ax[1].scatter(m.index[sel], np.full(sel.sum(), yy), s=4, c="k")
            ax[1].text(-1, yy, f"{c}={v}", ha="right", va="center", fontsize=6)
            yy += 1
    ax[1].set_yticks([])
    fig.tight_layout()
    fig.savefig(ruta, dpi=130)
    plt.close(fig)


# ------------------------------------------------------------------ main
def main():
    print("[1] panel y sellado", flush=True)
    panel = cd.build_panel()
    conteos = cd.conteos_presello(panel)
    train = cd.seal_panel(panel)            # desde aquí solo entrenamiento
    del panel
    if SMOKE:
        train = train[train.muni == "08019"].copy()
    pan, lead = cd.prep(train)
    preps = {(t, r_, mv): cd.prep(train, t, r_, mv)[0] for t in ("VC", "VU") for r_ in ("mediana", "eur")
             for mv in (0, 100)}
    xy = c1_geo.centroides()
    rent = float(pan.alq_eur.mean()) if "alq_eur" in pan else float("nan")
    dv = float(lead.d_vut100.std())
    R["panel"] = {"filas_entrenamiento": int(len(train)), "secciones_main": int(pan.codigo.nunique()),
                  "distritos_main": int(pan.distrito.nunique()), "conteos_sellado_presello": conteos,
                  "alquiler_medio_eur_mes": rent, "sd_dVUT_2021_24_pp": dv}
    pan6 = pan[pan.muni.isin(CIU6)]
    pan5 = pan[pan.muni.isin(CIU5)]
    if SMOKE:
        pan6 = pan5 = pan
    # ---------------------------------------------------------------- P2
    print("[2] P2 EMD", flush=True)
    p2 = {}
    r_nac = ce.fit(pan, "vut100", keep=True)
    r_6 = ce.fit(pan6, "vut100", keep=True)
    s5 = ce.shift(pan5, "2108", "muni", True)
    r_iv = ce.fit(s5, "vut100", z=["z"], keep=True)
    gs = {k: max(v["distritos"], 2) for k, v in conteos.items()}
    p2["H3-1 nacional"] = emd(r_nac, gs["nacional"], REPS)
    p2["H3-1 6 ciudades"] = emd(r_6, gs["6 ciudades"], REPS)
    p2["H3-2 5 ciudades (sellada: 6 ciudades)"] = emd(r_iv, gs["6 ciudades"], REPS)
    p2["H3-2 5 ciudades (sellada: 6 ciudades)"]["F"] = f(r_iv["F"])
    pd.DataFrame(p2).T.to_csv(OUT / "p2_emd.csv")
    R["P2"] = {k: {a: (f(b) if isinstance(b, float) else b) for a, b in v.items()} for k, v in p2.items()}
    est31 = p2["H3-1 nacional"]["estimable"]
    est32 = p2["H3-2 5 ciudades (sellada: 6 ciudades)"]["estimable"]
    # ---------------------------------------------------------------- P1 test de adelanto
    print("[3] adelanto", flush=True)
    ad = {}
    L6 = lead[lead.muni.isin(CIU6)] if not SMOKE else lead
    for nom, ll in (("nacional", lead), ("6_ciudades", L6)):
        ad[nom] = {x: lead_reg(ll, x) for x in ("d_vut100", "vut100_2021")}
    s_all = ce.shift(pan5, "2108", "muni", True)
    zz = s_all.pivot(index="codigo", columns="anio", values="z")
    L5 = lead[lead.codigo.isin(zz.index)].copy()
    L5["d_z"] = L5.codigo.map(zz[2024] - zz[2021])
    L5["share0"] = 100 * L5.vut_2108 / L5.viv
    ad["H3-2_5_ciudades"] = {x: lead_reg(L5, x) for x in ("d_z", "share0")}
    rf = ce.fit(s_all, "z", keep=False)               # forma reducida principal (coef. de z)
    b_main = {"nacional": r_nac["b"], "6_ciudades": r_6["b"], "H3-2_5_ciudades": rf["b"]}
    for nom, v in ad.items():
        for x, r in v.items():
            r["pasa"] = bool(r["p"] > 0.10 and abs(r["b"]) < 0.5 * abs(b_main[nom]))
            r["b_principal_comparado"] = f(b_main[nom])
    pd.DataFrame([{"muestra": n, "regresor": x, **r} for n, v in ad.items() for x, r in v.items()]).to_csv(
        OUT / "adelanto.csv", index=False)
    R["adelanto"] = ad
    for n, v in ad.items():
        for x, r in v.items():
            rlog("adelanto_P1", f"{n}|{x}", "dln_alq_2016_20 ~ regresor + FE muni", r, f"pasa={r['pasa']}")
    pasa_ad31 = all(ad["nacional"][x]["pasa"] for x in ad["nacional"])
    pasa_ad32 = all(ad["H3-2_5_ciudades"][x]["pasa"] for x in ad["H3-2_5_ciudades"])

    # ---------------------------------------------------------------- H3-1
    print("[4] H3-1", flush=True)
    h31 = {"estimado": est31}
    if est31:
        pr = {}
        for nom, sub, rr in (("nacional", pan, r_nac), ("6_ciudades", pan6, r_6)):
            o = resumen(rr)
            w = ce.wcb(rr["yt"], rr["xt"], rr["xh"], rr["cl"], reps=REPS)
            o.update(wcb_p=w["p"], wcb_crit=w["crit"], wcb_ic95=[rr["b"] - w["crit"] * rr["se"],
                                                                 rr["b"] + w["crit"] * rr["se"]],
                     G_menor_50=bool(rr["G"] < 50))
            cy = ce.conley(rr, xy)
            o["conley"] = cy
            pm = ce.permutacion(rr, sub, "vut100", REPS)
            o["placebo_permutacion"] = pm
            pa = adrh_panel(sub)
            if pa.distrito.nunique() >= 3:
                ra = ce.fit(pa, "vut100", y="lnadrh")
                o["placebo_resultado_ADRH"] = resumen(ra) | {"anios": [2022, 2023]}
                rlog("placebo_resultado", f"H3-1|{nom}|ADRH", "ln renta hogar ~ VUT", ra)
            o["sensibilidad"] = ce.oster_rv(sub, "vut100", "lnalq", CTRL)
            o["magnitud"] = efecto(rr["b"], rr["lo"], rr["hi"], dv, rent)
            o["magnitud_1pp"] = efecto(rr["b"], rr["lo"], rr["hi"], 1.0, rent)
            pr[nom] = o
            rlog("H3-1_principal", nom, "lnalq ~ vut100 | seccion + anio x municipio", rr, f"cluster distrito G={rr['G']}")
        pc = {}
        for m_, nom in cd.CIUDADES.items():
            sub = pan[pan.muni == m_]
            if sub.distrito.nunique() >= 3:
                rr = ce.fit(sub, "vut100", keep=True)
                w = ce.wcb(rr["yt"], rr["xt"], rr["xh"], rr["cl"], reps=REPS)
                pc[nom] = resumen(rr, {"wcb_p": w["p"], "nota": "descriptivo; G<20"})
                rlog("H3-1_ciudad", nom, "lnalq ~ vut100 | FE", rr, "descriptivo")
        pr["por_ciudad_descriptivo"] = pc
        h31["principal"] = pr
        # multiverso
        print("    multiverso", flush=True)
        mv = {}
        for nom, ciu in (("nacional", None), ("6_ciudades", CIU6 if not SMOKE else None)):
            m = multiverso_h31(preps, ciu, nom)
            m.to_csv(OUT / f"multiverso_H3-1_{nom}.csv", index=False)
            ref = np.sign(pr[nom]["b"])
            curva(m, nom, ref, OUT / f"curva_especificaciones_H3-1_{nom}.png")
            mv[nom] = {"n_especificaciones": int(len(m)), "mediana_efecto_sd": f(m.efecto_sd.median()),
                       "mediana_b_por_tratamiento": {k: f(v) for k, v in m.groupby("tratamiento").b.median().items()},
                       "prop_mismo_signo_que_principal": f((np.sign(m.efecto_sd) == ref).mean()),
                       "prop_positivo": f((m.efecto_sd > 0).mean()), "prop_p05": f((m.p < 0.05).mean()),
                       "prop_p05_BH": f((m.p_bh < 0.05).mean())}
        h31["multiverso"] = mv
    R["H3-1"] = h31

    # ---------------------------------------------------------------- H3-2
    print("[5] H3-2", flush=True)
    h32 = {"estimado": est32}
    if est32:
        o = resumen(r_iv)
        w = ce.wcb(r_iv["yt"], r_iv["xt"], r_iv["xh"], r_iv["cl"], reps=REPS)
        o.update(wcb_p=w["p"], wcb_crit=w["crit"], wcb_ic95=[r_iv["b"] - w["crit"] * r_iv["se"],
                                                             r_iv["b"] + w["crit"] * r_iv["se"]])
        o["conley"] = ce.conley(r_iv, xy)
        o["primera_etapa_F"] = f(r_iv["F"])
        o["F_mayor_10"] = bool(r_iv["F"] > 10)
        o["placebo_permutacion_instrumento"] = ce.permutacion(r_iv, s5, "z", REPS, instr=True)
        pa = adrh_panel(s5)
        if pa.distrito.nunique() >= 3:
            ra = ce.fit(pa, "vut100", y="lnadrh", z=["z"])
            o["placebo_resultado_ADRH"] = resumen(ra) | {"anios": [2022, 2023]}
            rlog("placebo_resultado", "H3-2|ADRH", "ln renta hogar ~ VUT (IV)", ra)
        o["sensibilidad_2SLS"] = ce.oster_rv(s5, "vut100", "lnalq", CTRL, z=["z"])
        o["magnitud"] = efecto(r_iv["b"], r_iv["lo"], r_iv["hi"], dv, rent)
        o["magnitud_1pp"] = efecto(r_iv["b"], r_iv["lo"], r_iv["hi"], 1.0, rent)
        # forma reducida y MCO misma muestra
        o["forma_reducida_z"] = resumen(rf)
        o["MCO_misma_muestra"] = resumen(ce.fit(s5, "vut100"))
        rot = ce.rotemberg(s5, "vut100", "lnalq")
        rot["ciudad"] = rot.ciudad.map(cd.CIUDADES)
        rot.to_csv(OUT / "rotemberg_H3-2.csv", index=False)
        o["rotemberg"] = rot.round(5).to_dict("records")
        o["rotemberg_max_peso"] = {"ciudad": rot.loc[rot.alpha.abs().idxmax(), "ciudad"],
                                   "peso": f(rot.alpha.abs().max())}
        loo = {}
        for m_ in sorted(s5.muni.unique()):
            sub = s5[s5.muni != m_]
            if sub.distrito.nunique() >= 3:
                rr = ce.fit(sub, "vut100", z=["z"])
                loo[cd.CIUDADES[m_]] = resumen(rr)
        o["sin_ciudad"] = loo
        o["BHJ"] = ("No procede: el instrumento usa 5 shocks de ciudad (3 años) con exclusión de la propia sección, "
                    "no un conjunto grande de shocks idiosincráticos; la inferencia de Borusyak-Hull-Jaravel "
                    "exige muchos shocks. La validez descansa en las cuotas (GPSS): se reportan los pesos de "
                    "Rotemberg y la exclusión de cada ciudad.")
        rlog("H3-2_principal", "5 ciudades base 2021M08 LOO municipio", "2SLS lnalq~vut100|z", r_iv, f"F={r_iv['F']:.1f}")
        # multiverso H3-2
        filas = []
        for base, niv, rel in itertools.product(["2108", "2102"], ["muni", "prov"], [True, False]):
            try:
                ss = ce.shift(pan5 if niv == "muni" else pan, base, niv, rel)
                ss = ss[ss.muni.isin(CIU5)] if not SMOKE else ss
                rr = ce.fit(ss, "vut100", z=["z"])
            except Exception as ex:  # noqa: BLE001
                filas.append(dict(base=base, agregado=niv, crecimiento="rel" if rel else "abs", error=repr(ex)))
                continue
            filas.append(dict(base=base, agregado=niv, crecimiento="relativo" if rel else "absoluto", b=rr["b"],
                              se=rr["se"], p=rr["p"], F=rr["F"], n=rr["n"], G=rr["G"]))
            rlog("multiverso_H3-2", f"{base}|{niv}|{rel}", "2SLS", filas[-1], "exploratorio")
        m2 = pd.DataFrame(filas)
        m2.to_csv(OUT / "multiverso_H3-2.csv", index=False)
        ok = m2.dropna(subset=["b"]) if "b" in m2 else m2
        o["multiverso"] = {"n": int(len(ok)), "mediana_b": f(ok.b.median()),
                           "prop_mismo_signo": f((np.sign(ok.b) == np.sign(r_iv["b"])).mean()),
                           "prop_p05": f((ok.p < 0.05).mean()), "F_min": f(ok.F.min())}
        h32["principal"] = o
    R["H3-2"] = h32

    # ---------------------------------------------------------------- evaluación sellada
    print("[6] sellado", flush=True)
    sel = {}
    sel["H3-1"] = evalua_sellado("H3-1", fn_h31, train) if est31 else {"no_estimado": "EMD > EER"}
    sel["H3-2"] = evalua_sellado("H3-2", fn_h32, train) if est32 else {"no_estimado": "EMD > EER"}
    R["sellado"] = sel
    cierre(pan, lead, rent, dv)


def _sig(b, lo, hi):
    return bool(b is not None and b > 0 and lo > 0)


def _holm():
    h = pd.read_csv(cd.RAIZ / "output/v3/holm_v3.csv").set_index("hipotesis")
    return {k: f(h.loc[k, "p_holm"]) for k in ("H3-1", "H3-2")}


def cierre(pan, lead, rent, dv):
    capas = {}
    for hip, key_n, key_s in (("H3-1", "nacional", "nacional"), ("H3-2", "6_ciudades", "6_ciudades")):
        h = R[hip]
        if not h.get("estimado"):
            capas[hip] = {"capa": "C4", "motivo": "no detectable (EMD > EER): no se estima"}
            continue
        pr = h["principal"] if hip == "H3-2" else h["principal"]["nacional"]
        crit = {}
        pasa_ad = R["adelanto"]["nacional" if hip == "H3-1" else "H3-2_5_ciudades"]
        crit["a_adelanto"] = {"pasa": all(v["pasa"] for v in pasa_ad.values()),
                              "detalle": {x: {"p": f(v["p"]), "b": f(v["b"])} for x, v in pasa_ad.items()}}
        pm = pr.get("placebo_permutacion") or pr.get("placebo_permutacion_instrumento")
        ra = pr.get("placebo_resultado_ADRH")
        crit["b_placebos"] = {"pasa": bool(pm["size5"] <= 0.10),
                              "nota_ADRH": "P3: ADRH significativo (p<0,05) se informa sin invalidar automáticamente"
                              if ra is not None and ra["p"] < 0.05 else "ADRH no significativo",
                              "tamano_placebo_tratamiento": f(pm["size5"]),
                              "p_ADRH": f(ra["p"]) if ra else None, "p_aleatorizacion_real": f(pm["p_rand"])}
        se = pr.get("sensibilidad") or pr.get("sensibilidad_2SLS")
        mejor = max(se["r2_mejor_cov_y"], se["r2_mejor_cov_d"])
        crit["c_sensibilidad"] = {"pasa": bool(se["RV_q1"] > mejor and abs(se["delta_oster"]) > 1),
                                  "RV_q1": f(se["RV_q1"]), "R2_parcial_mejor_cov": f(mejor),
                                  "delta_oster": f(se["delta_oster"])}
        s = R["sellado"][hip]
        sk = s.get(key_s) if isinstance(s, dict) else None
        if sk and "b" in sk:
            crit["d_sellado"] = {"pasa": bool(sk["b"] > 0 and sk["lo"] > 0 and pr["b"] > 0),
                                 "b": sk["b"], "ic95": [sk["lo"], sk["hi"]], "p": sk["p"],
                                 "mismo_signo_que_entrenamiento": bool(np.sign(sk["b"]) == np.sign(pr["b"]))}
        else:
            crit["d_sellado"] = {"pasa": False, "nota": "sin resultado sellado utilizable", "detalle": s}
        crit["e_Holm_m4"] = {"pasa": None, "nota": "lo aplica el orquestador con el p sellado"}
        if hip == "H3-2":
            crit["F_primera_etapa_mayor_10"] = {"pasa": pr["F_mayor_10"], "F": pr["primera_etapa_F"]}
        key = "P2 sellada"
        p2k = "H3-1 nacional" if hip == "H3-1" else "H3-2 5 ciudades (sellada: 6 ciudades)"
        crit[key] = {"validacion_sellada": R["P2"][p2k]["validacion_sellada"]}
        base_ok = all(crit[k]["pasa"] for k in ("a_adelanto", "b_placebos", "c_sensibilidad", "d_sellado"))
        if hip == "H3-2":
            base_ok = base_ok and crit["F_primera_etapa_mayor_10"]["pasa"]
        base_ok = base_ok and crit[key]["validacion_sellada"] == "potente"
        falla = [k for k in ("a_adelanto", "b_placebos", "c_sensibilidad", "d_sellado") if not crit[k]["pasa"]]
        capas[hip] = {"capa": "C3 (condicionada a Holm)" if base_ok else "C4", "criterios": crit,
                      "fallan": falla + (["P2 sellada no concluyente"] if crit[key]["validacion_sellada"] != "potente"
                                         else [])}
    R["capas"] = capas
    h1, h2 = R["H3-1"], R["H3-2"]
    est = h1["principal"]["nacional"] if h1.get("estimado") else {}
    sell1 = R["sellado"]["H3-1"].get("nacional", {}) if isinstance(R["sellado"]["H3-1"], dict) else {}
    capa_final = "C3 (condicionada a Holm m=4)" if any(c["capa"].startswith("C3") for c in capas.values()) else "C4"
    HOLM = _holm()
    res = {
        "rama": "C1",
        "pregunta": "¿Se asocia más VUT por cada 100 viviendas de una sección con más alquiler SERPAVI? (H3-1 FE; "
                    "H3-2 shift-share leave-one-out)",
        "datos": "SERPAVI sección (VC, mediana €/m²; stock IRPF) 2016-2024; VUT INE oleada de agosto 2021-2024; "
                 "Censo 2021; ADRH (placebo). Sellado v3 por distrito; oleada 2026M05 fuera.",
        "N": est.get("n"),
        "metodo": "MCO con FE sección + año×municipio, cluster distrito (H3-1); 2SLS shift-share LOO (H3-2)",
        "estimacion": est.get("b"),
        "ic95": [est.get("lo"), est.get("hi")],
        "p_ajustado": HOLM,
        "p_sellado": {"H3-1": sell1.get("p"),
                      "H3-2": (R["sellado"]["H3-2"].get("6_ciudades") or {}).get("p")
                      if isinstance(R["sellado"]["H3-2"], dict) else None},
        "nivel_evidencia": "CAUSAL" if capa_final.startswith("C3") else "EXPLORATORIO",
        "capa": capa_final,
        "diagnosticos": {k: R[k] for k in ("P2", "adelanto", "capas")},
        "hipotesis": {"H3-1": h1, "H3-2": h2, "sellado": R["sellado"]},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None,
                          "nota": "no aplica: coeficientes de asociación entre secciones; la validación fuera de "
                                  "muestra es la evaluación sellada por distritos (no es un pronóstico, AR(4) y "
                                  "ECM v1 no comparables)"},
        "panel": R["panel"],
        "notas": "p_ajustado lo fija el orquestador (Holm m=4) con p_sellado. Estimación de entrenamiento: "
                 "H3-1 nacional. Magnitudes en hipotesis.*.principal.*.magnitud.",
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    print("capa:", capa_final, {k: v["capa"] for k, v in capas.items()})


if __name__ == "__main__":
    main()
