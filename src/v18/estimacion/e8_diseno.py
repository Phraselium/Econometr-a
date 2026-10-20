"""V18 · E8 (ITP) · diseño: mínimos de datos y MDE de cada especificación principal (adenda 1.3), calculados ANTES de mirar ningún coeficiente.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. MDE al 80 % de potencia, bilateral al 5 %, por Monte Carlo (R = 2.000): reasignaciones
aleatorias de los calendarios de dosis entre las 8 comunidades (la variación real: número, fechas y dosis de los cambios), con el estimador principal
(dCDH de dosis continua, ℓ = 4 trimestres o 12 meses); el valor crítico es el cuantil 95 % de |β̂| entre las reasignaciones. σ y dependencia «ya vistas»
(el propio panel de entrenamiento, como en V15 y V16: ni se usa el coeficiente observado ni se mira el resultado).
Umbral: MDE ≤ |referencia| (Anexo B: Dolls et al. −3 % por pp en el precio; Fritzsche y Vandrei −6 % por pp en el volumen).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e2_datos as D2  # noqa: E402
import e8_datos as D8  # noqa: E402
from herr18 import dcdh as DC  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
SEED = K.SEMILLA
OUT = K.RAIZ / "output" / "v18" / "estimacion" / "e8"
R_MDE = 2000

ESPEC = {
    "E8-R1": {"ref": 0.03, "delta": 0.015, "umbral": 0.03, "ell": 4, "frec": "T", "fuente_ref": "Dolls et al. (versión publicada): −3 % por pp en el precio"},
    "E8-R2": {"ref": 0.06, "delta": 0.03, "umbral": 0.06, "ell": 12, "frec": "M", "fuente_ref": "Fritzsche y Vandrei: −6 % por pp en el volumen"},
    "E8-A1": {"ref": None, "delta": 0.05, "umbral": 0.10, "ell": None, "frec": "A", "fuente_ref": "sin referencia: 2δ"},
    "E8-A2": {"ref": 0.06, "delta": 0.03, "umbral": 0.06, "ell": 4, "frec": "T", "fuente_ref": "Fritzsche y Vandrei: −6 % por pp en el volumen"},
}


def placebos_dcdh(Y: np.ndarray, Dc: np.ndarray, cl_idx: np.ndarray, ell: int, R: int, rng: np.random.Generator) -> np.ndarray:
    """β̂ de dCDH (ℓ) bajo R reasignaciones de los calendarios de dosis entre las comunidades (se incluye solo lo finito)."""
    G = Dc.shape[0]
    out = []
    for b0 in range(0, R, 100):
        b = min(100, R - b0)
        perms = DC.permutaciones(rng, G, b)
        Dp = Dc[perms][:, cl_idx, :]
        out.append(DC.estimar(Y[None], Dp, ell)["beta"])
    return np.concatenate(out)


def panel_a2(provs: dict[str, str]) -> dict:
    """Compraventas municipales trimestrales (MIVAU) de los municipios grandes de las 8 comunidades, 2007T1-2024T4, con código INE por nombre."""
    t = D2.mivau_municipal("mivau_transacciones_municipios.csv", "trans_total")
    per = K.trimestres("2007T1", "2024T4")
    w = K.ancho(t, per).dropna()
    w = w[(w > 0).all(axis=1)]
    w = w[w.index.str[:2].isin(provs)]
    cods = list(w.index)
    return {"cod": np.array(cods), "Y": np.log(w.values), "cols": per, "ccaa": np.array([provs[c[:2]] for c in cods])}


def fila(id_, n_u, n_cl, T, minimo, mde, extra="") -> dict:
    e = ESPEC[id_]
    ok_mde = mde is not None and mde["mde80"] <= e["umbral"]
    est = bool(minimo["ok"] and ok_mde)
    mot = []
    if not minimo["ok"]:
        mot.append(minimo["texto"])
    if mde is not None and not ok_mde:
        mot.append(f"MDE80 = {mde['mde80']:.4f} por punto > umbral {e['umbral']:.4f}")
    if extra:
        mot.append(extra)
    return {"id": id_, "n_unidades": n_u, "n_comunidades": n_cl, "T": T, "minimo_datos": minimo["texto"], "minimo_ok": minimo["ok"],
            "mde80": None if mde is None else mde["mde80"], "sd_placebo": None if mde is None else mde["sd_placebo"],
            "tamano_nominal_placebo": None if mde is None else mde["tamano_nominal"], "R": None if mde is None else mde["R"],
            "umbral": e["umbral"], "referencia": e["fuente_ref"], "estimable": est, "motivo_no_estimable": "; ".join(mot) if not est else ""}


def estimabilidad() -> tuple[pd.DataFrame, dict]:
    rng = np.random.default_rng(SEED)
    provs = D8.provincias_e8()
    ev = D8.eventos("exacta")
    filas, paneles = [], {}
    # E8-R1: valor tasado trimestral (30 provincias con serie)
    v = D8.panel_valor_tasado(provs)
    cc = sorted(set(v["ccaa"]))
    cl = np.array([cc.index(c) for c in v["ccaa"]])
    n_ev, n_cc = D8.n_cambios_efectivos(ev, v["cols"], "T", 4, cc)
    Dc, _ = D8.calendarios(ev, v["cols"], "T", cc)
    mn = {"ok": n_ev >= 8 and n_cc >= 4, "texto": f"{n_ev} cambios efectivos del tipo general en {n_cc} comunidades (mínimo 8 en 4); {len(v['cod'])} provincias con valor tasado"}
    paneles["E8-R1"] = {"panel": v, "Dc": Dc, "cl": cl, "ccaa": cc}
    mde = K.mde_desde_placebos(placebos_dcdh(v["Y"], Dc, cl, 4, R_MDE, rng)) if mn["ok"] else None
    filas.append(fila("E8-R1", len(v["cod"]), len(set(cl)), len(v["cols"]), mn, mde))
    # E8-R2: compraventas mensuales (usada)
    c = D8.panel_compraventas(provs, "usada")
    cc2 = sorted(set(c["ccaa"]))
    cl2 = np.array([cc2.index(x) for x in c["ccaa"]])
    n_ev2, n_cc2 = D8.n_cambios_efectivos(ev, c["cols"], "M", 12, cc2)
    Dc2, _ = D8.calendarios(ev, c["cols"], "M", cc2)
    mn2 = {"ok": n_ev2 >= 8 and n_cc2 >= 4, "texto": f"{n_ev2} cambios efectivos del tipo general en {n_cc2} comunidades (mínimo 8 en 4); {len(c['cod'])} provincias"}
    paneles["E8-R2"] = {"panel": c, "Dc": Dc2, "cl": cl2, "ccaa": cc2}
    mde2 = K.mde_desde_placebos(placebos_dcdh(c["Y"], Dc2, cl2, 12, R_MDE, rng)) if mn2["ok"] else None
    filas.append(fila("E8-R2", len(c["cod"]), len(set(cl2)), len(c["cols"]), mn2, mde2))
    # E8-A1: recaudación del ITP
    filas.append(fila("E8-A1", 0, 0, 0, {"ok": False, "texto": "la recaudación del ITP por comunidad (liquidación de tributos cedidos, Hacienda) no está en el repositorio: fuente `itp_recaudacion_ccaa` posterior a la etiqueta, sin descargar"}, None))
    # E8-A2: municipios grandes
    a2 = panel_a2(provs)
    cc3 = sorted(set(a2["ccaa"]))
    cl3 = np.array([cc3.index(x) for x in a2["ccaa"]])
    Dc3, _ = D8.calendarios(ev, a2["cols"], "T", cc3)
    n_ev3, n_cc3 = D8.n_cambios_efectivos(ev, a2["cols"], "T", 4, cc3)
    mn3 = {"ok": n_ev3 >= 8 and n_cc3 >= 4 and len(a2["cod"]) >= 30, "texto": f"{n_ev3} cambios efectivos en {n_cc3} comunidades; {len(a2['cod'])} municipios grandes con compraventas trimestrales (código INE por nombre)"}
    paneles["E8-A2"] = {"panel": a2, "Dc": Dc3, "cl": cl3, "ccaa": cc3}
    mde3 = K.mde_desde_placebos(placebos_dcdh(a2["Y"], Dc3, cl3, 4, R_MDE, rng)) if mn3["ok"] else None
    filas.append(fila("E8-A2", len(a2["cod"]), len(set(cl3)), len(a2["cols"]), mn3, mde3))
    return pd.DataFrame(filas), paneles


if __name__ == "__main__":
    est, _ = estimabilidad()
    with pd.option_context("display.width", 250, "display.max_columns", 30, "display.max_colwidth", 140):
        print(est.to_string())
