"""F7 - Síntesis. Lee SOLO tablas ya escritas en output/ (y docs/literatura.md, docs/limitaciones.md).

No estima modelos; solo agregados triviales (Holm/Bonferroni sobre p-valores ya calculados, IC normal
coef +- 1,96 EE donde la tabla de origen no lo trae, p aproximado por normal en la tabla de robustez).
Determinista, sin red, sin fechas de ejecución. Escribe:
  output/tablas/*.csv, output/registro_busqueda.csv, output/informe.md
Parámetros metodológicos (docs/decisiones.md): ALPHA, MAXLAGS.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
TAB = OUT / "tablas"
DOCS = ROOT / "docs"
TAB.mkdir(parents=True, exist_ok=True)

ALPHA = 0.05      # docs/decisiones.md (Generales)
MAXLAGS = 4       # docs/decisiones.md (Generales): HAC Newey-West
RATIO_MAG = 3.0   # regla de robustez: razón máxima de magnitudes (ver REGLA_ROBUSTEZ)
NAN = float("nan")


# ------------------------------------------------------------------ utilidades de formato
def rd(rel: str, **kw) -> pd.DataFrame:
    return pd.read_csv(OUT / rel, **kw)


def isn(x) -> bool:
    return x is None or (isinstance(x, float) and np.isnan(x)) or (not isinstance(x, str) and pd.isna(x))


def fm(x, nd: int = 3) -> str:
    if isn(x):
        return "n/d"
    return f"{float(x):.{nd}f}".replace(".", ",")


def fi(x) -> str:
    if isn(x):
        return "n/d"
    return f"{int(round(float(x))):,}".replace(",", ".")


def fp(p) -> str:
    if isn(p):
        return "n/d"
    p = float(p)
    if p < 0.001:
        return "<0,001"
    return fm(p, 3)


def ce(c, e, nd: int = 3) -> str:
    """coef (EE)"""
    return f"{fm(c, nd)} ({fm(e, nd)})"


def mdt(df: pd.DataFrame) -> str:
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("" if isn(v) else str(v) for v in r.values) + " |")
    return "\n" + "\n".join(lines) + "\n"


def save_csv(df: pd.DataFrame, name: str) -> Path:
    p = TAB / name
    df.to_csv(p, index=False, float_format="%.6g")
    return p


def holm(pv: list[float]) -> list[float]:
    """Holm-Bonferroni (ajustado, monótono) sobre una lista de p-valores."""
    m = len(pv)
    order = np.argsort(pv)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * pv[i])
        adj[i] = min(1.0, run)
    return list(adj)


def pnorm(coef, se, ref=0.0):
    if isn(coef) or isn(se) or se == 0:
        return NAN
    return float(2 * stats.norm.sf(abs((coef - ref) / se)))


# ------------------------------------------------------------------ carga
reg_parts = []
for n in range(2, 7):
    reg_parts.append(rd(f"registro_busqueda_f{n}.csv"))
REG = pd.concat(reg_parts, ignore_index=True)
REG["n_total_fase"] = REG.groupby("fase")["modelo_id"].transform("count")
REG["n_total_registro"] = len(REG)
save_reg = REG.copy()
save_reg.to_csv(OUT / "registro_busqueda.csv", index=False, float_format="%.10g")
N_TOTAL = len(REG)
POR_FASE = REG.groupby("fase").size()
K_CP_NOM = int(REG.modelo_id.str.startswith("busq_").sum())
K_CP_REAL = int(REG.modelo_id.str.startswith("real_busq_").sum())

ecr = rd("f2/ecuacion_real.csv")
n_ccaa = int(rd("f4/panel_ccaa.csv").CCAA.iloc[0])
_f5 = REG[REG.modelo_id == "A_FE_cl"].iloc[0]
N_F5 = int(_f5.n)
MUESTRA_F5 = f"{_f5.muestra_ini}-{_f5.muestra_fin}"
reg2 = REG[REG.fase == "F2"].set_index("modelo_id")
MUESTRA_LP = f"{reg2.loc['real_DOLS', 'muestra_ini']}-{reg2.loc['real_DOLS', 'muestra_fin']}"
MUESTRA_CP = f"{reg2.loc['real_preferido_refit', 'muestra_ini']}-{reg2.loc['real_preferido_refit', 'muestra_fin']}"
K_LP_REG = int(sum(i.startswith(("lr_", "rep_LR", "real_DOLS")) for i in reg2.index))   # especificaciones de largo plazo registradas

SRC = {}  # sección -> lista de archivos citados


# ======================================================================================
# (1) ECUACIÓN FINAL (precio real) + réplica nominal
# ======================================================================================
lp_nom = rd("f2/largo_plazo.csv")
lp_nom = lp_nom[lp_nom.metodo == "DOLS base (+q)"].set_index("var")
ecm_nom = rd("f2/ecm_preferido.csv").rename(columns={"Unnamed: 0": "termino"}).set_index("termino")
eba_nom = rd("f2/busqueda_eba.csv").set_index("termino")
eba_real = rd("f2/real_busqueda_eba.csv").set_index("termino")

LP_REAL = ecr[ecr.bloque.str.startswith("LR")].copy()
CP_REAL = ecr[ecr.bloque.str.startswith("CP")].copy()
SLOPES_LP = [t for t in LP_REAL.termino if t != "const"]
K_FAM_LP = 2 * len(SLOPES_LP)           # 4 pendientes x {nominal, real}
NOMMAP = {"tipo_hip_real": "tipo_hip", "ln_costes_real": "ln_costes"}
SLOPES_NOM = [NOMMAP.get(t, t) for t in SLOPES_LP]
p_family = [float(LP_REAL.set_index("termino").loc[t, "p"]) for t in SLOPES_LP] + \
           [float(lp_nom.loc[t, "p"]) for t in SLOPES_NOM]
holm_family = holm(p_family)
HOLM_LP = {("real", t): holm_family[i] for i, t in enumerate(SLOPES_LP)}
HOLM_LP.update({("nominal", t): holm_family[len(SLOPES_LP) + i] for i, t in enumerate(SLOPES_NOM)})


def tabla_final(df: pd.DataFrame, muestra: str, bloque_lp: bool) -> pd.DataFrame:
    o = df.copy()
    if bloque_lp:
        o["K"] = [K_FAM_LP if t != "const" else NAN for t in o.termino]
        o["p_bonf_K"] = [min(1.0, p * K_FAM_LP) if t != "const" else NAN for t, p in zip(o.termino, o.p)]
        o["p_holm_K"] = [HOLM_LP[("real", t)] if t != "const" else NAN for t in o.termino]
        o["regla_correccion"] = f"familia de {K_FAM_LP} pendientes de largo plazo (4 x nominal/real); NO cubre la elección de regresores"
    else:
        o["p_holm_K"] = NAN
        o["regla_correccion"] = "Bonferroni con K = nº de modelos de la búsqueda que contienen el término (f2/real_busqueda_eba.csv); sin K para intercepto y dummies"
    o["muestra"] = muestra
    o["precio"] = "real"
    o["EE_tipo"] = f"HAC Newey-West ({MAXLAGS} retardos)"
    return o[["termino", "coef", "EE_HAC", "IC95_inf", "IC95_sup", "p", "K", "p_bonf_K", "p_holm_K", "N", "muestra", "precio", "EE_tipo", "regla_correccion"]] \
        if "K" in o.columns else o


LP_T = tabla_final(LP_REAL.rename(columns={"K": "K"}), MUESTRA_LP, True)
CP_T = CP_REAL.copy()
CP_T["p_holm_K"] = NAN
CP_T["muestra"] = MUESTRA_CP
CP_T["precio"] = "real"
CP_T["EE_tipo"] = f"HAC Newey-West ({MAXLAGS} retardos)"
CP_T["regla_correccion"] = "Bonferroni con K = nº de modelos de la búsqueda que contienen el término (f2/real_busqueda_eba.csv); sin K para intercepto y dummies"
CP_T = CP_T[["termino", "coef", "EE_HAC", "IC95_inf", "IC95_sup", "p", "K", "p_bonf_K", "p_holm_K", "N", "muestra", "precio", "EE_tipo", "regla_correccion"]]
save_csv(LP_T, "ecuacion_final_lp.csv")
save_csv(CP_T, "ecuacion_final_cp.csv")

# réplica nominal: DOLS base (+q) y ECM preferido nominal + réplica del punto de partida
rows = []
NOM_LP_TERMS = ["const", "ln_ocupados", "tipo_hip", "ln_permisos_l4", "ln_costes"]
for t in NOM_LP_TERMS:
    r = lp_nom.loc[t]
    rows.append(dict(bloque="LP nominal (DOLS +-2, HAC)", termino=t, coef=r.coef, EE_HAC=r.EE_HAC, IC95_inf=r.coef - 1.96 * r.EE_HAC,
                     IC95_sup=r.coef + 1.96 * r.EE_HAC, p=r.p, K=K_FAM_LP if t != "const" else NAN,
                     p_bonf_K=min(1.0, r.p * K_FAM_LP) if t != "const" else NAN, N=int(r.N), muestra=MUESTRA_LP,
                     punto_partida=NAN))
reg_nom_pref = reg2.loc["rob_Preferido1"]
for t, r in ecm_nom.iterrows():
    K = eba_nom.K_modelos.get(t, NAN) if t in eba_nom.index else NAN
    pb = eba_nom.p_bonf_K.get(t, NAN) if t in eba_nom.index else NAN
    rows.append(dict(bloque="CP nominal (ECM preferido R2aj)", termino=t, coef=r.coef, EE_HAC=r.EE_HAC, IC95_inf=r.coef - 1.96 * r.EE_HAC,
                     IC95_sup=r.coef + 1.96 * r.EE_HAC, p=r.p, K=K, p_bonf_K=pb, N=int(reg_nom_pref.n),
                     muestra=f"{reg_nom_pref.muestra_ini}-{reg_nom_pref.muestra_fin}", punto_partida=NAN))
rl = rd("f2/replica_LR.csv").rename(columns={"Unnamed: 0": "termino"})
for _, r in rl.iterrows():
    if r.termino in ("Intercept", "ln_ocupados", "tipo_hip", "ln_permisos_l4", "ln_costes"):
        rows.append(dict(bloque="Réplica punto de partida (EG estático)", termino=r.termino, coef=r.replica, EE_HAC=r.EE_HAC,
                         IC95_inf=r.replica - 1.96 * r.EE_HAC, IC95_sup=r.replica + 1.96 * r.EE_HAC, p=r.p, K=NAN, p_bonf_K=NAN,
                         N=72, muestra="2008Q1-2025Q4", punto_partida=r.punto_partida))
re_ = rd("f2/replica_ECM.csv").rename(columns={"Unnamed: 0": "termino"})
for _, r in re_.iterrows():
    if r.termino in ("R2_aj", "N"):
        continue
    rows.append(dict(bloque="Réplica punto de partida (ECM dos etapas, con dummies)", termino=r.termino, coef=r.con_dum, EE_HAC=r.EE_con,
                     IC95_inf=r.con_dum - 1.96 * r.EE_con, IC95_sup=r.con_dum + 1.96 * r.EE_con, p=r.p_con, K=NAN, p_bonf_K=NAN,
                     N=72, muestra="2008Q1-2025Q4", punto_partida=r.punto_partida))
REPL = pd.DataFrame(rows)
REPL["precio"] = "nominal"
REPL["EE_tipo"] = f"HAC Newey-West ({MAXLAGS} retardos)"
save_csv(REPL, "ecuacion_replica_nominal.csv")

# ======================================================================================
# (2) SIGNIFICATIVIDAD
# ======================================================================================
SIGNO = {  # variable -> (signo esperado, referencia en docs/literatura.md "Tabla: signos esperados")
    "ocupados": ("+", "Martínez Pagés y Maza (2003); Bover y Jimeno (2007)"),
    "renta": ("+", "Martínez Pagés y Maza (2003); Himmelberg et al. (2005)"),
    "tipo": ("-", "Poterba (1984); Himmelberg et al. (2005); Martínez Pagés y Maza (2003)"),
    "costes_precio": ("+", "Glaeser y Gyourko (2005, 2018)"),
    "costes_oferta": ("-", "Glaeser y Gyourko (2005, 2018) (costes sobre oferta)"),
    "permisos": ("-", "Saiz (2010); Hilber y Vermeulen (2016); BdE IA 2025"),
    "terminadas": ("-", "Saiz (2010); Hilber y Vermeulen (2016); BdE IA 2025 (oferta sobre precio)"),
    "credito": ("+", "Mian y Sufi (2009, 2011)"),
    "ect": ("-", "Engle y Granger (1987); Johansen (1988, 1991); Pesaran, Shin y Smith (2001)"),
    "inmig": ("+", "Saiz (2007); González y Ortega (2013); Accetturo et al. (2014) (Sá 2015: negativo en UK)"),
    "elasticidad": ("+", "Saiz (2010); BdE IA 2025 (elasticidad de oferta positiva)"),
    "persistencia": ("n/a", "sin signo esperado en la tabla de literatura (inercia)"),
}


def sg(x):
    return "+" if x > 0 else ("-" if x < 0 else "0")


SIG = []


def add_sig(bloque, variable, coef, se, p, K, p_corr, regla, clave, fuente, nota=""):
    esp, ref = SIGNO[clave]
    if isn(coef):
        coincide = "indeterminado"
    elif esp == "n/a":
        coincide = "n/a"
    else:
        coincide = "sí" if sg(coef) == esp else "no"
    SIG.append(dict(bloque=bloque, variable=variable, coef=coef, EE=se, p=p, K_correccion=K, p_corregido=p_corr, regla_correccion=regla,
                    signo_esperado=esp, referencia_signo=ref, signo_obtenido=("n/d" if isn(coef) else sg(coef)),
                    coincide=coincide, significativo_corregido=("sí" if (not isn(p_corr) and p_corr < ALPHA) else "no"),
                    fuente=fuente, nota=nota))


LPR = LP_REAL.set_index("termino")
for t, clave, lab in [("ln_ocupados", "ocupados", "Empleo (LP real)"), ("tipo_hip_real", "tipo", "Tipo hipotecario real (LP real)"),
                      ("ln_permisos_l4", "permisos", "Permisos t-4 (LP real)"), ("ln_costes_real", "costes_precio", "Costes reales (LP real)")]:
    r = LPR.loc[t]
    add_sig("P1 LP real (DOLS)", lab, r.coef, r.EE_HAC, r.p, K_FAM_LP, HOLM_LP[("real", t)],
            f"Holm sobre familia de {K_FAM_LP} pendientes LP (4 x nominal/real)", clave, "f2/ecuacion_real.csv")
for t, clave, lab in [("ln_ocupados", "ocupados", "Empleo (LP nominal, réplica)"), ("tipo_hip", "tipo", "Tipo hipotecario (LP nominal)"),
                      ("ln_permisos_l4", "permisos", "Permisos t-4 (LP nominal)"), ("ln_costes", "costes_precio", "Costes (LP nominal)")]:
    r = lp_nom.loc[t]
    add_sig("P1 LP nominal (réplica)", lab, r.coef, r.EE_HAC, r.p, K_FAM_LP, HOLM_LP[("nominal", t)],
            f"Holm sobre familia de {K_FAM_LP} pendientes LP (4 x nominal/real)", clave, "f2/largo_plazo.csv")
CPR = CP_REAL.set_index("termino")
for t, clave, lab in [("ect_l1", "ect", "Corrección de error ect(t-1)"), ("d_ln_ocupados_l1", "ocupados", "Empleo Δ (t-1) (CP real)"),
                      ("d_tipo_hip_l1", "tipo", "Δ tipo hipotecario (t-1) (CP real)"), ("d_ln_renta_hog_real", "renta", "Δ renta real del hogar (CP real)"),
                      ("d_ln_ipv_real_l4", "persistencia", "Δ precio real (t-4) (CP real)"), ("d_ln_credito_nuevo", "credito", "Δ crédito nuevo (CP real; comovimiento)")]:
    r = CPR.loc[t]
    add_sig("P1 CP real (ECM)", lab, r.coef, r.EE_HAC, r.p, r.K, r.p_bonf_K, "Bonferroni con K = modelos de la búsqueda con el término",
            clave, "f2/ecuacion_real.csv")
# inmigración: stock en F2
rpe = rd("f2/largo_plazo.csv")
rpe = rpe[(rpe.metodo == "DOLS +pob_extranj") & (rpe["var"] == "ln_pob_extranj")].iloc[0]
add_sig("P2 inmigración (stock, LP nominal)", "ln pob. extranjera (DOLS +pob_extranj)", rpe.coef, rpe.EE_HAC, rpe.p, K_LP_REG,
        min(1.0, rpe.p * K_LP_REG), f"Bonferroni con K = {K_LP_REG} especificaciones de LP registradas en F2", "inmig", "f2/largo_plazo.csv",
        "cointegración con +pob_extranj: 2/3 (nominal) y 2/3 (real) en f2/cointegracion.csv; el LP con pob_extranj no se usa como ecuación final")
for nm, tab, lab in [("nominal", eba_nom, "d ln pob. extranjera (CP búsqueda nominal)"), ("real", eba_real, "d ln pob. extranjera (CP búsqueda real)")]:
    r = tab.loc["d_ln_pob_extranj"]
    add_sig("P2 inmigración (stock, CP)", lab, NAN, NAN, NAN, r.K_modelos, NAN,
            "sin p único: término no incluido en el preferido", "inmig", f"f2/{'busqueda_eba' if nm == 'nominal' else 'real_busqueda_eba'}.csv",
            f"signo positivo en {fm(100 * r.signo_pos, 0)} % de los {fi(r.K_modelos)} modelos que lo incluyen; significativo al 5 % en {fm(100 * r.frac_signif_5pct, 0)} %")
c3 = rd("f3/correccion_busqueda.csv").set_index("modelo_id")
p3 = rd("f3/panel_principal.csv").set_index("modelo")
for mid, pm, lab, nota in [("PAN_ipv_FE_2SLS", "ipv|FE|2SLS", "Flujo neto extranjeros/pob. → IPV (2SLS shift-share)", ""),
                           ("PAN_p_tasado_FE_2SLS", "tasado|FE|2SLS", "Flujo neto → valor tasado (2SLS)", ""),
                           ("PAN_serpavi_FE_OLS", "serpavi|FE|OLS", "Flujo neto → alquiler SERPAVI (OLS)", ""),
                           ("PAN_ipc_alq_FE_OLS", "ipc_alq|FE|OLS", "Flujo neto → IPC alquiler (OLS)", "no estaba en el diseño prefijado (docs/decisiones.md)"),
                           ("PAN_ipc_alq_FE_2SLS", "ipc_alq|FE|2SLS", "Flujo neto → IPC alquiler (2SLS)", "")]:
    r = c3.loc[mid]
    ee = NAN
    if pm in p3.index:
        ee = p3.loc[pm, "EE_cluster"]
    add_sig("P2 inmigración (panel F3)", lab, r.coef_interes, ee, r.p_interes, len(c3), r.p_holm,
            f"Holm sobre {len(c3)} especificaciones de F3 (p = wild cluster bootstrap restringido)", "inmig", "f3/correccion_busqueda.csv",
            nota or "p sin corregir = WCB restringido")
for mid, lab in [("NAC_LP_ln_ipv_x_ext_h0", "Flujo/stock extranjeros → IPV, h=0 (proyección local)"),
                 ("NAC_LP_ln_ipc_alquiler_x_ext_h8", "Δ4 stock extranjeros → IPC alquiler, h=8 (proyección local)")]:
    r = c3.loc[mid]
    add_sig("P2 inmigración (series temporales F3)", lab, r.coef_interes, NAN, r.p_interes, len(c3), r.p_holm,
            f"Holm sobre {len(c3)} especificaciones de F3", "inmig", "f3/correccion_busqueda.csv")
fe5 = rd("f5/tabla_fe_principal.csv").set_index("variable")
cb5 = rd("f5/correccion_busqueda_beta2.csv").rename(columns={"Unnamed: 0": "id"}).set_index("id")
b2 = fe5.loc["b2 d(extr/total, pp)"]
add_sig("P4 panel CCAA (F5)", "Δ(cuota extranjera, pp) → Δln IPV (FE CCAA+año)", b2.coef, b2.EE_cluster, b2.p_wild_Webb, len(cb5), cb5.loc["A_FE_wild", "p_Holm"],
        f"Holm sobre {len(cb5)} variantes de b2 (F5)", "inmig", "f5/tabla_fe_principal.csv; f5/correccion_busqueda_beta2.csv", "p = wild cluster bootstrap (Webb)")
b4 = fe5.loc["b4 terminadas/1000 hab (t-1)"]
pw4 = [float(fe5.loc[v, "p_wild_Webb"]) for v in fe5.index]
add_sig("P4 panel CCAA (F5)", "Terminadas/1000 hab. (t-1) → Δln IPV", b4.coef, b4.EE_cluster, b4.p_wild_Webb, len(fe5),
        holm(pw4)[list(fe5.index).index("b4 terminadas/1000 hab (t-1)")], f"Holm sobre los {len(fe5)} coeficientes del FE principal (p wild)",
        "terminadas", "f5/tabla_fe_principal.csv")
c4 = rd("f4/correccion_busqueda.csv").set_index("modelo_id")
dols4 = rd("f4/dols_resultados.csv").set_index("modelo")
for mid, clave, lab, base in [("dols_visados_k4_ipv", "elasticidad", "Elasticidad oferta: iniciadas libres vs precio real (DOLS k=4)", None)]:
    r = c4.loc[mid]
    d = dols4.loc[mid]
    add_sig("P3 oferta (F4)", lab, d.beta, d.EE, r.p_interes, len(c4), r.p_holm_familia, f"Holm sobre {len(c4)} modelos de la familia de elasticidad",
            clave, "f4/correccion_busqueda.csv", "p de niveles NO válido sin cointegración (1/3): lectura solo del signo")
for mid, clave, lab in [("dols_visados_k4_ipv", "costes_oferta", "Costes reales en la ecuación de iniciadas (DOLS k=4)"),
                        ("dols_permisos_k4_ipv", "costes_oferta", "Costes reales en la ecuación de permisos (DOLS k=4)")]:
    d = dols4.loc[mid]
    pc = pnorm(d.beta_costes, d.EE_costes)
    add_sig("P3 oferta (F4)", lab, d.beta_costes, d.EE_costes, pc, len(c4), min(1.0, pc * len(c4)),
            f"Bonferroni con K = {len(c4)} (p aproximado por normal)", clave, "f4/dols_resultados.csv",
            "el signo positivo en permisos es contrario al esperado" if d.beta_costes > 0 else "")
SIGDF = pd.DataFrame(SIG)
save_csv(SIGDF, "significatividad.csv")

# ======================================================================================
# (3) ROBUSTEZ
# ======================================================================================
REGLA_ROBUSTEZ = (
    "Regla (explícita, mecánica): sea B la estimación de la columna 'muestra completa' y A el conjunto de columnas alternativas con estimación "
    "disponible (pre-COVID, desde 2014, con dummies EPA2021/tipos2022, el precio nominal o real distinto del base, valor tasado y otras "
    "especificaciones; 'n/d' = no estimado, no cuenta). Una alternativa FALLA si cambia el signo de (coef - referencia) respecto de B o si "
    f"su p >= {ALPHA} (cuando hay p). Resultado: 'no' si B no es significativa (p >= {ALPHA}), o si fallan más de la mitad de A, o si el signo "
    "cambia en 2 o más alternativas; 'parcial' si hay al menos un fallo (pero no se cumple 'no'), si hay menos de 2 alternativas disponibles, "
    f"o si la razón entre la mayor y la menor magnitud |coef - referencia| entre columnas con el mismo signo supera {RATIO_MAG:g}; 'sí' en otro caso. "
    "Para la beta de València la referencia es 1 (H0: beta = 1); para el resto es 0. p aproximado con la normal (coef/EE) si la tabla de origen no trae p (marcado '~')."
)


def cell(coef, se=NAN, p=NAN, tag=""):
    approx = False
    if isn(p) and not isn(se):
        p = pnorm(coef, se)
        approx = True
    return dict(coef=coef, se=se, p=p, approx=approx, tag=tag)


def ctext(c, nd=3, ref=0.0):
    if c is None:
        return "n/d"
    s = fm(c["coef"], nd)
    if not isn(c["se"]):
        s += f" ({fm(c['se'], nd)})"
    if isn(c["p"]):
        s += " [sin p]"
    else:
        s += f" [p{'~' if c['approx'] else ''}={fp(c['p'])}]"
    if c["tag"]:
        s += f" {{{c['tag']}}}"
    return s


def parse_ce(s):
    m = re.match(r"\s*(-?[\d.]+)\s*\((-?[\d.]+)\)", str(s))
    return float(m.group(1)), float(m.group(2))


def evalua(row, ref):
    b = row["completa"]
    alts = [row[k] for k in ALT_COLS if row.get(k) is not None and k != "completa" and k in row["_alt"]]
    out = dict(n_alt=len(alts), n_fallos=0, n_cambios_signo=0, razon_magnitud=NAN)
    if b is None or isn(b["p"]):
        return "parcial", out, "estimación base sin p"
    if b["p"] >= ALPHA:
        return "no", out, f"la estimación base no es significativa (p = {fp(b['p'])})"
    sb = sg(b["coef"] - ref)
    fallos = flips = 0
    mags = [abs(b["coef"] - ref)]
    for a in alts:
        flip = sg(a["coef"] - ref) != sb
        ns = (not isn(a["p"])) and a["p"] >= ALPHA
        flips += int(flip)
        fallos += int(flip or ns)
        if not flip:
            mags.append(abs(a["coef"] - ref))
    out.update(n_fallos=fallos, n_cambios_signo=flips)
    mags = [m for m in mags if m > 0]
    ratio = max(mags) / min(mags) if len(mags) > 1 else NAN
    out["razon_magnitud"] = ratio
    if len(alts) and (fallos > len(alts) / 2 or flips >= 2):
        return "no", out, f"fallan {fallos} de {len(alts)} alternativas ({flips} con cambio de signo)"
    if len(alts) < 2:
        return "parcial", out, f"menos de 2 alternativas disponibles ({len(alts)})"
    if fallos >= 1:
        return "parcial", out, f"fallan {fallos} de {len(alts)} alternativas ({flips} con cambio de signo)"
    if not isn(ratio) and ratio > RATIO_MAG:
        return "parcial", out, f"signo y significatividad estables pero magnitud inestable (razón {fm(ratio, 1)})"
    return "sí", out, f"0 fallos en {len(alts)} alternativas"


ALT_COLS = ["pre_COVID", "desde_2014", "dummies_EPA21_tipos22", "nominal", "real", "valor_tasado", "otra_1", "otra_2"]
dsp = rd("f2/dols_subperiodos.csv")
dsp14 = dsp[dsp.subperiodo.str.startswith("2014Q1")].set_index("var")
estab = rd("f2/estabilidad_muestras.csv")
rrob = rd("f2/real_robustez.csv").set_index("modelo")
lpall = rd("f2/largo_plazo.csv")
lp_dum = lpall[lpall.metodo == "DOLS base + epa21 + tipo22"].set_index("var")


def lp_cell_from_ce(sub, var, tag):
    c, e = parse_ce(sub.loc[var, "DOLS_k1"])
    return cell(c, e, tag=tag)


def precovid_real(var):
    ex = rrob.loc["Pre-COVID (≤2019Q4; ect re-estimado)", "extras"]
    m = re.search(var + r"=(-?[\d.]+)", ex)
    return cell(float(m.group(1)), NAN, NAN, "real; sin EE en la tabla") if m else None


def comp_nom(var):
    r = lp_nom.loc[var]
    return cell(r.coef, r.EE_HAC, r.p, "nominal")


ROB = []


def add_rob(nombre, base_price, ref, completa, alt_cols, cells, advert="", fuente=""):
    row = dict(coeficiente=nombre, precio_base=base_price, completa=completa, _alt=alt_cols)
    for k in ALT_COLS:
        row[k] = cells.get(k)
    res, info, why = evalua(row, ref)
    row["_res"] = (res, info, why, advert, fuente, ref)
    ROB.append(row)


# --- empleo LP
r_real = LPR.loc["ln_ocupados"]
add_rob("Empleo LP (ln ocupados)", "real", 0.0, cell(r_real.coef, r_real.EE_HAC, r_real.p, "real"),
        ["pre_COVID", "desde_2014", "dummies_EPA21_tipos22", "nominal"],
        dict(pre_COVID=precovid_real("ln_ocupados"), desde_2014=lp_cell_from_ce(dsp14, "ln_ocupados", "nominal DOLS k=1"),
             dummies_EPA21_tipos22=cell(lp_dum.loc["ln_ocupados", "coef"], lp_dum.loc["ln_ocupados", "EE_HAC"], lp_dum.loc["ln_ocupados", "p"], "nominal"),
             nominal=comp_nom("ln_ocupados"), real=cell(r_real.coef, r_real.EE_HAC, r_real.p, "real")),
        "valor tasado no estimado en el DOLS de F2; pre-COVID real sin EE; el LP real no es estable por subperiodos",
        "f2/ecuacion_real.csv; f2/real_robustez.csv; f2/dols_subperiodos.csv; f2/largo_plazo.csv")
r_ = LPR.loc["tipo_hip_real"]
add_rob("Tipo hipotecario LP (real)", "real", 0.0, cell(r_.coef, r_.EE_HAC, r_.p, "real"),
        ["pre_COVID", "desde_2014", "dummies_EPA21_tipos22", "nominal"],
        dict(pre_COVID=precovid_real("tipo_hip_real"), desde_2014=lp_cell_from_ce(dsp14, "tipo_hip", "nominal DOLS k=1"),
             dummies_EPA21_tipos22=cell(lp_dum.loc["tipo_hip", "coef"], lp_dum.loc["tipo_hip", "EE_HAC"], lp_dum.loc["tipo_hip", "p"], "nominal"),
             nominal=comp_nom("tipo_hip"), real=cell(r_.coef, r_.EE_HAC, r_.p, "real")),
        "tipo real ≈ 0 en la ecuación final", "f2/ecuacion_real.csv; f2/real_robustez.csv; f2/dols_subperiodos.csv; f2/largo_plazo.csv")
r_ = LPR.loc["ln_permisos_l4"]
add_rob("Permisos t-4 LP (proxy de oferta)", "real", 0.0, cell(r_.coef, r_.EE_HAC, r_.p, "real"),
        ["pre_COVID", "desde_2014", "dummies_EPA21_tipos22", "nominal"],
        dict(pre_COVID=precovid_real("ln_permisos_l4"), desde_2014=lp_cell_from_ce(dsp14, "ln_permisos_l4", "nominal DOLS k=1"),
             dummies_EPA21_tipos22=cell(lp_dum.loc["ln_permisos_l4", "coef"], lp_dum.loc["ln_permisos_l4", "EE_HAC"], lp_dum.loc["ln_permisos_l4", "p"], "nominal"),
             nominal=comp_nom("ln_permisos_l4"), real=cell(r_.coef, r_.EE_HAC, r_.p, "real")),
        "", "f2/ecuacion_real.csv; f2/real_robustez.csv; f2/dols_subperiodos.csv; f2/largo_plazo.csv")
r_ = LPR.loc["ln_costes_real"]
add_rob("Costes LP (reales / nominales)", "real", 0.0, cell(r_.coef, r_.EE_HAC, r_.p, "real"),
        ["pre_COVID", "desde_2014", "dummies_EPA21_tipos22", "nominal"],
        dict(pre_COVID=precovid_real("ln_costes_real"), desde_2014=lp_cell_from_ce(dsp14, "ln_costes", "nominal DOLS k=1"),
             dummies_EPA21_tipos22=cell(lp_dum.loc["ln_costes", "coef"], lp_dum.loc["ln_costes", "EE_HAC"], lp_dum.loc["ln_costes", "p"], "nominal"),
             nominal=comp_nom("ln_costes"), real=cell(r_.coef, r_.EE_HAC, r_.p, "real")),
        "el signo negativo del coste real contradice el signo esperado: relación estadística, no estructural",
        "f2/ecuacion_real.csv; f2/real_robustez.csv; f2/dols_subperiodos.csv; f2/largo_plazo.csv")
# --- ect
rr = {k: v for k, v in rrob.iterrows()}
r_ = CPR.loc["ect_l1"]
rn = ecm_nom.loc["ect_l1"]


def ect_cell(row, tag):
    c, e = parse_ce(row["ect"])
    return cell(c, e, row["p_ect"], tag)


add_rob("Corrección de error ect(t-1)", "real", 0.0, cell(r_.coef, r_.EE_HAC, r_.p, "real"),
        ["pre_COVID", "desde_2014", "dummies_EPA21_tipos22", "nominal"],
        dict(pre_COVID=ect_cell(rr["Pre-COVID (≤2019Q4; ect re-estimado)"], "real"), desde_2014=ect_cell(rr["2014Q1-2026Q2"], "real"),
             dummies_EPA21_tipos22=ect_cell(rr["+ epa21 (quiebre_epa_2021) + tipo22 (escalón 2022Q3)"], "real"),
             nominal=cell(rn.coef, rn.EE_HAC, rn.p, "nominal"), real=cell(r_.coef, r_.EE_HAC, r_.p, "real")),
        "valor tasado no estimado en el ECM; el p del ect NO contrasta cointegración (distribución no estándar)",
        "f2/ecuacion_real.csv; f2/real_robustez.csv; f2/ecm_preferido.csv")
# --- empleo CP
r_ = CPR.loc["d_ln_ocupados_l1"]
est = estab.set_index("muestra")


def est_cell(idx, col, tag):
    c, e = parse_ce(est.loc[idx, col].split(" p=")[0])
    return cell(c, e, tag=tag)


i14 = [i for i in est.index if i.startswith("2014Q1")][0]
ipc = [i for i in est.index if "pre-COVID" in i][0]
add_rob("Empleo CP (Δ ln ocupados)", "real", 0.0, cell(r_.coef, r_.EE_HAC, r_.p, "real (t-1)"),
        ["pre_COVID", "desde_2014", "nominal"],
        dict(pre_COVID=est_cell(ipc, "d_ln_ocupados", "nominal (t)"), desde_2014=est_cell(i14, "d_ln_ocupados", "nominal (t)"),
             nominal=cell(ecm_nom.loc["d_ln_ocupados", "coef"], ecm_nom.loc["d_ln_ocupados", "EE_HAC"], ecm_nom.loc["d_ln_ocupados", "p"], "nominal (t)"),
             real=cell(r_.coef, r_.EE_HAC, r_.p, "real (t-1)")),
        "el término es Δ ocupados en t (nominal) y en t-1 (real): la búsqueda elige uno u otro; no sobrevive a Bonferroni (K=%s)" % fi(r_.K),
        "f2/ecuacion_real.csv; f2/estabilidad_muestras.csv; f2/ecm_preferido.csv")
# --- inmigración (panel F3 y F5, stock F2)
ppf = rd("f3/panel_principal.csv")


def f3c(res, spec, est_, tag=""):
    r = ppf[(ppf.resultado == res) & (ppf.spec == spec) & (ppf.est == est_)].iloc[0]
    return cell(r.coef, r.EE_cluster, r.p_WCB_restr if not isn(r.p_WCB_restr) else r.p_cluster, tag)


add_rob("Flujo neto extranjeros → IPV (panel F3, OLS FE)", "IPV (nominal)", 0.0, f3c("IPV (precio)", "FE", "OLS"),
        ["pre_COVID", "valor_tasado", "otra_1"],
        dict(pre_COVID=f3c("IPV (precio)", "FE sin 2020-2021", "OLS", "sin 2020-21"), valor_tasado=f3c("valor tasado", "FE", "OLS", "valor tasado"),
             otra_1=f3c("IPV (precio)", "FE", "2SLS", "2SLS")),
        "columna 'pre_COVID' = muestra sin 2020-2021 (no hay muestra pre-COVID en el panel anual); p = wild cluster bootstrap",
        "f3/panel_principal.csv")
add_rob("Flujo neto extranjeros → alquiler IPC (panel F3, OLS FE)", "IPC alquiler", 0.0, f3c("IPC alquiler", "FE", "OLS"),
        ["pre_COVID", "otra_1"],
        dict(pre_COVID=f3c("IPC alquiler", "FE sin 2020-2021", "OLS", "sin 2020-21"), otra_1=f3c("IPC alquiler", "FE", "2SLS", "2SLS")),
        "pretendencia significativa (grupo América); resultado posterior al diseño prefijado; p = WCB",
        "f3/panel_principal.csv; f3/pretendencias.csv")
add_rob("Flujo neto extranjeros → alquiler SERPAVI (panel F3, OLS FE)", "SERPAVI", 0.0, f3c("alquiler SERPAVI", "FE", "OLS"),
        ["pre_COVID", "otra_1"],
        dict(pre_COVID=f3c("alquiler SERPAVI", "FE sin 2020-2021", "OLS", "sin 2020-21"), otra_1=f3c("alquiler SERPAVI", "FE", "2SLS", "2SLS")),
        "p = WCB", "f3/panel_principal.csv")
tf = rd("f5/robustez_muestras_anual.csv")
tf_b2 = tf[(tf["muestra/dependiente"] == "Valor tasado, 2009-2025") & tf.variable.str.startswith("b2")].iloc[0]
tcce = rd("f5/tabla_cce.csv")
tcce_p = tcce[(tcce.estimador == "CCE-P") & tcce["var"].str.startswith("b2")].iloc[0]
add_rob("Cuota extranjera (pp) → Δln IPV (panel F5, FE CCAA+año)", "IPV (nominal)", 0.0, cell(b2.coef, b2.EE_cluster, b2.p_wild_Webb, "WCB"),
        ["valor_tasado", "otra_1", "otra_2"],
        dict(valor_tasado=cell(tf_b2.coef, tf_b2.EE_cluster, tf_b2.p, "valor tasado; p cluster"),
             otra_1=cell(tcce_p.coef, tcce_p.EE, tcce_p.p, "CCE-P"),
             otra_2=cell(rd("f5/tabla_fe_tendencias.csv").set_index("Unnamed: 0").loc["b2 d(extr/total, pp)", "coef"],
                         rd("f5/tabla_fe_tendencias.csv").set_index("Unnamed: 0").loc["b2 d(extr/total, pp)", "EE_cluster"],
                         rd("f5/tabla_fe_tendencias.csv").set_index("Unnamed: 0").loc["b2 d(extr/total, pp)", "p_cluster"], "FE+tendencias")),
        "el efecto depende de la alineación temporal (f5/timing_b2.csv) y ninguna variante sobrevive a Holm", "f5/tabla_fe_principal.csv; f5/robustez_muestras_anual.csv; f5/tabla_cce.csv")
add_rob("Stock de extranjeros LP (ln pob. extranjera, DOLS)", "nominal", 0.0, cell(rpe.coef, rpe.EE_HAC, rpe.p, "nominal"), [], {},
        "solo un DOLS con pob_extranj; sin contraste en otras muestras ni con precio real", "f2/largo_plazo.csv")
# --- oferta
d4v = dols4.loc["dols_visados_k4_ipv"]
d4t = dols4.loc["dols_visados_k4_tasado"]
cb = rd("f4/contraste_bde.csv")
cb_v = cb[(cb.dep == "visados") & (cb.k == 4)].set_index("estimador")
ols4 = rd("f4/ols_delta4.csv").set_index("modelo").loc["ols_d4_visados_k4"]
add_rob("Elasticidad de la oferta (iniciadas libres, DOLS k=4)", "real (IPV deflactado)", 0.0, cell(d4v.beta, d4v.EE, d4v.p, "DOLS"),
        ["desde_2014", "valor_tasado", "otra_1", "otra_2"],
        dict(desde_2014=cell(cb_v.loc["DOLS ±1 2014T1+", "beta"], cb_v.loc["DOLS ±1 2014T1+", "EE"], cb_v.loc["DOLS ±1 2014T1+", "p"], "DOLS ±1, 2014T1+"),
             valor_tasado=cell(d4t.beta, d4t.EE, d4t.p, "valor tasado real"),
             otra_1=cell(ols4.beta, ols4.EE_HAC8, ols4.p, "OLS Δ4"),
             otra_2=cell(cb_v.loc["IV 2SLS Δ4", "beta"], cb_v.loc["IV 2SLS Δ4", "EE"], cb_v.loc["IV 2SLS Δ4", "p"], "IV Δ4")),
        "los p de niveles no son válidos (cointegración 1/3); el IV en Δ4 no es significativo; no se rechaza beta = 0,45 en Δ4 (f4/contraste_H0_045_principales.csv)",
        "f4/dols_resultados.csv; f4/contraste_bde.csv; f4/ols_delta4.csv")
# --- beta València
bt = rd("f6/beta_todos.csv")
bte = bt[(bt.modelo == "beta_València_vs_España") & (bt.maxlags == MAXLAGS)].iloc[0]
btr = rd("f6/beta_por_tramos.csv")
btr = btr[btr.modelo == "València_vs_España"].set_index("tramo")


def bcell(r, tag):
    return dict(coef=r.beta, se=r.EE_HAC, p=r.p_beta_igual_1, approx=False, tag=tag)


tr = list(btr.index)
add_rob("Beta de València frente a España (Δ4 valor tasado, H0: beta = 1)", "valor tasado (nominal)", 1.0,
        dict(coef=bte.beta, se=bte.EE_HAC, p=bte.p_beta_igual_1, approx=False, tag="HAC4"),
        ["pre_COVID", "otra_1", "otra_2"],
        dict(pre_COVID=bcell(btr.loc[tr[0]], f"tramo {tr[0]}"), otra_1=bcell(btr.loc[tr[1]], f"tramo {tr[1]}"), otra_2=bcell(btr.loc[tr[2]], f"tramo {tr[2]}"),
             valor_tasado=dict(coef=bte.beta, se=bte.EE_HAC, p=bte.p_beta_igual_1, approx=False, tag="es la base")),
        "el p es de H0: beta = 1; EE por tramo aproximados (24-26 trimestres); València forma parte de CV y España (componente parte-todo); el IPV no existe para el municipio",
        "f6/beta_todos.csv; f6/beta_por_tramos.csv")

rob_rows = []
for r in ROB:
    res, info, why, advert, fuente, ref = r["_res"]
    allc = [r["completa"]] + [r[k] for k in ALT_COLS if r.get(k) is not None and k in r["_alt"]]
    coefs = [c["coef"] for c in allc]
    rob_rows.append({
        "coeficiente": r["coeficiente"], "precio_base": r["precio_base"], "referencia_H0": ref,
        "muestra_completa": ctext(r["completa"]),
        "pre_COVID": ctext(r["pre_COVID"]), "desde_2014": ctext(r["desde_2014"]),
        "dummies_EPA21_tipos22": ctext(r["dummies_EPA21_tipos22"]),
        "nominal": ctext(r["nominal"]), "real": ctext(r["real"]), "precio_valor_tasado": ctext(r["valor_tasado"]),
        "otra_especificacion_1": ctext(r["otra_1"]), "otra_especificacion_2": ctext(r["otra_2"]),
        "coef_min": min(coefs), "coef_max": max(coefs),
        "n_alternativas": info["n_alt"], "n_fallos": info["n_fallos"], "n_cambios_signo": info["n_cambios_signo"],
        "razon_magnitud": info["razon_magnitud"], "¿sobrevive?": res, "motivo_regla": why, "advertencia": advert, "fuente": fuente})
ROBDF = pd.DataFrame(rob_rows)
save_csv(ROBDF, "robustez.csv")

# ======================================================================================
# (4) COINTEGRACIÓN
# ======================================================================================
c2 = rd("f2/cointegracion.csv")
c2["bloque"] = "F2 precio nacional"
c2["precio"] = np.where(c2.y.str.contains("real"), "real", np.where(c2.y.str.contains("p_tasado|p_bde"), "valor tasado/BdE", "nominal"))
c4 = rd("f4/cointegracion.csv")
c4["bloque"] = "F4 ecuación de oferta (precio real)"
c4["precio"] = "real"
COINT = pd.concat([c2, c4], ignore_index=True)
cols = ["bloque", "precio", "sistema", "y", "X", "ini", "fin", "N", "EG_t", "EG_p", "EG_rech", "J_traza0", "J_cv95", "J_rango_traza", "J_rech",
        "ARDL_F", "ARDL_I0_5", "ARDL_I1_5", "ARDL_rech", "ARDL_zona", "n_rechazos", "decision"]
for c in cols:
    if c not in COINT.columns:
        COINT[c] = NAN
COINT["decision_regla"] = "se exige >=2 de 3 {Engle-Granger, Johansen traza, ARDL bounds} (docs/decisiones.md)"
COINT = COINT[cols + ["decision_regla"]]
save_csv(COINT, "cointegracion.csv")

# ======================================================================================
# (5) DÉFICIT
# ======================================================================================
dv = rd("f4/deficit_variantes.csv")
dv.insert(0, "tipo", "variante")
bdec = rd("f4/comparacion_bde_deficit.csv")
bdec = bdec.rename(columns={"concepto": "variante", "este_trabajo_principal": "deficit", "BdE": "bde", "nota": "nota"})
bdec.insert(0, "tipo", "comparación BdE (concepto)")
dsc = rd("f4/descomposicion_diferencia_bde.csv").rename(columns={"componente": "variante", "este_trabajo": "deficit"})
dsc.insert(0, "tipo", "descomposición de la diferencia con el BdE")
anual = rd("f4/deficit_anual_principal.csv").rename(columns={"Unnamed: 0": "variante", "deficit_anual": "deficit"})
anual.insert(0, "tipo", "principal por año")
DEF = pd.concat([dv, bdec, dsc, anual], ignore_index=True)
save_csv(DEF, "deficit.csv")

# ======================================================================================
# (6) INMIGRACIÓN IV
# ======================================================================================
pe1 = rd("f3/panel_primera_etapa.csv")
iv = ppf.copy()
# mapa de ids (panel_principal -> correccion_busqueda)
RES_ID = {"IPV (precio)": "ipv", "valor tasado": "p_tasado", "alquiler SERPAVI": "serpavi", "IPC alquiler": "ipc_alq"}
SPEC_ID = {"FE": "FE", "FE+tend": "FE+tend", "FE+ctrl d_ln_ocupados": "FEocu", "FE sin 2020-2021": "FEsinCOVID"}


def corr_id(r):
    if r.spec in SPEC_ID:
        return f"PAN_{RES_ID[r.resultado]}_{SPEC_ID[r.spec]}_{r.est}"
    if r.spec.startswith("FE, x_t y x_t-1"):
        return f"PAN_{RES_ID[r.resultado]}_FElag_{r.est}" if "[x]" in r.spec else None
    return None


iv["id_correccion"] = iv.apply(corr_id, axis=1)
iv["p_holm_150"] = iv.id_correccion.map(c3.p_holm)
iv["p_bonf_150"] = iv.id_correccion.map(c3.p_bonf)
nivel3 = rd("f3/nivel_evidencia.csv")
iv["nivel_evidencia_resultado"] = iv.resultado.map(nivel3.set_index("resultado").nivel)
iv["F_efectivo_ge10_resultado"] = iv.resultado.map(nivel3.set_index("resultado").F_ge10)
iv["sobrevive_WCB_resultado"] = iv.resultado.map(nivel3.set_index("resultado").sobrevive_WCB)
iv["pretendencias_no_signif_resultado"] = iv.resultado.map(nivel3.set_index("resultado").pretend_no_signif)
IVT = iv.drop(columns=["modelo"]).rename(columns={"G": "clusters"})
save_csv(IVT, "inmigracion_iv.csv")

# ======================================================================================
# (7) PANEL CCAA
# ======================================================================================
rows = []
for v, r in fe5.iterrows():
    rows.append(dict(bloque="F5 FE CCAA+año, Δln IPV", especificacion="FE principal (cluster CCAA, DK, wild Webb)", variable=v, coef=r.coef,
                     EE=r.EE_cluster, p=r.p_cluster, p_alternativo=r.p_wild_Webb, tipo_p_alternativo="wild cluster bootstrap (Webb)", N=289, fuente="f5/tabla_fe_principal.csv"))
for _, r in rd("f5/tabla_cce.csv").iterrows():
    rows.append(dict(bloque="F5 CCE", especificacion=r.estimador, variable=r["var"], coef=r.coef, EE=r.EE, p=r.p, N=N_F5, fuente="f5/tabla_cce.csv"))
for v, r in rd("f5/tabla_fe_tendencias.csv").set_index("Unnamed: 0").iterrows():
    rows.append(dict(bloque="F5 FE + tendencias CCAA", especificacion="FE+tendencias", variable=v, coef=r.coef, EE=r.EE_cluster, p=r.p_cluster, N=N_F5,
                     fuente="f5/tabla_fe_tendencias.csv"))
for _, r in rd("f5/timing_b2.csv").iterrows():
    rows.append(dict(bloque="F5 alineación temporal de b2", especificacion=r["alineacion de la cuota"], variable="b2 d(extr/total, pp)", coef=r.b2,
                     EE=r.EE_cluster, p=r.p_cluster, p_alternativo=r.p_wild_Webb, tipo_p_alternativo="wild cluster bootstrap (Webb)", N=int(r.N),
                     fuente="f5/timing_b2.csv"))
for k, r in cb5.iterrows():
    rows.append(dict(bloque="F5 corrección por búsqueda (b2)", especificacion=k, variable="b2", p=r.p_sin_corregir, p_alternativo=r.p_Holm,
                     tipo_p_alternativo="Holm sobre 15", fuente="f5/correccion_busqueda_beta2.csv"))
pool = rd("f5/poolability.csv").iloc[0]
rows.append(dict(bloque="F5 poolability", especificacion=pool["Unnamed: 0"], variable="pendientes iguales entre CCAA", coef=pool.F, p=pool.p_clasico,
                 p_alternativo=pool.p_wild_Webb, tipo_p_alternativo="wild cluster bootstrap (Webb); límite de aleatorización 1/17", fuente="f5/poolability.csv"))
for _, r in rd("f5/valencia_vs_espana.csv").iterrows():
    rows.append(dict(bloque="F5 C. Valenciana vs España (descriptivo)", especificacion=f"{r.periodo} {r.serie}", variable="crecimiento acumulado CV-España (pp)",
                     coef=r.dif_pp, fuente="f5/valencia_vs_espana.csv"))
for _, r in rd("f4/panel_ccaa.csv").iterrows():
    rows.append(dict(bloque="F4 panel oferta (robustez)", especificacion=r.modelo, variable=f"beta ({r.dep}, retardo {r.lag_trim} trim.)", coef=r.beta, EE=r.EE_cluster,
                     p=r.p_cluster, p_alternativo=r.p_WCB_webb, tipo_p_alternativo="wild cluster bootstrap (Webb)", N=int(r.n), fuente="f4/panel_ccaa.csv"))
PAN = pd.DataFrame(rows)
save_csv(PAN, "panel_ccaa.csv")

# ======================================================================================
# (8) VALÈNCIA
# ======================================================================================
rows = []
for _, r in bt.iterrows():
    rows.append(dict(bloque="Beta Δ4 (HAC)", especificacion=r.modelo, tramo="muestra completa", maxlags=r.maxlags, N=r.N, estimacion=r.beta, EE_HAC=r.EE_HAC,
                     p=r.p_beta_igual_1, hipotesis="beta = 1", fuente="f6/beta_todos.csv"))
for _, r in rd("f6/beta_por_tramos.csv").iterrows():
    rows.append(dict(bloque="Beta por tramos", especificacion=r.modelo, tramo=r.tramo, N=r.N_tramo, estimacion=r.beta, EE_HAC=r.EE_HAC, p=r.p_beta_igual_1,
                     hipotesis="beta = 1", fuente="f6/beta_por_tramos.csv"))
for _, r in rd("f6/diferencial_nivel_por_tramos.csv").iterrows():
    rows.append(dict(bloque="Diferencial de crecimiento por tramo (pp/año)", especificacion=r.modelo, tramo=r.tramo, N=r.N_tramo, estimacion=r.dif_media_pp,
                     EE_HAC=r.EE_HAC, p=r.p_dif_igual_0, hipotesis="dif = 0", fuente="f6/diferencial_nivel_por_tramos.csv"))
for _, r in rd("f6/quiebres_wald_hac.csv").iterrows():
    rows.append(dict(bloque="Quiebres (Wald HAC8)", especificacion=r.modelo, tramo=r.fecha, N=r.n, estimacion=r.dif_beta_post, EE_HAC=r.EE_dif_beta, p=r.p_Wald_HAC8,
                     hipotesis="sin cambio de beta", fuente="f6/quiebres_wald_hac.csv"))
for _, r in rd("f6/bai_perron_beta.csv").iterrows():
    rows.append(dict(bloque="Bai-Perron sobre la beta", especificacion=r.modelo, tramo=r.fechas, N=NAN, estimacion=r.n_quiebres, hipotesis="nº de quiebres",
                     fuente="f6/bai_perron_beta.csv"))
for _, r in rd("f6/diagnosticos_beta.csv").iterrows():
    rows.append(dict(bloque="Diagnósticos (p)", especificacion=r.modelo, tramo="BG4/RESET/CUSUM", N=r.n, estimacion=NAN,
                     p=min(r.BG4_p, r.RESET_p, r.CUSUM_p), hipotesis=f"BG4 p={fp(r.BG4_p)}; RESET p={fp(r.RESET_p)}; CUSUM p={fp(r.CUSUM_p)}", fuente="f6/diagnosticos_beta.csv"))
cq = rd("f6/cuota_extranjeros_inferencia.csv").set_index("concepto")
rows.append(dict(bloque="Cuota de compradores extranjeros CV - España (descriptivo)", especificacion="trimestres con CV > España", tramo="2007Q1-",
                 N=cq.loc["N", "valor"], estimacion=cq.loc["trimestres con CV > ES", "valor"], hipotesis="hecho descriptivo (el p numérico no es fiable)",
                 fuente="f6/cuota_extranjeros_inferencia.csv"))
VAL = pd.DataFrame(rows)
save_csv(VAL, "valencia.csv")

# ======================================================================================
# (9) REFERENCIAS (se escribe tras generar el texto)
# ======================================================================================
LIT = (DOCS / "literatura.md").read_text(encoding="utf-8")


def _ascii(x: str) -> str:
    return unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()


def _surnames(authors: str) -> list[str]:
    sn = re.findall(r"([^\W\d_][\w'\-]*(?: [\w'\-]+)*?), (?:[^\W\d_]\.\s?)+", authors)
    sn = [re.sub(r"^y ", "", x.strip()) for x in sn]
    return sn if sn else [authors.strip()]


def _clave(surn: list[str], year: str, title: str) -> str:
    if len(surn) == 1:
        a = surn[0]
    elif len(surn) == 2:
        a = f"{surn[0]} y {surn[1]}"
    else:
        a = f"{surn[0]} et al."
    return f"{a} ({year}). {title}"


def parse_lit():
    ent = []
    sec = None
    for ln in LIT.splitlines():
        if ln.startswith("## "):
            sec = ln
            continue
        if sec and sec.startswith("## Bibliografía verificada") and ln.startswith("- "):
            txt = ln[2:].strip()
            if txt.startswith("Documentos no académicos"):
                continue
            m = re.match(r"(.+?) \((\d{4})\)\. (.+?)\.(?: |$)", txt)
            if not m:
                continue
            authors, year, title = m.group(1), m.group(2), m.group(3)
            title = re.sub(r"\*", "", title).split(", cap")[0].strip()
            if authors.startswith("Funcas:"):
                authors = authors.split(":", 1)[1].strip()
            surn = _surnames(authors)
            if authors.startswith("Banco de España"):
                surn = ["Banco de España"]
            low = txt.lower()
            marca = "VERIFICADA"
            if "**no verificada**" in low:
                marca = "NO VERIFICADA"
            elif "no se verificó" in low or "verificación **parcial**" in low:
                marca = "PARCIAL"
            ent.append(dict(clave=_clave(surn, year, title)[:140], apellidos=surn, años=[year], marca=marca,
                            detalle=re.sub(r"\s+", " ", txt)[:300], origen="Bibliografía verificada"))
        if sec and sec.startswith("## ANEXO") and ln.startswith("|") and not ln.startswith("|---") and not ln.startswith("| Referencia"):
            cells = [c.strip() for c in ln.strip("|").split("|")]
            m = re.match(r"(.+?) \(([^)]*)\)", cells[0])
            if not m:
                continue
            nombre, par = m.group(1), m.group(2)
            years = re.findall(r"(\d{4})", par)
            low = " ".join(cells).lower()
            marca = "VERIFICADA"
            if "verificación **parcial**" in low or "no verificado" in low or "no localizado" in low or "p. final no verificada" in low:
                marca = "PARCIAL"
            if "**no verificada**" in low:
                marca = "NO VERIFICADA"
            surn = [x.strip() for x in re.split(r" y |, ", nombre)]
            ent.append(dict(clave=cells[0], apellidos=surn, años=years, marca=marca,
                            detalle=re.sub(r"\s+", " ", " ; ".join(cells[:3]))[:300], origen="Anexo metodológico"))
    return ent


LITENT = parse_lit()

# ======================================================================================
# INFORME
# ======================================================================================
L: list[str] = []


def H(t, n=2):
    L.append("\n" + "#" * n + " " + t + "\n")


def P(t=""):
    L.append(t)


def PL(items):
    """lista Markdown compacta (un solo bloque)"""
    L.append("\n".join(f"- {i}" for i in items))


def fuente(*fs):
    P("\n*Fuentes: " + "; ".join(f"`output/{f}`" if not f.startswith(("docs/", "output/")) else f"`{f}`" for f in fs) + ".*\n")


# valores ----------------------------------------------------------------------------
lp_r = LPR
cp_r = CPR
cdf2 = c2.set_index("sistema")
sys_nom = [s for s in c2.sistema if s.startswith("ln_ipv 2008Q1") and s.endswith("/ base")][0]
sys_real = [s for s in c2.sistema if s.startswith("ln_ipv_real") and s.endswith("/ base")][0]
cn, cr = cdf2.loc[sys_nom], cdf2.loc[sys_real]
cmp_nr = rd("f2/comparacion_nominal_real.csv").set_index("Unnamed: 0") if "Unnamed: 0" in rd("f2/comparacion_nominal_real.csv").columns else None
cmp_nr = rd("f2/comparacion_nominal_real.csv")
cmp_nr = cmp_nr.rename(columns={cmp_nr.columns[0]: "k"}).set_index("k")
oos_r = rd("f2/real_oos_dm.csv").set_index("modelo")
oos_n = rd("f2/oos_dm.csv").set_index("modelo")
rdiag = rd("f2/real_diagnosticos.csv").rename(columns={"Unnamed: 0": "modelo"}).set_index("modelo")
rchow = rd("f2/real_chow.csv").set_index("fecha")
nchow = rd("f2/chow.csv").set_index("fecha")
rbp = rd("f2/real_bai_perron.csv").set_index("ecuacion")
ectrec = rd("f2/ect_recursivo.csv").set_index("hasta")
boot_r = rd("f2/real_busqueda_bootstrap.csv")
gan_r = rd("f2/real_busqueda_ganadores.csv")
frec_pref = float(cmp_nr.loc["frec. bootstrap del preferido", "real"])
r2_real = float(cmp_nr.loc["R2_aj CP", "real"])
r2_nom = float(cmp_nr.loc["R2_aj CP", "nominal"])
MIN_P_INM = float(c3.p_interes.min())
MIN_HOLM_F3 = float(c3.p_holm.min())
MIN_HOLM_F5 = float(cb5.p_Holm.min())
n_f3 = len(c3)
# dummies/estabilidad
real_ect_pre = rrob.loc["Pre-COVID (≤2019Q4; ect re-estimado)"]
real_ect_14 = rrob.loc["2014Q1-2026Q2"]
real_ect_dum = rrob.loc["+ epa21 (quiebre_epa_2021) + tipo22 (escalón 2022Q3)"]
ect_pre_c, ect_pre_e = parse_ce(real_ect_pre["ect"])
ect_14_c, ect_14_e = parse_ce(real_ect_14["ect"])
# F4
dvs = dv.set_index("variante")
d_main = dvs.loc["(a) EPA corregida (PRINCIPAL)"].iloc[0] if isinstance(dvs.loc["(a) EPA corregida (PRINCIPAL)"], pd.DataFrame) else dvs.loc["(a) EPA corregida (PRINCIPAL)"]
dv_main = dv[dv.variante == "(a) EPA corregida (PRINCIPAL)"].iloc[0]
dv_main26 = dv[dv.variante == "(a) EPA corregida (PRINCIPAL)"].iloc[1]
dv_a0 = dv[dv.variante.str.startswith("(a') ")].iloc[0]
dv_raw = dv[dv.variante.str.startswith("(a'') ")].iloc[0]
dv_ecp = dv[dv.variante.str.startswith("(b) ECP")].iloc[0]
dv_pk = dv[dv.variante.str.startswith("(c) ")].iloc[0]
bdec_i = bdec.set_index("variante")
bde_def = bdec_i.loc["Déficit acumulado 2021-2025", "bde"]
bde_ief = bdec_i.loc["Déficit 2021-2025 (IEF otoño 2025)", "bde"]
dsc_i = dsc.set_index("variante")
H0_045 = float(cb.loc[0, "BdE_0.45"])
h045 = rd("f4/contraste_H0_045_principales.csv")
h045_v = h045[(h045.dep == "visados")].set_index("estimador")
ci4 = cb_v.loc["DOLS ±2"]
corr4 = rd("f4/correccion_busqueda.csv")
n_nac4 = len(corr4[~corr4.modelo_id.str.startswith("panel")])
cnac = corr4[~corr4.modelo_id.str.startswith("panel")]
# F4 cointegración principal
c4i = c4.iloc[2]
ecm4 = rd("f4/ecm_resultados.csv").set_index("modelo").loc["ecm_visados_k4"]
chow4 = rd("f4/chow.csv")
bp4 = rd("f4/bai_perron.csv")
iv4 = rd("f4/iv_resultados.csv").set_index("modelo")
# F5
tt = rd("f5/timing_b2.csv")
diag5 = rd("f5/diagnosticos_fe.csv")
hetero = rd("f5/heterogeneidad_interacciones.csv")
n_ccaa = int(rd("f4/panel_ccaa.csv").CCAA.iloc[0])
vcv = rd("f5/valencia_vs_espana.csv")
# F6
bpt = rd("f6/beta_por_tramos.csv")
dnt = rd("f6/diferencial_nivel_por_tramos.csv")
qw = rd("f6/quiebres_wald_hac.csv")
bpb = rd("f6/bai_perron_beta.csv").set_index("modelo")
cuota = rd("f6/cuota_extranjeros_inferencia.csv").set_index("concepto")["valor"]
ca = rd("f6/crecimiento_acumulado_p_tasado.csv").set_index("Unnamed: 0")
ivt = rd("f6/ipv_vs_tasado_acumulado.csv").set_index("medida")
tN = rd("f6/tabla_N_series.csv")
n_desc = int((tN.uso.str.startswith("descriptivo")).sum())
n_elig_usadas = int(((tN.uso.str.startswith("elegible")) & (tN.usada_en_estimacion == "sí")).sum())
n_noval = tN[tN.validado != "sí"]
n_noval_estim = int((n_noval.usada_en_estimacion == "sí").sum())
dc6 = rd("f6/diagnosticos_beta.csv")

_ok = CP_T[(CP_T.p_bonf_K < ALPHA)].termino.tolist()
BONF_TXT = ("ningún término del corto plazo sobrevive a Bonferroni (K = nº de modelos de la búsqueda que lo contienen)." if not _ok
            else "sobreviven a Bonferroni solo: " + ", ".join(_ok) + ".")
# ---------------------------------------------------------------------------- portada
P("# Determinantes del precio de la vivienda en España: síntesis (módulo C. Valenciana / València)\n")
P("Documento generado por `src/report.py` a partir de las tablas de `output/` (ninguna cifra del texto está escrita a mano; cada sección cita el archivo de origen). "
  "Lenguaje: *asociación*; ninguna pregunta alcanza el nivel causal. Errores estándar: HAC Newey-West "
  f"({MAXLAGS} retardos) en series temporales y cluster por CCAA (con wild cluster bootstrap y Driscoll-Kraay como robustez) en panel. Nivel de significación de referencia {fm(100 * ALPHA, 0)} % (docs/decisiones.md).")

# ---------------------------------------------------------------------------- resumen ejecutivo
H("1. Resumen ejecutivo")
sv_si = ROBDF["¿sobrevive?"].value_counts()
IPV2 = iv[(iv.resultado == "IPV (precio)") & (iv.spec == "FE") & (iv.est == "2SLS")].iloc[0]
P(f"- **Alcance de la búsqueda:** {fi(N_TOTAL)} especificaciones registradas en total ({', '.join(f'{k}: {fi(v)}' for k, v in POR_FASE.items())}); "
  f"la búsqueda de corto plazo de F2 cubre {fi(K_CP_NOM)} modelos con precio nominal y {fi(K_CP_REAL)} con precio real. Ningún resultado de este informe es confirmatorio en el sentido de una única hipótesis prefijada.")
P(f"- **P1 (asociación).** Ecuación final con precio **real**: largo plazo (DOLS, N={fi(LPR.loc['ln_ocupados', 'N'])}) con empleo {ce(LPR.loc['ln_ocupados', 'coef'], LPR.loc['ln_ocupados', 'EE_HAC'])} y corto plazo (ECM, N={fi(CPR.loc['ect_l1', 'N'])}) con "
  f"término de corrección del error {ce(CPR.loc['ect_l1', 'coef'], CPR.loc['ect_l1', 'EE_HAC'])} (p = {fp(CPR.loc['ect_l1', 'p'])}), "
  f"que **cambia de signo antes de 2020** ({ce(ect_pre_c, ect_pre_e)}, p = {fp(real_ect_pre['p_ect'])}). Cointegración: real {int(cr.n_rechazos)}/3, nominal {int(cn.n_rechazos)}/3. "
  f"El modelo preferido gana en el {fm(100 * frec_pref, 1)} % de las réplicas del bootstrap de la selección y no mejora al AR(4) fuera de muestra (DM p = {fp(oos_r.loc['Preferido (R2aj)', 'p vs AR4+q'])}).")
P(f"- **P2 (asociación).** El flujo neto de extranjeros no se asocia de forma robusta con el precio de compra: 2SLS shift-share sobre IPV {ce(IPV2.coef, IPV2.EE_cluster)}; "
  f"el menor p ajustado por Holm sobre {fi(n_f3)} especificaciones es {fp(MIN_HOLM_F3)}. Asociación positiva con el alquiler en OLS que no sobrevive al ajuste ni al 2SLS.")
P(f"- **P3 (descriptivo / asociación débil).** Déficit acumulado 2021-2025 = {fi(dv_main.deficit)} viviendas (EPA corregida; {fi(dv_ecp.deficit)} con ECP) frente a ~{fi(bde_def)} del BdE. "
  f"Elasticidad de la oferta (iniciadas, DOLS k=4) = {ce(d4v.beta, d4v.EE, 2)}; en Δ4 no se rechaza {fm(H0_045, 2)} (p Holm = {fp(h045_v.loc['OLS Δ4 (HAC8)', 'p_holm_H0_045'])}).")
b2r = fe5.loc["b2 d(extr/total, pp)"]
P(f"- **P4 (asociación; València descriptiva).** Panel de {n_ccaa} CCAA: b2 = {ce(b2r.coef, b2r.EE_cluster, 4)} (p wild = {fp(b2r.p_wild_Webb)}); no se detecta heterogeneidad (p wild de poolability = {fp(pool.p_wild_Webb)}), lo que no prueba homogeneidad. "
  f"València: beta frente a España {ce(bte.beta, bte.EE_HAC, 2)}, inestable por tramos.")
_rej0 = [f for f in rchow.index if rchow.loc[f, "p"] < ALPHA]
_nrej0 = [f for f in rchow.index if rchow.loc[f, "p"] >= ALPHA]
P(f"- **P5 (descriptivo).** Chow (ECM real) rechaza en {', '.join(_rej0)} (2014Q1: p = {fp(rchow.loc['2014Q1', 'p'])}) y no rechaza en {', '.join(_nrej0)}; Bai-Perron en niveles: {rbp.loc['LR real (niveles)', 'fechas']}. El modelo **no es estable**.")
P(f"- **Robustez** ({len(ROBDF)} coeficientes clave; regla en la sección 8): sobreviven ('sí') {int(sv_si.get('sí', 0))}; parcialmente {int(sv_si.get('parcial', 0))}; no {int(sv_si.get('no', 0))} (`tablas/robustez.csv`).")
fuente("registro_busqueda.csv", "tablas/ecuacion_final_lp.csv", "tablas/ecuacion_final_cp.csv", "tablas/robustez.csv", "tablas/cointegracion.csv", "tablas/deficit.csv", "tablas/inmigracion_iv.csv", "tablas/panel_ccaa.csv", "tablas/valencia.csv")

# ---------------------------------------------------------------------------- datos y muestra
H("2. Datos y muestra")
P("Todos los modelos leen únicamente `data/processed` y las muestras se recortan a la común antes de estimar (docs/decisiones.md). N exacto por modelo:")
nrows = []
for fase, lab in [("F2", "Precio nacional"), ("F3", "Inmigración"), ("F4", "Oferta"), ("F5", "Panel CCAA"), ("F6", "València")]:
    s = REG[REG.fase == fase]
    nrows.append(dict(fase=fase, ámbito=lab, especificaciones=len(s), n_min=int(s.n.min()), n_max=int(s.n.max())))
P(mdt(pd.DataFrame(nrows).assign(especificaciones=lambda d: d.especificaciones.map(fi), n_min=lambda d: d.n_min.map(fi), n_max=lambda d: d.n_max.map(fi))))
P("")
mod_n = [
    ("LP real (DOLS ±2)", LPR.loc["ln_ocupados", "N"], MUESTRA_LP, "f2/ecuacion_real.csv"),
    ("CP real (ECM preferido)", CPR.loc["ect_l1", "N"], MUESTRA_CP, "f2/ecuacion_real.csv"),
    ("Cointegración nominal/real", cn.N, f"{cn.ini}-{cn.fin}", "f2/cointegracion.csv"),
    ("Pre-COVID real (ECM)", real_ect_pre.N, "2008Q2-2019Q4", "f2/real_robustez.csv"),
    ("2014+ real (ECM)", real_ect_14.N, "2014Q1-2026Q2", "f2/real_robustez.csv"),
    ("Proyecciones locales (IPV)", rd("f3/nacional_lp.csv").query("dep=='ln_ipv'").n.iloc[0], rd("f3/nacional_lp.csv").query("dep=='ln_ipv'").muestra.iloc[0], "f3/nacional_lp.csv"),
    ("Panel F3 IPV / valor tasado / SERPAVI / IPC alq.", " / ".join(fi(x) for x in pe1.n), "17 CCAA anuales", "f3/panel_primera_etapa.csv"),
    ("Oferta: DOLS / Δ4", f"{fi(d4v.n)} / {fi(ols4.n)}", "2009Q4-2025Q4 / Δ4", "f4/dols_resultados.csv; f4/ols_delta4.csv"),
    ("Panel F5 (FE principal)", N_F5, f"{MUESTRA_F5}, {n_ccaa} CCAA", "f5/tabla_fe_principal.csv (N del registro)"),
    ("València: beta Δ4 / compraventas", f"{fi(bte.N)} / {fi(bt[bt.modelo.str.startswith('beta_compraventas')].N.iloc[0])}", "2005Q1-2026Q2 (Δ4) / 2007Q1-2026Q1", "f6/beta_todos.csv"),
]
P(mdt(pd.DataFrame([dict(modelo=a, N=fi(b) if not isinstance(b, str) else b, muestra=c, fuente=f"`output/{d}`") for a, b, c, d in mod_n])))
P("")
P(f"**Interpolaciones y limitaciones de datos** (de `docs/limitaciones.md`, sección Datos): ")
lim_txt = (DOCS / "limitaciones.md").read_text(encoding="utf-8")


def lim_sections():
    secs, cur, name = {}, [], None
    for ln in lim_txt.splitlines():
        if ln.startswith("## "):
            if name:
                secs[name] = cur
            name, cur = ln[3:].strip(), []
        elif ln.startswith("- ") and name:
            cur.append(ln[2:].strip())
    if name:
        secs[name] = cur
    return secs


LIMS = lim_sections()
for k, v in LIMS.items():
    if k.startswith("Datos"):
        PL(v)
P("")
P(f"**Datos no validados.** De las {fi(len(tN))} series de `valencia.csv` listadas, {fi(len(n_noval))} tienen validación 'plausibilidad' (no 'sí'); de ellas {fi(n_noval_estim)} entran en alguna estimación. "
  f"Las series con N < 40 ({fi(n_desc)}) se tratan solo de forma descriptiva y las series de PDF no validadas quedan limitadas a robustez, nunca al modelo principal (CLAUDE.md). "
  "Ninguna serie procede de OCR (docs/diccionario_variables.md).")
fuente("registro_busqueda.csv", "f6/tabla_N_series.csv", "docs/limitaciones.md", "docs/diccionario_variables.md")
H("Métodos y diagnósticos utilizados", 3)
P("Errores estándar HAC: Newey y West (1987). Raíces unitarias: Dickey y Fuller (1979), Kwiatkowski, Phillips, Schmidt y Shin (1992) y Zivot y Andrews (1992); p-valores de MacKinnon (1996). "
  "Largo plazo: DOLS de Stock y Watson (1993); cointegración: Engle y Granger (1987), Johansen (1988, 1991) y contrastes de límites de Pesaran, Shin y Smith (2001). "
  "Diagnósticos por modelo: Durbin y Watson (1950), Breusch (1978) y Godfrey (1978b) para autocorrelación, Breusch y Pagan (1979), Jarque y Bera (1987), Ramsey (1969) para RESET, Brown, Durbin y Evans (1975) para CUSUM, "
  "Chow (1960) y Bai y Perron (1998, 2003) para quiebres, y factor de inflación de la varianza (VIF). Predicción: Diebold y Mariano (1995). "
  "Búsqueda de especificaciones: Holm (1979) y Bonferroni, y cotas extremas de Leamer (1983). Panel: Driscoll y Kraay (1998), Cameron, Gelbach y Miller (2008), Webb (2023), Pesaran (2006) y Pesaran (2007). "
  "Inmigración: Jordà (2005) para proyecciones locales y Card (2001) y Goldsmith-Pinkham, Sorkin y Swift (2020) para el diseño shift-share.")
fuente("docs/literatura.md")


# ---------------------------------------------------------------------------- P1
H("3. P1 - Ecuación de largo y corto plazo del precio nacional")
P("**Respuesta.** La ecuación que se interpreta es la de precio **real** (IPV deflactado por el deflactor implícito del PIB), porque es la única cuya relación de nivel cointegra en los tres contrastes. "
  "Es una desviación motivada del pre-registro (docs/decisiones.md): la nominal se mantiene como réplica del punto de partida y se reportan ambas. Se lee como asociación estadística, no como relación estructural.")
P(f"**Nivel de evidencia: ASOCIACIÓN.** Justificación: no hay identificación (regresores endógenos, sin instrumento); la cointegración del vector real es {int(cr.n_rechazos)}/3 pero la del nominal es {int(cn.n_rechazos)}/3; "
  f"el término de corrección del error cambia de signo antes de 2020; {BONF_TXT}")
P("\n### 3.1 Ecuación final de largo plazo (DOLS ±2, precio real)\n")
t = LP_T.copy()
t = pd.DataFrame(dict(término=t.termino, coef=t.coef.map(lambda x: fm(x, 4)), EE_HAC=t.EE_HAC.map(lambda x: fm(x, 4)), IC95=[f"[{fm(a, 3)}; {fm(b, 3)}]" for a, b in zip(t.IC95_inf, t.IC95_sup)],
                      p=t.p.map(fp), p_Bonf_K=t.p_bonf_K.map(fp), p_Holm=t.p_holm_K.map(fp), N=t.N.map(fi)))
P(mdt(t))
eq_lp = "ln IPV_real = " + fm(LPR.loc["const", "coef"], 2) + " " + " ".join(f"{'+' if LPR.loc[x, 'coef'] >= 0 else '-'} {fm(abs(LPR.loc[x, 'coef']), 3)}·{x}" for x in SLOPES_LP)
P(f"\nEcuación: `{eq_lp}` (más dummies trimestrales y adelantos/retardos del DOLS; muestra {MUESTRA_LP}). Corrección: familia de {K_FAM_LP} pendientes de largo plazo (4 × {{nominal, real}}); no cubre la elección de regresores, que en el largo plazo no se buscó.")
P("\n### 3.2 Ecuación final de corto plazo (ECM preferido por R² ajustado, precio real)\n")
t = CP_T.copy()
t = pd.DataFrame(dict(término=t.termino, coef=t.coef.map(lambda x: fm(x, 4)), EE_HAC=t.EE_HAC.map(lambda x: fm(x, 4)), IC95=[f"[{fm(a, 3)}; {fm(b, 3)}]" for a, b in zip(t.IC95_inf, t.IC95_sup)],
                      p=t.p.map(fp), K=t.K.map(fi), p_Bonf_K=t.p_bonf_K.map(fp), N=t.N.map(fi)))
P(mdt(t))
P(f"\nR² ajustado = {fm(r2_real, 3)} (nominal: {fm(r2_nom, 3)}). Muestra {MUESTRA_CP}. `ect_l1` es el residuo rezagado del DOLS real. "
  f"El preferido aparece como ganador en el {fm(100 * frec_pref, 1)} % de las réplicas del bootstrap por bloques de la selección completa: la especificación concreta **no está identificada**; "
  f"{fi(K_CP_REAL)} modelos en la búsqueda real.")
P("\n### 3.3 Réplica nominal del punto de partida\n")
rn_ = REPL[REPL.bloque.str.startswith("LP nominal")]
P(mdt(pd.DataFrame(dict(término=rn_.termino, coef=rn_.coef.map(lambda x: fm(x, 4)), EE_HAC=rn_.EE_HAC.map(lambda x: fm(x, 4)), p=rn_.p.map(fp), N=rn_.N.map(fi)))))
P(f"\nCP nominal: término de corrección {ce(ecm_nom.loc['ect_l1', 'coef'], ecm_nom.loc['ect_l1', 'EE_HAC'], 4)}, R² ajustado {fm(r2_nom, 3)}. "
  "La réplica del punto de partida (EG estático) reproduce sus pendientes casi exactamente (`tablas/ecuacion_replica_nominal.csv`, bloque 'Réplica punto de partida').")
P("\n### 3.4 Cointegración (los tres contrastes, nominal y real)\n")
ct = COINT[COINT.bloque.str.startswith("F2") & COINT.sistema.str.endswith("/ base") & ~COINT.sistema.str.startswith(("ln_p_tasado", "ln_p_bde"))]
P(mdt(pd.DataFrame(dict(precio=ct.precio, N=ct.N.map(fi), EG_p=ct.EG_p.map(fp), Johansen_traza=[f"{fm(a, 1)} (cv {fm(b, 1)})" for a, b in zip(ct.J_traza0, ct.J_cv95)],
                        ARDL_F=[f"{fm(a, 2)} (I1 {fm(b, 2)}; {z})" for a, b, z in zip(ct.ARDL_F, ct.ARDL_I1_5, ct.ARDL_zona)], rechazos=ct.n_rechazos.map(fi), decisión=ct.decision))))
P(f"\nRegla: se exige concordancia de al menos 2 de 3 contrastes. El t del ect NO contrasta cointegración (distribución no estándar; Banerjee-Dolado-Mestre 1998). "
  "Con valor tasado y BdE (la misma serie) el vector base da: {cdf2.loc[[x for x in cdf2.index if x.startswith('ln_p_tasado') and x.endswith('/ base')][0], 'decision']} (`tablas/cointegracion.csv`).")
P("\n### 3.5 Diagnósticos de la ecuación final\n")
dg = rdiag.copy()
dg_rows = []
for mname, r in dg.iterrows():
    fails = [n for n, v in [("BG(4)", r.BG4_p), ("Breusch-Pagan", r.BP_p), ("Jarque-Bera", r.JB_p), ("RESET", r.RESET_p), ("CUSUM", r.CUSUM_p)] if v < ALPHA]
    if r.VIF_max > 10:
        fails.append("VIF")
    dg_rows.append(dict(modelo=mname, N=fi(r.n), DW=fm(r.DW, 2), BG4_p=fp(r.BG4_p), BP_p=fp(r.BP_p), JB_p=fp(r.JB_p), RESET_p=fp(r.RESET_p), CUSUM_p=fp(r.CUSUM_p),
                        VIF_max=fm(r.VIF_max, 1), fallan=", ".join(fails) if fails else "ninguno"))
P(mdt(pd.DataFrame(dg_rows)))
P(f"\nChow (ECM real): 2014Q1 p = {fp(rchow.loc['2014Q1', 'p'])}; 2020Q1 p = {fp(rchow.loc['2020Q1', 'p'])}; 2022Q3 p = {fp(rchow.loc['2022Q3', 'p'])}. "
  "El DOLS real de largo plazo falla autocorrelación, RESET y colinealidad: su inferencia es sólo indicativa.")
P("\n### 3.6 Corrección por búsqueda y predicción fuera de muestra\n")
P(f"Búsqueda de corto plazo con precio real: {fi(K_CP_REAL)} modelos (nominal: {fi(K_CP_NOM)}). Bonferroni con K = modelos que contienen cada término (columna K arriba). "
  f"Fuera de muestra (ventana expansiva, {fi(oos_r.loc['Preferido (R2aj)', 'n_oos'])} periodos): RMSE del preferido {fm(oos_r.loc['Preferido (R2aj)', 'RMSE'], 4)} frente a {fm(oos_r.loc['[ref] AR4+q', 'RMSE'], 4)} del AR(4) con dummies; "
  f"Diebold-Mariano (HAC) vs AR(4): p = {fp(oos_r.loc['Preferido (R2aj)', 'p vs AR4+q'])}. Con precio nominal: p = {fp(oos_n.loc['Preferido (R2aj)', 'p vs AR4+q'])}. No se puede afirmar que el modelo prediga mejor que un AR(4).")
P("\n### 3.7 Significatividad y signos frente a la literatura\n")
sg_show = SIGDF[SIGDF.bloque.str.startswith(("P1",))].copy()
P(mdt(pd.DataFrame(dict(bloque=sg_show.bloque, variable=sg_show.variable, coef=sg_show.coef.map(lambda x: fm(x, 4)), p=sg_show.p.map(fp), p_corregido=sg_show.p_corregido.map(fp),
                        esperado=sg_show.signo_esperado, coincide=sg_show.coincide))))
_sg = pd.DataFrame([dict(clase=k, signo_esperado=v[0], referencia=v[1]) for k, v in SIGNO.items()])
P("Signos esperados y referencias (docs/literatura.md, «Tabla: signos esperados»):")
P(mdt(_sg))
P("\nAnálisis de signos: el empleo y la persistencia del precio son las asociaciones más estables; el coste real tiene signo contrario al esperado y el tipo real es ≈ 0 en el largo plazo (relación estadística, no estructural). Tabla completa en `tablas/significatividad.csv`.")
fuente("f2/ecuacion_real.csv", "f2/largo_plazo.csv", "f2/ecm_preferido.csv", "f2/cointegracion.csv", "f2/real_diagnosticos.csv", "f2/real_chow.csv", "f2/real_oos_dm.csv", "f2/oos_dm.csv",
       "f2/comparacion_nominal_real.csv", "f2/real_busqueda_eba.csv", "tablas/ecuacion_final_lp.csv", "tablas/ecuacion_final_cp.csv", "tablas/ecuacion_replica_nominal.csv", "tablas/significatividad.csv")

# ---------------------------------------------------------------------------- P2
H("4. P2 - Inmigración (stock y flujo): ¿cuánto aporta y es causal?")
P("**Respuesta.** No es causal y no se documenta una aportación robusta al precio de compra. Hay una asociación positiva con el alquiler en OLS por CCAA que no sobrevive a la corrección por búsqueda ni al 2SLS, y con una pretendencia significativa en algunos grupos de países.")
P(f"**Nivel de evidencia: ASOCIACIÓN.** Justificación: el IV shift-share (Card 2001; cuotas de 2002) supera F ≥ 10 en todos los resultados, pero ningún efecto sobrevive al wild cluster bootstrap ni a Holm "
  f"(mínimo p Holm = {fp(MIN_HOLM_F3)} sobre {fi(n_f3)} especificaciones); el alquiler tiene pretendencia significativa; con {n_ccaa} clusters el J de Hansen tiene poca potencia y AKM/BHJ no son viables con tan pocos grupos de países. La condición de identificación (F > 10 + exclusión argumentada) no se cumple.")
P("\n### 4.1 Panel de CCAA, IV shift-share (efectos fijos de CCAA y año)\n")
mainiv = ppf[(ppf.spec == "FE")].copy()
mainiv = mainiv.merge(pe1[["resultado", "F_cluster"]], on="resultado", how="left")
mainiv["IC95"] = [f"[{fm(c - 1.96 * e, 2)}; {fm(c + 1.96 * e, 2)}]" for c, e in zip(mainiv.coef, mainiv.EE_cluster)]
P(mdt(pd.DataFrame(dict(resultado=mainiv.resultado, estimador=mainiv.est, N=mainiv.n.map(fi), coef=mainiv.coef.map(lambda x: fm(x, 3)), EE_cluster=mainiv.EE_cluster.map(lambda x: fm(x, 3)),
                        IC95_normal=mainiv.IC95, p_WCB=mainiv.p_WCB_restr.map(fp), F_1ª_etapa=mainiv.F_1a_etapa.map(lambda x: fm(x, 1))))))
ic = rd("f3/ic95_2sls_principal.csv")
P(f"\nIC95 % del 2SLS sobre IPV: [{fm(ic.IC95_lo[0], 2)}; {fm(ic.IC95_hi[0], 2)}] (según `f3/ic95_2sls_principal.csv`). Coeficiente = variación % del precio por cada punto porcentual de flujo neto de extranjeros sobre la población total.")
P("\n### 4.2 Nivel de evidencia por resultado (F3)\n")
P(mdt(nivel3.assign(p_pretend_min=nivel3.p_pretend_min.map(fp)).rename(columns={"F_ge10": "F≥10", "pretend_no_signif": "pretendencias no signif.", "J_no_rechaza": "J no rechaza", "sobrevive_WCB": "sobrevive WCB"})))
P("\n### 4.3 Series temporales nacionales (proyecciones locales, HAC)\n")
nl = rd("f3/nacional_lp.csv")
sel = nl[(nl.x == "x_ext") & nl.h.isin([0, 4, 8])]
P(mdt(pd.DataFrame(dict(resultado=sel.dep, h=sel.h, N=sel.n.map(fi), muestra=sel.muestra, coef=sel.coef.map(lambda x: fm(x, 4)), EE_HAC=sel.EE_HAC.map(lambda x: fm(x, 4)), p=sel.p.map(fp)))))
na = rd("f3/nacional_anual.csv")
a1 = na[(na.modelo == "A1_flujo_t") & (na["var"] == "tasa")].iloc[0]
a3 = na[(na.modelo == "A3_stock_t") & (na["var"] == "d_ln_pob_extranj")].iloc[0]
P(f"\nEn frecuencia anual (N = {fi(a1.n)}), el flujo contemporáneo da {ce(a1.coef, a1.EE_HAC4)} (p = {fp(a1.p)}) y el stock {ce(a3.coef, a3.EE_HAC4)} (p = {fp(a3.p)}); "
  f"tras Holm el p del flujo es {fp(c3.loc['NAC_ANUAL_A1_flujo_t', 'p_holm'])}. Con N tan pequeño no hay inferencia HAC fiable.")
P(f"\n**Corrección por búsqueda para la variable de interés (inmigración).** Menor p sin corregir = {fp(MIN_P_INM)}; Holm sobre {fi(n_f3)} (F3) = {fp(MIN_HOLM_F3)}; "
  f"Holm sobre las variantes de b2 de F5 = {fp(MIN_HOLM_F5)}; Bonferroni con el total de especificaciones del proyecto (K = {fi(N_TOTAL)}) = {fp(min(1.0, MIN_P_INM * N_TOTAL))}. No se calculó Romano-Wolf.")
P("\n### 4.4 Comparación con la literatura\n")
P("La literatura (Saiz 2007; González y Ortega 2013; Accetturo et al. 2014) apunta a efectos positivos sobre precios/alquileres; Sá (2015) obtiene un signo negativo en el Reino Unido. "
  f"El IC95 % del 2SLS sobre IPV ([{fm(ic.IC95_lo[0], 2)}; {fm(ic.IC95_hi[0], 2)}]) excluye las magnitudes de Saiz y González-Ortega; la diferencia se atribuye a diseño y periodo (2008+, peso de la cuota europea de 2002), no a un error. "
  "Las unidades no son directamente comparables (docs/literatura.md).")
P("\n### 4.5 Canal comprador\n")
P("El coeficiente 2SLS del canal comprador (compras de extranjeros residentes) es muy negativo incluso sin 2008-09 y se interpreta como posible violación de la exclusión; no se interpreta (docs/limitaciones.md).")
fuente("f3/panel_principal.csv", "f3/panel_primera_etapa.csv", "f3/nivel_evidencia.csv", "f3/correccion_busqueda.csv", "f3/nacional_lp.csv", "f3/nacional_anual.csv", "f3/ic95_2sls_principal.csv", "f5/correccion_busqueda_beta2.csv", "tablas/inmigracion_iv.csv")

# ---------------------------------------------------------------------------- P3
H("5. P3 - Elasticidad precio de la oferta y déficit acumulado (contraste con el BdE)")
P("**Respuesta.** (i) El déficit 2021-2025 es una cuenta contable (flujo acumulado de Δ hogares − viviendas terminadas) y sale por encima de la cifra del BdE; la diferencia se descompone en la fuente de hogares y en la vivienda protegida ausente de las terminadas MIVAU (libres). "
  "(ii) La elasticidad de la oferta es una asociación descriptiva débil, no una elasticidad estructural identificada.")
P("**Nivel de evidencia: DESCRIPTIVO (déficit: aritmética contable con fuentes oficiales) y ASOCIACIÓN DÉBIL/DESCRIPTIVA (elasticidad).** "
  f"Justificación de la elasticidad: la cointegración de la especificación principal es {int(c4i.n_rechazos)}/3, el ECM no es significativo (p = {fp(ecm4.p_ect)}), BG y RESET fallan, hay quiebre en 2014 y el IV solo es defendible con la renta como instrumento (ocupados y población extranjera afectan a la oferta).")
P("\n### 5.1 Déficit (flujo acumulado desde 2021)\n")
dshow = dv[dv.variante.isin(["(a) EPA corregida (PRINCIPAL)", "(a') EPA con Δ2021T1 = 0", "(a'') EPA sin corregir (solo referencia)", "(b) ECP 60131 (stock a 1 de enero)", "(c) Δparque MIVAU anual − Δhogares EPA corregida"])]
dshow = dshow[dshow.periodo.str.startswith("2021T1-2025T4") | dshow.periodo.eq("2021-2025")]
P(mdt(pd.DataFrame(dict(variante=dshow.variante, periodo=dshow.periodo, Δhogares=dshow.sum_delta_hogares.map(fi), terminadas=dshow.sum_terminadas.map(fi), déficit=dshow.deficit.map(fi),
                        pct_hogares_2025T4=dshow.pct_hogares_2025T4.map(lambda x: fm(x, 1))))))
P(f"\nExtensión de la variante principal a 2026T2: {fi(dv_main26.deficit)}. BdE (IA 2025): ≈ {fi(bde_def)}; IEF otoño 2025: ≈ {fi(bde_ief)}. "
  f"Diferencia con el BdE: {fi(dv_main.deficit - bde_def)}, de la cual {fi(dsc_i.loc['Δhogares 2021-2025', 'contribucion_a_deficit_nuestro_menos_BdE'])} por la fuente de hogares (EPA corregida frente a ECP a 1 de enero) y "
  f"{fi(dsc_i.loc['Terminadas 2021-2025', 'contribucion_a_deficit_nuestro_menos_BdE'])} por la vivienda protegida no incluida (inferencia nuestra; el BdE no nombra la operación estadística). "
  f"La corrección del salto de 2021T1 pesa {fi(dv_main.deficit - dv_raw.deficit)} viviendas: sin ella el déficit sería {fi(dv_raw.deficit)}. "
  "Es un flujo acumulado, no un déficit en niveles (requeriría un equilibrio inicial). La cifra de ~100.980 terminadas en 2024 citada en prensa es NO VERIFICADA.")
P("\n### 5.2 Elasticidad de la oferta (iniciadas libres, DOLS ±2, precio real retardado)\n")
cmpb = cb[(cb.k.isin([4, 8])) & (((cb.dep == "visados") & (cb.k == 4)) | ((cb.dep == "terminadas") & (cb.k == 8)) | ((cb.dep == "permisos") & (cb.k == 4)))]
cmpb = cmpb.assign(dep=cmpb.dep.replace({"visados": "iniciadas (código 'visados')"}))
P(mdt(pd.DataFrame(dict(variable=cmpb.dep, k=cmpb.k, estimador=cmpb.estimador, muestra=cmpb.muestra, N=cmpb.n.map(fi), beta=cmpb.beta.map(lambda x: fm(x, 2)), EE=cmpb.EE.map(lambda x: fm(x, 2)),
                        IC95=[f"[{fm(a, 2)}; {fm(b, 2)}]" for a, b in zip(cmpb.IC95_inf, cmpb.IC95_sup)], p_H0_045=cmpb["p_H0_beta=0.45"].map(fp)))))
P(f"\nLos DOLS en niveles son descriptivos (cointegración {int(c4i.n_rechazos)}/3 en la especificación principal). En Δ4 (válido con cualquier orden de integración) las iniciadas dan {ce(ols4.beta, ols4.EE_HAC8, 2)} y "
  f"**no se rechaza β = {fm(H0_045, 2)}**: p Holm = {fp(h045_v.loc['OLS Δ4 (HAC8)', 'p_holm_H0_045'])} (IV Δ4: p = {fp(h045_v.loc['IV Δ4', 'p_H0_045'])}). "
  f"Rango nacional de las {fi(n_nac4)} estimaciones de la familia: {fm(cnac.coef_interes.min(), 2)} a {fm(cnac.coef_interes.max(), 2)}. "
  "Sin ajuste de frecuencia/concepto la comparación con el BdE no es de igual a igual (ver 5.3).")
P("\n### 5.3 Comparación con el Banco de España\n")
P(f"- **Déficit:** BdE ≈ {fi(bde_def)} (IA 2025, p. 157); este trabajo {fi(dv_main.deficit)} (EPA corregida), {fi(dv_ecp.deficit)} (ECP a 1 de enero) y {fi(dv_pk.deficit)} (Δparque MIVAU).")
P(f"- **Elasticidad {fm(H0_045, 2)}:** cifra del IA 2025 (p. 156), que cita a Caldera y Johansson (2013) y Cavalleri, Cournède y Özsöğüt (2019): **ambas referencias NO VERIFICADAS** de forma independiente. "
  "Que el 0,45 sea la elasticidad de la inversión residencial es una **inferencia nuestra** (el BdE habla de una «elasticidad de la oferta a largo plazo» con modelos entre países, como cota superior). "
  f"Nuestra elasticidad de flujo en niveles ({fm(d4v.beta, 2)}) es varias veces mayor, pero no es comparable en concepto; en Δ4 no se rechaza {fm(H0_045, 2)}. La traducción de flujo a stock no se ha hecho: una elasticidad de flujo alta es compatible con una oferta de stock muy inelástica (aritmética en `f4/resumen_f4.md`).")
P(f"- **Signo de costes:** en iniciadas y terminadas el coste real tiene el signo esperado (negativo); en permisos es positivo ({fm(dols4.loc['dols_permisos_k4_ipv', 'beta_costes'], 2)}), contrario al esperado.")
P("\n### 5.4 Quiebres y estabilidad de la oferta\n")
P(f"Chow rechaza la estabilidad en 2014Q1 en las tres ecuaciones de oferta (p entre {fp(chow4[chow4.fecha == '2014Q1'].p.min())} y {fp(chow4[chow4.fecha == '2014Q1'].p.max())}); Bai-Perron: "
  + "; ".join(f"{r.dep} ({r.fechas})" for r in bp4.itertuples()) + ".")
fuente("f4/deficit_variantes.csv", "f4/comparacion_bde_deficit.csv", "f4/descomposicion_diferencia_bde.csv", "f4/contraste_bde.csv", "f4/contraste_H0_045_principales.csv", "f4/ols_delta4.csv", "f4/cointegracion.csv", "f4/ecm_resultados.csv", "f4/chow.csv", "f4/bai_perron.csv", "tablas/deficit.csv", "f4/resumen_f4.md")

# ---------------------------------------------------------------------------- P4
H("6. P4 - Heterogeneidad entre CCAA y Comunitat Valenciana / València")
P(f"**Respuesta.** No se detecta heterogeneidad entre CCAA con el panel disponible (lo que no prueba homogeneidad: el límite de aleatorización con {n_ccaa} clusters es 1/{n_ccaa}). "
  "La Comunitat Valenciana solo difiere en lo descriptivo y el signo depende de la medida de precio (IPV frente a valor tasado). Para València (municipio) hay una comparativa con HAC sobre el valor tasado (N ≥ 40) y el resto es descriptivo.")
P("**Nivel de evidencia: ASOCIACIÓN (panel CCAA) y DESCRIPTIVO (València).** Justificación: ningún efecto de la cuota de extranjeros sobrevive a Holm en el panel; las series de València con N < 40 no admiten inferencia; la beta de València frente a España es un promedio inestable con diagnósticos que fallan y componente parte-todo. No hay identificación.")
P("\n### 6.1 Panel de CCAA (F5): FE CCAA + año, Δln IPV\n")
P(mdt(pd.DataFrame(dict(variable=fe5.index, coef=fe5.coef.map(lambda x: fm(x, 4)), EE_cluster=fe5.EE_cluster.map(lambda x: fm(x, 4)), p_cluster=fe5.p_cluster.map(fp), p_DK=fe5.p_DK_bw2.map(fp), p_wild_Webb=fe5.p_wild_Webb.map(fp)))))
P(f"\nN = {fi(N_F5)}, {n_ccaa} CCAA, {MUESTRA_F5}. EE cluster por CCAA ({n_ccaa} clusters), Driscoll-Kraay y wild cluster bootstrap. Alineación temporal de b2: "
  + "; ".join(f"{r['alineacion de la cuota']}: {fm(r['b2 en %/pp'], 2)} %/pp (p wild {fp(r.p_wild_Webb)})" for _, r in tt.iterrows())
  + f". Holm sobre las {len(cb5)} variantes de b2: mínimo {fp(MIN_HOLM_F5)} (nada es significativo tras la corrección). "
  f"Poolability: F = {fm(pool.F, 2)}, p clásico {fp(pool.p_clasico)}, p wild {fp(pool.p_wild_Webb)}. Terminadas retardadas: signo positivo, contrario al esperado (p wild {fp(fe5.loc['b4 terminadas/1000 hab (t-1)', 'p_wild_Webb'])}). "
  "El test CD de Pesaran no es interpretable sobre residuos de FE bidireccional/CCE (Juodis y Reese 2022).")
P("\n### 6.2 Comunitat Valenciana frente a España (descriptivo)\n")
P(mdt(pd.DataFrame(dict(periodo=vcv.periodo, serie=vcv.serie, CV_acum_pct=vcv["crec_acum_CV_%"].map(lambda x: fm(x, 1)), España_acum_pct=vcv["crec_acum_Espana_%"].map(lambda x: fm(x, 1)), dif_pp=vcv.dif_pp.map(lambda x: fm(x, 1))))))
P("\n### 6.3 València (valor tasado, N ≥ 40): beta de Δ4 frente a comparadores\n")
P(mdt(pd.DataFrame(dict(modelo=bt.modelo, maxlags=bt.maxlags.map(fi), N=bt.N.map(fi), beta=bt.beta.map(lambda x: fm(x, 3)), EE_HAC=bt.EE_HAC.map(lambda x: fm(x, 3)), IC95=[f"[{fm(a, 2)}; {fm(b, 2)}]" for a, b in zip(bt.IC95_inf, bt.IC95_sup)], p_beta1=bt.p_beta_igual_1.map(fp)))))
P("\nPor tramos (interacciones, HAC8; EE aproximados por tener 24-26 trimestres efectivos por tramo):\n")
P(mdt(pd.DataFrame(dict(modelo=bpt.modelo, tramo=bpt.tramo, N=bpt.N_tramo.map(fi), beta=bpt.beta.map(lambda x: fm(x, 2)), EE_HAC=bpt.EE_HAC.map(lambda x: fm(x, 2)), p_beta1=bpt.p_beta_igual_1.map(fp)))))
P(f"\nDiferencial medio de crecimiento por tramo (pp/año): " + "; ".join(f"{r.modelo} {r.tramo}: {fm(r.dif_media_pp, 1)} (EE {fm(r.EE_HAC, 1)})" for r in dnt[dnt.modelo == 'València_vs_España'].itertuples())
  + f". Crecimiento acumulado del valor tasado 2020-2026Q2: València {fm(ca.loc['2020-2026Q2', 'València'], 1)} %, CV {fm(ca.loc['2020-2026Q2', 'C. Valenciana'], 1)} %, España {fm(ca.loc['2020-2026Q2', 'España'], 1)} %; "
  f"con el IPV del INE la CV ({fm(ivt.loc['ipv_CV', '2019Q4->2026Q2_%'], 1)} %) y España ({fm(ivt.loc['ipv_ES', '2019Q4->2026Q2_%'], 1)} %) casi no difieren: el exceso es sobre todo del valor tasado (composición de lo tasado). "
  f"Cuota de compradores extranjeros CV superior a España en {fi(cuota['trimestres con CV > ES'])} de {fi(cuota['N'])} trimestres (hecho descriptivo; no se cita el p-valor numérico).")
P(f"\nDiagnósticos de los {fi(len(dc6))} modelos beta (Δ4): p máximos entre modelos de BG(4) = {fp(dc6.BG4_p.max())}, RESET = {fp(dc6.RESET_p.max())}, CUSUM = {fp(dc6.CUSUM_p.max())} "
  f"({'todos por debajo de' if max(dc6.BG4_p.max(), dc6.RESET_p.max(), dc6.CUSUM_p.max()) < ALPHA else 'no todos por debajo de'} {fm(ALPHA, 2)}); la beta es un promedio inestable y no debe leerse como parámetro estructural.")
fuente("f5/tabla_fe_principal.csv", "f5/timing_b2.csv", "f5/poolability.csv", "f5/correccion_busqueda_beta2.csv", "f5/valencia_vs_espana.csv", "f6/beta_todos.csv", "f6/beta_por_tramos.csv", "f6/diferencial_nivel_por_tramos.csv",
       "f6/crecimiento_acumulado_p_tasado.csv", "f6/ipv_vs_tasado_acumulado.csv", "f6/cuota_extranjeros_inferencia.csv", "f6/diagnosticos_beta.csv", "tablas/panel_ccaa.csv", "tablas/valencia.csv")

# ---------------------------------------------------------------------------- P5
H("7. P5 - Quiebres (2008, 2014, 2020, 2022) y estabilidad del modelo")
_rej = [f for f in rchow.index if rchow.loc[f, "p"] < ALPHA]
_nrej = [f for f in rchow.index if rchow.loc[f, "p"] >= ALPHA]
P(f"**Respuesta.** Chow rechaza la estabilidad en el ECM real en {', '.join(_rej) if _rej else 'ninguna fecha candidata'} y no la rechaza en {', '.join(_nrej) if _nrej else 'ninguna'}; Bai-Perron fecha {fi(rbp.loc['LR real (niveles)', 'n_quiebres'])} quiebres en el largo plazo en niveles ({rbp.loc['LR real (niveles)', 'fechas']}). La corrección de error es inestable: el modelo no es estable.")
P("**Nivel de evidencia: DESCRIPTIVO (diagnóstico de estabilidad; contrastes con fechas candidatas y fechas estimadas, sin identificación).** Los contrastes de Chow con fechas candidatas elegidas ex ante se complementan con Bai-Perron (fechas estimadas), cuya inferencia no es estándar.")
P("\n### 7.1 Chow y Bai-Perron\n")
P(mdt(pd.DataFrame(dict(fecha=rchow.index, F=rchow.F.map(lambda x: fm(x, 2)), p_ECM_real=rchow.p.map(fp), p_ECM_nominal=[fp(nchow.loc[f, "p"]) for f in rchow.index], n1=rchow.n1.map(fi), n2=rchow.n2.map(fi)))))
P(f"\nBai-Perron (ruptures): ECM real preferido: {fi(rbp.loc['ECM real preferido', 'n_quiebres'])} quiebres; largo plazo real en niveles: {rbp.loc['LR real (niveles)', 'fechas']}. Oferta (F4): " + "; ".join(f"{r.dep} ({r.fechas})" for r in bp4.itertuples()) + ".")
P("\n### 7.2 Estabilidad del término de corrección del error\n")
rows_e = []
for lab, key in [("Muestra completa", "Preferido real"), ("Con dummies EPA2021 y tipos 2022", "+ epa21 (quiebre_epa_2021) + tipo22 (escalón 2022Q3)"), ("Con escalones Bai-Perron", "+ escalones Bai-Perron"),
                 ("Desde 2014Q1", "2014Q1-2026Q2"), ("Pre-COVID (≤2019Q4)", "Pre-COVID (≤2019Q4; ect re-estimado)")]:
    r = rrob.loc[key]
    rows_e.append(dict(muestra=lab, N=fi(r.N), ect=ce(*parse_ce(r.ect), 4), p=fp(r.p_ect), R2_aj=fm(r.R2_aj, 3), BG4_p=fp(r.BG4_p), RESET_p=fp(r.RESET_p)))
P(mdt(pd.DataFrame(rows_e)))
P(f"\nEl ect recursivo pasa de {fm(ectrec.loc['2019Q4', 'coef_ect'], 3)} (hasta 2019Q4) a {fm(ectrec.iloc[-1].coef_ect, 3)} (hasta {ectrec.index[-1]}). Por subperiodos, el DOLS cambia de signo en costes y permisos antes de 2020 (`f2/dols_subperiodos.csv`). "
  "Los escalones de 2021 (EPA) y de 2022 (tipos) no son significativos en el ECM real.")
fuente("f2/real_chow.csv", "f2/chow.csv", "f2/real_bai_perron.csv", "f2/real_robustez.csv", "f2/ect_recursivo.csv", "f2/dols_subperiodos.csv", "f4/chow.csv", "f4/bai_perron.csv", "f6/quiebres_wald_hac.csv")

# ---------------------------------------------------------------------------- robustez
H("8. Robustez de los coeficientes clave")
P(REGLA_ROBUSTEZ)
rshow = ROBDF[["coeficiente", "muestra_completa", "pre_COVID", "desde_2014", "dummies_EPA21_tipos22", "nominal", "real", "precio_valor_tasado", "otra_especificacion_1", "otra_especificacion_2", "¿sobrevive?"]]
P(mdt(rshow))
P("\nLeyenda: cada celda es coef (EE) [p]; '{..}' indica la especificación de origen; '~' = p aproximado por la normal; 'n/d' = no estimado. Motivo de la clasificación y advertencias en `tablas/robustez.csv`.")
PL([f"**{r.coeficiente}:** {r['¿sobrevive?']} ({r.motivo_regla}). {r.advertencia}" for _, r in ROBDF.iterrows()])
fuente("tablas/robustez.csv")

# ---------------------------------------------------------------------------- limitaciones
H("9. Limitaciones (priorizadas)")
P("Prioridad según su efecto sobre la inferencia de P1-P5 (1 = invalida lecturas causales o la estabilidad; 2 = condiciona magnitudes; 3 = datos). Texto de `docs/limitaciones.md`.")
PRIO = [("F3", "1 (identificación de P2)"), ("F2 (", "1 (estabilidad y selección de P1/P5)"), ("F2 —", "1 (estabilidad y selección de P1/P5; precio real)"),
        ("F4", "2 (magnitudes de P3)"), ("F5", "2 (alcance de P4)"), ("Datos", "3 (datos)")]
ordered = []
for pref, lab in PRIO:
    for k, v in LIMS.items():
        if k.startswith(pref) and not k.startswith("Resueltos"):
            ordered.append((lab, k, v))
ordered.sort(key=lambda x: x[0])
for lab, k, v in ordered:
    P(f"**Prioridad {lab} · {k}**")
    PL(v)
fuente("docs/limitaciones.md")

# ---------------------------------------------------------------------------- qué NO se puede afirmar
H("10. Qué NO se puede afirmar")
P(f"1. Que la inmigración **cause** subidas de precios (o de alquileres): el IV no sobrevive al wild cluster bootstrap ni a Holm (mínimo {fp(MIN_HOLM_F3)}) y el alquiler tiene pretendencia significativa.")
P(f"2. Que el modelo del precio **prediga mejor que un AR(4)**: DM p = {fp(oos_r.loc['Preferido (R2aj)', 'p vs AR4+q'])} (real) y {fp(oos_n.loc['Preferido (R2aj)', 'p vs AR4+q'])} (nominal), y RMSE del preferido {'mayor' if oos_r.loc['Preferido (R2aj)', 'RMSE'] > oos_r.loc['[ref] AR4+q', 'RMSE'] else 'menor'} que el del AR(4) (real).")
P(f"3. Que la **elasticidad de la oferta esté identificada**: cointegración {int(c4i.n_rechazos)}/3, ECM no significativo, IV solo defendible con la renta; en Δ4 no se rechaza {fm(H0_045, 2)}.")
P(f"4. Que exista un **equilibrio de largo plazo estable**: cointegración nominal {int(cn.n_rechazos)}/3; real {int(cr.n_rechazos)}/3 pero el ect pasa de {fm(ect_pre_c, 3)} (pre-COVID, p = {fp(real_ect_pre['p_ect'])}) a {fm(CPR.loc['ect_l1', 'coef'], 3)}; costes y tipo con signos no esperados; Bai-Perron: {rbp.loc['LR real (niveles)', 'fechas']}.")
P("5. **Efectos causales en València** (ni de la inmigración, ni del turismo, ni de ninguna otra variable): la comparativa es descriptiva y la beta es inestable con componente parte-todo.")
P(f"6. Que cualquier coeficiente individual del corto plazo sea la «verdadera» especificación: el preferido gana en el {fm(100 * frec_pref, 1)} % de las réplicas del bootstrap de la selección y tras Bonferroni: {BONF_TXT}")
P(f"7. Que la **heterogeneidad entre CCAA sea nula**: solo que no se detecta (p wild de poolability = {fp(pool.p_wild_Webb)}; límite de aleatorización 1/{n_ccaa}).")
P(f"8. Que el **déficit sea exactamente** {fi(bde_def)} o {fi(dv_main.deficit)}: depende de la fuente de hogares (rango {fi(min(dv_ecp.deficit, dv_pk.deficit, dv_a0.deficit, dv_main.deficit))}-{fi(max(dv_ecp.deficit, dv_pk.deficit, dv_a0.deficit, dv_main.deficit))} entre variantes con corrección) y de la ausencia de protegidas.")
P("9. Que las referencias Caldera-Johansson (2013) y Cavalleri et al. (2019) respalden el 0,45 del BdE: NO VERIFICADAS de forma independiente.")

# ---------------------------------------------------------------------------- búsqueda
H("11. Número total de especificaciones probadas y corrección por búsqueda")
P(f"**Total: {fi(N_TOTAL)} especificaciones registradas** en `output/registro_busqueda.csv` (concatenación de las fases F2-F6, con columnas `fase`, `n_total_fase` y `n_total_registro`).")
P(mdt(pd.DataFrame(dict(fase=POR_FASE.index, especificaciones=[fi(v) for v in POR_FASE.values]))))
P(f"\nDe las {fi(POR_FASE.get('F2', 0))} de F2, {fi(K_CP_NOM)} son la búsqueda de corto plazo nominal y {fi(K_CP_REAL)} la real (candidatos cerrados antes de estimar). Correcciones aplicadas: Bonferroni por término con K de la búsqueda (F2), Holm sobre {fi(n_f3)} (F3), "
  f"Holm sobre {fi(len(cb5))} variantes de b2 (F5), Holm sobre {fi(len(corr4))} modelos de elasticidad y sobre las {fi(len(h045))} hipótesis β = {fm(H0_045, 2)} (F4) y Holm sobre {fi(len(rd('f6/correccion_holm.csv')))} contrastes (F6). "
  "No se calculó Romano-Wolf. Las 'correcciones' del registro son parciales: condicionales a los p-valores válidos y no cubren la elección de la muestra ni del precio (nominal/real).")
fuente("registro_busqueda.csv", "f3/correccion_busqueda.csv", "f4/correccion_busqueda.csv", "f5/correccion_busqueda_beta2.csv", "f6/correccion_holm.csv")

# ---------------------------------------------------------------------------- referencias (se calculan con el texto anterior)
body = "\n".join(L)
alltext = body
for f in sorted(OUT.glob("f[2-6]/*.md")):
    alltext += "\n" + f.read_text(encoding="utf-8")


def _norm(t: str) -> str:
    return _ascii(t)


body_n = _norm(body)
md_files = {f"output/{p.parent.name}/{p.name}": _norm(p.read_text(encoding="utf-8")) for p in sorted(OUT.glob("f[2-6]/*.md"))}
md_files.update({f"output/tablas/{p.name}": _norm(p.read_text(encoding="utf-8")) for p in sorted(TAB.glob("*.csv")) if p.name != "referencias.csv"})


def cited_in(e):
    pats = []
    for y in e["años"]:
        for a in e["apellidos"]:
            pats.append(re.escape(_norm(a)) + r"[^\n]{0,60}?" + y)
    if e["apellidos"] == ["Banco de España"]:
        pats += [r"informe anual 2025", r"\bia 2025"] if "Informe Anual" in e["clave"] else [r"ief otono 2025", r"informe de estabilidad financiera"]
    hits = []
    if any(re.search(p, body_n) for p in pats):
        hits.append("informe")
    for name, tx in md_files.items():
        if any(re.search(p, tx) for p in pats):
            hits.append(name)
    return hits


refs = []
for e in LITENT:
    hits = cited_in(e)
    if hits:
        refs.append(dict(referencia=e["clave"], marca=e["marca"], origen_en_literatura=e["origen"], citada_en="; ".join(hits[:8]) + (" ..." if len(hits) > 8 else ""), detalle=e["detalle"]))
# citas "Autor (año)" que no figuran en literatura.md
known = {(_norm(a), y) for e in LITENT for a in e["apellidos"] for y in e["años"]}
found = set(re.findall(r"([A-ZÁÉÍÓÚ][a-záéíóúñü\-]+(?:[ -][A-Z][a-záéíóúñü]+)?(?: et al\.)?) \((\d{4})[ab]?\)", alltext))
missing = []
for a, y in sorted(found):
    toks = [t for t in re.split(r"[- ]| y ", _norm(a.replace(" et al.", ""))) if t]
    if not any((t, y) in known for t in toks):
        missing.append((a, y))
for a, y in missing:
    refs.append(dict(referencia=f"{a} ({y})", marca="NO VERIFICADA", origen_en_literatura="no figura en docs/literatura.md",
                     citada_en="detectada por patrón 'Autor (año)' en output/ o informe", detalle="revisar manualmente"))
REFDF = pd.DataFrame(refs).sort_values("referencia").reset_index(drop=True)
save_csv(REFDF, "referencias.csv")

H("12. Referencias citadas (marca de verificación)")
P("Marca según `docs/literatura.md`: VERIFICADA (comprobada contra Crossref/IDEAS/PDF oficial), PARCIAL (DOI, páginas o versión sin comprobar) y NO VERIFICADA. "
  "Se listan solo las referencias citadas en este informe o en los resúmenes de `output/`.")
cnt = REFDF.marca.value_counts()
P(f"Total: {fi(len(REFDF))} (VERIFICADA: {fi(cnt.get('VERIFICADA', 0))}; PARCIAL: {fi(cnt.get('PARCIAL', 0))}; NO VERIFICADA: {fi(cnt.get('NO VERIFICADA', 0))}).\n")
PL([f"[{r.marca}] {r.referencia}" for _, r in REFDF.iterrows()])
fuente("tablas/referencias.csv", "docs/literatura.md")

TXT = "\n\n".join(L).strip() + "\n"
TXT = TXT.replace("= <0,001", "< 0,001").replace("=<0,001", "<0,001")
TXT = re.sub(r"\n{3,}", "\n\n", TXT)
(OUT / "informe.md").write_text(TXT, encoding="utf-8")
print(f"report: informe.md ({len(L)} bloques), {len(list(TAB.glob('*.csv')))} tablas, registro con {N_TOTAL} especificaciones")
