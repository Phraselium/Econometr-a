"""V7.2-4 · Ficha del verificador «¿Hay una burbuja?» con el GSADF nacional (reverificado) y el regional juntos. Capa C4.

Lee output/v7_2/gsadf/reverificacion.csv (nacional, mismo método y semilla que v5), output/v5/R1B/tablas/gsadf_corregido.csv
(34 series de CCAA, panel 2007-2026) y output/v5/E/hechos.json (E-V6-M1B-GSADF-*: 11 CCAA, provincias de entrenamiento, 2015-2024).
Escribe output/v7_2/gsadf/{hechos.json, ficha_burbuja.json, ficha_burbuja.md}. Sin red, determinista.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v7_2" / "gsadf"
FECHA = "2026-10-13"


def h(i, ind, v, uni, per, cob, fue):
    return dict(id=i, indicador=ind, valor=v, min=None, max=None, unidad=uni, periodo=per, cobertura=cob, fuentes=fue, capa="C4",
                fecha_dato=FECHA, sentido_min_max="sin min/max")


def main():
    n = pd.read_csv(OUT / "reverificacion.csv")
    r = pd.read_csv(RAIZ / "output/v5/R1B/tablas/gsadf_corregido.csv")
    cc = r[r.familia == "ccaa"]
    v6 = {x["id"]: x for x in json.loads((RAIZ / "output/v5/E/hechos.json").read_text())}   # hechos de v6 M1B recogidos en E
    fu = n[n.familia == "fundamentales"]
    ratios = fu[fu.medida.str.startswith(("precio/renta", "precio/alquiler"))]
    tipos = fu[~fu.index.isin(ratios.index)]
    niv = n[n.familia == "referencia"]
    k = dict(rat_p=int((ratios.p < .05).sum()), rat_n=len(ratios), rat_bh=int(ratios.exuberancia_bh05.sum()),
             tip_p=int((tipos.p < .05).sum()), tip_n=len(tipos), niv_bh=int(niv.exuberancia_bh05.sum()), niv_n=len(niv),
             cc_bh=int(cc.exuberancia_bh05.sum()), cc_n=len(cc), cc_p=int((cc.p_corr < .05).sum()),
             v6_sig=int(v6["E-V6-M1B-GSADF-SIG"]["valor"]), v6_n=int(v6["E-V6-M1B-GSADF-TOT"]["valor"]),
             coinciden=int(n.coincide.sum()), total=len(n))
    fn = "GSADF con valores críticos por bootstrap AR(p) estimado, 499 réplicas, BH por familia (v5 R1B, reverificado en v7.2)"
    H = [h("V72-GSADF-rev", "Series nacionales del GSADF de v5 que se reproducen exactamente con el mismo método y la misma semilla", k["coinciden"], "series", "2007T1-2026T2", "Nacional", fn),
         h("V72-GSADF-ratios-p05", "Cocientes precio/renta y precio/alquiler nacionales con exuberancia sin ajuste múltiple (p<0,05)", k["rat_p"], "series", "2007T1-2026T2", "Nacional", fn),
         h("V72-GSADF-ratios-bh", "Cocientes precio/renta y precio/alquiler nacionales con exuberancia tras BH", k["rat_bh"], "series", "2007T1-2026T2", "Nacional", fn),
         h("V72-GSADF-tipos-p05", "Precio frente a valores de referencia con tipos de interés (descuento del alquiler y cuota sobre renta) con exuberancia sin ajuste", k["tip_p"], "series", "2007T1-2026T2", "Nacional", fn),
         h("V72-GSADF-niveles-bh", "Niveles de precio nacionales (IPV y valor tasado, sin fundamentales) con exuberancia tras BH", k["niv_bh"], "series", "2007T1-2026T2", "Nacional", fn),
         h("V72-GSADF-ccaa-bh", "Series de CCAA (precio/alquiler, IPV y valor tasado; 17 CCAA) con exuberancia tras BH", k["cc_bh"], "series", "2007T1-2026T2", "17 CCAA", fn),
         h("V72-GSADF-ccaa-v6", "CCAA con exuberancia (p<0,05) en el ratio precio/alquiler, provincias de entrenamiento v6", k["v6_sig"], "CCAA", "2015T1-2024T4", "11 CCAA", "v6 M1B, mismo método, T=40")]
    for x in H:
        x["valor"] = float(x["valor"])
    (OUT / "hechos.json").write_text(json.dumps(H, ensure_ascii=False, indent=1), encoding="utf-8")
    mag = (f"NACIONAL (2007T1-2026T2; reverificado: {k['coinciden']} de {k['total']} series idénticas a v5). "
           f"Los cocientes precio/renta y precio/alquiler muestran exuberancia sin ajuste en {k['rat_p']} de {k['rat_n']}, pero en {k['rat_bh']} tras BH. "
           f"Frente a valores de referencia con tipos de interés (descuento del alquiler, cuota sobre renta): {k['tip_p']} de {k['tip_n']}. "
           f"Los niveles de precio, sin fundamentales, sí son explosivos tras BH ({k['niv_bh']} de {k['niv_n']}). "
           f"REGIONAL: {k['cc_bh']} de {k['cc_n']} series de CCAA con exuberancia tras BH ({k['cc_p']} sin ajuste; panel 2007-2026); "
           f"en v6, con otra muestra (provincias de entrenamiento, 2015-2024, T=40), {k['v6_sig']} de {k['v6_n']} CCAA.")
    ficha = dict(id="V72-BURBUJA", tema="Burbuja de precios: nacional y regional juntos",
                 enunciado="Hay una burbuja en el precio de la vivienda en España.", capa="C4", magnitud=mag, intervalo="—", cota="—",
                 literatura="Phillips, Shi y Yu (2015), GSADF: NO VERIFICADA.",
                 veredicto="ANALIZADA, NO CONCLUYENTE",
                 regla=("No se puede afirmar que haya una burbuja: la exuberancia de los cocientes nacionales no sobrevive al ajuste múltiple, "
                        "frente a los valores con tipos no la hay, y un test de exuberancia no identifica sobrevaloración ni su causa. "
                        "Tampoco se puede afirmar que NO la haya: los niveles nacionales y algunas series regionales son explosivos tras BH, "
                        "el valor fundamental usado es una referencia simple con supuestos propios y la muestra es corta para el ciclo."),
                 limites="T=78 (T=40 en v6); ADF con un rezago; sin renta por CCAA; los resultados regionales de v5 y v6 usan muestras distintas y no son comparables entre sí.",
                 evidencia=["output/v7_2/gsadf/reverificacion.csv", "output/v5/R1B/tablas/gsadf_corregido.csv", "output/v5/E/hechos.json (E-V6-M1B-GSADF-*)"],
                 version="v7.2")
    (OUT / "ficha_burbuja.json").write_text(json.dumps([ficha], ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"## {ficha['id']} · {ficha['tema']}", "", f"**Afirmación evaluada:** {ficha['enunciado']}", "",
          f"**Veredicto:** {ficha['veredicto']} ({ficha['capa']})", "", f"**Magnitud:** {mag}", "",
          f"**No se puede afirmar, en ningún sentido:** {ficha['regla']}", "", f"**Límites:** {ficha['limites']}", "",
          "**Evidencia:** " + "; ".join(ficha["evidencia"]), ""]
    (OUT / "ficha_burbuja.md").write_text("\n".join(md), encoding="utf-8")
    print("ficha_burbuja:", k)


if __name__ == "__main__":
    main()
