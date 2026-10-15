"""V12-B6 · Condiciones de vivienda por origen (descriptivo, C4; sin modelos ni lenguaje causal).

Neutralidad: se describen condiciones de vivienda de los hogares según la nacionalidad o el lugar de nacimiento de sus
miembros; no se atribuyen responsabilidades. Las personas recién llegadas forman parte de la demanda y de la oferta de
trabajo como el resto de la población.

1. ECV 2018-último (microdatos, personas ponderadas con RB050; definiciones de src/v10/atlas_microdatos.py):
   tenencia (propiedad, alquiler a precio de mercado), sobrecarga > 30 % y > 40 %, esfuerzo del alquiler > 30 % y
   > 40 % (hogares en alquiler de mercado) y hacinamiento (Eurostat). Por año y nacionalidad (España, resto de la UE,
   resto del mundo) y, desde que la ECV lo trae, país de nacimiento (RB280). Intervalos por linealización con el hogar
   como conglomerado (sin estratos en los ficheros públicos: algo estrechos).
2. Comparación con nacionales españoles de la MISMA edad y renta: celdas edad (18-34, 35-49, 50-64, 65+) × quintil de
   renta equivalente, años agrupados 2023-último. Tasa de los españoles reponderada a la composición por edad y renta
   del grupo extranjero (estandarización directa); diferencia con IC bootstrap (200 réplicas por hogar, SEED).
3. Censo 2021 (muestra del 10 % de los hogares; persona de referencia = la de mayor edad): tenencia, superficie útil
   < 46 m², superficie por ocupante < 15 m² (indicador censal de espacio, no es el hacinamiento de Eurostat) por
   nacionalidad, país de nacimiento, periodo de llegada a España, edad de la persona de referencia y tipo de hogar.
   IC binomial con corrección por población finita (f = 0,1).
Celdas pequeñas: ECV, < 50 observaciones se suprimen (como en V10) y además se exige ≥ 10 casos con el atributo y error
relativo ≤ 30 %; Censo, ≥ 10 hogares con el atributo y error relativo ≤ 30 %.
EPA: no recoge la tenencia ni el gasto en vivienda; no se usa para estos indicadores (sí en V10 para la emancipación).
Salidas: output/v12/b6/.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output/v12/b6"
SEED = 20261010
Z = 1.959964
N_MIN, CASOS_MIN, RSE_MAX, F_CENSO = 50, 10, 0.30, 0.10
_spec = importlib.util.spec_from_file_location("atlas_v10", RAIZ / "src/v10/atlas_microdatos.py")
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)
IND = {"propiedad": None, "tenencia_3": "alquiler a precio de mercado", "sobrecarga_30": None, "sobrecarga_40": None,
       "esfuerzo_alquiler_30": None, "esfuerzo_alquiler_40": None, "hacinamiento": None}
NACIDO = {"España": "nacido en España", "UE": "nacido en otro país de la UE", "resto": "nacido fuera de la UE"}


def ecv() -> pd.DataFrame:
    import zipfile
    partes = []
    anios = sorted(int(p.stem.split("_")[1]) for p in (A.MICRO / "ecv").glob("datos_*.zip"))
    for a in anios:
        p = A.preparar(A.ecv_anio(a))
        with zipfile.ZipFile(A.MICRO / "ecv" / f"datos_{a}.zip") as z:
            r = A._leer(z, "Tr", a)
        if "RB280" in r:
            nac = pd.to_numeric(r.set_index("RB030").RB280, errors="coerce").map({1: "España", 2: "UE", 3: "resto"})
            p["nacimiento"] = p.RB030.map(nac).map(NACIDO)
        else:
            p["nacimiento"] = np.nan
        p["propiedad"] = (p.tenencia_1 + p.tenencia_2).where(p.tenencia_1.notna())
        partes.append(p)
    p = pd.concat(partes, ignore_index=True)
    p["edad_g"] = pd.cut(pd.to_numeric(p.RB081, errors="coerce"), [-1, 17, 34, 49, 64, 200], labels=["0-17", "18-34", "35-49", "50-64", "65+"]).astype(str)
    p["quintil_renta"] = np.ceil(p.decil_renta / 2)
    p["origen"] = p.nacionalidad.map({"España": "española", "resto de la UE": "UE", "resto del mundo": "fuera de la UE"})
    p["extranjera"] = np.select([p.origen.isin(["UE", "fuera de la UE"]), p.origen == "española"], ["extranjera", "española"], "sin dato")
    return p


def _fila(y: pd.Series, w: pd.Series, cl: pd.Series) -> dict | None:
    est, se, n = A.media_lineal(y, w, cl)
    casos = int((y.dropna() > 0).sum())
    if n < N_MIN or np.isnan(est):
        return None
    rse = se / est if est > 0 else np.inf
    ok = casos >= CASOS_MIN and rse <= RSE_MAX
    return {"valor": round(100 * est, 2) if ok else np.nan, "ic95_inf": round(100 * (est - Z * se), 2) if ok else np.nan,
            "ic95_sup": round(100 * (est + Z * se), 2) if ok else np.nan, "n_muestral": n, "casos": casos if ok else np.nan,
            "error_relativo": round(rse, 3) if ok else np.nan, "publicable": ok}


def tabla_anual(p: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for a, x in p.groupby("anio"):
        for g in ("origen", "nacimiento"):
            for cat, y in x.groupby(g):
                for ind in IND:
                    f = _fila(y[ind], y.RB050, y.HB030)
                    if f:
                        filas.append({"anio": a, "grupo": g, "categoria": cat, "indicador": ind, **f})
    return pd.DataFrame(filas)


def tabla_cruces(p: pd.DataFrame, desde: int) -> pd.DataFrame:
    """Nacionalidad × edad y nacionalidad × quintil de renta, años agrupados (conglomerado = hogar × año)."""
    x = p[(p.anio >= desde) & (p.edad_g != "0-17")].copy()
    x["cl"] = x.anio.astype(str) + "-" + x.HB030.astype(str)
    filas = []
    for g in ("edad_g", "quintil_renta", "tipo_hogar"):
        for (o, c), y in x.groupby(["extranjera", g]):
            for ind in IND:
                f = _fila(y[ind], y.RB050, y.cl)
                if f:
                    filas.append({"periodo": f"{desde}-{int(p.anio.max())}", "nacionalidad": o, "grupo": g, "categoria": str(c), "indicador": ind, **f})
    return pd.DataFrame(filas)


def estandarizada(p: pd.DataFrame, desde: int, B: int = 200) -> pd.DataFrame:
    """Brecha extranjera − española con la tasa española reponderada a la edad × renta del grupo extranjero."""
    x = p[(p.anio >= desde) & (p.edad_g != "0-17") & p.quintil_renta.notna() & p.extranjera.isin(["española", "extranjera"])].copy()
    x["celda"] = x.edad_g + "|" + x.quintil_renta.astype(int).astype(str)
    x["cl"] = x.anio.astype(str) + "-" + x.HB030.astype(str)
    rng = np.random.default_rng(SEED)
    hog = x.cl.unique()
    idx = x.groupby("cl").indices

    def calc(d: pd.DataFrame, ind: str) -> tuple[float, float, float]:
        d = d[d[ind].notna()]
        ex, es = d[d.extranjera == "extranjera"], d[d.extranjera == "española"]
        w_ex = ex.groupby("celda").RB050.sum() / ex.RB050.sum()
        t_es = es.groupby("celda").apply(lambda g: np.average(g[ind], weights=g.RB050))
        t_ex = np.average(ex[ind], weights=ex.RB050)
        comun = w_ex.index.intersection(t_es.index)
        std = float((w_ex[comun] * t_es[comun]).sum() / w_ex[comun].sum())
        cruda = float(np.average(es[ind], weights=es.RB050))
        return float(t_ex), cruda, std

    filas = []
    for ind in IND:
        t_ex, cruda, std = calc(x, ind)
        bs = []
        for _ in range(B):
            s = rng.choice(hog, len(hog), replace=True)
            d = x.iloc[np.concatenate([idx[h] for h in s])]
            e, _, st = calc(d, ind)
            bs.append(e - st)
        lo, hi = np.nanpercentile(bs, [2.5, 97.5])
        filas.append({"periodo": f"{desde}-{int(p.anio.max())}", "indicador": ind, "extranjera": round(100 * t_ex, 2),
                      "espanola_cruda": round(100 * cruda, 2), "espanola_misma_edad_y_renta": round(100 * std, 2),
                      "diferencia_estandarizada": round(100 * (t_ex - std), 2), "ic95_inf": round(100 * lo, 2), "ic95_sup": round(100 * hi, 2),
                      "n_extranjera": int((x.extranjera == "extranjera").sum()), "n_espanola": int((x.extranjera == "española").sum())})
    return pd.DataFrame(filas)


def censo() -> pd.DataFrame:
    h = pd.read_csv(RAIZ / "data/raw/v11/ine_censo2021/hogares_muestra_municipio_nacionalidad.csv.gz", dtype=str)
    h["n"] = pd.to_numeric(h.hogares_muestra)
    ten = pd.to_numeric(h.tenencia, errors="coerce")
    sup = pd.to_numeric(h.superficie, errors="coerce")
    supo = pd.to_numeric(h.superficie_por_ocupante, errors="coerce")
    h["propiedad"] = np.where(ten == 9, np.nan, (ten == 2).astype(float))
    h["alquiler"] = np.where(ten == 9, np.nan, (ten == 3).astype(float))
    h["superficie_menor_46m2"] = np.where(sup == 99, np.nan, (sup <= 3).astype(float))          # códigos 02-03: ≤ 45 m²
    h["menos_15m2_por_ocupante"] = np.where(supo == 99, np.nan, (supo <= 3).astype(float))      # códigos 02-03: < 15 m²
    tipo = {"01": "unipersonal", "02": "sin núcleo", "03": "sin núcleo", "04": "un núcleo", "05": "un núcleo con otras personas",
            "06": "dos núcleos o más", "07": "con personas no emparentadas", "08": "dos familias o más"}
    h["tipo_hogar_c"] = h.tipo_hogar.map(tipo)
    h["total"] = "Total"
    filas = []
    for g in ("total", "nac_primera_persona", "nacido_en_espana", "llegada_espana", "edad_primera_persona", "tipo_hogar_c"):
        for nac in ("todas", "ES", "EXT"):
            y0 = h if nac == "todas" else h[h.nac_primera_persona == nac]
            if g == "nac_primera_persona" and nac != "todas":
                continue
            for cat, y in y0.groupby(g):
                for ind in ("propiedad", "alquiler", "superficie_menor_46m2", "menos_15m2_por_ocupante"):
                    v = y.dropna(subset=[ind])
                    n = int(v.n.sum())
                    x = float((v[ind] * v.n).sum())
                    if n == 0:
                        continue
                    pr = x / n
                    se = np.sqrt(pr * (1 - pr) / n * (1 - F_CENSO))
                    rse = se / pr if pr > 0 else np.inf
                    ok = x >= CASOS_MIN and rse <= RSE_MAX
                    filas.append({"grupo": g, "nacionalidad_persona_referencia": nac, "categoria": cat, "indicador": ind, "hogares_muestra": n,
                                  "valor": round(100 * pr, 2) if ok else np.nan, "ic95_inf": round(100 * (pr - Z * se), 2) if ok else np.nan,
                                  "ic95_sup": round(100 * (pr + Z * se), 2) if ok else np.nan, "publicable": ok})
    return pd.DataFrame(filas)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    if not any((A.MICRO / "ecv").glob("datos_*.zip")):
        # microdatos no versionados (`make datos_v9`): sin ellos se conservan las salidas versionadas de la ECV y se
        # rehace solo la parte del Censo (versionada)
        censo().to_csv(OUT / "censo2021_condiciones_origen.csv", index=False)
        print("[b6] sin microdatos de la ECV: se conservan output/v12/b6/ecv_*.csv versionados")
        return 0
    p = ecv()
    ult = int(p.anio.max())
    ta = tabla_anual(p)
    ta.to_csv(OUT / "ecv_anual_origen.csv", index=False)
    tc = tabla_cruces(p, ult - 2)
    tc.to_csv(OUT / "ecv_cruces_origen.csv", index=False)
    es = estandarizada(p, ult - 2)
    es.to_csv(OUT / "ecv_brecha_misma_edad_renta.csv", index=False)
    c = censo()
    c.to_csv(OUT / "censo2021_condiciones_origen.csv", index=False)
    u = ta[(ta.anio == ult) & (ta.grupo == "origen")].pivot_table(index="indicador", columns="categoria", values="valor")
    res = {"rama": "V12-B6", "pregunta": "¿En qué condiciones viven los hogares según su origen?", "capa": "C4",
           "metodo": "descriptivo con intervalos (linealización; bootstrap por hogar; binomial con CPF)",
           "datos": f"ECV 2018-{ult} (microdatos), Censo 2021 (muestra)", "N": int(len(p)),
           "ecv_ultimo_por_nacionalidad": {i: {k: (None if pd.isna(v) else float(v)) for k, v in r.items()} for i, r in u.iterrows()},
           "brecha_misma_edad_y_renta": es[["indicador", "extranjera", "espanola_cruda", "espanola_misma_edad_y_renta", "diferencia_estandarizada",
                                           "ic95_inf", "ic95_sup"]].to_dict(orient="records"),
           "celdas_suprimidas": {"ecv_anual": int((~ta.publicable).sum()), "ecv_cruces": int((~tc.publicable).sum()), "censo": int((~c.publicable).sum())},
           "notas": ["descriptivo: las diferencias no se atribuyen a la nacionalidad", "persona de referencia del censo = la de mayor edad",
                     "intervalos de la ECV sin efecto de diseño de estratos (no publicados)"]}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
