"""Replica ciega lote «a» (V16, fase previa a la 7). SEED=20261010.

Una funcion por id. Solo lee data/raw con las definiciones de output/v6_2/anexo_metodologico.md
y metodologia/. Sin data/sealed, sin codigo de versiones anteriores.
Salida: output/v16/replica/v10_a/resultado.json (con el publicado leido solo AL FINAL).
"""
import json
import unicodedata
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
RAIZ = Path(__file__).resolve().parents[3]
RAW = RAIZ / "data" / "raw"
SALIDA = RAIZ / "output" / "v16" / "replica" / "v10_a"


def _sin_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn")


def _clave(s):
    return _sin_acentos(str(s)).lower().split("/")[0].strip()


def _nucleo(vars_, tol=0.15):
    """Mayor subconjunto con (1+max)/(1+min)-1 <= tol; empate: menor amplitud."""
    mejor = None
    nombres = list(vars_)
    for k in range(len(nombres), 0, -1):
        cand = []
        for c in combinations(nombres, k):
            v = [vars_[x] for x in c]
            amp = (1 + max(v)) / (1 + min(v)) - 1
            if amp <= tol:
                cand.append((amp, c))
        if cand:
            cand.sort()
            mejor = cand[0][1]
            break
    return mejor


# ---------------------------------------------------------------- dh_2125
def dh_2125():
    epa = pd.read_csv(RAW / "ine_epa_hogares.csv")
    epa = epa[epa.serie == "EPA430446"].set_index("periodo").valor  # miles de hogares
    m = lambda y: np.mean([epa[f"{y}T{q}"] for q in range(1, 5)])
    d_epa = (m(2025) - m(2021)) * 1000
    ecp = pd.read_csv(RAW / "ine_hogares_60131.csv")
    ecp = ecp[ecp.serie == "ECP355533"].set_index("periodo").valor
    d_ecp = ecp["2025T1"] - ecp["2021T1"]
    lo, hi = min(d_epa, d_ecp), max(d_epa, d_ecp)
    return {"valor": (lo + hi) / 2, "min": lo, "max": hi,
            "detalle": {"epa": d_epa, "ecp": d_ecp}}


# ---------------------------------------------------------------- terminadas
def _terminadas_anuales():
    fo = pd.read_csv(RAW / "mivau_fin_obra.csv")
    pr = pd.read_csv(RAW / "mivau_v2_protegida.csv")

    def libres(serie):
        x = fo[fo.serie == serie].copy()
        x["y"] = x.periodo.astype(str).str[:4].astype(int)
        return x.groupby("y").valor.sum()

    def prot(serie):
        x = pr[pr.serie == serie]
        return x.assign(y=x.periodo.astype(int)).set_index("y").valor

    anios = range(2019, 2025)
    nac = {y: libres("viv_libres_terminadas_nacional").get(y, 0) + prot("prot_definitiva_anual_nacional").get(y, 0)
           for y in anios}
    pv = {y: libres("viv_libres_terminadas_ccaa_pais_vasco").get(y, 0) + prot("prot_definitiva_anual_ccaa_pais_vasco").get(y, 0)
          for y in anios}
    na = {y: libres("viv_libres_terminadas_ccaa_navarra_comunidad_foral_de").get(y, 0)
          + prot("prot_definitiva_anual_ccaa_navarra_comunidad_foral_de").get(y, 0) for y in anios}
    return nac, pv, na


def terminadas_1924():
    nac, pv, na = _terminadas_anuales()
    comun = {y: nac[y] - pv[y] - na[y] for y in nac}
    v = list(comun.values())
    return {"valor": None, "min": min(v), "max": max(v), "detalle": comun}


def E_T7_prod():
    nac, _, _ = _terminadas_anuales()
    v = list(nac.values())
    return {"valor": None, "min": min(v), "max": max(v), "detalle": nac}


# ---------------------------------------------------------------- demolicion
def E_T7_demol_2024():
    """Licencias 2024: estrecha = viviendas a demoler (demolicion total) + viviendas suprimidas (parcial),
    tabla 10 de licencias; amplia = 'obras de demolicion total (3)' de la tabla 6. Divide entre parque MIVAU."""
    d = RAW / "v5_1" / "t1"
    t10 = pd.read_excel(d / "10011000.XLS", header=None)
    f10 = t10[t10[0] == 2024].iloc[0]
    viv_total, viv_supr = float(f10[6]), float(f10[9])
    t6 = pd.read_excel(d / "10010600.XLS", header=None)
    f6 = t6[t6[0] == 2024].iloc[0]
    amplia = float(f6[8])
    estrecha = viv_total + viv_supr
    p = pd.read_csv(RAW / "mivau_parque.csv")
    p = p[p.serie == "parque_total_viviendas_nacional"].set_index("periodo").valor
    P24, P23 = p.loc[2024], p.loc[2023]
    return {"valor": None, "min": 100 * estrecha / P24, "max": 100 * amplia / P24,
            "detalle": {"estrecha": estrecha, "amplia": amplia, "parque_2024": P24, "parque_2023": P23,
                        "variante_parque_2023": {"min": 100 * estrecha / P23, "max": 100 * amplia / P23}}}


# ---------------------------------------------------------------- A23-A2
def A23_A2():
    ipc = pd.read_csv(RAW / "ine_ipc_alquiler.csv")
    ipc = ipc[ipc.nombre == "Nacional. Alquiler de vivienda. Índice."].copy()
    ipc["y"] = ipc.periodo.str[:4].astype(int)
    a = ipc.groupby("y").valor.mean()
    v_ipc = a[2024] / a[2015] - 1
    iv = pd.read_csv(RAW / "ine_v2_ipva.csv")
    iv = iv[(iv.nivel == "nacional") & (iv.medida == "IPVA_indice")]
    tot = iv[(iv.tabla == 59058) & (iv.desglose == "Total")].set_index("periodo").valor
    v_tot = tot[2024] / tot[2015] - 1
    ex = iv[(iv.tabla == 59005) & (iv.desglose == "Contrato existente")].set_index("periodo").valor
    v_ex_ficha = ex[2024] / 100 - 1          # formula de la ficha (base 2021=100)
    v_ex_alt = ex[2024] / ex[2021] - 1        # alternativa: cociente 2024/2021 con los datos tal cual
    sp = pd.read_csv(RAW / "pdf" / "serpavi_esp_agregado.csv")
    sp = sp[sp.serie == "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_constante"].set_index("periodo").valor
    v_sp = sp[2024] / sp[2015] - 1
    vars_ = {"IPC": v_ipc, "IPVA_existente": v_ex_ficha, "IPVA_total": v_tot, "SERPAVI": v_sp}
    nuc = _nucleo(vars_)
    vals = [vars_[k] for k in nuc]
    return {"valor": None, "min": 100 * min(vals), "max": 100 * max(vals),
            "detalle": {"variaciones_%": {k: 100 * v for k, v in vars_.items()}, "nucleo": nuc,
                        "ipva_existente_alt_2024_sobre_2021_%": 100 * v_ex_alt,
                        "ipva_existente_indice_2021_2024": [float(ex[2021]), float(ex[2024])]}}


# ---------------------------------------------------------------- A23-P2
def A23_P2():
    mv = pd.read_csv(RAW / "mivau_valor_tasado_nacional_ccaa_prov.csv")
    mv = mv[mv.serie == "valor_tasado_libre_nacional"].copy()
    mv["y"] = mv.periodo.str[:4].astype(int)
    g = mv.groupby("y").valor.agg(["mean", "count"])
    v_mv = g.loc[2025, "mean"] / g.loc[2015, "mean"] - 1
    nt = pd.read_csv(RAW / "pdf" / "notariado_cgn_extranjeros_semestral.csv")
    nt = nt[(nt.serie == "precio_m2") & (nt.categoria == "Total general")].copy()
    nt["y"] = nt.periodo.str[:4].astype(int)
    gn = nt.groupby("y").valor.agg(["mean", "count"])
    gn = gn[gn["count"] == 2]
    v_nt = gn.loc[2025, "mean"] / gn.loc[2015, "mean"] - 1
    rg = pd.read_csv(RAW / "pdf" / "registradores_opendata_anual.csv")
    rg = rg[(rg.serie == "compraventas_viv_pm2") & (rg.nivel == "nacional")].set_index("periodo").valor
    v_rg = rg[2025] / rg[2015] - 1
    vars_ = {"MIVAU": v_mv, "Notariado": v_nt, "Registradores": v_rg}
    nuc = _nucleo(vars_)
    vals = [vars_[k] for k in nuc]
    return {"valor": 100 * float(np.median(vals)), "min": 100 * min(vals), "max": 100 * max(vals),
            "detalle": {"variaciones_%": {k: 100 * v for k, v in vars_.items()}, "nucleo": nuc,
                        "mivau_n_trim_2015_2025": [int(g.loc[2015, 'count']), int(g.loc[2025, 'count'])]}}


# ---------------------------------------------------------------- A23-A10 y A9
def _ipva_prov_nuevo(territorios):
    iv = pd.read_csv(RAW / "ine_v2_ipva.csv")
    iv = iv[(iv.nivel == "provincia") & (iv.tabla == 59005) & (iv.medida == "IPVA_indice")
            & (iv.desglose == "Nuevo contrato")]
    out = {}
    for t in territorios:
        s = iv[iv.territorio == t].set_index("periodo").valor
        out[t] = s[2024] / s[2021] - 1
    return out


def _pesos_serpavi(prefijo_cod):
    s = pd.read_csv(RAW / "pdf" / "serpavi_provincias.csv")
    s = s[(s.variable == "n_contratos") & (s.tipologia == "VC") & (s.periodo == 2024)]
    return {_clave(r.nombre): r.valor for r in s.itertuples() if int(r.codigo) in prefijo_cod}


def A23_A10():
    terr = ["Alicante/Alacant", "Castellón/Castelló", "Valencia/València"]
    var = _ipva_prov_nuevo(terr)
    w = _pesos_serpavi({3, 12, 46})
    num = sum(var[t] * w[_clave(t)] for t in terr)
    den = sum(w[_clave(t)] for t in terr)
    v_ipva = num / den
    fr = []
    for y in range(2020, 2027):
        p = RAW / "v5" / f"gva_fianzas_{y}.csv"
        if p.exists():
            fr.append(pd.read_csv(p, sep=";", usecols=["anyo_datos", "importe_fianza"]))
    fr = pd.concat(fr)
    fr["importe_fianza"] = pd.to_numeric(fr.importe_fianza.astype(str).str.replace(",", "."), errors="coerce")
    fr = fr[(fr.importe_fianza >= 100) & (fr.importe_fianza <= 5000)]
    med = fr.groupby("anyo_datos").importe_fianza.median()
    v_fi = med[2024] / med[2021] - 1
    vars_ = {"IPVA_nuevo": v_ipva, "fianzas": v_fi}
    nuc = _nucleo(vars_)
    vals = [vars_[k] for k in nuc]
    return {"valor": 100 * float(np.mean(vals)), "min": 100 * min(vals), "max": 100 * max(vals),
            "detalle": {"var_prov_%": {k: 100 * v for k, v in var.items()}, "pesos": w,
                        "ipva_pond_%": 100 * v_ipva, "fianzas_%": 100 * v_fi,
                        "mediana_fianza_2021_2024": [float(med[2021]), float(med[2024])], "nucleo": nuc}}


def A23_A9():
    terr = ["Barcelona", "Girona", "Lleida", "Tarragona"]
    var = _ipva_prov_nuevo(terr)
    w = _pesos_serpavi({8, 17, 25, 43})
    num = sum(var[t] * w[_clave(t)] for t in terr)
    den = sum(w[_clave(t)] for t in terr)
    v_ipva = num / den
    inc = pd.read_csv(RAW / "v3" / "incasol_fianzas_municipio_v3.csv.gz")

    def renta(y, ponderar_por="banda"):
        x = inc[inc.periodo == f"{y} gener-desembre"].copy()
        x["t"] = x.serie.str.extract(r"FIANZAS_\d+_(n_contratos|renta_media)")[0]
        n = x[(x.t == "n_contratos") & (x.banda != "TOTAL_bandas")][["codigo", "banda", "valor"]].rename(columns={"valor": "n"})
        r = x[x.t == "renta_media"][["codigo", "banda", "valor"]].rename(columns={"valor": "r"})
        m = r.merge(n, on=["codigo", "banda"], how="inner")
        m = m[(m.n > 0) & m.r.notna()]
        return float((m.r * m.n).sum() / m.n.sum()), len(m)

    r21, n21 = renta(2021)
    r24, n24 = renta(2024)
    v_inc = r24 / r21 - 1
    vars_ = {"IPVA_nuevo": v_ipva, "Incasol": v_inc}
    nuc = _nucleo(vars_)
    vals = [vars_[k] for k in nuc]
    return {"valor": 100 * float(np.mean(vals)), "min": 100 * min(vals), "max": 100 * max(vals),
            "detalle": {"var_prov_%": {k: 100 * v for k, v in var.items()}, "pesos": w,
                        "ipva_pond_%": 100 * v_ipva, "incasol_%": 100 * v_inc,
                        "renta_media_2021_2024": [r21, r24], "celdas": [n21, n24], "nucleo": nuc}}


# ---------------------------------------------------------------- R1C-001
def R1C_001():
    e = pd.read_csv(RAW / "v3" / "eff_tenencia_edad_v3.csv")
    eff = float(e[(e.serie == "eff_pct_hogares_vivienda_principal|edad=total|ed=DO 2413 (EFF2022)") & (e.periodo == 2022)].valor.iloc[0])
    c = pd.read_csv(RAW / "v3" / "ine_ecv_tenencia_edad_v3.csv")
    ecv = float(c[(c.serie == "ecv_pct_hogares_tenencia|Propiedad|edad_persona_referencia=Total|sexo=Ambos sexos") & (c.periodo == 2022)].valor.iloc[0])
    ce = pd.read_csv(RAW / "v4" / "ine_v4_t59523.csv").set_index("serie_nombre").valor
    prop = ce["Total Nacional, En propiedad, Total (tamaño de municipio)"]
    tot = ce["Total Nacional, Total (régimen de tenencia), Total (tamaño de municipio)"]
    censo = 100 * prop / tot
    v = [eff, ecv, censo]
    return {"valor": float(np.mean(v)), "min": min(v), "max": max(v),
            "detalle": {"eff": eff, "ecv": ecv, "censo": censo, "censo_n": [float(prop), float(tot)]}}


FUNCS = {"A23-A10": A23_A10, "A23-A2": A23_A2, "A23-A9": A23_A9, "A23-P2": A23_P2, "R1C-001": R1C_001,
         "dh_2125": dh_2125, "terminadas_1924": terminadas_1924, "E-T7-prod": E_T7_prod,
         "E-T7-demol-2024": E_T7_demol_2024}


def _num(x):
    if x is None or x == "" or (isinstance(x, float) and np.isnan(x)):
        return None
    return float(x)


def _cmp(pub, rep, exacto=False):
    """Compara campo a campo; devuelve (ok, detalle)."""
    res, ok = {}, True
    for k in ("valor", "min", "max"):
        p, r = _num(pub[k]), _num(rep[k])
        if p is None and r is None:
            res[k] = "ambos vacios"
            continue
        if p is None or r is None:
            res[k] = f"vacio en {'publicado' if p is None else 'replica'}"
            ok = False
            continue
        rel = abs(r - p) / abs(p) if p else float("inf")
        res[k] = {"abs": r - p, "rel_%": 100 * rel}
        if (exacto and round(r) != round(p)) or (not exacto and rel > 0.01):
            ok = False
    return ok, res


DIAG = {
    "A23-A10": "Coincide con la ficha A9 (IPVA ponderado 26,08 %; fianzas 30,84 %; media 28,46 %). Diferencias solo de redondeo.",
    "A23-A2": "Coincide. Salvedad de la ficha: el IPVA 'Contrato existente' (tabla 59005) en data/raw trae 2021=112,229 y 2024=120,637, no base 2021=100; la ficha divide 2024 entre 100 (20,64 %) y la replica la sigue. Con 2024/2021 daria 7,5 %, y el min cambiaria. Convendria aclarar la base en la ficha.",
    "A23-A9": "Coincide tras corregir un fallo propio: la media ponderada de Incasol solo debe usar celdas municipio-banda con renta_media no nula (297/300 celdas vacias en 2021/2024). Sin ese filtro la replica daba 16,42 % (-1,1 % relativo en el min). La ficha B solo dice 'media ponderada por contratos'; el filtro no esta explicitado.",
    "A23-P2": "Coincide con la ficha A8 (MIVAU 44,22; Notariado 47,21; Registradores 56,12; mediana 47,2).",
    "R1C-001": "Coincide (EFF 72,1; ECV 75,9; Censo 75,46; media 74,49).",
    "dh_2125": "Coincide exacto (EPA 1.013.350; ECP 981.823; punto medio 997.586,5).",
    "terminadas_1924": "Coincide exacto (libres mensuales sumadas + protegidas definitivas, nacional menos Pais Vasco y Navarra; 2019=72.264, 2024=94.426).",
    "E-T7-prod": "Coincide exacto (nacional 2019=78.810; 2024=100.980).",
    "E-T7-demol-2024": "Coincide dentro de 1 % con el parque de 2024 de la ficha (0,0218-0,0359 %: desv. 0,4 %). Con el parque a 31-12-2023 (stock de inicio de 2024) el resultado es identico al publicado (0,0219236595 y 0,03607850781); esa variante se identifico comparando con el publicado, no desde la ficha. La ficha dice 'parque de 2024' y no aclara cual; el original parece usar el parque de 2023. Estrecha = viviendas a demoler (total) + viviendas suprimidas (parcial), tabla 10; amplia = demolicion total (3), tabla 6; definiciones no explicitas en la ficha (reconstruidas por combinacion de columnas).",
}


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    rep = {i: f() for i, f in FUNCS.items()}
    # el publicado se lee solo ahora, tras calcular
    pub = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    sal = []
    for i, r in rep.items():
        p = {k: _num(pub.loc[i, k]) for k in ("valor", "min", "max")}
        exacto = i in ("dh_2125", "terminadas_1924", "E-T7-prod")
        ok, det = _cmp(p, r, exacto)
        sal.append({"id": i, "publicado": p,
                    "replica": {k: _num(r[k]) for k in ("valor", "min", "max")},
                    "veredicto": "COINCIDE" if ok else "DISCREPA", "comparacion": det,
                    "detalle_replica": r["detalle"], "diagnostico": DIAG[i]})
    with open(SALIDA / "resultado.json", "w", encoding="utf-8") as f:
        json.dump(sal, f, ensure_ascii=False, indent=2, default=lambda o: float(o) if hasattr(o, "__float__") else str(o))
    for s in sal:
        print(s["id"], s["publicado"], s["replica"], s["veredicto"])


if __name__ == "__main__":
    main()
