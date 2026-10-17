"""V15-B · E1 (P2): precio frente a alquiler y coste de uso, panel provincial/CCAA trimestral. Solo entrenamiento.

Westerlund, CIPS y CS-ARDL NO APTOS (K13): todo PUNTUAL, sin p ni IC. CD de Pesaran, CIPS (estadístico), MG y PMG son magnitudes descriptivas.
Uso: python3 src/v15/p2_fundamentales.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v15.pb_comun import OUT, Registry, cargar, escribe_json, hecho, resultado_base, serie_q, trim  # noqa: E402

CARPETA = OUT / "p2"


def panel(d, var, nivel):
    x = trim(d[(d.variable == var) & (d.nivel == nivel)]).drop_duplicates(["territorio_codigo", "q"])
    return x.pivot(index="q", columns="territorio_codigo", values="valor").sort_index()


def coste_uso(d):
    tr = serie_q(d, "tipo_hip_real_bde")
    vt = serie_q(d, "ipv")           # sustituido abajo por el valor tasado nacional (media de provincias de entrenamiento)
    p = panel(d, "valor_tasado", "provincia")
    gl = np.log(p).mean(axis=1)
    ganancia = (400 * gl.diff()).rolling(8).mean()
    return (tr + 2.0 - ganancia).rename("uc").dropna()


def datos(medida):
    d = cargar("p2_fundamentales")
    uc = coste_uso(d)
    if medida == "tasado":
        P, A = panel(d, "valor_tasado", "provincia"), panel(d, "ipc_alquiler_indice", "provincia")
    else:
        P, A = panel(d, "ipv", "ccaa"), panel(d, "ipc_alquiler", "ccaa")
    cols = sorted(set(P.columns) & set(A.columns))
    idx = P.index.intersection(A.index).intersection(uc.index)
    y, a = np.log(P.loc[idx, cols]), np.log(A.loc[idx, cols])
    ok = y.notna().all(axis=1) & a.notna().all(axis=1)
    return y[ok], a[ok], uc.loc[y[ok].index]


def lags(M, k):
    return np.vstack([np.full((k, M.shape[1]), np.nan), M[:-k]]) if k else M


def unit_design(i, y, a, uc, p, con_uc, csa):
    """Devuelve Dy, regresores de nivel (y_{t-1}, a_{t-1}[, uc_{t-1}]), cortos y CSA."""
    T = len(y)
    dy = np.r_[np.nan, np.diff(y[:, i])]
    da = np.r_[np.nan, np.diff(a[:, i])]
    duc = np.r_[np.nan, np.diff(uc)]
    lev = [np.r_[np.nan, y[:-1, i]], np.r_[np.nan, a[:-1, i]]] + ([np.r_[np.nan, uc[:-1]]] if con_uc else [])
    cort = [np.r_[np.full(l, np.nan), dy[:T - l]] for l in range(1, p + 1)] + [np.r_[np.full(l, np.nan), da[:T - l]] for l in range(0, p + 1)]
    if con_uc:
        cort += [np.r_[np.full(l, np.nan), duc[:T - l]] for l in range(0, p + 1)]
    ex = []
    if csa is not None:
        for c in csa:
            ex += [np.r_[np.full(l, np.nan), c[:T - l]] for l in range(0, p + 1)]
    return dy, lev, cort, ex


def csa_series(y, a):
    dy = np.r_[np.nan, np.diff(y.mean(1))]
    da = np.r_[np.nan, np.diff(a.mean(1))]
    return [dy, np.r_[np.nan, y.mean(1)[:-1]], np.r_[np.nan, a.mean(1)[:-1]], da]


def ols_ardl(dy, lev, cort, ex):
    Z = np.column_stack([np.ones(len(dy))] + lev + cort + ex)
    ok = np.all(np.isfinite(np.column_stack([dy, Z])), axis=1)
    b, *_ = np.linalg.lstsq(Z[ok], dy[ok], rcond=None)
    r = dy[ok] - Z[ok] @ b
    return b, r, int(ok.sum())


def mg_like(y, a, uc, p, con_uc, cs):
    N = y.shape[1]
    csa = csa_series(y, a) if cs else None
    th, ph, res = [], [], {}
    nl = 3 if con_uc else 2
    for i in range(N):
        dy, lev, cort, ex = unit_design(i, y, a, uc, p, con_uc, csa)
        b, r, n = ols_ardl(dy, lev, cort, ex)
        phi = b[1]
        if phi >= -1e-4 or phi < -1.5:       # sin corrección de error estable: la unidad no aporta velocidad de ajuste
            continue
        th.append(-b[2:1 + nl] / phi)
        ph.append(phi)
        res[i] = r
    return np.array(th), np.array(ph), res


def pmg(y, a, uc, p, con_uc):
    N, nl = y.shape[1], (2 if con_uc else 1)
    unidades = [unit_design(i, y, a, uc, p, con_uc, None) for i in range(N)]

    def fit(theta):
        tot, ph = 0.0, []
        for dy, lev, cort, ex in unidades:
            lv = lev[0] - lev[1] * theta[0] - (lev[2] * theta[1] if con_uc else 0)
            Z = np.column_stack([np.ones(len(dy)), lv] + cort)
            ok = np.all(np.isfinite(np.column_stack([dy, Z])), axis=1)
            b, *_ = np.linalg.lstsq(Z[ok], dy[ok], rcond=None)
            r = dy[ok] - Z[ok] @ b
            tot += ok.sum() * np.log(r @ r / ok.sum())
            ph.append(b[1])
        return tot, np.array(ph)
    x0 = np.ones(nl)
    r = minimize(lambda t: fit(t)[0], x0, method="L-BFGS-B", bounds=[(-5.0, 10.0)] * nl)
    return r.x, fit(r.x)[1]


def cd_pesaran(R):
    """Estadístico CD (Pesaran 2004) de una matriz T x N (descriptivo)."""
    Rz = R - np.nanmean(R, 0)
    C = np.corrcoef(Rz[np.all(np.isfinite(Rz), axis=1)].T)
    N, T = C.shape[0], np.sum(np.all(np.isfinite(Rz), axis=1))
    return float(np.sqrt(2 * T / (N * (N - 1))) * C[np.triu_indices(N, 1)].sum()), float(C[np.triu_indices(N, 1)].mean())


def cips(M, p=1):
    """Media de los t de la CADF(p) con media transversal (estadístico CIPS; solo descriptivo, herramienta NO APTA)."""
    T, N = M.shape
    ybar = M.mean(1)
    ts = []
    for i in range(N):
        dy = np.r_[np.nan, np.diff(M[:, i])]
        cols = [np.r_[np.nan, M[:-1, i]], np.r_[np.nan, ybar[:-1]], np.r_[np.nan, np.diff(ybar)]] + [np.r_[np.full(l, np.nan), dy[:T - l]] for l in range(1, p + 1)]
        Z = np.column_stack([np.ones(T)] + cols)
        ok = np.all(np.isfinite(np.column_stack([dy, Z])), axis=1)
        b, *_ = np.linalg.lstsq(Z[ok], dy[ok], rcond=None)
        r = dy[ok] - Z[ok] @ b
        s2 = r @ r / (ok.sum() - Z.shape[1])
        se = np.sqrt(s2 * np.linalg.inv(Z[ok].T @ Z[ok])[1, 1])
        ts.append(b[1] / se)
    return float(np.mean(ts))


def resumen(th, ph):
    if len(ph) == 0:
        return {"n_unidades": 0}
    hl = np.log(0.5) / np.log1p(ph)
    return {"n_unidades": int(len(ph)), "theta_precio_alquiler_media": float(np.mean(th[:, 0])), "theta_mediana": float(np.median(th[:, 0])),
            "theta_iqr": [float(np.quantile(th[:, 0], .25)), float(np.quantile(th[:, 0], .75))],
            "theta_uso_media": float(np.mean(th[:, 1])) if th.shape[1] > 1 else None,
            "velocidad_media": float(np.mean(ph)), "velocidad_mediana": float(np.median(ph)),
            "semivida_mediana_anios": float(np.median(hl) / 4), "semivida_iqr_anios": [float(np.quantile(hl, .25) / 4), float(np.quantile(hl, .75) / 4)]}


def main():
    CARPETA.mkdir(parents=True, exist_ok=True)
    reg = Registry(CARPETA / "registro.csv")
    filas, diag = [], {}
    for medida in ("tasado", "ipv"):
        yy, aa, uc = datos(medida)
        y, a, ucv = yy.values, aa.values, uc.values
        per = f"{yy.index[0]}-{yy.index[-1]}"
        cd, rho = cd_pesaran(np.diff(y, axis=0))
        diag[f"{medida}_estructura"] = {"N": int(y.shape[1]), "T": int(y.shape[0]), "periodo": per, "CD_Pesaran_dlog_precio": cd, "correlacion_media": rho,
                                        "CIPS_log_precio_p1": cips(y), "CIPS_log_alquiler_p1": cips(a), "tipo": "descriptivo (CIPS NO APTO)"}
        for est in ("MG", "CS-ARDL", "PMG"):
            for p in (0, 1, 2):
                for cu in (False, True):
                    if est == "PMG":
                        thv, ph = pmg(y, a, ucv, p, cu)
                        th = np.tile(thv, (len(ph), 1))
                        ph = ph[(ph < -1e-4) & (ph > -1.5)]
                        th = th[:len(ph)]
                    else:
                        th, ph, _ = mg_like(y, a, ucv, p, cu, est == "CS-ARDL")
                    r = resumen(th, ph)
                    idm = f"E1-{medida}-{est}-p{p}-{'uso' if cu else 'sinuso'}"
                    filas.append({"id": idm, "medida": medida, "estimador": est, "rezagos": p, "coste_uso": cu, **{k: (v if not isinstance(v, list) else str(v)) for k, v in r.items()}})
                    reg.log("E1", idm, f"{medida} {est} p={p} uso={cu}", yy.index[0], yy.index[-1], int(y.shape[0] * y.shape[1]), np.nan, np.nan, np.nan,
                            coef_interes=r.get("theta_precio_alquiler_media", np.nan), notas="puntual (CS-ARDL/Westerlund/CIPS NO APTOS)")
    F = pd.DataFrame(filas)
    F.to_csv(CARPETA / "multiverso.csv", index=False)
    pr = F[(F.medida == "tasado") & (F.estimador == "CS-ARDL") & (F.rezagos == 1) & (~F.coste_uso)].iloc[0]
    resumen_mv = {"n": int(len(F)), "theta_media_min": float(F.theta_precio_alquiler_media.min()), "theta_media_max": float(F.theta_precio_alquiler_media.max()),
                  "frac_semivida_2_a_7": float(((F.semivida_mediana_anios >= 2) & (F.semivida_mediana_anios <= 7)).mean()),
                  "semivida_mediana_min_max": [float(F.semivida_mediana_anios.min()), float(F.semivida_mediana_anios.max())],
                  "por_estimador": F.groupby("estimador").theta_precio_alquiler_media.median().to_dict()}
    diag["multiverso_36"] = resumen_mv
    diag["herramientas_no_aptas"] = {"Westerlund": "NO APTO (tamaño 0,09-0,20)", "CIPS": "NO APTO (tamaño 0,0105, conservador)", "CS-ARDL": "NO APTO (elasticidad: cobertura 0,99; velocidad: cobertura 0,003)",
                                     "consecuencia": "solo puntual; sin p ni IC; la «cointegración» no se contrasta"}
    diag["PMG_con_coste_de_uso"] = "no identificado: θ del coste de uso en el límite del rango [-5, 10] con velocidad ≈ 0 (verosimilitud degenerada); se reporta n_unidades = 0 (DV15-B-7)"
    diag["MG_dispersion"] = "las medias de grupo del MG están dominadas por unidades con velocidad cercana a 0 (θ = -b/φ); léase la mediana y el rango intercuartílico en multiverso.csv"
    diag["criterio_potencia_V15"] = "potencia de Westerlund frente a -0,04 < 0,5 o NO APTO: E1 solo descriptiva"
    sel = F[(F.medida == "tasado") & (F.estimador.isin(["MG", "PMG"])) & (~F.coste_uso)].semivida_mediana_anios
    sv_mg, sv_lo, sv_hi = float(sel.median()), float(sel.min()), float(sel.max())
    res = resultado_base("r15/p2", "E1: ¿existe una relación de largo plazo entre el valor tasado y el alquiler/coste de uso en el panel provincial? (descriptiva)",
                         "data/processed/v15/p2_fundamentales.parquet (38 provincias; entrenamiento)", int(diag["tasado_estructura"]["N"] * diag["tasado_estructura"]["T"]),
                         "ECM por unidad: CS-ARDL (principal declarado, p=1, sin coste de uso), MG y PMG como contraste; todo puntual",
                         {"theta_precio_alquiler_CS_ARDL": float(pr.theta_precio_alquiler_media), "velocidad_media": float(pr.velocidad_media), "semivida_mediana_anios": float(pr.semivida_mediana_anios)},
                         None, "DESCRIPTIVO (asociación de largo plazo; C4, sin inferencia APTA)", diag, {"modelo": None, "rmse": None, "dm_vs_ar4": None},
                         ["Sin p ni IC (herramientas NO APTAS). Capa C4; pendiente de evaluación sellada (valor tasado e IPC alquiler posteriores al corte).",
                          "No contrasta cointegración: V7.2 («no se establece cointegración») ni se confirma ni se matiza con inferencia."],
                         [{"id": "E1-principal", "p": None, "motivo": "NO APTO"}] + [{"id": r_, "p": None} for r_ in F.id])
    escribe_json(CARPETA / "resultado.json", res)
    escribe_json(CARPETA / "hechos.json", [
        hecho("V15-E1-theta", "Elasticidad de largo plazo precio-alquiler (CS-ARDL, media de provincias; puntual)", round(float(pr.theta_precio_alquiler_media), 3),
              round(resumen_mv["theta_media_min"], 3), round(resumen_mv["theta_media_max"], 3), "elasticidad", "2002T1-2026T2", "38 provincias de entrenamiento", "MIVAU valor tasado; INE IPC alquiler", "theta", "p2"),
        hecho("V15-E1-semivida", "Semivida mediana del desajuste en MG y PMG sin coste de uso (años; puntual; el CS-ARDL se descarta como cifra: cobertura de la velocidad 0,003 en el Monte Carlo)", round(sv_mg, 2),
              round(sv_lo, 2), round(sv_hi, 2), "años", "2002T1-2026T2", "38 provincias", "MIVAU; INE", "semivida", "p2")])
    print(F[["id", "n_unidades", "theta_precio_alquiler_media", "velocidad_media", "semivida_mediana_anios"]].to_string())
    print(diag["tasado_estructura"], diag["ipv_estructura"])


if __name__ == "__main__":
    main()
