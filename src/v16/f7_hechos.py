"""V16 · Fase 7 · Cifras derivadas para el informe integral, solo LEÍDAS de resultados versionados (sin estimar nada).

La revisión adversarial (K17) pide citar Q3-b (V16) y H4 (V15) como correlaciones frágiles «con mediana y rango». El rango ya está
en V16-Q3-b-beta y V15-H4-beta (min/max = extremos del multiverso); la mediana del multiverso está en sus resultado.json pero no en
cifras_clave. Este script la expone con un id propio. Escribe output/v16/f7_hechos/hechos.json. Sin red, determinista.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v16" / "f7_hechos"


def _hecho(base: dict, i: str, ind: str, valor: float, mn: float, mx: float, origen: str) -> dict:
    return dict(id=i, indicador=ind, valor=valor, min=mn, max=mx, unidad=base["unidad"], periodo=base["periodo"], cobertura=base["cobertura"],
                fuentes=f"{base['fuentes']}; mediana leída de {origen}", capa="C4", fecha_dato=base["fecha_dato"], ficha=base["ficha"])


def main() -> int:
    q3 = {h["id"]: h for h in json.loads((RAIZ / "output/v16/q3/hechos.json").read_text(encoding="utf-8"))}["V16-Q3-b-beta"]
    h4 = {h["id"]: h for h in json.loads((RAIZ / "output/v15/p4/hechos.json").read_text(encoding="utf-8"))}["V15-H4-beta"]
    r3 = json.loads((RAIZ / "output/v16/q3/resultado.json").read_text(encoding="utf-8"))["estimacion"]["Q3-b"]["multiverso"]
    r4 = json.loads((RAIZ / "output/v15/p4/resultado.json").read_text(encoding="utf-8"))["diagnosticos"]["multiverso_64"]
    H = [_hecho(q3, "V16-Q3-b-mediana", f"Q3-b: mediana de las {r3['n_especificaciones']} especificaciones del multiverso (min/max = extremos; "
                "correlación frágil, sin inferencia válida)", r3["mediana_beta_por_DT"], r3["min"], r3["max"],
                "output/v16/q3/resultado.json (estimacion.Q3-b.multiverso)"),
         _hecho(h4, "V15-H4-mediana", f"H4: mediana de las {r4['n']} especificaciones del multiverso, % por punto (min/max = extremos; "
                "correlación frágil)", round(100 * r4["beta_pp_mediana"], 4), round(100 * r4["beta_pp_min"], 4), round(100 * r4["beta_pp_max"], 4),
                "output/v15/p4/resultado.json (diagnosticos.multiverso_64, ×100)")]
    # H5 (V15): la revisión adversarial (1.1) pide citar el rango entre implementaciones; el extremo inferior es la réplica ciega (K16)
    h5 = {h["id"]: h for h in json.loads((RAIZ / "output/v15/p9/hechos.json").read_text(encoding="utf-8"))}["V15-H5-razon-ecm"]
    rr = json.loads((RAIZ / "output/v16/replica/h5/resultado.json").read_text(encoding="utf-8"))["estimacion"]["razon_ECM_comb_AR4"]
    H.append(dict(_hecho(h5, "V15-H5-razon-replica", "H5: razón ECM de la combinación frente al AR(4) en la réplica ciega de V16 (otra implementación "
                         "de las elecciones abiertas; min/max = réplica y producción pre-registrada)", round(rr, 4), round(rr, 4), round(h5["valor"], 4),
                         "output/v16/replica/h5/resultado.json (estimacion.razon_ECM_comb_AR4)"), fuentes=h5["fuentes"] + "; réplica ciega de V16"))
    # Arbitraje del informe (hallazgo 7): si dos medidas discrepan se dan ambas. El IPV del INE (ajustado por calidad) de 2019-2025 está
    # en la ficha de V16-HEC-PRECIO-{NOM,REAL}-2019-2025 («Todas las medidas»), sin id propio; se expone aquí como C4 (una sola fuente).
    import re
    fichas = (RAIZ / "output/v16/f2_hechos/fichas.md").read_text(encoding="utf-8")
    hh = {h["id"]: h for h in json.loads((RAIZ / "output/v16/f2_hechos/hechos.json").read_text(encoding="utf-8"))}
    for tipo, etq in (("NOM", "nominal"), ("REAL", "real (deflactor IPC general)")):
        i = f"V16-HEC-PRECIO-{tipo}-2019-2025"
        bloque = fichas.split(f"### {i}\n", 1)[1].split("\n### ", 1)[0]
        v = float(re.search(r"'INE IPV': ([-0-9.]+)", bloque).group(1))
        b = hh[i]
        H.append(dict(id=f"V16-HEC-IPV-{tipo}-2019-2025", indicador=f"Precio de compra, cambio acumulado {etq} 2019-2025 (media anual), España; medida: "
                      "IPV del INE (ajustado por calidad); una sola fuente", valor=v, min=None, max=None, unidad="%", periodo=b["periodo"],
                      cobertura="España", fuentes="INE IPV; leído de output/v16/f2_hechos/fichas.md («Todas las medidas»)", capa="C4",
                      fecha_dato=b["fecha_dato"], ficha=b["ficha"]))
    # Arbitraje (hallazgo 15): mínimo alternativo de T4-H2 con interpolación lineal (orden del autor K20; réplica ciega v10_b2)
    t4 = [x for x in json.loads((RAIZ / "output/v16/replica/v10_b2/resultado.json").read_text(encoding="utf-8")) if x["id"] == "T4-H2"][0]
    H.append(dict(id="V16-T4-H2-min-interp", indicador="T4-H2: mínimo de la rejilla del cambio del déficit 2025-2030 con interpolación lineal entre 2025 "
                  "y el relleno (el publicado, con la convención «tras 2025 = relleno», es el min de T4-H2)", valor=round(t4["replica"]["min"], 1),
                  min=None, max=None, unidad="viviendas", periodo="2026-2030", cobertura="España",
                  fuentes="Réplica ciega de V16 (output/v16/replica/v10_b2/resultado.json)", capa="C4", fecha_dato="2025",
                  ficha="output/v6_2/anexo_metodologico.md (T4-H2 / T4-H3, dos versiones del mínimo)"))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "hechos.json").write_text(json.dumps(H, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"f7_hechos: {len(H)} cifras derivadas en {(OUT / 'hechos.json').relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
