"""V16 · fase 5 · Validación Monte Carlo de los errores de Conley a 2 km con efectos fijos de municipio (Q3-b).

Ejecución: python src/v16/montecarlo/conley_seccion.py [--R 2000]   (SEED 20261010, k = 32)
Estructura real: centroides de las secciones de entrenamiento con dato de alquiler SERPAVI en 2021 y 2024 (solo disponibilidad, nunca el valor)
de data/base/geo/secciones.parquet y data/processed/v16/entrenamiento/base_alquiler.parquet; unidad_sellada_v16 excluye las selladas.
El resultado y la exposición se SIMULAN con correlación espacial por distancia.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.spatial import cKDTree

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_iv_espacial as C  # noqa: E402

HERR, K_SEM = "conley_seccion", 32
CORTE_KM = 2.0
BETA_ALT = 0.05
RADIOS = {"principal: radio del campo 1,0 km (correlación nula más allá de 2 km)": 1.0,
          "sens: radio 0,5 km": 0.5, "sens: radio 1,5 km (correlación hasta 3 km, mayor que el corte)": 1.5}
Z = 1.959964


def estructura() -> dict:
    import shapely
    import holdout as H
    s = pd.read_parquet(RAIZ / "data/base/geo/secciones.parquet", columns=["cod_seccion", "cod_municipio", "cod_provincia", "geometry"])
    s = s[~H.unidad_sellada_v16(s.cod_seccion, "seccion")]
    a = pd.read_parquet(C.ENT / "base_alquiler.parquet", columns=["variable", "nivel", "territorio_codigo", "periodo", "valor"])
    a = a[(a.nivel == "seccion") & (a.variable == "serpavi_alquiler_m2_mediana") & a.periodo.isin(["2021", "2024"]) & a.valor.notna()]
    ok = a.groupby("territorio_codigo").periodo.nunique()
    ok = set(ok[ok == 2].index)
    s = s[s.cod_seccion.isin(ok)].copy()
    n_mun = s.groupby("cod_municipio").cod_seccion.transform("size")
    n_sec_total = len(s)
    s = s[n_mun > 1].sort_values(["cod_municipio", "cod_seccion"]).reset_index(drop=True)
    c = shapely.centroid(shapely.from_wkb(s.geometry.values))
    lon, lat = np.radians(shapely.get_x(c)), np.radians(shapely.get_y(c))
    xyz = 6371.0 * np.column_stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)])
    mun = pd.factorize(s.cod_municipio)[0]
    prov = pd.factorize(s.cod_provincia)[0]
    return {"xyz": xyz, "mun": mun, "prov": prov, "n": len(s), "n_mun": int(mun.max() + 1), "n_prov": int(prov.max() + 1), "n_sec_total": n_sec_total}


def matrices(est: dict, radio_campo: float):
    tree = cKDTree(est["xyz"])
    D = tree.sparse_distance_matrix(tree, max(CORTE_KM, radio_campo), output_type="coo_matrix")
    d, i, j = D.data, D.row, D.col
    n = est["n"]
    # diagonal (distancia 0 no se almacena en coo de sparse_distance_matrix con ceros): se añade explícita
    idx = np.arange(n)
    ii = np.concatenate([i, idx]); jj = np.concatenate([j, idx]); dd = np.concatenate([d, np.zeros(n)])
    # sparse_distance_matrix SÍ guarda la diagonal (distancia 0 explícita): el núcleo del estimador la toma una sola vez (corrección K16;
    # la versión anterior la sumaba dos veces). El campo W del proceso generador se deja como estaba (proceso declarado).
    fuera = np.concatenate([i != j, np.ones(n, dtype=bool)])
    kk = np.maximum(0.0, 1 - dd[fuera] / CORTE_KM)
    K = sp.csr_matrix((kk, (ii[fuera], jj[fuera])), shape=(n, n))
    w = np.maximum(0.0, 1 - dd / radio_campo)
    W = sp.csr_matrix((w, (ii, jj)), shape=(n, n))
    nrm = np.sqrt(np.asarray(W.multiply(W).sum(1)).ravel())
    W = sp.diags(1 / nrm) @ W
    return K, W.tocsr()


def dgp_texto(est: dict, K, nvec: float) -> str:
    return f"""# conley_seccion · Q3-b (corte transversal por sección, Conley a 2 km, efectos fijos de municipio)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** {est['n']:,} secciones de entrenamiento (de {est['n_sec_total']:,} con SERPAVI 2021 y 2024 disponibles, tras `unidad_sellada_v16`; se descartan las de
  municipios con una sola sección, cuyo efecto fijo las absorbe) en {est['n_mun']:,} municipios y {est['n_prov']} provincias; centroides de data/base/geo/secciones.parquet
  (distancia en km sobre esfera de 6.371 km). Vecinos medios dentro de 2 km (con la propia sección): {nvec:.1f}.
- **Exposición y resultado:** x_i = m^x_{{mun(i)}} + √0,6·z^x_i + √0,4·ξ^x_i;  y_i = β·x_i + h_{{mun(i)}}·(m^y_{{mun(i)}} + √0,6·z^y_i + √0,4·ξ^y_i), con efectos de municipio m ~ N(0,1) (absorbidos por el FE),
  ξ ruido idiosincrásico N(0,1), h_mun = exp(0,5·N(0,1)) (heterocedasticidad entre municipios), y z = campo gaussiano espacial con media móvil triangular de radio r sobre
  ruido blanco (correlación entre secciones positiva solo a menos de 2r; varianza unitaria). Los campos de x e y son independientes bajo el nulo.
- **Escenario principal:** r = 1,0 km (la correlación se anula a 2 km, el corte de Conley). **Sensibilidad (informativa):** r = 0,5 y 1,5 km (esta última deja correlación entre 2 y 3 km).
- **Nulo:** β = 0 (tamaño). **Alternativa:** β = {BETA_ALT} (DT de y por DT de x; Q3-b no tiene magnitud de referencia): sesgo, RMSE, cobertura y potencia.
- **Estimación:** MCO de y sobre x con efectos fijos de municipio (demedia intra-municipio). Inferencia: Conley con núcleo de Bartlett (triangular) a 2 km, normal.
  Si la varianza de Conley sale no positiva (el núcleo triangular no es semidefinido positivo en 2D) la réplica cuenta como no rechazo y se informa su frecuencia.
- **Corrección K16 (2026-10-18).** La primera ejecución sumaba dos veces la diagonal del núcleo (scipy ya la guarda con distancia 0), lo que inflaba el EE; con ese error salió APTO (tamaño 0,0435, cobertura 0,9565). La réplica ciega de Q3-b lo detectó. Esta tabla es la del núcleo correcto; el campo W del proceso generador no se ha cambiado.
  Referencias (no candidatas): EE robustos HC1 y EE agrupados por municipio.
- **Alternativa nombrada en el punto 3:** ninguna (Conley a 2 km es la principal). Si no pasa → «NO APTO → diseño solo descriptivo».
- **Pocos clusters / T corto:** corte transversal; dependencia por distancia; sin dimensión temporal.
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97].
"""


def f_rep(rng, n, est=None, K=None, W=None):
    N = est["n"]; mun = est["mun"]; G = est["n_mun"]; prov = est["prov"]
    cnt = np.bincount(mun, minlength=G).astype(float)
    # campos: (N, n)
    def campo(sx):
        z = W @ rng.standard_normal((N, n))
        return np.sqrt(0.6) * z + np.sqrt(0.4) * rng.standard_normal((N, n))
    mx = rng.standard_normal((G, n))
    my = rng.standard_normal((G, n))
    h = np.exp(0.5 * rng.standard_normal((G, n)))
    x = mx[mun] + campo(0)
    e = h[mun] * (my[mun] + campo(1))
    ini = np.r_[0, np.cumsum(cnt)[:-1]].astype(int)
    dm = lambda a: a - (np.add.reduceat(a, ini, axis=0) / cnt[:, None])[mun]
    xt = dm(x)
    out = []
    for beta in (0.0, BETA_ALT):
        yt = dm(beta * x + e)
        sxx = (xt ** 2).sum(0)
        bh = (xt * yt).sum(0) / sxx
        res = yt - bh * xt
        s = xt * res
        Ks = K @ s
        v_c = (s * Ks).sum(0)
        v_h = (s ** 2).sum(0)
        # agrupado por municipio
        cs = np.zeros((G, n)); np.add.at(cs, mun, s)
        v_g = (cs ** 2).sum(0) * G / (G - 1)
        out.append((bh, sxx, v_c, v_h, v_g))
    (b0, sx0, vc0, vh0, vg0), (b1, sx1, vc1, vh1, vg1) = out
    se = lambda v, sx: np.sqrt(np.maximum(v, 0)) / sx
    pos0, pos1 = vc0 > 0, vc1 > 0
    cols = [
        b0, b1,
        pos0 & (np.abs(b0) / np.where(pos0, se(vc0, sx0), 1) > Z), np.abs(b0) / se(vh0, sx0) > Z, np.abs(b0) / se(vg0, sx0) > Z,
        pos1 & (np.abs(b1) / np.where(pos1, se(vc1, sx1), 1) > Z), np.abs(b1) / se(vh1, sx1) > Z, np.abs(b1) / se(vg1, sx1) > Z,
        pos1 & (np.abs(b1 - BETA_ALT) <= Z * np.where(pos1, se(vc1, sx1), 1)), np.abs(b1 - BETA_ALT) <= Z * se(vh1, sx1), np.abs(b1 - BETA_ALT) <= Z * se(vg1, sx1),
        ~pos0, 2 * Z * se(vc1, sx1),
    ]
    return np.column_stack([np.asarray(c, dtype=float) for c in cols])


def resumir(M: np.ndarray) -> pd.DataFrame:
    R = len(M)
    filas = []
    for j, m in enumerate(["Conley 2 km", "HC1 (referencia)", "agrupado por municipio (referencia)"]):
        tam, cob = M[:, 2 + j].mean(), M[:, 8 + j].mean()
        filas.append({"inferencia": m, "R": R, "tamano_5pct": tam, "tamano_ic95": str(C.ic_binomial(tam, R)), "cobertura_95": cob,
                      "potencia_beta": M[:, 5 + j].mean(), "sesgo": float(np.mean(M[:, 1] - BETA_ALT)),
                      "rmse": float(np.sqrt(np.mean((M[:, 1] - BETA_ALT) ** 2))),
                      "var_no_positiva": float(M[:, 11].mean()) if j == 0 else float("nan")})
    return pd.DataFrame(filas)


def main(R: int = 2000):
    est = estructura()
    mats = {k: matrices(est, r) for k, r in RADIOS.items()}
    K0 = mats[list(RADIOS)[0]][0]
    nvec = K0.nnz / est["n"]
    C.declarar_dgp(HERR, dgp_texto(est, K0, nvec))
    tablas = []
    for esc in RADIOS:
        K, W = mats[esc]
        M = C.paralelo(f_rep, K_SEM, R if esc.startswith("principal") else max(C.R_MIN, R // 2), n_jobs=4, n_trozos=40, est=est, K=K, W=W)
        t = resumir(M)
        t.insert(0, "escenario", esc)
        tablas.append(t)
    tab = pd.concat(tablas, ignore_index=True)
    pr = tab[tab.escenario.str.startswith("principal")].set_index("inferencia")
    v = C.veredicto(float(pr.loc["Conley 2 km", "tamano_5pct"]), int(pr.loc["Conley 2 km", "R"]), float(pr.loc["Conley 2 km", "cobertura_95"]))
    sens = tab[(~tab.escenario.str.startswith("principal")) & (tab.inferencia == "Conley 2 km")]
    sens_ok = [bool(C.veredicto(r.tamano_5pct, int(r.R), r.cobertura_95)["veredicto"] == "APTO") for r in sens.itertuples()]
    if v["veredicto"] != "APTO":
        vf = "NO APTO → diseño solo descriptivo"
    elif all(sens_ok):
        vf = "APTO"
    else:
        vf = "APTO (solo escenario principal; no robusto a la sensibilidad del rango espacial)"
    res = C.resultado_base("Q3-b (correlación transversal por sección)", f"{est['n']} secciones, {est['n_mun']} municipios",
                           "MCO con FE de municipio y errores de Conley a 2 km", "simulados; geometría real de secciones de entrenamiento (solo estructura)")
    res["estimacion"] = {"beta_alt": BETA_ALT, "sesgo": float(pr.loc["Conley 2 km", "sesgo"]), "rmse": float(pr.loc["Conley 2 km", "rmse"])}
    res["diagnosticos"] = {"veredicto": vf, "criterio": v, "tamano_conley": float(pr.loc["Conley 2 km", "tamano_5pct"]),
                           "cobertura_conley": float(pr.loc["Conley 2 km", "cobertura_95"]), "potencia": float(pr.loc["Conley 2 km", "potencia_beta"]),
                           "tamano_hc1": float(pr.loc["HC1 (referencia)", "tamano_5pct"]), "R": int(pr.loc["Conley 2 km", "R"]), "semilla": C.SEED,
                           "vecinos_medios_2km": nvec,
                           "pasa_sensibilidad": dict(zip(sens.escenario, sens_ok))}
    res["notas"] = ["Sin magnitud de referencia en la adenda: potencia frente a beta = 0,05 DT/DT declarada en el proceso generador."]
    md = f"## Resultados (R = {R} réplicas en el escenario principal; semilla {C.SEED}, k = {K_SEM})\n\n{C.md_tabla(tab)}\n\n**Veredicto: {vf}.**\n"
    if v["veredicto"] == "APTO" and not all(sens_ok):
        md += ("\n**Advertencia.** El tamaño en el escenario principal (correlación espacial que se anula justo en el corte de 2 km) está en el intervalo, pero no se mantiene "
               "con campos de rango menor (tamaño conservador) ni mayor (sobre-rechazo): la calibración depende de que el corte coincida con el alcance de la correlación. "
               "Q3-b es C4 (correlación) y debe llevar esta advertencia.\n")
    if v["fallos"]:
        md += "\nCondición que falla: " + "; ".join(v["fallos"]) + ".\n"
    C.escribir_salidas(HERR, res, tab, md)
    print(tab.to_string())
    print(vf)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    main(ap.parse_args().R)
