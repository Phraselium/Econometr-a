"""Reproduccion de Chaves-Fonseca (2026), SERIEs, tabla 2 (efecto de los anuncios de Airbnb sobre el
log del precio de la vivienda, Madrid, barrio-ano 2010-2018). Traduccion a Python de
code/01_analysis_main.do (Stata, reghdfe/ivreghdfe) del paquete de replicacion (CC BY 4.0,
figshare 10.6084/m9.figshare.26263979.v2).

Reproduccion del estudio original con sus datos; no usa datos del proyecto.
Requiere: pandas, numpy, statsmodels, linearmodels (pip install linearmodels si falta).
pyreadstat NO hace falta: pandas.read_stata lee el .dta.
"""
import json
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS

ALCANCE_TERRITORIAL = "sin lectura de datos"  # no lee data/raw, data/processed ni la base del proyecto
SEED = 20261010
np.random.seed(SEED)

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CLAVE = "chavesfonseca2026"
PAQ = os.path.join(RAIZ, "data", "bib", "replicacion", CLAVE, "replication_package_published")
SALIDA = os.path.join(RAIZ, "output", "v18", "reproduccion", CLAVE)

# Publicado: output/tables/tab_2.tex (columnas 1-7): coeficiente, error tipico, F primera etapa
PUBLICADO = {
    1: (0.061, 0.017, None), 2: (0.024, 0.007, None), 3: (0.025, 0.005, None),
    4: (0.015, 0.003, None), 5: (0.014, 0.003, None),
    6: (0.020, 0.004, 20.691), 7: (0.022, 0.005, 15.955),
}
N_PUBLICADO = 1029


def cargar():
    d = pd.read_stata(os.path.join(PAQ, "data", "01_masterdata.dta"), convert_categoricals=False)
    d = d[d["year"] >= 2010].copy()
    d["unit"] = d["neighborhood_id"].astype(int)
    d["time"] = d["year"].rank(method="dense").astype(int)  # egen group(year)
    d["t_sq"] = d["time"] ** 2
    d["bnb100"] = d["bnb_eh_1r_y"] / 100
    d["ln_h_price"] = np.log(d["h_price"].astype(float))
    d["ln_pop_density"] = np.log(d["pop_density"])
    d["foreign_share"] = d["foreign_share"] / 100
    d["ln_m_hh_income"] = np.log(d["m_hh_income"].astype(float))
    d["dist_km"] = d["dist_sol"].astype(float) / 1000
    d["dist_t"] = d["dist_km"] * d["time"]
    d["dist_t2"] = d["dist_km"] * d["t_sq"]
    d["ln_instrument3"] = np.log(d["share_iv_top3"].astype(float).where(d["share_iv_top3"] > 0)) * d["search_interest"].astype(float)
    return d


CONTROLES = ["ln_pop_density", "foreign_share", "median_age", "ln_m_hh_income", "high_educ_share"]


def estimar(d, controles, efectos_fijos, tendencia, iv):
    cols = ["ln_h_price", "bnb100", "unit", "time", "dist_t", "dist_t2", "ln_instrument3"] + CONTROLES
    m = d[cols].dropna().copy()
    X = pd.DataFrame({"const": 1.0}, index=m.index)
    if controles:
        for c in CONTROLES:
            X[c] = m[c].astype(float)
    if tendencia:
        X["dist_t"] = m["dist_t"]
        X["dist_t2"] = m["dist_t2"]
    if efectos_fijos:
        X = X.join(pd.get_dummies(m["unit"], prefix="u", drop_first=True, dtype=float))
        X = X.join(pd.get_dummies(m["time"], prefix="t", drop_first=True, dtype=float))
    y = m["ln_h_price"].astype(float)
    x = m["bnb100"].astype(float)
    g = m["unit"].values
    n = len(m)
    if not iv:
        res = sm.OLS(y, pd.concat([x, X], axis=1)).fit(
            cov_type="cluster", cov_kwds={"groups": g, "use_correction": True})
        # reghdfe: correccion G/(G-1)*(N-1)/(N-K), K sin efectos fijos anidados en el cluster
        b, se = res.params["bnb100"], res.bse["bnb100"]
        k_total = X.shape[1] + 1
        k_reghdfe = k_total - (X.filter(like="u_").shape[1] if efectos_fijos else 0)
        G = len(np.unique(g))
        ajuste_sm = (G / (G - 1)) * ((n - 1) / (n - k_total))
        ajuste_rh = (G / (G - 1)) * ((n - 1) / (n - k_reghdfe))
        se = se / np.sqrt(ajuste_sm) * np.sqrt(ajuste_rh)
        return dict(b=float(b), se=float(se), F=None, n=n)
    # IV: ivreghdfe sin 'small': varianza agrupada sin correccion de muestra finita de gl
    mod = IV2SLS(y, X, x, m[["ln_instrument3"]]).fit(cov_type="clustered", clusters=g, debiased=False)
    b, se = float(mod.params["bnb100"]), float(mod.std_errors["bnb100"])
    # F de primera etapa (Kleibergen-Paap rk Wald F con 1 instrumento: t^2 agrupado)
    fs = sm.OLS(x, pd.concat([m[["ln_instrument3"]], X], axis=1)).fit(
        cov_type="cluster", cov_kwds={"groups": g, "use_correction": False})
    F_asint = float(fs.tvalues["ln_instrument3"] ** 2)
    G = len(np.unique(g))
    k = X.shape[1] + 1
    # no se replica el ajuste exacto de ivreg2; la F asintotica difiere ~2 % de la publicada (ver informe)
    return dict(b=b, se=se, F=F_asint, F_asint=F_asint, n=n)


def main():
    os.makedirs(SALIDA, exist_ok=True)
    d = cargar()
    esp = {
        1: dict(controles=False, efectos_fijos=False, tendencia=False, iv=False),
        2: dict(controles=True, efectos_fijos=False, tendencia=False, iv=False),
        3: dict(controles=False, efectos_fijos=True, tendencia=False, iv=False),
        4: dict(controles=True, efectos_fijos=True, tendencia=False, iv=False),
        5: dict(controles=True, efectos_fijos=True, tendencia=True, iv=False),
        6: dict(controles=True, efectos_fijos=True, tendencia=False, iv=True),
        7: dict(controles=True, efectos_fijos=True, tendencia=True, iv=True),
    }
    filas = []
    for c, e in esp.items():
        r = estimar(d, **e)
        pb, pse, pF = PUBLICADO[c]
        dif = r["b"] - pb
        rel = dif / pb
        dentro_redondeo = round(r["b"], 3) == pb
        dentro_error = abs(dif) <= pse
        ok = dentro_redondeo or (abs(rel) < 0.05 and dentro_error)
        filas.append(dict(
            columna=c, tipo="IV" if e["iv"] else "MCO", coef_repro=round(r["b"], 5), se_repro=round(r["se"], 5),
            coef_publicado=pb, se_publicado=pse, dif_abs=round(dif, 5), dif_rel=round(rel, 4),
            se_dif_abs=round(r["se"] - pse, 5), F_repro=None if r["F"] is None else round(r["F"], 3),
            F_asint_sin_ajuste=None if r["F"] is None else round(r["F_asint"], 3),
            F_publicado=pF, n_repro=r["n"], n_publicado=N_PUBLICADO,
            veredicto="coincide" if ok else "difiere"))
    tab = pd.DataFrame(filas)
    tab.to_csv(os.path.join(SALIDA, "tabla.csv"), index=False)

    iv = tab[tab["tipo"] == "IV"].set_index("columna")
    ok_iv = bool((iv["veredicto"] == "coincide").all())
    todos = bool((tab["veredicto"] == "coincide").all())
    c6 = iv.loc[6]
    est = float(c6["coef_repro"])
    se = float(c6["se_repro"])
    ic = [round(est - 1.96 * se, 4), round(est + 1.96 * se, 4)]
    veredicto = "coincide" if todos else ("coincide (IV)" if ok_iv else "difiere")
    res = dict(
        rama="v18-reproduccion", pregunta=CLAVE, capa="C4",
        datos="Paquete de replicacion de Chaves-Fonseca (2026), panel barrio-ano Madrid 2010-2018, CC BY 4.0",
        N=int(c6["n_repro"]),
        metodo="IV (shift-share: ln proximidad top-3 atractivos x busquedas Google), efectos fijos de barrio y ano, "
               "controles, error tipico agrupado por barrio; traduccion Python (linearmodels) de ivreghdfe; tabla 2 col. 6",
        estimacion=est, ic95=ic, p_ajustado=None, nivel_evidencia="EXPLORATORIO (reproduccion; no es evidencia del proyecto)",
        diagnosticos=dict(F_primera_etapa_col6=c6["F_repro"], F_publicado_col6=20.691,
                          col7_coef=float(iv.loc[7, "coef_repro"]), col7_se=float(iv.loc[7, "se_repro"]),
                          col7_F=iv.loc[7, "F_repro"], col7_F_publicado=15.955),
        fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
        notas=f"Veredicto: {veredicto}. Madrid esta sellada en la validacion v6 del proyecto: la replica con datos "
              "del proyecto en Madrid no se hara; esta reproduccion usa solo datos del autor original. "
              "Movilidad (tabla 4) y alquileres no reproducidos.")
    with open(os.path.join(SALIDA, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

    lineas = [
        "# Reproduccion de Chaves-Fonseca (2026), tabla 2 (precios)",
        "",
        "**Rotulo: reproduccion del estudio original con sus datos; no usa datos del proyecto.**",
        "",
        "- Estudio: Chaves-Fonseca (2026), SERIEs, DOI 10.1007/s13209-026-00335-2. Paquete CC BY 4.0, figshare "
        "10.6084/m9.figshare.26263979.v2 (version 2 del 7-4-2026).",
        "- Codigo original: Stata (`code/01_analysis_main.do`, lineas 371-519; reghdfe/ivreghdfe). Sin Stata: traducido a Python "
        "(pandas, statsmodels, linearmodels 7.0; efectos fijos por variables ficticias; `pandas.read_stata`, sin pyreadstat).",
        "- Semilla 20261010 (la estimacion es determinista, no hay aleatoriedad).",
        "- Aviso territorial: Madrid es provincia sellada en la validacion v6 del proyecto. Reproducir el estudio con los datos de su "
        "autor no la toca, pero la replica con datos del proyecto en Madrid no se hara.",
        "- Decisiones de traduccion: `egen group(year)` -> rango denso del ano; tendencia `c.dist_sol#c.time` y `#c.time^2` con "
        "distancia en km; IV con una sola excluida `ln(share_iv_top3) x search_interest`; error tipico agrupado por barrio. "
        "OLS: correccion reghdfe (G/(G-1)*(N-1)/(N-K), con efectos de barrio anidados excluidos de K). IV: sin correccion de gl "
        "(ivreghdfe sin `small`). F de primera etapa: t^2 agrupado sin ajuste de muestra finita (aproximacion al rk Wald F de Kleibergen-Paap; difiere ~2 % de la publicada por el ajuste de grados de libertad de ivreg2, no replicado).",
        "",
        "## Comparacion con tab_2.tex (variable dependiente: log precio; coeficiente por 100 anuncios)",
        "",
        "| Col | Tipo | Repro | EE repro | Publicado | EE publ. | Dif abs | Dif rel | F repro | F publ. | N | Veredicto |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for _, r in tab.iterrows():
        lineas.append(
            f"| {r.columna} | {r.tipo} | {r.coef_repro:.4f} | {r.se_repro:.4f} | {r.coef_publicado:.3f} | {r.se_publicado:.3f} | "
            f"{r.dif_abs:.4f} | {r.dif_rel:.1%} | {'' if pd.isna(r.F_repro) else r.F_repro} | "
            f"{'' if pd.isna(r.F_publicado) else r.F_publicado} | {r.n_repro} | {r.veredicto} |")
    lineas += [
        "",
        f"N publicado: {N_PUBLICADO}. Veredicto global: **{veredicto}**.",
        "",
        "## Alcance y limites",
        "",
        "- Reproducido: tabla 2 (cols. 1-7). No reproducidos: tabla 4 (movilidad: requiere ivreghdfe con tendencias por valor base, "
        "no hecho por tiempo), tabla 5 (mediacion `ivmediate`) y alquileres (revision); no se contrastan con el texto del articulo "
        "(solo resumen y tablas del paquete).",
        "- No se redistribuyen datos del paquete: aqui solo hay coeficientes y estadisticos agregados.",
        "- Dependencia anotada: `pip install linearmodels` (ya instalado, version 7.0).",
    ]
    with open(os.path.join(SALIDA, "informe.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print(tab.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
