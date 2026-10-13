"""V8: validación limpia DIFERIDA (`make evaluate_v8`). Fuera de `make all`. Capa C4 (predicción no es causalidad).

Evalúa UNA sola vez las predicciones congeladas por src/v8/f6_congelar.py (hipotesis.md §10) con datos publicados después de 2026T2:
precio real de compra (valor tasado MIVAU deflactado con IPC general) y alquiler real (IPC alquiler deflactado), crecimiento
trimestral log x100, objetivos 2026T3-2027T2.

Pasos:
  1. Comprueba sha256 de cada fichero congelado y el conjunto frente a docs/v8/notas_release.md (la congelación es anterior).
  2. Si ya hay una apertura registrada en docs/v8/evaluate_v8_accesos.md, se niega (una sola evaluación).
  3. Descarga (CON red) a data/raw/v8_eval/<fecha>/ con RAW_DIR (src/utils_fetch.py lo respeta; fetch_mivau.py, fetch_ine.py y
     fetch_v8.py lo usan vía utils_fetch), sin tocar data/raw.
  4. Si no hay periodos > 2026T2, o no están los cuatro objetivos 2026T3-2027T2 en las tres series, sale SIN registrar apertura
     (evita gastar la única evaluación con datos parciales).
  5. Registra la apertura ANTES de evaluar; después RMSE h=1-4 frente a AR(4) y la base fuerte (AR con factor común), DM-HLN y Holm.
  6. Escribe output/v8/evaluate/resultado.json y añade la evaluación al registro de accesos.
Con 4 objetivos y un único origen la potencia de DM es muy baja: los p son DESCRIPTIVOS, no concluyentes (se declara en el resultado).

Uso: python3 src/v8/evaluate_v8.py [--simular]
  --simular: ensayo con datos de entrenamiento troceados (origen 2023T4, objetivos 2024T1-T4 ya vistos); sin red; no registra nada.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import dm_test, holm  # noqa: E402

CONG = RAIZ / "output" / "v8" / "congelacion" / "congelacion.json"
NOTAS = RAIZ / "docs" / "v8" / "notas_release.md"
ACCESOS = RAIZ / "docs" / "v8" / "evaluate_v8_accesos.md"
OUT = RAIZ / "output" / "v8" / "evaluate"
ENSAYO = RAIZ / "output" / "v8" / "congelacion" / "ensayo_evaluate.md"
ULTIMO_ENTRENO = "2026Q2"
OBJETIVOS = ["2026Q3", "2026Q4", "2027Q1", "2027Q2"]
BASES = ("ar4", "ar_fc")
SCRIPTS_FETCH = ("src/fetch_mivau.py", "src/fetch_ine.py", "src/v8/fetch_v8.py")


def sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ya_abierto() -> bool:
    if not ACCESOS.exists():
        return False
    return any(ln.startswith("|") and "| APERTURA |" in ln for ln in ACCESOS.read_text(encoding="utf-8").splitlines())


def sha_anotado() -> str | None:
    if NOTAS.exists():
        for ln in NOTAS.read_text(encoding="utf-8").splitlines():
            if ln.strip().startswith("sha256_predicciones_v8:"):
                return ln.split(":", 1)[1].strip().split()[0]
    return None


def verificar() -> tuple[bool, str, dict]:
    if not CONG.exists():
        return False, "falta output/v8/congelacion/congelacion.json (F6 no ha congelado)", {}
    cj = json.loads(CONG.read_text(encoding="utf-8"))
    for f, s in cj["sha256_ficheros"].items():
        if sha256(RAIZ / f) != s:
            return False, f"sha256 distinto en {f}", cj
    if sha_anotado() != cj["sha256_conjunto"]:
        return False, "el sha256 conjunto no coincide con docs/v8/notas_release.md", cj
    return True, "ok", cj


def descargar(destino: Path) -> None:
    """Descarga con los scripts fetch existentes hacia un directorio aparte (RAW_DIR; no reescribe data/raw)."""
    destino.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "RAW_DIR": str(destino), "FORCE": "1"}
    for s in SCRIPTS_FETCH:
        subprocess.run([sys.executable, s], cwd=RAIZ, env=env, check=False)


# ------------------------------------------------------------------------------------------------ observados
def _serie(df: pd.DataFrame, serie: str, freq: str) -> pd.Series:
    s = df.loc[df["serie"] == serie].dropna(subset=["valor"])
    f = pd.to_datetime(s["fecha"])
    return pd.Series(s["valor"].to_numpy(float), index=pd.PeriodIndex(f, freq=freq)).sort_index()


def _m2q(s: pd.Series) -> pd.Series:
    q = pd.PeriodIndex(s.index.to_timestamp(), freq="Q")
    g = s.groupby(q)
    r = g.mean()
    return r[g.count() == 3]   # solo trimestres completos


def observados(dirx: Path) -> pd.DataFrame:
    """Crecimiento trimestral real (log x100) de compra y alquiler desde ficheros con el formato de data/raw."""
    vt = _serie(pd.read_csv(dirx / "mivau_valor_tasado_nacional_ccaa_prov.csv"), "valor_tasado_libre_nacional", "Q")
    al = _m2q(_serie(pd.read_csv(dirx / "ine_ipc_alquiler.csv"), "IPC290887", "M"))
    ipc = _m2q(_serie(pd.read_csv(dirx / "v8" / "ine_ipc_24077_general.csv"), "IPC290751", "M"))
    out = {}
    for m, s in (("compra", vt), ("alquiler", al)):
        niv = np.log(s) - np.log(ipc.reindex(s.index))
        t = 100 * niv.diff()
        for p, v in t.dropna().items():
            out[(m, f"{p.year}Q{p.quarter}")] = float(v)
    return pd.DataFrame([(m, q, v) for (m, q), v in out.items()], columns=["mercado", "trimestre", "obs"])


# ------------------------------------------------------------------------------------------------ evaluación
def evaluar(P: pd.DataFrame, obs: pd.DataFrame) -> dict:
    """P: modelo, mercado, fecha_objetivo, h, punto. obs: mercado, trimestre, obs. Misma muestra para todos los modelos."""
    M = P.merge(obs, left_on=["mercado", "fecha_objetivo"], right_on=["mercado", "trimestre"], how="inner")
    M["e"] = M["obs"] - M["punto"]
    # misma muestra: solo objetivos observados para TODOS los modelos del mercado
    ok = M.groupby(["mercado", "fecha_objetivo"])["modelo"].nunique()
    nmod = M.groupby("mercado")["modelo"].nunique()
    keep = [(m, f) for (m, f), n in ok.items() if n == nmod[m]]
    M = M[[(m, f) in set(keep) for m, f in zip(M["mercado"], M["fecha_objetivo"])]]
    rm_h = M.assign(e2=M["e"] ** 2).groupby(["mercado", "modelo", "h"]).agg(rmse_pp=("e2", lambda s: float(np.sqrt(s.mean()))), n=("e", "size")).reset_index()
    rm = M.assign(e2=M["e"] ** 2).groupby(["mercado", "modelo"]).agg(rmse_pp=("e2", lambda s: float(np.sqrt(s.mean()))), n=("e", "size")).reset_index()
    pend = []
    for m, g in M.groupby("mercado"):
        E = g.pivot(index="fecha_objetivo", columns="modelo", values="e")
        for mod in E.columns:
            for ref in BASES:
                if mod == ref or ref not in E.columns or len(E) < 3 or (mod == "ar_fc" and ref == "ar4"):
                    continue
                r = dm_test(E[mod].values, E[ref].values, h=1)   # h=1: con n=4 la correccion HLN de h=4 se anula (ver docstring)
                pend.append(dict(mercado=m, modelo=mod, ref=ref, dm_hln=r["DM"], p=r["p"], n=r["n"],
                                 rmse_ratio=float(np.sqrt((E[mod] ** 2).mean() / (E[ref] ** 2).mean()))))
    D = pd.DataFrame(pend)
    if len(D):
        hh = holm({f"{r.mercado}|{r.modelo}|{r.ref}": r.p for r in D.itertuples()})
        D["p_holm"] = [hh[f"{r.mercado}|{r.modelo}|{r.ref}"] for r in D.itertuples()]
    return dict(rmse_por_h=rm_h.to_dict("records"), rmse=rm.to_dict("records"), dm=D.to_dict("records"),
                objetivos=sorted(M["fecha_objetivo"].unique()), n_modelos=int(M["modelo"].nunique()))


def bvar_m2(cj: dict) -> pd.DataFrame:
    m2 = pd.read_csv(RAIZ / "output" / "v8" / "M2" / "predicciones_congeladas.csv")
    m2 = m2[(m2["evaluable"].astype(str) == "True") & m2["medida"].str.startswith("tasa_trim") & m2["variable"].isin(["p", "r"])]
    return pd.DataFrame(dict(modelo="bvar_m2", mercado=m2["mercado"], fecha_objetivo=m2["fecha_objetivo"],
                             h=m2["h_desde_2026T2"], punto=m2["mediana"]))


def md(res: dict, titulo: str) -> str:
    L = [f"# {titulo}", "", f"Objetivos evaluados: {', '.join(res['objetivos'])}; modelos: {res['n_modelos']}.", "",
         "## RMSE (pp, crecimiento trimestral real log x100)", "", "| mercado | modelo | RMSE | n |", "|---|---|---|---|"]
    L += [f"| {r['mercado']} | {r['modelo']} | {r['rmse_pp']:.3f} | {r['n']} |" for r in res["rmse"]]
    L += ["", "## DM-HLN y Holm (vs AR(4) y vs AR + factor comun)", "", "| mercado | modelo | ref | RMSE/RMSE_ref | DM-HLN | p | p Holm |", "|---|---|---|---|---|---|---|"]
    L += [f"| {r['mercado']} | {r['modelo']} | {r['ref']} | {r['rmse_ratio']:.2f} | {r['dm_hln']:.2f} | {r['p']:.3f} | {r['p_holm']:.3f} |" for r in res["dm"]]
    L += ["", "Aviso: con 4 objetivos de un solo origen los p son DESCRIPTIVOS (potencia muy baja). C4: prediccion, no causalidad."]
    return "\n".join(L) + "\n"


def simular() -> int:
    import f6_congelar as F6
    ok, msg, cj = verificar()
    print(f"evaluate_v8 --simular: verificacion de la congelacion: {msg}")
    import m2_svar as M2
    S = M2.series_base(M2.cargar())
    origen = "2023Q4"
    P = F6.predecir(origen)
    P = P[P["evaluable"]]
    obs = pd.DataFrame([(m, t, float(S[c].loc[t])) for m, c in F6.MERC.items() for t in P["fecha_objetivo"].unique()],
                       columns=["mercado", "trimestre", "obs"])
    res = evaluar(P, obs)
    txt = md(res, "Ensayo de evaluate_v8 (--simular)")
    txt += ("\nCondiciones del ensayo: origen " + origen + ", objetivos 2024T1-T4 (YA VISTOS: dentro de la muestra de entrenamiento de la congelacion; "
            "no es evidencia); modelos ar4, ar_fc, ecm_v1 (el BVAR de M2 no se re-estima en el ensayo). Sin red; no se escribe docs/v8/evaluate_v8_accesos.md.\n")
    ENSAYO.parent.mkdir(parents=True, exist_ok=True)
    ENSAYO.write_text(txt, encoding="utf-8")
    print(txt)
    return 0


def main(sim: bool = False) -> int:
    if sim:
        return simular()
    ok, msg, cj = verificar()
    if not ok:
        print(f"evaluate_v8: {msg}: no se evalua.")
        return 2
    if ya_abierto():
        print("evaluate_v8: la validacion diferida ya se abrio una vez (docs/v8/evaluate_v8_accesos.md).")
        return 3
    hoy = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    destino = RAIZ / "data" / "raw" / "v8_eval" / hoy[:10]
    descargar(destino)
    try:
        obs = observados(destino)
    except Exception as ex:   # descarga incompleta: sin datos no hay apertura
        print(f"evaluate_v8: no se pudieron leer los datos nuevos ({type(ex).__name__}: {ex}); no se registra apertura.")
        return 0
    nuevos = sorted(set(obs.loc[obs["trimestre"] > ULTIMO_ENTRENO, "trimestre"]))
    if not nuevos:
        print("evaluate_v8: aun no hay periodos posteriores a 2026T2; no se registra apertura.")
        return 0
    cobertura = obs[obs["trimestre"].isin(OBJETIVOS)].groupby("trimestre")["mercado"].nunique()
    if not all(cobertura.get(q, 0) == 2 for q in OBJETIVOS):
        print(f"evaluate_v8: faltan objetivos (hay {nuevos}); se esperan {OBJETIVOS} en compra y alquiler; no se registra apertura.")
        return 0
    with ACCESOS.open("a", encoding="utf-8") as f:
        f.write(f"| {hoy} | APERTURA | periodos {OBJETIVOS[0]}-{OBJETIVOS[-1]} | sha256 congelacion {cj['sha256_conjunto']} |\n")
    P = pd.concat([pd.read_csv(RAIZ / "output" / "v8" / "congelacion" / "predicciones_congeladas.csv")[["modelo", "mercado", "fecha_objetivo", "h", "punto"]],
                   bvar_m2(cj)], ignore_index=True)
    res = evaluar(P, obs)
    rmse = {f"{r['mercado']}|{r['modelo']}": r["rmse_pp"] for r in res["rmse"]}
    dm4 = {f"{r['mercado']}|{r['modelo']}|{r['ref']}": dict(dm_hln=r["dm_hln"], p=r["p"], p_holm=r["p_holm"]) for r in res["dm"]}
    out = dict(rama="v8/evaluate", pregunta="¿predicen mejor que AR(4) y que AR + factor comun las predicciones congeladas de V8 (h=1-4 desde 2026T2)?",
               capa="C4", datos=f"data/raw/v8_eval/{hoy[:10]} (valor tasado MIVAU, IPC alquiler, IPC general; INE/MIVAU)", N=len(res["objetivos"]),
               metodo="RMSE h=1-4, DM con correccion HLN (h=1) y Holm; una unica apertura", estimacion=rmse, ic95=None,
               p_ajustado={k: v["p_holm"] for k, v in dm4.items()}, nivel_evidencia="EXPLORATORIO (prediccion; no causal)",
               diagnosticos=dict(dm=dm4, rmse_por_h=res["rmse_por_h"], objetivos=res["objetivos"], sha256_conjunto=cj["sha256_conjunto"]),
               fuera_muestra=dict(modelo="mejor de cada familia (ar4, ar_fc, ecm_v1, bvar_m2)", rmse=rmse, dm_vs_ar4={k: v for k, v in dm4.items() if k.endswith("|ar4")}),
               notas="n=4 objetivos y un solo origen: p descriptivos. Un modelo solo «predice mejor» si supera a la base mas exigente (AR con factor comun o AR(4)).")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "resultado.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    with ACCESOS.open("a", encoding="utf-8") as f:
        f.write(f"| {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} | EVALUACION | rmse {json.dumps(rmse, ensure_ascii=False)[:300]} | |\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sim="--simular" in sys.argv))
