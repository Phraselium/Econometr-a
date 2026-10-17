"""V16 · fase 5 · Validación Monte Carlo del DiD de intensidad (exposición continua × posterior): Q2a (provincial, wild bootstrap de Webb) y Q2c (municipal, agrupado por provincia).

Ejecución: python src/v16/montecarlo/did_intensidad_webb.py [--R 2000] [--B 399]   (SEED 20261010, k = 33)
Estructura real: 41 provincias de entrenamiento (centroides de data/base/geo/provincias.parquet), 391 municipios IPVA de entrenamiento y su provincia
(base_precio.parquet, solo el código); calendario Q2a 2017-2019 vs 2022-2025; Q2c 2021-2024. Resultado y exposición se SIMULAN.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_iv_espacial as C  # noqa: E402

HERR, K_SEM = "did_intensidad_webb", 33
BETA_REF = 0.04            # por DT de la exposición (log), magnitud de referencia del punto 3
SIG_P, SIG_M = 0.05, 0.08  # DT del ruido (log, anual) provincial y municipal
Z = 1.959964
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
PERIODOS_P = [2017, 2018, 2019, 2022, 2023, 2024, 2025]
POST_P = np.array([0, 0, 0, 1, 1, 1, 1], float)
PERIODOS_M = [2021, 2022, 2023, 2024]
POST_M = np.array([0, 0, 1, 1], float)


def estructura() -> dict:
    import shapely
    ge = pd.read_parquet(RAIZ_GEO, columns=["cod_provincia", "geometry"])
    a = pd.read_parquet(C.ENT / "base_alquiler.parquet", columns=["variable", "nivel", "territorio_codigo"])
    provs = sorted(a[(a.variable == "ipc_alquiler_indice") & (a.nivel == "provincia")].territorio_codigo.unique())
    ge = ge[ge.cod_provincia.isin(provs)].set_index("cod_provincia").loc[provs]
    c = shapely.centroid(shapely.from_wkb(ge.geometry.values))
    lon, lat = np.radians(shapely.get_x(c)), np.radians(shapely.get_y(c))
    xyz = 6371.0 * np.column_stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)])
    D = np.linalg.norm(xyz[:, None] - xyz[None], axis=2)
    b = pd.read_parquet(C.ENT / "base_precio.parquet", columns=["variable", "nivel", "territorio_codigo"])
    m = sorted(b[(b.variable == "ipva_tam_indice") & (b.nivel == "municipio")].territorio_codigo.unique())
    prov_m = pd.factorize(pd.Series(m).str[:2])[0]
    return {"D": D, "G": len(provs), "mun_prov": prov_m, "Nm": len(m), "Gm": int(prov_m.max() + 1)}


RAIZ_GEO = C.RAIZ / "data/base/geo/provincias.parquet"


def dgp_texto(e: dict) -> str:
    return f"""# did_intensidad_webb · Q2a (provincial, Webb) y Q2c (municipal, agrupado por provincia)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** Q2a: {e['G']} provincias de entrenamiento, periodos {PERIODOS_P} (2017-2019 frente a 2022-2025; 2020-2021 fuera), posterior = 2022+,
  distancias entre centroides de data/base/geo/provincias.parquet. Q2c: {e['Nm']} municipios con IPVA de entrenamiento en {e['Gm']} provincias (tamaños de cluster reales: de 1 a
  {int(np.bincount(e['mun_prov']).max())} municipios), años {PERIODOS_M}, posterior = 2023-2024 (la adenda fija «la misma regla que Q2a»; el corte 2023 es una convención de esta validación).
- **Exposición:** e_i ~ N(0,1) estandarizada (log de la exposición). Q2a: campo gaussiano con correlación espacial exp(-d/300 km). Q2c: 40 % de la varianza común dentro de la provincia, 60 % municipal, estandarizada.
- **Resultado Q2a:** y_it = β·e_i·post_t + σ_P·ε_it, σ_P = {SIG_P}; ε_it = √0,5·η_it + √0,3·(λ_i1 f_t1 + λ_i2 f_t2)/√2 + √0,2·u_it con η_it espacial (correlación exp(-d/300 km) entre provincias, AR(1) ρ = 0,7 en t),
  f factores comunes AR(1) ρ = 0,7, cargas λ ~ N(0,1) independientes de la exposición (la tendencia paralela se cumple), u AR(1) ρ = 0,5.
- **Resultado Q2c:** y_it = β·e_i·post_t + σ_M·ε_it, σ_M = {SIG_M}; ε_it = √0,35·v_{{prov(i)}}t (choque provincia-año común) + √0,15·f_t·λ_i + √0,5·u_it, con v, f AR(1) ρ = 0,5 y u AR(1) ρ = 0,3. Efectos fijos de unidad y de año (absorbidos).
- **Nulo:** β = 0. **Alternativa:** β = {BETA_REF} (por DT de la exposición): sesgo, RMSE, cobertura (inversión de la prueba en β = {BETA_REF}) y potencia.
- **Inferencias.** Q2a: wild cluster bootstrap con residuos restringidos, pesos de Webb de 6 puntos, B = bootstrap-t simétrico por provincia (principal, punto 3); referencia no candidata: CR1 por provincia con t(G-1).
  Q2c: CR1 agrupado por provincia con t(G-1) (principal, punto 3); Webb por provincia se informa como referencia extra (NO es la alternativa nombrada para Q2c, que no tiene ninguna).
- **Pocos clusters:** G = {e['G']} (Q2a) y {e['Gm']} muy desiguales (Q2c). **T corto:** 7 y 4 periodos.
- **Alternativa nombrada:** Q2a: Webb es la principal, sin otra; Q2c: ninguna. Si la principal no pasa → «NO APTO → diseño solo descriptivo».
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97] (cobertura de la prueba bootstrap invertida en el valor verdadero).
"""


def sim_p(rng, n, e):
    G, T = e["G"], len(PERIODOS_P)
    L = np.linalg.cholesky(np.exp(-e["D"] / 300.0) + 1e-9 * np.eye(G))
    ex = L @ rng.standard_normal((G, n))                       # (G, n)
    ex = (ex - ex.mean(0)) / ex.std(0)
    eta = np.einsum("ij,njt->nit", L, C.ar1(rng, (n, G, T), 0.7))
    f = C.ar1(rng, (n, 2, T), 0.7)
    lam = rng.standard_normal((n, G, 2))
    u = C.ar1(rng, (n, G, T), 0.5)
    eps = np.sqrt(0.5) * eta + np.sqrt(0.3) * np.einsum("nik,nkt->nit", lam, f) / np.sqrt(2) + np.sqrt(0.2) * u
    return ex.T, SIG_P * eps, POST_P


def sim_m(rng, n, e):
    N, G, T = e["Nm"], e["Gm"], len(PERIODOS_M)
    pm = e["mun_prov"]
    ex = np.sqrt(0.4) * rng.standard_normal((n, G))[:, pm] + np.sqrt(0.6) * rng.standard_normal((n, N))
    ex = (ex - ex.mean(1, keepdims=True)) / ex.std(1, keepdims=True)
    v = C.ar1(rng, (n, G, T), 0.5)[:, pm, :]
    f = C.ar1(rng, (n, T), 0.5)
    lam = rng.standard_normal((n, N))
    u = C.ar1(rng, (n, N, T), 0.3)
    eps = np.sqrt(0.35) * v + np.sqrt(0.15) * lam[:, :, None] * f[:, None, :] + np.sqrt(0.5) * u
    return ex, SIG_M * eps, POST_M


def dm2(a):
    return a - a.mean(-1, keepdims=True) - a.mean(-2, keepdims=True) + a.mean((-1, -2), keepdims=True)


def crit_t(t, df):
    return stats.t.ppf(0.975, df)


def cr1(xt, yt, cl, Gc):
    """Estimador y t de CR1 agrupado. xt, yt: (N,T) con FE ya quitados; cl: etiqueta de cluster por unidad."""
    sxx = (xt ** 2).sum()
    b = (xt * yt).sum() / sxx
    res = yt - b * xt
    sc = np.bincount(cl, weights=(xt * res).sum(1), minlength=Gc)
    se = np.sqrt((sc ** 2).sum() * Gc / (Gc - 1)) / sxx
    return b, se


def webb_p(xt, ytilde0, cl, Gc, B, rng, b_obs_t):
    """p-valor bootstrap-t simétrico con residuos restringidos (H0 impuesta en ytilde0 = demeaned(y - b0 x))."""
    N, T = xt.shape
    w = WEBB[rng.integers(0, 6, size=(B, Gc))][:, cl]          # (B,N)
    ystar = ytilde0[None] * w[:, :, None]
    ystar = dm2(ystar)
    sxx = (xt ** 2).sum()
    bs = (xt[None] * ystar).sum((1, 2)) / sxx
    res = ystar - bs[:, None, None] * xt[None]
    sc = np.zeros((B, Gc))
    s_i = (xt[None] * res).sum(2)                              # (B,N)
    np.add.at(sc.T, cl, s_i.T)
    se = np.sqrt((sc ** 2).sum(1) * Gc / (Gc - 1)) / sxx
    ts = bs / se
    return float((np.abs(ts) >= abs(b_obs_t)).mean())


def f_rep(rng, n, e=None, B=399, modo="P"):
    sim = sim_p if modo == "P" else sim_m
    ex, eps, post = sim(rng, n, e)
    cl = np.arange(e["G"]) if modo == "P" else e["mun_prov"]
    Gc = e["G"] if modo == "P" else e["Gm"]
    out = np.zeros((n, 12))
    for r in range(n):
        x = ex[r][:, None] * post[None, :]
        xt = dm2(x)
        fila = []
        for beta in (0.0, BETA_REF):
            y = beta * x + eps[r]
            for b0 in ((0.0,) if beta == 0.0 else (0.0, BETA_REF)):
                yt0 = dm2(y - b0 * x)
                b, se = cr1(xt, dm2(y), cl, Gc)
                t0 = (b - b0) / se
                tc = stats.t.ppf(0.975, Gc - 1)
                rej_cr = abs(t0) > tc
                p = webb_p(xt, yt0, cl, Gc, B, rng, t0)
                fila += [rej_cr, p < 0.05]
            if beta == 0.0:
                bh0 = b
            else:
                bh1 = b
        # fila: [cr(null), webb(null), cr(alt b0=0), webb(alt b0=0), cr(alt b0=ref), webb(alt b0=ref)]
        out[r, :6] = fila
        out[r, 6], out[r, 7] = bh0, bh1
    return out[:, :8]


def resumir(M, modo):
    R = len(M)
    nm = {"P": ["Webb (principal)", "CR1 por provincia (referencia)"], "M": ["CR1 por provincia (principal)", "Webb por provincia (referencia extra)"]}[modo]
    idx = {"P": (1, 0), "M": (0, 1)}[modo]          # columna de rechazo: 0=CR1, 1=Webb
    filas = []
    for nombre, j in zip(nm, idx):
        tam = M[:, j].mean()
        pot = M[:, 2 + j].mean()
        cob = 1 - M[:, 4 + j].mean()
        filas.append({"diseno": "Q2a provincial" if modo == "P" else "Q2c municipal", "inferencia": nombre, "R": R, "tamano_5pct": tam,
                      "tamano_ic95": str(C.ic_binomial(tam, R)), "cobertura_95": cob, "potencia_beta_ref": pot,
                      "sesgo": float(np.mean(M[:, 7] - BETA_REF)), "rmse": float(np.sqrt(np.mean((M[:, 7] - BETA_REF) ** 2)))})
    return filas


def main(R: int = 2000, B: int = 399):
    e = estructura()
    C.declarar_dgp(HERR, dgp_texto(e))
    filas, ver = [], {}
    for modo, k in (("P", 0), ("M", 1)):
        M = C.paralelo(f_rep, K_SEM * 10 + k, R, n_jobs=4, n_trozos=40, e=e, B=B, modo=modo)
        fs = resumir(M, modo)
        filas += fs
        ver["Q2a" if modo == "P" else "Q2c"] = C.veredicto(fs[0]["tamano_5pct"], len(M), fs[0]["cobertura_95"])
    tab = pd.DataFrame(filas)
    vf = {q: (v["veredicto"] if v["veredicto"] == "APTO" else "NO APTO → diseño solo descriptivo") for q, v in ver.items()}
    res = C.resultado_base("Q2a / Q2c (DiD de intensidad)", f"{e['G']} provincias x 7 periodos; {e['Nm']} municipios x 4 años en {e['Gm']} provincias",
                           "TWFE de exposición continua × posterior; Webb (Q2a) / CR1 por provincia (Q2c)", "simulados; estructura real (provincias, distancias, municipios IPVA)")
    res["estimacion"] = {"beta_ref_por_DT": BETA_REF}
    res["diagnosticos"] = {"veredicto": vf, "criterio": ver, "tabla": tab.to_dict("records"), "R": R, "B_bootstrap": B, "semilla": C.SEED}
    res["notas"] = ["Veredictos separados por diseño (Q2a, Q2c); el de Q2c no tiene alternativa nombrada."]
    md = f"## Resultados (R = {R} réplicas por diseño, B = {B}; semilla {C.SEED}, k = {K_SEM})\n\n{C.md_tabla(tab)}\n\n**Veredicto: Q2a {vf['Q2a']}; Q2c {vf['Q2c']}.**\n"
    for q, v in ver.items():
        if v["fallos"]:
            md += f"\n- {q}: condición que falla: {'; '.join(v['fallos'])}.\n"
    C.escribir_salidas(HERR, res, tab, md)
    print(tab.to_string())
    print(vf)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--B", type=int, default=399)
    a = ap.parse_args()
    main(a.R, a.B)
