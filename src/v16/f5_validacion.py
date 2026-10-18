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


def _determinante(nombre: str, d: dict, determinante: dict) -> str:
    partes = []
    for etiqueta, ruta in determinante.get(nombre, []):
        x = _ruta(d, ruta)
        texto = _rango(x)  # un número, o «mín.-máx.» si la ruta apunta a un diccionario por celda o escenario
        if texto:
            partes.append(f"{etiqueta} {texto}")
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
        return "; ".join(f"{k}: {_texto_veredicto(x)}" for k, x in v.items())
    return str(v) if v not in (None, "") else "sin veredicto"


def _veredicto(nombre: str, d: dict, inferencia: dict = INFERENCIA_UTILIZABLE, determinante: dict = DETERMINANTE) -> dict:
    v = None
    for fuente in (d.get("diagnosticos") or {}, d.get("estimacion") or {}, d):
        if isinstance(fuente, dict) and "veredicto" in fuente:
            v = fuente["veredicto"]
            break
    if v is None:  # veredictos por escenario o por inferencia (veredicto_DM, veredictos_por_inferencia, ...)
        g = d.get("diagnosticos") or {}
        if "veredicto_por_escenario" in g:  # el veredicto del diseño; los de cada inferencia quedan en la sección
            g = {"veredicto_por_escenario": g["veredicto_por_escenario"]}
        v = {k: (_texto_veredicto(x) if isinstance(x, dict) and "veredicto" in x else x)
             for k, x in g.items() if k.startswith("veredicto")} or None
    texto = _texto_veredicto(v)
    apto = nombre in inferencia
    fallos = list(dict.fromkeys(_fallos(d.get("diagnosticos") or {})))
    return {"determinante": _determinante(nombre, d, determinante),
            "fallos": (" / ".join(fallos[:4]) + (f" / (y {len(fallos) - 4} más)" if len(fallos) > 4 else "")).replace("|", "/"),
            "tamano": _buscar_prefijo(d, "tamano") or _buscar_prefijo(d, "fdr_max"),
            "cobertura": _buscar_prefijo(d, "cobertura"),
            "replicas": d.get("N", ""),
            "veredicto": texto.replace("|", "/"),
            "inferencia_valida": inferencia[nombre] if apto else "descriptivo"}


# V15 (herramientas pendientes validadas en la fase 5 de V16): mismas reglas de lectura; criterio de cada sección.
INFERENCIA_V15 = {
    "sar_sdm": "Wald de ρ y efectos indirectos (SAR/SDM/SEM, contigüidad y distancia inversa a 25 km)",
    "dfm_bvar_mcs": "DM-HLN (Clark-West y MCS al 10 % NO APTOS)",
}
DETERMINANTE_V15 = {
    "akm_municipal": [("tamaño AKM", "estimacion.tamano_AKM"), ("tamaño AKM0", "estimacion.tamano_AKM0"),
                      ("cobertura AKM0", "estimacion.cobertura_AKM0")],
    "control_sintetico": [("tamaño", "estimacion.tamano"), ("cobertura", "estimacion.cobertura")],
    "dfm_bvar_mcs": [("tamaño DM-HLN", "estimacion.tamano_DM_HLN"), ("tamaño Clark-West", "estimacion.tamano_CW_delta0"),
                     ("tamaño MCS 10 %", "estimacion.tamano_mcs_10pct")],
    "honest_did": [("tamaño M̄=0", "estimacion.tamano_A"), ("tamaño M̄=0 con Σ verdadera", "estimacion.tamano_A_Sigma_verdadera"),
                   ("potencia M̄=1", "estimacion.potencia_B_mde")],
    "westerlund_csardl": [("tamaño Gτ", "estimacion.tamano_Gtau"), ("cobertura velocidad CS-ARDL", "estimacion.cobertura_CSARDL_velocidad")],
    "sar_sdm": [("tamaño Wald ρ (rango de celdas)", "estimacion.tamano_wald_rho_hetero"),
                ("cobertura efecto indirecto (rango)", "estimacion.cobertura_indirecto_hetero")],
    "sdid_placebo_h1h2": [("tamaño Webb S1", "estimacion.S1_H1_74donantes.webb_cluster.tamano"),
                          ("S2", "estimacion.S2_H1_14donantes_10km.webb_cluster.tamano"),
                          ("S3", "estimacion.S3_H2_74donantes.webb_cluster.tamano")],
    "wild_webb_v15": [("tamaño W1", "estimacion.tamano_W1"), ("cobertura W1", "estimacion.cobertura_W1")],
}
VERSIONES = {
    "v16": dict(mc=MC, secc=SECC, sal=SAL, inferencia=INFERENCIA_UTILIZABLE, determinante=DETERMINANTE,
                titulo="# V16 · Validación de herramientas por Monte Carlo (fase 5)", publicado="metodologia/validacion_montecarlo_v16.md",
                criterio="Criterio (adenda del pre-registro V16, punto 11): tamaño al 5 % en [0,04; 0,06] con R ≥ 2.000 réplicas y "
                         "cobertura al 95 % en [0,92; 0,97]."),
    "v15": dict(mc=RAIZ / "output" / "v15" / "montecarlo", secc=RAIZ / "docs" / "v15" / "validacion_montecarlo",
                sal=RAIZ / "docs" / "v15" / "validacion_montecarlo.md", inferencia=INFERENCIA_V15, determinante=DETERMINANTE_V15,
                titulo="# V15 · Validación por Monte Carlo de las herramientas pendientes (fase 5 de V16)",
                publicado="metodologia/validacion_montecarlo_v15.md",
                criterio="Criterio: el de la fase 5 de V16 (tamaño al 5 % en [0,04; 0,06] con R ≥ 2.000 y cobertura al 95 % en [0,92; 0,97]); "
                         "cada sección declara su proceso generador y sus rectificaciones."),
}


def main(version: str = "v16") -> int:
    c = VERSIONES[version]
    mc, secc, sal = c["mc"], c["secc"], c["sal"]
    filas = []
    for r in sorted(mc.glob("*/resultado.json")):
        d = json.loads(r.read_text(encoding="utf-8"))
        v = _veredicto(r.parent.name, d, c["inferencia"], c["determinante"])
        filas.append({"herramienta": r.parent.name, **v})
    if not filas:
        print("f5_validacion: sin resultados de Monte Carlo todavía")
        return 0
    mc.mkdir(parents=True, exist_ok=True)
    with (mc / "veredictos.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["herramienta", "determinante", "fallos", "tamano", "cobertura", "replicas", "veredicto",
                                           "inferencia_valida"], lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    L = [c["titulo"], "",
         f"Generado por `python3 src/v16/f5_validacion.py {version}`; publicado como {c['publicado']}. Cada herramienta se valida con un "
         "proceso generador que reproduce la estructura de los datos de entrenamiento (unidades, periodos, clusters, calendario de "
         "tratamiento, distancias) con resultados SIMULADOS: ningún dato real de resultado ni ninguna muestra sellada. "
         f"{c['criterio']} Una herramienta NO APTA no se usa en la fase 6 (su diseño queda descriptivo).", "",
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
        s = secc / f"{x['herramienta']}.md"
        if s.exists():
            L += [s.read_text(encoding="utf-8").rstrip(), ""]
    sal.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"f5_validacion {version}: {len(filas)} herramientas")
    return 0


if __name__ == "__main__":
    sys.exit(main(*(sys.argv[1:2] or ["v16"])) if len(sys.argv) < 2 or sys.argv[1] != "todas" else max(main("v16"), main("v15")))
