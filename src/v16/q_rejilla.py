"""V16 fase 6 · rejilla fija de 83 celdas (output/v16/potencia/rejilla_fija.csv): TWFE puntual por celda (NO APTO: sin errores típicos, p ni IC)
y 5 variantes de robustez por celda (415 declaradas). Solo entrenamiento. Operacionalización: docs/v16/desviaciones.md, D4. Uso: python3 src/v16/q_rejilla.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from src.v16 import qc_comun as C  # noqa: E402

warnings.filterwarnings("ignore")
Q = C.Q
OUT = C.OUTD / "rejilla"
ENTR = Q.ENTR
ARCHIVOS = ["base_precio", "base_alquiler", "tension_social_terceros", "base_oferta"]
CONTEOS = ("cgpj_", "incasol_contratos", "serpavi_n_contratos", "obra_nueva", "hip_n", "iniciadas", "terminadas", "compraventas")
_cache: dict = {}


def prov_ccaa():
    return Q.centroides_provincia()[1]


# ------------------------------------------------------------------ resultados anuales
def resultado(var: str, nivel: str) -> pd.DataFrame:
    k = ("res", var, nivel)
    if k in _cache:
        return _cache[k]
    partes = []
    for a in ARCHIVOS:
        d = pd.read_parquet(ENTR / f"{a}.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable", "valor"],
                            filters=[("variable", "==", var), ("nivel", "==", nivel)])
        if len(d):
            partes.append(d)
    d = pd.concat(partes).drop_duplicates(["territorio_codigo", "periodo"])
    d["territorio_codigo"] = d.territorio_codigo.astype(str)
    p = d.periodo.astype(str)
    anual = d[p.str.fullmatch(r"\d{4}")].assign(t=lambda x: x.periodo.astype(int))[["territorio_codigo", "t", "valor"]]
    if len(anual) < 0.5 * len(d):      # serie esencialmente trimestral: agregar por año con 4 trimestres
        tr = d[p.str.contains("T")].copy()
        tr["t"] = tr.periodo.astype(str).str[:4].astype(int)
        g = tr.groupby(["territorio_codigo", "t"]).valor
        suma = var.startswith(CONTEOS) or any(var.startswith(c) for c in CONTEOS)
        agg = (g.sum() if suma else g.mean()).rename("valor")
        n4 = g.count()
        anual = agg[n4 >= 4].reset_index()
    anual = anual.rename(columns={"territorio_codigo": "u"})
    anual = anual[anual.valor > 0].assign(y=lambda x: np.log(x.valor))[["u", "t", "y"]]
    _cache[k] = anual
    return anual


# ------------------------------------------------------------------ exposiciones (u, t, x)
def mun_de(u: str) -> str:
    return u[:5]


def exp_q1(escala: str) -> pd.DataFrame:
    z = Q.cargar("base_regulacion", "municipio", "zt_vigente")
    z["t"] = z.periodo.astype(str).str[:4].astype(int)
    f = z.groupby(["territorio_codigo", "t"]).periodo.nunique().div(4).clip(upper=1).rename("x").reset_index().rename(columns={"territorio_codigo": "u"})
    if escala == "municipio":
        return f
    pob = Q.cargar("base_poblacion", "municipio", "pob_censo_anual")
    pob = pob[(pob.periodo.astype(str) == "2021") & (pob.desagregacion == "nacionalidad=Total")].set_index("territorio_codigo").valor
    pp = Q.cargar("base_poblacion", "provincia", "pob_censo_anual")
    pp = pp[(pp.periodo.astype(str) == "2021") & (pp.desagregacion == "nacionalidad=Total")].set_index("territorio_codigo").valor
    f["w"] = f.u.map(pob).fillna(0) * f.x
    g = f.assign(p=f.u.str[:2]).groupby(["p", "t"]).w.sum().reset_index()
    g["x"] = g.w / g.p.map(pp)
    return g.rename(columns={"p": "u"})[["u", "t", "x"]]


def exp_q2(escala: str) -> pd.DataFrame:
    nivel = "provincia" if escala == "provincia" else "municipio"
    v = Q.cargar("alquiler_turismo", nivel)
    v = v[v.variable.str.startswith("ine_vte_porcentaje")].copy()
    v["t"] = v.periodo.astype(str).str[:4].astype(int)
    g = v.groupby(["territorio_codigo", "t"]).valor.mean().rename("pct").reset_index().rename(columns={"territorio_codigo": "u"})
    g = g[g.pct > 0]
    g["x"] = np.log(g.pct)
    return g[["u", "t", "x"]]


def _shift(nivel: str) -> pd.DataFrame:
    k = ("ss", nivel)
    if k not in _cache:
        import qb_shiftshare as S
        s = S.shiftshare(nivel, 2003)
        _cache[k] = pd.DataFrame(s["x"], index=s["unidades"], columns=s["años"]).stack().rename("x").reset_index().rename(columns={"level_0": "u", "level_1": "t"})
    return _cache[k]


def exp_q3(escala: str) -> pd.DataFrame:
    return _shift("provincia" if escala == "provincia" else "municipio")


def exp_q4() -> pd.DataFrame:
    rn = Q.cargar("oferta_suelo_terceros", "municipio", "miteco_rn2000_porcentaje_superficie_municipal").groupby("territorio_codigo").valor.first() / 100
    s = _shift("municipio")
    s = s.assign(x=s.x * s.u.map(rn))
    return s.dropna()


def exp_q6() -> pd.DataFrame:
    import q6_itp as I
    t = I.tipos(0).rename(columns={"c": "cc", "d": "x"}).dropna()
    pc = prov_ccaa()
    filas = [(p, r.t, r.x) for p, c in pc.items() for r in t[t.cc == c].itertuples()]
    return pd.DataFrame(filas, columns=["u", "t", "x"])


def exposicion(fam: str, escala: str) -> pd.DataFrame:
    k = ("exp", fam, escala)
    if k not in _cache:
        e = {"Q1": lambda: exp_q1(escala), "Q2": lambda: exp_q2("provincia" if escala == "provincia" else "municipio"),
             "Q3": lambda: exp_q3(escala), "Q4": exp_q4, "Q6": exp_q6}[fam]()
        _cache[k] = e
    return _cache[k]


# ------------------------------------------------------------------ controles
def controles() -> pd.DataFrame:
    pt = Q.cargar("base_poblacion", "provincia", "pob_total")
    pt = pt[pt.periodo.astype(str).str.fullmatch(r"\d{4}")]
    pw = pt.assign(t=pt.periodo.astype(int)).pivot_table(index="t", columns="territorio_codigo", values="valor")
    pw = pw.reindex(range(2002, 2027)).ffill()
    lp = np.log(pw).stack().rename("ln_pob").reset_index().rename(columns={"territorio_codigo": "p"})
    cov = Q.covariables_provincia(sorted(pw.columns))
    lp["ln_renta"] = lp.p.map(cov.ln_renta)
    return lp


def asegura_mun(df: pd.DataFrame, escala: str, fam: str) -> pd.DataFrame:
    """Para distrito y sección el exposición es la de su municipio (Q2, Q3); para Q1 municipal, las unidades sin zona tienen x = 0."""
    return df


def celda(fila, variante: str, excl_grandes: bool = False):
    fam, escala, var, vent = fila.pregunta, fila.escala, fila.resultado, fila.ventana
    t0, t1 = [int(a) for a in vent.split("-")]
    if variante == "d":
        t1 = min(t1, 2019)
    if variante == "e":
        t0 = max(t0, 2020)
    if t1 - t0 + 1 < (3 if variante in ("d", "e") else 2):
        return {"estado": "no estimable", "motivo": "menos de 3 años en el tramo" if variante in ("d", "e") else "menos de 2 años"}
    y = resultado(var, escala)
    ex = exposicion(fam, escala)
    d = y[(y.t >= t0) & (y.t <= t1)].copy()
    if escala in ("distrito", "seccion"):
        d["um"] = d.u.str[:5]
        x = ex.rename(columns={"u": "um"})
        d = d.merge(x, on=["um", "t"], how="left")
    else:
        if fam == "Q1":     # sin zona = exposición 0 (el panel de zonas solo lista las unidades con zona vigente)
            d = d.merge(ex, on=["u", "t"], how="left")
            d["x"] = d.x.fillna(0.0)
        else:
            d = d.merge(ex, on=["u", "t"], how="left")
    d = d.dropna(subset=["x"])
    if fam == "Q6":
        pass
    pc = prov_ccaa()
    d["p"] = d.u.str[:2]
    d["cc"] = d.p.map(pc)
    d = d[d.cc.notna()]
    if excl_grandes:
        if escala == "provincia":
            d = d[~d.u.isin(Q.GRANDES_PROV)]
        else:
            d = d[~d.u.str[:5].isin(Q.GRANDES_MUN)]
    if fam == "Q2":     # exposición estandarizada en la muestra de la celda
        d["x"] = (d.x - d.x.mean()) / d.x.std(ddof=1)
    ctrl = []
    if variante in ("a", "c"):
        for k, cc in enumerate(sorted(d.cc.unique())):
            d[f"tr{k}"] = (d.cc == cc) * (d.t - t0)
            ctrl.append(f"tr{k}")
    if variante in ("b", "c"):
        d = d.merge(controles(), left_on=["p", "t"], right_on=["p", "t"], how="left").dropna(subset=["ln_pob", "ln_renta"])
        d["renta_tr"] = d.ln_renta * (d.t - t0)
        ctrl += ["ln_pob", "renta_tr"]
    n_un = d.u.nunique()
    if d.t.nunique() < 2 or n_un < 10 or len(d) < 30:
        return {"estado": "no estimable", "motivo": f"{n_un} unidades, {d.t.nunique()} periodos"}
    xdm = d.x - d.groupby("u").x.transform("mean")
    xdm = xdm - xdm.groupby(d.t).transform("mean")
    if xdm.std() < 1e-9:
        return {"estado": "no estimable", "motivo": "sin variación de la exposición dentro de unidad y periodo"}
    r = Q.twfe(d, "y", "x", "u", "t", controles=ctrl)
    sd = float(d.x.std(ddof=1))
    return {"estado": "estimada", "beta": r["beta"], "beta_por_DT": r["beta"] * sd, "sd_x": sd, "n": r["n"], "n_unidades": int(n_un), "r2_dentro": r["r2"], "periodos": f"{t0}-{t1}"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rj = pd.read_csv(C.OUTD / "potencia" / "rejilla_fija.csv")
    rj = rj[rj.en_rejilla].reset_index(drop=True)
    assert len(rj) == 83
    filas, reg = [], []
    for fila in rj.itertuples():
        base = celda(fila, "P")
        rec = {"celda": fila.celda, "pregunta": fila.pregunta, "escala": fila.escala, "resultado": fila.resultado, "ventana": fila.ventana, **{f"P_{k}": v for k, v in base.items()}}
        if base["estado"] == "estimada":
            ex = celda(fila, "P", excl_grandes=True)
            rec["excl_grandes_beta"] = ex.get("beta")
        for v in "abcde":
            rv = celda(fila, v)
            rec.update({f"{v}_estado": rv["estado"], f"{v}_beta": rv.get("beta"), f"{v}_n": rv.get("n")})
        filas.append(rec)
        reg.append({"id": f"REJ-{fila.celda}", "pregunta": fila.pregunta, "rol": "principal", "especificacion": f"log {fila.resultado} ~ exposición + EF de unidad y periodo ({fila.escala}, {fila.ventana})",
                    "muestra": f"{base.get('n_unidades', 0)} unidades, {base.get('periodos', fila.ventana)}", "n": base.get("n"), "estimacion": base.get("beta"), "unidad": "log por unidad de exposición",
                    "inferencia": "ninguna (rejilla_twfe NO APTO)", "nota": base.get("motivo", "")})
        for v, nm in zip("abcde", ("tendencias CCAA", "controles", "tendencias+controles", "hasta 2019", "desde 2020")):
            reg.append({"id": f"REJ-{fila.celda}-{v}", "pregunta": fila.pregunta, "rol": "robustez", "especificacion": f"variante ({v}) {nm}", "muestra": fila.ventana, "n": rec[f"{v}_n"],
                        "estimacion": rec[f"{v}_beta"], "unidad": "log por unidad de exposición", "inferencia": "ninguna", "nota": rec[f"{v}_estado"]})
        print(fila.celda, base["estado"], base.get("beta"), flush=True)
    df = pd.DataFrame(filas)
    df.to_csv(OUT / "rejilla_resultados.csv", index=False)
    Q.registro(reg, OUT / "registro.csv")
    est = df[df.P_estado == "estimada"]
    # resumen: signo, estabilidad en variantes
    def estab(r):
        vs = [r[f"{v}_beta"] for v in "abcde" if r[f"{v}_estado"] == "estimada" and np.isfinite(r[f"{v}_beta"])]
        return np.nan if not vs else float(np.mean(np.sign(vs) == np.sign(r.P_beta)))
    est = est.assign(mismo_signo_variantes=est.apply(estab, axis=1))
    por_fam = {}
    for fam, g in df.groupby("pregunta"):
        e = g[g.P_estado == "estimada"]
        por_fam[fam] = {"celdas": int(len(g)), "estimadas": int(len(e)), "no_estimables": int(len(g) - len(e)),
                        "beta_positivo": int((e.P_beta > 0).sum()), "beta_negativo": int((e.P_beta < 0).sum()),
                        "mismo_signo_en_variantes_mediana": float(est[est.pregunta == fam].mismo_signo_variantes.median()) if len(e) else None}
    resumen = {"celdas": 83, "estimadas": int(len(est)), "no_estimables": int(83 - len(est)), "por_familia": por_fam,
               "variantes_declaradas": 415, "variantes_estimadas": int(sum((df[f"{v}_estado"] == "estimada").sum() for v in "abcde")),
               "mismo_signo_variantes_mediana_global": float(est.mismo_signo_variantes.median())}
    py = [{"id": r.celda, "p": None, "motivo": "rejilla_twfe NO APTO (municipio y provincia): solo estimación puntual"} for r in rj.itertuples()]
    diag = [C.diag("calibración TWFE de la rejilla", "NO APTO", "tamaño municipio 0,203 / provincia 0,1105; cobertura 0,8055: solo estimación puntual, sin p ni IC"),
            C.diag("balance, pretendencias, Honest DiD, placebos de fecha/unidades, MOP, Moran", "no ejecutado por celda", "la rejilla es una búsqueda declarada con estimador puntual; los diagnósticos de diseño están en los informes de Q1-Q6"),
            C.diag("exclusión de grandes ciudades (Barcelona, València, Sevilla, Málaga)", "reportada por celda", "columna excl_grandes_beta de rejilla_resultados.csv"),
            C.diag("estabilidad en variantes", "reportada", {"mediana_proporcion_mismo_signo": resumen["mismo_signo_variantes_mediana_global"]}),
            C.diag("celdas no estimables", "reportadas", resumen["no_estimables"])]
    r = C.resultado("rejilla", "Rejilla fija multiescala: 83 celdas, TWFE puntual de log del resultado sobre la exposición de Q1, Q2, Q3, Q4 y Q6",
                    "data/processed/v16/entrenamiento (paneles anuales por unidad)", {"celdas": 83, "estimadas": resumen["estimadas"]},
                    "TWFE con EF de unidad y periodo, estimación puntual (NO APTA); 5 variantes de robustez por celda", resumen, diag,
                    ["C4 exploratorio, pendiente de evaluación sellada; asociación, sin lenguaje causal.", "Sin errores típicos válidos no hay p-valor: las 83 celdas entran en el BY del orquestador con p null.",
                     "Q3 y Q4 cubren hasta 2022 por el padrón por nacionalidad."], py)
    Q.jdump(r, OUT / "resultado.json")
    f = C.f
    hs = [C.hecho("estimadas", "REJILLA", "Celdas de la rejilla fija con estimación TWFE puntual (de 83)", resumen["estimadas"], resumen["estimadas"], resumen["estimadas"], "celdas", "2011-2025", "83 celdas", "paneles de entrenamiento", "resumen")]
    for i, (fam, v) in enumerate(por_fam.items(), 1):
        hs.append(C.hecho(f"fam-{fam}", "REJILLA", f"{fam}: celdas estimadas con coeficiente positivo (de las estimadas)", v["beta_positivo"], 0, v["estimadas"], "celdas", "2011-2025",
                          f"{v['celdas']} celdas", "paneles de entrenamiento", "resumen"))
    Q.jdump(hs, OUT / "hechos.json")
    md = ["# Rejilla fija multiescala (83 celdas) · C4, pendiente de evaluación sellada\n",
          "**Capa.** C4. TWFE de municipio y provincia NO APTO (tamaño 0,203 y 0,1105): **estimación puntual, sin p-valor ni IC**; las 83 celdas pasan al control BY del orquestador con p null. Asociación, sin lenguaje causal.\n",
          "<a id=\"resumen\"></a>## Resumen\n", f"- Celdas estimadas: {resumen['estimadas']} de 83; no estimables: {resumen['no_estimables']} (sin variación de la exposición en la ventana o < 10 unidades).",
          f"- Variantes de robustez declaradas: 415; estimadas: {resumen['variantes_estimadas']}. Mediana de la proporción de variantes con el mismo signo que la principal: {f(resumen['mismo_signo_variantes_mediana_global'], 2)}.\n",
          "| Familia | Celdas | Estimadas | β > 0 | β < 0 | Mediana mismo signo en variantes |", "|---|---|---|---|---|---|"]
    for fam, v in por_fam.items():
        md.append(f"| {fam} | {v['celdas']} | {v['estimadas']} | {v['beta_positivo']} | {v['beta_negativo']} | {f(v['mismo_signo_en_variantes_mediana'], 2)} |")
    md += ["", "## Especificación y límites", "log del resultado anual ~ exposición + EF de unidad y periodo (pre-registrada; adenda, punto 4). Exposiciones: Q1 fracción del año con zona vigente; Q2 log del % de vivienda turística INE estandarizado; Q3 shift-share del padrón de 2003; "
           "Q4 Red Natura × Q3; Q6 tipo general del ITP de su CCAA. Q3 y Q4 llegan a 2022. Las celdas por unidad (β por unidad de exposición y por DT, n, variantes y exclusión de grandes ciudades) están en rejilla_resultados.csv.",
           "No se elige ninguna celda por su resultado; el listado completo, con las no estimables, es el de rejilla_fija.csv. Diagnósticos de diseño (pretendencias, placebos, Honest DiD, Oster): en los informes de Q1-Q6, no por celda."]
    (OUT / "informe.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return resumen


if __name__ == "__main__":
    print(main())
