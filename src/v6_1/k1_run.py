"""K1 (v6.1): lineas base exigentes. Reanalisis de la validacion sellada v6. Entra en make.

Lee SOLO JSON/CSV versionados: output/v6/M4/sellado_*.json (modelos y lineas base de v6), output/v6_1/K1/sellado_*.json
(lineas base nuevas, evaluadas por src/v6/m4_lineas_base.py con evaluate_v6, ids k1_*) y output/v6/M4/mejor_modelo.csv.
No abre data/sealed. Sin red; SEED=20261010; un hilo. Capa maxima C4 (prediccion, no causalidad).

Para cada tarea y grupo (espacial, temporal, conjunta, total), en las MISMAS filas (celdas provincia-periodo):
  - RMSE (log-puntos x100, aprox. %).
  - Linea base mas exigente = menor RMSE espacial entre persistencia, AR por unidad, ECM v1, M1 econ y las tres nuevas
    en su variante FACTIBLE. Las variantes oraculo (usan el factor del periodo objetivo, no conocible al predecir) se
    reportan aparte y no definen la base exigente.
  - Diebold-Mariano con correccion de muestra pequena de Harvey-Leybourne-Newbold (h=1, perdida cuadratica, celdas
    provincia-periodo y, por separado, agregado por periodo) y test de permutacion por inversion de signo de la diferencia de
    perdidas por provincia (10.000 permutaciones, SEED), ambos de una cola; Holm dentro de cada tarea y grupo.
  - Clase: "predice mejor que la base mas exigente" solo si RMSE menor y p_holm < 0,05 en DM-HLN Y en permutacion en el grupo
    ESPACIAL; "peor" si la base es mejor con p_holm < 0,05 en ambos; si no, "no distinguible".
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry  # noqa: E402

SEED = 20261010
NPERM = 10000
V6 = RAIZ / "output/v6/M4"
K1 = RAIZ / "output/v6_1/K1"
FECHA = "2026-10-11"
GRUPOS = ("espacial", "temporal", "conjunta", "total")
BASES_V6 = ("persistencia", "ar_unidad", "ecm_v1", "m1_econ")
BASES_FAC = BASES_V6 + ("ult_crec_nac_fac", "ar_factor_fac", "twfe_fac")
BASES_ORA = ("ult_crec_nac_ora", "ar_factor_ora", "twfe_ora")
CL_MEJOR, CL_NO, CL_PEOR = "predice mejor que la base mas exigente", "no distinguible", "peor"
REG = Registry(K1 / "registro.csv")
_SIGNOS = {}


def signos(n):
    if n not in _SIGNOS:
        _SIGNOS[n] = np.random.default_rng(SEED).choice(np.array([-1.0, 1.0]), size=(NPERM, n))
    return _SIGNOS[n]


def dm_hln(d):
    """DM-HLN (h=1) sobre la serie de diferencias de perdida d = L_modelo - L_base. Devuelve (estadistico, p_mejor, p_peor)."""
    d = np.asarray(d, float)
    n = len(d)
    if n < 3 or np.allclose(d, 0):
        return np.nan, np.nan, np.nan
    dc = d - d.mean()
    lrv = dc @ dc / n
    if lrv <= 0:
        return np.nan, np.nan, np.nan
    st = d.mean() / np.sqrt(lrv / n) * np.sqrt((n - 1) / n)
    return float(st), float(stats.t.cdf(st, n - 1)), float(stats.t.sf(st, n - 1))


def perm_prov(c):
    """Permutacion por inversion de signo de la diferencia de perdidas por provincia. Devuelve (n_prov, p_mejor, p_peor)."""
    dp = c.groupby("cod_prov").apply(lambda x: (x.sse - x.sse_b).sum() / x.n.sum(), include_groups=False).to_numpy(float)
    k = len(dp)
    if k < 3 or np.allclose(dp, 0):
        return k, np.nan, np.nan
    obs = dp.mean()
    pm = (signos(k) @ dp) / k
    p_mejor = (1 + np.sum(pm <= obs + 1e-15)) / (1 + NPERM)
    p_peor = (1 + np.sum(pm >= obs - 1e-15)) / (1 + NPERM)
    return k, float(p_mejor), float(p_peor)


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(np.where(np.isnan(p), 2, p))
    m = int(np.sum(~np.isnan(p)))
    out = np.full(len(p), np.nan)
    run = 0.0
    for r, i in enumerate(o[:m]):
        run = max(run, (m - r) * p[i])
        out[i] = min(1.0, run)
    return out


def carga():
    mod = {}
    for carpeta in (V6, K1):
        for f in sorted(carpeta.glob("sellado_*.json")):
            d = json.loads(f.read_text())
            if d.get("estado") == "evaluado":
                d["clave"] = d["modelo"] if d["rol"] == "base" else d["modelo_id"]
                mod[(d["tarea"], d["clave"])] = d
    return mod


def celdas(d, g):
    c = pd.DataFrame(d["celdas"])
    c = c if g == "total" else c[c.grupo == g]
    return c[["cod_prov", "per", "grupo", "n", "sse"]]


def comparar(dm_, db_, g):
    """Modelo contra base en las mismas celdas. Devuelve dict con DM-HLN (celda y periodo) y permutacion."""
    cm, cb = celdas(dm_, g), celdas(db_, g)
    c = cm.merge(cb, on=["cod_prov", "per", "grupo"], suffixes=("", "_b")).sort_values(["per", "cod_prov"])
    if len(c) < 3:
        return dict(n_celdas=len(c))
    st, pm, pp = dm_hln(c.sse / c.n - c.sse_b / c.n_b)
    pa = c.assign(l=c.sse / c.n, lb=c.sse_b / c.n_b).groupby("per")[["l", "lb"]].mean()
    stp, pmp, ppp = dm_hln(pa.l - pa.lb)
    k, qm, qp = perm_prov(c)
    return dict(n_celdas=len(c), n_prov=k, dm=st, p_mejor=pm, p_peor=pp, dm_per=stp, p_mejor_per=pmp, p_peor_per=ppp,
                p_perm_mejor=qm, p_perm_peor=qp)


def md_tabla(df, cols, dec=4):
    def f(x):
        if isinstance(x, (float, np.floating)):
            return "" if pd.isna(x) else f"{x:.{dec}f}"
        return str(x)
    cab = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    return cab + "\n".join("| " + " | ".join(f(r[c]) for c in cols) + " |" for _, r in df.iterrows()) + "\n"


def main():
    mod = carga()
    mejor_v6 = pd.read_csv(V6 / "mejor_modelo.csv").set_index("tarea")
    tareas = sorted({t for t, _ in mod})
    largo, resumen = [], []
    for tid in tareas:
        ms = {k: d for (t, k), d in mod.items() if t == tid}
        modelos = {k: d for k, d in ms.items() if d["rol"] == "modelo"}
        if not modelos:
            continue
        info = next(iter(ms.values()))
        faltan = [b for b in BASES_FAC if b not in ms]
        if faltan:
            raise SystemExit(f"{tid}: faltan lineas base {faltan}; ejecutar src/v6/m4_lineas_base.py --real")
        rm = lambda d, g: d["metricas"][g]["rmse"]  # noqa: E731
        # linea base mas exigente (factible) y mejor oraculo, por RMSE espacial
        exig = min(BASES_FAC, key=lambda b: rm(ms[b], "espacial"))
        orac = min(BASES_ORA, key=lambda b: rm(ms[b], "espacial"))
        filas_t = []
        for g in GRUPOS:
            ref = {"exigente": exig, "ar_unidad": "ar_unidad", "oraculo": orac}
            res = {}
            for etq, b in ref.items():
                lst = []
                for k, d in modelos.items():
                    if not d["metricas"][g]["n"] or not ms[b]["metricas"][g]["n"]:
                        continue
                    r = comparar(d, ms[b], g)
                    r.update(modelo_id=k, base=b, ref=etq, grupo=g, rmse_modelo=rm(d, g), rmse_base=rm(ms[b], g))
                    lst.append(r)
                if lst:
                    L = pd.DataFrame(lst)
                    for c in ("p_mejor", "p_peor", "p_perm_mejor", "p_perm_peor", "p_mejor_per"):
                        if c in L:
                            L[c + "_holm"] = holm(L[c].to_numpy())
                    res[etq] = L
            for etq, L in res.items():
                for r in L.itertuples():
                    d = {**r._asdict(), "tarea": tid}
                    d.pop("Index", None)
                    largo.append(d)
                    REG.log("K1_OOS_SELLADA", f"{tid}__{r.modelo_id}|{g}|vs_{etq}:{r.base}",
                            f"DM-HLN y permutacion de {r.modelo_id} contra {r.base}; {info['nivel']}; {info['medida']}", "", "", int(r.n_celdas),
                            np.nan, np.nan, np.nan, r.rmse_modelo, getattr(r, "dm", np.nan), getattr(r, "p_mejor_holm", np.nan),
                            f"medida_precio={info['medida_precio']}; p_perm_holm={getattr(r, 'p_perm_mejor_holm', np.nan)}; ref={etq}")
        # clase por modelo (grupo espacial y resto de grupos)
        L = pd.DataFrame([d for d in largo if d["tarea"] == tid and d["ref"] == "exigente"])
        L["clase"] = np.where((L.rmse_modelo < L.rmse_base) & (L.p_mejor_holm < 0.05) & (L.p_perm_mejor_holm < 0.05), CL_MEJOR,
                              np.where((L.rmse_modelo > L.rmse_base) & (L.p_peor_holm < 0.05) & (L.p_perm_peor_holm < 0.05), CL_PEOR, CL_NO))
        for i in L.index:
            largo_idx = [j for j, d in enumerate(largo) if d["tarea"] == tid and d["ref"] == "exigente"
                         and d["modelo_id"] == L.loc[i, "modelo_id"] and d["grupo"] == L.loc[i, "grupo"]]
            largo[largo_idx[0]]["clase"] = L.loc[i, "clase"]
        esp = L[L.grupo == "espacial"].sort_values("rmse_modelo")
        b = esp.iloc[0]
        fila = dict(tarea=tid, mercado=info["mercado"], medida_precio=info["medida_precio"], nivel=info["nivel"],
                    mejor_modelo=b.modelo_id, base_exigente=exig, rmse_pct_modelo=100 * b.rmse_modelo, rmse_pct_base=100 * b.rmse_base,
                    ratio=b.rmse_modelo / b.rmse_base, p_dm_hln_holm=b.p_mejor_holm, p_perm_holm=b.p_perm_mejor_holm,
                    p_dm_hln_per_holm=b.p_mejor_per_holm, clase=b.clase, n_celdas=int(b.n_celdas), n_prov=int(b.n_prov),
                    rmse_pct_persistencia=100 * rm(ms["persistencia"], "espacial"), rmse_pct_ar_unidad=100 * rm(ms["ar_unidad"], "espacial"),
                    rmse_pct_ecm_v1=100 * rm(ms["ecm_v1"], "espacial"), base_oraculo=orac,
                    rmse_pct_base_oraculo=100 * rm(ms[orac], "espacial"), ratio_vs_oraculo=b.rmse_modelo / rm(ms[orac], "espacial"),
                    n_modelos_m3_mejor_que_base=int((esp.clase == CL_MEJOR).sum()), n_modelos_m3=int(len(esp)))
        for g in GRUPOS[1:]:
            x = L[(L.grupo == g) & (L.modelo_id == b.modelo_id)]
            if len(x):
                x = x.iloc[0]
                bx = min(BASES_FAC, key=lambda bb: rm(ms[bb], g))
                fila.update({f"ratio_{g}": x.rmse_modelo / x.rmse_base, f"clase_{g}": x.clase, f"base_exigente_{g}": x.base,
                             f"p_dm_hln_holm_{g}": x.p_mejor_holm, f"p_perm_holm_{g}": x.p_perm_mejor_holm, f"base_menor_rmse_{g}": bx})
        if tid in mejor_v6.index:
            mv = mejor_v6.loc[tid]
            fila.update(v6_m3_bate_persistencia=bool(mv.m3_bate_persistencia), v6_m3_bate_ar=bool(mv.m3_bate_ar),
                        v6_m3_bate_ecm=bool(mv.m3_bate_ecm))
        # dm vs AR por unidad del mejor modelo (para fuera_muestra)
        ar = [d for d in largo if d["tarea"] == tid and d["ref"] == "ar_unidad" and d["grupo"] == "espacial" and d["modelo_id"] == b.modelo_id]
        if ar:
            fila.update(dm_vs_ar=ar[0].get("dm"), p_holm_vs_ar=ar[0].get("p_mejor_holm"))
        resumen.append(fila)
    REG.flush()
    K1.mkdir(parents=True, exist_ok=True)
    LG = pd.DataFrame(largo)
    LG.to_csv(K1 / "tabla_largo_k1.csv", index=False)
    R = pd.DataFrame(resumen)
    R.to_csv(K1 / "tabla_modelos_k1.csv", index=False)
    escribir_md(R, LG)
    escribir_json(R, mod, tareas)
    print(f"k1_run: {len(R)} tareas; clase espacial: " + "; ".join(f"{r.tarea}={r.clase}" for r in R.itertuples()))
    return 0


def escribir_md(R, LG):
    md = ["# K1: modelos de v6 frente a lineas base exigentes (validacion sellada v6)\n",
          f"Fecha: {FECHA}. Segunda mirada a la misma muestra sellada para NUEVOS comparadores (las predicciones de los modelos de v6 no cambian). "
          "Error en log-puntos x100 (aprox. %). La base exigente es la de menor RMSE espacial entre persistencia, AR por unidad, ECM v1, "
          "M1 econ y las tres nuevas en su variante factible. DM-HLN y permutacion de una cola (a favor del modelo), Holm por tarea y grupo; "
          "11 provincias selladas: poca potencia.\n", "## Resultado por tarea (grupo espacial)\n",
          md_tabla(R, ["tarea", "medida_precio", "mejor_modelo", "base_exigente", "rmse_pct_modelo", "rmse_pct_base", "ratio",
                       "p_dm_hln_holm", "p_perm_holm", "clase"]),
          "## Otros grupos (mejor modelo espacial contra su base exigente espacial)\n",
          md_tabla(R, ["tarea", "ratio_temporal", "clase_temporal", "ratio_conjunta", "clase_conjunta", "ratio_total", "clase_total"]),
          "## Variante oraculo (factor del periodo objetivo, no conocible al predecir; solo informativa)\n",
          md_tabla(R, ["tarea", "base_oraculo", "rmse_pct_base_oraculo", "rmse_pct_modelo", "ratio_vs_oraculo"]),
          "## Referencias v6 (mejor M3 bate segun v6)\n",
          md_tabla(R, ["tarea", "rmse_pct_persistencia", "rmse_pct_ar_unidad", "rmse_pct_ecm_v1", "v6_m3_bate_persistencia",
                       "v6_m3_bate_ar", "v6_m3_bate_ecm", "n_modelos_m3_mejor_que_base", "n_modelos_m3"])]
    (K1 / "tabla_modelos_k1.md").write_text("\n".join(md))


def escribir_json(R, mod, tareas):
    n_mej = int((R.clase == CL_MEJOR).sum())
    h = R[R.tarea == "alq_provincia"].iloc[0]
    res = dict(
        rama="v6_1/K1", modulo="K1",
        pregunta="Que modelos de v6 siguen prediciendo mejor, en la misma validacion sellada, cuando la referencia es la linea base mas exigente?",
        capa="C4",
        medida_precio={"principal": "valor tasado MIVAU (provincia, municipio)", "robustez": ["Registradores (provincia anual)"],
                       "alquiler": "no aplica (SERPAVI, stock)"},
        datos="output/v6/M4/sellado_*.json y output/v6_1/K1/sellado_*.json (evaluate_v6, ids k1_*)",
        N={"tareas": int(len(R)), "provincias_selladas": 11, "celdas_espaciales_min": int(R.n_celdas.min())},
        metodo=("RMSE, DM-HLN (celdas provincia-periodo y agregado por periodo), permutacion por inversion de signo por provincia "
                "(10.000, SEED=20261010) y Holm; base exigente = menor RMSE espacial entre 7 bases factibles."),
        estimacion=R[["tarea", "mejor_modelo", "base_exigente", "rmse_pct_modelo", "rmse_pct_base", "ratio", "clase"]].to_dict("records"),
        ic95=None, p_ajustado="Holm por tarea y grupo (DM-HLN y permutacion; tabla_largo_k1.csv)",
        nivel_evidencia="EXPLORATORIO (C4): prediccion, no causalidad",
        diagnosticos={"clases": R.clase.value_counts().to_dict(), "n_tareas_mejor_que_base_exigente": n_mej,
                      "variante_oraculo": "usa el factor del periodo objetivo (no conocible al predecir); solo informativa"},
        fuera_muestra={"modelo": h.mejor_modelo, "rmse": float(h.rmse_pct_modelo / 100),
                       "dm_vs_ar4": {"DM_HLN": None if pd.isna(h.get("dm_vs_ar")) else float(h.dm_vs_ar),
                                     "p_holm": None if pd.isna(h.get("p_holm_vs_ar")) else float(h.p_holm_vs_ar),
                                     "grupo": "espacial sellado; alquiler provincia; AR por unidad"}},
        notas=("Capa C4. Segunda mirada a la misma muestra sellada para nuevos comparadores; 11 provincias selladas, poca potencia. "
               "El 'mejor modelo' se elige por RMSE sellado (optimista). Ver notas.md. Fecha: " + FECHA))
    (K1 / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    hechos = []
    for r in R.itertuples():
        med = f", medida de precio: {r.medida_precio}" if isinstance(r.medida_precio, str) else ""
        base = dict(min=None, max=None, periodo="validacion sellada v6 (11 provincias, grupo espacial)", cobertura=f"{r.n_celdas} celdas provincia-periodo",
                    fuentes=["output/v6_1/K1/tabla_modelos_k1.csv"], capa="C4", fecha_dato=FECHA)
        hechos.append(dict(id=f"K1-RMSE-{r.tarea}", indicador=f"RMSE espacial sellado del mejor modelo ({r.mejor_modelo}), {r.mercado}, {r.nivel}{med}",
                           valor=round(float(r.rmse_pct_modelo), 3), unidad="log-puntos x100 (aprox. %)", **base))
        hechos.append(dict(id=f"K1-BASE-{r.tarea}", indicador=f"RMSE espacial sellado de la base mas exigente ({r.base_exigente}), {r.mercado}, {r.nivel}{med}",
                           valor=round(float(r.rmse_pct_base), 3), unidad="log-puntos x100 (aprox. %)", **base))
        hechos.append(dict(id=f"K1-RATIO-{r.tarea}", indicador=f"Cociente de RMSE espacial, mejor modelo / base mas exigente, {r.mercado}, {r.nivel}{med}",
                           valor=round(float(r.ratio), 3), unidad="cociente", **base))
    hechos.append(dict(id="K1-N-MEJOR", indicador="Tareas en que el mejor modelo predice mejor que la base mas exigente (DM-HLN y permutacion, Holm, grupo espacial)",
                       valor=n_mej, min=None, max=None, unidad="tareas", periodo="validacion sellada v6", cobertura=f"{len(R)} tareas",
                       fuentes=["output/v6_1/K1/tabla_modelos_k1.csv"], capa="C4", fecha_dato=FECHA))
    (K1 / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1, default=float))


if __name__ == "__main__":
    sys.exit(main())
