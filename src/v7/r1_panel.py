"""V7 R1: panel regional (CCAA trimestral) y panel provincial (52 provincias) desde data/raw.

Determinista, sin red, SEED=20261010. Cruces territoriales por código INE (texto, 2 dígitos).
Excepción declarada (puente de nombres): las tablas MIVAU provinciales (valor tasado, iniciadas, terminadas) no traen
código INE; se les asigna con una tabla (clave normalizada -> cod_prov) construida a partir de los pares
(territorio, código) del propio INE (ine_v2_etdp_prov). Se exige correspondencia 1:1 y se informan los no casados.
Aguas abajo todo es por cod_prov.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "data" / "processed" / "v7"
OUT_R = RAIZ / "output" / "v7" / "R1"
DOC = RAIZ / "docs" / "v7" / "diccionario.md"
np.random.seed(SEED)
sys.path.insert(0, str(RAIZ / "src"))

# provincia -> CCAA (códigos INE; misma tabla que src/holdout.py CCAA_PROV, copiada para no importar el módulo)
PROV_A_CCAA = {
    "01": "16", "02": "08", "03": "10", "04": "01", "05": "07", "06": "11", "07": "04", "08": "09", "09": "07",
    "10": "11", "11": "01", "12": "10", "13": "08", "14": "01", "15": "12", "16": "08", "17": "09", "18": "01",
    "19": "08", "20": "16", "21": "01", "22": "02", "23": "01", "24": "07", "25": "09", "26": "17", "27": "12",
    "28": "13", "29": "01", "30": "14", "31": "15", "32": "12", "33": "03", "34": "07", "35": "05", "36": "12",
    "37": "07", "38": "05", "39": "06", "40": "07", "41": "01", "42": "07", "43": "09", "44": "02", "45": "08",
    "46": "10", "47": "07", "48": "16", "49": "07", "50": "02", "51": "18", "52": "19"}
PROVS = sorted(PROV_A_CCAA)
CCAA17 = [f"{i:02d}" for i in range(1, 18)]
N_PROV_EN_CCAA = pd.Series(PROV_A_CCAA).value_counts().to_dict()
MANIFEST = pd.read_csv(RAW / "_manifest.csv").set_index("archivo")["descargado_utc"].to_dict()
DOCROWS: list[dict] = []


def rd(nombre: str, **kw) -> pd.DataFrame:
    return pd.read_csv(RAW / nombre, dtype={"codigo": str, "cod_ccaa": str, "cod_provincia": str}, **kw)


def descarga(archivos: str) -> str:
    out = []
    for a in archivos.split("+"):
        a = a.strip()
        out.append(f"{a}: {str(MANIFEST.get(a, 'no consta en _manifest'))[:10]}")
    return "; ".join(out)


def fechas(df: pd.DataFrame) -> pd.DataFrame:
    f = pd.to_datetime(df["fecha"])
    df = df.copy()
    df["anio"] = f.dt.year
    df["mes"] = f.dt.month
    df["q"] = (f.dt.month - 1) // 3 + 1
    df["trimestre"] = df["anio"].astype(str) + "Q" + df["q"].astype(str)
    return df


def prov_a_ccaa(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["cod_ccaa"] = df["cod_prov"].map(PROV_A_CCAA)
    return df


def mensual_a_trim(df: pd.DataFrame, col: str, how: str = "sum") -> pd.DataFrame:
    """Mensual -> trimestral por cod_prov; NaN si faltan meses del trimestre (no se completa)."""
    df = fechas(df)
    g = df.groupby(["cod_prov", "anio", "q"])[col]
    r = (g.sum(min_count=3) if how == "sum" else g.mean()).where(g.count() == 3).rename(col).reset_index()
    r["trimestre"] = r["anio"].astype(str) + "Q" + r["q"].astype(str)
    return r.drop(columns=["anio", "q"])


def agrega_ccaa(pq: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Suma de provincias de cada CCAA (por código); NaN si falta alguna provincia."""
    p = prov_a_ccaa(pq)
    g = p.groupby(["cod_ccaa", "trimestre"])
    out = g[cols].sum(min_count=1)
    cnt = g[cols].count()
    esperado = pd.Series([N_PROV_EN_CCAA[c] for c in out.index.get_level_values(0)], index=out.index)
    out = out.where(cnt.eq(esperado, axis=0))
    return out.reset_index()


# ------------------------------------------------------------------------------------------------ puente MIVAU
def _clave(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def _variantes(n: str) -> set[str]:
    out = {_clave(n)} | {_clave(p) for p in str(n).split("/")}
    m = re.match(r"^(.*?),\s*(El|La|Los|Las|Els|Les|L')\s*$|^(.*?),\s*(Illes|Islas)\s*$", str(n).strip(), re.I)
    if m:
        base, art = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        out |= {_clave(base), _clave(art + base)}
    return {k for k in out if k}


def puente_nombres() -> pd.DataFrame:
    e = rd("ine_v2_etdp_prov.csv")
    e = e[e["nivel"] == "provincia"][["territorio", "codigo"]].drop_duplicates()
    filas = [(k, c) for t, c in zip(e["territorio"], e["codigo"]) for k in _variantes(t)]
    b = pd.DataFrame(filas, columns=["k_norm", "cod_prov"]).drop_duplicates()
    dup = b["k_norm"].duplicated(keep=False)
    return b[~dup]


NO_CASADOS: dict[str, list[str]] = {}


def asigna_cod(df: pd.DataFrame, col_txt: str, etiqueta: str) -> pd.DataFrame:
    b = puente_nombres()
    df = df.copy()
    claves = df[col_txt].drop_duplicates().to_frame()
    cand = []
    for t in claves[col_txt]:
        hit = sorted({k for k in _variantes(t)} & set(b["k_norm"]))
        cand.append((t, hit[0] if hit else None))
    cl = pd.DataFrame(cand, columns=[col_txt, "k_norm"])
    cl = cl.merge(b, on="k_norm", how="left")
    NO_CASADOS[etiqueta] = sorted(cl[cl["cod_prov"].isna()][col_txt].tolist())
    assert cl["cod_prov"].dropna().is_unique, f"{etiqueta}: dos nombres casan con el mismo código"
    df = df.merge(cl[[col_txt, "cod_prov"]], on=col_txt, how="left")
    return df[df["cod_prov"].notna()]


# ------------------------------------------------------------------------------------------------ fuentes provinciales
def carga_prov() -> dict[str, pd.DataFrame]:
    d: dict[str, pd.DataFrame] = {}
    epa = rd("ine_v2_epa_prov.csv")
    epa = epa[epa["nivel"] == "provincia"].rename(columns={"codigo": "cod_prov"})
    epa = fechas(epa)
    w = epa.pivot_table(index=["cod_prov", "trimestre"], columns="medida", values="valor", aggfunc="first")
    d["epa_q"] = w.rename(columns={"EPA_ocupados": "ocupados_epa", "EPA_parados": "parados_epa"}).reset_index()

    h = rd("ine_v2_hipotecas_prov.csv")
    h = h[h["nivel"] == "provincia"].rename(columns={"codigo": "cod_prov"})
    hn = mensual_a_trim(h[h["medida"] == "hipotecas_viviendas_numero"], "valor").rename(columns={"valor": "hip_n"})
    hi = mensual_a_trim(h[h["medida"] == "hipotecas_viviendas_importe"], "valor").rename(columns={"valor": "hip_importe"})
    d["hip_q"] = hn.merge(hi, on=["cod_prov", "trimestre"], how="outer")

    e = rd("ine_v2_etdp_prov.csv")
    e = e[(e["nivel"] == "provincia") & (e["desglose"] == "total")].rename(columns={"codigo": "cod_prov"})
    d["etdp_q"] = mensual_a_trim(e, "valor").rename(columns={"valor": "compraventas"})

    ip = rd("ine_v2_ipc_alquiler_prov.csv")
    ip = ip[ip["nivel"] == "provincia"].rename(columns={"codigo": "cod_prov"})
    a = mensual_a_trim(ip[ip["medida"] == "IPC_alquiler_vivienda_indice"], "valor", "mean")
    b = mensual_a_trim(ip[ip["medida"] == "IPC_alquiler_vivienda_variacion_anual"], "valor", "mean")
    d["ipc_q"] = a.rename(columns={"valor": "ipc_alquiler_indice"}).merge(
        b.rename(columns={"valor": "ipc_alquiler_yoy"}), on=["cod_prov", "trimestre"], how="outer")

    m = rd("mivau_v2_iniciadas_terminadas_prov.csv")
    m = m[m["nivel"] == "provincia"]
    for cod_tabla, nom in [(32100500, "iniciadas"), (32101000, "terminadas")]:
        x = m[m["tabla_codigo"] == cod_tabla]
        x = asigna_cod(x, "territorio", f"mivau_{nom}_mensual")
        x = x.assign(fecha=pd.to_datetime(x["periodo"] + "-01"))
        assert not x.duplicated(["cod_prov", "fecha"]).any()
        d[f"{nom}_q"] = mensual_a_trim(x, "valor").rename(columns={"valor": nom})
    for cod_tabla, nom in [(32200500, "iniciadas"), (32201000, "terminadas")]:
        x = m[m["tabla_codigo"] == cod_tabla]
        x = asigna_cod(x, "territorio", f"mivau_{nom}_anual")
        x = x.assign(anio=x["periodo"].astype(int))
        assert not x.duplicated(["cod_prov", "anio"]).any()
        d[f"{nom}_a"] = x[["cod_prov", "anio", "valor"]].rename(columns={"valor": f"{nom}_anual_tabla"})

    v = rd("mivau_valor_tasado_nacional_ccaa_prov.csv")
    v = v[(v["nivel"] == "provincia") & v["serie"].str.startswith("valor_tasado_libre_provincia_")]
    v = asigna_cod(v, "territorio", "mivau_valor_tasado")
    v = fechas(v)
    assert not v.duplicated(["cod_prov", "trimestre"]).any()
    d["vt_q"] = v[["cod_prov", "trimestre", "valor"]].rename(columns={"valor": "valor_tasado"})

    p = rd("ine_v2_padron_prov_pais.csv")
    p = p[(p["nivel"] == "provincia") & p["desglose"].isin(["nacionalidad=Total", "nacionalidad=Extranjera"])]
    p = p.assign(anio=pd.to_datetime(p["fecha"]).dt.year).rename(columns={"codigo": "cod_prov"})
    pp = p.pivot_table(index=["cod_prov", "anio"], columns="desglose", values="valor", aggfunc="first")
    d["padron_a"] = pp.rename(columns={"nacionalidad=Total": "pob_total", "nacionalidad=Extranjera": "pob_extranj"}).reset_index()

    c = rd("ine_v2_cre.csv")
    c = c[c["nivel"] == "provincia"].rename(columns={"codigo": "cod_prov"})
    d["pib_a"] = c.assign(anio=c["periodo"].astype(int))[["cod_prov", "anio", "valor"]].rename(columns={"valor": "pib_miles_eur"})

    s = rd("ine_v2_ipva.csv")
    s = s[(s["nivel"] == "provincia") & (s["medida"] == "IPVA_indice") & (s["desglose"] == "Total")]
    d["ipva_a"] = s.assign(anio=s["periodo"].astype(int)).rename(columns={"codigo": "cod_prov", "valor": "ipva_indice"})[
        ["cod_prov", "anio", "ipva_indice"]]

    u = rd("ine_v2_vut.csv")
    u = u[(u["nivel"] == "provincia") & (u["medida"] == "viviendas_turisticas")].rename(columns={"codigo": "cod_prov"})
    d["vut_obs"] = fechas(u)[["cod_prov", "fecha", "anio", "trimestre", "valor"]].rename(columns={"valor": "vut_viviendas"})
    return d


# ------------------------------------------------------------------------------------------------ eventos
def q_fin(trim: str) -> pd.Timestamp:
    y, q = int(trim[:4]), int(trim[-1])
    return pd.Timestamp(year=y, month=3 * q, day=1) + pd.offsets.MonthEnd(0)


def q_ini(trim: str) -> pd.Timestamp:
    return q_fin(trim) - pd.offsets.MonthBegin(3)


def vigente_fin(ini, fin, trim: str) -> bool:
    """Vigente el último día del trimestre."""
    qe = q_fin(trim)
    return bool(pd.notna(ini) and ini <= qe and (pd.isna(fin) or fin >= qe))


def frac_dias(ini, fin, trim: str) -> float:
    qs, qe = q_ini(trim), q_fin(trim)
    a = max(qs, ini) if pd.notna(ini) else qe + pd.Timedelta(days=1)
    b = min(qe, fin) if pd.notna(fin) else qe
    return max((b - a).days + 1, 0) / ((qe - qs).days + 1)


def regulatorias(trims: list[str]) -> tuple[pd.DataFrame, dict]:
    ev = pd.read_csv(RAW / "v2_eventos_politica.csv", dtype=str)
    ev["ini"] = pd.to_datetime(ev["fecha_entrada_vigor"])
    ev["fin"] = pd.to_datetime(ev["fecha_fin"])
    ev3 = pd.read_csv(RAW / "v3" / "eventos_v3.csv")
    ini3 = pd.to_datetime(ev3.loc[ev3["evento"].str.startswith("Ley por el derecho a la vivienda"), "fecha_entrada_vigor"]).iloc[0]
    e = ev.set_index("id")
    ley12 = e.loc["E14", "ini"]
    meta = {"ley12_2023_inicio_v2": str(ley12.date()), "ley12_2023_inicio_v3": str(ini3.date()),
            "ley12_coincide_v2_v3": bool(ley12 == ini3)}
    # zonas tensionadas: v3 (primaria) vs v2 (misma relación; se comprueba)
    zt = pd.read_csv(RAW / "v3" / "zonas_tensionadas_v3.csv", dtype=str)
    zt2 = pd.read_csv(RAW / "v2_zonas_tensionadas.csv", dtype=str)
    meta["zonas_v2_igual_v3"] = bool(zt.fillna("").equals(zt2.fillna("")))
    zt["ef"] = pd.to_datetime(zt["fecha_efecto"])
    zt["fp"] = pd.to_datetime(zt["fecha_fin_prevista"])
    dic = pd.read_excel(RAW / "ine_diccionario_municipios_2026.xlsx", sheet_name=0, header=1, dtype=str)
    dic = dic.dropna(subset=["CPRO", "CMUN", "CODAUTO"]).copy()
    dic["cod_muni"] = dic["CPRO"].str.zfill(2) + dic["CMUN"].str.zfill(3)
    dic = dic.drop_duplicates("cod_muni")
    n_muni = dic.groupby(dic["CODAUTO"].str.zfill(2))["cod_muni"].nunique()
    ct = pd.read_csv(RAW / "v3" / "cataluna_contencion_rentas_v3.csv", dtype=str)
    ct = ct[ct["regimen"] == "ley11_2020"]
    ct_ini, ct_fin = pd.to_datetime(ct["fecha_vigencia_inicio"]).min(), pd.to_datetime(ct["fecha_vigencia_fin"]).max()
    meta["tope_rentas_cat_v3_ventana"] = f"{ct_ini.date()} a {ct_fin.date()}"
    tur = ev[(ev["ambito"] == "CCAA") & (ev["mercado"] == "alquiler turístico")]
    tope = ev[(ev["ambito"] == "CCAA") & (ev["id"] == "E09")]
    filas = []
    for c in CCAA17:
        for t in trims:
            qe = q_fin(t)
            z = zt[(zt["cod_ccaa"] == c) & (zt["ef"] <= qe) & (zt["fp"].isna() | (zt["fp"] > qe))]
            cuota = z["cod_ine_municipio"].nunique() / n_muni[c]
            r = {"codigo_ine_ccaa": c, "trimestre": t, "zt_n_municipios": z["cod_ine_municipio"].nunique(),
                 "zt_cuota_municipios": cuota, "zt_declarada": int(len(z) > 0)}
            tp = tope[tope["codigos_ine_ccaa"] == c]
            r["tope_rentas_ccaa"] = int(any(vigente_fin(a, b, t) for a, b in zip(tp["ini"], tp["fin"])))
            r["tope_rentas_ccaa_frac"] = sum(frac_dias(a, b, t) for a, b in zip(tp["ini"], tp["fin"]))
            r["tope_rentas_ccaa_alt_v3"] = int(c == "09" and vigente_fin(ct_ini, ct_fin, t))
            tu = tur[tur["codigos_ine_ccaa"] == c]
            r["vut_regulacion_ccaa"] = int(any(vigente_fin(a, b, t) for a, b in zip(tu["ini"], tu["fin"])))
            r["ley12_2023_nac"] = int(vigente_fin(ley12, pd.NaT, t))
            r["tope_actualiz_rentas_nac"] = int(vigente_fin(e.loc["E11", "ini"], e.loc["E11", "fin"], t))
            r["registro_unico_arrend_nac"] = int(vigente_fin(e.loc["E22", "ini"], pd.NaT, t))
            filas.append(r)
    return pd.DataFrame(filas), meta


# ------------------------------------------------------------------------------------------------ diccionario
def reg(var, definicion, unidad, fuente, archivos, nivel, frec, metodo, nsrc=1, df=None, panel=""):
    DOCROWS.append({"var": var, "def": definicion, "unidad": unidad, "fuente": fuente, "desc": descarga(archivos),
                    "nivel": nivel, "frec": frec, "metodo": metodo, "capa": "C1" if nsrc >= 2 else "C4",
                    "df": df, "panel": panel})


def interp_log_anual(df: pd.DataFrame, col_anual: str, grupo: str, trims: list[str]) -> pd.DataFrame:
    """Anual -> trimestral: ancla en el T3 de cada año y logarítmico-lineal entre anclas; sin extrapolar."""
    filas = []
    for g, sub in df.groupby(grupo):
        s = sub.dropna(subset=[col_anual]).set_index("anio")[col_anual]
        idx = {t: int(t[:4]) * 4 + int(t[-1]) - 1 for t in trims}
        ancl = {a * 4 + 2: np.log(v) for a, v in s.items()}
        xs = sorted(ancl)
        for t in trims:
            x = idx[t]
            if not xs or x < xs[0] or x > xs[-1]:
                val, est = np.nan, ""
            elif x in ancl:
                val, est = float(np.exp(ancl[x])), "observado_anual_ancla_T3"
            else:
                val, est = float(np.exp(np.interp(x, xs, [ancl[k] for k in xs]))), "interpolacion_loglineal_entre_anclas_T3"
            filas.append({grupo: g, "trimestre": t, "val": val, "metodo": est})
    return pd.DataFrame(filas)


def anade_ln(df: pd.DataFrame, cols: list[str], grupo: str) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        df[f"ln_{c}"] = np.log(df[c].where(df[c] > 0))
        df[f"d_ln_{c}"] = df.groupby(grupo)[f"ln_{c}"].diff()
        df[f"d4_ln_{c}"] = df.groupby(grupo)[f"ln_{c}"].diff(4)
    return df


def main() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    OUT_R.mkdir(parents=True, exist_ok=True)
    d = carga_prov()
    base = pd.read_csv(RAIZ / "data" / "processed" / "panel_ccaa_q.csv", dtype={"codigo_ine_ccaa": str})
    base = base[base["trimestre"] >= "2007Q1"].copy()
    trims = sorted(base["trimestre"].unique())

    # ------------------------------- panel CCAA trimestral
    epa = agrega_ccaa(d["epa_q"].assign(), ["ocupados_epa", "parados_epa"]).rename(
        columns={"cod_ccaa": "codigo_ine_ccaa", "ocupados_epa": "ocupados_epa_prov", "parados_epa": "parados_epa"})
    epa["tasa_paro_epa"] = 100 * epa["parados_epa"] / (epa["parados_epa"] + epa["ocupados_epa_prov"])
    hip = agrega_ccaa(d["hip_q"], ["hip_n", "hip_importe"]).rename(columns={"cod_ccaa": "codigo_ine_ccaa"})
    reg_df, meta = regulatorias(trims)
    pa = prov_a_ccaa(d["pib_a"])
    pib = pa.groupby(["cod_ccaa", "anio"])["pib_miles_eur"].sum(min_count=1)
    pib = pib.where(pa.groupby(["cod_ccaa", "anio"])["cod_prov"].nunique() == pd.Series(
        {k: N_PROV_EN_CCAA[k[0]] for k in pib.index})).reset_index().rename(columns={"cod_ccaa": "codigo_ine_ccaa"})
    pib_q = interp_log_anual(pib, "pib_miles_eur", "codigo_ine_ccaa", trims).rename(
        columns={"val": "pib_ccaa_q", "metodo": "pib_ccaa_q_metodo"})
    pib_a = pib.rename(columns={"pib_miles_eur": "pib_ccaa_anual"})
    pib_a["trimestre_anio"] = pib_a["anio"]
    # VUT por CCAA: suma de provincias en la fecha observada; interpolación lineal entre observaciones, sin extrapolar
    vu = prov_a_ccaa(d["vut_obs"])
    vg = vu.groupby(["cod_ccaa", "fecha", "trimestre"])
    vs = vg["vut_viviendas"].sum(min_count=1).where(vg["cod_prov"].nunique() == pd.Series(
        {k: N_PROV_EN_CCAA[k[0]] for k in vg["vut_viviendas"].sum().index})).reset_index()
    vs = vs.groupby(["cod_ccaa", "trimestre"], as_index=False)["vut_viviendas"].last()
    vut_filas = []
    for c, sub in vs.groupby("cod_ccaa"):
        s = sub.set_index("trimestre")["vut_viviendas"].dropna()
        xs = {int(t[:4]) * 4 + int(t[-1]) - 1: v for t, v in s.items()}
        ks = sorted(xs)
        for t in trims:
            x = int(t[:4]) * 4 + int(t[-1]) - 1
            if not ks or x < ks[0] or x > ks[-1]:
                vut_filas.append((c, t, np.nan, "", False))
            elif x in xs:
                vut_filas.append((c, t, xs[x], "observado", False))
            else:
                vut_filas.append((c, t, float(np.interp(x, ks, [xs[k] for k in ks])), "interpolacion_lineal_entre_observaciones", True))
    vut = pd.DataFrame(vut_filas, columns=["codigo_ine_ccaa", "trimestre", "vut_viviendas", "vut_viviendas_metodo", "vut_viviendas_interp"])
    # exposición predeterminada 2015-2019
    hq = prov_a_ccaa(d["hip_q"])
    hq["anio"] = hq["trimestre"].str[:4].astype(int)
    hq = hq[hq["anio"].between(2015, 2019)]
    ha = hq.groupby(["cod_ccaa", "anio"])[["hip_n", "hip_importe"]].sum(min_count=1).groupby("cod_ccaa").mean()
    pb = pib[pib["anio"].between(2015, 2019)].groupby("codigo_ine_ccaa")["pib_miles_eur"].mean()
    pg = prov_a_ccaa(d["padron_a"])
    pg = pg[pg["anio"].between(2015, 2019)].groupby(["cod_ccaa", "anio"])["pob_total"].sum().groupby("cod_ccaa").mean()
    expo = pd.DataFrame({"codigo_ine_ccaa": ha.index,
                         "exp_hip_importe_pib_1519": (100 * ha["hip_importe"] / pb.reindex(ha.index)).to_numpy(),
                         "exp_hip_n_1000hab_1519": (1000 * ha["hip_n"] / pg.reindex(ha.index)).to_numpy()})
    nac = pd.read_csv(RAIZ / "data" / "processed" / "nacional_q.csv")
    cols_n = ["tipo_hip", "euribor", "credito_nuevo", "tipo_bce"]
    sh = nac[["trimestre"] + cols_n + [f"{c}_interp" for c in cols_n if f"{c}_interp" in nac]].copy()
    sh = sh.rename(columns={c: f"nac_{c}" for c in sh.columns if c != "trimestre"})

    p = base.copy()
    for t in (epa, hip, reg_df, pib_q, vut, expo):
        p = p.merge(t, on=[c for c in ("codigo_ine_ccaa", "trimestre") if c in t.columns], how="left")
    p["anio"] = p["trimestre"].str[:4].astype(int)
    p = p.merge(pib_a[["codigo_ine_ccaa", "anio", "pib_ccaa_anual"]], on=["codigo_ine_ccaa", "anio"], how="left").drop(columns="anio")
    p = p.merge(sh, on="trimestre", how="left")
    for c, m in [("parados_epa", "agregado_provincias_suma"), ("tasa_paro_epa", "agregado_provincias_ratio_de_sumas"),
                 ("hip_n", "agregado_suma_3_meses_y_provincias"), ("hip_importe", "agregado_suma_3_meses_y_provincias")]:
        p[f"{c}_metodo"] = np.where(p[c].notna(), m, "")
        p[f"{c}_interp"] = False
    p["pib_ccaa_q_interp"] = p["pib_ccaa_q_metodo"].eq("interpolacion_loglineal_entre_anclas_T3")
    p["pib_ccaa_anual_interp"] = False
    p["vut_viviendas_interp"] = p["vut_viviendas_interp"].fillna(False).astype(bool)
    p = anade_ln(p, ["parados_epa", "hip_n", "hip_importe", "pib_ccaa_q", "vut_viviendas"], "codigo_ine_ccaa")
    p = p.sort_values(["codigo_ine_ccaa", "trimestre"]).reset_index(drop=True)
    p.to_csv(OUT / "panel_ccaa_q_v7.csv", index=False)

    # ------------------------------- panel provincial trimestral
    pq = pd.DataFrame([(c, t) for c in PROVS for t in sorted({f"{y}Q{q}" for y in range(2002, 2027) for q in range(1, 5)} - {"2026Q3", "2026Q4"})],
                      columns=["cod_prov", "trimestre"])
    for k in ["epa_q", "hip_q", "etdp_q", "ipc_q", "iniciadas_q", "terminadas_q", "vt_q"]:
        pq = pq.merge(d[k], on=["cod_prov", "trimestre"], how="left")
    pq["cod_ccaa"] = pq["cod_prov"].map(PROV_A_CCAA)
    pq = anade_ln(pq, ["hip_n", "hip_importe", "compraventas", "parados_epa", "valor_tasado"], "cod_prov")
    pq.to_csv(OUT / "panel_prov_q_v7.csv", index=False)

    # ------------------------------- panel provincial anual 2002-2024
    pq["anio"] = pq["trimestre"].str[:4].astype(int)
    g = pq.groupby(["cod_prov", "anio"])
    cnt = g["hip_n"].count()
    pa_ = pd.DataFrame(index=cnt.index)
    for c in ["hip_n", "hip_importe", "compraventas", "iniciadas", "terminadas"]:
        pa_[c] = g[c].sum(min_count=4).where(g[c].count() == 4)
    for c in ["ocupados_epa", "parados_epa", "valor_tasado", "ipc_alquiler_indice", "ipc_alquiler_yoy"]:
        pa_[c] = g[c].mean().where(g[c].count() == 4)
    pa_ = pa_.reset_index()
    pa_ = pa_[pa_["anio"].between(2002, 2024)]
    allp = pd.DataFrame([(c, y) for c in PROVS for y in range(2002, 2025)], columns=["cod_prov", "anio"])
    allp = allp.merge(d["padron_a"], on=["cod_prov", "anio"], how="left").merge(pa_, on=["cod_prov", "anio"], how="left")
    for k in ["iniciadas_a", "terminadas_a", "pib_a", "ipva_a"]:
        allp = allp.merge(d[k], on=["cod_prov", "anio"], how="left")
    va = d["vut_obs"].groupby(["cod_prov", "anio"], as_index=False)["vut_viviendas"].mean()
    allp = allp.merge(va, on=["cod_prov", "anio"], how="left")
    allp["cod_ccaa"] = allp["cod_prov"].map(PROV_A_CCAA)
    from_holdout = {}
    try:
        import holdout  # noqa: PLC0415  (solo funciones puras; no abre data/sealed)
        from_holdout = {"v2": holdout.provincias_selladas(), "v6": holdout.provincias_selladas_v6()}
    except Exception as ex:  # pragma: no cover
        from_holdout = {"error": str(ex)}
    allp["prov_sellada_v2"] = allp["cod_prov"].isin(from_holdout.get("v2", []))
    allp["prov_sellada_v6"] = allp["cod_prov"].isin(from_holdout.get("v6", []))
    allp["anio_embargo_v2"] = allp["anio"] >= 2024
    allp = anade_ln(allp, ["pob_total", "pob_extranj", "ocupados_epa", "parados_epa", "compraventas", "hip_n", "hip_importe",
                           "iniciadas", "terminadas", "valor_tasado", "ipva_indice", "pib_miles_eur"], "cod_prov")
    allp.to_csv(OUT / "panel_prov_a_v7.csv", index=False)

    docs(p, pq, allp, meta, from_holdout)
    res = resultado(p, pq, allp, meta, from_holdout)
    return res


# ------------------------------------------------------------------------------------------------ documentación
def docs(p, pq, pa, meta, hold) -> None:
    A = "ine_v2_epa_prov.csv"
    PQ = "panel_ccaa_q_v7"
    R = [
        ("parados_epa", "Parados EPA, suma de provincias de la CCAA", "miles de personas", "INE EPA tabla 65345, medida EPA_parados", A, "CCAA", "T", "agregado", 1, p, PQ),
        ("ocupados_epa_prov", "Ocupados EPA, suma de provincias (contraste con ocupados CCAA)", "miles de personas", "INE EPA 65345 EPA_ocupados", A, "CCAA", "T", "agregado", 2, p, PQ),
        ("tasa_paro_epa", "Parados/(parados+ocupados) provinciales agregados", "%", "INE EPA 65345", A, "CCAA", "T", "agregado", 1, p, PQ),
        ("hip_n", "Hipotecas constituidas sobre viviendas, número", "número", "INE Hipotecas, serie HPT por provincia, hipotecas_viviendas_numero", "ine_v2_hipotecas_prov.csv", "CCAA", "T (de M)", "agregado: suma 3 meses y provincias; NaN si falta un mes o provincia", 1, p, PQ),
        ("hip_importe", "Importe de hipotecas sobre viviendas", "miles de euros", "INE Hipotecas, hipotecas_viviendas_importe", "ine_v2_hipotecas_prov.csv", "CCAA", "T (de M)", "agregado (idem)", 1, p, PQ),
        ("zt_n_municipios", "Municipios en zona tensionada vigente al cierre del trimestre (alcance parcial cuenta como municipio)", "número", "Resoluciones de zonas tensionadas, v3/zonas_tensionadas_v3.csv (fecha_efecto, fecha_fin_prevista)", "v3/zonas_tensionadas_v3.csv", "CCAA", "T", "observado (evento)", 1, p, PQ),
        ("zt_cuota_municipios", "Municipios en zona tensionada / municipios de la CCAA (diccionario INE 2026)", "proporción", "idem + ine_diccionario_municipios_2026.xlsx", "v3/zonas_tensionadas_v3.csv+ine_diccionario_municipios_2026.xlsx", "CCAA", "T", "observado/derivado", 1, p, PQ),
        ("zt_declarada", "Al menos un municipio en zona tensionada vigente (Ley 12/2023, art. 18)", "0/1", "idem", "v3/zonas_tensionadas_v3.csv", "CCAA", "T", "observado (evento)", 1, p, PQ),
        ("tope_rentas_ccaa", "Tope de rentas autonómico vigente al cierre del trimestre (E09: Ley catalana 11/2020, 2020-09-22 a 2022-04-08, anulación parcial STC 37/2022)", "0/1", "v2_eventos_politica.csv, E09 (BOE)", "v2_eventos_politica.csv", "CCAA", "T", "observado (evento)", 1, p, PQ),
        ("tope_rentas_ccaa_frac", "Fracción de días del trimestre con tope vigente (E09)", "proporción", "idem", "v2_eventos_politica.csv", "CCAA", "T", "derivado", 1, p, PQ),
        ("tope_rentas_ccaa_alt_v3", "Tope vigente con la ventana de la ley según cataluna_contencion_rentas_v3 (hasta 2021-09-21); se reporta junto a E09 porque las ventanas difieren", "0/1", "v3/cataluna_contencion_rentas_v3.csv", "v3/cataluna_contencion_rentas_v3.csv", "CCAA", "T", "observado (evento)", 1, p, PQ),
        ("vut_regulacion_ccaa", "Norma autonómica de viviendas de uso turístico vigente (E23 Cataluña 2023-11-09, E24 C. Valenciana 2024-08-08, E25 Baleares 2025-04-16, E26 Canarias 2025-12-13)", "0/1", "v2_eventos_politica.csv", "v2_eventos_politica.csv", "CCAA", "T", "observado (evento)", 1, p, PQ),
        ("ley12_2023_nac", "Ley 12/2023 en vigor (2023-05-26) [COMÚN nacional]", "0/1", "v2_eventos_politica E14 y v3/eventos_v3", "v2_eventos_politica.csv+v3/eventos_v3.csv", "Nacional", "T", "observado (evento)", 2, p, PQ),
        ("tope_actualiz_rentas_nac", "Tope a la actualización anual de rentas (E11, 2022-03-31 a 2024-12-31) [COMÚN nacional]", "0/1", "v2_eventos_politica E11", "v2_eventos_politica.csv", "Nacional", "T", "observado (evento)", 1, p, PQ),
        ("registro_unico_arrend_nac", "Registro Único de Arrendamientos (RD 1312/2024, en vigor 2025-01-02) [COMÚN nacional]", "0/1", "v2_eventos_politica E22", "v2_eventos_politica.csv", "Nacional", "T", "observado (evento)", 2, p, PQ),
        ("pib_ccaa_anual", "PIB a precios corrientes, suma de provincias (CRE 80109); control; el valor anual se repite en los 4 trimestres sin interpolar", "miles de euros", "INE CRE 80109 PIB_precios_corrientes", "ine_v2_cre.csv", "CCAA", "A", "agregado", 1, p, PQ),
        ("pib_ccaa_q", "PIB trimestralizado: ancla en T3, log-lineal entre anclas, sin extrapolar (huecos tras el último ancla); solo robustez", "miles de euros", "idem", "ine_v2_cre.csv", "CCAA", "A->T", "interpolado (ver pib_ccaa_q_metodo / _interp)", 1, p, PQ),
        ("vut_viviendas", "Viviendas turísticas (INE experimental), suma de provincias; interpolación lineal entre fechas observadas; sin extrapolar", "número", "INE VUT tabla 39364 viviendas_turisticas", "ine_v2_vut.csv", "CCAA", "S/irregular -> T", "observado en fechas de publicación; interpolado entre ellas (vut_viviendas_interp)", 1, p, PQ),
        ("exp_hip_importe_pib_1519", "Exposición: importe medio anual de hipotecas / PIB medio, 2015-2019 (predeterminada, constante en el tiempo) ", "%", "INE Hipotecas / CRE", "ine_v2_hipotecas_prov.csv+ine_v2_cre.csv", "CCAA", "const.", "derivado", 1, p, PQ),
        ("exp_hip_n_1000hab_1519", "Exposición: hipotecas anuales medias por 1.000 habitantes (padrón 1 ene), 2015-2019", "número", "INE Hipotecas / padrón ECP", "ine_v2_hipotecas_prov.csv+ine_v2_padron_prov_pais.csv", "CCAA", "const.", "derivado", 1, p, PQ),
        ("nac_tipo_hip", "COMÚN: tipo hipotecario nacional (nacional_q). No usar como regresor regional sin interacción", "%", "nacional_q.csv (BdE/BCE)", "bde_tipo_hipotecario_referencia.csv+ecb_tipo_hipotecario_es.csv", "Nacional", "T", "heredado (ver nac_*_interp)", 2, p, PQ),
        ("nac_euribor", "COMÚN: Euribor 12m. Sin interacción no es regresor regional", "%", "nacional_q.csv (BCE)", "ecb_euribor1y.csv", "Nacional", "T", "heredado", 1, p, PQ),
        ("nac_credito_nuevo", "COMÚN: crédito nuevo a vivienda. Sin interacción no es regresor regional", "según nacional_q", "nacional_q.csv (BCE)", "ecb_nuevo_credito_vivienda_es.csv", "Nacional", "T", "heredado", 1, p, PQ),
        ("nac_tipo_bce", "COMÚN: tipo oficial BCE. Sin interacción no es regresor regional", "%", "nacional_q.csv (BCE)", "ecb_tipo_oficial.csv", "Nacional", "T", "heredado", 1, p, PQ),
        # provincial trimestral / anual
        ("ocupados_epa, parados_epa", "Ocupados y parados EPA provinciales (anual = media de 4 trimestres)", "miles de personas", "INE EPA 65345", A, "Provincia", "T / A", "observado / media", 1, pq, "panel_prov_q_v7 y panel_prov_a_v7"),
        ("hip_n, hip_importe", "Hipotecas sobre vivienda, número e importe (anual = suma de 4 trimestres)", "número / miles de euros", "INE Hipotecas", "ine_v2_hipotecas_prov.csv", "Provincia", "M->T->A", "agregado", 1, pq, "ambos"),
        ("compraventas", "Compraventas de viviendas ETDP, total (anual = suma)", "número", "INE ETDP 6150, desglose total", "ine_v2_etdp_prov.csv", "Provincia", "M->T->A", "agregado", 1, pq, "ambos"),
        ("iniciadas, terminadas", "Viviendas libres iniciadas y terminadas (MIVAU; mensual->T, y anual de tabla anual 3.1/3.2)", "viviendas", "MIVAU sedal 32100500/32101000 (mensual) y 32200500/32201000 (anual)", "mivau_v2_iniciadas_terminadas_prov.csv", "Provincia", "M->T->A", "agregado; casadas por puente de nombres (sin código en origen)", 1, pq, "ambos"),
        ("iniciadas_anual_tabla, terminadas_anual_tabla", "Idem, tabla anual oficial (contraste con la suma mensual)", "viviendas", "MIVAU sedal 32200500/32201000", "mivau_v2_iniciadas_terminadas_prov.csv", "Provincia", "A", "observado", 1, pa, "panel_prov_a_v7"),
        ("valor_tasado", "Valor tasado medio vivienda libre (anual = media de 4 trimestres)", "euros/m2", "MIVAU sedal 35101000", "mivau_valor_tasado_nacional_ccaa_prov.csv", "Provincia", "T / A", "observado / media; puente de nombres", 1, pq, "ambos"),
        ("ipc_alquiler_indice, ipc_alquiler_yoy", "IPC alquiler de vivienda: índice y variación anual (media del periodo); stock de alquileres, no contratos nuevos", "índice / %", "INE IPC tabla 76142", "ine_v2_ipc_alquiler_prov.csv", "Provincia", "M->T->A", "media", 1, pq, "ambos"),
        ("pob_total, pob_extranj", "Población residente a 1 de enero, total y extranjera (ECP/padrón)", "personas", "INE ECP 77023", "ine_v2_padron_prov_pais.csv", "Provincia", "A", "observado", 1, pa, "panel_prov_a_v7"),
        ("pib_miles_eur", "PIB a precios corrientes (CRE 80109)", "miles de euros", "INE CRE 80109", "ine_v2_cre.csv", "Provincia", "A", "observado", 1, pa, "panel_prov_a_v7"),
        ("ipva_indice", "Índice de precios de vivienda en alquiler (IPVA, base SERPAVI), total; 48 provincias, desde 2011; stock", "índice", "INE IPVA, IPVA_indice Total", "ine_v2_ipva.csv", "Provincia", "A", "observado", 1, pa, "panel_prov_a_v7"),
        ("vut_viviendas", "Viviendas turísticas, media de las fechas publicadas en el año; desde 2020", "número", "INE VUT 39364", "ine_v2_vut.csv", "Provincia", "A", "media de observaciones", 1, pa, "panel_prov_a_v7"),
    ]
    L = ["# Diccionario V7 (R1: paneles regionales)", "",
         "Generado por `src/v7/r1_panel.py`. Variables heredadas del panel v1-v6 (ipv, ocupados, etc.): ver `docs/diccionario_variables.md`. "
         "Capa: C1 solo si hay >=2 fuentes; C4 si una. Prefijos `ln_`, `d_ln_`, `d4_ln_` para logaritmos y diferencias (no listados uno a uno).", "",
         "| variable | definición | unidad | fuente (fichero y serie) | descarga/edición | nivel | frec. | periodo | método | capa | % NaN |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for v, de, un, fu, ar, ni, fr, me, ns, df, pn in R:
        vs = [x.strip() for x in v.split(",")]
        col = vs[0]
        s = df[col] if col in df else None
        nan = f"{100 * s.isna().mean():.1f} % ({pn})" if s is not None else "n/d"
        per = ""
        if s is not None:
            key = "trimestre" if "trimestre" in df else "anio"
            ok = df.loc[s.notna(), key]
            per = f"{ok.min()}-{ok.max()}" if len(ok) else "vacío"
        ncol = "C1" if ns >= 2 else "C4"
        L.append(f"| {v} | {de} | {un} | {fu} | {descarga(ar)} | {ni} | {fr} | {per} | {me} | {ncol} | {nan} |")
    L += ["", "## Interpolaciones y agregaciones temporales (regla 4)", "",
          "- `pib_ccaa_q` (`pib_ccaa_q_metodo`, `pib_ccaa_q_interp`): PIB anual CRE; ancla en el T3, interpolación log-lineal entre anclas; sin extrapolación (NaN antes del primer ancla y tras 2025T3). Solo robustez. Renta de los hogares por CCAA: no existe en data/raw (solo nacional CNT y Eurostat nacional): hueco.",
          "- `vut_viviendas` CCAA: interpolación lineal entre fechas publicadas (2020M08...2026M05); `vut_viviendas_interp` marca las filas interpoladas; NaN fuera del rango.",
          "- Hipotecas, parados, compraventas, iniciadas, terminadas: suma mensual->trimestral->anual solo con todos los meses/trimestres presentes; sin interpolación (`*_interp` = False).",
          "- Las variables `nac_*` conservan los indicadores `_interp` de `nacional_q.csv`.", "",
          "## Eventos regulatorios (fecha de entrada en vigor; verificación en v2_eventos_politica.csv, 2026-10-10)", "",
          f"- Ley 12/2023: inicio v2 {meta['ley12_2023_inicio_v2']}, v3 {meta['ley12_2023_inicio_v3']} (coinciden: {meta['ley12_coincide_v2_v3']}).",
          "- Convención de dummies: vigente el último día del trimestre; la columna `_frac` da la fracción de días. Con ello el tope catalán (E09, 2020-09-22 a 2022-04-08) vale 1 en 2020T3-2022T1; "
          f"con la ventana de la ley (v3, {meta['tope_rentas_cat_v3_ventana']}) la variante `_alt_v3` vale 1 en 2020T3-2021T2. Se reportan ambas.",
          f"- Zonas tensionadas: v2 y v3 son la misma relación ({meta['zonas_v2_igual_v3']}): una sola fuente (C4).", "",
          "## Nota de contaminación de validaciones selladas", "",
          f"`panel_prov_a_v7.csv`/`panel_prov_q_v7.csv` incluyen las 52 provincias, también las selladas en v2 {hold.get('v2')} y en v6 {hold.get('v6')}, y 2024 "
          "(año de embargo de v2). Se construyen solo desde data/raw (no desde los paneles de entrenamiento) y no abren data/sealed. Es correcto "
          "usarlos solo si V7 no reutiliza esas provincias/años para evaluar hipótesis confirmatorias de v2 o v6; las columnas `prov_sellada_v2`, `prov_sellada_v6` y `anio_embargo_v2` "
          "permiten excluirlas. Para hipótesis nuevas de V7 hace falta un sellado propio. Los backtests con el panel CCAA: «informativo, muestra ya vista en v1».", "",
          "## Puente de nombres MIVAU", "", "Provincias sin casar (sin código en origen): " + json.dumps(NO_CASADOS, ensure_ascii=False)]
    DOC.write_text("\n".join(L) + "\n", encoding="utf-8")


def resultado(p, pq, pa, meta, hold) -> dict:
    nuevas = [c for c in p.columns if c not in pd.read_csv(RAIZ / "data/processed/panel_ccaa_q.csv", nrows=1).columns]
    cob = {}
    for c in nuevas:
        if c.startswith(("ln_", "d_ln_", "d4_ln_")) or c.endswith(("_metodo", "_interp")):
            continue
        s = p[c]
        ok = p.loc[s.notna(), "trimestre"]
        cob[c] = {"pct_nan": round(100 * s.isna().mean(), 1), "desde": ok.min() if len(ok) else None, "hasta": ok.max() if len(ok) else None}
    cobp = {c: round(100 * pa[c].isna().mean(), 1) for c in pa.columns if not c.startswith(("ln_", "d_ln_", "d4_ln_"))}
    res = {"rama": "v7/R1", "pregunta": "Construcción del panel regional (17 CCAA x trimestre) y provincial (52 prov. x año/trimestre) para V7",
           "capa": "C4", "datos": ["panel_ccaa_q_v7.csv", "panel_prov_a_v7.csv", "panel_prov_q_v7.csv"],
           "N": {"ccaa_q": int(len(p)), "prov_a": int(len(pa)), "prov_q": int(len(pq))}, "metodo": "agregación por código INE; interpolación declarada",
           "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
           "diagnosticos": {"cobertura_ccaa": cob, "pct_nan_prov_anual": cobp, "eventos": meta, "provincias_selladas": hold,
                            "provincias_sin_casar_mivau": NO_CASADOS},
           "fuera_muestra": None, "medida_precio": "no aplica (panel de datos)",
           "notas": "Panel CCAA no sellado y ya usado en v1: backtests informativos. Panel provincial incluye provincias selladas v2/v6; ver docs/v7/diccionario.md."}
    (OUT_R / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return res


if __name__ == "__main__":
    r = main()
    print(json.dumps(r["N"]), "OK")
