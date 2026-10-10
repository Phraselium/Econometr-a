"""A23 · Conciliación de precios de compra (A2) y de alquiler (A3). Determinista, sin red.

Uso: python3 src/v5/a23_run.py [--smoke]   (smoke: solo precio nacional y alquiler nacional, salida en smoke/)

Supuestos declarados:
  - Independencia: INE IPV y Notariado comparten fuente notarial (un grupo); MIVAU (tasación) y
    Registradores (inscripción) son grupos distintos (MIVAU-Notariado parcialmente independientes).
    Alquiler: IPC alquiler (INE, encuesta/administrativo) es un grupo; SERPAVI e IPVA son ambos AEAT-IRPF
    (un grupo); Incasòl y GVA (fianzas) son grupos propios.
  - Puente de precio en puntos de log sobre medias anuales 2015-2025. El factor «pesos CCAA comunes» es
    una recomputación (Laspeyres con pesos de importe 2015 de Registradores) -> C2 por el supuesto de pesos;
    desfase, nueva/usada y residuo -> C4.
  - Fianza = una mensualidad de renta (LAU art. 36); NO VERIFICADO en esta sesión, se declara como supuesto.
  - Tope legal de actualización: 2 % (RDL 6/2022), 3 % (2023 y 2024; RDL 8/2023). NO VERIFICADO el texto legal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import econ_utils  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
SMOKE = "--smoke" in sys.argv
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v5" / "A23" / ("smoke" if SMOKE else "")
TAB = OUT / "tablas"
TAB.mkdir(parents=True, exist_ok=True)
REG = econ_utils.Registry(OUT / "registro.csv")
GRUPO = {"INE_IPV": "notarial", "Notariado": "notarial", "MIVAU_tasado": "tasacion", "Registradores": "registral",
         "IPC_alquiler": "ine", "SERPAVI": "irpf", "IPVA_total": "irpf", "IPVA_existente": "irpf",
         "IPVA_nuevo": "irpf", "Incasol": "fianzas_cat", "GVA_fianzas": "fianzas_cv"}
TOL_NIVEL = 0.15
HECHOS: list[dict] = []
FECHA = "2026-10-10"
MP = {"Principado de Asturias": "Asturias", "C. Foral de Navarra": "Comunidad Foral de Navarra"}


def reg(fase, mid, formula, n, notas, ini="", fin="", coef=np.nan, p=np.nan):
    REG.log(fase, mid, formula, ini, fin, n, np.nan, np.nan, np.nan, coef_interes=coef, p_interes=p, notas=notas)


def hecho(id_, ind, valor, vmin, vmax, unidad, periodo, cob, fuentes, capa, fecha_dato):
    f = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)  # noqa: E731
    HECHOS.append({"id": id_, "indicador": ind, "valor": f(valor), "min": f(vmin), "max": f(vmax), "unidad": unidad,
                   "periodo": periodo, "cobertura": cob, "fuentes": fuentes, "capa": capa, "fecha_dato": fecha_dato})


def anual_trim(df, col, shift=0):
    """Media anual de una serie trimestral (años con 4 trimestres); shift en trimestres (ventana desplazada)."""
    d = df[["trimestre", col]].dropna().copy()
    d["t"] = d.trimestre.str[:4].astype(int) * 4 + d.trimestre.str[-1].astype(int) - 1
    s = d.set_index("t")[col]
    out = {}
    for y in range(2005, 2027):
        qs = [4 * y + k + shift for k in range(4)]
        if all(q in s.index for q in qs):
            out[y] = float(np.mean([s[q] for q in qs]))
    return pd.Series(out)


def rebase(s, base=2015):
    return 100 * s / s.loc[base]


def cum(s, a0, a1):
    return float(s.loc[a1] / s.loc[a0] - 1) if a0 in s.index and a1 in s.index else np.nan


def nucleo(c):
    """Mayor conjunto de fuentes con niveles acumulados a <=15 % entre sí; C1 si >=2 y >=2 grupos."""
    ks = sorted(c, key=lambda k: c[k])
    best: list[str] = []
    for i in range(len(ks)):
        for j in range(i, len(ks)):
            if (1 + c[ks[j]]) / (1 + c[ks[i]]) - 1 <= TOL_NIVEL and j - i + 1 > len(best):
                best = ks[i:j + 1]
    ok = len(best) >= 2 and len({GRUPO[k] for k in best}) >= 2
    return best, ok


# ====================================================================== A2 · PRECIO
def precio(nac, pan):
    res: dict = {}
    cgn = pd.read_csv(RAW / "pdf/notariado_cgn_extranjeros_semestral.csv")
    cgn = cgn[(cgn.serie == "precio_m2") & (cgn.categoria == "Total general")].copy()
    cgn["y"] = cgn.periodo.str[:4].astype(int)
    g = cgn.groupby("y").valor.agg(["mean", "count"])
    notar = g[g["count"] == 2]["mean"]
    rg = pd.read_csv(RAW / "pdf/registradores_opendata_anual.csv")

    def regs(serie, nivel="nacional"):
        x = rg[(rg.serie == serie) & (rg.nivel == nivel)]
        if nivel == "nacional":
            return pd.Series(x.valor.to_numpy(), index=x.periodo.astype(int).to_numpy())
        x = x.assign(ccaa=x.territorio.replace(MP), anio=x.periodo.astype(int))
        return x.pivot_table(index="anio", columns="ccaa", values="valor")

    pm2n = regs("compraventas_viv_pm2")
    imp = regs("compraventas_viv_imp")
    niv = {"INE_IPV": anual_trim(nac, "ipv"), "MIVAU_tasado": anual_trim(nac, "p_tasado"),
           "Registradores": pm2n, "Notariado": notar}
    idx = {k: rebase(s) for k, s in niv.items()}
    yrs = list(range(2015, 2026))
    pd.DataFrame({k: v.reindex(yrs) for k, v in idx.items()}).to_csv(TAB / "idx_precio_publicado_2015.csv", index_label="anio")
    c = {k: cum(v, 2015, 2025) for k, v in idx.items()}
    core_keys = ["MIVAU_tasado", "Notariado", "Registradores"]
    core_med = float(np.median([c[k] for k in core_keys]))
    res["cum_publicado"] = c
    res["core_med"] = core_med

    # ---- (b3) mix CCAA: pesos comunes de importe 2015 de Registradores
    ccs = sorted(pan.ccaa.unique())
    num = regs("compraventas_viv_num", "ccaa")[ccs]
    impc = regs("compraventas_viv_imp", "ccaa")[ccs]
    pm2c = regs("compraventas_viv_pm2", "ccaa")[ccs]
    val = num * impc
    pesos = {"importe2015": val.loc[2015] / val.loc[2015].sum(), "num2015": num.loc[2015] / num.loc[2015].sum(),
             "importe2025": val.loc[2025] / val.loc[2025].sum(),
             "importe_medio": (val.loc[2015] / val.loc[2015].sum() + val.loc[2025] / val.loc[2025].sum()) / 2}
    pd.DataFrame(pesos).to_csv(TAB / "pesos_ccaa.csv", index_label="ccaa")
    ccaa_idx = {"INE_IPV": pd.DataFrame({cc: anual_trim(pan[pan.ccaa == cc], "ipv") for cc in ccs}),
                "MIVAU_tasado": pd.DataFrame({cc: anual_trim(pan[pan.ccaa == cc], "p_tasado") for cc in ccs}),
                "Registradores": pm2c}
    cw = {}
    filas = []
    for wn, w in pesos.items():
        for k, df in ccaa_idx.items():
            rel = df.loc[2025, ccs] / df.loc[2015, ccs]
            cw[(wn, k)] = float((w * rel).sum() - 1)
            filas.append({"pesos": wn, "fuente": k, "cum_pesos_comunes_pct": 100 * cw[(wn, k)],
                          "cum_publicado_pct": 100 * c[k], "efecto_mix_ccaa_pp": 100 * (cw[(wn, k)] - c[k])})
    pd.DataFrame(filas).to_csv(TAB / "mix_ccaa_por_fuente.csv", index=False)
    res["cw"] = {f"{a}|{b}": v for (a, b), v in cw.items()}
    # Notariado sin desglose CCAA en el repositorio: se mantiene el publicado
    cw_core = {k: cw[("importe2015", k)] if k in ccaa_idx else c[k] for k in core_keys}
    cw_core_med = float(np.median(list(cw_core.values())))
    cw_ine = cw[("importe2015", "INE_IPV")]
    for wn in pesos:
        reg("puente", f"mix_ccaa_{wn}", "Laspeyres CCAA, 2015-2025, 3 fuentes", 17,
            "; ".join(f"{k}={100 * cw[(wn, k)]:.1f}%" for k in ccaa_idx), 2015, 2025, coef=cw[(wn, 'INE_IPV')])

    # ---- (b3bis) mix provincial dentro de CCAA (solo Registradores: MIVAU provincial cubre 43 de 50 provincias)
    rp_ = rg[(rg.nivel == "provincia") & (rg.serie.isin(["compraventas_viv_pm2", "compraventas_viv_num", "compraventas_viv_imp"]))]
    pp = rp_.assign(anio=rp_.periodo.astype(int)).pivot_table(index=["anio"], columns=["serie", "territorio"], values="valor")
    prov = [t for t in pp["compraventas_viv_pm2"].columns if not pp["compraventas_viv_pm2"].loc[[2015, 2025], t].isna().any()
            and not pp["compraventas_viv_num"].loc[2015, t] != pp["compraventas_viv_num"].loc[2015, t]]
    wp = (pp["compraventas_viv_num"].loc[2015, prov] * pp["compraventas_viv_imp"].loc[2015, prov])
    wp = wp / wp.sum()
    cum_prov = float((wp * pp["compraventas_viv_pm2"].loc[2025, prov] / pp["compraventas_viv_pm2"].loc[2015, prov]).sum() - 1)
    res["mix_provincial_registradores"] = {"cum_pesos_provincia_importe2015": cum_prov, "n_provincias": len(prov)}
    reg("puente", "mix_provincial_reg", "Laspeyres provincial Registradores", len(prov), f"{100 * cum_prov:.1f}% frente a publicado {100 * c['Registradores']:.1f}%",
        2015, 2025, coef=cum_prov)

    # ---- (c) desfase temporal del INE: ventana desplazada k trimestres
    lag = {}
    for k in (-2, -1, 0, 1, 2):
        s = anual_trim(nac, "ipv", shift=k)
        lag[k] = cum(s, 2015, 2025) if 2015 in s.index and 2025 in s.index else np.nan
    lagm = {k: v for k, v in lag.items() if not np.isnan(v)}
    pd.DataFrame({"desplazamiento_trimestres": list(lag), "cum_INE_2015_2025_pct": [100 * v for v in lag.values()]}
                 ).to_csv(TAB / "sensibilidad_desfase_ine.csv", index=False)
    lag_lo, lag_hi = min(lagm.values()) - lag[0], max(lagm.values()) - lag[0]

    # ---- (b1) nueva frente a usada
    ine_n, ine_u = anual_trim(nac, "ipv_nueva"), anual_trim(nac, "ipv_usada")
    c_n, c_u = cum(ine_n, 2015, 2025), cum(ine_u, 2015, 2025)
    et = pd.read_csv(RAW / "ine_v2_etdp_prov.csv")
    et = et[(et.nivel == "nacional") & et.desglose.isin(["nueva", "usada"])].copy()
    et["y"] = et.periodo.astype(str).str[:4].astype(int)
    sh = et.groupby(["y", "desglose"]).valor.sum().unstack()
    sh_new = sh["nueva"] / (sh["nueva"] + sh["usada"])
    eri = pd.read_csv(RAW / "pdf/registradores_eri_anuario.csv")
    eri = eri[(eri.nivel == "nacional") & (eri.periodo == 2025)].drop_duplicates(["serie"])
    pn = float(eri[eri.serie == "precio_m2_viv_nueva"].valor.iloc[0])
    pu = float(eri[eri.serie == "precio_m2_viv_usada"].valor.iloc[0])
    prem = pn / pu - 1
    mix_nu = (sh_new.loc[2025] - sh_new.loc[2015]) * prem   # variación aprox. de la media de pm2 por el cambio de peso (en log aprox.)
    pd.DataFrame({"cuota_nueva_etdp": sh_new.reindex(yrs), "ine_ipv_nueva_idx": rebase(ine_n).reindex(yrs),
                  "ine_ipv_usada_idx": rebase(ine_u).reindex(yrs)}).to_csv(TAB / "nueva_usada.csv", index_label="anio")
    reg("puente", "nueva_usada", "Δcuota nueva × prima nueva/usada (Registradores 2025)", 11,
        f"Δcuota={100 * (sh_new.loc[2025] - sh_new.loc[2015]):.2f} pp; prima={100 * prem:.1f}%; efecto={100 * mix_nu:.2f} pp",
        2015, 2025, coef=mix_nu)

    # ---- (b2) tamaño implícito (Registradores): superficie = importe medio / pm2
    sup = imp / pm2n
    d_sup = cum(sup, 2015, 2025)
    c_imp = cum(imp, 2015, 2025)
    pd.DataFrame({"pm2": pm2n.reindex(yrs), "importe_medio_vivienda": imp.reindex(yrs),
                  "superficie_implicita_m2": sup.reindex(yrs)}).to_csv(TAB / "tamano_implicito_registradores.csv", index_label="anio")

    # ---- puente en puntos porcentuales acumulados (log aditivo, luego reconvertido)
    L = lambda x: float(np.log1p(x))  # noqa: E731
    e = lambda x: float(np.expm1(x))  # noqa: E731
    p0 = c["INE_IPV"]
    l1 = L(cw_ine)
    p1 = e(l1)
    l2 = l1 + L(mix_nu) if False else l1 + mix_nu   # prima x Δcuota actúa sobre fuentes de media por m2
    p2 = e(l2)
    # desfase: efecto central 0 (rango en la tabla)
    l3 = l2
    l_core_cw = L(cw_core_med)
    residuo = l_core_cw - l3
    p4 = e(l_core_cw)
    p5 = core_med
    pasos = [
        ("0", "IPV INE publicado (media anual 2025 / 2015)", p0, np.nan, np.nan, "C1", "Hecho: INE IPV, 4 trimestres por año", "hecho"),
        ("1", "Pesos CCAA comunes (importe 2015) aplicados al IPV", p1 - p0, np.nan, np.nan, "C2",
         "Laspeyres con pesos de importe 2015 de Registradores; rango por pesos en mix_ccaa_por_fuente.csv", "composición geográfica"),
        ("2", "Nueva/usada: cambio de peso × prima de nueva (media de pm2)", p2 - p1, np.nan, np.nan, "C4",
         "Prima de nueva constante e igual a la de 2025; cuotas ETDP", "composición antigüedad"),
        ("3", "Desfase temporal (escritura/tasación/inscripción)", 0.0, lag_lo, lag_hi, "C4",
         "Efecto central 0 por construcción; rango = ventana INE desplazada ±2 trimestres", "cobertura/periodo"),
        ("4", "RESIDUO: método (hedónico frente a media/mediana de pm2), calidad, tamaño, cobertura y ruido",
         p4 - p2, np.nan, np.nan, "C4", "No descomponible con los datos del repositorio; es lo que falta hasta el núcleo con pesos comunes",
         "residuo"),
        ("5", "Pesos CCAA propios de las fuentes del núcleo (deshacer pesos comunes)", p5 - p4, np.nan, np.nan, "C2",
         "Mediana de MIVAU/Notariado/Registradores publicados frente a con pesos comunes (Notariado sin CCAA: sin cambio)", "composición geográfica"),
        ("6", "Mediana del núcleo publicada (MIVAU, Notariado, Registradores)", p5, np.nan, np.nan, "C1",
         "Cuantía C1 del núcleo en M7", "hecho"),
    ]
    tb = pd.DataFrame(pasos, columns=["paso", "descripcion", "pp_o_nivel", "rango_min_pp", "rango_max_pp", "capa", "supuesto", "factor"])
    for col in ("pp_o_nivel", "rango_min_pp", "rango_max_pp"):
        tb[col] = 100 * tb[col]
    # el acumulado se calcula en niveles, no sumando saltos en log (los saltos se reportan en pp de variación acumulada)
    tb["acumulado_pct"] = [100 * x for x in [p0, p1, p2, p2, p4, p5, p5]]
    tb.to_csv(TAB / "puente_precio.csv", index=False)
    res["puente"] = {"p0": p0, "p1": p1, "p2": p2, "p4": p4, "p5": p5, "residuo_pp": p4 - p2, "lag": lag,
                     "lag_rango_pp": [100 * lag_lo, 100 * lag_hi], "mix_nu_pp": 100 * mix_nu, "prima_nueva": prem,
                     "cum_ine_nueva": c_n, "cum_ine_usada": c_u, "d_sup": d_sup, "c_imp": c_imp,
                     "cuota_nueva": {"2015": float(sh_new.loc[2015]), "2025": float(sh_new.loc[2025])}}
    # por fuente: hueco frente al IPV con pesos comunes
    fu = []
    for k in core_keys:
        ck = cw_core[k]
        fu.append({"fuente": k, "cum_publicado_pct": 100 * c[k], "cum_pesos_comunes_pct": 100 * ck,
                   "hueco_vs_ine_pesos_comunes_pp": 100 * (cw_ine - ck)})
    pd.DataFrame(fu).to_csv(TAB / "puente_por_fuente.csv", index=False)
    reg("puente", "puente_total", "INE IPV -> mediana núcleo", 11,
        f"INE {100 * p0:.1f}% ; núcleo {100 * p5:.1f}% ; residuo {100 * (p4 - p2):.1f} pp", 2015, 2025, coef=p0 - p5)

    # ---- (d) índice frente a pm2 en nivel + triangulación + factor común
    band = pd.DataFrame({"min": pd.DataFrame(idx).reindex(yrs).min(axis=1), "max": pd.DataFrame(idx).reindex(yrs).max(axis=1),
                         "mediana_4": pd.DataFrame(idx).reindex(yrs).median(axis=1),
                         "min_nucleo": pd.DataFrame({k: idx[k] for k in core_keys}).reindex(yrs).min(axis=1),
                         "max_nucleo": pd.DataFrame({k: idx[k] for k in core_keys}).reindex(yrs).max(axis=1),
                         "mediana_nucleo": pd.DataFrame({k: idx[k] for k in core_keys}).reindex(yrs).median(axis=1)})
    dl = np.log(pd.DataFrame(idx).reindex(yrs)).diff().dropna()
    z = (dl - dl.mean()) / dl.std(ddof=1)
    u, sv, vt = np.linalg.svd(z.to_numpy(), full_matrices=False)
    load = vt[0] if vt[0].sum() > 0 else -vt[0]
    share = float(sv[0] ** 2 / (sv ** 2).sum())
    wl = load / load.sum()
    fgr = dl.to_numpy() @ wl                      # crecimiento común = media de dln ponderada por cargas del PC1
    fac = pd.Series(np.r_[0.0, np.cumsum(fgr)], index=yrs)
    band["factor_comun_idx"] = 100 * np.exp(fac)
    band.to_csv(TAB / "indice_triangulado.csv", index_label="anio")
    res["factor"] = {"var_explicada": share, "cargas": dict(zip(idx.keys(), map(float, load)))}
    res["band"] = {"min": min(c.values()), "max": max(c.values()), "mediana4": float(np.median(list(c.values())))}
    nuc, ok = nucleo(c)
    res["nucleo"] = {"fuentes": nuc, "c1": ok, "rango": [min(c[k] for k in nuc), max(c[k] for k in nuc)]}
    reg("tri", "nucleo_2015_2025", "mayor conjunto a <=15 % en nivel con >=2 grupos", 4, f"{nuc}; C1={ok}", 2015, 2025,
        coef=float(np.median([c[k] for k in nuc])))
    # pm2 nivel con ajuste de composición (pesos CCAA 2015 sobre pm2 Registradores)
    w = pesos["importe2015"]
    lev = pd.DataFrame({"pm2_registradores_publicado": pm2n.reindex(yrs),
                        "pm2_registradores_pesos_CCAA2015": [(w * pm2c.loc[y, ccs]).sum() for y in yrs],
                        "pm2_notariado": notar.reindex(yrs), "pm2_mivau_tasado": niv["MIVAU_tasado"].reindex(yrs)}, index=yrs)
    lev.to_csv(TAB / "precio_m2_nivel.csv", index_label="anio")
    res["nivel"] = {"reg_2015": float(pm2n.loc[2015]), "reg_2025": float(pm2n.loc[2025]),
                    "reg_cw_2025": float(lev.loc[2025, "pm2_registradores_pesos_CCAA2015"]),
                    "not_2015": float(notar.loc[2015]), "not_2025": float(notar.loc[2025]),
                    "mivau_2015": float(niv["MIVAU_tasado"].loc[2015]), "mivau_2025": float(niv["MIVAU_tasado"].loc[2025])}
    res["cum_nivel_reg_cw"] = float(lev.loc[2025, "pm2_registradores_pesos_CCAA2015"] / lev.loc[2015, "pm2_registradores_pesos_CCAA2015"] - 1)
    # figura
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for k, v in idx.items():
        ax[0].plot(yrs, v.reindex(yrs), marker="o", label=k)
    ax[0].fill_between(yrs, band["min_nucleo"], band["max_nucleo"], alpha=0.15, color="grey", label="banda núcleo")
    ax[0].set_title("Precio de compra, índices 2015=100")
    ax[0].legend(fontsize=7)
    ax[1].bar(range(len(tb)), tb["acumulado_pct"])
    ax[1].set_xticks(range(len(tb)))
    ax[1].set_xticklabels(tb["paso"])
    ax[1].set_title("Puente INE IPV -> núcleo (variación acumulada 2015-2025, %)")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_puente_precio.png", dpi=110)
    plt.close(fig)
    return res


# ====================================================================== A3 · ALQUILER
PROV_CCAA = {
    "Andalucía": ["Almería", "Cádiz", "Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla"],
    "Aragón": ["Huesca", "Teruel", "Zaragoza"], "Asturias": ["Asturias"], "Illes Balears": ["Balears, Illes"],
    "Canarias": ["Palmas, Las", "Santa Cruz de Tenerife"], "Cantabria": ["Cantabria"],
    "Castilla y León": ["Ávila", "Burgos", "León", "Palencia", "Salamanca", "Segovia", "Soria", "Valladolid", "Zamora"],
    "Castilla-La Mancha": ["Albacete", "Ciudad Real", "Cuenca", "Guadalajara", "Toledo"],
    "Cataluña": ["Barcelona", "Girona", "Lleida", "Tarragona"],
    "Comunitat Valenciana": ["Alicante/Alacant", "Castellón/Castelló", "Valencia/València"],
    "Extremadura": ["Badajoz", "Cáceres"], "Galicia": ["Coruña, A", "Lugo", "Ourense", "Pontevedra"],
    "Comunidad de Madrid": ["Madrid"], "Región de Murcia": ["Murcia"], "País Vasco": [],   # sin provincias en IPVA (Araba, Bizkaia, Gipuzkoa ausentes)
    "La Rioja": ["Rioja, La"], "Ceuta": ["Ceuta"], "Melilla": ["Melilla"]}
PROV2CC = {p: c for c, ps in PROV_CCAA.items() for p in ps}
# nombres SERPAVI provincial -> IPVA
SERP2IPVA = {"Alicante": "Alicante/Alacant", "Castellón": "Castellón/Castelló", "Valencia": "Valencia/València",
             "A Coruña": "Coruña, A", "Illes Balears": "Balears, Illes", "Las Palmas": "Palmas, Las",
             "Santa Cruz de Tenerife": "Santa Cruz de Tenerife", "La Rioja": "Rioja, La",
             "Asturias": "Asturias", "Principado de Asturias": "Asturias"}


def incasol_series():
    inc = pd.read_csv(RAW / "v3/incasol_fianzas_municipio_v3.csv.gz")
    inc = inc[inc.periodo.str.contains("gener-desembre")].copy()
    inc["y"] = inc.periodo.str[:4].astype(int)
    inc["tipo"] = np.where(inc.unidad == "EUR/mes", "renta", "n")
    inc["banda_k"] = inc.serie.str.replace(r"_(renta_media|n_contratos)_", "|", regex=True).str.split("|").str[1]
    inc = inc[inc.banda_k != "TOTAL_bandas"]
    w = inc[inc.tipo == "n"].pivot_table(index=["codigo", "y", "banda_k"], values="valor", aggfunc="sum")
    r = inc[inc.tipo == "renta"].pivot_table(index=["codigo", "y", "banda_k"], values="valor", aggfunc="mean")
    j = w.join(r, lsuffix="_n", rsuffix="_r", how="inner").dropna()
    j["nr"] = j.valor_n * j.valor_r
    gy = j.groupby("y")[["valor_n", "nr"]].sum()
    gm = j.groupby(["codigo", "y"])[["valor_n", "nr"]].sum()
    gm = gm[gm.valor_n > 0]
    return gy.nr / gy.valor_n, gy.valor_n, (gm.nr / gm.valor_n).unstack("y"), gm.valor_n.unstack("y")


def gva_series():
    g = pd.concat([pd.read_csv(RAW / f"v5/gva_fianzas_{y}.csv", sep=";") for y in range(2020, 2027)])
    g["importe"] = pd.to_numeric(g.importe_fianza, errors="coerce")
    g = g[(g.importe >= 100) & (g.importe <= 5000)].copy()   # descarta fianzas de <100 y >5000 (no residenciales o errores); se cuenta
    g["y"] = g.anyo_datos.astype(int)
    return g


def alquiler(nac, pan):
    res: dict = {}
    yrs = list(range(2015, 2026))
    ipc = rebase(anual_trim(nac, "ipc_alquiler"))
    srp = pd.read_csv(RAW / "pdf/serpavi_esp_agregado.csv")
    sp = {t: srp[srp.serie.str.endswith(f"pond_{t}")].set_index("periodo").valor for t in ("composicion_constante", "composicion_variable")}
    serp = rebase(sp["composicion_constante"])
    ip = pd.read_csv(RAW / "ine_v2_ipva.csv")
    ipn = ip[(ip.nivel == "nacional") & (ip.medida == "IPVA_indice")].pivot_table(index="periodo", columns="desglose", values="valor")
    ip_tot, ip_ex, ip_nu = ipn["Total"], ipn["Contrato existente"].dropna(), ipn["Nuevo contrato"].dropna()
    incm, incn, incmun, incmun_n = incasol_series()
    inc_idx = rebase(incm)
    g = gva_series()
    gm = g.groupby("y").importe.agg(["median", "mean", "count"])
    prov_w = g[g.y == 2020].groupby("cod_provincia").size()
    gp = g.groupby(["y", "cod_provincia"]).importe.median().unstack()
    gva_fix = (gp * (prov_w / prov_w.sum())).sum(axis=1)       # mediana provincial con pesos fijos 2020
    gva_med = gm["median"]
    pd.DataFrame({"IPC_alquiler": ipc.reindex(yrs), "SERPAVI_constante": serp.reindex(yrs), "IPVA_total": ip_tot.reindex(yrs),
                  "IPVA_existente_2015=100": ip_ex.reindex(yrs), "IPVA_nuevo_2015=100": ip_nu.reindex(yrs),
                  "Incasol_renta_media_eur": incm.reindex(yrs), "Incasol_idx2015": inc_idx.reindex(yrs),
                  "Incasol_n_contratos": incn.reindex(yrs)}).to_csv(TAB / "alquiler_series_nacional_cataluna.csv", index_label="anio")
    gout = pd.DataFrame({"mediana_eur": gm["median"], "media_eur": gm["mean"], "n_fianzas": gm["count"],
                         "mediana_provincial_pesos2020": gva_fix})
    gout.to_csv(TAB / "gva_fianzas_resumen.csv", index_label="anio")
    # ---- 1. stock frente a nuevos: variaciones
    cs = {"IPC_alquiler (2015-2025)": cum(ipc, 2015, 2025), "SERPAVI (2015-2024)": cum(serp, 2015, 2024),
          "IPVA_total (2015-2024)": cum(ip_tot, 2015, 2024)}
    ex24 = float(ip_ex.loc[2024] / 100 - 1)
    nu24 = float(ip_nu.loc[2024] / 100 - 1)
    comp = {"IPC_alquiler": cum(ipc, 2015, 2024), "SERPAVI": cum(serp, 2015, 2024), "IPVA_existente": ex24, "IPVA_total": cum(ip_tot, 2015, 2024)}
    nuc_s, ok_s = nucleo(comp)
    comp_n = {"IPVA_nuevo": nu24}
    res["stock"] = {"cum_2015_2025_ipc": cs["IPC_alquiler (2015-2025)"], "cum_2015_2024": comp, "nucleo_stock": nuc_s, "c1_cuantia_stock": ok_s}
    # nuevos: periodo común 2021-2024 (IPVA nuevo, Incasòl, GVA)
    nuevos = {"IPVA_nuevo": float(ip_nu.loc[2024] / ip_nu.loc[2021] - 1), "Incasol": cum(incm, 2021, 2024), "GVA_fianzas": cum(gva_med, 2021, 2024)}
    nuevos_cat_cv = {}
    # coherencia territorial 2021-2024: IPVA nuevo por provincia de CAT y CV frente a Incasòl y GVA
    ipv_prov = ip[(ip.nivel == "provincia") & (ip.tabla == 59005) & (ip.medida == "IPVA_indice")]
    pv = ipv_prov.pivot_table(index=["territorio", "periodo"], columns="desglose", values="valor")
    # pesos: contratos SERPAVI vigentes provinciales 2024
    sp_p = pd.read_csv(RAW / "pdf/serpavi_provincias.csv")
    spn = sp_p[(sp_p.variable == "n_contratos") & (sp_p.tipologia == "VC") & (sp_p.periodo == 2024)].copy()
    spn["terr"] = spn.nombre.replace(SERP2IPVA)
    wprov = spn.set_index("terr").valor
    tabp = []
    for p in sorted(pv.index.get_level_values(0).unique()):
        try:
            e24, n24 = pv.loc[(p, 2024), "Contrato existente"], pv.loc[(p, 2024), "Nuevo contrato"]
            e21, n21 = pv.loc[(p, 2021), "Contrato existente"], pv.loc[(p, 2021), "Nuevo contrato"]
        except KeyError:
            continue
        tabp.append({"provincia": p, "ccaa": PROV2CC.get(p, ""), "idx_existente_2024": e24, "idx_nuevo_2024": n24,
                     "brecha_nuevo_menos_existente_pct_2024": 100 * (n24 / e24 - 1),
                     "var_existente_2021_2024_pct": 100 * (e24 / e21 - 1), "var_nuevo_2021_2024_pct": 100 * (n24 / n21 - 1),
                     "contratos_serpavi_2024": float(wprov.get(p, np.nan))})
    tp = pd.DataFrame(tabp)
    tp.to_csv(TAB / "brecha_nuevo_stock_provincia.csv", index=False)
    cc_rows = []
    for cc, d in tp.groupby("ccaa"):
        if cc == "":
            continue
        wv = d.contratos_serpavi_2024.fillna(d.contratos_serpavi_2024.mean() if d.contratos_serpavi_2024.notna().any() else 1.0)
        wv = wv if wv.sum() > 0 else pd.Series(1.0, index=d.index)
        cc_rows.append({"ccaa": cc, "n_provincias": len(d),
                        "brecha_nuevo_menos_existente_pct_2024": float(np.average(d.brecha_nuevo_menos_existente_pct_2024, weights=wv)),
                        "var_existente_2021_2024_pct": float(np.average(d.var_existente_2021_2024_pct, weights=wv)),
                        "var_nuevo_2021_2024_pct": float(np.average(d.var_nuevo_2021_2024_pct, weights=wv))})
    tc = pd.DataFrame(cc_rows).sort_values("brecha_nuevo_menos_existente_pct_2024", ascending=False)
    tc.to_csv(TAB / "brecha_nuevo_stock_ccaa.csv", index=False)
    cat_p = tp[tp.ccaa == "Cataluña"]
    cv_p = tp[tp.ccaa == "Comunitat Valenciana"]
    wc = cat_p.contratos_serpavi_2024.fillna(1.0)
    wv_ = cv_p.contratos_serpavi_2024.fillna(1.0)
    nuevos_cat_cv = {"Cataluña": {"IPVA_nuevo": float(np.average(cat_p.var_nuevo_2021_2024_pct, weights=wc)) / 100,
                                  "Incasol": cum(incm, 2021, 2024),
                                  "IPVA_existente": float(np.average(cat_p.var_existente_2021_2024_pct, weights=wc)) / 100,
                                  "IPC_alquiler": cum(rebase(anual_trim(pan[pan.ccaa == "Cataluña"], "ipc_alquiler")), 2021, 2024)},
                     "Comunitat Valenciana": {"IPVA_nuevo": float(np.average(cv_p.var_nuevo_2021_2024_pct, weights=wv_)) / 100,
                                              "GVA_fianzas": cum(gva_med, 2021, 2024),
                                              "GVA_fianzas_pesos_prov": cum(gva_fix, 2021, 2024),
                                              "IPVA_existente": float(np.average(cv_p.var_existente_2021_2024_pct, weights=wv_)) / 100,
                                              "IPC_alquiler": cum(rebase(anual_trim(pan[pan.ccaa == "Comunitat Valenciana"], "ipc_alquiler")), 2021, 2024)}}
    # ---- extensión a 2025 donde hay datos (Incasòl y GVA)
    ext = {"Incasol_2015_2025": cum(incm, 2015, 2025), "Incasol_2021_2025": cum(incm, 2021, 2025),
           "GVA_mediana_2020_2025": cum(gva_med, 2020, 2025), "GVA_mediana_2021_2025": cum(gva_med, 2021, 2025),
           "GVA_pesos_prov_2020_2025": cum(gva_fix, 2020, 2025),
           "IPC_alquiler_CV_2020_2025": cum(rebase(anual_trim(pan[pan.ccaa == "Comunitat Valenciana"], "ipc_alquiler"), 2020), 2020, 2025)
           if 2020 in anual_trim(pan[pan.ccaa == "Comunitat Valenciana"], "ipc_alquiler").index else np.nan,
           "IPC_alquiler_CAT_2015_2025": cum(rebase(anual_trim(pan[pan.ccaa == "Cataluña"], "ipc_alquiler")), 2015, 2025)}
    res["nuevos"] = {"nacional_2021_2024": nuevos, "territorial_2021_2024": nuevos_cat_cv, "extension": ext}
    # dirección C1 de contratos nuevos por territorio: >=2 fuentes de grupos distintos, mismo signo, |var|>=5 %
    def dir_c1(d):
        ks = [k for k in d if k.split("_pesos")[0] in GRUPO and k.startswith(("IPVA_nuevo", "Incasol", "GVA"))]
        pos = [k for k in ks if d[k] >= 0.05 and not np.isnan(d[k])]
        return len({GRUPO[k.split("_pesos")[0]] for k in pos}) >= 2, pos
    res["dir_c1"] = {t: dir_c1(d) for t, d in nuevos_cat_cv.items()}
    res["cuantia_nuevos_territorial"] = {}
    for t, d in nuevos_cat_cv.items():
        dn = {k: v for k, v in d.items() if k in ("IPVA_nuevo", "Incasol", "GVA_fianzas")}
        nc, okc = nucleo(dn)
        res["cuantia_nuevos_territorial"][t] = {"nucleo": nc, "c1": okc, "rango": [min(dn[k] for k in nc), max(dn[k] for k in nc)] if nc else None}
    ipn_ok = bool(((ip_tot.reindex([2021, 2022, 2023, 2024]) >= ip_ex.reindex([2021, 2022, 2023, 2024]))
                   & (ip_tot.reindex([2021, 2022, 2023, 2024]) <= ip_nu.reindex([2021, 2022, 2023, 2024]))).all())
    res["ipva_base_coherente"] = ipn_ok
    reg("nuevos", "dir_cat", "IPVA nuevo + Incasòl 2021-2024", 2, str(nuevos_cat_cv["Cataluña"]), 2021, 2024)
    reg("nuevos", "dir_cv", "IPVA nuevo + GVA fianzas 2021-2024", 2, str(nuevos_cat_cv["Comunitat Valenciana"]), 2021, 2024)

    # ---- 2. descomposición del IPVA total: s_t (cuota implícita de contratos nuevos), contribuciones
    T, E, N = ip_tot.reindex([2021, 2022, 2023, 2024]), ip_ex.reindex([2021, 2022, 2023, 2024]), ip_nu.reindex([2021, 2022, 2023, 2024])
    s = (T - E) / (N - E)
    dT = T.loc[2024] - T.loc[2021]
    c_exist = float((1 - s).mean() * (E.loc[2024] - E.loc[2021]))
    c_new = float(s.mean() * (N.loc[2024] - N.loc[2021]))
    c_comp = float(dT - c_exist - c_new)
    pd.DataFrame({"IPVA_total": T, "IPVA_existente": E, "IPVA_nuevo": N, "cuota_implicita_nuevos": s,
                  "razon_nuevo_existente": N / E}).to_csv(TAB / "ipva_cuota_implicita.csv", index_label="anio")
    # rotación observada: fianzas / contratos SERPAVI vigentes
    spc = pd.read_csv(RAW / "pdf/serpavi_ccaa.csv")
    spc = spc[(spc.variable == "n_contratos") & (spc.tipologia == "VC")].pivot_table(index="periodo", columns="nombre", values="valor")
    rot_cat = (incn / spc["Cataluña"]).dropna()
    gcv = g.groupby("y").size()
    rot_cv = (gcv / spc["Comunitat Valenciana"]).dropna()
    pd.DataFrame({"Incasol_fianzas": incn, "SERPAVI_contratos_CAT": spc["Cataluña"], "rotacion_CAT": rot_cat,
                  "GVA_fianzas": gcv, "SERPAVI_contratos_CV": spc["Comunitat Valenciana"], "rotacion_CV": rot_cv}
                 ).to_csv(TAB / "rotacion_fianzas_sobre_stock.csv", index_label="anio")
    # ---- 3. tope legal frente a IPC (contrafáctico C2)
    h = pd.read_csv(RAW / "ecb_hicp_es.csv")
    h["y"] = h.periodo.str[:4].astype(int)
    hy = h.groupby("y").valor.mean()           # media anual de la tasa interanual (% )
    cap = {2022: 0.02, 2023: 0.03, 2024: 0.03}
    cf = float(E.loc[2021]); real = float(E.loc[2021])
    filas = []
    for y in (2022, 2023, 2024):
        real = float(E.loc[y])
        cf = cf * (1 + hy.loc[y] / 100)
        filas.append({"anio": y, "IPVA_existente_idx": float(E.loc[y]), "var_existente_pct": 100 * float(E.loc[y] / E.loc[y - 1] - 1),
                      "tope_legal_pct": 100 * cap[y], "HICP_ES_media_anual_pct": float(hy.loc[y]),
                      "idx_contrafactico_IPC_sin_tope": cf,
                      "nuevo_menos_existente_pct": 100 * float(N.loc[y] / E.loc[y] - 1)})
    tl = pd.DataFrame(filas)
    tl.to_csv(TAB / "tope_legal_contrafactico.csv", index=False)
    gap24 = float(N.loc[2024] / E.loc[2024] - 1)
    cf_gap = float(cf / real - 1)    # cuánto más habría subido el stock si TODOS los contratos se actualizasen al HICP
    explicacion = {
        "brecha_nuevo_existente_2024": gap24,
        "stock_IPVA_existente_2021_2024": float(E.loc[2024] / E.loc[2021] - 1),
        "nuevo_IPVA_2021_2024": float(N.loc[2024] / N.loc[2021] - 1),
        "total_IPVA_2021_2024": float(T.loc[2024] / T.loc[2021] - 1),
        "cuota_implicita_nuevos": {int(k): float(v) for k, v in s.items()},
        "contrib_total_pts_2021_2024": {"existentes": c_exist, "nuevos": c_new, "composicion_residuo": c_comp, "total": float(dT)},
        "tope_legal_contrafactico_pp": cf_gap,
        "HICP_acum_2022_2024": float(np.prod([1 + hy.loc[y] / 100 for y in (2022, 2023, 2024)]) - 1),
        "tope_acum_2022_2024": float(np.prod([1 + cap[y] for y in cap]) - 1),
        "rotacion_cat": {int(k): float(v) for k, v in rot_cat.items() if k >= 2015},
        "rotacion_cv": {int(k): float(v) for k, v in rot_cv.items()}}
    res["explicacion"] = explicacion
    reg("expl", "cuota_nuevos", "(T-E)/(N-E) IPVA 2021-2024", 4, str({int(k): round(float(v), 3) for k, v in s.items()}), 2021, 2024)
    reg("expl", "tope_contrafactico", "E_cf = E2021 * prod(1+HICP)", 3, f"stock +{100 * cf_gap:.1f}% adicional si todo se actualizase al HICP", 2022, 2024, coef=cf_gap)
    # ---- 4. doblar: municipios con >=+100 % (descriptivo)
    d = {}
    m2 = (incmun[2025] / incmun[2015]).dropna()
    ok2 = (incmun_n[2015] >= 30) & (incmun_n[2025] >= 30)
    m2 = m2[ok2.reindex(m2.index).fillna(False)]
    d["incasol_municipios_n"] = int(len(m2))
    d["incasol_municipios_dobles"] = int((m2 >= 2).sum())
    gmun = g.groupby(["cod_provincia", "cod_municipio", "y"]).importe.agg(["median", "count"]).unstack("y")
    gmed = gmun["median"]; gcnt = gmun["count"]
    okg = (gcnt[2020] >= 30) & (gcnt[2025] >= 30)
    gr = (gmed[2025] / gmed[2020])[okg]
    d["gva_municipios_n"] = int(len(gr))
    d["gva_municipios_dobles_2020_2025"] = int((gr >= 2).sum())
    res["municipal"] = d
    # ---- figura
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(yrs, ipc.reindex(yrs), label="IPC alquiler (stock)", marker="o")
    ax[0].plot(range(2015, 2025), serp.reindex(range(2015, 2025)), label="SERPAVI (stock IRPF)", marker="o")
    ax[0].plot(range(2015, 2025), ip_tot.reindex(range(2015, 2025)), label="IPVA total", marker="o")
    ax[0].plot([2021, 2022, 2023, 2024], ip_nu.reindex([2021, 2022, 2023, 2024]), label="IPVA contrato nuevo", marker="s")
    ax[0].plot([2021, 2022, 2023, 2024], ip_ex.reindex([2021, 2022, 2023, 2024]), label="IPVA contrato existente", marker="s")
    ax[0].plot(yrs, inc_idx.reindex(yrs), label="Incasòl (nuevos, Cataluña)", marker="^")
    ax[0].axhline(200, color="k", lw=0.5, ls=":")
    ax[0].set_title("Alquiler, índices 2015=100")
    ax[0].legend(fontsize=6)
    ax[1].plot(gm.index, gm["median"], marker="o")
    ax[1].set_title("GVA: mediana de fianza (EUR) por año de depósito (2026 parcial)")
    fig.tight_layout()
    fig.savefig(OUT / "fig2_alquiler.png", dpi=110)
    plt.close(fig)
    res["series"] = {"ipc": ipc, "serp": serp, "ip_tot": ip_tot, "ip_ex": ip_ex, "ip_nu": ip_nu, "inc": incm, "gva": gva_med, "gva_n": int(gm.loc[2020:2025, "count"].sum())}
    res["tablas"] = {"cc": tc}
    return res


# ====================================================================== salida
def pct(x):
    return None if x is None or np.isnan(x) else round(100 * float(x), 1)


def escribir(rp, ra):
    pb, ex = rp["puente"], ra["explicacion"]
    c = rp["cum_publicado"]
    hecho("A23-P1", "Precio de compra, variación acumulada 2015-2025, INE IPV", pct(c["INE_IPV"]), None, None, "%", "2015-2025 (media anual)",
          "España", "INE IPV (tabla 25171/80270)", "C4", "2025T4")
    hecho("A23-P2", "Precio de compra, núcleo MIVAU/Notariado/Registradores 2015-2025", pct(rp["core_med"]), pct(rp["nucleo"]["rango"][0]),
          pct(rp["nucleo"]["rango"][1]), "%", "2015-2025 (media anual)", "España",
          "MIVAU valor tasado; Notariado CGN; Registradores opendata", "C1" if rp["nucleo"]["c1"] else "C4", "2025 (anual)")
    hecho("A23-P3", "Residuo no identificado del puente INE IPV -> núcleo (sin descomponer; candidatos: método, calidad, tamaño, cobertura)", pct(pb["residuo_pp"]), None, None, "pp",
          "2015-2025", "España", "cálculo A23 (puente_precio.csv)", "C4", "2025T4")
    hecho("A23-P4", "Diferencia contable del IPV con pesos CCAA comunes", pct(pb["p1"] - pb["p0"]), None, None, "pp", "2015-2025", "17 CCAA",
          "INE IPV CCAA + Registradores (pesos)", "C4", "2025T4")
    hecho("A23-P5", "Diferencia contable por composición nueva/usada en la media de pm2", round(pb["mix_nu_pp"], 2), None, None, "pp", "2015-2025",
          "España", "INE ETDP + Registradores ERI 2025", "C4", "2025")
    hecho("A23-P6", "Precio por m2 Registradores nacional 2025", rp["nivel"]["reg_2025"], None, None, "EUR/m2", "2025", "España",
          "Registradores opendata", "C4", "2025")
    hecho("A23-P7", "Precio por m2 Notariado 2025", rp["nivel"]["not_2025"], None, None, "EUR/m2", "2025", "España", "Notariado CGN", "C4", "2025S2")
    s_ = ra["stock"]["cum_2015_2024"]
    # v5 (orquestador): el C1 de cuantía es el NÚCLEO (fuentes dentro de ±15 % en nivel); SERPAVI va aparte
    nuc_v = {k: s_[k] for k in ra["stock"]["nucleo_stock"] if k in s_}
    hecho("A23-A2", "Alquiler stock 2015-2024: núcleo IPC de alquiler e IPVA (contratos existentes y total; tolerancia ±15 % en nivel)", None,
          pct(min(nuc_v.values())), pct(max(nuc_v.values())), "%", "2015-2024", "España", "INE IPC (encuesta); INE IPVA (datos tributarios AEAT)",
          "C1" if ra["stock"]["c1_cuantia_stock"] else "C4", "2024")
    hecho("A23-A2b", "Alquiler stock 2015-2024: SERPAVI (renta declarada, composición constante), discrepante del núcleo", pct(s_["SERPAVI"]), None, None,
          "%", "2015-2024", "España", "Ministerio SERPAVI", "C4", "2024")
    nuv = ra["nuevos"]
    hecho("A23-A3", "Contratos nuevos, IPVA nuevo contrato 2015-2024 (base 2015=100)", pct(float(ra["series"]["ip_nu"].loc[2024] / 100 - 1)), None, None,
          "%", "2015-2024", "España", "INE IPVA (AEAT)", "C4", "2024")
    hecho("A23-A4", "Contratos nuevos, Incasòl renta media 2015-2025", pct(nuv["extension"]["Incasol_2015_2025"]), None, None, "%", "2015-2025",
          "Cataluña", "Incasòl fianzas", "C4", "2025")
    hecho("A23-A5", "Contratos nuevos, GVA mediana fianza 2020-2025", pct(nuv["extension"]["GVA_mediana_2020_2025"]), None, None, "%", "2020-2025",
          "Comunitat Valenciana", "GVA registro de fianzas", "C4", "2025")
    hecho("A23-A6", "Brecha nuevo menos existente (IPVA) 2024", pct(ex["brecha_nuevo_existente_2024"]), None, None, "%", "2024", "España",
          "INE IPVA (AEAT)", "C4", "2024")
    hecho("A23-A7", "Cuota implícita de contratos nuevos en el IPVA", pct(float(np.mean(list(ex["cuota_implicita_nuevos"].values())))),
          pct(min(ex["cuota_implicita_nuevos"].values())), pct(max(ex["cuota_implicita_nuevos"].values())), "%", "2021-2024", "España",
          "INE IPVA", "C4", "2024")
    hecho("A23-A8", "Subida adicional del stock si todo contrato se actualizase al HICP (sin tope)", pct(ex["tope_legal_contrafactico_pp"]), None, None,
          "%", "2022-2024", "España", "INE IPVA; BCE HICP; supuesto de tope", "C4", "2024")
    mp_ = rp["mix_provincial_registradores"]["cum_pesos_provincia_importe2015"]
    hecho("A23-P8", "Registradores con pesos provinciales de importe 2015 (52 provincias)", pct(mp_), None, None, "%", "2015-2025", "España",
          "Registradores opendata (provincia)", "C4", "2025")
    hecho("A23-P9", "Registradores con pesos CCAA de importe 2015", pct(rp["cw"]["importe2015|Registradores"]), None, None, "%", "2015-2025",
          "17 CCAA", "Registradores opendata (CCAA)", "C4", "2025")
    hecho("A23-P10", "Factor común de las 4 fuentes de precio: varianza explicada por el 1.er componente", pct(rp["factor"]["var_explicada"]), None, None,
          "%", "2016-2025 (dln anual)", "España", "INE, MIVAU, Notariado, Registradores", "C4", "2025T4")
    ct = ra["cuantia_nuevos_territorial"]
    hecho("A23-A9", "Contratos nuevos Cataluña 2021-2024: IPVA nuevo e Incasòl", pct(float(np.mean(ct["Cataluña"]["rango"]))), pct(ct["Cataluña"]["rango"][0]),
          pct(ct["Cataluña"]["rango"][1]), "%", "2021-2024", "Cataluña", "INE IPVA (AEAT); Incasòl", "C1" if ct["Cataluña"]["c1"] else "C4", "2024")
    cv_ = ct["Comunitat Valenciana"]
    hecho("A23-A10", "Contratos nuevos Comunitat Valenciana 2021-2024: IPVA nuevo y fianzas GVA", pct(float(np.mean(cv_["rango"]))), pct(cv_["rango"][0]),
          pct(cv_["rango"][1]), "%", "2021-2024", "Comunitat Valenciana", "INE IPVA (AEAT); GVA fianzas", "C1" if cv_["c1"] else "C4", "2024")
    hecho("A23-A11", "Rotación Cataluña: fianzas Incasòl / contratos vigentes SERPAVI", pct(ex["rotacion_cat"][2024]), pct(min(ex["rotacion_cat"].values())),
          pct(max(ex["rotacion_cat"].values())), "%", "2015-2024", "Cataluña", "Incasòl; SERPAVI", "C4", "2024")
    hecho("A23-A12", "Rotación Comunitat Valenciana: fianzas GVA / contratos vigentes SERPAVI", pct(ex["rotacion_cv"][2024]), pct(min(ex["rotacion_cv"].values())),
          pct(max(ex["rotacion_cv"].values())), "%", "2020-2024", "Comunitat Valenciana", "GVA; SERPAVI", "C4", "2024")
    hecho("A23-A13", "Municipios con renta media de fianzas x2 o más (Incasòl 2015-2025, >=30 fianzas)", ra["municipal"]["incasol_municipios_dobles"], None, None,
          "municipios", "2015-2025", f"{ra['municipal']['incasol_municipios_n']} municipios de Cataluña", "Incasòl", "C4", "2025")
    hecho("A23-A14", "Municipios con mediana de fianza x2 o más (GVA 2020-2025, >=30 fianzas)", ra["municipal"]["gva_municipios_dobles_2020_2025"], None, None,
          "municipios", "2020-2025", f"{ra['municipal']['gva_municipios_n']} municipios de la C. Valenciana", "GVA fianzas", "C4", "2025")
    json.dump(HECHOS, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)
    fichas(rp, ra)
    resultado(rp, ra)


def fichas(rp, ra):
    st, nv, ex = ra["stock"], ra["nuevos"], ra["explicacion"]
    cs = st["cum_2015_2024"]
    ct = ra["cuantia_nuevos_territorial"]
    ipn = ra["series"]["ip_nu"]
    lim_comun = ("Sin fianzas de Madrid, Euskadi ni Baleares (sin dato abierto localizado, docs/v5/fuentes_fallidas.md); IPVA nuevo contrato solo 2021-2024 "
                 "(2015=100 supuesto, coherente con el total); portales (Idealista, Fotocasa) fuera de la ficha (C4, sin cifra verificada); medias no excluyen "
                 "municipios concretos con subidas mayores.")
    f1 = {"id": "A23-V1", "variante": "stock de contratos", "tema": "Alquiler",
          "enunciado": "El alquiler se ha duplicado (variante stock: renta de los contratos vigentes).", "capa": "C1" if st["c1_cuantia_stock"] else "C4",
          "periodo": "2015-2025 (IPC alquiler) y 2015-2024 (SERPAVI, IPVA)", "fuente": "INE IPC alquiler; MIVAU-SERPAVI (AEAT-IRPF); INE IPVA",
          "magnitud": (f"Stock 2015-2025: IPC alquiler +{pct(st['cum_2015_2025_ipc'])} %. 2015-2024: IPC alquiler +{pct(cs['IPC_alquiler'])} %, IPVA contratos existentes "
                       f"+{pct(cs['IPVA_existente'])} %, IPVA total +{pct(cs['IPVA_total'])} %, SERPAVI (composición constante) +{pct(cs['SERPAVI'])} %. Ninguna fuente llega a +100 %."),
          "intervalo": f"[{pct(min(cs.values()))}; {pct(max(cs.values()))}] % (núcleo IPC/IPVA: {pct(min(cs[k] for k in st['nucleo_stock']))}-{pct(max(cs[k] for k in st['nucleo_stock']))} %; SERPAVI discrepante)",
          "cota": "Cuantía C1 en el núcleo (IPC alquiler, grupo INE; IPVA, grupo AEAT); SERPAVI comparte fuente (AEAT) con el IPVA y queda fuera del núcleo; se reportan ambos.",
          "literatura": "No aplica.", "veredicto": "CONTRADICHA",
          "regla": "Duplicarse exige +100 %; el stock mide las mismas viviendas o contratos vigentes y todas las medidas quedan por debajo.",
          "limites": "El stock sube menos que la renta de quien busca piso (ver variante contratos nuevos). " + lim_comun,
          "evidencia": ["output/v5/A23/tablas/alquiler_series_nacional_cataluna.csv", "output/v5/A23/tablas/ipva_cuota_implicita.csv"],
          "fecha_dato": "IPC 2025T4; SERPAVI e IPVA 2024"}
    f2 = {"id": "A23-V2", "variante": "contratos nuevos", "tema": "Alquiler",
          "enunciado": "El alquiler se ha duplicado (variante contratos nuevos: renta de quien firma ahora).", "capa": "C4",
          "periodo": "2015-2024 (IPVA nuevo), 2015-2025 (Incasòl, Cataluña), 2020-2025 (GVA, C. Valenciana)",
          "fuente": "INE IPVA contrato nuevo (AEAT); Incasòl fianzas; GVA registro de fianzas",
          "magnitud": (f"IPVA contrato nuevo 2015-2024 +{pct(ipn.loc[2024] / 100 - 1)} % (nacional). Incasòl renta media 2015-2025 +{pct(nv['extension']['Incasol_2015_2025'])} % (Cataluña). "
                       f"GVA mediana de fianza 2020-2025 +{pct(nv['extension']['GVA_mediana_2020_2025'])} % (C. Valenciana). 2021-2024: Cataluña {pct(ct['Cataluña']['rango'][0])}-{pct(ct['Cataluña']['rango'][1])} %, "
                       f"C. Valenciana {pct(ct['Comunitat Valenciana']['rango'][0])}-{pct(ct['Comunitat Valenciana']['rango'][1])} %. Municipios con renta de fianzas x2 o más: "
                       f"{ra['municipal']['incasol_municipios_dobles']} de {ra['municipal']['incasol_municipios_n']} (Cataluña, 2015-2025) y {ra['municipal']['gva_municipios_dobles_2020_2025']} de {ra['municipal']['gva_municipios_n']} (C. Valenciana, 2020-2025)."),
          "intervalo": f"[{pct(min(ipn.loc[2024] / 100 - 1, nv['extension']['Incasol_2015_2025']))}; {pct(max(ipn.loc[2024] / 100 - 1, nv['extension']['Incasol_2015_2025']))}] % en 2015-2024/25",
          "cota": "Dirección C1 en Cataluña y C. Valenciana (IPVA, Incasòl y GVA, grupos independientes, mismo signo); cuantía nacional C4 (fuentes de cobertura distinta).",
          "literatura": "No aplica.", "veredicto": "ANALIZADA, NO CONCLUYENTE",
          "regla": "Regla B5: la cuantía nacional de contratos nuevos es de fuente única (IPVA, C4), así que el veredicto nacional es como máximo ANALIZADA, NO CONCLUYENTE. Limitado a Cataluña y C. Valenciana (C1 en dirección y banda 2021-2024), la afirmación queda CONTRADICHA en promedio en 2021-2024. Las medias de contratos nuevos suben más que el stock, pero ninguna fuente alcanza +100 % en el periodo; la afirmación puede cumplirse en municipios o segmentos concretos fuera de las fuentes oficiales con dato.",
          "limites": lim_comun, "evidencia": ["output/v5/A23/tablas/brecha_nuevo_stock_ccaa.csv", "output/v5/A23/tablas/gva_fianzas_resumen.csv"],
          "fecha_dato": "IPVA 2024; Incasòl 2025; GVA 2025 (2026 parcial excluido)"}
    json.dump([f1, f2], open(OUT / "fichas_verificador.json", "w"), ensure_ascii=False, indent=1)


def resultado(rp, ra):
    pb, ex = rp["puente"], ra["explicacion"]
    r = {"rama": "A23",
         "pregunta": "A2: ¿por qué el IPV del INE (+80 % en 2015-2025) y el núcleo MIVAU/Notariado/Registradores (+44 % a +56 %) difieren y qué banda triangulada resulta? "
                     "A3: ¿por qué la renta del stock de contratos sube menos que la de los contratos nuevos y cuánto?",
         "capa": "C1 (núcleo de precio 2015-2025 y 2021-2025; núcleo de alquiler de stock; contratos nuevos 2021-2024 en Cataluña y C. Valenciana) / C4 (resto: fuentes únicas, reponderaciones, puente, desfase, nueva/usada, rotación, tope contrafactual)",
         "datos": "INE IPV (25171/80270), MIVAU valor tasado, Notariado CGN, Registradores opendata y ERI, INE ETDP, INE IPC alquiler, INE IPVA (59005/59058), SERPAVI, Incasòl, GVA fianzas 2020-2026 (nueva descarga), BCE HICP",
         "N": {"precio_anios": 11, "ccaa": 17, "provincias_registradores": rp["mix_provincial_registradores"]["n_provincias"],
               "fianzas_gva_2020_2025": int(ra["series"]["gva_n"]), "ipva_provincias": 48},
         "metodo": "Puente en log de la variación acumulada de medias anuales 2015-2025 con pesos comunes (Laspeyres, importe 2015); sensibilidad a pesos y al desfase; banda mínimo-máximo y mediana; factor común (1.er componente); descomposición del IPVA en existentes y nuevos; contrafactual de tope legal frente al HICP; rotación = fianzas / contratos SERPAVI.",
         "estimacion": {
             "precio": {"INE_IPV_pct": pct(pb["p0"]), "nucleo_pct": [pct(rp["nucleo"]["rango"][0]), pct(rp["nucleo"]["rango"][1])], "mediana_nucleo_pct": pct(rp["core_med"]),
                        "efecto_pesos_CCAA_en_INE_pp": pct(pb["p1"] - pb["p0"]), "efecto_nueva_usada_pp": round(pb["mix_nu_pp"], 3),
                        "desfase_rango_pp": [round(pb["lag_rango_pp"][0], 1), round(pb["lag_rango_pp"][1], 1)], "residuo_pp": pct(pb["residuo_pp"]),
                        "registradores_pesos_provincia_pct": pct(rp["mix_provincial_registradores"]["cum_pesos_provincia_importe2015"]),
                        "variacion_superficie_implicita_registradores_pct": pct(pb["d_sup"]), "factor_comun_var_explicada_pct": pct(rp["factor"]["var_explicada"])},
             "alquiler": {"stock_2015_2024_pct": {k: pct(v) for k, v in ra["stock"]["cum_2015_2024"].items()}, "ipc_2015_2025_pct": pct(ra["stock"]["cum_2015_2025_ipc"]),
                          "nuevo_2021_2024_pct": {k: pct(v) for k, v in ra["nuevos"]["nacional_2021_2024"].items()},
                          "brecha_nuevo_existente_2024_pct": pct(ex["brecha_nuevo_existente_2024"]),
                          "cuota_implicita_nuevos_pct": {k: pct(v) for k, v in ex["cuota_implicita_nuevos"].items()},
                          "contribuciones_IPVA_total_2021_2024_pts": {k: round(v, 2) for k, v in ex["contrib_total_pts_2021_2024"].items()},
                          "tope_contrafactico_stock_adicional_pct": pct(ex["tope_legal_contrafactico_pp"])}},
         "ic95": None, "p_ajustado": None, "nivel_evidencia": "ASOCIACIÓN / DESCRIPTIVO: conciliación contable, sin identificación causal; sin lenguaje causal",
         "diagnosticos": {"independencia": "INE IPV y Notariado: un grupo (fuente notarial); MIVAU y Notariado parcialmente independientes; Registradores independiente. IPVA y SERPAVI: un grupo (AEAT-IRPF); IPC alquiler, Incasòl y GVA: grupos propios.",
                          "nucleo_precio": rp["nucleo"], "banda_precio_total_pct": [pct(rp["band"]["min"]), pct(rp["band"]["max"])],
                          "nucleo_stock_alquiler": ra["stock"]["nucleo_stock"], "dir_c1_nuevos": {k: bool(v[0]) for k, v in ra["dir_c1"].items()},
                          "cuantia_nuevos_territorial": ra["cuantia_nuevos_territorial"], "ipva_base_2015_coherente": ra["ipva_base_coherente"],
                          "sensibilidad_pesos_ccaa": "ver tablas/mix_ccaa_por_fuente.csv (cuatro juegos de pesos)",
                          "rotacion": {"cat": ex["rotacion_cat"], "cv": ex["rotacion_cv"]},
                          "tests_y_fdr": "Sin contraste de hipótesis: todas las especificaciones están en registro.csv; Holm/BH no aplica"},
         "fuera_muestra": {"modelo": "no aplica (conciliación descriptiva, sin predicción)", "rmse": None, "dm_vs_ar4": None},
         "notas": ["El residuo del puente de precio (método hedónico frente a media/mediana de pm2, calidad, tamaño, cobertura) no se descompone con los datos del repositorio.",
                   "Los pesos CCAA aumentan la variación de MIVAU y Registradores y casi no cambian el IPV: la reponderación geográfica no reduce la diferencia INE frente a núcleo; la amplía.",
                   "Con pesos provinciales la variación de Registradores es mayor (+66,8 %) que la media publicada de pm2.",
                   "Cuota implícita de contratos nuevos del IPVA 14-18 % (supuesto: índices existente y nuevo en base 2015=100, agregación lineal); rotación observada Incasòl/SERPAVI 25-43 % y GVA/SERPAVI 13-16 %: definiciones distintas, se dan ambas.",
                   "Tope legal 2 % (2022) y 3 % (2023-2024) y fianza = una mensualidad: NO VERIFICADOS en esta sesión; el contrafactual es una cota C2 que supone actualización anual al HICP de todos los contratos.",
                   "Portales (Idealista, Fotocasa): sin cifra incluida (sin descarga verificable); solo serían C4.",
                   "GVA 2026 parcial (excluido de variaciones). Fianzas de Madrid, Euskadi y Baleares: sin datos abiertos localizados.",
                   "IPVA contrato nuevo/existente: AEAT-IRPF, 2021-2024 (48 provincias, sin País Vasco ni Navarra)."]}
    json.dump(r, open(OUT / "resultado.json", "w"), ensure_ascii=False, indent=1)


def main():
    nac = pd.read_csv(RAIZ / "data/processed/nacional_q.csv")
    pan = pd.read_csv(RAIZ / "data/processed/panel_ccaa_q.csv")
    rp = precio(nac, pan)
    ra = alquiler(nac, pan)
    escribir(rp, ra)
    json.dump({"precio": rp, "alquiler": {k: v for k, v in ra.items() if k not in ("series", "tablas")}},
              open(OUT / "calculos.json", "w"), ensure_ascii=False, indent=1, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))
    print(json.dumps({"precio": rp["puente"], "nucleo": rp["nucleo"], "factor": rp["factor"], "cum": rp["cum_publicado"]}, default=str, indent=1))
    print(json.dumps({k: v for k, v in ra.items() if k not in ("series", "tablas")}, default=str, indent=1)[:6000])


if __name__ == "__main__":
    main()
