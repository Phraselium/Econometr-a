"""V16-F2.1 · Hecho 2: alquiler, contratos nuevos frente a vigentes.

Stock (vigentes): INE IPC alquiler (encuesta), INE IPVA y SERPAVI (ambos de datos tributarios AEAT-IRPF: un solo grupo).
Nuevos: IPVA «nuevo contrato» (AEAT), fianzas Incasòl (Cataluña) y fianzas GVA (C. Valenciana). Inside Airbnb NO entra (turístico).
Brecha = cambio acumulado de los contratos nuevos menos el de los vigentes, 2021-2024 (periodo común con IPVA provincial).
Dos estimaciones de la brecha en el mismo territorio y periodo: A = IPVA nuevo - IPVA existente (grupo aeat_irpf);
B = fianzas (Incasòl o GVA) - IPC alquiler de la CCAA (grupos fianzas y encuesta_ine). C1 si coinciden dentro de ±3 p.p.
Control: el IPVA nuevo y las fianzas 2021-2024 reproducen el rango publicado A23-A9 y A23-A10; si no, discrepancias.
Cataluña y C. Valenciana no están en la muestra sellada v6 (K8). Las fianzas se leen como agregado propio (terceros_1_0: agregados).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from f2_hechos_base import FECHA, RAIZ, TOL_PP, anotar, capa_por_vara, pct
from f2_hechos_precios import cambio, media_anual, real

RAW = RAIZ / "data" / "raw"
PROV = {"Cataluña": ["Barcelona", "Girona", "Lleida", "Tarragona"],
        "Comunitat Valenciana": ["Alicante/Alacant", "Castellón/Castelló", "Valencia/València"]}
SERP2IPVA = {"Alicante": "Alicante/Alacant", "Castellón": "Castellón/Castelló", "Valencia": "Valencia/València",
             "Valencia/Valéncia": "Valencia/València", "A Coruña": "Coruña, A"}


def incasol_renta() -> pd.Series:
    inc = pd.read_csv(RAW / "v3/incasol_fianzas_municipio_v3.csv.gz")
    inc = inc[inc.periodo.str.contains("gener-desembre")].copy()
    inc["y"] = inc.periodo.str[:4].astype(int)
    inc["tipo"] = np.where(inc.unidad == "EUR/mes", "renta", "n")
    inc["banda_k"] = inc.serie.str.replace(r"_(renta_media|n_contratos)_", "|", regex=True).str.split("|").str[1]
    inc = inc[inc.banda_k != "TOTAL_bandas"]
    w = inc[inc.tipo == "n"].pivot_table(index=["codigo", "y", "banda_k"], values="valor", aggfunc="sum")
    r = inc[inc.tipo == "renta"].pivot_table(index=["codigo", "y", "banda_k"], values="valor", aggfunc="mean")
    j = w.join(r, lsuffix="_n", rsuffix="_r", how="inner").dropna()
    j["nr"] = j.valor_n * j.valor_r
    gy = j.groupby("y")[["valor_n", "nr"]].sum()
    return gy.nr / gy.valor_n


def gva_mediana() -> pd.Series:
    g = pd.concat([pd.read_csv(RAW / f"v5/gva_fianzas_{y}.csv", sep=";") for y in range(2020, 2027)])
    g["importe"] = pd.to_numeric(g.importe_fianza, errors="coerce")
    g = g[(g.importe >= 100) & (g.importe <= 5000)]
    return g.groupby(g.anyo_datos.astype(int)).importe.median()


def ipva_prov() -> pd.DataFrame:
    ip = pd.read_csv(RAW / "ine_v2_ipva.csv")
    pv = ip[(ip.nivel == "provincia") & (ip.tabla == 59005) & (ip.medida == "IPVA_indice")]
    return pv.pivot_table(index=["territorio", "periodo"], columns="desglose", values="valor")


def pesos_serpavi() -> pd.Series:
    sp = pd.read_csv(RAW / "pdf/serpavi_provincias.csv")
    s = sp[(sp.variable == "n_contratos") & (sp.tipologia == "VC") & (sp.periodo == 2024)].copy()
    s["terr"] = s.nombre.replace(SERP2IPVA)
    return s.set_index("terr").valor


def ipva_ccaa(cc: str, pv: pd.DataFrame, w: pd.Series) -> dict:
    ps = PROV[cc]
    v = {"nuevo": [], "existente": [], "brecha24": [], "peso": []}
    for p in ps:
        e21, n21 = pv.loc[(p, 2021), ["Contrato existente", "Nuevo contrato"]]
        e24, n24 = pv.loc[(p, 2024), ["Contrato existente", "Nuevo contrato"]]
        v["nuevo"].append(n24 / n21 - 1)
        v["existente"].append(e24 / e21 - 1)
        v["brecha24"].append(n24 / e24 - 1)
        v["peso"].append(float(w.get(p, np.nan)))
    pe = np.array(v["peso"])
    pe = np.where(np.isnan(pe), np.nanmean(pe), pe)
    return {k: float(np.average(v[k], weights=pe)) for k in ("nuevo", "existente", "brecha24")}


def stock_nacional() -> list[str]:
    avisos = []
    n = pd.read_csv(RAIZ / "data/processed/v8/nacional_q_v8.csv")
    ipc = media_anual(n, "ipc_general")
    alq = media_anual(n, "ipc_alquiler")
    ip = pd.read_csv(RAW / "ine_v2_ipva.csv")
    ipn = ip[(ip.nivel == "nacional") & (ip.medida == "IPVA_indice") & (ip.desglose == "Total")].pivot_table(index="periodo", values="valor")["valor"]
    srp = pd.read_csv(RAW / "pdf/serpavi_esp_agregado.csv")
    srp = srp[srp.serie.str.endswith("pond_composicion_constante")].set_index("periodo").valor
    # control 1.0: stock 2015-2024, A23-A2 (10,9 a 22,9) y SERPAVI A23-A2b (43,0)
    c15 = {"INE IPC alquiler": cambio(alq, 2015, 2024), "INE IPVA": cambio(ipn, 2015, 2024), "SERPAVI": cambio(srp, 2015, 2024)}
    if abs(100 * c15["SERPAVI"] - 43.0) > 0.1:
        avisos.append(f"Control SERPAVI 2015-2024: V16 {100 * c15['SERPAVI']:.1f} frente a 1.0 43,0 (A23-A2b)")
    for b in (2013, 2019):
        nom = {"INE IPC alquiler": cambio(alq, b, 2024), "INE IPVA": cambio(ipn, b, 2024), "SERPAVI": cambio(srp, b, 2024)}
        for tipo in ("nominal", "real"):
            vals = {k: 100 * (real(v, cambio(ipc, b, 2024)) if tipo == "real" else v) for k, v in nom.items()}
            capa, nuc = capa_por_vara(vals)
            cual = {k: round(v, 1) for k, v in vals.items()}
            if capa == "C1":
                v, lo, hi = float(np.mean([vals[k] for k in nuc])), min(vals[k] for k in nuc), max(vals[k] for k in nuc)
                mot = f"Coinciden {', '.join(nuc)} (grupos distintos) dentro de ±{TOL_PP} p.p. Todas: {cual}."
            else:
                v, lo, hi = None, min(vals.values()), max(vals.values())
                mot = (f"Sin dos grupos distintos dentro de ±{TOL_PP} p.p.: {cual}. INE IPVA y SERPAVI comparten fuente primaria (AEAT-IRPF): "
                       "un solo grupo. Se publican todas.")
            anotar(f"V16-HEC-ALQ-STOCK-{tipo.upper()}-{b}-2024", f"Alquiler de contratos vigentes, cambio acumulado {tipo} {b}-2024, España",
                   v, lo, hi, "%", f"{b}-2024 (media anual)", "España", list(vals), capa, "2024 (anual)",
                   "f2_hechos_alquiler.py:stock_nacional; media anual; IPVA total (59005), SERPAVI composición constante, IPC alquiler; "
                   "real con IPC general.", tolerancia=f"±{TOL_PP} p.p.", motivo_capa=mot)
    for b in (2007, 2013, 2019):
        nom = cambio(alq, b, 2025)
        for tipo, val in (("nominal", nom), ("real", real(nom, cambio(ipc, b, 2025)))):
            anotar(f"V16-HEC-ALQ-IPC-{tipo.upper()}-{b}-2025", f"IPC de alquiler (stock), cambio acumulado {tipo} {b}-2025, España",
                   pct(val), None, None, "%", f"{b}-2025 (media anual)", "España", ["INE IPC alquiler"], "C4", "2025 (anual)",
                   "f2_hechos_alquiler.py:stock_nacional; media anual de 4 trimestres del IPC alquiler; IPVA y SERPAVI acaban en 2024, "
                   "así que 2025 no tiene segunda fuente.", motivo_capa="Estadística oficial de fuente única en 2025 (IPVA y SERPAVI acaban en 2024).")
    return avisos


def brechas() -> list[str]:
    avisos = []
    pan = pd.read_csv(RAIZ / "data/processed/v8/panel_ccaa_q_v8.csv")
    pan["y"] = pan.trimestre.str[:4].astype(int)
    pv, w = ipva_prov(), pesos_serpavi()
    inc, gva = incasol_renta(), gva_mediana()
    nuevos = {"Cataluña": ("Incasòl fianzas", inc, "A23-A9", (16.6, 17.2)), "Comunitat Valenciana": ("GVA fianzas", gva, "A23-A10", (26.1, 30.8))}
    for cc, (fuente, serie, idpub, rango) in nuevos.items():
        i = ipva_ccaa(cc, pv, w)
        d = pan[pan.ccaa == cc]
        stock = media_anual(d, "ipc_alquiler")
        c_ipc = cambio(stock, 2021, 2024)
        c_f = cambio(serie, 2021, 2024)
        # control frente a la 1.0: IPVA nuevo y fianzas dentro del rango publicado (±0,3 p.p. de margen de redondeo)
        for nom_c, v in (("IPVA nuevo", 100 * i["nuevo"]), (fuente, 100 * c_f)):
            if not (rango[0] - 0.3 <= v <= rango[1] + 0.3):
                avisos.append(f"Control {idpub} {cc}: {nom_c} 2021-2024 = {v:.1f} fuera de {rango} publicado")
        gA = 100 * (i["nuevo"] - i["existente"])
        gB = 100 * (c_f - c_ipc)
        capa, _ = capa_por_vara({"INE IPVA": gA, fuente: gB}) if abs(gA - gB) <= TOL_PP else ("C4", [])
        mot = (f"Brecha A (IPVA nuevo - IPVA existente) = {gA:.1f} p.p. y brecha B ({fuente} - IPC alquiler {cc}) = {gB:.1f} p.p." +
               (f" Coinciden dentro de ±{TOL_PP} p.p. con fuentes de tres grupos (aeat_irpf, fianzas, encuesta_ine); valor = punto medio." if capa == "C1"
                else f" No coinciden dentro de ±{TOL_PP} p.p.: se publican ambas (rango), capa C4."))
        fu = ["INE IPVA", fuente, "INE IPC alquiler"]
        anotar(f"V16-HEC-ALQ-BRECHA-2124-{'CAT' if cc == 'Cataluña' else 'CV'}",
               f"Brecha de crecimiento contratos nuevos menos vigentes 2021-2024, {cc}",
               (gA + gB) / 2 if capa == "C1" else None, min(gA, gB), max(gA, gB), "p.p.", "2021-2024", cc, fu, capa, "2024",
               f"f2_hechos_alquiler.py:brechas; IPVA provincial (59005) ponderado por contratos SERPAVI 2024; cambio acumulado de los "
               f"contratos nuevos - vigentes. Controles con {idpub}: IPVA nuevo {100 * i['nuevo']:.1f} %, {fuente} {100 * c_f:.1f} %, "
               f"IPC alquiler {100 * c_ipc:.1f} %, IPVA existente {100 * i['existente']:.1f} %.",
               tolerancia=f"±{TOL_PP} p.p. entre las dos estimaciones de la brecha", motivo_capa=mot)
        anotar(f"V16-HEC-ALQ-NIVEL-2024-{'CAT' if cc == 'Cataluña' else 'CV'}",
               f"Brecha de nivel contrato nuevo frente a existente en 2024 (IPVA), {cc}", pct(i["brecha24"]), None, None, "%", "2024", cc,
               ["INE IPVA"], "C4", "2024", "f2_hechos_alquiler.py:brechas; cociente IPVA nuevo/existente 2024 por provincia, ponderado.",
               motivo_capa="Una sola fuente (IPVA, AEAT-IRPF): el nivel relativo no tiene segunda fuente independiente comparable en la misma unidad.")
        c25 = cambio(stock, 2021, 2025)
        f25 = cambio(serie, 2021, 2025)
        anotar(f"V16-HEC-ALQ-BRECHA-2125-{'CAT' if cc == 'Cataluña' else 'CV'}",
               f"Brecha de crecimiento fianzas nuevas menos IPC alquiler 2021-2025, {cc}", pct(f25 - c25), None, None, "p.p.", "2021-2025", cc,
               [fuente, "INE IPC alquiler"], "C4", "2025 (anual)",
               f"f2_hechos_alquiler.py:brechas; {fuente} {100 * f25:.1f} % menos IPC alquiler {100 * c25:.1f} %. IPVA acaba en 2024.",
               motivo_capa="Una sola medida de contratos nuevos en 2025 (IPVA acaba en 2024): C4.")
    return avisos
