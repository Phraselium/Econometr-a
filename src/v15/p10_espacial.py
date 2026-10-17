"""V15-B · E3 (P10): dependencia espacial del crecimiento del alquiler municipal (Δlog SERPAVI VC 2011-2019 y 2015-2024). SAR/SEM/SDM APTO
(Wald de ρ/λ y efectos indirectos por simulación). Estimadores importados de src/v15/montecarlo/sar_sdm.py. Sin Conley (no figura en la tabla). Solo entrenamiento.
Uso: python3 src/v15/p10_espacial.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from shapely import wkb  # noqa: E402
from shapely.strtree import STRtree  # noqa: E402

from src.v15.montecarlo import _comun_v15 as C  # noqa: E402
from src.v15.montecarlo import sar_sdm as S  # noqa: E402
from src.v15.pb_comun import GRANDES_MUN, OUT, ROOT, SEED, Registry, cargar, escribe_json, hecho, resultado_base  # noqa: E402

CARPETA = OUT / "p10"


def muestra(a0, a1):
    d = cargar("p10_espacial", nivel="municipio")
    v = d[(d.variable == "serpavi_alquiler_m2_mediana") & (d.desagregacion == "tipologia=VC") & d.periodo.isin([str(a0), str(a1)])]
    n = d[(d.variable == "serpavi_n_contratos_recuento") & (d.desagregacion == "tipologia=VC") & (d.periodo == str(a0))]
    w = v.pivot_table(index="territorio_codigo", columns="periodo", values="valor").dropna()
    w = w[(w > 0).all(axis=1)]
    nn = n.drop_duplicates("territorio_codigo").set_index("territorio_codigo").valor
    w = w.join(nn.rename("n0"), how="inner")
    w = w[w.n0 > 0]
    return pd.DataFrame({"dy": np.log(w[str(a1)]) - np.log(w[str(a0)]), "lr0": np.log(w[str(a0)]), "ln0": np.log(w.n0)})


def mallas(cods):
    g = pd.read_parquet(ROOT / "data" / "base" / "geo" / "municipios.parquet", columns=["cod_municipio", "geometry"])
    g["cod"] = g.cod_municipio.astype(str).str.zfill(5)
    g = g[g.cod.isin(cods)].drop_duplicates("cod").sort_values("cod").reset_index(drop=True)
    geoms = [wkb.loads(b) for b in g.geometry]
    cen = np.array([[q.centroid.y, q.centroid.x] for q in geoms])
    tree = STRtree(geoms)
    n = len(g)
    A = np.zeros((n, n))
    for i, q in enumerate(geoms):
        for j in tree.query(q, predicate="intersects"):
            if j != i:
                A[i, j] = 1.0
    d = C.dist_km(cen)
    B = np.where((d < 25.0) & (d > 0), 1.0 / np.maximum(d, 1e-6), 0.0)
    ok = (A.sum(1) > 0) & (B.sum(1) > 0)
    while True:
        ok2 = (A[np.ix_(ok, ok)].sum(1) > 0) & (B[np.ix_(ok, ok)].sum(1) > 0)
        if ok2.all():
            break
        ok[np.where(ok)[0][~ok2]] = False
    A, B = A[np.ix_(ok, ok)], B[np.ix_(ok, ok)]
    return list(g.cod[ok]), {"contigüidad": (A, A / A.sum(1, keepdims=True)), "dist_inversa_25km": (B, B / B.sum(1, keepdims=True))}, cen[ok]


def ajusta_celda(df, W, A, modelo, rng):
    X = np.column_stack([np.ones(len(df)), df.lr0.values, df.ln0.values])
    y = df.dy.values
    lam = S.autovalores(W, np.sqrt(A.sum(1)))
    M = S.Malla(W, X, modelo, lam)
    a = S.ajusta(M, y)
    z = a["par"] / a["se"] if np.isfinite(a["se"]) else np.nan
    out = {"modelo": modelo, "rho_o_lambda": float(a["par"]), "se": float(a["se"]), "z": float(z), "p_wald": float(2 * stats.norm.sf(abs(z))) if np.isfinite(z) else None,
           "lr": float(a["lr"]), "p_lr": float(stats.chi2.sf(a["lr"], 1)), "n": len(y)}
    if modelo in ("SAR", "SDM"):
        for cual, nom in ((1, "log_alquiler_inicial"), (2, "log_contratos_inicial")):
            ef = S.efectos(M, a, rng, cual=cual)
            if ef is not None:
                (il, ih), (dl, dh), im = ef
                out[f"indirecto_{nom}"] = {"mediana": im, "ic95_simulado": [float(il), float(ih)]}
                out[f"directo_{nom}_ic95"] = [float(dl), float(dh)]
    return out


def main():
    CARPETA.mkdir(parents=True, exist_ok=True)
    reg = Registry(CARPETA / "registro.csv")
    filas, pby, diag = [], [], {}
    rng = np.random.default_rng([SEED, 10])
    for (a0, a1) in ((2015, 2024), (2011, 2019)):
        df0 = muestra(a0, a1)
        cods, WW, cen = mallas(set(df0.index))
        df = df0.loc[cods]
        X = np.column_stack([np.ones(len(df)), df.lr0.values, df.ln0.values])
        for nw, (A, W) in WW.items():
            Mo = S.moran_prep(W, X)
            zmo = S.moran_z(Mo, df.dy.values)
            diag[f"moran_{a0}_{a1}_{nw}"] = {"z_moran_residuos_MCO": float(zmo), "p_bilateral_normal": float(2 * stats.norm.sf(abs(zmo))), "n": len(df)}
            for modelo in ("SAR", "SEM", "SDM"):
                r = ajusta_celda(df, W, A, modelo, rng)
                idm = f"E3-{modelo}-{nw}-{a0}_{a1}"
                r.update({"id": idm, "W": nw, "periodo": f"{a0}-{a1}", "vecinos_medios": float((A > 0).sum(1).mean())})
                filas.append(r)
                reg.log("E3", idm, f"dlog SERPAVI VC {a0}-{a1} ~ 1+lr0+ln0; {modelo}; W={nw}", a0, a1, r["n"], np.nan, np.nan, np.nan, coef_interes=r["rho_o_lambda"], p_interes=r["p_wald"] or np.nan)
                pby.append({"id": idm, "p": r["p_wald"], "contraste": "Wald de rho/lambda (APTO)"})
        # exclusión de grandes ciudades (principal: SAR, contigüidad, 2015-2024)
        if (a0, a1) == (2015, 2024):
            keep = ~df.index.isin(GRANDES_MUN)
            sub = df[keep]
            idx = np.where(keep)[0]
            A, W = WW["contigüidad"]
            A2, W2 = A[np.ix_(idx, idx)], None
            ok = A2.sum(1) > 0
            A2 = A2[np.ix_(ok, ok)]
            sub = sub[ok]
            W2 = A2 / A2.sum(1, keepdims=True)
            r = ajusta_celda(sub, W2, A2, "SAR", rng)
            diag["exclusion_Barcelona_Valencia_SAR_contiguidad_2015_2024"] = {k: r[k] for k in ("rho_o_lambda", "se", "p_wald", "n")}
    F = pd.DataFrame(filas)
    F.drop(columns=[c for c in F.columns if c.startswith(("indirecto", "directo"))]).to_csv(CARPETA / "multiverso.csv", index=False)
    pr = F[(F.id == "E3-SAR-contigüidad-2015_2024")].iloc[0]
    sig = F[F.modelo.isin(["SAR", "SEM"])]
    diag["multiverso_12"] = {"n": int(len(F)), "rho_lambda_min": float(F.rho_o_lambda.min()), "rho_lambda_max": float(F.rho_o_lambda.max()),
                             "frac_p_wald_lt_005_sin_ajustar": float((F.p_wald < 0.05).mean())}
    diag["herramientas"] = {"SAR/SDM/SEM": "APTO (K13): Wald de ρ y efectos indirectos", "Conley": "no figura en la tabla V15: no se usa"}
    diag["sdm_cota"] = "efectos indirectos del SDM dependen de W (limitación declarada)"
    res = resultado_base("r15/p10", "E3: ¿hay dependencia espacial en el crecimiento del alquiler municipal (SERPAVI VC)?", "data/processed/v15/p10_espacial.parquet (entrenamiento)",
                         int(pr.n), "SAR/SEM/SDM de máxima verosimilitud; W de contigüidad y de distancia inversa (25 km); Δlog SERPAVI VC",
                         {"rho_SAR_contiguidad_2015_2024": float(pr.rho_o_lambda), "se": float(pr.se)}, [float(pr.rho_o_lambda - 1.96 * pr.se), float(pr.rho_o_lambda + 1.96 * pr.se)],
                         "ASOCIACIÓN espacial (C4, exploratoria)", diag, {"modelo": None, "rmse": None, "dm_vs_ar4": None},
                         ["IC95 = ρ ± 1,96 EE (Wald, APTO). Efectos directo/indirecto en multiverso (resultado en este json, filas completas en detalle).", "Capa C4; pendiente de evaluación sellada."], pby,
                         extra={"detalle": filas})
    escribe_json(CARPETA / "resultado.json", res)
    escribe_json(CARPETA / "hechos.json", [hecho("V15-E3-rho", "Parámetro autorregresivo espacial ρ (SAR, contigüidad, Δlog SERPAVI VC 2015-2024)", round(float(pr.rho_o_lambda), 3),
                                                round(float(F.rho_o_lambda.min()), 3), round(float(F.rho_o_lambda.max()), 3), "ρ", "2015-2024", f"{int(pr.n)} municipios", "MIVAU SERPAVI", "rho", "p10")])
    print(F[["id", "rho_o_lambda", "se", "p_wald", "n"]].to_string())
    print(diag["multiverso_12"])


if __name__ == "__main__":
    main()
