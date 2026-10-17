"""V16 · fase 6 · Q3-c1 (log valor tasado) y Q3-c2 (log compraventas): shift-share provincial en forma reducida (adenda, punto 3).

Especificación principal: log y_pt = β · x_pt + α_p + γ_t, ventana 2011-2022 (D2: el padrón por nacionalidad termina en 2022),
x = población extranjera predicha (puntos de la población de 2003; cuotas del padrón de 2003 × crecimiento nacional sin la provincia).
Inferencia: AKM y AKM0 NO APTOS (output/v16/montecarlo/veredictos.csv) → SOLO estimación puntual, sin p-valor ni IC.
Capa: C4 (asociación); pendiente de evaluación sellada. Ejecución: python src/v16/q3_shiftshare.py
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qb_comun as C  # noqa: E402
import qb_shiftshare as S  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = C.RAIZ / "output" / "v16" / "q3"
VENT = (2011, 2022)
REF_SAIZ = 0.01  # log por punto de población (elasticidad 1,0 de Saiz: 1 % de población inmigrante ~ 1 % de renta)


def panel_resultados() -> dict[str, pd.Series]:
    vt = C.anual(C.cargar("base_precio", "valor_tasado", "provincia").query("frecuencia == 'A'"), "y")
    cv = C.anual(C.cargar("base_precio", "compraventas", "provincia").query("frecuencia == 'A'"), "y")
    return {"Q3-c1": np.log(vt), "Q3-c2": np.log(cv)}


def exposicion(base: int, excl: list[str] | None, norm: str) -> tuple[pd.Series, dict]:
    s = S.shiftshare("provincia", base, excl)
    x = pd.DataFrame(s["x"], index=s["unidades"], columns=s["años"]).stack()
    x.index.names = ["u", "t"]
    if norm == "log1p":
        x = np.log1p(x / 100.0)
    return x.rename("x"), s


def rotemberg(s: dict, y_idx: pd.MultiIndex) -> pd.DataFrame:
    """Pesos de Rotemberg del shift-share (solo dependen de x): α_o = Σ c̃_o · B̃ / Σ B̃²; c̃ residualizado en FE de provincia y año."""
    ui = {u: i for i, u in enumerate(s["unidades"])}
    ti = {t: i for i, t in enumerate(s["años"])}
    u = np.array([ui[a] for a, _ in y_idx]); t = np.array([ti[b] for _, b in y_idx])
    gr = [C.codif([a for a, _ in y_idx]), C.codif([b for _, b in y_idx])]
    comp = s["comp"][u, t, :]
    ct = C._desmedia(np.nan_to_num(comp), gr)
    B = ct.sum(1)
    alfa = (ct * B[:, None]).sum(0) / (B ** 2).sum()
    return pd.DataFrame({"origen": s["origenes"], "alfa_rotemberg": alfa}).sort_values("alfa_rotemberg", key=np.abs, ascending=False)


def ajustar(y: pd.Series, x: pd.Series, efectos: str, controles: pd.DataFrame | None = None, excluir_prov: set | None = None,
            ventana=VENT) -> dict | None:
    d = pd.concat([y, x], axis=1, join="inner").dropna()
    if controles is not None:
        d = d.join(controles, how="inner")
    d = d.reset_index()
    d = d[(d.t >= ventana[0]) & (d.t <= ventana[1])]
    if excluir_prov:
        d = d[~d.u.isin(excluir_prov)]
    if len(d) < 30:
        return None
    g = [C.codif(d.u), C.codif(d.t)]
    cols = ["x"] + ([c for c in controles.columns] if controles is not None else [])
    X = d[cols].values.astype(float)
    if efectos == "año+CCAA×tendencia":
        cc = d.u.map(C.PROV_CCAA)
        tend = (d.t - ventana[0]).values[:, None] * pd.get_dummies(cc).astype(float).values
        X = np.column_stack([X, tend[:, 1:]])
    r = C.mco_fe(d.y.values, X, g)
    r["d"] = d
    r["b"] = float(r["beta"][0])
    return r


def main():
    reg = Registry(OUT / "registro_q3c.csv")
    OUT.mkdir(parents=True, exist_ok=True)
    ys = panel_resultados()
    x0, s0 = exposicion(2003, None, "pts")
    res: dict = {"especificaciones": [], "principal": {}, "diagnosticos": {}}
    idx_main = ys["Q3-c1"].index.intersection(x0.index)
    idx_main = idx_main[[(VENT[0] <= t <= VENT[1]) for _, t in idx_main]]
    rot = rotemberg(s0, idx_main)
    top5 = list(rot.origen.head(5))
    res["diagnosticos"]["rotemberg_top5"] = rot.head(5).to_dict("records")
    res["diagnosticos"]["rotemberg_suma_alfa"] = float(rot.alfa_rotemberg.sum())
    res["diagnosticos"]["rotemberg_suma_alfa_negativos"] = float(rot.alfa_rotemberg.clip(upper=0).sum())
    res["diagnosticos"]["top5_excluidos"] = top5
    rot.to_csv(OUT / "q3c_rotemberg.csv", index=False)

    cache_x = {}
    for base, orig, norm in itertools.product([2003, 2004], ["todos", "sin_top5"], ["pts", "log1p"]):
        cache_x[(base, orig, norm)] = exposicion(base, top5 if orig == "sin_top5" else None, norm)[0]

    for q, y in ys.items():
        for (base, orig, norm), efectos in itertools.product(itertools.product([2003, 2004], ["todos", "sin_top5"], ["pts", "log1p"]),
                                                              ["año", "año+CCAA×tendencia"]):
            r = ajustar(y.rename("y"), cache_x[(base, orig, norm)], efectos)
            if r is None:
                continue
            principal = (base, orig, norm, efectos) == (2003, "todos", "pts", "año")
            mid = f"{q}|base{base}|{orig}|{norm}|{efectos}" + ("|PRINCIPAL" if principal else "")
            reg.log("v16-fase6", mid, f"log y ~ x + FE ({efectos})", f"{VENT[0]}", f"{VENT[1]}", r["n"], r["r2_total"], np.nan, np.nan,
                    np.nan, r["b"], np.nan, "puntual; AKM/AKM0 NO APTOS; r2_adj = R2 total")
            res["especificaciones"].append({"id": mid, "pregunta": q, "base": base, "origenes": orig, "norm": norm, "efectos": efectos,
                                            "beta": r["b"], "beta_por_DT": r["b"] * float(r["sdx_t"][0]), "n": r["n"], "r2": r["r2_total"], "principal": principal})
            if principal:
                res["principal"][q] = {"beta_por_punto": r["b"], "n": r["n"], "n_provincias": int(r["d"].u.nunique()),
                                       "sd_x_dentro": float(r["sdx_t"][0]), "r2_total": r["r2_total"], "r2_within": r["r2_within"]}
                dg = {}
                # Oster / E-value
                d = r["d"]
                x0r = C.mco_fe(d.y.values, d[["x"]].values, [np.zeros(len(d), int)])
                dg["oster"] = {"beta_sin_efectos": float(x0r["beta"][0]), "r2_sin_efectos": x0r["r2_total"], "beta_con_efectos": r["b"],
                               "r2_con_efectos": r["r2_total"], "delta_beta0_rmax1_3": C.oster_delta(float(x0r["beta"][0]), x0r["r2_total"], r["b"], r["r2_total"]),
                               "fragil_delta_lt_1": bool(0 <= C.oster_delta(float(x0r["beta"][0]), x0r["r2_total"], r["b"], r["r2_total"]) < 1),
                               "nota": "δ < 0 = al añadir efectos fijos la estimación se aleja de 0: no es el caso de fragilidad; se publica el valor"}
                dg["e_value_punto"] = C.e_value_puntual(r["b"], float(r["sdx_t"][0]), r["sdy_t"])
                dg["cinelli_hazlett_RV"] = "no calculado: requiere t con inferencia APTA (AKM/AKM0 NO APTOS)"
                # residuos: heterocedasticidad, autocorrelación, Moran
                dg["het_autocorr"] = C.heterocedasticidad_autocorr(r["resid"], r["Xt"][:, 0], d.u.values, d.t.values)
                rm = pd.Series(r["resid"]).groupby(d.u.values).mean()
                cp = C.centroides_prov()
                rm = rm[rm.index.isin(cp.index)]
                dg["moran_residuos_prov"] = C.moran(rm.values, cp.loc[rm.index].values)
                # grandes ciudades
                r2 = ajustar(y.rename("y"), cache_x[(2003, "todos", "pts")], "año", excluir_prov=C.GRANDES_PROV)
                dg["sin_grandes_ciudades"] = {"beta": r2["b"], "n": r2["n"], "provincias_excluidas": sorted(C.GRANDES_PROV), "islas": "ninguna no sellada"}
                reg.log("v16-fase6", f"{q}|excl_grandes", "idem sin 08/46/41/29", VENT[0], VENT[1], r2["n"], r2["r2_total"], np.nan, np.nan, np.nan, r2["b"], np.nan, "diagnóstico")
                # Jaeger-Ruist-Stuhler: x retardado 4 años
                xl = cache_x[(2003, "todos", "pts")].groupby(level=0).shift(4).rename("xlag4")
                r3 = ajustar(y.rename("y"), cache_x[(2003, "todos", "pts")], "año", controles=xl.to_frame())
                dg["control_instrumento_retardado"] = {"beta_x": r3["b"], "beta_xlag4": float(r3["beta"][1]), "n": r3["n"]}
                reg.log("v16-fase6", f"{q}|JRS_lag4", "idem + x(t-4)", VENT[0], VENT[1], r3["n"], r3["r2_total"], np.nan, np.nan, np.nan, r3["b"], np.nan, "diagnóstico")
                # pretendencias: Δlog y previo sobre la exposición acumulada (corte transversal)
                pre = (2003, 2008) if q == "Q3-c1" else (2007, 2010)
                yy = y.unstack()
                dp = (yy[pre[1]] - yy[pre[0]]).dropna()
                xa = cache_x[(2003, "todos", "pts")].unstack()[2022].reindex(dp.index).dropna()
                dp = dp.reindex(xa.index)
                A = np.column_stack([np.ones(len(xa)), xa.values])
                bb, *_ = np.linalg.lstsq(A, dp.values, rcond=None)
                dg["pretendencia"] = {"periodo_previo": list(pre), "pendiente_dlogy_por_punto_exposicion_2022": float(bb[1]), "n": len(xa),
                                      "lectura": "pendiente puntual; sin p-valor (herramienta NO APTA); se compara con el efecto principal por punto"}
                reg.log("v16-fase6", f"{q}|pretendencia", "Δlog y previo ~ x2022", pre[0], pre[1], len(xa), np.nan, np.nan, np.nan, np.nan, float(bb[1]), np.nan, "diagnóstico")
                # primera etapa descriptiva: extranjeros observados (Extranjera/Total del padrón) en puntos de población de 2003
                ex = C.cargar("base_poblacion", "padron_pob_nacionalidad", "provincia", "nacionalidad=Extranjera")
                tot = C.cargar("base_poblacion", "padron_pob_nacionalidad", "provincia", "nacionalidad=Total")
                pb = C.anual(tot).xs(2003, level="t")
                obs = (100 * C.anual(ex) / pb.reindex(C.anual(ex).index.get_level_values("u")).values).rename("y")
                r4 = ajustar(obs, cache_x[(2003, "todos", "pts")], "año")
                dg["primera_etapa_descriptiva"] = {"coef": r4["b"], "r2_within": r4["r2_within"], "n": r4["n"],
                                                   "nota": "F efectivo de Montiel Olea-Pflueger: herramienta no validada (AKM NO APTO); en V9-D4 el F fue de 3,4 a 3,7"}
                # magnitud de referencia
                dg["magnitud_referencia"] = {"saiz_por_punto": REF_SAIZ if q == "Q3-c1" else None,
                                             "razon_estimacion_sobre_referencia": (r["b"] / REF_SAIZ if q == "Q3-c1" else None),
                                             "nota": "sin SE válido no se calculan errores S y M: (b) de la regla de hallazgo no se evalúa"}
                res["diagnosticos"][q] = dg
    E = pd.DataFrame(res["especificaciones"])
    resumen = {}
    for q, g in E.groupby("pregunta"):
        b0 = res["principal"][q]["beta_por_punto"]
        resumen[q] = {"n_especificaciones": len(g), "mediana_beta_por_DT": float(g.beta_por_DT.median()), "min_por_DT": float(g.beta_por_DT.min()), "max_por_DT": float(g.beta_por_DT.max()),
                      "mediana_beta_por_punto_solo_pts": float(g[g.norm == "pts"].beta.median()), "min_por_punto_solo_pts": float(g[g.norm == "pts"].beta.min()), "max_por_punto_solo_pts": float(g[g.norm == "pts"].beta.max()),
                      "proporcion_mismo_signo_que_principal": float((np.sign(g.beta_por_DT) == np.sign(b0)).mean()),
                      "nota": "sin IC válido: no se puede contar «IC que excluye el 0»"}
    res["multiverso"] = resumen
    (OUT / "q3c_resultado_parcial.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=C._j) + "\n", encoding="utf-8")
    reg.flush()
    print(json.dumps({"principal": res["principal"], "multiverso": resumen}, ensure_ascii=False, indent=1, default=C._j))


if __name__ == "__main__":
    main()
