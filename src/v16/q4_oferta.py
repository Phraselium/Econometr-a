"""V16 · fase 6 · Q4a y Q4b: oferta municipal y restricción física (% de superficie en Red Natura 2000). Adenda, puntos 3 y 8.

Q4a: log obra nueva neta del Catastro (obra > 0), municipal 2018-2025, ~ % Red Natura (estandarizado) + FE de provincia y año.
Q4b: Δlog SERPAVI municipal (VC) 2018-2022 ~ choque de Q3 (Δ del shift-share municipal) × % Red Natura + choque + FE de municipio y año.
Agrupación por provincia: rejilla TWFE NO APTA (output/v16/montecarlo/veredictos.csv) → SOLO estimación puntual, sin p-valor ni IC.
Capa C4, descriptiva; la Red Natura no se presenta como exógena. Ejecución: python src/v16/q4_oferta.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qb_comun as C  # noqa: E402
import qb_shiftshare as S  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = C.RAIZ / "output" / "v16" / "q4"


def red_natura() -> pd.Series:
    d = C.cargar("oferta_suelo_terceros", "miteco_rn2000_porcentaje_superficie_municipal", "municipio")
    return d.groupby("territorio_codigo").valor.first().rename("rn")


def q4a(reg, res):
    rn = red_natura()
    ob = C.anual(C.cargar("base_oferta", "obra_nueva_neta_catastro", "municipio"), "obra").reset_index()
    ur = C.anual(C.cargar("base_oferta", "catastro_unidades_urbanas_residenciales", "municipio"), "ur").reset_index()
    ur17 = ur[ur.t == 2017].set_index("u").ur.rename("ur17")
    base = ob.merge(rn, left_on="u", right_index=True).merge(ur17, left_on="u", right_index=True, how="left")
    base["prov"] = base.u.str[:2]
    out = []
    for transf, ctrl, vent in itertools.product(["log_pos", "asinh"], ["sin", "log_unidades_2017"], [(2018, 2025), (2018, 2021)]):
        d = base[(base.t >= vent[0]) & (base.t <= vent[1])].copy()
        if transf == "log_pos":
            d = d[d.obra > 0]
            d["y"] = np.log(d.obra)
        else:
            d["y"] = np.arcsinh(d.obra)
        cols = []
        if ctrl != "sin":
            d = d[d.ur17 > 0]
            d["lur"] = np.log(d.ur17)
            cols = ["lur"]
        d = d.dropna(subset=["y", "rn"] + cols)
        mu, sd = base.drop_duplicates("u").rn.mean(), base.drop_duplicates("u").rn.std()
        d["x"] = (d.rn - mu) / sd
        r = C.mco_fe(d.y.values, d[["x"] + cols].values, [C.codif(d.prov), C.codif(d.t)])
        principal = (transf, ctrl, vent) == ("log_pos", "sin", (2018, 2025))
        mid = f"Q4a|{transf}|{ctrl}|{vent[0]}-{vent[1]}" + ("|PRINCIPAL" if principal else "")
        reg.log("v16-fase6", mid, "y ~ RN_std (+control) + FE provincia + FE año", vent[0], vent[1], r["n"], r["r2_total"], np.nan, np.nan, np.nan, float(r["beta"][0]), np.nan, "puntual; agrupación provincial NO APTA")
        out.append({"id": mid, "beta_por_DT": float(r["beta"][0]), "n": r["n"], "r2": r["r2_total"], "principal": principal})
        if principal:
            P, dP = r, d
    E = pd.DataFrame(out)
    b0 = float(P["beta"][0])
    q = {"principal": {"beta_por_DT_RN": b0, "n": P["n"], "n_municipios": int(dP.u.nunique()), "r2_total": P["r2_total"], "r2_within": P["r2_within"],
                       "sd_rn_entre_municipios_pp": float(base.drop_duplicates("u").rn.std())},
         "multiverso": {"n": len(E), "mediana": float(E.beta_por_DT.median()), "min": float(E.beta_por_DT.min()), "max": float(E.beta_por_DT.max()),
                        "proporcion_mismo_signo": float((np.sign(E.beta_por_DT) == np.sign(b0)).mean())},
         "especificaciones": out}
    dg = {}
    x0 = C.mco_fe(dP.y.values, dP.x.values, [np.zeros(len(dP), int)])
    dg["oster"] = {"beta_sin_FE": float(x0["beta"][0]), "r2_sin_FE": x0["r2_total"], "beta_con_FE": b0, "r2_con_FE": P["r2_total"],
                   "delta_beta0_rmax1_3": C.oster_delta(float(x0["beta"][0]), x0["r2_total"], b0, P["r2_total"])}
    dl = dg["oster"]["delta_beta0_rmax1_3"]
    dg["oster"]["fragil_delta_lt_1"] = bool(np.isfinite(dl) and 0 <= dl < 1)
    dg["e_value_punto"] = C.e_value_puntual(b0, float(P["sdx_t"][0]), P["sdy_t"])
    dg["cinelli_hazlett"] = "no calculado: requiere t con inferencia APTA (agrupación provincial NO APTA)"
    dg["het_autocorr"] = C.heterocedasticidad_autocorr(P["resid"], P["Xt"][:, 0], dP.u.values, dP.t.values)
    # Moran sobre residuos medios por municipio
    m = pd.read_parquet(C.RAIZ / "data/base/geo/municipios.parquet", columns=["cod_municipio", "geometry"])
    m = m[m.cod_municipio.isin(dP.u.unique())].reset_index(drop=True)
    xyz = C.centroides(m)
    rm = pd.Series(P["resid"]).groupby(dP.u.values).mean().reindex(m.cod_municipio)
    ok = rm.notna().values
    dg["moran_residuos_municipios"] = C.moran(rm.values[ok], xyz[ok])
    ex = dP[~dP.u.isin(C.GRANDES_MUN)]
    r2 = C.mco_fe(ex.y.values, ex[["x"]].values, [C.codif(ex.prov), C.codif(ex.t)])
    dg["sin_grandes_ciudades"] = {"beta": float(r2["beta"][0]), "n": r2["n"], "excluidos": sorted(C.GRANDES_MUN), "islas": "ninguna no sellada"}
    reg.log("v16-fase6", "Q4a|excl_grandes", "idem sin 4 ciudades", 2018, 2025, r2["n"], r2["r2_total"], np.nan, np.nan, np.nan, float(r2["beta"][0]), np.nan, "diagnóstico")
    # placebo de periodo: 2012-2016 (regularización catastral 2013-2017: no es placebo limpio, se declara)
    dpl = base[(base.t >= 2012) & (base.t <= 2016) & (base.obra > 0)].copy()
    mu, sd = base.drop_duplicates("u").rn.mean(), base.drop_duplicates("u").rn.std()
    dpl["x"] = (dpl.rn - mu) / sd
    rp = C.mco_fe(np.log(dpl.obra.values), dpl[["x"]].values, [C.codif(dpl.prov), C.codif(dpl.t)])
    dg["periodo_regularizacion_2012_2016"] = {"beta": float(rp["beta"][0]), "n": rp["n"], "nota": "periodo excluido del principal por la regularización catastral de 2013-2017; no es placebo"}
    dg["magnitud_referencia"] = "ninguna (b no se cumple)"
    q["diagnosticos"] = dg
    return q


def q4b(reg, res):
    rn = red_natura()
    s = S.shiftshare("municipio", 2003)
    x = pd.DataFrame(s["x"], index=s["unidades"], columns=s["años"])
    x[s["pob"][:, s["ib"]] <= 0] = np.nan
    shock = x.diff(axis=1).stack().rename("shock")
    shock.index.names = ["u", "t"]
    out = []
    P = None
    for tip, vent, fe in itertools.product(["VC", "VU"], [(2018, 2022), (2018, 2020)], ["año", "provincia×año"]):
        a = C.cargar("base_alquiler", "serpavi_alquiler_m2_mediana", "municipio", f"tipologia={tip}")
        y = np.log(C.anual(a, "ly").where(lambda s_: s_ > 0))
        dy = y.groupby(level=0).diff().rename("dy")
        d = pd.concat([dy, shock], axis=1, join="inner").dropna().reset_index()
        d = d.merge(rn, left_on="u", right_index=True)
        d = d[(d.t >= vent[0]) & (d.t <= vent[1])]
        d["prov"] = d.u.str[:2]
        d["rnz"] = (d.rn - rn.mean()) / rn.std()
        d["inter"] = d.shock * d.rnz
        grupos = [C.codif(d.t)] if fe == "año" else [C.codif(d.prov + d.t.astype(str))]
        r = C.mco_fe(d.dy.values, d[["inter", "shock"]].values, grupos)  # el efecto fijo de municipio se absorbe al diferenciar
        principal = (tip, vent, fe) == ("VC", (2018, 2022), "año")
        mid = f"Q4b|{tip}|{vent[0]}-{vent[1]}|{fe}" + ("|PRINCIPAL" if principal else "")
        reg.log("v16-fase6", mid, "Δlog SERPAVI ~ choque×RN_std + choque + FE año (FE municipio absorbido en Δ)", vent[0], vent[1], r["n"], r["r2_total"], np.nan, np.nan, np.nan,
                float(r["beta"][0]), np.nan, "puntual; agrupación provincial NO APTA")
        out.append({"id": mid, "beta_interaccion": float(r["beta"][0]), "beta_choque": float(r["beta"][1]), "n": r["n"], "principal": principal})
        if principal:
            P, dP = r, d
    E = pd.DataFrame(out)
    b0 = float(P["beta"][0])
    q = {"principal": {"beta_interaccion_por_DT_RN_y_punto_de_choque": b0, "beta_choque_main": float(P["beta"][1]), "n": P["n"],
                       "n_municipios": int(dP.u.nunique()), "r2_total": P["r2_total"], "r2_within": P["r2_within"]},
         "multiverso": {"n": len(E), "mediana": float(E.beta_interaccion.median()), "min": float(E.beta_interaccion.min()), "max": float(E.beta_interaccion.max()),
                        "proporcion_mismo_signo": float((np.sign(E.beta_interaccion) == np.sign(b0)).mean())},
         "especificaciones": out}
    dg = {}
    dg["e_value_punto"] = C.e_value_puntual(b0, float(P["sdx_t"][0]), P["sdy_t"])
    dg["het_autocorr"] = C.heterocedasticidad_autocorr(P["resid"], P["Xt"][:, 0], dP.u.values, dP.t.values)
    ex = dP[~dP.u.isin(C.GRANDES_MUN)]
    r2 = C.mco_fe(ex.dy.values, ex[["inter", "shock"]].values, [C.codif(ex.t)])
    dg["sin_grandes_ciudades"] = {"beta_interaccion": float(r2["beta"][0]), "n": r2["n"], "excluidos": sorted(C.GRANDES_MUN), "islas": "ninguna no sellada"}
    reg.log("v16-fase6", "Q4b|excl_grandes", "idem sin 4 ciudades", 2018, 2022, r2["n"], r2["r2_total"], np.nan, np.nan, np.nan, float(r2["beta"][0]), np.nan, "diagnóstico")
    # pretendencia: la interacción con el choque adelantado un año (choque t+1)
    sh1 = shock.groupby(level=0).shift(-1).rename("shock_f")
    d = dP.merge(sh1.reset_index(), on=["u", "t"], how="left").dropna(subset=["shock_f"])
    d["inter_f"] = d.shock_f * d.rnz
    rl = C.mco_fe(d.dy.values, d[["inter_f", "shock_f"]].values, [C.codif(d.t)])
    dg["placebo_choque_adelantado"] = {"beta_interaccion": float(rl["beta"][0]), "n": rl["n"], "lectura": "puntual; una interacción adelantada no nula sería señal de tendencias previas"}
    reg.log("v16-fase6", "Q4b|placebo_adelantado", "Δlog ~ choque(t+1)×RN", 2018, 2021, rl["n"], rl["r2_total"], np.nan, np.nan, np.nan, float(rl["beta"][0]), np.nan, "diagnóstico")
    # balance: RN frente a renta/población (corte transversal municipal)
    dg["magnitud_referencia"] = "ninguna (b no se cumple)"
    dg["nota"] = "choque de Q3 construido con el padrón hasta 2022 (D2): la ventana es 2018-2022"
    q["diagnosticos"] = dg
    return q


def main():
    reg = Registry(OUT / "registro.csv")
    OUT.mkdir(parents=True, exist_ok=True)
    res = {"Q4a": q4a(reg, None), "Q4b": q4b(reg, None)}
    C.volcar(OUT / "q4_resultado_parcial.json", res)
    reg.flush()
    for k, v in res.items():
        print(k, v["principal"], v["multiverso"])
        print(v["diagnosticos"])


if __name__ == "__main__":
    main()
