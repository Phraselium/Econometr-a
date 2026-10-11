"""M4 v6: tabla unica de modelos, sintesis por variable y mercado, fichas del verificador. Entra en make.

Lee SOLO los sellado_*.json versionados de output/v6/M4 (no reabre el sellado) y los resultados versionados de M1A, M1B,
M2, M3A y M3B. Sin red; SEED=20261010; un hilo. Capa maxima C4: nada causal desde importancias, SHAP, ALE o PDP.
Limitacion de la validacion: espacial nueva; temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src/v6"))
import m3a_lib as A  # noqa: E402
from econ_utils import Registry  # noqa: E402

SEED = 20261010
V6 = RAIZ / "output/v6"
OUT = V6 / "M4"
FECHA = "2026-10-11"
GRUPOS = ("espacial", "temporal", "conjunta", "total")
BASES = ("persistencia", "ar_unidad", "ecm_v1")
LIM = ("Validacion espacial nueva (11 provincias nunca usadas como validacion); temporal ya vista en v2 (otras provincias) y "
       "de forma descriptiva en v4-v5; el ultimo anio cae en la ventana sellada de v2. Las conclusiones se apoyan en la parte espacial.")
EXP = {  # signo esperado (hipotesis.md seccion 2); 0 = sin signo a priori
    "alq": {"ln_pob": 1, "share_ext_pob": 1, "ln_pib_pc": 1, "ln_vut": 1, "ln_terminadas_libres": -1, "ln_iniciadas_libres": -1,
            "n_mun_tensionados": -1, "n_mun_topes_cat": -1},
    "cp": {"ln_pob": 1, "share_ext_pob": 1, "ln_pib_pc": 1, "ln_ocupados_miles": 1, "paro_tasa": -1, "ln_terminadas_libres": -1,
           "ln_iniciadas_libres": -1, "ln_suelo_pm2_m50k": 1, "ln_vut": 0, "ln_hip_viv_num": 1},
    "vol": {"ln_pib_pc": 1, "ln_ocupados_miles": 1, "ln_pob": 1, "paro_tasa": -1, "ln_terminadas_libres": 0, "ln_iniciadas_libres": 0},
}
FAM_M3B = {"ln_pob": "demanda_poblacion", "share_ext_pob": "demanda_poblacion", "ln_vut": "demanda_poblacion",
           "ln_pib_pc": "renta_empleo", "paro_tasa": "renta_empleo", "ln_ocupados_miles": "renta_empleo",
           "ln_terminadas_libres": "oferta_suelo", "ln_iniciadas_libres": "oferta_suelo", "ln_suelo_pm2_m50k": "oferta_suelo",
           "ln_hip_viv_num": "credito_hipotecas"}
REG = Registry(OUT / "registro.csv")


# ---------------------------------------------------------------- DM-HLN (h=1, perdida cuadratica, cola a favor del modelo)
def dm(l1, l2):
    d = np.asarray(l1, float) - np.asarray(l2, float)
    n = len(d)
    if n < 3 or np.allclose(d, 0):
        return np.nan, np.nan
    dc = d - d.mean()
    lrv = dc @ dc / n
    if lrv <= 0:
        return np.nan, np.nan
    st = d.mean() / np.sqrt(lrv / n) * np.sqrt((n - 1) / n)
    return float(st), float(stats.t.cdf(st, n - 1))  # p de una cola: H1 = el modelo 1 tiene menor error


def holm(p):
    return A.holm(p)


def carga():
    modelos = {}
    for f in sorted(OUT.glob("sellado_*.json")):
        d = json.loads(f.read_text())
        if d.get("estado") == "evaluado":
            modelos[d["modelo_id"]] = d
    return modelos


def cel(d):
    c = pd.DataFrame(d["celdas"])
    c["l"] = c.sse / c.n
    return c


# ---------------------------------------------------------------- (a) tabla de modelos
def tabla_modelos(modelos):
    filas, pcs = [], []
    por_tarea = {}
    for k, d in modelos.items():
        por_tarea.setdefault(d["tarea"], []).append(d)
    for tid, lst in por_tarea.items():
        base = {b: next((x for x in lst if x["rol"] == "base" and x["modelo"] == b), None) for b in BASES + ("m1_econ",)}
        for g in GRUPOS:
            comp = []
            for d in lst:
                c = cel(d)
                cg = c if g == "total" else c[c.grupo == g]
                for b in BASES:
                    bd = base[b]
                    if bd is None or d is bd:
                        continue
                    cb = cel(bd)
                    cb = cb if g == "total" else cb[cb.grupo == g]
                    m = cg.merge(cb, on=["cod_prov", "per", "grupo"], suffixes=("", "_b"))
                    m = m.sort_values(["per", "cod_prov"])
                    st, p = dm(m.l, m.l_b)
                    pa = m.groupby("per")[["l", "l_b"]].mean()
                    stp, pp = dm(pa.l, pa.l_b)
                    comp.append(dict(modelo_id=d["modelo_id"], base=b, dm=st, p=p, dm_per=stp, p_per=pp, n_celdas=len(m)))
            comp = pd.DataFrame(comp)
            if len(comp):
                comp["p_holm"] = holm(comp.p.to_numpy())
                comp["p_holm_per"] = holm(comp.p_per.to_numpy())
            for d in lst:
                c = cel(d)
                cg = c if g == "total" else c[c.grupo == g]
                m_ = d["metricas"][g]
                if not m_["n"]:
                    continue
                pr = cg.assign(r=np.sqrt(cg.sse / cg.n)).groupby("per").r.mean()
                pv = cg.assign(r=np.sqrt(cg.sse / cg.n)).groupby("cod_prov").r.mean()
                fila = dict(tarea=tid, mercado=d["mercado"], medida=d["medida"], medida_precio=d["medida_precio"], nivel=d["nivel"],
                            modelo_id=d["modelo_id"], familia=d["familia"], rol=d["rol"], grupo=g, n=m_["n"], rmse_ln=m_["rmse"],
                            mae_ln=m_["mae"], rmse_pct=100 * m_["rmse"], cobertura95=m_["cobertura95"],
                            sd_rmse_entre_periodos=float(pr.std(ddof=1)) if len(pr) > 1 else np.nan,
                            sd_rmse_entre_provincias=float(pv.std(ddof=1)) if len(pv) > 1 else np.nan,
                            n_fallback_persistencia=d["n_fallback_persistencia"])
                for b in BASES:
                    r = comp[(comp.modelo_id == d["modelo_id"]) & (comp.base == b)] if len(comp) else comp
                    if len(r):
                        r = r.iloc[0]
                        fila.update({f"dm_vs_{b}": r.dm, f"p_vs_{b}": r.p, f"p_holm_vs_{b}": r.p_holm, f"p_per_holm_vs_{b}": r.p_holm_per})
                    bd = base[b]
                    if bd is not None and bd["metricas"][g]["rmse"]:
                        fila[f"ratio_rmse_vs_{b}"] = m_["rmse"] / bd["metricas"][g]["rmse"]
                filas.append(fila)
    T = pd.DataFrame(filas)
    return T


def mejores(T):
    """Mejor modelo por tarea: menor RMSE espacial; si hay empate tecnico (<=5 %), el de menor dispersion entre periodos.
    Nunca por R2. Si el mejor es una linea base, se declara que no se bate."""
    res = []
    for tid, t in T[T.grupo == "espacial"].groupby("tarea"):
        t = t.dropna(subset=["rmse_ln"])
        mn = t.rmse_ln.min()
        cand = t[t.rmse_ln <= 1.05 * mn].sort_values(["sd_rmse_entre_periodos", "rmse_ln"], na_position="last")
        b = cand.iloc[0]
        per = t[t.modelo_id.str.endswith("persistencia")].iloc[0]
        tot = T[(T.tarea == tid) & (T.grupo == "total") & (T.modelo_id == b.modelo_id)]
        tem = T[(T.tarea == tid) & (T.grupo == "temporal") & (T.modelo_id == b.modelo_id)]
        tpe = T[(T.tarea == tid) & (T.grupo == "temporal") & (T.modelo_id.str.endswith("persistencia"))]
        es_base = b.rol == "base"
        ml = t[t.rol == "modelo"].sort_values("rmse_ln").iloc[0]
        bate_per = bool(b.rmse_ln < per.rmse_ln and (b.get("p_holm_vs_persistencia", 1) or 1) < 0.05) if not es_base else False
        ml_bate_per = bool(ml.rmse_ln < per.rmse_ln and (ml.get("p_holm_vs_persistencia", 1) or 1) < 0.05)
        ml_bate_ecm = bool(ml.get("ratio_rmse_vs_ecm_v1", 9) < 1 and (ml.get("p_holm_vs_ecm_v1", 1) or 1) < 0.05)
        ml_bate_ar = bool(ml.get("ratio_rmse_vs_ar_unidad", 9) < 1 and (ml.get("p_holm_vs_ar_unidad", 1) or 1) < 0.05)
        if es_base:
            lec = (f"El mejor es la linea base {b.modelo_id.split('__')[-1]}: el mejor modelo de M3 ({ml.modelo_id}) no la mejora "
                   f"en mas de un 5 % de RMSE en la parte espacial.")
        elif bate_per:
            lec = "Bate a la persistencia en la parte espacial (DM-HLN una cola, Holm)."
        else:
            lec = "No bate a la persistencia con DM-HLN y Holm en la parte espacial."
        res.append(dict(tarea=tid, mercado=b.mercado, medida=b.medida, medida_precio=b.medida_precio, nivel=b.nivel,
                        mejor_modelo=b.modelo_id, familia=b.familia, rol=b.rol, rmse_espacial=b.rmse_ln, n_espacial=b.n,
                        rmse_pct_espacial=b.rmse_pct, cobertura95_espacial=b.cobertura95,
                        sd_rmse_entre_periodos=b.sd_rmse_entre_periodos, rmse_persistencia_espacial=per.rmse_ln,
                        p_holm_vs_persistencia=b.get("p_holm_vs_persistencia"), p_holm_vs_ar=b.get("p_holm_vs_ar_unidad"),
                        p_holm_vs_ecm=b.get("p_holm_vs_ecm_v1"), dm_vs_ar=b.get("dm_vs_ar_unidad"),
                        mejor_m3=ml.modelo_id, rmse_m3_espacial=ml.rmse_ln, m3_bate_persistencia=ml_bate_per,
                        m3_bate_ar=ml_bate_ar, m3_bate_ecm=ml_bate_ecm,
                        rmse_temporal=float(tem.rmse_ln.iloc[0]) if len(tem) else np.nan,
                        rmse_temporal_persistencia=float(tpe.rmse_ln.iloc[0]) if len(tpe) else np.nan,
                        rmse_total=float(tot.rmse_ln.iloc[0]) if len(tot) else np.nan,
                        bate_persistencia=bate_per, lectura=lec,
                        criterio="menor RMSE espacial sellado; empate tecnico (<=5 %) por menor dispersion entre periodos; nunca R2"))
    return pd.DataFrame(res)


def persistencia_por_grupo(T):
    """Para cada tarea y grupo: el mejor modelo de M3 frente a la persistencia (resultado negativo si no la bate)."""
    f = []
    for (tid, g), t in T.groupby(["tarea", "grupo"]):
        m = t[t.rol == "modelo"].dropna(subset=["rmse_ln"])
        pe = t[t.modelo_id.str.endswith("persistencia")]
        if m.empty or pe.empty:
            continue
        b = m.sort_values("rmse_ln").iloc[0]
        p = b.get("p_holm_vs_persistencia")
        f.append(dict(tarea=tid, grupo=g, mejor_m3=b.modelo_id, rmse_m3=b.rmse_ln, rmse_persistencia=pe.rmse_ln.iloc[0],
                      p_holm_vs_persistencia=p,
                      bate_persistencia=bool(b.rmse_ln < pe.rmse_ln.iloc[0] and p is not None and not pd.isna(p) and p < 0.05)))
    return pd.DataFrame(f)


# ---------------------------------------------------------------- (b) sintesis por variable y mercado
def signo(x, umbral=0.0):
    return 0 if x is None or pd.isna(x) or abs(x) <= umbral else int(np.sign(x))


def ale_signo(x, y):
    if len(x) < 2:
        return 0
    return signo(y[-1] - y[0], 1e-9)


def sintesis(T):
    m1a = pd.read_csv(V6 / "M1A/tabla_coeficientes.csv")
    m1a = m1a[(m1a.mercado == "alquiler de stock") & (m1a.nivel == "provincia") & m1a.spec.str.startswith("S0 pre")]
    fe = pd.read_csv(V6 / "M1B/tablas/fe_prov.csv")
    fe = fe[fe.spec == "S1_prereg_10"]
    mult = pd.read_csv(V6 / "M1B/tablas/multiplicidad_p_ajustados.csv")
    m2a = pd.read_csv(V6 / "M2/peso_variables.csv").set_index("variable")
    m2v = pd.read_csv(V6 / "M2/peso_variables_volumen.csv").set_index("variable")
    imp_a = pd.read_csv(V6 / "M3A/importancia_permutacion_provincia.csv", index_col=0)
    ale_a = json.loads((V6 / "M3A/interpretacion.json").read_text())["ale"]["provincia"]
    fichas_a = {f["id"]: json.loads((RAIZ / f["ruta"]).read_text()) for f in json.loads((V6 / "M3A/modelos_finales.json").read_text())
                if f["nivel"] == "provincia"}
    fichas_b = {f["especificacion"]["setting"]: f for f in json.loads((V6 / "M3B/modelos_finales.json").read_text())}
    out = []
    for mk, etq in (("alq", "alquiler de stock (SERPAVI)"), ("cp", "compra (precio, valor tasado MIVAU)"), ("vol", "compra (volumen, ETDP)")):
        for v, es in EXP[mk].items():
            r = dict(mercado=etq, variable=v, signo_esperado=es)
            # ---- F1: econometria
            if mk == "alq":
                x = m1a[m1a["var"] == v]
                if len(x):
                    x = x.iloc[0]
                    r.update(F1_coef=x.b, F1_lo=x.lo, F1_hi=x.hi, F1_p_wcb=x.p, F1_p_holm=x.p_ajustado, F1_unidad=x.unidad,
                             mag_M1_eur_mes=x.eur_mes, mag_M1_lo=x.eur_mes_lo, mag_M1_hi=x.eur_mes_hi, mag_unidad="EUR/mes")
                m2 = m2a.loc[v] if v in m2a.index else None
                pre = "ALQ_"
            else:
                y = "ln_pm2_tasado" if mk == "cp" else "ln_cv_etdp"
                x = fe[(fe.y == y) & (fe["var"] == v)]
                if len(x):
                    x = x.iloc[0]
                    tq = stats.t.ppf(0.975, int(x.clusters) - 1)
                    ph = mult[mult.id == f"A_fe_prov_anual|S1_prereg_10|{y}|{v}"]
                    r.update(F1_coef=x.coef, F1_lo=x.coef - tq * x.se_cr1, F1_hi=x.coef + tq * x.se_cr1, F1_p_wcb=x.p_wcb,
                             F1_p_holm=float(ph.p_adj.iloc[0]) if len(ph) else np.nan,
                             F1_unidad="log-puntos de ln(Y) por log-punto o punto de X",
                             mag_M1_eur_mes=x.efecto_abs, mag_unidad=x.unidad_abs if mk == "cp" else "% de compraventas",
                             mag_M1_pct=x.efecto_pct_unidad)
                if mk == "cp":
                    m2, pre = (m2a.loc[v] if v in m2a.index else None), "COMPRA_"
                else:
                    m2, pre = (m2v.loc[v] if v in m2v.index else None), ""
            # ---- F2: BMA / multiverso
            if m2 is not None:
                r.update(PIP=float(m2[pre + "pip"]), bma_media_pct=float(m2[pre + "bma_media_pct"]),
                         multiverso_mediana_pct=float(m2[pre + "mv_mediana_pct"]), multiverso_pct_mismo_signo=float(m2[pre + "mv_pct_mismo_signo"]),
                         mag_M2_p25=float(m2[pre + "mv_abs_p25"]), mag_M2_mediana=float(m2[pre + "mv_abs_mediana"]),
                         mag_M2_p75=float(m2[pre + "mv_abs_p75"]), mag_M2_unidad=m2[pre + "unidad_abs"])
            # ---- F3: ML (permutacion por familia sobre el ruido + signo de ALE)
            if mk == "alq":
                fam = A.FAM_DE.get(v)
                if fam in imp_a.index:
                    r.update(F3_familia=fam, F3_importancia=float(imp_a.loc[fam, "media"]),
                             F3_sobre_ruido=bool(imp_a.loc[fam, "por_encima_del_ruido"]))
                a = ale_a.get(v)
                ids = list(fichas_a)
                mod_incl = [i for i in ids if v in fichas_a[i]["variables"]]
                tid = "alq_provincia"
            else:
                tid = "PROV_PRECIO_ANUAL" if mk == "cp" else "PROV_VOL_ANUAL"
                fam = FAM_M3B[v]
                pa = pd.read_csv(V6 / f"M3B/tablas/permutacion_agrupada_{tid}.csv", index_col=0)
                col = pa[fam]
                nz = col[col != 0]
                r.update(F3_familia=fam, F3_importancia=float(col.mean()),
                         F3_sobre_ruido=bool(len(nz) > 0 and (nz > 0).all()),
                         F3_nota="M3B sin referencia de ruido: se exige importancia > 0 en todos los pliegues con valor distinto de 0")
                fa = V6 / f"M3B/tablas/ale_{tid}_{v}_l1.csv"
                a = None
                if fa.exists():
                    ale = pd.read_csv(fa)
                    a = {"x": ale.x.tolist(), "ale": ale.ale.tolist()}
                feats = [f.removesuffix("_l1") for f in fichas_b[tid]["especificacion"]["features"]]
                mod_incl = [fichas_b[tid]["id"]] if v in feats else []
            r["F3_signo_ALE"] = ale_signo(a["x"], a["ale"]) if a else np.nan
            # ---- criterio A (3 familias, mismo signo que el esperado)
            s1 = signo(r.get("F1_coef"))
            f1 = bool(es != 0 and r.get("F1_p_holm", 1) is not None and r.get("F1_p_holm", 1) < 0.05 and s1 == es)
            f2 = bool(es != 0 and r.get("PIP", 0) >= 0.5 and signo(r.get("bma_media_pct")) == es)
            f3 = bool(es != 0 and r.get("F3_sobre_ruido", False) and r.get("F3_signo_ALE") == es)
            r.update(signo_F1=s1, signo_F2=signo(r.get("bma_media_pct")), signo_F3=r.get("F3_signo_ALE"),
                     F1_ok=f1, F2_ok=f2, F3_ok=f3, n_familias_ok=int(f1) + int(f2) + int(f3),
                     criterio_A=bool(es != 0 and int(f1) + int(f2) + int(f3) >= 2))
            # ---- criterio B (mejor modelo que incluye la variable bate a AR y ECM v1 en la sellada, espacial)
            cand = T[(T.tarea == tid) & (T.grupo == "espacial") & (T.modelo_id.isin(mod_incl)) & (T.rol == "modelo")]
            if len(cand):
                b = cand.sort_values("rmse_ln").iloc[0]
                ok_ar = (b.get("ratio_rmse_vs_ar_unidad", 9) < 1) and (b.get("p_holm_vs_ar_unidad", 1) < 0.05)
                ok_ecm = (b.get("ratio_rmse_vs_ecm_v1", 9) < 1) and (b.get("p_holm_vs_ecm_v1", 1) < 0.05)
                ok_per = (b.get("ratio_rmse_vs_persistencia", 9) < 1) and (b.get("p_holm_vs_persistencia", 1) < 0.05)
                r.update(B_modelo=b.modelo_id, B_rmse_espacial=b.rmse_ln, B_ratio_vs_ar=b.get("ratio_rmse_vs_ar_unidad"),
                         B_ratio_vs_ecm=b.get("ratio_rmse_vs_ecm_v1"), B_p_holm_vs_ar=b.get("p_holm_vs_ar_unidad"),
                         B_p_holm_vs_ecm=b.get("p_holm_vs_ecm_v1"), B_bate_persistencia=bool(ok_per),
                         B_p_per_holm_vs_ar=b.get("p_per_holm_vs_ar_unidad"), B_p_per_holm_vs_ecm=b.get("p_per_holm_vs_ecm_v1"),
                         criterio_B=bool(ok_ar and ok_ecm))
            else:
                r["criterio_B"] = False
            r["relevante_con_seguridad"] = bool(r["criterio_A"] and r["criterio_B"])
            fam_ok = r["n_familias_ok"]
            r["capa"] = "C4"
            r["clasificacion"] = ("RELEVANTE CON SEGURIDAD (criterio pre-registrado A y B)" if r["relevante_con_seguridad"]
                                  else ("EXPLORATORIA (C4): cumple A, no B" if r["criterio_A"]
                                        else ("EXPLORATORIA (C4): apoyo en una familia" if fam_ok == 1
                                              else "SIN APOYO suficiente (C4)")))
            r["direccion"] = {1: "positiva", -1: "negativa", 0: "sin direccion estable"}[
                int(np.sign(sum(x for x in (r["signo_F1"], r["signo_F2"], r["signo_F3"] if not pd.isna(r["signo_F3"]) else 0)))) ]
            out.append(r)
    S = pd.DataFrame(out)
    # lo que pesa en un mercado y no en el otro (variables comunes alquiler / compra-precio)
    S["pesa"] = (S.n_familias_ok >= 1) | (S.PIP.fillna(0) >= 0.5)
    comp = []
    for v in sorted(set(EXP["alq"]) & set(EXP["cp"])):
        a = S[(S.variable == v) & S.mercado.str.startswith("alquiler")].iloc[0]
        c = S[(S.variable == v) & S.mercado.str.startswith("compra (precio")].iloc[0]
        comp.append(dict(variable=v, pesa_alquiler=bool(a.pesa), pesa_compra=bool(c.pesa), PIP_alq=a.PIP, PIP_compra=c.PIP,
                         dir_alq=a.direccion, dir_compra=c.direccion,
                         lectura=("pesa en ambos" if a.pesa and c.pesa else "pesa en alquiler y no en compra" if a.pesa
                                  else "pesa en compra y no en alquiler" if c.pesa else "no pesa en ninguno")))
    return S, pd.DataFrame(comp)


# ---------------------------------------------------------------- (c) fichas
def f4(x, n=4):
    return "n/d" if x is None or pd.isna(x) else f"{x:.{n}f}".replace(".", ",")


def fichas(T, M, S, C):
    def mejor(t):
        return M[M.tarea == t].iloc[0]

    def lista(mercado_pref, sol="relevante"):
        s = S[S.mercado.str.startswith(mercado_pref)]
        return s

    ev = ["output/v6/M4/tabla_modelos.csv", "output/v6/M4/mejor_modelo.csv", "output/v6/M4/sintesis_variables.csv"]
    # alquiler
    sa = lista("alquiler")
    ma = mejor("alq_provincia")
    ap = sa[sa.n_familias_ok >= 1].variable.tolist()
    a_rel = sa[sa.relevante_con_seguridad].variable.tolist()
    pib_a = sa[sa.PIP >= 0.5].variable.tolist()
    # compra
    sc = lista("compra (precio")
    mc = mejor("PROV_PRECIO_ANUAL")
    cp = sc[sc.n_familias_ok >= 1].variable.tolist()
    c_rel = sc[sc.relevante_con_seguridad].variable.tolist()
    pip_c = sc[sc.PIP >= 0.5].variable.tolist()
    ficha = []
    ficha.append(dict(
        id="M4-V1", tema="Diferencias entre provincias en la subida del alquiler",
        enunciado="Que explica que unas provincias suban mas que otras en alquiler.", capa="C4",
        magnitud=(f"Alquiler de stock (SERPAVI), 41 provincias de entrenamiento y 11 selladas, datos hasta 2023-2024. Variables con apoyo en al menos una familia: "
                  f"{', '.join(ap) or 'ninguna'}; con PIP>=0,5: {', '.join(pib_a) or 'ninguna'}. 'Relevante con seguridad' (criterio A y B): "
                  f"{', '.join(a_rel) or 'ninguna'}. Mejor modelo en la validacion espacial sellada: {ma.mejor_modelo} "
                  f"(RMSE {f4(ma.rmse_espacial)} log-puntos, {f4(ma.rmse_pct_espacial, 2)} % aprox.; persistencia {f4(ma.rmse_persistencia_espacial)})."),
        intervalo=f"RMSE espacial {f4(ma.rmse_espacial)}; cobertura empirica del intervalo al 95 %: {f4(ma.cobertura95_espacial, 2)}",
        cota="—", literatura="Saiz (2007) y Caldera y Johansson (2013): solo orientan el signo; cuartil no verificado en Saiz (2007).",
        veredicto="ANALIZADA, NO CONCLUYENTE",
        regla=("Con capa C4 el veredicto es como maximo ANALIZADA, NO CONCLUYENTE. Ninguna variable alcanza la significacion tras Holm en la "
               "especificacion pre-registrada; prediccion no es causalidad: las importancias y los ALE son descriptivos."),
        limites=LIM + " Solo 41 provincias de entrenamiento; regresores en t-1.", evidencia=ev))
    ficha.append(dict(
        id="M4-V2", tema="Diferencias entre provincias en la subida de la compra",
        enunciado="Que explica que unas provincias suban mas que otras en compra.", capa="C4",
        magnitud=(f"Compra, precio (valor tasado MIVAU, EUR/m2), provincias, datos hasta 2024-2025. Variables con apoyo en al menos una familia: "
                  f"{', '.join(cp) or 'ninguna'}; con PIP>=0,5: {', '.join(pip_c) or 'ninguna'}. 'Relevante con seguridad': "
                  f"{', '.join(c_rel) or 'ninguna'}. Mejor modelo en la validacion espacial sellada: {mc.mejor_modelo} "
                  f"(RMSE {f4(mc.rmse_espacial)} log-puntos; persistencia {f4(mc.rmse_persistencia_espacial)}; "
                  f"{'bate' if mc.bate_persistencia else 'no bate'} a la persistencia con Holm)."),
        intervalo=f"RMSE espacial {f4(mc.rmse_espacial)}; cobertura empirica al 95 %: {f4(mc.cobertura95_espacial, 2)}",
        cota="—", literatura="Sa (2015) y Cavalleri, Cournede y Ozsogut (2019, DOI 10.1787/4777e29a-en; documento de trabajo): solo orientan el signo.",
        veredicto="ANALIZADA, NO CONCLUYENTE",
        regla="Capa C4: ninguna hipotesis confirmatoria sobrevive a Holm; la persistencia es una referencia dificil de batir en compra.",
        limites=LIM + " La medida de precio es el valor tasado (Registradores como robustez).", evidencia=ev))
    comp = C
    ambos = comp[comp.lectura == "pesa en ambos"].variable.tolist()
    solo_a = comp[comp.lectura == "pesa en alquiler y no en compra"].variable.tolist()
    solo_c = comp[comp.lectura == "pesa en compra y no en alquiler"].variable.tolist()
    ficha.append(dict(
        id="M4-V3", tema="Factores comunes a alquiler y compra",
        enunciado="El alquiler y la compra se mueven por los mismos factores.", capa="C4",
        magnitud=(f"Variables comunes (6): pesan en ambos mercados {', '.join(ambos) or 'ninguna'}; solo en alquiler {', '.join(solo_a) or 'ninguna'}; "
                  f"solo en compra {', '.join(solo_c) or 'ninguna'} (criterio: apoyo en al menos una familia o PIP>=0,5). Alquiler (stock SERPAVI) "
                  f"y compra (valor tasado) se comparan por separado; no hay contratos nuevos en el contraste."),
        intervalo="Ver sintesis_variables.csv (PIP, IC de M1 y rango del multiverso por mercado)", cota="—",
        literatura="No aplica.", veredicto="ANALIZADA, NO CONCLUYENTE",
        regla="Una coincidencia parcial de variables con apoyo debil (C4) no permite afirmar ni negar que ambos mercados compartan factores.",
        limites=LIM + " Las dos medidas tienen distinta cobertura temporal y frecuencia.", evidencia=ev + ["output/v6/M4/comparacion_mercados.csv"]))
    ru = pd.read_csv(V6 / "M1B/tablas/ratio_ult.csv")
    gs = pd.read_csv(V6 / "M1B/tablas/gsadf.csv")
    n_ep = int((gs.p_BH < 0.05).sum())
    ficha.append(dict(
        id="M4-V4", tema="Ratio precio/alquiler y sobrevaloracion",
        enunciado="La ratio precio/alquiler indica sobrevaloracion.", capa="C4",
        magnitud=(f"Ratio precio/alquiler anual (valor tasado / SERPAVI), {len(ru)} provincias de entrenamiento, {int(ru.anio.iloc[0])}: mediana "
                  f"{f4(ru.ratio_anios.median(), 1)} anos de alquiler (rango {f4(ru.ratio_anios.min(), 1)}-{f4(ru.ratio_anios.max(), 1)}); rentabilidad bruta mediana "
                  f"{f4(ru.rent_yield_bruta_pct.median(), 2)} %. Contraste de burbuja GSADF por CCAA: {n_ep} de {len(gs)} con episodio explosivo "
                  f"(p BH<0,05). No existe un nivel de referencia identificado con el que la ratio senale sobrevaloracion."),
        intervalo="Brecha rentabilidad menos coste de uso (g=2 %): mediana "
                  f"{f4(ru.brecha_pp_g2.median(), 2)} pp, rango {f4(ru.brecha_pp_g2.min(), 2)} a {f4(ru.brecha_pp_g2.max(), 2)} pp",
        cota="—", literatura="No aplica.", veredicto="ANALIZADA, NO CONCLUYENTE",
        regla="La ratio es una descripcion (C4) sin umbral de equilibrio validado; el contraste GSADF tiene pocas provincias por CCAA.",
        limites=LIM + " Las provincias selladas no entran en la ratio; precio tasado frente a alquiler de stock (no contratos nuevos).",
        evidencia=["output/v6/M1B/tablas/ratio_ult.csv", "output/v6/M1B/tablas/gsadf.csv"]))
    return ficha


# ---------------------------------------------------------------- main
def md_tabla(df, cols, fmt=None):
    d = df[cols].copy()
    for c in d.columns:
        if d[c].dtype.kind == "f":
            d[c] = d[c].map(lambda x: "" if pd.isna(x) else f"{x:.4f}")
    h = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    return h + "\n".join("| " + " | ".join(str(x) for x in r) + " |" for r in d.itertuples(index=False)) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    modelos = carga()
    if not modelos:
        print("m4_run: sin sellado_*.json versionados")
        return 1
    T = tabla_modelos(modelos)
    T.to_csv(OUT / "tabla_modelos.csv", index=False, float_format="%.6g")
    M = mejores(T)
    M.to_csv(OUT / "mejor_modelo.csv", index=False, float_format="%.6g")
    PG = persistencia_por_grupo(T)
    PG.to_csv(OUT / "persistencia_por_grupo.csv", index=False, float_format="%.6g")
    S, C = sintesis(T)
    S.to_csv(OUT / "sintesis_variables.csv", index=False, float_format="%.6g")
    C.to_csv(OUT / "comparacion_mercados.csv", index=False, float_format="%.6g")
    F = fichas(T, M, S, C)
    (OUT / "fichas_verificador.json").write_text(json.dumps(F, ensure_ascii=False, indent=1))
    # registro de especificaciones evaluadas
    for r in T.itertuples():
        REG.log("OOS_SELLADA", f"{r.modelo_id}|{r.grupo}", f"{r.rol} {r.familia}; {r.nivel}; {r.medida}", "", "", int(r.n), np.nan, np.nan, np.nan,
                r.rmse_ln, getattr(r, "dm_vs_persistencia", np.nan), getattr(r, "p_holm_vs_persistencia", np.nan),
                f"medida_precio={r.medida_precio}; p_holm_vs_ar={getattr(r, 'p_holm_vs_ar_unidad', np.nan)}; cobertura95={r.cobertura95}")
    REG.flush()
    # md
    cm = ["tarea", "modelo_id", "rol", "n", "rmse_pct", "cobertura95", "sd_rmse_entre_periodos", "ratio_rmse_vs_persistencia",
          "p_holm_vs_persistencia", "p_holm_vs_ar_unidad", "p_holm_vs_ecm_v1"]
    cm = [c for c in cm if c in T.columns]
    md = ["# M4: modelos en la validacion sellada v6\n", f"Fecha: {FECHA}. {LIM}\n",
          "Error en log-puntos x100 (aprox. %). DM-HLN una cola a favor del modelo, perdida cuadratica, celdas (provincia, periodo); "
          "Holm dentro de cada tarea y grupo.\n", "## Mejor modelo por tarea (grupo espacial)\n",
          md_tabla(M, ["tarea", "mercado", "medida_precio", "nivel", "mejor_modelo", "rmse_pct_espacial", "rmse_persistencia_espacial",
                       "p_holm_vs_persistencia", "bate_persistencia", "lectura"]),
          "## Sintesis por variable\n",
          md_tabla(S, ["mercado", "variable", "signo_esperado", "direccion", "PIP", "F1_ok", "F2_ok", "F3_ok", "criterio_A", "criterio_B", "clasificacion"])]
    for g in ("espacial", "temporal"):
        md += [f"## Tabla de modelos, grupo {g}\n", md_tabla(T[T.grupo == g], cm)]
    (OUT / "tabla_modelos.md").write_text("\n".join(md))
    # resultado.json
    h = M[M.tarea == "alq_provincia"].iloc[0]
    n_rel = int(S.relevante_con_seguridad.sum())
    res = dict(
        rama="v6/M4", modulo="M4",
        pregunta="Que modelo predice mejor, en la validacion sellada, el alquiler de stock y la compra (precio y volumen), y que variables se sostienen en las tres familias?",
        mercado=["alquiler de stock (SERPAVI)", "compra (precio)", "compra (volumen)"], capa="C4",
        medida_precio={"principal": "valor tasado MIVAU (provincia, municipio)", "robustez": ["Registradores (provincia anual)"],
                       "no_usadas": "Notariado (solo Comunitat Valenciana), indice triangulado A23 e IPV INE (sin desagregacion provincial)"},
        datos="output/v6/M4/sellado_*.json (evaluacion unica por modelo con holdout.evaluate_v6) y resultados versionados de M1A, M1B, M2, M3A y M3B",
        N={"modelos_evaluados": len(modelos), "tareas": int(M.shape[0]),
           "filas_espaciales_prov_alquiler": int(h.n_espacial)},
        metodo=("Prediccion a un paso con modelos ya ajustados (sin reajustar con el sellado); RMSE, MAE, cobertura del intervalo; DM-HLN (una cola, "
                "celdas provincia-periodo) con Holm frente a persistencia, AR por unidad y ECM v1; mejor modelo por RMSE espacial y estabilidad, nunca por R2."),
        estimacion=M[["tarea", "mejor_modelo", "rmse_espacial", "rmse_persistencia_espacial", "bate_persistencia"]].to_dict("records"),
        ic95=None, p_ajustado="Holm dentro de cada tarea y grupo (tabla_modelos.csv)",
        nivel_evidencia="EXPLORATORIO (C4): prediccion, no causalidad; ninguna variable pasa de C4",
        diagnosticos={"variables_relevantes_con_seguridad": S[S.relevante_con_seguridad][["mercado", "variable"]].to_dict("records"),
                      "n_relevantes_con_seguridad": n_rel, "limitacion_validacion": LIM,
                      "persistencia_no_batida": PG[~PG.bate_persistencia][["tarea", "grupo"]].to_dict("records"),
                      "fallbacks": "unidades nuevas sin efecto fijo -> persistencia (columna n_fallback_persistencia)"},
        fuera_muestra={"modelo": h.mejor_modelo, "rmse": float(h.rmse_espacial),
                       "dm_vs_ar4": {"DM_HLN": None if pd.isna(h.dm_vs_ar) else float(h.dm_vs_ar), "p_holm": None if pd.isna(h.p_holm_vs_ar) else float(h.p_holm_vs_ar),
                                     "grupo": "espacial sellado (AR por unidad = persistencia en unidades nuevas)",
                                     "alquiler_provincia": True}},
        notas=("Capa C4. Alquiler (stock) y contratos nuevos van separados; contratos nuevos sin modelo. " + LIM + " Fecha de la evaluacion: " + FECHA))
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    # hechos.json
    hechos = []
    for r in M.itertuples():
        hechos.append(dict(id=f"V6-M4-RMSE-{r.tarea}", indicador=f"RMSE espacial sellado del mejor modelo ({r.mejor_modelo}), {r.mercado}, {r.nivel}, "
                           f"medida {r.medida}" + (f" ({r.medida_precio})" if r.medida_precio else ""),
                           valor=round(float(r.rmse_pct_espacial), 3), min=None, max=None, unidad="log-puntos x100 (aprox. %)",
                           periodo="validacion sellada v6 (11 provincias, 2016-2025)", cobertura=f"{int(r.n_espacial)} observaciones",
                           fuentes=["SERPAVI (MIVAU)" if r.mercado.startswith("alquiler") else "MIVAU valor tasado / INE ETDP / Registradores"],
                           capa="C4", fecha_dato=FECHA))
        hechos.append(dict(id=f"V6-M4-PERS-{r.tarea}", indicador=f"RMSE espacial sellado de la persistencia, {r.mercado}, {r.nivel}",
                           valor=round(100 * float(r.rmse_persistencia_espacial), 3), min=None, max=None, unidad="log-puntos x100 (aprox. %)",
                           periodo="validacion sellada v6 (11 provincias)", cobertura=f"{int(r.n_espacial)} observaciones",
                           fuentes=["output/v6/M4/mejor_modelo.csv"], capa="C4", fecha_dato=FECHA))
    hechos.append(dict(id="V6-M4-N-REL", indicador="Variables 'relevante con seguridad' (criterios A y B pre-registrados), alquiler y compra",
                       valor=n_rel, min=None, max=None, unidad="variables", periodo="entrenamiento 2015-2024 y sellado v6",
                       cobertura="3 mercados, 24 combinaciones variable-mercado", fuentes=["output/v6/M4/sintesis_variables.csv"],
                       capa="C4", fecha_dato=FECHA))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1, default=float))
    print(f"m4_run: {len(modelos)} modelos, {len(M)} tareas, {n_rel} variables relevantes con seguridad")
    return 0


if __name__ == "__main__":
    sys.exit(main())
