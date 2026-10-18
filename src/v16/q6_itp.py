"""V16 · fase 6 · Q6-v (log compraventas) y Q6-p (log valor tasado): tipo general del ITP, panel provincial anual 2011-2024 (adenda, punto 3).

Estimador principal: Wald-DID de de Chaisemartin-D'Haultfœuille con dosis continua y no absorbente: cambio del tipo general (puntos) de la CCAA
en el año de efecto frente a las provincias estables del mismo año; el año anterior a cada cambio queda fuera (anticipación, D2).
dCDH con aleatorización: NO APTO (tamaño 0,0775) → SOLO estimación puntual, sin p-valor ni IC. Honest DiD no validado: no se usa.
Capa C4; pendiente de evaluación sellada. Ejecución: python src/v16/q6_itp.py
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qb_comun as C  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = C.RAIZ / "output" / "v16" / "q6"
CCAA_OK = ["01", "06", "07", "08", "09", "10", "11", "12"]  # CCAA no selladas con tipo general autonómico variable en entrenamiento
REF = {"Q6-v": -0.07, "Q6-p": -0.01}


def tipos(desplazar: int = 0) -> pd.DataFrame:
    i = pd.read_csv(C.RAIZ / "output/v16/f1/intervenciones.csv", dtype={"cod_ine": str})
    i = i[(i.instrumento == "itp") & i.parametro.str.contains("tipo general ITP")].copy()
    i["v"] = pd.to_numeric(i.valor, errors="coerce")
    i["a"] = pd.to_datetime(i.fecha_efecto).dt.year + desplazar
    i = i.dropna(subset=["v"]).sort_values(["cod_ine", "fecha_efecto"])
    filas = []
    for c in CCAA_OK:
        s = i[i.cod_ine == c]
        for t in range(2009, 2025):
            prev = s[s.a <= t]
            filas.append((c, t, float(prev.v.iloc[-1]) if len(prev) else np.nan))
    return pd.DataFrame(filas, columns=["c", "t", "d"])


def panel(res_var: str, desplazar: int, ventana: tuple[int, int]) -> pd.DataFrame:
    if res_var == "Q6-v":
        y = np.log(C.anual(C.cargar("base_precio", "compraventas", "provincia").query("frecuencia == 'A'"), "y"))
    elif res_var == "Q6-p":
        y = np.log(C.anual(C.cargar("base_precio", "valor_tasado", "provincia").query("frecuencia == 'A'"), "y"))
    else:  # control negativo
        y = np.log(C.anual(C.cargar("base_poblacion", "pob_total", "provincia"), "y"))
    d = y.reset_index()
    d["c"] = d.u.map(C.PROV_CCAA)
    d = d[d.c.isin(CCAA_OK)].merge(tipos(desplazar), on=["c", "t"], how="left").sort_values(["u", "t"])
    d = d[(d.t >= ventana[0] - 1) & (d.t <= ventana[1])]
    d["dy"] = d.groupby("u").y.diff()
    d["dd"] = d.groupby("u").d.diff()
    d["dd_f"] = d.groupby("u").dd.shift(-1)  # cambio del año siguiente (anticipación)
    d["dy_l"] = d.groupby("u").dy.shift(1)  # ΔY retardado (placebo de pretendencia)
    return d[d.t >= ventana[0]].dropna(subset=["dy", "dd"])


def wald_did(d: pd.DataFrame, col: str = "dy", signo: int = 0) -> dict:
    """Σ_t Σ_{switchers}(ΔY - media ΔY de estables) / Σ Δtipo. signo = +1 solo subidas, -1 solo bajadas, 0 todos."""
    num = den = 0.0
    nsw = set()
    nt = 0
    for t, g in d.groupby("t"):
        sw = g[(g.dd != 0) & (g.dd_f.fillna(0) == 0)]
        if signo:
            sw = sw[np.sign(sw.dd) == signo]
        ct = g[(g.dd == 0) & (g.dd_f.fillna(0) == 0)].dropna(subset=[col])
        sw = sw.dropna(subset=[col])
        if len(sw) == 0 or len(ct) == 0:
            continue
        num += float((sw[col] - ct[col].mean()).sum())
        den += float(sw.dd.sum())
        nsw |= set(sw.u)
        nt += 1
    return {"beta": num / den if den != 0 else np.nan, "n_provincias_switchers": len(nsw), "n_años_con_contraste": nt}


def twfe(d: pd.DataFrame, res_var: str, desplazar: int, ventana) -> dict:
    full = panel(res_var, desplazar, ventana)
    base = full.copy()
    # nivel: necesita y y d en niveles
    y = {"Q6-v": ("compraventas", "base_precio"), "Q6-p": ("valor_tasado", "base_precio"), "NEG": ("pob_total", "base_poblacion")}[res_var if res_var != "NEG" else "NEG"]
    yy = np.log(C.anual(C.cargar(y[1], y[0], "provincia").query("frecuencia == 'A'"), "y")).reset_index()
    yy["c"] = yy.u.map(C.PROV_CCAA)
    yy = yy[yy.c.isin(CCAA_OK)].merge(tipos(desplazar), on=["c", "t"], how="left")
    yy = yy[(yy.t >= ventana[0]) & (yy.t <= ventana[1])].dropna(subset=["y", "d"])
    r = C.mco_fe(yy.y.values, yy[["d"]].values, [C.codif(yy.u), C.codif(yy.t)])
    return {"beta": float(r["beta"][0]), "n": r["n"], "r": r, "d": yy}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    reg = Registry(OUT / "registro.csv")
    res: dict = {"Q6-v": {"especificaciones": []}, "Q6-p": {"especificaciones": []}}
    # calendario de cambios (descriptivo)
    T = tipos(0)
    T["dd"] = T.groupby("c").d.diff()
    cal = T[(T.dd.fillna(0) != 0) & (T.t >= 2011)]
    res["calendario_cambios"] = cal.assign(cambio_puntos=cal.dd).drop(columns="dd").to_dict("records")
    for q in ["Q6-v", "Q6-p"]:
        for est, desp, vent in itertools.product(["dCDH", "TWFE"], [0, -1], [(2011, 2024), (2011, 2019)]):
            principal = (est, desp, vent) == ("dCDH", 0, (2011, 2024))
            if est == "dCDH":
                d = panel(q, desp, vent)
                w = wald_did(d)
                b, n = w["beta"], len(d)
                extra = {k: w[k] for k in ["n_provincias_switchers", "n_años_con_contraste"]}
            else:
                w = twfe(None, q, desp, vent)
                b, n, extra = w["beta"], w["n"], {}
            mid = f"{q}|{est}|fecha{'_efecto' if desp == 0 else '_adelantada1'}|{vent[0]}-{vent[1]}" + ("|PRINCIPAL" if principal else "")
            reg.log("v16-fase6", mid, "Δlog y ~ Δtipo (dCDH Wald-DID)" if est == "dCDH" else "log y ~ tipo + FE prov + FE año", vent[0], vent[1], n, np.nan, np.nan, np.nan, np.nan, b,
                    np.nan, "puntual; dCDH con aleatorización NO APTO")
            res[q]["especificaciones"].append({"id": mid, "estimador": est, "fecha": desp, "ventana": list(vent), "beta_por_punto": b, "n": n, "principal": principal, **extra})
    for q in ["Q6-v", "Q6-p"]:
        E = pd.DataFrame(res[q]["especificaciones"])
        pr = E[E.principal].iloc[0]
        d = panel(q, 0, (2011, 2024))
        up, dn = wald_did(d, signo=1), wald_did(d, signo=-1)
        pl = wald_did(d.assign(dy_pl=d.dy_l), col="dy_pl")
        neg = wald_did(panel("NEG", 0, (2011, 2024)))
        excl = wald_did(d[~d.u.isin(C.GRANDES_PROV)])
        tw = twfe(None, q, 0, (2011, 2024))
        dsd = float(d[d.dd != 0].dd.std())
        sdy = float(d.dy.std())
        ev = C.e_value_puntual(float(pr.beta_por_punto), dsd, sdy)
        rm = pd.Series(tw["r"]["resid"]).groupby(tw["d"].u.values).mean()
        cp = C.centroides_prov()
        rm = rm[rm.index.isin(cp.index)]
        dg = {"subidas": up, "bajadas": dn, "placebo_dy_retardado": pl, "control_negativo_log_poblacion": neg, "sin_grandes_ciudades": excl,
              "e_value_punto": ev, "cinelli_hazlett": "no calculado: requiere t con inferencia APTA (dCDH con aleatorización NO APTO)",
              "oster": "no aplica al Wald-DID; para la referencia TWFE ver ‘twfe_referencia’",
              "twfe_referencia": {"beta": tw["beta"], "n": tw["n"], "r2_total": tw["r"]["r2_total"], "r2_within": tw["r"]["r2_within"]},
              "het_autocorr_twfe": C.heterocedasticidad_autocorr(tw["r"]["resid"], tw["r"]["Xt"][:, 0], tw["d"].u.values, tw["d"].t.values),
              "moran_residuos_twfe_prov": C.moran(rm.values, cp.loc[rm.index].values),
              "honest_did": "no usado: no validado por Monte Carlo (veredictos.csv)", "islas": "ninguna no sellada",
              "magnitud_referencia": REF[q], "razon_estimacion_sobre_referencia": float(pr.beta_por_punto) / REF[q],
              "estables_vs_cambios": "ver calendario_cambios; sin errores S y M (sin SE válido)"}
        # dCDH con la fecha adelantada un año reproduce el placebo de pretendencia (el año previo al cambio queda fuera como anticipación):
        # no estima el efecto y sale del resumen del multiverso (sigue en el registro; corrección K17 tras la revisión adversarial).
        Em = E[~((E.estimador == "dCDH") & (E.fecha == -1))]
        mult = {"n": len(Em), "mediana": float(Em.beta_por_punto.median()), "min": float(Em.beta_por_punto.min()), "max": float(Em.beta_por_punto.max()),
                "proporcion_mismo_signo": float((np.sign(Em.beta_por_punto) == np.sign(pr.beta_por_punto)).mean()),
                "mediana_solo_dCDH": float(Em[Em.estimador == "dCDH"].beta_por_punto.median()),
                "excluidas": "dCDH con fecha adelantada un año (equivale al placebo)"}
        res[q].update({"principal": pr.to_dict(), "diagnosticos": dg, "multiverso": mult})
        reg.log("v16-fase6", f"{q}|excl_grandes", "dCDH sin 08/46/41/29", 2011, 2024, len(d), np.nan, np.nan, np.nan, np.nan, excl["beta"], np.nan, "diagnóstico")
        reg.log("v16-fase6", f"{q}|placebo_dy_retardado", "dCDH con ΔY(t-1)", 2011, 2024, len(d), np.nan, np.nan, np.nan, np.nan, pl["beta"], np.nan, "diagnóstico")
        reg.log("v16-fase6", f"{q}|control_negativo_poblacion", "dCDH con log población", 2011, 2024, len(d), np.nan, np.nan, np.nan, np.nan, neg["beta"], np.nan, "diagnóstico")
    C.volcar(OUT / "q6_resultado_parcial.json", res)
    reg.flush()
    for q in ["Q6-v", "Q6-p"]:
        print(q, res[q]["principal"], res[q]["multiverso"])
        print({k: v for k, v in res[q]["diagnosticos"].items() if k in ("subidas", "bajadas", "placebo_dy_retardado", "control_negativo_log_poblacion", "sin_grandes_ciudades", "twfe_referencia", "e_value_punto")})
    print(len(res["calendario_cambios"]))


if __name__ == "__main__":
    main()
