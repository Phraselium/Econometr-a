"""V16 · B-4 (2b) · Banda exacta, mediana y sensibilidad al tipo del BdE de V8-QNA-pp-c-P5 (cuota no atribuida, compra, P5). Capa C3s.

Orden del autor (2026-10-18): publicar la banda exacta en lugar de la aproximada (suma de los límites de las dos bandas del 68 %), añadir
la mediana junto a la media, con la nota de cola pesada y la sensibilidad al tipo hipotecario del Banco de España.
Reproduce el posterior de M2 V3 con las funciones de src/v8/m2_svar.py y su configuración original (objetivo 500, M 3.000, D0 300,
Dmax 40.000, clave 10), sin escribir en output/v8. Cuota no atribuida en pp = determinista + no_identificados (desviaciones V8 l.42(3));
media y cuantiles 16/50/84 ponderados por los pesos ARW del posterior. Sensibilidad: la misma especificación con i = tipo_hip_bde.
Escribe output/v16/b4_v8/qna_c_p5.json, que lee src/v8/f6_hechos.py. Sin red. Uso: python3 src/v16/b4_qna_exacta.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
import m2_svar as M  # noqa: E402

OUT = RAIZ / "output" / "v16" / "b4_v8"


def _cuantiles(x, w, qs):
    i = np.argsort(x)
    cw = np.cumsum(w[i]) / w.sum()
    return [float(x[i][np.searchsorted(cw, q)]) for q in qs]


def _posterior():
    d = M.cargar()
    o = M.procesar(M.construir("V3", d), 500, 3000, 300, 40000, 10, False, None)
    hd = o["hdraw"][("compra", "P5")]
    w = np.asarray(o["res"]["peso"], dtype=float)
    s = np.asarray(hd["comp"]["determinista"] + hd["comp"]["no_identificados"], dtype=float)
    q16, q50, q84 = _cuantiles(s, w, (.16, .5, .84))
    return dict(media=float((w * s).sum() / w.sum()), mediana=q50, banda68_exacta=[q16, q84], n_sorteos=int(len(w)),
                ess=float(w.sum() ** 2 / (w ** 2).sum()), delta_y_pp=float(hd["total"]))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    base = _posterior()
    sb = M.series_base

    def sb_bde(d, defl="ipc_general"):
        S = sb(d, defl)
        S["i"] = d["tipo_hip_bde"]
        return S

    M.series_base = sb_bde
    bde = _posterior()
    M.series_base = sb
    res = dict(id="V8-QNA-pp-c-P5", capa="C3s", principal_tipo_bce=base, sensibilidad_tipo_bde=bde,
               nota=("Media posterior con cola derecha pesada: la mediana es mucho menor que la media. La banda exacta son los cuantiles 16 y 84 "
                     "ponderados de la suma; la publicada en la 1.0 era la suma de los límites de las dos bandas (aproximada y más ancha). "
                     "Con el tipo hipotecario del Banco de España en lugar del BCE, la media cambia mucho; la mediana mucho menos."))
    (OUT / "qna_c_p5.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
