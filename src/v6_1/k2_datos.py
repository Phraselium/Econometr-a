"""K2 (v6.1): construccion de los paneles de trabajo. Solo entrenamiento (holdout.load_train via v2_common) y ficheros
versionados de output/v6/M0/paneles (entrenamiento) y data/processed. No abre data/sealed. Sin red.

Muestra: las 41 provincias de entrenamiento de v6 (las 11 selladas de v6 quedan fuera) y, para los datos de v2, las
provincias de entrenamiento de v2 que coinciden (38). Nacional y CCAA son series publicadas en v1 que agregan todas las
provincias (se declara en las notas).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v2"))
PAN = RAIZ / "output/v6/M0/paneles"
PROC = RAIZ / "data/processed"
ANIOS = list(range(2002, 2025))

V6REG = ["share_ext_pob", "ln_pob", "ln_pib_pc", "paro_tasa", "ln_ocupados_miles", "ln_terminadas_libres",
         "ln_iniciadas_libres", "ln_hip_viv_num", "ln_vut", "share_compra_ext_res_pct"]
NUCLEO = ["l1_ln_pob", "l1_ln_pib_pc", "l1_paro_tasa", "l1_ln_ocupados_miles", "l1_ln_terminadas_libres",
          "l1_ln_iniciadas_libres", "l1_ln_hip_viv_num"]


def _train_codes():
    return sorted(pd.read_csv(PAN / "prov_compra_anual_train.csv.gz")["cod"].unique().tolist())


def _grid(codes):
    return pd.DataFrame([(c, a) for c in codes for a in ANIOS], columns=["cod", "anio"])


def _lag(U, cols, k=1, pref="l"):
    g = U.groupby("cod")
    for c in cols:
        U[f"{pref}{k}_{c}"] = g[c].shift(k)


def cargar(smoke=False):
    """Devuelve (U, meta). U: provincia-anio 2002-2024 con variables de v2 (2SLS shift-share, flujos, stocks) y de v6."""
    import bi_core as bc  # noqa: E402
    codes = _train_codes()
    if smoke:
        codes = codes[:14]
    orig = bc.vc.load

    def load(nombre):
        d = orig(nombre)
        if nombre == "panel_prov_a":
            d = d[d["cod_prov"].astype(int).isin(codes)]
        return d

    bc.vc.load = load
    try:
        d, _ = bc.construir_panel()
    finally:
        bc.vc.load = orig
    d = d.rename(columns={"cod_prov": "cod"})
    d["cod"] = d["cod"].astype(int)
    keep = ["cod", "anio", "cod_ccaa", "x", "x_stock", "z", "z_fwd", "pop_l", "y_alq", "y_pre", "y_dif", "pob_total",
            "pob_extranj", "inmig_flujo", "p_tasado", "ipc_alquiler", "serpavi_mediana_vc", "ipva_indice", "ocupados",
            "parados", "pib_pc", "iniciadas_libres_anual", "vut_viviendas", "costa", "extr02"]
    d = d[keep]
    pc = pd.read_csv(PAN / "prov_compra_anual_train.csv.gz")
    pa = pd.read_csv(PAN / "prov_alquiler_anual_train.csv.gz")
    pc = pc[pc["cod"].isin(codes)]
    pa = pa[pa["cod"].isin(codes)]
    c6 = ["ln_pm2_tasado", "ln_pm2_registradores", "no_res_share_R1A_pct", "ln_cv_etdp"] + V6REG
    c6 = [c for c in dict.fromkeys(c6) if c in pc.columns and c != "ln_vut"]
    U = _grid(codes).merge(d, on=["cod", "anio"], how="left")
    U = U.merge(pc[["cod", "anio"] + c6], on=["cod", "anio"], how="left")
    U = U.merge(pa[["cod", "anio", "ln_alq_m2_serpavi_vc", "ln_alq_mes_serpavi_vc", "ln_ipc_alq_idx", "ln_vut"]],
                on=["cod", "anio"], how="left")
    est = pd.read_csv(PAN / "prov_estatico.csv")
    est = est[["cod", "costa", "isla", "costa_sol", "pct_no_principal_2021"]].rename(columns={"costa": "costa6"})
    U = U.merge(est, on="cod", how="left")
    nr = pc[pc["anio"].isin([2015, 2016])].groupby("cod")["no_res_share_R1A_pct"].mean().rename("nores_1516")
    U = U.merge(nr, on="cod", how="left")
    U = U.sort_values(["cod", "anio"]).reset_index(drop=True)
    g = U.groupby("cod")
    # variables de v2 derivadas
    U["cuota"] = 100 * U["pob_extranj"] / U["pob_total"]
    U["d_cuota"] = g["cuota"].diff()
    U["ln_pop_l"] = np.log(U["pop_l"])
    U["y_alq_ser"] = 100 * g["serpavi_mediana_vc"].transform(lambda s: np.log(s).diff())
    U["y_pre_nom"] = 100 * g["p_tasado"].transform(lambda s: np.log(s).diff())
    U["y_pre_reg"] = 100 * g["ln_pm2_registradores"].diff()
    U["y_pre_ipv"] = 100 * g["ipva_indice"].transform(lambda s: np.log(s).diff())
    U["y_pre_t6"] = 100 * g["ln_pm2_tasado"].diff()
    U["y_alq6"] = 100 * g["ln_alq_m2_serpavi_vc"].diff()
    U["y_ipc6"] = 100 * g["ln_ipc_alq_idx"].diff()
    U["lv_ipc2"] = 100 * np.log(U["ipc_alquiler"])
    U["lv_ser2"] = 100 * np.log(U["serpavi_mediana_vc"])
    U["lv_tas2"] = 100 * np.log(U["p_tasado"])
    U["lv_tas6"] = 100 * U["ln_pm2_tasado"]
    U["lv_reg6"] = 100 * U["ln_pm2_registradores"]
    U["lv_alq6"] = 100 * U["ln_alq_m2_serpavi_vc"]
    U["lv_ipc6"] = 100 * U["ln_ipc_alq_idx"]
    U["lv_ipv"] = 100 * np.log(U["ipva_indice"])
    # empleo, renta, iniciadas (v2): variacion en pp
    U["g_ocup"] = 100 * g["ocupados"].transform(lambda s: np.log(s).diff())
    U["g_pib_pc"] = 100 * g["pib_pc"].transform(lambda s: np.log(s).diff())
    U["g_inic"] = 100 * g["iniciadas_libres_anual"].transform(lambda s: np.log(s.where(s > 0)).diff())
    U["g_vut_v2"] = 100 * g["vut_viviendas"].transform(lambda s: np.log(s.where(s > 0)).diff())
    for c in ["ocupados", "pib_pc"]:
        U[f"lag_g_{c}"] = g[f"g_{'ocup' if c == 'ocupados' else 'pib_pc'}"].shift(1)
    _lag(U, V6REG + ["cuota"], 1)
    _lag(U, V6REG + ["cuota"], 2)
    for c in V6REG + ["cuota"]:
        U[f"dl1_{c}"] = U[f"l1_{c}"] - U[f"l2_{c}"]
    t0 = 2019
    U["t_c"] = U["anio"] - t0
    U["costa_lvl"] = U["costa6"]
    U["nop_lvl"] = U["pct_no_principal_2021"]
    U["nores_lvl"] = U["nores_1516"]
    U["tend_costa"] = U["costa6"] * U["t_c"]
    U["tend_nop"] = U["pct_no_principal_2021"] * U["t_c"] / 10.0
    U["tend_nores"] = U["nores_1516"] * U["t_c"] / 10.0
    meta = dict(codes=codes, n_codes=len(codes),
                renta_media=float(np.exp(pa["ln_alq_mes_serpavi_vc"]).mean()),
                precio_medio=float(np.exp(pc["ln_pm2_tasado"]).mean()),
                islas_en_train=int(est.loc[est["cod"].isin(codes), "isla"].fillna(0).sum()),
                costa_en_train=int(est.loc[est["cod"].isin(codes), "costa6"].fillna(0).sum()),
                n_v2=int(d["cod"].nunique()))
    return U, meta


def dummies_x(m, var, tag):
    """Variable invariante por provincia x dummies de anio (control de choques anuales distintos segun var)."""
    A = pd.get_dummies(m["anio"], dtype=float)
    out = A.mul(m[var].to_numpy(float), axis=0)
    out.columns = [f"{tag}_{int(c)}" for c in A.columns]
    return out


def municipal(codes):
    """Panel municipal de v2 (entrenamiento) restringido a las provincias de entrenamiento de v6."""
    m = pd.read_csv(RAIZ / "data/processed/v2/train/panel_muni_a.csv",
                    usecols=["cod_muni", "cod_prov", "anio", "serpavi_mediana_vc", "p_tasado", "vut_viviendas"])
    m = m[m["cod_prov"].isin(codes)].sort_values(["cod_muni", "anio"]).reset_index(drop=True)
    g = m.groupby("cod_muni")
    m["y_alq_ser"] = 100 * g["serpavi_mediana_vc"].transform(lambda s: np.log(s.where(s > 0)).diff())
    m["y_pre_nom"] = 100 * g["p_tasado"].transform(lambda s: np.log(s.where(s > 0)).diff())
    m["lv_ser"] = 100 * np.log(m["serpavi_mediana_vc"].where(m["serpavi_mediana_vc"] > 0))
    m["lv_tas"] = 100 * np.log(m["p_tasado"].where(m["p_tasado"] > 0))
    m["ln_vut_m"] = np.log(m["vut_viviendas"].where(m["vut_viviendas"] > 0))
    m["l1_ln_vut_m"] = m.groupby("cod_muni")["ln_vut_m"].shift(1)
    return m


def ccaa(max_anio=2023):
    c = pd.read_csv(PROC / "panel_ccaa_a.csv")
    c = c[c["anio"].between(2002, max_anio)].sort_values(["ccaa", "anio"]).reset_index(drop=True)
    g = c.groupby("ccaa")
    c["pop_l"] = g["pob_total"].shift(1)
    c["x_stock"] = 100 * g["pob_extranj"].diff() / c["pop_l"]
    c["cuota"] = 100 * c["pob_extranj"] / c["pob_total"]
    c["d_cuota"] = g["cuota"].diff()
    c["y_alq"] = 100 * g["ipc_alquiler"].transform(lambda s: np.log(s).diff())
    c["y_pre_nom"] = 100 * g["p_tasado"].transform(lambda s: np.log(s).diff())
    c["y_pre_ipv"] = 100 * g["ipv"].transform(lambda s: np.log(s).diff())
    c["y_alq_ser"] = 100 * g["serpavi_vc_mediana"].transform(lambda s: np.log(s).diff())
    c["cod"] = pd.factorize(c["ccaa"])[0]
    return c


def nacional(max_anio=2023):
    q = pd.read_csv(PROC / "nacional_q.csv")
    q["anio"] = q["trimestre"].astype(str).str[:4].astype(int)
    a = q.groupby("anio").agg(ipc_alquiler=("ipc_alquiler", "mean"), p_tasado=("p_tasado", "mean"),
                              ipv=("ipv", "mean"), pob_total=("pob_total", "first"), pob_extranj=("pob_extranj", "first"),
                              n_q=("ipc_alquiler", "count")).reset_index()
    na = pd.read_csv(PROC / "nacional_a.csv")[["anio", "inmig_anual", "quiebre_emcr_2021"]]
    a = a.merge(na, on="anio", how="left")
    a = a[a["anio"].between(2002, max_anio)].sort_values("anio").reset_index(drop=True)
    a["pop_l"] = a["pob_total"].shift(1)
    a["x_stock"] = 100 * a["pob_extranj"].diff() / a["pop_l"]
    a["x_flujo"] = 100 * a["inmig_anual"] / a["pop_l"]
    a["y_alq"] = 100 * np.log(a["ipc_alquiler"]).diff()
    a["y_pre_nom"] = 100 * np.log(a["p_tasado"]).diff()
    a["y_pre_ipv"] = 100 * np.log(a["ipv"]).diff()
    return a
