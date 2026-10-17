"""V16-F3 · Metaanálisis de la literatura por instrumento (docs/v16/plan.md, fase 3): distribuciones a priori para la fase 6.

Entrada: docs/v16/literatura/*_efectos.csv (una fila por estimación leída; columnas del encargo de los lectores).
Regla fijada antes de mirar los resultados (docs/v16/decisiones.md K7):
- Grupo = fichero × `resultado` (texto literal del lector). Un estudio = `autores_anio`.
- Un estudio aporta UNA estimación: la primera fila que el lector anotó para ese estudio y resultado (el lector anota primero la principal).
  Las filas de fichas de V15 citadas de segunda mano (leido = «ficha V15») cuentan como estudio si traen error estándar.
- El error estándar es el del autor; si falta y hay IC 95 %, ee = (sup − inf) / (2 · 1,96). Nunca se imputa.
- Solo hay metaanálisis si el grupo tiene ≥ 5 estudios con ee y la misma unidad_efecto. Con menos, «insuficiente»: se informa el rango
  de las estimaciones y su mediana, sin agregar.
- Efectos aleatorios: DerSimonian-Laird y REML (se informan los dos). Heterogeneidad: τ², I², Q.
- Sesgo de publicación: Egger (intercepto de z sobre la precisión), PET (WLS de la estimación sobre ee) y PEESE (sobre ee²); con k < 10
  se informan con la advertencia de baja potencia.
Salida: output/v16/f3/metaanalisis.csv, output/v16/f3/metaanalisis.md y output/v16/f3/resultado.json. Determinista, sin red.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

RAIZ = Path(__file__).resolve().parents[2]
LIT = RAIZ / "docs" / "v16" / "literatura"
SAL = RAIZ / "output" / "v16" / "f3"
K_MIN = 5
Z = 1.959963984540054


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace(",", ".", regex=False).str.replace("−", "-", regex=False), errors="coerce")


def leer() -> pd.DataFrame:
    partes = []
    for f in sorted(LIT.glob("*_efectos.csv")):
        import csv
        with f.open(encoding="utf-8", newline="") as fh:
            largos = {len(x) for x in csv.reader(fh)}
        if len(largos) != 1:   # una coma sin comillas desplaza las columnas: se para, no se adivina
            raise SystemExit(f"f3_metaanalisis: {f.name} tiene filas de {sorted(largos)} campos")
        d = pd.read_csv(f, dtype=str).fillna("")
        d.insert(0, "fichero", f.name.replace("_efectos.csv", ""))
        partes.append(d)
    d = pd.concat(partes, ignore_index=True)
    d["est"], d["ee_n"] = _num(d.estimacion), _num(d.ee)
    inf, sup = _num(d.ic95_inf), _num(d.ic95_sup)
    d["ee_ic"] = (sup - inf) / (2 * Z)
    d["ee_final"] = d.ee_n.where(d.ee_n > 0, d.ee_ic.where(d.ee_ic > 0))
    d["orden"] = range(len(d))
    return d


def dl(y: np.ndarray, v: np.ndarray) -> tuple[float, float, float, float]:
    w = 1 / v
    mu_f = np.sum(w * y) / np.sum(w)
    q = float(np.sum(w * (y - mu_f) ** 2))
    k = len(y)
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (q - (k - 1)) / c)
    ws = 1 / (v + tau2)
    mu = float(np.sum(ws * y) / np.sum(ws))
    return mu, float(np.sqrt(1 / np.sum(ws))), tau2, q


def reml(y: np.ndarray, v: np.ndarray, it: int = 500) -> tuple[float, float, float]:
    tau2 = dl(y, v)[2]
    for _ in range(it):
        w = 1 / (v + tau2)
        mu = np.sum(w * y) / np.sum(w)
        nuevo = max(0.0, float(np.sum(w ** 2 * ((y - mu) ** 2 - v)) / np.sum(w ** 2) + 1 / np.sum(w)))
        if abs(nuevo - tau2) < 1e-12:
            tau2 = nuevo
            break
        tau2 = nuevo
    w = 1 / (v + tau2)
    return float(np.sum(w * y) / np.sum(w)), float(np.sqrt(1 / np.sum(w))), tau2


def sesgo(y: np.ndarray, se: np.ndarray) -> dict:
    eg = sm.OLS(y / se, sm.add_constant(1 / se)).fit()
    pet = sm.WLS(y, sm.add_constant(se), weights=1 / se ** 2).fit()
    peese = sm.WLS(y, sm.add_constant(se ** 2), weights=1 / se ** 2).fit()
    return {"egger_intercepto": float(eg.params[0]), "egger_p": float(eg.pvalues[0]),
            "pet": float(pet.params[0]), "pet_ee": float(pet.bse[0]), "pet_p": float(pet.pvalues[0]),
            "peese": float(peese.params[0]), "peese_ee": float(peese.bse[0])}


def main() -> int:
    d = leer()
    filas = []
    for (fich, res), g in d.groupby(["fichero", "resultado"], sort=True):
        prim = g.sort_values("orden").drop_duplicates("autores_anio")      # una estimación por estudio: la primera anotada
        prim = prim[prim.est.notna()]
        con = prim[prim.ee_final.notna()]
        unidades = sorted(set(con.unidad_efecto))
        base = {"instrumento": fich, "resultado": res, "estudios": int(prim.autores_anio.nunique()),
                "estudios_con_ee": int(len(con)), "unidad_efecto": " | ".join(sorted(set(prim.unidad_efecto)))[:200],
                "min": float(prim.est.min()) if len(prim) else None, "mediana": float(prim.est.median()) if len(prim) else None,
                "max": float(prim.est.max()) if len(prim) else None}
        if len(con) >= K_MIN and len(unidades) == 1:
            y, se = con.est.to_numpy(float), con.ee_final.to_numpy(float)
            mu, emu, tau2, q = dl(y, se ** 2)
            mr, emr, tr = reml(y, se ** 2)
            i2 = max(0.0, (q - (len(y) - 1)) / q) if q > 0 else 0.0
            base.update({"estado": "metaanálisis", "dl": mu, "dl_ic95": [mu - Z * emu, mu + Z * emu], "reml": mr,
                         "reml_ic95": [mr - Z * emr, mr + Z * emr], "tau2_dl": tau2, "tau2_reml": tr, "I2": i2, "Q": q,
                         **sesgo(y, se), "aviso": "k < 10: pruebas de sesgo de baja potencia" if len(y) < 10 else ""})
        else:
            motivo = (f"{len(con)} estudios con ee (< {K_MIN})" if len(con) < K_MIN else f"unidades distintas: {len(unidades)}")
            n_uni = prim.unidad_efecto.nunique()
            if n_uni > 1:
                motivo += f"; el rango mezcla {n_uni} unidades (no comparable)"
            base.update({"estado": "insuficiente", "aviso": motivo})
        filas.append(base)
    r = pd.DataFrame(filas)
    SAL.mkdir(parents=True, exist_ok=True)
    out = r.copy()
    for c in ("dl_ic95", "reml_ic95"):
        if c in out:
            out[c] = out[c].map(lambda x: "" if not isinstance(x, list) else f"{x[0]:.4g};{x[1]:.4g}")
    out.to_csv(SAL / "metaanalisis.csv", index=False, lineterminator="\n", float_format="%.6g")
    ma = r[r.estado == "metaanálisis"]
    L = ["# V16 · Metaanálisis de la literatura (fase 3)", "",
         "Generado por `python3 src/v16/f3_metaanalisis.py` desde docs/v16/literatura/*_efectos.csv. Regla fijada de antemano (decisiones K7): "
         f"un estudio, una estimación (la primera anotada); metaanálisis solo con ≥ {K_MIN} estudios con error estándar y la misma unidad. "
         "Las fichas están NO VERIFICADAS hasta pasar el verificador de referencias, y casi todas se leyeron en resumen: estos agregados son "
         "distribuciones a priori orientativas para la fase 6, no hallazgos (capa C4).", "",
         f"Grupos: {len(r)}; con metaanálisis: {len(ma)}; insuficientes: {len(r) - len(ma)}.", ""]
    for _, m in ma.iterrows():
        L += [f"## {m.instrumento} · {m.resultado}", "",
              f"- Unidad: {m.unidad_efecto}. Estudios: {m.estudios_con_ee}.",
              f"- Efectos aleatorios DL: {m.dl:.4g} (IC 95 % {m.dl_ic95[0]:.4g} a {m.dl_ic95[1]:.4g}); REML: {m.reml:.4g} "
              f"(IC 95 % {m.reml_ic95[0]:.4g} a {m.reml_ic95[1]:.4g}).",
              f"- Heterogeneidad: τ² (DL) = {m.tau2_dl:.4g}; I² = {100 * m.I2:.0f} %; Q = {m.Q:.4g}.",
              f"- Sesgo de publicación: Egger, intercepto {m.egger_intercepto:.3g} (p = {m.egger_p:.3g}); PET {m.pet:.4g} (ee {m.pet_ee:.3g}); "
              f"PEESE {m.peese:.4g} (ee {m.peese_ee:.3g}). {m.aviso}", ""]
    L += ["## Grupos sin metaanálisis (rango de las estimaciones, sin agregar)", "",
          "| Instrumento | Resultado | Estudios | Con ee | Mínimo | Mediana | Máximo | Motivo |", "|---|---|---|---|---|---|---|---|"]
    for _, m in r[r.estado != "metaanálisis"].iterrows():
        f = (lambda x: "" if x is None or pd.isna(x) else f"{x:.3g}")
        L.append(f"| {m.instrumento} | {str(m.resultado).replace('|', '/')} | {m.estudios} | {m.estudios_con_ee} | {f(m['min'])} | "
                 f"{f(m.mediana)} | {f(m['max'])} | {m.aviso} |")
    (SAL / "metaanalisis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    res = {"rama": "v16-f3-metaanalisis", "pregunta": "Distribuciones a priori por instrumento desde la literatura leída", "capa": "C4",
           "datos": sorted(str(p.relative_to(RAIZ)) for p in LIT.glob("*_efectos.csv")), "N": int(len(d)),
           "metodo": "efectos aleatorios DL y REML; Egger, PET-PEESE", "estimacion": None, "ic95": None, "p_ajustado": None,
           "nivel_evidencia": "DESCRIPTIVO",
           "diagnosticos": {"grupos": int(len(r)), "con_metaanalisis": int(len(ma)),
                            "metaanalisis": [{k: (v if not isinstance(v, float) else round(v, 6)) for k, v in m.items()
                                              if k in ("instrumento", "resultado", "estudios_con_ee", "dl", "dl_ic95", "reml", "reml_ic95",
                                                       "I2", "egger_p", "pet", "peese")} for _, m in ma.iterrows()]},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Fichas NO VERIFICADAS y casi todas leídas en resumen; priors orientativos, no hallazgos."}
    (SAL / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float) + "\n", encoding="utf-8")
    print(f"f3_metaanalisis: {len(r)} grupos, {len(ma)} con metaanálisis")
    return 0


if __name__ == "__main__":
    sys.exit(main())
