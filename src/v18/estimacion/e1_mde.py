"""V18 · fase 4 · E1 · estimabilidad previa (adenda 1.3): mínimos de datos y efecto mínimo detectable (MDE) por Monte Carlo, ANTES de estimar ningún coeficiente.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. R = 2.000 réplicas, SEED = 20261010. El ruido se remuestrea del residuo del PERIODO PREVIO al tratamiento de
cada diseño («σ residual del resultado solo en el periodo previo», declarado como «ya visto» porque V15 y V16 no publican la σ residual de este resultado). La variación real del
tratamiento es la de cada diseño. El resultado observado del periodo de estimación no interviene: se sustituye por ceros en la parte que no necesita el MDE.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e1_estim as E  # noqa: E402
import e1_nucleo as N  # noqa: E402

R_MC = 2000


def _pool(Pref: pd.DataFrame, unidades_orden: list, anios_pre: list[int], cluster_col: str, extra_fun) -> N.PoolResiduos:
    """Residuos del periodo previo (unidad × año) reordenados a las unidades de la muestra de estimación; huecos a 0."""
    d = Pref[Pref.anio.isin(anios_pre)].dropna(subset=["y"]).copy()
    d = d[d.cod_seccion.isin(set(unidades_orden))]
    d = d.sort_values(["cod_seccion", "anio"]).reset_index(drop=True)
    R, unidades = N.residuos_previos_fe(d, "y", "cod_seccion", "anio", anios_pre, extra_fun)
    Rdf = pd.DataFrame(R, index=unidades).reindex(unidades_orden).fillna(0.0)
    cl = Pref.drop_duplicates("cod_seccion").set_index("cod_seccion")[cluster_col].reindex(unidades_orden).astype(str).values
    return N.PoolResiduos(Rdf.values, cl)


def _posiciones(d: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list]:
    """Posición de la unidad y del año (dentro de la ventana) de cada observación, en el orden de d."""
    unidades = d.drop_duplicates("u").sort_values("u").cod_seccion.tolist()
    return d.u.values.astype(int), d.t.values.astype(int), unidades


def estimabilidad_r1(P: pd.DataFrame) -> dict:
    d = E.muestra(P, E.VENTANA_R, ["y", "hut"])
    # mínimo de datos: barrios cuyo stock HUT cambia >= 10 % entre el primer (2018) y el último (2024) valor anual, con el primero como denominador
    s = P.drop_duplicates("cod_seccion").copy()
    st0 = (s.hut2018 * s.viv / 100.0).groupby(s.barrio).sum()
    st1 = (s.hut2024 * s.viv / 100.0).groupby(s.barrio).sum()
    cambia = ((st1 - st0).abs() / st0.replace(0, np.nan) >= 0.10)
    n_barrios = int(cambia.sum())
    M = K.Modelo(np.zeros(len(d)), d.hut.values, d.u.values, d.t.values, extra=E.extra_trend(d, "lineal"), cluster=d.cl.values)
    uo, to, unidades = _posiciones(d)
    pool = _pool(P, unidades, list(range(2011, 2018)), "barrio", lambda x: N.tendencias(x["barrio"], x["anio"]))
    m = N.mde_ols(M, pool, uo, to, T=len(E.VENTANA_R), R=R_MC)
    return {"id": "E1-R1", "n_unidades": int(d.u.nunique()), "n_obs": len(d), "G": M.G, "sd_intra_tratamiento": N.sd_intra(d, "hut", "u"), "minimo_datos": f"barrios con cambio >= 10 % del stock HUT 2018-2024: {n_barrios} (mínimo 20)",
            "cumple_minimo": n_barrios >= 20, "n_barrios_cambian": n_barrios, "umbral": E.REF["E1-R1"], "sigma_fuente": "ya vista: residuo de ln SERPAVI 2011-2017 tras efectos de sección y año y tendencias por barrio", **m}


def estimabilidad_iv(P: pd.DataFrame, ident: str) -> dict:
    """MDE del contraste AR de R2 (Barcelona, 2018-2024) o de A1 (cuatro ciudades, 2021-2024)."""
    if ident in ("E1-R2", "E1-R2-v5"):
        v5 = ident == "E1-R2-v5"          # suplementaria: solo MDE de la variante con INE-VUT como endógena (2022-2024); no se estima
        d = E.muestra(P, [2022, 2023, 2024] if v5 else E.VENTANA_R, ["y", "vut_pct" if v5 else "hut", "prox3", "trends", "dist_c"])
        d["z"] = E._z(d, "prox3", "trends")
        ex = N.interaccion_anio(d.dist_c.values, d.anio.values)
        x, pre_anios, T, cl_col = ("vut_pct" if v5 else "hut"), list(range(2011, 2018)), (3 if v5 else len(E.VENTANA_R)), "barrio"
        pre_fun = lambda z: N.interaccion_anio(z["dist_c"].values, z["anio"].values)  # noqa: E731
    else:
        d = E.muestra(P, E.VENTANA_A1, ["y", "vut_pct", "prox3", "noches", "dist_c"], cluster="cod_distrito")
        d["z"] = E._z(d, "prox3", "noches")
        ex = np.hstack([N.dummies(d.cod_mun.astype(str) + "_" + d.anio.astype(str)), N.interaccion_anio(d.dist_c.values, d.anio.values)])
        x, pre_anios, T, cl_col = "vut_pct", list(range(2011, 2021)), len(E.VENTANA_A1), "cod_distrito"
        pre_fun = lambda z: np.hstack([N.dummies(z["cod_mun"].astype(str) + "_" + z["anio"].astype(str)), N.interaccion_anio(z["dist_c"].values, z["anio"].values)])  # noqa: E731
    d0 = d.assign(y=0.0)       # el resultado observado no entra: solo importan la primera etapa y el instrumento
    res = N.iv_ajustar(d0, "y", x, "z", extra=ex)
    uo, to, unidades = _posiciones(d)
    Pref = P if ident.startswith("E1-R2") else P[P.cod_mun.isin(d.cod_mun.unique())].assign(barrio=lambda z: z["cod_distrito"])
    pool = _pool(Pref, unidades, pre_anios, cl_col if ident.startswith("E1-R2") else "barrio", pre_fun)
    m = N.mde_iv_ar(res, pool, uo, to, T=T, R=R_MC)
    return {"id": ident, "n_unidades": int(d.u.nunique()), "n_obs": len(d), "G": res["G"], "F_efectivo_primera_etapa": res["F_efectivo"], "pi_primera_etapa": res["pi"],
            "minimo_datos": "primera etapa y instrumento reales; F efectivo publicado (no es un criterio de estimabilidad)", "cumple_minimo": True, "umbral": E.REF["E1-R2" if ident.startswith("E1-R2") else ident],
            "sigma_fuente": f"ya vista: residuo de ln SERPAVI {pre_anios[0]}-{pre_anios[-1]} tras efectos de sección y año y los mismos controles", **m}


def estimabilidad_r3(P: pd.DataFrame) -> dict:
    d = E.muestra(P, E.ANIOS_R3, ["y", "dosis0"])
    sd = d.drop_duplicates("cod_seccion").dosis0.std(ddof=0)
    d["D"] = d.dosis0 / sd
    d["Dpost"] = d.D * (d.anio >= 2014).astype(float)
    lead = np.column_stack([(d.anio.values == k) * d.D.values for k in (2011, 2012)])
    M = K.Modelo(np.zeros(len(d)), d.Dpost.values, d.u.values, d.t.values, extra=lead, cluster=d.cl.values)
    uo, to, unidades = _posiciones(d)
    pool = _pool(P, unidades, [2011, 2012, 2013], "barrio", None)
    m = N.mde_ols(M, pool, uo, to, T=len(E.ANIOS_R3), R=R_MC)
    return {"id": "E1-R3", "n_unidades": int(d.u.nunique()), "n_obs": len(d), "G": M.G, "sd_intra_tratamiento": float(sd), "minimo_datos": "dosis de 2018T2 con variación entre secciones y barrios",
            "cumple_minimo": True, "umbral": E.REF["E1-R3"] * float(sd), "umbral_unidad": "por desviación típica de la dosis (referencia por pp × DT de la dosis en pp)", "sd_dosis_pp": float(sd),
            "sigma_fuente": "ya vista: residuo de ln SERPAVI 2011-2013 (3 años; ventana circular de 9 años) tras efectos de sección y año", **m}


def estimabilidad_r4(P: pd.DataFrame, g: pd.DataFrame) -> dict:
    cnt = E.r4_conteos(g)
    ok75 = bool(cnt["cuota_radio"] >= 0.75 and cnt["cuota_anillo"] >= 0.75)
    base = {"id": "E1-R4", "recuento_geometria": cnt, "minimo_datos": f"radio {cnt['radio_no_sellado']}/{cnt['radio_total']} y anillo {cnt['anillo_no_sellado']}/{cnt['anillo_total']} secciones no selladas (mínimo 75 % en cada uno)",
            "cumple_minimo": ok75, "umbral": 2 * E.DELTA["E1-R4"], "umbral_unidad": "2δ (sin referencia; δ = 0,05)"}
    if not ok75:
        return {**base, "mde80": np.nan, "G": 0, "n_unidades": 0}
    gg = g.set_index("cod_seccion")
    d = E.muestra(P, E.ANIOS_R3, ["y"])
    dist = d.cod_seccion.map(gg.dist_sf)
    d["tr"] = (dist < 0.5).astype(float)
    d["anillo"] = ((dist >= 0.5) & (dist < 1.0)).astype(float)
    d = d[(d.tr == 1) | (d.anillo == 1)].copy().sort_values(["cod_seccion", "anio"]).reset_index(drop=True)
    d["u"], d["t"], d["cl"] = pd.factorize(d.cod_seccion)[0], pd.factorize(d.anio)[0], pd.factorize(d.barrio)[0]
    d["Dpost"] = d.tr * (d.anio >= 2014).astype(float)
    lead = np.column_stack([(d.anio.values == k) * d.tr.values for k in (2011, 2012)])
    M = K.Modelo(np.zeros(len(d)), d.Dpost.values, d.u.values, d.t.values, extra=lead, cluster=d.cl.values)
    uo, to, unidades = _posiciones(d)
    pool = _pool(P, unidades, [2011, 2012, 2013], "barrio", None)
    m = N.mde_ols(M, pool, uo, to, T=len(E.ANIOS_R3), R=R_MC)
    m.update(N.tamano_webb(d, "Dpost", lead, pool, uo, to, T=len(E.ANIOS_R3)))
    return {**base, "n_unidades": int(d.u.nunique()), "n_obs": len(d), "G": M.G, "n_tratadas": int((d.drop_duplicates("u").tr == 1).sum()),
            "sigma_fuente": "ya vista: residuo de ln SERPAVI 2011-2013 (3 años; ventana circular) de las secciones del radio y del anillo", **m}
