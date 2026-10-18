"""V15-A · H3 (P5): vivienda turística (INE) y alquiler SERPAVI por sección, 2021-2024. SOLO entrenamiento.

Asociación pre-registrada (capa máxima C4). Especificación: preregistro_v15 §3 H3 + adendas + DV15-A (A5).
Ejecución: python3 src/v15/p5_turismo.py   (SEED 20261010). No usa SERPAVI 2025 ni nada sellado.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pa_comun import OUT, PROC, SEED, centroides_municipio, registrar, volcar, xyz_km  # noqa: E402
import pa_panel as PN  # noqa: E402
from econ_utils import Registry  # noqa: E402

SALIDA = OUT / "p5"
ANIOS = [2021, 2022, 2023, 2024]
GRANDES = {"08019", "46250"}  # Madrid, Illes Balears y Canarias ya están fuera (sellado v6)
VARS = {"pct": "ine_vut_porcentaje_vivienda_turistica", "n": "ine_vut_vivienda_turistica", "plazas": "ine_vut_plazas"}


def centroides_secciones(codigos) -> pd.DataFrame:
    import shapely
    g = pd.read_parquet(RAIZ_GEO, columns=["cod_seccion", "geometry"])
    g = g[g.cod_seccion.isin(set(codigos))]
    c = shapely.centroid(shapely.from_wkb(g.geometry.values))
    return pd.DataFrame({"sec": g.cod_seccion.values, "lon": shapely.get_x(c), "lat": shapely.get_y(c)})


RAIZ_GEO = Path(__file__).resolve().parents[2] / "data/base/geo/secciones.parquet"


def cargar():
    d = pd.read_parquet(PROC / "p5_turismo_seccion.parquet")
    s = d[d.nivel == "seccion"]
    ine = s[s.variable.isin(VARS.values())].copy()
    ine["anio"] = ine.periodo.str[:4].astype(int)
    # código presente en las ediciones INE de 2021 y de 2024
    pres = ine.groupby("territorio_codigo").anio.agg(lambda a: {2021, 2024} <= set(a))
    codigos_ok = set(pres[pres].index)
    anual = ine.groupby(["territorio_codigo", "anio", "variable"]).valor.mean().unstack("variable").reset_index()
    anual = anual.rename(columns={v: k for k, v in VARS.items()}).rename(columns={"territorio_codigo": "sec"})
    # saltos de factor > 10 en el porcentaje entre ediciones consecutivas con valores positivos
    p = ine[ine.variable == VARS["pct"]].sort_values(["territorio_codigo", "periodo"])
    lg = np.log(p.valor.where(p.valor > 0))
    p = p.assign(lg=lg)
    p["dl"] = p.groupby("territorio_codigo").lg.diff().abs()
    salto = p.groupby("territorio_codigo").dl.max() > np.log(10)
    salto = salto.fillna(False)
    ren = s[(s.variable == "serpavi_alquiler_m2_mediana")].copy()
    ren["anio"] = ren.periodo.astype(int)
    ren = ren[ren.anio.isin(ANIOS)]
    ren["tip"] = ren.desagregacion.str[-2:]
    r = ren.pivot_table(index=["territorio_codigo", "anio"], columns="tip", values="valor", aggfunc="first").reset_index().rename(columns={"territorio_codigo": "sec", "VC": "y_VC", "VU": "y_VU"})
    P = r.merge(anual, on=["sec", "anio"], how="inner")
    P = P[P.sec.isin(codigos_ok)]
    P["salto"] = P.sec.map(salto).fillna(False).astype(bool)
    P["mun"] = P.sec.str[:5]
    P["gran"] = P.mun.isin(GRANDES)
    # IPVA por distrito
    dist = d[d.nivel == "distrito"]
    ip = dist[dist.variable == "ipva_indice"].assign(anio=lambda x: x.periodo.astype(int))[["territorio_codigo", "anio", "valor"]].rename(columns={"territorio_codigo": "dis", "valor": "ipva"})
    dd = dist[dist.variable.isin(VARS.values())].copy()
    dd["anio"] = dd.periodo.str[:4].astype(int)
    da = dd.groupby(["territorio_codigo", "anio", "variable"]).valor.mean().unstack("variable").reset_index().rename(columns={v: k for k, v in VARS.items()}).rename(columns={"territorio_codigo": "dis"})
    IP = ip.merge(da, on=["dis", "anio"], how="inner")
    IP = IP[IP.anio.isin(ANIOS)]
    IP["mun"] = IP.dis.str[:5]
    return P, IP, len(codigos_ok)


def preparar_muestra(P, resultado, expo, sin_saltos=False, sin_grandes=False, lead=False):
    """Devuelve DataFrame de la muestra de una especificación (con exposición estandarizada por DT intra-sección)."""
    cols = [f"y_{resultado}", expo]
    df = P.copy()
    if lead:
        nxt = P[["sec", "anio", expo]].copy()
        nxt["anio"] -= 1
        df = df.merge(nxt.rename(columns={expo: expo + "_lead"}), on=["sec", "anio"], how="inner")
        cols.append(expo + "_lead")
    df = df.dropna(subset=cols)
    df = df[df[f"y_{resultado}"] > 0]
    if sin_saltos:
        df = df[~df.salto]
    if sin_grandes:
        df = df[~df.gran]
    n = df.groupby("sec").anio.transform("size")
    df = df[n >= 2].copy()
    # DT intra-sección (de la exposición de t) en esta muestra
    xd = df[expo] - df.groupby("sec")[expo].transform("mean")
    sd = float(np.sqrt((xd ** 2).mean()))
    df["z"] = df[expo] / sd
    if lead:
        df["z_lead"] = df[expo + "_lead"] / sd
    df["ly"] = np.log(df[f"y_{resultado}"])
    return df.reset_index(drop=True), sd


def estimar(df, tfe, K_full, sec_index, mod="z", con_lead=False):
    sec = pd.factorize(df.sec)[0]
    mun = pd.factorize(df.mun)[0]
    if tfe == "anio":
        grp = pd.factorize(df.anio)[0]
    else:
        grp = pd.factorize(df.mun + "_" + df.anio.astype(str))[0]
    X = df[["z", "z_lead"]].values if con_lead else df[["z"]].values
    # índice de sección dentro de la matriz K local
    secs = df.sec.values
    uniq = pd.unique(secs)
    loc = pd.Series(np.arange(len(uniq)), index=uniq)
    so = loc.loc[secs].values
    K = K_full[sec_index.loc[uniq].values][:, sec_index.loc[uniq].values] if K_full is not None else None
    r = PN.ols_fe(df.ly.values, X, sec, grp, mun, so, K)
    r["n_sec"] = int(len(uniq))
    r["n_mun"] = int(mun.max() + 1)
    r["sec_unicos"] = uniq
    r["so"] = so
    return r


def p_norm(b, se):
    from scipy.stats import norm
    if se is None or not np.isfinite(se) or se <= 0:
        return np.nan
    return float(2 * (1 - norm.cdf(abs(b / se))))


def main():
    t0 = time.time()
    SALIDA.mkdir(parents=True, exist_ok=True)
    reg = Registry(SALIDA / "registro.csv")
    P, IP, n_codigos_ok = cargar()
    # centroides y matriz de Conley sobre todas las secciones de la muestra máxima
    todas = pd.unique(P.sec)
    cs = centroides_secciones(todas).drop_duplicates("sec").set_index("sec").reindex(todas)
    ok_geo = cs.lon.notna().values
    xyz = xyz_km(cs.lon.fillna(0).values, cs.lat.fillna(0).values)
    falt = np.where(~ok_geo)[0]
    xyz[falt] = np.column_stack([20000.0 + 50.0 * np.arange(len(falt)), np.zeros(len(falt)), np.zeros(len(falt))])  # sin centroide: lejos de todo
    K_full = PN.matriz_conley(xyz, 2.0)
    sec_index = pd.Series(np.arange(len(todas)), index=todas)
    res = {"n_secciones_codigo_estable": n_codigos_ok, "n_secciones_panel": int(len(todas)), "sin_centroide": int((~ok_geo).sum())}

    multiverso = []
    for resultado in ("VC", "VU"):
        for expo in ("pct", "n", "plazas"):
            for tfe in ("anio", "mun_anio"):
                for sin_saltos in (False, True):
                    df, sd = preparar_muestra(P, resultado, expo, sin_saltos=sin_saltos)
                    if len(df) < 50:
                        continue
                    r = estimar(df, tfe, K_full, sec_index)
                    b, se_m, se_c = float(r["b"][0]), float(r["se_mun"][0]), float(r["se_conley"][0])
                    for agr, se in (("municipio", se_m), ("conley2km", se_c)):
                        multiverso.append({"resultado": resultado, "exposicion": expo, "fe_temporal": tfe, "muestra": "sin_saltos" if sin_saltos else "todas", "agrupacion": agr,
                                           "beta_log_por_DT": b, "pct_por_DT": 100 * b, "se": se, "p_normal_descriptivo": p_norm(b, se), "n_obs": r["n"], "n_secciones": r["n_sec"], "n_municipios": r["n_mun"], "dt_intra": sd,
                                           "principal": bool(resultado == "VC" and expo == "pct" and tfe == "mun_anio" and not sin_saltos and agr == "municipio")})
                        registrar(reg, "V15-A", f"H3-{resultado}-{expo}-{tfe}-{'ss' if sin_saltos else 'todas'}-{agr}", f"log(SERPAVI {resultado}) ~ z({expo}) + FE sección + FE {tfe}", "2021", "2024", r["n"], coef=b, p=p_norm(b, se),
                                  notas=f"p normal descriptivo; {'Conley 2 km NO APTO tras K16 (referencia)' if agr == 'conley2km' else 'agrupado municipio: sin validación MC en panel (descriptivo)'}")
    res["multiverso"] = multiverso

    # --------- principal ---------
    df, sd = preparar_muestra(P, "VC", "pct")
    pr = estimar(df, "mun_anio", K_full, sec_index)
    b = float(pr["b"][0])
    n_obs, n_sec, n_mun = pr["n"], pr["n_sec"], pr["n_mun"]
    dof = n_obs - pr["n_fe"] - 1
    t_c = b / float(pr["se_conley"][0])
    f = abs(t_c) / np.sqrt(dof)
    rv = 0.5 * (np.sqrt(f ** 4 + 4 * f ** 2) - f ** 2)
    # Oster: corto = año; largo = municipio x año
    cort = estimar(df, "anio", K_full, sec_index)
    r2_c = 1 - cort["ssr"] / cort["tss"]
    r2_l = 1 - pr["ssr"] / pr["tss"]
    bc, bl = float(cort["b"][0]), b
    rmax = min(1.0, 1.3 * r2_l)
    den = (bc - bl) * (rmax - r2_l)
    delta = bl * (r2_l - r2_c) / den if abs(den) > 1e-12 else np.nan
    # Moran de residuos: por año (la media por sección es 0 por construcción con efectos fijos de sección)
    sec_ord = pr["sec_unicos"]
    ii = sec_index.loc[sec_ord].values
    morans = []
    for a in ANIOS:
        m = (df.anio.values == a)
        loc_idx = pr["so"][m]
        rr = pr["resid"][m]
        g = ok_geo[ii[loc_idx]]
        if g.sum() > 50:
            morans.append(PN.moran_I(rr[g], xyz[ii[loc_idx]][g], 2.0))
    I = float(np.mean(morans))
    res["principal"] = {"beta_log_por_DT": b, "pct_por_DT": 100 * b, "se_municipio": float(pr["se_mun"][0]), "se_conley2km": float(pr["se_conley"][0]), "p_conley_normal": p_norm(b, float(pr["se_conley"][0])),
                        "p_municipio_normal_descriptivo": p_norm(b, float(pr["se_mun"][0])), "n_obs": n_obs, "n_secciones": n_sec, "n_municipios": n_mun, "dt_intra_seccion_pct": sd, "conley_var_no_positiva": pr["conley_var_no_positiva"],
                        "MDE80_conley_pct_por_DT": 100 * 2.8 * float(pr["se_conley"][0]), "MDE80_municipio_pct_por_DT": 100 * 2.8 * float(pr["se_mun"][0]),
                        "cinelli_hazlett_RV_q1": float(rv), "oster_delta": float(delta) if np.isfinite(delta) else None, "oster_R2_corto": r2_c, "oster_R2_largo": r2_l, "oster_beta_corto": bc, "oster_Rmax": rmax,
                        "moran_I_residuos": I, "moran_I_por_anio": morans, "moran_nota": "pesos de distancia inversa truncada a 2 km; solo estadístico, sin p"}

    # --------- comprobación de la medida (adenda 1, punto 17: se aplica a cualquier resultado) ---------
    mm = df.groupby("sec").pct.agg(["mean", "min", "max"])
    expuestas = mm.index[mm["mean"] >= 1.0]
    dh = df[df.sec.isin(expuestas)].reset_index(drop=True)
    xdh = dh.pct - dh.groupby("sec").pct.transform("mean")
    sd_h = float(np.sqrt((xdh ** 2).mean()))
    dh = dh.assign(z=dh.pct / sd_h)
    ph = estimar(dh, "mun_anio", K_full, sec_index)
    res["comprobacion_medida"] = {"obs_con_exposicion_cero": float((df.pct == 0).mean()), "secciones_sin_variacion_intra": float(((mm["max"] - mm["min"]) == 0).mean()),
                                  "dt_intra_pct_puntos": sd, "dt_intra_secciones_media_pct_ge_1": sd_h, "n_secciones_media_pct_ge_1": int(len(expuestas)),
                                  "beta_log_por_DT_secciones_expuestas": float(ph["b"][0]), "se_conley_expuestas": float(ph["se_conley"][0]), "se_mun_expuestas": float(ph["se_mun"][0]), "n_obs_expuestas": ph["n"],
                                  "corr_pct_n": float(df[["pct", "n"]].corr().iloc[0, 1]), "corr_pct_plazas": float(df[["pct", "plazas"]].corr().iloc[0, 1]),
                                  "desv_tipica_residual_log_alquiler": float(np.std(pr["resid"])), "nota": "diagnóstico de la medida; no es una especificación alternativa ni sustituye al principal"}
    registrar(reg, "V15-A", "H3-medida-expuestas", "diagnóstico: secciones con media pct >= 1", "2021", "2024", ph["n"], coef=float(ph["b"][0]), notas="diagnóstico de la medida")
    # --------- placebo de adelanto ---------
    dfl, sdl = preparar_muestra(P, "VC", "pct", lead=True)
    pl = estimar(dfl, "mun_anio", K_full, sec_index, con_lead=True)
    res["placebo_adelanto"] = {"beta_t": float(pl["b"][0]), "beta_lead": float(pl["b"][1]), "se_conley_lead": float(pl["se_conley"][1]), "se_mun_lead": float(pl["se_mun"][1]), "p_conley_lead": p_norm(float(pl["b"][1]), float(pl["se_conley"][1])),
                               "p_municipio_lead_descriptivo": p_norm(float(pl["b"][1]), float(pl["se_mun"][1])), "n_obs": pl["n"], "anios": "2021-2023 (la exposición t+1 usa 2022-2024)"}
    # --------- exclusión de grandes ciudades ---------
    dfg, _ = preparar_muestra(P, "VC", "pct", sin_grandes=True)
    pg = estimar(dfg, "mun_anio", K_full, sec_index)
    res["sin_grandes_ciudades"] = {"beta_log_por_DT": float(pg["b"][0]), "se_conley": float(pg["se_conley"][0]), "se_mun": float(pg["se_mun"][0]), "n_obs": pg["n"], "excluidas": sorted(GRANDES)}
    # regla del 1 % superior de exposición (continua)
    corte = df.groupby("sec").pct.mean().quantile(0.99)
    d99 = df[df.sec.map(df.groupby("sec").pct.mean()) <= corte]
    p99 = estimar(d99.reset_index(drop=True), "mun_anio", K_full, sec_index)
    res["sin_1pct_superior"] = {"beta_log_por_DT": float(p99["b"][0]), "se_conley": float(p99["se_conley"][0]), "n_obs": p99["n"]}
    # --------- IPVA por distrito ---------
    ip_res = {}
    for tfe in ("anio", "mun_anio"):
        q = IP.dropna(subset=["pct", "ipva"]).copy()
        q = q[q.ipva > 0]
        q = q[q.groupby("dis").anio.transform("size") >= 2].copy()
        xd = q.pct - q.groupby("dis").pct.transform("mean")
        sdd = float(np.sqrt((xd ** 2).mean()))
        q["z"], q["ly"] = q.pct / sdd, np.log(q.ipva)
        dis = pd.factorize(q.dis)[0]
        mun = pd.factorize(q.mun)[0]
        grp = pd.factorize(q.anio)[0] if tfe == "anio" else pd.factorize(q.mun + "_" + q.anio.astype(str))[0]
        r = PN.ols_fe(q.ly.values, q[["z"]].values, dis, grp, mun)
        ip_res[tfe] = {"beta_log_por_DT": float(r["b"][0]), "se_municipio": float(r["se_mun"][0]), "n_obs": r["n"], "n_distritos": int(dis.max() + 1), "n_municipios": int(mun.max() + 1)}
        registrar(reg, "V15-A", f"H3-IPVA-distrito-{tfe}", f"log(IPVA distrito) ~ z(pct) + FE distrito + FE {tfe}", "2021", "2024", r["n"], coef=float(r["b"][0]), notas="agrupado por municipio: descriptivo (sin validación MC)")
    res["ipva_distrito"] = ip_res
    for k, v in (("placebo", res["placebo_adelanto"]["beta_lead"]), ("sin_grandes", res["sin_grandes_ciudades"]["beta_log_por_DT"]), ("sin_1pct", res["sin_1pct_superior"]["beta_log_por_DT"])):
        registrar(reg, "V15-A", f"H3-prueba-{k}", "diagnóstico", "2021", "2024", 0, coef=v, notas="diagnóstico")
    # resumen del multiverso
    M = pd.DataFrame(multiverso)
    Mc = M[M.agrupacion == "conley2km"]
    res["resumen_multiverso"] = {"n": int(len(M)), "n_especificaciones": int(len(M) // 2), "pct_positivos": float((M.beta_log_por_DT > 0).mean()), "rango_pct_por_DT": [float(M.pct_por_DT.min()), float(M.pct_por_DT.max())],
                                 "mediana_pct_por_DT": float(M.pct_por_DT.median()), "n_conley_p05": int((Mc.p_normal_descriptivo < 0.05).sum()), "n_conley": int(len(Mc))}
    res["tiempo_s"] = round(time.time() - t0, 1)
    volcar(SALIDA / "estimacion_bruta.json", res)
    reg.flush()
    return res


if __name__ == "__main__":
    main()
