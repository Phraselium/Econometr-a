"""V9 F3 · D1 zonas tensionadas y topes (pre-registro: docs/v9/hipotesis.md, D1). SEED = 20261010.

D1a zonas tensionadas de Cataluña (Incasòl trimestral 2022T2-2026T1; addendum A1), D1b Ley 11/2020 (2019T1-2022T1),
D1c Euskadi (EMAL, exploratorio). Estimadores de src/v9/herramientas.py (validados por Monte Carlo).
Salidas: output/v9/d1/{tabla_d1.csv, estudio_eventos.csv, pruebas.csv, resultado.json, registry.csv, fig_d1*.png}.
Incasòl no es redistribuible: las salidas solo contienen estimaciones agregadas.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import herramientas as H  # noqa: E402
import paneles as P  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = P.RAIZ / "output" / "v9" / "d1"
REG = Registry(OUT / "registry.csv")
B = 999
NPERM = 500


def matriz(df: pd.DataFrame, var: str, t_ini: int, t_fin: int, tcol: str = "t") -> pd.DataFrame:
    d = df[(df[tcol] >= t_ini) & (df[tcol] <= t_fin)]
    w = d.pivot_table(index="cod", columns=tcol, values=var)
    w = w[(w > 0).all(1)].dropna()
    return np.log(w)


def fila(diseno, hip, resultado, espec, r, n_t, n_c, T, conf, diag=""):
    lo, hi = r["att"] - 1.96 * r["se"], r["att"] + 1.96 * r["se"]
    return {"diseno": diseno, "hipotesis": hip, "resultado": resultado, "especificacion": espec, "beta": r["att"],
            "se": r["se"], "ic95_lo": lo, "ic95_hi": hi, "p": r.get("p_boot", r.get("p_normal")),
            "p_normal": r.get("p_normal"), "N_unidades": n_t + n_c, "tratadas": n_t, "controles": n_c, "periodos": T,
            "confirmatoria": conf, "diagnosticos": diag}


def permutacion(Yv: np.ndarray, g: np.ndarray, att_real: float, seed: int) -> float:
    """Prueba de aleatorización de Fisher (addendum A1.2): se permutan las etiquetas de cohorte (tamaños reales) sobre
    el conjunto tratados + nunca tratados; p = proporción de |ATT*| ≥ |ATT real|."""
    rng = np.random.default_rng(seed)
    ats = []
    for _ in range(NPERM):
        ats.append(H.cs(Yv, rng.permutation(g), B=2)["att"])
    return float((np.sum(np.abs(ats) >= abs(att_real)) + 1) / (len(ats) + 1))


def pruebas(Yv, g, r, nombre, seed, desplaz=4, e_lo=-8):
    w_pre, p_pre, gl = H.pretendencias(r, e_lo, -2)
    # Honest DiD pre-registrado: IC de Rambachan y Roth (magnitudes relativas; contraste LF de ARP, unión de piezas)
    # (revisión F3, hallazgo 1). La versión simplificada (sustitución) se conserva como complemento.
    ic1 = H.honest_rr(r, 1.0, seed=seed)
    ic05 = H.honest_rr(r, 0.5, seed=seed)
    ruptura = H.honest_rr_ruptura(r, seed=seed)
    s1 = H.honest_rm(r, 1.0)
    # placebo de fecha: falso tratamiento `desplaz` periodos antes con la muestra previa al primer tratamiento
    g_min = int(np.nanmin(g[np.isfinite(g)]))
    Ypre = Yv[:, :g_min]
    gf = np.where(np.isfinite(g), g - desplaz, np.inf)
    rf = H.cs(Ypre, gf, B=B, seed=seed) if g_min - desplaz >= 1 else {"att": np.nan, "p_boot": np.nan}
    p_perm = permutacion(Yv, g, r["att"], seed)
    return {"prueba_diseno": nombre, "pretend_wald": w_pre, "pretend_p": p_pre, "pretend_gl": gl,
            "honest_M1_lo": ic1[0], "honest_M1_hi": ic1[1], "honest_M05_lo": ic05[0], "honest_M05_hi": ic05[1],
            "honest_Mbar_ruptura": ruptura, "honest_simplificado_M1_lo": s1[0], "honest_simplificado_M1_hi": s1[1],
            "honest_simplificado_ruptura": H.honest_ruptura(r), "placebo_fecha_att": rf["att"], "placebo_fecha_p": rf.get("p_boot"),
            "permutacion_etiquetas_p": p_perm}


def es_tabla(r, diseno, resultado, t_cero):
    return [{"diseno": diseno, "resultado": resultado, "e": e, "att_e": v[0], "se": v[1], "periodo_e0": t_cero}
            for e, v in sorted(r["es"].items())] + [{"diseno": diseno, "resultado": resultado, "e": -1, "att_e": 0.0, "se": 0.0, "periodo_e0": t_cero}]


def per(t: int) -> str:
    return f"{t // 4}T{t % 4 + 1}"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    q = P.incasol("T")
    tr = P.tratamientos_cat()
    ley = set(tr[tr.ley11].cod)
    zt = tr.dropna(subset=["zt_t0"]).set_index("cod").zt_t0
    pob = P.padron_nac("municipio")
    pob = pob[(pob.nacionalidad == "Total") & (pob.anio == 2022)].set_index("cod_municipio").poblacion
    tabla, es_rows, pr_rows = [], [], []
    resultados = {"renta_media": "log renta media de contratos nuevos", "contratos": "log contratos nuevos"}

    # ------------------------------------------------------------------------------------------- D1a
    t_ini, t_fin = 2022 * 4 + 1, 2026 * 4 + 0
    for var, nombre in resultados.items():
        conf = var == "renta_media"          # addendum A1.1: H1a-contratos es exploratoria
        hip = "H1a-renta" if conf else "H1a-contratos (exploratoria)"
        W = matriz(q, var, t_ini, t_fin)
        W = W[~(W.index.isin(ley) & ~W.index.isin(zt.index))]      # fuera: Ley 11/2020 sin zona tensionada
        g = np.array([zt[c] - t_ini if c in zt.index else np.inf for c in W.index], float)
        Yv = W.values
        n_t, n_c = int(np.isfinite(g).sum()), int((~np.isfinite(g)).sum())
        r = H.cs(Yv, g, B=B)
        tabla.append(fila("D1a", hip, nombre, "CS nunca tratados (principal)", r, n_t, n_c, Yv.shape[1], conf))
        REG.log("v9-D1a", f"{hip}-CS", f"{var}~CS(nunca)", per(t_ini), per(t_fin), n_t + n_c, np.nan, np.nan, np.nan,
                coef_interes=r["att"], p_interes=r["p_boot"], notas="principal")
        es_rows += es_tabla(r, "D1a", nombre, "2024T2/2024T4")
        pr = pruebas(Yv, g, r, f"D1a {nombre}", P.SEED)
        pr_rows.append(pr)
        # alternativas
        rb = H.bjs(Yv, g, B=199)
        tabla.append(fila("D1a", hip, nombre, "BJS imputación", rb, n_t, n_c, Yv.shape[1], False))
        rd = H.dcdh(Yv, g, B=B)
        tabla.append(fila("D1a", hip, nombre, "dCDH DID_l (aún no tratados)", rd, n_t, n_c, Yv.shape[1], False))
        r2 = H.cs(Yv[:, :-1], g, B=B)
        tabla.append(fila("D1a", hip, nombre, "CS ventana hasta 2025T4", r2, n_t, n_c, Yv.shape[1] - 1, False))
        cont = q[(q.t == t_ini)].set_index("cod").contratos.reindex(W.index).fillna(1).values
        r3 = H.cs(Yv, g, B=B, w=cont)
        tabla.append(fila("D1a", hip, nombre, "CS ponderado por contratos de 2022T2", r3, n_t, n_c, Yv.shape[1], False))
        sinb = W.index != "08019"
        r4 = H.cs(Yv[sinb], g[sinb], B=B)
        tabla.append(fila("D1a", hip, nombre, "CS sin Barcelona", r4, int(np.isfinite(g[sinb]).sum()), n_c, Yv.shape[1], False))
        # heterogeneidad (exploratoria): tamaño y cohorte
        pobw = pob.reindex(W.index).values
        med = np.nanmedian(pobw[np.isfinite(g)])
        for etiqueta, m in (("tamaño > mediana", (pobw > med) | ~np.isfinite(g)), ("tamaño ≤ mediana", (pobw <= med) | ~np.isfinite(g))):
            rh = H.cs(Yv[m], g[m], B=B)
            tabla.append(fila("D1a", hip, nombre, f"heterogeneidad: {etiqueta}", rh, int(np.isfinite(g[m]).sum()), n_c, Yv.shape[1], False))
        for gg in sorted(set(g[np.isfinite(g)])):
            m = (g == gg) | ~np.isfinite(g)
            rh = H.cs(Yv[m], g[m], B=B)
            tabla.append(fila("D1a", hip, nombre, f"heterogeneidad: cohorte {per(int(gg) + t_ini)}", rh, int((g == gg).sum()), n_c, Yv.shape[1], False))
        for x in tabla[-9:]:
            REG.log("v9-D1a", f"{hip}-{x['especificacion']}", var, per(t_ini), per(t_fin), x["N_unidades"], np.nan, np.nan,
                    np.nan, coef_interes=x["beta"], p_interes=x["p"], notas="alternativa/heterogeneidad")

    # ------------------------------------------------------------------------------------------- D1b
    t_ini, t_fin = 2019 * 4 + 0, 2022 * 4 + 0
    t0 = 2020 * 4 + 3
    a = P.incasol("A")
    for var, nombre in resultados.items():
        conf = var == "renta_media"
        hip = "H1b-renta" if conf else "H1b-contratos (exploratoria)"
        W = matriz(q, var, t_ini, t_fin)
        g = np.array([t0 - t_ini if c in ley else np.inf for c in W.index], float)
        Yv = W.values
        n_t, n_c = int(np.isfinite(g).sum()), int((~np.isfinite(g)).sum())
        r = H.cs(Yv, g, B=B)
        tabla.append(fila("D1b", hip, nombre, "CS nunca tratados (principal)", r, n_t, n_c, Yv.shape[1], conf))
        REG.log("v9-D1b", f"{hip}-CS", f"{var}~CS(nunca)", per(t_ini), per(t_fin), n_t + n_c, np.nan, np.nan, np.nan,
                coef_interes=r["att"], p_interes=r["p_boot"], notas="principal")
        es_rows += es_tabla(r, "D1b", nombre, "2020T4")
        pr_rows.append(pruebas(Yv, g, r, f"D1b {nombre}", P.SEED, e_lo=-7))
        rb = H.bjs(Yv, g, B=199)
        tabla.append(fila("D1b", hip, nombre, "BJS imputación", rb, n_t, n_c, Yv.shape[1], False))
        fin_alt = (2021 * 4 + 2) - t_ini + 1
        r2 = H.cs(Yv[:, :fin_alt], g, B=B)
        tabla.append(fila("D1b", hip, nombre, "CS fin alternativo 2021T3 (fecha de data/raw/v3)", r2, n_t, n_c, fin_alt, False))
        keep = [j for j in range(Yv.shape[1]) if (t_ini + j) not in (2020 * 4 + 1, 2020 * 4 + 2)]
        g_k = np.array([keep.index(int(x)) if np.isfinite(x) else np.inf for x in g], float)
        r3 = H.cs(Yv[:, keep], g_k, B=B)
        tabla.append(fila("D1b", hip, nombre, "CS sin 2020T2-2020T3 (confinamiento)", r3, n_t, n_c, len(keep), False))
        cont = q[(q.t == t_ini)].set_index("cod").contratos.reindex(W.index).fillna(1).values
        r4 = H.cs(Yv, g, B=B, w=cont)
        tabla.append(fila("D1b", hip, nombre, "CS ponderado por contratos de 2019T1", r4, n_t, n_c, Yv.shape[1], False))
        sinb = W.index != "08019"
        r5 = H.cs(Yv[sinb], g[sinb], B=B)
        tabla.append(fila("D1b", hip, nombre, "CS sin Barcelona", r5, int(np.isfinite(g[sinb]).sum()), n_c, Yv.shape[1], False))
        # anual 2014-2021 sin 2020; 2021 tratado
        WA = a[(a.anio >= 2014) & (a.anio <= 2021) & (a.anio != 2020)].pivot_table(index="cod", columns="anio", values=var)
        WA = np.log(WA[(WA > 0).all(1)].dropna())
        gA = np.array([list(WA.columns).index(2021) if c in ley else np.inf for c in WA.index], float)
        r6 = H.cs(WA.values, gA, B=B, e_min=-6)
        tabla.append(fila("D1b", hip, nombre, "CS anual 2014-2021 (sin 2020)", r6, int(np.isfinite(gA).sum()),
                          int((~np.isfinite(gA)).sum()), WA.shape[1], False,
                          diag=f"pretend p = {H.pretendencias(r6, -6, -2)[1]:.3f}"))
        for x in tabla[-6:]:
            REG.log("v9-D1b", f"{hip}-{x['especificacion']}", var, per(t_ini), per(t_fin), x["N_unidades"], np.nan, np.nan,
                    np.nan, coef_interes=x["beta"], p_interes=x["p"], notas="alternativa")

    # ------------------------------------------------------------------------------------------- D1c (exploratorio)
    e = P.emal()
    pv = P.tratamientos_pv().set_index("cod").zt_t0
    t_ini, t_fin = 2016 * 4, 2025 * 4 + 3
    for var, nombre in resultados.items():
        W = matriz(e, var, t_ini, t_fin)
        g = np.array([pv[c] - t_ini if c in pv.index and pv[c] <= t_fin else np.inf for c in W.index], float)
        r = H.cs(W.values, g, control="aun_no", B=B, e_min=-8, e_max=4)
        tabla.append(fila("D1c", "exploratoria", nombre, "CS aún no tratados (EMAL)", r, int(np.isfinite(g).sum()),
                          int((~np.isfinite(g)).sum()), W.shape[1], False,
                          diag=f"pretend p = {H.pretendencias(r, -8, -2)[1]:.3f}; tratadas con efecto ≤ 2025T4"))
        es_rows += es_tabla(r, "D1c", nombre, "escalonado 2025T1-2025T4")
        REG.log("v9-D1c", f"D1c-{var}", f"{var}~CS(aun_no)", per(t_ini), per(t_fin), W.shape[0], np.nan, np.nan, np.nan,
                coef_interes=r["att"], p_interes=r["p_boot"], notas="exploratorio")

    T = pd.DataFrame(tabla)
    PR = pd.DataFrame(pr_rows)
    ES = pd.DataFrame(es_rows).sort_values(["diseno", "resultado", "e"])
    T.to_csv(OUT / "tabla_d1.csv", index=False, float_format="%.5f")
    PR.to_csv(OUT / "pruebas.csv", index=False, float_format="%.5f")
    ES.to_csv(OUT / "estudio_eventos.csv", index=False, float_format="%.5f")
    for dis in ("D1a", "D1b", "D1c"):
        fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
        for j, (var, nombre) in enumerate(resultados.items()):
            s = ES[(ES.diseno == dis) & (ES.resultado == nombre)]
            ax[j].errorbar(s.e, s.att_e, yerr=1.96 * s.se, fmt="o", ms=3, capsize=2)
            ax[j].axhline(0, color="grey", lw=0.8)
            ax[j].axvline(-0.5, color="grey", ls="--", lw=0.8)
            ax[j].set_title(nombre, fontsize=9)
            ax[j].set_xlabel("trimestres desde el inicio del tratamiento")
        fig.suptitle(f"{dis}: estudio de eventos (CS; IC 95 %). Fuente: Incasòl/EMAL; elaboración propia", fontsize=9)
        fig.tight_layout()
        fig.savefig(OUT / f"fig_{dis.lower()}_eventos.png", dpi=130)
        plt.close(fig)
    principal = T[T.especificacion == "CS nunca tratados (principal)"]
    res = {"rama": "v9/d1", "pregunta": "¿Cambian la renta y los contratos nuevos con la contención de rentas (zonas tensionadas; Ley 11/2020)?",
           "capa": "pendiente de la clasificación (src/v9/f3_capas.py)", "datos": "Incasòl trimestral 2019T1-2026T1; EMAL 2016T1-2025T4",
           "N": int(principal.N_unidades.sum()), "metodo": "Callaway-Sant'Anna; BJS; dCDH; Honest DiD (RR, simplificado); bootstrap salvaje por municipio",
           "estimacion": principal[["diseno", "resultado", "beta"]].to_dict("records"),
           "ic95": principal[["ic95_lo", "ic95_hi"]].values.tolist(), "p_ajustado": "ver output/v9/f3/tabla_capas.csv",
           "nivel_evidencia": "pendiente", "diagnosticos": PR.to_dict("records"),
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "Incasòl no redistribuible: solo agregados."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    REG.flush()
    with pd.option_context("display.width", 250, "display.max_columns", 12):
        print(T[["diseno", "resultado", "especificacion", "beta", "se", "p", "N_unidades", "tratadas"]].to_string())
        print(PR.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
