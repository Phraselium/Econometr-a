"""V18 · réplica ciega de E2-R1 (Ley 11/2020 de Cataluña, Incasòl trimestral, renta media en logaritmos).

Desde docs/v18/plan_replicacion.md (1.2) y la adenda (R-1, R-16, 1.3, 1.5, Anexo A). Capa C4; réplica ciega V18.
Determinista (SEED 20261010), sin red. Lecturas con sellado.filtrar (guarda de check_v17); nunca data/sealed.

Especificación: ln renta_mt = b * Reg_m * Post_t + th * Reg_m * 1[t = 2020T3] + a_m + g_t + X'l + e_mt
  ventana 2019T1-2022T1 (13 trimestres); Post = 2020T4-2022T1; anticipación 2020T3; base 2019T4 (la ficha lo fija como normalización
  del estudio de eventos; en la DiD agrupada los trimestres previos van en la referencia).
  Tratados: 61 municipios de la Ley 11/2020 (data/raw/v3/cataluna_contencion_rentas_v3.csv) sin Barcelona ciudad.
  Controles (JMS, p. 8 según la adenda R-16): municipios catalanes no regulados con crecimiento anual compuesto de la renta media
  2014-2019 > 4,15 %, con renta y contratos en los 13 trimestres (panel equilibrado), sin Barcelona.
  Covariables: ln paro registrado (SEPE, media trimestral de los meses); Población municipal 2019-2022 no está en la base (pob_total municipal tiene 1 municipio; pob_censo_anual empieza en 2021) y ERTE no está: se omiten y se dice.
  Inferencia: no hay correspondencia municipio-comarca en el repositorio, así que la agrupación de la adenda (comarca, 42) no se puede
  construir: se usa cluster por municipio, con CR1 y con wild cluster bootstrap de Webb (WCR, H0 impuesta, 9.999 réplicas).
  IC95 Webb: bootstrap-t percentil (WCU) con el mismo generador.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import holdout  # noqa: E402,F401
import sellado  # noqa: E402

SEED = 20261010
SALIDA = RAIZ / "output" / "v18" / "replica" / "e2_r1"
QS = [f"{a}T{k}" for a in (2019, 2020, 2021, 2022) for k in (1, 2, 3, 4)][:13]  # 2019T1 .. 2022T1
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
BARCELONA = "08019"


def leer_incasol():
    d = pd.read_csv(RAIZ / "data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz", dtype={"codi_territorial": str})
    t = d[d.periodo_iso.str.match(r"^\d{4}T[1-4]$")].copy()
    a = d[d.periodo_iso.str.match(r"^\d{4}_gener-desembre$")].copy()
    a["anio"] = a.periodo_iso.str[:4]
    t = sellado.filtrar(t, "codi_territorial", "municipio", "periodo_iso", "incasol_renta_media", "T")
    a = sellado.filtrar(a, "codi_territorial", "municipio", "anio", "incasol_renta_media", "A")
    return t, a


def leer_covariables():
    """Paro registrado trimestral (media de los meses del fichero mensual del SEPE; el anual de la base
    no tiene 2020). El mensual hereda el tope del anual por la regla 1.4 f (mismo dato, mismo nivel)."""
    m = pd.read_csv(RAIZ / "data/raw/v9/sepe_municipios/paro_registrado_municipio_mensual.csv.gz", dtype={"cod_municipio": str, "mes": str})
    m["anio"] = m["mes"].str[:4]
    m = m[(m.anio >= "2019") & (m.anio <= "2022")]
    m = sellado.filtrar(m, "cod_municipio", "municipio", "anio", "sepe_paro_registrado_media_anual", "A")
    m["trim"] = m["mes"].str[:4] + "T" + ((m["mes"].str[4:6].astype(int) - 1) // 3 + 1).astype(str)
    paro = m.groupby(["cod_municipio", "trim"]).paro_registrado.mean().unstack()
    return {"paro_trim": paro}


def desmedia2(A):
    return A - A.mean(-1, keepdims=True) - A.mean(-2, keepdims=True) + A.mean((-2, -1), keepdims=True)


def ols_cr1(y, Z):
    """y (G,T), Z (G,T,K) ya con dos vías desmediadas. Devuelve beta, EE CR1 por cluster (fila), residuos."""
    G, T, K = Z.shape
    Zf = Z.reshape(G * T, K)
    yf = y.reshape(-1)
    A = np.linalg.inv(Zf.T @ Zf)
    b = A @ (Zf.T @ yf)
    e = (yf - Zf @ b).reshape(G, T)
    S = np.einsum("gtk,gt->gk", Z, e)
    V = A @ (S.T @ S) @ A
    N = G * T
    c = G / (G - 1) * (N - 1) / (N - (K + T - 1))
    return b, np.sqrt(np.diag(c * V)), e, A, c


def wild_webb(y, Z, j, B, rng, b0=0.0):
    """WCR (p-valor) y WCU (IC percentil-t) de Webb por cluster para el coeficiente j; efectos por dos vías reabsorbidos."""
    G, T, K = Z.shape
    b, se, e, A, c = ols_cr1(y, Z)
    t_obs = (b[j] - b0) / se[j]
    # restringido: quitar b0 * Z_j, reestimar sin Z_j para los residuos restringidos
    idx = [k for k in range(K) if k != j]
    Zr = Z[:, :, idx]
    Zrf = Zr.reshape(G * T, -1)
    yr = (y - b0 * Z[:, :, j]).reshape(-1)
    br = np.linalg.solve(Zrf.T @ Zrf, Zrf.T @ yr)
    er = (yr - Zrf @ br).reshape(G, T)
    fit_r = (Zrf @ br).reshape(G, T) + b0 * Z[:, :, j]
    Zf = Z.reshape(G * T, K)
    Ainv = A
    cuenta = 0
    tb_u = np.empty(B)
    N = G * T
    for r0 in range(0, B, 1000):
        n = min(1000, B - r0)
        w = WEBB[rng.integers(0, 6, size=(n, G))]
        # WCR
        ys = fit_r[None] + w[:, :, None] * er[None]
        ys = desmedia2(ys)
        bs = np.einsum("kf,bf->bk", Ainv @ Zf.T, ys.reshape(n, -1))
        es = ys - np.einsum("gtk,bk->bgt", Z, bs)
        S = np.einsum("gtk,bgt->bgk", Z, es)
        Vj = np.einsum("k,bgk->bg", Ainv[j], S)
        seb = np.sqrt(c * (Vj ** 2).sum(1))
        cuenta += int(np.sum(np.abs((bs[:, j] - b0) / seb) >= abs(t_obs) - 1e-12))
        # WCU: residuos sin restringir, centrado en b (percentil-t)
        fit_u = (Zf @ b).reshape(G, T)
        yu = desmedia2(fit_u[None] + w[:, :, None] * e[None])
        bu = np.einsum("kf,bf->bk", Ainv @ Zf.T, yu.reshape(n, -1))
        eu = yu - np.einsum("gtk,bk->bgt", Z, bu)
        Su = np.einsum("gtk,bgt->bgk", Z, eu)
        Vu = np.einsum("k,bgk->bg", Ainv[j], Su)
        seu = np.sqrt(c * (Vu ** 2).sum(1))
        tb_u[r0:r0 + n] = (bu[:, j] - b[j]) / seu
    p = cuenta / B
    lo, hi = np.quantile(tb_u, [0.025, 0.975])
    return p, (float(b[j] - hi * se[j]), float(b[j] - lo * se[j]))


def construir():
    t, a = leer_incasol()
    cov = leer_covariables()
    tr = pd.read_csv(RAIZ / "data/raw/v3/cataluna_contencion_rentas_v3.csv", dtype=str)
    tratados = set(tr[tr.regimen == "ley11_2020"].cod_ine) - {BARCELONA}
    P = t[t.periodo_iso.isin(QS)]
    ok = P.dropna(subset=["renda"])
    ok = ok[ok.habitatges >= 1]
    n = ok.groupby("codi_territorial").size()
    equil = set(n[n == len(QS)].index) - {BARCELONA}
    # crecimiento 2014-2019: renta anual 2014 y media ponderada por contratos de los trimestres de 2019
    r14 = a[a.anio == "2014"].set_index("codi_territorial")["renda"]
    p19 = P[P.periodo_iso.str.startswith("2019")].dropna(subset=["renda"])
    r19 = (p19.assign(w=p19.renda * p19.habitatges).groupby("codi_territorial").w.sum() / p19.groupby("codi_territorial").habitatges.sum())
    g = ((r19 / r14) ** (1 / 5) - 1).dropna()
    controles = {m for m in equil - tratados if m in g.index and g[m] > 0.0415}
    trat = equil & tratados
    muni = sorted(trat | controles)
    W = P.pivot(index="codi_territorial", columns="periodo_iso", values="renda").loc[muni, QS]
    Y = np.log(W.to_numpy(float))
    reg = np.array([m in trat for m in muni], float)
    post = np.array([1.0 if q >= "2020T4" else 0.0 for q in QS])
    ant = np.array([1.0 if q == "2020T3" else 0.0 for q in QS])
    D = reg[:, None] * post[None, :]
    TH = reg[:, None] * ant[None, :]
    anio = [q[:4] for q in QS]
    lu = np.log1p(cov["paro_trim"].reindex(muni)[QS].to_numpy(float))
    return muni, trat, controles, Y, D, TH, lu, g


def estimar(Y, D, TH, covs, B, rng):
    sin_th = float(np.abs(TH).sum()) == 0.0
    comps = ([D] if sin_th else [D, TH]) + covs
    keep = np.all([np.isfinite(c).all(1) for c in comps] + [np.isfinite(Y).all(1)], axis=0)
    Z = np.stack([desmedia2(c[keep]) for c in comps], axis=-1)
    y = desmedia2(Y[keep])
    b, se, e, A, c = ols_cr1(y, Z)
    p_w, ic_w = wild_webb(y, Z, 0, B, rng)
    return {"beta": float(b[0]), "se_cr1_municipio": float(se[0]), "ic95_cr1": [float(b[0] - 1.96 * se[0]), float(b[0] + 1.96 * se[0])],
            "p_webb_wcr": float(p_w), "ic95_webb_wcu": list(ic_w), "theta_anticipacion": None if sin_th else float(b[1]), "se_theta": None if sin_th else float(se[1]),
            "n_municipios": int(keep.sum()), "N": int(keep.sum() * Y.shape[1])}


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    muni, trat, controles, Y, D, TH, lu, g = construir()
    nt, nc = len(trat), len(controles)
    out = {"rama": "replica_ciega_v18", "pregunta": "E2-R1: efecto de la Ley 11/2020 sobre ln renta media de contratos nuevos (Incasòl)",
           "capa": "C4", "rotulo": "réplica ciega V18; capa C4",
           "datos": "Incasòl municipio-trimestre 2019T1-2022T1 (renta, contratos; sellado.filtrar); paro SEPE mensual->trimestral",
           "n_tratados": nt, "n_controles": nc, "minimo_30_30": bool(nt >= 30 and nc >= 30)}
    if not out["minimo_30_30"]:
        # regla de la adenda 1.3: por debajo del mínimo de datos la especificación es NO ESTIMABLE; se estima igualmente y se rotula
        out["aviso_minimo"] = "tratados o controles < 30: NO ESTIMABLE por la adenda 1.3; se publica la estimación solo como réplica"
    rng = np.random.default_rng(SEED)
    pr = estimar(Y, D, TH, [lu], 9999, rng)
    sc = estimar(Y, D, TH, [], 9999, np.random.default_rng(SEED))
    # variante: sin 2020T1-2020T3 en el periodo previo (v1) -> se quitan esas columnas de Y/D/TH
    cols = [i for i, q in enumerate(QS) if q not in ("2020T1", "2020T2", "2020T3")]
    v1 = estimar(Y[:, cols], D[:, cols], TH[:, cols], [lu[:, cols]], 9999, np.random.default_rng(SEED))
    out.update({
        "N": pr["N"], "metodo": "DiD TWFE (efectos municipio y trimestre), cluster municipio; Webb WCR/WCU 9.999; SEED 20261010",
        "estimacion": pr["beta"], "ic95": pr["ic95_webb_wcu"], "ic95_cr1": pr["ic95_cr1"], "se_cr1_municipio": pr["se_cr1_municipio"],
        "p_webb": pr["p_webb_wcr"], "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO",
        "clasificacion_v18": "no se clasifica (réplica ciega)",
        "diagnosticos": {"principal": pr, "sin_covariables_v5": sc, "sin_2020T1_T3_v1": v1,
                         "crecimiento_control_mediana": float(np.median([g[m] for m in controles])),
                         "comarca": "no disponible en el repositorio: cluster por municipio en lugar de comarca (adenda, 42 comarcas)",
                         "erte": "no disponible: omitido", "barcelona": "excluida (principal de la adenda)"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Episodio histórico: nunca C3. Los parcialmente tratados y las entradas/salidas del régimen no se pueden identificar con el fichero: declarado.",
    })
    (SALIDA / "resultado.json").write_text(json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print(nt, nc, json.dumps({"principal": pr, "sin_cov": sc, "v1": v1}, indent=1))


if __name__ == "__main__":
    main()
