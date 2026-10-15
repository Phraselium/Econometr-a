"""V9 F3 · D7 contabilidad hogares-viviendas por provincia (contable; sin contraste ni p-valores).
Pre-registro: docs/v9/hipotesis.md (D7) y addendum A1.8 («componente población» y «componente tasa de jefatura»).

1. ΔH = h̄·ΔP (componente población) + P̄·Δh (componente tasa de jefatura), h = H/P, medias del periodo:
   - 2011→2021: hogares = viviendas principales de los censos 2011 (3457) y 2021 (municipios sumados a provincia);
     población del padrón a 1-1-2012 y 1-1-2022 (lo más próximo a las fechas censales de noviembre);
   - 2022→2026 (años 2022-2025): hogares de la ECP a 1-1-2022 (2022T1) y 1-1-2026 (2026T1); población del censo
     anual a 1-1-2022 y 1-1-2025 extrapolada no: se usa la ECP solo para hogares y el censo anual 2022 y 2025 (marcado).
2. ΔP por componentes: saldo exterior y saldo interprovincial (EM 2012-2020; EMCR 2021-2024) y residuo (crecimiento
   natural, ajustes de padrón y diferencias de calendario).
3. Reconciliación del déficit 2021-2025: proyecto (cifras_clave L3-DEF-2125, T1-H10), BdE (LA18) y OCDE (LA21).
C1 solo para recuentos con dos fuentes coincidentes (hogares censo 2021 frente a ECP); el resto C4.
Salidas: output/v9/d7/{descomposicion_provincia.csv, componentes_poblacion.csv, reconciliacion_deficit.csv,
contraste_c1.csv, resultado.json, fig_d7.png}.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paneles as P  # noqa: E402

OUT = P.RAIZ / "output" / "v9" / "d7"
CV = ["03", "12", "46"]


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace(".", "", regex=False), errors="coerce")


def censo2011() -> pd.Series:
    c = pd.read_csv(P.RAW9 / "ine_censos/censo_t3457.csv.gz", sep=";", dtype=str)
    col = c.columns[0]
    es_prov, sig = {}, 1
    for e in c[col].drop_duplicates():
        if e[:2].isdigit() and int(e[:2]) == sig:
            es_prov[e], sig = False, sig + 1
        else:
            es_prov[e] = e[:2].isdigit()
    c = c[c[col].map(es_prov) & (c["Tipo de vivienda"] == "Vivienda principal")]
    return num(c.Total).set_axis(c[col].str[:2]).groupby(level=0).sum()


def censo2021() -> pd.Series:
    v = pd.read_csv(P.RAW / "v3/ine_v3_censo2021_municipio_viviendas.csv", dtype={"codigo": str})
    v = v[(v.serie == "V_PRINCIPAL") & (v.nivel == "municipio")]
    return v.groupby(v.codigo.str[:2]).valor.sum()


def ecp_hogares() -> pd.DataFrame:
    h = pd.read_csv(P.RAW / "ine_v2_hogares_prov.csv", dtype=str)
    h = h[(h.desglose == "tamaño=Total") & (h.nivel == "provincia")]
    h["v"] = pd.to_numeric(h.valor)
    return h.pivot_table(index="codigo", columns="periodo", values="v")


def descomponer(H0, H1, P0, P1) -> pd.DataFrame:
    h0, h1 = H0 / P0, H1 / P1
    d = pd.DataFrame({"H0": H0, "H1": H1, "P0": P0, "P1": P1, "h0": h0, "h1": h1})
    d["dH"] = d.H1 - d.H0
    d["comp_poblacion"] = (d.h0 + d.h1) / 2 * (d.P1 - d.P0)
    d["comp_jefatura"] = (d.P0 + d.P1) / 2 * (d.h1 - d.h0)
    return d


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pad = P.padron_nac("provincia")
    ptot = pad[pad.nacionalidad == "Total"].pivot_table(index="cod_provincia", columns="anio", values="poblacion")
    pext = pad[pad.nacionalidad == "Extranjera"].pivot_table(index="cod_provincia", columns="anio", values="poblacion")
    ca = pd.read_csv(P.RAW9 / "ine_censo_anual/censo_municipio_sexo.csv.gz", dtype={"cod_municipio": str, "edicion": str})
    ca = ca[ca.sexo.isin(["Total", "Ambos sexos"])] if ca.sexo.isin(["Total", "Ambos sexos"]).any() else ca
    cap = ca.groupby([ca.cod_municipio.str[:2], "edicion"]).poblacion.sum().unstack()
    H11, H21 = censo2011(), censo2021()
    ecp = ecp_hogares()
    provs = sorted(set(H11.index) & set(H21.index) & set(ptot.index))
    a = descomponer(H11[provs], H21[provs], ptot.loc[provs, 2012], ptot.loc[provs, 2022]).assign(periodo="2011-2021 (censos)")
    provs2 = sorted(set(ecp.index) & set(cap.index))
    b = descomponer(ecp.loc[provs2, "2022T1"], ecp.loc[provs2, "2026T1"], cap.loc[provs2, "2022"], cap.loc[provs2, "2025"]).assign(
        periodo="2022-2025 (ECP; población del censo anual 2022 y 2025, desfase de un año marcado)")
    D = pd.concat([a, b]).rename_axis("cod_provincia").reset_index()
    D["capa"] = "C4"
    tot = D.groupby("periodo")[["dH", "comp_poblacion", "comp_jefatura", "H0", "H1", "P0", "P1"]].sum().assign(cod_provincia="ES")
    cv = D[D.cod_provincia.isin(CV)].groupby("periodo")[["dH", "comp_poblacion", "comp_jefatura", "H0", "H1", "P0", "P1"]].sum().assign(cod_provincia="CV")
    agg = pd.concat([tot, cv]).reset_index()
    agg["residuo_interaccion"] = agg.dH - agg.comp_poblacion - agg.comp_jefatura
    agg["cuota_poblacion"] = agg.comp_poblacion / agg.dH
    D = pd.concat([D, agg.assign(capa="C4")], ignore_index=True)
    D.to_csv(OUT / "descomposicion_provincia.csv", index=False, float_format="%.4f")

    # componentes de ΔP (españoles y extranjeros por separado donde existe)
    filas = []
    em_in = pd.read_csv(P.RAW9 / "ine_migraciones/ine_em_24323.csv.gz", dtype=str)
    em_out = pd.read_csv(P.RAW9 / "ine_migraciones/ine_em_24326.csv.gz", dtype=str)
    em_ip = pd.read_csv(P.RAW9 / "ine_migraciones/ine_em_24385.csv.gz", dtype=str)
    for df, nombre in ((em_in, "inmigración exterior"), (em_out, "emigración exterior"), (em_ip, "saldo interprovincial")):
        df = df[df.Provincias.str.match(r"^\d{2} ") & df.Nacionalidad.isin(["Total", "Española", "Extranjera"])
                & df.Periodo.astype(int).between(2012, 2020)]
        g = df.assign(v=num(df.Total)).groupby([df.Provincias.str[:2], "Nacionalidad"]).v.sum()
        for (p, nac), v in g.items():
            filas.append({"cod_provincia": p, "periodo": "2012-2020 (EM)", "componente": nombre, "nacionalidad": nac, "personas": v})
    em = pd.read_csv(P.RAW9 / "ine_migraciones/ine_emcr_69764.csv.gz", dtype=str)
    em = em[em.Provincias.fillna("").str.match(r"^\d{2} ") & em.Periodo.astype(int).between(2022, 2024)]
    g = em.assign(v=num(em.Total)).groupby([em.Provincias.str[:2], "Tipo de saldo", "Nacionalidad"]).v.sum()
    for (p, tipo, nac), v in g.items():
        filas.append({"cod_provincia": p, "periodo": "2022-2024 (EMCR)", "componente": tipo, "nacionalidad": nac, "personas": v})
    C = pd.DataFrame(filas)
    for per, (y0, y1) in (("2012-2020 (EM)", (2012, 2021)),):
        dp = (ptot[y1] - ptot[y0]).rename("personas")
        dpe = (pext[y1] - pext[y0]).rename("personas")
        C = pd.concat([C, dp.rename_axis("cod_provincia").reset_index().assign(periodo=per, componente="Δ población (padrón 1-1-2012 → 1-1-2021)", nacionalidad="Total"),
                       dpe.rename_axis("cod_provincia").reset_index().assign(periodo=per, componente="Δ población (padrón 1-1-2012 → 1-1-2021)", nacionalidad="Extranjera")])
    for zona, cods in (("ES", None), ("CV", CV)):
        sub = C if cods is None else C[C.cod_provincia.isin(cods)]
        s = sub.groupby(["periodo", "componente", "nacionalidad"]).personas.sum().reset_index().assign(cod_provincia=zona)
        C = pd.concat([C, s])
    C["capa"] = "C4"
    C.to_csv(OUT / "componentes_poblacion.csv", index=False, float_format="%.0f")

    # contraste C1: hogares censo 2021 frente a ECP (2022T1, la más próxima) por provincia
    c1 = pd.DataFrame({"censo2021_principales": H21, "ecp_2022T1": ecp["2022T1"]}).dropna()
    c1["dif_pct"] = 100 * (c1.ecp_2022T1 / c1.censo2021_principales - 1)
    c1.loc["ES"] = [c1.censo2021_principales.sum(), c1.ecp_2022T1.sum(), 100 * (c1.ecp_2022T1.sum() / c1.censo2021_principales.sum() - 1)]
    c1["capa"] = np.where(c1.dif_pct.abs() <= 2.0, "C1 (dos fuentes coinciden ±2 %)", "C4 (discrepan > 2 %)")
    c1.rename_axis("cod_provincia").reset_index().to_csv(OUT / "contraste_c1.csv", index=False, float_format="%.2f")

    # reconciliación del déficit
    ck = pd.read_csv(P.RAIZ / "output/v5/cifras_clave.csv", dtype=str).set_index("id")
    rec = [
        {"fuente": "Proyecto (V5/V6.2): déficit 2021-2025 sin bajas", "id": "L3-DEF-2125", "valor": float(ck.loc["L3-DEF-2125", "valor"]),
         "rango": f"{ck.loc['L3-DEF-2125', 'min']}-{ck.loc['L3-DEF-2125', 'max']}", "periodo": "2021-2025", "hogares": "EPA y ECP",
         "bajas": "no", "capa": ck.loc["L3-DEF-2125", "capa"], "estado_referencia": "cifra publicada del proyecto"},
        {"fuente": "Proyecto (V5.1): déficit contable con bajas estimadas", "id": "T1-H10", "valor": float(ck.loc["T1-H10", "valor"]),
         "rango": f"{ck.loc['T1-H10', 'min']}-{ck.loc['T1-H10', 'max']}", "periodo": "2021-2025", "hogares": "ECP", "bajas": "sí (estimadas)",
         "capa": ck.loc["T1-H10", "capa"], "estado_referencia": "cifra publicada del proyecto"},
        {"fuente": "Banco de España, Informe Anual 2025 (LA18)", "id": "LA18", "valor": 750000.0, "rango": "≈", "periodo": "2021-2025",
         "hogares": "no detallado", "bajas": "no detallado", "capa": "C4", "estado_referencia": "VERIFICADA (informe institucional; cuartil no aplica)"},
        {"fuente": "OCDE, Economic Survey of Spain 2025 (LA21)", "id": "LA21", "valor": 600000.0, "rango": "≈", "periodo": "2022-2025",
         "hogares": "no detallado", "bajas": "no detallado", "capa": "C4", "estado_referencia": "NO VERIFICADA (capítulo no leído en el original)"},
        {"fuente": "V9 D7: ΔH ECP 2022T1→2026T1 (contexto; no es déficit)", "id": "V9-D7-dH", "valor": float(tot.loc[tot.index.str.startswith("2022"), "dH"].iloc[0]),
         "rango": "—", "periodo": "1-1-2022 a 1-1-2026", "hogares": "ECP", "bajas": "—", "capa": "C4", "estado_referencia": "cálculo propio"},
    ]
    R = pd.DataFrame(rec)
    R.to_csv(OUT / "reconciliacion_deficit.csv", index=False, float_format="%.0f")

    fig, ax = plt.subplots(figsize=(8, 3.8))
    sel = agg.set_index(["cod_provincia", "periodo"])[["comp_poblacion", "comp_jefatura"]] / 1000
    sel.plot.barh(stacked=True, ax=ax)
    ax.set_xlabel("miles de hogares")
    ax.set_title("D7 (contable, C4): componentes del aumento de hogares, España (ES) y Comunitat Valenciana (CV).\n"
                 "Fuente: INE (censos 2011 y 2021, ECP, padrón, censo anual); elaboración propia", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig_d7.png", dpi=130)
    plt.close(fig)
    res = {"rama": "v9/d7", "pregunta": "¿Qué parte del aumento de hogares corresponde a más población y qué parte a más hogares por persona?",
           "capa": "C4 (contable); C1 solo en el contraste censo-ECP donde coinciden", "datos": "Censos 2011 y 2021, ECP, padrón, censo anual, EM, EMCR",
           "N": len(provs), "metodo": "descomposición de cambio (medias del periodo) e identidad de componentes de población",
           "estimacion": agg[["cod_provincia", "periodo", "dH", "comp_poblacion", "comp_jefatura"]].to_dict("records"),
           "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
           "diagnosticos": {"contraste_c1_ES_dif_pct": float(c1.loc["ES", "dif_pct"])},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Regla v5.1: las viviendas liberadas por envejecimiento no se restan de la necesidad."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    print(agg.to_string())
    print(c1.loc[["ES"] + CV].to_string())
    print(R[["fuente", "valor", "periodo"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
