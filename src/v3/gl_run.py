"""Réplica conceptual de García-López et al. (2020), Barcelona. C4. Determinista, sin red.
Uso: python src/v3/gl_run.py [--smoke]"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gl_data as g  # noqa: E402

from econ_utils import Registry, holm  # noqa: E402

OUT = g.RAIZ / "output/v3/GL"
OUT.mkdir(parents=True, exist_ok=True)
SMOKE = "--smoke" in sys.argv
OBJ, OBJ_EE = 0.035, 0.009   # WP 2019, Tabla 3 panel A col. 2 (log alquiler por 100 anuncios)
CIUDADES = {"Barcelona": "08019", "Madrid": "28079", "València": "46250", "Sevilla": "41091",
            "Málaga": "29067", "Palma": "07040"}
reg = Registry(OUT / "registro.csv")
rows = []


def clasifica(lo, hi, b, comparable):
    if not comparable:
        return "NO REPLICABLE", "unidades no homogéneas con el objetivo"
    if lo <= OBJ <= hi and b > 0:
        return "REPLICADO", "IC95 contiene 0,035 y mismo signo"
    if b > 0 and hi > 0 and lo > 0 and not lo <= OBJ <= hi:
        return "PARCIAL", "mismo signo, IC95 no contiene 0,035"
    if b > 0:
        return "PARCIAL", "mismo signo pero IC95 no contiene 0,035"
    return "NO REPLICADO", "signo distinto"


def estima(nombre, p, nivel, x, unidad, comparable, w=None):
    p = p.copy()
    if x == "vut_cien":
        p["vut_cien"] = p.vut / 100
    if p.codigo.nunique() < 5 or p.distrito.nunique() < 2:
        return None
    r = g.fe_cluster(p, "lnalq", [x], w=None if w is None else p[w].values)
    b, se, lo, hi, pv = (float(r[k][0]) if k != "n" else r[k] for k in ["b", "se", "lo", "hi", "p"])
    # unidades homogéneas: log-puntos por 100 anuncios (VUT), objetivo 0,035
    cl, crit = clasifica(lo, hi, b, comparable)
    rows.append(dict(especificacion=nombre, nivel=nivel, regresor=x, unidad_coef=unidad, N=r["n"],
                     unidades=int(p.codigo.nunique()), clusters=r["G"], objetivo=OBJ if comparable else np.nan,
                     coef=b, ee=se, ic95_lo=lo, ic95_hi=hi, p=pv, clasificacion=cl, criterio=crit))
    reg.log("GL", nombre, f"lnalq ~ {x} | FE unidad+año, cluster distrito", 2021, 2024, r["n"], np.nan, np.nan,
            np.nan, coef_interes=b, p_interes=pv, notas=f"{nivel}; {unidad}; {cl}")
    return r, p


def main():
    perd = {}
    prov = ["08"] if SMOKE else None
    ciudades = {"Barcelona": "08019"} if SMOKE else CIUDADES
    sec, perd["seccion_nacional" if not SMOKE else "seccion_08"] = g.carga("seccion", prov)
    dis, perd["distrito_nacional" if not SMOKE else "distrito_08"] = g.carga("distrito", prov)
    bcn = sec[sec.muni == "08019"]
    bcnd = dis[dis.codigo.str[:5] == "08019"]
    ex = {"distritos_BCN_incluidos": sorted(bcn.distrito.str[5:].unique().tolist())}
    # principal y variantes
    estima("GL1_bcn_seccion_vut100viv", bcn, "seccion", "vut100", "log-puntos por 100 VUT/100 viviendas (1 pp)", False)
    estima("GL2_bcn_distrito_vut100viv", bcnd, "distrito", "vut100", "log-puntos por 1 pp", False)
    estima("GL3_bcn_seccion_vut_cien", bcn, "seccion", "vut_cien", "log-puntos por 100 VUT (homogéneo)", True)
    estima("GL4_bcn_distrito_vut_cien", bcnd, "distrito", "vut_cien", "log-puntos por 100 VUT (homogéneo)", True)
    bw = bcn.copy()
    estima("GL5_bcn_seccion_vut_cien_pond_viv", bw, "seccion", "vut_cien", "log-puntos por 100 VUT, pond. viviendas",
           True, w="viv")
    # extensión
    for c, m in ciudades.items():
        if c == "Barcelona":
            continue
        if estima(f"EXT_{c}_seccion_vut100viv", sec[sec.muni == m], "seccion", "vut100", "log-puntos por 1 pp", False) is None:
            ex[f"{c}_no_estimable"] = "menos de 2 distritos no sellados con datos: sin clusters"
            continue
        estima(f"EXT_{c}_seccion_vut_cien", sec[sec.muni == m], "seccion", "vut_cien", "log-puntos por 100 VUT", True)
    out = estima("EXT_Espana_seccion_vut100viv", sec, "seccion", "vut100", "log-puntos por 1 pp", False)
    estima("EXT_Espana_seccion_vut_cien", sec, "seccion", "vut_cien", "log-puntos por 100 VUT", True)
    # diagnósticos: pretendencias (adelanto) y placebo por permutación en Barcelona
    diag = {}
    b = bcn.sort_values(["codigo", "anio"]).copy()
    b["lead"] = b.groupby("codigo").vut100.shift(-1)
    pl = b[b.anio <= 2023].dropna(subset=["lead"])
    r = g.fe_cluster(pl, "lnalq", ["vut100", "lead"], u="codigo", t="anio")
    diag["pretendencia_adelanto_BCN"] = dict(coef_lead=float(r["b"][1]), ee=float(r["se"][1]), p=float(r["p"][1]),
                                              nota="N=3 años; FE; el adelanto de VUT no debería predecir el alquiler")
    reg.log("GL", "GL_pretend_lead", "lnalq ~ vut100+lead", 2021, 2023, r["n"], np.nan, np.nan, np.nan,
            coef_interes=float(r["b"][1]), p_interes=float(r["p"][1]), notas="pretendencias")
    base = float(g.fe_cluster(bcn, "lnalq", ["vut100"])["b"][0])
    rng = np.random.default_rng(g.SEED)
    reps = 100 if SMOKE else 500
    cods = bcn.codigo.unique()
    sims = []
    for _ in range(reps):
        q = bcn.copy()
        perm = dict(zip(cods, rng.permutation(cods)))
        aux = bcn.set_index(["codigo", "anio"]).vut100
        q["vut100"] = [aux[(perm[c], a)] for c, a in zip(q.codigo, q.anio)]
        sims.append(float(g.fe_cluster(q, "lnalq", ["vut100"])["b"][0]))
    sims = np.array(sims)
    diag["placebo_permutacion_BCN"] = dict(reps=reps, coef_real=base, p_perm=float((np.abs(sims) >= abs(base)).mean()),
                                            sd_placebo=float(sims.std()))
    # Holm sobre los coeficientes principales
    df = pd.DataFrame(rows)
    ph = holm({r_["especificacion"]: r_["p"] for r_ in rows})
    df["p_holm"] = df.especificacion.map(ph)
    df.to_csv(OUT / "tabla_replicacion.csv", index=False)
    lines = ["# Réplica conceptual de García-López et al. (2020), Barcelona (C4, EXPLORATORIO)", "",
             "Objetivo: 0,035 (EE 0,009) log-puntos de alquiler por 100 anuncios (WP 2019, Tabla 3, panel A, col. 2). "
             "Propio: log mediana SERPAVI €/m2 (vivienda colectiva, stock IRPF) 2021-2024, VUT del INE (media anual de oleadas "
             "hasta 2024M11), FE de sección y año, cluster por distrito. Sin sellados v3 (distritos 09 y 10 de Barcelona "
             "excluidos) y sin 2026M05. Sin instrumento ni histórico 2012-2016: NO es réplica exacta.", "",
             df[["especificacion", "nivel", "unidad_coef", "N", "clusters", "coef", "ee", "ic95_lo", "ic95_hi", "p_holm",
                 "clasificacion", "criterio"]].round(4).to_markdown(index=False), "",
             "Las filas con unidades «por 1 pp» (VUT por 100 viviendas) no son homogéneas con el objetivo (por 100 anuncios): "
             "clasificación NO REPLICABLE por unidades. Las filas «por 100 VUT» sí son homogéneas (VUT INE ≈ anuncios, "
             "salvedad de definición).", "", "## Diagnósticos", "```", json.dumps(diag, indent=1), "```",
             "", f"Pérdidas de armonización (unidades): {json.dumps(perd)}", "", "REPLICADO con IC que incluye 0 (Madrid, València, Málaga) es una coincidencia por imprecisión, no confirmación.", "", f"Notas: {json.dumps(ex, ensure_ascii=False)}", "", "Nivel de evidencia: EXPLORATORIO (C4)."]
    (OUT / "replicacion.md").write_text("\n".join(lines))
    prin = df[df.especificacion == "GL3_bcn_seccion_vut_cien"].iloc[0]
    res = dict(rama="GL", capa="C4", pregunta="¿Reproduce el efecto de los alquileres turísticos sobre el alquiler (García-López 2020) en Barcelona 2021-2024?",
               datos="SERPAVI sección/distrito (stock IRPF) 2021-2024; VUT INE oleadas 2021M02-2024M11; Censo 2021; sellado v3 excluido",
               N=int(prin.N), metodo="MCO con FE de sección y año, cluster distrito (réplica conceptual, sin IV)",
               estimacion=float(prin.coef), ic95=[float(prin.ic95_lo), float(prin.ic95_hi)],
               p_ajustado=float(prin.p_holm), nivel_evidencia="EXPLORATORIO",
               diagnosticos=diag, fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None,
                                                   nota="no aplica: réplica de coeficiente"),
               clasificacion={r_.especificacion: r_.clasificacion for r_ in df.itertuples()},
               notas=f"Pérdidas armonización {perd}. {ex}. Smoke={SMOKE}")
    (OUT / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    reg.flush()
    print(df[["especificacion", "N", "coef", "ee", "ic95_lo", "ic95_hi", "clasificacion"]].round(4).to_string())
    print(diag)


if __name__ == "__main__":
    main()
