"""V16 · B-4 · Estabilidad del GSADF de V7.2 corregido (E1 y E2) frente al número de réplicas y a la semilla. Capa C4.

Orden del autor (2026-10-18): subir las réplicas hasta que p y recuentos sean estables en al menos 5 semillas; probar 1.999 y 4.999 y
elegir el menor estable. Se añade 499 (lo publicado en la 1.0) como referencia de la inestabilidad.
Usa las funciones de src/v5/r1b_gsadf.py (ya corregidas) sin escribir en output/v5: semilla de la serie k = SEED + 500 + k + 100.000·j,
j = 0..4 (j = 0 es la semilla original). Recuentos con las familias publicadas (BH de 8 = cocientes + tipos; 2 niveles; 34 CCAA) y la
familia de 4 cocientes como sensibilidad.
Escribe output/v16/b4_gsadf/{estabilidad.csv, recuentos.csv, resumen.json}. Uso: python3 src/v16/b4_gsadf_estabilidad.py [--np 4]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import json  # noqa: E402
import sys  # noqa: E402
from multiprocessing import Pool  # noqa: E402
from pathlib import Path  # noqa: E402

import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
import holdout  # noqa: E402
import r1b_gsadf as G  # noqa: E402

OUT = RAIZ / "output" / "v16" / "b4_gsadf"
G.REG.path = OUT / "registro_estabilidad.csv"   # el Registry del módulo de v5 se escribe al salir: aquí, no en output/v5
NBOOTS = (499, 1999, 4999)
NSEM = 5
COCIENTES = ("precio/renta", "precio/alquiler")
_SERIES: list = []


def _cargar():
    nq = holdout.load_full("nacional_q_v2", "V16-B4-estabilidad-gsadf")
    pan = pd.read_csv(RAIZ / "data/processed/panel_ccaa_q.csv")
    S, _ = G.construir_series(nq, pan)
    return [(k, terr, fam, med, s.to_numpy()) for k, (terr, fam, med, s) in enumerate(S)]


def _init(series):
    _SERIES[:] = series


def _tarea(a):
    k, nb, j = a
    _, terr, fam, med, y = _SERIES[k]
    r = G.gsadf_corr(y, nb, G.SEED + 500 + k + 100000 * j)
    return dict(k=k, territorio=terr, familia=fam, medida=med, nboot=nb, semilla=j, T=r["T"], gsadf=r["gsadf"], cv95=r["cv95"], p=r["p"], ar_p=r["ar_p"])


def recuentos(d: pd.DataFrame) -> dict:
    fu = d[d.familia == "fundamentales"].reset_index(drop=True)
    es_rat = fu.medida.str.startswith(COCIENTES).to_numpy()
    rat, tip = fu[es_rat], fu[~es_rat]
    niv, cc = d[d.familia == "referencia"], d[d.familia == "ccaa"]
    return dict(ratios_p05=int((rat.p < .05).sum()), ratios_bh_fam8=int((G.bh(fu.p.to_numpy())[es_rat] < .05).sum()),
                ratios_bh_fam4_sens=int((G.bh(rat.p.to_numpy()) < .05).sum()), tipos_p05=int((tip.p < .05).sum()),
                niveles_bh=int((G.bh(niv.p.to_numpy()) < .05).sum()), ccaa_bh=int((G.bh(cc.p.to_numpy()) < .05).sum()), ccaa_p05=int((cc.p < .05).sum()))


def main() -> int:
    npr = int(sys.argv[sys.argv.index("--np") + 1]) if "--np" in sys.argv else 4
    OUT.mkdir(parents=True, exist_ok=True)
    series = _cargar()
    tareas = [(k, nb, j) for nb in NBOOTS for j in range(NSEM) for k in range(len(series))]
    with Pool(npr, initializer=_init, initargs=(series,)) as pool:
        filas = pool.map(_tarea, tareas, chunksize=1)
    df = pd.DataFrame(filas)
    df.round(6).to_csv(OUT / "estabilidad.csv", index=False)
    rc = pd.DataFrame([dict(nboot=nb, semilla=j, **recuentos(d)) for (nb, j), d in df.groupby(["nboot", "semilla"])])
    rc.to_csv(OUT / "recuentos.csv", index=False)
    cols = [c for c in rc.columns if c not in ("nboot", "semilla")]
    estable = {int(nb): {c: bool(d[c].nunique() == 1) for c in cols} for nb, d in rc.groupby("nboot")}
    rango = {int(nb): {c: [int(d[c].min()), int(d[c].max())] for c in cols} for nb, d in rc.groupby("nboot")}
    nac = df[df.familia != "ccaa"]
    p_rango = {int(nb): {m: [round(float(x.p.min()), 4), round(float(x.p.max()), 4)] for m, x in d.groupby("medida")} for nb, d in nac.groupby("nboot")}
    # regla: el menor B (entre 1.999 y 4.999) con todos los recuentos estables salvo los que dependen de una serie con p en el borde (su p
    # medio entre semillas a ese B está a menos de 2 errores típicos de Monte Carlo de 0,05): esos no se estabilizan con ningún B finito
    borde = {}
    for nb, d in nac.groupby("nboot"):
        m = d.groupby("medida").p.mean()
        et = (0.05 * 0.95 / nb) ** 0.5
        borde[int(nb)] = sorted(m[(m - 0.05).abs() < 2 * et].index)
    elegido = None
    for nb in (1999, 4999):
        inestables = [c for c, v in estable[nb].items() if not v]
        if all(c in ("ratios_p05", "niveles_p05") for c in inestables) and (not inestables or borde[nb]):
            elegido = nb
            break
    res = dict(nboots=list(NBOOTS), semillas=NSEM, semilla_serie="SEED + 500 + k + 100000·j (j = 0: la original)", estable=estable, rango=rango,
               p_rango_nacional=p_rango, series_en_borde=borde, nboot_elegido=elegido,
               regla=("el menor B entre 1.999 y 4.999 con todos los recuentos idénticos en las 5 semillas, salvo un recuento sin ajuste cuya serie "
                      "tiene un p medio a menos de 2 errores típicos de Monte Carlo de 0,05 (ningún B finito lo estabiliza: se publica con su rango)"),
               capa="C4")
    (OUT / "resumen.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(rc.to_string())
    print(json.dumps({"elegido": elegido, "borde": borde, "estable": estable}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
