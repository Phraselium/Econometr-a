"""K1 (v6.1): lineas base exigentes en la MISMA validacion sellada de v6. NO entra en make (como m4_sellado.py).

Uso:
  python3 src/v6/m4_lineas_base.py --dry [filtro ...]   ensayo con sellado FALSO (no abre data/sealed)
  python3 src/v6/m4_lineas_base.py --real               abre el sellado UNA vez por (linea base, tarea); escribe
                                                        output/v6_1/K1/sellado_<tarea>__<variante>.json

Mismas tareas, filas y grupos (espacial, temporal, conjunta, total) que m4_sellado.py (se reutilizan sus constructores).
Tres lineas base, cada una en dos variantes que salen de UNA sola apertura (id evaluate_v6 = k1_<tarea>__<linea>):
  ult_crec_nac : ultimo valor de la unidad x crecimiento nacional del periodo.
  ar_factor    : AR(1) en diferencias con factor comun, dy_it = a_i + b dy_i,t-1 + c f_t-1 (+ d f_t en oraculo).
  twfe         : efectos fijos de unidad y periodo sobre dy; prediccion y_t-1 + a_i + lambda_t.
Variantes: `fac` (factible: usa el factor f_t-1, ya conocido en t) y `ora` (oraculo: usa f_t, no conocible al predecir).
Factor f_t = media, entre las provincias NO selladas, de la media provincial de dy (cada provincia pesa igual; en municipio y
distrito se promedia primero dentro de la provincia). Es el factor NACIONAL (sin provincias selladas): para el grupo espacial
no existe factor provincial propio. Coeficientes SOLO con el entrenamiento (periodos < corte). Los valores del factor en periodos
>= corte (filas de provincias no selladas dentro de la ventana sellada) se usan solo como dato de entrada pasado (fac, f_t-1)
o realizado (ora, f_t), nunca para estimar. Efecto de unidad inexistente (provincia sellada o unidad nueva): media de los efectos
de unidad del entrenamiento (la CCAA tambien esta sellada entera, no hay efecto de CCAA). Sin prediccion posible -> persistencia
(contado en n_fallback_persistencia). Nunca reajusta con el sellado.
"""
from __future__ import annotations

import json
import sys
import traceback

import numpy as np
import pandas as pd

import m4_sellado as S  # noqa: E402  (fija rutas, hilos y Registry nulo)

holdout, RAIZ = S.holdout, S.RAIZ
OUT = RAIZ / "output/v6_1/K1"
LINEAS = {"ult_crec_nac": "ultimo valor x crecimiento nacional del periodo",
          "ar_factor": "AR(1) en dy con factor comun (estimado con entrenamiento)",
          "twfe": "efectos fijos de unidad y periodo sobre dy (entrenamiento)"}
VARIANTES = {"fac": "factible (factor/efecto del periodo t-1)", "ora": "oraculo (factor/efecto del periodo t, no conocible)"}


def prov_de(unit, largo):
    s = str(int(unit)) if str(unit).isdigit() else str(unit)
    return s.zfill(largo)[:2]


def preparar(t, T):
    """Devuelve (tr, va, allp): unit, per, y, y1, prov. `va` conserva el orden y las filas de T['va']."""
    if t["kind"] == "alq":
        tr, va = T["tr"].copy(), T["va"].copy()
        for d in (tr, va):
            d["per"] = d.anio.astype(int)
            d["y1"] = d["y_lag1"]
            d["unit"] = d.unit.astype(str)
    else:
        tr, va = T["tr"].copy(), T["va"].copy()
    largo = {"provincia": 2, "provincia (anual)": 2, "provincia (trimestral)": 2, "municipio": 5, "municipio (anual)": 5,
             "distrito": 7}[t["nivel"]]
    for d in (tr, va):
        d["prov"] = [prov_de(u, largo) for u in d.unit]
    cols = ["unit", "per", "y", "y1", "prov"]
    allp = pd.concat([tr[cols], va[cols]], ignore_index=True).drop_duplicates(["unit", "per"])
    return tr, va, allp


def factor(d, excluir):
    """f_t: media entre provincias no selladas de la media provincial de dy."""
    d = d[~d.prov.isin(excluir)].assign(dy=lambda x: x.y - x.y1).dropna(subset=["dy"])
    return d.groupby(["prov", "per"]).dy.mean().groupby("per").mean()


def lag2(df, ylook):
    idx = pd.MultiIndex.from_arrays([df.unit, df.per - 2])
    y2 = ylook.reindex(idx).to_numpy(float)
    return y2


def ajuste_intra(X, y, u):
    """Regresion con efecto fijo de unidad (transformacion intra). Devuelve b y los efectos a_i."""
    ug = pd.factorize(u)[0]
    Xm = pd.DataFrame(X).groupby(ug).transform("mean").to_numpy()
    ym = pd.Series(y).groupby(ug).transform("mean").to_numpy()
    b = np.linalg.lstsq(X - Xm, y - ym, rcond=None)[0]
    res = pd.DataFrame({"u": u, "r": y - X @ b}).groupby("u").r.mean()
    return b, res


def twfe_ajuste(dy, u, p, it=200):
    """Efectos de unidad y periodo por proyecciones alternas (panel no balanceado); lambda con media cero entre periodos."""
    df = pd.DataFrame({"u": u, "p": p, "dy": dy})
    a = pd.Series(0.0, index=df.u.unique())
    lam = pd.Series(0.0, index=df.p.unique())
    for _ in range(it):
        a_new = (df.dy - df.p.map(lam)).groupby(df.u).mean()
        lam_new = (df.dy - df.u.map(a_new)).groupby(df.p).mean()
        if np.max(np.abs(lam_new - lam)) < 1e-10 and np.max(np.abs(a_new - a)) < 1e-10:
            a, lam = a_new, lam_new
            break
        a, lam = a_new, lam_new
    m = lam.mean()
    return a + m, lam - m


def predecir_lineas(t, T, corte):
    """Devuelve {(linea, variante): pred alineada con T['va']}."""
    tr, va, allp = preparar(t, T)
    sel = set(S.prov_selladas())
    f_tr = factor(tr, sel)
    f_all = factor(allp, sel)
    ylook = allp.set_index(["unit", "per"]).y
    tr = tr.dropna(subset=["y", "y1"]).copy()
    tr = tr[tr.anio < corte].copy()
    y1v = va.y1.to_numpy(float)
    per = va.per.to_numpy(int)
    fa_t = f_all.reindex(per).to_numpy(float)
    fa_p = f_all.reindex(per - 1).to_numpy(float)
    out = {("ult_crec_nac", "ora"): y1v + fa_t, ("ult_crec_nac", "fac"): y1v + fa_p}

    # ---- AR(1) en dy con factor comun
    tr["dy"] = tr.y - tr.y1
    tr["y2"] = lag2(tr, ylook)
    tr["dy1"] = tr.y1 - tr.y2
    tr["f1"] = f_tr.reindex(tr.per - 1).to_numpy(float)
    tr["f0"] = f_tr.reindex(tr.per).to_numpy(float)
    dva = va.assign(dy1=y1v - lag2(va, ylook), f1=fa_p, f0=fa_t)
    for var, xs in (("fac", ["dy1", "f1"]), ("ora", ["dy1", "f1", "f0"])):
        m = tr.dropna(subset=["dy"] + xs)
        b, ai = ajuste_intra(m[xs].to_numpy(float), m.dy.to_numpy(float), m.unit.to_numpy())
        a_i = dva.unit.map(ai).fillna(ai.mean()).to_numpy(float)
        out[("ar_factor", var)] = y1v + a_i + dva[xs].to_numpy(float) @ b
        out[("ar_factor", var + "_coef")] = b
    # ---- efectos fijos de unidad y periodo
    m = tr.dropna(subset=["dy"])
    a, lam = twfe_ajuste(m.dy.to_numpy(float), m.unit.to_numpy(), m.per.to_numpy())
    a_bar = float(a.mean())
    a_v = va.unit.map(a).fillna(a_bar).to_numpy(float)

    def lam_de(p):
        est = pd.Series(p).map(lam).to_numpy(float)
        return np.where(np.isnan(est), f_all.reindex(p).to_numpy(float) - a_bar, est)
    out[("twfe", "ora")] = y1v + a_v + lam_de(per)
    out[("twfe", "fac")] = y1v + a_v + lam_de(per - 1)
    return out


def evaluar(tid, linea, s_ref, dry_sell=None):
    t = dict(S.TAREAS[tid], _id=tid)
    hid = f"k1_{tid}__{linea}"
    rutas = {v: OUT / f"sellado_{tid}__{linea}_{v}.json" for v in VARIANTES}

    def fn(sell):
        estados = {}
        try:
            T = S.construir_alq(t, sell) if t["kind"] == "alq" else S.construir_cp(t, sell)
            preds = predecir_lineas(t, T, T["corte"])
            for v in VARIANTES:
                d = T["va"].copy()
                d["pred"] = preds[(linea, v)]
                met, cells, nfb, n, nout = S.resumir(d, T["corte"], s_ref)
                key = f"{tid}__{linea}_{v}"
                res = dict(modelo_id=key, tarea=tid, rol="base", modelo=f"{linea}_{v}", familia=f"{linea}_{v}", mercado=t["mercado"],
                           nivel=t["nivel"], medida=t["medida"], medida_precio=t["medida_precio"], corte_temporal=T["corte"],
                           provincias_selladas=S.prov_selladas(), s_ref_intervalo=s_ref,
                           intervalo="pred +- 1,96 x RMSE de validacion en bloques del entrenamiento (cobertura empirica en el sellado)",
                           metricas=met, n_filas=n, n_fuera_de_grupo=nout, n_fallback_persistencia=nfb, celdas=cells,
                           linea_base=linea, variante=v, descripcion=f"{LINEAS[linea]}; {VARIANTES[v]}", id_apertura=hid,
                           coef_ar=[float(x) for x in preds.get((linea, v + "_coef"), [])] or None,
                           validacion="espacial nueva; temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5",
                           capa="C4", estado="evaluado")
                estados[v] = res
        except Exception as e:  # el sellado ya esta abierto: se registra el fallo
            for v in VARIANTES:
                estados[v] = dict(modelo_id=f"{tid}__{linea}_{v}", tarea=tid, estado="fallo_tras_apertura", error=repr(e),
                                  traza=traceback.format_exc()[-1500:])
        if not S.MODO["dry"]:
            OUT.mkdir(parents=True, exist_ok=True)
            for v, r in estados.items():
                rutas[v].write_text(json.dumps(r, ensure_ascii=False, indent=1, default=float))
        return {"modelo_id": hid, "estados": {v: r["estado"] for v, r in estados.items()},
                "metricas": {v: r.get("metricas") for v, r in estados.items()},
                "error": next((r.get("error") for r in estados.values() if r.get("error")), None),
                "traza": next((r.get("traza") for r in estados.values() if r.get("traza")), None)}

    if S.MODO["dry"]:
        return fn(dry_sell)
    if all(r.exists() for r in rutas.values()):
        return {"modelo_id": hid, "estados": "ya_evaluado"}
    return holdout.evaluate_v6(hid, fn, "K1", t["paneles"])


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo not in ("--dry", "--real"):
        print(__doc__)
        return 2
    if modo == "--dry":
        S.MODO.update(dry=True, corte_alq=int(pd.read_csv(S.A.PAN / "prov_alquiler_anual_train.csv.gz").dropna(
            subset=["ln_alq_m2_serpavi_vc"]).anio.max()), corte_cp=int(pd.read_csv(S.A.PAN / "prov_compra_anual_train.csv.gz").anio.max()))
    filtro = sys.argv[2:]
    for tid in S.TAREAS:
        if filtro and not any(f in tid for f in filtro):
            continue
        for linea in LINEAS:
            s_ref = S.s_ref_de(tid, "base", "persistencia")
            r = evaluar(tid, linea, s_ref, S.fake_sellado(S.TAREAS[tid]["paneles"]) if modo == "--dry" else None)
            if modo == "--dry":
                print(tid, linea, r["estados"], r.get("error") or "", flush=True)
                for v, m in (r.get("metricas") or {}).items():
                    print("   ", v, {g: (x["n"], round(x["rmse"], 4) if x["rmse"] is not None else None) for g, x in (m or {}).items()})
                if r.get("traza"):
                    print(r["traza"])
            else:
                print(tid, linea, r.get("estados"), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
