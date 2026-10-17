"""V16 fase 2 · esfuerzo de acceso (ECV 2004-2025) y descomposiciones contables. Capa C4, sin interpretación de mecanismos.

Uso:  python3 src/v16/f2_esfuerzo.py            (completo: B = 500 réplicas)
      python3 src/v16/f2_esfuerzo.py --smoke    (submuestra: 3 años, B = 20; escribe en el directorio temporal)
Salidas en output/v16/f2_esfuerzo/. SEED = 20261010. Sin red. No lee data/sealed.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")   # un hilo por proceso: evita sobresuscripción con el Pool

import json
import multiprocessing as mp
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v16"))
from econ_utils import Registry  # noqa: E402
from f2_esfuerzo_datos import ANIOS, cargar  # noqa: E402
from f2_esfuerzo_nucleo import (CCAA_NOMBRES, EDAD, INDIC_ALL, NAC, QUIN, SEED, TEN, UNID, bh,  # noqa: E402
                                bootstrap_anio, descomponer, directa, preparar, resumen_celda, tabla_anio)

OUT = ROOT / "output" / "v16" / "f2_esfuerzo"
PERIODOS = [(2008, 2015), (2015, 2025), (2008, 2025), (2019, 2025)]
GRUPOS = ["alquiler_mercado", "prop_con_hipoteca"]
FECHA_DATO = "2026-06-10"
FUENTE = "INE, Encuesta de Condiciones de Vida (microdatos transversales 2004-2025; ficheros D, H, R, P)"
D_ = None  # datos preparados (heredados por fork)


# ------------------------------------------------------------------------------------------------ tareas
def _tarea_anio(args):
    y, B = args
    g = D_[D_.anio == y].reset_index(drop=True)
    res, nobs = bootstrap_anio(g, B, SEED)
    return y, res, nobs


def _muestra(g, ten):
    x = g[(g.ten == ten) & g.edad_sust.notna() & g.HX040.notna()].copy()
    return x.reset_index(drop=True)


def _tarea_desc(args):
    ten, (ya, yb), B, k = args
    a, b = _muestra(D_[D_.anio == ya], ten), _muestra(D_[D_.anio == yb], ten)
    out = descomponer(a, b)
    dire = {"G": directa(a, b, "G")}
    alt = "HH060" if ten == "alquiler_mercado" else "cuotahip"
    for x in (a, b):
        x["Galt"] = 12 * x[alt]
    a2, b2 = a.dropna(subset=["Galt"]), b.dropna(subset=["Galt"])
    dire["Galt"] = directa(a2, b2, "Galt")
    rng = np.random.default_rng([SEED, 1000 + k])
    reps, reps_d = [], {"G": [], "Galt": []}
    for _ in range(B):
        ra = a.iloc[rng.integers(0, len(a), len(a))]
        rb = b.iloc[rng.integers(0, len(b), len(b))]
        try:
            reps.append(descomponer(ra, rb))
            reps_d["G"].append(directa(ra, rb, "G"))
            r2a, r2b = ra.dropna(subset=["Galt"]), rb.dropna(subset=["Galt"])
            reps_d["Galt"].append(directa(r2a, r2b, "Galt"))
        except Exception:   # réplica degenerada: se omite (se cuenta en el informe)
            continue
    return ten, (ya, yb), out, reps, dire, reps_d, (len(a), len(b)), (len(a2), len(b2))


# ------------------------------------------------------------------------------------------------ utilidades
def ci(v, pt):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    if len(v) < 10:
        return np.nan, np.nan, np.nan
    lo, hi = np.percentile(v, [2.5, 97.5])
    p = 2 * min((np.sum(v <= 0) + 1) / (len(v) + 1), (np.sum(v >= 0) + 1) / (len(v) + 1))
    return float(lo), float(hi), min(1.0, p)


def clave_a_fila(k):
    p = k.split("|")
    if k == "media|total":
        return "observado", "media", "total"
    if p[0] in ("OB2", "OB3"):
        return p[0], "media", p[1]
    if p[0] == "OB2det":
        return "OB2_detalle", "media", p[1]
    if p[0] == "DFL" and p[1] == "ess_ratio":
        return "DFL", "media", "ess_ratio"
    if p[0] == "DFL":
        return "DFL", p[1], p[2]
    if p[0] == "RIF":
        return "RIF", p[1], p[2]
    if p[0] == "RIFdet":
        return "RIF_detalle", p[1], p[2]
    raise KeyError(k)


def solo_informe():
    """Regenera informe, hechos y resultado desde las tablas ya escritas (sin recalcular)."""
    from f2_esfuerzo_informe import escribir_informe
    r = lambda n: pd.read_csv(OUT / n, keep_default_na=False, na_values=[""])  # noqa: E731
    T = r("esfuerzo_por_anio.csv")
    T["categoria"] = T.categoria.astype(str)
    CH = r("esfuerzo_cambios.csv")
    CH["categoria"] = CH.categoria.astype(str)
    escribir_informe(OUT, T, CH, r("comparacion_eurostat.csv"), r("descomposiciones.csv"), r("comparacion_metodos.csv"),
                     r("descomposicion_directa.csv"), int(T.B.iloc[0]), sorted(T.anio.unique()), False)


def main(smoke: bool = False):
    global D_
    B = 20 if smoke else 500
    out = Path(__import__("tempfile").gettempdir()) / "v16_f2_smoke" if smoke else OUT
    out.mkdir(parents=True, exist_ok=True)
    anios = [2008, 2015, 2019, 2025] if smoke else ANIOS
    raw = cargar(anios=anios)
    D_ = preparar(raw)
    n_proc = 3
    ctx = mp.get_context("fork")

    # 1. esfuerzo por año
    with ctx.Pool(n_proc) as pool:
        porano = pool.map(_tarea_anio, [(y, B) for y in anios])
    filas, RES = [], {}
    for y, res, nobs in porano:
        filas += tabla_anio(res, nobs, y)
        RES[y] = (res, nobs)
    T = pd.DataFrame(filas)
    T["categoria_nombre"] = np.where(T.dimension == "CCAA", T.categoria.map(CCAA_NOMBRES), T.categoria)
    T["B"] = B
    T.to_csv(out / "esfuerzo_por_anio.csv", index=False, float_format="%.4f")

    # 2. cambios entre años
    ch = []
    for ya, yb in PERIODOS:
        if ya not in RES or yb not in RES:
            continue
        for (d, c, i), va in RES[ya][0].items():
            vb = RES[yb][0][(d, c, i)]
            sa, sb = resumen_celda(va, RES[ya][1][(d, c)]), resumen_celda(vb, RES[yb][1][(d, c)])
            dif = vb - va
            lo, hi, p = ci(dif[1:], dif[0])
            ok = sa["estado"] == "publicable" and sb["estado"] == "publicable"
            ch.append(dict(periodo=f"{ya}-{yb}", dimension=d, categoria=c, indicador=i, unidad="puntos porcentuales",
                           valor_ini=va[0], valor_fin=vb[0], cambio=dif[0], ic_lo=lo, ic_hi=hi, p_boot=p,
                           estado="publicable" if ok else "suprimida"))
    CH = pd.DataFrame(ch)
    CH["categoria_nombre"] = np.where(CH.dimension == "CCAA", CH.categoria.map(CCAA_NOMBRES), CH.categoria)
    CH.to_csv(out / "esfuerzo_cambios.csv", index=False, float_format="%.4f")

    # 3. comparación con Eurostat (ilc_lvho07a, total, ambos sexos, toda la población)
    eu = pd.read_parquet(ROOT / "data/processed/v16/demanda_internacional.parquet")
    eu = eu[(eu.variable == "eurostat_sobrecarga_coste_vivienda_pct") & (eu.territorio_codigo == "ES")
            & (eu.desagregacion == "edad=TOTAL;sexo=T;pobreza=TOTAL")]
    eu = eu.assign(anio=eu.periodo.astype(int)).set_index("anio").valor
    ce = []
    for y in anios:
        v = RES[y][0][("Total", "Espana", "sobre40")]
        s = resumen_celda(v, RES[y][1][("Total", "Espana")])
        e = float(eu.get(y, np.nan))
        ce.append(dict(anio=y, ecv_microdatos=v[0], ic_lo=s["ic_lo"], ic_hi=s["ic_hi"], eurostat_ilc_lvho07a=e,
                       diferencia_pp=v[0] - e, dentro_0_5pp=bool(abs(v[0] - e) <= 0.5)))
    CE = pd.DataFrame(ce)
    CE.to_csv(out / "comparacion_eurostat.csv", index=False, float_format="%.4f")

    # 4. descomposiciones
    tareas = [(t, p, B, k) for k, (t, p) in enumerate((t, p) for t in GRUPOS for p in PERIODOS)
              if p[0] in anios and p[1] in anios]
    with ctx.Pool(n_proc) as pool:
        DR = pool.map(_tarea_desc, tareas)
    filas, dfilas = [], []
    for ten, (ya, yb), pt, reps, dire, reps_d, nn, nn2 in DR:
        for k, v in pt.items():
            met, est, comp = clave_a_fila(k)
            esc = 1.0 if comp == "ess_ratio" else 100.0   # r en fracción -> puntos porcentuales
            rv = [r[k] * esc for r in reps if k in r]
            lo, hi, p = ci(rv, v * esc)
            filas.append(dict(tenencia=ten, periodo=f"{ya}-{yb}", metodo=met, estadistico=est, componente=comp,
                              valor_pp=v * esc, ic_lo=lo, ic_hi=hi, p_boot=p, n_ini=nn[0], n_fin=nn[1],
                              B_validas=len(rv)))
        for var, dd in dire.items():
            for comp in ("R0", "R1", "dR", "gasto", "renta", "interaccion", "dlnG", "dlnY", "dlnR"):
                rv = [r[comp] for r in reps_d[var]]
                lo, hi, p = ci(rv, dd[comp])
                dfilas.append(dict(tenencia=ten, periodo=f"{ya}-{yb}",
                                   gasto_definicion="HH070 neto de ayudas" if var == "G" else (
                                       "alquiler HH060" if ten == "alquiler_mercado" else "cuota hipotecaria cuotahip"),
                                   componente=comp, valor=dd[comp], ic_lo=lo, ic_hi=hi, B_validas=len(rv),
                                   unidad="puntos porcentuales" if comp in ("R0", "R1", "dR", "gasto", "renta", "interaccion") else "log"))
    DC = pd.DataFrame(filas)
    # BH sobre las contrastaciones de la parte «atribuida/composición»
    m = ((DC.metodo == "OB2") & (DC.componente == "atribuido")) | ((DC.metodo == "DFL") & (DC.componente == "composicion")) \
        | ((DC.metodo == "RIF") & (DC.componente == "atribuido"))
    DC["p_ajustado_BH"] = np.nan
    DC.loc[m, "p_ajustado_BH"] = bh(DC.loc[m, "p_boot"].values)
    DC.to_csv(out / "descomposiciones.csv", index=False, float_format="%.5f")
    pd.DataFrame(dfilas).to_csv(out / "descomposicion_directa.csv", index=False, float_format="%.5f")

    # comparación de métodos
    cm = []
    for (ten, per), g in DC.groupby(["tenencia", "periodo"]):
        for est in ("media", "p10", "p50", "p90"):
            tot = g[(g.metodo == "DFL") & (g.estadistico == est) & (g.componente == "total")].valor_pp.iloc[0]
            comp = g[(g.metodo == "DFL") & (g.estadistico == est) & (g.componente == "composicion")].valor_pp.iloc[0]
            if est == "media":
                ex = g[(g.metodo == "OB2") & (g.componente == "atribuido")].valor_pp.iloc[0]
                nm = "OB2"
            else:
                ex = g[(g.metodo == "RIF") & (g.estadistico == est) & (g.componente == "atribuido")].valor_pp.iloc[0]
                nm = "RIF"
            dis = bool(np.sign(ex) != np.sign(comp) or abs(ex - comp) > 0.25 * abs(tot))
            cm.append(dict(tenencia=ten, periodo=per, estadistico=est, cambio_total_pp=tot, metodo_regresion=nm,
                           atribuido_regresion_pp=ex, composicion_DFL_pp=comp, diferencia_pp=ex - comp,
                           discrepan=dis))
    CM = pd.DataFrame(cm)
    CM.to_csv(out / "comparacion_metodos.csv", index=False, float_format="%.4f")

    # 5. registro de especificaciones
    reg = Registry(out / "registro.csv")
    esp = []
    n_tot = int(len(D_))
    for ind, formula in [("sobre40", "100*sum(wp*[G>0.40*Y])/sum(wp); G=12*HH070-HY070N; Y=HY020-HY070N"),
                         ("sobre30", "100*sum(wp*[G>0.30*Y])/sum(wp); G=12*HH070-HY070N; Y=HY020-HY070N"),
                         ("cae_bajo_umbral", "[eq_pre>=z & eq_post<z]; eq_pre=HY020/HX240; eq_post=(HY020-12*HH070)/HX240; z=0.6*mediana(eq_pre)"),
                         ("pobreza_antes", "[eq_pre<z]"), ("pobreza_despues", "[eq_post<z]"),
                         ("esfuerzo_medio", "mean_wh(min(G/Y,1))")]:
        reg.log("V16-F2", f"ESF-{ind}", formula, min(anios), max(anios), n_tot, np.nan, np.nan, np.nan,
                notas=f"descriptivo; bootstrap de hogares B={B}; celdas con n<50 o CV>30% suprimidas")
        esp.append(dict(id=f"ESF-{ind}", tipo="indicador", formula=formula, muestra=f"{min(anios)}-{max(anios)}", n=n_tot))
    for ten, per, ob, ex, p in [(r.tenencia, r.periodo, r.metodo, r.valor_pp, r.p_boot) for r in
                                DC[(DC.metodo == "OB2") & (DC.componente == "atribuido")].itertuples()]:
        n_ = DC[(DC.tenencia == ten) & (DC.periodo == per)].n_ini.iloc[0] + DC[(DC.tenencia == ten) & (DC.periodo == per)].n_fin.iloc[0]
        for mid, f in [("OB2", "r ~ ln_renta + edad + edad2 + tam + nacionalidad + region; dos pliegues, referencia agrupada"),
                       ("OB3", "idem; tres pliegues (dotaciones, coeficientes, interacción), referencia año inicial"),
                       ("DFL", "logit P(año fin | X) -> reponderación del año inicial; media, p10, p50, p90"),
                       ("RIF", "RIF(r; q_tau) ~ X, tau=0.1,0.5,0.9; referencia agrupada"),
                       ("DIRECTA", "dR = dG/Y0 + G0*d(1/Y) + dG*d(1/Y) (razón de medias)")]:
            reg.log("V16-F2", f"{mid}-{ten}-{per}", f, per[:4], per[5:], int(n_), np.nan, np.nan, np.nan,
                    coef_interes=ex if mid == "OB2" else np.nan, p_interes=p if mid == "OB2" else np.nan,
                    notas="contabilidad, sin interpretación de mecanismos; IC por bootstrap de hogares")
            esp.append(dict(id=f"{mid}-{ten}-{per}", tipo="descomposicion", formula=f, muestra=per, n=int(n_)))
    reg.log("V16-F2", "EUROSTAT-ilc_lvho07a", "dif = sobre40 ECV - ilc_lvho07a (ES, total)", min(anios), max(anios),
            len(CE), np.nan, np.nan, np.nan, notas="prueba de implementación; ±0,5 pp")
    esp.append(dict(id="EUROSTAT-ilc_lvho07a", tipo="validacion", formula="|sobre40 - ilc_lvho07a| <= 0,5 pp",
                    muestra=f"{min(anios)}-{max(anios)}", n=len(CE)))
    reg.flush()
    pd.DataFrame(esp).to_csv(out / "especificaciones.csv", index=False)

    # 6. hechos, resultado, informe
    from f2_esfuerzo_informe import escribir_informe
    escribir_informe(out, T, CH, CE, DC, CM, pd.DataFrame(dfilas), B, anios, smoke)
    print("OK", out)


if __name__ == "__main__":
    if "--informe" in sys.argv:
        solo_informe()
    else:
        main(smoke="--smoke" in sys.argv)
