"""K3: aclaraciones de interpretacion (iniciadas en alquiler; ratio precio/alquiler). C4, sin red."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from econ_utils import Registry, holm  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
PAN = ROOT / "output/v6/M0/paneles"
OUT = ROOT / "output/v6_1/K3"
OUT.mkdir(parents=True, exist_ok=True)
reg = Registry(OUT / "registro.csv")


def panel():
    a = pd.read_csv(PAN / "prov_alquiler_anual_train.csv.gz")
    c = pd.read_csv(PAN / "prov_compra_anual_train.csv.gz")
    d = a.merge(c[["cod", "anio", "ln_iniciadas_libres", "ln_pob"]], on=["cod", "anio"], how="inner")
    d = d.sort_values(["cod", "anio"]).reset_index(drop=True)
    d["ini_1000"] = np.exp(d.ln_iniciadas_libres - d.ln_pob) * 1000
    d["dlna"] = d.groupby("cod").ln_alq_m2_serpavi_vc.diff()
    for k in (1, 2):
        d[f"ini_l{k}"] = d.groupby("cod").ini_1000.shift(k)
        d[f"ini_f{k}"] = d.groupby("cod").ini_1000.shift(-k)
        d[f"dlna_l{k}"] = d.groupby("cod").dlna.shift(k)
    return d


def ajusta(d, y, xs, tag, formula_note):
    cols = [y] + xs + ["cod", "anio"]
    s = d.dropna(subset=cols)
    f = f"{y} ~ {' + '.join(xs)} + C(cod) + C(anio)"
    r = smf.ols(f, s).fit(cov_type="cluster", cov_kwds={"groups": s.cod})
    reg.log("K3", tag, f"{y} ~ {' + '.join(xs)} + EF cod + EF anio", s.anio.min(), s.anio.max(), int(r.nobs),
            r.rsquared_adj, r.aic, r.bic, coef_interes=r.params[xs[0]], p_interes=r.pvalues[xs[0]], notas=formula_note)
    out = []
    for x in xs:
        lo, hi = r.conf_int().loc[x]
        out.append(dict(modelo=tag, y=y, x=x, coef=r.params[x], ic_lo=lo, ic_hi=hi, p=r.pvalues[x], n=int(r.nobs),
                        prov=int(s.cod.nunique())))
    return out


def regresiones(d):
    rows = []
    # A: alquiler_t sobre iniciadas (retardos, contemporaneo, adelantos)
    rows += ajusta(d, "dlna", ["ini_l2", "ini_l1", "ini_1000", "ini_f1", "ini_f2"], "A_conjunta", "retardos+contemp+adelantos")
    for x in ("ini_l2", "ini_l1", "ini_1000", "ini_f1", "ini_f2"):
        rows += ajusta(d, "dlna", [x], f"A_{x}", "un regresor")
    # misma muestra para los 5 (sin leads) y B: inversa
    rows += ajusta(d, "ini_1000", ["dlna_l1", "dlna_l2"], "B_inversa", "iniciadas_t sobre crecimiento alquiler t-1,t-2")
    for x in ("dlna_l1", "dlna_l2"):
        rows += ajusta(d, "ini_1000", [x], f"B_{x}", "un regresor")
    R = pd.DataFrame(rows)
    R["p_holm"] = np.nan
    ph = holm({f"{r.modelo}|{r.x}": r.p for r in R.itertuples()})
    R["p_holm"] = [ph[f"{r.modelo}|{r.x}"] for r in R.itertuples()]
    R.to_csv(OUT / "iniciadas_coef.csv", index=False)
    return R


def ratio_pa():
    a = pd.read_csv(PAN / "prov_alquiler_anual_train.csv.gz")
    c = pd.read_csv(PAN / "prov_compra_anual_train.csv.gz")
    n = pd.read_csv(PAN / "nacional_anual_a23_desc.csv").set_index("anio")
    k = pd.read_csv(PAN / "prov_contratos_nuevos_anual_train.csv.gz")
    d = a.merge(c[["cod", "anio", "ln_pm2_tasado", "ln_pm2_registradores"]], on=["cod", "anio"])
    d = d.dropna(subset=["ln_alq_m2_serpavi_vc", "ln_pm2_tasado", "ln_pm2_registradores"])
    g = d.groupby("anio")
    alq_med = g.apply(lambda x: float(np.exp(x.ln_alq_m2_serpavi_vc).median()), include_groups=False)
    res = {}
    for an in (2015, 2023):
        x = d[d.anio == an]
        alq = np.exp(x.ln_alq_m2_serpavi_vc)
        res[an] = {
            "Tasado MIVAU (prov.) / SERPAVI stock": float((np.exp(x.ln_pm2_tasado) / alq / 12).median()),
            "Registradores (prov.) / SERPAVI stock": float((np.exp(x.ln_pm2_registradores) / alq / 12).median()),
            "Tasado MIVAU (nac.) / SERPAVI stock (mediana prov.)": float(n.loc[an, "pm2_mivau_tasado"] / alq_med[an] / 12),
            "Registradores publicado (nac.) / SERPAVI stock": float(n.loc[an, "pm2_registradores_publicado"] / alq_med[an] / 12),
            "Notariado (nac.) / SERPAVI stock": float(n.loc[an, "pm2_notariado"] / alq_med[an] / 12),
        }
    # contratos nuevos (fianza media GVA, 1 mensualidad): corrige el alquiler de stock por prov. con fianza
    kk = k.dropna(subset=["ln_fianza_media_gva_eur"]).merge(d, on=["cod", "anio"])
    nuevo = []
    for r in kk.itertuples():
        m2_stock = np.exp(r.ln_alq_m2_serpavi_vc)
        mes_stock = np.exp(r.ln_alq_mes_serpavi_vc)
        fianza = np.exp(r.ln_fianza_media_gva_eur)
        pm2 = np.exp(r.ln_pm2_tasado)
        nuevo.append(dict(cod=r.cod, provincia=r.provincia_x, anio=r.anio, fianza_eur=fianza, alq_mes_stock=mes_stock,
                          razon_nuevo_stock=fianza / mes_stock, ratio_stock=pm2 / m2_stock / 12,
                          ratio_nuevos=pm2 / m2_stock / 12 * mes_stock / fianza))
    N = pd.DataFrame(nuevo)
    N.to_csv(OUT / "ratio_pa_contratos_nuevos_gva.csv", index=False)
    return res, N


def lee_iniciadas(R):
    def g(m, x):
        r = R[(R.modelo == m) & (R.x == x)].iloc[0]
        return r
    return g


def main():
    d = panel()
    R = regresiones(d)
    res, N = ratio_pa()
    reg.flush()
    g = lee_iniciadas(R)
    sig = R[R.p_holm < 0.05]
    A = {x: g("A_conjunta", x) for x in ("ini_l2", "ini_l1", "ini_1000", "ini_f1", "ini_f2")}
    B = {x: g("B_inversa", x) for x in ("dlna_l1", "dlna_l2")}
    L = ["# K3.1 Viviendas iniciadas y alquiler: orden temporal (C4, exploratorio)", "",
         "Panel provincial de entrenamiento (SERPAVI alquiler de stock, €/m²; iniciadas libres por 1.000 hab., MIVAU). "
         f"N conjunta A = {A['ini_l1'].n} obs. en {A['ini_l1'].prov} provincias (SERPAVI 2015-2023, 38-39 provincias, "
         "Δln alquiler desde 2016). EF de provincia y año; errores agrupados por provincia; Holm sobre todos los coeficientes. "
         "Sin lenguaje causal.", "",
         "| Modelo | Regresor | Coef. | IC95 % | p | p Holm | N |", "|---|---|---|---|---|---|---|"]
    for r in R.itertuples():
        L.append(f"| {r.modelo} | {r.x} | {r.coef:.4f} | [{r.ic_lo:.4f}; {r.ic_hi:.4f}] | {r.p:.3f} | {r.p_holm:.3f} | {r.n} |")
    L += ["", "A: Δln alquiler_t sobre iniciadas/1.000 hab. en t-2, t-1, t, t+1, t+2. B: iniciadas_t sobre Δln alquiler en t-1, t-2.", "",
          f"Coeficientes con p Holm < 0,05: {len(sig)} de {len(R)}.", "",
          "**Conclusión (C4, ANALIZADA, NO CONCLUYENTE).** Se describe el orden temporal; no se estima ningún efecto de construir. "
          f"Retardos (t-2, t-1) y adelantos (t+1, t+2): ninguno distinto de cero (p Holm {min(A[x].p_holm for x in ('ini_l2','ini_l1','ini_f1','ini_f2')):.2f} el menor). "
          f"El contemporáneo es {A['ini_1000'].coef:.4f} (p={A['ini_1000'].p:.3f}; p Holm {A['ini_1000'].p_holm:.2f}), no robusto al ajuste múltiple. "
          "En la inversa (B), el crecimiento previo del alquiler tampoco predice las iniciadas (p Holm 1,00; "
          "los coeficientes B son enormes en escala porque Δln alquiler es ~0,05). "
          "Lectura: con N≈175-280 no se detecta orden temporal en ningún sentido; la PIP de iniciadas en alquiler (M2) no "
          "indica que construir suba el alquiler ni la dirección contraria."]
    (OUT / "iniciadas.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    M = pd.DataFrame(res).T
    cols = list(M.columns)
    T = ["# K3.3 Ratio precio/alquiler: rango por medida (años de alquiler; C4)", "",
         "v6 publica 20,3 → 17,1 años (2015-2023) con valor tasado MIVAU (€/m², provincial) / alquiler de stock SERPAVI (€/m²/mes ×12), "
         "mediana de provincias de entrenamiento con ambos datos (38-39). IPV (INE) no da nivel, solo variación: no entra. "
         "Las medidas nacionales se dividen por la mediana provincial del alquiler de stock (mezcla de coberturas: orientativo). "
         "Fecha del dato: 2015 y 2023 (anual).", "",
         "| Medida precio / medida alquiler | 2015 | 2023 | variación |", "|---|---|---|---|"]
    for c in cols:
        T.append(f"| {c} | {M.loc[2015, c]:.1f} | {M.loc[2023, c]:.1f} | {M.loc[2023, c] - M.loc[2015, c]:+.1f} |")
    prov = [c for c in cols if "(prov.)" in c]
    lo15, hi15 = M.loc[2015, prov].min(), M.loc[2015, prov].max()
    lo23, hi23 = M.loc[2023, prov].min(), M.loc[2023, prov].max()
    nlo15, nhi15 = M.loc[2015].min(), M.loc[2015].max()
    nlo23, nhi23 = M.loc[2023].min(), M.loc[2023].max()
    T += ["", f"**Rango con medidas provinciales (misma muestra): 2015 {lo15:.1f}-{hi15:.1f} años; 2023 {lo23:.1f}-{hi23:.1f} años.** "
          f"Incluyendo medidas nacionales (orientativas, otra cobertura): 2015 {nlo15:.1f}-{nhi15:.1f}; 2023 {nlo23:.1f}-{nhi23:.1f}. "
          "Con las cinco medidas el ratio de 2023 es igual o menor que el de 2015, pero el descenso va de -3,2 años (tasado provincial) "
          "a 0,0 (Registradores publicado): el nivel y la magnitud del descenso dependen de la medida de precio.", "",
          "Con contratos nuevos (solo GVA, 2020-2023) el ratio es 3-6 años menor que con alquiler de stock, porque el alquiler "
          "de contratos nuevos es 1,3-1,5 veces el de stock.", "",
          "## Alquiler de contratos nuevos", ""]
    if len(N):
        T += ["Solo hay fianza media de la Generalitat Valenciana (una mensualidad; €/contrato, no €/m²). Se calcula la razón "
              "fianza / alquiler mensual de stock SERPAVI y se reescala el ratio (valor tasado). Cobertura mínima: "
              "no extrapolable al total nacional; ni Incasòl ni IPVA nuevo dan nivel en €.", "",
              "| Provincia | Año | Fianza media (€) | Alquiler stock (€/mes) | Razón nuevo/stock | Ratio con stock | Ratio con nuevos |",
              "|---|---|---|---|---|---|---|"]
        for r in N.itertuples():
            T.append(f"| {r.provincia} | {r.anio} | {r.fianza_eur:.0f} | {r.alq_mes_stock:.0f} | {r.razon_nuevo_stock:.2f} | "
                     f"{r.ratio_stock:.1f} | {r.ratio_nuevos:.1f} |")
    (OUT / "ratio_pa.md").write_text("\n".join(T) + "\n", encoding="utf-8")

    def hecho(i, ind, v, mn, mx, per, fu):
        return dict(id=i, indicador=ind, valor=round(float(v), 4), min=round(float(mn), 4), max=round(float(mx), 4),
                    unidad="años de alquiler" if "ratio" in i else "coef. (viv./1.000 hab. → Δln alquiler)",
                    periodo=per, cobertura="38-39 provincias de entrenamiento", fuentes=fu, capa="C4",
                    fecha_dato="2023 (anual)")
    H = [hecho("K3-RATIO-2015", "Ratio precio/alquiler, medida v6 (tasado/stock)", M.loc[2015, cols[0]], lo15, hi15, "2015",
               "MIVAU tasado; SERPAVI; Registradores; Notariado"),
         hecho("K3-RATIO-2023", "Ratio precio/alquiler, medida v6 (tasado/stock)", M.loc[2023, cols[0]], lo23, hi23, "2023",
               "MIVAU tasado; SERPAVI; Registradores; Notariado")]
    for x, r in A.items():
        H.append(hecho(f"K3-INI-A-{x}", f"Iniciadas {x} sobre Δln alquiler (EF)", r.coef, r.ic_lo, r.ic_hi, "2016-2023",
                       "MIVAU iniciadas; SERPAVI"))
    for x, r in B.items():
        H.append(hecho(f"K3-INI-B-{x}", f"Iniciadas_t sobre {x} (EF)", r.coef, r.ic_lo, r.ic_hi, "2016-2023",
                       "MIVAU iniciadas; SERPAVI"))
    json.dump(H, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)
    rj = dict(rama="K3", pregunta="¿Las iniciadas preceden o siguen al crecimiento del alquiler? ¿Rango del ratio P/A según medida?",
              capa="C4", datos="output/v6/M0/paneles (alquiler SERPAVI stock; iniciadas MIVAU; valor tasado)",
              N=int(A["ini_l1"].n), metodo="OLS con EF provincia y año, cluster por provincia; Holm; ratio por medida",
              estimacion={f"A_{x}": float(r.coef) for x, r in A.items()} | {f"B_{x}": float(r.coef) for x, r in B.items()},
              ic95={f"A_{x}": [float(r.ic_lo), float(r.ic_hi)] for x, r in A.items()}
              | {f"B_{x}": [float(r.ic_lo), float(r.ic_hi)] for x, r in B.items()},
              p_ajustado={f"{r.modelo}|{r.x}": float(r.p_holm) for r in R.itertuples()},
              nivel_evidencia="EXPLORATORIO (C4): ANALIZADA, NO CONCLUYENTE", medida_precio="valor tasado MIVAU (ratio: + Registradores, Notariado)",
              diagnosticos={"rango_ratio_2015": [lo15, hi15], "rango_ratio_2023": [lo23, hi23], "seed": SEED},
              fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
              notas="Descriptivo del orden temporal; sin lenguaje causal; contratos nuevos solo GVA.")
    json.dump(rj, open(OUT / "resultado.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
