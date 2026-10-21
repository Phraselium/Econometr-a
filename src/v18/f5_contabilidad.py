"""V18 · fase 5 · contabilidad de la subida (plan, sección 4; adenda 1.10).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Determinista (SEED 20261010), sin red.

ES CONTABILIDAD CON ELASTICIDADES ESTIMADAS, NO UNA DESCOMPOSICIÓN ESTRUCTURAL: contribución_f = magnitud_f × variación observada del factor f. No hay
interacciones ni efectos de equilibrio general y los factores no son ortogonales.

Qué entra (adenda 1.10, leída con el plan):
- Principal (contabilidad.csv): solo factores con magnitud preferida de B5 construida con una estimación propia de diseño válido. Tras B5
  (f5_magnitudes.py) ninguno la tiene: E2-R1 es SUGESTIVO, pero el metaanálisis no da magnitud preferida (la decisión no coincide en las tres priors y
  I² > 75 % con intervalo de predicción que cambia de signo). Cada factor dice «sin magnitud»; todo queda en «no explicado».
- Ilustración (contabilidad_ilustracion.csv): magnitudes de la literatura (rango de estudios, un solo estudio o efecto fijo) y E2-R1 propia sola.
  Rotulada como ilustración: no es una atribución.
Periodos del plan (1995T1-2007T4, 2008T1-2013T4, 2014T1-2019T4, 2020T1-2022T2, 2022T3-2026T2); para comparar con V8 se repite el agregado nacional con los
inicios de V8 (2008T3 y 2020T2). Unidad: 100 × Δln (≈ puntos porcentuales). Propagación: 10.000 extracciones de la magnitud (SEED 20261010); la variación
observada del factor se toma sin error (una sola fuente, declarado). Independencia entre factores: no hay dos magnitudes del mismo modelo.
Sellado: toda serie con detalle territorial o temporal pasa por sellado.filtrar (tope de V18) y holdout.excluir_sellados_v6; nunca data/sealed.
"""
from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
for _p in (RAIZ / "src", RAIZ / "src" / "v18", RAIZ / "src" / "v18" / "estimacion"):
    sys.path.insert(0, str(_p))
import holdout  # noqa: E402
import sellado  # noqa: E402
import f5_magnitudes as MAG  # noqa: E402

warnings.filterwarnings("ignore", category=FutureWarning)
ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
SEMILLA = 20261010
N_EXT = 10000
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v18" / "f5"
ROTULO = "análisis V18; capa C4; pre-registro interno plan-replicacion-v18"
REL = "relativa entre provincias (o unidades), sin el componente común"
REL_PROV = ("relativa a la media simple de las provincias no selladas con dato, sin el componente común: no se suma ni se compara con la "
            "cifra nacional")

PERIODOS = [("1995T1-2007T4", "1995T1", "2007T4"), ("2008T1-2013T4", "2008T1", "2013T4"), ("2014T1-2019T4", "2014T1", "2019T4"),
            ("2020T1-2022T2", "2020T1", "2022T2"), ("2022T3-2026T2", "2022T3", "2026T2")]
PERIODOS_V8 = [("1995T1-2007T4", "1995T1", "2007T4", "P1"), ("2008T3-2013T4", "2008T3", "2013T4", "P2"), ("2014T1-2019T4", "2014T1", "2019T4", "P3"),
               ("2020T2-2022T2", "2020T2", "2022T2", "P4"), ("2022T3-2026T2", "2022T3", "2026T2", "P5")]
CCAA = {"01": ("Andalucía", ["04", "11", "14", "18", "21", "23", "29", "41"]), "06": ("Cantabria", ["39"]),
        "07": ("Castilla y León", ["05", "09", "24", "34", "37", "40", "42", "47", "49"]), "08": ("Castilla-La Mancha", ["02", "13", "16", "19", "45"]),
        "09": ("Cataluña", ["08", "17", "25", "43"]), "10": ("Comunitat Valenciana", ["03", "12", "46"]), "11": ("Extremadura", ["06", "10"]),
        "12": ("Galicia", ["15", "27", "32", "36"]), "16": ("País Vasco", ["01", "20", "48"])}
PROV_A_CCAA = {p: c for c, (_, ps) in CCAA.items() for p in ps}
NOMBRE_A_PROV = {
    "Albacete": "02", "Alicante/Alacant": "03", "Almería": "04", "Araba/Alava": "01", "Badajoz": "06", "Barcelona": "08", "Bizkaia": "48",
    "Burgos": "09", "Castellón/Castelló": "12", "Ciudad Real": "13", "Coruña (A)": "15", "Cuenca": "16", "Cáceres": "10", "Cádiz": "11",
    "Córdoba": "14", "Gipuzkoa": "20", "Girona": "17", "Granada": "18", "Guadalajara": "19", "Huelva": "21", "Huesca": "22", "Jaén": "23",
    "León": "24", "Lleida": "25", "Lugo": "27", "Málaga": "29", "Ourense": "32", "Palencia": "34", "Palmas (Las)": "35", "Pontevedra": "36",
    "Salamanca": "37", "Santa Cruz de Tenerife": "38", "Segovia": "40", "Sevilla": "41", "Soria": "42", "Tarragona": "43", "Teruel": "44",
    "Toledo": "45", "Valencia/València": "46", "Valladolid": "47", "Zamora": "49", "Zaragoza": "50", "Ávila": "05",
}
FACTORES = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"]
NOMBRE_FACTOR = {"E1": "vivienda turística", "E2": "topes al alquiler", "E3": "inmigración", "E4": "ayudas a la demanda", "E5": "oferta y suelo",
                 "E6": "obra nueva", "E7": "tipos de interés", "E8": "fiscalidad de la compra (ITP)", "E9": "compradores no residentes"}
SIN_VARIACION = {"E4": "sin variación medida del factor (no hay datos de beneficiarios ni de importes: V18-E4-X1)",
                 "E5": "la magnitud es la elasticidad de la oferta al precio; no hay una elasticidad del precio a la cantidad construida que permita traducir la variación de la oferta",
                 "E6": "la unidad de la magnitud (oferta nueva local por región y año, Mense) no tiene variación comparable medida en España"}


# ------------------------------------------------------------------------------------------------ tiempo
def qi(p: str) -> int:
    y, q = p.split("T")
    return int(y) * 4 + int(q) - 1


def qs(i: int) -> str:
    return f"{i // 4}T{i % 4 + 1}"


def ini_nivel(p: str) -> int:
    """Trimestre cuyo nivel es el de partida: el anterior al primero del periodo (el primero de la serie, 1995T1, no tiene anterior)."""
    return qi(p) if p == "1995T1" else qi(p) - 1


def anio_ini(p: str) -> int:
    y, q = p.split("T")
    return int(y) + (1 if q == "4" else 0)


def anio_fin(p: str) -> int:
    y, q = p.split("T")
    return int(y) + (1 if q in ("3", "4") else 0)


# ------------------------------------------------------------------------------------------------ lectura con sellado
def leer(variable: str, nivel: str, frec: str, codigos=None) -> pd.DataFrame:
    filtros = [("variable", "==", variable), ("nivel", "==", nivel), ("frecuencia", "==", frec)]
    if codigos is not None:
        filtros.append(("territorio_codigo", "in", list(codigos)))
    df = pd.read_parquet(HECHOS, columns=["territorio_codigo", "periodo", "valor", "edicion", "muestra_sellada_v6"], filters=filtros)
    df["territorio_codigo"] = df["territorio_codigo"].astype(str)
    df["periodo"] = df["periodo"].astype(str)
    df = sellado.filtrar(df, "territorio_codigo", nivel, "periodo", variable, frec)
    if nivel in ("ccaa", "provincia", "municipio"):
        df = holdout.excluir_sellados_v6(df, "territorio_codigo", nivel)
    return df


def ancho_q(df: pd.DataFrame) -> pd.DataFrame:
    w = df.pivot_table(index="periodo", columns="territorio_codigo", values="valor", aggfunc="first")
    w.index = [qi(p) for p in w.index]
    return w.sort_index()


def ancho_a(df: pd.DataFrame) -> pd.DataFrame:
    w = df.pivot_table(index="periodo", columns="territorio_codigo", values="valor", aggfunc="first")
    w.index = [int(p) for p in w.index]
    return w.sort_index()


def nacional_heredado(variable: str, frec: str, clave: tuple[str, str, str]) -> pd.DataFrame:
    """Serie nacional sin clave propia en sellado_v18.json: hereda el tope de una serie hermana (regla 1.4 f). Error si la clave hermana no existe."""
    tope = sellado.tope(*clave)
    df = pd.read_parquet(HECHOS, columns=["territorio_codigo", "periodo", "valor"], filters=[("variable", "==", variable), ("nivel", "==", "nacional"), ("frecuencia", "==", frec)])
    df["periodo"] = df["periodo"].astype(str)
    return df[df["periodo"].str[:4] <= tope[:4]]


class Datos:
    """Series de resultado, de población y de factores, ya con el sellado de V18. Todo en memoria; nada se escribe aquí."""

    def __init__(self) -> None:
        d = leer("deflactor", "nacional", "T")
        self.defl = np.log(ancho_q(d)["00"])
        self.precio_nac = ancho_q(leer("p_tasado", "nacional", "T"))
        self.precio_prov = ancho_q(leer("valor_tasado", "provincia", "T"))
        self.precio_val = ancho_q(leer("p_tasado", "municipio", "T", ["46250"]))
        self.alq_nac = ancho_q(leer("ipc_alquiler", "nacional", "T"))
        self.alq_prov = ancho_q(leer("ipc_alquiler_indice", "provincia", "T"))
        self.provincias = sorted(c for c in self.precio_prov.columns if c in PROV_A_CCAA)
        self.pob_prov = ancho_a(leer("pob_total", "provincia", "A", self.provincias))
        self.ext_prov = ancho_a(leer("pob_extranj", "provincia", "A", self.provincias))
        pt = ancho_q(leer("pob_total", "nacional", "T"))["00"]
        self.pob_nac = pd.Series({qs(i)[:4]: v for i, v in pt.items() if qs(i).endswith("T1")})
        self.pob_nac.index = self.pob_nac.index.astype(int)
        ne = nacional_heredado("pob_extranj", "T", ("pob_extranj", "provincia", "A"))
        ne = ne[ne["periodo"].str.endswith("T1")]
        self.ext_nac = pd.Series(ne["valor"].values, index=ne["periodo"].str[:4].astype(int))
        self.pob_val = ancho_a(leer("pob_total", "municipio", "A", ["46250"]))["46250"]
        self.ext_val = ancho_a(leer("pob_extranjera", "municipio", "A", ["46250"]))["46250"]
        self.tipo = ancho_q(leer("tipo_hip_bde", "nacional", "T"))["00"]
        self.cuota_prov, self.cuota_nac = self._cuota()
        self.incasol = self._incasol()
        self.hut_bcn = self._hut_barcelona()

    # -- cuota de compras de no residentes (MIVAU, trimestral): no residentes / total
    def _cuota(self):
        d = pd.read_csv(RAW / "mivau_transacciones_residencia.csv", usecols=["periodo", "serie", "valor", "territorio", "nivel"])
        d = d[d.serie.str.startswith("tx_residencia_no_residentes_total_") | d.serie.str.startswith("tx_residencia_total_")].copy()
        d["tipo"] = np.where(d.serie.str.startswith("tx_residencia_no_residentes_total_"), "nr", "tot")
        res = {}
        for nivel in ("provincia", "nacional"):
            x = d[d.nivel == nivel].copy()
            x["territorio_codigo"] = x.territorio.map(NOMBRE_A_PROV) if nivel == "provincia" else "00"
            x = x.dropna(subset=["territorio_codigo"])
            nr = x[x.tipo == "nr"][["territorio_codigo", "periodo", "valor"]]
            tot = x[x.tipo == "tot"][["territorio_codigo", "periodo", "valor"]]
            m = nr.merge(tot, on=["territorio_codigo", "periodo"], suffixes=("_nr", "_tot"))
            if nivel == "provincia":
                m = sellado.filtrar(m.rename(columns={"valor_nr": "valor"}), "territorio_codigo", "provincia", "periodo", "cuota_no_residentes_mivau", "T")
                m = holdout.excluir_sellados_v6(m, "territorio_codigo", "provincia").rename(columns={"valor": "valor_nr"})
            else:
                tope = sellado.tope("cuota_no_residentes_mivau", "provincia", "T")
                m = m[m.periodo <= tope]
            res[nivel] = m
        out = []
        for nivel in ("provincia", "nacional"):
            m = res[nivel]
            nr = m.pivot_table(index="periodo", columns="territorio_codigo", values="valor_nr", aggfunc="first")
            tot = m.pivot_table(index="periodo", columns="territorio_codigo", values="valor_tot", aggfunc="first")
            for w in (nr, tot):
                w.index = [qi(p) for p in w.index]
            out.append((nr.sort_index(), tot.sort_index()))
        return out[0], out[1]

    # -- Incasòl (renta media de contratos nuevos y número de contratos) por municipio y trimestre, sin tramos
    def _incasol(self):
        r = leer("incasol_renta_media", "municipio", "T")
        n = leer("incasol_contratos", "municipio", "T")
        m = r.rename(columns={"valor": "renta"})[["territorio_codigo", "periodo", "renta"]].merge(
            n.rename(columns={"valor": "contratos"})[["territorio_codigo", "periodo", "contratos"]], on=["territorio_codigo", "periodo"])
        m["q"] = m["periodo"].map(qi)
        return m

    def _hut_barcelona(self):
        import e1_datos as D  # noqa: E402 (secciones no selladas, HUT geocodificado y viviendas del Censo 2021: reutiliza la capa de datos de E1)
        sec = D.secciones("08019")
        W, _ = D.hut_por_seccion(sec)
        viv = float(D.viviendas_censo2021(sec.cod_seccion).sum())
        s = W.sum()
        return pd.Series({c: 100.0 * v / viv for c, v in s.items()}), viv, len(sec), sec.attrs["n_total"]


# ------------------------------------------------------------------------------------------------ resultados observados
def d_nivel(W: pd.DataFrame, a: int, b: int) -> pd.DataFrame:
    """Por columna: Δln entre el primer trimestre disponible ≥ a y el último ≤ b; devuelve d, qa, qb (NaN si no hay ventana)."""
    filas = {}
    for c in W.columns:
        s = W[c].dropna()
        s = s[s > 0]
        ini = s[(s.index >= a) & (s.index <= b)]
        if len(ini) < 2:
            filas[c] = (np.nan, np.nan, np.nan)
            continue
        qa, qb = ini.index[0], ini.index[-1]
        filas[c] = (float(np.log(ini.iloc[-1]) - np.log(ini.iloc[0])), qa, qb)
    return pd.DataFrame(filas, index=["d", "qa", "qb"]).T


def resultado_real(dat: Datos, W: pd.DataFrame, a: int, b: int) -> pd.DataFrame:
    r = d_nivel(W, a, b)
    out = {}
    for c, row in r.iterrows():
        if np.isnan(row.d):
            out[c] = (np.nan, "")
            continue
        qa, qb = int(row.qa), int(row.qb)
        dd = float(dat.defl.get(qb, np.nan) - dat.defl.get(qa, np.nan))
        out[c] = (100.0 * (row.d - dd), f"{qs(qa)} a {qs(qb)}")
    return pd.DataFrame(out, index=["obs", "ventana"]).T


def obs_territorios(dat: Datos, resultado: str, a: int, b: int, ys: int) -> pd.DataFrame:
    """Δ observada (100·Δln real) por territorio: nacional '00', provincias, CCAA (media ponderada por la población provincial al inicio) y ciudades."""
    if resultado == "precio":
        nac = resultado_real(dat, dat.precio_nac, a, b)
        prov = resultado_real(dat, dat.precio_prov, a, b).loc[dat.provincias]
        ciu = resultado_real(dat, dat.precio_val, a, b)
    else:
        nac = resultado_real(dat, dat.alq_nac, a, b)
        prov = resultado_real(dat, dat.alq_prov, a, b).reindex(dat.provincias)
        ciu = pd.DataFrame(columns=["obs", "ventana"])
    # K14 (árbitro, ronda 2, N10): si las provincias no empiezan todas a la vez (1995T1-2007T4: la Comunitat Valenciana desde 1995T1, el resto
    # desde 2002T1), las filas relativas usan la ventana común (el inicio más tardío) en todas las provincias y ciudades, con los mismos datos y
    # el mismo cálculo; así la media simple de referencia y cada fila relativa cubren el mismo periodo. La fila nacional no cambia.
    ini = prov.ventana[prov.ventana.astype(str).str.len() > 0].str.slice(0, 6)
    comun = ""
    if ini.nunique() > 1:
        comun = ("; todas las provincias con la ventana común desde " + qs(max(qi(q) for q in ini.unique())) + ", también las que tienen serie "
                 "desde antes (" + ", ".join(f"{n} desde {i}" for i, n in ini.value_counts().items()) + "), para que la media de referencia y "
                 "cada fila cubran el mismo periodo (K14)")
        a_com = max(qi(q) for q in ini.unique())
        W = dat.precio_prov if resultado == "precio" else dat.alq_prov
        prov = resultado_real(dat, W, a_com, b).reindex(dat.provincias)
        ys = a_com // 4   # peso: población provincial al inicio de la ventana común
        if len(ciu):
            ciu = resultado_real(dat, dat.precio_val, a_com, b)
    filas = [("nacional", "00", "Nacional", nac.iloc[0].obs, nac.iloc[0].ventana)]
    py = min(max(ys, dat.pob_prov.index.min()), dat.pob_prov.index.max())
    w = dat.pob_prov.loc[py]
    for c, (nom, ps) in CCAA.items():
        ps = [p for p in ps if p in prov.index and not np.isnan(prov.loc[p, "obs"])]
        if ps:
            filas.append(("ccaa", c, nom, float(np.average(prov.loc[ps, "obs"], weights=w[ps])), prov.loc[ps[0], "ventana"] + " (media de provincias no selladas, ponderada por población)"))
    for p in dat.provincias:
        filas.append(("provincia", p, f"provincia {p}", prov.loc[p, "obs"], prov.loc[p, "ventana"]))
    for c, row in ciu.iterrows():
        filas.append(("ciudad", c, "València", row.obs, row.ventana))
    df = pd.DataFrame(filas, columns=["tipo", "codigo", "nombre", "obs", "ventana"])
    media = df[df.tipo == "provincia"].obs.mean()
    df["obs_rel"] = np.where(df.tipo == "nacional", np.nan, df.obs - media)
    df["media_provincial"] = media
    df["ventana_comun"] = comun
    return df


# ------------------------------------------------------------------------------------------------ variación del factor
def delta_e3(dat: Datos, ys: int, ye: int) -> pd.DataFrame:
    """Δ de la población extranjera / población inicial (pp). Stock a 1 de enero; ventana anual recortada al tope (2024) y al inicio de la serie (2002)."""
    y0 = max(ys, int(dat.ext_prov.index.min()))
    y1 = min(ye, int(dat.ext_prov.index.max()))
    if y1 <= y0:
        return pd.DataFrame(columns=["tipo", "codigo", "delta", "ventana"])
    filas = []
    e = dat.ext_prov
    p = dat.pob_prov
    for c in dat.provincias:
        filas.append(("provincia", c, 100.0 * (e.loc[y1, c] - e.loc[y0, c]) / p.loc[y0, c]))
    for c, (_, ps) in CCAA.items():
        ps = [x for x in ps if x in dat.provincias]
        if not ps:
            continue
        filas.append(("ccaa", c, 100.0 * (e.loc[y1, ps].sum() - e.loc[y0, ps].sum()) / p.loc[y0, ps].sum()))
    filas.append(("nacional", "00", 100.0 * (dat.ext_nac.get(y1, np.nan) - dat.ext_nac.get(y0, np.nan)) / dat.pob_nac.get(y0, np.nan)))
    yv0, yv1 = max(y0, int(dat.ext_val.dropna().index.min())), min(y1, int(dat.ext_val.dropna().index.max()), 2022)
    if yv1 > yv0:
        filas.append(("ciudad", "46250", 100.0 * (dat.ext_val[yv1] - dat.ext_val[yv0]) / dat.pob_val[yv0]))
    df = pd.DataFrame(filas, columns=["tipo", "codigo", "delta"])
    df["ventana"] = f"stock a 1 de enero de {y0} a {y1}"
    return df


def delta_e9(dat: Datos, a: int, b: int) -> pd.DataFrame:
    nr, tot = dat.cuota_prov
    nrn, totn = dat.cuota_nac
    qmin = int(nr.index.min()) + 3
    a2 = max(a, qmin)
    filas = []
    if b < qmin + 1 or a2 >= b:
        return pd.DataFrame(columns=["tipo", "codigo", "delta", "ventana"])

    def cuota(nrW, totW, cols, q):
        idx = [x for x in range(q - 3, q + 1) if x in nrW.index]
        if len(idx) < 4:
            return np.nan
        return 100.0 * nrW.loc[idx, cols].sum().sum() / totW.loc[idx, cols].sum().sum()

    for c in dat.provincias:
        if c in nr.columns:
            filas.append(("provincia", c, cuota(nr, tot, [c], b) - cuota(nr, tot, [c], a2)))
    for k, (_, ps) in CCAA.items():
        ps = [x for x in ps if x in nr.columns]
        if ps:
            filas.append(("ccaa", k, cuota(nr, tot, ps, b) - cuota(nr, tot, ps, a2)))
    filas.append(("nacional", "00", cuota(nrn, totn, ["00"], b) - cuota(nrn, totn, ["00"], a2)))
    df = pd.DataFrame(filas, columns=["tipo", "codigo", "delta"])
    df["ventana"] = f"cuota media de cuatro trimestres: {qs(a2)} a {qs(b)}"
    return df


def delta_e7(dat: Datos, a: int, b: int, horizonte: int = 8) -> dict:
    """Variación del tipo hipotecario (pp) en los últimos `horizonte` trimestres del periodo (adenda 1.10: solo cuenta el cambio dentro del horizonte
    estimado); lo anterior se devuelve aparte como «fuera del horizonte»."""
    t = dat.tipo
    a_ = max(a, int(t.index.min()))
    c = max(a_, b - horizonte)
    dentro = float(t.get(b) - t.get(c))
    fuera = float(t.get(c) - t.get(a_))
    cambios = (t - t.shift(horizonte)).dropna()
    return {"delta": dentro, "fuera": fuera, "ventana": f"{qs(c)} a {qs(b)} (horizonte de {horizonte} trimestres)", "soporte": (float(cambios.quantile(0.05)), float(cambios.quantile(0.95)))}


def delta_e8(a: int, b: int) -> pd.DataFrame:
    ev = pd.read_csv(RAIZ / "output" / "v18" / "estimacion" / "e8" / "calendario.csv", dtype={"cod_ine": str})
    ev["fecha"] = pd.to_datetime(ev["fecha"])
    f0 = pd.Timestamp(year=a // 4, month=3 * (a % 4) + 1, day=1) + pd.DateOffset(months=3)     # primer día del trimestre siguiente al nivel de partida
    f1 = pd.Timestamp(year=b // 4, month=3 * (b % 4) + 1, day=1) + pd.DateOffset(months=3) - pd.Timedelta(days=1)
    primera = pd.Timestamp("2010-01-01")
    if f1 < primera:
        return pd.DataFrame(columns=["tipo", "codigo", "delta", "ventana"])
    f0 = max(f0, primera)
    x = ev[(ev.fecha >= f0) & (ev.fecha <= f1)].groupby("cod_ine").dosis.sum()
    cods = sorted(ev.cod_ine.unique())
    df = pd.DataFrame({"tipo": "ccaa", "codigo": cods, "delta": [float(x.get(c, 0.0)) for c in cods]})
    df["ventana"] = f"cambios del tipo general entre {f0.date()} y {f1.date()} (el calendario empieza en 2010-01-01; fechas sin contraste con el BOE)"
    return df


def e2_cuota(dat: Datos) -> dict:
    """Cuota de contratos del Incasòl en municipios sujetos a la Ley 11/2020 (sin Barcelona ciudad ni municipios sellados), media de 2020T4-2022T1."""
    c = pd.read_csv(RAW / "v3" / "cataluna_contencion_rentas_v3.csv", dtype=str)
    reg = set(c[c.regimen == "ley11_2020"].cod_ine.str.zfill(5)) - {"08019"}
    m = dat.incasol[(dat.incasol.q >= qi("2020T4")) & (dat.incasol.q <= qi("2022T1")) & (dat.incasol.territorio_codigo != "08019")].copy()
    m["reg"] = m.territorio_codigo.isin(reg)
    m["prov"] = m.territorio_codigo.str[:2]
    out = {}
    for p, g in list(m.groupby("prov")) + [("09", m)]:
        s = g.groupby("periodo").apply(lambda z: z.loc[z.reg, "contratos"].sum() / z.contratos.sum(), include_groups=False)
        out[p] = (float(s.mean()), int(g.territorio_codigo.nunique()), int(g[g.reg].territorio_codigo.nunique()))
    return out


def obs_incasol(dat: Datos, a: int, b: int, provs: list[str] | None) -> tuple[float, str]:
    """Δ de la renta media de los contratos nuevos (Incasòl), ponderada por contratos, sin Barcelona ciudad; nominal menos deflactor."""
    m = dat.incasol[(dat.incasol.territorio_codigo != "08019")].copy()
    if provs:
        m = m[m.territorio_codigo.str[:2].isin(provs)]
    s = m.groupby("q").apply(lambda z: np.average(z.renta, weights=z.contratos), include_groups=False)
    s = s[(s.index >= a) & (s.index <= b)]
    if len(s) < 2:
        return float("nan"), ""
    qa, qb = int(s.index[0]), int(s.index[-1])
    return 100.0 * (np.log(s.iloc[-1]) - np.log(s.iloc[0]) - (dat.defl[qb] - dat.defl[qa])), f"{qs(qa)} a {qs(qb)}"


def obs_barcelona_alquiler(dat: Datos, a: int, b: int) -> tuple[float, str]:
    m = dat.incasol[dat.incasol.territorio_codigo == "08019"].set_index("q").renta.sort_index()
    m = m[(m.index >= a) & (m.index <= b)]
    if len(m) < 2:
        return float("nan"), ""
    qa, qb = int(m.index[0]), int(m.index[-1])
    return 100.0 * (np.log(m.iloc[-1]) - np.log(m.iloc[0]) - (dat.defl[qb] - dat.defl[qa])), f"{qs(qa)} a {qs(qb)}"


def delta_e1_barcelona(dat: Datos, a: int, b: int) -> dict:
    """Δ de las viviendas de uso turístico registradas (HUT) por 100 viviendas del Censo 2021, secciones no selladas de Barcelona. Cortes de 4T (y 2018T2)."""
    s, viv, n_sec, n_tot = dat.hut_bcn
    cortes = {qi(c): v for c, v in s.items()}
    fa = [q for q in cortes if q <= a + 1]
    fb = [q for q in cortes if q <= b]
    if not fa or not fb or max(fa) >= max(fb):
        return {"delta": np.nan, "ventana": "sin cortes del registro HUT en el periodo"}
    qa, qb = max(fa), max(fb)
    return {"delta": float(cortes[qb] - cortes[qa]), "ventana": f"cortes del registro HUT {qs(qa)} a {qs(qb)}; {n_sec} de {n_tot} secciones (las selladas de V15/V16 no se leen)"}


# ------------------------------------------------------------------------------------------------ motor
def estad(x: np.ndarray) -> dict:
    return {"med": float(np.median(x)), "p16": float(np.quantile(x, 0.16)), "p84": float(np.quantile(x, 0.84)), "p05": float(np.quantile(x, 0.05)), "p95": float(np.quantile(x, 0.95))}


def dentro_soporte(valor: float, ref: np.ndarray | tuple) -> str:
    if isinstance(ref, tuple):
        lo, hi = ref
    else:
        r = ref[~np.isnan(ref)]
        if len(r) < 8:
            return "soporte no evaluable (menos de 8 unidades)"
        lo, hi = np.quantile(r, 0.05), np.quantile(r, 0.95)
    return "dentro del soporte" if lo <= valor <= hi else "fuera del soporte"


def distribuciones() -> dict:
    d: dict[str, dict | None] = {}
    for f in FACTORES:
        d[f] = MAG.distribucion(f, N_EXT, SEMILLA)
    prop = MAG.propia_e2()
    rng = np.random.default_rng(SEMILLA + 5000)
    d["E2_propia"] = {"tipo": "propia", "x": rng.normal(prop.y, prop.se, N_EXT), "centro": prop.y, "ref": "E2-R1 propia sola (SUGESTIVO), sin pasar por B5"}
    return d


def construir_ilustracion(dat: Datos, dist: dict, periodos, alineacion: str, filas: list[dict], estados_b5: dict) -> None:
    """Filas de la ilustración: cada factor con magnitud (de la literatura o E2-R1 propia sola) por resultado, periodo y territorio."""
    for nombre, pa, pb, *_ in periodos:
        a, b = ini_nivel(pa), qi(pb)
        ys, ye = anio_ini(pa), anio_fin(pb)
        for resultado in ("precio", "alquiler"):
            obs = obs_territorios(dat, resultado, a, b, ys)
            factores = []     # (factor, DataFrame tipo/codigo/delta/ventana, extra)
            if resultado == "precio":
                factores.append(("E3", delta_e3(dat, ys, ye), {}))
                factores.append(("E9", delta_e9(dat, a, b), {"alternativa": True}))
                factores.append(("E8", delta_e8(a, b), {}))
                e7 = delta_e7(dat, a, b)
                factores.append(("E7", pd.DataFrame([("nacional", "00", e7["delta"], e7["ventana"])], columns=["tipo", "codigo", "delta", "ventana"]), {"e7": e7}))
            _ilustrar(dat, dist, nombre, alineacion, resultado, obs, factores, filas)


def _ilustrar(dat, dist, periodo, alineacion, resultado, obs, factores, filas) -> None:
    nfac = {f: df for f, df, _ in factores}
    extra = {f: ex for f, _, ex in factores}
    # soporte de cada factor: percentiles 5-95 de la variación provincial (E3, E9) o de las CCAA (E8) o de los cambios de 8 trimestres del tipo (E7)
    sop = {}
    for f in ("E3", "E9"):
        df = nfac.get(f)
        if df is not None and len(df):
            p = df[df.tipo == "provincia"].delta.values
            sop[f] = {"abs": p, "rel": p - np.nanmean(p) if len(p) else p}
    if "E8" in nfac and len(nfac["E8"]):
        p = nfac["E8"].delta.values
        sop["E8"] = {"abs": p, "rel": p - np.mean(p)}
    for _, o in obs.iterrows():
        tkey = (o.tipo, o.codigo)
        suma = {"base": np.zeros(N_EXT), "alt_E9": np.zeros(N_EXT)}
        n_con_cifra = 0
        fila_obs = o.obs if o.tipo == "nacional" else o.obs_rel
        if np.isnan(fila_obs):
            continue
        for f, df, ex in factores:
            if f not in dist or dist[f] is None or len(df) == 0:
                continue
            r = df[(df.tipo == o.tipo) & (df.codigo == o.codigo)]
            if r.empty:
                continue
            delta_abs = float(r.delta.iloc[0])
            if np.isnan(delta_abs):
                continue
            ventana = r.ventana.iloc[0]
            if f == "E7":
                delta_use, rotulo = delta_abs, "serie nacional: incluye el componente común"
                supo = dentro_soporte(delta_abs, ex["e7"]["soporte"])
                nota_x = f"fuera del horizonte (sin cifra): {ex['e7']['fuera']:.2f} pp de variación del tipo antes de los últimos 8 trimestres"
            else:
                if o.tipo == "nacional":
                    delta_use, rotulo = delta_abs, REL + " (fila nacional con la variación absoluta; incluye las 11 provincias selladas)"
                    supo = dentro_soporte(delta_use, sop[f]["abs"]) if f in sop else "soporte no evaluable"
                else:
                    base = float(sop[f]["abs"].mean()) if f in sop and f != "E8" else (float(nfac[f].delta.mean()) if f == "E8" else 0.0)
                    delta_use = delta_abs - base
                    rotulo = REL
                    supo = dentro_soporte(delta_use, sop[f]["rel"]) if f in sop else "soporte no evaluable"
                nota_x = ""
            k = 100.0 if f in ("E1", "E2") else 1.0
            x = dist[f]["x"]
            con_cifra = supo != "fuera del soporte"
            contrib = x * delta_use * k
            e = estad(contrib) if con_cifra else {}
            pct = (e["med"] / fila_obs * 100.0) if (con_cifra and abs(fila_obs) >= 1.0) else np.nan
            filas.append({"marco": "ilustracion", "alineacion": alineacion, "resultado": resultado, "periodo": periodo, "territorio_tipo": o.tipo, "territorio": o.codigo, "nombre": o.nombre,
                          "factor": f, "tipo_fila": "factor", "origen_magnitud": dist[f]["ref"], "magnitud_centro": dist[f]["centro"], "clase_estimacion_propia": "NO ESTIMABLE" if f != "E2" else "SUGESTIVO",
                          "variacion_factor": delta_use, "ventana_factor": ventana, "obs_pp": fila_obs, "contrib_med": e.get("med", np.nan), "p16": e.get("p16", np.nan), "p84": e.get("p84", np.nan),
                          "p05": e.get("p05", np.nan), "p95": e.get("p95", np.nan), "pct_de_obs": pct, "soporte": supo, "rotulo": rotulo,
                          "en_suma": (not ex.get("alternativa", False)) and con_cifra, "nota": ("ilustración con magnitud de la literatura; " if f != "E2" else "") + nota_x})
            if con_cifra:
                if f in ("E3", "E7", "E8"):
                    suma["base"] += contrib
                    n_con_cifra += 1
                if f in ("E9", "E7", "E8"):
                    suma["alt_E9"] += contrib
        if n_con_cifra:
            ne = fila_obs - suma["base"]
            e = estad(ne)
            filas.append({"marco": "ilustracion", "alineacion": alineacion, "resultado": resultado, "periodo": periodo, "territorio_tipo": o.tipo, "territorio": o.codigo, "nombre": o.nombre,
                          "factor": "NOEXPL", "tipo_fila": "no_explicado", "origen_magnitud": "", "magnitud_centro": np.nan, "clase_estimacion_propia": "", "variacion_factor": np.nan,
                          "ventana_factor": "", "obs_pp": fila_obs, "contrib_med": e["med"], "p16": e["p16"], "p84": e["p84"], "p05": e["p05"], "p95": e["p95"],
                          "pct_de_obs": e["med"] / fila_obs * 100.0 if abs(fila_obs) >= 1.0 else np.nan, "soporte": "", "rotulo": REL if o.tipo != "nacional" else REL + " (mezcla componentes)",
                          "en_suma": True, "nota": "Δ observada menos la suma de las contribuciones con cifra de la fila, extracción a extracción; E3 y E9 no se suman (cuotas del padrón por nacionalidad)"})
        if "E9" in nfac and len(nfac["E9"]) and "E9" in dist and dist["E9"] is not None:
            r9 = nfac["E9"][(nfac["E9"].tipo == o.tipo) & (nfac["E9"].codigo == o.codigo)]
            if len(r9):
                ne = fila_obs - suma["alt_E9"]
                e = estad(ne)
                filas.append({"marco": "ilustracion", "alineacion": alineacion, "resultado": resultado, "periodo": periodo, "territorio_tipo": o.tipo, "territorio": o.codigo, "nombre": o.nombre,
                              "factor": "NOEXPL_alt_E9", "tipo_fila": "no_explicado_alternativa", "origen_magnitud": "", "magnitud_centro": np.nan, "clase_estimacion_propia": "",
                              "variacion_factor": np.nan, "ventana_factor": "", "obs_pp": fila_obs, "contrib_med": e["med"], "p16": e["p16"], "p84": e["p84"], "p05": e["p05"], "p95": e["p95"],
                              "pct_de_obs": e["med"] / fila_obs * 100.0 if abs(fila_obs) >= 1.0 else np.nan, "soporte": "", "rotulo": REL,
                              "en_suma": False, "nota": "sensibilidad: E9 sustituye a E3 (adenda 1.10, sin doble cómputo)"})


def construir_ilustracion_locales(dat: Datos, dist: dict, filas: list[dict]) -> None:
    """E2-R1 propia sola en Cataluña (renta de contratos nuevos del Incasòl) y E1 en Barcelona (alquiler del Incasòl): solo donde los datos existen."""
    e2c = e2_cuota(dat)
    for nombre, pa, pb in PERIODOS[3:]:
        a, b = ini_nivel(pa), qi(pb)
        for cod in ["09", "08", "17", "25", "43"]:
            obs, vent = obs_incasol(dat, a, b, None if cod == "09" else [cod])
            if np.isnan(obs):
                continue
            share, n_mun, n_reg = e2c.get(cod, (np.nan, 0, 0))
            tipo = "ccaa" if cod == "09" else "provincia"
            nom = "Cataluña (sin Barcelona ciudad)" if cod == "09" else f"provincia {cod} (sin Barcelona ciudad)"
            if nombre == "2020T1-2022T2":
                # variación entre extremos: el régimen no está vigente al final (STC 37/2022): 0; diferencia asociada durante la vigencia: coeficiente × cuota
                x = dist["E2_propia"]["x"]
                for sub, delta, rot, nota in (("extremos", 0.0, "variación entre extremos del periodo", "el régimen de la Ley 11/2020 ya no estaba vigente en 2022T2 (STC 37/2022; reversión estimada −0,0016): la variación entre extremos del factor es 0"),
                                              ("vigencia", share, "durante la vigencia 2020T4-2022T1 (nivel medio, no cambio entre extremos)", "diferencia de E2-R1 × cuota de contratos en municipios regulados; nivel medio durante la vigencia")):
                    contrib = x * 100.0 * delta + 0.0
                    e = estad(contrib)
                    filas.append({"marco": "ilustracion", "alineacion": "plan", "resultado": "alquiler_contratos_nuevos", "periodo": nombre, "territorio_tipo": tipo, "territorio": cod, "nombre": nom,
                                  "factor": "E2", "tipo_fila": f"factor_{sub}", "origen_magnitud": dist["E2_propia"]["ref"], "magnitud_centro": dist["E2_propia"]["centro"],
                                  "clase_estimacion_propia": "SUGESTIVO", "variacion_factor": delta, "ventana_factor": f"cuota de contratos en {n_reg} de {n_mun} municipios con contratos (sin Barcelona ciudad ni sellados)",
                                  "obs_pp": obs, "contrib_med": e["med"], "p16": e["p16"], "p84": e["p84"], "p05": e["p05"], "p95": e["p95"],
                                  "pct_de_obs": e["med"] / obs * 100.0 if abs(obs) >= 1.0 else np.nan,
                                  "soporte": "dentro del soporte (cuota entre 0 y 1: combinación de municipios tratados y de control de la muestra)",
                                  "rotulo": "relativa entre municipios (regulados frente a no regulados de Cataluña), sin el componente común", "en_suma": sub == "extremos",
                                  "nota": rot + "; " + nota + "; la renta observada es la de contratos nuevos del Incasòl (nominal menos deflactor); frase de limitación de E2-R1 obligatoria al difundir"})
                    if sub == "extremos":
                        e2 = estad(obs - contrib)
                        filas.append({"marco": "ilustracion", "alineacion": "plan", "resultado": "alquiler_contratos_nuevos", "periodo": nombre, "territorio_tipo": tipo, "territorio": cod,
                                      "nombre": nom, "factor": "NOEXPL", "tipo_fila": "no_explicado", "origen_magnitud": "", "magnitud_centro": np.nan, "clase_estimacion_propia": "",
                                      "variacion_factor": np.nan, "ventana_factor": vent, "obs_pp": obs, "contrib_med": e2["med"], "p16": e2["p16"], "p84": e2["p84"], "p05": e2["p05"], "p95": e2["p95"],
                                      "pct_de_obs": e2["med"] / obs * 100.0 if abs(obs) >= 1.0 else np.nan, "soporte": "", "rotulo": "relativa entre municipios, sin el componente común",
                                      "en_suma": True, "nota": "Δ observada (extremos) menos la contribución entre extremos (0)"})
            else:
                filas.append({"marco": "ilustracion", "alineacion": "plan", "resultado": "alquiler_contratos_nuevos", "periodo": nombre, "territorio_tipo": tipo, "territorio": cod, "nombre": nom,
                              "factor": "E2", "tipo_fila": "factor_sin_magnitud", "origen_magnitud": "", "magnitud_centro": np.nan, "clase_estimacion_propia": "NO ESTIMABLE (E2-A1)",
                              "variacion_factor": np.nan, "ventana_factor": vent, "obs_pp": obs, "contrib_med": np.nan, "p16": np.nan, "p84": np.nan, "p05": np.nan, "p95": np.nan, "pct_de_obs": np.nan,
                              "soporte": "fuera del soporte (régimen distinto)", "rotulo": "", "en_suma": False,
                              "nota": "zonas tensionadas de la Ley 12/2023 desde 2024: otro régimen; la magnitud de la Ley 11/2020 no se extrapola (E2-A1 es NO ESTIMABLE por variación)"})
    # E1 en Barcelona ciudad (alquiler de contratos nuevos del Incasòl; Segú, un solo estudio)
    for nombre, pa, pb in PERIODOS[3:]:
        a, b = ini_nivel(pa), qi(pb)
        obs, vent = obs_barcelona_alquiler(dat, a, b)
        d1 = delta_e1_barcelona(dat, a, b)
        if np.isnan(obs) or np.isnan(d1["delta"]):
            continue
        x = dist["E1"]["x"]
        contrib = x * 100.0 * d1["delta"]
        e = estad(contrib)
        filas.append({"marco": "ilustracion", "alineacion": "plan", "resultado": "alquiler_contratos_nuevos", "periodo": nombre, "territorio_tipo": "ciudad", "territorio": "08019", "nombre": "Barcelona",
                      "factor": "E1", "tipo_fila": "factor", "origen_magnitud": dist["E1"]["ref"] + " (Segú 2018)", "magnitud_centro": dist["E1"]["centro"], "clase_estimacion_propia": "NO ESTIMABLE",
                      "variacion_factor": d1["delta"], "ventana_factor": d1["ventana"], "obs_pp": obs, "contrib_med": e["med"], "p16": e["p16"], "p84": e["p84"], "p05": e["p05"], "p95": e["p95"],
                      "pct_de_obs": e["med"] / obs * 100.0 if abs(obs) >= 1.0 else np.nan, "soporte": "soporte no evaluable (una sola ciudad)", "rotulo": REL, "en_suma": True,
                      "nota": "ilustración con magnitud de la literatura (por pp de densidad de Airbnb; aquí viviendas registradas HUT por 100 viviendas: medidas distintas); la ciudad tiene distritos sellados en V15/V16, su total municipal es una fuga declarada (adenda 1.5)"})
        e2 = estad(obs - contrib)
        filas.append({"marco": "ilustracion", "alineacion": "plan", "resultado": "alquiler_contratos_nuevos", "periodo": nombre, "territorio_tipo": "ciudad", "territorio": "08019", "nombre": "Barcelona",
                      "factor": "NOEXPL", "tipo_fila": "no_explicado", "origen_magnitud": "", "magnitud_centro": np.nan, "clase_estimacion_propia": "", "variacion_factor": np.nan, "ventana_factor": vent,
                      "obs_pp": obs, "contrib_med": e2["med"], "p16": e2["p16"], "p84": e2["p84"], "p05": e2["p05"], "p95": e2["p95"],
                      "pct_de_obs": e2["med"] / obs * 100.0 if abs(obs) >= 1.0 else np.nan, "soporte": "", "rotulo": REL, "en_suma": True, "nota": ""})


def construir_principal(dat: Datos, periodos, alineacion: str, filas: list[dict], estados_b5: dict, solo_nacional: bool = False) -> None:
    """Contabilidad principal: sin magnitud preferida con estimación propia en ningún factor; todo queda en «no explicado»."""
    for nombre, pa, pb, *_ in periodos:
        a, b = ini_nivel(pa), qi(pb)
        ys = anio_ini(pa)
        for resultado in ("precio", "alquiler"):
            obs = obs_territorios(dat, resultado, a, b, ys)
            for _, o in obs.iterrows():
                if solo_nacional and o.tipo != "nacional":
                    continue
                v = o.obs if o.tipo == "nacional" else o.obs_rel
                if np.isnan(v):
                    continue
                if o.tipo == "nacional":
                    for f in FACTORES:
                        filas.append({"marco": "principal", "alineacion": alineacion, "resultado": resultado, "periodo": nombre, "territorio_tipo": o.tipo, "territorio": o.codigo, "nombre": o.nombre,
                                      "factor": f, "tipo_fila": "factor", "origen_magnitud": "", "magnitud_centro": np.nan, "clase_estimacion_propia": estados_b5[f]["clase"], "variacion_factor": np.nan,
                                      "ventana_factor": "", "obs_pp": v, "contrib_med": np.nan, "p16": np.nan, "p84": np.nan, "p05": np.nan, "p95": np.nan, "pct_de_obs": np.nan,
                                      "soporte": "", "rotulo": "", "en_suma": False, "nota": "sin magnitud: " + estados_b5[f]["motivo"]})
                filas.append({"marco": "principal", "alineacion": alineacion, "resultado": resultado, "periodo": nombre, "territorio_tipo": o.tipo, "territorio": o.codigo, "nombre": o.nombre,
                              "factor": "OBS", "tipo_fila": "observado", "origen_magnitud": "", "magnitud_centro": np.nan, "clase_estimacion_propia": "", "variacion_factor": np.nan,
                              "ventana_factor": o.ventana, "obs_pp": v, "contrib_med": np.nan, "p16": np.nan, "p84": np.nan, "p05": np.nan, "p95": np.nan, "pct_de_obs": 100.0 if abs(v) >= 1 else np.nan,
                              "soporte": "", "rotulo": "" if o.tipo == "nacional" else REL, "en_suma": False,
                              "nota": "variación observada del resultado real (100·Δln, valor tasado o IPC de alquiler menos deflactor)" + ("" if o.tipo == "nacional" else "; fila relativa a la media simple de las provincias no selladas con dato" + o.ventana_comun)})
                filas.append({"marco": "principal", "alineacion": alineacion, "resultado": resultado, "periodo": nombre, "territorio_tipo": o.tipo, "territorio": o.codigo, "nombre": o.nombre,
                              "factor": "NOEXPL", "tipo_fila": "no_explicado", "origen_magnitud": "", "magnitud_centro": np.nan, "clase_estimacion_propia": "", "variacion_factor": np.nan,
                              "ventana_factor": o.ventana, "obs_pp": v, "contrib_med": v, "p16": v, "p84": v, "p05": v, "p95": v, "pct_de_obs": 100.0 if abs(v) >= 1 else np.nan, "soporte": "",
                              "rotulo": "" if o.tipo == "nacional" else REL, "en_suma": True,
                              "nota": "ningún factor tiene magnitud preferida con estimación propia (B5): todo queda sin explicar; la variación observada no es un resultado de factores"
                                      + ("" if o.tipo == "nacional" else o.ventana_comun)})


def estados_b5() -> dict:
    mag = pd.read_csv(OUT / "magnitudes.csv")
    out = {}
    for f in FACTORES:
        r = mag[mag.factor == f].iloc[0]
        out[f] = {"clase": str(r.clase_estimacion_propia), "motivo": f"{r.estado_b5}; {r.motivo_propia}"}
    return out


# ------------------------------------------------------------------------------------------------ comparación con V8
def comparar_v8(ilu: pd.DataFrame) -> pd.DataFrame:
    v8 = pd.read_csv(RAIZ / "output" / "v8" / "F5" / "atribucion_combinada.csv")
    v8 = v8[(v8.metodo == "svar_hd") & (v8.ambito == "nacional") & (v8.variante.isin(["V3", "larga"]))]
    corr = {"demografia": ["E3", "E9"], "credito_tipos": ["E7"], "oferta": ["E5", "E6"], "empleo_renta": ["F1 (sensibilidad)"], "turismo": ["E1"]}
    filas = []
    nac = ilu[(ilu.territorio_tipo == "nacional") & (ilu.alineacion == "v8") & (ilu.resultado == "precio")]
    for r in v8[v8.mercado == "compra"].itertuples():
        for f in corr.get(r.factor, []):
            x = nac[nac.factor == f]
            pmap = {"P1": "1995T1-2007T4", "P2": "2008T3-2013T4", "P3": "2014T1-2019T4", "P4": "2020T2-2022T2", "P5": "2022T3-2026T2"}
            if r.periodo not in pmap:
                continue
            x = x[x.periodo == pmap[r.periodo]]
            if r.variante == "larga" and r.periodo != "P1":
                continue
            if x.empty:
                filas.append({"periodo_v8": r.periodo, "factor_v8": r.factor, "factor_v18": f, "v8_mediana": r.mediana, "v8_b68_lo": r.b68_lo, "v8_b68_hi": r.b68_hi, "v18_mediana": np.nan,
                              "v18_p16": np.nan, "v18_p84": np.nan, "mismo_signo": "", "intervalos_solapan": "", "variante_v8": r.variante, "nota": "V18 sin cifra para este factor y periodo (sin variación medida, fuera del soporte o sin magnitud)"})
                continue
            x = x.iloc[0]
            if np.isnan(x.contrib_med):
                filas.append({"periodo_v8": r.periodo, "factor_v8": r.factor, "factor_v18": f, "v8_mediana": r.mediana, "v8_b68_lo": r.b68_lo, "v8_b68_hi": r.b68_hi, "v18_mediana": np.nan,
                              "v18_p16": np.nan, "v18_p84": np.nan, "mismo_signo": "", "intervalos_solapan": "", "variante_v8": r.variante, "nota": f"V18 {x.soporte}: sin cifra"})
                continue
            filas.append({"periodo_v8": r.periodo, "factor_v8": r.factor, "factor_v18": f, "v8_mediana": r.mediana, "v8_b68_lo": r.b68_lo, "v8_b68_hi": r.b68_hi, "v18_mediana": x.contrib_med,
                          "v18_p16": x.p16, "v18_p84": x.p84, "mismo_signo": bool(np.sign(r.mediana) == np.sign(x.contrib_med)), "intervalos_solapan": bool(max(r.b68_lo, x.p16) <= min(r.b68_hi, x.p84)),
                          "variante_v8": r.variante, "nota": "contabilidad con elasticidades de la literatura (ilustración) frente a descomposición histórica del SVAR (C3s): no se suman ni se promedian"})
    return pd.DataFrame(filas)


# ------------------------------------------------------------------------------------------------ respuesta, hechos e informe
CONFIANZA = {
    "E2": "la evidencia sugiere (E2-R1, SUGESTIVO, fuera de B5: sin magnitud preferida)",
    "otro": "la evidencia no permite concluir (sin estimación propia estimable; magnitud solo de la literatura)",
}


def respuesta(cp: pd.DataFrame, ci: pd.DataFrame) -> pd.DataFrame:
    filas = []
    base = ci[(ci.alineacion == "plan") & ci.territorio_tipo.isin(["nacional", "ccaa", "ciudad"]) & (ci.resultado == "precio")]
    for (res, per, tt, cod), g in base.groupby(["resultado", "periodo", "territorio_tipo", "territorio"], sort=False):
        f = g[(g.tipo_fila == "factor") & g.en_suma & g.contrib_med.notna()]
        ne = g[g.tipo_fila == "no_explicado"]
        alt = g[g.tipo_fila == "no_explicado_alternativa"]
        obs = g.obs_pp.iloc[0]
        nombre = g.nombre.iloc[0]
        if f.empty:
            continue
        mayor = f.loc[f.contrib_med.abs().idxmax()]
        filas.append({"resultado": res, "periodo": per, "territorio_tipo": tt, "territorio": cod, "nombre": nombre, "obs_pp": obs, "factor_mayor": mayor.factor,
                      "contrib_med": mayor.contrib_med, "p16": mayor.p16, "p84": mayor.p84, "pct_de_obs": mayor.pct_de_obs,
                      "no_explicado_principal_pct": 100.0 if abs(obs) >= 1 else np.nan,
                      "no_explicado_ilustracion_pct": ne.pct_de_obs.iloc[0] if len(ne) else np.nan,
                      "no_explicado_alt_E9_pct": alt.pct_de_obs.iloc[0] if len(alt) else np.nan,
                      "confianza": CONFIANZA["otro"], "nota": "ilustración con magnitudes de la literatura; en la contabilidad principal todo queda sin explicar"})
    loc = ci[ci.resultado == "alquiler_contratos_nuevos"]
    for (per, cod), g in loc.groupby(["periodo", "territorio"], sort=False):
        f = g[(g.factor.isin(["E1", "E2"])) & (g.tipo_fila.isin(["factor", "factor_extremos"])) & g.contrib_med.notna()]
        ne = g[g.tipo_fila == "no_explicado"]
        if f.empty:
            continue
        r = f.iloc[0]
        filas.append({"resultado": "alquiler_contratos_nuevos", "periodo": per, "territorio_tipo": r.territorio_tipo, "territorio": cod, "nombre": r.nombre, "obs_pp": r.obs_pp,
                      "factor_mayor": r.factor, "contrib_med": r.contrib_med, "p16": r.p16, "p84": r.p84, "pct_de_obs": r.pct_de_obs, "no_explicado_principal_pct": 100.0,
                      "no_explicado_ilustracion_pct": ne.pct_de_obs.iloc[0] if len(ne) else np.nan, "no_explicado_alt_E9_pct": np.nan,
                      "confianza": CONFIANZA["E2"] if r.factor == "E2" else CONFIANZA["otro"], "nota": "factor local; contribución entre extremos del periodo"})
    return pd.DataFrame(filas)


CLASE_HECHO = {"SUGESTIVO": "SUGESTIVO", "ASOCIACIÓN": "ASOCIACIÓN", "NO ESTIMABLE": "NO ESTIMABLE", "NO CONCLUYENTE": "NO CONCLUYENTE"}


def _clase(s: str) -> str:
    """Clase de la estimación propia designada, también cuando magnitudes.csv la escribe como «no entra (ASOCIACIÓN)» (K12)."""
    s = str(s)
    for k in ("SUGESTIVO", "ASOCIACIÓN", "NO CONCLUYENTE"):
        if s.startswith(k) or f"({k}" in s:
            return k
    return "NO ESTIMABLE"


def _periodo_estudios(factor: str) -> str:
    """Periodo de los datos de los estudios que forman la magnitud o el rango de B5 del factor (K12; antes «estudios 1983-2024» en todos)."""
    e = pd.read_csv(OUT / "magnitudes_estudios.csv")
    e = e[(e.factor == factor) & e.valor.notna()]
    if (e.entra_en_B5 == "sí").any():
        e = e[e.entra_en_B5 == "sí"]
    else:   # sin metaanálisis: los estudios que forman el rango de la literatura
        e = e[e.estudio.isin(MAG.rango_estudios(factor, MAG.estudios_todos())[2])]
    anios = [int(a) for ref in e.referencia for a in re.findall(r"\b((?:19|20)\d\d)", str(ref).split("), ", 1)[-1])]
    return f"estudios {min(anios)}-{max(anios)}" if anios else "estudios (sin periodo en la ficha)"


def _periodo_real(nombre: str, ventana: str) -> str:
    """Periodo del dato: el del plan, salvo que la serie empiece después (por ejemplo, provincias desde 2002T1; árbitro, hallazgo 1)."""
    m = re.match(r"(\d{4}T\d) a (\d{4}T\d)", str(ventana))
    if not m:
        return nombre
    pa, pb = nombre.split("-")
    return nombre if m.group(1) in (pa, qs(ini_nivel(pa))) else f"{m.group(1)}-{m.group(2)}"


def _v(x):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), 4)


def hechos(mag: pd.DataFrame, cp: pd.DataFrame, ci: pd.DataFrame) -> list[dict]:
    fuentes_b = ["output/v18/f5/magnitudes_estudios.csv", "output/v18/f1/catalogo.csv", "docs/v18/plan_replicacion_adenda.md (1.9)"]
    h = []
    for r in mag.itertuples():
        vals = [r.magnitud, r.ic_lo, r.ic_hi, r.rango_lo, r.rango_hi]
        mu = _v(r.magnitud) if str(r.magnitud) not in ("", "nan") else None
        lo = _v(r.ic_lo) if str(r.ic_lo) not in ("", "nan") else _v(r.rango_lo)
        hi = _v(r.ic_hi) if str(r.ic_hi) not in ("", "nan") else _v(r.rango_hi)
        propia = str(r.origen).startswith("propia")
        lim = "" if str(r.limitacion) in ("", "nan") else f"{r.limitacion}. "
        # K14 (árbitro, ronda 2, N1): cobertura sin paréntesis anidados, para que el documento la use como frase
        n = int(r.n_estudios)
        cob = ((f"{n} estudios con error típico en la unidad; método: {r.metodo}" if n > 1 else
                ("1 estudio con error típico en la unidad" if n == 1 else "ningún estudio con error típico en la unidad"))
               + f"; estado B5: {r.estado_b5}")
        h.append({"id": f"V18-B5-{r.factor}", "indicador": f"Magnitud preferida de {NOMBRE_FACTOR[r.factor]} ({r.factor}): {r.unidad}", "valor": mu, "min": lo, "max": hi, "unidad": r.unidad,
                  "periodo": _periodo_estudios(r.factor), "cobertura": cob, "fuentes": fuentes_b,
                  "capa": "C4", "clasificacion_v18": _clase(r.clase_estimacion_propia),
                  "nota": f"{r.origen}. Estimación propia designada {r.estimacion_propia}: {r.clase_estimacion_propia}. {lim}" + ("" if propia else "Magnitud de la literatura; ")
                  + "la clasificación es la de la estimación propia designada del factor, no la de la magnitud ni la del rango (K12); "
                  + f"{ROTULO}."})
    # principal: nacional y CCAA. Si las provincias no empiezan todas a la vez, la media provincial mezcla ventanas (K12, árbitro, hallazgo 1)
    pv = cp[(cp.territorio_tipo == "provincia") & (cp.tipo_fila == "no_explicado") & (cp.alineacion == "plan")]
    mezcla = {}
    for (res_, per_), g in pv.groupby(["resultado", "periodo"]):
        ini = g.ventana_factor.str.slice(0, 6).value_counts()
        if len(ini) > 1:
            mezcla[(res_, per_)] = ("la media provincial mezcla ventanas (" + "; ".join(f"{n} provincias desde {i}" for i, n in ini.items())
                                    + "): las filas relativas de este periodo no son comparables entre sí; ")
    for r in cp[(cp.tipo_fila != "observado")].itertuples():
        if r.territorio_tipo not in ("nacional", "ccaa") or r.alineacion != "plan":
            continue
        ab = "P" if r.resultado == "precio" else "A"
        pid = f"V18-C5-{r.periodo}-{r.territorio}-{r.factor}-{ab}"
        if r.tipo_fila == "factor":
            h.append({"id": pid, "indicador": f"Contribución de {NOMBRE_FACTOR[r.factor]} a la variación del {r.resultado} real, {r.periodo}, {r.nombre}", "valor": None, "min": None, "max": None,
                      "unidad": "pp (100·Δln)", "periodo": r.periodo, "cobertura": r.nombre, "fuentes": ["output/v18/f5/contabilidad.csv"], "capa": "C4", "clasificacion_v18": _clase(r.clase_estimacion_propia),
                      "nota": f"sin magnitud: {r.nota}. Contabilidad con elasticidades, no descomposición estructural. {ROTULO}."})
        else:
            per = _periodo_real(r.periodo, r.ventana_factor)
            rel = r.territorio_tipo != "nacional"
            ind = f"Variación del {r.resultado} real sin explicar, {per}, {r.nombre}" + (" (relativa a la media de las provincias no selladas, sin el componente común)" if rel else "")
            rot = f"{REL_PROV}; {mezcla.get((r.resultado, r.periodo), '')}" if rel else ""
            aviso = f"periodo del dato {per} (la serie empieza después del inicio del periodo del plan {r.periodo}); " if per != r.periodo else ""
            h.append({"id": pid, "indicador": ind, "valor": _v(r.contrib_med), "min": _v(r.p05), "max": _v(r.p95), "unidad": "pp (100·Δln)",
                      "periodo": per, "cobertura": f"{r.nombre}; {r.ventana_factor}", "fuentes": ["output/v18/f5/contabilidad.csv", "data/base/hechos.parquet (valor tasado, IPC de alquiler, deflactor)"], "capa": "C4",
                      "clasificacion_v18": "NO ESTIMABLE", "nota": f"{r.nota}; {aviso}{rot}{ROTULO}.".replace("  ", " ")})
    # ilustración: nacional, CCAA y ciudades
    # K14 (árbitro, ronda 2, N4): las filas «no explicado» de la ilustración no entran en hechos.json. En la nacional se restan de la
    # variación nacional magnitudes relativas entre provincias (E3, E9) y una nacional (E7): la resta mezcla componentes y no se interpreta;
    # en las demás, la ilustración no es una atribución y la diferencia no añade nada a las filas de cada factor. Siguen en
    # contabilidad_ilustracion.csv con su rótulo. Para leer cada fila de factor frente a lo observado: la variación observada está en las
    # filas V18-C5 (nacional y comunidades) y, en las unidades locales del alquiler de contratos nuevos, en las filas OBS de abajo.
    sub = ci[ci.territorio_tipo.isin(["nacional", "ccaa", "ciudad"]) & (ci.alineacion == "plan") & ~ci.tipo_fila.str.startswith("no_explicado")]
    loc = sub[sub.resultado == "alquiler_contratos_nuevos"].drop_duplicates(["periodo", "territorio"])
    for r in loc.itertuples():
        h.append({"id": f"V18-C5I-{r.periodo}-{r.territorio}-OBS-N", "indicador": f"Variación observada de la renta real de los contratos nuevos de alquiler (Incasòl), {r.periodo}, {r.nombre}",
                  "valor": _v(r.obs_pp), "min": None, "max": None, "unidad": "pp (100·Δln)", "periodo": r.periodo, "cobertura": r.nombre,
                  "fuentes": ["output/v18/f5/contabilidad_ilustracion.csv", "data/base/hechos.parquet"], "capa": "C4", "clasificacion_v18": "NO ESTIMABLE",
                  "nota": "variación observada (renta nominal de los contratos nuevos del Incasòl menos el deflactor), no un resultado de factores; "
                          f"se lee al lado de las filas de la ilustración, sin restarlas (K14). {ROTULO}."})
    for r in sub.itertuples():
        ab = {"precio": "P", "alquiler": "A", "alquiler_contratos_nuevos": "N"}[r.resultado]
        fac = r.factor + ("-" + r.tipo_fila.split("_")[1] if r.tipo_fila in ("factor_extremos", "factor_vigencia") else "")
        pid = f"V18-C5I-{r.periodo}-{r.territorio}-{fac}-{ab}"
        es_e2 = r.factor == "E2"
        # K12 (árbitro, hallazgos 2 y 6): la clase de E2-R1 no se traslada a la ilustración, porque E2 no tiene magnitud preferida en B5
        clase = "NO ESTIMABLE"
        origen = "magnitud de la literatura" if not es_e2 else ("sin magnitud preferida para E2 (B5); ilustración con E2-R1 propia sola, fuera de B5: "
                                                                "la clase de E2-R1 (SUGESTIVO) no se traslada a esta fila")
        aviso = ""
        nombre_f = NOMBRE_FACTOR.get(r.factor, "variación sin explicar")
        h.append({"id": pid, "indicador": f"Ilustración: {nombre_f}, {r.resultado} real, {r.periodo}, {r.nombre} ({r.tipo_fila})", "valor": _v(r.contrib_med), "min": _v(r.p05), "max": _v(r.p95), "unidad": "pp (100·Δln)",
                  "periodo": r.periodo, "cobertura": f"{r.nombre}; {r.ventana_factor}", "fuentes": ["output/v18/f5/contabilidad_ilustracion.csv", "data/base/hechos.parquet", "output/v18/f5/magnitudes.csv"],
                  "capa": "C4", "clasificacion_v18": clase,
                  "nota": f"{origen}; ilustración, no atribución; mínimo y máximo: percentiles 5 y 95 de la propagación; {aviso}{r.soporte}; {r.rotulo}. Contabilidad con elasticidades, no descomposición estructural. {ROTULO}.".replace("nan", "")})
    return h


def f(x, d=1) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.{d}f}".replace(".", ",")


def tabla_md(df: pd.DataFrame, cols: list[str], cab: list[str] | None = None) -> str:
    cab = cab or cols
    lin = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lin.append("| " + " | ".join("" if (isinstance(r[c], float) and not np.isfinite(r[c])) else str(r[c]) for c in cols) + " |")
    return "\n".join(lin)


def informe(mag: pd.DataFrame, est: pd.DataFrame, sens: pd.DataFrame, cp: pd.DataFrame, ci: pd.DataFrame, resp: pd.DataFrame, v8: pd.DataFrame) -> str:
    L = []
    L.append("# V18 · Fase 5 · Magnitudes preferidas y contabilidad de la subida\n")
    L.append(f"**{ROTULO}.** Nivel de evidencia EXPLORATORIO; toda cifra es C4 y la clasificación V18 va al lado. Código: `src/v18/f5_magnitudes.py` y `src/v18/f5_contabilidad.py`; SEED 20261010, 10.000 extracciones; sin red.\n")
    # resumen
    n_pref = int((mag.estado_b5 == "magnitud preferida").sum())
    L.append("## 1. Resumen\n")
    L.append("- **B5 (magnitud preferida).** La adenda 1.9 fija una estimación propia por factor. Solo **E2-R1** (Ley 11/2020, SUGESTIVO) tiene diseño válido y no es NO ESTIMABLE; E1, E3, E4, E5, E6, E7 y E9 salen NO ESTIMABLE y E8-R1 es ASOCIACIÓN (K7): no entran. E1-R4 y E3-R1 (NO CONCLUYENTE) no son las estimaciones designadas de su factor y están en otra unidad: se muestran al lado, sin combinar.")
    e2 = mag[mag.factor == "E2"].iloc[0]
    L.append(f"- **E2 no tiene magnitud preferida:** con el episodio catalán (E2-R1, Jofre-Monseny et al. y Monràs y García-Montalvo, ρ = 0,8, contado una vez), Breuille et al. y Hahn et al. la decisión no coincide en las tres priors (el intervalo de credibilidad al 95 % con la prior s/2 incluye el cero) y I² = {f(e2.I2,2)} con un intervalo de predicción que cambia de signo (regla del plan). Se publica el rango de las tres priors: {f(e2.rango_lo,3)} a {f(e2.rango_hi,3)}. La única magnitud con diseño propio es −0,038 (IC95 −0,051 a −0,026) en Cataluña, con la frase de limitación de la sección 2.")
    L.append(f"- **Magnitud preferida solo con literatura:** E1 (un estudio, Segú 2018), E4 (θ, dos estudios con error, efecto fijo con heterogeneidad) y E6 (un estudio, Mense 2025). E3 y E5 tienen 5 y 3 estudios en la unidad, pero I² > 75 % e intervalo de predicción que cambia de signo: rango sin magnitud preferida. E7, E8 y E9 no tienen ningún estudio con error típico en la unidad: rango de la literatura sin intervalo estadístico.")
    L.append("- **Contabilidad principal (adenda 1.10):** ningún factor tiene magnitud preferida construida con una estimación propia IDENTIFICADO o SUGESTIVO. Cada factor dice «sin magnitud» (no cero) y toda la variación observada queda en «no explicado» (100 %).")
    L.append("- **Ilustración con magnitudes de la literatura** (tabla aparte, rotulada así): no es una atribución. Sus resultados, con cualquier magnitud, dejan sin explicar la mayor parte de la variación en casi todos los periodos y territorios (secciones 4 y 5).\n")
    L.append("**Es contabilidad con elasticidades estimadas, no una descomposición estructural:** contribución = magnitud × variación observada del factor; sin interacciones ni efectos de equilibrio general, y los factores no son ortogonales.\n")
    # B5
    L.append("## 2. Magnitud preferida por factor (B5)\n")
    m2 = mag.copy()

    def mp(r):
        if str(r.magnitud) not in ("", "nan"):
            return f(float(r.magnitud), 3)
        return "sin magnitud preferida"

    def inter(r):
        if str(r.ic_lo) not in ("", "nan"):
            return f"[{f(float(r.ic_lo),3)}; {f(float(r.ic_hi),3)}] (IC95)"
        if str(r.rango_lo) not in ("", "nan"):
            return f"rango [{f(float(r.rango_lo),3)}; {f(float(r.rango_hi),3)}]"
        return "—"

    def het(r):
        if str(r.I2) not in ("", "nan") and str(r.tau) not in ("", "nan"):
            return f"τ = {f(float(r.tau),3)}; I² = {f(float(r.I2),2)}"
        if str(r.I2) not in ("", "nan"):
            return f"I² = {f(float(r.I2),2)} (Q, K = 2)"
        return "no estimable"

    m2["magnitud_preferida"] = [mp(r) for r in m2.itertuples()]
    m2["intervalo"] = [inter(r) for r in m2.itertuples()]
    m2["heterogeneidad"] = [het(r) for r in m2.itertuples()]
    m2["lim"] = [f"{r.estado_b5}. {r.limitacion if isinstance(r.limitacion, str) else ''}".strip() for r in m2.itertuples()]
    L.append(tabla_md(m2, ["factor", "magnitud_preferida", "intervalo", "heterogeneidad", "n_estudios", "origen", "lim"],
                      ["factor", "magnitud preferida", "intervalo", "heterogeneidad", "n estudios", "origen (propia/literatura)", "limitación"]))
    L.append("\nUnidades: " + "; ".join(f"{r.factor}: {r.unidad}" for r in mag.itertuples()) + ".\n")
    L.append("**Advertencia del Monte Carlo (K5).** El metaanálisis bayesiano (herr18/meta_bayes) es NO APTO por conservador: con verdades fijas la cobertura de μ es 0,96-0,99 (intervalos que cubren de más), el prior s/2 queda corto en calibración (0,85-0,92) y, con K = 2, el efecto fijo cubre μ solo 0,50-0,56 si hay heterogeneidad. Los intervalos de las filas con K ≥ 3 son por tanto prudentes y los de las filas con K = 2 no deben leerse como IC95 fiables. La regla «la decisión debe coincidir en las tres priors» parte de intervalos conservadores.\n")
    L.append("### Estudios y estado de la ficha\n")
    e = est[["factor", "estudio", "estado_ficha", "valor", "error_tipico", "entra_en_B5", "etiqueta_I6", "motivo_si_no_entra"]].copy()
    e["valor"] = e.valor.map(lambda x: f(x, 3) if isinstance(x, float) else x)
    e["error_tipico"] = e.error_tipico.map(lambda x: f(x, 3) if isinstance(x, float) else x)
    L.append(tabla_md(e, list(e.columns), ["factor", "estudio", "estado de la ficha", "valor", "error típico", "entra", "etiqueta I6", "motivo si no entra"]))
    L.append("\nEl estado es el de `docs/v18/bib` según el verificador de DOI (VERIFICADA, NO VERIFICADA, DISCREPANTE por versión de trabajo frente a publicada); el cuartil Scimago no está verificado. Todas las referencias de B5 y de I6 llevan su estado (adenda 1.9, R-26). Las cifras con «solo resumen» no se han leído en texto completo.\n")
    L.append("### Episodios compartidos y sensibilidad\n")
    L.append("- **E2:** la estimación propia, Jofre-Monseny et al. (2023) y Monràs y García-Montalvo (2023) usan el mismo registro (Incasòl) y el mismo episodio: entran como un solo episodio, combinados con ρ = 0,8 por mínima varianza con pesos no negativos. Con ρ = 0,8 los pesos son 0,325 (E2-R1), 0,675 (Jofre-Monseny) y 0 (Monràs); con ρ = 1 se queda con la más precisa.")
    L.append("- **E3:** González y Ortega (2009, IZA; 2011, Chicago Fed; 2013, J. Regional Science) son versiones del mismo trabajo: cuentan una vez (versión de 2009, que es la que da «% por 1 %»; su error se reconstruye por proporcionalidad con el de €/m²).")
    L.append("- **E9 frente a E3 (sin doble cómputo):** ambos usan cuotas del padrón por nacionalidad; la correlación entre el índice de exposición de E9 (cuotas de 2003 de los orígenes con riesgo) y el instrumento medio de E3-R1 es 0,85 (output/v18/estimacion/e9/informe.md). No se suman: la principal usa E3 y E9 va como alternativa.\n")
    s = sens.copy()
    for c in ("mu", "lo", "hi"):
        s[c] = s[c].map(lambda x: f(x, 3) if isinstance(x, float) else x)
    L.append(tabla_md(s, ["factor", "variante", "k", "estado", "mu", "lo", "hi", "I2", "notas"], ["factor", "variante", "K", "estado", "μ o media", "lo", "hi", "I²", "notas"]))
    L.append("\n**La estimación propia de E2 (K9), con su frase de limitación obligatoria al difundir la cifra:** «" + MAG.frase_limitacion_e2() + "»\n")
    # contabilidad
    L.append("## 3. Contabilidad principal (adenda 1.10)\n")
    L.append("La adenda 1.10 deroga el filtro «al menos una estimación IDENTIFICADO o SUGESTIVO» y manda usar «todo factor con magnitud preferida de B5, construida con las reglas de 1.9», con la clase de su estimación propia como techo de la confianza y «sin magnitud» (no cero) para el resto. Lectura aplicada: el plan (sección 4) deja las magnitudes «solo literatura» en una tabla secundaria rotulada; la adenda no lo revoca, y una magnitud sin estimación propia no tiene clase que ponga techo a la confianza. Por eso la tabla principal solo admitiría factores con estimación propia dentro de B5, y ninguno lo cumple: **la contabilidad principal no tiene filas con cifra.** Se dice así y todo se deja en «no explicado»; la ilustración va aparte (sección 4).\n")
    nac = cp[(cp.alineacion == "plan") & (cp.territorio_tipo == "nacional") & (cp.tipo_fila == "observado")]
    nr = nac.pivot_table(index="periodo", columns="resultado", values="obs_pp", aggfunc="first")
    nr = nr.reset_index()
    nr["precio"] = nr.precio.map(lambda x: f(x, 1))
    nr["alquiler"] = nr.alquiler.map(lambda x: f(x, 1))
    nr["no_explicado"] = "100 % (sin magnitud en ningún factor)"
    L.append(tabla_md(nr, ["periodo", "precio", "alquiler", "no_explicado"], ["periodo", "Δ precio real (pp)", "Δ alquiler real (pp)", "no explicado"]))
    L.append("\nΔ observada = 100·Δln del valor tasado (MIVAU) o del IPC de alquiler, menos el deflactor del PIB del INE (base:deflactor): difiere del IPC general que usó V8, por lo que las cifras de variación observada no coinciden con las de V8 (P4 y P5 sobre todo). El alquiler de 1995-2007 solo existe desde 2002T1. Las tablas provinciales y de CCAA (en `contabilidad.csv`) son **relativas a la media de las provincias no selladas** y no suman el total nacional. Cantabria no tiene serie provincial de valor tasado en la base (38 provincias con dato, no 39) y su CCAA queda fuera. 11 provincias selladas (v6) y los municipios de V15 y V16 se excluyen.\n")
    # ilustración
    L.append("## 4. Ilustración con magnitudes de la literatura (no es una atribución)\n")
    L.append("Magnitud: rango uniforme entre los estudios (E3, E7, E8, E9; sin intervalo estadístico), efecto fijo o estudio único (E1) y, para Cataluña, E2-R1 propia sola. Variación observada del factor sin error (una sola fuente). Los factores de unidad no comparable con la contabilidad (E5: elasticidad de la oferta al precio; E6: oferta nueva local de Mense; E4: sin variación medida) no tienen fila. Tipos (E7): solo cuenta el cambio de los últimos 8 trimestres del periodo; lo anterior es «fuera del horizonte estimado», sin cifra. Todas las filas de panel (E1, E2, E3, E8, E9) llevan el rótulo «" + REL + "»; solo E7 incluye el componente común. La fila nacional de esos factores usa la variación absoluta e incluye las 11 provincias selladas; se contrasta con el soporte (percentiles 5-95 de la variación provincial) y, si queda fuera, no lleva cifra.\n")
    n = ci[(ci.alineacion == "plan") & (ci.territorio_tipo == "nacional") & (ci.resultado == "precio")].copy()
    for c in ("contrib_med", "p16", "p84", "obs_pp", "variacion_factor", "pct_de_obs"):
        n[c] = n[c].map(lambda x: f(x, 1))
    L.append("### Nacional, precio real de compra (periodos del plan)\n")
    L.append(tabla_md(n, ["periodo", "factor", "variacion_factor", "contrib_med", "p16", "p84", "pct_de_obs", "obs_pp", "soporte"],
                      ["periodo", "factor", "variación del factor", "mediana (pp)", "p16", "p84", "% de la Δ obs.", "Δ obs. (pp)", "soporte"]))
    L.append("\nE9 es la alternativa de E3 (no se suman): la fila `NOEXPL_alt_E9` de `contabilidad_ilustracion.csv` da el no explicado cuando E9 sustituye a E3. Intervalos al 68 % (p16-p84); al 90 % están en el CSV (p05, p95).\n")
    loc = ci[ci.resultado == "alquiler_contratos_nuevos"].copy()
    for c in ("contrib_med", "p16", "p84", "obs_pp", "variacion_factor"):
        loc[c] = loc[c].map(lambda x: f(x, 2))
    L.append("### Cataluña (E2-R1 propia sola) y Barcelona (E1)\n")
    L.append(tabla_md(loc, ["periodo", "nombre", "factor", "tipo_fila", "variacion_factor", "contrib_med", "p16", "p84", "obs_pp"],
                      ["periodo", "territorio", "factor", "fila", "variación", "mediana (pp)", "p16", "p84", "Δ obs. (pp)"]))
    L.append("\nEn 2020T1-2022T2 el régimen de la Ley 11/2020 no estaba vigente al final (STC 37/2022; reversión estimada −0,0016): la variación entre extremos del factor es 0 y su contribución a la variación del periodo es 0; durante la vigencia (2020T4-2022T1), con E2-R1 sola (E2 no tiene magnitud preferida en B5; ilustración, no atribución), la diferencia asociada en el nivel medio de la renta de los contratos nuevos de Cataluña, ponderada por la cuota de contratos regulados, es de −2,7 pp (mediana; la cifra requiere la frase de limitación de la sección 2). La renta observada es la de contratos nuevos del Incasòl (sin Barcelona ciudad), no el IPC. Barcelona ciudad no estaba en la muestra de E2-R1 (criterio de Jofre-Monseny et al.) y no lleva cifra de E2; su cifra de E1 mide viviendas HUT por 100 viviendas con una magnitud definida por anuncios de Airbnb. En 2022T3-2026T2 la zona tensionada de 2024 es otro régimen: sin magnitud.\n")
    # respuesta
    L.append("## 5. Respuesta por periodo y territorio\n")
    L.append("Descripción sin interpretación de efectos: lo que sigue indica cuánta de la variación observada se asocia en la ilustración con cada factor y cuánta queda sin explicar. La confianza usa la escala del Banco de España (V17) y no supera la clase del factor de menor nivel que la sostiene: sin estimación propia estimable, «la evidencia no permite concluir»; E2 en Cataluña, «la evidencia sugiere» (SUGESTIVO).\n")
    rn = resp[(resp.territorio_tipo == "nacional") & (resp.resultado == "precio")].copy()
    for c in ("obs_pp", "contrib_med", "pct_de_obs", "no_explicado_principal_pct", "no_explicado_ilustracion_pct", "no_explicado_alt_E9_pct"):
        rn[c] = rn[c].map(lambda x: f(x, 1))
    L.append(tabla_md(rn, ["periodo", "obs_pp", "factor_mayor", "contrib_med", "pct_de_obs", "no_explicado_principal_pct", "no_explicado_ilustracion_pct", "no_explicado_alt_E9_pct", "confianza"],
                      ["periodo", "Δ obs. (pp)", "factor con mayor contribución", "mediana (pp)", "% de la Δ", "no explicado (principal, %)", "no explicado (ilustración, %)", "no explicado (E9 en lugar de E3, %)", "confianza"]))
    ccaa = resp[(resp.territorio_tipo == "ccaa") & (resp.resultado == "precio")]
    L.append(f"\nPor CCAA ({ccaa.nombre.nunique()} con dato; tabla completa en `respuesta.csv`): en la ilustración la mediana del porcentaje que queda sin explicar es {f(ccaa.no_explicado_ilustracion_pct.abs().median(),0)} % (valor absoluto, relativo al componente común); el factor con mayor contribución es {ccaa.factor_mayor.value_counts().idxmax()} en {int(ccaa.factor_mayor.value_counts().max())} de {len(ccaa)} combinaciones de CCAA y periodo.")
    big = ci[(ci.alineacion == "plan") & (ci.territorio_tipo == "nacional") & (ci.resultado == "precio") & (ci.tipo_fila == "factor") & ci.pct_de_obs.notna() & (ci.pct_de_obs.abs() > 50)]
    big_txt = "; ".join(f"{r.factor} en {r.periodo} ({f(r.pct_de_obs,0)} %, mediana {f(r.contrib_med,1)} pp frente a una variación de {f(r.obs_pp,1)} pp)" for r in big.itertuples()) or "ninguno"
    hb = sens[(sens.factor == "E2") & (sens.variante == "hahn_estrategia_B")].iloc[0]
    L.append("**Respuesta corta.** Con los criterios de la adenda no hay ningún factor que explique la mayor parte de la variación en ningún periodo ni territorio con respaldo propio: la contabilidad principal deja el 100 % sin explicar. Con magnitudes de la literatura, las contribuciones nacionales con cifra que superan el 50 % de la variación observada (en valor absoluto) son: " + big_txt + ". La de E9 tiene signo opuesto al de la variación observada, procede de un rango de otro país sin error típico y no se suma a E3. Qué queda sin explicar: la parte común a todas las provincias (el componente común, no identificable con diseños de panel con efectos de periodo) y la variación de los fundamentales no medidos aquí (renta y crédito: F1 es ASOCIACIÓN y no entra).\n")
    L.append(f"**Sensibilidad de E2.** Con la estrategia B de Hahn et al. (−0,075 en lugar de −0,113; la A se fijó antes de combinar, por ser la primera de la ficha) el metaanálisis sí daría magnitud preferida: {f(float(hb.mu.replace(',', '.')) if isinstance(hb.mu, str) else hb.mu,3)} [{hb.lo}; {hb.hi}], I² = {hb.I2}. Se publica como sensibilidad; no cambia la tabla principal, porque la regla se fijó antes. Si se adoptara, E2 entraría en la contabilidad con clase SUGESTIVO como techo, pero su variación entre extremos del periodo 2020-2022 sería 0 (la norma no estaba vigente al final del periodo).\n")
    # comparación V8
    L.append("## 6. Comparación con V8 y con el Banco de España (sin sumar)\n")
    L.append("**V8 (descomposición histórica del SVAR, C3s, bandas del 68 %).** V8 no designó ningún factor como el más relevante en ninguno de los diez casos. Correspondencias: demográfico ↔ inmigración (E3, E9); crédito y tipos ↔ tipos (E7); oferta ↔ E5/E6 (sin fila en V18); actividad y renta ↔ F1 (ASOCIACIÓN, no entra). Se comparan el signo y el solape de las bandas del 68 %; los periodos de V8 son los suyos (2008T3-2013T4, 2020T2-2022T2) y la Δ observada de V18 usa otro deflactor.\n")
    vv = v8.copy()
    for c in ("v8_mediana", "v8_b68_lo", "v8_b68_hi", "v18_mediana", "v18_p16", "v18_p84"):
        vv[c] = vv[c].map(lambda x: f(x, 1))
    L.append(tabla_md(vv, ["periodo_v8", "factor_v8", "factor_v18", "v8_mediana", "v8_b68_lo", "v8_b68_hi", "v18_mediana", "v18_p16", "v18_p84", "mismo_signo", "intervalos_solapan"],
                      ["periodo V8", "factor V8", "factor V18", "V8 mediana", "V8 p16", "V8 p84", "V18 mediana", "V18 p16", "V18 p84", "mismo signo", "bandas se solapan"]))
    cv = v8[v8.v18_mediana.notna() & v8.factor_v18.isin(["E3", "E7"])]
    L.append(f"\\nCon cifra en ambos lados (E3 y E7, la contabilidad principal de la ilustración): {len(cv)} comparaciones; mismo signo en {int((cv.mismo_signo == True).sum())} y bandas del 68 % que se solapan en {int((cv.intervalos_solapan == True).sum())}. Las bandas de V8 incluyen el cero casi siempre, por lo que el solape es una prueba débil; no se suman ni se promedian.")
    L.append("\n**Banco de España (referencias de V17 y fichas de `docs/v18/bib/modelos_conjunto` y `no_residentes`; no se suman).** (i) Sobrevaloración del precio: 10-15 % en diciembre de 2025 (IEF de primavera de 2026, rango entre métodos), un indicador de nivel frente a fundamentales que la contabilidad con elasticidades no replica. (ii) Tipos: San Juan (2023) estima ≈ −2 % del precio a 8 trimestres por +100 pb (BVAR, intervalos al 68 % solo en gráfico); el rango usado aquí (−5 a −2) lo incluye. (iii) Lajer Baron et al. (2024): un diferencial de unos 365.000 entre hogares y viviendas en 2022-2023 y unas 120.000 viviendas más de déficit por los no residentes; son contabilidad de cantidades, no de precios. (iv) Informe Anual 2025: no residentes 7,4 % de las compras (Alicante 33,3 %, Málaga 27,9 %, Baleares 23,0 %) y elasticidad de oferta 0,45 como cota superior (V16; cifra que el Documento Ocasional 2433 no recoge); frente a ello, el rango de E5 (0,26-0,87 entre tres estudios) es de otro orden de incertidumbre y no se usa en la contabilidad.\n")
    L.append("## 7. Contradicciones con lo publicado\n")
    L.append("Ninguna estimación propia de V18 es IDENTIFICADO, así que no hay parada G. Compatibilidad con conclusiones publicadas: (a) V8 («ningún factor puede designarse»): coherente; V18 tampoco designa ninguno. (b) Informe integral III.2 y V17: los topes de Cataluña («prometedora», −4 a −6 % en la renta regulada): E2-R1 (−3,8 %) es compatible y añade que la diferencia se apaga dentro de la vigencia. (c) V17, inmigración (≈ 1,3 % de precio por 1 % de población): cae dentro del rango de la literatura de E3 (−1,6 a 3,2); la ilustración asocia a la inmigración en torno al 10 % de la subida de 1995-2007 con la mediana de ese rango, bastante por debajo del «un cuarto» de González y Ortega (2013) para 2000-2010, que corresponde al extremo alto del rango; se documenta, no contradice (la cifra de V17 es una ilustración). (d) V17, tipos («frenó el precio» en 2022-2023): el horizonte de 8 trimestres de la contabilidad deja fuera del horizonte ese aumento del tipo, y en 2022T3-2026T2 solo cuenta la bajada posterior (de signo contrario): la contabilidad no contradice la afirmación, no la contrasta.\n")
    L.append("## 8. Limitaciones y desviaciones\n")
    L.append("- Magnitudes de la literatura (muchas «solo resumen» o NO VERIFICADAS) aplicadas a España; E7, E8 y E9 sin error típico; E1 con un solo estudio y unidades que no coinciden con la variación disponible (anuncios de Airbnb frente a registro HUT).\n- Factores sin variación comparable medida (E4, E5, E6) y turismo antes de 2018 (no medido, no cero).\n- Variación observada sin error; independencia entre factores (no hay dos magnitudes del mismo modelo, así que la sensibilidad a ρ = ±0,5 entre magnitudes no aplica).\n- Conversión de % a log (≈ igual) y efectos de nivel permanentes para E3, E8 y E9, que en la literatura son a 12 meses o promedios del periodo.\n- Ventanas de factor anuales (stock a 1 de enero) recortadas a los topes de sellado (2024 en el padrón y la población extranjera); los ITP usan fechas sin contraste con el BOE y solo desde 2010.\n- Desviaciones de la contabilidad respecto al plan: deflactor del PIB en lugar del IPC de V8; rangos de la literatura en lugar de posterior de B5 cuando B5 no da magnitud; Cantabria sin serie provincial; E1 y E2 solo en Barcelona y Cataluña (grandes ciudades solo València y Barcelona con dato no sellado); lectura de la adenda 1.10 explicada en la sección 3.\n")
    return "\n".join(L)


# ------------------------------------------------------------------------------------------------ salidas
def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    dat = Datos()
    dist = distribuciones()
    est = estados_b5()
    principal: list[dict] = []
    ilu: list[dict] = []
    construir_principal(dat, [(p[0], p[1], p[2]) for p in PERIODOS], "plan", principal, est)
    construir_principal(dat, PERIODOS_V8, "v8", principal, est, solo_nacional=True)
    construir_ilustracion(dat, dist, [(p[0], p[1], p[2]) for p in PERIODOS], "plan", ilu, est)
    construir_ilustracion(dat, dist, PERIODOS_V8, "v8", ilu, est)
    construir_ilustracion_locales(dat, dist, ilu)
    cp = pd.DataFrame(principal)
    ci = pd.DataFrame(ilu)
    ci = ci[(ci.alineacion == "plan") | (ci.territorio_tipo == "nacional")].reset_index(drop=True)
    cp.to_csv(OUT / "contabilidad.csv", index=False, encoding="utf-8", float_format="%.4f")
    ci.to_csv(OUT / "contabilidad_ilustracion.csv", index=False, encoding="utf-8", float_format="%.4f")
    v8 = comparar_v8(ci)
    v8.to_csv(OUT / "comparacion_v8.csv", index=False, encoding="utf-8", float_format="%.4f")
    resp = respuesta(cp, ci)
    resp.to_csv(OUT / "respuesta.csv", index=False, encoding="utf-8", float_format="%.4f")
    mag = pd.read_csv(OUT / "magnitudes.csv")
    estu = pd.read_csv(OUT / "magnitudes_estudios.csv")
    sens = pd.read_csv(OUT / "sensibilidad_b5.csv")
    h = hechos(mag, cp, ci)
    (OUT / "hechos.json").write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "informe.md").write_text(informe(mag, estu, sens, cp, ci, resp, v8), encoding="utf-8")
    print(f"contabilidad.csv: {len(cp)} filas; contabilidad_ilustracion.csv: {len(ci)} filas; hechos: {len(h)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
