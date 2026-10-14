"""V10-B2a · Atlas «quién lo sufre»: indicadores descriptivos con microdatos ECV (2018-2025) y EPA (2018T1-2026T2).

Solo descriptivo (sin modelos). Entradas: data/raw/v9/ine_microdatos/{ecv,epa} (no versionados; `make datos_v9`).
Salida: output/v10/atlas/a_quien_ecv.csv, a_quien_epa.csv y a_contraste_eurostat.csv.

Definiciones (ECV; unidad de análisis: personas, ponderadas con RB050; los datos del hogar se asignan a sus miembros):
- tenencia: HH021 (1 propiedad sin hipoteca, 2 con hipoteca, 3 alquiler a precio de mercado, 4 alquiler inferior al
  de mercado, 5 cesión);
- sobrecarga_30 / sobrecarga_40: gastos de vivienda netos de ayudas a la vivienda sobre renta disponible neta de esas
  ayudas, (12·HH070 − HY070N) / (HY020 − HY070N), por encima del 30 % / 40 % (definición de Eurostat para el 40 %);
  con renta no positiva y gastos positivos se cuenta como sobrecarga;
- esfuerzo_alquiler: 12·HH060 / HY020 en hogares con alquiler a precio de mercado (media y proporción >30 % y >40 %);
- esfuerzo_hipoteca: 12·cuotahip / HY020 en propietarios con hipoteca (la cuota incluye amortización, a diferencia de
  HH070, que solo recoge intereses);
- hacinamiento: definición de Eurostat (una habitación para el hogar, una por pareja, una por persona de 18 o más,
  una por cada dos de 12-17 del mismo sexo, una por cada dos menores de 12) frente a HH030;
- antes de 2021 la edad se calcula con el año de nacimiento (RB080) y la nacionalidad solo existe para los adultos
  (PB220A); los menores quedan sin nacionalidad en esos años;
- grupos: total, CCAA (DB040), decil de renta equivalente (HY020/HX240, deciles ponderados por personas), edad
  (RB081), nacionalidad (RB290: España, resto de la UE, resto del mundo), tipo de hogar (HX060 agrupado) y tenencia.
EPA (personas de 16 o más; FACTOREL): proporción que vive con al menos uno de sus padres (NPADRE o NMADRE ≠ 0) por
tramo de edad quinquenal, CCAA y nacionalidad (NAC1), media de los cuatro trimestres del año.

Intervalos: linealización de Taylor con el hogar como unidad primaria y muestreo con reposición. Los ficheros públicos
no traen estratos ni secciones, así que los intervalos no recogen el efecto del diseño (son algo estrechos).
Celdas con menos de 50 observaciones: se suprimen; de 50 a 149: marca `muestra_pequena`.
Capa: C4 (fuente única) salvo las series nacionales que coinciden con la tabla oficial de Eurostat (ilc_lvho07a/c,
ilc_lvho05a; data/raw/v5) dentro de 0,5 puntos en TODOS los años, que pasan a C1 (microdatos propios y tabla oficial).
La sobrecarga del 40 % (total y por tenencia) cumple; el hacinamiento queda unos 0,8 puntos por debajo de Eurostat
todos los años (diferencia de definición no resuelta) y se queda en C4.
"""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
MICRO = RAIZ / "data" / "raw" / "v9" / "ine_microdatos"
OUT = RAIZ / "output" / "v10" / "atlas"
Z = 1.959964
N_MIN, N_AVISO = 50, 150
CCAA_NUTS = {"ES11": "12", "ES12": "03", "ES13": "06", "ES21": "16", "ES22": "15", "ES23": "17", "ES24": "02",
             "ES30": "13", "ES41": "07", "ES42": "08", "ES43": "11", "ES51": "09", "ES52": "10", "ES53": "04",
             "ES61": "01", "ES62": "14", "ES63": "18", "ES64": "19", "ES70": "05"}
TIPO_HOGAR = {1: "unipersonal <65", 2: "unipersonal <65", 4: "unipersonal <65", 5: "unipersonal <65",
              3: "unipersonal 65+", 6: "unipersonal 65+", 7: "pareja sin hijos", 8: "pareja sin hijos",
              9: "otros sin hijos", 10: "monoparental", 11: "pareja con hijos", 12: "pareja con hijos",
              13: "pareja con hijos", 14: "otros con hijos"}
TENENCIA = {1: "propiedad sin hipoteca", 2: "propiedad con hipoteca", 3: "alquiler de mercado",
            4: "alquiler inferior al de mercado", 5: "cesión gratuita"}
NACIONALIDAD = {1: "España", 2: "resto de la UE", 3: "resto del mundo"}


# ------------------------------------------------------------------------------------------------ lectura
def _leer(zip_anual: zipfile.ZipFile, fichero: str, anio: int) -> pd.DataFrame:
    interno = next(n for n in zip_anual.namelist() if n.startswith(f"ECV_{fichero}_{anio}") and n.endswith(".zip"))
    with zipfile.ZipFile(io.BytesIO(zip_anual.read(interno))) as z:
        nombre = next(n for n in z.namelist() if n.upper().startswith("CSV/ECV_") and n.endswith((".csv", ".tab")))
        return pd.read_csv(io.BytesIO(z.read(nombre)), sep="\t", low_memory=False)


def ecv_anio(anio: int) -> pd.DataFrame:
    with zipfile.ZipFile(MICRO / "ecv" / f"datos_{anio}.zip") as z:
        d = _leer(z, "Td", anio)[["DB030", "DB040", "DB090"]]
        h = _leer(z, "Th", anio)
        r = _leer(z, "Tr", anio)
        if "RB290" not in r:   # antes de 2021: nacionalidad solo de adultos (PB220A del fichero P; mismos códigos)
            pa = _leer(z, "Tp", anio)[["PB030", "PB220A"]].rename(columns={"PB030": "RB030", "PB220A": "RB290"})
            r = r.merge(pa, on="RB030", how="left")
    if "RB081" not in r:       # edad a 31 de diciembre del año anterior a la encuesta
        r["RB081"] = anio - 1 - pd.to_numeric(r.RB080, errors="coerce")
    h = h[["HB030", "HY020", "HY070N", "HH021", "HH030", "HH060", "HH070", "cuotahip", "HX060", "HX240"]].copy()
    r = r[["RB030", "RB050", "RB081", "RB090", "RB240", "RB290"]].copy()
    r["HB030"] = r.RB030 // 100
    p = r.merge(h, on="HB030", how="inner").merge(d, left_on="HB030", right_on="DB030", how="inner")
    for c in ("HY020", "HY070N", "HH060", "HH070", "cuotahip", "HX240", "HH030", "RB050"):
        p[c] = pd.to_numeric(p[c], errors="coerce")
    p["anio"] = anio
    return p


def hacinamiento(p: pd.DataFrame) -> pd.Series:
    """Habitaciones necesarias (Eurostat) frente a HH030, por hogar; devuelve 0/1 por persona."""
    edad = pd.to_numeric(p.RB081, errors="coerce")
    pareja = pd.to_numeric(p.RB240, errors="coerce").fillna(0) > 0
    g = p.assign(edad=edad, pareja=pareja, sexo=p.RB090)
    filas = []
    for hb, x in g.groupby("HB030"):
        parejas = int(x.pareja.sum() // 2)
        adultos_solos = int(((x.edad >= 18) & ~x.pareja).sum())
        ad = x[(x.edad >= 12) & (x.edad < 18)]
        h = int((ad.sexo == 1).sum())
        m = int((ad.sexo == 2).sum())
        pares_ad = h // 2 + m // 2
        sueltos = h % 2 + m % 2
        ninos = int((x.edad < 12).sum())
        # los adolescentes sueltos pueden compartir con un menor de 12
        empareja = min(sueltos, ninos)
        necesarias = 1 + parejas + adultos_solos + pares_ad + sueltos + int(np.ceil((ninos - empareja) / 2))
        filas.append((hb, necesarias))
    nec = pd.Series(dict(filas))
    return (p.HB030.map(nec) > p.HH030).astype(float).where(p.HH030.notna())


def preparar(p: pd.DataFrame) -> pd.DataFrame:
    p = p[p.RB050 > 0].copy()
    ingreso = p.HY020 - p.HY070N.fillna(0)
    coste = 12 * p.HH070 - p.HY070N.fillna(0)
    carga = np.where(ingreso > 0, coste / ingreso, np.where(coste > 0, np.inf, 0))
    p["sobrecarga_30"] = (carga > 0.30).astype(float)
    p["sobrecarga_40"] = (carga > 0.40).astype(float)
    p.loc[p.HH070.isna(), ["sobrecarga_30", "sobrecarga_40"]] = np.nan
    ten = pd.to_numeric(p.HH021, errors="coerce")
    p["tenencia"] = ten.map(TENENCIA)
    alq = (ten == 3) & (p.HY020 > 0) & (p.HH060 > 0)
    p["esfuerzo_alquiler"] = np.where(alq, 12 * p.HH060 / p.HY020, np.nan)
    p["esfuerzo_alquiler_30"] = np.where(alq, (p.esfuerzo_alquiler > 0.30).astype(float), np.nan)
    p["esfuerzo_alquiler_40"] = np.where(alq, (p.esfuerzo_alquiler > 0.40).astype(float), np.nan)
    hip = (ten == 2) & (p.HY020 > 0) & (p.cuotahip > 0)
    p["esfuerzo_hipoteca"] = np.where(hip, 12 * p.cuotahip / p.HY020, np.nan)
    p["esfuerzo_hipoteca_30"] = np.where(hip, (p.esfuerzo_hipoteca > 0.30).astype(float), np.nan)
    for k, v in TENENCIA.items():
        p[f"tenencia_{k}"] = np.where(ten.notna(), (ten == k).astype(float), np.nan)
    p["hacinamiento"] = hacinamiento(p)
    # grupos
    p["ccaa"] = p.DB040.map(CCAA_NUTS)
    eq = p.HY020 / p.HX240
    p["decil_renta"] = np.nan
    for _, x in p.groupby("anio"):
        orden = eq.loc[x.index].dropna().sort_values().index
        cw = x.loc[orden, "RB050"].cumsum() / x.loc[orden, "RB050"].sum()
        p.loc[orden, "decil_renta"] = np.clip(np.ceil(cw * 10), 1, 10)
    edad = pd.to_numeric(p.RB081, errors="coerce")
    p["edad"] = pd.cut(edad, [-1, 17, 29, 34, 44, 64, 200], labels=["0-17", "18-29", "30-34", "35-44", "45-64", "65+"]).astype(str)
    p["nacionalidad"] = pd.to_numeric(p.RB290, errors="coerce").map(NACIONALIDAD)
    p["tipo_hogar"] = pd.to_numeric(p.HX060, errors="coerce").map(TIPO_HOGAR)
    return p


# ------------------------------------------------------------------------------------------------ estimación
def media_lineal(y: pd.Series, w: pd.Series, cl: pd.Series) -> tuple[float, float, int]:
    """Media ponderada (razón) y su error típico por linealización con conglomerado = hogar."""
    m = y.notna() & w.notna()
    y, w, cl = y[m], w[m], cl[m]
    n = len(y)
    if n == 0:
        return np.nan, np.nan, 0
    sw = w.sum()
    est = float((w * y).sum() / sw)
    z = (w * (y - est) / sw).groupby(cl.values).sum()
    k = len(z)
    se = float(np.sqrt(k / (k - 1) * ((z - z.mean()) ** 2).sum())) if k > 1 else np.nan
    return est, se, n


def mediana_woodruff(y: pd.Series, w: pd.Series, cl: pd.Series) -> tuple[float, float, float, int]:
    """Mediana ponderada e IC 95 % de Woodruff (se linealiza la proporción por debajo de la mediana)."""
    m = y.notna() & w.notna() & np.isfinite(y)
    y, w, cl = y[m], w[m], cl[m]
    n = len(y)
    if n == 0:
        return np.nan, np.nan, np.nan, 0
    o = np.argsort(y.values)
    yv, cw = y.values[o], np.cumsum(w.values[o]) / w.values.sum()

    def q(p):
        return float(yv[min(np.searchsorted(cw, min(max(p, 0), 1)), n - 1)])
    med = q(0.5)
    _, se, _ = media_lineal((y <= med).astype(float), w, cl)
    return med, q(0.5 - Z * se), q(0.5 + Z * se), n


MEDIANAS = {"esfuerzo_alquiler_mediana": "esfuerzo_alquiler", "esfuerzo_hipoteca_mediana": "esfuerzo_hipoteca"}
INDICADORES = {"sobrecarga_30": "%", "sobrecarga_40": "%", "esfuerzo_alquiler_30": "%",
               "esfuerzo_alquiler_40": "%", "esfuerzo_hipoteca_30": "%", "hacinamiento": "%",
               **{f"tenencia_{k}": "%" for k in TENENCIA}}
GRUPOS = ["total", "ccaa", "decil_renta", "edad", "nacionalidad", "tipo_hogar", "tenencia"]


def tabla_ecv(p: pd.DataFrame) -> pd.DataFrame:
    filas = []
    p = p.assign(total="Total")
    for anio, x in p.groupby("anio"):
        for g in GRUPOS:
            for cat, y in x.groupby(g):
                if cat in ("nan", None) or pd.isna(cat):
                    continue
                for ind in INDICADORES:
                    if g == "tenencia" and ind.startswith("tenencia_"):
                        continue
                    est, se, n = media_lineal(y[ind], y.RB050, y.HB030)
                    if n < N_MIN or np.isnan(est):
                        continue
                    filas.append({"anio": anio, "grupo": g, "categoria": str(int(cat)) if g == "decil_renta" else str(cat),
                                  "indicador": ind, "valor": 100 * est, "ee": 100 * se,
                                  "ic95_inf": 100 * (est - Z * se), "ic95_sup": 100 * (est + Z * se), "n_muestral": n,
                                  "muestra_pequena": n < N_AVISO})
                for ind, base in MEDIANAS.items():
                    med, lo, hi, n = mediana_woodruff(y[base], y.RB050, y.HB030)
                    if n < N_MIN:
                        continue
                    filas.append({"anio": anio, "grupo": g, "categoria": str(int(cat)) if g == "decil_renta" else str(cat),
                                  "indicador": ind, "valor": 100 * med, "ee": np.nan, "ic95_inf": 100 * lo,
                                  "ic95_sup": 100 * hi, "n_muestral": n, "muestra_pequena": n < N_AVISO})
    t = pd.DataFrame(filas)
    t["unidad"] = np.where(t.indicador.str.endswith("_mediana"), "% de la renta disponible del hogar (mediana)", "% de personas")
    t["fuente"] = "INE, Encuesta de Condiciones de Vida (microdatos); cálculo propio"
    t["fecha_dato"] = t.anio.astype(str) + "-12-31"
    t["capa"] = "C4"
    t["nota"] = "IC por linealización con conglomerado hogar; sin estratos (no publicados): IC algo estrechos"
    return t


EUROSTAT = {  # (fichero, columna de desagregación) -> indicador propio y mapa de categorías
    ("ca_eurostat_ilc_lvho07a.csv", None): ("sobrecarga_40", {None: ("total", "Total")}),
    ("cc_eurostat_ilc_lvho07c.csv", "tenure"): ("sobrecarga_40", {"TOTAL": ("total", "Total"),
                                                "OWN_NL": ("tenencia", "propiedad sin hipoteca"),
                                                "OWN_L": ("tenencia", "propiedad con hipoteca"),
                                                "RENT_MKT": ("tenencia", "alquiler de mercado")}),
    ("ca_eurostat_ilc_lvho05a.csv", None): ("hacinamiento", {None: ("total", "Total")}),
}
TOL_C1 = 0.5   # puntos porcentuales, en TODOS los años del indicador y la categoría


def contraste_eurostat(t: pd.DataFrame) -> pd.DataFrame:
    """Contraste de los totales propios con las tablas oficiales de Eurostat (España). Coincidencia ≤1 punto → C1."""
    filas = []
    for (fichero, col), (ind, mapa) in EUROSTAT.items():
        e = pd.read_csv(RAIZ / "data/raw/v5" / fichero, dtype=str)
        e = e[e.geo == "ES"]
        for r in e.itertuples():
            clave = getattr(r, col) if col else None
            if clave not in mapa:
                continue
            g, cat = mapa[clave]
            propio = t[(t.anio == int(r.time)) & (t.grupo == g) & (t.categoria == cat) & (t.indicador == ind)]
            if propio.empty:
                continue
            filas.append({"anio": int(r.time), "grupo": g, "categoria": cat, "indicador": ind,
                          "valor_propio": float(propio.valor.iloc[0]), "valor_eurostat": float(r.valor),
                          "tabla_eurostat": fichero.split("_", 2)[-1].replace(".csv", "")})
    c = pd.DataFrame(filas).drop_duplicates(["anio", "grupo", "categoria", "indicador"])
    c["diferencia_pp"] = c.valor_propio - c.valor_eurostat
    c["coincide_anio"] = c.diferencia_pp.abs() <= TOL_C1
    c["coincide"] = c.groupby(["grupo", "categoria", "indicador"]).coincide_anio.transform("all")
    return c


def epa() -> pd.DataFrame:
    partes = []
    for z in sorted((MICRO / "epa").glob("datos_*t*.zip")):
        with zipfile.ZipFile(z) as zz:
            nombre = next(n for n in zz.namelist() if n.startswith("CSV/") and n.endswith((".csv", ".tab")))
            d = pd.read_csv(io.BytesIO(zz.read(nombre)), sep="\t", dtype=str)
        edad = "EDAD1" if "EDAD1" in d else "EDAD5"
        d = d[["CICLO", "CCAA", "NVIVI", edad, "NPADRE", "NMADRE", "NAC1", "FACTOREL"]].rename(columns={edad: "edad5"})
        t, yy = z.stem.split("_")[1].split("t")
        d["anio"], d["trimestre"] = 2000 + int(yy), int(t)
        partes.append(d)
    d = pd.concat(partes, ignore_index=True)
    d["edad5"] = pd.to_numeric(d.edad5, errors="coerce")
    d = d[d.edad5.isin([20, 25, 30, 35])]
    d["w"] = pd.to_numeric(d.FACTOREL, errors="coerce")
    d["con_padres"] = ((pd.to_numeric(d.NPADRE, errors="coerce").fillna(0) > 0) |
                       (pd.to_numeric(d.NMADRE, errors="coerce").fillna(0) > 0)).astype(float)
    d["nacionalidad"] = pd.to_numeric(d.NAC1, errors="coerce").map({1: "española", 2: "doble nacionalidad", 3: "extranjera"})
    d["ccaa"] = d.CCAA.str.zfill(2)
    d["hogar"] = d.CICLO + "-" + d.NVIVI
    d["tramo_edad"] = d.edad5.map({20: "20-24", 25: "25-29", 30: "30-34", 35: "35-39"})
    filas = []
    d = d.assign(total="Total")
    for (anio, tramo), x in d.groupby(["anio", "tramo_edad"]):
        nt = x.trimestre.nunique()
        for g in ("total", "ccaa", "nacionalidad"):
            for cat, y in x.groupby(g):
                est, se, n = media_lineal(y.con_padres, y.w, y.hogar)
                if n < N_MIN:
                    continue
                filas.append({"anio": anio, "trimestres": nt, "tramo_edad": tramo, "grupo": g, "categoria": cat,
                              "indicador": "vive_con_padres", "valor": 100 * est, "ee": 100 * se,
                              "ic95_inf": 100 * (est - Z * se), "ic95_sup": 100 * (est + Z * se), "n_muestral": n,
                              "muestra_pequena": n < N_AVISO})
    t = pd.DataFrame(filas)
    t["unidad"] = "% de personas del tramo de edad"
    t["fuente"] = "INE, Encuesta de Población Activa (microdatos); cálculo propio"
    t["fecha_dato"] = t.anio.astype(str) + "-" + t.trimestres.map({1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"})
    t["capa"] = "C4"
    t["posterior_prereg"] = False
    t["nota"] = np.where(t.trimestres < 4, "año incompleto: media de los trimestres disponibles", "media de 4 trimestres")
    return t


def main() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    anios = sorted(int(z.stem.split("_")[1]) for z in (MICRO / "ecv").glob("datos_*.zip"))
    p = pd.concat([preparar(ecv_anio(a)) for a in anios], ignore_index=True)
    t = tabla_ecv(p)
    c = contraste_eurostat(t)
    c.to_csv(OUT / "a_contraste_eurostat.csv", index=False, float_format="%.4f")
    ok = c[c.coincide][["anio", "grupo", "categoria", "indicador"]].assign(c1=True)
    t = t.merge(ok, how="left", on=["anio", "grupo", "categoria", "indicador"])
    t.loc[t.c1.fillna(False).astype(bool), "capa"] = "C1"
    t.loc[t.capa == "C1", "nota"] = t.nota + "; coincide con Eurostat (≤0,5 puntos todos los años)"
    t = t.drop(columns="c1")
    t.to_csv(OUT / "a_quien_ecv.csv", index=False, float_format="%.4f")
    e = epa()
    e.to_csv(OUT / "a_quien_epa.csv", index=False, float_format="%.4f")
    return {"filas_ecv": len(t), "anios_ecv": anios, "filas_epa": len(e)}


if __name__ == "__main__":
    print(main())
