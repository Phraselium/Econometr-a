"""M3a v6: modelo jerárquico con coeficientes variables por territorio.
Sin PyMC ni NumPyro instalados: SUSTITUTO DECLARADO = modelo mixto (statsmodels MixedLM, REML), no bayesiano pleno.
dy = y - y_lag1 ~ efectos fijos (y_lag1, dy_lag1, regresores) + intercepto y pendientes aleatorias por territorio
(CCAA en provincia; provincia en municipio y distrito). Predicción: efectos fijos + BLUP del territorio (si se vio)."""
import pickle
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m3a_lib as L  # noqa: E402

warnings.filterwarnings("ignore")
FIJOS = {"provincia": ["y_lag1", "dy_lag1", "ln_pob", "share_ext_pob", "ln_pib_pc", "ln_terminadas_libres",
                       "ln_iniciadas_libres", "n_mun_topes_cat"],
         "municipio": ["y_lag1", "dy_lag1", "ln_pob", "share_ext_pob", "ln_pib_pc", "ln_terminadas_libres",
                       "ln_iniciadas_libres", "tensionada_mun", "tope_cat_mun"],
         "distrito": ["y_lag1", "dy_lag1", "ln_pib_pc"]}
ALEAT = {"provincia": ["y_lag1", "ln_pob"], "municipio": ["y_lag1", "dy_lag1"], "distrito": ["y_lag1", "dy_lag1"]}
GRUPO = {"provincia": "ccaa", "municipio": "cod_prov", "distrito": "cod_prov"}


def ajustar(nivel, tr, aleat=None):
    import statsmodels.formula.api as smf
    fx, ra, g = FIJOS[nivel], ALEAT[nivel] if aleat is None else aleat, GRUPO[nivel]
    t = tr.dropna(subset=fx + ["dy"]).copy()
    fx = [c for c in fx if t[c].std() > 1e-9]  # sin varianza en el entrenamiento del pliegue: se omite
    ra = [a for a in ra if a in fx]
    f = "dy ~ " + " + ".join(fx)
    mod = smf.mixedlm(f, t, groups=t[g], re_formula="~" + " + ".join(ra) if ra else "~1")
    try:
        r = mod.fit(method="lbfgs", reml=True, maxiter=200)
        if not np.isfinite(r.llf):
            raise ValueError
    except Exception:
        ra = []
        r = smf.mixedlm(f, t, groups=t[g]).fit(method="lbfgs", reml=True)
    return {"res_fe": r.fe_params.to_dict(), "re": {k: v.to_dict() for k, v in r.random_effects.items()},
            "fijos": fx, "aleat": ra, "grupo": g, "cov_re": np.asarray(r.cov_re).tolist(),
            "convergido": bool(r.converged), "n": int(len(t)), "n_grupos": int(t[g].nunique())}


def predecir_obj(m, va):
    fe = m["res_fe"]
    X = va[m["fijos"]].to_numpy(float)
    b = np.array([fe[c] for c in m["fijos"]])
    out = fe["Intercept"] + X @ b
    for i, gv in enumerate(va[m["grupo"]]):
        re = m["re"].get(gv)
        if re is not None:
            out[i] += re.get("Group", 0.0) + sum(re.get(a, 0.0) * va[a].iloc[i] for a in m["aleat"])
    ok = va[m["fijos"]].notna().all(axis=1).to_numpy()
    out[~ok] = np.nan
    return va.y_lag1.to_numpy(float) + out


def predecir_mixto(ruta, obj):
    with open(ruta, "rb") as f:
        m = pickle.load(f)
    p = predecir_obj(m, obj)
    return np.where(np.isnan(p), obj.y_lag1.to_numpy(float), p)  # sin rasgos completos -> persistencia (declarado)


def main():
    import json
    out = L.OUT
    preds, fin, reg = [], [], []
    for nivel in ("provincia", "municipio", "distrito"):
        P = L.cargar(nivel)
        P["unit_g"] = P[GRUPO[nivel]]
        anio_max = int(P.dropna(subset=["y"]).anio.max())
        for o, ymax, vanios in L.pliegues(nivel, anio_max):
            tr = P[(P.anio <= ymax)].dropna(subset=["y"])
            va = P[P.anio.isin(vanios)].dropna(subset=["y", "y_lag1"])
            m = ajustar(nivel, tr)
            p = predecir_obj(m, va)
            b = va[["unit", "anio", "y", "y_lag1", "cod_prov", "ccaa"]].copy()
            preds.append(b.assign(origen=o, nivel=nivel, modelo="mixto_jerarquico", pred=p))
        m = ajustar(nivel, P.dropna(subset=["y"]))
        mid = f"alquiler_{nivel}_mixto"
        with open(out / "modelos" / f"{mid}.pkl", "wb") as f:
            pickle.dump(m, f, protocol=4)
        cols = sorted(set(FIJOS[nivel] + [GRUPO[nivel]]))
        ficha = {"id": mid, "mercado": "alquiler de stock (SERPAVI)", "nivel": nivel, "medida": L.YCOL[nivel],
                 "familia": "mixto", "variables": cols, "objetivo": "dy; prediccion = y_lag1 + fijos + BLUP territorio",
                 "hiperparametros": {"fijos": FIJOS[nivel], "pendientes_aleatorias": m["aleat"], "grupo": GRUPO[nivel]},
                 "semilla": L.SEED, "ruta_modelo": f"modelos/{mid}.pkl", "convergido": m["convergido"], "n": m["n"],
                 "sustituto": "MixedLM (REML) en lugar de PyMC/NumPyro (no instalados)",
                 "funcion_prediccion": "src/v6/m3a_lib.predecir_modelo(id, {nombre: DataFrame sellado})",
                 "nombres_paneles": L.NOMBRES[nivel]}
        (out / "modelos" / f"{mid}.json").write_text(json.dumps(ficha, indent=1, ensure_ascii=False))
        fin.append({k: ficha[k] for k in ("id", "nivel", "medida", "familia")} | {"mercado": "alquiler", "ruta": f"output/v6/M3A/modelos/{mid}.json"})
        reg.append({"nivel": nivel, "familia": "mixto", "config_id": 0, "config": json.dumps(ficha["hiperparametros"]),
                    "rmse_bloques_espaciotemporales": np.nan, "n_bloques": 0, "estado": "1 especificacion (sin busqueda); cuenta en el Registry"})
        sd = np.sqrt(np.diag(np.asarray(m["cov_re"]))).round(4).tolist()
        print(nivel, "mixto", m["convergido"], m["n"], m["n_grupos"], sd, flush=True)
        # pendientes por territorio (coeficientes variables) a CSV
        pd.DataFrame(m["re"]).T.round(5).to_csv(out / f"mixto_efectos_territorio_{nivel}.csv")
    pd.concat(preds).to_csv(out / "predicciones_cv_mixto.csv.gz", index=False)
    (out / "modelos_finales_mixto.json").write_text(json.dumps(fin, indent=1, ensure_ascii=False))
    pd.DataFrame(reg).to_csv(out / "registro_mixto.csv", index=False)


if __name__ == "__main__":
    main()
