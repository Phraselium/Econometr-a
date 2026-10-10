"""C3 (P-C3, topes Ley 11/2020): paneles de fianzas Incasòl (trimestral/anual) y SERPAVI municipal de Cataluña.
Pasos 1 y 2 del orden obligatorio: fianzas -> sellar_v3 (solo vuelve el entrenamiento); SERPAVI -> sellar_fuente_v3
(construido SIN mirarlo: ni describe ni estimación ni gráficos)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

D = RAIZ / "data/raw/v3"
SERPAVI = RAIZ / "data/raw/pdf/serpavi_v2_municipios.csv.gz"
TRIM = {"gener-març": 1, "abril-juny": 2, "juliol-setembre": 3, "octubre-desembre": 4}
PROV_CAT = ("08", "17", "25", "43")


def fianzas_panel() -> pd.DataFrame:
    """Municipio x periodo (trimestres discretos 2019Q1-2023Q4 y años completos 2007-2025). n = contratos totales;
    alq = renta media ponderada por nº de contratos de las medias de banda (las bandas cambian entre años)."""
    f = pd.read_csv(D / "incasol_fianzas_municipio_v3.csv.gz", usecols=["periodo", "serie", "valor", "codigo", "banda"],
                    dtype={"codigo": str})
    f["anio"] = f.periodo.str[:4].astype(int)
    lab = f.periodo.str[5:]
    f["q"] = lab.map(TRIM).fillna(0).astype(int)
    f["freq"] = np.where(lab == "gener-desembre", "A", np.where(f.q > 0, "Q", ""))
    f = f[f.freq != ""].copy()
    f["tipo"] = f.serie.str.split("_").str[3]
    k = ["codigo", "freq", "anio", "q"]
    n = f[(f.tipo == "n") & (f.banda == "TOTAL_bandas")].groupby(k).valor.sum().rename("n")
    nb = f[(f.tipo == "n") & (f.banda != "TOTAL_bandas")].set_index(k + ["banda"]).valor.rename("nb")
    r = f[f.tipo == "renta"].set_index(k + ["banda"]).valor.rename("renta")
    j = pd.concat([nb, r], axis=1).dropna()
    j["w"] = j.nb * j.renta
    g = j.groupby(level=list(range(4)))
    alq = (g.w.sum() / g.nb.sum()).rename("alq")
    cob = g.nb.sum().rename("nb_sum")
    p = pd.concat([n, alq, cob], axis=1).reset_index().rename(columns={"codigo": "cod_ine"})
    p["cob"] = p.nb_sum / p.n
    p = p[(p.n > 0) & (p.alq > 0)].drop(columns="nb_sum")
    return p.sort_values(["cod_ine", "freq", "anio", "q"]).reset_index(drop=True)


def serpavi_cat() -> pd.DataFrame:
    """Municipio x año 2018-2023, Cataluña: alq = mediana €/m²/mes de vivienda colectiva (VC); n_viv = nº de inmuebles
    en alquiler declarados en el IRPF (VC + VU; VU ausente cuenta 0 si hay VC). Definido antes de mirar los datos."""
    s = pd.read_csv(SERPAVI, usecols=["periodo", "codigo", "tipologia", "variable", "estadistico", "valor"],
                    dtype={"codigo": str})
    s["codigo"] = s.codigo.str.zfill(5)
    s = s[s.codigo.str[:2].isin(PROV_CAT) & s.periodo.between(2018, 2023)]
    a = s[(s.variable == "alquiler_m2") & (s.tipologia == "VC") & (s.estadistico == "mediana")]
    a = a.set_index(["codigo", "periodo"]).valor.rename("alq")
    nn = s[(s.variable == "n_contratos") & (s.estadistico == "recuento")].pivot_table(
        index=["codigo", "periodo"], columns="tipologia", values="valor", aggfunc="sum")
    nn = nn.reindex(columns=["VC", "VU"])
    nv = (nn.VC.fillna(0) + nn.VU.fillna(0)).where(nn.VC.notna() | nn.VU.notna()).rename("n_viv")
    p = pd.concat([a, nv], axis=1).reset_index().rename(columns={"codigo": "cod_ine", "periodo": "anio"})
    return p.sort_values(["cod_ine", "anio"]).reset_index(drop=True)


def construir_y_sellar():
    """Devuelve el panel de fianzas de ENTRENAMIENTO. El SERPAVI se sella sin devolverse."""
    fz = fianzas_panel()
    train = holdout.sellar_v3(fz, "c3_fianzas", col_codigo="cod_ine", col_municipio="cod_ine")
    holdout.sellar_fuente_v3(serpavi_cat(), "c3_serpavi")
    return train


def poblacion_censo2021() -> pd.Series:
    """Población residente por municipio (Censo 2021, suma de grandes grupos de edad de las secciones)."""
    e = pd.read_csv(D / "ine_v3_censo2021_seccion_edad.csv", usecols=["serie", "valor", "codigo"], dtype={"codigo": str})
    e = e[e.serie.str.startswith("EDAD")]
    e["mun"] = e.codigo.str.zfill(10).str[:5]
    return e.groupby("mun").valor.sum().rename("pop")
