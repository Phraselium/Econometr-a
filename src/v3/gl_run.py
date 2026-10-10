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


def viv_bcn():
    c = pd.read_csv(g.D / "ine_v3_censo2021_seccion_indicadores.csv.gz", usecols=["serie", "codigo", "valor"],
                    dtype={"codigo": str})
    c = c[(c.serie == "t18_1") & c.codigo.str.zfill(10).str.startswith("08019")]
    return float(c.valor.sum())


VIV = viv_bcn()
V_BARRIO = VIV / 73
T_PP = OBJ * V_BARRIO / 100 / 100            # log-puntos por 1 pp de VUT/parque
T_RANGO = (OBJ * 5000 / 1e4, OBJ * 20000 / 1e4)


def clasifica(lo, hi, b, T):
    if T is None:
        return "NO CLASIFICADA (informativa)", "unidad no homogénea con el objetivo"
    cont_T, cont_0 = lo <= T <= hi, lo <= 0 <= hi
    if cont_T and not cont_0:
        return "REPLICADO", "IC95 contiene T y excluye 0"
    if cont_T and cont_0:
        return "PARCIAL", "IC95 contiene T y 0 (no concluyente)"
    if not cont_0 and b > 0:
        return "PARCIAL", "excluye 0 con signo de T pero no contiene T (difiere la magnitud)"
    return "NO REPLICADO", "IC95 excluye T" + ("; signo contrario" if (not cont_0 and b < 0) else "")


def estima(nombre, p, nivel, x, unidad, comparable, w=None):
    p = p.copy()
    if x == "vut_cien":
        p["vut_cien"] = p.vut / 100
    if p.codigo.nunique() < 5 or p.distrito.nunique() < 2:
        return None
    r = g.fe_cluster(p, "lnalq", [x], w=None if w is None else p[w].values)
    b, se, lo, hi, pv = (float(r[k][0]) if k != "n" else r[k] for k in ["b", "se", "lo", "hi", "p"])
    # unidades homogéneas: log-puntos por 100 anuncios (VUT), objetivo 0,035
    T = T_PP if x == 'vut100' else None
    cl, crit = clasifica(lo, hi, b, T)
    rows.append(dict(especificacion=nombre, nivel=nivel, regresor=x, unidad_coef=unidad, N=r["n"],
                     unidades=int(p.codigo.nunique()), clusters=r["G"], objetivo=T if T is not None else np.nan,
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
             "Objetivo: 0,035 (EE 0,009) log-puntos por 100 anuncios en un barrio (WP 2019, Tabla 3, panel A, col. 2). "
             f"Conversión: T_pp = 0,035 x (viviendas por barrio/100)/100; parque Barcelona censo 2021 = {VIV:.0f} viviendas / 73 barrios = {V_BARRIO:.0f}; T_pp = {T_PP:.6f} (rango {T_RANGO[0]:.6f} a {T_RANGO[1]:.6f} con barrios de 5.000 y 20.000). Comparación principal: coeficiente por pp de VUT/parque. "
             "Propio: log mediana SERPAVI €/m2 (vivienda colectiva, stock IRPF) 2021-2024, VUT del INE (media anual de oleadas "
             "hasta 2024M11), FE de sección y año, cluster por distrito. Sin sellados v3 (distritos 09 y 10 de Barcelona "
             "excluidos) y sin 2026M05. Sin instrumento ni histórico 2012-2016: NO es réplica exacta.", "",
             df[["especificacion", "nivel", "unidad_coef", "N", "clusters", "coef", "ee", "ic95_lo", "ic95_hi", "p_holm",
                 "clasificacion", "criterio"]].round(4).to_markdown(index=False), "",
             "Las filas «por 100 VUT» en la sección son solo informativas (unidad no homogénea) y no se clasifican. Criterio: REPLICADO si IC95 contiene T y excluye 0; PARCIAL si contiene T y 0, o excluye 0 con signo de T sin contener T; NO REPLICADO en otro caso.", "",
             "## Límites", "SERPAVI es stock IRPF y amortigua los cambios, frente al precio de oferta de Idealista que usa GL. El periodo es 2021-2024, frente a 2012-2016. No hay instrumento. Es C4 (EXPLORATORIO).", "", "## Diagnósticos", "```", json.dumps(diag, indent=1), "```",
             "", f"Pérdidas de armonización (unidades): {json.dumps(perd)}", "", f"Notas: {json.dumps(ex, ensure_ascii=False)}", "", "Nivel de evidencia: EXPLORATORIO (C4)."]
    (OUT / "replicacion.md").write_text("\n".join(lines))
    prin = df[df.especificacion == "GL1_bcn_seccion_vut100viv"].iloc[0]
    res = dict(rama="GL", capa="C4", pregunta="¿Reproduce el efecto de los alquileres turísticos sobre el alquiler (García-López 2020) en Barcelona 2021-2024?",
               datos="SERPAVI sección/distrito (stock IRPF) 2021-2024; VUT INE oleadas 2021M02-2024M11; Censo 2021; sellado v3 excluido",
               N=int(prin.N), metodo="MCO con FE de sección y año, cluster distrito (réplica conceptual, sin IV)",
               estimacion=float(prin.coef), ic95=[float(prin.ic95_lo), float(prin.ic95_hi)],
               p_ajustado=float(prin.p_holm), nivel_evidencia="EXPLORATORIO",
               diagnosticos=diag, objetivo_T_pp=T_PP, T_pp_rango=T_RANGO, fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None,
                                                   nota="no aplica: réplica de coeficiente"),
               clasificacion={r_.especificacion: r_.clasificacion for r_ in df.itertuples()},
               notas=f"Pérdidas armonización {perd}. {ex}. Smoke={SMOKE}")
    (OUT / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    reg.flush()
    print(df[["especificacion", "N", "coef", "ee", "ic95_lo", "ic95_hi", "clasificacion"]].round(4).to_string())
    print(diag)


if __name__ == "__main__":
    main()
