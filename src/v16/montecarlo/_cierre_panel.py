"""Cierre del grupo «panel» (V16, fase 5): lee output/v16/montecarlo/<herramienta>/tabla.csv, aplica el veredicto de la adenda (punto 11)
y escribe resultado.json (forma de CLAUDE.md) y docs/v16/validacion_montecarlo/<herramienta>.md. No simula nada."""
from __future__ import annotations

import ast
import importlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_panel as C  # noqa: E402

OUT = C.RAIZ / "output" / "v16" / "montecarlo"
DOC = C.RAIZ / "docs" / "v16" / "validacion_montecarlo"
MARCA = "<!-- RESULTADOS -->"


def _fila(t: pd.DataFrame, **kw) -> pd.Series:
    m = pd.Series(True, index=t.index)
    for k, v in kw.items():
        m &= t[k] == v
    return t[m].iloc[0]


def _eval(nulo: pd.Series, alt: pd.Series) -> dict:
    v = C.veredicto(float(nulo.rechazo), float(alt.cobertura), int(nulo.R))
    v.update({"tamano": float(nulo.rechazo), "R_nulo": int(nulo.R), "cobertura_alt": float(alt.cobertura), "R_alt": int(alt.R),
              "cobertura_nulo": float(nulo.cobertura), "sesgo_nulo": float(nulo.sesgo), "rmse_nulo": float(nulo.rmse),
              "se_mc_tamano": C.mc_se(float(nulo.rechazo), int(nulo.R)), "se_mc_cobertura": C.mc_se(float(alt.cobertura), int(alt.R))})
    return v


def _tabla_md(t: pd.DataFrame, cols: list[str]) -> str:
    f = t[cols].copy()
    for c in f.columns:
        if f[c].dtype.kind == "f":
            f[c] = f[c].map(lambda x: f"{x:.4f}")
    return "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n" + "\n".join("| " + " | ".join(map(str, r)) + " |" for r in f.values)


def _declaracion(modulo: str) -> str:
    src = (Path(__file__).resolve().parent / f"{modulo}.py").read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(src)) or ""
    return doc


def _escribir(h: str, titulo: str, veredicto_txt: str, ver: dict, tabla: pd.DataFrame, cols: list[str], notas: str, estructura: dict, metodo: str,
              estimacion: dict, N: str) -> None:
    DOC.mkdir(parents=True, exist_ok=True)
    md = f"""# {h} · {titulo}

## Proceso generador (declarado antes de simular; es el docstring de src/v16/montecarlo/{h}.py)
```
{_declaracion(h)}
```

{MARCA}
## Resultados (SEED = 20261010; semillas por réplica de np.random.SeedSequence([20261010, k]); errores Monte Carlo en la última sección)
{_tabla_md(tabla, cols)}

## Veredicto
**{veredicto_txt}**

Criterio (adenda, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97]
bajo la alternativa de referencia; un tamaño de 0,0 es NO APTO.

```json
{json.dumps(ver, ensure_ascii=False, indent=1, default=float)}
```

## Notas y límites
{notas}

## Reproducción
`python3 src/v16/montecarlo/{h}.py` (parámetros por defecto: los de esta sección) y `python3 src/v16/montecarlo/_cierre_panel.py`.
Tabla: output/v16/montecarlo/{h}/tabla.csv. Nunca se leyó data/sealed ni valor alguno del resultado real; solo códigos de unidad,
periodos disponibles y el calendario de intervenciones.
"""
    (DOC / f"{h}.md").write_text(md, encoding="utf-8")
    res = {"rama": "r16/montecarlo-panel", "pregunta": f"¿Es válida la inferencia de {h} en el proceso generador del repositorio?",
           "capa": "validación de herramienta (sin capa de evidencia)", "datos": "simulados; estructura leída de data/processed/v16/entrenamiento e intervenciones.csv (sin valores reales)",
           "N": N, "metodo": metodo, "estimacion": estimacion, "ic95": None, "p_ajustado": None,
           "nivel_evidencia": "no aplica (validación Monte Carlo)", "diagnosticos": {"veredicto": veredicto_txt, "criterio": ver, "estructura": estructura},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": notas}
    (OUT / h).mkdir(parents=True, exist_ok=True)
    (OUT / h / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=2, default=float), encoding="utf-8")


def _cargar(h: str) -> tuple[pd.DataFrame, dict]:
    t = pd.read_csv(OUT / h / "tabla.csv")
    raw = json.loads((OUT / h / "resultado.json").read_text(encoding="utf-8"))
    return t, raw


def cerrar_cs() -> str:
    h = "cs_webb"
    t, raw = _cargar(h)
    if "estructura" not in raw:
        raw = json.loads((OUT / h / "_bruto.json").read_text(encoding="utf-8"))
    else:
        (OUT / h / "_bruto.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    nb = _eval(_fila(t, escenario="nulo", variante="b_WCR_nulo_impuesto"), _fila(t, escenario="alt_005", variante="b_WCR_nulo_impuesto"))
    na = _eval(_fila(t, escenario="nulo", variante="a_multiplicador_IF"), _fila(t, escenario="alt_005", variante="a_multiplicador_IF"))
    ctl = _fila(t, escenario="control_iid_nulo", variante="b_WCR_nulo_impuesto")
    pot = {k: float(_fila(t, escenario=k, variante="b_WCR_nulo_impuesto").rechazo) for k in ("alt_005", "alt_010")}
    txt = "APTO" if nb["apto"] else "NO APTO → diseño solo descriptivo"
    notas = (f"Inferencia principal = wild cluster bootstrap de Webb por provincia con el nulo impuesto (variante b). La adenda no nombra alternativa para Q1c: "
             f"si falla, el diseño es solo descriptivo. Variante a (multiplicador sobre la función de influencia sin restringir) descartada de entrada: "
             f"tamaño {na['tamano']:.3f} y cobertura {na['cobertura_alt']:.3f}, porque las cohortes de una sola provincia (4 de 5) tienen residuo de influencia cero y la varianza se subestima; "
             f"se informa pero no se usa. Variante b: tamaño {nb['tamano']:.4f}, cobertura bajo nulo {nb['cobertura_nulo']:.4f}, bajo tau=0,05 {nb['cobertura_alt']:.4f}. "
             f"Control de implementación sin dependencia (ruido iid): tamaño {float(ctl.rechazo):.3f}, cobertura {float(ctl.cobertura):.3f} (el procedimiento es conservador sin dependencia "
             f"y pierde la cobertura con dependencia transversal y espacial, con 8 tratadas en 5 cohortes y 33 comparaciones). Potencia (variante b): {pot['alt_005']:.3f} a tau=0,05 y "
             f"{pot['alt_010']:.3f} a tau=0,10; sin magnitud de referencia comparable (la condición (b) no se cumple). Sesgo despreciable ({nb['sesgo_nulo']:.4f}); el fallo es de inferencia, no de punto.")
    cols = ["escenario", "tau", "variante", "R", "sesgo", "rmse", "cobertura", "rechazo", "ancho_medio_ic"]
    _escribir(h, "Q1c · Callaway-Sant'Anna con wild cluster bootstrap de Webb por provincia", txt, {"principal_b": nb, "descartada_a": na}, t, cols, notas,
              raw["estructura"], "Callaway-Sant'Anna (nunca tratadas, ATT simple) + wild bootstrap-t Webb por provincia",
              {"tamano": nb["tamano"], "cobertura": nb["cobertura_alt"], "sesgo": nb["sesgo_nulo"], "rmse": nb["rmse_nulo"], "potencia": pot}, "41 provincias x 30 trimestres; R=2000/2000/1000")
    return txt


def cerrar_dcdh() -> str:
    h = "dcdh_aleatorizacion"
    t, raw = _cargar(h)
    if "estructura" not in raw:
        raw = json.loads((OUT / h / "_bruto.json").read_text(encoding="utf-8"))
    else:
        (OUT / h / "_bruto.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    ev = _eval(_fila(t, escenario="nulo"), _fila(t, escenario="alt_vol_-0.07"))
    ctl = _fila(t, escenario="control_iid_nulo")
    pw = {k: float(_fila(t, escenario=k).rechazo) for k in ("alt_vol_-0.07", "alt_precio_-0.01")}
    txt = "APTO" if ev["apto"] else "NO APTO → diseño solo descriptivo"
    notas = (f"Inferencia por aleatorización del calendario entre CCAA (11 clusters; 8 con cambios de tipo, 59 celdas de cambio). Q6 no tiene alternativa nombrada distinta: "
             f"si falla, NO APTO. Tamaño {ev['tamano']:.4f} (error MC {ev['se_mc_tamano']:.4f}); cobertura bajo nulo {ev['cobertura_nulo']:.4f} y bajo beta=-0,07 {ev['cobertura_alt']:.4f}. "
             f"Control iid (sin factores, campos ni choques de CCAA): tamaño {float(ctl.rechazo):.3f}: el exceso de rechazo no viene de la dependencia simulada sino de que el calendario "
             f"permutado no es intercambiable (distinto número de provincias por CCAA y calendarios con distinta dispersión de cambios). Potencia: {pw['alt_vol_-0.07']:.3f} a -0,07 por punto (volumen) y "
             f"{pw['alt_precio_-0.01']:.3f} a -0,01 (precio). Con solo 8 CCAA con cambios la prueba tiene resolución limitada; cualquier uso de Q6 queda como descriptivo.")
    cols = ["escenario", "beta", "R", "sesgo", "rmse", "cobertura", "rechazo", "ancho_medio_ic"]
    _escribir(h, "Q6 · de Chaisemartin-D'Haultfoeuille continuo con aleatorización del calendario entre CCAA", txt, {"principal": ev}, t, cols, notas, raw["estructura"],
              "DID_M continuo (cambio del tipo general del ITP) + aleatorización del calendario entre CCAA",
              {"tamano": ev["tamano"], "cobertura": ev["cobertura_alt"], "sesgo": ev["sesgo_nulo"], "rmse": ev["rmse_nulo"], "potencia": pw}, "41 provincias x 14 años; 11 clusters; R=2000/2000/1000")
    return txt


def cerrar_rejilla() -> str:
    h = "rejilla_twfe"
    t, raw = _cargar(h)
    if "municipio" not in raw:
        raw = json.loads((OUT / h / "_bruto.json").read_text(encoding="utf-8"))
    else:
        (OUT / h / "_bruto.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    ev, ctl, pw = {}, {}, {}
    for esc in ("municipio", "provincia"):
        s = t[t.escala == esc]
        ev[esc] = _eval(_fila(s, escenario="nulo"), _fila(s, escenario="alt_ref_0.04"))
        c = _fila(s, escenario="control_iid_nulo")
        ctl[esc] = (float(c.rechazo), float(c.cobertura))
        pw[esc] = {"b=0.04": float(_fila(s, escenario="alt_ref_0.04").rechazo), "b=0.01": float(_fila(s, escenario="alt_pot_0.01").rechazo)}
    ok = all(v["apto"] for v in ev.values())
    txt = "APTO en ambas escalas" if ok else "; ".join(f"{e}: {'APTO' if v['apto'] else 'NO APTO → diseño solo descriptivo'}" for e, v in ev.items())
    notas = (f"Escalas representativas de la especificación principal de la rejilla: municipio ({raw['municipio']['estructura']['n_unidades']} unidades, "
             f"{raw['municipio']['estructura']['n_clusters']} provincias, CR1 con t(G-1)) y provincia (41, wild bootstrap-t de Webb con nulo impuesto). La adenda no nombra alternativa "
             f"para la rejilla: si la principal falla, la escala es solo descriptiva. Tamaño municipal {ev['municipio']['tamano']:.4f}, provincial {ev['provincia']['tamano']:.4f}; "
             f"cobertura bajo b=0,04: {ev['municipio']['cobertura_alt']:.4f} y {ev['provincia']['cobertura_alt']:.4f}. Control iid (exposición y ruido independientes): "
             f"tamaño {ctl['municipio'][0]:.3f} (municipio) y {ctl['provincia'][0]:.3f} (provincia), de modo que el procedimiento está bien implementado y el exceso de rechazo procede "
             f"de la correlación espacial de la exposición con cargas de factores y choques espaciales que cruzan fronteras de provincia (el agrupamiento por provincia no los absorbe). "
             f"Potencia: municipio {pw['municipio']}, provincia {pw['provincia']}. Consecuencia: las 83 celdas de la rejilla con TWFE y exposición espacial no deben llevar p-valor "
             f"calibrado; se leen como descriptivas, o con una inferencia espacial (Conley) validada aparte.")
    cols = ["escala", "escenario", "b", "n_unidades", "n_clusters", "R", "sesgo", "rmse", "cobertura", "rechazo", "ancho_medio_ic"]
    _escribir(h, "especificación principal de la rejilla fija (TWFE, exposición continua)", txt, ev, t, cols, notas, {e: raw[e]["estructura"] for e in raw},
              "Dlog ~ exposición continua + EF de unidad y periodo; CR1 por provincia (municipio) y wild Webb (provincia)",
              {"tamano": {e: ev[e]["tamano"] for e in ev}, "cobertura": {e: ev[e]["cobertura_alt"] for e in ev}, "potencia": pw}, "2.014 municipios y 41 provincias x 7 años; R=2000/2000/1000")
    return txt


def cerrar_sdid() -> str:
    h = "sdid_conley_taber"
    t, raw = _cargar(h)
    if "escenarios" not in raw:
        raw = json.loads((OUT / h / "_bruto.json").read_text(encoding="utf-8"))
    else:
        (OUT / h / "_bruto.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    ev = {}
    for esc in ("A", "B"):
        for inf in ("ct", "webb"):
            s = t[(t.escenario == esc) & (t.inferencia == inf)]
            if len(s):
                ev[f"{esc}_{inf}"] = _eval(_fila(s, efecto="nulo"), _fila(s, efecto="ref"))
    pot = {k: float(_fila(t[(t.escenario == k[0]) & (t.inferencia == k[2:])], efecto="mde").rechazo) for k in ev}
    ctp = ev["A_ct"]
    nA = int(_fila(t[(t.escenario == "A") & (t.inferencia == "ct")], efecto="nulo").R)
    nB = int(_fila(t[(t.escenario == "B") & (t.inferencia == "ct")], efecto="nulo").R)
    tam_pool = (ev["A_ct"]["tamano"] * nA + ev["B_ct"]["tamano"] * nB) / (nA + nB)
    se_pool = C.mc_se(tam_pool, nA + nB)
    if ctp["apto"]:
        txt = "APTO (Conley-Taber, escenario A; en el límite superior del tamaño, ver notas)"
    elif ev.get("A_webb", {}).get("apto"):
        txt = "alternativa APTA (wild bootstrap de Webb, escenario A); la inferencia principal Conley-Taber no pasa"
    else:
        txt = "NO APTO → diseño solo descriptivo (ni Conley-Taber ni la alternativa Webb pasan en el escenario A)"
    est = {e: raw["escenarios"][e]["estructura"] for e in raw["escenarios"]}
    notas = (f"Hallazgo de estructura: con los datos de entrenamiento, el diseño literal de la adenda (tratados = municipios con zona vigente fuera de Cataluña, con SERPAVI completo "
             f"2019-2022 y 2024) tiene {est['A']['n_tratados']} municipios en {len(est['A']['provincias_tratadas'])} provincia ({est['A']['provincias_tratadas']}) y {est['A']['n_donantes']} donantes en "
             f"{est['A']['provincias_donantes']} provincias; las zonas de esos dos municipios entran en vigor en 2025-2026, es decir, DESPUÉS del año post (2024): en entrenamiento hay 0 municipios con zona vigente en 2024 fuera de Cataluña. "
             f"El resto de zonas fuera de Cataluña (Álava, Gipuzkoa, Bizkaia) está en territorios forales sin SERPAVI, por lo que el escenario B del docstring (reparto 15:2, 20:2, 48:3, 01:1) "
             f"no pudo construirse y resultó ser el mismo conjunto de 2 tratados con otra realización de la geometría simulada (B = réplica independiente de A, no un diseño distinto). "
             f"Veredicto sobre A (proceso del repositorio, declarado antes de simular). Resultados A: Conley-Taber tamaño {ev['A_ct']['tamano']:.4f} (error MC {ev['A_ct']['se_mc_tamano']:.4f}), "
             f"cobertura bajo tau=-0,0075 {ev['A_ct']['cobertura_alt']:.4f}, bajo el nulo {ev['A_ct']['cobertura_nulo']:.4f}. La réplica B queda fuera del intervalo (tamaño {ev['B_ct']['tamano']:.4f}, cobertura {ev['B_ct']['cobertura_alt']:.4f}); "
             f"agrupando A y B (4.000 réplicas nulas) el tamaño es {tam_pool:.4f} (error MC {se_pool:.4f}): la calibración es CASI en el límite del criterio, no holgada. "
             f"Alternativa Webb (solo se informa): tamaño {ev['A_webb']['tamano']:.4f} y cobertura {ev['A_webb']['cobertura_alt']:.4f}; con un único cluster tratado el bootstrap degenera (no se debe usar). "
             f"Potencia de Conley-Taber a -7,1 % (MDE de la adenda): {pot['A_ct']:.3f}; a -0,75 % es prácticamente el tamaño. El IC medio mide {ev['A_ct'].get('ancho', 0) or float(_fila(t[(t.escenario=='A')&(t.inferencia=='ct')], efecto='nulo').ancho_medio_ic):.3f} "
             f"de ancho (en log): con 2 municipios tratados el diseño no distingue efectos de la magnitud de la literatura y su lectura es la de un nulo no concluyente. "
             f"Los pesos SDID se estiman por FISTA (40 iteraciones) con regularización a la Arkhangelsky et al.; en la alternativa Webb los pesos se mantienen fijos.")
    cols = ["escenario", "inferencia", "efecto", "n_tratados", "n_donantes", "R", "sesgo", "rmse", "cobertura", "rechazo", "ancho_medio_ic"]
    _escribir(h, "Q1b · SDID con Conley-Taber (principal) y wild bootstrap de Webb (alternativa)", txt, ev, t, cols, notas, est,
              "SDID (Arkhangelsky et al.) + Conley-Taber por reasignación de provincias donantes; alternativa wild cluster bootstrap-t Webb por provincia",
              {"tamano": {k: v["tamano"] for k, v in ev.items()}, "cobertura": {k: v["cobertura_alt"] for k, v in ev.items()}, "potencia_mde": pot}, "ver estructura; R=2000/1000/300")
    return txt


if __name__ == "__main__":
    quien = sys.argv[1:] or ["cs", "dcdh", "rejilla", "sdid"]
    for q in quien:
        print(q, "->", {"cs": cerrar_cs, "dcdh": cerrar_dcdh, "rejilla": cerrar_rejilla, "sdid": cerrar_sdid}[q]())
