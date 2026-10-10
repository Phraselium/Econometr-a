"""CA · Tres ángulos (determinista, sin red). Lee data/raw (versionado) y data/raw/v5/ca_*.csv.

C4: comparación europea (Eurostat): posición de España en la UE-27.
C1: crédito a construcción y actividades inmobiliarias (BdE) y su relación descriptiva con las iniciadas.
C3: compras al contado frente a hipotecarias (INE, Registradores).
Salidas en output/v5/CA/. SEED = 20261010, un solo hilo.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry, dm_test, holm  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
V5 = RAW / "v5"
OUT = RAIZ / "output" / "v5" / "CA"
TAB, FIG = OUT / "tablas", OUT / "figuras"
for d in (TAB, FIG):
    d.mkdir(parents=True, exist_ok=True)
REG = Registry(OUT / "registro.csv")
SMOKE = os.environ.get("CA_SMOKE") == "1"

UE27 = ("AT BE BG HR CY CZ DK EE FI FR DE EL HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE").split()
HECHOS: list[dict] = []


def hecho(id_, indicador, valor, unidad, periodo, cobertura, fuentes, capa, fecha, mn=None, mx=None):
    HECHOS.append({"id": id_, "indicador": indicador, "valor": None if valor is None else round(float(valor), 3),
                   "min": mn, "max": mx, "unidad": unidad, "periodo": periodo, "cobertura": cobertura,
                   "fuentes": fuentes, "capa": capa, "fecha_dato": fecha})


# ======================================================================= C4 · Europa
def wide_eu(f, filtro, col="valor", geo="geo", tiempo="periodo"):
    d = pd.read_csv(RAW / f)
    d = d[d.serie.str.startswith(filtro)]
    d = d[d[tiempo].astype(str).str.fullmatch(r"\d{4}")]
    d["y"] = d[tiempo].astype(int)
    return d.pivot_table(index="y", columns=geo, values=col)


def wide_new(f, filtros):
    d = pd.read_csv(V5 / f)
    for k, v in filtros.items():
        d = d[d[k] == v]
    d = d[d.time.astype(str).str.fullmatch(r"\d{4}")]
    d["y"] = d.time.astype(int)
    return d.pivot_table(index="y", columns="geo", values="valor"), d.actualizado.iloc[0][:10]


def europa():
    hpi = wide_eu("eu_hpi.csv", "prc_hpi_a|A|TOTAL|I15_A_AVG")
    hicp = wide_eu("eu_hicp.csv", "prc_hicp_aind|A|INX_A_AVG|CP00")
    renta = wide_eu("eu_hicp_rent.csv", "prc_hicp_aind|A|INX_A_AVG|CP041")
    rb = lambda w: w / w.loc[2015] * 100  # noqa: E731
    hpi_real = rb(rb(hpi) / rb(hicp)) if False else rb(hpi) / rb(hicp) * 100
    renta_real = rb(renta) / rb(hicp) * 100
    perm = wide_eu("eu_permits.csv", "sts_cobp_a|A|BPRM_DW")
    pop = wide_eu("eu_migr_pop.csv", "demo_pjan|A|NR|TOTAL|T")
    perm1000 = perm / pop.reindex(perm.index) * 1000 * 1000  # miles de viviendas -> viviendas por 1.000 hab.
    sob, f1 = wide_new("ca_eurostat_ilc_lvho07a.csv", {"age": "TOTAL", "sex": "T", "rskpovth": "TOTAL"})
    hac, f2 = wide_new("ca_eurostat_ilc_lvho05a.csv", {"age": "TOTAL", "sex": "T", "rskpovth": "TOTAL"})
    eman, f3 = wide_new("ca_eurostat_yth_demo_030.csv", {"sex": "T"})
    prop, f4 = wide_new("ca_eurostat_ilc_lvho02.csv", {"tenure": "OWN", "rskpovth": "TOTAL", "hhcomp": "TOTAL"})
    alq, _ = wide_new("ca_eurostat_ilc_lvho02.csv", {"tenure": "RENT_MKT", "rskpovth": "TOTAL", "hhcomp": "TOTAL"})
    crec, f5 = wide_new("ca_eurostat_demo_gind.csv", {"indic_de": "GROWRT"})
    mig, _ = wide_new("ca_eurostat_demo_gind.csv", {"indic_de": "CNMIGRATRT"})
    # (id, nombre, wide, unidad, tipo de variante, fecha del dato)
    IND = [
        ("hpi_real", "Precio de la vivienda real (HPI deflactado por IPCA, 2015=100)", hpi_real, "índice 2015=100", "cum", "2026-04"),
        ("alq_real", "Alquiler real (IPCA rúbrica CP041 deflactado, 2015=100)", renta_real, "índice 2015=100", "cum", "2025-12"),
        ("sobrecarga", "Sobrecarga de coste de vivienda (ilc_lvho07a)", sob, "% población", "dif", f1),
        ("hacinamiento", "Hacinamiento (ilc_lvho05a)", hac, "% población", "dif", f2),
        ("emancipacion", "Edad media de salida del hogar parental (yth_demo_030)", eman, "años", "dif", f3),
        ("propiedad", "Tenencia en propiedad (ilc_lvho02)", prop, "% población", "dif", f4),
        ("alquiler_mercado", "Alquiler a precio de mercado (ilc_lvho02)", alq, "% población", "dif", f4),
        ("permisos_1000", "Viviendas con permiso por 1.000 habitantes (sts_cobp_a / demo_pjan)", perm1000, "viv./1.000 hab.", "dif", "2026-04"),
        ("crec_pob", "Crecimiento de la población (demo_gind)", crec, "por 1.000 hab.", "dif", f5),
        ("migr_neta", "Migración neta con ajuste (demo_gind)", mig, "por 1.000 hab.", "dif", f5),
    ]
    filas = []
    ref_series = {}
    for id_, nom, w, un, tipo, fecha in IND:
        w = w[[c for c in UE27 if c in w.columns]]
        cnt = w.notna().sum(axis=1)
        ult = int(cnt[cnt >= 20][w["ES"].notna()].index.max())
        anyos_ult = [y for y in range(ult - 4, ult + 1) if cnt.get(y, 0) >= 20 and not np.isnan(w.loc[y, "ES"])]
        variantes = [("nivel", w, f"nivel {un}")]
        if id_ in ("hpi_real", "alq_real"):
            variantes = [("crecimiento", w / w.loc[2015] * 100 - 100, "% acumulado desde 2015")]
        elif id_ in ("sobrecarga", "hacinamiento", "emancipacion", "propiedad", "alquiler_mercado", "permisos_1000"):
            variantes.append(("cambio_desde_2015", w - w.loc[2015], f"cambio desde 2015 ({un})"))
        for var, ww, desc in variantes:
            ys = {}
            for y in anyos_ult + ([2015] if 2015 in ww.index else []):
                s = ww.loc[y].dropna()
                if "ES" not in s.index or len(s) < 20:
                    continue
                q1, med, q3 = s.quantile([0.25, 0.5, 0.75])
                pct = 100 * (s <= s["ES"]).mean()
                lado = "sobre" if s["ES"] > q3 else ("bajo" if s["ES"] < q1 else "dentro")
                ys[y] = (s["ES"], med, q1, q3, pct, lado, len(s))
            if ult not in ys:
                continue
            ult_lados = [ys[y][5] for y in anyos_ult if y in ys]
            sost5 = len(ult_lados) == 5 and len(set(ult_lados)) == 1 and ult_lados[0] != "dentro"
            sost3 = len(ult_lados) >= 3 and len(set(ult_lados[-3:])) == 1 and ult_lados[-1] != "dentro"
            for y, (v, med, q1, q3, pct, lado, n) in ys.items():
                if y != ult and not (y == 2015 and var == "nivel"):
                    continue
                filas.append({"id": id_, "indicador": nom, "variante": var, "descripcion": desc, "anio": y,
                              "es_ultimo": y == ult, "ES": round(v, 2), "mediana_UE27": round(med, 2),
                              "p25": round(q1, 2), "p75": round(q3, 2), "desv_vs_mediana": round(v - med, 2),
                              "percentil_ES": round(pct, 1), "n_paises": n, "posicion": lado,
                              "sostenido_5a": sost5 if y == ult else None, "sostenido_3a": sost3 if y == ult else None,
                              "fecha_dato": fecha})
                REG.log("C4_europa", f"{id_}|{var}|{y}", "posición ES en UE-27 (IQR)", y, y, n, np.nan, np.nan, np.nan,
                        notas=f"pct={pct:.1f}; {lado}")
            ref_series[(id_, var)] = ww
    t = pd.DataFrame(filas)
    t.to_csv(TAB / "europa_posicion_es.csv", index=False)

    # Contraste con fuentes nacionales (INE): ES de Eurostat frente a INE, misma muestra anual
    cont = []

    def comp(id_, nom, es_eu, nac, tol, unidad_tol, fecha):
        j = pd.concat([es_eu, nac], axis=1, keys=["eurostat", "ine"]).dropna()
        j = j.loc[j.index >= 2015]
        dif = (j.eurostat - j.ine).abs() if unidad_tol == "pp" else ((j.eurostat / j.ine - 1).abs() * 100)
        cont.append({"id": id_, "indicador": nom, "anios": f"{j.index.min()}-{j.index.max()}", "n": len(j),
                     "dif_max": round(dif.max(), 3), "tolerancia": tol, "unidad_tol": unidad_tol,
                     "dentro_tolerancia": bool(dif.max() <= tol), "candidata_C1_si_se_acepta_coherencia": bool(dif.max() <= tol),
                     "fecha_dato": fecha})

    ipv = pd.read_csv(RAW / "ine_ipv_25171.csv")
    ipv = ipv[ipv.nombre == "Nacional. General. Índice."].assign(y=lambda d: d.fecha.str[:4].astype(int))
    ipvq = ipv.groupby("y").valor.agg(["mean", "count"])
    ipva = ipvq[ipvq["count"] == 4]["mean"]
    comp("hpi_real", "HPI nominal Eurostat (ES) vs INE IPV general, 2015=100",
         hpi["ES"] / hpi.loc[2015, "ES"] * 100, ipva / ipva.loc[2015] * 100, 1.0, "%", "2025-10")
    ipc = pd.read_csv(RAW / "ine_ipc_alquiler.csv")
    ipc = ipc[ipc.serie == "IPC290887"].assign(y=lambda d: d.fecha.str[:4].astype(int))
    ipca = ipc.groupby("y").valor.agg(["mean", "count"])
    ipca = ipca[ipca["count"] == 12]["mean"]
    comp("alq_real", "IPCA alquiler Eurostat (ES) vs IPC alquiler INE, 2015=100",
         renta["ES"] / renta.loc[2015, "ES"] * 100, ipca / ipca.loc[2015] * 100, 2.0, "%", "2025-12")
    ecv = pd.read_csv(RAW / "v3" / "ine_ecv_tenencia_edad_v3.csv")
    ecv = ecv[ecv.serie.str.startswith("ecv_pct_hogares_tenencia|Propiedad|edad_persona_referencia=Total")
              & (ecv.territorio == "España")]
    ecv = ecv.assign(y=ecv.fecha.str[:4].astype(int)).groupby("y").valor.mean()
    comp("propiedad", "Propiedad Eurostat ilc_lvho02 (% población) vs INE ECV (% hogares)", prop["ES"], ecv, 3.0, "pp", "2025")
    ecp = pd.read_csv(RAW / "ine_ecp_nacional.csv")
    ecp = ecp[ecp.serie == "ECP320"].assign(y=lambda d: d.fecha.str[:4].astype(int))
    ecp = ecp.groupby("y").valor.last()
    comp("crec_pob", "Población 1 enero Eurostat demo_pjan (ES) vs INE ECP", pop["ES"], ecp, 0.5, "%", "2025")
    c = pd.DataFrame(cont)
    c.to_csv(TAB / "europa_contraste_nacional.csv", index=False)

    # Figura determinista: percentiles de España en el último año
    u = t[t.es_ultimo]
    fig, ax = plt.subplots(figsize=(9, 5))
    lab = (u.id + "|" + u.variante).tolist()
    ax.barh(lab, u.percentil_ES, color="#4477aa")
    ax.axvline(25, color="grey", ls=":")
    ax.axvline(75, color="grey", ls=":")
    ax.set_xlabel("Percentil de España en la UE-27 (último año; 25 y 75 = rango intercuartílico)")
    fig.tight_layout()
    fig.savefig(FIG / "europa_percentiles.png", dpi=110, metadata={"Software": None})
    plt.close(fig)

    # hechos
    # Capa conservadora: el dato de España en Eurostat procede del INE (no es independiente); la coincidencia
    # dentro de tolerancia hace al valor CANDIDATO a C1 (columna del contraste), pero la capa publicada es C4.
    capa_es = {r["id"]: "C4" for r in cont}
    for r in u.itertuples():
        base = capa_es.get(r.id, "C4")
        hecho(f"CA-EU-{r.id}-{r.variante}", f"{r.indicador} · {r.variante}: España", r.ES, r.descripcion,
              f"{r.anio}", "España; UE-27 (mediana %.2f, RIC %.2f-%.2f; %s %s)" % (r.mediana_UE27, r.p25, r.p75, r.posicion, "IQR"),
              "Eurostat" + (" + INE (contraste de coherencia)" if r.id in capa_es else ""), base, r.fecha_dato, r.p25, r.p75)
    return t, c


# ======================================================================= C1 · crédito a promotores
def ols_hac(y, x, maxlags=8):
    X = sm.add_constant(x)
    r = sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
    return r


def credito():
    b = pd.read_csv(V5 / "ca_bde_be0418_credito_actividad.csv")
    b["fecha"] = pd.to_datetime(b.fecha)
    w = b.pivot_table(index="fecha", columns="serie", values="valor") / 1e3  # millones de euros
    w = w.rename(columns={"D_MEE61000": "total_productivo", "D_MEE61010": "construccion",
                          "D_MEE61013": "inmobiliarias"})[["total_productivo", "construccion", "inmobiliarias"]]
    q = w[w.index.month.isin([3, 6, 9, 12])].copy()
    q.index = q.index.to_period("Q")
    q["constr_mas_inmob"] = q.construccion + q.inmobiliarias
    q = q.loc["2005Q1":"2025Q4"]
    q.round(0).to_csv(TAB / "credito_stock_trimestral_meur.csv")
    ini = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    m = ini[ini.serie == "viv_libres_iniciadas_mensual_nacional"].copy()
    m["p"] = pd.PeriodIndex(m.periodo, freq="M")
    iq = m.groupby(m.p.dt.asfreq("Q")).valor.agg(["sum", "count"])
    iq = iq[iq["count"] == 3]["sum"].loc["2008Q1":"2025Q4"]
    bls = pd.read_csv(V5 / "ca_ecb_bls_es.csv")
    be = bls[bls.KEY == "BLS.Q.ES.ALL.CP.E.Z.B3.ST.S.FNET"].copy()
    be.index = pd.PeriodIndex(be.TIME_PERIOD.str.replace("-", ""), freq="Q")
    be = be.OBS_VALUE.loc["2005Q1":"2025Q4"]
    d = pd.DataFrame({"inic": iq}).join(q).join(be.rename("bls_empresas_criterios"))
    dl = lambda s: np.log(s).diff(4)  # noqa: E731
    d["g_inic"] = dl(d.inic)
    for c in ("construccion", "inmobiliarias", "constr_mas_inmob", "total_productivo"):
        d["g_" + c] = dl(d[c])
    d = d.loc["2009Q1":]  # primera tasa interanual de iniciadas
    if SMOKE:
        d = d.iloc[:40]
    d.round(4).to_csv(TAB / "credito_iniciadas_trimestral.csv")
    regs = ["g_construccion", "g_inmobiliarias", "g_constr_mas_inmob", "bls_empresas_criterios"]
    res, pv = [], {}
    for x in regs:
        for k in range(0, 9):
            xx = d[x].shift(k)
            j = pd.concat([d.g_inic, xx], axis=1).dropna()
            r = ols_hac(j.iloc[:, 0], j.iloc[:, 1])
            rho = j.corr().iloc[0, 1]
            key = f"{x}|k={k}"
            pv[key] = float(r.pvalues.iloc[1])
            res.append({"regresor": x, "retardo_trim": k, "n": len(j), "beta": r.params.iloc[1], "rho": rho,
                        "p_hac": pv[key], "muestra": f"{j.index.min()}-{j.index.max()}"})
            REG.log("C1_credito", key, "g_inic ~ regresor(-k)", j.index.min(), j.index.max(), len(j), r.rsquared_adj,
                    r.aic, r.bic, coef_interes=float(r.params.iloc[1]), p_interes=pv[key],
                    notas="descriptivo, HAC(8); sin lectura causal")
    h = holm(pv)
    t = pd.DataFrame(res)
    t["p_holm"] = [h[f"{a}|k={k}"] for a, k in zip(t.regresor, t.retardo_trim)]
    t["rechaza_holm_5pc"] = t.p_holm < 0.05
    t.round(4).to_csv(TAB / "credito_iniciadas_retardos.csv", index=False)
    # Anual 2005-2025 (descriptivo)
    ia = ini[ini.serie == "viv_libres_iniciadas_anual_nacional"].assign(y=lambda x: x.periodo.astype(int)).set_index("y").valor
    qa = q[q.index.quarter == 4].copy()
    qa.index = qa.index.year
    an = pd.DataFrame({"iniciadas_libres": ia.loc[2005:2025]}).join(qa.round(0))
    an["ratio_stock_c_i_sobre_prod"] = (an.constr_mas_inmob / an.total_productivo).round(4)
    an.to_csv(TAB / "credito_iniciadas_anual.csv")
    # Fuera de muestra: ADL(1; credito retardo 4) frente a AR(4), bloques con embargo de 4 trimestres
    OOS = None
    jj = d[["g_inic", "g_constr_mas_inmob"]].dropna()
    e_ar, e_adl, idx = [], [], list(jj.index)
    T0 = 36
    for t_ in range(T0, len(jj)):
        tr = jj.iloc[: t_ - 4]  # embargo: se excluyen los 4 trimestres previos al objetivo
        yv = jj.g_inic
        Xa = pd.concat([yv.shift(l) for l in range(1, 5)], axis=1)
        Xb = pd.concat([Xa, jj.g_constr_mas_inmob.shift(4)], axis=1)
        def aj(X, tr=tr, yv=yv, t_=t_):
            Z = pd.concat([yv, X], axis=1).loc[tr.index].dropna()
            beta = np.linalg.lstsq(np.c_[np.ones(len(Z)), Z.iloc[:, 1:]], Z.iloc[:, 0], rcond=None)[0]
            xt = np.r_[1, X.iloc[t_].values]
            return float(xt @ beta)
        try:
            pa, pb = aj(Xa), aj(Xb)
        except Exception:  # noqa: BLE001
            continue
        e_ar.append(yv.iloc[t_] - pa)
        e_adl.append(yv.iloc[t_] - pb)
    if len(e_ar) > 12:
        e_ar, e_adl = np.array(e_ar), np.array(e_adl)
        dm = dm_test(e_adl, e_ar, h=1)
        OOS = {"modelo": "ADL(4)+crédito constr.+inmob. (retardo 4) frente a AR(4); 1 paso, ventana expansiva, embargo 4 trim.",
               "rmse": float(np.sqrt((e_adl ** 2).mean())), "rmse_ar4": float(np.sqrt((e_ar ** 2).mean())),
               "dm_vs_ar4": {"DM_HLN": dm["DM"], "p": dm["p"], "n": dm["n"]},
               "ecm_v1": "no aplicable: el ECM v1 modela el precio, no las iniciadas"}
        REG.log("C1_credito", "OOS_ADL_vs_AR4", "g_inic", idx[T0], idx[-1], dm["n"], np.nan, np.nan, np.nan,
                rmse_oos=OOS["rmse"], coef_interes=dm["DM"], p_interes=dm["p"], notas="DM-HLN; negativo = ADL mejor")
    # Figura
    fig, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    ax[0].plot(d.index.to_timestamp(), d.g_inic, label="iniciadas libres (var. interanual log)")
    ax[0].plot(d.index.to_timestamp(), d.g_constr_mas_inmob, label="saldo crédito constr.+inmob. (var. interanual log)")
    ax[0].legend(fontsize=8)
    ax[1].plot(d.index.to_timestamp(), d.bls_empresas_criterios, color="#aa3377")
    ax[1].set_ylabel("EPB España: criterios empresas\n(% neto endurecimiento)")
    fig.tight_layout()
    fig.savefig(FIG / "credito_iniciadas.png", dpi=110, metadata={"Software": None})
    plt.close(fig)
    # hechos
    pico = q.constr_mas_inmob.idxmax()
    hecho("CA-CR-saldo-pico", "Saldo de crédito a construcción + actividades inmobiliarias: máximo 2005-2025",
          q.constr_mas_inmob.max() / 1e3, "miles de millones de euros", str(pico), "España, entidades de crédito y EFC", "BdE be0418",
          "C4", str(b.fecha.max().date()))
    hecho("CA-CR-saldo-2025", "Saldo de crédito a construcción + actividades inmobiliarias",
          q.constr_mas_inmob.iloc[-1] / 1e3, "miles de millones de euros", str(q.index[-1]), "España", "BdE be0418", "C4",
          str(b.fecha.max().date()))
    hecho("CA-CR-saldo-caida", "Caída del saldo de crédito a constr.+inmob. desde su máximo hasta 2025Q4",
          100 * (q.constr_mas_inmob.iloc[-1] / q.constr_mas_inmob.max() - 1), "%", f"{pico}-{q.index[-1]}", "España", "BdE be0418",
          "C4", str(b.fecha.max().date()))
    return t, OOS, d


# ======================================================================= C3 · contado frente a hipoteca
REGISTRADORES_HIP = {2022: 463463, 2023: 383738, 2024: 435328, 2025: 498500}  # ERI Anuarios 2023-2025 (texto del cap. 17)


def contado():
    h = pd.read_csv(RAW / "ine_v2_hipotecas_prov.csv")
    h = h[(h.nivel == "nacional") & (h.medida == "hipotecas_viviendas_numero")].assign(y=lambda d: d.fecha.str[:4].astype(int))
    hy = h.groupby("y").valor.agg(["sum", "count"])
    hy = hy[hy["count"] == 12]["sum"]
    e = pd.read_csv(RAW / "ine_etdp_compraventas.csv")
    e = e[e.serie == "ETDP1826"].assign(y=lambda d: d.fecha.str[:4].astype(int))
    ey = e.groupby("y").valor.agg(["sum", "count"])
    ey = ey[ey["count"] == 12]["sum"]
    rg = pd.read_csv(RAW / "pdf" / "registradores_opendata_anual.csv")
    rg = rg[(rg.serie == "compraventas_viv_num") & (rg.territorio == "Espana")]
    rg = rg.set_index(rg.periodo.astype(int)).valor
    rh = pd.Series(REGISTRADORES_HIP)
    t = pd.DataFrame({"ine_hipotecas_viv": hy, "ine_compraventas_viv": ey, "reg_compraventas_viv": rg, "reg_hipotecas_viv": rh})
    t = t.loc[2007:2025].dropna(subset=["ine_hipotecas_viv", "ine_compraventas_viv"], how="any")
    t["ratio_ine"] = t.ine_hipotecas_viv / t.ine_compraventas_viv
    t["ratio_reg"] = t.reg_hipotecas_viv / t.reg_compraventas_viv
    t["dif_hip_ine_vs_reg_pct"] = (t.ine_hipotecas_viv / t.reg_hipotecas_viv - 1) * 100
    t["dif_ratio_pp"] = (t.ratio_ine - t.ratio_reg) * 100
    t.round(4).to_csv(TAB / "contado_ratio_hipotecas_compraventas.csv")
    com = t.dropna(subset=["ratio_reg"])
    tol_pp = 5.0
    ok = bool((com.dif_ratio_pp.abs() <= tol_pp).all())
    for y, r in com.iterrows():
        REG.log("C3_contado", f"triangulacion|{y}", "ratio hipotecas/compraventas INE vs Registradores", y, y, 1, np.nan, np.nan,
                np.nan, coef_interes=float(r.dif_ratio_pp), notas=f"tolerancia ±{tol_pp} pp")
    # Cota: contado >= 1 - phi * r, phi = fracción de hipotecas sobre vivienda destinadas a compraventa (supuesto)
    ult = int(t.index.max())
    r_ult = float(t.loc[ult, "ratio_ine"])
    g = pd.DataFrame({"phi": [0.6, 0.7, 0.8, 0.9, 1.0]})
    g["hipoteca_en_compras_pct"] = (g.phi * r_ult * 100).round(1)
    g["contado_pct"] = (100 - g.hipoteca_en_compras_pct).round(1)
    g["mayoria_contado"] = g.contado_pct > 50
    g["anio"] = ult
    g.to_csv(TAB / "contado_sensibilidad_phi.csv", index=False)
    for r in g.itertuples():
        REG.log("C3_contado", f"cota|phi={r.phi}", "contado = 1 - phi*ratio", ult, ult, 1, np.nan, np.nan, np.nan,
                coef_interes=float(r.contado_pct), notas="supuesto declarado sobre phi")
    phi_c = 0.5 / r_ult
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t.index, t.ratio_ine * 100, marker="o", label="INE: hipotecas / compraventas")
    ax.plot(t.index, t.ratio_reg * 100, marker="s", label="Registradores: hipotecas / compraventas")
    ax.axhline(50, color="grey", ls=":")
    ax.set_ylabel("% (hipotecas por 100 compraventas de vivienda)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "contado_ratio.png", dpi=110, metadata={"Software": None})
    plt.close(fig)
    f_ine = str(h.fecha.max())[:10]
    capa = "C4"  # INE (H, ETDP) y Registradores comparten origen registral: coherencia, no independencia
    hecho("CA-CT-ratio-ine", "Hipotecas sobre vivienda por 100 compraventas de vivienda (INE)", r_ult * 100,
          "hipotecas por 100 compraventas", str(ult), "España", "INE H (76317) y ETDP (6150)", "C4", f_ine,
          float(t.ratio_ine.min() * 100), float(t.ratio_ine.max() * 100))
    for y in com.index:
        hecho(f"CA-CT-ratio-triang-{y}", f"Hipotecas por 100 compraventas: INE {t.loc[y, 'ratio_ine']*100:.1f} frente a Registradores {t.loc[y, 'ratio_reg']*100:.1f}",
              t.loc[y, "ratio_ine"] * 100, "hipotecas por 100 compraventas", str(y), "España", "INE + Registradores (ERI Anuario)", capa,
              f"{y}-12-31", float(min(t.loc[y, "ratio_ine"], t.loc[y, "ratio_reg"]) * 100),
              float(max(t.loc[y, "ratio_ine"], t.loc[y, "ratio_reg"]) * 100))
    hecho("CA-CT-phi-critico", "Fracción de hipotecas dedicadas a compra por debajo de la cual el contado supera el 50 %",
          phi_c * 100, "% de las hipotecas", str(ult), "España; supuesto sobre phi", "INE", "C4", f_ine)
    hecho("CA-CT-contado-cota", "Cota inferior del contado si todas las hipotecas fueran de compra (phi = 1)",
          100 - r_ult * 100, "% de compraventas", str(ult), "España", "INE", "C4", f_ine)
    return t, g, ok, phi_c, r_ult, ult


# ======================================================================= salidas
def main():
    te, tc = europa()
    tcr, oos, d = credito()
    t3, g, ok, phi_c, r_ult, ult = contado()
    REG.flush()
    u = te[te.es_ultimo]
    fuera = u[(u.posicion != "dentro") & (u.sostenido_5a == True)]  # noqa: E712
    fuera3 = u[(u.posicion != "dentro") & (u.sostenido_3a == True)]  # noqa: E712
    sig = tcr[tcr.rechaza_holm_5pc]
    rr = {
        "rama": "CA",
        "pregunta": "(C4) ¿Qué es específico de España frente a la UE-27? (C1) ¿El crédito a promotores se asocia a las iniciadas? (C3) ¿Se compra al contado o con hipoteca?",
        "capa": "C4 (Europa; el valor de España es C1 donde coincide con el INE) · C4 (crédito, descriptivo) · C4 (contado: cota con supuesto)",
        "datos": "Eurostat (prc_hpi_a, prc_hicp_aind, ilc_lvho07a, ilc_lvho05a, yth_demo_030, ilc_lvho02, sts_cobp_a, demo_pjan, demo_gind); BdE be0418; BCE BLS (EPB) España; MIVAU iniciadas; INE H 76317, ETDP 6150; Registradores ERI",
        "N": {"europa_indicadores": int(te.id.nunique()), "credito_trimestres": int(len(d)), "contado_anios": int(len(t3))},
        "metodo": "Posición en la UE-27 (percentil, desviación frente a la mediana, rango intercuartílico); regresiones descriptivas con HAC(8) y Holm sobre 36 pruebas; razón hipotecas/compraventas con cota 1-phi*razón",
        "estimacion": {"fuera_IQR_sostenido_5a": fuera[["id", "variante", "posicion", "percentil_ES"]].to_dict("records"),
                       "fuera_IQR_sostenido_3a": fuera3[["id", "variante", "posicion", "percentil_ES"]].to_dict("records"),
                       "credito_retardos_significativos_holm": sig[["regresor", "retardo_trim", "rho", "p_holm"]].round(4).to_dict("records"),
                       "contado": {"anio": ult, "hipotecas_por_100_compraventas_INE": round(r_ult * 100, 1),
                                   "phi_critico_pct": round(phi_c * 100, 1)}},
        "ic95": None,
        "p_ajustado": {"metodo": "Holm", "n_pruebas": int(len(tcr)), "min": float(tcr.p_holm.min())},
        "nivel_evidencia": "EXPLORATORIO (C4) en los tres ángulos; sin lenguaje causal",
        "diagnosticos": {"triangulacion_contado_ok": ok, "contraste_nacional": tc[["id", "dif_max", "tolerancia", "dentro_tolerancia"]].to_dict("records"),
                         "solapamiento_regresiones": "variaciones interanuales solapadas; p con HAC(8)"},
        "fuera_muestra": {"modelo": oos["modelo"] if oos else None, "rmse": oos["rmse"] if oos else None,
                          "dm_vs_ar4": oos["dm_vs_ar4"] if oos else None},
        "notas": "Notariado: sin datos accesibles (CIEN sin compraventas; portal con cuenta). Registradores: solo 2022-2025 (texto de los ERI Anuarios). "
                 "El saldo por actividad no es nuevas operaciones; las nuevas operaciones por finalidad no están en el Boletín. "
                 "ECM v1 no aplicable al crédito/iniciadas. Eurostat toma los datos de ES del INE: el contraste con el INE es de coherencia, no de independencia.",
    }
    (OUT / "resultado.json").write_text(json.dumps(rr, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1), encoding="utf-8")

    def v(i, var, col="ES"):
        r = u[(u.id == i) & (u.variante == var)].iloc[0]
        return r
    hp, al, so = v("hpi_real", "crecimiento"), v("alq_real", "crecimiento"), v("sobrecarga", "nivel")
    em, ps = v("emancipacion", "nivel"), v("permisos_1000", "nivel")
    an = pd.read_csv(TAB / "credito_iniciadas_anual.csv", index_col=0)
    pk = an.constr_mas_inmob
    g_ = g.set_index("phi")
    fichas = [
        {"id": "CA-V1", "tema": "Comparación europea",
         "enunciado": "La vivienda en España es más cara que en Europa.", "capa": "C4",
         "magnitud": (f"Crecimiento (real, 2015-{hp.anio}): precio {hp.ES:+.1f} % en España frente a una mediana UE-27 de {hp.mediana_UE27:+.1f} % "
                      f"(percentil {hp.percentil_ES:.0f}, {hp.posicion} del rango intercuartílico {hp.p25:.1f} a {hp.p75:.1f}); alquiler real {al.ES:+.1f} % frente a {al.mediana_UE27:+.1f} % "
                      f"(percentil {al.percentil_ES:.0f}, {al.posicion}). Nivel: Eurostat no publica un precio por m² comparable; "
                      f"como aproximación, la sobrecarga de coste de vivienda es {so.ES:.1f} % de la población ({so.anio}) frente a una mediana de {so.mediana_UE27:.1f} % (percentil {so.percentil_ES:.0f}, {so.posicion}). "
                      f"Sostenidamente fuera del rango (5 años): {', '.join(fuera.id + '|' + fuera.variante) or 'ninguno'}; (3 años): {', '.join(fuera3.id + '|' + fuera3.variante) or 'ninguno'}."),
         "intervalo": f"percentil de España en el precio real: {hp.percentil_ES:.0f}; en la sobrecarga: {so.percentil_ES:.0f}",
         "cota": "—", "literatura": "—",
         "veredicto": "ANALIZADA, NO CONCLUYENTE",
         "regla": "Variante de nivel: no contrastable con un precio comparable (el HPI es un índice, no un nivel); las aproximaciones de asequibilidad no sitúan a España fuera del rango intercuartílico. "
                  "Variante de crecimiento: el precio real acumulado desde 2015 queda dentro del rango; el alquiler real queda por debajo de la mediana. Capa C4: el dato del resto de países es de fuente única (Eurostat) y el de España procede del INE.",
         "limites": "Comparación entre índices con base 2015; deflactor IPCA general; Eurostat toma los datos de España del INE (coherencia, no independencia). Países sin dato en el año omitidos.",
         "evidencia": ["output/v5/CA/tablas/europa_posicion_es.csv", "output/v5/CA/tablas/europa_contraste_nacional.csv"]},
        {"id": "CA-V2", "tema": "Crédito a promotores",
         "enunciado": "La falta de crédito a promotores frena la oferta de vivienda.", "capa": "C4",
         "magnitud": (f"El saldo de crédito a construcción y actividades inmobiliarias pasó de {pk.max()/1e3:.0f} mil millones de euros (máximo, {int(pk.idxmax())}) a {pk.iloc[-1]/1e3:.0f} en 2025. "
                      f"De 36 pruebas (retardos de 0 a 8 trimestres, 4 regresores) con Holm, {len(sig)} resulta distinta de cero: "
                      f"{', '.join(sig.regresor + ' retardo ' + sig.retardo_trim.astype(str) + ' (rho ' + sig.rho.round(2).astype(str) + ')') or 'ninguna'}; el signo es negativo (asociación descriptiva únicamente). "
                      f"Fuera de muestra, el modelo con crédito {'no mejora' if oos and oos['dm_vs_ar4']['p'] > 0.05 else 'mejora'} a AR(4) (DM-HLN p = {oos['dm_vs_ar4']['p']:.2f})."),
         "intervalo": "—", "cota": "—", "literatura": "—",
         "veredicto": "ANALIZADA, NO CONCLUYENTE",
         "regla": "Relación descriptiva entre variaciones interanuales, sin interpretación de efecto. El saldo no es nuevas operaciones (no disponibles por finalidad en el Boletín).",
         "limites": "Variaciones interanuales solapadas (HAC 8); iniciadas libres, no protegidas; la EPB de España trae criterios de empresas desde 2003 y de vivienda desde 2022.",
         "evidencia": ["output/v5/CA/tablas/credito_iniciadas_retardos.csv", "output/v5/CA/tablas/credito_iniciadas_anual.csv"]},
        {"id": "CA-V3", "tema": "Forma de pago",
         "enunciado": "La mayoría compra al contado.", "capa": "C4",
         "magnitud": (f"En {ult}, el INE registra {r_ult*100:.1f} hipotecas sobre vivienda por cada 100 compraventas de vivienda; Registradores da {t3.loc[ult, 'ratio_reg']*100:.1f} "
                      f"(diferencia máxima {t3.dif_ratio_pp.abs().max():.1f} pp en 2022-2025). Si todas las hipotecas financiaran compras, el contado sería al menos el {100 - r_ult*100:.0f} %; "
                      f"la mayoría al contado exige que menos del {phi_c*100:.0f} % de las hipotecas sobre vivienda financie una compra, fracción no observada."),
         "intervalo": f"contado {g_.loc[1.0, 'contado_pct']:.0f} % (phi = 1) a {g_.loc[0.6, 'contado_pct']:.0f} % (phi = 0,6)",
         "cota": "C2-like: contado = 100 - phi x razón; supuesto sobre phi declarado, no estimado",
         "literatura": "—", "veredicto": "ANALIZADA, NO CONCLUYENTE",
         "regla": "La razón hipotecas/compraventas es un hecho coherente en dos fuentes (ambas de origen registral); el porcentaje al contado depende de qué parte de las hipotecas no es de compra. "
                  "La demanda inversora no equivale al contado: un inversor puede financiarse con hipoteca y un comprador residente puede pagar al contado.",
         "limites": "Notariado (porcentaje de compras financiadas) sin dato accesible; Registradores solo 2022-2025 (texto de los Anuarios ERI). No distingue comprador residente de inversor.",
         "evidencia": ["output/v5/CA/tablas/contado_ratio_hipotecas_compraventas.csv", "output/v5/CA/tablas/contado_sensibilidad_phi.csv"]},
    ]
    (OUT / "fichas_verificador.json").write_text(json.dumps(fichas, ensure_ascii=False, indent=1), encoding="utf-8")
    print("OK", len(HECHOS), "hechos")
    print(te[te.es_ultimo][["id", "variante", "anio", "ES", "mediana_UE27", "p25", "p75", "percentil_ES", "posicion", "sostenido_5a", "sostenido_3a"]].to_string())
    print(tc.to_string())
    print(sig.to_string())
    print(t3.round(3).tail(6).to_string())
    print(g.to_string())
    print(oos)


if __name__ == "__main__":
    main()
