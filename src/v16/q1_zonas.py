"""V16 fase 6 · Q1 · zonas tensionadas (grupo A). Solo entrenamiento. C4 como máximo; pendiente de evaluación sellada.

Q1a  diagnóstico descriptivo de elegibilidad (sin RD ni efecto).
Q1b  SDID con Conley-Taber (APTO solo en el escenario A, tamaño 0,0575): se comprueba si existe periodo posterior en el entrenamiento.
Q1c  Callaway-Sant'Anna (CS-Webb NO APTO): estimación puntual descriptiva, sin p-valor ni IC.
BLP/GATES de Q1: no estimable (ver docs/v16/desviaciones.md, D3).
Uso: python3 -I? no; python3 src/v16/q1_zonas.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from src.v16 import q_comun as Q

OUT = ROOT / "output" / "v16" / "q1"
G0, G1 = pd.Period("2019Q1", "Q"), pd.Period("2026Q2", "Q")


# ---------------------------------------------------------------- Q1a · elegibilidad
def inflacion_acumulada(a: str = "2018", b: str = "2023") -> float:
    m = Q.cargar("base_macro", "nacional", "inflacion_ipc_yoy")
    m = m[m.periodo.astype(str).str.endswith("T4")].set_index(m[m.periodo.astype(str).str.endswith("T4")].periodo.astype(str)).valor
    años = [str(y) + "T4" for y in range(int(a) + 1, int(b) + 1)]
    return float(np.prod([1 + m[y] / 100 for y in años]) - 1)


def q1a() -> dict:
    s = Q.cargar("base_alquiler", "municipio", "serpavi_alquiler_m2_mediana")
    s = s[s.desagregacion == "tipologia=VC"]
    w = s.pivot_table(index="territorio_codigo", columns=s.periodo.astype(str), values="valor")
    w = w.dropna(subset=["2018", "2023"])
    ipc = inflacion_acumulada()
    umbral = np.log(1 + ipc + 0.03)
    asign = np.log(w["2023"] / w["2018"]) - umbral
    z = Q.cargar("base_regulacion", "municipio", "zt_vigente")
    decl = set(z.territorio_codigo)
    d = pd.DataFrame({"asignacion": asign})
    d["prov"] = d.index.str[:2]
    d["cataluna"] = d.prov.isin(["08", "17", "25", "43"])
    d["declarado"] = d.index.isin(decl)
    d["elegible"] = d.asignacion > 0
    d["en_banda_10pts"] = d.asignacion.abs() <= 0.10
    tab = d.groupby(["cataluna", "elegible"]).agg(n=("declarado", "size"), declarados=("declarado", "sum")).reset_index()
    tab["tasa_declaracion"] = tab.declarados / tab.n
    tab.to_csv(OUT / "q1a_elegibilidad.csv", index=False)
    return {"ipc_acumulado_2018_2023": ipc, "umbral_log": float(umbral), "n_municipios": int(len(d)),
            "n_en_banda_10pts": int(d.en_banda_10pts.sum()), "n_elegibles": int(d.elegible.sum()),
            "n_declarados_en_muestra": int(d.declarado.sum()), "declarados_elegibles": int((d.declarado & d.elegible).sum()),
            "declarados_no_elegibles": int((d.declarado & ~d.elegible).sum()),
            "tasa_declaracion_elegibles": float(d[d.elegible].declarado.mean()),
            "tasa_declaracion_no_elegibles": float(d[~d.elegible].declarado.mean()),
            "tabla": tab.to_dict("records"),
            "lectura": "Recuento de elegibilidad por el criterio de precio del art. 18 (SERPAVI VC 2018-2023). No es un RD: el resultado de Q1a solo existe en la muestra sellada (adenda, punto 3)."}


# ---------------------------------------------------------------- Q1b · comprobación de periodo posterior
def q1b() -> dict:
    sys.path.insert(0, str(ROOT))
    from src.v16.montecarlo import _comun_panel as C
    z = C.zonas_tensionadas()
    zfc = z[z.ccaa != "09"].copy()
    s = C.estructura_serpavi_municipal(False)
    zfc["en_panel_serpavi"] = zfc.cod.isin(set(s.cod))
    ent = zfc[zfc.en_panel_serpavi].drop_duplicates("cod")
    sc = C.estructura_serpavi_municipal(True)
    ent_c = zfc[zfc.cod.isin(set(sc.cod))].drop_duplicates("cod")
    reg = Q.cargar("base_regulacion", "municipio", "zt_vigente")
    reg["prov"] = reg.territorio_codigo.str[:2]
    reg_fc = reg[~reg.prov.isin(["08", "17", "25", "43"])]
    # último año de SERPAVI municipal en entrenamiento
    ult = Q.cargar("base_alquiler", "municipio", "serpavi_alquiler_m2_mediana").periodo.astype(str).max()
    primer_efecto = ent.efecto.min() if len(ent) else None
    hay_post = bool(len(ent) and primer_efecto.year <= int(ult))
    # balance tratados/donantes (descriptivo, punto 5 de la adenda)
    rp = Q.cargar("renta_parque", "municipio", ["ine_adrh_renta_neta_media_hogar_eur", "ine_adrh_poblacion_personas"])
    rp = rp[rp.periodo.astype(str) == "2019"].pivot_table(index="territorio_codigo", columns="variable", values="valor")
    cen = Q.cargar("base_poblacion", "municipio", "pob_censo_anual")
    cen = cen[cen.periodo.astype(str) == "2021"].pivot_table(index="territorio_codigo", columns="desagregacion", values="valor")
    vut = Q.cargar("alquiler_turismo", "municipio")
    vut = vut[vut.variable.str.startswith("ine_vte_porcentaje") & (vut.periodo.astype(str) == "2021-02")].set_index("territorio_codigo").valor
    zc = set(z.ccaa)
    donantes = s[~s.ccaa.isin(zc)].cod
    filas = []
    for nombre, cods in (("tratados_fuera_Cataluña", list(ent.cod)), ("donantes_CCAA_sin_zonas", list(donantes))):
        c = pd.Index(cods)
        filas.append({"grupo": nombre, "n": len(c),
                      "renta_neta_hogar_ADRH_2019": float(rp.reindex(c)["ine_adrh_renta_neta_media_hogar_eur"].mean()),
                      "poblacion_2019": float(rp.reindex(c)["ine_adrh_poblacion_personas"].mean()),
                      "cuota_extranjeros_2021": float((1 - cen.reindex(c)["nacionalidad=España"] / cen.reindex(c)["nacionalidad=Total"]).mean()),
                      "pct_vivienda_turistica_2021_02": float(vut.reindex(c).mean()),
                      "exposicion_tipo_variable": None})
    bal = pd.DataFrame(filas)
    bal.to_csv(OUT / "q1b_balance.csv", index=False)
    ent[["cod", "ccaa", "efecto"]].assign(efecto=ent.efecto.astype(str)).to_csv(OUT / "q1b_tratados_fuera_cataluna.csv", index=False)
    return {"tratados_fuera_cataluna_en_panel_serpavi": int(len(ent)), "tratados_en_panel_completo_2019_2024": int(len(ent_c)),
            "primer_efecto_fuera_cataluna": None if primer_efecto is None else str(primer_efecto.date()),
            "ultimo_anio_serpavi_entrenamiento": ult, "zt_vigente_fuera_cataluna_antes_2025": int((reg_fc.periodo.astype(str) < "2025").sum()),
            "hay_periodo_posterior_en_entrenamiento": hay_post,
            "veredicto": ("estimable" if hay_post else "NO ESTIMABLE en el entrenamiento; pendiente de la evaluación sellada"),
            "inferencia": "SDID con Conley-Taber APTA solo en el escenario A (tamaño 0,0575, en el límite superior de [0,04; 0,06]); no se usa porque no hay periodo posterior",
            "potencia": "MDE 7,1 % frente a −0,75 % de referencia: sin potencia (adenda, punto 5)",
            "balance": bal.to_dict("records")}


# ---------------------------------------------------------------- Q1c · Callaway-Sant'Anna descriptivo
def panel_cv(prov_excluir=()) -> pd.DataFrame:
    x = Q.trimestral(Q.cargar("base_precio", "provincia", "compraventas"))
    w = x.pivot_table(index="territorio_codigo", columns="q", values="valor")
    w = w.loc[:, (w.columns >= G0) & (w.columns <= G1)]
    w = np.log(w.where(w > 0))
    return w.drop(index=list(prov_excluir), errors="ignore")


def cohortes() -> dict:
    r = Q.cargar("base_regulacion", "municipio", "zt_vigente")
    r["prov"] = r.territorio_codigo.str[:2]
    r["q"] = pd.PeriodIndex([f"{v[:4]}Q{v[-1]}" for v in r.periodo.astype(str)], freq="Q")
    return r.groupby("prov").q.min().to_dict()


def cs_att(w: pd.DataFrame, coh: dict, desplaza: int = 0, t_max: dict | None = None, ventana_ev=(-8, 6)):
    """ATT(g,t) de Callaway-Sant'Anna sin regresores: nunca tratadas como comparación, base g−1 (universal).

    desplaza: adelanta la cohorte (placebo de fecha). t_max: por provincia, último periodo utilizable (placebo: antes del tratamiento real)."""
    trat = {p: g - desplaza for p, g in coh.items() if p in w.index}
    nunca = [p for p in w.index if p not in coh]
    filas = []
    for g in sorted(set(trat.values())):
        gi = [p for p, gg in trat.items() if gg == g]
        base = g - 1
        if base not in w.columns:
            continue
        for t in w.columns:
            e = (t - g).n
            if e < ventana_ev[0] or e > ventana_ev[1] or t == base:
                continue
            if t_max is not None:
                gi_t = [p for p in gi if t <= t_max[p]]
            else:
                gi_t = gi
            if not gi_t:
                continue
            dy_t = (w.loc[gi_t, t] - w.loc[gi_t, base]).mean()
            dy_c = (w.loc[nunca, t] - w.loc[nunca, base]).mean()
            filas.append({"g": str(g), "t": str(t), "e": e, "N_g": len(gi_t), "att": float(dy_t - dy_c)})
    d = pd.DataFrame(filas).dropna()
    post = d[d.e >= 0]
    glob = float((post.att * post.N_g).sum() / post.N_g.sum()) if len(post) else None
    ev = d.groupby("e").apply(lambda x: float((x.att * x.N_g).sum() / x.N_g.sum()), include_groups=False)
    pre = d[d.e < -1]
    return d, glob, ev, (float(pre.att.abs().mean()) if len(pre) else None), (float(pre.att.mean()) if len(pre) else None)


def q1c(registro: list) -> dict:
    coh = cohortes()
    w = panel_cv()
    d, glob, ev, pre_abs, pre_mean = cs_att(w, coh)
    d.to_csv(OUT / "q1c_att_gt.csv", index=False)
    ev.rename("att").reset_index().to_csv(OUT / "q1c_evento.csv", index=False)
    registro.append({"id": "Q1c-P", "pregunta": "Q1c", "rol": "principal", "especificacion": "CS sin regresores, nunca tratadas, base g-1; log compraventas provincial trimestral 2019T1-2026T2",
                     "muestra": f"{w.shape[0]} provincias ({len(coh)} tratadas)", "n": int(w.shape[0] * w.shape[1]), "estimacion": glob, "unidad": "Δlog (ATT global)",
                     "inferencia": "ninguna (CS-Webb NO APTO)", "nota": "incluye Cataluña (solapa con H1/H2)"})
    # sin grandes ciudades (punto 14): fuera la provincia de Barcelona (tratada) y las de València, Sevilla y Málaga (controles)
    w2 = panel_cv(prov_excluir=Q.GRANDES_PROV.keys())
    coh2 = {p: g for p, g in coh.items() if p in w2.index}
    d2, glob2, ev2, *_ = cs_att(w2, coh2)
    registro.append({"id": "Q1c-X1", "pregunta": "Q1c", "rol": "robustez (punto 14)", "especificacion": "sin Barcelona, València, Sevilla y Málaga (provincias)",
                     "muestra": f"{w2.shape[0]} provincias ({len(coh2)} tratadas)", "n": int(w2.shape[0] * w2.shape[1]), "estimacion": glob2, "unidad": "Δlog (ATT global)",
                     "inferencia": "ninguna", "nota": "islas no selladas: ninguna (Baleares y Canarias son de v6)"})
    # solo Cataluña tratada / solo País Vasco y Galicia: NO declarado -> no se hace (ver desviaciones)
    # placebo de fecha: cohortes 8 trimestres antes, solo datos anteriores al tratamiento real
    tmax = {p: g - 1 for p, g in coh.items()}
    dp, globp, evp, *_ = cs_att(w, coh, desplaza=8, t_max=tmax, ventana_ev=(0, 7))
    registro.append({"id": "Q1c-PL1", "pregunta": "Q1c", "rol": "placebo de fecha", "especificacion": "cohortes adelantadas 8 trimestres, datos hasta g_real−1",
                     "muestra": f"{w.shape[0]} provincias", "n": int(len(dp)), "estimacion": globp, "unidad": "Δlog (ATT placebo)", "inferencia": "ninguna", "nota": "debería estar cerca de 0"})
    # balance (descriptivo)
    prov = list(w.index)
    cv = Q.covariables_provincia(prov)
    cv["pct_vut_2020_08"] = Q.vut_provincia(prov)
    cv["tratada"] = [p in coh for p in prov]
    cols = ["ln_renta", "ln_pob", "cuota_extranj", "pct_vut_2020_08", "obra_pc"]
    bal = []
    for c in cols:
        a, b = cv[cv.tratada][c].dropna(), cv[~cv.tratada][c].dropna()
        sd = np.sqrt((a.var() + b.var()) / 2)
        bal.append({"variable": c, "media_tratadas": float(a.mean()), "media_no_tratadas": float(b.mean()), "dif_estandarizada": float((a.mean() - b.mean()) / sd)})
    pd.DataFrame(bal).to_csv(OUT / "q1c_balance.csv", index=False)
    # ajuste preintervención y diagnósticos de corte (Δ post − pre por provincia)
    pre_cols = [c for c in w.columns if c < pd.Period("2024Q1", "Q")]
    post_cols = [c for c in w.columns if c >= pd.Period("2024Q1", "Q")]
    dd = (w[post_cols].mean(axis=1) - w[pre_cols].mean(axis=1)).rename("dy").to_frame().join(cv)
    dd = dd.dropna(subset=["ln_renta", "ln_pob", "cuota_extranj"])
    corto = Q.ols_corte(dd.dy.values, dd.tratada.astype(float).values)
    largo = Q.ols_corte(dd.dy.values, dd.tratada.astype(float).values, dd[["ln_renta", "ln_pob", "cuota_extranj"]].values)
    sens = Q.sensibilidad(corto, largo)
    cen, _ = Q.centroides_provincia()
    mor = Q.moran(largo["residuos"], np.array([cen[p] for p in dd.index]))
    bp = Q.breusch_pagan(largo["residuos"], dd[["ln_renta", "ln_pob", "cuota_extranj"]].values)
    registro.append({"id": "Q1c-D1", "pregunta": "Q1c", "rol": "diagnóstico", "especificacion": "diferencia de corte post(2024T1+)−pre sobre tratada, con controles 2019",
                     "muestra": f"{len(dd)} provincias", "n": len(dd), "estimacion": largo["beta"], "unidad": "Δlog", "inferencia": "ninguna", "nota": "base de Oster/CH/E-value/Moran/BP"})
    # Bai-Perron sobre la brecha media tratadas − nunca tratadas
    from src.econ_utils import bai_perron
    gap = (w.loc[[p for p in w.index if p in coh]].mean() - w.loc[[p for p in w.index if p not in coh]].mean())
    gap.index = pd.PeriodIndex(gap.index, freq="Q")
    try:
        bpr = bai_perron(gap, pd.DataFrame({"c": np.ones(len(gap))}, index=gap.index), max_bkps=2, min_size=6)
    except Exception as e:  # pragma: no cover
        bpr = {"error": str(e)}
    pre_e = ev[ev.index < -1]
    return {"att_global": glob, "att_global_sin_grandes_ciudades": glob2, "att_placebo_fecha": globp,
            "evento": {int(k): float(v) for k, v in ev.items()}, "pretendencia": {"media_abs_pre": pre_abs, "media_pre": pre_mean, "media_coef_pre_evento": float(pre_e.mean()) if len(pre_e) else None},
            "n_provincias": int(w.shape[0]), "n_tratadas": len(coh), "cohortes": {p: str(g) for p, g in coh.items()},
            "balance": bal, "sensibilidad_corte": sens, "moran_residuos": mor, "breusch_pagan": bp, "bai_perron_brecha": bpr,
            "att_por_cohorte": d[d.e >= 0].groupby("g").apply(lambda x: float(x.att.mean()), include_groups=False).to_dict()}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    registro: list = []
    r1a = q1a()
    r1b = q1b()
    registro.append({"id": "Q1a-D", "pregunta": "Q1a", "rol": "diagnóstico descriptivo", "especificacion": "recuento de elegibilidad art. 18 (SERPAVI VC 2018-2023)",
                     "muestra": f"{r1a['n_municipios']} municipios", "n": r1a["n_municipios"], "estimacion": r1a["tasa_declaracion_elegibles"], "unidad": "tasa de declaración entre elegibles", "inferencia": "ninguna", "nota": "sin RD"})
    registro.append({"id": "Q1b-P", "pregunta": "Q1b", "rol": "principal", "especificacion": "SDID Conley-Taber (2019-2022 vs 2024; 2023 fuera)", "muestra": f"{r1b['tratados_fuera_cataluna_en_panel_serpavi']} tratados fuera de Cataluña",
                     "n": 0, "estimacion": None, "unidad": "Δlog SERPAVI", "inferencia": "Conley-Taber (escenario A)", "nota": r1b["veredicto"]})
    r1c = q1c(registro)
    Q.registro(registro, OUT / "registro.csv")
    Q.jdump({"q1a": r1a, "q1b": r1b, "q1c": r1c}, OUT / "q1_detalle.json")
    print(r1b["veredicto"], r1b["primer_efecto_fuera_cataluna"], "ATT", r1c["att_global"], r1c["att_global_sin_grandes_ciudades"], r1c["att_placebo_fecha"])


if __name__ == "__main__":
    main()
