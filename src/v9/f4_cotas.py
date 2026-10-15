"""V9 F4 · cotas de contribución (C2) según el addendum A1.7 al pre-registro.

Solo se acotan efectos C3/C3s que hayan superado todas sus pruebas (cota de Manski: efecto entre 0 y el extremo del IC
95 % del mismo signo, sin desbordamientos, × exposición observada; advertencia única: equilibrio parcial). Si un factor
no tiene ningún resultado C3/C3s, la tabla dice «no identificado» y no da cifra. Los resultados C4 no se convierten en
contribuciones (no se usan las palabras «contribución» ni «atribuible» con ellos).
Contexto de la subida (cifras publicadas de cifras_clave, sin cambios): A23-P2 (precio de compra, núcleo, C1),
A23-A3 (contratos nuevos IPVA, C4), A23-A10 (contratos nuevos Comunitat Valenciana, C1) y A23-A5 (GVA, C4).
Salidas: output/v9/f4/{cotas.csv, cotas.md, resultado.json}.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paneles as P  # noqa: E402

V9 = P.RAIZ / "output" / "v9"
OUT = V9 / "f4"
FACTORES = [  # factor, diseños, filtro de hipótesis en tabla_capas
    ("Zonas tensionadas y topes de renta", ["D1a", "D1b", "D1c"]),
    ("Pisos turísticos", ["D2", "D3"]),
    ("Inmigración", ["D4"]),
    ("Tipos de interés (exposición a tipo variable)", ["D5"]),
    ("Ayudas a jóvenes (Bono Alquiler Joven)", ["D6"]),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    T = pd.read_csv(V9 / "f3/tabla_capas.csv")
    ck = pd.read_csv(P.RAIZ / "output/v5/cifras_clave.csv", dtype=str).set_index("id")
    ctx = {i: f"{ck.loc[i, 'indicador']}: {ck.loc[i, 'valor']} {ck.loc[i, 'unidad']} ({ck.loc[i, 'periodo']}; {ck.loc[i, 'capa']}) [{i}]"
           for i in ("A23-P2", "A23-A3", "A23-A10", "A23-A5")}
    filas = []
    for factor, dis in FACTORES:
        sub = T[T.diseno.isin(dis)]
        c3 = sub[sub.capa.isin(["C3", "C3s"])]
        if len(c3):
            raise SystemExit("hay resultados C3/C3s: implementar la cota de Manski antes de publicar")  # no ocurre en V9
        if "D6" in dis:
            estado = "no estimado (sin edad exacta ni receptores identificados)"
        else:
            capas = ", ".join(sorted(set(sub.capa))) if len(sub) else "—"
            estado = f"no identificado (mejor capa alcanzada: {capas})"
        filas.append({"factor": factor, "disenos": ", ".join(dis), "estado": estado,
                      "cota_nacional_min": None, "cota_nacional_max": None, "cota_cv_min": None, "cota_cv_max": None,
                      "capa_cota": "—", "advertencia": "equilibrio parcial"})
    C = pd.DataFrame(filas)
    C.to_csv(OUT / "cotas.csv", index=False)
    lin = ["# F4 · Cotas de contribución a la subida (C2): resultado de V9", "",
           "Regla (addendum A1.7, aprobado antes de estimar): solo se acotan efectos C3/C3s que superan todas sus pruebas. "
           "Ningún resultado de V9 alcanza C3/C3s (output/v9/f3/tabla_capas.csv), así que **no hay cotas numéricas**: "
           "con la evidencia de V9 no se puede decir cuánto de la subida nacional o de la Comunitat Valenciana corresponde a cada factor.", "",
           "| Factor | Diseños | Estado | Máximo atribuible (España / C. Valenciana) | Mínimo atribuible (España / C. Valenciana) |",
           "|---|---|---|---|---|"]
    for _, r in C.iterrows():
        lin.append(f"| {r.factor} | {r.disenos} | {r.estado} | no acotado | no acotado |")
    lin += ["", "Subida de referencia (cifras publicadas, sin cambios):", ""] + [f"- {v}" for v in ctx.values()]
    lin += ["", "Lo que sí aportan los diseños (C4, sin lenguaje causal) está en output/v9/f3/tabla_revista.md. "
            "D7 (contable) descompone el aumento de hogares en componente población y componente tasa de jefatura "
            "(output/v9/d7); es una identidad contable, no una atribución causal de la subida de precios."]
    (OUT / "cotas.md").write_text("\n".join(lin) + "\n", encoding="utf-8")
    res = {"rama": "v9/f4", "pregunta": "¿Qué parte de la subida nacional y de la Comunitat Valenciana se puede acotar por factor?",
           "capa": "C2 (vacía: ningún C3/C3s)", "datos": "output/v9/f3/tabla_capas.csv; cifras_clave", "N": len(C),
           "metodo": "Manski con supuestos explícitos sobre efectos C3/C3s (addendum A1.7)", "estimacion": None, "ic95": None,
           "p_ajustado": None, "nivel_evidencia": "—", "diagnosticos": C[["factor", "estado"]].to_dict("records"),
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "Equilibrio parcial."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(C.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
