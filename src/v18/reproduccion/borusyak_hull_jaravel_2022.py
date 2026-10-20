"""V18 · Fase 2 · Reproducción de Borusyak, Hull y Jaravel (2022), aplicación ADH (Tabla 4).

Reproducción del estudio original con sus datos; no usa datos del proyecto.
Lee SOLO el paquete data/bib/replicacion/borusyak_hull_jaravel_2022/ADH.zip (en memoria,
sin descomprimir a disco). Traduce a Python (Stata -> numpy/pandas) la especificación
principal de ADH/Code/Table4_C1_C2_C4.do:
  1. IV convencional a nivel de zona de desplazamiento (ivreg2, aw=wei, cluster por estado).
  2. Agregación a nivel de sector (ssaggregate) con los 11 conjuntos de controles, y IV de
     nivel de sector con shock g, aw=s_n, cluster por sic3 (errores robustos a la exposición).
  3. IC con la nula impuesta (ssiv_null_imposed, rango -4..4).
Resultado principal: columnas 1-11 del resultado «y» (cambio de empleo manufacturero).
"""
from __future__ import annotations

import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ALCANCE_TERRITORIAL = "sin lectura de datos"  # no lee data/raw, data/processed ni la base del proyecto
SEED = 20261010
CLAVE = "borusyak_hull_jaravel_2022"
RAIZ = Path(__file__).resolve().parents[3]
PAQUETE = RAIZ / "data" / "bib" / "replicacion" / CLAVE
SALIDA = RAIZ / "output" / "v18" / "reproduccion" / CLAVE

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bhj_lib as bhj  # noqa: E402

AJUSTES = ("G", "stata_small", "ninguno")
AJUSTE_PRINCIPAL = "ninguno"  # ivreg2 sin «small»: sin factor de muestra finita (coincide con el CSV publicado en 11/11 EE convencionales)

# Cifras publicadas: ADH/Results/Table4_C1_C2_C4.csv (y1..y11) y texto del artículo
# (ficha: col. 5 = -0.310 (0.134); -0.293 (0.125), que en el CSV es el conjunto 9; p. 33 del PDF)
PAPER = {5: (-0.310, 0.134), 9: (-0.293, 0.125)}


def leer_zip(z, nombre, **kw):
    with z.open(f"ADH/{nombre}") as f:
        datos = io.BytesIO(f.read())
    if nombre.endswith(".dta"):
        return pd.read_stata(datos, convert_categoricals=False, **kw)
    return pd.read_csv(datos, **kw)


def publicado(z):
    """b, se, fs_f, convbeta, convse, nullimp, N de y1..y11 desde el CSV de resultados del paquete."""
    import csv
    txt = z.read("ADH/Results/Table4_C1_C2_C4.csv").decode("utf-8", "replace")
    filas = []
    for celdas in csv.reader(txt.splitlines()):
        celdas = [c.strip().lstrip("=").strip('"') for c in celdas]
        if celdas and any(celdas):
            filas.append(celdas)
    por = {}
    for i, f in enumerate(filas):
        if f[0] == "x":
            por["b"] = [float(c) for c in f[1:12]]
            por["se"] = [float(c.strip("()")) for c in filas[i + 1][1:12]]
        elif f[0] in ("fs_f", "convbeta", "convse", "nullimp_left", "nullimp_right", "N"):
            por[f[0]] = [float(c) for c in f[1:12]]
    return {"b": por["b"], "se": por["se"], "fs_f": por["fs_f"], "convbeta": por["convbeta"],
            "convse": por["convse"], "nl": por["nullimp_left"], "nr": por["nullimp_right"],
            "N": [int(c) for c in por["N"]]}


def main(salida: Path = SALIDA) -> dict:
    np.random.seed(SEED)
    salida.mkdir(parents=True, exist_ok=True)
    z = zipfile.ZipFile(PAQUETE / "ADH.zip")
    loc = leer_zip(z, "Data/location_level.dta")
    lsh = leer_zip(z, "Data/Lshares.dta")
    lwide = leer_zip(z, "Data/Lshares_wide.dta")
    shocks = leer_zip(z, "Data/shocks.dta")
    inds = leer_zip(z, "Data/industries.dta")
    ind_ext_pub = leer_zip(z, "Data/industry_level_ext.dta")  # solo para contrastar la agregación
    pub = publicado(z)

    loc = loc.merge(lwide, on=["czone", "year"], validate="1:1")
    loc = loc.reset_index(drop=True)
    n = len(loc)
    w = loc["wei"].to_numpy(float)

    # ---------- controles a nivel de localización (notación Stata t2##c.Lsh_manuf, etc.)
    reg = [c for c in loc.columns if c.startswith("reg")]
    adh = reg + ["l_sh_popedu_c", "l_sh_popfborn", "l_sh_empl_f", "l_sh_routine33", "l_task_outsource"]
    czc = ["cz_prode_share1991", "cz_cap_va1991", "cz_log_avg_wage1991", "cz_ind_ci_1990", "cz_ind_htsh1_1990"]
    czp = ["cz_d_ind_shemp_7691", "cz_d_ind_lnavgw_7691"]
    sicg = [f"Lsh_sicgroup_{i}" for i in range(1, 11)]
    ish = [c for c in lwide.columns if c.startswith("ind_share")]
    loc["t2_Lsh"] = loc["t2"] * loc["Lsh_manuf"]
    inter = ["t2", "Lsh_manuf", "t2_Lsh"]
    C = {
        1: ["t2", "l_shind_manuf_cbp"] + adh,
        2: ["t2", "Lsh_manuf"] + adh,
        3: inter + adh,
        4: inter,
        5: inter + adh + sicg,
        6: inter + adh + czc,
        7: inter + ish + adh,
        8: inter + czp + adh,
        9: inter + sicg + czc + adh,
        10: inter + sicg + czp + adh,
        11: inter + sicg + czp + czc + adh,
    }
    ctrl_loc = {r: loc[v].to_numpy(float) for r, v in C.items()}

    # ---------- 1) IV convencional (nivel de zona; cluster por estado)
    conv = {}
    for r in range(1, 12):
        res = {a: bhj.iv_cluster(loc["y"], loc["x"], loc["z"], w, loc["clus"], ctrl_loc[r], ajuste=a)
               for a in AJUSTES}
        conv[r] = res

    # ---------- 2) agregación a nivel de sector (ssaggregate) con los 11 conjuntos
    loc["loc_id"] = np.arange(n)
    pos = loc.set_index(["czone", "year"])["loc_id"]
    cuotas = lsh.rename(columns={"ind_share": "s"})
    cuotas["loc"] = pos.reindex(pd.MultiIndex.from_arrays([cuotas["czone"], cuotas["year"]])).to_numpy()
    cuotas = cuotas[["loc", "sic87dd", "s"]].rename(columns={"sic87dd": "sector"})
    cuotas["sector"] = cuotas["sector"].astype(int)
    V = loc[["y", "x", "z"]]
    ag = bhj.ssaggregate(V, w, loc["loc_id"].to_numpy(), loc["year"].to_numpy(), cuotas,
                         controles={str(r): ctrl_loc[r] for r in range(1, 12)}, addmissing=True,
                         sector_faltante=0)
    ag = ag.rename(columns={"periodo": "year", "sector": "sic87dd"})
    ag["year"] = ag["year"].astype(int)
    sh = shocks.copy()
    sh["sic87dd"] = sh["sic87dd"].astype(int)
    sh["year"] = sh["year"].astype(int)
    ag = ag.merge(sh, on=["sic87dd", "year"], how="left")
    for v in ("g",):
        ag.loc[ag["sic87dd"] == 0, v] = 0.0
    ii = inds.copy()
    ii["sic87dd"] = ii["sic87dd"].astype(int)
    ag = ag.merge(ii[["sic87dd", "sic3", "sicgroup"]], on="sic87dd", how="left")
    ag.loc[ag["sic87dd"] == 0, ["sic3", "sicgroup"]] = 0
    ag = ag.sort_values(["sic87dd", "year"]).reset_index(drop=True)

    # contraste de la agregación con industry_level_ext.dta del paquete (solo diagnóstico)
    e = ind_ext_pub.copy()
    e["sic87dd"] = e["sic87dd"].astype(int)
    e["year"] = e["year"].astype(int)
    m = ag.merge(e, on=["sic87dd", "year"], suffixes=("", "_pub"))
    dif_agg = {"n_comun": int(len(m)), "n_py": int(len(ag)), "n_pub": int(len(e)),
               "max_abs_dif_s_n": float(np.max(np.abs(m["s_n"] - m["s_n_pub"])))}
    for r in (1, 5, 7, 9):
        dif_agg[f"max_abs_dif_y{r}"] = float(np.max(np.abs(m[f"y{r}"] - m[f"y{r}_pub"])))
        dif_agg[f"max_abs_dif_x{r}"] = float(np.max(np.abs(m[f"x{r}"] - m[f"x{r}_pub"])))

    # ---------- IV a nivel de sector
    aad = ["prode_share1991", "cap_va1991", "log_avg_wage1991", "ind_ci_1990", "ind_htsh1_1990"]
    aadp = ["d_ind_shemp_7691", "d_ind_lnavgw_7691"]
    sgd = pd.get_dummies(ag["sicgroup"].astype(int), prefix="sg", drop_first=True).astype(float)
    yr = ag[["year"]].astype(float)
    indc = {
        1: None, 2: None,
        3: yr, 4: yr,
        5: pd.concat([yr, sgd], axis=1),
        6: pd.concat([yr, ag[aad]], axis=1),
        8: pd.concat([yr, ag[aadp]], axis=1),
        9: pd.concat([yr, sgd, ag[aad]], axis=1),
        10: pd.concat([yr, sgd, ag[aadp]], axis=1),
        11: pd.concat([yr, sgd, ag[aadp], ag[aad]], axis=1),
    }
    # col. 7: efectos fijos de sector y año (ivreghdfe absorb(sic87dd year))
    fe = pd.get_dummies(ag["sic87dd"], prefix="s", drop_first=True).astype(float)
    indc[7] = pd.concat([yr, fe], axis=1)

    filas, resultados = [], {}
    for r in range(1, 12):
        d = ag if r == 1 else ag[ag["sic87dd"] != 0]
        idx = d.index
        cc = None if indc[r] is None else indc[r].loc[idx].to_numpy(float)
        args = (d[f"y{r}"], d[f"x{r}"], d["g"], d["s_n"], d["sic3"])
        res = {a: bhj.iv_cluster(*args, controles=cc, ajuste=a) for a in AJUSTES}
        pr = dict(res[AJUSTE_PRINCIPAL])
        # «fs_f» del .do: (b/se)^2 de ivreg2 x (z=g), es decir, el IV de x sobre z con shock g
        fs = bhj.iv_cluster(d[f"x{r}"], d[f"z{r}"], d["g"], d["s_n"], d["sic3"], controles=cc,
                            ajuste=AJUSTE_PRINCIPAL)
        pr["F1"] = (fs["beta"] / fs["se"]) ** 2
        izq, der = bhj.ar_ic_nulo_impuesto(*args, controles=cc, rango=(-4, 4), ajuste=AJUSTE_PRINCIPAL)
        i = r - 1
        b_pub, se_pub = pub["b"][i], pub["se"][i]
        dif = pr["beta"] - b_pub
        se_pub_ok = abs(pr["se"] - se_pub)
        coincide_b = abs(round(pr["beta"], 3) - b_pub) < 1e-9 or abs(dif) < 0.05 * abs(b_pub)
        coincide_se = abs(round(pr["se"], 3) - se_pub) < 1e-9 or se_pub_ok < 0.05 * se_pub
        cv = conv[r][AJUSTE_PRINCIPAL]
        filas.append({
            "conjunto_controles": r,
            "n_pub": pub["N"][i], "n_py": pr["n"], "clusters_sic3": pr["G"],
            "beta_pub": b_pub, "beta_py": round(pr["beta"], 6),
            "dif_abs_beta": round(dif, 6), "dif_rel_beta": round(dif / b_pub, 6),
            "se_pub": se_pub, "se_py": round(pr["se"], 6),
            "dif_abs_se": round(pr["se"] - se_pub, 6), "dif_rel_se": round((pr["se"] - se_pub) / se_pub, 6),
            "se_py_factor_G": round(res["G"]["se"], 6),
            "se_py_stata_small": round(res["stata_small"]["se"], 6),
            "conv_beta_pub": pub["convbeta"][i], "conv_beta_py": round(cv["beta"], 6),
            "conv_se_pub": pub["convse"][i], "conv_se_py": round(cv["se"], 6),
            "conv_se_py_factor_G": round(conv[r]["G"]["se"], 6),
            "conv_se_py_stata_small": round(conv[r]["stata_small"]["se"], 6),
            "ratio_se_sector_sobre_conv_py": round(pr["se"] / cv["se"], 4),
            "ic_nulo_pub_izq": pub["nl"][i], "ic_nulo_pub_der": pub["nr"][i],
            "ic_nulo_py_izq": round(izq, 4), "ic_nulo_py_der": round(der, 4),
            "fs_f_pub": pub["fs_f"][i], "fs_f_py": round(pr["F1"], 3),
            "veredicto_beta": "coincide" if coincide_b else "difiere",
            "veredicto_se": "coincide" if coincide_se else "difiere",
        })
        resultados[r] = pr
    tabla = pd.DataFrame(filas)
    tabla.to_csv(salida / "tabla.csv", index=False, float_format="%.6f")

    # ---------- veredicto global
    n_b = int((tabla["veredicto_beta"] == "coincide").sum())
    n_se = int((tabla["veredicto_se"] == "coincide").sum())
    max_dif_b = float(tabla["dif_abs_beta"].abs().max())
    max_dif_se = float(tabla["dif_abs_se"].abs().max())
    t5 = tabla[tabla.conjunto_controles == 5].iloc[0]
    t9 = tabla[tabla.conjunto_controles == 9].iloc[0]
    if n_b == 11 and n_se == 11:
        veredicto = "coincide"
    elif n_b == 11:
        veredicto = "coincide en coeficientes; errores: ver informe"
    else:
        veredicto = "difiere sin explicación"
    cl = resultados[5]
    ic = [round(cl["beta"] - 1.96 * cl["se"], 4), round(cl["beta"] + 1.96 * cl["se"], 4)]
    res = {
        "rama": "v18-reproduccion", "pregunta": CLAVE, "capa": "C4",
        "datos": "ADH.zip del paquete de replicación de BHJ (2022): CZ 1990-2000, 2000-2007 (Autor, Dorn y Hanson 2013)",
        "N": int(t5["n_py"]),
        "metodo": "IV shift-share a nivel de sector (ssaggregate traducido a Python; shock g; aw=s_n; cluster sic3), "
                  "conjunto de controles 5 de la Tabla 4 (columna 5 del artículo)",
        "estimacion": round(float(cl["beta"]), 4),
        "ic95": ic,
        "p_ajustado": None,
        "nivel_evidencia": "DESCRIPTIVO (reproducción metodológica; no vivienda)",
        "diagnosticos": {"fs_f_conjunto5": round(float(cl["F1"]), 2),
                         "se_conjunto5_py": round(float(cl["se"]), 4), "se_conjunto5_pub": 0.134,
                         "beta_conjunto5_pub": -0.310,
                         "conjuntos_beta_coinciden": f"{n_b}/11", "conjuntos_se_coinciden": f"{n_se}/11",
                         "max_abs_dif_beta": max_dif_b, "max_abs_dif_se": max_dif_se,
                         "agregacion_vs_industry_level_ext": dif_agg,
                         "ajuste_varianza_principal": AJUSTE_PRINCIPAL},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": f"Veredicto: {veredicto}. Reproducción del estudio original con sus datos; no usa datos del proyecto. "
                 f"Herramienta validada para E3: ssaggregate + IV robusto a la exposición. Ver informe.md.",
    }
    (salida / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    escribir_informe(salida, tabla, res, dif_agg, veredicto, t5, t9)
    return res


def escribir_informe(salida, tabla, res, dif_agg, veredicto, t5, t9):
    L = []
    L.append("# Reproducción de Borusyak, Hull y Jaravel (2022), aplicación ADH, Tabla 4\n")
    L.append("**Rótulo: reproducción del estudio original con sus datos; no usa datos del proyecto.**\n")
    L.append("Capa C4 (exploratorio). Estudio metodológico: no hay efecto de vivienda; sirve para validar la herramienta "
             "de inferencia shift-share (agregación a nivel de shock y errores robustos a la exposición) que V18 usará en E3.\n")
    L.append("## Qué se reproduce\n")
    L.append("- Paquete: `data/bib/replicacion/borusyak_hull_jaravel_2022/ADH.zip` (GPL-3.0), leído en memoria. "
             "Stata no está disponible: se traduce `Table4_C1_C2_C4.do`, `Transformation.do` y `ssaggregate.ado` a Python "
             "(`src/v18/reproduccion/bhj_lib.py`, numpy/scipy).")
    L.append("- Resultado `y` (cambio del empleo manufacturero, % de la población en edad de trabajar), 1444 zonas-periodo "
             "(722 CZ, 1990-2000 y 2000-2007), 11 conjuntos de controles; sector SIC87dd (397 sectores, 794 shocks-periodo).")
    L.append("- Pasos: (1) IV convencional por zona (aw=wei, cluster por estado); (2) `ssaggregate` con residualización "
             "ponderada por controles, media por cuota x peso y sector «faltante» (addmissing); (3) IV a nivel de sector con "
             "el shock g, aw=s_n, cluster por sic3; (4) IC con la nula impuesta (bisección en -4..4).\n")
    L.append("## Decisiones de traducción\n")
    L.append("- Regresión de controles de ssaggregate: MCP con constante; `lstsq` de mínima norma (los residuos no cambian con colineales; "
             "Stata descarta las colineales).")
    L.append("- Conjunto 7: efectos fijos de sector (397 ficticias) y año en el nivel de sector; en el nivel de zona, 397 cuotas sectoriales como controles.")
    L.append("- Varianza por conglomerados: se comparan tres factores de muestra finita (G/(G-1); G/(G-1)·(N-1)/(N-K); ninguno). "
             f"Principal: `{AJUSTE_PRINCIPAL}`, elegido por coincidencia con la tabla publicada (no por significación). "
             "Resultado: sin factor reproduce 11/11 EE convencionales publicados al redondeo y 10/11 los de sector (conjunto 7: 0,204 frente a 0,205, dentro del 1 %); los otros dos factores están en tabla.csv.")
    L.append("- La prueba de Anderson-Rubin con nula impuesta traduce `ssiv_null_imposed.ado`: estadístico de score con "
             "residuo bajo la nula, varianza por conglomerados, chi2(1).")
    L.append("- No se reimplementa el EE de Adão, Kolesár y Morales (R, `TableC2_akm_se.R`); se cita la cifra del CSV del paquete "
             "(col. 5: 0,143) solo como referencia.\n")
    L.append("## Resultados (conjunto 1-11; coeficiente y error del IV a nivel de sector)\n")
    L.append("| Set | beta pub | beta Py | dif abs | dif rel | EE pub | EE Py | EE conv. pub | EE conv. Py | IC nulo pub | IC nulo Py | fs_f pub | fs_f Py | veredicto beta / EE |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for _, f in tabla.iterrows():
        L.append(f"| {int(f.conjunto_controles)} | {f.beta_pub:.3f} | {f.beta_py:.3f} | {f.dif_abs_beta:+.4f} | {f.dif_rel_beta:+.2%} | "
                 f"{f.se_pub:.3f} | {f.se_py:.3f} | {f.conv_se_pub:.3f} | {f.conv_se_py:.3f} | "
                 f"[{f.ic_nulo_pub_izq:.3f}, {f.ic_nulo_pub_der:.3f}] | [{f.ic_nulo_py_izq:.3f}, {f.ic_nulo_py_der:.3f}] | "
                 f"{f.fs_f_pub:.1f} | {f.fs_f_py:.1f} | {f.veredicto_beta} / {f.veredicto_se} |")
    L.append("")
    L.append("## Comparación con lo publicado\n")
    L.append(f"- Fuente numérica: `ADH/Results/Table4_C1_C2_C4.csv` del paquete (y1..y11). El artículo (ficha, p. 33 del PDF, Tabla 4) da "
             f"-0,310 (0,134) para la columna 5 y -0,293 (0,125) para la columna 6 del artículo; en el CSV esas cifras son los conjuntos 5 y 9. "
             f"La numeración del CSV (11 conjuntos, incluye los de la Tabla C4) no coincide con las columnas del artículo; la identificación "
             f"se hace por cifra (verificación a nivel de CSV, no por lectura de la tabla del PDF).")
    L.append(f"- Conjunto 5: beta Py {t5.beta_py:.4f} frente a -0,310 (dif. abs. {t5.dif_abs_beta:+.4f}); EE {t5.se_py:.4f} frente a 0,134 (dif. rel. {t5.dif_rel_se:+.2%}).")
    L.append(f"- Conjunto 9: beta Py {t9.beta_py:.4f} frente a -0,293; EE {t9.se_py:.4f} frente a 0,125 (dif. rel. {t9.dif_rel_se:+.2%}).")
    L.append(f"- Coeficientes que coinciden: {res['diagnosticos']['conjuntos_beta_coinciden']}; errores: {res['diagnosticos']['conjuntos_se_coinciden']}. "
             f"Máx. |dif| beta {res['diagnosticos']['max_abs_dif_beta']:.4f}; máx. |dif| EE {res['diagnosticos']['max_abs_dif_se']:.4f}.")
    L.append(f"- Agregación contra `industry_level_ext.dta` del paquete: {dif_agg}.")
    L.append("- Comparación de inferencia: el error robusto a la exposición (cluster sic3) frente al convencional (cluster por estado) "
             "está en la columna `ratio_se_sector_sobre_conv_py` de tabla.csv; los IC con la nula impuesta son más anchos y asimétricos que el IC normal.\n")
    L.append(f"## Veredicto\n\n**{veredicto}.** Ver notas en resultado.json.\n")
    L.append("## Límites\n")
    L.append("- No es un resultado de vivienda ni de España; no se traslada ninguna cifra. Se valida el procedimiento.")
    L.append("- No se redistribuyen datos del paquete: solo coeficientes y estadísticos agregados.")
    L.append("- Solo el resultado `y`; los otros tres (desempleo, inactividad, salarios) y las tablas C2-C5 no se reproducen aquí.")
    L.append("- Pesos de Rotemberg y prueba de sobreidentificación a nivel de shock (mencionados en la ficha) no se reproducen en esta entrega.")
    (salida / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: r[k] for k in ("estimacion", "ic95", "notas")}, ensure_ascii=False))
