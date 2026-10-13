"""V8-F6: tablas de modelos destacados (md, csv, xlsx). Solo lee salidas versionadas de output/v8 (M0-M9, F5).

No estima nada. Criterio de §9 del pre-registro:
 (a) modelos que cumplen la regla de §8 (cumple_regla_m0) Y la del multiverso (cumple_multiverso);
 (b) ademas, el mejor de cada familia por mercado y periodo segun el error fuera de muestra (bloques con embargo),
     NUNCA por p, marcado «no cumple la regla» si es el caso.
Unidad de destacado: modelo_id (la ecuacion completa); la regla (a) se evalua por variable.
Determinista (SEED = 20261010), sin red, sin aleatoriedad.
"""
import hashlib
import json
import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Font  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v8"
SAL = OUT / "F6"
SCRIPT = "src/v8/f6_tablas.py"
FECHA_FIJA = datetime(2026, 10, 13, 0, 0, 0)
MODULOS_COEF = ["M0", "M1", "M3", "M4", "M5", "M6", "M8", "M9"]
COLS_CONTRATO = [
    "modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion",
    "medida_precio", "variable", "beta", "ee", "tipo_ee", "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo",
    "ic95_hi", "beta_std", "elasticidad", "n", "r2", "r2_adj", "aic", "bic", "vel_ajuste", "semivida", "coint_p",
    "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable", "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa",
    "n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_regla_m0", "cumple_multiverso", "destacado",
    "motivo_destacado", "script"]
COLS_EXTRA = ["criterio_destacado", "oos_ref", "rmse_oos", "rmse_ar4_oos", "ratio_rmse_vs_ar4", "no_cumple_regla",
              "fuente"]
AZUL, NEGRO, VERDE = "0000FF", "000000", "008000"


# ----------------------------------------------------------------------------------------- utilidades
def rel(p):
    return str(Path(p).resolve().relative_to(RAIZ))


def vacio(x):
    return x is None or (isinstance(x, float) and np.isnan(x)) or (x is pd.NA) or (isinstance(x, str) and x == "")


def fmt(x, d=3):
    if vacio(x):
        return "—"
    if isinstance(x, (bool, np.bool_)):
        return "sí" if x else "no"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        if x != 0 and abs(x) < 10 ** (-d):
            return f"{x:.1e}"
        return f"{x:.{d}f}"
    return str(x)


def sino(x):
    if vacio(x):
        return "—"
    if isinstance(x, str):
        return {"True": "sí", "False": "no", "si": "sí"}.get(x, x)
    return "sí" if bool(x) else "no"


def estrellas(p):
    if vacio(p):
        return ""
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def norm_var(v):
    return v[3:] if isinstance(v, str) and v.startswith("d4_") else v


def sha256(p):
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return h.hexdigest()


# ----------------------------------------------------------------------------------------- lectura
def leer_coef():
    fr = []
    for m in MODULOS_COEF:
        f = OUT / m / "coeficientes.csv"
        d = pd.read_csv(f)
        d["fuente"] = rel(f)
        fr.append(d)
    return pd.concat(fr, ignore_index=True, sort=False)


def leer_oos():
    """Tabla larga de error fuera de muestra por modulo: columnas modulo, mercado, ambito, muestra, modelo, rmse,
    rmse_ar4, p_dm_vs_ar4, metodo_p, fuente. Solo lee fuera_muestra de los resultados de cada modulo."""
    filas = []
    # M0 (resultado.json)
    f = OUT / "M0" / "resultado.json"
    r = json.load(open(f))["fuera_muestra"]
    for mer, d in r["rmse"].items():
        det = r["detalle"][mer]
        for mod, v in d.items():
            p = None if mod == "AR4" else r["dm_vs_ar4"][mer][mod]["p"]
            filas.append(dict(modulo="M0", mercado=mer, ambito="nacional", muestra=det["muestra"], modelo=mod,
                              rmse=v, rmse_ar4=d["AR4"], p_dm_vs_ar4=p, metodo_p="sin ajustar (DM-HLN)",
                              fuente=rel(f)))
    # M4
    f = OUT / "M4" / "fuera_muestra.csv"
    d = pd.read_csv(f)
    sr = [c for c in d.columns if c.startswith("rmse_SR")][0]
    ec = [c for c in d.columns if c.startswith("rmse_ECM")][0]
    psr = [c for c in d.columns if c.startswith("dm_p_SR") and c.endswith("_ajustado")][0]
    pec = [c for c in d.columns if c.startswith("dm_p_ECM") and c.endswith("_ajustado")][0]
    for _, x in d.iterrows():
        base = dict(modulo="M4", mercado=x["mercado"], ambito="nacional", muestra=f'{x["muestra"]} (n={x["n"]})',
                    rmse_ar4=x["rmse_AR4"], metodo_p=f'{x["metodo_ajuste"]} (DM-HLN)', fuente=rel(f))
        filas.append(dict(base, modelo=f'{x["spec"]}_{x["rupturas"]}_AR4', rmse=x["rmse_AR4"], p_dm_vs_ar4=None))
        filas.append(dict(base, modelo=f'{x["spec"]}_{x["rupturas"]}_SR', rmse=x[sr], p_dm_vs_ar4=x[psr]))
        filas.append(dict(base, modelo=f'{x["spec"]}_{x["rupturas"]}_ECM', rmse=x[ec], p_dm_vs_ar4=x[pec]))
    # M6
    f = OUT / "M6" / "fuera_muestra.csv"
    d = pd.read_csv(f)
    for _, x in d.iterrows():
        filas.append(dict(modulo="M6", mercado=x["mercado"], ambito="nacional",
                          muestra=f'{x["periodo"]} (n_oos={x["n_oos"]})', modelo=x["modelo"], rmse=x["rmse"],
                          rmse_ar4=x["rmse_ar4"], p_dm_vs_ar4=None if x["modelo"] == "ar4" else x["p_holm_vs_ar4"],
                          metodo_p="Holm (DM-HLN)", fuente=rel(f)))
    # M9
    f = OUT / "M9" / "oos.csv"
    d = pd.read_csv(f)
    for mer in ("compra", "alquiler"):
        for amb in d["ambito"].unique():
            s = d[(d["mercado"] == mer) & (d["ambito"] == amb)]
            ar4 = float(s.loc[s["modelo"] == "ar4", "rmse"].iloc[0])
            for _, x in s.iterrows():
                filas.append(dict(modulo="M9", mercado=mer, ambito=amb, muestra=f'n_test={x["n_test"]}',
                                  modelo=x["modelo"], rmse=x["rmse"], rmse_ar4=ar4,
                                  p_dm_vs_ar4=None if x["modelo"] == "ar4" else x["p_ajustado_vs_ar4"],
                                  metodo_p="BH (DM-HLN)", fuente=rel(f)))
    return pd.DataFrame(filas)


# ----------------------------------------------------------------------------------------- criterio de destacado
def seleccion_b(coef, oos):
    """(b): mejor de cada familia por mercado (y periodo cuando el modulo lo desagrega) segun RMSE fuera de muestra.
    El OOS de M0 y M4 es de toda la muestra (no por periodo): la ecuacion por periodo de M0 se destaca como bloque.
    Familias sin OOS (M1, M3, M5, M8, M9-DML, M0 ampliada) no son elegibles: se declara en el informe."""
    sel = []

    def reg(modelo_ids, oos_row, familia, nota):
        for mid in modelo_ids:
            sel.append(dict(modelo_id=mid, oos_ref=f'{oos_row["modulo"]}:{oos_row["modelo"]}', rmse_oos=oos_row["rmse"],
                            rmse_ar4_oos=oos_row["rmse_ar4"], criterio=f"(b) mejor de la familia {familia}: {nota}"))
    for mer in ("compra", "alquiler"):
        # M0: unico candidato OOS de la familia ols_tramos_hac (AR1+X por periodo)
        o = oos[(oos.modulo == "M0") & (oos.mercado == mer) & (oos.modelo == "AR1+X_por_periodo")].iloc[0]
        ids = sorted(coef[(coef.modulo == "M0") & (coef.mercado == mer) & (coef.familia_modelo == "ols_tramos_hac")
                          & coef.modelo_id.str.contains("_base_")].modelo_id.unique())
        reg(ids, o, "ols_tramos_hac", "ecuacion AR1+X por periodo; unico candidato con OOS en la familia")
        # M4: mejor spec (sin rupturas) por min(SR, ECM); mismas especificaciones para dols/fmols/ardl
        o4 = oos[(oos.modulo == "M4") & (oos.mercado == mer) & oos.modelo.str.endswith(("_SR", "_ECM"))].copy()
        o4 = o4.sort_values(["rmse", "modelo"]).iloc[0]
        spec, rup = o4["modelo"].split("_")[0], "sin_rupturas"
        ids = sorted(coef[(coef.modulo == "M4") & (coef.mercado == mer) & (coef.spec == spec)
                          & (coef.rupturas == rup)].modelo_id.unique())
        reg(ids, o4, "dols/fmols/ardl", f"especificacion {spec} de menor RMSE ({o4['modelo'].split('_')[-1]}); el OOS "
                                         "se hace con beta OLS estatico y es comun a los tres estimadores")
        # M6: ols_factores (unico modelo de la familia con coeficientes y OOS), muestra completa trimestral
        o6 = oos[(oos.modulo == "M6") & (oos.mercado == mer) & (oos.modelo == "ols_factores")].iloc[0]
        reg([f"M6_ols_{mer}_trimestral_completo"], o6, "ols_familias", "ols_factores trimestral, periodo completo")
    return pd.DataFrame(sel)


def construir_destacados(coef, m7, r0, oos):
    sel = seleccion_b(coef, oos)
    filas = []
    m7v = m7[m7.variable != "TODAS"].set_index(["mercado", "periodo", "variable"])
    r0i = r0.set_index(["mercado", "periodo", "variable"])
    for _, s in sel.iterrows():
        d = coef[coef.modelo_id == s["modelo_id"]].copy()
        for i, x in d.iterrows():
            v = x["variable"]
            k = (x["mercado"], x["periodo"], norm_var(v))
            # regla §8
            if vacio(x["cumple_regla_m0"]):
                kk = (x["mercado"], x["periodo"], "d4_" + norm_var(v))
                d.loc[i, "cumple_regla_m0"] = r0i.loc[kk, "cumple"] if kk in r0i.index else "no_evaluable"
            # multiverso: el del propio modulo si lo trae (M6); si no, M7 orientado a nivel de variable
            if vacio(x["cumple_multiverso"]):
                if k in m7v.index:
                    m = m7v.loc[k]
                    d.loc[i, ["n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_multiverso"]] = [
                        m["n_multiverso"], m["pct_mismo_signo"], m["pct_sig_bh"], bool(m["cumple_multiverso"])]
                else:
                    d.loc[i, "cumple_multiverso"] = "no_evaluable"
        d["cumple_ambas"] = (d["cumple_regla_m0"].astype(str) == "si") & (d["cumple_multiverso"].astype(str) == "True")
        d["criterio_destacado"] = s["criterio"]
        d["oos_ref"] = s["oos_ref"]
        d["rmse_oos"] = s["rmse_oos"]
        d["rmse_ar4_oos"] = s["rmse_ar4_oos"]
        d["ratio_rmse_vs_ar4"] = s["rmse_oos"] / s["rmse_ar4_oos"]
        d["destacado"] = "si"
        filas.append(d)
    D = pd.concat(filas, ignore_index=True)
    # la fila (a) -- ambas reglas por variable -- marca el modelo como (a)+(b)
    amb = D.groupby("modelo_id")["cumple_ambas"].transform("any")
    D["no_cumple_regla"] = np.where(D["cumple_ambas"], "no", "si")
    D["motivo_destacado"] = np.where(
        amb, "(a) cumple regla §8 y multiverso en al menos una variable; " + D["criterio_destacado"],
        D["criterio_destacado"] + "; NO CUMPLE LA REGLA (§8 y multiverso) en ninguna variable; RMSE "
        + D["rmse_oos"].map(lambda v: f"{v:.3f}") + " vs AR(4) " + D["rmse_ar4_oos"].map(lambda v: f"{v:.3f}")
        + np.where(D["rmse_oos"] > D["rmse_ar4_oos"], " (peor que AR(4))", " (no peor que AR(4))"))
    D["fuente"] = D["fuente"]
    return D


def parciales(coef, m7, r0):
    """Variables que cumplen UNA sola de las dos reglas (informativo; no son destacados)."""
    r0i = r0.set_index(["mercado", "periodo", "variable"])
    sal = []
    for _, x in r0[r0.cumple == "si"].iterrows():
        k = (x["mercado"], x["periodo"], norm_var(x["variable"]))
        m = m7[(m7.mercado == k[0]) & (m7.periodo == k[1]) & (m7.variable == k[2])]
        sal.append(dict(regla="solo §8", mercado=k[0], periodo=k[1], variable=k[2],
                        cumple_regla_m0="si", cumple_multiverso=sino(m["cumple_multiverso"].iloc[0]) if len(m) else "—",
                        pct_mismo_signo=m["pct_mismo_signo"].iloc[0] if len(m) else np.nan,
                        pct_sig_bh=m["pct_sig_bh"].iloc[0] if len(m) else np.nan))
    for _, x in m7[(m7.variable != "TODAS") & (m7.cumple_multiverso == True)].iterrows():  # noqa: E712
        kk = (x["mercado"], x["periodo"], "d4_" + x["variable"])
        c0 = r0i.loc[kk, "cumple"] if kk in r0i.index else "no_evaluable"
        sal.append(dict(regla="solo multiverso", mercado=x["mercado"], periodo=x["periodo"], variable=x["variable"],
                        cumple_regla_m0=c0, cumple_multiverso="sí", pct_mismo_signo=x["pct_mismo_signo"],
                        pct_sig_bh=x["pct_sig_bh"]))
    return pd.DataFrame(sal)


# ----------------------------------------------------------------------------------------- hipotesis
def tabla_hipotesis():
    f2, f5, f1 = OUT / "M2" / "hipotesis_m2.csv", OUT / "M5" / "hipotesis_m5.csv", OUT / "M1" / "hipotesis_m1.csv"
    h2 = pd.read_csv(f2)
    h2 = h2[h2["principal"].astype(str) == "si"] if "principal" in h2 else h2
    h5, h1 = pd.read_csv(f5), pd.read_csv(f1)
    filas = []
    for _, x in h2.iterrows():
        est = (f'contribucion acumulada {x["contribucion_pp"]:.2f} pp (mediana {x["mediana"]:.2f}; banda 68 % '
               f'[{x["b68_lo"]:.2f}; {x["b68_hi"]:.2f}]); P(signo esperado) = {x["prob_posterior"]:.3f}')
        filas.append(dict(id=x["id"], hipotesis=x["hipotesis"], estimacion=est, p=x["p_unilateral"],
                          p_holm=x["p_holm"], metodo_ajuste="Holm", capa=x["capa"],
                          decision=("respaldada tras Holm" if bool(x["rechaza_H0_alfa05"]) else "no respaldada tras Holm")
                          + " (C3s: condicionada a las restricciones de signo)", fuente=rel(f2)))
    for _, x in h5.iterrows():
        est = (f'beta descriptivo (cociente) {x["beta_descriptivo"]:.2f} (no es evidencia); F efectivo {x["F_efectivo"]:.2f}; '
               f'IC AR95 [{x["ar_lo"]}; {x["ar_hi"]}]; signo forma reducida {x["signo_forma_reducida"]} '
               f'(esperado {x["signo_esperado_forma_reducida"]})')
        filas.append(dict(id=x["id"], hipotesis=x["hipotesis"], estimacion=est, p=x["ar_p"], p_holm=x["p_holm"],
                          metodo_ajuste="Holm", capa=x["capa"],
                          decision=("respaldada tras Holm" if bool(x["rechaza_H0_alfa05"]) else "no respaldada tras Holm")
                          + "; " + str(x["lectura"]), fuente=rel(f5)))
    for _, x in h1.iterrows():
        filas.append(dict(id=x["id"], hipotesis=x["hipotesis"], estimacion=str(x["estimacion"]), p=x["p"],
                          p_holm=x["p_holm"], metodo_ajuste="Holm", capa=x["capa"],
                          decision=("respaldada tras Holm" if bool(x["rechaza_H0_alfa05"]) else "no respaldada tras Holm")
                          + " (C4: asociacion, sin lectura causal)", fuente=rel(f1)))
    H = pd.DataFrame(filas)
    H["_o"] = H["id"].str.extract(r"H8-(\d+)")[0].astype(int)
    return H.sort_values("_o").drop(columns="_o").reset_index(drop=True)


# ----------------------------------------------------------------------------------------- markdown
NOTA_PIE = (
    "Notas. Estrellas basadas en el p AJUSTADO (BH o Holm, segun la columna «método»): * < 0,10; ** < 0,05; "
    "*** < 0,01; sin estrella si no se alcanza o no hay p ajustado. El tipo de error estandar (EE) se indica en cada "
    "fila (HAC-NW, EWC, delta, etc.). β std. = coeficiente estandarizado; elasticidad solo cuando el modulo la define. "
    "La capa de todos los modelos de esta tabla es C4 (asociacion): sin lenguaje causal. Los modelos destacados por "
    "el criterio (b) se eligen por su error fuera de muestra, nunca por su p, y se marcan «NO CUMPLE LA REGLA» si no "
    "cumplen la regla de §8 y la del multiverso. Un RMSE mayor que el de AR(4) indica que el modelo no predice mejor "
    "que esa linea base. Valores «—» = no aplica.")


def tabla_modelo(D):
    x0 = D.iloc[0]
    L = []
    cab = ("| variable | β (EE) | tipo EE | p | p aj. (método) | IC95 | β std. | elasticidad | regla §8 | "
           "multiverso (n; % signo; % sig. BH; cumple) |")
    L += [cab, "|" + "---|" * 10]
    for _, x in D.iterrows():
        mv = (f'{fmt(x["n_multiverso"], 0)}; {fmt(x["pct_mismo_signo"], 2)}; {fmt(x["pct_sig_bh"], 2)}; '
              f'{sino(x["cumple_multiverso"])}')
        L.append(f'| {x["variable"]} | {fmt(x["beta"])}{estrellas(x["p_ajustado"])} ({fmt(x["ee"])}) | '
                 f'{fmt(x["tipo_ee"])} | {fmt(x["p"], 4)} | {fmt(x["p_ajustado"], 4)} ({fmt(x["metodo_ajuste"])}) | '
                 f'[{fmt(x["ic95_lo"])}; {fmt(x["ic95_hi"])}] | {fmt(x["beta_std"])} | {fmt(x["elasticidad"])} | '
                 f'{sino(x["cumple_regla_m0"])} | {mv} |')
    L.append("")
    pie = [
        ("N", fmt(x0["n"], 0)), ("periodo / ámbito", f'{x0["periodo"]} / {x0["ambito"]}'),
        ("R² / R² ajustado", f'{fmt(x0["r2"])} / {fmt(x0["r2_adj"])}'),
        ("AIC / BIC", f'{fmt(x0["aic"], 2)} / {fmt(x0["bic"], 2)}'),
        ("velocidad de ajuste / semivida (trim.)", f'{fmt(x0["vel_ajuste"])} / {fmt(x0["semivida"], 1)}'),
        ("diagnósticos (p): BG / BP / JB / RESET",
         f'{fmt(x0["bg_p"], 4)} / {fmt(x0["bp_p"], 4)} / {fmt(x0["jb_p"], 4)} / {fmt(x0["reset_p"], 4)}'),
        ("CUSUM estable / VIF máx.", f'{sino(x0["cusum_estable"])} / {fmt(x0["vif_max"], 2)}'),
        ("cointegración (p)", fmt(x0["coint_p"], 4)),
        ("IV: F de primera etapa / intervalo AR95", f'{fmt(x0["f1_etapa"])} / [{fmt(x0["ar_lo"])}; {fmt(x0["ar_hi"])}]'),
        ("capa", fmt(x0["capa"])),
        ("fuera de muestra: RMSE (modelo) vs AR(4)",
         f'{fmt(x0["rmse_oos"])} vs {fmt(x0["rmse_ar4_oos"])} (ratio {fmt(x0["ratio_rmse_vs_ar4"], 2)}; {x0["oos_ref"]})'),
        ("cumple regla M0 (§8) / cumple multiverso",
         "por variable (columnas de la tabla); modelo con alguna variable que cumple ambas: "
         + ("sí" if D["cumple_ambas"].any() else "no")),
        ("motivo destacado", x0["motivo_destacado"]),
        ("medida de precio", fmt(x0["medida_precio"])), ("transformación", fmt(x0["transformacion"])),
        ("dependiente", fmt(x0["dependiente"])), ("script", fmt(x0["script"])), ("fuente", fmt(x0["fuente"]))]
    L += ["| concepto | valor |", "|---|---|"] + [f"| {a} | {b} |" for a, b in pie] + [""]
    return L


def md_tabla(df, cols, dec=4):
    L = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, x in df.iterrows():
        L.append("| " + " | ".join(fmt(x[c], dec) if not isinstance(x[c], str) else x[c] for c in cols) + " |")
    return L


def escribir_md(D, P, H, V, F, ruta, r0cumple_eval):
    modelos = D.drop_duplicates("modelo_id")
    L = ["# Tablas de modelos destacados V8 (F6)", "",
         "Generado por `src/v8/f6_tablas.py` solo a partir de salidas versionadas (output/v8/M0-M9 y F5). No se estima "
         "nada nuevo. Capa: C4 (asociación) para todos los modelos de coeficientes; C3s solo en H8-1…H8-4 "
         "(condicionada a las restricciones de signo). Sin lenguaje causal fuera de esas capas.", "",
         "## 1. Criterio y resultado", "",
         "Criterio de §9 del pre-registro:", "",
         "- **(a)** modelos que cumplen la regla de §8 (efecto por periodo, `cumple_regla_m0`) Y la del multiverso "
         "(signo estable ≥ 80 % y significativo tras BH ≥ 50 % en las especificaciones de la variable; M7 orientado).",
         "- **(b)** además, el mejor de cada familia por mercado y periodo según el error fuera de muestra en bloques "
         "con embargo, nunca por su p, marcado «NO CUMPLE LA REGLA» si es el caso.", "",
         f"**Resultado (a): {int(D.groupby('modelo_id')['cumple_ambas'].any().sum())} modelos cumplen ambas reglas.** "
         f"Pocos (es lo esperable): la regla de §8 la cumplen {int((P.regla == 'solo §8').sum())} variables de las "
         f"{int(r0cumple_eval)} evaluables y ninguna cumple el multiverso orientado; las {int((P.regla == 'solo multiverso').sum())} "
         "variables que cumplen el multiverso no cumplen o no pueden evaluar §8. Se listan como parciales, sin ser destacados:", ""]
    L += md_tabla(P, ["regla", "mercado", "periodo", "variable", "cumple_regla_m0", "cumple_multiverso",
                      "pct_mismo_signo", "pct_sig_bh"], 3) + [""]
    n_mejor = int((modelos["ratio_rmse_vs_ar4"] <= 1).sum())
    L += [f"**Resultado (b): {len(modelos)} modelos destacados** (todos «NO CUMPLE LA REGLA» salvo indicación). "
          "Ámbito de la elección: el error fuera de muestra solo existe, por módulo, a nivel de mercado "
          "(M0, M4) o de mercado y muestra completa (M6); no hay OOS por periodo para esos modelos, de modo que la "
          "ecuación por periodo de M0 se destaca como bloque. Familias sin error fuera de muestra y por tanto no "
          "elegibles: M1 (factor común), M3 (regímenes), M5 (LP-IV), M8 (regional), M9-DML (el OOS de M9 es de los "
          "modelos predictivos LightGBM/GAM, que no tienen coeficientes) y M0 ampliada. Comparación con AR(4): "
          f"{n_mejor} de {len(modelos)} tienen RMSE menor o igual que AR(4) en su "
          "módulo (razón RMSE en la fila «fuera de muestra» de cada tabla; sin ajuste de multiplicidad aquí: los p "
          "DM-HLN ajustados están en la hoja Fuera_muestra).", ""]
    L += ["## 2. Modelos destacados por mercado y periodo", ""]
    for (mer, per), g in sorted(modelos.groupby(["mercado", "periodo"]), key=lambda t: t[0]):
        L += [f"### {mer} · {per}", ""]
        for mid in g["modelo_id"]:
            d = D[D.modelo_id == mid]
            L += [f"**{mid}** ({d.iloc[0]['familia_modelo']}; módulo {d.iloc[0]['modulo']})", ""]
            L += tabla_modelo(d)
    L += [NOTA_PIE, "", "## 3. Hipótesis H8-1…H8-9 (§7)", ""]
    L += md_tabla(H.assign(p=H["p"], p_holm=H["p_holm"]), ["id", "hipotesis", "estimacion", "p", "p_holm", "capa",
                                                          "decision"], 4)
    L += ["", "p: unilateral (H8-1…H8-4, posterior), Anderson-Rubin con signo a priori (H8-5…H8-7) y bootstrap "
          "(H8-8, H8-9). Holm dentro de cada familia ({H8-1…H8-4}, {H8-5…H8-7}, {H8-8, H8-9}). Ninguna hipótesis de "
          "SVAR ni de instrumentos se respalda; H8-9 (C4) es una asociación sin lectura causal.", "",
          "## 4. Votos de la regla de §9 (F5)", ""]
    cols = ["mercado", "periodo", "voto_svar_hd", "voto_dominancia", "voto_lpiv", "voto_contabilidad",
            "factor_evaluado", "n_votos", "cond1", "cond2", "cond3", "resultado"]
    Vm = V.copy()
    for c in ("cond1", "cond2", "cond3"):
        Vm[c] = Vm[c].map(sino)
    for c in ("voto_dominancia", "voto_lpiv", "voto_contabilidad"):
        Vm[c] = Vm[c].fillna("abstiene")
    L += md_tabla(Vm, cols, 0)
    L += ["", f"Celdas designadas: {int((V['resultado'] == 'designado').sum())} de {len(V)}. "
          "svar_hd es C3s (condicionada a los supuestos de signo); dominancia, LP-IV y contabilidad son C4.", "",
          "## 5. Tabla común fuera de muestra (F5; RMSE en pp de crecimiento trimestral real)", ""]
    L += md_tabla(F, ["mercado", "modelo", "rmse_pp", "evaluable", "p_holm_vs_ar4", "p_holm_vs_exigente",
                      "mejor_que_exigente"], 4)
    L += ["", "Prueba 2016T2-2026T1, 5 bloques con embargo de 4 trimestres; DM con corrección HLN y Holm. Ningún modelo "
          "supera a la base más exigente.", ""]
    ruta.write_text("\n".join(L), encoding="utf-8")


# ----------------------------------------------------------------------------------------- excel
class Hoja:
    def __init__(self, wb, nombre):
        self.ws = wb.create_sheet(nombre)
        self.ws.freeze_panes = None
        self.fila = 1

    def cab(self, cols):
        for j, c in enumerate(cols, 1):
            self.ws.cell(self.fila, j, c).font = Font(bold=True)
        self.fila += 1

    def put(self, j, valor, color=AZUL, fila=None):
        if isinstance(valor, (np.bool_, bool)):
            valor = "sí" if valor else "no"
        elif isinstance(valor, np.integer):
            valor = int(valor)
        elif isinstance(valor, np.floating):
            valor = None if np.isnan(valor) else float(valor)
        elif isinstance(valor, float) and np.isnan(valor):
            valor = None
        c = self.ws.cell(fila or self.fila, j, valor)
        c.font = Font(color=color)
        return c

    def anchos(self, minimo=8, maximo=45):
        w = {}
        for row in self.ws.iter_rows():
            for c in row:
                if c.value is not None:
                    s = str(c.value)
                    w[c.column] = max(w.get(c.column, 0), min(len(s), 60) if not s.startswith("=") else 14)
        for j, n in w.items():
            self.ws.column_dimensions[get_column_letter(j)].width = max(minimo, min(maximo, n + 2))


def df_a_hoja(h, df, cols, color=AZUL):
    h.cab(cols)
    for _, x in df.iterrows():
        for j, c in enumerate(cols, 1):
            h.put(j, x[c], color)
        h.fila += 1


def fijar_zip(ruta):
    """Reescribe el zip con fechas y orden fijos para que dos ejecuciones den el mismo sha256."""
    with zipfile.ZipFile(ruta) as z:
        datos = [(n, z.read(n)) for n in sorted(z.namelist())]
    fijo = FECHA_FIJA.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    datos = [(n, re.sub(rb"(<dcterms:(?:modified|created)[^>]*>)[^<]*", rb"\g<1>" + fijo, b)
              if n == "docProps/core.xml" else b) for n, b in datos]
    tmp = Path(str(ruta) + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in datos:
            zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, b)
    tmp.replace(ruta)


def escribir_xlsx(D, H, V, F, A, R, REG, M7, O, ruta):
    wb = Workbook()
    wb.remove(wb.active)
    wb.properties.creator = "Econometr-a V8 (src/v8/f6_tablas.py)"
    wb.properties.lastModifiedBy = None
    wb.properties.created = FECHA_FIJA
    wb.properties.modified = FECHA_FIJA
    wb.properties.title = "Tablas V8"

    # --- Leeme
    hl = Hoja(wb, "Leeme")
    lineas = [
        ("Tablas V8 (F6). Generado por src/v8/f6_tablas.py a partir de salidas versionadas; no estima nada.", None),
        ("Capas: C3s (svar_hd, H8-1…H8-4) condicionada a las restricciones de signo; C4 (asociación) el resto: sin lectura causal.", None),
        ("Fuentes: output/v8/M0…M9 (coeficientes.csv, hipotesis_*.csv, resumen_multiverso.csv, fuera_muestra*), output/v8/F5 (regla_s9, ranking, atribucion_combinada, regional_ranking, fuera_muestra_comun).", None),
        ("Convenciones de color:", None),
        ("AZUL (0000FF): entrada tomada de un fichero de datos o salida; la columna «fuente» da la ruta del fichero.", AZUL),
        ("NEGRO (000000): cálculo hecho en la hoja con fórmula de Excel (=SUM, =COUNTIF, =SUMIFS, cocientes).", NEGRO),
        ("VERDE (008000): vínculo a otra hoja del libro (=Hoja!A1).", VERDE),
        ("Sin paneles inmovilizados. Estrellas (si las hay) basadas en el p AJUSTADO. Modelos destacados: véase tablas_modelos_destacados.md.", None),
        ("Hojas: Destacados, Hipotesis, Votos_s9, Atribucion, Ranking, Fuera_muestra, Regional, Multiverso.", None)]
    for i, (t, col) in enumerate(lineas, 1):
        c = hl.ws.cell(i, 1, t)
        c.font = Font(bold=(i == 1), color=col or NEGRO)
    hl.ws.column_dimensions["A"].width = 120
    # resumen enlazado (se rellena tras crear las demas hojas)

    # --- Fuera_muestra (antes de Destacados para conocer filas); orden de hojas se fija despues
    hf = Hoja(wb, "Fuera_muestra")
    colsF = ["mercado", "modelo", "tipo", "rmse_pp", "n_test", "evaluable", "mejor_que_exigente", "p_holm_vs_ar4",
             "p_holm_vs_exigente", "fuente"]
    colsF_xl = colsF[:-1] + ["fuente", "ratio_rmse_vs_ar4_calc"]
    hf.cab(colsF_xl)
    fila_ar4 = {}
    inicio = hf.fila
    for _, x in F.iterrows():
        if x["modelo"] == "ar4":
            fila_ar4[x["mercado"]] = hf.fila
        hf.fila += 1
    hf.fila = inicio
    for _, x in F.iterrows():
        for j, c in enumerate(colsF, 1):
            hf.put(j, x[c] if c != "fuente" else "output/v8/F5/fuera_muestra_comun.csv", AZUL)
        hf.put(len(colsF) + 1, f"=D{hf.fila}/D{fila_ar4[x['mercado']]}", NEGRO)
        hf.fila += 1
    hf.fila += 2
    hf.ws.cell(hf.fila, 1, "Error fuera de muestra por módulo (bloques con embargo; muestras propias de cada módulo)").font = Font(bold=True)
    hf.fila += 1
    colsO = ["modulo", "mercado", "ambito", "muestra", "modelo", "rmse", "rmse_ar4", "p_dm_vs_ar4", "metodo_p",
             "fuente"]
    hf.cab(colsO + ["ratio_rmse_vs_ar4_calc"])
    filaO = {}
    for _, x in O.iterrows():
        for j, c in enumerate(colsO, 1):
            hf.put(j, x[c], AZUL)
        hf.put(len(colsO) + 1, f"=F{hf.fila}/G{hf.fila}", NEGRO)
        filaO[(x["modulo"], x["mercado"], x["ambito"], x["modelo"], x["muestra"])] = hf.fila
        hf.fila += 1
    hf.anchos()

    # --- Destacados
    hd = Hoja(wb, "Destacados")
    colsD = COLS_CONTRATO + ["criterio_destacado", "oos_ref", "no_cumple_regla", "fuente"]
    hd.cab(colsD + ["rmse_oos (vínculo)", "rmse_ar4_oos (vínculo)", "ratio_rmse_vs_ar4_calc"])
    Dx = D.copy()
    Dx["destacado"] = "si"
    for _, x in Dx.iterrows():
        for j, c in enumerate(colsD, 1):
            hd.put(j, x[c], AZUL)
        mod, ref = x["oos_ref"].split(":", 1)
        cand = [v for k, v in filaO.items() if k[0] == mod and k[1] == x["mercado"] and k[3] == _oos_modelo(ref, mod)]
        r = cand[0] if cand else None
        n = len(colsD)
        if r:
            hd.put(n + 1, f"=Fuera_muestra!F{r}", VERDE)
            hd.put(n + 2, f"=Fuera_muestra!G{r}", VERDE)
            hd.put(n + 3, f"={get_column_letter(n + 1)}{hd.fila}/{get_column_letter(n + 2)}{hd.fila}", NEGRO)
        hd.fila += 1
    hd.anchos()

    # --- Hipotesis
    hh = Hoja(wb, "Hipotesis")
    colsH = ["id", "hipotesis", "estimacion", "p", "p_holm", "metodo_ajuste", "capa", "decision", "fuente"]
    hh.cab(colsH + ["rechaza_H0_calc (p_holm < 0,05)"])
    for _, x in H.iterrows():
        for j, c in enumerate(colsH, 1):
            hh.put(j, x[c])
        hh.put(len(colsH) + 1, f'=IF(E{hh.fila}<0.05,"sí","no")', NEGRO)
        hh.fila += 1
    hh.anchos()

    # --- Votos_s9
    hv = Hoja(wb, "Votos_s9")
    colsV = ["mercado", "periodo", "voto_svar_hd", "voto_dominancia", "voto_lpiv", "voto_contabilidad",
             "factor_evaluado", "n_votos", "cond1", "cond2", "cond3", "resultado", "capa", "fuente"]
    hv.cab(colsV + ["votos_factor_calc (COUNTIF)", "cond1_calc (>=3)"])
    Vx = V.copy()
    for c in ("cond1", "cond2", "cond3"):
        Vx[c] = Vx[c].map(sino)
    for c in ("voto_dominancia", "voto_lpiv", "voto_contabilidad"):
        Vx[c] = Vx[c].fillna("abstiene")
    f0 = hv.fila
    fila_v = {}
    for _, x in Vx.iterrows():
        for j, c in enumerate(colsV, 1):
            hv.put(j, x[c] if c != "fuente" else "output/v8/F5/regla_s9.csv")
        n = len(colsV)
        hv.put(n + 1, f"=COUNTIF(C{hv.fila}:F{hv.fila},G{hv.fila})", NEGRO)
        hv.put(n + 2, f'=IF({get_column_letter(n + 1)}{hv.fila}>=3,"sí","no")', NEGRO)
        fila_v[(x["mercado"], x["periodo"])] = hv.fila
        hv.fila += 1
    hv.fila += 1
    hv.ws.cell(hv.fila, 1, "Celdas designadas (calc.)").font = Font(bold=True)
    hv.put(2, f'=COUNTIF(L{f0}:L{f0 + len(Vx) - 1},"designado")', NEGRO)
    hv.fila += 1
    hv.ws.cell(hv.fila, 1, "Celdas con condición 1 (calc.)").font = Font(bold=True)
    hv.put(2, f'=COUNTIF({get_column_letter(len(colsV) + 2)}{f0}:{get_column_letter(len(colsV) + 2)}{f0 + len(Vx) - 1},"sí")', NEGRO)
    hv.anchos()
    fila_designadas = f0 + len(Vx) + 1

    # --- Atribucion
    ha = Hoja(wb, "Atribucion")
    colsA = ["mercado", "ambito", "periodo", "factor", "metodo", "contribucion_pp", "media", "mediana", "pct_signo",
             "b68_lo", "b68_hi", "b90_lo", "b90_hi", "capa", "compite", "vota", "variante", "delta_y_metodo_pp",
             "notas", "fuente"]
    ha.cab(colsA + ["pct_total_calc (contribución / ΔY)", "suma_contribuciones_celda_calc (SUMIFS)"])
    n0 = ha.fila
    n1 = n0 + len(A) - 1
    for _, x in A.iterrows():
        for j, c in enumerate(colsA, 1):
            ha.put(j, x[c] if c != "fuente" else "output/v8/F5/atribucion_combinada.csv")
        n = len(colsA)
        ha.put(n + 1, f'=IF(R{ha.fila}=0,"",F{ha.fila}/R{ha.fila})', NEGRO)
        ha.put(n + 2, f"=SUMIFS(F${n0}:F${n1},A${n0}:A${n1},A{ha.fila},C${n0}:C${n1},C{ha.fila},"
                      f"E${n0}:E${n1},E{ha.fila},Q${n0}:Q${n1},Q{ha.fila})", NEGRO)
        ha.fila += 1
    ha.anchos()

    # --- Ranking
    hr = Hoja(wb, "Ranking")
    colsR = list(R.columns) + ["fuente"]
    hr.cab(colsR + ["resultado_s9 (vínculo)"])
    R = R.assign(fuente="output/v8/F5/ranking.csv")
    for _, x in R.iterrows():
        for j, c in enumerate(colsR, 1):
            hr.put(j, x[c])
        hr.put(len(colsR) + 1, f"=Votos_s9!L{fila_v[(x['mercado'], x['periodo'])]}", VERDE)
        hr.fila += 1
    hr.anchos()

    # --- Regional
    hg = Hoja(wb, "Regional")
    REG = REG.assign(fuente="output/v8/F5/regional_ranking.csv")
    df_a_hoja(hg, REG, list(REG.columns))
    hg.anchos()

    # --- Multiverso
    hm = Hoja(wb, "Multiverso")
    colsM = ["mercado", "periodo", "factor", "variable", "n_multiverso", "pct_mismo_signo", "signo_mayoritario",
             "pct_sig_bh", "beta_std_mediana", "p05", "p95", "cumple_multiverso", "pct_interpoladas", "orientacion",
             "beta_orient_mediana", "variable_principal", "cumple_R3", "capa", "fuente"]
    M7x = M7.assign(fuente="output/v8/M7/resumen_multiverso.csv")
    df_a_hoja(hm, M7x, colsM)
    hm.anchos()

    # --- Leeme: vinculos
    k = len(lineas) + 2
    hl.ws.cell(k, 1, "Resumen enlazado (verde = vínculo a otra hoja)").font = Font(bold=True)
    hl.ws.cell(k + 1, 1, "Celdas designadas (hoja Votos_s9)")
    hl.ws.cell(k + 1, 2, f"=Votos_s9!B{fila_designadas}").font = Font(color=VERDE)
    hl.ws.cell(k + 2, 1, "Hipótesis tabuladas (hoja Hipotesis, filas)")
    hl.ws.cell(k + 2, 2, "=COUNTA(Hipotesis!A2:A200)").font = Font(color=NEGRO)
    hl.ws.column_dimensions["B"].width = 14

    wb._sheets = [wb[n] for n in ["Leeme", "Destacados", "Hipotesis", "Votos_s9", "Atribucion", "Ranking",
                                  "Fuera_muestra", "Regional", "Multiverso"]]
    wb.active = 0
    wb.save(ruta)
    fijar_zip(ruta)


def _oos_modelo(ref, mod):
    """Traduce oos_ref (p. ej. 'AR1+X_por_periodo' o 'C1_sin_rupturas_ECM') al nombre de modelo de la tabla OOS."""
    return ref


# ----------------------------------------------------------------------------------------- main
def main():
    SAL.mkdir(parents=True, exist_ok=True)
    coef = leer_coef()
    m7 = pd.read_csv(OUT / "M7" / "resumen_multiverso.csv")
    r0 = pd.read_csv(OUT / "M0" / "regla_m0.csv")
    oos = leer_oos()
    D = construir_destacados(coef, m7, r0, oos)
    P = parciales(coef, m7, r0)
    H = tabla_hipotesis()
    V = pd.read_csv(OUT / "F5" / "regla_s9.csv")
    F = pd.read_csv(OUT / "F5" / "fuera_muestra_comun.csv")
    F["rmse_pp"] = F["rmse_pp"] if "rmse_pp" in F else F["rmse_pp"]
    A = pd.read_csv(OUT / "F5" / "atribucion_combinada.csv")
    R = pd.read_csv(OUT / "F5" / "ranking.csv")
    REG = pd.read_csv(OUT / "F5" / "regional_ranking.csv")

    # md
    Fm = F.rename(columns={"rmse_pp": "rmse_pp"})
    escribir_md(D, P, H, V, Fm, OUT / "tablas_modelos_destacados.md", int((r0.cumple != "no_evaluable").sum()))
    # csv largo: columnas del contrato + modelo destacado
    cols = COLS_CONTRATO + COLS_EXTRA
    D[cols].to_csv(OUT / "tablas_modelos_destacados.csv", index=False, float_format="%.10g")
    # xlsx
    escribir_xlsx(D, H, V, F, A, R, REG, m7, oos, OUT / "tablas_v8.xlsx")
    # resultado.json
    nmod = int(D["modelo_id"].nunique())
    n_amb = int(D.groupby("modelo_id")["cumple_ambas"].any().sum())
    res = {
        "rama": "F6",
        "pregunta": "Que modelos se destacan segun §9 y como se presentan en formato de revista?",
        "capa": "C4 (asociacion) para los modelos de coeficientes; C3s solo H8-1..H8-4 (condicionada a las restricciones de signo)",
        "datos": "output/v8/M0-M9 y output/v8/F5 (solo lectura)",
        "N": {"modelos_destacados": nmod, "filas_csv": int(len(D)), "cumplen_a": n_amb},
        "metodo": "seleccion (a) regla §8 y multiverso; (b) mejor de cada familia por RMSE fuera de muestra (nunca por p)",
        "estimacion": {"cumplen_ambas_reglas": n_amb, "destacados_b": nmod},
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "C4: sin lenguaje causal",
        "diagnosticos": {"sha256_xlsx": sha256(OUT / "tablas_v8.xlsx"), "seed": SEED},
        "fuera_muestra": {"modelo": "ver tablas_modelos_destacados.md", "rmse": None, "dm_vs_ar4": None},
        "notas": "Ver el md: razones RMSE frente a AR(4) por modelo; ningun destacado cumple la regla (a).",
    }
    (SAL / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"destacados: {nmod} modelos ({len(D)} filas); cumplen (a): {n_amb}")


if __name__ == "__main__":
    sys.exit(main())
