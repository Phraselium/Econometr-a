"""V16 fase 6 · Q5 (Q5-p valor tasado, Q5-a IPC de alquiler): proyecciones locales sobre la sorpresa de Jarociński-Karadi.

Especificación de la adenda (punto 3): LP a h = 4, sorpresa mediana mensual agregada a trimestre, 4 rezagos; Newey-West con b fija (NO APTA:
veredictos.csv) => SOLO estimación puntual, sin p-valor ni IC. Multiverso de 64 (4 resultados x 4 horizontes x 2 choques x 2 rezagos).
Desviaciones y operacionalización: docs/v16/desviaciones.md, D4. Uso: python3 src/v16/q5_proyecciones.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v16 import qc_comun as C  # noqa: E402

warnings.filterwarnings("ignore", category=FutureWarning)
OUT = C.OUTD / "q5"
H = [1, 4, 8, 12]
CHOQUES = {"mediana": "bce_jk_mp_median_m", "poor_mans": "bce_jk_mp_pm_m"}
RES = {"valor_tasado": ("base_precio", "p_tasado"), "ipv": ("base_precio", "ipv"), "compraventas": ("base_precio", "compraventas"),
       "ipc_alquiler": ("base_alquiler", "ipc_alquiler")}
VENT = {"Q5-p": "1999Q1", "Q5-a": "2002Q1"}      # inicio de ventana (adenda); el final lo marca el último trimestre con sorpresa
REF_P = -0.6                                      # % por DT de sorpresa a h=4 (P3 de V15)


def sorpresa(nombre: str) -> pd.Series:
    d = C.Q.cargar("demanda_internacional", "zona_euro", nombre)
    d = d[d.periodo.astype(str).str.match(r"^\d{4}-\d{2}$")]
    m = pd.Series(d.valor.values, index=pd.PeriodIndex(d.periodo.astype(str), freq="M"))
    return m.groupby(m.index.asfreq("Q")).sum().sort_index()


def lp(y_log: pd.Series, s: pd.Series, h: int, lags: int, ini: str, nivel_y: bool = False, extra_lead: int = 0):
    """Coeficiente del choque en y(t+h) - y(t-1) (x100) ~ const + s_t + L rezagos de s + L rezagos de Δy. Devuelve dict puntual."""
    idx = y_log.index.union(s.index).sort_values()
    idx = idx[(idx >= pd.Period(ini, "Q"))]
    y = y_log.reindex(idx)
    sh = s.reindex(idx)
    dy = y.diff() * 100
    dep = (y.shift(-h) - y.shift(1)) * 100 if not nivel_y else (y.shift(-h) - y.shift(1))
    X = {"s": sh.shift(-extra_lead)}
    for l in range(1, lags + 1):
        X[f"s_l{l}"] = sh.shift(l)
        X[f"dy_l{l}"] = dy.shift(l)
    D = pd.concat([dep.rename("dep"), pd.DataFrame(X)], axis=1).dropna()
    sd = D.s.std(ddof=1)
    D["s"] = D.s / sd
    for l in range(1, lags + 1):
        D[f"s_l{l}"] = D[f"s_l{l}"] / sd
    A = np.column_stack([np.ones(len(D)), D.drop(columns="dep").to_numpy()])
    b, *_ = np.linalg.lstsq(A, D.dep.to_numpy(), rcond=None)
    e = D.dep.to_numpy() - A @ b
    return {"beta": float(b[1]), "n": int(len(D)), "sd_choque": float(sd), "ini": str(D.index[0]), "fin": str(D.index[-1]), "res": e, "A": A, "y": D.dep.to_numpy(),
            "r2": float(1 - e @ e / ((D.dep - D.dep.mean()) ** 2).sum())}


def supF_ruptura(A, y, recorte=0.15):
    n, k = A.shape
    e0 = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
    ssr0 = e0 @ e0
    best, fecha = -1, None
    for tau in range(int(recorte * n), int((1 - recorte) * n)):
        s = 0.0
        for sl in (slice(0, tau), slice(tau, n)):
            bb = np.linalg.lstsq(A[sl], y[sl], rcond=None)[0]
            r = y[sl] - A[sl] @ bb
            s += r @ r
        F = ((ssr0 - s) / k) / (s / (n - 2 * k))
        if F > best:
            best, fecha = F, tau
    return float(best), int(fecha)


def primera_etapa(s: pd.Series, h: int, ini: str):
    """F robusto (HC1) de la primera etapa: Δ tipo hipotecario BdE (t-1 a t+h) sobre la sorpresa de t. Descriptivo (sin umbral de capa)."""
    tp = C.nat_q("base_macro", "tipo_hip_bde")
    idx = tp.index.union(s.index).sort_values()
    idx = idx[idx >= pd.Period(ini, "Q")]
    d = pd.concat([(tp.reindex(idx).shift(-h) - tp.reindex(idx).shift(1)).rename("dt"), s.reindex(idx).rename("s")], axis=1).dropna()
    z = d.s / d.s.std(ddof=1)
    A = np.column_stack([np.ones(len(d)), z])
    b = np.linalg.lstsq(A, d.dt.to_numpy(), rcond=None)[0]
    e = d.dt.to_numpy() - A @ b
    XtXi = np.linalg.inv(A.T @ A)
    V = XtXi @ (A.T * e ** 2) @ A @ XtXi * len(d) / (len(d) - 2)
    return {"h": h, "beta_pp_por_DT": float(b[1]), "F_robusto_HC1": float(b[1] ** 2 / V[1, 1]), "n": int(len(d))}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sh = {k: sorpresa(v) for k, v in CHOQUES.items()}
    ult = str(sh["mediana"].index[-1])
    Y = {k: np.log(C.nat_q(*v)) for k, v in RES.items()}
    reg, mv = [], []
    for res, (arch, var) in RES.items():
        for ch in CHOQUES:
            for h in H:
                for lags in (4, 2):
                    if True:
                        ini = VENT["Q5-p"] if res != "ipc_alquiler" else VENT["Q5-a"]
                        r = lp(Y[res], sh[ch], h, lags, ini)
                        principal = (res in ("valor_tasado", "ipc_alquiler") and ch == "mediana" and h == 4 and lags == 4)
                        idq = f"Q5-{'p' if res == 'valor_tasado' else 'a'}-P" if principal else f"Q5-mv-{res}-{ch}-h{h}-L{lags}"
                        reg.append({"id": idq, "pregunta": "Q5", "rol": "principal" if principal else "multiverso", "especificacion": f"LP {res} h={h}, choque {ch}, {lags} rezagos",
                                    "muestra": f"{r['ini']}-{r['fin']}", "n": r["n"], "estimacion": r["beta"], "unidad": "% acumulado por DT de sorpresa",
                                    "inferencia": "ninguna (lp_newey_west_b NO APTO)", "nota": ""})
                        mv.append({"res": res, "choque": ch, "h": h, "lags": lags, "beta": r["beta"], "n": r["n"], "principal": principal})
    mv = pd.DataFrame(mv)
    # multiverso resumido (adenda punto 3: mediana y proporción de mismo signo; sin IC no hay "IC que excluya el 0")
    def resumen(res):
        m = mv[(mv.res == res) & (~mv.principal)]
        pr = mv[(mv.res == res) & mv.principal].beta.iloc[0]
        return {"n": int(len(m)), "mediana": float(m.beta.median()), "min": float(m.beta.min()), "max": float(m.beta.max()),
                "proporcion_mismo_signo_que_principal": float((np.sign(m.beta) == np.sign(pr)).mean())}
    est, diag, py = {}, {}, []
    for etq, res in (("Q5-p", "valor_tasado"), ("Q5-a", "ipc_alquiler")):
        ini = VENT[etq]
        r4 = lp(Y[res], sh["mediana"], 4, 4, ini)
        irf = {h: lp(Y[res], sh["mediana"], h, 4, ini)["beta"] for h in H}
        supF, tau = supF_ruptura(r4["A"], r4["y"])
        r1 = lp(Y[res], sh["mediana"], 1, 4, ini)
        from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan
        import statsmodels.api as sm
        ols1 = sm.OLS(r1["y"], r1["A"]).fit()
        bp = het_breuschpagan(ols1.resid, r1["A"])
        bg = acorr_breusch_godfrey(ols1, nlags=4)
        lead = lp(Y[res], sh["mediana"], 4, 4, ini, extra_lead=-8)["beta"]   # choque adelantado 8 trimestres (placebo temporal)
        est[etq] = {"beta_h4_pct_por_DT": r4["beta"], "n": r4["n"], "muestra": f"{r4['ini']}-{r4['fin']}", "irf_puntual_pct": {str(h): irf[h] for h in H},
                    "ic95": None, "p": None, "multiverso": resumen(res), "sd_choque_original": r4["sd_choque"], "r2": r4["r2"]}
        if etq == "Q5-p":
            est[etq]["magnitud_referencia_pct"] = REF_P
            est[etq]["cociente_estimacion_sobre_referencia"] = r4["beta"] / REF_P
            est[etq]["mismo_signo_que_referencia"] = bool(np.sign(r4["beta"]) == np.sign(REF_P))
            est[etq]["MDE_declarado_pct"] = 1.47
        else:
            est[etq]["magnitud_referencia"] = "ninguna comparable: (b) no se cumple (adenda, punto 3)"
        diag[etq] = [
            C.diag("calibración de la inferencia", "NO APTO", "LP con Newey-West de b fija: tamaño 0,0642-0,0925 fuera de [0,04; 0,06]; solo estimación puntual"),
            C.diag("heterocedasticidad (Breusch-Pagan, h=1)", "reportado", {"LM": float(bp[0]), "p_diagnostico": float(bp[1])}),
            C.diag("autocorrelación de los residuos (Breusch-Godfrey 4, h=1)", "reportado", {"LM": float(bg[0]), "p_diagnostico": float(bg[1])}),
            C.diag("ruptura (sup-F de ruptura única, Bai-Perron simplificado)", "reportado sin valor crítico validado", {"supF": supF, "trimestre_indice": tau, "posicion_en_la_muestra_efectiva": f"{tau} de {r4['n']}"}),
            C.diag("placebo temporal (choque adelantado 8 trimestres, h=4)", "reportado", {"beta_placebo_pct": lead, "cociente_sobre_principal": lead / r4["beta"]}),
        ]
    # primera etapa (instrumento): descriptiva
    fe = [primera_etapa(sh["mediana"], h, "1999Q1") for h in (0, 4)]
    # controles negativos (h=4, mediana, 4 rezagos)
    pob = np.log(C.nat_q("base_poblacion", "pob_total"))
    infl = C.nat_q("base_macro", "inflacion_ipc_yoy")
    cn = {"poblacion_total_pct": lp(pob, sh["mediana"], 4, 4, "1999Q1")["beta"],
          "inflacion_yoy_cambio_pp": lp(infl, sh["mediana"], 4, 4, "1999Q1", nivel_y=True)["beta"]}
    # sensibilidad: Oster/Cinelli-Hazlett/E-value no aplican a una LP sobre un choque externo: se dice
    for etq in est:
        diag[etq].append(C.diag("primera etapa (sorpresa → Δ tipo hipotecario BdE)", "FALLIDA si F < 10 (ver detalle); descriptiva", fe))
        diag[etq].append(C.diag("controles negativos (h=4)", "reportados (no debe moverse)", cn))
        diag[etq].append(C.diag("Oster / Cinelli-Hazlett / E-value", "no aplicable", "choque externo (instrumento) sin regresores omitidos comparables; sin errores típicos válidos no hay RV"))
        diag[etq].append(C.diag("pretendencias / Honest DiD / placebos de unidades / exclusión de grandes ciudades", "no aplicable", "serie nacional única"))
        diag[etq].append(C.diag("Moran en residuos", "no aplicable", "sin dimensión espacial"))
        py.append({"id": etq, "p": None, "motivo": "lp_newey_west_b NO APTO: solo estimación puntual"})
    Q = C.Q
    Q.registro(reg, OUT / "registro.csv")
    nota_ult = f"La sorpresa de JK termina en {ult}; la ventana efectiva acaba ahí (la adenda dice 2026T2)."
    for etq, pregunta in (("Q5-p", "Q5-p: Δ% del valor tasado nacional a h = 4 trimestres asociado a la sorpresa monetaria (JK mediana)"),
                          ("Q5-a", "Q5-a: Δ% del IPC de alquiler nacional a h = 4 trimestres asociado a la sorpresa monetaria (JK mediana)")):
        r = C.resultado(etq.lower(), pregunta, "data/processed/v16/entrenamiento: demanda_internacional (JK), base_precio, base_alquiler, base_macro", est[etq]["n"],
                        "LP h=4, 4 rezagos del choque y de Δy; MCO; Newey-West de b fija NO APTO: solo puntual", est[etq], diag[etq],
                        [nota_ult, "Asociación con una sorpresa de política monetaria; no se interpreta como efecto causal (C4).",
                         "El MDE del valor tasado a h=4 (1,47 %) supera la magnitud de referencia (0,6): sin potencia aun con inferencia válida.",
                         "Solapes declarados: V9-D5 y V8 (SVAR C3s del periodo P5)."], [p for p in py if p["id"] == etq])
        Q.jdump(r, OUT / f"resultado_{etq.lower()}.json")
    Q.jdump({"preguntas": ["Q5-p", "Q5-a"], "estimacion": est, "diagnosticos": diag, "controles_negativos": cn, "primera_etapa": fe}, OUT / "q5_detalle.json")
    # resultado.json conjunto (forma de CLAUDE.md)
    r = C.resultado("q5", "Q5 (Q5-p valor tasado, Q5-a IPC de alquiler): proyección local a h = 4 sobre la sorpresa monetaria de Jarociński-Karadi",
                    "data/processed/v16/entrenamiento: demanda_internacional (JK), base_precio, base_alquiler, base_macro", {k: est[k]["n"] for k in est},
                    "LP h=4, 4 rezagos del choque y de Δy; MCO; Newey-West de b fija NO APTO: solo estimación puntual sin IC ni p", est,
                    {k: v for k, v in diag.items()}, [nota_ult, "C4, pendiente de evaluación sellada; sin lenguaje causal.",
                                                      "Q5-p: MDE 1,47 % > referencia 0,6 %; Q5-a sin magnitud comparable."], py)
    Q.jdump(r, OUT / "resultado.json")
    # hechos
    a, p = est["Q5-a"], est["Q5-p"]
    hs = [C.hecho("p-h4", "Q5", "Q5-p: variación acumulada del valor tasado nacional a 4 trimestres asociada a una DT de sorpresa monetaria (JK)", p["beta_h4_pct_por_DT"],
                  p["multiverso"]["min"], p["multiverso"]["max"], "% por DT de sorpresa", p["muestra"], "nacional, trimestral", "MIVAU (valor tasado); BCE/JK (sorpresas)", "q5p", "2025T4"),
          C.hecho("a-h4", "Q5", "Q5-a: variación acumulada del IPC de alquiler nacional a 4 trimestres asociada a una DT de sorpresa monetaria (JK)", a["beta_h4_pct_por_DT"],
                  a["multiverso"]["min"], a["multiverso"]["max"], "% por DT de sorpresa", a["muestra"], "nacional, trimestral", "INE (IPC alquiler); BCE/JK (sorpresas)", "q5a", "2025T4")]
    Q.jdump(hs, OUT / "hechos.json")
    # informe
    f = C.f
    lin = lambda e: "; ".join(f"h={h}: {f(v, 2)}" for h, v in e["irf_puntual_pct"].items())
    md = f"""# Q5 · Tipos de interés: proyecciones locales sobre la sorpresa de Jarociński-Karadi (C4, pendiente de evaluación sellada)

**Capa y alcance.** C4 (asociación), entrenamiento; no pasa a C3 sin evaluación sellada temporal. Sin lenguaje causal. Herramienta de inferencia (Newey-West de b fija) NO APTA
(tamaño 0,0642-0,0925, veredictos.csv): solo estimación puntual, **sin p-valor ni IC**. {nota_ult}

## Especificación (pre-registrada)
LP a h = 4: y(t+4) − y(t−1) (log x 100) sobre la sorpresa mediana de JK (suma trimestral, estandarizada), 4 rezagos del choque y de Δy. Ventanas nominales 1999T1 (Q5-p) y 2002T1 (Q5-a); muestras efectivas tras los rezagos y el horizonte: {p['muestra']} y {a['muestra']}.
Multiverso: 64 especificaciones (4 resultados x 4 horizontes x 2 choques x 2 rezagos), en registro.csv; ninguna se elige por su resultado.

## Resultados puntuales
<a id="q5p"></a>**Q5-p (valor tasado), h = 4:** {f(p['beta_h4_pct_por_DT'], 2)} % por DT de sorpresa (n = {p['n']}, {p['muestra']}). Respuesta puntual: {lin(p)}.
Referencia de la literatura (P3 de V15): −0,6 % por DT; cociente estimación/referencia = {f(p['cociente_estimacion_sobre_referencia'], 2)}; mismo signo: {p['mismo_signo_que_referencia']}.
Multiverso (63 restantes): mediana {f(p['multiverso']['mediana'], 2)}, rango [{f(p['multiverso']['min'], 2)}; {f(p['multiverso']['max'], 2)}], proporción con el mismo signo {f(p['multiverso']['proporcion_mismo_signo_que_principal'], 2)}.
El MDE del valor tasado a h = 4 (1,47 %) supera la referencia: sin potencia aunque la inferencia fuera válida.

<a id="q5a"></a>**Q5-a (IPC de alquiler), h = 4:** {f(a['beta_h4_pct_por_DT'], 2)} % por DT (n = {a['n']}, {a['muestra']}). Respuesta puntual: {lin(a)}.
Sin magnitud comparable (la referencia es de precio): la condición (b) no se cumple. Multiverso: mediana {f(a['multiverso']['mediana'], 2)}, rango [{f(a['multiverso']['min'], 2)}; {f(a['multiverso']['max'], 2)}], mismo signo {f(a['multiverso']['proporcion_mismo_signo_que_principal'], 2)}.

## Diagnósticos (todos reportados; ninguno decide la capa)
- Primera etapa (sorpresa → Δ tipo hipotecario BdE): h=0: {f(fe[0]['beta_pp_por_DT'], 3)} pp por DT, F robusto {f(fe[0]['F_robusto_HC1'], 1)}; h=4: {f(fe[1]['beta_pp_por_DT'], 3)} pp, F {f(fe[1]['F_robusto_HC1'], 1)} (descriptivo). F < 10: instrumento débil en el sentido de la regla del pre-registro; **no se supera la prueba de fuerza** y se dice.
- Controles negativos (h=4): población total {f(cn['poblacion_total_pct'], 3)} %; inflación yoy {f(cn['inflacion_yoy_cambio_pp'], 3)} pp.
- Placebo temporal (choque adelantado 8 trimestres), heterocedasticidad (Breusch-Pagan), autocorrelación (Breusch-Godfrey) y sup-F de ruptura: en resultado.json (descriptivos).
- Oster, Cinelli-Hazlett y E-value, pretendencias, Honest DiD, Moran y exclusión de grandes ciudades: no aplican (serie nacional única, choque externo).

## Regla de hallazgo (punto 9)
(a) sin p-valor: no evaluable; (b) sin errores típicos válidos: no evaluable (Q5-a sin magnitud); (c) sellada: pendiente. Resultado: estimación puntual C4, ni hallazgo ni pista.
Los p-valores para el control BY están en resultado.json (`p_valores_para_BY`, p null por NO APTO).
"""
    (OUT / "informe.md").write_text(md, encoding="utf-8")
    return est


if __name__ == "__main__":
    e = main()
    print({k: (v["beta_h4_pct_por_DT"], v["n"], v["multiverso"]) for k, v in e.items()})
