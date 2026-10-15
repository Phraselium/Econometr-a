"""V9 F5 · adenda V9 de docs/v6_1/historial_conclusiones.md: qué confirma, matiza o contradice V9 respecto a v8.1.
Reescribe solo el bloque entre <!-- V9:inicio --> y <!-- V9:fin --> (lo crea al final si no existe). Cifras de
output/v5/cifras_clave.csv (ids «V9-» y «V8-»). Determinista.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DOC = RAIZ / "docs" / "v6_1" / "historial_conclusiones.md"


def main() -> int:
    ck = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv", dtype=str).set_index("id")

    def v(i, d=1):
        return f"{float(ck.loc[i, 'valor']):.{d}f}".replace(".", ",").replace("-", "−")

    def ic(i, d=1):
        return f"({float(ck.loc[i, 'min']):.{d}f} a {float(ck.loc[i, 'max']):.{d}f})".replace(".", ",").replace("-", "−")

    def p(i):
        x = float(ck.loc[i, "valor"])
        return "< 0,001" if x < 0.001 else f"{x:.3f}".replace(".", ",")

    filas = [
        ("Topes de renta (Ley catalana 11/2020)", "Renta de contratos nuevos (Incasòl)", f"{v('V9-D1b-renta-att')} % {ic('V9-D1b-renta-att')} [V9-D1b-renta-att]",
         "DiD (Callaway-Sant'Anna), confirmatoria", "−", "C4",
         f"**Matiza** (v5-v8: «topes, signo no estable», C4): la diferencia es negativa, de magnitud igual a la literatura (LB01), y supera pretendencias "
         f"(p {p('V9-D1b-renta-pretend-p')}) y placebos, pero no la robustez a desviaciones de tendencia pre-registrada (M̄ de ruptura {v('V9-D1b-renta-ruptura')}); no pasa a C3"),
        ("Zonas tensionadas (Ley 12/2023, Cataluña)", "Renta de contratos nuevos", f"{v('V9-D1a-renta-att')} % {ic('V9-D1a-renta-att')} [V9-D1a-renta-att]",
         "DiD escalonado, confirmatoria", "−", "C4",
         f"**Nuevo**: sin lectura causal; pretendencias (p {p('V9-D1a-renta-pretend-p')}) y placebo de fecha (p {p('V9-D1a-renta-placebo-p')}) rechazados"),
        ("Regulación y número de contratos", "Contratos nuevos (fianzas)", f"Ley 11/2020 {v('V9-D1b-contratos-att')} %; zonas tensionadas {v('V9-D1a-contratos-att')} %",
         "DiD, exploratoria", "0", "C4", "**Nuevo**: no se detecta caída (BH ≥ 0,10); coincide con LB01"),
        ("Turismo y viviendas turísticas", "Renta de contratos nuevos (Cataluña); fianzas por CP (C. Valenciana)",
         f"reapertura {v('V9-D2-renta-reap', 2)} % por DE de dosis; D3 {v('V9-D3-media', 2)} % por VUT/100 viv.", "Dosis-respuesta; diferencias largas",
         "+ / 0", "C4", f"**Se mantiene** (V8: no concluyente): asociación con pretendencias rechazadas (p {p('V9-D2-renta-pretend-p')}) y D3 descriptivo con placebo del mismo signo"),
        ("Demografía e inmigración", "IPC de alquiler; valor tasado (provincias)", f"{v('V9-D4-ipc-replica', 2)} % por punto (réplica 2003-2012); F efectiva {v('V9-D4-ipc-replica-F')}",
         "2SLS shift-share (Card), AKM, AR", "no concluyente", "C4",
         "**Se mantiene** (V8: instrumento migratorio sin primera etapa): el instrumento sigue siendo débil a escala provincial"),
        ("Tipos de interés", "Precio (BIS) y alquiler (IPCA), zona euro", f"precio h=4 {v('V9-D5-precio-h4')} %; alquiler h=4 {v('V9-D5-alq-h4')} % por shock y DE de exposición",
         "Proyecciones locales, Driscoll-Kraay", "0 (precio); − (alquiler)", "C4",
         "**Se mantiene** en el precio (V8: no distinguible de 0); **nuevo** en el alquiler: asociación negativa a 4 trimestres, exploratoria y sin potencia"),
        ("Hogares (contable)", "Aumento de hogares 2022-2025", f"componente población {v('V9-D7-ES-2225-cuota-pob', 0)} % (España), {v('V9-D7-CV-2225-cuota-pob', 0)} % (C. Valenciana)",
         "Descomposición contable", "+", "C4", "**Confirma** el orden de magnitud de V4/M2 (peso de la población extranjera en ΔH) con otra medida; identidad, no atribución"),
        ("Un factor con efecto identificado", "—", "0 resultados en C3/C3s [V9-NC3]", "Pre-registro V9 + addendum A1", "—", "—",
         "**Confirma** V8 (ningún factor designado): con diseños locales tampoco se identifica ningún efecto con las reglas fijadas antes de estimar"),
    ]
    L = ["<!-- V9:inicio -->", "", "## Adenda V9 (qué causa qué, 2026-10-15)", "",
         "Una fila por factor. Las cifras salen de `output/v5/cifras_clave.csv` (ids `V9-`). Ningún resultado de V9 alcanza C3/C3s; todo es "
         "asociación o descripción (C4). «Estado» compara con v8.1.", "",
         "| Factor | Medida de resultado | Magnitud | Método | Signo | Capa | Estado en V9 frente a v8.1 y porqué | Fuente |",
         "|---|---|---|---|---|---|---|---|"]
    for f in filas:
        L.append("| " + " | ".join(f) + " | output/v9/F5/hechos.json; output/v9/f3/tabla_capas.csv |")
    L += ["", "<!-- V9:fin -->"]
    bloque = "\n".join(L)
    t = DOC.read_text(encoding="utf-8")
    if "<!-- V9:inicio -->" in t:
        a, b = t.index("<!-- V9:inicio -->"), t.index("<!-- V9:fin -->") + len("<!-- V9:fin -->")
        t = t[:a] + bloque + t[b:]
    else:
        t = t.rstrip("\n") + "\n\n" + bloque + "\n"
    t = t.replace("Nota V8 (2026-10-13): este historial incluye V8;", "Nota V8 (2026-10-13; V9 2026-10-15): este historial incluye V8 y V9 (adenda «Adenda V9» al final);", 1)
    DOC.write_text(t, encoding="utf-8")
    print("historial: adenda V9 con", len(filas), "filas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
