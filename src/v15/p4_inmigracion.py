"""V15-B · H4 (P4): inmigración y alquiler, shift-share municipal (SERPAVI VC/VU, padrón 2003-2022). Solo entrenamiento.

AKM y AKM0 NO APTOS (K13): estimación PUNTUAL, sin p ni IC. F efectivo, pesos de Rotemberg, pretendencias y balance son magnitudes descriptivas.
Uso: python3 src/v15/p4_inmigracion.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v15.pb_comun import (COSTERAS, GRANDES_MUN, OUT, P15, Registry, SEED, cargar, centroides_mun, demean, escribe_json, hecho,  # noqa: E402
                              resultado_base)

PAISES = ["Alemania", "Argelia", "Argentina", "Bolivia", "Brasil", "Bulgaria", "Chile", "China", "Colombia", "Cuba", "Ecuador", "Francia",
          "Italia", "Marruecos", "Nigeria", "Pakistán", "Paraguay", "Perú", "Polonia", "Portugal", "Reino Unido", "República Dominicana",
          "Rumanía", "Rusia", "Senegal", "Ucrania", "Uruguay", "Venezuela"]
RESIDENCIALES = ["Alemania", "Francia", "Italia", "Portugal", "Reino Unido"]
CONTINENTES = ["De Africa", "De América", "De Asia", "Europa (sin España)", "Oceanía y Apátridas"]
ANIOS = list(range(2003, 2023))
CARPETA = OUT / "p4"


def cargar_datos():
    d = cargar("p4_inmigracion")
    p = d[(d.variable == "padron_municipal_nacionalidad") & (d.nivel == "municipio")].copy()
    p["nac"] = p.desagregacion.str.replace("nacionalidad=", "", regex=False)
    p["periodo"] = p.periodo.astype(int)
    s = d[(d.variable == "serpavi_alquiler_m2_mediana") & (d.nivel == "municipio")].copy()
    s["periodo"] = s.periodo.astype(int)
    s["tip"] = s.desagregacion.str.replace("tipologia=", "", regex=False)
    return p, s


def matrices(p, s):
    muni = sorted(set(p.territorio_codigo) & set(s.territorio_codigo))
    mi = {m: i for i, m in enumerate(muni)}
    ti = {a: j for j, a in enumerate(ANIOS)}
    nacs = PAISES + CONTINENTES + ["Extranjera", "Total"]
    ni = {n: k for k, n in enumerate(nacs)}
    A = np.full((len(muni), len(nacs), len(ANIOS)), np.nan)
    q = p[p.nac.isin(nacs) & p.territorio_codigo.isin(mi)]
    A[q.territorio_codigo.map(mi).values, q.nac.map(ni).values, q.periodo.map(ti).values] = q.valor.values
    R = {}
    for tip in ("VC", "VU"):
        M = np.full((len(muni), len(ANIOS)), np.nan)
        x = s[(s.tip == tip) & s.territorio_codigo.isin(mi) & s.periodo.isin(ti)]
        M[x.territorio_codigo.map(mi).values, x.periodo.map(ti).values] = x.valor.values
        R[tip] = M
    return muni, nacs, ni, A, R


def instrumento(A, ni, origenes, base):
    """z[i,t] = sum_k s_ik(base) * g_kt (g leave-one-out). Devuelve z (n x T) y componentes z_k (n x K x T) para Rotemberg."""
    tb = ANIOS.index(base)
    Ik = [ni[o] for o in origenes]
    N = A[:, Ik, :]                                  # n x K x T
    tot_b = A[:, ni["Total"], tb]
    share = N[:, :, tb] / tot_b[:, None]
    NK = np.nansum(N, axis=0)                        # K x T
    num = (NK[None, :, 1:] - N[:, :, 1:]) - (NK[None, :, :-1] - N[:, :, :-1])
    den = NK[None, :, :-1] - N[:, :, :-1]
    with np.errstate(divide="ignore", invalid="ignore"):
        g = np.where(den > 0, num / den, np.nan)       # n x K x (T-1): crecimiento t frente a t-1
    zk = np.full(N.shape, np.nan)
    zk[:, :, 1:] = share[:, :, None] * g
    zk = np.nan_to_num(zk, nan=0.0)
    return zk.sum(1), zk, share


def panel(A, R, ni, muni, tip, norm, origenes, base, minpob=0, excluir=None, years=range(2012, 2023), minobs=6):
    ti = ANIOS.index
    z, zk, _ = instrumento(A, ni, origenes, base)
    ext, tot = A[:, ni["Extranjera"], :], A[:, ni["Total"], :]
    rows = []
    for a in years:
        t, t0 = ti(a), ti(a - 1)
        den = tot[:, t0] if norm == "prev" else tot[:, ti(base)]
        x = 100 * (ext[:, t] - ext[:, t0]) / den
        y = np.log(R[tip][:, t]) - np.log(R[tip][:, t0])
        rows.append(pd.DataFrame({"i": np.arange(len(muni)), "anio": a, "y": y, "x": x, "z": 100 * z[:, t], "zl": 100 * z[:, t0] if t0 > 0 else np.nan,
                                  "pob_base": tot[:, ti(base)], "prov": [m[:2] for m in muni]}))
    L = pd.concat(rows, ignore_index=True)
    L = L.replace([np.inf, -np.inf], np.nan).dropna(subset=["y", "x", "z"])
    if minpob:
        L = L[L.pob_base >= minpob]
    if excluir is not None:
        L = L[~L.i.isin(excluir)]
    n_obs = L.groupby("i").size()
    L = L[L.i.isin(n_obs[n_obs >= minobs].index)]
    return L.reset_index(drop=True), zk


def fe_grupo(L, temporal):
    if temporal == "provincia_anio":
        return [L.prov.astype(str) + "_" + L.anio.astype(str)], None
    cost = (L.prov.isin(COSTERAS).astype(float) * 1.0).values
    dums = np.column_stack([cost * (L.anio == a).values for a in sorted(L.anio.unique())[1:]])
    return [L.anio.astype(str)], dums


def dos_sls(L, temporal="provincia_anio", controles=None, endog=("x",), inst=("z",)):
    g, dums = fe_grupo(L, temporal)
    cols = [L[c].values for c in (*endog, *inst)] + [L.y.values]
    if controles:
        cols += [L[c].values for c in controles]
    M = demean(np.column_stack(cols), g)
    ne, nz = len(endog), len(inst)
    Xe, Z, y = M[:, :ne], M[:, ne:ne + nz], M[:, ne + nz]
    C = M[:, ne + nz + 1:] if controles else np.empty((len(L), 0))
    if dums is not None:
        D = demean(dums, g)
        C = np.column_stack([C, D])
    if C.shape[1]:
        P = np.eye(len(y)) if False else None
        H = np.linalg.lstsq(C, np.column_stack([Xe, Z, y]), rcond=None)[0]
        R = np.column_stack([Xe, Z, y]) - C @ H
        Xe, Z, y = R[:, :ne], R[:, ne:ne + nz], R[:, ne + nz]
    Pz = Z @ np.linalg.solve(Z.T @ Z, Z.T @ Xe)
    b = np.linalg.solve(Pz.T @ Xe, Pz.T @ y)
    ols_b = np.linalg.solve(Xe.T @ Xe, Xe.T @ y)
    pi = np.linalg.solve(Z.T @ Z, Z.T @ Xe[:, 0])
    u = Xe[:, 0] - Z @ pi
    # F robusta de primera etapa (HC1) para un instrumento; descriptiva (no hay inferencia APTA)
    Zr = Z - 0
    meat = (Zr * u[:, None]).T @ (Zr * u[:, None])
    V = np.linalg.solve(Z.T @ Z, meat) @ np.linalg.inv(Z.T @ Z) * len(y) / max(len(y) - nz, 1)
    F = float(pi @ np.linalg.solve(V, pi) / nz)
    rf = np.linalg.solve(Z.T @ Z, Z.T @ y)
    return {"beta_pp": float(b[0]), "ols_pp": float(ols_b[0]), "forma_reducida": [float(v) for v in rf], "F_robusto": F, "pi": [float(v) for v in pi],
            "n": int(len(y)), "n_municipios": int(L.i.nunique()), "_xt": Xe[:, 0], "_zt": Z[:, 0], "_yt": y}


def rotemberg(L, zk, temporal="provincia_anio"):
    g, dums = fe_grupo(L, temporal)
    K = zk.shape[1]
    anios = L.anio.values
    ti = np.array([ANIOS.index(a) for a in anios])
    cols = [zk[L.i.values, k, ti] * 100 for k in range(K)]
    M = demean(np.column_stack(cols + [L.x.values, L.y.values]), g)
    xt, yt = M[:, K], M[:, K + 1]
    zt = M[:, :K]
    num = zt.T @ xt
    tot = num.sum()
    alpha = num / tot
    with np.errstate(divide="ignore", invalid="ignore"):
        bk = (zt.T @ yt) / num
    return alpha, bk


def main():
    CARPETA.mkdir(parents=True, exist_ok=True)
    reg = Registry(CARPETA / "registro.csv")
    p, s = cargar_datos()
    muni, nacs, ni, A, R = matrices(p, s)
    principal = [o for o in PAISES if o not in RESIDENCIALES]
    base = dict(tip="VC", norm="prev", origenes=principal, base=2003, minpob=0)
    L, zk = panel(A, R, ni, muni, **base)
    est = dos_sls(L)
    reg.log("H4", "H4-principal", "dlog SERPAVI VC ~ dExt/Pob(t-1) [IV z_UE14-excl_2003]; FE provincia x anio", 2012, 2022, est["n"], np.nan, np.nan, np.nan,
            coef_interes=est["beta_pp"], p_interes=np.nan, notas="puntual (AKM/AKM0 NO APTOS); sin p")
    diag = {}
    # --- Rotemberg y número efectivo de choques
    alpha, bk = rotemberg(L, zk[:, [PAISES.index(o) for o in principal]] if False else zk)
    nombres = principal
    # zk aqui: dimension K=len(principal) (instrumento() usa solo los origenes dados)
    orden = np.argsort(-np.abs(alpha))
    rot = [{"origen": nombres[k], "peso": float(alpha[k]), "beta_k_pp": float(bk[k])} for k in orden[:8]]
    neff = float(1 / np.sum(alpha ** 2))
    diag["rotemberg"] = {"top8": rot, "n_efectivo_choques_1_sobre_HHI": neff, "suma_pesos_negativos": float(alpha[alpha < 0].sum()), "tipo": "descriptivo"}
    # --- Pretendencias: instrumento medio 2014-2022 frente a dlog SERPAVI 2012-2013 (SERPAVI 2011-2013)
    pre, _ = panel(A, R, ni, muni, years=[2012, 2013], minobs=1, **base)
    zbar = L.groupby("i").z.mean()
    pre = pre.groupby("i").agg(y=("y", "mean"), prov=("prov", "first")).join(zbar.rename("zbar"), how="inner").reset_index()
    Mp = demean(pre[["y", "zbar"]].values, [pre.prov])
    pend = float((Mp[:, 0] @ Mp[:, 1]) / (Mp[:, 1] @ Mp[:, 1]))
    corr = float(np.corrcoef(Mp[:, 0], Mp[:, 1])[0, 1])
    diag["pretendencias_2011_2013"] = {"pendiente_dlog_por_pp_z": pend, "correlacion": corr, "n": int(len(pre)), "tipo": "descriptivo (sin inferencia APTA)"}
    # --- Balance: instrumento medio frente a características de 2003
    ti3 = ANIOS.index(2003)
    car = pd.DataFrame({"i": np.arange(len(muni)), "lpob03": np.log(A[:, ni["Total"], ti3]), "cuota_ext03": A[:, ni["Extranjera"], ti3] / A[:, ni["Total"], ti3]})
    bal = pre.merge(car, on="i").replace([np.inf, -np.inf], np.nan).dropna()
    Mb = demean(bal[["zbar", "lpob03", "cuota_ext03"]].values, [bal.prov])
    diag["balance_2003"] = {"corr_z_logpob03": float(np.corrcoef(Mb[:, 0], Mb[:, 1])[0, 1]), "corr_z_cuota_ext03": float(np.corrcoef(Mb[:, 0], Mb[:, 2])[0, 1]),
                            "n": int(len(bal)), "tipo": "descriptivo"}
    # --- JRS: instrumento retardado como control
    Lj = L.dropna(subset=["zl"])
    diag["jaeger_ruist_stuhler_control_z_retardado"] = {k: v for k, v in dos_sls(Lj, controles=["zl"]).items() if not k.startswith("_")}
    # --- exclusion 5 orígenes de mayor peso Rotemberg
    top5 = [nombres[k] for k in orden[:5]]
    L5, _ = panel(A, R, ni, muni, tip="VC", norm="prev", origenes=[o for o in principal if o not in top5], base=2003, minpob=0)
    diag["excluye_5_origenes_Rotemberg"] = {"excluidos": top5, **{k: v for k, v in dos_sls(L5).items() if not k.startswith("_")}}
    # --- desbordamiento 15 km: vecinos <15 km añadidos como regresor endógeno instrumentado
    cen = centroides_mun(muni)
    idx = np.array([m in cen.index for m in muni])
    xyz = cen.reindex(muni).values
    Wd = np.full((len(muni), len(muni)), False)
    ok = np.where(idx)[0]
    D = np.sqrt(((xyz[ok][:, None, :] - xyz[ok][None, :, :]) ** 2).sum(-1))
    Wn = (D < 15) & (D > 0)
    W = np.zeros((len(muni), len(muni)))
    W[np.ix_(ok, ok)] = Wn / np.maximum(Wn.sum(1, keepdims=True), 1)
    Ls = L.copy()
    xs = Ls.pivot(index="i", columns="anio", values="x").reindex(range(len(muni)))
    zs = Ls.pivot(index="i", columns="anio", values="z").reindex(range(len(muni)))
    xn = pd.DataFrame(W @ np.nan_to_num(xs.values), index=xs.index, columns=xs.columns)
    zn = pd.DataFrame(W @ np.nan_to_num(zs.values), index=zs.index, columns=zs.columns)
    Ls["x_nb"] = [xn.at[i, a] for i, a in zip(Ls.i, Ls.anio)]
    Ls["z_nb"] = [zn.at[i, a] for i, a in zip(Ls.i, Ls.anio)]
    Ls = Ls[Ls.i.isin(ok[Wn.sum(1) > 0])]
    sp = dos_sls(Ls, endog=("x", "x_nb"), inst=("z", "z_nb"))
    diag["desbordamiento_15km"] = {"beta_propio_pp": sp["beta_pp"], "n": sp["n"], "tipo": "puntual"}
    # --- exclusiones preregistradas: grandes ciudades y 1 % superior de exposición
    idx_gr = [muni.index(m) for m in GRANDES_MUN if m in muni]
    Lg, _ = panel(A, R, ni, muni, excluir=idx_gr, **base)
    diag["excluye_Barcelona_Valencia"] = {k: v for k, v in dos_sls(Lg).items() if not k.startswith("_")}
    xm = L.groupby("i").x.mean()
    top1 = xm[xm >= xm.quantile(0.99)].index.tolist()
    Lt, _ = panel(A, R, ni, muni, excluir=top1, **base)
    diag["excluye_1pct_superior_exposicion"] = {k: v for k, v in dos_sls(Lt).items() if not k.startswith("_")}
    # --- instrumento con los 28 orígenes (robustez)
    L28, _ = panel(A, R, ni, muni, tip="VC", norm="prev", origenes=PAISES, base=2003)
    diag["instrumento_28_origenes"] = {k: v for k, v in dos_sls(L28).items() if not k.startswith("_")}
    # --- multiverso 64
    mv = []
    for tip in ("VC", "VU"):
        for norm in ("prev", "base"):
            for orig_n, orig in (("28", PAISES), ("continentes", CONTINENTES)):
                for temp in ("provincia_anio", "anio"):
                    for b in (2003, 2008):
                        for mp, mpn in ((0, "todas"), (1000, "ge1000")):
                            Lm, _ = panel(A, R, ni, muni, tip=tip, norm=norm, origenes=orig, base=b, minpob=mp)
                            e = dos_sls(Lm, temporal=temp)
                            idm = f"H4-mv-{tip}-{norm}-{orig_n}-{temp}-{b}-{mpn}"
                            mv.append({"id": idm, "tip": tip, "norm": norm, "origenes": orig_n, "temporal": temp, "base": b, "muestra": mpn,
                                       "beta_pp": e["beta_pp"], "ols_pp": e["ols_pp"], "F_robusto": e["F_robusto"], "n": e["n"]})
                            reg.log("H4", idm, f"{tip},{norm},{orig_n},{temp},{b},{mpn}", 2012, 2022, e["n"], np.nan, np.nan, np.nan, coef_interes=e["beta_pp"], notas="puntual")
    mvd = pd.DataFrame(mv)
    mvd.to_csv(CARPETA / "multiverso.csv", index=False)
    # --- sesgo OLS y descripción
    est_pub = {k: v for k, v in est.items() if not k.startswith("_")}
    diag["f_efectivo_primera_etapa"] = {"F_robusto_HC1": est["F_robusto"], "umbral_MOP_tau10_referencia_un_instrumento": 23.1,
                                        "nota": "descriptivo; el procedimiento MOP/AR/AKM no es APTO (K13). Referencia de valor crítico para 1 instrumento y tau=10 %: ~23,1 (Montiel Olea-Pflueger, cota)"}
    diag["herramientas_no_aptas"] = {"AKM": "NO APTO (tamaño 0,22-0,33)", "AKM0": "NO APTO (tamaño 0,005-0,008, conservador)", "agrupacion_provincia": "NO APTO (tamaño 0,43-0,71)",
                                     "consecuencia": "solo estimación puntual; sin p ni IC; sin TOST"}
    diag["pruebas_C3_no_evaluables_ahora"] = ["evaluación sellada temporal 2022->2025 (pendiente: último trimestre de 2027)", "AKM/AR (no apto)", "F efectivo MOP (descriptivo)"]
    diag["multiverso_64"] = {"n": int(len(mvd)), "beta_pp_min": float(mvd.beta_pp.min()), "beta_pp_max": float(mvd.beta_pp.max()), "beta_pp_mediana": float(mvd.beta_pp.median()),
                             "signo_positivo_frac": float((mvd.beta_pp > 0).mean()), "F_robusto_mediana": float(mvd.F_robusto.median()), "F_robusto_max": float(mvd.F_robusto.max())}
    res = resultado_base(
        "r15/p4", "H4: ¿se asocia la población extranjera predicha por cuotas de origen con el alquiler municipal? (asociación, solo puntual)",
        "data/processed/v15/p4_inmigracion.parquet (padrón 2003-2022, SERPAVI municipal 2011-2022; entrenamiento)", est["n"],
        "2SLS shift-share (Δlog alquiler SERPAVI VC sobre ΔPobExt/Pob(t-1); instrumento Σ cuotas 2003 × crecimiento nacional leave-one-out, sin orígenes residenciales); FE provincia×año; puntual",
        {"beta_pp_alquiler_por_pp_poblacion_extranjera": est["beta_pp"] * 100, "unidad": "% de alquiler por punto porcentual de población extranjera", "ols_pp": est["ols_pp"] * 100,
         "forma_reducida": est["forma_reducida"], "primera_etapa_pi": est["pi"], "F_robusto": est["F_robusto"], "n_municipios": est["n_municipios"]},
        None, "ASOCIACIÓN (C4, estimación puntual; sin inferencia APTA)", diag,
        {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        ["Herramientas de inferencia NO APTAS (K13): estimación puntual sin p ni IC.", "Capa máxima C4; pendiente de evaluación sellada temporal (último trimestre de 2027).",
         "Contrasta con V9-D4 (provincial, IPC/valor tasado, F efectiva 2,8-4,6): no es lo mismo ni lo reemplaza.", "Preperiodo SERPAVI 2011-2013; sin lenguaje causal."],
        [{"id": "H4-principal", "p": None, "motivo": "AKM/AKM0 NO APTO"}] + [{"id": r["id"], "p": None} for r in mv])
    escribe_json(CARPETA / "resultado.json", res)
    h = [hecho("V15-H4-beta", "Asociación (2SLS puntual) entre población extranjera predicha y alquiler municipal (SERPAVI VC), % por punto", round(est["beta_pp"] * 100, 3),
               round(float(mvd.beta_pp.min()) * 100, 3), round(float(mvd.beta_pp.max()) * 100, 3), "% por p.p.", "2012-2022", f"{est['n_municipios']} municipios de entrenamiento",
               "INE padrón; MIVAU SERPAVI", "beta", "p4"),
         hecho("V15-H4-F", "F robusto de primera etapa (descriptivo)", round(est["F_robusto"], 2), round(float(mvd.F_robusto.min()), 2), round(float(mvd.F_robusto.max()), 2), "F", "2012-2022",
               "entrenamiento", "INE padrón", "F", "p4"),
         hecho("V15-H4-neff", "Número efectivo de choques (1/HHI de Rotemberg)", round(neff, 2), None, None, "choques", "2012-2022", "entrenamiento", "INE padrón", "rotemberg", "p4")]
    escribe_json(CARPETA / "hechos.json", h)
    print(est_pub, neff, diag["multiverso_64"])
    return res


if __name__ == "__main__":
    main()
