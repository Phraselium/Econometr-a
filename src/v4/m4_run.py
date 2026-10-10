"""M4 · Parque frente a mercado (C1). Determinista, sin red. Uso: python3 src/v4/m4_run.py [--smoke]

Lee data/raw (incluidas las descargas de src/v4/m4_fetch.py en data/raw/v4). Escribe output/v4/M4/.
Sin estimaciones causales: hechos descriptivos y ratios. Toda cifra producida se anota en el Registry.
Supuestos declarados:
  - Ciudades: Madrid, Barcelona, Valencia, Sevilla, Zaragoza, Malaga y Bilbao (6 grandes + Valencia
    se interpreta como estas siete; decision registrada en docs/v4/decisiones.md).
  - Costa e islas: provincias con litoral y Balears/Canarias (lista COSTA); Ceuta y Melilla fuera.
  - Comprador PJ (ETDP) = persona fisica->PJ + PJ->PJ (titular = adquirente).
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import econ_utils  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
SMOKE = "--smoke" in sys.argv
OUT = RAIZ / "output" / "v4" / "M4" / ("smoke" if SMOKE else "")
TAB = OUT / "tablas"
TAB.mkdir(parents=True, exist_ok=True)
REG = econ_utils.Registry(OUT / "registro.csv")

CIUDADES = {"28079": "Madrid", "08019": "Barcelona", "46250": "València", "41091": "Sevilla",
            "50297": "Zaragoza", "29067": "Málaga", "48020": "Bilbao"}
COSTA = {"03", "04", "11", "12", "17", "18", "21", "29", "30", "43", "46", "08", "15", "27", "36", "33",
         "39", "48", "20", "35", "38", "07"}
ISLAS = {"07", "35", "38"}
UNIPROV_CCAA = {"asturias": "33", "balears": "07", "cantabria": "39", "madrid": "28", "murcia": "30",
                "navarra": "31", "rioja": "26"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    toks = re.sub(r"[^a-z0-9]+", " ", s).split()
    toks = [t for t in toks if t not in ("de", "del", "principado", "comunidad", "region", "foral", "la")] or toks
    return " ".join(sorted(toks))


def reg(fase, mid, formula, n, notas, ini="", fin="", coef=np.nan):
    REG.log(fase, mid, formula, ini, fin, n, np.nan, np.nan, np.nan, coef_interes=coef, notas=notas)


def jerarquia(codigos_nombres):
    """Asigna nivel (nacional/ccaa/provincia/municipio) por orden de aparicion: CCAA si su codigo
    es el siguiente codigo de CCAA esperado (01, 02, ...)."""
    out, esperado = {}, 1
    for cod, nom in codigos_nombres:
        if nom.startswith("Total Nacional"):
            out[(cod, nom)] = "nacional"
        elif len(cod) == 5:
            out[(cod, nom)] = "municipio"
        elif int(cod) == esperado and esperado <= 19:
            out[(cod, nom)] = "ccaa"
            esperado += 1
        else:
            out[(cod, nom)] = "provincia"
    return out


def parte(nombre, sufijos):
    for m in sorted(sufijos, key=len, reverse=True):
        if nombre.endswith(", " + m):
            return nombre[: -len(m) - 2], m
    return None, None


# ---------------------------------------------------------------- (a) STOCK
def stock():
    d = json.load(open(RAW / "v3" / "pa_aux" / "ine_t59531.json"))
    mets = ["Viviendas totales", "Viviendas vacías", "Viviendas con bajo consumo", "Viviendas de uso esporádico"]
    filas, orden = [], []
    for x in d:
        terr, m = parte(x["Nombre"], mets)
        if m is None or not x["Data"]:
            continue
        if terr == "Total Nacional":
            cod, nom = "ES", "Total Nacional"
        else:
            cod, nom = terr.split(" ", 1)
        v = x["Data"][0]["Valor"]
        filas.append((cod, nom, m, v))
        if m == "Viviendas totales":
            orden.append((cod if cod != "ES" else "ES", nom if cod != "ES" else "Total Nacional"))
    h = jerarquia([(c, n) for c, n in orden])
    df = pd.DataFrame(filas, columns=["codigo", "territorio", "metrica", "valor"])
    df["nivel"] = [h.get((c, n)) for c, n in zip(df.codigo, df.territorio)]
    if df.nivel.isna().any():
        df.loc[df.nivel.isna(), "nivel"] = df[df.nivel.isna()].apply(
            lambda r: "municipio" if len(r.codigo) == 5 else h.get((r.codigo, r.territorio), "provincia"), axis=1)
    w = df.pivot_table(index=["codigo", "territorio", "nivel"], columns="metrica", values="valor").reset_index()
    w = w.rename(columns={"Viviendas totales": "viv_total_consumo", "Viviendas vacías": "vacias",
                          "Viviendas con bajo consumo": "bajo_consumo", "Viviendas de uso esporádico": "esporadico"})
    # principal / no principal: Censo 2021 por municipio (59525); se agrega a provincia por prefijo
    c = pd.read_csv(RAW / "v3" / "ine_v3_censo2021_municipio_viviendas.csv", dtype={"codigo": str},
                    usecols=["serie", "valor", "codigo", "nivel"])
    cn = c[c.nivel == "nacional"].pivot_table(index="codigo", columns="serie", values="valor")
    cm = c[c.nivel == "municipio"].pivot_table(index="codigo", columns="serie", values="valor")
    cp = cm.groupby(cm.index.str[:2]).sum()
    # VUT INE (mayo 2026)
    v = pd.read_csv(RAW / "ine_v2_vut.csv", dtype={"codigo": str},
                    usecols=["periodo", "valor", "territorio", "nivel", "codigo", "medida"])
    v = v[(v.medida == "viviendas_turisticas") & (v.periodo == "2026M05")]
    vut_nac = float(v[v.nivel == "nacional"].valor.iloc[0])
    vp = v[(v.nivel == "provincia") & v.codigo.isin([f"{i:02d}" for i in range(1, 53)])]
    vp = vp.drop_duplicates("codigo").set_index("codigo").valor
    vm = v[v.nivel == "municipio"].groupby("territorio").valor.agg(["first", "count"])
    nac = w[w.nivel == "nacional"].iloc[0]
    fila_n = {"territorio": "España", "codigo": "ES", "nivel": "nacional",
              "viv_total_censo": cn.loc["ES", "V_TOTAL"], "principal": cn.loc["ES", "V_PRINCIPAL"],
              "no_principal": cn.loc["ES", "V_NOPRINCIPAL"], "vacias": nac.vacias, "esporadico": nac.esporadico,
              "bajo_consumo": nac.bajo_consumo, "vut_ine_2026M05": vut_nac}
    filas_p = []
    for _, r in w[w.nivel == "provincia"].iterrows():
        if SMOKE and len(filas_p) >= 5:
            break
        cod = r.codigo
        filas_p.append({"territorio": r.territorio, "codigo": cod, "nivel": "provincia",
                        "viv_total_censo": cp.V_TOTAL.get(cod, np.nan), "principal": cp.V_PRINCIPAL.get(cod, np.nan),
                        "no_principal": cp.V_NOPRINCIPAL.get(cod, np.nan), "vacias": r.vacias,
                        "esporadico": r.esporadico, "bajo_consumo": r.bajo_consumo,
                        "vut_ine_2026M05": vp.get(cod, np.nan), "costa_islas": cod in COSTA})
    filas_c = []
    for cod, nom in CIUDADES.items():
        r = w[w.codigo == cod]
        if r.empty:
            continue
        r = r.iloc[0]
        vn = {"València": "València", "Málaga": "Málaga"}.get(nom, nom)
        filas_c.append({"territorio": nom, "codigo": cod, "nivel": "municipio",
                        "viv_total_censo": cm.V_TOTAL.get(cod, np.nan), "principal": cm.V_PRINCIPAL.get(cod, np.nan),
                        "no_principal": cm.V_NOPRINCIPAL.get(cod, np.nan), "vacias": r.vacias,
                        "esporadico": r.esporadico, "bajo_consumo": r.bajo_consumo,
                        "vut_ine_2026M05": vm.loc[vn, "first"] if vn in vm.index and vm.loc[vn, "count"] == 1 else np.nan})
    res = {}
    for nombre, filas in (("nacional", [fila_n]), ("provincia", filas_p), ("ciudades", filas_c)):
        t = pd.DataFrame(filas)
        t["pct_principal"] = 100 * t.principal / t.viv_total_censo
        t["pct_vacias"] = 100 * t.vacias / t.viv_total_censo
        t["pct_esporadico"] = 100 * t.esporadico / t.viv_total_censo
        t["pct_vut"] = 100 * t.vut_ine_2026M05 / t.viv_total_censo
        t["ratio_vacias_esporadico_sobre_vut"] = (t.vacias + t.esporadico) / t.vut_ine_2026M05
        t["nota"] = ("Censo 2021 (59525; 59531 consumo electrico); VUT INE mayo 2026 (experimental) no suma: "
                     "es subconjunto de las viviendas del Censo en otra fecha")
        t.round(3).to_csv(TAB / f"stock_uso_{nombre}.csv", index=False)
        res[nombre] = t
        reg("stock", f"stock_uso_{nombre}", "tabla descriptiva", len(t), "C1 hecho; sin contraste")
    # contraste VUT: INE frente a registro autonomico (Comunitat Valenciana)
    g = pd.read_csv(RAW / "gva_vut_municipio.csv", dtype={"codigo": str},
                    usecols=["periodo", "serie", "valor", "ambito", "codigo"])
    g = g[g.serie.str.startswith("vut_stock_prov_")]
    ult = g.periodo.max()
    gv = g[g.periodo == ult].set_index("codigo").valor
    cmp = pd.DataFrame({"codigo": ["03", "12", "46"], "gva_registro_stock": [gv.get(c, np.nan) for c in ("03", "12", "46")],
                        "ine_vut_2026M05": [vp.get(c, np.nan) for c in ("03", "12", "46")]})
    cmp["periodo_gva"] = ult
    cmp.to_csv(TAB / "vut_ine_frente_registro_gva.csv", index=False)
    reg("stock", "vut_ine_vs_gva", "INE VUT vs registro GVA", 3, "dos metodos discrepan: se reportan ambos")
    return res, cmp


# ---------------------------------------------------------------- titularidad / tenencia
def tenencia():
    t = pd.read_csv(RAW / "v4" / "ine_v4_t59523.csv")
    ten = ["Total (régimen de tenencia)", "En propiedad", "En alquiler", "Otro régimen de tenencia"]
    rows = []
    for _, r in t.iterrows():
        mt = re.match(r"^(.*), (" + "|".join(map(re.escape, ten)) + r"), (Total \(tamaño de municipio\))$", r.serie_nombre)
        if mt:
            rows.append((mt.group(1), mt.group(2), r.valor))
    d = pd.DataFrame(rows, columns=["terr", "ten", "valor"])
    ordenados = list(dict.fromkeys(d.terr))
    cn = [("ES", x) if x.startswith("Total Nacional") else tuple(x.split(" ", 1)) for x in ordenados]
    h = jerarquia(cn)
    niv = {x: h[c] for x, c in zip(ordenados, cn)}
    w = d.pivot_table(index="terr", columns="ten", values="valor").reset_index()
    w["nivel"] = w.terr.map(niv)
    w = w.rename(columns={"Total (régimen de tenencia)": "total", "En propiedad": "propiedad",
                          "En alquiler": "alquiler", "Otro régimen de tenencia": "otro_cesion"})
    for k in ("propiedad", "alquiler", "otro_cesion"):
        w[f"pct_{k}"] = 100 * w[k] / w.total
    w["terr"] = w.terr.str.replace(r"^\d{2} ", "", regex=True)
    w["fuente"] = "INE Censo 2021, tabla 59523 (viviendas principales)"
    w = w[w.nivel.isin(["nacional", "provincia"])].sort_values(["nivel", "terr"])
    if SMOKE:
        w = w.head(6)
    # ciudades (59529)
    c = pd.read_csv(RAW / "v4" / "ine_v4_t59529.csv")
    c["cod"] = c.serie_nombre.str.slice(0, 5)
    c["ten"] = c.serie_nombre.str.rsplit(", ", n=1).str[-1]
    cw = c[c.cod.isin(CIUDADES)].pivot_table(index="cod", columns="ten", values="valor")
    cw = cw.rename(columns={"Total (régimen de tenencia)": "total", "En propiedad": "propiedad",
                            "En alquiler": "alquiler", "Otro régimen de tenencia": "otro_cesion"})
    cw["terr"] = [CIUDADES[i] for i in cw.index]
    cw["nivel"] = "municipio"
    for k in ("propiedad", "alquiler", "otro_cesion"):
        cw[f"pct_{k}"] = 100 * cw[k] / cw.total
    cw["fuente"] = "INE Censo 2021, tabla 59529 (viviendas principales)"
    out = pd.concat([w, cw.reset_index(drop=True)], ignore_index=True)
    out.round(3).to_csv(TAB / "tenencia_censo2021.csv", index=False)
    reg("titularidad", "tenencia_censo2021", "tabla descriptiva", len(out), "C1 (Censo 2021); no distingue arrendador")
    # EFF
    f = pd.read_csv(RAW / "v3" / "eff_tenencia_edad_v3.csv")
    f = f[f.serie.str.startswith("eff_pct_hogares_otras_propiedades")].copy()
    f["edad"] = f.serie.str.extract(r"edad=([^|]+)")[0]
    f = f[f.periodo == f.periodo.max()][["periodo", "edad", "valor", "fuente", "validado", "error_max"]]
    f.to_csv(TAB / "eff_otras_propiedades_edad.csv", index=False)
    reg("titularidad", "eff_otras_propiedades", "tabla descriptiva", len(f), "hogares, no personas juridicas; sin percentil")
    return out, f


# ---------------------------------------------------------------- (b) FLUJOS: personas juridicas
def flujo_pj():
    a = pd.read_csv(RAW / "v4" / "ine_v4_t50272.csv")
    a["anyo"] = a.fecha.str[:4].astype(int)
    a["par"] = a.serie_nombre.str.extract(r"Nacional\. (Persona \w+)\. (Persona \w+)\.").apply(
        lambda r: f"{r[0]}->{r[1]}", axis=1)
    w = a.pivot_table(index="anyo", columns="par", values="valor")
    w["suma_cuatro"] = w.sum(axis=1)
    w["pct_comprador_pj"] = w["Persona física->Persona jurídica"] + w["Persona jurídica->Persona jurídica"]
    w["pct_vendedor_pj"] = w["Persona jurídica->Persona física"] + w["Persona jurídica->Persona jurídica"]
    w["fuente"] = "INE ETDP tabla 50272 (compraventas de viviendas por transmitente y titular)"
    w.round(2).to_csv(TAB / "flujo_compraventas_comprador_pj_etdp.csv")
    m = pd.read_csv(RAW / "v4" / "ine_v4_t50256.csv")
    m["par"] = m.serie_nombre.str.extract(r"Nacional\. (Persona \w+)\. (Persona \w+)\.").apply(
        lambda r: f"{r[0]}->{r[1]}", axis=1)
    mw = m.pivot_table(index="fecha", columns="par", values="valor")
    mw["pct_comprador_pj"] = mw["Persona física->Persona jurídica"] + mw["Persona jurídica->Persona jurídica"]
    mw.round(2).to_csv(TAB / "flujo_compraventas_comprador_pj_etdp_mensual.csv")
    reg("flujos", "etdp_comprador_pj", "PF->PJ + PJ->PJ", len(w), "fuente unica -> C4 para el contraste con el stock",
        w.index.min(), w.index.max(), coef=float(w.pct_comprador_pj.iloc[-1]))
    # Incasol: contratos de fianza (sin tipo de arrendador)
    i = pd.read_csv(RAW / "v3" / "incasol_fianzas_municipio_v3.csv.gz", usecols=["periodo", "serie", "valor"])
    i = i[i.serie.str.contains("_n_contratos_") & i.periodo.str.endswith("gener-desembre")]
    i["anyo"] = i.periodo.str[:4].astype(int)
    ic = i.groupby("anyo").valor.sum().rename("contratos_fianza_cataluna").reset_index()
    ic["arrendador_tipo"] = "no disponible en la fuente (solo municipio, tramo de renda y periodo)"
    ic.to_csv(TAB / "flujo_alquiler_incasol_contratos.csv", index=False)
    reg("flujos", "incasol_contratos", "suma anual de contratos", len(ic), "sin tipo de arrendador")
    return w, mw, ic


# ---------------------------------------------------------------- compradores extranjeros
def anual_mivau():
    m = pd.read_csv(RAW / "mivau_transacciones_residencia.csv", usecols=["periodo", "serie", "valor", "territorio", "nivel"])
    m["var"] = m.serie.str.replace(r"_(nacional|ccaa_.*|provincia_.*|ciudad_autonoma_.*)$", "", regex=True)
    m["anyo"] = m.periodo.str[:4].astype(int)
    cnt = m.groupby(["var", "nivel", "territorio", "anyo"]).valor.agg(["sum", "count"]).reset_index()
    cnt = cnt[cnt["count"] == 4]
    return cnt


def extranjeros():
    cn = anual_mivau()
    nac = cn[cn.nivel == "nacional"].pivot_table(index="anyo", columns="var", values="sum")
    mv = pd.DataFrame({"mivau_total": nac.tx_residencia_total,
                       "mivau_ext_residentes": nac.tx_residencia_residentes_extranjeros,
                       "mivau_ext_no_residentes": nac.tx_residencia_no_residentes_extranjeros})
    mv["mivau_pct_ext"] = 100 * (mv.mivau_ext_residentes + mv.mivau_ext_no_residentes) / mv.mivau_total
    mv["mivau_pct_ext_residentes"] = 100 * mv.mivau_ext_residentes / mv.mivau_total
    mv["mivau_pct_ext_no_residentes"] = 100 * mv.mivau_ext_no_residentes / mv.mivau_total
    n = pd.read_csv(RAW / "pdf" / "notariado_cgn_extranjeros_semestral.csv")
    n = n[(n.serie == "op_viv_libre") & (n.territorio == "Espana")].copy()
    n["anyo"] = n.periodo.str[:4].astype(int)
    nw = n.pivot_table(index="anyo", columns="categoria", values="valor", aggfunc="sum")
    nt = pd.DataFrame({"notariado_total_viv_libre": nw["Total general"],
                       "notariado_pct_ext": 100 * nw["Extranjero"] / nw["Total general"],
                       "notariado_pct_ext_residentes": 100 * nw["Extranjero - Residente"] / nw["Total general"],
                       "notariado_pct_ext_no_residentes": 100 * nw["Extranjero - No residente"] / nw["Total general"]})
    # Registradores: publicado (nacional 2023-25) y derivado desde CCAA con pesos OpenData
    r = pd.read_csv(RAW / "pdf" / "registradores_eri_anuario.csv")
    rn = r[(r.serie == "viv_pct_compras_extranjeros") & (r.nivel == "nacional")].set_index("periodo").valor
    rc = r[r.serie == "viv_pct_compras_extranjeros_serie8a"].sort_values("edicion").drop_duplicates(
        ["territorio", "periodo"], keep="last")
    od = pd.read_csv(RAW / "pdf" / "registradores_opendata_anual.csv")
    odc = od[(od.serie == "compraventas_viv_num") & (od.nivel == "ccaa")].copy()
    odc["k"] = odc.territorio.map(norm)
    rc = rc.assign(k=rc.territorio.map(norm)).merge(odc[["k", "periodo", "valor"]].rename(columns={"valor": "cv"}),
                                                      on=["k", "periodo"], how="left")
    der = rc.dropna(subset=["cv"]).groupby("periodo").apply(
        lambda g: (g.valor * g.cv).sum() / g.cv.sum(), include_groups=False)
    cob = rc.dropna(subset=["cv"]).groupby("periodo").cv.sum() / od[(od.serie == "compraventas_viv_num") &
                                                                    (od.nivel == "nacional")].set_index("periodo").valor
    rg = pd.DataFrame({"registradores_pct_ext_derivado_ccaa": der, "registradores_cobertura_ccaa": cob,
                       "registradores_pct_ext_publicado": rn})
    ev = pd.concat([mv, nt, rg], axis=1).sort_index()
    ev.round(2).to_csv(TAB / "extranjeros_evolucion_nacional.csv")
    reg("extranjeros", "evolucion_nacional", "cuotas por fuente", len(ev), "3 fuentes; definiciones distintas",
        ev.index.min(), ev.index.max())
    # provincias: MIVAU y Registradores (2023-2025)
    rp = r[(r.serie == "viv_pct_compras_extranjeros") & (r.nivel == "provincia")].copy()
    rp["k"] = rp.territorio.map(norm)
    rp = rp.drop_duplicates(["k", "periodo"])
    odp = od[(od.serie == "compraventas_viv_num") & (od.nivel == "provincia")].copy()
    odp["k"] = odp.territorio.map(norm)
    rp = rp.merge(odp[["k", "periodo", "valor", "territorio"]].rename(columns={"valor": "cv", "territorio": "terr_od"}),
                  on=["k", "periodo"], how="left")
    rp["ext_n"] = rp.valor / 100 * rp.cv
    k2c = prov_codes()
    rp["codigo"] = rp.k.map(k2c)
    reg_p = rp.groupby("codigo").agg(registradores_pct_ext=("valor", "mean"), ext_n=("ext_n", "sum"),
                                     cv=("cv", "sum")).reset_index()
    reg_p["registradores_pct_ext_ponderado_2023_25"] = 100 * reg_p.ext_n / reg_p.cv
    mp = cn[(cn.anyo >= 2023) & (cn.anyo <= 2025)]
    mp = mp[mp.nivel.isin(["provincia", "ccaa"])].copy()
    mp["codigo"] = [k2c.get(norm(t)) if nv == "provincia" else UNIPROV_CCAA.get(next(
        (u for u in UNIPROV_CCAA if u in norm(t)), ""), None) for t, nv in zip(mp.territorio, mp.nivel)]
    mp = mp.dropna(subset=["codigo"])
    mpw = mp.pivot_table(index="codigo", columns="var", values="sum", aggfunc="sum")
    mprov = pd.DataFrame({"mivau_total_2023_25": mpw.tx_residencia_total,
                          "mivau_ext_residentes": mpw.tx_residencia_residentes_extranjeros,
                          "mivau_ext_no_residentes": mpw.tx_residencia_no_residentes_extranjeros}).reset_index()
    mprov["mivau_pct_ext"] = 100 * (mprov.mivau_ext_residentes + mprov.mivau_ext_no_residentes) / mprov.mivau_total_2023_25
    mprov["mivau_pct_no_res_sobre_ext"] = 100 * mprov.mivau_ext_no_residentes / (
        mprov.mivau_ext_residentes + mprov.mivau_ext_no_residentes)
    nombres = {v: k for k, v in k2c.items()}
    pv = mprov.merge(reg_p[["codigo", "registradores_pct_ext_ponderado_2023_25", "ext_n"]].rename(
        columns={"ext_n": "registradores_ext_n_2023_25"}), on="codigo", how="outer")
    pv["clave_nombre"] = pv.codigo.map(nombres)
    pv["zona"] = np.where(pv.codigo.isin(ISLAS), "islas", np.where(pv.codigo.isin(COSTA), "costa", "interior"))
    pv.loc[pv.codigo.isin(["51", "52"]), "zona"] = "otras"
    pv = pv.sort_values("codigo")
    if SMOKE:
        pv = pv.head(6)
    pv.round(3).to_csv(TAB / "extranjeros_provincias_2023_2025.csv", index=False)
    reg("extranjeros", "provincias_2023_25", "cuotas por provincia", len(pv), "MIVAU y Registradores")
    # concentracion geografica MIVAU 2007-2025 (compras extranjeras por zona)
    mz = cn[(cn.nivel.isin(["provincia", "ccaa"])) & (cn["var"].isin(["tx_residencia_residentes_extranjeros",
                                                                    "tx_residencia_no_residentes_extranjeros",
                                                                    "tx_residencia_total"]))].copy()
    mz["codigo"] = [k2c.get(norm(t)) if nv == "provincia" else UNIPROV_CCAA.get(next(
        (u for u in UNIPROV_CCAA if u in norm(t)), ""), None) for t, nv in zip(mz.territorio, mz.nivel)]
    mz = mz.dropna(subset=["codigo"])
    mz["zona"] = np.where(mz.codigo.isin(ISLAS), "islas", np.where(mz.codigo.isin(COSTA), "costa", "interior"))
    mz = mz[~mz.codigo.isin(["51", "52"])]
    zz = mz.pivot_table(index=["anyo", "zona"], columns="var", values="sum", aggfunc="sum").reset_index()
    zz["ext"] = zz.tx_residencia_residentes_extranjeros + zz.tx_residencia_no_residentes_extranjeros
    tot = zz.groupby("anyo")[["ext", "tx_residencia_total", "tx_residencia_no_residentes_extranjeros"]].transform("sum")
    zz["pct_compras_ext_en_zona"] = 100 * zz.ext / tot.ext
    zz["pct_compraventas_total_en_zona"] = 100 * zz.tx_residencia_total / tot.tx_residencia_total
    zz["pct_ext_en_la_zona"] = 100 * zz.ext / zz.tx_residencia_total
    zz["pct_no_res_ext_en_zona"] = 100 * zz.tx_residencia_no_residentes_extranjeros / tot.tx_residencia_no_residentes_extranjeros
    zz[["anyo", "zona", "ext", "tx_residencia_total", "pct_compras_ext_en_zona", "pct_compraventas_total_en_zona",
        "pct_ext_en_la_zona", "pct_no_res_ext_en_zona"]].round(2).to_csv(TAB / "extranjeros_concentracion_zonas.csv", index=False)
    reg("extranjeros", "concentracion_zonas", "reparto costa/islas/interior", len(zz), "supuesto COSTA declarado")
    # Notariado CV: tres provincias valencianas, 2018-2025
    cv = pd.read_csv(RAW / "pdf" / "notariado_cv_prov_trimestral.csv")
    cv = cv[cv.serie.isin(["viv_vendidas_esp", "viv_vendidas_ext"])].copy()
    cv["anyo"] = cv.periodo.str[:4].astype(int)
    cvw = cv.pivot_table(index=["territorio", "anyo"], columns="serie", values="valor", aggfunc="sum").reset_index()
    cvw["notariado_cv_pct_ext"] = 100 * cvw.viv_vendidas_ext / (cvw.viv_vendidas_ext + cvw.viv_vendidas_esp)
    cvw["codigo"] = cvw.territorio.map({"Valencia": "46", "Alicante": "03", "Castellón": "12"})
    cmp = cvw.merge(pv[["codigo", "mivau_pct_ext", "registradores_pct_ext_ponderado_2023_25"]], on="codigo", how="left")
    cvw.round(2).to_csv(TAB / "extranjeros_notariado_cv_provincias.csv", index=False)
    return ev, pv, zz, cvw


def prov_codes():
    d = json.load(open(RAW / "v3" / "pa_aux" / "ine_t59531.json"))
    orden = []
    for x in d:
        if x["Nombre"].endswith(", Viviendas totales") and not x["Nombre"].startswith("Total"):
            c, n = x["Nombre"][: -len(", Viviendas totales")].split(" ", 1)
            orden.append((c, n))
    h = jerarquia(orden)
    return {norm(n): c for (c, n), nv in h.items() if nv == "provincia"}


# ---------------------------------------------------------------- (c) oferta anunciada (robustez)
def oferta(stock_ciudades):
    a = pd.read_csv(RAW / "v3" / "airbnb_insideairbnb_agregados_v3.csv.gz")
    a = a[a.nivel == "CIUDAD"].copy()
    a["tipo"] = a.serie.str.extract(r"IA_anuncios_activos_(\w+?)__")[0]
    a["zona"] = a.serie.str.extract(r"__(\w+)$")[0]
    a = a.dropna(subset=["tipo"])
    a = a.sort_values("fecha").drop_duplicates(["tipo", "zona"], keep="last")
    w = a.pivot_table(index=["zona", "fecha"], columns="tipo", values="valor").reset_index()
    w["fuente"] = "Inside Airbnb (CC BY 4.0), listados publicos agregados; anuncios no son viviendas; solo robustez"
    mp = {"madrid": "Madrid", "barcelona": "Barcelona", "valencia": "València", "sevilla": "Sevilla", "malaga": "Málaga"}
    vut = stock_ciudades.set_index("territorio").vut_ine_2026M05
    w["vut_ine_2026M05"] = w.zona.map(lambda z: vut.get(mp.get(z), np.nan))
    w["ratio_entera_sobre_vut_ine"] = w.entera / w.vut_ine_2026M05
    w.round(3).to_csv(TAB / "oferta_anunciada_airbnb_robustez.csv", index=False)
    reg("oferta", "airbnb_robustez", "ratio anuncios/VUT", len(w), "solo robustez; sin scraping; alquiler de temporada no distinguido")
    return w


# ---------------------------------------------------------------- fichas, figuras, salida
def figuras(pjt, ev, zz):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(pjt.index, pjt.pct_comprador_pj, label="compra PJ (ETDP)")
    ax[0].plot(pjt.index, pjt.pct_vendedor_pj, label="vende PJ (ETDP)")
    ax[0].set_title("Peso de personas jurídicas en compraventas de vivienda (%)")
    ax[0].legend()
    for c, lab in (("mivau_pct_ext", "MIVAU"), ("notariado_pct_ext", "Notariado (libre)"),
                   ("registradores_pct_ext_derivado_ccaa", "Registradores (derivado)")):
        ax[1].plot(ev.index, ev[c], label=lab)
    ax[1].set_title("Compras por extranjeros, % de compraventas")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(OUT / "fig_pj_y_extranjeros.png", dpi=110)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    for z, g in zz.groupby("zona"):
        ax.plot(g.anyo, g.pct_compras_ext_en_zona, label=z)
    ax.set_title("Reparto de compras extranjeras por zona (MIVAU, %)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "fig_extranjeros_zonas.png", dpi=110)
    plt.close(fig)


def main():
    st, cmp_gva = stock()
    ten, eff = tenencia()
    pjt, pjm, inc = flujo_pj()
    ev, pv, zz, cvw = extranjeros()
    of = oferta(st["ciudades"])
    figuras(pjt, ev, zz)
    n = st["nacional"].iloc[0]
    u = pjt.index.max()
    last = ev.dropna(subset=["mivau_pct_ext"]).index.max()
    e = ev.loc[last]
    nt = ev.dropna(subset=["notariado_pct_ext"]).iloc[-1]
    rg_pub = ev.registradores_pct_ext_publicado.dropna()
    costa = zz[(zz.anyo == zz.anyo.max())].set_index("zona")
    ten_n = ten[ten.nivel == "nacional"].iloc[0]
    hechos = {
        "stock_uso_nacional": {
            "viv_total": float(n.viv_total_censo), "principal": float(n.principal), "no_principal": float(n.no_principal),
            "vacias_consumo": float(n.vacias), "uso_esporadico_consumo": float(n.esporadico),
            "turisticas_ine_2026M05": float(n.vut_ine_2026M05),
            "pct_vacias": float(n.pct_vacias), "pct_esporadico": float(n.pct_esporadico), "pct_vut": float(n.pct_vut),
            "ratio_vacias_esporadico_sobre_vut": float(n.ratio_vacias_esporadico_sobre_vut),
            "fuentes": "INE Censo 2021 (59525, 59531 consumo electrico); INE VUT (experimental)",
            "capa": "C1 turisticas (INE y registro GVA); C4 vacias y esporadicas (fuente unica INE)"},
        "tenencia_nacional": {"pct_alquiler": float(ten_n.pct_alquiler), "pct_propiedad": float(ten_n.pct_propiedad),
                              "pct_otro_cesion": float(ten_n.pct_otro_cesion), "fuente": "Censo 2021, 59523"},
        "eff_otras_propiedades_total": float(eff[eff.edad == "total"].valor.iloc[0]),
        "pj_comprador_etdp": {"anyo": int(u), "pct_comprador_pj": float(pjt.pct_comprador_pj.loc[u]),
                              "pct_vendedor_pj": float(pjt.pct_vendedor_pj.loc[u]),
                              "pct_comprador_pj_2007": float(pjt.pct_comprador_pj.iloc[0]),
                              "capa": "C4 (fuente unica)"},
        "pj_stock": "sin dato: Catastro no publica titulares por tipo; Incasol y Censo no traen tipo de arrendador",
        "extranjeros_nacional": {"anyo_mivau": int(last), "mivau_pct": float(e.mivau_pct_ext),
                                 "mivau_pct_residentes": float(e.mivau_pct_ext_residentes),
                                 "mivau_pct_no_residentes": float(e.mivau_pct_ext_no_residentes),
                                 "notariado_anyo": int(nt.name), "notariado_pct": float(nt.notariado_pct_ext),
                                 "notariado_pct_residentes": float(nt.notariado_pct_ext_residentes),
                                 "notariado_pct_no_residentes": float(nt.notariado_pct_ext_no_residentes),
                                 "registradores_pct_publicado": {int(k): float(v) for k, v in rg_pub.items()},
                                 "capa": "C1 (3 fuentes; definiciones y coberturas distintas)"},
        "extranjeros_concentracion_ultimo_anyo_mivau": {z: {"pct_compras_ext": float(r.pct_compras_ext_en_zona),
                                                            "pct_compraventas_total": float(r.pct_compraventas_total_en_zona),
                                                            "pct_ext_en_zona": float(r.pct_ext_en_la_zona)}
                                                        for z, r in costa.iterrows()},
        "airbnb_robustez": "solo robustez; ver tablas/oferta_anunciada_airbnb_robustez.csv",
    }
    json.dump(hechos, open(OUT / "hechos.json", "w"), ensure_ascii=False, indent=1)
    json.dump(fichas(hechos, ev, pjt, pv, zz), open(OUT / "fichas_verificador.json", "w"), ensure_ascii=False, indent=1)
    res = {
        "rama": "M4",
        "pregunta": "¿Qué peso tienen personas jurídicas y compradores extranjeros en el parque (stock) y en el mercado (flujos)?",
        "capa": "C1 (stock por uso, tenencia, extranjeros) / C4 (peso de PJ: fuente única en flujos, sin dato de stock)",
        "datos": ["ine_t59531", "ine_v3_censo2021_municipio_viviendas", "ine_v2_vut", "gva_vut_municipio",
                  "ine_v4_t59523", "ine_v4_t59529", "ine_v4_t50272", "ine_v4_t50256", "eff_tenencia_edad_v3",
                  "notariado_cgn_extranjeros_semestral", "notariado_cv_prov_trimestral", "registradores_eri_anuario",
                  "registradores_opendata_anual", "mivau_transacciones_residencia", "incasol_fianzas_municipio_v3",
                  "airbnb_insideairbnb_agregados_v3 (robustez)"],
        "N": {"provincias": int(len(st["provincia"])), "ciudades": int(len(st["ciudades"])),
              "anyos_extranjeros": int(len(ev))},
        "metodo": "Descriptivo: cuotas, ratios y reparto por zonas; sin estimación causal",
        "estimacion": hechos,
        "ic95": None,
        "p_ajustado": None,
        "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {"corr_prov_mivau_registradores_2023_25": float(pv[["mivau_pct_ext", "registradores_pct_ext_ponderado_2023_25"]].dropna().corr().iloc[0, 1]),
                         "dif_media_registradores_menos_mivau_pp": float((pv.registradores_pct_ext_ponderado_2023_25 - pv.mivau_pct_ext).mean()),"cuadre_etdp_suma_cuatro": float(pjt.suma_cuatro.round(0).mean()),
                         "cobertura_registradores_ccaa_min": float(ev.registradores_cobertura_ccaa.min()),
                         "vut_ine_vs_gva": cmp_gva.to_dict("records")},
        "fuera_muestra": {"modelo": "no aplica (hechos descriptivos)", "rmse": None, "dm_vs_ar4": None},
        "notas": "Catastro no publica titulares por tipo; Incasol sin tipo de arrendador (ver docs/v4/fuentes_fallidas.md). "
                 "Airbnb solo robustez. Ciudades: siete (Madrid, Barcelona, Valencia, Sevilla, Zaragoza, Malaga, Bilbao).",
    }
    json.dump(res, open(OUT / "resultado.json", "w"), ensure_ascii=False, indent=1, default=float)
    REG.flush()


def miles(x):
    return f"{x:,.0f}".replace(",", ".")


def f1(x):
    return f"{x:.1f}".replace(".", ",")


def fichas(h, ev, pjt, pv, zz):
    e = h["extranjeros_nacional"]
    s = h["stock_uso_nacional"]
    cz = h["extranjeros_concentracion_ultimo_anyo_mivau"]
    rp = e["registradores_pct_publicado"]
    lo = min(e["mivau_pct"], rp[max(rp)] if rp else e["mivau_pct"])
    hi = max(e["notariado_pct"], max(rp.values()) if rp else 0)
    pj = h["pj_comprador_etdp"]
    ev_x = ["output/v4/M4/tablas/extranjeros_evolucion_nacional.csv",
            "output/v4/M4/tablas/extranjeros_provincias_2023_2025.csv",
            "output/v4/M4/tablas/extranjeros_concentracion_zonas.csv"]
    return [
        {"id": "M4-V1", "tema": "Compradores extranjeros (sustituye a V14)",
         "enunciado": "Los compradores extranjeros encarecen la vivienda en España.", "capa": "C1",
         "magnitud": (f"Peso en las compraventas: MIVAU {f1(e['mivau_pct'])} % en {e['anyo_mivau']} "
                      f"(residentes {f1(e['mivau_pct_residentes'])} %, no residentes {f1(e['mivau_pct_no_residentes'])} %); "
                      f"Notariado, vivienda libre, {f1(e['notariado_pct'])} % en {e['notariado_anyo']} "
                      f"(residentes {f1(e['notariado_pct_residentes'])} %, no residentes {f1(e['notariado_pct_no_residentes'])} %); "
                      f"Registradores {f1(min(rp.values()))}-{f1(max(rp.values()))} % en 2023-2025. "
                      "El efecto sobre el precio no se ha estimado."),
         "intervalo": f"[{f1(lo)}; {f1(hi)}] % de las compraventas (rango entre fuentes, por definiciones distintas)",
         "cota": "— (sin cota C2 de precio)",
         "literatura": "v2 (BV): sin efecto identificado; el peso es un hecho C1, no un efecto.",
         "veredicto": "ANALIZADA, NO CONCLUYENTE",
         "regla": "Hay un hecho C1 con tres fuentes sobre el peso, pero ningún diseño ni cota C2 sobre el efecto en el precio.",
         "limites": ("Las fuentes difieren en cobertura (MIVAU: todas las transmisiones; Notariado: operaciones de vivienda "
                     "libre; Registradores: compraventas registradas). Registradores no separa residentes de no residentes. "
                     "La concentración en costa e islas es un hecho descriptivo; no implica efecto."),
         "evidencia": ev_x},
        {"id": "M4-V2", "tema": "Empresas en el mercado del alquiler",
         "enunciado": "Las empresas dominan el mercado del alquiler.", "capa": "C4",
         "magnitud": (f"Flujo: las personas jurídicas son el {f1(pj['pct_comprador_pj'])} % de los compradores y el "
                      f"{f1(pj['pct_vendedor_pj'])} % de los vendedores en las compraventas de vivienda ({pj['anyo']}, INE ETDP; fuente única). "
                      "Stock de viviendas en alquiler por tipo de titular y contratos nuevos por tipo de arrendador: sin dato."),
         "intervalo": "—", "cota": "—", "literatura": "No revisada en esta ficha.",
         "veredicto": "NO ANALIZADA: FALTAN DATOS",
         "regla": ("Faltan titularidad (Catastro no publica titulares por tipo), arrendador en las fianzas de Incasòl y "
                   "tipo de arrendador en el Censo. La cuota de compra no mide el alquiler."),
         "limites": "El único dato por tipo de persona es de compraventas (ETDP), no de alquiler ni de stock; capa C4 declarada.",
         "evidencia": ["output/v4/M4/tablas/flujo_compraventas_comprador_pj_etdp.csv",
                       "output/v4/M4/tablas/tenencia_censo2021.csv", "output/v4/M4/tablas/flujo_alquiler_incasol_contratos.csv"]},
        {"id": "M4-V3", "tema": "Viviendas vacías, de uso esporádico y turísticas",
         "enunciado": "Hay muchas viviendas vacías o de uso esporádico frente a las turísticas.",
         "capa": "C4",
         "magnitud": (f"España: {miles(s['vacias_consumo'])} vacías ({f1(s['pct_vacias'])} % del parque) y "
                      f"{miles(s['uso_esporadico_consumo'])} de uso esporádico ({f1(s['pct_esporadico'])} %) en el Censo 2021 "
                      f"(método de consumo eléctrico); {miles(s['turisticas_ine_2026M05'])} turísticas en mayo de 2026 "
                      f"({f1(s['pct_vut'])} % del parque 2021). Ratio (vacías + esporádicas) / turísticas: "
                      f"{f1(s['ratio_vacias_esporadico_sobre_vut'])}."),
         "intervalo": "—", "cota": "—", "literatura": "No revisada en esta ficha.",
         "veredicto": "ANALIZADA, NO CONCLUYENTE",
         "regla": "Hecho descriptivo: las vacías y esporádicas suman un orden de magnitud más que las turísticas. «Muchas» no tiene umbral y la fuente de vacías es única (capa C4), por lo que no cabe veredicto de respaldo.",
         "limites": ("Vacía y esporádica se infieren del consumo eléctrico (INE, experimental); las turísticas son de otra fecha y "
                     "pertenecen al parque principal o no principal (no suman). El registro de la Generalitat Valenciana y el INE difieren "
                     "en turísticas (ver vut_ine_frente_registro_gva.csv). No se estima ningún efecto."),
         "evidencia": ["output/v4/M4/tablas/stock_uso_nacional.csv", "output/v4/M4/tablas/stock_uso_provincia.csv",
                       "output/v4/M4/tablas/stock_uso_ciudades.csv", "output/v4/M4/tablas/vut_ine_frente_registro_gva.csv"]},
    ]


if __name__ == "__main__":
    main()
