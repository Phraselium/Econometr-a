"""V16-F6 · Triangulación entre diseños y comparación con la literatura (docs/v16/plan.md, fase 6.7).

Lee las estimaciones de output/v15/*/resultado*.json y output/v16/q*/resultado.json (por ruta explícita, sin copiar cifras a mano) y los
rangos de la literatura de output/v16/f3/metaanalisis.csv. Ningún grupo de la literatura tiene metaanálisis (≥ 5 estudios con EE y la
misma unidad; decisión K7), así que la comparación es de SIGNO y, cuando la unidad coincide, de orden de magnitud.
Regla del plan: si un resultado se aparta de la literatura, se explica por qué o se rebaja la capa. Todos los resultados ya son C4 y
la mayoría solo puntuales; un apartamiento sin explicación los deja en DESCRIPTIVO.
Escribe output/v16/triangulacion/informe.md y resultado.json. Sin red; determinista.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v16" / "triangulacion"
META = RAIZ / "output" / "v16" / "f3" / "metaanalisis.csv"

# (id, pregunta, fichero, ruta, unidad, grupo de literatura (instrumento, resultado) o None, explicación si el signo difiere)
FILAS = [
    ("H1-CS", "Zonas tensionadas y renta de contratos nuevos (Cataluña)", "output/v15/p6/resultado_H1.json", "estimacion.CS_att_pct", "%",
     ("L1_control_alquileres", "renta_contratos_regulados"), ""),
    ("H1-SDID", "Ídem, SDID", "output/v15/p6/resultado_H1.json", "estimacion.SDID_att_pct", "%",
     ("L1_control_alquileres", "renta_contratos_regulados"), ""),
    ("H2-PPML", "Zonas tensionadas y número de contratos", "output/v15/p6/resultado_H2.json", "estimacion.PPML_principal_pct", "%",
     ("L1_control_alquileres", "oferta_contratos"), ""),
    ("Q1c", "Zonas tensionadas y compraventas provinciales", "output/v16/q1/resultado.json", "estimacion.Q1c_estimador_CS_global_dlog", "log",
     ("L1_control_alquileres", "compraventa_numero"), ""),
    ("H3", "Vivienda turística y alquiler por sección", "output/v15/p5/resultado.json", "estimacion.beta_pct_por_DT", "% por DT",
     ("L2_vivienda_turistica_regulacion", "alquiler"), ""),
    ("Q2a", "Vivienda turística y IPC de alquiler provincial", "output/v16/q2/resultado.json", "estimacion.Q2a_beta_por_DT_log_exposicion", "log por DT",
     ("L2_vivienda_turistica_regulacion", "alquiler"), ""),
    ("Q2c", "Vivienda turística e IPVA municipal", "output/v16/q2/resultado.json", "estimacion.Q2c_beta_por_DT", "log por DT",
     ("L2_vivienda_turistica_regulacion", "alquiler"),
     "Signo opuesto al de la literatura con una magnitud muy pequeña frente a la referencia (0,063) y sin inferencia válida: no se distingue "
     "de cero en ningún sentido operativo; se lee como robustez de H3 (casi nula), no como evidencia en contra."),
    ("H4", "Inmigración y alquiler municipal (shift-share)", "output/v15/p4/resultado.json", "estimacion.beta_pp_alquiler_por_pp_poblacion_extranjera",
     "% por p.p.", None, ""),
    ("Q3-c1", "Inmigración y valor tasado provincial", "output/v16/q3/resultado.json",
     "estimacion.Q3-c1.beta_log_valor_tasado_por_punto_poblacion_extranjera_predicha", "log por punto", None, ""),
    ("Q3-b", "Inmigración y alquiler por sección", "output/v16/q3/resultado.json", "estimacion.Q3-b.beta_dlog_serpavi_por_DT_cuota_extranjeros",
     "log por DT", None, ""),
    ("Q6-v", "ITP y compraventas", "output/v16/q6/resultado.json", "estimacion.Q6-v.beta_por_punto_de_tipo", "log por punto",
     ("L4_fiscalidad_compra", "compraventas"),
     "Signo opuesto a la referencia (−0,07) y a la mediana de la literatura; el placebo con ΔY retardado es de signo contrario y mayor que la "
     "estimación, y los 14 cambios de tipo se concentran en 2012-2013 (crisis): el diseño no separa el ITP del ciclo. Queda DESCRIPTIVO."),
    ("Q6-p", "ITP y valor tasado", "output/v16/q6/resultado.json", "estimacion.Q6-p.beta_por_punto_de_tipo", "log por punto",
     ("L4_fiscalidad_compra", "precio"), ""),
    ("Q5-p", "Sorpresas monetarias y valor tasado (h = 4)", "output/v16/q5/resultado.json", "estimacion.Q5-p.beta_h4_pct_por_DT", "% por DT", None, ""),
]
# Pares de diseños que miden lo mismo con datos o métodos distintos (triangulación interna).
PARES = [("H1-CS", "H1-SDID"), ("H3", "Q2a"), ("H3", "Q2c"), ("H4", "Q3-c1"), ("H4", "Q3-b")]
# Magnitudes de referencia pre-registradas (adenda V16, punto 3; V15 para H1), por ruta, para el orden de magnitud.
REFERENCIA = {"Q2a": ("output/v16/q2/resultado.json", "estimacion.Q2a_referencia_por_DT"),
              "Q2c": ("output/v16/q2/resultado.json", "estimacion.Q2c_referencia_por_DT"),
              "Q6-v": ("output/v16/q6/resultado.json", "estimacion.Q6-v.magnitud_referencia"),
              "Q6-p": ("output/v16/q6/resultado.json", "estimacion.Q6-p.magnitud_referencia"),
              "Q5-p": ("output/v16/q5/resultado.json", "estimacion.Q5-p.magnitud_referencia_pct")}


def _ruta(fichero: str, ruta: str):
    d = json.loads((RAIZ / fichero).read_text(encoding="utf-8"))
    for p in ruta.split("."):
        d = d[p]
    return float(d)


def _signo(x: float) -> int:
    return 0 if x == 0 else (1 if x > 0 else -1)


def literatura() -> dict:
    with META.open(encoding="utf-8") as fh:
        return {(r["instrumento"], r["resultado"]): r for r in csv.DictReader(fh)}


def main() -> int:
    lit = literatura()
    filas, val = [], {}
    for i, preg, fich, ruta, unidad, grupo, expl in FILAS:
        v = _ruta(fich, ruta)
        val[i] = v
        ref = _ruta(*REFERENCIA[i]) if i in REFERENCIA else None
        fila = {"id": i, "pregunta": preg, "estimacion": v, "unidad": unidad, "fuente": f"{fich}#{ruta}", "referencia_prereg": ref}
        if grupo and grupo in lit:
            g = lit[grupo]
            med = float(g["mediana"])
            mezcla = "mezcla" in g["aviso"]
            mismo = _signo(v) == _signo(med)
            fila.update({"literatura": f"{grupo[0]} / {grupo[1]}", "estudios": int(g["estudios"]), "lit_min": float(g["min"]),
                         "lit_mediana": med, "lit_max": float(g["max"]), "unidades_mezcladas": mezcla, "mismo_signo": mismo})
            if mismo:
                fila["lectura"] = "mismo signo que la literatura" + (" (unidades no comparables: solo signo)" if mezcla else "")
            else:
                fila["lectura"] = "SE APARTA de la literatura: " + (expl or "sin explicación: queda DESCRIPTIVO")
        else:
            fila.update({"literatura": "sin grupo comparable en output/v16/f3/metaanalisis.csv", "lectura": "sin comparación con la literatura"})
        if ref is not None:
            fila["mismo_signo_que_referencia"] = _signo(v) == _signo(ref)
            fila["cociente_sobre_referencia"] = v / ref
        filas.append(fila)
    pares = [{"a": a, "b": b, "mismo_signo": _signo(val[a]) == _signo(val[b])} for a, b in PARES]
    OUT.mkdir(parents=True, exist_ok=True)
    res = {"rama": "v16-triangulacion", "pregunta": "triangulación entre diseños y comparación con la literatura (fase 6.7)", "capa": "C4",
           "metodo": "comparación de signo y, con la misma unidad, de orden de magnitud; sin metaanálisis (0 de 88 grupos lo permiten, K7)",
           "filas": filas, "pares": pares,
           "notas": "Ningún resultado sube de capa por coincidir con la literatura; los que se apartan sin explicación quedan DESCRIPTIVO."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    f = (lambda x, n=4: "" if x is None else f"{x:.{n}g}".replace(".", ","))
    L = ["# V16 · Triangulación y comparación con la literatura (fase 6)", "",
         "Generado por `python3 src/v16/f6_triangulacion.py`. " + res["metodo"] + ". " + res["notas"], "",
         "| Id | Pregunta | Estimación | Unidad | Referencia pre-registrada | Literatura (mín · mediana · máx; estudios) | Lectura |", "|---|---|---|---|---|---|---|"]
    for x in filas:
        litx = (f"{f(x['lit_min'])} · {f(x['lit_mediana'])} · {f(x['lit_max'])}; {x['estudios']}" if "lit_mediana" in x else "—")
        L.append(f"| {x['id']} | {x['pregunta']} | {f(x['estimacion'])} | {x['unidad']} | {f(x['referencia_prereg'])} | {litx} | {x['lectura']} |")
    L += ["", "## Triangulación entre diseños", "", "| Diseño A | Diseño B | Mismo signo |", "|---|---|---|"]
    L += [f"| {p['a']} | {p['b']} | {'sí' if p['mismo_signo'] else 'NO'} |" for p in pares]
    L += ["", "Las cifras salen por ruta de cada resultado.json (columna «fuente» de resultado.json); los rangos de la literatura mezclan "
          "unidades salvo que se diga lo contrario, así que solo se compara el signo."]
    (OUT / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"f6_triangulacion: {len(filas)} filas; se apartan: {[x['id'] for x in filas if x.get('mismo_signo') is False]}; "
          f"pares con signo distinto: {[(p['a'], p['b']) for p in pares if not p['mismo_signo']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
