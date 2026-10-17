"""V16 fase 6 · Q2 · vivienda turística (grupo A). Solo entrenamiento. C4; pendiente de evaluación sellada.

Q2a  DiD de intensidad en forma reducida (Webb NO APTO: estimación puntual, sin p-valor ni IC).
Q2b  solo robustez de Q2a (Andalucía, dosis OpenRTA reconstruida, sesgo de supervivencia).
Q2c  exposición INE-VUT municipal frente al IPVA-TAM municipal (Webb NO APTO).
BLP/GATES de Q2: descriptivo (NO APTO). Precisiones de implementación: docs/v16/desviaciones.md, D3.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from src.v16 import q_comun as Q

OUT = ROOT / "output" / "v16" / "q2"
PRE, POST = [2017, 2018, 2019], [2022, 2023, 2024, 2025]


def zs(x):
    return (x - x.mean()) / x.std(ddof=1)


# ---------------------------------------------------------------- Q2a
def panel_ipc(prov):
    x = Q.trimestral(Q.cargar("base_alquiler", "provincia", "ipc_alquiler_indice"))
    x["anio"] = x.q.dt.year
    a = x.groupby(["territorio_codigo", "anio"]).valor.mean().reset_index()
    a["y"] = np.log(a.valor)
    return a[a.territorio_codigo.isin(prov)]


def q2a(registro: list) -> dict:
    prov = sorted(Q.cargar("base_alquiler", "provincia", "ipc_alquiler_indice").territorio_codigo.unique())
    vut = Q.vut_provincia(prov)
    lv = np.log(vut)
    sd_log = float(lv.std(ddof=1))
    cv = Q.covariables_provincia(prov)
    d = pd.DataFrame({"z": zs(lv)})
    for c in ("ln_renta", "ln_pob", "cuota_extranj"):
        d[c] = zs(cv[c])
    a = panel_ipc(prov)
    a = a[a.anio.isin(PRE + POST)].merge(d, left_on="territorio_codigo", right_index=True)
    a["post"] = a.anio.isin(POST).astype(float)
    a["zp"] = a.z * a.post
    for c in ("ln_renta", "ln_pob", "cuota_extranj"):
        a[c + "_p"] = a[c] * a.post
    ref_sd = 0.04 * sd_log
    r = Q.twfe(a, "y", "zp", "territorio_codigo", "anio")
    el = r["beta"] / sd_log
    registro.append({"id": "Q2a-P", "pregunta": "Q2a", "rol": "principal", "especificacion": "DiD intensidad: log IPC alquiler prov. ~ z(log %VUT 2020-08)×post(2022-25) + EF provincia y año; sin 2020-21",
                     "muestra": f"{a.territorio_codigo.nunique()} provincias, pre 2017-19, post 2022-25", "n": r["n"], "estimacion": r["beta"], "unidad": "Δlog por DT del log de la exposición",
                     "inferencia": "ninguna (did_intensidad_webb NO APTO)", "nota": f"elasticidad {el:.4f}; referencia {ref_sd:.4f}"})
    # exclusión grandes ciudades
    b = a[~a.territorio_codigo.isin(Q.GRANDES_PROV)]
    z2 = zs(lv[~lv.index.isin(Q.GRANDES_PROV)])
    b = b.assign(zp=b.territorio_codigo.map(z2) * b.post)
    rx = Q.twfe(b, "y", "zp", "territorio_codigo", "anio")
    registro.append({"id": "Q2a-X1", "pregunta": "Q2a", "rol": "robustez (punto 14)", "especificacion": "sin provincias de Barcelona, València, Sevilla y Málaga (exposición re-estandarizada)",
                     "muestra": f"{b.territorio_codigo.nunique()} provincias", "n": rx["n"], "estimacion": rx["beta"], "unidad": "Δlog por DT", "inferencia": "ninguna", "nota": "islas no selladas: ninguna"})
    # con controles x post (largo de Oster)
    ctr = ["ln_renta_p", "ln_pob_p", "cuota_extranj_p"]
    ac = a.dropna(subset=ctr)
    corto = Q.twfe(ac, "y", "zp", "territorio_codigo", "anio")
    largo = Q.twfe(ac, "y", "zp", "territorio_codigo", "anio", controles=ctr)
    registro.append({"id": "Q2a-C1", "pregunta": "Q2a", "rol": "robustez (controles)", "especificacion": "principal + renta ADRH, población y cuota de extranjeros 2019 × post",
                     "muestra": f"{ac.territorio_codigo.nunique()} provincias", "n": largo["n"], "estimacion": largo["beta"], "unidad": "Δlog por DT", "inferencia": "ninguna", "nota": "base de Oster/CH"})
    sens = Q.sensibilidad({"beta": corto["beta"], "r2": corto["r2"]}, largo)
    # placebo de fecha dentro del preperiodo: pre 2012-2015, post falso 2016-2019
    p = panel_ipc(prov)
    p = p[p.anio.between(2012, 2019)].merge(d[["z"]], left_on="territorio_codigo", right_index=True)
    p["zp"] = p.z * (p.anio >= 2016)
    rpl = Q.twfe(p, "y", "zp", "territorio_codigo", "anio")
    registro.append({"id": "Q2a-PL1", "pregunta": "Q2a", "rol": "placebo de fecha", "especificacion": "post falso 2016-2019 frente a 2012-2015",
                     "muestra": f"{p.territorio_codigo.nunique()} provincias", "n": rpl["n"], "estimacion": rpl["beta"], "unidad": "Δlog por DT", "inferencia": "ninguna", "nota": "debería estar cerca de 0"})
    # estudio de eventos (base 2019)
    e = panel_ipc(prov)
    e = e[e.anio.between(2012, 2025) & ~e.anio.isin([2020, 2021])].merge(d[["z"]], left_on="territorio_codigo", right_index=True)
    años = [y for y in sorted(e.anio.unique()) if y != 2019]
    for y in años:
        e[f"e{y}"] = e.z * (e.anio == y)
    X = [f"e{y}" for y in años]
    ee = e[["territorio_codigo", "anio", "y", *X]].copy()
    M = Q._demean(ee[["y", *X]].to_numpy(float), ee.territorio_codigo.to_numpy(), ee.anio.to_numpy())
    bb, *_ = np.linalg.lstsq(M[:, 1:], M[:, 0], rcond=None)
    evento = {int(y): float(b_) for y, b_ in zip(años, bb)}
    pre_coef = [v for y, v in evento.items() if y < 2019]
    pend_pre = float(np.polyfit([y for y in evento if y < 2019], pre_coef, 1)[0])
    # diagnósticos de corte: Δ post−pre
    wide = a.pivot_table(index="territorio_codigo", columns="anio", values="y")
    dy = (wide[POST].mean(axis=1) - wide[PRE].mean(axis=1)).rename("dy").to_frame().join(d)
    dyc = dy.dropna()
    cor = Q.ols_corte(dyc.dy.values, dyc.z.values, dyc[["ln_renta", "ln_pob", "cuota_extranj"]].values)
    cen, _ = Q.centroides_provincia()
    mor = Q.moran(cor["residuos"], np.array([cen[p_] for p_ in dyc.index]))
    bp = Q.breusch_pagan(cor["residuos"], dyc[["z", "ln_renta", "ln_pob", "cuota_extranj"]].values)
    # Bai-Perron sobre la brecha tercil alto − tercil bajo (trimestral 2007-2025)
    from src.econ_utils import bai_perron
    x = Q.trimestral(Q.cargar("base_alquiler", "provincia", "ipc_alquiler_indice"))
    w = np.log(x.pivot_table(index="territorio_codigo", columns="q", values="valor"))
    w = w.loc[:, (w.columns >= pd.Period("2007Q1", "Q")) & (w.columns <= pd.Period("2025Q4", "Q"))]
    alto = lv[lv >= lv.quantile(2 / 3)].index
    bajo = lv[lv <= lv.quantile(1 / 3)].index
    gap = w.loc[alto].mean() - w.loc[bajo].mean()
    gap.index = pd.PeriodIndex(gap.index, freq="Q")
    try:
        bpr = bai_perron(gap, pd.DataFrame({"c": np.ones(len(gap))}, index=gap.index), max_bkps=2, min_size=12)
    except Exception as ex:  # pragma: no cover
        bpr = {"error": str(ex)}
    # balance exposición alta/baja
    bal = []
    cvv = cv.join(vut.rename("pct_vut"))
    for c in ("ln_renta", "ln_pob", "cuota_extranj", "obra_pc"):
        hi, lo = cvv.loc[alto, c].dropna(), cvv.loc[bajo, c].dropna()
        sd = np.sqrt((hi.var() + lo.var()) / 2)
        bal.append({"variable": c, "media_tercil_alto": float(hi.mean()), "media_tercil_bajo": float(lo.mean()), "dif_estandarizada": float((hi.mean() - lo.mean()) / sd)})
    # BLP/GATES provincial (moderadores sin la propia exposición: colineal)
    mod = dyc.join(cv[["obra_pc"]]).dropna()
    nm = ["ln_renta", "ln_pob", "cuota_extranj", "obra_pc"]
    Xm = np.column_stack([zs(mod[c]).values for c in nm])
    blp = Q.blp_gates(mod.dy.values, mod.z.values, Xm, nm)
    return {"beta_por_DT": r["beta"], "elasticidad": el, "dt_log_exposicion": sd_log, "referencia_b_por_DT": ref_sd,
            "magnitud_referencia": "0,04 × DT del log de la exposición (elasticidad central de L2/P5)", "n_obs": r["n"],
            "beta_sin_grandes_ciudades": rx["beta"], "beta_con_controles": largo["beta"], "beta_corto_misma_muestra": corto["beta"],
            "placebo_fecha": rpl["beta"], "evento_base_2019": evento, "pendiente_coef_pre": pend_pre,
            "r2_parcial": r["r2_parcial"], "sensibilidad": sens, "moran_residuos": mor, "breusch_pagan": bp, "bai_perron_brecha_tercil": bpr,
            "balance_terciles": bal, "blp_gates": blp,
            "honest_did": "no validado en la fase 5 (no figura en veredictos.csv): no se usa; se publican los coeficientes previos del estudio de eventos"}


# ---------------------------------------------------------------- Q2c
def vut_municipal():
    v = Q.cargar("alquiler_turismo", "municipio")
    v = v[v.variable.str.startswith("ine_vte_porcentaje")].copy()
    v["anio"] = v.periodo.astype(str).str[:4].astype(int)
    return v.groupby(["territorio_codigo", "anio"]).valor.mean().rename("pct").reset_index()


def q2c(registro: list) -> dict:
    ip = Q.cargar("base_alquiler", "municipio", "ipva_tam_indice")
    ip["anio"] = ip.periodo.astype(str).astype(int)
    ip = ip[ip.anio.between(2021, 2024)][["territorio_codigo", "anio", "valor"]].rename(columns={"valor": "idx"})
    ip["y"] = np.log(ip.idx)
    ip = ip.sort_values(["territorio_codigo", "anio"])
    ip["dy"] = ip.groupby("territorio_codigo").y.diff()
    v = vut_municipal()
    d = ip.merge(v, on=["territorio_codigo", "anio"], how="inner")
    d = d[d.pct > 0].copy()          # principal: log; municipio-años con 0 % fuera (D3)
    d["lpct"] = np.log(d.pct)
    sdl = float(d.lpct.std(ddof=1))
    d["z"] = (d.lpct - d.lpct.mean()) / sdl
    ref = 0.04 * sdl
    r = Q.twfe(d, "y", "z", "territorio_codigo", "anio")
    registro.append({"id": "Q2c-P", "pregunta": "Q2c", "rol": "principal", "especificacion": "log IPVA-TAM municipal ~ z(log %VUT INE) + EF municipio y año, 2021-2024",
                     "muestra": f"{d.territorio_codigo.nunique()} municipios", "n": r["n"], "estimacion": r["beta"], "unidad": "Δlog por DT del log de la exposición",
                     "inferencia": "ninguna (did_intensidad_webb NO APTO; agrupación por provincia no se calcula)", "nota": f"referencia {ref:.4f} (= 0,04 × DT log = {sdl:.3f})"})
    # variante E2: nivel estandarizado, incluye ceros
    d2 = ip.merge(v, on=["territorio_codigo", "anio"], how="inner")
    d2["z"] = (d2.pct - d2.pct.mean()) / d2.pct.std(ddof=1)
    r2 = Q.twfe(d2, "y", "z", "territorio_codigo", "anio")
    registro.append({"id": "Q2c-V1", "pregunta": "Q2c", "rol": "variante declarada (exposición)", "especificacion": "exposición en nivel estandarizado (incluye 0 %)", "muestra": f"{d2.territorio_codigo.nunique()} municipios",
                     "n": r2["n"], "estimacion": r2["beta"], "unidad": "Δlog por DT del nivel", "inferencia": "ninguna", "nota": ""})
    # variantes de resultado: variación anual
    d3 = d.dropna(subset=["dy"])
    r3 = Q.twfe(d3, "dy", "z", "territorio_codigo", "anio")
    registro.append({"id": "Q2c-V2", "pregunta": "Q2c", "rol": "variante declarada (resultado)", "especificacion": "Δlog IPVA-TAM (2022-2024) ~ z(log %VUT)", "muestra": f"{d3.territorio_codigo.nunique()} municipios",
                     "n": r3["n"], "estimacion": r3["beta"], "unidad": "Δlog por DT del log", "inferencia": "ninguna", "nota": ""})
    d4 = d2.dropna(subset=["dy"])
    r4 = Q.twfe(d4, "dy", "z", "territorio_codigo", "anio")
    registro.append({"id": "Q2c-V3", "pregunta": "Q2c", "rol": "variante declarada (resultado × exposición)", "especificacion": "Δlog IPVA-TAM ~ z(nivel %VUT)", "muestra": f"{d4.territorio_codigo.nunique()} municipios",
                     "n": r4["n"], "estimacion": r4["beta"], "unidad": "Δlog por DT del nivel", "inferencia": "ninguna", "nota": ""})
    # sin grandes ciudades
    dx = d[~d.territorio_codigo.isin(Q.GRANDES_MUN)]
    rx = Q.twfe(dx, "y", "z", "territorio_codigo", "anio")
    registro.append({"id": "Q2c-X1", "pregunta": "Q2c", "rol": "robustez (punto 14)", "especificacion": "sin Barcelona, València, Sevilla y Málaga", "muestra": f"{dx.territorio_codigo.nunique()} municipios",
                     "n": rx["n"], "estimacion": rx["beta"], "unidad": "Δlog por DT", "inferencia": "ninguna", "nota": "islas no selladas: ninguna"})
    # controles × tendencia (Oster)
    rp = Q.cargar("renta_parque", "municipio", ["ine_adrh_renta_neta_media_hogar_eur", "ine_adrh_poblacion_personas"])
    rp = rp[rp.periodo.astype(str) == "2019"].pivot_table(index="territorio_codigo", columns="variable", values="valor")
    cm = pd.DataFrame({"ln_renta": np.log(rp["ine_adrh_renta_neta_media_hogar_eur"]), "ln_pob": np.log(rp["ine_adrh_poblacion_personas"])})
    dc = d.merge(cm, left_on="territorio_codigo", right_index=True).dropna(subset=["ln_renta", "ln_pob"])
    t = dc.anio - 2021
    dc["c1"] = (dc.ln_renta - dc.ln_renta.mean()) * t
    dc["c2"] = (dc.ln_pob - dc.ln_pob.mean()) * t
    corto = Q.twfe(dc, "y", "z", "territorio_codigo", "anio")
    largo = Q.twfe(dc, "y", "z", "territorio_codigo", "anio", controles=["c1", "c2"])
    registro.append({"id": "Q2c-C1", "pregunta": "Q2c", "rol": "robustez (controles)", "especificacion": "principal + renta y población 2019 × tendencia", "muestra": f"{dc.territorio_codigo.nunique()} municipios",
                     "n": largo["n"], "estimacion": largo["beta"], "unidad": "Δlog por DT", "inferencia": "ninguna", "nota": "base de Oster/CH"})
    sens = Q.sensibilidad({"beta": corto["beta"], "r2": corto["r2"]}, largo)
    # placebo de fecha: estimar con exposición adelantada (lead) 1 año -> Δ resultado actual sobre exposición futura (no causal; chequeo)
    dl = d.sort_values(["territorio_codigo", "anio"]).copy()
    dl["z_lead"] = dl.groupby("territorio_codigo").z.shift(-1)
    dl = dl.dropna(subset=["z_lead"])
    rl = Q.twfe(dl, "y", "z_lead", "territorio_codigo", "anio")
    registro.append({"id": "Q2c-PL1", "pregunta": "Q2c", "rol": "placebo temporal (exposición adelantada)", "especificacion": "log IPVA-TAM ~ z(t+1)", "muestra": f"{dl.territorio_codigo.nunique()} municipios",
                     "n": rl["n"], "estimacion": rl["beta"], "unidad": "Δlog por DT", "inferencia": "ninguna", "nota": "la exposición futura no debería explicar el presente si no hay tendencia previa"})
    # Moran aproximado por provincia (no hay coordenadas municipales en disco)
    res = pd.Series(largo["residuos"], index=largo["indice"])
    dd = dc.loc[res.index].assign(res=res.values)
    pr = dd.groupby(dd.territorio_codigo.str[:2]).res.mean()
    cen, _ = Q.centroides_provincia()
    mor = Q.moran(pr.values, np.array([cen[p_] for p_ in pr.index]))
    bp = Q.breusch_pagan(largo["residuos"], dc[["z", "c1", "c2"]].values)
    # BLP/GATES municipal en diferencias 2021→2024
    w = d.pivot_table(index="territorio_codigo", columns="anio", values=["y", "z"])
    ok = w.dropna()
    dy = ok[("y", 2024)] - ok[("y", 2021)]
    dz = ok[("z", 2024)] - ok[("z", 2021)]
    censo = Q.cargar("base_poblacion", "municipio", "pob_censo_anual")
    censo = censo[censo.periodo.astype(str) == "2021"].pivot_table(index="territorio_codigo", columns="desagregacion", values="valor")
    ext = 1 - censo["nacionalidad=España"] / censo["nacionalidad=Total"]
    ob = Q.cargar("base_poblacion", "municipio", "v12_obra_neta")
    ob = ob[ob.desagregacion == "periodo=2021-2025"].set_index("territorio_codigo").valor
    pct21 = v[v.anio == 2021].set_index("territorio_codigo").pct
    mm = pd.DataFrame({"dy": dy, "dz": dz}).join(cm).join(ext.rename("cuota_extranj")).join(pct21.rename("pct_vut_2021")).join((ob / np.exp(cm.ln_pob) * 1000).rename("obra_pc")).dropna()
    nm = ["ln_renta", "ln_pob", "cuota_extranj", "pct_vut_2021", "obra_pc"]
    blp = Q.blp_gates(mm.dy.values, mm.dz.values, np.column_stack([zs(mm[c]).values for c in nm]), nm)
    vals = [r["beta"], r2["beta"], r3["beta"], r4["beta"], rx["beta"], largo["beta"]]
    return {"beta_por_DT": r["beta"], "dt_log_exposicion": sdl, "referencia_b_por_DT": ref, "n_obs": r["n"], "n_municipios": int(d.territorio_codigo.nunique()),
            "beta_variante_nivel": r2["beta"], "beta_variante_dlog": r3["beta"], "beta_variante_dlog_nivel": r4["beta"],
            "beta_sin_grandes_ciudades": rx["beta"], "beta_con_controles": largo["beta"], "placebo_exposicion_adelantada": rl["beta"],
            "multiverso": {"n_especificaciones": 6, "mediana": float(np.median(vals)), "min": float(min(vals)), "max": float(max(vals)),
                           "proporcion_mismo_signo_que_principal": float(np.mean([np.sign(v_) == np.sign(r["beta"]) for v_ in vals])),
                           "nota": "la proporción con IC95 % que excluye 0 no se calcula: sin inferencia apta"},
            "r2_parcial": r["r2_parcial"], "sensibilidad": sens, "moran_residuos_por_provincia": mor, "breusch_pagan": bp, "blp_gates": blp,
            "agrupacion_provincia": "no calculada: did_intensidad_webb NO APTO (Q2c: tamaño 0,0975)"}


# ---------------------------------------------------------------- Q2b (solo robustez)
def q2b(registro: list) -> dict:
    t = Q.cargar("alquiler_turismo_terceros", "municipio", "andalucia_rta_altas_acumuladas_numero")
    t = t[t.desagregacion == "grupo=Completa"].copy()
    t["anio"] = t.periodo.astype(str).astype(int)
    rp = Q.cargar("renta_parque", "municipio", "ine_adrh_poblacion_personas")
    pob = rp[rp.periodo.astype(str) == "2019"].set_index("territorio_codigo").valor
    t["dosis_pc"] = t.valor / t.territorio_codigo.map(pob) * 1000
    t["dosis_ln"] = np.log1p(t.valor)
    s = Q.cargar("base_alquiler", "municipio", "serpavi_alquiler_m2_mediana")
    s = s[s.desagregacion == "tipologia=VC"]
    s["anio"] = s.periodo.astype(str).astype(int)
    s["y_serpavi"] = np.log(s.valor)
    i = Q.cargar("base_alquiler", "municipio", "ipva_tam_indice")
    i["anio"] = i.periodo.astype(str).astype(int)
    i["y_ipva"] = np.log(i.valor)
    base = t[["territorio_codigo", "anio", "dosis_pc", "dosis_ln"]]
    filas = {}
    for res, df in (("y_serpavi", s), ("y_ipva", i)):
        m = base.merge(df[["territorio_codigo", "anio", res]], on=["territorio_codigo", "anio"]).dropna()
        for dos in ("dosis_pc", "dosis_ln"):
            for ini in (2016, 2019):
                mm = m[(m.anio >= ini) & (m.anio <= 2024)]
                if mm.territorio_codigo.nunique() < 5:
                    continue
                rr = Q.twfe(mm, res, dos, "territorio_codigo", "anio")
                k = f"{res}|{dos}|{ini}-2024"
                filas[k] = (rr, mm.territorio_codigo.nunique())
                registro.append({"id": f"Q2b-{len(filas):02d}", "pregunta": "Q2b", "rol": "robustez de Q2a" + (" (principal de Q2b)" if (res, dos, ini) == ("y_serpavi", "dosis_pc", 2016) else ""),
                                 "especificacion": f"{res} ~ {dos} + EF municipio y año, {ini}-2024", "muestra": f"{filas[k][1]} municipios de Andalucía", "n": rr["n"], "estimacion": rr["beta"],
                                 "unidad": "Δlog por unidad de dosis", "inferencia": "ninguna", "nota": "dosis reconstruida (sesgo de supervivencia); solo robustez"})
    # estudio de eventos de dosis continua (principal): dosis final 2024 × año
    p = base[base.anio == 2024].set_index("territorio_codigo").dosis_pc.rename("d24")
    m = s[s.anio.between(2016, 2024)][["territorio_codigo", "anio", "y_serpavi"]].merge(p, left_on="territorio_codigo", right_index=True).dropna()
    m = m[m.territorio_codigo.isin(base.territorio_codigo.unique())]
    ev = {}
    if m.territorio_codigo.nunique() >= 5:
        m["z"] = (m.d24 - m.d24.mean()) / m.d24.std(ddof=1)
        años = [y for y in sorted(m.anio.unique()) if y != 2019]
        for y in años:
            m[f"e{y}"] = m.z * (m.anio == y)
        M = Q._demean(m[["y_serpavi", *[f"e{y}" for y in años]]].to_numpy(float), m.territorio_codigo.to_numpy(), m.anio.to_numpy())
        bb, *_ = np.linalg.lstsq(M[:, 1:], M[:, 0], rcond=None)
        ev = {int(y): float(b_) for y, b_ in zip(años, bb)}
    vals = [v[0]["beta"] for v in filas.values()]
    return {"n_especificaciones": len(filas), "estimaciones": {k: v[0]["beta"] for k, v in filas.items()},
            "municipios": {k: v[1] for k, v in filas.items()},
            "mediana": float(np.median(vals)) if vals else None,
            "proporcion_mismo_signo_que_la_primera": float(np.mean([np.sign(x) == np.sign(vals[0]) for x in vals])) if vals else None,
            "evento_dosis_final_base_2019": ev,
            "nota": "solo robustez de Q2a (adenda, punto 3); sin inferencia; dosis reconstruida con sesgo de supervivencia"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    registro: list = []
    a = q2a(registro)
    b = q2b(registro)
    c = q2c(registro)
    Q.registro(registro, OUT / "registro.csv")
    Q.jdump({"q2a": a, "q2b": b, "q2c": c}, OUT / "q2_detalle.json")
    print("Q2a", a["beta_por_DT"], a["referencia_b_por_DT"], "| Q2c", c["beta_por_DT"], c["referencia_b_por_DT"], "| Q2b", b["n_especificaciones"], b["mediana"])


if __name__ == "__main__":
    main()
