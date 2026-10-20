"""V18 · E3 (inmigración: González y Ortega 2013 y su versión IZA de 2009) · réplica y ampliaciones con nuestros datos.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md, 1.3, + adenda). SEED = 20261010; sin red.
Orden por especificación: (1) MDE (adenda 1.3) con la variación real del instrumento y del regresor, SIN la variable resultado; (2) registro en el Registry; (3) estimación con
inferencia por provincia (Webb-AR + AR exacto; D-E359-7); (4) pruebas B4; (5) Holm por familia; (6) clasificación I1-I8 revisados (I8, réplica ciega, queda pendiente).
Salidas: output/v18/estimacion/e3/{resultado.json, tabla.csv, informe.md, hechos.json, registro.csv, mde.csv}.
Uso: python3 src/v18/estimacion/e3_inmigracion.py [--rapido]   (--rapido: B = 999, para desarrollo; la salida definitiva usa 9.999).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e359_comun as K  # noqa: E402
import e3_extra as EX  # noqa: E402
import e3_municipal as EM  # noqa: E402
import e3_panel as EP  # noqa: E402

SEMILLA = K.SEMILLA
SALIDA = K.OUT / "e3"
GRUPOS = EP.GRUPOS
RAPIDO = "--rapido" in sys.argv
B_WEBB = 999 if RAPIDO else 9999
R_MDE = 500 if RAPIDO else 2000

# ------------------------------------------------------------------------------------------------ referencias únicas (adenda, Anexo B)
REF = {
    "R1": dict(v=44.72, se=18.58, nombre="González y Ortega (2009, IZA): 44,72 €/m² por punto de población", estado="NO VERIFICADA", delta=22.4, unidad="€/m² por punto"),
    "R1q": dict(v=0.462, se=0.033, nombre="González y Ortega (2009, IZA): 0,462 viviendas por inmigrante", estado="NO VERIFICADA", delta=0.231, unidad="viviendas por inmigrante"),
    "R2": dict(v=0.959, se=0.984, nombre="González y Ortega (2011, Chicago Fed), solo redes, 2001-2010", estado="NO VERIFICADA", delta=0.48, unidad="elasticidad"),
    "R2b": dict(v=0.927, se=0.596, nombre="González y Ortega (2011), solo redes, 2001-2008", estado="NO VERIFICADA", delta=0.46, unidad="elasticidad"),
    "R2q": dict(v=1.05, se=0.578, nombre="González y Ortega (2011), cantidad", estado="NO VERIFICADA", delta=0.525, unidad="elasticidad"),
    "A1": dict(v=3.046, se=1.214, nombre="Sanchis-Guarner (2017/2023), precios, semielasticidad", estado="DISCREPANTE (año)", delta=1.52, unidad="% por punto"),
    "A2": dict(v=0.947, se=0.470, nombre="Sanchis-Guarner (2017/2023), alquileres, semielasticidad", estado="DISCREPANTE (año)", delta=0.47, unidad="% por punto"),
    "A3": dict(v=0.947, se=0.470, nombre="Sanchis-Guarner (2017/2023), alquileres, semielasticidad", estado="DISCREPANTE (año)", delta=0.47, unidad="% por punto"),
    "A5": dict(v=3.046, se=1.214, nombre="Sanchis-Guarner (2017/2023), precios, semielasticidad", estado="DISCREPANTE (año)", delta=1.52, unidad="% por punto"),
}
FAMILIA = "E3"
TOPE_V94 = "tope SUGESTIVO: año base 2001 tras el F de 3,4-4,6 de V9-D4 (adenda 1.6)"

PRE = {"R": list(range(1996, 2002)), "A1": list(range(2009, 2014)), "A2": [2012, 2013]}


def cfg_r1(**kw):
    c = dict(ventana=(2002, 2008), x="pp_ext", y="dprecio", peso="pob1998", controles=dict(construccion=True, costa=True), shares="censo2001")
    c.update(kw)
    return c


def cfg_r1q(**kw):
    kw.setdefault("y", "ini_pc")
    return cfg_r1(fe_prov=True, **kw)


def cfg_r2(**kw):
    c = dict(ventana=(2002, 2010), x="dln_wap", y="dlnp", peso="pob2000", controles=dict(construccion=True, costa=True), shares="censo2001")
    c.update(kw)
    return c


def cfg_a1(**kw):
    c = dict(ventana=(2014, 2022), x="pp_ext", y="dlnp100", peso="pob_ini", controles=dict(construccion=True, costa=True), shares="censo2001")
    c.update(kw)
    return c


def cfg_a2(**kw):
    kw.setdefault("y", "dlnrent100")
    return cfg_a1(**kw)


def cfg_a5(**kw):
    return cfg_a1(ventana=(2002, 2019), peso="pob_ini", **kw)


NOCT = dict(construccion=False, costa=False)
SIN_G12 = ["G1_UE15", "G2_AELC"]


def construir_specs() -> list[dict]:
    S = []

    def add(id_, rol, cfg, ref, padre=None, pre="R", tope=None, nota="", holgura=False, ne=None):
        S.append(dict(id=id_, rol=rol, cfg=dict(cfg, id=id_), ref=ref, padre=padre, pre=pre, tope=tope, nota=nota, holgura=holgura, ne=ne))

    # ---- R1 (ventana IZA, principal 2002-2008 con cuotas del Censo de 2001)
    add("E3-R1", "principal", cfg_r1(), "R1", tope=TOPE_V94, nota="repite_visto (V9-D4)")
    for v, kw, nota in [("v2", dict(shares="padron2003"), "cuotas del padrón de 2003 (dentro de la ventana: contaminadas; máximo ASOCIACIÓN si fuera la principal)"),
                        ("v4", dict(peso=None), "sin ponderar"), ("v5", dict(grupos_excl=SIN_G12), "sin los grupos 1 y 2 (UE-15 y AELC)"),
                        ("v6", dict(controles=NOCT), "sin construcción ni costa × año"), ("v7", dict(controles=dict(construccion=True, costa=True, ficticias=True)),
                                                                                             "ficticias de 2005 y 2006 × cuota no comunitaria de 2001"),
                        ("v8", dict(excl_prov=["08"]), "sin Barcelona"), ("v9", dict(excl_prov=["03", "29"]), "sin Alicante ni Málaga")]:
        add(f"E3-R1-{v}", "variante", cfg_r1(**kw), "R1", padre="E3-R1", nota=nota)
    add("E3-R1-v11", "variante", cfg_r1(interpolar_2003=True), "R1", padre="E3-R1", holgura=True, nota="holgura nº 1: 2003 con la composición interpolada (marcada)")
    for v, motivo in [("v1", "ventana 1998-2008: sin stock provincial de extranjeros antes de 2002"), ("v3", "Censo de 1991 no está en el repositorio"),
                      ("v10", "choque sin la propia provincia con el padrón por nacionalidad: no reconstruye los 8 grupos")]:
        add(f"E3-R1-{v}", "variante", cfg_r1(), "R1", padre="E3-R1", ne=motivo)
    # ---- R1q
    add("E3-R1q", "principal", cfg_r1q(), "R1q", tope=None, nota="repite_visto (V9-D4)")
    add("E3-R1q-v1", "variante", cfg_r1q(y="ter_pc"), "R1q", padre="E3-R1q", nota="terminadas en lugar de iniciadas")
    add("E3-R1q-v2", "variante", cfg_r1q(), "R1q", padre="E3-R1q", ne="ventana 1998-2008: sin stock provincial de extranjeros antes de 2002")
    # ---- R2 (ventana publicada 2002-2010)
    add("E3-R2", "principal", cfg_r2(), "R2", tope=TOPE_V94, nota="repite_visto (V9-D4); es la estimación propia de E3 para B5 (adenda 1.9)")
    for v, kw, nota in [("v1", dict(ventana=(2000, 2010)), "ventana 2000-2010 (la del original)"), ("v2", dict(x="dln_pob"), "población total en lugar de 15-64"),
                        ("v3", dict(grupos_excl=SIN_G12), "sin los grupos 1 y 2"), ("v4", dict(controles=NOCT), "sin construcción ni costa"),
                        ("v5", dict(peso=None), "sin ponderar"), ("v6", dict(shares="padron2003"), "cuotas del padrón de 2003"),
                        ("v8", dict(excl_prov=["08"]), "sin Barcelona")]:
        add(f"E3-R2-{v}", "variante", cfg_r2(**kw), "R2", padre="E3-R2", nota=nota)
    add("E3-R2-v7", "variante", cfg_r2(), "R2", padre="E3-R2", ne="Censo de 1991 no está en el repositorio")
    add("E3-R2b", "principal", cfg_r2(ventana=(2002, 2008)), "R2b", nota="subperiodo 2002-2008 de R2")
    add("E3-R2b-v1", "variante", cfg_r2(ventana=(2001, 2008)), "R2b", padre="E3-R2b", nota="ventana 2001-2008")
    add("E3-R2q", "principal", cfg_r2(y="dlnini"), "R2q", nota="cantidad: Δ ln iniciadas")
    add("E3-R2q-v1", "variante", cfg_r2(y="dlnter"), "R2q", padre="E3-R2q", nota="terminadas")
    # ---- ampliaciones provinciales
    add("E3-A1", "principal", cfg_a1(), "A1", pre="A1", nota="repite_visto (Q3-c1); es el respaldo de E3 para B5")
    for v, kw, nota in [("v1", dict(grupos_excl=SIN_G12), "sin los grupos 1 y 2"), ("v2", dict(shares="padron2003"), "cuotas del padrón de 2003"),
                        ("v3", dict(peso=None), "sin ponderar"), ("v5", dict(excl_prov=["08"]), "sin Barcelona"), ("v6", dict(controles=NOCT), "sin construcción ni costa")]:
        add(f"E3-A1-{v}", "variante", cfg_a1(**kw), "A1", padre="E3-A1", pre="A1", nota=nota)
    add("E3-A1-v4", "variante", cfg_a1(), "A1", padre="E3-A1", pre="A1", ne="IPV por CCAA: nueve clusters, inferencia sin Monte Carlo apto (Webb con 8 clusters: NO APTO)")
    add("E3-A2", "principal", cfg_a2(), "A2", pre="A2", nota="repite_visto (H4, Q3); alquiler SERPAVI provincial (vivienda colectiva)")
    for v, kw, nota in [("v1", dict(y="dlnipva100"), "IPVA"), ("v2", dict(y="dlnipc100"), "IPC de alquiler"), ("v3", dict(grupos_excl=SIN_G12), "sin los grupos 1 y 2"),
                        ("v4", dict(peso=None), "sin ponderar"), ("v5", dict(shares="padron2003"), "cuotas del padrón de 2003"), ("v6", dict(excl_prov=["08"]), "sin Barcelona")]:
        add(f"E3-A2-{v}", "variante", cfg_a2(**kw), "A2", padre="E3-A2", pre="A2", nota=nota)
    add("E3-A4", "principal", cfg_a1(), "A1", nota="dos endógenas por tenencia del Censo de 2011 (SUGESTIVO como máximo)",
        ne="la tenencia por nacionalidad del Censo de 2011 por provincia no está en el repositorio ni en Eurostat (cens_11htts_r2 es por hogares y NUTS 2, sin nacionalidad)")
    add("E3-A5", "principal", cfg_a5(), "A5", nota="ventana larga 2002-2019 (partición 2002-2010 / 2011-2019 como diagnóstico)")
    add("E3-A5-v1", "variante", cfg_a5(), "A5", padre="E3-A5", ne="choque sin la propia provincia con el padrón por nacionalidad: no reconstruye los 8 grupos")
    return S


# ------------------------------------------------------------------------------------------------ cálculo por especificación
def periodo_pre(spec) -> list[int]:
    if spec["pre"] == "A1":
        return PRE["A1"]
    if spec["pre"] == "A2":
        return PRE["A2"]
    return PRE["R"]


def y_pre_cfg(spec):
    c = dict(spec["cfg"])
    return c


def precomprobar(dat: EP.DatosE3, spec: dict) -> dict:
    """MDE (adenda 1.3) con la variación real del regresor y del instrumento; σ y ρ del preperiodo. No usa la variable resultado de la ventana."""
    pan = dat.panel(spec["cfg"])
    dis = K.DisenoIV(pan.y, pan.x, pan.z, pan.prov, C=pan.C, w=pan.w, B=1)
    pre = dat.pre_panel(spec["cfg"], periodo_pre(spec))
    sig, rho = K.sigma_rho_de_panel(pre.y, pre.prov, pre.año, pre.C, pre.w)
    m = K.mde_iv(dis, pan.año[dis.orden], sig, rho, R=R_MDE)
    ref = REF[spec["ref"]]
    m.update({"ref": ref["v"], "estimable": bool(m["mde80"] <= ref["v"]), "n": dis.n, "G": dis.G, "k": dis.k, "n_pre": len(pre.y),
              "inv_hhi_origen": hhi_origen(pan), "F_eff": dis.f_efectivo()})
    return m


def hhi_origen(pan: EP.Panel) -> dict:
    """1/HHI de los pesos de los choques (BHJ): s_c = Σ_pt w·e_pc,t por origen, y por origen × año ponderando además por el tamaño medio del choque."""
    E = pan.expo
    w = np.ones(len(E)) if pan.w is None else pan.w
    s_c = (w[:, None] * E).sum(axis=0)
    out = {"por_origen": K.inv_hhi(s_c), "pesos_origen": {o: float(v) for o, v in zip(pan.origenes, s_c / s_c.sum())}}
    sn = []
    for t in np.unique(pan.año):
        m = pan.año == t
        sn += list((w[m, None] * E[m]).sum(axis=0) * np.abs(np.mean(pan.g[m], axis=0)))
    out["por_origen_año"] = K.inv_hhi(np.array(sn))
    return out


def estimar(dat: EP.DatosE3, spec: dict, completo: bool, B: int = B_WEBB) -> dict:
    pan = dat.panel(spec["cfg"])
    dis = K.DisenoIV(pan.y, pan.x, pan.z, pan.prov, C=pan.C, w=pan.w, B=B)
    r = dis.resumen(con_ic=True, con_ic90=completo)
    r["panel"] = pan
    r["dis"] = dis
    return r


def efectos_atipicos(pan: EP.Panel) -> list[str]:
    """Provincia con mayor exposición media y provincia con la variación media del resultado más extrema (1 % superior con 39 unidades = 1 provincia por criterio)."""
    d = pd.DataFrame({"p": pan.prov, "z": pan.z, "y": pan.y}).groupby("p").mean()
    a = d["z"].idxmax()
    b = (d["y"] - d["y"].median()).abs().idxmax()
    return sorted({a, b})


def diag_principal(dat: EP.DatosE3, spec: dict, r: dict, B: int = B_WEBB) -> dict:
    cfg = spec["cfg"]
    pan, dis = r["panel"], r["dis"]
    out = {}
    ref = REF[spec["ref"]]
    ic = (r["ic_webb_ar"]["lo"], r["ic_webb_ar"]["hi"])
    # -- pretendencias del instrumento (corte transversal) y su potencia
    pre_años = periodo_pre(spec)
    pre = dat.pre_panel(cfg, pre_años)
    dfp = pd.DataFrame({"p": pre.prov, "y": pre.y}).groupby("p")["y"].mean()
    if cfg["y"] in ("ini_pc", "ter_pc"):
        a = pd.DataFrame({"p": pre.prov, "t": pre.año, "y": pre.y})
        m1 = a[a["t"] >= max(pre_años) - 2].groupby("p")["y"].mean()
        m0 = a[a["t"] < max(pre_años) - 2].groupby("p")["y"].mean()
        dfp = (m1 - m0).dropna()
    zbar = pd.DataFrame({"p": pan.prov, "z": pan.z, "x": pan.x}).groupby("p").mean()
    comunes = [p for p in dfp.index if p in zbar.index]
    reg = np.array([K.MACRO[p] for p in comunes])
    w = None if cfg.get("peso") is None else dat._peso(cfg, np.array(comunes), None)
    out["pretendencia"] = K.pendiente_previa(dfp.loc[comunes].to_numpy(), zbar.loc[comunes, "z"].to_numpy(), zbar.loc[comunes, "x"].to_numpy(), reg, w, B=B)
    out["pretendencia"]["roth_ok"] = bool(out["pretendencia"]["sesgo_detectable_beta"] < 0.5 * ref["v"])
    # -- placebo de fecha: instrumento de t + 6 en el preperiodo (años con instrumento definido)
    zf = dat.z_en(cfg, pre.prov, pre.año, desfase=6)
    ok = np.isfinite(zf)
    if ok.sum() > 30:
        Cpf, _ = dat._controles(cfg, pre.prov[ok], pre.año[ok])
        wp = None if pre.w is None else pre.w[ok]
        out["placebo_fecha"] = K.placebo_fecha(pre.y[ok], zf[ok], pre.prov[ok], Cpf, wp, r["rf"], B=B)
    else:
        out["placebo_fecha"] = None
    # -- placebo de resultado: población de 65 años o más (total)
    c65 = dict(cfg, y="dln65")
    pan65 = dat.panel(c65)
    d65 = K.DisenoIV(pan65.y, pan65.x, pan65.z, pan65.prov, C=pan65.C, w=pan65.w, B=B)
    r65 = d65.iv()
    out["placebo_resultado"] = {"coef": r65["beta"], "se": r65["se"], "p_webb_ar": d65.webb_ar_p(0.0), "p_ar_exacto": d65.ar_exacto()["p_beta0"], "n": r65["n"]}
    # -- balance a nivel de choque (BHJ; el del plan) y, como información, a nivel de provincia (falla de forma mecánica: ver D-E359-16)
    out["balance"] = EX.balance_choques(dat, pan)
    X = pd.DataFrame({"constr": dat.cuota_constr, "indus": dat.cuota_indus, "lpob": np.log(dat.stock["pob_total"].reindex(dat.P)), "ext01": dat.cuota_ext01}).reindex(comunes)
    out["balance_provincial_info"] = K.balance_provincial(zbar.loc[comunes, "z"].to_numpy(), X.to_numpy(), reg)
    # -- Rotemberg y exclusión de los 2 orígenes de más peso
    ZC = np.column_stack([dis._m(dis.sw * pan.zc[dis.orden, j]) for j in range(pan.zc.shape[1])])
    rot = K.rotemberg(ZC, dis.xt, dis.yt)
    alpha = rot["alpha"]
    top = list(np.argsort(-np.abs(alpha))[:2])
    keep = [j for j in range(len(alpha)) if j not in top]
    z2 = pan.zc[:, keep].sum(axis=1)
    d2 = K.DisenoIV(pan.y, pan.x, z2, pan.prov, C=pan.C, w=pan.w, B=B)
    r2 = d2.iv()
    ic2 = d2.ic_webb_ar(0.05, centro=r2["beta"], escala=r2["se"])
    out["rotemberg"] = {"alpha": {o: float(a_) for o, a_ in zip(pan.origenes, alpha)}, "beta_por_origen": {o: (None if not np.isfinite(b_) else float(b_)) for o, b_ in zip(pan.origenes, rot["beta_k"])},
                        "excluidos": [pan.origenes[j] for j in top], "beta_sin_top": r2["beta"], "se": r2["se"], "F_eff": d2.f_efectivo(), "ic_webb_ar": ic2,
                        "mismo_signo": bool(np.sign(r2["beta"]) == np.sign(r["beta"])), "dentro_ic": bool(ic[0] <= r2["beta"] <= ic[1])}
    # -- Jaeger-Ruist-Stuhler: instrumento retardado (t-4) como control
    try:
        cj = dict(cfg, con_lag=True, lag=4)
        pj = dat.panel(cj)
        dj = K.DisenoIV(pj.y, pj.x, pj.z, pj.prov, C=pj.C, w=pj.w, B=B)
        rj = dj.iv()
        out["jrs"] = {"beta": rj["beta"], "se": rj["se"], "F_eff": dj.f_efectivo(), "n": rj["n"], "dentro_ic": bool(ic[0] <= rj["beta"] <= ic[1]),
                      "nota": "instrumento de t-4 como control (D-E359-10); se pierden los años cuyo retardo cae en 2003"}
    except Exception as e:  # pragma: no cover
        out["jrs"] = {"error": str(e)}
    # -- sin atípicos
    at = efectos_atipicos(pan)
    ca = dict(cfg, excl_prov=list(set(cfg.get("excl_prov", [])) | set(at)))
    pa = dat.panel(ca)
    da = K.DisenoIV(pa.y, pa.x, pa.z, pa.prov, C=pa.C, w=pa.w, B=B)
    ra = da.iv()
    out["sin_atipicos"] = {"excluidas": at, "beta": ra["beta"], "se": ra["se"], "mismo_signo": bool(np.sign(ra["beta"]) == np.sign(r["beta"])), "n": ra["n"]}
    # -- control de la suma de exposiciones × año (BHJ, cuotas incompletas): información, no entra en la clasificación
    suma = pan.expo.sum(axis=1)
    Cs = np.hstack([pan.C, np.column_stack([(pan.año == t) * suma for t in np.unique(pan.año)])])
    ds = K.DisenoIV(pan.y, pan.x, pan.z, pan.prov, C=Cs, w=pan.w, B=B)
    rs = ds.iv()
    out["con_suma_exposicion"] = {"beta": rs["beta"], "se": rs["se"], "F_eff": ds.f_efectivo(), "ic_webb_ar": ds.ic_webb_ar(0.05, centro=rs["beta"], escala=rs["se"]), "n": rs["n"],
                                  "nota": "información adicional (no preinscrita): control de la suma de cuotas × año, como en V9-D4 y la recomendación de BHJ con cuotas incompletas"}
    # -- BHJ alternativo (con el control de la suma de cuotas, condición de equivalencia con el IV de localización)
    try:
        out["bhj_alternativa"] = K.bhj_alternativa(pan.y, pan.x, pan.expo, pan.g, pan.w, pan.año, Cs, pan.origenes)
    except Exception as e:  # pragma: no cover
        out["bhj_alternativa"] = {"error": str(e)}
    return out


def parcial_a5(dat: EP.DatosE3, spec: dict, B: int) -> dict:
    """E3-A5: partición 2002-2010 / 2011-2019 (diagnóstico)."""
    res = {}
    for nombre, v in (("2002-2010", (2002, 2010)), ("2011-2019", (2011, 2019))):
        c = dict(spec["cfg"], ventana=v)
        pan = dat.panel(c)
        d = K.DisenoIV(pan.y, pan.x, pan.z, pan.prov, C=pan.C, w=pan.w, B=B)
        r = d.iv()
        res[nombre] = {"beta": r["beta"], "se": r["se"], "F_eff": d.f_efectivo(), "n": r["n"], "p_webb_ar": d.webb_ar_p(0.0)}
    return res


# ------------------------------------------------------------------------------------------------ especificaciones municipales y coprincipales
def specs_municipales() -> list[dict]:
    S = []

    def add(id_, rol, cfgm, ref, padre=None, nota="", ne=None):
        S.append(dict(id=id_, rol=rol, cfgm=cfgm, ref=ref, padre=padre, nota=nota, ne=ne))

    base = dict(ventana=(2014, 2022), peso_pob0=True)
    add("E3-A3", "principal", dict(base), "A3", nota="repite_visto (H4); alquiler SERPAVI municipal (vivienda colectiva), 28 países, pesos de población de 2013, efectos provincia-año")
    add("E3-A3-v1", "variante", dict(base, resultado="tasado"), "A3", padre="E3-A3", ne="valor tasado municipal: el fichero de MIVAU (309 municipios) no trae código INE y la base solo lo tiene para un municipio")
    add("E3-A3-v2", "variante", dict(base, sin_distritos_sellados=True), "A3", padre="E3-A3", nota="sin los municipios con distritos sellados (adenda 1.5)")
    add("E3-A3-v3", "variante", dict(ventana=(2014, 2022), peso_pob0=False), "A3", padre="E3-A3", nota="sin ponderar")
    add("E3-A3-v4", "variante", dict(base, mun_min_pob=20000), "A3", padre="E3-A3", nota="municipios de más de 20.000 habitantes (población de 2013)")
    add("E3-A3-v5", "variante", dict(base, origenes="sin_res"), "A3", padre="E3-A3", nota="sin los cinco países de la UE-15 del padrón (Alemania, Francia, Italia, Portugal, Reino Unido): los de H4")
    add("E3-P-H4", "coprincipal", dict(ventana=(2012, 2022), peso_pob0=False, origenes="sin_res"), "A3",
        nota="réplica de H4 (V16, src/v16/replica/h4.py): 23 orígenes, 2012-2022, sin pesos; publicado: 2SLS 0,29 % por punto (N = 13.442 en V16)")
    return S


def cfg_municipal(mun: EM.DatosMunicipal, c: dict) -> dict:
    c = dict(c)
    if c.get("origenes") == "sin_res":
        c["origenes"] = [o for o in mun.paises if o not in EM.RES]
    return c


def main() -> int:
    t0 = time.time()
    dat = EP.DatosE3()
    specs = construir_specs()
    reg = K.Registry(SALIDA / "registro.csv")
    mde_tab, res, ne, diag = {}, {}, {}, {}
    # ---- (1) MDE y comprobación previa de las principales provinciales (nunca el coeficiente)
    for s in specs:
        reg.log("v18-E3", f"{s['id']}|registrada", f"y~x|z ({s['cfg']['y']}; {s['cfg']['x']}; {s['cfg']['ventana']})", s["cfg"]["ventana"][0], s["cfg"]["ventana"][1], 0, np.nan,
                np.nan, np.nan, notas=f"{s['rol']}; ref {s['ref']}")
        if s["ne"]:
            ne[s["id"]] = s["ne"]
            continue
        if s["rol"] == "principal":
            m = precomprobar(dat, s)
            mde_tab[s["id"]] = m
            if not m["estimable"]:
                ne[s["id"]] = f"NO ESTIMABLE por variación: MDE {m['mde80']:.3g} > |referencia| {m['ref']:.3g} ({REF[s['ref']]['unidad']})"
        print(f"[{time.time() - t0:5.0f}s] MDE {s['id']}: " + (f"{mde_tab[s['id']]['mde80']:.4g} (ref {mde_tab[s['id']]['ref']})" if s["id"] in mde_tab else s["ne"] or ""), flush=True)
    # ---- (1b) municipal
    mun = EM.DatosMunicipal()
    mspecs = specs_municipales()
    for s in mspecs:
        reg.log("v18-E3", f"{s['id']}|registrada", f"y~x|z municipal ({s['cfgm']})", s["cfgm"]["ventana"][0], s["cfgm"]["ventana"][1], 0, np.nan, np.nan, np.nan, notas=f"{s['rol']}; ref {s['ref']}")
        if s["ne"]:
            ne[s["id"]] = s["ne"]
            continue
        if s["rol"] in ("principal", "coprincipal"):
            cfgm = cfg_municipal(mun, s["cfgm"])
            m = EX.precomprobar_municipal(mun, cfgm, REF[s["ref"]]["v"], R_MDE)
            mde_tab[s["id"]] = m
            if s["rol"] == "principal" and not m["estimable"]:
                ne[s["id"]] = f"NO ESTIMABLE por variación: MDE {m['mde80']:.3g} > |referencia| {m['ref']:.3g} ({REF[s['ref']]['unidad']})"
        print(f"[{time.time() - t0:5.0f}s] MDE {s['id']}: " + (f"{mde_tab[s['id']]['mde80']:.4g} (ref {mde_tab[s['id']]['ref']})" if s["id"] in mde_tab else s["ne"] or ""), flush=True)
    # ---- (2) estimación provincial
    for s in specs:
        if s["id"] in ne:
            continue
        pad = s["padre"]
        if pad and pad in ne:
            ne[s["id"]] = f"su principal {pad} es NO ESTIMABLE"
            continue
        try:
            res[s["id"]] = estimar(dat, s, completo=(s["rol"] == "principal"))
        except Exception as e:
            ne[s["id"]] = f"error de construcción: {e}"
            continue
        r = res[s["id"]]
        reg.log("v18-E3", f"{s['id']}|estimada", f"2SLS por provincia; Webb-AR ({B_WEBB}) + AR", s["cfg"]["ventana"][0], s["cfg"]["ventana"][1], r["n"], np.nan, np.nan, np.nan,
                coef_interes=r["beta"], p_interes=max(r["p_webb_ar"], r["ar"]["p_beta0"]), notas=s["nota"])
        print(f"[{time.time() - t0:5.0f}s] {s['id']}: n={r['n']} G={r['G']} F={r['F_eff']:.1f}", flush=True)
    # ---- (2b) estimación municipal
    for s in mspecs:
        if s["id"] in ne:
            continue
        if s["padre"] and s["padre"] in ne:
            ne[s["id"]] = f"su principal {s['padre']} es NO ESTIMABLE"
            continue
        cfgm = cfg_municipal(mun, s["cfgm"])
        r = EX.estimar_municipal(mun, cfgm, B_WEBB, completo=(s["rol"] == "principal"))
        res[s["id"]] = r
        reg.log("v18-E3", f"{s['id']}|estimada", f"2SLS municipal; Webb-AR ({B_WEBB}) + AR", cfgm["ventana"][0], cfgm["ventana"][1], r["n"], np.nan, np.nan, np.nan, coef_interes=r["beta"],
                p_interes=max(r["p_webb_ar"], r["ar"]["p_beta0"]), notas=s["nota"])
        print(f"[{time.time() - t0:5.0f}s] {s['id']}: n={r['n']} G={r['G']} F={r['F_eff']:.1f}", flush=True)
    # ---- (2c) P provinciales
    pd4 = EX.p_d4(dat, B_WEBB)
    pq3 = EX.p_q3c1(dat, B_WEBB)
    reg.log("v18-E3", "E3-P-D4|estimada", "V9-D4 2003-2012, valor tasado", 2003, 2012, pd4["valor tasado"]["n"], np.nan, np.nan, np.nan, coef_interes=pd4["valor tasado"]["beta"],
            p_interes=max(pd4["valor tasado"]["p_webb_ar"], pd4["valor tasado"]["p_ar"]), notas="coprincipal")
    reg.log("v18-E3", "E3-P-Q3c1|estimada", "V16 Q3-c1 TWFE 2011-2022", 2011, 2022, pq3["n"], np.nan, np.nan, np.nan, coef_interes=pq3["beta"], p_interes=pq3["p_webb"], notas="coprincipal")
    print(f"[{time.time() - t0:5.0f}s] P-D4 y P-Q3c1 listas", flush=True)
    import e3_salidas as SAL
    SAL.escribir(sys.modules[__name__], dat, mun, specs, mspecs, mde_tab, res, ne, pd4, pq3, reg, B_WEBB, t0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
