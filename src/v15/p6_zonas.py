"""V15-A · H1 y H2 (P6a/P6b): zonas tensionadas en Cataluña, renta y contratos nuevos (Incasòl). SOLO entrenamiento.

Especificación: docs/v15/preregistro_v15.md (H1, H2) + adendas 1 y 2 + docs/v15/desviaciones.md (DV15-A).
Inferencia NO APTA (SDID placebo, Webb, Honest DiD, control sintético): estimación puntual, sin p ni IC.
Ejecución: python3 src/v15/p6_zonas.py   (SEED 20261010). Nada de muestra sellada.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pa_comun import FECHA, OUT, SEED, centroides_municipio, registrar, volcar, xyz_km  # noqa: E402
import pa_did as D  # noqa: E402
from econ_utils import Registry  # noqa: E402

SALIDA = OUT / "p6"
QS = D.QUARTERS
FINES = {"2026T1": "2026T1", "2025T4": "2025T4"}


def preparar():
    P = D.construir_panel()
    N, R, coh = P["N"], P["R"], P["coh"]
    cen = centroides_municipio().set_index("cod").reindex(N.index)
    xyz = xyz_km(cen.lon.values, cen.lat.values)
    return N, R, coh.values, xyz


def distancia_a_tratado(xyz, coh, mask):
    from scipy.spatial import cKDTree
    tr = np.isin(coh, [D.G1, D.G4]) & mask
    d = np.full(len(coh), np.nan)
    d[:] = cKDTree(xyz[tr]).query(xyz)[0]
    return d


def especificacion(Y, N, coh, xyz, estim, umbral, radio, fin, mask_extra=None):
    """Una celda del multiverso. Devuelve dict con att (log) y metadatos."""
    pre_mean = N[:, :7].mean(axis=1)
    mask = pre_mean >= umbral
    if mask_extra is not None:
        mask &= mask_extra
    dist = distancia_a_tratado(xyz, coh, mask)
    don = (dist >= radio) if radio > 0 else np.ones(len(coh), bool)
    sub = mask
    Ys, cs, ds = Y[sub], coh[sub], don[sub]
    out = {"estimador": estim, "umbral": umbral, "radio_km": radio, "fin": fin}
    if estim == "CS":
        cel = D.cs_celdas(Ys, cs, QS, fin, "todos", ds)
        out["att"] = D.cs_agregar(cel)
        out["n_tr"] = int(np.isin(cs, [D.G1, D.G4]).sum())
        out["n_donantes"] = int(((cs == "nunca") & ds).sum())
    else:
        r = D.sdid_cohortes(Ys, cs, QS, fin, ds)
        out["att"] = r["att"]
        out["n_tr"] = r.get("n_tr")
        out["n_donantes"] = r["n_donantes"]
        out["contraste_2023T3_T4"] = r.get("contraste")
        out["degenerada"] = bool(r["n_donantes"] < 3)
    return out


def balance(Rl, Nl, coh, xyz):
    """Balance de preperiodo (tratados frente a nunca tratados) y soporte común de la renta media previa."""
    tr = np.isin(coh, [D.G1, D.G4])
    pr = np.nanmean(Rl[:, :7], axis=1)
    pn = np.log(Nl[:, :7].mean(axis=1))
    out = {}
    for nom, v in (("log_renta_pre", pr), ("log_contratos_pre", pn)):
        a, b = v[tr], v[~tr]
        a, b = a[np.isfinite(a)], b[np.isfinite(b)]
        sd = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
        out[nom] = {"media_tratados": float(a.mean()), "media_donantes": float(b.mean()), "dif_tipificada": float((a.mean() - b.mean()) / sd), "n_tr": len(a), "n_don": len(b)}
    lo, hi = np.nanpercentile(pr[tr], [5, 95])
    soporte = int((~tr & (pr >= lo) & (pr <= hi)).sum())
    out["donantes_en_soporte_comun_renta"] = soporte
    out["soporte_comun_menos_30"] = bool(soporte < 30)
    return out


def pretendencias(Y, coh, donantes=None):
    ev = D.cs_eventos(Y, coh, QS, donantes)
    pre = ev[ev.t < ev.g.map(lambda g: D.idx_periodo(D.periodo_idx(g) - 1))]
    # ponderar por n_tr
    pre = pre.dropna(subset=["coef"])
    pend = np.polyfit(pre.e.values, pre.coef.values, 1)[0] * 4 if len(pre) > 2 else np.nan  # por año
    return {"max_abs_pre": float(pre.coef.abs().max()), "media_pre": float(np.average(pre.coef, weights=pre.n_tr)),
            "pendiente_lineal_por_anio": float(pend), "n_coef_pre": int(len(pre)), "eventos": ev}


def permutaciones(Y, coh, R_perm, seed_off, sdid_R=0):
    rng = np.random.default_rng([SEED, 6, seed_off])
    sub = np.arange(len(coh))
    n1, n4 = int((coh == D.G1).sum()), int((coh == D.G4).sum())
    cs_att, sd_att = [], []
    for k in range(R_perm):
        perm = rng.permutation(sub)
        c = np.array(["nunca"] * len(coh), dtype=object)
        c[perm[:n1]] = D.G1
        c[perm[n1:n1 + n4]] = D.G4
        cs_att.append(D.cs_agregar(D.cs_celdas(Y, c, QS, "2026T1")))
        if k < sdid_R:
            sd_att.append(D.sdid_cohortes(Y, c, QS, "2026T1")["att"])
    f = lambda a: {"n": len(a), "media": float(np.nanmean(a)), "dt": float(np.nanstd(a, ddof=1)), "p2_5": float(np.nanpercentile(a, 2.5)), "p97_5": float(np.nanpercentile(a, 97.5))} if len(a) else None
    return {"CS": f(np.array(cs_att)), "SDID": f(np.array(sd_att))}


def placebo_temporal(Y, coh):
    """Adopción falsa en 2023T2 sobre el preperiodo limpio: CS (base 2023T1, post 2023T2-2023T4) y SDID (pesos en 2022T2-2023T1)."""
    q = {p: i for i, p in enumerate(QS)}
    tr = np.isin(coh, [D.G1, D.G4])
    ne = coh == "nunca"
    b = q["2023T1"]
    cs = []
    for p in ("2023T2", "2023T3", "2023T4"):
        a, _ = D._dif(Y, b, q[p], tr)
        c, _ = D._dif(Y, b, q[p], ne)
        cs.append(a - c)
    ok = np.isfinite(Y[:, :7]).all(axis=1)
    pre = [q[p] for p in QS[:4]]
    post = [q[p] for p in ("2023T2", "2023T3", "2023T4")]
    sd = D.sdid(Y[tr & ok][:, :7], Y[ne & ok][:, :7], pre, post)
    return {"CS": float(np.mean(cs)), "SDID": float(sd["att"])}


def exclusiones(Y, N, coh, xyz, codigos, estim_fun):
    """(v) sin Barcelona ni municipios con renta previa en el 10 % superior; (vi) provincia 08 sin la capital."""
    pre_r = np.nanmean(D_R[:, :7], axis=1)
    p90 = np.nanpercentile(pre_r, 90)
    m_v = (codigos != "08019") & ~(pre_r >= p90)
    m_vi = np.array([c.startswith("08") and c != "08019" for c in codigos])
    return {"sin_Barcelona_ni_decil_superior": estim_fun(m_v), "provincia_08_sin_capital": estim_fun(m_vi)}


def moran_residuos(Rv, coh, xyz, radio=25.0):
    """I de Moran (solo el estadístico, sin p) de los residuos de regresar el cambio de renta previo-posterior sobre el indicador de tratamiento."""
    from scipy.spatial import cKDTree
    q = {p: i for i, p in enumerate(QS)}
    post = [q[p] for p in QS if p >= "2024T2"]
    delta = np.nanmean(Rv[:, post], axis=1) - np.nanmean(Rv[:, :7], axis=1)
    ok = np.isfinite(delta)
    x = np.isin(coh, [D.G1, D.G4]).astype(float)[ok]
    y = delta[ok]
    X = np.column_stack([np.ones(len(x)), x])
    e = y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
    P = xyz[ok]
    tree = cKDTree(P)
    Wd = tree.sparse_distance_matrix(tree, radio, output_type="coo_matrix")
    m = Wd.row != Wd.col
    w = 1.0 / np.maximum(Wd.data[m], 1.0)
    import scipy.sparse as sp
    W = sp.csr_matrix((w, (Wd.row[m], Wd.col[m])), shape=(len(e), len(e)))
    rs = np.asarray(W.sum(axis=1)).ravel()
    rs[rs == 0] = 1
    W = sp.diags(1 / rs) @ W
    z = e - e.mean()
    I = float(len(z) / W.sum() * (z @ (W @ z)) / (z @ z))
    return {"I_moran": I, "n": int(len(z)), "W": f"distancia inversa, corte {radio:.0f} km, filas normalizadas"}


def ruptura_largo(codigos, coh):
    """Prueba de ruptura en 2022T2 sobre el preperiodo largo 2019T1-2023T4 (descriptiva; adenda 1, punto 1).

    Serie = renta media (log) de los tratados menos la de los donantes, unidades con renta en los 20 trimestres.
    Se informa el salto de nivel en 2022T2 y la fecha de ruptura única que minimiza la SCR (Bai-Perron con una ruptura, recorte del 15 %).
    """
    d = pd.read_parquet(D.PROC / "p6_zonas_tensionadas.parquet")
    t = d[(d.frecuencia == "T") & d.variable.isin(["incasol_contratos", "incasol_renta_media"]) & d.territorio_codigo.isin(codigos)]
    w = t.pivot_table(index=["territorio_codigo", "periodo", "desagregacion"], columns="variable", values="valor", aggfunc="first").reset_index()
    w = w[(w.periodo >= "2019T1") & (w.periodo <= "2023T4")]
    w["imp"] = w.incasol_contratos * w.incasol_renta_media
    w["cr"] = np.where(w.incasol_renta_media.notna(), w.incasol_contratos, 0.0)
    g = w.groupby(["territorio_codigo", "periodo"]).agg(imp=("imp", "sum"), cr=("cr", "sum")).reset_index()
    g["lr"] = np.log(g.imp / g.cr.where(g.cr > 0))
    W = g.pivot(index="territorio_codigo", columns="periodo", values="lr")
    W = W.dropna()
    cs = pd.Series(coh, index=codigos).reindex(W.index)
    tr = cs.isin([D.G1, D.G4])
    gap = (W[tr].mean() - W[~tr].mean()).values
    per = list(W.columns)
    i0 = per.index("2022T2")
    salto = float(gap[i0:].mean() - gap[:i0].mean())
    n = len(gap)
    lo, hi = int(np.ceil(0.15 * n)), int(np.floor(0.85 * n))
    best = None
    for k in range(lo, hi + 1):
        ssr = ((gap[:k] - gap[:k].mean()) ** 2).sum() + ((gap[k:] - gap[k:].mean()) ** 2).sum()
        if best is None or ssr < best[1]:
            best = (k, ssr)
    return {"n_unidades": int(len(W)), "n_tratados": int(tr.sum()), "n_donantes": int((~tr).sum()), "salto_nivel_2022T2": salto, "ruptura_unica_estimada": per[best[0]],
            "brecha_media_2019T1_2022T1": float(gap[:i0].mean()), "brecha_media_2022T2_2023T4": float(gap[i0:].mean())}


def main(R_perm: int = 1000, R_sdid: int = 200):
    t0 = time.time()
    SALIDA.mkdir(parents=True, exist_ok=True)
    reg = Registry(SALIDA / "registro.csv")
    N, R, coh, xyz = preparar()
    codigos = np.array(N.index)
    global D_R
    D_R = R.values
    Nv = N.values
    Rv = R.values
    Cv = np.log1p(Nv)
    res = {"N_muestra": int(len(coh)), "tratados": int(np.isin(coh, [D.G1, D.G4]).sum()), "cohorte_2024T1": int((coh == D.G1).sum()),
           "cohorte_2024T4": int((coh == D.G4).sum()), "nunca_tratados": int((coh == "nunca").sum())}
    rent_16 = np.isfinite(Rv).all(axis=1)
    res["N_renta_equilibrado_16q"] = int(rent_16.sum())
    res["N_tratados_renta_16q"] = int((rent_16 & np.isin(coh, [D.G1, D.G4])).sum())
    res["N_donantes_renta_16q"] = int((rent_16 & (coh == "nunca")).sum())
    res["balance"] = balance(Rv, Nv, coh, xyz)

    # ---------------- H1: multiverso de 36 ----------------
    multi = {"H1": [], "H2": []}
    for outc, Y in (("H1", Rv), ("H2", Cv)):
        for est in ("CS", "SDID"):
            for umbral in (5, 10, 30):
                for radio in (0, 10, 25):
                    for fin in ("2026T1", "2025T4"):
                        s = especificacion(Y, Nv, coh, xyz, est, umbral, radio, fin)
                        s["resultado"] = outc
                        multi[outc].append(s)
                        registrar(reg, "V15-A", f"{outc}-{est}-u{umbral}-r{radio}-{fin}", f"{est} {'log renta' if outc == 'H1' else 'log(1+contratos)'} umbral={umbral} radio={radio}km hasta {fin}",
                                  "2022T2", fin, s.get("n_tr") if isinstance(s.get("n_tr"), int) else sum((s.get("n_tr") or {}).values()), coef=s["att"],
                                  notas=f"puntual; donantes={s['n_donantes']}; {'degenerada' if s.get('degenerada') else ''}")
    res["multiverso"] = multi

    # ---------------- principales ----------------
    pr = {}
    for outc, Y in (("H1", Rv), ("H2", Cv)):
        cel = D.cs_celdas(Y, coh, QS, "2026T1", "todos")
        cel_a1 = D.cs_celdas(Y, coh, QS, "2026T1", "solo_g4")
        sd = D.sdid_cohortes(Y, coh, QS, "2026T1")
        pt = pretendencias(Y, coh)
        pr[outc] = {"CS_att": D.cs_agregar(cel), "CS_att_por_cohorte": {g: float(np.average(c.att.dropna(), weights=c.loc[c.att.notna(), "n_tr"])) for g, c in cel.groupby("g")},
                    "CS_a1_cohorte4_control_solo": D.cs_agregar(cel_a1), "SDID_att": sd["att"], "SDID_por_cohorte": sd["por_cohorte"],
                    "SDID_n_donantes": sd["n_donantes"], "SDID_contraste_2023T3_T4": sd["contraste"], "SDID_rmse_pre": sd.get("rmse_pre"),
                    "SDID_donantes_peso_positivo": sd.get("donantes_pesos_pos"),
                    "pretendencias": {k: v for k, v in pt.items() if k != "eventos"}, "eventos_cs": pt["eventos"].round(5).to_dict(orient="records"),
                    "placebo_temporal_2023T2": placebo_temporal(Y, coh)}
        # SDID evento por trimestre (cohorte 2024T1) para informe
        pr[outc]["celdas_cs"] = cel.round(5).to_dict(orient="records")
    res["principal"] = pr

    # ---------------- PPML (H2 principal) ----------------
    pp = {}
    for fin in ("2026T1", "2025T4"):
        pp[fin] = D.ppml(Nv, coh, QS, fin)
        registrar(reg, "V15-A", f"H2-PPML-{fin}", "PPML contratos ~ cohorte x post + FE municipio + FE trimestre", "2022T2", fin, pp[fin]["n_obs"], coef=pp[fin]["att_pct"] / 100, notas="puntual (sin error típico válido)")
    res["ppml"] = pp
    # PPML placebo temporal: cohortes falsas no se estiman (sin inferencia); ver DV15-A

    # ---------------- exclusiones ----------------
    def ex_fun_factory(Y, outcome):
        def f(mask):
            cel = D.cs_celdas(Y[mask], coh[mask], QS, "2026T1")
            sd = D.sdid_cohortes(Y[mask], coh[mask], QS, "2026T1")
            return {"CS": D.cs_agregar(cel), "SDID": sd["att"], "n": int(mask.sum()), "n_donantes": int(((coh[mask]) == "nunca").sum())}
        return f
    ex = {}
    for outc, Y in (("H1", Rv), ("H2", Cv)):
        ex[outc] = exclusiones(Y, Nv, coh, xyz, codigos, ex_fun_factory(Y, outc))
    ex["H2"]["PPML_sin_Barcelona_ni_decil"] = None
    m_v = (codigos != "08019") & ~(np.nanmean(Rv[:, :7], axis=1) >= np.nanpercentile(np.nanmean(Rv[:, :7], axis=1), 90))
    ex["H2"]["PPML_sin_Barcelona_ni_decil"] = D.ppml(Nv[m_v], coh[m_v], QS, "2026T1")["att_pct"]
    res["exclusiones"] = ex

    # ---------------- control sintético (10 mayores tratados), puntual ----------------
    tr_idx = np.where(np.isin(coh, [D.G1, D.G4]) & rent_16)[0]
    top = tr_idx[np.argsort(-Nv[tr_idx, :7].mean(axis=1))[:10]]
    don = np.where((coh == "nunca") & rent_16)[0]
    q = {p: i for i, p in enumerate(QS)}
    sc = []
    for u in top:
        ini = "2024T2" if coh[u] == D.G1 else D.G4
        post = [q[p] for p in QS if p >= ini]
        e = D.sintetico_unidad(Rv[u], Rv[don], list(range(7)), post)
        sc.append({"municipio": codigos[u], "cohorte": coh[u], "efecto_pct": float(100 * (np.exp(e) - 1))})
    res["control_sintetico_10_mayores"] = {"unidades": sc, "mediana_pct": float(np.median([s["efecto_pct"] for s in sc])), "media_pct": float(np.mean([s["efecto_pct"] for s in sc]))}

    # ---------------- Lee ----------------
    post_idx = [q[p] for p in QS if p >= "2024T2"]
    S = np.isfinite(Rv[:, post_idx]).all(axis=1) & np.isfinite(Rv[:, :7]).all(axis=1)
    delta = np.nanmean(Rv[:, post_idx], axis=1) - np.nanmean(Rv[:, :7], axis=1)
    trm = np.isin(coh, [D.G1, D.G4])
    nm = coh == "nunca"
    res["lee_H1"] = D.lee_cotas(delta[trm], S[trm].astype(int), delta[nm], S[nm].astype(int))

    # ---------------- permutaciones (placebo espacial) ----------------
    res["placebo_espacial"] = {"H1": permutaciones(Rv, coh, R_perm, 1, R_sdid), "H2": permutaciones(Cv, coh, R_perm, 2, R_sdid)}
    res["moran_residuos_H1"] = moran_residuos(Rv, coh, xyz)
    res["ruptura_preperiodo_largo"] = ruptura_largo(codigos, coh)
    res["tiempo_s"] = round(time.time() - t0, 1)
    volcar(SALIDA / "estimacion_bruta.json", res)
    reg.flush()
    return res


if __name__ == "__main__":
    main()
