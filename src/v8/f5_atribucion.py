#!/usr/bin/env python3
"""V8-F5: atribucion combinada y regla del «factor mas relevante» (hipotesis.md §9; R0-R8 de docs/v8/revision_F4.md §5).

NO estima modelos nuevos salvo la tabla comun fuera de muestra (J7/Y9). Lee las salidas versionadas de output/v8/M0-M9
(variante principal) y aplica la regla FIJADA en docs/v8/desviaciones.md, sin ajustarla al resultado.
Uso: python3 src/v8/f5_atribucion.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

warnings.filterwarnings("ignore")
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import Registry, dm_test, holm  # noqa: E402

SEED = 20261010
OUT = RAIZ / "output" / "v8"
SCRIPT = "src/v8/f5_atribucion.py"
PERS = ["P1", "P2", "P3", "P4", "P5"]
MERC = ["compra", "alquiler"]
FACTORES7 = ["demografia", "empleo_renta", "credito_tipos", "oferta", "demanda_externa", "turismo", "factor_europeo"]
NO_COMPITEN = {"determinista", "no_identificados", "residuo", "factor_comun"}
UMBRAL_MULTIVERSO = 0.80
IMPRECISOS = {("compra", "P4"), ("alquiler", "P4"), ("alquiler", "P1")}
ROTULO_R1 = "la mayor parte de la variacion no se atribuye a los shocks identificados"
AVISO_CAPA = ("svar_hd: C3s, condicionado a los supuestos de signo y de cero de M2 (V3: solo impacto; magnitudes posiblemente atenuadas, Y6). "
              "El resto de metodos son C4 (asociacion): sin lectura causal.")


def leer(mod: str, f: str, base: Path | None = None) -> pd.DataFrame:
    return pd.read_csv((base or OUT) / mod / f)


def ppr(x, n=1):
    return "n.d." if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{n}f}"


# ------------------------------------------------------------------------------------------------ entradas
def entradas(base: Path | None = None) -> dict:
    E = {}
    a2 = leer("M2", "atribucion.csv", base)
    E["m2"] = a2[a2["principal"] == "si"].copy()
    pm = leer("M2", "prob_mayor.csv", base)
    E["pm"] = pm[pm["principal"] == "si"].copy()
    E["dom_voto"] = leer("M6", "voto_dominancia.csv", base)
    a6 = leer("M6", "atribucion.csv", base)
    E["m6"] = a6[(a6["principal"] == "si") & (a6["metodo"] == "dominancia")].copy()
    E["m5"] = leer("M5", "atribucion.csv", base)
    E["m4_voto"] = leer("M4", "voto_contabilidad.csv", base)
    a4 = leer("M4", "atribucion.csv", base)
    E["m4"] = a4[a4["principal"] == "si"].copy()
    E["m7"] = leer("M7", "resumen_multiverso.csv", base)
    E["m7_fall"] = leer("M7", "fallidas.csv", base)
    E["m1"] = leer("M1", "atribucion.csv", base)
    a8 = leer("M8", "atribucion.csv", base)
    E["m8"] = a8[a8["principal"] == "si"].copy()
    a9 = leer("M9", "atribucion.csv", base)
    E["m9"] = a9[a9["principal"] == "si"].copy()
    E["shap_rank"] = leer("M9", "ranking_shap.csv", base)
    return E


def dy_ref(E: dict) -> dict:
    """DeltaY (pp, R0) por (mercado, periodo): la de M2 si existe; si no, la de M6."""
    d = {}
    for r in E["dom_voto"].itertuples():
        d[(r.mercado, r.periodo)] = float(r.delta_y_pp)
    for (m, p), g in E["pm"].groupby(["mercado", "periodo"]):
        d[(m, p)] = float(g["delta_y_obs_pp"].iloc[0])
    return d


# ------------------------------------------------------------------------------------------------ votos
def cand_svar(E: dict, m: str, p: str) -> dict | None:
    g = E["pm"][(E["pm"]["mercado"] == m) & (E["pm"]["periodo"] == p)]
    if g.empty:
        return None
    g = g.sort_values("factor").reset_index(drop=True)
    i_med, i_p = int(g["media_c_signo"].values.argmax()), int(g["prob_mayor"].values.argmax())
    nota = []
    if g["factor"].iloc[i_med] != g["factor"].iloc[i_p]:
        nota.append("ranking incierto (media y P(f*) discrepan)")   # Y10
    if float(g["prob_mayor"].iloc[i_p]) < 0.5:
        nota.append("ranking incierto (P(f*) < 0,5)")             # R2
    return dict(voto=g["factor"].iloc[i_p], p_fstar=float(g["prob_mayor"].iloc[i_p]), factor_media=g["factor"].iloc[i_med],
                media_cs=float(g["media_c_signo"].iloc[i_p]), nota="; ".join(nota), tabla=g)


def voto_dom(E: dict, m: str, p: str):
    g = E["dom_voto"][(E["dom_voto"]["mercado"] == m) & (E["dom_voto"]["periodo"] == p)]
    if g.empty:
        return None, "sin fila"
    f = g["factor_votado"].iloc[0]
    return (None, str(g["nota"].iloc[0])) if f == "abstiene" else (f, "")


def voto_lpiv(E: dict, m: str, p: str, sg: float, svar: dict | None):
    g = E["m5"][(E["m5"]["mercado"] == m) & (E["m5"]["ambito"] == "nacional") & (E["m5"]["periodo"] == p) & (E["m5"]["principal"] == "si")]
    if g.empty:
        return None, "sin fila de lpiv"
    g = g[g["vota_s9"] == "si"]
    if g.empty:
        return None, "F < 10 y AR 68 % no acotado: se abstiene"
    g = g.assign(cs=g["contribucion_pp"] * sg).sort_values("cs", ascending=False)
    top = g.iloc[0]
    if svar is None:
        return None, "sin svar_hd con el que comparar: se abstiene"
    maxsv = float(svar["tabla"]["media_c_signo"].max())
    if float(top["cs"]) > maxsv:
        return top["factor"], ""
    return None, f"c·sign(dY) de lpiv ({top['cs']:.1f} pp) no supera la mayor de svar_hd ({maxsv:.1f} pp): se abstiene"


def voto_contab(E: dict, m: str, p: str):
    g = E["m4_voto"][(E["m4_voto"]["mercado"] == m) & (E["m4_voto"]["periodo"] == p)]
    if g.empty:
        return None, "sin fila"
    return ("demografia", "") if str(g["vota_demografia"].iloc[0]) == "si" else (None, "brecha sin el signo de dY o por debajo del 0,5 % del stock")


# ------------------------------------------------------------------------------------------------ multiverso (condicion 2)
def cond2(E: dict, m: str, p: str, f: str) -> dict:
    t = E["m7"]
    fam = t[(t["mercado"] == m) & (t["periodo"] == p) & (t["factor"] == f) & (t["variable"] == "TODAS")]
    out = dict(pct_familia=np.nan, pct_variable=np.nan, pct_familia_fall=np.nan, pct_variable_fall=np.nan, variable_principal="", ok=False,
               nota="", signo_familia="", signo_variable="")
    if fam.empty:
        out["nota"] = "factor sin multiverso en esta celda"
        return out
    fam = fam.iloc[0]
    vp = str(fam["variable_principal"])
    var = t[(t["mercado"] == m) & (t["periodo"] == p) & (t["factor"] == f) & (t["variable"] == vp)]
    fl = E["m7_fall"]
    fl = fl[(fl["mercado"] == m) & (fl["periodo"] == p) & (fl["factor"] == f)]
    nf_fam, nf_var = len(fl), int((fl["variable"] == vp).sum())
    out["variable_principal"] = vp
    out["pct_familia"] = float(fam["pct_mismo_signo"])
    out["signo_familia"] = str(fam["signo_mayoritario"])
    out["pct_familia_fall"] = float(fam["pct_mismo_signo"] * fam["n_multiverso"] / (fam["n_multiverso"] + nf_fam))
    if not var.empty:
        v = var.iloc[0]
        out["pct_variable"] = float(v["pct_mismo_signo"])
        out["signo_variable"] = str(v["signo_mayoritario"])
        out["pct_variable_fall"] = float(v["pct_mismo_signo"] * v["n_multiverso"] / (v["n_multiverso"] + nf_var))
    out["ok"] = bool(out["pct_familia"] >= UMBRAL_MULTIVERSO and out["pct_variable"] >= UMBRAL_MULTIVERSO)
    out["nota"] = f"fallidas: {nf_fam} en la familia, {nf_var} en la variable principal"
    return out


# ------------------------------------------------------------------------------------------------ R1: cuota no atribuida
def cuota_no_atribuida(E: dict, m: str, p: str, dy: float, primero_cs: float | None) -> dict:
    g = E["m2"][(E["m2"]["mercado"] == m) & (E["m2"]["periodo"] == p) & (E["m2"]["ambito"] == "nacional")
                & E["m2"]["factor"].isin(["determinista", "no_identificados"])]
    if len(g) < 2 or not np.isfinite(dy) or dy == 0:
        return dict(pp=np.nan, cuota=np.nan, b68_lo=np.nan, b68_hi=np.nan, cuota_lo=np.nan, cuota_hi=np.nan, rotulo="", nota="sin svar_hd")
    sg = np.sign(dy)
    pp = float(g["media"].sum())
    lo, hi = float(g["b68_lo"].sum()), float(g["b68_hi"].sum())          # banda aproximada (suma de limites)
    cs = pp * sg
    lo_s, hi_s = (lo * sg, hi * sg) if sg > 0 else (hi * sg, lo * sg)
    excluye0 = (lo_s > 0) or (hi_s < 0)
    rot = ROTULO_R1 if (excluye0 and primero_cs is not None and cs > primero_cs) else ""
    q = sorted([lo / dy, hi / dy])
    return dict(pp=pp, cuota=pp / dy, b68_lo=lo, b68_hi=hi, cuota_lo=q[0], cuota_hi=q[1], rotulo=rot,
                nota="banda aproximada (suma de limites de determinista y no_identificados; sorteos no versionados)"
                + ("; cuota inestable: |dY| < 3 pp" if abs(dy) < 3 else ""))


# ------------------------------------------------------------------------------------------------ regla s9
def regla_s9(E: dict, reg: Registry) -> pd.DataFrame:
    dyr = dy_ref(E)
    filas = []
    for m in MERC:
        for p in PERS:
            dy = dyr.get((m, p), np.nan)
            sg = float(np.sign(dy)) if np.isfinite(dy) else 0.0
            sv = cand_svar(E, m, p)
            vd, nd = voto_dom(E, m, p)
            vl, nl = voto_lpiv(E, m, p, sg, sv)
            vc, nc = voto_contab(E, m, p)
            votos = {"svar_hd": sv["voto"] if sv else None, "dominancia": vd, "lpiv": vl, "contabilidad": vc}
            cuenta: dict[str, int] = {}
            for v in votos.values():
                if v:
                    cuenta[v] = cuenta.get(v, 0) + 1
            # factor evaluado: el de mas votos; empate -> voto de svar_hd, luego dominancia
            orden = sorted(cuenta, key=lambda f: (-cuenta[f], f != votos["svar_hd"], f != votos["dominancia"], f))
            fmax = orden[0] if orden else ""
            nmax = cuenta.get(fmax, 0)
            c1 = nmax >= 3
            c2 = cond2(E, m, p, fmax) if fmax else dict(pct_familia=np.nan, pct_variable=np.nan, pct_familia_fall=np.nan,
                                                         pct_variable_fall=np.nan, variable_principal="", ok=False, nota="",
                                                         signo_familia="", signo_variable="")
            g2 = E["m2"][(E["m2"]["mercado"] == m) & (E["m2"]["periodo"] == p) & (E["m2"]["factor"] == fmax)]
            if g2.empty or not fmax:
                c3, lo, hi = False, np.nan, np.nan
            else:
                lo, hi = float(g2["b68_lo"].iloc[0]), float(g2["b68_hi"].iloc[0])
                c3 = bool(lo > 0 or hi < 0)
            r7 = (m, p) in IMPRECISOS
            en7 = fmax in FACTORES7
            primero_cs = float(sv["tabla"]["media_c_signo"].max()) if sv else None
            cq = cuota_no_atribuida(E, m, p, dy, primero_cs)
            motivos = []
            if not c1:
                motivos.append(f"condicion 1 no se cumple: maximo {nmax} de 4 votos" + (f" ({fmax})" if fmax else "")
                               + "; lpiv " + ("abstiene" if not vl else "vota") + f" ({nl or 'ok'})")
            if c1 and not en7:
                motivos.append(f"{fmax} no es uno de los 7 factores pre-registrados")
            if not c2["ok"]:
                motivos.append(f"condicion 2 no se cumple (multiverso orientado: familia {ppr(100 * c2['pct_familia'], 0)} %, "
                               f"variable principal {ppr(100 * c2['pct_variable'], 0)} %; umbral 80 %)" if fmax else "condicion 2 sin candidato")
            if not c3:
                motivos.append("condicion 3 no se cumple: la banda del 68 % de svar_hd incluye el 0" if sv else
                               "condicion 3 no evaluable: no hay svar_hd en esta celda")
            if r7:
                motivos.append("R7: periodo impreciso (P4 de 9 trimestres / alquiler P1 sin svar_hd)")
            designado = bool(c1 and en7 and c2["ok"] and c3 and not r7)
            res = fmax if designado else "no designado"
            if designado:
                motivos = ["cumple las tres condiciones (C3s condicionada a los supuestos de signos de M2)"]
            filas.append(dict(
                mercado=m, ambito="nacional", periodo=p, delta_y_pp=dy, ventana_R0=("2022T3-2026T1" if p == "P5" else "ventana de cada metodo (P1: desde su 1.er trimestre)"),
                voto_svar_hd=votos["svar_hd"] or "abstiene", p_fstar=sv["p_fstar"] if sv else np.nan, factor_mayor_media_svar=sv["factor_media"] if sv else "",
                nota_svar=sv["nota"] if sv else "sin svar_hd (M2 no cubre esta celda)",
                voto_dominancia=vd or "abstiene", motivo_dominancia=nd, voto_lpiv=vl or "abstiene", motivo_lpiv=nl,
                voto_contabilidad=vc or "abstiene", motivo_contabilidad=nc,
                votos_por_factor="; ".join(f"{f}:{cuenta[f]}" for f in orden) or "ninguno", factor_evaluado=fmax, n_votos=nmax,
                cond1=c1, variable_principal_m7=c2["variable_principal"], pct_multiverso_familia=c2["pct_familia"],
                pct_multiverso_variable=c2["pct_variable"], pct_multiverso_familia_con_fallidas=c2["pct_familia_fall"],
                pct_multiverso_variable_con_fallidas=c2["pct_variable_fall"], cond2=c2["ok"], nota_cond2=c2["nota"],
                signo_mayoritario_familia=c2["signo_familia"], signo_mayoritario_variable=c2["signo_variable"],
                b68_lo_svar=lo, b68_hi_svar=hi, cond3=c3, R7_impreciso=r7,
                Y10_ranking_incierto=bool(sv and sv["nota"]), resultado=res, motivo="; ".join(motivos),
                capa=("C3s (condicionada)" if designado else "C4 (ranking; sin designacion)"),
                cuota_no_atribuida_pp=cq["pp"], cuota_no_atribuida=cq["cuota"], cuota_b68_lo_pp=cq["b68_lo"], cuota_b68_hi_pp=cq["b68_hi"],
                cuota_b68_lo=cq["cuota_lo"], cuota_b68_hi=cq["cuota_hi"], rotulo_R1=cq["rotulo"], nota_cuota=cq["nota"]))
            reg.log("F5", f"f5_regla_s9_{m}_{p}", f"regla §9 (R0-R8): {m} {p}; evaluado={fmax or '-'}; resultado={res}", p, p, 1, np.nan, np.nan, np.nan,
                    notas=f"votos={dict((k, v) for k, v in votos.items())}; cond1={c1} cond2={c2['ok']} cond3={c3} R7={r7}")
    return pd.DataFrame(filas)


# ------------------------------------------------------------------------------------------------ atribucion combinada
COLS_COMB = ["mercado", "ambito", "periodo", "factor", "metodo", "contribucion_pp", "media", "mediana", "pct_signo", "b68_lo", "b68_hi",
             "b90_lo", "b90_hi", "capa", "compite", "vota", "variante", "delta_y_metodo_pp", "notas"]


def combinada(E: dict, R: pd.DataFrame) -> pd.DataFrame:
    dyr = dy_ref(E)
    votos = {(r.mercado, r.periodo): dict(svar_hd=r.voto_svar_hd, dominancia=r.voto_dominancia, lpiv=r.voto_lpiv, contabilidad=r.voto_contabilidad)
             for r in R.itertuples()}
    filas = []

    def fila(r, metodo, media=np.nan, mediana=np.nan, s=np.nan, dy_m=np.nan, nota=""):
        compite = r["factor"] not in NO_COMPITEN
        v = "no_compite" if not compite else "no_vota"
        k = (r["mercado"], r["periodo"])
        if compite and r["ambito"] == "nacional" and metodo in ("svar_hd", "dominancia", "lpiv", "contabilidad_lp", "contabilidad") and k in votos:
            mm = "contabilidad" if metodo.startswith("contabilidad") else metodo
            vm = votos[k][mm]
            if mm == "contabilidad" and metodo == "contabilidad_lp":
                v = "no_vota (DOLS sin cointegracion demostrada, J10)"
            elif mm == "contabilidad" and r["factor"] != "demografia":
                v = "no_vota"
            else:
                v = "abstiene" if vm == "abstiene" else ("si" if vm == r["factor"] else "no")
        filas.append(dict(mercado=r["mercado"], ambito=r["ambito"], periodo=r["periodo"], factor=r["factor"], metodo=metodo,
                          contribucion_pp=r["contribucion_pp"], media=media, mediana=mediana, pct_signo=s,
                          b68_lo=r.get("b68_lo", np.nan), b68_hi=r.get("b68_hi", np.nan), b90_lo=r.get("b90_lo", np.nan), b90_hi=r.get("b90_hi", np.nan),
                          capa=("C3s" if metodo == "svar_hd" else r.get("capa", "C4")), compite=("si" if compite else "no"), vota=v,
                          variante=r.get("variante", ""), delta_y_metodo_pp=dy_m, notas=nota))

    for _, r in E["m2"].iterrows():
        dy = dyr.get((r["mercado"], r["periodo"]), np.nan)
        fila(r, "svar_hd", r["media"], r["mediana"], r["contribucion_pp"] / dy if np.isfinite(dy) and dy else np.nan, dy,
             "media posterior (aditiva); R0; C3s condicionada a los supuestos")
    for _, r in E["m6"].iterrows():
        fila(r, "dominancia", s=r["pct_total"] / 100 if np.isfinite(r["pct_total"]) else np.nan, dy_m=r["delta_y_pp"],
             nota="cuota LMG x R2 x dY (asociacion; no causal)")
    for _, r in E["m5"].iterrows():
        dy = dyr.get((r["mercado"], r["periodo"]), np.nan)
        fila(r, "lpiv", s=r["pct_total"] / 100, nota=f"vota_s9={r.get('vota_s9')}; {str(r.get('motivo_vota_s9', ''))[:120]}")
    for _, r in E["m4"].iterrows():
        fila(r, r["metodo"], s=r["pct_total"] / 100, nota="DOLS sin escalones; sin cointegracion demostrada" if r["metodo"] == "contabilidad_lp" else "")
    for _, r in E["m1"].iterrows():
        fila(r, "factor_comun_m1", s=r["pct_total"] / 100, nota="contraste (R6): parte europea; no vota")
    for _, r in E["m8"].iterrows():
        fila(r, r["metodo"], s=r["pct_total"] / 100 if np.isfinite(r["pct_total"]) else np.nan, nota="contraste regional (R6); no vota")
    for _, r in E["m9"].iterrows():
        dy = dyr.get((r["mercado"], r["periodo"]), np.nan) if r["ambito"] == "nacional" else np.nan
        s = r["contribucion_pp"] / dy if np.isfinite(dy) and dy else np.nan
        fila(r, "shap", s=s, dy_m=dy, nota="contraste (R6): media interanual x T/4; nunca causal; s_f respecto a dY de M2/M6")
    return pd.DataFrame(filas)[COLS_COMB]


# ------------------------------------------------------------------------------------------------ ranking
def parse_rank_dom(s: str) -> dict:
    out = {}
    for i, mt in enumerate(re.finditer(r"(\w+)\(([\d.]+);([+-])\)", s), start=1):
        out[mt.group(1)] = (i, float(mt.group(2)), mt.group(3))
    return out


def ranking(E: dict) -> pd.DataFrame:
    filas = []
    dyr = dy_ref(E)
    for m in MERC:
        for p in PERS:
            dy = dyr.get((m, p), np.nan)
            sg = float(np.sign(dy)) if np.isfinite(dy) else 1.0
            sv = cand_svar(E, m, p)
            dv = E["dom_voto"][(E["dom_voto"]["mercado"] == m) & (E["dom_voto"]["periodo"] == p)]
            dom = parse_rank_dom(str(dv["ranking_cuota"].iloc[0])) if len(dv) else {}
            sh = E["shap_rank"][(E["shap_rank"]["mercado"] == m) & (E["shap_rank"]["ambito"] == "nacional") & (E["shap_rank"]["periodo"] == p)]
            shd = {r.factor: (r.rango_mediano, r.prob_primero) for r in sh.itertuples()}
            facs = list(dict.fromkeys(([] if sv is None else list(sv["tabla"]["factor"])) + list(dom) + list(shd)))
            m2 = E["m2"][(E["m2"]["mercado"] == m) & (E["m2"]["periodo"] == p) & (E["m2"]["ambito"] == "nacional")].set_index("factor")
            tab = None if sv is None else sv["tabla"].set_index("factor")
            rk_m = (sv["tabla"].sort_values("media_c_signo", ascending=False)["factor"].tolist() if sv else [])
            rk_p = (sv["tabla"].sort_values("prob_mayor", ascending=False)["factor"].tolist() if sv else [])
            for f in facs:
                row = dict(mercado=m, periodo=p, factor=f, delta_y_pp=dy, impreciso=((m, p) in IMPRECISOS))
                if tab is not None and f in tab.index and f in m2.index:
                    mm = m2.loc[f]
                    lo, hi, lo9, hi9 = mm["b68_lo"], mm["b68_hi"], mm["b90_lo"], mm["b90_hi"]
                    row.update(rank_svar_media=rk_m.index(f) + 1, media_c_signo_pp=float(tab.loc[f, "media_c_signo"]),
                               b68_lo=(lo if sg >= 0 else -hi), b68_hi=(hi if sg >= 0 else -lo),
                               b90_lo=(lo9 if sg >= 0 else -hi9), b90_hi=(hi9 if sg >= 0 else -lo9),
                               prob_mayor=float(tab.loc[f, "prob_mayor"]), rank_svar_prob=rk_p.index(f) + 1)
                if f in dom:
                    row.update(rango_dominancia=dom[f][0], cuota_lmg=dom[f][1], signo_parcial_dominancia=dom[f][2])
                if f in shd:
                    row.update(rango_shap=shd[f][0], prob_primero_shap=shd[f][1])
                row["nota"] = ("svar_hd: C3s condicionada a los supuestos; dominancia y SHAP: contraste C4, nunca causal. "
                               + (sv["nota"] if sv and sv["nota"] else "") + (" Sin svar_hd en esta celda: solo contraste." if sv is None else ""))
                filas.append(row)
    cols = ["mercado", "periodo", "factor", "delta_y_pp", "rank_svar_media", "media_c_signo_pp", "b68_lo", "b68_hi", "b90_lo", "b90_hi",
            "prob_mayor", "rank_svar_prob", "rango_dominancia", "cuota_lmg", "signo_parcial_dominancia", "rango_shap", "prob_primero_shap",
            "impreciso", "nota"]
    return pd.DataFrame(filas).reindex(columns=cols)


# ------------------------------------------------------------------------------------------------ regional
def regional(E: dict) -> pd.DataFrame:
    a = E["m8"]
    filas = []
    for (m, amb, per), g in a.groupby(["mercado", "ambito", "periodo"]):
        imp = g[(g["contribucion_pp"].abs() > 1e-9) & g["pct_total"].notna() & (g["pct_total"].abs() > 1e-9)]
        dy = float(np.median(imp["contribucion_pp"] / imp["pct_total"] * 100)) if len(imp) else np.nan
        sg = np.sign(dy) if np.isfinite(dy) else 1.0
        comp = g[(~g["factor"].isin(NO_COMPITEN)) & (g["metodo"] == "regional_panel")]
        rk = comp.assign(cs=comp["contribucion_pp"] * sg).sort_values("cs", ascending=False)["factor"].tolist()
        for _, r in g.iterrows():
            filas.append(dict(mercado=m, ambito=amb, periodo=per, factor=r["factor"], metodo=r["metodo"], variante=r["variante"],
                              contribucion_pp=r["contribucion_pp"], pct_total=r["pct_total"], b68_lo=r["b68_lo"], b68_hi=r["b68_hi"],
                              delta_y_implicita_pp=dy, rank_c_signo=(rk.index(r["factor"]) + 1 if r["factor"] in rk else np.nan),
                              compite=("si" if r["factor"] not in NO_COMPITEN else "no"),
                              designacion="no designado (contraste C4: no hay svar_hd regional)",
                              nota=("CCAA: ranking por c_f·sign(dY) del panel FE (M8); " if amb.startswith("ccaa:") else
                                    "CV/Valencia: solo factor comun frente a residuo (M8), sin ranking de factores; ")
                              + "asociacion, sin lectura causal; el factor comun es un resumen de comovimiento (pendiente ~1 mecanica, J23)"))
    return pd.DataFrame(filas)


# ------------------------------------------------------------------------------------------------ J7: tabla comun fuera de muestra
def carga_r5():
    spec = importlib.util.spec_from_file_location("r5_prediccion", RAIZ / "src" / "v7" / "r5_prediccion.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _ols(Z, y):
    return np.linalg.lstsq(Z, y, rcond=None)[0]


def fuera_muestra_comun(reg: Registry, rapido: bool = False) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    from sklearn.model_selection import TimeSeriesSplit

    import m2_svar as M2
    from herramientas import bvar

    r5 = carga_r5()
    d = M2.cargar()
    S = M2.series_base(d)
    qs_v7, _, data7 = r5.carga_panel()
    INI = "2007Q1"
    q = [t for t in S.index if INI <= t <= "2026Q1"]
    nsp = 3 if rapido else 5
    folds = list(TimeSeriesSplit(n_splits=nsp, test_size=8, gap=4).split(np.arange(len(q))))
    ld = np.log(d["ipc_general"])
    niv = {"compra": (np.log(d["p_tasado"]) - ld), "alquiler": (np.log(d["ipc_alquiler"]) - ld)}
    col = {"compra": "p", "alquiler": "r"}
    spec = M2.construir("V3", d)
    Yb, Xb = spec["Y"], spec["X"]
    P: dict = {}
    nota_modelo: dict = {}
    for m in MERC:
        y = S[col[m]]
        idx = {t: i for i, t in enumerate(S.index)}
        Xn = data7[m][1].mean(0)                     # medias de las 17 CCAA (como m_ecm_v1)
        y1 = np.array([niv[m].get(t, np.nan) for t in qs_v7], float)[None, :]
        X1 = Xn[None, :, :]
        rows = []
        for tr, te in folds:
            ini_te, fin_tr = q[te[0]], q[tr[-1]]
            tr_q = [t for t in q if t <= fin_tr]
            te_q = [q[i] for i in te]
            # AR(4) y AR + factor comun (dos retardos del HPI zona euro)
            for nom, extra in (("ar4", 0), ("ar_fc", 2)):
                def Z(ts, extra=extra):
                    cols = [np.ones(len(ts))] + [np.array([y.iloc[idx[t] - k] for t in ts]) for k in range(1, 5)]
                    cols += [np.array([S["dhpi"].iloc[idx[t] - k] for t in ts]) for k in range(1, extra + 1)]
                    return np.column_stack(cols)
                b = _ols(Z(tr_q), np.array([y.iloc[idx[t]] for t in tr_q]))
                pr = Z(te_q) @ b
                rows += [(m, nom, t, float(y.iloc[idx[t]]), float(p_)) for t, p_ in zip(te_q, pr)]
            # ECM v1 (especificacion A de v7: m_ecm_v1 + _ec_forecast importadas)
            try:
                e = qs_v7.index(fin_tr)
                _, info = r5.m_ecm_v1(y1[:, :e + 1], X1[:, :e + 1], 1)
                coef, th = np.array(info["coef[phi,const,gamma_X..,rho]"]), np.array(info["theta"])
                for t in te_q:
                    j = qs_v7.index(t)
                    nxt = r5._ec_forecast(coef, y1[0, j - 1], y1[0, j - 1] - y1[0, j - 2], Xn[j - 1], th, 1)[0]
                    rows.append((m, "ecm_v1", t, float(y.iloc[idx[t]]), float(100 * (nxt - y1[0, j - 1]))))
            except Exception as ex:   # no evaluable
                nota_modelo[(m, "ecm_v1")] = f"no evaluable: {type(ex).__name__}: {ex}"
            # BVAR de M2 (forma reducida, V3)
            try:
                ini_b = Yb.index.get_loc(INI) - spec["p"]
                fin_b = Yb.index.get_loc(fin_tr)
                post = bvar.estimar(Yb.values[ini_b:fin_b + 1], spec["p"], lam=None, delta=spec["delta"], exog=Xb.values[ini_b:fin_b + 1])
                yy, Xl = bvar.retardos(Yb.values, spec["p"], True, Xb.values)
                pred_all = Xl @ post["B"]
                vi = spec["vars"].index(col[m])
                for t in te_q:
                    rows.append((m, "bvar_m2", t, float(y.iloc[idx[t]]), float(pred_all[Yb.index.get_loc(t) - spec["p"], vi])))
            except Exception as ex:
                nota_modelo[(m, "bvar_m2")] = f"no evaluable: {type(ex).__name__}: {ex}"
        P[m] = pd.DataFrame(rows, columns=["mercado", "modelo", "trimestre", "obs", "pred"])
    PR = pd.concat(P.values(), ignore_index=True)
    PR["e"] = PR["obs"] - PR["pred"]
    # metricas
    bases = ["ar4", "ecm_v1", "ar_fc"]
    filas = []
    for m in MERC:
        g = PR[PR["mercado"] == m]
        rm = {k: float(np.sqrt((v["e"] ** 2).mean())) for k, v in g.groupby("modelo")}
        exig = min([b for b in bases if b in rm], key=lambda b: rm[b])
        ntr = g["trimestre"].nunique()
        pend = []
        for mod in rm:
            e_m = g[g["modelo"] == mod].set_index("trimestre")["e"]
            for ref, etq in (("ar4", "ar4"), (exig, "exigente")):
                if mod == ref or (etq == "exigente" and exig == "ar4"):
                    continue   # si AR(4) es la base mas exigente, ambas comparaciones coinciden: una sola prueba en Holm
                e_r = g[g["modelo"] == ref].set_index("trimestre")["e"]
                ix = e_m.index.intersection(e_r.index)
                r1 = dm_test(e_m.loc[ix].values, e_r.loc[ix].values, h=1)
                r4 = dm_test(e_m.loc[ix].values, e_r.loc[ix].values, h=4)
                pend.append(dict(mercado=m, modelo=mod, comparador=etq, ref=ref, dm_hln=r1["DM"], p=r1["p"], dm_hln_h4=r4["DM"], p_h4=r4["p"],
                                 n=r1["n"]))
        PD = pd.DataFrame(pend)
        if len(PD):
            hh = holm({f"{r.modelo}|{r.comparador}": r.p for r in PD.itertuples()})
            PD["p_holm"] = [hh[f"{r.modelo}|{r.comparador}"] for r in PD.itertuples()]
            hh4 = holm({f"{r.modelo}|{r.comparador}": r.p_h4 for r in PD.itertuples()})
            PD["p_holm_h4"] = [hh4[f"{r.modelo}|{r.comparador}"] for r in PD.itertuples()]
        for mod in ("ar4", "ecm_v1", "ar_fc", "bvar_m2"):
            f = dict(mercado=m, modelo=mod, tipo=("base" if mod in bases else "candidato"))
            if mod in rm:
                f.update(rmse_pp=rm[mod], n_test=int((g["modelo"] == mod).sum()), n_trimestres=ntr, base_mas_exigente=exig,
                         evaluable="si", nota=("; ".join(["pronostico a 1 paso, parametros hasta el inicio del bloque menos 4 trimestres"])))
                for etq in ("ar4", "exigente"):
                    et_ = "ar4" if (etq == "exigente" and exig == "ar4") else etq
                    s = PD[(PD["modelo"] == mod) & (PD["comparador"] == et_)] if len(PD) else PD
                    if len(s):
                        s = s.iloc[0]
                        f.update({f"dm_hln_vs_{etq}": s["dm_hln"], f"p_vs_{etq}": s["p"], f"p_holm_vs_{etq}": s["p_holm"],
                                  f"p_holm_h4_vs_{etq}": s["p_holm_h4"]})
                f["mejor_que_exigente"] = bool(mod not in bases and rm[mod] < rm[exig] and f.get("p_holm_vs_exigente", 1) < 0.05
                                              and f.get("dm_hln_vs_exigente", 1) < 0)
            else:
                f.update(evaluable="no evaluable", nota=nota_modelo.get((m, mod), "sin predicciones"))
            filas.append(f)
            reg.log("F5", f"f5_oos_{m}_{mod}", f"{col[m]} (crec. trim. real log x100) ~ {mod}; bloques 5x8, embargo 4; prueba 2016T2-2026T1",
                    q[folds[0][1][0]], q[-1], int((g["modelo"] == mod).sum()), np.nan, np.nan, np.nan, rmse_oos=f.get("rmse_pp", np.nan),
                    notas=f.get("nota", "") + ("; C4 (prediccion no es causalidad)" if mod == "bvar_m2" else ""))
    T = pd.DataFrame(filas)
    meta = dict(n_pliegues=len(folds), prueba=f"{q[folds[0][1][0]]}-{q[-1]}", entrenamiento_desde=INI)
    return T, PR, meta


# ------------------------------------------------------------------------------------------------ fichas
def fichas(R: pd.DataFrame) -> str:
    L = ["# Fichas F5: factor mas relevante por mercado y periodo (ambito nacional)", "", AVISO_CAPA, "",
         "Regla fijada ANTES de calcular (docs/v8/desviaciones.md, R0-R8): 3 de 4 votos + multiverso orientado >= 80 % (familia y variable principal) + banda 68 % de svar_hd sin el 0; "
         "P4 y alquiler P1 no se designan. Una abstencion cuenta como «no apoya».", ""]
    for r in R.itertuples():
        L += [f"## {r.mercado.capitalize()} {r.periodo}", ""]
        L.append(f"- dY observada (R0): {ppr(r.delta_y_pp)} pp ({r.ventana_R0}).")
        L.append(f"- Votos: svar_hd = {r.voto_svar_hd}" + (f" (P(f*) = {r.p_fstar:.2f})" if np.isfinite(r.p_fstar) else "")
                 + f"; dominancia = {r.voto_dominancia}; lpiv = {r.voto_lpiv}; contabilidad = {r.voto_contabilidad}.")
        L.append(f"- Recuento: {r.votos_por_factor}. Factor evaluado: {r.factor_evaluado or '-'} ({r.n_votos} de 4).")
        if r.nota_svar:
            L.append(f"- Aviso svar_hd: {r.nota_svar}.")
        L.append(f"- Multiverso orientado ({r.variable_principal_m7 or '-'}): familia {ppr(100 * r.pct_multiverso_familia, 0)} % "
                 f"({ppr(100 * r.pct_multiverso_familia_con_fallidas, 0)} % con fallidas); variable principal {ppr(100 * r.pct_multiverso_variable, 0)} % "
                 f"({ppr(100 * r.pct_multiverso_variable_con_fallidas, 0)} % con fallidas). "
                 f"Signo mayoritario (orientado): familia {r.signo_mayoritario_familia or '-'}; variable principal {r.signo_mayoritario_variable or '-'}.")
        L.append(f"- Banda 68 % de svar_hd del factor evaluado: [{ppr(r.b68_lo_svar)}; {ppr(r.b68_hi_svar)}] pp.")
        if np.isfinite(r.cuota_no_atribuida):
            L.append(f"- Cuota no atribuida (determinista + no identificados): {ppr(r.cuota_no_atribuida_pp)} pp = {ppr(100 * r.cuota_no_atribuida, 0)} % de dY "
                     f"(banda 68 % aproximada {ppr(100 * r.cuota_b68_lo, 0)} % a {ppr(100 * r.cuota_b68_hi, 0)} %)." + (f" Rotulo R1: {r.rotulo_R1}." if r.rotulo_R1 else ""))
        L.append(f"- Resultado: **{r.resultado}**. {r.motivo}.")
        if r.resultado == "no designado":
            L.append(f"- Conclusion: no se designa un factor mas relevante en {r.mercado} {r.periodo}; se publica el ranking con incertidumbre (ranking.csv), "
                     "sin lectura causal salvo la condicionada de svar_hd (C3s).")
        else:
            L.append(f"- Conclusion: en {r.mercado} {r.periodo}, bajo los supuestos de signos de M2 (C3s), {r.resultado} es el factor con mayor contribucion.")
        L.append("")
    return "\n".join(L)


# ------------------------------------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=str(OUT / "F5"))
    a = ap.parse_args(argv)
    sal = Path(a.salida)
    sal.mkdir(parents=True, exist_ok=True)
    np.random.seed(SEED)
    t0 = time.time()
    tiempos = {}
    reg = Registry(sal / "registro.csv")
    E = entradas()
    R = regla_s9(E, reg)
    tiempos["regla_s9_s"] = round(time.time() - t0, 2)
    C = combinada(E, R)
    K = ranking(E)
    G = regional(E)
    for nom, df in (("atribucion_combinada", C), ("regla_s9", R), ("ranking", K), ("regional_ranking", G)):
        df.to_csv(sal / f"{nom}.csv", index=False, float_format="%.6g")
    (sal / "fichas.md").write_text(fichas(R))
    t1 = time.time()
    T, PR, meta = fuera_muestra_comun(reg, a.rapido)
    tiempos["fuera_muestra_comun_s"] = round(time.time() - t1, 2)
    T.to_csv(sal / "fuera_muestra_comun.csv", index=False, float_format="%.6g")
    PR.to_csv(sal / "fuera_muestra_comun_predicciones.csv", index=False, float_format="%.6g")
    reg.flush()
    des = R[R["resultado"] != "no designado"]
    est = {f"{r.mercado}_{r.periodo}": r.resultado for r in R.itertuples()}
    fm = {}
    for m in MERC:
        s = T[(T["mercado"] == m) & (T["modelo"] == "bvar_m2")]
        if len(s) and s["evaluable"].iloc[0] == "si":
            s = s.iloc[0]
            fm[m] = dict(modelo="BVAR M2 (forma reducida)", rmse=round(float(s["rmse_pp"]), 4),
                         dm_vs_ar4=dict(DM=round(float(s["dm_hln_vs_ar4"]), 3), p_holm=round(float(s["p_holm_vs_ar4"]), 4)),
                         base_mas_exigente=str(s["base_mas_exigente"]))
    res = dict(
        rama="F5",
        pregunta="Cual es el factor mas relevante en la subida del precio de compra y del alquiler por periodo, segun la regla de §9, o por que no se puede designar?",
        capa="C3s condicionada a supuestos para svar_hd (M2); C4 para el resto",
        datos="output/v8/M0-M9 (variante principal, solo lectura); data/processed/v8/nacional_q_v8.csv y panel v7 para la tabla comun J7",
        N=dict(celdas_regla=int(len(R)), filas_combinada=int(len(C)), filas_regional=int(len(G)), test_oos=meta),
        metodo="regla R0-R8 fijada en desviaciones.md; votos svar_hd/dominancia/lpiv/contabilidad; multiverso orientado M7; banda 68 % svar_hd; cuota no atribuida (R1); "
               "tabla comun fuera de muestra (5 bloques x 8, embargo 4) con AR(4), ECM v1 (v7 espec. A), BVAR M2, AR+factor comun; DM-HLN y Holm",
        estimacion=dict(designaciones=est, n_designados=int(len(des))),
        ic95=None, p_ajustado=None,
        nivel_evidencia="C3s condicionada a supuestos (svar_hd); C4 para el resto: sin lenguaje causal fuera de C3s",
        diagnosticos=dict(imprecisos=sorted(f"{m}_{p}" for m, p in IMPRECISOS), umbral_multiverso=UMBRAL_MULTIVERSO,
                          periodo_completo="no evaluado (M2 no lo cubre)", seed=SEED),
        fuera_muestra=fm,
        notas=["Los tiempos de ejecucion estan en tiempos.json.",
               "demanda_vivienda (demanda especifica de M2) compite en svar_hd pero no es un factor pre-registrado.",
               "Regional: sin designacion (no hay svar_hd regional); ranking C4 de M8."])
    (sal / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    tiempos["total_s"] = round(time.time() - t0, 2)
    (sal / "tiempos.json").write_text(json.dumps(tiempos, indent=1))
    # resumen
    L = ["# F5: atribucion y «factor mas relevante»", "", AVISO_CAPA, "",
         "## Designaciones (regla §9 fijada)", "", "| Mercado | Periodo | Votos (svar_hd/dom/lpiv/contab) | Evaluado | Cond.1 | Cond.2 | Cond.3 | Resultado |", "|---|---|---|---|---|---|---|---|"]
    for r in R.itertuples():
        L.append(f"| {r.mercado} | {r.periodo} | {r.voto_svar_hd}/{r.voto_dominancia}/{r.voto_lpiv}/{r.voto_contabilidad} | {r.factor_evaluado or '-'} ({r.n_votos}) | "
                 f"{'si' if r.cond1 else 'no'} | {'si' if r.cond2 else 'no'} | {'si' if r.cond3 else 'no'} | {r.resultado} |")
    L += ["", f"Designados: {len(des)} de {len(R)} celdas.", "",
          "## Tabla comun fuera de muestra (J7; RMSE en pp de crecimiento trimestral real; prueba 2016T2-2026T1)", "",
          T[["mercado", "modelo", "rmse_pp", "evaluable", "p_holm_vs_ar4", "p_holm_vs_exigente", "mejor_que_exigente"]].round(4).to_markdown(index=False), "",
          "Ver regla_s9.csv, ranking.csv, regional_ranking.csv, atribucion_combinada.csv y fichas.md."]
    (sal / "resumen.md").write_text("\n".join(L))
    return R, T


if __name__ == "__main__":
    main()
