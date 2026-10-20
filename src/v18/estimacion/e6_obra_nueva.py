"""V18 · fase 4 · E6 · obra nueva y alquileres cercanos: orquestación (estimabilidad → estimación → pruebas → clasificación → salidas).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (plan_replicacion.md §1.6 + adenda 1.3, anexos A-C). Orden fijado por la adenda 1.3: mínimos de datos y MDE por Monte Carlo se
calculan y se registran ANTES de estimar ningún coeficiente; lo que no los supera queda «NO ESTIMABLE» y no se estima. Determinista (SEED 20261010). Sin red.

- E6-R1 (piloto, provincia de València): pilas por cohorte de terminación 2015-2018, secciones contiguas sin la propia, controles terminados en T+6 o después.
- E6-A1 (50 viviendas, anillo de 250 m), E6-R1-v1..v6: recuentos del diseño, sin resultado.
- E6-R2 / E6-A3 (Mense): NO ESTIMABLES sin la lluvia de AEMET (X1); E6-A2 sin la descarga masiva del Catastro.

Uso: python3 src/v18/estimacion/e6_obra_nueva.py     (ensayo de código con resultado sintético: V18_E6_ENSAYO=<directorio>)
Salidas: output/v18/estimacion/e6/{mde.csv, registro.csv, tabla.csv, resultado.json, hechos.json, informe.md}
Lecturas: solo con sellado.filtrar + holdout.excluir_sellados_v6 (e1_datos, e6_datos). Nunca data/sealed.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e1_datos as D  # noqa: E402
import e1_nucleo as N  # noqa: E402
import e6_diseno as G  # noqa: E402
import e6_estim as E  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
OUT = K.RAIZ / "output" / "v18" / "estimacion" / "e6"
SEMILLA = K.SEMILLA
VARIANTES_R1 = [("v1", "M", "SERPAVI de vivienda unifamiliar", {"tip": "VU"}), ("v2", "E", "fecha de evento = terminación − 2", {"resta": 2}), ("v3", "U", "sin València ciudad", {"sin_valencia": True}),
                ("v4", "U", "con la sección propia", {"propia": True}), ("v5", "C", "cerca frente a lejos (contiguas de segundo orden)", {"segundo_orden": True}), ("v6", "U", "umbral de 10 viviendas", {"umbral": 10})]
VARIANTES_R2 = [("v1", "U", "sin 2019 ni 2024 en València (DANA)"), ("v2", "M", "IPC de alquiler trimestral"), ("v3", "U", "sin Barcelona"), ("v4", "M", "lluvia de agosto-septiembre")]
FORMULAS = {
    "E6-R1": "ln SERPAVI_ja = Σ_k γ_k·Tr_j·1[k] + β·Tr_j·1[0<=k<=3] + α_(j,pila) + δ_(año,pila) + θ_(mun,año,pila) + ε (secciones contiguas sin la propia; edificios >= 20 viviendas; cohortes 2015-2018; cluster sección del edificio)",
    "E6-R2": "IV: ln alquiler_pt = β·(T^Q4_{p,t-1}/media T_p) + α_p + γ_t + ε; Z = duración de las rachas de lluvia de julio a septiembre en t−1 (AEMET), 2011-2024",
    "E6-A1": "E6-R1 con umbral de 50 viviendas y anillo de 250 m",
    "E6-A2": "E6-R1 en el resto de España",
    "E6-A3": "E6-R2 con el IPC de alquiler 2002-2025",
}


def main() -> int:
    t0 = time.time()
    ensayo = os.environ.get("V18_E6_ENSAYO")
    out_dir = Path(ensayo) if ensayo else OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEMILLA)
    B = G.base()
    secs = B["secs"]
    print(f"[{time.time() - t0:5.0f}s] base: {secs.attrs['n_tras_sellado']} de {secs.attrs['n_total']} secciones de la provincia, {len(B['edif'])} edificios cualificados de cualquier tamaño", flush=True)
    if ensayo:                                  # ensayo de código: resultado sintético (ruido), fuera del repositorio
        for t in B["sp"]:
            B["sp"][t] = B["sp"][t] * np.exp(rng.normal(size=B["sp"][t].shape))
    assert not D.sellado.mascara_v15_v16(pd.Series(list(B["ok"])), "seccion").any()
    reg = K.Registry(out_dir / "registro.csv")
    for ident, form in FORMULAS.items():
        reg.log("v18-E6-prereg", ident, form, "", "", 0, np.nan, np.nan, np.nan, notas="principal o ampliación; registrada antes de estimar (estimabilidad calculada sin coeficientes)")
    for suf, dim, desc, _ in VARIANTES_R1:
        reg.log("v18-E6-prereg", f"E6-R1-{suf}", f"variante [{dim}] {desc}", "", "", 0, np.nan, np.nan, np.nan, notas="variante enumerada (adenda, anexo A)")
    for suf, dim, desc in VARIANTES_R2:
        reg.log("v18-E6-prereg", f"E6-R2-{suf}", f"variante [{dim}] {desc}", "", "", 0, np.nan, np.nan, np.nan, notas="variante enumerada (adenda, anexo A)")
    reg.flush()

    # ------------------------------------------------------------------ recuentos del diseño (sin resultado) y estimabilidad de E6-R1
    c1 = G.construir(B)
    d1 = E.preparar(c1["datos"], secs)
    n_tr = int(d1[d1.tr == 1].cod_seccion.nunique())
    n_co = int(d1[d1.tr == 0].cod_seccion.nunique())
    minimo = n_tr >= 30 and n_co >= 30
    mde = E.mde(d1, secs, B["sp"]["VC"], R=2000)
    mde_10k = E.mde(d1, secs, B["sp"]["VC"], R=10000)
    umbral = abs(E.REF_R1)
    ok = bool(minimo and np.isfinite(mde["mde80"]) and mde["mde80"] <= umbral)
    dec = ("estimable" if ok else (f"NO ESTIMABLE por datos: {n_tr} tratadas y {n_co} de control (mínimo 30 y 30)" if not minimo else
                                   f"NO ESTIMABLE por variación: MDE80 {mde['mde80']:.4f} > umbral {umbral:.3f}"))
    reg.log("v18-E6-estimabilidad", "E6-R1", FORMULAS["E6-R1"], "", "", int(len(d1)), np.nan, np.nan, np.nan, notas=f"MDE80 {mde['mde80']}; umbral {umbral}; {dec}; registrada antes de estimar")
    print(f"[{time.time() - t0:5.0f}s] E6-R1: {n_tr} tratadas, {n_co} controles, G = {mde['G']}, MDE80 {mde['mde80']:.4f} (R = 10.000: {mde_10k['mde80']:.4f}); {dec}", flush=True)
    cuentas = {"E6-R1": c1}
    for suf, dim, desc, kw in VARIANTES_R1:
        cuentas[f"E6-R1-{suf}"] = G.construir(B, **kw)
    cuentas["E6-A1"] = G.construir(B, umbral=50, modo="anillo")
    reg.flush()

    # ------------------------------------------------------------------ estimación (solo si supera la estimabilidad)
    est = None
    if ok:
        est = estimar_r1(d1, secs, rng, B, reg)
    else:
        no_est = {"E6-R1": dec, "E6-A1": "NO ESTIMABLE por datos: menos de 30 secciones tratadas", "E6-A2": "NO ESTIMABLE (datos): descarga masiva del Catastro", "E6-R2": "NO ESTIMABLE (X1): sin lluvia de AEMET",
                  "E6-A3": "NO ESTIMABLE (X1): sin lluvia de AEMET"}
        no_est |= {f"E6-R1-{s}": "no estimada (principal NO ESTIMABLE)" for s, _, _, _ in VARIANTES_R1} | {f"E6-R2-{s}": "no estimada (E6-R2 NO ESTIMABLE)" for s, _, _ in VARIANTES_R2}
        for k, v in no_est.items():
            reg.log("v18-E6-no-estimada", k, FORMULAS.get(k, k), "", "", 0, np.nan, np.nan, np.nan, notas=v)
    import e6_salidas as S
    S.escribir(out_dir, B, secs, c1, d1, cuentas, {"n_tr": n_tr, "n_co": n_co, "minimo": minimo, "mde": mde, "mde_10k": mde_10k, "umbral": umbral, "ok": ok, "decision": dec}, est, time.time() - t0)
    reg.flush()
    print(f"[{time.time() - t0:5.0f}s] salidas escritas en {out_dir}", flush=True)
    return 0


def estimar_r1(d1: pd.DataFrame, secs: pd.DataFrame, rng, B: dict, reg) -> dict:
    """Solo si E6-R1 supera la estimabilidad: coeficiente medio de k = 0..3 con CR1 t(G−1) y Webb 9.999, Conley, estudio de eventos, placebo de fecha, Honest DiD y variantes."""
    r = E.estimar(d1, webb_B=9999, rng=rng, conley=True)
    ev = E.evento(d1)
    pf = E.placebo_fecha(d1)
    out = {"r": r, "ev": ev, "placebo_fecha": pf, "variantes": {}}
    for suf, dim, desc, kw in VARIANTES_R1:
        c = G.construir(B, **kw)
        if len(c["datos"]) and c["datos"].tr.sum() > 0 and (c["datos"].tr == 0).any():
            dv = E.preparar(c["datos"], secs)
            try:
                out["variantes"][suf] = E.estimar(dv)
            except Exception as e:  # noqa: BLE001
                out["variantes"][suf] = {"error": str(e)[:80]}
    da = E.sin_atipicos(d1)
    out["sin_atipicos"] = E.estimar(E.preparar(da.drop(columns=[c for c in da.columns if c.startswith("lead") or c in ("u", "t", "cl", "Dpost", "x", "y_c")]), secs))
    return out


if __name__ == "__main__":
    sys.exit(main())
