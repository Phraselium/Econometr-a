"""V16-F5 · Reúne la validación por Monte Carlo de las herramientas de V16 (docs/v16/plan.md, fase 5).

Lee output/v16/montecarlo/<herramienta>/resultado.json y docs/v16/validacion_montecarlo/<herramienta>.md, y escribe:
- docs/v16/validacion_montecarlo.md (publicado como metodologia/validacion_montecarlo_v16.md con `make publicacion`): tabla de
  veredictos y, debajo, la sección de cada herramienta;
- output/v16/montecarlo/veredictos.csv: herramienta, tamaño, cobertura, veredicto, inferencia que se puede usar en la fase 6.
Criterio (adenda del pre-registro V16, punto 11): tamaño al 5 % en [0,04; 0,06] con R ≥ 2.000 y cobertura al 95 % en [0,92; 0,97].
La fase 6 solo usa una herramienta con veredicto APTO o «alternativa APTA» (y entonces con esa inferencia). Sin red; determinista.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
MC = RAIZ / "output" / "v16" / "montecarlo"
SECC = RAIZ / "docs" / "v16" / "validacion_montecarlo"
SAL = RAIZ / "docs" / "v16" / "validacion_montecarlo.md"
TAB = MC / "veredictos.csv"


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# Inferencia que la fase 6 puede usar, revisada a mano contra cada sección (docs/v16/validacion_montecarlo/<herramienta>.md).
# Lo que no figura aquí queda «descriptivo» (estimación puntual sin p-valor ni IC).
INFERENCIA_UTILIZABLE = {
    "sdid_conley_taber": "Conley-Taber (escenario A; tamaño en el límite superior)",
    "conley_seccion": "Conley 2 km (solo escenario principal; no robusto al rango espacial)",
    "gsadf_factor": "bootstrap salvaje (válido con heterocedasticidad; conservador si homocedástico)",
    "bh_jerarquico": "Benjamini-Yekutieli (en lugar de BH jerárquico)",
    "tost": "TOST solo si Δ/EE ≥ umbral; si no, «no concluyente»",
}


# Cifras que deciden el veredicto (inferencia principal o alternativa nombrada), leídas por ruta del resultado.json; el rango de la tabla
# junta escenarios y variantes de referencia (p. ej. Webb en SDID), que no deciden el veredicto.
DETERMINANTE = {
    "bayes_jerarquico": [("cobertura μ mín.", "estimacion.cobertura_mu_min")],
    "bh_jerarquico": [("FDR máx. BH", "estimacion.FDR_max_BH"), ("FDR máx. BY", "estimacion.FDR_max_BY")],
    "blp_gates": [("tamaño", "diagnosticos.tamano"), ("cobertura", "diagnosticos.cobertura_ate_nulo")],
    "cips_bootstrap": [("tamaño bootstrap", "estimacion.tamano_boot")],
    "conley_seccion": [("tamaño Conley", "diagnosticos.tamano_conley"), ("cobertura", "diagnosticos.cobertura_conley")],
    "cs_webb": [("tamaño", "estimacion.tamano"), ("cobertura", "estimacion.cobertura")],
    "csardl": [("tamaño", "estimacion.tamano_5pct"), ("cobertura", "estimacion.cobertura_normal_boot")],
    "dcdh_aleatorizacion": [("tamaño", "estimacion.tamano"), ("cobertura", "estimacion.cobertura")],
    "did_intensidad_webb": [("tamaño Q2a", "diagnosticos.tabla.0.tamano_5pct"), ("cobertura Q2a", "diagnosticos.tabla.0.cobertura_95")],
    "dm_hln": [("tamaño HLN", "estimacion.tamano_HLN_unilateral"), ("tamaño Clark-West", "estimacion.tamano_CW")],
    "gsadf_factor": [("tamaño (salto)", "estimacion.tamano.nulo_salto"), ("tamaño (estocástica)", "estimacion.tamano.nulo_estoc"),
                     ("tamaño (homocedástico)", "estimacion.tamano.nulo_homo")],
    "lp_newey_west_b": [("tamaño mín.", "diagnosticos.tamano_min"), ("tamaño máx.", "diagnosticos.tamano_max")],
    "rejilla_twfe": [("tamaño municipio", "estimacion.tamano.municipio"), ("tamaño provincia", "estimacion.tamano.provincia")],
    "sdid_conley_taber": [("tamaño Conley-Taber A", "estimacion.tamano.A_ct"), ("cobertura A", "estimacion.cobertura.A_ct")],
    "shiftshare_akm": [("tamaño AKM", "diagnosticos.tamano_akm"), ("tamaño AKM0", "diagnosticos.tamano_akm0"),
                       ("cobertura AKM0", "diagnosticos.cobertura_akm0")],
    "tost": [("tamaño en el borde (razón mediana)", "estimacion.tamano_borde_df12_a_razon_mediana")],
}


def _ruta(d, ruta: str):
    for p in ruta.split("."):
        if isinstance(d, list):
            d = d[int(p)] if p.isdigit() and int(p) < len(d) else None
        elif isinstance(d, dict):
            d = d.get(p)
        else:
            return None
    return d


def _determinante(nombre: str, d: dict) -> str:
    partes = []
    for etiqueta, ruta in DETERMINANTE.get(nombre, []):
        n = _num(_ruta(d, ruta))
        if n is not None:
            partes.append(f"{etiqueta} {_fmt(n)}")
    return "; ".join(partes)


def _fallos(x) -> list:
    """Todas las listas «fallos» de los criterios, en cualquier nivel."""
    if isinstance(x, dict):
        out = []
        for k, v in x.items():
            if k == "fallos" and isinstance(v, list):
                out += [str(f) for f in v]
            else:
                out += _fallos(v)
        return out
    if isinstance(x, list):
        return [f for v in x for f in _fallos(v)]
    return []


def _fmt(x) -> str:
    return f"{x:.4f}".rstrip("0").rstrip(",.").replace(".", ",") if isinstance(x, float) else str(x)


def _rango(v) -> str:
    """Un número o un diccionario por escenario/escala → texto «valor» o «mín.-máx.»."""
    if isinstance(v, dict):
        nums = [n for n in (_num(x) for x in v.values()) if n is not None]
        if not nums:
            return ""
        return _fmt(min(nums)) if min(nums) == max(nums) else f"{_fmt(min(nums))}-{_fmt(max(nums))}"
    n = _num(v)
    return "" if n is None else _fmt(n)


def _buscar_prefijo(d: dict, prefijo: str) -> str:
    """Primer valor cuya clave empieza por `prefijo` en estimacion o diagnosticos; con varias claves (p. ej. _min/_max) da el rango."""
    for fuente in (d.get("estimacion") or {}, d.get("diagnosticos") or {}):
        if not isinstance(fuente, dict):
            continue
        claves = [k for k in fuente if k.lower().startswith(prefijo)]
        if not claves:
            continue
        if len(claves) == 1:
            return _rango(fuente[claves[0]])
        valores = {}
        for k in claves:
            v = fuente[k]
            if isinstance(v, dict):
                valores.update({f"{k}.{j}": x for j, x in v.items()})
            else:
                valores[k] = v
        return _rango(valores)
    return ""


def _texto_veredicto(v) -> str:
    if isinstance(v, dict):
        if "veredicto" in v:
            return str(v["veredicto"])
        return "; ".join(f"{k}: {x}" for k, x in v.items())
    return str(v) if v not in (None, "") else "sin veredicto"


def _veredicto(nombre: str, d: dict) -> dict:
    v = None
    for fuente in (d.get("diagnosticos") or {}, d.get("estimacion") or {}, d):
        if isinstance(fuente, dict) and "veredicto" in fuente:
            v = fuente["veredicto"]
            break
    texto = _texto_veredicto(v)
    apto = nombre in INFERENCIA_UTILIZABLE
    fallos = list(dict.fromkeys(_fallos(d.get("diagnosticos") or {})))
    return {"determinante": _determinante(nombre, d),
            "fallos": " / ".join(fallos).replace("|", "/"),
            "tamano": _buscar_prefijo(d, "tamano") or _buscar_prefijo(d, "fdr_max"),
            "cobertura": _buscar_prefijo(d, "cobertura"),
            "replicas": d.get("N", ""),
            "veredicto": texto.replace("|", "/"),
            "inferencia_valida": INFERENCIA_UTILIZABLE[nombre] if apto else "descriptivo"}


def main() -> int:
    filas = []
    for r in sorted(MC.glob("*/resultado.json")):
        d = json.loads(r.read_text(encoding="utf-8"))
        v = _veredicto(r.parent.name, d)
        filas.append({"herramienta": r.parent.name, **v})
    if not filas:
        print("f5_validacion: sin resultados de Monte Carlo todavía")
        return 0
    MC.mkdir(parents=True, exist_ok=True)
    with TAB.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["herramienta", "determinante", "fallos", "tamano", "cobertura", "replicas", "veredicto",
                                           "inferencia_valida"], lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    L = ["# V16 · Validación de herramientas por Monte Carlo (fase 5)", "",
         "Generado por `python3 src/v16/f5_validacion.py`. Cada herramienta se valida con un proceso generador que reproduce la estructura de los "
         "datos de entrenamiento de V16 (unidades, periodos, clusters, calendario de tratamiento, distancias) con resultados SIMULADOS: ningún "
         "dato real de resultado ni ninguna muestra sellada. Criterio (adenda del pre-registro, punto 11): tamaño al 5 % en [0,04; 0,06] con "
         "R ≥ 2.000 réplicas y cobertura al 95 % en [0,92; 0,97]. Una herramienta NO APTA no se usa en la fase 6 (su diseño queda descriptivo).", "",
         "«Cifras determinantes» son las de la inferencia que decide el veredicto (principal o alternativa nombrada); las columnas de rango "
         "juntan todos los escenarios y variantes de referencia (p. ej. Webb en SDID o HC1 en Conley), que no deciden el veredicto. "
         "El detalle de cada herramienta está en su sección, debajo de la tabla.", "",
         "| Herramienta | Cifras determinantes | Fallos del criterio | Tamaño (rango) | Cobertura (rango) | Veredicto | Inferencia utilizable |",
         "|---|---|---|---|---|---|---|"]
    for x in filas:
        L.append(f"| {x['herramienta']} | {x['determinante']} | {x['fallos']} | {x['tamano']} | {x['cobertura']} | {x['veredicto']} | "
                 f"{x['inferencia_valida']} |")
    L.append("")
    for x in filas:
        s = SECC / f"{x['herramienta']}.md"
        if s.exists():
            L += [s.read_text(encoding="utf-8").rstrip(), ""]
    SAL.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"f5_validacion: {len(filas)} herramientas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
