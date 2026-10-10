"""P-B (capa C2): cotas de identificación parcial (estilo Manski) para turísticos, inmigración, grandes tenedores y tipos.

Especificación fijada: docs/v3/especificacion_PA_PB.md (sección P-B). Determinista, sin red, SEED=20261010.
Sin contrastes de hipótesis: no hay p-valores, por lo que no se aplica Holm/BH (se dice en resultado.json).
Todas las cifras son cotas bajo supuestos explícitos; la única fórmula de atribución admitida es
«como máximo X puede atribuirse a Y bajo el supuesto Z».

Uso:
    python3 src/v3/pb_run.py                 # run completo -> output/v3/PB/
    python3 src/v3/pb_run.py --smoke 46      # smoke test con una provincia -> carpeta temporal
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v3"))

import holdout  # noqa: E402
from econ_utils import Registry  # noqa: E402
from ingesta_grandes_tenedores import main as ingesta_gt  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
RAW3 = RAW / "v3"

# ---------------------------------------------------------------- supuestos (todos explícitos)
# |ε_d|: elasticidad-precio de la demanda (valor absoluto). Lagunas de lit. v3 parte B: no hay estimación
# verificada para España. Valores IMPLÍCITOS (no estimados como tal) de dos referencias:
#   mínimo 0,33 = 17 % de flujo -> +52 % de precio (González y Ortega 2013): 1/ε = 52/17 ≈ 3,06;
#   central 1,0 = 1 % de población -> ≈ +1 % de alquiler (Saiz 2007).
EPS_MIN, EPS_CENTRAL = 0.33, 1.0
EPS_GRID = [0.25, 0.33, 0.5, 0.75, 1.0, 1.5, 2.0]
M2_TIPO = 80.0                      # m2 de la vivienda tipo (misma convención que A4)
UMBRAL_DVUT = 0.001                 # 0,1 puntos de ΔVUT/stock de alquiler
UMBRALES = [0.001, 0.005, 0.01, 0.02]
TAM_EXT = {"min": 2.0, "max": 3.0}  # personas por hogar extranjero (rango); central = media nacional
BAJAS = [0.0, 0.001, 0.002]
DEP, GAN, IBI = [1.0, 2.0, 3.0], [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0], [0.5, 0.75, 1.0]
UC_SUELO = 1.0                      # uc (en %) mínimo para que 1/uc esté definido y acotado
CIUDADES = {"28079": "Madrid", "08019": "Barcelona", "46250": "València", "41091": "Sevilla",
            "50297": "Zaragoza", "29067": "Málaga"}
PERIODOS_B2 = [(2002, 2007), (2008, 2013), (2009, 2014), (2014, 2019), (2020, 2025), (2021, 2025), (2014, 2025)]


class Ctx:
    def __init__(self, out: Path, smoke: str | None):
        self.out, self.tab, self.fig = out, out / "tablas", out / "figuras"
        for d in (self.tab, self.fig):
            d.mkdir(parents=True, exist_ok=True)
        self.smoke = smoke
        self.reg = Registry(out / "registro.csv")
        self.cotas: list[dict] = []
        self.notas: list[str] = []

    def csv(self, df: pd.DataFrame, nombre: str):
        df.to_csv(self.tab / nombre, index=False, float_format="%.6g")

    def log(self, modelo_id, formula, ini, fin, n, valor, notas=""):
        self.reg.log("PB", modelo_id, formula, ini, fin, int(n), np.nan, np.nan, np.nan, coef_interes=valor, notas=notas)

    def cota(self, id, factor, ambito, periodo, valor, unidad, supuesto, no_explica, smin, smax, limites, frase_obj=""):
        f = lambda v: None if v is None or (isinstance(v, float) and not np.isfinite(v)) else round(float(v), 4)  # noqa: E731
        self.cotas.append({
            "id": id, "factor": factor, "ambito": ambito, "periodo": periodo, "cota_superior": f(valor), "unidad": unidad,
            "supuesto_extremo": supuesto, "no_explica": f(no_explica), "sensibilidad_min": f(smin), "sensibilidad_max": f(smax),
            "capa": "C2", "limites": limites,
            "frase": f"como máximo {f(valor)} {unidad} puede atribuirse a {frase_obj or factor} bajo el supuesto {supuesto}"})


# ---------------------------------------------------------------- datos
def cargar():
    d = {n: holdout.load_full(n, "PB") for n in ["panel_prov_a", "panel_muni_a", "nacional_q_v2", "panel_prov_q"]}
    d["pp"], d["pm"], d["nat"] = d["panel_prov_a"], d["panel_muni_a"], d["nacional_q_v2"].set_index("trimestre")
    d["pp"]["cod_prov"] = d["pp"]["cod_prov"].astype(str).str.zfill(2)
    d["pm"]["cod_muni"] = d["pm"]["cod_muni"].astype(int).astype(str).str.zfill(5)
    d["pm"]["cod_prov"] = d["pm"]["cod_prov"].astype(int).astype(str).str.zfill(2)
    return d


def censo_secciones() -> pd.DataFrame:
    s = pd.read_csv(RAW3 / "ine_v3_censo2021_seccion_indicadores.csv.gz", dtype={"codigo": str},
                    usecols=["serie", "valor", "codigo"])
    s = s[s.serie.isin(["t18_1", "t19_1", "t20_2", "t21_1", "t1_1", "t5_1", "t6_1"])]
    w = s.pivot_table(index="codigo", columns="serie", values="valor", aggfunc="first")
    w = w.rename(columns={"t18_1": "viv_total", "t19_1": "viv_prin", "t20_2": "viv_alquiler", "t21_1": "hogares",
                          "t1_1": "personas", "t5_1": "pct_extranj", "t6_1": "pct_nacidos_ext"}).reset_index()
    w["muni"], w["prov"] = w.codigo.str[:5], w.codigo.str[:2]
    return w


def vut_nacional() -> pd.Series:
    v = pd.read_csv(RAW / "ine_v2_vut.csv", dtype=str, usecols=["periodo", "valor", "nivel", "medida"])
    v = v[(v.nivel == "nacional") & (v.medida == "viviendas_turisticas")]
    return v.set_index("periodo").valor.astype(float)


def oleada_a_q(p: str) -> str:
    y, m = p.split("M")
    return f"{y}Q{(int(m) - 1) // 3 + 1}"


def lnr(a, b):
    return float(np.log(b / a))


# ---------------------------------------------------------------- B1
def b1(c: Ctx, d: dict, cen: pd.DataFrame):
    nat, pp, pm = d["nat"], d["pp"], d["pm"]
    prov_f = c.smoke
    vn = vut_nacional()
    stock_cen = cen.viv_alquiler.sum()
    parque_cen = cen.viv_total.sum()
    # fuente alternativa de stock de alquiler: ECV 2021 (alquiler de mercado 15,2 % + inferior a mercado 2,8 %) x hogares ECP 2021Q4
    ecv = pd.read_csv(RAW3 / "ine_ecv_tenencia_edad_v3.csv", usecols=["periodo", "serie", "valor"])
    ecv = ecv[ecv.serie.str.endswith("edad_persona_referencia=Total|sexo=Ambos sexos")]
    cuota = {k: float(ecv[(ecv.periodo == 2021) & ecv.serie.str.contains(k, regex=False)].valor.iloc[0])
             for k in ["Alquiler a precio de mercado", "Alquiler inferior al precio de mercado"]}
    stock_ecv = sum(cuota.values()) / 100 * nat.loc["2021Q4", "hogares_ecp"]
    stocks = {"censo2021": stock_cen, "ECV2021xECP": stock_ecv}
    # nivel de alquiler SERPAVI 2020 ponderado por contratos (EUR/mes, 80 m2)
    m20 = pm[(pm.anio == 2020) & pm.serpavi_mediana_vc.notna() & (pm.serpavi_n_vc > 0)]
    renta_m2_nac = float(np.average(m20.serpavi_mediana_vc, weights=m20.serpavi_n_vc))
    renta_eur = renta_m2_nac * M2_TIPO

    # ---- nacional (total JAXI) por periodos
    per = [("2020M08", "2024M08"), ("2021M08", "2024M08"), ("2020M08", "2026M05"), ("2024M08", "2026M05")]
    filas = []
    for a, b in per:
        qa, qb = oleada_a_q(a), oleada_a_q(b)
        dv = vn[b] - vn[a]
        dlr = lnr(nat.loc[qa, "ipc_alquiler"], nat.loc[qb, "ipc_alquiler"])
        for (sk, sv), e in product(stocks.items(), EPS_GRID):
            q = dv / sv
            filas.append(dict(periodo=f"{a}-{b}", stock=sk, stock_alquiler=sv, eps=e, dVUT=dv, VUT_ini=vn[a], VUT_fin=vn[b],
                              peso_parque_pct=100 * vn[b] / parque_cen, peso_alquiler_pct=100 * vn[b] / sv,
                              cota_cantidad_pct=100 * q, cota_precio_pct=100 * q / e, dlnR_obs_pct=100 * dlr,
                              no_explica_agregado_pct=100 * max(0.0, 1 - max(q / e, 0) / dlr) if dlr > 0 else np.nan,
                              cota_eur_mes=q / e * renta_eur))
    t = pd.DataFrame(filas)
    c.csv(t, "b1_nacional_sensibilidad.csv")
    for r in t[(t.stock == "censo2021") & t.eps.isin([EPS_MIN])].itertuples():
        c.log(f"B1-nac-{r.periodo}", "dlnR_max=(dVUT/stock)/eps; stock=censo2021; eps=0.33", r.periodo[:7], r.periodo[8:], 1, r.cota_precio_pct,
              "cota nacional JAXI")

    # ---- municipal: peso y "lo que no puede explicar"
    cm = cen.groupby("muni")[["viv_total", "viv_alquiler", "hogares"]].sum().reset_index()
    pmw = pm[pm.anio.isin([2020, 2024])].pivot_table(index=["cod_muni", "cod_prov"], columns="anio",
                                                     values=["vut_viviendas", "serpavi_mediana_vc", "serpavi_n_vc", "uu_residenciales"]).reset_index()
    pmw.columns = ["_".join(str(x) for x in col if x != "").strip("_") for col in pmw.columns]
    pmw = pmw.rename(columns={"cod_muni": "muni", "cod_prov": "prov"}).merge(cm, on="muni", how="left")
    if prov_f:
        pmw = pmw[pmw.prov == prov_f]
    pmw["dVUT"] = pmw.vut_viviendas_2024 - pmw.vut_viviendas_2020
    pmw["q_alq"] = pmw.dVUT / pmw.viv_alquiler.replace(0, np.nan)
    pmw["peso_parque_pct"] = 100 * pmw.vut_viviendas_2024 / pmw.viv_total
    pmw["peso_alquiler_pct"] = 100 * pmw.vut_viviendas_2024 / pmw.viv_alquiler.replace(0, np.nan)
    pmw["dlnR"] = np.log(pmw.serpavi_mediana_vc_2024 / pmw.serpavi_mediana_vc_2020)
    c.csv(pmw[["muni", "prov", "vut_viviendas_2020", "vut_viviendas_2024", "viv_total", "viv_alquiler", "dVUT", "q_alq",
               "peso_parque_pct", "peso_alquiler_pct", "dlnR"]], "b1_municipio.csv")
    ok = pmw.dropna(subset=["q_alq", "dlnR", "viv_alquiler"])
    ok = ok[ok.viv_alquiler > 0]
    cob = ok.viv_alquiler.sum() / cm.viv_alquiler.sum() if not prov_f else np.nan
    nx = []
    for u in UMBRALES:
        sel = ok.q_alq < u
        contrib = ok.viv_alquiler * ok.dlnR
        tot, parte = contrib.sum(), contrib[sel].sum()
        # radio provincial: el municipio cuenta como "sin turísticos" solo si su provincia entera tampoco los tiene
        pr = ok.groupby("prov").apply(lambda g: g.dVUT.sum() / g.viv_alquiler.sum(), include_groups=False)
        sel_p = ok.prov.map(pr) < u
        nx.append(dict(umbral_pp=100 * u, n_muni=int(sel.sum()), n_total=len(ok), stock_en_set_pct=100 * ok.viv_alquiler[sel].sum() / ok.viv_alquiler.sum(),
                       no_explica_muni_pct=100 * parte / tot, n_prov_set=int((pr < u).sum()),
                       no_explica_radio_prov_pct=100 * contrib[sel_p].sum() / tot, dlnR_medio_pond_pct=100 * tot / ok.viv_alquiler.sum(),
                       cobertura_stock_alquiler_pct=100 * cob if np.isfinite(cob) else np.nan))
    nx = pd.DataFrame(nx)
    c.csv(nx, "b1_no_explica_municipal.csv")
    ne_muni = float(nx.loc[nx.umbral_pp == 0.1, "no_explica_muni_pct"].iloc[0])
    ne_prov = float(nx.loc[nx.umbral_pp == 0.1, "no_explica_radio_prov_pct"].iloc[0])
    for r in nx.itertuples():
        c.log(f"B1-noexplica-umbral{r.umbral_pp}", "sum_i w_i dlnR_i [dVUT_i/stock_i<umbral] / sum_i w_i dlnR_i", 2020, 2024, r.n_total, r.no_explica_muni_pct,
              f"radio provincial {r.no_explica_radio_prov_pct:.1f}")

    # ---- nacional: cotas
    main = t[(t.periodo == "2020M08-2024M08")]
    qmain = main[(main.stock == "censo2021") & (main.eps == EPS_MIN)].iloc[0]
    qc = main[(main.stock == "censo2021") & (main.eps == EPS_CENTRAL)].iloc[0]
    lim = ("JAXI total (VUT = oferta turística registrada, estadística experimental del INE); stock de alquiler = Censo 2021 constante; "
           "sustitución 1:1 y traspaso completo a la demanda de alquiler; |ε_d| implícito de la literatura (laguna: sin estimación verificada); "
           "base 2020M08 próxima al mínimo de la pandemia; alquiler IPC nacional (no mide el stock). Sin efectos de desbordamiento fuera del ámbito.")
    ps = f"{qmain.periodo}"
    c.cota("B1-nac-cantidad", "turisticos", "nacional", ps, qmain.cota_cantidad_pct, "% del stock de alquiler (desplazamiento máx. de oferta)",
           "sustitución 1:1 de toda vivienda turística nueva por una vivienda de alquiler menos", ne_muni,
           main.cota_cantidad_pct.min(), main.cota_cantidad_pct.max(), lim, "las viviendas turísticas nuevas")
    c.cota("B1-nac-cantidad-viviendas", "turisticos", "nacional", ps, qmain.dVUT, "viviendas", "sustitución 1:1", ne_muni,
           qmain.dVUT, qmain.dVUT, lim, "las viviendas turísticas nuevas")
    c.cota("B1-nac-precio-eps_min", "turisticos", "nacional", ps, qmain.cota_precio_pct, "% de alquiler (Δ ln)",
           f"sustitución 1:1 y |ε_d|={EPS_MIN} (valor bajo del rango; sin respuesta de la oferta)", ne_muni,
           main.cota_precio_pct.min(), main.cota_precio_pct.max(), lim, "el aumento de viviendas turísticas")
    c.cota("B1-nac-precio-central", "turisticos", "nacional", ps, qc.cota_precio_pct, "% de alquiler (Δ ln)",
           f"sustitución 1:1 y |ε_d|={EPS_CENTRAL} (central)", ne_muni, main[main.eps >= EPS_CENTRAL].cota_precio_pct.min(),
           main[main.eps >= EPS_CENTRAL].cota_precio_pct.max(), lim, "el aumento de viviendas turísticas")
    c.cota("B1-nac-precio-eps_min-eur", "turisticos", "nacional", ps, qmain.cota_eur_mes, "€/mes (alquiler tipo de 80 m2)",
           f"sustitución 1:1 y |ε_d|={EPS_MIN}", ne_muni, main.cota_eur_mes.min(), main.cota_eur_mes.max(), lim, "el aumento de viviendas turísticas")
    for r in t[(t.stock == "censo2021") & (t.eps == EPS_MIN) & (t.periodo != ps)].itertuples():
        c.cota(f"B1-nac-precio-eps_min-{r.periodo}", "turisticos", "nacional", r.periodo, r.cota_precio_pct, "% de alquiler (Δ ln)",
               f"sustitución 1:1 y |ε_d|={EPS_MIN}" + (" (ΔVUT negativo: liberación de oferta; la cota superior es ≤ 0)" if r.dVUT < 0 else ""),
               ne_muni, None, None, lim, "el aumento de viviendas turísticas")

    # ---- provincial
    cp = cen.groupby("prov")[["viv_total", "viv_alquiler"]].sum().reset_index().rename(columns={"prov": "cod_prov"})
    w = pp[pp.anio.isin([2020, 2024])].pivot_table(index="cod_prov", columns="anio", values=["vut_viviendas", "ipc_alquiler"]).reset_index()
    w.columns = ["_".join(str(x) for x in col if x != "").strip("_") for col in w.columns]
    w = w.merge(cp, on="cod_prov", how="left").merge(pp[["cod_prov", "provincia"]].drop_duplicates(), on="cod_prov")
    if prov_f:
        w = w[w.cod_prov == prov_f]
    w["dVUT"] = w.vut_viviendas_2024 - w.vut_viviendas_2020
    w["q"] = w.dVUT / w.viv_alquiler
    w["dlnR_obs_pct"] = 100 * np.log(w.ipc_alquiler_2024 / w.ipc_alquiler_2020)
    w["peso_parque_pct"], w["peso_alquiler_pct"] = 100 * w.vut_viviendas_2024 / w.viv_total, 100 * w.vut_viviendas_2024 / w.viv_alquiler
    w["cota_cantidad_pct"] = 100 * w.q
    w["cota_precio_epsmin_pct"], w["cota_precio_central_pct"] = 100 * w.q / EPS_MIN, 100 * w.q / EPS_CENTRAL
    w["no_explica_agregado_pct"] = np.where(w.dlnR_obs_pct > 0, 100 * np.clip(1 - np.maximum(w.cota_precio_epsmin_pct, 0) / w.dlnR_obs_pct, 0, 1), np.nan)
    c.csv(w, "b1_provincia.csv")
    # no explica con IPC provincial (nivel provincia): peso por stock de alquiler
    wp = w.dropna(subset=["dlnR_obs_pct", "q"])
    pn = []
    for u in UMBRALES:
        sel = wp.q < u
        contrib = wp.viv_alquiler * wp.dlnR_obs_pct
        pn.append(dict(umbral_pp=100 * u, n_prov=int(sel.sum()), n_total=len(wp),
                       no_explica_prov_pct=100 * contrib[sel].sum() / contrib.sum() if contrib.sum() else np.nan))
    c.csv(pd.DataFrame(pn), "b1_no_explica_provincial.csv")
    for r in w.itertuples():
        c.log(f"B1-prov-{r.cod_prov}", "dlnR_max=(dVUT/stock)/eps; eps=0.33", 2020, 2024, 1, r.cota_precio_epsmin_pct, r.provincia)
        c.cota(f"B1-prov-{r.cod_prov}-precio-eps_min", "turisticos", f"provincia {r.provincia}", "2020-2024", r.cota_precio_epsmin_pct,
               "% de alquiler (Δ ln)", f"sustitución 1:1 y |ε_d|={EPS_MIN} dentro de la provincia", r.no_explica_agregado_pct,
               100 * r.q / max(EPS_GRID), 100 * r.q / min(EPS_GRID),
               "Alquiler = IPC de alquiler provincial (anual); stock = Censo 2021; VUT = panel provincial (oleada de agosto). " + lim.split(";")[3])

    # ---- ciudades (municipio) y València por sección
    ciu = pmw[pmw.muni.isin(CIUDADES)].copy()
    if len(ciu):
        ciu["ciudad"] = ciu.muni.map(CIUDADES)
        ciu["renta_eur_mes_2020"] = ciu.serpavi_mediana_vc_2020 * M2_TIPO
        ciu["cota_cantidad_pct"] = 100 * ciu.q_alq
        ciu["cota_precio_epsmin_pct"], ciu["cota_precio_central_pct"] = 100 * ciu.q_alq / EPS_MIN, 100 * ciu.q_alq / EPS_CENTRAL
        ciu["cota_eur_mes_epsmin"] = ciu.q_alq / EPS_MIN * ciu.renta_eur_mes_2020
        ciu["dlnR_obs_pct"] = 100 * ciu.dlnR
        ciu["no_explica_agregado_pct"] = np.where(ciu.dlnR > 0, 100 * np.clip(1 - np.maximum(ciu.cota_precio_epsmin_pct, 0) / ciu.dlnR_obs_pct, 0, 1), np.nan)
        c.csv(ciu.drop(columns=[x for x in ciu.columns if x.startswith("uu_") or x.startswith("hogares")]), "b1_ciudades.csv")
        for r in ciu.itertuples():
            c.log(f"B1-ciudad-{r.muni}", "dlnR_max=(dVUT/stock)/eps; eps=0.33", 2020, 2024, 1, r.cota_precio_epsmin_pct, r.ciudad)
            c.cota(f"B1-ciudad-{r.muni}-cantidad", "turisticos", f"ciudad {r.ciudad}", "2020-2024", r.cota_cantidad_pct,
                   "% del stock de alquiler", "sustitución 1:1", r.no_explica_agregado_pct, 100 * r.q_alq, 100 * r.q_alq,
                   "SERPAVI = stock de contratos declarados (amortigua cambios); ΔVUT negativo implica cota ≤ 0 (la oferta turística bajó).", "las viviendas turísticas nuevas")
            c.cota(f"B1-ciudad-{r.muni}-precio-eps_min", "turisticos", f"ciudad {r.ciudad}", "2020-2024", r.cota_precio_epsmin_pct,
                   "% de alquiler (Δ ln)", f"sustitución 1:1 y |ε_d|={EPS_MIN}", r.no_explica_agregado_pct,
                   100 * r.q_alq / max(EPS_GRID), 100 * r.q_alq / min(EPS_GRID),
                   "SERPAVI = stock de contratos declarados (amortigua cambios); ΔVUT negativo implica cota ≤ 0.", "el aumento de viviendas turísticas")
            c.cota(f"B1-ciudad-{r.muni}-precio-eur", "turisticos", f"ciudad {r.ciudad}", "2020-2024", r.cota_eur_mes_epsmin,
                   "€/mes (alquiler tipo de 80 m2)", f"sustitución 1:1 y |ε_d|={EPS_MIN}", r.no_explica_agregado_pct, None, None,
                   "Renta SERPAVI 2020 x 80 m2 (supuesto de vivienda tipo).", "el aumento de viviendas turísticas")
    # secciones de las ciudades: 2021M08 -> 2024M08
    sec = b1_secciones(c, cen)
    return dict(ne_muni=ne_muni, ne_prov=ne_prov, nac=t, qmain=qmain, cob=cob, sec=sec, renta_eur=renta_eur)


def b1_secciones(c: Ctx, cen: pd.DataFrame):
    pref = tuple(CIUDADES)
    z = pd.read_csv(RAW3 / "ine_v3_vut_seccion.csv.gz", dtype=str, usecols=["periodo", "valor", "nivel", "codigo", "medida"])
    z = z[(z.nivel == "seccion") & (z.medida == "vivienda_turistica") & z.codigo.str.startswith(pref) & z.periodo.isin(["2021M08", "2024M08"])]
    z["valor"] = z.valor.astype(float)
    zv = z.pivot_table(index="codigo", columns="periodo", values="valor").reset_index().rename(columns={"2021M08": "vut_2021M08", "2024M08": "vut_2024M08"})
    rows = []
    for ch in pd.read_csv(RAW3 / "serpavi_secciones_nacional_v3.csv.gz", dtype=str, usecols=["periodo", "serie", "valor", "codigo"], chunksize=400000):
        ch = ch[ch.serie.str.endswith("ALQM2_LV_M_VC") & ch.codigo.str.startswith(pref) & ch.periodo.isin(["2021", "2024"])]
        rows.append(ch)
    r = pd.concat(rows)
    r["valor"] = r.valor.astype(float)
    rr = r.pivot_table(index="codigo", columns="periodo", values="valor").reset_index().rename(columns={"2021": "r2021", "2024": "r2024"})
    s = zv.merge(rr, on="codigo", how="left").merge(cen[["codigo", "viv_total", "viv_alquiler", "muni"]], on="codigo", how="left")
    s["dVUT"] = s.vut_2024M08 - s.vut_2021M08
    s["q_alq"] = s.dVUT / s.viv_alquiler.replace(0, np.nan)
    s["peso_parque_pct"] = 100 * s.vut_2024M08 / s.viv_total
    s["peso_alquiler_pct"] = 100 * s.vut_2024M08 / s.viv_alquiler.replace(0, np.nan)
    s["dlnR"] = np.log(s.r2024 / s.r2021)
    s["ciudad"] = s.muni.map(CIUDADES)
    c.csv(s, "b1_secciones_ciudades.csv")
    out = []
    for ciudad, g in s.groupby("ciudad"):
        g = g.dropna(subset=["q_alq", "dlnR"])
        g = g[g.viv_alquiler > 0]
        if g.empty:
            continue
        contrib = g.viv_alquiler * g.dlnR
        for u in UMBRALES:
            sel = g.q_alq < u
            out.append(dict(ciudad=ciudad, umbral_pp=100 * u, n_secciones=len(g), n_set=int(sel.sum()),
                            no_explica_seccion_pct=100 * contrib[sel].sum() / contrib.sum() if contrib.sum() > 0 else np.nan,
                            dlnR_medio_pond_pct=100 * contrib.sum() / g.viv_alquiler.sum(), cota_precio_ciudad_epsmin_pct=100 * g.dVUT.sum() / g.viv_alquiler.sum() / EPS_MIN))
    o = pd.DataFrame(out)
    c.csv(o, "b1_no_explica_secciones.csv")
    for r_ in o[o.umbral_pp == 0.1].itertuples():
        c.log(f"B1-seccion-{r_.ciudad}", "no explica por sección, umbral 0.1pp", "2021M08", "2024M08", r_.n_secciones, r_.no_explica_seccion_pct)
    return o


# ---------------------------------------------------------------- B2
def b2(c: Ctx, d: dict, cen: pd.DataFrame):
    nat, pp = d["nat"], d["pp"]
    prov_f = c.smoke
    par = pd.read_csv(RAW / "mivau_parque.csv", usecols=["periodo", "serie", "valor"])
    par = par[par.serie == "parque_total_viviendas_nacional"].set_index("periodo").valor
    par.index = par.index.astype(int)
    stock_alq = cen.viv_alquiler.sum()
    pa = pp.groupby("anio").agg(ext=("pob_extranjera_todas", "sum"), tot=("pob_total_todas", "sum"),
                                term=("terminadas_libres", "sum"), prot=("protegida", "sum"), n=("cod_prov", "nunique"))
    q1 = lambda col, y: float(nat.loc[f"{y}Q1", col])  # noqa: E731  (1 de enero ~ trimestre 1)
    rows, prow = [], []
    for a, b in PERIODOS_B2:
        dext = pa.ext[b] - pa.ext[a]
        dh_epa = 1000 * (q1("hogares_epa", b) - q1("hogares_epa", a))
        dh_ecp = (q1("hogares_ecp", b) - q1("hogares_ecp", a)) if (a >= 2021 and not np.isnan(nat.loc[f"{a}Q1", "hogares_ecp"])) else np.nan
        tam_c = float(nat.loc[f"{b}Q1", "pob_total"] / (1000 * nat.loc[f"{b}Q1", "hogares_epa"]))
        term = pa.term.loc[max(a, 2008):b - 1].sum() + pa.prot.loc[max(a, 2008):b - 1].sum() if a >= 2008 else np.nan
        dlp = lnr(q1("p_tasado", a), q1("p_tasado", b))
        dlr = lnr(q1("ipc_alquiler", a), q1("ipc_alquiler", b))
        for tk, tam in [("min", TAM_EXT["min"]), ("central", tam_c), ("max", TAM_EXT["max"])]:
            dhe = dext / tam
            for fuente, dht in [("EPA", dh_epa), ("ECP", dh_ecp)]:
                if np.isnan(dht):
                    continue
                share = dhe / dht if dht > 0 else np.nan
                for baja in BAJAS:
                    D = dht - (term - baja * float(par[a]) * (b - a)) if not np.isnan(term) else np.nan
                    viv_cota = min(max(dhe, 0), max(D, 0)) if not np.isnan(D) else np.nan
                    for e in EPS_GRID:
                        pc = max(dhe, 0) / float(par[a]) / e
                        pr = max(dhe, 0) / stock_alq / e
                        rows.append(dict(periodo=f"{a}-{b}", tam_ext=tk, tam_hogar_ext=tam, fuente_hogares=fuente, baja_anual=baja, eps=e,
                                         dPob_ext=dext, dH_ext=dhe, dH_total=dht, cuota_max_dH_pct=100 * share if np.isfinite(share) else np.nan,
                                         terminadas=term, D_deficit=D, cota_viviendas=viv_cota,
                                         cota_precio_compra_pct=100 * pc, cota_precio_alquiler_pct=100 * pr,
                                         dlnP_obs_pct=100 * dlp, dlnR_obs_pct=100 * dlr,
                                         no_explica_compra_pct=(100 * max(0.0, 1 - pc / dlp) if dlp > 0 else np.nan),
                                         no_explica_alquiler_pct=(100 * max(0.0, 1 - pr / dlr) if dlr > 0 else np.nan),
                                         saldo_ext_no_positivo=bool(dext <= 0)))
    t = pd.DataFrame(rows)
    c.csv(t, "b2_nacional_sensibilidad.csv")
    # provincias: saldo extranjero y subida en provincias con saldo <= 0
    cp = cen.groupby("prov")[["viv_total", "viv_alquiler"]].sum()
    pw = pp.set_index(["cod_prov", "anio"])
    for a, b in PERIODOS_B2:
        for cod in sorted(pp.cod_prov.unique()):
            if prov_f and cod != prov_f:
                continue
            try:
                x0, x1 = pw.loc[(cod, a)], pw.loc[(cod, b)]
            except KeyError:
                continue
            dext = x1.pob_extranjera_todas - x0.pob_extranjera_todas
            prow.append(dict(periodo=f"{a}-{b}", cod_prov=cod, provincia=x1.provincia, dPob_ext=dext, dH_ext_central=dext / 2.5,
                             dlnP_pct=100 * np.log(x1.p_tasado / x0.p_tasado) if x0.p_tasado > 0 and x1.p_tasado > 0 else np.nan,
                             dlnR_pct=100 * np.log(x1.ipc_alquiler / x0.ipc_alquiler), parque_censo=cp.viv_total.get(cod, np.nan),
                             stock_alq_censo=cp.viv_alquiler.get(cod, np.nan)))
    pr_ = pd.DataFrame(prow)
    pr_["cota_precio_compra_epsmin_pct"] = 100 * np.maximum(pr_.dH_ext_central, 0) / pr_.parque_censo / EPS_MIN
    pr_["cota_precio_alquiler_epsmin_pct"] = 100 * np.maximum(pr_.dH_ext_central, 0) / pr_.stock_alq_censo / EPS_MIN
    c.csv(pr_, "b2_provincias.csv")
    # lo que no puede explicar: parte de la subida (ponderada por parque) en provincias con saldo extranjero <= 0
    nx = []
    for per_, g in pr_.groupby("periodo"):
        for var, lab in [("dlnP_pct", "compra"), ("dlnR_pct", "alquiler")]:
            gg = g.dropna(subset=[var, "parque_censo"])
            pos = gg[gg[var] > 0]
            w_ = pos.parque_censo * pos[var]
            nx.append(dict(periodo=per_, mercado=lab, n_prov=len(gg), n_prov_saldo_no_pos=int((gg.dPob_ext <= 0).sum()),
                           no_explica_saldo_no_pos_pct=100 * w_[pos.dPob_ext <= 0].sum() / w_.sum() if w_.sum() > 0 else np.nan,
                           subida_ponderada_pct=(gg.parque_censo * gg[var]).sum() / gg.parque_censo.sum()))
    nx = pd.DataFrame(nx)
    c.csv(nx, "b2_no_explica_provincias.csv")
    # cotas
    for a, b in PERIODOS_B2:
        pe = f"{a}-{b}"
        g = t[t.periodo == pe]
        if g.empty:
            continue
        extremo = g[(g.tam_ext == "min")]
        base = extremo[(extremo.fuente_hogares == "EPA") & (extremo.baja_anual == 0.0)]
        r0 = base.iloc[0]
        cuota = r0.cuota_max_dH_pct
        saldo_ng = bool(r0.saldo_ext_no_positivo)
        ne_comp = g[(g.tam_ext == "min") & (g.eps == EPS_MIN)].no_explica_compra_pct.iloc[0]
        nxp = nx[(nx.periodo == pe) & (nx.mercado == "compra")]
        lim = ("Hogares extranjeros = ΔPoblación extranjera (padrón, 1 de enero) / tamaño de hogar en rango 2,0-3,0 (supuesto: no hay hogares por nacionalidad en la ECP; "
               "central = personas/hogar nacional); hogares totales = EPA (quiebre 2021) y ECP si existe; sin respuesta de la oferta ni de la población nacional; "
               "|ε_d| implícito de la literatura. Todos los hogares extranjeros netos se suponen demandantes en el mercado considerado.")
        if np.isfinite(cuota) and r0.dH_total > 0:
            c.cota(f"B2-nac-cuota-{pe}", "inmigracion", "nacional", pe, min(cuota, 100.0) if cuota > 0 else 0.0, "% de Σ Δhogares (máx. fracción del déficit atribuible)",
                   "tamaño de hogar extranjero = 2,0 (máximo número de hogares) y todos los hogares extranjeros netos adicionales",
                   100.0 if saldo_ng else (100 - max(cuota, 0)), float(g.cuota_max_dH_pct.min()), float(g.cuota_max_dH_pct.max()), lim,
                   "la población extranjera neta")
        if not np.isnan(r0.cota_viviendas):
            c.cota(f"B2-nac-viviendas-{pe}", "inmigracion", "nacional", pe, r0.cota_viviendas, "viviendas del déficit A1 (con bajas 0 %)",
                   "tamaño de hogar 2,0 y bajas 0 %", None, float(g.cota_viviendas.min()), float(g.cota_viviendas.max()), lim, "la población extranjera neta")
        for mk, col, nec in [("compra", "cota_precio_compra_pct", "no_explica_compra_pct"), ("alquiler", "cota_precio_alquiler_pct", "no_explica_alquiler_pct")]:
            gm = g[(g.tam_ext == "min") & (g.eps == EPS_MIN) & (g.fuente_hogares == "EPA") & (g.baja_anual == 0.0)].iloc[0]
            lo, hi = float(g[col].min()), float(g[col].max())
            c.cota(f"B2-nac-precio-{mk}-{pe}", "inmigracion", "nacional", pe, gm[col], "% de precio (Δ ln)" if mk == "compra" else "% de alquiler (Δ ln)",
                   f"tamaño de hogar 2,0 y |ε_d|={EPS_MIN}" + ("; saldo extranjero ≤ 0: cota 0" if saldo_ng else ""),
                   gm[nec], lo, hi, lim + (" Nota: en este periodo el Δ ln observado no es positivo, el «no explica» no se define." if not np.isfinite(gm[nec]) else ""),
                   "el saldo de hogares extranjeros")
        c.log(f"B2-nac-{pe}", "cuota_max=dH_ext(tam=2.0)/sum dH_total", a, b, int(pa.n[b]), cuota,
              f"saldo_ext_no_pos={saldo_ng}; no_explica_compra={ne_comp:.1f}; prov_saldo_no_pos={nxp.n_prov_saldo_no_pos.iloc[0] if len(nxp) else ''}")
    return dict(t=t, nx=nx, pr=pr_)


# ---------------------------------------------------------------- B4
def b4(c: Ctx, d: dict):
    nat = d["nat"].copy()
    nat["anio"] = nat.index.str[:4].astype(int)
    an = nat.groupby("anio")[["tipo_hip", "tipo_hip_real", "p_tasado", "ipv", "ipc_alquiler", "coste_uso_aprox"]].mean()
    pers = [(2014, 2021), (2021, 2025), (2007, 2014)]       # el tercero (2007-2014) es solo informativo (signo)
    filas, suelos = [], []
    for (a, b), dep, g, ibi in product(pers, DEP, GAN, IBI):
        i0, i1 = an.tipo_hip[a], an.tipo_hip[b]
        uc0, uc1 = i0 + dep + ibi - g, i1 + dep + ibi - g
        ok = (uc0 >= UC_SUELO) and (uc1 >= UC_SUELO)
        filas.append(dict(periodo=f"{a}-{b}", dep=dep, ganancia=g, ibi=ibi, tipo0=i0, tipo1=i1, uc0=uc0, uc1=uc1, definido=ok,
                          dln_inv_uc_pct=100 * np.log(uc0 / uc1) if ok else np.nan))
    t = pd.DataFrame(filas)
    c.csv(t, "b4_rejilla.csv")
    res = []
    for a, b in pers:
        pe = f"{a}-{b}"
        g = t[t.periodo == pe]
        gd = g[g.definido]
        dlp = 100 * lnr(an.p_tasado[a], an.p_tasado[b])
        dlv = 100 * lnr(an.ipv[a], an.ipv[b]) if not np.isnan(an.ipv[a]) else np.nan
        dlr = 100 * lnr(an.ipc_alquiler[a], an.ipc_alquiler[b])
        mx, mn = gd.dln_inv_uc_pct.max(), gd.dln_inv_uc_pct.min()
        ext = gd.loc[gd.dln_inv_uc_pct.idxmax()]
        signo_contrario = (mx < 0 and dlp > 0) or (mn > 0 and dlp < 0)
        ne = 100.0 if (mx <= 0 < dlp) else (100 * max(0.0, 1 - mx / dlp) if dlp > 0 else np.nan)
        res.append(dict(periodo=pe, tipo_ini=an.tipo_hip[a], tipo_fin=an.tipo_hip[b], n_combos=len(g), n_definidos=len(gd),
                        dln_inv_uc_min_pct=mn, dln_inv_uc_max_pct=mx, dln_inv_uc_central_pct=gd[(gd.dep == 2.0) & (gd.ganancia == 1.5) & (gd.ibi == 0.75)].dln_inv_uc_pct.mean(),
                        dlnP_tasado_pct=dlp, dlnIPV_pct=dlv, dlnR_pct=dlr, signo_contrario=bool(signo_contrario),
                        no_explica_compra_pct=ne, no_explica_alquiler_pct=100.0,
                        extremo=f"dep={ext.dep}, ganancia={ext.ganancia}, ibi={ext.ibi}", coste_uso_v2_ini=an.coste_uso_aprox[a], coste_uso_v2_fin=an.coste_uso_aprox[b]))
        # sensibilidad al suelo de uc
        sm = []
        for suelo in (0.5, 1.0, 2.0):
            gg = g[(g.uc0 >= suelo) & (g.uc1 >= suelo)]
            v = 100 * np.log(gg.uc0 / gg.uc1)
            sm.append(dict(periodo=pe, suelo_uc=suelo, n_definidos=len(gg), dln_inv_uc_min_pct=v.min(), dln_inv_uc_max_pct=v.max()))
            c.log(f"B4-{pe}-suelo{suelo}", "dln(1/uc)=ln(uc0/uc1)", a, b, len(gg), float(v.max()), f"min={v.min():.2f}")
        suelos.append(pd.DataFrame(sm))
        res[-1]["sens_min"], res[-1]["sens_max"] = min(x["dln_inv_uc_min_pct"] for x in sm), max(x["dln_inv_uc_max_pct"] for x in sm)
    r = pd.DataFrame(res)
    c.csv(r, "b4_periodos.csv")
    c.csv(pd.concat(suelos), "b4_sensibilidad_suelo_uc.csv")
    # real (referencia): tipo real ex-post con ganancia real; casi todo indefinido
    real = []
    for (a, b), dep, g, ibi in product(pers[:2], DEP, GAN, IBI):
        u0, u1 = an.tipo_hip_real[a] + dep + ibi - g, an.tipo_hip_real[b] + dep + ibi - g
        real.append(dict(periodo=f"{a}-{b}", definido=bool(u0 >= UC_SUELO and u1 >= UC_SUELO)))
    c.csv(pd.DataFrame(real).groupby("periodo").definido.agg(["sum", "count"]).reset_index().rename(columns={"sum": "n_definidos", "count": "n_combos"}),
          "b4_variante_tipo_real_definidos.csv")
    lim = ("uc = tipo hipotecario nominal (media anual, BdE) + depreciación + IBI - ganancia esperada, estado estacionario P/R = 1/uc; "
           "sin impuestos ni deducciones, sin racionamiento de crédito, expectativas fijas; combinaciones con uc < 1 % se excluyen (1/uc sin cota). "
           "Los tipos no actúan directamente sobre el alquiler.")
    for r_ in r.itertuples():
        if r_.periodo == "2007-2014":
            continue
        pe = r_.periodo
        c.cota(f"B4-nac-{pe}", "tipos", "nacional", pe, r_.dln_inv_uc_max_pct, "% de precio de compra (Δ ln(1/uc))",
               f"{r_.extremo} (uc más bajo permitido)" + ("; SIGNO CONTRARIO: la cota superior es negativa" if r_.signo_contrario else ""),
               r_.no_explica_compra_pct, r_.sens_min, r_.sens_max, lim + " Sensibilidad: suelo de uc 0,5-2 %.", "la variación del coste de uso")
        c.cota(f"B4-nac-alquiler-{pe}", "tipos", "nacional", pe, 0.0, "% de alquiler (sin canal directo)", "los tipos no entran en el alquiler por supuesto",
               100.0, None, None, "El estado estacionario de B4 solo acota el precio de compra.", "los tipos")
    return r


# ---------------------------------------------------------------- figuras
def figuras(c: Ctx, r1: dict, r2: dict, r4: pd.DataFrame):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    f = c.tab / "b1_ciudades.csv"
    if f.exists():
        ci = pd.read_csv(f)
        fig, ax = plt.subplots(figsize=(7, 4))
        x = np.arange(len(ci))
        ax.bar(x - 0.2, ci.cota_precio_epsmin_pct, 0.4, label="cota de precio (|ε_d|=0,33)")
        ax.bar(x + 0.2, ci.dlnR_obs_pct, 0.4, label="Δ ln alquiler SERPAVI 2020-2024")
        ax.set_xticks(x, ci.ciudad)
        ax.axhline(0, color="k", lw=0.5)
        ax.set_ylabel("%")
        ax.set_title("B1 (C2): cota superior de turísticos vs subida observada")
        ax.legend()
        fig.tight_layout()
        fig.savefig(c.fig / "b1_ciudades.png", dpi=120)
        plt.close(fig)
    t = r2["t"]
    g = t[(t.fuente_hogares == "EPA") & (t.baja_anual == 0.0) & (t.eps == EPS_MIN)].pivot_table(index="periodo", columns="tam_ext", values="cuota_max_dH_pct")
    fig, ax = plt.subplots(figsize=(7, 4))
    g[["max", "min"]].plot.bar(ax=ax)
    ax.set_ylabel("% de Σ Δhogares")
    ax.set_title("B2 (C2): cuota máxima de la población extranjera neta (tamaño 3,0 / 2,0)")
    fig.tight_layout()
    fig.savefig(c.fig / "b2_cuota.png", dpi=120)
    plt.close(fig)
    r = r4[r4.periodo != "2007-2014"]
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(r))
    ax.bar(x - 0.2, r.dln_inv_uc_max_pct, 0.4, yerr=[r.dln_inv_uc_max_pct - r.dln_inv_uc_min_pct, np.zeros(len(r))], label="Δ ln(1/uc): máx. (barra hasta mín.)")
    ax.bar(x + 0.2, r.dlnP_tasado_pct, 0.4, label="Δ ln precio tasado")
    ax.set_xticks(x, r.periodo)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_ylabel("%")
    ax.set_title("B4 (C2): coste de uso vs precio")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(c.fig / "b4_tipos.png", dpi=120)
    plt.close(fig)


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", default=None, help="código de provincia para el smoke test (p. ej. 46)")
    a = ap.parse_args(argv)
    out = RAIZ / "output" / "v3" / "PB"
    if a.smoke:
        out = Path(tempfile.mkdtemp(prefix="pb_smoke_"))
    out.mkdir(parents=True, exist_ok=True)
    c = Ctx(out, a.smoke)
    gt = ingesta_gt()           # B3: solo ingesta -> output/v3/PB/grandes_tenedores.json
    d = cargar()
    cen = censo_secciones()
    r1 = b1(c, d, cen)
    r2 = b2(c, d, cen)
    r4 = b4(c, d)
    if not a.smoke:
        figuras(c, r1, r2, r4)
    c.cota("B3-espera", "grandes_tenedores", "nacional", "", None, "n/d", "sin datos: solicitud de transparencia pendiente", None, None, None,
           f"Estado: {gt.get('estado')}. Se definirá con el esquema de B1 (variación de la cuota de grandes tenedores en el alquiler).", "los grandes tenedores")
    (out / "cotas.json").write_text(json.dumps(c.cotas, ensure_ascii=False, indent=1))
    q = r1["qmain"]
    nac = {k["id"]: k for k in c.cotas}
    res = {
        "rama": "PB", "pregunta": "¿Qué parte máxima de la subida de precios y alquileres puede atribuirse a turísticos, inmigración, grandes tenedores y tipos, bajo supuestos débiles?",
        "datos": "paneles completos (holdout.load_full, uso PB); INE VUT (JAXI y sección); Censo 2021 (alquiler por sección); SERPAVI; padrón; EPA/ECP; BdE tipos",
        "N": {"municipios_B1": int(len(pd.read_csv(c.tab / "b1_municipio.csv"))), "provincias": int(d["pp"].cod_prov.nunique())},
        "metodo": "identificación parcial (cotas de Manski): sustitución 1:1, traspaso completo, ε_d implícito de la literatura, estado estacionario P/R=1/uc",
        "estimacion": {"B1_precio_eps_min_pct": nac["B1-nac-precio-eps_min"]["cota_superior"], "B1_precio_central_pct": nac["B1-nac-precio-central"]["cota_superior"],
                       "B1_cantidad_pct": nac["B1-nac-cantidad"]["cota_superior"], "B1_no_explica_pct": nac["B1-nac-cantidad"]["no_explica"],
                       "B2_cuota_max_2014-2025_pct": nac.get("B2-nac-cuota-2014-2025", {}).get("cota_superior"),
                       "B2_cuota_max_2020-2025_pct": nac.get("B2-nac-cuota-2020-2025", {}).get("cota_superior"),
                       "B4_dln_inv_uc_max_2014-2021_pct": nac["B4-nac-2014-2021"]["cota_superior"],
                       "B4_dln_inv_uc_max_2021-2025_pct": nac["B4-nac-2021-2025"]["cota_superior"]},
        "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "COTA C2 (identificación parcial; no CAUSAL)",
        "diagnosticos": {"cobertura_stock_alquiler_B1_municipal": float(r1["cob"]) if np.isfinite(r1["cob"]) else None,
                         "B3": gt.get("estado"), "FDR": "no aplica: sin contrastes de hipótesis"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": ["No hay predicción fuera de muestra: las cotas son aritmética bajo supuestos, no modelos predictivos (sin DM ni AR(4)).",
                  "Sin lenguaje causal: solo «como máximo X puede atribuirse a Y bajo el supuesto Z».",
                  "|ε_d| (0,33-1,0) es implícito de González y Ortega (2013) y Saiz (2007); laguna de la literatura v3 B: sin estimación verificada para España.",
                  "Total JAXI para cifras nacionales de VUT; la suma por sección cubre solo 89-90 %.",
                  "Hogares por nacionalidad no existen en la ECP: tamaño de hogar extranjero en rango 2,0-3,0 (supuesto).",
                  "EPA tiene quiebre en 2021 (se contrasta con ECP).", *c.notas],
    }
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    c.reg.flush()
    print("PB listo:", out, "cotas:", len(c.cotas), "q_main_precio:", round(q.cota_precio_pct, 2))
    return out


if __name__ == "__main__":
    main()
