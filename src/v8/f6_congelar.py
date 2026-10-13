#!/usr/bin/env python3
"""V8-F6: congelacion de predicciones (hipotesis.md §10). Capa C4 (prediccion no es causalidad).

Predicciones nacionales del crecimiento trimestral REAL (log x100, deflactado con IPC general) del precio de compra (valor tasado MIVAU)
y del alquiler (IPC alquiler), h=1..4 desde 2026T2 (2026T3-2027T2), de:
  - ar4: AR(4) con constante; ar_fc: AR(4) + 2 retardos del HPI zona euro (dhpi); ecm_v1: especificacion A de v7 (m_ecm_v1 + _ec_forecast
    importadas como en f5_atribucion.py), regresores futuros dX = 0; estimados con TODOS los datos hasta 2026T2 (muestra desde 2007T1, como F5).
  - bvar_m2: BVAR principal, ya congelado en output/v8/M2/predicciones_congeladas.csv (NO se recalcula: se referencia con su sha256;
    origen 2026T1, filas evaluable=True = h 1..4 desde 2026T2).
Es el mejor (y unico) modelo de cada familia de output/v8/F5/fuera_muestra_comun.csv. Bandas de ar4/ar_fc: simulacion gaussiana con la
varianza residual MCO (sin incertidumbre de parametros); ecm_v1 sin bandas. Para ar_fc, el dhpi futuro se proyecta con un AR(4) propio.
Uso: python3 src/v8/f6_congelar.py [--recongelar]
  Si ya existe congelacion.json y el sha conjunto recalculado difiere, sale con error salvo --recongelar. notas_release.md no se reescribe si ya
  tiene un sha distinto de PENDIENTE.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
SEED = 20261010
OUT = RAIZ / "output" / "v8" / "congelacion"
M2_CSV = RAIZ / "output" / "v8" / "M2" / "predicciones_congeladas.csv"
F5_TAB = RAIZ / "output" / "v8" / "F5" / "fuera_muestra_comun.csv"
NOTAS = RAIZ / "docs" / "v8" / "notas_release.md"
INI = "2007Q1"
ORIGEN = "2026Q2"
H = 4
MEDIDA = "tasa_trim_pp(log x100, real)"
MERC = {"compra": "p", "alquiler": "r"}
NS = 4000
FECHA_CONGELACION = "2026-10-13"   # fecha de la congelacion vigente (constante: md5 estable)


def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def qidx(s: str) -> int:
    a, q = s.split("Q")
    return int(a) * 4 + int(q) - 1


def qstr(i: int) -> str:
    return f"{i // 4}Q{i % 4 + 1}"


def _ols(Z, y):
    b = np.linalg.lstsq(Z, y, rcond=None)[0]
    res = y - Z @ b
    return b, float(np.sqrt(res @ res / max(len(y) - Z.shape[1], 1)))


def lags(v: np.ndarray, t: np.ndarray, ks) -> np.ndarray:
    return np.column_stack([v[t - k] for k in ks])


def ar_pred(y: np.ndarray, dh: np.ndarray, extra: int, rng) -> tuple[np.ndarray, np.ndarray]:
    """y, dh: arrays hasta el origen (misma longitud). Devuelve punto (H,) y simulaciones (NS, H)."""
    n = len(y)
    t = np.arange(4, n)
    Z = np.column_stack([np.ones(len(t)), lags(y, t, range(1, 5))] + ([lags(dh, t, range(1, extra + 1))] if extra else []))
    b, s = _ols(Z, y[t])
    bd, sd = _ols(np.column_stack([np.ones(len(t)), lags(dh, t, range(1, 5))]), dh[t]) if extra else (None, 0.0)

    punto = np.zeros(H)
    sim = np.zeros((NS, H))
    for modo in ("punto", "sim"):
        n_r = 1 if modo == "punto" else NS
        ys = np.tile(y[-4:][::-1], (n_r, 1))          # [y_{T}, y_{T-1}, ...]
        ds = np.tile(dh[-4:][::-1], (n_r, 1))
        for k in range(H):
            ey = np.zeros(n_r) if modo == "punto" else rng.normal(0, s, n_r)
            ed = np.zeros(n_r) if modo == "punto" else rng.normal(0, sd, n_r)
            mu = b[0] + ys @ b[1:5] + (ds[:, :extra] @ b[5:5 + extra] if extra else 0)
            ynew = mu + ey
            if extra:
                dnew = bd[0] + ds @ bd[1:5] + ed
                ds = np.column_stack([dnew, ds[:, :3]])
            ys = np.column_stack([ynew, ys[:, :3]])
            if modo == "punto":
                punto[k] = ynew[0]
            else:
                sim[:, k] = ynew
    return punto, sim


def carga_r5():
    spec = importlib.util.spec_from_file_location("r5_prediccion", RAIZ / "src" / "v7" / "r5_prediccion.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DESC = {"ar4": "AR(4) con constante", "ar_fc": "AR(4) + 2 retardos del HPI zona euro (dhpi); dhpi futuro con AR(4)",
        "ecm_v1": "ECM v1, especificacion A de v7 (dX futuro = 0)"}


def predecir(origen: str = ORIGEN) -> pd.DataFrame:
    """ar4, ar_fc y ecm_v1 estimados con datos hasta `origen` (inclusive); h=1..4. Reutilizada por evaluate_v8 --simular."""
    import m2_svar as M2
    d = M2.cargar()
    S = M2.series_base(d)
    q = [t for t in S.index if INI <= t <= origen]
    assert q[-1] == origen, f"las series no llegan a {origen}"
    r5 = carga_r5()
    qs7, _, data7 = r5.carga_panel()
    ld = np.log(d["ipc_general"])
    niv = {"compra": np.log(d["p_tasado"]) - ld, "alquiler": np.log(d["ipc_alquiler"]) - ld}
    rows = []
    for m, col in MERC.items():
        sub = S.loc[q]
        y, dh = sub[col].to_numpy(float), sub["dhpi"].to_numpy(float)
        assert np.isfinite(y).all() and np.isfinite(dh).all(), "NaN en la muestra de estimacion"
        for nom, extra in (("ar4", 0), ("ar_fc", 2)):
            rng = np.random.default_rng([SEED, 6, len(rows), extra])
            pt_, sim = ar_pred(y, dh, extra, rng)
            for k in range(H):
                lo68, hi68 = np.percentile(sim[:, k], [16, 84])
                lo90, hi90 = np.percentile(sim[:, k], [5, 95])
                rows.append((nom, nom, m, MEDIDA, origen, qstr(qidx(origen) + k + 1), k + 1, pt_[k], lo68, hi68, lo90, hi90))
        y1 = np.array([niv[m].get(t, np.nan) for t in qs7], float)[None, :]
        Xn = data7[m][1].mean(0)
        e = qs7.index(origen)
        assert np.isfinite(y1[0, :e + 1]).all(), "ECM: nivel real con NaN"
        _, info = r5.m_ecm_v1(y1[:, :e + 1], Xn[None, :e + 1], 1)
        coef, th = np.array(info["coef[phi,const,gamma_X..,rho]"]), np.array(info["theta"])
        niveles = r5._ec_forecast(coef, y1[0, e], y1[0, e] - y1[0, e - 1], Xn[e], th, H)
        tasas = 100 * np.diff(np.concatenate([[y1[0, e]], niveles]))
        for k in range(H):
            rows.append(("ecm_v1", "ecm_v1", m, MEDIDA, origen, qstr(qidx(origen) + k + 1), k + 1, float(tasas[k]), np.nan, np.nan, np.nan, np.nan))
    P = pd.DataFrame(rows, columns=["modelo", "familia", "mercado", "medida", "origen", "fecha_objetivo", "h", "punto", "b68_lo", "b68_hi", "b90_lo", "b90_hi"])
    P["evaluable"] = [qidx(f) > qidx(origen) for f in P["fecha_objetivo"]]
    P["nota"] = [DESC[mm] for mm in P["modelo"]]
    return P


def main() -> int:
    recongelar = "--recongelar" in sys.argv
    import m2_svar as M2
    S = M2.series_base(M2.cargar())
    ultimo = {c: S[c].dropna().index[-1] for c in ("p", "r", "dhpi")}
    P = predecir(ORIGEN)
    pcsv = OUT / "predicciones_congeladas.csv"
    pbytes = P.to_csv(index=False, float_format="%.8g", lineterminator="\n").encode("utf-8")
    sha_m2 = sha256(M2_CSV)
    manif_txt = json.dumps({
        "referencias": {"output/v8/M2/predicciones_congeladas.csv": sha_m2},
        "nota": "BVAR principal congelado en M2 (origen 2026Q1; evaluable=True <=> h 1..4 desde 2026T2); no se recalcula aqui."},
        ensure_ascii=False, indent=1)
    ficheros = {"output/v8/congelacion/predicciones_congeladas.csv": hashlib.sha256(pbytes).hexdigest(),
                "output/v8/congelacion/manifiesto.json": hashlib.sha256(manif_txt.encode("utf-8")).hexdigest(),
                "output/v8/M2/predicciones_congeladas.csv": sha_m2}
    conj = hashlib.sha256("\n".join(f"{k} {v}" for k, v in sorted(ficheros.items())).encode()).hexdigest()
    cj_path = OUT / "congelacion.json"
    if cj_path.exists():
        previo = json.loads(cj_path.read_text(encoding="utf-8")).get("sha256_conjunto")
        if previo != conj and not recongelar:
            print(f"f6_congelar: ERROR: el sha256 conjunto recalculado ({conj}) difiere del congelado ({previo}). La congelacion no se rehace en silencio; "
                  "use --recongelar (y anote una fila nueva en docs/v8/desviaciones.md).")
            return 1
    OUT.mkdir(parents=True, exist_ok=True)
    pcsv.write_bytes(pbytes)
    (OUT / "manifiesto.json").write_text(manif_txt, encoding="utf-8")
    tab = pd.read_csv(F5_TAB)
    fam = {m_: dict(modelo=g.sort_values("rmse_pp").iloc[0]["modelo"], rmse_pp=float(g.sort_values("rmse_pp").iloc[0]["rmse_pp"]))
           for m_, g in tab[tab["evaluable"] == "si"].groupby("mercado")}
    cj = dict(semilla=SEED, fecha=FECHA_CONGELACION, capa="C4 (prediccion no es causalidad)",
              muestra=f"{INI}-{ORIGEN} (ar4, ar_fc, ecm_v1); BVAR principal 2004Q2-2026Q1 (M2)",
              origen={"ar4/ar_fc/ecm_v1": ORIGEN, "bvar_m2": "2026Q1 (h_desde_2026T2 = 1..4)"}, ultimo_dato_series=ultimo,
              objetivo="2026T3-2027T2", medida=MEDIDA,
              familias="mejor (unico) modelo de cada familia de output/v8/F5/fuera_muestra_comun.csv: ar4, ar_fc, ecm_v1, bvar_m2",
              rmse_f5_por_mercado=fam, sha256_ficheros=ficheros, sha256_conjunto=conj,
              regla_sha_conjunto="sha256 de las lineas «ruta sha256» ordenadas, unidas con salto de linea")
    cj_path.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    # notas_release: solo se escribe si el sha anotado es PENDIENTE (o falta); una vez anotado no se toca
    txt = NOTAS.read_text(encoding="utf-8").splitlines()
    nuevo = []
    for ln in txt:
        if ln.strip().startswith("sha256_predicciones_v8:"):
            anot = ln.split(":", 1)[1].strip().split()[0] if ":" in ln and ln.split(":", 1)[1].strip() else "PENDIENTE"
            if anot != "PENDIENTE":
                if anot != conj:
                    print(f"f6_congelar: AVISO: docs/v8/notas_release.md conserva el sha anotado {anot}, distinto del recalculado.")
                nuevo.append(ln)
                continue
            ln = f"sha256_predicciones_v8: {conj}"
        nuevo.append(ln)
    if nuevo != txt:
        NOTAS.write_text("\n".join(nuevo) + "\n", encoding="utf-8")
    print(P.pivot_table(index=["mercado", "modelo"], columns="fecha_objetivo", values="punto").round(2).to_string())
    print("sha256_conjunto", conj)
    return 0


if __name__ == "__main__":
    sys.exit(main())
