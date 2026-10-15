"""V9 F5 · hechos.json de V9 (ids «V9-…») para output/v5/cifras_clave.csv (src/v5/cifras_clave.py los incorpora desde
output/v9/*/hechos.json). Toda cifra difundible de V9 (web, verificador, textos, Excel) sale de aquí vía cifras_clave.
Los coeficientes en log se expresan ×100 (≈ %). Sin redondeo aquí: el formato lo aplica el renderizador.
Salida: output/v9/F5/hechos.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paneles as P  # noqa: E402

V9 = P.RAIZ / "output" / "v9"
OUT = V9 / "F5"


def h(i, ind, val, mn, mx, uni, per, cob, fue, capa, fecha, origen):
    return {"id": i, "indicador": ind, "valor": None if pd.isna(val) else float(val),
            "min": None if mn is None or pd.isna(mn) else float(mn), "max": None if mx is None or pd.isna(mx) else float(mx),
            "unidad": uni, "periodo": per, "cobertura": cob, "fuentes": fue, "capa": capa, "fecha_dato": fecha, "ficha": "—",
            "origen": origen}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    T = pd.read_csv(V9 / "f3/tabla_capas.csv")
    pr1 = pd.read_csv(V9 / "d1/pruebas.csv").set_index("prueba_diseno")
    pr2 = pd.read_csv(V9 / "d2/pruebas.csv").set_index("prueba_diseno")
    d4 = pd.read_csv(V9 / "d4/tabla_d4.csv")
    d7 = pd.read_csv(V9 / "d7/descomposicion_provincia.csv", dtype={"cod_provincia": str})
    c1 = pd.read_csv(V9 / "d7/contraste_c1.csv", dtype={"cod_provincia": str}).set_index("cod_provincia")
    out = []
    PP = "%"   # puntos logarítmicos ×100 (≈ %); se explica en los textos
    INC = "Incasòl (fianzas; no redistribuible), BOE; elaboración propia"

    def fila(dis, txt):
        s = T[(T.diseno == dis) & T.resultado.str.contains(txt, regex=False)]
        return s.iloc[0]

    for dis, per, cob in (("D1a", "2022T2-2026T1", "Cataluña, municipios"), ("D1b", "2019T1-2022T1", "Cataluña, municipios")):
        for res, clave in (("log renta media", "renta"), ("log contratos", "contratos")):
            r = fila(dis, res)
            nom = "zonas tensionadas (Ley 12/2023)" if dis == "D1a" else "Ley catalana 11/2020"
            out.append(h(f"V9-{dis}-{clave}-att", f"{nom}: ATT sobre {res.replace('log ', '')} de contratos nuevos (CS)", 100 * r.beta,
                         100 * r.ic95_lo, 100 * r.ic95_hi, PP, per, cob, INC, r.capa, per[-6:], f"output/v9/f3/tabla_capas.csv:{dis}"))
            pr = pr1.loc[f"{dis} {r.resultado}"]
            out.append(h(f"V9-{dis}-{clave}-pretend-p", f"{nom}, {res}: p del contraste conjunto de pretendencias", pr.pretend_p, None, None,
                         "p-valor", per, cob, INC, r.capa, per[-6:], f"output/v9/d1/pruebas.csv:{dis}"))
            out.append(h(f"V9-{dis}-{clave}-placebo-p", f"{nom}, {res}: p del placebo de fecha (4 trimestres antes)", pr.placebo_fecha_p,
                         None, None, "p-valor", per, cob, INC, r.capa, per[-6:], f"output/v9/d1/pruebas.csv:{dis}"))
            out.append(h(f"V9-{dis}-{clave}-ruptura", f"{nom}, {res}: M̄ de ruptura de Honest DiD (magnitudes relativas, simplificado)",
                         pr.honest_Mbar_ruptura, None, None, "M̄", per, cob, INC, r.capa, per[-6:], f"output/v9/d1/pruebas.csv:{dis}"))
            if r.confirmatoria:
                out.append(h(f"V9-{dis}-{clave}-pholm", f"{nom}, {res}: p ajustado por Holm (familia confirmatoria de V9)", r.p_holm, None, None,
                             "p-valor", per, cob, INC, r.capa, per[-6:], "output/v9/f3/tabla_capas.csv"))
    r = fila("D1c", "log renta media")
    out.append(h("V9-D1c-renta-att", "Zonas tensionadas de Euskadi: ATT exploratorio sobre la renta de fianzas nuevas (EMAL)", 100 * r.beta,
                 100 * r.ic95_lo, 100 * r.ic95_hi, PP, "2016T1-2025T4", "Euskadi, municipios > 20.000 hab.", "Gobierno Vasco EMAL; BOE",
                 r.capa, "2025T4", "output/v9/f3/tabla_capas.csv:D1c"))
    for per, clave in (("reapertura", "reap"), ("covid", "covid")):
        r = fila("D2", f"renta media de contratos nuevos ({per}")
        out.append(h(f"V9-D2-renta-{clave}", f"Viviendas de uso turístico en 2019 × {'reapertura 2022-2025' if clave == 'reap' else 'COVID 2020-2021'}: "
                     "variación de la renta de contratos nuevos por 1 DE de dosis", 100 * r.beta, 100 * r.ic95_lo, 100 * r.ic95_hi, PP,
                     "2014-2025", "Cataluña, municipios", "Incasòl; IDESCAT; INE padrón", r.capa, "2025", "output/v9/f3/tabla_capas.csv:D2"))
    out.append(h("V9-D2-renta-pretend-p", "D2, renta: p del contraste conjunto de pretendencias (2014-2018)",
                 pr2.loc["D2 log renta media de contratos nuevos"].pretend_p, None, None, "p-valor", "2014-2018", "Cataluña",
                 "Incasòl; IDESCAT", "C4", "2018", "output/v9/d2/pruebas.csv"))
    for col, clave, txt in (("d_lmedia", "media", "fianza media"), ("d_cuota", "cuota", "cuota provincial de fianzas")):
        r = fila("D3", col)
        out.append(h(f"V9-D3-{clave}", f"Caída del registro VUT (por 1 VUT por 100 viviendas) y variación de la {txt} 2024→2025 por CP (descriptivo)",
                     100 * r.beta if clave == "media" else r.beta, (100 if clave == "media" else 1) * r.ic95_lo,
                     (100 if clave == "media" else 1) * r.ic95_hi, PP if clave == "media" else "puntos de cuota", "2024-2025",
                     "Comunitat Valenciana, códigos postales", "GVA (fianzas, registro VUT); INE; elaboración propia", r.capa, "2025",
                     "output/v9/f3/tabla_capas.csv:D3"))
    for txt, clave in (("IPC de alquiler (principal (réplica", "ipc-replica"), ("valor tasado (principal (réplica", "tasado-replica"),
                       ("valor tasado (ampliación", "tasado-ampliacion"), ("IPC de alquiler (ampliación", "ipc-ampliacion")):
        r = fila("D4", txt)
        out.append(h(f"V9-D4-{clave}", f"Inmigración (2SLS shift-share), {txt.split(' (')[0]}: elasticidad por punto de población extranjera "
                     f"({'2003-2012' if 'réplica' in txt else '2015-2022'})", 100 * r.beta, 100 * r.ic95_lo, 100 * r.ic95_hi,
                     "% por punto de población", "2003-2012" if "réplica" in txt else "2015-2022", "50 provincias",
                     "INE padrón e IPC; MIVAU valor tasado; elaboración propia", r.capa, "2012" if "réplica" in txt else "2022",
                     "output/v9/f3/tabla_capas.csv:D4"))
        out.append(h(f"V9-D4-{clave}-F", f"Inmigración, {txt.split(' (')[0]}: F efectiva del instrumento", r.F_eff, None, None, "estadístico F",
                     "2003-2012" if "réplica" in txt else "2015-2022", "50 provincias", "INE padrón", r.capa, "2012", "output/v9/f3/tabla_capas.csv:D4"))
    for txt, clave in (("alquiler (h = 4)", "alq-h4"), ("precio (h = 4)", "precio-h4"), ("precio (h = 8)", "precio-h8")):
        r = fila("D5", txt)
        out.append(h(f"V9-D5-{clave}", f"Shock monetario del BCE × cuota de hipotecas a tipo variable (1 DE): Δ log {txt}", 100 * r.beta,
                     100 * r.ic95_lo, 100 * r.ic95_hi, "%", "2008T1-2025T3", "18 países de la zona euro",
                     "BIS; Eurostat; BCE (RAI); Jarociński-Karadi (no redistribuible)", r.capa, "2025T3", "output/v9/f3/tabla_capas.csv:D5"))
    for zona, cob in (("ES", "España"), ("CV", "Comunitat Valenciana")):
        for per, clave in (("2011-2021", "1121"), ("2022-2025", "2225")):
            s = d7[(d7.cod_provincia == zona) & d7.periodo.str.startswith(per)].iloc[0]
            out.append(h(f"V9-D7-{zona}-{clave}-dH", f"Aumento de hogares ({per})", s.dH, None, None, "hogares", per, cob,
                         "INE (censos, ECP, padrón, censo anual)", "C4", per[-4:], "output/v9/d7/descomposicion_provincia.csv"))
            for col, nom, uni in (("H0", "Hogares al inicio", "hogares"), ("H1", "Hogares al final", "hogares"),
                                  ("P0", "Población al inicio", "personas"), ("P1", "Población al final", "personas")):
                out.append(h(f"V9-D7-{zona}-{clave}-{col}", f"{nom} ({per}; descomposición D7)", s[col], None, None, uni, per, cob,
                             "INE (censos, ECP, padrón, censo anual)", "C4", per[-4:], "output/v9/d7/descomposicion_provincia.csv"))
            out.append(h(f"V9-D7-{zona}-{clave}-cuota-pob", f"Componente población del aumento de hogares ({per}), % del total",
                         100 * s.comp_poblacion / s.dH, None, None, "%", per, cob, "INE; elaboración propia (descomposición contable)",
                         "C4", per[-4:], "output/v9/d7/descomposicion_provincia.csv"))
    out.append(h("V9-D7-c1-dif", "Hogares 2021: ECP (1-1-2022) frente a censo 2021 (viviendas principales), diferencia", c1.loc["ES", "dif_pct"],
                 None, None, "%", "2021", "España", "INE censo 2021; INE ECP", "C1" if abs(c1.loc["ES", "dif_pct"]) <= 2 else "C4", "2022T1",
                 "output/v9/d7/contraste_c1.csv"))
    out.append(h("V9-NC3", "Resultados de V9 que alcanzan C3 o C3s", int((T.capa.isin(["C3", "C3s"])).sum()), None, None, "efectos",
                 "2026", "D1-D5", "output/v9/f3/tabla_capas.csv", "C4", "2026-10-15", "output/v9/f3/tabla_capas.csv"))
    (OUT / "hechos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(out), "hechos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
