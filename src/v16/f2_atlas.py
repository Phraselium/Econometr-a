"""V16-F2.3 · Atlas multiescala descriptivo (capa C4) con incertidumbre y supresión de celdas pequeñas.

Uso: python3 src/v16/f2_atlas.py [--smoke]   (SEED = 20261010; sin red; no lee data/sealed).
Salidas en output/v16/f2_atlas/: atlas.parquet, atlas.md, mapas/*.png, hechos.json, resultado.json, registro.csv.
Amplía el atlas de V10 (output/v10/atlas: coste por grupo, València, CV) con las fuentes nuevas de V16 y todas las escalas;
no repite sus tablas. Sin lenguaje causal: es un inventario descriptivo.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v16"))
import f2_atlas_datos as D  # noqa: E402
import f2_atlas_ind as I  # noqa: E402
from econ_utils import Registry  # noqa: E402

SAL = RAIZ / "output" / "v16" / "f2_atlas"
SEED = D.SEED


def construir(smoke: bool = False) -> pd.DataFrame:
    """Devuelve el atlas en formato largo, ordenado y sin unidades selladas."""
    np.random.seed(SEED)
    renta, hogar = I.adrh(smoke)
    alq, aux = I.serpavi(smoke)
    esf = I.esfuerzo(aux, hogar)
    park, viv_mun, _ = I.parque(smoke)
    partes = [renta, alq, esf, I.precio(smoke), I.vte(smoke, viv_mun), I.inside_airbnb(smoke, viv_mun), I.extranjera(smoke), park,
              I.lanzamientos(smoke, viv_mun), I.intervenciones(smoke), I.ecv_ccaa()]
    a = pd.concat(partes, ignore_index=True)
    a = a[a.valor.notna() | a.suprimida].copy()
    a = D.sin_sellados(a)  # cinturón de seguridad: ninguna unidad sellada llega al fichero
    a["territorio_codigo"] = a.territorio_codigo.astype(str)
    a = a.sort_values(["indicador", "nivel", "periodo", "territorio_codigo"], kind="mergesort").reset_index(drop=True)
    for c in ("valor", "ic_inf", "ic_sup", "n_base", "cv"):
        a[c] = a[c].astype("float64").round(6)
    return a


def registrar(a: pd.DataFrame, reg: Registry) -> None:
    for (ind, nivel), g in a.groupby(["indicador", "nivel"]):
        reg.log("f2_atlas", f"V16-ATL-{ind}-{nivel}", f"indicador {ind} a escala {nivel} [{g.fuente.iloc[0]}]", g.periodo.min(), g.periodo.max(),
                int(len(g)), np.nan, np.nan, np.nan,
                notas=f"C4 descriptivo; {int(g.suprimida.sum())} suprimidas; sin contraste de hipótesis (FDR no aplica)")


def main(smoke: bool = False) -> None:
    import f2_atlas_mapas as M
    import f2_atlas_texto as T
    out = SAL / "smoke" if smoke else SAL
    out.mkdir(parents=True, exist_ok=True)
    a = construir(smoke)
    a.to_parquet(out / "atlas.parquet", index=False, compression="zstd")
    reg = Registry(out / "registro.csv")
    registrar(a, reg)
    reg.flush()
    h = T.escribir(a, out, smoke)
    if not smoke:
        M.mapas(a, out / "mapas")
    print(f"atlas: {len(a):,} filas; {int(a.suprimida.sum()):,} suprimidas; {(out / 'atlas.parquet').stat().st_size / 1e6:.1f} MB; {len(h)} cifras")


if __name__ == "__main__":
    main("--smoke" in sys.argv)
