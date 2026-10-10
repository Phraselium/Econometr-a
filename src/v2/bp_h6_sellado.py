"""H6 (zonas tensionadas en Cataluña, 2024). NO SE EJECUTA desde la rama BP. El orquestador la llama UNA vez:
    holdout.evaluate("H6", bp_h6_sellado.evaluar_H6, "BP", ["panel_prov_q"])

DISEÑO FIJADO ANTES DE LA LLAMADA (fiel a docs/v2/hipotesis.md, H6)
* Resultado: ln IPC de alquiler provincial (principal); Δ4 ln (secundario, no decide).
* Tratadas: 08, 17, 25, 43 (agregado: media simple de las 4). Tratamiento: zonas tensionadas (140 municipios
  desde 2024-03-16; 131 más desde 2024-10-10).
* Donantes: provincias de ENTRENAMIENTO (49) menos las 4 catalanas y menos 01, 20, 48, 31, 15 (zona tensionada
  declarada hasta 2026Q2) => 40. Las selladas 11, 16, 45 no son donantes (no están en `train`). Un donante con
  algún NaN en las ventanas usadas se descarta (se informa); se aborta si quedan < 30 o si falta algún dato de las
  tratadas o algún trimestre de la ventana de efecto.
* Estimador principal: Synthetic DiD propio (bp_lib.sdid). Los pesos ω y λ se ajustan SOLO con datos <= 2023Q4.
  Tratamiento de 2024Q1-Q2 (dentro de entrenamiento, ya con 140 municipios tratados desde el 16-mar-2024): EXCLUIDOS
  del pre-periodo y del post-periodo (opción conservadora). El tope catalán (Ley 11/2020, 2020Q4-2022Q1) contamina
  la serie de las tratadas: también se excluye del pre-periodo para el nivel. Pre-periodo del nivel: 2016Q1-2020Q3 y
  2022Q2-2023Q4 (26 trimestres). Pre-periodo de Δ4 (secundario): 2016Q1-2020Q3 y 2023Q2-2023Q4 (los Δ4 de
  2020Q4-2023Q1 incluyen en su ventana trimestres del tope).
* Efecto: media en 2024Q3-2026Q2 (8 trimestres).
* Inferencia: permutación espacial con B=1000 subconjuntos de 4 donantes (semilla 20261010) re-estimando todo;
  p bilateral = (1+#{|τ_b| >= |τ|})/(B+1) (la una cola, solo informativa).
* REGLA DE DECISIÓN (confirmatoria): H6 se CONFIRMA si τ_SDiD(ln IPC alquiler) < 0 Y p_permutación_bilateral < 0,05.
  Entra después en el Holm de las 7 confirmatorias (lo aplica el orquestador).
* DECLARACIÓN EX ANTE DE POTENCIA Y LECTURA (antes de abrir): efecto mínimo detectable (80 %, bilateral) ≈ 2,8 x DE
  placebo ≈ 1,7 % en ln IPC de alquiler (H6; output/v2/BP/h6_preparacion.json) y ≈ 0,56 % en H5 (2,8 x 0,0020).
  El IPC de alquiler del INE mide las rentas de TODOS los contratos vigentes (el parque), mientras que la regulación
  actúa sobre todo en contratos nuevos y solo en los municipios declarados (referencia de magnitud en contratos nuevos:
  Jofre-Monseny, Martínez-Mazza y Segú 2023, Regional Science and Urban Economics 101, 103916, rentas de contratos
  nuevos de orden 4-6 % en municipios regulados, según el resumen publicado; cuartil no verificado). Un no rechazo de H6
  se leerá como "no detectable en el IPC provincial", NO como "sin efecto".
* RIESGOS DECLARADOS ex ante: (a) anticipación: la Resolución TER/2940/2023 (agosto de 2023) precede a 2024 y λ
  probablemente se concentre en 2023Q4, de modo que un efecto anticipado en 2023Q3-Q4 sesga τ hacia 0; (b) paquete
  catalán: DL 3/2023 de viviendas de uso turístico (en vigor 2023-11-09) y 2.ª ronda (efecto 2024-10-10) entran en el
  mismo contraste: H6 mide "Cataluña 2024-2026", no la zona tensionada aislada; (c) el pre 2022Q2-2023Q4 incluye
  contratos firmados bajo el tope que siguen en el parque; (d) choques nacionales (tope del 3 % en 2024, IRAV desde 2025)
  se absorben solo si su incidencia no difiere entre Cataluña y los donantes; (e) la inferencia placebo supone unidades
  intercambiables (la media de 4 provincias con Barcelona puede ser menos ruidosa que 4 donantes al azar: prueba
  conservadora); (f) zona_tensionada_share usa pesos catastrales del año de stock más cercano, que puede ser sellado
  (solo afecta al secundario ponderado). Secundario informativo fijado ahora: SDiD sin 2023Q3-Q4 en el pre.
* GUARDA: aborta antes de calcular nada si algún |Δln| entre 2024Q2 y 2024Q3 supera 0,05 (cambio de base).
* Orden de cálculo: PRINCIPAL y DECISION se fijan primero; cada secundario va en try/except (el error queda como texto).
* Ejecutar con OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 y timeout amplio (~1 min esperado): si se corta, H6 queda quemada.
* Secundarios (informativos, no deciden): SC de Abadie y DiD; Δ4; agregado ponderado por zona_tensionada_share de
  2024Q2 (del entrenamiento); cada tratada sola con permutación exacta sobre los donantes.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bp_lib as bl  # noqa: E402

SEED = 20261010
UMBRAL_SALTO = 0.05   # guarda de base: |Δln IPC| máximo admitido entre 2024Q2 y 2024Q3 (fijado antes de abrir)


def qrange(a, b):
    ya, qa = int(a[:4]), int(a[-1])
    yb, qb = int(b[:4]), int(b[-1])
    out, y, q = [], ya, qa
    while (y, q) <= (yb, qb):
        out.append(f"{y}Q{q}")
        y, q = (y, q + 1) if q < 4 else (y + 1, 1)
    return out


CFG_REAL = dict(
    tratadas=["08", "17", "25", "43"],
    no_donantes=["01", "20", "48", "31", "15"],
    q_ini="2015Q1",                                          # 2015Q1 solo para calcular Δ4 desde 2016Q1
    pre_nivel=qrange("2016Q1", "2020Q3") + qrange("2022Q2", "2023Q4"),
    pre_d4=qrange("2016Q1", "2020Q3") + qrange("2023Q2", "2023Q4"),
    post=qrange("2024Q3", "2026Q2"),
    B=1000, min_donantes=30, share_col="zona_tensionada_share", share_q="2024Q2")


def _wide(pan_all, cfg):
    q_all = qrange(cfg["q_ini"], cfg["post"][-1])
    w = pan_all.pivot(index="cod_prov", columns="trimestre", values="ipc_alquiler")
    w = w.reindex(columns=q_all)
    return np.log(w), q_all


def _evaluar(sellado, train, cfg):
    pt, ps = train["panel_prov_q"].copy(), sellado["panel_prov_q"].copy()
    for d in (pt, ps):
        d["cod_prov"] = d["cod_prov"].astype(str)
        d["trimestre"] = d["trimestre"].astype(str)
    pan_all = pd.concat([pt, ps]).drop_duplicates(["cod_prov", "trimestre"]).sort_values(["cod_prov", "trimestre"])
    units_train = sorted(pt["cod_prov"].unique())
    trat = list(cfg["tratadas"])
    if not set(trat) <= set(units_train):
        raise RuntimeError("abortado: tratadas ausentes del entrenamiento")
    donantes = [u for u in units_train if u not in trat and u not in cfg["no_donantes"]]
    niv, q_all = _wide(pan_all, cfg)
    # GUARDA DE BASE (umbral fijado antes de abrir): un salto |Δln| > 0,05 entre el último trimestre de entrenamiento y el
    # primero de la ventana en cualquier provincia indica niveles en bases distintas (el crecimiento trimestral normal es ~1 %).
    q_last, q_first = max(pt["trimestre"]), cfg["post"][0]
    salto = (niv[q_first] - niv[q_last]).abs()
    if (salto > UMBRAL_SALTO).any() or salto.isna().all():
        raise RuntimeError(f"abortado: salto de nivel anómalo {q_last}->{q_first} (máx {salto.max():.3f} > {UMBRAL_SALTO}); "
                           "posible cambio de base entre entrenamiento y sellado")
    d4 = niv - niv.shift(4, axis=1)
    pos = {q: i for i, q in enumerate(q_all)}
    pre_n, pre_4, post = cfg["pre_nivel"], cfg["pre_d4"], cfg["post"]
    cols_n = sorted(set(pre_n) | set(post))
    cols_4 = sorted(set(pre_4) | set(post))
    if niv.loc[trat, cols_n].isna().any().any() or d4.loc[trat, cols_4].isna().any().any():
        raise RuntimeError("abortado: faltan datos de las tratadas en las ventanas")
    ok = [u for u in donantes if not (niv.loc[u, cols_n].isna().any() or d4.loc[u, cols_4].isna().any())]
    descartados = sorted(set(donantes) - set(ok))
    if len(ok) < cfg["min_donantes"]:
        raise RuntimeError(f"abortado: solo {len(ok)} donantes completos")
    units = trat + ok
    k = len(trat)
    tr_idx, co_idx = np.arange(k), np.arange(k, len(units))
    subsets = bl.draws_subsets(len(co_idx), k, cfg["B"])
    subsets1 = bl.draws_subsets(len(co_idx), 1, len(co_idx))
    res = dict(regla="H6 se confirma si tau_SDiD(ln IPC alquiler) < 0 y p de permutación bilateral < 0,05",
               tratadas=trat, n_donantes=len(ok), donantes=ok, donantes_descartados_por_NaN=descartados,
               pre_nivel=[pre_n[0], pre_n[-1], len(pre_n)], post=[post[0], post[-1], len(post)], B=len(subsets))

    def resumen(r):
        return {m: dict(tau=float(v["tau"]), se_placebo=float(v["se_placebo"]),
                        ic95=[float(v["ic95"][0]), float(v["ic95"][1])], p_perm_bilateral=float(v["p_dos"]),
                        p_perm_una_cola=float(v["p_una"]), B=int(v["B"])) for m, v in r.items()}
    Yn, Y4 = niv.loc[units].values, d4.loc[units].values
    pn, p4, po = [pos[q] for q in pre_n], [pos[q] for q in pre_4], [pos[q] for q in post]
    prin = bl.run_design(Yn, tr_idx, co_idx, pn, po, subsets)
    res["PRINCIPAL_ln_ipc_alquiler"] = resumen(prin)
    s = prin["sdid"]
    om = s["omega"]
    res["PRINCIPAL_ln_ipc_alquiler"]["sdid"]["peso_max_donante"] = float(om.max())
    res["PRINCIPAL_ln_ipc_alquiler"]["sdid"]["n_donantes_peso_gt_1pct"] = int((om > 0.01).sum())
    gap = s["gap"]
    res["PRINCIPAL_ln_ipc_alquiler"]["sdid"]["rmse_brecha_pre"] = float(np.sqrt(np.mean((gap[pn] - s["lam"] @ gap[pn]) ** 2)))
    tau, p = res["PRINCIPAL_ln_ipc_alquiler"]["sdid"]["tau"], res["PRINCIPAL_ln_ipc_alquiler"]["sdid"]["p_perm_bilateral"]
    res["DECISION"] = dict(tau=tau, p_perm_bilateral=p, cumple_regla=bool(tau < 0 and p < 0.05))
    def sec(nombre, fn):
        try:
            res[nombre] = fn()
        except Exception as e:  # noqa: BLE001  (un secundario no puede impedir devolver la decisión)
            res[nombre] = f"error: {type(e).__name__}: {e}"

    sec("sec_delta4", lambda: resumen(bl.run_design(Y4, tr_idx, co_idx, p4, po, subsets, metodos=("sdid", "sc", "did"))))

    def _pond():
        sh = pt[pt["trimestre"] == cfg["share_q"]].set_index("cod_prov")[cfg["share_col"]].reindex(trat)
        if sh.notna().all() and (sh > 0).all():
            return dict(pesos=[float(x) for x in sh.values],
                        **resumen(bl.run_design(Yn, tr_idx, co_idx, pn, po, subsets, w_tr=sh.values, metodos=("sdid",))))
        return "no disponible (share ausente en el entrenamiento)"
    sec("sec_ponderado_share", _pond)

    def _solas():
        uno = {}
        for i, u in enumerate(trat):
            r = bl.run_design(Yn, [i], co_idx, pn, po, subsets1, metodos=("sdid",))["sdid"]
            uno[u] = dict(tau=float(r["tau"]), p_perm_bilateral=float(r["p_dos"]), n_placebos=int(r["B"]))
        return uno
    sec("sec_tratadas_solas", _solas)

    def _sin2023():
        pn2 = [pos[q] for q in pre_n if q not in ("2023Q3", "2023Q4")]
        return resumen(bl.run_design(Yn, tr_idx, co_idx, pn2, po, subsets, metodos=("sdid",)))
    sec("sec_sin_2023Q3_Q4_en_pre", _sin2023)
    res["optimizador_no_convergidos"] = int(bl.NO_CONV[0])
    return res


def evaluar_H6(sellado: dict, train: dict) -> dict:
    """Función para holdout.evaluate("H6", ...). Parámetros fijos del diseño (ver docstring del módulo)."""
    return _evaluar(sellado, train, CFG_REAL)


def preparar_entrenamiento(pan, B=1000, smoke=False):
    """Preparación con SOLO datos de entrenamiento (<= 2023Q4): donantes, pesos, ajuste previo y potencia
    (SD del efecto placebo en una ventana pseudo-post 2022Q3-2023Q4 con 4 donantes ficticios tratados)."""
    cfg = dict(CFG_REAL)
    pan = pan.copy()
    pan["cod_prov"] = pan["cod_prov"].astype(str)
    pan["trimestre"] = pan["trimestre"].astype(str)
    q_all = qrange(cfg["q_ini"], "2023Q4")
    niv = np.log(pan.pivot(index="cod_prov", columns="trimestre", values="ipc_alquiler").reindex(columns=q_all))
    units_train = sorted(niv.index)
    trat = cfg["tratadas"]
    donantes = [u for u in units_train if u not in trat and u not in cfg["no_donantes"]]
    if smoke:
        donantes = sorted(np.random.default_rng(SEED).choice(donantes, 10, replace=False).tolist())
    pos = {q: i for i, q in enumerate(q_all)}
    units = trat + donantes
    Yn = niv.loc[units].values
    tr_idx, co_idx = np.arange(4), np.arange(4, len(units))
    pn = [pos[q] for q in cfg["pre_nivel"]]
    # SDiD de prueba: pre = primeros trimestres del pre-periodo, pseudo-post = sus últimos 8 (sin datos de efecto)
    om_fit = bl.sdid(Yn[co_idx], Yn[tr_idx].mean(0), pn[:-8], pn[-8:], n_tr=4)
    gap = om_fit["gap"]
    # potencia: placebo con pseudo-post 2022Q3-2023Q4 (pre 2016Q1-2020Q3), tratadas ficticias entre los donantes
    pre_p = [pos[q] for q in qrange("2016Q1", "2020Q3")]
    post_p = [pos[q] for q in qrange("2022Q3", "2023Q4")]
    sub = bl.draws_subsets(len(co_idx), 4, B)
    taus = []
    for s in sub:
        s = np.asarray(s)
        rest = np.setdiff1d(np.arange(len(co_idx)), s)
        taus.append(bl.sdid(Yn[co_idx[rest]], Yn[co_idx[s]].mean(0), pre_p, post_p, n_tr=4)["tau"])
    sd_p = float(np.std(taus, ddof=1))
    return dict(
        nota="Preparación con datos <= 2023Q4. No se estima ningún efecto de H6.",
        n_donantes=len(donantes), donantes=donantes, excluidos_ex_ante=cfg["no_donantes"],
        pre_nivel=[cfg["pre_nivel"][0], cfg["pre_nivel"][-1], len(cfg["pre_nivel"])],
        excluidos_del_ajuste="2020Q4-2022Q1 (tope catalán) y 2024Q1-2024Q2 (140 municipios tratados desde 2024-03-16)",
        ajuste_prueba_pesos=dict(pre_ajuste=len(pn) - 8, rmse_brecha_centrada=float(np.sqrt(np.mean(
            (gap[pn[:-8]] - gap[pn[:-8]].mean()) ** 2))), peso_max=float(om_fit["omega"].max()),
            n_pesos_gt_1pct=int((om_fit["omega"] > 0.01).sum())),
        potencia=dict(ventana_pseudo_post="2022Q3-2023Q4", sd_efecto_placebo=sd_p,
                      mde_aprox_80pct_dos_colas=2.8 * sd_p, B=len(sub),
                      lectura="orden de magnitud del efecto mínimo detectable (en ln IPC de alquiler) con ventana post de 6 trimestres; la real tiene 8"))


if __name__ == "__main__":
    raise SystemExit("solo vía holdout.evaluate('H6', evaluar_H6, 'BP', ['panel_prov_q'])")
