"""V17 · fase 2 · grupo v15_v16_micro: inferencia convencional A POSTERIORI de H1-H4 (V15) y Q1-Q4, Q6-Q8 (V16).

Análisis a posteriori (V17). Misma muestra, misma especificación y mismo estimador puntual que lo publicado: solo cambia la inferencia.
Encargo: docs/v17/brief_f2_inferencia.md. SEED = 20261010, sin red. No lee data/sealed ni muestras selladas (las funciones de preparación
de V15/V16 ya filtran con src/holdout.py); no ejecuta evaluate_*; no modifica scripts ni salidas de versiones anteriores (solo importa
funciones y copia la preparación de datos).

Regla de publicación (B2): tamaño real > 15 % -> «no fiable» y la fila solo lleva la estimación puntual; entre 5 % y 15 % (y por debajo,
contraste conservador) se publica con la frase «p = x; el contraste rechaza un y % de las veces bajo la nula»; sin Monte Carlo -> «sin medir».
B3: Holm y BH dentro de cada pregunta (nunca entre preguntas), como sensibilidad junto al ajuste original del proyecto.

Uso: python3 src/v17/f2_inferencia_v15_v16_micro.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ALCANCE_TERRITORIAL = "reproduce publicado"   # guarda de fuga v6 (check_v17): lee solo a través de los cargadores de V15 y V16 que reproduce (guarda «lecturas v6» de check_v15)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v15"))
sys.path.insert(0, str(ROOT / "src" / "v16"))

SEED = 20261010
B_WEBB = 9999
UMBRAL = 0.15
SALIDA = ROOT / "output" / "v17" / "lectura_bde" / "v15_v16_micro"
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])

COLS = ["version", "id_resultado", "pregunta", "estimacion_publicada", "estimacion_reproducida", "unidad", "capa_proyecto", "inferencia_original",
        "metodo_convencional", "n_clusters", "se_conv", "p_conv", "ic95_lo", "ic95_hi", "herramienta_mc", "tamano_real", "fuente_mc", "publicable",
        "p_holm_pregunta", "p_bh_pregunta", "frase", "nota"]

# ------------------------------------------------------------------ distorsión medida (tamaño real al 5 % nominal)
MC15 = "docs/v15/validacion_montecarlo/{}.md; output/v15/montecarlo/{}"
MC16 = "docs/v16/validacion_montecarlo.md; output/v16/montecarlo/{}"
MC = {
    "H1_CS": (0.2165, "wild_webb_v15 W1_H1H2_198municipios, CR1 por municipio", MC15.format("wild_webb_v15", "wild_webb_v15")),
    "H2_CS": (0.2165, "wild_webb_v15 W1_H1H2_198municipios, CR1 por municipio", MC15.format("wild_webb_v15", "wild_webb_v15")),
    "H2_PPML": (0.2165, "wild_webb_v15 W1 (CR1 por municipio; TWFE lineal, análogo del PPML: PPML sin medir)", MC15.format("wild_webb_v15", "wild_webb_v15")),
    "H1_SDID": (0.2080, "sdid_placebo_h1h2 S1_H1_74donantes, webb_cluster", MC15.format("sdid_placebo_h1h2", "sdid_placebo_h1h2")),
    "H2_SDID": (0.0930, "sdid_placebo_h1h2 S3_H2_74donantes, webb_cluster", MC15.format("sdid_placebo_h1h2", "sdid_placebo_h1h2")),
    "CONLEY": (0.0963, "conley_seccion, escenario principal (radio 1,0 km), Conley 2 km", MC16.format("conley_seccion")),
    "H4_AKM0": (0.0047, "akm_municipal M3_instr_sin_residenciales_F_alta, AKM0 (AR)", MC15.format("akm_municipal", "akm_municipal")),
    "H4_AKM": (0.3283, "akm_municipal M3_instr_sin_residenciales_F_alta, AKM", MC15.format("akm_municipal", "akm_municipal")),
    "H4_PROV": (0.7050, "akm_municipal M3_instr_sin_residenciales_F_alta, agrupado provincia t(40)", MC15.format("akm_municipal", "akm_municipal")),
    "Q1C": (0.0655, "cs_webb variante b (WCR, nulo impuesto, Webb por provincia)", MC16.format("cs_webb")),
    "Q2A": (0.1420, "did_intensidad_webb Q2a provincial, Webb (principal)", MC16.format("did_intensidad_webb")),
    "Q2C_WEBB": (0.0605, "did_intensidad_webb Q2c municipal, Webb por provincia (referencia extra)", MC16.format("did_intensidad_webb")),
    "Q3C_AKM0": (0.0108, "shiftshare_akm principal wA=0,5, AKM0", MC16.format("shiftshare_akm")),
    "Q3C_AKM": (0.3762, "shiftshare_akm principal wA=0,5, AKM", MC16.format("shiftshare_akm")),
    "Q4": (0.2030, "rejilla_twfe escala municipio (CR1 por provincia, 41 clusters), TWFE de exposición continua; análogo, no el diseño exacto", MC16.format("rejilla_twfe")),
    "Q6_RAND": (0.0775, "dcdh_aleatorizacion nulo (aleatorización del calendario entre CCAA)", MC16.format("dcdh_aleatorizacion")),
    "SIN_MEDIR": (np.nan, "sin medir (no hay Monte Carlo de esta herramienta en el repositorio)", "sin medir"),
}


# ------------------------------------------------------------------ utilidades
def pct(b):
    return 100.0 * (np.exp(b) - 1.0)


def holm(p):
    p = np.asarray(p, float)
    out = np.full(len(p), np.nan)
    ok = np.isfinite(p)
    m = len(p)
    idx = np.argsort(p[ok])
    ps = p[ok][idx]
    adj = np.maximum.accumulate((m - np.arange(len(ps))) * ps)
    r = np.empty(len(ps))
    r[idx] = np.minimum(adj, 1.0)
    out[ok] = r
    return out


def bh(p):
    p = np.asarray(p, float)
    out = np.full(len(p), np.nan)
    ok = np.isfinite(p)
    m = len(p)
    idx = np.argsort(p[ok])
    ps = p[ok][idx]
    adj = np.minimum.accumulate((m / (np.arange(len(ps)) + 1.0) * ps)[::-1])[::-1]
    r = np.empty(len(ps))
    r[idx] = np.minimum(adj, 1.0)
    out[ok] = r
    return out


def clasifica(tam: float) -> str:
    """Regla del 15 %: 'no_fiable' si el tamaño real supera 0,15; 'sin_medir' si no hay Monte Carlo; 'si' en otro caso."""
    if not np.isfinite(tam):
        return "sin_medir"
    return "no_fiable" if tam > UMBRAL else "si"


def coma(x, d=3):
    return f"{x:.{d}f}".replace(".", ",")


def frase(estado: str, p: float, tam: float, metodo: str) -> str:
    if estado == "no_fiable":
        return f"Inferencia convencional NO publicada: el contraste ({metodo}) rechaza un {coma(100 * tam, 1)} % de las veces bajo la nula (> 15 %); solo estimación puntual. A posteriori."
    if estado == "sin_medir":
        return f"p = {coma(p)}; distorsión del contraste sin medir (no hay Monte Carlo de esta herramienta). A posteriori."
    extra = " (contraste conservador: por debajo del 5 % nominal)" if tam < 0.05 else ""
    return f"p = {coma(p)}; el contraste rechaza un {coma(100 * tam, 1)} % de las veces bajo la nula{extra}. A posteriori."


def webb_if(att, psi, psi0, cl, ncl, k, B=B_WEBB):
    """Wild cluster bootstrap-t de Webb sobre la función de influencia (nulo impuesto), como la variante b de cs_webb. cl: índice de cluster por unidad."""
    s = np.bincount(cl, weights=psi, minlength=ncl)
    s0 = np.bincount(cl, weights=psi0, minlength=ncl)
    v = WEBB[np.random.default_rng([SEED, k]).integers(0, 6, size=(ncl, B))]
    se = float(np.sqrt((s ** 2).sum()))
    tobs = att / max(se, 1e-15)
    sv = v * s0[:, None]
    tstar = sv.sum(0) / np.maximum(np.sqrt((sv ** 2).sum(0)), 1e-15)
    c = float(np.quantile(np.abs(tstar), 0.95))
    return {"se": se, "p": float((1 + np.sum(np.abs(tstar) >= abs(tobs))) / (B + 1)), "lo": att - c * se, "hi": att + c * se, "ncl": ncl}


def cr1_normal(att, psi, cl, ncl):
    s = np.bincount(cl, weights=psi, minlength=ncl)
    se = float(np.sqrt((s ** 2).sum() * ncl / (ncl - 1)))
    t = stats.t.ppf(0.975, ncl - 1)
    return {"se": se, "p": float(2 * stats.t.sf(abs(att / se), ncl - 1)), "lo": att - t * se, "hi": att + t * se, "ncl": ncl}


def twfe_webb(y, x, unit, time_, cl, k, B=B_WEBB):
    """MCO con efectos fijos de unidad y tiempo (FWL con la proyección Q), CR1 por cluster y wild cluster bootstrap-t de Webb (residuos restringidos)."""
    n = len(y)
    ui, ti, ci = pd.factorize(pd.Series(unit))[0], pd.factorize(pd.Series(time_))[0], pd.factorize(pd.Series(cl))[0]
    nu, nt, G = ui.max() + 1, ti.max() + 1, ci.max() + 1
    Dm = np.zeros((n, nu + nt - 1))
    Dm[np.arange(n), ui] = 1.0
    m = ti > 0
    Dm[np.where(m)[0], nu + ti[m] - 1] = 1.0
    Qm = np.eye(n) - Dm @ np.linalg.pinv(Dm)
    z, xt = Qm @ y, Qm @ x
    sxx = float(xt @ xt)
    b = float(xt @ z / sxx)
    e = z - b * xt
    sc = np.bincount(ci, weights=xt * e, minlength=G)
    se = float(np.sqrt((sc ** 2).sum() * G / (G - 1)) / sxx)
    out = {"b": b, "se": se, "G": G, "p_cr1": float(2 * stats.t.sf(abs(b / se), G - 1))}
    rng = np.random.default_rng([SEED, k])
    v = WEBB[rng.integers(0, 6, size=(G, B))]
    Cm = np.zeros((n, G))
    Cm[np.arange(n), ci] = 1.0
    ts = []
    for a in range(0, B, 1000):
        vb = v[:, a:a + 1000][ci]
        Zs = Qm @ (vb * z[:, None])
        bs = (xt @ Zs) / sxx
        Es = Zs - xt[:, None] * bs[None, :]
        scs = Cm.T @ (xt[:, None] * Es)
        ses = np.sqrt((scs ** 2).sum(0) * G / (G - 1)) / sxx
        ts.append(bs / ses)
    ts = np.concatenate(ts)
    out["p_webb"] = float((1 + np.sum(np.abs(ts) >= abs(b / se))) / (B + 1))
    c = float(np.quantile(np.abs(ts), 0.95))
    out["lo"], out["hi"] = b - c * se, b + c * se
    return out


# ------------------------------------------------------------------ registro de filas
FILAS: list[dict] = []
INTERNO: dict = {}  # (id) -> p calculado (también de las no fiables, solo para fijar m en Holm/BH)


def pub(rutas: str, *clave):
    d = json.loads((ROOT / rutas).read_text(encoding="utf-8"))
    for c in clave:
        d = d[c]
    return float(d)


def fila(version, rid, pregunta, publicada, reproducida, unidad, orig, metodo, ncl, se, p, lo, hi, mc_clave, nota, alt=False, capa="C4"):
    tam, herr, fuente = MC[mc_clave]
    estado = clasifica(tam)
    if estado == "si" and not (0.04 <= tam <= 0.06):
        nota = (nota + " " if nota else "") + "La herramienta figura NO APTA en su Monte Carlo (tamaño fuera de [0,04; 0,06]); la regla B2 solo excluye por encima del 15 %."
    rel = abs(reproducida - publicada) / max(abs(publicada), 1e-300)
    nota = (nota + " " if nota else "") + ("Punto reproducido (rel. %.1e)." % rel if rel <= 1e-6 else "ATENCIÓN: el punto NO reproduce el publicado (rel. %.2e)." % rel)
    r = {"version": version, "id_resultado": rid, "pregunta": pregunta, "estimacion_publicada": publicada, "estimacion_reproducida": reproducida, "unidad": unidad,
         "capa_proyecto": capa, "inferencia_original": orig, "metodo_convencional": metodo, "n_clusters": ncl, "se_conv": se, "p_conv": p, "ic95_lo": lo, "ic95_hi": hi,
         "herramienta_mc": herr, "tamano_real": tam, "fuente_mc": fuente, "publicable": estado, "p_holm_pregunta": np.nan, "p_bh_pregunta": np.nan,
         "frase": "", "nota": nota, "_alt": alt, "_p": p, "_metodo": metodo}
    FILAS.append(r)
    return r


def cierre() -> pd.DataFrame:
    df = pd.DataFrame(FILAS)
    for preg, g in df[~df._alt].groupby("pregunta"):
        hp, bp = holm(g._p.values), bh(g._p.values)
        df.loc[g.index, "p_holm_pregunta"] = hp
        df.loc[g.index, "p_bh_pregunta"] = bp
    for i, r in df.iterrows():
        df.at[i, "frase"] = frase(r.publicable, r._p, r.tamano_real, r._metodo)
        if r.publicable == "no_fiable":
            for c in ("se_conv", "p_conv", "ic95_lo", "ic95_hi", "p_holm_pregunta", "p_bh_pregunta"):
                df.at[i, c] = np.nan
    df["p_holm_pregunta"] = df.p_holm_pregunta.where(~df._alt)
    df["p_bh_pregunta"] = df.p_bh_pregunta.where(~df._alt)
    return df[COLS]


# ------------------------------------------------------------------ V15 · H1 y H2 (zonas tensionadas, Cataluña)
def cs_if(Y, coh, D, fin="2026T1", donantes=None):
    qs = D.QUARTERS
    q = {p: i for i, p in enumerate(qs)}
    nunca = (coh == "nunca") if donantes is None else ((coh == "nunca") & donantes)
    cel = []
    for g, ini in ((D.G1, "2024T2"), (D.G4, D.G4)):
        mg = coh == g
        b = q[D.idx_periodo(D.periodo_idx(g) - 1)]
        for p in qs:
            if p < ini or p > fin:
                continue
            t = q[p]
            mc = nunca | ((coh == D.G4) & (g == D.G1) & (D.periodo_idx(p) < D.periodo_idx(D.G4)))
            d = Y[:, t] - Y[:, b]
            fi = np.isfinite(d)
            A, C = mg & fi, mc & fi
            if A.sum() == 0 or C.sum() == 0:
                continue
            cel.append((A, C, d))
    tot = sum(c[0].sum() for c in cel)
    n = len(coh)
    att, psi, psi0 = 0.0, np.zeros(n), np.zeros(n)
    for A, C, d in cel:
        w = A.sum() / tot
        mG, mC = d[A].mean(), d[C].mean()
        att += w * (mG - mC)
        psi[A] += w * (d[A] - mG) / A.sum()
        psi[C] -= w * (d[C] - mC) / C.sum()
        psi0[A] += w * (d[A] - mC) / A.sum()
        psi0[C] -= w * (d[C] - mC) / C.sum()
    return float(att), psi, psi0


def sdid_if(Y, coh, D, fin="2026T1", donantes=None):
    qs = D.QUARTERS
    r = D.sdid_cohortes(Y, coh, qs, fin, donantes)
    q = {p: i for i, p in enumerate(qs)}
    cols_ok = [q[p] for p in qs if p <= fin]
    fin_ok = np.isfinite(Y[:, cols_ok]).all(axis=1)
    don = (coh == "nunca") & fin_ok
    if donantes is not None:
        don &= donantes
    pre = [q[p] for p in qs[:5]]
    n = len(coh)
    pesos = {g: ((coh == g) & fin_ok).sum() * len([p for p in qs if ini <= p <= fin]) for g, ini in ((D.G1, "2024T2"), (D.G4, D.G4)) if g in r["_res"]}
    tot = sum(pesos.values())
    att, psi, psi0 = 0.0, np.zeros(n), np.zeros(n)
    for g, ini in ((D.G1, "2024T2"), (D.G4, D.G4)):
        if g not in r["_res"]:
            continue
        mg = (coh == g) & fin_ok
        post = [q[p] for p in qs if ini <= p <= fin]
        lam, om = r["_res"][g]["lambda"], r["_res"][g]["omega"]
        Yc = Y[:, cols_ok]
        delta = Yc[:, post].mean(axis=1) - Yc[:, pre] @ lam
        itr, ido = np.where(mg)[0], np.where(don)[0]
        mu = float(om @ delta[ido])
        w = pesos[g] / tot
        ntr = len(itr)
        att += w * (delta[itr].mean() - mu)
        psi[itr] += w * (delta[itr] - delta[itr].mean()) / ntr
        psi[ido] -= w * om * (delta[ido] - mu)
        psi0[itr] += w * (delta[itr] - mu) / ntr
        psi0[ido] -= w * om * (delta[ido] - mu)
    assert abs(att - r["att"]) < 1e-9, (att, r["att"])
    return float(att), psi, psi0


def ppml_cluster(N, coh, D, fin="2026T1"):
    import statsmodels.api as sm
    qs = D.QUARTERS
    idx = np.arange(len(coh))
    cols = [i for i, p in enumerate(qs) if p <= fin]
    filas = []
    for u in idx:
        for c in cols:
            p = qs[c]
            if coh[u] == D.G1 and p == D.G1:
                continue
            filas.append((u, c, N[u, c], float(coh[u] == D.G1 and p >= "2024T2"), float(coh[u] == D.G4 and p >= D.G4)))
    df = pd.DataFrame(filas, columns=["u", "t", "y", "d1", "d4"])
    X = pd.concat([df[["d1", "d4"]], pd.get_dummies(df.u, prefix="u", drop_first=True, dtype=float), pd.get_dummies(df.t, prefix="t", drop_first=True, dtype=float)], axis=1)
    m = sm.GLM(df.y.values, X.values, family=sm.families.Poisson()).fit(maxiter=100, cov_type="cluster", cov_kwds={"groups": df.u.values})
    t1, t4 = float(m.params[0]), float(m.params[1])
    n1, n4 = int(df.d1.sum()), int(df.d4.sum())
    agg = (n1 * (np.exp(t1) - 1) + n4 * (np.exp(t4) - 1)) / (n1 + n4) * 100
    grad = np.array([n1 * np.exp(t1), n4 * np.exp(t4)]) / (n1 + n4) * 100
    se = float(np.sqrt(grad @ np.asarray(m.cov_params())[:2, :2] @ grad))
    G = len(coh)
    return agg, se, G


def bloque_v15_zonas():
    import pa_did as D
    P = D.construir_panel()
    N, R, coh = P["N"], P["R"], P["coh"].values
    Rv, Nv, Cv = R.values, N.values, np.log1p(N.values)
    G = len(coh)
    cl = np.arange(G)
    fam = "V15 zonas tensionadas (H1, H2)"
    orig = "ninguna (herramientas NO APTAS: solo estimación puntual)"
    pj = {h: f"output/v15/p6/resultado_{h}.json" for h in ("H1", "H2")}
    for hid, Y, tag in (("H1", Rv, "H1"), ("H2", Cv, "H2")):
        # Callaway-Sant'Anna 2x2
        att, psi, psi0 = cs_if(Y, coh, D)
        r = cr1_normal(att, psi, cl, G)
        pb = pub(pj[hid], "estimacion", "CS_att_pct")
        e = pct(att)
        fila("V15", f"{hid}-CS", fam, pb, e, "% (100·(exp(ATT)-1))", orig, "errores robustos agrupados por municipio (función de influencia, t(G-1)); nivel del tratamiento = municipio (308 > 40 clusters: sin Webb)",
             G, 100 * np.exp(att) * r["se"], r["p"], pct(r["lo"]), pct(r["hi"]), f"{tag}_CS",
             "Resultado en log(renta) (H1) o log(1+contratos) (H2). La dependencia espacial entre municipios no está recogida por el agrupamiento.")
        # SDID
        att, psi, psi0 = sdid_if(Y, coh, D)
        w = webb_if(att, psi, psi0, cl, G, 10 if hid == "H1" else 11)
        pb = pub(pj[hid], "estimacion", "SDID_att_pct")
        fila("V15", f"{hid}-SDID", fam, pb, pct(att), "% (100·(exp(ATT)-1))", orig,
             "wild cluster bootstrap-t de Webb por municipio sobre la puntuación SDID (pesos fijos, nulo impuesto, B=9.999); IC percentil-t simétrico",
             G, 100 * np.exp(att) * w["se"], w["p"], pct(w["lo"]), pct(w["hi"]), f"{tag}_SDID", "Pesos SDID tratados como fijos (como en el Monte Carlo sdid_placebo_h1h2).")
    # PPML (H2 principal)
    agg, se, G2 = ppml_cluster(Nv, coh, D)
    pb = pub(pj["H2"], "estimacion", "PPML_principal_pct")
    tcrit = stats.t.ppf(0.975, G2 - 1)
    p = float(2 * stats.t.sf(abs(agg / se), G2 - 1))
    fila("V15", "H2-PPML", fam, pb, agg, "% (cambio porcentual)", orig, "PPML con efectos de municipio y trimestre; errores robustos agrupados por municipio (método delta para el agregado de las dos cohortes)",
         G2, se, p, agg - tcrit * se, agg + tcrit * se, "H2_PPML", "Principal de H2. Monte Carlo del PPML no existe: se toma el TWFE lineal de wild_webb_v15 W1 como análogo.")


# ------------------------------------------------------------------ V15 · H3 (turismo por sección, Conley)
def bloque_v15_h3():
    import p5_turismo as T5
    import pa_panel as PN
    from pa_comun import xyz_km
    P, IP, nok = T5.cargar()
    todas = pd.unique(P.sec)
    cs = T5.centroides_secciones(todas).drop_duplicates("sec").set_index("sec").reindex(todas)
    ok_geo = cs.lon.notna().values
    xyz = xyz_km(cs.lon.fillna(0).values, cs.lat.fillna(0).values)
    falt = np.where(~ok_geo)[0]
    xyz[falt] = np.column_stack([20000.0 + 50.0 * np.arange(len(falt)), np.zeros(len(falt)), np.zeros(len(falt))])
    K = PN.matriz_conley(xyz, 2.0)
    sec_index = pd.Series(np.arange(len(todas)), index=todas)
    df, sd = T5.preparar_muestra(P, "VC", "pct", sin_saltos=False)
    r = T5.estimar(df, "mun_anio", K, sec_index)
    b, sec_, sem = float(r["b"][0]), float(r["se_conley"][0]), float(r["se_mun"][0])
    pb = pub("output/v15/p5/resultado.json", "estimacion", "beta_pct_por_DT")
    z = stats.norm.ppf(0.975)
    pc = float(2 * stats.norm.sf(abs(b / sec_)))
    fila("V15", "H3", "V15 turismo por sección (H3)", pb, 100 * b, "% de alquiler por DT intra-sección del % de viviendas turísticas", "ninguna (Conley 2 km NO APTO tras K16)",
         "Conley 2 km (núcleo de Bartlett, normal), mismo radio que el diseño original; efectos fijos de sección y municipio×año",
         int(r["n_mun"]), 100 * sec_, pc, 100 * (b - z * sec_), 100 * (b + z * sec_), "CONLEY",
         f"Panel T=4 (el Monte Carlo es de corte transversal con efectos fijos de municipio: escenario más parecido). EE agrupado por municipio: {100 * sem:.4f} (p = {2 * stats.norm.sf(abs(b / sem)):.3f}); referencia, sin medir en panel.")


# ------------------------------------------------------------------ V15 · H4 y V16 · Q3-c (shift-share: AKM / AKM0)
def akm(zk, zt, xt, yt, cl=None):
    """AKM y AKM0 (idénticas fórmulas a src/v15/montecarlo/akm_municipal.py): zk (filas x K) componentes por origen del regresor/instrumento."""
    Z = 1.959964
    szx = float(zt @ xt)
    b = float((zt @ yt) / szx)
    Ak, Bk = zk.T @ yt, zk.T @ xt
    SA, SB = Ak.sum(), Bk.sum()
    se_akm = float(np.sqrt(((Ak - b * Bk) ** 2).sum()) / abs(szx))
    z0 = SA / np.sqrt((Ak ** 2).sum())
    a2 = SB ** 2 - Z ** 2 * (Bk ** 2).sum()
    a1 = -2 * SA * SB + 2 * Z ** 2 * (Ak * Bk).sum()
    a0 = SA ** 2 - Z ** 2 * (Ak ** 2).sum()
    disc = a1 ** 2 - 4 * a2 * a0
    acot = bool(a2 > 0 and disc >= 0)
    lo, hi = ((-a1 - np.sqrt(disc)) / (2 * a2), (-a1 + np.sqrt(disc)) / (2 * a2)) if acot else (np.nan, np.nan)
    pih = szx / float(zt @ zt)
    rx = xt - pih * zt
    Fk = zk.T @ rx
    feff = float((pih / (np.sqrt((Fk ** 2).sum()) / float(zt @ zt))) ** 2) if not np.allclose(zt, xt) else float("nan")
    out = {"b": b, "se_akm": se_akm, "p_akm": float(2 * stats.norm.sf(abs(b / se_akm))), "p_akm0": float(2 * stats.norm.sf(abs(z0))), "ic_akm0": (lo, hi), "acotado": acot,
           "F_efectivo_MOP": feff, "K": zk.shape[1], "n_efectivo": float(1 / np.sum((Ak / SA) ** 2)) if SA != 0 else np.nan}
    if cl is not None:
        res = yt - b * xt
        G = cl.max() + 1
        sc = np.bincount(cl, weights=zt * res, minlength=G)
        se = float(np.sqrt((sc ** 2).sum() * G / (G - 1)) / abs(szx))
        out.update({"se_cl": se, "p_cl": float(2 * stats.t.sf(abs(b / se), G - 1)), "G": int(G)})
    return out


def bloque_v15_h4():
    from src.v15 import p4_inmigracion as P4
    p, s = P4.cargar_datos()
    muni, nacs, ni, A, R = P4.matrices(p, s)
    principal = [o for o in P4.PAISES if o not in P4.RESIDENCIALES]
    L, zk = P4.panel(A, R, ni, muni, tip="VC", norm="prev", origenes=principal, base=2003, minpob=0)
    est = P4.dos_sls(L)
    ti = np.array([P4.ANIOS.index(a) for a in L.anio.values])
    zkL = zk[L.i.values, :, ti] * 100
    cl = pd.factorize(L.prov)[0]
    a = akm(zkL, est["_zt"], est["_xt"], est["_yt"], cl)
    pb = pub("output/v15/p4/resultado.json", "estimacion", "beta_pp_alquiler_por_pp_poblacion_extranjera")
    fam = "V15 inmigración shift-share (H4)"
    orig = "ninguna (AKM y AKM0 NO APTOS: solo estimación puntual)"
    u = "% de alquiler por punto porcentual de población extranjera"
    lo, hi = a["ic_akm0"]
    nota0 = (f"F efectivo de Montiel Olea-Pflueger (varianza AKM de la primera etapa) = {a['F_efectivo_MOP']:.1f} (referencia 23,1 para tau=10 %, un instrumento; el F robusto HC1 publicado es 70,2); "
             f"número efectivo de choques = {a['n_efectivo']:.1f}; IC AKM0 {'acotado' if a['acotado'] else 'NO acotado (el contraste no excluye ningún valor)'}.")
    fila("V15", "H4-AKM0", fam, pb, 100 * a["b"], u, orig, "Anderson-Rubin / AKM0 (inversión del contraste con residuos bajo la nula; varianza por origen)", a["K"], np.nan, a["p_akm0"],
         100 * lo, 100 * hi, "H4_AKM0", nota0 + " Primaria de H4 (única inferencia con tamaño ≤ 15 %; muy conservadora: potencia 0,008 frente a la referencia de Saiz).")
    fila("V15", "H4-AKM", fam, pb, 100 * a["b"], u, orig, "AKM (varianza por origen, normal)", a["K"], 100 * a["se_akm"], a["p_akm"], 100 * (a["b"] - 1.959964 * a["se_akm"]),
         100 * (a["b"] + 1.959964 * a["se_akm"]), "H4_AKM", "Alternativa de la misma estimación (excluida de Holm/BH).", alt=True)
    fila("V15", "H4-PROV", fam, pb, 100 * a["b"], u, orig, "error agrupado por provincia, t(G-1)", a["G"], 100 * a["se_cl"], a["p_cl"], np.nan, np.nan, "H4_PROV",
         "Alternativa (excluida de Holm/BH).", alt=True)


def bloque_v16_q3c():
    import q3_shiftshare as S3
    ys = S3.panel_resultados()
    x0, s0 = S3.exposicion(2003, None, "pts")
    ui = {u: i for i, u in enumerate(s0["unidades"])}
    ti_ = {t: i for i, t in enumerate(s0["años"])}
    fam = "V16 Q3 inmigración (Q3-b, Q3-c)"
    orig = "ninguna (AKM y AKM0 NO APTOS: solo estimación puntual)"
    claves = {"Q3-c1": ("beta_log_valor_tasado_por_punto_poblacion_extranjera_predicha", "log del valor tasado por punto de población extranjera predicha"),
              "Q3-c2": ("beta_log_compraventas_por_punto", "log de las compraventas por punto de población extranjera predicha")}
    for q, y in ys.items():
        r = S3.ajustar(y.rename("y"), x0, "año")
        d = r["d"]
        zk = s0["comp"][[ui[u] for u in d.u], [ti_[t] for t in d.t], :]
        xt, yt = r["Xt"][:, 0], r["yt"]
        a = akm(zk, xt, xt, yt)
        pb = pub("output/v16/q3/resultado.json", "estimacion", q, claves[q][0])
        lo, hi = a["ic_akm0"]
        fila("V16", f"{q}-AKM0", fam, pb, a["b"], claves[q][1], orig, "AKM0 (inversión del contraste con residuos bajo la nula; varianza por origen), forma reducida",
             a["K"], np.nan, a["p_akm0"], lo, hi, "Q3C_AKM0",
             f"Forma reducida sin instrumento: Anderson-Rubin y F efectivo no aplican. Número efectivo de choques = {a['n_efectivo']:.1f}; IC AKM0 {'acotado' if a['acotado'] else 'no acotado'}.")
        fila("V16", f"{q}-AKM", fam, pb, a["b"], claves[q][1], orig, "AKM (varianza por origen, normal), forma reducida", a["K"], a["se_akm"], a["p_akm"],
             a["b"] - 1.959964 * a["se_akm"], a["b"] + 1.959964 * a["se_akm"], "Q3C_AKM", "Alternativa (excluida de Holm/BH).", alt=True)


# ------------------------------------------------------------------ V16 · Q3-b (Conley)
def bloque_v16_q3b():
    import q3_seccion as S
    geo = S.geometria()
    cu = S.cuotas()
    vc = S.serpavi("VC", [2018, 2021, 2022, 2024])
    D = geo.set_index("cod_seccion").join(cu, how="inner").join(vc.add_prefix("vc"), how="inner")
    D["dy"] = D["vc2024"] - D["vc2021"]
    D["x"] = D.cuota_ext
    D = D.reset_index()
    D = D.rename(columns={D.columns[0]: "cod_seccion"}) if "cod_seccion" not in D.columns else D
    P = S.ajustar(D, "dy", "x", True)
    pb = pub("output/v16/q3/resultado.json", "estimacion", "Q3-b", "beta_dlog_serpavi_por_DT_cuota_extranjeros")
    fila("V16", "Q3-b", "V16 Q3 inmigración (Q3-b, Q3-c)", pb, P["beta_por_DT"], "Δlog SERPAVI VC 2021-2024 por DT de la cuota de extranjeros", "ninguna (Conley 2 km NO APTO tras K16)",
         "Conley 2 km (núcleo de Bartlett, normal), mismo radio y núcleo corregido (K16); efectos fijos de municipio", P["n_mun"], P["se"], P["p"], P["ic95"][0], P["ic95"][1], "CONLEY",
         "Escenario exacto del Monte Carlo (corte transversal con efectos fijos de municipio). Pretendencia 2018-2021 no nula en la publicación (diagnóstico del original): la inferencia no corrige el sesgo de selección.")


# ------------------------------------------------------------------ V16 · Q1c (CS con Webb por provincia)
def bloque_v16_q1():
    from src.v16 import q1_zonas as Q1
    coh = Q1.cohortes()
    fam = "V16 Q1 zonas tensionadas (Q1c)"
    orig = "ninguna (CS-Webb NO APTO: solo estimación puntual)"
    pj = "output/v16/q1/resultado.json"
    for rid, excl, clave, k in (("Q1c-global", (), "Q1c_estimador_CS_global_dlog", 20), ("Q1c-sin-grandes", tuple(Q1.Q.GRANDES_PROV.keys()), "Q1c_sin_grandes_ciudades", 21)):
        w = Q1.panel_cv(prov_excluir=excl)
        co = {p: g for p, g in coh.items() if p in w.index}
        d, glob, ev, *_ = Q1.cs_att(w, co)
        nunca = np.array([p not in co for p in w.index])
        provs = list(w.index)
        n = len(provs)
        post = d[d.e >= 0]
        tot = post.N_g.sum()
        psi, psi0 = np.zeros(n), np.zeros(n)
        att = 0.0
        for _, rw in post.iterrows():
            g, t = pd.Period(rw.g, "Q"), pd.Period(rw.t, "Q")
            base = g - 1
            dv = (w[t] - w[base]).values
            A = np.array([(provs[i] in co) and co[provs[i]] == g for i in range(n)]) & np.isfinite(dv)
            C = nunca & np.isfinite(dv)
            wt = rw.N_g / tot
            mG, mC = dv[A].mean(), dv[C].mean()
            att += wt * (mG - mC)
            psi[A] += wt * (dv[A] - mG) / A.sum()
            psi[C] -= wt * (dv[C] - mC) / C.sum()
            psi0[A] += wt * (dv[A] - mC) / A.sum()
            psi0[C] -= wt * (dv[C] - mC) / C.sum()
        wb = webb_if(att, psi, psi0, np.arange(n), n, k)
        pb = pub(pj, "estimacion", clave)
        fila("V16", rid, fam, pb, att, "Δlog (ATT global)", orig,
             "wild cluster bootstrap-t de Webb por provincia (nulo impuesto, B=9.999) sobre la función de influencia del ATT de Callaway-Sant'Anna; solo 8 provincias tratadas en 5 cohortes",
             n, wb["se"], wb["p"], wb["lo"], wb["hi"], "Q1C", "Q1c incluye Cataluña (solapa con H1/H2). Q1a es un recuento y Q1b no es estimable en el entrenamiento: sin inferencia aplicable.")


# ------------------------------------------------------------------ V16 · Q2 (DiD de intensidad con Webb)
def bloque_v16_q2():
    from src.v16 import q2_turismo as Q2
    Q = Q2.Q
    pj = "output/v16/q2/resultado.json"
    fam = "V16 Q2 turismo (Q2a, Q2c)"
    orig = "ninguna (did_intensidad_webb NO APTO: solo estimación puntual)"
    # Q2a
    prov = sorted(Q.cargar("base_alquiler", "provincia", "ipc_alquiler_indice").territorio_codigo.unique())
    lv = np.log(Q.vut_provincia(prov))
    cv = Q.covariables_provincia(prov)
    d = pd.DataFrame({"z": Q2.zs(lv)})
    a = Q2.panel_ipc(prov)
    a = a[a.anio.isin(Q2.PRE + Q2.POST)].merge(d, left_on="territorio_codigo", right_index=True)
    a["post"] = a.anio.isin(Q2.POST).astype(float)
    a["zp"] = a.z * a.post
    a = a.dropna(subset=["y", "zp"]).reset_index(drop=True)
    r0 = Q.twfe(a, "y", "zp", "territorio_codigo", "anio")
    tw = twfe_webb(a.y.values, a.zp.values, a.territorio_codigo.values, a.anio.values, a.territorio_codigo.values, 30)
    pb = pub(pj, "estimacion", "Q2a_beta_por_DT_log_exposicion")
    fila("V16", "Q2a", fam, pb, tw["b"], "Δlog IPC alquiler por DT del log de la exposición", orig,
         "wild cluster bootstrap-t de Webb por provincia (residuos restringidos, B=9.999); EE CR1 por provincia", tw["G"], tw["se"], tw["p_webb"], tw["lo"], tw["hi"], "Q2A",
         f"EE CR1 por provincia, t(G-1): p = {tw['p_cr1']:.3f} (referencia). Punto reproducido también con Q.twfe ({r0['beta']:.6f}).")
    # Q2c
    ip = Q.cargar("base_alquiler", "municipio", "ipva_tam_indice")
    ip["anio"] = ip.periodo.astype(str).astype(int)
    ip = ip[ip.anio.between(2021, 2024)][["territorio_codigo", "anio", "valor"]].rename(columns={"valor": "idx"})
    ip["y"] = np.log(ip.idx)
    ip = ip.sort_values(["territorio_codigo", "anio"])
    ip["dy"] = ip.groupby("territorio_codigo").y.diff()
    v = Q2.vut_municipal()
    d2 = ip.merge(v, on=["territorio_codigo", "anio"], how="inner")
    d2["z"] = (d2.pct - d2.pct.mean()) / d2.pct.std(ddof=1)
    dd = d2.dropna(subset=["dy"]).reset_index(drop=True)
    r1 = Q.twfe(dd, "dy", "z", "territorio_codigo", "anio")
    prv = dd.territorio_codigo.str[:2].values
    tw = twfe_webb(dd.dy.values, dd.z.values, dd.territorio_codigo.values, dd.anio.values, prv, 31)
    pb = pub(pj, "estimacion", "Q2c_beta_por_DT")
    fila("V16", "Q2c", fam, pb, tw["b"], "Δlog IPVA-TAM por DT de la exposición (nivel)", orig,
         "wild cluster bootstrap-t de Webb por provincia (residuos restringidos, B=9.999); EE CR1 por provincia", tw["G"], tw["se"], tw["p_webb"], tw["lo"], tw["hi"], "Q2C_WEBB",
         f"El Monte Carlo del principal de Q2c (CR1 por provincia) da tamaño 0,0975; Webb por provincia (la herramienta usada aquí) 0,0605 (referencia extra del Monte Carlo). EE CR1: p = {tw['p_cr1']:.3f}. Punto con Q.twfe: {r1['beta']:.6f}.")


# ------------------------------------------------------------------ V16 · Q4 (oferta, TWFE con Red Natura)
def cr1_ols(Xt, e, cl, j):
    G = cl.max() + 1
    inv = np.linalg.inv(Xt.T @ Xt)
    sc = np.zeros((G, Xt.shape[1]))
    np.add.at(sc, cl, Xt * e[:, None])
    V = inv @ (sc.T @ sc) @ inv * G / (G - 1)
    return float(np.sqrt(V[j, j])), int(G)


def bloque_v16_q4():
    import q4_oferta as Q4
    C = Q4.C
    S = Q4.S
    fam = "V16 Q4 oferta (Q4a, Q4b)"
    orig = "ninguna (rejilla TWFE NO APTA: solo estimación puntual)"
    pj = "output/v16/q4/resultado.json"
    rn = Q4.red_natura()
    ob = C.anual(C.cargar("base_oferta", "obra_nueva_neta_catastro", "municipio"), "obra").reset_index()
    ur = C.anual(C.cargar("base_oferta", "catastro_unidades_urbanas_residenciales", "municipio"), "ur").reset_index()
    ur17 = ur[ur.t == 2017].set_index("u").ur.rename("ur17")
    base = ob.merge(rn, left_on="u", right_index=True).merge(ur17, left_on="u", right_index=True, how="left")
    base["prov"] = base.u.str[:2]
    d = base[(base.t >= 2018) & (base.t <= 2025)].copy()
    d = d[d.obra > 0]
    d["y"] = np.log(d.obra)
    d = d.dropna(subset=["y", "rn"])
    mu, sd = base.drop_duplicates("u").rn.mean(), base.drop_duplicates("u").rn.std()
    d["x"] = (d.rn - mu) / sd
    r = C.mco_fe(d.y.values, d[["x"]].values, [C.codif(d.prov), C.codif(d.t)])
    cl = C.codif(d.prov)
    se, G = cr1_ols(r["Xt"], r["resid"], cl, 0)
    clm = C.codif(d.u)
    sem, Gm = cr1_ols(r["Xt"], r["resid"], clm, 0)
    b = float(r["beta"][0])
    p = float(2 * stats.t.sf(abs(b / se), G - 1))
    tc = stats.t.ppf(0.975, G - 1)
    pb = pub(pj, "estimacion", "Q4a", "beta_log_obra_neta_por_DT_red_natura")
    nota = (f"Agrupado por provincia (análogo al Monte Carlo) en lugar de por municipio (nivel del tratamiento: la correlación espacial de la Red Natura cruza municipios); "
            f"EE agrupado por municipio ({Gm} clusters) = {sem:.4f}.")
    fila("V16", "Q4a", fam, pb, b, "Δlog obra nueva neta por DT del % Red Natura", orig, "errores robustos agrupados por provincia, t(G-1); efectos fijos de provincia y año", G, se, p, b - tc * se, b + tc * se, "Q4", nota)
    # Q4b
    s = S.shiftshare("municipio", 2003)
    x = pd.DataFrame(s["x"], index=s["unidades"], columns=s["años"])
    x[s["pob"][:, s["ib"]] <= 0] = np.nan
    shock = x.diff(axis=1).stack().rename("shock")
    shock.index.names = ["u", "t"]
    a = C.cargar("base_alquiler", "serpavi_alquiler_m2_mediana", "municipio", "tipologia=VC")
    y = np.log(C.anual(a, "ly").where(lambda s_: s_ > 0))
    dy = y.groupby(level=0).diff().rename("dy")
    dq = pd.concat([dy, shock], axis=1, join="inner").dropna().reset_index()
    dq = dq.merge(rn, left_on="u", right_index=True)
    dq = dq[(dq.t >= 2018) & (dq.t <= 2022)]
    dq["prov"] = dq.u.str[:2]
    dq["rnz"] = (dq.rn - rn.mean()) / rn.std()
    dq["inter"] = dq.shock * dq.rnz
    r = C.mco_fe(dq.dy.values, dq[["inter", "shock"]].values, [C.codif(dq.t)])
    se, G = cr1_ols(r["Xt"], r["resid"], C.codif(dq.prov), 0)
    sem, Gm = cr1_ols(r["Xt"], r["resid"], C.codif(dq.u), 0)
    b = float(r["beta"][0])
    p = float(2 * stats.t.sf(abs(b / se), G - 1))
    tc = stats.t.ppf(0.975, G - 1)
    pb = pub(pj, "estimacion", "Q4b", "beta_interaccion_choque_x_RN")
    nota = f"Agrupado por provincia (análogo al Monte Carlo); EE agrupado por municipio ({Gm} clusters) = {sem:.5f}. El choque de demanda es el shift-share de Q3 (generado a partir de cuotas): ni AKM ni la corrección por regresor generado están aplicados."
    fila("V16", "Q4b", fam, pb, b, "Δlog SERPAVI por DT de Red Natura y punto de choque", orig, "errores robustos agrupados por provincia, t(G-1); efectos fijos de año", G, se, p, b - tc * se, b + tc * se, "Q4", nota)


# ------------------------------------------------------------------ V16 · Q6 (ITP, dCDH)
def bloque_v16_q6():
    import q6_itp as Q6
    fam = "V16 Q6 fiscalidad ITP (Q6-v, Q6-p)"
    orig = "ninguna (dCDH con aleatorización NO APTO: solo estimación puntual)"
    pj = "output/v16/q6/resultado.json"
    T = Q6.tipos(0)
    T["dd"] = T.groupby("c").d.diff()
    dd_c = {c: g.set_index("t").dd for c, g in T.groupby("c")}
    ccaa = list(Q6.CCAA_OK)
    for q, k in (("Q6-v", 40), ("Q6-p", 41)):
        d = Q6.panel(q, 0, (2011, 2024)).reset_index(drop=True)
        b0 = Q6.wald_did(d)["beta"]
        pb = pub(pj, "estimacion", q, "beta_por_punto_de_tipo")
        years = sorted(d.t.unique())
        idx = {t: np.where(d.t.values == t)[0] for t in years}
        dy, tt, cc = d.dy.values, d.t.values, d.c.values
        ddf0 = d.dd_f.values

        def calendario(mapa):
            dd = np.array([dd_c[mapa[c]].get(t, np.nan) for c, t in zip(cc, tt)])
            ddf = np.array([dd_c[mapa[c]].get(t + 1, np.nan) for c, t in zip(cc, tt)])
            ddf = np.where(np.isnan(ddf0), np.nan, ddf)
            return dd, ddf

        def wald(dd, ddf):
            num = den = 0.0
            for t in years:
                m = idx[t]
                di, f, y = dd[m], np.nan_to_num(ddf[m]), dy[m]
                sw, ct = (di != 0) & (f == 0), (di == 0) & (f == 0)
                if sw.sum() == 0 or ct.sum() == 0:
                    continue
                num += float((y[sw] - y[ct].mean()).sum())
                den += float(di[sw].sum())
            return num / den if den != 0 else np.nan

        ddo, ddfo = calendario({c: c for c in ccaa})
        bid = wald(ddo, ddfo)
        assert abs(bid - b0) < 1e-12, (bid, b0)
        rng = np.random.default_rng([SEED, k])
        perm = np.empty(B_WEBB)
        for i in range(B_WEBB):
            pr = rng.permutation(len(ccaa))
            perm[i] = wald(*calendario({c: ccaa[j] for c, j in zip(ccaa, pr)}))
        ok = np.isfinite(perm)
        p = float((1 + np.sum(np.abs(perm[ok]) >= abs(b0))) / (ok.sum() + 1))
        c95 = float(np.quantile(np.abs(perm[ok]), 0.95))
        tam = f"Los calendarios se reasignan entre las {len(ccaa)} CCAA del panel (el Monte Carlo usó 11, con Ceuta y Melilla)."
        fila("V16", q, fam, pb, b0, "Δlog por punto de tipo general del ITP", orig,
             "inferencia por aleatorización del calendario entre CCAA (B=9.999 permutaciones), IC = beta ± cuantil 95 % de |beta permutado| (la del Monte Carlo dcdh_aleatorizacion)",
             len(ccaa), c95 / 1.959964, p, b0 - c95, b0 + c95, "Q6_RAND", tam + " Con 8 CCAA y pocos cambios de tipo la prueba tiene resolución limitada.")
        # Webb por CCAA sobre el Wald-DID (convencional del encargo; sin medir)
        den_t, a_i = {}, np.zeros(len(d))
        used = np.zeros(len(d), bool)
        mu_t = np.zeros(len(d))
        for t in years:
            m = idx[t]
            di, f, y = ddo[m], np.nan_to_num(ddfo[m]), dy[m]
            sw, ct = (di != 0) & (f == 0), (di == 0) & (f == 0)
            if sw.sum() == 0 or ct.sum() == 0:
                continue
            ai = np.zeros(len(m))
            ai[sw], ai[ct] = 1.0, -sw.sum() / ct.sum()
            a_i[m], mu_t[m] = ai, y[ct].mean()
            used[m] = sw | ct
        den = float(np.where(used, ddo, 0.0)[a_i == 1].sum())
        cl = pd.factorize(cc)[0]
        G = cl.max() + 1
        ddu = np.where(used, np.nan_to_num(ddo), 0.0)
        res0 = np.where(used, dy - mu_t, 0.0)
        e = np.where(used, dy - mu_t - b0 * ddu, 0.0)
        sc = np.bincount(cl, weights=a_i * e, minlength=G)
        se = float(np.sqrt((sc ** 2).sum() * G / (G - 1)) / abs(den))
        v = WEBB[np.random.default_rng([SEED, k + 10]).integers(0, 6, size=(G, B_WEBB))][cl]
        ys = v * res0[:, None]
        bs = (a_i[:, None] * ys).sum(0) / den
        mus = np.zeros_like(ys)
        for t in years:
            m = idx[t]
            ctm = (np.nan_to_num(ddo[m]) == 0) & (np.nan_to_num(ddfo[m]) == 0) & used[m]
            if ctm.sum():
                mus[m] = ys[m][ctm].mean(0)
        es = np.where(used[:, None], ys - mus - bs[None, :] * ddu[:, None], 0.0)
        scs = np.zeros((G, B_WEBB))
        np.add.at(scs, cl, a_i[:, None] * es)
        ses = np.sqrt((scs ** 2).sum(0) * G / (G - 1)) / abs(den)
        ts = bs / ses
        pw = float((1 + np.sum(np.abs(ts) >= abs(b0 / se))) / (B_WEBB + 1))
        cw = float(np.quantile(np.abs(ts), 0.95))
        fila("V16", q + "-Webb", fam, pb, b0, "Δlog por punto de tipo general del ITP", orig,
             "wild cluster bootstrap-t de Webb por CCAA (B=9.999; nulo impuesto) sobre el Wald-DID de dCDH (linealización por clusters)", int(G), se, pw, b0 - cw * se, b0 + cw * se, "SIN_MEDIR",
             "Webb sobre dCDH no está en el Monte Carlo: sin medir. Alternativa de la misma estimación (excluida de Holm/BH). Con 8 clusters el bootstrap tiene pocas combinaciones distintas.", alt=True)


# ------------------------------------------------------------------ V16 · Q7 (diferencia en discontinuidades, ECV)
def bloque_v16_q7():
    from src.v16 import q7_bono as Q7
    x = Q7.datos()
    r, _ = Q7.preparar_resultados(x)
    corte, h = 35, 5
    s = r[r.edad_sust.between(corte - h, corte + h) & r.anio.isin(Q7.ANTES + Q7.DESPUES)].dropna(subset=["log_alquiler", "DB090"]).copy()
    s["T"] = (s.edad_sust <= corte).astype(float)
    s["e"] = s.edad_sust - (corte + 0.5)
    s["post"] = s.anio.isin(Q7.DESPUES).astype(float)
    X = np.column_stack([np.ones(len(s)), s["T"], s.e, s.e * s["T"], s.post, s.post * s["T"], s.post * s.e, s.post * s.e * s["T"]])
    y = s.log_alquiler.to_numpy(float)
    sw = np.sqrt(s.DB090.to_numpy(float))
    Xs, ys = X * sw[:, None], y * sw
    XtXi = np.linalg.inv(Xs.T @ Xs)
    bet = XtXi @ Xs.T @ ys
    j = 5
    aj = Xs @ XtXi[:, j]  # fila j de (X'X)^-1 X' en forma de vector (n,)
    cl = pd.factorize(s.edad_sust)[0]
    G = cl.max() + 1
    e = ys - Xs @ bet
    sc = np.bincount(cl, weights=aj * e, minlength=G)
    se = float(np.sqrt((sc ** 2).sum() * G / (G - 1)))
    # restringido: sin la columna j
    keep = [c for c in range(X.shape[1]) if c != j]
    Xr = Xs[:, keep]
    br = np.linalg.lstsq(Xr, ys, rcond=None)[0]
    fit_r, u_r = Xr @ br, ys - Xr @ br
    rng = np.random.default_rng([SEED, 50])
    v = WEBB[rng.integers(0, 6, size=(G, B_WEBB))]
    Cm = np.zeros((len(ys), G))
    Cm[np.arange(len(ys)), cl] = 1.0
    ts = []
    for a in range(0, B_WEBB, 1000):
        Ys = fit_r[:, None] + v[:, a:a + 1000][cl] * u_r[:, None]
        Bs = XtXi @ (Xs.T @ Ys)
        Es = Ys - Xs @ Bs
        scs = Cm.T @ (aj[:, None] * Es)
        ses = np.sqrt((scs ** 2).sum(0) * G / (G - 1))
        ts.append(Bs[j] / ses)
    ts = np.concatenate(ts)
    tobs = float(bet[j] / se)
    p = float((1 + np.sum(np.abs(ts) >= abs(tobs))) / (B_WEBB + 1))
    c = float(np.quantile(np.abs(ts), 0.95))
    pb = pub("output/v16/q7/resultado.json", "estimacion", "principal_log_alquiler_h5")
    fila("V16", "Q7", "V16 Q7 bono alquiler joven", pb, float(bet[j]), "Δlog alquiler (diferencia en discontinuidades, ancho ±5)", "ninguna (sin intervalo; no se usa Kolesár-Rothe)",
         f"wild cluster bootstrap-t de Webb por edad del sustentador (variable de asignación discreta, {G} clusters; MCO ponderado con DB090, residuos restringidos, B=9.999)", int(G), se, p,
         float(bet[j]) - c * se, float(bet[j]) + c * se, "SIN_MEDIR",
         "Agrupar por edad es el estándar con variable de asignación discreta (Lee y Card 2008); la ECV es muestreo complejo (estratos y conglomerados no declarados en la publicación). Lectura: cambio de generosidad entre el Plan 2018-2021 y el Bono, no efecto del programa (ver q7).")


# ------------------------------------------------------------------ V16 · Q8 (no residentes, serie)
def bloque_v16_q8():
    import statsmodels.api as sm
    from src.v16 import q8_no_residentes as Q8
    aut, _ = Q8.cargar()
    w = Q8.agregado(aut)
    a0, a1, b0, b1 = (pd.Period(x, "Q") for x in ("2024Q2", "2025Q1", "2025Q2", "2026Q1"))
    antes, desp = w.loc[a0:a1], w.loc[b0:b1]
    cuota = lambda s_: float(s_.no_residentes_total.sum() / s_.total.sum() * 100)
    pubd = cuota(desp) - cuota(antes)
    pb = pub("output/v16/q8/resultado.json", "estimacion", "dif_pp")
    ss = pd.concat([antes, desp])
    yv = ss.cuota_no_res.values
    X = sm.add_constant((np.arange(len(ss)) >= 4).astype(float))
    L = int(np.floor(4 * (len(ss) / 100) ** (2 / 9)))
    m = sm.OLS(yv, X).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": True}, use_t=True)
    b, se = float(m.params[1]), float(m.bse[1])
    tc = stats.t.ppf(0.975, len(ss) - 2)
    fila("V16", "Q8", "V16 Q8 no residentes", pb, pubd, "puntos porcentuales de cuota (ventana de 4 trimestres posterior a 2025Q2 menos la anterior)", "ninguna (descriptiva)",
         f"Newey-West (Bartlett, retardo {L} = regla de Newey-West 1994 con T=8) sobre la cuota trimestral con una ficticia de periodo, t(6)", len(ss), se, float(m.pvalues[1]), b - tc * se, b + tc * se,
         "SIN_MEDIR", f"La estimación publicada es la razón de sumas ({pubd:.4f}); la regresión sobre cuotas trimestrales da {b:.4f} (diferencia de medias simples): se usa para la inferencia. Solo 8 trimestres: la corrección de HAC con T tan pequeño es poco fiable. "
         "La referencia del año anterior (-0,68 pp) no se contrasta: la comparación es entre ventanas, no un diseño con grupo de control.")
    FILAS[-1]["nota"] += " (El punto reproducido es la razón de sumas publicada, no el de la regresión.)"


# ------------------------------------------------------------------ salida
def escribe(df: pd.DataFrame, t0: float):
    SALIDA.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA / "inferencia.csv", index=False)
    rep = df.assign(rel=(df.estimacion_reproducida - df.estimacion_publicada).abs() / df.estimacion_publicada.abs().clip(lower=1e-300))
    pubs = df[df.publicable == "si"]
    res = {
        "rama": "v17/f2/v15_v16_micro",
        "pregunta": "¿Qué inferencia convencional daría un trabajo estándar a las estimaciones de V15 (H1-H4) y V16 (Q1-Q4, Q6-Q8) publicadas sin inferencia, y con qué distorsión medida?",
        "capa": "C4 (sin cambio: la lectura convencional va en su propia columna)",
        "datos": "entrenamiento de V15 y V16 (data/processed/v15, data/processed/v16/entrenamiento, ECV y MIVAU en data/raw); sin muestras selladas",
        "N": {"filas": int(len(df)), "publicables": int((df.publicable == "si").sum()), "no_fiables": int((df.publicable == "no_fiable").sum()), "sin_medir": int((df.publicable == "sin_medir").sum())},
        "metodo": "Inferencia convencional a posteriori según docs/v17/brief_f2_inferencia.md; regla del 15 % con el tamaño real de los Monte Carlo de V15 y V16; Holm y BH dentro de cada pregunta",
        "estimacion": {r.id_resultado: {"estimacion": r.estimacion_reproducida, "unidad": r.unidad} for r in df.itertuples()},
        "ic95": {r.id_resultado: [r.ic95_lo, r.ic95_hi] for r in pubs.itertuples()},
        "p_ajustado": {r.id_resultado: {"p": r.p_conv, "holm_pregunta": r.p_holm_pregunta, "bh_pregunta": r.p_bh_pregunta, "pregunta": r.pregunta} for r in df[df.publicable != "no_fiable"].itertuples()
                       if np.isfinite(r.p_holm_pregunta)},
        "nivel_evidencia": "DESCRIPTIVO (sin cambio de capa; lectura convencional a posteriori)",
        "diagnosticos": {"reproduccion_punto_maxima_rel": float(rep.rel.max()), "filas_no_reproducidas": rep[rep.rel > 1e-6].id_resultado.tolist(),
                         "no_fiables": df[df.publicable == "no_fiable"].id_resultado.tolist(), "sin_medir": df[df.publicable == "sin_medir"].id_resultado.tolist(),
                         "publicables": pubs.id_resultado.tolist(), "semilla": SEED, "B_webb": B_WEBB, "segundos": round(time.time() - t0, 1)},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "nota": "a posteriori",
        "notas": "Análisis a posteriori (V17): no sustituye a las capas del proyecto ni es confirmatorio. Las filas no fiables solo llevan la estimación puntual. Sin lenguaje causal.",
    }
    (SALIDA / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else float(o)) + "\n", encoding="utf-8")
    informe(df)


def informe(df: pd.DataFrame):
    L = ["Análisis a posteriori (V17). Inferencia convencional de las estimaciones de V15 y V16 (grupo v15_v16_micro) publicadas sin inferencia.", "",
         "Misma muestra, misma especificación y mismo estimador puntual que lo publicado; solo cambia la inferencia. Regla del 15 %: si el tamaño real del contraste al 5 % nominal "
         "medido en el Monte Carlo del repositorio supera el 15 %, la fila es «no fiable» y solo lleva la estimación puntual. Holm y BH se calculan dentro de cada pregunta (nunca entre preguntas) "
         "como sensibilidad junto al ajuste original del proyecto; m es el número de contrastes primarios de la pregunta (incluidos los no fiables); las filas alternativas del mismo punto quedan fuera. "
         "Nada cambia de capa (todas siguen en C4, DESCRIPTIVO). Sin lenguaje causal.", "",
         "| id | pregunta | estimación publicada | reproducida | método convencional | p | IC 95 % | tamaño real | publicable | Holm | BH |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    f = lambda x, d=4: "" if not np.isfinite(x) else f"{x:.{d}g}"
    for r in df.itertuples():
        ic = "" if not np.isfinite(r.ic95_lo) else f"[{r.ic95_lo:.4g}; {r.ic95_hi:.4g}]"
        L.append(f"| {r.id_resultado} | {r.pregunta} | {f(r.estimacion_publicada, 6)} | {f(r.estimacion_reproducida, 6)} | {r.metodo_convencional[:70]} | {f(r.p_conv)} | {ic} | {f(r.tamano_real)} | {r.publicable} | {f(r.p_holm_pregunta)} | {f(r.p_bh_pregunta)} |")
    L += ["", "## Frases publicables", ""]
    L += [f"- **{r.id_resultado}** ({r.herramienta_mc}): {r.frase}" for r in df.itertuples() if r.publicable != "no_fiable"]
    L += ["", "## No fiables (solo estimación puntual)", ""]
    L += [f"- **{r.id_resultado}**: {r.frase} Distorsión tomada de: {r.herramienta_mc}." for r in df.itertuples() if r.publicable == "no_fiable"]
    L += ["", "## Notas por fila", ""] + [f"- **{r.id_resultado}**: {r.nota}" for r in df.itertuples()]
    L += ["", "## No cubierto", "",
          "- Q1a (recuento de elegibilidad) y Q1b (SDID con Conley-Taber, no estimable en el entrenamiento por no haber periodo posterior): sin estimación sujeta a inferencia.",
          "- Q3-b y Q3-c comparten familia (Q3); las alternativas AKM/AKM0 de la misma estimación y los Webb sin medir de Q6 no entran en Holm/BH.",
          "- Honest DiD, TOST y BLP/GATES no son inferencia de estos resultados y no se tocan. Fuentes del tamaño real: docs/v15/validacion_montecarlo/*.md, docs/v16/validacion_montecarlo.md y output/v16/montecarlo/."]
    (SALIDA / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    t0 = time.time()
    for nombre, fn in (("v15 zonas", bloque_v15_zonas), ("v15 h3", bloque_v15_h3), ("v15 h4", bloque_v15_h4), ("v16 q1", bloque_v16_q1), ("v16 q2", bloque_v16_q2),
                       ("v16 q3b", bloque_v16_q3b), ("v16 q3c", bloque_v16_q3c), ("v16 q4", bloque_v16_q4), ("v16 q6", bloque_v16_q6), ("v16 q7", bloque_v16_q7), ("v16 q8", bloque_v16_q8)):
        t = time.time()
        fn()
        print(nombre, round(time.time() - t, 1), "s", flush=True)
    escribe(cierre(), t0)
    print("hecho", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
