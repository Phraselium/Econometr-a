"""V18 · réplica ciega de E8-R1 (ITP por CCAA, valor tasado provincial trimestral, dCDH con dosis continua).

Desde docs/v18/plan_replicacion.md (1.8) y la adenda (R-18, 1.3, 1.12, Anexo A). Capa C4; réplica ciega V18.
Determinista (SEED 20261010), sin red. Lecturas territoriales con sellado.filtrar (guarda de check_v17).

Decisiones (cada una con la lectura que admitía más de una):
- Tratamiento: tipo general del ITP por CCAA, de data/raw/v16/intervenciones/intervenciones.csv (fechas de entrada en vigor de
  las memorias de Tributación Autonómica de Hacienda). Se usa solo 'tipo general ITP' y, si la CCAA no lo trae, el tipo mínimo de la escala.
- Mes de efecto: día <= 15, ese mes; si no, el siguiente. Trimestre de ese mes.
- Dos cambios de una CCAA a menos de 12 meses: un solo evento con la dosis acumulada en la primera fecha.
- Panel 2010T1-2026T2: antes de 2010 el fichero no da tipos (no se extrapola). 36 provincias de las 8 CCAA de régimen común no selladas.
- Sin control de recaudación previa (no está descargada): tope SUGESTIVO por la adenda.
- Estimador: dCDH con dosis continua (src/v18/herramientas/dcdh.py), efecto acumulado a l = 4 trimestres por +1 pp, resultado ln valor tasado.
  Inferencia: aleatorización del calendario entre las 8 CCAA (9.999 permutaciones, estudentizada) y bootstrap de Webb con H0 impuesta.
  IC95 por inversión del contraste de aleatorización (rejilla), con el EE de agrupación por CCAA como referencia.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import holdout  # noqa: E402,F401
import sellado  # noqa: E402
from herramientas import dcdh  # noqa: E402

SEED = 20261010
SALIDA = RAIZ / "output" / "v18" / "replica" / "e8_r1"
ELL = 4
CCAA8 = ["01", "06", "07", "08", "09", "10", "11", "12"]  # códigos del fichero de intervenciones (INE-CCAA propio del fichero)
CCAA_NOMBRE = {"01": "Andalucía", "06": "Cantabria", "07": "Castilla y León", "08": "Castilla-La Mancha", "09": "Cataluña",
               "10": "Comunitat Valenciana", "11": "Extremadura", "12": "Galicia"}
PROV_CCAA = {"Andalucía": ["04", "11", "14", "18", "21", "23", "29", "41"], "Cantabria": ["39"],
             "Castilla y León": ["05", "09", "24", "34", "37", "40", "42", "47", "49"],
             "Castilla-La Mancha": ["02", "13", "16", "19", "45"], "Cataluña": ["08", "17", "25", "43"],
             "Comunitat Valenciana": ["03", "12", "46"], "Extremadura": ["06", "10"], "Galicia": ["15", "27", "32", "36"]}


def trimestre(fecha: pd.Timestamp) -> str:
    """Regla de codificación de la adenda: día <= 15, mes de entrada en vigor; si no, el siguiente."""
    f = fecha if fecha.day <= 15 else (fecha + pd.offsets.MonthBegin(1))
    return f"{f.year}T{(f.month - 1) // 3 + 1}"


def calendario(desplazar_meses: int = 0) -> pd.DataFrame:
    d = pd.read_csv(RAIZ / "data/raw/v16/intervenciones/intervenciones.csv", dtype={"cod_ine": str})
    i = d[(d.instrumento == "itp") & d.territorio.isin(CCAA_NOMBRE.values())].copy()
    gen = i[i.parametro == "tipo general ITP"]
    mini = i[i.parametro == "tipo general ITP (tipo mínimo de la escala)"]
    usar = pd.concat([gen, mini[~mini.territorio.isin(gen.territorio)]])
    usar["valor"] = pd.to_numeric(usar["valor"])
    usar["inicio"] = pd.to_datetime(usar["fecha_efecto"])
    usar = usar.sort_values(["territorio", "inicio"])
    ev = []
    for t, g in usar.groupby("territorio"):
        g = g.reset_index(drop=True)
        g["dosis"] = g["valor"].diff()
        g = g[g["dosis"].fillna(0) != 0]
        # agrupar cambios a < 12 meses en el primero
        acum = []
        for _, r in g.iterrows():
            if acum and (r["inicio"] - acum[-1]["inicio"]).days < 365:
                acum[-1]["dosis"] += r["dosis"]
            else:
                acum.append({"territorio": t, "inicio": r["inicio"], "dosis": float(r["dosis"])})
        ev += acum
    e = pd.DataFrame(ev)
    f = e["inicio"] + pd.DateOffset(months=desplazar_meses)
    e["trimestre"] = [trimestre(x) for x in f]
    return e


def panel_dosis(ev: pd.DataFrame, periodos: list[str]) -> pd.DataFrame:
    """Nivel de dosis acumulada (pp sobre el tipo inicial 2010T1) por CCAA y trimestre."""
    out = {}
    for t in CCAA_NOMBRE.values():
        e = ev[ev.territorio == t]
        out[t] = [float(e.loc[e.trimestre <= p, "dosis"].sum()) for p in periodos]
    return pd.DataFrame(out, index=periodos).T


def cargar_resultado() -> pd.DataFrame:
    h = pd.read_parquet(RAIZ / "data/base/hechos.parquet",
                        filters=[("variable", "=", "valor_tasado"), ("nivel", "=", "provincia"), ("frecuencia", "=", "T")])
    h = h[["territorio_codigo", "periodo", "valor", "muestra_sellada_v6"]].copy()
    h["territorio_codigo"] = h["territorio_codigo"].astype(str).str.zfill(2)
    return sellado.filtrar(h, "territorio_codigo", "provincia", "periodo", "valor_tasado", "T")


def preparar(desplazar=0, quitar_2012_13=False):
    y = cargar_resultado()
    periodos = [f"{a}T{q}" for a in range(2010, 2027) for q in range(1, 5) if f"{a}T{q}" <= "2026T2"]
    y = y[y.periodo.isin(periodos)]
    ev = calendario(desplazar)
    if quitar_2012_13:
        ev = ev[~ev.trimestre.str[:4].isin(["2012", "2013"])]
    dc = panel_dosis(ev, periodos)
    filas = [(p, c) for c, ps in PROV_CCAA.items() for p in ps]
    provs = [p for p, _ in filas]
    w = y.pivot(index="territorio_codigo", columns="periodo", values="valor").reindex(index=provs, columns=periodos)
    completo = w.notna().all(axis=1)
    provs_ok = [p for p in provs if completo[p]]
    cc = [c for p, c in filas if completo[p]]
    Y = np.log(w.loc[provs_ok].to_numpy(float))
    ccaas = list(CCAA_NOMBRE.values())
    cl = np.array([ccaas.index(c) for c in cc])
    Dc = dc.loc[ccaas].to_numpy(float)
    return Y, Dc, cl, provs_ok, periodos, ev, [p for p in provs if not completo[p]]


def ic_inversion(Y, Dc, cl, perms, b, se, ell):
    """IC95 por inversión del contraste de aleatorización: valores theta0 con p >= 0,05 en una rejilla."""
    rej = np.linspace(b - 6 * se, b + 6 * se, 241)
    ok = [t for t in rej if dcdh.p_aleatorizacion(Y, Dc, cl, t, ell, perms) >= 0.05]
    return (float(min(ok)), float(max(ok))) if ok else (float("nan"), float("nan"))


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    Y, Dc, cl, provs, periodos, ev, perdidas = preparar()
    G = Dc.shape[0]
    M = dcdh.onehot(cl)
    D = Dc[cl]
    nchg = int((np.diff(Dc, axis=1) != 0).sum())
    ccaa_cambio = int((np.abs(np.diff(Dc, axis=1)).sum(1) > 0).sum())
    perms = dcdh.permutaciones(rng, G, 9999)
    res = {}
    for ell in [0, 2, 4, 6, 8]:
        r = dcdh.estimar(Y, D, ell)
        se = float(dcdh.ee_cluster(r["IF"], M))
        res[ell] = {"beta": float(r["beta"]), "se_cluster_ccaa": se, "den": float(r["den"])}
    r4 = dcdh.estimar(Y, D, ELL)
    b = float(r4["beta"])
    se = res[ELL]["se_cluster_ccaa"]
    p_ale = dcdh.p_aleatorizacion(Y, D[:, :] * 0 + D, cl, 0.0, ELL, perms) if False else dcdh.p_aleatorizacion(Y, Dc, cl, 0.0, ELL, perms)
    p_webb = dcdh.p_webb(Y, D, 0.0, ELL, M, np.random.default_rng(SEED), B=9999)
    ic = ic_inversion(Y, Dc, cl, perms, b, se, ELL)
    # robustez: fechas -3 / +3 meses, sin 2012-2013
    rob = {}
    for nom, kw in [("fechas_-3m", dict(desplazar=-3)), ("fechas_+3m", dict(desplazar=3)), ("sin_2012_2013", dict(quitar_2012_13=True))]:
        Yr, Dr, clr, *_ = preparar(**kw)
        rr = dcdh.estimar(Yr, Dr[clr], ELL)
        rob[nom] = {"beta": float(rr["beta"]), "se_cluster_ccaa": float(dcdh.ee_cluster(rr["IF"], dcdh.onehot(clr)))}
    out = {
        "rama": "replica_ciega_v18", "pregunta": "E8-R1: efecto de +1 pp del tipo general del ITP en el log del valor tasado a 4 trimestres",
        "capa": "C4", "rotulo": "réplica ciega V18; capa C4",
        "datos": "valor_tasado provincial trimestral (base) 2010T1-2026T2 (sellado.filtrar), 36 provincias de 8 CCAA; "
                 "tipos generales de data/raw/v16/intervenciones/intervenciones.csv (memorias de Hacienda)",
        "N": int(Y.shape[0] * Y.shape[1]), "n_provincias": int(Y.shape[0]), "n_clusters": int(G), "n_trimestres": int(Y.shape[1]),
        "provincias_perdidas_por_huecos": perdidas,
        "metodo": "dCDH dosis continua l=4; ln valor tasado; cluster CCAA; aleatorización del calendario (9.999) y Webb",
        "estimacion": b, "se_cluster_ccaa": se, "ic95": list(ic), "ic95_metodo": "inversión del contraste de aleatorización (rejilla ±6 EE)",
        "ic95_normal_cluster": [b - 1.96 * se, b + 1.96 * se],
        "p_ajustado": None, "p_aleatorizacion": p_ale, "p_webb": p_webb,
        "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": "no se clasifica (réplica ciega)",
        "diagnosticos": {"efectos_por_horizonte": res, "robustez": rob, "cambios_efectivos": nchg, "ccaa_con_cambio": ccaa_cambio,
                         "eventos": ev.assign(inicio=ev.inicio.dt.strftime("%Y-%m-%d")).to_dict("records"),
                         "sin_control_recaudacion_previa": True},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Sin recaudación previa (no descargada): tope SUGESTIVO. Panel desde 2010T1 (sin tipos antes). Sin evaluación sellada.",
    }
    (SALIDA / "resultado.json").write_text(json.dumps(out, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ["N", "n_provincias", "estimacion", "se_cluster_ccaa", "ic95", "ic95_normal_cluster", "p_aleatorizacion", "p_webb"]}, indent=1))
    print(res); print(rob); print(nchg, ccaa_cambio, perdidas)


if __name__ == "__main__":
    main()
