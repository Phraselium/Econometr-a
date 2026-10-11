"""M2 v6: tabla «peso de cada variable», BH del registro, resultado.json y hechos.json. Sin red, determinista."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/v6/M2"
T = OUT / "tablas"
PAN = ROOT / "output/v6/M0/paneles"
FECHA = "2026-10-11"
COMUNES = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_vut", "ln_terminadas_libres", "ln_iniciadas_libres"]
LN10 = float(np.log(1.1))


def delta(v):
    """Unidad interpretable: +10 % en variables ln_, +1 pp en share_/paro, +1 municipio en contadores."""
    if v.startswith("ln_"):
        return LN10, "+10 %"
    if v.startswith("share_") or v.startswith("paro"):
        return 1.0, "+1 pp"
    return 1.0, "+1 municipio"


def bh(pv, q=0.10):
    p = np.asarray(pv, float)
    n = len(p)
    o = np.argsort(p)
    adj = np.empty(n)
    adj[o] = np.minimum.accumulate((p[o] * n / (np.arange(n) + 1))[::-1])[::-1]
    return np.clip(adj, 0, 1)


def niveles():
    pa = pd.read_csv(PAN / "prov_alquiler_anual_train.csv.gz")
    pc = pd.read_csv(PAN / "prov_compra_anual_train.csv.gz")
    return float(np.exp(pa["ln_alq_mes_serpavi_vc"]).mean()), float(np.exp(pc["ln_pm2_tasado"]).mean())


def bloque(nombre, escala, unidad_abs):
    b = pd.read_csv(T / f"bma_{nombre}.csv")
    u = b[b.prior == "uniforme"]
    bb = b[b.prior == "betabin"][["variable", "muestra", "pip"]].rename(columns={"pip": "pip_betabin"})
    c = u[u.muestra == "completa"].merge(bb[bb.muestra == "completa"][["variable", "pip_betabin"]], on="variable")
    nuc = u[u.muestra == "nucleo"][["variable", "pip"]].rename(columns={"pip": "pip_nucleo"})
    c = c.merge(nuc, on="variable", how="left")
    mv = pd.read_csv(T / f"multiverso_resumen_{nombre}.csv")
    pdsd = pd.read_csv(T / f"pds_{nombre}.csv")
    pdsd = pdsd[pdsd.muestra == "completa"][["variable", "seleccion_enet", "coef_pds", "ic_lo", "ic_hi", "p_pds"]]
    r = c.merge(mv, on="variable", how="left").merge(pdsd, on="variable", how="left")
    rows = []
    for _, x in r.iterrows():
        d, ud = delta(x.variable)
        pct = lambda z: 100 * z * d  # noqa: E731
        rows.append({
            "variable": x.variable, "unidad": ud, "pip": x.pip, "pip_betabin": x.pip_betabin,
            "pip_nucleo": x.pip_nucleo,
            "bma_media_pct": pct(x.media_post), "bma_q025_pct": pct(x.q025), "bma_q975_pct": pct(x.q975),
            "mv_mediana_pct": pct(x.mediana), "mv_p25_pct": pct(x.p25), "mv_p75_pct": pct(x.p75),
            "mv_abs_mediana": x.mediana * d * escala, "mv_abs_p25": x.p25 * d * escala, "mv_abs_p75": x.p75 * d * escala,
            "unidad_abs": unidad_abs, "mv_pct_mismo_signo": x.pct_mismo_signo, "mv_n_spec": x.n_spec,
            "pds_seleccion_enet": bool(x.seleccion_enet), "pds_coef_pct": pct(x.coef_pds),
            "pds_ic_lo_pct": pct(x.ic_lo), "pds_ic_hi_pct": pct(x.ic_hi), "pds_p": x.p_pds,
            "n_bma": x.n, "capa": "C4"})
    return pd.DataFrame(rows)


def main():
    alq_mes, pm2 = niveles()
    A = bloque("alq_stock_prov", alq_mes, "€/mes")
    C = bloque("compra_precio_prov", pm2, "€/m²")
    V = bloque("compra_volumen_prov", 1.0, "% (volumen)")
    A.to_csv(OUT / "peso_alquiler_prov.csv", index=False)
    C.to_csv(OUT / "peso_compra_prov.csv", index=False)
    V.to_csv(OUT / "peso_variables_volumen.csv", index=False)
    vars_ = list(dict.fromkeys(list(A.variable) + list(C.variable)))
    W = pd.DataFrame({"variable": vars_})
    W = W.merge(A.add_prefix("ALQ_").rename(columns={"ALQ_variable": "variable"}), on="variable", how="left")
    W = W.merge(C.add_prefix("COMPRA_").rename(columns={"COMPRA_variable": "variable"}), on="variable", how="left")

    def disc(r):
        if r.variable not in COMUNES:
            return "no comparable (solo en un mercado)"
        a, c = r.ALQ_pip, r.COMPRA_pip
        an, cn = r.ALQ_pip_nucleo, r.COMPRA_pip_nucleo
        f = []
        if a >= .5 and c < .2:
            f.append("pesa en ALQUILER y no en COMPRA (set completo)")
        if c >= .5 and a < .2:
            f.append("pesa en COMPRA y no en ALQUILER (set completo)")
        if an >= .5 and cn < .2:
            f.append("pesa en ALQUILER y no en COMPRA (núcleo)")
        if cn >= .5 and an < .2:
            f.append("pesa en COMPRA y no en ALQUILER (núcleo)")
        return "; ".join(f) if f else "sin discrepancia"
    W["discrepancia_mercados"] = W.apply(disc, axis=1)
    W["capa"] = "C4"
    W.to_csv(OUT / "peso_variables.csv", index=False)

    def f(x, n=2):
        return "–" if pd.isna(x) else f"{x:.{n}f}"
    L = ["# Peso de cada variable (M2, provincia) — C4, asociativo", "",
         f"Fecha: {FECHA}. PIP = soporte predictivo/asociativo dentro del espacio de modelos, NO efecto causal. "
         "Datos: paneles *_train de M0 (anual, provincia); variables en t−1 con FE de unidad y año fuera del promedio. "
         "g-prior g = max(N, K²); prior uniforme (columna PIP) y beta-binomial(1,1) (PIP bb). "
         "«PIP núcleo» = BMA sin ln_vut ni ln_suelo (más observaciones). Rango BMA = intervalo creíble 95 %; "
         "mult. = mediana [p25; p75] del multiverso. Unidad: +10 % en variables ln_, +1 pp en share_/paro, "
         "+1 municipio en contadores. ALQUILER = stock SERPAVI, €/m²/mes → %, y €/mes con el alquiler medio del panel "
         f"({alq_mes:.0f} €/mes). COMPRA = valor tasado MIVAU → %, y €/m² con el precio medio del panel ({pm2:.0f} €/m²). "
         "Mismo signo = % de especificaciones con el signo de la mediana. Sel. enet = elastic net conjunto (CV en bloques, embargo 1 año).", ""]
    for nm, D, ab in [("ALQUILER (stock, SERPAVI; medida: mediana VC)", A, "€/mes"),
                      ("COMPRA, precio (medida_precio: valor tasado MIVAU)", C, "€/m²"),
                      ("COMPRA, volumen (compraventas INE ETDP; efecto en %)", V, "%")]:
        L += [f"## {nm}", "",
              "| Variable | Unidad | PIP | PIP bb | PIP núcleo | BMA media % [IC95] | Mult. mediana % [p25; p75] | " +
              ("Mult. " + ab + " | " if ab != "%" else "") + "% mismo signo | Sel. enet | PDS coef % [IC95] | Capa |",
              "|---|---|---|---|---|---|---|" + ("---|" if ab != "%" else "") + "---|---|---|---|"]
        for _, r in D.iterrows():
            L.append(f"| {r.variable} | {r.unidad} | {f(r.pip)} | {f(r.pip_betabin)} | {f(r.pip_nucleo)} | "
                     f"{f(r.bma_media_pct)} [{f(r.bma_q025_pct)}; {f(r.bma_q975_pct)}] | "
                     f"{f(r.mv_mediana_pct)} [{f(r.mv_p25_pct)}; {f(r.mv_p75_pct)}] | " +
                     (f"{f(r.mv_abs_mediana)} [{f(r.mv_abs_p25)}; {f(r.mv_abs_p75)}] | " if ab != "%" else "") +
                     f"{f(r.mv_pct_mismo_signo, 0)} | {'sí' if r.pds_seleccion_enet else 'no'} | "
                     f"{f(r.pds_coef_pct)} [{f(r.pds_ic_lo_pct)}; {f(r.pds_ic_hi_pct)}] | C4 |")
        L.append("")
    L += ["## Variables que pesan en un mercado y no en el otro (PIP ≥ 0,5 en uno y < 0,2 en el otro)", ""]
    ds = W[W.discrepancia_mercados.str.startswith("pesa")]
    if ds.empty:
        L.append("Ninguna variable común cumple el criterio.")
    for _, r in ds.iterrows():
        L.append(f"- **{r.variable}**: {r.discrepancia_mercados}. PIP alquiler {f(r.ALQ_pip)} (núcleo {f(r.ALQ_pip_nucleo)}), "
                 f"PIP compra {f(r.COMPRA_pip)} (núcleo {f(r.COMPRA_pip_nucleo)}).")
    L += ["", "Lectura: C4 en todas las filas; veredicto máximo «ANALIZADA, NO CONCLUYENTE». Sin lenguaje causal. "
          "El BMA completo usa solo observaciones con ln_vut y ln_suelo disponibles (alquiler N=" +
          f"{int(A.n_bma.iloc[0])}, compra N={int(C.n_bma.iloc[0])}), por lo que su potencia es baja."]
    (OUT / "peso_variables.md").write_text("\n".join(L), encoding="utf-8")

    # BH sobre el registro
    R = pd.read_csv(OUT / "registro.csv")
    m = R.p_interes.notna()
    R["p_bh"] = np.nan
    R.loc[m, "p_bh"] = bh(R.loc[m, "p_interes"].values)
    R["bh_q10"] = R.p_bh < 0.10
    R.to_csv(OUT / "registro_bh.csv", index=False)
    nb = int(R.bh_q10.sum())
    nreg = int(m.sum())

    # resultado.json y hechos.json
    def top(D, k=3):
        return [{"variable": r.variable, "pip": round(float(r.pip), 3)} for _, r in D.sort_values("pip", ascending=False).head(k).iterrows()]
    nmin = {"alquiler_prov_completa": int(A.n_bma.iloc[0]), "compra_prov_completa": int(C.n_bma.iloc[0])}
    base = {
        "rama": "v6/M2", "capa": "C4", "nivel_evidencia": "EXPLORATORIO",
        "pregunta": "Incertidumbre de modelo en alquiler (stock) y compra (precio y volumen): PIP, PDS y multiverso.",
        "metodo": "BMA (enumeración, g=max(N,K²), uniforme y beta-binomial), elastic net + PDS con CV en bloques y embargo 1 año, "
                  "multiverso de especificaciones; FE de unidad y año; BH q=0,10 sobre el registro.",
        "datos": "output/v6/M0/paneles/*_train.csv.gz (provincia anual; municipio y distrito con regresores provinciales unidos)",
        "N": nmin,
        "estimacion": {"alquiler_prov": A[["variable", "pip", "bma_media_pct", "mv_mediana_pct", "mv_pct_mismo_signo"]].round(4).to_dict("records"),
                       "compra_precio_prov": C[["variable", "pip", "bma_media_pct", "mv_mediana_pct", "mv_pct_mismo_signo"]].round(4).to_dict("records"),
                       "compra_volumen_prov": V[["variable", "pip", "bma_media_pct", "mv_mediana_pct", "mv_pct_mismo_signo"]].round(4).to_dict("records")},
        "ic95": {"alquiler_prov": {r.variable: [round(r.bma_q025_pct, 3), round(r.bma_q975_pct, 3)] for _, r in A.iterrows()},
                 "compra_precio_prov": {r.variable: [round(r.bma_q025_pct, 3), round(r.bma_q975_pct, 3)] for _, r in C.iterrows()}},
        "p_ajustado": {"metodo": "BH q=0,10 sobre registro (multiverso + PDS)", "n_contrastes": nreg, "n_rechazos": nb,
                       "archivo": "output/v6/M2/registro_bh.csv"},
        "diagnosticos": {"top_pip_alquiler": top(A), "top_pip_compra_precio": top(C), "top_pip_compra_volumen": top(V),
                         "discrepancias_mercados": ds[["variable", "discrepancia_mercados"]].to_dict("records")},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "mercado": ["alquiler de stock (SERPAVI)", "precio de compra", "volumen de compra"],
        "medida_precio": "valor tasado MIVAU (provincia y municipio); robustez: Registradores",
        "notas": "Sin modelo de contratos nuevos (N≈15, pre-registro §3). Fuera de muestra no evaluado en M2 (se hace en M4 con "
                 "evaluate_v6). PIP mide soporte asociativo; nada causal. Ver desviaciones.md.",
    }
    (OUT / "resultado.json").write_text(json.dumps(base, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    hechos = []
    for tag, D, mk, per in [("alq", A, "alquiler de stock (SERPAVI)", "2015-2023"), ("cp", C, "precio de compra (tasado MIVAU)", "2015-2024"),
                            ("cv", V, "volumen de compra (INE ETDP)", "2015-2024")]:
        for _, r in D.iterrows():
            hechos.append({"id": f"m2_pip_{tag}_{r.variable}", "indicador": f"PIP BMA de {r.variable}, {mk}, provincia",
                           "valor": round(float(r.pip), 4), "min": round(float(r.pip_nucleo), 4) if pd.notna(r.pip_nucleo) else None,
                           "max": round(float(r.pip_betabin), 4), "unidad": "probabilidad",
                           "periodo": per, "cobertura": "provincias con datos en el panel de entrenamiento",
                           "fuentes": ["output/v6/M0/paneles"], "capa": "C4", "fecha_dato": FECHA})
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1), encoding="utf-8")
    print(W[["variable", "ALQ_pip", "COMPRA_pip", "ALQ_pip_nucleo", "COMPRA_pip_nucleo", "discrepancia_mercados"]].round(2).to_string())
    print("BH", nb, nreg)


if __name__ == "__main__":
    main()
