"""K2 (v6.1): reconciliacion de la inmigracion entre versiones, analisis «una dimension cada vez». Determinista, sin red.

SEED=20261010, un hilo. Lee solo entrenamiento (holdout.load_train via v2_common) y output/v6/M0/paneles (entrenamiento) y
data/processed. NO abre data/sealed ni usa evaluacion sellada. Capa maxima C4; nada causal.

Salidas (output/v6_1/K2): registro.csv (Registry), registro_holm.csv, pasos_inmigracion.csv, inmigracion.md,
otros_cambios.md (con k2_otros), resultado.json, hechos.json, que_cambio.md.

Uso: python3 src/v6_1/k2_inmigracion.py [--smoke]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import k2_datos as kd  # noqa: E402
import k2_lib as kl  # noqa: E402

RAIZ = AQUI.parents[1]
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
FECHA = "2026-10-11"
SMOKE = "--smoke" in sys.argv
OUT = RAIZ / ("output/v6_1/K2/smoke" if SMOKE else "output/v6_1/K2")
OUT.mkdir(parents=True, exist_ok=True)
REG = Registry(OUT / "registro.csv")

FILAS: list[dict] = []
CTX: dict = {}


# ------------------------------------------------------------------ especificaciones
def spec(**kw):
    s = dict(ya="y_alq", yc="y_pre", xs=["x"], ctrl=[], z=None, a0=2009, a1=2021, fe="dobles", cl="cod",
             k=1.0, nivel="provincia", medida_alq="IPC alquiler (stock)", medida_precio="valor tasado MIVAU",
             metodo="", xdef="", extra=None, unidad_x="+1 pp", desc_y="", nota="")
    s.update(kw)
    return s


def _need(s, mercado):
    y = s["ya"] if mercado == "alquiler" else s["yc"]
    cols = [y] + list(s["xs"]) + list(s["ctrl"]) + ([s["z"]] if s["z"] else []) + ["cod", "anio", s["cl"]]
    return [c for c in cols if c is not None]


def _frame(U, s, mask=None):
    m = U[U["anio"].between(s["a0"], s["a1"])]
    if mask is not None:
        m = m[mask.reindex(m.index, fill_value=False)]
    return m


def _extra(m, s):
    ex = s.get("extra")
    if not ex:
        return None
    parts = []
    for kind in ex:
        var, tag = {"costa_anio": ("costa6", "costa"), "nop_anio": ("pct_no_principal_2021", "nop"),
                    "nores_anio": ("nores_1516", "nores")}[kind]
        parts.append(kd.dummies_x(m.assign(**{var: m[var].fillna(0)}), var, tag) if var in m else None)
    return pd.concat(parts, axis=1) if parts else None


def estimar(U, s, mercado, mask=None):
    """Estima una especificacion en un mercado. Devuelve dict de resultado (o None)."""
    y = s["ya"] if mercado == "alquiler" else s["yc"]
    if y is None:
        return None
    m = _frame(U, s, mask)
    need = [c for c in _need(s, mercado)]
    ex_needs = []
    for kind in (s.get("extra") or []):
        ex_needs.append({"costa_anio": "costa6", "nop_anio": "pct_no_principal_2021", "nores_anio": "nores_1516"}[kind])
    m = m.dropna(subset=need + ex_needs)
    if len(m) < 30:
        return None
    ex = _extra(m, s)
    r = kl.fit(m, y, s["xs"], s["ctrl"], fe=s["fe"], z=s["z"], cl=s["cl"], extra=ex)
    return r


def fila(r, s, mercado, **kw):
    """Convierte el resultado en fila de tabla con unidades interpretables."""
    medida = s["medida_alq"] if mercado == "alquiler" else s["medida_precio"]
    k = s["k"]
    ref = CTX["renta_media"] if mercado == "alquiler" else CTX["precio_medio"]
    unidad_abs = "EUR/mes" if mercado == "alquiler" else "EUR/m2"
    f = dict(mercado=mercado, medida=medida, nivel=s["nivel"], periodo=f"{s['a0']}-{s['a1']}", metodo=s["metodo"],
             x=s["xs"][0], unidad_x=s["unidad_x"], controles=",".join(s["ctrl"] + (s.get("extra") or [])) or "ninguno",
             efectos_fijos=s["fe"], cluster=s["cl"], y=(s["ya"] if mercado == "alquiler" else s["yc"]))
    if r is None:
        f.update(N=0, G=0, coef=np.nan, se=np.nan, lo=np.nan, hi=np.nan, p=np.nan, coef_abs=np.nan, F1=np.nan)
    else:
        f.update(N=r["N"], G=r["G"], coef=r["coef"] * k, se=r["se"] * k, lo=r["lo"] * k, hi=r["hi"] * k, p=r["p"],
                 coef_abs=r["coef"] * k * ref / 100, F1=r["F1"])
    f["unidad_coef"] = "% de la medida por " + s["unidad_x"]
    f["unidad_abs"] = unidad_abs
    f.update(kw)
    return f


def registrar(f, bloque, via, paso, dimension, nota=""):
    f.update(bloque=bloque, via=via, paso=paso, dimension=dimension, nota=nota)
    f["id"] = f"{bloque}|{via}|{paso}|{f['mercado']}"
    FILAS.append(f)
    ym = f["periodo"].split("-")
    REG.log("K2", f["id"], f"{f['y']}~{f['x']}+{f['controles']} (EF {f['efectos_fijos']}, {f['metodo']})", ym[0], ym[1],
            f["N"], np.nan, np.nan, np.nan, np.nan, f["coef"], f["p"], f"{f['medida']}; {f['nivel']}; C4; {nota}")
    return f


def correr(U, s, bloque, via, paso, dimension, mercados=("alquiler", "compra"), mask=None, nota="", extra_cols=None):
    out = {}
    for mk in mercados:
        r = estimar(U, s, mk, mask)
        f = fila(r, s, mk)
        if extra_cols:
            f.update(extra_cols)
        out[mk] = registrar(f, bloque, via, paso, dimension, nota)
    return out


def comunes(U, s_prev, s_new, mercado):
    """Filas validas para ambas especificaciones (misma muestra) dentro del periodo de la nueva."""
    def ok(s):
        y = s["ya"] if mercado == "alquiler" else s["yc"]
        c = [y] + list(s["xs"]) + list(s["ctrl"]) + ([s["z"]] if s["z"] else [])
        ex = [{"costa_anio": "costa6", "nop_anio": "pct_no_principal_2021", "nores_anio": "nores_1516"}[k]
              for k in (s.get("extra") or [])]
        return U[c + ex].notna().all(axis=1)
    return ok(s_prev) & ok(s_new)


def paso_encadenado(U, prev, new, bloque, paso, dimension, mismo_periodo=True):
    """Calcula `new` y `prev` en la MISMA muestra (cuando solo cambia una dimension distinta del periodo)."""
    res = {}
    for mk in ("alquiler", "compra"):
        mask = None
        sp = dict(prev)
        if mismo_periodo:
            sp["a0"], sp["a1"] = new["a0"], new["a1"]
            mask = comunes(U, sp, new, mk)
        r_new = estimar(U, new, mk, mask)
        r_prev = estimar(U, sp, mk, mask)
        f = fila(r_new, new, mk)
        fp = fila(r_prev, sp, mk)
        f.update(coef_anterior_misma_muestra=fp["coef"], ic_anterior=f"[{fp['lo']:.2f}; {fp['hi']:.2f}]",
                 N_anterior=fp["N"])
        res[mk] = registrar(f, bloque, "acumulado", paso, dimension,
                            "anterior estimado en la misma muestra" if mismo_periodo else
                            "el periodo cambia: la muestra no es comun")
    return res


# ------------------------------------------------------------------ bloque 1: camino acumulado v1-v3 -> v6
def camino(U):
    B = "inmigracion"
    P0 = spec(est="2SLS", z="z", metodo="2SLS shift-share (cuotas 2002), EF prov+anio", xdef="flujo/poblacion t-1",
              unidad_x="+1 pp de poblacion (flujo)", desc_y="variacion anual %")
    P1 = {**P0, "z": None, "metodo": "MCO, EF prov+anio"}
    P2 = {**P1, "xs": ["x_stock"], "xdef": "crecimiento del stock de extranjeros (pp de pob.)",
          "unidad_x": "+1 pp de poblacion (variacion del stock)"}
    P3 = {**P2, "xs": ["d_cuota"], "xdef": "variacion de la cuota de extranjeros", "unidad_x": "+1 pp de cuota (variacion)"}
    P4 = {**P3, "xs": ["l1_cuota"], "ya": "lv_ipc2", "yc": "lv_tas2", "metodo": "MCO niveles ln, EF prov+anio (v6)",
          "xdef": "cuota de extranjeros t-1 (nivel)", "unidad_x": "+1 pp de cuota (nivel, t-1)"}
    P5 = {**P4, "a0": 2016, "a1": 2023}
    P6 = {**P5, "ya": "lv_ser2", "medida_alq": "SERPAVI VC (stock)"}
    P7 = {**P6, "xs": ["l1_share_ext_pob"], "ya": "lv_alq6", "yc": "lv_tas6", "xdef": "cuota de extranjeros t-1 (panel v6)"}
    P8 = {**P7, "ctrl": ["l1_ln_pob"], "metodo": "MCO niveles ln, EF prov+anio, + poblacion"}
    P9 = {**P8, "ctrl": kd.NUCLEO, "metodo": "MCO niveles ln, EF prov+anio, + nucleo de M2"}
    P10 = {**P9, "a1": 2024}
    cadena = [
        ("P0", "base v2-BI (reproducida en las provincias de entrenamiento v6)", P0, None),
        ("P1", "metodo: 2SLS -> MCO", P1, "metodo"),
        ("P2", "definicion: flujo -> variacion del stock", P2, "definicion"),
        ("P3", "definicion: stock -> variacion de la cuota", P3, "definicion"),
        ("P4", "metodo: primeras diferencias -> niveles con EF dobles", P4, "metodo"),
        ("P5", "periodo: 2009-2021 -> 2016-2023", P5, "periodo"),
        ("P6", "medida de alquiler: IPC -> SERPAVI", P6, "medida"),
        ("P7", "fuente: panel v2 -> panel v6 (mismos conceptos)", P7, "fuente de datos"),
        ("P8", "controles: + poblacion (ln, t-1)", P8, "controles"),
        ("P9", "controles: + nucleo de M2 (renta, paro, ocupados, oferta, hipotecas)", P9, "controles"),
        ("P10", "periodo: compra hasta 2024 (alquiler hasta 2023)", P10, "periodo"),
    ]
    prev = None
    for pid, desc, s, dim in cadena:
        if prev is None:
            correr(U, s, B, "acumulado", pid, desc)
        else:
            paso_encadenado(U, prev, s, B, pid, desc, mismo_periodo=(dim != "periodo"))
        prev = s
    CTX["P"] = {pid: s for pid, _, s, _ in cadena}
    return cadena


# ------------------------------------------------------------------ bloque 2: una dimension desde la base MCO
def una_dimension(U, meta):
    B = "inmigracion"
    base = spec(metodo="MCO, EF prov+anio", unidad_x="+1 pp de poblacion (flujo)")
    CTX["base"] = base

    def vs_base(nombre, new, dimension, mercados=("alquiler", "compra")):
        for mk in mercados:
            sb = dict(base)
            sb["a0"], sb["a1"] = new["a0"], new["a1"]
            mask = comunes(U, sb, new, mk)
            rb = estimar(U, sb, mk, mask)
            rn = estimar(U, new, mk, mask)
            f = fila(rn, new, mk)
            fb = fila(rb, sb, mk)
            f.update(coef_anterior_misma_muestra=fb["coef"], ic_anterior=f"[{fb['lo']:.2f}; {fb['hi']:.2f}]",
                     N_anterior=fb["N"])
            registrar(f, B, "una_dimension", nombre, dimension, "base (MCO EF dobles, flujo) en la misma muestra")

    # (a) definicion
    vs_base("def_dstock", {**base, "xs": ["x_stock"], "unidad_x": "+1 pp de poblacion (variacion del stock)"}, "definicion")
    vs_base("def_dcuota", {**base, "xs": ["d_cuota"], "unidad_x": "+1 pp de cuota (variacion)"}, "definicion")
    vs_base("def_cuota_t1", {**base, "xs": ["l1_cuota"], "unidad_x": "+1 pp de cuota (nivel t-1, desenlace en variacion)"},
            "definicion")
    # (c) periodo
    for a0, a1 in [(2009, 2014), (2015, 2021), (2009, 2019)]:
        vs_base(f"periodo_{a0}_{a1}", {**base, "a0": a0, "a1": a1}, "periodo")
    # (e) metodo
    for fe, txt in [("pooled", "MCO pooled (sin EF)"), ("unidad", "MCO EF provincia"), ("anio", "MCO EF anio"),
                    ("dobles_tend", "MCO EF dobles + tendencia por provincia")]:
        vs_base(f"metodo_{fe}", {**base, "fe": fe, "metodo": txt}, "metodo")
    vs_base("metodo_2sls", {**base, "z": "z", "metodo": "2SLS shift-share"}, "metodo")
    vs_base("metodo_2sls_pob", {**base, "z": "z", "ctrl": ["ln_pop_l"], "metodo": "2SLS shift-share + ln poblacion"},
            "colinealidad con poblacion")
    vs_base("mco_pob", {**base, "ctrl": ["ln_pop_l"], "metodo": "MCO + ln poblacion t-1"}, "colinealidad con poblacion")
    # (d) medida de alquiler y de precio (muestras comunes entre medidas)
    vs_base("alq_serpavi", {**base, "ya": "y_alq_ser", "medida_alq": "SERPAVI VC (stock)"}, "medida alquiler",
            mercados=("alquiler",))
    sb_alq = {**base, "a0": 2012, "a1": 2021}
    sn = {**sb_alq, "ya": "y_alq_ser", "medida_alq": "SERPAVI VC (stock)"}
    for mk in ("alquiler",):
        mask = comunes(U, sb_alq, sn, mk)
        f1 = fila(estimar(U, sb_alq, mk, mask), sb_alq, mk)
        f2 = fila(estimar(U, sn, mk, mask), sn, mk)
        registrar(f1, B, "una_dimension", "medida_alq_IPC_muestra_comun", "medida alquiler", "muestra comun IPC/SERPAVI 2012-2021")
        registrar(f2, B, "una_dimension", "medida_alq_SERPAVI_muestra_comun", "medida alquiler",
                  "muestra comun IPC/SERPAVI 2012-2021")
    # precio: tasado real (v2), tasado nominal, Registradores, IPV (cluster CCAA)
    base_p = {**base, "a0": 2016, "a1": 2021}
    opciones = [("tasado_real", "yc", "y_pre", "valor tasado MIVAU (real)", "cod"),
                ("tasado_nominal", "yc", "y_pre_nom", "valor tasado MIVAU (nominal)", "cod"),
                ("registradores", "yc", "y_pre_reg", "Registradores (m2)", "cod"),
                ("ipv_ine", "yc", "y_pre_ipv", "IPV INE (CCAA asignado a la provincia)", "cod_ccaa")]
    cols = [o[2] for o in opciones]
    mask = U[cols + ["x"]].notna().all(axis=1)
    for nom, _, y, med, cl in opciones:
        s = {**base_p, "yc": y, "medida_precio": med, "cl": cl}
        r = estimar(U, s, "compra", mask)
        registrar(fila(r, s, "compra"), B, "una_dimension", f"medida_precio_{nom}", "medida precio",
                  "muestra comun 2016-2021; Notariado: sin panel provincial en data/processed (solo Comunitat Valenciana)")
    # (b) nivel
    nivel_bloques(U, meta)


def nivel_bloques(U, meta):
    B = "inmigracion"
    base = CTX["base"]
    cc = kd.ccaa()
    sc = spec(nivel="CCAA", xs=["x_stock"], a0=2009, a1=2021, metodo="MCO, EF CCAA+anio", cl="cod",
              unidad_x="+1 pp de poblacion (variacion del stock)", ya="y_alq", yc="y_pre_nom",
              medida_precio="valor tasado MIVAU (nominal)")
    sp = {**base, "xs": ["x_stock"], "unidad_x": "+1 pp de poblacion (variacion del stock)", "yc": "y_pre_nom",
          "medida_precio": "valor tasado MIVAU (nominal)"}
    correr(U, sp, B, "una_dimension", "nivel_provincia_ref_dstock", "nivel", nota="referencia provincial, misma definicion")
    correr(cc, sc, B, "una_dimension", "nivel_CCAA", "nivel", nota="17 CCAA; incluye agregados con las provincias selladas v6 (serie v1, sin modelizacion)")
    sc2 = {**sc, "yc": "y_pre_ipv", "medida_precio": "IPV INE (CCAA)", "a0": 2009}
    correr(cc, sc2, B, "una_dimension", "nivel_CCAA_ipv", "nivel", mercados=("compra",))
    sc3 = {**sc, "a0": 2012, "ya": "y_alq_ser", "medida_alq": "SERPAVI VC (stock)"}
    correr(cc, sc3, B, "una_dimension", "nivel_CCAA_serpavi", "nivel", mercados=("alquiler",))
    # nacional: series temporales con HAC
    nacional_filas()
    # municipio: la cuota/variacion provincial se une a cada municipio (sin dato municipal de extranjeros en data/processed)
    mun = kd.municipal(meta["codes"])
    keyU = U[["cod", "anio", "x_stock", "x", "d_cuota"]].rename(columns={"cod": "cod_prov"})
    mm = mun.merge(keyU, on=["cod_prov", "anio"], how="left")
    mm["cod"] = mm["cod_muni"]
    mm["cod_prov_cl"] = mm["cod_prov"]
    for per in [(2012, 2021), (2009, 2021)]:
        s = spec(nivel="municipio (x provincial unida)", xs=["x_stock"], a0=per[0], a1=per[1], ya="y_alq_ser", yc="y_pre_nom",
                 medida_alq="SERPAVI VC (stock)", medida_precio="valor tasado MIVAU municipal (nominal)",
                 cl="cod_prov_cl", metodo="MCO, EF municipio+anio, cluster provincia",
                 unidad_x="+1 pp de poblacion (variacion del stock provincial)")
        if SMOKE:
            mm_ = mm[mm["cod_muni"].astype(str).str[:3].isin(mm["cod_muni"].astype(str).str[:3].unique()[:30])]
        else:
            mm_ = mm
        correr(mm_, s, B, "una_dimension", f"nivel_municipio_{per[0]}_{per[1]}", "nivel",
               nota="pseudo-replicacion: el regresor es provincial; cluster provincia")


def nacional_filas():
    B = "inmigracion"
    na = kd.nacional()
    import statsmodels.api as sm
    for x, nom in [("x_stock", "variacion del stock (pp de pob.)"), ("x_flujo", "flujo anual INE/Eurostat (pp de pob.)")]:
        for y, mk, med in [("y_alq", "alquiler", "IPC alquiler (stock)"), ("y_pre_nom", "compra", "valor tasado MIVAU (nominal)"),
                           ("y_pre_ipv", "compra", "IPV INE")]:
            a0 = 2004 if x == "x_stock" else 2009
            d = na[na["anio"].between(a0, 2021)].dropna(subset=[x, y])
            if len(d) < 8:
                continue
            res = sm.OLS(d[y], sm.add_constant(d[x])).fit(cov_type="HAC", cov_kwds={"maxlags": 2}, use_t=True)
            ci = res.conf_int().loc[x]
            s = spec(nivel="nacional", xs=[x], a0=a0, a1=2021, metodo="MCO serie temporal, HAC(2)", ya=y, yc=y,
                     medida_alq=med, medida_precio=med, unidad_x=f"+1 pp ({nom})")
            r = dict(coef=float(res.params[x]), se=float(res.bse[x]), p=float(res.pvalues[x]), lo=float(ci[0]),
                     hi=float(ci[1]), N=int(res.nobs), G=int(res.nobs), F1=np.nan)
            f = fila(r, s, mk)
            registrar(f, B, "una_dimension", f"nivel_nacional_{x}_{y}", "nivel", "serie anual agregada; sin EF; N pequeno")


# ------------------------------------------------------------------ bloque 3: colinealidad y demanda externa
def colinealidad(U):
    out = {}
    m = U.dropna(subset=["l1_share_ext_pob", "l1_ln_pob", "lv_tas6"])
    m = m[m["anio"].between(2016, 2024)]
    out["v6_share_vs_ln_pob"] = kl.corr_tipos(m, "l1_share_ext_pob", "l1_ln_pob")
    v, n = kl.vif_within(m, ["l1_share_ext_pob", "l1_ln_pob"])
    out["v6_vif_share_pob"] = dict(v, N=n)
    v2, n2 = kl.vif_within(m.dropna(subset=kd.NUCLEO), ["l1_share_ext_pob"] + kd.NUCLEO)
    out["v6_vif_nucleo"] = dict(v2, N=n2)
    # base v2: flujo/poblacion t-1 frente a ln poblacion
    mb = U[U["anio"].between(2009, 2021)].dropna(subset=["x", "ln_pop_l"])
    out["v2_flujo_vs_ln_pob"] = kl.corr_tipos(mb, "x", "ln_pop_l")
    mb2 = U[U["anio"].between(2009, 2021)].dropna(subset=["x_stock", "ln_pop_l"])
    out["v2_dstock_vs_ln_pob"] = kl.corr_tipos(mb2, "x_stock", "ln_pop_l")
    mb3 = U[U["anio"].between(2009, 2021)].dropna(subset=["d_cuota", "ln_pop_l"])
    out["v2_dcuota_vs_ln_pob"] = kl.corr_tipos(mb3, "d_cuota", "ln_pop_l")
    # cuota frente a variables de demanda externa
    for v, tag in [("costa6", "costa"), ("pct_no_principal_2021", "no_principal"), ("nores_1516", "no_residentes_1516"),
                   ("l1_share_compra_ext_res_pct", "compra_ext_residentes")]:
        mm = m.dropna(subset=[v])
        if v == "l1_share_compra_ext_res_pct":
            out[f"corr_cuota_{tag}"] = kl.corr_tipos(mm, "l1_share_ext_pob", v)
        else:
            g = mm.groupby("cod")[["l1_share_ext_pob", v]].mean()
            out[f"corr_cuota_{tag}"] = dict(entre=float(np.corrcoef(g.iloc[:, 0], g.iloc[:, 1])[0, 1]), N=len(g))
    return out


def demanda_externa(U):
    """Cuota de extranjeros t-1 en niveles (v6): con y sin controles de demanda externa, tres desenlaces."""
    B = "inmigracion"
    ctrl_sets = {"sin_controles": [], "con_poblacion": ["l1_ln_pob"], "con_nucleo": kd.NUCLEO}
    ext_sets = {"sin_externa": ([], None),
                "costa_x_anio": ([], ["costa_anio"]),
                "no_principal_x_anio": ([], ["nop_anio"]),
                "compras_ext_residentes": (["l1_share_compra_ext_res_pct"], None),
                "costa+no_principal+compras_ext": (["l1_share_compra_ext_res_pct"], ["costa_anio", "nop_anio"]),
                "no_residentes_1516_x_anio": ([], ["nores_anio"])}
    mercados = [("compra", "lv_tas6", "valor tasado MIVAU", 2016, 2024),
                ("compra", "lv_reg6", "Registradores (m2)", 2016, 2024),
                ("alquiler", "lv_alq6", "SERPAVI VC (stock)", 2016, 2023)]
    res = {}
    for mk, y, med, a0, a1 in mercados:
        for cn, cs in ctrl_sets.items():
            for en, (ec, ex) in ext_sets.items():
                s = spec(xs=["l1_share_ext_pob"], ctrl=cs + ec, extra=ex, a0=a0, a1=a1,
                         ya=(y if mk == "alquiler" else None), yc=(y if mk == "compra" else None),
                         medida_alq=med, medida_precio=med, metodo="MCO niveles ln, EF prov+anio",
                         unidad_x="+1 pp de cuota de extranjeros (t-1)")
                # misma muestra dentro de cada (mercado, medida, controles): la de la especificacion con todos los controles externos
                s_full = {**s, "ctrl": cs + ["l1_share_compra_ext_res_pct"], "extra": ["costa_anio", "nop_anio"]}
                mask = comunes(U, s, s_full, mk) if en != "no_residentes_1516_x_anio" else None
                r = estimar(U, s, mk, mask)
                f = fila(r, s, mk)
                f2 = registrar(f, B, "demanda_externa", f"{med}|{cn}|{en}", "controles de demanda externa",
                               "muestra comun a las variantes con compras de extranjeros residentes" if mask is not None else
                               "muestra distinta: no residentes solo 2015-2016 (R1A), 38 provincias")
                res[(med, cn, en)] = f2
    # pooled (sin EF): la cuota capta provincias de demanda externa mediante niveles
    for mk, y, med, a0, a1 in mercados:
        for en, ctrl in [("sin_externa", []), ("costa+no_principal", ["costa_lvl", "nop_lvl"]),
                         ("costa+no_principal+compras_ext", ["costa_lvl", "nop_lvl", "l1_share_compra_ext_res_pct"])]:
            s = spec(xs=["l1_share_ext_pob"], ctrl=["l1_ln_pob"] + ctrl, a0=a0, a1=a1, fe="anio",
                     ya=(y if mk == "alquiler" else None), yc=(y if mk == "compra" else None), medida_alq=med,
                     medida_precio=med, metodo="MCO pooled con EF de anio (sin EF de provincia)",
                     unidad_x="+1 pp de cuota de extranjeros (t-1)")
            s_full = {**s, "ctrl": ["l1_ln_pob", "costa_lvl", "nop_lvl", "l1_share_compra_ext_res_pct"]}
            mask = comunes(U, s, s_full, mk)
            f2 = registrar(fila(estimar(U, s, mk, mask), s, mk), B, "demanda_externa", f"{med}|pooled|{en}",
                           "controles de demanda externa", "pooled; muestra comun")
            res[(med, "pooled", en)] = f2
    # primeras diferencias con controles de demanda externa (tendencias por intensidad)
    for mk, y, med, a0, a1 in [("compra", "y_pre_t6", "valor tasado MIVAU", 2017, 2024),
                               ("alquiler", "y_alq6", "SERPAVI VC (stock)", 2017, 2023)]:
        for en, ctrl in [("sin_externa", ["dl1_ln_pob"]),
                         ("tendencia_costa+tendencia_no_principal", ["dl1_ln_pob", "tend_costa", "tend_nop"]),
                         ("+ compras_ext (var.)", ["dl1_ln_pob", "tend_costa", "tend_nop", "dl1_share_compra_ext_res_pct"])]:
            s = spec(xs=["dl1_share_ext_pob"], ctrl=ctrl, a0=a0, a1=a1, ya=(y if mk == "alquiler" else None),
                     yc=(y if mk == "compra" else None), medida_alq=med, medida_precio=med,
                     metodo="primeras diferencias, EF anio+provincia", unidad_x="+1 pp de variacion de la cuota (t-1)")
            s_full = {**s, "ctrl": ["dl1_ln_pob", "tend_costa", "tend_nop", "dl1_share_compra_ext_res_pct"]}
            mask = comunes(U, s, s_full, mk)
            f2 = registrar(fila(estimar(U, s, mk, mask), s, mk), B, "demanda_externa", f"{med}|FD|{en}",
                           "controles de demanda externa", "primeras diferencias; muestra comun")
            res[(med, "FD", en)] = f2
    return res


def bma_bloque(U):
    """PIP aproximado (BIC) de la cuota con y sin controles de demanda externa (nucleo de M2)."""
    out = {}
    for mk, y, a0, a1 in [("compra", "lv_tas6", 2016, 2024), ("alquiler", "lv_alq6", 2016, 2023)]:
        m = U[U["anio"].between(a0, a1)]
        base_x = ["l1_share_ext_pob"] + kd.NUCLEO
        ext_x = base_x + ["l1_share_compra_ext_res_pct", "tend_costa", "tend_nop"]
        mm = m.dropna(subset=[y] + ext_x)
        for nom, xs in [("nucleo_M2", base_x), ("nucleo+demanda_externa", ext_x)]:
            r, n, nm = kl.bma_bic(mm, y, xs)
            out[(mk, nom)] = dict(pip=r["l1_share_ext_pob"]["pip"], media=r["l1_share_ext_pob"]["media"],
                                  pip_pob=r["l1_ln_pob"]["pip"], N=n, modelos=nm, todos={k: v["pip"] for k, v in r.items()})
            REG.log("K2", f"BMA_BIC|{mk}|{nom}", f"{y}~{'+'.join(xs)} (EF prov+anio, BMA con BIC)", a0, a1, n, np.nan, np.nan,
                    np.nan, np.nan, r["l1_share_ext_pob"]["media"], np.nan,
                    f"PIP cuota={r['l1_share_ext_pob']['pip']:.3f}; valor tasado/SERPAVI; C4")
    return out


# ------------------------------------------------------------------ principal
def main():
    U, meta = kd.cargar(smoke=SMOKE)
    CTX.update(renta_media=meta["renta_media"], precio_medio=meta["precio_medio"], smoke=SMOKE)
    cadena = camino(U)
    una_dimension(U, meta)
    col = colinealidad(U)
    dem = demanda_externa(U)
    bma = bma_bloque(U)
    import k2_otros as ko
    ko.run(U, meta, CTX, FILAS, registrar, fila, estimar, spec, comunes, REG, OUT)
    import k2_salidas as ks
    ks.escribir(U, meta, CTX, FILAS, cadena, col, dem, bma, REG, OUT, SMOKE)


if __name__ == "__main__":
    main()
