"""V17 fase 2 · grupo series_v8_v9_v12. ANÁLISIS A POSTERIORI (V17 se ejecuta dentro de V18).

Recalcula la inferencia CONVENCIONAL (Newey-West 1994 en series; error de media de grupo en paneles; Pearson/Fisher; DM-HLN y Clark-West) de
resultados ya publicados, con el mismo estimador puntual, y la pone junto al tamaño real medido en el Monte Carlo del repositorio (regla del 15 %).
No estima nada nuevo; no lee data/sealed ni muestras selladas; no ejecuta evaluate_*; no modifica scripts ni salidas anteriores (se importan funciones).
Uso: python3 src/v17/f2_inferencia_series_v8_v9_v12.py
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
warnings.filterwarnings("ignore")
SEED = 20261010
OUT = ROOT / "output" / "v17" / "lectura_bde" / "series_v8_v9_v12"
TOL = 1e-6
UMBRAL = 0.15
COLS = ["version", "id_resultado", "pregunta", "estimacion_publicada", "estimacion_reproducida", "unidad", "capa_proyecto", "inferencia_original",
        "metodo_convencional", "n_clusters", "se_conv", "p_conv", "ic95_lo", "ic95_hi", "herramienta_mc", "tamano_real", "fuente_mc", "publicable",
        "p_holm_pregunta", "p_bh_pregunta", "frase", "nota"]
NAN = np.nan
MC16, MC15, MC8 = "docs/v16/validacion_montecarlo.md", "docs/v15/validacion_montecarlo.md", "output/v8/F3/otros/montecarlo.csv"


# ------------------------------------------------------------------ utilidades
def nw_lag(n: int) -> int:
    """Retardo de Newey-West (1994): floor(4 (n/100)^(2/9))."""
    return int(np.floor(4 * (n / 100) ** (2 / 9)))


def nw_cov(A: np.ndarray, e: np.ndarray, L: int) -> np.ndarray:
    """Covarianza HAC (Bartlett) del MCO. A: n x k; e: residuos."""
    n, k = A.shape
    XtXi = np.linalg.inv(A.T @ A)
    u = A * e[:, None]
    S = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        G = u[l:].T @ u[:-l]
        S += w * (G + G.T)
    return XtXi @ S @ XtXi * n / (n - k)


def regla(tam):
    """Regla de publicación del encargo: >15 % no fiable; 5-15 % con frase; <=5 % conservador; sin medir -> con reserva."""
    if tam is None or (isinstance(tam, float) and np.isnan(tam)):
        return "con reserva (sin medir)"
    if tam > UMBRAL:
        return "no (no fiable)"
    return "sí"


def frase(p, tam, publ, extra=""):
    if publ.startswith("no"):
        return f"no fiable: el contraste convencional rechaza un {100 * tam:.1f} % de las veces bajo la nula (> 15 %); solo estimación puntual"
    ps = f"{p:.3g}".replace(".", ",")
    if publ.startswith("con reserva"):
        return f"p = {ps}; distorsión del contraste sin medir en el Monte Carlo del repositorio{extra}"
    t = f"{100 * tam:.1f}".replace(".", ",")
    s = f"p = {ps}; el contraste rechaza un {t} % de las veces bajo la nula"
    return s + ("; por debajo del 5 % nominal: conservador" if tam < 0.05 else "") + extra


def fila(version, idr, preg, pub, rep, unidad, capa, orig, met, se, p, lo, hi, herr, tam, fuente, nclus=NAN, nota="", extra=""):
    publ = regla(tam)
    ok = not publ.startswith("no")
    r = dict(version=version, id_resultado=idr, pregunta=preg, estimacion_publicada=pub, estimacion_reproducida=rep, unidad=unidad, capa_proyecto=capa,
             inferencia_original=orig, metodo_convencional=met, n_clusters=nclus, se_conv=se if ok else NAN, p_conv=p if ok else NAN,
             ic95_lo=lo if ok else NAN, ic95_hi=hi if ok else NAN, herramienta_mc=herr, tamano_real=NAN if tam is None else tam, fuente_mc=fuente,
             publicable=publ, p_holm_pregunta=NAN, p_bh_pregunta=NAN, frase="", nota=nota)
    if p is not None and not (isinstance(p, float) and np.isnan(p)):
        r["frase"] = frase(p, tam if tam is not None else NAN, publ, extra)
    elif not ok:
        r["frase"] = frase(NAN, tam, publ)
    else:
        r["frase"] = "sin p convencional (ver nota)"
    return r


def sin_inferencia(version, idr, preg, capa, orig, motivo, herr="", tam=None, fuente=""):
    """Fila de bloque ya publicado con bandas/IC, contable o descriptivo: no se recalcula."""
    r = {c: NAN for c in COLS}
    r.update(version=version, id_resultado=idr, pregunta=preg, capa_proyecto=capa, inferencia_original=orig, metodo_convencional="no se recalcula",
            herramienta_mc=herr, tamano_real=NAN if tam is None else tam, fuente_mc=fuente, publicable="n/a", frase=motivo, nota=motivo)
    return r


def familias(df: pd.DataFrame) -> pd.DataFrame:
    """Holm y BH DENTRO de cada pregunta, solo sobre filas con p convencional publicable. Nunca entre preguntas."""
    from statsmodels.stats.multitest import multipletests
    for preg, g in df.groupby("pregunta"):
        g = g[g.p_conv.notna()]
        if len(g) == 0:
            continue
        df.loc[g.index, "p_holm_pregunta"] = multipletests(g.p_conv.to_numpy(float), method="holm")[1]
        df.loc[g.index, "p_bh_pregunta"] = multipletests(g.p_conv.to_numpy(float), method="fdr_bh")[1]
    return df


# ------------------------------------------------------------------ V16 · Q5 (proyecciones locales, Newey-West)
# Tamaño real: V16 lp_newey_west_b, fila «NW M=4 normal», rho = 0,95 (persistencia intermedia), n ≈ 100, por horizonte.
TAM_NW = {1: 0.0843, 4: 0.1014, 8: 0.1102, 12: 0.1155}


def q5():
    from src.v16 import q5_proyecciones as Q5, qc_comun as C
    pub = json.load(open(ROOT / "output/v16/q5/resultado.json"))["estimacion"]
    sh = Q5.sorpresa(Q5.CHOQUES["mediana"])
    filas = []
    for etq, res in (("Q5-p", "valor_tasado"), ("Q5-a", "ipc_alquiler")):
        Y = np.log(C.nat_q(*Q5.RES[res]))
        for h in Q5.H:
            r = Q5.lp(Y, sh, h, 4, Q5.VENT[etq])
            A, e, n = r["A"], r["res"], r["n"]
            L = nw_lag(n)
            se = float(np.sqrt(nw_cov(A, e, L)[1, 1]))
            z = r["beta"] / se
            p = float(2 * (1 - stats.norm.cdf(abs(z))))
            pu = pub[etq]["irf_puntual_pct"][str(h)]
            fila_ = fila("V16", f"{etq}-h{h}" + ("-P" if h == 4 else ""), "Q5", pu, r["beta"], "% acumulado por DT de sorpresa", "C4",
                         "ninguna (lp_newey_west_b NO APTO)", f"Newey-West 1994 (retardo {L}), normal", se, p, r["beta"] - 1.96 * se, r["beta"] + 1.96 * se,
                         "lp_newey_west_b, NW M=4 normal, rho 0,95, h=%d" % h, TAM_NW[h], MC16 + " (lp_newey_west_b)",
                         nota=f"n = {n}; muestra {r['ini']}-{r['fin']}; LP con 4 rezagos del choque y de Δy; serie nacional (sin clusters). "
                              "Asociación con una sorpresa monetaria; MDE del valor tasado 1,47 % > referencia 0,6 %.")
            filas.append(fila_)
    return filas


# ------------------------------------------------------------------ V16 · Q9 (GSADF y CS-ARDL)
def q9():
    from src.v16 import q9_burbuja as Q9
    pub = json.load(open(ROOT / "output/v16/q9/resultado.json"))["estimacion"]
    g = pub["Q9-g"]
    filas = [fila("V16", "Q9-g", "Q9", g["gsadf_factor"], NAN, "estadístico GSADF del factor común", "C4", "bootstrap salvaje (Harvey et al. 2016), B=499; p = %.3f" % g["p_bootstrap"],
                  "ninguna adicional: el bootstrap salvaje ya es inferencia válida (se anota, no se recalcula)", NAN, g["p_bootstrap"], NAN, NAN,
                  "gsadf_factor (bootstrap salvaje; salto y volatilidad estocástica)", 0.0455, MC16 + " (gsadf_factor): APTO",
                  nota="Tamaño 0,0455 con salto y con volatilidad estocástica; 0,017 en homocedástico (conservador). El factor es heterocedástico (ARCH-LM p < 1e-6), "
                       "el escenario relevante es el de salto/estocástica. Potencia limitada (0,13 en alt_salto). Sin lectura convencional añadida.",
                  extra="; inferencia bootstrap ya publicada y APTA")]
    lvt, lrent, prov, idx = Q9.paneles()
    from src.v16 import qc_series as S
    r = S.mg_cs(lvt.to_numpy(), lrent.to_numpy(), 2, "CS-ARDL")
    th = np.asarray(r["theta_i"], float)
    th = th[np.isfinite(th)]
    n = len(th)
    se = float(th.std(ddof=1) / np.sqrt(n))
    t = float(th.mean() / se)
    p = float(2 * (1 - stats.t.cdf(abs(t), n - 1)))
    q = stats.t.ppf(0.975, n - 1)
    filas.append(fila("V16", "Q9-c-CS-ARDL-p2", "Q9", pub["Q9-c"]["theta_principal_CS_ARDL_p2"], float(th.mean()), "elasticidad de largo plazo (θ medio)", "C4",
                      "ninguna (csardl NO APTO)", "error de media de grupo (Pesaran-Smith): sd(θ_i)/√N, t(N-1)", se, p, float(th.mean() - q * se), float(th.mean() + q * se),
                      "csardl (N=38, T=95; escenario más parecido; el contraste simulado usa bootstrap de bloques, no el error de media de grupo)", 0.1015,
                      MC16 + " (csardl)", nclus=n,
                      nota=f"{n} provincias estimables; la media de grupo está dominada por unidades con velocidad cercana a 0 (mediana {np.median(th):.3f}); "
                           "el error de media de grupo no corrige dependencia transversal residual: lectura optimista."))
    return filas


# ------------------------------------------------------------------ V16 · Q10 (DM-HLN y Clark-West)
def dm_hln(e1, e2, h):
    d = e1 ** 2 - e2 ** 2
    P = len(d)
    dbar = d.mean()
    dc = d - dbar
    g = [float((dc[k:] * dc[:P - k]).sum() / P) for k in range(h)]
    var = (g[0] + 2 * sum(g[1:])) / P
    if var <= 0:
        return NAN, NAN, NAN
    dm = dbar / np.sqrt(var)
    hl = dm * np.sqrt((P + 1 - 2 * h + h * (h - 1) / P) / P)
    return float(hl), float(1 - stats.t.cdf(hl, P - 1)), float(np.sqrt(var))


def clark_west(real, y1, y2, h):
    """Modelo 1 = AR(4) (pequeño), modelo 2 = grande. H1: el grande reduce el ECM. Normal unilateral, NW con h-1 retardos."""
    e1, e2 = real - y1, real - y2
    f = e1 ** 2 - (e2 ** 2 - (y1 - y2) ** 2)
    P = len(f)
    A = np.ones((P, 1))
    se = float(np.sqrt(nw_cov(A, f - f.mean(), h - 1)[0, 0]))
    t = f.mean() / se
    return float(t), float(1 - stats.norm.cdf(t)), se


def q10():
    pub = json.load(open(ROOT / "output/v16/q10/resultado.json"))["estimacion"]
    filas = []
    for q in ("Q10-1", "Q10-2", "Q10-3"):
        prin = pub[q]["modelo_principal"]
        for h in (1, 4):
            d = pd.read_csv(ROOT / f"output/v16/q10/previsiones_{q.lower()}_h{h}.csv")
            real, a4 = d.real.to_numpy(), d.AR4.to_numpy()
            mods = [prin] + (["ECM_v1"] if q == "Q10-1" else [])
            for m in mods:
                ym = d[m].to_numpy()
                red = 1 - ((real - ym) ** 2).mean() / ((real - a4) ** 2).mean()
                pu = pub[q][f"h{h}"]["reduccion_ecm_vs_AR4"][m]
                tests = [("DM-HLN unilateral", dm_hln(real - a4, real - ym, h), 0.002 if h == 1 and m != "ECM_v1" else None, "dm_hln (nulo anidado, HLN unilateral, h=1)")]
                if m != "ECM_v1":   # Clark-West solo para pares anidados
                    tests.append(("Clark-West normal unilateral", clark_west(real, a4, ym, h), 0.033 if h == 1 else None, "dm_hln (nulo anidado, CW normal unilateral, h=1)"))
                for nom, (stat, p, se), tam, herr in tests:
                    nota = (f"n = {len(d)} objetivos ({d.objetivo.iloc[0]}-{d.objetivo.iloc[-1]}), misma muestra que AR(4); H1: el modelo reduce el ECM; ventana expansiva. "
                            + ("Horizonte 4: el Monte Carlo solo cubre h = 1 (sin medir). " if h == 4 else "")
                            + ("Par no anidado (ECM v1 frente a AR(4)): el Monte Carlo es de pares anidados (sin medir). " if m == "ECM_v1" else "")
                            + "Estadístico = %.3f." % stat)
                    filas.append(fila("V16", f"{q}-{m}-h{h}-{'HLN' if nom.startswith('DM') else 'CW'}", q, pu, red, "reducción relativa del ECM frente al AR(4)", "C4",
                                      "ninguna (dm_hln NO APTO)", nom + (f", NW h-1={h - 1} retardos" if nom.startswith("Clark") else ", HLN, t(P-1)"), se if np.isfinite(se) else NAN, p,
                                      NAN, NAN, herr if tam is not None else herr + " (sin escenario comparable)", tam, MC16 + " (dm_hln)", nota=nota))
    return filas


# ------------------------------------------------------------------ V15 · H5, P2, P7, P10
def v15():
    filas = []
    p9 = json.load(open(ROOT / "output/v15/p9/resultado.json"))
    dm = p9["diagnosticos"]["linea_base_K1"]["dm_combinacion_vs_base"]
    red = 1 - p9["estimacion"]["razon_ECM_combinacion_AR4"]
    filas.append(fila("V15", "H5-DM-HLN", "H5", red, NAN, "reducción relativa del ECM frente al AR(4)", "C4", "DM-HLN unilateral (APTO, V15)",
                      "DM-HLN unilateral ya publicado (no se recalcula: las previsiones no se guardaron)", NAN, dm["p_unilateral"], NAN, NAN,
                      "dfm_bvar_mcs (DM-HLN, P = 73; aquí P = 53)", 0.0545, MC15 + " (dfm_bvar_mcs): DM-HLN APTO",
                      nota="Inferencia ya válida y publicada. Tamaño medido con P = 73; con P = 53 no está medido exactamente. La combinación no bate al AR(4)."))
    filas.append(fila("V15", "H5-ClarkWest", "H5", red, NAN, "reducción relativa del ECM frente al AR(4)", "C4", "Clark-West NO APTO (V15)",
                      "Clark-West normal unilateral (no se calcula: no fiable)", NAN, NAN, NAN, NAN, "dfm_bvar_mcs (Clark-West, δ = 0)", 0.1895,
                      MC15 + " (dfm_bvar_mcs)", nota="Tamaño 0,1895 > 15 %: no fiable, solo estimación puntual. MCS al 10 % (0,123) y GW (0,031) no aptos."))
    # P2: CS-ARDL del valor tasado, p = 1 sin coste de uso (principal declarado)
    from src.v15 import p2_fundamentales as P2
    yy, aa, uc = P2.datos("tasado")
    th, ph, _ = P2.mg_like(yy.values, aa.values, uc.values, 1, False, True)
    pub2 = json.load(open(ROOT / "output/v15/p2/resultado.json"))["estimacion"]
    for nom, v, pubv, tam, herr, unidad in (("theta", th[:, 0], pub2["theta_precio_alquiler_CS_ARDL"], 0.0075, "westerlund_csardl: CS-ARDL elasticidad de largo plazo (cobertura 0,9925)", "elasticidad de largo plazo (θ medio)"),
                                            ("velocidad", ph, pub2["velocidad_media"], 0.997, "westerlund_csardl: CS-ARDL velocidad de ajuste media (cobertura 0,003)", "velocidad de ajuste media (φ)")):
        n = len(v)
        se = float(v.std(ddof=1) / np.sqrt(n))
        p = float(2 * (1 - stats.t.cdf(abs(v.mean() / se), n - 1)))
        q = stats.t.ppf(0.975, n - 1)
        filas.append(fila("V15", f"E1-P2-CS-ARDL-p1-{nom}", "P2", pubv, float(v.mean()), unidad, "C4", "ninguna (CS-ARDL NO APTO)", "error de media de grupo: sd/√N, t(N-1)", se, p,
                          float(v.mean() - q * se), float(v.mean() + q * se), herr, tam, MC15 + " (westerlund_csardl)", nclus=n,
                          nota=f"{n} provincias con corrección de error estable de 38; dependencia transversal fuerte (CD de Pesaran 128,7). No contrasta cointegración."))
    # P7: correlaciones provinciales (Pearson, t de Student y Fisher)
    from src.v15 import p7_demografia as P7
    pob0, dpob, ofertas, outs = P7.provincial()
    reg7 = pd.read_csv(ROOT / "output/v15/p7/registro.csv").set_index("modelo_id")
    for dem in ("hogares", "poblacion"):
        dh = dpob / P7.HOGAR if dem == "hogares" else dpob
        for on, oferta in ofertas.items():
            ofe = oferta if dem == "hogares" else oferta * P7.HOGAR
            exc = ((dh - ofe) / pob0).replace([np.inf, -np.inf], np.nan)
            for rn, ro in outs.items():
                df = pd.concat([exc.rename("x"), ro.rename("y")], axis=1).dropna()
                n = len(df)
                r = float(stats.pearsonr(df.x, df.y)[0])
                t = r * np.sqrt((n - 2) / (1 - r ** 2))
                p = float(2 * (1 - stats.t.cdf(abs(t), n - 2)))
                z, sz = np.arctanh(r), 1 / np.sqrt(n - 3)
                idr = f"E2-prov-{on}-{dem}-{rn}"
                filas.append(fila("V15", idr, "P7", float(reg7.loc[idr, "coef_interes"]), r, "correlación de Pearson", "C4", "ninguna (sin herramienta en K13)",
                                  "t de Student (df = n-2) e IC de Fisher; supone independencia entre provincias", float(np.tanh(z + sz) - r), p,
                                  float(np.tanh(z - 1.96 * sz)), float(np.tanh(z + 1.96 * sz)), "sin Monte Carlo para correlaciones provinciales", None, "sin medir", nclus=n,
                                  nota=f"n = {n} provincias; dependencia espacial probable (Moran en E3 p < 1e-40 a escala municipal): el IC es optimista. "
                                       "Se_conv = semiancho del IC en la escala de r. Asociación, no efecto."))
    s = json.load(open(ROOT / "output/v15/p10/resultado.json"))
    filas.append(fila("V15", "E3-SAR-contigüidad-2015_2024", "P10", s["estimacion"]["rho_SAR_contiguidad_2015_2024"], NAN, "ρ espacial (SAR, contigüidad)", "C4",
                      "Wald de ρ (sar_sdm APTO)", "Wald de ρ ya publicado (no se recalcula)", s["estimacion"]["se"], s["p_valores_para_BY"][0]["p"], s["ic95"][0], s["ic95"][1],
                      "sar_sdm: Wald de ρ (rango de celdas 0,0453-0,055)", 0.055, MC15 + " (sar_sdm): APTO",
                      nota="Ya tiene inferencia APTA y publicada; Moran de los residuos MCO z = 14,1 (contigüidad). Sin lectura convencional adicional."))
    return filas


# ------------------------------------------------------------------ V8
def v8():
    f = []
    h5 = pd.read_csv(ROOT / "output/v8/M5/hipotesis_m5.csv")
    for _, r in h5.iterrows():
        f.append(fila("V8", r["id"], "V8-M5", float(r.beta_descriptivo), NAN, "LP-IV acumulado (descriptivo)", "C4", "intervalo de Anderson-Rubin: (-inf, +inf) por instrumento débil",
                      f"Anderson-Rubin ya publicado; Wald/2SLS convencional NO se calcula (F efectivo de Montiel Olea-Pflueger = {r.F_efectivo:.2f} < 10)", NAN, float(r.ar_p),
                      NAN, NAN, "lp_iv, intervalo AR (cobertura 0,913-1,000)", 0.087, MC8 + " (lp_iv, AR: tamaño ≈ 1 - cobertura mínima)", nota=f"mercado {r.mercado}; "
                      f"primera etapa t = {r.t_primera_etapa:.2f}; instrumento débil: no hay inferencia informativa. IC normal tendría cobertura 0,85-0,997."))
    bl = [("M0", "C4", "OLS por tramo con EE HAC; confirmaciones con bootstrap sieve-AR; BH q = 0,10 (70 coeficientes)", "lp_ols/NW (aprox.)", MC8),
          ("M1", "C4", "PCA/DFM, IC por bootstrap de bloques circulares; Holm {H8-8, H8-9}", "dfm_pca / dfm_ml", MC8),
          ("M2", "C3s", "BVAR-GLP + restricciones de signo: bandas 68/90 % de IRF y descomposición histórica; Holm H8-1..H8-4 (p 0,43-0,82)", "BVAR-GLP (cobertura 90 %: 0,86-0,97, con reservas)", "output/v8/F3/var/validacion.md"),
          ("M3", "C4", "LP-OLS con interacción por periodo, EWC fixed-b; BH", "lp_ols EWC (cobertura 0,838-0,948)", MC8),
          ("M4", "C4", "DOLS/FMOLS/ARDL-bounds; BH sobre largo plazo", "sin Monte Carlo propio", ""),
          ("M6", "C4", "dominancia LMG/Shapley con bandas bootstrap de bloques (68/90 %)", "dominancia (V8 F3)", MC8),
          ("M7", "C4", "multiverso: OLS HAC, BH por mercado y periodo", "lp_ols/NW (aprox.)", MC8),
          ("M8", "C4", "ecuación por CCAA, panel FE con Driscoll-Kraay, LP panel (DK); BH", "sin Monte Carlo para Driscoll-Kraay", ""),
          ("M9", "C4", "LightGBM/SHAP con bandas bootstrap de bloques; DML con IC95; BH", "shap_grupos (V8 F3)", MC8),
          ("F5", "C3s para svar_hd; C4 el resto", "atribución combinada con banda 68 % de svar_hd; cuota no atribuida explícita", "BVAR-GLP", "output/v8/F3/var/validacion.md")]
    for b, capa, orig, herr, fu in bl:
        f.append(sin_inferencia("V8", f"V8-{b}", f"V8-{b}-bloque", capa, orig, "ya tiene bandas/IC publicados: se anota y no se recalcula. Atribución con bandas; sin lectura causal fuera de C3/C3s", herr, None, fu))
    return f


# ------------------------------------------------------------------ V9
MAPA9 = {"D1a": ("wild_webb_v15 W1 (CS, wild bootstrap por municipio, 198 municipios)", 0.2155, MC15 + " (wild_webb_v15, W1_H1H2_198municipios)"),
         "D1b": ("wild_webb_v15 W1 (escenario más parecido; Barcelona, 60 tratados)", 0.2155, MC15 + " (wild_webb_v15, W1)"),
         "D1c": ("sin Monte Carlo (CS aún no tratados, N = 13-20)", None, "sin medir"),
         "D2": ("rejilla_twfe, municipio (TWFE con dosis continua)", 0.203, MC16 + " (rejilla_twfe, municipio)"),
         "D3": ("conley_seccion (Conley a 2 km; aquí 10 km)", 0.0963, MC16 + " (conley_seccion)"),
         "D4": ("akm_municipal, AKM (shift-share; también shiftshare_akm 0,3762)", 0.2193, MC15 + " (akm_municipal, M1)"),
         "D5": ("sin Monte Carlo para Driscoll-Kraay (N = 17-18 países)", None, "sin medir")}


def v9():
    t = pd.read_csv(ROOT / "output/v9/f3/tabla_capas.csv")
    f = []
    for i, r in t.iterrows():
        herr, tam, fu = MAPA9[r.diseno]
        f.append(fila("V9", f"V9-{r.diseno}-{i:02d}-{str(r.hipotesis)[:24]}", f"V9-{r.diseno}", NAN, NAN, str(r.resultado)[:60], r.capa, f"{r.metodo} (inferencia convencional ya publicada)",
                      "la ya publicada en tabla_capas.csv (no recalculada: pipeline de V9 no reejecutado)", float(r.se), float(r.p), float(r.ic95_lo), float(r.ic95_hi), herr, tam, fu,
                      nclus=NAN, nota=f"beta publicado = {r.beta:.5f}; N = {int(r.N)}; estimacion_publicada se deja vacía porque el punto no se reestima aquí: es lectura del fichero publicado."))
        f[-1]["estimacion_publicada"] = float(r.beta)
    f.append(sin_inferencia("V9", "V9-D7", "V9-D7", "C4 (contable)", "descomposición contable de población (sin estimación)", "contable: sin inferencia que recalcular"))
    f.append(sin_inferencia("V9", "V9-D6", "V9-D6", "no estimado", "no se estima (ECV sin mes de nacimiento)", "no estimado en V9"))
    return f


# ------------------------------------------------------------------ V12
def v12():
    bl = [("f0", "correcciones y hechos de partida: contable"), ("b1", "contabilidad de población: contable"), ("b2", "flujos migratorios: contable + Spearman con IC bootstrap y Holm ya publicados (descriptivo C4)"),
          ("b3", "hogares: contable"), ("b4", "oferta: contable"), ("b5", "titularidad: Spearman con IC y Holm ya publicados (descriptivo C4)"), ("b6", "condiciones de vivienda: descriptivo"),
          ("b7", "turismo: contrastes descriptivos con Holm/BH ya publicados (C4)")]
    return [sin_inferencia("V12", f"V12-{b}", f"V12-{b}", "C1/C4 (contable o descriptivo)", o, "contable o descriptivo: sin estimación causal ni inferencia que recalcular (una fila por bloque)") for b, o in bl]


# ------------------------------------------------------------------ principal
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(q5() + q9() + q10() + v15() + v8() + v9() + v12(), columns=COLS)
    df = familias(df)
    df.to_csv(OUT / "inferencia.csv", index=False)
    rep = df[df.estimacion_reproducida.notna() & df.estimacion_publicada.notna()]
    desv = (rep.estimacion_reproducida - rep.estimacion_publicada).abs() / rep.estimacion_publicada.abs().clip(lower=1e-12)
    res = {"rama": "v17/f2/series_v8_v9_v12", "pregunta": "Inferencia convencional a posteriori de V8, V9, V12, V15 y V16 (grupo series) junto a la distorsión del Monte Carlo",
           "capa": "sin cambio de capa (lectura paralela a posteriori)", "datos": "output/v8, v9, v12, v15, v16 (entrenamiento; nunca muestras selladas)",
           "N": int(len(df)), "metodo": "Newey-West 1994 en series; error de media de grupo en paneles; Pearson/Fisher; DM-HLN y Clark-West; regla del 15 %; Holm y BH dentro de cada pregunta",
           "estimacion": {"filas": int(len(df)), "reproducidas": int(len(rep)), "max_desviacion_relativa": float(desv.max()) if len(desv) else None,
                          "publicables": int((df.publicable == "sí").sum()), "con_reserva_sin_medir": int((df.publicable == "con reserva (sin medir)").sum()),
                          "no_fiables": int(df.publicable.str.startswith("no").sum()), "bloques_sin_recalcular": int((df.publicable == "n/a").sum())},
           "ic95": None, "p_ajustado": {"metodo": "Holm y BH dentro de cada pregunta (sensibilidad; no sustituye al ajuste original)", "ver": "inferencia.csv"},
           "nivel_evidencia": "DESCRIPTIVO / lectura convencional a posteriori", "diagnosticos": {"semilla": SEED, "tolerancia_reproduccion": TOL, "regla": "tamaño real > 15 % → no fiable"},
           "fuera_muestra": {"modelo": "Q10 y H5 evaluados con DM-HLN y Clark-West frente a AR(4)", "rmse": None, "dm_vs_ar4": "ver inferencia.csv (filas Q10-* y H5-*)"},
           "notas": ["a posteriori", "Nada cambia de capa ni de valor publicado."], "nota": "a posteriori"}
    (OUT / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    informe(df, res)
    return df


def informe(df: pd.DataFrame, res: dict):
    e = res["estimacion"]
    L = ["Análisis a posteriori (V17). Grupo series_v8_v9_v12: inferencia convencional de resultados publicados sin inferencia apta, junto al tamaño real medido en el Monte Carlo.", "",
         f"Filas: {e['filas']}; reproducidas: {e['reproducidas']} (desviación relativa máxima {e['max_desviacion_relativa']:.2e}, tolerancia 1e-6); publicables: {e['publicables']}; "
         f"con reserva (sin medir): {e['con_reserva_sin_medir']}; no fiables (> 15 %): {e['no_fiables']}; bloques sin recalcular: {e['bloques_sin_recalcular']}.", "",
         "Todo se rotula a posteriori; nada cambia de capa ni de valor. Sin lenguaje causal. Holm y BH por pregunta, nunca entre preguntas.", ""]
    for v, g in df.groupby("version", sort=False):
        L += [f"## {v}", ""]
        for _, r in g.iterrows():
            est = "" if pd.isna(r.estimacion_publicada) else f" punto {r.estimacion_publicada:.4g};"
            L.append(f"- **{r.id_resultado}** ({r.pregunta}, {r.capa_proyecto}):{est} {r.frase} [{r.publicable}; herramienta: {r.herramienta_mc}]")
        L.append("")
    L += ["## Límites", "- V8, V9 y V12: salvo M5, se anota que ya tienen bandas/IC publicados o son contables; V9 reutiliza el error publicado y solo añade la regla del 15 % (pipeline no reejecutado).",
          "- Newey-West de Q5: retardo de Newey-West 1994 con normal; el escenario del Monte Carlo es «NW M=4 normal», rho = 0,95.",
          "- El error de media de grupo (Q9-c, P2) no corrige dependencia transversal residual; el Monte Carlo disponible usa otro procedimiento (bootstrap de bloques).",
          "- Correlaciones de P7: distorsión sin medir; el IC supone independencia entre provincias.",
          "- No se calculó Driscoll-Kraay ni Webb: los paneles de V9 no se reestimaron.", "- P10 ya tiene inferencia APTA (Wald de ρ); Q9-g tiene bootstrap salvaje APTO."]
    (OUT / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    d = main()
    print(d.publicable.value_counts().to_dict())
